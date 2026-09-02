"""Module that enables order management in eumdac CLI."""

import os
import random
import re
import shutil
import string
import threading
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import *

import yaml

from eumdac.config import get_config_dir
from eumdac.datatailor import DataTailor
from eumdac.errors import EumdacError
from eumdac.logging import gen_table_printer
from eumdac.product import Product
from eumdac.tailor_models import Chain


@dataclass
class ProductInfo:
    p_id: str
    p_dict: Dict[str, Any]


class Order:
    def __init__(self, order_file: Optional[Path] = None, order_dir: Optional[Path] = None):
        if order_dir is None:
            order_dir = get_default_order_dir()
        self._order_file = order_file or new_order_filename(order_dir)
        self._lock = threading.Lock()
        self._update_lock = threading.Lock()

    def initialize(
        self,
        chain: Optional[Chain],
        products: Iterable[Product],
        output_dir: Path,
        file_pattern: Optional[Iterable[str]],
        query: Optional[Dict[str, str]],
        dirs: bool = False,
        onedir: bool = False,
        no_warning_logs: bool = True,
    ) -> None:
        self._chain = chain
        self._output_dir = output_dir
        self._file_patterns = file_pattern
        self._no_warning_logs = no_warning_logs

        order_info: Dict[str, Any] = {
            "file_patterns": file_pattern,
            "output_dir": str(output_dir.resolve()),
            "query": query,
            "dirs": dirs,
            "onedir": onedir,
        }

        if chain:
            order_info["type"] = "tailor"
            order_info["chain"] = chain.asdict()
            order_info["products_to_process"] = {
                p._id: {
                    "col_id": p.collection._id,
                    "server_state": "UNSUBMITTED",
                    "customisation": None,
                }
                for p in products
            }
        else:
            order_info["type"] = "download"
            order_info["products_to_process"] = {
                p._id: {
                    "col_id": p.collection._id,
                    "server_state": "UNSUBMITTED",
                }
                for p in products
            }

        with self._lock:
            with self._order_file.open("w") as orf:
                yaml.dump(
                    order_info,
                    orf,
                )

    def __str__(self) -> str:
        return Path(self._order_file).stem

    def get_dict_entries(self, *args: str) -> Tuple[Optional[str], ...]:
        ret: List[Optional[str]] = []
        with self.dict_from_file() as order_d:
            for name in args:
                try:
                    ret.append(order_d[name])
                except KeyError:
                    ret.append(None)
        return tuple(ret)

    def status(self) -> str:
        if self.all_done():
            return "DONE"
        for p_info in self.iter_product_info():
            if p_info.p_dict["server_state"] in ("FAILED", "INACTIVE", "KILLED"):
                return "FAILED"
        return "NOT COMPLETED"

    def delete(self) -> None:
        os.remove(self._order_file)

    def move_to_failed(self) -> None:
        shutil.move(str(self._order_file), get_default_order_failed_dir() / self._order_file.name)

    def collections(self) -> List[str]:
        ret = []
        for p_info in self.iter_product_info():
            ret.append(p_info.p_dict["col_id"])
        return list(set(ret))

    def pretty_string(self, print_products: bool = False) -> str:
        ret_lines: List[str] = []
        (typ, query, chain, output_dir) = self.get_dict_entries(
            "type", "query", "chain", "output_dir"
        )
        ret = [
            f"Order {str(self)}",
            f"Status: {self.status()}",
            f"Collection: {self.collections()}",
            "Query:",
        ]
        query_dump = yaml.dump(query).strip()
        for line in query_dump.split("\n"):
            ret.append(f"    {line.rstrip()}")
        if chain:
            ret.append("Chain:")
            chain_dump = yaml.dump(chain).strip()
            for line in chain_dump.split("\n"):
                ret.append(f"    {line.rstrip()}")
        ret.append(f"Output directory: {output_dir}")
        if print_products:
            print_func = ret.append
            if typ == "tailor":
                printer = gen_table_printer(
                    print_func, [("Product", 60), ("Job Id", 10), ("Status", 12)]
                )
                for p_info in self.iter_product_info():
                    state = _compute_state(p_info.p_dict)
                    printer([p_info.p_id, p_info.p_dict["customisation"], state])
            elif typ == "download":
                printer = gen_table_printer(print_func, [("Product", 60), ("Status", 12)])
                for p_info in self.iter_product_info():
                    printer([p_info.p_id, p_info.p_dict["server_state"]])
            else:
                raise NotImplementedError(typ)
        return "\n".join(ret)

    def _locked_serialize(self, order_dict: Dict[str, Any]) -> None:
        with self._lock:
            with self._order_file.open("w") as orf:
                yaml.dump(order_dict, orf)

    @contextmanager
    def dict_from_file(self) -> Generator[Dict[str, Any], None, None]:
        with self._lock:
            ret_dict = self._deserialize()
        yield ret_dict

    def _deserialize(self) -> Dict[str, Any]:
        with self._order_file.open("r") as orf:
            ret_val = yaml.safe_load(orf)
        if ret_val is None:
            raise EumdacError(f"{self._order_file.resolve()} is corrupted.")
        return ret_val

    def remote_delete_failed(self, datatailor: DataTailor) -> None:
        for p_info in self.iter_product_info():
            if p_info.p_dict["server_state"] == "FAILED":
                customisation_id = p_info.p_dict["customisation"]
                if customisation_id:
                    try:
                        customisation = datatailor.get_customisation(customisation_id)
                        # Check the status of the job before deleting (it may already be deleted)
                        if customisation.status in ["FAILED", "KILLED"]:
                            customisation.delete()
                    except EumdacError:
                        continue

    def resolve_product_num(self, product_id: str) -> Tuple[int, int]:
        num_products = len(list(self.iter_product_info()))
        for num, p_info in enumerate(self.iter_product_info(), 1):
            if p_info.p_id == product_id:
                return num_products, num
        raise KeyError(product_id)

    def update(
        self,
        customisation_id: Optional[str],
        product_id: str,
        status: Optional[str] = None,
        download_states: Optional[Dict[str, str]] = None,
    ) -> None:
        with self._update_lock:
            with self.dict_from_file() as order:
                if status:
                    order["products_to_process"][product_id]["server_state"] = status
                if download_states:
                    order["products_to_process"][product_id]["download_states"] = download_states
                if customisation_id:
                    order["products_to_process"][product_id]["customisation"] = customisation_id
            self._locked_serialize(order)

    def reset_states(self) -> None:
        with self.dict_from_file() as order:
            products = order["products_to_process"]
        for prod_id, prod_info in products.items():
            if "download_states" in prod_info:
                del prod_info["download_states"]
            prod_info["server_state"] = "UNSUBMITTED"
            if order["type"] == "tailor":
                prod_info["customisation"] = None
        self._locked_serialize(order)

    def iter_product_info(self) -> Iterable[ProductInfo]:
        with self.dict_from_file() as order:
            orders = order["products_to_process"].items()
        for p_id, p_dict in orders:
            yield ProductInfo(p_id, p_dict)

    def get_products(self, datastore: Any) -> Iterable[Product]:
        for p_info in self.iter_product_info():
            yield datastore.get_product(p_info.p_dict["col_id"], p_info.p_id)

    def all_done(self) -> bool:
        (typ,) = self.get_dict_entries("type")
        if typ == "tailor":
            return self._all_done_tailor()
        elif typ == "download":
            return self._all_done_download()
        else:
            raise NotImplementedError(typ)

    def _all_done_tailor(self) -> bool:
        for p_info in self.iter_product_info():
            if not "download_states" in p_info.p_dict:
                return False
            for _fname, state in p_info.p_dict["download_states"].items():
                if state != "DOWNLOADED":
                    return False
        return True

    def _all_done_download(self) -> bool:
        return all([pi.p_dict["server_state"] == "DONE" for pi in self.iter_product_info()])


def _compute_state(p_dict: Dict[str, Any]) -> str:
    server_state = p_dict["server_state"]
    if server_state != "DONE":
        return server_state
    if not "download_states" in p_dict:
        return "DONE (NOT DOWNLOADED)"
    for _fname, state in p_dict["download_states"].items():
        if state != "DOWNLOADED":
            return "DONE (NOT DOWNLOADED)"
    return "DONE"


def get_default_order_dir() -> Path:
    order_dir = get_config_dir() / "orders" / "active"
    order_dir.mkdir(exist_ok=True, parents=True)
    return order_dir


def get_default_order_failed_dir() -> Path:
    failed_dir = get_config_dir() / "orders" / "failed"
    failed_dir.mkdir(exist_ok=True, parents=True)
    return failed_dir


def get_default_order_archive_dir() -> Path:
    archive_dir = get_config_dir() / "orders" / "archived"
    archive_dir.mkdir(exist_ok=True, parents=True)
    return archive_dir


def all_order_filenames(
    order_dir: Path,
    prefix: str = "",
) -> List[Path]:
    glob = "*.yml"
    if len(prefix) > 0:
        glob = f"{prefix}#*.yml"
    return sorted(order_dir.glob(glob), key=creation_time_of_order)


def creation_time_of_order(order_fn: Path) -> datetime:
    timeformat = r"(\d{4}-\d{2}-\d{2}#\d{6}\.\d{6})"
    m = re.match(timeformat, order_fn.name)
    if m is None:
        return datetime.fromtimestamp(order_fn.stat().st_ctime)
    return datetime.strptime(m.group(0), "%Y-%m-%d#%H%M%S.%f")


def latest_order_file(order_dir: Path) -> Path:
    filepaths = all_order_filenames(order_dir)
    return filepaths[-1]


def generate_order_name() -> str:
    now = datetime.now()
    order_prefix = f"{datetime.now().strftime('%Y-%m-%d')}"
    salt = generate_random_string(2)
    return f"{order_prefix}#{now.strftime('%H%M%S.%f')}_{salt}.yml"


def new_order_filename(order_dir: Path) -> Path:
    order_fn = order_dir / Path(generate_order_name())
    order_fn.touch(exist_ok=False)
    return order_fn


def resolve_order(order_dir: Path, order_name: str) -> Order:
    if order_name == "latest":
        filenames = list(all_order_filenames(order_dir))
        if len(filenames) == 0:
            raise EumdacError("No order files found.")
        return Order(latest_order_file(order_dir))
    return Order(order_dir / Path(f"{order_name}.yml"))


def generate_random_string(length: int = 12) -> str:
    # Define the character set: lowercase, uppercase, and digits
    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    # Randomly select characters from the character set
    random_string = "".join(random.choice(characters) for _ in range(length))
    return random_string
