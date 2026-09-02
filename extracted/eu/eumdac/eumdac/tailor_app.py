"""module containing the TailorApp which will be used when using
eumdac download **with** the --tailor argument."""

from __future__ import annotations

import concurrent
import fnmatch
import re
import shutil
import signal
import tempfile
import threading
import time
import typing
from collections import namedtuple
from datetime import timedelta
from pathlib import Path
from queue import Queue, Empty
from typing import Any, Callable, Dict, Generator, Iterable, List, Optional, Tuple

import eumdac.config
from eumdac.customisation import (
    Customisation,
    CustomisationError,
    UnableToGetCustomisationError,
)
from eumdac.datastore import DataStore
from eumdac.datatailor import DataTailor
from eumdac.errors import EumdacError
from eumdac.futures import EumdacFutureFunc, EumdacThreadPoolExecutor
from eumdac.job_id import JobIdentifier
from eumdac.logging import logger
from eumdac.order import Order
from eumdac.product import Product
from eumdac.signals import signal_registry
from eumdac.tailor_models import Chain


class FailedStateTransitionError(Exception):
    def __init__(self, msg: str, faillog: str) -> None:
        self.faillog = faillog
        super().__init__(msg)

    def find_lines(self, search_string: str) -> Generator[str, None, None]:
        if self.faillog:
            for line in self.faillog.splitlines():
                if search_string in line:
                    result_text = line.split(" - ")[-1]
                    yield result_text


class TailorApp:
    def __init__(
        self,
        order: Order,
        datastore: Any,
        datatailor: Any,
    ) -> None:
        self.server_state_monitor_executor = EumdacThreadPoolExecutor(max_workers=3)
        self.download_executor = EumdacThreadPoolExecutor(max_workers=2)
        self.datastore = datastore
        self.datatailor = datatailor
        self.order = order

        with self.order.dict_from_file() as order_d:
            self.output_dir = Path(order_d["output_dir"])
            self.output_dir.mkdir(exist_ok=True, parents=True)
            self.chain = Chain(**order_d["chain"])

        signal_registry.register(signal.SIGINT, self.handle_shutdown)

    def handle_shutdown(self) -> None:
        self.server_state_monitor_executor.shutdown(wait=False, cancel_futures=True)
        self.download_executor.shutdown(wait=False, cancel_futures=True)

    def run(self) -> bool:
        success = False
        try:
            success = self.resume()
        except FatalTailorError as fee:
            logger.error(f"Fatal error during execution: {fee}")
            self.order.remote_delete_failed(self.datatailor)

        signal_registry.unregister(signal.SIGINT, self.handle_shutdown)

        return success

    def shutdown(self) -> None:
        self.server_state_monitor_executor.pool_shutdown()
        self.download_executor.pool_shutdown()
        with self.order._lock:
            return

    def concurrent_download(
        self,
        products: Iterable[Product],
        output_dir: Path,
        customization_add_func: Callable[[Product], Customisation],
        timeout: float = 600,
    ) -> None:
        customisation_futures: List[concurrent.futures.Future[Any]] = []
        download_futures = []

        failed_customisations = []
        done_customistations = []

        num_jobs = len(list(self.order.iter_product_info()))
        job_identificator = JobIdentifier(num_jobs)
        customisation_blackboard: Queue[Customisation] = Queue()

        def cleanup_customisations() -> None:
            logger.info(f"Cleaning up customisations")
            while True:
                try:
                    c = customisation_blackboard.get(timeout=0.5)
                except Empty:
                    break

                logger.debug(f"Trying to clean up {c}")
                try:
                    if c.status not in ["DONE", "FAILED", "KILLED"]:
                        c.kill()
                except Exception as e:
                    # Job may be already over, it's ok if cancelling fails
                    logger.debug(f"Failed to kill {c}: {e}")

                try:
                    c.delete()
                except Exception as e:
                    logger.debug(f"Clean up {c} failed: {e}")

        signal_registry.register(signal.SIGINT, cleanup_customisations)

        for product in products:
            f = self.server_state_monitor_executor.pool_submit(
                WaitForDoneCustomisationFutureFunc(
                    customization_add_func,
                    self.order,
                    job_identificator,
                    customisation_blackboard,
                ),
                product,
            )
            if f is not None:
                customisation_futures.append(f)

        while customisation_futures:
            done_concurrent_futures: List[concurrent.futures.Future[Any]] = []
            not_done_concurrent_futures: List[
                concurrent.futures.Future[Any]
            ] = customisation_futures
            try:
                (
                    done_concurrent_futures,
                    not_done_concurrent_futures,
                ) = [
                    list(x)
                    for x in concurrent.futures.wait(
                        customisation_futures,
                        return_when=concurrent.futures.FIRST_COMPLETED,
                        timeout=0.1,
                    )
                ]
                for future in done_concurrent_futures:
                    customisation_futures.remove(future)
            except concurrent.futures.TimeoutError:
                pass

            # at this point done_concurrent_futures contain all finished customisations
            # now check if they failed and submit a task to download the result if success
            for done_future in done_concurrent_futures:
                try:
                    completed_customistation, product = done_future.result()
                    done_customistations.append(completed_customistation)
                except GracefulAbortError as graceful_abort_error:
                    logger.debug(f"External abort for {done_future}: {graceful_abort_error}")
                    continue
                except FatalTailorError as fatal_eumdac_error:
                    for future in customisation_futures:
                        future.cancel()
                    self.server_state_monitor_executor.pool_shutdown()
                    raise
                except CustomisationTimeoutError as te:
                    logger.error(f"{completed_customistation} timed out: {te}")
                    failed_customisations.append(completed_customistation)
                    continue
                except CustomisationError as ce:
                    logger.error(f"Failed: {ce}")
                    continue
                except Exception as exc:
                    logger.error(f"{done_future} failed: {exc}")
                    failed_customisations.append(done_future)
                    continue

                logger.debug(f"{completed_customistation} processed and ready to download.")

                f = self.download_executor.pool_submit(
                    DownloadRunFutureFunc(
                        self.order,
                        output_dir,
                        job_identificator.job_id_str(product),
                    ),
                    completed_customistation,
                    product,
                )
                if f is not None:
                    download_futures.append(f)

        # Allow interruptions to be processed while futures are running
        while True:
            if all([not x.running() for x in download_futures]):
                break
            time.sleep(0.1)

    def resume(self) -> bool:
        # handle existing customisations
        customisations = []
        products_to_resume = []
        products_to_repeat = []

        # query all customisation states
        success_customisation_product_futures = []

        try:
            user_name = self.datatailor.user_info["username"]
            quota_info = self.datatailor.quota["data"][user_name]
            if (
                quota_info["space_usage_percentage"]
                > eumdac.config.tailor_app_quota_percentage_warning
            ):
                logger.warning(f"Reaching maximum quota: {quota_info['space_usage_percentage']}%")
            elif quota_info["space_usage_percentage"] > 100:
                logger.warning(f"Over maximum quota: {quota_info['space_usage_percentage']}%")
        except EumdacError as e:
            # The quota call is unsupported by local-tailor, so we don't report
            if not self.datatailor.is_local:
                logger.warning(f"Could not determine current quota: {e}")

        for p_info in self.order.iter_product_info():
            f = self.server_state_monitor_executor.pool_submit(
                StateQueryFutureFunc(),
                p_info.p_id,
                p_info.p_dict,
                self.datatailor,
                self.datastore,
            )
            if f is not None:
                success_customisation_product_futures.append(f)

        done_success_customisation_product_futures, _ = concurrent.futures.wait(
            success_customisation_product_futures,
            return_when=concurrent.futures.ALL_COMPLETED,
        )
        for done_success_customisation_product_future in done_success_customisation_product_futures:
            (
                success,
                customisation,
                product,
            ) = done_success_customisation_product_future.result()
            if success:
                customisations.append(customisation)
                products_to_resume.append(product)
            else:
                products_to_repeat.append(product)

        if len(products_to_resume) > 0:
            self.concurrent_download(
                products_to_resume,
                self.output_dir,
                customization_add_func=GetCustomisation(customisations),
            )
        if len(products_to_repeat) > 0:
            self.concurrent_download(
                products_to_repeat,
                self.output_dir,
                customization_add_func=lambda x: self.datatailor.new_customisation(x, self.chain),
            )

        return True


class DownloadRunFutureFunc(EumdacFutureFunc):
    def __init__(self, order: Order, output_dir: Path, job_id: str):
        super().__init__()
        self.order = order
        self.output_dir = output_dir
        self.job_id = job_id

    @typing.no_type_check
    def __call__(
        self,
        customisation: Customisation,
        product: Product,
    ) -> None:
        results = customisation.outputs
        # compare with file_patterns from order_file
        (file_patterns,) = self.order.get_dict_entries("file_patterns")
        if file_patterns:
            filtered_results = []
            for pattern in file_patterns:
                matches = fnmatch.filter(results, pattern)
                filtered_results.extend(matches)
            results = filtered_results

        logger.debug(f"{self.job_id}: Starting download(s) for {results}")
        download_states = {result: "PENDING" for result in results}
        self.order.update(
            customisation._id,
            product._id,
            status=None,
            download_states=download_states,
        )

        with self.order.dict_from_file() as order_d:
            dirs = order_d["dirs"]

        num_total, num = self.order.resolve_product_num(product._id)
        for result in results:
            if self.aborted:
                break
            download_states[result] = "DOWNLOAD_ERROR"
            try:
                logger.info(
                    f"{self.job_id}: Downloading output of job {customisation._id} for {product._id}"
                )
                self.download_customisation_result(customisation, result, dirs)
                logger.info(f"{self.job_id}: {Path(result).parts[-1]} has been downloaded.")
                download_states[result] = "DOWNLOADED"
            except DownloadExistsError as err:
                logger.info(f"{self.job_id}: Skipping download. File exists: {err.product_path}")
                download_states[result] = "DOWNLOADED"
            except DownloadAbortedError as err:
                logger.warning(f"{self.job_id}: Download of {err.product_path} aborted")
            except Exception as exc:
                logger.error(f"{self.job_id}: Error while downloading: {exc}")

            self.order.update(
                customisation._id,
                product._id,
                status=None,
                download_states=download_states,
            )

        # delete serverside customisation on success
        if "DOWNLOAD_ERROR" not in download_states.values():
            logger.info(
                f"{self.job_id}: Deleting customization {customisation._id} for {product._id}"
            )
            customisation.delete()
        else:
            logger.warning(
                f"{self.job_id}: {customisation} download failed. Keeping customisation."
            )

    fatal_error_logs = {
        "ERROR": ["invalid", "INTERNAL ERROR"],
    }

    def download_customisation_result(
        self, customisation: Customisation, result: str, dirs: bool
    ) -> None:
        product_path = self.output_dir / Path(result).parts[-1]

        if dirs:
            # when the dirs flag is used
            # a subdirectory is created
            # to avoid overwriting common files
            output_subdir = self.output_dir / f"{Path(result).parts[0]}"
            output_subdir.mkdir(exist_ok=True)
            product_path = output_subdir / Path(result).parts[-1]

        if product_path.is_file():
            raise DownloadExistsError(product_path)

        with tempfile.TemporaryDirectory(dir=self.output_dir, suffix=".tmp") as tempdir:
            tmp_prod_p = Path(tempdir) / product_path.parts[-1]
            with tmp_prod_p.open("wb") as tmp_prod:
                with customisation.stream_output_iter_content(result) as chunks:
                    for chunk in chunks:
                        if self.aborted:
                            raise DownloadAbortedError(product_path)
                        tmp_prod.write(chunk)
            shutil.move(str(tmp_prod_p), str(product_path))


def check_invalid_state_transition_changelog(error: FailedStateTransitionError) -> None:
    fatal_error_logs = {
        "ERROR": ["INTERNAL ERROR", "incompatible"],
    }
    # find messages containing errors
    for severity, filters in fatal_error_logs.items():
        for line in error.find_lines(severity):
            if any(f in line for f in filters):
                desc = {"status": 200, "title": severity, "description": line}
                raise FatalTailorError(EumdacError(line, desc))


class StateQueryFutureFunc(EumdacFutureFunc):
    @typing.no_type_check
    def __call__(
        self,
        p_id: str,
        p_info: Dict[str, Any],
        datatailor: DataTailor,
        datastore: DataStore,
    ) -> Tuple[bool, Optional[Customisation], Optional[Product]]:
        if self.aborted:
            return False, None, None
        product = datastore.get_product(p_info["col_id"], p_id)
        customisation_id = p_info["customisation"]
        if customisation_id is None:
            return False, None, product
        customisation = datatailor.get_customisation(customisation_id)
        success = False
        try:
            _ = customisation.status
            success = True
        except (CustomisationError, CustomisationTimeoutError) as ce:
            download_states = {}
            if "download_states" in p_info:
                download_states = p_info["download_states"]

            if "DOWNLOADED" in download_states.values():
                logger.warning(
                    f"Customisation {customisation_id} has already been finished and downloaded."
                )
            else:
                logger.warning(f"Could not restore customisation for {customisation_id}: {ce}")
                try:
                    if customisation:
                        customisation.delete()
                except:
                    pass

        return success, customisation, product


class GetCustomisation:
    def __init__(self, customisations: List[Customisation]):
        self.cnt = 0
        self.customisations = customisations
        self.lock = threading.Lock()

    def __call__(self, _product: Product) -> Customisation:
        with self.lock:
            result = self.customisations[self.cnt]
            if self.cnt < len(self.customisations):
                self.cnt += 1
            return result


State = namedtuple("State", "name log")


class WaitForDoneCustomisationFutureFunc(EumdacFutureFunc):
    def __init__(
        self,
        customization_add_func: Callable[[Product], Customisation],
        order: Order,
        job_identificator: JobIdentifier,
        customisation_blackboard: Queue[Customisation],
        timeout: float = 1800,
        polling_interval: float = 1.0,
        max_retries: int = -1,
        max_timeouts: int = 3,
        wait_timedelta: timedelta = timedelta(seconds=5.0),
    ) -> None:
        super().__init__()
        self.customization_add_func = customization_add_func
        self.order = order
        self.job_identificator = job_identificator
        self.customisation_blackboard = customisation_blackboard
        self.timeout = timeout
        self.polling_interval = polling_interval
        if max_retries < 0:
            max_retries = eumdac.config.tailor_app_max_retries
        self.max_retries = max_retries
        self.max_timeouts = max_timeouts
        self.wait_timedelta = wait_timedelta

        self.terminated = False
        self.failed = False
        self.state = State("UNSUBMITTED", "")
        self.state_transitions: Dict[str, List[str]] = {
            "UNSUBMITTED": ["QUEUED", "RUNNING", "DONE", "FAILED", "INACTIVE", "KILLED"],
            "QUEUED": ["QUEUED", "RUNNING", "DONE", "FAILED", "INACTIVE", "KILLED"],
            "RUNNING": ["RUNNING", "DONE", "FAILED", "INACTIVE", "KILLED"],
            "DONE": [],
            "FAILED": [],
            "INACTIVE": ["KILLED"],
            "KILLED": ["KILLED"],
        }
        self.timed_out = False
        self.job_identificator = job_identificator
        self.job_id = "(? / ?)"

    @typing.no_type_check
    def __call__(
        self,
        product: Product,
    ) -> Optional[Customisation]:
        if self.aborted:
            return

        # Set the job id only when the Future is actually called by the Scheduler to ensure
        # (somewhat) correct ordering.
        self.job_identificator.register(product)
        self.job_id = self.job_identificator.job_id_str(product)

        logger.info(f"Triggering {self.job_id.lower()} of {self.job_identificator.total_jobs}")
        logger.debug(
            f"{self.job_id} tracked as {self.job_identificator.registered_objects[product]}"
        )
        customisation = self.try_to_add_customisation(product)
        self.customisation_blackboard.put(customisation)
        return self.wait_for_success(customisation, product)

    def try_to_add_customisation(self, product: Product) -> Optional[Customisation]:
        retries = 0
        while True:
            if self.aborted:
                raise GracefulAbortError("Abort requested.")

            if retries >= self.max_retries:
                raise CustomisationError(
                    f"{self.job_id}: Could not add customisation after {retries} retries"
                )
            try:
                return self.customization_add_func(product)
            except EumdacError as e:
                retries += 1
                try:
                    check_error_response(e)
                except ExceedingNumberOfCustomisationsEumdacError as _exceeding_number_error:
                    pass

                logger.warning(
                    f"{self.job_id}: {e}: Could not create customisation. Retry: {retries}"
                )
                time.sleep(self.wait_timedelta.total_seconds())

    def wait_for_success(
        self, customisation: Customisation, product: Product
    ) -> Tuple[Customisation, Product]:
        retries = 0
        timeouts = 0
        while retries < self.max_retries:
            if self.aborted:
                break
            self.state_timer = self.windup_timer()
            try:
                while not self.aborted and not self.terminated:
                    self.step(customisation, product._id)
                    if self.timed_out:
                        logger.error(f"{self.job_id}: {self} timed_out")
                        retries += 1
                        timeouts += 1
                        if timeouts >= self.max_timeouts:
                            raise FatalTailorError(
                                EumdacError(f"{self.job_id}: {customisation._id} timed out")
                            )
                break
            except FailedStateTransitionError as fste:
                logger.debug(f"{fste}: {fste.faillog}")
                check_invalid_state_transition_changelog(fste)

                if customisation:
                    if self.state.name == "INACTIVE":
                        customisation.kill()
                    customisation.delete()

                retries += 1
                logger.warning(
                    f"{self.job_id}: Customisation {customisation._id} for {product} failed on attempt {retries}/{self.max_retries}"
                )
                if retries < self.max_retries:
                    # if we retry this reinitialize state
                    self.state = State("UNSUBMITTED", "")

                while retries < self.max_retries:
                    ret_customisation = self.try_to_add_customisation(product)
                    if ret_customisation:
                        customisation = ret_customisation
                        break
                    retries += 1

            finally:
                self.state_timer.cancel()
                if retries >= self.max_retries:
                    raise FatalTailorError(
                        EumdacError(f"{self.job_id}: All attempts failed for {product}")
                    )

        return customisation, product

    def step(self, customisation: Customisation, product_id: str) -> None:
        self.transition(customisation, product_id)

        self.terminated = self.state.name == "DONE"
        self.failed = self.state.name in ["FAILED", "INACTIVE", "KILLED"]
        if self.terminated:
            return
        if self.failed:
            logs = self.get_latest_log(customisation)
            if not getattr(self.order, "_no_warning_logs", None):
                log_message = logs.split("\n\n")
                logger.warning(f"{self.job_id}: {log_message[-1]}")
            raise FailedStateTransitionError(
                f"{self.job_id}: Server state is: {self.state.name}",
                faillog=logs,
            )

        if self.state.name not in self.state_transitions.keys():
            raise InvalidStateTransitionError(
                "{self.job_id}: Unexpected State: {self.state.name})",
                old_state=self.state,
                new_state=State(self.state.name, self.get_latest_log(customisation)),
            )

    def transition(
        self,
        customisation: Customisation,
        product_id: str,
    ) -> None:
        new_state = customisation.status
        if self.state.name != new_state:
            logger.debug(
                f"{self.job_id}: {customisation}: State change: {self.state.name} -> {new_state}"
            )
            num_total, num = self.order.resolve_product_num(product_id)
            suffix = {
                "QUEUED": "is now queued",
                "RUNNING": "is now running",
                "DONE": "has finished",
                "FAILED": "has failed",
                "INACTIVE": "is inactive",
                "KILLED": "has been cancelled",
            }
            logger.info(
                f"{self.job_id}: Customisation {customisation._id} for {product_id} {suffix[new_state]}"
            )

        if new_state not in self.state_transitions[self.state.name]:
            self.state_timer.cancel()
            raise InvalidStateTransitionError(
                f"{self.job_id}: Tried to transition from state {self.state} to {new_state}, "
                "which is not expected",
                old_state=self.state,
                new_state=State(new_state, self.get_latest_log(customisation)),
            )
        elif self.state.name != new_state:
            self.state_timer.cancel()
            self.state_timer = self.windup_timer()
            self.state = State(new_state, self.get_latest_log(customisation))
            if self.order:
                self.order.update(
                    customisation._id,
                    product_id,
                    self.state.name,
                )

    def windup_timer(self) -> threading.Timer:
        logger.debug(f"{self.job_id}: {repr(self)} windup_timer")
        timer = threading.Timer(self.timeout, self.on_timeout)
        timer.start()
        return timer

    def on_timeout(self) -> None:
        logger.debug(f"{self.job_id}: {repr(self)} on_timeout")
        self.timed_out = True

    def get_latest_log(self, customisation: Customisation) -> str:
        try:
            return customisation.logfile
        except UnableToGetCustomisationError:
            return "Unable to get logs"


class InvalidStateTransitionError(EumdacError):
    def __init__(self, msg: str, old_state: State, new_state: State) -> None:
        self.old_state = old_state
        self.new_state = new_state
        super().__init__(msg)


class CustomisationTimeoutError(EumdacError):
    """Error raised during downloads"""


class DownloadError(EumdacError):
    """Error raised during downloads"""

    def __init__(self, product_path: Path, *args: Any) -> None:
        super().__init__(msg=str(product_path))
        self.product_path = product_path


class DownloadAbortedError(DownloadError):
    """Error raised when a download is aborted"""


class DownloadExistsError(DownloadError):
    """Error raised when a download file already exists"""


class GracefulAbortError(EumdacError):
    """Error related to abort conditions when creating customisations"""


class FatalTailorError(EumdacError):
    """Unrecoverable Error"""

    def __init__(self, eumdac_error: EumdacError):
        msg = "Unrecoverable Data Tailor error"
        if not eumdac_error.extra_info:
            msg += f" - {str(eumdac_error)}"
        super().__init__(msg, eumdac_error.extra_info)


class ExceedingNumberOfCustomisationsEumdacError(EumdacError):
    """Error for server responding that maximum number of customisations is reached"""

    def __init__(self, eumdac_error: EumdacError, number_of_customisations: int):
        super().__init__(eumdac_error.args[0], eumdac_error.extra_info)
        self.number_of_customisations = number_of_customisations


def check_error_response(error: Exception) -> None:
    """helper function to check error responses from the server"""
    fatal_error_responses = {
        400: [""],
    }

    number_of_customisation_responses = {
        500: ["You are exceeding your maximum number"],
    }

    if isinstance(error, EumdacError):
        if (
            error.extra_info
            and error.extra_info["status"] in fatal_error_responses
            and "description" in error.extra_info
        ):
            if any(
                fatal_response in error.extra_info["description"]
                for fatal_response in fatal_error_responses[error.extra_info["status"]]
            ):
                raise FatalTailorError(error)

        if (
            error.extra_info
            and error.extra_info["status"] in number_of_customisation_responses
            and "description" in error.extra_info
        ):
            if any(
                number_response in error.extra_info["description"]
                for number_response in number_of_customisation_responses[error.extra_info["status"]]
            ):
                response_match = re.search(r"([\d]+)", error.extra_info["description"])
                if response_match:
                    number = int(response_match[0])
                else:
                    number = -1
                raise ExceedingNumberOfCustomisationsEumdacError(error, number)

    else:
        return
