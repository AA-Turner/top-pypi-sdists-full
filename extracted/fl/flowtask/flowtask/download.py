"""
Plugin Downloader.
"""
import ssl
import io
from collections.abc import Callable
from pathlib import PurePath
import hashlib
import zipfile
from tqdm import tqdm
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.exceptions import InvalidSignature
import aiohttp
from aiohttp import ClientConnectorError
from navconfig.logging import logger
from .conf import MARKETPLACE_URL, PLUGINS_DIR, USE_SSL, MARKETPLACE_PUBLIC_KEY


def md5(fname):
    hash_md5 = hashlib.md5()
    hash_md5.update(open(str(fname), "rb").read())
    return hash_md5.hexdigest()


def read_line(filename):
    with open(filename, mode="r", encoding="utf-8") as fp:
        return fp.readline().strip()


def read_content(filename):
    with open(filename, "rb") as fp:
        return fp.read()


def verify_signature(filename: PurePath, signature):
    sign = read_content(signature)
    data = read_content(filename)
    public_key = load_pem_public_key(
        read_content(MARKETPLACE_PUBLIC_KEY), backend=default_backend
    )
    try:
        public_key.verify(sign, data, padding.PKCS1v15(), hashes.SHA256())
        return True
    except InvalidSignature:
        return False


async def download_component(component: str) -> Callable:
    url = f"{MARKETPLACE_URL}components/{component}"
    conn = aiohttp.TCPConnector(limit=100)
    try:
        async with aiohttp.ClientSession(connector=conn) as session:
            context = {}
            if USE_SSL is True:
                context = {"ssl": ssl.create_default_context()}
            async with session.get(url, **context) as response:
                if response.status == 200:
                    ### getting the stream binary zip
                    # Read the content of the response into a BytesIO buffer
                    zip_data = io.BytesIO(await response.read())
                    # Open the ZIP archive from the buffer
                    with zipfile.ZipFile(zip_data, "r") as zip_archive:
                        components_dir = PLUGINS_DIR.joinpath("components")
                        extracted = zip_archive.namelist()
                        logger.debug(f"Component Extracted: {extracted}")
                        signature = components_dir.joinpath(f"{component}.py.sign")
                        checksum = components_dir.joinpath(f"{component}.py.checksum")
                        cp = components_dir.joinpath(f"{component}.py")
                        # Loop over each file
                        for file in tqdm(
                            iterable=zip_archive.namelist(),
                            total=len(zip_archive.namelist()),
                        ):
                            zip_archive.extract(member=file, path=components_dir)
                        # zip_archive.extractall(components_dir)
                        ## then, first: check if component has a valid checksum
                        if md5(cp) == read_line(checksum):
                            checksum.unlink(missing_ok=True)
                        else:
                            checksum.unlink(missing_ok=True)
                            signature.unlink(missing_ok=True)
                            cp.unlink(missing_ok=True)
                            raise RuntimeError(
                                f"Failed Security Checksum for Component {component}"
                            )
                        # second, check signature from certificate:
                        if verify_signature(cp, signature):
                            return True
                        else:
                            ## if false, then remove the component code:
                            signature.unlink(missing_ok=True)
                            cp.unlink(missing_ok=True)
                            return False
                else:
                    logger.error(
                        f"Cannot Download Component {component} from Marketplace"
                    )
    except ClientConnectorError as e:
        logger.error(f"Error Connecting to Marketplace: {e}")
