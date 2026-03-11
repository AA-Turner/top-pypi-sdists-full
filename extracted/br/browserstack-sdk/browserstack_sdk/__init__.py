# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import atexit
import shlex
import signal
import yaml
import socket
import datetime
import string
import random
import collections.abc
import traceback
import copy
import threading
import time
import inspect
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import json
from browserstack_sdk.sdk_cli.bstack111l1l1111_opy_ import bstack1ll11l1lll_opy_
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from browserstack_sdk.bstack1111ll111l_opy_ import bstack11l1ll11_opy_
from browserstack_sdk.bstack111111111_opy_ import *
import time
import requests
from bstack_utils.constants import EVENTS, STAGE, bstack1ll1lll1ll_opy_
from bstack_utils.messages import bstack1l1l1lll1_opy_, bstack1ll111ll_opy_, bstack11llll11ll_opy_, bstack1ll111ll1_opy_, bstack11l1l111ll_opy_, bstack1111l1l1l1_opy_
from bstack_utils.measure import measure
from bstack_utils.logger_utils import get_logger
from bstack_utils.helper import bstack111lllllll_opy_
from browserstack_sdk.bstack11ll1ll1_opy_ import bstack11l11lllll_opy_
logger = get_logger(__name__)
def bstack11lll1111_opy_():
  global CONFIG
  headers = {
        bstack1ll111_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack1ll111_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack111lllllll_opy_(CONFIG, bstack1ll1lll1ll_opy_)
  try:
    response = requests.get(bstack1ll1lll1ll_opy_, headers=headers, proxies=proxies, timeout=2)
    if response.json():
      bstack11ll1ll111_opy_ = response.json()[bstack1ll111_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1l1l1lll1_opy_.format(response.json()))
      return bstack11ll1ll111_opy_
    else:
      logger.debug(bstack1ll111ll_opy_.format(bstack1ll111_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack1ll111ll_opy_.format(e))
def bstack111ll1l111_opy_(hub_url):
  global CONFIG
  url = bstack1ll111_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack1ll111_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack1ll111_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack1ll111_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack111lllllll_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=(0.5, 1.0))
    latency = time.perf_counter() - start_time
    logger.debug(bstack11llll11ll_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1ll111ll1_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack1l1lllll1l_opy_, stage=STAGE.bstack11ll1111_opy_)
def bstack111l111l1l_opy_():
  try:
    global bstack1l1l11lll_opy_
    global CONFIG
    if bstack1ll111_opy_ (u"ࠫ࡭ࡻࡢࡓࡧࡪ࡭ࡴࡴࠧࡾ") in CONFIG and CONFIG[bstack1ll111_opy_ (u"ࠬ࡮ࡵࡣࡔࡨ࡫࡮ࡵ࡮ࠨࡿ")]:
      from bstack_utils.constants import bstack1llll1l1l_opy_
      bstack1lllll1ll_opy_ = CONFIG[bstack1ll111_opy_ (u"࠭ࡨࡶࡤࡕࡩ࡬࡯࡯࡯ࠩࢀ")]
      if bstack1lllll1ll_opy_ in bstack1llll1l1l_opy_:
        bstack1l1l11lll_opy_ = bstack1llll1l1l_opy_[bstack1lllll1ll_opy_]
        logger.debug(bstack11l1l111ll_opy_.format(bstack1l1l11lll_opy_))
        return
      else:
        logger.debug(bstack1ll111_opy_ (u"ࠢࡉࡷࡥࠤࡰ࡫ࡹࠡࠩࡾࢁࠬࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࡎࡕࡃࡡࡘࡖࡑࡥࡍࡂࡒ࠯ࠤ࡫ࡧ࡬࡭࡫ࡱ࡫ࠥࡨࡡࡤ࡭ࠣࡸࡴࠦ࡯ࡱࡶ࡬ࡱࡦࡲࠠࡩࡷࡥࠤࡩ࡫ࡴࡦࡥࡷ࡭ࡴࡴࠢࢁ").format(bstack1lllll1ll_opy_))
    bstack11ll1ll111_opy_ = bstack11lll1111_opy_()
    from concurrent.futures import ThreadPoolExecutor, as_completed
    if bstack11ll1ll111_opy_:
        with ThreadPoolExecutor(max_workers=len(bstack11ll1ll111_opy_)) as executor:
            bstack1l11l11ll1_opy_ = {executor.submit(bstack111ll1l111_opy_, bstack1lllll11_opy_): bstack1lllll11_opy_ for bstack1lllll11_opy_ in bstack11ll1ll111_opy_}
            for future in as_completed(bstack1l11l11ll1_opy_):
                result = future.result()
                if result and result.get(bstack1ll111_opy_ (u"ࠨ࡮ࡤࡸࡪࡴࡣࡺࠩࢂ")) is not None:
                    bstack1l1l11lll_opy_ = result[bstack1ll111_opy_ (u"ࠩ࡫ࡹࡧࡥࡵࡳ࡮ࠪࢃ")]
                    logger.debug(bstack11l1l111ll_opy_.format(bstack1l1l11lll_opy_))
                    return
        bstack1l1l11lll_opy_ = bstack11ll1ll111_opy_[0]
        logger.debug(bstack11l1l111ll_opy_.format(bstack1l1l11lll_opy_))
        return
  except Exception as e:
    logger.debug(bstack1111l1l1l1_opy_.format(e))
from browserstack_sdk.bstack1l1ll11ll_opy_ import *
from browserstack_sdk.bstack11ll1ll1_opy_ import *
from browserstack_sdk.bstack1ll11l11_opy_ import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.logger_utils import get_logger
from bstack_utils.measure import measure
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack1lll1111l1_opy_, stage=STAGE.bstack11ll1111_opy_)
def bstack11l111l1l_opy_():
    global bstack1l1l11lll_opy_
    try:
        bstack1llll1lll_opy_ = bstack1l111ll1l1_opy_()
        bstack111ll11ll1_opy_(bstack1llll1lll_opy_)
        hub_url = bstack1llll1lll_opy_.get(bstack1ll111_opy_ (u"ࠥࡹࡷࡲࠢࢄ"), bstack1ll111_opy_ (u"ࠦࠧࢅ"))
        if hub_url.endswith(bstack1ll111_opy_ (u"ࠬ࠵ࡷࡥ࠱࡫ࡹࡧ࠭ࢆ")):
            hub_url = hub_url.rsplit(bstack1ll111_opy_ (u"࠭࠯ࡸࡦ࠲࡬ࡺࡨࠧࢇ"), 1)[0]
        if hub_url.startswith(bstack1ll111_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࠨ࢈")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack1ll111_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࠪࢉ")):
            hub_url = hub_url[8:]
        bstack1l1l11lll_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack1l111ll1l1_opy_():
    global CONFIG
    bstack1lllll1111_opy_ = CONFIG.get(bstack1ll111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢊ"), {}).get(bstack1ll111_opy_ (u"ࠪ࡫ࡷ࡯ࡤࡏࡣࡰࡩࠬࢋ"), bstack1ll111_opy_ (u"ࠫࡓࡕ࡟ࡈࡔࡌࡈࡤࡔࡁࡎࡇࡢࡔࡆ࡙ࡓࡆࡆࠪࢌ"))
    if not isinstance(bstack1lllll1111_opy_, str):
        raise ValueError(bstack1ll111_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡌࡸࡩࡥࠢࡱࡥࡲ࡫ࠠ࡮ࡷࡶࡸࠥࡨࡥࠡࡣࠣࡺࡦࡲࡩࡥࠢࡶࡸࡷ࡯࡮ࡨࠤࢍ"))
    try:
        bstack1llll1lll_opy_ = bstack1ll11l11ll_opy_(bstack1lllll1111_opy_)
        return bstack1llll1lll_opy_
    except Exception as e:
        logger.error(bstack1ll111_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡩࡵ࡭ࡩࠦࡤࡦࡶࡤ࡭ࡱࡹࠠ࠻ࠢࡾࢁࠧࢎ").format(str(e)))
        return {}
def bstack1ll11l11ll_opy_(bstack1lllll1111_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack1ll111_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ࢏")] or not CONFIG[bstack1ll111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ࢐")]:
            raise ValueError(bstack1ll111_opy_ (u"ࠤࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠤࡴࡸࠠࡢࡥࡦࡩࡸࡹࠠ࡬ࡧࡼࠦ࢑"))
        url = bstack1l11ll1l1_opy_ + bstack1lllll1111_opy_
        auth = (CONFIG[bstack1ll111_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ࢒")], CONFIG[bstack1ll111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ࢓")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack11l1l11l_opy_ = json.loads(response.text)
            return bstack11l1l11l_opy_
    except ValueError as ve:
        logger.error(bstack1ll111_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡩࡵ࡭ࡩࠦࡤࡦࡶࡤ࡭ࡱࡹࠠ࠻ࠢࡾࢁࠧ࢔").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack1ll111_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡪࡶ࡮ࡪࠠࡥࡧࡷࡥ࡮ࡲࡳࠡ࠼ࠣࡿࢂࠨ࢕").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack111ll11ll1_opy_(bstack1ll1lll1l_opy_):
    global CONFIG
    if bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ࢖") not in CONFIG or str(CONFIG[bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬࢗ")]).lower() == bstack1ll111_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ࢘"):
        CONFIG[bstack1ll111_opy_ (u"ࠪࡰࡴࡩࡡ࡭࢙ࠩ")] = False
    elif bstack1ll111_opy_ (u"ࠫ࡮ࡹࡔࡳ࡫ࡤࡰࡌࡸࡩࡥ࢚ࠩ") in bstack1ll1lll1l_opy_:
        bstack11l11l11l_opy_ = CONFIG.get(bstack1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴ࢛ࠩ"), {})
        logger.debug(bstack1ll111_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡸࡪࡵࡷ࡭ࡳ࡭ࠠ࡭ࡱࡦࡥࡱࠦ࡯ࡱࡶ࡬ࡳࡳࡹ࠺ࠡࠧࡶࠦ࢜"), bstack11l11l11l_opy_)
        bstack111lll1l11_opy_ = bstack1ll1lll1l_opy_.get(bstack1ll111_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡒࡦࡲࡨࡥࡹ࡫ࡲࡴࠤ࢝"), [])
        bstack111ll1111_opy_ = bstack1ll111_opy_ (u"ࠣ࠮ࠥ࢞").join(bstack111lll1l11_opy_)
        logger.debug(bstack1ll111_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡅࡸࡷࡹࡵ࡭ࠡࡴࡨࡴࡪࡧࡴࡦࡴࠣࡷࡹࡸࡩ࡯ࡩ࠽ࠤࠪࡹࠢ࢟"), bstack111ll1111_opy_)
        bstack1lll111l1l_opy_ = {
            bstack1ll111_opy_ (u"ࠥࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧࢠ"): bstack1ll111_opy_ (u"ࠦࡦࡺࡳ࠮ࡴࡨࡴࡪࡧࡴࡦࡴࠥࢡ"),
            bstack1ll111_opy_ (u"ࠧ࡬࡯ࡳࡥࡨࡐࡴࡩࡡ࡭ࠤࢢ"): bstack1ll111_opy_ (u"ࠨࡴࡳࡷࡨࠦࢣ"),
            bstack1ll111_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࠭ࡳࡧࡳࡩࡦࡺࡥࡳࠤࢤ"): bstack111ll1111_opy_
        }
        bstack11l11l11l_opy_.update(bstack1lll111l1l_opy_)
        logger.debug(bstack1ll111_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡖࡲࡧࡥࡹ࡫ࡤࠡ࡮ࡲࡧࡦࡲࠠࡰࡲࡷ࡭ࡴࡴࡳ࠻ࠢࠨࡷࠧࢥ"), bstack11l11l11l_opy_)
        CONFIG[bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢦ")] = bstack11l11l11l_opy_
        logger.debug(bstack1ll111_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡉ࡭ࡳࡧ࡬ࠡࡅࡒࡒࡋࡏࡇ࠻ࠢࠨࡷࠧࢧ"), CONFIG)
def get_turboscale_playwright_url():
    bstack1llll1lll_opy_ = bstack1l111ll1l1_opy_()
    if not bstack1llll1lll_opy_[bstack1ll111_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡖࡴ࡯ࠫࢨ")]:
      raise ValueError(bstack1ll111_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡗࡵࡰࠥ࡯ࡳࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡩࡶࡴࡳࠠࡨࡴ࡬ࡨࠥࡪࡥࡵࡣ࡬ࡰࡸ࠴ࠢࢩ"))
    return bstack1llll1lll_opy_[bstack1ll111_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡘࡶࡱ࠭ࢪ")] + bstack1ll111_opy_ (u"ࠧࡀࡥࡤࡴࡸࡃࠧࢫ")
@measure(event_name=EVENTS.bstack1l111l1l_opy_, stage=STAGE.bstack11ll1111_opy_)
def bstack1l1ll1lll1_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack1ll111_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪࢬ")], CONFIG[bstack1ll111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬࢭ")])
        url = bstack11l1111111_opy_
        logger.debug(bstack1ll111_opy_ (u"ࠥࡅࡹࡺࡥ࡮ࡲࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴࠢࡩࡶࡴࡳࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡔࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠣࡅࡕࡏࠢࢮ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack1ll111_opy_ (u"ࠦࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠥࢯ"): bstack1ll111_opy_ (u"ࠧࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠣࢰ")})
            if response.status_code == 200:
                bstack111lll111l_opy_ = json.loads(response.text)
                bstack1ll1l11l1_opy_ = bstack111lll111l_opy_.get(bstack1ll111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡸ࠭ࢱ"), [])
                if bstack1ll1l11l1_opy_:
                    bstack1l11ll1ll1_opy_ = bstack1ll1l11l1_opy_[0]
                    build_hashed_id = bstack1l11ll1ll1_opy_.get(bstack1ll111_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪࢲ"))
                    bstack1l1l11ll11_opy_ = bstack1lll11l11l_opy_ + build_hashed_id
                    result.extend([build_hashed_id, bstack1l1l11ll11_opy_])
                    logger.info(bstack111llll111_opy_.format(bstack1l1l11ll11_opy_))
                    bstack1lll111lll_opy_ = CONFIG[bstack1ll111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫࢳ")]
                    if bstack1ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࢴ") in CONFIG:
                      bstack1lll111lll_opy_ += bstack1ll111_opy_ (u"ࠪࠤࠬࢵ") + CONFIG[bstack1ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࢶ")]
                    if bstack1lll111lll_opy_ != bstack1l11ll1ll1_opy_.get(bstack1ll111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪࢷ")):
                      logger.debug(bstack1l1l1l111l_opy_.format(bstack1l11ll1ll1_opy_.get(bstack1ll111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫࢸ")), bstack1lll111lll_opy_))
                    return result
                else:
                    logger.debug(bstack1ll111_opy_ (u"ࠢࡂࡖࡖࠤ࠿ࠦࡎࡰࠢࡥࡹ࡮ࡲࡤࡴࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠱ࠦࢹ"))
            else:
                logger.debug(bstack1ll111_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴ࠰ࠥࢺ"))
        except Exception as e:
            logger.error(bstack1ll111_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࡶࠤ࠿ࠦࡻࡾࠤࢻ").format(str(e)))
    else:
        logger.debug(bstack1ll111_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡆࡓࡓࡌࡉࡈࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡶࡩࡹ࠴ࠠࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴ࠰ࠥࢼ"))
    return [None, None]
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1lll11111_opy_ import bstack1lll11111_opy_, Events, bstack1lll11ll11_opy_, bstack1lll1111_opy_
from bstack_utils.measure import bstack11lll11l1l_opy_
from bstack_utils.measure import measure
from bstack_utils.percy import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1l1l1llll_opy_ import bstack1ll1llll11_opy_
from bstack_utils.messages import *
from bstack_utils import logger_utils
from bstack_utils.constants import *
from bstack_utils.helper import bstack1111ll11l_opy_, bstack11111l1l_opy_, bstack1l1ll11lll_opy_, bstack11llll11l_opy_, \
  bstack1l111l111_opy_, \
  Notset, is_robot_playwright_installed, bstack1111lllll_opy_, \
  bstack11l1l11ll_opy_, bstack1111ll1l1_opy_, bstack1lll11ll1_opy_, bstack1ll1lll111_opy_, bstack11l11l1111_opy_, bstack11ll1ll11l_opy_, \
  bstack1l1l111l11_opy_, \
  bstack11l11ll11l_opy_, bstack1l1lll11ll_opy_, bstack1l111ll11_opy_, bstack11l1llll1_opy_, \
  bstack1111l11l1l_opy_, bstack11111lll_opy_, bstack1l11lll111_opy_, bstack1l1ll1ll_opy_, bstack1l111l11l_opy_
from bstack_utils.bstack11l11ll11_opy_ import bstack1lll1l11_opy_
from bstack_utils.bstack1l1l1l1l1_opy_ import bstack1lll1l1l11_opy_, bstack1lll11ll_opy_
from bstack_utils.bstack11ll1lll1_opy_ import bstack1lll1l1ll_opy_
from bstack_utils.session_utils import bstack111lll11_opy_, bstack1llll1l1_opy_
from bstack_utils.bstack1l1l1l1lll_opy_ import bstack1l1l1l1lll_opy_
from bstack_utils.bstack11l11l1l11_opy_ import bstack111l1l11l1_opy_
from bstack_utils.proxy import bstack1l1l11l1l_opy_, bstack111lllllll_opy_, bstack11lll11l_opy_, bstack1lll1ll1l_opy_
from bstack_utils.bstack11l1lll1l1_opy_ import bstack1l1111l1l1_opy_, bstack1ll111l11_opy_
import bstack_utils.bstack1ll1l1l1ll_opy_ as TestHubUtils
import bstack_utils.bstack1llllllll1_opy_ as bstack1llll11lll_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.utils.bstack1l1ll1111l_opy_ import bstack111ll11l1_opy_
from bstack_utils.bstack111ll11l_opy_ import bstack1l1ll111l_opy_
from bstack_utils.bstack1l111111_opy_ import bstack111l11l1ll_opy_
from bstack_utils.bstack11lll11l1l_opy_ import bstack111ll11111_opy_
if os.getenv(bstack1ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡉࡑࡒࡏࡘ࠭ࢽ")):
  cli.bstack1ll1l1ll1l_opy_()
else:
  os.environ[bstack1ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡊࡒࡓࡐ࡙ࠧࢾ")] = bstack1ll111_opy_ (u"࠭ࡴࡳࡷࡨࠫࢿ")
bstack1ll11ll1l_opy_ = bstack1ll111_opy_ (u"ࠧࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠠࠡ࡫ࡩࠬࡵࡧࡧࡦࠢࡀࡁࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠠࡼ࡞ࡱࠤࠥࠦࡴࡳࡻࡾࡠࡳࠦࡣࡰࡰࡶࡸࠥ࡬ࡳࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࡡ࠭ࡦࡴ࡞ࠪ࠭ࡀࡢ࡮ࠡࠢࠣࠤࠥ࡬ࡳ࠯ࡣࡳࡴࡪࡴࡤࡇ࡫࡯ࡩࡘࡿ࡮ࡤࠪࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠬࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡳࡣ࡮ࡴࡤࡦࡺࠬࠤ࠰ࠦࠢ࠻ࠤࠣ࠯ࠥࡐࡓࡐࡐ࠱ࡷࡹࡸࡩ࡯ࡩ࡬ࡪࡾ࠮ࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࠬࡦࡽࡡࡪࡶࠣࡲࡪࡽࡐࡢࡩࡨ࠶࠳࡫ࡶࡢ࡮ࡸࡥࡹ࡫ࠨࠣࠪࠬࠤࡂࡄࠠࡼࡿࠥ࠰ࠥࡢࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡨࡧࡷࡗࡪࡹࡳࡪࡱࡱࡈࡪࡺࡡࡪ࡮ࡶࠦࢂࡢࠧࠪࠫࠬ࡟ࠧ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠣ࡟ࠬࠤ࠰ࠦࠢ࠭࡞࡟ࡲࠧ࠯࡜࡯ࠢࠣࠤࠥࢃࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡽ࡝ࡰࠣࠤ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠧࣀ")
LAUNCH_PATCH_ROBOT_PLAYWRIGHT = bstack1ll111_opy_ (u"ࠨ࡞ࡱ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࡢ࡮ࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡰࡢࡶ࡫ࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳࡞࡞ࡱࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠴ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡶ࡟ࡪࡰࡧࡩࡽࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠴ࡠࡠࡳࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡹ࡬ࡪࡥࡨࠬ࠵࠲ࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࠬࡠࡳࡩ࡯࡯ࡵࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬ࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ࠭ࡀࡢ࡮ࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮࡭ࡣࡸࡲࡨ࡮ࠠ࠾ࠢࡤࡷࡾࡴࡣࠡࠪ࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴࠫࠣࡁࡃࠦࡻ࡝ࡰ࡯ࡩࡹࠦࡣࡢࡲࡶ࠿ࡡࡴࡴࡳࡻࠣࡿࡡࡴࡣࡢࡲࡶࠤࡂࠦࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠪ࡞ࡱࠤࠥࢃࠠࡤࡣࡷࡧ࡭࠮ࡥࡹࠫࠣࡿࡡࡴࠠࠡࠢࠣࢁࡡࡴࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡣࡺࡥ࡮ࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮ࡤࡱࡱࡲࡪࡩࡴࠩࡽ࡟ࡲࠥࠦࠠࠡࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸ࠿ࠦࡠࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠦࡾࡩࡳࡩ࡯ࡥࡧࡘࡖࡎࡉ࡯࡮ࡲࡲࡲࡪࡴࡴࠩࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡦࡥࡵࡹࠩࠪࡿࡣ࠰ࡡࡴࠠࠡࠢࠣ࠲࠳࠴࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸࡢ࡮ࠡࠢࢀ࠭ࡡࡴࡽ࡝ࡰࡦࡳࡳࡹࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡧࡴࡴ࡮ࡦࡥࡷࠤࡂࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺ࠮ࡣ࡫ࡱࡨ࠭࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠮ࡁ࡜࡯࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭࠯ࡥࡲࡲࡳ࡫ࡣࡵࠢࡀࠤࡦࡹࡹ࡯ࡥࠣࠬࡨࡵ࡮࡯ࡧࡦࡸࡔࡶࡴࡪࡱࡱࡷ࠮ࠦ࠽࠿ࠢࡾࡠࡳࠦࠠ࡭ࡧࡷࠤࡨࡧࡰࡴ࠽࡟ࡲࠥࠦࡴࡳࡻࠣࡿࡡࡴࠠࠡࠢࠣࡧࡦࡶࡳࠡ࠿ࠣࡎࡘࡕࡎ࠯ࡲࡤࡶࡸ࡫ࠨࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷ࠮ࡢ࡮ࠡࠢࢀࠤࡨࡧࡴࡤࡪࠫࡩࡽ࠯ࠠࡼ࡞ࡱࠤࠥࢃ࡜࡯ࠢࠣࡧࡴࡴࡳࡵࠢࡰࡳࡩ࡯ࡦࡪࡧࡧࡉࡳࡪࡰࡰ࡫ࡱࡸࠥࡃࠠࡡࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࡣࠤ࠰ࠦࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭ࡀࡢ࡮ࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤ࠳࠴࠮ࡤࡱࡱࡲࡪࡩࡴࡐࡲࡷ࡭ࡴࡴࡳ࠭࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࡝ࡰࠣࠤࢂ࠯࡜࡯ࡿ࡟ࡲ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵࡜࡯ࠩࣁ")
from ._version import __version__
bstack1ll1llll1l_opy_ = None
CONFIG = {}
bstack1111l1l1_opy_ = {}
bstack11111ll1l_opy_ = {}
bstack1l11111l_opy_ = None
bstack1lll1lll1l_opy_ = None
SESSION_NAME = None
PLATFORM_INDEX = -1
bstack1ll1l111l_opy_ = 0
bstack1ll11ll11_opy_ = bstack1l1lllll1_opy_
bstack111ll1l1l1_opy_ = 1
PARALLELISE_VANILLA_PYTHON = False
PARALLELISE_THREADING_PYTHON = False
FRAMEWORK_NAME = bstack1ll111_opy_ (u"ࠩࠪࣂ")
bstack11l111ll1l_opy_ = bstack1ll111_opy_ (u"ࠪࠫࣃ")
bstack11l1l1l1_opy_ = False
BROWSERSTACK_AUTOMATION = True
bstack1ll1111l1l_opy_ = False
bstack11lll1l111_opy_ = bstack1ll111_opy_ (u"ࠫࠬࣄ")
bstack1l111lll11_opy_ = []
bstack11llll1ll_opy_ = threading.Lock()
bstack1111lll11l_opy_ = threading.Lock()
bstack11lll11l1_opy_ = None
bstack1l1l11lll_opy_ = bstack1ll111_opy_ (u"ࠬ࠭ࣅ")
SELENIUM_OR_PLAYWRIGHT_INSTALLED = False
bstack1l1ll111_opy_ = None
bstack11lll1l11_opy_ = None
bstack1llllll1l_opy_ = None
bstack1l1lll11l1_opy_ = -1
bstack1l111l111l_opy_ = os.path.join(os.path.expanduser(bstack1ll111_opy_ (u"࠭ࡾࠨࣆ")), bstack1ll111_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧࣇ"), bstack1ll111_opy_ (u"ࠨ࠰ࡵࡳࡧࡵࡴ࠮ࡴࡨࡴࡴࡸࡴ࠮ࡪࡨࡰࡵ࡫ࡲ࠯࡬ࡶࡳࡳ࠭ࣈ"))
bstack111llll1l1_opy_ = 0
bstack11llllll_opy_ = 0
bstack111ll11l1l_opy_ = []
bstack1llll11ll_opy_ = []
ROBOT_PYTHON_ERRORS = []
bstack11l11l111l_opy_ = []
bstack11l1l11l1l_opy_ = bstack1ll111_opy_ (u"ࠩࠪࣉ")
bstack1l11111l11_opy_ = bstack1ll111_opy_ (u"ࠪࠫ࣊")
bstack11111l111_opy_ = False
bstack111l1l11l_opy_ = False
bstack1111111ll_opy_ = {}
bstack1l1l111l1l_opy_ = {}
bstack1111lllll1_opy_ = None
bstack1l11ll11l_opy_ = None
bstack1111lll11_opy_ = None
bstack1l111llll_opy_ = None
bstack1l1l1l1ll_opy_ = None
bstack1111111l1_opy_ = None
bstack1llll111l1_opy_ = None
bstack11l1ll1l11_opy_ = None
bstack1lll1lll1_opy_ = None
bstack1l111l11l1_opy_ = None
bstack1ll1ll11l1_opy_ = None
bstack1ll1ll11l_opy_ = None
bstack1l1l1lllll_opy_ = None
bstack11l1ll11l_opy_ = None
bstack1lllll11l_opy_ = None
bstack1l11l11l1_opy_ = None
bstack1l1llll1ll_opy_ = None
bstack11l111l11_opy_ = None
bstack1l1ll1ll1_opy_ = None
bstack1lll11lll1_opy_ = None
bstack1l11l111_opy_ = None
bstack1111111l_opy_ = None
bstack1llll11l_opy_ = None
thread_local = threading.local()
bstack1ll1ll1l_opy_ = False
bstack1l111ll1l_opy_ = bstack1ll111_opy_ (u"ࠦࠧ࣋")
_11l1l1lll1_opy_ = None
logger = logger_utils.get_logger(__name__, bstack1ll11ll11_opy_)
bstack1l11llll_opy_ = logger_utils.bstack1111l1ll1_opy_(__name__)
global_config = Config.get_instance()
percy = bstack1ll11111l_opy_()
bstack1lll111ll1_opy_ = bstack1ll1llll11_opy_()
bstack1lll11ll1l_opy_ = bstack1ll11l11_opy_()
def bstack11l1ll1l1l_opy_():
  global CONFIG
  global bstack11111l111_opy_
  global global_config
  testContextOptions = bstack1llll1111_opy_(CONFIG)
  if bstack1l111l111_opy_(CONFIG):
    if (bstack1ll111_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ࣌") in testContextOptions and str(testContextOptions[bstack1ll111_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ࣍")]).lower() == bstack1ll111_opy_ (u"ࠧࡵࡴࡸࡩࠬ࣎")):
      bstack11111l111_opy_ = True
      global_config.bstack1llll1l1l1_opy_(True)
    if (bstack1ll111_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷ࣏ࠬ") in testContextOptions and str(testContextOptions[bstack1ll111_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࣐࠭")]).lower() == bstack1ll111_opy_ (u"ࠪࡸࡷࡻࡥࠨ࣑")):
      global_config.bstack11l1111l1l_opy_(True)
  else:
    bstack11111l111_opy_ = True
    global_config.bstack1llll1l1l1_opy_(True)
    global_config.bstack11l1111l1l_opy_(True)
def bstack1l1111ll1_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack11l1l1l11_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1lll1l11l_opy_():
  global bstack1l1l111l1l_opy_
  args = sys.argv
  for i in range(len(args)):
    if bstack1ll111_opy_ (u"ࠦ࠲࠳ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡨࡵ࡮ࡧ࡫ࡪࡪ࡮ࡲࡥ࣒ࠣ") == args[i].lower() or bstack1ll111_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰࡰࡩ࡭࡬ࠨ࣓") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      bstack1l1l111l1l_opy_[bstack1ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࡤࡌࡉࡍࡇࠪࣔ")] = path
      return path
  return None
bstack11lllll111_opy_ = re.compile(bstack1ll111_opy_ (u"ࡲࠣ࠰࠭ࡃࡡࠪࡻࠩ࠰࠭ࡃ࠮ࢃ࠮ࠫࡁࠥࣕ"))
def bstack1ll11111_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack11lllll111_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack1ll111_opy_ (u"ࠣࠦࡾࠦࣖ") + group + bstack1ll111_opy_ (u"ࠤࢀࠦࣗ"), os.environ.get(group))
  return value
def bstack11ll11llll_opy_():
  global bstack1llll11l_opy_
  if bstack1llll11l_opy_ is None:
        bstack1llll11l_opy_ = bstack1lll1l11l_opy_()
  bstack111111l1l_opy_ = bstack1llll11l_opy_
  if bstack111111l1l_opy_ and os.path.exists(os.path.abspath(bstack111111l1l_opy_)):
    fileName = bstack111111l1l_opy_
  if bstack1ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋࠧࣘ") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack1ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨࣙ")])) and not bstack1ll111_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡑࡥࡲ࡫ࠧࣚ") in locals():
    fileName = os.environ[bstack1ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࡤࡌࡉࡍࡇࠪࣛ")]
  if bstack1ll111_opy_ (u"ࠧࡧ࡫࡯ࡩࡓࡧ࡭ࡦࠩࣜ") in locals():
    bstack11l111_opy_ = os.path.abspath(fileName)
  else:
    bstack11l111_opy_ = bstack1ll111_opy_ (u"ࠨࠩࣝ")
  bstack11l1lll111_opy_ = os.getcwd()
  bstack1ll111111l_opy_ = bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬࣞ")
  bstack1l11lllll1_opy_ = bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡥࡲࡲࠧࣟ")
  while (not os.path.exists(bstack11l111_opy_)) and bstack11l1lll111_opy_ != bstack1ll111_opy_ (u"ࠦࠧ࣠"):
    bstack11l111_opy_ = os.path.join(bstack11l1lll111_opy_, bstack1ll111111l_opy_)
    if not os.path.exists(bstack11l111_opy_):
      bstack11l111_opy_ = os.path.join(bstack11l1lll111_opy_, bstack1l11lllll1_opy_)
    if bstack11l1lll111_opy_ != os.path.dirname(bstack11l1lll111_opy_):
      bstack11l1lll111_opy_ = os.path.dirname(bstack11l1lll111_opy_)
    else:
      bstack11l1lll111_opy_ = bstack1ll111_opy_ (u"ࠧࠨ࣡")
  bstack1llll11l_opy_ = bstack11l111_opy_ if os.path.exists(bstack11l111_opy_) else None
  return bstack1llll11l_opy_
def bstack11l11ll1l1_opy_(config):
    if bstack1ll111_opy_ (u"࠭ࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬࠭࣢") in config:
      config[bstack1ll111_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࣣࠫ")] = config[bstack1ll111_opy_ (u"ࠨࡶࡨࡷࡹࡘࡥࡱࡱࡵࡸ࡮ࡴࡧࠨࣤ")]
    if bstack1ll111_opy_ (u"ࠩࡷࡩࡸࡺࡒࡦࡲࡲࡶࡹ࡯࡮ࡨࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣥ") in config:
      config[bstack1ll111_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࣦࠧ")] = config[bstack1ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࡓࡵࡺࡩࡰࡰࡶࠫࣧ")]
def bstack1ll1l11lll_opy_():
  bstack11l111_opy_ = bstack11ll11llll_opy_()
  if not os.path.exists(bstack11l111_opy_):
    bstack1111l1l1ll_opy_(
      bstack1lllllll1l_opy_.format(os.getcwd()))
  try:
    with open(bstack11l111_opy_, bstack1ll111_opy_ (u"ࠬࡸࠧࣨ")) as stream:
      yaml.add_implicit_resolver(bstack1ll111_opy_ (u"ࠨࠡࡱࡣࡷ࡬ࡪࡾࣩࠢ"), bstack11lllll111_opy_)
      yaml.add_constructor(bstack1ll111_opy_ (u"ࠢࠢࡲࡤࡸ࡭࡫ࡸࠣ࣪"), bstack1ll11111_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      bstack11l11ll1l1_opy_(config)
      return config
  except:
    with open(bstack11l111_opy_, bstack1ll111_opy_ (u"ࠨࡴࠪ࣫")) as stream:
      try:
        config = yaml.safe_load(stream)
        bstack11l11ll1l1_opy_(config)
        return config
      except yaml.YAMLError as exc:
        bstack1111l1l1ll_opy_(bstack1ll11l11l1_opy_.format(str(exc)))
def bstack1111l1l1l_opy_(config):
  bstack111lll1ll_opy_ = bstack1l1ll1l11_opy_(config)
  for option in list(bstack111lll1ll_opy_):
    if option.lower() in bstack1l11lll11l_opy_ and option != bstack1l11lll11l_opy_[option.lower()]:
      bstack111lll1ll_opy_[bstack1l11lll11l_opy_[option.lower()]] = bstack111lll1ll_opy_[option]
      del bstack111lll1ll_opy_[option]
  return config
def bstack11l1l1l1l_opy_():
  global bstack11111ll1l_opy_
  for key, bstack111llll1ll_opy_ in bstack111ll1ll1_opy_.items():
    if isinstance(bstack111llll1ll_opy_, list):
      for var in bstack111llll1ll_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack11111ll1l_opy_[key] = os.environ[var]
          break
    elif bstack111llll1ll_opy_ in os.environ and os.environ[bstack111llll1ll_opy_] and str(os.environ[bstack111llll1ll_opy_]).strip():
      bstack11111ll1l_opy_[key] = os.environ[bstack111llll1ll_opy_]
  if bstack1ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ࣬") in os.environ:
    bstack11111ll1l_opy_[bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹ࣭ࠧ")] = {}
    bstack11111ll1l_opy_[bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ࣮")][bstack1ll111_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣯ࠧ")] = os.environ[bstack1ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨࣰ")]
def bstack11ll1ll11_opy_():
  global bstack1111l1l1_opy_
  global bstack11lll1l111_opy_
  global bstack1l1l111l1l_opy_
  bstack111l11ll1_opy_ = []
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) - 1 and bstack1ll111_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࣱࠪ").lower() == val.lower():
      bstack1111l1l1_opy_[bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࣲࠬ")] = {}
      bstack1111l1l1_opy_[bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࣳ")][bstack1ll111_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣴ")] = sys.argv[idx + 1]
      bstack111l11ll1_opy_.extend([idx, idx + 1])
      break
  for key, bstack1111lll111_opy_ in bstack1l11ll11ll_opy_.items():
    if isinstance(bstack1111lll111_opy_, list):
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        for var in bstack1111lll111_opy_:
          if bstack1ll111_opy_ (u"ࠫ࠲࠳ࠧࣵ") + var.lower() == val.lower() and key not in bstack1111l1l1_opy_:
            bstack1111l1l1_opy_[key] = sys.argv[idx + 1]
            bstack11lll1l111_opy_ += bstack1ll111_opy_ (u"ࠬࠦ࠭࠮ࣶࠩ") + var + bstack1ll111_opy_ (u"࠭ࠠࠨࣷ") + shlex.quote(sys.argv[idx + 1])
            bstack1l111l11l_opy_(bstack1l1l111l1l_opy_, key, sys.argv[idx + 1])
            bstack111l11ll1_opy_.extend([idx, idx + 1])
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        if bstack1ll111_opy_ (u"ࠧ࠮࠯ࠪࣸ") + bstack1111lll111_opy_.lower() == val.lower() and key not in bstack1111l1l1_opy_:
          bstack1111l1l1_opy_[key] = sys.argv[idx + 1]
          bstack11lll1l111_opy_ += bstack1ll111_opy_ (u"ࠨࠢ࠰࠱ࣹࠬ") + bstack1111lll111_opy_ + bstack1ll111_opy_ (u"ࣺࠩࠣࠫ") + shlex.quote(sys.argv[idx + 1])
          bstack1l111l11l_opy_(bstack1l1l111l1l_opy_, key, sys.argv[idx + 1])
          bstack111l11ll1_opy_.extend([idx, idx + 1])
  for idx in sorted(set(bstack111l11ll1_opy_), reverse=True):
    if idx < len(sys.argv):
      del sys.argv[idx]
def bstack11l1l1111_opy_(config):
  bstack1l11ll1lll_opy_ = config.keys()
  for bstack1l1l1l11l_opy_, bstack11l1ll1lll_opy_ in bstack1l11ll111l_opy_.items():
    if bstack11l1ll1lll_opy_ in bstack1l11ll1lll_opy_:
      config[bstack1l1l1l11l_opy_] = config[bstack11l1ll1lll_opy_]
      del config[bstack11l1ll1lll_opy_]
  for bstack1l1l1l11l_opy_, bstack11l1ll1lll_opy_ in bstack1111llll_opy_.items():
    if isinstance(bstack11l1ll1lll_opy_, list):
      for bstack1lll1ll11_opy_ in bstack11l1ll1lll_opy_:
        if bstack1lll1ll11_opy_ in bstack1l11ll1lll_opy_:
          config[bstack1l1l1l11l_opy_] = config[bstack1lll1ll11_opy_]
          del config[bstack1lll1ll11_opy_]
          break
    elif bstack11l1ll1lll_opy_ in bstack1l11ll1lll_opy_:
      config[bstack1l1l1l11l_opy_] = config[bstack11l1ll1lll_opy_]
      del config[bstack11l1ll1lll_opy_]
  for bstack1lll1ll11_opy_ in list(config):
    for bstack1l11lll11_opy_ in bstack11111111_opy_:
      if bstack1lll1ll11_opy_.lower() == bstack1l11lll11_opy_.lower() and bstack1lll1ll11_opy_ != bstack1l11lll11_opy_:
        config[bstack1l11lll11_opy_] = config[bstack1lll1ll11_opy_]
        del config[bstack1lll1ll11_opy_]
  bstack11l11l1l1l_opy_ = [{}]
  if not config.get(bstack1ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣻ")):
    config[bstack1ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣼ")] = [{}]
  bstack11l11l1l1l_opy_ = config[bstack1ll111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨࣽ")]
  for platform in bstack11l11l1l1l_opy_:
    for bstack1lll1ll11_opy_ in list(platform):
      for bstack1l11lll11_opy_ in bstack11111111_opy_:
        if bstack1lll1ll11_opy_.lower() == bstack1l11lll11_opy_.lower() and bstack1lll1ll11_opy_ != bstack1l11lll11_opy_:
          platform[bstack1l11lll11_opy_] = platform[bstack1lll1ll11_opy_]
          del platform[bstack1lll1ll11_opy_]
  for bstack1l1l1l11l_opy_, bstack11l1ll1lll_opy_ in bstack1111llll_opy_.items():
    for platform in bstack11l11l1l1l_opy_:
      if isinstance(bstack11l1ll1lll_opy_, list):
        for bstack1lll1ll11_opy_ in bstack11l1ll1lll_opy_:
          if bstack1lll1ll11_opy_ in platform:
            platform[bstack1l1l1l11l_opy_] = platform[bstack1lll1ll11_opy_]
            del platform[bstack1lll1ll11_opy_]
            break
      elif bstack11l1ll1lll_opy_ in platform:
        platform[bstack1l1l1l11l_opy_] = platform[bstack11l1ll1lll_opy_]
        del platform[bstack11l1ll1lll_opy_]
  for bstack111ll111l1_opy_ in bstack1ll1111ll_opy_:
    if bstack111ll111l1_opy_ in config:
      if not bstack1ll1111ll_opy_[bstack111ll111l1_opy_] in config:
        config[bstack1ll1111ll_opy_[bstack111ll111l1_opy_]] = {}
      config[bstack1ll1111ll_opy_[bstack111ll111l1_opy_]].update(config[bstack111ll111l1_opy_])
      del config[bstack111ll111l1_opy_]
  for platform in bstack11l11l1l1l_opy_:
    for bstack111ll111l1_opy_ in bstack1ll1111ll_opy_:
      if bstack111ll111l1_opy_ in list(platform):
        if not bstack1ll1111ll_opy_[bstack111ll111l1_opy_] in platform:
          platform[bstack1ll1111ll_opy_[bstack111ll111l1_opy_]] = {}
        platform[bstack1ll1111ll_opy_[bstack111ll111l1_opy_]].update(platform[bstack111ll111l1_opy_])
        del platform[bstack111ll111l1_opy_]
  config = bstack1111l1l1l_opy_(config)
  return config
def bstack11lllll11l_opy_(config):
  global bstack11l111ll1l_opy_
  bstack1l11llll1l_opy_ = False
  if bstack1ll111_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪࣾ") in config and str(config[bstack1ll111_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫࣿ")]).lower() != bstack1ll111_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧऀ"):
    if bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ँ") not in config or str(config[bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧं")]).lower() == bstack1ll111_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪः"):
      config[bstack1ll111_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫऄ")] = False
    else:
      bstack1llll1lll_opy_ = bstack1l111ll1l1_opy_()
      if bstack1ll111_opy_ (u"࠭ࡩࡴࡖࡵ࡭ࡦࡲࡇࡳ࡫ࡧࠫअ") in bstack1llll1lll_opy_:
        if not bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫआ") in config:
          config[bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬइ")] = {}
        config[bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ई")][bstack1ll111_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬउ")] = bstack1ll111_opy_ (u"ࠫࡦࡺࡳ࠮ࡴࡨࡴࡪࡧࡴࡦࡴࠪऊ")
        bstack1l11llll1l_opy_ = True
        bstack11l111ll1l_opy_ = config[bstack1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩऋ")].get(bstack1ll111_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨऌ"))
  if bstack1l111l111_opy_(config) and bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫऍ") in config and str(config[bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬऎ")]).lower() != bstack1ll111_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨए") and not bstack1l11llll1l_opy_:
    if not bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧऐ") in config:
      config[bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऑ")] = {}
    if not config[bstack1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩऒ")].get(bstack1ll111_opy_ (u"࠭ࡳ࡬࡫ࡳࡆ࡮ࡴࡡࡳࡻࡌࡲ࡮ࡺࡩࡢ࡮࡬ࡷࡦࡺࡩࡰࡰࠪओ")) and not bstack1ll111_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऔ") in config[bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬक")]:
      current_time = datetime.datetime.now()
      bstack1l1l111ll_opy_ = current_time.strftime(bstack1ll111_opy_ (u"ࠩࠨࡨࡤࠫࡢࡠࠧࡋࠩࡒ࠭ख"))
      hostname = socket.gethostname()
      bstack1l1l1l11l1_opy_ = bstack1ll111_opy_ (u"ࠪࠫग").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1ll111_opy_ (u"ࠫࢀࢃ࡟ࡼࡿࡢࡿࢂ࠭घ").format(bstack1l1l111ll_opy_, hostname, bstack1l1l1l11l1_opy_)
      config[bstack1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩङ")][bstack1ll111_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨच")] = identifier
    bstack11l111ll1l_opy_ = config[bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫछ")].get(bstack1ll111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪज"))
  return config
def bstack1l11111lll_opy_():
  bstack1l111llll1_opy_ =  bstack1ll1lll111_opy_()[bstack1ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠨझ")]
  return bstack1l111llll1_opy_ if bstack1l111llll1_opy_ else -1
def bstack1llllll1ll_opy_(bstack1l111llll1_opy_):
  global CONFIG
  if not bstack1ll111_opy_ (u"ࠪࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬञ") in CONFIG[bstack1ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ट")]:
    return
  CONFIG[bstack1ll111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧठ")] = CONFIG[bstack1ll111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨड")].replace(
    bstack1ll111_opy_ (u"ࠧࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩढ"),
    str(bstack1l111llll1_opy_)
  )
def bstack11lllllll_opy_():
  global CONFIG
  if not bstack1ll111_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧण") in CONFIG[bstack1ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫत")]:
    return
  current_time = datetime.datetime.now()
  bstack1l1l111ll_opy_ = current_time.strftime(bstack1ll111_opy_ (u"ࠪࠩࡩ࠳ࠥࡣ࠯ࠨࡌ࠿ࠫࡍࠨथ"))
  CONFIG[bstack1ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭द")] = CONFIG[bstack1ll111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧध")].replace(
    bstack1ll111_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬन"),
    bstack1l1l111ll_opy_
  )
def bstack11ll111l1l_opy_():
  global CONFIG
  if bstack1ll111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऩ") in CONFIG and not bool(CONFIG[bstack1ll111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪप")]):
    del CONFIG[bstack1ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫफ")]
    return
  if not bstack1ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬब") in CONFIG:
    CONFIG[bstack1ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭भ")] = bstack1ll111_opy_ (u"ࠬࠩࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨम")
  if bstack1ll111_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬय") in CONFIG[bstack1ll111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩर")]:
    bstack11lllllll_opy_()
    os.environ[bstack1ll111_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬऱ")] = CONFIG[bstack1ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫल")]
  if not bstack1ll111_opy_ (u"ࠪࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬळ") in CONFIG[bstack1ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ऴ")]:
    return
  bstack1l111llll1_opy_ = bstack1ll111_opy_ (u"ࠬ࠭व")
  bstack11l1111l1_opy_ = bstack1l11111lll_opy_()
  if bstack11l1111l1_opy_ != -1:
    bstack1l111llll1_opy_ = bstack1ll111_opy_ (u"࠭ࡃࡊࠢࠪश") + str(bstack11l1111l1_opy_)
  if bstack1l111llll1_opy_ == bstack1ll111_opy_ (u"ࠧࠨष"):
    bstack1l1ll11111_opy_ = bstack11l1l11l11_opy_(CONFIG[bstack1ll111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫस")])
    if bstack1l1ll11111_opy_ != -1:
      bstack1l111llll1_opy_ = str(bstack1l1ll11111_opy_)
  if bstack1l111llll1_opy_:
    bstack1llllll1ll_opy_(bstack1l111llll1_opy_)
    os.environ[bstack1ll111_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ह")] = CONFIG[bstack1ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬऺ")]
def bstack1ll11l1l1l_opy_(bstack1l1111ll_opy_, bstack11ll111l1_opy_, path):
  json_data = {
    bstack1ll111_opy_ (u"ࠫ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨऻ"): bstack11ll111l1_opy_
  }
  if os.path.exists(path):
    bstack1lll11l1l_opy_ = json.load(open(path, bstack1ll111_opy_ (u"ࠬࡸࡢࠨ़")))
  else:
    bstack1lll11l1l_opy_ = {}
  bstack1lll11l1l_opy_[bstack1l1111ll_opy_] = json_data
  with open(path, bstack1ll111_opy_ (u"ࠨࡷࠬࠤऽ")) as outfile:
    json.dump(bstack1lll11l1l_opy_, outfile)
def bstack11l1l11l11_opy_(bstack1l1111ll_opy_):
  bstack1l1111ll_opy_ = str(bstack1l1111ll_opy_)
  bstack111l1ll11_opy_ = os.path.join(os.path.expanduser(bstack1ll111_opy_ (u"ࠧࡿࠩा")), bstack1ll111_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨि"))
  try:
    if not os.path.exists(bstack111l1ll11_opy_):
      os.makedirs(bstack111l1ll11_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1ll111_opy_ (u"ࠩࢁࠫी")), bstack1ll111_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪु"), bstack1ll111_opy_ (u"ࠫ࠳ࡨࡵࡪ࡮ࡧ࠱ࡳࡧ࡭ࡦ࠯ࡦࡥࡨ࡮ࡥ࠯࡬ࡶࡳࡳ࠭ू"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1ll111_opy_ (u"ࠬࡽࠧृ")):
        pass
      with open(file_path, bstack1ll111_opy_ (u"ࠨࡷࠬࠤॄ")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1ll111_opy_ (u"ࠧࡳࠩॅ")) as bstack111l1l1l1l_opy_:
      bstack1ll111l11l_opy_ = json.load(bstack111l1l1l1l_opy_)
    if bstack1l1111ll_opy_ in bstack1ll111l11l_opy_:
      bstack11lll11l11_opy_ = bstack1ll111l11l_opy_[bstack1l1111ll_opy_][bstack1ll111_opy_ (u"ࠨ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬॆ")]
      bstack1111l11l_opy_ = int(bstack11lll11l11_opy_) + 1
      bstack1ll11l1l1l_opy_(bstack1l1111ll_opy_, bstack1111l11l_opy_, file_path)
      return bstack1111l11l_opy_
    else:
      bstack1ll11l1l1l_opy_(bstack1l1111ll_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warning(bstack111l11l1l1_opy_.format(str(e)))
    return -1
def bstack1ll111l1l1_opy_(config):
  if not config[bstack1ll111_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫे")] or not config[bstack1ll111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ै")]:
    return True
  else:
    return False
def bstack1l1l1ll1l1_opy_(config, index=0):
  global bstack11l1l1l1_opy_
  bstack1ll111ll11_opy_ = {}
  caps = bstack1ll111lll_opy_ + bstack111l111lll_opy_
  if config.get(bstack1ll111_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨॉ"), False):
    bstack1ll111ll11_opy_[bstack1ll111_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩॊ")] = True
    bstack1ll111ll11_opy_[bstack1ll111_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪो")] = config.get(bstack1ll111_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࡓࡵࡺࡩࡰࡰࡶࠫौ"), {})
  if bstack11l1l1l1_opy_:
    caps += bstack1lll1l1l1_opy_
  for key in config:
    if key in caps + [bstack1ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶ्ࠫ")]:
      continue
    bstack1ll111ll11_opy_[key] = config[key]
  if bstack1ll111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॎ") in config:
    for bstack1ll11111l1_opy_ in config[bstack1ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॏ")][index]:
      if bstack1ll11111l1_opy_ in caps:
        continue
      bstack1ll111ll11_opy_[bstack1ll11111l1_opy_] = config[bstack1ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॐ")][index][bstack1ll11111l1_opy_]
  bstack1ll111ll11_opy_[bstack1ll111_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧ॑")] = socket.gethostname()
  if bstack1ll111_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴ॒ࠧ") in bstack1ll111ll11_opy_:
    del (bstack1ll111ll11_opy_[bstack1ll111_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨ॓")])
  return bstack1ll111ll11_opy_
def bstack11ll1l1l1_opy_(config):
  global bstack11l1l1l1_opy_
  bstack11llllll1_opy_ = {}
  caps = bstack111l111lll_opy_
  if bstack11l1l1l1_opy_:
    caps += bstack1lll1l1l1_opy_
  for key in caps:
    if key in config:
      bstack11llllll1_opy_[key] = config[key]
  return bstack11llllll1_opy_
def bstack1ll111l1_opy_(bstack1ll111ll11_opy_, bstack11llllll1_opy_):
  bstack1ll11lllll_opy_ = {}
  for key in bstack1ll111ll11_opy_.keys():
    if key in bstack1l11ll111l_opy_:
      bstack1ll11lllll_opy_[bstack1l11ll111l_opy_[key]] = bstack1ll111ll11_opy_[key]
    else:
      bstack1ll11lllll_opy_[key] = bstack1ll111ll11_opy_[key]
  for key in bstack11llllll1_opy_:
    if key in bstack1l11ll111l_opy_:
      bstack1ll11lllll_opy_[bstack1l11ll111l_opy_[key]] = bstack11llllll1_opy_[key]
    else:
      bstack1ll11lllll_opy_[key] = bstack11llllll1_opy_[key]
  return bstack1ll11lllll_opy_
def get_caps(config, index=0):
  global bstack11l1l1l1_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack11ll11111_opy_ = bstack1111ll11l_opy_(bstack1111l1llll_opy_, config, logger)
  bstack11llllll1_opy_ = bstack11ll1l1l1_opy_(config)
  bstack111l1111_opy_ = bstack111l111lll_opy_
  bstack111l1111_opy_ += bstack1l1l11l11l_opy_
  bstack11llllll1_opy_ = update(bstack11llllll1_opy_, bstack11ll11111_opy_)
  if bstack11l1l1l1_opy_:
    bstack111l1111_opy_ += bstack1lll1l1l1_opy_
  if bstack1ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ॔") in config:
    if bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧॕ") in config[bstack1ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॖ")][index]:
      caps[bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩॗ")] = config[bstack1ll111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨक़")][index][bstack1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫख़")]
    if bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨग़") in config[bstack1ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫज़")][index]:
      caps[bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪड़")] = str(config[bstack1ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ढ़")][index][bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬफ़")])
    bstack1l11111l1_opy_ = bstack1111ll11l_opy_(bstack1111l1llll_opy_, config[bstack1ll111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨय़")][index], logger)
    bstack111l1111_opy_ += list(bstack1l11111l1_opy_.keys())
    for bstack1lll1111l_opy_ in bstack111l1111_opy_:
      if bstack1lll1111l_opy_ in config[bstack1ll111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩॠ")][index]:
        if bstack1lll1111l_opy_ == bstack1ll111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩॡ"):
          try:
            bstack1l11111l1_opy_[bstack1lll1111l_opy_] = str(config[bstack1ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫॢ")][index][bstack1lll1111l_opy_] * 1.0)
          except:
            bstack1l11111l1_opy_[bstack1lll1111l_opy_] = str(config[bstack1ll111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॣ")][index][bstack1lll1111l_opy_])
        else:
          bstack1l11111l1_opy_[bstack1lll1111l_opy_] = config[bstack1ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭।")][index][bstack1lll1111l_opy_]
        del (config[bstack1ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ॥")][index][bstack1lll1111l_opy_])
    bstack11llllll1_opy_ = update(bstack11llllll1_opy_, bstack1l11111l1_opy_)
  bstack1ll111ll11_opy_ = bstack1l1l1ll1l1_opy_(config, index)
  for bstack1lll1ll11_opy_ in bstack111l111lll_opy_ + list(bstack11ll11111_opy_.keys()):
    if bstack1lll1ll11_opy_ in bstack1ll111ll11_opy_:
      bstack11llllll1_opy_[bstack1lll1ll11_opy_] = bstack1ll111ll11_opy_[bstack1lll1ll11_opy_]
      del (bstack1ll111ll11_opy_[bstack1lll1ll11_opy_])
  if bstack1111lllll_opy_(config):
    bstack1ll111ll11_opy_[bstack1ll111_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ०")] = True
    caps.update(bstack11llllll1_opy_)
    caps[bstack1ll111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ१")] = bstack1ll111ll11_opy_
  else:
    bstack1ll111ll11_opy_[bstack1ll111_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧ२")] = False
    caps.update(bstack1ll111l1_opy_(bstack1ll111ll11_opy_, bstack11llllll1_opy_))
    if bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭३") in caps:
      caps[bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪ४")] = caps[bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ५")]
      del (caps[bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ६")])
    if bstack1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭७") in caps:
      caps[bstack1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ८")] = caps[bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ९")]
      del (caps[bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ॰")])
  return caps
def bstack1ll1l111_opy_():
  global bstack1l1l11lll_opy_
  global CONFIG
  if bstack1l1l11lll_opy_ != bstack1ll111_opy_ (u"ࠩࠪॱ") and (bstack1l1l11lll_opy_.startswith(bstack1ll111_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫॲ")) or bstack1l1l11lll_opy_.startswith(bstack1ll111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࠭ॳ"))):
    return bstack1l1l11lll_opy_
  if bstack11l1l1l11_opy_() <= version.parse(bstack1ll111_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬॴ")):
    if bstack1l1l11lll_opy_ != bstack1ll111_opy_ (u"࠭ࠧॵ"):
      return bstack1ll111_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣॶ") + bstack1l1l11lll_opy_ + bstack1ll111_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧॷ")
    return bstack11l11l11l1_opy_
  if bstack1l1l11lll_opy_ != bstack1ll111_opy_ (u"ࠩࠪॸ"):
    return bstack1ll111_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧॹ") + bstack1l1l11lll_opy_ + bstack1ll111_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧॺ")
  return HTTPS_HUB
def bstack1ll1ll11_opy_(options):
  return hasattr(options, bstack1ll111_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭ॻ"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack11l1l1llll_opy_(options, bstack11l1lll1ll_opy_):
  for bstack1l11l11lll_opy_ in bstack11l1lll1ll_opy_:
    if bstack1l11l11lll_opy_ in [bstack1ll111_opy_ (u"࠭ࡡࡳࡩࡶࠫॼ"), bstack1ll111_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫॽ")]:
      continue
    if bstack1l11l11lll_opy_ in options._experimental_options:
      options._experimental_options[bstack1l11l11lll_opy_] = update(options._experimental_options[bstack1l11l11lll_opy_],
                                                         bstack11l1lll1ll_opy_[bstack1l11l11lll_opy_])
    else:
      options.add_experimental_option(bstack1l11l11lll_opy_, bstack11l1lll1ll_opy_[bstack1l11l11lll_opy_])
  if bstack1ll111_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ॾ") in bstack11l1lll1ll_opy_:
    for arg in bstack11l1lll1ll_opy_[bstack1ll111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॿ")]:
      options.add_argument(arg)
    del (bstack11l1lll1ll_opy_[bstack1ll111_opy_ (u"ࠪࡥࡷ࡭ࡳࠨঀ")])
  if bstack1ll111_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨঁ") in bstack11l1lll1ll_opy_:
    for ext in bstack11l1lll1ll_opy_[bstack1ll111_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩং")]:
      try:
        options.add_extension(ext)
      except OSError:
        options.add_encoded_extension(ext)
    del (bstack11l1lll1ll_opy_[bstack1ll111_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪঃ")])
def bstack1l11lll1l_opy_(options):
  global CONFIG
  global bstack1ll1111l1l_opy_
  try:
    if not bstack1ll1111l1l_opy_ or not options:
      return options
    from bstack_utils.bstack111l111ll1_opy_ import bstack11l1ll1l_opy_
    bstack111lll1l1_opy_ = bstack11l1ll1l_opy_(options, bstack1l11l111l_opy_=bstack1ll111_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢ঄"))
    if bstack111lll1l1_opy_ > 0:
      logger.debug(bstack1ll111_opy_ (u"ࠣࡎࡲࡥࡩࠦࡴࡦࡵࡷ࡭ࡳ࡭࠺ࠡࡃࡧࡨࡪࡪࠠࡼࡿࠣࡨࡪ࡬ࡡࡶ࡮ࡷࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠠࡧࡱࡵࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠦঅ").format(bstack111lll1l1_opy_))
  except Exception as e:
    logger.debug(bstack1ll111_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡯࡮࡫ࡧࡦࡸࠥࡲ࡯ࡢࡦࠣࡸࡪࡹࡴࡪࡰࡪࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡴࡶࡴࡪࡱࡱࡷ࠿ࠦࡻࡾࠤআ").format(e))
  return options
def bstack1l1l11111l_opy_(options, bstack11lll11111_opy_):
  if bstack1ll111_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩই") in bstack11lll11111_opy_:
    for bstack1ll1l1l1l1_opy_ in bstack11lll11111_opy_[bstack1ll111_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪঈ")]:
      if bstack1ll1l1l1l1_opy_ in options._preferences:
        options._preferences[bstack1ll1l1l1l1_opy_] = update(options._preferences[bstack1ll1l1l1l1_opy_], bstack11lll11111_opy_[bstack1ll111_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫউ")][bstack1ll1l1l1l1_opy_])
      else:
        options.set_preference(bstack1ll1l1l1l1_opy_, bstack11lll11111_opy_[bstack1ll111_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬঊ")][bstack1ll1l1l1l1_opy_])
  if bstack1ll111_opy_ (u"ࠧࡢࡴࡪࡷࠬঋ") in bstack11lll11111_opy_:
    for arg in bstack11lll11111_opy_[bstack1ll111_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ঌ")]:
      options.add_argument(arg)
def bstack111lll1l1l_opy_(options, bstack1l111lll1_opy_):
  if bstack1ll111_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࠪ঍") in bstack1l111lll1_opy_:
    options.use_webview(bool(bstack1l111lll1_opy_[bstack1ll111_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࠫ঎")]))
  bstack11l1l1llll_opy_(options, bstack1l111lll1_opy_)
def bstack1l1l1l1ll1_opy_(options, bstack1lll111ll_opy_):
  for bstack1111ll1l1l_opy_ in bstack1lll111ll_opy_:
    if bstack1111ll1l1l_opy_ in [bstack1ll111_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨএ"), bstack1ll111_opy_ (u"ࠬࡧࡲࡨࡵࠪঐ")]:
      continue
    options.set_capability(bstack1111ll1l1l_opy_, bstack1lll111ll_opy_[bstack1111ll1l1l_opy_])
  if bstack1ll111_opy_ (u"࠭ࡡࡳࡩࡶࠫ঑") in bstack1lll111ll_opy_:
    for arg in bstack1lll111ll_opy_[bstack1ll111_opy_ (u"ࠧࡢࡴࡪࡷࠬ঒")]:
      options.add_argument(arg)
  if bstack1ll111_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬও") in bstack1lll111ll_opy_:
    options.bstack1l1l1l11_opy_(bool(bstack1lll111ll_opy_[bstack1ll111_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭ঔ")]))
def bstack1l11l1l1l1_opy_(options, bstack11l1lll1l_opy_):
  for bstack11llll1lll_opy_ in bstack11l1lll1l_opy_:
    if bstack11llll1lll_opy_ in [bstack1ll111_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧক"), bstack1ll111_opy_ (u"ࠫࡦࡸࡧࡴࠩখ")]:
      continue
    options._options[bstack11llll1lll_opy_] = bstack11l1lll1l_opy_[bstack11llll1lll_opy_]
  if bstack1ll111_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩগ") in bstack11l1lll1l_opy_:
    for bstack1l111ll1_opy_ in bstack11l1lll1l_opy_[bstack1ll111_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪঘ")]:
      options.bstack1l11111ll1_opy_(
        bstack1l111ll1_opy_, bstack11l1lll1l_opy_[bstack1ll111_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫঙ")][bstack1l111ll1_opy_])
  if bstack1ll111_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭চ") in bstack11l1lll1l_opy_:
    for arg in bstack11l1lll1l_opy_[bstack1ll111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧছ")]:
      options.add_argument(arg)
def bstack1l111lllll_opy_(options, caps):
  if not hasattr(options, bstack1ll111_opy_ (u"ࠪࡏࡊ࡟ࠧজ")):
    return
  if options.KEY == bstack1ll111_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩঝ"):
    options = bstack1ll11lll11_opy_.bstack1l11llll1_opy_(bstack111llll1l_opy_=options, config=CONFIG)
  if options.KEY == bstack1ll111_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪঞ") and options.KEY in caps:
    bstack11l1l1llll_opy_(options, caps[bstack1ll111_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫট")])
  elif options.KEY == bstack1ll111_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬঠ") and options.KEY in caps:
    bstack1l1l11111l_opy_(options, caps[bstack1ll111_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ড")])
  elif options.KEY == bstack1ll111_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪঢ") and options.KEY in caps:
    bstack1l1l1l1ll1_opy_(options, caps[bstack1ll111_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫণ")])
  elif options.KEY == bstack1ll111_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬত") and options.KEY in caps:
    bstack111lll1l1l_opy_(options, caps[bstack1ll111_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭থ")])
  elif options.KEY == bstack1ll111_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬদ") and options.KEY in caps:
    bstack1l11l1l1l1_opy_(options, caps[bstack1ll111_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ধ")])
def bstack1l11ll1ll_opy_(caps):
  global bstack11l1l1l1_opy_
  if isinstance(os.environ.get(bstack1ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩন")), str):
    bstack11l1l1l1_opy_ = eval(os.getenv(bstack1ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ঩")))
  if bstack11l1l1l1_opy_:
    if bstack1l1111ll1_opy_() < version.parse(bstack1ll111_opy_ (u"ࠪ࠶࠳࠹࠮࠱ࠩপ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1ll111_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫফ")
    if bstack1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪব") in caps:
      browser = caps[bstack1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫভ")]
    elif bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨম") in caps:
      browser = caps[bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩয")]
    browser = str(browser).lower()
    if browser == bstack1ll111_opy_ (u"ࠩ࡬ࡴ࡭ࡵ࡮ࡦࠩর") or browser == bstack1ll111_opy_ (u"ࠪ࡭ࡵࡧࡤࠨ঱"):
      browser = bstack1ll111_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫল")
    if browser == bstack1ll111_opy_ (u"ࠬࡹࡡ࡮ࡵࡸࡲ࡬࠭঳"):
      browser = bstack1ll111_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭঴")
    if browser not in [bstack1ll111_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ঵"), bstack1ll111_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭শ"), bstack1ll111_opy_ (u"ࠩ࡬ࡩࠬষ"), bstack1ll111_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪস"), bstack1ll111_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬহ")]:
      return None
    try:
      package = bstack1ll111_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡿࢂ࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧ঺").format(browser)
      name = bstack1ll111_opy_ (u"࠭ࡏࡱࡶ࡬ࡳࡳࡹࠧ঻")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1ll1ll11_opy_(options):
        return None
      for bstack1lll1ll11_opy_ in caps.keys():
        options.set_capability(bstack1lll1ll11_opy_, caps[bstack1lll1ll11_opy_])
      bstack1l111lllll_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack111ll1l11l_opy_(options, bstack11l111llll_opy_):
  if not bstack1ll1ll11_opy_(options):
    return
  for bstack1lll1ll11_opy_ in bstack11l111llll_opy_.keys():
    if bstack1lll1ll11_opy_ in bstack1l1l11l11l_opy_:
      continue
    if bstack1lll1ll11_opy_ in options._caps and type(options._caps[bstack1lll1ll11_opy_]) in [dict, list]:
      options._caps[bstack1lll1ll11_opy_] = update(options._caps[bstack1lll1ll11_opy_], bstack11l111llll_opy_[bstack1lll1ll11_opy_])
    else:
      options.set_capability(bstack1lll1ll11_opy_, bstack11l111llll_opy_[bstack1lll1ll11_opy_])
  bstack1l111lllll_opy_(options, bstack11l111llll_opy_)
  if bstack1ll111_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ়࠭") in options._caps:
    if options._caps[bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ঽ")] and options._caps[bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧা")].lower() != bstack1ll111_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫি"):
      del options._caps[bstack1ll111_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪী")]
def bstack1l11llllll_opy_(proxy_config):
  if bstack1ll111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩু") in proxy_config:
    proxy_config[bstack1ll111_opy_ (u"࠭ࡳࡴ࡮ࡓࡶࡴࡾࡹࠨূ")] = proxy_config[bstack1ll111_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫৃ")]
    del (proxy_config[bstack1ll111_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬৄ")])
  if bstack1ll111_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬ৅") in proxy_config and proxy_config[bstack1ll111_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭৆")].lower() != bstack1ll111_opy_ (u"ࠫࡩ࡯ࡲࡦࡥࡷࠫে"):
    proxy_config[bstack1ll111_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨৈ")] = bstack1ll111_opy_ (u"࠭࡭ࡢࡰࡸࡥࡱ࠭৉")
  if bstack1ll111_opy_ (u"ࠧࡱࡴࡲࡼࡾࡇࡵࡵࡱࡦࡳࡳ࡬ࡩࡨࡗࡵࡰࠬ৊") in proxy_config:
    proxy_config[bstack1ll111_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫো")] = bstack1ll111_opy_ (u"ࠩࡳࡥࡨ࠭ৌ")
  return proxy_config
def bstack1l1111l111_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1ll111_opy_ (u"ࠪࡴࡷࡵࡸࡺ্ࠩ") in config:
    return proxy
  config[bstack1ll111_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪৎ")] = bstack1l11llllll_opy_(config[bstack1ll111_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ৏")])
  if proxy == None:
    proxy = Proxy(config[bstack1ll111_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ৐")])
  return proxy
def bstack111lllll_opy_(self):
  global CONFIG
  global bstack1ll1ll11l_opy_
  try:
    proxy = bstack11lll11l_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1ll111_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ৑")):
        proxies = bstack1l1l11l1l_opy_(proxy, bstack1ll1l111_opy_())
        if len(proxies) > 0:
          protocol, bstack111l111l_opy_ = proxies.popitem()
          if bstack1ll111_opy_ (u"ࠣ࠼࠲࠳ࠧ৒") in bstack111l111l_opy_:
            return bstack111l111l_opy_
          else:
            return bstack1ll111_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ৓") + bstack111l111l_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1ll111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡰࡳࡱࡻࡽࠥࡻࡲ࡭ࠢ࠽ࠤࢀࢃࠢ৔").format(str(e)))
  return bstack1ll1ll11l_opy_(self)
def bstack1111l1l11l_opy_():
  global CONFIG
  return bstack1lll1ll1l_opy_(CONFIG) and bstack11ll1ll11l_opy_() and bstack11l1l1l11_opy_() >= version.parse(bstack1l11l11l1l_opy_)
def bstack11l1lllll_opy_():
  global CONFIG
  return (bstack1ll111_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ৕") in CONFIG or bstack1ll111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ৖") in CONFIG) and bstack1l1l111l11_opy_()
def bstack1l1ll1l11_opy_(config):
  bstack111lll1ll_opy_ = {}
  if bstack1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪৗ") in config:
    bstack111lll1ll_opy_ = config[bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ৘")]
  if bstack1ll111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ৙") in config:
    bstack111lll1ll_opy_ = config[bstack1ll111_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ৚")]
  proxy = bstack11lll11l_opy_(config)
  if proxy:
    if proxy.endswith(bstack1ll111_opy_ (u"ࠪ࠲ࡵࡧࡣࠨ৛")) and os.path.isfile(proxy):
      bstack111lll1ll_opy_[bstack1ll111_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧড়")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1ll111_opy_ (u"ࠬ࠴ࡰࡢࡥࠪঢ়")):
        proxies = bstack111lllllll_opy_(config, bstack1ll1l111_opy_())
        if len(proxies) > 0:
          protocol, bstack111l111l_opy_ = proxies.popitem()
          if bstack1ll111_opy_ (u"ࠨ࠺࠰࠱ࠥ৞") in bstack111l111l_opy_:
            parsed_url = urlparse(bstack111l111l_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1ll111_opy_ (u"ࠢ࠻࠱࠲ࠦয়") + bstack111l111l_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack111lll1ll_opy_[bstack1ll111_opy_ (u"ࠨࡲࡵࡳࡽࡿࡈࡰࡵࡷࠫৠ")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack111lll1ll_opy_[bstack1ll111_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬৡ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack111lll1ll_opy_[bstack1ll111_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭ৢ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack111lll1ll_opy_[bstack1ll111_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧৣ")] = str(parsed_url.password)
  return bstack111lll1ll_opy_
def bstack1llll1111_opy_(config):
  if bstack1ll111_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪ৤") in config:
    return config[bstack1ll111_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫ৥")]
  return {}
def update_caps_for_local(caps):
  global bstack11l111ll1l_opy_
  if bstack1ll111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ০") in caps:
    caps[bstack1ll111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ১")][bstack1ll111_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨ২")] = True
    if bstack11l111ll1l_opy_:
      caps[bstack1ll111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ৩")][bstack1ll111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭৪")] = bstack11l111ll1l_opy_
  else:
    caps[bstack1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪ৫")] = True
    if bstack11l111ll1l_opy_:
      caps[bstack1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ৬")] = bstack11l111ll1l_opy_
@measure(event_name=EVENTS.bstack1lllll1l1l_opy_, stage=STAGE.bstack11ll1111_opy_, bstack11l11l111_opy_=SESSION_NAME)
def bstack111ll1lll1_opy_():
  global CONFIG
  if not bstack1l111l111_opy_(CONFIG) or cli.is_enabled(CONFIG):
    return
  if bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ৭") in CONFIG and bstack1l11lll111_opy_(CONFIG[bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ৮")]):
    if (
      bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭৯") in CONFIG
      and bstack1l11lll111_opy_(CONFIG[bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧৰ")].get(bstack1ll111_opy_ (u"ࠫࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠨৱ")))
    ):
      logger.debug(bstack1ll111_opy_ (u"ࠧࡒ࡯ࡤࡣ࡯ࠤࡧ࡯࡮ࡢࡴࡼࠤࡳࡵࡴࠡࡵࡷࡥࡷࡺࡥࡥࠢࡤࡷࠥࡹ࡫ࡪࡲࡅ࡭ࡳࡧࡲࡺࡋࡱ࡭ࡹ࡯ࡡ࡭࡫ࡶࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠨ৲"))
      return
    bstack111lll1ll_opy_ = bstack1l1ll1l11_opy_(CONFIG)
    bstack1l11ll11_opy_(CONFIG[bstack1ll111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ৳")], bstack111lll1ll_opy_)
def bstack1l11ll11_opy_(key, bstack111lll1ll_opy_):
  global bstack1ll1llll1l_opy_
  logger.info(bstack1l11l1l11_opy_)
  try:
    bstack1ll1llll1l_opy_ = Local()
    bstack111lll11l_opy_ = {bstack1ll111_opy_ (u"ࠧ࡬ࡧࡼࠫ৴"): key}
    bstack111lll11l_opy_.update(bstack111lll1ll_opy_)
    logger.debug(bstack11l1llll1l_opy_.format(str(bstack111lll11l_opy_)).replace(key, bstack1ll111_opy_ (u"ࠨ࡝ࡕࡉࡉࡇࡃࡕࡇࡇࡡࠬ৵")))
    bstack1ll1llll1l_opy_.start(**bstack111lll11l_opy_)
    if bstack1ll1llll1l_opy_.isRunning():
      logger.info(bstack1111l1ll11_opy_)
  except Exception as e:
    bstack1111l1l1ll_opy_(bstack1ll11111ll_opy_.format(str(e)))
def bstack1111l1lll1_opy_():
  global bstack1ll1llll1l_opy_
  if bstack1ll1llll1l_opy_.isRunning():
    logger.info(bstack1ll11lll_opy_)
    bstack1ll1llll1l_opy_.stop()
  bstack1ll1llll1l_opy_ = None
def bstack11ll1llll_opy_(bstack1lll1l1l_opy_=[]):
  global CONFIG
  bstack11ll1l1lll_opy_ = []
  bstack111lll1111_opy_ = [bstack1ll111_opy_ (u"ࠩࡲࡷࠬ৶"), bstack1ll111_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭৷"), bstack1ll111_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨ৸"), bstack1ll111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ৹"), bstack1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ৺"), bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ৻")]
  try:
    for err in bstack1lll1l1l_opy_:
      bstack111lllll1l_opy_ = {}
      for k in bstack111lll1111_opy_:
        val = CONFIG[bstack1ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫৼ")][int(err[bstack1ll111_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ৽")])].get(k)
        if val:
          bstack111lllll1l_opy_[k] = val
      if(err[bstack1ll111_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ৾")] != bstack1ll111_opy_ (u"ࠫࠬ৿")):
        bstack111lllll1l_opy_[bstack1ll111_opy_ (u"ࠬࡺࡥࡴࡶࡶࠫ਀")] = {
          err[bstack1ll111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫਁ")]: err[bstack1ll111_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ਂ")]
        }
        bstack11ll1l1lll_opy_.append(bstack111lllll1l_opy_)
  except Exception as e:
    logger.debug(bstack1ll111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪࡴࡸ࡭ࡢࡶࡷ࡭ࡳ࡭ࠠࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴ࠻ࠢࠪਃ") + str(e))
  finally:
    return bstack11ll1l1lll_opy_
def bstack11l111l1_opy_(file_name):
  bstack111l1lll1_opy_ = []
  try:
    bstack1111l11l1_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1111l11l1_opy_):
      with open(bstack1111l11l1_opy_) as f:
        bstack1111l11lll_opy_ = json.load(f)
        bstack111l1lll1_opy_ = bstack1111l11lll_opy_
      os.remove(bstack1111l11l1_opy_)
    return bstack111l1lll1_opy_
  except Exception as e:
    logger.debug(bstack1ll111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡫࡯࡮ࡥ࡫ࡱ࡫ࠥ࡫ࡲࡳࡱࡵࠤࡱ࡯ࡳࡵ࠼ࠣࠫ਄") + str(e))
    return bstack111l1lll1_opy_
def bstack1ll1ll1lll_opy_():
  try:
      import time
      from bstack_utils.constants import bstack1l1l111l_opy_, EVENTS
      from bstack_utils.helper import bstack11111l1l_opy_, get_host_info, global_config
      from datetime import datetime
      from filelock import FileLock
      from bstack_utils.bstack11lll11l1l_opy_ import bstack111ll11111_opy_
      bstack111ll11111_opy_.bstack1l1ll1l1ll_opy_()
      bstack1ll1l1ll1_opy_ = os.path.join(os.getcwd(), bstack1ll111_opy_ (u"ࠪࡰࡴ࡭ࠧਅ"), bstack1ll111_opy_ (u"ࠫࡰ࡫ࡹ࠮࡯ࡨࡸࡷ࡯ࡣࡴ࠰࡭ࡷࡴࡴࠧਆ"))
      data = None
      lock = FileLock(bstack1ll1l1ll1_opy_+bstack1ll111_opy_ (u"ࠧ࠴࡬ࡰࡥ࡮ࠦਇ"), timeout=2)
      try:
          with lock:
              with open(bstack1ll1l1ll1_opy_, bstack1ll111_opy_ (u"ࠨࡲࠣਈ"), encoding=bstack1ll111_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨਉ")) as file:
                  data = json.load(file)
      except Exception as e:
          logger.debug(bstack1ll111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡷ࡫ࡡࡥࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹࠠࡧ࡫࡯ࡩ࠿ࠦࡻࡾࠤਊ").format(e))
          return
      if not data:
          return
      def bstack111l1lll11_opy_():
          try:
              config = {
                  bstack1ll111_opy_ (u"ࠤ࡫ࡩࡦࡪࡥࡳࡵࠥ਋"): {
                      bstack1ll111_opy_ (u"ࠥࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠤ਌"): bstack1ll111_opy_ (u"ࠦࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠢ਍"),
                  }
              }
              bstack1lllll1ll1_opy_ = datetime.utcnow()
              current_time = bstack1lllll1ll1_opy_.strftime(bstack1ll111_opy_ (u"࡙ࠧࠫ࠮ࠧࡰ࠱ࠪࡪࡔࠦࡊ࠽ࠩࡒࡀࠥࡔ࠰ࠨࡪ࡛ࠥࡔࡄࠤ਎"))
              test_id = os.environ.get(bstack1ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫਏ")) if os.environ.get(bstack1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬਐ")) else global_config.get_property(bstack1ll111_opy_ (u"ࠣࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠥ਑"))
              payload = {
                  bstack1ll111_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪࠨ਒"): bstack1ll111_opy_ (u"ࠥࡷࡩࡱ࡟ࡦࡸࡨࡲࡹࡹࠢਓ"),
                  bstack1ll111_opy_ (u"ࠦࡩࡧࡴࡢࠤਔ"): {
                      bstack1ll111_opy_ (u"ࠧࡺࡥࡴࡶ࡫ࡹࡧࡥࡵࡶ࡫ࡧࠦਕ"): test_id,
                      bstack1ll111_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡪ࡟ࡥࡣࡼࠦਖ"): current_time,
                      bstack1ll111_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥ࡮ࡢ࡯ࡨࠦਗ"): bstack1ll111_opy_ (u"ࠣࡕࡇࡏࡋ࡫ࡡࡵࡷࡵࡩࡕ࡫ࡲࡧࡱࡵࡱࡦࡴࡣࡦࠤਘ"),
                      bstack1ll111_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠ࡬ࡶࡳࡳࠨਙ"): {
                          bstack1ll111_opy_ (u"ࠥࡱࡪࡧࡳࡶࡴࡨࡷࠧਚ"): data,
                          bstack1ll111_opy_ (u"ࠦࡸࡪ࡫ࡓࡷࡱࡍࡩࠨਛ"): global_config.get_property(bstack1ll111_opy_ (u"ࠧࡹࡤ࡬ࡔࡸࡲࡎࡪࠢਜ"))
                      },
                      bstack1ll111_opy_ (u"ࠨࡵࡴࡧࡵࡣࡩࡧࡴࡢࠤਝ"): global_config.get_property(bstack1ll111_opy_ (u"ࠢࡶࡵࡨࡶࡓࡧ࡭ࡦࠤਞ")),
                      bstack1ll111_opy_ (u"ࠣࡪࡲࡷࡹࡥࡩ࡯ࡨࡲࠦਟ"): get_host_info()
                  }
              }
              bstack1ll1lllll_opy_ = bstack1l1ll11lll_opy_(cli.config, [bstack1ll111_opy_ (u"ࠤࡤࡴ࡮ࡹࠢਠ"), bstack1ll111_opy_ (u"ࠥࡩࡩࡹࡉ࡯ࡵࡷࡶࡺࡳࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠣਡ"), bstack1ll111_opy_ (u"ࠦࡦࡶࡩࠣਢ")], bstack1l1l111l_opy_)
              response = bstack11111l1l_opy_(bstack1ll111_opy_ (u"ࠧࡖࡏࡔࡖࠥਣ"), bstack1ll1lllll_opy_, payload, config)
              if response.status_code >= 200 and response.status_code < 300:
                  logger.info(bstack1ll111_opy_ (u"ࠨࡋࡦࡻࠣࡱࡪࡺࡲࡪࡥࡶࠤࡸ࡫࡮ࡵࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡶࡲࠤࢀࢃࠢਤ").format(bstack1l1l111l_opy_))
              else:
                  logger.debug(bstack1ll111_opy_ (u"ࠢࡌࡧࡼࠤࡲ࡫ࡴࡳ࡫ࡦࡷࠥࡸࡥࡲࡷࡨࡷࡹࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫ࠤࡸࡺࡡࡵࡷࡶࠤࢀࢃࠢਥ").format(response.status_code))
          except Exception as e:
              logger.debug(bstack1ll111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫࡮ࡥࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹ࠺ࠡࡽࢀࠦਦ").format(e))
      bstack111l1lll11_opy_()
  except Exception as e:
      logger.debug(bstack1ll111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫࡮ࡥࡡ࡮ࡩࡾࡥ࡭ࡦࡶࡵ࡭ࡨࡹ࠺ࠡࡽࢀࠦਧ").format(e))
def bstack1l1l1lll_opy_(bstack1l1l1l1111_opy_=False):
  bstack1ll1llll1_opy_ = bstack1ll111_opy_ (u"ࠥࠦਨ")
  global bstack1l111ll1l_opy_
  global bstack1l111lll11_opy_
  global bstack111ll11l1l_opy_
  global bstack1llll11ll_opy_
  global ROBOT_PYTHON_ERRORS
  global bstack1l11111l11_opy_
  global CONFIG
  bstack11l11lll_opy_ = os.environ.get(bstack1ll111_opy_ (u"ࠫࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ࡟ࡖࡕࡈࡈࠬ਩"))
  if bstack11l11lll_opy_ not in [bstack1ll111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ਪ")]:
    bstack1ll1llll1_opy_ = bstack111ll11111_opy_.bstack111l11l11_opy_(EVENTS.bstack11ll1l111l_opy_)
  percy.shutdown()
  if bstack1l111ll1l_opy_:
    logger.warning(bstack1llll111_opy_.format(str(bstack1l111ll1l_opy_)))
  else:
    try:
      bstack1lll11l1l_opy_ = bstack11l1l11ll_opy_(bstack1ll111_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬਫ"), logger)
      if bstack1lll11l1l_opy_.get(bstack1ll111_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬਬ")) and bstack1lll11l1l_opy_.get(bstack1ll111_opy_ (u"ࠨࡰࡸࡨ࡬࡫࡟࡭ࡱࡦࡥࡱ࠭ਭ")).get(bstack1ll111_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫਮ")):
        logger.warning(bstack1llll111_opy_.format(str(bstack1lll11l1l_opy_[bstack1ll111_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨਯ")][bstack1ll111_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ਰ")])))
    except Exception as e:
      logger.error(e)
  if cli.is_running() and bstack11l11lll_opy_ not in [bstack1ll111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭਱")]:
    if _11l1l1lll1_opy_ is not None:
      bstack1l1l1l1111_opy_ = _11l1l1lll1_opy_
    else:
      bstack1l1l1l1111_opy_ = cli.is_running()
    bstack1lll11111_opy_.invoke(Events.bstack111l11ll1l_opy_)
  elif _11l1l1lll1_opy_ is not None:
    bstack1l1l1l1111_opy_ = _11l1l1lll1_opy_
  logger.info(bstack1ll11ll1ll_opy_)
  global bstack1ll1llll1l_opy_
  if bstack1ll1llll1l_opy_:
    bstack1111l1lll1_opy_()
  try:
    with bstack11llll1ll_opy_:
      bstack11l1l1l111_opy_ = bstack1l111lll11_opy_.copy()
    for driver in bstack11l1l1l111_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1l111111l1_opy_)
  ROBOT_PYTHON_ERRORS = []
  if bstack1l11111l11_opy_ == bstack1ll111_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬਲ"):
    ROBOT_PYTHON_ERRORS = bstack11l111l1_opy_(bstack1ll111_opy_ (u"ࠧࡳࡱࡥࡳࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨਲ਼"))
  if bstack1l11111l11_opy_ == bstack1ll111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ਴") and len(bstack1llll11ll_opy_) == 0:
    bstack1llll11ll_opy_ = bstack11l111l1_opy_(bstack1ll111_opy_ (u"ࠩࡳࡻࡤࡶࡹࡵࡧࡶࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧਵ"))
    if len(bstack1llll11ll_opy_) == 0:
      bstack1llll11ll_opy_ = bstack11l111l1_opy_(bstack1ll111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡴࡵࡶ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩਸ਼"))
  bstack1l11l11l_opy_ = bstack1ll111_opy_ (u"ࠫࠬ਷")
  if len(bstack111ll11l1l_opy_) > 0:
    bstack1l11l11l_opy_ = bstack11ll1llll_opy_(bstack111ll11l1l_opy_)
  elif len(bstack1llll11ll_opy_) > 0:
    bstack1l11l11l_opy_ = bstack11ll1llll_opy_(bstack1llll11ll_opy_)
  elif len(ROBOT_PYTHON_ERRORS) > 0:
    bstack1l11l11l_opy_ = bstack11ll1llll_opy_(ROBOT_PYTHON_ERRORS)
  elif len(bstack11l11l111l_opy_) > 0:
    bstack1l11l11l_opy_ = bstack11ll1llll_opy_(bstack11l11l111l_opy_)
  if bstack11l11lll_opy_ not in [bstack1ll111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ਸ")]:
    def bstack11lll1llll_opy_():
      try:
        if bstack11l11lll_opy_ in [bstack1ll111_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬਹ"), bstack1ll111_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭਺")]:
          bstack1l111ll111_opy_()
      except Exception as e:
        logger.debug(bstack1ll111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪ࡮ࡴࡡ࡭ࡡࡨࡼࡪࡩࡵࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤ਻").format(e))
    def bstack1111ll111_opy_():
      try:
        if bool(bstack1l11l11l_opy_):
          bstack1lll1llll1_opy_(bstack1l11l11l_opy_, bstack1l1l1l1111_opy_=bstack1l1l1l1111_opy_)
        else:
          bstack1lll1llll1_opy_(bstack1l1l1l1111_opy_=bstack1l1l1l1111_opy_)
      except Exception as e:
        logger.debug(bstack1ll111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡵࡨࡲࡩ࡯࡮ࡨࠢࡨࡺࡪࡴࡴ࠻ࠢࡾࢁ਼ࠧ").format(e))
    def bstack1ll1111lll_opy_():
      try:
        logger_utils.bstack11lll1l1_opy_(CONFIG)
      except Exception as e:
        logger.debug(bstack1ll111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡶࡩࡳࡪࡩ࡯ࡩࠣࡰࡴ࡭ࡳ࠻ࠢࡾࢁࠧ਽").format(e))
    bstack1l11lll1ll_opy_ = threading.Thread(target=bstack11lll1llll_opy_)
    bstack11ll1l1ll_opy_ = threading.Thread(target=bstack1111ll111_opy_)
    bstack1111ll11_opy_ = threading.Thread(target=bstack1ll1111lll_opy_)
    threads = [bstack1l11lll1ll_opy_, bstack11ll1l1ll_opy_, bstack1111ll11_opy_]
    for thread in threads:
      try:
        thread.start()
      except Exception as e:
        logger.debug(bstack1ll111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡷࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡺࡨࡳࡧࡤࡨࠥࢁࡽ࠻ࠢࡾࢁࠧਾ").format(thread.name, e))
    for thread in threads:
      try:
        thread.join()
      except Exception as e:
        logger.debug(bstack1ll111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡯ࡵࡩ࡯࡫ࡱ࡫ࠥࡺࡨࡳࡧࡤࡨࠥࢁࡽ࠻ࠢࡾࢁࠧਿ").format(thread.name, e))
    bstack1111ll1l1_opy_(bstack11l111lll_opy_, logger)
    bstack1111ll1l1_opy_(os.path.join(os.getcwd(), bstack1ll111_opy_ (u"࠭࡬ࡰࡩࠪੀ"), bstack1ll111_opy_ (u"ࠧ࡬ࡧࡼ࠱ࡲ࡫ࡴࡳ࡫ࡦࡷ࠳ࡰࡳࡰࡰࠪੁ")), logger)
  if bstack11l11lll_opy_ not in [bstack1ll111_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩੂ")]:
    bstack111ll11111_opy_.end(EVENTS.bstack11ll1l111l_opy_.value, bstack1ll1llll1_opy_ + bstack1ll111_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ੃"), bstack1ll1llll1_opy_ + bstack1ll111_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ੄"), status=True, failure=None, test_name=None)
    bstack1ll1ll1lll_opy_()
    logger_utils.bstack111l11111_opy_()
    logging.shutdown()
  if len(ROBOT_PYTHON_ERRORS) > 0:
    sys.exit(len(ROBOT_PYTHON_ERRORS))
def bstack11llll1l_opy_(bstack111l1l1l1_opy_, frame):
  global global_config
  logger.error(bstack11l11l1ll_opy_)
  global_config.bstack1lll11l111_opy_(bstack1ll111_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡓࡵࠧ੅"), bstack111l1l1l1_opy_)
  if hasattr(signal, bstack1ll111_opy_ (u"࡙ࠬࡩࡨࡰࡤࡰࡸ࠭੆")):
    global_config.bstack1lll11l111_opy_(bstack1ll111_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭ੇ"), signal.Signals(bstack111l1l1l1_opy_).name)
  else:
    global_config.bstack1lll11l111_opy_(bstack1ll111_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡔ࡫ࡪࡲࡦࡲࠧੈ"), bstack1ll111_opy_ (u"ࠨࡕࡌࡋ࡚ࡔࡋࡏࡑ࡚ࡒࠬ੉"))
  bstack1l1l1l1111_opy_ = cli.is_running()
  if bstack1l1l1l1111_opy_:
    bstack1lll11111_opy_.invoke(Events.bstack111l11ll1l_opy_)
  bstack11l11lll_opy_ = os.environ.get(bstack1ll111_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪ੊"))
  if bstack11l11lll_opy_ == bstack1ll111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪੋ") and not cli.is_enabled(CONFIG):
    TestHubHandler.stop(global_config.get_property(bstack1ll111_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡘ࡯ࡧ࡯ࡣ࡯ࠫੌ")))
  bstack1l1l1lll_opy_(bstack1l1l1l1111_opy_)
  sys.exit(1)
def bstack1111l1l1ll_opy_(err):
  logger.critical(bstack1lllll1l11_opy_.format(str(err)))
  bstack1lll1llll1_opy_(bstack1lllll1l11_opy_.format(str(err)), True)
  atexit.unregister(bstack1l1l1lll_opy_)
  bstack1l111ll111_opy_()
  sys.exit(1)
def bstack1l1ll1l1_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1lll1llll1_opy_(message, True)
  atexit.unregister(bstack1l1l1lll_opy_)
  bstack1l111ll111_opy_()
  sys.exit(1)
def bstack1ll1lll1_opy_():
  global CONFIG
  global bstack1111l1l1_opy_
  global bstack11111ll1l_opy_
  global BROWSERSTACK_AUTOMATION
  CONFIG = bstack1ll1l11lll_opy_()
  load_dotenv(CONFIG.get(bstack1ll111_opy_ (u"ࠬ࡫࡮ࡷࡈ࡬ࡰࡪ੍࠭")))
  bstack11l1l1l1l_opy_()
  bstack11ll1ll11_opy_()
  CONFIG = bstack11l1l1111_opy_(CONFIG)
  update(CONFIG, bstack11111ll1l_opy_)
  update(CONFIG, bstack1111l1l1_opy_)
  if not cli.is_enabled(CONFIG):
    CONFIG = bstack11lllll11l_opy_(CONFIG)
  BROWSERSTACK_AUTOMATION = bstack1l111l111_opy_(CONFIG)
  os.environ[bstack1ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ੎")] = BROWSERSTACK_AUTOMATION.__str__().lower()
  global_config.bstack1lll11l111_opy_(bstack1ll111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ੏"), BROWSERSTACK_AUTOMATION)
  if (bstack1ll111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ੐") in CONFIG and bstack1ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬੑ") in bstack1111l1l1_opy_) or (
          bstack1ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭੒") in CONFIG and bstack1ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ੓") not in bstack11111ll1l_opy_):
    if os.getenv(bstack1ll111_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩ੔")):
      CONFIG[bstack1ll111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ੕")] = os.getenv(bstack1ll111_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫ੖"))
    else:
      if not CONFIG.get(bstack1ll111_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠦ੗"), bstack1ll111_opy_ (u"ࠤࠥ੘")) in bstack11ll1l11l_opy_:
        bstack11ll111l1l_opy_()
  elif (bstack1ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ਖ਼") not in CONFIG and bstack1ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ਗ਼") in CONFIG) or (
          bstack1ll111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨਜ਼") in bstack11111ll1l_opy_ and bstack1ll111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩੜ") not in bstack1111l1l1_opy_):
    del (CONFIG[bstack1ll111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ੝")])
  if bstack1ll111l1l1_opy_(CONFIG):
    bstack1111l1l1ll_opy_(bstack1lll1l111_opy_)
  Config.get_instance().bstack1lll11l111_opy_(bstack1ll111_opy_ (u"ࠣࡷࡶࡩࡷࡔࡡ࡮ࡧࠥਫ਼"), CONFIG[bstack1ll111_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ੟")])
  bstack1ll1ll111_opy_()
  bstack1l11lll1l1_opy_()
  if bstack11l1l1l1_opy_ and not CONFIG.get(bstack1ll111_opy_ (u"ࠥࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠨ੠"), bstack1ll111_opy_ (u"ࠦࠧ੡")) in bstack11ll1l11l_opy_:
    CONFIG[bstack1ll111_opy_ (u"ࠬࡧࡰࡱࠩ੢")] = bstack1l1ll1llll_opy_(CONFIG)
    logger.info(bstack11ll11l11_opy_.format(CONFIG[bstack1ll111_opy_ (u"࠭ࡡࡱࡲࠪ੣")]))
  if not BROWSERSTACK_AUTOMATION:
    CONFIG[bstack1ll111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ੤")] = [{}]
def bstack11l1lll11_opy_(config, bstack1l11l11111_opy_):
  global CONFIG
  global bstack11l1l1l1_opy_
  CONFIG = config
  bstack11l1l1l1_opy_ = bstack1l11l11111_opy_
def bstack1l11lll1l1_opy_():
  global CONFIG
  global bstack11l1l1l1_opy_
  if bstack1ll111_opy_ (u"ࠨࡣࡳࡴࠬ੥") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1l1ll1l1_opy_(e, bstack11ll111lll_opy_)
    bstack11l1l1l1_opy_ = True
    global_config.bstack1lll11l111_opy_(bstack1ll111_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨ੦"), True)
def bstack1l1ll1llll_opy_(config):
  bstack11l1l1ll_opy_ = bstack1ll111_opy_ (u"ࠪࠫ੧")
  app = config[bstack1ll111_opy_ (u"ࠫࡦࡶࡰࠨ੨")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1lll111l_opy_:
      if os.path.exists(app):
        bstack11l1l1ll_opy_ = bstack1l1l11111_opy_(config, app)
      elif bstack1l1111111_opy_(app):
        bstack11l1l1ll_opy_ = app
      else:
        bstack1111l1l1ll_opy_(bstack11ll1111ll_opy_.format(app))
    else:
      if bstack1l1111111_opy_(app):
        bstack11l1l1ll_opy_ = app
      elif os.path.exists(app):
        bstack11l1l1ll_opy_ = bstack1l1l11111_opy_(app)
      else:
        bstack1111l1l1ll_opy_(bstack1ll1llllll_opy_)
  else:
    if len(app) > 2:
      bstack1111l1l1ll_opy_(bstack1l1lll1lll_opy_)
    elif len(app) == 2:
      if bstack1ll111_opy_ (u"ࠬࡶࡡࡵࡪࠪ੩") in app and bstack1ll111_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩ੪") in app:
        if os.path.exists(app[bstack1ll111_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ੫")]):
          bstack11l1l1ll_opy_ = bstack1l1l11111_opy_(config, app[bstack1ll111_opy_ (u"ࠨࡲࡤࡸ࡭࠭੬")], app[bstack1ll111_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ੭")])
        else:
          bstack1111l1l1ll_opy_(bstack11ll1111ll_opy_.format(app))
      else:
        bstack1111l1l1ll_opy_(bstack1l1lll1lll_opy_)
    else:
      for key in app:
        if key in bstack1l1l1lll11_opy_:
          if key == bstack1ll111_opy_ (u"ࠪࡴࡦࡺࡨࠨ੮"):
            if os.path.exists(app[key]):
              bstack11l1l1ll_opy_ = bstack1l1l11111_opy_(config, app[key])
            else:
              bstack1111l1l1ll_opy_(bstack11ll1111ll_opy_.format(app))
          else:
            bstack11l1l1ll_opy_ = app[key]
        else:
          bstack1111l1l1ll_opy_(bstack1ll11l1111_opy_)
  return bstack11l1l1ll_opy_
def bstack1l1111111_opy_(bstack11l1l1ll_opy_):
  import re
  bstack1ll1l1l11l_opy_ = re.compile(bstack1ll111_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬࠧࠦ੯"))
  bstack11l1l1ll11_opy_ = re.compile(bstack1ll111_opy_ (u"ࡷࠨ࡞࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭࠳ࡠࡧ࠭ࡻࡃ࠰࡞࠵࠳࠹࡝ࡡ࠱ࡠ࠲ࡣࠪࠥࠤੰ"))
  if bstack1ll111_opy_ (u"࠭ࡢࡴ࠼࠲࠳ࠬੱ") in bstack11l1l1ll_opy_ or re.fullmatch(bstack1ll1l1l11l_opy_, bstack11l1l1ll_opy_) or re.fullmatch(bstack11l1l1ll11_opy_, bstack11l1l1ll_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack111l1l1l_opy_, stage=STAGE.bstack11ll1111_opy_, bstack11l11l111_opy_=SESSION_NAME)
def bstack1l1l11111_opy_(config, path, bstack1111l111l_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1ll111_opy_ (u"ࠧࡳࡤࠪੲ")).read()).hexdigest()
  bstack11l1l111l1_opy_ = bstack11lllll1ll_opy_(md5_hash)
  bstack11l1l1ll_opy_ = None
  if bstack11l1l111l1_opy_:
    logger.info(bstack11llll1l1l_opy_.format(bstack11l1l111l1_opy_, md5_hash))
    return bstack11l1l111l1_opy_
  bstack1ll1l1l111_opy_ = datetime.datetime.now()
  multipart_data = MultipartEncoder(
    fields={
      bstack1ll111_opy_ (u"ࠨࡨ࡬ࡰࡪ࠭ੳ"): (os.path.basename(path), open(os.path.abspath(path), bstack1ll111_opy_ (u"ࠩࡵࡦࠬੴ")), bstack1ll111_opy_ (u"ࠪࡸࡪࡾࡴ࠰ࡲ࡯ࡥ࡮ࡴࠧੵ")),
      bstack1ll111_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧ੶"): bstack1111l111l_opy_
    }
  )
  response = requests.post(bstack1ll1l1ll_opy_, data=multipart_data,
                           headers={bstack1ll111_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ੷"): multipart_data.content_type},
                           auth=(config[bstack1ll111_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ੸")], config[bstack1ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ੹")]))
  try:
    res = json.loads(response.text)
    bstack11l1l1ll_opy_ = res[bstack1ll111_opy_ (u"ࠨࡣࡳࡴࡤࡻࡲ࡭ࠩ੺")]
    logger.info(bstack1ll1l11l11_opy_.format(bstack11l1l1ll_opy_))
    bstack111l1111ll_opy_(md5_hash, bstack11l1l1ll_opy_)
    cli.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺ࡶࡲ࡯ࡳࡦࡪ࡟ࡢࡲࡳࠦ੻"), datetime.datetime.now() - bstack1ll1l1l111_opy_)
  except ValueError as err:
    bstack1111l1l1ll_opy_(bstack11lll11lll_opy_.format(str(err)))
  return bstack11l1l1ll_opy_
def bstack1ll1ll111_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack111ll1l1l1_opy_
  bstack11l1l11111_opy_ = 1
  bstack1llll1l11_opy_ = 1
  if bstack1ll111_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ੼") in CONFIG:
    bstack1llll1l11_opy_ = CONFIG[bstack1ll111_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ੽")]
  else:
    bstack1llll1l11_opy_ = bstack1l1111lll_opy_(framework_name, args) or 1
  if bstack1ll111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ੾") in CONFIG:
    bstack11l1l11111_opy_ = len(CONFIG[bstack1ll111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ੿")])
  bstack111ll1l1l1_opy_ = int(bstack1llll1l11_opy_) * int(bstack11l1l11111_opy_)
def bstack1l1111lll_opy_(framework_name, args):
  if framework_name == bstack1ll1ll1ll1_opy_ and args and bstack1ll111_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ઀") in args:
      bstack11l1lll11l_opy_ = args.index(bstack1ll111_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ઁ"))
      return int(args[bstack11l1lll11l_opy_ + 1]) or 1
  return 1
def bstack11lllll1ll_opy_(md5_hash):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1ll111_opy_ (u"ࠩࡩ࡭ࡱ࡫࡬ࡰࡥ࡮ࠤࡳࡵࡴࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨ࠰ࠥࡻࡳࡪࡰࡪࠤࡧࡧࡳࡪࡥࠣࡪ࡮ࡲࡥࠡࡱࡳࡩࡷࡧࡴࡪࡱࡱࡷࠬં"))
    bstack11lll1ll_opy_ = os.path.join(os.path.expanduser(bstack1ll111_opy_ (u"ࠪࢂࠬઃ")), bstack1ll111_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ઄"), bstack1ll111_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭અ"))
    if os.path.exists(bstack11lll1ll_opy_):
      try:
        bstack1111l1111_opy_ = json.load(open(bstack11lll1ll_opy_, bstack1ll111_opy_ (u"࠭ࡲࡣࠩઆ")))
        if md5_hash in bstack1111l1111_opy_:
          bstack11l1ll111l_opy_ = bstack1111l1111_opy_[md5_hash]
          bstack1lll1ll1ll_opy_ = datetime.datetime.now()
          bstack1l1l11l1_opy_ = datetime.datetime.strptime(bstack11l1ll111l_opy_[bstack1ll111_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪઇ")], bstack1ll111_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬઈ"))
          if (bstack1lll1ll1ll_opy_ - bstack1l1l11l1_opy_).days > 30:
            return None
          elif version.parse(str(__version__)) > version.parse(bstack11l1ll111l_opy_[bstack1ll111_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧઉ")]):
            return None
          return bstack11l1ll111l_opy_[bstack1ll111_opy_ (u"ࠪ࡭ࡩ࠭ઊ")]
      except Exception as e:
        logger.debug(bstack1ll111_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡶࡪࡧࡤࡪࡰࡪࠤࡒࡊ࠵ࠡࡪࡤࡷ࡭ࠦࡦࡪ࡮ࡨ࠾ࠥࢁࡽࠨઋ").format(str(e)))
    return None
  bstack11lll1ll_opy_ = os.path.join(os.path.expanduser(bstack1ll111_opy_ (u"ࠬࢄࠧઌ")), bstack1ll111_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ઍ"), bstack1ll111_opy_ (u"ࠧࡢࡲࡳ࡙ࡵࡲ࡯ࡢࡦࡐࡈ࠺ࡎࡡࡴࡪ࠱࡮ࡸࡵ࡮ࠨ઎"))
  lock_file = bstack11lll1ll_opy_ + bstack1ll111_opy_ (u"ࠨ࠰࡯ࡳࡨࡱࠧએ")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack11lll1ll_opy_):
        with open(bstack11lll1ll_opy_, bstack1ll111_opy_ (u"ࠩࡵࠫઐ")) as f:
          content = f.read().strip()
          if content:
            bstack1111l1111_opy_ = json.loads(content)
            if md5_hash in bstack1111l1111_opy_:
              bstack11l1ll111l_opy_ = bstack1111l1111_opy_[md5_hash]
              bstack1lll1ll1ll_opy_ = datetime.datetime.now()
              bstack1l1l11l1_opy_ = datetime.datetime.strptime(bstack11l1ll111l_opy_[bstack1ll111_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ઑ")], bstack1ll111_opy_ (u"ࠫࠪࡪ࠯ࠦ࡯࠲ࠩ࡞ࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨ઒"))
              if (bstack1lll1ll1ll_opy_ - bstack1l1l11l1_opy_).days > 30:
                return None
              elif version.parse(str(__version__)) > version.parse(bstack11l1ll111l_opy_[bstack1ll111_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪઓ")]):
                return None
              return bstack11l1ll111l_opy_[bstack1ll111_opy_ (u"࠭ࡩࡥࠩઔ")]
      return None
  except Exception as e:
    logger.debug(bstack1ll111_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡷࡪࡶ࡫ࠤ࡫࡯࡬ࡦࠢ࡯ࡳࡨࡱࡩ࡯ࡩࠣࡪࡴࡸࠠࡎࡆ࠸ࠤ࡭ࡧࡳࡩ࠼ࠣࡿࢂ࠭ક").format(str(e)))
    return None
def bstack111l1111ll_opy_(md5_hash, bstack11l1l1ll_opy_):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1ll111_opy_ (u"ࠨࡨ࡬ࡰࡪࡲ࡯ࡤ࡭ࠣࡲࡴࡺࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧ࠯ࠤࡺࡹࡩ࡯ࡩࠣࡦࡦࡹࡩࡤࠢࡩ࡭ࡱ࡫ࠠࡰࡲࡨࡶࡦࡺࡩࡰࡰࡶࠫખ"))
    bstack111l1ll11_opy_ = os.path.join(os.path.expanduser(bstack1ll111_opy_ (u"ࠩࢁࠫગ")), bstack1ll111_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪઘ"))
    if not os.path.exists(bstack111l1ll11_opy_):
      os.makedirs(bstack111l1ll11_opy_)
    bstack11lll1ll_opy_ = os.path.join(os.path.expanduser(bstack1ll111_opy_ (u"ࠫࢃ࠭ઙ")), bstack1ll111_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬચ"), bstack1ll111_opy_ (u"࠭ࡡࡱࡲࡘࡴࡱࡵࡡࡥࡏࡇ࠹ࡍࡧࡳࡩ࠰࡭ࡷࡴࡴࠧછ"))
    bstack1l1llllll1_opy_ = {
      bstack1ll111_opy_ (u"ࠧࡪࡦࠪજ"): bstack11l1l1ll_opy_,
      bstack1ll111_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫઝ"): datetime.datetime.strftime(datetime.datetime.now(), bstack1ll111_opy_ (u"ࠩࠨࡨ࠴ࠫ࡭࠰ࠧ࡜ࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭ઞ")),
      bstack1ll111_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨટ"): str(__version__)
    }
    try:
      bstack1111l1111_opy_ = {}
      if os.path.exists(bstack11lll1ll_opy_):
        bstack1111l1111_opy_ = json.load(open(bstack11lll1ll_opy_, bstack1ll111_opy_ (u"ࠫࡷࡨࠧઠ")))
      bstack1111l1111_opy_[md5_hash] = bstack1l1llllll1_opy_
      with open(bstack11lll1ll_opy_, bstack1ll111_opy_ (u"ࠧࡽࠫࠣડ")) as outfile:
        json.dump(bstack1111l1111_opy_, outfile)
    except Exception as e:
      logger.debug(bstack1ll111_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡻࡰࡥࡣࡷ࡭ࡳ࡭ࠠࡎࡆ࠸ࠤ࡭ࡧࡳࡩࠢࡩ࡭ࡱ࡫࠺ࠡࡽࢀࠫઢ").format(str(e)))
    return
  bstack111l1ll11_opy_ = os.path.join(os.path.expanduser(bstack1ll111_opy_ (u"ࠧࡿࠩણ")), bstack1ll111_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨત"))
  if not os.path.exists(bstack111l1ll11_opy_):
    os.makedirs(bstack111l1ll11_opy_)
  bstack11lll1ll_opy_ = os.path.join(os.path.expanduser(bstack1ll111_opy_ (u"ࠩࢁࠫથ")), bstack1ll111_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪદ"), bstack1ll111_opy_ (u"ࠫࡦࡶࡰࡖࡲ࡯ࡳࡦࡪࡍࡅ࠷ࡋࡥࡸ࡮࠮࡫ࡵࡲࡲࠬધ"))
  lock_file = bstack11lll1ll_opy_ + bstack1ll111_opy_ (u"ࠬ࠴࡬ࡰࡥ࡮ࠫન")
  bstack1l1llllll1_opy_ = {
    bstack1ll111_opy_ (u"࠭ࡩࡥࠩ઩"): bstack11l1l1ll_opy_,
    bstack1ll111_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪપ"): datetime.datetime.strftime(datetime.datetime.now(), bstack1ll111_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬફ")),
    bstack1ll111_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧબ"): str(__version__)
  }
  try:
    with FileLock(lock_file, timeout=10):
      bstack1111l1111_opy_ = {}
      if os.path.exists(bstack11lll1ll_opy_):
        with open(bstack11lll1ll_opy_, bstack1ll111_opy_ (u"ࠪࡶࠬભ")) as f:
          content = f.read().strip()
          if content:
            bstack1111l1111_opy_ = json.loads(content)
      bstack1111l1111_opy_[md5_hash] = bstack1l1llllll1_opy_
      with open(bstack11lll1ll_opy_, bstack1ll111_opy_ (u"ࠦࡼࠨમ")) as outfile:
        json.dump(bstack1111l1111_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1ll111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡼ࡯ࡴࡩࠢࡩ࡭ࡱ࡫ࠠ࡭ࡱࡦ࡯࡮ࡴࡧࠡࡨࡲࡶࠥࡓࡄ࠶ࠢ࡫ࡥࡸ࡮ࠠࡶࡲࡧࡥࡹ࡫࠺ࠡࡽࢀࠫય").format(str(e)))
def bstack11lll111ll_opy_(self):
  return
def bstack1l11l1ll11_opy_(self):
  return
def bstack11ll11l1l_opy_():
  global bstack1llllll1l_opy_
  bstack1llllll1l_opy_ = True
def bstack1l11l111ll_opy_(self):
  global FRAMEWORK_NAME
  global bstack1l11111l_opy_
  global bstack1l11ll11l_opy_
  bstack1l1l1l111_opy_ = bstack111ll11111_opy_.bstack111l11l11_opy_(EVENTS.bstack1l1l11llll_opy_)
  try:
    if bstack1ll111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ર") in FRAMEWORK_NAME and self.session_id != None and bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫ઱"), bstack1ll111_opy_ (u"ࠨࠩલ")) != bstack1ll111_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪળ"):
      bstack1l1l111111_opy_ = bstack1ll111_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ઴") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1ll111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫવ")
      if bstack1l1l111111_opy_ == bstack1ll111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬશ"):
        bstack1111l11l1l_opy_(logger)
      if self != None:
        bstack111lll11_opy_(self, bstack1l1l111111_opy_, bstack1ll111_opy_ (u"࠭ࠬࠡࠩષ").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack1ll111_opy_ (u"ࠧࠨસ")
    if bstack1ll111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨહ") in FRAMEWORK_NAME and getattr(threading.current_thread(), bstack1ll111_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ઺"), None):
      bstack1l1ll11l1l_opy_.bstack1l1l11l111_opy_(self, bstack1111111ll_opy_, logger, wait=True)
    if bstack1ll111_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ઻") in FRAMEWORK_NAME:
      bstack1llll11lll_opy_.bstack1111lll1ll_opy_(self)
    bstack111ll11111_opy_.end(EVENTS.bstack1l1l11llll_opy_.value, bstack1l1l1l111_opy_ + bstack1ll111_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷ઼ࠦ"), bstack1l1l1l111_opy_ + bstack1ll111_opy_ (u"ࠧࡀࡥ࡯ࡦࠥઽ"), status=True, failure=None, test_name=None)
  except Exception as e:
    logger.debug(bstack1ll111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࠢા") + str(e))
    bstack111ll11111_opy_.end(EVENTS.bstack1l1l11llll_opy_.value, bstack1l1l1l111_opy_ + bstack1ll111_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢિ"), bstack1l1l1l111_opy_ + bstack1ll111_opy_ (u"ࠣ࠼ࡨࡲࡩࠨી"), status=False, failure=str(e), test_name=None)
  bstack1l11ll11l_opy_(self)
  self.session_id = None
def bstack1l11lll1_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack111ll11l11_opy_
    global FRAMEWORK_NAME
    command_executor = kwargs.get(bstack1ll111_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠬુ"), bstack1ll111_opy_ (u"ࠪࠫૂ"))
    bstack11l11ll1l_opy_ = False
    if type(command_executor) == str and bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧૃ") in command_executor:
      bstack11l11ll1l_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨૄ") in str(getattr(command_executor, bstack1ll111_opy_ (u"࠭࡟ࡶࡴ࡯ࠫૅ"), bstack1ll111_opy_ (u"ࠧࠨ૆"))):
      bstack11l11ll1l_opy_ = True
    else:
      kwargs = bstack1ll11lll11_opy_.bstack1l11llll1_opy_(bstack111llll1l_opy_=kwargs, config=CONFIG)
      return bstack1111lllll1_opy_(self, *args, **kwargs)
    if bstack11l11ll1l_opy_:
      bstack1ll11l1l11_opy_ = TestHubUtils.bstack1111llll11_opy_(CONFIG, FRAMEWORK_NAME)
      if kwargs.get(bstack1ll111_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩે")):
        kwargs[bstack1ll111_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪૈ")] = bstack111ll11l11_opy_(kwargs[bstack1ll111_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫૉ")], FRAMEWORK_NAME, CONFIG, bstack1ll11l1l11_opy_)
      elif kwargs.get(bstack1ll111_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ૊")):
        kwargs[bstack1ll111_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬો")] = bstack111ll11l11_opy_(kwargs[bstack1ll111_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ૌ")], FRAMEWORK_NAME, CONFIG, bstack1ll11l1l11_opy_)
  except Exception as e:
    logger.error(bstack1ll111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩࡧࡱࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡕࡇࡏࠥࡩࡡࡱࡵ࠽ࠤࢀࢃ્ࠢ").format(str(e)))
  return bstack1111lllll1_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack1l1lll111_opy_, stage=STAGE.bstack11ll1111_opy_, bstack11l11l111_opy_=SESSION_NAME)
def bstack1ll111llll_opy_(self, command_executor=bstack1ll111_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰࠳࠵࠻࠳࠶࠮࠱࠰࠴࠾࠹࠺࠴࠵ࠤ૎"), *args, **kwargs):
  global bstack1l11111l_opy_
  global bstack1l111lll11_opy_
  bstack1l1l1111ll_opy_ = bstack1l11lll1_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack11l1ll1111_opy_.on():
    return bstack1l1l1111ll_opy_
  try:
    logger.debug(bstack1ll111_opy_ (u"ࠩࡆࡳࡲࡳࡡ࡯ࡦࠣࡉࡽ࡫ࡣࡶࡶࡲࡶࠥࡽࡨࡦࡰࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡩࡴࠢࡩࡥࡱࡹࡥࠡ࠯ࠣࡿࢂ࠭૏").format(str(command_executor)))
    logger.debug(bstack1ll111_opy_ (u"ࠪࡌࡺࡨࠠࡖࡔࡏࠤ࡮ࡹࠠ࠮ࠢࡾࢁࠬૐ").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧ૑") in command_executor._url:
      global_config.bstack1lll11l111_opy_(bstack1ll111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭૒"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩ૓") in command_executor):
    global_config.bstack1lll11l111_opy_(bstack1ll111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ૔"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack11ll1ll1l1_opy_ = getattr(threading.current_thread(), bstack1ll111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡕࡧࡶࡸࡒ࡫ࡴࡢࠩ૕"), None)
  bstack11ll111l_opy_ = {}
  if self.capabilities is not None:
    bstack11ll111l_opy_[bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡲࡦࡳࡥࠨ૖")] = self.capabilities.get(bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ૗"))
    bstack11ll111l_opy_[bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭૘")] = self.capabilities.get(bstack1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭૙"))
    bstack11ll111l_opy_[bstack1ll111_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡥ࡯ࡱࡶ࡬ࡳࡳࡹࠧ૚")] = self.capabilities.get(bstack1ll111_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ૛"))
  if CONFIG.get(bstack1ll111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ૜"), False) and bstack1ll11lll11_opy_.bstack111l1l1lll_opy_(bstack11ll111l_opy_):
    threading.current_thread().a11yPlatform = True
  if bstack1ll111_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ૝") in FRAMEWORK_NAME or bstack1ll111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ૞") in FRAMEWORK_NAME:
    TestHubHandler.send_cbt_info(self)
  if bstack1ll111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ૟") in FRAMEWORK_NAME and bstack11ll1ll1l1_opy_ and bstack11ll1ll1l1_opy_.get(bstack1ll111_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬૠ"), bstack1ll111_opy_ (u"࠭ࠧૡ")) == bstack1ll111_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨૢ"):
    TestHubHandler.send_cbt_info(self)
  bstack1l11111l_opy_ = self.session_id
  with bstack11llll1ll_opy_:
    bstack1l111lll11_opy_.append(self)
  return bstack1l1l1111ll_opy_
def bstack1l1111l1_opy_(args):
  return bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠩૣ") in str(args)
def bstack1llllllll_opy_(self, driver_command, *args, **kwargs):
  global bstack1lll11lll1_opy_
  global bstack1ll1ll1l_opy_
  bstack1111ll1ll_opy_ = bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭૤"), None) and bstack11llll11l_opy_(
          threading.current_thread(), bstack1ll111_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ૥"), None)
  bstack11l11l11ll_opy_ = bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ૦"), None) and bstack11llll11l_opy_(
          threading.current_thread(), bstack1ll111_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ૧"), None)
  bstack1111l111_opy_ = getattr(self, bstack1ll111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭૨"), None) != None and getattr(self, bstack1ll111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧ૩"), None) == True
  if not bstack1ll1ll1l_opy_ and bstack1ll111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ૪") in CONFIG and CONFIG[bstack1ll111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ૫")] == True and bstack1l1l1l1lll_opy_.bstack1ll1l1111_opy_(driver_command) and (bstack1111l111_opy_ or bstack1111ll1ll_opy_ or bstack11l11l11ll_opy_) and not bstack1l1111l1_opy_(args):
    try:
      bstack1ll1ll1l_opy_ = True
      logger.debug(bstack1ll111_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡾࢁࠬ૬").format(driver_command))
      bstack11ll1l1111_opy_ = perform_scan(self, driver_command=driver_command)
      logger.debug(bstack11ll1l1111_opy_)
      try:
        bstack1ll1l111l1_opy_ = {
          bstack1ll111_opy_ (u"ࠦࡷ࡫ࡱࡶࡧࡶࡸࠧ૭"): {
            bstack1ll111_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࠨ૮"): bstack1ll111_opy_ (u"ࠨࡁ࠲࠳࡜ࡣࡘࡉࡁࡏࠤ૯"),
            bstack1ll111_opy_ (u"ࠢࡱࡣࡵࡥࡲ࡫ࡴࡦࡴࡶࠦ૰"): [
              {
                bstack1ll111_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠣ૱"): driver_command
              }
            ]
          },
          bstack1ll111_opy_ (u"ࠤࡵࡩࡸࡶ࡯࡯ࡵࡨࠦ૲"): {
            bstack1ll111_opy_ (u"ࠥࡦࡴࡪࡹࠣ૳"): {
              bstack1ll111_opy_ (u"ࠦࡲࡹࡧࠣ૴"): bstack11ll1l1111_opy_.get(bstack1ll111_opy_ (u"ࠧࡳࡳࡨࠤ૵"), bstack1ll111_opy_ (u"ࠨࠢ૶")) if isinstance(bstack11ll1l1111_opy_, dict) else bstack1ll111_opy_ (u"ࠢࠣ૷"),
              bstack1ll111_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴࠤ૸"): bstack11ll1l1111_opy_.get(bstack1ll111_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥૹ"), True) if isinstance(bstack11ll1l1111_opy_, dict) else True
            }
          }
        }
        logger.debug(bstack1ll111_opy_ (u"ࠪࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮ࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡲ࡯ࡨࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠫૺ").format(bstack1ll1l111l1_opy_))
        bstack1l11llll_opy_.info(json.dumps(bstack1ll1l111l1_opy_, separators=(bstack1ll111_opy_ (u"ࠫ࠱࠭ૻ"), bstack1ll111_opy_ (u"ࠬࡀࠧૼ"))))
      except Exception as bstack111ll1ll1l_opy_:
        logger.debug(bstack1ll111_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢ࡯ࡳ࡬ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡤࡣࡱࠤࡩࡧࡴࡢ࠼ࠣࡿࢂ࠭૽").format(str(bstack111ll1ll1l_opy_)))
    except Exception as err:
      logger.debug(bstack1ll111_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡪࡸࡦࡰࡴࡰࠤࡸࡩࡡ࡯ࠢࡾࢁࠬ૾").format(str(err)))
    bstack1ll1ll1l_opy_ = False
  response = bstack1lll11lll1_opy_(self, driver_command, *args, **kwargs)
  if (bstack1ll111_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ૿") in str(FRAMEWORK_NAME).lower() or bstack1ll111_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ଀") in str(FRAMEWORK_NAME).lower()) and bstack11l1ll1111_opy_.on():
    try:
      if driver_command == bstack1ll111_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧଁ"):
        TestHubHandler.bstack11ll11111l_opy_({
            bstack1ll111_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪଂ"): response[bstack1ll111_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫଃ")],
            bstack1ll111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭଄"): TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack11l1ll1111_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
def bstack11l1l11l1_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack1l11111l_opy_
  global PLATFORM_INDEX
  global SESSION_NAME
  global PARALLELISE_VANILLA_PYTHON
  global PARALLELISE_THREADING_PYTHON
  global FRAMEWORK_NAME
  global bstack1111lllll1_opy_
  global bstack1l111lll11_opy_
  global bstack1l1lll11l1_opy_
  global bstack1111111ll_opy_
  bstack1l1l1l111_opy_ = bstack111ll11111_opy_.bstack111l11l11_opy_(EVENTS.bstack11ll11l111_opy_.value)
  if os.getenv(bstack1ll111_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬଅ")) is not None and bstack1ll11lll11_opy_.bstack1111llll1_opy_(CONFIG) is None:
    CONFIG[bstack1ll111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨଆ")] = True
  CONFIG[bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫଇ")] = str(FRAMEWORK_NAME) + str(__version__)
  bstack111l11lll1_opy_ = os.environ[bstack1ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨଈ")]
  bstack1ll11l1l11_opy_ = TestHubUtils.bstack1111llll11_opy_(CONFIG, FRAMEWORK_NAME)
  CONFIG[bstack1ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧଉ")] = bstack111l11lll1_opy_
  CONFIG[bstack1ll111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧଊ")] = bstack1ll11l1l11_opy_
  if CONFIG.get(bstack1ll111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ଋ"),bstack1ll111_opy_ (u"ࠧࠨଌ")) and bstack1ll111_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ଍") in FRAMEWORK_NAME:
    CONFIG[bstack1ll111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ଎")].pop(bstack1ll111_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨଏ"), None)
    CONFIG[bstack1ll111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫଐ")].pop(bstack1ll111_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ଑"), None)
  command_executor = bstack1ll1l111_opy_()
  logger.debug(bstack11ll11lll1_opy_.format(command_executor))
  proxy = bstack1l1111l111_opy_(CONFIG, proxy)
  bstack1l1ll1l1l_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
  try:
    if PARALLELISE_VANILLA_PYTHON is True:
      bstack1l1ll1l1l_opy_ = int(multiprocessing.current_process().name)
    elif PARALLELISE_THREADING_PYTHON is True:
      bstack1l1ll1l1l_opy_ = int(threading.current_thread().name)
  except:
    bstack1l1ll1l1l_opy_ = 0
  bstack11l111llll_opy_ = get_caps(CONFIG, bstack1l1ll1l1l_opy_)
  logger.debug(CONFIG_FILE_CONTENT.format(str(bstack11l111llll_opy_)))
  if bstack1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ଒") in CONFIG and bstack1l11lll111_opy_(CONFIG[bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫଓ")]):
    update_caps_for_local(bstack11l111llll_opy_)
  if bstack1ll11lll11_opy_.bstack1111l1ll1l_opy_(CONFIG, bstack1l1ll1l1l_opy_) and bstack1ll11lll11_opy_.bstack1l1l1l1l1l_opy_(bstack11l111llll_opy_, options, desired_capabilities, CONFIG):
    threading.current_thread().a11yPlatform = True
    if (cli.accessibility is None or not cli.accessibility.is_enabled()):
      bstack1ll11lll11_opy_.set_capabilities(bstack11l111llll_opy_, CONFIG)
  if desired_capabilities:
    bstack1lllll111l_opy_ = bstack11l1l1111_opy_(desired_capabilities)
    bstack1lllll111l_opy_[bstack1ll111_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨଔ")] = bstack1111lllll_opy_(CONFIG)
    bstack111l1ll1ll_opy_ = get_caps(bstack1lllll111l_opy_)
    if bstack111l1ll1ll_opy_:
      bstack11l111llll_opy_ = update(bstack111l1ll1ll_opy_, bstack11l111llll_opy_)
    desired_capabilities = None
  if options:
    bstack111ll1l11l_opy_(options, bstack11l111llll_opy_)
  if not options:
    options = bstack1l11ll1ll_opy_(bstack11l111llll_opy_)
  try:
    if bstack1ll1111l1l_opy_:
      def _11ll111111_opy_(bstack11111l11l_opy_):
        if not isinstance(bstack11111l11l_opy_, dict):
          return
        for _1111l111ll_opy_ in list(bstack11111l11l_opy_.keys()):
          _11ll1l1l11_opy_ = bstack11111l11l_opy_[_1111l111ll_opy_]
          if _11ll1l1l11_opy_ is None:
            bstack11111l11l_opy_.pop(_1111l111ll_opy_, None)
          elif isinstance(_11ll1l1l11_opy_, dict):
            _11ll111111_opy_(_11ll1l1l11_opy_)
      _11ll111111_opy_(bstack11l111llll_opy_)
      _11ll111111_opy_(desired_capabilities)
      if options is not None and hasattr(options, bstack1ll111_opy_ (u"ࠩࡢࡧࡦࡶࡳࠨକ")):
        _11ll111111_opy_(options._caps)
  except Exception as e:
    logger.debug(bstack1ll111_opy_ (u"ࠥࡱࡴࡪ࡟ࡪࡰ࡬ࡸ࠭࠯ࠠࡱࡱࡶࡸ࠲ࡵࡰࡵ࡫ࡲࡲࡸࠦࡰࡳࡷࡱࡩࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡾࠤଖ").format(e))
  if bstack1ll1111l1l_opy_:
    options = bstack1l11lll1l_opy_(options)
  bstack1111111ll_opy_ = CONFIG.get(bstack1ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଗ"))[bstack1l1ll1l1l_opy_]
  if proxy and bstack11l1l1l11_opy_() >= version.parse(bstack1ll111_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬଘ")):
    options.proxy(proxy)
  if options and bstack11l1l1l11_opy_() >= version.parse(bstack1ll111_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬଙ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack11l1l1l11_opy_() < version.parse(bstack1ll111_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ଚ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack11l111llll_opy_)
  logger.info(bstack1l11l11l11_opy_)
  bstack11lll11l1l_opy_.end(EVENTS.bstack11l11l1l1_opy_.value, EVENTS.bstack11l11l1l1_opy_.value + bstack1ll111_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣଛ"), EVENTS.bstack11l11l1l1_opy_.value + bstack1ll111_opy_ (u"ࠤ࠽ࡩࡳࡪࠢଜ"), status=True, failure=None, test_name=SESSION_NAME)
  if bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡵࡸ࡯ࡧ࡫࡯ࡩࠬଝ") in kwargs:
    del kwargs[bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡶࡲࡰࡨ࡬ࡰࡪ࠭ଞ")]
  bstack111ll11111_opy_.end(EVENTS.bstack11ll11l111_opy_.value, bstack1l1l1l111_opy_ + bstack1ll111_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧଟ"), bstack1l1l1l111_opy_ + bstack1ll111_opy_ (u"ࠨ࠺ࡦࡰࡧࠦଠ"), status=True, failure=None, test_name=SESSION_NAME)
  try:
    if bstack11l1l1l11_opy_() >= version.parse(bstack1ll111_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧଡ")):
      bstack1111lllll1_opy_(self, command_executor=command_executor,
                options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
    elif bstack11l1l1l11_opy_() >= version.parse(bstack1ll111_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧଢ")):
      bstack1111lllll1_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities, options=options,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11l1l1l11_opy_() >= version.parse(bstack1ll111_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩଣ")):
      bstack1111lllll1_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    else:
      bstack1111lllll1_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive)
  except Exception as bstack1l1llll1l_opy_:
    logger.error(bstack111lll11l1_opy_.format(bstack1ll111_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠩତ"), str(bstack1l1llll1l_opy_)))
    raise bstack1l1llll1l_opy_
  bstack1l1l1l111_opy_ = bstack111ll11111_opy_.bstack111l11l11_opy_(EVENTS.bstack1l1lll111_opy_.value)
  if bstack1ll11lll11_opy_.bstack1111l1ll1l_opy_(CONFIG, bstack1l1ll1l1l_opy_) and bstack1ll11lll11_opy_.bstack1l1l1l1l1l_opy_(self.caps, options, desired_capabilities):
    if CONFIG[bstack1ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ଥ")][bstack1ll111_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫଦ")] == True:
      threading.current_thread().appA11yPlatform = True
      if cli.accessibility is None or not cli.accessibility.is_enabled():
        bstack1ll11lll11_opy_.set_capabilities(bstack11l111llll_opy_, CONFIG)
  try:
    bstack11l1ll111_opy_ = bstack1ll111_opy_ (u"࠭ࠧଧ")
    if bstack11l1l1l11_opy_() >= version.parse(bstack1ll111_opy_ (u"ࠧ࠵࠰࠳࠲࠵ࡨ࠱ࠨନ")):
      if self.caps is not None:
        bstack11l1ll111_opy_ = self.caps.get(bstack1ll111_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣ଩"))
    else:
      if self.capabilities is not None:
        bstack11l1ll111_opy_ = self.capabilities.get(bstack1ll111_opy_ (u"ࠤࡲࡴࡹ࡯࡭ࡢ࡮ࡋࡹࡧ࡛ࡲ࡭ࠤପ"))
    if bstack11l1ll111_opy_:
      bstack1l111ll11_opy_(bstack11l1ll111_opy_)
      if bstack11l1l1l11_opy_() <= version.parse(bstack1ll111_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪଫ")):
        if bstack1l1l11lll_opy_.startswith(bstack1ll111_opy_ (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࠬବ")) or bstack1l1l11lll_opy_.startswith(bstack1ll111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠧଭ")):
          self.command_executor._url = bstack1l1l11lll_opy_
        else:
          self.command_executor._url = bstack1ll111_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢମ") + bstack1l1l11lll_opy_ + bstack1ll111_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦଯ")
      else:
        self.command_executor._url = bstack1ll111_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥର") + bstack11l1ll111_opy_ + bstack1ll111_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥ଱")
      logger.debug(bstack1l1ll1l1l1_opy_.format(bstack11l1ll111_opy_))
    else:
      logger.debug(bstack1ll1111l11_opy_.format(bstack1ll111_opy_ (u"ࠥࡓࡵࡺࡩ࡮ࡣ࡯ࠤࡍࡻࡢࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧࠦଲ")))
  except Exception as e:
    logger.debug(bstack1ll1111l11_opy_.format(e))
  if bstack1ll111_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪଳ") in FRAMEWORK_NAME:
    bstack1l1111lll1_opy_(PLATFORM_INDEX, bstack1l1lll11l1_opy_)
  bstack1l11111l_opy_ = self.session_id
  if bstack1ll111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ଴") in FRAMEWORK_NAME or bstack1ll111_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ଵ") in FRAMEWORK_NAME or bstack1ll111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ଶ") in FRAMEWORK_NAME or bstack1ll111_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩଷ") in FRAMEWORK_NAME:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack11ll1ll1l1_opy_ = getattr(threading.current_thread(), bstack1ll111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡖࡨࡷࡹࡓࡥࡵࡣࠪସ"), None)
  if bstack1ll111_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪହ") in FRAMEWORK_NAME or bstack1ll111_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ଺") in FRAMEWORK_NAME:
    TestHubHandler.send_cbt_info(self)
  if bstack1ll111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ଻") in FRAMEWORK_NAME and bstack11ll1ll1l1_opy_ and bstack11ll1ll1l1_opy_.get(bstack1ll111_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ଼࠭"), bstack1ll111_opy_ (u"ࠧࠨଽ")) == bstack1ll111_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩା"):
    TestHubHandler.send_cbt_info(self)
  with bstack11llll1ll_opy_:
    bstack1l111lll11_opy_.append(self)
  if bstack1ll111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬି") in CONFIG and bstack1ll111_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨୀ") in CONFIG[bstack1ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧୁ")][bstack1l1ll1l1l_opy_]:
    SESSION_NAME = CONFIG[bstack1ll111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨୂ")][bstack1l1ll1l1l_opy_][bstack1ll111_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫୃ")]
  logger.debug(bstack11l1l1ll1l_opy_.format(bstack1l11111l_opy_))
  bstack111ll11111_opy_.end(EVENTS.bstack1l1lll111_opy_.value, bstack1l1l1l111_opy_ + bstack1ll111_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢୄ"), bstack1l1l1l111_opy_ + bstack1ll111_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ୅"), status=True, failure=None, test_name=SESSION_NAME)
bstack1111111l_opy_ = None
def set_playwright_globals(**kwargs):
    bstack1ll111_opy_ (u"ࠤࠥࠦࡎࡴࡪࡦࡥࡷࠤ࡬ࡲ࡯ࡣࡣ࡯ࡷࠥ࡬ࡲࡰ࡯ࠣࡣࡤ࡯࡮ࡪࡶࡢࡣ࠳ࡶࡹࠡ࡫ࡱࡸࡴࠦࡴࡩ࡫ࡶࠤࡲࡵࡤࡶ࡮ࡨࠫࡸࠦ࡮ࡢ࡯ࡨࡷࡵࡧࡣࡦ࠰ࠍࠤࠥࠦࠠࡄࡣ࡯ࡰࡪࡪࠠࡣࡻࠣࡣࡤ࡯࡮ࡪࡶࡢࡣ࠳ࡶࡹࠡࡤࡨࡪࡴࡸࡥࠡࡲࡤࡸࡨ࡮࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠬ࠮ࠦࡳࡰࠢࡷ࡬ࡦࡺࠠ࡮ࡱࡧࡣࡱࡧࡵ࡯ࡥ࡫ࠎࠥࠦࠠࠡࡣࡱࡨࠥࡶࡡࡵࡥ࡫ࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡥࡤࡲࠥࡧࡣࡤࡧࡶࡷࠥࡉࡏࡏࡈࡌࡋ࠱ࠦࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࡡࡑࡅࡒࡋࠬࠡࡧࡷࡧ࠳ࠨࠢࠣ୆")
    g = globals()
    for key, value in kwargs.items():
        g[key] = value
ROBOT_PLAYWRIGHT_CDP_URL = None
try:
  try:
    import Browser
    import os
    from subprocess import Popen
    from browserstack_sdk.__init__ import get_turboscale_playwright_url
    def bstack1llll1l111_opy_(self, args, **kwargs):
      global CONFIG
      global SELENIUM_OR_PLAYWRIGHT_INSTALLED
      global ROBOT_PLAYWRIGHT_CDP_URL
      from browserstack_sdk.__init__ import LAUNCH_PATCH_ROBOT_PLAYWRIGHT
      if(bstack1ll111_opy_ (u"ࠥ࡭ࡳࡪࡥࡹ࠰࡭ࡷࠧେ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1ll111_opy_ (u"ࠫࢃ࠭ୈ")), bstack1ll111_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ୉"), bstack1ll111_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨ୊")), bstack1ll111_opy_ (u"ࠧࡸࠩୋ")) as fp:
          fp.write(bstack1ll111_opy_ (u"ࠣࠤୌ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1ll111_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸࡠࡤࡶࡸࡦࡩ࡫࠯࡬ࡶ୍ࠦ")))):
          with open(args[1], bstack1ll111_opy_ (u"ࠪࡶࠬ୎")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1ll111_opy_ (u"ࠫࡦࡹࡹ࡯ࡥࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࡥ࡮ࡦࡹࡓࡥ࡬࡫ࠨࡤࡱࡱࡸࡪࡾࡴ࠭ࠢࡳࡥ࡬࡫ࠠ࠾ࠢࡹࡳ࡮ࡪࠠ࠱ࠫࠪ୏") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1ll11ll1l_opy_)
            if bstack1ll111_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ୐") in CONFIG and str(CONFIG[bstack1ll111_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ୑")]).lower() != bstack1ll111_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭୒"):
                cdpUrl = get_turboscale_playwright_url()
                LAUNCH_PATCH_ROBOT_PLAYWRIGHT = bstack1ll111_opy_ (u"ࠨࠩࠪࠎ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠊࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡰࡢࡶ࡫ࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳࡞࠽ࠍࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠴ࡡࡀࠐࡣࡰࡰࡶࡸࠥࡶ࡟ࡪࡰࡧࡩࡽࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠴ࡠ࠿ࠏࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡹ࡬ࡪࡥࡨࠬ࠵࠲ࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࠬ࠿ࠏࡩ࡯࡯ࡵࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬ࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ࠭ࡀࠐࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴࡬ࡢࡷࡱࡧ࡭ࠦ࠽ࠡࡣࡶࡽࡳࡩࠠࠩ࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁࡻࠋࠢࠣࡰࡪࡺࠠࡤࡣࡳࡷࡀࠐࠠࠡࡶࡵࡽࠥࢁࡻࠋࠢࠣࠤࠥࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࠼ࠌࠣࠤࢂࢃࠠࡤࡣࡷࡧ࡭ࠦࠨࡦࡺࠬࠤࢀࢁࠊࠡࠢࠣࠤࡨࡵ࡮ࡴࡱ࡯ࡩ࠳࡫ࡲࡳࡱࡵࠬࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࡀࠢ࠭ࠢࡨࡼ࠮ࡁࠊࠡࠢࢀࢁࠏࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠨࡼࡽࠍࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥ࠭ࡻࡤࡦࡳ࡙ࡷࡲࡽࠨࠢ࠮ࠤࡪࡴࡣࡰࡦࡨ࡙ࡗࡏࡃࡰ࡯ࡳࡳࡳ࡫࡮ࡵࠪࡍࡗࡔࡔ࠮ࡴࡶࡵ࡭ࡳ࡭ࡩࡧࡻࠫࡧࡦࡶࡳࠪࠫ࠯ࠎࠥࠦࠠࠡ࠰࠱࠲ࡱࡧࡵ࡯ࡥ࡫ࡓࡵࡺࡩࡰࡰࡶࠎࠥࠦࡽࡾࠫ࠾ࠎࢂࢃ࠻ࠋࡥࡲࡲࡸࡺࠠࡰࡴ࡬࡫࡮ࡴࡡ࡭ࡡࡦࡳࡳࡴࡥࡤࡶࠣࡁࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡩ࡯࡯ࡰࡨࡧࡹ࠴ࡢࡪࡰࡧࠬ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠭ࡀࠐࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠠ࠾ࠢࡤࡷࡾࡴࡣࠡࠪࡦࡳࡳࡴࡥࡤࡶࡒࡴࡹ࡯࡯࡯ࡵࠬࠤࡂࡄࠠࡼࡽࠍࠤࠥࡲࡥࡵࠢࡦࡥࡵࡹ࠻ࠋࠢࠣࡸࡷࡿࠠࡼࡽࠍࠤࠥࠦࠠࡤࡣࡳࡷࠥࡃࠠࡋࡕࡒࡒ࠳ࡶࡡࡳࡵࡨࠬࡧࡹࡴࡢࡥ࡮ࡣࡨࡧࡰࡴࠫ࠾ࠎࠥࠦࡽࡾࠢࡦࡥࡹࡩࡨࠡࠪࡨࡼ࠮ࠦࡻࡼࠌࠣࠤࢂࢃࠊࠡࠢࡦࡳࡳࡹࡴࠡ࡯ࡲࡨ࡮࡬ࡩࡦࡦࡈࡲࡩࡶ࡯ࡪࡰࡷࠤࡂࠦࠧࡼࡥࡧࡴ࡚ࡸ࡬ࡾࠩࠣ࠯ࠥ࡫࡮ࡤࡱࡧࡩ࡚ࡘࡉࡄࡱࡰࡴࡴࡴࡥ࡯ࡶࠫࡎࡘࡕࡎ࠯ࡵࡷࡶ࡮ࡴࡧࡪࡨࡼࠬࡨࡧࡰࡴࠫࠬ࠿ࠏࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦ࡯ࡳ࡫ࡪ࡭ࡳࡧ࡬ࡠࡥࡲࡲࡳ࡫ࡣࡵࠪࡾࡿࠏࠦࠠࠡࠢ࠱࠲࠳ࡩ࡯࡯ࡰࡨࡧࡹࡕࡰࡵ࡫ࡲࡲࡸ࠲ࠊࠡࠢࠣࠤࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࠻ࠢࡰࡳࡩ࡯ࡦࡪࡧࡧࡉࡳࡪࡰࡰ࡫ࡱࡸࠏࠦࠠࡾࡿࠬ࠿ࠏࢃࡽ࠼ࠌ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࠏ࠭ࠧࠨ୓").format(cdpUrl=cdpUrl)
            lines.insert(1, LAUNCH_PATCH_ROBOT_PLAYWRIGHT)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1ll111_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸࡠࡤࡶࡸࡦࡩ࡫࠯࡬ࡶࠦ୔")), bstack1ll111_opy_ (u"ࠪࡻࠬ୕")) as bstack1l1llllll_opy_:
              bstack1l1llllll_opy_.writelines(lines)
        CONFIG[bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ୖ")] = str(FRAMEWORK_NAME) + str(__version__)
        bstack111l11lll1_opy_ = os.environ[bstack1ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪୗ")]
        bstack1ll11l1l11_opy_ = TestHubUtils.bstack1111llll11_opy_(CONFIG, FRAMEWORK_NAME)
        CONFIG[bstack1ll111_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ୘")] = bstack111l11lll1_opy_
        CONFIG[bstack1ll111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩ୙")] = bstack1ll11l1l11_opy_
        bstack1l1ll1l1l_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
        try:
          if PARALLELISE_VANILLA_PYTHON is True:
            bstack1l1ll1l1l_opy_ = int(multiprocessing.current_process().name)
          elif PARALLELISE_THREADING_PYTHON is True:
            bstack1l1ll1l1l_opy_ = int(threading.current_thread().name)
        except Exception:
          bstack1l1ll1l1l_opy_ = 0
        CONFIG[bstack1ll111_opy_ (u"ࠣࡷࡶࡩ࡜࠹ࡃࠣ୚")] = False
        CONFIG[bstack1ll111_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ୛")] = True
        bstack11l111llll_opy_ = get_caps(CONFIG, bstack1l1ll1l1l_opy_)
        logger.debug(CONFIG_FILE_CONTENT.format(str(bstack11l111llll_opy_)))
        if CONFIG.get(bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧଡ଼")):
          update_caps_for_local(bstack11l111llll_opy_)
          bstack11l111llll_opy_[bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬଢ଼")] = os.environ[bstack1ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ୞")]
        import urllib.parse
        if bstack1ll111_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪୟ") in CONFIG and str(CONFIG[bstack1ll111_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫୠ")]).lower() != bstack1ll111_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧୡ"):
          ROBOT_PLAYWRIGHT_CDP_URL = get_turboscale_playwright_url() + urllib.parse.quote(json.dumps(bstack11l111llll_opy_))
        else:
          ROBOT_PLAYWRIGHT_CDP_URL = bstack1ll111_opy_ (u"ࠩࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠫୢ") + urllib.parse.quote(json.dumps(bstack11l111llll_opy_))
        os.environ[bstack1ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡓࡇࡕࡔࡠࡒ࡚ࡣࡈࡊࡐࡠࡗࡕࡐࠬୣ")] = ROBOT_PLAYWRIGHT_CDP_URL
        if bstack1ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ୤") in CONFIG and bstack1ll111_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ୥") in CONFIG[bstack1ll111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ୦")][bstack1l1ll1l1l_opy_]:
          SESSION_NAME = CONFIG[bstack1ll111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ୧")][bstack1l1ll1l1l_opy_][bstack1ll111_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭୨")]
        args.append(os.path.join(os.path.expanduser(bstack1ll111_opy_ (u"ࠩࢁࠫ୩")), bstack1ll111_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ୪"), bstack1ll111_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭୫")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack11l111llll_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1ll111_opy_ (u"ࠧ࡯࡮ࡥࡧࡻࡣࡧࡹࡴࡢࡥ࡮࠲࡯ࡹࠢ୬"))
      SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
      return bstack1lllll11l_opy_(self, args, **kwargs)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1llll1ll_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global PLATFORM_INDEX
    global SESSION_NAME
    global PARALLELISE_VANILLA_PYTHON
    global PARALLELISE_THREADING_PYTHON
    global FRAMEWORK_NAME
    CONFIG[bstack1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ୭")] = str(FRAMEWORK_NAME) + str(__version__)
    bstack111l11lll1_opy_ = os.environ[bstack1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ୮")]
    bstack1ll11l1l11_opy_ = TestHubUtils.bstack1111llll11_opy_(CONFIG, FRAMEWORK_NAME)
    CONFIG[bstack1ll111_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ୯")] = bstack111l11lll1_opy_
    CONFIG[bstack1ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ୰")] = bstack1ll11l1l11_opy_
    bstack1l1ll1l1l_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
    try:
      if PARALLELISE_VANILLA_PYTHON is True:
        bstack1l1ll1l1l_opy_ = int(multiprocessing.current_process().name)
      elif PARALLELISE_THREADING_PYTHON is True:
        bstack1l1ll1l1l_opy_ = int(threading.current_thread().name)
    except Exception:
      bstack1l1ll1l1l_opy_ = 0
    CONFIG[bstack1ll111_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤୱ")] = True
    bstack11l111llll_opy_ = get_caps(CONFIG, bstack1l1ll1l1l_opy_)
    bstack11lll1lll_opy_ = bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬ୲") if bstack1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭୳") in bstack11l111llll_opy_ else bstack1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ୴")
    logger.debug(CONFIG_FILE_CONTENT.format(str(bstack11l111llll_opy_)))
    if CONFIG.get(bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ୵")):
      update_caps_for_local(bstack11l111llll_opy_)
    if bstack1ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ୶") in CONFIG and bstack1ll111_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ୷") in CONFIG[bstack1ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭୸")][bstack1l1ll1l1l_opy_]:
      SESSION_NAME = CONFIG[bstack1ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ୹")][bstack1l1ll1l1l_opy_][bstack1ll111_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ୺")]
    import urllib
    import json
    if bstack1ll111_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ୻") in CONFIG and str(CONFIG[bstack1ll111_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ୼")]).lower() != bstack1ll111_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧ୽"):
        bstack1111l11l11_opy_ = get_turboscale_playwright_url()
        cdpUrl = bstack1111l11l11_opy_ + urllib.parse.quote(json.dumps(bstack11l111llll_opy_))
    else:
        cdpUrl = bstack1ll111_opy_ (u"ࠩࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠫ୾") + urllib.parse.quote(json.dumps(bstack11l111llll_opy_))
    try:
        from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
        PlaywrightDriverWrapperDirect.setup_dispatch_capture()
    except Exception as exc:
        logger.debug(bstack1ll111_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࡸࡴࠥࡪࡩࡴࡲࡤࡸࡨ࡮ࠠࡤࡣࡳࡸࡺࡸࡥࠡࡨࡲࡶࠥࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥ࠼ࠣࠩࡸࠨ୿"), exc)
    browser = bstack1111111l_opy_(self, cdpUrl)
    try:
        from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
        wrapper = PlaywrightDriverWrapperDirect(browser, page=None, capabilities=bstack11l111llll_opy_, config=CONFIG)
        threading.current_thread().bstackSessionDriver = wrapper
        threading.current_thread().bstackTestErrorMessages = []
        if wrapper.session_id and not wrapper._cbt_info_sent:
            PlaywrightDriverWrapperDirect._send_cbt_info_on_session()
        try:
            from playwright.sync_api import Browser as bstack1111l11ll_opy_
            if not hasattr(bstack1111l11ll_opy_, bstack1ll111_opy_ (u"ࠫࡤࡨࡳࡵࡣࡦ࡯ࡤࡴࡥࡸࡡࡳࡥ࡬࡫࡟ࡱࡣࡷࡧ࡭࡫ࡤࠨ஀")):
                _111llll1_opy_ = bstack1111l11ll_opy_.new_page
                def _1l1l111lll_opy_(bstack1l11l1l111_opy_, *bstack11l1111lll_opy_, **bstack1llll1111l_opy_):
                    page = _111llll1_opy_(bstack1l11l1l111_opy_, *bstack11l1111lll_opy_, **bstack1llll1111l_opy_)
                    try:
                        _w = getattr(threading.current_thread(), bstack1ll111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ஁"), None)
                        if _w and hasattr(_w, bstack1ll111_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡥࡰࡢࡩࡨࠫஂ")):
                            _w.update_page(page)
                    except Exception as exc:
                        logger.debug(bstack1ll111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡹࡵࡪࡡࡵࡧࠣࡴࡦ࡭ࡥࠡ࡫ࡱࠤࡼࡸࡡࡱࡲࡨࡶ࠿ࠦࠥࡴࠤஃ"), exc)
                    return page
                bstack1111l11ll_opy_.new_page = _1l1l111lll_opy_
                bstack1111l11ll_opy_._bstack_new_page_patched = True
        except Exception as exc:
            logger.debug(bstack1ll111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡴࡤࡪࠣࡗࡾࡴࡣࡃࡴࡲࡻࡸ࡫ࡲ࠯ࡰࡨࡻࡤࡶࡡࡨࡧࠣࡪࡴࡸࠠࡱࡣࡪࡩࠥࡩࡡࡱࡶࡸࡶࡪࡀࠠࠦࡵࠥ஄"), exc)
        try:
            from playwright.sync_api import Page as bstack1l1l1111l_opy_, Browser as _1ll111111_opy_
            if not hasattr(bstack1l1l1111l_opy_, bstack1ll111_opy_ (u"ࠩࡢࡦࡸࡺࡡࡤ࡭ࡢࡴࡦ࡭ࡥࡠࡥ࡯ࡳࡸ࡫࡟ࡱࡣࡷࡧ࡭࡫ࡤࠨஅ")):
                _11ll11ll_opy_ = bstack1l1l1111l_opy_.close
                def _1ll11ll1l1_opy_(bstack1l11l1l11l_opy_, *bstack11lll11ll_opy_, _bstack_sdk_close=False, **bstack1l11l1l1_opy_):
                    if not _bstack_sdk_close:
                        logger.debug(bstack1ll111_opy_ (u"ࠥࡈࡪ࡬ࡥࡳࡴࡨࡨࠥࡶࡡࡨࡧ࠱ࡧࡱࡵࡳࡦࠪࠬࠤ⠙ࠦࡷࡪ࡮࡯ࠤࡨࡲ࡯ࡴࡧࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢஆ"))
                        threading.current_thread().bstack_deferred_page_close = True
                        threading.current_thread().bstack_deferred_page_ref = bstack1l11l1l11l_opy_
                        return
                    return _11ll11ll_opy_(bstack1l11l1l11l_opy_, *bstack11lll11ll_opy_, **bstack1l11l1l1_opy_)
                bstack1l1l1111l_opy_.close = _1ll11ll1l1_opy_
                bstack1l1l1111l_opy_._bstack_page_close_patched = True
            if not hasattr(_1ll111111_opy_, bstack1ll111_opy_ (u"ࠫࡤࡨࡳࡵࡣࡦ࡯ࡤࡨࡲࡰࡹࡶࡩࡷࡥࡣ࡭ࡱࡶࡩࡤࡶࡡࡵࡥ࡫ࡩࡩ࠭இ")):
                _1lll1ll1l1_opy_ = _1ll111111_opy_.close
                def _1lll111111_opy_(bstack1l11l1l111_opy_, *bstack11llll11l1_opy_, _bstack_sdk_close=False, **bstack111l1ll1l_opy_):
                    if not _bstack_sdk_close:
                        logger.debug(bstack1ll111_opy_ (u"ࠧࡊࡥࡧࡧࡵࡶࡪࡪࠠࡣࡴࡲࡻࡸ࡫ࡲ࠯ࡥ࡯ࡳࡸ࡫ࠨࠪࠢ⠗ࠤࡼ࡯࡬࡭ࠢࡦࡰࡴࡹࡥࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧஈ"))
                        threading.current_thread().bstack_deferred_browser_close = True
                        threading.current_thread().bstack_deferred_browser_ref = bstack1l11l1l111_opy_
                        return
                    return _1lll1ll1l1_opy_(bstack1l11l1l111_opy_, *bstack11llll11l1_opy_, **bstack111l1ll1l_opy_)
                _1ll111111_opy_.close = _1lll111111_opy_
                _1ll111111_opy_._bstack_browser_close_patched = True
            if not hasattr(bstack1l1l1111l_opy_, bstack1ll111_opy_ (u"࠭࡟ࡣࡵࡷࡥࡨࡱ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡣࡵࡧࡴࡤࡪࡨࡨࠬஉ")):
                _1llll11l11_opy_ = bstack1l1l1111l_opy_.screenshot
                def _111ll111l_opy_(bstack1l11l1l11l_opy_, *bstack1l1lll1l1l_opy_, **bstack11ll11lll_opy_):
                    result = _1llll11l11_opy_(bstack1l11l1l11l_opy_, *bstack1l1lll1l1l_opy_, **bstack11ll11lll_opy_)
                    try:
                        from bstack_utils.testhub_handler import TestHubHandler
                        from bstack_utils.bstack11l1llll_opy_ import bstack11l1ll1111_opy_
                        if bstack11l1ll1111_opy_.on():
                            import base64
                            if isinstance(result, bytes):
                                bstack1l1ll11ll1_opy_ = base64.b64encode(result).decode(bstack1ll111_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ஊ"))
                            else:
                                bstack1l1ll11ll1_opy_ = str(result)
                            test_uuid = TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack11l1ll1111_opy_.current_hook_uuid()
                            if test_uuid and bstack1l1ll11ll1_opy_:
                                TestHubHandler.bstack11ll11111l_opy_({
                                    bstack1ll111_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧ஋"): bstack1l1ll11ll1_opy_,
                                    bstack1ll111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ஌"): test_uuid
                                })
                                logger.debug(bstack1ll111_opy_ (u"ࠥࡗࡪࡴࡴࠡࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠢࡷࡳࠥࡕ࠱࠲ࡻࠣࡪࡴࡸࠠࡵࡧࡶࡸࠥࢁࡽࠣ஍").format(test_uuid))
                    except Exception as bstack1llllll11l_opy_:
                        logger.debug(bstack1ll111_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡱࡨࠥࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠦࡴࡰࠢࡒ࠵࠶ࡿ࠺ࠡࡽࢀࠦஎ").format(str(bstack1llllll11l_opy_)))
                    return result
                bstack1l1l1111l_opy_.screenshot = _111ll111l_opy_
                bstack1l1l1111l_opy_._bstack_screenshot_patched = True
        except Exception as exc:
            logger.debug(bstack1ll111_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡨࠤࡩ࡫ࡦࡦࡴࡵࡩࡩࠦࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡧࡱࡵࡳࡦࠢ࡫ࡳࡴࡱࡳ࠻ࠢࠨࡷࠧஏ"), exc)
        logger.debug(bstack1ll111_opy_ (u"ࠨࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡇࡶ࡮ࡼࡥࡳ࡙ࡵࡥࡵࡶࡥࡳࡆ࡬ࡶࡪࡩࡴࠡࡵࡨࡸࡺࡶࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࠢࡩࡳࡷࠦࡴࡩࡴࡨࡥࡩࠦࡻࡾࠤஐ").format(threading.get_ident()))
    except Exception as e:
        logger.debug(bstack1ll111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡷࡳࡣࡳࡴࡪࡸ࠺ࠡࡽࢀࠦ஑").format(str(e)))
    return browser
  async def bstack111llll11l_opy_(self, *args, **kwargs):
    global bstack1111111l_opy_, CONFIG, FRAMEWORK_NAME, __version__, BROWSERSTACK_AUTOMATION
    global PLATFORM_INDEX, PARALLELISE_VANILLA_PYTHON, PARALLELISE_THREADING_PYTHON, SESSION_NAME
    import urllib.parse as _11ll1l1l1l_opy_
    import json
    ws_endpoint = args[0] if args else kwargs.get(bstack1ll111_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬஒ"), kwargs.get(bstack1ll111_opy_ (u"ࠩࡺࡷࡤ࡫࡮ࡥࡲࡲ࡭ࡳࡺࠧஓ"), bstack1ll111_opy_ (u"ࠪࠫஔ")))
    bstack111l1l111_opy_ = (ws_endpoint
                 and bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧக") in str(ws_endpoint)
                 and bstack1ll111_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫ஖") in str(ws_endpoint))
    bstack111111l11_opy_ = {}
    if bstack111l1l111_opy_:
        from bstack_utils.helper import bstack1lll111l1_opy_
        bstack1l1l1111l1_opy_ = bstack1lll111l1_opy_()
        try:
            if bstack1l1l1111l1_opy_:
                CONFIG[bstack1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ஗")] = str(FRAMEWORK_NAME) + str(__version__)
                bstack111l11lll1_opy_ = os.environ.get(bstack1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ஘"), bstack1ll111_opy_ (u"ࠨࠩங"))
                if bstack111l11lll1_opy_:
                    CONFIG[bstack1ll111_opy_ (u"ࠩࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬச")] = bstack111l11lll1_opy_
                CONFIG[bstack1ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬ஛")] = TestHubUtils.bstack1111llll11_opy_(CONFIG, FRAMEWORK_NAME)
                bstack1l1ll1l1l_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
                try:
                    if PARALLELISE_VANILLA_PYTHON is True:
                        bstack1l1ll1l1l_opy_ = int(multiprocessing.current_process().name)
                    elif PARALLELISE_THREADING_PYTHON is True:
                        bstack1l1ll1l1l_opy_ = int(threading.current_thread().name)
                except Exception:
                    bstack1l1ll1l1l_opy_ = 0
                CONFIG[bstack1ll111_opy_ (u"ࠦ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥஜ")] = True
                bstack111111l11_opy_ = get_caps(CONFIG, bstack1l1ll1l1l_opy_)
                if CONFIG.get(bstack1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ஝")):
                    update_caps_for_local(bstack111111l11_opy_)
                if bstack1ll111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩஞ") in CONFIG and bstack1ll111_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬட") in CONFIG[bstack1ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ஠")][bstack1l1ll1l1l_opy_]:
                    SESSION_NAME = CONFIG[bstack1ll111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ஡")][bstack1l1ll1l1l_opy_][bstack1ll111_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ஢")]
                logger.debug(bstack1ll111_opy_ (u"ࠦࡈࡧࡳࡦࠢࡄ࠾ࠥࡘࡥࡱ࡮ࡤࡧࡪࡪࠠࡶࡵࡨࡶࠥࡩࡡࡱࡵࠣࡻ࡮ࡺࡨࠡࡻࡰࡰࠥࡩࡡࡱࡵ࠽ࠤࢀࢃࠢண").format(str(bstack111111l11_opy_)))
            else:
                bstack11ll11l1l1_opy_ = str(ws_endpoint).split(bstack1ll111_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫத"))[1]
                bstack111111l11_opy_ = json.loads(_11ll1l1l1l_opy_.unquote(bstack11ll11l1l1_opy_))
                bstack111111l11_opy_ = bstack111111l11_opy_ or {}
                bstack111l11lll1_opy_ = os.environ.get(bstack1ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ஥"), bstack1ll111_opy_ (u"ࠧࠨ஦"))
                bstack1ll11l1l11_opy_ = TestHubUtils.bstack1111llll11_opy_(CONFIG, FRAMEWORK_NAME)
                bstack111111l11_opy_[bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ஧")] = str(FRAMEWORK_NAME) + str(__version__)
                bstack111111l11_opy_[bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪந")] = BROWSERSTACK_AUTOMATION
                if bstack111l11lll1_opy_:
                    bstack111111l11_opy_[bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬன")] = bstack111l11lll1_opy_
                bstack111111l11_opy_[bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬப")] = bstack1ll11l1l11_opy_
                logger.debug(bstack1ll111_opy_ (u"ࠧࡉࡡࡴࡧࠣࡈ࠿ࠦࡍࡦࡴࡪࡩࡩࠦࡓࡅࡍࠣࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࠦࡩ࡯ࡶࡲࠤࡺࡹࡥࡳࠢࡦࡥࡵࡹࠢ஫"))
            ws_url = str(ws_endpoint).split(bstack1ll111_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬ஬"))[0]
            ws_endpoint = ws_url + bstack1ll111_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭஭") + _11ll1l1l1l_opy_.quote(json.dumps(bstack111111l11_opy_))
            if args:
                args = (ws_endpoint,) + args[1:]
            else:
                if bstack1ll111_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬம") in kwargs:
                    kwargs[bstack1ll111_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭ய")] = ws_endpoint
                else:
                    kwargs[bstack1ll111_opy_ (u"ࠪࡻࡸࡥࡥ࡯ࡦࡳࡳ࡮ࡴࡴࠨர")] = ws_endpoint
            logger.debug(bstack1ll111_opy_ (u"ࠦࡑ࡫ࡧࡢࡥࡼࠤࡨࡵ࡮࡯ࡧࡦࡸ࡛ࠥࡒࡍࠢࡸࡴࡩࡧࡴࡦࡦࠣࡻ࡮ࡺࡨࠡࡽࢀࠤࡨࡧࡰࡴࠤற").format(bstack1ll111_opy_ (u"ࠧࡿ࡭࡭ࠤல") if bstack1l1l1111l1_opy_ else bstack1ll111_opy_ (u"ࠨࡴࡦ࡮ࡨࡱࡪࡺࡲࡺࠤள")))
        except Exception as e:
            logger.debug(bstack1ll111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡪࡸࡧࡦࠢࡦࡥࡵࡹࠠࡪࡰࡷࡳࠥࡩ࡯࡯ࡰࡨࡧࡹࠦࡕࡓࡎ࠽ࠤࢀࢃࠢழ").format(str(e)))
        try:
            from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
            PlaywrightDriverWrapperDirect.setup_dispatch_capture()
        except Exception as exc:
            logger.debug(bstack1ll111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࡶࡲࠣࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠥࡩࡡࡱࡶࡸࡶࡪࠦࡩ࡯ࠢࡰࡳࡩࡥࡣࡰࡰࡱࡩࡨࡺ࠺ࠡࠧࡶࠦவ"), exc)
    browser = await bstack1111111l_opy_(self, *args, **kwargs)
    if bstack111l1l111_opy_:
        try:
            from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
            wrapper = PlaywrightDriverWrapperDirect(browser, page=None, capabilities=bstack111111l11_opy_, config=CONFIG)
            threading.current_thread().bstackSessionDriver = wrapper
            threading.current_thread().bstackTestErrorMessages = []
            if wrapper.session_id and not wrapper._cbt_info_sent:
                PlaywrightDriverWrapperDirect._send_cbt_info_on_session()
            try:
                from playwright.sync_api import Browser as bstack1111l11ll_opy_
                if not hasattr(bstack1111l11ll_opy_, bstack1ll111_opy_ (u"ࠩࡢࡦࡸࡺࡡࡤ࡭ࡢࡲࡪࡽ࡟ࡱࡣࡪࡩࡤࡶࡡࡵࡥ࡫ࡩࡩ࠭ஶ")):
                    _111llll1_opy_ = bstack1111l11ll_opy_.new_page
                    def _1l1l111lll_opy_(bstack1l11l1l111_opy_, *bstack11l1111lll_opy_, **bstack1llll1111l_opy_):
                        page = _111llll1_opy_(bstack1l11l1l111_opy_, *bstack11l1111lll_opy_, **bstack1llll1111l_opy_)
                        try:
                            _w = getattr(threading.current_thread(), bstack1ll111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩஷ"), None)
                            if _w and hasattr(_w, bstack1ll111_opy_ (u"ࠫࡺࡶࡤࡢࡶࡨࡣࡵࡧࡧࡦࠩஸ")):
                                _w.update_page(page)
                        except Exception as exc:
                            logger.debug(bstack1ll111_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡷࡳࡨࡦࡺࡥࠡࡲࡤ࡫ࡪࠦࡩ࡯ࠢࡺࡶࡦࡶࡰࡦࡴࠣࠬࡲࡵࡤࡠࡥࡲࡲࡳ࡫ࡣࡵࠫ࠽ࠤࠪࡹࠢஹ"), exc)
                        return page
                    bstack1111l11ll_opy_.new_page = _1l1l111lll_opy_
                    bstack1111l11ll_opy_._bstack_new_page_patched = True
            except Exception as exc:
                logger.debug(bstack1ll111_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡹࡩࡨࠡࡕࡼࡲࡨࡈࡲࡰࡹࡶࡩࡷ࠴࡮ࡦࡹࡢࡴࡦ࡭ࡥࠡ࡫ࡱࠤࡲࡵࡤࡠࡥࡲࡲࡳ࡫ࡣࡵ࠼ࠣࠩࡸࠨ஺"), exc)
            try:
                from playwright.sync_api import Page as bstack1l1l1111l_opy_, Browser as _1ll111111_opy_
                if not hasattr(bstack1l1l1111l_opy_, bstack1ll111_opy_ (u"ࠧࡠࡤࡶࡸࡦࡩ࡫ࡠࡲࡤ࡫ࡪࡥࡣ࡭ࡱࡶࡩࡤࡶࡡࡵࡥ࡫ࡩࡩ࠭஻")):
                    _11ll11ll_opy_ = bstack1l1l1111l_opy_.close
                    def _1ll11ll1l1_opy_(bstack1l11l1l11l_opy_, *bstack11lll11ll_opy_, _bstack_sdk_close=False, **bstack1l11l1l1_opy_):
                        if not _bstack_sdk_close:
                            logger.debug(bstack1ll111_opy_ (u"ࠣࡆࡨࡪࡪࡸࡲࡦࡦࠣࡴࡦ࡭ࡥ࠯ࡥ࡯ࡳࡸ࡫ࠨࠪࠢ⠗ࠤࡼ࡯࡬࡭ࠢࡦࡰࡴࡹࡥࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧ஼"))
                            threading.current_thread().bstack_deferred_page_close = True
                            threading.current_thread().bstack_deferred_page_ref = bstack1l11l1l11l_opy_
                            return
                        return _11ll11ll_opy_(bstack1l11l1l11l_opy_, *bstack11lll11ll_opy_, **bstack1l11l1l1_opy_)
                    bstack1l1l1111l_opy_.close = _1ll11ll1l1_opy_
                    bstack1l1l1111l_opy_._bstack_page_close_patched = True
                if not hasattr(_1ll111111_opy_, bstack1ll111_opy_ (u"ࠩࡢࡦࡸࡺࡡࡤ࡭ࡢࡦࡷࡵࡷࡴࡧࡵࡣࡨࡲ࡯ࡴࡧࡢࡴࡦࡺࡣࡩࡧࡧࠫ஽")):
                    _1lll1ll1l1_opy_ = _1ll111111_opy_.close
                    def _1lll111111_opy_(bstack1l11l1l111_opy_, *bstack11llll11l1_opy_, _bstack_sdk_close=False, **bstack111l1ll1l_opy_):
                        if not _bstack_sdk_close:
                            logger.debug(bstack1ll111_opy_ (u"ࠥࡈࡪ࡬ࡥࡳࡴࡨࡨࠥࡨࡲࡰࡹࡶࡩࡷ࠴ࡣ࡭ࡱࡶࡩ࠭࠯ࠠ⠕ࠢࡺ࡭ࡱࡲࠠࡤ࡮ࡲࡷࡪࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥா"))
                            threading.current_thread().bstack_deferred_browser_close = True
                            threading.current_thread().bstack_deferred_browser_ref = bstack1l11l1l111_opy_
                            return
                        return _1lll1ll1l1_opy_(bstack1l11l1l111_opy_, *bstack11llll11l1_opy_, **bstack111l1ll1l_opy_)
                    _1ll111111_opy_.close = _1lll111111_opy_
                    _1ll111111_opy_._bstack_browser_close_patched = True
                if not hasattr(bstack1l1l1111l_opy_, bstack1ll111_opy_ (u"ࠫࡤࡨࡳࡵࡣࡦ࡯ࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡡࡳࡥࡹࡩࡨࡦࡦࠪி")):
                    _1llll11l11_opy_ = bstack1l1l1111l_opy_.screenshot
                    def _111ll111l_opy_(bstack1l11l1l11l_opy_, *bstack1l1lll1l1l_opy_, **bstack11ll11lll_opy_):
                        result = _1llll11l11_opy_(bstack1l11l1l11l_opy_, *bstack1l1lll1l1l_opy_, **bstack11ll11lll_opy_)
                        try:
                            from bstack_utils.testhub_handler import TestHubHandler
                            from bstack_utils.bstack11l1llll_opy_ import bstack11l1ll1111_opy_
                            if bstack11l1ll1111_opy_.on():
                                import base64
                                if isinstance(result, bytes):
                                    bstack1l1ll11ll1_opy_ = base64.b64encode(result).decode(bstack1ll111_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫீ"))
                                else:
                                    bstack1l1ll11ll1_opy_ = str(result)
                                test_uuid = TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack11l1ll1111_opy_.current_hook_uuid()
                                if test_uuid and bstack1l1ll11ll1_opy_:
                                    TestHubHandler.bstack11ll11111l_opy_({
                                        bstack1ll111_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬு"): bstack1l1ll11ll1_opy_,
                                        bstack1ll111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧூ"): test_uuid
                                    })
                        except Exception as bstack1llllll11l_opy_:
                            logger.debug(bstack1ll111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫࡮ࡥࠢࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠣࡸࡴࠦࡏ࠲࠳ࡼࠤ࠭ࡳ࡯ࡥࡡࡦࡳࡳࡴࡥࡤࡶࠬ࠾ࠥࠫࡳࠣ௃"), bstack1llllll11l_opy_)
                        return result
                    bstack1l1l1111l_opy_.screenshot = _111ll111l_opy_
                    bstack1l1l1111l_opy_._bstack_screenshot_patched = True
            except Exception as exc:
                logger.debug(bstack1ll111_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡥࠡࡦࡨࡪࡪࡸࡲࡦࡦࠣࡧࡱࡵࡳࡦࠢ࡫ࡳࡴࡱࡳࠡ࡫ࡱࠤࡲࡵࡤࡠࡥࡲࡲࡳ࡫ࡣࡵ࠼ࠣࠩࡸࠨ௄"), exc)
            logger.debug(bstack1ll111_opy_ (u"ࠥࡐࡪ࡭ࡡࡤࡻࠣࡧࡴࡴ࡮ࡦࡥࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡺࡲࡢࡥ࡮࡭ࡳ࡭ࠠࡴࡧࡷࡹࡵࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࠡࡨࡲࡶࠥࡺࡨࡳࡧࡤࡨࠥࢁࡽࠣ௅").format(threading.get_ident()))
        except Exception as e:
            logger.debug(bstack1ll111_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦ࡬ࡦࡩࡤࡧࡾࠦࡣࡰࡰࡱࡩࡨࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡶࡵࡥࡨࡱࡩ࡯ࡩ࠽ࠤࢀࢃࠢெ").format(str(e)))
    return browser
except Exception as e:
    pass
def patch_playwright():
    global SELENIUM_OR_PLAYWRIGHT_INSTALLED
    global FRAMEWORK_NAME
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1lll111l1_opy_
        global bstack1111111l_opy_
        if not bstack1111111l_opy_:
            bstack1111111l_opy_ = BrowserType.connect
        BrowserType.connect = bstack111llll11l_opy_
        if bstack1lll111l1_opy_():
            BrowserType.launch = bstack1llll1ll_opy_
            SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
        try:
            from playwright.sync_api._context_manager import PlaywrightContextManager
            if not hasattr(PlaywrightContextManager, bstack1ll111_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥࡥ࡯ࡶࡨࡶࡤࡶࡡࡵࡥ࡫ࡩࡩ࠭ே")):
                _1l11l1ll1_opy_ = PlaywrightContextManager.__enter__
                def _111lllll11_opy_(bstack11l11111_opy_):
                    pw = _1l11l1ll1_opy_(bstack11l11111_opy_)
                    _1l1ll1ll1l_opy_ = pw.stop
                    _111l1111l1_opy_ = threading.current_thread()
                    _111l1111l1_opy_.bstack_deferred_pw_ref = pw
                    _111l1111l1_opy_.bstack_deferred_pw_stop_fn = _1l1ll1ll1l_opy_
                    def _11lllll11_opy_(*args, _bstack_sdk_close=False, **kwargs):
                        if not _bstack_sdk_close:
                            logger.debug(bstack1ll111_opy_ (u"ࠨࡄࡦࡨࡨࡶࡷ࡫ࡤࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠳ࡹࡴࡰࡲࠫ࠭ࠥ⠚ࠠࡸ࡫࡯ࡰࠥࡹࡴࡰࡲࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢை"))
                            threading.current_thread().bstack_deferred_pw_stop = True
                            return
                        return _1l1ll1ll1l_opy_()
                    pw.stop = _11lllll11_opy_
                    return pw
                PlaywrightContextManager.__enter__ = _111lllll11_opy_
                PlaywrightContextManager._bstack_enter_patched = True
        except Exception as e:
            logger.debug(bstack1ll111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡺࡣࡩࠢࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡉ࡯࡯ࡶࡨࡼࡹࡓࡡ࡯ࡣࡪࡩࡷ࠴࡟ࡠࡧࡱࡸࡪࡸ࡟ࡠ࠼ࠣࠩࡸࠨ௉"), e)
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1llll1l111_opy_
      SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
    except Exception as e:
      pass
def playwright_set_session_name(context, bstack11l1l11ll1_opy_):
  try:
    if getattr(context, bstack1ll111_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭ொ"), None):
      context.page.evaluate(bstack1ll111_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥோ"), bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠧௌ")+ json.dumps(bstack11l1l11ll1_opy_) + bstack1ll111_opy_ (u"ࠦࢂࢃ்ࠢ"))
  except Exception as e:
    logger.debug(bstack1ll111_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡼࡿ࠽ࠤࢀࢃࠢ௎").format(str(e), traceback.format_exc()))
def playwright_annotate(context, message, level):
  try:
    if getattr(context, bstack1ll111_opy_ (u"࠭ࡰࡢࡩࡨࠫ௏"), None):
      context.page.evaluate(bstack1ll111_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣௐ"), bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭௑") + json.dumps(message) + bstack1ll111_opy_ (u"ࠩ࠯ࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠬ௒") + json.dumps(level) + bstack1ll111_opy_ (u"ࠪࢁࢂ࠭௓"))
  except Exception as e:
    logger.debug(bstack1ll111_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡢࡰࡱࡳࡹࡧࡴࡪࡱࡱࠤࢀࢃ࠺ࠡࡽࢀࠦ௔").format(str(e), traceback.format_exc()))
@measure(event_name=EVENTS.bstack1l1lll1l1_opy_, stage=STAGE.bstack11ll1111_opy_, bstack11l11l111_opy_=SESSION_NAME)
def bstack1111ll11l1_opy_(self, url):
  global bstack11l1ll11l_opy_
  try:
    bstack1l11l1llll_opy_(url)
  except Exception as err:
    logger.debug(bstack1ll1111111_opy_.format(str(err)))
  try:
    bstack11l1ll11l_opy_(self, url)
  except Exception as e:
    try:
      parsed_error = str(e)
      if any(err_msg in parsed_error for err_msg in bstack1l11l1lll_opy_):
        bstack1l11l1llll_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1ll1111111_opy_.format(str(err)))
    raise e
def bstack1lll11llll_opy_(self):
  global bstack11lll1l11_opy_
  bstack11lll1l11_opy_ = self
  return
def bstack111l11l1_opy_(self):
  global bstack1l1ll111_opy_
  bstack1l1ll111_opy_ = self
  return
def bstack1111l1l11_opy_(test_name, bstack11111111l_opy_):
  global CONFIG
  if percy.bstack1ll1l1l1l_opy_() == bstack1ll111_opy_ (u"ࠧࡺࡲࡶࡧࠥ௕"):
    bstack11111llll_opy_ = os.path.relpath(bstack11111111l_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack11111llll_opy_)
    bstack11l11l111_opy_ = suite_name + bstack1ll111_opy_ (u"ࠨ࠭ࠣ௖") + test_name
    threading.current_thread().percySessionName = bstack11l11l111_opy_
def bstack1lllll111_opy_(self, test, *args, **kwargs):
  global bstack1111lll11_opy_
  test_name = None
  bstack11111111l_opy_ = None
  if test:
    test_name = str(test.name)
    bstack11111111l_opy_ = str(test.source)
  bstack1111l1l11_opy_(test_name, bstack11111111l_opy_)
  bstack1111lll11_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.bstack1lllll11l1_opy_, stage=STAGE.bstack11ll1111_opy_, bstack11l11l111_opy_=SESSION_NAME)
def bstack11l1ll1l1_opy_(driver, bstack11l11l111_opy_):
  if not bstack11111l111_opy_ and bstack11l11l111_opy_:
      bstack11lll1111l_opy_ = {
          bstack1ll111_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧௗ"): bstack1ll111_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ௘"),
          bstack1ll111_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ௙"): {
              bstack1ll111_opy_ (u"ࠪࡲࡦࡳࡥࠨ௚"): bstack11l11l111_opy_
          }
      }
      bstack111l111l11_opy_ = bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩ௛").format(json.dumps(bstack11lll1111l_opy_))
      driver.execute_script(bstack111l111l11_opy_)
  if bstack1lll1lll1l_opy_:
      bstack1l111l11ll_opy_ = {
          bstack1ll111_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬ௜"): bstack1ll111_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨ௝"),
          bstack1ll111_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ௞"): {
              bstack1ll111_opy_ (u"ࠨࡦࡤࡸࡦ࠭௟"): bstack11l11l111_opy_ + bstack1ll111_opy_ (u"ࠩࠣࡴࡦࡹࡳࡦࡦࠤࠫ௠"),
              bstack1ll111_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ௡"): bstack1ll111_opy_ (u"ࠫ࡮ࡴࡦࡰࠩ௢")
          }
      }
      if bstack1lll1lll1l_opy_.status == bstack1ll111_opy_ (u"ࠬࡖࡁࡔࡕࠪ௣"):
          bstack1111ll1111_opy_ = bstack1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫ௤").format(json.dumps(bstack1l111l11ll_opy_))
          driver.execute_script(bstack1111ll1111_opy_)
          bstack111lll11_opy_(driver, bstack1ll111_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ௥"))
      elif bstack1lll1lll1l_opy_.status == bstack1ll111_opy_ (u"ࠨࡈࡄࡍࡑ࠭௦"):
          reason = bstack1ll111_opy_ (u"ࠤࠥ௧")
          bstack1111l1lll_opy_ = bstack11l11l111_opy_ + bstack1ll111_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠫ௨")
          if bstack1lll1lll1l_opy_.message:
              reason = str(bstack1lll1lll1l_opy_.message)
              bstack1111l1lll_opy_ = bstack1111l1lll_opy_ + bstack1ll111_opy_ (u"ࠫࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠫ௩") + reason
          bstack1l111l11ll_opy_[bstack1ll111_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ௪")] = {
              bstack1ll111_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ௫"): bstack1ll111_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭௬"),
              bstack1ll111_opy_ (u"ࠨࡦࡤࡸࡦ࠭௭"): bstack1111l1lll_opy_
          }
          bstack1111ll1111_opy_ = bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧ௮").format(json.dumps(bstack1l111l11ll_opy_))
          driver.execute_script(bstack1111ll1111_opy_)
          bstack111lll11_opy_(driver, bstack1ll111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ௯"), reason)
          bstack11111lll_opy_(reason, str(bstack1lll1lll1l_opy_), str(PLATFORM_INDEX), logger)
@measure(event_name=EVENTS.bstack1l11l111l1_opy_, stage=STAGE.bstack11ll1111_opy_, bstack11l11l111_opy_=SESSION_NAME)
def bstack1l1l1ll1_opy_(driver, test):
  if percy.bstack1ll1l1l1l_opy_() == bstack1ll111_opy_ (u"ࠦࡹࡸࡵࡦࠤ௰") and percy.bstack1ll11l111l_opy_() == bstack1ll111_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢ௱"):
      bstack11l11ll1ll_opy_ = bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"࠭ࡰࡦࡴࡦࡽࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ௲"), None)
      bstack1l1ll1111_opy_(driver, bstack11l11ll1ll_opy_, test)
  if (bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ௳"), None) and
      bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ௴"), None)) or (
      bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ௵"), None) and
      bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ௶"), None)):
      logger.info(bstack1ll111_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠢࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡮ࡹࠠࡶࡰࡧࡩࡷࡽࡡࡺ࠰ࠣࠦ௷"))
      bstack1ll11lll11_opy_.bstack11lll1lll1_opy_(driver, name=test.name, path=test.source)
def bstack111l1l111l_opy_(test, bstack11l11l111_opy_):
    try:
      bstack1ll1l1l111_opy_ = datetime.datetime.now()
      data = {}
      if test:
        data[bstack1ll111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ௸")] = bstack11l11l111_opy_
      if bstack1lll1lll1l_opy_:
        if bstack1lll1lll1l_opy_.status == bstack1ll111_opy_ (u"࠭ࡐࡂࡕࡖࠫ௹"):
          data[bstack1ll111_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ௺")] = bstack1ll111_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ௻")
        elif bstack1lll1lll1l_opy_.status == bstack1ll111_opy_ (u"ࠩࡉࡅࡎࡒࠧ௼"):
          data[bstack1ll111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ௽")] = bstack1ll111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ௾")
          if bstack1lll1lll1l_opy_.message:
            data[bstack1ll111_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ௿")] = str(bstack1lll1lll1l_opy_.message)
      user = CONFIG[bstack1ll111_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨఀ")]
      key = CONFIG[bstack1ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪఁ")]
      host = bstack1l1ll11lll_opy_(cli.config, [bstack1ll111_opy_ (u"ࠣࡣࡳ࡭ࡸࠨం"), bstack1ll111_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨࠦః"), bstack1ll111_opy_ (u"ࠥࡥࡵ࡯ࠢఄ")], bstack1ll111_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠧఅ"))
      url = bstack1ll111_opy_ (u"ࠬࢁࡽ࠰ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡷࡪࡹࡳࡪࡱࡱࡷ࠴ࢁࡽ࠯࡬ࡶࡳࡳ࠭ఆ").format(host, bstack1l11111l_opy_)
      headers = {
        bstack1ll111_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡵࡻࡳࡩࠬఇ"): bstack1ll111_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪఈ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers, auth=(user, key))
        cli.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠣࡪࡷࡸࡵࡀࡵࡱࡦࡤࡸࡪࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡹࡴࡢࡶࡸࡷࠧఉ"), datetime.datetime.now() - bstack1ll1l1l111_opy_)
    except Exception as e:
      logger.error(bstack111ll1l11_opy_.format(str(e)))
def bstack1l1ll111l1_opy_(test, bstack11l11l111_opy_):
  global CONFIG
  global bstack1l1ll111_opy_
  global bstack11lll1l11_opy_
  global bstack1l11111l_opy_
  global bstack1lll1lll1l_opy_
  global SESSION_NAME
  global bstack1l111llll_opy_
  global bstack1l1l1l1ll_opy_
  global bstack1111111l1_opy_
  global bstack1l11l111_opy_
  global bstack1l111lll11_opy_
  global bstack1111111ll_opy_
  global bstack1111lll11l_opy_
  try:
    if not bstack1l11111l_opy_:
      with bstack1111lll11l_opy_:
        bstack1111llllll_opy_ = os.path.join(os.path.expanduser(bstack1ll111_opy_ (u"ࠩࢁࠫఊ")), bstack1ll111_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪఋ"), bstack1ll111_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭ఌ"))
        if os.path.exists(bstack1111llllll_opy_):
          with open(bstack1111llllll_opy_, bstack1ll111_opy_ (u"ࠬࡸࠧ఍")) as f:
            content = f.read().strip()
            if content:
              bstack1lll1ll1_opy_ = json.loads(bstack1ll111_opy_ (u"ࠨࡻࠣఎ") + content + bstack1ll111_opy_ (u"ࠧࠣࡺࠥ࠾ࠥࠨࡹࠣࠩఏ") + bstack1ll111_opy_ (u"ࠣࡿࠥఐ"))
              bstack1l11111l_opy_ = bstack1lll1ll1_opy_.get(str(threading.get_ident()))
  except Exception as e:
    logger.debug(bstack1ll111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡴࡨࡥࡩ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡍࡉࡹࠠࡧ࡫࡯ࡩ࠿ࠦࠧ఑") + str(e))
  if not is_robot_playwright_installed():
    if bstack1l111lll11_opy_:
      with bstack11llll1ll_opy_:
        bstack1ll1l1l1_opy_ = bstack1l111lll11_opy_.copy()
      for driver in bstack1ll1l1l1_opy_:
        if bstack1l11111l_opy_ == driver.session_id:
          if test:
            bstack1l1l1ll1_opy_(driver, test)
          bstack11l1ll1l1_opy_(driver, bstack11l11l111_opy_)
    elif bstack1l11111l_opy_:
      bstack111l1l111l_opy_(test, bstack11l11l111_opy_)
    if bstack1l1ll111_opy_:
      bstack1l1l1l1ll_opy_(bstack1l1ll111_opy_)
    if bstack11lll1l11_opy_:
      bstack1111111l1_opy_(bstack11lll1l11_opy_)
    if bstack1llllll1l_opy_:
      bstack1l11l111_opy_()
def bstack1ll11llll_opy_(self, test, *args, **kwargs):
  bstack11l11l111_opy_ = None
  if test:
    bstack11l11l111_opy_ = str(test.name)
  bstack1l1ll111l1_opy_(test, bstack11l11l111_opy_)
  bstack1l111llll_opy_(self, test, *args, **kwargs)
def bstack111l1l11ll_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1llll111l1_opy_
  global CONFIG
  global bstack1l111lll11_opy_
  global bstack1l11111l_opy_
  global bstack1111lll11l_opy_
  bstack11l11l11_opy_ = None
  try:
    if bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩఒ"), None) or bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ఓ"), None):
      try:
        if not bstack1l11111l_opy_:
          bstack1111llllll_opy_ = os.path.join(os.path.expanduser(bstack1ll111_opy_ (u"ࠬࢄࠧఔ")), bstack1ll111_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭క"), bstack1ll111_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩఖ"))
          with bstack1111lll11l_opy_:
            if os.path.exists(bstack1111llllll_opy_):
              with open(bstack1111llllll_opy_, bstack1ll111_opy_ (u"ࠨࡴࠪగ")) as f:
                content = f.read().strip()
                if content:
                  bstack1lll1ll1_opy_ = json.loads(bstack1ll111_opy_ (u"ࠤࡾࠦఘ") + content + bstack1ll111_opy_ (u"ࠪࠦࡽࠨ࠺ࠡࠤࡼࠦࠬఙ") + bstack1ll111_opy_ (u"ࠦࢂࠨచ"))
                  bstack1l11111l_opy_ = bstack1lll1ll1_opy_.get(str(threading.get_ident()))
      except Exception as e:
        logger.debug(bstack1ll111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡷ࡫ࡡࡥ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡉࡅࡵࠣࡪ࡮ࡲࡥࠡ࡫ࡱࠤࡹ࡫ࡳࡵࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࠫఛ") + str(e))
      if bstack1l111lll11_opy_:
        with bstack11llll1ll_opy_:
          bstack1ll1l1l1_opy_ = bstack1l111lll11_opy_.copy()
        for driver in bstack1ll1l1l1_opy_:
          if bstack1l11111l_opy_ == driver.session_id:
            bstack11l11l11_opy_ = driver
    bstack111lll1lll_opy_ = bstack1ll11lll11_opy_.bstack11l1llll11_opy_(test.tags)
    if bstack11l11l11_opy_:
      threading.current_thread().isA11yTest = bstack1ll11lll11_opy_.bstack11ll1l1l_opy_(bstack11l11l11_opy_, bstack111lll1lll_opy_)
      threading.current_thread().isAppA11yTest = bstack1ll11lll11_opy_.bstack11ll1l1l_opy_(bstack11l11l11_opy_, bstack111lll1lll_opy_)
    else:
      threading.current_thread().isA11yTest = bstack111lll1lll_opy_
      threading.current_thread().isAppA11yTest = bstack111lll1lll_opy_
  except:
    pass
  bstack1llll111l1_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1lll1lll1l_opy_
  try:
    bstack1lll1lll1l_opy_ = self._test
  except:
    bstack1lll1lll1l_opy_ = self.test
def bstack1llllll1l1_opy_():
  global bstack1l111l111l_opy_
  try:
    if os.path.exists(bstack1l111l111l_opy_):
      os.remove(bstack1l111l111l_opy_)
  except Exception as e:
    logger.debug(bstack1ll111_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡦࡨࡰࡪࡺࡩ࡯ࡩࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺ࠡࠩజ") + str(e))
def bstack11lll1l1l_opy_():
  global bstack1l111l111l_opy_
  bstack1lll11l1l_opy_ = {}
  lock_file = bstack1l111l111l_opy_ + bstack1ll111_opy_ (u"ࠧ࠯࡮ࡲࡧࡰ࠭ఝ")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1ll111_opy_ (u"ࠨࡨ࡬ࡰࡪࡲ࡯ࡤ࡭ࠣࡲࡴࡺࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧ࠯ࠤࡺࡹࡩ࡯ࡩࠣࡦࡦࡹࡩࡤࠢࡩ࡭ࡱ࡫ࠠࡰࡲࡨࡶࡦࡺࡩࡰࡰࡶࠫఞ"))
    try:
      if not os.path.isfile(bstack1l111l111l_opy_):
        with open(bstack1l111l111l_opy_, bstack1ll111_opy_ (u"ࠩࡺࠫట")) as f:
          json.dump({}, f)
      if os.path.exists(bstack1l111l111l_opy_):
        with open(bstack1l111l111l_opy_, bstack1ll111_opy_ (u"ࠪࡶࠬఠ")) as f:
          content = f.read().strip()
          if content:
            bstack1lll11l1l_opy_ = json.loads(content)
    except Exception as e:
      logger.debug(bstack1ll111_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡲࡦࡣࡧ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭డ") + str(e))
    return bstack1lll11l1l_opy_
  try:
    os.makedirs(os.path.dirname(bstack1l111l111l_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      if not os.path.isfile(bstack1l111l111l_opy_):
        with open(bstack1l111l111l_opy_, bstack1ll111_opy_ (u"ࠬࡽࠧఢ")) as f:
          json.dump({}, f)
      if os.path.exists(bstack1l111l111l_opy_):
        with open(bstack1l111l111l_opy_, bstack1ll111_opy_ (u"࠭ࡲࠨణ")) as f:
          content = f.read().strip()
          if content:
            bstack1lll11l1l_opy_ = json.loads(content)
  except Exception as e:
    logger.debug(bstack1ll111_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡵࡩࡦࡪࡩ࡯ࡩࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺ࠡࠩత") + str(e))
  finally:
    return bstack1lll11l1l_opy_
def bstack1l1111lll1_opy_(platform_index, item_index):
  global bstack1l111l111l_opy_
  lock_file = bstack1l111l111l_opy_ + bstack1ll111_opy_ (u"ࠨ࠰࡯ࡳࡨࡱࠧథ")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1ll111_opy_ (u"ࠩࡩ࡭ࡱ࡫࡬ࡰࡥ࡮ࠤࡳࡵࡴࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨ࠰ࠥࡻࡳࡪࡰࡪࠤࡧࡧࡳࡪࡥࠣࡪ࡮ࡲࡥࠡࡱࡳࡩࡷࡧࡴࡪࡱࡱࡷࠬద"))
    try:
      bstack1lll11l1l_opy_ = {}
      if os.path.exists(bstack1l111l111l_opy_):
        with open(bstack1l111l111l_opy_, bstack1ll111_opy_ (u"ࠪࡶࠬధ")) as f:
          content = f.read().strip()
          if content:
            bstack1lll11l1l_opy_ = json.loads(content)
      bstack1lll11l1l_opy_[item_index] = platform_index
      with open(bstack1l111l111l_opy_, bstack1ll111_opy_ (u"ࠦࡼࠨన")) as outfile:
        json.dump(bstack1lll11l1l_opy_, outfile)
    except Exception as e:
      logger.debug(bstack1ll111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡸࡴ࡬ࡸ࡮ࡴࡧࠡࡶࡲࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪ఩") + str(e))
    return
  try:
    os.makedirs(os.path.dirname(bstack1l111l111l_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      bstack1lll11l1l_opy_ = {}
      if os.path.exists(bstack1l111l111l_opy_):
        with open(bstack1l111l111l_opy_, bstack1ll111_opy_ (u"࠭ࡲࠨప")) as f:
          content = f.read().strip()
          if content:
            bstack1lll11l1l_opy_ = json.loads(content)
      bstack1lll11l1l_opy_[item_index] = platform_index
      with open(bstack1l111l111l_opy_, bstack1ll111_opy_ (u"ࠢࡸࠤఫ")) as outfile:
        json.dump(bstack1lll11l1l_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1ll111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡻࡷ࡯ࡴࡪࡰࡪࠤࡹࡵࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭బ") + str(e))
def bstack11ll1l1ll1_opy_(bstack11ll111l11_opy_):
  global CONFIG
  bstack111l11lll_opy_ = bstack1ll111_opy_ (u"ࠩࠪభ")
  if not bstack1ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭మ") in CONFIG:
    logger.info(bstack1ll111_opy_ (u"ࠫࡓࡵࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠣࡴࡦࡹࡳࡦࡦࠣࡹࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡴࡨࡴࡴࡸࡴࠡࡨࡲࡶࠥࡘ࡯ࡣࡱࡷࠤࡷࡻ࡮ࠨయ"))
  try:
    platform = CONFIG[bstack1ll111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨర")][bstack11ll111l11_opy_]
    if bstack1ll111_opy_ (u"࠭࡯ࡴࠩఱ") in platform:
      bstack111l11lll_opy_ += str(platform[bstack1ll111_opy_ (u"ࠧࡰࡵࠪల")]) + bstack1ll111_opy_ (u"ࠨ࠮ࠣࠫళ")
    if bstack1ll111_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬఴ") in platform:
      bstack111l11lll_opy_ += str(platform[bstack1ll111_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭వ")]) + bstack1ll111_opy_ (u"ࠫ࠱ࠦࠧశ")
    if bstack1ll111_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩష") in platform:
      bstack111l11lll_opy_ += str(platform[bstack1ll111_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪస")]) + bstack1ll111_opy_ (u"ࠧ࠭ࠢࠪహ")
    if bstack1ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪ఺") in platform:
      bstack111l11lll_opy_ += str(platform[bstack1ll111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ఻")]) + bstack1ll111_opy_ (u"ࠪ࠰఼ࠥ࠭")
    if bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩఽ") in platform:
      bstack111l11lll_opy_ += str(platform[bstack1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪా")]) + bstack1ll111_opy_ (u"࠭ࠬࠡࠩి")
    if bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨీ") in platform:
      bstack111l11lll_opy_ += str(platform[bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩు")]) + bstack1ll111_opy_ (u"ࠩ࠯ࠤࠬూ")
  except Exception as e:
    logger.debug(bstack1ll111_opy_ (u"ࠪࡗࡴࡳࡥࠡࡧࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡳ࡭ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡶࡸࡷ࡯࡮ࡨࠢࡩࡳࡷࠦࡲࡦࡲࡲࡶࡹࠦࡧࡦࡰࡨࡶࡦࡺࡩࡰࡰࠪృ") + str(e))
  finally:
    if bstack111l11lll_opy_[len(bstack111l11lll_opy_) - 2:] == bstack1ll111_opy_ (u"ࠫ࠱ࠦࠧౄ"):
      bstack111l11lll_opy_ = bstack111l11lll_opy_[:-2]
    return bstack111l11lll_opy_
def bstack1l1111l11l_opy_(path, bstack111l11lll_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack11l111ll_opy_ = ET.parse(path)
    bstack11lll1l11l_opy_ = bstack11l111ll_opy_.getroot()
    bstack11lll1ll11_opy_ = None
    for suite in bstack11lll1l11l_opy_.iter(bstack1ll111_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫ౅")):
      if bstack1ll111_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ె") in suite.attrib:
        suite.attrib[bstack1ll111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬే")] += bstack1ll111_opy_ (u"ࠨࠢࠪై") + bstack111l11lll_opy_
        bstack11lll1ll11_opy_ = suite
    bstack1l11ll1111_opy_ = None
    for robot in bstack11lll1l11l_opy_.iter(bstack1ll111_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ౉")):
      bstack1l11ll1111_opy_ = robot
    bstack111lll1l_opy_ = len(bstack1l11ll1111_opy_.findall(bstack1ll111_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩొ")))
    if bstack111lll1l_opy_ == 1:
      bstack1l11ll1111_opy_.remove(bstack1l11ll1111_opy_.findall(bstack1ll111_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪో"))[0])
      bstack1ll1l1111l_opy_ = ET.Element(bstack1ll111_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫౌ"), attrib={bstack1ll111_opy_ (u"࠭࡮ࡢ࡯ࡨ్ࠫ"): bstack1ll111_opy_ (u"ࠧࡔࡷ࡬ࡸࡪࡹࠧ౎"), bstack1ll111_opy_ (u"ࠨ࡫ࡧࠫ౏"): bstack1ll111_opy_ (u"ࠩࡶ࠴ࠬ౐")})
      bstack1l11ll1111_opy_.insert(1, bstack1ll1l1111l_opy_)
      bstack1l11l1l1l_opy_ = None
      for suite in bstack1l11ll1111_opy_.iter(bstack1ll111_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩ౑")):
        bstack1l11l1l1l_opy_ = suite
      bstack1l11l1l1l_opy_.append(bstack11lll1ll11_opy_)
      bstack11l111l11l_opy_ = None
      for status in bstack11lll1ll11_opy_.iter(bstack1ll111_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ౒")):
        bstack11l111l11l_opy_ = status
      bstack1l11l1l1l_opy_.append(bstack11l111l11l_opy_)
    bstack11l111ll_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1ll111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡵࡷ࡮ࡴࡧࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡱࡩࡷࡧࡴࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠪ౓") + str(e))
def bstack1llll1l1ll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack11l111l11_opy_
  global CONFIG
  if bstack1ll111_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡶࡡࡵࡪࠥ౔") in options:
    del options[bstack1ll111_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡰࡢࡶ࡫ౕࠦ")]
  json_data = bstack11lll1l1l_opy_()
  for item_id in json_data.keys():
    path = os.path.join(outs_dir, str(item_id), bstack1ll111_opy_ (u"ࠨࡱࡸࡸࡵࡻࡴ࠯ࡺࡰࡰౖࠬ"))
    bstack1l1111l11l_opy_(path, bstack11ll1l1ll1_opy_(json_data[item_id]))
  bstack1llllll1l1_opy_()
  return bstack11l111l11_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1llll111l_opy_(self, ff_profile_dir):
  global bstack11l1ll1l11_opy_
  if not ff_profile_dir:
    return None
  return bstack11l1ll1l11_opy_(self, ff_profile_dir)
def bstack1lllllll1_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack11l111ll1l_opy_
  bstack1l1ll1l11l_opy_ = []
  if bstack1ll111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ౗") in CONFIG:
    bstack1l1ll1l11l_opy_ = CONFIG[bstack1ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ౘ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1ll111_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࠧౙ")],
      pabot_args[bstack1ll111_opy_ (u"ࠧࡼࡥࡳࡤࡲࡷࡪࠨౚ")],
      argfile,
      pabot_args.get(bstack1ll111_opy_ (u"ࠨࡨࡪࡸࡨࠦ౛")),
      pabot_args[bstack1ll111_opy_ (u"ࠢࡱࡴࡲࡧࡪࡹࡳࡦࡵࠥ౜")],
      platform[0],
      bstack11l111ll1l_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1ll111_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡩ࡭ࡱ࡫ࡳࠣౝ")] or [(bstack1ll111_opy_ (u"ࠤࠥ౞"), None)]
    for platform in enumerate(bstack1l1ll1l11l_opy_)
  ]
def bstack11l1l111l_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1l1l111l1_opy_=bstack1ll111_opy_ (u"ࠪࠫ౟")):
  global bstack1l111l11l1_opy_
  self.platform_index = platform_index
  self.bstack1l11111l1l_opy_ = bstack1l1l111l1_opy_
  bstack1l111l11l1_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1111ll1l11_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1ll1ll11l1_opy_
  global bstack11lll1l111_opy_
  bstack111l111l1_opy_ = copy.deepcopy(item)
  if not bstack1ll111_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ౠ") in item.options:
    bstack111l111l1_opy_.options[bstack1ll111_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧౡ")] = []
  bstack11l1llllll_opy_ = bstack111l111l1_opy_.options[bstack1ll111_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨౢ")].copy()
  for v in bstack111l111l1_opy_.options[bstack1ll111_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩౣ")]:
    if bstack1ll111_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡑࡎࡄࡘࡋࡕࡒࡎࡋࡑࡈࡊ࡞ࠧ౤") in v:
      bstack11l1llllll_opy_.remove(v)
    if bstack1ll111_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡅࡏࡍࡆࡘࡇࡔࠩ౥") in v:
      bstack11l1llllll_opy_.remove(v)
    if bstack1ll111_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡇࡉࡋࡒࡏࡄࡃࡏࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ౦") in v:
      bstack11l1llllll_opy_.remove(v)
  bstack11l1llllll_opy_.insert(0, bstack1ll111_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚࠽ࡿࢂ࠭౧").format(bstack111l111l1_opy_.platform_index))
  bstack11l1llllll_opy_.insert(0, bstack1ll111_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡉࡋࡆࡍࡑࡆࡅࡑࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓ࠼ࡾࢁࠬ౨").format(bstack111l111l1_opy_.bstack1l11111l1l_opy_))
  bstack111l111l1_opy_.options[bstack1ll111_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨ౩")] = bstack11l1llllll_opy_
  if bstack11lll1l111_opy_:
    bstack111l111l1_opy_.options[bstack1ll111_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ౪")].insert(0, bstack1ll111_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓ࠻ࡽࢀࠫ౫").format(bstack11lll1l111_opy_))
  return bstack1ll1ll11l1_opy_(caller_id, datasources, is_last, bstack111l111l1_opy_, outs_dir)
def bstack1l111l1l11_opy_(command, item_index):
  try:
    if global_config.get_property(bstack1ll111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪ౬")):
      os.environ[bstack1ll111_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫ౭")] = json.dumps(CONFIG[bstack1ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ౮")][item_index % bstack1ll1l111l_opy_])
    global bstack11lll1l111_opy_
    os.environ[bstack1ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ౯")] = str(item_index % bstack1ll1l111l_opy_)
    listener_arg = bstack1ll111_opy_ (u"࠭ࠧ౰")
    if is_robot_playwright_installed() and cli.is_enabled(CONFIG):
      listener_arg = bstack1ll111_opy_ (u"ࠧࠡ࠯࠰ࡰ࡮ࡹࡴࡦࡰࡨࡶࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡸࡪ࡫࠯ࡴࡲࡦࡴࡺ࡟࡭࡫ࡶࡸࡪࡴࡥࡳࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠴ࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡓࡥࡹࡩࡨࡦࡴࠪ౱")
      logger.debug(bstack1ll111_opy_ (u"ࠣࡃࡧࡨ࡮ࡴࡧࠡࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡕࡧࡴࡤࡪࡨࡶࠥࡲࡩࡴࡶࡨࡲࡪࡸࠠࡧࡱࡵࠤ࡮ࡺࡥ࡮ࠢࡾࢁࠧ౲").format(item_index))
    bstack1ll11l1l1_opy_ = bstack1ll111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠮ࡵࡧ࡯ࠥࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱࠦ࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࠢࠥ౳") + \
              str(item_index % bstack1ll1l111l_opy_) + \
              bstack1ll111_opy_ (u"ࠥࠤ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠣࠦ౴") + \
              str(item_index) + \
              listener_arg
    if bstack11lll1l111_opy_:
        bstack1ll11l1l1_opy_ += bstack1ll111_opy_ (u"ࠦࠥࠨ౵") + bstack11lll1l111_opy_
    command[0:1] = bstack1ll11l1l1_opy_.split()
  except Exception as e:
    logger.error(bstack1ll111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡲࡵࡤࡪࡨࡼ࡭ࡳ࡭ࠠࡤࡱࡰࡱࡦࡴࡤࠡࡨࡲࡶࠥࡶࡡࡣࡱࡷࠤࡷࡻ࡮࠻ࠢࡾࢁࠬ౶").format(str(e)))
def bstack1l1llll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1lll1lll1_opy_
  try:
    bstack1l111l1l11_opy_(command, item_index)
    return bstack1lll1lll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
  except Exception as e:
    logger.error(bstack1ll111_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠࡳࡷࡱ࠾ࠥࢁࡽࠨ౷").format(str(e)))
    raise e
def bstack1lll11l1l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1lll1lll1_opy_
  try:
    bstack1l111l1l11_opy_(command, item_index)
    return bstack1lll1lll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
  except Exception as e:
    logger.error(bstack1ll111_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡧࡵࡴࠡࡴࡸࡲࠥ࠸࠮࠲࠵࠽ࠤࢀࢃࠧ౸").format(str(e)))
    try:
      return bstack1lll1lll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
    except Exception as e2:
      logger.error(bstack1ll111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡦࡨ࡯ࡵࠢ࠵࠲࠶࠹ࠠࡧࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣࡿࢂ࠭౹").format(str(e2)))
      raise e
def bstack11111lll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1lll1lll1_opy_
  try:
    bstack1l111l1l11_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    return bstack1lll1lll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
  except Exception as e:
    logger.error(bstack1ll111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡢࡰࡶࠣࡶࡺࡴࠠ࠳࠰࠴࠹࠿ࠦࡻࡾࠩ౺").format(str(e)))
    try:
      return bstack1lll1lll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
    except Exception as e2:
      logger.error(bstack1ll111_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡣࡱࡷࠤ࠷࠴࠱࠶ࠢࡩࡥࡱࡲࡢࡢࡥ࡮࠾ࠥࢁࡽࠨ౻").format(str(e2)))
      raise e
def _11l11l1lll_opy_(bstack11l11ll111_opy_, item_index, process_timeout, sleep_before_start, bstack1ll1l1llll_opy_):
  bstack1l111l1l11_opy_(bstack11l11ll111_opy_, item_index)
  if process_timeout is None:
    process_timeout = 3600
  if sleep_before_start and sleep_before_start > 0:
    time.sleep(min(sleep_before_start, 5))
  return process_timeout
def bstack11l11llll_opy_(command, bstack1l11ll1l11_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack1lll1lll1_opy_
  global bstack1l1l111l1l_opy_
  global bstack11lll1l111_opy_
  try:
    for env_name, bstack1l111l11_opy_ in bstack1l1l111l1l_opy_.items():
      os.environ[env_name] = bstack1l111l11_opy_
    bstack11lll1l111_opy_ = bstack1ll111_opy_ (u"ࠦࠧ౼")
    bstack1l111l1l11_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    if sleep_before_start and sleep_before_start > 0:
      time.sleep(min(sleep_before_start, 5))
    return bstack1lll1lll1_opy_(command, bstack1l11ll1l11_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack1ll111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡥࡳࡹࠦࡲࡶࡰࠣ࠹࠳࠶࠺ࠡࡽࢀࠫ౽").format(str(e)))
    try:
      return bstack1lll1lll1_opy_(command, bstack1l11ll1l11_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack1ll111_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠࡧࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣࡿࢂ࠭౾").format(str(e2)))
      raise e
def bstack1llll1ll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack1lll1lll1_opy_
  try:
    process_timeout = _11l11l1lll_opy_(command, item_index, process_timeout, sleep_before_start, bstack1ll111_opy_ (u"ࠧ࠵࠰࠵ࠫ౿"))
    return bstack1lll1lll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack1ll111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡦࡨ࡯ࡵࠢࡵࡹࡳࠦ࠴࠯࠴࠽ࠤࢀࢃࠧಀ").format(str(e)))
    try:
      return bstack1lll1lll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack1ll111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡢࡰࡶࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࡻࡾࠩಁ").format(str(e2)))
      raise e
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack1ll1lllll1_opy_(self, runner, quiet=False, capture=True):
  global bstack1l1l1ll111_opy_
  bstack1l11ll11l1_opy_ = bstack1l1l1ll111_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack1ll111_opy_ (u"ࠪࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࡥࡡࡳࡴࠪಂ")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1ll111_opy_ (u"ࠫࡪࡾࡣࡠࡶࡵࡥࡨ࡫ࡢࡢࡥ࡮ࡣࡦࡸࡲࠨಃ")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1l11ll11l1_opy_
def bstack11l111l1ll_opy_(runner, hook_name, context, element, bstack11l1lll1_opy_, *args):
  global bstack11lll11l1_opy_
  try:
    if runner.hooks.get(hook_name):
      bstack1lll11ll1l_opy_.bstack1llllll111_opy_(hook_name, element)
    if bstack11lll11l1_opy_ is None or bstack11lll11l1_opy_:
      bstack11l1lll1_opy_(runner, hook_name, context, *args)
    else:
      bstack1lll1l111l_opy_ = (context,) + args
      bstack11l1lll1_opy_(runner, hook_name, *bstack1lll1l111l_opy_)
    if runner.hooks.get(hook_name):
      bstack1lll11ll1l_opy_.bstack111l1llll_opy_(element)
      if hook_name not in [bstack1ll111_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠩ಄"), bstack1ll111_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠩಅ")] and args and hasattr(args[0], bstack1ll111_opy_ (u"ࠧࡦࡴࡵࡳࡷࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠧಆ")):
        args[0].error_message = bstack1ll111_opy_ (u"ࠨࠩಇ")
  except Exception as e:
    logger.debug(bstack1ll111_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡮ࡡ࡯ࡦ࡯ࡩࠥ࡮࡯ࡰ࡭ࡶࠤ࡮ࡴࠠࡣࡧ࡫ࡥࡻ࡫࠺ࠡࡽࢀࠫಈ").format(str(e)))
@measure(event_name=EVENTS.bstack1l111l1l1l_opy_, stage=STAGE.bstack11ll1111_opy_, hook_type=bstack1ll111_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡄࡰࡱࠨಉ"), bstack11l11l111_opy_=SESSION_NAME)
def bstack11111ll11_opy_(runner, name, context, bstack11l1lll1_opy_, *args):
    if runner.hooks.get(bstack1ll111_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣಊ")).__name__ != bstack1ll111_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࡡࡧࡩ࡫ࡧࡵ࡭ࡶࡢ࡬ࡴࡵ࡫ࠣಋ"):
      bstack11l111l1ll_opy_(runner, name, context, runner, bstack11l1lll1_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack1ll1ll1ll_opy_(bstack1ll111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬಌ")) else context.browser
      runner.driver_initialised = bstack1ll111_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦ಍")
    except Exception as e:
      logger.debug(bstack1ll111_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡦࡵ࡭ࡻ࡫ࡲࠡ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡶࡩࠥࡧࡴࡵࡴ࡬ࡦࡺࡺࡥ࠻ࠢࡾࢁࠬಎ").format(str(e)))
def bstack1ll11l111_opy_(runner, name, context, bstack11l1lll1_opy_, *args):
    bstack11l111l1ll_opy_(runner, name, context, context.feature, bstack11l1lll1_opy_, *args)
    try:
      if not bstack11111l111_opy_:
        bstack11l11l11_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll1ll1ll_opy_(bstack1ll111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨಏ")) else context.browser
        if is_driver_active(bstack11l11l11_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack1ll111_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦಐ")
          bstack11l1l11ll1_opy_ = str(runner.feature.name)
          playwright_set_session_name(context, bstack11l1l11ll1_opy_)
          bstack11l11l11_opy_.execute_script(bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩ಑") + json.dumps(bstack11l1l11ll1_opy_) + bstack1ll111_opy_ (u"ࠬࢃࡽࠨಒ"))
    except Exception as e:
      logger.debug(bstack1ll111_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭ಓ").format(str(e)))
def bstack1llll1ll1_opy_(runner, name, context, bstack11l1lll1_opy_, *args):
    target = context.scenario if hasattr(context, bstack1ll111_opy_ (u"ࠧࡴࡥࡨࡲࡦࡸࡩࡰࠩಔ")) else context.feature
    bstack11l111l1ll_opy_(runner, name, context, target, bstack11l1lll1_opy_, *args)
@measure(event_name=EVENTS.bstack1l1l111ll1_opy_, stage=STAGE.bstack11ll1111_opy_, bstack11l11l111_opy_=SESSION_NAME)
def bstack1l1lll111l_opy_(runner, name, context, bstack11l1lll1_opy_, *args):
    bstack1lll11ll1l_opy_.start_test(context)
    bstack11l111l1ll_opy_(runner, name, context, context.scenario, bstack11l1lll1_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack1llll11lll_opy_.bstack111ll1l1ll_opy_(context, *args)
    try:
      bstack11l11l11_opy_ = bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧಕ"), context.browser)
      if is_driver_active(bstack11l11l11_opy_):
        TestHubHandler.send_cbt_info(bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨಖ"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack1ll111_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧಗ")
        if (not bstack11111l111_opy_):
          scenario_name = args[0].name
          feature_name = bstack11l1l11ll1_opy_ = str(runner.feature.name)
          bstack11l1l11ll1_opy_ = feature_name + bstack1ll111_opy_ (u"ࠫࠥ࠳ࠠࠨಘ") + scenario_name
          if runner.driver_initialised == bstack1ll111_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢಙ"):
            playwright_set_session_name(context, bstack11l1l11ll1_opy_)
            bstack11l11l11_opy_.execute_script(bstack1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫಚ") + json.dumps(bstack11l1l11ll1_opy_) + bstack1ll111_opy_ (u"ࠧࡾࡿࠪಛ"))
    except Exception as e:
      logger.debug(bstack1ll111_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡨ࡫࡮ࡢࡴ࡬ࡳ࠿ࠦࡻࡾࠩಜ").format(str(e)))
@measure(event_name=EVENTS.bstack1l111l1l1l_opy_, stage=STAGE.bstack11ll1111_opy_, hook_type=bstack1ll111_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡕࡷࡩࡵࠨಝ"), bstack11l11l111_opy_=SESSION_NAME)
def bstack1l1lll11_opy_(runner, name, context, bstack11l1lll1_opy_, *args):
    bstack11l111l1ll_opy_(runner, name, context, args[0], bstack11l1lll1_opy_, *args)
    try:
      bstack11l11l11_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll1ll1ll_opy_(bstack1ll111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩಞ")) else context.browser
      if is_driver_active(bstack11l11l11_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack1ll111_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤಟ")
        bstack1lll11ll1l_opy_.bstack111lll1ll1_opy_(args[0])
        if runner.driver_initialised == bstack1ll111_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥಠ") and not bstack11111l111_opy_:
          feature_name = bstack11l1l11ll1_opy_ = str(runner.feature.name)
          bstack11l1l11ll1_opy_ = feature_name + bstack1ll111_opy_ (u"࠭ࠠ࠮ࠢࠪಡ") + context.scenario.name
          playwright_set_session_name(context, bstack11l1l11ll1_opy_)
          bstack11l11l11_opy_.execute_script(bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬಢ") + json.dumps(bstack11l1l11ll1_opy_) + bstack1ll111_opy_ (u"ࠨࡿࢀࠫಣ"))
    except Exception as e:
      logger.debug(bstack1ll111_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡ࡫ࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡺࡥࡱ࠼ࠣࡿࢂ࠭ತ").format(str(e)))
@measure(event_name=EVENTS.bstack1l111l1l1l_opy_, stage=STAGE.bstack11ll1111_opy_, hook_type=bstack1ll111_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࡕࡷࡩࡵࠨಥ"), bstack11l11l111_opy_=SESSION_NAME)
def bstack1l1111111l_opy_(runner, name, context, bstack11l1lll1_opy_, *args):
  bstack1lll11ll1l_opy_.bstack1l1l11lll1_opy_(args[0])
  try:
    step_status = args[0].status.name
    bstack11l11l11_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪದ") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack11l11l11_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack1ll111_opy_ (u"ࠬ࡯࡮ࡴࡶࡨࡴࠬಧ")
        if not bstack11111l111_opy_:
          feature_name = bstack11l1l11ll1_opy_ = str(runner.feature.name)
          bstack11l1l11ll1_opy_ = feature_name + bstack1ll111_opy_ (u"࠭ࠠ࠮ࠢࠪನ") + context.scenario.name
          playwright_set_session_name(context, bstack11l1l11ll1_opy_)
          bstack11l11l11_opy_.execute_script(bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬ಩") + json.dumps(bstack11l1l11ll1_opy_) + bstack1ll111_opy_ (u"ࠨࡿࢀࠫಪ"))
    if str(step_status).lower() in [bstack1ll111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩಫ"), bstack1ll111_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩಬ")]:
      bstack1l1111l11_opy_ = bstack1ll111_opy_ (u"ࠫࠬಭ")
      bstack1l11111111_opy_ = bstack1ll111_opy_ (u"ࠬ࠭ಮ")
      bstack11ll1lll_opy_ = bstack1ll111_opy_ (u"࠭ࠧಯ")
      try:
        import traceback
        bstack1l1111l11_opy_ = runner.exception.__class__.__name__
        bstack1ll111lll1_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1l11111111_opy_ = bstack1ll111_opy_ (u"ࠧࠡࠩರ").join(bstack1ll111lll1_opy_)
        bstack11ll1lll_opy_ = bstack1ll111lll1_opy_[-1]
      except Exception as e:
        logger.debug(bstack111llll11_opy_.format(str(e)))
      bstack1l1111l11_opy_ += bstack11ll1lll_opy_
      playwright_annotate(context, json.dumps(str(args[0].name) + bstack1ll111_opy_ (u"ࠣࠢ࠰ࠤࡋࡧࡩ࡭ࡧࡧࠥࡡࡴࠢಱ") + str(bstack1l11111111_opy_)),
                          bstack1ll111_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣಲ"))
      if runner.driver_initialised == bstack1ll111_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣಳ"):
        bstack1llll1l1_opy_(getattr(context, bstack1ll111_opy_ (u"ࠫࡵࡧࡧࡦࠩ಴"), None), bstack1ll111_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧವ"), bstack1l1111l11_opy_)
        bstack11l11l11_opy_.execute_script(bstack1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫಶ") + json.dumps(str(args[0].name) + bstack1ll111_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨಷ") + str(bstack1l11111111_opy_)) + bstack1ll111_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨಸ"))
      if runner.driver_initialised == bstack1ll111_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢಹ"):
        bstack111lll11_opy_(bstack11l11l11_opy_, bstack1ll111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ಺"), bstack1ll111_opy_ (u"ࠦࡘࡩࡥ࡯ࡣࡵ࡭ࡴࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࡢ࡮ࠣ಻") + str(bstack1l1111l11_opy_))
    else:
      playwright_annotate(context, bstack1ll111_opy_ (u"ࠧࡖࡡࡴࡵࡨࡨࠦࠨ಼"), bstack1ll111_opy_ (u"ࠨࡩ࡯ࡨࡲࠦಽ"))
      if runner.driver_initialised == bstack1ll111_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧಾ"):
        bstack1llll1l1_opy_(getattr(context, bstack1ll111_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭ಿ"), None), bstack1ll111_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤೀ"))
      bstack11l11l11_opy_.execute_script(bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨು") + json.dumps(str(args[0].name) + bstack1ll111_opy_ (u"ࠦࠥ࠳ࠠࡑࡣࡶࡷࡪࡪࠡࠣೂ")) + bstack1ll111_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫೃ"))
      if runner.driver_initialised == bstack1ll111_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦೄ"):
        bstack111lll11_opy_(bstack11l11l11_opy_, bstack1ll111_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ೅"))
  except Exception as e:
    logger.debug(bstack1ll111_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࠥࡹࡴࡦࡲ࠽ࠤࢀࢃࠧೆ").format(str(e)))
  bstack11l111l1ll_opy_(runner, name, context, args[0], bstack11l1lll1_opy_, *args)
@measure(event_name=EVENTS.bstack1l11l1111l_opy_, stage=STAGE.bstack11ll1111_opy_, bstack11l11l111_opy_=SESSION_NAME)
def bstack11llllllll_opy_(runner, name, context, bstack11l1lll1_opy_, *args):
  bstack1lll11ll1l_opy_.end_test(args[0])
  try:
    bstack11l1l11lll_opy_ = args[0].status.name
    bstack11l11l11_opy_ = bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨೇ"), context.browser)
    bstack1llll11lll_opy_.bstack1111lll1ll_opy_(bstack11l11l11_opy_)
    if str(bstack11l1l11lll_opy_).lower() in [bstack1ll111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪೈ"), bstack1ll111_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ೉")]:
      bstack1l1111l11_opy_ = bstack1ll111_opy_ (u"ࠬ࠭ೊ")
      bstack1l11111111_opy_ = bstack1ll111_opy_ (u"࠭ࠧೋ")
      bstack11ll1lll_opy_ = bstack1ll111_opy_ (u"ࠧࠨೌ")
      try:
        import traceback
        bstack1l1111l11_opy_ = runner.exception.__class__.__name__
        bstack1ll111lll1_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1l11111111_opy_ = bstack1ll111_opy_ (u"ࠨ್ࠢࠪ").join(bstack1ll111lll1_opy_)
        bstack11ll1lll_opy_ = bstack1ll111lll1_opy_[-1]
      except Exception as e:
        logger.debug(bstack111llll11_opy_.format(str(e)))
      bstack1l1111l11_opy_ += bstack11ll1lll_opy_
      playwright_annotate(context, json.dumps(str(args[0].name) + bstack1ll111_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣ೎") + str(bstack1l11111111_opy_)),
                          bstack1ll111_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤ೏"))
      if runner.driver_initialised == bstack1ll111_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨ೐") or runner.driver_initialised == bstack1ll111_opy_ (u"ࠬ࡯࡮ࡴࡶࡨࡴࠬ೑"):
        bstack1llll1l1_opy_(getattr(context, bstack1ll111_opy_ (u"࠭ࡰࡢࡩࡨࠫ೒"), None), bstack1ll111_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ೓"), bstack1l1111l11_opy_)
        bstack11l11l11_opy_.execute_script(bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭೔") + json.dumps(str(args[0].name) + bstack1ll111_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣೕ") + str(bstack1l11111111_opy_)) + bstack1ll111_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪೖ"))
      if runner.driver_initialised == bstack1ll111_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨ೗") or runner.driver_initialised == bstack1ll111_opy_ (u"ࠬ࡯࡮ࡴࡶࡨࡴࠬ೘"):
        bstack111lll11_opy_(bstack11l11l11_opy_, bstack1ll111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭೙"), bstack1ll111_opy_ (u"ࠢࡔࡥࡨࡲࡦࡸࡩࡰࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦ೚") + str(bstack1l1111l11_opy_))
    else:
      playwright_annotate(context, bstack1ll111_opy_ (u"ࠣࡒࡤࡷࡸ࡫ࡤࠢࠤ೛"), bstack1ll111_opy_ (u"ࠤ࡬ࡲ࡫ࡵࠢ೜"))
      if runner.driver_initialised == bstack1ll111_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧೝ") or runner.driver_initialised == bstack1ll111_opy_ (u"ࠫ࡮ࡴࡳࡵࡧࡳࠫೞ"):
        bstack1llll1l1_opy_(getattr(context, bstack1ll111_opy_ (u"ࠬࡶࡡࡨࡧࠪ೟"), None), bstack1ll111_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨೠ"))
      bstack11l11l11_opy_.execute_script(bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬೡ") + json.dumps(str(args[0].name) + bstack1ll111_opy_ (u"ࠣࠢ࠰ࠤࡕࡧࡳࡴࡧࡧࠥࠧೢ")) + bstack1ll111_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧࢃࡽࠨೣ"))
      if runner.driver_initialised == bstack1ll111_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧ೤") or runner.driver_initialised == bstack1ll111_opy_ (u"ࠫ࡮ࡴࡳࡵࡧࡳࠫ೥"):
        bstack111lll11_opy_(bstack11l11l11_opy_, bstack1ll111_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ೦"))
  except Exception as e:
    logger.debug(bstack1ll111_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨ೧").format(str(e)))
  bstack11l111l1ll_opy_(runner, name, context, context.scenario, bstack11l1lll1_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack11ll1l111_opy_(runner, name, context, bstack11l1lll1_opy_, *args):
    target = context.scenario if hasattr(context, bstack1ll111_opy_ (u"ࠧࡴࡥࡨࡲࡦࡸࡩࡰࠩ೨")) else context.feature
    bstack11l111l1ll_opy_(runner, name, context, target, bstack11l1lll1_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack11llll1ll1_opy_(runner, name, context, bstack11l1lll1_opy_, *args):
    try:
      bstack11l11l11_opy_ = bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ೩"), context.browser)
      bstack1ll11l11l_opy_ = bstack1ll111_opy_ (u"ࠩࠪ೪")
      if context.failed is True:
        bstack111111ll_opy_ = []
        bstack1ll1111l_opy_ = []
        bstack11lllll1l_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack111111ll_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1ll111lll1_opy_ = traceback.format_tb(exc_tb)
            bstack1l1l1ll11_opy_ = bstack1ll111_opy_ (u"ࠪࠤࠬ೫").join(bstack1ll111lll1_opy_)
            bstack1ll1111l_opy_.append(bstack1l1l1ll11_opy_)
            bstack11lllll1l_opy_.append(bstack1ll111lll1_opy_[-1])
        except Exception as e:
          logger.debug(bstack111llll11_opy_.format(str(e)))
        bstack1l1111l11_opy_ = bstack1ll111_opy_ (u"ࠫࠬ೬")
        for i in range(len(bstack111111ll_opy_)):
          bstack1l1111l11_opy_ += bstack111111ll_opy_[i] + bstack11lllll1l_opy_[i] + bstack1ll111_opy_ (u"ࠬࡢ࡮ࠨ೭")
        bstack1ll11l11l_opy_ = bstack1ll111_opy_ (u"࠭ࠠࠨ೮").join(bstack1ll1111l_opy_)
        if runner.driver_initialised in [bstack1ll111_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣ೯"), bstack1ll111_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧ೰")]:
          playwright_annotate(context, bstack1ll11l11l_opy_, bstack1ll111_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣೱ"))
          bstack1llll1l1_opy_(getattr(context, bstack1ll111_opy_ (u"ࠪࡴࡦ࡭ࡥࠨೲ"), None), bstack1ll111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦೳ"), bstack1l1111l11_opy_)
          bstack11l11l11_opy_.execute_script(bstack1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ೴") + json.dumps(bstack1ll11l11l_opy_) + bstack1ll111_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥࢁࢂ࠭೵"))
          bstack111lll11_opy_(bstack11l11l11_opy_, bstack1ll111_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ೶"), bstack1ll111_opy_ (u"ࠣࡕࡲࡱࡪࠦࡳࡤࡧࡱࡥࡷ࡯࡯ࡴࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡠࡳࠨ೷") + str(bstack1l1111l11_opy_))
          bstack1l1ll11l1_opy_ = bstack11l1llll1_opy_(bstack1ll11l11l_opy_, runner.feature.name, logger)
          if (bstack1l1ll11l1_opy_ != None):
            bstack11l11l111l_opy_.append(bstack1l1ll11l1_opy_)
      else:
        if runner.driver_initialised in [bstack1ll111_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠥ೸"), bstack1ll111_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢ೹")]:
          playwright_annotate(context, bstack1ll111_opy_ (u"ࠦࡋ࡫ࡡࡵࡷࡵࡩ࠿ࠦࠢ೺") + str(runner.feature.name) + bstack1ll111_opy_ (u"ࠧࠦࡰࡢࡵࡶࡩࡩࠧࠢ೻"), bstack1ll111_opy_ (u"ࠨࡩ࡯ࡨࡲࠦ೼"))
          bstack1llll1l1_opy_(getattr(context, bstack1ll111_opy_ (u"ࠧࡱࡣࡪࡩࠬ೽"), None), bstack1ll111_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ೾"))
          bstack11l11l11_opy_.execute_script(bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ೿") + json.dumps(bstack1ll111_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨ࠾ࠥࠨഀ") + str(runner.feature.name) + bstack1ll111_opy_ (u"ࠦࠥࡶࡡࡴࡵࡨࡨࠦࠨഁ")) + bstack1ll111_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫം"))
          bstack111lll11_opy_(bstack11l11l11_opy_, bstack1ll111_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ഃ"))
          bstack1l1ll11l1_opy_ = bstack11l1llll1_opy_(bstack1ll11l11l_opy_, runner.feature.name, logger)
          if (bstack1l1ll11l1_opy_ != None):
            bstack11l11l111l_opy_.append(bstack1l1ll11l1_opy_)
    except Exception as e:
      logger.debug(bstack1ll111_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩഄ").format(str(e)))
    bstack11l111l1ll_opy_(runner, name, context, context.feature, bstack11l1lll1_opy_, *args)
@measure(event_name=EVENTS.bstack1l111l1l1l_opy_, stage=STAGE.bstack11ll1111_opy_, hook_type=bstack1ll111_opy_ (u"ࠣࡣࡩࡸࡪࡸࡁ࡭࡮ࠥഅ"), bstack11l11l111_opy_=SESSION_NAME)
def bstack1ll1l11l_opy_(runner, name, context, bstack11l1lll1_opy_, *args):
    bstack11l111l1ll_opy_(runner, name, context, runner, bstack11l1lll1_opy_, *args)
def bstack1lll11l1ll_opy_(self, filename=None):
  global bstack1ll1l111ll_opy_
  bstack1ll1l111ll_opy_(self, filename)
  bstack11ll1l11ll_opy_ = []
  bstack1lll1l1111_opy_ = [bstack1ll111_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠪആ"), bstack1ll111_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡸࡦ࡭ࠧഇ"), bstack1ll111_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ഈ"), bstack1ll111_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ഉ"), bstack1ll111_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡺࡡࡨࠩഊ"), bstack1ll111_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡦࡦࡣࡷࡹࡷ࡫ࠧഋ")]
  bstack1ll1111ll1_opy_ = lambda *_: None
  for hook_name in bstack1lll1l1111_opy_:
    if hook_name not in self.hooks:
      self.hooks[hook_name] = bstack1ll1111ll1_opy_
      bstack11ll1l11ll_opy_.append(hook_name)
  if bstack11ll1l11ll_opy_:
    os.environ[bstack1ll111_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡕࡇࡏࡤࡊࡅࡇࡃࡘࡐ࡙ࡥࡈࡐࡑࡎࡗࠬഌ")] = bstack1ll111_opy_ (u"ࠩ࠯ࠫ഍").join(bstack11ll1l11ll_opy_)
def _execute_deferred_playwright_close():
  try:
    _111l1111l1_opy_ = threading.current_thread()
    _1lllll1lll_opy_ = getattr(_111l1111l1_opy_, bstack1ll111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡨࡪ࡬ࡥࡳࡴࡨࡨࡤࡶࡡࡨࡧࡢࡶࡪ࡬ࠧഎ"), None)
    _1ll11ll111_opy_ = getattr(_111l1111l1_opy_, bstack1ll111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡩ࡫ࡦࡦࡴࡵࡩࡩࡥࡢࡳࡱࡺࡷࡪࡸ࡟ࡳࡧࡩࠫഏ"), None)
    _11lll1ll1_opy_ = getattr(_111l1111l1_opy_, bstack1ll111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡪࡥࡧࡧࡵࡶࡪࡪ࡟ࡱࡹࡢࡷࡹࡵࡰࡠࡨࡱࠫഐ"), None)
    _wrapper = getattr(_111l1111l1_opy_, bstack1ll111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ഑"), None)
    if not _1ll11ll111_opy_ and _wrapper and hasattr(_wrapper, bstack1ll111_opy_ (u"ࠧࡠࡤࡵࡳࡼࡹࡥࡳࠩഒ")):
      _1ll11ll111_opy_ = _wrapper._browser
    if not _1lllll1lll_opy_ and _wrapper and hasattr(_wrapper, bstack1ll111_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧഓ")):
      _1lllll1lll_opy_ = _wrapper._page
    if not _11lll1ll1_opy_:
      _111l11111l_opy_ = getattr(_111l1111l1_opy_, bstack1ll111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡧࡩ࡫࡫ࡲࡳࡧࡧࡣࡵࡽ࡟ࡳࡧࡩࠫഔ"), None)
      if _111l11111l_opy_ and hasattr(_111l11111l_opy_, bstack1ll111_opy_ (u"ࠪࡷࡹࡵࡰࠨക")):
        _11lll1ll1_opy_ = _111l11111l_opy_.stop
    _11ll111ll_opy_ = _1lllll1lll_opy_ or _1ll11ll111_opy_ or _11lll1ll1_opy_
    if not _11ll111ll_opy_:
      return
    if _1lllll1lll_opy_ and hasattr(_1lllll1lll_opy_, bstack1ll111_opy_ (u"ࠫࡨࡲ࡯ࡴࡧࠪഖ")):
      try:
        _1lllll1lll_opy_.close(_bstack_sdk_close=True)
      except TypeError:
        try:
          _1lllll1lll_opy_.close()
        except Exception:
          pass
      except Exception as e:
        logger.debug(bstack1ll111_opy_ (u"ࠬࡊࡥࡧࡧࡵࡶࡪࡪࠠࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡵࡧࡧࡦ࠰ࡦࡰࡴࡹࡥࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࡾࢁࠬഗ").format(str(e)))
    if _1ll11ll111_opy_ and hasattr(_1ll11ll111_opy_, bstack1ll111_opy_ (u"࠭ࡣ࡭ࡱࡶࡩࠬഘ")):
      try:
        _1ll11ll111_opy_.close(_bstack_sdk_close=True)
      except TypeError:
        try:
          _1ll11ll111_opy_.close()
        except Exception:
          pass
      except Exception as e:
        logger.debug(bstack1ll111_opy_ (u"ࠧࡅࡧࡩࡩࡷࡸࡥࡥࠢࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡢࡳࡱࡺࡷࡪࡸ࠮ࡤ࡮ࡲࡷࡪࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࡼࡿࠪങ").format(str(e)))
    if _11lll1ll1_opy_:
      try:
        _11lll1ll1_opy_(_bstack_sdk_close=True)
      except TypeError:
        try:
          _11lll1ll1_opy_()
        except Exception:
          pass
      except Exception as e:
        logger.debug(bstack1ll111_opy_ (u"ࠨࡆࡨࡪࡪࡸࡲࡦࡦࠣࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡶࡲࡴࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡾࠩച").format(str(e)))
    for attr in (bstack1ll111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡧࡩ࡫࡫ࡲࡳࡧࡧࡣࡵࡧࡧࡦࡡࡦࡰࡴࡹࡥࠨഛ"), bstack1ll111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡨࡪ࡬ࡥࡳࡴࡨࡨࡤࡶࡡࡨࡧࡢࡶࡪ࡬ࠧജ"),
                 bstack1ll111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡩ࡫ࡦࡦࡴࡵࡩࡩࡥࡢࡳࡱࡺࡷࡪࡸ࡟ࡤ࡮ࡲࡷࡪ࠭ഝ"), bstack1ll111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡪࡥࡧࡧࡵࡶࡪࡪ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡠࡴࡨࡪࠬഞ"),
                 bstack1ll111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡤࡦࡨࡨࡶࡷ࡫ࡤࡠࡲࡺࡣࡸࡺ࡯ࡱࠩട"), bstack1ll111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡥࡧࡩࡩࡷࡸࡥࡥࡡࡳࡻࡤࡹࡴࡰࡲࡢࡪࡳ࠭ഠ"),
                 bstack1ll111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡦࡨࡪࡪࡸࡲࡦࡦࡢࡴࡼࡥࡲࡦࡨࠪഡ")):
      try:
        delattr(_111l1111l1_opy_, attr)
      except AttributeError:
        pass
    if _wrapper:
      try:
        _wrapper._page = None
        _wrapper._browser = None
      except Exception:
        pass
    logger.debug(bstack1ll111_opy_ (u"ࠩࡇࡩ࡫࡫ࡲࡳࡧࡧࠤࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡥ࡯ࡳࡸ࡫ࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࡦࠣࡪࡴࡸࠠࡵࡪࡵࡩࡦࡪࠠࡼࡿࠪഢ").format(_111l1111l1_opy_.ident))
  except Exception as e:
    logger.debug(bstack1ll111_opy_ (u"ࠪࡈࡪ࡬ࡥࡳࡴࡨࡨࠥࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡦࡰࡴࡹࡥࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࡾࢁࠬണ").format(str(e)))
def bstack1ll1l11ll_opy_(self, name, *args):
  global bstack11l1lll1_opy_
  global bstack11lll11l1_opy_
  try:
    if BROWSERSTACK_AUTOMATION:
      platform_index = int(threading.current_thread()._name) % bstack1ll1l111l_opy_
      bstack111l1l1ll1_opy_ = CONFIG[bstack1ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧത")][platform_index]
      os.environ[bstack1ll111_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭ഥ")] = json.dumps(bstack111l1l1ll1_opy_)
    if not hasattr(self, bstack1ll111_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡧࡧࠫദ")):
      self.driver_initialised = None
    bstack1l1111ll11_opy_ = {
        bstack1ll111_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠫധ"): bstack11111ll11_opy_,
        bstack1ll111_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠩന"): bstack1ll11l111_opy_,
        bstack1ll111_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡷࡥ࡬࠭ഩ"): bstack1llll1ll1_opy_,
        bstack1ll111_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬപ"): bstack1l1lll111l_opy_,
        bstack1ll111_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠩഫ"): bstack1l1lll11_opy_,
        bstack1ll111_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡺࡥࡱࠩബ"): bstack1l1111111l_opy_,
        bstack1ll111_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧഭ"): bstack11llllllll_opy_,
        bstack1ll111_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡴࡢࡩࠪമ"): bstack11ll1l111_opy_,
        bstack1ll111_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨയ"): bstack11llll1ll1_opy_,
        bstack1ll111_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠬര"): bstack1ll1l11l_opy_
    }
    handler = bstack1l1111ll11_opy_.get(name, bstack11l1lll1_opy_)
    try:
      if args:
        context = args[0]
        remaining_args = args[1:]
        if bstack11lll11l1_opy_ is None or not bstack11lll11l1_opy_:
          context = self.context
          remaining_args = args
      else:
        context = self.context
        remaining_args = ()
      handler(self, name, context, bstack11l1lll1_opy_, *remaining_args)
    except Exception as e:
      logger.debug(bstack1ll111_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡨࡥࡩࡣࡹࡩࠥ࡮࡯ࡰ࡭ࠣ࡬ࡦࡴࡤ࡭ࡧࡵࠤࢀࢃ࠺ࠡࡽࢀࠫറ").format(name, str(e)))
    if name == bstack1ll111_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬല"):
      _execute_deferred_playwright_close()
    if name in [bstack1ll111_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬള"), bstack1ll111_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧഴ"), bstack1ll111_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪവ")]:
      try:
        bstack11l11l11_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll1ll1ll_opy_(bstack1ll111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧശ")) else context.browser
        bstack1l111l1ll_opy_ = (
          (name == bstack1ll111_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠬഷ") and self.driver_initialised == bstack1ll111_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢസ")) or
          (name == bstack1ll111_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫഹ") and self.driver_initialised == bstack1ll111_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨഺ")) or
          (name == bstack1ll111_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵ഻ࠧ") and self.driver_initialised in [bstack1ll111_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤ഼"), bstack1ll111_opy_ (u"ࠣ࡫ࡱࡷࡹ࡫ࡰࠣഽ")]) or
          (name == bstack1ll111_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡷࡩࡵ࠭ാ") and self.driver_initialised == bstack1ll111_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣി"))
        )
        if bstack1l111l1ll_opy_:
          self.driver_initialised = None
          if bstack11l11l11_opy_ and hasattr(bstack11l11l11_opy_, bstack1ll111_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨീ")):
            try:
              bstack11l11l11_opy_.quit()
            except Exception as e:
              logger.debug(bstack1ll111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡶࡻࡩࡵࡶ࡬ࡲ࡬ࠦࡤࡳ࡫ࡹࡩࡷࠦࡩ࡯ࠢࡥࡩ࡭ࡧࡶࡦࠢ࡫ࡳࡴࡱ࠺ࠡࡽࢀࠫു").format(str(e)))
      except Exception as e:
        logger.debug(bstack1ll111_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡣࡩࡸࡪࡸࠠࡩࡱࡲ࡯ࠥࡩ࡬ࡦࡣࡱࡹࡵࠦࡦࡰࡴࠣࡿࢂࡀࠠࡼࡿࠪൂ").format(name, str(e)))
  except Exception as e:
    logger.debug(bstack1ll111_opy_ (u"ࠧࡄࡴ࡬ࡸ࡮ࡩࡡ࡭ࠢࡨࡶࡷࡵࡲࠡ࡫ࡱࠤࡧ࡫ࡨࡢࡸࡨࠤࡷࡻ࡮ࠡࡪࡲࡳࡰࠦࡻࡾ࠼ࠣࡿࢂ࠭ൃ").format(name, str(e)))
    try:
      if bstack11lll11l1_opy_ is None or bstack11lll11l1_opy_:
        try:
          bstack11l1lll1_opy_(self, name, self.context, *args)
        except TypeError:
          bstack11l1lll1_opy_(self, name, *args)
      else:
        bstack11l1lll1_opy_(self, name, *args)
    except Exception as e2:
      logger.debug(bstack1ll111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡵࡲࡪࡩ࡬ࡲࡦࡲࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡩࡱࡲ࡯ࠥࢁࡽ࠻ࠢࡾࢁࠬൄ").format(name, str(e2)))
  finally:
    if name == bstack1ll111_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ൅"):
      _execute_deferred_playwright_close()
def bstack1ll11ll1_opy_(config, startdir):
  return bstack1ll111_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀ࠶ࡽࠣെ").format(bstack1ll111_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥേ"))
notset = Notset()
def bstack1lll1ll111_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1l11l11l1_opy_
  if str(name).lower() == bstack1ll111_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࠬൈ"):
    return bstack1ll111_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧ൉")
  else:
    return bstack1l11l11l1_opy_(self, name, default, skip)
def bstack1l1llll1_opy_(item, when):
  global bstack1l1llll1ll_opy_
  try:
    bstack1l1llll1ll_opy_(item, when)
  except Exception as e:
    pass
def bstack11ll111ll1_opy_():
  return
def browserstack_executor_helper(type, name, status, reason, bstack1lll1llll_opy_, bstack1ll1l1l11_opy_):
  bstack11lll1111l_opy_ = {
    bstack1ll111_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧൊ"): type,
    bstack1ll111_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫോ"): {}
  }
  if type == bstack1ll111_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫൌ"):
    bstack11lll1111l_opy_[bstack1ll111_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ്࠭")][bstack1ll111_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪൎ")] = bstack1lll1llll_opy_
    bstack11lll1111l_opy_[bstack1ll111_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ൏")][bstack1ll111_opy_ (u"࠭ࡤࡢࡶࡤࠫ൐")] = json.dumps(str(bstack1ll1l1l11_opy_))
  if type == bstack1ll111_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ൑"):
    bstack11lll1111l_opy_[bstack1ll111_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ൒")][bstack1ll111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ൓")] = name
  if type == bstack1ll111_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ൔ"):
    bstack11lll1111l_opy_[bstack1ll111_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧൕ")][bstack1ll111_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬൖ")] = status
    if status == bstack1ll111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ൗ"):
      bstack11lll1111l_opy_[bstack1ll111_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ൘")][bstack1ll111_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨ൙")] = json.dumps(str(reason))
  bstack111l111l11_opy_ = bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧ൚").format(json.dumps(bstack11lll1111l_opy_))
  return bstack111l111l11_opy_
def bstack11l11lll11_opy_(driver_command, response):
    if driver_command == bstack1ll111_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧ൛"):
        TestHubHandler.bstack11ll11111l_opy_({
            bstack1ll111_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪ൜"): response[bstack1ll111_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫ൝")],
            bstack1ll111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭൞"): TestHubHandler.current_test_uuid()
        })
def bstack11l111ll11_opy_(item, call, rep):
  global bstack1l1ll1ll1_opy_
  global bstack1l111lll11_opy_
  global bstack11111l111_opy_
  name = bstack1ll111_opy_ (u"ࠧࠨൟ")
  try:
    if rep.when == bstack1ll111_opy_ (u"ࠨࡥࡤࡰࡱ࠭ൠ"):
      bstack1l11111l_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack11111l111_opy_:
          name = str(rep.nodeid)
          executor_string = browserstack_executor_helper(bstack1ll111_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪൡ"), name, bstack1ll111_opy_ (u"ࠪࠫൢ"), bstack1ll111_opy_ (u"ࠫࠬൣ"), bstack1ll111_opy_ (u"ࠬ࠭൤"), bstack1ll111_opy_ (u"࠭ࠧ൥"))
          threading.current_thread().bstack111l11l111_opy_ = name
          for driver in bstack1l111lll11_opy_:
            if bstack1l11111l_opy_ == driver.session_id:
              driver.execute_script(executor_string)
      except Exception as e:
        logger.debug(bstack1ll111_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧ൦").format(str(e)))
      try:
        bstack1l1111l1l1_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack1ll111_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ൧"):
          status = bstack1ll111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ൨") if rep.outcome.lower() == bstack1ll111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ൩") else bstack1ll111_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ൪")
          reason = bstack1ll111_opy_ (u"ࠬ࠭൫")
          if status == bstack1ll111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭൬"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack1ll111_opy_ (u"ࠧࡪࡰࡩࡳࠬ൭") if status == bstack1ll111_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ൮") else bstack1ll111_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ൯")
          data = name + bstack1ll111_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬ൰") if status == bstack1ll111_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ൱") else name + bstack1ll111_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩࠧࠠࠨ൲") + reason
          bstack1lll1lllll_opy_ = browserstack_executor_helper(bstack1ll111_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨ൳"), bstack1ll111_opy_ (u"ࠧࠨ൴"), bstack1ll111_opy_ (u"ࠨࠩ൵"), bstack1ll111_opy_ (u"ࠩࠪ൶"), level, data)
          for driver in bstack1l111lll11_opy_:
            if bstack1l11111l_opy_ == driver.session_id:
              driver.execute_script(bstack1lll1lllll_opy_)
      except Exception as e:
        logger.debug(bstack1ll111_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡤࡱࡱࡸࡪࡾࡴࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧ൷").format(str(e)))
  except Exception as e:
    logger.debug(bstack1ll111_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡶࡤࡸࡪࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁࡽࠨ൸").format(str(e)))
  bstack1l1ll1ll1_opy_(item, call, rep)
def bstack1l1ll1111_opy_(driver, bstack1l111ll1ll_opy_, test=None):
  global PLATFORM_INDEX
  if test != None:
    bstack1llll11l1_opy_ = getattr(test, bstack1ll111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ൹"), None)
    bstack1ll11l1ll1_opy_ = getattr(test, bstack1ll111_opy_ (u"࠭ࡵࡶ࡫ࡧࠫൺ"), None)
    PercySDK.screenshot(driver, bstack1l111ll1ll_opy_, bstack1llll11l1_opy_=bstack1llll11l1_opy_, bstack1ll11l1ll1_opy_=bstack1ll11l1ll1_opy_, bstack1llll11111_opy_=PLATFORM_INDEX)
  else:
    PercySDK.screenshot(driver, bstack1l111ll1ll_opy_)
@measure(event_name=EVENTS.bstack111ll111ll_opy_, stage=STAGE.bstack11ll1111_opy_, bstack11l11l111_opy_=SESSION_NAME)
def bstack1l11l1111_opy_(driver):
  if bstack1lll111ll1_opy_.bstack11lll111_opy_() is True or bstack1lll111ll1_opy_.capturing() is True:
    return
  bstack1lll111ll1_opy_.bstack1111l111l1_opy_()
  while not bstack1lll111ll1_opy_.bstack11lll111_opy_():
    bstack1l1l11ll1_opy_ = bstack1lll111ll1_opy_.bstack11ll1111l_opy_()
    bstack1l1ll1111_opy_(driver, bstack1l1l11ll1_opy_)
  bstack1lll111ll1_opy_.bstack1lll1l1l1l_opy_()
def bstack111ll1ll_opy_(sequence, driver_command, response = None, bstack1l11ll1l1l_opy_ = None, args = None):
    try:
      if sequence != bstack1ll111_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧൻ"):
        return
      if percy.bstack1ll1l1l1l_opy_() == bstack1ll111_opy_ (u"ࠣࡨࡤࡰࡸ࡫ࠢർ"):
        return
      bstack1l1l11ll1_opy_ = bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠩࡳࡩࡷࡩࡹࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬൽ"), None)
      for command in bstack1111lll1l_opy_:
        if command == driver_command:
          with bstack11llll1ll_opy_:
            bstack1ll1l1l1_opy_ = bstack1l111lll11_opy_.copy()
          for driver in bstack1ll1l1l1_opy_:
            bstack1l11l1111_opy_(driver)
      bstack1l111111l_opy_ = percy.bstack1ll11l111l_opy_()
      if driver_command in bstack1l111l1lll_opy_[bstack1l111111l_opy_]:
        bstack1lll111ll1_opy_.bstack1ll1l1lll_opy_(bstack1l1l11ll1_opy_, driver_command)
    except Exception as e:
      pass
_1ll1lll11l_opy_ = threading.Event()
def bstack111lll11ll_opy_(framework_name):
  if global_config.get_property(bstack1ll111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡱࡴࡪ࡟ࡤࡣ࡯ࡰࡪࡪࠧൾ")):
      _1ll1lll11l_opy_.wait(timeout=30)
      return
  global_config.bstack1lll11l111_opy_(bstack1ll111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨൿ"), True)
  global FRAMEWORK_NAME
  global SELENIUM_OR_PLAYWRIGHT_INSTALLED
  global bstack111l1l11l_opy_
  FRAMEWORK_NAME = framework_name
  logger.info(bstack11111l1l1_opy_.format(FRAMEWORK_NAME.split(bstack1ll111_opy_ (u"ࠬ࠳ࠧ඀"))[0]))
  bstack11l1ll1l1l_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    global bstack1ll1111l1l_opy_
    bstack1l1ll111ll_opy_ = BROWSERSTACK_AUTOMATION or bstack1ll1111l1l_opy_
    if bstack1l1ll111ll_opy_:
      Service.start = bstack11lll111ll_opy_
      Service.stop = bstack1l11l1ll11_opy_
      webdriver.Remote.get = bstack1111ll11l1_opy_
      WebDriver.quit = bstack1l11l111ll_opy_
      webdriver.Remote.__init__ = bstack11l1l11l1_opy_
    if not BROWSERSTACK_AUTOMATION and not bstack1ll1111l1l_opy_:
        webdriver.Remote.__init__ = bstack1ll111llll_opy_
    WebDriver.getAccessibilityResults = getAccessibilityResults
    WebDriver.get_accessibility_results = getAccessibilityResults
    WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
    WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
    WebDriver.performScan = perform_scan
    WebDriver.perform_scan = perform_scan
    WebDriver.execute = bstack1llllllll_opy_
    SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
  except Exception as e:
    pass
  try:
    bstack1l1ll111ll_opy_ = BROWSERSTACK_AUTOMATION or bstack1ll1111l1l_opy_
    if bstack1l1ll111ll_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack11ll11l1l_opy_
  except Exception as e:
    pass
  try:
    import sys as _sys
    _1ll1ll1l1l_opy_ = _sys.modules[bstack1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡹࡤ࡬࠰ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ඁ")]
    _1ll1ll1l1l_opy_.set_playwright_globals(
        CONFIG=CONFIG,
        FRAMEWORK_NAME=FRAMEWORK_NAME,
        PLATFORM_INDEX=PLATFORM_INDEX,
        SESSION_NAME=SESSION_NAME,
        PARALLELISE_VANILLA_PYTHON=PARALLELISE_VANILLA_PYTHON,
        PARALLELISE_THREADING_PYTHON=PARALLELISE_THREADING_PYTHON,
        __version__=__version__,
        TestHubUtils=TestHubUtils,
        get_caps=get_caps,
        update_caps_for_local=update_caps_for_local,
        logger=logger,
        CONFIG_FILE_CONTENT=CONFIG_FILE_CONTENT,
        BROWSERSTACK_AUTOMATION=BROWSERSTACK_AUTOMATION,
        SELENIUM_OR_PLAYWRIGHT_INSTALLED=SELENIUM_OR_PLAYWRIGHT_INSTALLED,
        global_config=global_config,
        get_turboscale_playwright_url=get_turboscale_playwright_url,
        os=os,
        threading=threading,
        multiprocessing=multiprocessing,
        json=json,
        traceback=traceback,
    )
  except Exception as e:
    logger.debug(bstack1ll111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤ࡬ࡲ࡯ࡣࡣ࡯ࡷ࠿ࠦࡻࡾࠤං").format(str(e)))
  patch_playwright()
  if not SELENIUM_OR_PLAYWRIGHT_INSTALLED:
    bstack1l1ll1l1_opy_(bstack1ll111_opy_ (u"ࠣࡒࡤࡧࡰࡧࡧࡦࡵࠣࡲࡴࡺࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠥඃ"), bstack1111ll11ll_opy_)
  if bstack1111l1l11l_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      if hasattr(RemoteConnection, bstack1ll111_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪ඄")) and callable(getattr(RemoteConnection, bstack1ll111_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫඅ"))):
        RemoteConnection._get_proxy_url = bstack111lllll_opy_
      else:
        from selenium.webdriver.remote.client_config import ClientConfig
        ClientConfig.get_proxy_url = bstack111lllll_opy_
    except Exception as e:
      logger.error(bstack11l11l1l_opy_.format(str(e)))
  if bstack11l1lllll_opy_():
    bstack11l11ll11l_opy_(CONFIG, logger)
  if (bstack1ll111_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪආ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      try:
        from pabot.pabot import QueueItem
        from pabot import pabot
      except Exception as e:
        logger.warning(bstack1lllllll11_opy_ + str(e))
      if not is_robot_playwright_installed():
        try:
          if percy.bstack1ll1l1l1l_opy_() == bstack1ll111_opy_ (u"ࠧࡺࡲࡶࡧࠥඇ"):
            bstack1lll1l1ll_opy_(bstack111ll1ll_opy_)
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
          WebDriverCreator._get_ff_profile = bstack1llll111l_opy_
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
          WebDriverCache.close = bstack111l11l1_opy_
        except Exception as e:
          logger.warning(bstack1llll111ll_opy_ + str(e))
        try:
          from AppiumLibrary.utils.applicationcache import ApplicationCache
          ApplicationCache.close = bstack1lll11llll_opy_
        except Exception as e:
          logger.debug(bstack1llll11l1l_opy_ + str(e))
    except Exception as e:
      bstack1l1ll1l1_opy_(e, bstack1llll111ll_opy_)
    Output.start_test = bstack1lllll111_opy_
    Output.end_test = bstack1ll11llll_opy_
    TestStatus.__init__ = bstack111l1l11ll_opy_
    QueueItem.__init__ = bstack11l1l111l_opy_
    pabot._create_items = bstack1lllllll1_opy_
    try:
      from pabot import __version__ as bstack1lllll11ll_opy_
      if version.parse(bstack1lllll11ll_opy_) >= version.parse(bstack1ll111_opy_ (u"࠭࠵࠯࠲࠱࠴ࠬඈ")):
        pabot._run = bstack11l11llll_opy_
      elif version.parse(bstack1lllll11ll_opy_) >= version.parse(bstack1ll111_opy_ (u"ࠧ࠵࠰࠵࠲࠵࠭ඉ")):
        pabot._run = bstack1llll1ll1l_opy_
      elif version.parse(bstack1lllll11ll_opy_) >= version.parse(bstack1ll111_opy_ (u"ࠨ࠴࠱࠵࠺࠴࠰ࠨඊ")):
        pabot._run = bstack11111lll1_opy_
      elif version.parse(bstack1lllll11ll_opy_) >= version.parse(bstack1ll111_opy_ (u"ࠩ࠵࠲࠶࠹࠮࠱ࠩඋ")):
        pabot._run = bstack1lll11l1l1_opy_
      else:
        pabot._run = bstack1l1llll11_opy_
    except Exception as e:
      pabot._run = bstack1l1llll11_opy_
    pabot._create_command_for_execution = bstack1111ll1l11_opy_
    pabot._report_results = bstack1llll1l1ll_opy_
  if bstack1ll111_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪඌ") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l1ll1l1_opy_(e, bstack1l1l1ll11l_opy_)
    Runner.run_hook = bstack1ll1l11ll_opy_
    try:
      from behave import __version__ as bstack111l111111_opy_
      if version.parse(bstack111l111111_opy_) >= version.parse(bstack1ll111_opy_ (u"ࠫ࠶࠴࠳࠯࠲ࠪඍ")):
        Runner.load_hooks = bstack1lll11l1ll_opy_
    except Exception as e:
      logger.debug(bstack1ll111_opy_ (u"ࠬࡉ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤࡧ࡫ࡨࡢࡸࡨࠤࡻ࡫ࡲࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩඎ").format(str(e)))
    Step.run = bstack1ll1lllll1_opy_
  if bstack1ll111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ඏ") in str(framework_name).lower():
    if not BROWSERSTACK_AUTOMATION:
      _1ll1lll11l_opy_.set()
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack1ll11ll1_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack11ll111ll1_opy_
      Config.getoption = bstack1lll1ll111_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack11l111ll11_opy_
    except Exception as e:
      pass
  _1ll1lll11l_opy_.set()
def bstack1l11ll111_opy_():
  global CONFIG
  if bstack1ll111_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧඐ") in CONFIG and int(CONFIG[bstack1ll111_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨඑ")]) > 1:
    logger.warning(bstack1lll11111l_opy_)
def bstack1l11l1lll1_opy_(arg, bstack1l11l1l1ll_opy_, bstack111l1lll1_opy_=None):
  global CONFIG
  global bstack1l1l11lll_opy_
  global bstack11l1l1l1_opy_
  global BROWSERSTACK_AUTOMATION
  global bstack1ll1111l1l_opy_
  global global_config
  bstack11l11lll_opy_ = bstack1ll111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩඒ")
  if bstack1l11l1l1ll_opy_ and isinstance(bstack1l11l1l1ll_opy_, str):
    bstack1l11l1l1ll_opy_ = eval(bstack1l11l1l1ll_opy_)
  CONFIG = bstack1l11l1l1ll_opy_[bstack1ll111_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪඓ")]
  bstack1l1l11lll_opy_ = bstack1l11l1l1ll_opy_[bstack1ll111_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬඔ")]
  bstack11l1l1l1_opy_ = bstack1l11l1l1ll_opy_[bstack1ll111_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧඕ")]
  BROWSERSTACK_AUTOMATION = bstack1l11l1l1ll_opy_[bstack1ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩඖ")]
  try:
    bstack111ll1l1l_opy_ = bstack1l11l1l1ll_opy_.get(bstack1ll111_opy_ (u"ࠧࡐࡘࡈࡖࡗࡏࡄࡆࡡࡏࡓࡆࡊ࡟ࡕࡇࡖࡘࡎࡔࡇࠨ඗"), False)
    bstack1ll1111l1l_opy_ = bool(bstack111ll1l1l_opy_)
    os.environ[bstack1ll111_opy_ (u"ࠨࡑ࡙ࡉࡗࡘࡉࡅࡇࡢࡐࡔࡇࡄࡠࡖࡈࡗ࡙ࡏࡎࡈࠩ඘")] = str(bstack1ll1111l1l_opy_).lower()
  except Exception as e:
    logger.error(bstack1ll111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡏࡗࡇࡕࡖࡎࡊࡅࡠࡎࡒࡅࡉࡥࡔࡆࡕࡗࡍࡓࡍ࠺ࠡࡽࢀࠦ඙").format(e))
    bstack1ll1111l1l_opy_ = False
    os.environ[bstack1ll111_opy_ (u"ࠪࡓ࡛ࡋࡒࡓࡋࡇࡉࡤࡒࡏࡂࡆࡢࡘࡊ࡙ࡔࡊࡐࡊࠫක")] = bstack1ll111_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪඛ")
  global_config.bstack1lll11l111_opy_(bstack1ll111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ග"), BROWSERSTACK_AUTOMATION)
  os.environ[bstack1ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨඝ")] = bstack11l11lll_opy_
  os.environ[bstack1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌ࠭ඞ")] = json.dumps(CONFIG)
  os.environ[bstack1ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡉࡗࡅࡣ࡚ࡘࡌࠨඟ")] = bstack1l1l11lll_opy_
  os.environ[bstack1ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪච")] = str(bstack11l1l1l1_opy_)
  os.environ[bstack1ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡐ࡚ࡍࡉࡏࠩඡ")] = str(True)
  if bstack1lll11ll1_opy_(arg, [bstack1ll111_opy_ (u"ࠫ࠲ࡴࠧජ"), bstack1ll111_opy_ (u"ࠬ࠳࠭࡯ࡷࡰࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ඣ")]) != -1:
    os.environ[bstack1ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡁࡓࡃࡏࡐࡊࡒࠧඤ")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack111lll111_opy_)
    return
  bstack11l111111l_opy_()
  global bstack111ll1l1l1_opy_
  global PLATFORM_INDEX
  global bstack11l111ll1l_opy_
  global bstack11lll1l111_opy_
  global bstack1llll11ll_opy_
  global bstack111l1l11l_opy_
  global PARALLELISE_VANILLA_PYTHON
  arg.append(bstack1ll111_opy_ (u"ࠢ࠮࡙ࠥඥ"))
  arg.append(bstack1ll111_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡥ࠻ࡏࡲࡨࡺࡲࡥࠡࡣ࡯ࡶࡪࡧࡤࡺࠢ࡬ࡱࡵࡵࡲࡵࡧࡧ࠾ࡵࡿࡴࡦࡵࡷ࠲ࡕࡿࡴࡦࡵࡷ࡛ࡦࡸ࡮ࡪࡰࡪࠦඦ"))
  arg.append(bstack1ll111_opy_ (u"ࠤ࠰࡛ࠧට"))
  arg.append(bstack1ll111_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧ࠽ࡘ࡭࡫ࠠࡩࡱࡲ࡯࡮ࡳࡰ࡭ࠤඨ"))
  global bstack1111lllll1_opy_
  global bstack1l11ll11l_opy_
  global bstack1lll11lll1_opy_
  global bstack1llll111l1_opy_
  global bstack11l1ll1l11_opy_
  global bstack1l111l11l1_opy_
  global bstack1ll1ll11l1_opy_
  global bstack1l1l1lllll_opy_
  global bstack11l1ll11l_opy_
  global bstack1ll1ll11l_opy_
  global bstack1l11l11l1_opy_
  global bstack1l1llll1ll_opy_
  global bstack1l1ll1ll1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1111lllll1_opy_ = webdriver.Remote.__init__
    bstack1l11ll11l_opy_ = WebDriver.quit
    bstack1l1l1lllll_opy_ = WebDriver.close
    bstack11l1ll11l_opy_ = WebDriver.get
    bstack1lll11lll1_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1lll1ll1l_opy_(CONFIG) and bstack11ll1ll11l_opy_():
    if bstack11l1l1l11_opy_() < version.parse(bstack1l11l11l1l_opy_):
      logger.error(bstack11l11111l1_opy_.format(bstack11l1l1l11_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack1ll111_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬඩ")) and callable(getattr(RemoteConnection, bstack1ll111_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭ඪ"))):
          bstack1ll1ll11l_opy_ = RemoteConnection._get_proxy_url
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          bstack1ll1ll11l_opy_ = ClientConfig.get_proxy_url
      except Exception as e:
        logger.error(bstack11l11l1l_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1l11l11l1_opy_ = Config.getoption
    from _pytest import runner
    bstack1l1llll1ll_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warning(bstack1ll111_opy_ (u"ࠨࠥࡴ࠼ࠣࠩࡸࠨණ"), bstack1l1ll11l_opy_, str(e))
  try:
    from pytest_bdd import reporting
    bstack1l1ll1ll1_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack1ll111_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨඬ"))
  if cli.is_enabled(CONFIG) and cli.config:
    bstack11l111ll1l_opy_ = cli.config.get(bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬත"), {}).get(bstack1ll111_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫථ"))
  else:
    bstack11l111ll1l_opy_ = CONFIG.get(bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧද"), {}).get(bstack1ll111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ධ"))
  PARALLELISE_VANILLA_PYTHON = True
  if cli.is_enabled(CONFIG):
    if cli.bstack111ll1l1_opy_():
      bstack1lll11111_opy_.invoke(Events.CONNECT, bstack1lll1111_opy_())
    platform_index = int(os.environ.get(bstack1ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬන"), bstack1ll111_opy_ (u"࠭࠰ࠨ඲")))
  else:
    bstack111lll11ll_opy_(bstack1l111l1l1_opy_)
  os.environ[bstack1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨඳ")] = CONFIG[bstack1ll111_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪප")]
  os.environ[bstack1ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬඵ")] = CONFIG[bstack1ll111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭බ")]
  os.environ[bstack1ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧභ")] = BROWSERSTACK_AUTOMATION.__str__()
  from _pytest.config import main as bstack1lll11lll_opy_
  bstack1111l1ll_opy_ = []
  try:
    exit_code = bstack1lll11lll_opy_(arg)
    if cli.is_enabled(CONFIG):
      cli.bstack1l11lllll_opy_()
    if bstack1ll111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩම") in multiprocessing.current_process().__dict__.keys():
      for bstack1l111l1111_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1111l1ll_opy_.append(bstack1l111l1111_opy_)
    try:
      bstack1l11111ll_opy_ = (bstack1111l1ll_opy_, int(exit_code))
      bstack111l1lll1_opy_.append(bstack1l11111ll_opy_)
    except:
      bstack111l1lll1_opy_.append((bstack1111l1ll_opy_, exit_code))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack1111l1ll_opy_.append({bstack1ll111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫඹ"): bstack1ll111_opy_ (u"ࠧࡑࡴࡲࡧࡪࡹࡳࠡࠩය") + os.environ.get(bstack1ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨර")), bstack1ll111_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ඼"): traceback.format_exc(), bstack1ll111_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩල"): int(os.environ.get(bstack1ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ඾")))})
    bstack111l1lll1_opy_.append((bstack1111l1ll_opy_, 1))
def mod_behave_main(args, retries):
  try:
    from behave.configuration import Configuration
    from behave.__main__ import run_behave
    from browserstack_sdk.bstack_behave_runner import BehaveRunner
    config = Configuration(args)
    config.update_userdata({bstack1ll111_opy_ (u"ࠧࡸࡥࡵࡴ࡬ࡩࡸࠨ඿"): str(retries)})
    return run_behave(config, runner_class=BehaveRunner)
  except Exception as e:
    bstack1l1llll11l_opy_ = e.__class__.__name__
    print(bstack1ll111_opy_ (u"ࠨࠥࡴ࠼ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡦࡪ࡮ࡡࡷࡧࠣࡸࡪࡹࡴࠡࠧࡶࠦව") % (bstack1l1llll11l_opy_, e))
    return 1
def bstack1111llll1l_opy_(arg):
  global bstack11llllll_opy_
  bstack111lll11ll_opy_(bstack1l1ll1l111_opy_)
  os.environ[bstack1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨශ")] = str(bstack11l1l1l1_opy_)
  retries = bstack1l1ll111l_opy_.bstack1l1l11ll1l_opy_(CONFIG)
  status_code = 0
  if bstack1l1ll111l_opy_.bstack1lll11l11_opy_(CONFIG):
    status_code = mod_behave_main(arg, retries)
  else:
    from behave.__main__ import main as bstack111l1ll1_opy_
    status_code = bstack111l1ll1_opy_(arg)
  if status_code != 0:
    bstack11llllll_opy_ = status_code
def bstack1ll1ll1111_opy_():
  logger.info(bstack1l1lll1ll1_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1ll111_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧෂ"), help=bstack1ll111_opy_ (u"ࠩࡊࡩࡳ࡫ࡲࡢࡶࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡧࡴࡴࡦࡪࡩࠪස"))
  parser.add_argument(bstack1ll111_opy_ (u"ࠪ࠱ࡺ࠭හ"), bstack1ll111_opy_ (u"ࠫ࠲࠳ࡵࡴࡧࡵࡲࡦࡳࡥࠨළ"), help=bstack1ll111_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫෆ"))
  parser.add_argument(bstack1ll111_opy_ (u"࠭࠭࡬ࠩ෇"), bstack1ll111_opy_ (u"ࠧ࠮࠯࡮ࡩࡾ࠭෈"), help=bstack1ll111_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡧࡣࡤࡧࡶࡷࠥࡱࡥࡺࠩ෉"))
  parser.add_argument(bstack1ll111_opy_ (u"ࠩ࠰ࡪ්ࠬ"), bstack1ll111_opy_ (u"ࠪ࠱࠲࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ෋"), help=bstack1ll111_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ෌"))
  bstack11l111lll1_opy_ = parser.parse_args()
  try:
    bstack1l1llll111_opy_ = bstack1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡬࡫࡮ࡦࡴ࡬ࡧ࠳ࡿ࡭࡭࠰ࡶࡥࡲࡶ࡬ࡦࠩ෍")
    if bstack11l111lll1_opy_.framework and bstack11l111lll1_opy_.framework not in (bstack1ll111_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭෎"), bstack1ll111_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨා")):
      bstack1l1llll111_opy_ = bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࠱ࡽࡲࡲ࠮ࡴࡣࡰࡴࡱ࡫ࠧැ")
    bstack1ll1l1ll11_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l1llll111_opy_)
    bstack1l1l11ll_opy_ = open(bstack1ll1l1ll11_opy_, bstack1ll111_opy_ (u"ࠩࡵࠫෑ"))
    bstack11l1ll1ll_opy_ = bstack1l1l11ll_opy_.read()
    bstack1l1l11ll_opy_.close()
    if bstack11l111lll1_opy_.username:
      bstack11l1ll1ll_opy_ = bstack11l1ll1ll_opy_.replace(bstack1ll111_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪි"), bstack11l111lll1_opy_.username)
    if bstack11l111lll1_opy_.key:
      bstack11l1ll1ll_opy_ = bstack11l1ll1ll_opy_.replace(bstack1ll111_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭ී"), bstack11l111lll1_opy_.key)
    if bstack11l111lll1_opy_.framework:
      bstack11l1ll1ll_opy_ = bstack11l1ll1ll_opy_.replace(bstack1ll111_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ු"), bstack11l111lll1_opy_.framework)
    file_name = bstack1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩ෕")
    file_path = os.path.abspath(file_name)
    bstack1lll1lll_opy_ = open(file_path, bstack1ll111_opy_ (u"ࠧࡸࠩූ"))
    bstack1lll1lll_opy_.write(bstack11l1ll1ll_opy_)
    bstack1lll1lll_opy_.close()
    logger.info(bstack1l11l1ll1l_opy_)
    try:
      os.environ[bstack1ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪ෗")] = bstack11l111lll1_opy_.framework if bstack11l111lll1_opy_.framework != None else bstack1ll111_opy_ (u"ࠤࠥෘ")
      config = yaml.safe_load(bstack11l1ll1ll_opy_)
      config[bstack1ll111_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪෙ")] = bstack1ll111_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱ࡸ࡫ࡴࡶࡲࠪේ")
      bstack11lllllll1_opy_(bstack11ll1lll11_opy_, config)
    except Exception as e:
      logger.debug(bstack1llll1l11l_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack11l1l1l1l1_opy_.format(str(e)))
def bstack11lllllll1_opy_(bstack11l1l1l11l_opy_, config, bstack1l1l1llll1_opy_=None, bstack1l1l1l1111_opy_=False):
  global BROWSERSTACK_AUTOMATION
  global bstack1l11111l11_opy_
  global global_config
  if not config:
    return
  if bstack1l1l1llll1_opy_ is None:
    bstack1l1l1llll1_opy_ = {}
  bstack111lllll1_opy_ = bstack111ll1llll_opy_ if not BROWSERSTACK_AUTOMATION else (
    bstack1ll1ll1l1_opy_ if bstack1ll111_opy_ (u"ࠬࡧࡰࡱࠩෛ") in config else (
        bstack1l11l11ll_opy_ if config.get(bstack1ll111_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪො")) else bstack11ll1ll1l_opy_
    )
)
  bstack1l1lll1l_opy_ = False
  bstack11ll1l11_opy_ = False
  if BROWSERSTACK_AUTOMATION is True:
      if bstack1ll111_opy_ (u"ࠧࡢࡲࡳࠫෝ") in config:
          bstack1l1lll1l_opy_ = True
      else:
          bstack11ll1l11_opy_ = True
  bstack1ll11l1l11_opy_ = TestHubUtils.bstack1111llll11_opy_(config, bstack1l11111l11_opy_)
  bstack111l1111l_opy_ = bstack1lll11ll_opy_()
  data = {
    bstack1ll111_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪෞ"): config[bstack1ll111_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫෟ")],
    bstack1ll111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭෠"): config[bstack1ll111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ෡")],
    bstack1ll111_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ෢"): bstack11l1l1l11l_opy_,
    bstack1ll111_opy_ (u"࠭ࡤࡦࡶࡨࡧࡹ࡫ࡤࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ෣"): os.environ.get(bstack1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩ෤"), bstack1l11111l11_opy_),
    bstack1ll111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ෥"): bstack11l1l11l1l_opy_,
    bstack1ll111_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯ࠫ෦"): bstack1l1lll11ll_opy_(),
    bstack1ll111_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭෧"): {
      bstack1ll111_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ෨"): str(config[bstack1ll111_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ෩")]) if bstack1ll111_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭෪") in config else bstack1ll111_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣ෫"),
      bstack1ll111_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧ࡙ࡩࡷࡹࡩࡰࡰࠪ෬"): sys.version,
      bstack1ll111_opy_ (u"ࠩࡵࡩ࡫࡫ࡲࡳࡧࡵࠫ෭"): bstack111l1l11_opy_(os.environ.get(bstack1ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬ෮"), bstack1l11111l11_opy_)),
      bstack1ll111_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭෯"): bstack1ll111_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ෰"),
      bstack1ll111_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧ෱"): bstack111lllll1_opy_,
      bstack1ll111_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬෲ"): bstack1ll11l1l11_opy_,
      bstack1ll111_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡡࡸࡹ࡮ࡪࠧෳ"): os.environ[bstack1ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ෴")],
      bstack1ll111_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭෵"): os.environ.get(bstack1ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭෶"), bstack1l11111l11_opy_),
      bstack1ll111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ෷"): bstack1lll1l1l11_opy_(os.environ.get(bstack1ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ෸"), bstack1l11111l11_opy_)),
      bstack1ll111_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭෹"): bstack111l1111l_opy_.get(bstack1ll111_opy_ (u"ࠨࡰࡤࡱࡪ࠭෺")),
      bstack1ll111_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ෻"): bstack111l1111l_opy_.get(bstack1ll111_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫ෼")),
      bstack1ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ෽"): config[bstack1ll111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ෾")] if config[bstack1ll111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ෿")] else bstack1ll111_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣ฀"),
      bstack1ll111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪก"): str(config[bstack1ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫข")]) if bstack1ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬฃ") in config else bstack1ll111_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧค"),
      bstack1ll111_opy_ (u"ࠬࡵࡳࠨฅ"): sys.platform,
      bstack1ll111_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨฆ"): socket.gethostname(),
      bstack1ll111_opy_ (u"ࠧࡪࡵࡆࡐࡎࡋ࡮ࡢࡤ࡯ࡩࡩ࠭ง"): bstack1l1l1l1111_opy_,
      bstack1ll111_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪจ"): global_config.get_property(bstack1ll111_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫฉ"))
    }
  }
  if not global_config.get_property(bstack1ll111_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪช")) is None:
    data[bstack1ll111_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧซ")][bstack1ll111_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࡍࡦࡶࡤࡨࡦࡺࡡࠨฌ")] = {
      bstack1ll111_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ญ"): bstack1ll111_opy_ (u"ࠧࡶࡵࡨࡶࡤࡱࡩ࡭࡮ࡨࡨࠬฎ"),
      bstack1ll111_opy_ (u"ࠨࡵ࡬࡫ࡳࡧ࡬ࠨฏ"): global_config.get_property(bstack1ll111_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩฐ")),
      bstack1ll111_opy_ (u"ࠪࡷ࡮࡭࡮ࡢ࡮ࡑࡹࡲࡨࡥࡳࠩฑ"): global_config.get_property(bstack1ll111_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡓࡵࠧฒ"))
    }
  if bstack11l1l1l11l_opy_ == bstack1l1l1l1l11_opy_:
    data[bstack1ll111_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨณ")][bstack1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡈࡵ࡮ࡧ࡫ࡪࠫด")] = bstack1l1ll1ll_opy_(config)
    data[bstack1ll111_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪต")][bstack1ll111_opy_ (u"ࠨ࡫ࡶࡔࡪࡸࡣࡺࡃࡸࡸࡴࡋ࡮ࡢࡤ࡯ࡩࡩ࠭ถ")] = percy.bstack11l1l1l1ll_opy_
    data[bstack1ll111_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬท")][bstack1ll111_opy_ (u"ࠪࡴࡪࡸࡣࡺࡄࡸ࡭ࡱࡪࡉࡥࠩธ")] = percy.percy_build_id
  if not bstack1l1ll111l_opy_.bstack11lll1l1ll_opy_(CONFIG):
    data[bstack1ll111_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧน")][bstack1ll111_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠩบ")] = bstack1l1ll111l_opy_.bstack11lll1l1ll_opy_(CONFIG)
  bstack1111ll1ll1_opy_ = bstack11l11llll1_opy_.get_instance(CONFIG, logger)
  bstack111ll11l_opy_ = bstack1l1ll111l_opy_.get_instance(config=CONFIG)
  if bstack1111ll1ll1_opy_ is not None and bstack111ll11l_opy_ is not None and bstack111ll11l_opy_.bstack11l1ll11ll_opy_():
    data[bstack1ll111_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩป")][bstack111ll11l_opy_.bstack1111lll1l1_opy_()] = bstack1111ll1ll1_opy_.bstack1lll1ll11l_opy_()
  update(data[bstack1ll111_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪผ")], bstack1l1l1llll1_opy_)
  try:
    response = bstack11111l1l_opy_(bstack1ll111_opy_ (u"ࠨࡒࡒࡗ࡙࠭ฝ"), bstack1lll1l11_opy_(bstack1l1l11l11_opy_), data, {
      bstack1ll111_opy_ (u"ࠩࡤࡹࡹ࡮ࠧพ"): (config[bstack1ll111_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬฟ")], config[bstack1ll111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧภ")])
    })
    if response:
      logger.debug(bstack111l1ll111_opy_.format(bstack11l1l1l11l_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1ll111l111_opy_.format(str(e)))
def bstack111l1l11_opy_(framework):
  return bstack1ll111_opy_ (u"ࠧࢁࡽ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࡻࡾࠤม").format(str(framework), __version__) if framework else bstack1ll111_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࢀࢃࠢย").format(
    __version__)
def bstack11l111111l_opy_():
  global CONFIG
  global bstack1ll11ll11_opy_
  if bool(CONFIG):
    return
  try:
    bstack1ll1lll1_opy_()
    logger.debug(bstack11ll11l1ll_opy_.format(str(CONFIG)))
    bstack1ll11ll11_opy_ = logger_utils.configure_logger(CONFIG, bstack1ll11ll11_opy_)
    bstack11l1ll1l1l_opy_()
  except Exception as e:
    logger.error(bstack1ll111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱ࠮ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠦร") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1l1l11l1l1_opy_
  atexit.register(bstack1l1l1lll_opy_)
  signal.signal(signal.SIGINT, bstack11llll1l_opy_)
  signal.signal(signal.SIGTERM, bstack11llll1l_opy_)
def bstack1l1l11l1l1_opy_(exctype, value, traceback):
  global bstack1l111lll11_opy_
  try:
    for driver in bstack1l111lll11_opy_:
      bstack111lll11_opy_(driver, bstack1ll111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨฤ"), bstack1ll111_opy_ (u"ࠤࡖࡩࡸࡹࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧล") + str(value))
  except Exception:
    pass
  logger.info(bstack1llll1llll_opy_)
  bstack1lll1llll1_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1lll1llll1_opy_(message=bstack1ll111_opy_ (u"ࠪࠫฦ"), bstack11l1lllll1_opy_ = False, bstack1l1l1l1111_opy_ = False):
  global CONFIG
  bstack1llll11ll1_opy_ = bstack1ll111_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡉࡽࡩࡥࡱࡶ࡬ࡳࡳ࠭ว") if bstack11l1lllll1_opy_ else bstack1ll111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫศ")
  bstack111ll111_opy_ = bstack111ll11111_opy_.bstack111l11l11_opy_(EVENTS.bstack1ll1111l1_opy_)
  try:
    if message:
      bstack1l1l1llll1_opy_ = {
        bstack1llll11ll1_opy_ : str(message)
      }
      try:
        bstack11lllllll1_opy_(bstack1l1l1l1l11_opy_, CONFIG, bstack1l1l1llll1_opy_, bstack1l1l1l1111_opy_)
      finally:
        bstack111ll11111_opy_.end(EVENTS.bstack1ll1111l1_opy_.value, bstack111ll111_opy_ + bstack1ll111_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨษ"), bstack111ll111_opy_ + bstack1ll111_opy_ (u"ࠢ࠻ࡧࡱࡨࠧส"), status=True, failure=None, test_name=None)
    else:
      try:
        bstack11lllllll1_opy_(bstack1l1l1l1l11_opy_, CONFIG, bstack1l1l1l1111_opy_=bstack1l1l1l1111_opy_)
      finally:
        bstack111ll11111_opy_.end(EVENTS.bstack1ll1111l1_opy_.value, bstack111ll111_opy_ + bstack1ll111_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣห"), bstack111ll111_opy_ + bstack1ll111_opy_ (u"ࠤ࠽ࡩࡳࡪࠢฬ"), status=True, failure=None, test_name=None)
  except Exception as e:
    logger.debug(bstack111l111ll_opy_.format(str(e)))
def bstack1l111ll11l_opy_(bstack1ll111l1l_opy_, size):
  bstack1ll11l1l_opy_ = []
  while len(bstack1ll111l1l_opy_) > size:
    bstack1ll1l11l1l_opy_ = bstack1ll111l1l_opy_[:size]
    bstack1ll11l1l_opy_.append(bstack1ll1l11l1l_opy_)
    bstack1ll111l1l_opy_ = bstack1ll111l1l_opy_[size:]
  bstack1ll11l1l_opy_.append(bstack1ll111l1l_opy_)
  return bstack1ll11l1l_opy_
def bstack1llll1lll1_opy_(args):
  if bstack1ll111_opy_ (u"ࠪ࠱ࡲ࠭อ") in args and bstack1ll111_opy_ (u"ࠫࡵࡪࡢࠨฮ") in args:
    return True
  return False
@measure(event_name=EVENTS.bstack11l11l1l1_opy_, stage=STAGE.bstack11ll11ll1l_opy_)
def run_on_browserstack(bstack1ll1llll_opy_=None, bstack111l1lll1_opy_=None, bstack11ll11l11l_opy_=False):
  global CONFIG
  global bstack1l1l11lll_opy_
  global bstack11l1l1l1_opy_
  global bstack1l11111l11_opy_
  global global_config
  bstack11l11lll_opy_ = bstack1ll111_opy_ (u"ࠬ࠭ฯ")
  bstack111111lll_opy_ = bstack1ll111_opy_ (u"ࠨࠢะ")
  bstack1111ll1l1_opy_(bstack11l111lll_opy_, logger)
  if bstack1ll1llll_opy_ and isinstance(bstack1ll1llll_opy_, str):
    bstack1ll1llll_opy_ = eval(bstack1ll1llll_opy_)
  if bstack1ll1llll_opy_:
    CONFIG = bstack1ll1llll_opy_[bstack1ll111_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧั")]
    bstack1l1l11lll_opy_ = bstack1ll1llll_opy_[bstack1ll111_opy_ (u"ࠨࡊࡘࡆࡤ࡛ࡒࡍࠩา")]
    bstack11l1l1l1_opy_ = bstack1ll1llll_opy_[bstack1ll111_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫำ")]
    global_config.bstack1lll11l111_opy_(bstack1ll111_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬิ"), bstack11l1l1l1_opy_)
    bstack11l11lll_opy_ = bstack1ll111_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠬี")
  global_config.bstack1lll11l111_opy_(bstack1ll111_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪࠧึ"), uuid4().__str__())
  logger.info(bstack1ll111_opy_ (u"࠭ࡓࡅࡍࠣࡶࡺࡴࠠࡴࡶࡤࡶࡹ࡫ࡤࠡࡹ࡬ࡸ࡭ࠦࡩࡥ࠼ࠣࠫื") + global_config.get_property(bstack1ll111_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥุࠩ")));
  logger.debug(bstack1ll111_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࡀูࠫ") + global_config.get_property(bstack1ll111_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧฺࠫ")))
  if not bstack11ll11l11l_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack111lll111_opy_)
      return
    if sys.argv[1] == bstack1ll111_opy_ (u"ࠪ࠱࠲ࡼࡥࡳࡵ࡬ࡳࡳ࠭฻") or sys.argv[1] == bstack1ll111_opy_ (u"ࠫ࠲ࡼࠧ฼"):
      logger.info(bstack1ll111_opy_ (u"ࠬࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡕࡿࡴࡩࡱࡱࠤࡘࡊࡋࠡࡸࡾࢁࠬ฽").format(__version__))
      return
    if sys.argv[1] == bstack1ll111_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ฾"):
      bstack1ll1ll1111_opy_()
      return
    if sys.argv[1] == bstack1ll111_opy_ (u"ࠧ࡭ࡱࡤࡨࠬ฿"):
      from browserstack_sdk.bstack11lll11ll1_opy_ import bstack1ll11llll1_opy_
      bstack11l111111l_opy_()
      bstack1ll11llll1_opy_(CONFIG)
      return
  args = sys.argv
  bstack11l111111l_opy_()
  global bstack1ll1111l1l_opy_
  try:
    from bstack_utils import constants as bstack11llllll11_opy_
    override_value = CONFIG.get(bstack1ll111_opy_ (u"ࠨࡱࡹࡩࡷࡸࡩࡥࡧࡏࡳࡦࡪࡔࡦࡵࡷ࡭ࡳ࡭ࠧเ"), False)
    bstack1ll1111l1l_opy_ = bool(override_value)
  except Exception as e:
    logger.error(bstack1ll111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡏࡗࡇࡕࡖࡎࡊࡅࡠࡎࡒࡅࡉࡥࡔࡆࡕࡗࡍࡓࡍ࠺ࠡࡽࢀࠦแ").format(e))
    bstack1ll1111l1l_opy_ = False
  if bstack1ll1111l1l_opy_:
    bstack11lllll1l1_opy_ = CONFIG.get(bstack1ll111_opy_ (u"ࠪࡰࡴࡧࡤࡕࡧࡶࡸ࡮ࡴࡧࡉࡷࡥ࡙ࡗࡒࠧโ")) or bstack11llllll11_opy_.bstack111l1ll11l_opy_
    logger.info(bstack1ll111_opy_ (u"ࠦࡌࡲ࡯ࡣࡣ࡯ࠤࡴࡼࡥࡳࡴ࡬ࡨࡪࡲ࡯ࡢࡦࡷࡩࡸࡺࡩ࡯ࡩࠣࡩࡳࡧࡢ࡭ࡧࡧ࠰ࠥࡻࡳࡪࡰࡪࠤ࡭ࡻࡢ࠻ࠢࡾࢁࠧใ").format(bstack11lllll1l1_opy_))
    bstack1l1l11lll_opy_ = bstack11lllll1l1_opy_
    try:
      bstack11llllll11_opy_.HTTPS_HUB = bstack11lllll1l1_opy_
      bstack11llllll11_opy_.bstack11l11l11l1_opy_ = bstack11lllll1l1_opy_
    except Exception:
      pass
  global bstack111ll1l1l1_opy_
  global bstack1ll1l111l_opy_
  global PARALLELISE_VANILLA_PYTHON
  global PARALLELISE_THREADING_PYTHON
  global PLATFORM_INDEX
  global bstack11l111ll1l_opy_
  global bstack11lll1l111_opy_
  global bstack111ll11l1l_opy_
  global bstack1llll11ll_opy_
  global bstack111l1l11l_opy_
  global bstack111llll1l1_opy_
  bstack1ll1l111l_opy_ = len(CONFIG.get(bstack1ll111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨไ"), []))
  if not bstack11l11lll_opy_:
    if args[1] == bstack1ll111_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ๅ") or args[1] == bstack1ll111_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨๆ") or args[1] == bstack1ll111_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩ็"):
      bstack11l11lll_opy_ = bstack1ll111_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥ่ࠪ")
      args = args[2:]
    elif args[1] == bstack1ll111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ้ࠩ"):
      bstack11l11lll_opy_ = bstack1ll111_opy_ (u"ࠫࡷࡵࡢࡰࡶ๊ࠪ")
      args = args[2:]
    elif args[1] == bstack1ll111_opy_ (u"ࠬࡶࡡࡣࡱࡷ๋ࠫ"):
      bstack11l11lll_opy_ = bstack1ll111_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ์")
      args = args[2:]
    elif args[1] == bstack1ll111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨํ"):
      bstack11l11lll_opy_ = bstack1ll111_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ๎")
      args = args[2:]
    elif args[1] == bstack1ll111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ๏"):
      bstack11l11lll_opy_ = bstack1ll111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ๐")
      args = args[2:]
    elif args[1] == bstack1ll111_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ๑"):
      bstack11l11lll_opy_ = bstack1ll111_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ๒")
      args = args[2:]
    else:
      if not bstack1ll111_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ๓") in CONFIG or str(CONFIG[bstack1ll111_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ๔")]).lower() in [bstack1ll111_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ๕"), bstack1ll111_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪ๖"), bstack1ll111_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠫ๗")]:
        bstack11l11lll_opy_ = bstack1ll111_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠬ๘")
        args = args[1:]
      elif str(CONFIG[bstack1ll111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ๙")]).lower() == bstack1ll111_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ๚"):
        bstack11l11lll_opy_ = bstack1ll111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭๛")
        args = args[1:]
      elif str(CONFIG[bstack1ll111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ๜")]).lower() == bstack1ll111_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ๝"):
        bstack11l11lll_opy_ = bstack1ll111_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ๞")
        args = args[1:]
      elif str(CONFIG[bstack1ll111_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ๟")]).lower() == bstack1ll111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ๠"):
        bstack11l11lll_opy_ = bstack1ll111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭๡")
        args = args[1:]
      elif str(CONFIG[bstack1ll111_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ๢")]).lower() == bstack1ll111_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ๣"):
        bstack11l11lll_opy_ = bstack1ll111_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ๤")
        args = args[1:]
      else:
        os.environ[bstack1ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬ๥")] = bstack11l11lll_opy_
        bstack1111l1l1ll_opy_(bstack1llllll11_opy_)
  os.environ[bstack1ll111_opy_ (u"ࠫࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ࡟ࡖࡕࡈࡈࠬ๦")] = bstack11l11lll_opy_
  bstack1l11111l11_opy_ = bstack11l11lll_opy_
  if cli.is_enabled(CONFIG):
    try:
      if bstack11l11lll_opy_ == bstack1ll111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ๧") and bstack11l11l1111_opy_():
        bstack1l1l1l1l_opy_ = bstack11lll111l_opy_[bstack1ll111_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙࠳ࡂࡅࡆࠪ๨")]
      elif bstack11l11lll_opy_ in [bstack1ll111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ๩"), bstack1ll111_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ๪")]:
        bstack1l1l1l1l_opy_ = bstack1ll111_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ๫")
      else:
        bstack1l1l1l1l_opy_ = bstack11l11lll_opy_
      bstack1lll11111_opy_.invoke(Events.bstack11l1111l11_opy_, bstack1lll11ll11_opy_(
        sdk_version=__version__,
        path_config=bstack11ll11llll_opy_(),
        path_project=os.getcwd(),
        test_framework=bstack1l1l1l1l_opy_,
        frameworks=[bstack1l1l1l1l_opy_],
        framework_versions={
          bstack1l1l1l1l_opy_: bstack1lll1l1l11_opy_(bstack1ll111_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩ๬") if bstack11l11lll_opy_ in [bstack1ll111_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ๭"), bstack1ll111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ๮"), bstack1ll111_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧ๯")] else bstack11l11lll_opy_)
        },
        bs_config=CONFIG
      ))
      if cli.config and cli.config.get(bstack1ll111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤ๰"), None):
        CONFIG[bstack1ll111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠥ๱")] = cli.config.get(bstack1ll111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠦ๲"), None)
    except Exception as e:
      bstack1lll11111_opy_.invoke(Events.bstack1l111111ll_opy_, e.__traceback__, 1)
    if bstack11l1l1l1_opy_:
      CONFIG[bstack1ll111_opy_ (u"ࠥࡥࡵࡶࠢ๳")] = cli.config[bstack1ll111_opy_ (u"ࠦࡦࡶࡰࠣ๴")]
      logger.info(bstack11ll11l11_opy_.format(CONFIG[bstack1ll111_opy_ (u"ࠬࡧࡰࡱࠩ๵")]))
  else:
    bstack1lll11111_opy_.clear()
  global bstack1lllll11l_opy_
  global bstack1111111l_opy_
  if bstack1ll1llll_opy_:
    try:
      bstack1ll1l1l111_opy_ = datetime.datetime.now()
      os.environ[bstack1ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ๶")] = bstack11l11lll_opy_
      bstack11l1l1lll_opy_ = bstack111ll11111_opy_.bstack111l11l11_opy_(EVENTS.bstack11l1l1111l_opy_)
      try:
        logger.info(bstack1ll111_opy_ (u"ࠢࡔࡧࡱࡨ࡮ࡴࡧࠡࡕࡇࡏ࡚ࠥࡥࡴࡶࠣࡅࡹࡺࡥ࡮ࡲࡷࡩࡩࠦࡥࡷࡧࡱࡸࠧ๷"))
        bstack11lllllll1_opy_(bstack11ll11ll11_opy_, CONFIG)
      finally:
        bstack111ll11111_opy_.end(EVENTS.bstack11l1l1111l_opy_.value, bstack11l1l1lll_opy_ + bstack1ll111_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ๸"), bstack11l1l1lll_opy_ + bstack1ll111_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ๹"), status=True, failure=None, test_name=None)
      cli.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻ࡵࡧ࡯ࡤࡺࡥࡴࡶࡢࡥࡹࡺࡥ࡮ࡲࡷࡩࡩࠨ๺"), datetime.datetime.now() - bstack1ll1l1l111_opy_)
    except Exception as e:
      logger.debug(bstack11lll111l1_opy_.format(str(e)))
  global bstack1111lllll1_opy_
  global bstack1l11ll11l_opy_
  global bstack1111lll11_opy_
  global bstack1l111llll_opy_
  global bstack1111111l1_opy_
  global bstack1l1l1l1ll_opy_
  global bstack1llll111l1_opy_
  global bstack11l1ll1l11_opy_
  global bstack1lll1lll1_opy_
  global bstack1l111l11l1_opy_
  global bstack1ll1ll11l1_opy_
  global bstack1l1l1lllll_opy_
  global bstack11l1lll1_opy_
  global bstack1ll1l111ll_opy_
  global bstack1l1l1ll111_opy_
  global bstack11l1ll11l_opy_
  global bstack1ll1ll11l_opy_
  global bstack1l11l11l1_opy_
  global bstack1l1llll1ll_opy_
  global bstack11l111l11_opy_
  global bstack1l1ll1ll1_opy_
  global bstack1lll11lll1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1111lllll1_opy_ = webdriver.Remote.__init__
    bstack1l11ll11l_opy_ = WebDriver.quit
    bstack1l1l1lllll_opy_ = WebDriver.close
    bstack11l1ll11l_opy_ = WebDriver.get
    bstack1lll11lll1_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1lllll11l_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack1ll1lll11_opy_
    bstack1111111l_opy_ = bstack1ll1lll11_opy_()
  except Exception as e:
    pass
  try:
    global bstack1l11l111_opy_
    from QWeb.keywords import browser
    bstack1l11l111_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1lll1ll1l_opy_(CONFIG) and bstack11ll1ll11l_opy_():
    if bstack11l1l1l11_opy_() < version.parse(bstack1l11l11l1l_opy_):
      logger.error(bstack11l11111l1_opy_.format(bstack11l1l1l11_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack1ll111_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬ๻")) and callable(getattr(RemoteConnection, bstack1ll111_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭๼"))):
          RemoteConnection._get_proxy_url = bstack111lllll_opy_
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          ClientConfig.get_proxy_url = bstack111lllll_opy_
      except Exception as e:
        logger.error(bstack11l11l1l_opy_.format(str(e)))
  if not CONFIG.get(bstack1ll111_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨ๽"), False) and not bstack1ll1llll_opy_:
    logger.info(bstack111l1lll_opy_)
  bstack11l11ll1_opy_ = not cli.is_enabled(CONFIG) and bstack11l11lll_opy_ not in [bstack1ll111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ๾")]
  bstack11l11lll1l_opy_ = bstack11l11ll1_opy_ and bstack1ll111_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ๿") in CONFIG and str(CONFIG[bstack1ll111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭຀")]).lower() != bstack1ll111_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩກ")
  bstack111l1l1l11_opy_ = bstack11l11ll1_opy_ and not bstack11l11lll1l_opy_ and (bstack11l11lll_opy_ != bstack1ll111_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠬຂ") or (bstack11l11lll_opy_ == bstack1ll111_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨ࠭຃") and not bstack1ll1llll_opy_))
  if bstack11l11lll_opy_ not in [bstack1ll111_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧຄ")]:
    bstack1111ll1l1_opy_(os.path.join(os.getcwd(), bstack1ll111_opy_ (u"ࠧ࡭ࡱࡪࠫ຅"), bstack1ll111_opy_ (u"ࠨ࡭ࡨࡽ࠲ࡳࡥࡵࡴ࡬ࡧࡸ࠴ࡪࡴࡱࡱࠫຆ")), logger)
  if (bstack11l11lll_opy_ in [bstack1ll111_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨງ"), bstack1ll111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩຈ"), bstack1ll111_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬຉ")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      try:
        from pabot.pabot import QueueItem
        from pabot import pabot
      except Exception as e:
        logger.warning(bstack1lllllll11_opy_ + str(e))
      if not is_robot_playwright_installed():
        try:
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
          WebDriverCreator._get_ff_profile = bstack1llll111l_opy_
          bstack1l1l1l1ll_opy_ = WebDriverCache.close
        except Exception as e:
          logger.warning(bstack1llll111ll_opy_ + str(e))
        try:
          from AppiumLibrary.utils.applicationcache import ApplicationCache
          bstack1111111l1_opy_ = ApplicationCache.close
        except Exception as e:
          logger.debug(bstack1llll11l1l_opy_ + str(e))
    except Exception as e:
      bstack1l1ll1l1_opy_(e, bstack1llll111ll_opy_)
    if bstack11l11lll_opy_ != bstack1ll111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ຊ"):
      bstack1llllll1l1_opy_()
    bstack1111lll11_opy_ = Output.start_test
    bstack1l111llll_opy_ = Output.end_test
    bstack1llll111l1_opy_ = TestStatus.__init__
    bstack1lll1lll1_opy_ = pabot._run
    bstack1l111l11l1_opy_ = QueueItem.__init__
    bstack1ll1ll11l1_opy_ = pabot._create_command_for_execution
    bstack11l111l11_opy_ = pabot._report_results
  if bstack11l11lll_opy_ == bstack1ll111_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭຋"):
    global bstack11lll11l1_opy_
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l1ll1l1_opy_(e, bstack1l1l1ll11l_opy_)
    bstack11l1lll1_opy_ = Runner.run_hook
    bstack1ll1l111ll_opy_ = Runner.load_hooks
    bstack1l1l1ll111_opy_ = Step.run
    try:
      sig = inspect.signature(bstack11l1lll1_opy_)
      params = list(sig.parameters.keys())
      bstack11lll11l1_opy_ = bstack1ll111_opy_ (u"ࠧࡤࡱࡱࡸࡪࡾࡴࠨຌ") in params
      logger.info(bstack1ll111_opy_ (u"ࠨࡆࡨࡸࡪࡩࡴࡦࡦࠣࡦࡪ࡮ࡡࡷࡧࠣࡶࡺࡴ࡟ࡩࡱࡲ࡯ࠥࡹࡩࡨࡰࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬຍ").format(bstack1ll111_opy_ (u"ࠩ࠴࠲࠷࠴࠶ࠡࠪࡺ࡭ࡹ࡮ࠠࡤࡱࡱࡸࡪࡾࡴࠪࠩຎ") if bstack11lll11l1_opy_ else bstack1ll111_opy_ (u"ࠪ࠵࠳࠹ࠫࠡࠪࡺ࡭ࡹ࡮࡯ࡶࡶࠣࡧࡴࡴࡴࡦࡺࡷ࠭ࠬຏ")))
    except Exception as e:
      logger.debug(bstack1ll111_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡨࡺࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡳࡷࡱࡣ࡭ࡵ࡯࡬ࠢࡶ࡭࡬ࡴࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩຐ").format(str(e)))
      bstack11lll11l1_opy_ = None
  if bstack11l11lll_opy_ == bstack1ll111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬຑ"):
    try:
      from _pytest.config import Config
      bstack1l11l11l1_opy_ = Config.getoption
      from _pytest import runner
      bstack1l1llll1ll_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warning(bstack1ll111_opy_ (u"ࠨࠥࡴ࠼ࠣࠩࡸࠨຒ"), bstack1l1ll11l_opy_, str(e))
    try:
      from pytest_bdd import reporting
      bstack1l1ll1ll1_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1ll111_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨຓ"))
    if bstack1ll111l11_opy_():
      logger.warning(bstack1l1ll11l11_opy_[bstack1ll111_opy_ (u"ࠨࡕࡇࡏ࠲ࡍࡅࡏ࠯࠳࠴࠺࠭ດ")])
  try:
    framework_name = bstack1ll111_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨຕ") if bstack11l11lll_opy_ in [bstack1ll111_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩຖ"), bstack1ll111_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪທ"), bstack1ll111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ຘ")] else bstack1l1ll1lll_opy_(bstack11l11lll_opy_)
    bstack11111l1ll_opy_ = {
      bstack1ll111_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࠧນ"): bstack1ll111_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩບ") if bstack11l11lll_opy_ == bstack1ll111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨປ") and bstack11l11l1111_opy_() else framework_name,
      bstack1ll111_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ຜ"): bstack1lll1l1l11_opy_(framework_name),
      bstack1ll111_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨຝ"): __version__,
      bstack1ll111_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬພ"): bstack11l11lll_opy_
    }
    if bstack11l11lll_opy_ in bstack111l11llll_opy_ + bstack111l1lll1l_opy_:
      if bstack1ll11lll11_opy_.bstack1l1lll1111_opy_(CONFIG):
        if bstack1ll111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬຟ") in CONFIG:
          os.environ[bstack1ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧຠ")] = os.getenv(bstack1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨມ"), json.dumps(CONFIG[bstack1ll111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨຢ")]))
          CONFIG[bstack1ll111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩຣ")].pop(bstack1ll111_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨ຤"), None)
          CONFIG[bstack1ll111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫລ")].pop(bstack1ll111_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ຦"), None)
        bstack11111l1ll_opy_[bstack1ll111_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ວ")] = {
          bstack1ll111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬຨ"): bstack1ll111_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࠪຩ"),
          bstack1ll111_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪສ"): str(bstack11l1l1l11_opy_())
        }
    bstack111l11ll_opy_, bstack1ll11ll11l_opy_ = None, {}
    bstack11lll1l1l1_opy_ = None
    bstack11l1l111_opy_ = None
    def bstack11l11111l_opy_():
      if bstack11l11lll1l_opy_:
        bstack11l111l1l_opy_()
      elif bstack111l1l1l11_opy_:
        bstack111l111l1l_opy_()
    def bstack1ll1lll1l1_opy_():
      nonlocal bstack111l11ll_opy_, bstack1ll11ll11l_opy_
      if bstack11l11lll_opy_ not in [bstack1ll111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫຫ")] and not cli.is_running():
        bstack111l11ll_opy_, bstack1ll11ll11l_opy_ = TestHubHandler.launch(CONFIG, bstack11111l1ll_opy_)
    if bstack11l11lll1l_opy_ or bstack111l1l1l11_opy_:
      bstack11lll1l1l1_opy_ = threading.Thread(target=bstack11l11111l_opy_)
      bstack11lll1l1l1_opy_.start()
    if bstack11l11lll_opy_ not in [bstack1ll111_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬຬ")] and not cli.is_running():
      bstack11l1l111_opy_ = threading.Thread(target=bstack1ll1lll1l1_opy_)
      bstack11l1l111_opy_.start()
    if bstack11lll1l1l1_opy_:
      bstack11lll1l1l1_opy_.join()
    if bstack11l1l111_opy_:
      bstack11l1l111_opy_.join()
    if bstack1ll11ll11l_opy_.get(bstack1ll111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬອ")) is not None and bstack1ll11lll11_opy_.bstack1111llll1_opy_(CONFIG) is None:
      value = bstack1ll11ll11l_opy_[bstack1ll111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ຮ")].get(bstack1ll111_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨຯ"))
      if value is not None:
          CONFIG[bstack1ll111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨະ")] = value
      else:
        logger.debug(bstack1ll111_opy_ (u"ࠤࡑࡳࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡪࡡࡵࡣࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠢັ"))
  except Exception as e:
    logger.debug(bstack111lll11l1_opy_.format(bstack1ll111_opy_ (u"ࠪࡘࡪࡹࡴࡉࡷࡥࠫາ"), str(e)))
  if bstack11l11lll_opy_ == bstack1ll111_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠬຳ"):
    PARALLELISE_VANILLA_PYTHON = True
    if bstack1ll1llll_opy_ and bstack11ll11l11l_opy_:
      if cli.is_enabled(CONFIG):
        bstack11l111ll1l_opy_ = cli.config.get(bstack1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩິ"), {}).get(bstack1ll111_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨີ")) if cli.config else None
      else:
        bstack11l111ll1l_opy_ = CONFIG.get(bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫຶ"), {}).get(bstack1ll111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪື"))
      bstack111lll11ll_opy_(bstack111111ll1_opy_)
    elif bstack1ll1llll_opy_:
      if cli.is_enabled(CONFIG):
        bstack11l111ll1l_opy_ = cli.config.get(bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸຸ࠭"), {}).get(bstack1ll111_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶູࠬ")) if cli.config else None
      else:
        bstack11l111ll1l_opy_ = CONFIG.get(bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ຺"), {}).get(bstack1ll111_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧົ"))
      global bstack1l111lll11_opy_
      try:
        if bstack1llll1lll1_opy_(bstack1ll1llll_opy_[bstack1ll111_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩຼ")]) and multiprocessing.current_process().name == bstack1ll111_opy_ (u"ࠧ࠱ࠩຽ"):
          bstack1ll1llll_opy_[bstack1ll111_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ຾")].remove(bstack1ll111_opy_ (u"ࠩ࠰ࡱࠬ຿"))
          bstack1ll1llll_opy_[bstack1ll111_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ເ")].remove(bstack1ll111_opy_ (u"ࠫࡵࡪࡢࠨແ"))
          bstack1ll1llll_opy_[bstack1ll111_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨໂ")] = bstack1ll1llll_opy_[bstack1ll111_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩໃ")][0]
          with open(bstack1ll1llll_opy_[bstack1ll111_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪໄ")], bstack1ll111_opy_ (u"ࠨࡴࠪ໅")) as f:
            file_content = f.read()
          bstack11llll111l_opy_ = bstack1ll111_opy_ (u"ࠤࠥࠦ࡫ࡸ࡯࡮ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡵࡧ࡯ࠥ࡯࡭ࡱࡱࡵࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥ࠼ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩ࠭ࢁࡽࠪ࠽ࠣࡪࡷࡵ࡭ࠡࡲࡧࡦࠥ࡯࡭ࡱࡱࡵࡸࠥࡖࡤࡣ࠽ࠣࡳ࡬ࡥࡤࡣࠢࡀࠤࡕࡪࡢ࠯ࡦࡲࡣࡧࡸࡥࡢ࡭࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡥࡧࡩࠤࡲࡵࡤࡠࡤࡵࡩࡦࡱࠨࡴࡧ࡯ࡪ࠱ࠦࡡࡳࡩ࠯ࠤࡹ࡫࡭ࡱࡱࡵࡥࡷࡿࠠ࠾ࠢ࠳࠭࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡹࡸࡹ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡤࡶ࡬ࠦ࠽ࠡࡵࡷࡶ࠭࡯࡮ࡵࠪࡤࡶ࡬࠯ࠫ࠲࠲ࠬࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡨࡼࡨ࡫ࡰࡵࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡧࡳࠡࡧ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡵࡧࡳࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡰࡩࡢࡨࡧ࠮ࡳࡦ࡮ࡩ࠰ࡦࡸࡧ࠭ࡶࡨࡱࡵࡵࡲࡢࡴࡼ࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡒࡧࡦ࠳ࡪ࡯ࡠࡤࠣࡁࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡕࡪࡢ࠯ࡦࡲࡣࡧࡸࡥࡢ࡭ࠣࡁࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡕࡪࡢࠩࠫ࠱ࡷࡪࡺ࡟ࡵࡴࡤࡧࡪ࠮ࠩ࡝ࡰࠥࠦࠧໆ").format(str(bstack1ll1llll_opy_))
          bstack1lll1l1ll1_opy_ = bstack11llll111l_opy_ + file_content
          bstack1llll1ll11_opy_ = bstack1ll1llll_opy_[bstack1ll111_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭໇")] + bstack1ll111_opy_ (u"ࠫࡤࡨࡳࡵࡣࡦ࡯ࡤࡺࡥ࡮ࡲ࠱ࡴࡾ່࠭")
          with open(bstack1llll1ll11_opy_, bstack1ll111_opy_ (u"ࠬࡽ້ࠧ")):
            pass
          with open(bstack1llll1ll11_opy_, bstack1ll111_opy_ (u"ࠨࡷࠬࠤ໊")) as f:
            f.write(bstack1lll1l1ll1_opy_)
          import subprocess
          bstack1lll11l1_opy_ = subprocess.run([bstack1ll111_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴ໋ࠢ"), bstack1llll1ll11_opy_])
          if os.path.exists(bstack1llll1ll11_opy_):
            os.unlink(bstack1llll1ll11_opy_)
          os._exit(bstack1lll11l1_opy_.returncode)
        else:
          if bstack1llll1lll1_opy_(bstack1ll1llll_opy_[bstack1ll111_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ໌")]):
            bstack1ll1llll_opy_[bstack1ll111_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬໍ")].remove(bstack1ll111_opy_ (u"ࠪ࠱ࡲ࠭໎"))
            bstack1ll1llll_opy_[bstack1ll111_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ໏")].remove(bstack1ll111_opy_ (u"ࠬࡶࡤࡣࠩ໐"))
            bstack1ll1llll_opy_[bstack1ll111_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ໑")] = bstack1ll1llll_opy_[bstack1ll111_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ໒")][0]
          bstack111lll11ll_opy_(bstack111111ll1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1ll1llll_opy_[bstack1ll111_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ໓")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1ll111_opy_ (u"ࠩࡢࡣࡳࡧ࡭ࡦࡡࡢࠫ໔")] = bstack1ll111_opy_ (u"ࠪࡣࡤࡳࡡࡪࡰࡢࡣࠬ໕")
          mod_globals[bstack1ll111_opy_ (u"ࠫࡤࡥࡦࡪ࡮ࡨࡣࡤ࠭໖")] = os.path.abspath(bstack1ll1llll_opy_[bstack1ll111_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ໗")])
          exec(open(bstack1ll1llll_opy_[bstack1ll111_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ໘")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1ll111_opy_ (u"ࠧࡄࡣࡸ࡫࡭ࡺࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃࠧ໙").format(str(e)))
          for driver in bstack1l111lll11_opy_:
            bstack111l1lll1_opy_.append({
              bstack1ll111_opy_ (u"ࠨࡰࡤࡱࡪ࠭໚"): bstack1ll1llll_opy_[bstack1ll111_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ໛")],
              bstack1ll111_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩໜ"): str(e),
              bstack1ll111_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪໝ"): multiprocessing.current_process().name
            })
            bstack111lll11_opy_(driver, bstack1ll111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬໞ"), bstack1ll111_opy_ (u"ࠨࡓࡦࡵࡶ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤໟ") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1l111lll11_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack11l1l1l1_opy_, CONFIG, logger)
      bstack111ll1lll1_opy_()
      bstack1l11ll111_opy_()
      percy.bstack1111ll1l_opy_()
      bstack1l11l1l1ll_opy_ = {
        bstack1ll111_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ໠"): args[0],
        bstack1ll111_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨ໡"): CONFIG,
        bstack1ll111_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪ໢"): bstack1l1l11lll_opy_,
        bstack1ll111_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ໣"): bstack11l1l1l1_opy_
      }
      if bstack1ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ໤") in CONFIG:
        bstack1l1lll11l_opy_ = bstack11l1ll11_opy_(args, logger, CONFIG, BROWSERSTACK_AUTOMATION, bstack1ll1l111l_opy_)
        bstack111ll11l1l_opy_ = bstack1l1lll11l_opy_.bstack11l1ll1ll1_opy_(run_on_browserstack, bstack1l11l1l1ll_opy_, bstack1llll1lll1_opy_(args))
      else:
        if bstack1llll1lll1_opy_(args):
          bstack1l11l1l1ll_opy_[bstack1ll111_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ໥")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1l11l1l1ll_opy_,))
          test.start()
          test.join()
        else:
          bstack111lll11ll_opy_(bstack111111ll1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1ll111_opy_ (u"࠭࡟ࡠࡰࡤࡱࡪࡥ࡟ࠨ໦")] = bstack1ll111_opy_ (u"ࠧࡠࡡࡰࡥ࡮ࡴ࡟ࡠࠩ໧")
          mod_globals[bstack1ll111_opy_ (u"ࠨࡡࡢࡪ࡮ࡲࡥࡠࡡࠪ໨")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack11l11lll_opy_ == bstack1ll111_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ໩") or bstack11l11lll_opy_ == bstack1ll111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ໪"):
    percy.init(bstack11l1l1l1_opy_, CONFIG, logger)
    percy.bstack1111ll1l_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1l1ll1l1_opy_(e, bstack1llll111ll_opy_)
    bstack111ll1lll1_opy_()
    bstack111lll11ll_opy_(bstack1ll1ll1ll1_opy_)
    if BROWSERSTACK_AUTOMATION:
      bstack1ll1ll111_opy_(bstack1ll1ll1ll1_opy_, args)
      if bstack1ll111_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩ໫") in args:
        i = args.index(bstack1ll111_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ໬"))
        args.pop(i)
        args.pop(i)
      if bstack1ll111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ໭") not in CONFIG:
        CONFIG[bstack1ll111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ໮")] = [{}]
        bstack1ll1l111l_opy_ = 1
      if bstack111ll1l1l1_opy_ == 0:
        bstack111ll1l1l1_opy_ = 1
      args.insert(0, str(bstack111ll1l1l1_opy_))
      args.insert(0, str(bstack1ll111_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭໯")))
    if TestHubHandler.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack111l11l11l_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1l111l1ll1_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack1ll111_opy_ (u"ࠤࡕࡓࡇࡕࡔࡠࡑࡓࡘࡎࡕࡎࡔࠤ໰"),
        ).parse_args(bstack111l11l11l_opy_)
        bstack1ll1l1lll1_opy_ = args.index(bstack111l11l11l_opy_[0]) if len(bstack111l11l11l_opy_) > 0 else len(args)
        args.insert(bstack1ll1l1lll1_opy_, str(bstack1ll111_opy_ (u"ࠪ࠱࠲ࡲࡩࡴࡶࡨࡲࡪࡸࠧ໱")))
        args.insert(bstack1ll1l1lll1_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡷࡵࡢࡰࡶࡢࡰ࡮ࡹࡴࡦࡰࡨࡶ࠳ࡶࡹࠨ໲"))))
        if bstack1l1ll111l_opy_.bstack1lll11l11_opy_(CONFIG):
          args.insert(bstack1ll1l1lll1_opy_, str(bstack1ll111_opy_ (u"ࠬ࠳࠭࡭࡫ࡶࡸࡪࡴࡥࡳࠩ໳")))
          args.insert(bstack1ll1l1lll1_opy_ + 1, str(bstack1ll111_opy_ (u"࠭ࡒࡦࡶࡵࡽࡋࡧࡩ࡭ࡧࡧ࠾ࢀࢃࠧ໴").format(bstack1l1ll111l_opy_.bstack1l1l11ll1l_opy_(CONFIG))))
        if bstack1l11lll111_opy_(os.environ.get(bstack1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠬ໵"))) and str(os.environ.get(bstack1ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࡥࡔࡆࡕࡗࡗࠬ໶"), bstack1ll111_opy_ (u"ࠩࡱࡹࡱࡲࠧ໷"))) != bstack1ll111_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ໸"):
          for bstack1l1l1l11ll_opy_ in bstack1l111l1ll1_opy_:
            args.remove(bstack1l1l1l11ll_opy_)
          test_files = os.environ.get(bstack1ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠨ໹")).split(bstack1ll111_opy_ (u"ࠬ࠲ࠧ໺"))
          for bstack111ll11lll_opy_ in test_files:
            args.append(bstack111ll11lll_opy_)
      except Exception as e:
        logger.error(bstack1ll111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡦࡺࡴࡢࡥ࡫࡭ࡳ࡭ࠠ࡭࡫ࡶࡸࡪࡴࡥࡳࠢࡩࡳࡷࠦࡻࡾ࠰ࠣࡉࡷࡸ࡯ࡳࠢ࠰ࠤࢀࢃࠢ໻").format(bstack11llll1l1_opy_, e))
    pabot.main(args)
  elif bstack11l11lll_opy_ == bstack1ll111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ໼"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1l1ll1l1_opy_(e, bstack1llll111ll_opy_)
    for a in args:
      if bstack1ll111_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡑࡎࡄࡘࡋࡕࡒࡎࡋࡑࡈࡊ࡞ࠧ໽") in a:
        PLATFORM_INDEX = int(a.split(bstack1ll111_opy_ (u"ࠩ࠽ࠫ໾"))[1])
      if bstack1ll111_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡇࡉࡋࡒࡏࡄࡃࡏࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ໿") in a:
        bstack11l111ll1l_opy_ = str(a.split(bstack1ll111_opy_ (u"ࠫ࠿࠭ༀ"))[1])
      if bstack1ll111_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡒࡉࡂࡔࡊࡗࠬ༁") in a:
        bstack11lll1l111_opy_ = str(a.split(bstack1ll111_opy_ (u"࠭࠺ࠨ༂"))[1])
    bstack1lll1l11l1_opy_ = None
    bstack1l1l1ll1ll_opy_ = None
    if bstack1ll111_opy_ (u"ࠧ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽ࠭༃") in args:
      i = args.index(bstack1ll111_opy_ (u"ࠨ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠧ༄"))
      args.pop(i)
      bstack1lll1l11l1_opy_ = args.pop(i)
    if bstack1ll111_opy_ (u"ࠩ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࠬ༅") in args:
      i = args.index(bstack1ll111_opy_ (u"ࠪ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽ࠭༆"))
      args.pop(i)
      bstack1l1l1ll1ll_opy_ = args.pop(i)
    if bstack1lll1l11l1_opy_ is not None:
      global bstack1l1lll11l1_opy_
      bstack1l1lll11l1_opy_ = bstack1lll1l11l1_opy_
    if bstack1l1l1ll1ll_opy_ is not None and int(PLATFORM_INDEX) < 0:
      PLATFORM_INDEX = int(bstack1l1l1ll1ll_opy_)
    if cli.is_enabled(CONFIG):
      if cli.bstack111ll1l1_opy_():
        bstack1lll11111_opy_.invoke(Events.CONNECT, bstack1lll1111_opy_())
        cli.bstack1lll111l11_opy_(PLATFORM_INDEX)
      if cli.bstack11l1111ll1_opy_(bstack1ll11l1lll_opy_):
        cli.bstack111ll1ll11_opy_()
    bstack111lll11ll_opy_(bstack1ll1ll1ll1_opy_)
    run_cli(args)
    if bstack1ll111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴࠨ༇") in multiprocessing.current_process().__dict__.keys():
      for bstack1l111l1111_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack111l1lll1_opy_.append(bstack1l111l1111_opy_)
  elif bstack11l11lll_opy_ == bstack1ll111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ༈"):
    bstack11l111l1l1_opy_ = bstack1l1ll11l1l_opy_(args, logger, CONFIG, BROWSERSTACK_AUTOMATION)
    bstack11l111l1l1_opy_.bstack111l1llll1_opy_()
    bstack111ll1lll1_opy_()
    PARALLELISE_THREADING_PYTHON = True
    bstack111l1l11l_opy_ = bstack11l111l1l1_opy_.bstack1ll1ll1l11_opy_()
    bstack11l111l1l1_opy_.bstack1l11l1l1ll_opy_(bstack11111l111_opy_)
    bstack11l111l1l1_opy_.bstack11ll1llll1_opy_()
    bstack111l11l1ll_opy_(bstack11l11lll_opy_, CONFIG, bstack11l111l1l1_opy_.bstack1l1111l1ll_opy_())
    bstack11lll11l1l_opy_.end(EVENTS.bstack11l11l1l1_opy_.value, EVENTS.bstack11l11l1l1_opy_.value + bstack1ll111_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ༉"), EVENTS.bstack11l11l1l1_opy_.value + bstack1ll111_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ༊"), status=True, failure=None, test_name=SESSION_NAME)
    bstack1l1lllll_opy_ = bstack11l111l1l1_opy_.bstack11l1ll1ll1_opy_(bstack1l11l1lll1_opy_, {
      bstack1ll111_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨ་"): CONFIG,
      bstack1ll111_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪ༌"): bstack1l1l11lll_opy_,
      bstack1ll111_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ།"): bstack11l1l1l1_opy_,
      bstack1ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ༎"): BROWSERSTACK_AUTOMATION,
      bstack1ll111_opy_ (u"ࠬࡕࡖࡆࡔࡕࡍࡉࡋ࡟ࡍࡑࡄࡈࡤ࡚ࡅࡔࡖࡌࡒࡌ࠭༏"): bstack1ll1111l1l_opy_
    })
    if not bstack1ll1llll_opy_:
      bstack111111lll_opy_ = bstack111ll11111_opy_.bstack111l11l11_opy_(EVENTS.bstack1l1111ll1l_opy_.value)
    try:
      bstack1111l1ll_opy_, bstack1111l1l111_opy_ = map(list, zip(*bstack1l1lllll_opy_))
      bstack1llll11ll_opy_ = bstack1111l1ll_opy_[0]
      for status_code in bstack1111l1l111_opy_:
        if status_code != 0:
          bstack111llll1l1_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack1ll111_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡥࡻ࡫ࠠࡦࡴࡵࡳࡷࡹࠠࡢࡰࡧࠤࡸࡺࡡࡵࡷࡶࠤࡨࡵࡤࡦ࠰ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦ࠺ࠡࡽࢀࠦ༐").format(str(e)))
  elif bstack11l11lll_opy_ == bstack1ll111_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ༑"):
    try:
      from behave.__main__ import main as bstack111l1ll1_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1l1ll1l1_opy_(e, bstack1l1l1ll11l_opy_)
    bstack111ll1lll1_opy_()
    PARALLELISE_THREADING_PYTHON = True
    bstack11l11lll1_opy_ = 1
    if bstack1ll111_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ༒") in CONFIG:
      bstack11l11lll1_opy_ = CONFIG[bstack1ll111_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ༓")]
    if bstack1ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭༔") in CONFIG:
      bstack1lll1l1lll_opy_ = int(bstack11l11lll1_opy_) * int(len(CONFIG[bstack1ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ༕")]))
    else:
      bstack1lll1l1lll_opy_ = int(bstack11l11lll1_opy_)
    config = Configuration(args)
    bstack1ll11lll1_opy_ = config.paths
    if len(bstack1ll11lll1_opy_) == 0:
      import glob
      pattern = bstack1ll111_opy_ (u"ࠬ࠰ࠪ࠰ࠬ࠱ࡪࡪࡧࡴࡶࡴࡨࠫ༖")
      bstack1ll11lll1l_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1ll11lll1l_opy_)
      config = Configuration(args)
      bstack1ll11lll1_opy_ = config.paths
    bstack11l111l111_opy_ = [os.path.normpath(item) for item in bstack1ll11lll1_opy_]
    bstack11ll11l1_opy_ = [os.path.normpath(item) for item in args]
    bstack1ll1ll111l_opy_ = [item for item in bstack11ll11l1_opy_ if item not in bstack11l111l111_opy_]
    import platform as pf
    if pf.system().lower() == bstack1ll111_opy_ (u"࠭ࡷࡪࡰࡧࡳࡼࡹࠧ༗"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack11l111l111_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l1l11l1ll_opy_)))
                    for bstack1l1l11l1ll_opy_ in bstack11l111l111_opy_]
    bstack11l1111l_opy_ = []
    for spec in bstack11l111l111_opy_:
      bstack11111ll1_opy_ = []
      bstack11111ll1_opy_ += bstack1ll1ll111l_opy_
      bstack11111ll1_opy_.append(spec)
      bstack11l1111l_opy_.append(bstack11111ll1_opy_)
    execution_items = []
    for bstack11111ll1_opy_ in bstack11l1111l_opy_:
      if bstack1ll111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵ༘ࠪ") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack1ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶ༙ࠫ")]):
          item = {}
          item[bstack1ll111_opy_ (u"ࠩࡤࡶ࡬࠭༚")] = bstack1ll111_opy_ (u"ࠪࠤࠬ༛").join(bstack11111ll1_opy_)
          item[bstack1ll111_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ༜")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack1ll111_opy_ (u"ࠬࡧࡲࡨࠩ༝")] = bstack1ll111_opy_ (u"࠭ࠠࠨ༞").join(bstack11111ll1_opy_)
        item[bstack1ll111_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭༟")] = 0
        execution_items.append(item)
    bstack1111l11ll1_opy_ = bstack1l111ll11l_opy_(execution_items, bstack1lll1l1lll_opy_)
    for execution_item in bstack1111l11ll1_opy_:
      bstack1l1lllll11_opy_ = []
      for item in execution_item:
        bstack1l1lllll11_opy_.append(bstack11l11lllll_opy_(name=str(item[bstack1ll111_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ༠")]),
                                             target=bstack1111llll1l_opy_,
                                             args=(item[bstack1ll111_opy_ (u"ࠩࡤࡶ࡬࠭༡")],)))
      for t in bstack1l1lllll11_opy_:
        t.start()
      for t in bstack1l1lllll11_opy_:
        t.join()
  else:
    bstack1111l1l1ll_opy_(bstack1llllll11_opy_)
  if not bstack1ll1llll_opy_:
    bstack1l111ll111_opy_()
    if bstack111111lll_opy_:
      bstack111ll11111_opy_.end(EVENTS.bstack1l1111ll1l_opy_.value, bstack111111lll_opy_ + bstack1ll111_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ༢"), bstack111111lll_opy_ + bstack1ll111_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ༣"), status=True, failure=None, test_name=None)
  logger_utils.bstack111l11111_opy_()
def browserstack_initialize(bstack11lllll1_opy_=None):
  logger.info(bstack1ll111_opy_ (u"ࠬࡘࡵ࡯ࡰ࡬ࡲ࡬ࠦࡓࡅࡍࠣࡻ࡮ࡺࡨࠡࡣࡵ࡫ࡸࡀࠠࠨ༤") + str(bstack11lllll1_opy_))
  run_on_browserstack(bstack11lllll1_opy_, None, True)
@measure(event_name=EVENTS.bstack1l111lll_opy_, stage=STAGE.bstack11ll1111_opy_, bstack11l11l111_opy_=SESSION_NAME)
def bstack1l111ll111_opy_():
  global CONFIG
  global bstack1l11111l11_opy_
  global bstack111llll1l1_opy_
  global bstack11llllll_opy_
  global global_config
  global _11l1l1lll1_opy_
  bstack111ll11l1_opy_.bstack111llllll1_opy_()
  _11l1l1lll1_opy_ = cli.is_running()
  if _11l1l1lll1_opy_:
    bstack1lll11111_opy_.invoke(Events.bstack111l11ll1l_opy_)
  else:
    bstack111ll11l_opy_ = bstack1l1ll111l_opy_.get_instance(config=CONFIG)
    bstack111ll11l_opy_.bstack11l111ll1_opy_(CONFIG)
  hashed_id = None
  bstack1l1l11ll11_opy_ = None
  def bstack111l1ll1l1_opy_():
    try:
      if bstack1l11111l11_opy_ == bstack1ll111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭༥"):
        if not cli.is_enabled(CONFIG):
          TestHubHandler.stop()
      else:
        TestHubHandler.stop()
    except Exception as e:
      logger.debug(bstack1ll111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡳࡵࡱࡳࡴ࡮ࡴࡧࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࡿࢂࠨ༦").format(e))
  def bstack111l11ll11_opy_():
    try:
      if not cli.is_enabled(CONFIG):
        bstack11l1ll1111_opy_.bstack11ll1l11l1_opy_()
    except Exception as e:
      logger.debug(bstack1ll111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡱࡴ࡬ࡲࡹ࡯࡮ࡨࠢࡥࡹ࡮ࡲࡤࠡ࡮࡬ࡲࡰࡀࠠࡼࡿࠥ༧").format(e))
  def bstack11lll1ll1l_opy_():
    nonlocal hashed_id, bstack1l1l11ll11_opy_
    try:
      if bstack1ll111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭༨") in CONFIG and str(CONFIG[bstack1ll111_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ༩")]).lower() != bstack1ll111_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪ༪"):
        hashed_id, bstack1l1l11ll11_opy_ = bstack1l1ll1lll1_opy_()
      else:
        hashed_id, bstack1l1l11ll11_opy_ = get_build_link()
    except Exception as e:
      logger.debug(bstack1ll111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡨࡵࡪ࡮ࡧࠤࡱ࡯࡮࡬࠼ࠣࡿࢂࠨ༫").format(e))
  bstack111ll1lll_opy_ = threading.Thread(target=bstack111l1ll1l1_opy_)
  bstack1ll11l1ll_opy_ = threading.Thread(target=bstack111l11ll11_opy_)
  bstack1l1llll1l1_opy_ = threading.Thread(target=bstack11lll1ll1l_opy_)
  threads = [bstack111ll1lll_opy_, bstack1ll11l1ll_opy_, bstack1l1llll1l1_opy_]
  for thread in threads:
    try:
      thread.start()
    except Exception as e:
      logger.debug(bstack1ll111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡹࡴࡢࡴࡷ࡭ࡳ࡭ࠠࡵࡪࡵࡩࡦࡪࠠࡼࡿ࠽ࠤࢀࢃࠢ༬").format(thread.name, e))
  for thread in threads:
    try:
      thread.join()
    except Exception as e:
      logger.debug(bstack1ll111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡪࡰ࡫ࡱ࡭ࡳ࡭ࠠࡵࡪࡵࡩࡦࡪࠠࡼࡿ࠽ࠤࢀࢃࠢ༭").format(thread.name, e))
  bstack11llll1l11_opy_(hashed_id)
  logger.info(bstack1ll111_opy_ (u"ࠨࡕࡇࡏࠥࡸࡵ࡯ࠢࡨࡲࡩ࡫ࡤࠡࡨࡲࡶࠥ࡯ࡤ࠻ࠩ༮") + global_config.get_property(bstack1ll111_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫ༯"), bstack1ll111_opy_ (u"ࠪࠫ༰")) + bstack1ll111_opy_ (u"ࠫ࠱ࠦࡴࡦࡵࡷ࡬ࡺࡨࠠࡪࡦ࠽ࠤࠬ༱") + os.getenv(bstack1ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ༲"), bstack1ll111_opy_ (u"࠭ࠧ༳")))
  if hashed_id is not None and bstack1l11111lll_opy_() != -1:
    sessions = bstack11ll1lll1l_opy_(hashed_id)
    bstack11llll1111_opy_(sessions, bstack1l1l11ll11_opy_)
  if bstack1l11111l11_opy_ == bstack1ll111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ༴") and bstack111llll1l1_opy_ != 0:
    sys.exit(bstack111llll1l1_opy_)
  if bstack1l11111l11_opy_ == bstack1ll111_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ༵") and bstack11llllll_opy_ != 0:
    sys.exit(bstack11llllll_opy_)
def bstack11llll1l11_opy_(new_id):
    global bstack11l1l11l1l_opy_
    bstack11l1l11l1l_opy_ = new_id
def bstack1l1ll1lll_opy_(bstack111ll11ll_opy_):
  if bstack111ll11ll_opy_:
    return bstack111ll11ll_opy_.capitalize()
  else:
    return bstack1ll111_opy_ (u"ࠩࠪ༶")
@measure(event_name=EVENTS.bstack1lllllllll_opy_, stage=STAGE.bstack11ll1111_opy_, bstack11l11l111_opy_=SESSION_NAME)
def bstack1l1lll1l11_opy_(bstack11l11111ll_opy_):
  if bstack1ll111_opy_ (u"ࠪࡲࡦࡳࡥࠨ༷") in bstack11l11111ll_opy_ and bstack11l11111ll_opy_[bstack1ll111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ༸")] != bstack1ll111_opy_ (u"༹ࠬ࠭"):
    return bstack11l11111ll_opy_[bstack1ll111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ༺")]
  else:
    bstack11l11l111_opy_ = bstack1ll111_opy_ (u"ࠢࠣ༻")
    if bstack1ll111_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨ༼") in bstack11l11111ll_opy_ and bstack11l11111ll_opy_[bstack1ll111_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩ༽")] != None:
      bstack11l11l111_opy_ += bstack11l11111ll_opy_[bstack1ll111_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪ༾")] + bstack1ll111_opy_ (u"ࠦ࠱ࠦࠢ༿")
      if bstack11l11111ll_opy_[bstack1ll111_opy_ (u"ࠬࡵࡳࠨཀ")] == bstack1ll111_opy_ (u"ࠨࡩࡰࡵࠥཁ"):
        bstack11l11l111_opy_ += bstack1ll111_opy_ (u"ࠢࡪࡑࡖࠤࠧག")
      bstack11l11l111_opy_ += (bstack11l11111ll_opy_[bstack1ll111_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬགྷ")] or bstack1ll111_opy_ (u"ࠩࠪང"))
      return bstack11l11l111_opy_
    else:
      bstack11l11l111_opy_ += bstack1l1ll1lll_opy_(bstack11l11111ll_opy_[bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫཅ")]) + bstack1ll111_opy_ (u"ࠦࠥࠨཆ") + (
              bstack11l11111ll_opy_[bstack1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧཇ")] or bstack1ll111_opy_ (u"࠭ࠧ཈")) + bstack1ll111_opy_ (u"ࠢ࠭ࠢࠥཉ")
      if bstack11l11111ll_opy_[bstack1ll111_opy_ (u"ࠨࡱࡶࠫཊ")] == bstack1ll111_opy_ (u"ࠤ࡚࡭ࡳࡪ࡯ࡸࡵࠥཋ"):
        bstack11l11l111_opy_ += bstack1ll111_opy_ (u"࡛ࠥ࡮ࡴࠠࠣཌ")
      bstack11l11l111_opy_ += bstack11l11111ll_opy_[bstack1ll111_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨཌྷ")] or bstack1ll111_opy_ (u"ࠬ࠭ཎ")
      return bstack11l11l111_opy_
@measure(event_name=EVENTS.bstack11ll1ll1ll_opy_, stage=STAGE.bstack11ll1111_opy_, bstack11l11l111_opy_=SESSION_NAME)
def bstack1l11ll1l_opy_(bstack11l1ll11l1_opy_):
  if bstack11l1ll11l1_opy_ == bstack1ll111_opy_ (u"ࠨࡤࡰࡰࡨࠦཏ"):
    return bstack1ll111_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡪࡶࡪ࡫࡮࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡪࡶࡪ࡫࡮ࠣࡀࡆࡳࡲࡶ࡬ࡦࡶࡨࡨࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪཐ")
  elif bstack11l1ll11l1_opy_ == bstack1ll111_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣད"):
    return bstack1ll111_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡷ࡫ࡤ࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡵࡩࡩࠨ࠾ࡇࡣ࡬ࡰࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬདྷ")
  elif bstack11l1ll11l1_opy_ == bstack1ll111_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥན"):
    return bstack1ll111_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡧࡳࡧࡨࡲࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡧࡳࡧࡨࡲࠧࡄࡐࡢࡵࡶࡩࡩࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫཔ")
  elif bstack11l1ll11l1_opy_ == bstack1ll111_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦཕ"):
    return bstack1ll111_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡴࡨࡨࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡲࡦࡦࠥࡂࡊࡸࡲࡰࡴ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨབ")
  elif bstack11l1ll11l1_opy_ == bstack1ll111_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࠣབྷ"):
    return bstack1ll111_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࠧࡪ࡫ࡡ࠴࠴࠹࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࠩࡥࡦࡣ࠶࠶࠻ࠨ࠾ࡕ࡫ࡰࡩࡴࡻࡴ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭མ")
  elif bstack11l1ll11l1_opy_ == bstack1ll111_opy_ (u"ࠤࡵࡹࡳࡴࡩ࡯ࡩࠥཙ"):
    return bstack1ll111_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡨ࡬ࡢࡥ࡮࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡨ࡬ࡢࡥ࡮ࠦࡃࡘࡵ࡯ࡰ࡬ࡲ࡬ࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫཚ")
  else:
    return bstack1ll111_opy_ (u"ࠫࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡣ࡮ࡤࡧࡰࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡣ࡮ࡤࡧࡰࠨ࠾ࠨཛ") + bstack1l1ll1lll_opy_(
      bstack11l1ll11l1_opy_) + bstack1ll111_opy_ (u"ࠬࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫཛྷ")
def bstack1111lll1_opy_(session):
  return bstack1ll111_opy_ (u"࠭࠼ࡵࡴࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡶࡴࡽࠢ࠿࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠣࡷࡪࡹࡳࡪࡱࡱ࠱ࡳࡧ࡭ࡦࠤࡁࡀࡦࠦࡨࡳࡧࡩࡁࠧࢁࡽࠣࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥࡣࡧࡲࡡ࡯࡭ࠥࡂࢀࢃ࠼࠰ࡣࡁࡀ࠴ࡺࡤ࠿ࡽࢀࡿࢂࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽࠱ࡷࡶࡃ࠭ཝ").format(
    session[bstack1ll111_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࡟ࡶࡴ࡯ࠫཞ")], bstack1l1lll1l11_opy_(session), bstack1l11ll1l_opy_(session[bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡴࡶࡤࡸࡺࡹࠧཟ")]),
    bstack1l11ll1l_opy_(session[bstack1ll111_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩའ")]),
    bstack1l1ll1lll_opy_(session[bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫཡ")] or session[bstack1ll111_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫར")] or bstack1ll111_opy_ (u"ࠬ࠭ལ")) + bstack1ll111_opy_ (u"ࠨࠠࠣཤ") + (session[bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩཥ")] or bstack1ll111_opy_ (u"ࠨࠩས")),
    session[bstack1ll111_opy_ (u"ࠩࡲࡷࠬཧ")] + bstack1ll111_opy_ (u"ࠥࠤࠧཨ") + session[bstack1ll111_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨཀྵ")], session[bstack1ll111_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧཪ")] or bstack1ll111_opy_ (u"࠭ࠧཫ"),
    session[bstack1ll111_opy_ (u"ࠧࡤࡴࡨࡥࡹ࡫ࡤࡠࡣࡷࠫཬ")] if session[bstack1ll111_opy_ (u"ࠨࡥࡵࡩࡦࡺࡥࡥࡡࡤࡸࠬ཭")] else bstack1ll111_opy_ (u"ࠩࠪ཮"))
@measure(event_name=EVENTS.bstack111l11l1l_opy_, stage=STAGE.bstack11ll1111_opy_, bstack11l11l111_opy_=SESSION_NAME)
def bstack11llll1111_opy_(sessions, bstack1l1l11ll11_opy_):
  try:
    bstack1l1111l1l_opy_ = bstack1ll111_opy_ (u"ࠥࠦ཯")
    if not os.path.exists(bstack1l1lll1ll_opy_):
      os.mkdir(bstack1l1lll1ll_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll111_opy_ (u"ࠫࡦࡹࡳࡦࡶࡶ࠳ࡷ࡫ࡰࡰࡴࡷ࠲࡭ࡺ࡭࡭ࠩ཰")), bstack1ll111_opy_ (u"ࠬࡸཱࠧ")) as f:
      bstack1l1111l1l_opy_ = f.read()
    bstack1l1111l1l_opy_ = bstack1l1111l1l_opy_.replace(bstack1ll111_opy_ (u"࠭ࡻࠦࡔࡈࡗ࡚ࡒࡔࡔࡡࡆࡓ࡚ࡔࡔࠦࡿིࠪ"), str(len(sessions)))
    bstack1l1111l1l_opy_ = bstack1l1111l1l_opy_.replace(bstack1ll111_opy_ (u"ࠧࡼࠧࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠪࢃཱིࠧ"), bstack1l1l11ll11_opy_)
    bstack1l1111l1l_opy_ = bstack1l1111l1l_opy_.replace(bstack1ll111_opy_ (u"ࠨࡽࠨࡆ࡚ࡏࡌࡅࡡࡑࡅࡒࡋࠥࡾུࠩ"),
                                              sessions[0].get(bstack1ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡰࡤࡱࡪཱུ࠭")) if sessions[0] else bstack1ll111_opy_ (u"ࠪࠫྲྀ"))
    with open(os.path.join(bstack1l1lll1ll_opy_, bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡶࡪࡶ࡯ࡳࡶ࠱࡬ࡹࡳ࡬ࠨཷ")), bstack1ll111_opy_ (u"ࠬࡽࠧླྀ")) as stream:
      stream.write(bstack1l1111l1l_opy_.split(bstack1ll111_opy_ (u"࠭ࡻࠦࡕࡈࡗࡘࡏࡏࡏࡕࡢࡈࡆ࡚ࡁࠦࡿࠪཹ"))[0])
      for session in sessions:
        stream.write(bstack1111lll1_opy_(session))
      stream.write(bstack1l1111l1l_opy_.split(bstack1ll111_opy_ (u"ࠧࡼࠧࡖࡉࡘ࡙ࡉࡐࡐࡖࡣࡉࡇࡔࡂࠧࢀེࠫ"))[1])
    logger.info(bstack1ll111_opy_ (u"ࠨࡉࡨࡲࡪࡸࡡࡵࡧࡧࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡦࡺ࡯࡬ࡥࠢࡤࡶࡹ࡯ࡦࡢࡥࡷࡷࠥࡧࡴࠡࡽࢀཻࠫ").format(bstack1l1lll1ll_opy_));
  except Exception as e:
    logger.debug(bstack11111l11_opy_.format(str(e)))
def bstack11ll1lll1l_opy_(hashed_id):
  global CONFIG
  try:
    bstack1ll1l1l111_opy_ = datetime.datetime.now()
    host = bstack1ll111_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡵ࡯࠭ࡤ࡮ࡲࡹࡩ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ོࠩ") if bstack1ll111_opy_ (u"ࠪࡥࡵࡶཽࠧ") in CONFIG else bstack1ll111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬཾ")
    user = CONFIG[bstack1ll111_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧཿ")]
    key = CONFIG[bstack1ll111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺྀࠩ")]
    bstack11l1l1ll1_opy_ = bstack1ll111_opy_ (u"ࠧࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪཱྀ࠭") if bstack1ll111_opy_ (u"ࠨࡣࡳࡴࠬྂ") in CONFIG else (bstack1ll111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭ྃ") if CONFIG.get(bstack1ll111_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫྄ࠧ")) else bstack1ll111_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭྅"))
    host = bstack1l1ll11lll_opy_(cli.config, [bstack1ll111_opy_ (u"ࠧࡧࡰࡪࡵࠥ྆"), bstack1ll111_opy_ (u"ࠨࡡࡱࡲࡄࡹࡹࡵ࡭ࡢࡶࡨࠦ྇"), bstack1ll111_opy_ (u"ࠢࡢࡲ࡬ࠦྈ")], host) if bstack1ll111_opy_ (u"ࠨࡣࡳࡴࠬྉ") in CONFIG else bstack1l1ll11lll_opy_(cli.config, [bstack1ll111_opy_ (u"ࠤࡤࡴ࡮ࡹࠢྊ"), bstack1ll111_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷࡩࠧྋ"), bstack1ll111_opy_ (u"ࠦࡦࡶࡩࠣྌ")], host)
    url = bstack1ll111_opy_ (u"ࠬࢁࡽ࠰ࡽࢀ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃ࠯ࡴࡧࡶࡷ࡮ࡵ࡮ࡴ࠰࡭ࡷࡴࡴࠧྍ").format(host, bstack11l1l1ll1_opy_, hashed_id)
    headers = {
      bstack1ll111_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡵࡻࡳࡩࠬྎ"): bstack1ll111_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪྏ"),
    }
    proxies = bstack111lllllll_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies, auth=(user, key))
    if response.json():
      cli.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠣࡪࡷࡸࡵࡀࡧࡦࡶࡢࡷࡪࡹࡳࡪࡱࡱࡷࡤࡲࡩࡴࡶࠥྐ"), datetime.datetime.now() - bstack1ll1l1l111_opy_)
      return list(map(lambda session: session[bstack1ll111_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠧྑ")], response.json()))
  except Exception as e:
    logger.debug(bstack1ll111ll1l_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack11l111111_opy_, stage=STAGE.bstack11ll1111_opy_, bstack11l11l111_opy_=SESSION_NAME)
def get_build_link():
  global CONFIG
  global bstack11l1l11l1l_opy_
  try:
    if bstack1ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ྒ") in CONFIG:
      bstack1ll1l1l111_opy_ = datetime.datetime.now()
      host = bstack1ll111_opy_ (u"ࠫࡦࡶࡩ࠮ࡥ࡯ࡳࡺࡪࠧྒྷ") if bstack1ll111_opy_ (u"ࠬࡧࡰࡱࠩྔ") in CONFIG else bstack1ll111_opy_ (u"࠭ࡡࡱ࡫ࠪྕ")
      user = CONFIG[bstack1ll111_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩྖ")]
      key = CONFIG[bstack1ll111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫྗ")]
      bstack11l1l1ll1_opy_ = bstack1ll111_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨ྘") if bstack1ll111_opy_ (u"ࠪࡥࡵࡶࠧྙ") in CONFIG else bstack1ll111_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ྚ")
      url = bstack1ll111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡻࡾ࠼ࡾࢁࡅࢁࡽ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࢀࢃ࠯ࡣࡷ࡬ࡰࡩࡹ࠮࡫ࡵࡲࡲࠬྛ").format(user, key, host, bstack11l1l1ll1_opy_)
      if cli.is_enabled(CONFIG):
        bstack1l1l11ll11_opy_, hashed_id = cli.bstack1lll1111ll_opy_()
        logger.info(bstack111llll111_opy_.format(bstack1l1l11ll11_opy_))
        return [hashed_id, bstack1l1l11ll11_opy_]
      else:
        headers = {
          bstack1ll111_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡵࡻࡳࡩࠬྜ"): bstack1ll111_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪྜྷ"),
        }
        if bstack1ll111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪྞ") in CONFIG:
          params = {bstack1ll111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧྟ"): CONFIG[bstack1ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ྠ")], bstack1ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧྡ"): CONFIG[bstack1ll111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧྡྷ")]}
        else:
          params = {bstack1ll111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫྣ"): CONFIG[bstack1ll111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪྤ")]}
        proxies = bstack111lllllll_opy_(CONFIG, url)
        response = requests.get(url, params=params, headers=headers, proxies=proxies)
        if response.json():
          bstack11llllll1l_opy_ = response.json()[0][bstack1ll111_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡨࡵࡪ࡮ࡧࠫྥ")]
          if bstack11llllll1l_opy_:
            bstack1l1l11ll11_opy_ = bstack11llllll1l_opy_[bstack1ll111_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤࡡࡸࡶࡱ࠭ྦ")].split(bstack1ll111_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥ࠰ࡦࡺ࡯࡬ࡥࠩྦྷ"))[0] + bstack1ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡶ࠳ࠬྨ") + bstack11llllll1l_opy_[
              bstack1ll111_opy_ (u"ࠬ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨྩ")]
            logger.info(bstack111llll111_opy_.format(bstack1l1l11ll11_opy_))
            bstack11l1l11l1l_opy_ = bstack11llllll1l_opy_[bstack1ll111_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩྪ")]
            bstack1lll111lll_opy_ = CONFIG[bstack1ll111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪྫ")]
            if bstack1ll111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪྫྷ") in CONFIG:
              bstack1lll111lll_opy_ += bstack1ll111_opy_ (u"ࠩࠣࠫྭ") + CONFIG[bstack1ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬྮ")]
            if bstack1lll111lll_opy_ != bstack11llllll1l_opy_[bstack1ll111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩྯ")]:
              logger.debug(bstack1l1l1l111l_opy_.format(bstack11llllll1l_opy_[bstack1ll111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪྰ")], bstack1lll111lll_opy_))
            cli.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠨࡨࡵࡶࡳ࠾࡬࡫ࡴࡠࡤࡸ࡭ࡱࡪ࡟࡭࡫ࡱ࡯ࠧྱ"), datetime.datetime.now() - bstack1ll1l1l111_opy_)
            return [bstack11llllll1l_opy_[bstack1ll111_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪྲ")], bstack1l1l11ll11_opy_]
    else:
      logger.warning(bstack1l11l1ll_opy_)
  except Exception as e:
    logger.debug(bstack11llll111_opy_.format(str(e)))
  return [None, None]
def bstack1l11l1llll_opy_(url, bstack1l1l1ll1l_opy_=False):
  global CONFIG
  global bstack1l111ll1l_opy_
  if not bstack1l111ll1l_opy_:
    hostname = bstack111l1lllll_opy_(url)
    is_private = bstack1111ll1lll_opy_(hostname)
    if (bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬླ") in CONFIG and not bstack1l11lll111_opy_(CONFIG[bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ྴ")])) and (is_private or bstack1l1l1ll1l_opy_):
      bstack1l111ll1l_opy_ = hostname
def bstack111l1lllll_opy_(url):
  return urlparse(url).hostname
def bstack1111ll1lll_opy_(hostname):
  for bstack1l1l1111_opy_ in bstack1l11llll11_opy_:
    regex = re.compile(bstack1l1l1111_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1ll1ll1ll_opy_(bstack1ll111l1ll_opy_):
  return True if bstack1ll111l1ll_opy_ in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack1ll1l11111_opy_, stage=STAGE.bstack11ll1111_opy_, bstack11l11l111_opy_=SESSION_NAME)
def getAccessibilityResults(driver):
  global CONFIG
  global PLATFORM_INDEX
  bstack1lll1l11ll_opy_ = not (bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧྵ"), None) and bstack11llll11l_opy_(
          threading.current_thread(), bstack1ll111_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪྶ"), None))
  bstack11llll11_opy_ = getattr(driver, bstack1ll111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬྷ"), None) != True
  bstack11l11l11ll_opy_ = bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ྸ"), None) and bstack11llll11l_opy_(
          threading.current_thread(), bstack1ll111_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩྐྵ"), None)
  if bstack11l11l11ll_opy_:
    if not bstack11ll1111l1_opy_():
      logger.warning(bstack1ll111_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡳࡴࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶ࠲ࠧྺ"))
      return {}
    logger.debug(bstack1ll111_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸ࠭ྻ"))
    logger.debug(perform_scan(driver, driver_command=bstack1ll111_opy_ (u"ࠪࡩࡽ࡫ࡣࡶࡶࡨࡗࡨࡸࡩࡱࡶࠪྼ")))
    results = bstack1ll1ll11ll_opy_(bstack1ll111_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷࡷࠧ྽"))
    if results is not None and results.get(bstack1ll111_opy_ (u"ࠧ࡯ࡳࡴࡷࡨࡷࠧ྾")) is not None:
        return results[bstack1ll111_opy_ (u"ࠨࡩࡴࡵࡸࡩࡸࠨ྿")]
    logger.error(bstack1ll111_opy_ (u"ࠢࡏࡱࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡖࡪࡹࡵ࡭ࡶࡶࠤࡼ࡫ࡲࡦࠢࡩࡳࡺࡴࡤ࠯ࠤ࿀"))
    return []
  if not bstack1ll11lll11_opy_.bstack1111l1ll1l_opy_(CONFIG, PLATFORM_INDEX) or (bstack11llll11_opy_ and bstack1lll1l11ll_opy_):
    logger.warning(bstack1ll111_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵ࠱ࠦ࿁"))
    return {}
  try:
    logger.debug(bstack1ll111_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸ࠭࿂"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack1l1l1l1lll_opy_.bstack111111l1_opy_)
    return results
  except Exception:
    logger.error(bstack1ll111_opy_ (u"ࠥࡒࡴࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡸࡧࡵࡩࠥ࡬࡯ࡶࡰࡧ࠲ࠧ࿃"))
    return {}
@measure(event_name=EVENTS.bstack1l1ll1ll11_opy_, stage=STAGE.bstack11ll1111_opy_, bstack11l11l111_opy_=SESSION_NAME)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global PLATFORM_INDEX
  bstack1lll1l11ll_opy_ = not (bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ࿄"), None) and bstack11llll11l_opy_(
          threading.current_thread(), bstack1ll111_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ࿅"), None))
  bstack11llll11_opy_ = getattr(driver, bstack1ll111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࿆࠭"), None) != True
  bstack11l11l11ll_opy_ = bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ࿇"), None) and bstack11llll11l_opy_(
          threading.current_thread(), bstack1ll111_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ࿈"), None)
  if bstack11l11l11ll_opy_:
    if not bstack11ll1111l1_opy_():
      logger.warning(bstack1ll111_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡴࡵࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡂࡲࡳࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡹࡵ࡮࡯ࡤࡶࡾ࠴ࠢ࿉"))
      return {}
    logger.debug(bstack1ll111_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡲࡦࡵࡸࡰࡹࡹࠠࡴࡷࡰࡱࡦࡸࡹࠨ࿊"))
    logger.debug(perform_scan(driver, driver_command=bstack1ll111_opy_ (u"ࠫࡪࡾࡥࡤࡷࡷࡩࡘࡩࡲࡪࡲࡷࠫ࿋")))
    results = bstack1ll1ll11ll_opy_(bstack1ll111_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸࡘࡻ࡭࡮ࡣࡵࡽࠧ࿌"))
    if results is not None and results.get(bstack1ll111_opy_ (u"ࠨࡳࡶ࡯ࡰࡥࡷࡿࠢ࿍")) is not None:
        return results[bstack1ll111_opy_ (u"ࠢࡴࡷࡰࡱࡦࡸࡹࠣ࿎")]
    logger.error(bstack1ll111_opy_ (u"ࠣࡐࡲࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡗ࡫ࡳࡶ࡮ࡷࡷ࡙ࠥࡵ࡮࡯ࡤࡶࡾࠦࡷࡢࡵࠣࡪࡴࡻ࡮ࡥ࠰ࠥ࿏"))
    return {}
  if not bstack1ll11lll11_opy_.bstack1111l1ll1l_opy_(CONFIG, PLATFORM_INDEX) or (bstack11llll11_opy_ and bstack1lll1l11ll_opy_):
    logger.warning(bstack1ll111_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡸࡻ࡭࡮ࡣࡵࡽ࠳ࠨ࿐"))
    return {}
  try:
    logger.debug(bstack1ll111_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡲࡦࡵࡸࡰࡹࡹࠠࡴࡷࡰࡱࡦࡸࡹࠨ࿑"))
    logger.debug(perform_scan(driver))
    bstack111l1l1ll_opy_ = driver.execute_async_script(bstack1l1l1l1lll_opy_.bstack111ll1111l_opy_)
    return bstack111l1l1ll_opy_
  except Exception:
    logger.error(bstack1ll111_opy_ (u"ࠦࡓࡵࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡷࡰࡱࡦࡸࡹࠡࡹࡤࡷࠥ࡬࡯ࡶࡰࡧ࠲ࠧ࿒"))
    return {}
def bstack11ll1111l1_opy_():
  global CONFIG
  global PLATFORM_INDEX
  bstack11ll1lllll_opy_ = bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠬ࡯ࡳࡂࡲࡳࡅ࠶࠷ࡹࡕࡧࡶࡸࠬ࿓"), None) and bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ࿔"), None)
  if not bstack1ll11lll11_opy_.bstack1111l1ll1l_opy_(CONFIG, PLATFORM_INDEX) or not bstack11ll1lllll_opy_:
        logger.warning(bstack1ll111_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡲࡳࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡪࡺࡲࡪࡧࡹࡩࠥࡸࡥࡴࡷ࡯ࡸࡸ࠴ࠢ࿕"))
        return False
  return True
def bstack1ll1ll11ll_opy_(result_type):
    bstack11ll11ll1_opy_ = TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack11l1ll1111_opy_.current_hook_uuid()
    with ThreadPoolExecutor() as executor:
        future = executor.submit(bstack111l1l11l1_opy_(bstack11ll11ll1_opy_, result_type))
        try:
            return future.result(timeout=bstack111llllll_opy_)
        except TimeoutError:
            logger.error(bstack1ll111_opy_ (u"ࠣࡖ࡬ࡱࡪࡵࡵࡵࠢࡤࡪࡹ࡫ࡲࠡࡽࢀࡷࠥࡽࡨࡪ࡮ࡨࠤ࡫࡫ࡴࡤࡪ࡬ࡲ࡬ࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡒࡦࡵࡸࡰࡹࡹࠢ࿖").format(bstack111llllll_opy_))
        except Exception as ex:
            logger.debug(bstack1ll111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡴࡨࡸࡷ࡯ࡥࡷ࡫ࡱ࡫ࠥࡇࡰࡱࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡻࡾ࠰ࠣࡉࡷࡸ࡯ࡳࠢ࠰ࠤࢀࢃࠢ࿗").format(result_type, str(ex)))
    return {}
@measure(event_name=EVENTS.bstack1ll1l11ll1_opy_, stage=STAGE.bstack11ll1111_opy_, bstack11l11l111_opy_=SESSION_NAME)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global PLATFORM_INDEX
  bstack1lll1l11ll_opy_ = not (bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ࿘"), None) and bstack11llll11l_opy_(
          threading.current_thread(), bstack1ll111_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ࿙"), None))
  bstack1l1l1lll1l_opy_ = not (bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠬ࡯ࡳࡂࡲࡳࡅ࠶࠷ࡹࡕࡧࡶࡸࠬ࿚"), None) and bstack11llll11l_opy_(
          threading.current_thread(), bstack1ll111_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ࿛"), None))
  bstack11llll11_opy_ = getattr(driver, bstack1ll111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧ࿜"), None) != True
  if not bstack1ll11lll11_opy_.bstack1111l1ll1l_opy_(CONFIG, PLATFORM_INDEX) or (bstack11llll11_opy_ and bstack1lll1l11ll_opy_ and bstack1l1l1lll1l_opy_):
    logger.warning(bstack1ll111_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡷࡱࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸࡩࡡ࡯࠰ࠥ࿝"))
    return {}
  try:
    bstack1l111lll1l_opy_ = bstack1ll111_opy_ (u"ࠩࡤࡴࡵ࠭࿞") in CONFIG and CONFIG.get(bstack1ll111_opy_ (u"ࠪࡥࡵࡶࠧ࿟"), bstack1ll111_opy_ (u"ࠫࠬ࿠"))
    session_id = getattr(driver, bstack1ll111_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠩ࿡"), None)
    if not session_id:
      logger.warning(bstack1ll111_opy_ (u"ࠨࡎࡰࠢࡶࡩࡸࡹࡩࡰࡰࠣࡍࡉࠦࡦࡰࡷࡱࡨࠥ࡬࡯ࡳࠢࡧࡶ࡮ࡼࡥࡳࠤ࿢"))
      return {bstack1ll111_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨ࿣"): bstack1ll111_opy_ (u"ࠣࡐࡲࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡏࡄࠡࡨࡲࡹࡳࡪࠢ࿤")}
    if bstack1l111lll1l_opy_:
      try:
        bstack1l1lllllll_opy_ = {
              bstack1ll111_opy_ (u"ࠩࡷ࡬ࡏࡽࡴࡕࡱ࡮ࡩࡳ࠭࿥"): os.environ.get(bstack1ll111_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ࿦"), os.environ.get(bstack1ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ࿧"), bstack1ll111_opy_ (u"ࠬ࠭࿨"))),
              bstack1ll111_opy_ (u"࠭ࡴࡩࡖࡨࡷࡹࡘࡵ࡯ࡗࡸ࡭ࡩ࠭࿩"): TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack11l1ll1111_opy_.current_hook_uuid(),
              bstack1ll111_opy_ (u"ࠧࡢࡷࡷ࡬ࡍ࡫ࡡࡥࡧࡵࠫ࿪"): os.environ.get(bstack1ll111_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭࿫")),
              bstack1ll111_opy_ (u"ࠩࡶࡧࡦࡴࡔࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ࿬"): str(int(datetime.datetime.now().timestamp() * 1000)),
              bstack1ll111_opy_ (u"ࠪࡸ࡭ࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ࿭"): os.environ.get(bstack1ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ࿮"), bstack1ll111_opy_ (u"ࠬ࠭࿯")),
              bstack1ll111_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩ࠭࿰"): kwargs.get(bstack1ll111_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸ࡟ࡤࡱࡰࡱࡦࡴࡤࠨ࿱"), None) or bstack1ll111_opy_ (u"ࠨࠩ࿲")
          }
        if not hasattr(thread_local, bstack1ll111_opy_ (u"ࠩࡥࡥࡸ࡫࡟ࡢࡲࡳࡣࡦ࠷࠱ࡺࡡࡶࡧࡷ࡯ࡰࡵࠩ࿳")):
            scripts = {bstack1ll111_opy_ (u"ࠪࡷࡨࡧ࡮ࠨ࿴"): bstack1l1l1l1lll_opy_.perform_scan}
            thread_local.base_app_a11y_script = scripts
        bstack1lll1lll11_opy_ = copy.deepcopy(thread_local.base_app_a11y_script)
        bstack1lll1lll11_opy_[bstack1ll111_opy_ (u"ࠫࡸࡩࡡ࡯ࠩ࿵")] = bstack1lll1lll11_opy_[bstack1ll111_opy_ (u"ࠬࡹࡣࡢࡰࠪ࿶")] % json.dumps(bstack1l1lllllll_opy_)
        bstack1l1l1l1lll_opy_.bstack1lllll1l1_opy_(bstack1lll1lll11_opy_)
        bstack1l1l1l1lll_opy_.store()
        bstack1l1111llll_opy_ = driver.execute_script(bstack1l1l1l1lll_opy_.perform_scan)
      except Exception as bstack11l1111ll_opy_:
        logger.info(bstack1ll111_opy_ (u"ࠨࡁࡱࡲ࡬ࡹࡲࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡤࡣࡱࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࠨ࿷") + str(bstack11l1111ll_opy_))
        bstack1l1111llll_opy_ = {bstack1ll111_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨ࿸"): str(bstack11l1111ll_opy_)}
    else:
      bstack1l1111llll_opy_ = driver.execute_async_script(bstack1l1l1l1lll_opy_.perform_scan, {bstack1ll111_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࠨ࿹"): kwargs.get(bstack1ll111_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࡡࡦࡳࡲࡳࡡ࡯ࡦࠪ࿺"), None) or bstack1ll111_opy_ (u"ࠪࠫ࿻")})
    return bstack1l1111llll_opy_
  except Exception as err:
    logger.error(bstack1ll111_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡳࡷࡱࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸࡩࡡ࡯࠰ࠣࡿࢂࠨ࿼").format(str(err)))
    return {}