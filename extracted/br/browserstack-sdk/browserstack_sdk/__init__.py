# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
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
from browserstack_sdk.sdk_cli.bstack1l111l1lll_opy_ import bstack1lll11ll1_opy_
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from browserstack_sdk.bstack1l1l11111l_opy_ import bstack111lll1ll1_opy_
from browserstack_sdk.bstack11ll11llll_opy_ import *
import time
import requests
from bstack_utils.constants import EVENTS, STAGE, bstack1111l11l1_opy_
from bstack_utils.messages import bstack111ll1l111_opy_, bstack11l1ll11l1_opy_, bstack11l1111ll1_opy_, bstack11111l11l1_opy_, bstack1lll11ll_opy_, bstack1lll1ll1_opy_
from bstack_utils.measure import measure
from bstack_utils.logger_utils import get_logger
from bstack_utils.helper import bstack11l11ll1ll_opy_
from browserstack_sdk.bstack1ll11l111_opy_ import bstack1l1lllll_opy_
logger = get_logger(__name__)
def bstack1ll1l11l_opy_():
  global CONFIG
  headers = {
        bstack1ll1lll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack1ll1lll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack11l11ll1ll_opy_(CONFIG, bstack1111l11l1_opy_)
  try:
    response = requests.get(bstack1111l11l1_opy_, headers=headers, proxies=proxies, timeout=2)
    if response.json():
      bstack11lllll1l1_opy_ = response.json()[bstack1ll1lll_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack111ll1l111_opy_.format(response.json()))
      return bstack11lllll1l1_opy_
    else:
      logger.debug(bstack11l1ll11l1_opy_.format(bstack1ll1lll_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack11l1ll11l1_opy_.format(e))
def bstack1l1111l111_opy_(hub_url):
  global CONFIG
  url = bstack1ll1lll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack1ll1lll_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack1ll1lll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack1ll1lll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack11l11ll1ll_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=(0.5, 1.0))
    latency = time.perf_counter() - start_time
    logger.debug(bstack11l1111ll1_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack11111l11l1_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack11l1l1l11l_opy_, stage=STAGE.bstack1111l1ll1_opy_)
def bstack1l1llll11l_opy_():
  try:
    global bstack1l11ll1ll_opy_
    global CONFIG
    if bstack1ll1lll_opy_ (u"ࠫ࡭ࡻࡢࡓࡧࡪ࡭ࡴࡴࠧࡾ") in CONFIG and CONFIG[bstack1ll1lll_opy_ (u"ࠬ࡮ࡵࡣࡔࡨ࡫࡮ࡵ࡮ࠨࡿ")]:
      from bstack_utils.constants import bstack1111l1llll_opy_
      bstack11l11111l_opy_ = CONFIG[bstack1ll1lll_opy_ (u"࠭ࡨࡶࡤࡕࡩ࡬࡯࡯࡯ࠩࢀ")]
      if bstack11l11111l_opy_ in bstack1111l1llll_opy_:
        bstack1l11ll1ll_opy_ = bstack1111l1llll_opy_[bstack11l11111l_opy_]
        logger.debug(bstack1lll11ll_opy_.format(bstack1l11ll1ll_opy_))
        return
      else:
        logger.debug(bstack1ll1lll_opy_ (u"ࠢࡉࡷࡥࠤࡰ࡫ࡹࠡࠩࡾࢁࠬࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࡎࡕࡃࡡࡘࡖࡑࡥࡍࡂࡒ࠯ࠤ࡫ࡧ࡬࡭࡫ࡱ࡫ࠥࡨࡡࡤ࡭ࠣࡸࡴࠦ࡯ࡱࡶ࡬ࡱࡦࡲࠠࡩࡷࡥࠤࡩ࡫ࡴࡦࡥࡷ࡭ࡴࡴࠢࢁ").format(bstack11l11111l_opy_))
    bstack11lllll1l1_opy_ = bstack1ll1l11l_opy_()
    from concurrent.futures import ThreadPoolExecutor, as_completed
    if bstack11lllll1l1_opy_:
        with ThreadPoolExecutor(max_workers=len(bstack11lllll1l1_opy_)) as executor:
            bstack1l11llll11_opy_ = {executor.submit(bstack1l1111l111_opy_, bstack1l1ll1l11l_opy_): bstack1l1ll1l11l_opy_ for bstack1l1ll1l11l_opy_ in bstack11lllll1l1_opy_}
            for future in as_completed(bstack1l11llll11_opy_):
                result = future.result()
                if result and result.get(bstack1ll1lll_opy_ (u"ࠨ࡮ࡤࡸࡪࡴࡣࡺࠩࢂ")) is not None:
                    bstack1l11ll1ll_opy_ = result[bstack1ll1lll_opy_ (u"ࠩ࡫ࡹࡧࡥࡵࡳ࡮ࠪࢃ")]
                    logger.debug(bstack1lll11ll_opy_.format(bstack1l11ll1ll_opy_))
                    return
        bstack1l11ll1ll_opy_ = bstack11lllll1l1_opy_[0]
        logger.debug(bstack1lll11ll_opy_.format(bstack1l11ll1ll_opy_))
        return
  except Exception as e:
    logger.debug(bstack1lll1ll1_opy_.format(e))
from browserstack_sdk.bstack1111ll111_opy_ import *
from browserstack_sdk.bstack111l11l1ll_opy_ import bstack111l11111l_opy_
from browserstack_sdk.bstack1ll11l111_opy_ import *
from browserstack_sdk.bstack11ll1ll111_opy_ import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.logger_utils import get_logger
from bstack_utils.measure import measure
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack111ll111_opy_, stage=STAGE.bstack1111l1ll1_opy_)
def bstack1lll1ll1l1_opy_():
    global bstack1l11ll1ll_opy_
    try:
        bstack1lll11ll11_opy_ = bstack1llll1ll1l_opy_()
        bstack1ll1lll1ll_opy_(bstack1lll11ll11_opy_)
        hub_url = bstack1lll11ll11_opy_.get(bstack1ll1lll_opy_ (u"ࠥࡹࡷࡲࠢࢄ"), bstack1ll1lll_opy_ (u"ࠦࠧࢅ"))
        if hub_url.endswith(bstack1ll1lll_opy_ (u"ࠬ࠵ࡷࡥ࠱࡫ࡹࡧ࠭ࢆ")):
            hub_url = hub_url.rsplit(bstack1ll1lll_opy_ (u"࠭࠯ࡸࡦ࠲࡬ࡺࡨࠧࢇ"), 1)[0]
        if hub_url.startswith(bstack1ll1lll_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࠨ࢈")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack1ll1lll_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࠪࢉ")):
            hub_url = hub_url[8:]
        bstack1l11ll1ll_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack1llll1ll1l_opy_():
    global CONFIG
    bstack11llllll1l_opy_ = CONFIG.get(bstack1ll1lll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢊ"), {}).get(bstack1ll1lll_opy_ (u"ࠪ࡫ࡷ࡯ࡤࡏࡣࡰࡩࠬࢋ"), bstack1ll1lll_opy_ (u"ࠫࡓࡕ࡟ࡈࡔࡌࡈࡤࡔࡁࡎࡇࡢࡔࡆ࡙ࡓࡆࡆࠪࢌ"))
    if not isinstance(bstack11llllll1l_opy_, str):
        raise ValueError(bstack1ll1lll_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡌࡸࡩࡥࠢࡱࡥࡲ࡫ࠠ࡮ࡷࡶࡸࠥࡨࡥࠡࡣࠣࡺࡦࡲࡩࡥࠢࡶࡸࡷ࡯࡮ࡨࠤࢍ"))
    try:
        bstack1lll11ll11_opy_ = bstack1ll11lllll_opy_(bstack11llllll1l_opy_)
        return bstack1lll11ll11_opy_
    except Exception as e:
        logger.error(bstack1ll1lll_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡩࡵ࡭ࡩࠦࡤࡦࡶࡤ࡭ࡱࡹࠠ࠻ࠢࡾࢁࠧࢎ").format(str(e)))
        return {}
def bstack1ll11lllll_opy_(bstack11llllll1l_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack1ll1lll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ࢏")] or not CONFIG[bstack1ll1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ࢐")]:
            raise ValueError(bstack1ll1lll_opy_ (u"ࠤࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠤࡴࡸࠠࡢࡥࡦࡩࡸࡹࠠ࡬ࡧࡼࠦ࢑"))
        url = bstack11ll11111l_opy_ + bstack11llllll1l_opy_
        auth = (CONFIG[bstack1ll1lll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ࢒")], CONFIG[bstack1ll1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ࢓")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack11l111lll_opy_ = json.loads(response.text)
            return bstack11l111lll_opy_
    except ValueError as ve:
        logger.error(bstack1ll1lll_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡩࡵ࡭ࡩࠦࡤࡦࡶࡤ࡭ࡱࡹࠠ࠻ࠢࡾࢁࠧ࢔").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack1ll1lll_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡪࡶ࡮ࡪࠠࡥࡧࡷࡥ࡮ࡲࡳࠡ࠼ࠣࡿࢂࠨ࢕").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack1ll1lll1ll_opy_(bstack1l1l1l11ll_opy_):
    global CONFIG
    if bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ࢖") not in CONFIG or str(CONFIG[bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬࢗ")]).lower() == bstack1ll1lll_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ࢘"):
        CONFIG[bstack1ll1lll_opy_ (u"ࠪࡰࡴࡩࡡ࡭࢙ࠩ")] = False
    elif bstack1ll1lll_opy_ (u"ࠫ࡮ࡹࡔࡳ࡫ࡤࡰࡌࡸࡩࡥ࢚ࠩ") in bstack1l1l1l11ll_opy_:
        bstack111l1llll1_opy_ = CONFIG.get(bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴ࢛ࠩ"), {})
        logger.debug(bstack1ll1lll_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡸࡪࡵࡷ࡭ࡳ࡭ࠠ࡭ࡱࡦࡥࡱࠦ࡯ࡱࡶ࡬ࡳࡳࡹ࠺ࠡࠧࡶࠦ࢜"), bstack111l1llll1_opy_)
        bstack11l1l1ll1_opy_ = bstack1l1l1l11ll_opy_.get(bstack1ll1lll_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡒࡦࡲࡨࡥࡹ࡫ࡲࡴࠤ࢝"), [])
        bstack1l1l111l1l_opy_ = bstack1ll1lll_opy_ (u"ࠣ࠮ࠥ࢞").join(bstack11l1l1ll1_opy_)
        logger.debug(bstack1ll1lll_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡅࡸࡷࡹࡵ࡭ࠡࡴࡨࡴࡪࡧࡴࡦࡴࠣࡷࡹࡸࡩ࡯ࡩ࠽ࠤࠪࡹࠢ࢟"), bstack1l1l111l1l_opy_)
        bstack1l1ll11ll1_opy_ = {
            bstack1ll1lll_opy_ (u"ࠥࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧࢠ"): bstack1ll1lll_opy_ (u"ࠦࡦࡺࡳ࠮ࡴࡨࡴࡪࡧࡴࡦࡴࠥࢡ"),
            bstack1ll1lll_opy_ (u"ࠧ࡬࡯ࡳࡥࡨࡐࡴࡩࡡ࡭ࠤࢢ"): bstack1ll1lll_opy_ (u"ࠨࡴࡳࡷࡨࠦࢣ"),
            bstack1ll1lll_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࠭ࡳࡧࡳࡩࡦࡺࡥࡳࠤࢤ"): bstack1l1l111l1l_opy_
        }
        bstack111l1llll1_opy_.update(bstack1l1ll11ll1_opy_)
        logger.debug(bstack1ll1lll_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡖࡲࡧࡥࡹ࡫ࡤࠡ࡮ࡲࡧࡦࡲࠠࡰࡲࡷ࡭ࡴࡴࡳ࠻ࠢࠨࡷࠧࢥ"), bstack111l1llll1_opy_)
        CONFIG[bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢦ")] = bstack111l1llll1_opy_
        logger.debug(bstack1ll1lll_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡉ࡭ࡳࡧ࡬ࠡࡅࡒࡒࡋࡏࡇ࠻ࠢࠨࡷࠧࢧ"), CONFIG)
def get_turboscale_playwright_url():
    bstack1lll11ll11_opy_ = bstack1llll1ll1l_opy_()
    if not bstack1lll11ll11_opy_[bstack1ll1lll_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡖࡴ࡯ࠫࢨ")]:
      raise ValueError(bstack1ll1lll_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡗࡵࡰࠥ࡯ࡳࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡩࡶࡴࡳࠠࡨࡴ࡬ࡨࠥࡪࡥࡵࡣ࡬ࡰࡸ࠴ࠢࢩ"))
    return bstack1lll11ll11_opy_[bstack1ll1lll_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡘࡶࡱ࠭ࢪ")] + bstack1ll1lll_opy_ (u"ࠧࡀࡥࡤࡴࡸࡃࠧࢫ")
@measure(event_name=EVENTS.bstack11ll1l1111_opy_, stage=STAGE.bstack1111l1ll1_opy_)
def bstack1lllll1l1_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack1ll1lll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪࢬ")], CONFIG[bstack1ll1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬࢭ")])
        url = bstack1ll1ll1111_opy_
        logger.debug(bstack1ll1lll_opy_ (u"ࠥࡅࡹࡺࡥ࡮ࡲࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴࠢࡩࡶࡴࡳࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡔࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠣࡅࡕࡏࠢࢮ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack1ll1lll_opy_ (u"ࠦࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠥࢯ"): bstack1ll1lll_opy_ (u"ࠧࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠣࢰ")})
            if response.status_code == 200:
                bstack1lll11l1l_opy_ = json.loads(response.text)
                bstack1ll11l111l_opy_ = bstack1lll11l1l_opy_.get(bstack1ll1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡸ࠭ࢱ"), [])
                if bstack1ll11l111l_opy_:
                    bstack11l11ll1_opy_ = bstack1ll11l111l_opy_[0]
                    build_hashed_id = bstack11l11ll1_opy_.get(bstack1ll1lll_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪࢲ"))
                    bstack11ll1l1l_opy_ = bstack1ll111l1_opy_ + build_hashed_id
                    result.extend([build_hashed_id, bstack11ll1l1l_opy_])
                    logger.info(bstack1l1111lll1_opy_.format(bstack11ll1l1l_opy_))
                    bstack1lll1l1ll_opy_ = CONFIG[bstack1ll1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫࢳ")]
                    if bstack1ll1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࢴ") in CONFIG:
                      bstack1lll1l1ll_opy_ += bstack1ll1lll_opy_ (u"ࠪࠤࠬࢵ") + CONFIG[bstack1ll1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࢶ")]
                    if bstack1lll1l1ll_opy_ != bstack11l11ll1_opy_.get(bstack1ll1lll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪࢷ")):
                      logger.debug(bstack1lll1ll1l_opy_.format(bstack11l11ll1_opy_.get(bstack1ll1lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫࢸ")), bstack1lll1l1ll_opy_))
                    return result
                else:
                    logger.debug(bstack1ll1lll_opy_ (u"ࠢࡂࡖࡖࠤ࠿ࠦࡎࡰࠢࡥࡹ࡮ࡲࡤࡴࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠱ࠦࢹ"))
            else:
                logger.debug(bstack1ll1lll_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴ࠰ࠥࢺ"))
        except Exception as e:
            logger.error(bstack1ll1lll_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࡶࠤ࠿ࠦࡻࡾࠤࢻ").format(str(e)))
    else:
        logger.debug(bstack1ll1lll_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡆࡓࡓࡌࡉࡈࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡶࡩࡹ࠴ࠠࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴ࠰ࠥࢼ"))
    return [None, None]
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack11llllll11_opy_ import bstack11llllll11_opy_, Events, bstack1lll11l11l_opy_, bstack1l1llll1_opy_
from bstack_utils.measure import bstack1l111ll111_opy_
from bstack_utils.measure import measure
from bstack_utils.percy import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1ll1l1llll_opy_ import bstack11l111l1ll_opy_
from bstack_utils.messages import *
from bstack_utils import logger_utils
from bstack_utils.constants import *
from bstack_utils.helper import bstack111l1lll11_opy_, bstack111lll1l11_opy_, bstack11l11l11ll_opy_, bstack1l11lll1_opy_, \
  bstack1111111l11_opy_, \
  Notset, is_robot_playwright_installed, bstack1ll1ll11ll_opy_, \
  bstack1l111llll1_opy_, bstack1l1ll1l111_opy_, bstack1l1111llll_opy_, bstack1ll11l1l11_opy_, bstack1111ll11_opy_, bstack1lllllll1l_opy_, \
  bstack11l11111l1_opy_, \
  bstack1llllll11l_opy_, bstack1l1l111111_opy_, bstack1lll1ll111_opy_, bstack11lll1llll_opy_, \
  bstack1ll1llll1_opy_, bstack11l1ll1lll_opy_, bstack1l11l11111_opy_, bstack1111l11lll_opy_, bstack111l1lll_opy_
from bstack_utils.bstack111111111_opy_ import bstack1l11l1ll_opy_
from bstack_utils.bstack111ll11ll1_opy_ import bstack1llllllll_opy_, bstack111ll1l11_opy_
from bstack_utils.bstack1111l1ll11_opy_ import bstack1ll1ll1ll_opy_
from bstack_utils.session_utils import bstack1ll1lll1l_opy_, bstack1ll1l1lll1_opy_
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.bstack1111l1l11_opy_ import bstack11ll111lll_opy_
from bstack_utils.proxy import bstack11ll111ll1_opy_, bstack11l11ll1ll_opy_, bstack111l111ll1_opy_, bstack111111l11_opy_
from bstack_utils.bstack111ll1llll_opy_ import bstack1ll1l11ll_opy_, bstack1l1ll1l1ll_opy_
import bstack_utils.bstack111l111lll_opy_ as TestHubUtils
import bstack_utils.bstack1ll11lll1_opy_ as bstack1l11ll1l1_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.utils.bstack1l1l1l1ll_opy_ import bstack11l1111l1l_opy_
from bstack_utils.bstack1lll111ll_opy_ import bstack1l111111l1_opy_
from bstack_utils.bstack1lll1lllll_opy_ import bstack1l1l11l11_opy_
from bstack_utils.bstack1l111ll111_opy_ import bstack1l1l11ll1_opy_
if os.getenv(bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡉࡑࡒࡏࡘ࠭ࢽ")):
  cli.bstack1lll111l1_opy_()
else:
  os.environ[bstack1ll1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡊࡒࡓࡐ࡙ࠧࢾ")] = bstack1ll1lll_opy_ (u"࠭ࡴࡳࡷࡨࠫࢿ")
bstack1ll1l1l1ll_opy_ = bstack1ll1lll_opy_ (u"ࠧࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠠࠡ࡫ࡩࠬࡵࡧࡧࡦࠢࡀࡁࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠠࡼ࡞ࡱࠤࠥࠦࡴࡳࡻࡾࡠࡳࠦࡣࡰࡰࡶࡸࠥ࡬ࡳࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࡡ࠭ࡦࡴ࡞ࠪ࠭ࡀࡢ࡮ࠡࠢࠣࠤࠥ࡬ࡳ࠯ࡣࡳࡴࡪࡴࡤࡇ࡫࡯ࡩࡘࡿ࡮ࡤࠪࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠬࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡳࡣ࡮ࡴࡤࡦࡺࠬࠤ࠰ࠦࠢ࠻ࠤࠣ࠯ࠥࡐࡓࡐࡐ࠱ࡷࡹࡸࡩ࡯ࡩ࡬ࡪࡾ࠮ࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࠬࡦࡽࡡࡪࡶࠣࡲࡪࡽࡐࡢࡩࡨ࠶࠳࡫ࡶࡢ࡮ࡸࡥࡹ࡫ࠨࠣࠪࠬࠤࡂࡄࠠࡼࡿࠥ࠰ࠥࡢࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡨࡧࡷࡗࡪࡹࡳࡪࡱࡱࡈࡪࡺࡡࡪ࡮ࡶࠦࢂࡢࠧࠪࠫࠬ࡟ࠧ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠣ࡟ࠬࠤ࠰ࠦࠢ࠭࡞࡟ࡲࠧ࠯࡜࡯ࠢࠣࠤࠥࢃࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡽ࡝ࡰࠣࠤ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠧࣀ")
LAUNCH_PATCH_ROBOT_PLAYWRIGHT = bstack1ll1lll_opy_ (u"ࠨ࡞ࡱ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࡢ࡮ࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠻࡝ࠡ࠿ࡀࡁࠥࡢࠧࡵࡴࡸࡩࡡ࠭࡜࡯ࡥࡲࡲࡸࡺࠠࡣࡵࡷࡥࡨࡱ࡟ࡱࡣࡷ࡬ࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴࡟࡟ࡲࡨࡵ࡮ࡴࡶࠣࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࡝ࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠵ࡢࡢ࡮ࡤࡱࡱࡷࡹࠦࡰࡠ࡫ࡱࡨࡪࡾࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠵ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠵࡟ࠣࡁࡂࡃࠠ࡝ࠩࡷࡶࡺ࡫࡜ࠨ࡞ࡱࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡷࡱ࡯ࡣࡦࠪ࠳࠰ࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠵ࠪ࡞ࡱࡧࡴࡴࡳࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣࠫ࠾ࡠࡳࡩ࡯࡯ࡵࡷࠤࡴࡸࡩࡨ࡫ࡱࡥࡱࡥࡣࡩࡴࡲࡱ࡮ࡻ࡭ࡠ࡮ࡤࡹࡳࡩࡨࠡ࠿ࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡰࡦࡻ࡮ࡤࡪ࠱ࡦ࡮ࡴࡤࠩ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭ࠪ࠽࡟ࡲ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡱࡧࡵ࡯ࡥ࡫ࠤࡂࠦࡡࡴࡻࡱࡧࠥ࠮࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸ࠯ࠠ࠾ࡀࠣࡿࡡࡴࡩࡧࠢࠫࠥࡧࡹࡴࡢࡥ࡮ࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠪࠢࡾࡠࡳࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦ࡯ࡳ࡫ࡪ࡭ࡳࡧ࡬ࡠࡥ࡫ࡶࡴࡳࡩࡶ࡯ࡢࡰࡦࡻ࡮ࡤࡪࠫࡰࡦࡻ࡮ࡤࡪࡒࡴࡹ࡯࡯࡯ࡵࠬ࠿ࡡࡴࡽ࡝ࡰ࡯ࡩࡹࠦࡣࡢࡲࡶ࠿ࡡࡴࡴࡳࡻࠣࡿࡡࡴࡣࡢࡲࡶࠤࡂࠦࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠪ࡞ࡱࠤࠥࢃࠠࡤࡣࡷࡧ࡭࠮ࡥࡹࠫࠣࡿࡡࡴࠠࠡࠢࠣࢁࡡࡴࠠࠡ࡫ࡩࠤ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࠮ࠦࡻ࡝ࡰࠣࠤࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡩ࡯࡯ࡰࡨࡧࡹࡕࡶࡦࡴࡆࡈࡕ࠮ࡻ࡝ࡰࠣࠤࠥࠦࠠࠡࡧࡱࡨࡵࡵࡩ࡯ࡶࡘࡖࡑࡀࠠࡡࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠧࡿࡪࡴࡣࡰࡦࡨ࡙ࡗࡏࡃࡰ࡯ࡳࡳࡳ࡫࡮ࡵࠪࡍࡗࡔࡔ࠮ࡴࡶࡵ࡭ࡳ࡭ࡩࡧࡻࠫࡧࡦࡶࡳࠪࠫࢀࡤ࠱ࡢ࡮ࠡࠢࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴ࡞ࡱࠤࠥࠦࠠࡾࠫ࡟ࡲࠥࠦࡽ࡝ࡰࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࠻ࠢࡣࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠩࢁࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭ࢂࡦࠬ࡝ࡰࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴ࡞ࡱࠤࠥࢃࠩ࡝ࡰࢀࡠࡳࡩ࡯࡯ࡵࡷࠤࡴࡸࡩࡨ࡫ࡱࡥࡱࡥࡣࡰࡰࡱࡩࡨࡺࠠ࠾ࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱ࠮ࡤࡪࡵࡳࡲ࡯ࡵ࡮࠰ࡦࡳࡳࡴࡥࡤࡶ࠱ࡦ࡮ࡴࡤࠩ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭ࠪ࠽࡟ࡲ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡨࡵ࡮࡯ࡧࡦࡸࠥࡃࠠࡢࡵࡼࡲࡨࠦࠨࡤࡱࡱࡲࡪࡩࡴࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁ࡜࡯ࠢࠣ࡭࡫ࠦࠨࠢࡤࡶࡸࡦࡩ࡫ࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠮ࠦࡻ࡝ࡰࠣࠤࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥࡵࡲࡪࡩ࡬ࡲࡦࡲ࡟ࡤࡱࡱࡲࡪࡩࡴࠩࡥࡲࡲࡳ࡫ࡣࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠫ࠾ࡠࡳࠦࠠࡾ࡞ࡱࠤࠥࡲࡥࡵࠢࡦࡥࡵࡹ࠻࡝ࡰࠣࠤࡹࡸࡹࠡࡽ࡟ࡲࠥࠦࠠࠡࡥࡤࡴࡸࠦ࠽ࠡࡌࡖࡓࡓ࠴ࡰࡢࡴࡶࡩ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡩࡡࡱࡵࠬࡠࡳࠦࠠࡾࠢࡦࡥࡹࡩࡨࠩࡧࡻ࠭ࠥࢁ࡜࡯ࠢࠣࢁࡡࡴࠠࠡࡥࡲࡲࡸࡺࠠ࡮ࡱࡧ࡭࡫࡯ࡥࡥࡇࡱࡨࡵࡵࡩ࡯ࡶࠣࡁࠥࡦࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࡡࠢ࠮ࠤࡪࡴࡣࡰࡦࡨ࡙ࡗࡏࡃࡰ࡯ࡳࡳࡳ࡫࡮ࡵࠪࡍࡗࡔࡔ࠮ࡴࡶࡵ࡭ࡳ࡭ࡩࡧࡻࠫࡧࡦࡶࡳࠪࠫ࠾ࡠࡳࠦࠠࡪࡨࠣࠬࡧࡹࡴࡢࡥ࡮ࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ࠭ࠥࢁ࡜࡯ࠢࠣࠤࠥࡸࡥࡵࡷࡵࡲࠥࡧࡷࡢ࡫ࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡨࡵ࡮࡯ࡧࡦࡸࡔࡼࡥࡳࡅࡇࡔ࠭ࢁ࡜࡯ࠢࠣࠤࠥࠦࠠࡦࡰࡧࡴࡴ࡯࡮ࡵࡗࡕࡐ࠿ࠦ࡭ࡰࡦ࡬ࡪ࡮࡫ࡤࡆࡰࡧࡴࡴ࡯࡮ࡵ࠮࡟ࡲࠥࠦࠠࠡࠢࠣ࠲࠳࠴ࡣࡰࡰࡱࡩࡨࡺࡏࡱࡶ࡬ࡳࡳࡹ࡜࡯ࠢࠣࠤࠥࢃࠩ࡝ࡰࠣࠤࢂࡢ࡮ࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤ࠳࠴࠮ࡤࡱࡱࡲࡪࡩࡴࡐࡲࡷ࡭ࡴࡴࡳ࠭࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࡝ࡰࠣࠤࢂ࠯࡜࡯ࡿ࡟ࡲࡱ࡫ࡴࠡࡄࡵࡳࡼࡹࡥࡳࡅࡲࡲࡹ࡫ࡸࡵ࠽࡟ࡲࡹࡸࡹࠡࡽ࡟ࡲࠥࠦࡣࡰࡰࡶࡸࠥࡶࡡࡵࡪࡐࡳࡩࡻ࡬ࡦࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭ࠨࡰࡢࡶ࡫ࠦ࠮ࡁ࡜࡯ࠢࠣࡧࡴࡴࡳࡵࠢࡳࡻࡈࡵࡲࡦࡒࡤࡸ࡭ࠦ࠽ࠡࡲࡤࡸ࡭ࡓ࡯ࡥࡷ࡯ࡩ࠳ࡪࡩࡳࡰࡤࡱࡪ࠮ࡲࡦࡳࡸ࡭ࡷ࡫࠮ࡳࡧࡶࡳࡱࡼࡥࠩࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠳ࡣࡰࡴࡨ࠳ࡵࡧࡣ࡬ࡣࡪࡩ࠳ࡰࡳࡰࡰࠥ࠭࠮ࡁ࡜࡯ࠢࠣࡆࡷࡵࡷࡴࡧࡵࡇࡴࡴࡴࡦࡺࡷࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨࡱࡣࡷ࡬ࡒࡵࡤࡶ࡮ࡨ࠲࡯ࡵࡩ࡯ࠪࡳࡻࡈࡵࡲࡦࡒࡤࡸ࡭࠲ࠠࠣ࡮࡬ࡦ࠴ࡩ࡬ࡪࡧࡱࡸ࠴ࡨࡲࡰࡹࡶࡩࡷࡉ࡯࡯ࡶࡨࡼࡹࠨࠩࠪ࠰ࡅࡶࡴࡽࡳࡦࡴࡆࡳࡳࡺࡥࡹࡶ࠾ࡠࡳࢃࠠࡤࡣࡷࡧ࡭ࠦࠨࡦࠫࠣࡿࡡࡴࠠࠡࡥࡲࡲࡸࡵ࡬ࡦ࠰ࡺࡥࡷࡴࠨࠣࡅࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡱࡵࡡࡥࠢࡅࡶࡴࡽࡳࡦࡴࡆࡳࡳࡺࡥࡹࡶࠣࡪࡷࡵ࡭ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠲ࡩ࡯ࡳࡧ࠽ࠦ࠱ࠦࡥ࠯࡯ࡨࡷࡸࡧࡧࡦࠫ࠾ࡠࡳࢃ࡜࡯ࡥࡲࡲࡸࡺࠠࡰࡴ࡬࡫࡮ࡴࡡ࡭ࡡࡱࡩࡼࡖࡡࡨࡧࠣࡁࠥࡈࡲࡰࡹࡶࡩࡷࡉ࡯࡯ࡶࡨࡼࡹ࠴ࡰࡳࡱࡷࡳࡹࡿࡰࡦ࠰ࡱࡩࡼࡖࡡࡨࡧ࠾ࡠࡳࡈࡲࡰࡹࡶࡩࡷࡉ࡯࡯ࡶࡨࡼࡹ࠴ࡰࡳࡱࡷࡳࡹࡿࡰࡦ࠰ࡱࡩࡼࡖࡡࡨࡧࠣࡁࠥࡧࡳࡺࡰࡦࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠮ࠩࠡࡽ࡟ࡲࠥࠦࡩࡧࠢࠫࡦࡸࡺࡡࡤ࡭ࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠬࠤࢀࡢ࡮ࠡࠢࠣࠤࡹࡸࡹࠡࡽ࡟ࡲࠥࠦࠠࠡࠢࠣࡧࡴࡴࡳࡵࠢࡥࡶࡴࡽࡳࡦࡴࠣࡁࠥࡺࡨࡪࡵ࠱ࡦࡷࡵࡷࡴࡧࡵࠤࠫࠬࠠࡵࡪ࡬ࡷ࠳ࡨࡲࡰࡹࡶࡩࡷ࠮ࠩ࠼࡞ࡱࠤࠥࠦࠠࠡࠢ࡯ࡩࡹࠦࡰࡳ࡫ࡰࡥࡷࡿࡃࡰࡰࡷࡩࡽࡺࠠ࠾ࠢࡥࡶࡴࡽࡳࡦࡴࠣࠪࠫࠦࡴࡺࡲࡨࡳ࡫ࠦࡢࡳࡱࡺࡷࡪࡸ࠮ࡤࡱࡱࡸࡪࡾࡴࡴࠢࡀࡁࡂࠦ࡜ࠨࡨࡸࡲࡨࡺࡩࡰࡰ࡟ࠫࠥࡅࠠࡣࡴࡲࡻࡸ࡫ࡲ࠯ࡥࡲࡲࡹ࡫ࡸࡵࡵࠫ࠭ࡠ࠶࡝ࠡ࠼ࠣࡲࡺࡲ࡬࠼࡞ࡱࠤࠥࠦࠠࠡࠢ࡬ࡪࠥ࠮ࠡࡱࡴ࡬ࡱࡦࡸࡹࡄࡱࡱࡸࡪࡾࡴࠡࠨࠩࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࠬࠦࠡࡶࡼࡴࡪࡵࡦࠡࡤࡵࡳࡼࡹࡥࡳ࠰ࡱࡩࡼࡉ࡯࡯ࡶࡨࡼࡹࠦ࠽࠾࠿ࠣࡠࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡜ࠨࠫࠣࡿࡡࡴࠠࠡࠢࠣࠤࠥࠦࠠࡱࡴ࡬ࡱࡦࡸࡹࡄࡱࡱࡸࡪࡾࡴࠡ࠿ࠣࡥࡼࡧࡩࡵࠢࡥࡶࡴࡽࡳࡦࡴ࠱ࡲࡪࡽࡃࡰࡰࡷࡩࡽࡺࠨࠪ࠽࡟ࡲࠥࠦࠠࠡࠢࠣࢁࡡࡴࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡵࡷࠤࡹࡧࡲࡨࡧࡷࡇࡴࡴࡴࡦࡺࡷࠤࡂࠦࡰࡳ࡫ࡰࡥࡷࡿࡃࡰࡰࡷࡩࡽࡺࠠࡽࡾࠣࡸ࡭࡯ࡳ࠼࡞ࡱࠤࠥࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡲࡪࡽࡐࡢࡩࡨ࠲ࡨࡧ࡬࡭ࠪࡷࡥࡷ࡭ࡥࡵࡅࡲࡲࡹ࡫ࡸࡵࠫ࠾ࡠࡳࠦࠠࠡࠢࢀࠤࡨࡧࡴࡤࡪࠣࠬࡪ࠯ࠠࡼ࡞ࡱࠤࠥࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡲࡪࡽࡐࡢࡩࡨ࠲ࡨࡧ࡬࡭ࠪࡷ࡬࡮ࡹࠩ࠼࡞ࡱࠤࠥࠦࠠࡾ࡞ࡱࠤࠥࢃࠠ࡝ࡰࠣࠤࡪࡲࡳࡦࠢࡾࡠࡳࠦࠠࠡࠢࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣࡳࡷ࡯ࡧࡪࡰࡤࡰࡤࡴࡥࡸࡒࡤ࡫ࡪ࠴ࡣࡢ࡮࡯ࠬࡹ࡮ࡩࡴࠫ࠾ࡠࡳࠦࠠࡾ࡞ࡱࢁࡀࡢ࡮࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱࡟ࡲࠬࣁ")
from ._version import __version__
bstack1l111llll_opy_ = None
CONFIG = {}
bstack11lllll1l_opy_ = {}
bstack11l1ll11l_opy_ = {}
bstack1lllll1ll1_opy_ = None
bstack1l1l1llll1_opy_ = None
SESSION_NAME = None
PLATFORM_INDEX = -1
bstack11ll1l11_opy_ = 0
bstack1l11l11ll_opy_ = bstack1l1111ll_opy_
bstack1ll1ll11_opy_ = 1
PARALLELISE_VANILLA_PYTHON = False
PARALLELISE_THREADING_PYTHON = False
FRAMEWORK_NAME = bstack1ll1lll_opy_ (u"ࠩࠪࣂ")
bstack1l1l11111_opy_ = bstack1ll1lll_opy_ (u"ࠪࠫࣃ")
bstack111l11l11_opy_ = False
BROWSERSTACK_AUTOMATION = True
bstack111l1ll1l_opy_ = False
bstack1l11l111_opy_ = bstack1ll1lll_opy_ (u"ࠫࠬࣄ")
bstack11ll1llll_opy_ = []
bstack1l1l1ll1l_opy_ = threading.Lock()
bstack1l11l1llll_opy_ = threading.Lock()
bstack11111l11ll_opy_ = None
bstack1l11ll1ll_opy_ = bstack1ll1lll_opy_ (u"ࠬ࠭ࣅ")
SELENIUM_OR_PLAYWRIGHT_INSTALLED = False
bstack1l11ll1l1l_opy_ = None
bstack111ll1l1_opy_ = None
bstack1111l1l1ll_opy_ = None
bstack11ll111l11_opy_ = -1
bstack11l1111111_opy_ = os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"࠭ࡾࠨࣆ")), bstack1ll1lll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧࣇ"), bstack1ll1lll_opy_ (u"ࠨ࠰ࡵࡳࡧࡵࡴ࠮ࡴࡨࡴࡴࡸࡴ࠮ࡪࡨࡰࡵ࡫ࡲ࠯࡬ࡶࡳࡳ࠭ࣈ"))
bstack11l111l1l_opy_ = 0
bstack1111111l_opy_ = 0
bstack1lll1l111l_opy_ = []
bstack11lll1ll1_opy_ = []
ROBOT_PYTHON_ERRORS = []
bstack11l11lll_opy_ = []
bstack1l111l111_opy_ = bstack1ll1lll_opy_ (u"ࠩࠪࣉ")
bstack111llll1_opy_ = bstack1ll1lll_opy_ (u"ࠪࠫ࣊")
bstack1ll11l1l_opy_ = False
bstack111ll11l1l_opy_ = False
bstack1l11ll11l1_opy_ = {}
bstack1l1lll1l11_opy_ = {}
bstack1l1ll11l_opy_ = None
bstack1l1l1l111_opy_ = None
bstack111lll1l1l_opy_ = None
bstack111111l1l_opy_ = None
bstack111l11ll_opy_ = None
bstack1ll1l1l1l1_opy_ = None
bstack1111l11l11_opy_ = None
bstack11l111lll1_opy_ = None
bstack11l1l111_opy_ = None
bstack1lllll1lll_opy_ = None
bstack1111111l1l_opy_ = None
bstack111l11lll1_opy_ = None
bstack1l11111ll_opy_ = None
bstack1l111lll11_opy_ = None
bstack1ll11ll1l1_opy_ = None
bstack1ll1llll11_opy_ = None
bstack11lll11l11_opy_ = None
bstack1llll1l1ll_opy_ = None
bstack1l1lll1l_opy_ = None
bstack1l11lll1l1_opy_ = None
bstack1l1llll1ll_opy_ = None
bstack111l11ll1l_opy_ = None
bstack1l1ll1ll_opy_ = None
thread_local = threading.local()
bstack1l1llll1l1_opy_ = False
bstack1l1l1l111l_opy_ = bstack1ll1lll_opy_ (u"ࠦࠧ࣋")
_1111l1l1_opy_ = None
logger = logger_utils.get_logger(__name__, bstack1l11l11ll_opy_)
automation_logger = logger_utils.get_automation_logger(__name__)
global_config = Config.get_instance()
percy = bstack1lll1ll1ll_opy_()
bstack1l111ll1l_opy_ = bstack11l111l1ll_opy_()
bstack11l11111_opy_ = bstack11ll1ll111_opy_()
def bstack1111lll11l_opy_():
  global CONFIG
  global bstack1ll11l1l_opy_
  global global_config
  testContextOptions = bstack1111llll1l_opy_(CONFIG)
  if bstack1111111l11_opy_(CONFIG):
    if (bstack1ll1lll_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ࣌") in testContextOptions and str(testContextOptions[bstack1ll1lll_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ࣍")]).lower() == bstack1ll1lll_opy_ (u"ࠧࡵࡴࡸࡩࠬ࣎")):
      bstack1ll11l1l_opy_ = True
      global_config.bstack1lllll11l_opy_(True)
    if (bstack1ll1lll_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷ࣏ࠬ") in testContextOptions and str(testContextOptions[bstack1ll1lll_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࣐࠭")]).lower() == bstack1ll1lll_opy_ (u"ࠪࡸࡷࡻࡥࠨ࣑")):
      global_config.bstack1ll11111ll_opy_(True)
  else:
    bstack1ll11l1l_opy_ = True
    global_config.bstack1lllll11l_opy_(True)
    global_config.bstack1ll11111ll_opy_(True)
def bstack111lll1lll_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1l1l11l1l1_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1ll111l11l_opy_():
  global bstack1l1lll1l11_opy_
  args = sys.argv
  for i in range(len(args)):
    if bstack1ll1lll_opy_ (u"ࠦ࠲࠳ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡨࡵ࡮ࡧ࡫ࡪࡪ࡮ࡲࡥ࣒ࠣ") == args[i].lower() or bstack1ll1lll_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰࡰࡩ࡭࡬ࠨ࣓") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      bstack1l1lll1l11_opy_[bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࡤࡌࡉࡍࡇࠪࣔ")] = path
      return path
  return None
bstack1llll1ll11_opy_ = re.compile(bstack1ll1lll_opy_ (u"ࡲࠣ࠰࠭ࡃࡡࠪࡻࠩ࠰࠭ࡃ࠮ࢃ࠮ࠫࡁࠥࣕ"))
def bstack1lllll1l1l_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1llll1ll11_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack1ll1lll_opy_ (u"ࠣࠦࡾࠦࣖ") + group + bstack1ll1lll_opy_ (u"ࠤࢀࠦࣗ"), os.environ.get(group))
  return value
def bstack111lllll1l_opy_():
  global bstack1l1ll1ll_opy_
  if bstack1l1ll1ll_opy_ is None:
        bstack1l1ll1ll_opy_ = bstack1ll111l11l_opy_()
  bstack1l1ll11l11_opy_ = bstack1l1ll1ll_opy_
  if bstack1l1ll11l11_opy_ and os.path.exists(os.path.abspath(bstack1l1ll11l11_opy_)):
    fileName = bstack1l1ll11l11_opy_
  if bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋࠧࣘ") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨࣙ")])) and not bstack1ll1lll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡑࡥࡲ࡫ࠧࣚ") in locals():
    fileName = os.environ[bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࡤࡌࡉࡍࡇࠪࣛ")]
  if bstack1ll1lll_opy_ (u"ࠧࡧ࡫࡯ࡩࡓࡧ࡭ࡦࠩࣜ") in locals():
    bstack111lll_opy_ = os.path.abspath(fileName)
  else:
    bstack111lll_opy_ = bstack1ll1lll_opy_ (u"ࠨࠩࣝ")
  bstack1111llll_opy_ = os.getcwd()
  bstack111111111l_opy_ = bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬࣞ")
  bstack111l1111l_opy_ = bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡥࡲࡲࠧࣟ")
  while (not os.path.exists(bstack111lll_opy_)) and bstack1111llll_opy_ != bstack1ll1lll_opy_ (u"ࠦࠧ࣠"):
    bstack111lll_opy_ = os.path.join(bstack1111llll_opy_, bstack111111111l_opy_)
    if not os.path.exists(bstack111lll_opy_):
      bstack111lll_opy_ = os.path.join(bstack1111llll_opy_, bstack111l1111l_opy_)
    if bstack1111llll_opy_ != os.path.dirname(bstack1111llll_opy_):
      bstack1111llll_opy_ = os.path.dirname(bstack1111llll_opy_)
    else:
      bstack1111llll_opy_ = bstack1ll1lll_opy_ (u"ࠧࠨ࣡")
  bstack1l1ll1ll_opy_ = bstack111lll_opy_ if os.path.exists(bstack111lll_opy_) else None
  return bstack1l1ll1ll_opy_
def bstack1ll11l11ll_opy_(config):
    if bstack1ll1lll_opy_ (u"࠭ࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬࠭࣢") in config:
      config[bstack1ll1lll_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࣣࠫ")] = config[bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹࡘࡥࡱࡱࡵࡸ࡮ࡴࡧࠨࣤ")]
    if bstack1ll1lll_opy_ (u"ࠩࡷࡩࡸࡺࡒࡦࡲࡲࡶࡹ࡯࡮ࡨࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣥ") in config:
      config[bstack1ll1lll_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࣦࠧ")] = config[bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࡓࡵࡺࡩࡰࡰࡶࠫࣧ")]
def bstack1l1ll11l1_opy_():
  bstack111lll_opy_ = bstack111lllll1l_opy_()
  if not os.path.exists(bstack111lll_opy_):
    bstack1lll1111l_opy_(
      bstack11lllll11_opy_.format(os.getcwd()))
  try:
    with open(bstack111lll_opy_, bstack1ll1lll_opy_ (u"ࠬࡸࠧࣨ")) as stream:
      yaml.add_implicit_resolver(bstack1ll1lll_opy_ (u"ࠨࠡࡱࡣࡷ࡬ࡪࡾࣩࠢ"), bstack1llll1ll11_opy_)
      yaml.add_constructor(bstack1ll1lll_opy_ (u"ࠢࠢࡲࡤࡸ࡭࡫ࡸࠣ࣪"), bstack1lllll1l1l_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      bstack1ll11l11ll_opy_(config)
      return config
  except:
    with open(bstack111lll_opy_, bstack1ll1lll_opy_ (u"ࠨࡴࠪ࣫")) as stream:
      try:
        config = yaml.safe_load(stream)
        bstack1ll11l11ll_opy_(config)
        return config
      except yaml.YAMLError as exc:
        bstack1lll1111l_opy_(bstack1ll11ll1_opy_.format(str(exc)))
def bstack1l11l111l1_opy_(config):
  bstack111l11111_opy_ = bstack11ll1111_opy_(config)
  for option in list(bstack111l11111_opy_):
    if option.lower() in bstack111ll111l1_opy_ and option != bstack111ll111l1_opy_[option.lower()]:
      bstack111l11111_opy_[bstack111ll111l1_opy_[option.lower()]] = bstack111l11111_opy_[option]
      del bstack111l11111_opy_[option]
  return config
def bstack11ll1111l1_opy_():
  global bstack11l1ll11l_opy_
  for key, bstack111ll11lll_opy_ in bstack1l11lllll_opy_.items():
    if isinstance(bstack111ll11lll_opy_, list):
      for var in bstack111ll11lll_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack11l1ll11l_opy_[key] = os.environ[var]
          break
    elif bstack111ll11lll_opy_ in os.environ and os.environ[bstack111ll11lll_opy_] and str(os.environ[bstack111ll11lll_opy_]).strip():
      bstack11l1ll11l_opy_[key] = os.environ[bstack111ll11lll_opy_]
  if bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ࣬") in os.environ:
    bstack11l1ll11l_opy_[bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹ࣭ࠧ")] = {}
    bstack11l1ll11l_opy_[bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ࣮")][bstack1ll1lll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣯ࠧ")] = os.environ[bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨࣰ")]
def bstack1l11lllll1_opy_():
  global bstack11lllll1l_opy_
  global bstack1l11l111_opy_
  global bstack1l1lll1l11_opy_
  bstack11111ll11l_opy_ = []
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) - 1 and bstack1ll1lll_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࣱࠪ").lower() == val.lower():
      bstack11lllll1l_opy_[bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࣲࠬ")] = {}
      bstack11lllll1l_opy_[bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࣳ")][bstack1ll1lll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣴ")] = sys.argv[idx + 1]
      bstack11111ll11l_opy_.extend([idx, idx + 1])
      break
  for key, bstack1111ll11l1_opy_ in bstack1lllll11l1_opy_.items():
    if isinstance(bstack1111ll11l1_opy_, list):
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        for var in bstack1111ll11l1_opy_:
          if bstack1ll1lll_opy_ (u"ࠫ࠲࠳ࠧࣵ") + var.lower() == val.lower() and key not in bstack11lllll1l_opy_:
            bstack11lllll1l_opy_[key] = sys.argv[idx + 1]
            bstack1l11l111_opy_ += bstack1ll1lll_opy_ (u"ࠬࠦ࠭࠮ࣶࠩ") + var + bstack1ll1lll_opy_ (u"࠭ࠠࠨࣷ") + shlex.quote(sys.argv[idx + 1])
            bstack111l1lll_opy_(bstack1l1lll1l11_opy_, key, sys.argv[idx + 1])
            bstack11111ll11l_opy_.extend([idx, idx + 1])
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        if bstack1ll1lll_opy_ (u"ࠧ࠮࠯ࠪࣸ") + bstack1111ll11l1_opy_.lower() == val.lower() and key not in bstack11lllll1l_opy_:
          bstack11lllll1l_opy_[key] = sys.argv[idx + 1]
          bstack1l11l111_opy_ += bstack1ll1lll_opy_ (u"ࠨࠢ࠰࠱ࣹࠬ") + bstack1111ll11l1_opy_ + bstack1ll1lll_opy_ (u"ࣺࠩࠣࠫ") + shlex.quote(sys.argv[idx + 1])
          bstack111l1lll_opy_(bstack1l1lll1l11_opy_, key, sys.argv[idx + 1])
          bstack11111ll11l_opy_.extend([idx, idx + 1])
  for idx in sorted(set(bstack11111ll11l_opy_), reverse=True):
    if idx < len(sys.argv):
      del sys.argv[idx]
def bstack111l1l1lll_opy_(config):
  bstack1l1l1ll11_opy_ = config.keys()
  for bstack11ll11lll1_opy_, bstack11111l1lll_opy_ in bstack11lllllll1_opy_.items():
    if bstack11111l1lll_opy_ in bstack1l1l1ll11_opy_:
      config[bstack11ll11lll1_opy_] = config[bstack11111l1lll_opy_]
      del config[bstack11111l1lll_opy_]
  for bstack11ll11lll1_opy_, bstack11111l1lll_opy_ in bstack1l1l1lll1l_opy_.items():
    if isinstance(bstack11111l1lll_opy_, list):
      for bstack11l1l11l1_opy_ in bstack11111l1lll_opy_:
        if bstack11l1l11l1_opy_ in bstack1l1l1ll11_opy_:
          config[bstack11ll11lll1_opy_] = config[bstack11l1l11l1_opy_]
          del config[bstack11l1l11l1_opy_]
          break
    elif bstack11111l1lll_opy_ in bstack1l1l1ll11_opy_:
      config[bstack11ll11lll1_opy_] = config[bstack11111l1lll_opy_]
      del config[bstack11111l1lll_opy_]
  for bstack11l1l11l1_opy_ in list(config):
    for bstack1lll1l1l11_opy_ in bstack1l1l1l1l1_opy_:
      if bstack11l1l11l1_opy_.lower() == bstack1lll1l1l11_opy_.lower() and bstack11l1l11l1_opy_ != bstack1lll1l1l11_opy_:
        config[bstack1lll1l1l11_opy_] = config[bstack11l1l11l1_opy_]
        del config[bstack11l1l11l1_opy_]
  bstack1l11l1111_opy_ = [{}]
  if not config.get(bstack1ll1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣻ")):
    config[bstack1ll1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣼ")] = [{}]
  bstack1l11l1111_opy_ = config[bstack1ll1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨࣽ")]
  for platform in bstack1l11l1111_opy_:
    for bstack11l1l11l1_opy_ in list(platform):
      for bstack1lll1l1l11_opy_ in bstack1l1l1l1l1_opy_:
        if bstack11l1l11l1_opy_.lower() == bstack1lll1l1l11_opy_.lower() and bstack11l1l11l1_opy_ != bstack1lll1l1l11_opy_:
          platform[bstack1lll1l1l11_opy_] = platform[bstack11l1l11l1_opy_]
          del platform[bstack11l1l11l1_opy_]
  for bstack11ll11lll1_opy_, bstack11111l1lll_opy_ in bstack1l1l1lll1l_opy_.items():
    for platform in bstack1l11l1111_opy_:
      if isinstance(bstack11111l1lll_opy_, list):
        for bstack11l1l11l1_opy_ in bstack11111l1lll_opy_:
          if bstack11l1l11l1_opy_ in platform:
            platform[bstack11ll11lll1_opy_] = platform[bstack11l1l11l1_opy_]
            del platform[bstack11l1l11l1_opy_]
            break
      elif bstack11111l1lll_opy_ in platform:
        platform[bstack11ll11lll1_opy_] = platform[bstack11111l1lll_opy_]
        del platform[bstack11111l1lll_opy_]
  for bstack1l1111l1ll_opy_ in bstack111111lll_opy_:
    if bstack1l1111l1ll_opy_ in config:
      if not bstack111111lll_opy_[bstack1l1111l1ll_opy_] in config:
        config[bstack111111lll_opy_[bstack1l1111l1ll_opy_]] = {}
      config[bstack111111lll_opy_[bstack1l1111l1ll_opy_]].update(config[bstack1l1111l1ll_opy_])
      del config[bstack1l1111l1ll_opy_]
  for platform in bstack1l11l1111_opy_:
    for bstack1l1111l1ll_opy_ in bstack111111lll_opy_:
      if bstack1l1111l1ll_opy_ in list(platform):
        if not bstack111111lll_opy_[bstack1l1111l1ll_opy_] in platform:
          platform[bstack111111lll_opy_[bstack1l1111l1ll_opy_]] = {}
        platform[bstack111111lll_opy_[bstack1l1111l1ll_opy_]].update(platform[bstack1l1111l1ll_opy_])
        del platform[bstack1l1111l1ll_opy_]
  config = bstack1l11l111l1_opy_(config)
  return config
def bstack11llll11_opy_(config):
  global bstack1l1l11111_opy_
  bstack1llll11l1_opy_ = False
  if bstack1ll1lll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪࣾ") in config and str(config[bstack1ll1lll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫࣿ")]).lower() != bstack1ll1lll_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧऀ"):
    if bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ँ") not in config or str(config[bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧं")]).lower() == bstack1ll1lll_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪः"):
      config[bstack1ll1lll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫऄ")] = False
    else:
      bstack1lll11ll11_opy_ = bstack1llll1ll1l_opy_()
      if bstack1ll1lll_opy_ (u"࠭ࡩࡴࡖࡵ࡭ࡦࡲࡇࡳ࡫ࡧࠫअ") in bstack1lll11ll11_opy_:
        if not bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫआ") in config:
          config[bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬइ")] = {}
        config[bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ई")][bstack1ll1lll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬउ")] = bstack1ll1lll_opy_ (u"ࠫࡦࡺࡳ࠮ࡴࡨࡴࡪࡧࡴࡦࡴࠪऊ")
        bstack1llll11l1_opy_ = True
        bstack1l1l11111_opy_ = config[bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩऋ")].get(bstack1ll1lll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨऌ"))
  if bstack1111111l11_opy_(config) and bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫऍ") in config and str(config[bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬऎ")]).lower() != bstack1ll1lll_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨए") and not bstack1llll11l1_opy_:
    if not bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧऐ") in config:
      config[bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऑ")] = {}
    if not config[bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩऒ")].get(bstack1ll1lll_opy_ (u"࠭ࡳ࡬࡫ࡳࡆ࡮ࡴࡡࡳࡻࡌࡲ࡮ࡺࡩࡢ࡮࡬ࡷࡦࡺࡩࡰࡰࠪओ")) and not bstack1ll1lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऔ") in config[bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬक")]:
      current_time = datetime.datetime.now()
      bstack1lll11l1ll_opy_ = current_time.strftime(bstack1ll1lll_opy_ (u"ࠩࠨࡨࡤࠫࡢࡠࠧࡋࠩࡒ࠭ख"))
      hostname = socket.gethostname()
      bstack1111l1l1l1_opy_ = bstack1ll1lll_opy_ (u"ࠪࠫग").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1ll1lll_opy_ (u"ࠫࢀࢃ࡟ࡼࡿࡢࡿࢂ࠭घ").format(bstack1lll11l1ll_opy_, hostname, bstack1111l1l1l1_opy_)
      config[bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩङ")][bstack1ll1lll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨच")] = identifier
    bstack1l1l11111_opy_ = config[bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫछ")].get(bstack1ll1lll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪज"))
  return config
def bstack1l111l1l1l_opy_():
  bstack11lll1lll1_opy_ =  bstack1ll11l1l11_opy_()[bstack1ll1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠨझ")]
  return bstack11lll1lll1_opy_ if bstack11lll1lll1_opy_ else -1
def bstack1l1l111l11_opy_(bstack11lll1lll1_opy_):
  global CONFIG
  if not bstack1ll1lll_opy_ (u"ࠪࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬञ") in CONFIG[bstack1ll1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ट")]:
    return
  CONFIG[bstack1ll1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧठ")] = CONFIG[bstack1ll1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨड")].replace(
    bstack1ll1lll_opy_ (u"ࠧࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩढ"),
    str(bstack11lll1lll1_opy_)
  )
def bstack11ll1l11l_opy_():
  global CONFIG
  if not bstack1ll1lll_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧण") in CONFIG[bstack1ll1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫत")]:
    return
  current_time = datetime.datetime.now()
  bstack1lll11l1ll_opy_ = current_time.strftime(bstack1ll1lll_opy_ (u"ࠪࠩࡩ࠳ࠥࡣ࠯ࠨࡌ࠿ࠫࡍࠨथ"))
  CONFIG[bstack1ll1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭द")] = CONFIG[bstack1ll1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧध")].replace(
    bstack1ll1lll_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬन"),
    bstack1lll11l1ll_opy_
  )
def bstack1l1lll11l_opy_():
  global CONFIG
  if bstack1ll1lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऩ") in CONFIG and not bool(CONFIG[bstack1ll1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪप")]):
    del CONFIG[bstack1ll1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫफ")]
    return
  if not bstack1ll1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬब") in CONFIG:
    CONFIG[bstack1ll1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭भ")] = bstack1ll1lll_opy_ (u"ࠬࠩࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨम")
  if bstack1ll1lll_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬय") in CONFIG[bstack1ll1lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩर")]:
    bstack11ll1l11l_opy_()
    os.environ[bstack1ll1lll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬऱ")] = CONFIG[bstack1ll1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫल")]
  if not bstack1ll1lll_opy_ (u"ࠪࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬळ") in CONFIG[bstack1ll1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ऴ")]:
    return
  bstack11lll1lll1_opy_ = bstack1ll1lll_opy_ (u"ࠬ࠭व")
  bstack11ll11ll1l_opy_ = bstack1l111l1l1l_opy_()
  if bstack11ll11ll1l_opy_ != -1:
    bstack11lll1lll1_opy_ = bstack1ll1lll_opy_ (u"࠭ࡃࡊࠢࠪश") + str(bstack11ll11ll1l_opy_)
  if bstack11lll1lll1_opy_ == bstack1ll1lll_opy_ (u"ࠧࠨष"):
    bstack1l1111l1_opy_ = bstack111l1llll_opy_(CONFIG[bstack1ll1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫस")])
    if bstack1l1111l1_opy_ != -1:
      bstack11lll1lll1_opy_ = str(bstack1l1111l1_opy_)
  if bstack11lll1lll1_opy_:
    bstack1l1l111l11_opy_(bstack11lll1lll1_opy_)
    os.environ[bstack1ll1lll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ह")] = CONFIG[bstack1ll1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬऺ")]
def bstack11111111_opy_(bstack1ll11ll111_opy_, bstack1llll1ll_opy_, path):
  json_data = {
    bstack1ll1lll_opy_ (u"ࠫ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨऻ"): bstack1llll1ll_opy_
  }
  if os.path.exists(path):
    bstack1111l11ll1_opy_ = json.load(open(path, bstack1ll1lll_opy_ (u"ࠬࡸࡢࠨ़")))
  else:
    bstack1111l11ll1_opy_ = {}
  bstack1111l11ll1_opy_[bstack1ll11ll111_opy_] = json_data
  with open(path, bstack1ll1lll_opy_ (u"ࠨࡷࠬࠤऽ")) as outfile:
    json.dump(bstack1111l11ll1_opy_, outfile)
def bstack111l1llll_opy_(bstack1ll11ll111_opy_):
  bstack1ll11ll111_opy_ = str(bstack1ll11ll111_opy_)
  bstack1ll11ll1ll_opy_ = os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"ࠧࡿࠩा")), bstack1ll1lll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨि"))
  try:
    if not os.path.exists(bstack1ll11ll1ll_opy_):
      os.makedirs(bstack1ll11ll1ll_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"ࠩࢁࠫी")), bstack1ll1lll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪु"), bstack1ll1lll_opy_ (u"ࠫ࠳ࡨࡵࡪ࡮ࡧ࠱ࡳࡧ࡭ࡦ࠯ࡦࡥࡨ࡮ࡥ࠯࡬ࡶࡳࡳ࠭ू"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1ll1lll_opy_ (u"ࠬࡽࠧृ")):
        pass
      with open(file_path, bstack1ll1lll_opy_ (u"ࠨࡷࠬࠤॄ")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1ll1lll_opy_ (u"ࠧࡳࠩॅ")) as bstack1llll1lll_opy_:
      bstack1111l1111_opy_ = json.load(bstack1llll1lll_opy_)
    if bstack1ll11ll111_opy_ in bstack1111l1111_opy_:
      bstack1ll111111l_opy_ = bstack1111l1111_opy_[bstack1ll11ll111_opy_][bstack1ll1lll_opy_ (u"ࠨ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬॆ")]
      bstack1llll1l1l1_opy_ = int(bstack1ll111111l_opy_) + 1
      bstack11111111_opy_(bstack1ll11ll111_opy_, bstack1llll1l1l1_opy_, file_path)
      return bstack1llll1l1l1_opy_
    else:
      bstack11111111_opy_(bstack1ll11ll111_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warning(bstack1l111111_opy_.format(str(e)))
    return -1
def bstack11l1111l_opy_(config):
  if not config[bstack1ll1lll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫे")] or not config[bstack1ll1lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ै")]:
    return True
  else:
    return False
def bstack11l111ll1_opy_(config, index=0):
  global bstack111l11l11_opy_
  bstack1lll1111l1_opy_ = {}
  caps = bstack11ll111l1l_opy_ + bstack1l1ll111l_opy_
  if config.get(bstack1ll1lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨॉ"), False):
    bstack1lll1111l1_opy_[bstack1ll1lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩॊ")] = True
    bstack1lll1111l1_opy_[bstack1ll1lll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪो")] = config.get(bstack1ll1lll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࡓࡵࡺࡩࡰࡰࡶࠫौ"), {})
  if bstack111l11l11_opy_:
    caps += bstack1llll11ll1_opy_
  for key in config:
    if key in caps + [bstack1ll1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶ्ࠫ")]:
      continue
    bstack1lll1111l1_opy_[key] = config[key]
  if bstack1ll1lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॎ") in config:
    for bstack1l111ll11l_opy_ in config[bstack1ll1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॏ")][index]:
      if bstack1l111ll11l_opy_ in caps:
        continue
      bstack1lll1111l1_opy_[bstack1l111ll11l_opy_] = config[bstack1ll1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॐ")][index][bstack1l111ll11l_opy_]
  bstack1lll1111l1_opy_[bstack1ll1lll_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧ॑")] = socket.gethostname()
  if bstack1ll1lll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴ॒ࠧ") in bstack1lll1111l1_opy_:
    del (bstack1lll1111l1_opy_[bstack1ll1lll_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨ॓")])
  return bstack1lll1111l1_opy_
def bstack1l1ll111ll_opy_(config):
  global bstack111l11l11_opy_
  bstack1l1l1lll_opy_ = {}
  caps = bstack1l1ll111l_opy_
  if bstack111l11l11_opy_:
    caps += bstack1llll11ll1_opy_
  for key in caps:
    if key in config:
      bstack1l1l1lll_opy_[key] = config[key]
  return bstack1l1l1lll_opy_
def bstack11llll1lll_opy_(bstack1lll1111l1_opy_, bstack1l1l1lll_opy_):
  bstack1ll11l1lll_opy_ = {}
  for key in bstack1lll1111l1_opy_.keys():
    if key in bstack11lllllll1_opy_:
      bstack1ll11l1lll_opy_[bstack11lllllll1_opy_[key]] = bstack1lll1111l1_opy_[key]
    else:
      bstack1ll11l1lll_opy_[key] = bstack1lll1111l1_opy_[key]
  for key in bstack1l1l1lll_opy_:
    if key in bstack11lllllll1_opy_:
      bstack1ll11l1lll_opy_[bstack11lllllll1_opy_[key]] = bstack1l1l1lll_opy_[key]
    else:
      bstack1ll11l1lll_opy_[key] = bstack1l1l1lll_opy_[key]
  return bstack1ll11l1lll_opy_
def get_caps(config, index=0):
  global bstack111l11l11_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack1111111l1_opy_ = bstack111l1lll11_opy_(bstack11lll11ll1_opy_, config, logger)
  bstack1l1l1lll_opy_ = bstack1l1ll111ll_opy_(config)
  bstack1ll1lll11l_opy_ = bstack1l1ll111l_opy_
  bstack1ll1lll11l_opy_ += bstack11ll11l11l_opy_
  bstack1l1l1lll_opy_ = update(bstack1l1l1lll_opy_, bstack1111111l1_opy_)
  if bstack111l11l11_opy_:
    bstack1ll1lll11l_opy_ += bstack1llll11ll1_opy_
  if bstack1ll1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ॔") in config:
    if bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧॕ") in config[bstack1ll1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॖ")][index]:
      caps[bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩॗ")] = config[bstack1ll1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨक़")][index][bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫख़")]
    if bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨग़") in config[bstack1ll1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫज़")][index]:
      caps[bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪड़")] = str(config[bstack1ll1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ढ़")][index][bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬफ़")])
    bstack111l1l11l_opy_ = bstack111l1lll11_opy_(bstack11lll11ll1_opy_, config[bstack1ll1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨय़")][index], logger)
    bstack1ll1lll11l_opy_ += list(bstack111l1l11l_opy_.keys())
    for bstack11l111ll1l_opy_ in bstack1ll1lll11l_opy_:
      if bstack11l111ll1l_opy_ in config[bstack1ll1lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩॠ")][index]:
        if bstack11l111ll1l_opy_ == bstack1ll1lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩॡ"):
          try:
            bstack111l1l11l_opy_[bstack11l111ll1l_opy_] = str(config[bstack1ll1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫॢ")][index][bstack11l111ll1l_opy_] * 1.0)
          except:
            bstack111l1l11l_opy_[bstack11l111ll1l_opy_] = str(config[bstack1ll1lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॣ")][index][bstack11l111ll1l_opy_])
        else:
          bstack111l1l11l_opy_[bstack11l111ll1l_opy_] = config[bstack1ll1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭।")][index][bstack11l111ll1l_opy_]
        del (config[bstack1ll1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ॥")][index][bstack11l111ll1l_opy_])
    bstack1l1l1lll_opy_ = update(bstack1l1l1lll_opy_, bstack111l1l11l_opy_)
  bstack1lll1111l1_opy_ = bstack11l111ll1_opy_(config, index)
  for bstack11l1l11l1_opy_ in bstack1l1ll111l_opy_ + list(bstack1111111l1_opy_.keys()):
    if bstack11l1l11l1_opy_ in bstack1lll1111l1_opy_:
      bstack1l1l1lll_opy_[bstack11l1l11l1_opy_] = bstack1lll1111l1_opy_[bstack11l1l11l1_opy_]
      del (bstack1lll1111l1_opy_[bstack11l1l11l1_opy_])
  if bstack1ll1ll11ll_opy_(config):
    bstack1lll1111l1_opy_[bstack1ll1lll_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ०")] = True
    caps.update(bstack1l1l1lll_opy_)
    caps[bstack1ll1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ१")] = bstack1lll1111l1_opy_
  else:
    bstack1lll1111l1_opy_[bstack1ll1lll_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧ२")] = False
    caps.update(bstack11llll1lll_opy_(bstack1lll1111l1_opy_, bstack1l1l1lll_opy_))
    if bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭३") in caps:
      caps[bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪ४")] = caps[bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ५")]
      del (caps[bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ६")])
    if bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭७") in caps:
      caps[bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ८")] = caps[bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ९")]
      del (caps[bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ॰")])
  return caps
def bstack11llll1l1l_opy_():
  global bstack1l11ll1ll_opy_
  global CONFIG
  if bstack1l11ll1ll_opy_ != bstack1ll1lll_opy_ (u"ࠩࠪॱ") and (bstack1l11ll1ll_opy_.startswith(bstack1ll1lll_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫॲ")) or bstack1l11ll1ll_opy_.startswith(bstack1ll1lll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࠭ॳ"))):
    return bstack1l11ll1ll_opy_
  if bstack1l1l11l1l1_opy_() <= version.parse(bstack1ll1lll_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬॴ")):
    if bstack1l11ll1ll_opy_ != bstack1ll1lll_opy_ (u"࠭ࠧॵ"):
      return bstack1ll1lll_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣॶ") + bstack1l11ll1ll_opy_ + bstack1ll1lll_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧॷ")
    return bstack1ll1l11l1_opy_
  if bstack1l11ll1ll_opy_ != bstack1ll1lll_opy_ (u"ࠩࠪॸ"):
    return bstack1ll1lll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧॹ") + bstack1l11ll1ll_opy_ + bstack1ll1lll_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧॺ")
  return HTTPS_HUB
def bstack11l1lllll_opy_(options):
  return hasattr(options, bstack1ll1lll_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭ॻ"))
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
def bstack1lll1l11l_opy_(options, bstack11l11llll1_opy_):
  for bstack1l111l11ll_opy_ in bstack11l11llll1_opy_:
    if bstack1l111l11ll_opy_ in [bstack1ll1lll_opy_ (u"࠭ࡡࡳࡩࡶࠫॼ"), bstack1ll1lll_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫॽ")]:
      continue
    if bstack1l111l11ll_opy_ in options._experimental_options:
      options._experimental_options[bstack1l111l11ll_opy_] = update(options._experimental_options[bstack1l111l11ll_opy_],
                                                         bstack11l11llll1_opy_[bstack1l111l11ll_opy_])
    else:
      options.add_experimental_option(bstack1l111l11ll_opy_, bstack11l11llll1_opy_[bstack1l111l11ll_opy_])
  if bstack1ll1lll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ॾ") in bstack11l11llll1_opy_:
    for arg in bstack11l11llll1_opy_[bstack1ll1lll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॿ")]:
      options.add_argument(arg)
    del (bstack11l11llll1_opy_[bstack1ll1lll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨঀ")])
  if bstack1ll1lll_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨঁ") in bstack11l11llll1_opy_:
    for ext in bstack11l11llll1_opy_[bstack1ll1lll_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩং")]:
      try:
        options.add_extension(ext)
      except OSError:
        options.add_encoded_extension(ext)
    del (bstack11l11llll1_opy_[bstack1ll1lll_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪঃ")])
def bstack11llll1l1_opy_(options):
  global CONFIG
  global bstack111l1ll1l_opy_
  try:
    if not bstack111l1ll1l_opy_ or not options:
      return options
    from bstack_utils.bstack11l1l11l_opy_ import bstack11l1ll111_opy_
    bstack1ll1l11111_opy_ = bstack11l1ll111_opy_(options, bstack11111ll1ll_opy_=bstack1ll1lll_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢ঄"))
    if bstack1ll1l11111_opy_ > 0:
      logger.debug(bstack1ll1lll_opy_ (u"ࠣࡎࡲࡥࡩࠦࡴࡦࡵࡷ࡭ࡳ࡭࠺ࠡࡃࡧࡨࡪࡪࠠࡼࡿࠣࡨࡪ࡬ࡡࡶ࡮ࡷࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠠࡧࡱࡵࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠦঅ").format(bstack1ll1l11111_opy_))
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡯࡮࡫ࡧࡦࡸࠥࡲ࡯ࡢࡦࠣࡸࡪࡹࡴࡪࡰࡪࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡴࡶࡴࡪࡱࡱࡷ࠿ࠦࡻࡾࠤআ").format(e))
  return options
def bstack11ll1l11l1_opy_(options, bstack111l1ll1_opy_):
  if bstack1ll1lll_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩই") in bstack111l1ll1_opy_:
    for bstack111l1l111l_opy_ in bstack111l1ll1_opy_[bstack1ll1lll_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪঈ")]:
      if bstack111l1l111l_opy_ in options._preferences:
        options._preferences[bstack111l1l111l_opy_] = update(options._preferences[bstack111l1l111l_opy_], bstack111l1ll1_opy_[bstack1ll1lll_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫউ")][bstack111l1l111l_opy_])
      else:
        options.set_preference(bstack111l1l111l_opy_, bstack111l1ll1_opy_[bstack1ll1lll_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬঊ")][bstack111l1l111l_opy_])
  if bstack1ll1lll_opy_ (u"ࠧࡢࡴࡪࡷࠬঋ") in bstack111l1ll1_opy_:
    for arg in bstack111l1ll1_opy_[bstack1ll1lll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ঌ")]:
      options.add_argument(arg)
def bstack11l1l11l11_opy_(options, bstack1ll1l111_opy_):
  if bstack1ll1lll_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࠪ঍") in bstack1ll1l111_opy_:
    options.use_webview(bool(bstack1ll1l111_opy_[bstack1ll1lll_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࠫ঎")]))
  bstack1lll1l11l_opy_(options, bstack1ll1l111_opy_)
def bstack11ll111l1_opy_(options, bstack111111l1_opy_):
  for bstack1l11ll111l_opy_ in bstack111111l1_opy_:
    if bstack1l11ll111l_opy_ in [bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨএ"), bstack1ll1lll_opy_ (u"ࠬࡧࡲࡨࡵࠪঐ")]:
      continue
    options.set_capability(bstack1l11ll111l_opy_, bstack111111l1_opy_[bstack1l11ll111l_opy_])
  if bstack1ll1lll_opy_ (u"࠭ࡡࡳࡩࡶࠫ঑") in bstack111111l1_opy_:
    for arg in bstack111111l1_opy_[bstack1ll1lll_opy_ (u"ࠧࡢࡴࡪࡷࠬ঒")]:
      options.add_argument(arg)
  if bstack1ll1lll_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬও") in bstack111111l1_opy_:
    options.bstack1111l1l1l_opy_(bool(bstack111111l1_opy_[bstack1ll1lll_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭ঔ")]))
def bstack1ll11lll1l_opy_(options, bstack1llll1111_opy_):
  for bstack1llllll111_opy_ in bstack1llll1111_opy_:
    if bstack1llllll111_opy_ in [bstack1ll1lll_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧক"), bstack1ll1lll_opy_ (u"ࠫࡦࡸࡧࡴࠩখ")]:
      continue
    options._options[bstack1llllll111_opy_] = bstack1llll1111_opy_[bstack1llllll111_opy_]
  if bstack1ll1lll_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩগ") in bstack1llll1111_opy_:
    for bstack111ll11l1_opy_ in bstack1llll1111_opy_[bstack1ll1lll_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪঘ")]:
      options.bstack1lll1l11l1_opy_(
        bstack111ll11l1_opy_, bstack1llll1111_opy_[bstack1ll1lll_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫঙ")][bstack111ll11l1_opy_])
  if bstack1ll1lll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭চ") in bstack1llll1111_opy_:
    for arg in bstack1llll1111_opy_[bstack1ll1lll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧছ")]:
      options.add_argument(arg)
def bstack11l1l11111_opy_(options, caps):
  if not hasattr(options, bstack1ll1lll_opy_ (u"ࠪࡏࡊ࡟ࠧজ")):
    return
  if options.KEY == bstack1ll1lll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩঝ"):
    options = a11y.bstack1l1lllll1_opy_(bstack11lll1l111_opy_=options, config=CONFIG)
  if options.KEY == bstack1ll1lll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪঞ") and options.KEY in caps:
    bstack1lll1l11l_opy_(options, caps[bstack1ll1lll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫট")])
  elif options.KEY == bstack1ll1lll_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬঠ") and options.KEY in caps:
    bstack11ll1l11l1_opy_(options, caps[bstack1ll1lll_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ড")])
  elif options.KEY == bstack1ll1lll_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪঢ") and options.KEY in caps:
    bstack11ll111l1_opy_(options, caps[bstack1ll1lll_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫণ")])
  elif options.KEY == bstack1ll1lll_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬত") and options.KEY in caps:
    bstack11l1l11l11_opy_(options, caps[bstack1ll1lll_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭থ")])
  elif options.KEY == bstack1ll1lll_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬদ") and options.KEY in caps:
    bstack1ll11lll1l_opy_(options, caps[bstack1ll1lll_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ধ")])
def bstack1l1l1llll_opy_(caps):
  global bstack111l11l11_opy_
  if isinstance(os.environ.get(bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩন")), str):
    bstack111l11l11_opy_ = eval(os.getenv(bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ঩")))
  if bstack111l11l11_opy_:
    if bstack111lll1lll_opy_() < version.parse(bstack1ll1lll_opy_ (u"ࠪ࠶࠳࠹࠮࠱ࠩপ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1ll1lll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫফ")
    if bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪব") in caps:
      browser = caps[bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫভ")]
    elif bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨম") in caps:
      browser = caps[bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩয")]
    browser = str(browser).lower()
    if browser == bstack1ll1lll_opy_ (u"ࠩ࡬ࡴ࡭ࡵ࡮ࡦࠩর") or browser == bstack1ll1lll_opy_ (u"ࠪ࡭ࡵࡧࡤࠨ঱"):
      browser = bstack1ll1lll_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫল")
    if browser == bstack1ll1lll_opy_ (u"ࠬࡹࡡ࡮ࡵࡸࡲ࡬࠭঳"):
      browser = bstack1ll1lll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭঴")
    if browser not in [bstack1ll1lll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ঵"), bstack1ll1lll_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭শ"), bstack1ll1lll_opy_ (u"ࠩ࡬ࡩࠬষ"), bstack1ll1lll_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪস"), bstack1ll1lll_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬহ")]:
      return None
    try:
      package = bstack1ll1lll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡿࢂ࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧ঺").format(browser)
      name = bstack1ll1lll_opy_ (u"࠭ࡏࡱࡶ࡬ࡳࡳࡹࠧ঻")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack11l1lllll_opy_(options):
        return None
      for bstack11l1l11l1_opy_ in caps.keys():
        options.set_capability(bstack11l1l11l1_opy_, caps[bstack11l1l11l1_opy_])
      bstack11l1l11111_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1ll111l1ll_opy_(options, bstack11l1l11lll_opy_):
  if not bstack11l1lllll_opy_(options):
    return
  for bstack11l1l11l1_opy_ in bstack11l1l11lll_opy_.keys():
    if bstack11l1l11l1_opy_ in bstack11ll11l11l_opy_:
      continue
    if bstack11l1l11l1_opy_ in options._caps and type(options._caps[bstack11l1l11l1_opy_]) in [dict, list]:
      options._caps[bstack11l1l11l1_opy_] = update(options._caps[bstack11l1l11l1_opy_], bstack11l1l11lll_opy_[bstack11l1l11l1_opy_])
    else:
      options.set_capability(bstack11l1l11l1_opy_, bstack11l1l11lll_opy_[bstack11l1l11l1_opy_])
  bstack11l1l11111_opy_(options, bstack11l1l11lll_opy_)
  if bstack1ll1lll_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ়࠭") in options._caps:
    if options._caps[bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ঽ")] and options._caps[bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧা")].lower() != bstack1ll1lll_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫি"):
      del options._caps[bstack1ll1lll_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪী")]
def bstack1ll11ll11l_opy_(proxy_config):
  if bstack1ll1lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩু") in proxy_config:
    proxy_config[bstack1ll1lll_opy_ (u"࠭ࡳࡴ࡮ࡓࡶࡴࡾࡹࠨূ")] = proxy_config[bstack1ll1lll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫৃ")]
    del (proxy_config[bstack1ll1lll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬৄ")])
  if bstack1ll1lll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬ৅") in proxy_config and proxy_config[bstack1ll1lll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭৆")].lower() != bstack1ll1lll_opy_ (u"ࠫࡩ࡯ࡲࡦࡥࡷࠫে"):
    proxy_config[bstack1ll1lll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨৈ")] = bstack1ll1lll_opy_ (u"࠭࡭ࡢࡰࡸࡥࡱ࠭৉")
  if bstack1ll1lll_opy_ (u"ࠧࡱࡴࡲࡼࡾࡇࡵࡵࡱࡦࡳࡳ࡬ࡩࡨࡗࡵࡰࠬ৊") in proxy_config:
    proxy_config[bstack1ll1lll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫো")] = bstack1ll1lll_opy_ (u"ࠩࡳࡥࡨ࠭ৌ")
  return proxy_config
def bstack1l11111111_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1ll1lll_opy_ (u"ࠪࡴࡷࡵࡸࡺ্ࠩ") in config:
    return proxy
  config[bstack1ll1lll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪৎ")] = bstack1ll11ll11l_opy_(config[bstack1ll1lll_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ৏")])
  if proxy == None:
    proxy = Proxy(config[bstack1ll1lll_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ৐")])
  return proxy
def bstack1l1111111l_opy_(self):
  global CONFIG
  global bstack111l11lll1_opy_
  try:
    proxy = bstack111l111ll1_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1ll1lll_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ৑")):
        proxies = bstack11ll111ll1_opy_(proxy, bstack11llll1l1l_opy_())
        if len(proxies) > 0:
          protocol, bstack1l11lll111_opy_ = proxies.popitem()
          if bstack1ll1lll_opy_ (u"ࠣ࠼࠲࠳ࠧ৒") in bstack1l11lll111_opy_:
            return bstack1l11lll111_opy_
          else:
            return bstack1ll1lll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ৓") + bstack1l11lll111_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1ll1lll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡰࡳࡱࡻࡽࠥࡻࡲ࡭ࠢ࠽ࠤࢀࢃࠢ৔").format(str(e)))
  return bstack111l11lll1_opy_(self)
def bstack111l1lll1l_opy_():
  global CONFIG
  return bstack111111l11_opy_(CONFIG) and bstack1lllllll1l_opy_() and bstack1l1l11l1l1_opy_() >= version.parse(bstack1lll1ll11l_opy_)
def bstack1111ll1l11_opy_():
  global CONFIG
  return (bstack1ll1lll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ৕") in CONFIG or bstack1ll1lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ৖") in CONFIG) and bstack11l11111l1_opy_()
def bstack11ll1111_opy_(config):
  bstack111l11111_opy_ = {}
  if bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪৗ") in config:
    bstack111l11111_opy_ = config[bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ৘")]
  if bstack1ll1lll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ৙") in config:
    bstack111l11111_opy_ = config[bstack1ll1lll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ৚")]
  proxy = bstack111l111ll1_opy_(config)
  if proxy:
    if proxy.endswith(bstack1ll1lll_opy_ (u"ࠪ࠲ࡵࡧࡣࠨ৛")) and os.path.isfile(proxy):
      bstack111l11111_opy_[bstack1ll1lll_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧড়")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1ll1lll_opy_ (u"ࠬ࠴ࡰࡢࡥࠪঢ়")):
        proxies = bstack11l11ll1ll_opy_(config, bstack11llll1l1l_opy_())
        if len(proxies) > 0:
          protocol, bstack1l11lll111_opy_ = proxies.popitem()
          if bstack1ll1lll_opy_ (u"ࠨ࠺࠰࠱ࠥ৞") in bstack1l11lll111_opy_:
            parsed_url = urlparse(bstack1l11lll111_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1ll1lll_opy_ (u"ࠢ࠻࠱࠲ࠦয়") + bstack1l11lll111_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack111l11111_opy_[bstack1ll1lll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡈࡰࡵࡷࠫৠ")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack111l11111_opy_[bstack1ll1lll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬৡ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack111l11111_opy_[bstack1ll1lll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭ৢ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack111l11111_opy_[bstack1ll1lll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧৣ")] = str(parsed_url.password)
  return bstack111l11111_opy_
def bstack1111llll1l_opy_(config):
  if bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪ৤") in config:
    return config[bstack1ll1lll_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫ৥")]
  return {}
def update_caps_for_local(caps):
  global bstack1l1l11111_opy_
  if bstack1ll1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ০") in caps:
    caps[bstack1ll1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ১")][bstack1ll1lll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨ২")] = True
    if bstack1l1l11111_opy_:
      caps[bstack1ll1lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ৩")][bstack1ll1lll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭৪")] = bstack1l1l11111_opy_
  else:
    caps[bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪ৫")] = True
    if bstack1l1l11111_opy_:
      caps[bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ৬")] = bstack1l1l11111_opy_
@measure(event_name=EVENTS.bstack1111lll111_opy_, stage=STAGE.bstack1111l1ll1_opy_, bstack1l1l1l11_opy_=SESSION_NAME)
def bstack111111l1ll_opy_():
  global CONFIG
  if not bstack1111111l11_opy_(CONFIG) or cli.is_enabled(CONFIG):
    return
  if bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ৭") in CONFIG and bstack1l11l11111_opy_(CONFIG[bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ৮")]):
    if (
      bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭৯") in CONFIG
      and bstack1l11l11111_opy_(CONFIG[bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧৰ")].get(bstack1ll1lll_opy_ (u"ࠫࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠨৱ")))
    ):
      logger.debug(bstack1ll1lll_opy_ (u"ࠧࡒ࡯ࡤࡣ࡯ࠤࡧ࡯࡮ࡢࡴࡼࠤࡳࡵࡴࠡࡵࡷࡥࡷࡺࡥࡥࠢࡤࡷࠥࡹ࡫ࡪࡲࡅ࡭ࡳࡧࡲࡺࡋࡱ࡭ࡹ࡯ࡡ࡭࡫ࡶࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠨ৲"))
      return
    bstack111l11111_opy_ = bstack11ll1111_opy_(CONFIG)
    bstack111111ll1l_opy_(CONFIG[bstack1ll1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ৳")], bstack111l11111_opy_)
def bstack111111ll1l_opy_(key, bstack111l11111_opy_):
  global bstack1l111llll_opy_
  logger.info(bstack1lll1lll11_opy_)
  try:
    bstack1l111llll_opy_ = Local()
    bstack1l111ll11_opy_ = {bstack1ll1lll_opy_ (u"ࠧ࡬ࡧࡼࠫ৴"): key}
    bstack1l111ll11_opy_.update(bstack111l11111_opy_)
    logger.debug(bstack1lllll11_opy_.format(str(bstack1l111ll11_opy_)).replace(key, bstack1ll1lll_opy_ (u"ࠨ࡝ࡕࡉࡉࡇࡃࡕࡇࡇࡡࠬ৵")))
    bstack1l111llll_opy_.start(**bstack1l111ll11_opy_)
    if bstack1l111llll_opy_.isRunning():
      logger.info(bstack111l1l1l11_opy_)
  except Exception as e:
    bstack1lll1111l_opy_(bstack1111ll11l_opy_.format(str(e)))
def bstack11ll1lll1l_opy_():
  global bstack1l111llll_opy_
  if bstack1l111llll_opy_.isRunning():
    logger.info(bstack1ll1ll11l1_opy_)
    bstack1l111llll_opy_.stop()
  bstack1l111llll_opy_ = None
def bstack1ll1ll1lll_opy_(bstack11llllllll_opy_=[]):
  global CONFIG
  bstack1l1111l1l1_opy_ = []
  bstack1l1l1lll11_opy_ = [bstack1ll1lll_opy_ (u"ࠩࡲࡷࠬ৶"), bstack1ll1lll_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭৷"), bstack1ll1lll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨ৸"), bstack1ll1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ৹"), bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ৺"), bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ৻")]
  try:
    for err in bstack11llllllll_opy_:
      bstack1l1ll1l1l1_opy_ = {}
      for k in bstack1l1l1lll11_opy_:
        val = CONFIG[bstack1ll1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫৼ")][int(err[bstack1ll1lll_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ৽")])].get(k)
        if val:
          bstack1l1ll1l1l1_opy_[k] = val
      if(err[bstack1ll1lll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ৾")] != bstack1ll1lll_opy_ (u"ࠫࠬ৿")):
        bstack1l1ll1l1l1_opy_[bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶࡶࠫ਀")] = {
          err[bstack1ll1lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫਁ")]: err[bstack1ll1lll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ਂ")]
        }
        bstack1l1111l1l1_opy_.append(bstack1l1ll1l1l1_opy_)
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪࡴࡸ࡭ࡢࡶࡷ࡭ࡳ࡭ࠠࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴ࠻ࠢࠪਃ") + str(e))
  finally:
    return bstack1l1111l1l1_opy_
def bstack1l1l11ll1l_opy_(file_name):
  bstack1l1l111l1_opy_ = []
  try:
    bstack1l11ll1l_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1l11ll1l_opy_):
      with open(bstack1l11ll1l_opy_) as f:
        bstack1llll11111_opy_ = json.load(f)
        bstack1l1l111l1_opy_ = bstack1llll11111_opy_
      os.remove(bstack1l11ll1l_opy_)
    return bstack1l1l111l1_opy_
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡫࡯࡮ࡥ࡫ࡱ࡫ࠥ࡫ࡲࡳࡱࡵࠤࡱ࡯ࡳࡵ࠼ࠣࠫ਄") + str(e))
    return bstack1l1l111l1_opy_
def bstack111ll111l_opy_():
  try:
      import time
      from bstack_utils.constants import bstack11ll1ll1l1_opy_, EVENTS
      from bstack_utils.helper import bstack111lll1l11_opy_, get_host_info, global_config
      from datetime import datetime
      from filelock import FileLock
      from bstack_utils.bstack1l111ll111_opy_ import bstack1l1l11ll1_opy_
      bstack1l1l11ll1_opy_.bstack11lllll11l_opy_()
      bstack1l1ll1ll1_opy_ = os.path.join(os.getcwd(), bstack1ll1lll_opy_ (u"ࠪࡰࡴ࡭ࠧਅ"), bstack1ll1lll_opy_ (u"ࠫࡰ࡫ࡹ࠮࡯ࡨࡸࡷ࡯ࡣࡴ࠰࡭ࡷࡴࡴࠧਆ"))
      data = None
      lock = FileLock(bstack1l1ll1ll1_opy_+bstack1ll1lll_opy_ (u"ࠧ࠴࡬ࡰࡥ࡮ࠦਇ"), timeout=2)
      try:
          with lock:
              with open(bstack1l1ll1ll1_opy_, bstack1ll1lll_opy_ (u"ࠨࡲࠣਈ"), encoding=bstack1ll1lll_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨਉ")) as file:
                  data = json.load(file)
      except Exception as e:
          logger.debug(bstack1ll1lll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡷ࡫ࡡࡥࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹࠠࡧ࡫࡯ࡩ࠿ࠦࡻࡾࠤਊ").format(e))
          return
      if not data:
          return
      def bstack1lll11l111_opy_():
          try:
              config = {
                  bstack1ll1lll_opy_ (u"ࠤ࡫ࡩࡦࡪࡥࡳࡵࠥ਋"): {
                      bstack1ll1lll_opy_ (u"ࠥࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠤ਌"): bstack1ll1lll_opy_ (u"ࠦࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠢ਍"),
                  }
              }
              bstack11lll11lll_opy_ = datetime.utcnow()
              current_time = bstack11lll11lll_opy_.strftime(bstack1ll1lll_opy_ (u"࡙ࠧࠫ࠮ࠧࡰ࠱ࠪࡪࡔࠦࡊ࠽ࠩࡒࡀࠥࡔ࠰ࠨࡪ࡛ࠥࡔࡄࠤ਎"))
              test_id = os.environ.get(bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫਏ")) if os.environ.get(bstack1ll1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬਐ")) else global_config.get_property(bstack1ll1lll_opy_ (u"ࠣࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠥ਑"))
              payload = {
                  bstack1ll1lll_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪࠨ਒"): bstack1ll1lll_opy_ (u"ࠥࡷࡩࡱ࡟ࡦࡸࡨࡲࡹࡹࠢਓ"),
                  bstack1ll1lll_opy_ (u"ࠦࡩࡧࡴࡢࠤਔ"): {
                      bstack1ll1lll_opy_ (u"ࠧࡺࡥࡴࡶ࡫ࡹࡧࡥࡵࡶ࡫ࡧࠦਕ"): test_id,
                      bstack1ll1lll_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡪ࡟ࡥࡣࡼࠦਖ"): current_time,
                      bstack1ll1lll_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥ࡮ࡢ࡯ࡨࠦਗ"): bstack1ll1lll_opy_ (u"ࠣࡕࡇࡏࡋ࡫ࡡࡵࡷࡵࡩࡕ࡫ࡲࡧࡱࡵࡱࡦࡴࡣࡦࠤਘ"),
                      bstack1ll1lll_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠ࡬ࡶࡳࡳࠨਙ"): {
                          bstack1ll1lll_opy_ (u"ࠥࡱࡪࡧࡳࡶࡴࡨࡷࠧਚ"): data,
                          bstack1ll1lll_opy_ (u"ࠦࡸࡪ࡫ࡓࡷࡱࡍࡩࠨਛ"): global_config.get_property(bstack1ll1lll_opy_ (u"ࠧࡹࡤ࡬ࡔࡸࡲࡎࡪࠢਜ"))
                      },
                      bstack1ll1lll_opy_ (u"ࠨࡵࡴࡧࡵࡣࡩࡧࡴࡢࠤਝ"): global_config.get_property(bstack1ll1lll_opy_ (u"ࠢࡶࡵࡨࡶࡓࡧ࡭ࡦࠤਞ")),
                      bstack1ll1lll_opy_ (u"ࠣࡪࡲࡷࡹࡥࡩ࡯ࡨࡲࠦਟ"): get_host_info()
                  }
              }
              bstack11l1llll_opy_ = bstack11l11l11ll_opy_(cli.config, [bstack1ll1lll_opy_ (u"ࠤࡤࡴ࡮ࡹࠢਠ"), bstack1ll1lll_opy_ (u"ࠥࡩࡩࡹࡉ࡯ࡵࡷࡶࡺࡳࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠣਡ"), bstack1ll1lll_opy_ (u"ࠦࡦࡶࡩࠣਢ")], bstack11ll1ll1l1_opy_)
              response = bstack111lll1l11_opy_(bstack1ll1lll_opy_ (u"ࠧࡖࡏࡔࡖࠥਣ"), bstack11l1llll_opy_, payload, config)
              if response.status_code >= 200 and response.status_code < 300:
                  logger.info(bstack1ll1lll_opy_ (u"ࠨࡋࡦࡻࠣࡱࡪࡺࡲࡪࡥࡶࠤࡸ࡫࡮ࡵࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡶࡲࠤࢀࢃࠢਤ").format(bstack11ll1ll1l1_opy_))
              else:
                  logger.debug(bstack1ll1lll_opy_ (u"ࠢࡌࡧࡼࠤࡲ࡫ࡴࡳ࡫ࡦࡷࠥࡸࡥࡲࡷࡨࡷࡹࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫ࠤࡸࡺࡡࡵࡷࡶࠤࢀࢃࠢਥ").format(response.status_code))
          except Exception as e:
              logger.debug(bstack1ll1lll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫࡮ࡥࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹ࠺ࠡࡽࢀࠦਦ").format(e))
      bstack1lll11l111_opy_()
  except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫࡮ࡥࡡ࡮ࡩࡾࡥ࡭ࡦࡶࡵ࡭ࡨࡹ࠺ࠡࡽࢀࠦਧ").format(e))
def bstack11l1l111l_opy_(bstack1l11llllll_opy_=False):
  bstack111ll1111_opy_ = bstack1ll1lll_opy_ (u"ࠥࠦਨ")
  global bstack1l1l1l111l_opy_
  global bstack11ll1llll_opy_
  global bstack1lll1l111l_opy_
  global bstack11lll1ll1_opy_
  global ROBOT_PYTHON_ERRORS
  global bstack111llll1_opy_
  global CONFIG
  bstack1ll11ll1l_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠫࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ࡟ࡖࡕࡈࡈࠬ਩"))
  if bstack1ll11ll1l_opy_ not in [bstack1ll1lll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ਪ")]:
    bstack111ll1111_opy_ = bstack1l1l11ll1_opy_.bstack11l1llllll_opy_(EVENTS.bstack1ll1l1111l_opy_)
  percy.shutdown()
  if bstack1l1l1l111l_opy_:
    logger.warning(bstack111ll111ll_opy_.format(str(bstack1l1l1l111l_opy_)))
  else:
    try:
      bstack1111l11ll1_opy_ = bstack1l111llll1_opy_(bstack1ll1lll_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬਫ"), logger)
      if bstack1111l11ll1_opy_.get(bstack1ll1lll_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬਬ")) and bstack1111l11ll1_opy_.get(bstack1ll1lll_opy_ (u"ࠨࡰࡸࡨ࡬࡫࡟࡭ࡱࡦࡥࡱ࠭ਭ")).get(bstack1ll1lll_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫਮ")):
        logger.warning(bstack111ll111ll_opy_.format(str(bstack1111l11ll1_opy_[bstack1ll1lll_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨਯ")][bstack1ll1lll_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ਰ")])))
    except Exception as e:
      logger.error(e)
  if cli.is_running() and bstack1ll11ll1l_opy_ not in [bstack1ll1lll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭਱")]:
    if _1111l1l1_opy_ is not None:
      bstack1l11llllll_opy_ = _1111l1l1_opy_
    else:
      bstack1l11llllll_opy_ = cli.is_running()
    bstack11llllll11_opy_.invoke(Events.bstack111l1111ll_opy_)
  elif _1111l1l1_opy_ is not None:
    bstack1l11llllll_opy_ = _1111l1l1_opy_
  logger.info(bstack1llll1l111_opy_)
  global bstack1l111llll_opy_
  if bstack1l111llll_opy_:
    bstack11ll1lll1l_opy_()
  try:
    with bstack1l1l1ll1l_opy_:
      bstack11l11ll111_opy_ = bstack11ll1llll_opy_.copy()
    for driver in bstack11l11ll111_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack111llll11l_opy_)
  ROBOT_PYTHON_ERRORS = []
  if bstack111llll1_opy_ == bstack1ll1lll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬਲ"):
    ROBOT_PYTHON_ERRORS = bstack1l1l11ll1l_opy_(bstack1ll1lll_opy_ (u"ࠧࡳࡱࡥࡳࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨਲ਼"))
  if bstack111llll1_opy_ == bstack1ll1lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ਴") and len(bstack11lll1ll1_opy_) == 0:
    bstack11lll1ll1_opy_ = bstack1l1l11ll1l_opy_(bstack1ll1lll_opy_ (u"ࠩࡳࡻࡤࡶࡹࡵࡧࡶࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧਵ"))
    if len(bstack11lll1ll1_opy_) == 0:
      bstack11lll1ll1_opy_ = bstack1l1l11ll1l_opy_(bstack1ll1lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡴࡵࡶ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩਸ਼"))
  bstack11l11l11l1_opy_ = bstack1ll1lll_opy_ (u"ࠫࠬ਷")
  if len(bstack1lll1l111l_opy_) > 0:
    bstack11l11l11l1_opy_ = bstack1ll1ll1lll_opy_(bstack1lll1l111l_opy_)
  elif len(bstack11lll1ll1_opy_) > 0:
    bstack11l11l11l1_opy_ = bstack1ll1ll1lll_opy_(bstack11lll1ll1_opy_)
  elif len(ROBOT_PYTHON_ERRORS) > 0:
    bstack11l11l11l1_opy_ = bstack1ll1ll1lll_opy_(ROBOT_PYTHON_ERRORS)
  elif len(bstack11l11lll_opy_) > 0:
    bstack11l11l11l1_opy_ = bstack1ll1ll1lll_opy_(bstack11l11lll_opy_)
  if bstack1ll11ll1l_opy_ not in [bstack1ll1lll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ਸ")]:
    def bstack11ll1l1l1l_opy_():
      try:
        if bstack1ll11ll1l_opy_ in [bstack1ll1lll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬਹ"), bstack1ll1lll_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭਺")]:
          bstack1ll11l1ll_opy_()
      except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪ࡮ࡴࡡ࡭ࡡࡨࡼࡪࡩࡵࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤ਻").format(e))
    def bstack1l1l11ll11_opy_():
      try:
        if bool(bstack11l11l11l1_opy_):
          bstack11ll11l1l_opy_(bstack11l11l11l1_opy_, bstack1l11llllll_opy_=bstack1l11llllll_opy_)
        else:
          bstack11ll11l1l_opy_(bstack1l11llllll_opy_=bstack1l11llllll_opy_)
      except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡵࡨࡲࡩ࡯࡮ࡨࠢࡨࡺࡪࡴࡴ࠻ࠢࡾࢁ਼ࠧ").format(e))
    def bstack1ll1l1l11l_opy_():
      try:
        logger_utils.bstack11111l1l1l_opy_(CONFIG)
      except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡶࡩࡳࡪࡩ࡯ࡩࠣࡰࡴ࡭ࡳ࠻ࠢࡾࢁࠧ਽").format(e))
    bstack11111llll1_opy_ = threading.Thread(target=bstack11ll1l1l1l_opy_)
    bstack111lll1l_opy_ = threading.Thread(target=bstack1l1l11ll11_opy_)
    bstack11ll1111ll_opy_ = threading.Thread(target=bstack1ll1l1l11l_opy_)
    threads = [bstack11111llll1_opy_, bstack111lll1l_opy_, bstack11ll1111ll_opy_]
    for thread in threads:
      try:
        thread.start()
      except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡷࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡺࡨࡳࡧࡤࡨࠥࢁࡽ࠻ࠢࡾࢁࠧਾ").format(thread.name, e))
    for thread in threads:
      try:
        thread.join()
      except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡯ࡵࡩ࡯࡫ࡱ࡫ࠥࡺࡨࡳࡧࡤࡨࠥࢁࡽ࠻ࠢࡾࢁࠧਿ").format(thread.name, e))
    bstack1l1ll1l111_opy_(bstack11ll1l111_opy_, logger)
    bstack1l1ll1l111_opy_(os.path.join(os.getcwd(), bstack1ll1lll_opy_ (u"࠭࡬ࡰࡩࠪੀ"), bstack1ll1lll_opy_ (u"ࠧ࡬ࡧࡼ࠱ࡲ࡫ࡴࡳ࡫ࡦࡷ࠳ࡰࡳࡰࡰࠪੁ")), logger)
  if bstack1ll11ll1l_opy_ not in [bstack1ll1lll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩੂ")]:
    bstack1l1l11ll1_opy_.end(EVENTS.bstack1ll1l1111l_opy_.value, bstack111ll1111_opy_ + bstack1ll1lll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ੃"), bstack111ll1111_opy_ + bstack1ll1lll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ੄"), status=True, failure=None, test_name=None)
    bstack111ll111l_opy_()
    logger_utils.bstack11111111l_opy_()
    logging.shutdown()
  if len(ROBOT_PYTHON_ERRORS) > 0:
    sys.exit(len(ROBOT_PYTHON_ERRORS))
def bstack1ll11111l1_opy_(bstack111lll11l1_opy_, frame):
  global global_config
  logger.error(bstack1ll1l111l_opy_)
  global_config.bstack1l1ll1llll_opy_(bstack1ll1lll_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡓࡵࠧ੅"), bstack111lll11l1_opy_)
  if hasattr(signal, bstack1ll1lll_opy_ (u"࡙ࠬࡩࡨࡰࡤࡰࡸ࠭੆")):
    global_config.bstack1l1ll1llll_opy_(bstack1ll1lll_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭ੇ"), signal.Signals(bstack111lll11l1_opy_).name)
  else:
    global_config.bstack1l1ll1llll_opy_(bstack1ll1lll_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡔ࡫ࡪࡲࡦࡲࠧੈ"), bstack1ll1lll_opy_ (u"ࠨࡕࡌࡋ࡚ࡔࡋࡏࡑ࡚ࡒࠬ੉"))
  bstack1l11llllll_opy_ = cli.is_running()
  if bstack1l11llllll_opy_:
    bstack11llllll11_opy_.invoke(Events.bstack111l1111ll_opy_)
  bstack1ll11ll1l_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪ੊"))
  if bstack1ll11ll1l_opy_ == bstack1ll1lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪੋ") and not cli.is_enabled(CONFIG):
    TestHubHandler.stop(global_config.get_property(bstack1ll1lll_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡘ࡯ࡧ࡯ࡣ࡯ࠫੌ")))
  bstack11l1l111l_opy_(bstack1l11llllll_opy_)
  sys.exit(1)
def bstack1lll1111l_opy_(err):
  logger.critical(bstack11ll11l111_opy_.format(str(err)))
  bstack11ll11l1l_opy_(bstack11ll11l111_opy_.format(str(err)), True)
  atexit.unregister(bstack11l1l111l_opy_)
  bstack1ll11l1ll_opy_()
  sys.exit(1)
def bstack11l1l111ll_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack11ll11l1l_opy_(message, True)
  atexit.unregister(bstack11l1l111l_opy_)
  bstack1ll11l1ll_opy_()
  sys.exit(1)
def bstack1lllll111l_opy_():
  global CONFIG
  global bstack11lllll1l_opy_
  global bstack11l1ll11l_opy_
  global BROWSERSTACK_AUTOMATION
  CONFIG = bstack1l1ll11l1_opy_()
  load_dotenv(CONFIG.get(bstack1ll1lll_opy_ (u"ࠬ࡫࡮ࡷࡈ࡬ࡰࡪ੍࠭")))
  bstack11ll1111l1_opy_()
  bstack1l11lllll1_opy_()
  CONFIG = bstack111l1l1lll_opy_(CONFIG)
  update(CONFIG, bstack11l1ll11l_opy_)
  update(CONFIG, bstack11lllll1l_opy_)
  if not cli.is_enabled(CONFIG):
    CONFIG = bstack11llll11_opy_(CONFIG)
  BROWSERSTACK_AUTOMATION = bstack1111111l11_opy_(CONFIG)
  os.environ[bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ੎")] = BROWSERSTACK_AUTOMATION.__str__().lower()
  global_config.bstack1l1ll1llll_opy_(bstack1ll1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ੏"), BROWSERSTACK_AUTOMATION)
  if (bstack1ll1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ੐") in CONFIG and bstack1ll1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬੑ") in bstack11lllll1l_opy_) or (
          bstack1ll1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭੒") in CONFIG and bstack1ll1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ੓") not in bstack11l1ll11l_opy_):
    if os.getenv(bstack1ll1lll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩ੔")):
      CONFIG[bstack1ll1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ੕")] = os.getenv(bstack1ll1lll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫ੖"))
    else:
      if not CONFIG.get(bstack1ll1lll_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠦ੗"), bstack1ll1lll_opy_ (u"ࠤࠥ੘")) in bstack1ll1ll1l1_opy_:
        bstack1l1lll11l_opy_()
  elif (bstack1ll1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ਖ਼") not in CONFIG and bstack1ll1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ਗ਼") in CONFIG) or (
          bstack1ll1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨਜ਼") in bstack11l1ll11l_opy_ and bstack1ll1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩੜ") not in bstack11lllll1l_opy_):
    del (CONFIG[bstack1ll1lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ੝")])
  if bstack11l1111l_opy_(CONFIG):
    bstack1lll1111l_opy_(bstack11ll1l1ll_opy_)
  Config.get_instance().bstack1l1ll1llll_opy_(bstack1ll1lll_opy_ (u"ࠣࡷࡶࡩࡷࡔࡡ࡮ࡧࠥਫ਼"), CONFIG[bstack1ll1lll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ੟")])
  bstack111ll1l1ll_opy_()
  bstack11l1l1llll_opy_()
  if bstack111l11l11_opy_ and not CONFIG.get(bstack1ll1lll_opy_ (u"ࠥࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠨ੠"), bstack1ll1lll_opy_ (u"ࠦࠧ੡")) in bstack1ll1ll1l1_opy_:
    CONFIG[bstack1ll1lll_opy_ (u"ࠬࡧࡰࡱࠩ੢")] = bstack1ll1ll1l11_opy_(CONFIG)
    logger.info(bstack11l1llll1_opy_.format(CONFIG[bstack1ll1lll_opy_ (u"࠭ࡡࡱࡲࠪ੣")]))
  if not BROWSERSTACK_AUTOMATION:
    CONFIG[bstack1ll1lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ੤")] = [{}]
def bstack11l1l1l1ll_opy_(config, bstack1l11l11l1l_opy_):
  global CONFIG
  global bstack111l11l11_opy_
  CONFIG = config
  bstack111l11l11_opy_ = bstack1l11l11l1l_opy_
def bstack11l1l1llll_opy_():
  global CONFIG
  global bstack111l11l11_opy_
  if bstack1ll1lll_opy_ (u"ࠨࡣࡳࡴࠬ੥") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack11l1l111ll_opy_(e, bstack111l11ll1_opy_)
    bstack111l11l11_opy_ = True
    global_config.bstack1l1ll1llll_opy_(bstack1ll1lll_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨ੦"), True)
def bstack1ll1ll1l11_opy_(config):
  bstack1l11llll1_opy_ = bstack1ll1lll_opy_ (u"ࠪࠫ੧")
  app = config[bstack1ll1lll_opy_ (u"ࠫࡦࡶࡰࠨ੨")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1l11l111l_opy_:
      if os.path.exists(app):
        bstack1l11llll1_opy_ = bstack11l1ll1l_opy_(config, app)
      elif bstack1111ll1l1l_opy_(app):
        bstack1l11llll1_opy_ = app
      else:
        bstack1lll1111l_opy_(bstack1l11l1ll1_opy_.format(app))
    else:
      if bstack1111ll1l1l_opy_(app):
        bstack1l11llll1_opy_ = app
      elif os.path.exists(app):
        bstack1l11llll1_opy_ = bstack11l1ll1l_opy_(app)
      else:
        bstack1lll1111l_opy_(bstack1l11l111ll_opy_)
  else:
    if len(app) > 2:
      bstack1lll1111l_opy_(bstack11ll11lll_opy_)
    elif len(app) == 2:
      if bstack1ll1lll_opy_ (u"ࠬࡶࡡࡵࡪࠪ੩") in app and bstack1ll1lll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩ੪") in app:
        if os.path.exists(app[bstack1ll1lll_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ੫")]):
          bstack1l11llll1_opy_ = bstack11l1ll1l_opy_(config, app[bstack1ll1lll_opy_ (u"ࠨࡲࡤࡸ࡭࠭੬")], app[bstack1ll1lll_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ੭")])
        else:
          bstack1lll1111l_opy_(bstack1l11l1ll1_opy_.format(app))
      else:
        bstack1lll1111l_opy_(bstack11ll11lll_opy_)
    else:
      for key in app:
        if key in bstack1lllllllll_opy_:
          if key == bstack1ll1lll_opy_ (u"ࠪࡴࡦࡺࡨࠨ੮"):
            if os.path.exists(app[key]):
              bstack1l11llll1_opy_ = bstack11l1ll1l_opy_(config, app[key])
            else:
              bstack1lll1111l_opy_(bstack1l11l1ll1_opy_.format(app))
          else:
            bstack1l11llll1_opy_ = app[key]
        else:
          bstack1lll1111l_opy_(bstack11111ll1_opy_)
  return bstack1l11llll1_opy_
def bstack1111ll1l1l_opy_(bstack1l11llll1_opy_):
  import re
  bstack1l1l1lll1_opy_ = re.compile(bstack1ll1lll_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬࠧࠦ੯"))
  bstack1l1lll111l_opy_ = re.compile(bstack1ll1lll_opy_ (u"ࡷࠨ࡞࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭࠳ࡠࡧ࠭ࡻࡃ࠰࡞࠵࠳࠹࡝ࡡ࠱ࡠ࠲ࡣࠪࠥࠤੰ"))
  if bstack1ll1lll_opy_ (u"࠭ࡢࡴ࠼࠲࠳ࠬੱ") in bstack1l11llll1_opy_ or re.fullmatch(bstack1l1l1lll1_opy_, bstack1l11llll1_opy_) or re.fullmatch(bstack1l1lll111l_opy_, bstack1l11llll1_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack11ll11111_opy_, stage=STAGE.bstack1111l1ll1_opy_, bstack1l1l1l11_opy_=SESSION_NAME)
def bstack11l1ll1l_opy_(config, path, bstack111l1l11l1_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1ll1lll_opy_ (u"ࠧࡳࡤࠪੲ")).read()).hexdigest()
  bstack1ll1111l1l_opy_ = bstack11ll1l11ll_opy_(md5_hash)
  bstack1l11llll1_opy_ = None
  if bstack1ll1111l1l_opy_:
    logger.info(bstack11ll11l1l1_opy_.format(bstack1ll1111l1l_opy_, md5_hash))
    return bstack1ll1111l1l_opy_
  bstack11lllll111_opy_ = datetime.datetime.now()
  multipart_data = MultipartEncoder(
    fields={
      bstack1ll1lll_opy_ (u"ࠨࡨ࡬ࡰࡪ࠭ੳ"): (os.path.basename(path), open(os.path.abspath(path), bstack1ll1lll_opy_ (u"ࠩࡵࡦࠬੴ")), bstack1ll1lll_opy_ (u"ࠪࡸࡪࡾࡴ࠰ࡲ࡯ࡥ࡮ࡴࠧੵ")),
      bstack1ll1lll_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧ੶"): bstack111l1l11l1_opy_
    }
  )
  response = requests.post(bstack11lllll1ll_opy_, data=multipart_data,
                           headers={bstack1ll1lll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ੷"): multipart_data.content_type},
                           auth=(config[bstack1ll1lll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ੸")], config[bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ੹")]))
  try:
    res = json.loads(response.text)
    bstack1l11llll1_opy_ = res[bstack1ll1lll_opy_ (u"ࠨࡣࡳࡴࡤࡻࡲ࡭ࠩ੺")]
    logger.info(bstack1111ll1l_opy_.format(bstack1l11llll1_opy_))
    bstack1l111l11l1_opy_(md5_hash, bstack1l11llll1_opy_)
    cli.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺ࡶࡲ࡯ࡳࡦࡪ࡟ࡢࡲࡳࠦ੻"), datetime.datetime.now() - bstack11lllll111_opy_)
  except ValueError as err:
    bstack1lll1111l_opy_(bstack1l1lll1lll_opy_.format(str(err)))
  return bstack1l11llll1_opy_
def bstack111ll1l1ll_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack1ll1ll11_opy_
  bstack111l11l111_opy_ = 1
  bstack1l1ll11lll_opy_ = 1
  if bstack1ll1lll_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ੼") in CONFIG:
    bstack1l1ll11lll_opy_ = CONFIG[bstack1ll1lll_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ੽")]
  else:
    bstack1l1ll11lll_opy_ = bstack1lll111ll1_opy_(framework_name, args) or 1
  if bstack1ll1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ੾") in CONFIG:
    bstack111l11l111_opy_ = len(CONFIG[bstack1ll1lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ੿")])
  bstack1ll1ll11_opy_ = int(bstack1l1ll11lll_opy_) * int(bstack111l11l111_opy_)
def bstack1lll111ll1_opy_(framework_name, args):
  if framework_name == bstack1l11l1l1_opy_ and args and bstack1ll1lll_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ઀") in args:
      bstack11l111111l_opy_ = args.index(bstack1ll1lll_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ઁ"))
      return int(args[bstack11l111111l_opy_ + 1]) or 1
  return 1
def bstack11ll1l11ll_opy_(md5_hash):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1ll1lll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡬ࡰࡥ࡮ࠤࡳࡵࡴࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨ࠰ࠥࡻࡳࡪࡰࡪࠤࡧࡧࡳࡪࡥࠣࡪ࡮ࡲࡥࠡࡱࡳࡩࡷࡧࡴࡪࡱࡱࡷࠬં"))
    bstack1llll1llll_opy_ = os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"ࠪࢂࠬઃ")), bstack1ll1lll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ઄"), bstack1ll1lll_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭અ"))
    if os.path.exists(bstack1llll1llll_opy_):
      try:
        bstack1llllll11_opy_ = json.load(open(bstack1llll1llll_opy_, bstack1ll1lll_opy_ (u"࠭ࡲࡣࠩઆ")))
        if md5_hash in bstack1llllll11_opy_:
          bstack1l1l11l1_opy_ = bstack1llllll11_opy_[md5_hash]
          bstack11lll111l1_opy_ = datetime.datetime.now()
          bstack1111l11111_opy_ = datetime.datetime.strptime(bstack1l1l11l1_opy_[bstack1ll1lll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪઇ")], bstack1ll1lll_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬઈ"))
          if (bstack11lll111l1_opy_ - bstack1111l11111_opy_).days > 30:
            return None
          elif version.parse(str(__version__)) > version.parse(bstack1l1l11l1_opy_[bstack1ll1lll_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧઉ")]):
            return None
          return bstack1l1l11l1_opy_[bstack1ll1lll_opy_ (u"ࠪ࡭ࡩ࠭ઊ")]
      except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡶࡪࡧࡤࡪࡰࡪࠤࡒࡊ࠵ࠡࡪࡤࡷ࡭ࠦࡦࡪ࡮ࡨ࠾ࠥࢁࡽࠨઋ").format(str(e)))
    return None
  bstack1llll1llll_opy_ = os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"ࠬࢄࠧઌ")), bstack1ll1lll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ઍ"), bstack1ll1lll_opy_ (u"ࠧࡢࡲࡳ࡙ࡵࡲ࡯ࡢࡦࡐࡈ࠺ࡎࡡࡴࡪ࠱࡮ࡸࡵ࡮ࠨ઎"))
  lock_file = bstack1llll1llll_opy_ + bstack1ll1lll_opy_ (u"ࠨ࠰࡯ࡳࡨࡱࠧએ")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack1llll1llll_opy_):
        with open(bstack1llll1llll_opy_, bstack1ll1lll_opy_ (u"ࠩࡵࠫઐ")) as f:
          content = f.read().strip()
          if content:
            bstack1llllll11_opy_ = json.loads(content)
            if md5_hash in bstack1llllll11_opy_:
              bstack1l1l11l1_opy_ = bstack1llllll11_opy_[md5_hash]
              bstack11lll111l1_opy_ = datetime.datetime.now()
              bstack1111l11111_opy_ = datetime.datetime.strptime(bstack1l1l11l1_opy_[bstack1ll1lll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ઑ")], bstack1ll1lll_opy_ (u"ࠫࠪࡪ࠯ࠦ࡯࠲ࠩ࡞ࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨ઒"))
              if (bstack11lll111l1_opy_ - bstack1111l11111_opy_).days > 30:
                return None
              elif version.parse(str(__version__)) > version.parse(bstack1l1l11l1_opy_[bstack1ll1lll_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪઓ")]):
                return None
              return bstack1l1l11l1_opy_[bstack1ll1lll_opy_ (u"࠭ࡩࡥࠩઔ")]
      return None
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡷࡪࡶ࡫ࠤ࡫࡯࡬ࡦࠢ࡯ࡳࡨࡱࡩ࡯ࡩࠣࡪࡴࡸࠠࡎࡆ࠸ࠤ࡭ࡧࡳࡩ࠼ࠣࡿࢂ࠭ક").format(str(e)))
    return None
def bstack1l111l11l1_opy_(md5_hash, bstack1l11llll1_opy_):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1ll1lll_opy_ (u"ࠨࡨ࡬ࡰࡪࡲ࡯ࡤ࡭ࠣࡲࡴࡺࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧ࠯ࠤࡺࡹࡩ࡯ࡩࠣࡦࡦࡹࡩࡤࠢࡩ࡭ࡱ࡫ࠠࡰࡲࡨࡶࡦࡺࡩࡰࡰࡶࠫખ"))
    bstack1ll11ll1ll_opy_ = os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"ࠩࢁࠫગ")), bstack1ll1lll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪઘ"))
    if not os.path.exists(bstack1ll11ll1ll_opy_):
      os.makedirs(bstack1ll11ll1ll_opy_)
    bstack1llll1llll_opy_ = os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"ࠫࢃ࠭ઙ")), bstack1ll1lll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬચ"), bstack1ll1lll_opy_ (u"࠭ࡡࡱࡲࡘࡴࡱࡵࡡࡥࡏࡇ࠹ࡍࡧࡳࡩ࠰࡭ࡷࡴࡴࠧછ"))
    bstack111l1l1111_opy_ = {
      bstack1ll1lll_opy_ (u"ࠧࡪࡦࠪજ"): bstack1l11llll1_opy_,
      bstack1ll1lll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫઝ"): datetime.datetime.strftime(datetime.datetime.now(), bstack1ll1lll_opy_ (u"ࠩࠨࡨ࠴ࠫ࡭࠰ࠧ࡜ࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭ઞ")),
      bstack1ll1lll_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨટ"): str(__version__)
    }
    try:
      bstack1llllll11_opy_ = {}
      if os.path.exists(bstack1llll1llll_opy_):
        bstack1llllll11_opy_ = json.load(open(bstack1llll1llll_opy_, bstack1ll1lll_opy_ (u"ࠫࡷࡨࠧઠ")))
      bstack1llllll11_opy_[md5_hash] = bstack111l1l1111_opy_
      with open(bstack1llll1llll_opy_, bstack1ll1lll_opy_ (u"ࠧࡽࠫࠣડ")) as outfile:
        json.dump(bstack1llllll11_opy_, outfile)
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡻࡰࡥࡣࡷ࡭ࡳ࡭ࠠࡎࡆ࠸ࠤ࡭ࡧࡳࡩࠢࡩ࡭ࡱ࡫࠺ࠡࡽࢀࠫઢ").format(str(e)))
    return
  bstack1ll11ll1ll_opy_ = os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"ࠧࡿࠩણ")), bstack1ll1lll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨત"))
  if not os.path.exists(bstack1ll11ll1ll_opy_):
    os.makedirs(bstack1ll11ll1ll_opy_)
  bstack1llll1llll_opy_ = os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"ࠩࢁࠫથ")), bstack1ll1lll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪદ"), bstack1ll1lll_opy_ (u"ࠫࡦࡶࡰࡖࡲ࡯ࡳࡦࡪࡍࡅ࠷ࡋࡥࡸ࡮࠮࡫ࡵࡲࡲࠬધ"))
  lock_file = bstack1llll1llll_opy_ + bstack1ll1lll_opy_ (u"ࠬ࠴࡬ࡰࡥ࡮ࠫન")
  bstack111l1l1111_opy_ = {
    bstack1ll1lll_opy_ (u"࠭ࡩࡥࠩ઩"): bstack1l11llll1_opy_,
    bstack1ll1lll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪપ"): datetime.datetime.strftime(datetime.datetime.now(), bstack1ll1lll_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬફ")),
    bstack1ll1lll_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧબ"): str(__version__)
  }
  try:
    with FileLock(lock_file, timeout=10):
      bstack1llllll11_opy_ = {}
      if os.path.exists(bstack1llll1llll_opy_):
        with open(bstack1llll1llll_opy_, bstack1ll1lll_opy_ (u"ࠪࡶࠬભ")) as f:
          content = f.read().strip()
          if content:
            bstack1llllll11_opy_ = json.loads(content)
      bstack1llllll11_opy_[md5_hash] = bstack111l1l1111_opy_
      with open(bstack1llll1llll_opy_, bstack1ll1lll_opy_ (u"ࠦࡼࠨમ")) as outfile:
        json.dump(bstack1llllll11_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡼ࡯ࡴࡩࠢࡩ࡭ࡱ࡫ࠠ࡭ࡱࡦ࡯࡮ࡴࡧࠡࡨࡲࡶࠥࡓࡄ࠶ࠢ࡫ࡥࡸ࡮ࠠࡶࡲࡧࡥࡹ࡫࠺ࠡࡽࢀࠫય").format(str(e)))
def bstack1llll11l_opy_(self):
  return
def bstack1l1l1l11l1_opy_(self):
  return
def bstack11ll1l1lll_opy_():
  global bstack1111l1l1ll_opy_
  bstack1111l1l1ll_opy_ = True
def bstack1l1111l1l_opy_(self):
  global FRAMEWORK_NAME
  global bstack1lllll1ll1_opy_
  global bstack1l1l1l111_opy_
  bstack111l1l1l1_opy_ = bstack1l1l11ll1_opy_.bstack11l1llllll_opy_(EVENTS.bstack1lll1l11_opy_)
  try:
    if bstack1ll1lll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ર") in FRAMEWORK_NAME and self.session_id != None and bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫ઱"), bstack1ll1lll_opy_ (u"ࠨࠩલ")) != bstack1ll1lll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪળ"):
      bstack111llll11_opy_ = bstack1ll1lll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ઴") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1ll1lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫવ")
      if bstack111llll11_opy_ == bstack1ll1lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬશ"):
        bstack1ll1llll1_opy_(logger)
      if self != None:
        bstack1ll1lll1l_opy_(self, bstack111llll11_opy_, bstack1ll1lll_opy_ (u"࠭ࠬࠡࠩષ").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack1ll1lll_opy_ (u"ࠧࠨસ")
    if bstack1ll1lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨહ") in FRAMEWORK_NAME and getattr(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ઺"), None):
      bstack1l11111l_opy_.bstack1lll1l111_opy_(self, bstack1l11ll11l1_opy_, logger, wait=True)
    if bstack1ll1lll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ઻") in FRAMEWORK_NAME:
      bstack1l11ll1l1_opy_.bstack11l1lll1l1_opy_(self)
    bstack1l1l11ll1_opy_.end(EVENTS.bstack1lll1l11_opy_.value, bstack111l1l1l1_opy_ + bstack1ll1lll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷ઼ࠦ"), bstack111l1l1l1_opy_ + bstack1ll1lll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥઽ"), status=True, failure=None, test_name=None)
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࠢા") + str(e))
    bstack1l1l11ll1_opy_.end(EVENTS.bstack1lll1l11_opy_.value, bstack111l1l1l1_opy_ + bstack1ll1lll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢિ"), bstack111l1l1l1_opy_ + bstack1ll1lll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨી"), status=False, failure=str(e), test_name=None)
  bstack1l1l1l111_opy_(self)
  self.session_id = None
def bstack1l1ll11ll_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack1l1ll111_opy_
    global FRAMEWORK_NAME
    command_executor = kwargs.get(bstack1ll1lll_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠬુ"), bstack1ll1lll_opy_ (u"ࠪࠫૂ"))
    bstack1l1l1111l1_opy_ = False
    if type(command_executor) == str and bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧૃ") in command_executor:
      bstack1l1l1111l1_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨૄ") in str(getattr(command_executor, bstack1ll1lll_opy_ (u"࠭࡟ࡶࡴ࡯ࠫૅ"), bstack1ll1lll_opy_ (u"ࠧࠨ૆"))):
      bstack1l1l1111l1_opy_ = True
    else:
      kwargs = a11y.bstack1l1lllll1_opy_(bstack11lll1l111_opy_=kwargs, config=CONFIG)
      return bstack1l1ll11l_opy_(self, *args, **kwargs)
    if bstack1l1l1111l1_opy_:
      bstack11l1ll1l11_opy_ = TestHubUtils.bstack1ll1l1ll1_opy_(CONFIG, FRAMEWORK_NAME)
      if kwargs.get(bstack1ll1lll_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩે")):
        kwargs[bstack1ll1lll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪૈ")] = bstack1l1ll111_opy_(kwargs[bstack1ll1lll_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫૉ")], FRAMEWORK_NAME, CONFIG, bstack11l1ll1l11_opy_)
      elif kwargs.get(bstack1ll1lll_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ૊")):
        kwargs[bstack1ll1lll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬો")] = bstack1l1ll111_opy_(kwargs[bstack1ll1lll_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ૌ")], FRAMEWORK_NAME, CONFIG, bstack11l1ll1l11_opy_)
  except Exception as e:
    logger.error(bstack1ll1lll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩࡧࡱࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡕࡇࡏࠥࡩࡡࡱࡵ࠽ࠤࢀࢃ્ࠢ").format(str(e)))
  return bstack1l1ll11l_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack1l111l1l1_opy_, stage=STAGE.bstack1111l1ll1_opy_, bstack1l1l1l11_opy_=SESSION_NAME)
def bstack11lll1l11l_opy_(self, command_executor=bstack1ll1lll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰࠳࠵࠻࠳࠶࠮࠱࠰࠴࠾࠹࠺࠴࠵ࠤ૎"), *args, **kwargs):
  global bstack1lllll1ll1_opy_
  global bstack11ll1llll_opy_
  bstack11ll1ll1_opy_ = bstack1l1ll11ll_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack11llll1l_opy_.on():
    return bstack11ll1ll1_opy_
  try:
    if isinstance(command_executor, (str, bytes)):
      bstack11ll1ll1l_opy_ = str(command_executor)
    else:
      bstack11ll1ll1l_opy_ = str(
        getattr(command_executor, bstack1ll1lll_opy_ (u"ࠩࡢࡹࡷࡲࠧ૏"), None)
        or getattr(getattr(command_executor, bstack1ll1lll_opy_ (u"ࠪࡣࡨࡲࡩࡦࡰࡷࡣࡨࡵ࡮ࡧ࡫ࡪࠫૐ"), None), bstack1ll1lll_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡣࡸ࡫ࡲࡷࡧࡵࡣࡦࡪࡤࡳࠩ૑"), None)
        or bstack1ll1lll_opy_ (u"ࠬ࠭૒")
      )
    logger.debug(bstack1ll1lll_opy_ (u"࠭ࡈࡶࡤ࡙ࠣࡗࡒࠠࡪࡵࠣ࠱ࠥࢁࡽࠨ૓").format(bstack11ll1ll1l_opy_.split(bstack1ll1lll_opy_ (u"ࠧࡁࠩ૔"))[-1] if bstack1ll1lll_opy_ (u"ࠨࡂࠪ૕") in bstack11ll1ll1l_opy_ else bstack11ll1ll1l_opy_))
    if bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬ૖") in bstack11ll1ll1l_opy_:
      global_config.bstack1l1ll1llll_opy_(bstack1ll1lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫ૗"), True)
  except Exception as e:
    logger.error(bstack1ll1lll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡦ࡬ࡪࡩ࡫ࡪࡰࡪࠤࡨࡵ࡭࡮ࡣࡱࡨࠥ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫ૘").format(str(e)))
    pass
  if (isinstance(command_executor, str) and bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨ૙") in command_executor):
    global_config.bstack1l1ll1llll_opy_(bstack1ll1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ૚"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1l1l111lll_opy_ = getattr(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡔࡦࡵࡷࡑࡪࡺࡡࠨ૛"), None)
  bstack1ll1l1l11_opy_ = {}
  if self.capabilities is not None:
    bstack1ll1l1l11_opy_[bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧ૜")] = self.capabilities.get(bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ૝"))
    bstack1ll1l1l11_opy_[bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ૞")] = self.capabilities.get(bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ૟"))
    bstack1ll1l1l11_opy_[bstack1ll1lll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡤࡵࡰࡵ࡫ࡲࡲࡸ࠭ૠ")] = self.capabilities.get(bstack1ll1lll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫૡ"))
  if CONFIG.get(bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧૢ"), False) and a11y.bstack11ll1ll11l_opy_(bstack1ll1l1l11_opy_):
    threading.current_thread().a11yPlatform = True
  if bstack1ll1lll_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨૣ") in FRAMEWORK_NAME or bstack1ll1lll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ૤") in FRAMEWORK_NAME:
    TestHubHandler.send_cbt_info(self)
  if bstack1ll1lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ૥") in FRAMEWORK_NAME and bstack1l1l111lll_opy_ and bstack1l1l111lll_opy_.get(bstack1ll1lll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ૦"), bstack1ll1lll_opy_ (u"ࠬ࠭૧")) == bstack1ll1lll_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧ૨"):
    TestHubHandler.send_cbt_info(self)
  bstack1lllll1ll1_opy_ = self.session_id
  with bstack1l1l1ll1l_opy_:
    bstack11ll1llll_opy_.append(self)
  return bstack11ll1ll1_opy_
def bstack1ll1l11l1l_opy_(args):
  return bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲࠨ૩") in str(args)
def bstack11l1ll1ll1_opy_(self, driver_command, *args, **kwargs):
  global bstack1l11lll1l1_opy_
  global bstack1l1llll1l1_opy_
  bstack11llll1ll1_opy_ = bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬ૪"), None) and bstack1l11lll1_opy_(
          threading.current_thread(), bstack1ll1lll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ૫"), None)
  bstack111llll1l_opy_ = bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ૬"), None) and bstack1l11lll1_opy_(
          threading.current_thread(), bstack1ll1lll_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭૭"), None)
  bstack11lll1111_opy_ = getattr(self, bstack1ll1lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬ૮"), None) != None and getattr(self, bstack1ll1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭૯"), None) == True
  if not bstack1l1llll1l1_opy_ and bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ૰") in CONFIG and CONFIG[bstack1ll1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ૱")] == True and accessibility_scripts.bstack11l11llll_opy_(driver_command) and (bstack11lll1111_opy_ or bstack11llll1ll1_opy_ or bstack111llll1l_opy_) and not bstack1ll1l11l1l_opy_(args):
    try:
      bstack1l1llll1l1_opy_ = True
      logger.debug(bstack1ll1lll_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡽࢀࠫ૲").format(driver_command))
      bstack11111l111_opy_ = perform_scan(self, driver_command=driver_command)
      logger.debug(bstack11111l111_opy_)
      try:
        log_data = {
          bstack1ll1lll_opy_ (u"ࠥࡶࡪࡷࡵࡦࡵࡷࠦ૳"): {
            bstack1ll1lll_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࠧ૴"): bstack1ll1lll_opy_ (u"ࠧࡇ࠱࠲࡛ࡢࡗࡈࡇࡎࠣ૵"),
            bstack1ll1lll_opy_ (u"ࠨࡰࡢࡴࡤࡱࡪࡺࡥࡳࡵࠥ૶"): [
              {
                bstack1ll1lll_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢ૷"): driver_command
              }
            ]
          },
          bstack1ll1lll_opy_ (u"ࠣࡴࡨࡷࡵࡵ࡮ࡴࡧࠥ૸"): {
            bstack1ll1lll_opy_ (u"ࠤࡥࡳࡩࡿࠢૹ"): {
              bstack1ll1lll_opy_ (u"ࠥࡱࡸ࡭ࠢૺ"): bstack11111l111_opy_.get(bstack1ll1lll_opy_ (u"ࠦࡲࡹࡧࠣૻ"), bstack1ll1lll_opy_ (u"ࠧࠨૼ")) if isinstance(bstack11111l111_opy_, dict) else bstack1ll1lll_opy_ (u"ࠨࠢ૽"),
              bstack1ll1lll_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳࠣ૾"): bstack11111l111_opy_.get(bstack1ll1lll_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴࠤ૿"), True) if isinstance(bstack11111l111_opy_, dict) else True
            }
          }
        }
        logger.debug(bstack1ll1lll_opy_ (u"ࠩࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡧࡦࡴࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡱࡵࡧࠡࡦࡤࡸࡦࡀࠠࡼࡿࠪ଀").format(log_data))
        automation_logger.info(json.dumps(log_data, separators=(bstack1ll1lll_opy_ (u"ࠪ࠰ࠬଁ"), bstack1ll1lll_opy_ (u"ࠫ࠿࠭ଂ"))))
      except Exception as bstack1lll1l11ll_opy_:
        logger.debug(bstack1ll1lll_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡮ࡲ࡫ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡣࡢࡰࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠬଃ").format(str(bstack1lll1l11ll_opy_)))
    except Exception as err:
      logger.debug(bstack1ll1lll_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡩࡷ࡬࡯ࡳ࡯ࠣࡷࡨࡧ࡮ࠡࡽࢀࠫ଄").format(str(err)))
    bstack1l1llll1l1_opy_ = False
  response = bstack1l11lll1l1_opy_(self, driver_command, *args, **kwargs)
  if (bstack1ll1lll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ଅ") in str(FRAMEWORK_NAME).lower() or bstack1ll1lll_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨଆ") in str(FRAMEWORK_NAME).lower()) and bstack11llll1l_opy_.on():
    try:
      if driver_command == bstack1ll1lll_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭ଇ"):
        TestHubHandler.bstack1111ll1lll_opy_({
            bstack1ll1lll_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩଈ"): response[bstack1ll1lll_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪଉ")],
            bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬଊ"): TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack11llll1l_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
def bstack1111l111l_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack1lllll1ll1_opy_
  global PLATFORM_INDEX
  global SESSION_NAME
  global PARALLELISE_VANILLA_PYTHON
  global PARALLELISE_THREADING_PYTHON
  global FRAMEWORK_NAME
  global bstack1l1ll11l_opy_
  global bstack11ll1llll_opy_
  global bstack11ll111l11_opy_
  global bstack1l11ll11l1_opy_
  bstack111l1l1l1_opy_ = bstack1l1l11ll1_opy_.bstack11l1llllll_opy_(EVENTS.bstack1lll1l1111_opy_.value)
  if os.getenv(bstack1ll1lll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫଋ")) is not None and a11y.bstack11ll11ll_opy_(CONFIG) is None:
    CONFIG[bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧଌ")] = True
  CONFIG[bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ଍")] = str(FRAMEWORK_NAME) + str(__version__)
  bstack111l1ll11l_opy_ = os.environ[bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ଎")]
  bstack11l1ll1l11_opy_ = TestHubUtils.bstack1ll1l1ll1_opy_(CONFIG, FRAMEWORK_NAME)
  CONFIG[bstack1ll1lll_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ଏ")] = bstack111l1ll11l_opy_
  CONFIG[bstack1ll1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ଐ")] = bstack11l1ll1l11_opy_
  if CONFIG.get(bstack1ll1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ଑"),bstack1ll1lll_opy_ (u"࠭ࠧ଒")) and bstack1ll1lll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ଓ") in FRAMEWORK_NAME:
    CONFIG[bstack1ll1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨଔ")].pop(bstack1ll1lll_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧକ"), None)
    CONFIG[bstack1ll1lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪଖ")].pop(bstack1ll1lll_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩଗ"), None)
  command_executor = bstack11llll1l1l_opy_()
  logger.debug(bstack111lllll1_opy_.format(command_executor))
  proxy = bstack1l11111111_opy_(CONFIG, proxy)
  bstack11111lll_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
  try:
    if PARALLELISE_VANILLA_PYTHON is True:
      bstack11111lll_opy_ = int(multiprocessing.current_process().name)
    elif PARALLELISE_THREADING_PYTHON is True:
      bstack11111lll_opy_ = int(threading.current_thread().name)
  except:
    bstack11111lll_opy_ = 0
  bstack11l1l11lll_opy_ = get_caps(CONFIG, bstack11111lll_opy_)
  logger.debug(CONFIG_FILE_CONTENT.format(str(bstack11l1l11lll_opy_)))
  if bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩଘ") in CONFIG and bstack1l11l11111_opy_(CONFIG[bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪଙ")]):
    update_caps_for_local(bstack11l1l11lll_opy_)
  if a11y.is_enabled_platform(CONFIG, bstack11111lll_opy_) and a11y.is_platform_supported(bstack11l1l11lll_opy_, options, desired_capabilities, CONFIG):
    threading.current_thread().a11yPlatform = True
    if (cli.accessibility is None or not cli.accessibility.is_enabled()):
      a11y.set_capabilities(bstack11l1l11lll_opy_, CONFIG)
  if desired_capabilities:
    bstack1l111l1l_opy_ = bstack111l1l1lll_opy_(desired_capabilities)
    bstack1l111l1l_opy_[bstack1ll1lll_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧଚ")] = bstack1ll1ll11ll_opy_(CONFIG)
    bstack1l1l1l11l_opy_ = get_caps(bstack1l111l1l_opy_)
    if bstack1l1l1l11l_opy_:
      bstack11l1l11lll_opy_ = update(bstack1l1l1l11l_opy_, bstack11l1l11lll_opy_)
    desired_capabilities = None
  if options:
    bstack1ll111l1ll_opy_(options, bstack11l1l11lll_opy_)
  if not options:
    options = bstack1l1l1llll_opy_(bstack11l1l11lll_opy_)
  try:
    if bstack111l1ll1l_opy_:
      def _1l1llllll1_opy_(bstack11l11l111l_opy_):
        if not isinstance(bstack11l11l111l_opy_, dict):
          return
        for _11l111ll_opy_ in list(bstack11l11l111l_opy_.keys()):
          _111llllll1_opy_ = bstack11l11l111l_opy_[_11l111ll_opy_]
          if _111llllll1_opy_ is None:
            bstack11l11l111l_opy_.pop(_11l111ll_opy_, None)
          elif isinstance(_111llllll1_opy_, dict):
            _1l1llllll1_opy_(_111llllll1_opy_)
      _1l1llllll1_opy_(bstack11l1l11lll_opy_)
      _1l1llllll1_opy_(desired_capabilities)
      if options is not None and hasattr(options, bstack1ll1lll_opy_ (u"ࠨࡡࡦࡥࡵࡹࠧଛ")):
        _1l1llllll1_opy_(options._caps)
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠤࡰࡳࡩࡥࡩ࡯࡫ࡷࠬ࠮ࠦࡰࡰࡵࡷ࠱ࡴࡶࡴࡪࡱࡱࡷࠥࡶࡲࡶࡰࡨࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽࠣଜ").format(e))
  if bstack111l1ll1l_opy_:
    options = bstack11llll1l1_opy_(options)
  bstack1l11ll11l1_opy_ = CONFIG.get(bstack1ll1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ଝ"))[bstack11111lll_opy_]
  if proxy and bstack1l1l11l1l1_opy_() >= version.parse(bstack1ll1lll_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫଞ")):
    options.proxy(proxy)
  if options and bstack1l1l11l1l1_opy_() >= version.parse(bstack1ll1lll_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫଟ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1l1l11l1l1_opy_() < version.parse(bstack1ll1lll_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬଠ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack11l1l11lll_opy_)
  logger.info(bstack1ll111ll11_opy_)
  bstack1l111ll111_opy_.end(EVENTS.bstack11ll1111l_opy_.value, EVENTS.bstack11ll1111l_opy_.value + bstack1ll1lll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢଡ"), EVENTS.bstack11ll1111l_opy_.value + bstack1ll1lll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨଢ"), status=True, failure=None, test_name=SESSION_NAME)
  if bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡴࡷࡵࡦࡪ࡮ࡨࠫଣ") in kwargs:
    del kwargs[bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡵࡸ࡯ࡧ࡫࡯ࡩࠬତ")]
  bstack1l1l11ll1_opy_.end(EVENTS.bstack1lll1l1111_opy_.value, bstack111l1l1l1_opy_ + bstack1ll1lll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦଥ"), bstack111l1l1l1_opy_ + bstack1ll1lll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥଦ"), status=True, failure=None, test_name=SESSION_NAME)
  try:
    if bstack1l1l11l1l1_opy_() >= version.parse(bstack1ll1lll_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ଧ")):
      bstack1l1ll11l_opy_(self, command_executor=command_executor,
                options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
    elif bstack1l1l11l1l1_opy_() >= version.parse(bstack1ll1lll_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ନ")):
      bstack1l1ll11l_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities, options=options,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l1l11l1l1_opy_() >= version.parse(bstack1ll1lll_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨ଩")):
      bstack1l1ll11l_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    else:
      bstack1l1ll11l_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive)
  except Exception as bstack1111llll1_opy_:
    logger.error(bstack11l111l1_opy_.format(bstack1ll1lll_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠨପ"), str(bstack1111llll1_opy_)))
    raise bstack1111llll1_opy_
  bstack111l1l1l1_opy_ = bstack1l1l11ll1_opy_.bstack11l1llllll_opy_(EVENTS.bstack1l111l1l1_opy_.value)
  if a11y.is_enabled_platform(CONFIG, bstack11111lll_opy_) and a11y.is_platform_supported(self.caps, options, desired_capabilities):
    if CONFIG[bstack1ll1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬଫ")][bstack1ll1lll_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪବ")] == True:
      threading.current_thread().appA11yPlatform = True
      if cli.accessibility is None or not cli.accessibility.is_enabled():
        a11y.set_capabilities(bstack11l1l11lll_opy_, CONFIG)
  try:
    bstack11l1ll11_opy_ = bstack1ll1lll_opy_ (u"ࠬ࠭ଭ")
    if bstack1l1l11l1l1_opy_() >= version.parse(bstack1ll1lll_opy_ (u"࠭࠴࠯࠲࠱࠴ࡧ࠷ࠧମ")):
      if self.caps is not None:
        bstack11l1ll11_opy_ = self.caps.get(bstack1ll1lll_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢଯ"))
    else:
      if self.capabilities is not None:
        bstack11l1ll11_opy_ = self.capabilities.get(bstack1ll1lll_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣର"))
    if bstack11l1ll11_opy_:
      bstack1lll1ll111_opy_(bstack11l1ll11_opy_)
      if bstack1l1l11l1l1_opy_() <= version.parse(bstack1ll1lll_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩ଱")):
        if bstack1l11ll1ll_opy_.startswith(bstack1ll1lll_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫଲ")) or bstack1l11ll1ll_opy_.startswith(bstack1ll1lll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࠭ଳ")):
          self.command_executor._url = bstack1l11ll1ll_opy_
        else:
          self.command_executor._url = bstack1ll1lll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨ଴") + bstack1l11ll1ll_opy_ + bstack1ll1lll_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥଵ")
      else:
        self.command_executor._url = bstack1ll1lll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤଶ") + bstack11l1ll11_opy_ + bstack1ll1lll_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤଷ")
      logger.debug(bstack1lllll1ll_opy_.format(bstack11l1ll11_opy_))
    else:
      logger.debug(bstack11111ll1l1_opy_.format(bstack1ll1lll_opy_ (u"ࠤࡒࡴࡹ࡯࡭ࡢ࡮ࠣࡌࡺࡨࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦࠥସ")))
  except Exception as e:
    logger.debug(bstack11111ll1l1_opy_.format(e))
  if bstack1ll1lll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩହ") in FRAMEWORK_NAME:
    bstack1l11l1l11l_opy_(PLATFORM_INDEX, bstack11ll111l11_opy_)
  bstack1lllll1ll1_opy_ = self.session_id
  if bstack1ll1lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ଺") in FRAMEWORK_NAME or bstack1ll1lll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ଻") in FRAMEWORK_NAME or bstack1ll1lll_opy_ (u"࠭ࡲࡰࡤࡲࡸ଼ࠬ") in FRAMEWORK_NAME or bstack1ll1lll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡨࡧࡱࡩࡷ࡯ࡣࠨଽ") in FRAMEWORK_NAME:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack1l1l111lll_opy_ = getattr(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡕࡧࡶࡸࡒ࡫ࡴࡢࠩା"), None)
  if bstack1ll1lll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩି") in FRAMEWORK_NAME or bstack1ll1lll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩୀ") in FRAMEWORK_NAME:
    TestHubHandler.send_cbt_info(self)
  if bstack1ll1lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫୁ") in FRAMEWORK_NAME and bstack1l1l111lll_opy_ and bstack1l1l111lll_opy_.get(bstack1ll1lll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬୂ"), bstack1ll1lll_opy_ (u"࠭ࠧୃ")) == bstack1ll1lll_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨୄ"):
    TestHubHandler.send_cbt_info(self)
  with bstack1l1l1ll1l_opy_:
    bstack11ll1llll_opy_.append(self)
  if bstack1ll1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ୅") in CONFIG and bstack1ll1lll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ୆") in CONFIG[bstack1ll1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭େ")][bstack11111lll_opy_]:
    SESSION_NAME = CONFIG[bstack1ll1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧୈ")][bstack11111lll_opy_][bstack1ll1lll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ୉")]
  logger.debug(bstack1l1ll1ll1l_opy_.format(bstack1lllll1ll1_opy_))
  bstack1l1l11ll1_opy_.end(EVENTS.bstack1l111l1l1_opy_.value, bstack111l1l1l1_opy_ + bstack1ll1lll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ୊"), bstack111l1l1l1_opy_ + bstack1ll1lll_opy_ (u"ࠢ࠻ࡧࡱࡨࠧୋ"), status=True, failure=None, test_name=SESSION_NAME)
ROBOT_PLAYWRIGHT_CDP_URL = None
bstack1l111l1111_opy_ = False
bstack111l11ll1l_opy_ = None
def set_playwright_globals(**kwargs):
    bstack1ll1lll_opy_ (u"ࠣࠤࠥࡍࡳࡰࡥࡤࡶࠣ࡫ࡱࡵࡢࡢ࡮ࡶࠤ࡫ࡸ࡯࡮ࠢࡢࡣ࡮ࡴࡩࡵࡡࡢ࠲ࡵࡿࠠࡪࡰࡷࡳࠥࡺࡨࡪࡵࠣࡱࡴࡪࡵ࡭ࡧࠪࡷࠥࡴࡡ࡮ࡧࡶࡴࡦࡩࡥ࠯ࠌࠣࠤࠥࠦࡃࡢ࡮࡯ࡩࡩࠦࡢࡺࠢࡢࡣ࡮ࡴࡩࡵࡡࡢ࠲ࡵࡿࠠࡣࡧࡩࡳࡷ࡫ࠠࡱࡣࡷࡧ࡭ࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠫ࠭ࠥࡹ࡯ࠡࡶ࡫ࡥࡹࠦ࡭ࡰࡦࡢࡰࡦࡻ࡮ࡤࡪࠍࠤࠥࠦࠠࡢࡰࡧࠤࡵࡧࡴࡤࡪࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡤࡣࡱࠤࡦࡩࡣࡦࡵࡶࠤࡈࡕࡎࡇࡋࡊ࠰ࠥࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡐࡄࡑࡊ࠲ࠠࡦࡶࡦ࠲ࠧࠨࠢୌ")
    g = globals()
    for key, value in kwargs.items():
        g[key] = value
try:
  try:
    import Browser
    import os
    from subprocess import Popen
    from browserstack_sdk.__init__ import get_turboscale_playwright_url
    from browserstack_sdk.sdk_cli.utils.bstack11lll1ll_opy_ import bstack11l11l1l1l_opy_
    def bstack11ll111111_opy_(self, args, **kwargs):
      global CONFIG
      global SELENIUM_OR_PLAYWRIGHT_INSTALLED
      global ROBOT_PLAYWRIGHT_CDP_URL
      global bstack1l111l1111_opy_
      from browserstack_sdk.__init__ import LAUNCH_PATCH_ROBOT_PLAYWRIGHT
      if(bstack1ll1lll_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸ࠯࡬ࡶ୍ࠦ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"ࠪࢂࠬ୎")), bstack1ll1lll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ୏"), bstack1ll1lll_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧ୐")), bstack1ll1lll_opy_ (u"࠭ࡷࠨ୑")) as fp:
          fp.write(bstack1ll1lll_opy_ (u"ࠢࠣ୒"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1ll1lll_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥ୓")))):
          with open(args[1], bstack1ll1lll_opy_ (u"ࠩࡵࠫ୔")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1ll1lll_opy_ (u"ࠪࡥࡸࡿ࡮ࡤࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࡤࡴࡥࡸࡒࡤ࡫ࡪ࠮ࡣࡰࡰࡷࡩࡽࡺࠬࠡࡲࡤ࡫ࡪࠦ࠽ࠡࡸࡲ࡭ࡩࠦ࠰ࠪࠩ୕") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1ll1l1l1ll_opy_)
            if bstack1ll1lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨୖ") in CONFIG and str(CONFIG[bstack1ll1lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩୗ")]).lower() != bstack1ll1lll_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ୘"):
                cdpUrl = get_turboscale_playwright_url()
                LAUNCH_PATCH_ROBOT_PLAYWRIGHT = bstack1ll1lll_opy_ (u"ࠧࠨࠩࠍ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࠐࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠺ࡣࠠ࠾࠿ࡀࠤࠬࡺࡲࡶࡧࠪ࠿ࠏࡩ࡯࡯ࡵࡷࠤࡧࡹࡴࡢࡥ࡮ࡣࡵࡧࡴࡩࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸ࡣ࠻ࠋࡥࡲࡲࡸࡺࠠࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠲࡟࠾ࠎࡨࡵ࡮ࡴࡶࠣࡴࡤ࡯࡮ࡥࡧࡻࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠲࡞࠽ࠍࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠹ࡣࠠ࠾࠿ࡀࠤࠬࡺࡲࡶࡧࠪ࠿ࠏࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡹ࡬ࡪࡥࡨࠬ࠵࠲ࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠷ࠬ࠿ࠏࡩ࡯࡯ࡵࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬ࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ࠭ࡀࠐࡣࡰࡰࡶࡸࠥࡵࡲࡪࡩ࡬ࡲࡦࡲ࡟ࡤࡪࡵࡳࡲ࡯ࡵ࡮ࡡ࡯ࡥࡺࡴࡣࡩࠢࡀࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡱࡧࡵ࡯ࡥ࡫࠲ࡧ࡯࡮ࡥࠪ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱ࠮ࡤࡪࡵࡳࡲ࡯ࡵ࡮ࠫ࠾ࠎ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡱࡧࡵ࡯ࡥ࡫ࠤࡂࠦࡡࡴࡻࡱࡧࠥ࠮࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸ࠯ࠠ࠾ࡀࠣࡿࢀࠐࠠࠡ࡫ࡩࠤ࠭ࠧࡢࡴࡶࡤࡧࡰࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠬࠤࢀࢁࠊࠡࠢࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣࡳࡷ࡯ࡧࡪࡰࡤࡰࡤࡩࡨࡳࡱࡰ࡭ࡺࡳ࡟࡭ࡣࡸࡲࡨ࡮ࠨ࡭ࡣࡸࡲࡨ࡮ࡏࡱࡶ࡬ࡳࡳࡹࠩ࠼ࠌࠣࠤࢂࢃࠊࠡࠢ࡯ࡩࡹࠦࡣࡢࡲࡶ࠿ࠏࠦࠠࡵࡴࡼࠤࢀࢁࠊࠡࠢࠣࠤࡨࡧࡰࡴࠢࡀࠤࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸ࠯࠻ࠋࠢࠣࢁࢂࠦࡣࡢࡶࡦ࡬ࠥ࠮ࡥࡹࠫࠣࡿࢀࠐࠠࠡࠢࠣࡧࡴࡴࡳࡰ࡮ࡨ࠲ࡪࡸࡲࡰࡴࠫࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷ࠿ࠨࠬࠡࡧࡻ࠭ࡀࠐࠠࠡࡿࢀࠎࠥࠦࡩࡧࠢࠫࡦࡸࡺࡡࡤ࡭ࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠬࠤࢀࢁࠊࠡࠢࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷࡓࡻ࡫ࡲࡄࡆࡓࠬࢀࢁࠊࠡࠢࠣࠤࠥࠦࡥ࡯ࡦࡳࡳ࡮ࡴࡴࡖࡔࡏ࠾ࠥ࠭ࡻࡤࡦࡳ࡙ࡷࡲࡽࠨࠢ࠮ࠤࡪࡴࡣࡰࡦࡨ࡙ࡗࡏࡃࡰ࡯ࡳࡳࡳ࡫࡮ࡵࠪࡍࡗࡔࡔ࠮ࡴࡶࡵ࡭ࡳ࡭ࡩࡧࡻࠫࡧࡦࡶࡳࠪࠫ࠯ࠎࠥࠦࠠࠡࠢࠣ࠲࠳࠴࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸࠐࠠࠡࠢࠣࢁࢂ࠯࠻ࠋࠢࠣࢁࢂࠐࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡣࡺࡥ࡮ࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮ࡤࡱࡱࡲࡪࡩࡴࠩࡽࡾࠎࠥࠦࠠࠡࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸ࠿ࠦࠧࡼࡥࡧࡴ࡚ࡸ࡬ࡾࠩࠣ࠯ࠥ࡫࡮ࡤࡱࡧࡩ࡚ࡘࡉࡄࡱࡰࡴࡴࡴࡥ࡯ࡶࠫࡎࡘࡕࡎ࠯ࡵࡷࡶ࡮ࡴࡧࡪࡨࡼࠬࡨࡧࡰࡴࠫࠬ࠰ࠏࠦࠠࠡࠢ࠱࠲࠳ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷࠏࠦࠠࡾࡿࠬ࠿ࠏࢃࡽ࠼ࠌࡦࡳࡳࡹࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡧࡴࡴ࡮ࡦࡥࡷࠤࡂࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺ࠮ࡣ࡫ࡱࡨ࠭࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠮ࡁࠊࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮ࡤࡱࡱࡲࡪࡩࡴࠡ࠿ࠣࡥࡸࡿ࡮ࡤࠢࠫࡧࡴࡴ࡮ࡦࡥࡷࡓࡵࡺࡩࡰࡰࡶ࠭ࠥࡃ࠾ࠡࡽࡾࠎࠥࠦࡩࡧࠢࠫࠥࡧࡹࡴࡢࡥ࡮ࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠪࠢࡾࡿࠏࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡧࡴࡴ࡮ࡦࡥࡷࠬࡨࡵ࡮࡯ࡧࡦࡸࡔࡶࡴࡪࡱࡱࡷ࠮ࡁࠊࠡࠢࢀࢁࠏࠦࠠ࡭ࡧࡷࠤࡨࡧࡰࡴ࠽ࠍࠤࠥࡺࡲࡺࠢࡾࡿࠏࠦࠠࠡࠢࡦࡥࡵࡹࠠ࠾ࠢࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࡢࡴࡶࡤࡧࡰࡥࡣࡢࡲࡶ࠭ࡀࠐࠠࠡࡿࢀࠤࡨࡧࡴࡤࡪࠣࠬࡪࡾࠩࠡࡽࡾࠎࠥࠦࡽࡾࠌࠣࠤࡨࡵ࡮ࡴࡶࠣࡱࡴࡪࡩࡧ࡫ࡨࡨࡊࡴࡤࡱࡱ࡬ࡲࡹࠦ࠽ࠡࠩࡾࡧࡩࡶࡕࡳ࡮ࢀࠫࠥ࠱ࠠࡦࡰࡦࡳࡩ࡫ࡕࡓࡋࡆࡳࡲࡶ࡯࡯ࡧࡱࡸ࠭ࡐࡓࡐࡐ࠱ࡷࡹࡸࡩ࡯ࡩ࡬ࡪࡾ࠮ࡣࡢࡲࡶ࠭࠮ࡁࠊࠡࠢ࡬ࡪࠥ࠮ࡢࡴࡶࡤࡧࡰࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠯ࠠࡼࡽࠍࠤࠥࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࡏࡷࡧࡵࡇࡉࡖࠨࡼࡽࠍࠤࠥࠦࠠࠡࠢࡨࡲࡩࡶ࡯ࡪࡰࡷ࡙ࡗࡒ࠺ࠡ࡯ࡲࡨ࡮࡬ࡩࡦࡦࡈࡲࡩࡶ࡯ࡪࡰࡷ࠰ࠏࠦࠠࠡࠢࠣࠤ࠳࠴࠮ࡤࡱࡱࡲࡪࡩࡴࡐࡲࡷ࡭ࡴࡴࡳࠋࠢࠣࠤࠥࢃࡽࠪ࠽ࠍࠤࠥࢃࡽࠋࠢࠣࡶࡪࡺࡵࡳࡰࠣࡥࡼࡧࡩࡵࠢࡲࡶ࡮࡭ࡩ࡯ࡣ࡯ࡣࡨࡵ࡮࡯ࡧࡦࡸ࠭ࢁࡻࠋࠢࠣࠤࠥ࠴࠮࠯ࡥࡲࡲࡳ࡫ࡣࡵࡑࡳࡸ࡮ࡵ࡮ࡴ࠮ࠍࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࡅ࡯ࡦࡳࡳ࡮ࡴࡴࠋࠢࠣࢁࢂ࠯࠻ࠋࡿࢀ࠿ࠏ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯ࠋࠩࠪࠫ୙").format(cdpUrl=cdpUrl)
            lines.insert(1, LAUNCH_PATCH_ROBOT_PLAYWRIGHT)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1ll1lll_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥ୚")), bstack1ll1lll_opy_ (u"ࠩࡺࠫ୛")) as bstack11lll11111_opy_:
              bstack11lll11111_opy_.writelines(lines)
        CONFIG[bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬଡ଼")] = str(FRAMEWORK_NAME) + str(__version__)
        bstack111l1ll11l_opy_ = os.environ[bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩଢ଼")]
        bstack11l1ll1l11_opy_ = TestHubUtils.bstack1ll1l1ll1_opy_(CONFIG, FRAMEWORK_NAME)
        CONFIG[bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ୞")] = bstack111l1ll11l_opy_
        CONFIG[bstack1ll1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨୟ")] = bstack11l1ll1l11_opy_
        bstack11111lll_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
        try:
          if PARALLELISE_VANILLA_PYTHON is True:
            bstack11111lll_opy_ = int(multiprocessing.current_process().name)
          elif PARALLELISE_THREADING_PYTHON is True:
            bstack11111lll_opy_ = int(threading.current_thread().name)
        except Exception:
          bstack11111lll_opy_ = 0
        CONFIG[bstack1ll1lll_opy_ (u"ࠢࡶࡵࡨ࡛࠸ࡉࠢୠ")] = False
        CONFIG[bstack1ll1lll_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢୡ")] = True
        bstack1ll111ll1l_opy_ = bstack11l11l1l1l_opy_(bstack11111lll_opy_)
        if bstack1ll111ll1l_opy_ is not None:
          import bstack_utils.constants as _1l11111lll_opy_
          _111llll1l1_opy_ = bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪୢ") if bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫୣ") in bstack1ll111ll1l_opy_ else bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ୤")
          _1111111ll1_opy_ = bstack1ll111ll1l_opy_.get(_111llll1l1_opy_, bstack1ll1lll_opy_ (u"ࠬ࠭୥")).strip().lower()
          _1111ll1ll_opy_ = _1111111ll1_opy_ in _1l11111lll_opy_.bstack1l1l11l1ll_opy_
          if bstack1ll111ll1l_opy_.get(bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ୦")) and not _1111ll1ll_opy_:
            bstack1ll111ll1l_opy_[bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭୧")] = False
            _11l1l1l11_opy_ = [k for k in bstack1ll111ll1l_opy_ if k.startswith(bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ୨"))]
            for k in _11l1l1l11_opy_:
              del bstack1ll111ll1l_opy_[k]
          bstack11lll1lll_opy_ = bstack1ll111ll1l_opy_
          import urllib.parse
          if bstack1ll1lll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭୩") in CONFIG and str(CONFIG[bstack1ll1lll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ୪")]).lower() != bstack1ll1lll_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪ୫"):
            ROBOT_PLAYWRIGHT_CDP_URL = get_turboscale_playwright_url() + urllib.parse.quote(json.dumps(bstack11lll1lll_opy_))
          else:
            ROBOT_PLAYWRIGHT_CDP_URL = bstack1ll1lll_opy_ (u"ࠬࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠧ୬") + urllib.parse.quote(json.dumps(bstack11lll1lll_opy_))
          os.environ[bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡏࡃࡑࡗࡣࡕ࡝࡟ࡄࡆࡓࡣ࡚ࡘࡌࠨ୭")] = ROBOT_PLAYWRIGHT_CDP_URL
          bstack1l111l1111_opy_ = True
          from browserstack_sdk.sdk_cli.bstack111l11ll11_opy_ import bstack11ll11l1_opy_
          from browserstack_sdk.sdk_cli.bstack1l1ll1111l_opy_ import bstack111l111ll_opy_
          instance = next(iter(bstack11ll11l1_opy_.bstack1111l1ll1l_opy_.values()), None)
          if instance:
            bstack111l111ll_opy_.bstack1lll1111ll_opy_(instance, bstack111l111ll_opy_.bstack11l11l11_opy_, bstack1ll111ll1l_opy_)
            bstack111l111ll_opy_.bstack1lll1111ll_opy_(instance, bstack111l111ll_opy_.bstack1lll111l_opy_, ROBOT_PLAYWRIGHT_CDP_URL)
          try:
            from browserstack_sdk.sdk_cli.cli import cli as _11l1l1ll11_opy_
            from browserstack_sdk.sdk_cli.bstack111l11ll11_opy_ import bstack11lll111_opy_, bstack1l11l11l1_opy_
            _11l1l1ll11_opy_.bstack111l11ll11_opy_.bstack1l1lll1l1_opy_(
              None,
              (instance, bstack1ll1lll_opy_ (u"ࠧ࡮ࡱࡧࡣࡵࡵࡰࡦࡰࠪ୮")),
              (bstack11lll111_opy_.bstack1l111ll1l1_opy_, bstack1l11l11l1_opy_.PRE),
              None,
            )
          except Exception as e:
            logger.debug(bstack1ll1lll_opy_ (u"ࠣ࡯ࡲࡨࡤࡶ࡯ࡱࡧࡱ࠾ࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡨ࡬ࡶࡪࠦࡃࡓࡇࡄࡘࡊ࠴ࡐࡓࡇ࠽ࠤࢀࢃࠢ୯").format(e))
          logger.debug(bstack1ll1lll_opy_ (u"ࠤࡰࡳࡩࡥࡰࡰࡲࡨࡲ࠿ࠦࡵࡴ࡫ࡱ࡫ࠥ࡬ࡩ࡯ࡣ࡯ࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠣࡪࡷࡵ࡭ࠡࡆࡵ࡭ࡻ࡫ࡲࡊࡰ࡬ࡸࠧ୰"))
        else:
          bstack11lll1lll_opy_ = get_caps(CONFIG, bstack11111lll_opy_)
          if CONFIG.get(bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧୱ")):
            update_caps_for_local(bstack11lll1lll_opy_)
            bstack11lll1lll_opy_[bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ୲")] = os.environ[bstack1ll1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ୳")]
          logger.debug(bstack1ll1lll_opy_ (u"ࠨ࡭ࡰࡦࡢࡴࡴࡶࡥ࡯࠼ࠣࡈࡷ࡯ࡶࡦࡴࡌࡲ࡮ࡺࠠࡶࡰࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩ࠱ࠦࡦࡢ࡮࡯࡭ࡳ࡭ࠠࡣࡣࡦ࡯ࠥࡺ࡯ࠡࡩࡨࡸࡤࡩࡡࡱࡵࠥ୴"))
        logger.debug(CONFIG_FILE_CONTENT.format(str(bstack11lll1lll_opy_)))
        if bstack1ll1lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ୵") in CONFIG and bstack1ll1lll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭୶") in CONFIG[bstack1ll1lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ୷")][bstack11111lll_opy_]:
          SESSION_NAME = CONFIG[bstack1ll1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭୸")][bstack11111lll_opy_][bstack1ll1lll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ୹")]
        from bstack_utils.helper import bstack1111111l11_opy_
        args.append(bstack1ll1lll_opy_ (u"ࠬࡺࡲࡶࡧࠪ୺") if bstack1111111l11_opy_(CONFIG) else bstack1ll1lll_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ୻"))
        args.append(str(bstack11lll1lll_opy_.get(bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭୼"), False)).lower())
        args.append(os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"ࠨࢀࠪ୽")), bstack1ll1lll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ୾"), bstack1ll1lll_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬ୿")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack11lll1lll_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1ll1lll_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨ஀"))
      SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
      return bstack1ll11ll1l1_opy_(self, args, **kwargs)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack11l11l1ll_opy_(self,
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
    CONFIG[bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ஁")] = str(FRAMEWORK_NAME) + str(__version__)
    bstack111l1ll11l_opy_ = os.environ[bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫஂ")]
    bstack11l1ll1l11_opy_ = TestHubUtils.bstack1ll1l1ll1_opy_(CONFIG, FRAMEWORK_NAME)
    CONFIG[bstack1ll1lll_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪஃ")] = bstack111l1ll11l_opy_
    CONFIG[bstack1ll1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ஄")] = bstack11l1ll1l11_opy_
    bstack11111lll_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
    try:
      if PARALLELISE_VANILLA_PYTHON is True:
        bstack11111lll_opy_ = int(multiprocessing.current_process().name)
      elif PARALLELISE_THREADING_PYTHON is True:
        bstack11111lll_opy_ = int(threading.current_thread().name)
    except Exception:
      bstack11111lll_opy_ = 0
    CONFIG[bstack1ll1lll_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣஅ")] = True
    bstack11l1l11lll_opy_ = get_caps(CONFIG, bstack11111lll_opy_)
    bstack1l1ll11l1l_opy_ = bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫஆ") if bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬஇ") in bstack11l1l11lll_opy_ else bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪஈ")
    bstack1l1111ll1_opy_ = False
    try:
        from bstack_utils import accessibility as a11y
        import bstack_utils.constants as bstack111l1l1ll1_opy_
        bstack11l1l1111_opy_ = bstack11l1l11lll_opy_.get(bstack1l1ll11l1l_opy_, bstack1ll1lll_opy_ (u"࠭ࠧஉ")).strip().lower()
        browser_version = str(bstack11l1l11lll_opy_.get(bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩஊ"), bstack11l1l11lll_opy_.get(bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ஋"), bstack1ll1lll_opy_ (u"ࠩࠪ஌")))).strip()
        bstack111111l111_opy_ = bstack11l1l1111_opy_ in bstack111l1l1ll1_opy_.bstack1l1l11l1ll_opy_
        min_version = bstack111l1l1ll1_opy_.MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION
        if not browser_version or browser_version.lower().startswith(bstack1ll1lll_opy_ (u"ࠪࡰࡦࡺࡥࡴࡶࠪ஍")):
            bstack11llllll_opy_ = True
        else:
            major = browser_version.split(bstack1ll1lll_opy_ (u"ࠫ࠳࠭எ"))[0]
            bstack11llllll_opy_ = major.isdigit() and int(major) > min_version
        if not bstack11llllll_opy_:
            logger.warning(bstack1ll1lll_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡨࡴࡨࡥࡹ࡫ࡲࠡࡶ࡫ࡥࡳࠦࡻࡾ࠰ࠣࡇࡺࡸࡲࡦࡰࡷࠤࡻ࡫ࡲࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠤஏ").format(min_version, browser_version))
        if a11y.is_enabled_platform(CONFIG, bstack11111lll_opy_) and bstack111111l111_opy_ and bstack11llllll_opy_ and a11y.is_platform_supported(bstack11l1l11lll_opy_, options=None, config=CONFIG):
            bstack1l1111ll1_opy_ = True
            import browserstack_sdk
            browserstack_sdk.CONFIG[bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬஐ")] = True
            bstack11l1l11lll_opy_[bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭஑")] = True
            if CONFIG.get(bstack1ll1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪஒ")):
                bstack11l1l11lll_opy_[bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪஓ")] = CONFIG[bstack1ll1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬஔ")]
            import json as _json
            bstack1l11l1l1l1_opy_ = os.getenv(bstack1ll1lll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩக"))
            bstack11111l1ll_opy_ = bstack11l1l11lll_opy_.get(bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶ࠲ࡦࡻࡴࡩࡖࡲ࡯ࡪࡴࠧ஖"))
            if not bstack1l11l1l1l1_opy_ and bstack11111l1ll_opy_:
                os.environ[bstack1ll1lll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ஗")] = bstack11111l1ll_opy_
                bstack1l11l1l1l1_opy_ = bstack11111l1ll_opy_
            if bstack1l11l1l1l1_opy_:
                bstack11l1l11lll_opy_[bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠴ࡡࡶࡶ࡫ࡘࡴࡱࡥ࡯ࠩ஘")] = bstack1l11l1l1l1_opy_
            bstack11111l11_opy_ = _json.loads(os.getenv(bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩங"), bstack1ll1lll_opy_ (u"ࠩࡾࢁࠬச"))).get(bstack1ll1lll_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ஛"))
            if bstack11111l11_opy_:
                bstack11l1l11lll_opy_[bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵ࠱ࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫஜ")] = bstack11111l11_opy_
            bstack11l1l11lll_opy_.pop(bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ஝"), None)
            bstack11l1l11lll_opy_.pop(bstack1ll1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ஞ"), None)
            bstack11l1l11lll_opy_.pop(bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧட"), None)
            logger.debug(bstack1ll1lll_opy_ (u"ࠣࡃ࠴࠵ࡾࠦࡥ࡯ࡣࡥࡰࡪࡪࠠࡧࡱࡵࠤࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࠫࡿࢂࠦࡻࡾࠫࠥ஠").format(
                bstack11l1l1111_opy_, browser_version))
    except Exception as e:
        bstack1l1111ll1_opy_ = False
        logger.debug(bstack1ll1lll_opy_ (u"ࠤࡄ࠵࠶ࡿࠠࡥࡧࡷࡩࡨࡺࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࢀࢃࠢ஡").format(str(e)))
    logger.debug(CONFIG_FILE_CONTENT.format(str(bstack11l1l11lll_opy_)))
    if CONFIG.get(bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ஢")):
      update_caps_for_local(bstack11l1l11lll_opy_)
    if bstack1ll1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧண") in CONFIG and bstack1ll1lll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪத") in CONFIG[bstack1ll1lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ஥")][bstack11111lll_opy_]:
      SESSION_NAME = CONFIG[bstack1ll1lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ஦")][bstack11111lll_opy_][bstack1ll1lll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭஧")]
    import urllib
    import json
    if bstack1ll1lll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ந") in CONFIG and str(CONFIG[bstack1ll1lll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧன")]).lower() != bstack1ll1lll_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪப"):
        bstack1ll1lll1l1_opy_ = get_turboscale_playwright_url()
        cdpUrl = bstack1ll1lll1l1_opy_ + urllib.parse.quote(json.dumps(bstack11l1l11lll_opy_))
    else:
        cdpUrl = bstack1ll1lll_opy_ (u"ࠬࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠧ஫") + urllib.parse.quote(json.dumps(bstack11l1l11lll_opy_))
    try:
        from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
        PlaywrightDriverWrapperDirect.setup_dispatch_capture()
    except Exception as exc:
        logger.debug(bstack1ll1lll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰࠡࡦ࡬ࡷࡵࡧࡴࡤࡪࠣࡧࡦࡶࡴࡶࡴࡨࠤ࡫ࡵࡲࠡࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨ࠿ࠦࠥࡴࠤ஬"), exc)
    if bstack1l1111ll1_opy_:
        browser = self.connect_over_cdp(cdpUrl)
    else:
        browser = bstack111l11ll1l_opy_(self, cdpUrl)
    try:
        from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
        wrapper = PlaywrightDriverWrapperDirect(browser, page=None, capabilities=bstack11l1l11lll_opy_, config=CONFIG)
        threading.current_thread().bstackSessionDriver = wrapper
        logger.debug(bstack1ll1lll_opy_ (u"ࠢࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡈࡷ࡯ࡶࡦࡴ࡚ࡶࡦࡶࡰࡦࡴࡇ࡭ࡷ࡫ࡣࡵࠢࡶࡩࡹࡻࡰࠡࡥࡲࡱࡵࡲࡥࡵࡧࠣࡪࡴࡸࠠࡵࡪࡵࡩࡦࡪࠠࠦࡵࠥ஭"), threading.get_ident())
        threading.current_thread().bstackTestErrorMessages = []
        if bstack1l1111ll1_opy_:
            threading.current_thread().a11yPlatform = True
            wrapper.bstackA11yShouldScan = True
        if wrapper.session_id and not wrapper._cbt_info_sent:
            PlaywrightDriverWrapperDirect._send_cbt_info_on_session()
        try:
            from playwright.sync_api import Browser as bstack1l1llll1l_opy_
            if not hasattr(bstack1l1llll1l_opy_, bstack1ll1lll_opy_ (u"ࠨࡡࡥࡷࡹࡧࡣ࡬ࡡࡱࡩࡼࡥࡰࡢࡩࡨࡣࡵࡧࡴࡤࡪࡨࡨࠬம")):
                _111l1lll1_opy_ = bstack1l1llll1l_opy_.new_page
                def _1ll111llll_opy_(bstack111ll1l1l1_opy_, *bstack1l111l111l_opy_, **bstack11lll11l_opy_):
                    if getattr(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨய"), None):
                        try:
                            bstack11l111l11_opy_ = bstack111ll1l1l1_opy_.contexts[0] if bstack111ll1l1l1_opy_.contexts else None
                            if bstack11l111l11_opy_ and bstack11l111l11_opy_.pages:
                                page = None
                                for _1l111lll_opy_ in bstack11l111l11_opy_.pages:
                                    if bstack1ll1lll_opy_ (u"ࠥࡥࡧࡵࡵࡵ࠼ࡥࡰࡦࡴ࡫ࠣர") in _1l111lll_opy_.url:
                                        page = _1l111lll_opy_
                                        logger.debug(bstack1ll1lll_opy_ (u"ࠦࡆ࠷࠱ࡺ࠼ࠣࡶࡪࡻࡳࡪࡰࡪࠤࡦࡨ࡯ࡶࡶ࠽ࡦࡱࡧ࡮࡬ࠢࡳࡥ࡬࡫ࠠࡧࡴࡲࡱࠥࡪࡥࡧࡣࡸࡰࡹࠦࡣࡰࡰࡷࡩࡽࡺࠢற"))
                                        break
                                if page is None:
                                    page = bstack11l111l11_opy_.new_page(*bstack1l111l111l_opy_, **bstack11lll11l_opy_)
                                    logger.debug(bstack1ll1lll_opy_ (u"ࠧࡇ࠱࠲ࡻ࠽ࠤࡳࡵࠠࡣ࡮ࡤࡲࡰࠦࡰࡢࡩࡨࠤ࡫ࡵࡵ࡯ࡦ࠯ࠤࡨࡸࡥࡢࡶࡨࡨࠥࡴࡥࡸࠢࡳࡥ࡬࡫ࠠࡪࡰࠣࡨࡪ࡬ࡡࡶ࡮ࡷࠤࡨࡵ࡮ࡵࡧࡻࡸࠧல"))
                            elif bstack11l111l11_opy_:
                                page = bstack11l111l11_opy_.new_page(*bstack1l111l111l_opy_, **bstack11lll11l_opy_)
                                logger.debug(bstack1ll1lll_opy_ (u"ࠨࡁ࠲࠳ࡼ࠾ࠥࡩࡲࡦࡣࡷࡩࡩࠦ࡮ࡦࡹࠣࡴࡦ࡭ࡥࠡ࡫ࡱࠤࡩ࡫ࡦࡢࡷ࡯ࡸࠥࡩ࡯࡯ࡶࡨࡼࡹࠨள"))
                            else:
                                page = _111l1lll1_opy_(bstack111ll1l1l1_opy_, *bstack1l111l111l_opy_, **bstack11lll11l_opy_)
                                logger.debug(bstack1ll1lll_opy_ (u"ࠢࡂ࠳࠴ࡽ࠿ࠦ࡮ࡰࠢࡧࡩ࡫ࡧࡵ࡭ࡶࠣࡧࡴࡴࡴࡦࡺࡷ࠰ࠥ࡬ࡡ࡭࡮࡬ࡲ࡬ࠦࡢࡢࡥ࡮ࠤࡹࡵࠠ࡯ࡧࡺࡣࡵࡧࡧࡦࠪࠬࠦழ"))
                        except Exception as bstack1111l111l1_opy_:
                            logger.debug(bstack1ll1lll_opy_ (u"ࠣࡃ࠴࠵ࡾࡀࠠࡥࡧࡩࡥࡺࡲࡴࠡࡥࡲࡲࡹ࡫ࡸࡵࠢࡳࡥ࡬࡫ࠠࡳࡧࡸࡷࡪࠦࡦࡢ࡫࡯ࡩࡩࠦࠨࠦࡵࠬ࠰ࠥ࡬ࡡ࡭࡮࡬ࡲ࡬ࠦࡢࡢࡥ࡮ࠦவ"), bstack1111l111l1_opy_)
                            page = _111l1lll1_opy_(bstack111ll1l1l1_opy_, *bstack1l111l111l_opy_, **bstack11lll11l_opy_)
                    else:
                        page = _111l1lll1_opy_(bstack111ll1l1l1_opy_, *bstack1l111l111l_opy_, **bstack11lll11l_opy_)
                    try:
                        _w = getattr(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨஶ"), None)
                        if _w and hasattr(_w, bstack1ll1lll_opy_ (u"ࠪࡹࡵࡪࡡࡵࡧࡢࡴࡦ࡭ࡥࠨஷ")):
                            _w.update_page(page)
                        if _w and not _w.session_id:
                            try:
                                import json as _json
                                result = page.evaluate(
                                    bstack1ll1lll_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧஸ"), bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧ࡭ࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡆࡨࡸࡦ࡯࡬ࡴࠤࢀࠫஹ"))
                                if isinstance(result, str):
                                    result = _json.loads(result)
                                if isinstance(result, dict):
                                    sid = result.get(bstack1ll1lll_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ஺")) or result.get(bstack1ll1lll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠫ஻")) or result.get(bstack1ll1lll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡋࡧࠫ஼"))
                                    if sid:
                                        import threading as _1l1111111_opy_
                                        from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
                                        with PlaywrightDriverWrapperDirect._session_ids_lock:
                                            PlaywrightDriverWrapperDirect._session_ids[_1l1111111_opy_.get_ident()] = sid
                                        logger.debug(bstack1ll1lll_opy_ (u"ࠤࡆࡥࡵࡺࡵࡳࡧࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠡࡸ࡬ࡥࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠦࡵࠥ஽"), sid)
                                        PlaywrightDriverWrapperDirect._send_cbt_info_on_session()
                                    else:
                                        logger.debug(bstack1ll1lll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵࠤ࡬࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡧࡷࡥ࡮ࡲࡳࠡࡴࡨࡸࡺࡸ࡮ࡦࡦࠣࡲࡴࠦࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦ࠽ࠤࠪࡹࠢா"), result)
                                else:
                                    logger.debug(bstack1ll1lll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠥ࡭ࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡆࡨࡸࡦ࡯࡬ࡴࠢࡵࡩࡸࡻ࡬ࡵ࠼ࠣࠩࡸࠨி"), result)
                            except Exception as _1ll11l11l_opy_:
                                logger.debug(bstack1ll1lll_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠢࡩࡥࡱࡲࡢࡢࡥ࡮ࠤࡻ࡯ࡡࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࠩࡸࠨீ"), _1ll11l11l_opy_)
                        if (getattr(threading.current_thread(), bstack1ll1lll_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬு"), None)
                                and not getattr(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠧࡢ࠳࠴ࡽࡤࡹࡴࡢࡴࡷࡩࡩ࠭ூ"), False)):
                            threading.current_thread().a11y_started = True
                            try:
                                from bstack_utils import accessibility as _11l1lll111_opy_
                                bstack11111lll11_opy_ = getattr(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬ௃"), True)
                                _11l1lll111_opy_.start_test_capture(_w, bstack11111lll11_opy_)
                            except Exception:
                                logger.debug(bstack1ll1lll_opy_ (u"ࠤࡇࡩ࡫࡫ࡲࡳࡧࡧࠤࡆ࠷࠱ࡺࠢࡶࡸࡦࡸࡴࡠࡶࡨࡷࡹࡥࡣࡢࡲࡷࡹࡷ࡫ࠠࡧࡣ࡬ࡰࡪࡪࠢ௄"))
                    except Exception as exc:
                        logger.debug(bstack1ll1lll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡵࡱࡦࡤࡸࡪࠦࡰࡢࡩࡨࠤ࡮ࡴࠠࡸࡴࡤࡴࡵ࡫ࡲ࠻ࠢࠨࡷࠧ௅"), exc)
                    return page
                bstack1l1llll1l_opy_.new_page = _1ll111llll_opy_
                bstack1l1llll1l_opy_._bstack_new_page_patched = True
        except Exception as exc:
            logger.debug(bstack1ll1lll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡷࡧ࡭ࠦࡓࡺࡰࡦࡆࡷࡵࡷࡴࡧࡵ࠲ࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠦࡦࡰࡴࠣࡴࡦ࡭ࡥࠡࡥࡤࡴࡹࡻࡲࡦ࠼ࠣࠩࡸࠨெ"), exc)
        try:
            from playwright.sync_api import Page as bstack11l1l111l1_opy_, Browser as _1ll1ll1ll1_opy_
            if not hasattr(bstack11l1l111l1_opy_, bstack1ll1lll_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥࡰࡢࡩࡨࡣࡨࡲ࡯ࡴࡧࡢࡴࡦࡺࡣࡩࡧࡧࠫே")):
                _1l1l1ll1_opy_ = bstack11l1l111l1_opy_.close
                def _11111l1l11_opy_(bstack11l1l11ll1_opy_, *bstack11l1111l11_opy_, _bstack_sdk_close=False, **bstack11l1l1l1_opy_):
                    if not _bstack_sdk_close:
                        logger.debug(bstack1ll1lll_opy_ (u"ࠨࡄࡦࡨࡨࡶࡷ࡫ࡤࠡࡲࡤ࡫ࡪ࠴ࡣ࡭ࡱࡶࡩ࠭࠯ࠠ⠕ࠢࡺ࡭ࡱࡲࠠࡤ࡮ࡲࡷࡪࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥை"))
                        threading.current_thread().bstack_deferred_page_close = True
                        threading.current_thread().bstack_deferred_page_ref = bstack11l1l11ll1_opy_
                        return
                    return _1l1l1ll1_opy_(bstack11l1l11ll1_opy_, *bstack11l1111l11_opy_, **bstack11l1l1l1_opy_)
                bstack11l1l111l1_opy_.close = _11111l1l11_opy_
                bstack11l1l111l1_opy_._bstack_page_close_patched = True
            if not hasattr(_1ll1ll1ll1_opy_, bstack1ll1lll_opy_ (u"ࠧࡠࡤࡶࡸࡦࡩ࡫ࡠࡤࡵࡳࡼࡹࡥࡳࡡࡦࡰࡴࡹࡥࡠࡲࡤࡸࡨ࡮ࡥࡥࠩ௉")):
                _1l1l11l1l_opy_ = _1ll1ll1ll1_opy_.close
                def _1111l1lll_opy_(bstack111ll1l1l1_opy_, *bstack1l11l1ll1l_opy_, _bstack_sdk_close=False, **bstack111l111l1_opy_):
                    if not _bstack_sdk_close:
                        logger.debug(bstack1ll1lll_opy_ (u"ࠣࡆࡨࡪࡪࡸࡲࡦࡦࠣࡦࡷࡵࡷࡴࡧࡵ࠲ࡨࡲ࡯ࡴࡧࠫ࠭ࠥ⠚ࠠࡸ࡫࡯ࡰࠥࡩ࡬ࡰࡵࡨࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣொ"))
                        threading.current_thread().bstack_deferred_browser_close = True
                        threading.current_thread().bstack_deferred_browser_ref = bstack111ll1l1l1_opy_
                        return
                    return _1l1l11l1l_opy_(bstack111ll1l1l1_opy_, *bstack1l11l1ll1l_opy_, **bstack111l111l1_opy_)
                _1ll1ll1ll1_opy_.close = _1111l1lll_opy_
                _1ll1ll1ll1_opy_._bstack_browser_close_patched = True
            if not hasattr(bstack11l1l111l1_opy_, bstack1ll1lll_opy_ (u"ࠩࡢࡦࡸࡺࡡࡤ࡭ࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺ࡟ࡱࡣࡷࡧ࡭࡫ࡤࠨோ")):
                _1l1ll1l1l_opy_ = bstack11l1l111l1_opy_.screenshot
                def _1ll1l11l11_opy_(bstack11l1l11ll1_opy_, *bstack11l11l11l_opy_, **bstack111l1l1ll_opy_):
                    result = _1l1ll1l1l_opy_(bstack11l1l11ll1_opy_, *bstack11l11l11l_opy_, **bstack111l1l1ll_opy_)
                    try:
                        from bstack_utils.testhub_handler import TestHubHandler
                        from bstack_utils.bstack1l11111l1_opy_ import bstack11llll1l_opy_
                        if bstack11llll1l_opy_.on():
                            import base64
                            if isinstance(result, bytes):
                                bstack11ll1lllll_opy_ = base64.b64encode(result).decode(bstack1ll1lll_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩௌ"))
                            else:
                                bstack11ll1lllll_opy_ = str(result)
                            test_uuid = TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack11llll1l_opy_.current_hook_uuid()
                            if test_uuid and bstack11ll1lllll_opy_:
                                TestHubHandler.bstack1111ll1lll_opy_({
                                    bstack1ll1lll_opy_ (u"ࠫ࡮ࡳࡡࡨࡧ்ࠪ"): bstack11ll1lllll_opy_,
                                    bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ௎"): test_uuid
                                })
                                logger.debug(bstack1ll1lll_opy_ (u"ࠨࡓࡦࡰࡷࠤࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠥࡺ࡯ࠡࡑ࠴࠵ࡾࠦࡦࡰࡴࠣࡸࡪࡹࡴࠡࡽࢀࠦ௏").format(test_uuid))
                    except Exception as bstack1lll11111_opy_:
                        logger.debug(bstack1ll1lll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡴࡤࠡࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠢࡷࡳࠥࡕ࠱࠲ࡻ࠽ࠤࢀࢃࠢௐ").format(str(bstack1lll11111_opy_)))
                    return result
                bstack11l1l111l1_opy_.screenshot = _1ll1l11l11_opy_
                bstack11l1l111l1_opy_._bstack_screenshot_patched = True
        except Exception as exc:
            logger.debug(bstack1ll1lll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷ࡫ࠠࡥࡧࡩࡩࡷࡸࡥࡥࠢࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡣ࡭ࡱࡶࡩࠥ࡮࡯ࡰ࡭ࡶ࠾ࠥࠫࡳࠣ௑"), exc)
        logger.debug(bstack1ll1lll_opy_ (u"ࠤࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡊࡲࡪࡸࡨࡶ࡜ࡸࡡࡱࡲࡨࡶࡉ࡯ࡲࡦࡥࡷࠤࡸ࡫ࡴࡶࡲࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࠥ࡬࡯ࡳࠢࡷ࡬ࡷ࡫ࡡࡥࠢࡾࢁࠧ௒").format(threading.get_ident()))
    except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࡸࡴࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡺࡶࡦࡶࡰࡦࡴ࠽ࠤࢀࢃࠢ௓").format(str(e)))
    return browser
  async def bstack1llll11lll_opy_(self, *args, **kwargs):
    global bstack111l11ll1l_opy_, CONFIG, FRAMEWORK_NAME, __version__, BROWSERSTACK_AUTOMATION
    global PLATFORM_INDEX, PARALLELISE_VANILLA_PYTHON, PARALLELISE_THREADING_PYTHON, SESSION_NAME
    import urllib.parse as _1l1ll1lll_opy_
    import json
    ws_endpoint = args[0] if args else kwargs.get(bstack1ll1lll_opy_ (u"ࠫࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴࠨ௔"), kwargs.get(bstack1ll1lll_opy_ (u"ࠬࡽࡳࡠࡧࡱࡨࡵࡵࡩ࡯ࡶࠪ௕"), bstack1ll1lll_opy_ (u"࠭ࠧ௖")))
    bstack111ll1111l_opy_ = (ws_endpoint
                 and bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪௗ") in str(ws_endpoint)
                 and bstack1ll1lll_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧ௘") in str(ws_endpoint))
    bstack1llll1lll1_opy_ = {}
    if bstack111ll1111l_opy_:
        from bstack_utils.helper import bstack11lll11l1_opy_
        bstack1lll11lll1_opy_ = bstack11lll11l1_opy_()
        try:
            if bstack1lll11lll1_opy_:
                CONFIG[bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ௙")] = str(FRAMEWORK_NAME) + str(__version__)
                bstack111l1ll11l_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ௚"), bstack1ll1lll_opy_ (u"ࠫࠬ௛"))
                if bstack111l1ll11l_opy_:
                    CONFIG[bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ௜")] = bstack111l1ll11l_opy_
                CONFIG[bstack1ll1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨ௝")] = TestHubUtils.bstack1ll1l1ll1_opy_(CONFIG, FRAMEWORK_NAME)
                bstack11111lll_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
                try:
                    if PARALLELISE_VANILLA_PYTHON is True:
                        bstack11111lll_opy_ = int(multiprocessing.current_process().name)
                    elif PARALLELISE_THREADING_PYTHON is True:
                        bstack11111lll_opy_ = int(threading.current_thread().name)
                except Exception:
                    bstack11111lll_opy_ = 0
                CONFIG[bstack1ll1lll_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ௞")] = True
                bstack1llll1lll1_opy_ = get_caps(CONFIG, bstack11111lll_opy_)
                if CONFIG.get(bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ௟")):
                    update_caps_for_local(bstack1llll1lll1_opy_)
                if bstack1ll1lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ௠") in CONFIG and bstack1ll1lll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ௡") in CONFIG[bstack1ll1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ௢")][bstack11111lll_opy_]:
                    SESSION_NAME = CONFIG[bstack1ll1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ௣")][bstack11111lll_opy_][bstack1ll1lll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ௤")]
                logger.debug(bstack1ll1lll_opy_ (u"ࠢࡄࡣࡶࡩࠥࡇ࠺ࠡࡔࡨࡴࡱࡧࡣࡦࡦࠣࡹࡸ࡫ࡲࠡࡥࡤࡴࡸࠦࡷࡪࡶ࡫ࠤࡾࡳ࡬ࠡࡥࡤࡴࡸࡀࠠࡼࡿࠥ௥").format(str(bstack1llll1lll1_opy_)))
            else:
                bstack1ll1l1l111_opy_ = str(ws_endpoint).split(bstack1ll1lll_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧ௦"))[1]
                bstack1llll1lll1_opy_ = json.loads(_1l1ll1lll_opy_.unquote(bstack1ll1l1l111_opy_))
                bstack1llll1lll1_opy_ = bstack1llll1lll1_opy_ or {}
                bstack111l1ll11l_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ௧"), bstack1ll1lll_opy_ (u"ࠪࠫ௨"))
                bstack11l1ll1l11_opy_ = TestHubUtils.bstack1ll1l1ll1_opy_(CONFIG, FRAMEWORK_NAME)
                bstack1llll1lll1_opy_[bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ௩")] = str(FRAMEWORK_NAME) + str(__version__)
                bstack1llll1lll1_opy_[bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭௪")] = BROWSERSTACK_AUTOMATION
                if bstack111l1ll11l_opy_:
                    bstack1llll1lll1_opy_[bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ௫")] = bstack111l1ll11l_opy_
                bstack1llll1lll1_opy_[bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨ௬")] = bstack11l1ll1l11_opy_
                logger.debug(bstack1ll1lll_opy_ (u"ࠣࡅࡤࡷࡪࠦࡄ࠻ࠢࡐࡩࡷ࡭ࡥࡥࠢࡖࡈࡐࠦࡴࡦ࡮ࡨࡱࡪࡺࡲࡺࠢ࡬ࡲࡹࡵࠠࡶࡵࡨࡶࠥࡩࡡࡱࡵࠥ௭"))
            ws_url = str(ws_endpoint).split(bstack1ll1lll_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨ௮"))[0]
            ws_endpoint = ws_url + bstack1ll1lll_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩ௯") + _1l1ll1lll_opy_.quote(json.dumps(bstack1llll1lll1_opy_))
            if args:
                args = (ws_endpoint,) + args[1:]
            else:
                if bstack1ll1lll_opy_ (u"ࠫࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴࠨ௰") in kwargs:
                    kwargs[bstack1ll1lll_opy_ (u"ࠬࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵࠩ௱")] = ws_endpoint
                else:
                    kwargs[bstack1ll1lll_opy_ (u"࠭ࡷࡴࡡࡨࡲࡩࡶ࡯ࡪࡰࡷࠫ௲")] = ws_endpoint
            logger.debug(bstack1ll1lll_opy_ (u"ࠢࡍࡧࡪࡥࡨࡿࠠࡤࡱࡱࡲࡪࡩࡴࠡࡗࡕࡐࠥࡻࡰࡥࡣࡷࡩࡩࠦࡷࡪࡶ࡫ࠤࢀࢃࠠࡤࡣࡳࡷࠧ௳").format(bstack1ll1lll_opy_ (u"ࠣࡻࡰࡰࠧ௴") if bstack1lll11lll1_opy_ else bstack1ll1lll_opy_ (u"ࠤࡷࡩࡱ࡫࡭ࡦࡶࡵࡽࠧ௵")))
        except Exception as e:
            logger.debug(bstack1ll1lll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡦࡴࡪࡩࠥࡩࡡࡱࡵࠣ࡭ࡳࡺ࡯ࠡࡥࡲࡲࡳ࡫ࡣࡵࠢࡘࡖࡑࡀࠠࡼࡿࠥ௶").format(str(e)))
        try:
            from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
            PlaywrightDriverWrapperDirect.setup_dispatch_capture()
        except Exception as exc:
            logger.debug(bstack1ll1lll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦࡤࡪࡵࡳࡥࡹࡩࡨࠡࡥࡤࡴࡹࡻࡲࡦࠢ࡬ࡲࠥࡳ࡯ࡥࡡࡦࡳࡳࡴࡥࡤࡶ࠽ࠤࠪࡹࠢ௷"), exc)
    browser = await bstack111l11ll1l_opy_(self, *args, **kwargs)
    if bstack111ll1111l_opy_:
        try:
            from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
            wrapper = PlaywrightDriverWrapperDirect(browser, page=None, capabilities=bstack1llll1lll1_opy_, config=CONFIG)
            threading.current_thread().bstackSessionDriver = wrapper
            logger.debug(bstack1ll1lll_opy_ (u"ࠧࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡆࡵ࡭ࡻ࡫ࡲࡘࡴࡤࡴࡵ࡫ࡲࡅ࡫ࡵࡩࡨࡺࠠࡴࡧࡷࡹࡵࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࠡࡨࡲࡶࠥࡺࡨࡳࡧࡤࡨࠥࠫࡳࠣ௸"), threading.get_ident())
            threading.current_thread().bstackTestErrorMessages = []
            if wrapper.session_id and not wrapper._cbt_info_sent:
                PlaywrightDriverWrapperDirect._send_cbt_info_on_session()
            try:
                from playwright.sync_api import Browser as bstack1l1llll1l_opy_
                if not hasattr(bstack1l1llll1l_opy_, bstack1ll1lll_opy_ (u"࠭࡟ࡣࡵࡷࡥࡨࡱ࡟࡯ࡧࡺࡣࡵࡧࡧࡦࡡࡳࡥࡹࡩࡨࡦࡦࠪ௹")):
                    _111l1lll1_opy_ = bstack1l1llll1l_opy_.new_page
                    def _1ll111llll_opy_(bstack111ll1l1l1_opy_, *bstack1l111l111l_opy_, **bstack11lll11l_opy_):
                        page = _111l1lll1_opy_(bstack111ll1l1l1_opy_, *bstack1l111l111l_opy_, **bstack11lll11l_opy_)
                        try:
                            _w = getattr(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭௺"), None)
                            if _w and hasattr(_w, bstack1ll1lll_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡠࡲࡤ࡫ࡪ࠭௻")):
                                _w.update_page(page)
                        except Exception as exc:
                            logger.debug(bstack1ll1lll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡻࡰࡥࡣࡷࡩࠥࡶࡡࡨࡧࠣ࡭ࡳࠦࡷࡳࡣࡳࡴࡪࡸࠠࠩ࡯ࡲࡨࡤࡩ࡯࡯ࡰࡨࡧࡹ࠯࠺ࠡࠧࡶࠦ௼"), exc)
                        return page
                    bstack1l1llll1l_opy_.new_page = _1ll111llll_opy_
                    bstack1l1llll1l_opy_._bstack_new_page_patched = True
            except Exception as exc:
                logger.debug(bstack1ll1lll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡶࡦ࡬࡙ࠥࡹ࡯ࡥࡅࡶࡴࡽࡳࡦࡴ࠱ࡲࡪࡽ࡟ࡱࡣࡪࡩࠥ࡯࡮ࠡ࡯ࡲࡨࡤࡩ࡯࡯ࡰࡨࡧࡹࡀࠠࠦࡵࠥ௽"), exc)
            try:
                from playwright.sync_api import Page as bstack11l1l111l1_opy_, Browser as _1ll1ll1ll1_opy_
                if not hasattr(bstack11l1l111l1_opy_, bstack1ll1lll_opy_ (u"ࠫࡤࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡨࡧࡢࡧࡱࡵࡳࡦࡡࡳࡥࡹࡩࡨࡦࡦࠪ௾")):
                    _1l1l1ll1_opy_ = bstack11l1l111l1_opy_.close
                    def _11111l1l11_opy_(bstack11l1l11ll1_opy_, *bstack11l1111l11_opy_, _bstack_sdk_close=False, **bstack11l1l1l1_opy_):
                        if not _bstack_sdk_close:
                            logger.debug(bstack1ll1lll_opy_ (u"ࠧࡊࡥࡧࡧࡵࡶࡪࡪࠠࡱࡣࡪࡩ࠳ࡩ࡬ࡰࡵࡨࠬ࠮ࠦ⠔ࠡࡹ࡬ࡰࡱࠦࡣ࡭ࡱࡶࡩࠥ࡯࡮ࠡࡣࡩࡸࡪࡸ࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤ௿"))
                            threading.current_thread().bstack_deferred_page_close = True
                            threading.current_thread().bstack_deferred_page_ref = bstack11l1l11ll1_opy_
                            return
                        return _1l1l1ll1_opy_(bstack11l1l11ll1_opy_, *bstack11l1111l11_opy_, **bstack11l1l1l1_opy_)
                    bstack11l1l111l1_opy_.close = _11111l1l11_opy_
                    bstack11l1l111l1_opy_._bstack_page_close_patched = True
                if not hasattr(_1ll1ll1ll1_opy_, bstack1ll1lll_opy_ (u"࠭࡟ࡣࡵࡷࡥࡨࡱ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡠࡥ࡯ࡳࡸ࡫࡟ࡱࡣࡷࡧ࡭࡫ࡤࠨఀ")):
                    _1l1l11l1l_opy_ = _1ll1ll1ll1_opy_.close
                    def _1111l1lll_opy_(bstack111ll1l1l1_opy_, *bstack1l11l1ll1l_opy_, _bstack_sdk_close=False, **bstack111l111l1_opy_):
                        if not _bstack_sdk_close:
                            logger.debug(bstack1ll1lll_opy_ (u"ࠢࡅࡧࡩࡩࡷࡸࡥࡥࠢࡥࡶࡴࡽࡳࡦࡴ࠱ࡧࡱࡵࡳࡦࠪࠬࠤ⠙ࠦࡷࡪ࡮࡯ࠤࡨࡲ࡯ࡴࡧࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢఁ"))
                            threading.current_thread().bstack_deferred_browser_close = True
                            threading.current_thread().bstack_deferred_browser_ref = bstack111ll1l1l1_opy_
                            return
                        return _1l1l11l1l_opy_(bstack111ll1l1l1_opy_, *bstack1l11l1ll1l_opy_, **bstack111l111l1_opy_)
                    _1ll1ll1ll1_opy_.close = _1111l1lll_opy_
                    _1ll1ll1ll1_opy_._bstack_browser_close_patched = True
                if not hasattr(bstack11l1l111l1_opy_, bstack1ll1lll_opy_ (u"ࠨࡡࡥࡷࡹࡧࡣ࡬ࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡥࡰࡢࡶࡦ࡬ࡪࡪࠧం")):
                    _1l1ll1l1l_opy_ = bstack11l1l111l1_opy_.screenshot
                    def _1ll1l11l11_opy_(bstack11l1l11ll1_opy_, *bstack11l11l11l_opy_, **bstack111l1l1ll_opy_):
                        result = _1l1ll1l1l_opy_(bstack11l1l11ll1_opy_, *bstack11l11l11l_opy_, **bstack111l1l1ll_opy_)
                        try:
                            from bstack_utils.testhub_handler import TestHubHandler
                            from bstack_utils.bstack1l11111l1_opy_ import bstack11llll1l_opy_
                            if bstack11llll1l_opy_.on():
                                import base64
                                if isinstance(result, bytes):
                                    bstack11ll1lllll_opy_ = base64.b64encode(result).decode(bstack1ll1lll_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨః"))
                                else:
                                    bstack11ll1lllll_opy_ = str(result)
                                test_uuid = TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack11llll1l_opy_.current_hook_uuid()
                                if test_uuid and bstack11ll1lllll_opy_:
                                    TestHubHandler.bstack1111ll1lll_opy_({
                                        bstack1ll1lll_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩఄ"): bstack11ll1lllll_opy_,
                                        bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫఅ"): test_uuid
                                    })
                        except Exception as bstack1lll11111_opy_:
                            logger.debug(bstack1ll1lll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡲࡩࠦࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠠࡵࡱࠣࡓ࠶࠷ࡹࠡࠪࡰࡳࡩࡥࡣࡰࡰࡱࡩࡨࡺࠩ࠻ࠢࠨࡷࠧఆ"), bstack1lll11111_opy_)
                        return result
                    bstack11l1l111l1_opy_.screenshot = _1ll1l11l11_opy_
                    bstack11l1l111l1_opy_._bstack_screenshot_patched = True
            except Exception as exc:
                logger.debug(bstack1ll1lll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡩࠥࡪࡥࡧࡧࡵࡶࡪࡪࠠࡤ࡮ࡲࡷࡪࠦࡨࡰࡱ࡮ࡷࠥ࡯࡮ࠡ࡯ࡲࡨࡤࡩ࡯࡯ࡰࡨࡧࡹࡀࠠࠦࡵࠥఇ"), exc)
            logger.debug(bstack1ll1lll_opy_ (u"ࠢࡍࡧࡪࡥࡨࡿࠠࡤࡱࡱࡲࡪࡩࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡷࡶࡦࡩ࡫ࡪࡰࡪࠤࡸ࡫ࡴࡶࡲࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࠥ࡬࡯ࡳࠢࡷ࡬ࡷ࡫ࡡࡥࠢࡾࢁࠧఈ").format(threading.get_ident()))
        except Exception as e:
            logger.debug(bstack1ll1lll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࡶࡲࠣࡰࡪ࡭ࡡࡤࡻࠣࡧࡴࡴ࡮ࡦࡥࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡺࡲࡢࡥ࡮࡭ࡳ࡭࠺ࠡࡽࢀࠦఉ").format(str(e)))
    return browser
except Exception as e:
    pass
def patch_playwright():
    global SELENIUM_OR_PLAYWRIGHT_INSTALLED
    global FRAMEWORK_NAME
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack11lll11l1_opy_
        global bstack111l11ll1l_opy_
        if not bstack111l11ll1l_opy_:
            bstack111l11ll1l_opy_ = BrowserType.connect
        BrowserType.connect = bstack1llll11lll_opy_
        if bstack11lll11l1_opy_():
            BrowserType.launch = bstack11l11l1ll_opy_
            SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
        try:
            from playwright.sync_api._context_manager import PlaywrightContextManager
            if not hasattr(PlaywrightContextManager, bstack1ll1lll_opy_ (u"ࠩࡢࡦࡸࡺࡡࡤ࡭ࡢࡩࡳࡺࡥࡳࡡࡳࡥࡹࡩࡨࡦࡦࠪఊ")):
                _111lll1l1_opy_ = PlaywrightContextManager.__enter__
                def _11l1l1ll_opy_(bstack11l1111lll_opy_):
                    pw = _111lll1l1_opy_(bstack11l1111lll_opy_)
                    _1llll111ll_opy_ = pw.stop
                    _1lll1l1lll_opy_ = threading.current_thread()
                    _1lll1l1lll_opy_.bstack_deferred_pw_ref = pw
                    _1lll1l1lll_opy_.bstack_deferred_pw_stop_fn = _1llll111ll_opy_
                    def _1ll111lll1_opy_(*args, _bstack_sdk_close=False, **kwargs):
                        if not _bstack_sdk_close:
                            logger.debug(bstack1ll1lll_opy_ (u"ࠥࡈࡪ࡬ࡥࡳࡴࡨࡨࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠰ࡶࡸࡴࡶࠨࠪࠢ⠗ࠤࡼ࡯࡬࡭ࠢࡶࡸࡴࡶࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦఋ"))
                            threading.current_thread().bstack_deferred_pw_stop = True
                            return
                        return _1llll111ll_opy_()
                    pw.stop = _1ll111lll1_opy_
                    return pw
                PlaywrightContextManager.__enter__ = _11l1l1ll_opy_
                PlaywrightContextManager._bstack_enter_patched = True
        except Exception as e:
            logger.debug(bstack1ll1lll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡷࡧ࡭ࠦࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡆࡳࡳࡺࡥࡹࡶࡐࡥࡳࡧࡧࡦࡴ࠱ࡣࡤ࡫࡮ࡵࡧࡵࡣࡤࡀࠠࠦࡵࠥఌ"), e)
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack11ll111111_opy_
      SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
    except Exception as e:
      pass
def playwright_set_session_name(context, bstack111l1lllll_opy_):
  try:
    if getattr(context, bstack1ll1lll_opy_ (u"ࠬࡶࡡࡨࡧࠪ఍"), None):
      context.page.evaluate(bstack1ll1lll_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢఎ"), bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫఏ")+ json.dumps(bstack111l1lllll_opy_) + bstack1ll1lll_opy_ (u"ࠣࡿࢀࠦఐ"))
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃ࠺ࠡࡽࢀࠦ఑").format(str(e), traceback.format_exc()))
def playwright_annotate(context, message, level):
  try:
    if getattr(context, bstack1ll1lll_opy_ (u"ࠪࡴࡦ࡭ࡥࠨఒ"), None):
      context.page.evaluate(bstack1ll1lll_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧఓ"), bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪఔ") + json.dumps(message) + bstack1ll1lll_opy_ (u"࠭ࠬࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠩక") + json.dumps(level) + bstack1ll1lll_opy_ (u"ࠧࡾࡿࠪఖ"))
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡࡽࢀ࠾ࠥࢁࡽࠣగ").format(str(e), traceback.format_exc()))
@measure(event_name=EVENTS.bstack1lll11l1l1_opy_, stage=STAGE.bstack1111l1ll1_opy_, bstack1l1l1l11_opy_=SESSION_NAME)
def bstack11ll1lll_opy_(self, url):
  global bstack1l111lll11_opy_
  try:
    bstack11l1ll1111_opy_(url)
  except Exception as err:
    logger.debug(bstack11l11lll1l_opy_.format(str(err)))
  try:
    bstack1l111lll11_opy_(self, url)
  except Exception as e:
    try:
      parsed_error = str(e)
      if any(err_msg in parsed_error for err_msg in bstack11l1l1lll1_opy_):
        bstack11l1ll1111_opy_(url, True)
    except Exception as err:
      logger.debug(bstack11l11lll1l_opy_.format(str(err)))
    raise e
def bstack11l1lll11_opy_(self):
  global bstack111ll1l1_opy_
  bstack111ll1l1_opy_ = self
  return
def bstack1ll111l1l_opy_(self):
  global bstack1l11ll1l1l_opy_
  bstack1l11ll1l1l_opy_ = self
  return
def bstack1l111l1ll1_opy_(test_name, bstack11l1lll1ll_opy_):
  global CONFIG
  if percy.bstack11l1l1lll_opy_() == bstack1ll1lll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢఘ"):
    bstack11ll111l_opy_ = os.path.relpath(bstack11l1lll1ll_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack11ll111l_opy_)
    bstack1l1l1l11_opy_ = suite_name + bstack1ll1lll_opy_ (u"ࠥ࠱ࠧఙ") + test_name
    threading.current_thread().percySessionName = bstack1l1l1l11_opy_
def bstack1ll1llll_opy_(self, test, *args, **kwargs):
  global bstack111lll1l1l_opy_
  test_name = None
  bstack11l1lll1ll_opy_ = None
  if test:
    test_name = str(test.name)
    bstack11l1lll1ll_opy_ = str(test.source)
  bstack1l111l1ll1_opy_(test_name, bstack11l1lll1ll_opy_)
  bstack111lll1l1l_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.bstack111111ll11_opy_, stage=STAGE.bstack1111l1ll1_opy_, bstack1l1l1l11_opy_=SESSION_NAME)
def bstack11111l111l_opy_(driver, bstack1l1l1l11_opy_):
  if not bstack1ll11l1l_opy_ and bstack1l1l1l11_opy_:
      bstack1ll1lll111_opy_ = {
          bstack1ll1lll_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫచ"): bstack1ll1lll_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ఛ"),
          bstack1ll1lll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩజ"): {
              bstack1ll1lll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬఝ"): bstack1l1l1l11_opy_
          }
      }
      bstack11l111llll_opy_ = bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ఞ").format(json.dumps(bstack1ll1lll111_opy_))
      driver.execute_script(bstack11l111llll_opy_)
  if bstack1l1l1llll1_opy_:
      bstack1l111ll1_opy_ = {
          bstack1ll1lll_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩట"): bstack1ll1lll_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬఠ"),
          bstack1ll1lll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧడ"): {
              bstack1ll1lll_opy_ (u"ࠬࡪࡡࡵࡣࠪఢ"): bstack1l1l1l11_opy_ + bstack1ll1lll_opy_ (u"࠭ࠠࡱࡣࡶࡷࡪࡪࠡࠨణ"),
              bstack1ll1lll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭త"): bstack1ll1lll_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭థ")
          }
      }
      if bstack1l1l1llll1_opy_.status == bstack1ll1lll_opy_ (u"ࠩࡓࡅࡘ࡙ࠧద"):
          bstack1ll1ll1l_opy_ = bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨధ").format(json.dumps(bstack1l111ll1_opy_))
          driver.execute_script(bstack1ll1ll1l_opy_)
          bstack1ll1lll1l_opy_(driver, bstack1ll1lll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫన"))
      elif bstack1l1l1llll1_opy_.status == bstack1ll1lll_opy_ (u"ࠬࡌࡁࡊࡎࠪ఩"):
          reason = bstack1ll1lll_opy_ (u"ࠨࠢప")
          bstack1l1l11lll_opy_ = bstack1l1l1l11_opy_ + bstack1ll1lll_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠨఫ")
          if bstack1l1l1llll1_opy_.message:
              reason = str(bstack1l1l1llll1_opy_.message)
              bstack1l1l11lll_opy_ = bstack1l1l11lll_opy_ + bstack1ll1lll_opy_ (u"ࠨࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࡀࠠࠨబ") + reason
          bstack1l111ll1_opy_[bstack1ll1lll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬభ")] = {
              bstack1ll1lll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩమ"): bstack1ll1lll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪయ"),
              bstack1ll1lll_opy_ (u"ࠬࡪࡡࡵࡣࠪర"): bstack1l1l11lll_opy_
          }
          bstack1ll1ll1l_opy_ = bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫఱ").format(json.dumps(bstack1l111ll1_opy_))
          driver.execute_script(bstack1ll1ll1l_opy_)
          bstack1ll1lll1l_opy_(driver, bstack1ll1lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧల"), reason)
          bstack11l1ll1lll_opy_(reason, str(bstack1l1l1llll1_opy_), str(PLATFORM_INDEX), logger)
@measure(event_name=EVENTS.bstack1ll1lll11_opy_, stage=STAGE.bstack1111l1ll1_opy_, bstack1l1l1l11_opy_=SESSION_NAME)
def bstack1l11l11lll_opy_(driver, test):
  if percy.bstack11l1l1lll_opy_() == bstack1ll1lll_opy_ (u"ࠣࡶࡵࡹࡪࠨళ") and percy.bstack1ll1lllll_opy_() == bstack1ll1lll_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦఴ"):
      bstack1ll11lll11_opy_ = bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠪࡴࡪࡸࡣࡺࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭వ"), None)
      bstack1l11l11l11_opy_(driver, bstack1ll11lll11_opy_, test)
  if (bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨశ"), None) and
      bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫష"), None)) or (
      bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭స"), None) and
      bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩహ"), None)):
      logger.info(bstack1ll1lll_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠦࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡ࡫ࡶࠤࡺࡴࡤࡦࡴࡺࡥࡾ࠴ࠠࠣ఺"))
      a11y.bstack1111l1ll_opy_(driver, name=test.name, path=test.source)
def bstack1111l1lll1_opy_(test, bstack1l1l1l11_opy_):
    try:
      bstack11lllll111_opy_ = datetime.datetime.now()
      data = {}
      if test:
        data[bstack1ll1lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ఻")] = bstack1l1l1l11_opy_
      if bstack1l1l1llll1_opy_:
        if bstack1l1l1llll1_opy_.status == bstack1ll1lll_opy_ (u"ࠪࡔࡆ࡙ࡓࠨ఼"):
          data[bstack1ll1lll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫఽ")] = bstack1ll1lll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬా")
        elif bstack1l1l1llll1_opy_.status == bstack1ll1lll_opy_ (u"࠭ࡆࡂࡋࡏࠫి"):
          data[bstack1ll1lll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧీ")] = bstack1ll1lll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨు")
          if bstack1l1l1llll1_opy_.message:
            data[bstack1ll1lll_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩూ")] = str(bstack1l1l1llll1_opy_.message)
      user = CONFIG[bstack1ll1lll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬృ")]
      key = CONFIG[bstack1ll1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧౄ")]
      host = bstack11l11l11ll_opy_(cli.config, [bstack1ll1lll_opy_ (u"ࠧࡧࡰࡪࡵࠥ౅"), bstack1ll1lll_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥࠣె"), bstack1ll1lll_opy_ (u"ࠢࡢࡲ࡬ࠦే")], bstack1ll1lll_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠤై"))
      url = bstack1ll1lll_opy_ (u"ࠩࡾࢁ࠴ࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡴࡧࡶࡷ࡮ࡵ࡮ࡴ࠱ࡾࢁ࠳ࡰࡳࡰࡰࠪ౉").format(host, bstack1lllll1ll1_opy_)
      headers = {
        bstack1ll1lll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩొ"): bstack1ll1lll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧో"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers, auth=(user, key))
        cli.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽ࡹࡵࡪࡡࡵࡧࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡸࡦࡺࡵࡴࠤౌ"), datetime.datetime.now() - bstack11lllll111_opy_)
    except Exception as e:
      logger.error(bstack11l1l11l1l_opy_.format(str(e)))
def bstack1l1lll1l1l_opy_(test, bstack1l1l1l11_opy_):
  global CONFIG
  global bstack1l11ll1l1l_opy_
  global bstack111ll1l1_opy_
  global bstack1lllll1ll1_opy_
  global bstack1l1l1llll1_opy_
  global SESSION_NAME
  global bstack111111l1l_opy_
  global bstack111l11ll_opy_
  global bstack1ll1l1l1l1_opy_
  global bstack1l1llll1ll_opy_
  global bstack11ll1llll_opy_
  global bstack1l11ll11l1_opy_
  global bstack1l11l1llll_opy_
  try:
    if not bstack1lllll1ll1_opy_:
      with bstack1l11l1llll_opy_:
        bstack11ll1llll1_opy_ = os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"࠭ࡾࠨ్")), bstack1ll1lll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ౎"), bstack1ll1lll_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪ౏"))
        if os.path.exists(bstack11ll1llll1_opy_):
          with open(bstack11ll1llll1_opy_, bstack1ll1lll_opy_ (u"ࠩࡵࠫ౐")) as f:
            content = f.read().strip()
            if content:
              bstack111l1l11ll_opy_ = json.loads(bstack1ll1lll_opy_ (u"ࠥࡿࠧ౑") + content + bstack1ll1lll_opy_ (u"ࠫࠧࡾࠢ࠻ࠢࠥࡽࠧ࠭౒") + bstack1ll1lll_opy_ (u"ࠧࢃࠢ౓"))
              bstack1lllll1ll1_opy_ = bstack111l1l11ll_opy_.get(str(threading.get_ident()))
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡸࡥࡢࡦ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡊࡆࡶࠤ࡫࡯࡬ࡦ࠼ࠣࠫ౔") + str(e))
  if not is_robot_playwright_installed():
    if bstack11ll1llll_opy_:
      with bstack1l1l1ll1l_opy_:
        bstack111111lll1_opy_ = bstack11ll1llll_opy_.copy()
      for driver in bstack111111lll1_opy_:
        if bstack1lllll1ll1_opy_ == driver.session_id:
          if test:
            bstack1l11l11lll_opy_(driver, test)
          bstack11111l111l_opy_(driver, bstack1l1l1l11_opy_)
    elif bstack1lllll1ll1_opy_:
      bstack1111l1lll1_opy_(test, bstack1l1l1l11_opy_)
    if bstack1l11ll1l1l_opy_:
      bstack111l11ll_opy_(bstack1l11ll1l1l_opy_)
    if bstack111ll1l1_opy_:
      bstack1ll1l1l1l1_opy_(bstack111ll1l1_opy_)
    if bstack1111l1l1ll_opy_:
      bstack1l1llll1ll_opy_()
def bstack1ll1lll1_opy_(self, test, *args, **kwargs):
  bstack1l1l1l11_opy_ = None
  if test:
    bstack1l1l1l11_opy_ = str(test.name)
  bstack1l1lll1l1l_opy_(test, bstack1l1l1l11_opy_)
  bstack111111l1l_opy_(self, test, *args, **kwargs)
def bstack1l11l1111l_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1111l11l11_opy_
  global CONFIG
  global bstack11ll1llll_opy_
  global bstack1lllll1ll1_opy_
  global bstack1l11l1llll_opy_
  bstack1111lll1ll_opy_ = None
  try:
    if bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲౕ࠭"), None) or bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ౖࠪ"), None):
      try:
        if not bstack1lllll1ll1_opy_:
          bstack11ll1llll1_opy_ = os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"ࠩࢁࠫ౗")), bstack1ll1lll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪౘ"), bstack1ll1lll_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭ౙ"))
          with bstack1l11l1llll_opy_:
            if os.path.exists(bstack11ll1llll1_opy_):
              with open(bstack11ll1llll1_opy_, bstack1ll1lll_opy_ (u"ࠬࡸࠧౚ")) as f:
                content = f.read().strip()
                if content:
                  bstack111l1l11ll_opy_ = json.loads(bstack1ll1lll_opy_ (u"ࠨࡻࠣ౛") + content + bstack1ll1lll_opy_ (u"ࠧࠣࡺࠥ࠾ࠥࠨࡹࠣࠩ౜") + bstack1ll1lll_opy_ (u"ࠣࡿࠥౝ"))
                  bstack1lllll1ll1_opy_ = bstack111l1l11ll_opy_.get(str(threading.get_ident()))
      except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡴࡨࡥࡩ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡍࡉࡹࠠࡧ࡫࡯ࡩࠥ࡯࡮ࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࡀࠠࠨ౞") + str(e))
      if bstack11ll1llll_opy_:
        with bstack1l1l1ll1l_opy_:
          bstack111111lll1_opy_ = bstack11ll1llll_opy_.copy()
        for driver in bstack111111lll1_opy_:
          if bstack1lllll1ll1_opy_ == driver.session_id:
            bstack1111lll1ll_opy_ = driver
    bstack11111lll11_opy_ = a11y.is_enabled_testcase(test.tags)
    if bstack1111lll1ll_opy_:
      threading.current_thread().isA11yTest = a11y.start_test_capture(bstack1111lll1ll_opy_, bstack11111lll11_opy_)
      threading.current_thread().isAppA11yTest = a11y.start_test_capture(bstack1111lll1ll_opy_, bstack11111lll11_opy_)
    else:
      threading.current_thread().isA11yTest = bstack11111lll11_opy_
      threading.current_thread().isAppA11yTest = bstack11111lll11_opy_
  except:
    pass
  bstack1111l11l11_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1l1l1llll1_opy_
  try:
    bstack1l1l1llll1_opy_ = self._test
  except:
    bstack1l1l1llll1_opy_ = self.test
def bstack11lllll1_opy_():
  global bstack11l1111111_opy_
  try:
    if os.path.exists(bstack11l1111111_opy_):
      os.remove(bstack11l1111111_opy_)
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭౟") + str(e))
def bstack11l111l11l_opy_():
  global bstack11l1111111_opy_
  bstack1111l11ll1_opy_ = {}
  lock_file = bstack11l1111111_opy_ + bstack1ll1lll_opy_ (u"ࠫ࠳ࡲ࡯ࡤ࡭ࠪౠ")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1ll1lll_opy_ (u"ࠬ࡬ࡩ࡭ࡧ࡯ࡳࡨࡱࠠ࡯ࡱࡷࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠬࠡࡷࡶ࡭ࡳ࡭ࠠࡣࡣࡶ࡭ࡨࠦࡦࡪ࡮ࡨࠤࡴࡶࡥࡳࡣࡷ࡭ࡴࡴࡳࠨౡ"))
    try:
      if not os.path.isfile(bstack11l1111111_opy_):
        with open(bstack11l1111111_opy_, bstack1ll1lll_opy_ (u"࠭ࡷࠨౢ")) as f:
          json.dump({}, f)
      if os.path.exists(bstack11l1111111_opy_):
        with open(bstack11l1111111_opy_, bstack1ll1lll_opy_ (u"ࠧࡳࠩౣ")) as f:
          content = f.read().strip()
          if content:
            bstack1111l11ll1_opy_ = json.loads(content)
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡶࡪࡧࡤࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪ౤") + str(e))
    return bstack1111l11ll1_opy_
  try:
    os.makedirs(os.path.dirname(bstack11l1111111_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      if not os.path.isfile(bstack11l1111111_opy_):
        with open(bstack11l1111111_opy_, bstack1ll1lll_opy_ (u"ࠩࡺࠫ౥")) as f:
          json.dump({}, f)
      if os.path.exists(bstack11l1111111_opy_):
        with open(bstack11l1111111_opy_, bstack1ll1lll_opy_ (u"ࠪࡶࠬ౦")) as f:
          content = f.read().strip()
          if content:
            bstack1111l11ll1_opy_ = json.loads(content)
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡲࡦࡣࡧ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭౧") + str(e))
  finally:
    return bstack1111l11ll1_opy_
def bstack1l11l1l11l_opy_(platform_index, item_index):
  global bstack11l1111111_opy_
  lock_file = bstack11l1111111_opy_ + bstack1ll1lll_opy_ (u"ࠬ࠴࡬ࡰࡥ࡮ࠫ౨")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1ll1lll_opy_ (u"࠭ࡦࡪ࡮ࡨࡰࡴࡩ࡫ࠡࡰࡲࡸࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥ࠭ࠢࡸࡷ࡮ࡴࡧࠡࡤࡤࡷ࡮ࡩࠠࡧ࡫࡯ࡩࠥࡵࡰࡦࡴࡤࡸ࡮ࡵ࡮ࡴࠩ౩"))
    try:
      bstack1111l11ll1_opy_ = {}
      if os.path.exists(bstack11l1111111_opy_):
        with open(bstack11l1111111_opy_, bstack1ll1lll_opy_ (u"ࠧࡳࠩ౪")) as f:
          content = f.read().strip()
          if content:
            bstack1111l11ll1_opy_ = json.loads(content)
      bstack1111l11ll1_opy_[item_index] = platform_index
      with open(bstack11l1111111_opy_, bstack1ll1lll_opy_ (u"ࠣࡹࠥ౫")) as outfile:
        json.dump(bstack1111l11ll1_opy_, outfile)
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡼࡸࡩࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧ౬") + str(e))
    return
  try:
    os.makedirs(os.path.dirname(bstack11l1111111_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      bstack1111l11ll1_opy_ = {}
      if os.path.exists(bstack11l1111111_opy_):
        with open(bstack11l1111111_opy_, bstack1ll1lll_opy_ (u"ࠪࡶࠬ౭")) as f:
          content = f.read().strip()
          if content:
            bstack1111l11ll1_opy_ = json.loads(content)
      bstack1111l11ll1_opy_[item_index] = platform_index
      with open(bstack11l1111111_opy_, bstack1ll1lll_opy_ (u"ࠦࡼࠨ౮")) as outfile:
        json.dump(bstack1111l11ll1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡸࡴ࡬ࡸ࡮ࡴࡧࠡࡶࡲࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪ౯") + str(e))
def bstack1l11ll11ll_opy_(bstack1ll111ll_opy_):
  global CONFIG
  bstack111lll1ll_opy_ = bstack1ll1lll_opy_ (u"࠭ࠧ౰")
  if not bstack1ll1lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ౱") in CONFIG:
    logger.info(bstack1ll1lll_opy_ (u"ࠨࡐࡲࠤࡵࡲࡡࡵࡨࡲࡶࡲࡹࠠࡱࡣࡶࡷࡪࡪࠠࡶࡰࡤࡦࡱ࡫ࠠࡵࡱࠣ࡫ࡪࡴࡥࡳࡣࡷࡩࠥࡸࡥࡱࡱࡵࡸࠥ࡬࡯ࡳࠢࡕࡳࡧࡵࡴࠡࡴࡸࡲࠬ౲"))
  try:
    platform = CONFIG[bstack1ll1lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ౳")][bstack1ll111ll_opy_]
    if bstack1ll1lll_opy_ (u"ࠪࡳࡸ࠭౴") in platform:
      bstack111lll1ll_opy_ += str(platform[bstack1ll1lll_opy_ (u"ࠫࡴࡹࠧ౵")]) + bstack1ll1lll_opy_ (u"ࠬ࠲ࠠࠨ౶")
    if bstack1ll1lll_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ౷") in platform:
      bstack111lll1ll_opy_ += str(platform[bstack1ll1lll_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪ౸")]) + bstack1ll1lll_opy_ (u"ࠨ࠮ࠣࠫ౹")
    if bstack1ll1lll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭౺") in platform:
      bstack111lll1ll_opy_ += str(platform[bstack1ll1lll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧ౻")]) + bstack1ll1lll_opy_ (u"ࠫ࠱ࠦࠧ౼")
    if bstack1ll1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ౽") in platform:
      bstack111lll1ll_opy_ += str(platform[bstack1ll1lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ౾")]) + bstack1ll1lll_opy_ (u"ࠧ࠭ࠢࠪ౿")
    if bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ಀ") in platform:
      bstack111lll1ll_opy_ += str(platform[bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧಁ")]) + bstack1ll1lll_opy_ (u"ࠪ࠰ࠥ࠭ಂ")
    if bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬಃ") in platform:
      bstack111lll1ll_opy_ += str(platform[bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭಄")]) + bstack1ll1lll_opy_ (u"࠭ࠬࠡࠩಅ")
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠧࡔࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡱࡩࡷࡧࡴࡪࡰࡪࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡳࡵࡴ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡶࡪࡶ࡯ࡳࡶࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡴࡴࠧಆ") + str(e))
  finally:
    if bstack111lll1ll_opy_[len(bstack111lll1ll_opy_) - 2:] == bstack1ll1lll_opy_ (u"ࠨ࠮ࠣࠫಇ"):
      bstack111lll1ll_opy_ = bstack111lll1ll_opy_[:-2]
    return bstack111lll1ll_opy_
def bstack11llll111l_opy_(path, bstack111lll1ll_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1lll1llll_opy_ = ET.parse(path)
    bstack1l11lll11_opy_ = bstack1lll1llll_opy_.getroot()
    bstack111l11l1l1_opy_ = None
    for suite in bstack1l11lll11_opy_.iter(bstack1ll1lll_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨಈ")):
      if bstack1ll1lll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪಉ") in suite.attrib:
        suite.attrib[bstack1ll1lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩಊ")] += bstack1ll1lll_opy_ (u"ࠬࠦࠧಋ") + bstack111lll1ll_opy_
        bstack111l11l1l1_opy_ = suite
    bstack111l1ll11_opy_ = None
    for robot in bstack1l11lll11_opy_.iter(bstack1ll1lll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬಌ")):
      bstack111l1ll11_opy_ = robot
    bstack1ll1111l1_opy_ = len(bstack111l1ll11_opy_.findall(bstack1ll1lll_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭಍")))
    if bstack1ll1111l1_opy_ == 1:
      bstack111l1ll11_opy_.remove(bstack111l1ll11_opy_.findall(bstack1ll1lll_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧಎ"))[0])
      bstack1111l111ll_opy_ = ET.Element(bstack1ll1lll_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨಏ"), attrib={bstack1ll1lll_opy_ (u"ࠪࡲࡦࡳࡥࠨಐ"): bstack1ll1lll_opy_ (u"ࠫࡘࡻࡩࡵࡧࡶࠫ಑"), bstack1ll1lll_opy_ (u"ࠬ࡯ࡤࠨಒ"): bstack1ll1lll_opy_ (u"࠭ࡳ࠱ࠩಓ")})
      bstack111l1ll11_opy_.insert(1, bstack1111l111ll_opy_)
      bstack111lll11l_opy_ = None
      for suite in bstack111l1ll11_opy_.iter(bstack1ll1lll_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭ಔ")):
        bstack111lll11l_opy_ = suite
      bstack111lll11l_opy_.append(bstack111l11l1l1_opy_)
      bstack11llll1ll_opy_ = None
      for status in bstack111l11l1l1_opy_.iter(bstack1ll1lll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨಕ")):
        bstack11llll1ll_opy_ = status
      bstack111lll11l_opy_.append(bstack11llll1ll_opy_)
    bstack1lll1llll_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡲࡴ࡫ࡱ࡫ࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠧಖ") + str(e))
def bstack1lll11l11_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1llll1l1ll_opy_
  global CONFIG
  if bstack1ll1lll_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࡳࡥࡹ࡮ࠢಗ") in options:
    del options[bstack1ll1lll_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡴࡦࡺࡨࠣಘ")]
  json_data = bstack11l111l11l_opy_()
  for item_id in json_data.keys():
    path = os.path.join(outs_dir, str(item_id), bstack1ll1lll_opy_ (u"ࠬࡵࡵࡵࡲࡸࡸ࠳ࡾ࡭࡭ࠩಙ"))
    bstack11llll111l_opy_(path, bstack1l11ll11ll_opy_(json_data[item_id]))
  bstack11lllll1_opy_()
  return bstack1llll1l1ll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1lllll111_opy_(self, ff_profile_dir):
  global bstack11l111lll1_opy_
  if not ff_profile_dir:
    return None
  return bstack11l111lll1_opy_(self, ff_profile_dir)
def bstack1llll11ll_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1l1l11111_opy_
  bstack1ll111l11_opy_ = []
  if bstack1ll1lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩಚ") in CONFIG:
    bstack1ll111l11_opy_ = CONFIG[bstack1ll1lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪಛ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1ll1lll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤಜ")],
      pabot_args[bstack1ll1lll_opy_ (u"ࠤࡹࡩࡷࡨ࡯ࡴࡧࠥಝ")],
      argfile,
      pabot_args.get(bstack1ll1lll_opy_ (u"ࠥ࡬࡮ࡼࡥࠣಞ")),
      pabot_args[bstack1ll1lll_opy_ (u"ࠦࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠢಟ")],
      platform[0],
      bstack1l1l11111_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1ll1lll_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡦࡪ࡮ࡨࡷࠧಠ")] or [(bstack1ll1lll_opy_ (u"ࠨࠢಡ"), None)]
    for platform in enumerate(bstack1ll111l11_opy_)
  ]
def bstack1l1ll1l11_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1111l11l_opy_=bstack1ll1lll_opy_ (u"ࠧࠨಢ")):
  global bstack1lllll1lll_opy_
  self.platform_index = platform_index
  self.bstack1l111111l_opy_ = bstack1111l11l_opy_
  bstack1lllll1lll_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1lll11lll_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1111111l1l_opy_
  global bstack1l11l111_opy_
  bstack111ll11l_opy_ = copy.deepcopy(item)
  if not bstack1ll1lll_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪಣ") in item.options:
    bstack111ll11l_opy_.options[bstack1ll1lll_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫತ")] = []
  bstack1l1l1ll1ll_opy_ = bstack111ll11l_opy_.options[bstack1ll1lll_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬಥ")].copy()
  for v in bstack111ll11l_opy_.options[bstack1ll1lll_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ದ")]:
    if bstack1ll1lll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡕࡒࡁࡕࡈࡒࡖࡒࡏࡎࡅࡇ࡛ࠫಧ") in v:
      bstack1l1l1ll1ll_opy_.remove(v)
    if bstack1ll1lll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘ࠭ನ") in v:
      bstack1l1l1ll1ll_opy_.remove(v)
    if bstack1ll1lll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡄࡆࡈࡏࡓࡈࡇࡌࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ಩") in v:
      bstack1l1l1ll1ll_opy_.remove(v)
  bstack1l1l1ll1ll_opy_.insert(0, bstack1ll1lll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡑࡎࡄࡘࡋࡕࡒࡎࡋࡑࡈࡊ࡞࠺ࡼࡿࠪಪ").format(bstack111ll11l_opy_.platform_index))
  bstack1l1l1ll1ll_opy_.insert(0, bstack1ll1lll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡆࡈࡊࡑࡕࡃࡂࡎࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗࡀࡻࡾࠩಫ").format(bstack111ll11l_opy_.bstack1l111111l_opy_))
  bstack111ll11l_opy_.options[bstack1ll1lll_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬಬ")] = bstack1l1l1ll1ll_opy_
  if bstack1l11l111_opy_:
    bstack111ll11l_opy_.options[bstack1ll1lll_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ಭ")].insert(0, bstack1ll1lll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡒࡉࡂࡔࡊࡗ࠿ࢁࡽࠨಮ").format(bstack1l11l111_opy_))
  return bstack1111111l1l_opy_(caller_id, datasources, is_last, bstack111ll11l_opy_, outs_dir)
def bstack11l11l111_opy_(command, item_index):
  try:
    if global_config.get_property(bstack1ll1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧಯ")):
      os.environ[bstack1ll1lll_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨರ")] = json.dumps(CONFIG[bstack1ll1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫಱ")][item_index % bstack11ll1l11_opy_])
    global bstack1l11l111_opy_
    os.environ[bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩಲ")] = str(item_index % bstack11ll1l11_opy_)
    listener_arg = bstack1ll1lll_opy_ (u"ࠪࠫಳ")
    if is_robot_playwright_installed() and cli.is_enabled(CONFIG):
      listener_arg = bstack1ll1lll_opy_ (u"ࠫࠥ࠳࠭࡭࡫ࡶࡸࡪࡴࡥࡳࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡵࡧ࡯࠳ࡸ࡯ࡣࡱࡷࡣࡱ࡯ࡳࡵࡧࡱࡩࡷࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠱ࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࡐࡢࡶࡦ࡬ࡪࡸࠧ಴")
      logger.debug(bstack1ll1lll_opy_ (u"ࠧࡇࡤࡥ࡫ࡱ࡫ࠥࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡒࡤࡸࡨ࡮ࡥࡳࠢ࡯࡭ࡸࡺࡥ࡯ࡧࡵࠤ࡫ࡵࡲࠡ࡫ࡷࡩࡲࠦࡻࡾࠤವ").format(item_index))
    bstack1ll11llll_opy_ = bstack1ll1lll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡹࡤ࡬ࠢࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠣ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࠦࠢಶ") + \
              str(item_index % bstack11ll1l11_opy_) + \
              bstack1ll1lll_opy_ (u"ࠢࠡ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠠࠣಷ") + \
              str(item_index) + \
              listener_arg
    if bstack1l11l111_opy_:
        bstack1ll11llll_opy_ += bstack1ll1lll_opy_ (u"ࠣࠢࠥಸ") + bstack1l11l111_opy_
    command[0:1] = bstack1ll11llll_opy_.split()
  except Exception as e:
    logger.error(bstack1ll1lll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡯ࡲࡨ࡮࡬ࡹࡪࡰࡪࠤࡨࡵ࡭࡮ࡣࡱࡨࠥ࡬࡯ࡳࠢࡳࡥࡧࡵࡴࠡࡴࡸࡲ࠿ࠦࡻࡾࠩಹ").format(str(e)))
def bstack1llll111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack11l1l111_opy_
  try:
    bstack11l11l111_opy_(command, item_index)
    return bstack11l1l111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
  except Exception as e:
    logger.error(bstack1ll1lll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡣࡱࡷࠤࡷࡻ࡮࠻ࠢࡾࢁࠬ಺").format(str(e)))
    raise e
def bstack1l1l1l1ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack11l1l111_opy_
  try:
    bstack11l11l111_opy_(command, item_index)
    return bstack11l1l111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
  except Exception as e:
    logger.error(bstack1ll1lll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡢࡤࡲࡸࠥࡸࡵ࡯ࠢ࠵࠲࠶࠹࠺ࠡࡽࢀࠫ಻").format(str(e)))
    try:
      return bstack11l1l111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
    except Exception as e2:
      logger.error(bstack1ll1lll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡥࡳࡹࠦ࠲࠯࠳࠶ࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࡼࡿ಼ࠪ").format(str(e2)))
      raise e
def bstack1llllll1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack11l1l111_opy_
  try:
    bstack11l11l111_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    return bstack11l1l111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
  except Exception as e:
    logger.error(bstack1ll1lll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠࡳࡷࡱࠤ࠷࠴࠱࠶࠼ࠣࡿࢂ࠭ಽ").format(str(e)))
    try:
      return bstack11l1l111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
    except Exception as e2:
      logger.error(bstack1ll1lll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡧࡵࡴࠡ࠴࠱࠵࠺ࠦࡦࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢࡾࢁࠬಾ").format(str(e2)))
      raise e
def _1lll1l1l_opy_(bstack1l11111ll1_opy_, item_index, process_timeout, sleep_before_start, bstack1l1llll111_opy_):
  bstack11l11l111_opy_(bstack1l11111ll1_opy_, item_index)
  if process_timeout is None:
    process_timeout = 3600
  if sleep_before_start and sleep_before_start > 0:
    time.sleep(min(sleep_before_start, 5))
  return process_timeout
def bstack1l1ll1lll1_opy_(command, bstack1111ll11ll_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack11l1l111_opy_
  global bstack1l1lll1l11_opy_
  global bstack1l11l111_opy_
  try:
    for env_name, bstack1l1ll111l1_opy_ in bstack1l1lll1l11_opy_.items():
      os.environ[env_name] = bstack1l1ll111l1_opy_
    bstack1l11l111_opy_ = bstack1ll1lll_opy_ (u"ࠣࠤಿ")
    bstack11l11l111_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    if sleep_before_start and sleep_before_start > 0:
      time.sleep(min(sleep_before_start, 5))
    return bstack11l1l111_opy_(command, bstack1111ll11ll_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack1ll1lll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡢࡰࡶࠣࡶࡺࡴࠠ࠶࠰࠳࠾ࠥࢁࡽࠨೀ").format(str(e)))
    try:
      return bstack11l1l111_opy_(command, bstack1111ll11ll_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack1ll1lll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡣࡱࡷࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࡼࡿࠪು").format(str(e2)))
      raise e
def bstack1l111l1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack11l1l111_opy_
  try:
    process_timeout = _1lll1l1l_opy_(command, item_index, process_timeout, sleep_before_start, bstack1ll1lll_opy_ (u"ࠫ࠹࠴࠲ࠨೂ"))
    return bstack11l1l111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack1ll1lll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡥࡳࡹࠦࡲࡶࡰࠣ࠸࠳࠸࠺ࠡࡽࢀࠫೃ").format(str(e)))
    try:
      return bstack11l1l111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack1ll1lll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠࡧࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣࡿࢂ࠭ೄ").format(str(e2)))
      raise e
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack11llll11ll_opy_(self, runner, quiet=False, capture=True):
  global bstack1l1llllll_opy_
  bstack1lll1ll11_opy_ = bstack1l1llllll_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack1ll1lll_opy_ (u"ࠧࡦࡺࡦࡩࡵࡺࡩࡰࡰࡢࡥࡷࡸࠧ೅")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1ll1lll_opy_ (u"ࠨࡧࡻࡧࡤࡺࡲࡢࡥࡨࡦࡦࡩ࡫ࡠࡣࡵࡶࠬೆ")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1lll1ll11_opy_
def bstack1lllll11ll_opy_(runner, hook_name, context, element, bstack1111lllll_opy_, *args):
  global bstack11111l11ll_opy_
  try:
    if runner.hooks.get(hook_name):
      bstack11l11111_opy_.bstack111l1l11_opy_(hook_name, element)
    if bstack11111l11ll_opy_ is None or bstack11111l11ll_opy_:
      bstack1111lllll_opy_(runner, hook_name, context, *args)
    else:
      bstack11l11lll11_opy_ = (context,) + args
      bstack1111lllll_opy_(runner, hook_name, *bstack11l11lll11_opy_)
    if runner.hooks.get(hook_name):
      bstack11l11111_opy_.bstack111lll111l_opy_(element)
      if hook_name not in [bstack1ll1lll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱ࠭ೇ"), bstack1ll1lll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ࠭ೈ")] and args and hasattr(args[0], bstack1ll1lll_opy_ (u"ࠫࡪࡸࡲࡰࡴࡢࡱࡪࡹࡳࡢࡩࡨࠫ೉")):
        args[0].error_message = bstack1ll1lll_opy_ (u"ࠬ࠭ೊ")
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢ࡫ࡥࡳࡪ࡬ࡦࠢ࡫ࡳࡴࡱࡳࠡ࡫ࡱࠤࡧ࡫ࡨࡢࡸࡨ࠾ࠥࢁࡽࠨೋ").format(str(e)))
@measure(event_name=EVENTS.bstack11111l1l_opy_, stage=STAGE.bstack1111l1ll1_opy_, hook_type=bstack1ll1lll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࡁ࡭࡮ࠥೌ"), bstack1l1l1l11_opy_=SESSION_NAME)
def bstack1l1l1111ll_opy_(runner, name, context, bstack1111lllll_opy_, *args):
    if runner.hooks.get(bstack1ll1lll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰ್ࠧ")).__name__ != bstack1ll1lll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࡥࡤࡦࡨࡤࡹࡱࡺ࡟ࡩࡱࡲ࡯ࠧ೎"):
      bstack1lllll11ll_opy_(runner, name, context, runner, bstack1111lllll_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack1l11ll1111_opy_(bstack1ll1lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ೏")) else context.browser
      runner.driver_initialised = bstack1ll1lll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣ೐")
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡪࡲࡪࡸࡨࡶࠥ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡳࡦࠢࡤࡸࡹࡸࡩࡣࡷࡷࡩ࠿ࠦࡻࡾࠩ೑").format(str(e)))
def bstack1l1lll111_opy_(runner, name, context, bstack1111lllll_opy_, *args):
    bstack1lllll11ll_opy_(runner, name, context, context.feature, bstack1111lllll_opy_, *args)
    try:
      if not bstack1ll11l1l_opy_:
        bstack1111lll1ll_opy_ = threading.current_thread().bstackSessionDriver if bstack1l11ll1111_opy_(bstack1ll1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ೒")) else context.browser
        if is_driver_active(bstack1111lll1ll_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack1ll1lll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣ೓")
          bstack111l1lllll_opy_ = str(runner.feature.name)
          playwright_set_session_name(context, bstack111l1lllll_opy_)
          bstack1111lll1ll_opy_.execute_script(bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭೔") + json.dumps(bstack111l1lllll_opy_) + bstack1ll1lll_opy_ (u"ࠩࢀࢁࠬೕ"))
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡬ࡥࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪೖ").format(str(e)))
def bstack1l111lll1_opy_(runner, name, context, bstack1111lllll_opy_, *args):
    target = context.scenario if hasattr(context, bstack1ll1lll_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭೗")) else context.feature
    bstack1lllll11ll_opy_(runner, name, context, target, bstack1111lllll_opy_, *args)
@measure(event_name=EVENTS.bstack111ll1ll11_opy_, stage=STAGE.bstack1111l1ll1_opy_, bstack1l1l1l11_opy_=SESSION_NAME)
def bstack1l11ll11_opy_(runner, name, context, bstack1111lllll_opy_, *args):
    bstack11l11111_opy_.start_test(context)
    bstack1lllll11ll_opy_(runner, name, context, context.scenario, bstack1111lllll_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack1l11ll1l1_opy_.bstack1l11l1l1l_opy_(context, *args)
    try:
      bstack1111lll1ll_opy_ = bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ೘"), context.browser)
      if is_driver_active(bstack1111lll1ll_opy_):
        TestHubHandler.send_cbt_info(bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ೙"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack1ll1lll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤ೚")
        if (not bstack1ll11l1l_opy_):
          scenario_name = args[0].name
          feature_name = bstack111l1lllll_opy_ = str(runner.feature.name)
          bstack111l1lllll_opy_ = feature_name + bstack1ll1lll_opy_ (u"ࠨࠢ࠰ࠤࠬ೛") + scenario_name
          if runner.driver_initialised == bstack1ll1lll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦ೜"):
            playwright_set_session_name(context, bstack111l1lllll_opy_)
            bstack1111lll1ll_opy_.execute_script(bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨೝ") + json.dumps(bstack111l1lllll_opy_) + bstack1ll1lll_opy_ (u"ࠫࢂࢃࠧೞ"))
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤ࡮ࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡥࡨࡲࡦࡸࡩࡰ࠼ࠣࡿࢂ࠭೟").format(str(e)))
@measure(event_name=EVENTS.bstack11111l1l_opy_, stage=STAGE.bstack1111l1ll1_opy_, hook_type=bstack1ll1lll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪ࡙ࡴࡦࡲࠥೠ"), bstack1l1l1l11_opy_=SESSION_NAME)
def bstack111l1l1l_opy_(runner, name, context, bstack1111lllll_opy_, *args):
    bstack1lllll11ll_opy_(runner, name, context, args[0], bstack1111lllll_opy_, *args)
    try:
      bstack1111lll1ll_opy_ = threading.current_thread().bstackSessionDriver if bstack1l11ll1111_opy_(bstack1ll1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ೡ")) else context.browser
      if is_driver_active(bstack1111lll1ll_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack1ll1lll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨೢ")
        bstack11l11111_opy_.bstack111ll11l11_opy_(args[0])
        if runner.driver_initialised == bstack1ll1lll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢೣ") and not bstack1ll11l1l_opy_:
          feature_name = bstack111l1lllll_opy_ = str(runner.feature.name)
          bstack111l1lllll_opy_ = feature_name + bstack1ll1lll_opy_ (u"ࠪࠤ࠲ࠦࠧ೤") + context.scenario.name
          playwright_set_session_name(context, bstack111l1lllll_opy_)
          bstack1111lll1ll_opy_.execute_script(bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩ೥") + json.dumps(bstack111l1lllll_opy_) + bstack1ll1lll_opy_ (u"ࠬࢃࡽࠨ೦"))
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡷࡩࡵࡀࠠࡼࡿࠪ೧").format(str(e)))
@measure(event_name=EVENTS.bstack11111l1l_opy_, stage=STAGE.bstack1111l1ll1_opy_, hook_type=bstack1ll1lll_opy_ (u"ࠢࡢࡨࡷࡩࡷ࡙ࡴࡦࡲࠥ೨"), bstack1l1l1l11_opy_=SESSION_NAME)
def bstack1l1l11llll_opy_(runner, name, context, bstack1111lllll_opy_, *args):
  bstack11l11111_opy_.bstack1l1l1ll111_opy_(args[0])
  try:
    step_status = args[0].status.name
    bstack1111lll1ll_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ೩") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack1111lll1ll_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack1ll1lll_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩ೪")
        if not bstack1ll11l1l_opy_:
          feature_name = bstack111l1lllll_opy_ = str(runner.feature.name)
          bstack111l1lllll_opy_ = feature_name + bstack1ll1lll_opy_ (u"ࠪࠤ࠲ࠦࠧ೫") + context.scenario.name
          playwright_set_session_name(context, bstack111l1lllll_opy_)
          bstack1111lll1ll_opy_.execute_script(bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩ೬") + json.dumps(bstack111l1lllll_opy_) + bstack1ll1lll_opy_ (u"ࠬࢃࡽࠨ೭"))
    if str(step_status).lower() in [bstack1ll1lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭೮"), bstack1ll1lll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭೯")]:
      bstack1l1l11l11l_opy_ = bstack1ll1lll_opy_ (u"ࠨࠩ೰")
      bstack1l1111l11l_opy_ = bstack1ll1lll_opy_ (u"ࠩࠪೱ")
      bstack1l1111l11_opy_ = bstack1ll1lll_opy_ (u"ࠪࠫೲ")
      try:
        import traceback
        bstack1l1l11l11l_opy_ = runner.exception.__class__.__name__
        bstack1111l11l1l_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1l1111l11l_opy_ = bstack1ll1lll_opy_ (u"ࠫࠥ࠭ೳ").join(bstack1111l11l1l_opy_)
        bstack1l1111l11_opy_ = bstack1111l11l1l_opy_[-1]
      except Exception as e:
        logger.debug(bstack111lllll_opy_.format(str(e)))
      bstack1l1l11l11l_opy_ += bstack1l1111l11_opy_
      playwright_annotate(context, json.dumps(str(args[0].name) + bstack1ll1lll_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦ೴") + str(bstack1l1111l11l_opy_)),
                          bstack1ll1lll_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ೵"))
      if runner.driver_initialised == bstack1ll1lll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧ೶"):
        bstack1ll1l1lll1_opy_(getattr(context, bstack1ll1lll_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭೷"), None), bstack1ll1lll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ೸"), bstack1l1l11l11l_opy_)
        bstack1111lll1ll_opy_.execute_script(bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨ೹") + json.dumps(str(args[0].name) + bstack1ll1lll_opy_ (u"ࠦࠥ࠳ࠠࡇࡣ࡬ࡰࡪࡪࠡ࡝ࡰࠥ೺") + str(bstack1l1111l11l_opy_)) + bstack1ll1lll_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥࡩࡷࡸ࡯ࡳࠤࢀࢁࠬ೻"))
      if runner.driver_initialised == bstack1ll1lll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦ೼"):
        bstack1ll1lll1l_opy_(bstack1111lll1ll_opy_, bstack1ll1lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ೽"), bstack1ll1lll_opy_ (u"ࠣࡕࡦࡩࡳࡧࡲࡪࡱࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧ೾") + str(bstack1l1l11l11l_opy_))
    else:
      playwright_annotate(context, bstack1ll1lll_opy_ (u"ࠤࡓࡥࡸࡹࡥࡥࠣࠥ೿"), bstack1ll1lll_opy_ (u"ࠥ࡭ࡳ࡬࡯ࠣഀ"))
      if runner.driver_initialised == bstack1ll1lll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤഁ"):
        bstack1ll1l1lll1_opy_(getattr(context, bstack1ll1lll_opy_ (u"ࠬࡶࡡࡨࡧࠪം"), None), bstack1ll1lll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨഃ"))
      bstack1111lll1ll_opy_.execute_script(bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬഄ") + json.dumps(str(args[0].name) + bstack1ll1lll_opy_ (u"ࠣࠢ࠰ࠤࡕࡧࡳࡴࡧࡧࠥࠧഅ")) + bstack1ll1lll_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧࢃࡽࠨആ"))
      if runner.driver_initialised == bstack1ll1lll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣഇ"):
        bstack1ll1lll1l_opy_(bstack1111lll1ll_opy_, bstack1ll1lll_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦഈ"))
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡶࡸࡪࡶ࠺ࠡࡽࢀࠫഉ").format(str(e)))
  bstack1lllll11ll_opy_(runner, name, context, args[0], bstack1111lllll_opy_, *args)
@measure(event_name=EVENTS.bstack11ll1ll1ll_opy_, stage=STAGE.bstack1111l1ll1_opy_, bstack1l1l1l11_opy_=SESSION_NAME)
def bstack11llll11l1_opy_(runner, name, context, bstack1111lllll_opy_, *args):
  bstack11l11111_opy_.end_test(args[0])
  try:
    bstack1l1l111l_opy_ = args[0].status.name
    bstack1111lll1ll_opy_ = bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬഊ"), context.browser)
    bstack1l11ll1l1_opy_.bstack11l1lll1l1_opy_(bstack1111lll1ll_opy_)
    if str(bstack1l1l111l_opy_).lower() in [bstack1ll1lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧഋ"), bstack1ll1lll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧഌ")]:
      bstack1l1l11l11l_opy_ = bstack1ll1lll_opy_ (u"ࠩࠪ഍")
      bstack1l1111l11l_opy_ = bstack1ll1lll_opy_ (u"ࠪࠫഎ")
      bstack1l1111l11_opy_ = bstack1ll1lll_opy_ (u"ࠫࠬഏ")
      try:
        import traceback
        bstack1l1l11l11l_opy_ = runner.exception.__class__.__name__
        bstack1111l11l1l_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1l1111l11l_opy_ = bstack1ll1lll_opy_ (u"ࠬࠦࠧഐ").join(bstack1111l11l1l_opy_)
        bstack1l1111l11_opy_ = bstack1111l11l1l_opy_[-1]
      except Exception as e:
        logger.debug(bstack111lllll_opy_.format(str(e)))
      bstack1l1l11l11l_opy_ += bstack1l1111l11_opy_
      playwright_annotate(context, json.dumps(str(args[0].name) + bstack1ll1lll_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧ഑") + str(bstack1l1111l11l_opy_)),
                          bstack1ll1lll_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨഒ"))
      if runner.driver_initialised == bstack1ll1lll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥഓ") or runner.driver_initialised == bstack1ll1lll_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩഔ"):
        bstack1ll1l1lll1_opy_(getattr(context, bstack1ll1lll_opy_ (u"ࠪࡴࡦ࡭ࡥࠨക"), None), bstack1ll1lll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦഖ"), bstack1l1l11l11l_opy_)
        bstack1111lll1ll_opy_.execute_script(bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪഗ") + json.dumps(str(args[0].name) + bstack1ll1lll_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧഘ") + str(bstack1l1111l11l_opy_)) + bstack1ll1lll_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦࢂࢃࠧങ"))
      if runner.driver_initialised == bstack1ll1lll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥച") or runner.driver_initialised == bstack1ll1lll_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩഛ"):
        bstack1ll1lll1l_opy_(bstack1111lll1ll_opy_, bstack1ll1lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪജ"), bstack1ll1lll_opy_ (u"ࠦࡘࡩࡥ࡯ࡣࡵ࡭ࡴࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࡢ࡮ࠣഝ") + str(bstack1l1l11l11l_opy_))
    else:
      playwright_annotate(context, bstack1ll1lll_opy_ (u"ࠧࡖࡡࡴࡵࡨࡨࠦࠨഞ"), bstack1ll1lll_opy_ (u"ࠨࡩ࡯ࡨࡲࠦട"))
      if runner.driver_initialised == bstack1ll1lll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤഠ") or runner.driver_initialised == bstack1ll1lll_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨഡ"):
        bstack1ll1l1lll1_opy_(getattr(context, bstack1ll1lll_opy_ (u"ࠩࡳࡥ࡬࡫ࠧഢ"), None), bstack1ll1lll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥണ"))
      bstack1111lll1ll_opy_.execute_script(bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩത") + json.dumps(str(args[0].name) + bstack1ll1lll_opy_ (u"ࠧࠦ࠭ࠡࡒࡤࡷࡸ࡫ࡤࠢࠤഥ")) + bstack1ll1lll_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤࢀࢁࠬദ"))
      if runner.driver_initialised == bstack1ll1lll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤധ") or runner.driver_initialised == bstack1ll1lll_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨന"):
        bstack1ll1lll1l_opy_(bstack1111lll1ll_opy_, bstack1ll1lll_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤഩ"))
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡯࡮ࠡࡣࡩࡸࡪࡸࠠࡧࡧࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬപ").format(str(e)))
  bstack1lllll11ll_opy_(runner, name, context, context.scenario, bstack1111lllll_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack11l11ll11_opy_(runner, name, context, bstack1111lllll_opy_, *args):
    target = context.scenario if hasattr(context, bstack1ll1lll_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ഫ")) else context.feature
    bstack1lllll11ll_opy_(runner, name, context, target, bstack1111lllll_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack11ll1l111l_opy_(runner, name, context, bstack1111lllll_opy_, *args):
    try:
      bstack1111lll1ll_opy_ = bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫബ"), context.browser)
      bstack1ll11111_opy_ = bstack1ll1lll_opy_ (u"࠭ࠧഭ")
      if context.failed is True:
        bstack1lll11llll_opy_ = []
        bstack1111lll1l_opy_ = []
        bstack1lll11l1_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack1lll11llll_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1111l11l1l_opy_ = traceback.format_tb(exc_tb)
            bstack11l11lll1_opy_ = bstack1ll1lll_opy_ (u"ࠧࠡࠩമ").join(bstack1111l11l1l_opy_)
            bstack1111lll1l_opy_.append(bstack11l11lll1_opy_)
            bstack1lll11l1_opy_.append(bstack1111l11l1l_opy_[-1])
        except Exception as e:
          logger.debug(bstack111lllll_opy_.format(str(e)))
        bstack1l1l11l11l_opy_ = bstack1ll1lll_opy_ (u"ࠨࠩയ")
        for i in range(len(bstack1lll11llll_opy_)):
          bstack1l1l11l11l_opy_ += bstack1lll11llll_opy_[i] + bstack1lll11l1_opy_[i] + bstack1ll1lll_opy_ (u"ࠩ࡟ࡲࠬര")
        bstack1ll11111_opy_ = bstack1ll1lll_opy_ (u"ࠪࠤࠬറ").join(bstack1111lll1l_opy_)
        if runner.driver_initialised in [bstack1ll1lll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠧല"), bstack1ll1lll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤള")]:
          playwright_annotate(context, bstack1ll11111_opy_, bstack1ll1lll_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧഴ"))
          bstack1ll1l1lll1_opy_(getattr(context, bstack1ll1lll_opy_ (u"ࠧࡱࡣࡪࡩࠬവ"), None), bstack1ll1lll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣശ"), bstack1l1l11l11l_opy_)
          bstack1111lll1ll_opy_.execute_script(bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧഷ") + json.dumps(bstack1ll11111_opy_) + bstack1ll1lll_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪസ"))
          bstack1ll1lll1l_opy_(bstack1111lll1ll_opy_, bstack1ll1lll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦഹ"), bstack1ll1lll_opy_ (u"࡙ࠧ࡯࡮ࡧࠣࡷࡨ࡫࡮ࡢࡴ࡬ࡳࡸࠦࡦࡢ࡫࡯ࡩࡩࡀࠠ࡝ࡰࠥഺ") + str(bstack1l1l11l11l_opy_))
          bstack1llllll1l_opy_ = bstack11lll1llll_opy_(bstack1ll11111_opy_, runner.feature.name, logger)
          if (bstack1llllll1l_opy_ != None):
            bstack11l11lll_opy_.append(bstack1llllll1l_opy_)
      else:
        if runner.driver_initialised in [bstack1ll1lll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫഻ࠢ"), bstack1ll1lll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯഼ࠦ")]:
          playwright_annotate(context, bstack1ll1lll_opy_ (u"ࠣࡈࡨࡥࡹࡻࡲࡦ࠼ࠣࠦഽ") + str(runner.feature.name) + bstack1ll1lll_opy_ (u"ࠤࠣࡴࡦࡹࡳࡦࡦࠤࠦാ"), bstack1ll1lll_opy_ (u"ࠥ࡭ࡳ࡬࡯ࠣി"))
          bstack1ll1l1lll1_opy_(getattr(context, bstack1ll1lll_opy_ (u"ࠫࡵࡧࡧࡦࠩീ"), None), bstack1ll1lll_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧു"))
          bstack1111lll1ll_opy_.execute_script(bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫൂ") + json.dumps(bstack1ll1lll_opy_ (u"ࠢࡇࡧࡤࡸࡺࡸࡥ࠻ࠢࠥൃ") + str(runner.feature.name) + bstack1ll1lll_opy_ (u"ࠣࠢࡳࡥࡸࡹࡥࡥࠣࠥൄ")) + bstack1ll1lll_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧࢃࡽࠨ൅"))
          bstack1ll1lll1l_opy_(bstack1111lll1ll_opy_, bstack1ll1lll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪെ"))
          bstack1llllll1l_opy_ = bstack11lll1llll_opy_(bstack1ll11111_opy_, runner.feature.name, logger)
          if (bstack1llllll1l_opy_ != None):
            bstack11l11lll_opy_.append(bstack1llllll1l_opy_)
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭േ").format(str(e)))
    bstack1lllll11ll_opy_(runner, name, context, context.feature, bstack1111lllll_opy_, *args)
@measure(event_name=EVENTS.bstack11111l1l_opy_, stage=STAGE.bstack1111l1ll1_opy_, hook_type=bstack1ll1lll_opy_ (u"ࠧࡧࡦࡵࡧࡵࡅࡱࡲࠢൈ"), bstack1l1l1l11_opy_=SESSION_NAME)
def bstack11lll1ll11_opy_(runner, name, context, bstack1111lllll_opy_, *args):
    bstack1lllll11ll_opy_(runner, name, context, runner, bstack1111lllll_opy_, *args)
def bstack111lll11ll_opy_(self, filename=None):
  global bstack11111111l1_opy_
  bstack11111111l1_opy_(self, filename)
  bstack1l1l1111l_opy_ = []
  bstack1llll1111l_opy_ = [bstack1ll1lll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠧ൉"), bstack1ll1lll_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡵࡣࡪࠫൊ"), bstack1ll1lll_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪോ"), bstack1ll1lll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪൌ"), bstack1ll1lll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡷࡥ࡬്࠭"), bstack1ll1lll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫൎ")]
  bstack1l11ll1lll_opy_ = lambda *_: None
  for hook_name in bstack1llll1111l_opy_:
    if hook_name not in self.hooks:
      self.hooks[hook_name] = bstack1l11ll1lll_opy_
      bstack1l1l1111l_opy_.append(hook_name)
  if bstack1l1l1111l_opy_:
    os.environ[bstack1ll1lll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤ࡙ࡄࡌࡡࡇࡉࡋࡇࡕࡍࡖࡢࡌࡔࡕࡋࡔࠩ൏")] = bstack1ll1lll_opy_ (u"࠭ࠬࠨ൐").join(bstack1l1l1111l_opy_)
def _execute_deferred_playwright_close():
  try:
    _1lll1l1lll_opy_ = threading.current_thread()
    _1ll1lllll1_opy_ = getattr(_1lll1l1lll_opy_, bstack1ll1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡥࡧࡩࡩࡷࡸࡥࡥࡡࡳࡥ࡬࡫࡟ࡳࡧࡩࠫ൑"), None)
    _11llll11l_opy_ = getattr(_1lll1l1lll_opy_, bstack1ll1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡦࡨࡪࡪࡸࡲࡦࡦࡢࡦࡷࡵࡷࡴࡧࡵࡣࡷ࡫ࡦࠨ൒"), None)
    _1l111l11_opy_ = getattr(_1lll1l1lll_opy_, bstack1ll1lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡧࡩ࡫࡫ࡲࡳࡧࡧࡣࡵࡽ࡟ࡴࡶࡲࡴࡤ࡬࡮ࠨ൓"), None)
    _wrapper = getattr(_1lll1l1lll_opy_, bstack1ll1lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩൔ"), None)
    if not _11llll11l_opy_ and _wrapper and hasattr(_wrapper, bstack1ll1lll_opy_ (u"ࠫࡤࡨࡲࡰࡹࡶࡩࡷ࠭ൕ")):
      _11llll11l_opy_ = _wrapper._browser
    if not _1ll1lllll1_opy_ and _wrapper and hasattr(_wrapper, bstack1ll1lll_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫൖ")):
      _1ll1lllll1_opy_ = _wrapper._page
    if not _1l111l11_opy_:
      _1lll111111_opy_ = getattr(_1lll1l1lll_opy_, bstack1ll1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡤࡦࡨࡨࡶࡷ࡫ࡤࡠࡲࡺࡣࡷ࡫ࡦࠨൗ"), None)
      if _1lll111111_opy_ and hasattr(_1lll111111_opy_, bstack1ll1lll_opy_ (u"ࠧࡴࡶࡲࡴࠬ൘")):
        _1l111l11_opy_ = _1lll111111_opy_.stop
    _1111ll1111_opy_ = _1ll1lllll1_opy_ or _11llll11l_opy_ or _1l111l11_opy_
    if not _1111ll1111_opy_:
      return
    if _1ll1lllll1_opy_ and hasattr(_1ll1lllll1_opy_, bstack1ll1lll_opy_ (u"ࠨࡥ࡯ࡳࡸ࡫ࠧ൙")):
      try:
        _1ll1lllll1_opy_.close(_bstack_sdk_close=True)
      except TypeError:
        try:
          _1ll1lllll1_opy_.close()
        except Exception:
          pass
      except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠩࡇࡩ࡫࡫ࡲࡳࡧࡧࠤࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡲࡤ࡫ࡪ࠴ࡣ࡭ࡱࡶࡩࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡾࠩ൚").format(str(e)))
    if _11llll11l_opy_ and hasattr(_11llll11l_opy_, bstack1ll1lll_opy_ (u"ࠪࡧࡱࡵࡳࡦࠩ൛")):
      try:
        _11llll11l_opy_.close(_bstack_sdk_close=True)
      except TypeError:
        try:
          _11llll11l_opy_.close()
        except Exception:
          pass
      except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠫࡉ࡫ࡦࡦࡴࡵࡩࡩࠦࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡦࡷࡵࡷࡴࡧࡵ࠲ࡨࡲ࡯ࡴࡧࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࢀࢃࠧ൜").format(str(e)))
    if _1l111l11_opy_:
      try:
        _1l111l11_opy_(_bstack_sdk_close=True)
      except TypeError:
        try:
          _1l111l11_opy_()
        except Exception:
          pass
      except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠬࡊࡥࡧࡧࡵࡶࡪࡪࠠࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸࡺ࡯ࡱࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡿࢂ࠭൝").format(str(e)))
    for attr in (bstack1ll1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡤࡦࡨࡨࡶࡷ࡫ࡤࡠࡲࡤ࡫ࡪࡥࡣ࡭ࡱࡶࡩࠬ൞"), bstack1ll1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡥࡧࡩࡩࡷࡸࡥࡥࡡࡳࡥ࡬࡫࡟ࡳࡧࡩࠫൟ"),
                 bstack1ll1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡦࡨࡪࡪࡸࡲࡦࡦࡢࡦࡷࡵࡷࡴࡧࡵࡣࡨࡲ࡯ࡴࡧࠪൠ"), bstack1ll1lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡧࡩ࡫࡫ࡲࡳࡧࡧࡣࡧࡸ࡯ࡸࡵࡨࡶࡤࡸࡥࡧࠩൡ"),
                 bstack1ll1lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡨࡪ࡬ࡥࡳࡴࡨࡨࡤࡶࡷࡠࡵࡷࡳࡵ࠭ൢ"), bstack1ll1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡩ࡫ࡦࡦࡴࡵࡩࡩࡥࡰࡸࡡࡶࡸࡴࡶ࡟ࡧࡰࠪൣ"),
                 bstack1ll1lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡪࡥࡧࡧࡵࡶࡪࡪ࡟ࡱࡹࡢࡶࡪ࡬ࠧ൤")):
      try:
        delattr(_1lll1l1lll_opy_, attr)
      except AttributeError:
        pass
    if _wrapper:
      try:
        _wrapper._page = None
        _wrapper._browser = None
      except Exception:
        pass
    logger.debug(bstack1ll1lll_opy_ (u"࠭ࡄࡦࡨࡨࡶࡷ࡫ࡤࠡࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡩ࡬ࡰࡵࡨࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࡪࠠࡧࡱࡵࠤࡹ࡮ࡲࡦࡣࡧࠤࢀࢃࠧ൥").format(_1lll1l1lll_opy_.ident))
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠧࡅࡧࡩࡩࡷࡸࡥࡥࠢࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡣ࡭ࡱࡶࡩࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡾࠩ൦").format(str(e)))
def bstack1l1llll11_opy_(self, name, *args):
  global bstack1111lllll_opy_
  global bstack11111l11ll_opy_
  try:
    if BROWSERSTACK_AUTOMATION:
      platform_index = int(threading.current_thread()._name) % bstack11ll1l11_opy_
      bstack1ll11l11l1_opy_ = CONFIG[bstack1ll1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ൧")][platform_index]
      os.environ[bstack1ll1lll_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪ൨")] = json.dumps(bstack1ll11l11l1_opy_)
    if not hasattr(self, bstack1ll1lll_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡸ࡫ࡤࠨ൩")):
      self.driver_initialised = None
    bstack111llll1ll_opy_ = {
        bstack1ll1lll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠨ൪"): bstack1l1l1111ll_opy_,
        bstack1ll1lll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭൫"): bstack1l1lll111_opy_,
        bstack1ll1lll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡴࡢࡩࠪ൬"): bstack1l111lll1_opy_,
        bstack1ll1lll_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩ൭"): bstack1l11ll11_opy_,
        bstack1ll1lll_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵ࠭൮"): bstack111l1l1l_opy_,
        bstack1ll1lll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡷࡩࡵ࠭൯"): bstack1l1l11llll_opy_,
        bstack1ll1lll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ൰"): bstack11llll11l1_opy_,
        bstack1ll1lll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡸࡦ࡭ࠧ൱"): bstack11l11ll11_opy_,
        bstack1ll1lll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬ൲"): bstack11ll1l111l_opy_,
        bstack1ll1lll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠩ൳"): bstack11lll1ll11_opy_
    }
    handler = bstack111llll1ll_opy_.get(name, bstack1111lllll_opy_)
    try:
      if args:
        context = args[0]
        remaining_args = args[1:]
        if bstack11111l11ll_opy_ is None or not bstack11111l11ll_opy_:
          context = self.context
          remaining_args = args
      else:
        context = self.context
        remaining_args = ()
      handler(self, name, context, bstack1111lllll_opy_, *remaining_args)
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡥࡩ࡭ࡧࡶࡦࠢ࡫ࡳࡴࡱࠠࡩࡣࡱࡨࡱ࡫ࡲࠡࡽࢀ࠾ࠥࢁࡽࠨ൴").format(name, str(e)))
    if name == bstack1ll1lll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩ൵"):
      _execute_deferred_playwright_close()
    if name in [bstack1ll1lll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠩ൶"), bstack1ll1lll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ൷"), bstack1ll1lll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡥࡱࡲࠧ൸")]:
      try:
        bstack1111lll1ll_opy_ = threading.current_thread().bstackSessionDriver if bstack1l11ll1111_opy_(bstack1ll1lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ൹")) else context.browser
        bstack11l1lll11l_opy_ = (
          (name == bstack1ll1lll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠩൺ") and self.driver_initialised == bstack1ll1lll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦൻ")) or
          (name == bstack1ll1lll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨർ") and self.driver_initialised == bstack1ll1lll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠥൽ")) or
          (name == bstack1ll1lll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫൾ") and self.driver_initialised in [bstack1ll1lll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨൿ"), bstack1ll1lll_opy_ (u"ࠧ࡯࡮ࡴࡶࡨࡴࠧ඀")]) or
          (name == bstack1ll1lll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡴࡦࡲࠪඁ") and self.driver_initialised == bstack1ll1lll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧං"))
        )
        if bstack11l1lll11l_opy_:
          self.driver_initialised = None
          if bstack1111lll1ll_opy_ and hasattr(bstack1111lll1ll_opy_, bstack1ll1lll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠬඃ")):
            try:
              bstack1111lll1ll_opy_.quit()
            except Exception as e:
              logger.debug(bstack1ll1lll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡳࡸ࡭ࡹࡺࡩ࡯ࡩࠣࡨࡷ࡯ࡶࡦࡴࠣ࡭ࡳࠦࡢࡦࡪࡤࡺࡪࠦࡨࡰࡱ࡮࠾ࠥࢁࡽࠨ඄").format(str(e)))
      except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡭ࡵ࡯࡬ࠢࡦࡰࡪࡧ࡮ࡶࡲࠣࡪࡴࡸࠠࡼࡿ࠽ࠤࢀࢃࠧඅ").format(name, str(e)))
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠫࡈࡸࡩࡵ࡫ࡦࡥࡱࠦࡥࡳࡴࡲࡶࠥ࡯࡮ࠡࡤࡨ࡬ࡦࡼࡥࠡࡴࡸࡲࠥ࡮࡯ࡰ࡭ࠣࡿࢂࡀࠠࡼࡿࠪආ").format(name, str(e)))
    try:
      if bstack11111l11ll_opy_ is None or bstack11111l11ll_opy_:
        try:
          bstack1111lllll_opy_(self, name, self.context, *args)
        except TypeError:
          bstack1111lllll_opy_(self, name, *args)
      else:
        bstack1111lllll_opy_(self, name, *args)
    except Exception as e2:
      logger.debug(bstack1ll1lll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡲࡶ࡮࡭ࡩ࡯ࡣ࡯ࠤࡧ࡫ࡨࡢࡸࡨࠤ࡭ࡵ࡯࡬ࠢࡾࢁ࠿ࠦࡻࡾࠩඇ").format(name, str(e2)))
  finally:
    if name == bstack1ll1lll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧඈ"):
      _execute_deferred_playwright_close()
def bstack11lll11l1l_opy_(config, startdir):
  return bstack1ll1lll_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࠳ࢁࠧඉ").format(bstack1ll1lll_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢඊ"))
notset = Notset()
def bstack1l1111lll_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1ll1llll11_opy_
  if str(name).lower() == bstack1ll1lll_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࠩඋ"):
    return bstack1ll1lll_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤඌ")
  else:
    return bstack1ll1llll11_opy_(self, name, default, skip)
def bstack1ll11l1ll1_opy_(item, when):
  global bstack11lll11l11_opy_
  try:
    bstack11lll11l11_opy_(item, when)
  except Exception as e:
    pass
def bstack1ll11l1111_opy_():
  return
def browserstack_executor_helper(type, name, status, reason, bstack11l111l1l1_opy_, bstack111llll111_opy_):
  bstack1ll1lll111_opy_ = {
    bstack1ll1lll_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫඍ"): type,
    bstack1ll1lll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨඎ"): {}
  }
  if type == bstack1ll1lll_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨඏ"):
    bstack1ll1lll111_opy_[bstack1ll1lll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪඐ")][bstack1ll1lll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧඑ")] = bstack11l111l1l1_opy_
    bstack1ll1lll111_opy_[bstack1ll1lll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬඒ")][bstack1ll1lll_opy_ (u"ࠪࡨࡦࡺࡡࠨඓ")] = json.dumps(str(bstack111llll111_opy_))
  if type == bstack1ll1lll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬඔ"):
    bstack1ll1lll111_opy_[bstack1ll1lll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨඕ")][bstack1ll1lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫඖ")] = name
  if type == bstack1ll1lll_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪ඗"):
    bstack1ll1lll111_opy_[bstack1ll1lll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ඘")][bstack1ll1lll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ඙")] = status
    if status == bstack1ll1lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪක"):
      bstack1ll1lll111_opy_[bstack1ll1lll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧඛ")][bstack1ll1lll_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬග")] = json.dumps(str(reason))
  bstack11l111llll_opy_ = bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫඝ").format(json.dumps(bstack1ll1lll111_opy_))
  return bstack11l111llll_opy_
def bstack11l11l1l11_opy_(driver_command, response):
    if driver_command == bstack1ll1lll_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫඞ"):
        TestHubHandler.bstack1111ll1lll_opy_({
            bstack1ll1lll_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧඟ"): response[bstack1ll1lll_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨච")],
            bstack1ll1lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪඡ"): TestHubHandler.current_test_uuid()
        })
def bstack1l1l1l1l11_opy_(item, call, rep):
  global bstack1l1lll1l_opy_
  global bstack11ll1llll_opy_
  global bstack1ll11l1l_opy_
  name = bstack1ll1lll_opy_ (u"ࠫࠬජ")
  try:
    if rep.when == bstack1ll1lll_opy_ (u"ࠬࡩࡡ࡭࡮ࠪඣ"):
      bstack1lllll1ll1_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1ll11l1l_opy_:
          name = str(rep.nodeid)
          executor_string = browserstack_executor_helper(bstack1ll1lll_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧඤ"), name, bstack1ll1lll_opy_ (u"ࠧࠨඥ"), bstack1ll1lll_opy_ (u"ࠨࠩඦ"), bstack1ll1lll_opy_ (u"ࠩࠪට"), bstack1ll1lll_opy_ (u"ࠪࠫඨ"))
          threading.current_thread().bstack1ll1l11lll_opy_ = name
          for driver in bstack11ll1llll_opy_:
            if bstack1lllll1ll1_opy_ == driver.session_id:
              driver.execute_script(executor_string)
      except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫඩ").format(str(e)))
      try:
        bstack1ll1l11ll_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack1ll1lll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ඪ"):
          status = bstack1ll1lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ණ") if rep.outcome.lower() == bstack1ll1lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧඬ") else bstack1ll1lll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨත")
          reason = bstack1ll1lll_opy_ (u"ࠩࠪථ")
          if status == bstack1ll1lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪද"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack1ll1lll_opy_ (u"ࠫ࡮ࡴࡦࡰࠩධ") if status == bstack1ll1lll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬන") else bstack1ll1lll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ඲")
          data = name + bstack1ll1lll_opy_ (u"ࠧࠡࡲࡤࡷࡸ࡫ࡤࠢࠩඳ") if status == bstack1ll1lll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨප") else name + bstack1ll1lll_opy_ (u"ࠩࠣࡪࡦ࡯࡬ࡦࡦࠤࠤࠬඵ") + reason
          bstack1l11ll111_opy_ = browserstack_executor_helper(bstack1ll1lll_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬබ"), bstack1ll1lll_opy_ (u"ࠫࠬභ"), bstack1ll1lll_opy_ (u"ࠬ࠭ම"), bstack1ll1lll_opy_ (u"࠭ࠧඹ"), level, data)
          for driver in bstack11ll1llll_opy_:
            if bstack1lllll1ll1_opy_ == driver.session_id:
              driver.execute_script(bstack1l11ll111_opy_)
      except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡨࡵ࡮ࡵࡧࡻࡸࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫය").format(str(e)))
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡸࡺࡡࡵࡧࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾࢁࠬර").format(str(e)))
  bstack1l1lll1l_opy_(item, call, rep)
def bstack1l11l11l11_opy_(driver, bstack11l1llll1l_opy_, test=None):
  global PLATFORM_INDEX
  if test != None:
    bstack11l11ll1l1_opy_ = getattr(test, bstack1ll1lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ඼"), None)
    bstack1ll1l11ll1_opy_ = getattr(test, bstack1ll1lll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨල"), None)
    PercySDK.screenshot(driver, bstack11l1llll1l_opy_, bstack11l11ll1l1_opy_=bstack11l11ll1l1_opy_, bstack1ll1l11ll1_opy_=bstack1ll1l11ll1_opy_, bstack11lll1l1ll_opy_=PLATFORM_INDEX)
  else:
    PercySDK.screenshot(driver, bstack11l1llll1l_opy_)
@measure(event_name=EVENTS.bstack11llll1111_opy_, stage=STAGE.bstack1111l1ll1_opy_, bstack1l1l1l11_opy_=SESSION_NAME)
def bstack11111l1111_opy_(driver):
  if bstack1l111ll1l_opy_.bstack1111lll11_opy_() is True or bstack1l111ll1l_opy_.capturing() is True:
    return
  bstack1l111ll1l_opy_.bstack11lll111l_opy_()
  while not bstack1l111ll1l_opy_.bstack1111lll11_opy_():
    bstack111l111l11_opy_ = bstack1l111ll1l_opy_.bstack11l1ll1l1_opy_()
    bstack1l11l11l11_opy_(driver, bstack111l111l11_opy_)
  bstack1l111ll1l_opy_.bstack1llll11l11_opy_()
def bstack1111lllll1_opy_(sequence, driver_command, response = None, bstack11111l1ll1_opy_ = None, args = None):
    try:
      if sequence != bstack1ll1lll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫ඾"):
        return
      if percy.bstack11l1l1lll_opy_() == bstack1ll1lll_opy_ (u"ࠧ࡬ࡡ࡭ࡵࡨࠦ඿"):
        return
      bstack111l111l11_opy_ = bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"࠭ࡰࡦࡴࡦࡽࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩව"), None)
      for command in bstack11ll1ll11_opy_:
        if command == driver_command:
          with bstack1l1l1ll1l_opy_:
            bstack111111lll1_opy_ = bstack11ll1llll_opy_.copy()
          for driver in bstack111111lll1_opy_:
            bstack11111l1111_opy_(driver)
      bstack1llll1l1_opy_ = percy.bstack1ll1lllll_opy_()
      if driver_command in bstack1l111lll1l_opy_[bstack1llll1l1_opy_]:
        bstack1l111ll1l_opy_.bstack1lll1lll_opy_(bstack111l111l11_opy_, driver_command)
    except Exception as e:
      pass
_1ll111ll1_opy_ = threading.Event()
def bstack1l11111l11_opy_(framework_name):
  if global_config.get_property(bstack1ll1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟࡮ࡱࡧࡣࡨࡧ࡬࡭ࡧࡧࠫශ")):
      _1ll111ll1_opy_.wait(timeout=30)
      return
  global_config.bstack1l1ll1llll_opy_(bstack1ll1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬෂ"), True)
  global FRAMEWORK_NAME
  global SELENIUM_OR_PLAYWRIGHT_INSTALLED
  global bstack111ll11l1l_opy_
  FRAMEWORK_NAME = framework_name
  logger.info(bstack1llll111_opy_.format(FRAMEWORK_NAME.split(bstack1ll1lll_opy_ (u"ࠩ࠰ࠫස"))[0]))
  bstack1111lll11l_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    global bstack111l1ll1l_opy_
    bstack1llll1l11_opy_ = BROWSERSTACK_AUTOMATION or bstack111l1ll1l_opy_
    if bstack1llll1l11_opy_:
      Service.start = bstack1llll11l_opy_
      Service.stop = bstack1l1l1l11l1_opy_
      webdriver.Remote.get = bstack11ll1lll_opy_
      WebDriver.quit = bstack1l1111l1l_opy_
      webdriver.Remote.__init__ = bstack1111l111l_opy_
    if not BROWSERSTACK_AUTOMATION and not bstack111l1ll1l_opy_:
        webdriver.Remote.__init__ = bstack11lll1l11l_opy_
    WebDriver.getAccessibilityResults = getAccessibilityResults
    WebDriver.get_accessibility_results = getAccessibilityResults
    WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
    WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
    WebDriver.performScan = perform_scan
    WebDriver.perform_scan = perform_scan
    WebDriver.execute = bstack11l1ll1ll1_opy_
    SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
  except Exception as e:
    pass
  try:
    bstack1llll1l11_opy_ = BROWSERSTACK_AUTOMATION or bstack111l1ll1l_opy_
    if bstack1llll1l11_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack11ll1l1lll_opy_
  except Exception as e:
    pass
  try:
    set_playwright_globals(
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
    logger.debug(bstack1ll1lll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡨ࡮ࡲࡦࡦࡲࡳ࠻ࠢࡾࢁࠧහ").format(str(e)))
  patch_playwright()
  if not SELENIUM_OR_PLAYWRIGHT_INSTALLED:
    bstack11l1l111ll_opy_(bstack1ll1lll_opy_ (u"ࠦࡕࡧࡣ࡬ࡣࡪࡩࡸࠦ࡮ࡰࡶࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠨළ"), bstack1l11l1l11_opy_)
  if bstack111l1lll1l_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      if hasattr(RemoteConnection, bstack1ll1lll_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭ෆ")) and callable(getattr(RemoteConnection, bstack1ll1lll_opy_ (u"࠭࡟ࡨࡧࡷࡣࡵࡸ࡯ࡹࡻࡢࡹࡷࡲࠧ෇"))):
        RemoteConnection._get_proxy_url = bstack1l1111111l_opy_
      else:
        from selenium.webdriver.remote.client_config import ClientConfig
        ClientConfig.get_proxy_url = bstack1l1111111l_opy_
    except Exception as e:
      logger.error(bstack11l1l1l1l1_opy_.format(str(e)))
  if bstack1111ll1l11_opy_():
    bstack1llllll11l_opy_(CONFIG, logger)
  if (bstack1ll1lll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭෈") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      try:
        from pabot.pabot import QueueItem
        from pabot import pabot
      except Exception as e:
        logger.warning(bstack11llll111_opy_ + str(e))
      if not is_robot_playwright_installed():
        try:
          if percy.bstack11l1l1lll_opy_() == bstack1ll1lll_opy_ (u"ࠣࡶࡵࡹࡪࠨ෉"):
            bstack1ll1ll1ll_opy_(bstack1111lllll1_opy_)
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
          WebDriverCreator._get_ff_profile = bstack1lllll111_opy_
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
          WebDriverCache.close = bstack1ll111l1l_opy_
        except Exception as e:
          logger.warning(bstack111ll1l1l_opy_ + str(e))
        try:
          from AppiumLibrary.utils.applicationcache import ApplicationCache
          ApplicationCache.close = bstack11l1lll11_opy_
        except Exception as e:
          logger.debug(bstack111111l11l_opy_ + str(e))
    except Exception as e:
      bstack11l1l111ll_opy_(e, bstack111ll1l1l_opy_)
    Output.start_test = bstack1ll1llll_opy_
    Output.end_test = bstack1ll1lll1_opy_
    TestStatus.__init__ = bstack1l11l1111l_opy_
    QueueItem.__init__ = bstack1l1ll1l11_opy_
    pabot._create_items = bstack1llll11ll_opy_
    try:
      from pabot import __version__ as bstack1lllll1111_opy_
      if version.parse(bstack1lllll1111_opy_) >= version.parse(bstack1ll1lll_opy_ (u"ࠩ࠸࠲࠵࠴࠰ࠨ්")):
        pabot._run = bstack1l1ll1lll1_opy_
      elif version.parse(bstack1lllll1111_opy_) >= version.parse(bstack1ll1lll_opy_ (u"ࠪ࠸࠳࠸࠮࠱ࠩ෋")):
        pabot._run = bstack1l111l1ll_opy_
      elif version.parse(bstack1lllll1111_opy_) >= version.parse(bstack1ll1lll_opy_ (u"ࠫ࠷࠴࠱࠶࠰࠳ࠫ෌")):
        pabot._run = bstack1llllll1ll_opy_
      elif version.parse(bstack1lllll1111_opy_) >= version.parse(bstack1ll1lll_opy_ (u"ࠬ࠸࠮࠲࠵࠱࠴ࠬ෍")):
        pabot._run = bstack1l1l1l1ll1_opy_
      else:
        pabot._run = bstack1llll111l_opy_
    except Exception as e:
      pabot._run = bstack1llll111l_opy_
    pabot._create_command_for_execution = bstack1lll11lll_opy_
    pabot._report_results = bstack1lll11l11_opy_
  if bstack1ll1lll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭෎") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11l1l111ll_opy_(e, bstack11lll1l11_opy_)
    Runner.run_hook = bstack1l1llll11_opy_
    try:
      from behave import __version__ as bstack11l1ll111l_opy_
      if version.parse(bstack11l1ll111l_opy_) >= version.parse(bstack1ll1lll_opy_ (u"ࠧ࠲࠰࠶࠲࠵࠭ා")):
        Runner.load_hooks = bstack111lll11ll_opy_
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"ࠨࡅࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡷࡧࡵࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬැ").format(str(e)))
    Step.run = bstack11llll11ll_opy_
  if bstack1ll1lll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩෑ") in str(framework_name).lower():
    if not BROWSERSTACK_AUTOMATION:
      _1ll111ll1_opy_.set()
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack11lll11l1l_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1ll11l1111_opy_
      Config.getoption = bstack1l1111lll_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1l1l1l1l11_opy_
    except Exception as e:
      pass
  _1ll111ll1_opy_.set()
def bstack111ll1l11l_opy_():
  global CONFIG
  if bstack1ll1lll_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪි") in CONFIG and int(CONFIG[bstack1ll1lll_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫී")]) > 1:
    logger.warning(bstack1lll1lll1l_opy_)
def bstack11ll1l1ll1_opy_(arg, bstack11lllllll_opy_, bstack1l1l111l1_opy_=None):
  global CONFIG
  global bstack1l11ll1ll_opy_
  global bstack111l11l11_opy_
  global BROWSERSTACK_AUTOMATION
  global bstack111l1ll1l_opy_
  global global_config
  bstack1ll11ll1l_opy_ = bstack1ll1lll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬු")
  if bstack11lllllll_opy_ and isinstance(bstack11lllllll_opy_, str):
    bstack11lllllll_opy_ = eval(bstack11lllllll_opy_)
  CONFIG = bstack11lllllll_opy_[bstack1ll1lll_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭෕")]
  bstack1l11ll1ll_opy_ = bstack11lllllll_opy_[bstack1ll1lll_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨූ")]
  bstack111l11l11_opy_ = bstack11lllllll_opy_[bstack1ll1lll_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ෗")]
  BROWSERSTACK_AUTOMATION = bstack11lllllll_opy_[bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬෘ")]
  try:
    bstack1l1lll11_opy_ = bstack11lllllll_opy_.get(bstack1ll1lll_opy_ (u"ࠪࡓ࡛ࡋࡒࡓࡋࡇࡉࡤࡒࡏࡂࡆࡢࡘࡊ࡙ࡔࡊࡐࡊࠫෙ"), False)
    bstack111l1ll1l_opy_ = bool(bstack1l1lll11_opy_)
    os.environ[bstack1ll1lll_opy_ (u"ࠫࡔ࡜ࡅࡓࡔࡌࡈࡊࡥࡌࡐࡃࡇࡣ࡙ࡋࡓࡕࡋࡑࡋࠬේ")] = str(bstack111l1ll1l_opy_).lower()
  except Exception as e:
    logger.error(bstack1ll1lll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡒ࡚ࡊࡘࡒࡊࡆࡈࡣࡑࡕࡁࡅࡡࡗࡉࡘ࡚ࡉࡏࡉ࠽ࠤࢀࢃࠢෛ").format(e))
    bstack111l1ll1l_opy_ = False
    os.environ[bstack1ll1lll_opy_ (u"࠭ࡏࡗࡇࡕࡖࡎࡊࡅࡠࡎࡒࡅࡉࡥࡔࡆࡕࡗࡍࡓࡍࠧො")] = bstack1ll1lll_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ෝ")
  global_config.bstack1l1ll1llll_opy_(bstack1ll1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩෞ"), BROWSERSTACK_AUTOMATION)
  os.environ[bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫෟ")] = bstack1ll11ll1l_opy_
  os.environ[bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠩ෠")] = json.dumps(CONFIG)
  os.environ[bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡌ࡚ࡈ࡟ࡖࡔࡏࠫ෡")] = bstack1l11ll1ll_opy_
  os.environ[bstack1ll1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭෢")] = str(bstack111l11l11_opy_)
  os.environ[bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡌࡖࡉࡌࡒࠬ෣")] = str(True)
  if bstack1l1111llll_opy_(arg, [bstack1ll1lll_opy_ (u"ࠧ࠮ࡰࠪ෤"), bstack1ll1lll_opy_ (u"ࠨ࠯࠰ࡲࡺࡳࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩ෥")]) != -1:
    os.environ[bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡄࡖࡆࡒࡌࡆࡎࠪ෦")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1111l1l11l_opy_)
    return
  bstack11l11l1ll1_opy_()
  global bstack1ll1ll11_opy_
  global PLATFORM_INDEX
  global bstack1l1l11111_opy_
  global bstack1l11l111_opy_
  global bstack11lll1ll1_opy_
  global bstack111ll11l1l_opy_
  global PARALLELISE_VANILLA_PYTHON
  arg.append(bstack1ll1lll_opy_ (u"ࠥ࠱࡜ࠨ෧"))
  arg.append(bstack1ll1lll_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨ࠾ࡒࡵࡤࡶ࡮ࡨࠤࡦࡲࡲࡦࡣࡧࡽࠥ࡯࡭ࡱࡱࡵࡸࡪࡪ࠺ࡱࡻࡷࡩࡸࡺ࠮ࡑࡻࡷࡩࡸࡺࡗࡢࡴࡱ࡭ࡳ࡭ࠢ෨"))
  arg.append(bstack1ll1lll_opy_ (u"ࠧ࠳ࡗࠣ෩"))
  arg.append(bstack1ll1lll_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡀࡔࡩࡧࠣ࡬ࡴࡵ࡫ࡪ࡯ࡳࡰࠧ෪"))
  global bstack1l1ll11l_opy_
  global bstack1l1l1l111_opy_
  global bstack1l11lll1l1_opy_
  global bstack1111l11l11_opy_
  global bstack11l111lll1_opy_
  global bstack1lllll1lll_opy_
  global bstack1111111l1l_opy_
  global bstack1l11111ll_opy_
  global bstack1l111lll11_opy_
  global bstack111l11lll1_opy_
  global bstack1ll1llll11_opy_
  global bstack11lll11l11_opy_
  global bstack1l1lll1l_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l1ll11l_opy_ = webdriver.Remote.__init__
    bstack1l1l1l111_opy_ = WebDriver.quit
    bstack1l11111ll_opy_ = WebDriver.close
    bstack1l111lll11_opy_ = WebDriver.get
    bstack1l11lll1l1_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack111111l11_opy_(CONFIG) and bstack1lllllll1l_opy_():
    if bstack1l1l11l1l1_opy_() < version.parse(bstack1lll1ll11l_opy_):
      logger.error(bstack1111llllll_opy_.format(bstack1l1l11l1l1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack1ll1lll_opy_ (u"ࠧࡠࡩࡨࡸࡤࡶࡲࡰࡺࡼࡣࡺࡸ࡬ࠨ෫")) and callable(getattr(RemoteConnection, bstack1ll1lll_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩ෬"))):
          bstack111l11lll1_opy_ = RemoteConnection._get_proxy_url
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          bstack111l11lll1_opy_ = ClientConfig.get_proxy_url
      except Exception as e:
        logger.error(bstack11l1l1l1l1_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1ll1llll11_opy_ = Config.getoption
    from _pytest import runner
    bstack11lll11l11_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warning(bstack1ll1lll_opy_ (u"ࠤࠨࡷ࠿ࠦࠥࡴࠤ෭"), bstack111llllll_opy_, str(e))
  try:
    from pytest_bdd import reporting
    bstack1l1lll1l_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡲࠤࡷࡻ࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࡶࠫ෮"))
  if cli.is_enabled(CONFIG) and cli.config:
    bstack1l1l11111_opy_ = cli.config.get(bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ෯"), {}).get(bstack1ll1lll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ෰"))
  else:
    bstack1l1l11111_opy_ = CONFIG.get(bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ෱"), {}).get(bstack1ll1lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩෲ"))
  PARALLELISE_VANILLA_PYTHON = True
  if cli.is_enabled(CONFIG):
    if cli.bstack1l11lll1l_opy_():
      bstack11llllll11_opy_.invoke(Events.CONNECT, bstack1l1llll1_opy_())
    platform_index = int(os.environ.get(bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨෳ"), bstack1ll1lll_opy_ (u"ࠩ࠳ࠫ෴")))
  else:
    bstack1l11111l11_opy_(bstack1l1ll11111_opy_)
  os.environ[bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫ෵")] = CONFIG[bstack1ll1lll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭෶")]
  os.environ[bstack1ll1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨ෷")] = CONFIG[bstack1ll1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ෸")]
  os.environ[bstack1ll1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪ෹")] = BROWSERSTACK_AUTOMATION.__str__()
  from _pytest.config import main as bstack11l111111_opy_
  bstack1l1l1ll11l_opy_ = []
  try:
    exit_code = bstack11l111111_opy_(arg)
    if cli.is_enabled(CONFIG):
      cli.bstack11llllll1_opy_()
    if bstack1ll1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬ෺") in multiprocessing.current_process().__dict__.keys():
      for bstack1lll1l1ll1_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1l1l1ll11l_opy_.append(bstack1lll1l1ll1_opy_)
    try:
      bstack11l11l1lll_opy_ = (bstack1l1l1ll11l_opy_, int(exit_code))
      bstack1l1l111l1_opy_.append(bstack11l11l1lll_opy_)
    except:
      bstack1l1l111l1_opy_.append((bstack1l1l1ll11l_opy_, exit_code))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack1l1l1ll11l_opy_.append({bstack1ll1lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ෻"): bstack1ll1lll_opy_ (u"ࠪࡔࡷࡵࡣࡦࡵࡶࠤࠬ෼") + os.environ.get(bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ෽")), bstack1ll1lll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ෾"): traceback.format_exc(), bstack1ll1lll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ෿"): int(os.environ.get(bstack1ll1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ฀")))})
    bstack1l1l111l1_opy_.append((bstack1l1l1ll11l_opy_, 1))
def mod_behave_main(args, retries):
  try:
    from behave.configuration import Configuration
    from behave.__main__ import run_behave
    from browserstack_sdk.bstack_behave_runner import BehaveRunner
    config = Configuration(args)
    config.update_userdata({bstack1ll1lll_opy_ (u"ࠣࡴࡨࡸࡷ࡯ࡥࡴࠤก"): str(retries)})
    return run_behave(config, runner_class=BehaveRunner)
  except Exception as e:
    bstack1ll1ll111l_opy_ = e.__class__.__name__
    print(bstack1ll1lll_opy_ (u"ࠤࠨࡷ࠿ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡢࡦࡪࡤࡺࡪࠦࡴࡦࡵࡷࠤࠪࡹࠢข") % (bstack1ll1ll111l_opy_, e))
    return 1
def bstack11ll11ll1_opy_(arg):
  global bstack1111111l_opy_
  bstack1l11111l11_opy_(bstack1lllllll11_opy_)
  os.environ[bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫฃ")] = str(bstack111l11l11_opy_)
  retries = bstack1l111111l1_opy_.bstack1ll111111_opy_(CONFIG)
  status_code = 0
  if bstack1l111111l1_opy_.bstack11111l1l1_opy_(CONFIG):
    status_code = mod_behave_main(arg, retries)
  else:
    from behave.__main__ import main as bstack1ll111lll_opy_
    status_code = bstack1ll111lll_opy_(arg)
  if status_code != 0:
    bstack1111111l_opy_ = status_code
def bstack1l1l1l1l_opy_():
  logger.info(bstack1111l111_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1ll1lll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪค"), help=bstack1ll1lll_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡣࡰࡰࡩ࡭࡬࠭ฅ"))
  parser.add_argument(bstack1ll1lll_opy_ (u"࠭࠭ࡶࠩฆ"), bstack1ll1lll_opy_ (u"ࠧ࠮࠯ࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫง"), help=bstack1ll1lll_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠧจ"))
  parser.add_argument(bstack1ll1lll_opy_ (u"ࠩ࠰࡯ࠬฉ"), bstack1ll1lll_opy_ (u"ࠪ࠱࠲ࡱࡥࡺࠩช"), help=bstack1ll1lll_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡣࡦࡧࡪࡹࡳࠡ࡭ࡨࡽࠬซ"))
  parser.add_argument(bstack1ll1lll_opy_ (u"ࠬ࠳ࡦࠨฌ"), bstack1ll1lll_opy_ (u"࠭࠭࠮ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫญ"), help=bstack1ll1lll_opy_ (u"࡚ࠧࡱࡸࡶࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ฎ"))
  bstack1l1lllllll_opy_ = parser.parse_args()
  try:
    bstack11l1111ll_opy_ = bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡨࡧࡱࡩࡷ࡯ࡣ࠯ࡻࡰࡰ࠳ࡹࡡ࡮ࡲ࡯ࡩࠬฏ")
    if bstack1l1lllllll_opy_.framework and bstack1l1lllllll_opy_.framework not in (bstack1ll1lll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩฐ"), bstack1ll1lll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫฑ")):
      bstack11l1111ll_opy_ = bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠴ࡹ࡮࡮࠱ࡷࡦࡳࡰ࡭ࡧࠪฒ")
    bstack1l11l11ll1_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11l1111ll_opy_)
    bstack1l11lll11l_opy_ = open(bstack1l11l11ll1_opy_, bstack1ll1lll_opy_ (u"ࠬࡸࠧณ"))
    bstack1111111lll_opy_ = bstack1l11lll11l_opy_.read()
    bstack1l11lll11l_opy_.close()
    if bstack1l1lllllll_opy_.username:
      bstack1111111lll_opy_ = bstack1111111lll_opy_.replace(bstack1ll1lll_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭ด"), bstack1l1lllllll_opy_.username)
    if bstack1l1lllllll_opy_.key:
      bstack1111111lll_opy_ = bstack1111111lll_opy_.replace(bstack1ll1lll_opy_ (u"࡚ࠧࡑࡘࡖࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩต"), bstack1l1lllllll_opy_.key)
    if bstack1l1lllllll_opy_.framework:
      bstack1111111lll_opy_ = bstack1111111lll_opy_.replace(bstack1ll1lll_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩถ"), bstack1l1lllllll_opy_.framework)
    file_name = bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬท")
    file_path = os.path.abspath(file_name)
    bstack1111l11ll_opy_ = open(file_path, bstack1ll1lll_opy_ (u"ࠪࡻࠬธ"))
    bstack1111l11ll_opy_.write(bstack1111111lll_opy_)
    bstack1111l11ll_opy_.close()
    logger.info(bstack1lll111l1l_opy_)
    try:
      os.environ[bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭น")] = bstack1l1lllllll_opy_.framework if bstack1l1lllllll_opy_.framework != None else bstack1ll1lll_opy_ (u"ࠧࠨบ")
      config = yaml.safe_load(bstack1111111lll_opy_)
      config[bstack1ll1lll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ป")] = bstack1ll1lll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡴࡧࡷࡹࡵ࠭ผ")
      bstack1l11llll1l_opy_(bstack111l1111_opy_, config)
    except Exception as e:
      logger.debug(bstack11ll1lll11_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1l11l1lll_opy_.format(str(e)))
def bstack1l11llll1l_opy_(bstack111l1ll1ll_opy_, config, bstack1l1lll11ll_opy_=None, bstack1l11llllll_opy_=False):
  global BROWSERSTACK_AUTOMATION
  global bstack111llll1_opy_
  global global_config
  if not config:
    return
  if bstack1l1lll11ll_opy_ is None:
    bstack1l1lll11ll_opy_ = {}
  bstack11l1ll1l1l_opy_ = bstack1ll1l111l1_opy_ if not BROWSERSTACK_AUTOMATION else (
    bstack1lll1111_opy_ if bstack1ll1lll_opy_ (u"ࠨࡣࡳࡴࠬฝ") in config else (
        bstack1111l1111l_opy_ if config.get(bstack1ll1lll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭พ")) else bstack1l11l1l111_opy_
    )
)
  bstack11111l11l_opy_ = False
  bstack111111ll1_opy_ = False
  if BROWSERSTACK_AUTOMATION is True:
      if bstack1ll1lll_opy_ (u"ࠪࡥࡵࡶࠧฟ") in config:
          bstack11111l11l_opy_ = True
      else:
          bstack111111ll1_opy_ = True
  bstack11l1ll1l11_opy_ = TestHubUtils.bstack1ll1l1ll1_opy_(config, bstack111llll1_opy_)
  bstack11111ll111_opy_ = bstack111ll1l11_opy_()
  data = {
    bstack1ll1lll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ภ"): config[bstack1ll1lll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧม")],
    bstack1ll1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩย"): config[bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪร")],
    bstack1ll1lll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬฤ"): bstack111l1ll1ll_opy_,
    bstack1ll1lll_opy_ (u"ࠩࡧࡩࡹ࡫ࡣࡵࡧࡧࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ล"): os.environ.get(bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬฦ"), bstack111llll1_opy_),
    bstack1ll1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ว"): bstack1l111l111_opy_,
    bstack1ll1lll_opy_ (u"ࠬࡵࡰࡵ࡫ࡰࡥࡱࡥࡨࡶࡤࡢࡹࡷࡲࠧศ"): bstack1l1l111111_opy_(),
    bstack1ll1lll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩษ"): {
      bstack1ll1lll_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬส"): str(config[bstack1ll1lll_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨห")]) if bstack1ll1lll_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩฬ") in config else bstack1ll1lll_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦอ"),
      bstack1ll1lll_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ฮ"): sys.version,
      bstack1ll1lll_opy_ (u"ࠬࡸࡥࡧࡧࡵࡶࡪࡸࠧฯ"): bstack1l1l11ll_opy_(os.environ.get(bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨะ"), bstack111llll1_opy_)),
      bstack1ll1lll_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩั"): bstack1ll1lll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨา"),
      bstack1ll1lll_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪำ"): bstack11l1ll1l1l_opy_,
      bstack1ll1lll_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨิ"): bstack11l1ll1l11_opy_,
      bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡪࡸࡦࡤࡻࡵࡪࡦࠪี"): os.environ[bstack1ll1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪึ")],
      bstack1ll1lll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩื"): os.environ.get(bstack1ll1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌุࠩ"), bstack111llll1_opy_),
      bstack1ll1lll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱูࠫ"): bstack1llllllll_opy_(os.environ.get(bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎฺࠫ"), bstack111llll1_opy_)),
      bstack1ll1lll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ฻"): bstack11111ll111_opy_.get(bstack1ll1lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ฼")),
      bstack1ll1lll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫ฽"): bstack11111ll111_opy_.get(bstack1ll1lll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧ฾")),
      bstack1ll1lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ฿"): config[bstack1ll1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫเ")] if config[bstack1ll1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬแ")] else bstack1ll1lll_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦโ"),
      bstack1ll1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ใ"): str(config[bstack1ll1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧไ")]) if bstack1ll1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨๅ") in config else bstack1ll1lll_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣๆ"),
      bstack1ll1lll_opy_ (u"ࠨࡱࡶࠫ็"): sys.platform,
      bstack1ll1lll_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨ่ࠫ"): socket.gethostname(),
      bstack1ll1lll_opy_ (u"ࠪ࡭ࡸࡉࡌࡊࡇࡱࡥࡧࡲࡥࡥ้ࠩ"): bstack1l11llllll_opy_,
      bstack1ll1lll_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ๊࠭"): global_config.get_property(bstack1ll1lll_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪ๋ࠧ"))
    }
  }
  if not global_config.get_property(bstack1ll1lll_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭์")) is None:
    data[bstack1ll1lll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪํ")][bstack1ll1lll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡐࡩࡹࡧࡤࡢࡶࡤࠫ๎")] = {
      bstack1ll1lll_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩ๏"): bstack1ll1lll_opy_ (u"ࠪࡹࡸ࡫ࡲࡠ࡭࡬ࡰࡱ࡫ࡤࠨ๐"),
      bstack1ll1lll_opy_ (u"ࠫࡸ࡯ࡧ࡯ࡣ࡯ࠫ๑"): global_config.get_property(bstack1ll1lll_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬ๒")),
      bstack1ll1lll_opy_ (u"࠭ࡳࡪࡩࡱࡥࡱࡔࡵ࡮ࡤࡨࡶࠬ๓"): global_config.get_property(bstack1ll1lll_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡏࡱࠪ๔"))
    }
  if bstack111l1ll1ll_opy_ == bstack11l1lll1l_opy_:
    data[bstack1ll1lll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫ๕")][bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡄࡱࡱࡪ࡮࡭ࠧ๖")] = bstack1111l11lll_opy_(config)
    data[bstack1ll1lll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭๗")][bstack1ll1lll_opy_ (u"ࠫ࡮ࡹࡐࡦࡴࡦࡽࡆࡻࡴࡰࡇࡱࡥࡧࡲࡥࡥࠩ๘")] = percy.bstack1ll11l11_opy_
    data[bstack1ll1lll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨ๙")][bstack1ll1lll_opy_ (u"࠭ࡰࡦࡴࡦࡽࡇࡻࡩ࡭ࡦࡌࡨࠬ๚")] = percy.percy_build_id
  if not bstack1l111111l1_opy_.bstack1lll1llll1_opy_(CONFIG):
    data[bstack1ll1lll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪ๛")][bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠬ๜")] = bstack1l111111l1_opy_.bstack1lll1llll1_opy_(CONFIG)
  bstack111l11l1_opy_ = bstack111lll11_opy_.get_instance(CONFIG, logger)
  bstack1lll111ll_opy_ = bstack1l111111l1_opy_.get_instance(config=CONFIG)
  if bstack111l11l1_opy_ is not None and bstack1lll111ll_opy_ is not None and bstack1lll111ll_opy_.bstack1l11llll_opy_():
    data[bstack1ll1lll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬ๝")][bstack1lll111ll_opy_.bstack1l1lll1ll1_opy_()] = bstack111l11l1_opy_.bstack1ll1ll111_opy_()
  update(data[bstack1ll1lll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭๞")], bstack1l1lll11ll_opy_)
  try:
    response = bstack111lll1l11_opy_(bstack1ll1lll_opy_ (u"ࠫࡕࡕࡓࡕࠩ๟"), bstack1l11l1ll_opy_(bstack1l111111ll_opy_), data, {
      bstack1ll1lll_opy_ (u"ࠬࡧࡵࡵࡪࠪ๠"): (config[bstack1ll1lll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ๡")], config[bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ๢")])
    })
    if response:
      logger.debug(bstack1l1111ll1l_opy_.format(bstack111l1ll1ll_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack11lll1ll1l_opy_.format(str(e)))
def bstack1l1l11ll_opy_(framework):
  return bstack1ll1lll_opy_ (u"ࠣࡽࢀ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࡾࢁࠧ๣").format(str(framework), __version__) if framework else bstack1ll1lll_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࡼࡿࠥ๤").format(
    __version__)
def bstack11l11l1ll1_opy_():
  global CONFIG
  global bstack1l11l11ll_opy_
  if bool(CONFIG):
    return
  try:
    bstack1lllll111l_opy_()
    logger.debug(bstack1l1l1lllll_opy_.format(str(CONFIG)))
    bstack1l11l11ll_opy_ = logger_utils.configure_logger(CONFIG, bstack1l11l11ll_opy_)
    bstack1111lll11l_opy_()
  except Exception as e:
    logger.error(bstack1ll1lll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࡸࡴ࠱ࠦࡥࡳࡴࡲࡶ࠿ࠦࠢ๥") + str(e))
    sys.exit(1)
  sys.excepthook = bstack11l11l1l_opy_
  atexit.register(bstack11l1l111l_opy_)
  signal.signal(signal.SIGINT, bstack1ll11111l1_opy_)
  signal.signal(signal.SIGTERM, bstack1ll11111l1_opy_)
def bstack11l11l1l_opy_(exctype, value, traceback):
  global bstack11ll1llll_opy_
  try:
    for driver in bstack11ll1llll_opy_:
      bstack1ll1lll1l_opy_(driver, bstack1ll1lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ๦"), bstack1ll1lll_opy_ (u"࡙ࠧࡥࡴࡵ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࡢ࡮ࠣ๧") + str(value))
  except Exception:
    pass
  logger.info(bstack11ll1l1l11_opy_)
  bstack11ll11l1l_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack11ll11l1l_opy_(message=bstack1ll1lll_opy_ (u"࠭ࠧ๨"), bstack1llll1ll1_opy_ = False, bstack1l11llllll_opy_ = False):
  global CONFIG
  bstack1111ll111l_opy_ = bstack1ll1lll_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠩ๩") if bstack1llll1ll1_opy_ else bstack1ll1lll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ๪")
  bstack11ll11ll11_opy_ = bstack1l1l11ll1_opy_.bstack11l1llllll_opy_(EVENTS.bstack1lll11111l_opy_)
  try:
    if message:
      bstack1l1lll11ll_opy_ = {
        bstack1111ll111l_opy_ : str(message)
      }
      try:
        bstack1l11llll1l_opy_(bstack11l1lll1l_opy_, CONFIG, bstack1l1lll11ll_opy_, bstack1l11llllll_opy_)
      finally:
        bstack1l1l11ll1_opy_.end(EVENTS.bstack1lll11111l_opy_.value, bstack11ll11ll11_opy_ + bstack1ll1lll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ๫"), bstack11ll11ll11_opy_ + bstack1ll1lll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ๬"), status=True, failure=None, test_name=None)
    else:
      try:
        bstack1l11llll1l_opy_(bstack11l1lll1l_opy_, CONFIG, bstack1l11llllll_opy_=bstack1l11llllll_opy_)
      finally:
        bstack1l1l11ll1_opy_.end(EVENTS.bstack1lll11111l_opy_.value, bstack11ll11ll11_opy_ + bstack1ll1lll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ๭"), bstack11ll11ll11_opy_ + bstack1ll1lll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ๮"), status=True, failure=None, test_name=None)
  except Exception as e:
    logger.debug(bstack111l1l111_opy_.format(str(e)))
def bstack1l1lllll11_opy_(bstack111l111l_opy_, size):
  bstack1ll1l1111_opy_ = []
  while len(bstack111l111l_opy_) > size:
    bstack11ll11l1ll_opy_ = bstack111l111l_opy_[:size]
    bstack1ll1l1111_opy_.append(bstack11ll11l1ll_opy_)
    bstack111l111l_opy_ = bstack111l111l_opy_[size:]
  bstack1ll1l1111_opy_.append(bstack111l111l_opy_)
  return bstack1ll1l1111_opy_
def bstack111l111l1l_opy_(args):
  if bstack1ll1lll_opy_ (u"࠭࠭࡮ࠩ๯") in args and bstack1ll1lll_opy_ (u"ࠧࡱࡦࡥࠫ๰") in args:
    return True
  return False
@measure(event_name=EVENTS.bstack11ll1111l_opy_, stage=STAGE.bstack1l1lll11l1_opy_)
def run_on_browserstack(bstack11111ll11_opy_=None, bstack1l1l111l1_opy_=None, bstack1l1ll1l1_opy_=False):
  global CONFIG
  global bstack1l11ll1ll_opy_
  global bstack111l11l11_opy_
  global bstack111llll1_opy_
  global global_config
  bstack1ll11ll1l_opy_ = bstack1ll1lll_opy_ (u"ࠨࠩ๱")
  bstack111lllll11_opy_ = bstack1ll1lll_opy_ (u"ࠤࠥ๲")
  bstack1l1ll1l111_opy_(bstack11ll1l111_opy_, logger)
  if bstack11111ll11_opy_ and isinstance(bstack11111ll11_opy_, str):
    bstack11111ll11_opy_ = eval(bstack11111ll11_opy_)
  if bstack11111ll11_opy_:
    CONFIG = bstack11111ll11_opy_[bstack1ll1lll_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪ๳")]
    bstack1l11ll1ll_opy_ = bstack11111ll11_opy_[bstack1ll1lll_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬ๴")]
    bstack111l11l11_opy_ = bstack11111ll11_opy_[bstack1ll1lll_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ๵")]
    global_config.bstack1l1ll1llll_opy_(bstack1ll1lll_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ๶"), bstack111l11l11_opy_)
    bstack1ll11ll1l_opy_ = bstack1ll1lll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡨࡧࡱࡩࡷ࡯ࡣࠨ๷")
  global_config.bstack1l1ll1llll_opy_(bstack1ll1lll_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪ๸"), uuid4().__str__())
  logger.info(bstack1ll1lll_opy_ (u"ࠩࡖࡈࡐࠦࡲࡶࡰࠣࡷࡹࡧࡲࡵࡧࡧࠤࡼ࡯ࡴࡩࠢ࡬ࡨ࠿ࠦࠧ๹") + global_config.get_property(bstack1ll1lll_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࠬ๺")));
  logger.debug(bstack1ll1lll_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩࡃࠧ๻") + global_config.get_property(bstack1ll1lll_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪࠧ๼")))
  if not bstack1l1ll1l1_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1111l1l11l_opy_)
      return
    if sys.argv[1] == bstack1ll1lll_opy_ (u"࠭࠭࠮ࡸࡨࡶࡸ࡯࡯࡯ࠩ๽") or sys.argv[1] == bstack1ll1lll_opy_ (u"ࠧ࠮ࡸࠪ๾"):
      logger.info(bstack1ll1lll_opy_ (u"ࠨࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡑࡻࡷ࡬ࡴࡴࠠࡔࡆࡎࠤࡻࢁࡽࠨ๿").format(__version__))
      return
    if sys.argv[1] == bstack1ll1lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ຀"):
      bstack1l1l1l1l_opy_()
      return
    if sys.argv[1] == bstack1ll1lll_opy_ (u"ࠪࡰࡴࡧࡤࠨກ"):
      from browserstack_sdk.bstack1l11l1lll1_opy_ import bstack1l1l11l111_opy_
      bstack11l11l1ll1_opy_()
      bstack1l1l11l111_opy_(CONFIG)
      return
  args = sys.argv
  bstack11l11l1ll1_opy_()
  global bstack111l1ll1l_opy_
  try:
    from bstack_utils import constants as bstack111ll11111_opy_
    override_value = CONFIG.get(bstack1ll1lll_opy_ (u"ࠫࡴࡼࡥࡳࡴ࡬ࡨࡪࡒ࡯ࡢࡦࡗࡩࡸࡺࡩ࡯ࡩࠪຂ"), False)
    bstack111l1ll1l_opy_ = bool(override_value)
  except Exception as e:
    logger.error(bstack1ll1lll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡒ࡚ࡊࡘࡒࡊࡆࡈࡣࡑࡕࡁࡅࡡࡗࡉࡘ࡚ࡉࡏࡉ࠽ࠤࢀࢃࠢ຃").format(e))
    bstack111l1ll1l_opy_ = False
  if bstack111l1ll1l_opy_:
    bstack1l1l1111_opy_ = CONFIG.get(bstack1ll1lll_opy_ (u"࠭࡬ࡰࡣࡧࡘࡪࡹࡴࡪࡰࡪࡌࡺࡨࡕࡓࡎࠪຄ")) or bstack111ll11111_opy_.bstack111l11llll_opy_
    logger.info(bstack1ll1lll_opy_ (u"ࠢࡈ࡮ࡲࡦࡦࡲࠠࡰࡸࡨࡶࡷ࡯ࡤࡦ࡮ࡲࡥࡩࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡥ࡯ࡣࡥࡰࡪࡪࠬࠡࡷࡶ࡭ࡳ࡭ࠠࡩࡷࡥ࠾ࠥࢁࡽࠣ຅").format(bstack1l1l1111_opy_))
    bstack1l11ll1ll_opy_ = bstack1l1l1111_opy_
    try:
      bstack111ll11111_opy_.HTTPS_HUB = bstack1l1l1111_opy_
      bstack111ll11111_opy_.bstack1ll1l11l1_opy_ = bstack1l1l1111_opy_
    except Exception:
      pass
  global bstack1ll1ll11_opy_
  global bstack11ll1l11_opy_
  global PARALLELISE_VANILLA_PYTHON
  global PARALLELISE_THREADING_PYTHON
  global PLATFORM_INDEX
  global bstack1l1l11111_opy_
  global bstack1l11l111_opy_
  global bstack1lll1l111l_opy_
  global bstack11lll1ll1_opy_
  global bstack111ll11l1l_opy_
  global bstack11l111l1l_opy_
  bstack11ll1l11_opy_ = len(CONFIG.get(bstack1ll1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫຆ"), []))
  if not bstack1ll11ll1l_opy_:
    if args[1] == bstack1ll1lll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩງ") or args[1] == bstack1ll1lll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫຈ") or args[1] == bstack1ll1lll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠬຉ"):
      bstack1ll11ll1l_opy_ = bstack1ll1lll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨ࠭ຊ")
      args = args[2:]
    elif args[1] == bstack1ll1lll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ຋"):
      bstack1ll11ll1l_opy_ = bstack1ll1lll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ຌ")
      args = args[2:]
    elif args[1] == bstack1ll1lll_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧຍ"):
      bstack1ll11ll1l_opy_ = bstack1ll1lll_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨຎ")
      args = args[2:]
    elif args[1] == bstack1ll1lll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫຏ"):
      bstack1ll11ll1l_opy_ = bstack1ll1lll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬຐ")
      args = args[2:]
    elif args[1] == bstack1ll1lll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬຑ"):
      bstack1ll11ll1l_opy_ = bstack1ll1lll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ຒ")
      args = args[2:]
    elif args[1] == bstack1ll1lll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧຓ"):
      bstack1ll11ll1l_opy_ = bstack1ll1lll_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨດ")
      args = args[2:]
    else:
      if not bstack1ll1lll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬຕ") in CONFIG or str(CONFIG[bstack1ll1lll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ຖ")]).lower() in [bstack1ll1lll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫທ"), bstack1ll1lll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠸࠭ຘ"), bstack1ll1lll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡧࡦࡰࡨࡶ࡮ࡩࠧນ")]:
        bstack1ll11ll1l_opy_ = bstack1ll1lll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡨࡧࡱࡩࡷ࡯ࡣࠨບ")
        args = args[1:]
      elif str(CONFIG[bstack1ll1lll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫປ")]).lower() == bstack1ll1lll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨຜ"):
        bstack1ll11ll1l_opy_ = bstack1ll1lll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩຝ")
        args = args[1:]
      elif str(CONFIG[bstack1ll1lll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧພ")]).lower() == bstack1ll1lll_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫຟ"):
        bstack1ll11ll1l_opy_ = bstack1ll1lll_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬຠ")
        args = args[1:]
      elif str(CONFIG[bstack1ll1lll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪມ")]).lower() == bstack1ll1lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨຢ"):
        bstack1ll11ll1l_opy_ = bstack1ll1lll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩຣ")
        args = args[1:]
      elif str(CONFIG[bstack1ll1lll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭຤")]).lower() == bstack1ll1lll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫລ"):
        bstack1ll11ll1l_opy_ = bstack1ll1lll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ຦")
        args = args[1:]
      else:
        os.environ[bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨວ")] = bstack1ll11ll1l_opy_
        bstack1lll1111l_opy_(bstack1lll1l1l1_opy_)
  os.environ[bstack1ll1lll_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨຨ")] = bstack1ll11ll1l_opy_
  bstack111llll1_opy_ = bstack1ll11ll1l_opy_
  if cli.is_enabled(CONFIG):
    try:
      if bstack1ll11ll1l_opy_ == bstack1ll1lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨຩ") and bstack1111ll11_opy_():
        bstack1ll1llllll_opy_ = bstack1llll11l1l_opy_[bstack1ll1lll_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕ࠯ࡅࡈࡉ࠭ສ")]
      elif bstack1ll11ll1l_opy_ in [bstack1ll1lll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫຫ"), bstack1ll1lll_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪຬ")]:
        bstack1ll1llllll_opy_ = bstack1ll1lll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫອ")
      else:
        bstack1ll1llllll_opy_ = bstack1ll11ll1l_opy_
      bstack11llllll11_opy_.invoke(Events.bstack1ll1l1lll_opy_, bstack1lll11l11l_opy_(
        sdk_version=__version__,
        path_config=bstack111lllll1l_opy_(),
        path_project=os.getcwd(),
        test_framework=bstack1ll1llllll_opy_,
        frameworks=[bstack1ll1llllll_opy_],
        framework_versions={
          bstack1ll1llllll_opy_: bstack1llllllll_opy_(bstack1ll1lll_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬຮ") if bstack1ll11ll1l_opy_ in [bstack1ll1lll_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ຯ"), bstack1ll1lll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧະ"), bstack1ll1lll_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪັ")] else bstack1ll11ll1l_opy_)
        },
        bs_config=CONFIG
      ))
      if cli.config and cli.config.get(bstack1ll1lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧາ"), None):
        CONFIG[bstack1ll1lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࠨຳ")] = cli.config.get(bstack1ll1lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠢິ"), None)
    except Exception as e:
      bstack11llllll11_opy_.invoke(Events.bstack1111ll1l1_opy_, e.__traceback__, 1)
    if bstack111l11l11_opy_:
      CONFIG[bstack1ll1lll_opy_ (u"ࠨࡡࡱࡲࠥີ")] = cli.config[bstack1ll1lll_opy_ (u"ࠢࡢࡲࡳࠦຶ")]
      logger.info(bstack11l1llll1_opy_.format(CONFIG[bstack1ll1lll_opy_ (u"ࠨࡣࡳࡴࠬື")]))
  else:
    bstack11llllll11_opy_.clear()
  global bstack1ll11ll1l1_opy_
  global bstack111l11ll1l_opy_
  if bstack11111ll11_opy_:
    try:
      bstack11lllll111_opy_ = datetime.datetime.now()
      os.environ[bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎຸࠫ")] = bstack1ll11ll1l_opy_
      bstack11l11ll1l_opy_ = bstack1l1l11ll1_opy_.bstack11l1llllll_opy_(EVENTS.bstack1l111l1l11_opy_)
      try:
        logger.info(bstack1ll1lll_opy_ (u"ࠥࡗࡪࡴࡤࡪࡰࡪࠤࡘࡊࡋࠡࡖࡨࡷࡹࠦࡁࡵࡶࡨࡱࡵࡺࡥࡥࠢࡨࡺࡪࡴࡴູࠣ"))
        bstack1l11llll1l_opy_(bstack1lllll1l11_opy_, CONFIG)
      finally:
        bstack1l1l11ll1_opy_.end(EVENTS.bstack1l111l1l11_opy_.value, bstack11l11ll1l_opy_ + bstack1ll1lll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷ຺ࠦ"), bstack11l11ll1l_opy_ + bstack1ll1lll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥົ"), status=True, failure=None, test_name=None)
      cli.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠨࡨࡵࡶࡳ࠾ࡸࡪ࡫ࡠࡶࡨࡷࡹࡥࡡࡵࡶࡨࡱࡵࡺࡥࡥࠤຼ"), datetime.datetime.now() - bstack11lllll111_opy_)
    except Exception as e:
      logger.debug(bstack1l11ll1l11_opy_.format(str(e)))
  global bstack1l1ll11l_opy_
  global bstack1l1l1l111_opy_
  global bstack111lll1l1l_opy_
  global bstack111111l1l_opy_
  global bstack1ll1l1l1l1_opy_
  global bstack111l11ll_opy_
  global bstack1111l11l11_opy_
  global bstack11l111lll1_opy_
  global bstack11l1l111_opy_
  global bstack1lllll1lll_opy_
  global bstack1111111l1l_opy_
  global bstack1l11111ll_opy_
  global bstack1111lllll_opy_
  global bstack11111111l1_opy_
  global bstack1l1llllll_opy_
  global bstack1l111lll11_opy_
  global bstack111l11lll1_opy_
  global bstack1ll1llll11_opy_
  global bstack11lll11l11_opy_
  global bstack1llll1l1ll_opy_
  global bstack1l1lll1l_opy_
  global bstack1l11lll1l1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l1ll11l_opy_ = webdriver.Remote.__init__
    bstack1l1l1l111_opy_ = WebDriver.quit
    bstack1l11111ll_opy_ = WebDriver.close
    bstack1l111lll11_opy_ = WebDriver.get
    bstack1l11lll1l1_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1ll11ll1l1_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack1llllll1l1_opy_
    bstack111l11ll1l_opy_ = bstack1llllll1l1_opy_()
  except Exception as e:
    pass
  try:
    global bstack1l1llll1ll_opy_
    from QWeb.keywords import browser
    bstack1l1llll1ll_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack111111l11_opy_(CONFIG) and bstack1lllllll1l_opy_():
    if bstack1l1l11l1l1_opy_() < version.parse(bstack1lll1ll11l_opy_):
      logger.error(bstack1111llllll_opy_.format(bstack1l1l11l1l1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack1ll1lll_opy_ (u"ࠧࡠࡩࡨࡸࡤࡶࡲࡰࡺࡼࡣࡺࡸ࡬ࠨຽ")) and callable(getattr(RemoteConnection, bstack1ll1lll_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩ຾"))):
          RemoteConnection._get_proxy_url = bstack1l1111111l_opy_
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          ClientConfig.get_proxy_url = bstack1l1111111l_opy_
      except Exception as e:
        logger.error(bstack11l1l1l1l1_opy_.format(str(e)))
  if not CONFIG.get(bstack1ll1lll_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫ຿"), False) and not bstack11111ll11_opy_:
    logger.info(bstack1ll1l1ll1l_opy_)
  bstack1111ll1ll1_opy_ = not cli.is_enabled(CONFIG) and bstack1ll11ll1l_opy_ not in [bstack1ll1lll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫເ")]
  bstack1ll1ll11l_opy_ = bstack1111ll1ll1_opy_ and bstack1ll1lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨແ") in CONFIG and str(CONFIG[bstack1ll1lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩໂ")]).lower() != bstack1ll1lll_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬໃ")
  bstack11ll1lll1_opy_ = bstack1111ll1ll1_opy_ and not bstack1ll1ll11l_opy_ and (bstack1ll11ll1l_opy_ != bstack1ll1lll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡨࡧࡱࡩࡷ࡯ࡣࠨໄ") or (bstack1ll11ll1l_opy_ == bstack1ll1lll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩ໅") and not bstack11111ll11_opy_))
  if bstack1ll11ll1l_opy_ not in [bstack1ll1lll_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪໆ")]:
    bstack1l1ll1l111_opy_(os.path.join(os.getcwd(), bstack1ll1lll_opy_ (u"ࠪࡰࡴ࡭ࠧ໇"), bstack1ll1lll_opy_ (u"ࠫࡰ࡫ࡹ࠮࡯ࡨࡸࡷ࡯ࡣࡴ࠰࡭ࡷࡴࡴ່ࠧ")), logger)
  if (bstack1ll11ll1l_opy_ in [bstack1ll1lll_opy_ (u"ࠬࡶࡡࡣࡱࡷ້ࠫ"), bstack1ll1lll_opy_ (u"࠭ࡲࡰࡤࡲࡸ໊ࠬ"), bstack1ll1lll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ໋")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      try:
        from pabot.pabot import QueueItem
        from pabot import pabot
      except Exception as e:
        logger.warning(bstack11llll111_opy_ + str(e))
      if not is_robot_playwright_installed():
        try:
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
          WebDriverCreator._get_ff_profile = bstack1lllll111_opy_
          bstack111l11ll_opy_ = WebDriverCache.close
        except Exception as e:
          logger.warning(bstack111ll1l1l_opy_ + str(e))
        try:
          from AppiumLibrary.utils.applicationcache import ApplicationCache
          bstack1ll1l1l1l1_opy_ = ApplicationCache.close
        except Exception as e:
          logger.debug(bstack111111l11l_opy_ + str(e))
    except Exception as e:
      bstack11l1l111ll_opy_(e, bstack111ll1l1l_opy_)
    if bstack1ll11ll1l_opy_ != bstack1ll1lll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ໌"):
      bstack11lllll1_opy_()
    bstack111lll1l1l_opy_ = Output.start_test
    bstack111111l1l_opy_ = Output.end_test
    bstack1111l11l11_opy_ = TestStatus.__init__
    bstack11l1l111_opy_ = pabot._run
    bstack1lllll1lll_opy_ = QueueItem.__init__
    bstack1111111l1l_opy_ = pabot._create_command_for_execution
    bstack1llll1l1ll_opy_ = pabot._report_results
  if bstack1ll11ll1l_opy_ == bstack1ll1lll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩໍ"):
    global bstack11111l11ll_opy_
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11l1l111ll_opy_(e, bstack11lll1l11_opy_)
    bstack1111lllll_opy_ = Runner.run_hook
    bstack11111111l1_opy_ = Runner.load_hooks
    bstack1l1llllll_opy_ = Step.run
    try:
      sig = inspect.signature(bstack1111lllll_opy_)
      params = list(sig.parameters.keys())
      bstack11111l11ll_opy_ = bstack1ll1lll_opy_ (u"ࠪࡧࡴࡴࡴࡦࡺࡷࠫ໎") in params
      logger.info(bstack1ll1lll_opy_ (u"ࠫࡉ࡫ࡴࡦࡥࡷࡩࡩࠦࡢࡦࡪࡤࡺࡪࠦࡲࡶࡰࡢ࡬ࡴࡵ࡫ࠡࡵ࡬࡫ࡳࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨ໏").format(bstack1ll1lll_opy_ (u"ࠬ࠷࠮࠳࠰࠹ࠤ࠭ࡽࡩࡵࡪࠣࡧࡴࡴࡴࡦࡺࡷ࠭ࠬ໐") if bstack11111l11ll_opy_ else bstack1ll1lll_opy_ (u"࠭࠱࠯࠵࠮ࠤ࠭ࡽࡩࡵࡪࡲࡹࡹࠦࡣࡰࡰࡷࡩࡽࡺࠩࠨ໑")))
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡤࡶࠣࡦࡪ࡮ࡡࡷࡧࠣࡶࡺࡴ࡟ࡩࡱࡲ࡯ࠥࡹࡩࡨࡰࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬ໒").format(str(e)))
      bstack11111l11ll_opy_ = None
  if bstack1ll11ll1l_opy_ == bstack1ll1lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ໓"):
    try:
      from _pytest.config import Config
      bstack1ll1llll11_opy_ = Config.getoption
      from _pytest import runner
      bstack11lll11l11_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warning(bstack1ll1lll_opy_ (u"ࠤࠨࡷ࠿ࠦࠥࡴࠤ໔"), bstack111llllll_opy_, str(e))
    try:
      from pytest_bdd import reporting
      bstack1l1lll1l_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡲࠤࡷࡻ࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࡶࠫ໕"))
    if bstack1l1ll1l1ll_opy_():
      logger.warning(bstack1lll111lll_opy_[bstack1ll1lll_opy_ (u"ࠫࡘࡊࡋ࠮ࡉࡈࡒ࠲࠶࠰࠶ࠩ໖")])
  try:
    framework_name = bstack1ll1lll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ໗") if bstack1ll11ll1l_opy_ in [bstack1ll1lll_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ໘"), bstack1ll1lll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭໙"), bstack1ll1lll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ໚")] else bstack111l1ll111_opy_(bstack1ll11ll1l_opy_)
    bstack1lll111l11_opy_ = {
      bstack1ll1lll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࠪ໛"): bstack1ll1lll_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶ࠰ࡧࡺࡩࡵ࡮ࡤࡨࡶࠬໜ") if bstack1ll11ll1l_opy_ == bstack1ll1lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫໝ") and bstack1111ll11_opy_() else framework_name,
      bstack1ll1lll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩໞ"): bstack1llllllll_opy_(framework_name),
      bstack1ll1lll_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫໟ"): __version__,
      bstack1ll1lll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨ໠"): bstack1ll11ll1l_opy_
    }
    if bstack1ll11ll1l_opy_ in bstack11111llll_opy_ + bstack1l11l1ll11_opy_:
      if a11y.is_enabled_root(CONFIG):
        if bstack1ll1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ໡") in CONFIG:
          os.environ[bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ໢")] = os.getenv(bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ໣"), json.dumps(CONFIG[bstack1ll1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ໤")]))
          CONFIG[bstack1ll1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ໥")].pop(bstack1ll1lll_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫ໦"), None)
          CONFIG[bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ໧")].pop(bstack1ll1lll_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭໨"), None)
        bstack11l1llll11_opy_ = bstack1ll1lll_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭໩") if CONFIG.get(bstack1ll1lll_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩ໪")) or bstack11l11111l1_opy_() else bstack1ll1lll_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭໫")
        if bstack11l1llll11_opy_ == bstack1ll1lll_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩ໬"):
          try:
            import importlib.metadata as _11l1l1111l_opy_
            bstack1l11ll1ll1_opy_ = _11l1l1111l_opy_.version(bstack1ll1lll_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ໭"))
          except Exception:
            bstack1l11ll1ll1_opy_ = bstack1ll1lll_opy_ (u"ࠧࡶࡰ࡮ࡲࡴࡽ࡮ࠨ໮")
        else:
          bstack1l11ll1ll1_opy_ = str(bstack1l1l11l1l1_opy_())
        bstack1lll111l11_opy_[bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ໯")] = {
          bstack1ll1lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ໰"): bstack11l1llll11_opy_,
          bstack1ll1lll_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫ໱"): bstack1l11ll1ll1_opy_
        }
    bstack1ll11111l_opy_, bstack1ll111l1l1_opy_ = None, {}
    bstack1l111l11l_opy_ = None
    bstack1l1ll1111_opy_ = None
    def bstack1ll11l1l1l_opy_():
      if bstack1ll1ll11l_opy_:
        bstack1lll1ll1l1_opy_()
      elif bstack11ll1lll1_opy_:
        bstack1l1llll11l_opy_()
    def bstack1l111ll1ll_opy_():
      nonlocal bstack1ll11111l_opy_, bstack1ll111l1l1_opy_
      if bstack1ll11ll1l_opy_ not in [bstack1ll1lll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ໲")] and not cli.is_running():
        bstack1ll11111l_opy_, bstack1ll111l1l1_opy_ = TestHubHandler.launch(CONFIG, bstack1lll111l11_opy_)
    if bstack1ll1ll11l_opy_ or bstack11ll1lll1_opy_:
      bstack1l111l11l_opy_ = threading.Thread(target=bstack1ll11l1l1l_opy_)
      bstack1l111l11l_opy_.start()
    if bstack1ll11ll1l_opy_ not in [bstack1ll1lll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭໳")] and not cli.is_running():
      bstack1l1ll1111_opy_ = threading.Thread(target=bstack1l111ll1ll_opy_)
      bstack1l1ll1111_opy_.start()
    if bstack1l111l11l_opy_:
      bstack1l111l11l_opy_.join()
    if bstack1l1ll1111_opy_:
      bstack1l1ll1111_opy_.join()
    if bstack1ll111l1l1_opy_.get(bstack1ll1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭໴")) is not None and a11y.bstack11ll11ll_opy_(CONFIG) is None:
      value = bstack1ll111l1l1_opy_[bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ໵")].get(bstack1ll1lll_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩ໶"))
      if value is not None:
          CONFIG[bstack1ll1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ໷")] = value
      else:
        logger.debug(bstack1ll1lll_opy_ (u"ࠥࡒࡴࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡤࡢࡶࡤࠤ࡫ࡵࡵ࡯ࡦࠣ࡭ࡳࠦࡲࡦࡵࡳࡳࡳࡹࡥࠣ໸"))
  except Exception as e:
    logger.debug(bstack11l111l1_opy_.format(bstack1ll1lll_opy_ (u"࡙ࠫ࡫ࡳࡵࡊࡸࡦࠬ໹"), str(e)))
  if bstack1ll11ll1l_opy_ == bstack1ll1lll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨ࠭໺"):
    PARALLELISE_VANILLA_PYTHON = True
    if bstack11111ll11_opy_ and bstack1l1ll1l1_opy_:
      if cli.is_enabled(CONFIG):
        bstack1l1l11111_opy_ = cli.config.get(bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ໻"), {}).get(bstack1ll1lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ໼")) if cli.config else None
      else:
        bstack1l1l11111_opy_ = CONFIG.get(bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ໽"), {}).get(bstack1ll1lll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ໾"))
      bstack1l11111l11_opy_(bstack11lll1l1l_opy_)
    elif bstack11111ll11_opy_:
      if cli.is_enabled(CONFIG):
        bstack1l1l11111_opy_ = cli.config.get(bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ໿"), {}).get(bstack1ll1lll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ༀ")) if cli.config else None
      else:
        bstack1l1l11111_opy_ = CONFIG.get(bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ༁"), {}).get(bstack1ll1lll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ༂"))
      global bstack11ll1llll_opy_
      try:
        if bstack111l111l1l_opy_(bstack11111ll11_opy_[bstack1ll1lll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ༃")]) and multiprocessing.current_process().name == bstack1ll1lll_opy_ (u"ࠨ࠲ࠪ༄"):
          bstack11111ll11_opy_[bstack1ll1lll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ༅")].remove(bstack1ll1lll_opy_ (u"ࠪ࠱ࡲ࠭༆"))
          bstack11111ll11_opy_[bstack1ll1lll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ༇")].remove(bstack1ll1lll_opy_ (u"ࠬࡶࡤࡣࠩ༈"))
          bstack11111ll11_opy_[bstack1ll1lll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ༉")] = bstack11111ll11_opy_[bstack1ll1lll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ༊")][0]
          with open(bstack11111ll11_opy_[bstack1ll1lll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ་")], bstack1ll1lll_opy_ (u"ࠩࡵࠫ༌")) as f:
            file_content = f.read()
          bstack11ll1l1l1_opy_ = bstack1ll1lll_opy_ (u"ࠥࠦࠧ࡬ࡲࡰ࡯ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡨࡰࠦࡩ࡮ࡲࡲࡶࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦ࠽ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪ࠮ࡻࡾࠫ࠾ࠤ࡫ࡸ࡯࡮ࠢࡳࡨࡧࠦࡩ࡮ࡲࡲࡶࡹࠦࡐࡥࡤ࠾ࠤࡴ࡭࡟ࡥࡤࠣࡁࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡦࡨࡪࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠩࡵࡨࡰ࡫࠲ࠠࡢࡴࡪ࠰ࠥࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠡ࠿ࠣ࠴࠮ࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺࡲࡺ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡥࡷ࡭ࠠ࠾ࠢࡶࡸࡷ࠮ࡩ࡯ࡶࠫࡥࡷ࡭ࠩࠬ࠳࠳࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡩࡽࡩࡥࡱࡶࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡡࡴࠢࡨ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡶࡡࡴࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡱࡪࡣࡩࡨࠨࡴࡧ࡯ࡪ࠱ࡧࡲࡨ࠮ࡷࡩࡲࡶ࡯ࡳࡣࡵࡽ࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡓࡨࡧ࠴ࡤࡰࡡࡥࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮ࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣࠪࠬ࠲ࡸ࡫ࡴࡠࡶࡵࡥࡨ࡫ࠨࠪ࡞ࡱࠦࠧࠨ།").format(str(bstack11111ll11_opy_))
          bstack11111lll1_opy_ = bstack11ll1l1l1_opy_ + file_content
          bstack1l1l1l1l1l_opy_ = bstack11111ll11_opy_[bstack1ll1lll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ༎")] + bstack1ll1lll_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥࡴࡦ࡯ࡳ࠲ࡵࡿࠧ༏")
          with open(bstack1l1l1l1l1l_opy_, bstack1ll1lll_opy_ (u"࠭ࡷࠨ༐")):
            pass
          with open(bstack1l1l1l1l1l_opy_, bstack1ll1lll_opy_ (u"ࠢࡸ࠭ࠥ༑")) as f:
            f.write(bstack11111lll1_opy_)
          import subprocess
          bstack111ll1ll_opy_ = subprocess.run([bstack1ll1lll_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࠣ༒"), bstack1l1l1l1l1l_opy_])
          if os.path.exists(bstack1l1l1l1l1l_opy_):
            os.unlink(bstack1l1l1l1l1l_opy_)
          os._exit(bstack111ll1ll_opy_.returncode)
        else:
          if bstack111l111l1l_opy_(bstack11111ll11_opy_[bstack1ll1lll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ༓")]):
            bstack11111ll11_opy_[bstack1ll1lll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭༔")].remove(bstack1ll1lll_opy_ (u"ࠫ࠲ࡳࠧ༕"))
            bstack11111ll11_opy_[bstack1ll1lll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ༖")].remove(bstack1ll1lll_opy_ (u"࠭ࡰࡥࡤࠪ༗"))
            bstack11111ll11_opy_[bstack1ll1lll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧ༘ࠪ")] = bstack11111ll11_opy_[bstack1ll1lll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨ༙ࠫ")][0]
          bstack1l11111l11_opy_(bstack11lll1l1l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack11111ll11_opy_[bstack1ll1lll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ༚")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1ll1lll_opy_ (u"ࠪࡣࡤࡴࡡ࡮ࡧࡢࡣࠬ༛")] = bstack1ll1lll_opy_ (u"ࠫࡤࡥ࡭ࡢ࡫ࡱࡣࡤ࠭༜")
          mod_globals[bstack1ll1lll_opy_ (u"ࠬࡥ࡟ࡧ࡫࡯ࡩࡤࡥࠧ༝")] = os.path.abspath(bstack11111ll11_opy_[bstack1ll1lll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ༞")])
          exec(open(bstack11111ll11_opy_[bstack1ll1lll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ༟")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1ll1lll_opy_ (u"ࠨࡅࡤࡹ࡬࡮ࡴࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠨ༠").format(str(e)))
          for driver in bstack11ll1llll_opy_:
            bstack1l1l111l1_opy_.append({
              bstack1ll1lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ༡"): bstack11111ll11_opy_[bstack1ll1lll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭༢")],
              bstack1ll1lll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ༣"): str(e),
              bstack1ll1lll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ༤"): multiprocessing.current_process().name
            })
            bstack1ll1lll1l_opy_(driver, bstack1ll1lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭༥"), bstack1ll1lll_opy_ (u"ࠢࡔࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥ༦") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack11ll1llll_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack111l11l11_opy_, CONFIG, logger)
      bstack111111l1ll_opy_()
      bstack111ll1l11l_opy_()
      percy.bstack11lll1l1_opy_()
      bstack11lllllll_opy_ = {
        bstack1ll1lll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ༧"): args[0],
        bstack1ll1lll_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩ༨"): CONFIG,
        bstack1ll1lll_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫ༩"): bstack1l11ll1ll_opy_,
        bstack1ll1lll_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭༪"): bstack111l11l11_opy_
      }
      if bstack1ll1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ༫") in CONFIG:
        bstack1ll1l1ll11_opy_ = bstack111lll1ll1_opy_(args, logger, CONFIG, BROWSERSTACK_AUTOMATION, bstack11ll1l11_opy_)
        bstack1lll1l111l_opy_ = bstack1ll1l1ll11_opy_.bstack11l111ll11_opy_(run_on_browserstack, bstack11lllllll_opy_, bstack111l111l1l_opy_(args))
      else:
        if bstack111l111l1l_opy_(args):
          bstack11lllllll_opy_[bstack1ll1lll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ༬")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack11lllllll_opy_,))
          test.start()
          test.join()
        else:
          bstack1l11111l11_opy_(bstack11lll1l1l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1ll1lll_opy_ (u"ࠧࡠࡡࡱࡥࡲ࡫࡟ࡠࠩ༭")] = bstack1ll1lll_opy_ (u"ࠨࡡࡢࡱࡦ࡯࡮ࡠࡡࠪ༮")
          mod_globals[bstack1ll1lll_opy_ (u"ࠩࡢࡣ࡫࡯࡬ࡦࡡࡢࠫ༯")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1ll11ll1l_opy_ == bstack1ll1lll_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ༰") or bstack1ll11ll1l_opy_ == bstack1ll1lll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ༱"):
    percy.init(bstack111l11l11_opy_, CONFIG, logger)
    percy.bstack11lll1l1_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack11l1l111ll_opy_(e, bstack111ll1l1l_opy_)
    bstack111111l1ll_opy_()
    bstack1l11111l11_opy_(bstack1l11l1l1_opy_)
    if BROWSERSTACK_AUTOMATION:
      bstack111ll1l1ll_opy_(bstack1l11l1l1_opy_, args)
      if bstack1ll1lll_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ༲") in args:
        i = args.index(bstack1ll1lll_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ༳"))
        args.pop(i)
        args.pop(i)
      if bstack1ll1lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ༴") not in CONFIG:
        CONFIG[bstack1ll1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶ༵ࠫ")] = [{}]
        bstack11ll1l11_opy_ = 1
      if bstack1ll1ll11_opy_ == 0:
        bstack1ll1ll11_opy_ = 1
      args.insert(0, str(bstack1ll1ll11_opy_))
      args.insert(0, str(bstack1ll1lll_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ༶")))
    if TestHubHandler.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack11lll11ll_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1111lll1l1_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack1ll1lll_opy_ (u"ࠥࡖࡔࡈࡏࡕࡡࡒࡔ࡙ࡏࡏࡏࡕ༷ࠥ"),
        ).parse_args(bstack11lll11ll_opy_)
        bstack1ll11ll11_opy_ = args.index(bstack11lll11ll_opy_[0]) if len(bstack11lll11ll_opy_) > 0 else len(args)
        args.insert(bstack1ll11ll11_opy_, str(bstack1ll1lll_opy_ (u"ࠫ࠲࠳࡬ࡪࡵࡷࡩࡳ࡫ࡲࠨ༸")))
        args.insert(bstack1ll11ll11_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll1lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡸ࡯ࡣࡱࡷࡣࡱ࡯ࡳࡵࡧࡱࡩࡷ࠴ࡰࡺ༹ࠩ"))))
        if bstack1l111111l1_opy_.bstack11111l1l1_opy_(CONFIG):
          args.insert(bstack1ll11ll11_opy_, str(bstack1ll1lll_opy_ (u"࠭࠭࠮࡮࡬ࡷࡹ࡫࡮ࡦࡴࠪ༺")))
          args.insert(bstack1ll11ll11_opy_ + 1, str(bstack1ll1lll_opy_ (u"ࠧࡓࡧࡷࡶࡾࡌࡡࡪ࡮ࡨࡨ࠿ࢁࡽࠨ༻").format(bstack1l111111l1_opy_.bstack1ll111111_opy_(CONFIG))))
        if bstack1l11l11111_opy_(os.environ.get(bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓ࠭༼"))) and str(os.environ.get(bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭༽"), bstack1ll1lll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ༾"))) != bstack1ll1lll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ༿"):
          for bstack11l1l1l1l_opy_ in bstack1111lll1l1_opy_:
            args.remove(bstack11l1l1l1l_opy_)
          test_files = os.environ.get(bstack1ll1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠩཀ")).split(bstack1ll1lll_opy_ (u"࠭ࠬࠨཁ"))
          for bstack111ll1ll1l_opy_ in test_files:
            args.append(bstack111ll1ll1l_opy_)
      except Exception as e:
        logger.error(bstack1ll1lll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡧࡴࡵࡣࡦ࡬࡮ࡴࡧࠡ࡮࡬ࡷࡹ࡫࡮ࡦࡴࠣࡪࡴࡸࠠࡼࡿ࠱ࠤࡊࡸࡲࡰࡴࠣ࠱ࠥࢁࡽࠣག").format(bstack1l1l1l1lll_opy_, e))
    pabot.main(args)
  elif bstack1ll11ll1l_opy_ == bstack1ll1lll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩགྷ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack11l1l111ll_opy_(e, bstack111ll1l1l_opy_)
    for a in args:
      if bstack1ll1lll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘࠨང") in a:
        PLATFORM_INDEX = int(a.split(bstack1ll1lll_opy_ (u"ࠪ࠾ࠬཅ"))[1])
      if bstack1ll1lll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨཆ") in a:
        bstack1l1l11111_opy_ = str(a.split(bstack1ll1lll_opy_ (u"ࠬࡀࠧཇ"))[1])
      if bstack1ll1lll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘ࠭཈") in a:
        bstack1l11l111_opy_ = str(a.split(bstack1ll1lll_opy_ (u"ࠧ࠻ࠩཉ"))[1])
    bstack1llll111l1_opy_ = None
    bstack1111111111_opy_ = None
    if bstack1ll1lll_opy_ (u"ࠨ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠧཊ") in args:
      i = args.index(bstack1ll1lll_opy_ (u"ࠩ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠨཋ"))
      args.pop(i)
      bstack1llll111l1_opy_ = args.pop(i)
    if bstack1ll1lll_opy_ (u"ࠪ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽ࠭ཌ") in args:
      i = args.index(bstack1ll1lll_opy_ (u"ࠫ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࠧཌྷ"))
      args.pop(i)
      bstack1111111111_opy_ = args.pop(i)
    if bstack1llll111l1_opy_ is not None:
      global bstack11ll111l11_opy_
      bstack11ll111l11_opy_ = bstack1llll111l1_opy_
    if bstack1111111111_opy_ is not None and int(PLATFORM_INDEX) < 0:
      PLATFORM_INDEX = int(bstack1111111111_opy_)
    if cli.is_enabled(CONFIG):
      if cli.bstack1l11lll1l_opy_():
        bstack11llllll11_opy_.invoke(Events.CONNECT, bstack1l1llll1_opy_())
        cli.bstack111l11l11l_opy_(PLATFORM_INDEX)
      if cli.bstack1l1l111ll_opy_(bstack1lll11ll1_opy_):
        cli.bstack1111111ll_opy_()
    bstack1l11111l11_opy_(bstack1l11l1l1_opy_)
    run_cli(args)
    if bstack1ll1lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩཎ") in multiprocessing.current_process().__dict__.keys():
      for bstack1lll1l1ll1_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1l1l111l1_opy_.append(bstack1lll1l1ll1_opy_)
  elif bstack1ll11ll1l_opy_ == bstack1ll1lll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ཏ"):
    bstack111111l1l1_opy_ = bstack1l11111l_opy_(args, logger, CONFIG, BROWSERSTACK_AUTOMATION)
    bstack111111l1l1_opy_.bstack11lll1111l_opy_()
    bstack111111l1ll_opy_()
    PARALLELISE_THREADING_PYTHON = True
    bstack111ll11l1l_opy_ = bstack111111l1l1_opy_.bstack1l1lll1ll_opy_()
    bstack111111l1l1_opy_.bstack11lllllll_opy_(bstack1ll11l1l_opy_)
    bstack111111l1l1_opy_.bstack1ll1111lll_opy_()
    bstack1l1l11l11_opy_(bstack1ll11ll1l_opy_, CONFIG, bstack111111l1l1_opy_.bstack11l11lllll_opy_())
    bstack1l111ll111_opy_.end(EVENTS.bstack11ll1111l_opy_.value, EVENTS.bstack11ll1111l_opy_.value + bstack1ll1lll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢཐ"), EVENTS.bstack11ll1111l_opy_.value + bstack1ll1lll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨད"), status=True, failure=None, test_name=SESSION_NAME)
    bstack1l11lll1ll_opy_ = bstack111111l1l1_opy_.bstack11l111ll11_opy_(bstack11ll1l1ll1_opy_, {
      bstack1ll1lll_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩདྷ"): CONFIG,
      bstack1ll1lll_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫན"): bstack1l11ll1ll_opy_,
      bstack1ll1lll_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭པ"): bstack111l11l11_opy_,
      bstack1ll1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨཕ"): BROWSERSTACK_AUTOMATION,
      bstack1ll1lll_opy_ (u"࠭ࡏࡗࡇࡕࡖࡎࡊࡅࡠࡎࡒࡅࡉࡥࡔࡆࡕࡗࡍࡓࡍࠧབ"): bstack111l1ll1l_opy_
    })
    if not bstack11111ll11_opy_:
      bstack111lllll11_opy_ = bstack1l1l11ll1_opy_.bstack11l1llllll_opy_(EVENTS.bstack1ll1l1l1l_opy_.value)
    try:
      bstack1l1l1ll11l_opy_, bstack11l11l1111_opy_ = map(list, zip(*bstack1l11lll1ll_opy_))
      bstack11lll1ll1_opy_ = bstack1l1l1ll11l_opy_[0]
      for status_code in bstack11l11l1111_opy_:
        if status_code != 0:
          bstack11l111l1l_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡦࡼࡥࠡࡧࡵࡶࡴࡸࡳࠡࡣࡱࡨࠥࡹࡴࡢࡶࡸࡷࠥࡩ࡯ࡥࡧ࠱ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠ࠻ࠢࡾࢁࠧབྷ").format(str(e)))
  elif bstack1ll11ll1l_opy_ == bstack1ll1lll_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨམ"):
    try:
      from behave.__main__ import main as bstack1ll111lll_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack11l1l111ll_opy_(e, bstack11lll1l11_opy_)
    bstack111111l1ll_opy_()
    PARALLELISE_THREADING_PYTHON = True
    bstack1ll1l1ll_opy_ = 1
    if bstack1ll1lll_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩཙ") in CONFIG:
      bstack1ll1l1ll_opy_ = CONFIG[bstack1ll1lll_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪཚ")]
    if bstack1ll1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧཛ") in CONFIG:
      bstack1llll1l1l_opy_ = int(bstack1ll1l1ll_opy_) * int(len(CONFIG[bstack1ll1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨཛྷ")]))
    else:
      bstack1llll1l1l_opy_ = int(bstack1ll1l1ll_opy_)
    config = Configuration(args)
    bstack111l1l1l1l_opy_ = config.paths
    if len(bstack111l1l1l1l_opy_) == 0:
      import glob
      pattern = bstack1ll1lll_opy_ (u"࠭ࠪࠫ࠱࠭࠲࡫࡫ࡡࡵࡷࡵࡩࠬཝ")
      bstack1lllllll1_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1lllllll1_opy_)
      config = Configuration(args)
      bstack111l1l1l1l_opy_ = config.paths
    bstack11llll1l11_opy_ = [os.path.normpath(item) for item in bstack111l1l1l1l_opy_]
    bstack1llllllll1_opy_ = [os.path.normpath(item) for item in args]
    bstack11l11111ll_opy_ = [item for item in bstack1llllllll1_opy_ if item not in bstack11llll1l11_opy_]
    import platform as pf
    if pf.system().lower() == bstack1ll1lll_opy_ (u"ࠧࡸ࡫ࡱࡨࡴࡽࡳࠨཞ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack11llll1l11_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1111lll1_opy_)))
                    for bstack1111lll1_opy_ in bstack11llll1l11_opy_]
    try:
      bstack11111ll1l_opy_ = bstack111l11111l_opy_(args, logger, CONFIG, BROWSERSTACK_AUTOMATION)
      bstack11111ll1l_opy_.bstack111lllllll_opy_(bstack11llll1l11_opy_)
      bstack11111ll1l_opy_.bstack1ll1111lll_opy_()
      bstack11llll1l11_opy_ = bstack11111ll1l_opy_.bstack1l1l11lll1_opy_()
    except Exception as e:
      logger.error(bstack1ll1lll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡦࡶࡰ࡭ࡻࠣࡸࡪࡹࡴࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡨࡲࡶࠥࡨࡥࡩࡣࡹࡩ࠿ࠦࠥࡴࠤཟ"), e, exc_info=True)
      logger.info(bstack1ll1lll_opy_ (u"ࠤࡆࡳࡳࡺࡩ࡯ࡷ࡬ࡲ࡬ࠦࡷࡪࡶ࡫ࠤࡴࡸࡩࡨ࡫ࡱࡥࡱࠦࡳࡱࡧࡦࠤ࡫࡯࡬ࡦࡵࠣࡻ࡮ࡺࡨࡰࡷࡷࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠦའ"))
    bstack1l11ll11l_opy_ = []
    for spec in bstack11llll1l11_opy_:
      bstack11l1ll11ll_opy_ = []
      bstack11l1ll11ll_opy_ += bstack11l11111ll_opy_
      bstack11l1ll11ll_opy_.append(spec)
      bstack1l11ll11l_opy_.append(bstack11l1ll11ll_opy_)
    execution_items = []
    for bstack11l1ll11ll_opy_ in bstack1l11ll11l_opy_:
      if bstack1ll1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ཡ") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack1ll1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧར")]):
          item = {}
          item[bstack1ll1lll_opy_ (u"ࠬࡧࡲࡨࠩལ")] = bstack1ll1lll_opy_ (u"࠭ࠠࠨཤ").join(bstack11l1ll11ll_opy_)
          item[bstack1ll1lll_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ཥ")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack1ll1lll_opy_ (u"ࠨࡣࡵ࡫ࠬས")] = bstack1ll1lll_opy_ (u"ࠩࠣࠫཧ").join(bstack11l1ll11ll_opy_)
        item[bstack1ll1lll_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩཨ")] = 0
        execution_items.append(item)
    bstack111ll11ll_opy_ = bstack1l1lllll11_opy_(execution_items, bstack1llll1l1l_opy_)
    for execution_item in bstack111ll11ll_opy_:
      bstack11111lllll_opy_ = []
      for item in execution_item:
        bstack11111lllll_opy_.append(bstack1l1lllll_opy_(name=str(item[bstack1ll1lll_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪཀྵ")]),
                                             target=bstack11ll11ll1_opy_,
                                             args=(item[bstack1ll1lll_opy_ (u"ࠬࡧࡲࡨࠩཪ")],)))
      for t in bstack11111lllll_opy_:
        t.start()
      for t in bstack11111lllll_opy_:
        t.join()
  else:
    bstack1lll1111l_opy_(bstack1lll1l1l1_opy_)
  if not bstack11111ll11_opy_:
    bstack1ll11l1ll_opy_()
    if bstack111lllll11_opy_:
      bstack1l1l11ll1_opy_.end(EVENTS.bstack1ll1l1l1l_opy_.value, bstack111lllll11_opy_ + bstack1ll1lll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨཫ"), bstack111lllll11_opy_ + bstack1ll1lll_opy_ (u"ࠢ࠻ࡧࡱࡨࠧཬ"), status=True, failure=None, test_name=None)
  logger_utils.bstack11111111l_opy_()
def browserstack_initialize(bstack111l1ll1l1_opy_=None):
  logger.info(bstack1ll1lll_opy_ (u"ࠨࡔࡸࡲࡳ࡯࡮ࡨࠢࡖࡈࡐࠦࡷࡪࡶ࡫ࠤࡦࡸࡧࡴ࠼ࠣࠫ཭") + str(bstack111l1ll1l1_opy_))
  run_on_browserstack(bstack111l1ll1l1_opy_, None, True)
@measure(event_name=EVENTS.bstack1l1lll1111_opy_, stage=STAGE.bstack1111l1ll1_opy_, bstack1l1l1l11_opy_=SESSION_NAME)
def bstack1ll11l1ll_opy_():
  global CONFIG
  global bstack111llll1_opy_
  global bstack11l111l1l_opy_
  global bstack1111111l_opy_
  global global_config
  global _1111l1l1_opy_
  bstack11l1111l1l_opy_.bstack1ll111l111_opy_()
  _1111l1l1_opy_ = cli.is_running()
  if _1111l1l1_opy_:
    bstack11llllll11_opy_.invoke(Events.bstack111l1111ll_opy_)
  else:
    bstack1lll111ll_opy_ = bstack1l111111l1_opy_.get_instance(config=CONFIG)
    bstack1lll111ll_opy_.bstack1ll1ll1l1l_opy_(CONFIG)
  hashed_id = None
  bstack11ll1l1l_opy_ = None
  def bstack11l1l1l111_opy_():
    try:
      if bstack111llll1_opy_ == bstack1ll1lll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ཮"):
        if not cli.is_enabled(CONFIG):
          TestHubHandler.stop()
      else:
        TestHubHandler.stop()
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡶࡸࡴࡶࡰࡪࡰࡪࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࡻࡾࠤ཯").format(e))
  def bstack11l1l11ll_opy_():
    try:
      if not cli.is_enabled(CONFIG):
        bstack11llll1l_opy_.bstack1l1lllll1l_opy_()
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡴࡷ࡯࡮ࡵ࡫ࡱ࡫ࠥࡨࡵࡪ࡮ࡧࠤࡱ࡯࡮࡬࠼ࠣࡿࢂࠨ཰").format(e))
  def bstack111l1111l1_opy_():
    nonlocal hashed_id, bstack11ll1l1l_opy_
    try:
      if bstack1ll1lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦཱࠩ") in CONFIG and str(CONFIG[bstack1ll1lll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧིࠪ")]).lower() != bstack1ll1lll_opy_ (u"ࠧࡧࡣ࡯ࡷࡪཱི࠭"):
        hashed_id, bstack11ll1l1l_opy_ = bstack1lllll1l1_opy_()
      else:
        hashed_id, bstack11ll1l1l_opy_ = get_build_link()
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡤࡸ࡭ࡱࡪࠠ࡭࡫ࡱ࡯࠿ࠦࡻࡾࠤུ").format(e))
  bstack1ll1111ll1_opy_ = threading.Thread(target=bstack11l1l1l111_opy_)
  bstack1ll1l1l1_opy_ = threading.Thread(target=bstack11l1l11ll_opy_)
  bstack111ll1lll_opy_ = threading.Thread(target=bstack111l1111l1_opy_)
  threads = [bstack1ll1111ll1_opy_, bstack1ll1l1l1_opy_, bstack111ll1lll_opy_]
  for thread in threads:
    try:
      thread.start()
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡵࡷࡥࡷࡺࡩ࡯ࡩࠣࡸ࡭ࡸࡥࡢࡦࠣࡿࢂࡀࠠࡼࡿཱུࠥ").format(thread.name, e))
  for thread in threads:
    try:
      thread.join()
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡭ࡳ࡮ࡴࡩ࡯ࡩࠣࡸ࡭ࡸࡥࡢࡦࠣࡿࢂࡀࠠࡼࡿࠥྲྀ").format(thread.name, e))
  bstack11l1111l1_opy_(hashed_id)
  logger.info(bstack1ll1lll_opy_ (u"ࠫࡘࡊࡋࠡࡴࡸࡲࠥ࡫࡮ࡥࡧࡧࠤ࡫ࡵࡲࠡ࡫ࡧ࠾ࠬཷ") + global_config.get_property(bstack1ll1lll_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪࠧླྀ"), bstack1ll1lll_opy_ (u"࠭ࠧཹ")) + bstack1ll1lll_opy_ (u"ࠧ࠭ࠢࡷࡩࡸࡺࡨࡶࡤࠣ࡭ࡩࡀࠠࠨེ") + os.getenv(bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉཻ࠭"), bstack1ll1lll_opy_ (u"ོࠩࠪ")))
  if hashed_id is not None and bstack1l111l1l1l_opy_() != -1:
    sessions = bstack1l1111ll11_opy_(hashed_id)
    bstack111l111111_opy_(sessions, bstack11ll1l1l_opy_)
  if bstack111llll1_opy_ == bstack1ll1lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶཽࠪ") and bstack11l111l1l_opy_ != 0:
    sys.exit(bstack11l111l1l_opy_)
  if bstack111llll1_opy_ == bstack1ll1lll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫཾ") and bstack1111111l_opy_ != 0:
    sys.exit(bstack1111111l_opy_)
def bstack11l1111l1_opy_(new_id):
    global bstack1l111l111_opy_
    bstack1l111l111_opy_ = new_id
def bstack111l1ll111_opy_(bstack11111lll1l_opy_):
  if bstack11111lll1l_opy_:
    return bstack11111lll1l_opy_.capitalize()
  else:
    return bstack1ll1lll_opy_ (u"ࠬ࠭ཿ")
@measure(event_name=EVENTS.bstack1l11l1l1ll_opy_, stage=STAGE.bstack1111l1ll1_opy_, bstack1l1l1l11_opy_=SESSION_NAME)
def bstack11lll1l1l1_opy_(bstack11ll11l11_opy_):
  if bstack1ll1lll_opy_ (u"࠭࡮ࡢ࡯ࡨྀࠫ") in bstack11ll11l11_opy_ and bstack11ll11l11_opy_[bstack1ll1lll_opy_ (u"ࠧ࡯ࡣࡰࡩཱྀࠬ")] != bstack1ll1lll_opy_ (u"ࠨࠩྂ"):
    return bstack11ll11l11_opy_[bstack1ll1lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧྃ")]
  else:
    bstack1l1l1l11_opy_ = bstack1ll1lll_opy_ (u"྄ࠥࠦ")
    if bstack1ll1lll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫ྅") in bstack11ll11l11_opy_ and bstack11ll11l11_opy_[bstack1ll1lll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬ྆")] != None:
      bstack1l1l1l11_opy_ += bstack11ll11l11_opy_[bstack1ll1lll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭྇")] + bstack1ll1lll_opy_ (u"ࠢ࠭ࠢࠥྈ")
      if bstack11ll11l11_opy_[bstack1ll1lll_opy_ (u"ࠨࡱࡶࠫྉ")] == bstack1ll1lll_opy_ (u"ࠤ࡬ࡳࡸࠨྊ"):
        bstack1l1l1l11_opy_ += bstack1ll1lll_opy_ (u"ࠥ࡭ࡔ࡙ࠠࠣྋ")
      bstack1l1l1l11_opy_ += (bstack11ll11l11_opy_[bstack1ll1lll_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨྌ")] or bstack1ll1lll_opy_ (u"ࠬ࠭ྍ"))
      return bstack1l1l1l11_opy_
    else:
      bstack1l1l1l11_opy_ += bstack111l1ll111_opy_(bstack11ll11l11_opy_[bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧྎ")]) + bstack1ll1lll_opy_ (u"ࠢࠡࠤྏ") + (
              bstack11ll11l11_opy_[bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪྐ")] or bstack1ll1lll_opy_ (u"ࠩࠪྑ")) + bstack1ll1lll_opy_ (u"ࠥ࠰ࠥࠨྒ")
      if bstack11ll11l11_opy_[bstack1ll1lll_opy_ (u"ࠫࡴࡹࠧྒྷ")] == bstack1ll1lll_opy_ (u"ࠧ࡝ࡩ࡯ࡦࡲࡻࡸࠨྔ"):
        bstack1l1l1l11_opy_ += bstack1ll1lll_opy_ (u"ࠨࡗࡪࡰࠣࠦྕ")
      bstack1l1l1l11_opy_ += bstack11ll11l11_opy_[bstack1ll1lll_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫྖ")] or bstack1ll1lll_opy_ (u"ࠨࠩྗ")
      return bstack1l1l1l11_opy_
@measure(event_name=EVENTS.bstack11l111l111_opy_, stage=STAGE.bstack1111l1ll1_opy_, bstack1l1l1l11_opy_=SESSION_NAME)
def bstack1111llll11_opy_(bstack111l11lll_opy_):
  if bstack111l11lll_opy_ == bstack1ll1lll_opy_ (u"ࠤࡧࡳࡳ࡫ࠢ྘"):
    return bstack1ll1lll_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿࡭ࡲࡦࡧࡱ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧ࡭ࡲࡦࡧࡱࠦࡃࡉ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ྙ")
  elif bstack111l11lll_opy_ == bstack1ll1lll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦྚ"):
    return bstack1ll1lll_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡳࡧࡧ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡸࡥࡥࠤࡁࡊࡦ࡯࡬ࡦࡦ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨྛ")
  elif bstack111l11lll_opy_ == bstack1ll1lll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨྜ"):
    return bstack1ll1lll_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡪࡶࡪ࡫࡮࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡪࡶࡪ࡫࡮ࠣࡀࡓࡥࡸࡹࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧྜྷ")
  elif bstack111l11lll_opy_ == bstack1ll1lll_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢྞ"):
    return bstack1ll1lll_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡷ࡫ࡤ࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡵࡩࡩࠨ࠾ࡆࡴࡵࡳࡷࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫྟ")
  elif bstack111l11lll_opy_ == bstack1ll1lll_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࠦྠ"):
    return bstack1ll1lll_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࠣࡦࡧࡤ࠷࠷࠼࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࠥࡨࡩࡦ࠹࠲࠷ࠤࡁࡘ࡮ࡳࡥࡰࡷࡷࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩྡ")
  elif bstack111l11lll_opy_ == bstack1ll1lll_opy_ (u"ࠧࡸࡵ࡯ࡰ࡬ࡲ࡬ࠨྡྷ"):
    return bstack1ll1lll_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡤ࡯ࡥࡨࡱ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡤ࡯ࡥࡨࡱࠢ࠿ࡔࡸࡲࡳ࡯࡮ࡨ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧྣ")
  else:
    return bstack1ll1lll_opy_ (u"ࠧ࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡦࡱࡧࡣ࡬࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡦࡱࡧࡣ࡬ࠤࡁࠫྤ") + bstack111l1ll111_opy_(
      bstack111l11lll_opy_) + bstack1ll1lll_opy_ (u"ࠨ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧྥ")
def bstack1ll11llll1_opy_(session):
  return bstack1ll1lll_opy_ (u"ࠩ࠿ࡸࡷࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡲࡰࡹࠥࡂࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠦࡳࡦࡵࡶ࡭ࡴࡴ࠭࡯ࡣࡰࡩࠧࡄ࠼ࡢࠢ࡫ࡶࡪ࡬࠽ࠣࡽࢀࠦࠥࡺࡡࡳࡩࡨࡸࡂࠨ࡟ࡣ࡮ࡤࡲࡰࠨ࠾ࡼࡿ࠿࠳ࡦࡄ࠼࠰ࡶࡧࡂࢀࢃࡻࡾ࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀ࠴ࡺࡲ࠿ࠩྦ").format(
    session[bstack1ll1lll_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥࡢࡹࡷࡲࠧྦྷ")], bstack11lll1l1l1_opy_(session), bstack1111llll11_opy_(session[bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡷࡹࡧࡴࡶࡵࠪྨ")]),
    bstack1111llll11_opy_(session[bstack1ll1lll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬྩ")]),
    bstack111l1ll111_opy_(session[bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧྪ")] or session[bstack1ll1lll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧྫ")] or bstack1ll1lll_opy_ (u"ࠨࠩྫྷ")) + bstack1ll1lll_opy_ (u"ࠤࠣࠦྭ") + (session[bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬྮ")] or bstack1ll1lll_opy_ (u"ࠫࠬྯ")),
    session[bstack1ll1lll_opy_ (u"ࠬࡵࡳࠨྰ")] + bstack1ll1lll_opy_ (u"ࠨࠠࠣྱ") + session[bstack1ll1lll_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫྲ")], session[bstack1ll1lll_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪླ")] or bstack1ll1lll_opy_ (u"ࠩࠪྴ"),
    session[bstack1ll1lll_opy_ (u"ࠪࡧࡷ࡫ࡡࡵࡧࡧࡣࡦࡺࠧྵ")] if session[bstack1ll1lll_opy_ (u"ࠫࡨࡸࡥࡢࡶࡨࡨࡤࡧࡴࠨྶ")] else bstack1ll1lll_opy_ (u"ࠬ࠭ྷ"))
@measure(event_name=EVENTS.bstack11l1l1ll1l_opy_, stage=STAGE.bstack1111l1ll1_opy_, bstack1l1l1l11_opy_=SESSION_NAME)
def bstack111l111111_opy_(sessions, bstack11ll1l1l_opy_):
  try:
    bstack1lll11ll1l_opy_ = bstack1ll1lll_opy_ (u"ࠨࠢྸ")
    if not os.path.exists(bstack1ll1llll1l_opy_):
      os.mkdir(bstack1ll1llll1l_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll1lll_opy_ (u"ࠧࡢࡵࡶࡩࡹࡹ࠯ࡳࡧࡳࡳࡷࡺ࠮ࡩࡶࡰࡰࠬྐྵ")), bstack1ll1lll_opy_ (u"ࠨࡴࠪྺ")) as f:
      bstack1lll11ll1l_opy_ = f.read()
    bstack1lll11ll1l_opy_ = bstack1lll11ll1l_opy_.replace(bstack1ll1lll_opy_ (u"ࠩࡾࠩࡗࡋࡓࡖࡎࡗࡗࡤࡉࡏࡖࡐࡗࠩࢂ࠭ྻ"), str(len(sessions)))
    bstack1lll11ll1l_opy_ = bstack1lll11ll1l_opy_.replace(bstack1ll1lll_opy_ (u"ࠪࡿࠪࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠦࡿࠪྼ"), bstack11ll1l1l_opy_)
    bstack1lll11ll1l_opy_ = bstack1lll11ll1l_opy_.replace(bstack1ll1lll_opy_ (u"ࠫࢀࠫࡂࡖࡋࡏࡈࡤࡔࡁࡎࡇࠨࢁࠬ྽"),
                                              sessions[0].get(bstack1ll1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣࡳࡧ࡭ࡦࠩ྾")) if sessions[0] else bstack1ll1lll_opy_ (u"࠭ࠧ྿"))
    with open(os.path.join(bstack1ll1llll1l_opy_, bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡲࡦࡲࡲࡶࡹ࠴ࡨࡵ࡯࡯ࠫ࿀")), bstack1ll1lll_opy_ (u"ࠨࡹࠪ࿁")) as stream:
      stream.write(bstack1lll11ll1l_opy_.split(bstack1ll1lll_opy_ (u"ࠩࡾࠩࡘࡋࡓࡔࡋࡒࡒࡘࡥࡄࡂࡖࡄࠩࢂ࠭࿂"))[0])
      for session in sessions:
        stream.write(bstack1ll11llll1_opy_(session))
      stream.write(bstack1lll11ll1l_opy_.split(bstack1ll1lll_opy_ (u"ࠪࡿ࡙ࠪࡅࡔࡕࡌࡓࡓ࡙࡟ࡅࡃࡗࡅࠪࢃࠧ࿃"))[1])
    logger.info(bstack1ll1lll_opy_ (u"ࠫࡌ࡫࡮ࡦࡴࡤࡸࡪࡪࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡢࡶ࡫࡯ࡨࠥࡧࡲࡵ࡫ࡩࡥࡨࡺࡳࠡࡣࡷࠤࢀࢃࠧ࿄").format(bstack1ll1llll1l_opy_));
  except Exception as e:
    logger.debug(bstack1l1l111ll1_opy_.format(str(e)))
def bstack1l1111ll11_opy_(hashed_id):
  global CONFIG
  try:
    bstack11lllll111_opy_ = datetime.datetime.now()
    host = bstack1ll1lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡱ࡫࠰ࡧࡱࡵࡵࡥ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬ࿅") if bstack1ll1lll_opy_ (u"࠭ࡡࡱࡲ࿆ࠪ") in CONFIG else bstack1ll1lll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨ࿇")
    user = CONFIG[bstack1ll1lll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ࿈")]
    key = CONFIG[bstack1ll1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ࿉")]
    bstack1ll1l111ll_opy_ = bstack1ll1lll_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩ࿊") if bstack1ll1lll_opy_ (u"ࠫࡦࡶࡰࠨ࿋") in CONFIG else (bstack1ll1lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩ࿌") if CONFIG.get(bstack1ll1lll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪ࿍")) else bstack1ll1lll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩ࿎"))
    host = bstack11l11l11ll_opy_(cli.config, [bstack1ll1lll_opy_ (u"ࠣࡣࡳ࡭ࡸࠨ࿏"), bstack1ll1lll_opy_ (u"ࠤࡤࡴࡵࡇࡵࡵࡱࡰࡥࡹ࡫ࠢ࿐"), bstack1ll1lll_opy_ (u"ࠥࡥࡵ࡯ࠢ࿑")], host) if bstack1ll1lll_opy_ (u"ࠫࡦࡶࡰࠨ࿒") in CONFIG else bstack11l11l11ll_opy_(cli.config, [bstack1ll1lll_opy_ (u"ࠧࡧࡰࡪࡵࠥ࿓"), bstack1ll1lll_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥࠣ࿔"), bstack1ll1lll_opy_ (u"ࠢࡢࡲ࡬ࠦ࿕")], host)
    url = bstack1ll1lll_opy_ (u"ࠨࡽࢀ࠳ࢀࢃ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡷࡪࡹࡳࡪࡱࡱࡷ࠳ࡰࡳࡰࡰࠪ࿖").format(host, bstack1ll1l111ll_opy_, hashed_id)
    headers = {
      bstack1ll1lll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨ࿗"): bstack1ll1lll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭࿘"),
    }
    proxies = bstack11l11ll1ll_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies, auth=(user, key))
    if response.json():
      cli.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼ࡪࡩࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࡠ࡮࡬ࡷࡹࠨ࿙"), datetime.datetime.now() - bstack11lllll111_opy_)
      return list(map(lambda session: session[bstack1ll1lll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡩࡸࡹࡩࡰࡰࠪ࿚")], response.json()))
  except Exception as e:
    logger.debug(bstack11l1ll1ll_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack111111llll_opy_, stage=STAGE.bstack1111l1ll1_opy_, bstack1l1l1l11_opy_=SESSION_NAME)
def get_build_link():
  global CONFIG
  global bstack1l111l111_opy_
  try:
    if bstack1ll1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ࿛") in CONFIG:
      bstack11lllll111_opy_ = datetime.datetime.now()
      host = bstack1ll1lll_opy_ (u"ࠧࡢࡲ࡬࠱ࡨࡲ࡯ࡶࡦࠪ࿜") if bstack1ll1lll_opy_ (u"ࠨࡣࡳࡴࠬ࿝") in CONFIG else bstack1ll1lll_opy_ (u"ࠩࡤࡴ࡮࠭࿞")
      user = CONFIG[bstack1ll1lll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ࿟")]
      key = CONFIG[bstack1ll1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ࿠")]
      bstack1ll1l111ll_opy_ = bstack1ll1lll_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ࿡") if bstack1ll1lll_opy_ (u"࠭ࡡࡱࡲࠪ࿢") in CONFIG else bstack1ll1lll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩ࿣")
      url = bstack1ll1lll_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡾࢁ࠿ࢁࡽࡁࡽࢀ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡼࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠱࡮ࡸࡵ࡮ࠨ࿤").format(user, key, host, bstack1ll1l111ll_opy_)
      if cli.is_enabled(CONFIG):
        bstack11ll1l1l_opy_, hashed_id = cli.bstack1111l1l111_opy_()
        logger.info(bstack1l1111lll1_opy_.format(bstack11ll1l1l_opy_))
        return [hashed_id, bstack11ll1l1l_opy_]
      else:
        headers = {
          bstack1ll1lll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨ࿥"): bstack1ll1lll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭࿦"),
        }
        if bstack1ll1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࿧") in CONFIG:
          params = {bstack1ll1lll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ࿨"): CONFIG[bstack1ll1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ࿩")], bstack1ll1lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ࿪"): CONFIG[bstack1ll1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ࿫")]}
        else:
          params = {bstack1ll1lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ࿬"): CONFIG[bstack1ll1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭࿭")]}
        proxies = bstack11l11ll1ll_opy_(CONFIG, url)
        response = requests.get(url, params=params, headers=headers, proxies=proxies)
        if response.json():
          bstack1ll1111111_opy_ = response.json()[0][bstack1ll1lll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡤࡸ࡭ࡱࡪࠧ࿮")]
          if bstack1ll1111111_opy_:
            bstack11ll1l1l_opy_ = bstack1ll1111111_opy_[bstack1ll1lll_opy_ (u"ࠬࡶࡵࡣ࡮࡬ࡧࡤࡻࡲ࡭ࠩ࿯")].split(bstack1ll1lll_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨ࠳ࡢࡶ࡫࡯ࡨࠬ࿰"))[0] + bstack1ll1lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡹ࠯ࠨ࿱") + bstack1ll1111111_opy_[
              bstack1ll1lll_opy_ (u"ࠨࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ࿲")]
            logger.info(bstack1l1111lll1_opy_.format(bstack11ll1l1l_opy_))
            bstack1l111l111_opy_ = bstack1ll1111111_opy_[bstack1ll1lll_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ࿳")]
            bstack1lll1l1ll_opy_ = CONFIG[bstack1ll1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭࿴")]
            if bstack1ll1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࿵") in CONFIG:
              bstack1lll1l1ll_opy_ += bstack1ll1lll_opy_ (u"ࠬࠦࠧ࿶") + CONFIG[bstack1ll1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ࿷")]
            if bstack1lll1l1ll_opy_ != bstack1ll1111111_opy_[bstack1ll1lll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ࿸")]:
              logger.debug(bstack1lll1ll1l_opy_.format(bstack1ll1111111_opy_[bstack1ll1lll_opy_ (u"ࠨࡰࡤࡱࡪ࠭࿹")], bstack1lll1l1ll_opy_))
            cli.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺ࡨࡧࡷࡣࡧࡻࡩ࡭ࡦࡢࡰ࡮ࡴ࡫ࠣ࿺"), datetime.datetime.now() - bstack11lllll111_opy_)
            return [bstack1ll1111111_opy_[bstack1ll1lll_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭࿻")], bstack11ll1l1l_opy_]
    else:
      logger.warning(bstack1l11l11l_opy_)
  except Exception as e:
    logger.debug(bstack111ll1lll1_opy_.format(str(e)))
  return [None, None]
def bstack11l1ll1111_opy_(url, bstack11l1lllll1_opy_=False):
  global CONFIG
  global bstack1l1l1l111l_opy_
  if not bstack1l1l1l111l_opy_:
    hostname = bstack1l11111l1l_opy_(url)
    is_private = bstack1l111lllll_opy_(hostname)
    if (bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ࿼") in CONFIG and not bstack1l11l11111_opy_(CONFIG[bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ࿽")])) and (is_private or bstack11l1lllll1_opy_):
      bstack1l1l1l111l_opy_ = hostname
def bstack1l11111l1l_opy_(url):
  return urlparse(url).hostname
def bstack1l111lllll_opy_(hostname):
  for bstack1l1l1ll1l1_opy_ in bstack11ll111ll_opy_:
    regex = re.compile(bstack1l1l1ll1l1_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1l11ll1111_opy_(bstack1ll1111ll_opy_):
  return True if bstack1ll1111ll_opy_ in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack11lll111ll_opy_, stage=STAGE.bstack1111l1ll1_opy_, bstack1l1l1l11_opy_=SESSION_NAME)
def getAccessibilityResults(driver):
  global CONFIG
  global PLATFORM_INDEX
  bstack1lll1lll1_opy_ = not (bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ࿾"), None) and bstack1l11lll1_opy_(
          threading.current_thread(), bstack1ll1lll_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭࿿"), None))
  bstack1l1ll1ll11_opy_ = getattr(driver, bstack1ll1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨက"), None) != True
  bstack111llll1l_opy_ = bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩခ"), None) and bstack1l11lll1_opy_(
          threading.current_thread(), bstack1ll1lll_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬဂ"), None)
  if bstack111llll1l_opy_:
    if not bstack111ll1ll1_opy_():
      logger.warning(bstack1ll1lll_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡶࡰࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡄࡴࡵࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹ࠮ࠣဃ"))
      return {}
    logger.debug(bstack1ll1lll_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡴࡨࡷࡺࡲࡴࡴࠩင"))
    logger.debug(perform_scan(driver, driver_command=bstack1ll1lll_opy_ (u"࠭ࡥࡹࡧࡦࡹࡹ࡫ࡓࡤࡴ࡬ࡴࡹ࠭စ")))
    results = bstack111lll111_opy_(bstack1ll1lll_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡳࠣဆ"))
    if results is not None and results.get(bstack1ll1lll_opy_ (u"ࠣ࡫ࡶࡷࡺ࡫ࡳࠣဇ")) is not None:
        return results[bstack1ll1lll_opy_ (u"ࠤ࡬ࡷࡸࡻࡥࡴࠤဈ")]
    logger.error(bstack1ll1lll_opy_ (u"ࠥࡒࡴࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡒࡦࡵࡸࡰࡹࡹࠠࡸࡧࡵࡩࠥ࡬࡯ࡶࡰࡧ࠲ࠧဉ"))
    return []
  if not a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX) or (bstack1l1ll1ll11_opy_ and bstack1lll1lll1_opy_):
    logger.warning(bstack1ll1lll_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡪࡺࡲࡪࡧࡹࡩࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸ࠴ࠢည"))
    return {}
  try:
    logger.debug(bstack1ll1lll_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡴࡨࡷࡺࡲࡴࡴࠩဋ"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(accessibility_scripts.get_results)
    return results
  except Exception:
    logger.error(bstack1ll1lll_opy_ (u"ࠨࡎࡰࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡻࡪࡸࡥࠡࡨࡲࡹࡳࡪ࠮ࠣဌ"))
    return {}
@measure(event_name=EVENTS.bstack11111111ll_opy_, stage=STAGE.bstack1111l1ll1_opy_, bstack1l1l1l11_opy_=SESSION_NAME)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global PLATFORM_INDEX
  bstack1lll1lll1_opy_ = not (bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫဍ"), None) and bstack1l11lll1_opy_(
          threading.current_thread(), bstack1ll1lll_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧဎ"), None))
  bstack1l1ll1ll11_opy_ = getattr(driver, bstack1ll1lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩဏ"), None) != True
  bstack111llll1l_opy_ = bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪတ"), None) and bstack1l11lll1_opy_(
          threading.current_thread(), bstack1ll1lll_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ထ"), None)
  if bstack111llll1l_opy_:
    if not bstack111ll1ll1_opy_():
      logger.warning(bstack1ll1lll_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡰࡱࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡅࡵࡶࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡵࡸࡱࡲࡧࡲࡺ࠰ࠥဒ"))
      return {}
    logger.debug(bstack1ll1lll_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡷࡺࡳ࡭ࡢࡴࡼࠫဓ"))
    logger.debug(perform_scan(driver, driver_command=bstack1ll1lll_opy_ (u"ࠧࡦࡺࡨࡧࡺࡺࡥࡔࡥࡵ࡭ࡵࡺࠧန")))
    results = bstack111lll111_opy_(bstack1ll1lll_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࡔࡷࡰࡱࡦࡸࡹࠣပ"))
    if results is not None and results.get(bstack1ll1lll_opy_ (u"ࠤࡶࡹࡲࡳࡡࡳࡻࠥဖ")) is not None:
        return results[bstack1ll1lll_opy_ (u"ࠥࡷࡺࡳ࡭ࡢࡴࡼࠦဗ")]
    logger.error(bstack1ll1lll_opy_ (u"ࠦࡓࡵࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡓࡧࡶࡹࡱࡺࡳࠡࡕࡸࡱࡲࡧࡲࡺࠢࡺࡥࡸࠦࡦࡰࡷࡱࡨ࠳ࠨဘ"))
    return {}
  if not a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX) or (bstack1l1ll1ll11_opy_ and bstack1lll1lll1_opy_):
    logger.warning(bstack1ll1lll_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡴࡷࡰࡱࡦࡸࡹ࠯ࠤမ"))
    return {}
  try:
    logger.debug(bstack1ll1lll_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡷࡺࡳ࡭ࡢࡴࡼࠫယ"))
    logger.debug(perform_scan(driver))
    bstack11l1lll1_opy_ = driver.execute_async_script(accessibility_scripts.get_results_summary)
    return bstack11l1lll1_opy_
  except Exception:
    logger.error(bstack1ll1lll_opy_ (u"ࠢࡏࡱࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡺࡳ࡭ࡢࡴࡼࠤࡼࡧࡳࠡࡨࡲࡹࡳࡪ࠮ࠣရ"))
    return {}
def bstack111ll1ll1_opy_():
  global CONFIG
  global PLATFORM_INDEX
  bstack1ll11l1l1_opy_ = bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨလ"), None) and bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫဝ"), None)
  if not a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX) or not bstack1ll11l1l1_opy_:
        logger.warning(bstack1ll1lll_opy_ (u"ࠥࡒࡴࡺࠠࡢࡰࠣࡅࡵࡶࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࠡࡴࡨࡷࡺࡲࡴࡴ࠰ࠥသ"))
        return False
  return True
def bstack111lll111_opy_(result_type):
    bstack1lll1l1l1l_opy_ = TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack11llll1l_opy_.current_hook_uuid()
    with ThreadPoolExecutor() as executor:
        future = executor.submit(bstack11ll111lll_opy_(bstack1lll1l1l1l_opy_, result_type))
        try:
            return future.result(timeout=bstack111111ll_opy_)
        except TimeoutError:
            logger.error(bstack1ll1lll_opy_ (u"࡙ࠦ࡯࡭ࡦࡱࡸࡸࠥࡧࡦࡵࡧࡵࠤࢀࢃࡳࠡࡹ࡫࡭ࡱ࡫ࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡕࡩࡸࡻ࡬ࡵࡵࠥဟ").format(bstack111111ll_opy_))
        except Exception as ex:
            logger.debug(bstack1ll1lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡷ࡫ࡴࡳ࡫ࡨࡺ࡮ࡴࡧࠡࡃࡳࡴࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡾࢁ࠳ࠦࡅࡳࡴࡲࡶࠥ࠳ࠠࡼࡿࠥဠ").format(result_type, str(ex)))
    return {}
@measure(event_name=EVENTS.bstack1l1l1l1111_opy_, stage=STAGE.bstack1111l1ll1_opy_, bstack1l1l1l11_opy_=SESSION_NAME)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global PLATFORM_INDEX
  bstack1lll1lll1_opy_ = not (bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪအ"), None) and bstack1l11lll1_opy_(
          threading.current_thread(), bstack1ll1lll_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ဢ"), None))
  bstack11l11ll11l_opy_ = not (bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨဣ"), None) and bstack1l11lll1_opy_(
          threading.current_thread(), bstack1ll1lll_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫဤ"), None))
  bstack1l1ll1ll11_opy_ = getattr(driver, bstack1ll1lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪဥ"), None) != True
  if not a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX) or (bstack1l1ll1ll11_opy_ and bstack1lll1lll1_opy_ and bstack11l11ll11l_opy_):
    logger.warning(bstack1ll1lll_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡺࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡥࡤࡲ࠳ࠨဦ"))
    return {}
  try:
    bstack111l11l1l_opy_ = bstack1ll1lll_opy_ (u"ࠬࡧࡰࡱࠩဧ") in CONFIG and CONFIG.get(bstack1ll1lll_opy_ (u"࠭ࡡࡱࡲࠪဨ"), bstack1ll1lll_opy_ (u"ࠧࠨဩ"))
    session_id = getattr(driver, bstack1ll1lll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠬဪ"), None)
    if not session_id:
      logger.warning(bstack1ll1lll_opy_ (u"ࠤࡑࡳࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡉࡅࠢࡩࡳࡺࡴࡤࠡࡨࡲࡶࠥࡪࡲࡪࡸࡨࡶࠧါ"))
      return {bstack1ll1lll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤာ"): bstack1ll1lll_opy_ (u"ࠦࡓࡵࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡋࡇࠤ࡫ࡵࡵ࡯ࡦࠥိ")}
    if bstack111l11l1l_opy_:
      try:
        bstack1ll11lll_opy_ = {
              bstack1ll1lll_opy_ (u"ࠬࡺࡨࡋࡹࡷࡘࡴࡱࡥ࡯ࠩီ"): os.environ.get(bstack1ll1lll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫု"), os.environ.get(bstack1ll1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫူ"), bstack1ll1lll_opy_ (u"ࠨࠩေ"))),
              bstack1ll1lll_opy_ (u"ࠩࡷ࡬࡙࡫ࡳࡵࡔࡸࡲ࡚ࡻࡩࡥࠩဲ"): TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack11llll1l_opy_.current_hook_uuid(),
              bstack1ll1lll_opy_ (u"ࠪࡥࡺࡺࡨࡉࡧࡤࡨࡪࡸࠧဳ"): os.environ.get(bstack1ll1lll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩဴ")),
              bstack1ll1lll_opy_ (u"ࠬࡹࡣࡢࡰࡗ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬဵ"): str(int(datetime.datetime.now().timestamp() * 1000)),
              bstack1ll1lll_opy_ (u"࠭ࡴࡩࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫံ"): os.environ.get(bstack1ll1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈ့ࠬ"), bstack1ll1lll_opy_ (u"ࠨࠩး")),
              bstack1ll1lll_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥ္ࠩ"): kwargs.get(bstack1ll1lll_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࡢࡧࡴࡳ࡭ࡢࡰࡧ်ࠫ"), None) or bstack1ll1lll_opy_ (u"ࠫࠬျ")
          }
        if not hasattr(thread_local, bstack1ll1lll_opy_ (u"ࠬࡨࡡࡴࡧࡢࡥࡵࡶ࡟ࡢ࠳࠴ࡽࡤࡹࡣࡳ࡫ࡳࡸࠬြ")):
            scripts = {bstack1ll1lll_opy_ (u"࠭ࡳࡤࡣࡱࠫွ"): accessibility_scripts.perform_scan}
            thread_local.base_app_a11y_script = scripts
        bstack1llll1l11l_opy_ = copy.deepcopy(thread_local.base_app_a11y_script)
        bstack1llll1l11l_opy_[bstack1ll1lll_opy_ (u"ࠧࡴࡥࡤࡲࠬှ")] = bstack1llll1l11l_opy_[bstack1ll1lll_opy_ (u"ࠨࡵࡦࡥࡳ࠭ဿ")] % json.dumps(bstack1ll11lll_opy_)
        accessibility_scripts.bstack111lll1111_opy_(bstack1llll1l11l_opy_)
        accessibility_scripts.store()
        bstack11l11l1l1_opy_ = driver.execute_script(accessibility_scripts.perform_scan)
      except Exception as bstack1ll1111l_opy_:
        logger.info(bstack1ll1lll_opy_ (u"ࠤࡄࡴࡵ࡯ࡵ࡮ࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡧࡦࡴࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࠤ၀") + str(bstack1ll1111l_opy_))
        bstack11l11l1l1_opy_ = {bstack1ll1lll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤ၁"): str(bstack1ll1111l_opy_)}
    else:
      bstack11l11l1l1_opy_ = driver.execute_async_script(accessibility_scripts.perform_scan, {bstack1ll1lll_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࠫ၂"): kwargs.get(bstack1ll1lll_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࡤࡩ࡯࡮࡯ࡤࡲࡩ࠭၃"), None) or bstack1ll1lll_opy_ (u"࠭ࠧ၄")})
    return bstack11l11l1l1_opy_
  except Exception as err:
    logger.error(bstack1ll1lll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡶࡺࡴࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡥࡤࡲ࠳ࠦࡻࡾࠤ၅").format(str(err)))
    return {}