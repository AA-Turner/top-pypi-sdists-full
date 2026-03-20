# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
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
from browserstack_sdk.sdk_cli.bstack111l1l1lll_opy_ import bstack11lll11ll_opy_
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from browserstack_sdk.bstack1111l111ll_opy_ import bstack1l11ll1l11_opy_
from browserstack_sdk.bstack1lll11ll1_opy_ import *
import time
import requests
from bstack_utils.constants import EVENTS, STAGE, bstack11ll11111l_opy_
from bstack_utils.messages import bstack11lll11l1l_opy_, bstack1lllll1l1l_opy_, bstack11llll11l1_opy_, bstack1l111l1l1l_opy_, bstack1lll1llll1_opy_, bstack1l1111ll_opy_
from bstack_utils.measure import measure
from bstack_utils.logger_utils import get_logger
from bstack_utils.helper import bstack11l11l11l1_opy_
from browserstack_sdk.bstack1l1l1l11l_opy_ import bstack11ll11l111_opy_
logger = get_logger(__name__)
def bstack11111l1111_opy_():
  global CONFIG
  headers = {
        bstack11lll1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack11lll1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack11l11l11l1_opy_(CONFIG, bstack11ll11111l_opy_)
  try:
    response = requests.get(bstack11ll11111l_opy_, headers=headers, proxies=proxies, timeout=2)
    if response.json():
      bstack1l1l1ll1l_opy_ = response.json()[bstack11lll1_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack11lll11l1l_opy_.format(response.json()))
      return bstack1l1l1ll1l_opy_
    else:
      logger.debug(bstack1lllll1l1l_opy_.format(bstack11lll1_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack1lllll1l1l_opy_.format(e))
def bstack111l1l11ll_opy_(hub_url):
  global CONFIG
  url = bstack11lll1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack11lll1_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack11lll1_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack11lll1_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack11l11l11l1_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=(0.5, 1.0))
    latency = time.perf_counter() - start_time
    logger.debug(bstack11llll11l1_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1l111l1l1l_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack111l1l111l_opy_, stage=STAGE.bstack1lllllll11_opy_)
def bstack11llllllll_opy_():
  try:
    global bstack1llllllll_opy_
    global CONFIG
    if bstack11lll1_opy_ (u"ࠫ࡭ࡻࡢࡓࡧࡪ࡭ࡴࡴࠧࡾ") in CONFIG and CONFIG[bstack11lll1_opy_ (u"ࠬ࡮ࡵࡣࡔࡨ࡫࡮ࡵ࡮ࠨࡿ")]:
      from bstack_utils.constants import bstack11l1l11l_opy_
      bstack1111l1l1l1_opy_ = CONFIG[bstack11lll1_opy_ (u"࠭ࡨࡶࡤࡕࡩ࡬࡯࡯࡯ࠩࢀ")]
      if bstack1111l1l1l1_opy_ in bstack11l1l11l_opy_:
        bstack1llllllll_opy_ = bstack11l1l11l_opy_[bstack1111l1l1l1_opy_]
        logger.debug(bstack1lll1llll1_opy_.format(bstack1llllllll_opy_))
        return
      else:
        logger.debug(bstack11lll1_opy_ (u"ࠢࡉࡷࡥࠤࡰ࡫ࡹࠡࠩࡾࢁࠬࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࡎࡕࡃࡡࡘࡖࡑࡥࡍࡂࡒ࠯ࠤ࡫ࡧ࡬࡭࡫ࡱ࡫ࠥࡨࡡࡤ࡭ࠣࡸࡴࠦ࡯ࡱࡶ࡬ࡱࡦࡲࠠࡩࡷࡥࠤࡩ࡫ࡴࡦࡥࡷ࡭ࡴࡴࠢࢁ").format(bstack1111l1l1l1_opy_))
    bstack1l1l1ll1l_opy_ = bstack11111l1111_opy_()
    from concurrent.futures import ThreadPoolExecutor, as_completed
    if bstack1l1l1ll1l_opy_:
        with ThreadPoolExecutor(max_workers=len(bstack1l1l1ll1l_opy_)) as executor:
            bstack111l111lll_opy_ = {executor.submit(bstack111l1l11ll_opy_, bstack1lll1lll1_opy_): bstack1lll1lll1_opy_ for bstack1lll1lll1_opy_ in bstack1l1l1ll1l_opy_}
            for future in as_completed(bstack111l111lll_opy_):
                result = future.result()
                if result and result.get(bstack11lll1_opy_ (u"ࠨ࡮ࡤࡸࡪࡴࡣࡺࠩࢂ")) is not None:
                    bstack1llllllll_opy_ = result[bstack11lll1_opy_ (u"ࠩ࡫ࡹࡧࡥࡵࡳ࡮ࠪࢃ")]
                    logger.debug(bstack1lll1llll1_opy_.format(bstack1llllllll_opy_))
                    return
        bstack1llllllll_opy_ = bstack1l1l1ll1l_opy_[0]
        logger.debug(bstack1lll1llll1_opy_.format(bstack1llllllll_opy_))
        return
  except Exception as e:
    logger.debug(bstack1l1111ll_opy_.format(e))
from browserstack_sdk.bstack111l1ll11l_opy_ import *
from browserstack_sdk.bstack1l1l1l11l_opy_ import *
from browserstack_sdk.bstack1lll1lll11_opy_ import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.logger_utils import get_logger
from bstack_utils.measure import measure
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack1lll1lll1l_opy_, stage=STAGE.bstack1lllllll11_opy_)
def bstack1ll1ll11ll_opy_():
    global bstack1llllllll_opy_
    try:
        bstack1l1l11ll1_opy_ = bstack11llllll1_opy_()
        bstack11lll11l11_opy_(bstack1l1l11ll1_opy_)
        hub_url = bstack1l1l11ll1_opy_.get(bstack11lll1_opy_ (u"ࠥࡹࡷࡲࠢࢄ"), bstack11lll1_opy_ (u"ࠦࠧࢅ"))
        if hub_url.endswith(bstack11lll1_opy_ (u"ࠬ࠵ࡷࡥ࠱࡫ࡹࡧ࠭ࢆ")):
            hub_url = hub_url.rsplit(bstack11lll1_opy_ (u"࠭࠯ࡸࡦ࠲࡬ࡺࡨࠧࢇ"), 1)[0]
        if hub_url.startswith(bstack11lll1_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࠨ࢈")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack11lll1_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࠪࢉ")):
            hub_url = hub_url[8:]
        bstack1llllllll_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack11llllll1_opy_():
    global CONFIG
    bstack11lll111_opy_ = CONFIG.get(bstack11lll1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢊ"), {}).get(bstack11lll1_opy_ (u"ࠪ࡫ࡷ࡯ࡤࡏࡣࡰࡩࠬࢋ"), bstack11lll1_opy_ (u"ࠫࡓࡕ࡟ࡈࡔࡌࡈࡤࡔࡁࡎࡇࡢࡔࡆ࡙ࡓࡆࡆࠪࢌ"))
    if not isinstance(bstack11lll111_opy_, str):
        raise ValueError(bstack11lll1_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡌࡸࡩࡥࠢࡱࡥࡲ࡫ࠠ࡮ࡷࡶࡸࠥࡨࡥࠡࡣࠣࡺࡦࡲࡩࡥࠢࡶࡸࡷ࡯࡮ࡨࠤࢍ"))
    try:
        bstack1l1l11ll1_opy_ = bstack1l1l1ll11_opy_(bstack11lll111_opy_)
        return bstack1l1l11ll1_opy_
    except Exception as e:
        logger.error(bstack11lll1_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡩࡵ࡭ࡩࠦࡤࡦࡶࡤ࡭ࡱࡹࠠ࠻ࠢࡾࢁࠧࢎ").format(str(e)))
        return {}
def bstack1l1l1ll11_opy_(bstack11lll111_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack11lll1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ࢏")] or not CONFIG[bstack11lll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ࢐")]:
            raise ValueError(bstack11lll1_opy_ (u"ࠤࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠤࡴࡸࠠࡢࡥࡦࡩࡸࡹࠠ࡬ࡧࡼࠦ࢑"))
        url = bstack1111lll1_opy_ + bstack11lll111_opy_
        auth = (CONFIG[bstack11lll1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ࢒")], CONFIG[bstack11lll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ࢓")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack1ll1ll1l1_opy_ = json.loads(response.text)
            return bstack1ll1ll1l1_opy_
    except ValueError as ve:
        logger.error(bstack11lll1_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡩࡵ࡭ࡩࠦࡤࡦࡶࡤ࡭ࡱࡹࠠ࠻ࠢࡾࢁࠧ࢔").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack11lll1_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡪࡶ࡮ࡪࠠࡥࡧࡷࡥ࡮ࡲࡳࠡ࠼ࠣࡿࢂࠨ࢕").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack11lll11l11_opy_(bstack111l1lll11_opy_):
    global CONFIG
    if bstack11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ࢖") not in CONFIG or str(CONFIG[bstack11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬࢗ")]).lower() == bstack11lll1_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ࢘"):
        CONFIG[bstack11lll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭࢙ࠩ")] = False
    elif bstack11lll1_opy_ (u"ࠫ࡮ࡹࡔࡳ࡫ࡤࡰࡌࡸࡩࡥ࢚ࠩ") in bstack111l1lll11_opy_:
        bstack1lll11l1ll_opy_ = CONFIG.get(bstack11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴ࢛ࠩ"), {})
        logger.debug(bstack11lll1_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡸࡪࡵࡷ࡭ࡳ࡭ࠠ࡭ࡱࡦࡥࡱࠦ࡯ࡱࡶ࡬ࡳࡳࡹ࠺ࠡࠧࡶࠦ࢜"), bstack1lll11l1ll_opy_)
        bstack1ll11llll1_opy_ = bstack111l1lll11_opy_.get(bstack11lll1_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡒࡦࡲࡨࡥࡹ࡫ࡲࡴࠤ࢝"), [])
        bstack1lll1l11l1_opy_ = bstack11lll1_opy_ (u"ࠣ࠮ࠥ࢞").join(bstack1ll11llll1_opy_)
        logger.debug(bstack11lll1_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡅࡸࡷࡹࡵ࡭ࠡࡴࡨࡴࡪࡧࡴࡦࡴࠣࡷࡹࡸࡩ࡯ࡩ࠽ࠤࠪࡹࠢ࢟"), bstack1lll1l11l1_opy_)
        bstack1ll1111ll_opy_ = {
            bstack11lll1_opy_ (u"ࠥࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧࢠ"): bstack11lll1_opy_ (u"ࠦࡦࡺࡳ࠮ࡴࡨࡴࡪࡧࡴࡦࡴࠥࢡ"),
            bstack11lll1_opy_ (u"ࠧ࡬࡯ࡳࡥࡨࡐࡴࡩࡡ࡭ࠤࢢ"): bstack11lll1_opy_ (u"ࠨࡴࡳࡷࡨࠦࢣ"),
            bstack11lll1_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࠭ࡳࡧࡳࡩࡦࡺࡥࡳࠤࢤ"): bstack1lll1l11l1_opy_
        }
        bstack1lll11l1ll_opy_.update(bstack1ll1111ll_opy_)
        logger.debug(bstack11lll1_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡖࡲࡧࡥࡹ࡫ࡤࠡ࡮ࡲࡧࡦࡲࠠࡰࡲࡷ࡭ࡴࡴࡳ࠻ࠢࠨࡷࠧࢥ"), bstack1lll11l1ll_opy_)
        CONFIG[bstack11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢦ")] = bstack1lll11l1ll_opy_
        logger.debug(bstack11lll1_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡉ࡭ࡳࡧ࡬ࠡࡅࡒࡒࡋࡏࡇ࠻ࠢࠨࡷࠧࢧ"), CONFIG)
def get_turboscale_playwright_url():
    bstack1l1l11ll1_opy_ = bstack11llllll1_opy_()
    if not bstack1l1l11ll1_opy_[bstack11lll1_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡖࡴ࡯ࠫࢨ")]:
      raise ValueError(bstack11lll1_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡗࡵࡰࠥ࡯ࡳࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡩࡶࡴࡳࠠࡨࡴ࡬ࡨࠥࡪࡥࡵࡣ࡬ࡰࡸ࠴ࠢࢩ"))
    return bstack1l1l11ll1_opy_[bstack11lll1_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡘࡶࡱ࠭ࢪ")] + bstack11lll1_opy_ (u"ࠧࡀࡥࡤࡴࡸࡃࠧࢫ")
@measure(event_name=EVENTS.bstack111111l1l_opy_, stage=STAGE.bstack1lllllll11_opy_)
def bstack11ll1lll1_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack11lll1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪࢬ")], CONFIG[bstack11lll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬࢭ")])
        url = bstack11l11111_opy_
        logger.debug(bstack11lll1_opy_ (u"ࠥࡅࡹࡺࡥ࡮ࡲࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴࠢࡩࡶࡴࡳࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡔࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠣࡅࡕࡏࠢࢮ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack11lll1_opy_ (u"ࠦࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠥࢯ"): bstack11lll1_opy_ (u"ࠧࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠣࢰ")})
            if response.status_code == 200:
                bstack11l111ll_opy_ = json.loads(response.text)
                bstack1111lll11_opy_ = bstack11l111ll_opy_.get(bstack11lll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡸ࠭ࢱ"), [])
                if bstack1111lll11_opy_:
                    bstack1lll1ll1l1_opy_ = bstack1111lll11_opy_[0]
                    build_hashed_id = bstack1lll1ll1l1_opy_.get(bstack11lll1_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪࢲ"))
                    bstack1lll11l11l_opy_ = bstack1111ll11_opy_ + build_hashed_id
                    result.extend([build_hashed_id, bstack1lll11l11l_opy_])
                    logger.info(bstack11ll111ll1_opy_.format(bstack1lll11l11l_opy_))
                    bstack1lll11ll11_opy_ = CONFIG[bstack11lll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫࢳ")]
                    if bstack11lll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࢴ") in CONFIG:
                      bstack1lll11ll11_opy_ += bstack11lll1_opy_ (u"ࠪࠤࠬࢵ") + CONFIG[bstack11lll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࢶ")]
                    if bstack1lll11ll11_opy_ != bstack1lll1ll1l1_opy_.get(bstack11lll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪࢷ")):
                      logger.debug(bstack111l111l_opy_.format(bstack1lll1ll1l1_opy_.get(bstack11lll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫࢸ")), bstack1lll11ll11_opy_))
                    return result
                else:
                    logger.debug(bstack11lll1_opy_ (u"ࠢࡂࡖࡖࠤ࠿ࠦࡎࡰࠢࡥࡹ࡮ࡲࡤࡴࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠱ࠦࢹ"))
            else:
                logger.debug(bstack11lll1_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴ࠰ࠥࢺ"))
        except Exception as e:
            logger.error(bstack11lll1_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࡶࠤ࠿ࠦࡻࡾࠤࢻ").format(str(e)))
    else:
        logger.debug(bstack11lll1_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡆࡓࡓࡌࡉࡈࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡶࡩࡹ࠴ࠠࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴ࠰ࠥࢼ"))
    return [None, None]
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack11l1lll1_opy_ import bstack11l1lll1_opy_, Events, bstack1llll1l1l1_opy_, bstack11ll1l111_opy_
from bstack_utils.measure import bstack1lll11lll_opy_
from bstack_utils.measure import measure
from bstack_utils.percy import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1l11ll1l1_opy_ import bstack11111ll111_opy_
from bstack_utils.messages import *
from bstack_utils import logger_utils
from bstack_utils.constants import *
from bstack_utils.helper import bstack11l111l11l_opy_, bstack11l1lll11_opy_, bstack11111l11ll_opy_, bstack111ll1ll_opy_, \
  bstack1ll111l11l_opy_, \
  Notset, is_robot_playwright_installed, bstack1l1l11l1_opy_, \
  bstack1l1l1llll1_opy_, bstack1ll1lll11l_opy_, bstack1l11l1111l_opy_, bstack11l111111_opy_, bstack1ll11lll_opy_, bstack1llllllll1_opy_, \
  bstack111111l11_opy_, \
  bstack111ll111l_opy_, bstack1l1111l11l_opy_, bstack111lll11l_opy_, bstack1ll1lll1l1_opy_, \
  bstack111llll1l_opy_, bstack111lll11_opy_, bstack1lll11l1_opy_, bstack1l1ll11l1l_opy_, bstack1l1lll1ll_opy_
from bstack_utils.bstack1l1l1ll1_opy_ import bstack1lllll1l11_opy_
from bstack_utils.bstack1l11l111_opy_ import bstack1llllll11_opy_, bstack11l1ll1ll_opy_
from bstack_utils.bstack1l111ll11_opy_ import bstack111lll111_opy_
from bstack_utils.session_utils import bstack11111l11_opy_, bstack1ll11ll1ll_opy_
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.bstack1lll1l11_opy_ import bstack1llll1ll1_opy_
from bstack_utils.proxy import bstack1l11ll1ll_opy_, bstack11l11l11l1_opy_, bstack11111ll1_opy_, bstack1l111l1111_opy_
from bstack_utils.bstack1111l1lll_opy_ import bstack1111l1l1l_opy_, bstack1ll1ll1l11_opy_
import bstack_utils.bstack11l1l1l11l_opy_ as TestHubUtils
import bstack_utils.bstack11111lll11_opy_ as bstack1l11ll1l1l_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.utils.bstack11111l1l1_opy_ import bstack1ll1l1111_opy_
from bstack_utils.bstack1111ll1l_opy_ import bstack11lllllll_opy_
from bstack_utils.bstack1ll111111_opy_ import bstack1l11ll111_opy_
from bstack_utils.bstack1lll11lll_opy_ import bstack1llll11l_opy_
if os.getenv(bstack11lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡉࡑࡒࡏࡘ࠭ࢽ")):
  cli.bstack1111111ll_opy_()
else:
  os.environ[bstack11lll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡊࡒࡓࡐ࡙ࠧࢾ")] = bstack11lll1_opy_ (u"࠭ࡴࡳࡷࡨࠫࢿ")
bstack11ll1l11l_opy_ = bstack11lll1_opy_ (u"ࠧࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠠࠡ࡫ࡩࠬࡵࡧࡧࡦࠢࡀࡁࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠠࡼ࡞ࡱࠤࠥࠦࡴࡳࡻࡾࡠࡳࠦࡣࡰࡰࡶࡸࠥ࡬ࡳࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࡡ࠭ࡦࡴ࡞ࠪ࠭ࡀࡢ࡮ࠡࠢࠣࠤࠥ࡬ࡳ࠯ࡣࡳࡴࡪࡴࡤࡇ࡫࡯ࡩࡘࡿ࡮ࡤࠪࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠬࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡳࡣ࡮ࡴࡤࡦࡺࠬࠤ࠰ࠦࠢ࠻ࠤࠣ࠯ࠥࡐࡓࡐࡐ࠱ࡷࡹࡸࡩ࡯ࡩ࡬ࡪࡾ࠮ࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࠬࡦࡽࡡࡪࡶࠣࡲࡪࡽࡐࡢࡩࡨ࠶࠳࡫ࡶࡢ࡮ࡸࡥࡹ࡫ࠨࠣࠪࠬࠤࡂࡄࠠࡼࡿࠥ࠰ࠥࡢࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡨࡧࡷࡗࡪࡹࡳࡪࡱࡱࡈࡪࡺࡡࡪ࡮ࡶࠦࢂࡢࠧࠪࠫࠬ࡟ࠧ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠣ࡟ࠬࠤ࠰ࠦࠢ࠭࡞࡟ࡲࠧ࠯࡜࡯ࠢࠣࠤࠥࢃࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡽ࡝ࡰࠣࠤ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠧࣀ")
LAUNCH_PATCH_ROBOT_PLAYWRIGHT = bstack11lll1_opy_ (u"ࠨ࡞ࡱ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࡢ࡮ࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠻࡝ࠡ࠿ࡀࡁࠥࡢࠧࡵࡴࡸࡩࡡ࠭࡜࡯ࡥࡲࡲࡸࡺࠠࡣࡵࡷࡥࡨࡱ࡟ࡱࡣࡷ࡬ࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴࡟࡟ࡲࡨࡵ࡮ࡴࡶࠣࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࡝ࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠵ࡢࡢ࡮ࡤࡱࡱࡷࡹࠦࡰࡠ࡫ࡱࡨࡪࡾࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠵ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠵࡟ࠣࡁࡂࡃࠠ࡝ࠩࡷࡶࡺ࡫࡜ࠨ࡞ࡱࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡷࡱ࡯ࡣࡦࠪ࠳࠰ࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠵ࠪ࡞ࡱࡧࡴࡴࡳࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣࠫ࠾ࡠࡳࡩ࡯࡯ࡵࡷࠤࡴࡸࡩࡨ࡫ࡱࡥࡱࡥࡣࡩࡴࡲࡱ࡮ࡻ࡭ࡠ࡮ࡤࡹࡳࡩࡨࠡ࠿ࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡰࡦࡻ࡮ࡤࡪ࠱ࡦ࡮ࡴࡤࠩ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭ࠪ࠽࡟ࡲ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡱࡧࡵ࡯ࡥ࡫ࠤࡂࠦࡡࡴࡻࡱࡧࠥ࠮࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸ࠯ࠠ࠾ࡀࠣࡿࡡࡴࡩࡧࠢࠫࠥࡧࡹࡴࡢࡥ࡮ࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠪࠢࡾࡠࡳࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦ࡯ࡳ࡫ࡪ࡭ࡳࡧ࡬ࡠࡥ࡫ࡶࡴࡳࡩࡶ࡯ࡢࡰࡦࡻ࡮ࡤࡪࠫࡰࡦࡻ࡮ࡤࡪࡒࡴࡹ࡯࡯࡯ࡵࠬ࠿ࡡࡴࡽ࡝ࡰ࡯ࡩࡹࠦࡣࡢࡲࡶ࠿ࡡࡴࡴࡳࡻࠣࡿࡡࡴࡣࡢࡲࡶࠤࡂࠦࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠪ࡞ࡱࠤࠥࢃࠠࡤࡣࡷࡧ࡭࠮ࡥࡹࠫࠣࡿࡡࡴࠠࠡࠢࠣࢁࡡࡴࠠࠡ࡫ࡩࠤ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࠮ࠦࡻ࡝ࡰࠣࠤࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡩ࡯࡯ࡰࡨࡧࡹࡕࡶࡦࡴࡆࡈࡕ࠮ࡻ࡝ࡰࠣࠤࠥࠦࠠࠡࡧࡱࡨࡵࡵࡩ࡯ࡶࡘࡖࡑࡀࠠࡡࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠧࡿࡪࡴࡣࡰࡦࡨ࡙ࡗࡏࡃࡰ࡯ࡳࡳࡳ࡫࡮ࡵࠪࡍࡗࡔࡔ࠮ࡴࡶࡵ࡭ࡳ࡭ࡩࡧࡻࠫࡧࡦࡶࡳࠪࠫࢀࡤ࠱ࡢ࡮ࠡࠢࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴ࡞ࡱࠤࠥࠦࠠࡾࠫ࡟ࡲࠥࠦࡽ࡝ࡰࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࠻ࠢࡣࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠩࢁࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭ࢂࡦࠬ࡝ࡰࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴ࡞ࡱࠤࠥࢃࠩ࡝ࡰࢀࡠࡳࡩ࡯࡯ࡵࡷࠤࡴࡸࡩࡨ࡫ࡱࡥࡱࡥࡣࡰࡰࡱࡩࡨࡺࠠ࠾ࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱ࠮ࡤࡪࡵࡳࡲ࡯ࡵ࡮࠰ࡦࡳࡳࡴࡥࡤࡶ࠱ࡦ࡮ࡴࡤࠩ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭ࠪ࠽࡟ࡲ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡨࡵ࡮࡯ࡧࡦࡸࠥࡃࠠࡢࡵࡼࡲࡨࠦࠨࡤࡱࡱࡲࡪࡩࡴࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁ࡜࡯ࠢࠣ࡭࡫ࠦࠨࠢࡤࡶࡸࡦࡩ࡫ࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠮ࠦࡻ࡝ࡰࠣࠤࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥࡵࡲࡪࡩ࡬ࡲࡦࡲ࡟ࡤࡱࡱࡲࡪࡩࡴࠩࡥࡲࡲࡳ࡫ࡣࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠫ࠾ࡠࡳࠦࠠࡾ࡞ࡱࠤࠥࡲࡥࡵࠢࡦࡥࡵࡹ࠻࡝ࡰࠣࠤࡹࡸࡹࠡࡽ࡟ࡲࠥࠦࠠࠡࡥࡤࡴࡸࠦ࠽ࠡࡌࡖࡓࡓ࠴ࡰࡢࡴࡶࡩ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡩࡡࡱࡵࠬࡠࡳࠦࠠࡾࠢࡦࡥࡹࡩࡨࠩࡧࡻ࠭ࠥࢁ࡜࡯ࠢࠣࢁࡡࡴࠠࠡࡥࡲࡲࡸࡺࠠ࡮ࡱࡧ࡭࡫࡯ࡥࡥࡇࡱࡨࡵࡵࡩ࡯ࡶࠣࡁࠥࡦࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࡡࠢ࠮ࠤࡪࡴࡣࡰࡦࡨ࡙ࡗࡏࡃࡰ࡯ࡳࡳࡳ࡫࡮ࡵࠪࡍࡗࡔࡔ࠮ࡴࡶࡵ࡭ࡳ࡭ࡩࡧࡻࠫࡧࡦࡶࡳࠪࠫ࠾ࡠࡳࠦࠠࡪࡨࠣࠬࡧࡹࡴࡢࡥ࡮ࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ࠭ࠥࢁ࡜࡯ࠢࠣࠤࠥࡸࡥࡵࡷࡵࡲࠥࡧࡷࡢ࡫ࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡨࡵ࡮࡯ࡧࡦࡸࡔࡼࡥࡳࡅࡇࡔ࠭ࢁ࡜࡯ࠢࠣࠤࠥࠦࠠࡦࡰࡧࡴࡴ࡯࡮ࡵࡗࡕࡐ࠿ࠦ࡭ࡰࡦ࡬ࡪ࡮࡫ࡤࡆࡰࡧࡴࡴ࡯࡮ࡵ࠮࡟ࡲࠥࠦࠠࠡࠢࠣ࠲࠳࠴ࡣࡰࡰࡱࡩࡨࡺࡏࡱࡶ࡬ࡳࡳࡹ࡜࡯ࠢࠣࠤࠥࢃࠩ࡝ࡰࠣࠤࢂࡢ࡮ࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤ࠳࠴࠮ࡤࡱࡱࡲࡪࡩࡴࡐࡲࡷ࡭ࡴࡴࡳ࠭࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࡝ࡰࠣࠤࢂ࠯࡜࡯ࡿ࡟ࡲࡱ࡫ࡴࠡࡄࡵࡳࡼࡹࡥࡳࡅࡲࡲࡹ࡫ࡸࡵ࠽࡟ࡲࡹࡸࡹࠡࡽ࡟ࡲࠥࠦࡣࡰࡰࡶࡸࠥࡶࡡࡵࡪࡐࡳࡩࡻ࡬ࡦࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭ࠨࡰࡢࡶ࡫ࠦ࠮ࡁ࡜࡯ࠢࠣࡧࡴࡴࡳࡵࠢࡳࡻࡈࡵࡲࡦࡒࡤࡸ࡭ࠦ࠽ࠡࡲࡤࡸ࡭ࡓ࡯ࡥࡷ࡯ࡩ࠳ࡪࡩࡳࡰࡤࡱࡪ࠮ࡲࡦࡳࡸ࡭ࡷ࡫࠮ࡳࡧࡶࡳࡱࡼࡥࠩࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠳ࡣࡰࡴࡨ࠳ࡵࡧࡣ࡬ࡣࡪࡩ࠳ࡰࡳࡰࡰࠥ࠭࠮ࡁ࡜࡯ࠢࠣࡆࡷࡵࡷࡴࡧࡵࡇࡴࡴࡴࡦࡺࡷࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨࡱࡣࡷ࡬ࡒࡵࡤࡶ࡮ࡨ࠲࡯ࡵࡩ࡯ࠪࡳࡻࡈࡵࡲࡦࡒࡤࡸ࡭࠲ࠠࠣ࡮࡬ࡦ࠴ࡩ࡬ࡪࡧࡱࡸ࠴ࡨࡲࡰࡹࡶࡩࡷࡉ࡯࡯ࡶࡨࡼࡹࠨࠩࠪ࠰ࡅࡶࡴࡽࡳࡦࡴࡆࡳࡳࡺࡥࡹࡶ࠾ࡠࡳࢃࠠࡤࡣࡷࡧ࡭ࠦࠨࡦࠫࠣࡿࡡࡴࠠࠡࡥࡲࡲࡸࡵ࡬ࡦ࠰ࡺࡥࡷࡴࠨࠣࡅࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡱࡵࡡࡥࠢࡅࡶࡴࡽࡳࡦࡴࡆࡳࡳࡺࡥࡹࡶࠣࡪࡷࡵ࡭ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠲ࡩ࡯ࡳࡧ࠽ࠦ࠱ࠦࡥ࠯࡯ࡨࡷࡸࡧࡧࡦࠫ࠾ࡠࡳࢃ࡜࡯ࡥࡲࡲࡸࡺࠠࡰࡴ࡬࡫࡮ࡴࡡ࡭ࡡࡱࡩࡼࡖࡡࡨࡧࠣࡁࠥࡈࡲࡰࡹࡶࡩࡷࡉ࡯࡯ࡶࡨࡼࡹ࠴ࡰࡳࡱࡷࡳࡹࡿࡰࡦ࠰ࡱࡩࡼࡖࡡࡨࡧ࠾ࡠࡳࡈࡲࡰࡹࡶࡩࡷࡉ࡯࡯ࡶࡨࡼࡹ࠴ࡰࡳࡱࡷࡳࡹࡿࡰࡦ࠰ࡱࡩࡼࡖࡡࡨࡧࠣࡁࠥࡧࡳࡺࡰࡦࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠮ࠩࠡࡽ࡟ࡲࠥࠦࡩࡧࠢࠫࡦࡸࡺࡡࡤ࡭ࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠬࠤࢀࡢ࡮ࠡࠢࠣࠤࡹࡸࡹࠡࡽ࡟ࡲࠥࠦࠠࠡࠢࠣࡧࡴࡴࡳࡵࠢࡥࡶࡴࡽࡳࡦࡴࠣࡁࠥࡺࡨࡪࡵ࠱ࡦࡷࡵࡷࡴࡧࡵࠤࠫࠬࠠࡵࡪ࡬ࡷ࠳ࡨࡲࡰࡹࡶࡩࡷ࠮ࠩ࠼࡞ࡱࠤࠥࠦࠠࠡࠢ࡯ࡩࡹࠦࡰࡳ࡫ࡰࡥࡷࡿࡃࡰࡰࡷࡩࡽࡺࠠ࠾ࠢࡥࡶࡴࡽࡳࡦࡴࠣࠪࠫࠦࡴࡺࡲࡨࡳ࡫ࠦࡢࡳࡱࡺࡷࡪࡸ࠮ࡤࡱࡱࡸࡪࡾࡴࡴࠢࡀࡁࡂࠦ࡜ࠨࡨࡸࡲࡨࡺࡩࡰࡰ࡟ࠫࠥࡅࠠࡣࡴࡲࡻࡸ࡫ࡲ࠯ࡥࡲࡲࡹ࡫ࡸࡵࡵࠫ࠭ࡠ࠶࡝ࠡ࠼ࠣࡲࡺࡲ࡬࠼࡞ࡱࠤࠥࠦࠠࠡࠢ࡬ࡪࠥ࠮ࠡࡱࡴ࡬ࡱࡦࡸࡹࡄࡱࡱࡸࡪࡾࡴࠡࠨࠩࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࠬࠦࠡࡶࡼࡴࡪࡵࡦࠡࡤࡵࡳࡼࡹࡥࡳ࠰ࡱࡩࡼࡉ࡯࡯ࡶࡨࡼࡹࠦ࠽࠾࠿ࠣࡠࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡜ࠨࠫࠣࡿࡡࡴࠠࠡࠢࠣࠤࠥࠦࠠࡱࡴ࡬ࡱࡦࡸࡹࡄࡱࡱࡸࡪࡾࡴࠡ࠿ࠣࡥࡼࡧࡩࡵࠢࡥࡶࡴࡽࡳࡦࡴ࠱ࡲࡪࡽࡃࡰࡰࡷࡩࡽࡺࠨࠪ࠽࡟ࡲࠥࠦࠠࠡࠢࠣࢁࡡࡴࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡵࡷࠤࡹࡧࡲࡨࡧࡷࡇࡴࡴࡴࡦࡺࡷࠤࡂࠦࡰࡳ࡫ࡰࡥࡷࡿࡃࡰࡰࡷࡩࡽࡺࠠࡽࡾࠣࡸ࡭࡯ࡳ࠼࡞ࡱࠤࠥࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡲࡪࡽࡐࡢࡩࡨ࠲ࡨࡧ࡬࡭ࠪࡷࡥࡷ࡭ࡥࡵࡅࡲࡲࡹ࡫ࡸࡵࠫ࠾ࡠࡳࠦࠠࠡࠢࢀࠤࡨࡧࡴࡤࡪࠣࠬࡪ࠯ࠠࡼ࡞ࡱࠤࠥࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡲࡪࡽࡐࡢࡩࡨ࠲ࡨࡧ࡬࡭ࠪࡷ࡬࡮ࡹࠩ࠼࡞ࡱࠤࠥࠦࠠࡾ࡞ࡱࠤࠥࢃࠠ࡝ࡰࠣࠤࡪࡲࡳࡦࠢࡾࡠࡳࠦࠠࠡࠢࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣࡳࡷ࡯ࡧࡪࡰࡤࡰࡤࡴࡥࡸࡒࡤ࡫ࡪ࠴ࡣࡢ࡮࡯ࠬࡹ࡮ࡩࡴࠫ࠾ࡠࡳࠦࠠࡾ࡞ࡱࢁࡀࡢ࡮࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱࡟ࡲࠬࣁ")
from ._version import __version__
bstack11111111l_opy_ = None
CONFIG = {}
bstack11111lll_opy_ = {}
bstack111111ll1_opy_ = {}
bstack1l11l111l1_opy_ = None
bstack1l1llll1l1_opy_ = None
SESSION_NAME = None
PLATFORM_INDEX = -1
bstack111l111ll_opy_ = 0
bstack11ll1111l1_opy_ = bstack1lll1l111l_opy_
bstack1l11ll11_opy_ = 1
PARALLELISE_VANILLA_PYTHON = False
PARALLELISE_THREADING_PYTHON = False
FRAMEWORK_NAME = bstack11lll1_opy_ (u"ࠩࠪࣂ")
bstack111l11l1l1_opy_ = bstack11lll1_opy_ (u"ࠪࠫࣃ")
bstack1ll11l11_opy_ = False
BROWSERSTACK_AUTOMATION = True
bstack1111lll1ll_opy_ = False
bstack1l1l1lll1l_opy_ = bstack11lll1_opy_ (u"ࠫࠬࣄ")
bstack1ll111ll1l_opy_ = []
bstack1111lll11l_opy_ = threading.Lock()
bstack11ll11ll_opy_ = threading.Lock()
bstack11ll1ll11l_opy_ = None
bstack1llllllll_opy_ = bstack11lll1_opy_ (u"ࠬ࠭ࣅ")
SELENIUM_OR_PLAYWRIGHT_INSTALLED = False
bstack1l1l111lll_opy_ = None
bstack11l11l111l_opy_ = None
bstack1lll1lll_opy_ = None
bstack1l11l1l1l_opy_ = -1
bstack1111111l_opy_ = os.path.join(os.path.expanduser(bstack11lll1_opy_ (u"࠭ࡾࠨࣆ")), bstack11lll1_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧࣇ"), bstack11lll1_opy_ (u"ࠨ࠰ࡵࡳࡧࡵࡴ࠮ࡴࡨࡴࡴࡸࡴ࠮ࡪࡨࡰࡵ࡫ࡲ࠯࡬ࡶࡳࡳ࠭ࣈ"))
bstack1l1lllll1l_opy_ = 0
bstack1l1l1lll11_opy_ = 0
bstack111l1llll_opy_ = []
bstack11l1l1111_opy_ = []
ROBOT_PYTHON_ERRORS = []
bstack1lll1111l1_opy_ = []
bstack11l11l1l1l_opy_ = bstack11lll1_opy_ (u"ࠩࠪࣉ")
bstack1l11lllll1_opy_ = bstack11lll1_opy_ (u"ࠪࠫ࣊")
bstack1ll1l11l_opy_ = False
bstack1ll1l111l1_opy_ = False
bstack11llll1lll_opy_ = {}
bstack11111l1l1l_opy_ = {}
bstack1l11l11l_opy_ = None
bstack1l1ll111l1_opy_ = None
bstack1111l1l1_opy_ = None
bstack11ll1llll_opy_ = None
bstack11l11ll1l_opy_ = None
bstack11lll1llll_opy_ = None
bstack1llll1l11l_opy_ = None
bstack11ll1111ll_opy_ = None
bstack111111l1ll_opy_ = None
bstack1l1llllll1_opy_ = None
bstack111llll1ll_opy_ = None
bstack1ll111l111_opy_ = None
bstack1l1l11l1l_opy_ = None
bstack11lll1ll1_opy_ = None
bstack1l1111l1l_opy_ = None
bstack1l1l11l111_opy_ = None
bstack1l11l1llll_opy_ = None
bstack11llll11ll_opy_ = None
bstack1llll1111_opy_ = None
bstack1ll1ll1l_opy_ = None
bstack111l11ll1l_opy_ = None
bstack1ll11l1ll_opy_ = None
bstack11l1ll1l1_opy_ = None
thread_local = threading.local()
bstack11ll1l1l1l_opy_ = False
bstack11111l1lll_opy_ = bstack11lll1_opy_ (u"ࠦࠧ࣋")
_1l1lll1lll_opy_ = None
logger = logger_utils.get_logger(__name__, bstack11ll1111l1_opy_)
automation_logger = logger_utils.get_automation_logger(__name__)
global_config = Config.get_instance()
percy = bstack1l1ll11l11_opy_()
bstack1ll1l1llll_opy_ = bstack11111ll111_opy_()
bstack111l11l1_opy_ = bstack1lll1lll11_opy_()
def bstack111l11l11l_opy_():
  global CONFIG
  global bstack1ll1l11l_opy_
  global global_config
  testContextOptions = bstack1l1111l1l1_opy_(CONFIG)
  if bstack1ll111l11l_opy_(CONFIG):
    if (bstack11lll1_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ࣌") in testContextOptions and str(testContextOptions[bstack11lll1_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ࣍")]).lower() == bstack11lll1_opy_ (u"ࠧࡵࡴࡸࡩࠬ࣎")):
      bstack1ll1l11l_opy_ = True
      global_config.bstack1ll1l11l1l_opy_(True)
    if (bstack11lll1_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷ࣏ࠬ") in testContextOptions and str(testContextOptions[bstack11lll1_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࣐࠭")]).lower() == bstack11lll1_opy_ (u"ࠪࡸࡷࡻࡥࠨ࣑")):
      global_config.bstack111111ll_opy_(True)
  else:
    bstack1ll1l11l_opy_ = True
    global_config.bstack1ll1l11l1l_opy_(True)
    global_config.bstack111111ll_opy_(True)
def bstack11l1l111l1_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1ll11lll11_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack11ll1111_opy_():
  global bstack11111l1l1l_opy_
  args = sys.argv
  for i in range(len(args)):
    if bstack11lll1_opy_ (u"ࠦ࠲࠳ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡨࡵ࡮ࡧ࡫ࡪࡪ࡮ࡲࡥ࣒ࠣ") == args[i].lower() or bstack11lll1_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰࡰࡩ࡭࡬ࠨ࣓") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      bstack11111l1l1l_opy_[bstack11lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࡤࡌࡉࡍࡇࠪࣔ")] = path
      return path
  return None
bstack11l1l1lll_opy_ = re.compile(bstack11lll1_opy_ (u"ࡲࠣ࠰࠭ࡃࡡࠪࡻࠩ࠰࠭ࡃ࠮ࢃ࠮ࠫࡁࠥࣕ"))
def bstack11ll1l11ll_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack11l1l1lll_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack11lll1_opy_ (u"ࠣࠦࡾࠦࣖ") + group + bstack11lll1_opy_ (u"ࠤࢀࠦࣗ"), os.environ.get(group))
  return value
def bstack1ll1111ll1_opy_():
  global bstack11l1ll1l1_opy_
  if bstack11l1ll1l1_opy_ is None:
        bstack11l1ll1l1_opy_ = bstack11ll1111_opy_()
  bstack1l1l1l1l11_opy_ = bstack11l1ll1l1_opy_
  if bstack1l1l1l1l11_opy_ and os.path.exists(os.path.abspath(bstack1l1l1l1l11_opy_)):
    fileName = bstack1l1l1l1l11_opy_
  if bstack11lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋࠧࣘ") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack11lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨࣙ")])) and not bstack11lll1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡑࡥࡲ࡫ࠧࣚ") in locals():
    fileName = os.environ[bstack11lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࡤࡌࡉࡍࡇࠪࣛ")]
  if bstack11lll1_opy_ (u"ࠧࡧ࡫࡯ࡩࡓࡧ࡭ࡦࠩࣜ") in locals():
    bstack11111l1_opy_ = os.path.abspath(fileName)
  else:
    bstack11111l1_opy_ = bstack11lll1_opy_ (u"ࠨࠩࣝ")
  bstack11l11l1l1_opy_ = os.getcwd()
  bstack111llll1l1_opy_ = bstack11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬࣞ")
  bstack1111ll11l_opy_ = bstack11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡥࡲࡲࠧࣟ")
  while (not os.path.exists(bstack11111l1_opy_)) and bstack11l11l1l1_opy_ != bstack11lll1_opy_ (u"ࠦࠧ࣠"):
    bstack11111l1_opy_ = os.path.join(bstack11l11l1l1_opy_, bstack111llll1l1_opy_)
    if not os.path.exists(bstack11111l1_opy_):
      bstack11111l1_opy_ = os.path.join(bstack11l11l1l1_opy_, bstack1111ll11l_opy_)
    if bstack11l11l1l1_opy_ != os.path.dirname(bstack11l11l1l1_opy_):
      bstack11l11l1l1_opy_ = os.path.dirname(bstack11l11l1l1_opy_)
    else:
      bstack11l11l1l1_opy_ = bstack11lll1_opy_ (u"ࠧࠨ࣡")
  bstack11l1ll1l1_opy_ = bstack11111l1_opy_ if os.path.exists(bstack11111l1_opy_) else None
  return bstack11l1ll1l1_opy_
def bstack11l11llll_opy_(config):
    if bstack11lll1_opy_ (u"࠭ࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬࠭࣢") in config:
      config[bstack11lll1_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࣣࠫ")] = config[bstack11lll1_opy_ (u"ࠨࡶࡨࡷࡹࡘࡥࡱࡱࡵࡸ࡮ࡴࡧࠨࣤ")]
    if bstack11lll1_opy_ (u"ࠩࡷࡩࡸࡺࡒࡦࡲࡲࡶࡹ࡯࡮ࡨࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣥ") in config:
      config[bstack11lll1_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࣦࠧ")] = config[bstack11lll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࡓࡵࡺࡩࡰࡰࡶࠫࣧ")]
def bstack1l11lllll_opy_():
  bstack11111l1_opy_ = bstack1ll1111ll1_opy_()
  if not os.path.exists(bstack11111l1_opy_):
    bstack11l1111ll1_opy_(
      bstack11ll111ll_opy_.format(os.getcwd()))
  try:
    with open(bstack11111l1_opy_, bstack11lll1_opy_ (u"ࠬࡸࠧࣨ")) as stream:
      yaml.add_implicit_resolver(bstack11lll1_opy_ (u"ࠨࠡࡱࡣࡷ࡬ࡪࡾࣩࠢ"), bstack11l1l1lll_opy_)
      yaml.add_constructor(bstack11lll1_opy_ (u"ࠢࠢࡲࡤࡸ࡭࡫ࡸࠣ࣪"), bstack11ll1l11ll_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      bstack11l11llll_opy_(config)
      return config
  except:
    with open(bstack11111l1_opy_, bstack11lll1_opy_ (u"ࠨࡴࠪ࣫")) as stream:
      try:
        config = yaml.safe_load(stream)
        bstack11l11llll_opy_(config)
        return config
      except yaml.YAMLError as exc:
        bstack11l1111ll1_opy_(bstack1l1l1lllll_opy_.format(str(exc)))
def bstack11ll111l1l_opy_(config):
  bstack11111llll1_opy_ = bstack11l111l11_opy_(config)
  for option in list(bstack11111llll1_opy_):
    if option.lower() in bstack111ll1llll_opy_ and option != bstack111ll1llll_opy_[option.lower()]:
      bstack11111llll1_opy_[bstack111ll1llll_opy_[option.lower()]] = bstack11111llll1_opy_[option]
      del bstack11111llll1_opy_[option]
  return config
def bstack11l11lllll_opy_():
  global bstack111111ll1_opy_
  for key, bstack111lll111l_opy_ in bstack111ll1ll1l_opy_.items():
    if isinstance(bstack111lll111l_opy_, list):
      for var in bstack111lll111l_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack111111ll1_opy_[key] = os.environ[var]
          break
    elif bstack111lll111l_opy_ in os.environ and os.environ[bstack111lll111l_opy_] and str(os.environ[bstack111lll111l_opy_]).strip():
      bstack111111ll1_opy_[key] = os.environ[bstack111lll111l_opy_]
  if bstack11lll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ࣬") in os.environ:
    bstack111111ll1_opy_[bstack11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹ࣭ࠧ")] = {}
    bstack111111ll1_opy_[bstack11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ࣮")][bstack11lll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣯ࠧ")] = os.environ[bstack11lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨࣰ")]
def bstack111lll1111_opy_():
  global bstack11111lll_opy_
  global bstack1l1l1lll1l_opy_
  global bstack11111l1l1l_opy_
  bstack111ll1111_opy_ = []
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) - 1 and bstack11lll1_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࣱࠪ").lower() == val.lower():
      bstack11111lll_opy_[bstack11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࣲࠬ")] = {}
      bstack11111lll_opy_[bstack11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࣳ")][bstack11lll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣴ")] = sys.argv[idx + 1]
      bstack111ll1111_opy_.extend([idx, idx + 1])
      break
  for key, bstack11lllll11_opy_ in bstack1l111llll_opy_.items():
    if isinstance(bstack11lllll11_opy_, list):
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        for var in bstack11lllll11_opy_:
          if bstack11lll1_opy_ (u"ࠫ࠲࠳ࠧࣵ") + var.lower() == val.lower() and key not in bstack11111lll_opy_:
            bstack11111lll_opy_[key] = sys.argv[idx + 1]
            bstack1l1l1lll1l_opy_ += bstack11lll1_opy_ (u"ࠬࠦ࠭࠮ࣶࠩ") + var + bstack11lll1_opy_ (u"࠭ࠠࠨࣷ") + shlex.quote(sys.argv[idx + 1])
            bstack1l1lll1ll_opy_(bstack11111l1l1l_opy_, key, sys.argv[idx + 1])
            bstack111ll1111_opy_.extend([idx, idx + 1])
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        if bstack11lll1_opy_ (u"ࠧ࠮࠯ࠪࣸ") + bstack11lllll11_opy_.lower() == val.lower() and key not in bstack11111lll_opy_:
          bstack11111lll_opy_[key] = sys.argv[idx + 1]
          bstack1l1l1lll1l_opy_ += bstack11lll1_opy_ (u"ࠨࠢ࠰࠱ࣹࠬ") + bstack11lllll11_opy_ + bstack11lll1_opy_ (u"ࣺࠩࠣࠫ") + shlex.quote(sys.argv[idx + 1])
          bstack1l1lll1ll_opy_(bstack11111l1l1l_opy_, key, sys.argv[idx + 1])
          bstack111ll1111_opy_.extend([idx, idx + 1])
  for idx in sorted(set(bstack111ll1111_opy_), reverse=True):
    if idx < len(sys.argv):
      del sys.argv[idx]
def bstack11l11l1l_opy_(config):
  bstack1l1ll1llll_opy_ = config.keys()
  for bstack1llll1ll11_opy_, bstack1lll111ll1_opy_ in bstack111l1111ll_opy_.items():
    if bstack1lll111ll1_opy_ in bstack1l1ll1llll_opy_:
      config[bstack1llll1ll11_opy_] = config[bstack1lll111ll1_opy_]
      del config[bstack1lll111ll1_opy_]
  for bstack1llll1ll11_opy_, bstack1lll111ll1_opy_ in bstack111l1l1l1_opy_.items():
    if isinstance(bstack1lll111ll1_opy_, list):
      for bstack1ll111l1l1_opy_ in bstack1lll111ll1_opy_:
        if bstack1ll111l1l1_opy_ in bstack1l1ll1llll_opy_:
          config[bstack1llll1ll11_opy_] = config[bstack1ll111l1l1_opy_]
          del config[bstack1ll111l1l1_opy_]
          break
    elif bstack1lll111ll1_opy_ in bstack1l1ll1llll_opy_:
      config[bstack1llll1ll11_opy_] = config[bstack1lll111ll1_opy_]
      del config[bstack1lll111ll1_opy_]
  for bstack1ll111l1l1_opy_ in list(config):
    for bstack1l11ll1l_opy_ in bstack1ll11111_opy_:
      if bstack1ll111l1l1_opy_.lower() == bstack1l11ll1l_opy_.lower() and bstack1ll111l1l1_opy_ != bstack1l11ll1l_opy_:
        config[bstack1l11ll1l_opy_] = config[bstack1ll111l1l1_opy_]
        del config[bstack1ll111l1l1_opy_]
  bstack1l1l111ll1_opy_ = [{}]
  if not config.get(bstack11lll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣻ")):
    config[bstack11lll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣼ")] = [{}]
  bstack1l1l111ll1_opy_ = config[bstack11lll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨࣽ")]
  for platform in bstack1l1l111ll1_opy_:
    for bstack1ll111l1l1_opy_ in list(platform):
      for bstack1l11ll1l_opy_ in bstack1ll11111_opy_:
        if bstack1ll111l1l1_opy_.lower() == bstack1l11ll1l_opy_.lower() and bstack1ll111l1l1_opy_ != bstack1l11ll1l_opy_:
          platform[bstack1l11ll1l_opy_] = platform[bstack1ll111l1l1_opy_]
          del platform[bstack1ll111l1l1_opy_]
  for bstack1llll1ll11_opy_, bstack1lll111ll1_opy_ in bstack111l1l1l1_opy_.items():
    for platform in bstack1l1l111ll1_opy_:
      if isinstance(bstack1lll111ll1_opy_, list):
        for bstack1ll111l1l1_opy_ in bstack1lll111ll1_opy_:
          if bstack1ll111l1l1_opy_ in platform:
            platform[bstack1llll1ll11_opy_] = platform[bstack1ll111l1l1_opy_]
            del platform[bstack1ll111l1l1_opy_]
            break
      elif bstack1lll111ll1_opy_ in platform:
        platform[bstack1llll1ll11_opy_] = platform[bstack1lll111ll1_opy_]
        del platform[bstack1lll111ll1_opy_]
  for bstack1ll1ll1ll1_opy_ in bstack1llll11l1l_opy_:
    if bstack1ll1ll1ll1_opy_ in config:
      if not bstack1llll11l1l_opy_[bstack1ll1ll1ll1_opy_] in config:
        config[bstack1llll11l1l_opy_[bstack1ll1ll1ll1_opy_]] = {}
      config[bstack1llll11l1l_opy_[bstack1ll1ll1ll1_opy_]].update(config[bstack1ll1ll1ll1_opy_])
      del config[bstack1ll1ll1ll1_opy_]
  for platform in bstack1l1l111ll1_opy_:
    for bstack1ll1ll1ll1_opy_ in bstack1llll11l1l_opy_:
      if bstack1ll1ll1ll1_opy_ in list(platform):
        if not bstack1llll11l1l_opy_[bstack1ll1ll1ll1_opy_] in platform:
          platform[bstack1llll11l1l_opy_[bstack1ll1ll1ll1_opy_]] = {}
        platform[bstack1llll11l1l_opy_[bstack1ll1ll1ll1_opy_]].update(platform[bstack1ll1ll1ll1_opy_])
        del platform[bstack1ll1ll1ll1_opy_]
  config = bstack11ll111l1l_opy_(config)
  return config
def bstack11l111llll_opy_(config):
  global bstack111l11l1l1_opy_
  bstack1l11llll1_opy_ = False
  if bstack11lll1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪࣾ") in config and str(config[bstack11lll1_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫࣿ")]).lower() != bstack11lll1_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧऀ"):
    if bstack11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ँ") not in config or str(config[bstack11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧं")]).lower() == bstack11lll1_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪः"):
      config[bstack11lll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫऄ")] = False
    else:
      bstack1l1l11ll1_opy_ = bstack11llllll1_opy_()
      if bstack11lll1_opy_ (u"࠭ࡩࡴࡖࡵ࡭ࡦࡲࡇࡳ࡫ࡧࠫअ") in bstack1l1l11ll1_opy_:
        if not bstack11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫआ") in config:
          config[bstack11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬइ")] = {}
        config[bstack11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ई")][bstack11lll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬउ")] = bstack11lll1_opy_ (u"ࠫࡦࡺࡳ࠮ࡴࡨࡴࡪࡧࡴࡦࡴࠪऊ")
        bstack1l11llll1_opy_ = True
        bstack111l11l1l1_opy_ = config[bstack11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩऋ")].get(bstack11lll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨऌ"))
  if bstack1ll111l11l_opy_(config) and bstack11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫऍ") in config and str(config[bstack11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬऎ")]).lower() != bstack11lll1_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨए") and not bstack1l11llll1_opy_:
    if not bstack11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧऐ") in config:
      config[bstack11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऑ")] = {}
    if not config[bstack11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩऒ")].get(bstack11lll1_opy_ (u"࠭ࡳ࡬࡫ࡳࡆ࡮ࡴࡡࡳࡻࡌࡲ࡮ࡺࡩࡢ࡮࡬ࡷࡦࡺࡩࡰࡰࠪओ")) and not bstack11lll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऔ") in config[bstack11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬक")]:
      current_time = datetime.datetime.now()
      bstack11lll1l111_opy_ = current_time.strftime(bstack11lll1_opy_ (u"ࠩࠨࡨࡤࠫࡢࡠࠧࡋࠩࡒ࠭ख"))
      hostname = socket.gethostname()
      bstack1ll11l1l1l_opy_ = bstack11lll1_opy_ (u"ࠪࠫग").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack11lll1_opy_ (u"ࠫࢀࢃ࡟ࡼࡿࡢࡿࢂ࠭घ").format(bstack11lll1l111_opy_, hostname, bstack1ll11l1l1l_opy_)
      config[bstack11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩङ")][bstack11lll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨच")] = identifier
    bstack111l11l1l1_opy_ = config[bstack11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫछ")].get(bstack11lll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪज"))
  return config
def bstack11l11llll1_opy_():
  bstack1l111l1lll_opy_ =  bstack11l111111_opy_()[bstack11lll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠨझ")]
  return bstack1l111l1lll_opy_ if bstack1l111l1lll_opy_ else -1
def bstack111l1l11l1_opy_(bstack1l111l1lll_opy_):
  global CONFIG
  if not bstack11lll1_opy_ (u"ࠪࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬञ") in CONFIG[bstack11lll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ट")]:
    return
  CONFIG[bstack11lll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧठ")] = CONFIG[bstack11lll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨड")].replace(
    bstack11lll1_opy_ (u"ࠧࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩढ"),
    str(bstack1l111l1lll_opy_)
  )
def bstack1l11111ll_opy_():
  global CONFIG
  if not bstack11lll1_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧण") in CONFIG[bstack11lll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫत")]:
    return
  current_time = datetime.datetime.now()
  bstack11lll1l111_opy_ = current_time.strftime(bstack11lll1_opy_ (u"ࠪࠩࡩ࠳ࠥࡣ࠯ࠨࡌ࠿ࠫࡍࠨथ"))
  CONFIG[bstack11lll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭द")] = CONFIG[bstack11lll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧध")].replace(
    bstack11lll1_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬन"),
    bstack11lll1l111_opy_
  )
def bstack1ll1l1lll1_opy_():
  global CONFIG
  if bstack11lll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऩ") in CONFIG and not bool(CONFIG[bstack11lll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪप")]):
    del CONFIG[bstack11lll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫफ")]
    return
  if not bstack11lll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬब") in CONFIG:
    CONFIG[bstack11lll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭भ")] = bstack11lll1_opy_ (u"ࠬࠩࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨम")
  if bstack11lll1_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬय") in CONFIG[bstack11lll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩर")]:
    bstack1l11111ll_opy_()
    os.environ[bstack11lll1_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬऱ")] = CONFIG[bstack11lll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫल")]
  if not bstack11lll1_opy_ (u"ࠪࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬळ") in CONFIG[bstack11lll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ऴ")]:
    return
  bstack1l111l1lll_opy_ = bstack11lll1_opy_ (u"ࠬ࠭व")
  bstack11l1111l11_opy_ = bstack11l11llll1_opy_()
  if bstack11l1111l11_opy_ != -1:
    bstack1l111l1lll_opy_ = bstack11lll1_opy_ (u"࠭ࡃࡊࠢࠪश") + str(bstack11l1111l11_opy_)
  if bstack1l111l1lll_opy_ == bstack11lll1_opy_ (u"ࠧࠨष"):
    bstack1l1111111l_opy_ = bstack11ll11llll_opy_(CONFIG[bstack11lll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫस")])
    if bstack1l1111111l_opy_ != -1:
      bstack1l111l1lll_opy_ = str(bstack1l1111111l_opy_)
  if bstack1l111l1lll_opy_:
    bstack111l1l11l1_opy_(bstack1l111l1lll_opy_)
    os.environ[bstack11lll1_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ह")] = CONFIG[bstack11lll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬऺ")]
def bstack1llll1l1ll_opy_(bstack11ll1ll1l_opy_, bstack11lll1l1ll_opy_, path):
  json_data = {
    bstack11lll1_opy_ (u"ࠫ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨऻ"): bstack11lll1l1ll_opy_
  }
  if os.path.exists(path):
    bstack11l1l111_opy_ = json.load(open(path, bstack11lll1_opy_ (u"ࠬࡸࡢࠨ़")))
  else:
    bstack11l1l111_opy_ = {}
  bstack11l1l111_opy_[bstack11ll1ll1l_opy_] = json_data
  with open(path, bstack11lll1_opy_ (u"ࠨࡷࠬࠤऽ")) as outfile:
    json.dump(bstack11l1l111_opy_, outfile)
def bstack11ll11llll_opy_(bstack11ll1ll1l_opy_):
  bstack11ll1ll1l_opy_ = str(bstack11ll1ll1l_opy_)
  bstack1111llll1_opy_ = os.path.join(os.path.expanduser(bstack11lll1_opy_ (u"ࠧࡿࠩा")), bstack11lll1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨि"))
  try:
    if not os.path.exists(bstack1111llll1_opy_):
      os.makedirs(bstack1111llll1_opy_)
    file_path = os.path.join(os.path.expanduser(bstack11lll1_opy_ (u"ࠩࢁࠫी")), bstack11lll1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪु"), bstack11lll1_opy_ (u"ࠫ࠳ࡨࡵࡪ࡮ࡧ࠱ࡳࡧ࡭ࡦ࠯ࡦࡥࡨ࡮ࡥ࠯࡬ࡶࡳࡳ࠭ू"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack11lll1_opy_ (u"ࠬࡽࠧृ")):
        pass
      with open(file_path, bstack11lll1_opy_ (u"ࠨࡷࠬࠤॄ")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack11lll1_opy_ (u"ࠧࡳࠩॅ")) as bstack11l111ll11_opy_:
      bstack1l11ll1lll_opy_ = json.load(bstack11l111ll11_opy_)
    if bstack11ll1ll1l_opy_ in bstack1l11ll1lll_opy_:
      bstack1111l1lll1_opy_ = bstack1l11ll1lll_opy_[bstack11ll1ll1l_opy_][bstack11lll1_opy_ (u"ࠨ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬॆ")]
      bstack111l1lll_opy_ = int(bstack1111l1lll1_opy_) + 1
      bstack1llll1l1ll_opy_(bstack11ll1ll1l_opy_, bstack111l1lll_opy_, file_path)
      return bstack111l1lll_opy_
    else:
      bstack1llll1l1ll_opy_(bstack11ll1ll1l_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warning(bstack1l1llll111_opy_.format(str(e)))
    return -1
def bstack11l11l111_opy_(config):
  if not config[bstack11lll1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫे")] or not config[bstack11lll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ै")]:
    return True
  else:
    return False
def bstack1111111ll1_opy_(config, index=0):
  global bstack1ll11l11_opy_
  bstack1l1ll1ll1_opy_ = {}
  caps = bstack1l111lll_opy_ + bstack1l11llll11_opy_
  if config.get(bstack11lll1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨॉ"), False):
    bstack1l1ll1ll1_opy_[bstack11lll1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩॊ")] = True
    bstack1l1ll1ll1_opy_[bstack11lll1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪो")] = config.get(bstack11lll1_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࡓࡵࡺࡩࡰࡰࡶࠫौ"), {})
  if bstack1ll11l11_opy_:
    caps += bstack11lll1111_opy_
  for key in config:
    if key in caps + [bstack11lll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶ्ࠫ")]:
      continue
    bstack1l1ll1ll1_opy_[key] = config[key]
  if bstack11lll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॎ") in config:
    for bstack11l11l11l_opy_ in config[bstack11lll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॏ")][index]:
      if bstack11l11l11l_opy_ in caps:
        continue
      bstack1l1ll1ll1_opy_[bstack11l11l11l_opy_] = config[bstack11lll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॐ")][index][bstack11l11l11l_opy_]
  bstack1l1ll1ll1_opy_[bstack11lll1_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧ॑")] = socket.gethostname()
  if bstack11lll1_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴ॒ࠧ") in bstack1l1ll1ll1_opy_:
    del (bstack1l1ll1ll1_opy_[bstack11lll1_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨ॓")])
  return bstack1l1ll1ll1_opy_
def bstack111111lll1_opy_(config):
  global bstack1ll11l11_opy_
  bstack1ll111l11_opy_ = {}
  caps = bstack1l11llll11_opy_
  if bstack1ll11l11_opy_:
    caps += bstack11lll1111_opy_
  for key in caps:
    if key in config:
      bstack1ll111l11_opy_[key] = config[key]
  return bstack1ll111l11_opy_
def bstack111111111_opy_(bstack1l1ll1ll1_opy_, bstack1ll111l11_opy_):
  bstack111l1l11l_opy_ = {}
  for key in bstack1l1ll1ll1_opy_.keys():
    if key in bstack111l1111ll_opy_:
      bstack111l1l11l_opy_[bstack111l1111ll_opy_[key]] = bstack1l1ll1ll1_opy_[key]
    else:
      bstack111l1l11l_opy_[key] = bstack1l1ll1ll1_opy_[key]
  for key in bstack1ll111l11_opy_:
    if key in bstack111l1111ll_opy_:
      bstack111l1l11l_opy_[bstack111l1111ll_opy_[key]] = bstack1ll111l11_opy_[key]
    else:
      bstack111l1l11l_opy_[key] = bstack1ll111l11_opy_[key]
  return bstack111l1l11l_opy_
def get_caps(config, index=0):
  global bstack1ll11l11_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack11l1ll1ll1_opy_ = bstack11l111l11l_opy_(bstack111111lll_opy_, config, logger)
  bstack1ll111l11_opy_ = bstack111111lll1_opy_(config)
  bstack1l111lll11_opy_ = bstack1l11llll11_opy_
  bstack1l111lll11_opy_ += bstack111lll1l1l_opy_
  bstack1ll111l11_opy_ = update(bstack1ll111l11_opy_, bstack11l1ll1ll1_opy_)
  if bstack1ll11l11_opy_:
    bstack1l111lll11_opy_ += bstack11lll1111_opy_
  if bstack11lll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ॔") in config:
    if bstack11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧॕ") in config[bstack11lll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॖ")][index]:
      caps[bstack11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩॗ")] = config[bstack11lll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨक़")][index][bstack11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫख़")]
    if bstack11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨग़") in config[bstack11lll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫज़")][index]:
      caps[bstack11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪड़")] = str(config[bstack11lll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ढ़")][index][bstack11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬफ़")])
    bstack1l11lll1_opy_ = bstack11l111l11l_opy_(bstack111111lll_opy_, config[bstack11lll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨय़")][index], logger)
    bstack1l111lll11_opy_ += list(bstack1l11lll1_opy_.keys())
    for bstack11111l1ll_opy_ in bstack1l111lll11_opy_:
      if bstack11111l1ll_opy_ in config[bstack11lll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩॠ")][index]:
        if bstack11111l1ll_opy_ == bstack11lll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩॡ"):
          try:
            bstack1l11lll1_opy_[bstack11111l1ll_opy_] = str(config[bstack11lll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫॢ")][index][bstack11111l1ll_opy_] * 1.0)
          except:
            bstack1l11lll1_opy_[bstack11111l1ll_opy_] = str(config[bstack11lll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॣ")][index][bstack11111l1ll_opy_])
        else:
          bstack1l11lll1_opy_[bstack11111l1ll_opy_] = config[bstack11lll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭।")][index][bstack11111l1ll_opy_]
        del (config[bstack11lll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ॥")][index][bstack11111l1ll_opy_])
    bstack1ll111l11_opy_ = update(bstack1ll111l11_opy_, bstack1l11lll1_opy_)
  bstack1l1ll1ll1_opy_ = bstack1111111ll1_opy_(config, index)
  for bstack1ll111l1l1_opy_ in bstack1l11llll11_opy_ + list(bstack11l1ll1ll1_opy_.keys()):
    if bstack1ll111l1l1_opy_ in bstack1l1ll1ll1_opy_:
      bstack1ll111l11_opy_[bstack1ll111l1l1_opy_] = bstack1l1ll1ll1_opy_[bstack1ll111l1l1_opy_]
      del (bstack1l1ll1ll1_opy_[bstack1ll111l1l1_opy_])
  if bstack1l1l11l1_opy_(config):
    bstack1l1ll1ll1_opy_[bstack11lll1_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ०")] = True
    caps.update(bstack1ll111l11_opy_)
    caps[bstack11lll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ१")] = bstack1l1ll1ll1_opy_
  else:
    bstack1l1ll1ll1_opy_[bstack11lll1_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧ२")] = False
    caps.update(bstack111111111_opy_(bstack1l1ll1ll1_opy_, bstack1ll111l11_opy_))
    if bstack11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭३") in caps:
      caps[bstack11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪ४")] = caps[bstack11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ५")]
      del (caps[bstack11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ६")])
    if bstack11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭७") in caps:
      caps[bstack11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ८")] = caps[bstack11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ९")]
      del (caps[bstack11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ॰")])
  return caps
def bstack1111ll1ll_opy_():
  global bstack1llllllll_opy_
  global CONFIG
  if bstack1llllllll_opy_ != bstack11lll1_opy_ (u"ࠩࠪॱ") and (bstack1llllllll_opy_.startswith(bstack11lll1_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫॲ")) or bstack1llllllll_opy_.startswith(bstack11lll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࠭ॳ"))):
    return bstack1llllllll_opy_
  if bstack1ll11lll11_opy_() <= version.parse(bstack11lll1_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬॴ")):
    if bstack1llllllll_opy_ != bstack11lll1_opy_ (u"࠭ࠧॵ"):
      return bstack11lll1_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣॶ") + bstack1llllllll_opy_ + bstack11lll1_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧॷ")
    return bstack11l11lll_opy_
  if bstack1llllllll_opy_ != bstack11lll1_opy_ (u"ࠩࠪॸ"):
    return bstack11lll1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧॹ") + bstack1llllllll_opy_ + bstack11lll1_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧॺ")
  return HTTPS_HUB
def bstack111llll11_opy_(options):
  return hasattr(options, bstack11lll1_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭ॻ"))
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
def bstack11l11l1l11_opy_(options, bstack1ll111l1_opy_):
  for bstack1ll111ll1_opy_ in bstack1ll111l1_opy_:
    if bstack1ll111ll1_opy_ in [bstack11lll1_opy_ (u"࠭ࡡࡳࡩࡶࠫॼ"), bstack11lll1_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫॽ")]:
      continue
    if bstack1ll111ll1_opy_ in options._experimental_options:
      options._experimental_options[bstack1ll111ll1_opy_] = update(options._experimental_options[bstack1ll111ll1_opy_],
                                                         bstack1ll111l1_opy_[bstack1ll111ll1_opy_])
    else:
      options.add_experimental_option(bstack1ll111ll1_opy_, bstack1ll111l1_opy_[bstack1ll111ll1_opy_])
  if bstack11lll1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ॾ") in bstack1ll111l1_opy_:
    for arg in bstack1ll111l1_opy_[bstack11lll1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॿ")]:
      options.add_argument(arg)
    del (bstack1ll111l1_opy_[bstack11lll1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨঀ")])
  if bstack11lll1_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨঁ") in bstack1ll111l1_opy_:
    for ext in bstack1ll111l1_opy_[bstack11lll1_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩং")]:
      try:
        options.add_extension(ext)
      except OSError:
        options.add_encoded_extension(ext)
    del (bstack1ll111l1_opy_[bstack11lll1_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪঃ")])
def bstack111l1ll1ll_opy_(options):
  global CONFIG
  global bstack1111lll1ll_opy_
  try:
    if not bstack1111lll1ll_opy_ or not options:
      return options
    from bstack_utils.bstack1l111l111l_opy_ import bstack1l1l1l1ll1_opy_
    bstack11l1ll11l1_opy_ = bstack1l1l1l1ll1_opy_(options, bstack1l1ll1l11l_opy_=bstack11lll1_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢ঄"))
    if bstack11l1ll11l1_opy_ > 0:
      logger.debug(bstack11lll1_opy_ (u"ࠣࡎࡲࡥࡩࠦࡴࡦࡵࡷ࡭ࡳ࡭࠺ࠡࡃࡧࡨࡪࡪࠠࡼࡿࠣࡨࡪ࡬ࡡࡶ࡮ࡷࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠠࡧࡱࡵࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠦঅ").format(bstack11l1ll11l1_opy_))
  except Exception as e:
    logger.debug(bstack11lll1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡯࡮࡫ࡧࡦࡸࠥࡲ࡯ࡢࡦࠣࡸࡪࡹࡴࡪࡰࡪࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡴࡶࡴࡪࡱࡱࡷ࠿ࠦࡻࡾࠤআ").format(e))
  return options
def bstack1l11l11l1_opy_(options, bstack11l11l1ll_opy_):
  if bstack11lll1_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩই") in bstack11l11l1ll_opy_:
    for bstack11ll11lll_opy_ in bstack11l11l1ll_opy_[bstack11lll1_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪঈ")]:
      if bstack11ll11lll_opy_ in options._preferences:
        options._preferences[bstack11ll11lll_opy_] = update(options._preferences[bstack11ll11lll_opy_], bstack11l11l1ll_opy_[bstack11lll1_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫউ")][bstack11ll11lll_opy_])
      else:
        options.set_preference(bstack11ll11lll_opy_, bstack11l11l1ll_opy_[bstack11lll1_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬঊ")][bstack11ll11lll_opy_])
  if bstack11lll1_opy_ (u"ࠧࡢࡴࡪࡷࠬঋ") in bstack11l11l1ll_opy_:
    for arg in bstack11l11l1ll_opy_[bstack11lll1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ঌ")]:
      options.add_argument(arg)
def bstack111111ll11_opy_(options, bstack1l11l1ll1l_opy_):
  if bstack11lll1_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࠪ঍") in bstack1l11l1ll1l_opy_:
    options.use_webview(bool(bstack1l11l1ll1l_opy_[bstack11lll1_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࠫ঎")]))
  bstack11l11l1l11_opy_(options, bstack1l11l1ll1l_opy_)
def bstack1ll1111l11_opy_(options, bstack11ll11l1_opy_):
  for bstack111111ll1l_opy_ in bstack11ll11l1_opy_:
    if bstack111111ll1l_opy_ in [bstack11lll1_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨএ"), bstack11lll1_opy_ (u"ࠬࡧࡲࡨࡵࠪঐ")]:
      continue
    options.set_capability(bstack111111ll1l_opy_, bstack11ll11l1_opy_[bstack111111ll1l_opy_])
  if bstack11lll1_opy_ (u"࠭ࡡࡳࡩࡶࠫ঑") in bstack11ll11l1_opy_:
    for arg in bstack11ll11l1_opy_[bstack11lll1_opy_ (u"ࠧࡢࡴࡪࡷࠬ঒")]:
      options.add_argument(arg)
  if bstack11lll1_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬও") in bstack11ll11l1_opy_:
    options.bstack1l111l11ll_opy_(bool(bstack11ll11l1_opy_[bstack11lll1_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭ঔ")]))
def bstack11llllll11_opy_(options, bstack1lll1ll1ll_opy_):
  for bstack1lll11lll1_opy_ in bstack1lll1ll1ll_opy_:
    if bstack1lll11lll1_opy_ in [bstack11lll1_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧক"), bstack11lll1_opy_ (u"ࠫࡦࡸࡧࡴࠩখ")]:
      continue
    options._options[bstack1lll11lll1_opy_] = bstack1lll1ll1ll_opy_[bstack1lll11lll1_opy_]
  if bstack11lll1_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩগ") in bstack1lll1ll1ll_opy_:
    for bstack1111lll1l_opy_ in bstack1lll1ll1ll_opy_[bstack11lll1_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪঘ")]:
      options.bstack11111l111_opy_(
        bstack1111lll1l_opy_, bstack1lll1ll1ll_opy_[bstack11lll1_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫঙ")][bstack1111lll1l_opy_])
  if bstack11lll1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭চ") in bstack1lll1ll1ll_opy_:
    for arg in bstack1lll1ll1ll_opy_[bstack11lll1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧছ")]:
      options.add_argument(arg)
def bstack111l1111l1_opy_(options, caps):
  if not hasattr(options, bstack11lll1_opy_ (u"ࠪࡏࡊ࡟ࠧজ")):
    return
  if options.KEY == bstack11lll1_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩঝ"):
    options = a11y.bstack1l1111111_opy_(bstack1l1lll111l_opy_=options, config=CONFIG)
  if options.KEY == bstack11lll1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪঞ") and options.KEY in caps:
    bstack11l11l1l11_opy_(options, caps[bstack11lll1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫট")])
  elif options.KEY == bstack11lll1_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬঠ") and options.KEY in caps:
    bstack1l11l11l1_opy_(options, caps[bstack11lll1_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ড")])
  elif options.KEY == bstack11lll1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪঢ") and options.KEY in caps:
    bstack1ll1111l11_opy_(options, caps[bstack11lll1_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫণ")])
  elif options.KEY == bstack11lll1_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬত") and options.KEY in caps:
    bstack111111ll11_opy_(options, caps[bstack11lll1_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭থ")])
  elif options.KEY == bstack11lll1_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬদ") and options.KEY in caps:
    bstack11llllll11_opy_(options, caps[bstack11lll1_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ধ")])
def bstack1111llll11_opy_(caps):
  global bstack1ll11l11_opy_
  if isinstance(os.environ.get(bstack11lll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩন")), str):
    bstack1ll11l11_opy_ = eval(os.getenv(bstack11lll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ঩")))
  if bstack1ll11l11_opy_:
    if bstack11l1l111l1_opy_() < version.parse(bstack11lll1_opy_ (u"ࠪ࠶࠳࠹࠮࠱ࠩপ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack11lll1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫফ")
    if bstack11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪব") in caps:
      browser = caps[bstack11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫভ")]
    elif bstack11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨম") in caps:
      browser = caps[bstack11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩয")]
    browser = str(browser).lower()
    if browser == bstack11lll1_opy_ (u"ࠩ࡬ࡴ࡭ࡵ࡮ࡦࠩর") or browser == bstack11lll1_opy_ (u"ࠪ࡭ࡵࡧࡤࠨ঱"):
      browser = bstack11lll1_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫল")
    if browser == bstack11lll1_opy_ (u"ࠬࡹࡡ࡮ࡵࡸࡲ࡬࠭঳"):
      browser = bstack11lll1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭঴")
    if browser not in [bstack11lll1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ঵"), bstack11lll1_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭শ"), bstack11lll1_opy_ (u"ࠩ࡬ࡩࠬষ"), bstack11lll1_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪস"), bstack11lll1_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬহ")]:
      return None
    try:
      package = bstack11lll1_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡿࢂ࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧ঺").format(browser)
      name = bstack11lll1_opy_ (u"࠭ࡏࡱࡶ࡬ࡳࡳࡹࠧ঻")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack111llll11_opy_(options):
        return None
      for bstack1ll111l1l1_opy_ in caps.keys():
        options.set_capability(bstack1ll111l1l1_opy_, caps[bstack1ll111l1l1_opy_])
      bstack111l1111l1_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack11l11111ll_opy_(options, bstack1l1lll1ll1_opy_):
  if not bstack111llll11_opy_(options):
    return
  for bstack1ll111l1l1_opy_ in bstack1l1lll1ll1_opy_.keys():
    if bstack1ll111l1l1_opy_ in bstack111lll1l1l_opy_:
      continue
    if bstack1ll111l1l1_opy_ in options._caps and type(options._caps[bstack1ll111l1l1_opy_]) in [dict, list]:
      options._caps[bstack1ll111l1l1_opy_] = update(options._caps[bstack1ll111l1l1_opy_], bstack1l1lll1ll1_opy_[bstack1ll111l1l1_opy_])
    else:
      options.set_capability(bstack1ll111l1l1_opy_, bstack1l1lll1ll1_opy_[bstack1ll111l1l1_opy_])
  bstack111l1111l1_opy_(options, bstack1l1lll1ll1_opy_)
  if bstack11lll1_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ়࠭") in options._caps:
    if options._caps[bstack11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ঽ")] and options._caps[bstack11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧা")].lower() != bstack11lll1_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫি"):
      del options._caps[bstack11lll1_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪী")]
def bstack1ll11l11l_opy_(proxy_config):
  if bstack11lll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩু") in proxy_config:
    proxy_config[bstack11lll1_opy_ (u"࠭ࡳࡴ࡮ࡓࡶࡴࡾࡹࠨূ")] = proxy_config[bstack11lll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫৃ")]
    del (proxy_config[bstack11lll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬৄ")])
  if bstack11lll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬ৅") in proxy_config and proxy_config[bstack11lll1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭৆")].lower() != bstack11lll1_opy_ (u"ࠫࡩ࡯ࡲࡦࡥࡷࠫে"):
    proxy_config[bstack11lll1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨৈ")] = bstack11lll1_opy_ (u"࠭࡭ࡢࡰࡸࡥࡱ࠭৉")
  if bstack11lll1_opy_ (u"ࠧࡱࡴࡲࡼࡾࡇࡵࡵࡱࡦࡳࡳ࡬ࡩࡨࡗࡵࡰࠬ৊") in proxy_config:
    proxy_config[bstack11lll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫো")] = bstack11lll1_opy_ (u"ࠩࡳࡥࡨ࠭ৌ")
  return proxy_config
def bstack1ll1l1lll_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack11lll1_opy_ (u"ࠪࡴࡷࡵࡸࡺ্ࠩ") in config:
    return proxy
  config[bstack11lll1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪৎ")] = bstack1ll11l11l_opy_(config[bstack11lll1_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ৏")])
  if proxy == None:
    proxy = Proxy(config[bstack11lll1_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ৐")])
  return proxy
def bstack1l1lll11ll_opy_(self):
  global CONFIG
  global bstack1ll111l111_opy_
  try:
    proxy = bstack11111ll1_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack11lll1_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ৑")):
        proxies = bstack1l11ll1ll_opy_(proxy, bstack1111ll1ll_opy_())
        if len(proxies) > 0:
          protocol, bstack11ll11ll11_opy_ = proxies.popitem()
          if bstack11lll1_opy_ (u"ࠣ࠼࠲࠳ࠧ৒") in bstack11ll11ll11_opy_:
            return bstack11ll11ll11_opy_
          else:
            return bstack11lll1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ৓") + bstack11ll11ll11_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack11lll1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡰࡳࡱࡻࡽࠥࡻࡲ࡭ࠢ࠽ࠤࢀࢃࠢ৔").format(str(e)))
  return bstack1ll111l111_opy_(self)
def bstack11llll1ll_opy_():
  global CONFIG
  return bstack1l111l1111_opy_(CONFIG) and bstack1llllllll1_opy_() and bstack1ll11lll11_opy_() >= version.parse(bstack1ll1l1l1ll_opy_)
def bstack1llllll1l1_opy_():
  global CONFIG
  return (bstack11lll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ৕") in CONFIG or bstack11lll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ৖") in CONFIG) and bstack111111l11_opy_()
def bstack11l111l11_opy_(config):
  bstack11111llll1_opy_ = {}
  if bstack11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪৗ") in config:
    bstack11111llll1_opy_ = config[bstack11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ৘")]
  if bstack11lll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ৙") in config:
    bstack11111llll1_opy_ = config[bstack11lll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ৚")]
  proxy = bstack11111ll1_opy_(config)
  if proxy:
    if proxy.endswith(bstack11lll1_opy_ (u"ࠪ࠲ࡵࡧࡣࠨ৛")) and os.path.isfile(proxy):
      bstack11111llll1_opy_[bstack11lll1_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧড়")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack11lll1_opy_ (u"ࠬ࠴ࡰࡢࡥࠪঢ়")):
        proxies = bstack11l11l11l1_opy_(config, bstack1111ll1ll_opy_())
        if len(proxies) > 0:
          protocol, bstack11ll11ll11_opy_ = proxies.popitem()
          if bstack11lll1_opy_ (u"ࠨ࠺࠰࠱ࠥ৞") in bstack11ll11ll11_opy_:
            parsed_url = urlparse(bstack11ll11ll11_opy_)
          else:
            parsed_url = urlparse(protocol + bstack11lll1_opy_ (u"ࠢ࠻࠱࠲ࠦয়") + bstack11ll11ll11_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack11111llll1_opy_[bstack11lll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡈࡰࡵࡷࠫৠ")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack11111llll1_opy_[bstack11lll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬৡ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack11111llll1_opy_[bstack11lll1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭ৢ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack11111llll1_opy_[bstack11lll1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧৣ")] = str(parsed_url.password)
  return bstack11111llll1_opy_
def bstack1l1111l1l1_opy_(config):
  if bstack11lll1_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪ৤") in config:
    return config[bstack11lll1_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫ৥")]
  return {}
def update_caps_for_local(caps):
  global bstack111l11l1l1_opy_
  if bstack11lll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ০") in caps:
    caps[bstack11lll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ১")][bstack11lll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨ২")] = True
    if bstack111l11l1l1_opy_:
      caps[bstack11lll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ৩")][bstack11lll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭৪")] = bstack111l11l1l1_opy_
  else:
    caps[bstack11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪ৫")] = True
    if bstack111l11l1l1_opy_:
      caps[bstack11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ৬")] = bstack111l11l1l1_opy_
@measure(event_name=EVENTS.bstack1l1lll11l1_opy_, stage=STAGE.bstack1lllllll11_opy_, bstack1l11ll11l_opy_=SESSION_NAME)
def bstack11llll1111_opy_():
  global CONFIG
  if not bstack1ll111l11l_opy_(CONFIG) or cli.is_enabled(CONFIG):
    return
  if bstack11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ৭") in CONFIG and bstack1lll11l1_opy_(CONFIG[bstack11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ৮")]):
    if (
      bstack11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭৯") in CONFIG
      and bstack1lll11l1_opy_(CONFIG[bstack11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧৰ")].get(bstack11lll1_opy_ (u"ࠫࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠨৱ")))
    ):
      logger.debug(bstack11lll1_opy_ (u"ࠧࡒ࡯ࡤࡣ࡯ࠤࡧ࡯࡮ࡢࡴࡼࠤࡳࡵࡴࠡࡵࡷࡥࡷࡺࡥࡥࠢࡤࡷࠥࡹ࡫ࡪࡲࡅ࡭ࡳࡧࡲࡺࡋࡱ࡭ࡹ࡯ࡡ࡭࡫ࡶࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠨ৲"))
      return
    bstack11111llll1_opy_ = bstack11l111l11_opy_(CONFIG)
    bstack111ll1l1l1_opy_(CONFIG[bstack11lll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ৳")], bstack11111llll1_opy_)
def bstack111ll1l1l1_opy_(key, bstack11111llll1_opy_):
  global bstack11111111l_opy_
  logger.info(bstack11l1llll_opy_)
  try:
    bstack11111111l_opy_ = Local()
    bstack1l1l11111_opy_ = {bstack11lll1_opy_ (u"ࠧ࡬ࡧࡼࠫ৴"): key}
    bstack1l1l11111_opy_.update(bstack11111llll1_opy_)
    logger.debug(bstack1ll1lllll1_opy_.format(str(bstack1l1l11111_opy_)).replace(key, bstack11lll1_opy_ (u"ࠨ࡝ࡕࡉࡉࡇࡃࡕࡇࡇࡡࠬ৵")))
    bstack11111111l_opy_.start(**bstack1l1l11111_opy_)
    if bstack11111111l_opy_.isRunning():
      logger.info(bstack1llll11ll1_opy_)
  except Exception as e:
    bstack11l1111ll1_opy_(bstack1l11l1lll1_opy_.format(str(e)))
def bstack1l1llll11l_opy_():
  global bstack11111111l_opy_
  if bstack11111111l_opy_.isRunning():
    logger.info(bstack11lllll1ll_opy_)
    bstack11111111l_opy_.stop()
  bstack11111111l_opy_ = None
def bstack111ll111ll_opy_(bstack1lll1111ll_opy_=[]):
  global CONFIG
  bstack1llll1l111_opy_ = []
  bstack1llll11l1_opy_ = [bstack11lll1_opy_ (u"ࠩࡲࡷࠬ৶"), bstack11lll1_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭৷"), bstack11lll1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨ৸"), bstack11lll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ৹"), bstack11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ৺"), bstack11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ৻")]
  try:
    for err in bstack1lll1111ll_opy_:
      bstack1ll1l1l11_opy_ = {}
      for k in bstack1llll11l1_opy_:
        val = CONFIG[bstack11lll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫৼ")][int(err[bstack11lll1_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ৽")])].get(k)
        if val:
          bstack1ll1l1l11_opy_[k] = val
      if(err[bstack11lll1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ৾")] != bstack11lll1_opy_ (u"ࠫࠬ৿")):
        bstack1ll1l1l11_opy_[bstack11lll1_opy_ (u"ࠬࡺࡥࡴࡶࡶࠫ਀")] = {
          err[bstack11lll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫਁ")]: err[bstack11lll1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ਂ")]
        }
        bstack1llll1l111_opy_.append(bstack1ll1l1l11_opy_)
  except Exception as e:
    logger.debug(bstack11lll1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪࡴࡸ࡭ࡢࡶࡷ࡭ࡳ࡭ࠠࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴ࠻ࠢࠪਃ") + str(e))
  finally:
    return bstack1llll1l111_opy_
def bstack1l11l1111_opy_(file_name):
  bstack1l1llll11_opy_ = []
  try:
    bstack111111l11l_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack111111l11l_opy_):
      with open(bstack111111l11l_opy_) as f:
        bstack1l1ll11ll_opy_ = json.load(f)
        bstack1l1llll11_opy_ = bstack1l1ll11ll_opy_
      os.remove(bstack111111l11l_opy_)
    return bstack1l1llll11_opy_
  except Exception as e:
    logger.debug(bstack11lll1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡫࡯࡮ࡥ࡫ࡱ࡫ࠥ࡫ࡲࡳࡱࡵࠤࡱ࡯ࡳࡵ࠼ࠣࠫ਄") + str(e))
    return bstack1l1llll11_opy_
def bstack11l1ll1l11_opy_():
  try:
      import time
      from bstack_utils.constants import bstack1llll111ll_opy_, EVENTS
      from bstack_utils.helper import bstack11l1lll11_opy_, get_host_info, global_config
      from datetime import datetime
      from filelock import FileLock
      from bstack_utils.bstack1lll11lll_opy_ import bstack1llll11l_opy_
      bstack1llll11l_opy_.bstack1lll111l1l_opy_()
      bstack111ll11111_opy_ = os.path.join(os.getcwd(), bstack11lll1_opy_ (u"ࠪࡰࡴ࡭ࠧਅ"), bstack11lll1_opy_ (u"ࠫࡰ࡫ࡹ࠮࡯ࡨࡸࡷ࡯ࡣࡴ࠰࡭ࡷࡴࡴࠧਆ"))
      data = None
      lock = FileLock(bstack111ll11111_opy_+bstack11lll1_opy_ (u"ࠧ࠴࡬ࡰࡥ࡮ࠦਇ"), timeout=2)
      try:
          with lock:
              with open(bstack111ll11111_opy_, bstack11lll1_opy_ (u"ࠨࡲࠣਈ"), encoding=bstack11lll1_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨਉ")) as file:
                  data = json.load(file)
      except Exception as e:
          logger.debug(bstack11lll1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡷ࡫ࡡࡥࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹࠠࡧ࡫࡯ࡩ࠿ࠦࡻࡾࠤਊ").format(e))
          return
      if not data:
          return
      def bstack1l1llll1l_opy_():
          try:
              config = {
                  bstack11lll1_opy_ (u"ࠤ࡫ࡩࡦࡪࡥࡳࡵࠥ਋"): {
                      bstack11lll1_opy_ (u"ࠥࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠤ਌"): bstack11lll1_opy_ (u"ࠦࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠢ਍"),
                  }
              }
              bstack1ll111ll11_opy_ = datetime.utcnow()
              current_time = bstack1ll111ll11_opy_.strftime(bstack11lll1_opy_ (u"࡙ࠧࠫ࠮ࠧࡰ࠱ࠪࡪࡔࠦࡊ࠽ࠩࡒࡀࠥࡔ࠰ࠨࡪ࡛ࠥࡔࡄࠤ਎"))
              test_id = os.environ.get(bstack11lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫਏ")) if os.environ.get(bstack11lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬਐ")) else global_config.get_property(bstack11lll1_opy_ (u"ࠣࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠥ਑"))
              payload = {
                  bstack11lll1_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪࠨ਒"): bstack11lll1_opy_ (u"ࠥࡷࡩࡱ࡟ࡦࡸࡨࡲࡹࡹࠢਓ"),
                  bstack11lll1_opy_ (u"ࠦࡩࡧࡴࡢࠤਔ"): {
                      bstack11lll1_opy_ (u"ࠧࡺࡥࡴࡶ࡫ࡹࡧࡥࡵࡶ࡫ࡧࠦਕ"): test_id,
                      bstack11lll1_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡪ࡟ࡥࡣࡼࠦਖ"): current_time,
                      bstack11lll1_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥ࡮ࡢ࡯ࡨࠦਗ"): bstack11lll1_opy_ (u"ࠣࡕࡇࡏࡋ࡫ࡡࡵࡷࡵࡩࡕ࡫ࡲࡧࡱࡵࡱࡦࡴࡣࡦࠤਘ"),
                      bstack11lll1_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠ࡬ࡶࡳࡳࠨਙ"): {
                          bstack11lll1_opy_ (u"ࠥࡱࡪࡧࡳࡶࡴࡨࡷࠧਚ"): data,
                          bstack11lll1_opy_ (u"ࠦࡸࡪ࡫ࡓࡷࡱࡍࡩࠨਛ"): global_config.get_property(bstack11lll1_opy_ (u"ࠧࡹࡤ࡬ࡔࡸࡲࡎࡪࠢਜ"))
                      },
                      bstack11lll1_opy_ (u"ࠨࡵࡴࡧࡵࡣࡩࡧࡴࡢࠤਝ"): global_config.get_property(bstack11lll1_opy_ (u"ࠢࡶࡵࡨࡶࡓࡧ࡭ࡦࠤਞ")),
                      bstack11lll1_opy_ (u"ࠣࡪࡲࡷࡹࡥࡩ࡯ࡨࡲࠦਟ"): get_host_info()
                  }
              }
              bstack1lllll1lll_opy_ = bstack11111l11ll_opy_(cli.config, [bstack11lll1_opy_ (u"ࠤࡤࡴ࡮ࡹࠢਠ"), bstack11lll1_opy_ (u"ࠥࡩࡩࡹࡉ࡯ࡵࡷࡶࡺࡳࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠣਡ"), bstack11lll1_opy_ (u"ࠦࡦࡶࡩࠣਢ")], bstack1llll111ll_opy_)
              response = bstack11l1lll11_opy_(bstack11lll1_opy_ (u"ࠧࡖࡏࡔࡖࠥਣ"), bstack1lllll1lll_opy_, payload, config)
              if response.status_code >= 200 and response.status_code < 300:
                  logger.info(bstack11lll1_opy_ (u"ࠨࡋࡦࡻࠣࡱࡪࡺࡲࡪࡥࡶࠤࡸ࡫࡮ࡵࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡶࡲࠤࢀࢃࠢਤ").format(bstack1llll111ll_opy_))
              else:
                  logger.debug(bstack11lll1_opy_ (u"ࠢࡌࡧࡼࠤࡲ࡫ࡴࡳ࡫ࡦࡷࠥࡸࡥࡲࡷࡨࡷࡹࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫ࠤࡸࡺࡡࡵࡷࡶࠤࢀࢃࠢਥ").format(response.status_code))
          except Exception as e:
              logger.debug(bstack11lll1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫࡮ࡥࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹ࠺ࠡࡽࢀࠦਦ").format(e))
      bstack1l1llll1l_opy_()
  except Exception as e:
      logger.debug(bstack11lll1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫࡮ࡥࡡ࡮ࡩࡾࡥ࡭ࡦࡶࡵ࡭ࡨࡹ࠺ࠡࡽࢀࠦਧ").format(e))
def bstack1111l111l1_opy_(bstack1l111l11_opy_=False):
  bstack1111ll1l1_opy_ = bstack11lll1_opy_ (u"ࠥࠦਨ")
  global bstack11111l1lll_opy_
  global bstack1ll111ll1l_opy_
  global bstack111l1llll_opy_
  global bstack11l1l1111_opy_
  global ROBOT_PYTHON_ERRORS
  global bstack1l11lllll1_opy_
  global CONFIG
  bstack11llll1l11_opy_ = os.environ.get(bstack11lll1_opy_ (u"ࠫࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ࡟ࡖࡕࡈࡈࠬ਩"))
  if bstack11llll1l11_opy_ not in [bstack11lll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ਪ")]:
    bstack1111ll1l1_opy_ = bstack1llll11l_opy_.bstack11ll11l1l_opy_(EVENTS.bstack1l1ll1l1ll_opy_)
  percy.shutdown()
  if bstack11111l1lll_opy_:
    logger.warning(bstack1l1ll1ll_opy_.format(str(bstack11111l1lll_opy_)))
  else:
    try:
      bstack11l1l111_opy_ = bstack1l1l1llll1_opy_(bstack11lll1_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬਫ"), logger)
      if bstack11l1l111_opy_.get(bstack11lll1_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬਬ")) and bstack11l1l111_opy_.get(bstack11lll1_opy_ (u"ࠨࡰࡸࡨ࡬࡫࡟࡭ࡱࡦࡥࡱ࠭ਭ")).get(bstack11lll1_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫਮ")):
        logger.warning(bstack1l1ll1ll_opy_.format(str(bstack11l1l111_opy_[bstack11lll1_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨਯ")][bstack11lll1_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ਰ")])))
    except Exception as e:
      logger.error(e)
  if cli.is_running() and bstack11llll1l11_opy_ not in [bstack11lll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭਱")]:
    if _1l1lll1lll_opy_ is not None:
      bstack1l111l11_opy_ = _1l1lll1lll_opy_
    else:
      bstack1l111l11_opy_ = cli.is_running()
    bstack11l1lll1_opy_.invoke(Events.bstack1lll111l_opy_)
  elif _1l1lll1lll_opy_ is not None:
    bstack1l111l11_opy_ = _1l1lll1lll_opy_
  logger.info(bstack111l11llll_opy_)
  global bstack11111111l_opy_
  if bstack11111111l_opy_:
    bstack1l1llll11l_opy_()
  try:
    with bstack1111lll11l_opy_:
      bstack11l1ll11l_opy_ = bstack1ll111ll1l_opy_.copy()
    for driver in bstack11l1ll11l_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1111l1ll1l_opy_)
  ROBOT_PYTHON_ERRORS = []
  if bstack1l11lllll1_opy_ == bstack11lll1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬਲ"):
    ROBOT_PYTHON_ERRORS = bstack1l11l1111_opy_(bstack11lll1_opy_ (u"ࠧࡳࡱࡥࡳࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨਲ਼"))
  if bstack1l11lllll1_opy_ == bstack11lll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ਴") and len(bstack11l1l1111_opy_) == 0:
    bstack11l1l1111_opy_ = bstack1l11l1111_opy_(bstack11lll1_opy_ (u"ࠩࡳࡻࡤࡶࡹࡵࡧࡶࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧਵ"))
    if len(bstack11l1l1111_opy_) == 0:
      bstack11l1l1111_opy_ = bstack1l11l1111_opy_(bstack11lll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡴࡵࡶ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩਸ਼"))
  bstack11ll1lllll_opy_ = bstack11lll1_opy_ (u"ࠫࠬ਷")
  if len(bstack111l1llll_opy_) > 0:
    bstack11ll1lllll_opy_ = bstack111ll111ll_opy_(bstack111l1llll_opy_)
  elif len(bstack11l1l1111_opy_) > 0:
    bstack11ll1lllll_opy_ = bstack111ll111ll_opy_(bstack11l1l1111_opy_)
  elif len(ROBOT_PYTHON_ERRORS) > 0:
    bstack11ll1lllll_opy_ = bstack111ll111ll_opy_(ROBOT_PYTHON_ERRORS)
  elif len(bstack1lll1111l1_opy_) > 0:
    bstack11ll1lllll_opy_ = bstack111ll111ll_opy_(bstack1lll1111l1_opy_)
  if bstack11llll1l11_opy_ not in [bstack11lll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ਸ")]:
    def bstack1l1l1l111_opy_():
      try:
        if bstack11llll1l11_opy_ in [bstack11lll1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬਹ"), bstack11lll1_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭਺")]:
          bstack1ll1l111_opy_()
      except Exception as e:
        logger.debug(bstack11lll1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪ࡮ࡴࡡ࡭ࡡࡨࡼࡪࡩࡵࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤ਻").format(e))
    def bstack111ll1lll_opy_():
      try:
        if bool(bstack11ll1lllll_opy_):
          bstack1111l11ll_opy_(bstack11ll1lllll_opy_, bstack1l111l11_opy_=bstack1l111l11_opy_)
        else:
          bstack1111l11ll_opy_(bstack1l111l11_opy_=bstack1l111l11_opy_)
      except Exception as e:
        logger.debug(bstack11lll1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡵࡨࡲࡩ࡯࡮ࡨࠢࡨࡺࡪࡴࡴ࠻ࠢࡾࢁ਼ࠧ").format(e))
    def bstack11l111lll_opy_():
      try:
        logger_utils.bstack1l1111l1ll_opy_(CONFIG)
      except Exception as e:
        logger.debug(bstack11lll1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡶࡩࡳࡪࡩ࡯ࡩࠣࡰࡴ࡭ࡳ࠻ࠢࡾࢁࠧ਽").format(e))
    bstack1l111l1l_opy_ = threading.Thread(target=bstack1l1l1l111_opy_)
    bstack11l1l11l11_opy_ = threading.Thread(target=bstack111ll1lll_opy_)
    bstack1l11l1l1l1_opy_ = threading.Thread(target=bstack11l111lll_opy_)
    threads = [bstack1l111l1l_opy_, bstack11l1l11l11_opy_, bstack1l11l1l1l1_opy_]
    for thread in threads:
      try:
        thread.start()
      except Exception as e:
        logger.debug(bstack11lll1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡷࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡺࡨࡳࡧࡤࡨࠥࢁࡽ࠻ࠢࡾࢁࠧਾ").format(thread.name, e))
    for thread in threads:
      try:
        thread.join()
      except Exception as e:
        logger.debug(bstack11lll1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡯ࡵࡩ࡯࡫ࡱ࡫ࠥࡺࡨࡳࡧࡤࡨࠥࢁࡽ࠻ࠢࡾࢁࠧਿ").format(thread.name, e))
    bstack1ll1lll11l_opy_(bstack11l1lllll1_opy_, logger)
    bstack1ll1lll11l_opy_(os.path.join(os.getcwd(), bstack11lll1_opy_ (u"࠭࡬ࡰࡩࠪੀ"), bstack11lll1_opy_ (u"ࠧ࡬ࡧࡼ࠱ࡲ࡫ࡴࡳ࡫ࡦࡷ࠳ࡰࡳࡰࡰࠪੁ")), logger)
  if bstack11llll1l11_opy_ not in [bstack11lll1_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩੂ")]:
    bstack1llll11l_opy_.end(EVENTS.bstack1l1ll1l1ll_opy_.value, bstack1111ll1l1_opy_ + bstack11lll1_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ੃"), bstack1111ll1l1_opy_ + bstack11lll1_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ੄"), status=True, failure=None, test_name=None)
    bstack11l1ll1l11_opy_()
    logger_utils.bstack111l1ll1l_opy_()
    logging.shutdown()
  if len(ROBOT_PYTHON_ERRORS) > 0:
    sys.exit(len(ROBOT_PYTHON_ERRORS))
def bstack11l111l111_opy_(bstack1l1111lll1_opy_, frame):
  global global_config
  logger.error(bstack1lllll11ll_opy_)
  global_config.bstack1111l11l1_opy_(bstack11lll1_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡓࡵࠧ੅"), bstack1l1111lll1_opy_)
  if hasattr(signal, bstack11lll1_opy_ (u"࡙ࠬࡩࡨࡰࡤࡰࡸ࠭੆")):
    global_config.bstack1111l11l1_opy_(bstack11lll1_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭ੇ"), signal.Signals(bstack1l1111lll1_opy_).name)
  else:
    global_config.bstack1111l11l1_opy_(bstack11lll1_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡔ࡫ࡪࡲࡦࡲࠧੈ"), bstack11lll1_opy_ (u"ࠨࡕࡌࡋ࡚ࡔࡋࡏࡑ࡚ࡒࠬ੉"))
  bstack1l111l11_opy_ = cli.is_running()
  if bstack1l111l11_opy_:
    bstack11l1lll1_opy_.invoke(Events.bstack1lll111l_opy_)
  bstack11llll1l11_opy_ = os.environ.get(bstack11lll1_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪ੊"))
  if bstack11llll1l11_opy_ == bstack11lll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪੋ") and not cli.is_enabled(CONFIG):
    TestHubHandler.stop(global_config.get_property(bstack11lll1_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡘ࡯ࡧ࡯ࡣ࡯ࠫੌ")))
  bstack1111l111l1_opy_(bstack1l111l11_opy_)
  sys.exit(1)
def bstack11l1111ll1_opy_(err):
  logger.critical(bstack111ll111l1_opy_.format(str(err)))
  bstack1111l11ll_opy_(bstack111ll111l1_opy_.format(str(err)), True)
  atexit.unregister(bstack1111l111l1_opy_)
  bstack1ll1l111_opy_()
  sys.exit(1)
def bstack11l1l11111_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1111l11ll_opy_(message, True)
  atexit.unregister(bstack1111l111l1_opy_)
  bstack1ll1l111_opy_()
  sys.exit(1)
def bstack11l1llllll_opy_():
  global CONFIG
  global bstack11111lll_opy_
  global bstack111111ll1_opy_
  global BROWSERSTACK_AUTOMATION
  CONFIG = bstack1l11lllll_opy_()
  load_dotenv(CONFIG.get(bstack11lll1_opy_ (u"ࠬ࡫࡮ࡷࡈ࡬ࡰࡪ੍࠭")))
  bstack11l11lllll_opy_()
  bstack111lll1111_opy_()
  CONFIG = bstack11l11l1l_opy_(CONFIG)
  update(CONFIG, bstack111111ll1_opy_)
  update(CONFIG, bstack11111lll_opy_)
  if not cli.is_enabled(CONFIG):
    CONFIG = bstack11l111llll_opy_(CONFIG)
  BROWSERSTACK_AUTOMATION = bstack1ll111l11l_opy_(CONFIG)
  os.environ[bstack11lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ੎")] = BROWSERSTACK_AUTOMATION.__str__().lower()
  global_config.bstack1111l11l1_opy_(bstack11lll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ੏"), BROWSERSTACK_AUTOMATION)
  if (bstack11lll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ੐") in CONFIG and bstack11lll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬੑ") in bstack11111lll_opy_) or (
          bstack11lll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭੒") in CONFIG and bstack11lll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ੓") not in bstack111111ll1_opy_):
    if os.getenv(bstack11lll1_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩ੔")):
      CONFIG[bstack11lll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ੕")] = os.getenv(bstack11lll1_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫ੖"))
    else:
      if not CONFIG.get(bstack11lll1_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠦ੗"), bstack11lll1_opy_ (u"ࠤࠥ੘")) in bstack1llll111_opy_:
        bstack1ll1l1lll1_opy_()
  elif (bstack11lll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ਖ਼") not in CONFIG and bstack11lll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ਗ਼") in CONFIG) or (
          bstack11lll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨਜ਼") in bstack111111ll1_opy_ and bstack11lll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩੜ") not in bstack11111lll_opy_):
    del (CONFIG[bstack11lll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ੝")])
  if bstack11l11l111_opy_(CONFIG):
    bstack11l1111ll1_opy_(bstack1ll1l1ll_opy_)
  Config.get_instance().bstack1111l11l1_opy_(bstack11lll1_opy_ (u"ࠣࡷࡶࡩࡷࡔࡡ࡮ࡧࠥਫ਼"), CONFIG[bstack11lll1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ੟")])
  bstack11ll1l1l_opy_()
  bstack1l1l1l11l1_opy_()
  if bstack1ll11l11_opy_ and not CONFIG.get(bstack11lll1_opy_ (u"ࠥࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠨ੠"), bstack11lll1_opy_ (u"ࠦࠧ੡")) in bstack1llll111_opy_:
    CONFIG[bstack11lll1_opy_ (u"ࠬࡧࡰࡱࠩ੢")] = bstack1l11llll1l_opy_(CONFIG)
    logger.info(bstack11l1ll1l_opy_.format(CONFIG[bstack11lll1_opy_ (u"࠭ࡡࡱࡲࠪ੣")]))
  if not BROWSERSTACK_AUTOMATION:
    CONFIG[bstack11lll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ੤")] = [{}]
def bstack1ll11111ll_opy_(config, bstack11ll1ll1ll_opy_):
  global CONFIG
  global bstack1ll11l11_opy_
  CONFIG = config
  bstack1ll11l11_opy_ = bstack11ll1ll1ll_opy_
def bstack1l1l1l11l1_opy_():
  global CONFIG
  global bstack1ll11l11_opy_
  if bstack11lll1_opy_ (u"ࠨࡣࡳࡴࠬ੥") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack11l1l11111_opy_(e, bstack111l11111l_opy_)
    bstack1ll11l11_opy_ = True
    global_config.bstack1111l11l1_opy_(bstack11lll1_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨ੦"), True)
def bstack1l11llll1l_opy_(config):
  bstack111lll11l1_opy_ = bstack11lll1_opy_ (u"ࠪࠫ੧")
  app = config[bstack11lll1_opy_ (u"ࠫࡦࡶࡰࠨ੨")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack11111ll1ll_opy_:
      if os.path.exists(app):
        bstack111lll11l1_opy_ = bstack1l111l1ll_opy_(config, app)
      elif bstack111111l1l1_opy_(app):
        bstack111lll11l1_opy_ = app
      else:
        bstack11l1111ll1_opy_(bstack1l1l1ll1l1_opy_.format(app))
    else:
      if bstack111111l1l1_opy_(app):
        bstack111lll11l1_opy_ = app
      elif os.path.exists(app):
        bstack111lll11l1_opy_ = bstack1l111l1ll_opy_(app)
      else:
        bstack11l1111ll1_opy_(bstack1l1l1111l_opy_)
  else:
    if len(app) > 2:
      bstack11l1111ll1_opy_(bstack1l1l1llll_opy_)
    elif len(app) == 2:
      if bstack11lll1_opy_ (u"ࠬࡶࡡࡵࡪࠪ੩") in app and bstack11lll1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩ੪") in app:
        if os.path.exists(app[bstack11lll1_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ੫")]):
          bstack111lll11l1_opy_ = bstack1l111l1ll_opy_(config, app[bstack11lll1_opy_ (u"ࠨࡲࡤࡸ࡭࠭੬")], app[bstack11lll1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ੭")])
        else:
          bstack11l1111ll1_opy_(bstack1l1l1ll1l1_opy_.format(app))
      else:
        bstack11l1111ll1_opy_(bstack1l1l1llll_opy_)
    else:
      for key in app:
        if key in bstack1ll1lll11_opy_:
          if key == bstack11lll1_opy_ (u"ࠪࡴࡦࡺࡨࠨ੮"):
            if os.path.exists(app[key]):
              bstack111lll11l1_opy_ = bstack1l111l1ll_opy_(config, app[key])
            else:
              bstack11l1111ll1_opy_(bstack1l1l1ll1l1_opy_.format(app))
          else:
            bstack111lll11l1_opy_ = app[key]
        else:
          bstack11l1111ll1_opy_(bstack111ll1ll11_opy_)
  return bstack111lll11l1_opy_
def bstack111111l1l1_opy_(bstack111lll11l1_opy_):
  import re
  bstack11lll1ll_opy_ = re.compile(bstack11lll1_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬࠧࠦ੯"))
  bstack1llll11lll_opy_ = re.compile(bstack11lll1_opy_ (u"ࡷࠨ࡞࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭࠳ࡠࡧ࠭ࡻࡃ࠰࡞࠵࠳࠹࡝ࡡ࠱ࡠ࠲ࡣࠪࠥࠤੰ"))
  if bstack11lll1_opy_ (u"࠭ࡢࡴ࠼࠲࠳ࠬੱ") in bstack111lll11l1_opy_ or re.fullmatch(bstack11lll1ll_opy_, bstack111lll11l1_opy_) or re.fullmatch(bstack1llll11lll_opy_, bstack111lll11l1_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack1lllllll1_opy_, stage=STAGE.bstack1lllllll11_opy_, bstack1l11ll11l_opy_=SESSION_NAME)
def bstack1l111l1ll_opy_(config, path, bstack11l1l1l1ll_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack11lll1_opy_ (u"ࠧࡳࡤࠪੲ")).read()).hexdigest()
  bstack11l11ll1ll_opy_ = bstack11l1l1l1_opy_(md5_hash)
  bstack111lll11l1_opy_ = None
  if bstack11l11ll1ll_opy_:
    logger.info(bstack11l11l11ll_opy_.format(bstack11l11ll1ll_opy_, md5_hash))
    return bstack11l11ll1ll_opy_
  bstack111ll1l1_opy_ = datetime.datetime.now()
  multipart_data = MultipartEncoder(
    fields={
      bstack11lll1_opy_ (u"ࠨࡨ࡬ࡰࡪ࠭ੳ"): (os.path.basename(path), open(os.path.abspath(path), bstack11lll1_opy_ (u"ࠩࡵࡦࠬੴ")), bstack11lll1_opy_ (u"ࠪࡸࡪࡾࡴ࠰ࡲ࡯ࡥ࡮ࡴࠧੵ")),
      bstack11lll1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧ੶"): bstack11l1l1l1ll_opy_
    }
  )
  response = requests.post(bstack111l1111l_opy_, data=multipart_data,
                           headers={bstack11lll1_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ੷"): multipart_data.content_type},
                           auth=(config[bstack11lll1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ੸")], config[bstack11lll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ੹")]))
  try:
    res = json.loads(response.text)
    bstack111lll11l1_opy_ = res[bstack11lll1_opy_ (u"ࠨࡣࡳࡴࡤࡻࡲ࡭ࠩ੺")]
    logger.info(bstack1ll1lllll_opy_.format(bstack111lll11l1_opy_))
    bstack11l1l11l1_opy_(md5_hash, bstack111lll11l1_opy_)
    cli.bstack11l111ll1l_opy_(bstack11lll1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺ࡶࡲ࡯ࡳࡦࡪ࡟ࡢࡲࡳࠦ੻"), datetime.datetime.now() - bstack111ll1l1_opy_)
  except ValueError as err:
    bstack11l1111ll1_opy_(bstack1llll1l1l_opy_.format(str(err)))
  return bstack111lll11l1_opy_
def bstack11ll1l1l_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack1l11ll11_opy_
  bstack11l1l1ll11_opy_ = 1
  bstack1lllll1ll_opy_ = 1
  if bstack11lll1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ੼") in CONFIG:
    bstack1lllll1ll_opy_ = CONFIG[bstack11lll1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ੽")]
  else:
    bstack1lllll1ll_opy_ = bstack1l11111ll1_opy_(framework_name, args) or 1
  if bstack11lll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ੾") in CONFIG:
    bstack11l1l1ll11_opy_ = len(CONFIG[bstack11lll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ੿")])
  bstack1l11ll11_opy_ = int(bstack1lllll1ll_opy_) * int(bstack11l1l1ll11_opy_)
def bstack1l11111ll1_opy_(framework_name, args):
  if framework_name == bstack1lll1ll1l_opy_ and args and bstack11lll1_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ઀") in args:
      bstack1l1l11111l_opy_ = args.index(bstack11lll1_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ઁ"))
      return int(args[bstack1l1l11111l_opy_ + 1]) or 1
  return 1
def bstack11l1l1l1_opy_(md5_hash):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack11lll1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡬ࡰࡥ࡮ࠤࡳࡵࡴࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨ࠰ࠥࡻࡳࡪࡰࡪࠤࡧࡧࡳࡪࡥࠣࡪ࡮ࡲࡥࠡࡱࡳࡩࡷࡧࡴࡪࡱࡱࡷࠬં"))
    bstack111l1ll1_opy_ = os.path.join(os.path.expanduser(bstack11lll1_opy_ (u"ࠪࢂࠬઃ")), bstack11lll1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ઄"), bstack11lll1_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭અ"))
    if os.path.exists(bstack111l1ll1_opy_):
      try:
        bstack1l1lll111_opy_ = json.load(open(bstack111l1ll1_opy_, bstack11lll1_opy_ (u"࠭ࡲࡣࠩઆ")))
        if md5_hash in bstack1l1lll111_opy_:
          bstack11lll1lll1_opy_ = bstack1l1lll111_opy_[md5_hash]
          bstack1ll1l1l11l_opy_ = datetime.datetime.now()
          bstack1111ll111l_opy_ = datetime.datetime.strptime(bstack11lll1lll1_opy_[bstack11lll1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪઇ")], bstack11lll1_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬઈ"))
          if (bstack1ll1l1l11l_opy_ - bstack1111ll111l_opy_).days > 30:
            return None
          elif version.parse(str(__version__)) > version.parse(bstack11lll1lll1_opy_[bstack11lll1_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧઉ")]):
            return None
          return bstack11lll1lll1_opy_[bstack11lll1_opy_ (u"ࠪ࡭ࡩ࠭ઊ")]
      except Exception as e:
        logger.debug(bstack11lll1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡶࡪࡧࡤࡪࡰࡪࠤࡒࡊ࠵ࠡࡪࡤࡷ࡭ࠦࡦࡪ࡮ࡨ࠾ࠥࢁࡽࠨઋ").format(str(e)))
    return None
  bstack111l1ll1_opy_ = os.path.join(os.path.expanduser(bstack11lll1_opy_ (u"ࠬࢄࠧઌ")), bstack11lll1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ઍ"), bstack11lll1_opy_ (u"ࠧࡢࡲࡳ࡙ࡵࡲ࡯ࡢࡦࡐࡈ࠺ࡎࡡࡴࡪ࠱࡮ࡸࡵ࡮ࠨ઎"))
  lock_file = bstack111l1ll1_opy_ + bstack11lll1_opy_ (u"ࠨ࠰࡯ࡳࡨࡱࠧએ")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack111l1ll1_opy_):
        with open(bstack111l1ll1_opy_, bstack11lll1_opy_ (u"ࠩࡵࠫઐ")) as f:
          content = f.read().strip()
          if content:
            bstack1l1lll111_opy_ = json.loads(content)
            if md5_hash in bstack1l1lll111_opy_:
              bstack11lll1lll1_opy_ = bstack1l1lll111_opy_[md5_hash]
              bstack1ll1l1l11l_opy_ = datetime.datetime.now()
              bstack1111ll111l_opy_ = datetime.datetime.strptime(bstack11lll1lll1_opy_[bstack11lll1_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ઑ")], bstack11lll1_opy_ (u"ࠫࠪࡪ࠯ࠦ࡯࠲ࠩ࡞ࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨ઒"))
              if (bstack1ll1l1l11l_opy_ - bstack1111ll111l_opy_).days > 30:
                return None
              elif version.parse(str(__version__)) > version.parse(bstack11lll1lll1_opy_[bstack11lll1_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪઓ")]):
                return None
              return bstack11lll1lll1_opy_[bstack11lll1_opy_ (u"࠭ࡩࡥࠩઔ")]
      return None
  except Exception as e:
    logger.debug(bstack11lll1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡷࡪࡶ࡫ࠤ࡫࡯࡬ࡦࠢ࡯ࡳࡨࡱࡩ࡯ࡩࠣࡪࡴࡸࠠࡎࡆ࠸ࠤ࡭ࡧࡳࡩ࠼ࠣࡿࢂ࠭ક").format(str(e)))
    return None
def bstack11l1l11l1_opy_(md5_hash, bstack111lll11l1_opy_):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack11lll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡲ࡯ࡤ࡭ࠣࡲࡴࡺࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧ࠯ࠤࡺࡹࡩ࡯ࡩࠣࡦࡦࡹࡩࡤࠢࡩ࡭ࡱ࡫ࠠࡰࡲࡨࡶࡦࡺࡩࡰࡰࡶࠫખ"))
    bstack1111llll1_opy_ = os.path.join(os.path.expanduser(bstack11lll1_opy_ (u"ࠩࢁࠫગ")), bstack11lll1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪઘ"))
    if not os.path.exists(bstack1111llll1_opy_):
      os.makedirs(bstack1111llll1_opy_)
    bstack111l1ll1_opy_ = os.path.join(os.path.expanduser(bstack11lll1_opy_ (u"ࠫࢃ࠭ઙ")), bstack11lll1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬચ"), bstack11lll1_opy_ (u"࠭ࡡࡱࡲࡘࡴࡱࡵࡡࡥࡏࡇ࠹ࡍࡧࡳࡩ࠰࡭ࡷࡴࡴࠧછ"))
    bstack1l1l111l_opy_ = {
      bstack11lll1_opy_ (u"ࠧࡪࡦࠪજ"): bstack111lll11l1_opy_,
      bstack11lll1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫઝ"): datetime.datetime.strftime(datetime.datetime.now(), bstack11lll1_opy_ (u"ࠩࠨࡨ࠴ࠫ࡭࠰ࠧ࡜ࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭ઞ")),
      bstack11lll1_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨટ"): str(__version__)
    }
    try:
      bstack1l1lll111_opy_ = {}
      if os.path.exists(bstack111l1ll1_opy_):
        bstack1l1lll111_opy_ = json.load(open(bstack111l1ll1_opy_, bstack11lll1_opy_ (u"ࠫࡷࡨࠧઠ")))
      bstack1l1lll111_opy_[md5_hash] = bstack1l1l111l_opy_
      with open(bstack111l1ll1_opy_, bstack11lll1_opy_ (u"ࠧࡽࠫࠣડ")) as outfile:
        json.dump(bstack1l1lll111_opy_, outfile)
    except Exception as e:
      logger.debug(bstack11lll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡻࡰࡥࡣࡷ࡭ࡳ࡭ࠠࡎࡆ࠸ࠤ࡭ࡧࡳࡩࠢࡩ࡭ࡱ࡫࠺ࠡࡽࢀࠫઢ").format(str(e)))
    return
  bstack1111llll1_opy_ = os.path.join(os.path.expanduser(bstack11lll1_opy_ (u"ࠧࡿࠩણ")), bstack11lll1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨત"))
  if not os.path.exists(bstack1111llll1_opy_):
    os.makedirs(bstack1111llll1_opy_)
  bstack111l1ll1_opy_ = os.path.join(os.path.expanduser(bstack11lll1_opy_ (u"ࠩࢁࠫથ")), bstack11lll1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪદ"), bstack11lll1_opy_ (u"ࠫࡦࡶࡰࡖࡲ࡯ࡳࡦࡪࡍࡅ࠷ࡋࡥࡸ࡮࠮࡫ࡵࡲࡲࠬધ"))
  lock_file = bstack111l1ll1_opy_ + bstack11lll1_opy_ (u"ࠬ࠴࡬ࡰࡥ࡮ࠫન")
  bstack1l1l111l_opy_ = {
    bstack11lll1_opy_ (u"࠭ࡩࡥࠩ઩"): bstack111lll11l1_opy_,
    bstack11lll1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪપ"): datetime.datetime.strftime(datetime.datetime.now(), bstack11lll1_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬફ")),
    bstack11lll1_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧબ"): str(__version__)
  }
  try:
    with FileLock(lock_file, timeout=10):
      bstack1l1lll111_opy_ = {}
      if os.path.exists(bstack111l1ll1_opy_):
        with open(bstack111l1ll1_opy_, bstack11lll1_opy_ (u"ࠪࡶࠬભ")) as f:
          content = f.read().strip()
          if content:
            bstack1l1lll111_opy_ = json.loads(content)
      bstack1l1lll111_opy_[md5_hash] = bstack1l1l111l_opy_
      with open(bstack111l1ll1_opy_, bstack11lll1_opy_ (u"ࠦࡼࠨમ")) as outfile:
        json.dump(bstack1l1lll111_opy_, outfile)
  except Exception as e:
    logger.debug(bstack11lll1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡼ࡯ࡴࡩࠢࡩ࡭ࡱ࡫ࠠ࡭ࡱࡦ࡯࡮ࡴࡧࠡࡨࡲࡶࠥࡓࡄ࠶ࠢ࡫ࡥࡸ࡮ࠠࡶࡲࡧࡥࡹ࡫࠺ࠡࡽࢀࠫય").format(str(e)))
def bstack11ll1ll1l1_opy_(self):
  return
def bstack1l11lll1l1_opy_(self):
  return
def bstack111l111111_opy_():
  global bstack1lll1lll_opy_
  bstack1lll1lll_opy_ = True
def bstack1ll1l11ll1_opy_(self):
  global FRAMEWORK_NAME
  global bstack1l11l111l1_opy_
  global bstack1l1ll111l1_opy_
  bstack11lllll1_opy_ = bstack1llll11l_opy_.bstack11ll11l1l_opy_(EVENTS.bstack1llll11111_opy_)
  try:
    if bstack11lll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ર") in FRAMEWORK_NAME and self.session_id != None and bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫ઱"), bstack11lll1_opy_ (u"ࠨࠩલ")) != bstack11lll1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪળ"):
      bstack11111l11l1_opy_ = bstack11lll1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ઴") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11lll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫવ")
      if bstack11111l11l1_opy_ == bstack11lll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬશ"):
        bstack111llll1l_opy_(logger)
      if self != None:
        bstack11111l11_opy_(self, bstack11111l11l1_opy_, bstack11lll1_opy_ (u"࠭ࠬࠡࠩષ").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack11lll1_opy_ (u"ࠧࠨસ")
    if bstack11lll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨહ") in FRAMEWORK_NAME and getattr(threading.current_thread(), bstack11lll1_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ઺"), None):
      bstack1llll11ll_opy_.bstack1ll11ll11_opy_(self, bstack11llll1lll_opy_, logger, wait=True)
    if bstack11lll1_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ઻") in FRAMEWORK_NAME:
      bstack1l11ll1l1l_opy_.bstack111lll11ll_opy_(self)
    bstack1llll11l_opy_.end(EVENTS.bstack1llll11111_opy_.value, bstack11lllll1_opy_ + bstack11lll1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷ઼ࠦ"), bstack11lllll1_opy_ + bstack11lll1_opy_ (u"ࠧࡀࡥ࡯ࡦࠥઽ"), status=True, failure=None, test_name=None)
  except Exception as e:
    logger.debug(bstack11lll1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࠢા") + str(e))
    bstack1llll11l_opy_.end(EVENTS.bstack1llll11111_opy_.value, bstack11lllll1_opy_ + bstack11lll1_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢિ"), bstack11lllll1_opy_ + bstack11lll1_opy_ (u"ࠣ࠼ࡨࡲࡩࠨી"), status=False, failure=str(e), test_name=None)
  bstack1l1ll111l1_opy_(self)
  self.session_id = None
def bstack1lll11111l_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack1l1l11l1l1_opy_
    global FRAMEWORK_NAME
    command_executor = kwargs.get(bstack11lll1_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠬુ"), bstack11lll1_opy_ (u"ࠪࠫૂ"))
    bstack11ll1lll1l_opy_ = False
    if type(command_executor) == str and bstack11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧૃ") in command_executor:
      bstack11ll1lll1l_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨૄ") in str(getattr(command_executor, bstack11lll1_opy_ (u"࠭࡟ࡶࡴ࡯ࠫૅ"), bstack11lll1_opy_ (u"ࠧࠨ૆"))):
      bstack11ll1lll1l_opy_ = True
    else:
      kwargs = a11y.bstack1l1111111_opy_(bstack1l1lll111l_opy_=kwargs, config=CONFIG)
      return bstack1l11l11l_opy_(self, *args, **kwargs)
    if bstack11ll1lll1l_opy_:
      bstack1ll11l1l11_opy_ = TestHubUtils.bstack11lll11lll_opy_(CONFIG, FRAMEWORK_NAME)
      if kwargs.get(bstack11lll1_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩે")):
        kwargs[bstack11lll1_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪૈ")] = bstack1l1l11l1l1_opy_(kwargs[bstack11lll1_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫૉ")], FRAMEWORK_NAME, CONFIG, bstack1ll11l1l11_opy_)
      elif kwargs.get(bstack11lll1_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ૊")):
        kwargs[bstack11lll1_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬો")] = bstack1l1l11l1l1_opy_(kwargs[bstack11lll1_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ૌ")], FRAMEWORK_NAME, CONFIG, bstack1ll11l1l11_opy_)
  except Exception as e:
    logger.error(bstack11lll1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩࡧࡱࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡕࡇࡏࠥࡩࡡࡱࡵ࠽ࠤࢀࢃ્ࠢ").format(str(e)))
  return bstack1l11l11l_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack1ll111llll_opy_, stage=STAGE.bstack1lllllll11_opy_, bstack1l11ll11l_opy_=SESSION_NAME)
def bstack11lll1l1l1_opy_(self, command_executor=bstack11lll1_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰࠳࠵࠻࠳࠶࠮࠱࠰࠴࠾࠹࠺࠴࠵ࠤ૎"), *args, **kwargs):
  global bstack1l11l111l1_opy_
  global bstack1ll111ll1l_opy_
  bstack1ll1l1l111_opy_ = bstack1lll11111l_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack1ll1l1l1l1_opy_.on():
    return bstack1ll1l1l111_opy_
  try:
    logger.debug(bstack11lll1_opy_ (u"ࠩࡆࡳࡲࡳࡡ࡯ࡦࠣࡉࡽ࡫ࡣࡶࡶࡲࡶࠥࡽࡨࡦࡰࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡩࡴࠢࡩࡥࡱࡹࡥࠡ࠯ࠣࡿࢂ࠭૏").format(str(command_executor)))
    logger.debug(bstack11lll1_opy_ (u"ࠪࡌࡺࡨࠠࡖࡔࡏࠤ࡮ࡹࠠ࠮ࠢࡾࢁࠬૐ").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧ૑") in command_executor._url:
      global_config.bstack1111l11l1_opy_(bstack11lll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭૒"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩ૓") in command_executor):
    global_config.bstack1111l11l1_opy_(bstack11lll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ૔"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1ll11lll1l_opy_ = getattr(threading.current_thread(), bstack11lll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡕࡧࡶࡸࡒ࡫ࡴࡢࠩ૕"), None)
  bstack1lll1l1ll_opy_ = {}
  if self.capabilities is not None:
    bstack1lll1l1ll_opy_[bstack11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡲࡦࡳࡥࠨ૖")] = self.capabilities.get(bstack11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ૗"))
    bstack1lll1l1ll_opy_[bstack11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭૘")] = self.capabilities.get(bstack11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭૙"))
    bstack1lll1l1ll_opy_[bstack11lll1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡥ࡯ࡱࡶ࡬ࡳࡳࡹࠧ૚")] = self.capabilities.get(bstack11lll1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ૛"))
  if CONFIG.get(bstack11lll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ૜"), False) and a11y.bstack11ll11l11_opy_(bstack1lll1l1ll_opy_):
    threading.current_thread().a11yPlatform = True
  if bstack11lll1_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ૝") in FRAMEWORK_NAME or bstack11lll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ૞") in FRAMEWORK_NAME:
    TestHubHandler.send_cbt_info(self)
  if bstack11lll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ૟") in FRAMEWORK_NAME and bstack1ll11lll1l_opy_ and bstack1ll11lll1l_opy_.get(bstack11lll1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬૠ"), bstack11lll1_opy_ (u"࠭ࠧૡ")) == bstack11lll1_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨૢ"):
    TestHubHandler.send_cbt_info(self)
  bstack1l11l111l1_opy_ = self.session_id
  with bstack1111lll11l_opy_:
    bstack1ll111ll1l_opy_.append(self)
  return bstack1ll1l1l111_opy_
def bstack111ll1l11l_opy_(args):
  return bstack11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠩૣ") in str(args)
def bstack111l1111_opy_(self, driver_command, *args, **kwargs):
  global bstack1ll1ll1l_opy_
  global bstack11ll1l1l1l_opy_
  bstack1111ll1lll_opy_ = bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭૤"), None) and bstack111ll1ll_opy_(
          threading.current_thread(), bstack11lll1_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ૥"), None)
  bstack1lll11111_opy_ = bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ૦"), None) and bstack111ll1ll_opy_(
          threading.current_thread(), bstack11lll1_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ૧"), None)
  bstack1l111ll111_opy_ = getattr(self, bstack11lll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭૨"), None) != None and getattr(self, bstack11lll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧ૩"), None) == True
  if not bstack11ll1l1l1l_opy_ and bstack11lll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ૪") in CONFIG and CONFIG[bstack11lll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ૫")] == True and accessibility_scripts.bstack1l11ll1111_opy_(driver_command) and (bstack1l111ll111_opy_ or bstack1111ll1lll_opy_ or bstack1lll11111_opy_) and not bstack111ll1l11l_opy_(args):
    try:
      bstack11ll1l1l1l_opy_ = True
      logger.debug(bstack11lll1_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡾࢁࠬ૬").format(driver_command))
      bstack11ll1l1lll_opy_ = perform_scan(self, driver_command=driver_command)
      logger.debug(bstack11ll1l1lll_opy_)
      try:
        log_data = {
          bstack11lll1_opy_ (u"ࠦࡷ࡫ࡱࡶࡧࡶࡸࠧ૭"): {
            bstack11lll1_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࠨ૮"): bstack11lll1_opy_ (u"ࠨࡁ࠲࠳࡜ࡣࡘࡉࡁࡏࠤ૯"),
            bstack11lll1_opy_ (u"ࠢࡱࡣࡵࡥࡲ࡫ࡴࡦࡴࡶࠦ૰"): [
              {
                bstack11lll1_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠣ૱"): driver_command
              }
            ]
          },
          bstack11lll1_opy_ (u"ࠤࡵࡩࡸࡶ࡯࡯ࡵࡨࠦ૲"): {
            bstack11lll1_opy_ (u"ࠥࡦࡴࡪࡹࠣ૳"): {
              bstack11lll1_opy_ (u"ࠦࡲࡹࡧࠣ૴"): bstack11ll1l1lll_opy_.get(bstack11lll1_opy_ (u"ࠧࡳࡳࡨࠤ૵"), bstack11lll1_opy_ (u"ࠨࠢ૶")) if isinstance(bstack11ll1l1lll_opy_, dict) else bstack11lll1_opy_ (u"ࠢࠣ૷"),
              bstack11lll1_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴࠤ૸"): bstack11ll1l1lll_opy_.get(bstack11lll1_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥૹ"), True) if isinstance(bstack11ll1l1lll_opy_, dict) else True
            }
          }
        }
        logger.debug(bstack11lll1_opy_ (u"ࠪࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮ࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡲ࡯ࡨࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠫૺ").format(log_data))
        automation_logger.info(json.dumps(log_data, separators=(bstack11lll1_opy_ (u"ࠫ࠱࠭ૻ"), bstack11lll1_opy_ (u"ࠬࡀࠧૼ"))))
      except Exception as bstack1l1l1l1l1l_opy_:
        logger.debug(bstack11lll1_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢ࡯ࡳ࡬ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡤࡣࡱࠤࡩࡧࡴࡢ࠼ࠣࡿࢂ࠭૽").format(str(bstack1l1l1l1l1l_opy_)))
    except Exception as err:
      logger.debug(bstack11lll1_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡪࡸࡦࡰࡴࡰࠤࡸࡩࡡ࡯ࠢࡾࢁࠬ૾").format(str(err)))
    bstack11ll1l1l1l_opy_ = False
  response = bstack1ll1ll1l_opy_(self, driver_command, *args, **kwargs)
  if (bstack11lll1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ૿") in str(FRAMEWORK_NAME).lower() or bstack11lll1_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ଀") in str(FRAMEWORK_NAME).lower()) and bstack1ll1l1l1l1_opy_.on():
    try:
      if driver_command == bstack11lll1_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧଁ"):
        TestHubHandler.bstack1l11lll11_opy_({
            bstack11lll1_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪଂ"): response[bstack11lll1_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫଃ")],
            bstack11lll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭଄"): TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack1ll1l1l1l1_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
def bstack11111l1l11_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack1l11l111l1_opy_
  global PLATFORM_INDEX
  global SESSION_NAME
  global PARALLELISE_VANILLA_PYTHON
  global PARALLELISE_THREADING_PYTHON
  global FRAMEWORK_NAME
  global bstack1l11l11l_opy_
  global bstack1ll111ll1l_opy_
  global bstack1l11l1l1l_opy_
  global bstack11llll1lll_opy_
  bstack11lllll1_opy_ = bstack1llll11l_opy_.bstack11ll11l1l_opy_(EVENTS.bstack111l11l1l_opy_.value)
  if os.getenv(bstack11lll1_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬଅ")) is not None and a11y.bstack111ll11l11_opy_(CONFIG) is None:
    CONFIG[bstack11lll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨଆ")] = True
  CONFIG[bstack11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫଇ")] = str(FRAMEWORK_NAME) + str(__version__)
  bstack1l111ll1l_opy_ = os.environ[bstack11lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨଈ")]
  bstack1ll11l1l11_opy_ = TestHubUtils.bstack11lll11lll_opy_(CONFIG, FRAMEWORK_NAME)
  CONFIG[bstack11lll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧଉ")] = bstack1l111ll1l_opy_
  CONFIG[bstack11lll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧଊ")] = bstack1ll11l1l11_opy_
  if CONFIG.get(bstack11lll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ଋ"),bstack11lll1_opy_ (u"ࠧࠨଌ")) and bstack11lll1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ଍") in FRAMEWORK_NAME:
    CONFIG[bstack11lll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ଎")].pop(bstack11lll1_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨଏ"), None)
    CONFIG[bstack11lll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫଐ")].pop(bstack11lll1_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ଑"), None)
  command_executor = bstack1111ll1ll_opy_()
  logger.debug(bstack1lll11llll_opy_.format(command_executor))
  proxy = bstack1ll1l1lll_opy_(CONFIG, proxy)
  bstack11l111lll1_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
  try:
    if PARALLELISE_VANILLA_PYTHON is True:
      bstack11l111lll1_opy_ = int(multiprocessing.current_process().name)
    elif PARALLELISE_THREADING_PYTHON is True:
      bstack11l111lll1_opy_ = int(threading.current_thread().name)
  except:
    bstack11l111lll1_opy_ = 0
  bstack1l1lll1ll1_opy_ = get_caps(CONFIG, bstack11l111lll1_opy_)
  logger.debug(CONFIG_FILE_CONTENT.format(str(bstack1l1lll1ll1_opy_)))
  if bstack11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ଒") in CONFIG and bstack1lll11l1_opy_(CONFIG[bstack11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫଓ")]):
    update_caps_for_local(bstack1l1lll1ll1_opy_)
  if a11y.is_enabled_platform(CONFIG, bstack11l111lll1_opy_) and a11y.is_platform_supported(bstack1l1lll1ll1_opy_, options, desired_capabilities, CONFIG):
    threading.current_thread().a11yPlatform = True
    if (cli.accessibility is None or not cli.accessibility.is_enabled()):
      a11y.set_capabilities(bstack1l1lll1ll1_opy_, CONFIG)
  if desired_capabilities:
    bstack1l11lll1ll_opy_ = bstack11l11l1l_opy_(desired_capabilities)
    bstack1l11lll1ll_opy_[bstack11lll1_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨଔ")] = bstack1l1l11l1_opy_(CONFIG)
    bstack1l11l1l1_opy_ = get_caps(bstack1l11lll1ll_opy_)
    if bstack1l11l1l1_opy_:
      bstack1l1lll1ll1_opy_ = update(bstack1l11l1l1_opy_, bstack1l1lll1ll1_opy_)
    desired_capabilities = None
  if options:
    bstack11l11111ll_opy_(options, bstack1l1lll1ll1_opy_)
  if not options:
    options = bstack1111llll11_opy_(bstack1l1lll1ll1_opy_)
  try:
    if bstack1111lll1ll_opy_:
      def _1lll1l1111_opy_(bstack1111l1l111_opy_):
        if not isinstance(bstack1111l1l111_opy_, dict):
          return
        for _1llll1lll1_opy_ in list(bstack1111l1l111_opy_.keys()):
          _1l111ll1l1_opy_ = bstack1111l1l111_opy_[_1llll1lll1_opy_]
          if _1l111ll1l1_opy_ is None:
            bstack1111l1l111_opy_.pop(_1llll1lll1_opy_, None)
          elif isinstance(_1l111ll1l1_opy_, dict):
            _1lll1l1111_opy_(_1l111ll1l1_opy_)
      _1lll1l1111_opy_(bstack1l1lll1ll1_opy_)
      _1lll1l1111_opy_(desired_capabilities)
      if options is not None and hasattr(options, bstack11lll1_opy_ (u"ࠩࡢࡧࡦࡶࡳࠨକ")):
        _1lll1l1111_opy_(options._caps)
  except Exception as e:
    logger.debug(bstack11lll1_opy_ (u"ࠥࡱࡴࡪ࡟ࡪࡰ࡬ࡸ࠭࠯ࠠࡱࡱࡶࡸ࠲ࡵࡰࡵ࡫ࡲࡲࡸࠦࡰࡳࡷࡱࡩࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡾࠤଖ").format(e))
  if bstack1111lll1ll_opy_:
    options = bstack111l1ll1ll_opy_(options)
  bstack11llll1lll_opy_ = CONFIG.get(bstack11lll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଗ"))[bstack11l111lll1_opy_]
  if proxy and bstack1ll11lll11_opy_() >= version.parse(bstack11lll1_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬଘ")):
    options.proxy(proxy)
  if options and bstack1ll11lll11_opy_() >= version.parse(bstack11lll1_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬଙ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1ll11lll11_opy_() < version.parse(bstack11lll1_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ଚ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1l1lll1ll1_opy_)
  logger.info(bstack1ll1l1ll1l_opy_)
  bstack1lll11lll_opy_.end(EVENTS.bstack11l111l1ll_opy_.value, EVENTS.bstack11l111l1ll_opy_.value + bstack11lll1_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣଛ"), EVENTS.bstack11l111l1ll_opy_.value + bstack11lll1_opy_ (u"ࠤ࠽ࡩࡳࡪࠢଜ"), status=True, failure=None, test_name=SESSION_NAME)
  if bstack11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡵࡸ࡯ࡧ࡫࡯ࡩࠬଝ") in kwargs:
    del kwargs[bstack11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡶࡲࡰࡨ࡬ࡰࡪ࠭ଞ")]
  bstack1llll11l_opy_.end(EVENTS.bstack111l11l1l_opy_.value, bstack11lllll1_opy_ + bstack11lll1_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧଟ"), bstack11lllll1_opy_ + bstack11lll1_opy_ (u"ࠨ࠺ࡦࡰࡧࠦଠ"), status=True, failure=None, test_name=SESSION_NAME)
  try:
    if bstack1ll11lll11_opy_() >= version.parse(bstack11lll1_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧଡ")):
      bstack1l11l11l_opy_(self, command_executor=command_executor,
                options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
    elif bstack1ll11lll11_opy_() >= version.parse(bstack11lll1_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧଢ")):
      bstack1l11l11l_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities, options=options,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1ll11lll11_opy_() >= version.parse(bstack11lll1_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩଣ")):
      bstack1l11l11l_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    else:
      bstack1l11l11l_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive)
  except Exception as bstack1l1ll1ll11_opy_:
    logger.error(bstack1l111111l1_opy_.format(bstack11lll1_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠩତ"), str(bstack1l1ll1ll11_opy_)))
    raise bstack1l1ll1ll11_opy_
  bstack11lllll1_opy_ = bstack1llll11l_opy_.bstack11ll11l1l_opy_(EVENTS.bstack1ll111llll_opy_.value)
  if a11y.is_enabled_platform(CONFIG, bstack11l111lll1_opy_) and a11y.is_platform_supported(self.caps, options, desired_capabilities):
    if CONFIG[bstack11lll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ଥ")][bstack11lll1_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫଦ")] == True:
      threading.current_thread().appA11yPlatform = True
      if cli.accessibility is None or not cli.accessibility.is_enabled():
        a11y.set_capabilities(bstack1l1lll1ll1_opy_, CONFIG)
  try:
    bstack1l1111llll_opy_ = bstack11lll1_opy_ (u"࠭ࠧଧ")
    if bstack1ll11lll11_opy_() >= version.parse(bstack11lll1_opy_ (u"ࠧ࠵࠰࠳࠲࠵ࡨ࠱ࠨନ")):
      if self.caps is not None:
        bstack1l1111llll_opy_ = self.caps.get(bstack11lll1_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣ଩"))
    else:
      if self.capabilities is not None:
        bstack1l1111llll_opy_ = self.capabilities.get(bstack11lll1_opy_ (u"ࠤࡲࡴࡹ࡯࡭ࡢ࡮ࡋࡹࡧ࡛ࡲ࡭ࠤପ"))
    if bstack1l1111llll_opy_:
      bstack111lll11l_opy_(bstack1l1111llll_opy_)
      if bstack1ll11lll11_opy_() <= version.parse(bstack11lll1_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪଫ")):
        if bstack1llllllll_opy_.startswith(bstack11lll1_opy_ (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࠬବ")) or bstack1llllllll_opy_.startswith(bstack11lll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠧଭ")):
          self.command_executor._url = bstack1llllllll_opy_
        else:
          self.command_executor._url = bstack11lll1_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢମ") + bstack1llllllll_opy_ + bstack11lll1_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦଯ")
      else:
        self.command_executor._url = bstack11lll1_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥର") + bstack1l1111llll_opy_ + bstack11lll1_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥ଱")
      logger.debug(bstack1l11l111ll_opy_.format(bstack1l1111llll_opy_))
    else:
      logger.debug(bstack11ll11ll1_opy_.format(bstack11lll1_opy_ (u"ࠥࡓࡵࡺࡩ࡮ࡣ࡯ࠤࡍࡻࡢࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧࠦଲ")))
  except Exception as e:
    logger.debug(bstack11ll11ll1_opy_.format(e))
  if bstack11lll1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪଳ") in FRAMEWORK_NAME:
    bstack1llll1lll_opy_(PLATFORM_INDEX, bstack1l11l1l1l_opy_)
  bstack1l11l111l1_opy_ = self.session_id
  if bstack11lll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ଴") in FRAMEWORK_NAME or bstack11lll1_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ଵ") in FRAMEWORK_NAME or bstack11lll1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ଶ") in FRAMEWORK_NAME or bstack11lll1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩଷ") in FRAMEWORK_NAME:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack1ll11lll1l_opy_ = getattr(threading.current_thread(), bstack11lll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡖࡨࡷࡹࡓࡥࡵࡣࠪସ"), None)
  if bstack11lll1_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪହ") in FRAMEWORK_NAME or bstack11lll1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ଺") in FRAMEWORK_NAME:
    TestHubHandler.send_cbt_info(self)
  if bstack11lll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ଻") in FRAMEWORK_NAME and bstack1ll11lll1l_opy_ and bstack1ll11lll1l_opy_.get(bstack11lll1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ଼࠭"), bstack11lll1_opy_ (u"ࠧࠨଽ")) == bstack11lll1_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩା"):
    TestHubHandler.send_cbt_info(self)
  with bstack1111lll11l_opy_:
    bstack1ll111ll1l_opy_.append(self)
  if bstack11lll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬି") in CONFIG and bstack11lll1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨୀ") in CONFIG[bstack11lll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧୁ")][bstack11l111lll1_opy_]:
    SESSION_NAME = CONFIG[bstack11lll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨୂ")][bstack11l111lll1_opy_][bstack11lll1_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫୃ")]
  logger.debug(bstack1ll111l1ll_opy_.format(bstack1l11l111l1_opy_))
  bstack1llll11l_opy_.end(EVENTS.bstack1ll111llll_opy_.value, bstack11lllll1_opy_ + bstack11lll1_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢୄ"), bstack11lllll1_opy_ + bstack11lll1_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ୅"), status=True, failure=None, test_name=SESSION_NAME)
ROBOT_PLAYWRIGHT_CDP_URL = None
bstack1lll1ll11l_opy_ = False
bstack1ll11l1ll_opy_ = None
def set_playwright_globals(**kwargs):
    bstack11lll1_opy_ (u"ࠤࠥࠦࡎࡴࡪࡦࡥࡷࠤ࡬ࡲ࡯ࡣࡣ࡯ࡷࠥ࡬ࡲࡰ࡯ࠣࡣࡤ࡯࡮ࡪࡶࡢࡣ࠳ࡶࡹࠡ࡫ࡱࡸࡴࠦࡴࡩ࡫ࡶࠤࡲࡵࡤࡶ࡮ࡨࠫࡸࠦ࡮ࡢ࡯ࡨࡷࡵࡧࡣࡦ࠰ࠍࠤࠥࠦࠠࡄࡣ࡯ࡰࡪࡪࠠࡣࡻࠣࡣࡤ࡯࡮ࡪࡶࡢࡣ࠳ࡶࡹࠡࡤࡨࡪࡴࡸࡥࠡࡲࡤࡸࡨ࡮࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠬ࠮ࠦࡳࡰࠢࡷ࡬ࡦࡺࠠ࡮ࡱࡧࡣࡱࡧࡵ࡯ࡥ࡫ࠎࠥࠦࠠࠡࡣࡱࡨࠥࡶࡡࡵࡥ࡫ࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡥࡤࡲࠥࡧࡣࡤࡧࡶࡷࠥࡉࡏࡏࡈࡌࡋ࠱ࠦࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࡡࡑࡅࡒࡋࠬࠡࡧࡷࡧ࠳ࠨࠢࠣ୆")
    g = globals()
    for key, value in kwargs.items():
        g[key] = value
try:
  try:
    import Browser
    import os
    from subprocess import Popen
    from browserstack_sdk.__init__ import get_turboscale_playwright_url
    from browserstack_sdk.sdk_cli.utils.bstack11lll1ll1l_opy_ import bstack1l11llll_opy_
    def bstack1ll1l11ll_opy_(self, args, **kwargs):
      global CONFIG
      global SELENIUM_OR_PLAYWRIGHT_INSTALLED
      global ROBOT_PLAYWRIGHT_CDP_URL
      global bstack1lll1ll11l_opy_
      from browserstack_sdk.__init__ import LAUNCH_PATCH_ROBOT_PLAYWRIGHT
      if(bstack11lll1_opy_ (u"ࠥ࡭ࡳࡪࡥࡹ࠰࡭ࡷࠧେ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack11lll1_opy_ (u"ࠫࢃ࠭ୈ")), bstack11lll1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ୉"), bstack11lll1_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨ୊")), bstack11lll1_opy_ (u"ࠧࡸࠩୋ")) as fp:
          fp.write(bstack11lll1_opy_ (u"ࠣࠤୌ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack11lll1_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸࡠࡤࡶࡸࡦࡩ࡫࠯࡬ࡶ୍ࠦ")))):
          with open(args[1], bstack11lll1_opy_ (u"ࠪࡶࠬ୎")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack11lll1_opy_ (u"ࠫࡦࡹࡹ࡯ࡥࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࡥ࡮ࡦࡹࡓࡥ࡬࡫ࠨࡤࡱࡱࡸࡪࡾࡴ࠭ࠢࡳࡥ࡬࡫ࠠ࠾ࠢࡹࡳ࡮ࡪࠠ࠱ࠫࠪ୏") in line), None)
            if index is not None:
                lines.insert(index+2, bstack11ll1l11l_opy_)
            if bstack11lll1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ୐") in CONFIG and str(CONFIG[bstack11lll1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ୑")]).lower() != bstack11lll1_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭୒"):
                cdpUrl = get_turboscale_playwright_url()
                LAUNCH_PATCH_ROBOT_PLAYWRIGHT = bstack11lll1_opy_ (u"ࠨࠩࠪࠎ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠊࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠻࡝ࠡ࠿ࡀࡁࠥ࠭ࡴࡳࡷࡨࠫࡀࠐࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹࡝࠼ࠌࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠ࠿ࠏࡩ࡯࡯ࡵࡷࠤࡵࡥࡩ࡯ࡦࡨࡼࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠳࡟࠾ࠎࡨࡵ࡮ࡴࡶࠣࡦࡸࡺࡡࡤ࡭ࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠺࡝ࠡ࠿ࡀࡁࠥ࠭ࡴࡳࡷࡨࠫࡀࠐࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴ࡳ࡭࡫ࡦࡩ࠭࠶ࠬࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠸࠭ࡀࠐࡣࡰࡰࡶࡸࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭ࠣࡁࠥࡸࡥࡲࡷ࡬ࡶࡪ࠮ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦ࠮ࡁࠊࡤࡱࡱࡷࡹࠦ࡯ࡳ࡫ࡪ࡭ࡳࡧ࡬ࡠࡥ࡫ࡶࡴࡳࡩࡶ࡯ࡢࡰࡦࡻ࡮ࡤࡪࠣࡁࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡲࡡࡶࡰࡦ࡬࠳ࡨࡩ࡯ࡦࠫ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯ࠬ࠿ࠏ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡲࡡࡶࡰࡦ࡬ࠥࡃࠠࡢࡵࡼࡲࡨࠦࠨ࡭ࡣࡸࡲࡨ࡮ࡏࡱࡶ࡬ࡳࡳࡹࠩࠡ࠿ࡁࠤࢀࢁࠊࠡࠢ࡬ࡪࠥ࠮ࠡࡣࡵࡷࡥࡨࡱ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠭ࠥࢁࡻࠋࠢࠣࠤࠥࡸࡥࡵࡷࡵࡲࠥࡧࡷࡢ࡫ࡷࠤࡴࡸࡩࡨ࡫ࡱࡥࡱࡥࡣࡩࡴࡲࡱ࡮ࡻ࡭ࡠ࡮ࡤࡹࡳࡩࡨࠩ࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠪ࠽ࠍࠤࠥࢃࡽࠋࠢࠣࡰࡪࡺࠠࡤࡣࡳࡷࡀࠐࠠࠡࡶࡵࡽࠥࢁࡻࠋࠢࠣࠤࠥࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࠼ࠌࠣࠤࢂࢃࠠࡤࡣࡷࡧ࡭ࠦࠨࡦࡺࠬࠤࢀࢁࠊࠡࠢࠣࠤࡨࡵ࡮ࡴࡱ࡯ࡩ࠳࡫ࡲࡳࡱࡵࠬࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࡀࠢ࠭ࠢࡨࡼ࠮ࡁࠊࠡࠢࢀࢁࠏࠦࠠࡪࡨࠣࠬࡧࡹࡴࡢࡥ࡮ࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ࠭ࠥࢁࡻࠋࠢࠣࠤࠥࡸࡥࡵࡷࡵࡲࠥࡧࡷࡢ࡫ࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡨࡵ࡮࡯ࡧࡦࡸࡔࡼࡥࡳࡅࡇࡔ࠭ࢁࡻࠋࠢࠣࠤࠥࠦࠠࡦࡰࡧࡴࡴ࡯࡮ࡵࡗࡕࡐ࠿ࠦࠧࡼࡥࡧࡴ࡚ࡸ࡬ࡾࠩࠣ࠯ࠥ࡫࡮ࡤࡱࡧࡩ࡚ࡘࡉࡄࡱࡰࡴࡴࡴࡥ࡯ࡶࠫࡎࡘࡕࡎ࠯ࡵࡷࡶ࡮ࡴࡧࡪࡨࡼࠬࡨࡧࡰࡴࠫࠬ࠰ࠏࠦࠠࠡࠢࠣࠤ࠳࠴࠮࡭ࡣࡸࡲࡨ࡮ࡏࡱࡶ࡬ࡳࡳࡹࠊࠡࠢࠣࠤࢂࢃࠩ࠼ࠌࠣࠤࢂࢃࠊࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭࠯ࡥࡲࡲࡳ࡫ࡣࡵࠪࡾࡿࠏࠦࠠࠡࠢࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹࡀࠠࠨࡽࡦࡨࡵ࡛ࡲ࡭ࡿࠪࠤ࠰ࠦࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭࠱ࠐࠠࠡࠢࠣ࠲࠳࠴࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸࠐࠠࠡࡿࢀ࠭ࡀࠐࡽࡾ࠽ࠍࡧࡴࡴࡳࡵࠢࡲࡶ࡮࡭ࡩ࡯ࡣ࡯ࡣࡨࡵ࡮࡯ࡧࡦࡸࠥࡃࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮ࡤࡱࡱࡲࡪࡩࡴ࠯ࡤ࡬ࡲࡩ࠮ࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠯࠻ࠋ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭࠯ࡥࡲࡲࡳ࡫ࡣࡵࠢࡀࠤࡦࡹࡹ࡯ࡥࠣࠬࡨࡵ࡮࡯ࡧࡦࡸࡔࡶࡴࡪࡱࡱࡷ࠮ࠦ࠽࠿ࠢࡾࡿࠏࠦࠠࡪࡨࠣࠬࠦࡨࡳࡵࡣࡦ࡯ࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠫࠣࡿࢀࠐࠠࠡࠢࠣࡶࡪࡺࡵࡳࡰࠣࡥࡼࡧࡩࡵࠢࡲࡶ࡮࡭ࡩ࡯ࡣ࡯ࡣࡨࡵ࡮࡯ࡧࡦࡸ࠭ࡩ࡯࡯ࡰࡨࡧࡹࡕࡰࡵ࡫ࡲࡲࡸ࠯࠻ࠋࠢࠣࢁࢂࠐࠠࠡ࡮ࡨࡸࠥࡩࡡࡱࡵ࠾ࠎࠥࠦࡴࡳࡻࠣࡿࢀࠐࠠࠡࠢࠣࡧࡦࡶࡳࠡ࠿ࠣࡎࡘࡕࡎ࠯ࡲࡤࡶࡸ࡫ࠨࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷ࠮ࡁࠊࠡࠢࢀࢁࠥࡩࡡࡵࡥ࡫ࠤ࠭࡫ࡸࠪࠢࡾࡿࠏࠦࠠࡾࡿࠍࠤࠥࡩ࡯࡯ࡵࡷࠤࡲࡵࡤࡪࡨ࡬ࡩࡩࡋ࡮ࡥࡲࡲ࡭ࡳࡺࠠ࠾ࠢࠪࡿࡨࡪࡰࡖࡴ࡯ࢁࠬࠦࠫࠡࡧࡱࡧࡴࡪࡥࡖࡔࡌࡇࡴࡳࡰࡰࡰࡨࡲࡹ࠮ࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡤࡣࡳࡷ࠮࠯࠻ࠋࠢࠣ࡭࡫ࠦࠨࡣࡵࡷࡥࡨࡱ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠩࠡࡽࡾࠎࠥࠦࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡣࡺࡥ࡮ࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮ࡤࡱࡱࡲࡪࡩࡴࡐࡸࡨࡶࡈࡊࡐࠩࡽࡾࠎࠥࠦࠠࠡࠢࠣࡩࡳࡪࡰࡰ࡫ࡱࡸ࡚ࡘࡌ࠻ࠢࡰࡳࡩ࡯ࡦࡪࡧࡧࡉࡳࡪࡰࡰ࡫ࡱࡸ࠱ࠐࠠࠡࠢࠣࠤࠥ࠴࠮࠯ࡥࡲࡲࡳ࡫ࡣࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠌࠣࠤࠥࠦࡽࡾࠫ࠾ࠎࠥࠦࡽࡾࠌࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣࡳࡷ࡯ࡧࡪࡰࡤࡰࡤࡩ࡯࡯ࡰࡨࡧࡹ࠮ࡻࡼࠌࠣࠤࠥࠦ࠮࠯࠰ࡦࡳࡳࡴࡥࡤࡶࡒࡴࡹ࡯࡯࡯ࡵ࠯ࠎࠥࠦࠠࠡࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸ࠿ࠦ࡭ࡰࡦ࡬ࡪ࡮࡫ࡤࡆࡰࡧࡴࡴ࡯࡮ࡵࠌࠣࠤࢂࢃࠩ࠼ࠌࢀࢁࡀࠐ࠯ࠫࠢࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࠦࠪ࠰ࠌࠪࠫࠬ୓").format(cdpUrl=cdpUrl)
            lines.insert(1, LAUNCH_PATCH_ROBOT_PLAYWRIGHT)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack11lll1_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸࡠࡤࡶࡸࡦࡩ࡫࠯࡬ࡶࠦ୔")), bstack11lll1_opy_ (u"ࠪࡻࠬ୕")) as bstack1lllll1ll1_opy_:
              bstack1lllll1ll1_opy_.writelines(lines)
        CONFIG[bstack11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ୖ")] = str(FRAMEWORK_NAME) + str(__version__)
        bstack1l111ll1l_opy_ = os.environ[bstack11lll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪୗ")]
        bstack1ll11l1l11_opy_ = TestHubUtils.bstack11lll11lll_opy_(CONFIG, FRAMEWORK_NAME)
        CONFIG[bstack11lll1_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ୘")] = bstack1l111ll1l_opy_
        CONFIG[bstack11lll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩ୙")] = bstack1ll11l1l11_opy_
        bstack11l111lll1_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
        try:
          if PARALLELISE_VANILLA_PYTHON is True:
            bstack11l111lll1_opy_ = int(multiprocessing.current_process().name)
          elif PARALLELISE_THREADING_PYTHON is True:
            bstack11l111lll1_opy_ = int(threading.current_thread().name)
        except Exception:
          bstack11l111lll1_opy_ = 0
        CONFIG[bstack11lll1_opy_ (u"ࠣࡷࡶࡩ࡜࠹ࡃࠣ୚")] = False
        CONFIG[bstack11lll1_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ୛")] = True
        bstack111llll1_opy_ = bstack1l11llll_opy_(bstack11l111lll1_opy_)
        if bstack111llll1_opy_ is not None:
          import bstack_utils.constants as _11l1lllll_opy_
          _111ll11ll_opy_ = bstack11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫଡ଼") if bstack11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬଢ଼") in bstack111llll1_opy_ else bstack11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ୞")
          _1ll11ll1l1_opy_ = bstack111llll1_opy_.get(_111ll11ll_opy_, bstack11lll1_opy_ (u"࠭ࠧୟ")).strip().lower()
          _11llll11l_opy_ = _1ll11ll1l1_opy_ in _11l1lllll_opy_.bstack1ll1111l1l_opy_
          if bstack111llll1_opy_.get(bstack11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ୠ")) and not _11llll11l_opy_:
            bstack111llll1_opy_[bstack11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧୡ")] = False
            _1l1lll11_opy_ = [k for k in bstack111llll1_opy_ if k.startswith(bstack11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨୢ"))]
            for k in _1l1lll11_opy_:
              del bstack111llll1_opy_[k]
          bstack11ll11l1ll_opy_ = bstack111llll1_opy_
          import urllib.parse
          if bstack11lll1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧୣ") in CONFIG and str(CONFIG[bstack11lll1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ୤")]).lower() != bstack11lll1_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ୥"):
            ROBOT_PLAYWRIGHT_CDP_URL = get_turboscale_playwright_url() + urllib.parse.quote(json.dumps(bstack11ll11l1ll_opy_))
          else:
            ROBOT_PLAYWRIGHT_CDP_URL = bstack11lll1_opy_ (u"࠭ࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠨ୦") + urllib.parse.quote(json.dumps(bstack11ll11l1ll_opy_))
          os.environ[bstack11lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡐࡄࡒࡘࡤࡖࡗࡠࡅࡇࡔࡤ࡛ࡒࡍࠩ୧")] = ROBOT_PLAYWRIGHT_CDP_URL
          bstack1lll1ll11l_opy_ = True
          from browserstack_sdk.sdk_cli.bstack1llll1ll1l_opy_ import bstack1l1lll1111_opy_
          from browserstack_sdk.sdk_cli.bstack11l1l1ll1_opy_ import bstack1l1l11ll1l_opy_
          instance = next(iter(bstack1l1lll1111_opy_.bstack11l1lll111_opy_.values()), None)
          if instance:
            bstack1l1l11ll1l_opy_.bstack1ll1ll1l1l_opy_(instance, bstack1l1l11ll1l_opy_.bstack1l1l111l11_opy_, bstack111llll1_opy_)
            bstack1l1l11ll1l_opy_.bstack1ll1ll1l1l_opy_(instance, bstack1l1l11ll1l_opy_.bstack11l1111lll_opy_, ROBOT_PLAYWRIGHT_CDP_URL)
          try:
            from browserstack_sdk.sdk_cli.cli import cli as _11lll111l1_opy_
            from browserstack_sdk.sdk_cli.bstack1llll1ll1l_opy_ import bstack111ll1lll1_opy_, bstack11lllll11l_opy_
            _11lll111l1_opy_.bstack1llll1ll1l_opy_.bstack1ll1ll111l_opy_(
              None,
              (instance, bstack11lll1_opy_ (u"ࠨ࡯ࡲࡨࡤࡶ࡯ࡱࡧࡱࠫ୨")),
              (bstack111ll1lll1_opy_.bstack1l1111ll11_opy_, bstack11lllll11l_opy_.PRE),
              None,
            )
          except Exception as e:
            logger.debug(bstack11lll1_opy_ (u"ࠤࡰࡳࡩࡥࡰࡰࡲࡨࡲ࠿ࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡩ࡭ࡷ࡫ࠠࡄࡔࡈࡅ࡙ࡋ࠮ࡑࡔࡈ࠾ࠥࢁࡽࠣ୩").format(e))
          logger.debug(bstack11lll1_opy_ (u"ࠥࡱࡴࡪ࡟ࡱࡱࡳࡩࡳࡀࠠࡶࡵ࡬ࡲ࡬ࠦࡦࡪࡰࡤࡰࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠤ࡫ࡸ࡯࡮ࠢࡇࡶ࡮ࡼࡥࡳࡋࡱ࡭ࡹࠨ୪"))
        else:
          bstack11ll11l1ll_opy_ = get_caps(CONFIG, bstack11l111lll1_opy_)
          if CONFIG.get(bstack11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ୫")):
            update_caps_for_local(bstack11ll11l1ll_opy_)
            bstack11ll11l1ll_opy_[bstack11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭୬")] = os.environ[bstack11lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨ୭")]
          logger.debug(bstack11lll1_opy_ (u"ࠢ࡮ࡱࡧࡣࡵࡵࡰࡦࡰ࠽ࠤࡉࡸࡩࡷࡧࡵࡍࡳ࡯ࡴࠡࡷࡱࡥࡻࡧࡩ࡭ࡣࡥࡰࡪ࠲ࠠࡧࡣ࡯ࡰ࡮ࡴࡧࠡࡤࡤࡧࡰࠦࡴࡰࠢࡪࡩࡹࡥࡣࡢࡲࡶࠦ୮"))
        logger.debug(CONFIG_FILE_CONTENT.format(str(bstack11ll11l1ll_opy_)))
        if bstack11lll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ୯") in CONFIG and bstack11lll1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ୰") in CONFIG[bstack11lll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ୱ")][bstack11l111lll1_opy_]:
          SESSION_NAME = CONFIG[bstack11lll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ୲")][bstack11l111lll1_opy_][bstack11lll1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ୳")]
        from bstack_utils.helper import bstack1ll111l11l_opy_
        args.append(bstack11lll1_opy_ (u"࠭ࡴࡳࡷࡨࠫ୴") if bstack1ll111l11l_opy_(CONFIG) else bstack11lll1_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭୵"))
        args.append(str(bstack11ll11l1ll_opy_.get(bstack11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ୶"), False)).lower())
        args.append(os.path.join(os.path.expanduser(bstack11lll1_opy_ (u"ࠩࢁࠫ୷")), bstack11lll1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ୸"), bstack11lll1_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭୹")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack11ll11l1ll_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack11lll1_opy_ (u"ࠧ࡯࡮ࡥࡧࡻࡣࡧࡹࡴࡢࡥ࡮࠲࡯ࡹࠢ୺"))
      SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
      return bstack1l1111l1l_opy_(self, args, **kwargs)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1l11ll11l1_opy_(self,
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
    CONFIG[bstack11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ୻")] = str(FRAMEWORK_NAME) + str(__version__)
    bstack1l111ll1l_opy_ = os.environ[bstack11lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ୼")]
    bstack1ll11l1l11_opy_ = TestHubUtils.bstack11lll11lll_opy_(CONFIG, FRAMEWORK_NAME)
    CONFIG[bstack11lll1_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ୽")] = bstack1l111ll1l_opy_
    CONFIG[bstack11lll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ୾")] = bstack1ll11l1l11_opy_
    bstack11l111lll1_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
    try:
      if PARALLELISE_VANILLA_PYTHON is True:
        bstack11l111lll1_opy_ = int(multiprocessing.current_process().name)
      elif PARALLELISE_THREADING_PYTHON is True:
        bstack11l111lll1_opy_ = int(threading.current_thread().name)
    except Exception:
      bstack11l111lll1_opy_ = 0
    CONFIG[bstack11lll1_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤ୿")] = True
    bstack1l1lll1ll1_opy_ = get_caps(CONFIG, bstack11l111lll1_opy_)
    bstack1llll1ll_opy_ = bstack11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬ஀") if bstack11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭஁") in bstack1l1lll1ll1_opy_ else bstack11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫஂ")
    bstack1l1l111111_opy_ = False
    try:
        from bstack_utils import accessibility as a11y
        import bstack_utils.constants as bstack1l11llllll_opy_
        bstack11l111l1l1_opy_ = bstack1l1lll1ll1_opy_.get(bstack1llll1ll_opy_, bstack11lll1_opy_ (u"ࠧࠨஃ")).strip().lower()
        browser_version = str(bstack1l1lll1ll1_opy_.get(bstack11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪ஄"), bstack1l1lll1ll1_opy_.get(bstack11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪஅ"), bstack11lll1_opy_ (u"ࠪࠫஆ")))).strip()
        bstack1l1ll1l11_opy_ = bstack11l111l1l1_opy_ in bstack1l11llllll_opy_.bstack1ll1111l1l_opy_
        min_version = bstack1l11llllll_opy_.MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION
        if not browser_version or browser_version.lower().startswith(bstack11lll1_opy_ (u"ࠫࡱࡧࡴࡦࡵࡷࠫஇ")):
            bstack11l11ll1_opy_ = True
        else:
            major = browser_version.split(bstack11lll1_opy_ (u"ࠬ࠴ࠧஈ"))[0]
            bstack11l11ll1_opy_ = major.isdigit() and int(major) > min_version
        if not bstack11l11ll1_opy_:
            logger.warning(bstack11lll1_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡩࡵࡩࡦࡺࡥࡳࠢࡷ࡬ࡦࡴࠠࡼࡿ࠱ࠤࡈࡻࡲࡳࡧࡱࡸࠥࡼࡥࡳࡵ࡬ࡳࡳࡀࠠࡼࡿࠥஉ").format(min_version, browser_version))
        if a11y.is_enabled_platform(CONFIG, bstack11l111lll1_opy_) and bstack1l1ll1l11_opy_ and bstack11l11ll1_opy_ and a11y.is_platform_supported(bstack1l1lll1ll1_opy_, options=None, config=CONFIG):
            bstack1l1l111111_opy_ = True
            import browserstack_sdk
            browserstack_sdk.CONFIG[bstack11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ஊ")] = True
            bstack1l1lll1ll1_opy_[bstack11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ஋")] = True
            if CONFIG.get(bstack11lll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ஌")):
                bstack1l1lll1ll1_opy_[bstack11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ஍")] = CONFIG[bstack11lll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭எ")]
            import json as _json
            bstack1ll1l11lll_opy_ = os.getenv(bstack11lll1_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪஏ"))
            bstack1ll1l1111l_opy_ = bstack1l1lll1ll1_opy_.get(bstack11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷ࠳ࡧࡵࡵࡪࡗࡳࡰ࡫࡮ࠨஐ"))
            if not bstack1ll1l11lll_opy_ and bstack1ll1l1111l_opy_:
                os.environ[bstack11lll1_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ஑")] = bstack1ll1l1111l_opy_
                bstack1ll1l11lll_opy_ = bstack1ll1l1111l_opy_
            if bstack1ll1l11lll_opy_:
                bstack1l1lll1ll1_opy_[bstack11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹ࠮ࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪஒ")] = bstack1ll1l11lll_opy_
            bstack1lll11l1l1_opy_ = _json.loads(os.getenv(bstack11lll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪஓ"), bstack11lll1_opy_ (u"ࠪࡿࢂ࠭ஔ"))).get(bstack11lll1_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬக"))
            if bstack1lll11l1l1_opy_:
                bstack1l1lll1ll1_opy_[bstack11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶ࠲ࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ஖")] = bstack1lll11l1l1_opy_
            bstack1l1lll1ll1_opy_.pop(bstack11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ஗"), None)
            bstack1l1lll1ll1_opy_.pop(bstack11lll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ஘"), None)
            bstack1l1lll1ll1_opy_.pop(bstack11lll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨங"), None)
            logger.debug(bstack11lll1_opy_ (u"ࠤࡄ࠵࠶ࡿࠠࡦࡰࡤࡦࡱ࡫ࡤࠡࡨࡲࡶࠥࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࠬࢀࢃࠠࡼࡿࠬࠦச").format(
                bstack11l111l1l1_opy_, browser_version))
    except Exception as e:
        bstack1l1l111111_opy_ = False
        logger.debug(bstack11lll1_opy_ (u"ࠥࡅ࠶࠷ࡹࠡࡦࡨࡸࡪࡩࡴࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽࠣ஛").format(str(e)))
    logger.debug(CONFIG_FILE_CONTENT.format(str(bstack1l1lll1ll1_opy_)))
    if CONFIG.get(bstack11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨஜ")):
      update_caps_for_local(bstack1l1lll1ll1_opy_)
    if bstack11lll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ஝") in CONFIG and bstack11lll1_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫஞ") in CONFIG[bstack11lll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪட")][bstack11l111lll1_opy_]:
      SESSION_NAME = CONFIG[bstack11lll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ஠")][bstack11l111lll1_opy_][bstack11lll1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ஡")]
    import urllib
    import json
    if bstack11lll1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ஢") in CONFIG and str(CONFIG[bstack11lll1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨண")]).lower() != bstack11lll1_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫத"):
        bstack11111lll1l_opy_ = get_turboscale_playwright_url()
        cdpUrl = bstack11111lll1l_opy_ + urllib.parse.quote(json.dumps(bstack1l1lll1ll1_opy_))
    else:
        cdpUrl = bstack11lll1_opy_ (u"࠭ࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠨ஥") + urllib.parse.quote(json.dumps(bstack1l1lll1ll1_opy_))
    try:
        from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
        PlaywrightDriverWrapperDirect.setup_dispatch_capture()
    except Exception as exc:
        logger.debug(bstack11lll1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠤࡨࡧࡰࡵࡷࡵࡩࠥ࡬࡯ࡳࠢࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࡀࠠࠦࡵࠥ஦"), exc)
    if bstack1l1l111111_opy_:
        browser = self.connect_over_cdp(cdpUrl)
    else:
        browser = bstack1ll11l1ll_opy_(self, cdpUrl)
    try:
        from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
        wrapper = PlaywrightDriverWrapperDirect(browser, page=None, capabilities=bstack1l1lll1ll1_opy_, config=CONFIG)
        threading.current_thread().bstackSessionDriver = wrapper
        logger.debug(bstack11lll1_opy_ (u"ࠣࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡉࡸࡩࡷࡧࡵ࡛ࡷࡧࡰࡱࡧࡵࡈ࡮ࡸࡥࡤࡶࠣࡷࡪࡺࡵࡱࠢࡦࡳࡲࡶ࡬ࡦࡶࡨࠤ࡫ࡵࡲࠡࡶ࡫ࡶࡪࡧࡤࠡࠧࡶࠦ஧"), threading.get_ident())
        threading.current_thread().bstackTestErrorMessages = []
        if bstack1l1l111111_opy_:
            threading.current_thread().a11yPlatform = True
            wrapper.bstackA11yShouldScan = True
        if wrapper.session_id and not wrapper._cbt_info_sent:
            PlaywrightDriverWrapperDirect._send_cbt_info_on_session()
        try:
            from playwright.sync_api import Browser as bstack1ll1ll1lll_opy_
            if not hasattr(bstack1ll1ll1lll_opy_, bstack11lll1_opy_ (u"ࠩࡢࡦࡸࡺࡡࡤ࡭ࡢࡲࡪࡽ࡟ࡱࡣࡪࡩࡤࡶࡡࡵࡥ࡫ࡩࡩ࠭ந")):
                _11ll1l11_opy_ = bstack1ll1ll1lll_opy_.new_page
                def _1ll1l1l1l_opy_(bstack1111l11lll_opy_, *bstack111111l1_opy_, **bstack1l1111l111_opy_):
                    if getattr(threading.current_thread(), bstack11lll1_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩன"), None):
                        try:
                            bstack1ll11lllll_opy_ = bstack1111l11lll_opy_.contexts[0] if bstack1111l11lll_opy_.contexts else None
                            if bstack1ll11lllll_opy_ and bstack1ll11lllll_opy_.pages:
                                page = None
                                for _111l11lll_opy_ in bstack1ll11lllll_opy_.pages:
                                    if bstack11lll1_opy_ (u"ࠦࡦࡨ࡯ࡶࡶ࠽ࡦࡱࡧ࡮࡬ࠤப") in _111l11lll_opy_.url:
                                        page = _111l11lll_opy_
                                        logger.debug(bstack11lll1_opy_ (u"ࠧࡇ࠱࠲ࡻ࠽ࠤࡷ࡫ࡵࡴ࡫ࡱ࡫ࠥࡧࡢࡰࡷࡷ࠾ࡧࡲࡡ࡯࡭ࠣࡴࡦ࡭ࡥࠡࡨࡵࡳࡲࠦࡤࡦࡨࡤࡹࡱࡺࠠࡤࡱࡱࡸࡪࡾࡴࠣ஫"))
                                        break
                                if page is None:
                                    page = bstack1ll11lllll_opy_.new_page(*bstack111111l1_opy_, **bstack1l1111l111_opy_)
                                    logger.debug(bstack11lll1_opy_ (u"ࠨࡁ࠲࠳ࡼ࠾ࠥࡴ࡯ࠡࡤ࡯ࡥࡳࡱࠠࡱࡣࡪࡩࠥ࡬࡯ࡶࡰࡧ࠰ࠥࡩࡲࡦࡣࡷࡩࡩࠦ࡮ࡦࡹࠣࡴࡦ࡭ࡥࠡ࡫ࡱࠤࡩ࡫ࡦࡢࡷ࡯ࡸࠥࡩ࡯࡯ࡶࡨࡼࡹࠨ஬"))
                            elif bstack1ll11lllll_opy_:
                                page = bstack1ll11lllll_opy_.new_page(*bstack111111l1_opy_, **bstack1l1111l111_opy_)
                                logger.debug(bstack11lll1_opy_ (u"ࠢࡂ࠳࠴ࡽ࠿ࠦࡣࡳࡧࡤࡸࡪࡪࠠ࡯ࡧࡺࠤࡵࡧࡧࡦࠢ࡬ࡲࠥࡪࡥࡧࡣࡸࡰࡹࠦࡣࡰࡰࡷࡩࡽࡺࠢ஭"))
                            else:
                                page = _11ll1l11_opy_(bstack1111l11lll_opy_, *bstack111111l1_opy_, **bstack1l1111l111_opy_)
                                logger.debug(bstack11lll1_opy_ (u"ࠣࡃ࠴࠵ࡾࡀࠠ࡯ࡱࠣࡨࡪ࡬ࡡࡶ࡮ࡷࠤࡨࡵ࡮ࡵࡧࡻࡸ࠱ࠦࡦࡢ࡮࡯࡭ࡳ࡭ࠠࡣࡣࡦ࡯ࠥࡺ࡯ࠡࡰࡨࡻࡤࡶࡡࡨࡧࠫ࠭ࠧம"))
                        except Exception as bstack111lllll11_opy_:
                            logger.debug(bstack11lll1_opy_ (u"ࠤࡄ࠵࠶ࡿ࠺ࠡࡦࡨࡪࡦࡻ࡬ࡵࠢࡦࡳࡳࡺࡥࡹࡶࠣࡴࡦ࡭ࡥࠡࡴࡨࡹࡸ࡫ࠠࡧࡣ࡬ࡰࡪࡪࠠࠩࠧࡶ࠭࠱ࠦࡦࡢ࡮࡯࡭ࡳ࡭ࠠࡣࡣࡦ࡯ࠧய"), bstack111lllll11_opy_)
                            page = _11ll1l11_opy_(bstack1111l11lll_opy_, *bstack111111l1_opy_, **bstack1l1111l111_opy_)
                    else:
                        page = _11ll1l11_opy_(bstack1111l11lll_opy_, *bstack111111l1_opy_, **bstack1l1111l111_opy_)
                    try:
                        _w = getattr(threading.current_thread(), bstack11lll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩர"), None)
                        if _w and hasattr(_w, bstack11lll1_opy_ (u"ࠫࡺࡶࡤࡢࡶࡨࡣࡵࡧࡧࡦࠩற")):
                            _w.update_page(page)
                        if _w and not _w.session_id:
                            try:
                                import json as _json
                                result = page.evaluate(
                                    bstack11lll1_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨல"), bstack11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠥࢁࠬள"))
                                if isinstance(result, str):
                                    result = _json.loads(result)
                                if isinstance(result, dict):
                                    sid = result.get(bstack11lll1_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪழ")) or result.get(bstack11lll1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠬவ")) or result.get(bstack11lll1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡌࡨࠬஶ"))
                                    if sid:
                                        import threading as _11l111ll1_opy_
                                        from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
                                        with PlaywrightDriverWrapperDirect._session_ids_lock:
                                            PlaywrightDriverWrapperDirect._session_ids[_11l111ll1_opy_.get_ident()] = sid
                                        logger.debug(bstack11lll1_opy_ (u"ࠥࡇࡦࡶࡴࡶࡴࡨࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠢࡹ࡭ࡦࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࠧࡶࠦஷ"), sid)
                                        PlaywrightDriverWrapperDirect._send_cbt_info_on_session()
                                    else:
                                        logger.debug(bstack11lll1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠥ࡭ࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡆࡨࡸࡦ࡯࡬ࡴࠢࡵࡩࡹࡻࡲ࡯ࡧࡧࠤࡳࡵࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧ࠾ࠥࠫࡳࠣஸ"), result)
                                else:
                                    logger.debug(bstack11lll1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࠦࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠣࡶࡪࡹࡵ࡭ࡶ࠽ࠤࠪࡹࠢஹ"), result)
                            except Exception as _1ll11l11l1_opy_:
                                logger.debug(bstack11lll1_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡼࡩࡢࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࠪࡹࠢ஺"), _1ll11l11l1_opy_)
                        if (getattr(threading.current_thread(), bstack11lll1_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭஻"), None)
                                and not getattr(threading.current_thread(), bstack11lll1_opy_ (u"ࠨࡣ࠴࠵ࡾࡥࡳࡵࡣࡵࡸࡪࡪࠧ஼"), False)):
                            threading.current_thread().a11y_started = True
                            try:
                                from bstack_utils import accessibility as _1l1111ll1l_opy_
                                bstack1lll1l11l_opy_ = getattr(threading.current_thread(), bstack11lll1_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭஽"), True)
                                _1l1111ll1l_opy_.start_test_capture(_w, bstack1lll1l11l_opy_)
                            except Exception:
                                logger.debug(bstack11lll1_opy_ (u"ࠥࡈࡪ࡬ࡥࡳࡴࡨࡨࠥࡇ࠱࠲ࡻࠣࡷࡹࡧࡲࡵࡡࡷࡩࡸࡺ࡟ࡤࡣࡳࡸࡺࡸࡥࠡࡨࡤ࡭ࡱ࡫ࡤࠣா"))
                    except Exception as exc:
                        logger.debug(bstack11lll1_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡶࡲࡧࡥࡹ࡫ࠠࡱࡣࡪࡩࠥ࡯࡮ࠡࡹࡵࡥࡵࡶࡥࡳ࠼ࠣࠩࡸࠨி"), exc)
                    return page
                bstack1ll1ll1lll_opy_.new_page = _1ll1l1l1l_opy_
                bstack1ll1ll1lll_opy_._bstack_new_page_patched = True
        except Exception as exc:
            logger.debug(bstack11lll1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡸࡨ࡮ࠠࡔࡻࡱࡧࡇࡸ࡯ࡸࡵࡨࡶ࠳ࡴࡥࡸࡡࡳࡥ࡬࡫ࠠࡧࡱࡵࠤࡵࡧࡧࡦࠢࡦࡥࡵࡺࡵࡳࡧ࠽ࠤࠪࡹࠢீ"), exc)
        try:
            from playwright.sync_api import Page as bstack1lll11ll_opy_, Browser as _1l1l1l11ll_opy_
            if not hasattr(bstack1lll11ll_opy_, bstack11lll1_opy_ (u"࠭࡟ࡣࡵࡷࡥࡨࡱ࡟ࡱࡣࡪࡩࡤࡩ࡬ࡰࡵࡨࡣࡵࡧࡴࡤࡪࡨࡨࠬு")):
                _11l1111111_opy_ = bstack1lll11ll_opy_.close
                def _1l1l1l111l_opy_(bstack11111111_opy_, *bstack1ll1llllll_opy_, _bstack_sdk_close=False, **bstack11lll111ll_opy_):
                    if not _bstack_sdk_close:
                        logger.debug(bstack11lll1_opy_ (u"ࠢࡅࡧࡩࡩࡷࡸࡥࡥࠢࡳࡥ࡬࡫࠮ࡤ࡮ࡲࡷࡪ࠮ࠩࠡ⠖ࠣࡻ࡮ࡲ࡬ࠡࡥ࡯ࡳࡸ࡫ࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦூ"))
                        threading.current_thread().bstack_deferred_page_close = True
                        threading.current_thread().bstack_deferred_page_ref = bstack11111111_opy_
                        return
                    return _11l1111111_opy_(bstack11111111_opy_, *bstack1ll1llllll_opy_, **bstack11lll111ll_opy_)
                bstack1lll11ll_opy_.close = _1l1l1l111l_opy_
                bstack1lll11ll_opy_._bstack_page_close_patched = True
            if not hasattr(_1l1l1l11ll_opy_, bstack11lll1_opy_ (u"ࠨࡡࡥࡷࡹࡧࡣ࡬ࡡࡥࡶࡴࡽࡳࡦࡴࡢࡧࡱࡵࡳࡦࡡࡳࡥࡹࡩࡨࡦࡦࠪ௃")):
                _1l1ll111ll_opy_ = _1l1l1l11ll_opy_.close
                def _1111ll111_opy_(bstack1111l11lll_opy_, *bstack1lll11ll1l_opy_, _bstack_sdk_close=False, **bstack11l1ll1lll_opy_):
                    if not _bstack_sdk_close:
                        logger.debug(bstack11lll1_opy_ (u"ࠤࡇࡩ࡫࡫ࡲࡳࡧࡧࠤࡧࡸ࡯ࡸࡵࡨࡶ࠳ࡩ࡬ࡰࡵࡨࠬ࠮ࠦ⠔ࠡࡹ࡬ࡰࡱࠦࡣ࡭ࡱࡶࡩࠥ࡯࡮ࠡࡣࡩࡸࡪࡸ࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤ௄"))
                        threading.current_thread().bstack_deferred_browser_close = True
                        threading.current_thread().bstack_deferred_browser_ref = bstack1111l11lll_opy_
                        return
                    return _1l1ll111ll_opy_(bstack1111l11lll_opy_, *bstack1lll11ll1l_opy_, **bstack11l1ll1lll_opy_)
                _1l1l1l11ll_opy_.close = _1111ll111_opy_
                _1l1l1l11ll_opy_._bstack_browser_close_patched = True
            if not hasattr(bstack1lll11ll_opy_, bstack11lll1_opy_ (u"ࠪࡣࡧࡹࡴࡢࡥ࡮ࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡠࡲࡤࡸࡨ࡮ࡥࡥࠩ௅")):
                _11llll111_opy_ = bstack1lll11ll_opy_.screenshot
                def _1l1ll1ll1l_opy_(bstack11111111_opy_, *bstack1l1l11ll11_opy_, **bstack11l1l1ll1l_opy_):
                    result = _11llll111_opy_(bstack11111111_opy_, *bstack1l1l11ll11_opy_, **bstack11l1l1ll1l_opy_)
                    try:
                        from bstack_utils.testhub_handler import TestHubHandler
                        from bstack_utils.bstack1llll11l11_opy_ import bstack1ll1l1l1l1_opy_
                        if bstack1ll1l1l1l1_opy_.on():
                            import base64
                            if isinstance(result, bytes):
                                bstack11111ll1l1_opy_ = base64.b64encode(result).decode(bstack11lll1_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪெ"))
                            else:
                                bstack11111ll1l1_opy_ = str(result)
                            test_uuid = TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack1ll1l1l1l1_opy_.current_hook_uuid()
                            if test_uuid and bstack11111ll1l1_opy_:
                                TestHubHandler.bstack1l11lll11_opy_({
                                    bstack11lll1_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫே"): bstack11111ll1l1_opy_,
                                    bstack11lll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ை"): test_uuid
                                })
                                logger.debug(bstack11lll1_opy_ (u"ࠢࡔࡧࡱࡸࠥࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠦࡴࡰࠢࡒ࠵࠶ࡿࠠࡧࡱࡵࠤࡹ࡫ࡳࡵࠢࡾࢁࠧ௉").format(test_uuid))
                    except Exception as bstack1l1lllllll_opy_:
                        logger.debug(bstack11lll1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫࡮ࡥࠢࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠣࡸࡴࠦࡏ࠲࠳ࡼ࠾ࠥࢁࡽࠣொ").format(str(bstack1l1lllllll_opy_)))
                    return result
                bstack1lll11ll_opy_.screenshot = _1l1ll1ll1l_opy_
                bstack1lll11ll_opy_._bstack_screenshot_patched = True
        except Exception as exc:
            logger.debug(bstack11lll1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡥࠡࡦࡨࡪࡪࡸࡲࡦࡦࠣࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡤ࡮ࡲࡷࡪࠦࡨࡰࡱ࡮ࡷ࠿ࠦࠥࡴࠤோ"), exc)
        logger.debug(bstack11lll1_opy_ (u"ࠥࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࡄࡳ࡫ࡹࡩࡷ࡝ࡲࡢࡲࡳࡩࡷࡊࡩࡳࡧࡦࡸࠥࡹࡥࡵࡷࡳࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࠦࡦࡰࡴࠣࡸ࡭ࡸࡥࡢࡦࠣࡿࢂࠨௌ").format(threading.get_ident()))
    except Exception as e:
        logger.debug(bstack11lll1_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡻࡷࡧࡰࡱࡧࡵ࠾ࠥࢁࡽ்ࠣ").format(str(e)))
    return browser
  async def bstack1llll1l1_opy_(self, *args, **kwargs):
    global bstack1ll11l1ll_opy_, CONFIG, FRAMEWORK_NAME, __version__, BROWSERSTACK_AUTOMATION
    global PLATFORM_INDEX, PARALLELISE_VANILLA_PYTHON, PARALLELISE_THREADING_PYTHON, SESSION_NAME
    import urllib.parse as _111111l111_opy_
    import json
    ws_endpoint = args[0] if args else kwargs.get(bstack11lll1_opy_ (u"ࠬࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵࠩ௎"), kwargs.get(bstack11lll1_opy_ (u"࠭ࡷࡴࡡࡨࡲࡩࡶ࡯ࡪࡰࡷࠫ௏"), bstack11lll1_opy_ (u"ࠧࠨௐ")))
    bstack11lll1l1l_opy_ = (ws_endpoint
                 and bstack11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫ௑") in str(ws_endpoint)
                 and bstack11lll1_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨ௒") in str(ws_endpoint))
    bstack11ll11l1l1_opy_ = {}
    if bstack11lll1l1l_opy_:
        from bstack_utils.helper import bstack11l1111l1l_opy_
        bstack1111llllll_opy_ = bstack11l1111l1l_opy_()
        try:
            if bstack1111llllll_opy_:
                CONFIG[bstack11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ௓")] = str(FRAMEWORK_NAME) + str(__version__)
                bstack1l111ll1l_opy_ = os.environ.get(bstack11lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ௔"), bstack11lll1_opy_ (u"ࠬ࠭௕"))
                if bstack1l111ll1l_opy_:
                    CONFIG[bstack11lll1_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ௖")] = bstack1l111ll1l_opy_
                CONFIG[bstack11lll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩௗ")] = TestHubUtils.bstack11lll11lll_opy_(CONFIG, FRAMEWORK_NAME)
                bstack11l111lll1_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
                try:
                    if PARALLELISE_VANILLA_PYTHON is True:
                        bstack11l111lll1_opy_ = int(multiprocessing.current_process().name)
                    elif PARALLELISE_THREADING_PYTHON is True:
                        bstack11l111lll1_opy_ = int(threading.current_thread().name)
                except Exception:
                    bstack11l111lll1_opy_ = 0
                CONFIG[bstack11lll1_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢ௘")] = True
                bstack11ll11l1l1_opy_ = get_caps(CONFIG, bstack11l111lll1_opy_)
                if CONFIG.get(bstack11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭௙")):
                    update_caps_for_local(bstack11ll11l1l1_opy_)
                if bstack11lll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭௚") in CONFIG and bstack11lll1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ௛") in CONFIG[bstack11lll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ௜")][bstack11l111lll1_opy_]:
                    SESSION_NAME = CONFIG[bstack11lll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ௝")][bstack11l111lll1_opy_][bstack11lll1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ௞")]
                logger.debug(bstack11lll1_opy_ (u"ࠣࡅࡤࡷࡪࠦࡁ࠻ࠢࡕࡩࡵࡲࡡࡤࡧࡧࠤࡺࡹࡥࡳࠢࡦࡥࡵࡹࠠࡸ࡫ࡷ࡬ࠥࡿ࡭࡭ࠢࡦࡥࡵࡹ࠺ࠡࡽࢀࠦ௟").format(str(bstack11ll11l1l1_opy_)))
            else:
                bstack1ll1lll111_opy_ = str(ws_endpoint).split(bstack11lll1_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨ௠"))[1]
                bstack11ll11l1l1_opy_ = json.loads(_111111l111_opy_.unquote(bstack1ll1lll111_opy_))
                bstack11ll11l1l1_opy_ = bstack11ll11l1l1_opy_ or {}
                bstack1l111ll1l_opy_ = os.environ.get(bstack11lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ௡"), bstack11lll1_opy_ (u"ࠫࠬ௢"))
                bstack1ll11l1l11_opy_ = TestHubUtils.bstack11lll11lll_opy_(CONFIG, FRAMEWORK_NAME)
                bstack11ll11l1l1_opy_[bstack11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭௣")] = str(FRAMEWORK_NAME) + str(__version__)
                bstack11ll11l1l1_opy_[bstack11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ௤")] = BROWSERSTACK_AUTOMATION
                if bstack1l111ll1l_opy_:
                    bstack11ll11l1l1_opy_[bstack11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ௥")] = bstack1l111ll1l_opy_
                bstack11ll11l1l1_opy_[bstack11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩ௦")] = bstack1ll11l1l11_opy_
                logger.debug(bstack11lll1_opy_ (u"ࠤࡆࡥࡸ࡫ࠠࡅ࠼ࠣࡑࡪࡸࡧࡦࡦࠣࡗࡉࡑࠠࡵࡧ࡯ࡩࡲ࡫ࡴࡳࡻࠣ࡭ࡳࡺ࡯ࠡࡷࡶࡩࡷࠦࡣࡢࡲࡶࠦ௧"))
            ws_url = str(ws_endpoint).split(bstack11lll1_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩ௨"))[0]
            ws_endpoint = ws_url + bstack11lll1_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ௩") + _111111l111_opy_.quote(json.dumps(bstack11ll11l1l1_opy_))
            if args:
                args = (ws_endpoint,) + args[1:]
            else:
                if bstack11lll1_opy_ (u"ࠬࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵࠩ௪") in kwargs:
                    kwargs[bstack11lll1_opy_ (u"࠭ࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶࠪ௫")] = ws_endpoint
                else:
                    kwargs[bstack11lll1_opy_ (u"ࠧࡸࡵࡢࡩࡳࡪࡰࡰ࡫ࡱࡸࠬ௬")] = ws_endpoint
            logger.debug(bstack11lll1_opy_ (u"ࠣࡎࡨ࡫ࡦࡩࡹࠡࡥࡲࡲࡳ࡫ࡣࡵࠢࡘࡖࡑࠦࡵࡱࡦࡤࡸࡪࡪࠠࡸ࡫ࡷ࡬ࠥࢁࡽࠡࡥࡤࡴࡸࠨ௭").format(bstack11lll1_opy_ (u"ࠤࡼࡱࡱࠨ௮") if bstack1111llllll_opy_ else bstack11lll1_opy_ (u"ࠥࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࠨ௯")))
        except Exception as e:
            logger.debug(bstack11lll1_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡧࡵ࡫ࡪࠦࡣࡢࡲࡶࠤ࡮ࡴࡴࡰࠢࡦࡳࡳࡴࡥࡤࡶ࡙ࠣࡗࡒ࠺ࠡࡽࢀࠦ௰").format(str(e)))
        try:
            from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
            PlaywrightDriverWrapperDirect.setup_dispatch_capture()
        except Exception as exc:
            logger.debug(bstack11lll1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠࡥ࡫ࡶࡴࡦࡺࡣࡩࠢࡦࡥࡵࡺࡵࡳࡧࠣ࡭ࡳࠦ࡭ࡰࡦࡢࡧࡴࡴ࡮ࡦࡥࡷ࠾ࠥࠫࡳࠣ௱"), exc)
    browser = await bstack1ll11l1ll_opy_(self, *args, **kwargs)
    if bstack11lll1l1l_opy_:
        try:
            from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
            wrapper = PlaywrightDriverWrapperDirect(browser, page=None, capabilities=bstack11ll11l1l1_opy_, config=CONFIG)
            threading.current_thread().bstackSessionDriver = wrapper
            logger.debug(bstack11lll1_opy_ (u"ࠨࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡇࡶ࡮ࡼࡥࡳ࡙ࡵࡥࡵࡶࡥࡳࡆ࡬ࡶࡪࡩࡴࠡࡵࡨࡸࡺࡶࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࠢࡩࡳࡷࠦࡴࡩࡴࡨࡥࡩࠦࠥࡴࠤ௲"), threading.get_ident())
            threading.current_thread().bstackTestErrorMessages = []
            if wrapper.session_id and not wrapper._cbt_info_sent:
                PlaywrightDriverWrapperDirect._send_cbt_info_on_session()
            try:
                from playwright.sync_api import Browser as bstack1ll1ll1lll_opy_
                if not hasattr(bstack1ll1ll1lll_opy_, bstack11lll1_opy_ (u"ࠧࡠࡤࡶࡸࡦࡩ࡫ࡠࡰࡨࡻࡤࡶࡡࡨࡧࡢࡴࡦࡺࡣࡩࡧࡧࠫ௳")):
                    _11ll1l11_opy_ = bstack1ll1ll1lll_opy_.new_page
                    def _1ll1l1l1l_opy_(bstack1111l11lll_opy_, *bstack111111l1_opy_, **bstack1l1111l111_opy_):
                        page = _11ll1l11_opy_(bstack1111l11lll_opy_, *bstack111111l1_opy_, **bstack1l1111l111_opy_)
                        try:
                            _w = getattr(threading.current_thread(), bstack11lll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ௴"), None)
                            if _w and hasattr(_w, bstack11lll1_opy_ (u"ࠩࡸࡴࡩࡧࡴࡦࡡࡳࡥ࡬࡫ࠧ௵")):
                                _w.update_page(page)
                        except Exception as exc:
                            logger.debug(bstack11lll1_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡵࡱࡦࡤࡸࡪࠦࡰࡢࡩࡨࠤ࡮ࡴࠠࡸࡴࡤࡴࡵ࡫ࡲࠡࠪࡰࡳࡩࡥࡣࡰࡰࡱࡩࡨࡺࠩ࠻ࠢࠨࡷࠧ௶"), exc)
                        return page
                    bstack1ll1ll1lll_opy_.new_page = _1ll1l1l1l_opy_
                    bstack1ll1ll1lll_opy_._bstack_new_page_patched = True
            except Exception as exc:
                logger.debug(bstack11lll1_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡷࡧ࡭ࠦࡓࡺࡰࡦࡆࡷࡵࡷࡴࡧࡵ࠲ࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠦࡩ࡯ࠢࡰࡳࡩࡥࡣࡰࡰࡱࡩࡨࡺ࠺ࠡࠧࡶࠦ௷"), exc)
            try:
                from playwright.sync_api import Page as bstack1lll11ll_opy_, Browser as _1l1l1l11ll_opy_
                if not hasattr(bstack1lll11ll_opy_, bstack11lll1_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥࡰࡢࡩࡨࡣࡨࡲ࡯ࡴࡧࡢࡴࡦࡺࡣࡩࡧࡧࠫ௸")):
                    _11l1111111_opy_ = bstack1lll11ll_opy_.close
                    def _1l1l1l111l_opy_(bstack11111111_opy_, *bstack1ll1llllll_opy_, _bstack_sdk_close=False, **bstack11lll111ll_opy_):
                        if not _bstack_sdk_close:
                            logger.debug(bstack11lll1_opy_ (u"ࠨࡄࡦࡨࡨࡶࡷ࡫ࡤࠡࡲࡤ࡫ࡪ࠴ࡣ࡭ࡱࡶࡩ࠭࠯ࠠ⠕ࠢࡺ࡭ࡱࡲࠠࡤ࡮ࡲࡷࡪࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥ௹"))
                            threading.current_thread().bstack_deferred_page_close = True
                            threading.current_thread().bstack_deferred_page_ref = bstack11111111_opy_
                            return
                        return _11l1111111_opy_(bstack11111111_opy_, *bstack1ll1llllll_opy_, **bstack11lll111ll_opy_)
                    bstack1lll11ll_opy_.close = _1l1l1l111l_opy_
                    bstack1lll11ll_opy_._bstack_page_close_patched = True
                if not hasattr(_1l1l1l11ll_opy_, bstack11lll1_opy_ (u"ࠧࡠࡤࡶࡸࡦࡩ࡫ࡠࡤࡵࡳࡼࡹࡥࡳࡡࡦࡰࡴࡹࡥࡠࡲࡤࡸࡨ࡮ࡥࡥࠩ௺")):
                    _1l1ll111ll_opy_ = _1l1l1l11ll_opy_.close
                    def _1111ll111_opy_(bstack1111l11lll_opy_, *bstack1lll11ll1l_opy_, _bstack_sdk_close=False, **bstack11l1ll1lll_opy_):
                        if not _bstack_sdk_close:
                            logger.debug(bstack11lll1_opy_ (u"ࠣࡆࡨࡪࡪࡸࡲࡦࡦࠣࡦࡷࡵࡷࡴࡧࡵ࠲ࡨࡲ࡯ࡴࡧࠫ࠭ࠥ⠚ࠠࡸ࡫࡯ࡰࠥࡩ࡬ࡰࡵࡨࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣ௻"))
                            threading.current_thread().bstack_deferred_browser_close = True
                            threading.current_thread().bstack_deferred_browser_ref = bstack1111l11lll_opy_
                            return
                        return _1l1ll111ll_opy_(bstack1111l11lll_opy_, *bstack1lll11ll1l_opy_, **bstack11l1ll1lll_opy_)
                    _1l1l1l11ll_opy_.close = _1111ll111_opy_
                    _1l1l1l11ll_opy_._bstack_browser_close_patched = True
                if not hasattr(bstack1lll11ll_opy_, bstack11lll1_opy_ (u"ࠩࡢࡦࡸࡺࡡࡤ࡭ࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺ࡟ࡱࡣࡷࡧ࡭࡫ࡤࠨ௼")):
                    _11llll111_opy_ = bstack1lll11ll_opy_.screenshot
                    def _1l1ll1ll1l_opy_(bstack11111111_opy_, *bstack1l1l11ll11_opy_, **bstack11l1l1ll1l_opy_):
                        result = _11llll111_opy_(bstack11111111_opy_, *bstack1l1l11ll11_opy_, **bstack11l1l1ll1l_opy_)
                        try:
                            from bstack_utils.testhub_handler import TestHubHandler
                            from bstack_utils.bstack1llll11l11_opy_ import bstack1ll1l1l1l1_opy_
                            if bstack1ll1l1l1l1_opy_.on():
                                import base64
                                if isinstance(result, bytes):
                                    bstack11111ll1l1_opy_ = base64.b64encode(result).decode(bstack11lll1_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ௽"))
                                else:
                                    bstack11111ll1l1_opy_ = str(result)
                                test_uuid = TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack1ll1l1l1l1_opy_.current_hook_uuid()
                                if test_uuid and bstack11111ll1l1_opy_:
                                    TestHubHandler.bstack1l11lll11_opy_({
                                        bstack11lll1_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪ௾"): bstack11111ll1l1_opy_,
                                        bstack11lll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ௿"): test_uuid
                                    })
                        except Exception as bstack1l1lllllll_opy_:
                            logger.debug(bstack11lll1_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡳࡪࠠࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠡࡶࡲࠤࡔ࠷࠱ࡺࠢࠫࡱࡴࡪ࡟ࡤࡱࡱࡲࡪࡩࡴࠪ࠼ࠣࠩࡸࠨఀ"), bstack1l1lllllll_opy_)
                        return result
                    bstack1lll11ll_opy_.screenshot = _1l1ll1ll1l_opy_
                    bstack1lll11ll_opy_._bstack_screenshot_patched = True
            except Exception as exc:
                logger.debug(bstack11lll1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡧࡴࡴࡦࡪࡩࡸࡶࡪࠦࡤࡦࡨࡨࡶࡷ࡫ࡤࠡࡥ࡯ࡳࡸ࡫ࠠࡩࡱࡲ࡯ࡸࠦࡩ࡯ࠢࡰࡳࡩࡥࡣࡰࡰࡱࡩࡨࡺ࠺ࠡࠧࡶࠦఁ"), exc)
            logger.debug(bstack11lll1_opy_ (u"ࠣࡎࡨ࡫ࡦࡩࡹࠡࡥࡲࡲࡳ࡫ࡣࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡸࡷࡧࡣ࡬࡫ࡱ࡫ࠥࡹࡥࡵࡷࡳࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࠦࡦࡰࡴࠣࡸ࡭ࡸࡥࡢࡦࠣࡿࢂࠨం").format(threading.get_ident()))
        except Exception as e:
            logger.debug(bstack11lll1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࡷࡳࠤࡱ࡫ࡧࡢࡥࡼࠤࡨࡵ࡮࡯ࡧࡦࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡴࡳࡣࡦ࡯࡮ࡴࡧ࠻ࠢࡾࢁࠧః").format(str(e)))
    return browser
except Exception as e:
    pass
def patch_playwright():
    global SELENIUM_OR_PLAYWRIGHT_INSTALLED
    global FRAMEWORK_NAME
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack11l1111l1l_opy_
        global bstack1ll11l1ll_opy_
        if not bstack1ll11l1ll_opy_:
            bstack1ll11l1ll_opy_ = BrowserType.connect
        BrowserType.connect = bstack1llll1l1_opy_
        if bstack11l1111l1l_opy_():
            BrowserType.launch = bstack1l11ll11l1_opy_
            SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
        try:
            from playwright.sync_api._context_manager import PlaywrightContextManager
            if not hasattr(PlaywrightContextManager, bstack11lll1_opy_ (u"ࠪࡣࡧࡹࡴࡢࡥ࡮ࡣࡪࡴࡴࡦࡴࡢࡴࡦࡺࡣࡩࡧࡧࠫఄ")):
                _1l11ll11ll_opy_ = PlaywrightContextManager.__enter__
                def _1111llll_opy_(bstack111ll1l111_opy_):
                    pw = _1l11ll11ll_opy_(bstack111ll1l111_opy_)
                    _1l111111_opy_ = pw.stop
                    _11l1l1ll_opy_ = threading.current_thread()
                    _11l1l1ll_opy_.bstack_deferred_pw_ref = pw
                    _11l1l1ll_opy_.bstack_deferred_pw_stop_fn = _1l111111_opy_
                    def _1l11111lll_opy_(*args, _bstack_sdk_close=False, **kwargs):
                        if not _bstack_sdk_close:
                            logger.debug(bstack11lll1_opy_ (u"ࠦࡉ࡫ࡦࡦࡴࡵࡩࡩࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠱ࡷࡹࡵࡰࠩࠫࠣ⠘ࠥࡽࡩ࡭࡮ࠣࡷࡹࡵࡰࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧఅ"))
                            threading.current_thread().bstack_deferred_pw_stop = True
                            return
                        return _1l111111_opy_()
                    pw.stop = _1l11111lll_opy_
                    return pw
                PlaywrightContextManager.__enter__ = _1111llll_opy_
                PlaywrightContextManager._bstack_enter_patched = True
        except Exception as e:
            logger.debug(bstack11lll1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡸࡨ࡮ࠠࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡇࡴࡴࡴࡦࡺࡷࡑࡦࡴࡡࡨࡧࡵ࠲ࡤࡥࡥ࡯ࡶࡨࡶࡤࡥ࠺ࠡࠧࡶࠦఆ"), e)
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1ll1l11ll_opy_
      SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
    except Exception as e:
      pass
def playwright_set_session_name(context, bstack11l1ll1l1l_opy_):
  try:
    if getattr(context, bstack11lll1_opy_ (u"࠭ࡰࡢࡩࡨࠫఇ"), None):
      context.page.evaluate(bstack11lll1_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣఈ"), bstack11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬఉ")+ json.dumps(bstack11l1ll1l1l_opy_) + bstack11lll1_opy_ (u"ࠤࢀࢁࠧఊ"))
  except Exception as e:
    logger.debug(bstack11lll1_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽ࠻ࠢࡾࢁࠧఋ").format(str(e), traceback.format_exc()))
def playwright_annotate(context, message, level):
  try:
    if getattr(context, bstack11lll1_opy_ (u"ࠫࡵࡧࡧࡦࠩఌ"), None):
      context.page.evaluate(bstack11lll1_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨ఍"), bstack11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫఎ") + json.dumps(message) + bstack11lll1_opy_ (u"ࠧ࠭ࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠪఏ") + json.dumps(level) + bstack11lll1_opy_ (u"ࠨࡿࢀࠫఐ"))
  except Exception as e:
    logger.debug(bstack11lll1_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠢࡾࢁ࠿ࠦࡻࡾࠤ఑").format(str(e), traceback.format_exc()))
@measure(event_name=EVENTS.bstack1111l1l11l_opy_, stage=STAGE.bstack1lllllll11_opy_, bstack1l11ll11l_opy_=SESSION_NAME)
def bstack1lllll111_opy_(self, url):
  global bstack11lll1ll1_opy_
  try:
    bstack11lll1l1_opy_(url)
  except Exception as err:
    logger.debug(bstack111111llll_opy_.format(str(err)))
  try:
    bstack11lll1ll1_opy_(self, url)
  except Exception as e:
    try:
      parsed_error = str(e)
      if any(err_msg in parsed_error for err_msg in bstack1111l1l11_opy_):
        bstack11lll1l1_opy_(url, True)
    except Exception as err:
      logger.debug(bstack111111llll_opy_.format(str(err)))
    raise e
def bstack11l1l1llll_opy_(self):
  global bstack11l11l111l_opy_
  bstack11l11l111l_opy_ = self
  return
def bstack1ll11l11ll_opy_(self):
  global bstack1l1l111lll_opy_
  bstack1l1l111lll_opy_ = self
  return
def bstack11llll1l1_opy_(test_name, bstack1l11lll1l_opy_):
  global CONFIG
  if percy.bstack1l1l111l1_opy_() == bstack11lll1_opy_ (u"ࠥࡸࡷࡻࡥࠣఒ"):
    bstack1l11111l1_opy_ = os.path.relpath(bstack1l11lll1l_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack1l11111l1_opy_)
    bstack1l11ll11l_opy_ = suite_name + bstack11lll1_opy_ (u"ࠦ࠲ࠨఓ") + test_name
    threading.current_thread().percySessionName = bstack1l11ll11l_opy_
def bstack1l1llll1_opy_(self, test, *args, **kwargs):
  global bstack1111l1l1_opy_
  test_name = None
  bstack1l11lll1l_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1l11lll1l_opy_ = str(test.source)
  bstack11llll1l1_opy_(test_name, bstack1l11lll1l_opy_)
  bstack1111l1l1_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.bstack11l1llll1_opy_, stage=STAGE.bstack1lllllll11_opy_, bstack1l11ll11l_opy_=SESSION_NAME)
def bstack1l111lllll_opy_(driver, bstack1l11ll11l_opy_):
  if not bstack1ll1l11l_opy_ and bstack1l11ll11l_opy_:
      bstack11l1ll111l_opy_ = {
          bstack11lll1_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬఔ"): bstack11lll1_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧక"),
          bstack11lll1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪఖ"): {
              bstack11lll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭గ"): bstack1l11ll11l_opy_
          }
      }
      bstack1l1ll11l_opy_ = bstack11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧఘ").format(json.dumps(bstack11l1ll111l_opy_))
      driver.execute_script(bstack1l1ll11l_opy_)
  if bstack1l1llll1l1_opy_:
      bstack11111l1ll1_opy_ = {
          bstack11lll1_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪఙ"): bstack11lll1_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭చ"),
          bstack11lll1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨఛ"): {
              bstack11lll1_opy_ (u"࠭ࡤࡢࡶࡤࠫజ"): bstack1l11ll11l_opy_ + bstack11lll1_opy_ (u"ࠧࠡࡲࡤࡷࡸ࡫ࡤࠢࠩఝ"),
              bstack11lll1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧఞ"): bstack11lll1_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧట")
          }
      }
      if bstack1l1llll1l1_opy_.status == bstack11lll1_opy_ (u"ࠪࡔࡆ࡙ࡓࠨఠ"):
          bstack11l1lll11l_opy_ = bstack11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩడ").format(json.dumps(bstack11111l1ll1_opy_))
          driver.execute_script(bstack11l1lll11l_opy_)
          bstack11111l11_opy_(driver, bstack11lll1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬఢ"))
      elif bstack1l1llll1l1_opy_.status == bstack11lll1_opy_ (u"࠭ࡆࡂࡋࡏࠫణ"):
          reason = bstack11lll1_opy_ (u"ࠢࠣత")
          bstack111l1l11_opy_ = bstack1l11ll11l_opy_ + bstack11lll1_opy_ (u"ࠨࠢࡩࡥ࡮ࡲࡥࡥࠩథ")
          if bstack1l1llll1l1_opy_.message:
              reason = str(bstack1l1llll1l1_opy_.message)
              bstack111l1l11_opy_ = bstack111l1l11_opy_ + bstack11lll1_opy_ (u"ࠩࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸ࠺ࠡࠩద") + reason
          bstack11111l1ll1_opy_[bstack11lll1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ధ")] = {
              bstack11lll1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪన"): bstack11lll1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ఩"),
              bstack11lll1_opy_ (u"࠭ࡤࡢࡶࡤࠫప"): bstack111l1l11_opy_
          }
          bstack11l1lll11l_opy_ = bstack11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬఫ").format(json.dumps(bstack11111l1ll1_opy_))
          driver.execute_script(bstack11l1lll11l_opy_)
          bstack11111l11_opy_(driver, bstack11lll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨబ"), reason)
          bstack111lll11_opy_(reason, str(bstack1l1llll1l1_opy_), str(PLATFORM_INDEX), logger)
@measure(event_name=EVENTS.bstack1l1ll1l1l_opy_, stage=STAGE.bstack1lllllll11_opy_, bstack1l11ll11l_opy_=SESSION_NAME)
def bstack1l11l11111_opy_(driver, test):
  if percy.bstack1l1l111l1_opy_() == bstack11lll1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢభ") and percy.bstack1llllll11l_opy_() == bstack11lll1_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧమ"):
      bstack1l11111l11_opy_ = bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧయ"), None)
      bstack1ll1111l_opy_(driver, bstack1l11111l11_opy_, test)
  if (bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩర"), None) and
      bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬఱ"), None)) or (
      bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧల"), None) and
      bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪళ"), None)):
      logger.info(bstack11lll1_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠠࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡵࡻࡦࡿ࠮ࠡࠤఴ"))
      a11y.bstack111lll1l1_opy_(driver, name=test.name, path=test.source)
def bstack1l11l11ll_opy_(test, bstack1l11ll11l_opy_):
    try:
      bstack111ll1l1_opy_ = datetime.datetime.now()
      data = {}
      if test:
        data[bstack11lll1_opy_ (u"ࠪࡲࡦࡳࡥࠨవ")] = bstack1l11ll11l_opy_
      if bstack1l1llll1l1_opy_:
        if bstack1l1llll1l1_opy_.status == bstack11lll1_opy_ (u"ࠫࡕࡇࡓࡔࠩశ"):
          data[bstack11lll1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬష")] = bstack11lll1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭స")
        elif bstack1l1llll1l1_opy_.status == bstack11lll1_opy_ (u"ࠧࡇࡃࡌࡐࠬహ"):
          data[bstack11lll1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ఺")] = bstack11lll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ఻")
          if bstack1l1llll1l1_opy_.message:
            data[bstack11lll1_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰ఼ࠪ")] = str(bstack1l1llll1l1_opy_.message)
      user = CONFIG[bstack11lll1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ఽ")]
      key = CONFIG[bstack11lll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨా")]
      host = bstack11111l11ll_opy_(cli.config, [bstack11lll1_opy_ (u"ࠨࡡࡱ࡫ࡶࠦి"), bstack11lll1_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡦࠤీ"), bstack11lll1_opy_ (u"ࠣࡣࡳ࡭ࠧు")], bstack11lll1_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡵ࡯࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠥూ"))
      url = bstack11lll1_opy_ (u"ࠪࡿࢂ࠵ࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡵࡨࡷࡸ࡯࡯࡯ࡵ࠲ࡿࢂ࠴ࡪࡴࡱࡱࠫృ").format(host, bstack1l11l111l1_opy_)
      headers = {
        bstack11lll1_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪౄ"): bstack11lll1_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ౅"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers, auth=(user, key))
        cli.bstack11l111ll1l_opy_(bstack11lll1_opy_ (u"ࠨࡨࡵࡶࡳ࠾ࡺࡶࡤࡢࡶࡨࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡷࡹࡧࡴࡶࡵࠥె"), datetime.datetime.now() - bstack111ll1l1_opy_)
    except Exception as e:
      logger.error(bstack1l1l1l1l_opy_.format(str(e)))
def bstack1lll1l1l11_opy_(test, bstack1l11ll11l_opy_):
  global CONFIG
  global bstack1l1l111lll_opy_
  global bstack11l11l111l_opy_
  global bstack1l11l111l1_opy_
  global bstack1l1llll1l1_opy_
  global SESSION_NAME
  global bstack11ll1llll_opy_
  global bstack11l11ll1l_opy_
  global bstack11lll1llll_opy_
  global bstack111l11ll1l_opy_
  global bstack1ll111ll1l_opy_
  global bstack11llll1lll_opy_
  global bstack11ll11ll_opy_
  try:
    if not bstack1l11l111l1_opy_:
      with bstack11ll11ll_opy_:
        bstack11lllll1l_opy_ = os.path.join(os.path.expanduser(bstack11lll1_opy_ (u"ࠧࡿࠩే")), bstack11lll1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨై"), bstack11lll1_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫ౉"))
        if os.path.exists(bstack11lllll1l_opy_):
          with open(bstack11lllll1l_opy_, bstack11lll1_opy_ (u"ࠪࡶࠬొ")) as f:
            content = f.read().strip()
            if content:
              bstack1l11lll111_opy_ = json.loads(bstack11lll1_opy_ (u"ࠦࢀࠨో") + content + bstack11lll1_opy_ (u"ࠬࠨࡸࠣ࠼ࠣࠦࡾࠨࠧౌ") + bstack11lll1_opy_ (u"ࠨࡽ్ࠣ"))
              bstack1l11l111l1_opy_ = bstack1l11lll111_opy_.get(str(threading.get_ident()))
  except Exception as e:
    logger.debug(bstack11lll1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡲࡦࡣࡧ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡋࡇࡷࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬ౎") + str(e))
  if not is_robot_playwright_installed():
    if bstack1ll111ll1l_opy_:
      with bstack1111lll11l_opy_:
        bstack1lllll1l1_opy_ = bstack1ll111ll1l_opy_.copy()
      for driver in bstack1lllll1l1_opy_:
        if bstack1l11l111l1_opy_ == driver.session_id:
          if test:
            bstack1l11l11111_opy_(driver, test)
          bstack1l111lllll_opy_(driver, bstack1l11ll11l_opy_)
    elif bstack1l11l111l1_opy_:
      bstack1l11l11ll_opy_(test, bstack1l11ll11l_opy_)
    if bstack1l1l111lll_opy_:
      bstack11l11ll1l_opy_(bstack1l1l111lll_opy_)
    if bstack11l11l111l_opy_:
      bstack11lll1llll_opy_(bstack11l11l111l_opy_)
    if bstack1lll1lll_opy_:
      bstack111l11ll1l_opy_()
def bstack1ll11ll1_opy_(self, test, *args, **kwargs):
  bstack1l11ll11l_opy_ = None
  if test:
    bstack1l11ll11l_opy_ = str(test.name)
  bstack1lll1l1l11_opy_(test, bstack1l11ll11l_opy_)
  bstack11ll1llll_opy_(self, test, *args, **kwargs)
def bstack1ll1ll1111_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1llll1l11l_opy_
  global CONFIG
  global bstack1ll111ll1l_opy_
  global bstack1l11l111l1_opy_
  global bstack11ll11ll_opy_
  bstack111l111l1_opy_ = None
  try:
    if bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ౏"), None) or bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ౐"), None):
      try:
        if not bstack1l11l111l1_opy_:
          bstack11lllll1l_opy_ = os.path.join(os.path.expanduser(bstack11lll1_opy_ (u"ࠪࢂࠬ౑")), bstack11lll1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ౒"), bstack11lll1_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧ౓"))
          with bstack11ll11ll_opy_:
            if os.path.exists(bstack11lllll1l_opy_):
              with open(bstack11lllll1l_opy_, bstack11lll1_opy_ (u"࠭ࡲࠨ౔")) as f:
                content = f.read().strip()
                if content:
                  bstack1l11lll111_opy_ = json.loads(bstack11lll1_opy_ (u"ࠢࡼࠤౕ") + content + bstack11lll1_opy_ (u"ࠨࠤࡻࠦ࠿ࠦࠢࡺࠤౖࠪ") + bstack11lll1_opy_ (u"ࠤࢀࠦ౗"))
                  bstack1l11l111l1_opy_ = bstack1l11lll111_opy_.get(str(threading.get_ident()))
      except Exception as e:
        logger.debug(bstack11lll1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡵࡩࡦࡪࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡎࡊࡳࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢࡷࡩࡸࡺࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࠩౘ") + str(e))
      if bstack1ll111ll1l_opy_:
        with bstack1111lll11l_opy_:
          bstack1lllll1l1_opy_ = bstack1ll111ll1l_opy_.copy()
        for driver in bstack1lllll1l1_opy_:
          if bstack1l11l111l1_opy_ == driver.session_id:
            bstack111l111l1_opy_ = driver
    bstack1lll1l11l_opy_ = a11y.is_enabled_testcase(test.tags)
    if bstack111l111l1_opy_:
      threading.current_thread().isA11yTest = a11y.start_test_capture(bstack111l111l1_opy_, bstack1lll1l11l_opy_)
      threading.current_thread().isAppA11yTest = a11y.start_test_capture(bstack111l111l1_opy_, bstack1lll1l11l_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1lll1l11l_opy_
      threading.current_thread().isAppA11yTest = bstack1lll1l11l_opy_
  except:
    pass
  bstack1llll1l11l_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1l1llll1l1_opy_
  try:
    bstack1l1llll1l1_opy_ = self._test
  except:
    bstack1l1llll1l1_opy_ = self.test
def bstack1ll1llll11_opy_():
  global bstack1111111l_opy_
  try:
    if os.path.exists(bstack1111111l_opy_):
      os.remove(bstack1111111l_opy_)
  except Exception as e:
    logger.debug(bstack11lll1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧౙ") + str(e))
def bstack1lll1l1l1_opy_():
  global bstack1111111l_opy_
  bstack11l1l111_opy_ = {}
  lock_file = bstack1111111l_opy_ + bstack11lll1_opy_ (u"ࠬ࠴࡬ࡰࡥ࡮ࠫౚ")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack11lll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡰࡴࡩ࡫ࠡࡰࡲࡸࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥ࠭ࠢࡸࡷ࡮ࡴࡧࠡࡤࡤࡷ࡮ࡩࠠࡧ࡫࡯ࡩࠥࡵࡰࡦࡴࡤࡸ࡮ࡵ࡮ࡴࠩ౛"))
    try:
      if not os.path.isfile(bstack1111111l_opy_):
        with open(bstack1111111l_opy_, bstack11lll1_opy_ (u"ࠧࡸࠩ౜")) as f:
          json.dump({}, f)
      if os.path.exists(bstack1111111l_opy_):
        with open(bstack1111111l_opy_, bstack11lll1_opy_ (u"ࠨࡴࠪౝ")) as f:
          content = f.read().strip()
          if content:
            bstack11l1l111_opy_ = json.loads(content)
    except Exception as e:
      logger.debug(bstack11lll1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡷ࡫ࡡࡥ࡫ࡱ࡫ࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫ౞") + str(e))
    return bstack11l1l111_opy_
  try:
    os.makedirs(os.path.dirname(bstack1111111l_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      if not os.path.isfile(bstack1111111l_opy_):
        with open(bstack1111111l_opy_, bstack11lll1_opy_ (u"ࠪࡻࠬ౟")) as f:
          json.dump({}, f)
      if os.path.exists(bstack1111111l_opy_):
        with open(bstack1111111l_opy_, bstack11lll1_opy_ (u"ࠫࡷ࠭ౠ")) as f:
          content = f.read().strip()
          if content:
            bstack11l1l111_opy_ = json.loads(content)
  except Exception as e:
    logger.debug(bstack11lll1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡳࡧࡤࡨ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧౡ") + str(e))
  finally:
    return bstack11l1l111_opy_
def bstack1llll1lll_opy_(platform_index, item_index):
  global bstack1111111l_opy_
  lock_file = bstack1111111l_opy_ + bstack11lll1_opy_ (u"࠭࠮࡭ࡱࡦ࡯ࠬౢ")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack11lll1_opy_ (u"ࠧࡧ࡫࡯ࡩࡱࡵࡣ࡬ࠢࡱࡳࡹࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦ࠮ࠣࡹࡸ࡯࡮ࡨࠢࡥࡥࡸ࡯ࡣࠡࡨ࡬ࡰࡪࠦ࡯ࡱࡧࡵࡥࡹ࡯࡯࡯ࡵࠪౣ"))
    try:
      bstack11l1l111_opy_ = {}
      if os.path.exists(bstack1111111l_opy_):
        with open(bstack1111111l_opy_, bstack11lll1_opy_ (u"ࠨࡴࠪ౤")) as f:
          content = f.read().strip()
          if content:
            bstack11l1l111_opy_ = json.loads(content)
      bstack11l1l111_opy_[item_index] = platform_index
      with open(bstack1111111l_opy_, bstack11lll1_opy_ (u"ࠤࡺࠦ౥")) as outfile:
        json.dump(bstack11l1l111_opy_, outfile)
    except Exception as e:
      logger.debug(bstack11lll1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡽࡲࡪࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨ౦") + str(e))
    return
  try:
    os.makedirs(os.path.dirname(bstack1111111l_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      bstack11l1l111_opy_ = {}
      if os.path.exists(bstack1111111l_opy_):
        with open(bstack1111111l_opy_, bstack11lll1_opy_ (u"ࠫࡷ࠭౧")) as f:
          content = f.read().strip()
          if content:
            bstack11l1l111_opy_ = json.loads(content)
      bstack11l1l111_opy_[item_index] = platform_index
      with open(bstack1111111l_opy_, bstack11lll1_opy_ (u"ࠧࡽࠢ౨")) as outfile:
        json.dump(bstack11l1l111_opy_, outfile)
  except Exception as e:
    logger.debug(bstack11lll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡹࡵ࡭ࡹ࡯࡮ࡨࠢࡷࡳࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫ౩") + str(e))
def bstack1l111111l_opy_(bstack1l111l1l1_opy_):
  global CONFIG
  bstack1l1lll1l1_opy_ = bstack11lll1_opy_ (u"ࠧࠨ౪")
  if not bstack11lll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ౫") in CONFIG:
    logger.info(bstack11lll1_opy_ (u"ࠩࡑࡳࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠡࡲࡤࡷࡸ࡫ࡤࠡࡷࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࠦࡲࡦࡲࡲࡶࡹࠦࡦࡰࡴࠣࡖࡴࡨ࡯ࡵࠢࡵࡹࡳ࠭౬"))
  try:
    platform = CONFIG[bstack11lll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭౭")][bstack1l111l1l1_opy_]
    if bstack11lll1_opy_ (u"ࠫࡴࡹࠧ౮") in platform:
      bstack1l1lll1l1_opy_ += str(platform[bstack11lll1_opy_ (u"ࠬࡵࡳࠨ౯")]) + bstack11lll1_opy_ (u"࠭ࠬࠡࠩ౰")
    if bstack11lll1_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪ౱") in platform:
      bstack1l1lll1l1_opy_ += str(platform[bstack11lll1_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫ౲")]) + bstack11lll1_opy_ (u"ࠩ࠯ࠤࠬ౳")
    if bstack11lll1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧ౴") in platform:
      bstack1l1lll1l1_opy_ += str(platform[bstack11lll1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨ౵")]) + bstack11lll1_opy_ (u"ࠬ࠲ࠠࠨ౶")
    if bstack11lll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ౷") in platform:
      bstack1l1lll1l1_opy_ += str(platform[bstack11lll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ౸")]) + bstack11lll1_opy_ (u"ࠨ࠮ࠣࠫ౹")
    if bstack11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ౺") in platform:
      bstack1l1lll1l1_opy_ += str(platform[bstack11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ౻")]) + bstack11lll1_opy_ (u"ࠫ࠱ࠦࠧ౼")
    if bstack11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭౽") in platform:
      bstack1l1lll1l1_opy_ += str(platform[bstack11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ౾")]) + bstack11lll1_opy_ (u"ࠧ࠭ࠢࠪ౿")
  except Exception as e:
    logger.debug(bstack11lll1_opy_ (u"ࠨࡕࡲࡱࡪࠦࡥࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡱ࡫ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡴࡶࡵ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡷ࡫ࡰࡰࡴࡷࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡵ࡮ࠨಀ") + str(e))
  finally:
    if bstack1l1lll1l1_opy_[len(bstack1l1lll1l1_opy_) - 2:] == bstack11lll1_opy_ (u"ࠩ࠯ࠤࠬಁ"):
      bstack1l1lll1l1_opy_ = bstack1l1lll1l1_opy_[:-2]
    return bstack1l1lll1l1_opy_
def bstack11ll1lll11_opy_(path, bstack1l1lll1l1_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1ll111l1l_opy_ = ET.parse(path)
    bstack1ll1l11l11_opy_ = bstack1ll111l1l_opy_.getroot()
    bstack1ll1llll1l_opy_ = None
    for suite in bstack1ll1l11l11_opy_.iter(bstack11lll1_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩಂ")):
      if bstack11lll1_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫಃ") in suite.attrib:
        suite.attrib[bstack11lll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ಄")] += bstack11lll1_opy_ (u"࠭ࠠࠨಅ") + bstack1l1lll1l1_opy_
        bstack1ll1llll1l_opy_ = suite
    bstack111lllllll_opy_ = None
    for robot in bstack1ll1l11l11_opy_.iter(bstack11lll1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ಆ")):
      bstack111lllllll_opy_ = robot
    bstack111ll1ll1_opy_ = len(bstack111lllllll_opy_.findall(bstack11lll1_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧಇ")))
    if bstack111ll1ll1_opy_ == 1:
      bstack111lllllll_opy_.remove(bstack111lllllll_opy_.findall(bstack11lll1_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨಈ"))[0])
      bstack111l1lllll_opy_ = ET.Element(bstack11lll1_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩಉ"), attrib={bstack11lll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩಊ"): bstack11lll1_opy_ (u"࡙ࠬࡵࡪࡶࡨࡷࠬಋ"), bstack11lll1_opy_ (u"࠭ࡩࡥࠩಌ"): bstack11lll1_opy_ (u"ࠧࡴ࠲ࠪ಍")})
      bstack111lllllll_opy_.insert(1, bstack111l1lllll_opy_)
      bstack1l1ll1lll_opy_ = None
      for suite in bstack111lllllll_opy_.iter(bstack11lll1_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧಎ")):
        bstack1l1ll1lll_opy_ = suite
      bstack1l1ll1lll_opy_.append(bstack1ll1llll1l_opy_)
      bstack1ll1llll1_opy_ = None
      for status in bstack1ll1llll1l_opy_.iter(bstack11lll1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩಏ")):
        bstack1ll1llll1_opy_ = status
      bstack1l1ll1lll_opy_.append(bstack1ll1llll1_opy_)
    bstack1ll111l1l_opy_.write(path)
  except Exception as e:
    logger.debug(bstack11lll1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡳࡵ࡬ࡲ࡬ࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠨಐ") + str(e))
def bstack1l1l1l1l1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack11llll11ll_opy_
  global CONFIG
  if bstack11lll1_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡴࡦࡺࡨࠣ಑") in options:
    del options[bstack11lll1_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡵࡧࡴࡩࠤಒ")]
  json_data = bstack1lll1l1l1_opy_()
  for item_id in json_data.keys():
    path = os.path.join(outs_dir, str(item_id), bstack11lll1_opy_ (u"࠭࡯ࡶࡶࡳࡹࡹ࠴ࡸ࡮࡮ࠪಓ"))
    bstack11ll1lll11_opy_(path, bstack1l111111l_opy_(json_data[item_id]))
  bstack1ll1llll11_opy_()
  return bstack11llll11ll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1111l111l_opy_(self, ff_profile_dir):
  global bstack11ll1111ll_opy_
  if not ff_profile_dir:
    return None
  return bstack11ll1111ll_opy_(self, ff_profile_dir)
def bstack1lll111l11_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack111l11l1l1_opy_
  bstack11llll1l_opy_ = []
  if bstack11lll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪಔ") in CONFIG:
    bstack11llll1l_opy_ = CONFIG[bstack11lll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫಕ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack11lll1_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࠥಖ")],
      pabot_args[bstack11lll1_opy_ (u"ࠥࡺࡪࡸࡢࡰࡵࡨࠦಗ")],
      argfile,
      pabot_args.get(bstack11lll1_opy_ (u"ࠦ࡭࡯ࡶࡦࠤಘ")),
      pabot_args[bstack11lll1_opy_ (u"ࠧࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠣಙ")],
      platform[0],
      bstack111l11l1l1_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack11lll1_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡧ࡫࡯ࡩࡸࠨಚ")] or [(bstack11lll1_opy_ (u"ࠢࠣಛ"), None)]
    for platform in enumerate(bstack11llll1l_opy_)
  ]
def bstack1l1ll1l1_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack111l1ll11_opy_=bstack11lll1_opy_ (u"ࠨࠩಜ")):
  global bstack1l1llllll1_opy_
  self.platform_index = platform_index
  self.bstack1lll111111_opy_ = bstack111l1ll11_opy_
  bstack1l1llllll1_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack11lll1111l_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack111llll1ll_opy_
  global bstack1l1l1lll1l_opy_
  bstack1111l1l1ll_opy_ = copy.deepcopy(item)
  if not bstack11lll1_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫಝ") in item.options:
    bstack1111l1l1ll_opy_.options[bstack11lll1_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬಞ")] = []
  bstack11ll1ll11_opy_ = bstack1111l1l1ll_opy_.options[bstack11lll1_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ಟ")].copy()
  for v in bstack1111l1l1ll_opy_.options[bstack11lll1_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧಠ")]:
    if bstack11lll1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬಡ") in v:
      bstack11ll1ll11_opy_.remove(v)
    if bstack11lll1_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙ࠧಢ") in v:
      bstack11ll1ll11_opy_.remove(v)
    if bstack11lll1_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡅࡇࡉࡐࡔࡉࡁࡍࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬಣ") in v:
      bstack11ll1ll11_opy_.remove(v)
  bstack11ll1ll11_opy_.insert(0, bstack11lll1_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘ࠻ࡽࢀࠫತ").format(bstack1111l1l1ll_opy_.platform_index))
  bstack11ll1ll11_opy_.insert(0, bstack11lll1_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡇࡉࡋࡒࡏࡄࡃࡏࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘ࠺ࡼࡿࠪಥ").format(bstack1111l1l1ll_opy_.bstack1lll111111_opy_))
  bstack1111l1l1ll_opy_.options[bstack11lll1_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ದ")] = bstack11ll1ll11_opy_
  if bstack1l1l1lll1l_opy_:
    bstack1111l1l1ll_opy_.options[bstack11lll1_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧಧ")].insert(0, bstack11lll1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘࡀࡻࡾࠩನ").format(bstack1l1l1lll1l_opy_))
  return bstack111llll1ll_opy_(caller_id, datasources, is_last, bstack1111l1l1ll_opy_, outs_dir)
def bstack1ll111lll1_opy_(command, item_index):
  try:
    if global_config.get_property(bstack11lll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ಩")):
      os.environ[bstack11lll1_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩಪ")] = json.dumps(CONFIG[bstack11lll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬಫ")][item_index % bstack111l111ll_opy_])
    global bstack1l1l1lll1l_opy_
    os.environ[bstack11lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪಬ")] = str(item_index % bstack111l111ll_opy_)
    listener_arg = bstack11lll1_opy_ (u"ࠫࠬಭ")
    if is_robot_playwright_installed() and cli.is_enabled(CONFIG):
      listener_arg = bstack11lll1_opy_ (u"ࠬࠦ࠭࠮࡮࡬ࡷࡹ࡫࡮ࡦࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡨࡰ࠴ࡲࡰࡤࡲࡸࡤࡲࡩࡴࡶࡨࡲࡪࡸ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠲ࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡑࡣࡷࡧ࡭࡫ࡲࠨಮ")
      logger.debug(bstack11lll1_opy_ (u"ࠨࡁࡥࡦ࡬ࡲ࡬ࠦࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡓࡥࡹࡩࡨࡦࡴࠣࡰ࡮ࡹࡴࡦࡰࡨࡶࠥ࡬࡯ࡳࠢ࡬ࡸࡪࡳࠠࡼࡿࠥಯ").format(item_index))
    bstack1l11l1l1ll_opy_ = bstack11lll1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡳࡥ࡭ࠣࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠤ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࠠࠣರ") + \
              str(item_index % bstack111l111ll_opy_) + \
              bstack11lll1_opy_ (u"ࠣࠢ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠡࠤಱ") + \
              str(item_index) + \
              listener_arg
    if bstack1l1l1lll1l_opy_:
        bstack1l11l1l1ll_opy_ += bstack11lll1_opy_ (u"ࠤࠣࠦಲ") + bstack1l1l1lll1l_opy_
    command[0:1] = bstack1l11l1l1ll_opy_.split()
  except Exception as e:
    logger.error(bstack11lll1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡰࡳࡩ࡯ࡦࡺ࡫ࡱ࡫ࠥࡩ࡯࡮࡯ࡤࡲࡩࠦࡦࡰࡴࠣࡴࡦࡨ࡯ࡵࠢࡵࡹࡳࡀࠠࡼࡿࠪಳ").format(str(e)))
def bstack11ll11111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack111111l1ll_opy_
  try:
    bstack1ll111lll1_opy_(command, item_index)
    return bstack111111l1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
  except Exception as e:
    logger.error(bstack11lll1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡢࡤࡲࡸࠥࡸࡵ࡯࠼ࠣࡿࢂ࠭಴").format(str(e)))
    raise e
def bstack1111lllll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack111111l1ll_opy_
  try:
    bstack1ll111lll1_opy_(command, item_index)
    return bstack111111l1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
  except Exception as e:
    logger.error(bstack11lll1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡥࡳࡹࠦࡲࡶࡰࠣ࠶࠳࠷࠳࠻ࠢࡾࢁࠬವ").format(str(e)))
    try:
      return bstack111111l1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
    except Exception as e2:
      logger.error(bstack11lll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠ࠳࠰࠴࠷ࠥ࡬ࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࡽࢀࠫಶ").format(str(e2)))
      raise e
def bstack11llll111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack111111l1ll_opy_
  try:
    bstack1ll111lll1_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    return bstack111111l1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
  except Exception as e:
    logger.error(bstack11lll1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡧࡵࡴࠡࡴࡸࡲࠥ࠸࠮࠲࠷࠽ࠤࢀࢃࠧಷ").format(str(e)))
    try:
      return bstack111111l1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
    except Exception as e2:
      logger.error(bstack11lll1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡦࡨ࡯ࡵࠢ࠵࠲࠶࠻ࠠࡧࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣࡿࢂ࠭ಸ").format(str(e2)))
      raise e
def _11l11111l_opy_(bstack1l1ll1l111_opy_, item_index, process_timeout, sleep_before_start, bstack11111ll1l_opy_):
  bstack1ll111lll1_opy_(bstack1l1ll1l111_opy_, item_index)
  if process_timeout is None:
    process_timeout = 3600
  if sleep_before_start and sleep_before_start > 0:
    time.sleep(min(sleep_before_start, 5))
  return process_timeout
def bstack1l1ll111_opy_(command, bstack1ll1ll11l_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack111111l1ll_opy_
  global bstack11111l1l1l_opy_
  global bstack1l1l1lll1l_opy_
  try:
    for env_name, bstack11ll1ll111_opy_ in bstack11111l1l1l_opy_.items():
      os.environ[env_name] = bstack11ll1ll111_opy_
    bstack1l1l1lll1l_opy_ = bstack11lll1_opy_ (u"ࠤࠥಹ")
    bstack1ll111lll1_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    if sleep_before_start and sleep_before_start > 0:
      time.sleep(min(sleep_before_start, 5))
    return bstack111111l1ll_opy_(command, bstack1ll1ll11l_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack11lll1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡣࡱࡷࠤࡷࡻ࡮ࠡ࠷࠱࠴࠿ࠦࡻࡾࠩ಺").format(str(e)))
    try:
      return bstack111111l1ll_opy_(command, bstack1ll1ll11l_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack11lll1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡢࡤࡲࡸࠥ࡬ࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࡽࢀࠫ಻").format(str(e2)))
      raise e
def bstack1ll1l11l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack111111l1ll_opy_
  try:
    process_timeout = _11l11111l_opy_(command, item_index, process_timeout, sleep_before_start, bstack11lll1_opy_ (u"ࠬ࠺࠮࠳಼ࠩ"))
    return bstack111111l1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack11lll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠࡳࡷࡱࠤ࠹࠴࠲࠻ࠢࡾࢁࠬಽ").format(str(e)))
    try:
      return bstack111111l1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack11lll1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡧࡵࡴࠡࡨࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࢀࢃࠧಾ").format(str(e2)))
      raise e
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack1ll1111l1_opy_(self, runner, quiet=False, capture=True):
  global bstack11l1l1l11_opy_
  bstack11111l11l_opy_ = bstack11l1l1l11_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack11lll1_opy_ (u"ࠨࡧࡻࡧࡪࡶࡴࡪࡱࡱࡣࡦࡸࡲࠨಿ")):
      runner.exception_arr = []
    if not hasattr(runner, bstack11lll1_opy_ (u"ࠩࡨࡼࡨࡥࡴࡳࡣࡦࡩࡧࡧࡣ࡬ࡡࡤࡶࡷ࠭ೀ")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack11111l11l_opy_
def bstack1111lll1l1_opy_(runner, hook_name, context, element, bstack11111l1l_opy_, *args):
  global bstack11ll1ll11l_opy_
  try:
    if runner.hooks.get(hook_name):
      bstack111l11l1_opy_.bstack11l1111ll_opy_(hook_name, element)
    if bstack11ll1ll11l_opy_ is None or bstack11ll1ll11l_opy_:
      bstack11111l1l_opy_(runner, hook_name, context, *args)
    else:
      bstack11llllll1l_opy_ = (context,) + args
      bstack11111l1l_opy_(runner, hook_name, *bstack11llllll1l_opy_)
    if runner.hooks.get(hook_name):
      bstack111l11l1_opy_.bstack1111ll1111_opy_(element)
      if hook_name not in [bstack11lll1_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠧು"), bstack11lll1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡥࡱࡲࠧೂ")] and args and hasattr(args[0], bstack11lll1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡣࡲ࡫ࡳࡴࡣࡪࡩࠬೃ")):
        args[0].error_message = bstack11lll1_opy_ (u"࠭ࠧೄ")
  except Exception as e:
    logger.debug(bstack11lll1_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣ࡬ࡦࡴࡤ࡭ࡧࠣ࡬ࡴࡵ࡫ࡴࠢ࡬ࡲࠥࡨࡥࡩࡣࡹࡩ࠿ࠦࡻࡾࠩ೅").format(str(e)))
@measure(event_name=EVENTS.bstack1ll111111l_opy_, stage=STAGE.bstack1lllllll11_opy_, hook_type=bstack11lll1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡂ࡮࡯ࠦೆ"), bstack1l11ll11l_opy_=SESSION_NAME)
def bstack1l11l11lll_opy_(runner, name, context, bstack11111l1l_opy_, *args):
    if runner.hooks.get(bstack11lll1_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨೇ")).__name__ != bstack11lll1_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲ࡟ࡥࡧࡩࡥࡺࡲࡴࡠࡪࡲࡳࡰࠨೈ"):
      bstack1111lll1l1_opy_(runner, name, context, runner, bstack11111l1l_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack1ll11l1l1_opy_(bstack11lll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ೉")) else context.browser
      runner.driver_initialised = bstack11lll1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤೊ")
    except Exception as e:
      logger.debug(bstack11lll1_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡤࡳ࡫ࡹࡩࡷࠦࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡧࠣࡥࡹࡺࡲࡪࡤࡸࡸࡪࡀࠠࡼࡿࠪೋ").format(str(e)))
def bstack1111l11l1l_opy_(runner, name, context, bstack11111l1l_opy_, *args):
    bstack1111lll1l1_opy_(runner, name, context, context.feature, bstack11111l1l_opy_, *args)
    try:
      if not bstack1ll1l11l_opy_:
        bstack111l111l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll11l1l1_opy_(bstack11lll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ೌ")) else context.browser
        if is_driver_active(bstack111l111l1_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack11lll1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠤ್")
          bstack11l1ll1l1l_opy_ = str(runner.feature.name)
          playwright_set_session_name(context, bstack11l1ll1l1l_opy_)
          bstack111l111l1_opy_.execute_script(bstack11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧ೎") + json.dumps(bstack11l1ll1l1l_opy_) + bstack11lll1_opy_ (u"ࠪࢁࢂ࠭೏"))
    except Exception as e:
      logger.debug(bstack11lll1_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣ࡭ࡳࠦࡢࡦࡨࡲࡶࡪࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫ೐").format(str(e)))
def bstack11l111111l_opy_(runner, name, context, bstack11111l1l_opy_, *args):
    target = context.scenario if hasattr(context, bstack11lll1_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧ೑")) else context.feature
    bstack1111lll1l1_opy_(runner, name, context, target, bstack11111l1l_opy_, *args)
@measure(event_name=EVENTS.bstack1l1llll1ll_opy_, stage=STAGE.bstack1lllllll11_opy_, bstack1l11ll11l_opy_=SESSION_NAME)
def bstack1l11l111l_opy_(runner, name, context, bstack11111l1l_opy_, *args):
    bstack111l11l1_opy_.start_test(context)
    bstack1111lll1l1_opy_(runner, name, context, context.scenario, bstack11111l1l_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack1l11ll1l1l_opy_.bstack1111ll11l1_opy_(context, *args)
    try:
      bstack111l111l1_opy_ = bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ೒"), context.browser)
      if is_driver_active(bstack111l111l1_opy_):
        TestHubHandler.send_cbt_info(bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭೓"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack11lll1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥ೔")
        if (not bstack1ll1l11l_opy_):
          scenario_name = args[0].name
          feature_name = bstack11l1ll1l1l_opy_ = str(runner.feature.name)
          bstack11l1ll1l1l_opy_ = feature_name + bstack11lll1_opy_ (u"ࠩࠣ࠱ࠥ࠭ೕ") + scenario_name
          if runner.driver_initialised == bstack11lll1_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧೖ"):
            playwright_set_session_name(context, bstack11l1ll1l1l_opy_)
            bstack111l111l1_opy_.execute_script(bstack11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩ೗") + json.dumps(bstack11l1ll1l1l_opy_) + bstack11lll1_opy_ (u"ࠬࢃࡽࠨ೘"))
    except Exception as e:
      logger.debug(bstack11lll1_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱ࠽ࠤࢀࢃࠧ೙").format(str(e)))
@measure(event_name=EVENTS.bstack1ll111111l_opy_, stage=STAGE.bstack1lllllll11_opy_, hook_type=bstack11lll1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࡓࡵࡧࡳࠦ೚"), bstack1l11ll11l_opy_=SESSION_NAME)
def bstack1lll1l111_opy_(runner, name, context, bstack11111l1l_opy_, *args):
    bstack1111lll1l1_opy_(runner, name, context, args[0], bstack11111l1l_opy_, *args)
    try:
      bstack111l111l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll11l1l1_opy_(bstack11lll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ೛")) else context.browser
      if is_driver_active(bstack111l111l1_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack11lll1_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢ೜")
        bstack111l11l1_opy_.bstack1ll11ll111_opy_(args[0])
        if runner.driver_initialised == bstack11lll1_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣೝ") and not bstack1ll1l11l_opy_:
          feature_name = bstack11l1ll1l1l_opy_ = str(runner.feature.name)
          bstack11l1ll1l1l_opy_ = feature_name + bstack11lll1_opy_ (u"ࠫࠥ࠳ࠠࠨೞ") + context.scenario.name
          playwright_set_session_name(context, bstack11l1ll1l1l_opy_)
          bstack111l111l1_opy_.execute_script(bstack11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ೟") + json.dumps(bstack11l1ll1l1l_opy_) + bstack11lll1_opy_ (u"࠭ࡽࡾࠩೠ"))
    except Exception as e:
      logger.debug(bstack11lll1_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡸࡪࡶ࠺ࠡࡽࢀࠫೡ").format(str(e)))
@measure(event_name=EVENTS.bstack1ll111111l_opy_, stage=STAGE.bstack1lllllll11_opy_, hook_type=bstack11lll1_opy_ (u"ࠣࡣࡩࡸࡪࡸࡓࡵࡧࡳࠦೢ"), bstack1l11ll11l_opy_=SESSION_NAME)
def bstack1ll1111lll_opy_(runner, name, context, bstack11111l1l_opy_, *args):
  bstack111l11l1_opy_.bstack1l11111111_opy_(args[0])
  try:
    step_status = args[0].status.name
    bstack111l111l1_opy_ = threading.current_thread().bstackSessionDriver if bstack11lll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨೣ") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack111l111l1_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack11lll1_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪ೤")
        if not bstack1ll1l11l_opy_:
          feature_name = bstack11l1ll1l1l_opy_ = str(runner.feature.name)
          bstack11l1ll1l1l_opy_ = feature_name + bstack11lll1_opy_ (u"ࠫࠥ࠳ࠠࠨ೥") + context.scenario.name
          playwright_set_session_name(context, bstack11l1ll1l1l_opy_)
          bstack111l111l1_opy_.execute_script(bstack11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ೦") + json.dumps(bstack11l1ll1l1l_opy_) + bstack11lll1_opy_ (u"࠭ࡽࡾࠩ೧"))
    if str(step_status).lower() in [bstack11lll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ೨"), bstack11lll1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ೩")]:
      bstack1l1lllll1_opy_ = bstack11lll1_opy_ (u"ࠩࠪ೪")
      bstack111l1l1ll1_opy_ = bstack11lll1_opy_ (u"ࠪࠫ೫")
      bstack11ll1l1ll1_opy_ = bstack11lll1_opy_ (u"ࠫࠬ೬")
      try:
        import traceback
        bstack1l1lllll1_opy_ = runner.exception.__class__.__name__
        bstack1lll1l1l1l_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack111l1l1ll1_opy_ = bstack11lll1_opy_ (u"ࠬࠦࠧ೭").join(bstack1lll1l1l1l_opy_)
        bstack11ll1l1ll1_opy_ = bstack1lll1l1l1l_opy_[-1]
      except Exception as e:
        logger.debug(bstack1111l1111l_opy_.format(str(e)))
      bstack1l1lllll1_opy_ += bstack11ll1l1ll1_opy_
      playwright_annotate(context, json.dumps(str(args[0].name) + bstack11lll1_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧ೮") + str(bstack111l1l1ll1_opy_)),
                          bstack11lll1_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨ೯"))
      if runner.driver_initialised == bstack11lll1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨ೰"):
        bstack1ll11ll1ll_opy_(getattr(context, bstack11lll1_opy_ (u"ࠩࡳࡥ࡬࡫ࠧೱ"), None), bstack11lll1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥೲ"), bstack1l1lllll1_opy_)
        bstack111l111l1_opy_.execute_script(bstack11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩೳ") + json.dumps(str(args[0].name) + bstack11lll1_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦ೴") + str(bstack111l1l1ll1_opy_)) + bstack11lll1_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥࢁࢂ࠭೵"))
      if runner.driver_initialised == bstack11lll1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧ೶"):
        bstack11111l11_opy_(bstack111l111l1_opy_, bstack11lll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ೷"), bstack11lll1_opy_ (u"ࠤࡖࡧࡪࡴࡡࡳ࡫ࡲࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨ೸") + str(bstack1l1lllll1_opy_))
    else:
      playwright_annotate(context, bstack11lll1_opy_ (u"ࠥࡔࡦࡹࡳࡦࡦࠤࠦ೹"), bstack11lll1_opy_ (u"ࠦ࡮ࡴࡦࡰࠤ೺"))
      if runner.driver_initialised == bstack11lll1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥ೻"):
        bstack1ll11ll1ll_opy_(getattr(context, bstack11lll1_opy_ (u"࠭ࡰࡢࡩࡨࠫ೼"), None), bstack11lll1_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ೽"))
      bstack111l111l1_opy_.execute_script(bstack11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭೾") + json.dumps(str(args[0].name) + bstack11lll1_opy_ (u"ࠤࠣ࠱ࠥࡖࡡࡴࡵࡨࡨࠦࠨ೿")) + bstack11lll1_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩഀ"))
      if runner.driver_initialised == bstack11lll1_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤഁ"):
        bstack11111l11_opy_(bstack111l111l1_opy_, bstack11lll1_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧം"))
  except Exception as e:
    logger.debug(bstack11lll1_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࠣࡷࡹ࡫ࡰ࠻ࠢࡾࢁࠬഃ").format(str(e)))
  bstack1111lll1l1_opy_(runner, name, context, args[0], bstack11111l1l_opy_, *args)
@measure(event_name=EVENTS.bstack11ll111lll_opy_, stage=STAGE.bstack1lllllll11_opy_, bstack1l11ll11l_opy_=SESSION_NAME)
def bstack11l11lll1l_opy_(runner, name, context, bstack11111l1l_opy_, *args):
  bstack111l11l1_opy_.end_test(args[0])
  try:
    bstack1l1l1l1ll_opy_ = args[0].status.name
    bstack111l111l1_opy_ = bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ഄ"), context.browser)
    bstack1l11ll1l1l_opy_.bstack111lll11ll_opy_(bstack111l111l1_opy_)
    if str(bstack1l1l1l1ll_opy_).lower() in [bstack11lll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨഅ"), bstack11lll1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨആ")]:
      bstack1l1lllll1_opy_ = bstack11lll1_opy_ (u"ࠪࠫഇ")
      bstack111l1l1ll1_opy_ = bstack11lll1_opy_ (u"ࠫࠬഈ")
      bstack11ll1l1ll1_opy_ = bstack11lll1_opy_ (u"ࠬ࠭ഉ")
      try:
        import traceback
        bstack1l1lllll1_opy_ = runner.exception.__class__.__name__
        bstack1lll1l1l1l_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack111l1l1ll1_opy_ = bstack11lll1_opy_ (u"࠭ࠠࠨഊ").join(bstack1lll1l1l1l_opy_)
        bstack11ll1l1ll1_opy_ = bstack1lll1l1l1l_opy_[-1]
      except Exception as e:
        logger.debug(bstack1111l1111l_opy_.format(str(e)))
      bstack1l1lllll1_opy_ += bstack11ll1l1ll1_opy_
      playwright_annotate(context, json.dumps(str(args[0].name) + bstack11lll1_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨഋ") + str(bstack111l1l1ll1_opy_)),
                          bstack11lll1_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢഌ"))
      if runner.driver_initialised == bstack11lll1_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦ഍") or runner.driver_initialised == bstack11lll1_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪഎ"):
        bstack1ll11ll1ll_opy_(getattr(context, bstack11lll1_opy_ (u"ࠫࡵࡧࡧࡦࠩഏ"), None), bstack11lll1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧഐ"), bstack1l1lllll1_opy_)
        bstack111l111l1_opy_.execute_script(bstack11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ഑") + json.dumps(str(args[0].name) + bstack11lll1_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨഒ") + str(bstack111l1l1ll1_opy_)) + bstack11lll1_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨഓ"))
      if runner.driver_initialised == bstack11lll1_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦഔ") or runner.driver_initialised == bstack11lll1_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪക"):
        bstack11111l11_opy_(bstack111l111l1_opy_, bstack11lll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫഖ"), bstack11lll1_opy_ (u"࡙ࠧࡣࡦࡰࡤࡶ࡮ࡵࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤഗ") + str(bstack1l1lllll1_opy_))
    else:
      playwright_annotate(context, bstack11lll1_opy_ (u"ࠨࡐࡢࡵࡶࡩࡩࠧࠢഘ"), bstack11lll1_opy_ (u"ࠢࡪࡰࡩࡳࠧങ"))
      if runner.driver_initialised == bstack11lll1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥച") or runner.driver_initialised == bstack11lll1_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩഛ"):
        bstack1ll11ll1ll_opy_(getattr(context, bstack11lll1_opy_ (u"ࠪࡴࡦ࡭ࡥࠨജ"), None), bstack11lll1_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦഝ"))
      bstack111l111l1_opy_.execute_script(bstack11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪഞ") + json.dumps(str(args[0].name) + bstack11lll1_opy_ (u"ࠨࠠ࠮ࠢࡓࡥࡸࡹࡥࡥࠣࠥട")) + bstack11lll1_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥࢁࢂ࠭ഠ"))
      if runner.driver_initialised == bstack11lll1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥഡ") or runner.driver_initialised == bstack11lll1_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩഢ"):
        bstack11111l11_opy_(bstack111l111l1_opy_, bstack11lll1_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥണ"))
  except Exception as e:
    logger.debug(bstack11lll1_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭ത").format(str(e)))
  bstack1111lll1l1_opy_(runner, name, context, context.scenario, bstack11111l1l_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack111lllll1l_opy_(runner, name, context, bstack11111l1l_opy_, *args):
    target = context.scenario if hasattr(context, bstack11lll1_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧഥ")) else context.feature
    bstack1111lll1l1_opy_(runner, name, context, target, bstack11111l1l_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack11lll1lll_opy_(runner, name, context, bstack11111l1l_opy_, *args):
    try:
      bstack111l111l1_opy_ = bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬദ"), context.browser)
      bstack1111l11ll1_opy_ = bstack11lll1_opy_ (u"ࠧࠨധ")
      if context.failed is True:
        bstack11l1l1l111_opy_ = []
        bstack111l1l1111_opy_ = []
        bstack11ll1lll_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack11l1l1l111_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1lll1l1l1l_opy_ = traceback.format_tb(exc_tb)
            bstack1ll11111l1_opy_ = bstack11lll1_opy_ (u"ࠨࠢࠪന").join(bstack1lll1l1l1l_opy_)
            bstack111l1l1111_opy_.append(bstack1ll11111l1_opy_)
            bstack11ll1lll_opy_.append(bstack1lll1l1l1l_opy_[-1])
        except Exception as e:
          logger.debug(bstack1111l1111l_opy_.format(str(e)))
        bstack1l1lllll1_opy_ = bstack11lll1_opy_ (u"ࠩࠪഩ")
        for i in range(len(bstack11l1l1l111_opy_)):
          bstack1l1lllll1_opy_ += bstack11l1l1l111_opy_[i] + bstack11ll1lll_opy_[i] + bstack11lll1_opy_ (u"ࠪࡠࡳ࠭പ")
        bstack1111l11ll1_opy_ = bstack11lll1_opy_ (u"ࠫࠥ࠭ഫ").join(bstack111l1l1111_opy_)
        if runner.driver_initialised in [bstack11lll1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨബ"), bstack11lll1_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥഭ")]:
          playwright_annotate(context, bstack1111l11ll1_opy_, bstack11lll1_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨമ"))
          bstack1ll11ll1ll_opy_(getattr(context, bstack11lll1_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭യ"), None), bstack11lll1_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤര"), bstack1l1lllll1_opy_)
          bstack111l111l1_opy_.execute_script(bstack11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨറ") + json.dumps(bstack1111l11ll1_opy_) + bstack11lll1_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣࡿࢀࠫല"))
          bstack11111l11_opy_(bstack111l111l1_opy_, bstack11lll1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧള"), bstack11lll1_opy_ (u"ࠨࡓࡰ࡯ࡨࠤࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡹࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡ࡞ࡱࠦഴ") + str(bstack1l1lllll1_opy_))
          bstack1l11l1l111_opy_ = bstack1ll1lll1l1_opy_(bstack1111l11ll1_opy_, runner.feature.name, logger)
          if (bstack1l11l1l111_opy_ != None):
            bstack1lll1111l1_opy_.append(bstack1l11l1l111_opy_)
      else:
        if runner.driver_initialised in [bstack11lll1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣവ"), bstack11lll1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧശ")]:
          playwright_annotate(context, bstack11lll1_opy_ (u"ࠤࡉࡩࡦࡺࡵࡳࡧ࠽ࠤࠧഷ") + str(runner.feature.name) + bstack11lll1_opy_ (u"ࠥࠤࡵࡧࡳࡴࡧࡧࠥࠧസ"), bstack11lll1_opy_ (u"ࠦ࡮ࡴࡦࡰࠤഹ"))
          bstack1ll11ll1ll_opy_(getattr(context, bstack11lll1_opy_ (u"ࠬࡶࡡࡨࡧࠪഺ"), None), bstack11lll1_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ഻"))
          bstack111l111l1_opy_.execute_script(bstack11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾഼ࠬ") + json.dumps(bstack11lll1_opy_ (u"ࠣࡈࡨࡥࡹࡻࡲࡦ࠼ࠣࠦഽ") + str(runner.feature.name) + bstack11lll1_opy_ (u"ࠤࠣࡴࡦࡹࡳࡦࡦࠤࠦാ")) + bstack11lll1_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩി"))
          bstack11111l11_opy_(bstack111l111l1_opy_, bstack11lll1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫീ"))
          bstack1l11l1l111_opy_ = bstack1ll1lll1l1_opy_(bstack1111l11ll1_opy_, runner.feature.name, logger)
          if (bstack1l11l1l111_opy_ != None):
            bstack1lll1111l1_opy_.append(bstack1l11l1l111_opy_)
    except Exception as e:
      logger.debug(bstack11lll1_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧു").format(str(e)))
    bstack1111lll1l1_opy_(runner, name, context, context.feature, bstack11111l1l_opy_, *args)
@measure(event_name=EVENTS.bstack1ll111111l_opy_, stage=STAGE.bstack1lllllll11_opy_, hook_type=bstack11lll1_opy_ (u"ࠨࡡࡧࡶࡨࡶࡆࡲ࡬ࠣൂ"), bstack1l11ll11l_opy_=SESSION_NAME)
def bstack1ll1ll1ll_opy_(runner, name, context, bstack11111l1l_opy_, *args):
    bstack1111lll1l1_opy_(runner, name, context, runner, bstack11111l1l_opy_, *args)
def bstack1l11l1ll11_opy_(self, filename=None):
  global bstack1lll1l1lll_opy_
  bstack1lll1l1lll_opy_(self, filename)
  bstack11l1ll11ll_opy_ = []
  bstack1l111ll1_opy_ = [bstack11lll1_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠨൃ"), bstack11lll1_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡶࡤ࡫ࠬൄ"), bstack11lll1_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ൅"), bstack11lll1_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫെ"), bstack11lll1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡸࡦ࡭ࠧേ"), bstack11lll1_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬൈ")]
  bstack1lll1ll111_opy_ = lambda *_: None
  for hook_name in bstack1l111ll1_opy_:
    if hook_name not in self.hooks:
      self.hooks[hook_name] = bstack1lll1ll111_opy_
      bstack11l1ll11ll_opy_.append(hook_name)
  if bstack11l1ll11ll_opy_:
    os.environ[bstack11lll1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡓࡅࡍࡢࡈࡊࡌࡁࡖࡎࡗࡣࡍࡕࡏࡌࡕࠪ൉")] = bstack11lll1_opy_ (u"ࠧ࠭ࠩൊ").join(bstack11l1ll11ll_opy_)
def _execute_deferred_playwright_close():
  try:
    _11l1l1ll_opy_ = threading.current_thread()
    _1ll11111l_opy_ = getattr(_11l1l1ll_opy_, bstack11lll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡦࡨࡪࡪࡸࡲࡦࡦࡢࡴࡦ࡭ࡥࡠࡴࡨࡪࠬോ"), None)
    _1lll1l1l_opy_ = getattr(_11l1l1ll_opy_, bstack11lll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡧࡩ࡫࡫ࡲࡳࡧࡧࡣࡧࡸ࡯ࡸࡵࡨࡶࡤࡸࡥࡧࠩൌ"), None)
    _1lll1llll_opy_ = getattr(_11l1l1ll_opy_, bstack11lll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡨࡪ࡬ࡥࡳࡴࡨࡨࡤࡶࡷࡠࡵࡷࡳࡵࡥࡦ࡯്ࠩ"), None)
    _wrapper = getattr(_11l1l1ll_opy_, bstack11lll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪൎ"), None)
    if not _1lll1l1l_opy_ and _wrapper and hasattr(_wrapper, bstack11lll1_opy_ (u"ࠬࡥࡢࡳࡱࡺࡷࡪࡸࠧ൏")):
      _1lll1l1l_opy_ = _wrapper._browser
    if not _1ll11111l_opy_ and _wrapper and hasattr(_wrapper, bstack11lll1_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬ൐")):
      _1ll11111l_opy_ = _wrapper._page
    if not _1lll1llll_opy_:
      _111lll1l11_opy_ = getattr(_11l1l1ll_opy_, bstack11lll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡥࡧࡩࡩࡷࡸࡥࡥࡡࡳࡻࡤࡸࡥࡧࠩ൑"), None)
      if _111lll1l11_opy_ and hasattr(_111lll1l11_opy_, bstack11lll1_opy_ (u"ࠨࡵࡷࡳࡵ࠭൒")):
        _1lll1llll_opy_ = _111lll1l11_opy_.stop
    _1ll1lll1l_opy_ = _1ll11111l_opy_ or _1lll1l1l_opy_ or _1lll1llll_opy_
    if not _1ll1lll1l_opy_:
      return
    if _1ll11111l_opy_ and hasattr(_1ll11111l_opy_, bstack11lll1_opy_ (u"ࠩࡦࡰࡴࡹࡥࠨ൓")):
      try:
        _1ll11111l_opy_.close(_bstack_sdk_close=True)
      except TypeError:
        try:
          _1ll11111l_opy_.close()
        except Exception:
          pass
      except Exception as e:
        logger.debug(bstack11lll1_opy_ (u"ࠪࡈࡪ࡬ࡥࡳࡴࡨࡨࠥࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡳࡥ࡬࡫࠮ࡤ࡮ࡲࡷࡪࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࡼࡿࠪൔ").format(str(e)))
    if _1lll1l1l_opy_ and hasattr(_1lll1l1l_opy_, bstack11lll1_opy_ (u"ࠫࡨࡲ࡯ࡴࡧࠪൕ")):
      try:
        _1lll1l1l_opy_.close(_bstack_sdk_close=True)
      except TypeError:
        try:
          _1lll1l1l_opy_.close()
        except Exception:
          pass
      except Exception as e:
        logger.debug(bstack11lll1_opy_ (u"ࠬࡊࡥࡧࡧࡵࡶࡪࡪࠠࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡧࡸ࡯ࡸࡵࡨࡶ࠳ࡩ࡬ࡰࡵࡨࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽࠨൖ").format(str(e)))
    if _1lll1llll_opy_:
      try:
        _1lll1llll_opy_(_bstack_sdk_close=True)
      except TypeError:
        try:
          _1lll1llll_opy_()
        except Exception:
          pass
      except Exception as e:
        logger.debug(bstack11lll1_opy_ (u"࠭ࡄࡦࡨࡨࡶࡷ࡫ࡤࠡࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡴࡰࡲࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࢀࢃࠧൗ").format(str(e)))
    for attr in (bstack11lll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡥࡧࡩࡩࡷࡸࡥࡥࡡࡳࡥ࡬࡫࡟ࡤ࡮ࡲࡷࡪ࠭൘"), bstack11lll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡦࡨࡪࡪࡸࡲࡦࡦࡢࡴࡦ࡭ࡥࡠࡴࡨࡪࠬ൙"),
                 bstack11lll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡧࡩ࡫࡫ࡲࡳࡧࡧࡣࡧࡸ࡯ࡸࡵࡨࡶࡤࡩ࡬ࡰࡵࡨࠫ൚"), bstack11lll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡨࡪ࡬ࡥࡳࡴࡨࡨࡤࡨࡲࡰࡹࡶࡩࡷࡥࡲࡦࡨࠪ൛"),
                 bstack11lll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡩ࡫ࡦࡦࡴࡵࡩࡩࡥࡰࡸࡡࡶࡸࡴࡶࠧ൜"), bstack11lll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡪࡥࡧࡧࡵࡶࡪࡪ࡟ࡱࡹࡢࡷࡹࡵࡰࡠࡨࡱࠫ൝"),
                 bstack11lll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡤࡦࡨࡨࡶࡷ࡫ࡤࡠࡲࡺࡣࡷ࡫ࡦࠨ൞")):
      try:
        delattr(_11l1l1ll_opy_, attr)
      except AttributeError:
        pass
    if _wrapper:
      try:
        _wrapper._page = None
        _wrapper._browser = None
      except Exception:
        pass
    logger.debug(bstack11lll1_opy_ (u"ࠧࡅࡧࡩࡩࡷࡸࡥࡥࠢࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡣ࡭ࡱࡶࡩࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠡࡨࡲࡶࠥࡺࡨࡳࡧࡤࡨࠥࢁࡽࠨൟ").format(_11l1l1ll_opy_.ident))
  except Exception as e:
    logger.debug(bstack11lll1_opy_ (u"ࠨࡆࡨࡪࡪࡸࡲࡦࡦࠣࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡤ࡮ࡲࡷࡪࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࡼࡿࠪൠ").format(str(e)))
def bstack1ll11l1lll_opy_(self, name, *args):
  global bstack11111l1l_opy_
  global bstack11ll1ll11l_opy_
  try:
    if BROWSERSTACK_AUTOMATION:
      platform_index = int(threading.current_thread()._name) % bstack111l111ll_opy_
      bstack11l1ll1111_opy_ = CONFIG[bstack11lll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬൡ")][platform_index]
      os.environ[bstack11lll1_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫൢ")] = json.dumps(bstack11l1ll1111_opy_)
    if not hasattr(self, bstack11lll1_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡥࡥࠩൣ")):
      self.driver_initialised = None
    bstack111l1l1l11_opy_ = {
        bstack11lll1_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠩ൤"): bstack1l11l11lll_opy_,
        bstack11lll1_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠧ൥"): bstack1111l11l1l_opy_,
        bstack11lll1_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡵࡣࡪࠫ൦"): bstack11l111111l_opy_,
        bstack11lll1_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ൧"): bstack1l11l111l_opy_,
        bstack11lll1_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠧ൨"): bstack1lll1l111_opy_,
        bstack11lll1_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡸࡪࡶࠧ൩"): bstack1ll1111lll_opy_,
        bstack11lll1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ൪"): bstack11l11lll1l_opy_,
        bstack11lll1_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡹࡧࡧࠨ൫"): bstack111lllll1l_opy_,
        bstack11lll1_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭൬"): bstack11lll1lll_opy_,
        bstack11lll1_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪ൭"): bstack1ll1ll1ll_opy_
    }
    handler = bstack111l1l1l11_opy_.get(name, bstack11111l1l_opy_)
    try:
      if args:
        context = args[0]
        remaining_args = args[1:]
        if bstack11ll1ll11l_opy_ is None or not bstack11ll1ll11l_opy_:
          context = self.context
          remaining_args = args
      else:
        context = self.context
        remaining_args = ()
      handler(self, name, context, bstack11111l1l_opy_, *remaining_args)
    except Exception as e:
      logger.debug(bstack11lll1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡦࡪ࡮ࡡࡷࡧࠣ࡬ࡴࡵ࡫ࠡࡪࡤࡲࡩࡲࡥࡳࠢࡾࢁ࠿ࠦࡻࡾࠩ൮").format(name, str(e)))
    if name == bstack11lll1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ൯"):
      _execute_deferred_playwright_close()
    if name in [bstack11lll1_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪ൰"), bstack11lll1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ൱"), bstack11lll1_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠨ൲")]:
      try:
        bstack111l111l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll11l1l1_opy_(bstack11lll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ൳")) else context.browser
        bstack1l1ll11l1_opy_ = (
          (name == bstack11lll1_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪ൴") and self.driver_initialised == bstack11lll1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧ൵")) or
          (name == bstack11lll1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠩ൶") and self.driver_initialised == bstack11lll1_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦ൷")) or
          (name == bstack11lll1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ൸") and self.driver_initialised in [bstack11lll1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢ൹"), bstack11lll1_opy_ (u"ࠨࡩ࡯ࡵࡷࡩࡵࠨൺ")]) or
          (name == bstack11lll1_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡵࡧࡳࠫൻ") and self.driver_initialised == bstack11lll1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨർ"))
        )
        if bstack1l1ll11l1_opy_:
          self.driver_initialised = None
          if bstack111l111l1_opy_ and hasattr(bstack111l111l1_opy_, bstack11lll1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩ࠭ൽ")):
            try:
              bstack111l111l1_opy_.quit()
            except Exception as e:
              logger.debug(bstack11lll1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡴࡹ࡮ࡺࡴࡪࡰࡪࠤࡩࡸࡩࡷࡧࡵࠤ࡮ࡴࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡩࡱࡲ࡯࠿ࠦࡻࡾࠩൾ").format(str(e)))
      except Exception as e:
        logger.debug(bstack11lll1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࠥ࡮࡯ࡰ࡭ࠣࡧࡱ࡫ࡡ࡯ࡷࡳࠤ࡫ࡵࡲࠡࡽࢀ࠾ࠥࢁࡽࠨൿ").format(name, str(e)))
  except Exception as e:
    logger.debug(bstack11lll1_opy_ (u"ࠬࡉࡲࡪࡶ࡬ࡧࡦࡲࠠࡦࡴࡵࡳࡷࠦࡩ࡯ࠢࡥࡩ࡭ࡧࡶࡦࠢࡵࡹࡳࠦࡨࡰࡱ࡮ࠤࢀࢃ࠺ࠡࡽࢀࠫ඀").format(name, str(e)))
    try:
      if bstack11ll1ll11l_opy_ is None or bstack11ll1ll11l_opy_:
        try:
          bstack11111l1l_opy_(self, name, self.context, *args)
        except TypeError:
          bstack11111l1l_opy_(self, name, *args)
      else:
        bstack11111l1l_opy_(self, name, *args)
    except Exception as e2:
      logger.debug(bstack11lll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡨࡤࡰࡱࡨࡡࡤ࡭ࠣࡳࡷ࡯ࡧࡪࡰࡤࡰࠥࡨࡥࡩࡣࡹࡩࠥ࡮࡯ࡰ࡭ࠣࡿࢂࡀࠠࡼࡿࠪඁ").format(name, str(e2)))
  finally:
    if name == bstack11lll1_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨං"):
      _execute_deferred_playwright_close()
def bstack1lll1ll1_opy_(config, startdir):
  return bstack11lll1_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾ࠴ࢂࠨඃ").format(bstack11lll1_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣ඄"))
notset = Notset()
def bstack1lll111ll_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1l1l11l111_opy_
  if str(name).lower() == bstack11lll1_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪඅ"):
    return bstack11lll1_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥආ")
  else:
    return bstack1l1l11l111_opy_(self, name, default, skip)
def bstack1llllll1ll_opy_(item, when):
  global bstack1l11l1llll_opy_
  try:
    bstack1l11l1llll_opy_(item, when)
  except Exception as e:
    pass
def bstack11l11l1111_opy_():
  return
def browserstack_executor_helper(type, name, status, reason, bstack1l111111ll_opy_, bstack1ll111ll_opy_):
  bstack11l1ll111l_opy_ = {
    bstack11lll1_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬඇ"): type,
    bstack11lll1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩඈ"): {}
  }
  if type == bstack11lll1_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩඉ"):
    bstack11l1ll111l_opy_[bstack11lll1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫඊ")][bstack11lll1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨඋ")] = bstack1l111111ll_opy_
    bstack11l1ll111l_opy_[bstack11lll1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ඌ")][bstack11lll1_opy_ (u"ࠫࡩࡧࡴࡢࠩඍ")] = json.dumps(str(bstack1ll111ll_opy_))
  if type == bstack11lll1_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ඎ"):
    bstack11l1ll111l_opy_[bstack11lll1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩඏ")][bstack11lll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬඐ")] = name
  if type == bstack11lll1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫඑ"):
    bstack11l1ll111l_opy_[bstack11lll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬඒ")][bstack11lll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪඓ")] = status
    if status == bstack11lll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫඔ"):
      bstack11l1ll111l_opy_[bstack11lll1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨඕ")][bstack11lll1_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ඖ")] = json.dumps(str(reason))
  bstack1l1ll11l_opy_ = bstack11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬ඗").format(json.dumps(bstack11l1ll111l_opy_))
  return bstack1l1ll11l_opy_
def bstack11l11l11_opy_(driver_command, response):
    if driver_command == bstack11lll1_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬ඘"):
        TestHubHandler.bstack1l11lll11_opy_({
            bstack11lll1_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨ඙"): response[bstack11lll1_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩක")],
            bstack11lll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫඛ"): TestHubHandler.current_test_uuid()
        })
def bstack1lllll1111_opy_(item, call, rep):
  global bstack1llll1111_opy_
  global bstack1ll111ll1l_opy_
  global bstack1ll1l11l_opy_
  name = bstack11lll1_opy_ (u"ࠬ࠭ග")
  try:
    if rep.when == bstack11lll1_opy_ (u"࠭ࡣࡢ࡮࡯ࠫඝ"):
      bstack1l11l111l1_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1ll1l11l_opy_:
          name = str(rep.nodeid)
          executor_string = browserstack_executor_helper(bstack11lll1_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨඞ"), name, bstack11lll1_opy_ (u"ࠨࠩඟ"), bstack11lll1_opy_ (u"ࠩࠪච"), bstack11lll1_opy_ (u"ࠪࠫඡ"), bstack11lll1_opy_ (u"ࠫࠬජ"))
          threading.current_thread().bstack1ll1lll1_opy_ = name
          for driver in bstack1ll111ll1l_opy_:
            if bstack1l11l111l1_opy_ == driver.session_id:
              driver.execute_script(executor_string)
      except Exception as e:
        logger.debug(bstack11lll1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬඣ").format(str(e)))
      try:
        bstack1111l1l1l_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack11lll1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧඤ"):
          status = bstack11lll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧඥ") if rep.outcome.lower() == bstack11lll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨඦ") else bstack11lll1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩට")
          reason = bstack11lll1_opy_ (u"ࠪࠫඨ")
          if status == bstack11lll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫඩ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack11lll1_opy_ (u"ࠬ࡯࡮ࡧࡱࠪඪ") if status == bstack11lll1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ණ") else bstack11lll1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ඬ")
          data = name + bstack11lll1_opy_ (u"ࠨࠢࡳࡥࡸࡹࡥࡥࠣࠪත") if status == bstack11lll1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩථ") else name + bstack11lll1_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠥࠥ࠭ද") + reason
          bstack1l1l1lll1_opy_ = browserstack_executor_helper(bstack11lll1_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭ධ"), bstack11lll1_opy_ (u"ࠬ࠭න"), bstack11lll1_opy_ (u"࠭ࠧ඲"), bstack11lll1_opy_ (u"ࠧࠨඳ"), level, data)
          for driver in bstack1ll111ll1l_opy_:
            if bstack1l11l111l1_opy_ == driver.session_id:
              driver.execute_script(bstack1l1l1lll1_opy_)
      except Exception as e:
        logger.debug(bstack11lll1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡩ࡯࡯ࡶࡨࡼࡹࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬප").format(str(e)))
  except Exception as e:
    logger.debug(bstack11lll1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡴࡢࡶࡨࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿࢂ࠭ඵ").format(str(e)))
  bstack1llll1111_opy_(item, call, rep)
def bstack1ll1111l_opy_(driver, bstack111lll1l_opy_, test=None):
  global PLATFORM_INDEX
  if test != None:
    bstack1l11lll11l_opy_ = getattr(test, bstack11lll1_opy_ (u"ࠪࡲࡦࡳࡥࠨබ"), None)
    bstack1lll1l1ll1_opy_ = getattr(test, bstack11lll1_opy_ (u"ࠫࡺࡻࡩࡥࠩභ"), None)
    PercySDK.screenshot(driver, bstack111lll1l_opy_, bstack1l11lll11l_opy_=bstack1l11lll11l_opy_, bstack1lll1l1ll1_opy_=bstack1lll1l1ll1_opy_, bstack111l1lll1l_opy_=PLATFORM_INDEX)
  else:
    PercySDK.screenshot(driver, bstack111lll1l_opy_)
@measure(event_name=EVENTS.bstack11l11l1lll_opy_, stage=STAGE.bstack1lllllll11_opy_, bstack1l11ll11l_opy_=SESSION_NAME)
def bstack11l1l11ll_opy_(driver):
  if bstack1ll1l1llll_opy_.bstack1ll1ll111_opy_() is True or bstack1ll1l1llll_opy_.capturing() is True:
    return
  bstack1ll1l1llll_opy_.bstack1l1l11l11l_opy_()
  while not bstack1ll1l1llll_opy_.bstack1ll1ll111_opy_():
    bstack1ll1111111_opy_ = bstack1ll1l1llll_opy_.bstack11lll11l_opy_()
    bstack1ll1111l_opy_(driver, bstack1ll1111111_opy_)
  bstack1ll1l1llll_opy_.bstack1l11111l_opy_()
def bstack11l1111l1_opy_(sequence, driver_command, response = None, bstack1111ll1l11_opy_ = None, args = None):
    try:
      if sequence != bstack11lll1_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬම"):
        return
      if percy.bstack1l1l111l1_opy_() == bstack11lll1_opy_ (u"ࠨࡦࡢ࡮ࡶࡩࠧඹ"):
        return
      bstack1ll1111111_opy_ = bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"ࠧࡱࡧࡵࡧࡾ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪය"), None)
      for command in bstack111ll11ll1_opy_:
        if command == driver_command:
          with bstack1111lll11l_opy_:
            bstack1lllll1l1_opy_ = bstack1ll111ll1l_opy_.copy()
          for driver in bstack1lllll1l1_opy_:
            bstack11l1l11ll_opy_(driver)
      bstack11llll11_opy_ = percy.bstack1llllll11l_opy_()
      if driver_command in bstack111l111l11_opy_[bstack11llll11_opy_]:
        bstack1ll1l1llll_opy_.bstack11111llll_opy_(bstack1ll1111111_opy_, driver_command)
    except Exception as e:
      pass
_11l111l1l_opy_ = threading.Event()
def bstack111l1ll1l1_opy_(framework_name):
  if global_config.get_property(bstack11lll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬර")):
      _11l111l1l_opy_.wait(timeout=30)
      return
  global_config.bstack1111l11l1_opy_(bstack11lll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡰࡳࡩࡥࡣࡢ࡮࡯ࡩࡩ࠭඼"), True)
  global FRAMEWORK_NAME
  global SELENIUM_OR_PLAYWRIGHT_INSTALLED
  global bstack1ll1l111l1_opy_
  FRAMEWORK_NAME = framework_name
  logger.info(bstack1111l1ll11_opy_.format(FRAMEWORK_NAME.split(bstack11lll1_opy_ (u"ࠪ࠱ࠬල"))[0]))
  bstack111l11l11l_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    global bstack1111lll1ll_opy_
    bstack111ll111_opy_ = BROWSERSTACK_AUTOMATION or bstack1111lll1ll_opy_
    if bstack111ll111_opy_:
      Service.start = bstack11ll1ll1l1_opy_
      Service.stop = bstack1l11lll1l1_opy_
      webdriver.Remote.get = bstack1lllll111_opy_
      WebDriver.quit = bstack1ll1l11ll1_opy_
      webdriver.Remote.__init__ = bstack11111l1l11_opy_
    if not BROWSERSTACK_AUTOMATION and not bstack1111lll1ll_opy_:
        webdriver.Remote.__init__ = bstack11lll1l1l1_opy_
    WebDriver.getAccessibilityResults = getAccessibilityResults
    WebDriver.get_accessibility_results = getAccessibilityResults
    WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
    WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
    WebDriver.performScan = perform_scan
    WebDriver.perform_scan = perform_scan
    WebDriver.execute = bstack111l1111_opy_
    SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
  except Exception as e:
    pass
  try:
    bstack111ll111_opy_ = BROWSERSTACK_AUTOMATION or bstack1111lll1ll_opy_
    if bstack111ll111_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack111l111111_opy_
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
    logger.debug(bstack11lll1_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡩ࡯ࡳࡧࡧ࡬ࡴ࠼ࠣࡿࢂࠨ඾").format(str(e)))
  patch_playwright()
  if not SELENIUM_OR_PLAYWRIGHT_INSTALLED:
    bstack11l1l11111_opy_(bstack11lll1_opy_ (u"ࠧࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠠ࡯ࡱࡷࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪࠢ඿"), bstack1111111l1_opy_)
  if bstack11llll1ll_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      if hasattr(RemoteConnection, bstack11lll1_opy_ (u"࠭࡟ࡨࡧࡷࡣࡵࡸ࡯ࡹࡻࡢࡹࡷࡲࠧව")) and callable(getattr(RemoteConnection, bstack11lll1_opy_ (u"ࠧࡠࡩࡨࡸࡤࡶࡲࡰࡺࡼࡣࡺࡸ࡬ࠨශ"))):
        RemoteConnection._get_proxy_url = bstack1l1lll11ll_opy_
      else:
        from selenium.webdriver.remote.client_config import ClientConfig
        ClientConfig.get_proxy_url = bstack1l1lll11ll_opy_
    except Exception as e:
      logger.error(bstack1l11l1ll1_opy_.format(str(e)))
  if bstack1llllll1l1_opy_():
    bstack111ll111l_opy_(CONFIG, logger)
  if (bstack11lll1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧෂ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      try:
        from pabot.pabot import QueueItem
        from pabot import pabot
      except Exception as e:
        logger.warning(bstack1l1ll1lll1_opy_ + str(e))
      if not is_robot_playwright_installed():
        try:
          if percy.bstack1l1l111l1_opy_() == bstack11lll1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢස"):
            bstack111lll111_opy_(bstack11l1111l1_opy_)
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
          WebDriverCreator._get_ff_profile = bstack1111l111l_opy_
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
          WebDriverCache.close = bstack1ll11l11ll_opy_
        except Exception as e:
          logger.warning(bstack111l1llll1_opy_ + str(e))
        try:
          from AppiumLibrary.utils.applicationcache import ApplicationCache
          ApplicationCache.close = bstack11l1l1llll_opy_
        except Exception as e:
          logger.debug(bstack1l111llll1_opy_ + str(e))
    except Exception as e:
      bstack11l1l11111_opy_(e, bstack111l1llll1_opy_)
    Output.start_test = bstack1l1llll1_opy_
    Output.end_test = bstack1ll11ll1_opy_
    TestStatus.__init__ = bstack1ll1ll1111_opy_
    QueueItem.__init__ = bstack1l1ll1l1_opy_
    pabot._create_items = bstack1lll111l11_opy_
    try:
      from pabot import __version__ as bstack1lll11l111_opy_
      if version.parse(bstack1lll11l111_opy_) >= version.parse(bstack11lll1_opy_ (u"ࠪ࠹࠳࠶࠮࠱ࠩහ")):
        pabot._run = bstack1l1ll111_opy_
      elif version.parse(bstack1lll11l111_opy_) >= version.parse(bstack11lll1_opy_ (u"ࠫ࠹࠴࠲࠯࠲ࠪළ")):
        pabot._run = bstack1ll1l11l1_opy_
      elif version.parse(bstack1lll11l111_opy_) >= version.parse(bstack11lll1_opy_ (u"ࠬ࠸࠮࠲࠷࠱࠴ࠬෆ")):
        pabot._run = bstack11llll111l_opy_
      elif version.parse(bstack1lll11l111_opy_) >= version.parse(bstack11lll1_opy_ (u"࠭࠲࠯࠳࠶࠲࠵࠭෇")):
        pabot._run = bstack1111lllll1_opy_
      else:
        pabot._run = bstack11ll11111_opy_
    except Exception as e:
      pabot._run = bstack11ll11111_opy_
    pabot._create_command_for_execution = bstack11lll1111l_opy_
    pabot._report_results = bstack1l1l1l1l1_opy_
  if bstack11lll1_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ෈") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11l1l11111_opy_(e, bstack11l1lll1l_opy_)
    Runner.run_hook = bstack1ll11l1lll_opy_
    try:
      from behave import __version__ as bstack111ll11l_opy_
      if version.parse(bstack111ll11l_opy_) >= version.parse(bstack11lll1_opy_ (u"ࠨ࠳࠱࠷࠳࠶ࠧ෉")):
        Runner.load_hooks = bstack1l11l1ll11_opy_
    except Exception as e:
      logger.debug(bstack11lll1_opy_ (u"ࠩࡆࡳࡺࡲࡤࠡࡰࡲࡸࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡤࡨ࡬ࡦࡼࡥࠡࡸࡨࡶࡸ࡯࡯࡯࠼ࠣࡿࢂ්࠭").format(str(e)))
    Step.run = bstack1ll1111l1_opy_
  if bstack11lll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ෋") in str(framework_name).lower():
    if not BROWSERSTACK_AUTOMATION:
      _11l111l1l_opy_.set()
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack1lll1ll1_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack11l11l1111_opy_
      Config.getoption = bstack1lll111ll_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1lllll1111_opy_
    except Exception as e:
      pass
  _11l111l1l_opy_.set()
def bstack111l11l111_opy_():
  global CONFIG
  if bstack11lll1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ෌") in CONFIG and int(CONFIG[bstack11lll1_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ෍")]) > 1:
    logger.warning(bstack11111l111l_opy_)
def bstack1111ll11ll_opy_(arg, bstack1llll1l11_opy_, bstack1l1llll11_opy_=None):
  global CONFIG
  global bstack1llllllll_opy_
  global bstack1ll11l11_opy_
  global BROWSERSTACK_AUTOMATION
  global bstack1111lll1ll_opy_
  global global_config
  bstack11llll1l11_opy_ = bstack11lll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭෎")
  if bstack1llll1l11_opy_ and isinstance(bstack1llll1l11_opy_, str):
    bstack1llll1l11_opy_ = eval(bstack1llll1l11_opy_)
  CONFIG = bstack1llll1l11_opy_[bstack11lll1_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧා")]
  bstack1llllllll_opy_ = bstack1llll1l11_opy_[bstack11lll1_opy_ (u"ࠨࡊࡘࡆࡤ࡛ࡒࡍࠩැ")]
  bstack1ll11l11_opy_ = bstack1llll1l11_opy_[bstack11lll1_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫෑ")]
  BROWSERSTACK_AUTOMATION = bstack1llll1l11_opy_[bstack11lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭ි")]
  try:
    bstack11l111l1_opy_ = bstack1llll1l11_opy_.get(bstack11lll1_opy_ (u"ࠫࡔ࡜ࡅࡓࡔࡌࡈࡊࡥࡌࡐࡃࡇࡣ࡙ࡋࡓࡕࡋࡑࡋࠬී"), False)
    bstack1111lll1ll_opy_ = bool(bstack11l111l1_opy_)
    os.environ[bstack11lll1_opy_ (u"ࠬࡕࡖࡆࡔࡕࡍࡉࡋ࡟ࡍࡑࡄࡈࡤ࡚ࡅࡔࡖࡌࡒࡌ࠭ු")] = str(bstack1111lll1ll_opy_).lower()
  except Exception as e:
    logger.error(bstack11lll1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡓ࡛ࡋࡒࡓࡋࡇࡉࡤࡒࡏࡂࡆࡢࡘࡊ࡙ࡔࡊࡐࡊ࠾ࠥࢁࡽࠣ෕").format(e))
    bstack1111lll1ll_opy_ = False
    os.environ[bstack11lll1_opy_ (u"ࠧࡐࡘࡈࡖࡗࡏࡄࡆࡡࡏࡓࡆࡊ࡟ࡕࡇࡖࡘࡎࡔࡇࠨූ")] = bstack11lll1_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧ෗")
  global_config.bstack1111l11l1_opy_(bstack11lll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪෘ"), BROWSERSTACK_AUTOMATION)
  os.environ[bstack11lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬෙ")] = bstack11llll1l11_opy_
  os.environ[bstack11lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠪේ")] = json.dumps(CONFIG)
  os.environ[bstack11lll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡍ࡛ࡂࡠࡗࡕࡐࠬෛ")] = bstack1llllllll_opy_
  os.environ[bstack11lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧො")] = str(bstack1ll11l11_opy_)
  os.environ[bstack11lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡍࡗࡊࡍࡓ࠭ෝ")] = str(True)
  if bstack1l11l1111l_opy_(arg, [bstack11lll1_opy_ (u"ࠨ࠯ࡱࠫෞ"), bstack11lll1_opy_ (u"ࠩ࠰࠱ࡳࡻ࡭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪෟ")]) != -1:
    os.environ[bstack11lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡅࡗࡇࡌࡍࡇࡏࠫ෠")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1l1111l11_opy_)
    return
  bstack1l1l111l1l_opy_()
  global bstack1l11ll11_opy_
  global PLATFORM_INDEX
  global bstack111l11l1l1_opy_
  global bstack1l1l1lll1l_opy_
  global bstack11l1l1111_opy_
  global bstack1ll1l111l1_opy_
  global PARALLELISE_VANILLA_PYTHON
  arg.append(bstack11lll1_opy_ (u"ࠦ࠲࡝ࠢ෡"))
  arg.append(bstack11lll1_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩ࠿ࡓ࡯ࡥࡷ࡯ࡩࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡩ࡮ࡲࡲࡶࡹ࡫ࡤ࠻ࡲࡼࡸࡪࡹࡴ࠯ࡒࡼࡸࡪࡹࡴࡘࡣࡵࡲ࡮ࡴࡧࠣ෢"))
  arg.append(bstack11lll1_opy_ (u"ࠨ࠭ࡘࠤ෣"))
  arg.append(bstack11lll1_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫࠺ࡕࡪࡨࠤ࡭ࡵ࡯࡬࡫ࡰࡴࡱࠨ෤"))
  global bstack1l11l11l_opy_
  global bstack1l1ll111l1_opy_
  global bstack1ll1ll1l_opy_
  global bstack1llll1l11l_opy_
  global bstack11ll1111ll_opy_
  global bstack1l1llllll1_opy_
  global bstack111llll1ll_opy_
  global bstack1l1l11l1l_opy_
  global bstack11lll1ll1_opy_
  global bstack1ll111l111_opy_
  global bstack1l1l11l111_opy_
  global bstack1l11l1llll_opy_
  global bstack1llll1111_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l11l11l_opy_ = webdriver.Remote.__init__
    bstack1l1ll111l1_opy_ = WebDriver.quit
    bstack1l1l11l1l_opy_ = WebDriver.close
    bstack11lll1ll1_opy_ = WebDriver.get
    bstack1ll1ll1l_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1l111l1111_opy_(CONFIG) and bstack1llllllll1_opy_():
    if bstack1ll11lll11_opy_() < version.parse(bstack1ll1l1l1ll_opy_):
      logger.error(bstack1l1l1lll_opy_.format(bstack1ll11lll11_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack11lll1_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩ෥")) and callable(getattr(RemoteConnection, bstack11lll1_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪ෦"))):
          bstack1ll111l111_opy_ = RemoteConnection._get_proxy_url
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          bstack1ll111l111_opy_ = ClientConfig.get_proxy_url
      except Exception as e:
        logger.error(bstack1l11l1ll1_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1l1l11l111_opy_ = Config.getoption
    from _pytest import runner
    bstack1l11l1llll_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warning(bstack11lll1_opy_ (u"ࠥࠩࡸࡀࠠࠦࡵࠥ෧"), bstack1111l11l_opy_, str(e))
  try:
    from pytest_bdd import reporting
    bstack1llll1111_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack11lll1_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡳࠥࡸࡵ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࡷࠬ෨"))
  if cli.is_enabled(CONFIG) and cli.config:
    bstack111l11l1l1_opy_ = cli.config.get(bstack11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ෩"), {}).get(bstack11lll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ෪"))
  else:
    bstack111l11l1l1_opy_ = CONFIG.get(bstack11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ෫"), {}).get(bstack11lll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ෬"))
  PARALLELISE_VANILLA_PYTHON = True
  if cli.is_enabled(CONFIG):
    if cli.bstack1llllll111_opy_():
      bstack11l1lll1_opy_.invoke(Events.CONNECT, bstack11ll1l111_opy_())
    platform_index = int(os.environ.get(bstack11lll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ෭"), bstack11lll1_opy_ (u"ࠪ࠴ࠬ෮")))
  else:
    bstack111l1ll1l1_opy_(bstack1l11l1l11l_opy_)
  os.environ[bstack11lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬ෯")] = CONFIG[bstack11lll1_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ෰")]
  os.environ[bstack11lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩ෱")] = CONFIG[bstack11lll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪෲ")]
  os.environ[bstack11lll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫෳ")] = BROWSERSTACK_AUTOMATION.__str__()
  from _pytest.config import main as bstack11ll1l1l11_opy_
  bstack11ll11lll1_opy_ = []
  try:
    exit_code = bstack11ll1l1l11_opy_(arg)
    if cli.is_enabled(CONFIG):
      cli.bstack11lll111l_opy_()
    if bstack11lll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠭෴") in multiprocessing.current_process().__dict__.keys():
      for bstack11111ll11_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack11ll11lll1_opy_.append(bstack11111ll11_opy_)
    try:
      bstack11l11lll1_opy_ = (bstack11ll11lll1_opy_, int(exit_code))
      bstack1l1llll11_opy_.append(bstack11l11lll1_opy_)
    except:
      bstack1l1llll11_opy_.append((bstack11ll11lll1_opy_, exit_code))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack11ll11lll1_opy_.append({bstack11lll1_opy_ (u"ࠪࡲࡦࡳࡥࠨ෵"): bstack11lll1_opy_ (u"ࠫࡕࡸ࡯ࡤࡧࡶࡷࠥ࠭෶") + os.environ.get(bstack11lll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ෷")), bstack11lll1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ෸"): traceback.format_exc(), bstack11lll1_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭෹"): int(os.environ.get(bstack11lll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ෺")))})
    bstack1l1llll11_opy_.append((bstack11ll11lll1_opy_, 1))
def mod_behave_main(args, retries):
  try:
    from behave.configuration import Configuration
    from behave.__main__ import run_behave
    from browserstack_sdk.bstack_behave_runner import BehaveRunner
    config = Configuration(args)
    config.update_userdata({bstack11lll1_opy_ (u"ࠤࡵࡩࡹࡸࡩࡦࡵࠥ෻"): str(retries)})
    return run_behave(config, runner_class=BehaveRunner)
  except Exception as e:
    bstack1ll1lll1ll_opy_ = e.__class__.__name__
    print(bstack11lll1_opy_ (u"ࠥࠩࡸࡀࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡵࡧࡶࡸࠥࠫࡳࠣ෼") % (bstack1ll1lll1ll_opy_, e))
    return 1
def bstack111ll11l1_opy_(arg):
  global bstack1l1l1lll11_opy_
  bstack111l1ll1l1_opy_(bstack1111l1111_opy_)
  os.environ[bstack11lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ෽")] = str(bstack1ll11l11_opy_)
  retries = bstack11lllllll_opy_.bstack1l1l1l11_opy_(CONFIG)
  status_code = 0
  if bstack11lllllll_opy_.bstack1l11ll111l_opy_(CONFIG):
    status_code = mod_behave_main(arg, retries)
  else:
    from behave.__main__ import main as bstack11ll1llll1_opy_
    status_code = bstack11ll1llll1_opy_(arg)
  if status_code != 0:
    bstack1l1l1lll11_opy_ = status_code
def bstack1lll1lllll_opy_():
  logger.info(bstack11111ll11l_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack11lll1_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ෾"), help=bstack11lll1_opy_ (u"࠭ࡇࡦࡰࡨࡶࡦࡺࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡤࡱࡱࡪ࡮࡭ࠧ෿"))
  parser.add_argument(bstack11lll1_opy_ (u"ࠧ࠮ࡷࠪ฀"), bstack11lll1_opy_ (u"ࠨ࠯࠰ࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬก"), help=bstack11lll1_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡵࡴࡧࡵࡲࡦࡳࡥࠨข"))
  parser.add_argument(bstack11lll1_opy_ (u"ࠪ࠱ࡰ࠭ฃ"), bstack11lll1_opy_ (u"ࠫ࠲࠳࡫ࡦࡻࠪค"), help=bstack11lll1_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡤࡧࡨ࡫ࡳࡴࠢ࡮ࡩࡾ࠭ฅ"))
  parser.add_argument(bstack11lll1_opy_ (u"࠭࠭ࡧࠩฆ"), bstack11lll1_opy_ (u"ࠧ࠮࠯ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬง"), help=bstack11lll1_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧจ"))
  bstack111llll11l_opy_ = parser.parse_args()
  try:
    bstack11l1l111l_opy_ = bstack11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡩࡨࡲࡪࡸࡩࡤ࠰ࡼࡱࡱ࠴ࡳࡢ࡯ࡳࡰࡪ࠭ฉ")
    if bstack111llll11l_opy_.framework and bstack111llll11l_opy_.framework not in (bstack11lll1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪช"), bstack11lll1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬซ")):
      bstack11l1l111l_opy_ = bstack11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠮ࡺ࡯࡯࠲ࡸࡧ࡭ࡱ࡮ࡨࠫฌ")
    bstack111ll11l1l_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11l1l111l_opy_)
    bstack11ll11ll1l_opy_ = open(bstack111ll11l1l_opy_, bstack11lll1_opy_ (u"࠭ࡲࠨญ"))
    bstack1l1l111ll_opy_ = bstack11ll11ll1l_opy_.read()
    bstack11ll11ll1l_opy_.close()
    if bstack111llll11l_opy_.username:
      bstack1l1l111ll_opy_ = bstack1l1l111ll_opy_.replace(bstack11lll1_opy_ (u"࡚ࠧࡑࡘࡖࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧฎ"), bstack111llll11l_opy_.username)
    if bstack111llll11l_opy_.key:
      bstack1l1l111ll_opy_ = bstack1l1l111ll_opy_.replace(bstack11lll1_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪฏ"), bstack111llll11l_opy_.key)
    if bstack111llll11l_opy_.framework:
      bstack1l1l111ll_opy_ = bstack1l1l111ll_opy_.replace(bstack11lll1_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪฐ"), bstack111llll11l_opy_.framework)
    file_name = bstack11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ฑ")
    file_path = os.path.abspath(file_name)
    bstack11lllllll1_opy_ = open(file_path, bstack11lll1_opy_ (u"ࠫࡼ࠭ฒ"))
    bstack11lllllll1_opy_.write(bstack1l1l111ll_opy_)
    bstack11lllllll1_opy_.close()
    logger.info(bstack11l11l1ll1_opy_)
    try:
      os.environ[bstack11lll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧณ")] = bstack111llll11l_opy_.framework if bstack111llll11l_opy_.framework != None else bstack11lll1_opy_ (u"ࠨࠢด")
      config = yaml.safe_load(bstack1l1l111ll_opy_)
      config[bstack11lll1_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧต")] = bstack11lll1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡵࡨࡸࡺࡶࠧถ")
      bstack1ll11l1111_opy_(bstack1l1l11l11_opy_, config)
    except Exception as e:
      logger.debug(bstack1l1ll1l1l1_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack11lll11111_opy_.format(str(e)))
def bstack1ll11l1111_opy_(bstack111l11lll1_opy_, config, bstack1ll11l1ll1_opy_=None, bstack1l111l11_opy_=False):
  global BROWSERSTACK_AUTOMATION
  global bstack1l11lllll1_opy_
  global global_config
  if not config:
    return
  if bstack1ll11l1ll1_opy_ is None:
    bstack1ll11l1ll1_opy_ = {}
  bstack11l11lll11_opy_ = bstack1l111lll1l_opy_ if not BROWSERSTACK_AUTOMATION else (
    bstack11lll1l11l_opy_ if bstack11lll1_opy_ (u"ࠩࡤࡴࡵ࠭ท") in config else (
        bstack1l1l11l1ll_opy_ if config.get(bstack11lll1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧธ")) else bstack11l11ll111_opy_
    )
)
  bstack111l1l111_opy_ = False
  bstack11llll1l1l_opy_ = False
  if BROWSERSTACK_AUTOMATION is True:
      if bstack11lll1_opy_ (u"ࠫࡦࡶࡰࠨน") in config:
          bstack111l1l111_opy_ = True
      else:
          bstack11llll1l1l_opy_ = True
  bstack1ll11l1l11_opy_ = TestHubUtils.bstack11lll11lll_opy_(config, bstack1l11lllll1_opy_)
  bstack1l1111lll_opy_ = bstack11l1ll1ll_opy_()
  data = {
    bstack11lll1_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧบ"): config[bstack11lll1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨป")],
    bstack11lll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪผ"): config[bstack11lll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫฝ")],
    bstack11lll1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭พ"): bstack111l11lll1_opy_,
    bstack11lll1_opy_ (u"ࠪࡨࡪࡺࡥࡤࡶࡨࡨࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧฟ"): os.environ.get(bstack11lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ภ"), bstack1l11lllll1_opy_),
    bstack11lll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧม"): bstack11l11l1l1l_opy_,
    bstack11lll1_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬ࠨย"): bstack1l1111l11l_opy_(),
    bstack11lll1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪร"): {
      bstack11lll1_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ฤ"): str(config[bstack11lll1_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩล")]) if bstack11lll1_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪฦ") in config else bstack11lll1_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧว"),
      bstack11lll1_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࡖࡦࡴࡶ࡭ࡴࡴࠧศ"): sys.version,
      bstack11lll1_opy_ (u"࠭ࡲࡦࡨࡨࡶࡷ࡫ࡲࠨษ"): bstack1lll111l1_opy_(os.environ.get(bstack11lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩส"), bstack1l11lllll1_opy_)),
      bstack11lll1_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪห"): bstack11lll1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩฬ"),
      bstack11lll1_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫอ"): bstack11l11lll11_opy_,
      bstack11lll1_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩฮ"): bstack1ll11l1l11_opy_,
      bstack11lll1_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡥࡵࡶ࡫ࡧࠫฯ"): os.environ[bstack11lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫะ")],
      bstack11lll1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪั"): os.environ.get(bstack11lll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪา"), bstack1l11lllll1_opy_),
      bstack11lll1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬำ"): bstack1llllll11_opy_(os.environ.get(bstack11lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬิ"), bstack1l11lllll1_opy_)),
      bstack11lll1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪี"): bstack1l1111lll_opy_.get(bstack11lll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪึ")),
      bstack11lll1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬื"): bstack1l1111lll_opy_.get(bstack11lll1_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨุ")),
      bstack11lll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨูࠫ"): config[bstack11lll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩฺࠬ")] if config[bstack11lll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭฻")] else bstack11lll1_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧ฼"),
      bstack11lll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ฽"): str(config[bstack11lll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ฾")]) if bstack11lll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ฿") in config else bstack11lll1_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤเ"),
      bstack11lll1_opy_ (u"ࠩࡲࡷࠬแ"): sys.platform,
      bstack11lll1_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬโ"): socket.gethostname(),
      bstack11lll1_opy_ (u"ࠫ࡮ࡹࡃࡍࡋࡈࡲࡦࡨ࡬ࡦࡦࠪใ"): bstack1l111l11_opy_,
      bstack11lll1_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪࠧไ"): global_config.get_property(bstack11lll1_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨๅ"))
    }
  }
  if not global_config.get_property(bstack11lll1_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡔ࡫ࡪࡲࡦࡲࠧๆ")) is None:
    data[bstack11lll1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫ็")][bstack11lll1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡑࡪࡺࡡࡥࡣࡷࡥ่ࠬ")] = {
      bstack11lll1_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰ้ࠪ"): bstack11lll1_opy_ (u"ࠫࡺࡹࡥࡳࡡ࡮࡭ࡱࡲࡥࡥ๊ࠩ"),
      bstack11lll1_opy_ (u"ࠬࡹࡩࡨࡰࡤࡰ๋ࠬ"): global_config.get_property(bstack11lll1_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭์")),
      bstack11lll1_opy_ (u"ࠧࡴ࡫ࡪࡲࡦࡲࡎࡶ࡯ࡥࡩࡷ࠭ํ"): global_config.get_property(bstack11lll1_opy_ (u"ࠨࡵࡧ࡯ࡐ࡯࡬࡭ࡐࡲࠫ๎"))
    }
  if bstack111l11lll1_opy_ == bstack1111ll1ll1_opy_:
    data[bstack11lll1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬ๏")][bstack11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡅࡲࡲ࡫࡯ࡧࠨ๐")] = bstack1l1ll11l1l_opy_(config)
    data[bstack11lll1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧ๑")][bstack11lll1_opy_ (u"ࠬ࡯ࡳࡑࡧࡵࡧࡾࡇࡵࡵࡱࡈࡲࡦࡨ࡬ࡦࡦࠪ๒")] = percy.bstack1ll1l11111_opy_
    data[bstack11lll1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩ๓")][bstack11lll1_opy_ (u"ࠧࡱࡧࡵࡧࡾࡈࡵࡪ࡮ࡧࡍࡩ࠭๔")] = percy.percy_build_id
  if not bstack11lllllll_opy_.bstack1l1ll11ll1_opy_(CONFIG):
    data[bstack11lll1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫ๕")][bstack11lll1_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠭๖")] = bstack11lllllll_opy_.bstack1l1ll11ll1_opy_(CONFIG)
  bstack111ll11lll_opy_ = bstack1l1l1ll1ll_opy_.get_instance(CONFIG, logger)
  bstack1111ll1l_opy_ = bstack11lllllll_opy_.get_instance(config=CONFIG)
  if bstack111ll11lll_opy_ is not None and bstack1111ll1l_opy_ is not None and bstack1111ll1l_opy_.bstack1l1lllll_opy_():
    data[bstack11lll1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭๗")][bstack1111ll1l_opy_.bstack11l1l11ll1_opy_()] = bstack111ll11lll_opy_.bstack1l111ll1ll_opy_()
  update(data[bstack11lll1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧ๘")], bstack1ll11l1ll1_opy_)
  try:
    response = bstack11l1lll11_opy_(bstack11lll1_opy_ (u"ࠬࡖࡏࡔࡖࠪ๙"), bstack1lllll1l11_opy_(bstack1l1l11ll_opy_), data, {
      bstack11lll1_opy_ (u"࠭ࡡࡶࡶ࡫ࠫ๚"): (config[bstack11lll1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ๛")], config[bstack11lll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ๜")])
    })
    if response:
      logger.debug(bstack1llll1llll_opy_.format(bstack111l11lll1_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack111lllll1_opy_.format(str(e)))
def bstack1lll111l1_opy_(framework):
  return bstack11lll1_opy_ (u"ࠤࡾࢁ࠲ࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࡿࢂࠨ๝").format(str(framework), __version__) if framework else bstack11lll1_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࡽࢀࠦ๞").format(
    __version__)
def bstack1l1l111l1l_opy_():
  global CONFIG
  global bstack11ll1111l1_opy_
  if bool(CONFIG):
    return
  try:
    bstack11l1llllll_opy_()
    logger.debug(bstack11l1ll11_opy_.format(str(CONFIG)))
    bstack11ll1111l1_opy_ = logger_utils.configure_logger(CONFIG, bstack11ll1111l1_opy_)
    bstack111l11l11l_opy_()
  except Exception as e:
    logger.error(bstack11lll1_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࡹࡵ࠲ࠠࡦࡴࡵࡳࡷࡀࠠࠣ๟") + str(e))
    sys.exit(1)
  sys.excepthook = bstack11l1lll1ll_opy_
  atexit.register(bstack1111l111l1_opy_)
  signal.signal(signal.SIGINT, bstack11l111l111_opy_)
  signal.signal(signal.SIGTERM, bstack11l111l111_opy_)
def bstack11l1lll1ll_opy_(exctype, value, traceback):
  global bstack1ll111ll1l_opy_
  try:
    for driver in bstack1ll111ll1l_opy_:
      bstack11111l11_opy_(driver, bstack11lll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ๠"), bstack11lll1_opy_ (u"ࠨࡓࡦࡵࡶ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤ๡") + str(value))
  except Exception:
    pass
  logger.info(bstack111ll1l1l_opy_)
  bstack1111l11ll_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1111l11ll_opy_(message=bstack11lll1_opy_ (u"ࠧࠨ๢"), bstack11l1l111ll_opy_ = False, bstack1l111l11_opy_ = False):
  global CONFIG
  bstack1l1llllll_opy_ = bstack11lll1_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡆࡺࡦࡩࡵࡺࡩࡰࡰࠪ๣") if bstack11l1l111ll_opy_ else bstack11lll1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ๤")
  bstack1lllll11_opy_ = bstack1llll11l_opy_.bstack11ll11l1l_opy_(EVENTS.bstack1111l11l11_opy_)
  try:
    if message:
      bstack1ll11l1ll1_opy_ = {
        bstack1l1llllll_opy_ : str(message)
      }
      try:
        bstack1ll11l1111_opy_(bstack1111ll1ll1_opy_, CONFIG, bstack1ll11l1ll1_opy_, bstack1l111l11_opy_)
      finally:
        bstack1llll11l_opy_.end(EVENTS.bstack1111l11l11_opy_.value, bstack1lllll11_opy_ + bstack11lll1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ๥"), bstack1lllll11_opy_ + bstack11lll1_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ๦"), status=True, failure=None, test_name=None)
    else:
      try:
        bstack1ll11l1111_opy_(bstack1111ll1ll1_opy_, CONFIG, bstack1l111l11_opy_=bstack1l111l11_opy_)
      finally:
        bstack1llll11l_opy_.end(EVENTS.bstack1111l11l11_opy_.value, bstack1lllll11_opy_ + bstack11lll1_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ๧"), bstack1lllll11_opy_ + bstack11lll1_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ๨"), status=True, failure=None, test_name=None)
  except Exception as e:
    logger.debug(bstack1l1l1l1111_opy_.format(str(e)))
def bstack1l11l11ll1_opy_(bstack1l1l11lll_opy_, size):
  bstack11ll1l1111_opy_ = []
  while len(bstack1l1l11lll_opy_) > size:
    bstack11l1111l_opy_ = bstack1l1l11lll_opy_[:size]
    bstack11ll1l1111_opy_.append(bstack11l1111l_opy_)
    bstack1l1l11lll_opy_ = bstack1l1l11lll_opy_[size:]
  bstack11ll1l1111_opy_.append(bstack1l1l11lll_opy_)
  return bstack11ll1l1111_opy_
def bstack11111lllll_opy_(args):
  if bstack11lll1_opy_ (u"ࠧ࠮࡯ࠪ๩") in args and bstack11lll1_opy_ (u"ࠨࡲࡧࡦࠬ๪") in args:
    return True
  return False
@measure(event_name=EVENTS.bstack11l111l1ll_opy_, stage=STAGE.bstack11111lll1_opy_)
def run_on_browserstack(bstack1111l111_opy_=None, bstack1l1llll11_opy_=None, bstack1ll11l111_opy_=False):
  global CONFIG
  global bstack1llllllll_opy_
  global bstack1ll11l11_opy_
  global bstack1l11lllll1_opy_
  global global_config
  bstack11llll1l11_opy_ = bstack11lll1_opy_ (u"ࠩࠪ๫")
  bstack11ll1l1ll_opy_ = bstack11lll1_opy_ (u"ࠥࠦ๬")
  bstack1ll1lll11l_opy_(bstack11l1lllll1_opy_, logger)
  if bstack1111l111_opy_ and isinstance(bstack1111l111_opy_, str):
    bstack1111l111_opy_ = eval(bstack1111l111_opy_)
  if bstack1111l111_opy_:
    CONFIG = bstack1111l111_opy_[bstack11lll1_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫ๭")]
    bstack1llllllll_opy_ = bstack1111l111_opy_[bstack11lll1_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭๮")]
    bstack1ll11l11_opy_ = bstack1111l111_opy_[bstack11lll1_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ๯")]
    global_config.bstack1111l11l1_opy_(bstack11lll1_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ๰"), bstack1ll11l11_opy_)
    bstack11llll1l11_opy_ = bstack11lll1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩ๱")
  global_config.bstack1111l11l1_opy_(bstack11lll1_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫ๲"), uuid4().__str__())
  logger.info(bstack11lll1_opy_ (u"ࠪࡗࡉࡑࠠࡳࡷࡱࠤࡸࡺࡡࡳࡶࡨࡨࠥࡽࡩࡵࡪࠣ࡭ࡩࡀࠠࠨ๳") + global_config.get_property(bstack11lll1_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭๴")));
  logger.debug(bstack11lll1_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪ࠽ࠨ๵") + global_config.get_property(bstack11lll1_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨ๶")))
  if not bstack1ll11l111_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1l1111l11_opy_)
      return
    if sys.argv[1] == bstack11lll1_opy_ (u"ࠧ࠮࠯ࡹࡩࡷࡹࡩࡰࡰࠪ๷") or sys.argv[1] == bstack11lll1_opy_ (u"ࠨ࠯ࡹࠫ๸"):
      logger.info(bstack11lll1_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡒࡼࡸ࡭ࡵ࡮ࠡࡕࡇࡏࠥࡼࡻࡾࠩ๹").format(__version__))
      return
    if sys.argv[1] == bstack11lll1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ๺"):
      bstack1lll1lllll_opy_()
      return
    if sys.argv[1] == bstack11lll1_opy_ (u"ࠫࡱࡵࡡࡥࠩ๻"):
      from browserstack_sdk.bstack1111111lll_opy_ import bstack11ll1l1l1_opy_
      bstack1l1l111l1l_opy_()
      bstack11ll1l1l1_opy_(CONFIG)
      return
  args = sys.argv
  bstack1l1l111l1l_opy_()
  global bstack1111lll1ll_opy_
  try:
    from bstack_utils import constants as bstack1l1lllll11_opy_
    override_value = CONFIG.get(bstack11lll1_opy_ (u"ࠬࡵࡶࡦࡴࡵ࡭ࡩ࡫ࡌࡰࡣࡧࡘࡪࡹࡴࡪࡰࡪࠫ๼"), False)
    bstack1111lll1ll_opy_ = bool(override_value)
  except Exception as e:
    logger.error(bstack11lll1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡓ࡛ࡋࡒࡓࡋࡇࡉࡤࡒࡏࡂࡆࡢࡘࡊ࡙ࡔࡊࡐࡊ࠾ࠥࢁࡽࠣ๽").format(e))
    bstack1111lll1ll_opy_ = False
  if bstack1111lll1ll_opy_:
    bstack1l1l1l1lll_opy_ = CONFIG.get(bstack11lll1_opy_ (u"ࠧ࡭ࡱࡤࡨ࡙࡫ࡳࡵ࡫ࡱ࡫ࡍࡻࡢࡖࡔࡏࠫ๾")) or bstack1l1lllll11_opy_.bstack1lllll11l_opy_
    logger.info(bstack11lll1_opy_ (u"ࠣࡉ࡯ࡳࡧࡧ࡬ࠡࡱࡹࡩࡷࡸࡩࡥࡧ࡯ࡳࡦࡪࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡦࡰࡤࡦࡱ࡫ࡤ࠭ࠢࡸࡷ࡮ࡴࡧࠡࡪࡸࡦ࠿ࠦࡻࡾࠤ๿").format(bstack1l1l1l1lll_opy_))
    bstack1llllllll_opy_ = bstack1l1l1l1lll_opy_
    try:
      bstack1l1lllll11_opy_.HTTPS_HUB = bstack1l1l1l1lll_opy_
      bstack1l1lllll11_opy_.bstack11l11lll_opy_ = bstack1l1l1l1lll_opy_
    except Exception:
      pass
  global bstack1l11ll11_opy_
  global bstack111l111ll_opy_
  global PARALLELISE_VANILLA_PYTHON
  global PARALLELISE_THREADING_PYTHON
  global PLATFORM_INDEX
  global bstack111l11l1l1_opy_
  global bstack1l1l1lll1l_opy_
  global bstack111l1llll_opy_
  global bstack11l1l1111_opy_
  global bstack1ll1l111l1_opy_
  global bstack1l1lllll1l_opy_
  bstack111l111ll_opy_ = len(CONFIG.get(bstack11lll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ຀"), []))
  if not bstack11llll1l11_opy_:
    if args[1] == bstack11lll1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪກ") or args[1] == bstack11lll1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬຂ") or args[1] == bstack11lll1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨ࠭຃"):
      bstack11llll1l11_opy_ = bstack11lll1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡧࡦࡰࡨࡶ࡮ࡩࠧຄ")
      args = args[2:]
    elif args[1] == bstack11lll1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭຅"):
      bstack11llll1l11_opy_ = bstack11lll1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧຆ")
      args = args[2:]
    elif args[1] == bstack11lll1_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨງ"):
      bstack11llll1l11_opy_ = bstack11lll1_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩຈ")
      args = args[2:]
    elif args[1] == bstack11lll1_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬຉ"):
      bstack11llll1l11_opy_ = bstack11lll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ຊ")
      args = args[2:]
    elif args[1] == bstack11lll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭຋"):
      bstack11llll1l11_opy_ = bstack11lll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧຌ")
      args = args[2:]
    elif args[1] == bstack11lll1_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨຍ"):
      bstack11llll1l11_opy_ = bstack11lll1_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩຎ")
      args = args[2:]
    else:
      if not bstack11lll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ຏ") in CONFIG or str(CONFIG[bstack11lll1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧຐ")]).lower() in [bstack11lll1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬຑ"), bstack11lll1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧຒ"), bstack11lll1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡨࡧࡱࡩࡷ࡯ࡣࠨຓ")]:
        bstack11llll1l11_opy_ = bstack11lll1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩດ")
        args = args[1:]
      elif str(CONFIG[bstack11lll1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬຕ")]).lower() == bstack11lll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩຖ"):
        bstack11llll1l11_opy_ = bstack11lll1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪທ")
        args = args[1:]
      elif str(CONFIG[bstack11lll1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨຘ")]).lower() == bstack11lll1_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬນ"):
        bstack11llll1l11_opy_ = bstack11lll1_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ບ")
        args = args[1:]
      elif str(CONFIG[bstack11lll1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫປ")]).lower() == bstack11lll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩຜ"):
        bstack11llll1l11_opy_ = bstack11lll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪຝ")
        args = args[1:]
      elif str(CONFIG[bstack11lll1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧພ")]).lower() == bstack11lll1_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬຟ"):
        bstack11llll1l11_opy_ = bstack11lll1_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ຠ")
        args = args[1:]
      else:
        os.environ[bstack11lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩມ")] = bstack11llll1l11_opy_
        bstack11l1111ll1_opy_(bstack1l111l11l_opy_)
  os.environ[bstack11lll1_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩຢ")] = bstack11llll1l11_opy_
  bstack1l11lllll1_opy_ = bstack11llll1l11_opy_
  if cli.is_enabled(CONFIG):
    try:
      if bstack11llll1l11_opy_ == bstack11lll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩຣ") and bstack1ll11lll_opy_():
        bstack1ll11l1l_opy_ = bstack1l1lll1l_opy_[bstack11lll1_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖ࠰ࡆࡉࡊࠧ຤")]
      elif bstack11llll1l11_opy_ in [bstack11lll1_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬລ"), bstack11lll1_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ຦")]:
        bstack1ll11l1l_opy_ = bstack11lll1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬວ")
      else:
        bstack1ll11l1l_opy_ = bstack11llll1l11_opy_
      bstack11l1lll1_opy_.invoke(Events.bstack1llll1111l_opy_, bstack1llll1l1l1_opy_(
        sdk_version=__version__,
        path_config=bstack1ll1111ll1_opy_(),
        path_project=os.getcwd(),
        test_framework=bstack1ll11l1l_opy_,
        frameworks=[bstack1ll11l1l_opy_],
        framework_versions={
          bstack1ll11l1l_opy_: bstack1llllll11_opy_(bstack11lll1_opy_ (u"ࠧࡓࡱࡥࡳࡹ࠭ຨ") if bstack11llll1l11_opy_ in [bstack11lll1_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧຩ"), bstack11lll1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨສ"), bstack11lll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫຫ")] else bstack11llll1l11_opy_)
        },
        bs_config=CONFIG
      ))
      if cli.config and cli.config.get(bstack11lll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࠨຬ"), None):
        CONFIG[bstack11lll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠢອ")] = cli.config.get(bstack11lll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣຮ"), None)
    except Exception as e:
      bstack11l1lll1_opy_.invoke(Events.bstack1lll1ll11_opy_, e.__traceback__, 1)
    if bstack1ll11l11_opy_:
      CONFIG[bstack11lll1_opy_ (u"ࠢࡢࡲࡳࠦຯ")] = cli.config[bstack11lll1_opy_ (u"ࠣࡣࡳࡴࠧະ")]
      logger.info(bstack11l1ll1l_opy_.format(CONFIG[bstack11lll1_opy_ (u"ࠩࡤࡴࡵ࠭ັ")]))
  else:
    bstack11l1lll1_opy_.clear()
  global bstack1l1111l1l_opy_
  global bstack1ll11l1ll_opy_
  if bstack1111l111_opy_:
    try:
      bstack111ll1l1_opy_ = datetime.datetime.now()
      os.environ[bstack11lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬາ")] = bstack11llll1l11_opy_
      bstack1ll11llll_opy_ = bstack1llll11l_opy_.bstack11ll11l1l_opy_(EVENTS.bstack111ll1111l_opy_)
      try:
        logger.info(bstack11lll1_opy_ (u"ࠦࡘ࡫࡮ࡥ࡫ࡱ࡫࡙ࠥࡄࡌࠢࡗࡩࡸࡺࠠࡂࡶࡷࡩࡲࡶࡴࡦࡦࠣࡩࡻ࡫࡮ࡵࠤຳ"))
        bstack1ll11l1111_opy_(bstack111lllll_opy_, CONFIG)
      finally:
        bstack1llll11l_opy_.end(EVENTS.bstack111ll1111l_opy_.value, bstack1ll11llll_opy_ + bstack11lll1_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧິ"), bstack1ll11llll_opy_ + bstack11lll1_opy_ (u"ࠨ࠺ࡦࡰࡧࠦີ"), status=True, failure=None, test_name=None)
      cli.bstack11l111ll1l_opy_(bstack11lll1_opy_ (u"ࠢࡩࡶࡷࡴ࠿ࡹࡤ࡬ࡡࡷࡩࡸࡺ࡟ࡢࡶࡷࡩࡲࡶࡴࡦࡦࠥຶ"), datetime.datetime.now() - bstack111ll1l1_opy_)
    except Exception as e:
      logger.debug(bstack11l1lll1l1_opy_.format(str(e)))
  global bstack1l11l11l_opy_
  global bstack1l1ll111l1_opy_
  global bstack1111l1l1_opy_
  global bstack11ll1llll_opy_
  global bstack11lll1llll_opy_
  global bstack11l11ll1l_opy_
  global bstack1llll1l11l_opy_
  global bstack11ll1111ll_opy_
  global bstack111111l1ll_opy_
  global bstack1l1llllll1_opy_
  global bstack111llll1ll_opy_
  global bstack1l1l11l1l_opy_
  global bstack11111l1l_opy_
  global bstack1lll1l1lll_opy_
  global bstack11l1l1l11_opy_
  global bstack11lll1ll1_opy_
  global bstack1ll111l111_opy_
  global bstack1l1l11l111_opy_
  global bstack1l11l1llll_opy_
  global bstack11llll11ll_opy_
  global bstack1llll1111_opy_
  global bstack1ll1ll1l_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l11l11l_opy_ = webdriver.Remote.__init__
    bstack1l1ll111l1_opy_ = WebDriver.quit
    bstack1l1l11l1l_opy_ = WebDriver.close
    bstack11lll1ll1_opy_ = WebDriver.get
    bstack1ll1ll1l_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1l1111l1l_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack1l1ll11lll_opy_
    bstack1ll11l1ll_opy_ = bstack1l1ll11lll_opy_()
  except Exception as e:
    pass
  try:
    global bstack111l11ll1l_opy_
    from QWeb.keywords import browser
    bstack111l11ll1l_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1l111l1111_opy_(CONFIG) and bstack1llllllll1_opy_():
    if bstack1ll11lll11_opy_() < version.parse(bstack1ll1l1l1ll_opy_):
      logger.error(bstack1l1l1lll_opy_.format(bstack1ll11lll11_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack11lll1_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩື")) and callable(getattr(RemoteConnection, bstack11lll1_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ຸࠪ"))):
          RemoteConnection._get_proxy_url = bstack1l1lll11ll_opy_
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          ClientConfig.get_proxy_url = bstack1l1lll11ll_opy_
      except Exception as e:
        logger.error(bstack1l11l1ll1_opy_.format(str(e)))
  if not CONFIG.get(bstack11lll1_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷູࠬ"), False) and not bstack1111l111_opy_:
    logger.info(bstack11l1l1111l_opy_)
  bstack1lllllllll_opy_ = not cli.is_enabled(CONFIG) and bstack11llll1l11_opy_ not in [bstack11lll1_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰ຺ࠬ")]
  bstack1111llll1l_opy_ = bstack1lllllllll_opy_ and bstack11lll1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩົ") in CONFIG and str(CONFIG[bstack11lll1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪຼ")]).lower() != bstack11lll1_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ຽ")
  bstack11ll111l11_opy_ = bstack1lllllllll_opy_ and not bstack1111llll1l_opy_ and (bstack11llll1l11_opy_ != bstack11lll1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩ຾") or (bstack11llll1l11_opy_ == bstack11lll1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠪ຿") and not bstack1111l111_opy_))
  if bstack11llll1l11_opy_ not in [bstack11lll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫເ")]:
    bstack1ll1lll11l_opy_(os.path.join(os.getcwd(), bstack11lll1_opy_ (u"ࠫࡱࡵࡧࠨແ"), bstack11lll1_opy_ (u"ࠬࡱࡥࡺ࠯ࡰࡩࡹࡸࡩࡤࡵ࠱࡮ࡸࡵ࡮ࠨໂ")), logger)
  if (bstack11llll1l11_opy_ in [bstack11lll1_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬໃ"), bstack11lll1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ໄ"), bstack11lll1_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ໅")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      try:
        from pabot.pabot import QueueItem
        from pabot import pabot
      except Exception as e:
        logger.warning(bstack1l1ll1lll1_opy_ + str(e))
      if not is_robot_playwright_installed():
        try:
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
          WebDriverCreator._get_ff_profile = bstack1111l111l_opy_
          bstack11l11ll1l_opy_ = WebDriverCache.close
        except Exception as e:
          logger.warning(bstack111l1llll1_opy_ + str(e))
        try:
          from AppiumLibrary.utils.applicationcache import ApplicationCache
          bstack11lll1llll_opy_ = ApplicationCache.close
        except Exception as e:
          logger.debug(bstack1l111llll1_opy_ + str(e))
    except Exception as e:
      bstack11l1l11111_opy_(e, bstack111l1llll1_opy_)
    if bstack11llll1l11_opy_ != bstack11lll1_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪໆ"):
      bstack1ll1llll11_opy_()
    bstack1111l1l1_opy_ = Output.start_test
    bstack11ll1llll_opy_ = Output.end_test
    bstack1llll1l11l_opy_ = TestStatus.__init__
    bstack111111l1ll_opy_ = pabot._run
    bstack1l1llllll1_opy_ = QueueItem.__init__
    bstack111llll1ll_opy_ = pabot._create_command_for_execution
    bstack11llll11ll_opy_ = pabot._report_results
  if bstack11llll1l11_opy_ == bstack11lll1_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ໇"):
    global bstack11ll1ll11l_opy_
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11l1l11111_opy_(e, bstack11l1lll1l_opy_)
    bstack11111l1l_opy_ = Runner.run_hook
    bstack1lll1l1lll_opy_ = Runner.load_hooks
    bstack11l1l1l11_opy_ = Step.run
    try:
      sig = inspect.signature(bstack11111l1l_opy_)
      params = list(sig.parameters.keys())
      bstack11ll1ll11l_opy_ = bstack11lll1_opy_ (u"ࠫࡨࡵ࡮ࡵࡧࡻࡸ່ࠬ") in params
      logger.info(bstack11lll1_opy_ (u"ࠬࡊࡥࡵࡧࡦࡸࡪࡪࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡳࡷࡱࡣ࡭ࡵ࡯࡬ࠢࡶ࡭࡬ࡴࡡࡵࡷࡵࡩ࠿ࠦࡻࡾ້ࠩ").format(bstack11lll1_opy_ (u"࠭࠱࠯࠴࠱࠺ࠥ࠮ࡷࡪࡶ࡫ࠤࡨࡵ࡮ࡵࡧࡻࡸ࠮໊࠭") if bstack11ll1ll11l_opy_ else bstack11lll1_opy_ (u"ࠧ࠲࠰࠶࠯ࠥ࠮ࡷࡪࡶ࡫ࡳࡺࡺࠠࡤࡱࡱࡸࡪࡾࡴ໋ࠪࠩ")))
    except Exception as e:
      logger.debug(bstack11lll1_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡥࡷࠤࡧ࡫ࡨࡢࡸࡨࠤࡷࡻ࡮ࡠࡪࡲࡳࡰࠦࡳࡪࡩࡱࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭໌").format(str(e)))
      bstack11ll1ll11l_opy_ = None
  if bstack11llll1l11_opy_ == bstack11lll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩໍ"):
    try:
      from _pytest.config import Config
      bstack1l1l11l111_opy_ = Config.getoption
      from _pytest import runner
      bstack1l11l1llll_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warning(bstack11lll1_opy_ (u"ࠥࠩࡸࡀࠠࠦࡵࠥ໎"), bstack1111l11l_opy_, str(e))
    try:
      from pytest_bdd import reporting
      bstack1llll1111_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack11lll1_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡳࠥࡸࡵ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࡷࠬ໏"))
    if bstack1ll1ll1l11_opy_():
      logger.warning(bstack111l11ll11_opy_[bstack11lll1_opy_ (u"࡙ࠬࡄࡌ࠯ࡊࡉࡓ࠳࠰࠱࠷ࠪ໐")])
  try:
    framework_name = bstack11lll1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ໑") if bstack11llll1l11_opy_ in [bstack11lll1_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭໒"), bstack11lll1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ໓"), bstack11lll1_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ໔")] else bstack1l1l1111_opy_(bstack11llll1l11_opy_)
    bstack1l11l11l1l_opy_ = {
      bstack11lll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࠫ໕"): bstack11lll1_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷ࠱ࡨࡻࡣࡶ࡯ࡥࡩࡷ࠭໖") if bstack11llll1l11_opy_ == bstack11lll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ໗") and bstack1ll11lll_opy_() else framework_name,
      bstack11lll1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ໘"): bstack1llllll11_opy_(framework_name),
      bstack11lll1_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ໙"): __version__,
      bstack11lll1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡺࡹࡥࡥࠩ໚"): bstack11llll1l11_opy_
    }
    if bstack11llll1l11_opy_ in bstack111l11111_opy_ + bstack1ll1l1ll1_opy_:
      if a11y.is_enabled_root(CONFIG):
        if bstack11lll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ໛") in CONFIG:
          os.environ[bstack11lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫໜ")] = os.getenv(bstack11lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬໝ"), json.dumps(CONFIG[bstack11lll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬໞ")]))
          CONFIG[bstack11lll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ໟ")].pop(bstack11lll1_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬ໠"), None)
          CONFIG[bstack11lll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ໡")].pop(bstack11lll1_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ໢"), None)
        bstack11llll1ll1_opy_ = bstack11lll1_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧ໣") if CONFIG.get(bstack11lll1_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪ໤")) or bstack111111l11_opy_() else bstack11lll1_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧ໥")
        if bstack11llll1ll1_opy_ == bstack11lll1_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪ໦"):
          try:
            import importlib.metadata as _1lll11l11_opy_
            bstack111ll1l1ll_opy_ = _1lll11l11_opy_.version(bstack11lll1_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦ໧"))
          except Exception:
            bstack111ll1l1ll_opy_ = bstack11lll1_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࠩ໨")
        else:
          bstack111ll1l1ll_opy_ = str(bstack1ll11lll11_opy_())
        bstack1l11l11l1l_opy_[bstack11lll1_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ໩")] = {
          bstack11lll1_opy_ (u"ࠪࡲࡦࡳࡥࠨ໪"): bstack11llll1ll1_opy_,
          bstack11lll1_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬ໫"): bstack111ll1l1ll_opy_
        }
    bstack11l11ll11_opy_, bstack1l11l1ll_opy_ = None, {}
    bstack1llllll1l_opy_ = None
    bstack11ll1ll1_opy_ = None
    def bstack11l1l11l1l_opy_():
      if bstack1111llll1l_opy_:
        bstack1ll1ll11ll_opy_()
      elif bstack11ll111l11_opy_:
        bstack11llllllll_opy_()
    def bstack11l11ll1l1_opy_():
      nonlocal bstack11l11ll11_opy_, bstack1l11l1ll_opy_
      if bstack11llll1l11_opy_ not in [bstack11lll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭໬")] and not cli.is_running():
        bstack11l11ll11_opy_, bstack1l11l1ll_opy_ = TestHubHandler.launch(CONFIG, bstack1l11l11l1l_opy_)
    if bstack1111llll1l_opy_ or bstack11ll111l11_opy_:
      bstack1llllll1l_opy_ = threading.Thread(target=bstack11l1l11l1l_opy_)
      bstack1llllll1l_opy_.start()
    if bstack11llll1l11_opy_ not in [bstack11lll1_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧ໭")] and not cli.is_running():
      bstack11ll1ll1_opy_ = threading.Thread(target=bstack11l11ll1l1_opy_)
      bstack11ll1ll1_opy_.start()
    if bstack1llllll1l_opy_:
      bstack1llllll1l_opy_.join()
    if bstack11ll1ll1_opy_:
      bstack11ll1ll1_opy_.join()
    if bstack1l11l1ll_opy_.get(bstack11lll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ໮")) is not None and a11y.bstack111ll11l11_opy_(CONFIG) is None:
      value = bstack1l11l1ll_opy_[bstack11lll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ໯")].get(bstack11lll1_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪ໰"))
      if value is not None:
          CONFIG[bstack11lll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ໱")] = value
      else:
        logger.debug(bstack11lll1_opy_ (u"ࠦࡓࡵࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡥࡣࡷࡥࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡳࡧࡶࡴࡴࡴࡳࡦࠤ໲"))
  except Exception as e:
    logger.debug(bstack1l111111l1_opy_.format(bstack11lll1_opy_ (u"࡚ࠬࡥࡴࡶࡋࡹࡧ࠭໳"), str(e)))
  if bstack11llll1l11_opy_ == bstack11lll1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡧࡦࡰࡨࡶ࡮ࡩࠧ໴"):
    PARALLELISE_VANILLA_PYTHON = True
    if bstack1111l111_opy_ and bstack1ll11l111_opy_:
      if cli.is_enabled(CONFIG):
        bstack111l11l1l1_opy_ = cli.config.get(bstack11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ໵"), {}).get(bstack11lll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ໶")) if cli.config else None
      else:
        bstack111l11l1l1_opy_ = CONFIG.get(bstack11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭໷"), {}).get(bstack11lll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ໸"))
      bstack111l1ll1l1_opy_(bstack11l11111l1_opy_)
    elif bstack1111l111_opy_:
      if cli.is_enabled(CONFIG):
        bstack111l11l1l1_opy_ = cli.config.get(bstack11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ໹"), {}).get(bstack11lll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ໺")) if cli.config else None
      else:
        bstack111l11l1l1_opy_ = CONFIG.get(bstack11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ໻"), {}).get(bstack11lll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ໼"))
      global bstack1ll111ll1l_opy_
      try:
        if bstack11111lllll_opy_(bstack1111l111_opy_[bstack11lll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ໽")]) and multiprocessing.current_process().name == bstack11lll1_opy_ (u"ࠩ࠳ࠫ໾"):
          bstack1111l111_opy_[bstack11lll1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭໿")].remove(bstack11lll1_opy_ (u"ࠫ࠲ࡳࠧༀ"))
          bstack1111l111_opy_[bstack11lll1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ༁")].remove(bstack11lll1_opy_ (u"࠭ࡰࡥࡤࠪ༂"))
          bstack1111l111_opy_[bstack11lll1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ༃")] = bstack1111l111_opy_[bstack11lll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ༄")][0]
          with open(bstack1111l111_opy_[bstack11lll1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ༅")], bstack11lll1_opy_ (u"ࠪࡶࠬ༆")) as f:
            file_content = f.read()
          bstack1l1lll1l11_opy_ = bstack11lll1_opy_ (u"ࠦࠧࠨࡦࡳࡱࡰࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡷࡩࡱࠠࡪ࡯ࡳࡳࡷࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡧ࠾ࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿ࡫ࠨࡼࡿࠬ࠿ࠥ࡬ࡲࡰ࡯ࠣࡴࡩࡨࠠࡪ࡯ࡳࡳࡷࡺࠠࡑࡦࡥ࠿ࠥࡵࡧࡠࡦࡥࠤࡂࠦࡐࡥࡤ࠱ࡨࡴࡥࡢࡳࡧࡤ࡯ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡧࡩ࡫ࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠪࡶࡩࡱ࡬ࠬࠡࡣࡵ࡫࠱ࠦࡴࡦ࡯ࡳࡳࡷࡧࡲࡺࠢࡀࠤ࠵࠯࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡴࡳࡻ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡦࡸࡧࠡ࠿ࠣࡷࡹࡸࠨࡪࡰࡷࠬࡦࡸࡧࠪ࠭࠴࠴࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡪࡾࡣࡦࡲࡷࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡢࡵࠣࡩ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡰࡢࡵࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡲ࡫ࡤࡪࡢࠩࡵࡨࡰ࡫࠲ࡡࡳࡩ࠯ࡸࡪࡳࡰࡰࡴࡤࡶࡾ࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡔࡩࡨ࠮ࡥࡱࡢࡦࠥࡃࠠ࡮ࡱࡧࡣࡧࡸࡥࡢ࡭ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡐࡥࡤ࠱ࡨࡴࡥࡢࡳࡧࡤ࡯ࠥࡃࠠ࡮ࡱࡧࡣࡧࡸࡥࡢ࡭ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡐࡥࡤࠫ࠭࠳ࡹࡥࡵࡡࡷࡶࡦࡩࡥࠩࠫ࡟ࡲࠧࠨࠢ༇").format(str(bstack1111l111_opy_))
          bstack111llllll_opy_ = bstack1l1lll1l11_opy_ + file_content
          bstack11l1l11lll_opy_ = bstack1111l111_opy_[bstack11lll1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ༈")] + bstack11lll1_opy_ (u"࠭࡟ࡣࡵࡷࡥࡨࡱ࡟ࡵࡧࡰࡴ࠳ࡶࡹࠨ༉")
          with open(bstack11l1l11lll_opy_, bstack11lll1_opy_ (u"ࠧࡸࠩ༊")):
            pass
          with open(bstack11l1l11lll_opy_, bstack11lll1_opy_ (u"ࠣࡹ࠮ࠦ་")) as f:
            f.write(bstack111llllll_opy_)
          import subprocess
          bstack111l1ll111_opy_ = subprocess.run([bstack11lll1_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࠤ༌"), bstack11l1l11lll_opy_])
          if os.path.exists(bstack11l1l11lll_opy_):
            os.unlink(bstack11l1l11lll_opy_)
          os._exit(bstack111l1ll111_opy_.returncode)
        else:
          if bstack11111lllll_opy_(bstack1111l111_opy_[bstack11lll1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭།")]):
            bstack1111l111_opy_[bstack11lll1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ༎")].remove(bstack11lll1_opy_ (u"ࠬ࠳࡭ࠨ༏"))
            bstack1111l111_opy_[bstack11lll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ༐")].remove(bstack11lll1_opy_ (u"ࠧࡱࡦࡥࠫ༑"))
            bstack1111l111_opy_[bstack11lll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ༒")] = bstack1111l111_opy_[bstack11lll1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ༓")][0]
          bstack111l1ll1l1_opy_(bstack11l11111l1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1111l111_opy_[bstack11lll1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭༔")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack11lll1_opy_ (u"ࠫࡤࡥ࡮ࡢ࡯ࡨࡣࡤ࠭༕")] = bstack11lll1_opy_ (u"ࠬࡥ࡟࡮ࡣ࡬ࡲࡤࡥࠧ༖")
          mod_globals[bstack11lll1_opy_ (u"࠭࡟ࡠࡨ࡬ࡰࡪࡥ࡟ࠨ༗")] = os.path.abspath(bstack1111l111_opy_[bstack11lll1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧ༘ࠪ")])
          exec(open(bstack1111l111_opy_[bstack11lll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨ༙ࠫ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack11lll1_opy_ (u"ࠩࡆࡥࡺ࡭ࡨࡵࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠩ༚").format(str(e)))
          for driver in bstack1ll111ll1l_opy_:
            bstack1l1llll11_opy_.append({
              bstack11lll1_opy_ (u"ࠪࡲࡦࡳࡥࠨ༛"): bstack1111l111_opy_[bstack11lll1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ༜")],
              bstack11lll1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ༝"): str(e),
              bstack11lll1_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ༞"): multiprocessing.current_process().name
            })
            bstack11111l11_opy_(driver, bstack11lll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ༟"), bstack11lll1_opy_ (u"ࠣࡕࡨࡷࡸ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦ༠") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1ll111ll1l_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1ll11l11_opy_, CONFIG, logger)
      bstack11llll1111_opy_()
      bstack111l11l111_opy_()
      percy.bstack1l1l1111ll_opy_()
      bstack1llll1l11_opy_ = {
        bstack11lll1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ༡"): args[0],
        bstack11lll1_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪ༢"): CONFIG,
        bstack11lll1_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬ༣"): bstack1llllllll_opy_,
        bstack11lll1_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ༤"): bstack1ll11l11_opy_
      }
      if bstack11lll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ༥") in CONFIG:
        bstack1ll1llll_opy_ = bstack1l11ll1l11_opy_(args, logger, CONFIG, BROWSERSTACK_AUTOMATION, bstack111l111ll_opy_)
        bstack111l1llll_opy_ = bstack1ll1llll_opy_.bstack1l1ll111l_opy_(run_on_browserstack, bstack1llll1l11_opy_, bstack11111lllll_opy_(args))
      else:
        if bstack11111lllll_opy_(args):
          bstack1llll1l11_opy_[bstack11lll1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ༦")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1llll1l11_opy_,))
          test.start()
          test.join()
        else:
          bstack111l1ll1l1_opy_(bstack11l11111l1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack11lll1_opy_ (u"ࠨࡡࡢࡲࡦࡳࡥࡠࡡࠪ༧")] = bstack11lll1_opy_ (u"ࠩࡢࡣࡲࡧࡩ࡯ࡡࡢࠫ༨")
          mod_globals[bstack11lll1_opy_ (u"ࠪࡣࡤ࡬ࡩ࡭ࡧࡢࡣࠬ༩")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack11llll1l11_opy_ == bstack11lll1_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ༪") or bstack11llll1l11_opy_ == bstack11lll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ༫"):
    percy.init(bstack1ll11l11_opy_, CONFIG, logger)
    percy.bstack1l1l1111ll_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack11l1l11111_opy_(e, bstack111l1llll1_opy_)
    bstack11llll1111_opy_()
    bstack111l1ll1l1_opy_(bstack1lll1ll1l_opy_)
    if BROWSERSTACK_AUTOMATION:
      bstack11ll1l1l_opy_(bstack1lll1ll1l_opy_, args)
      if bstack11lll1_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ༬") in args:
        i = args.index(bstack11lll1_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ༭"))
        args.pop(i)
        args.pop(i)
      if bstack11lll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ༮") not in CONFIG:
        CONFIG[bstack11lll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ༯")] = [{}]
        bstack111l111ll_opy_ = 1
      if bstack1l11ll11_opy_ == 0:
        bstack1l11ll11_opy_ = 1
      args.insert(0, str(bstack1l11ll11_opy_))
      args.insert(0, str(bstack11lll1_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨ༰")))
    if TestHubHandler.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1lll1l11ll_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1111ll1l1l_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack11lll1_opy_ (u"ࠦࡗࡕࡂࡐࡖࡢࡓࡕ࡚ࡉࡐࡐࡖࠦ༱"),
        ).parse_args(bstack1lll1l11ll_opy_)
        bstack1111lllll_opy_ = args.index(bstack1lll1l11ll_opy_[0]) if len(bstack1lll1l11ll_opy_) > 0 else len(args)
        args.insert(bstack1111lllll_opy_, str(bstack11lll1_opy_ (u"ࠬ࠳࠭࡭࡫ࡶࡸࡪࡴࡥࡳࠩ༲")))
        args.insert(bstack1111lllll_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11lll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡲࡰࡤࡲࡸࡤࡲࡩࡴࡶࡨࡲࡪࡸ࠮ࡱࡻࠪ༳"))))
        if bstack11lllllll_opy_.bstack1l11ll111l_opy_(CONFIG):
          args.insert(bstack1111lllll_opy_, str(bstack11lll1_opy_ (u"ࠧ࠮࠯࡯࡭ࡸࡺࡥ࡯ࡧࡵࠫ༴")))
          args.insert(bstack1111lllll_opy_ + 1, str(bstack11lll1_opy_ (u"ࠨࡔࡨࡸࡷࡿࡆࡢ࡫࡯ࡩࡩࡀࡻࡾ༵ࠩ").format(bstack11lllllll_opy_.bstack1l1l1l11_opy_(CONFIG))))
        if bstack1lll11l1_opy_(os.environ.get(bstack11lll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠧ༶"))) and str(os.environ.get(bstack11lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙༷ࠧ"), bstack11lll1_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ༸"))) != bstack11lll1_opy_ (u"ࠬࡴࡵ࡭࡮༹ࠪ"):
          for bstack1llll111l_opy_ in bstack1111ll1l1l_opy_:
            args.remove(bstack1llll111l_opy_)
          test_files = os.environ.get(bstack11lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࡣ࡙ࡋࡓࡕࡕࠪ༺")).split(bstack11lll1_opy_ (u"ࠧ࠭ࠩ༻"))
          for bstack111l11l1ll_opy_ in test_files:
            args.append(bstack111l11l1ll_opy_)
      except Exception as e:
        logger.error(bstack11lll1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡡࡵࡶࡤࡧ࡭࡯࡮ࡨࠢ࡯࡭ࡸࡺࡥ࡯ࡧࡵࠤ࡫ࡵࡲࠡࡽࢀ࠲ࠥࡋࡲࡳࡱࡵࠤ࠲ࠦࡻࡾࠤ༼").format(bstack1ll11ll11l_opy_, e))
    pabot.main(args)
  elif bstack11llll1l11_opy_ == bstack11lll1_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ༽"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack11l1l11111_opy_(e, bstack111l1llll1_opy_)
    for a in args:
      if bstack11lll1_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡓࡐࡆ࡚ࡆࡐࡔࡐࡍࡓࡊࡅ࡙ࠩ༾") in a:
        PLATFORM_INDEX = int(a.split(bstack11lll1_opy_ (u"ࠫ࠿࠭༿"))[1])
      if bstack11lll1_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡉࡋࡆࡍࡑࡆࡅࡑࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩཀ") in a:
        bstack111l11l1l1_opy_ = str(a.split(bstack11lll1_opy_ (u"࠭࠺ࠨཁ"))[1])
      if bstack11lll1_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙ࠧག") in a:
        bstack1l1l1lll1l_opy_ = str(a.split(bstack11lll1_opy_ (u"ࠨ࠼ࠪགྷ"))[1])
    bstack1111lll111_opy_ = None
    bstack11l11ll11l_opy_ = None
    if bstack11lll1_opy_ (u"ࠩ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠨང") in args:
      i = args.index(bstack11lll1_opy_ (u"ࠪ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠩཅ"))
      args.pop(i)
      bstack1111lll111_opy_ = args.pop(i)
    if bstack11lll1_opy_ (u"ࠫ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࠧཆ") in args:
      i = args.index(bstack11lll1_opy_ (u"ࠬ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸࠨཇ"))
      args.pop(i)
      bstack11l11ll11l_opy_ = args.pop(i)
    if bstack1111lll111_opy_ is not None:
      global bstack1l11l1l1l_opy_
      bstack1l11l1l1l_opy_ = bstack1111lll111_opy_
    if bstack11l11ll11l_opy_ is not None and int(PLATFORM_INDEX) < 0:
      PLATFORM_INDEX = int(bstack11l11ll11l_opy_)
    if cli.is_enabled(CONFIG):
      if cli.bstack1llllll111_opy_():
        bstack11l1lll1_opy_.invoke(Events.CONNECT, bstack11ll1l111_opy_())
        cli.bstack1ll1ll11_opy_(PLATFORM_INDEX)
      if cli.bstack11ll111l1_opy_(bstack11lll11ll_opy_):
        cli.bstack1l1l11lll1_opy_()
    bstack111l1ll1l1_opy_(bstack1lll1ll1l_opy_)
    run_cli(args)
    if bstack11lll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶࠪ཈") in multiprocessing.current_process().__dict__.keys():
      for bstack11111ll11_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1l1llll11_opy_.append(bstack11111ll11_opy_)
  elif bstack11llll1l11_opy_ == bstack11lll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧཉ"):
    bstack1l11l1l11_opy_ = bstack1llll11ll_opy_(args, logger, CONFIG, BROWSERSTACK_AUTOMATION)
    bstack1l11l1l11_opy_.bstack11lll1ll11_opy_()
    bstack11llll1111_opy_()
    PARALLELISE_THREADING_PYTHON = True
    bstack1ll1l111l1_opy_ = bstack1l11l1l11_opy_.bstack11ll111111_opy_()
    bstack1l11l1l11_opy_.bstack1llll1l11_opy_(bstack1ll1l11l_opy_)
    bstack1l11l1l11_opy_.bstack1l11l11l11_opy_()
    bstack1l11ll111_opy_(bstack11llll1l11_opy_, CONFIG, bstack1l11l1l11_opy_.bstack11lll11ll1_opy_())
    bstack1lll11lll_opy_.end(EVENTS.bstack11l111l1ll_opy_.value, EVENTS.bstack11l111l1ll_opy_.value + bstack11lll1_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣཊ"), EVENTS.bstack11l111l1ll_opy_.value + bstack11lll1_opy_ (u"ࠤ࠽ࡩࡳࡪࠢཋ"), status=True, failure=None, test_name=SESSION_NAME)
    bstack1ll1l1l1_opy_ = bstack1l11l1l11_opy_.bstack1l1ll111l_opy_(bstack1111ll11ll_opy_, {
      bstack11lll1_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪཌ"): CONFIG,
      bstack11lll1_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬཌྷ"): bstack1llllllll_opy_,
      bstack11lll1_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧཎ"): bstack1ll11l11_opy_,
      bstack11lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩཏ"): BROWSERSTACK_AUTOMATION,
      bstack11lll1_opy_ (u"ࠧࡐࡘࡈࡖࡗࡏࡄࡆࡡࡏࡓࡆࡊ࡟ࡕࡇࡖࡘࡎࡔࡇࠨཐ"): bstack1111lll1ll_opy_
    })
    if not bstack1111l111_opy_:
      bstack11ll1l1ll_opy_ = bstack1llll11l_opy_.bstack11ll11l1l_opy_(EVENTS.bstack1lll11l1l_opy_.value)
    try:
      bstack11ll11lll1_opy_, bstack111l11l11_opy_ = map(list, zip(*bstack1ll1l1l1_opy_))
      bstack11l1l1111_opy_ = bstack11ll11lll1_opy_[0]
      for status_code in bstack111l11l11_opy_:
        if status_code != 0:
          bstack1l1lllll1l_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack11lll1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡧࡶࡦࠢࡨࡶࡷࡵࡲࡴࠢࡤࡲࡩࠦࡳࡵࡣࡷࡹࡸࠦࡣࡰࡦࡨ࠲ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࠼ࠣࡿࢂࠨད").format(str(e)))
  elif bstack11llll1l11_opy_ == bstack11lll1_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩདྷ"):
    try:
      from behave.__main__ import main as bstack11ll1llll1_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack11l1l11111_opy_(e, bstack11l1lll1l_opy_)
    bstack11llll1111_opy_()
    PARALLELISE_THREADING_PYTHON = True
    bstack1l111l111_opy_ = 1
    if bstack11lll1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪན") in CONFIG:
      bstack1l111l111_opy_ = CONFIG[bstack11lll1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫཔ")]
    if bstack11lll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨཕ") in CONFIG:
      bstack1ll11lll1_opy_ = int(bstack1l111l111_opy_) * int(len(CONFIG[bstack11lll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩབ")]))
    else:
      bstack1ll11lll1_opy_ = int(bstack1l111l111_opy_)
    config = Configuration(args)
    bstack1l111l11l1_opy_ = config.paths
    if len(bstack1l111l11l1_opy_) == 0:
      import glob
      pattern = bstack11lll1_opy_ (u"ࠧࠫࠬ࠲࠮࠳࡬ࡥࡢࡶࡸࡶࡪ࠭བྷ")
      bstack1lll111lll_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1lll111lll_opy_)
      config = Configuration(args)
      bstack1l111l11l1_opy_ = config.paths
    bstack111lll1ll_opy_ = [os.path.normpath(item) for item in bstack1l111l11l1_opy_]
    bstack111l111ll1_opy_ = [os.path.normpath(item) for item in args]
    bstack1l1ll1111_opy_ = [item for item in bstack111l111ll1_opy_ if item not in bstack111lll1ll_opy_]
    import platform as pf
    if pf.system().lower() == bstack11lll1_opy_ (u"ࠨࡹ࡬ࡲࡩࡵࡷࡴࠩམ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack111lll1ll_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1llll111l1_opy_)))
                    for bstack1llll111l1_opy_ in bstack111lll1ll_opy_]
    bstack1ll111lll_opy_ = []
    for spec in bstack111lll1ll_opy_:
      bstack1111l1ll1_opy_ = []
      bstack1111l1ll1_opy_ += bstack1l1ll1111_opy_
      bstack1111l1ll1_opy_.append(spec)
      bstack1ll111lll_opy_.append(bstack1111l1ll1_opy_)
    execution_items = []
    for bstack1111l1ll1_opy_ in bstack1ll111lll_opy_:
      if bstack11lll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬཙ") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack11lll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ཚ")]):
          item = {}
          item[bstack11lll1_opy_ (u"ࠫࡦࡸࡧࠨཛ")] = bstack11lll1_opy_ (u"ࠬࠦࠧཛྷ").join(bstack1111l1ll1_opy_)
          item[bstack11lll1_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬཝ")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack11lll1_opy_ (u"ࠧࡢࡴࡪࠫཞ")] = bstack11lll1_opy_ (u"ࠨࠢࠪཟ").join(bstack1111l1ll1_opy_)
        item[bstack11lll1_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨའ")] = 0
        execution_items.append(item)
    bstack1l1ll1111l_opy_ = bstack1l11l11ll1_opy_(execution_items, bstack1ll11lll1_opy_)
    for execution_item in bstack1l1ll1111l_opy_:
      bstack1ll1l111ll_opy_ = []
      for item in execution_item:
        bstack1ll1l111ll_opy_.append(bstack11ll11l111_opy_(name=str(item[bstack11lll1_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩཡ")]),
                                             target=bstack111ll11l1_opy_,
                                             args=(item[bstack11lll1_opy_ (u"ࠫࡦࡸࡧࠨར")],)))
      for t in bstack1ll1l111ll_opy_:
        t.start()
      for t in bstack1ll1l111ll_opy_:
        t.join()
  else:
    bstack11l1111ll1_opy_(bstack1l111l11l_opy_)
  if not bstack1111l111_opy_:
    bstack1ll1l111_opy_()
    if bstack11ll1l1ll_opy_:
      bstack1llll11l_opy_.end(EVENTS.bstack1lll11l1l_opy_.value, bstack11ll1l1ll_opy_ + bstack11lll1_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧལ"), bstack11ll1l1ll_opy_ + bstack11lll1_opy_ (u"ࠨ࠺ࡦࡰࡧࠦཤ"), status=True, failure=None, test_name=None)
  logger_utils.bstack111l1ll1l_opy_()
def browserstack_initialize(bstack11l1llll11_opy_=None):
  logger.info(bstack11lll1_opy_ (u"ࠧࡓࡷࡱࡲ࡮ࡴࡧࠡࡕࡇࡏࠥࡽࡩࡵࡪࠣࡥࡷ࡭ࡳ࠻ࠢࠪཥ") + str(bstack11l1llll11_opy_))
  run_on_browserstack(bstack11l1llll11_opy_, None, True)
@measure(event_name=EVENTS.bstack1ll11l111l_opy_, stage=STAGE.bstack1lllllll11_opy_, bstack1l11ll11l_opy_=SESSION_NAME)
def bstack1ll1l111_opy_():
  global CONFIG
  global bstack1l11lllll1_opy_
  global bstack1l1lllll1l_opy_
  global bstack1l1l1lll11_opy_
  global global_config
  global _1l1lll1lll_opy_
  bstack1ll1l1111_opy_.bstack111llll111_opy_()
  _1l1lll1lll_opy_ = cli.is_running()
  if _1l1lll1lll_opy_:
    bstack11l1lll1_opy_.invoke(Events.bstack1lll111l_opy_)
  else:
    bstack1111ll1l_opy_ = bstack11lllllll_opy_.get_instance(config=CONFIG)
    bstack1111ll1l_opy_.bstack11ll1l11l1_opy_(CONFIG)
  hashed_id = None
  bstack1lll11l11l_opy_ = None
  def bstack1l1111l1_opy_():
    try:
      if bstack1l11lllll1_opy_ == bstack11lll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨས"):
        if not cli.is_enabled(CONFIG):
          TestHubHandler.stop()
      else:
        TestHubHandler.stop()
    except Exception as e:
      logger.debug(bstack11lll1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡵࡷࡳࡵࡶࡩ࡯ࡩࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࢁࡽࠣཧ").format(e))
  def bstack1111l1ll_opy_():
    try:
      if not cli.is_enabled(CONFIG):
        bstack1ll1l1l1l1_opy_.bstack1lllllll1l_opy_()
    except Exception as e:
      logger.debug(bstack11lll1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡳࡶ࡮ࡴࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࠣࡰ࡮ࡴ࡫࠻ࠢࡾࢁࠧཨ").format(e))
  def bstack1ll1ll11l1_opy_():
    nonlocal hashed_id, bstack1lll11l11l_opy_
    try:
      if bstack11lll1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨཀྵ") in CONFIG and str(CONFIG[bstack11lll1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩཪ")]).lower() != bstack11lll1_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬཫ"):
        hashed_id, bstack1lll11l11l_opy_ = bstack11ll1lll1_opy_()
      else:
        hashed_id, bstack1lll11l11l_opy_ = get_build_link()
    except Exception as e:
      logger.debug(bstack11lll1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࠦ࡬ࡪࡰ࡮࠾ࠥࢁࡽࠣཬ").format(e))
  bstack1l11111l1l_opy_ = threading.Thread(target=bstack1l1111l1_opy_)
  bstack1l1111ll1_opy_ = threading.Thread(target=bstack1111l1ll_opy_)
  bstack1l111lll1_opy_ = threading.Thread(target=bstack1ll1ll11l1_opy_)
  threads = [bstack1l11111l1l_opy_, bstack1l1111ll1_opy_, bstack1l111lll1_opy_]
  for thread in threads:
    try:
      thread.start()
    except Exception as e:
      logger.debug(bstack11lll1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡴࡶࡤࡶࡹ࡯࡮ࡨࠢࡷ࡬ࡷ࡫ࡡࡥࠢࡾࢁ࠿ࠦࡻࡾࠤ཭").format(thread.name, e))
  for thread in threads:
    try:
      thread.join()
    except Exception as e:
      logger.debug(bstack11lll1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡬ࡲ࡭ࡳ࡯࡮ࡨࠢࡷ࡬ࡷ࡫ࡡࡥࠢࡾࢁ࠿ࠦࡻࡾࠤ཮").format(thread.name, e))
  bstack111llllll1_opy_(hashed_id)
  logger.info(bstack11lll1_opy_ (u"ࠪࡗࡉࡑࠠࡳࡷࡱࠤࡪࡴࡤࡦࡦࠣࡪࡴࡸࠠࡪࡦ࠽ࠫ཯") + global_config.get_property(bstack11lll1_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭཰"), bstack11lll1_opy_ (u"ཱࠬ࠭")) + bstack11lll1_opy_ (u"࠭ࠬࠡࡶࡨࡷࡹ࡮ࡵࡣࠢ࡬ࡨ࠿ིࠦࠧ") + os.getenv(bstack11lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈཱིࠬ"), bstack11lll1_opy_ (u"ࠨུࠩ")))
  if hashed_id is not None and bstack11l11llll1_opy_() != -1:
    sessions = bstack11llllll_opy_(hashed_id)
    bstack111l1l1ll_opy_(sessions, bstack1lll11l11l_opy_)
  if bstack1l11lllll1_opy_ == bstack11lll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵཱུࠩ") and bstack1l1lllll1l_opy_ != 0:
    sys.exit(bstack1l1lllll1l_opy_)
  if bstack1l11lllll1_opy_ == bstack11lll1_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪྲྀ") and bstack1l1l1lll11_opy_ != 0:
    sys.exit(bstack1l1l1lll11_opy_)
def bstack111llllll1_opy_(new_id):
    global bstack11l11l1l1l_opy_
    bstack11l11l1l1l_opy_ = new_id
def bstack1l1l1111_opy_(bstack111l1l1l1l_opy_):
  if bstack111l1l1l1l_opy_:
    return bstack111l1l1l1l_opy_.capitalize()
  else:
    return bstack11lll1_opy_ (u"ࠫࠬཷ")
@measure(event_name=EVENTS.bstack1111l1llll_opy_, stage=STAGE.bstack1lllllll11_opy_, bstack1l11ll11l_opy_=SESSION_NAME)
def bstack1l111l1ll1_opy_(bstack1l111l1l11_opy_):
  if bstack11lll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪླྀ") in bstack1l111l1l11_opy_ and bstack1l111l1l11_opy_[bstack11lll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫཹ")] != bstack11lll1_opy_ (u"ࠧࠨེ"):
    return bstack1l111l1l11_opy_[bstack11lll1_opy_ (u"ࠨࡰࡤࡱࡪཻ࠭")]
  else:
    bstack1l11ll11l_opy_ = bstack11lll1_opy_ (u"ࠤོࠥ")
    if bstack11lll1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧཽࠪ") in bstack1l111l1l11_opy_ and bstack1l111l1l11_opy_[bstack11lll1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫཾ")] != None:
      bstack1l11ll11l_opy_ += bstack1l111l1l11_opy_[bstack11lll1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬཿ")] + bstack11lll1_opy_ (u"ࠨࠬࠡࠤྀ")
      if bstack1l111l1l11_opy_[bstack11lll1_opy_ (u"ࠧࡰࡵཱྀࠪ")] == bstack11lll1_opy_ (u"ࠣ࡫ࡲࡷࠧྂ"):
        bstack1l11ll11l_opy_ += bstack11lll1_opy_ (u"ࠤ࡬ࡓࡘࠦࠢྃ")
      bstack1l11ll11l_opy_ += (bstack1l111l1l11_opy_[bstack11lll1_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴ྄ࠧ")] or bstack11lll1_opy_ (u"ࠫࠬ྅"))
      return bstack1l11ll11l_opy_
    else:
      bstack1l11ll11l_opy_ += bstack1l1l1111_opy_(bstack1l111l1l11_opy_[bstack11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭྆")]) + bstack11lll1_opy_ (u"ࠨࠠࠣ྇") + (
              bstack1l111l1l11_opy_[bstack11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩྈ")] or bstack11lll1_opy_ (u"ࠨࠩྉ")) + bstack11lll1_opy_ (u"ࠤ࠯ࠤࠧྊ")
      if bstack1l111l1l11_opy_[bstack11lll1_opy_ (u"ࠪࡳࡸ࠭ྋ")] == bstack11lll1_opy_ (u"ࠦ࡜࡯࡮ࡥࡱࡺࡷࠧྌ"):
        bstack1l11ll11l_opy_ += bstack11lll1_opy_ (u"ࠧ࡝ࡩ࡯ࠢࠥྍ")
      bstack1l11ll11l_opy_ += bstack1l111l1l11_opy_[bstack11lll1_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪྎ")] or bstack11lll1_opy_ (u"ࠧࠨྏ")
      return bstack1l11ll11l_opy_
@measure(event_name=EVENTS.bstack11l1llll1l_opy_, stage=STAGE.bstack1lllllll11_opy_, bstack1l11ll11l_opy_=SESSION_NAME)
def bstack11l1l1lll1_opy_(bstack11lllll1l1_opy_):
  if bstack11lllll1l1_opy_ == bstack11lll1_opy_ (u"ࠣࡦࡲࡲࡪࠨྐ"):
    return bstack11lll1_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾࡬ࡸࡥࡦࡰ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦ࡬ࡸࡥࡦࡰࠥࡂࡈࡵ࡭ࡱ࡮ࡨࡸࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬྑ")
  elif bstack11lllll1l1_opy_ == bstack11lll1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥྒ"):
    return bstack11lll1_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡲࡦࡦ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡷ࡫ࡤࠣࡀࡉࡥ࡮ࡲࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧྒྷ")
  elif bstack11lllll1l1_opy_ == bstack11lll1_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧྔ"):
    return bstack11lll1_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡩࡵࡩࡪࡴ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡩࡵࡩࡪࡴࠢ࠿ࡒࡤࡷࡸ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ྕ")
  elif bstack11lllll1l1_opy_ == bstack11lll1_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨྖ"):
    return bstack11lll1_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡶࡪࡪ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡴࡨࡨࠧࡄࡅࡳࡴࡲࡶࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪྗ")
  elif bstack11lllll1l1_opy_ == bstack11lll1_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥ྘"):
    return bstack11lll1_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࠩࡥࡦࡣ࠶࠶࠻ࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࠤࡧࡨࡥ࠸࠸࠶ࠣࡀࡗ࡭ࡲ࡫࡯ࡶࡶ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨྙ")
  elif bstack11lllll1l1_opy_ == bstack11lll1_opy_ (u"ࠦࡷࡻ࡮࡯࡫ࡱ࡫ࠧྚ"):
    return bstack11lll1_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡣ࡮ࡤࡧࡰࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡣ࡮ࡤࡧࡰࠨ࠾ࡓࡷࡱࡲ࡮ࡴࡧ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ྛ")
  else:
    return bstack11lll1_opy_ (u"࠭࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡥࡰࡦࡩ࡫࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡥࡰࡦࡩ࡫ࠣࡀࠪྜ") + bstack1l1l1111_opy_(
      bstack11lllll1l1_opy_) + bstack11lll1_opy_ (u"ࠧ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ྜྷ")
def bstack1l1lll11l_opy_(session):
  return bstack11lll1_opy_ (u"ࠨ࠾ࡷࡶࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡸ࡯ࡸࠤࡁࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠥࡹࡥࡴࡵ࡬ࡳࡳ࠳࡮ࡢ࡯ࡨࠦࡃࡂࡡࠡࡪࡵࡩ࡫ࡃࠢࡼࡿࠥࠤࡹࡧࡲࡨࡧࡷࡁࠧࡥࡢ࡭ࡣࡱ࡯ࠧࡄࡻࡾ࠾࠲ࡥࡃࡂ࠯ࡵࡦࡁࡿࢂࢁࡽ࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿࠳ࡹࡸ࠾ࠨྞ").format(
    session[bstack11lll1_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤࡡࡸࡶࡱ࠭ྟ")], bstack1l111l1ll1_opy_(session), bstack11l1l1lll1_opy_(session[bstack11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡸࡦࡺࡵࡴࠩྠ")]),
    bstack11l1l1lll1_opy_(session[bstack11lll1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫྡ")]),
    bstack1l1l1111_opy_(session[bstack11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ྡྷ")] or session[bstack11lll1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ྣ")] or bstack11lll1_opy_ (u"ࠧࠨྤ")) + bstack11lll1_opy_ (u"ࠣࠢࠥྥ") + (session[bstack11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫྦ")] or bstack11lll1_opy_ (u"ࠪࠫྦྷ")),
    session[bstack11lll1_opy_ (u"ࠫࡴࡹࠧྨ")] + bstack11lll1_opy_ (u"ࠧࠦࠢྩ") + session[bstack11lll1_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪྪ")], session[bstack11lll1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩྫ")] or bstack11lll1_opy_ (u"ࠨࠩྫྷ"),
    session[bstack11lll1_opy_ (u"ࠩࡦࡶࡪࡧࡴࡦࡦࡢࡥࡹ࠭ྭ")] if session[bstack11lll1_opy_ (u"ࠪࡧࡷ࡫ࡡࡵࡧࡧࡣࡦࡺࠧྮ")] else bstack11lll1_opy_ (u"ࠫࠬྯ"))
@measure(event_name=EVENTS.bstack111lll1ll1_opy_, stage=STAGE.bstack1lllllll11_opy_, bstack1l11ll11l_opy_=SESSION_NAME)
def bstack111l1l1ll_opy_(sessions, bstack1lll11l11l_opy_):
  try:
    bstack11ll1111l_opy_ = bstack11lll1_opy_ (u"ࠧࠨྰ")
    if not os.path.exists(bstack1l1l1111l1_opy_):
      os.mkdir(bstack1l1l1111l1_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11lll1_opy_ (u"࠭ࡡࡴࡵࡨࡸࡸ࠵ࡲࡦࡲࡲࡶࡹ࠴ࡨࡵ࡯࡯ࠫྱ")), bstack11lll1_opy_ (u"ࠧࡳࠩྲ")) as f:
      bstack11ll1111l_opy_ = f.read()
    bstack11ll1111l_opy_ = bstack11ll1111l_opy_.replace(bstack11lll1_opy_ (u"ࠨࡽࠨࡖࡊ࡙ࡕࡍࡖࡖࡣࡈࡕࡕࡏࡖࠨࢁࠬླ"), str(len(sessions)))
    bstack11ll1111l_opy_ = bstack11ll1111l_opy_.replace(bstack11lll1_opy_ (u"ࠩࡾࠩࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠥࡾࠩྴ"), bstack1lll11l11l_opy_)
    bstack11ll1111l_opy_ = bstack11ll1111l_opy_.replace(bstack11lll1_opy_ (u"ࠪࡿࠪࡈࡕࡊࡎࡇࡣࡓࡇࡍࡆࠧࢀࠫྵ"),
                                              sessions[0].get(bstack11lll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡲࡦࡳࡥࠨྶ")) if sessions[0] else bstack11lll1_opy_ (u"ࠬ࠭ྷ"))
    with open(os.path.join(bstack1l1l1111l1_opy_, bstack11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡸࡥࡱࡱࡵࡸ࠳࡮ࡴ࡮࡮ࠪྸ")), bstack11lll1_opy_ (u"ࠧࡸࠩྐྵ")) as stream:
      stream.write(bstack11ll1111l_opy_.split(bstack11lll1_opy_ (u"ࠨࡽࠨࡗࡊ࡙ࡓࡊࡑࡑࡗࡤࡊࡁࡕࡃࠨࢁࠬྺ"))[0])
      for session in sessions:
        stream.write(bstack1l1lll11l_opy_(session))
      stream.write(bstack11ll1111l_opy_.split(bstack11lll1_opy_ (u"ࠩࡾࠩࡘࡋࡓࡔࡋࡒࡒࡘࡥࡄࡂࡖࡄࠩࢂ࠭ྻ"))[1])
    logger.info(bstack11lll1_opy_ (u"ࠪࡋࡪࡴࡥࡳࡣࡷࡩࡩࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡨࡵࡪ࡮ࡧࠤࡦࡸࡴࡪࡨࡤࡧࡹࡹࠠࡢࡶࠣࡿࢂ࠭ྼ").format(bstack1l1l1111l1_opy_));
  except Exception as e:
    logger.debug(bstack11ll11l11l_opy_.format(str(e)))
def bstack11llllll_opy_(hashed_id):
  global CONFIG
  try:
    bstack111ll1l1_opy_ = datetime.datetime.now()
    host = bstack11lll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠯ࡦࡰࡴࡻࡤ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫ྽") if bstack11lll1_opy_ (u"ࠬࡧࡰࡱࠩ྾") in CONFIG else bstack11lll1_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡲ࡬࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧ྿")
    user = CONFIG[bstack11lll1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ࿀")]
    key = CONFIG[bstack11lll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ࿁")]
    bstack111l11ll1_opy_ = bstack11lll1_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨ࿂") if bstack11lll1_opy_ (u"ࠪࡥࡵࡶࠧ࿃") in CONFIG else (bstack11lll1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨ࿄") if CONFIG.get(bstack11lll1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩ࿅")) else bstack11lll1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ࿆"))
    host = bstack11111l11ll_opy_(cli.config, [bstack11lll1_opy_ (u"ࠢࡢࡲ࡬ࡷࠧ࿇"), bstack11lll1_opy_ (u"ࠣࡣࡳࡴࡆࡻࡴࡰ࡯ࡤࡸࡪࠨ࿈"), bstack11lll1_opy_ (u"ࠤࡤࡴ࡮ࠨ࿉")], host) if bstack11lll1_opy_ (u"ࠪࡥࡵࡶࠧ࿊") in CONFIG else bstack11111l11ll_opy_(cli.config, [bstack11lll1_opy_ (u"ࠦࡦࡶࡩࡴࠤ࿋"), bstack11lll1_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫ࠢ࿌"), bstack11lll1_opy_ (u"ࠨࡡࡱ࡫ࠥ࿍")], host)
    url = bstack11lll1_opy_ (u"ࠧࡼࡿ࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾ࠱ࡶࡩࡸࡹࡩࡰࡰࡶ࠲࡯ࡹ࡯࡯ࠩ࿎").format(host, bstack111l11ll1_opy_, hashed_id)
    headers = {
      bstack11lll1_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧ࿏"): bstack11lll1_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬ࿐"),
    }
    proxies = bstack11l11l11l1_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies, auth=(user, key))
    if response.json():
      cli.bstack11l111ll1l_opy_(bstack11lll1_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻ࡩࡨࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡹ࡟࡭࡫ࡶࡸࠧ࿑"), datetime.datetime.now() - bstack111ll1l1_opy_)
      return list(map(lambda session: session[bstack11lll1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩ࿒")], response.json()))
  except Exception as e:
    logger.debug(bstack1l111ll11l_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack1lll1111_opy_, stage=STAGE.bstack1lllllll11_opy_, bstack1l11ll11l_opy_=SESSION_NAME)
def get_build_link():
  global CONFIG
  global bstack11l11l1l1l_opy_
  try:
    if bstack11lll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ࿓") in CONFIG:
      bstack111ll1l1_opy_ = datetime.datetime.now()
      host = bstack11lll1_opy_ (u"࠭ࡡࡱ࡫࠰ࡧࡱࡵࡵࡥࠩ࿔") if bstack11lll1_opy_ (u"ࠧࡢࡲࡳࠫ࿕") in CONFIG else bstack11lll1_opy_ (u"ࠨࡣࡳ࡭ࠬ࿖")
      user = CONFIG[bstack11lll1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ࿗")]
      key = CONFIG[bstack11lll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭࿘")]
      bstack111l11ll1_opy_ = bstack11lll1_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪ࿙") if bstack11lll1_opy_ (u"ࠬࡧࡰࡱࠩ࿚") in CONFIG else bstack11lll1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ࿛")
      url = bstack11lll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡽࢀ࠾ࢀࢃࡀࡼࡿ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠰࡭ࡷࡴࡴࠧ࿜").format(user, key, host, bstack111l11ll1_opy_)
      if cli.is_enabled(CONFIG):
        bstack1lll11l11l_opy_, hashed_id = cli.bstack11l1ll111_opy_()
        logger.info(bstack11ll111ll1_opy_.format(bstack1lll11l11l_opy_))
        return [hashed_id, bstack1lll11l11l_opy_]
      else:
        headers = {
          bstack11lll1_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧ࿝"): bstack11lll1_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬ࿞"),
        }
        if bstack11lll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ࿟") in CONFIG:
          params = {bstack11lll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ࿠"): CONFIG[bstack11lll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ࿡")], bstack11lll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ࿢"): CONFIG[bstack11lll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ࿣")]}
        else:
          params = {bstack11lll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭࿤"): CONFIG[bstack11lll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ࿥")]}
        proxies = bstack11l11l11l1_opy_(CONFIG, url)
        response = requests.get(url, params=params, headers=headers, proxies=proxies)
        if response.json():
          bstack111ll1l11_opy_ = response.json()[0][bstack11lll1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡣࡷ࡬ࡰࡩ࠭࿦")]
          if bstack111ll1l11_opy_:
            bstack1lll11l11l_opy_ = bstack111ll1l11_opy_[bstack11lll1_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦࡣࡺࡸ࡬ࠨ࿧")].split(bstack11lll1_opy_ (u"ࠬࡶࡵࡣ࡮࡬ࡧ࠲ࡨࡵࡪ࡮ࡧࠫ࿨"))[0] + bstack11lll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡸ࠵ࠧ࿩") + bstack111ll1l11_opy_[
              bstack11lll1_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ࿪")]
            logger.info(bstack11ll111ll1_opy_.format(bstack1lll11l11l_opy_))
            bstack11l11l1l1l_opy_ = bstack111ll1l11_opy_[bstack11lll1_opy_ (u"ࠨࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ࿫")]
            bstack1lll11ll11_opy_ = CONFIG[bstack11lll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ࿬")]
            if bstack11lll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ࿭") in CONFIG:
              bstack1lll11ll11_opy_ += bstack11lll1_opy_ (u"ࠫࠥ࠭࿮") + CONFIG[bstack11lll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ࿯")]
            if bstack1lll11ll11_opy_ != bstack111ll1l11_opy_[bstack11lll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ࿰")]:
              logger.debug(bstack111l111l_opy_.format(bstack111ll1l11_opy_[bstack11lll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ࿱")], bstack1lll11ll11_opy_))
            cli.bstack11l111ll1l_opy_(bstack11lll1_opy_ (u"ࠣࡪࡷࡸࡵࡀࡧࡦࡶࡢࡦࡺ࡯࡬ࡥࡡ࡯࡭ࡳࡱࠢ࿲"), datetime.datetime.now() - bstack111ll1l1_opy_)
            return [bstack111ll1l11_opy_[bstack11lll1_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ࿳")], bstack1lll11l11l_opy_]
    else:
      logger.warning(bstack1lll1111l_opy_)
  except Exception as e:
    logger.debug(bstack111l111l1l_opy_.format(str(e)))
  return [None, None]
def bstack11lll1l1_opy_(url, bstack1ll1l1ll11_opy_=False):
  global CONFIG
  global bstack11111l1lll_opy_
  if not bstack11111l1lll_opy_:
    hostname = bstack111l1lll1_opy_(url)
    is_private = bstack1l11ll1ll1_opy_(hostname)
    if (bstack11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ࿴") in CONFIG and not bstack1lll11l1_opy_(CONFIG[bstack11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ࿵")])) and (is_private or bstack1ll1l1ll11_opy_):
      bstack11111l1lll_opy_ = hostname
def bstack111l1lll1_opy_(url):
  return urlparse(url).hostname
def bstack1l11ll1ll1_opy_(hostname):
  for bstack11lll11l1_opy_ in bstack1lllll11l1_opy_:
    regex = re.compile(bstack11lll11l1_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1ll11l1l1_opy_(bstack111l11ll_opy_):
  return True if bstack111l11ll_opy_ in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack11l1l1l1l1_opy_, stage=STAGE.bstack1lllllll11_opy_, bstack1l11ll11l_opy_=SESSION_NAME)
def getAccessibilityResults(driver):
  global CONFIG
  global PLATFORM_INDEX
  bstack1l1l1ll111_opy_ = not (bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ࿶"), None) and bstack111ll1ll_opy_(
          threading.current_thread(), bstack11lll1_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ࿷"), None))
  bstack11ll1l111l_opy_ = getattr(driver, bstack11lll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧ࿸"), None) != True
  bstack1lll11111_opy_ = bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ࿹"), None) and bstack111ll1ll_opy_(
          threading.current_thread(), bstack11lll1_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ࿺"), None)
  if bstack1lll11111_opy_:
    if not bstack1l1l11llll_opy_():
      logger.warning(bstack11lll1_opy_ (u"ࠥࡒࡴࡺࠠࡢࡰࠣࡅࡵࡶࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࠡࡃࡳࡴࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸ࠴ࠢ࿻"))
      return {}
    logger.debug(bstack11lll1_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡢࡦࡨࡲࡶࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡳࡧࡶࡹࡱࡺࡳࠨ࿼"))
    logger.debug(perform_scan(driver, driver_command=bstack11lll1_opy_ (u"ࠬ࡫ࡸࡦࡥࡸࡸࡪ࡙ࡣࡳ࡫ࡳࡸࠬ࿽")))
    results = bstack11lllll111_opy_(bstack11lll1_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹࡹࠢ࿾"))
    if results is not None and results.get(bstack11lll1_opy_ (u"ࠢࡪࡵࡶࡹࡪࡹࠢ࿿")) is not None:
        return results[bstack11lll1_opy_ (u"ࠣ࡫ࡶࡷࡺ࡫ࡳࠣက")]
    logger.error(bstack11lll1_opy_ (u"ࠤࡑࡳࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡘࡥࡴࡷ࡯ࡸࡸࠦࡷࡦࡴࡨࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦခ"))
    return []
  if not a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX) or (bstack11ll1l111l_opy_ and bstack1l1l1ll111_opy_):
    logger.warning(bstack11lll1_opy_ (u"ࠥࡒࡴࡺࠠࡢࡰࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷ࠳ࠨဂ"))
    return {}
  try:
    logger.debug(bstack11lll1_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡢࡦࡨࡲࡶࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡳࡧࡶࡹࡱࡺࡳࠨဃ"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(accessibility_scripts.get_results)
    return results
  except Exception:
    logger.error(bstack11lll1_opy_ (u"ࠧࡔ࡯ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡺࡩࡷ࡫ࠠࡧࡱࡸࡲࡩ࠴ࠢင"))
    return {}
@measure(event_name=EVENTS.bstack1l1lll1l1l_opy_, stage=STAGE.bstack1lllllll11_opy_, bstack1l11ll11l_opy_=SESSION_NAME)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global PLATFORM_INDEX
  bstack1l1l1ll111_opy_ = not (bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪစ"), None) and bstack111ll1ll_opy_(
          threading.current_thread(), bstack11lll1_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ဆ"), None))
  bstack11ll1l111l_opy_ = getattr(driver, bstack11lll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨဇ"), None) != True
  bstack1lll11111_opy_ = bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩဈ"), None) and bstack111ll1ll_opy_(
          threading.current_thread(), bstack11lll1_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬဉ"), None)
  if bstack1lll11111_opy_:
    if not bstack1l1l11llll_opy_():
      logger.warning(bstack11lll1_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡶࡰࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡄࡴࡵࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡴࡷࡰࡱࡦࡸࡹ࠯ࠤည"))
      return {}
    logger.debug(bstack11lll1_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡴࡨࡷࡺࡲࡴࡴࠢࡶࡹࡲࡳࡡࡳࡻࠪဋ"))
    logger.debug(perform_scan(driver, driver_command=bstack11lll1_opy_ (u"࠭ࡥࡹࡧࡦࡹࡹ࡫ࡓࡤࡴ࡬ࡴࡹ࠭ဌ")))
    results = bstack11lllll111_opy_(bstack11lll1_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡓࡶ࡯ࡰࡥࡷࡿࠢဍ"))
    if results is not None and results.get(bstack11lll1_opy_ (u"ࠣࡵࡸࡱࡲࡧࡲࡺࠤဎ")) is not None:
        return results[bstack11lll1_opy_ (u"ࠤࡶࡹࡲࡳࡡࡳࡻࠥဏ")]
    logger.error(bstack11lll1_opy_ (u"ࠥࡒࡴࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡒࡦࡵࡸࡰࡹࡹࠠࡔࡷࡰࡱࡦࡸࡹࠡࡹࡤࡷࠥ࡬࡯ࡶࡰࡧ࠲ࠧတ"))
    return {}
  if not a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX) or (bstack11ll1l111l_opy_ and bstack1l1l1ll111_opy_):
    logger.warning(bstack11lll1_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡪࡺࡲࡪࡧࡹࡩࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡳࡶ࡯ࡰࡥࡷࡿ࠮ࠣထ"))
    return {}
  try:
    logger.debug(bstack11lll1_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡴࡨࡷࡺࡲࡴࡴࠢࡶࡹࡲࡳࡡࡳࡻࠪဒ"))
    logger.debug(perform_scan(driver))
    bstack111lll1lll_opy_ = driver.execute_async_script(accessibility_scripts.get_results_summary)
    return bstack111lll1lll_opy_
  except Exception:
    logger.error(bstack11lll1_opy_ (u"ࠨࡎࡰࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡹࡲࡳࡡࡳࡻࠣࡻࡦࡹࠠࡧࡱࡸࡲࡩ࠴ࠢဓ"))
    return {}
def bstack1l1l11llll_opy_():
  global CONFIG
  global PLATFORM_INDEX
  bstack1l1ll11111_opy_ = bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧန"), None) and bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪပ"), None)
  if not a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX) or not bstack1l1ll11111_opy_:
        logger.warning(bstack11lll1_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡴࡵࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡳࡧࡶࡹࡱࡺࡳ࠯ࠤဖ"))
        return False
  return True
def bstack11lllll111_opy_(result_type):
    bstack1l11l1lll_opy_ = TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack1ll1l1l1l1_opy_.current_hook_uuid()
    with ThreadPoolExecutor() as executor:
        future = executor.submit(bstack1llll1ll1_opy_(bstack1l11l1lll_opy_, result_type))
        try:
            return future.result(timeout=bstack1lllll111l_opy_)
        except TimeoutError:
            logger.error(bstack11lll1_opy_ (u"ࠥࡘ࡮ࡳࡥࡰࡷࡷࠤࡦ࡬ࡴࡦࡴࠣࡿࢂࡹࠠࡸࡪ࡬ࡰࡪࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡔࡨࡷࡺࡲࡴࡴࠤဗ").format(bstack1lllll111l_opy_))
        except Exception as ex:
            logger.debug(bstack11lll1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡶࡪࡺࡲࡪࡧࡹ࡭ࡳ࡭ࠠࡂࡲࡳࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡽࢀ࠲ࠥࡋࡲࡳࡱࡵࠤ࠲ࠦࡻࡾࠤဘ").format(result_type, str(ex)))
    return {}
@measure(event_name=EVENTS.bstack1ll11ll1l_opy_, stage=STAGE.bstack1lllllll11_opy_, bstack1l11ll11l_opy_=SESSION_NAME)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global PLATFORM_INDEX
  bstack1l1l1ll111_opy_ = not (bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩမ"), None) and bstack111ll1ll_opy_(
          threading.current_thread(), bstack11lll1_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬယ"), None))
  bstack1l1l1ll11l_opy_ = not (bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧရ"), None) and bstack111ll1ll_opy_(
          threading.current_thread(), bstack11lll1_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪလ"), None))
  bstack11ll1l111l_opy_ = getattr(driver, bstack11lll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩဝ"), None) != True
  if not a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX) or (bstack11ll1l111l_opy_ and bstack1l1l1ll111_opy_ and bstack1l1l1ll11l_opy_):
    logger.warning(bstack11lll1_opy_ (u"ࠥࡒࡴࡺࠠࡢࡰࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡹࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡤࡣࡱ࠲ࠧသ"))
    return {}
  try:
    bstack11ll111l_opy_ = bstack11lll1_opy_ (u"ࠫࡦࡶࡰࠨဟ") in CONFIG and CONFIG.get(bstack11lll1_opy_ (u"ࠬࡧࡰࡱࠩဠ"), bstack11lll1_opy_ (u"࠭ࠧအ"))
    session_id = getattr(driver, bstack11lll1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠫဢ"), None)
    if not session_id:
      logger.warning(bstack11lll1_opy_ (u"ࠣࡐࡲࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡏࡄࠡࡨࡲࡹࡳࡪࠠࡧࡱࡵࠤࡩࡸࡩࡷࡧࡵࠦဣ"))
      return {bstack11lll1_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣဤ"): bstack11lll1_opy_ (u"ࠥࡒࡴࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡊࡆࠣࡪࡴࡻ࡮ࡥࠤဥ")}
    if bstack11ll111l_opy_:
      try:
        bstack11l1l1l1l_opy_ = {
              bstack11lll1_opy_ (u"ࠫࡹ࡮ࡊࡸࡶࡗࡳࡰ࡫࡮ࠨဦ"): os.environ.get(bstack11lll1_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪဧ"), os.environ.get(bstack11lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪဨ"), bstack11lll1_opy_ (u"ࠧࠨဩ"))),
              bstack11lll1_opy_ (u"ࠨࡶ࡫ࡘࡪࡹࡴࡓࡷࡱ࡙ࡺ࡯ࡤࠨဪ"): TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack1ll1l1l1l1_opy_.current_hook_uuid(),
              bstack11lll1_opy_ (u"ࠩࡤࡹࡹ࡮ࡈࡦࡣࡧࡩࡷ࠭ါ"): os.environ.get(bstack11lll1_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨာ")),
              bstack11lll1_opy_ (u"ࠫࡸࡩࡡ࡯ࡖ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫိ"): str(int(datetime.datetime.now().timestamp() * 1000)),
              bstack11lll1_opy_ (u"ࠬࡺࡨࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪီ"): os.environ.get(bstack11lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫု"), bstack11lll1_opy_ (u"ࠧࠨူ")),
              bstack11lll1_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࠨေ"): kwargs.get(bstack11lll1_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࡡࡦࡳࡲࡳࡡ࡯ࡦࠪဲ"), None) or bstack11lll1_opy_ (u"ࠪࠫဳ")
          }
        if not hasattr(thread_local, bstack11lll1_opy_ (u"ࠫࡧࡧࡳࡦࡡࡤࡴࡵࡥࡡ࠲࠳ࡼࡣࡸࡩࡲࡪࡲࡷࠫဴ")):
            scripts = {bstack11lll1_opy_ (u"ࠬࡹࡣࡢࡰࠪဵ"): accessibility_scripts.perform_scan}
            thread_local.base_app_a11y_script = scripts
        bstack111l1l1l_opy_ = copy.deepcopy(thread_local.base_app_a11y_script)
        bstack111l1l1l_opy_[bstack11lll1_opy_ (u"࠭ࡳࡤࡣࡱࠫံ")] = bstack111l1l1l_opy_[bstack11lll1_opy_ (u"ࠧࡴࡥࡤࡲ့ࠬ")] % json.dumps(bstack11l1l1l1l_opy_)
        accessibility_scripts.bstack11lll1l11_opy_(bstack111l1l1l_opy_)
        accessibility_scripts.store()
        bstack1111l11111_opy_ = driver.execute_script(accessibility_scripts.perform_scan)
      except Exception as bstack1ll1l111l_opy_:
        logger.info(bstack11lll1_opy_ (u"ࠣࡃࡳࡴ࡮ࡻ࡭ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࠣး") + str(bstack1ll1l111l_opy_))
        bstack1111l11111_opy_ = {bstack11lll1_opy_ (u"ࠤࡨࡶࡷࡵࡲ္ࠣ"): str(bstack1ll1l111l_opy_)}
    else:
      bstack1111l11111_opy_ = driver.execute_async_script(accessibility_scripts.perform_scan, {bstack11lll1_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦ်ࠪ"): kwargs.get(bstack11lll1_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࡣࡨࡵ࡭࡮ࡣࡱࡨࠬျ"), None) or bstack11lll1_opy_ (u"ࠬ࠭ြ")})
    return bstack1111l11111_opy_
  except Exception as err:
    logger.error(bstack11lll1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡵࡹࡳࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡤࡣࡱ࠲ࠥࢁࡽࠣွ").format(str(err)))
    return {}