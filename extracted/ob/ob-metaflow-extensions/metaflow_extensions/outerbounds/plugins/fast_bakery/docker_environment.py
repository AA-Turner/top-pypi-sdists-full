import hashlib
import json
import os
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from typing import Dict

from metaflow.exception import MetaflowException
from metaflow.metaflow_config import FAST_BAKERY_URL, get_pinned_conda_libs
from metaflow.metaflow_environment import MetaflowEnvironment
from metaflow.plugins.aws.batch.batch_decorator import BatchDecorator
from metaflow.plugins.kubernetes.kubernetes_decorator import KubernetesDecorator
from metaflow.plugins.pypi.conda_decorator import CondaStepDecorator
from metaflow.plugins.pypi.conda_environment import CondaEnvironment
from metaflow.plugins.pypi.pypi_decorator import PyPIStepDecorator
from metaflow import decorators

from .fast_bakery import FastBakery, FastBakeryApiResponse, FastBakeryException

BAKERY_METAFILE = ".imagebakery-cache"

import fcntl
import json
import os
from concurrent.futures import ThreadPoolExecutor
from functools import wraps


def cache_request(cache_file):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            call_args = kwargs.copy()
            call_args.update(zip(func.__code__.co_varnames, args))
            call_args.pop("self", None)
            call_args.pop("ref", None)
            # invalidate cache when moving from one deployment to another
            call_args.update({"fast_bakery_url": FAST_BAKERY_URL})
            cache_key = hashlib.md5(
                json.dumps(call_args, sort_keys=True).encode("utf-8")
            ).hexdigest()

            try:
                with open(cache_file, "r") as f:
                    cache = json.load(f)
                    if cache_key in cache:
                        return FastBakeryApiResponse(cache[cache_key])
            except (FileNotFoundError, json.JSONDecodeError):
                cache = {}

            result = func(*args, **kwargs)

            try:
                with open(cache_file, "r+") as f:
                    fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                    try:
                        f.seek(0)
                        cache = json.load(f)
                    except json.JSONDecodeError:
                        cache = {}

                    cache[cache_key] = result.response

                    f.seek(0)
                    f.truncate()
                    json.dump(cache, f)
            except FileNotFoundError:
                # path to cachefile might not exist.
                os.makedirs(os.path.dirname(cache_file), exist_ok=True)
                with open(cache_file, "w") as f:
                    fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                    json.dump({cache_key: result.response}, f)

            return result

        return wrapper

    return decorator


class DockerEnvironmentException(MetaflowException):
    headline = "Ran into an error while baking image"

    def __init__(self, msg):
        super(DockerEnvironmentException, self).__init__(msg)


class DockerEnvironment(MetaflowEnvironment):
    TYPE = "fast-bakery"
    _filecache = None
    _force_rebuild = False

    def __init__(self, flow):
        self.skipped_steps = set()
        self.flow = flow

        self.results = {}
        self.images_baked = 0

    def set_local_root(self, local_root):
        self.local_root = local_root

    def decospecs(self):
        # Due to conflicts with the CondaEnvironment fallback and bakery,
        # we can not simply attach 'conda' or 'pypi' to all steps here.
        # Instead we do this on a per-step basis in init_environment
        return ("fast_bakery_internal",) + super().decospecs()

    def validate_environment(self, logger, datastore_type):
        self.datastore_type = datastore_type
        self.logger = logger

        # Avoiding circular imports.
        from metaflow.plugins import DATASTORES

        self.datastore = [d for d in DATASTORES if d.TYPE == self.datastore_type][0]

    def init_environment(self, echo):
        self.skipped_steps = {
            step.name for step in self.flow if not _step_executes_remotely(step)
        }
        # Attach environment decorator as needed. This is done on a step-by-step basis
        # as we require a conda decorator for fallback steps, but prefer pypi for the baked ones.
        for step in self.flow:
            # Mixing @pypi/@conda in a single step is not supported yet.
            # We validate this before attaching any new ones as the OSS Conda environment requires an implicit conda decorator for pypi environments which would fail the validation.
            if sum(1 for deco in step.decorators if _is_env_deco(deco)) > 1:
                raise MetaflowException(
                    "Mixing and matching PyPI packages and Conda packages within a\n"
                    "step is not yet supported. Use one of @pypi or @conda only for the *%s* step."
                    % step.name
                )
            if step.name in self.skipped_steps:
                # Conda fallback requires a conda decorator as the default for a step
                decorators._attach_decorators_to_step(step, ["conda"])
            else:
                if not _step_has_environment_deco(step):
                    # We default to PyPI for steps that are going to be baked.
                    decorators._attach_decorators_to_step(step, ["pypi"])
                    # init the attached decorator
            # Initialize the decorator we attached.
            # This is crucial for the conda decorator to work properly in the fallback environment
            decorators._init(self.flow)
            for deco in step.decorators:
                if _is_env_deco(deco):
                    deco.step_init(
                        self.flow,
                        None,  # not passing graph as it is not available, and not required by conda/pypi decorators
                        step.name,
                        step.decorators,
                        self,
                        self.datastore,
                        echo,
                    )

        steps_to_bake = [
            step
            for step in self.flow
            if step.name not in self.skipped_steps and not self.is_disabled(step)
        ]
        if steps_to_bake:
            self.logger("🚀 Baking container image(s) ...")
            start_time = time.time()
            self.results = self._bake(steps_to_bake)
            for step in steps_to_bake:
                for d in step.decorators:
                    if _is_remote_deco(d):
                        d.attributes["image"] = self.results[step.name].container_image
                        d.attributes["executable"] = self.results[step.name].python_path
            if self.images_baked > 0:
                bake_time = time.time() - start_time
                self.logger(
                    f"🎉 All container image(s) baked in {bake_time:.2f} seconds!"
                )
            else:
                self.logger("🎉 All container image(s) baked!")

        if self.skipped_steps:
            self.delegate = CondaEnvironment(self.flow)
            self.delegate._force_rebuild = self._force_rebuild
            self.delegate.set_local_root(self.local_root)
            self.delegate.validate_environment(echo, self.datastore_type)
            self.delegate.init_environment(echo, self.skipped_steps)

    def _bake(self, steps) -> Dict[str, FastBakeryApiResponse]:
        metafile_path = get_fastbakery_metafile_path(self.local_root, self.flow.name)
        if self._force_rebuild:
            # clear the metafile if force rebuilding, effectively skipping the cache.
            try:
                os.remove(metafile_path)
            except Exception:
                pass

        logger_lock = threading.Lock()

        @cache_request(metafile_path)
        def _cached_bake(
            ref=None,
            python=None,
            pypi_packages=None,
            conda_packages=None,
            base_image=None,
        ):
            try:
                bakery = FastBakery(url=FAST_BAKERY_URL)
                bakery._reset_payload()
                bakery.python_version(python)
                bakery.pypi_packages(pypi_packages)
                bakery.conda_packages(conda_packages)
                bakery.base_image(base_image)
                if self._force_rebuild:
                    bakery.ignore_cache()

                with logger_lock:
                    self.logger(f"🍳 Baking [{ref}] ...")
                    self.logger(f"     🐍 Python: {python}")

                    if pypi_packages:
                        self.logger(f"     📦 PyPI packages:")
                        for package, version in pypi_packages.items():
                            self.logger(f"        🔧 {package}: {version}")

                    if conda_packages:
                        self.logger(f"     📦 Conda packages:")
                        for package, version in conda_packages.items():
                            self.logger(f"        🔧 {package}: {version}")

                    self.logger(f"     🏗️  Base image: {base_image}")

                start_time = time.time()
                res = bakery.bake()
                # TODO: Get actual bake time from bakery
                bake_time = time.time() - start_time

                with logger_lock:
                    self.logger(f"🏁 Baked [{ref}] in {bake_time:.2f} seconds!")
                self.images_baked += 1
                return res
            except FastBakeryException as ex:
                raise DockerEnvironmentException(f"Bake [{ref}] failed: {str(ex)}")

        def prepare_step(step):
            base_image = next(
                (
                    d.attributes.get("image")
                    for d in step.decorators
                    if isinstance(d, (KubernetesDecorator))
                ),
                None,
            )
            dependencies = next(
                (d for d in step.decorators if _is_env_deco(d)),
                None,
            )
            python = next(
                (
                    d.attributes["python"]
                    for d in step.decorators
                    if isinstance(d, CondaStepDecorator)
                ),
                None,
            )
            pypi_deco = next(
                (d for d in step.decorators if isinstance(d, PyPIStepDecorator)), None
            )
            # if pypi decorator is set and user has specified a python version, we must create a new environment.
            # otherwise rely on the base environment
            if pypi_deco is not None:
                python = (
                    pypi_deco.attributes["python"]
                    if pypi_deco.is_attribute_user_defined("python")
                    else None
                )

            packages = get_pinned_conda_libs(python, self.datastore_type)
            packages.update(dependencies.attributes["packages"] if dependencies else {})

            requested = {
                "python": python,
                "pypi_packages": (
                    packages if isinstance(dependencies, PyPIStepDecorator) else None
                ),
                "conda_packages": (
                    packages if isinstance(dependencies, CondaStepDecorator) else None
                ),
                "base_image": base_image,
            }
            dedup_key = hashlib.sha256(
                json.dumps(requested).encode("utf-8")
            ).hexdigest()

            return step.name, dedup_key, requested

        with ThreadPoolExecutor() as executor:
            prepared_args = list(executor.map(prepare_step, steps))
            # Deduplicate the requests for baking images of steps.
            # We do not want to bake the same image twice.
            dedup_requests = {}
            for step_name, key, args in prepared_args:
                if key not in dedup_requests:
                    dedup_requests[key] = {"step_names": set(), "args": args}
                dedup_requests[key]["step_names"].add(step_name)

            # unique futures
            futures = []
            for i, kv in enumerate(dedup_requests.items(), 1):
                key, value = kv
                future = executor.submit(
                    _cached_bake, **{**value["args"], "ref": f"#{i:02d}"}
                )
                futures.append({"step_names": value["step_names"], "future": future})

            results = {}
            for item in futures:
                for step_name in item["step_names"]:
                    results[step_name] = item["future"].result()

            return results

    def executable(self, step_name, default=None):
        if step_name in self.skipped_steps:
            return self.delegate.executable(step_name, default)
        # default is set to the right executable
        if default is not None:
            return default
        if default is None and step_name in self.results:
            # try to read pythonpath from results. This can happen immediately after baking.
            return self.results[step_name].python_path
        # we lack a default and baking results. fallback to parent executable.
        return super().executable(step_name, default)

    def interpreter(self, step_name):
        if step_name in self.skipped_steps:
            return self.delegate.interpreter(step_name)
        return None

    def is_disabled(self, step):
        for decorator in step.decorators:
            # @conda decorator is guaranteed to exist thanks to self.decospecs
            if decorator.name in ["conda", "pypi"]:
                # handle @conda/@pypi(disabled=True)
                disabled = decorator.attributes["disabled"]
                return str(disabled).lower() == "true"
        return False

    def pylint_config(self):
        config = super().pylint_config()
        # Disable (import-error) in pylint
        config.append("--disable=F0401")
        return config

    def get_package_commands(
        self, codepackage_url, datastore_type, code_package_metadata=None
    ):
        # we must set the skip install flag at this stage in order to skip package downloads,
        # doing so in bootstrap_commands is too late in the lifecycle.
        return [
            "export METAFLOW_SKIP_INSTALL_DEPENDENCIES=$FASTBAKERY_IMAGE",
        ] + super().get_package_commands(
            codepackage_url, datastore_type, code_package_metadata=code_package_metadata
        )

    def bootstrap_commands(self, step_name, datastore_type):
        if step_name in self.skipped_steps:
            return self.delegate.bootstrap_commands(step_name, datastore_type)
        return super().bootstrap_commands(step_name, datastore_type)


def get_fastbakery_metafile_path(local_root, flow_name):
    return os.path.join(local_root, flow_name, BAKERY_METAFILE)


def _is_remote_deco(deco):
    return isinstance(deco, (BatchDecorator, KubernetesDecorator))


def _step_executes_remotely(step):
    "Check if a step is going to execute remotely or locally"
    return any(_is_remote_deco(deco) for deco in step.decorators)


def _is_env_deco(deco):
    "Check if a decorator is a known environment decorator (conda/pypi)"
    return isinstance(deco, (PyPIStepDecorator, CondaStepDecorator))


def _step_has_environment_deco(step):
    "Check if a step has a virtual environment decorator"
    return any(_is_env_deco(deco) for deco in step.decorators)
