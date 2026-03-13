# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
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
from browserstack_sdk.sdk_cli.bstack1llll1l11_opy_ import bstack11l1l111ll_opy_
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from browserstack_sdk.bstack1111llllll_opy_ import bstack11111lll1_opy_
from browserstack_sdk.bstack1l11ll1l11_opy_ import *
import time
import requests
from bstack_utils.constants import EVENTS, STAGE, bstack11l1lll1_opy_
from bstack_utils.messages import bstack1lllll1l1l_opy_, bstack1l111l1l11_opy_, bstack11ll11ll_opy_, bstack11lllll1l1_opy_, bstack111ll11l_opy_, bstack1ll11ll11l_opy_
from bstack_utils.measure import measure
from bstack_utils.logger_utils import get_logger
from bstack_utils.helper import bstack1l1l111l11_opy_
from browserstack_sdk.bstack1ll1ll111l_opy_ import bstack1ll1lll1ll_opy_
logger = get_logger(__name__)
def bstack1l1l1lll1_opy_():
  global CONFIG
  headers = {
        bstack1111l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack1111l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1l1l111l11_opy_(CONFIG, bstack11l1lll1_opy_)
  try:
    response = requests.get(bstack11l1lll1_opy_, headers=headers, proxies=proxies, timeout=2)
    if response.json():
      bstack1l111l1l1l_opy_ = response.json()[bstack1111l_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1lllll1l1l_opy_.format(response.json()))
      return bstack1l111l1l1l_opy_
    else:
      logger.debug(bstack1l111l1l11_opy_.format(bstack1111l_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack1l111l1l11_opy_.format(e))
def bstack1l11llll1l_opy_(hub_url):
  global CONFIG
  url = bstack1111l_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack1111l_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack1111l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack1111l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1l1l111l11_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=(0.5, 1.0))
    latency = time.perf_counter() - start_time
    logger.debug(bstack11ll11ll_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack11lllll1l1_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack11lll111l1_opy_, stage=STAGE.bstack11lll111l_opy_)
def bstack1lll1ll11l_opy_():
  try:
    global bstack11l11lll11_opy_
    global CONFIG
    if bstack1111l_opy_ (u"ࠫ࡭ࡻࡢࡓࡧࡪ࡭ࡴࡴࠧࡾ") in CONFIG and CONFIG[bstack1111l_opy_ (u"ࠬ࡮ࡵࡣࡔࡨ࡫࡮ࡵ࡮ࠨࡿ")]:
      from bstack_utils.constants import bstack111l1l11l1_opy_
      bstack1111l1111_opy_ = CONFIG[bstack1111l_opy_ (u"࠭ࡨࡶࡤࡕࡩ࡬࡯࡯࡯ࠩࢀ")]
      if bstack1111l1111_opy_ in bstack111l1l11l1_opy_:
        bstack11l11lll11_opy_ = bstack111l1l11l1_opy_[bstack1111l1111_opy_]
        logger.debug(bstack111ll11l_opy_.format(bstack11l11lll11_opy_))
        return
      else:
        logger.debug(bstack1111l_opy_ (u"ࠢࡉࡷࡥࠤࡰ࡫ࡹࠡࠩࡾࢁࠬࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࡎࡕࡃࡡࡘࡖࡑࡥࡍࡂࡒ࠯ࠤ࡫ࡧ࡬࡭࡫ࡱ࡫ࠥࡨࡡࡤ࡭ࠣࡸࡴࠦ࡯ࡱࡶ࡬ࡱࡦࡲࠠࡩࡷࡥࠤࡩ࡫ࡴࡦࡥࡷ࡭ࡴࡴࠢࢁ").format(bstack1111l1111_opy_))
    bstack1l111l1l1l_opy_ = bstack1l1l1lll1_opy_()
    from concurrent.futures import ThreadPoolExecutor, as_completed
    if bstack1l111l1l1l_opy_:
        with ThreadPoolExecutor(max_workers=len(bstack1l111l1l1l_opy_)) as executor:
            bstack11llll1111_opy_ = {executor.submit(bstack1l11llll1l_opy_, bstack11l111lll_opy_): bstack11l111lll_opy_ for bstack11l111lll_opy_ in bstack1l111l1l1l_opy_}
            for future in as_completed(bstack11llll1111_opy_):
                result = future.result()
                if result and result.get(bstack1111l_opy_ (u"ࠨ࡮ࡤࡸࡪࡴࡣࡺࠩࢂ")) is not None:
                    bstack11l11lll11_opy_ = result[bstack1111l_opy_ (u"ࠩ࡫ࡹࡧࡥࡵࡳ࡮ࠪࢃ")]
                    logger.debug(bstack111ll11l_opy_.format(bstack11l11lll11_opy_))
                    return
        bstack11l11lll11_opy_ = bstack1l111l1l1l_opy_[0]
        logger.debug(bstack111ll11l_opy_.format(bstack11l11lll11_opy_))
        return
  except Exception as e:
    logger.debug(bstack1ll11ll11l_opy_.format(e))
from browserstack_sdk.bstack1ll11l1ll_opy_ import *
from browserstack_sdk.bstack1ll1ll111l_opy_ import *
from browserstack_sdk.bstack1ll1l1ll1l_opy_ import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.logger_utils import get_logger
from bstack_utils.measure import measure
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack1ll111lll_opy_, stage=STAGE.bstack11lll111l_opy_)
def bstack111l111l11_opy_():
    global bstack11l11lll11_opy_
    try:
        bstack11l11ll11l_opy_ = bstack1l1l1111_opy_()
        bstack1lll1ll111_opy_(bstack11l11ll11l_opy_)
        hub_url = bstack11l11ll11l_opy_.get(bstack1111l_opy_ (u"ࠥࡹࡷࡲࠢࢄ"), bstack1111l_opy_ (u"ࠦࠧࢅ"))
        if hub_url.endswith(bstack1111l_opy_ (u"ࠬ࠵ࡷࡥ࠱࡫ࡹࡧ࠭ࢆ")):
            hub_url = hub_url.rsplit(bstack1111l_opy_ (u"࠭࠯ࡸࡦ࠲࡬ࡺࡨࠧࢇ"), 1)[0]
        if hub_url.startswith(bstack1111l_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࠨ࢈")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack1111l_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࠪࢉ")):
            hub_url = hub_url[8:]
        bstack11l11lll11_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack1l1l1111_opy_():
    global CONFIG
    bstack111ll11l1l_opy_ = CONFIG.get(bstack1111l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢊ"), {}).get(bstack1111l_opy_ (u"ࠪ࡫ࡷ࡯ࡤࡏࡣࡰࡩࠬࢋ"), bstack1111l_opy_ (u"ࠫࡓࡕ࡟ࡈࡔࡌࡈࡤࡔࡁࡎࡇࡢࡔࡆ࡙ࡓࡆࡆࠪࢌ"))
    if not isinstance(bstack111ll11l1l_opy_, str):
        raise ValueError(bstack1111l_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡌࡸࡩࡥࠢࡱࡥࡲ࡫ࠠ࡮ࡷࡶࡸࠥࡨࡥࠡࡣࠣࡺࡦࡲࡩࡥࠢࡶࡸࡷ࡯࡮ࡨࠤࢍ"))
    try:
        bstack11l11ll11l_opy_ = bstack1ll111l1l1_opy_(bstack111ll11l1l_opy_)
        return bstack11l11ll11l_opy_
    except Exception as e:
        logger.error(bstack1111l_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡩࡵ࡭ࡩࠦࡤࡦࡶࡤ࡭ࡱࡹࠠ࠻ࠢࡾࢁࠧࢎ").format(str(e)))
        return {}
def bstack1ll111l1l1_opy_(bstack111ll11l1l_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack1111l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ࢏")] or not CONFIG[bstack1111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ࢐")]:
            raise ValueError(bstack1111l_opy_ (u"ࠤࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠤࡴࡸࠠࡢࡥࡦࡩࡸࡹࠠ࡬ࡧࡼࠦ࢑"))
        url = bstack1l1lllllll_opy_ + bstack111ll11l1l_opy_
        auth = (CONFIG[bstack1111l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ࢒")], CONFIG[bstack1111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ࢓")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack111l1111ll_opy_ = json.loads(response.text)
            return bstack111l1111ll_opy_
    except ValueError as ve:
        logger.error(bstack1111l_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡩࡵ࡭ࡩࠦࡤࡦࡶࡤ࡭ࡱࡹࠠ࠻ࠢࡾࢁࠧ࢔").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack1111l_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡪࡶ࡮ࡪࠠࡥࡧࡷࡥ࡮ࡲࡳࠡ࠼ࠣࡿࢂࠨ࢕").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack1lll1ll111_opy_(bstack1ll1l11l_opy_):
    global CONFIG
    if bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ࢖") not in CONFIG or str(CONFIG[bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬࢗ")]).lower() == bstack1111l_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ࢘"):
        CONFIG[bstack1111l_opy_ (u"ࠪࡰࡴࡩࡡ࡭࢙ࠩ")] = False
    elif bstack1111l_opy_ (u"ࠫ࡮ࡹࡔࡳ࡫ࡤࡰࡌࡸࡩࡥ࢚ࠩ") in bstack1ll1l11l_opy_:
        bstack1111ll1l1_opy_ = CONFIG.get(bstack1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴ࢛ࠩ"), {})
        logger.debug(bstack1111l_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡸࡪࡵࡷ࡭ࡳ࡭ࠠ࡭ࡱࡦࡥࡱࠦ࡯ࡱࡶ࡬ࡳࡳࡹ࠺ࠡࠧࡶࠦ࢜"), bstack1111ll1l1_opy_)
        bstack1l11ll1l_opy_ = bstack1ll1l11l_opy_.get(bstack1111l_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡒࡦࡲࡨࡥࡹ࡫ࡲࡴࠤ࢝"), [])
        bstack11l1l1l11l_opy_ = bstack1111l_opy_ (u"ࠣ࠮ࠥ࢞").join(bstack1l11ll1l_opy_)
        logger.debug(bstack1111l_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡅࡸࡷࡹࡵ࡭ࠡࡴࡨࡴࡪࡧࡴࡦࡴࠣࡷࡹࡸࡩ࡯ࡩ࠽ࠤࠪࡹࠢ࢟"), bstack11l1l1l11l_opy_)
        bstack11lll11l_opy_ = {
            bstack1111l_opy_ (u"ࠥࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧࢠ"): bstack1111l_opy_ (u"ࠦࡦࡺࡳ࠮ࡴࡨࡴࡪࡧࡴࡦࡴࠥࢡ"),
            bstack1111l_opy_ (u"ࠧ࡬࡯ࡳࡥࡨࡐࡴࡩࡡ࡭ࠤࢢ"): bstack1111l_opy_ (u"ࠨࡴࡳࡷࡨࠦࢣ"),
            bstack1111l_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࠭ࡳࡧࡳࡩࡦࡺࡥࡳࠤࢤ"): bstack11l1l1l11l_opy_
        }
        bstack1111ll1l1_opy_.update(bstack11lll11l_opy_)
        logger.debug(bstack1111l_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡖࡲࡧࡥࡹ࡫ࡤࠡ࡮ࡲࡧࡦࡲࠠࡰࡲࡷ࡭ࡴࡴࡳ࠻ࠢࠨࡷࠧࢥ"), bstack1111ll1l1_opy_)
        CONFIG[bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢦ")] = bstack1111ll1l1_opy_
        logger.debug(bstack1111l_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡉ࡭ࡳࡧ࡬ࠡࡅࡒࡒࡋࡏࡇ࠻ࠢࠨࡷࠧࢧ"), CONFIG)
def get_turboscale_playwright_url():
    bstack11l11ll11l_opy_ = bstack1l1l1111_opy_()
    if not bstack11l11ll11l_opy_[bstack1111l_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡖࡴ࡯ࠫࢨ")]:
      raise ValueError(bstack1111l_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡗࡵࡰࠥ࡯ࡳࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡩࡶࡴࡳࠠࡨࡴ࡬ࡨࠥࡪࡥࡵࡣ࡬ࡰࡸ࠴ࠢࢩ"))
    return bstack11l11ll11l_opy_[bstack1111l_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡘࡶࡱ࠭ࢪ")] + bstack1111l_opy_ (u"ࠧࡀࡥࡤࡴࡸࡃࠧࢫ")
@measure(event_name=EVENTS.bstack1l11lll1ll_opy_, stage=STAGE.bstack11lll111l_opy_)
def bstack1ll1ll1ll_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack1111l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪࢬ")], CONFIG[bstack1111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬࢭ")])
        url = bstack1ll1ll1l1l_opy_
        logger.debug(bstack1111l_opy_ (u"ࠥࡅࡹࡺࡥ࡮ࡲࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴࠢࡩࡶࡴࡳࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡔࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠣࡅࡕࡏࠢࢮ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack1111l_opy_ (u"ࠦࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠥࢯ"): bstack1111l_opy_ (u"ࠧࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠣࢰ")})
            if response.status_code == 200:
                bstack1l11l1l1l1_opy_ = json.loads(response.text)
                bstack1l1l1lll_opy_ = bstack1l11l1l1l1_opy_.get(bstack1111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡸ࠭ࢱ"), [])
                if bstack1l1l1lll_opy_:
                    bstack1ll111ll1_opy_ = bstack1l1l1lll_opy_[0]
                    build_hashed_id = bstack1ll111ll1_opy_.get(bstack1111l_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪࢲ"))
                    bstack11ll1l1l1l_opy_ = bstack1lllllll1l_opy_ + build_hashed_id
                    result.extend([build_hashed_id, bstack11ll1l1l1l_opy_])
                    logger.info(bstack11ll1ll111_opy_.format(bstack11ll1l1l1l_opy_))
                    bstack111l1l1l11_opy_ = CONFIG[bstack1111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫࢳ")]
                    if bstack1111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࢴ") in CONFIG:
                      bstack111l1l1l11_opy_ += bstack1111l_opy_ (u"ࠪࠤࠬࢵ") + CONFIG[bstack1111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࢶ")]
                    if bstack111l1l1l11_opy_ != bstack1ll111ll1_opy_.get(bstack1111l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪࢷ")):
                      logger.debug(bstack1l11l111l_opy_.format(bstack1ll111ll1_opy_.get(bstack1111l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫࢸ")), bstack111l1l1l11_opy_))
                    return result
                else:
                    logger.debug(bstack1111l_opy_ (u"ࠢࡂࡖࡖࠤ࠿ࠦࡎࡰࠢࡥࡹ࡮ࡲࡤࡴࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠱ࠦࢹ"))
            else:
                logger.debug(bstack1111l_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴ࠰ࠥࢺ"))
        except Exception as e:
            logger.error(bstack1111l_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࡶࠤ࠿ࠦࡻࡾࠤࢻ").format(str(e)))
    else:
        logger.debug(bstack1111l_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡆࡓࡓࡌࡉࡈࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡶࡩࡹ࠴ࠠࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴ࠰ࠥࢼ"))
    return [None, None]
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1111ll11_opy_ import bstack1111ll11_opy_, Events, bstack1ll11ll111_opy_, bstack1lllll111l_opy_
from bstack_utils.measure import bstack111l1l1ll1_opy_
from bstack_utils.measure import measure
from bstack_utils.percy import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1111l11l_opy_ import bstack1l1111l1l_opy_
from bstack_utils.messages import *
from bstack_utils import logger_utils
from bstack_utils.constants import *
from bstack_utils.helper import bstack1ll111l1_opy_, bstack1llll1ll1_opy_, bstack111l1lll1_opy_, bstack1l11l11l11_opy_, \
  bstack11l1ll11ll_opy_, \
  Notset, is_robot_playwright_installed, bstack11l1111l_opy_, \
  bstack11ll111111_opy_, bstack11ll1l11l1_opy_, bstack11lll1lll_opy_, bstack11llll111_opy_, bstack111ll11ll1_opy_, bstack1l11ll1111_opy_, \
  bstack1l1l1l1l11_opy_, \
  bstack11l1l11l_opy_, bstack1111l111_opy_, bstack11ll11111l_opy_, bstack1lll1llll_opy_, \
  bstack1111l1ll1_opy_, bstack1111ll1ll_opy_, bstack1ll111llll_opy_, bstack1ll1l11l11_opy_, bstack11111ll1_opy_
from bstack_utils.bstack1lll111l_opy_ import bstack11lll1ll_opy_
from bstack_utils.bstack111l1l111l_opy_ import bstack1lll11111l_opy_, bstack1111l1ll_opy_
from bstack_utils.bstack1111l11lll_opy_ import bstack1l111l1lll_opy_
from bstack_utils.session_utils import bstack1ll1111l1l_opy_, bstack1l111l11ll_opy_
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.bstack1l1l11l111_opy_ import bstack1l11lll1_opy_
from bstack_utils.proxy import bstack1llll1l1ll_opy_, bstack1l1l111l11_opy_, bstack11ll1lllll_opy_, bstack1ll1l1l11l_opy_
from bstack_utils.bstack1lll1l11l1_opy_ import bstack111lll111_opy_, bstack1ll1l1l1_opy_
import bstack_utils.bstack1ll1l111l1_opy_ as TestHubUtils
import bstack_utils.bstack1lll1ll1_opy_ as bstack1111l1ll11_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.utils.bstack1l1ll1l11_opy_ import bstack111l11l1_opy_
from bstack_utils.bstack11llllll1_opy_ import bstack11ll11l11l_opy_
from bstack_utils.bstack1lllll1l11_opy_ import bstack1l1lllll_opy_
from bstack_utils.bstack111l1l1ll1_opy_ import bstack1l11ll1l1_opy_
if os.getenv(bstack1111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡉࡑࡒࡏࡘ࠭ࢽ")):
  cli.bstack1l1l1lll1l_opy_()
else:
  os.environ[bstack1111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡊࡒࡓࡐ࡙ࠧࢾ")] = bstack1111l_opy_ (u"࠭ࡴࡳࡷࡨࠫࢿ")
bstack1l1l1ll11l_opy_ = bstack1111l_opy_ (u"ࠧࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠠࠡ࡫ࡩࠬࡵࡧࡧࡦࠢࡀࡁࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠠࡼ࡞ࡱࠤࠥࠦࡴࡳࡻࡾࡠࡳࠦࡣࡰࡰࡶࡸࠥ࡬ࡳࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࡡ࠭ࡦࡴ࡞ࠪ࠭ࡀࡢ࡮ࠡࠢࠣࠤࠥ࡬ࡳ࠯ࡣࡳࡴࡪࡴࡤࡇ࡫࡯ࡩࡘࡿ࡮ࡤࠪࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠬࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡳࡣ࡮ࡴࡤࡦࡺࠬࠤ࠰ࠦࠢ࠻ࠤࠣ࠯ࠥࡐࡓࡐࡐ࠱ࡷࡹࡸࡩ࡯ࡩ࡬ࡪࡾ࠮ࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࠬࡦࡽࡡࡪࡶࠣࡲࡪࡽࡐࡢࡩࡨ࠶࠳࡫ࡶࡢ࡮ࡸࡥࡹ࡫ࠨࠣࠪࠬࠤࡂࡄࠠࡼࡿࠥ࠰ࠥࡢࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡨࡧࡷࡗࡪࡹࡳࡪࡱࡱࡈࡪࡺࡡࡪ࡮ࡶࠦࢂࡢࠧࠪࠫࠬ࡟ࠧ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠣ࡟ࠬࠤ࠰ࠦࠢ࠭࡞࡟ࡲࠧ࠯࡜࡯ࠢࠣࠤࠥࢃࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡽ࡝ࡰࠣࠤ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠧࣀ")
LAUNCH_PATCH_ROBOT_PLAYWRIGHT = bstack1111l_opy_ (u"ࠨ࡞ࡱ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࡢ࡮ࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡰࡢࡶ࡫ࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳࡞࡞ࡱࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠴ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡶ࡟ࡪࡰࡧࡩࡽࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠴ࡠࡠࡳࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡹ࡬ࡪࡥࡨࠬ࠵࠲ࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࠬࡠࡳࡩ࡯࡯ࡵࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬ࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ࠭ࡀࡢ࡮ࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮࡭ࡣࡸࡲࡨ࡮ࠠ࠾ࠢࡤࡷࡾࡴࡣࠡࠪ࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴࠫࠣࡁࡃࠦࡻ࡝ࡰ࡯ࡩࡹࠦࡣࡢࡲࡶ࠿ࡡࡴࡴࡳࡻࠣࡿࡡࡴࡣࡢࡲࡶࠤࡂࠦࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠪ࡞ࡱࠤࠥࢃࠠࡤࡣࡷࡧ࡭࠮ࡥࡹࠫࠣࡿࡡࡴࠠࠡࠢࠣࢁࡡࡴࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡣࡺࡥ࡮ࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮ࡤࡱࡱࡲࡪࡩࡴࠩࡽ࡟ࡲࠥࠦࠠࠡࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸ࠿ࠦࡠࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠦࡾࡩࡳࡩ࡯ࡥࡧࡘࡖࡎࡉ࡯࡮ࡲࡲࡲࡪࡴࡴࠩࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡦࡥࡵࡹࠩࠪࡿࡣ࠰ࡡࡴࠠࠡࠢࠣ࠲࠳࠴࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸࡢ࡮ࠡࠢࢀ࠭ࡡࡴࡽ࡝ࡰࡦࡳࡳࡹࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡧࡴࡴ࡮ࡦࡥࡷࠤࡂࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺ࠮ࡣ࡫ࡱࡨ࠭࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠮ࡁ࡜࡯࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭࠯ࡥࡲࡲࡳ࡫ࡣࡵࠢࡀࠤࡦࡹࡹ࡯ࡥࠣࠬࡨࡵ࡮࡯ࡧࡦࡸࡔࡶࡴࡪࡱࡱࡷ࠮ࠦ࠽࠿ࠢࡾࡠࡳࠦࠠ࡭ࡧࡷࠤࡨࡧࡰࡴ࠽࡟ࡲࠥࠦࡴࡳࡻࠣࡿࡡࡴࠠࠡࠢࠣࡧࡦࡶࡳࠡ࠿ࠣࡎࡘࡕࡎ࠯ࡲࡤࡶࡸ࡫ࠨࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷ࠮ࡢ࡮ࠡࠢࢀࠤࡨࡧࡴࡤࡪࠫࡩࡽ࠯ࠠࡼ࡞ࡱࠤࠥࢃ࡜࡯ࠢࠣࡧࡴࡴࡳࡵࠢࡰࡳࡩ࡯ࡦࡪࡧࡧࡉࡳࡪࡰࡰ࡫ࡱࡸࠥࡃࠠࡡࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࡣࠤ࠰ࠦࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭ࡀࡢ࡮ࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤ࠳࠴࠮ࡤࡱࡱࡲࡪࡩࡴࡐࡲࡷ࡭ࡴࡴࡳ࠭࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࡝ࡰࠣࠤࢂ࠯࡜࡯ࡿ࡟ࡲ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵࡜࡯ࠩࣁ")
from ._version import __version__
bstack11l1l1lll1_opy_ = None
CONFIG = {}
bstack11l1llll_opy_ = {}
bstack1llll1111l_opy_ = {}
bstack1lll11111_opy_ = None
bstack111ll1ll11_opy_ = None
SESSION_NAME = None
PLATFORM_INDEX = -1
bstack11l1llll11_opy_ = 0
bstack111l11lll1_opy_ = bstack11l1111lll_opy_
bstack111l1l11_opy_ = 1
PARALLELISE_VANILLA_PYTHON = False
PARALLELISE_THREADING_PYTHON = False
FRAMEWORK_NAME = bstack1111l_opy_ (u"ࠩࠪࣂ")
bstack1l1l111ll_opy_ = bstack1111l_opy_ (u"ࠪࠫࣃ")
bstack1l1111111l_opy_ = False
BROWSERSTACK_AUTOMATION = True
bstack11l1l1l1l_opy_ = False
bstack111ll111l1_opy_ = bstack1111l_opy_ (u"ࠫࠬࣄ")
bstack1l1lll1ll_opy_ = []
bstack11ll11l1l_opy_ = threading.Lock()
bstack11ll11ll1_opy_ = threading.Lock()
bstack11ll1lll_opy_ = None
bstack11l11lll11_opy_ = bstack1111l_opy_ (u"ࠬ࠭ࣅ")
SELENIUM_OR_PLAYWRIGHT_INSTALLED = False
bstack1l1111ll11_opy_ = None
bstack1l1l1ll1l_opy_ = None
bstack1l11l1ll1_opy_ = None
bstack11lll1ll11_opy_ = -1
bstack111llll11_opy_ = os.path.join(os.path.expanduser(bstack1111l_opy_ (u"࠭ࡾࠨࣆ")), bstack1111l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧࣇ"), bstack1111l_opy_ (u"ࠨ࠰ࡵࡳࡧࡵࡴ࠮ࡴࡨࡴࡴࡸࡴ࠮ࡪࡨࡰࡵ࡫ࡲ࠯࡬ࡶࡳࡳ࠭ࣈ"))
bstack1ll1111ll1_opy_ = 0
bstack11l1l1111_opy_ = 0
bstack11l11l1l1l_opy_ = []
bstack11ll111l_opy_ = []
ROBOT_PYTHON_ERRORS = []
bstack11ll111l1l_opy_ = []
bstack1ll11l11l1_opy_ = bstack1111l_opy_ (u"ࠩࠪࣉ")
bstack1l111ll1ll_opy_ = bstack1111l_opy_ (u"ࠪࠫ࣊")
bstack1111ll111_opy_ = False
bstack1l1l11llll_opy_ = False
bstack111l1l111_opy_ = {}
bstack1lll1lll11_opy_ = {}
bstack1ll1l1ll_opy_ = None
bstack11l1ll11l_opy_ = None
bstack1ll11l1l1l_opy_ = None
bstack1l111l1ll_opy_ = None
bstack11llll1ll_opy_ = None
bstack1llll111l_opy_ = None
bstack1lllllll1_opy_ = None
bstack1l1ll1111_opy_ = None
bstack1111ll1l1l_opy_ = None
bstack1ll1l11ll1_opy_ = None
bstack1111111l_opy_ = None
bstack1l1l111l1l_opy_ = None
bstack11l11l11l1_opy_ = None
bstack11l11lll1_opy_ = None
bstack111l11l1l_opy_ = None
bstack1l11l1l1_opy_ = None
bstack1ll1l1111_opy_ = None
bstack111l11ll11_opy_ = None
bstack11ll11ll1l_opy_ = None
bstack1ll11l11ll_opy_ = None
bstack1l1ll1ll11_opy_ = None
bstack1l1l1l1l1l_opy_ = None
bstack11ll1llll_opy_ = None
thread_local = threading.local()
bstack1l1ll1ll_opy_ = False
bstack1l1111l1ll_opy_ = bstack1111l_opy_ (u"ࠦࠧ࣋")
_11l1ll11l1_opy_ = None
logger = logger_utils.get_logger(__name__, bstack111l11lll1_opy_)
automation_logger = logger_utils.get_automation_logger(__name__)
global_config = Config.get_instance()
percy = bstack1llll111ll_opy_()
bstack1ll1lll11l_opy_ = bstack1l1111l1l_opy_()
bstack1l1l1ll1_opy_ = bstack1ll1l1ll1l_opy_()
def bstack11l1111ll_opy_():
  global CONFIG
  global bstack1111ll111_opy_
  global global_config
  testContextOptions = bstack11lllll1ll_opy_(CONFIG)
  if bstack11l1ll11ll_opy_(CONFIG):
    if (bstack1111l_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ࣌") in testContextOptions and str(testContextOptions[bstack1111l_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ࣍")]).lower() == bstack1111l_opy_ (u"ࠧࡵࡴࡸࡩࠬ࣎")):
      bstack1111ll111_opy_ = True
      global_config.bstack1111ll111l_opy_(True)
    if (bstack1111l_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷ࣏ࠬ") in testContextOptions and str(testContextOptions[bstack1111l_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࣐࠭")]).lower() == bstack1111l_opy_ (u"ࠪࡸࡷࡻࡥࠨ࣑")):
      global_config.bstack111lllll11_opy_(True)
  else:
    bstack1111ll111_opy_ = True
    global_config.bstack1111ll111l_opy_(True)
    global_config.bstack111lllll11_opy_(True)
def bstack1l1llll1l1_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1l1ll1ll1l_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack11l1ll111_opy_():
  global bstack1lll1lll11_opy_
  args = sys.argv
  for i in range(len(args)):
    if bstack1111l_opy_ (u"ࠦ࠲࠳ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡨࡵ࡮ࡧ࡫ࡪࡪ࡮ࡲࡥ࣒ࠣ") == args[i].lower() or bstack1111l_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰࡰࡩ࡭࡬ࠨ࣓") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      bstack1lll1lll11_opy_[bstack1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࡤࡌࡉࡍࡇࠪࣔ")] = path
      return path
  return None
bstack11111l111_opy_ = re.compile(bstack1111l_opy_ (u"ࡲࠣ࠰࠭ࡃࡡࠪࡻࠩ࠰࠭ࡃ࠮ࢃ࠮ࠫࡁࠥࣕ"))
def bstack1ll11111ll_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack11111l111_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack1111l_opy_ (u"ࠣࠦࡾࠦࣖ") + group + bstack1111l_opy_ (u"ࠤࢀࠦࣗ"), os.environ.get(group))
  return value
def bstack111l1l1lll_opy_():
  global bstack11ll1llll_opy_
  if bstack11ll1llll_opy_ is None:
        bstack11ll1llll_opy_ = bstack11l1ll111_opy_()
  bstack1l1ll11111_opy_ = bstack11ll1llll_opy_
  if bstack1l1ll11111_opy_ and os.path.exists(os.path.abspath(bstack1l1ll11111_opy_)):
    fileName = bstack1l1ll11111_opy_
  if bstack1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋࠧࣘ") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack1111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨࣙ")])) and not bstack1111l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡑࡥࡲ࡫ࠧࣚ") in locals():
    fileName = os.environ[bstack1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࡤࡌࡉࡍࡇࠪࣛ")]
  if bstack1111l_opy_ (u"ࠧࡧ࡫࡯ࡩࡓࡧ࡭ࡦࠩࣜ") in locals():
    bstack1llll1l_opy_ = os.path.abspath(fileName)
  else:
    bstack1llll1l_opy_ = bstack1111l_opy_ (u"ࠨࠩࣝ")
  bstack11ll11l11_opy_ = os.getcwd()
  bstack11l1ll111l_opy_ = bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬࣞ")
  bstack1l1111lll1_opy_ = bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡥࡲࡲࠧࣟ")
  while (not os.path.exists(bstack1llll1l_opy_)) and bstack11ll11l11_opy_ != bstack1111l_opy_ (u"ࠦࠧ࣠"):
    bstack1llll1l_opy_ = os.path.join(bstack11ll11l11_opy_, bstack11l1ll111l_opy_)
    if not os.path.exists(bstack1llll1l_opy_):
      bstack1llll1l_opy_ = os.path.join(bstack11ll11l11_opy_, bstack1l1111lll1_opy_)
    if bstack11ll11l11_opy_ != os.path.dirname(bstack11ll11l11_opy_):
      bstack11ll11l11_opy_ = os.path.dirname(bstack11ll11l11_opy_)
    else:
      bstack11ll11l11_opy_ = bstack1111l_opy_ (u"ࠧࠨ࣡")
  bstack11ll1llll_opy_ = bstack1llll1l_opy_ if os.path.exists(bstack1llll1l_opy_) else None
  return bstack11ll1llll_opy_
def bstack1ll1l11l1_opy_(config):
    if bstack1111l_opy_ (u"࠭ࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬࠭࣢") in config:
      config[bstack1111l_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࣣࠫ")] = config[bstack1111l_opy_ (u"ࠨࡶࡨࡷࡹࡘࡥࡱࡱࡵࡸ࡮ࡴࡧࠨࣤ")]
    if bstack1111l_opy_ (u"ࠩࡷࡩࡸࡺࡒࡦࡲࡲࡶࡹ࡯࡮ࡨࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣥ") in config:
      config[bstack1111l_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࣦࠧ")] = config[bstack1111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࡓࡵࡺࡩࡰࡰࡶࠫࣧ")]
def bstack1l1lll1l_opy_():
  bstack1llll1l_opy_ = bstack111l1l1lll_opy_()
  if not os.path.exists(bstack1llll1l_opy_):
    bstack111llll1ll_opy_(
      bstack1lll1l111l_opy_.format(os.getcwd()))
  try:
    with open(bstack1llll1l_opy_, bstack1111l_opy_ (u"ࠬࡸࠧࣨ")) as stream:
      yaml.add_implicit_resolver(bstack1111l_opy_ (u"ࠨࠡࡱࡣࡷ࡬ࡪࡾࣩࠢ"), bstack11111l111_opy_)
      yaml.add_constructor(bstack1111l_opy_ (u"ࠢࠢࡲࡤࡸ࡭࡫ࡸࠣ࣪"), bstack1ll11111ll_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      bstack1ll1l11l1_opy_(config)
      return config
  except:
    with open(bstack1llll1l_opy_, bstack1111l_opy_ (u"ࠨࡴࠪ࣫")) as stream:
      try:
        config = yaml.safe_load(stream)
        bstack1ll1l11l1_opy_(config)
        return config
      except yaml.YAMLError as exc:
        bstack111llll1ll_opy_(bstack1l1l1l1lll_opy_.format(str(exc)))
def bstack1l1ll11l1_opy_(config):
  bstack1l1ll111l1_opy_ = bstack1lll11ll1l_opy_(config)
  for option in list(bstack1l1ll111l1_opy_):
    if option.lower() in bstack1l1l11l1_opy_ and option != bstack1l1l11l1_opy_[option.lower()]:
      bstack1l1ll111l1_opy_[bstack1l1l11l1_opy_[option.lower()]] = bstack1l1ll111l1_opy_[option]
      del bstack1l1ll111l1_opy_[option]
  return config
def bstack111ll11lll_opy_():
  global bstack1llll1111l_opy_
  for key, bstack1lll11lll1_opy_ in bstack1l11l11lll_opy_.items():
    if isinstance(bstack1lll11lll1_opy_, list):
      for var in bstack1lll11lll1_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1llll1111l_opy_[key] = os.environ[var]
          break
    elif bstack1lll11lll1_opy_ in os.environ and os.environ[bstack1lll11lll1_opy_] and str(os.environ[bstack1lll11lll1_opy_]).strip():
      bstack1llll1111l_opy_[key] = os.environ[bstack1lll11lll1_opy_]
  if bstack1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ࣬") in os.environ:
    bstack1llll1111l_opy_[bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹ࣭ࠧ")] = {}
    bstack1llll1111l_opy_[bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ࣮")][bstack1111l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣯ࠧ")] = os.environ[bstack1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨࣰ")]
def bstack11l111ll_opy_():
  global bstack11l1llll_opy_
  global bstack111ll111l1_opy_
  global bstack1lll1lll11_opy_
  bstack1llll1111_opy_ = []
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) - 1 and bstack1111l_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࣱࠪ").lower() == val.lower():
      bstack11l1llll_opy_[bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࣲࠬ")] = {}
      bstack11l1llll_opy_[bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࣳ")][bstack1111l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣴ")] = sys.argv[idx + 1]
      bstack1llll1111_opy_.extend([idx, idx + 1])
      break
  for key, bstack1lll1l111_opy_ in bstack11l1l11111_opy_.items():
    if isinstance(bstack1lll1l111_opy_, list):
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        for var in bstack1lll1l111_opy_:
          if bstack1111l_opy_ (u"ࠫ࠲࠳ࠧࣵ") + var.lower() == val.lower() and key not in bstack11l1llll_opy_:
            bstack11l1llll_opy_[key] = sys.argv[idx + 1]
            bstack111ll111l1_opy_ += bstack1111l_opy_ (u"ࠬࠦ࠭࠮ࣶࠩ") + var + bstack1111l_opy_ (u"࠭ࠠࠨࣷ") + shlex.quote(sys.argv[idx + 1])
            bstack11111ll1_opy_(bstack1lll1lll11_opy_, key, sys.argv[idx + 1])
            bstack1llll1111_opy_.extend([idx, idx + 1])
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        if bstack1111l_opy_ (u"ࠧ࠮࠯ࠪࣸ") + bstack1lll1l111_opy_.lower() == val.lower() and key not in bstack11l1llll_opy_:
          bstack11l1llll_opy_[key] = sys.argv[idx + 1]
          bstack111ll111l1_opy_ += bstack1111l_opy_ (u"ࠨࠢ࠰࠱ࣹࠬ") + bstack1lll1l111_opy_ + bstack1111l_opy_ (u"ࣺࠩࠣࠫ") + shlex.quote(sys.argv[idx + 1])
          bstack11111ll1_opy_(bstack1lll1lll11_opy_, key, sys.argv[idx + 1])
          bstack1llll1111_opy_.extend([idx, idx + 1])
  for idx in sorted(set(bstack1llll1111_opy_), reverse=True):
    if idx < len(sys.argv):
      del sys.argv[idx]
def bstack1ll1lll1l1_opy_(config):
  bstack11111llll1_opy_ = config.keys()
  for bstack11l11l11l_opy_, bstack11l1l11ll1_opy_ in bstack1l1l11111l_opy_.items():
    if bstack11l1l11ll1_opy_ in bstack11111llll1_opy_:
      config[bstack11l11l11l_opy_] = config[bstack11l1l11ll1_opy_]
      del config[bstack11l1l11ll1_opy_]
  for bstack11l11l11l_opy_, bstack11l1l11ll1_opy_ in bstack11lll1l1l_opy_.items():
    if isinstance(bstack11l1l11ll1_opy_, list):
      for bstack1lllll11l_opy_ in bstack11l1l11ll1_opy_:
        if bstack1lllll11l_opy_ in bstack11111llll1_opy_:
          config[bstack11l11l11l_opy_] = config[bstack1lllll11l_opy_]
          del config[bstack1lllll11l_opy_]
          break
    elif bstack11l1l11ll1_opy_ in bstack11111llll1_opy_:
      config[bstack11l11l11l_opy_] = config[bstack11l1l11ll1_opy_]
      del config[bstack11l1l11ll1_opy_]
  for bstack1lllll11l_opy_ in list(config):
    for bstack1l1111lll_opy_ in bstack11l1l1111l_opy_:
      if bstack1lllll11l_opy_.lower() == bstack1l1111lll_opy_.lower() and bstack1lllll11l_opy_ != bstack1l1111lll_opy_:
        config[bstack1l1111lll_opy_] = config[bstack1lllll11l_opy_]
        del config[bstack1lllll11l_opy_]
  bstack11l1111l1_opy_ = [{}]
  if not config.get(bstack1111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣻ")):
    config[bstack1111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣼ")] = [{}]
  bstack11l1111l1_opy_ = config[bstack1111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨࣽ")]
  for platform in bstack11l1111l1_opy_:
    for bstack1lllll11l_opy_ in list(platform):
      for bstack1l1111lll_opy_ in bstack11l1l1111l_opy_:
        if bstack1lllll11l_opy_.lower() == bstack1l1111lll_opy_.lower() and bstack1lllll11l_opy_ != bstack1l1111lll_opy_:
          platform[bstack1l1111lll_opy_] = platform[bstack1lllll11l_opy_]
          del platform[bstack1lllll11l_opy_]
  for bstack11l11l11l_opy_, bstack11l1l11ll1_opy_ in bstack11lll1l1l_opy_.items():
    for platform in bstack11l1111l1_opy_:
      if isinstance(bstack11l1l11ll1_opy_, list):
        for bstack1lllll11l_opy_ in bstack11l1l11ll1_opy_:
          if bstack1lllll11l_opy_ in platform:
            platform[bstack11l11l11l_opy_] = platform[bstack1lllll11l_opy_]
            del platform[bstack1lllll11l_opy_]
            break
      elif bstack11l1l11ll1_opy_ in platform:
        platform[bstack11l11l11l_opy_] = platform[bstack11l1l11ll1_opy_]
        del platform[bstack11l1l11ll1_opy_]
  for bstack1lll11l11l_opy_ in bstack11l111lll1_opy_:
    if bstack1lll11l11l_opy_ in config:
      if not bstack11l111lll1_opy_[bstack1lll11l11l_opy_] in config:
        config[bstack11l111lll1_opy_[bstack1lll11l11l_opy_]] = {}
      config[bstack11l111lll1_opy_[bstack1lll11l11l_opy_]].update(config[bstack1lll11l11l_opy_])
      del config[bstack1lll11l11l_opy_]
  for platform in bstack11l1111l1_opy_:
    for bstack1lll11l11l_opy_ in bstack11l111lll1_opy_:
      if bstack1lll11l11l_opy_ in list(platform):
        if not bstack11l111lll1_opy_[bstack1lll11l11l_opy_] in platform:
          platform[bstack11l111lll1_opy_[bstack1lll11l11l_opy_]] = {}
        platform[bstack11l111lll1_opy_[bstack1lll11l11l_opy_]].update(platform[bstack1lll11l11l_opy_])
        del platform[bstack1lll11l11l_opy_]
  config = bstack1l1ll11l1_opy_(config)
  return config
def bstack1ll1l1l1l1_opy_(config):
  global bstack1l1l111ll_opy_
  bstack111l111l_opy_ = False
  if bstack1111l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪࣾ") in config and str(config[bstack1111l_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫࣿ")]).lower() != bstack1111l_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧऀ"):
    if bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ँ") not in config or str(config[bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧं")]).lower() == bstack1111l_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪः"):
      config[bstack1111l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫऄ")] = False
    else:
      bstack11l11ll11l_opy_ = bstack1l1l1111_opy_()
      if bstack1111l_opy_ (u"࠭ࡩࡴࡖࡵ࡭ࡦࡲࡇࡳ࡫ࡧࠫअ") in bstack11l11ll11l_opy_:
        if not bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫआ") in config:
          config[bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬइ")] = {}
        config[bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ई")][bstack1111l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬउ")] = bstack1111l_opy_ (u"ࠫࡦࡺࡳ࠮ࡴࡨࡴࡪࡧࡴࡦࡴࠪऊ")
        bstack111l111l_opy_ = True
        bstack1l1l111ll_opy_ = config[bstack1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩऋ")].get(bstack1111l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨऌ"))
  if bstack11l1ll11ll_opy_(config) and bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫऍ") in config and str(config[bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬऎ")]).lower() != bstack1111l_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨए") and not bstack111l111l_opy_:
    if not bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧऐ") in config:
      config[bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऑ")] = {}
    if not config[bstack1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩऒ")].get(bstack1111l_opy_ (u"࠭ࡳ࡬࡫ࡳࡆ࡮ࡴࡡࡳࡻࡌࡲ࡮ࡺࡩࡢ࡮࡬ࡷࡦࡺࡩࡰࡰࠪओ")) and not bstack1111l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऔ") in config[bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬक")]:
      current_time = datetime.datetime.now()
      bstack1ll11llll1_opy_ = current_time.strftime(bstack1111l_opy_ (u"ࠩࠨࡨࡤࠫࡢࡠࠧࡋࠩࡒ࠭ख"))
      hostname = socket.gethostname()
      bstack1111lllll_opy_ = bstack1111l_opy_ (u"ࠪࠫग").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1111l_opy_ (u"ࠫࢀࢃ࡟ࡼࡿࡢࡿࢂ࠭घ").format(bstack1ll11llll1_opy_, hostname, bstack1111lllll_opy_)
      config[bstack1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩङ")][bstack1111l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨच")] = identifier
    bstack1l1l111ll_opy_ = config[bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫछ")].get(bstack1111l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪज"))
  return config
def bstack1l11l1lll_opy_():
  bstack1l111ll1_opy_ =  bstack11llll111_opy_()[bstack1111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠨझ")]
  return bstack1l111ll1_opy_ if bstack1l111ll1_opy_ else -1
def bstack111111111_opy_(bstack1l111ll1_opy_):
  global CONFIG
  if not bstack1111l_opy_ (u"ࠪࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬञ") in CONFIG[bstack1111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ट")]:
    return
  CONFIG[bstack1111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧठ")] = CONFIG[bstack1111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨड")].replace(
    bstack1111l_opy_ (u"ࠧࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩढ"),
    str(bstack1l111ll1_opy_)
  )
def bstack11l1lll11_opy_():
  global CONFIG
  if not bstack1111l_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧण") in CONFIG[bstack1111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫत")]:
    return
  current_time = datetime.datetime.now()
  bstack1ll11llll1_opy_ = current_time.strftime(bstack1111l_opy_ (u"ࠪࠩࡩ࠳ࠥࡣ࠯ࠨࡌ࠿ࠫࡍࠨथ"))
  CONFIG[bstack1111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭द")] = CONFIG[bstack1111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧध")].replace(
    bstack1111l_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬन"),
    bstack1ll11llll1_opy_
  )
def bstack1111l1111l_opy_():
  global CONFIG
  if bstack1111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऩ") in CONFIG and not bool(CONFIG[bstack1111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪप")]):
    del CONFIG[bstack1111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫफ")]
    return
  if not bstack1111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬब") in CONFIG:
    CONFIG[bstack1111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭भ")] = bstack1111l_opy_ (u"ࠬࠩࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨम")
  if bstack1111l_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬय") in CONFIG[bstack1111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩर")]:
    bstack11l1lll11_opy_()
    os.environ[bstack1111l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬऱ")] = CONFIG[bstack1111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫल")]
  if not bstack1111l_opy_ (u"ࠪࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬळ") in CONFIG[bstack1111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ऴ")]:
    return
  bstack1l111ll1_opy_ = bstack1111l_opy_ (u"ࠬ࠭व")
  bstack11l1l11l1l_opy_ = bstack1l11l1lll_opy_()
  if bstack11l1l11l1l_opy_ != -1:
    bstack1l111ll1_opy_ = bstack1111l_opy_ (u"࠭ࡃࡊࠢࠪश") + str(bstack11l1l11l1l_opy_)
  if bstack1l111ll1_opy_ == bstack1111l_opy_ (u"ࠧࠨष"):
    bstack1lll11l11_opy_ = bstack1ll1llll11_opy_(CONFIG[bstack1111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫस")])
    if bstack1lll11l11_opy_ != -1:
      bstack1l111ll1_opy_ = str(bstack1lll11l11_opy_)
  if bstack1l111ll1_opy_:
    bstack111111111_opy_(bstack1l111ll1_opy_)
    os.environ[bstack1111l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ह")] = CONFIG[bstack1111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬऺ")]
def bstack1lll111ll_opy_(bstack1ll111l1l_opy_, bstack111ll1l11_opy_, path):
  json_data = {
    bstack1111l_opy_ (u"ࠫ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨऻ"): bstack111ll1l11_opy_
  }
  if os.path.exists(path):
    bstack1l1lll1ll1_opy_ = json.load(open(path, bstack1111l_opy_ (u"ࠬࡸࡢࠨ़")))
  else:
    bstack1l1lll1ll1_opy_ = {}
  bstack1l1lll1ll1_opy_[bstack1ll111l1l_opy_] = json_data
  with open(path, bstack1111l_opy_ (u"ࠨࡷࠬࠤऽ")) as outfile:
    json.dump(bstack1l1lll1ll1_opy_, outfile)
def bstack1ll1llll11_opy_(bstack1ll111l1l_opy_):
  bstack1ll111l1l_opy_ = str(bstack1ll111l1l_opy_)
  bstack111lll11ll_opy_ = os.path.join(os.path.expanduser(bstack1111l_opy_ (u"ࠧࡿࠩा")), bstack1111l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨि"))
  try:
    if not os.path.exists(bstack111lll11ll_opy_):
      os.makedirs(bstack111lll11ll_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1111l_opy_ (u"ࠩࢁࠫी")), bstack1111l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪु"), bstack1111l_opy_ (u"ࠫ࠳ࡨࡵࡪ࡮ࡧ࠱ࡳࡧ࡭ࡦ࠯ࡦࡥࡨ࡮ࡥ࠯࡬ࡶࡳࡳ࠭ू"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1111l_opy_ (u"ࠬࡽࠧृ")):
        pass
      with open(file_path, bstack1111l_opy_ (u"ࠨࡷࠬࠤॄ")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1111l_opy_ (u"ࠧࡳࠩॅ")) as bstack111ll1ll1l_opy_:
      bstack11l11lllll_opy_ = json.load(bstack111ll1ll1l_opy_)
    if bstack1ll111l1l_opy_ in bstack11l11lllll_opy_:
      bstack1ll111111_opy_ = bstack11l11lllll_opy_[bstack1ll111l1l_opy_][bstack1111l_opy_ (u"ࠨ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬॆ")]
      bstack1ll1l1l1ll_opy_ = int(bstack1ll111111_opy_) + 1
      bstack1lll111ll_opy_(bstack1ll111l1l_opy_, bstack1ll1l1l1ll_opy_, file_path)
      return bstack1ll1l1l1ll_opy_
    else:
      bstack1lll111ll_opy_(bstack1ll111l1l_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warning(bstack11l1lllll_opy_.format(str(e)))
    return -1
def bstack11l11ll1ll_opy_(config):
  if not config[bstack1111l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫे")] or not config[bstack1111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ै")]:
    return True
  else:
    return False
def bstack1l11l11ll_opy_(config, index=0):
  global bstack1l1111111l_opy_
  bstack11llll11ll_opy_ = {}
  caps = bstack11l11l1l11_opy_ + bstack1111l1ll1l_opy_
  if config.get(bstack1111l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨॉ"), False):
    bstack11llll11ll_opy_[bstack1111l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩॊ")] = True
    bstack11llll11ll_opy_[bstack1111l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪो")] = config.get(bstack1111l_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࡓࡵࡺࡩࡰࡰࡶࠫौ"), {})
  if bstack1l1111111l_opy_:
    caps += bstack1ll1llllll_opy_
  for key in config:
    if key in caps + [bstack1111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶ्ࠫ")]:
      continue
    bstack11llll11ll_opy_[key] = config[key]
  if bstack1111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॎ") in config:
    for bstack1llll11lll_opy_ in config[bstack1111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॏ")][index]:
      if bstack1llll11lll_opy_ in caps:
        continue
      bstack11llll11ll_opy_[bstack1llll11lll_opy_] = config[bstack1111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॐ")][index][bstack1llll11lll_opy_]
  bstack11llll11ll_opy_[bstack1111l_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧ॑")] = socket.gethostname()
  if bstack1111l_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴ॒ࠧ") in bstack11llll11ll_opy_:
    del (bstack11llll11ll_opy_[bstack1111l_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨ॓")])
  return bstack11llll11ll_opy_
def bstack1111l11l1_opy_(config):
  global bstack1l1111111l_opy_
  bstack1l1l11l1ll_opy_ = {}
  caps = bstack1111l1ll1l_opy_
  if bstack1l1111111l_opy_:
    caps += bstack1ll1llllll_opy_
  for key in caps:
    if key in config:
      bstack1l1l11l1ll_opy_[key] = config[key]
  return bstack1l1l11l1ll_opy_
def bstack111l11l111_opy_(bstack11llll11ll_opy_, bstack1l1l11l1ll_opy_):
  bstack1l1lll1l1_opy_ = {}
  for key in bstack11llll11ll_opy_.keys():
    if key in bstack1l1l11111l_opy_:
      bstack1l1lll1l1_opy_[bstack1l1l11111l_opy_[key]] = bstack11llll11ll_opy_[key]
    else:
      bstack1l1lll1l1_opy_[key] = bstack11llll11ll_opy_[key]
  for key in bstack1l1l11l1ll_opy_:
    if key in bstack1l1l11111l_opy_:
      bstack1l1lll1l1_opy_[bstack1l1l11111l_opy_[key]] = bstack1l1l11l1ll_opy_[key]
    else:
      bstack1l1lll1l1_opy_[key] = bstack1l1l11l1ll_opy_[key]
  return bstack1l1lll1l1_opy_
def get_caps(config, index=0):
  global bstack1l1111111l_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack1l11l11ll1_opy_ = bstack1ll111l1_opy_(bstack1111ll1lll_opy_, config, logger)
  bstack1l1l11l1ll_opy_ = bstack1111l11l1_opy_(config)
  bstack1ll11l1l1_opy_ = bstack1111l1ll1l_opy_
  bstack1ll11l1l1_opy_ += bstack11l1111l1l_opy_
  bstack1l1l11l1ll_opy_ = update(bstack1l1l11l1ll_opy_, bstack1l11l11ll1_opy_)
  if bstack1l1111111l_opy_:
    bstack1ll11l1l1_opy_ += bstack1ll1llllll_opy_
  if bstack1111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ॔") in config:
    if bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧॕ") in config[bstack1111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॖ")][index]:
      caps[bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩॗ")] = config[bstack1111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨक़")][index][bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫख़")]
    if bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨग़") in config[bstack1111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫज़")][index]:
      caps[bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪड़")] = str(config[bstack1111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ढ़")][index][bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬफ़")])
    bstack111ll1lll_opy_ = bstack1ll111l1_opy_(bstack1111ll1lll_opy_, config[bstack1111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨय़")][index], logger)
    bstack1ll11l1l1_opy_ += list(bstack111ll1lll_opy_.keys())
    for bstack11l111l1l1_opy_ in bstack1ll11l1l1_opy_:
      if bstack11l111l1l1_opy_ in config[bstack1111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩॠ")][index]:
        if bstack11l111l1l1_opy_ == bstack1111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩॡ"):
          try:
            bstack111ll1lll_opy_[bstack11l111l1l1_opy_] = str(config[bstack1111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫॢ")][index][bstack11l111l1l1_opy_] * 1.0)
          except:
            bstack111ll1lll_opy_[bstack11l111l1l1_opy_] = str(config[bstack1111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॣ")][index][bstack11l111l1l1_opy_])
        else:
          bstack111ll1lll_opy_[bstack11l111l1l1_opy_] = config[bstack1111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭।")][index][bstack11l111l1l1_opy_]
        del (config[bstack1111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ॥")][index][bstack11l111l1l1_opy_])
    bstack1l1l11l1ll_opy_ = update(bstack1l1l11l1ll_opy_, bstack111ll1lll_opy_)
  bstack11llll11ll_opy_ = bstack1l11l11ll_opy_(config, index)
  for bstack1lllll11l_opy_ in bstack1111l1ll1l_opy_ + list(bstack1l11l11ll1_opy_.keys()):
    if bstack1lllll11l_opy_ in bstack11llll11ll_opy_:
      bstack1l1l11l1ll_opy_[bstack1lllll11l_opy_] = bstack11llll11ll_opy_[bstack1lllll11l_opy_]
      del (bstack11llll11ll_opy_[bstack1lllll11l_opy_])
  if bstack11l1111l_opy_(config):
    bstack11llll11ll_opy_[bstack1111l_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ०")] = True
    caps.update(bstack1l1l11l1ll_opy_)
    caps[bstack1111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ१")] = bstack11llll11ll_opy_
  else:
    bstack11llll11ll_opy_[bstack1111l_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧ२")] = False
    caps.update(bstack111l11l111_opy_(bstack11llll11ll_opy_, bstack1l1l11l1ll_opy_))
    if bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭३") in caps:
      caps[bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪ४")] = caps[bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ५")]
      del (caps[bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ६")])
    if bstack1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭७") in caps:
      caps[bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ८")] = caps[bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ९")]
      del (caps[bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ॰")])
  return caps
def bstack1ll11l111l_opy_():
  global bstack11l11lll11_opy_
  global CONFIG
  if bstack11l11lll11_opy_ != bstack1111l_opy_ (u"ࠩࠪॱ") and (bstack11l11lll11_opy_.startswith(bstack1111l_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫॲ")) or bstack11l11lll11_opy_.startswith(bstack1111l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࠭ॳ"))):
    return bstack11l11lll11_opy_
  if bstack1l1ll1ll1l_opy_() <= version.parse(bstack1111l_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬॴ")):
    if bstack11l11lll11_opy_ != bstack1111l_opy_ (u"࠭ࠧॵ"):
      return bstack1111l_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣॶ") + bstack11l11lll11_opy_ + bstack1111l_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧॷ")
    return bstack11l1l111l1_opy_
  if bstack11l11lll11_opy_ != bstack1111l_opy_ (u"ࠩࠪॸ"):
    return bstack1111l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧॹ") + bstack11l11lll11_opy_ + bstack1111l_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧॺ")
  return HTTPS_HUB
def bstack11lllll11_opy_(options):
  return hasattr(options, bstack1111l_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭ॻ"))
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
def bstack1lll1lll1l_opy_(options, bstack11l111111_opy_):
  for bstack1llll1lll_opy_ in bstack11l111111_opy_:
    if bstack1llll1lll_opy_ in [bstack1111l_opy_ (u"࠭ࡡࡳࡩࡶࠫॼ"), bstack1111l_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫॽ")]:
      continue
    if bstack1llll1lll_opy_ in options._experimental_options:
      options._experimental_options[bstack1llll1lll_opy_] = update(options._experimental_options[bstack1llll1lll_opy_],
                                                         bstack11l111111_opy_[bstack1llll1lll_opy_])
    else:
      options.add_experimental_option(bstack1llll1lll_opy_, bstack11l111111_opy_[bstack1llll1lll_opy_])
  if bstack1111l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ॾ") in bstack11l111111_opy_:
    for arg in bstack11l111111_opy_[bstack1111l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॿ")]:
      options.add_argument(arg)
    del (bstack11l111111_opy_[bstack1111l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨঀ")])
  if bstack1111l_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨঁ") in bstack11l111111_opy_:
    for ext in bstack11l111111_opy_[bstack1111l_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩং")]:
      try:
        options.add_extension(ext)
      except OSError:
        options.add_encoded_extension(ext)
    del (bstack11l111111_opy_[bstack1111l_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪঃ")])
def bstack11l1111l11_opy_(options):
  global CONFIG
  global bstack11l1l1l1l_opy_
  try:
    if not bstack11l1l1l1l_opy_ or not options:
      return options
    from bstack_utils.bstack11lll11l11_opy_ import bstack1l111l11l_opy_
    bstack1l1lllll11_opy_ = bstack1l111l11l_opy_(options, bstack1l11ll111_opy_=bstack1111l_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢ঄"))
    if bstack1l1lllll11_opy_ > 0:
      logger.debug(bstack1111l_opy_ (u"ࠣࡎࡲࡥࡩࠦࡴࡦࡵࡷ࡭ࡳ࡭࠺ࠡࡃࡧࡨࡪࡪࠠࡼࡿࠣࡨࡪ࡬ࡡࡶ࡮ࡷࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠠࡧࡱࡵࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠦঅ").format(bstack1l1lllll11_opy_))
  except Exception as e:
    logger.debug(bstack1111l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡯࡮࡫ࡧࡦࡸࠥࡲ࡯ࡢࡦࠣࡸࡪࡹࡴࡪࡰࡪࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡴࡶࡴࡪࡱࡱࡷ࠿ࠦࡻࡾࠤআ").format(e))
  return options
def bstack11ll11ll11_opy_(options, bstack1111l1l1ll_opy_):
  if bstack1111l_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩই") in bstack1111l1l1ll_opy_:
    for bstack11llllll1l_opy_ in bstack1111l1l1ll_opy_[bstack1111l_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪঈ")]:
      if bstack11llllll1l_opy_ in options._preferences:
        options._preferences[bstack11llllll1l_opy_] = update(options._preferences[bstack11llllll1l_opy_], bstack1111l1l1ll_opy_[bstack1111l_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫউ")][bstack11llllll1l_opy_])
      else:
        options.set_preference(bstack11llllll1l_opy_, bstack1111l1l1ll_opy_[bstack1111l_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬঊ")][bstack11llllll1l_opy_])
  if bstack1111l_opy_ (u"ࠧࡢࡴࡪࡷࠬঋ") in bstack1111l1l1ll_opy_:
    for arg in bstack1111l1l1ll_opy_[bstack1111l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ঌ")]:
      options.add_argument(arg)
def bstack1lll11l1ll_opy_(options, bstack1l1l11l11_opy_):
  if bstack1111l_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࠪ঍") in bstack1l1l11l11_opy_:
    options.use_webview(bool(bstack1l1l11l11_opy_[bstack1111l_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࠫ঎")]))
  bstack1lll1lll1l_opy_(options, bstack1l1l11l11_opy_)
def bstack1lll111ll1_opy_(options, bstack1l111l1l_opy_):
  for bstack111l1l1111_opy_ in bstack1l111l1l_opy_:
    if bstack111l1l1111_opy_ in [bstack1111l_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨএ"), bstack1111l_opy_ (u"ࠬࡧࡲࡨࡵࠪঐ")]:
      continue
    options.set_capability(bstack111l1l1111_opy_, bstack1l111l1l_opy_[bstack111l1l1111_opy_])
  if bstack1111l_opy_ (u"࠭ࡡࡳࡩࡶࠫ঑") in bstack1l111l1l_opy_:
    for arg in bstack1l111l1l_opy_[bstack1111l_opy_ (u"ࠧࡢࡴࡪࡷࠬ঒")]:
      options.add_argument(arg)
  if bstack1111l_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬও") in bstack1l111l1l_opy_:
    options.bstack11l1l1ll1l_opy_(bool(bstack1l111l1l_opy_[bstack1111l_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭ঔ")]))
def bstack1111llll_opy_(options, bstack1ll1ll1l11_opy_):
  for bstack1l111111_opy_ in bstack1ll1ll1l11_opy_:
    if bstack1l111111_opy_ in [bstack1111l_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧক"), bstack1111l_opy_ (u"ࠫࡦࡸࡧࡴࠩখ")]:
      continue
    options._options[bstack1l111111_opy_] = bstack1ll1ll1l11_opy_[bstack1l111111_opy_]
  if bstack1111l_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩগ") in bstack1ll1ll1l11_opy_:
    for bstack1l1l1ll1l1_opy_ in bstack1ll1ll1l11_opy_[bstack1111l_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪঘ")]:
      options.bstack11llll111l_opy_(
        bstack1l1l1ll1l1_opy_, bstack1ll1ll1l11_opy_[bstack1111l_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫঙ")][bstack1l1l1ll1l1_opy_])
  if bstack1111l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭চ") in bstack1ll1ll1l11_opy_:
    for arg in bstack1ll1ll1l11_opy_[bstack1111l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧছ")]:
      options.add_argument(arg)
def bstack11111111l_opy_(options, caps):
  if not hasattr(options, bstack1111l_opy_ (u"ࠪࡏࡊ࡟ࠧজ")):
    return
  if options.KEY == bstack1111l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩঝ"):
    options = a11y.bstack111l1l11ll_opy_(bstack111ll11l1_opy_=options, config=CONFIG)
  if options.KEY == bstack1111l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪঞ") and options.KEY in caps:
    bstack1lll1lll1l_opy_(options, caps[bstack1111l_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫট")])
  elif options.KEY == bstack1111l_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬঠ") and options.KEY in caps:
    bstack11ll11ll11_opy_(options, caps[bstack1111l_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ড")])
  elif options.KEY == bstack1111l_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪঢ") and options.KEY in caps:
    bstack1lll111ll1_opy_(options, caps[bstack1111l_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫণ")])
  elif options.KEY == bstack1111l_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬত") and options.KEY in caps:
    bstack1lll11l1ll_opy_(options, caps[bstack1111l_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭থ")])
  elif options.KEY == bstack1111l_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬদ") and options.KEY in caps:
    bstack1111llll_opy_(options, caps[bstack1111l_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ধ")])
def bstack1l11l1111l_opy_(caps):
  global bstack1l1111111l_opy_
  if isinstance(os.environ.get(bstack1111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩন")), str):
    bstack1l1111111l_opy_ = eval(os.getenv(bstack1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ঩")))
  if bstack1l1111111l_opy_:
    if bstack1l1llll1l1_opy_() < version.parse(bstack1111l_opy_ (u"ࠪ࠶࠳࠹࠮࠱ࠩপ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1111l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫফ")
    if bstack1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪব") in caps:
      browser = caps[bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫভ")]
    elif bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨম") in caps:
      browser = caps[bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩয")]
    browser = str(browser).lower()
    if browser == bstack1111l_opy_ (u"ࠩ࡬ࡴ࡭ࡵ࡮ࡦࠩর") or browser == bstack1111l_opy_ (u"ࠪ࡭ࡵࡧࡤࠨ঱"):
      browser = bstack1111l_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫল")
    if browser == bstack1111l_opy_ (u"ࠬࡹࡡ࡮ࡵࡸࡲ࡬࠭঳"):
      browser = bstack1111l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭঴")
    if browser not in [bstack1111l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ঵"), bstack1111l_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭শ"), bstack1111l_opy_ (u"ࠩ࡬ࡩࠬষ"), bstack1111l_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪস"), bstack1111l_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬহ")]:
      return None
    try:
      package = bstack1111l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡿࢂ࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧ঺").format(browser)
      name = bstack1111l_opy_ (u"࠭ࡏࡱࡶ࡬ࡳࡳࡹࠧ঻")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack11lllll11_opy_(options):
        return None
      for bstack1lllll11l_opy_ in caps.keys():
        options.set_capability(bstack1lllll11l_opy_, caps[bstack1lllll11l_opy_])
      bstack11111111l_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1111l11ll_opy_(options, bstack1ll11lll11_opy_):
  if not bstack11lllll11_opy_(options):
    return
  for bstack1lllll11l_opy_ in bstack1ll11lll11_opy_.keys():
    if bstack1lllll11l_opy_ in bstack11l1111l1l_opy_:
      continue
    if bstack1lllll11l_opy_ in options._caps and type(options._caps[bstack1lllll11l_opy_]) in [dict, list]:
      options._caps[bstack1lllll11l_opy_] = update(options._caps[bstack1lllll11l_opy_], bstack1ll11lll11_opy_[bstack1lllll11l_opy_])
    else:
      options.set_capability(bstack1lllll11l_opy_, bstack1ll11lll11_opy_[bstack1lllll11l_opy_])
  bstack11111111l_opy_(options, bstack1ll11lll11_opy_)
  if bstack1111l_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ়࠭") in options._caps:
    if options._caps[bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ঽ")] and options._caps[bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧা")].lower() != bstack1111l_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫি"):
      del options._caps[bstack1111l_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪী")]
def bstack1llll1ll11_opy_(proxy_config):
  if bstack1111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩু") in proxy_config:
    proxy_config[bstack1111l_opy_ (u"࠭ࡳࡴ࡮ࡓࡶࡴࡾࡹࠨূ")] = proxy_config[bstack1111l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫৃ")]
    del (proxy_config[bstack1111l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬৄ")])
  if bstack1111l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬ৅") in proxy_config and proxy_config[bstack1111l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭৆")].lower() != bstack1111l_opy_ (u"ࠫࡩ࡯ࡲࡦࡥࡷࠫে"):
    proxy_config[bstack1111l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨৈ")] = bstack1111l_opy_ (u"࠭࡭ࡢࡰࡸࡥࡱ࠭৉")
  if bstack1111l_opy_ (u"ࠧࡱࡴࡲࡼࡾࡇࡵࡵࡱࡦࡳࡳ࡬ࡩࡨࡗࡵࡰࠬ৊") in proxy_config:
    proxy_config[bstack1111l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫো")] = bstack1111l_opy_ (u"ࠩࡳࡥࡨ࠭ৌ")
  return proxy_config
def bstack11l11l1ll_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1111l_opy_ (u"ࠪࡴࡷࡵࡸࡺ্ࠩ") in config:
    return proxy
  config[bstack1111l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪৎ")] = bstack1llll1ll11_opy_(config[bstack1111l_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ৏")])
  if proxy == None:
    proxy = Proxy(config[bstack1111l_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ৐")])
  return proxy
def bstack1111l11ll1_opy_(self):
  global CONFIG
  global bstack1l1l111l1l_opy_
  try:
    proxy = bstack11ll1lllll_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1111l_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ৑")):
        proxies = bstack1llll1l1ll_opy_(proxy, bstack1ll11l111l_opy_())
        if len(proxies) > 0:
          protocol, bstack11llll1l1_opy_ = proxies.popitem()
          if bstack1111l_opy_ (u"ࠣ࠼࠲࠳ࠧ৒") in bstack11llll1l1_opy_:
            return bstack11llll1l1_opy_
          else:
            return bstack1111l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ৓") + bstack11llll1l1_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1111l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡰࡳࡱࡻࡽࠥࡻࡲ࡭ࠢ࠽ࠤࢀࢃࠢ৔").format(str(e)))
  return bstack1l1l111l1l_opy_(self)
def bstack1l1ll1l11l_opy_():
  global CONFIG
  return bstack1ll1l1l11l_opy_(CONFIG) and bstack1l11ll1111_opy_() and bstack1l1ll1ll1l_opy_() >= version.parse(bstack11l11ll1_opy_)
def bstack11lllllll1_opy_():
  global CONFIG
  return (bstack1111l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ৕") in CONFIG or bstack1111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ৖") in CONFIG) and bstack1l1l1l1l11_opy_()
def bstack1lll11ll1l_opy_(config):
  bstack1l1ll111l1_opy_ = {}
  if bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪৗ") in config:
    bstack1l1ll111l1_opy_ = config[bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ৘")]
  if bstack1111l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ৙") in config:
    bstack1l1ll111l1_opy_ = config[bstack1111l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ৚")]
  proxy = bstack11ll1lllll_opy_(config)
  if proxy:
    if proxy.endswith(bstack1111l_opy_ (u"ࠪ࠲ࡵࡧࡣࠨ৛")) and os.path.isfile(proxy):
      bstack1l1ll111l1_opy_[bstack1111l_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧড়")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1111l_opy_ (u"ࠬ࠴ࡰࡢࡥࠪঢ়")):
        proxies = bstack1l1l111l11_opy_(config, bstack1ll11l111l_opy_())
        if len(proxies) > 0:
          protocol, bstack11llll1l1_opy_ = proxies.popitem()
          if bstack1111l_opy_ (u"ࠨ࠺࠰࠱ࠥ৞") in bstack11llll1l1_opy_:
            parsed_url = urlparse(bstack11llll1l1_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1111l_opy_ (u"ࠢ࠻࠱࠲ࠦয়") + bstack11llll1l1_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1l1ll111l1_opy_[bstack1111l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡈࡰࡵࡷࠫৠ")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1l1ll111l1_opy_[bstack1111l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬৡ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1l1ll111l1_opy_[bstack1111l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭ৢ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1l1ll111l1_opy_[bstack1111l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧৣ")] = str(parsed_url.password)
  return bstack1l1ll111l1_opy_
def bstack11lllll1ll_opy_(config):
  if bstack1111l_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪ৤") in config:
    return config[bstack1111l_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫ৥")]
  return {}
def update_caps_for_local(caps):
  global bstack1l1l111ll_opy_
  if bstack1111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ০") in caps:
    caps[bstack1111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ১")][bstack1111l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨ২")] = True
    if bstack1l1l111ll_opy_:
      caps[bstack1111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ৩")][bstack1111l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭৪")] = bstack1l1l111ll_opy_
  else:
    caps[bstack1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪ৫")] = True
    if bstack1l1l111ll_opy_:
      caps[bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ৬")] = bstack1l1l111ll_opy_
@measure(event_name=EVENTS.bstack11l1l1ll1_opy_, stage=STAGE.bstack11lll111l_opy_, bstack11lll111_opy_=SESSION_NAME)
def bstack1l1ll11l11_opy_():
  global CONFIG
  if not bstack11l1ll11ll_opy_(CONFIG) or cli.is_enabled(CONFIG):
    return
  if bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ৭") in CONFIG and bstack1ll111llll_opy_(CONFIG[bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ৮")]):
    if (
      bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭৯") in CONFIG
      and bstack1ll111llll_opy_(CONFIG[bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧৰ")].get(bstack1111l_opy_ (u"ࠫࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠨৱ")))
    ):
      logger.debug(bstack1111l_opy_ (u"ࠧࡒ࡯ࡤࡣ࡯ࠤࡧ࡯࡮ࡢࡴࡼࠤࡳࡵࡴࠡࡵࡷࡥࡷࡺࡥࡥࠢࡤࡷࠥࡹ࡫ࡪࡲࡅ࡭ࡳࡧࡲࡺࡋࡱ࡭ࡹ࡯ࡡ࡭࡫ࡶࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠨ৲"))
      return
    bstack1l1ll111l1_opy_ = bstack1lll11ll1l_opy_(CONFIG)
    bstack11l11l1lll_opy_(CONFIG[bstack1111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ৳")], bstack1l1ll111l1_opy_)
def bstack11l11l1lll_opy_(key, bstack1l1ll111l1_opy_):
  global bstack11l1l1lll1_opy_
  logger.info(bstack11l111llll_opy_)
  try:
    bstack11l1l1lll1_opy_ = Local()
    bstack1l111111l1_opy_ = {bstack1111l_opy_ (u"ࠧ࡬ࡧࡼࠫ৴"): key}
    bstack1l111111l1_opy_.update(bstack1l1ll111l1_opy_)
    logger.debug(bstack1l1ll1llll_opy_.format(str(bstack1l111111l1_opy_)).replace(key, bstack1111l_opy_ (u"ࠨ࡝ࡕࡉࡉࡇࡃࡕࡇࡇࡡࠬ৵")))
    bstack11l1l1lll1_opy_.start(**bstack1l111111l1_opy_)
    if bstack11l1l1lll1_opy_.isRunning():
      logger.info(bstack1111lll111_opy_)
  except Exception as e:
    bstack111llll1ll_opy_(bstack111111l1l_opy_.format(str(e)))
def bstack1lll111111_opy_():
  global bstack11l1l1lll1_opy_
  if bstack11l1l1lll1_opy_.isRunning():
    logger.info(bstack11ll1111l1_opy_)
    bstack11l1l1lll1_opy_.stop()
  bstack11l1l1lll1_opy_ = None
def bstack11l1l1l11_opy_(bstack1ll1l1111l_opy_=[]):
  global CONFIG
  bstack1l1l1ll1ll_opy_ = []
  bstack1ll111l11_opy_ = [bstack1111l_opy_ (u"ࠩࡲࡷࠬ৶"), bstack1111l_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭৷"), bstack1111l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨ৸"), bstack1111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ৹"), bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ৺"), bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ৻")]
  try:
    for err in bstack1ll1l1111l_opy_:
      bstack11111l1l1_opy_ = {}
      for k in bstack1ll111l11_opy_:
        val = CONFIG[bstack1111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫৼ")][int(err[bstack1111l_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ৽")])].get(k)
        if val:
          bstack11111l1l1_opy_[k] = val
      if(err[bstack1111l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ৾")] != bstack1111l_opy_ (u"ࠫࠬ৿")):
        bstack11111l1l1_opy_[bstack1111l_opy_ (u"ࠬࡺࡥࡴࡶࡶࠫ਀")] = {
          err[bstack1111l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫਁ")]: err[bstack1111l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ਂ")]
        }
        bstack1l1l1ll1ll_opy_.append(bstack11111l1l1_opy_)
  except Exception as e:
    logger.debug(bstack1111l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪࡴࡸ࡭ࡢࡶࡷ࡭ࡳ࡭ࠠࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴ࠻ࠢࠪਃ") + str(e))
  finally:
    return bstack1l1l1ll1ll_opy_
def bstack1lll11l1l_opy_(file_name):
  bstack1ll1ll11l1_opy_ = []
  try:
    bstack1ll1llll_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1ll1llll_opy_):
      with open(bstack1ll1llll_opy_) as f:
        bstack11llll1l11_opy_ = json.load(f)
        bstack1ll1ll11l1_opy_ = bstack11llll1l11_opy_
      os.remove(bstack1ll1llll_opy_)
    return bstack1ll1ll11l1_opy_
  except Exception as e:
    logger.debug(bstack1111l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡫࡯࡮ࡥ࡫ࡱ࡫ࠥ࡫ࡲࡳࡱࡵࠤࡱ࡯ࡳࡵ࠼ࠣࠫ਄") + str(e))
    return bstack1ll1ll11l1_opy_
def bstack11llllll_opy_():
  try:
      import time
      from bstack_utils.constants import bstack11ll1111ll_opy_, EVENTS
      from bstack_utils.helper import bstack1llll1ll1_opy_, get_host_info, global_config
      from datetime import datetime
      from filelock import FileLock
      from bstack_utils.bstack111l1l1ll1_opy_ import bstack1l11ll1l1_opy_
      bstack1l11ll1l1_opy_.bstack111l111l1_opy_()
      bstack1l1lll11_opy_ = os.path.join(os.getcwd(), bstack1111l_opy_ (u"ࠪࡰࡴ࡭ࠧਅ"), bstack1111l_opy_ (u"ࠫࡰ࡫ࡹ࠮࡯ࡨࡸࡷ࡯ࡣࡴ࠰࡭ࡷࡴࡴࠧਆ"))
      data = None
      lock = FileLock(bstack1l1lll11_opy_+bstack1111l_opy_ (u"ࠧ࠴࡬ࡰࡥ࡮ࠦਇ"), timeout=2)
      try:
          with lock:
              with open(bstack1l1lll11_opy_, bstack1111l_opy_ (u"ࠨࡲࠣਈ"), encoding=bstack1111l_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨਉ")) as file:
                  data = json.load(file)
      except Exception as e:
          logger.debug(bstack1111l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡷ࡫ࡡࡥࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹࠠࡧ࡫࡯ࡩ࠿ࠦࡻࡾࠤਊ").format(e))
          return
      if not data:
          return
      def bstack111lllllll_opy_():
          try:
              config = {
                  bstack1111l_opy_ (u"ࠤ࡫ࡩࡦࡪࡥࡳࡵࠥ਋"): {
                      bstack1111l_opy_ (u"ࠥࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠤ਌"): bstack1111l_opy_ (u"ࠦࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠢ਍"),
                  }
              }
              bstack1111lll1l1_opy_ = datetime.utcnow()
              current_time = bstack1111lll1l1_opy_.strftime(bstack1111l_opy_ (u"࡙ࠧࠫ࠮ࠧࡰ࠱ࠪࡪࡔࠦࡊ࠽ࠩࡒࡀࠥࡔ࠰ࠨࡪ࡛ࠥࡔࡄࠤ਎"))
              test_id = os.environ.get(bstack1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫਏ")) if os.environ.get(bstack1111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬਐ")) else global_config.get_property(bstack1111l_opy_ (u"ࠣࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠥ਑"))
              payload = {
                  bstack1111l_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪࠨ਒"): bstack1111l_opy_ (u"ࠥࡷࡩࡱ࡟ࡦࡸࡨࡲࡹࡹࠢਓ"),
                  bstack1111l_opy_ (u"ࠦࡩࡧࡴࡢࠤਔ"): {
                      bstack1111l_opy_ (u"ࠧࡺࡥࡴࡶ࡫ࡹࡧࡥࡵࡶ࡫ࡧࠦਕ"): test_id,
                      bstack1111l_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡪ࡟ࡥࡣࡼࠦਖ"): current_time,
                      bstack1111l_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥ࡮ࡢ࡯ࡨࠦਗ"): bstack1111l_opy_ (u"ࠣࡕࡇࡏࡋ࡫ࡡࡵࡷࡵࡩࡕ࡫ࡲࡧࡱࡵࡱࡦࡴࡣࡦࠤਘ"),
                      bstack1111l_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠ࡬ࡶࡳࡳࠨਙ"): {
                          bstack1111l_opy_ (u"ࠥࡱࡪࡧࡳࡶࡴࡨࡷࠧਚ"): data,
                          bstack1111l_opy_ (u"ࠦࡸࡪ࡫ࡓࡷࡱࡍࡩࠨਛ"): global_config.get_property(bstack1111l_opy_ (u"ࠧࡹࡤ࡬ࡔࡸࡲࡎࡪࠢਜ"))
                      },
                      bstack1111l_opy_ (u"ࠨࡵࡴࡧࡵࡣࡩࡧࡴࡢࠤਝ"): global_config.get_property(bstack1111l_opy_ (u"ࠢࡶࡵࡨࡶࡓࡧ࡭ࡦࠤਞ")),
                      bstack1111l_opy_ (u"ࠣࡪࡲࡷࡹࡥࡩ࡯ࡨࡲࠦਟ"): get_host_info()
                  }
              }
              bstack1ll1ll1ll1_opy_ = bstack111l1lll1_opy_(cli.config, [bstack1111l_opy_ (u"ࠤࡤࡴ࡮ࡹࠢਠ"), bstack1111l_opy_ (u"ࠥࡩࡩࡹࡉ࡯ࡵࡷࡶࡺࡳࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠣਡ"), bstack1111l_opy_ (u"ࠦࡦࡶࡩࠣਢ")], bstack11ll1111ll_opy_)
              response = bstack1llll1ll1_opy_(bstack1111l_opy_ (u"ࠧࡖࡏࡔࡖࠥਣ"), bstack1ll1ll1ll1_opy_, payload, config)
              if response.status_code >= 200 and response.status_code < 300:
                  logger.info(bstack1111l_opy_ (u"ࠨࡋࡦࡻࠣࡱࡪࡺࡲࡪࡥࡶࠤࡸ࡫࡮ࡵࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡶࡲࠤࢀࢃࠢਤ").format(bstack11ll1111ll_opy_))
              else:
                  logger.debug(bstack1111l_opy_ (u"ࠢࡌࡧࡼࠤࡲ࡫ࡴࡳ࡫ࡦࡷࠥࡸࡥࡲࡷࡨࡷࡹࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫ࠤࡸࡺࡡࡵࡷࡶࠤࢀࢃࠢਥ").format(response.status_code))
          except Exception as e:
              logger.debug(bstack1111l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫࡮ࡥࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹ࠺ࠡࡽࢀࠦਦ").format(e))
      bstack111lllllll_opy_()
  except Exception as e:
      logger.debug(bstack1111l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫࡮ࡥࡡ࡮ࡩࡾࡥ࡭ࡦࡶࡵ࡭ࡨࡹ࠺ࠡࡽࢀࠦਧ").format(e))
def bstack11l11l1l1_opy_(bstack1111l1l1l1_opy_=False):
  bstack1llll1l111_opy_ = bstack1111l_opy_ (u"ࠥࠦਨ")
  global bstack1l1111l1ll_opy_
  global bstack1l1lll1ll_opy_
  global bstack11l11l1l1l_opy_
  global bstack11ll111l_opy_
  global ROBOT_PYTHON_ERRORS
  global bstack1l111ll1ll_opy_
  global CONFIG
  bstack11l11l11ll_opy_ = os.environ.get(bstack1111l_opy_ (u"ࠫࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ࡟ࡖࡕࡈࡈࠬ਩"))
  if bstack11l11l11ll_opy_ not in [bstack1111l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ਪ")]:
    bstack1llll1l111_opy_ = bstack1l11ll1l1_opy_.bstack11ll11l1ll_opy_(EVENTS.bstack11111l11_opy_)
  percy.shutdown()
  if bstack1l1111l1ll_opy_:
    logger.warning(bstack111l1lll_opy_.format(str(bstack1l1111l1ll_opy_)))
  else:
    try:
      bstack1l1lll1ll1_opy_ = bstack11ll111111_opy_(bstack1111l_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬਫ"), logger)
      if bstack1l1lll1ll1_opy_.get(bstack1111l_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬਬ")) and bstack1l1lll1ll1_opy_.get(bstack1111l_opy_ (u"ࠨࡰࡸࡨ࡬࡫࡟࡭ࡱࡦࡥࡱ࠭ਭ")).get(bstack1111l_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫਮ")):
        logger.warning(bstack111l1lll_opy_.format(str(bstack1l1lll1ll1_opy_[bstack1111l_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨਯ")][bstack1111l_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ਰ")])))
    except Exception as e:
      logger.error(e)
  if cli.is_running() and bstack11l11l11ll_opy_ not in [bstack1111l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭਱")]:
    if _11l1ll11l1_opy_ is not None:
      bstack1111l1l1l1_opy_ = _11l1ll11l1_opy_
    else:
      bstack1111l1l1l1_opy_ = cli.is_running()
    bstack1111ll11_opy_.invoke(Events.bstack1ll1l1lll_opy_)
  elif _11l1ll11l1_opy_ is not None:
    bstack1111l1l1l1_opy_ = _11l1ll11l1_opy_
  logger.info(bstack1l11lll1l_opy_)
  global bstack11l1l1lll1_opy_
  if bstack11l1l1lll1_opy_:
    bstack1lll111111_opy_()
  try:
    with bstack11ll11l1l_opy_:
      bstack11l11111_opy_ = bstack1l1lll1ll_opy_.copy()
    for driver in bstack11l11111_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack111111l1_opy_)
  ROBOT_PYTHON_ERRORS = []
  if bstack1l111ll1ll_opy_ == bstack1111l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬਲ"):
    ROBOT_PYTHON_ERRORS = bstack1lll11l1l_opy_(bstack1111l_opy_ (u"ࠧࡳࡱࡥࡳࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨਲ਼"))
  if bstack1l111ll1ll_opy_ == bstack1111l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ਴") and len(bstack11ll111l_opy_) == 0:
    bstack11ll111l_opy_ = bstack1lll11l1l_opy_(bstack1111l_opy_ (u"ࠩࡳࡻࡤࡶࡹࡵࡧࡶࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧਵ"))
    if len(bstack11ll111l_opy_) == 0:
      bstack11ll111l_opy_ = bstack1lll11l1l_opy_(bstack1111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡴࡵࡶ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩਸ਼"))
  bstack1ll111ll1l_opy_ = bstack1111l_opy_ (u"ࠫࠬ਷")
  if len(bstack11l11l1l1l_opy_) > 0:
    bstack1ll111ll1l_opy_ = bstack11l1l1l11_opy_(bstack11l11l1l1l_opy_)
  elif len(bstack11ll111l_opy_) > 0:
    bstack1ll111ll1l_opy_ = bstack11l1l1l11_opy_(bstack11ll111l_opy_)
  elif len(ROBOT_PYTHON_ERRORS) > 0:
    bstack1ll111ll1l_opy_ = bstack11l1l1l11_opy_(ROBOT_PYTHON_ERRORS)
  elif len(bstack11ll111l1l_opy_) > 0:
    bstack1ll111ll1l_opy_ = bstack11l1l1l11_opy_(bstack11ll111l1l_opy_)
  if bstack11l11l11ll_opy_ not in [bstack1111l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ਸ")]:
    def bstack1lllllll11_opy_():
      try:
        if bstack11l11l11ll_opy_ in [bstack1111l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬਹ"), bstack1111l_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭਺")]:
          bstack1ll1l1l1l_opy_()
      except Exception as e:
        logger.debug(bstack1111l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪ࡮ࡴࡡ࡭ࡡࡨࡼࡪࡩࡵࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤ਻").format(e))
    def bstack1llllllll_opy_():
      try:
        if bool(bstack1ll111ll1l_opy_):
          bstack11l11l1ll1_opy_(bstack1ll111ll1l_opy_, bstack1111l1l1l1_opy_=bstack1111l1l1l1_opy_)
        else:
          bstack11l11l1ll1_opy_(bstack1111l1l1l1_opy_=bstack1111l1l1l1_opy_)
      except Exception as e:
        logger.debug(bstack1111l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡵࡨࡲࡩ࡯࡮ࡨࠢࡨࡺࡪࡴࡴ࠻ࠢࡾࢁ਼ࠧ").format(e))
    def bstack11lll11lll_opy_():
      try:
        logger_utils.bstack1l1l1111l_opy_(CONFIG)
      except Exception as e:
        logger.debug(bstack1111l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡶࡩࡳࡪࡩ࡯ࡩࠣࡰࡴ࡭ࡳ࠻ࠢࡾࢁࠧ਽").format(e))
    bstack11lll11111_opy_ = threading.Thread(target=bstack1lllllll11_opy_)
    bstack1l1ll1l1l_opy_ = threading.Thread(target=bstack1llllllll_opy_)
    bstack1ll11111l1_opy_ = threading.Thread(target=bstack11lll11lll_opy_)
    threads = [bstack11lll11111_opy_, bstack1l1ll1l1l_opy_, bstack1ll11111l1_opy_]
    for thread in threads:
      try:
        thread.start()
      except Exception as e:
        logger.debug(bstack1111l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡷࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡺࡨࡳࡧࡤࡨࠥࢁࡽ࠻ࠢࡾࢁࠧਾ").format(thread.name, e))
    for thread in threads:
      try:
        thread.join()
      except Exception as e:
        logger.debug(bstack1111l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡯ࡵࡩ࡯࡫ࡱ࡫ࠥࡺࡨࡳࡧࡤࡨࠥࢁࡽ࠻ࠢࡾࢁࠧਿ").format(thread.name, e))
    bstack11ll1l11l1_opy_(bstack11l1llll1_opy_, logger)
    bstack11ll1l11l1_opy_(os.path.join(os.getcwd(), bstack1111l_opy_ (u"࠭࡬ࡰࡩࠪੀ"), bstack1111l_opy_ (u"ࠧ࡬ࡧࡼ࠱ࡲ࡫ࡴࡳ࡫ࡦࡷ࠳ࡰࡳࡰࡰࠪੁ")), logger)
  if bstack11l11l11ll_opy_ not in [bstack1111l_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩੂ")]:
    bstack1l11ll1l1_opy_.end(EVENTS.bstack11111l11_opy_.value, bstack1llll1l111_opy_ + bstack1111l_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ੃"), bstack1llll1l111_opy_ + bstack1111l_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ੄"), status=True, failure=None, test_name=None)
    bstack11llllll_opy_()
    logger_utils.bstack11l1l1l1_opy_()
    logging.shutdown()
  if len(ROBOT_PYTHON_ERRORS) > 0:
    sys.exit(len(ROBOT_PYTHON_ERRORS))
def bstack1l1llll11_opy_(bstack1lllll1ll1_opy_, frame):
  global global_config
  logger.error(bstack1ll1lll11_opy_)
  global_config.bstack1ll1111l11_opy_(bstack1111l_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡓࡵࠧ੅"), bstack1lllll1ll1_opy_)
  if hasattr(signal, bstack1111l_opy_ (u"࡙ࠬࡩࡨࡰࡤࡰࡸ࠭੆")):
    global_config.bstack1ll1111l11_opy_(bstack1111l_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭ੇ"), signal.Signals(bstack1lllll1ll1_opy_).name)
  else:
    global_config.bstack1ll1111l11_opy_(bstack1111l_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡔ࡫ࡪࡲࡦࡲࠧੈ"), bstack1111l_opy_ (u"ࠨࡕࡌࡋ࡚ࡔࡋࡏࡑ࡚ࡒࠬ੉"))
  bstack1111l1l1l1_opy_ = cli.is_running()
  if bstack1111l1l1l1_opy_:
    bstack1111ll11_opy_.invoke(Events.bstack1ll1l1lll_opy_)
  bstack11l11l11ll_opy_ = os.environ.get(bstack1111l_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪ੊"))
  if bstack11l11l11ll_opy_ == bstack1111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪੋ") and not cli.is_enabled(CONFIG):
    TestHubHandler.stop(global_config.get_property(bstack1111l_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡘ࡯ࡧ࡯ࡣ࡯ࠫੌ")))
  bstack11l11l1l1_opy_(bstack1111l1l1l1_opy_)
  sys.exit(1)
def bstack111llll1ll_opy_(err):
  logger.critical(bstack1l111l1ll1_opy_.format(str(err)))
  bstack11l11l1ll1_opy_(bstack1l111l1ll1_opy_.format(str(err)), True)
  atexit.unregister(bstack11l11l1l1_opy_)
  bstack1ll1l1l1l_opy_()
  sys.exit(1)
def bstack11ll1ll11l_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack11l11l1ll1_opy_(message, True)
  atexit.unregister(bstack11l11l1l1_opy_)
  bstack1ll1l1l1l_opy_()
  sys.exit(1)
def bstack1l111ll1l1_opy_():
  global CONFIG
  global bstack11l1llll_opy_
  global bstack1llll1111l_opy_
  global BROWSERSTACK_AUTOMATION
  CONFIG = bstack1l1lll1l_opy_()
  load_dotenv(CONFIG.get(bstack1111l_opy_ (u"ࠬ࡫࡮ࡷࡈ࡬ࡰࡪ੍࠭")))
  bstack111ll11lll_opy_()
  bstack11l111ll_opy_()
  CONFIG = bstack1ll1lll1l1_opy_(CONFIG)
  update(CONFIG, bstack1llll1111l_opy_)
  update(CONFIG, bstack11l1llll_opy_)
  if not cli.is_enabled(CONFIG):
    CONFIG = bstack1ll1l1l1l1_opy_(CONFIG)
  BROWSERSTACK_AUTOMATION = bstack11l1ll11ll_opy_(CONFIG)
  os.environ[bstack1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ੎")] = BROWSERSTACK_AUTOMATION.__str__().lower()
  global_config.bstack1ll1111l11_opy_(bstack1111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ੏"), BROWSERSTACK_AUTOMATION)
  if (bstack1111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ੐") in CONFIG and bstack1111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬੑ") in bstack11l1llll_opy_) or (
          bstack1111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭੒") in CONFIG and bstack1111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ੓") not in bstack1llll1111l_opy_):
    if os.getenv(bstack1111l_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩ੔")):
      CONFIG[bstack1111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ੕")] = os.getenv(bstack1111l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫ੖"))
    else:
      if not CONFIG.get(bstack1111l_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠦ੗"), bstack1111l_opy_ (u"ࠤࠥ੘")) in bstack11ll1111l_opy_:
        bstack1111l1111l_opy_()
  elif (bstack1111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ਖ਼") not in CONFIG and bstack1111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ਗ਼") in CONFIG) or (
          bstack1111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨਜ਼") in bstack1llll1111l_opy_ and bstack1111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩੜ") not in bstack11l1llll_opy_):
    del (CONFIG[bstack1111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ੝")])
  if bstack11l11ll1ll_opy_(CONFIG):
    bstack111llll1ll_opy_(bstack11llllll11_opy_)
  Config.get_instance().bstack1ll1111l11_opy_(bstack1111l_opy_ (u"ࠣࡷࡶࡩࡷࡔࡡ࡮ࡧࠥਫ਼"), CONFIG[bstack1111l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ੟")])
  bstack11111lllll_opy_()
  bstack1l11ll11ll_opy_()
  if bstack1l1111111l_opy_ and not CONFIG.get(bstack1111l_opy_ (u"ࠥࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠨ੠"), bstack1111l_opy_ (u"ࠦࠧ੡")) in bstack11ll1111l_opy_:
    CONFIG[bstack1111l_opy_ (u"ࠬࡧࡰࡱࠩ੢")] = bstack1llll1ll1l_opy_(CONFIG)
    logger.info(bstack11l1llllll_opy_.format(CONFIG[bstack1111l_opy_ (u"࠭ࡡࡱࡲࠪ੣")]))
  if not BROWSERSTACK_AUTOMATION:
    CONFIG[bstack1111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ੤")] = [{}]
def bstack1l111l111l_opy_(config, bstack1lll1ll1l_opy_):
  global CONFIG
  global bstack1l1111111l_opy_
  CONFIG = config
  bstack1l1111111l_opy_ = bstack1lll1ll1l_opy_
def bstack1l11ll11ll_opy_():
  global CONFIG
  global bstack1l1111111l_opy_
  if bstack1111l_opy_ (u"ࠨࡣࡳࡴࠬ੥") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack11ll1ll11l_opy_(e, bstack1l1l11l1l1_opy_)
    bstack1l1111111l_opy_ = True
    global_config.bstack1ll1111l11_opy_(bstack1111l_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨ੦"), True)
def bstack1llll1ll1l_opy_(config):
  bstack1ll1ll1111_opy_ = bstack1111l_opy_ (u"ࠪࠫ੧")
  app = config[bstack1111l_opy_ (u"ࠫࡦࡶࡰࠨ੨")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1l1111l1_opy_:
      if os.path.exists(app):
        bstack1ll1ll1111_opy_ = bstack1llll1llll_opy_(config, app)
      elif bstack1l1llll11l_opy_(app):
        bstack1ll1ll1111_opy_ = app
      else:
        bstack111llll1ll_opy_(bstack1l1ll11l_opy_.format(app))
    else:
      if bstack1l1llll11l_opy_(app):
        bstack1ll1ll1111_opy_ = app
      elif os.path.exists(app):
        bstack1ll1ll1111_opy_ = bstack1llll1llll_opy_(app)
      else:
        bstack111llll1ll_opy_(bstack1llll11l1_opy_)
  else:
    if len(app) > 2:
      bstack111llll1ll_opy_(bstack11lll1l1_opy_)
    elif len(app) == 2:
      if bstack1111l_opy_ (u"ࠬࡶࡡࡵࡪࠪ੩") in app and bstack1111l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩ੪") in app:
        if os.path.exists(app[bstack1111l_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ੫")]):
          bstack1ll1ll1111_opy_ = bstack1llll1llll_opy_(config, app[bstack1111l_opy_ (u"ࠨࡲࡤࡸ࡭࠭੬")], app[bstack1111l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ੭")])
        else:
          bstack111llll1ll_opy_(bstack1l1ll11l_opy_.format(app))
      else:
        bstack111llll1ll_opy_(bstack11lll1l1_opy_)
    else:
      for key in app:
        if key in bstack1lll1111l_opy_:
          if key == bstack1111l_opy_ (u"ࠪࡴࡦࡺࡨࠨ੮"):
            if os.path.exists(app[key]):
              bstack1ll1ll1111_opy_ = bstack1llll1llll_opy_(config, app[key])
            else:
              bstack111llll1ll_opy_(bstack1l1ll11l_opy_.format(app))
          else:
            bstack1ll1ll1111_opy_ = app[key]
        else:
          bstack111llll1ll_opy_(bstack1ll11l1ll1_opy_)
  return bstack1ll1ll1111_opy_
def bstack1l1llll11l_opy_(bstack1ll1ll1111_opy_):
  import re
  bstack1lllll11ll_opy_ = re.compile(bstack1111l_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬࠧࠦ੯"))
  bstack111l111ll_opy_ = re.compile(bstack1111l_opy_ (u"ࡷࠨ࡞࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭࠳ࡠࡧ࠭ࡻࡃ࠰࡞࠵࠳࠹࡝ࡡ࠱ࡠ࠲ࡣࠪࠥࠤੰ"))
  if bstack1111l_opy_ (u"࠭ࡢࡴ࠼࠲࠳ࠬੱ") in bstack1ll1ll1111_opy_ or re.fullmatch(bstack1lllll11ll_opy_, bstack1ll1ll1111_opy_) or re.fullmatch(bstack111l111ll_opy_, bstack1ll1ll1111_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack1lll111l1l_opy_, stage=STAGE.bstack11lll111l_opy_, bstack11lll111_opy_=SESSION_NAME)
def bstack1llll1llll_opy_(config, path, bstack1l111lll11_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1111l_opy_ (u"ࠧࡳࡤࠪੲ")).read()).hexdigest()
  bstack1l1111ll_opy_ = bstack1l1ll1111l_opy_(md5_hash)
  bstack1ll1ll1111_opy_ = None
  if bstack1l1111ll_opy_:
    logger.info(bstack111l11lll_opy_.format(bstack1l1111ll_opy_, md5_hash))
    return bstack1l1111ll_opy_
  bstack1lll1l11l_opy_ = datetime.datetime.now()
  multipart_data = MultipartEncoder(
    fields={
      bstack1111l_opy_ (u"ࠨࡨ࡬ࡰࡪ࠭ੳ"): (os.path.basename(path), open(os.path.abspath(path), bstack1111l_opy_ (u"ࠩࡵࡦࠬੴ")), bstack1111l_opy_ (u"ࠪࡸࡪࡾࡴ࠰ࡲ࡯ࡥ࡮ࡴࠧੵ")),
      bstack1111l_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧ੶"): bstack1l111lll11_opy_
    }
  )
  response = requests.post(bstack11lllll1_opy_, data=multipart_data,
                           headers={bstack1111l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ੷"): multipart_data.content_type},
                           auth=(config[bstack1111l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ੸")], config[bstack1111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ੹")]))
  try:
    res = json.loads(response.text)
    bstack1ll1ll1111_opy_ = res[bstack1111l_opy_ (u"ࠨࡣࡳࡴࡤࡻࡲ࡭ࠩ੺")]
    logger.info(bstack111l111ll1_opy_.format(bstack1ll1ll1111_opy_))
    bstack11l11l111l_opy_(md5_hash, bstack1ll1ll1111_opy_)
    cli.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺ࡶࡲ࡯ࡳࡦࡪ࡟ࡢࡲࡳࠦ੻"), datetime.datetime.now() - bstack1lll1l11l_opy_)
  except ValueError as err:
    bstack111llll1ll_opy_(bstack111l111lll_opy_.format(str(err)))
  return bstack1ll1ll1111_opy_
def bstack11111lllll_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack111l1l11_opy_
  bstack1111l11l11_opy_ = 1
  bstack1ll111l11l_opy_ = 1
  if bstack1111l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ੼") in CONFIG:
    bstack1ll111l11l_opy_ = CONFIG[bstack1111l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ੽")]
  else:
    bstack1ll111l11l_opy_ = bstack1l1l11ll1_opy_(framework_name, args) or 1
  if bstack1111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ੾") in CONFIG:
    bstack1111l11l11_opy_ = len(CONFIG[bstack1111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ੿")])
  bstack111l1l11_opy_ = int(bstack1ll111l11l_opy_) * int(bstack1111l11l11_opy_)
def bstack1l1l11ll1_opy_(framework_name, args):
  if framework_name == bstack1ll1l111_opy_ and args and bstack1111l_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ઀") in args:
      bstack1llllllll1_opy_ = args.index(bstack1111l_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ઁ"))
      return int(args[bstack1llllllll1_opy_ + 1]) or 1
  return 1
def bstack1l1ll1111l_opy_(md5_hash):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1111l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡬ࡰࡥ࡮ࠤࡳࡵࡴࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨ࠰ࠥࡻࡳࡪࡰࡪࠤࡧࡧࡳࡪࡥࠣࡪ࡮ࡲࡥࠡࡱࡳࡩࡷࡧࡴࡪࡱࡱࡷࠬં"))
    bstack1l1lll1lll_opy_ = os.path.join(os.path.expanduser(bstack1111l_opy_ (u"ࠪࢂࠬઃ")), bstack1111l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ઄"), bstack1111l_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭અ"))
    if os.path.exists(bstack1l1lll1lll_opy_):
      try:
        bstack111llllll_opy_ = json.load(open(bstack1l1lll1lll_opy_, bstack1111l_opy_ (u"࠭ࡲࡣࠩઆ")))
        if md5_hash in bstack111llllll_opy_:
          bstack1ll1l111ll_opy_ = bstack111llllll_opy_[md5_hash]
          bstack11lll1l1ll_opy_ = datetime.datetime.now()
          bstack111llll1l1_opy_ = datetime.datetime.strptime(bstack1ll1l111ll_opy_[bstack1111l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪઇ")], bstack1111l_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬઈ"))
          if (bstack11lll1l1ll_opy_ - bstack111llll1l1_opy_).days > 30:
            return None
          elif version.parse(str(__version__)) > version.parse(bstack1ll1l111ll_opy_[bstack1111l_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧઉ")]):
            return None
          return bstack1ll1l111ll_opy_[bstack1111l_opy_ (u"ࠪ࡭ࡩ࠭ઊ")]
      except Exception as e:
        logger.debug(bstack1111l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡶࡪࡧࡤࡪࡰࡪࠤࡒࡊ࠵ࠡࡪࡤࡷ࡭ࠦࡦࡪ࡮ࡨ࠾ࠥࢁࡽࠨઋ").format(str(e)))
    return None
  bstack1l1lll1lll_opy_ = os.path.join(os.path.expanduser(bstack1111l_opy_ (u"ࠬࢄࠧઌ")), bstack1111l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ઍ"), bstack1111l_opy_ (u"ࠧࡢࡲࡳ࡙ࡵࡲ࡯ࡢࡦࡐࡈ࠺ࡎࡡࡴࡪ࠱࡮ࡸࡵ࡮ࠨ઎"))
  lock_file = bstack1l1lll1lll_opy_ + bstack1111l_opy_ (u"ࠨ࠰࡯ࡳࡨࡱࠧએ")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack1l1lll1lll_opy_):
        with open(bstack1l1lll1lll_opy_, bstack1111l_opy_ (u"ࠩࡵࠫઐ")) as f:
          content = f.read().strip()
          if content:
            bstack111llllll_opy_ = json.loads(content)
            if md5_hash in bstack111llllll_opy_:
              bstack1ll1l111ll_opy_ = bstack111llllll_opy_[md5_hash]
              bstack11lll1l1ll_opy_ = datetime.datetime.now()
              bstack111llll1l1_opy_ = datetime.datetime.strptime(bstack1ll1l111ll_opy_[bstack1111l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ઑ")], bstack1111l_opy_ (u"ࠫࠪࡪ࠯ࠦ࡯࠲ࠩ࡞ࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨ઒"))
              if (bstack11lll1l1ll_opy_ - bstack111llll1l1_opy_).days > 30:
                return None
              elif version.parse(str(__version__)) > version.parse(bstack1ll1l111ll_opy_[bstack1111l_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪઓ")]):
                return None
              return bstack1ll1l111ll_opy_[bstack1111l_opy_ (u"࠭ࡩࡥࠩઔ")]
      return None
  except Exception as e:
    logger.debug(bstack1111l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡷࡪࡶ࡫ࠤ࡫࡯࡬ࡦࠢ࡯ࡳࡨࡱࡩ࡯ࡩࠣࡪࡴࡸࠠࡎࡆ࠸ࠤ࡭ࡧࡳࡩ࠼ࠣࡿࢂ࠭ક").format(str(e)))
    return None
def bstack11l11l111l_opy_(md5_hash, bstack1ll1ll1111_opy_):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1111l_opy_ (u"ࠨࡨ࡬ࡰࡪࡲ࡯ࡤ࡭ࠣࡲࡴࡺࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧ࠯ࠤࡺࡹࡩ࡯ࡩࠣࡦࡦࡹࡩࡤࠢࡩ࡭ࡱ࡫ࠠࡰࡲࡨࡶࡦࡺࡩࡰࡰࡶࠫખ"))
    bstack111lll11ll_opy_ = os.path.join(os.path.expanduser(bstack1111l_opy_ (u"ࠩࢁࠫગ")), bstack1111l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪઘ"))
    if not os.path.exists(bstack111lll11ll_opy_):
      os.makedirs(bstack111lll11ll_opy_)
    bstack1l1lll1lll_opy_ = os.path.join(os.path.expanduser(bstack1111l_opy_ (u"ࠫࢃ࠭ઙ")), bstack1111l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬચ"), bstack1111l_opy_ (u"࠭ࡡࡱࡲࡘࡴࡱࡵࡡࡥࡏࡇ࠹ࡍࡧࡳࡩ࠰࡭ࡷࡴࡴࠧછ"))
    bstack1lll11ll11_opy_ = {
      bstack1111l_opy_ (u"ࠧࡪࡦࠪજ"): bstack1ll1ll1111_opy_,
      bstack1111l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫઝ"): datetime.datetime.strftime(datetime.datetime.now(), bstack1111l_opy_ (u"ࠩࠨࡨ࠴ࠫ࡭࠰ࠧ࡜ࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭ઞ")),
      bstack1111l_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨટ"): str(__version__)
    }
    try:
      bstack111llllll_opy_ = {}
      if os.path.exists(bstack1l1lll1lll_opy_):
        bstack111llllll_opy_ = json.load(open(bstack1l1lll1lll_opy_, bstack1111l_opy_ (u"ࠫࡷࡨࠧઠ")))
      bstack111llllll_opy_[md5_hash] = bstack1lll11ll11_opy_
      with open(bstack1l1lll1lll_opy_, bstack1111l_opy_ (u"ࠧࡽࠫࠣડ")) as outfile:
        json.dump(bstack111llllll_opy_, outfile)
    except Exception as e:
      logger.debug(bstack1111l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡻࡰࡥࡣࡷ࡭ࡳ࡭ࠠࡎࡆ࠸ࠤ࡭ࡧࡳࡩࠢࡩ࡭ࡱ࡫࠺ࠡࡽࢀࠫઢ").format(str(e)))
    return
  bstack111lll11ll_opy_ = os.path.join(os.path.expanduser(bstack1111l_opy_ (u"ࠧࡿࠩણ")), bstack1111l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨત"))
  if not os.path.exists(bstack111lll11ll_opy_):
    os.makedirs(bstack111lll11ll_opy_)
  bstack1l1lll1lll_opy_ = os.path.join(os.path.expanduser(bstack1111l_opy_ (u"ࠩࢁࠫથ")), bstack1111l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪદ"), bstack1111l_opy_ (u"ࠫࡦࡶࡰࡖࡲ࡯ࡳࡦࡪࡍࡅ࠷ࡋࡥࡸ࡮࠮࡫ࡵࡲࡲࠬધ"))
  lock_file = bstack1l1lll1lll_opy_ + bstack1111l_opy_ (u"ࠬ࠴࡬ࡰࡥ࡮ࠫન")
  bstack1lll11ll11_opy_ = {
    bstack1111l_opy_ (u"࠭ࡩࡥࠩ઩"): bstack1ll1ll1111_opy_,
    bstack1111l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪપ"): datetime.datetime.strftime(datetime.datetime.now(), bstack1111l_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬફ")),
    bstack1111l_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧબ"): str(__version__)
  }
  try:
    with FileLock(lock_file, timeout=10):
      bstack111llllll_opy_ = {}
      if os.path.exists(bstack1l1lll1lll_opy_):
        with open(bstack1l1lll1lll_opy_, bstack1111l_opy_ (u"ࠪࡶࠬભ")) as f:
          content = f.read().strip()
          if content:
            bstack111llllll_opy_ = json.loads(content)
      bstack111llllll_opy_[md5_hash] = bstack1lll11ll11_opy_
      with open(bstack1l1lll1lll_opy_, bstack1111l_opy_ (u"ࠦࡼࠨમ")) as outfile:
        json.dump(bstack111llllll_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1111l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡼ࡯ࡴࡩࠢࡩ࡭ࡱ࡫ࠠ࡭ࡱࡦ࡯࡮ࡴࡧࠡࡨࡲࡶࠥࡓࡄ࠶ࠢ࡫ࡥࡸ࡮ࠠࡶࡲࡧࡥࡹ࡫࠺ࠡࡽࢀࠫય").format(str(e)))
def bstack1l11l111_opy_(self):
  return
def bstack11lll1l11l_opy_(self):
  return
def bstack11ll111l11_opy_():
  global bstack1l11l1ll1_opy_
  bstack1l11l1ll1_opy_ = True
def bstack11l1l1ll_opy_(self):
  global FRAMEWORK_NAME
  global bstack1lll11111_opy_
  global bstack11l1ll11l_opy_
  bstack1l1llll1_opy_ = bstack1l11ll1l1_opy_.bstack11ll11l1ll_opy_(EVENTS.bstack11111ll1l_opy_)
  try:
    if bstack1111l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ર") in FRAMEWORK_NAME and self.session_id != None and bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫ઱"), bstack1111l_opy_ (u"ࠨࠩલ")) != bstack1111l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪળ"):
      bstack11l1l1llll_opy_ = bstack1111l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ઴") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫવ")
      if bstack11l1l1llll_opy_ == bstack1111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬશ"):
        bstack1111l1ll1_opy_(logger)
      if self != None:
        bstack1ll1111l1l_opy_(self, bstack11l1l1llll_opy_, bstack1111l_opy_ (u"࠭ࠬࠡࠩષ").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack1111l_opy_ (u"ࠧࠨસ")
    if bstack1111l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨહ") in FRAMEWORK_NAME and getattr(threading.current_thread(), bstack1111l_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ઺"), None):
      bstack11l11llll1_opy_.bstack11l11l111_opy_(self, bstack111l1l111_opy_, logger, wait=True)
    if bstack1111l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ઻") in FRAMEWORK_NAME:
      bstack1111l1ll11_opy_.bstack1111l1lll1_opy_(self)
    bstack1l11ll1l1_opy_.end(EVENTS.bstack11111ll1l_opy_.value, bstack1l1llll1_opy_ + bstack1111l_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷ઼ࠦ"), bstack1l1llll1_opy_ + bstack1111l_opy_ (u"ࠧࡀࡥ࡯ࡦࠥઽ"), status=True, failure=None, test_name=None)
  except Exception as e:
    logger.debug(bstack1111l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࠢા") + str(e))
    bstack1l11ll1l1_opy_.end(EVENTS.bstack11111ll1l_opy_.value, bstack1l1llll1_opy_ + bstack1111l_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢિ"), bstack1l1llll1_opy_ + bstack1111l_opy_ (u"ࠣ࠼ࡨࡲࡩࠨી"), status=False, failure=str(e), test_name=None)
  bstack11l1ll11l_opy_(self)
  self.session_id = None
def bstack1111lll1l_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack1l111l11_opy_
    global FRAMEWORK_NAME
    command_executor = kwargs.get(bstack1111l_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠬુ"), bstack1111l_opy_ (u"ࠪࠫૂ"))
    bstack1l11111l_opy_ = False
    if type(command_executor) == str and bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧૃ") in command_executor:
      bstack1l11111l_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨૄ") in str(getattr(command_executor, bstack1111l_opy_ (u"࠭࡟ࡶࡴ࡯ࠫૅ"), bstack1111l_opy_ (u"ࠧࠨ૆"))):
      bstack1l11111l_opy_ = True
    else:
      kwargs = a11y.bstack111l1l11ll_opy_(bstack111ll11l1_opy_=kwargs, config=CONFIG)
      return bstack1ll1l1ll_opy_(self, *args, **kwargs)
    if bstack1l11111l_opy_:
      bstack11llll11_opy_ = TestHubUtils.bstack11l11l1111_opy_(CONFIG, FRAMEWORK_NAME)
      if kwargs.get(bstack1111l_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩે")):
        kwargs[bstack1111l_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪૈ")] = bstack1l111l11_opy_(kwargs[bstack1111l_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫૉ")], FRAMEWORK_NAME, CONFIG, bstack11llll11_opy_)
      elif kwargs.get(bstack1111l_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ૊")):
        kwargs[bstack1111l_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬો")] = bstack1l111l11_opy_(kwargs[bstack1111l_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ૌ")], FRAMEWORK_NAME, CONFIG, bstack11llll11_opy_)
  except Exception as e:
    logger.error(bstack1111l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩࡧࡱࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡕࡇࡏࠥࡩࡡࡱࡵ࠽ࠤࢀࢃ્ࠢ").format(str(e)))
  return bstack1ll1l1ll_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack1l1l11111_opy_, stage=STAGE.bstack11lll111l_opy_, bstack11lll111_opy_=SESSION_NAME)
def bstack1lll111lll_opy_(self, command_executor=bstack1111l_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰࠳࠵࠻࠳࠶࠮࠱࠰࠴࠾࠹࠺࠴࠵ࠤ૎"), *args, **kwargs):
  global bstack1lll11111_opy_
  global bstack1l1lll1ll_opy_
  bstack111ll11ll_opy_ = bstack1111lll1l_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack11l11ll1l1_opy_.on():
    return bstack111ll11ll_opy_
  try:
    logger.debug(bstack1111l_opy_ (u"ࠩࡆࡳࡲࡳࡡ࡯ࡦࠣࡉࡽ࡫ࡣࡶࡶࡲࡶࠥࡽࡨࡦࡰࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡩࡴࠢࡩࡥࡱࡹࡥࠡ࠯ࠣࡿࢂ࠭૏").format(str(command_executor)))
    logger.debug(bstack1111l_opy_ (u"ࠪࡌࡺࡨࠠࡖࡔࡏࠤ࡮ࡹࠠ࠮ࠢࡾࢁࠬૐ").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧ૑") in command_executor._url:
      global_config.bstack1ll1111l11_opy_(bstack1111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭૒"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩ૓") in command_executor):
    global_config.bstack1ll1111l11_opy_(bstack1111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ૔"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1111l111l_opy_ = getattr(threading.current_thread(), bstack1111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡕࡧࡶࡸࡒ࡫ࡴࡢࠩ૕"), None)
  bstack1l1lll11ll_opy_ = {}
  if self.capabilities is not None:
    bstack1l1lll11ll_opy_[bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡲࡦࡳࡥࠨ૖")] = self.capabilities.get(bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ૗"))
    bstack1l1lll11ll_opy_[bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭૘")] = self.capabilities.get(bstack1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭૙"))
    bstack1l1lll11ll_opy_[bstack1111l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡥ࡯ࡱࡶ࡬ࡳࡳࡹࠧ૚")] = self.capabilities.get(bstack1111l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ૛"))
  if CONFIG.get(bstack1111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ૜"), False) and a11y.bstack111ll111_opy_(bstack1l1lll11ll_opy_):
    threading.current_thread().a11yPlatform = True
  if bstack1111l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ૝") in FRAMEWORK_NAME or bstack1111l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ૞") in FRAMEWORK_NAME:
    TestHubHandler.send_cbt_info(self)
  if bstack1111l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ૟") in FRAMEWORK_NAME and bstack1111l111l_opy_ and bstack1111l111l_opy_.get(bstack1111l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬૠ"), bstack1111l_opy_ (u"࠭ࠧૡ")) == bstack1111l_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨૢ"):
    TestHubHandler.send_cbt_info(self)
  bstack1lll11111_opy_ = self.session_id
  with bstack11ll11l1l_opy_:
    bstack1l1lll1ll_opy_.append(self)
  return bstack111ll11ll_opy_
def bstack1l1l11l11l_opy_(args):
  return bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠩૣ") in str(args)
def bstack111l11ll1_opy_(self, driver_command, *args, **kwargs):
  global bstack1ll11l11ll_opy_
  global bstack1l1ll1ll_opy_
  bstack1llllll11l_opy_ = bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭૤"), None) and bstack1l11l11l11_opy_(
          threading.current_thread(), bstack1111l_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ૥"), None)
  bstack11l1llll1l_opy_ = bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ૦"), None) and bstack1l11l11l11_opy_(
          threading.current_thread(), bstack1111l_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ૧"), None)
  bstack1l1ll111ll_opy_ = getattr(self, bstack1111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭૨"), None) != None and getattr(self, bstack1111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧ૩"), None) == True
  if not bstack1l1ll1ll_opy_ and bstack1111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ૪") in CONFIG and CONFIG[bstack1111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ૫")] == True and accessibility_scripts.bstack11ll1l1l11_opy_(driver_command) and (bstack1l1ll111ll_opy_ or bstack1llllll11l_opy_ or bstack11l1llll1l_opy_) and not bstack1l1l11l11l_opy_(args):
    try:
      bstack1l1ll1ll_opy_ = True
      logger.debug(bstack1111l_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡾࢁࠬ૬").format(driver_command))
      bstack1lll1ll1ll_opy_ = perform_scan(self, driver_command=driver_command)
      logger.debug(bstack1lll1ll1ll_opy_)
      try:
        log_data = {
          bstack1111l_opy_ (u"ࠦࡷ࡫ࡱࡶࡧࡶࡸࠧ૭"): {
            bstack1111l_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࠨ૮"): bstack1111l_opy_ (u"ࠨࡁ࠲࠳࡜ࡣࡘࡉࡁࡏࠤ૯"),
            bstack1111l_opy_ (u"ࠢࡱࡣࡵࡥࡲ࡫ࡴࡦࡴࡶࠦ૰"): [
              {
                bstack1111l_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠣ૱"): driver_command
              }
            ]
          },
          bstack1111l_opy_ (u"ࠤࡵࡩࡸࡶ࡯࡯ࡵࡨࠦ૲"): {
            bstack1111l_opy_ (u"ࠥࡦࡴࡪࡹࠣ૳"): {
              bstack1111l_opy_ (u"ࠦࡲࡹࡧࠣ૴"): bstack1lll1ll1ll_opy_.get(bstack1111l_opy_ (u"ࠧࡳࡳࡨࠤ૵"), bstack1111l_opy_ (u"ࠨࠢ૶")) if isinstance(bstack1lll1ll1ll_opy_, dict) else bstack1111l_opy_ (u"ࠢࠣ૷"),
              bstack1111l_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴࠤ૸"): bstack1lll1ll1ll_opy_.get(bstack1111l_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥૹ"), True) if isinstance(bstack1lll1ll1ll_opy_, dict) else True
            }
          }
        }
        logger.debug(bstack1111l_opy_ (u"ࠪࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮ࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡲ࡯ࡨࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠫૺ").format(log_data))
        automation_logger.info(json.dumps(log_data, separators=(bstack1111l_opy_ (u"ࠫ࠱࠭ૻ"), bstack1111l_opy_ (u"ࠬࡀࠧૼ"))))
      except Exception as bstack1l11111l1_opy_:
        logger.debug(bstack1111l_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢ࡯ࡳ࡬ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡤࡣࡱࠤࡩࡧࡴࡢ࠼ࠣࡿࢂ࠭૽").format(str(bstack1l11111l1_opy_)))
    except Exception as err:
      logger.debug(bstack1111l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡪࡸࡦࡰࡴࡰࠤࡸࡩࡡ࡯ࠢࡾࢁࠬ૾").format(str(err)))
    bstack1l1ll1ll_opy_ = False
  response = bstack1ll11l11ll_opy_(self, driver_command, *args, **kwargs)
  if (bstack1111l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ૿") in str(FRAMEWORK_NAME).lower() or bstack1111l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ଀") in str(FRAMEWORK_NAME).lower()) and bstack11l11ll1l1_opy_.on():
    try:
      if driver_command == bstack1111l_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧଁ"):
        TestHubHandler.bstack11l1lll1l1_opy_({
            bstack1111l_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪଂ"): response[bstack1111l_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫଃ")],
            bstack1111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭଄"): TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack11l11ll1l1_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
def bstack1l11l111ll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack1lll11111_opy_
  global PLATFORM_INDEX
  global SESSION_NAME
  global PARALLELISE_VANILLA_PYTHON
  global PARALLELISE_THREADING_PYTHON
  global FRAMEWORK_NAME
  global bstack1ll1l1ll_opy_
  global bstack1l1lll1ll_opy_
  global bstack11lll1ll11_opy_
  global bstack111l1l111_opy_
  bstack1l1llll1_opy_ = bstack1l11ll1l1_opy_.bstack11ll11l1ll_opy_(EVENTS.bstack1l1lll111_opy_.value)
  if os.getenv(bstack1111l_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬଅ")) is not None and a11y.bstack1l1l1l1ll1_opy_(CONFIG) is None:
    CONFIG[bstack1111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨଆ")] = True
  CONFIG[bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫଇ")] = str(FRAMEWORK_NAME) + str(__version__)
  bstack1111l111ll_opy_ = os.environ[bstack1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨଈ")]
  bstack11llll11_opy_ = TestHubUtils.bstack11l11l1111_opy_(CONFIG, FRAMEWORK_NAME)
  CONFIG[bstack1111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧଉ")] = bstack1111l111ll_opy_
  CONFIG[bstack1111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧଊ")] = bstack11llll11_opy_
  if CONFIG.get(bstack1111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ଋ"),bstack1111l_opy_ (u"ࠧࠨଌ")) and bstack1111l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ଍") in FRAMEWORK_NAME:
    CONFIG[bstack1111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ଎")].pop(bstack1111l_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨଏ"), None)
    CONFIG[bstack1111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫଐ")].pop(bstack1111l_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ଑"), None)
  command_executor = bstack1ll11l111l_opy_()
  logger.debug(bstack11l1l1l1l1_opy_.format(command_executor))
  proxy = bstack11l11l1ll_opy_(CONFIG, proxy)
  bstack111l11l1ll_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
  try:
    if PARALLELISE_VANILLA_PYTHON is True:
      bstack111l11l1ll_opy_ = int(multiprocessing.current_process().name)
    elif PARALLELISE_THREADING_PYTHON is True:
      bstack111l11l1ll_opy_ = int(threading.current_thread().name)
  except:
    bstack111l11l1ll_opy_ = 0
  bstack1ll11lll11_opy_ = get_caps(CONFIG, bstack111l11l1ll_opy_)
  logger.debug(CONFIG_FILE_CONTENT.format(str(bstack1ll11lll11_opy_)))
  if bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ଒") in CONFIG and bstack1ll111llll_opy_(CONFIG[bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫଓ")]):
    update_caps_for_local(bstack1ll11lll11_opy_)
  if a11y.is_enabled_platform(CONFIG, bstack111l11l1ll_opy_) and a11y.is_platform_supported(bstack1ll11lll11_opy_, options, desired_capabilities, CONFIG):
    threading.current_thread().a11yPlatform = True
    if (cli.accessibility is None or not cli.accessibility.is_enabled()):
      a11y.set_capabilities(bstack1ll11lll11_opy_, CONFIG)
  if desired_capabilities:
    bstack1llll111l1_opy_ = bstack1ll1lll1l1_opy_(desired_capabilities)
    bstack1llll111l1_opy_[bstack1111l_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨଔ")] = bstack11l1111l_opy_(CONFIG)
    bstack1llll1ll_opy_ = get_caps(bstack1llll111l1_opy_)
    if bstack1llll1ll_opy_:
      bstack1ll11lll11_opy_ = update(bstack1llll1ll_opy_, bstack1ll11lll11_opy_)
    desired_capabilities = None
  if options:
    bstack1111l11ll_opy_(options, bstack1ll11lll11_opy_)
  if not options:
    options = bstack1l11l1111l_opy_(bstack1ll11lll11_opy_)
  try:
    if bstack11l1l1l1l_opy_:
      def _1l111ll11l_opy_(bstack11l11l1l_opy_):
        if not isinstance(bstack11l11l1l_opy_, dict):
          return
        for _1l11l1l111_opy_ in list(bstack11l11l1l_opy_.keys()):
          _1llllll1l_opy_ = bstack11l11l1l_opy_[_1l11l1l111_opy_]
          if _1llllll1l_opy_ is None:
            bstack11l11l1l_opy_.pop(_1l11l1l111_opy_, None)
          elif isinstance(_1llllll1l_opy_, dict):
            _1l111ll11l_opy_(_1llllll1l_opy_)
      _1l111ll11l_opy_(bstack1ll11lll11_opy_)
      _1l111ll11l_opy_(desired_capabilities)
      if options is not None and hasattr(options, bstack1111l_opy_ (u"ࠩࡢࡧࡦࡶࡳࠨକ")):
        _1l111ll11l_opy_(options._caps)
  except Exception as e:
    logger.debug(bstack1111l_opy_ (u"ࠥࡱࡴࡪ࡟ࡪࡰ࡬ࡸ࠭࠯ࠠࡱࡱࡶࡸ࠲ࡵࡰࡵ࡫ࡲࡲࡸࠦࡰࡳࡷࡱࡩࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡾࠤଖ").format(e))
  if bstack11l1l1l1l_opy_:
    options = bstack11l1111l11_opy_(options)
  bstack111l1l111_opy_ = CONFIG.get(bstack1111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଗ"))[bstack111l11l1ll_opy_]
  if proxy and bstack1l1ll1ll1l_opy_() >= version.parse(bstack1111l_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬଘ")):
    options.proxy(proxy)
  if options and bstack1l1ll1ll1l_opy_() >= version.parse(bstack1111l_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬଙ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1l1ll1ll1l_opy_() < version.parse(bstack1111l_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ଚ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1ll11lll11_opy_)
  logger.info(bstack111l11l11_opy_)
  bstack111l1l1ll1_opy_.end(EVENTS.bstack111l11111l_opy_.value, EVENTS.bstack111l11111l_opy_.value + bstack1111l_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣଛ"), EVENTS.bstack111l11111l_opy_.value + bstack1111l_opy_ (u"ࠤ࠽ࡩࡳࡪࠢଜ"), status=True, failure=None, test_name=SESSION_NAME)
  if bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡵࡸ࡯ࡧ࡫࡯ࡩࠬଝ") in kwargs:
    del kwargs[bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡶࡲࡰࡨ࡬ࡰࡪ࠭ଞ")]
  bstack1l11ll1l1_opy_.end(EVENTS.bstack1l1lll111_opy_.value, bstack1l1llll1_opy_ + bstack1111l_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧଟ"), bstack1l1llll1_opy_ + bstack1111l_opy_ (u"ࠨ࠺ࡦࡰࡧࠦଠ"), status=True, failure=None, test_name=SESSION_NAME)
  try:
    if bstack1l1ll1ll1l_opy_() >= version.parse(bstack1111l_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧଡ")):
      bstack1ll1l1ll_opy_(self, command_executor=command_executor,
                options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
    elif bstack1l1ll1ll1l_opy_() >= version.parse(bstack1111l_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧଢ")):
      bstack1ll1l1ll_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities, options=options,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l1ll1ll1l_opy_() >= version.parse(bstack1111l_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩଣ")):
      bstack1ll1l1ll_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    else:
      bstack1ll1l1ll_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive)
  except Exception as bstack1111l1l1l_opy_:
    logger.error(bstack111llll11l_opy_.format(bstack1111l_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠩତ"), str(bstack1111l1l1l_opy_)))
    raise bstack1111l1l1l_opy_
  bstack1l1llll1_opy_ = bstack1l11ll1l1_opy_.bstack11ll11l1ll_opy_(EVENTS.bstack1l1l11111_opy_.value)
  if a11y.is_enabled_platform(CONFIG, bstack111l11l1ll_opy_) and a11y.is_platform_supported(self.caps, options, desired_capabilities):
    if CONFIG[bstack1111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ଥ")][bstack1111l_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫଦ")] == True:
      threading.current_thread().appA11yPlatform = True
      if cli.accessibility is None or not cli.accessibility.is_enabled():
        a11y.set_capabilities(bstack1ll11lll11_opy_, CONFIG)
  try:
    bstack11111l1ll_opy_ = bstack1111l_opy_ (u"࠭ࠧଧ")
    if bstack1l1ll1ll1l_opy_() >= version.parse(bstack1111l_opy_ (u"ࠧ࠵࠰࠳࠲࠵ࡨ࠱ࠨନ")):
      if self.caps is not None:
        bstack11111l1ll_opy_ = self.caps.get(bstack1111l_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣ଩"))
    else:
      if self.capabilities is not None:
        bstack11111l1ll_opy_ = self.capabilities.get(bstack1111l_opy_ (u"ࠤࡲࡴࡹ࡯࡭ࡢ࡮ࡋࡹࡧ࡛ࡲ࡭ࠤପ"))
    if bstack11111l1ll_opy_:
      bstack11ll11111l_opy_(bstack11111l1ll_opy_)
      if bstack1l1ll1ll1l_opy_() <= version.parse(bstack1111l_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪଫ")):
        if bstack11l11lll11_opy_.startswith(bstack1111l_opy_ (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࠬବ")) or bstack11l11lll11_opy_.startswith(bstack1111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠧଭ")):
          self.command_executor._url = bstack11l11lll11_opy_
        else:
          self.command_executor._url = bstack1111l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢମ") + bstack11l11lll11_opy_ + bstack1111l_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦଯ")
      else:
        self.command_executor._url = bstack1111l_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥର") + bstack11111l1ll_opy_ + bstack1111l_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥ଱")
      logger.debug(bstack1l1lll11l_opy_.format(bstack11111l1ll_opy_))
    else:
      logger.debug(bstack1l11lll111_opy_.format(bstack1111l_opy_ (u"ࠥࡓࡵࡺࡩ࡮ࡣ࡯ࠤࡍࡻࡢࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧࠦଲ")))
  except Exception as e:
    logger.debug(bstack1l11lll111_opy_.format(e))
  if bstack1111l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪଳ") in FRAMEWORK_NAME:
    bstack11lll1ll1_opy_(PLATFORM_INDEX, bstack11lll1ll11_opy_)
  bstack1lll11111_opy_ = self.session_id
  if bstack1111l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ଴") in FRAMEWORK_NAME or bstack1111l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ଵ") in FRAMEWORK_NAME or bstack1111l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ଶ") in FRAMEWORK_NAME or bstack1111l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩଷ") in FRAMEWORK_NAME:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack1111l111l_opy_ = getattr(threading.current_thread(), bstack1111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡖࡨࡷࡹࡓࡥࡵࡣࠪସ"), None)
  if bstack1111l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪହ") in FRAMEWORK_NAME or bstack1111l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ଺") in FRAMEWORK_NAME:
    TestHubHandler.send_cbt_info(self)
  if bstack1111l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ଻") in FRAMEWORK_NAME and bstack1111l111l_opy_ and bstack1111l111l_opy_.get(bstack1111l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ଼࠭"), bstack1111l_opy_ (u"ࠧࠨଽ")) == bstack1111l_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩା"):
    TestHubHandler.send_cbt_info(self)
  with bstack11ll11l1l_opy_:
    bstack1l1lll1ll_opy_.append(self)
  if bstack1111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬି") in CONFIG and bstack1111l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨୀ") in CONFIG[bstack1111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧୁ")][bstack111l11l1ll_opy_]:
    SESSION_NAME = CONFIG[bstack1111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨୂ")][bstack111l11l1ll_opy_][bstack1111l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫୃ")]
  logger.debug(bstack1l11l1ll11_opy_.format(bstack1lll11111_opy_))
  bstack1l11ll1l1_opy_.end(EVENTS.bstack1l1l11111_opy_.value, bstack1l1llll1_opy_ + bstack1111l_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢୄ"), bstack1l1llll1_opy_ + bstack1111l_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ୅"), status=True, failure=None, test_name=SESSION_NAME)
ROBOT_PLAYWRIGHT_CDP_URL = None
bstack1l1l1l1l1l_opy_ = None
def set_playwright_globals(**kwargs):
    bstack1111l_opy_ (u"ࠤࠥࠦࡎࡴࡪࡦࡥࡷࠤ࡬ࡲ࡯ࡣࡣ࡯ࡷࠥ࡬ࡲࡰ࡯ࠣࡣࡤ࡯࡮ࡪࡶࡢࡣ࠳ࡶࡹࠡ࡫ࡱࡸࡴࠦࡴࡩ࡫ࡶࠤࡲࡵࡤࡶ࡮ࡨࠫࡸࠦ࡮ࡢ࡯ࡨࡷࡵࡧࡣࡦ࠰ࠍࠤࠥࠦࠠࡄࡣ࡯ࡰࡪࡪࠠࡣࡻࠣࡣࡤ࡯࡮ࡪࡶࡢࡣ࠳ࡶࡹࠡࡤࡨࡪࡴࡸࡥࠡࡲࡤࡸࡨ࡮࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠬ࠮ࠦࡳࡰࠢࡷ࡬ࡦࡺࠠ࡮ࡱࡧࡣࡱࡧࡵ࡯ࡥ࡫ࠎࠥࠦࠠࠡࡣࡱࡨࠥࡶࡡࡵࡥ࡫ࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡥࡤࡲࠥࡧࡣࡤࡧࡶࡷࠥࡉࡏࡏࡈࡌࡋ࠱ࠦࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࡡࡑࡅࡒࡋࠬࠡࡧࡷࡧ࠳ࠨࠢࠣ୆")
    g = globals()
    for key, value in kwargs.items():
        g[key] = value
try:
  try:
    import Browser
    import os
    from subprocess import Popen
    from browserstack_sdk.__init__ import get_turboscale_playwright_url
    def bstack1ll11ll1l_opy_(self, args, **kwargs):
      global CONFIG
      global SELENIUM_OR_PLAYWRIGHT_INSTALLED
      global ROBOT_PLAYWRIGHT_CDP_URL
      from browserstack_sdk.__init__ import LAUNCH_PATCH_ROBOT_PLAYWRIGHT
      if(bstack1111l_opy_ (u"ࠥ࡭ࡳࡪࡥࡹ࠰࡭ࡷࠧେ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1111l_opy_ (u"ࠫࢃ࠭ୈ")), bstack1111l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ୉"), bstack1111l_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨ୊")), bstack1111l_opy_ (u"ࠧࡸࠩୋ")) as fp:
          fp.write(bstack1111l_opy_ (u"ࠣࠤୌ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1111l_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸࡠࡤࡶࡸࡦࡩ࡫࠯࡬ࡶ୍ࠦ")))):
          with open(args[1], bstack1111l_opy_ (u"ࠪࡶࠬ୎")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1111l_opy_ (u"ࠫࡦࡹࡹ࡯ࡥࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࡥ࡮ࡦࡹࡓࡥ࡬࡫ࠨࡤࡱࡱࡸࡪࡾࡴ࠭ࠢࡳࡥ࡬࡫ࠠ࠾ࠢࡹࡳ࡮ࡪࠠ࠱ࠫࠪ୏") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1l1l1ll11l_opy_)
            if bstack1111l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ୐") in CONFIG and str(CONFIG[bstack1111l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ୑")]).lower() != bstack1111l_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭୒"):
                cdpUrl = get_turboscale_playwright_url()
                LAUNCH_PATCH_ROBOT_PLAYWRIGHT = bstack1111l_opy_ (u"ࠨࠩࠪࠎ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠊࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡰࡢࡶ࡫ࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳࡞࠽ࠍࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠴ࡡࡀࠐࡣࡰࡰࡶࡸࠥࡶ࡟ࡪࡰࡧࡩࡽࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠴ࡠ࠿ࠏࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡹ࡬ࡪࡥࡨࠬ࠵࠲ࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࠬ࠿ࠏࡩ࡯࡯ࡵࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬ࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ࠭ࡀࠐࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴࡬ࡢࡷࡱࡧ࡭ࠦ࠽ࠡࡣࡶࡽࡳࡩࠠࠩ࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁࡻࠋࠢࠣࡰࡪࡺࠠࡤࡣࡳࡷࡀࠐࠠࠡࡶࡵࡽࠥࢁࡻࠋࠢࠣࠤࠥࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࠼ࠌࠣࠤࢂࢃࠠࡤࡣࡷࡧ࡭ࠦࠨࡦࡺࠬࠤࢀࢁࠊࠡࠢࠣࠤࡨࡵ࡮ࡴࡱ࡯ࡩ࠳࡫ࡲࡳࡱࡵࠬࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࡀࠢ࠭ࠢࡨࡼ࠮ࡁࠊࠡࠢࢀࢁࠏࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠨࡼࡽࠍࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥ࠭ࡻࡤࡦࡳ࡙ࡷࡲࡽࠨࠢ࠮ࠤࡪࡴࡣࡰࡦࡨ࡙ࡗࡏࡃࡰ࡯ࡳࡳࡳ࡫࡮ࡵࠪࡍࡗࡔࡔ࠮ࡴࡶࡵ࡭ࡳ࡭ࡩࡧࡻࠫࡧࡦࡶࡳࠪࠫ࠯ࠎࠥࠦࠠࠡ࠰࠱࠲ࡱࡧࡵ࡯ࡥ࡫ࡓࡵࡺࡩࡰࡰࡶࠎࠥࠦࡽࡾࠫ࠾ࠎࢂࢃ࠻ࠋࡥࡲࡲࡸࡺࠠࡰࡴ࡬࡫࡮ࡴࡡ࡭ࡡࡦࡳࡳࡴࡥࡤࡶࠣࡁࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡩ࡯࡯ࡰࡨࡧࡹ࠴ࡢࡪࡰࡧࠬ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠭ࡀࠐࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠠ࠾ࠢࡤࡷࡾࡴࡣࠡࠪࡦࡳࡳࡴࡥࡤࡶࡒࡴࡹ࡯࡯࡯ࡵࠬࠤࡂࡄࠠࡼࡽࠍࠤࠥࡲࡥࡵࠢࡦࡥࡵࡹ࠻ࠋࠢࠣࡸࡷࡿࠠࡼࡽࠍࠤࠥࠦࠠࡤࡣࡳࡷࠥࡃࠠࡋࡕࡒࡒ࠳ࡶࡡࡳࡵࡨࠬࡧࡹࡴࡢࡥ࡮ࡣࡨࡧࡰࡴࠫ࠾ࠎࠥࠦࡽࡾࠢࡦࡥࡹࡩࡨࠡࠪࡨࡼ࠮ࠦࡻࡼࠌࠣࠤࢂࢃࠊࠡࠢࡦࡳࡳࡹࡴࠡ࡯ࡲࡨ࡮࡬ࡩࡦࡦࡈࡲࡩࡶ࡯ࡪࡰࡷࠤࡂࠦࠧࡼࡥࡧࡴ࡚ࡸ࡬ࡾࠩࠣ࠯ࠥ࡫࡮ࡤࡱࡧࡩ࡚ࡘࡉࡄࡱࡰࡴࡴࡴࡥ࡯ࡶࠫࡎࡘࡕࡎ࠯ࡵࡷࡶ࡮ࡴࡧࡪࡨࡼࠬࡨࡧࡰࡴࠫࠬ࠿ࠏࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦ࡯ࡳ࡫ࡪ࡭ࡳࡧ࡬ࡠࡥࡲࡲࡳ࡫ࡣࡵࠪࡾࡿࠏࠦࠠࠡࠢ࠱࠲࠳ࡩ࡯࡯ࡰࡨࡧࡹࡕࡰࡵ࡫ࡲࡲࡸ࠲ࠊࠡࠢࠣࠤࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࠻ࠢࡰࡳࡩ࡯ࡦࡪࡧࡧࡉࡳࡪࡰࡰ࡫ࡱࡸࠏࠦࠠࡾࡿࠬ࠿ࠏࢃࡽ࠼ࠌ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࠏ࠭ࠧࠨ୓").format(cdpUrl=cdpUrl)
            lines.insert(1, LAUNCH_PATCH_ROBOT_PLAYWRIGHT)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1111l_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸࡠࡤࡶࡸࡦࡩ࡫࠯࡬ࡶࠦ୔")), bstack1111l_opy_ (u"ࠪࡻࠬ୕")) as bstack1l11ll11l1_opy_:
              bstack1l11ll11l1_opy_.writelines(lines)
        CONFIG[bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ୖ")] = str(FRAMEWORK_NAME) + str(__version__)
        bstack1111l111ll_opy_ = os.environ[bstack1111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪୗ")]
        bstack11llll11_opy_ = TestHubUtils.bstack11l11l1111_opy_(CONFIG, FRAMEWORK_NAME)
        CONFIG[bstack1111l_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ୘")] = bstack1111l111ll_opy_
        CONFIG[bstack1111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩ୙")] = bstack11llll11_opy_
        bstack111l11l1ll_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
        try:
          if PARALLELISE_VANILLA_PYTHON is True:
            bstack111l11l1ll_opy_ = int(multiprocessing.current_process().name)
          elif PARALLELISE_THREADING_PYTHON is True:
            bstack111l11l1ll_opy_ = int(threading.current_thread().name)
        except Exception:
          bstack111l11l1ll_opy_ = 0
        CONFIG[bstack1111l_opy_ (u"ࠣࡷࡶࡩ࡜࠹ࡃࠣ୚")] = False
        CONFIG[bstack1111l_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ୛")] = True
        bstack1ll11lll11_opy_ = get_caps(CONFIG, bstack111l11l1ll_opy_)
        logger.debug(CONFIG_FILE_CONTENT.format(str(bstack1ll11lll11_opy_)))
        if CONFIG.get(bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧଡ଼")):
          update_caps_for_local(bstack1ll11lll11_opy_)
          bstack1ll11lll11_opy_[bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬଢ଼")] = os.environ[bstack1111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ୞")]
        import urllib.parse
        if bstack1111l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪୟ") in CONFIG and str(CONFIG[bstack1111l_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫୠ")]).lower() != bstack1111l_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧୡ"):
          ROBOT_PLAYWRIGHT_CDP_URL = get_turboscale_playwright_url() + urllib.parse.quote(json.dumps(bstack1ll11lll11_opy_))
        else:
          ROBOT_PLAYWRIGHT_CDP_URL = bstack1111l_opy_ (u"ࠩࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠫୢ") + urllib.parse.quote(json.dumps(bstack1ll11lll11_opy_))
        os.environ[bstack1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡓࡇࡕࡔࡠࡒ࡚ࡣࡈࡊࡐࡠࡗࡕࡐࠬୣ")] = ROBOT_PLAYWRIGHT_CDP_URL
        if bstack1111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ୤") in CONFIG and bstack1111l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ୥") in CONFIG[bstack1111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ୦")][bstack111l11l1ll_opy_]:
          SESSION_NAME = CONFIG[bstack1111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ୧")][bstack111l11l1ll_opy_][bstack1111l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭୨")]
        args.append(os.path.join(os.path.expanduser(bstack1111l_opy_ (u"ࠩࢁࠫ୩")), bstack1111l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ୪"), bstack1111l_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭୫")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1ll11lll11_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1111l_opy_ (u"ࠧ࡯࡮ࡥࡧࡻࡣࡧࡹࡴࡢࡥ࡮࠲࡯ࡹࠢ୬"))
      SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
      return bstack111l11l1l_opy_(self, args, **kwargs)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack11ll111l1_opy_(self,
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
    CONFIG[bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ୭")] = str(FRAMEWORK_NAME) + str(__version__)
    bstack1111l111ll_opy_ = os.environ[bstack1111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ୮")]
    bstack11llll11_opy_ = TestHubUtils.bstack11l11l1111_opy_(CONFIG, FRAMEWORK_NAME)
    CONFIG[bstack1111l_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ୯")] = bstack1111l111ll_opy_
    CONFIG[bstack1111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ୰")] = bstack11llll11_opy_
    bstack111l11l1ll_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
    try:
      if PARALLELISE_VANILLA_PYTHON is True:
        bstack111l11l1ll_opy_ = int(multiprocessing.current_process().name)
      elif PARALLELISE_THREADING_PYTHON is True:
        bstack111l11l1ll_opy_ = int(threading.current_thread().name)
    except Exception:
      bstack111l11l1ll_opy_ = 0
    CONFIG[bstack1111l_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤୱ")] = True
    bstack1ll11lll11_opy_ = get_caps(CONFIG, bstack111l11l1ll_opy_)
    bstack1lllll11_opy_ = bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬ୲") if bstack1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭୳") in bstack1ll11lll11_opy_ else bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ୴")
    bstack1ll1111l_opy_ = False
    try:
        from bstack_utils import accessibility as a11y
        import bstack_utils.constants as bstack111l11l1l1_opy_
        bstack1ll1ll1l_opy_ = bstack1ll11lll11_opy_.get(bstack1lllll11_opy_, bstack1111l_opy_ (u"ࠧࠨ୵")).strip().lower()
        browser_version = str(bstack1ll11lll11_opy_.get(bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪ୶"), bstack1ll11lll11_opy_.get(bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ୷"), bstack1111l_opy_ (u"ࠪࠫ୸")))).strip()
        bstack1l111ll11_opy_ = bstack1ll1ll1l_opy_ in (bstack1111l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫ୹"), bstack1111l_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠯ࡦ࡬ࡷࡵ࡭ࡪࡷࡰࠫ୺"), bstack1111l_opy_ (u"࠭ࡣࡩࡴࡲࡱ࡮ࡻ࡭ࠨ୻"))
        min_version = bstack111l11l1l1_opy_.MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION
        if not browser_version or browser_version.lower().startswith(bstack1111l_opy_ (u"ࠧ࡭ࡣࡷࡩࡸࡺࠧ୼")):
            bstack111l1ll11_opy_ = True
        else:
            major = browser_version.split(bstack1111l_opy_ (u"ࠨ࠰ࠪ୽"))[0]
            bstack111l1ll11_opy_ = major.isdigit() and int(major) > min_version
        if not bstack111l1ll11_opy_:
            logger.warning(bstack1111l_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࠣࡺࡪࡸࡳࡪࡱࡱࠤ࡬ࡸࡥࡢࡶࡨࡶࠥࡺࡨࡢࡰࠣࡿࢂ࠴ࠠࡄࡷࡵࡶࡪࡴࡴࠡࡸࡨࡶࡸ࡯࡯࡯࠼ࠣࡿࢂࠨ୾").format(min_version, browser_version))
        if a11y.is_enabled_platform(CONFIG, bstack111l11l1ll_opy_) and bstack1l111ll11_opy_ and bstack111l1ll11_opy_ and a11y.is_platform_supported(bstack1ll11lll11_opy_, options=None, config=CONFIG):
            bstack1ll1111l_opy_ = True
            import browserstack_sdk
            browserstack_sdk.CONFIG[bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ୿")] = True
            bstack1ll11lll11_opy_[bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ஀")] = True
            if CONFIG.get(bstack1111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧ஁")):
                bstack1ll11lll11_opy_[bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧஂ")] = CONFIG[bstack1111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩஃ")]
            import json as _json
            bstack111l11111_opy_ = os.getenv(bstack1111l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭஄"))
            bstack1l1l1l111_opy_ = bstack1ll11lll11_opy_.get(bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳ࠯ࡣࡸࡸ࡭࡚࡯࡬ࡧࡱࠫஅ"))
            if not bstack111l11111_opy_ and bstack1l1l1l111_opy_:
                os.environ[bstack1111l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨஆ")] = bstack1l1l1l111_opy_
                bstack111l11111_opy_ = bstack1l1l1l111_opy_
            if bstack111l11111_opy_:
                bstack1ll11lll11_opy_[bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵ࠱ࡥࡺࡺࡨࡕࡱ࡮ࡩࡳ࠭இ")] = bstack111l11111_opy_
            bstack1llll111_opy_ = _json.loads(os.getenv(bstack1111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ஈ"), bstack1111l_opy_ (u"࠭ࡻࡾࠩஉ"))).get(bstack1111l_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨஊ"))
            if bstack1llll111_opy_:
                bstack1ll11lll11_opy_[bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹ࠮ࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ஋")] = bstack1llll111_opy_
            bstack1ll11lll11_opy_.pop(bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ஌"), None)
            bstack1ll11lll11_opy_.pop(bstack1111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ஍"), None)
            bstack1ll11lll11_opy_.pop(bstack1111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫஎ"), None)
            logger.debug(bstack1111l_opy_ (u"ࠧࡇ࠱࠲ࡻࠣࡩࡳࡧࡢ࡭ࡧࡧࠤ࡫ࡵࡲࠡࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࠨࡼࡿࠣࡿࢂ࠯ࠢஏ").format(
                bstack1ll1ll1l_opy_, browser_version))
    except Exception as e:
        bstack1ll1111l_opy_ = False
        logger.debug(bstack1111l_opy_ (u"ࠨࡁ࠲࠳ࡼࠤࡩ࡫ࡴࡦࡥࡷ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡽࢀࠦஐ").format(str(e)))
    logger.debug(CONFIG_FILE_CONTENT.format(str(bstack1ll11lll11_opy_)))
    if CONFIG.get(bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ஑")):
      update_caps_for_local(bstack1ll11lll11_opy_)
    if bstack1111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫஒ") in CONFIG and bstack1111l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧஓ") in CONFIG[bstack1111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ஔ")][bstack111l11l1ll_opy_]:
      SESSION_NAME = CONFIG[bstack1111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧக")][bstack111l11l1ll_opy_][bstack1111l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ஖")]
    import urllib
    import json
    if bstack1111l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ஗") in CONFIG and str(CONFIG[bstack1111l_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ஘")]).lower() != bstack1111l_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧங"):
        bstack1l11111ll_opy_ = get_turboscale_playwright_url()
        cdpUrl = bstack1l11111ll_opy_ + urllib.parse.quote(json.dumps(bstack1ll11lll11_opy_))
    else:
        cdpUrl = bstack1111l_opy_ (u"ࠩࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠫச") + urllib.parse.quote(json.dumps(bstack1ll11lll11_opy_))
    try:
        from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
        PlaywrightDriverWrapperDirect.setup_dispatch_capture()
    except Exception as exc:
        logger.debug(bstack1111l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࡸࡴࠥࡪࡩࡴࡲࡤࡸࡨ࡮ࠠࡤࡣࡳࡸࡺࡸࡥࠡࡨࡲࡶࠥࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥ࠼ࠣࠩࡸࠨ஛"), exc)
    if bstack1ll1111l_opy_:
        browser = self.connect_over_cdp(cdpUrl)
    else:
        browser = bstack1l1l1l1l1l_opy_(self, cdpUrl)
    try:
        from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
        wrapper = PlaywrightDriverWrapperDirect(browser, page=None, capabilities=bstack1ll11lll11_opy_, config=CONFIG)
        threading.current_thread().bstackSessionDriver = wrapper
        logger.debug(bstack1111l_opy_ (u"ࠦࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡅࡴ࡬ࡺࡪࡸࡗࡳࡣࡳࡴࡪࡸࡄࡪࡴࡨࡧࡹࠦࡳࡦࡶࡸࡴࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫ࠠࡧࡱࡵࠤࡹ࡮ࡲࡦࡣࡧࠤࠪࡹࠢஜ"), threading.get_ident())
        threading.current_thread().bstackTestErrorMessages = []
        if bstack1ll1111l_opy_:
            threading.current_thread().a11yPlatform = True
            wrapper.bstackA11yShouldScan = True
        if wrapper.session_id and not wrapper._cbt_info_sent:
            PlaywrightDriverWrapperDirect._send_cbt_info_on_session()
        try:
            from playwright.sync_api import Browser as bstack1111l11l1l_opy_
            if not hasattr(bstack1111l11l1l_opy_, bstack1111l_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥ࡮ࡦࡹࡢࡴࡦ࡭ࡥࡠࡲࡤࡸࡨ࡮ࡥࡥࠩ஝")):
                _1l1ll11l1l_opy_ = bstack1111l11l1l_opy_.new_page
                def _11ll11l1l1_opy_(bstack1l1ll11ll_opy_, *bstack1111lll1ll_opy_, **bstack111ll1l1_opy_):
                    if getattr(threading.current_thread(), bstack1111l_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬஞ"), None):
                        try:
                            bstack1lll11l111_opy_ = bstack1l1ll11ll_opy_.contexts[0] if bstack1l1ll11ll_opy_.contexts else None
                            if bstack1lll11l111_opy_ and bstack1lll11l111_opy_.pages:
                                page = None
                                for _1l1111l11l_opy_ in bstack1lll11l111_opy_.pages:
                                    if bstack1111l_opy_ (u"ࠢࡢࡤࡲࡹࡹࡀࡢ࡭ࡣࡱ࡯ࠧட") in _1l1111l11l_opy_.url:
                                        page = _1l1111l11l_opy_
                                        logger.debug(bstack1111l_opy_ (u"ࠣࡃ࠴࠵ࡾࡀࠠࡳࡧࡸࡷ࡮ࡴࡧࠡࡣࡥࡳࡺࡺ࠺ࡣ࡮ࡤࡲࡰࠦࡰࡢࡩࡨࠤ࡫ࡸ࡯࡮ࠢࡧࡩ࡫ࡧࡵ࡭ࡶࠣࡧࡴࡴࡴࡦࡺࡷࠦ஠"))
                                        break
                                if page is None:
                                    page = bstack1lll11l111_opy_.new_page(*bstack1111lll1ll_opy_, **bstack111ll1l1_opy_)
                                    logger.debug(bstack1111l_opy_ (u"ࠤࡄ࠵࠶ࡿ࠺ࠡࡰࡲࠤࡧࡲࡡ࡯࡭ࠣࡴࡦ࡭ࡥࠡࡨࡲࡹࡳࡪࠬࠡࡥࡵࡩࡦࡺࡥࡥࠢࡱࡩࡼࠦࡰࡢࡩࡨࠤ࡮ࡴࠠࡥࡧࡩࡥࡺࡲࡴࠡࡥࡲࡲࡹ࡫ࡸࡵࠤ஡"))
                            elif bstack1lll11l111_opy_:
                                page = bstack1lll11l111_opy_.new_page(*bstack1111lll1ll_opy_, **bstack111ll1l1_opy_)
                                logger.debug(bstack1111l_opy_ (u"ࠥࡅ࠶࠷ࡹ࠻ࠢࡦࡶࡪࡧࡴࡦࡦࠣࡲࡪࡽࠠࡱࡣࡪࡩࠥ࡯࡮ࠡࡦࡨࡪࡦࡻ࡬ࡵࠢࡦࡳࡳࡺࡥࡹࡶࠥ஢"))
                            else:
                                page = _1l1ll11l1l_opy_(bstack1l1ll11ll_opy_, *bstack1111lll1ll_opy_, **bstack111ll1l1_opy_)
                                logger.debug(bstack1111l_opy_ (u"ࠦࡆ࠷࠱ࡺ࠼ࠣࡲࡴࠦࡤࡦࡨࡤࡹࡱࡺࠠࡤࡱࡱࡸࡪࡾࡴ࠭ࠢࡩࡥࡱࡲࡩ࡯ࡩࠣࡦࡦࡩ࡫ࠡࡶࡲࠤࡳ࡫ࡷࡠࡲࡤ࡫ࡪ࠮ࠩࠣண"))
                        except Exception as bstack11l111111l_opy_:
                            logger.debug(bstack1111l_opy_ (u"ࠧࡇ࠱࠲ࡻ࠽ࠤࡩ࡫ࡦࡢࡷ࡯ࡸࠥࡩ࡯࡯ࡶࡨࡼࡹࠦࡰࡢࡩࡨࠤࡷ࡫ࡵࡴࡧࠣࡪࡦ࡯࡬ࡦࡦࠣࠬࠪࡹࠩ࠭ࠢࡩࡥࡱࡲࡩ࡯ࡩࠣࡦࡦࡩ࡫ࠣத"), bstack11l111111l_opy_)
                            page = _1l1ll11l1l_opy_(bstack1l1ll11ll_opy_, *bstack1111lll1ll_opy_, **bstack111ll1l1_opy_)
                    else:
                        page = _1l1ll11l1l_opy_(bstack1l1ll11ll_opy_, *bstack1111lll1ll_opy_, **bstack111ll1l1_opy_)
                    try:
                        _w = getattr(threading.current_thread(), bstack1111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ஥"), None)
                        if _w and hasattr(_w, bstack1111l_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫࡟ࡱࡣࡪࡩࠬ஦")):
                            _w.update_page(page)
                        if _w and not _w.session_id:
                            try:
                                import json as _json
                                result = page.evaluate(
                                    bstack1111l_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ஧"), bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡪࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡥࡵࡣ࡬ࡰࡸࠨࡽࠨந"))
                                if isinstance(result, str):
                                    result = _json.loads(result)
                                if isinstance(result, dict):
                                    sid = result.get(bstack1111l_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ன")) or result.get(bstack1111l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨப")) or result.get(bstack1111l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡏࡤࠨ஫"))
                                    if sid:
                                        import threading as _11lllll11l_opy_
                                        from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
                                        with PlaywrightDriverWrapperDirect._session_ids_lock:
                                            PlaywrightDriverWrapperDirect._session_ids[_11lllll11l_opy_.get_ident()] = sid
                                        logger.debug(bstack1111l_opy_ (u"ࠨࡃࡢࡲࡷࡹࡷ࡫ࡤࠡࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠥࡼࡩࡢࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠪࡹࠢ஬"), sid)
                                        PlaywrightDriverWrapperDirect._send_cbt_info_on_session()
                                    else:
                                        logger.debug(bstack1111l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲࠡࡩࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡉ࡫ࡴࡢ࡫࡯ࡷࠥࡸࡥࡵࡷࡵࡲࡪࡪࠠ࡯ࡱࠣࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪ࠺ࠡࠧࡶࠦ஭"), result)
                                else:
                                    logger.debug(bstack1111l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠢࡪࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡥࡵࡣ࡬ࡰࡸࠦࡲࡦࡵࡸࡰࡹࡀࠠࠦࡵࠥம"), result)
                            except Exception as _111l1llll1_opy_:
                                logger.debug(bstack1111l_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠦࡦࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡸ࡬ࡥࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࠦࡵࠥய"), _111l1llll1_opy_)
                        if (getattr(threading.current_thread(), bstack1111l_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩர"), None)
                                and not getattr(threading.current_thread(), bstack1111l_opy_ (u"ࠫࡦ࠷࠱ࡺࡡࡶࡸࡦࡸࡴࡦࡦࠪற"), False)):
                            threading.current_thread().a11y_started = True
                            try:
                                from bstack_utils import accessibility as _1ll11l1l_opy_
                                bstack1lllll1l1_opy_ = getattr(threading.current_thread(), bstack1111l_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩல"), True)
                                _1ll11l1l_opy_.start_test_capture(_w, bstack1lllll1l1_opy_)
                            except Exception:
                                logger.debug(bstack1111l_opy_ (u"ࠨࡄࡦࡨࡨࡶࡷ࡫ࡤࠡࡃ࠴࠵ࡾࠦࡳࡵࡣࡵࡸࡤࡺࡥࡴࡶࡢࡧࡦࡶࡴࡶࡴࡨࠤ࡫ࡧࡩ࡭ࡧࡧࠦள"))
                    except Exception as exc:
                        logger.debug(bstack1111l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡹࡵࡪࡡࡵࡧࠣࡴࡦ࡭ࡥࠡ࡫ࡱࠤࡼࡸࡡࡱࡲࡨࡶ࠿ࠦࠥࡴࠤழ"), exc)
                    return page
                bstack1111l11l1l_opy_.new_page = _11ll11l1l1_opy_
                bstack1111l11l1l_opy_._bstack_new_page_patched = True
        except Exception as exc:
            logger.debug(bstack1111l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡴࡤࡪࠣࡗࡾࡴࡣࡃࡴࡲࡻࡸ࡫ࡲ࠯ࡰࡨࡻࡤࡶࡡࡨࡧࠣࡪࡴࡸࠠࡱࡣࡪࡩࠥࡩࡡࡱࡶࡸࡶࡪࡀࠠࠦࡵࠥவ"), exc)
        try:
            from playwright.sync_api import Page as bstack11111111_opy_, Browser as _11l11ll111_opy_
            if not hasattr(bstack11111111_opy_, bstack1111l_opy_ (u"ࠩࡢࡦࡸࡺࡡࡤ࡭ࡢࡴࡦ࡭ࡥࡠࡥ࡯ࡳࡸ࡫࡟ࡱࡣࡷࡧ࡭࡫ࡤࠨஶ")):
                _111111l11_opy_ = bstack11111111_opy_.close
                def _1ll11ll11_opy_(bstack1ll1l11lll_opy_, *bstack111lllll1l_opy_, _bstack_sdk_close=False, **bstack111ll1l1ll_opy_):
                    if not _bstack_sdk_close:
                        logger.debug(bstack1111l_opy_ (u"ࠥࡈࡪ࡬ࡥࡳࡴࡨࡨࠥࡶࡡࡨࡧ࠱ࡧࡱࡵࡳࡦࠪࠬࠤ⠙ࠦࡷࡪ࡮࡯ࠤࡨࡲ࡯ࡴࡧࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢஷ"))
                        threading.current_thread().bstack_deferred_page_close = True
                        threading.current_thread().bstack_deferred_page_ref = bstack1ll1l11lll_opy_
                        return
                    return _111111l11_opy_(bstack1ll1l11lll_opy_, *bstack111lllll1l_opy_, **bstack111ll1l1ll_opy_)
                bstack11111111_opy_.close = _1ll11ll11_opy_
                bstack11111111_opy_._bstack_page_close_patched = True
            if not hasattr(_11l11ll111_opy_, bstack1111l_opy_ (u"ࠫࡤࡨࡳࡵࡣࡦ࡯ࡤࡨࡲࡰࡹࡶࡩࡷࡥࡣ࡭ࡱࡶࡩࡤࡶࡡࡵࡥ࡫ࡩࡩ࠭ஸ")):
                _1llll11111_opy_ = _11l11ll111_opy_.close
                def _11l1lll11l_opy_(bstack1l1ll11ll_opy_, *bstack111lll1ll1_opy_, _bstack_sdk_close=False, **bstack11l1111ll1_opy_):
                    if not _bstack_sdk_close:
                        logger.debug(bstack1111l_opy_ (u"ࠧࡊࡥࡧࡧࡵࡶࡪࡪࠠࡣࡴࡲࡻࡸ࡫ࡲ࠯ࡥ࡯ࡳࡸ࡫ࠨࠪࠢ⠗ࠤࡼ࡯࡬࡭ࠢࡦࡰࡴࡹࡥࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧஹ"))
                        threading.current_thread().bstack_deferred_browser_close = True
                        threading.current_thread().bstack_deferred_browser_ref = bstack1l1ll11ll_opy_
                        return
                    return _1llll11111_opy_(bstack1l1ll11ll_opy_, *bstack111lll1ll1_opy_, **bstack11l1111ll1_opy_)
                _11l11ll111_opy_.close = _11l1lll11l_opy_
                _11l11ll111_opy_._bstack_browser_close_patched = True
            if not hasattr(bstack11111111_opy_, bstack1111l_opy_ (u"࠭࡟ࡣࡵࡷࡥࡨࡱ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡣࡵࡧࡴࡤࡪࡨࡨࠬ஺")):
                _1ll1l1l11_opy_ = bstack11111111_opy_.screenshot
                def _1111l1l11_opy_(bstack1ll1l11lll_opy_, *bstack1111lll11l_opy_, **bstack1l1ll11ll1_opy_):
                    result = _1ll1l1l11_opy_(bstack1ll1l11lll_opy_, *bstack1111lll11l_opy_, **bstack1l1ll11ll1_opy_)
                    try:
                        from bstack_utils.testhub_handler import TestHubHandler
                        from bstack_utils.bstack1lll1lll_opy_ import bstack11l11ll1l1_opy_
                        if bstack11l11ll1l1_opy_.on():
                            import base64
                            if isinstance(result, bytes):
                                bstack1l1l1llll_opy_ = base64.b64encode(result).decode(bstack1111l_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭஻"))
                            else:
                                bstack1l1l1llll_opy_ = str(result)
                            test_uuid = TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack11l11ll1l1_opy_.current_hook_uuid()
                            if test_uuid and bstack1l1l1llll_opy_:
                                TestHubHandler.bstack11l1lll1l1_opy_({
                                    bstack1111l_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧ஼"): bstack1l1l1llll_opy_,
                                    bstack1111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ஽"): test_uuid
                                })
                                logger.debug(bstack1111l_opy_ (u"ࠥࡗࡪࡴࡴࠡࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠢࡷࡳࠥࡕ࠱࠲ࡻࠣࡪࡴࡸࠠࡵࡧࡶࡸࠥࢁࡽࠣா").format(test_uuid))
                    except Exception as bstack1lll1l1lll_opy_:
                        logger.debug(bstack1111l_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡱࡨࠥࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠦࡴࡰࠢࡒ࠵࠶ࡿ࠺ࠡࡽࢀࠦி").format(str(bstack1lll1l1lll_opy_)))
                    return result
                bstack11111111_opy_.screenshot = _1111l1l11_opy_
                bstack11111111_opy_._bstack_screenshot_patched = True
        except Exception as exc:
            logger.debug(bstack1111l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡨࠤࡩ࡫ࡦࡦࡴࡵࡩࡩࠦࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡧࡱࡵࡳࡦࠢ࡫ࡳࡴࡱࡳ࠻ࠢࠨࡷࠧீ"), exc)
        logger.debug(bstack1111l_opy_ (u"ࠨࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡇࡶ࡮ࡼࡥࡳ࡙ࡵࡥࡵࡶࡥࡳࡆ࡬ࡶࡪࡩࡴࠡࡵࡨࡸࡺࡶࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࠢࡩࡳࡷࠦࡴࡩࡴࡨࡥࡩࠦࡻࡾࠤு").format(threading.get_ident()))
    except Exception as e:
        logger.debug(bstack1111l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡷࡳࡣࡳࡴࡪࡸ࠺ࠡࡽࢀࠦூ").format(str(e)))
    return browser
  async def bstack1ll1lll1l_opy_(self, *args, **kwargs):
    global bstack1l1l1l1l1l_opy_, CONFIG, FRAMEWORK_NAME, __version__, BROWSERSTACK_AUTOMATION
    global PLATFORM_INDEX, PARALLELISE_VANILLA_PYTHON, PARALLELISE_THREADING_PYTHON, SESSION_NAME
    import urllib.parse as _1l11l1ll1l_opy_
    import json
    ws_endpoint = args[0] if args else kwargs.get(bstack1111l_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬ௃"), kwargs.get(bstack1111l_opy_ (u"ࠩࡺࡷࡤ࡫࡮ࡥࡲࡲ࡭ࡳࡺࠧ௄"), bstack1111l_opy_ (u"ࠪࠫ௅")))
    bstack11ll1l1ll1_opy_ = (ws_endpoint
                 and bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧெ") in str(ws_endpoint)
                 and bstack1111l_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫே") in str(ws_endpoint))
    bstack1llll11ll_opy_ = {}
    if bstack11ll1l1ll1_opy_:
        from bstack_utils.helper import bstack111l1ll11l_opy_
        bstack1l1ll1lll1_opy_ = bstack111l1ll11l_opy_()
        try:
            if bstack1l1ll1lll1_opy_:
                CONFIG[bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨை")] = str(FRAMEWORK_NAME) + str(__version__)
                bstack1111l111ll_opy_ = os.environ.get(bstack1111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ௉"), bstack1111l_opy_ (u"ࠨࠩொ"))
                if bstack1111l111ll_opy_:
                    CONFIG[bstack1111l_opy_ (u"ࠩࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬோ")] = bstack1111l111ll_opy_
                CONFIG[bstack1111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬௌ")] = TestHubUtils.bstack11l11l1111_opy_(CONFIG, FRAMEWORK_NAME)
                bstack111l11l1ll_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
                try:
                    if PARALLELISE_VANILLA_PYTHON is True:
                        bstack111l11l1ll_opy_ = int(multiprocessing.current_process().name)
                    elif PARALLELISE_THREADING_PYTHON is True:
                        bstack111l11l1ll_opy_ = int(threading.current_thread().name)
                except Exception:
                    bstack111l11l1ll_opy_ = 0
                CONFIG[bstack1111l_opy_ (u"ࠦ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ்ࠥ")] = True
                bstack1llll11ll_opy_ = get_caps(CONFIG, bstack111l11l1ll_opy_)
                if CONFIG.get(bstack1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ௎")):
                    update_caps_for_local(bstack1llll11ll_opy_)
                if bstack1111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ௏") in CONFIG and bstack1111l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬௐ") in CONFIG[bstack1111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ௑")][bstack111l11l1ll_opy_]:
                    SESSION_NAME = CONFIG[bstack1111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ௒")][bstack111l11l1ll_opy_][bstack1111l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ௓")]
                logger.debug(bstack1111l_opy_ (u"ࠦࡈࡧࡳࡦࠢࡄ࠾ࠥࡘࡥࡱ࡮ࡤࡧࡪࡪࠠࡶࡵࡨࡶࠥࡩࡡࡱࡵࠣࡻ࡮ࡺࡨࠡࡻࡰࡰࠥࡩࡡࡱࡵ࠽ࠤࢀࢃࠢ௔").format(str(bstack1llll11ll_opy_)))
            else:
                bstack11l1ll1ll_opy_ = str(ws_endpoint).split(bstack1111l_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫ௕"))[1]
                bstack1llll11ll_opy_ = json.loads(_1l11l1ll1l_opy_.unquote(bstack11l1ll1ll_opy_))
                bstack1llll11ll_opy_ = bstack1llll11ll_opy_ or {}
                bstack1111l111ll_opy_ = os.environ.get(bstack1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ௖"), bstack1111l_opy_ (u"ࠧࠨௗ"))
                bstack11llll11_opy_ = TestHubUtils.bstack11l11l1111_opy_(CONFIG, FRAMEWORK_NAME)
                bstack1llll11ll_opy_[bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ௘")] = str(FRAMEWORK_NAME) + str(__version__)
                bstack1llll11ll_opy_[bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ௙")] = BROWSERSTACK_AUTOMATION
                if bstack1111l111ll_opy_:
                    bstack1llll11ll_opy_[bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬ௚")] = bstack1111l111ll_opy_
                bstack1llll11ll_opy_[bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬ௛")] = bstack11llll11_opy_
                logger.debug(bstack1111l_opy_ (u"ࠧࡉࡡࡴࡧࠣࡈ࠿ࠦࡍࡦࡴࡪࡩࡩࠦࡓࡅࡍࠣࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࠦࡩ࡯ࡶࡲࠤࡺࡹࡥࡳࠢࡦࡥࡵࡹࠢ௜"))
            ws_url = str(ws_endpoint).split(bstack1111l_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬ௝"))[0]
            ws_endpoint = ws_url + bstack1111l_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭௞") + _1l11l1ll1l_opy_.quote(json.dumps(bstack1llll11ll_opy_))
            if args:
                args = (ws_endpoint,) + args[1:]
            else:
                if bstack1111l_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬ௟") in kwargs:
                    kwargs[bstack1111l_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭௠")] = ws_endpoint
                else:
                    kwargs[bstack1111l_opy_ (u"ࠪࡻࡸࡥࡥ࡯ࡦࡳࡳ࡮ࡴࡴࠨ௡")] = ws_endpoint
            logger.debug(bstack1111l_opy_ (u"ࠦࡑ࡫ࡧࡢࡥࡼࠤࡨࡵ࡮࡯ࡧࡦࡸ࡛ࠥࡒࡍࠢࡸࡴࡩࡧࡴࡦࡦࠣࡻ࡮ࡺࡨࠡࡽࢀࠤࡨࡧࡰࡴࠤ௢").format(bstack1111l_opy_ (u"ࠧࡿ࡭࡭ࠤ௣") if bstack1l1ll1lll1_opy_ else bstack1111l_opy_ (u"ࠨࡴࡦ࡮ࡨࡱࡪࡺࡲࡺࠤ௤")))
        except Exception as e:
            logger.debug(bstack1111l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡪࡸࡧࡦࠢࡦࡥࡵࡹࠠࡪࡰࡷࡳࠥࡩ࡯࡯ࡰࡨࡧࡹࠦࡕࡓࡎ࠽ࠤࢀࢃࠢ௥").format(str(e)))
        try:
            from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
            PlaywrightDriverWrapperDirect.setup_dispatch_capture()
        except Exception as exc:
            logger.debug(bstack1111l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࡶࡲࠣࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠥࡩࡡࡱࡶࡸࡶࡪࠦࡩ࡯ࠢࡰࡳࡩࡥࡣࡰࡰࡱࡩࡨࡺ࠺ࠡࠧࡶࠦ௦"), exc)
    browser = await bstack1l1l1l1l1l_opy_(self, *args, **kwargs)
    if bstack11ll1l1ll1_opy_:
        try:
            from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
            wrapper = PlaywrightDriverWrapperDirect(browser, page=None, capabilities=bstack1llll11ll_opy_, config=CONFIG)
            threading.current_thread().bstackSessionDriver = wrapper
            logger.debug(bstack1111l_opy_ (u"ࠤࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡊࡲࡪࡸࡨࡶ࡜ࡸࡡࡱࡲࡨࡶࡉ࡯ࡲࡦࡥࡷࠤࡸ࡫ࡴࡶࡲࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࠥ࡬࡯ࡳࠢࡷ࡬ࡷ࡫ࡡࡥࠢࠨࡷࠧ௧"), threading.get_ident())
            threading.current_thread().bstackTestErrorMessages = []
            if wrapper.session_id and not wrapper._cbt_info_sent:
                PlaywrightDriverWrapperDirect._send_cbt_info_on_session()
            try:
                from playwright.sync_api import Browser as bstack1111l11l1l_opy_
                if not hasattr(bstack1111l11l1l_opy_, bstack1111l_opy_ (u"ࠪࡣࡧࡹࡴࡢࡥ࡮ࡣࡳ࡫ࡷࡠࡲࡤ࡫ࡪࡥࡰࡢࡶࡦ࡬ࡪࡪࠧ௨")):
                    _1l1ll11l1l_opy_ = bstack1111l11l1l_opy_.new_page
                    def _11ll11l1l1_opy_(bstack1l1ll11ll_opy_, *bstack1111lll1ll_opy_, **bstack111ll1l1_opy_):
                        page = _1l1ll11l1l_opy_(bstack1l1ll11ll_opy_, *bstack1111lll1ll_opy_, **bstack111ll1l1_opy_)
                        try:
                            _w = getattr(threading.current_thread(), bstack1111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ௩"), None)
                            if _w and hasattr(_w, bstack1111l_opy_ (u"ࠬࡻࡰࡥࡣࡷࡩࡤࡶࡡࡨࡧࠪ௪")):
                                _w.update_page(page)
                        except Exception as exc:
                            logger.debug(bstack1111l_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡸࡴࡩࡧࡴࡦࠢࡳࡥ࡬࡫ࠠࡪࡰࠣࡻࡷࡧࡰࡱࡧࡵࠤ࠭ࡳ࡯ࡥࡡࡦࡳࡳࡴࡥࡤࡶࠬ࠾ࠥࠫࡳࠣ௫"), exc)
                        return page
                    bstack1111l11l1l_opy_.new_page = _11ll11l1l1_opy_
                    bstack1111l11l1l_opy_._bstack_new_page_patched = True
            except Exception as exc:
                logger.debug(bstack1111l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡺࡣࡩࠢࡖࡽࡳࡩࡂࡳࡱࡺࡷࡪࡸ࠮࡯ࡧࡺࡣࡵࡧࡧࡦࠢ࡬ࡲࠥࡳ࡯ࡥࡡࡦࡳࡳࡴࡥࡤࡶ࠽ࠤࠪࡹࠢ௬"), exc)
            try:
                from playwright.sync_api import Page as bstack11111111_opy_, Browser as _11l11ll111_opy_
                if not hasattr(bstack11111111_opy_, bstack1111l_opy_ (u"ࠨࡡࡥࡷࡹࡧࡣ࡬ࡡࡳࡥ࡬࡫࡟ࡤ࡮ࡲࡷࡪࡥࡰࡢࡶࡦ࡬ࡪࡪࠧ௭")):
                    _111111l11_opy_ = bstack11111111_opy_.close
                    def _1ll11ll11_opy_(bstack1ll1l11lll_opy_, *bstack111lllll1l_opy_, _bstack_sdk_close=False, **bstack111ll1l1ll_opy_):
                        if not _bstack_sdk_close:
                            logger.debug(bstack1111l_opy_ (u"ࠤࡇࡩ࡫࡫ࡲࡳࡧࡧࠤࡵࡧࡧࡦ࠰ࡦࡰࡴࡹࡥࠩࠫࠣ⠘ࠥࡽࡩ࡭࡮ࠣࡧࡱࡵࡳࡦࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨ௮"))
                            threading.current_thread().bstack_deferred_page_close = True
                            threading.current_thread().bstack_deferred_page_ref = bstack1ll1l11lll_opy_
                            return
                        return _111111l11_opy_(bstack1ll1l11lll_opy_, *bstack111lllll1l_opy_, **bstack111ll1l1ll_opy_)
                    bstack11111111_opy_.close = _1ll11ll11_opy_
                    bstack11111111_opy_._bstack_page_close_patched = True
                if not hasattr(_11l11ll111_opy_, bstack1111l_opy_ (u"ࠪࡣࡧࡹࡴࡢࡥ࡮ࡣࡧࡸ࡯ࡸࡵࡨࡶࡤࡩ࡬ࡰࡵࡨࡣࡵࡧࡴࡤࡪࡨࡨࠬ௯")):
                    _1llll11111_opy_ = _11l11ll111_opy_.close
                    def _11l1lll11l_opy_(bstack1l1ll11ll_opy_, *bstack111lll1ll1_opy_, _bstack_sdk_close=False, **bstack11l1111ll1_opy_):
                        if not _bstack_sdk_close:
                            logger.debug(bstack1111l_opy_ (u"ࠦࡉ࡫ࡦࡦࡴࡵࡩࡩࠦࡢࡳࡱࡺࡷࡪࡸ࠮ࡤ࡮ࡲࡷࡪ࠮ࠩࠡ⠖ࠣࡻ࡮ࡲ࡬ࠡࡥ࡯ࡳࡸ࡫ࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦ௰"))
                            threading.current_thread().bstack_deferred_browser_close = True
                            threading.current_thread().bstack_deferred_browser_ref = bstack1l1ll11ll_opy_
                            return
                        return _1llll11111_opy_(bstack1l1ll11ll_opy_, *bstack111lll1ll1_opy_, **bstack11l1111ll1_opy_)
                    _11l11ll111_opy_.close = _11l1lll11l_opy_
                    _11l11ll111_opy_._bstack_browser_close_patched = True
                if not hasattr(bstack11111111_opy_, bstack1111l_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡢࡴࡦࡺࡣࡩࡧࡧࠫ௱")):
                    _1ll1l1l11_opy_ = bstack11111111_opy_.screenshot
                    def _1111l1l11_opy_(bstack1ll1l11lll_opy_, *bstack1111lll11l_opy_, **bstack1l1ll11ll1_opy_):
                        result = _1ll1l1l11_opy_(bstack1ll1l11lll_opy_, *bstack1111lll11l_opy_, **bstack1l1ll11ll1_opy_)
                        try:
                            from bstack_utils.testhub_handler import TestHubHandler
                            from bstack_utils.bstack1lll1lll_opy_ import bstack11l11ll1l1_opy_
                            if bstack11l11ll1l1_opy_.on():
                                import base64
                                if isinstance(result, bytes):
                                    bstack1l1l1llll_opy_ = base64.b64encode(result).decode(bstack1111l_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬ௲"))
                                else:
                                    bstack1l1l1llll_opy_ = str(result)
                                test_uuid = TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack11l11ll1l1_opy_.current_hook_uuid()
                                if test_uuid and bstack1l1l1llll_opy_:
                                    TestHubHandler.bstack11l1lll1l1_opy_({
                                        bstack1111l_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭௳"): bstack1l1l1llll_opy_,
                                        bstack1111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ௴"): test_uuid
                                    })
                        except Exception as bstack1lll1l1lll_opy_:
                            logger.debug(bstack1111l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥ࡯ࡦࠣࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠤࡹࡵࠠࡐ࠳࠴ࡽࠥ࠮࡭ࡰࡦࡢࡧࡴࡴ࡮ࡦࡥࡷ࠭࠿ࠦࠥࡴࠤ௵"), bstack1lll1l1lll_opy_)
                        return result
                    bstack11111111_opy_.screenshot = _1111l1l11_opy_
                    bstack11111111_opy_._bstack_screenshot_patched = True
            except Exception as exc:
                logger.debug(bstack1111l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡦࠢࡧࡩ࡫࡫ࡲࡳࡧࡧࠤࡨࡲ࡯ࡴࡧࠣ࡬ࡴࡵ࡫ࡴࠢ࡬ࡲࠥࡳ࡯ࡥࡡࡦࡳࡳࡴࡥࡤࡶ࠽ࠤࠪࡹࠢ௶"), exc)
            logger.debug(bstack1111l_opy_ (u"ࠦࡑ࡫ࡧࡢࡥࡼࠤࡨࡵ࡮࡯ࡧࡦࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡴࡳࡣࡦ࡯࡮ࡴࡧࠡࡵࡨࡸࡺࡶࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࠢࡩࡳࡷࠦࡴࡩࡴࡨࡥࡩࠦࡻࡾࠤ௷").format(threading.get_ident()))
        except Exception as e:
            logger.debug(bstack1111l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠ࡭ࡧࡪࡥࡨࡿࠠࡤࡱࡱࡲࡪࡩࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡷࡶࡦࡩ࡫ࡪࡰࡪ࠾ࠥࢁࡽࠣ௸").format(str(e)))
    return browser
except Exception as e:
    pass
def patch_playwright():
    global SELENIUM_OR_PLAYWRIGHT_INSTALLED
    global FRAMEWORK_NAME
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack111l1ll11l_opy_
        global bstack1l1l1l1l1l_opy_
        if not bstack1l1l1l1l1l_opy_:
            bstack1l1l1l1l1l_opy_ = BrowserType.connect
        BrowserType.connect = bstack1ll1lll1l_opy_
        if bstack111l1ll11l_opy_():
            BrowserType.launch = bstack11ll111l1_opy_
            SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
        try:
            from playwright.sync_api._context_manager import PlaywrightContextManager
            if not hasattr(PlaywrightContextManager, bstack1111l_opy_ (u"࠭࡟ࡣࡵࡷࡥࡨࡱ࡟ࡦࡰࡷࡩࡷࡥࡰࡢࡶࡦ࡬ࡪࡪࠧ௹")):
                _1l1l1llll1_opy_ = PlaywrightContextManager.__enter__
                def _11ll111lll_opy_(bstack111lll1lll_opy_):
                    pw = _1l1l1llll1_opy_(bstack111lll1lll_opy_)
                    _11lll1111_opy_ = pw.stop
                    _1lll1ll11_opy_ = threading.current_thread()
                    _1lll1ll11_opy_.bstack_deferred_pw_ref = pw
                    _1lll1ll11_opy_.bstack_deferred_pw_stop_fn = _11lll1111_opy_
                    def _1ll11l1lll_opy_(*args, _bstack_sdk_close=False, **kwargs):
                        if not _bstack_sdk_close:
                            logger.debug(bstack1111l_opy_ (u"ࠢࡅࡧࡩࡩࡷࡸࡥࡥࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠴ࡳࡵࡱࡳࠬ࠮ࠦ⠔ࠡࡹ࡬ࡰࡱࠦࡳࡵࡱࡳࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣ௺"))
                            threading.current_thread().bstack_deferred_pw_stop = True
                            return
                        return _11lll1111_opy_()
                    pw.stop = _1ll11l1lll_opy_
                    return pw
                PlaywrightContextManager.__enter__ = _11ll111lll_opy_
                PlaywrightContextManager._bstack_enter_patched = True
        except Exception as e:
            logger.debug(bstack1111l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡴࡤࡪࠣࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࡃࡰࡰࡷࡩࡽࡺࡍࡢࡰࡤ࡫ࡪࡸ࠮ࡠࡡࡨࡲࡹ࡫ࡲࡠࡡ࠽ࠤࠪࡹࠢ௻"), e)
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1ll11ll1l_opy_
      SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
    except Exception as e:
      pass
def playwright_set_session_name(context, bstack1ll11lll_opy_):
  try:
    if getattr(context, bstack1111l_opy_ (u"ࠩࡳࡥ࡬࡫ࠧ௼"), None):
      context.page.evaluate(bstack1111l_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦ௽"), bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠨ௾")+ json.dumps(bstack1ll11lll_opy_) + bstack1111l_opy_ (u"ࠧࢃࡽࠣ௿"))
  except Exception as e:
    logger.debug(bstack1111l_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡽࢀ࠾ࠥࢁࡽࠣఀ").format(str(e), traceback.format_exc()))
def playwright_annotate(context, message, level):
  try:
    if getattr(context, bstack1111l_opy_ (u"ࠧࡱࡣࡪࡩࠬఁ"), None):
      context.page.evaluate(bstack1111l_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤం"), bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧః") + json.dumps(message) + bstack1111l_opy_ (u"ࠪ࠰ࠧࡲࡥࡷࡧ࡯ࠦ࠿࠭ఄ") + json.dumps(level) + bstack1111l_opy_ (u"ࠫࢂࢃࠧఅ"))
  except Exception as e:
    logger.debug(bstack1111l_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡣࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠥࢁࡽ࠻ࠢࡾࢁࠧఆ").format(str(e), traceback.format_exc()))
@measure(event_name=EVENTS.bstack1111ll1ll1_opy_, stage=STAGE.bstack11lll111l_opy_, bstack11lll111_opy_=SESSION_NAME)
def bstack11ll1ll1_opy_(self, url):
  global bstack11l11lll1_opy_
  try:
    bstack1l11ll111l_opy_(url)
  except Exception as err:
    logger.debug(bstack1l1111l111_opy_.format(str(err)))
  try:
    bstack11l11lll1_opy_(self, url)
  except Exception as e:
    try:
      parsed_error = str(e)
      if any(err_msg in parsed_error for err_msg in bstack11lll1l1l1_opy_):
        bstack1l11ll111l_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1l1111l111_opy_.format(str(err)))
    raise e
def bstack1lll1lll1_opy_(self):
  global bstack1l1l1ll1l_opy_
  bstack1l1l1ll1l_opy_ = self
  return
def bstack1ll1l1llll_opy_(self):
  global bstack1l1111ll11_opy_
  bstack1l1111ll11_opy_ = self
  return
def bstack11111llll_opy_(test_name, bstack1l11ll1lll_opy_):
  global CONFIG
  if percy.bstack1l11111l1l_opy_() == bstack1111l_opy_ (u"ࠨࡴࡳࡷࡨࠦఇ"):
    bstack1l1111111_opy_ = os.path.relpath(bstack1l11ll1lll_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack1l1111111_opy_)
    bstack11lll111_opy_ = suite_name + bstack1111l_opy_ (u"ࠢ࠮ࠤఈ") + test_name
    threading.current_thread().percySessionName = bstack11lll111_opy_
def bstack11l111l1_opy_(self, test, *args, **kwargs):
  global bstack1ll11l1l1l_opy_
  test_name = None
  bstack1l11ll1lll_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1l11ll1lll_opy_ = str(test.source)
  bstack11111llll_opy_(test_name, bstack1l11ll1lll_opy_)
  bstack1ll11l1l1l_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.bstack1llllll1l1_opy_, stage=STAGE.bstack11lll111l_opy_, bstack11lll111_opy_=SESSION_NAME)
def bstack11l111l111_opy_(driver, bstack11lll111_opy_):
  if not bstack1111ll111_opy_ and bstack11lll111_opy_:
      bstack111l111111_opy_ = {
          bstack1111l_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨఉ"): bstack1111l_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪఊ"),
          bstack1111l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ఋ"): {
              bstack1111l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩఌ"): bstack11lll111_opy_
          }
      }
      bstack111l1l1ll_opy_ = bstack1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪ఍").format(json.dumps(bstack111l111111_opy_))
      driver.execute_script(bstack111l1l1ll_opy_)
  if bstack111ll1ll11_opy_:
      bstack1l11l1l1ll_opy_ = {
          bstack1111l_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭ఎ"): bstack1111l_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩఏ"),
          bstack1111l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫఐ"): {
              bstack1111l_opy_ (u"ࠩࡧࡥࡹࡧࠧ఑"): bstack11lll111_opy_ + bstack1111l_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬఒ"),
              bstack1111l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪఓ"): bstack1111l_opy_ (u"ࠬ࡯࡮ࡧࡱࠪఔ")
          }
      }
      if bstack111ll1ll11_opy_.status == bstack1111l_opy_ (u"࠭ࡐࡂࡕࡖࠫక"):
          bstack1l1lll1111_opy_ = bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬఖ").format(json.dumps(bstack1l11l1l1ll_opy_))
          driver.execute_script(bstack1l1lll1111_opy_)
          bstack1ll1111l1l_opy_(driver, bstack1111l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨగ"))
      elif bstack111ll1ll11_opy_.status == bstack1111l_opy_ (u"ࠩࡉࡅࡎࡒࠧఘ"):
          reason = bstack1111l_opy_ (u"ࠥࠦఙ")
          bstack1ll1lll1_opy_ = bstack11lll111_opy_ + bstack1111l_opy_ (u"ࠫࠥ࡬ࡡࡪ࡮ࡨࡨࠬచ")
          if bstack111ll1ll11_opy_.message:
              reason = str(bstack111ll1ll11_opy_.message)
              bstack1ll1lll1_opy_ = bstack1ll1lll1_opy_ + bstack1111l_opy_ (u"ࠬࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴ࠽ࠤࠬఛ") + reason
          bstack1l11l1l1ll_opy_[bstack1111l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩజ")] = {
              bstack1111l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ఝ"): bstack1111l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧఞ"),
              bstack1111l_opy_ (u"ࠩࡧࡥࡹࡧࠧట"): bstack1ll1lll1_opy_
          }
          bstack1l1lll1111_opy_ = bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨఠ").format(json.dumps(bstack1l11l1l1ll_opy_))
          driver.execute_script(bstack1l1lll1111_opy_)
          bstack1ll1111l1l_opy_(driver, bstack1111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫడ"), reason)
          bstack1111ll1ll_opy_(reason, str(bstack111ll1ll11_opy_), str(PLATFORM_INDEX), logger)
@measure(event_name=EVENTS.bstack111ll1111l_opy_, stage=STAGE.bstack11lll111l_opy_, bstack11lll111_opy_=SESSION_NAME)
def bstack111l1l1l1l_opy_(driver, test):
  if percy.bstack1l11111l1l_opy_() == bstack1111l_opy_ (u"ࠧࡺࡲࡶࡧࠥఢ") and percy.bstack11l11l11_opy_() == bstack1111l_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣణ"):
      bstack1111ll1l_opy_ = bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪత"), None)
      bstack1ll1111ll_opy_(driver, bstack1111ll1l_opy_, test)
  if (bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬథ"), None) and
      bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨద"), None)) or (
      bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪధ"), None) and
      bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭న"), None)):
      logger.info(bstack1111l_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠣࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡷࡱࡨࡪࡸࡷࡢࡻ࠱ࠤࠧ఩"))
      a11y.bstack1l1l1ll11_opy_(driver, name=test.name, path=test.source)
def bstack1l11l111l1_opy_(test, bstack11lll111_opy_):
    try:
      bstack1lll1l11l_opy_ = datetime.datetime.now()
      data = {}
      if test:
        data[bstack1111l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫప")] = bstack11lll111_opy_
      if bstack111ll1ll11_opy_:
        if bstack111ll1ll11_opy_.status == bstack1111l_opy_ (u"ࠧࡑࡃࡖࡗࠬఫ"):
          data[bstack1111l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨబ")] = bstack1111l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩభ")
        elif bstack111ll1ll11_opy_.status == bstack1111l_opy_ (u"ࠪࡊࡆࡏࡌࠨమ"):
          data[bstack1111l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫయ")] = bstack1111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬర")
          if bstack111ll1ll11_opy_.message:
            data[bstack1111l_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ఱ")] = str(bstack111ll1ll11_opy_.message)
      user = CONFIG[bstack1111l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩల")]
      key = CONFIG[bstack1111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫళ")]
      host = bstack111l1lll1_opy_(cli.config, [bstack1111l_opy_ (u"ࠤࡤࡴ࡮ࡹࠢఴ"), bstack1111l_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷࡩࠧవ"), bstack1111l_opy_ (u"ࠦࡦࡶࡩࠣశ")], bstack1111l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡱ࡫࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࠨష"))
      url = bstack1111l_opy_ (u"࠭ࡻࡾ࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡸ࡫ࡳࡴ࡫ࡲࡲࡸ࠵ࡻࡾ࠰࡭ࡷࡴࡴࠧస").format(host, bstack1lll11111_opy_)
      headers = {
        bstack1111l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭హ"): bstack1111l_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ఺"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers, auth=(user, key))
        cli.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺ࡶࡲࡧࡥࡹ࡫࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡳࡵࡣࡷࡹࡸࠨ఻"), datetime.datetime.now() - bstack1lll1l11l_opy_)
    except Exception as e:
      logger.error(bstack11111lll_opy_.format(str(e)))
def bstack111l1111l_opy_(test, bstack11lll111_opy_):
  global CONFIG
  global bstack1l1111ll11_opy_
  global bstack1l1l1ll1l_opy_
  global bstack1lll11111_opy_
  global bstack111ll1ll11_opy_
  global SESSION_NAME
  global bstack1l111l1ll_opy_
  global bstack11llll1ll_opy_
  global bstack1llll111l_opy_
  global bstack1l1ll1ll11_opy_
  global bstack1l1lll1ll_opy_
  global bstack111l1l111_opy_
  global bstack11ll11ll1_opy_
  try:
    if not bstack1lll11111_opy_:
      with bstack11ll11ll1_opy_:
        bstack1llll1l1l1_opy_ = os.path.join(os.path.expanduser(bstack1111l_opy_ (u"ࠪࢂ఼ࠬ")), bstack1111l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫఽ"), bstack1111l_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧా"))
        if os.path.exists(bstack1llll1l1l1_opy_):
          with open(bstack1llll1l1l1_opy_, bstack1111l_opy_ (u"࠭ࡲࠨి")) as f:
            content = f.read().strip()
            if content:
              bstack1l1ll1l1_opy_ = json.loads(bstack1111l_opy_ (u"ࠢࡼࠤీ") + content + bstack1111l_opy_ (u"ࠨࠤࡻࠦ࠿ࠦࠢࡺࠤࠪు") + bstack1111l_opy_ (u"ࠤࢀࠦూ"))
              bstack1lll11111_opy_ = bstack1l1ll1l1_opy_.get(str(threading.get_ident()))
  except Exception as e:
    logger.debug(bstack1111l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡵࡩࡦࡪࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡎࡊࡳࠡࡨ࡬ࡰࡪࡀࠠࠨృ") + str(e))
  if not is_robot_playwright_installed():
    if bstack1l1lll1ll_opy_:
      with bstack11ll11l1l_opy_:
        bstack11lll1111l_opy_ = bstack1l1lll1ll_opy_.copy()
      for driver in bstack11lll1111l_opy_:
        if bstack1lll11111_opy_ == driver.session_id:
          if test:
            bstack111l1l1l1l_opy_(driver, test)
          bstack11l111l111_opy_(driver, bstack11lll111_opy_)
    elif bstack1lll11111_opy_:
      bstack1l11l111l1_opy_(test, bstack11lll111_opy_)
    if bstack1l1111ll11_opy_:
      bstack11llll1ll_opy_(bstack1l1111ll11_opy_)
    if bstack1l1l1ll1l_opy_:
      bstack1llll111l_opy_(bstack1l1l1ll1l_opy_)
    if bstack1l11l1ll1_opy_:
      bstack1l1ll1ll11_opy_()
def bstack11lll11ll_opy_(self, test, *args, **kwargs):
  bstack11lll111_opy_ = None
  if test:
    bstack11lll111_opy_ = str(test.name)
  bstack111l1111l_opy_(test, bstack11lll111_opy_)
  bstack1l111l1ll_opy_(self, test, *args, **kwargs)
def bstack1111ll1l11_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1lllllll1_opy_
  global CONFIG
  global bstack1l1lll1ll_opy_
  global bstack1lll11111_opy_
  global bstack11ll11ll1_opy_
  bstack1lll1lllll_opy_ = None
  try:
    if bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪౄ"), None) or bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ౅"), None):
      try:
        if not bstack1lll11111_opy_:
          bstack1llll1l1l1_opy_ = os.path.join(os.path.expanduser(bstack1111l_opy_ (u"࠭ࡾࠨె")), bstack1111l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧే"), bstack1111l_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪై"))
          with bstack11ll11ll1_opy_:
            if os.path.exists(bstack1llll1l1l1_opy_):
              with open(bstack1llll1l1l1_opy_, bstack1111l_opy_ (u"ࠩࡵࠫ౉")) as f:
                content = f.read().strip()
                if content:
                  bstack1l1ll1l1_opy_ = json.loads(bstack1111l_opy_ (u"ࠥࡿࠧొ") + content + bstack1111l_opy_ (u"ࠫࠧࡾࠢ࠻ࠢࠥࡽࠧ࠭ో") + bstack1111l_opy_ (u"ࠧࢃࠢౌ"))
                  bstack1lll11111_opy_ = bstack1l1ll1l1_opy_.get(str(threading.get_ident()))
      except Exception as e:
        logger.debug(bstack1111l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡸࡥࡢࡦ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡊࡆࡶࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥࡺࡥࡴࡶࠣࡷࡹࡧࡴࡶࡵ࠽ࠤ్ࠬ") + str(e))
      if bstack1l1lll1ll_opy_:
        with bstack11ll11l1l_opy_:
          bstack11lll1111l_opy_ = bstack1l1lll1ll_opy_.copy()
        for driver in bstack11lll1111l_opy_:
          if bstack1lll11111_opy_ == driver.session_id:
            bstack1lll1lllll_opy_ = driver
    bstack1lllll1l1_opy_ = a11y.is_enabled_testcase(test.tags)
    if bstack1lll1lllll_opy_:
      threading.current_thread().isA11yTest = a11y.start_test_capture(bstack1lll1lllll_opy_, bstack1lllll1l1_opy_)
      threading.current_thread().isAppA11yTest = a11y.start_test_capture(bstack1lll1lllll_opy_, bstack1lllll1l1_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1lllll1l1_opy_
      threading.current_thread().isAppA11yTest = bstack1lllll1l1_opy_
  except:
    pass
  bstack1lllllll1_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack111ll1ll11_opy_
  try:
    bstack111ll1ll11_opy_ = self._test
  except:
    bstack111ll1ll11_opy_ = self.test
def bstack1ll1l11111_opy_():
  global bstack111llll11_opy_
  try:
    if os.path.exists(bstack111llll11_opy_):
      os.remove(bstack111llll11_opy_)
  except Exception as e:
    logger.debug(bstack1111l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪ౎") + str(e))
def bstack1l1111ll1_opy_():
  global bstack111llll11_opy_
  bstack1l1lll1ll1_opy_ = {}
  lock_file = bstack111llll11_opy_ + bstack1111l_opy_ (u"ࠨ࠰࡯ࡳࡨࡱࠧ౏")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1111l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡬ࡰࡥ࡮ࠤࡳࡵࡴࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨ࠰ࠥࡻࡳࡪࡰࡪࠤࡧࡧࡳࡪࡥࠣࡪ࡮ࡲࡥࠡࡱࡳࡩࡷࡧࡴࡪࡱࡱࡷࠬ౐"))
    try:
      if not os.path.isfile(bstack111llll11_opy_):
        with open(bstack111llll11_opy_, bstack1111l_opy_ (u"ࠪࡻࠬ౑")) as f:
          json.dump({}, f)
      if os.path.exists(bstack111llll11_opy_):
        with open(bstack111llll11_opy_, bstack1111l_opy_ (u"ࠫࡷ࠭౒")) as f:
          content = f.read().strip()
          if content:
            bstack1l1lll1ll1_opy_ = json.loads(content)
    except Exception as e:
      logger.debug(bstack1111l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡳࡧࡤࡨ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧ౓") + str(e))
    return bstack1l1lll1ll1_opy_
  try:
    os.makedirs(os.path.dirname(bstack111llll11_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      if not os.path.isfile(bstack111llll11_opy_):
        with open(bstack111llll11_opy_, bstack1111l_opy_ (u"࠭ࡷࠨ౔")) as f:
          json.dump({}, f)
      if os.path.exists(bstack111llll11_opy_):
        with open(bstack111llll11_opy_, bstack1111l_opy_ (u"ࠧࡳౕࠩ")) as f:
          content = f.read().strip()
          if content:
            bstack1l1lll1ll1_opy_ = json.loads(content)
  except Exception as e:
    logger.debug(bstack1111l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡶࡪࡧࡤࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ౖࠢࠪ") + str(e))
  finally:
    return bstack1l1lll1ll1_opy_
def bstack11lll1ll1_opy_(platform_index, item_index):
  global bstack111llll11_opy_
  lock_file = bstack111llll11_opy_ + bstack1111l_opy_ (u"ࠩ࠱ࡰࡴࡩ࡫ࠨ౗")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1111l_opy_ (u"ࠪࡪ࡮ࡲࡥ࡭ࡱࡦ࡯ࠥࡴ࡯ࡵࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩ࠱ࠦࡵࡴ࡫ࡱ࡫ࠥࡨࡡࡴ࡫ࡦࠤ࡫࡯࡬ࡦࠢࡲࡴࡪࡸࡡࡵ࡫ࡲࡲࡸ࠭ౘ"))
    try:
      bstack1l1lll1ll1_opy_ = {}
      if os.path.exists(bstack111llll11_opy_):
        with open(bstack111llll11_opy_, bstack1111l_opy_ (u"ࠫࡷ࠭ౙ")) as f:
          content = f.read().strip()
          if content:
            bstack1l1lll1ll1_opy_ = json.loads(content)
      bstack1l1lll1ll1_opy_[item_index] = platform_index
      with open(bstack111llll11_opy_, bstack1111l_opy_ (u"ࠧࡽࠢౚ")) as outfile:
        json.dump(bstack1l1lll1ll1_opy_, outfile)
    except Exception as e:
      logger.debug(bstack1111l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡹࡵ࡭ࡹ࡯࡮ࡨࠢࡷࡳࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫ౛") + str(e))
    return
  try:
    os.makedirs(os.path.dirname(bstack111llll11_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      bstack1l1lll1ll1_opy_ = {}
      if os.path.exists(bstack111llll11_opy_):
        with open(bstack111llll11_opy_, bstack1111l_opy_ (u"ࠧࡳࠩ౜")) as f:
          content = f.read().strip()
          if content:
            bstack1l1lll1ll1_opy_ = json.loads(content)
      bstack1l1lll1ll1_opy_[item_index] = platform_index
      with open(bstack111llll11_opy_, bstack1111l_opy_ (u"ࠣࡹࠥౝ")) as outfile:
        json.dump(bstack1l1lll1ll1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1111l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡼࡸࡩࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧ౞") + str(e))
def bstack1ll1l1lll1_opy_(bstack111llll111_opy_):
  global CONFIG
  bstack11l11lll_opy_ = bstack1111l_opy_ (u"ࠪࠫ౟")
  if not bstack1111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧౠ") in CONFIG:
    logger.info(bstack1111l_opy_ (u"ࠬࡔ࡯ࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠤࡵࡧࡳࡴࡧࡧࠤࡺࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡨࡧࡱࡩࡷࡧࡴࡦࠢࡵࡩࡵࡵࡲࡵࠢࡩࡳࡷࠦࡒࡰࡤࡲࡸࠥࡸࡵ࡯ࠩౡ"))
  try:
    platform = CONFIG[bstack1111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩౢ")][bstack111llll111_opy_]
    if bstack1111l_opy_ (u"ࠧࡰࡵࠪౣ") in platform:
      bstack11l11lll_opy_ += str(platform[bstack1111l_opy_ (u"ࠨࡱࡶࠫ౤")]) + bstack1111l_opy_ (u"ࠩ࠯ࠤࠬ౥")
    if bstack1111l_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭౦") in platform:
      bstack11l11lll_opy_ += str(platform[bstack1111l_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧ౧")]) + bstack1111l_opy_ (u"ࠬ࠲ࠠࠨ౨")
    if bstack1111l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪ౩") in platform:
      bstack11l11lll_opy_ += str(platform[bstack1111l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ౪")]) + bstack1111l_opy_ (u"ࠨ࠮ࠣࠫ౫")
    if bstack1111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ౬") in platform:
      bstack11l11lll_opy_ += str(platform[bstack1111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬ౭")]) + bstack1111l_opy_ (u"ࠫ࠱ࠦࠧ౮")
    if bstack1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ౯") in platform:
      bstack11l11lll_opy_ += str(platform[bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ౰")]) + bstack1111l_opy_ (u"ࠧ࠭ࠢࠪ౱")
    if bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ౲") in platform:
      bstack11l11lll_opy_ += str(platform[bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ౳")]) + bstack1111l_opy_ (u"ࠪ࠰ࠥ࠭౴")
  except Exception as e:
    logger.debug(bstack1111l_opy_ (u"ࠫࡘࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡴࡧࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡷࡹࡸࡩ࡯ࡩࠣࡪࡴࡸࠠࡳࡧࡳࡳࡷࡺࠠࡨࡧࡱࡩࡷࡧࡴࡪࡱࡱࠫ౵") + str(e))
  finally:
    if bstack11l11lll_opy_[len(bstack11l11lll_opy_) - 2:] == bstack1111l_opy_ (u"ࠬ࠲ࠠࠨ౶"):
      bstack11l11lll_opy_ = bstack11l11lll_opy_[:-2]
    return bstack11l11lll_opy_
def bstack1l1l1lllll_opy_(path, bstack11l11lll_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack11lll1l111_opy_ = ET.parse(path)
    bstack1111ll1111_opy_ = bstack11lll1l111_opy_.getroot()
    bstack1l11lll11_opy_ = None
    for suite in bstack1111ll1111_opy_.iter(bstack1111l_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬ౷")):
      if bstack1111l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ౸") in suite.attrib:
        suite.attrib[bstack1111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭౹")] += bstack1111l_opy_ (u"ࠩࠣࠫ౺") + bstack11l11lll_opy_
        bstack1l11lll11_opy_ = suite
    bstack1ll1ll111_opy_ = None
    for robot in bstack1111ll1111_opy_.iter(bstack1111l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ౻")):
      bstack1ll1ll111_opy_ = robot
    bstack1l11111lll_opy_ = len(bstack1ll1ll111_opy_.findall(bstack1111l_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪ౼")))
    if bstack1l11111lll_opy_ == 1:
      bstack1ll1ll111_opy_.remove(bstack1ll1ll111_opy_.findall(bstack1111l_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫ౽"))[0])
      bstack11ll11111_opy_ = ET.Element(bstack1111l_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬ౾"), attrib={bstack1111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ౿"): bstack1111l_opy_ (u"ࠨࡕࡸ࡭ࡹ࡫ࡳࠨಀ"), bstack1111l_opy_ (u"ࠩ࡬ࡨࠬಁ"): bstack1111l_opy_ (u"ࠪࡷ࠵࠭ಂ")})
      bstack1ll1ll111_opy_.insert(1, bstack11ll11111_opy_)
      bstack1l1l1lll11_opy_ = None
      for suite in bstack1ll1ll111_opy_.iter(bstack1111l_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪಃ")):
        bstack1l1l1lll11_opy_ = suite
      bstack1l1l1lll11_opy_.append(bstack1l11lll11_opy_)
      bstack11l1ll1l_opy_ = None
      for status in bstack1l11lll11_opy_.iter(bstack1111l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ಄")):
        bstack11l1ll1l_opy_ = status
      bstack1l1l1lll11_opy_.append(bstack11l1ll1l_opy_)
    bstack11lll1l111_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1111l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡶࡸ࡯࡮ࡨࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡱ࡫ࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠫಅ") + str(e))
def bstack1ll11111l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack111l11ll11_opy_
  global CONFIG
  if bstack1111l_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡰࡢࡶ࡫ࠦಆ") in options:
    del options[bstack1111l_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡱࡣࡷ࡬ࠧಇ")]
  json_data = bstack1l1111ll1_opy_()
  for item_id in json_data.keys():
    path = os.path.join(outs_dir, str(item_id), bstack1111l_opy_ (u"ࠩࡲࡹࡹࡶࡵࡵ࠰ࡻࡱࡱ࠭ಈ"))
    bstack1l1l1lllll_opy_(path, bstack1ll1l1lll1_opy_(json_data[item_id]))
  bstack1ll1l11111_opy_()
  return bstack111l11ll11_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1lll1l1ll1_opy_(self, ff_profile_dir):
  global bstack1l1ll1111_opy_
  if not ff_profile_dir:
    return None
  return bstack1l1ll1111_opy_(self, ff_profile_dir)
def bstack11lllll1l_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1l1l111ll_opy_
  bstack111lll11_opy_ = []
  if bstack1111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ಉ") in CONFIG:
    bstack111lll11_opy_ = CONFIG[bstack1111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧಊ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1111l_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࠨಋ")],
      pabot_args[bstack1111l_opy_ (u"ࠨࡶࡦࡴࡥࡳࡸ࡫ࠢಌ")],
      argfile,
      pabot_args.get(bstack1111l_opy_ (u"ࠢࡩ࡫ࡹࡩࠧ಍")),
      pabot_args[bstack1111l_opy_ (u"ࠣࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠦಎ")],
      platform[0],
      bstack1l1l111ll_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1111l_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡪ࡮ࡲࡥࡴࠤಏ")] or [(bstack1111l_opy_ (u"ࠥࠦಐ"), None)]
    for platform in enumerate(bstack111lll11_opy_)
  ]
def bstack1l1l111l1_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1l1ll1ll1_opy_=bstack1111l_opy_ (u"ࠫࠬ಑")):
  global bstack1ll1l11ll1_opy_
  self.platform_index = platform_index
  self.bstack11l1lllll1_opy_ = bstack1l1ll1ll1_opy_
  bstack1ll1l11ll1_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1l1ll11lll_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1111111l_opy_
  global bstack111ll111l1_opy_
  bstack11l1l1l1ll_opy_ = copy.deepcopy(item)
  if not bstack1111l_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧಒ") in item.options:
    bstack11l1l1l1ll_opy_.options[bstack1111l_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨಓ")] = []
  bstack1111llll1_opy_ = bstack11l1l1l1ll_opy_.options[bstack1111l_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩಔ")].copy()
  for v in bstack11l1l1l1ll_opy_.options[bstack1111l_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪಕ")]:
    if bstack1111l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘࠨಖ") in v:
      bstack1111llll1_opy_.remove(v)
    if bstack1111l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡆࡐࡎࡇࡒࡈࡕࠪಗ") in v:
      bstack1111llll1_opy_.remove(v)
    if bstack1111l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨಘ") in v:
      bstack1111llll1_opy_.remove(v)
  bstack1111llll1_opy_.insert(0, bstack1111l_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡕࡒࡁࡕࡈࡒࡖࡒࡏࡎࡅࡇ࡛࠾ࢀࢃࠧಙ").format(bstack11l1l1l1ll_opy_.platform_index))
  bstack1111llll1_opy_.insert(0, bstack1111l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔ࠽ࡿࢂ࠭ಚ").format(bstack11l1l1l1ll_opy_.bstack11l1lllll1_opy_))
  bstack11l1l1l1ll_opy_.options[bstack1111l_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩಛ")] = bstack1111llll1_opy_
  if bstack111ll111l1_opy_:
    bstack11l1l1l1ll_opy_.options[bstack1111l_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪಜ")].insert(0, bstack1111l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡅࡏࡍࡆࡘࡇࡔ࠼ࡾࢁࠬಝ").format(bstack111ll111l1_opy_))
  return bstack1111111l_opy_(caller_id, datasources, is_last, bstack11l1l1l1ll_opy_, outs_dir)
def bstack11l11lll1l_opy_(command, item_index):
  try:
    if global_config.get_property(bstack1111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫಞ")):
      os.environ[bstack1111l_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬಟ")] = json.dumps(CONFIG[bstack1111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨಠ")][item_index % bstack11l1llll11_opy_])
    global bstack111ll111l1_opy_
    os.environ[bstack1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ಡ")] = str(item_index % bstack11l1llll11_opy_)
    listener_arg = bstack1111l_opy_ (u"ࠧࠨಢ")
    if is_robot_playwright_installed() and cli.is_enabled(CONFIG):
      listener_arg = bstack1111l_opy_ (u"ࠨࠢ࠰࠱ࡱ࡯ࡳࡵࡧࡱࡩࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡹࡤ࡬࠰ࡵࡳࡧࡵࡴࡠ࡮࡬ࡷࡹ࡫࡮ࡦࡴࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠮ࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡔࡦࡺࡣࡩࡧࡵࠫಣ")
      logger.debug(bstack1111l_opy_ (u"ࠤࡄࡨࡩ࡯࡮ࡨࠢࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡖࡡࡵࡥ࡫ࡩࡷࠦ࡬ࡪࡵࡷࡩࡳ࡫ࡲࠡࡨࡲࡶࠥ࡯ࡴࡦ࡯ࠣࡿࢂࠨತ").format(item_index))
    bstack11llll11l1_opy_ = bstack1111l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡶࡨࡰࠦࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠠ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࠣࠦಥ") + \
              str(item_index % bstack11l1llll11_opy_) + \
              bstack1111l_opy_ (u"ࠦࠥ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠤࠧದ") + \
              str(item_index) + \
              listener_arg
    if bstack111ll111l1_opy_:
        bstack11llll11l1_opy_ += bstack1111l_opy_ (u"ࠧࠦࠢಧ") + bstack111ll111l1_opy_
    command[0:1] = bstack11llll11l1_opy_.split()
  except Exception as e:
    logger.error(bstack1111l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡳ࡯ࡥ࡫ࡩࡽ࡮ࡴࡧࠡࡥࡲࡱࡲࡧ࡮ࡥࠢࡩࡳࡷࠦࡰࡢࡤࡲࡸࠥࡸࡵ࡯࠼ࠣࡿࢂ࠭ನ").format(str(e)))
def bstack1l1l111111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1111ll1l1l_opy_
  try:
    bstack11l11lll1l_opy_(command, item_index)
    return bstack1111ll1l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
  except Exception as e:
    logger.error(bstack1111l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡧࡵࡴࠡࡴࡸࡲ࠿ࠦࡻࡾࠩ಩").format(str(e)))
    raise e
def bstack1l1l1l1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1111ll1l1l_opy_
  try:
    bstack11l11lll1l_opy_(command, item_index)
    return bstack1111ll1l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
  except Exception as e:
    logger.error(bstack1111l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡦࡨ࡯ࡵࠢࡵࡹࡳࠦ࠲࠯࠳࠶࠾ࠥࢁࡽࠨಪ").format(str(e)))
    try:
      return bstack1111ll1l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
    except Exception as e2:
      logger.error(bstack1111l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡢࡰࡶࠣ࠶࠳࠷࠳ࠡࡨࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࢀࢃࠧಫ").format(str(e2)))
      raise e
def bstack1ll11l111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1111ll1l1l_opy_
  try:
    bstack11l11lll1l_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    return bstack1111ll1l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
  except Exception as e:
    logger.error(bstack1111l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡣࡱࡷࠤࡷࡻ࡮ࠡ࠴࠱࠵࠺ࡀࠠࡼࡿࠪಬ").format(str(e)))
    try:
      return bstack1111ll1l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
    except Exception as e2:
      logger.error(bstack1111l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡢࡤࡲࡸࠥ࠸࠮࠲࠷ࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࡻࡾࠩಭ").format(str(e2)))
      raise e
def _111lll11l1_opy_(bstack1l1l11ll1l_opy_, item_index, process_timeout, sleep_before_start, bstack11l1lll111_opy_):
  bstack11l11lll1l_opy_(bstack1l1l11ll1l_opy_, item_index)
  if process_timeout is None:
    process_timeout = 3600
  if sleep_before_start and sleep_before_start > 0:
    time.sleep(min(sleep_before_start, 5))
  return process_timeout
def bstack1lll1l1l1l_opy_(command, bstack11llll1lll_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack1111ll1l1l_opy_
  global bstack1lll1lll11_opy_
  global bstack111ll111l1_opy_
  try:
    for env_name, bstack11l1l11l1_opy_ in bstack1lll1lll11_opy_.items():
      os.environ[env_name] = bstack11l1l11l1_opy_
    bstack111ll111l1_opy_ = bstack1111l_opy_ (u"ࠧࠨಮ")
    bstack11l11lll1l_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    if sleep_before_start and sleep_before_start > 0:
      time.sleep(min(sleep_before_start, 5))
    return bstack1111ll1l1l_opy_(command, bstack11llll1lll_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack1111l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠࡳࡷࡱࠤ࠺࠴࠰࠻ࠢࡾࢁࠬಯ").format(str(e)))
    try:
      return bstack1111ll1l1l_opy_(command, bstack11llll1lll_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack1111l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡧࡵࡴࠡࡨࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࢀࢃࠧರ").format(str(e2)))
      raise e
def bstack1111l1l111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack1111ll1l1l_opy_
  try:
    process_timeout = _111lll11l1_opy_(command, item_index, process_timeout, sleep_before_start, bstack1111l_opy_ (u"ࠨ࠶࠱࠶ࠬಱ"))
    return bstack1111ll1l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack1111l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡢࡰࡶࠣࡶࡺࡴࠠ࠵࠰࠵࠾ࠥࢁࡽࠨಲ").format(str(e)))
    try:
      return bstack1111ll1l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack1111l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡣࡱࡷࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࡼࡿࠪಳ").format(str(e2)))
      raise e
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack11l1ll1l1l_opy_(self, runner, quiet=False, capture=True):
  global bstack1l1l111ll1_opy_
  bstack1l1111l11_opy_ = bstack1l1l111ll1_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack1111l_opy_ (u"ࠫࡪࡾࡣࡦࡲࡷ࡭ࡴࡴ࡟ࡢࡴࡵࠫ಴")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1111l_opy_ (u"ࠬ࡫ࡸࡤࡡࡷࡶࡦࡩࡥࡣࡣࡦ࡯ࡤࡧࡲࡳࠩವ")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1l1111l11_opy_
def bstack1l11111ll1_opy_(runner, hook_name, context, element, bstack1llll1l1l_opy_, *args):
  global bstack11ll1lll_opy_
  try:
    if runner.hooks.get(hook_name):
      bstack1l1l1ll1_opy_.bstack11l111l1l_opy_(hook_name, element)
    if bstack11ll1lll_opy_ is None or bstack11ll1lll_opy_:
      bstack1llll1l1l_opy_(runner, hook_name, context, *args)
    else:
      bstack11ll1l1111_opy_ = (context,) + args
      bstack1llll1l1l_opy_(runner, hook_name, *bstack11ll1l1111_opy_)
    if runner.hooks.get(hook_name):
      bstack1l1l1ll1_opy_.bstack1ll11lllll_opy_(element)
      if hook_name not in [bstack1111l_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠪಶ"), bstack1111l_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪಷ")] and args and hasattr(args[0], bstack1111l_opy_ (u"ࠨࡧࡵࡶࡴࡸ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠨಸ")):
        args[0].error_message = bstack1111l_opy_ (u"ࠩࠪಹ")
  except Exception as e:
    logger.debug(bstack1111l_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡨࡢࡰࡧࡰࡪࠦࡨࡰࡱ࡮ࡷࠥ࡯࡮ࠡࡤࡨ࡬ࡦࡼࡥ࠻ࠢࡾࢁࠬ಺").format(str(e)))
@measure(event_name=EVENTS.bstack1l11ll1l1l_opy_, stage=STAGE.bstack11lll111l_opy_, hook_type=bstack1111l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡅࡱࡲࠢ಻"), bstack11lll111_opy_=SESSION_NAME)
def bstack1ll1ll1lll_opy_(runner, name, context, bstack1llll1l1l_opy_, *args):
    if runner.hooks.get(bstack1111l_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤ಼")).__name__ != bstack1111l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࡢࡨࡪ࡬ࡡࡶ࡮ࡷࡣ࡭ࡵ࡯࡬ࠤಽ"):
      bstack1l11111ll1_opy_(runner, name, context, runner, bstack1llll1l1l_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack1ll111ll_opy_(bstack1111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ಾ")) else context.browser
      runner.driver_initialised = bstack1111l_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧಿ")
    except Exception as e:
      logger.debug(bstack1111l_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡧࡶ࡮ࡼࡥࡳࠢ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡷࡪࠦࡡࡵࡶࡵ࡭ࡧࡻࡴࡦ࠼ࠣࡿࢂ࠭ೀ").format(str(e)))
def bstack11llll1l_opy_(runner, name, context, bstack1llll1l1l_opy_, *args):
    bstack1l11111ll1_opy_(runner, name, context, context.feature, bstack1llll1l1l_opy_, *args)
    try:
      if not bstack1111ll111_opy_:
        bstack1lll1lllll_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll111ll_opy_(bstack1111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩು")) else context.browser
        if is_driver_active(bstack1lll1lllll_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack1111l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠧೂ")
          bstack1ll11lll_opy_ = str(runner.feature.name)
          playwright_set_session_name(context, bstack1ll11lll_opy_)
          bstack1lll1lllll_opy_.execute_script(bstack1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪೃ") + json.dumps(bstack1ll11lll_opy_) + bstack1111l_opy_ (u"࠭ࡽࡾࠩೄ"))
    except Exception as e:
      logger.debug(bstack1111l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧ೅").format(str(e)))
def bstack1ll111111l_opy_(runner, name, context, bstack1llll1l1l_opy_, *args):
    target = context.scenario if hasattr(context, bstack1111l_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪೆ")) else context.feature
    bstack1l11111ll1_opy_(runner, name, context, target, bstack1llll1l1l_opy_, *args)
@measure(event_name=EVENTS.bstack111l1l11l_opy_, stage=STAGE.bstack11lll111l_opy_, bstack11lll111_opy_=SESSION_NAME)
def bstack111lll1l1l_opy_(runner, name, context, bstack1llll1l1l_opy_, *args):
    bstack1l1l1ll1_opy_.start_test(context)
    bstack1l11111ll1_opy_(runner, name, context, context.scenario, bstack1llll1l1l_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack1111l1ll11_opy_.bstack1ll1ll11l_opy_(context, *args)
    try:
      bstack1lll1lllll_opy_ = bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨೇ"), context.browser)
      if is_driver_active(bstack1lll1lllll_opy_):
        TestHubHandler.send_cbt_info(bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩೈ"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack1111l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨ೉")
        if (not bstack1111ll111_opy_):
          scenario_name = args[0].name
          feature_name = bstack1ll11lll_opy_ = str(runner.feature.name)
          bstack1ll11lll_opy_ = feature_name + bstack1111l_opy_ (u"ࠬࠦ࠭ࠡࠩೊ") + scenario_name
          if runner.driver_initialised == bstack1111l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣೋ"):
            playwright_set_session_name(context, bstack1ll11lll_opy_)
            bstack1lll1lllll_opy_.execute_script(bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬೌ") + json.dumps(bstack1ll11lll_opy_) + bstack1111l_opy_ (u"ࠨࡿࢀ್ࠫ"))
    except Exception as e:
      logger.debug(bstack1111l_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡ࡫ࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡀࠠࡼࡿࠪ೎").format(str(e)))
@measure(event_name=EVENTS.bstack1l11ll1l1l_opy_, stage=STAGE.bstack11lll111l_opy_, hook_type=bstack1111l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡖࡸࡪࡶࠢ೏"), bstack11lll111_opy_=SESSION_NAME)
def bstack1ll1lllll_opy_(runner, name, context, bstack1llll1l1l_opy_, *args):
    bstack1l11111ll1_opy_(runner, name, context, args[0], bstack1llll1l1l_opy_, *args)
    try:
      bstack1lll1lllll_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll111ll_opy_(bstack1111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ೐")) else context.browser
      if is_driver_active(bstack1lll1lllll_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack1111l_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥ೑")
        bstack1l1l1ll1_opy_.bstack1ll1l111l_opy_(args[0])
        if runner.driver_initialised == bstack1111l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦ೒") and not bstack1111ll111_opy_:
          feature_name = bstack1ll11lll_opy_ = str(runner.feature.name)
          bstack1ll11lll_opy_ = feature_name + bstack1111l_opy_ (u"ࠧࠡ࠯ࠣࠫ೓") + context.scenario.name
          playwright_set_session_name(context, bstack1ll11lll_opy_)
          bstack1lll1lllll_opy_.execute_script(bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭೔") + json.dumps(bstack1ll11lll_opy_) + bstack1111l_opy_ (u"ࠩࢀࢁࠬೕ"))
    except Exception as e:
      logger.debug(bstack1111l_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡴࡦࡲ࠽ࠤࢀࢃࠧೖ").format(str(e)))
@measure(event_name=EVENTS.bstack1l11ll1l1l_opy_, stage=STAGE.bstack11lll111l_opy_, hook_type=bstack1111l_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࡖࡸࡪࡶࠢ೗"), bstack11lll111_opy_=SESSION_NAME)
def bstack1ll1ll1l1_opy_(runner, name, context, bstack1llll1l1l_opy_, *args):
  bstack1l1l1ll1_opy_.bstack1lll1l1l_opy_(args[0])
  try:
    step_status = args[0].status.name
    bstack1lll1lllll_opy_ = threading.current_thread().bstackSessionDriver if bstack1111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ೘") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack1lll1lllll_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack1111l_opy_ (u"࠭ࡩ࡯ࡵࡷࡩࡵ࠭೙")
        if not bstack1111ll111_opy_:
          feature_name = bstack1ll11lll_opy_ = str(runner.feature.name)
          bstack1ll11lll_opy_ = feature_name + bstack1111l_opy_ (u"ࠧࠡ࠯ࠣࠫ೚") + context.scenario.name
          playwright_set_session_name(context, bstack1ll11lll_opy_)
          bstack1lll1lllll_opy_.execute_script(bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭೛") + json.dumps(bstack1ll11lll_opy_) + bstack1111l_opy_ (u"ࠩࢀࢁࠬ೜"))
    if str(step_status).lower() in [bstack1111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪೝ"), bstack1111l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪೞ")]:
      bstack1111l1lll_opy_ = bstack1111l_opy_ (u"ࠬ࠭೟")
      bstack111ll111l_opy_ = bstack1111l_opy_ (u"࠭ࠧೠ")
      bstack11l11llll_opy_ = bstack1111l_opy_ (u"ࠧࠨೡ")
      try:
        import traceback
        bstack1111l1lll_opy_ = runner.exception.__class__.__name__
        bstack1llllll111_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack111ll111l_opy_ = bstack1111l_opy_ (u"ࠨࠢࠪೢ").join(bstack1llllll111_opy_)
        bstack11l11llll_opy_ = bstack1llllll111_opy_[-1]
      except Exception as e:
        logger.debug(bstack11ll1l11ll_opy_.format(str(e)))
      bstack1111l1lll_opy_ += bstack11l11llll_opy_
      playwright_annotate(context, json.dumps(str(args[0].name) + bstack1111l_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣೣ") + str(bstack111ll111l_opy_)),
                          bstack1111l_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤ೤"))
      if runner.driver_initialised == bstack1111l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤ೥"):
        bstack1l111l11ll_opy_(getattr(context, bstack1111l_opy_ (u"ࠬࡶࡡࡨࡧࠪ೦"), None), bstack1111l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ೧"), bstack1111l1lll_opy_)
        bstack1lll1lllll_opy_.execute_script(bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ೨") + json.dumps(str(args[0].name) + bstack1111l_opy_ (u"ࠣࠢ࠰ࠤࡋࡧࡩ࡭ࡧࡧࠥࡡࡴࠢ೩") + str(bstack111ll111l_opy_)) + bstack1111l_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࡽࡾࠩ೪"))
      if runner.driver_initialised == bstack1111l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣ೫"):
        bstack1ll1111l1l_opy_(bstack1lll1lllll_opy_, bstack1111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ೬"), bstack1111l_opy_ (u"࡙ࠧࡣࡦࡰࡤࡶ࡮ࡵࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤ೭") + str(bstack1111l1lll_opy_))
    else:
      playwright_annotate(context, bstack1111l_opy_ (u"ࠨࡐࡢࡵࡶࡩࡩࠧࠢ೮"), bstack1111l_opy_ (u"ࠢࡪࡰࡩࡳࠧ೯"))
      if runner.driver_initialised == bstack1111l_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨ೰"):
        bstack1l111l11ll_opy_(getattr(context, bstack1111l_opy_ (u"ࠩࡳࡥ࡬࡫ࠧೱ"), None), bstack1111l_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥೲ"))
      bstack1lll1lllll_opy_.execute_script(bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩೳ") + json.dumps(str(args[0].name) + bstack1111l_opy_ (u"ࠧࠦ࠭ࠡࡒࡤࡷࡸ࡫ࡤࠢࠤ೴")) + bstack1111l_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤࢀࢁࠬ೵"))
      if runner.driver_initialised == bstack1111l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧ೶"):
        bstack1ll1111l1l_opy_(bstack1lll1lllll_opy_, bstack1111l_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ೷"))
  except Exception as e:
    logger.debug(bstack1111l_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡳࡵࡧࡳ࠾ࠥࢁࡽࠨ೸").format(str(e)))
  bstack1l11111ll1_opy_(runner, name, context, args[0], bstack1llll1l1l_opy_, *args)
@measure(event_name=EVENTS.bstack111l11l11l_opy_, stage=STAGE.bstack11lll111l_opy_, bstack11lll111_opy_=SESSION_NAME)
def bstack111ll111ll_opy_(runner, name, context, bstack1llll1l1l_opy_, *args):
  bstack1l1l1ll1_opy_.end_test(args[0])
  try:
    bstack1l1lll1l1l_opy_ = args[0].status.name
    bstack1lll1lllll_opy_ = bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ೹"), context.browser)
    bstack1111l1ll11_opy_.bstack1111l1lll1_opy_(bstack1lll1lllll_opy_)
    if str(bstack1l1lll1l1l_opy_).lower() in [bstack1111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ೺"), bstack1111l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ೻")]:
      bstack1111l1lll_opy_ = bstack1111l_opy_ (u"࠭ࠧ೼")
      bstack111ll111l_opy_ = bstack1111l_opy_ (u"ࠧࠨ೽")
      bstack11l11llll_opy_ = bstack1111l_opy_ (u"ࠨࠩ೾")
      try:
        import traceback
        bstack1111l1lll_opy_ = runner.exception.__class__.__name__
        bstack1llllll111_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack111ll111l_opy_ = bstack1111l_opy_ (u"ࠩࠣࠫ೿").join(bstack1llllll111_opy_)
        bstack11l11llll_opy_ = bstack1llllll111_opy_[-1]
      except Exception as e:
        logger.debug(bstack11ll1l11ll_opy_.format(str(e)))
      bstack1111l1lll_opy_ += bstack11l11llll_opy_
      playwright_annotate(context, json.dumps(str(args[0].name) + bstack1111l_opy_ (u"ࠥࠤ࠲ࠦࡆࡢ࡫࡯ࡩࡩࠧ࡜࡯ࠤഀ") + str(bstack111ll111l_opy_)),
                          bstack1111l_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥഁ"))
      if runner.driver_initialised == bstack1111l_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢം") or runner.driver_initialised == bstack1111l_opy_ (u"࠭ࡩ࡯ࡵࡷࡩࡵ࠭ഃ"):
        bstack1l111l11ll_opy_(getattr(context, bstack1111l_opy_ (u"ࠧࡱࡣࡪࡩࠬഄ"), None), bstack1111l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣഅ"), bstack1111l1lll_opy_)
        bstack1lll1lllll_opy_.execute_script(bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧആ") + json.dumps(str(args[0].name) + bstack1111l_opy_ (u"ࠥࠤ࠲ࠦࡆࡢ࡫࡯ࡩࡩࠧ࡜࡯ࠤഇ") + str(bstack111ll111l_opy_)) + bstack1111l_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣࡿࢀࠫഈ"))
      if runner.driver_initialised == bstack1111l_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢഉ") or runner.driver_initialised == bstack1111l_opy_ (u"࠭ࡩ࡯ࡵࡷࡩࡵ࠭ഊ"):
        bstack1ll1111l1l_opy_(bstack1lll1lllll_opy_, bstack1111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧഋ"), bstack1111l_opy_ (u"ࠣࡕࡦࡩࡳࡧࡲࡪࡱࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧഌ") + str(bstack1111l1lll_opy_))
    else:
      playwright_annotate(context, bstack1111l_opy_ (u"ࠤࡓࡥࡸࡹࡥࡥࠣࠥ഍"), bstack1111l_opy_ (u"ࠥ࡭ࡳ࡬࡯ࠣഎ"))
      if runner.driver_initialised == bstack1111l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨഏ") or runner.driver_initialised == bstack1111l_opy_ (u"ࠬ࡯࡮ࡴࡶࡨࡴࠬഐ"):
        bstack1l111l11ll_opy_(getattr(context, bstack1111l_opy_ (u"࠭ࡰࡢࡩࡨࠫ഑"), None), bstack1111l_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢഒ"))
      bstack1lll1lllll_opy_.execute_script(bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ഓ") + json.dumps(str(args[0].name) + bstack1111l_opy_ (u"ࠤࠣ࠱ࠥࡖࡡࡴࡵࡨࡨࠦࠨഔ")) + bstack1111l_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩക"))
      if runner.driver_initialised == bstack1111l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨഖ") or runner.driver_initialised == bstack1111l_opy_ (u"ࠬ࡯࡮ࡴࡶࡨࡴࠬഗ"):
        bstack1ll1111l1l_opy_(bstack1lll1lllll_opy_, bstack1111l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨഘ"))
  except Exception as e:
    logger.debug(bstack1111l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩങ").format(str(e)))
  bstack1l11111ll1_opy_(runner, name, context, context.scenario, bstack1llll1l1l_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack1l1lll111l_opy_(runner, name, context, bstack1llll1l1l_opy_, *args):
    target = context.scenario if hasattr(context, bstack1111l_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪച")) else context.feature
    bstack1l11111ll1_opy_(runner, name, context, target, bstack1llll1l1l_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack1ll1llll1_opy_(runner, name, context, bstack1llll1l1l_opy_, *args):
    try:
      bstack1lll1lllll_opy_ = bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨഛ"), context.browser)
      bstack11lll11l1_opy_ = bstack1111l_opy_ (u"ࠪࠫജ")
      if context.failed is True:
        bstack1l1l1ll111_opy_ = []
        bstack11lll11l1l_opy_ = []
        bstack1l1lllll1_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack1l1l1ll111_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1llllll111_opy_ = traceback.format_tb(exc_tb)
            bstack11ll1l111_opy_ = bstack1111l_opy_ (u"ࠫࠥ࠭ഝ").join(bstack1llllll111_opy_)
            bstack11lll11l1l_opy_.append(bstack11ll1l111_opy_)
            bstack1l1lllll1_opy_.append(bstack1llllll111_opy_[-1])
        except Exception as e:
          logger.debug(bstack11ll1l11ll_opy_.format(str(e)))
        bstack1111l1lll_opy_ = bstack1111l_opy_ (u"ࠬ࠭ഞ")
        for i in range(len(bstack1l1l1ll111_opy_)):
          bstack1111l1lll_opy_ += bstack1l1l1ll111_opy_[i] + bstack1l1lllll1_opy_[i] + bstack1111l_opy_ (u"࠭࡜࡯ࠩട")
        bstack11lll11l1_opy_ = bstack1111l_opy_ (u"ࠧࠡࠩഠ").join(bstack11lll11l1l_opy_)
        if runner.driver_initialised in [bstack1111l_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠤഡ"), bstack1111l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨഢ")]:
          playwright_annotate(context, bstack11lll11l1_opy_, bstack1111l_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤണ"))
          bstack1l111l11ll_opy_(getattr(context, bstack1111l_opy_ (u"ࠫࡵࡧࡧࡦࠩത"), None), bstack1111l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧഥ"), bstack1111l1lll_opy_)
          bstack1lll1lllll_opy_.execute_script(bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫദ") + json.dumps(bstack11lll11l1_opy_) + bstack1111l_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦࢂࢃࠧധ"))
          bstack1ll1111l1l_opy_(bstack1lll1lllll_opy_, bstack1111l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣന"), bstack1111l_opy_ (u"ࠤࡖࡳࡲ࡫ࠠࡴࡥࡨࡲࡦࡸࡩࡰࡵࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࡡࡴࠢഩ") + str(bstack1111l1lll_opy_))
          bstack1111lllll1_opy_ = bstack1lll1llll_opy_(bstack11lll11l1_opy_, runner.feature.name, logger)
          if (bstack1111lllll1_opy_ != None):
            bstack11ll111l1l_opy_.append(bstack1111lllll1_opy_)
      else:
        if runner.driver_initialised in [bstack1111l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦപ"), bstack1111l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣഫ")]:
          playwright_annotate(context, bstack1111l_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࡀࠠࠣബ") + str(runner.feature.name) + bstack1111l_opy_ (u"ࠨࠠࡱࡣࡶࡷࡪࡪࠡࠣഭ"), bstack1111l_opy_ (u"ࠢࡪࡰࡩࡳࠧമ"))
          bstack1l111l11ll_opy_(getattr(context, bstack1111l_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭യ"), None), bstack1111l_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤര"))
          bstack1lll1lllll_opy_.execute_script(bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨറ") + json.dumps(bstack1111l_opy_ (u"ࠦࡋ࡫ࡡࡵࡷࡵࡩ࠿ࠦࠢല") + str(runner.feature.name) + bstack1111l_opy_ (u"ࠧࠦࡰࡢࡵࡶࡩࡩࠧࠢള")) + bstack1111l_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤࢀࢁࠬഴ"))
          bstack1ll1111l1l_opy_(bstack1lll1lllll_opy_, bstack1111l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧവ"))
          bstack1111lllll1_opy_ = bstack1lll1llll_opy_(bstack11lll11l1_opy_, runner.feature.name, logger)
          if (bstack1111lllll1_opy_ != None):
            bstack11ll111l1l_opy_.append(bstack1111lllll1_opy_)
    except Exception as e:
      logger.debug(bstack1111l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࠥ࡬ࡥࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪശ").format(str(e)))
    bstack1l11111ll1_opy_(runner, name, context, context.feature, bstack1llll1l1l_opy_, *args)
@measure(event_name=EVENTS.bstack1l11ll1l1l_opy_, stage=STAGE.bstack11lll111l_opy_, hook_type=bstack1111l_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࡂ࡮࡯ࠦഷ"), bstack11lll111_opy_=SESSION_NAME)
def bstack11l11111l_opy_(runner, name, context, bstack1llll1l1l_opy_, *args):
    bstack1l11111ll1_opy_(runner, name, context, runner, bstack1llll1l1l_opy_, *args)
def bstack1lll1ll1l1_opy_(self, filename=None):
  global bstack1l11l1l11_opy_
  bstack1l11l1l11_opy_(self, filename)
  bstack111l1llll_opy_ = []
  bstack1lll1111ll_opy_ = [bstack1111l_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠫസ"), bstack1111l_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡹࡧࡧࠨഹ"), bstack1111l_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧഺ"), bstack1111l_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵ഻ࠧ"), bstack1111l_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡴࡢࡩ഼ࠪ"), bstack1111l_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨഽ")]
  bstack111l1ll1_opy_ = lambda *_: None
  for hook_name in bstack1lll1111ll_opy_:
    if hook_name not in self.hooks:
      self.hooks[hook_name] = bstack111l1ll1_opy_
      bstack111l1llll_opy_.append(hook_name)
  if bstack111l1llll_opy_:
    os.environ[bstack1111l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡖࡈࡐࡥࡄࡆࡈࡄ࡙ࡑ࡚࡟ࡉࡑࡒࡏࡘ࠭ാ")] = bstack1111l_opy_ (u"ࠪ࠰ࠬി").join(bstack111l1llll_opy_)
def _execute_deferred_playwright_close():
  try:
    _1lll1ll11_opy_ = threading.current_thread()
    _1l1l11l1l_opy_ = getattr(_1lll1ll11_opy_, bstack1111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡩ࡫ࡦࡦࡴࡵࡩࡩࡥࡰࡢࡩࡨࡣࡷ࡫ࡦࠨീ"), None)
    _11llll1ll1_opy_ = getattr(_1lll1ll11_opy_, bstack1111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡪࡥࡧࡧࡵࡶࡪࡪ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡠࡴࡨࡪࠬു"), None)
    _11lll111ll_opy_ = getattr(_1lll1ll11_opy_, bstack1111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡤࡦࡨࡨࡶࡷ࡫ࡤࡠࡲࡺࡣࡸࡺ࡯ࡱࡡࡩࡲࠬൂ"), None)
    _wrapper = getattr(_1lll1ll11_opy_, bstack1111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ൃ"), None)
    if not _11llll1ll1_opy_ and _wrapper and hasattr(_wrapper, bstack1111l_opy_ (u"ࠨࡡࡥࡶࡴࡽࡳࡦࡴࠪൄ")):
      _11llll1ll1_opy_ = _wrapper._browser
    if not _1l1l11l1l_opy_ and _wrapper and hasattr(_wrapper, bstack1111l_opy_ (u"ࠩࡢࡴࡦ࡭ࡥࠨ൅")):
      _1l1l11l1l_opy_ = _wrapper._page
    if not _11lll111ll_opy_:
      _1llll11l_opy_ = getattr(_1lll1ll11_opy_, bstack1111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡨࡪ࡬ࡥࡳࡴࡨࡨࡤࡶࡷࡠࡴࡨࡪࠬെ"), None)
      if _1llll11l_opy_ and hasattr(_1llll11l_opy_, bstack1111l_opy_ (u"ࠫࡸࡺ࡯ࡱࠩേ")):
        _11lll111ll_opy_ = _1llll11l_opy_.stop
    _1l111l1l1_opy_ = _1l1l11l1l_opy_ or _11llll1ll1_opy_ or _11lll111ll_opy_
    if not _1l111l1l1_opy_:
      return
    if _1l1l11l1l_opy_ and hasattr(_1l1l11l1l_opy_, bstack1111l_opy_ (u"ࠬࡩ࡬ࡰࡵࡨࠫൈ")):
      try:
        _1l1l11l1l_opy_.close(_bstack_sdk_close=True)
      except TypeError:
        try:
          _1l1l11l1l_opy_.close()
        except Exception:
          pass
      except Exception as e:
        logger.debug(bstack1111l_opy_ (u"࠭ࡄࡦࡨࡨࡶࡷ࡫ࡤࠡࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡶࡡࡨࡧ࠱ࡧࡱࡵࡳࡦࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡿࢂ࠭൉").format(str(e)))
    if _11llll1ll1_opy_ and hasattr(_11llll1ll1_opy_, bstack1111l_opy_ (u"ࠧࡤ࡮ࡲࡷࡪ࠭ൊ")):
      try:
        _11llll1ll1_opy_.close(_bstack_sdk_close=True)
      except TypeError:
        try:
          _11llll1ll1_opy_.close()
        except Exception:
          pass
      except Exception as e:
        logger.debug(bstack1111l_opy_ (u"ࠨࡆࡨࡪࡪࡸࡲࡦࡦࠣࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡣࡴࡲࡻࡸ࡫ࡲ࠯ࡥ࡯ࡳࡸ࡫ࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡽࢀࠫോ").format(str(e)))
    if _11lll111ll_opy_:
      try:
        _11lll111ll_opy_(_bstack_sdk_close=True)
      except TypeError:
        try:
          _11lll111ll_opy_()
        except Exception:
          pass
      except Exception as e:
        logger.debug(bstack1111l_opy_ (u"ࠩࡇࡩ࡫࡫ࡲࡳࡧࡧࠤࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡷࡳࡵࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࡼࡿࠪൌ").format(str(e)))
    for attr in (bstack1111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡨࡪ࡬ࡥࡳࡴࡨࡨࡤࡶࡡࡨࡧࡢࡧࡱࡵࡳࡦ്ࠩ"), bstack1111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡩ࡫ࡦࡦࡴࡵࡩࡩࡥࡰࡢࡩࡨࡣࡷ࡫ࡦࠨൎ"),
                 bstack1111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡪࡥࡧࡧࡵࡶࡪࡪ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡠࡥ࡯ࡳࡸ࡫ࠧ൏"), bstack1111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡤࡦࡨࡨࡶࡷ࡫ࡤࡠࡤࡵࡳࡼࡹࡥࡳࡡࡵࡩ࡫࠭൐"),
                 bstack1111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡥࡧࡩࡩࡷࡸࡥࡥࡡࡳࡻࡤࡹࡴࡰࡲࠪ൑"), bstack1111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡦࡨࡪࡪࡸࡲࡦࡦࡢࡴࡼࡥࡳࡵࡱࡳࡣ࡫ࡴࠧ൒"),
                 bstack1111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡧࡩ࡫࡫ࡲࡳࡧࡧࡣࡵࡽ࡟ࡳࡧࡩࠫ൓")):
      try:
        delattr(_1lll1ll11_opy_, attr)
      except AttributeError:
        pass
    if _wrapper:
      try:
        _wrapper._page = None
        _wrapper._browser = None
      except Exception:
        pass
    logger.debug(bstack1111l_opy_ (u"ࠪࡈࡪ࡬ࡥࡳࡴࡨࡨࠥࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡦࡰࡴࡹࡥࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠤ࡫ࡵࡲࠡࡶ࡫ࡶࡪࡧࡤࠡࡽࢀࠫൔ").format(_1lll1ll11_opy_.ident))
  except Exception as e:
    logger.debug(bstack1111l_opy_ (u"ࠫࡉ࡫ࡦࡦࡴࡵࡩࡩࠦࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡧࡱࡵࡳࡦࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡿࢂ࠭ൕ").format(str(e)))
def bstack111l1l1l1_opy_(self, name, *args):
  global bstack1llll1l1l_opy_
  global bstack11ll1lll_opy_
  try:
    if BROWSERSTACK_AUTOMATION:
      platform_index = int(threading.current_thread()._name) % bstack11l1llll11_opy_
      bstack11ll1l1l_opy_ = CONFIG[bstack1111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨൖ")][platform_index]
      os.environ[bstack1111l_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧൗ")] = json.dumps(bstack11ll1l1l_opy_)
    if not hasattr(self, bstack1111l_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡨࡨࠬ൘")):
      self.driver_initialised = None
    bstack1l1lll11l1_opy_ = {
        bstack1111l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠬ൙"): bstack1ll1ll1lll_opy_,
        bstack1111l_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠪ൚"): bstack11llll1l_opy_,
        bstack1111l_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡸࡦ࡭ࠧ൛"): bstack1ll111111l_opy_,
        bstack1111l_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭൜"): bstack111lll1l1l_opy_,
        bstack1111l_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠪ൝"): bstack1ll1lllll_opy_,
        bstack1111l_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡴࡦࡲࠪ൞"): bstack1ll1ll1l1_opy_,
        bstack1111l_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨൟ"): bstack111ll111ll_opy_,
        bstack1111l_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡵࡣࡪࠫൠ"): bstack1l1lll111l_opy_,
        bstack1111l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠩൡ"): bstack1ll1llll1_opy_,
        bstack1111l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ࠭ൢ"): bstack11l11111l_opy_
    }
    handler = bstack1l1lll11l1_opy_.get(name, bstack1llll1l1l_opy_)
    try:
      if args:
        context = args[0]
        remaining_args = args[1:]
        if bstack11ll1lll_opy_ is None or not bstack11ll1lll_opy_:
          context = self.context
          remaining_args = args
      else:
        context = self.context
        remaining_args = ()
      handler(self, name, context, bstack1llll1l1l_opy_, *remaining_args)
    except Exception as e:
      logger.debug(bstack1111l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡢࡦࡪࡤࡺࡪࠦࡨࡰࡱ࡮ࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶࠥࢁࡽ࠻ࠢࡾࢁࠬൣ").format(name, str(e)))
    if name == bstack1111l_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭൤"):
      _execute_deferred_playwright_close()
    if name in [bstack1111l_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭൥"), bstack1111l_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨ൦"), bstack1111l_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠫ൧")]:
      try:
        bstack1lll1lllll_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll111ll_opy_(bstack1111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ൨")) else context.browser
        bstack1ll1111l1_opy_ = (
          (name == bstack1111l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ࠭൩") and self.driver_initialised == bstack1111l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣ൪")) or
          (name == bstack1111l_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬ൫") and self.driver_initialised == bstack1111l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠢ൬")) or
          (name == bstack1111l_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨ൭") and self.driver_initialised in [bstack1111l_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥ൮"), bstack1111l_opy_ (u"ࠤ࡬ࡲࡸࡺࡥࡱࠤ൯")]) or
          (name == bstack1111l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡸࡪࡶࠧ൰") and self.driver_initialised == bstack1111l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤ൱"))
        )
        if bstack1ll1111l1_opy_:
          self.driver_initialised = None
          if bstack1lll1lllll_opy_ and hasattr(bstack1lll1lllll_opy_, bstack1111l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠩ൲")):
            try:
              bstack1lll1lllll_opy_.quit()
            except Exception as e:
              logger.debug(bstack1111l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡷࡵࡪࡶࡷ࡭ࡳ࡭ࠠࡥࡴ࡬ࡺࡪࡸࠠࡪࡰࠣࡦࡪ࡮ࡡࡷࡧࠣ࡬ࡴࡵ࡫࠻ࠢࡾࢁࠬ൳").format(str(e)))
      except Exception as e:
        logger.debug(bstack1111l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࠡࡪࡲࡳࡰࠦࡣ࡭ࡧࡤࡲࡺࡶࠠࡧࡱࡵࠤࢀࢃ࠺ࠡࡽࢀࠫ൴").format(name, str(e)))
  except Exception as e:
    logger.debug(bstack1111l_opy_ (u"ࠨࡅࡵ࡭ࡹ࡯ࡣࡢ࡮ࠣࡩࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡨࡥࡩࡣࡹࡩࠥࡸࡵ࡯ࠢ࡫ࡳࡴࡱࠠࡼࡿ࠽ࠤࢀࢃࠧ൵").format(name, str(e)))
    try:
      if bstack11ll1lll_opy_ is None or bstack11ll1lll_opy_:
        try:
          bstack1llll1l1l_opy_(self, name, self.context, *args)
        except TypeError:
          bstack1llll1l1l_opy_(self, name, *args)
      else:
        bstack1llll1l1l_opy_(self, name, *args)
    except Exception as e2:
      logger.debug(bstack1111l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࠦ࡯ࡳ࡫ࡪ࡭ࡳࡧ࡬ࠡࡤࡨ࡬ࡦࡼࡥࠡࡪࡲࡳࡰࠦࡻࡾ࠼ࠣࡿࢂ࠭൶").format(name, str(e2)))
  finally:
    if name == bstack1111l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ൷"):
      _execute_deferred_playwright_close()
def bstack1111ll11l_opy_(config, startdir):
  return bstack1111l_opy_ (u"ࠦࡩࡸࡩࡷࡧࡵ࠾ࠥࢁ࠰ࡾࠤ൸").format(bstack1111l_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦ൹"))
notset = Notset()
def bstack1l1111ll1l_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1l11l1l1_opy_
  if str(name).lower() == bstack1111l_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷ࠭ൺ"):
    return bstack1111l_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨൻ")
  else:
    return bstack1l11l1l1_opy_(self, name, default, skip)
def bstack1l1lll1l11_opy_(item, when):
  global bstack1ll1l1111_opy_
  try:
    bstack1ll1l1111_opy_(item, when)
  except Exception as e:
    pass
def bstack1l1l1l11_opy_():
  return
def browserstack_executor_helper(type, name, status, reason, bstack1l1l11ll_opy_, bstack1l111111ll_opy_):
  bstack111l111111_opy_ = {
    bstack1111l_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨർ"): type,
    bstack1111l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬൽ"): {}
  }
  if type == bstack1111l_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬൾ"):
    bstack111l111111_opy_[bstack1111l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧൿ")][bstack1111l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ඀")] = bstack1l1l11ll_opy_
    bstack111l111111_opy_[bstack1111l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩඁ")][bstack1111l_opy_ (u"ࠧࡥࡣࡷࡥࠬං")] = json.dumps(str(bstack1l111111ll_opy_))
  if type == bstack1111l_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩඃ"):
    bstack111l111111_opy_[bstack1111l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ඄")][bstack1111l_opy_ (u"ࠪࡲࡦࡳࡥࠨඅ")] = name
  if type == bstack1111l_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧආ"):
    bstack111l111111_opy_[bstack1111l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨඇ")][bstack1111l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ඈ")] = status
    if status == bstack1111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧඉ"):
      bstack111l111111_opy_[bstack1111l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫඊ")][bstack1111l_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩඋ")] = json.dumps(str(reason))
  bstack111l1l1ll_opy_ = bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨඌ").format(json.dumps(bstack111l111111_opy_))
  return bstack111l1l1ll_opy_
def bstack1l11l1llll_opy_(driver_command, response):
    if driver_command == bstack1111l_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨඍ"):
        TestHubHandler.bstack11l1lll1l1_opy_({
            bstack1111l_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫඎ"): response[bstack1111l_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬඏ")],
            bstack1111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧඐ"): TestHubHandler.current_test_uuid()
        })
def bstack11l1ll1111_opy_(item, call, rep):
  global bstack11ll11ll1l_opy_
  global bstack1l1lll1ll_opy_
  global bstack1111ll111_opy_
  name = bstack1111l_opy_ (u"ࠨࠩඑ")
  try:
    if rep.when == bstack1111l_opy_ (u"ࠩࡦࡥࡱࡲࠧඒ"):
      bstack1lll11111_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1111ll111_opy_:
          name = str(rep.nodeid)
          executor_string = browserstack_executor_helper(bstack1111l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫඓ"), name, bstack1111l_opy_ (u"ࠫࠬඔ"), bstack1111l_opy_ (u"ࠬ࠭ඕ"), bstack1111l_opy_ (u"࠭ࠧඖ"), bstack1111l_opy_ (u"ࠧࠨ඗"))
          threading.current_thread().bstack1ll11111_opy_ = name
          for driver in bstack1l1lll1ll_opy_:
            if bstack1lll11111_opy_ == driver.session_id:
              driver.execute_script(executor_string)
      except Exception as e:
        logger.debug(bstack1111l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨ඘").format(str(e)))
      try:
        bstack111lll111_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack1111l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ඙"):
          status = bstack1111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪක") if rep.outcome.lower() == bstack1111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫඛ") else bstack1111l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬග")
          reason = bstack1111l_opy_ (u"࠭ࠧඝ")
          if status == bstack1111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧඞ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack1111l_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭ඟ") if status == bstack1111l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩච") else bstack1111l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩඡ")
          data = name + bstack1111l_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭ජ") if status == bstack1111l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬඣ") else name + bstack1111l_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠡࠡࠩඤ") + reason
          bstack111lll111l_opy_ = browserstack_executor_helper(bstack1111l_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩඥ"), bstack1111l_opy_ (u"ࠨࠩඦ"), bstack1111l_opy_ (u"ࠩࠪට"), bstack1111l_opy_ (u"ࠪࠫඨ"), level, data)
          for driver in bstack1l1lll1ll_opy_:
            if bstack1lll11111_opy_ == driver.session_id:
              driver.execute_script(bstack111lll111l_opy_)
      except Exception as e:
        logger.debug(bstack1111l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡥࡲࡲࡹ࡫ࡸࡵࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨඩ").format(str(e)))
  except Exception as e:
    logger.debug(bstack1111l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡵࡷࡥࡹ࡫ࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻࡾࠩඪ").format(str(e)))
  bstack11ll11ll1l_opy_(item, call, rep)
def bstack1ll1111ll_opy_(driver, bstack1l1l1l11l_opy_, test=None):
  global PLATFORM_INDEX
  if test != None:
    bstack111llll1_opy_ = getattr(test, bstack1111l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫණ"), None)
    bstack1l111lll1l_opy_ = getattr(test, bstack1111l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬඬ"), None)
    PercySDK.screenshot(driver, bstack1l1l1l11l_opy_, bstack111llll1_opy_=bstack111llll1_opy_, bstack1l111lll1l_opy_=bstack1l111lll1l_opy_, bstack11lllllll_opy_=PLATFORM_INDEX)
  else:
    PercySDK.screenshot(driver, bstack1l1l1l11l_opy_)
@measure(event_name=EVENTS.bstack1l1111llll_opy_, stage=STAGE.bstack11lll111l_opy_, bstack11lll111_opy_=SESSION_NAME)
def bstack11l1ll1l11_opy_(driver):
  if bstack1ll1lll11l_opy_.bstack1l11ll1ll1_opy_() is True or bstack1ll1lll11l_opy_.capturing() is True:
    return
  bstack1ll1lll11l_opy_.bstack1l1111l1l1_opy_()
  while not bstack1ll1lll11l_opy_.bstack1l11ll1ll1_opy_():
    bstack1lll1111_opy_ = bstack1ll1lll11l_opy_.bstack111l11ll1l_opy_()
    bstack1ll1111ll_opy_(driver, bstack1lll1111_opy_)
  bstack1ll1lll11l_opy_.bstack11lll1llll_opy_()
def bstack111l1111_opy_(sequence, driver_command, response = None, bstack1llll1lll1_opy_ = None, args = None):
    try:
      if sequence != bstack1111l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨත"):
        return
      if percy.bstack1l11111l1l_opy_() == bstack1111l_opy_ (u"ࠤࡩࡥࡱࡹࡥࠣථ"):
        return
      bstack1lll1111_opy_ = bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠪࡴࡪࡸࡣࡺࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ද"), None)
      for command in bstack11ll1l1lll_opy_:
        if command == driver_command:
          with bstack11ll11l1l_opy_:
            bstack11lll1111l_opy_ = bstack1l1lll1ll_opy_.copy()
          for driver in bstack11lll1111l_opy_:
            bstack11l1ll1l11_opy_(driver)
      bstack11l11111ll_opy_ = percy.bstack11l11l11_opy_()
      if driver_command in bstack1llll11l1l_opy_[bstack11l11111ll_opy_]:
        bstack1ll1lll11l_opy_.bstack111111ll1_opy_(bstack1lll1111_opy_, driver_command)
    except Exception as e:
      pass
_1l111ll1l_opy_ = threading.Event()
def bstack111lllll1_opy_(framework_name):
  if global_config.get_property(bstack1111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨධ")):
      _1l111ll1l_opy_.wait(timeout=30)
      return
  global_config.bstack1ll1111l11_opy_(bstack1111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩන"), True)
  global FRAMEWORK_NAME
  global SELENIUM_OR_PLAYWRIGHT_INSTALLED
  global bstack1l1l11llll_opy_
  FRAMEWORK_NAME = framework_name
  logger.info(bstack1ll11lll1l_opy_.format(FRAMEWORK_NAME.split(bstack1111l_opy_ (u"࠭࠭ࠨ඲"))[0]))
  bstack11l1111ll_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    global bstack11l1l1l1l_opy_
    bstack1lll1l1l11_opy_ = BROWSERSTACK_AUTOMATION or bstack11l1l1l1l_opy_
    if bstack1lll1l1l11_opy_:
      Service.start = bstack1l11l111_opy_
      Service.stop = bstack11lll1l11l_opy_
      webdriver.Remote.get = bstack11ll1ll1_opy_
      WebDriver.quit = bstack11l1l1ll_opy_
      webdriver.Remote.__init__ = bstack1l11l111ll_opy_
    if not BROWSERSTACK_AUTOMATION and not bstack11l1l1l1l_opy_:
        webdriver.Remote.__init__ = bstack1lll111lll_opy_
    WebDriver.getAccessibilityResults = getAccessibilityResults
    WebDriver.get_accessibility_results = getAccessibilityResults
    WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
    WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
    WebDriver.performScan = perform_scan
    WebDriver.perform_scan = perform_scan
    WebDriver.execute = bstack111l11ll1_opy_
    SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
  except Exception as e:
    pass
  try:
    bstack1lll1l1l11_opy_ = BROWSERSTACK_AUTOMATION or bstack11l1l1l1l_opy_
    if bstack1lll1l1l11_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack11ll111l11_opy_
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
    logger.debug(bstack1111l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤ࡬ࡲ࡯ࡣࡣ࡯ࡷ࠿ࠦࡻࡾࠤඳ").format(str(e)))
  patch_playwright()
  if not SELENIUM_OR_PLAYWRIGHT_INSTALLED:
    bstack11ll1ll11l_opy_(bstack1111l_opy_ (u"ࠣࡒࡤࡧࡰࡧࡧࡦࡵࠣࡲࡴࡺࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠥප"), bstack111111ll_opy_)
  if bstack1l1ll1l11l_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      if hasattr(RemoteConnection, bstack1111l_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪඵ")) and callable(getattr(RemoteConnection, bstack1111l_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫබ"))):
        RemoteConnection._get_proxy_url = bstack1111l11ll1_opy_
      else:
        from selenium.webdriver.remote.client_config import ClientConfig
        ClientConfig.get_proxy_url = bstack1111l11ll1_opy_
    except Exception as e:
      logger.error(bstack111l1lllll_opy_.format(str(e)))
  if bstack11lllllll1_opy_():
    bstack11l1l11l_opy_(CONFIG, logger)
  if (bstack1111l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪභ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      try:
        from pabot.pabot import QueueItem
        from pabot import pabot
      except Exception as e:
        logger.warning(bstack11l1ll1l1_opy_ + str(e))
      if not is_robot_playwright_installed():
        try:
          if percy.bstack1l11111l1l_opy_() == bstack1111l_opy_ (u"ࠧࡺࡲࡶࡧࠥම"):
            bstack1l111l1lll_opy_(bstack111l1111_opy_)
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
          WebDriverCreator._get_ff_profile = bstack1lll1l1ll1_opy_
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
          WebDriverCache.close = bstack1ll1l1llll_opy_
        except Exception as e:
          logger.warning(bstack1l1llllll1_opy_ + str(e))
        try:
          from AppiumLibrary.utils.applicationcache import ApplicationCache
          ApplicationCache.close = bstack1lll1lll1_opy_
        except Exception as e:
          logger.debug(bstack1ll1l11l1l_opy_ + str(e))
    except Exception as e:
      bstack11ll1ll11l_opy_(e, bstack1l1llllll1_opy_)
    Output.start_test = bstack11l111l1_opy_
    Output.end_test = bstack11lll11ll_opy_
    TestStatus.__init__ = bstack1111ll1l11_opy_
    QueueItem.__init__ = bstack1l1l111l1_opy_
    pabot._create_items = bstack11lllll1l_opy_
    try:
      from pabot import __version__ as bstack1ll11ll1l1_opy_
      if version.parse(bstack1ll11ll1l1_opy_) >= version.parse(bstack1111l_opy_ (u"࠭࠵࠯࠲࠱࠴ࠬඹ")):
        pabot._run = bstack1lll1l1l1l_opy_
      elif version.parse(bstack1ll11ll1l1_opy_) >= version.parse(bstack1111l_opy_ (u"ࠧ࠵࠰࠵࠲࠵࠭ය")):
        pabot._run = bstack1111l1l111_opy_
      elif version.parse(bstack1ll11ll1l1_opy_) >= version.parse(bstack1111l_opy_ (u"ࠨ࠴࠱࠵࠺࠴࠰ࠨර")):
        pabot._run = bstack1ll11l111_opy_
      elif version.parse(bstack1ll11ll1l1_opy_) >= version.parse(bstack1111l_opy_ (u"ࠩ࠵࠲࠶࠹࠮࠱ࠩ඼")):
        pabot._run = bstack1l1l1l1ll_opy_
      else:
        pabot._run = bstack1l1l111111_opy_
    except Exception as e:
      pabot._run = bstack1l1l111111_opy_
    pabot._create_command_for_execution = bstack1l1ll11lll_opy_
    pabot._report_results = bstack1ll11111l_opy_
  if bstack1111l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪල") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11ll1ll11l_opy_(e, bstack1111l111l1_opy_)
    Runner.run_hook = bstack111l1l1l1_opy_
    try:
      from behave import __version__ as bstack11l1l11l11_opy_
      if version.parse(bstack11l1l11l11_opy_) >= version.parse(bstack1111l_opy_ (u"ࠫ࠶࠴࠳࠯࠲ࠪ඾")):
        Runner.load_hooks = bstack1lll1ll1l1_opy_
    except Exception as e:
      logger.debug(bstack1111l_opy_ (u"ࠬࡉ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤࡧ࡫ࡨࡢࡸࡨࠤࡻ࡫ࡲࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩ඿").format(str(e)))
    Step.run = bstack11l1ll1l1l_opy_
  if bstack1111l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ව") in str(framework_name).lower():
    if not BROWSERSTACK_AUTOMATION:
      _1l111ll1l_opy_.set()
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack1111ll11l_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1l1l1l11_opy_
      Config.getoption = bstack1l1111ll1l_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack11l1ll1111_opy_
    except Exception as e:
      pass
  _1l111ll1l_opy_.set()
def bstack11llll1l1l_opy_():
  global CONFIG
  if bstack1111l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧශ") in CONFIG and int(CONFIG[bstack1111l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨෂ")]) > 1:
    logger.warning(bstack11ll1ll1l1_opy_)
def bstack1lll1l1l1_opy_(arg, bstack111lll1l11_opy_, bstack1ll1ll11l1_opy_=None):
  global CONFIG
  global bstack11l11lll11_opy_
  global bstack1l1111111l_opy_
  global BROWSERSTACK_AUTOMATION
  global bstack11l1l1l1l_opy_
  global global_config
  bstack11l11l11ll_opy_ = bstack1111l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩස")
  if bstack111lll1l11_opy_ and isinstance(bstack111lll1l11_opy_, str):
    bstack111lll1l11_opy_ = eval(bstack111lll1l11_opy_)
  CONFIG = bstack111lll1l11_opy_[bstack1111l_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪහ")]
  bstack11l11lll11_opy_ = bstack111lll1l11_opy_[bstack1111l_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬළ")]
  bstack1l1111111l_opy_ = bstack111lll1l11_opy_[bstack1111l_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧෆ")]
  BROWSERSTACK_AUTOMATION = bstack111lll1l11_opy_[bstack1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ෇")]
  try:
    bstack1l111llll_opy_ = bstack111lll1l11_opy_.get(bstack1111l_opy_ (u"ࠧࡐࡘࡈࡖࡗࡏࡄࡆࡡࡏࡓࡆࡊ࡟ࡕࡇࡖࡘࡎࡔࡇࠨ෈"), False)
    bstack11l1l1l1l_opy_ = bool(bstack1l111llll_opy_)
    os.environ[bstack1111l_opy_ (u"ࠨࡑ࡙ࡉࡗࡘࡉࡅࡇࡢࡐࡔࡇࡄࡠࡖࡈࡗ࡙ࡏࡎࡈࠩ෉")] = str(bstack11l1l1l1l_opy_).lower()
  except Exception as e:
    logger.error(bstack1111l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡏࡗࡇࡕࡖࡎࡊࡅࡠࡎࡒࡅࡉࡥࡔࡆࡕࡗࡍࡓࡍ࠺ࠡࡽࢀ්ࠦ").format(e))
    bstack11l1l1l1l_opy_ = False
    os.environ[bstack1111l_opy_ (u"ࠪࡓ࡛ࡋࡒࡓࡋࡇࡉࡤࡒࡏࡂࡆࡢࡘࡊ࡙ࡔࡊࡐࡊࠫ෋")] = bstack1111l_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪ෌")
  global_config.bstack1ll1111l11_opy_(bstack1111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭෍"), BROWSERSTACK_AUTOMATION)
  os.environ[bstack1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ෎")] = bstack11l11l11ll_opy_
  os.environ[bstack1111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌ࠭ා")] = json.dumps(CONFIG)
  os.environ[bstack1111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡉࡗࡅࡣ࡚ࡘࡌࠨැ")] = bstack11l11lll11_opy_
  os.environ[bstack1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪෑ")] = str(bstack1l1111111l_opy_)
  os.environ[bstack1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡐ࡚ࡍࡉࡏࠩි")] = str(True)
  if bstack11lll1lll_opy_(arg, [bstack1111l_opy_ (u"ࠫ࠲ࡴࠧී"), bstack1111l_opy_ (u"ࠬ࠳࠭࡯ࡷࡰࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ු")]) != -1:
    os.environ[bstack1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡁࡓࡃࡏࡐࡊࡒࠧ෕")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack11ll1ll11_opy_)
    return
  bstack111ll1llll_opy_()
  global bstack111l1l11_opy_
  global PLATFORM_INDEX
  global bstack1l1l111ll_opy_
  global bstack111ll111l1_opy_
  global bstack11ll111l_opy_
  global bstack1l1l11llll_opy_
  global PARALLELISE_VANILLA_PYTHON
  arg.append(bstack1111l_opy_ (u"ࠢ࠮࡙ࠥූ"))
  arg.append(bstack1111l_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡥ࠻ࡏࡲࡨࡺࡲࡥࠡࡣ࡯ࡶࡪࡧࡤࡺࠢ࡬ࡱࡵࡵࡲࡵࡧࡧ࠾ࡵࡿࡴࡦࡵࡷ࠲ࡕࡿࡴࡦࡵࡷ࡛ࡦࡸ࡮ࡪࡰࡪࠦ෗"))
  arg.append(bstack1111l_opy_ (u"ࠤ࠰࡛ࠧෘ"))
  arg.append(bstack1111l_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧ࠽ࡘ࡭࡫ࠠࡩࡱࡲ࡯࡮ࡳࡰ࡭ࠤෙ"))
  global bstack1ll1l1ll_opy_
  global bstack11l1ll11l_opy_
  global bstack1ll11l11ll_opy_
  global bstack1lllllll1_opy_
  global bstack1l1ll1111_opy_
  global bstack1ll1l11ll1_opy_
  global bstack1111111l_opy_
  global bstack11l11l11l1_opy_
  global bstack11l11lll1_opy_
  global bstack1l1l111l1l_opy_
  global bstack1l11l1l1_opy_
  global bstack1ll1l1111_opy_
  global bstack11ll11ll1l_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1ll1l1ll_opy_ = webdriver.Remote.__init__
    bstack11l1ll11l_opy_ = WebDriver.quit
    bstack11l11l11l1_opy_ = WebDriver.close
    bstack11l11lll1_opy_ = WebDriver.get
    bstack1ll11l11ll_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1ll1l1l11l_opy_(CONFIG) and bstack1l11ll1111_opy_():
    if bstack1l1ll1ll1l_opy_() < version.parse(bstack11l11ll1_opy_):
      logger.error(bstack1ll1lllll1_opy_.format(bstack1l1ll1ll1l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack1111l_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬේ")) and callable(getattr(RemoteConnection, bstack1111l_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭ෛ"))):
          bstack1l1l111l1l_opy_ = RemoteConnection._get_proxy_url
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          bstack1l1l111l1l_opy_ = ClientConfig.get_proxy_url
      except Exception as e:
        logger.error(bstack111l1lllll_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1l11l1l1_opy_ = Config.getoption
    from _pytest import runner
    bstack1ll1l1111_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warning(bstack1111l_opy_ (u"ࠨࠥࡴ࠼ࠣࠩࡸࠨො"), bstack111ll11l11_opy_, str(e))
  try:
    from pytest_bdd import reporting
    bstack11ll11ll1l_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack1111l_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨෝ"))
  if cli.is_enabled(CONFIG) and cli.config:
    bstack1l1l111ll_opy_ = cli.config.get(bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬෞ"), {}).get(bstack1111l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫෟ"))
  else:
    bstack1l1l111ll_opy_ = CONFIG.get(bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ෠"), {}).get(bstack1111l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭෡"))
  PARALLELISE_VANILLA_PYTHON = True
  if cli.is_enabled(CONFIG):
    if cli.bstack11l1l111_opy_():
      bstack1111ll11_opy_.invoke(Events.CONNECT, bstack1lllll111l_opy_())
    platform_index = int(os.environ.get(bstack1111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ෢"), bstack1111l_opy_ (u"࠭࠰ࠨ෣")))
  else:
    bstack111lllll1_opy_(bstack111ll1l11l_opy_)
  os.environ[bstack1111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨ෤")] = CONFIG[bstack1111l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ෥")]
  os.environ[bstack1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬ෦")] = CONFIG[bstack1111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭෧")]
  os.environ[bstack1111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ෨")] = BROWSERSTACK_AUTOMATION.__str__()
  from _pytest.config import main as bstack11ll1l11l_opy_
  bstack1l11llll11_opy_ = []
  try:
    exit_code = bstack11ll1l11l_opy_(arg)
    if cli.is_enabled(CONFIG):
      cli.bstack1l11l1l11l_opy_()
    if bstack1111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩ෩") in multiprocessing.current_process().__dict__.keys():
      for bstack11l1lll1ll_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1l11llll11_opy_.append(bstack11l1lll1ll_opy_)
    try:
      bstack11llllllll_opy_ = (bstack1l11llll11_opy_, int(exit_code))
      bstack1ll1ll11l1_opy_.append(bstack11llllllll_opy_)
    except:
      bstack1ll1ll11l1_opy_.append((bstack1l11llll11_opy_, exit_code))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack1l11llll11_opy_.append({bstack1111l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ෪"): bstack1111l_opy_ (u"ࠧࡑࡴࡲࡧࡪࡹࡳࠡࠩ෫") + os.environ.get(bstack1111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ෬")), bstack1111l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ෭"): traceback.format_exc(), bstack1111l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ෮"): int(os.environ.get(bstack1111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ෯")))})
    bstack1ll1ll11l1_opy_.append((bstack1l11llll11_opy_, 1))
def mod_behave_main(args, retries):
  try:
    from behave.configuration import Configuration
    from behave.__main__ import run_behave
    from browserstack_sdk.bstack_behave_runner import BehaveRunner
    config = Configuration(args)
    config.update_userdata({bstack1111l_opy_ (u"ࠧࡸࡥࡵࡴ࡬ࡩࡸࠨ෰"): str(retries)})
    return run_behave(config, runner_class=BehaveRunner)
  except Exception as e:
    bstack111ll1l1l1_opy_ = e.__class__.__name__
    print(bstack1111l_opy_ (u"ࠨࠥࡴ࠼ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡦࡪ࡮ࡡࡷࡧࠣࡸࡪࡹࡴࠡࠧࡶࠦ෱") % (bstack111ll1l1l1_opy_, e))
    return 1
def bstack1lll1llll1_opy_(arg):
  global bstack11l1l1111_opy_
  bstack111lllll1_opy_(bstack11l1l11lll_opy_)
  os.environ[bstack1111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨෲ")] = str(bstack1l1111111l_opy_)
  retries = bstack11ll11l11l_opy_.bstack1l11l11l1l_opy_(CONFIG)
  status_code = 0
  if bstack11ll11l11l_opy_.bstack11lllll111_opy_(CONFIG):
    status_code = mod_behave_main(arg, retries)
  else:
    from behave.__main__ import main as bstack1l11111l11_opy_
    status_code = bstack1l11111l11_opy_(arg)
  if status_code != 0:
    bstack11l1l1111_opy_ = status_code
def bstack1111llll11_opy_():
  logger.info(bstack1llllll11_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1111l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧෳ"), help=bstack1111l_opy_ (u"ࠩࡊࡩࡳ࡫ࡲࡢࡶࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡧࡴࡴࡦࡪࡩࠪ෴"))
  parser.add_argument(bstack1111l_opy_ (u"ࠪ࠱ࡺ࠭෵"), bstack1111l_opy_ (u"ࠫ࠲࠳ࡵࡴࡧࡵࡲࡦࡳࡥࠨ෶"), help=bstack1111l_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫ෷"))
  parser.add_argument(bstack1111l_opy_ (u"࠭࠭࡬ࠩ෸"), bstack1111l_opy_ (u"ࠧ࠮࠯࡮ࡩࡾ࠭෹"), help=bstack1111l_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡧࡣࡤࡧࡶࡷࠥࡱࡥࡺࠩ෺"))
  parser.add_argument(bstack1111l_opy_ (u"ࠩ࠰ࡪࠬ෻"), bstack1111l_opy_ (u"ࠪ࠱࠲࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ෼"), help=bstack1111l_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ෽"))
  bstack111ll1111_opy_ = parser.parse_args()
  try:
    bstack11l1l1ll11_opy_ = bstack1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡬࡫࡮ࡦࡴ࡬ࡧ࠳ࡿ࡭࡭࠰ࡶࡥࡲࡶ࡬ࡦࠩ෾")
    if bstack111ll1111_opy_.framework and bstack111ll1111_opy_.framework not in (bstack1111l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭෿"), bstack1111l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨ฀")):
      bstack11l1l1ll11_opy_ = bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࠱ࡽࡲࡲ࠮ࡴࡣࡰࡴࡱ࡫ࠧก")
    bstack11l1l1l111_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11l1l1ll11_opy_)
    bstack1111111l1_opy_ = open(bstack11l1l1l111_opy_, bstack1111l_opy_ (u"ࠩࡵࠫข"))
    bstack11l111l11_opy_ = bstack1111111l1_opy_.read()
    bstack1111111l1_opy_.close()
    if bstack111ll1111_opy_.username:
      bstack11l111l11_opy_ = bstack11l111l11_opy_.replace(bstack1111l_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪฃ"), bstack111ll1111_opy_.username)
    if bstack111ll1111_opy_.key:
      bstack11l111l11_opy_ = bstack11l111l11_opy_.replace(bstack1111l_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭ค"), bstack111ll1111_opy_.key)
    if bstack111ll1111_opy_.framework:
      bstack11l111l11_opy_ = bstack11l111l11_opy_.replace(bstack1111l_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ฅ"), bstack111ll1111_opy_.framework)
    file_name = bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩฆ")
    file_path = os.path.abspath(file_name)
    bstack1lll111l11_opy_ = open(file_path, bstack1111l_opy_ (u"ࠧࡸࠩง"))
    bstack1lll111l11_opy_.write(bstack11l111l11_opy_)
    bstack1lll111l11_opy_.close()
    logger.info(bstack1ll1111lll_opy_)
    try:
      os.environ[bstack1111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪจ")] = bstack111ll1111_opy_.framework if bstack111ll1111_opy_.framework != None else bstack1111l_opy_ (u"ࠤࠥฉ")
      config = yaml.safe_load(bstack11l111l11_opy_)
      config[bstack1111l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪช")] = bstack1111l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱ࡸ࡫ࡴࡶࡲࠪซ")
      bstack111lll1l_opy_(bstack1l1ll1l111_opy_, config)
    except Exception as e:
      logger.debug(bstack1l111ll111_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1111lll11_opy_.format(str(e)))
def bstack111lll1l_opy_(bstack111lll11l_opy_, config, bstack1lllll111_opy_=None, bstack1111l1l1l1_opy_=False):
  global BROWSERSTACK_AUTOMATION
  global bstack1l111ll1ll_opy_
  global global_config
  if not config:
    return
  if bstack1lllll111_opy_ is None:
    bstack1lllll111_opy_ = {}
  bstack1l11llll1_opy_ = bstack1l111lll_opy_ if not BROWSERSTACK_AUTOMATION else (
    bstack1l11l1111_opy_ if bstack1111l_opy_ (u"ࠬࡧࡰࡱࠩฌ") in config else (
        bstack11ll1l11_opy_ if config.get(bstack1111l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪญ")) else bstack1l11l11l_opy_
    )
)
  bstack1ll1111111_opy_ = False
  bstack111llllll1_opy_ = False
  if BROWSERSTACK_AUTOMATION is True:
      if bstack1111l_opy_ (u"ࠧࡢࡲࡳࠫฎ") in config:
          bstack1ll1111111_opy_ = True
      else:
          bstack111llllll1_opy_ = True
  bstack11llll11_opy_ = TestHubUtils.bstack11l11l1111_opy_(config, bstack1l111ll1ll_opy_)
  bstack11l111ll1l_opy_ = bstack1111l1ll_opy_()
  data = {
    bstack1111l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪฏ"): config[bstack1111l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫฐ")],
    bstack1111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ฑ"): config[bstack1111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧฒ")],
    bstack1111l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩณ"): bstack111lll11l_opy_,
    bstack1111l_opy_ (u"࠭ࡤࡦࡶࡨࡧࡹ࡫ࡤࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪด"): os.environ.get(bstack1111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩต"), bstack1l111ll1ll_opy_),
    bstack1111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪถ"): bstack1ll11l11l1_opy_,
    bstack1111l_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯ࠫท"): bstack1111l111_opy_(),
    bstack1111l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭ธ"): {
      bstack1111l_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩน"): str(config[bstack1111l_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬบ")]) if bstack1111l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ป") in config else bstack1111l_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣผ"),
      bstack1111l_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧ࡙ࡩࡷࡹࡩࡰࡰࠪฝ"): sys.version,
      bstack1111l_opy_ (u"ࠩࡵࡩ࡫࡫ࡲࡳࡧࡵࠫพ"): bstack11ll11lll_opy_(os.environ.get(bstack1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬฟ"), bstack1l111ll1ll_opy_)),
      bstack1111l_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭ภ"): bstack1111l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬม"),
      bstack1111l_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧย"): bstack1l11llll1_opy_,
      bstack1111l_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬร"): bstack11llll11_opy_,
      bstack1111l_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡡࡸࡹ࡮ࡪࠧฤ"): os.environ[bstack1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧล")],
      bstack1111l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ฦ"): os.environ.get(bstack1111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ว"), bstack1l111ll1ll_opy_),
      bstack1111l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨศ"): bstack1lll11111l_opy_(os.environ.get(bstack1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨษ"), bstack1l111ll1ll_opy_)),
      bstack1111l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ส"): bstack11l111ll1l_opy_.get(bstack1111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ห")),
      bstack1111l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨฬ"): bstack11l111ll1l_opy_.get(bstack1111l_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫอ")),
      bstack1111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧฮ"): config[bstack1111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨฯ")] if config[bstack1111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩะ")] else bstack1111l_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣั"),
      bstack1111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪา"): str(config[bstack1111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫำ")]) if bstack1111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬิ") in config else bstack1111l_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧี"),
      bstack1111l_opy_ (u"ࠬࡵࡳࠨึ"): sys.platform,
      bstack1111l_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨื"): socket.gethostname(),
      bstack1111l_opy_ (u"ࠧࡪࡵࡆࡐࡎࡋ࡮ࡢࡤ࡯ࡩࡩุ࠭"): bstack1111l1l1l1_opy_,
      bstack1111l_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦูࠪ"): global_config.get_property(bstack1111l_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧฺࠫ"))
    }
  }
  if not global_config.get_property(bstack1111l_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪ฻")) is None:
    data[bstack1111l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧ฼")][bstack1111l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࡍࡦࡶࡤࡨࡦࡺࡡࠨ฽")] = {
      bstack1111l_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭฾"): bstack1111l_opy_ (u"ࠧࡶࡵࡨࡶࡤࡱࡩ࡭࡮ࡨࡨࠬ฿"),
      bstack1111l_opy_ (u"ࠨࡵ࡬࡫ࡳࡧ࡬ࠨเ"): global_config.get_property(bstack1111l_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩแ")),
      bstack1111l_opy_ (u"ࠪࡷ࡮࡭࡮ࡢ࡮ࡑࡹࡲࡨࡥࡳࠩโ"): global_config.get_property(bstack1111l_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡓࡵࠧใ"))
    }
  if bstack111lll11l_opy_ == bstack1l111llll1_opy_:
    data[bstack1111l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨไ")][bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡈࡵ࡮ࡧ࡫ࡪࠫๅ")] = bstack1ll1l11l11_opy_(config)
    data[bstack1111l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪๆ")][bstack1111l_opy_ (u"ࠨ࡫ࡶࡔࡪࡸࡣࡺࡃࡸࡸࡴࡋ࡮ࡢࡤ࡯ࡩࡩ࠭็")] = percy.bstack11ll1lll1_opy_
    data[bstack1111l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷ่ࠬ")][bstack1111l_opy_ (u"ࠪࡴࡪࡸࡣࡺࡄࡸ࡭ࡱࡪࡉࡥ้ࠩ")] = percy.percy_build_id
  if not bstack11ll11l11l_opy_.bstack1l1l11ll11_opy_(CONFIG):
    data[bstack1111l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹ๊ࠧ")][bstack1111l_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯๋ࠩ")] = bstack11ll11l11l_opy_.bstack1l1l11ll11_opy_(CONFIG)
  bstack11ll111ll_opy_ = bstack1l11lll1l1_opy_.get_instance(CONFIG, logger)
  bstack11llllll1_opy_ = bstack11ll11l11l_opy_.get_instance(config=CONFIG)
  if bstack11ll111ll_opy_ is not None and bstack11llllll1_opy_ is not None and bstack11llllll1_opy_.bstack11l111l1ll_opy_():
    data[bstack1111l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩ์")][bstack11llllll1_opy_.bstack11111l11l_opy_()] = bstack11ll111ll_opy_.bstack1l11l11111_opy_()
  update(data[bstack1111l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪํ")], bstack1lllll111_opy_)
  try:
    response = bstack1llll1ll1_opy_(bstack1111l_opy_ (u"ࠨࡒࡒࡗ࡙࠭๎"), bstack11lll1ll_opy_(bstack1l111l1111_opy_), data, {
      bstack1111l_opy_ (u"ࠩࡤࡹࡹ࡮ࠧ๏"): (config[bstack1111l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ๐")], config[bstack1111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ๑")])
    })
    if response:
      logger.debug(bstack11l11ll11_opy_.format(bstack111lll11l_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack11ll11l1_opy_.format(str(e)))
def bstack11ll11lll_opy_(framework):
  return bstack1111l_opy_ (u"ࠧࢁࡽ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࡻࡾࠤ๒").format(str(framework), __version__) if framework else bstack1111l_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࢀࢃࠢ๓").format(
    __version__)
def bstack111ll1llll_opy_():
  global CONFIG
  global bstack111l11lll1_opy_
  if bool(CONFIG):
    return
  try:
    bstack1l111ll1l1_opy_()
    logger.debug(bstack1l11l1ll_opy_.format(str(CONFIG)))
    bstack111l11lll1_opy_ = logger_utils.configure_logger(CONFIG, bstack111l11lll1_opy_)
    bstack11l1111ll_opy_()
  except Exception as e:
    logger.error(bstack1111l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱ࠮ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠦ๔") + str(e))
    sys.exit(1)
  sys.excepthook = bstack111ll1l1l_opy_
  atexit.register(bstack11l11l1l1_opy_)
  signal.signal(signal.SIGINT, bstack1l1llll11_opy_)
  signal.signal(signal.SIGTERM, bstack1l1llll11_opy_)
def bstack111ll1l1l_opy_(exctype, value, traceback):
  global bstack1l1lll1ll_opy_
  try:
    for driver in bstack1l1lll1ll_opy_:
      bstack1ll1111l1l_opy_(driver, bstack1111l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ๕"), bstack1111l_opy_ (u"ࠤࡖࡩࡸࡹࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧ๖") + str(value))
  except Exception:
    pass
  logger.info(bstack1lllllllll_opy_)
  bstack11l11l1ll1_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack11l11l1ll1_opy_(message=bstack1111l_opy_ (u"ࠪࠫ๗"), bstack111l1ll1ll_opy_ = False, bstack1111l1l1l1_opy_ = False):
  global CONFIG
  bstack11l1111111_opy_ = bstack1111l_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡉࡽࡩࡥࡱࡶ࡬ࡳࡳ࠭๘") if bstack111l1ll1ll_opy_ else bstack1111l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ๙")
  bstack1lll11lll_opy_ = bstack1l11ll1l1_opy_.bstack11ll11l1ll_opy_(EVENTS.bstack1l11111111_opy_)
  try:
    if message:
      bstack1lllll111_opy_ = {
        bstack11l1111111_opy_ : str(message)
      }
      try:
        bstack111lll1l_opy_(bstack1l111llll1_opy_, CONFIG, bstack1lllll111_opy_, bstack1111l1l1l1_opy_)
      finally:
        bstack1l11ll1l1_opy_.end(EVENTS.bstack1l11111111_opy_.value, bstack1lll11lll_opy_ + bstack1111l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ๚"), bstack1lll11lll_opy_ + bstack1111l_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ๛"), status=True, failure=None, test_name=None)
    else:
      try:
        bstack111lll1l_opy_(bstack1l111llll1_opy_, CONFIG, bstack1111l1l1l1_opy_=bstack1111l1l1l1_opy_)
      finally:
        bstack1l11ll1l1_opy_.end(EVENTS.bstack1l11111111_opy_.value, bstack1lll11lll_opy_ + bstack1111l_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ๜"), bstack1lll11lll_opy_ + bstack1111l_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ๝"), status=True, failure=None, test_name=None)
  except Exception as e:
    logger.debug(bstack111l1l1l_opy_.format(str(e)))
def bstack11llll11l_opy_(bstack11l1l111l_opy_, size):
  bstack1l1l11lll1_opy_ = []
  while len(bstack11l1l111l_opy_) > size:
    bstack1lll11l1_opy_ = bstack11l1l111l_opy_[:size]
    bstack1l1l11lll1_opy_.append(bstack1lll11l1_opy_)
    bstack11l1l111l_opy_ = bstack11l1l111l_opy_[size:]
  bstack1l1l11lll1_opy_.append(bstack11l1l111l_opy_)
  return bstack1l1l11lll1_opy_
def bstack1111llll1l_opy_(args):
  if bstack1111l_opy_ (u"ࠪ࠱ࡲ࠭๞") in args and bstack1111l_opy_ (u"ࠫࡵࡪࡢࠨ๟") in args:
    return True
  return False
@measure(event_name=EVENTS.bstack111l11111l_opy_, stage=STAGE.bstack1lll1l11ll_opy_)
def run_on_browserstack(bstack1l1llll1ll_opy_=None, bstack1ll1ll11l1_opy_=None, bstack111llll1l_opy_=False):
  global CONFIG
  global bstack11l11lll11_opy_
  global bstack1l1111111l_opy_
  global bstack1l111ll1ll_opy_
  global global_config
  bstack11l11l11ll_opy_ = bstack1111l_opy_ (u"ࠬ࠭๠")
  bstack1l1l111lll_opy_ = bstack1111l_opy_ (u"ࠨࠢ๡")
  bstack11ll1l11l1_opy_(bstack11l1llll1_opy_, logger)
  if bstack1l1llll1ll_opy_ and isinstance(bstack1l1llll1ll_opy_, str):
    bstack1l1llll1ll_opy_ = eval(bstack1l1llll1ll_opy_)
  if bstack1l1llll1ll_opy_:
    CONFIG = bstack1l1llll1ll_opy_[bstack1111l_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧ๢")]
    bstack11l11lll11_opy_ = bstack1l1llll1ll_opy_[bstack1111l_opy_ (u"ࠨࡊࡘࡆࡤ࡛ࡒࡍࠩ๣")]
    bstack1l1111111l_opy_ = bstack1l1llll1ll_opy_[bstack1111l_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ๤")]
    global_config.bstack1ll1111l11_opy_(bstack1111l_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ๥"), bstack1l1111111l_opy_)
    bstack11l11l11ll_opy_ = bstack1111l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠬ๦")
  global_config.bstack1ll1111l11_opy_(bstack1111l_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪࠧ๧"), uuid4().__str__())
  logger.info(bstack1111l_opy_ (u"࠭ࡓࡅࡍࠣࡶࡺࡴࠠࡴࡶࡤࡶࡹ࡫ࡤࠡࡹ࡬ࡸ࡭ࠦࡩࡥ࠼ࠣࠫ๨") + global_config.get_property(bstack1111l_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥࠩ๩")));
  logger.debug(bstack1111l_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࡀࠫ๪") + global_config.get_property(bstack1111l_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫ๫")))
  if not bstack111llll1l_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack11ll1ll11_opy_)
      return
    if sys.argv[1] == bstack1111l_opy_ (u"ࠪ࠱࠲ࡼࡥࡳࡵ࡬ࡳࡳ࠭๬") or sys.argv[1] == bstack1111l_opy_ (u"ࠫ࠲ࡼࠧ๭"):
      logger.info(bstack1111l_opy_ (u"ࠬࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡕࡿࡴࡩࡱࡱࠤࡘࡊࡋࠡࡸࡾࢁࠬ๮").format(__version__))
      return
    if sys.argv[1] == bstack1111l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ๯"):
      bstack1111llll11_opy_()
      return
    if sys.argv[1] == bstack1111l_opy_ (u"ࠧ࡭ࡱࡤࡨࠬ๰"):
      from browserstack_sdk.bstack111l111l1l_opy_ import bstack1lllll1111_opy_
      bstack111ll1llll_opy_()
      bstack1lllll1111_opy_(CONFIG)
      return
  args = sys.argv
  bstack111ll1llll_opy_()
  global bstack11l1l1l1l_opy_
  try:
    from bstack_utils import constants as bstack1l1llll1l_opy_
    override_value = CONFIG.get(bstack1111l_opy_ (u"ࠨࡱࡹࡩࡷࡸࡩࡥࡧࡏࡳࡦࡪࡔࡦࡵࡷ࡭ࡳ࡭ࠧ๱"), False)
    bstack11l1l1l1l_opy_ = bool(override_value)
  except Exception as e:
    logger.error(bstack1111l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡏࡗࡇࡕࡖࡎࡊࡅࡠࡎࡒࡅࡉࡥࡔࡆࡕࡗࡍࡓࡍ࠺ࠡࡽࢀࠦ๲").format(e))
    bstack11l1l1l1l_opy_ = False
  if bstack11l1l1l1l_opy_:
    bstack1l1l111l_opy_ = CONFIG.get(bstack1111l_opy_ (u"ࠪࡰࡴࡧࡤࡕࡧࡶࡸ࡮ࡴࡧࡉࡷࡥ࡙ࡗࡒࠧ๳")) or bstack1l1llll1l_opy_.bstack111ll1ll1_opy_
    logger.info(bstack1111l_opy_ (u"ࠦࡌࡲ࡯ࡣࡣ࡯ࠤࡴࡼࡥࡳࡴ࡬ࡨࡪࡲ࡯ࡢࡦࡷࡩࡸࡺࡩ࡯ࡩࠣࡩࡳࡧࡢ࡭ࡧࡧ࠰ࠥࡻࡳࡪࡰࡪࠤ࡭ࡻࡢ࠻ࠢࡾࢁࠧ๴").format(bstack1l1l111l_opy_))
    bstack11l11lll11_opy_ = bstack1l1l111l_opy_
    try:
      bstack1l1llll1l_opy_.HTTPS_HUB = bstack1l1l111l_opy_
      bstack1l1llll1l_opy_.bstack11l1l111l1_opy_ = bstack1l1l111l_opy_
    except Exception:
      pass
  global bstack111l1l11_opy_
  global bstack11l1llll11_opy_
  global PARALLELISE_VANILLA_PYTHON
  global PARALLELISE_THREADING_PYTHON
  global PLATFORM_INDEX
  global bstack1l1l111ll_opy_
  global bstack111ll111l1_opy_
  global bstack11l11l1l1l_opy_
  global bstack11ll111l_opy_
  global bstack1l1l11llll_opy_
  global bstack1ll1111ll1_opy_
  bstack11l1llll11_opy_ = len(CONFIG.get(bstack1111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ๵"), []))
  if not bstack11l11l11ll_opy_:
    if args[1] == bstack1111l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭๶") or args[1] == bstack1111l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨ๷") or args[1] == bstack1111l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩ๸"):
      bstack11l11l11ll_opy_ = bstack1111l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠪ๹")
      args = args[2:]
    elif args[1] == bstack1111l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ๺"):
      bstack11l11l11ll_opy_ = bstack1111l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ๻")
      args = args[2:]
    elif args[1] == bstack1111l_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ๼"):
      bstack11l11l11ll_opy_ = bstack1111l_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ๽")
      args = args[2:]
    elif args[1] == bstack1111l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ๾"):
      bstack11l11l11ll_opy_ = bstack1111l_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ๿")
      args = args[2:]
    elif args[1] == bstack1111l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ຀"):
      bstack11l11l11ll_opy_ = bstack1111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪກ")
      args = args[2:]
    elif args[1] == bstack1111l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫຂ"):
      bstack11l11l11ll_opy_ = bstack1111l_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ຃")
      args = args[2:]
    else:
      if not bstack1111l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩຄ") in CONFIG or str(CONFIG[bstack1111l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ຅")]).lower() in [bstack1111l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨຆ"), bstack1111l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪງ"), bstack1111l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠫຈ")]:
        bstack11l11l11ll_opy_ = bstack1111l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠬຉ")
        args = args[1:]
      elif str(CONFIG[bstack1111l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨຊ")]).lower() == bstack1111l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ຋"):
        bstack11l11l11ll_opy_ = bstack1111l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ຌ")
        args = args[1:]
      elif str(CONFIG[bstack1111l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫຍ")]).lower() == bstack1111l_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨຎ"):
        bstack11l11l11ll_opy_ = bstack1111l_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩຏ")
        args = args[1:]
      elif str(CONFIG[bstack1111l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧຐ")]).lower() == bstack1111l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬຑ"):
        bstack11l11l11ll_opy_ = bstack1111l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ຒ")
        args = args[1:]
      elif str(CONFIG[bstack1111l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪຓ")]).lower() == bstack1111l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨດ"):
        bstack11l11l11ll_opy_ = bstack1111l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩຕ")
        args = args[1:]
      else:
        os.environ[bstack1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬຖ")] = bstack11l11l11ll_opy_
        bstack111llll1ll_opy_(bstack1ll11ll1ll_opy_)
  os.environ[bstack1111l_opy_ (u"ࠫࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ࡟ࡖࡕࡈࡈࠬທ")] = bstack11l11l11ll_opy_
  bstack1l111ll1ll_opy_ = bstack11l11l11ll_opy_
  if cli.is_enabled(CONFIG):
    try:
      if bstack11l11l11ll_opy_ == bstack1111l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬຘ") and bstack111ll11ll1_opy_():
        bstack1l1l1111ll_opy_ = bstack11lll11ll1_opy_[bstack1111l_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙࠳ࡂࡅࡆࠪນ")]
      elif bstack11l11l11ll_opy_ in [bstack1111l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨບ"), bstack1111l_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧປ")]:
        bstack1l1l1111ll_opy_ = bstack1111l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨຜ")
      else:
        bstack1l1l1111ll_opy_ = bstack11l11l11ll_opy_
      bstack1111ll11_opy_.invoke(Events.bstack11l111ll1_opy_, bstack1ll11ll111_opy_(
        sdk_version=__version__,
        path_config=bstack111l1l1lll_opy_(),
        path_project=os.getcwd(),
        test_framework=bstack1l1l1111ll_opy_,
        frameworks=[bstack1l1l1111ll_opy_],
        framework_versions={
          bstack1l1l1111ll_opy_: bstack1lll11111l_opy_(bstack1111l_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩຝ") if bstack11l11l11ll_opy_ in [bstack1111l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪພ"), bstack1111l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫຟ"), bstack1111l_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧຠ")] else bstack11l11l11ll_opy_)
        },
        bs_config=CONFIG
      ))
      if cli.config and cli.config.get(bstack1111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤມ"), None):
        CONFIG[bstack1111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠥຢ")] = cli.config.get(bstack1111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠦຣ"), None)
    except Exception as e:
      bstack1111ll11_opy_.invoke(Events.bstack1l1llllll_opy_, e.__traceback__, 1)
    if bstack1l1111111l_opy_:
      CONFIG[bstack1111l_opy_ (u"ࠥࡥࡵࡶࠢ຤")] = cli.config[bstack1111l_opy_ (u"ࠦࡦࡶࡰࠣລ")]
      logger.info(bstack11l1llllll_opy_.format(CONFIG[bstack1111l_opy_ (u"ࠬࡧࡰࡱࠩ຦")]))
  else:
    bstack1111ll11_opy_.clear()
  global bstack111l11l1l_opy_
  global bstack1l1l1l1l1l_opy_
  if bstack1l1llll1ll_opy_:
    try:
      bstack1lll1l11l_opy_ = datetime.datetime.now()
      os.environ[bstack1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨວ")] = bstack11l11l11ll_opy_
      bstack1ll1lll111_opy_ = bstack1l11ll1l1_opy_.bstack11ll11l1ll_opy_(EVENTS.bstack1l1ll1lll_opy_)
      try:
        logger.info(bstack1111l_opy_ (u"ࠢࡔࡧࡱࡨ࡮ࡴࡧࠡࡕࡇࡏ࡚ࠥࡥࡴࡶࠣࡅࡹࡺࡥ࡮ࡲࡷࡩࡩࠦࡥࡷࡧࡱࡸࠧຨ"))
        bstack111lll1l_opy_(bstack1lll111l1_opy_, CONFIG)
      finally:
        bstack1l11ll1l1_opy_.end(EVENTS.bstack1l1ll1lll_opy_.value, bstack1ll1lll111_opy_ + bstack1111l_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣຩ"), bstack1ll1lll111_opy_ + bstack1111l_opy_ (u"ࠤ࠽ࡩࡳࡪࠢສ"), status=True, failure=None, test_name=None)
      cli.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻ࡵࡧ࡯ࡤࡺࡥࡴࡶࡢࡥࡹࡺࡥ࡮ࡲࡷࡩࡩࠨຫ"), datetime.datetime.now() - bstack1lll1l11l_opy_)
    except Exception as e:
      logger.debug(bstack1111l1l1_opy_.format(str(e)))
  global bstack1ll1l1ll_opy_
  global bstack11l1ll11l_opy_
  global bstack1ll11l1l1l_opy_
  global bstack1l111l1ll_opy_
  global bstack1llll111l_opy_
  global bstack11llll1ll_opy_
  global bstack1lllllll1_opy_
  global bstack1l1ll1111_opy_
  global bstack1111ll1l1l_opy_
  global bstack1ll1l11ll1_opy_
  global bstack1111111l_opy_
  global bstack11l11l11l1_opy_
  global bstack1llll1l1l_opy_
  global bstack1l11l1l11_opy_
  global bstack1l1l111ll1_opy_
  global bstack11l11lll1_opy_
  global bstack1l1l111l1l_opy_
  global bstack1l11l1l1_opy_
  global bstack1ll1l1111_opy_
  global bstack111l11ll11_opy_
  global bstack11ll11ll1l_opy_
  global bstack1ll11l11ll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1ll1l1ll_opy_ = webdriver.Remote.__init__
    bstack11l1ll11l_opy_ = WebDriver.quit
    bstack11l11l11l1_opy_ = WebDriver.close
    bstack11l11lll1_opy_ = WebDriver.get
    bstack1ll11l11ll_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack111l11l1l_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack1l11ll1ll_opy_
    bstack1l1l1l1l1l_opy_ = bstack1l11ll1ll_opy_()
  except Exception as e:
    pass
  try:
    global bstack1l1ll1ll11_opy_
    from QWeb.keywords import browser
    bstack1l1ll1ll11_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1ll1l1l11l_opy_(CONFIG) and bstack1l11ll1111_opy_():
    if bstack1l1ll1ll1l_opy_() < version.parse(bstack11l11ll1_opy_):
      logger.error(bstack1ll1lllll1_opy_.format(bstack1l1ll1ll1l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack1111l_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬຬ")) and callable(getattr(RemoteConnection, bstack1111l_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭ອ"))):
          RemoteConnection._get_proxy_url = bstack1111l11ll1_opy_
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          ClientConfig.get_proxy_url = bstack1111l11ll1_opy_
      except Exception as e:
        logger.error(bstack111l1lllll_opy_.format(str(e)))
  if not CONFIG.get(bstack1111l_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨຮ"), False) and not bstack1l1llll1ll_opy_:
    logger.info(bstack1ll11lll1_opy_)
  bstack11ll1l1ll_opy_ = not cli.is_enabled(CONFIG) and bstack11l11l11ll_opy_ not in [bstack1111l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨຯ")]
  bstack1lll11ll1_opy_ = bstack11ll1l1ll_opy_ and bstack1111l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬະ") in CONFIG and str(CONFIG[bstack1111l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ັ")]).lower() != bstack1111l_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩາ")
  bstack11l1l1lll_opy_ = bstack11ll1l1ll_opy_ and not bstack1lll11ll1_opy_ and (bstack11l11l11ll_opy_ != bstack1111l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠬຳ") or (bstack11l11l11ll_opy_ == bstack1111l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨ࠭ິ") and not bstack1l1llll1ll_opy_))
  if bstack11l11l11ll_opy_ not in [bstack1111l_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧີ")]:
    bstack11ll1l11l1_opy_(os.path.join(os.getcwd(), bstack1111l_opy_ (u"ࠧ࡭ࡱࡪࠫຶ"), bstack1111l_opy_ (u"ࠨ࡭ࡨࡽ࠲ࡳࡥࡵࡴ࡬ࡧࡸ࠴ࡪࡴࡱࡱࠫື")), logger)
  if (bstack11l11l11ll_opy_ in [bstack1111l_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨຸ"), bstack1111l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵູࠩ"), bstack1111l_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰ຺ࠬ")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      try:
        from pabot.pabot import QueueItem
        from pabot import pabot
      except Exception as e:
        logger.warning(bstack11l1ll1l1_opy_ + str(e))
      if not is_robot_playwright_installed():
        try:
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
          WebDriverCreator._get_ff_profile = bstack1lll1l1ll1_opy_
          bstack11llll1ll_opy_ = WebDriverCache.close
        except Exception as e:
          logger.warning(bstack1l1llllll1_opy_ + str(e))
        try:
          from AppiumLibrary.utils.applicationcache import ApplicationCache
          bstack1llll111l_opy_ = ApplicationCache.close
        except Exception as e:
          logger.debug(bstack1ll1l11l1l_opy_ + str(e))
    except Exception as e:
      bstack11ll1ll11l_opy_(e, bstack1l1llllll1_opy_)
    if bstack11l11l11ll_opy_ != bstack1111l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ົ"):
      bstack1ll1l11111_opy_()
    bstack1ll11l1l1l_opy_ = Output.start_test
    bstack1l111l1ll_opy_ = Output.end_test
    bstack1lllllll1_opy_ = TestStatus.__init__
    bstack1111ll1l1l_opy_ = pabot._run
    bstack1ll1l11ll1_opy_ = QueueItem.__init__
    bstack1111111l_opy_ = pabot._create_command_for_execution
    bstack111l11ll11_opy_ = pabot._report_results
  if bstack11l11l11ll_opy_ == bstack1111l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ຼ"):
    global bstack11ll1lll_opy_
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11ll1ll11l_opy_(e, bstack1111l111l1_opy_)
    bstack1llll1l1l_opy_ = Runner.run_hook
    bstack1l11l1l11_opy_ = Runner.load_hooks
    bstack1l1l111ll1_opy_ = Step.run
    try:
      sig = inspect.signature(bstack1llll1l1l_opy_)
      params = list(sig.parameters.keys())
      bstack11ll1lll_opy_ = bstack1111l_opy_ (u"ࠧࡤࡱࡱࡸࡪࡾࡴࠨຽ") in params
      logger.info(bstack1111l_opy_ (u"ࠨࡆࡨࡸࡪࡩࡴࡦࡦࠣࡦࡪ࡮ࡡࡷࡧࠣࡶࡺࡴ࡟ࡩࡱࡲ࡯ࠥࡹࡩࡨࡰࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬ຾").format(bstack1111l_opy_ (u"ࠩ࠴࠲࠷࠴࠶ࠡࠪࡺ࡭ࡹ࡮ࠠࡤࡱࡱࡸࡪࡾࡴࠪࠩ຿") if bstack11ll1lll_opy_ else bstack1111l_opy_ (u"ࠪ࠵࠳࠹ࠫࠡࠪࡺ࡭ࡹ࡮࡯ࡶࡶࠣࡧࡴࡴࡴࡦࡺࡷ࠭ࠬເ")))
    except Exception as e:
      logger.debug(bstack1111l_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡨࡺࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡳࡷࡱࡣ࡭ࡵ࡯࡬ࠢࡶ࡭࡬ࡴࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩແ").format(str(e)))
      bstack11ll1lll_opy_ = None
  if bstack11l11l11ll_opy_ == bstack1111l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬໂ"):
    try:
      from _pytest.config import Config
      bstack1l11l1l1_opy_ = Config.getoption
      from _pytest import runner
      bstack1ll1l1111_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warning(bstack1111l_opy_ (u"ࠨࠥࡴ࠼ࠣࠩࡸࠨໃ"), bstack111ll11l11_opy_, str(e))
    try:
      from pytest_bdd import reporting
      bstack11ll11ll1l_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1111l_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨໄ"))
    if bstack1ll1l1l1_opy_():
      logger.warning(bstack1llll1l1_opy_[bstack1111l_opy_ (u"ࠨࡕࡇࡏ࠲ࡍࡅࡏ࠯࠳࠴࠺࠭໅")])
  try:
    framework_name = bstack1111l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨໆ") if bstack11l11l11ll_opy_ in [bstack1111l_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ໇"), bstack1111l_opy_ (u"ࠫࡷࡵࡢࡰࡶ່ࠪ"), bstack1111l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ້࠭")] else bstack1111ll11l1_opy_(bstack11l11l11ll_opy_)
    bstack1ll111l111_opy_ = {
      bstack1111l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫໊ࠧ"): bstack1111l_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳ໋ࠩ") if bstack11l11l11ll_opy_ == bstack1111l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ໌") and bstack111ll11ll1_opy_() else framework_name,
      bstack1111l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ໍ"): bstack1lll11111l_opy_(framework_name),
      bstack1111l_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ໎"): __version__,
      bstack1111l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬ໏"): bstack11l11l11ll_opy_
    }
    if bstack11l11l11ll_opy_ in bstack1ll1l1ll11_opy_ + bstack111l1ll111_opy_:
      if a11y.is_enabled_root(CONFIG):
        if bstack1111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ໐") in CONFIG:
          os.environ[bstack1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ໑")] = os.getenv(bstack1111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ໒"), json.dumps(CONFIG[bstack1111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ໓")]))
          CONFIG[bstack1111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ໔")].pop(bstack1111l_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨ໕"), None)
          CONFIG[bstack1111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ໖")].pop(bstack1111l_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ໗"), None)
        bstack11ll1l111l_opy_ = bstack1111l_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪ໘") if CONFIG.get(bstack1111l_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭໙")) or bstack1l1l1l1l11_opy_() else bstack1111l_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࠪ໚")
        if bstack11ll1l111l_opy_ == bstack1111l_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭໛"):
          try:
            import importlib.metadata as _11l111l11l_opy_
            bstack1l1ll111l_opy_ = _11l111l11l_opy_.version(bstack1111l_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢໜ"))
          except Exception:
            bstack1l1ll111l_opy_ = bstack1111l_opy_ (u"ࠫࡺࡴ࡫࡯ࡱࡺࡲࠬໝ")
        else:
          bstack1l1ll111l_opy_ = str(bstack1l1ll1ll1l_opy_())
        bstack1ll111l111_opy_[bstack1111l_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬໞ")] = {
          bstack1111l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫໟ"): bstack11ll1l111l_opy_,
          bstack1111l_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨ໠"): bstack1l1ll111l_opy_
        }
    bstack11ll1lll11_opy_, bstack11111ll11_opy_ = None, {}
    bstack1l1ll1l1ll_opy_ = None
    bstack1l111l11l1_opy_ = None
    def bstack1111l1l11l_opy_():
      if bstack1lll11ll1_opy_:
        bstack111l111l11_opy_()
      elif bstack11l1l1lll_opy_:
        bstack1lll1ll11l_opy_()
    def bstack111l1lll11_opy_():
      nonlocal bstack11ll1lll11_opy_, bstack11111ll11_opy_
      if bstack11l11l11ll_opy_ not in [bstack1111l_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ໡")] and not cli.is_running():
        bstack11ll1lll11_opy_, bstack11111ll11_opy_ = TestHubHandler.launch(CONFIG, bstack1ll111l111_opy_)
    if bstack1lll11ll1_opy_ or bstack11l1l1lll_opy_:
      bstack1l1ll1l1ll_opy_ = threading.Thread(target=bstack1111l1l11l_opy_)
      bstack1l1ll1l1ll_opy_.start()
    if bstack11l11l11ll_opy_ not in [bstack1111l_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ໢")] and not cli.is_running():
      bstack1l111l11l1_opy_ = threading.Thread(target=bstack111l1lll11_opy_)
      bstack1l111l11l1_opy_.start()
    if bstack1l1ll1l1ll_opy_:
      bstack1l1ll1l1ll_opy_.join()
    if bstack1l111l11l1_opy_:
      bstack1l111l11l1_opy_.join()
    if bstack11111ll11_opy_.get(bstack1111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ໣")) is not None and a11y.bstack1l1l1l1ll1_opy_(CONFIG) is None:
      value = bstack11111ll11_opy_[bstack1111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ໤")].get(bstack1111l_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭໥"))
      if value is not None:
          CONFIG[bstack1111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭໦")] = value
      else:
        logger.debug(bstack1111l_opy_ (u"ࠢࡏࡱࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡨࡦࡺࡡࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡶࡪࡹࡰࡰࡰࡶࡩࠧ໧"))
  except Exception as e:
    logger.debug(bstack111llll11l_opy_.format(bstack1111l_opy_ (u"ࠨࡖࡨࡷࡹࡎࡵࡣࠩ໨"), str(e)))
  if bstack11l11l11ll_opy_ == bstack1111l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠪ໩"):
    PARALLELISE_VANILLA_PYTHON = True
    if bstack1l1llll1ll_opy_ and bstack111llll1l_opy_:
      if cli.is_enabled(CONFIG):
        bstack1l1l111ll_opy_ = cli.config.get(bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ໪"), {}).get(bstack1111l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭໫")) if cli.config else None
      else:
        bstack1l1l111ll_opy_ = CONFIG.get(bstack1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ໬"), {}).get(bstack1111l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ໭"))
      bstack111lllll1_opy_(bstack1l11lll11l_opy_)
    elif bstack1l1llll1ll_opy_:
      if cli.is_enabled(CONFIG):
        bstack1l1l111ll_opy_ = cli.config.get(bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ໮"), {}).get(bstack1111l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ໯")) if cli.config else None
      else:
        bstack1l1l111ll_opy_ = CONFIG.get(bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭໰"), {}).get(bstack1111l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ໱"))
      global bstack1l1lll1ll_opy_
      try:
        if bstack1111llll1l_opy_(bstack1l1llll1ll_opy_[bstack1111l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ໲")]) and multiprocessing.current_process().name == bstack1111l_opy_ (u"ࠬ࠶ࠧ໳"):
          bstack1l1llll1ll_opy_[bstack1111l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ໴")].remove(bstack1111l_opy_ (u"ࠧ࠮࡯ࠪ໵"))
          bstack1l1llll1ll_opy_[bstack1111l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ໶")].remove(bstack1111l_opy_ (u"ࠩࡳࡨࡧ࠭໷"))
          bstack1l1llll1ll_opy_[bstack1111l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭໸")] = bstack1l1llll1ll_opy_[bstack1111l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ໹")][0]
          with open(bstack1l1llll1ll_opy_[bstack1111l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ໺")], bstack1111l_opy_ (u"࠭ࡲࠨ໻")) as f:
            file_content = f.read()
          bstack1llll11l11_opy_ = bstack1111l_opy_ (u"ࠢࠣࠤࡩࡶࡴࡳࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡳࡥ࡭ࠣ࡭ࡲࡶ࡯ࡳࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪࡁࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡧࠫࡿࢂ࠯࠻ࠡࡨࡵࡳࡲࠦࡰࡥࡤࠣ࡭ࡲࡶ࡯ࡳࡶࠣࡔࡩࡨ࠻ࠡࡱࡪࡣࡩࡨࠠ࠾ࠢࡓࡨࡧ࠴ࡤࡰࡡࡥࡶࡪࡧ࡫࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡪࡥࡧࠢࡰࡳࡩࡥࡢࡳࡧࡤ࡯࠭ࡹࡥ࡭ࡨ࠯ࠤࡦࡸࡧ࠭ࠢࡷࡩࡲࡶ࡯ࡳࡣࡵࡽࠥࡃࠠ࠱ࠫ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡷࡶࡾࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡢࡴࡪࠤࡂࠦࡳࡵࡴࠫ࡭ࡳࡺࠨࡢࡴࡪ࠭࠰࠷࠰ࠪࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡦࡺࡦࡩࡵࡺࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡥࡸࠦࡥ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡳࡥࡸࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡵࡧࡠࡦࡥࠬࡸ࡫࡬ࡧ࠮ࡤࡶ࡬࠲ࡴࡦ࡯ࡳࡳࡷࡧࡲࡺࠫࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡐࡥࡤ࠱ࡨࡴࡥࡢࠡ࠿ࠣࡱࡴࡪ࡟ࡣࡴࡨࡥࡰࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡓࡨࡧ࠴ࡤࡰࡡࡥࡶࡪࡧ࡫ࠡ࠿ࠣࡱࡴࡪ࡟ࡣࡴࡨࡥࡰࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡓࡨࡧ࠮ࠩ࠯ࡵࡨࡸࡤࡺࡲࡢࡥࡨࠬ࠮ࡢ࡮ࠣࠤࠥ໼").format(str(bstack1l1llll1ll_opy_))
          bstack1l1l1111l1_opy_ = bstack1llll11l11_opy_ + file_content
          bstack11ll11llll_opy_ = bstack1l1llll1ll_opy_[bstack1111l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ໽")] + bstack1111l_opy_ (u"ࠩࡢࡦࡸࡺࡡࡤ࡭ࡢࡸࡪࡳࡰ࠯ࡲࡼࠫ໾")
          with open(bstack11ll11llll_opy_, bstack1111l_opy_ (u"ࠪࡻࠬ໿")):
            pass
          with open(bstack11ll11llll_opy_, bstack1111l_opy_ (u"ࠦࡼ࠱ࠢༀ")) as f:
            f.write(bstack1l1l1111l1_opy_)
          import subprocess
          bstack1lll1l1111_opy_ = subprocess.run([bstack1111l_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࠧ༁"), bstack11ll11llll_opy_])
          if os.path.exists(bstack11ll11llll_opy_):
            os.unlink(bstack11ll11llll_opy_)
          os._exit(bstack1lll1l1111_opy_.returncode)
        else:
          if bstack1111llll1l_opy_(bstack1l1llll1ll_opy_[bstack1111l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ༂")]):
            bstack1l1llll1ll_opy_[bstack1111l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ༃")].remove(bstack1111l_opy_ (u"ࠨ࠯ࡰࠫ༄"))
            bstack1l1llll1ll_opy_[bstack1111l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ༅")].remove(bstack1111l_opy_ (u"ࠪࡴࡩࡨࠧ༆"))
            bstack1l1llll1ll_opy_[bstack1111l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ༇")] = bstack1l1llll1ll_opy_[bstack1111l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ༈")][0]
          bstack111lllll1_opy_(bstack1l11lll11l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1l1llll1ll_opy_[bstack1111l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ༉")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1111l_opy_ (u"ࠧࡠࡡࡱࡥࡲ࡫࡟ࡠࠩ༊")] = bstack1111l_opy_ (u"ࠨࡡࡢࡱࡦ࡯࡮ࡠࡡࠪ་")
          mod_globals[bstack1111l_opy_ (u"ࠩࡢࡣ࡫࡯࡬ࡦࡡࡢࠫ༌")] = os.path.abspath(bstack1l1llll1ll_opy_[bstack1111l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭།")])
          exec(open(bstack1l1llll1ll_opy_[bstack1111l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ༎")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1111l_opy_ (u"ࠬࡉࡡࡶࡩ࡫ࡸࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠬ༏").format(str(e)))
          for driver in bstack1l1lll1ll_opy_:
            bstack1ll1ll11l1_opy_.append({
              bstack1111l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ༐"): bstack1l1llll1ll_opy_[bstack1111l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ༑")],
              bstack1111l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ༒"): str(e),
              bstack1111l_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ༓"): multiprocessing.current_process().name
            })
            bstack1ll1111l1l_opy_(driver, bstack1111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ༔"), bstack1111l_opy_ (u"ࠦࡘ࡫ࡳࡴ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢ༕") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1l1lll1ll_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1l1111111l_opy_, CONFIG, logger)
      bstack1l1ll11l11_opy_()
      bstack11llll1l1l_opy_()
      percy.bstack1l11lllll_opy_()
      bstack111lll1l11_opy_ = {
        bstack1111l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ༖"): args[0],
        bstack1111l_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭༗"): CONFIG,
        bstack1111l_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨ༘"): bstack11l11lll11_opy_,
        bstack1111l_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇ༙ࠪ"): bstack1l1111111l_opy_
      }
      if bstack1111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ༚") in CONFIG:
        bstack1llll1l11l_opy_ = bstack11111lll1_opy_(args, logger, CONFIG, BROWSERSTACK_AUTOMATION, bstack11l1llll11_opy_)
        bstack11l11l1l1l_opy_ = bstack1llll1l11l_opy_.bstack11ll1111_opy_(run_on_browserstack, bstack111lll1l11_opy_, bstack1111llll1l_opy_(args))
      else:
        if bstack1111llll1l_opy_(args):
          bstack111lll1l11_opy_[bstack1111l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭༛")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack111lll1l11_opy_,))
          test.start()
          test.join()
        else:
          bstack111lllll1_opy_(bstack1l11lll11l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1111l_opy_ (u"ࠫࡤࡥ࡮ࡢ࡯ࡨࡣࡤ࠭༜")] = bstack1111l_opy_ (u"ࠬࡥ࡟࡮ࡣ࡬ࡲࡤࡥࠧ༝")
          mod_globals[bstack1111l_opy_ (u"࠭࡟ࡠࡨ࡬ࡰࡪࡥ࡟ࠨ༞")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack11l11l11ll_opy_ == bstack1111l_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭༟") or bstack11l11l11ll_opy_ == bstack1111l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ༠"):
    percy.init(bstack1l1111111l_opy_, CONFIG, logger)
    percy.bstack1l11lllll_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack11ll1ll11l_opy_(e, bstack1l1llllll1_opy_)
    bstack1l1ll11l11_opy_()
    bstack111lllll1_opy_(bstack1ll1l111_opy_)
    if BROWSERSTACK_AUTOMATION:
      bstack11111lllll_opy_(bstack1ll1l111_opy_, args)
      if bstack1111l_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ༡") in args:
        i = args.index(bstack1111l_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨ༢"))
        args.pop(i)
        args.pop(i)
      if bstack1111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ༣") not in CONFIG:
        CONFIG[bstack1111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ༤")] = [{}]
        bstack11l1llll11_opy_ = 1
      if bstack111l1l11_opy_ == 0:
        bstack111l1l11_opy_ = 1
      args.insert(0, str(bstack111l1l11_opy_))
      args.insert(0, str(bstack1111l_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ༥")))
    if TestHubHandler.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack111111lll_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack111l1ll1l_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack1111l_opy_ (u"ࠢࡓࡑࡅࡓ࡙ࡥࡏࡑࡖࡌࡓࡓ࡙ࠢ༦"),
        ).parse_args(bstack111111lll_opy_)
        bstack111l1111l1_opy_ = args.index(bstack111111lll_opy_[0]) if len(bstack111111lll_opy_) > 0 else len(args)
        args.insert(bstack111l1111l1_opy_, str(bstack1111l_opy_ (u"ࠨ࠯࠰ࡰ࡮ࡹࡴࡦࡰࡨࡶࠬ༧")))
        args.insert(bstack111l1111l1_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡵࡳࡧࡵࡴࡠ࡮࡬ࡷࡹ࡫࡮ࡦࡴ࠱ࡴࡾ࠭༨"))))
        if bstack11ll11l11l_opy_.bstack11lllll111_opy_(CONFIG):
          args.insert(bstack111l1111l1_opy_, str(bstack1111l_opy_ (u"ࠪ࠱࠲ࡲࡩࡴࡶࡨࡲࡪࡸࠧ༩")))
          args.insert(bstack111l1111l1_opy_ + 1, str(bstack1111l_opy_ (u"ࠫࡗ࡫ࡴࡳࡻࡉࡥ࡮ࡲࡥࡥ࠼ࡾࢁࠬ༪").format(bstack11ll11l11l_opy_.bstack1l11l11l1l_opy_(CONFIG))))
        if bstack1ll111llll_opy_(os.environ.get(bstack1111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࠪ༫"))) and str(os.environ.get(bstack1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࡣ࡙ࡋࡓࡕࡕࠪ༬"), bstack1111l_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ༭"))) != bstack1111l_opy_ (u"ࠨࡰࡸࡰࡱ࠭༮"):
          for bstack11lll1lll1_opy_ in bstack111l1ll1l_opy_:
            args.remove(bstack11lll1lll1_opy_)
          test_files = os.environ.get(bstack1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭༯")).split(bstack1111l_opy_ (u"ࠪ࠰ࠬ༰"))
          for bstack1l111lll1_opy_ in test_files:
            args.append(bstack1l111lll1_opy_)
      except Exception as e:
        logger.error(bstack1111l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡤࡸࡹࡧࡣࡩ࡫ࡱ࡫ࠥࡲࡩࡴࡶࡨࡲࡪࡸࠠࡧࡱࡵࠤࢀࢃ࠮ࠡࡇࡵࡶࡴࡸࠠ࠮ࠢࡾࢁࠧ༱").format(bstack1l1lllll1l_opy_, e))
    pabot.main(args)
  elif bstack11l11l11ll_opy_ == bstack1111l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭༲"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack11ll1ll11l_opy_(e, bstack1l1llllll1_opy_)
    for a in args:
      if bstack1111l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬ༳") in a:
        PLATFORM_INDEX = int(a.split(bstack1111l_opy_ (u"ࠧ࠻ࠩ༴"))[1])
      if bstack1111l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡅࡇࡉࡐࡔࡉࡁࡍࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖ༵ࠬ") in a:
        bstack1l1l111ll_opy_ = str(a.split(bstack1111l_opy_ (u"ࠩ࠽ࠫ༶"))[1])
      if bstack1111l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡆࡐࡎࡇࡒࡈࡕ༷ࠪ") in a:
        bstack111ll111l1_opy_ = str(a.split(bstack1111l_opy_ (u"ࠫ࠿࠭༸"))[1])
    bstack1111111ll_opy_ = None
    bstack11l1ll1lll_opy_ = None
    if bstack1111l_opy_ (u"ࠬ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻ༹ࠫ") in args:
      i = args.index(bstack1111l_opy_ (u"࠭࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠬ༺"))
      args.pop(i)
      bstack1111111ll_opy_ = args.pop(i)
    if bstack1111l_opy_ (u"ࠧ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࠪ༻") in args:
      i = args.index(bstack1111l_opy_ (u"ࠨ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࠫ༼"))
      args.pop(i)
      bstack11l1ll1lll_opy_ = args.pop(i)
    if bstack1111111ll_opy_ is not None:
      global bstack11lll1ll11_opy_
      bstack11lll1ll11_opy_ = bstack1111111ll_opy_
    if bstack11l1ll1lll_opy_ is not None and int(PLATFORM_INDEX) < 0:
      PLATFORM_INDEX = int(bstack11l1ll1lll_opy_)
    if cli.is_enabled(CONFIG):
      if cli.bstack11l1l111_opy_():
        bstack1111ll11_opy_.invoke(Events.CONNECT, bstack1lllll111l_opy_())
        cli.bstack1lll11llll_opy_(PLATFORM_INDEX)
      if cli.bstack1lllll1ll_opy_(bstack11l1l111ll_opy_):
        cli.bstack1ll1llll1l_opy_()
    bstack111lllll1_opy_(bstack1ll1l111_opy_)
    run_cli(args)
    if bstack1111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠭༽") in multiprocessing.current_process().__dict__.keys():
      for bstack11l1lll1ll_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1ll1ll11l1_opy_.append(bstack11l1lll1ll_opy_)
  elif bstack11l11l11ll_opy_ == bstack1111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ༾"):
    bstack1l11l1lll1_opy_ = bstack11l11llll1_opy_(args, logger, CONFIG, BROWSERSTACK_AUTOMATION)
    bstack1l11l1lll1_opy_.bstack1l1l1l11ll_opy_()
    bstack1l1ll11l11_opy_()
    PARALLELISE_THREADING_PYTHON = True
    bstack1l1l11llll_opy_ = bstack1l11l1lll1_opy_.bstack1ll111l1ll_opy_()
    bstack1l11l1lll1_opy_.bstack111lll1l11_opy_(bstack1111ll111_opy_)
    bstack1l11l1lll1_opy_.bstack111l1ll1l1_opy_()
    bstack1l1lllll_opy_(bstack11l11l11ll_opy_, CONFIG, bstack1l11l1lll1_opy_.bstack1l1ll1l1l1_opy_())
    bstack111l1l1ll1_opy_.end(EVENTS.bstack111l11111l_opy_.value, EVENTS.bstack111l11111l_opy_.value + bstack1111l_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ༿"), EVENTS.bstack111l11111l_opy_.value + bstack1111l_opy_ (u"ࠧࡀࡥ࡯ࡦࠥཀ"), status=True, failure=None, test_name=SESSION_NAME)
    bstack111l11llll_opy_ = bstack1l11l1lll1_opy_.bstack11ll1111_opy_(bstack1lll1l1l1_opy_, {
      bstack1111l_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭ཁ"): CONFIG,
      bstack1111l_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨག"): bstack11l11lll11_opy_,
      bstack1111l_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪགྷ"): bstack1l1111111l_opy_,
      bstack1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬང"): BROWSERSTACK_AUTOMATION,
      bstack1111l_opy_ (u"ࠪࡓ࡛ࡋࡒࡓࡋࡇࡉࡤࡒࡏࡂࡆࡢࡘࡊ࡙ࡔࡊࡐࡊࠫཅ"): bstack11l1l1l1l_opy_
    })
    if not bstack1l1llll1ll_opy_:
      bstack1l1l111lll_opy_ = bstack1l11ll1l1_opy_.bstack11ll11l1ll_opy_(EVENTS.bstack1l1l1l111l_opy_.value)
    try:
      bstack1l11llll11_opy_, bstack1111lll1_opy_ = map(list, zip(*bstack111l11llll_opy_))
      bstack11ll111l_opy_ = bstack1l11llll11_opy_[0]
      for status_code in bstack1111lll1_opy_:
        if status_code != 0:
          bstack1ll1111ll1_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack1111l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡣࡹࡩࠥ࡫ࡲࡳࡱࡵࡷࠥࡧ࡮ࡥࠢࡶࡸࡦࡺࡵࡴࠢࡦࡳࡩ࡫࠮ࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࠿ࠦࡻࡾࠤཆ").format(str(e)))
  elif bstack11l11l11ll_opy_ == bstack1111l_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬཇ"):
    try:
      from behave.__main__ import main as bstack1l11111l11_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack11ll1ll11l_opy_(e, bstack1111l111l1_opy_)
    bstack1l1ll11l11_opy_()
    PARALLELISE_THREADING_PYTHON = True
    bstack111ll11111_opy_ = 1
    if bstack1111l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭཈") in CONFIG:
      bstack111ll11111_opy_ = CONFIG[bstack1111l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧཉ")]
    if bstack1111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫཊ") in CONFIG:
      bstack1l1ll111_opy_ = int(bstack111ll11111_opy_) * int(len(CONFIG[bstack1111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬཋ")]))
    else:
      bstack1l1ll111_opy_ = int(bstack111ll11111_opy_)
    config = Configuration(args)
    bstack1ll1ll11ll_opy_ = config.paths
    if len(bstack1ll1ll11ll_opy_) == 0:
      import glob
      pattern = bstack1111l_opy_ (u"ࠪ࠮࠯࠵ࠪ࠯ࡨࡨࡥࡹࡻࡲࡦࠩཌ")
      bstack1ll1l1ll1_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1ll1l1ll1_opy_)
      config = Configuration(args)
      bstack1ll1ll11ll_opy_ = config.paths
    bstack1lll1l11_opy_ = [os.path.normpath(item) for item in bstack1ll1ll11ll_opy_]
    bstack11ll1l1l1_opy_ = [os.path.normpath(item) for item in args]
    bstack1ll11llll_opy_ = [item for item in bstack11ll1l1l1_opy_ if item not in bstack1lll1l11_opy_]
    import platform as pf
    if pf.system().lower() == bstack1111l_opy_ (u"ࠫࡼ࡯࡮ࡥࡱࡺࡷࠬཌྷ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1lll1l11_opy_ = [str(PurePosixPath(PureWindowsPath(bstack11l1ll1ll1_opy_)))
                    for bstack11l1ll1ll1_opy_ in bstack1lll1l11_opy_]
    bstack1l111111l_opy_ = []
    for spec in bstack1lll1l11_opy_:
      bstack1l1l1l1l1_opy_ = []
      bstack1l1l1l1l1_opy_ += bstack1ll11llll_opy_
      bstack1l1l1l1l1_opy_.append(spec)
      bstack1l111111l_opy_.append(bstack1l1l1l1l1_opy_)
    execution_items = []
    for bstack1l1l1l1l1_opy_ in bstack1l111111l_opy_:
      if bstack1111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨཎ") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack1111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩཏ")]):
          item = {}
          item[bstack1111l_opy_ (u"ࠧࡢࡴࡪࠫཐ")] = bstack1111l_opy_ (u"ࠨࠢࠪད").join(bstack1l1l1l1l1_opy_)
          item[bstack1111l_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨདྷ")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack1111l_opy_ (u"ࠪࡥࡷ࡭ࠧན")] = bstack1111l_opy_ (u"ࠫࠥ࠭པ").join(bstack1l1l1l1l1_opy_)
        item[bstack1111l_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫཕ")] = 0
        execution_items.append(item)
    bstack11l1ll11_opy_ = bstack11llll11l_opy_(execution_items, bstack1l1ll111_opy_)
    for execution_item in bstack11l1ll11_opy_:
      bstack1ll11l11_opy_ = []
      for item in execution_item:
        bstack1ll11l11_opy_.append(bstack1ll1lll1ll_opy_(name=str(item[bstack1111l_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬབ")]),
                                             target=bstack1lll1llll1_opy_,
                                             args=(item[bstack1111l_opy_ (u"ࠧࡢࡴࡪࠫབྷ")],)))
      for t in bstack1ll11l11_opy_:
        t.start()
      for t in bstack1ll11l11_opy_:
        t.join()
  else:
    bstack111llll1ll_opy_(bstack1ll11ll1ll_opy_)
  if not bstack1l1llll1ll_opy_:
    bstack1ll1l1l1l_opy_()
    if bstack1l1l111lll_opy_:
      bstack1l11ll1l1_opy_.end(EVENTS.bstack1l1l1l111l_opy_.value, bstack1l1l111lll_opy_ + bstack1111l_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣམ"), bstack1l1l111lll_opy_ + bstack1111l_opy_ (u"ࠤ࠽ࡩࡳࡪࠢཙ"), status=True, failure=None, test_name=None)
  logger_utils.bstack11l1l1l1_opy_()
def browserstack_initialize(bstack1l11lllll1_opy_=None):
  logger.info(bstack1111l_opy_ (u"ࠪࡖࡺࡴ࡮ࡪࡰࡪࠤࡘࡊࡋࠡࡹ࡬ࡸ࡭ࠦࡡࡳࡩࡶ࠾ࠥ࠭ཚ") + str(bstack1l11lllll1_opy_))
  run_on_browserstack(bstack1l11lllll1_opy_, None, True)
@measure(event_name=EVENTS.bstack1111l11111_opy_, stage=STAGE.bstack11lll111l_opy_, bstack11lll111_opy_=SESSION_NAME)
def bstack1ll1l1l1l_opy_():
  global CONFIG
  global bstack1l111ll1ll_opy_
  global bstack1ll1111ll1_opy_
  global bstack11l1l1111_opy_
  global global_config
  global _11l1ll11l1_opy_
  bstack111l11l1_opy_.bstack1ll1l1l111_opy_()
  _11l1ll11l1_opy_ = cli.is_running()
  if _11l1ll11l1_opy_:
    bstack1111ll11_opy_.invoke(Events.bstack1ll1l1lll_opy_)
  else:
    bstack11llllll1_opy_ = bstack11ll11l11l_opy_.get_instance(config=CONFIG)
    bstack11llllll1_opy_.bstack1l1llll111_opy_(CONFIG)
  hashed_id = None
  bstack11ll1l1l1l_opy_ = None
  def bstack1l111lllll_opy_():
    try:
      if bstack1l111ll1ll_opy_ == bstack1111l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫཛ"):
        if not cli.is_enabled(CONFIG):
          TestHubHandler.stop()
      else:
        TestHubHandler.stop()
    except Exception as e:
      logger.debug(bstack1111l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡸࡺ࡯ࡱࡲ࡬ࡲ࡬ࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࡽࢀࠦཛྷ").format(e))
  def bstack1ll11l1l11_opy_():
    try:
      if not cli.is_enabled(CONFIG):
        bstack11l11ll1l1_opy_.bstack11ll11l111_opy_()
    except Exception as e:
      logger.debug(bstack1111l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡶࡲࡪࡰࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࠦ࡬ࡪࡰ࡮࠾ࠥࢁࡽࠣཝ").format(e))
  def bstack1ll1l11ll_opy_():
    nonlocal hashed_id, bstack11ll1l1l1l_opy_
    try:
      if bstack1111l_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫཞ") in CONFIG and str(CONFIG[bstack1111l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬཟ")]).lower() != bstack1111l_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨའ"):
        hashed_id, bstack11ll1l1l1l_opy_ = bstack1ll1ll1ll_opy_()
      else:
        hashed_id, bstack11ll1l1l1l_opy_ = get_build_link()
    except Exception as e:
      logger.debug(bstack1111l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡦࡺ࡯࡬ࡥࠢ࡯࡭ࡳࡱ࠺ࠡࡽࢀࠦཡ").format(e))
  bstack11ll1ll1ll_opy_ = threading.Thread(target=bstack1l111lllll_opy_)
  bstack1ll11l11l_opy_ = threading.Thread(target=bstack1ll11l1l11_opy_)
  bstack111l1lll1l_opy_ = threading.Thread(target=bstack1ll1l11ll_opy_)
  threads = [bstack11ll1ll1ll_opy_, bstack1ll11l11l_opy_, bstack111l1lll1l_opy_]
  for thread in threads:
    try:
      thread.start()
    except Exception as e:
      logger.debug(bstack1111l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡷࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡺࡨࡳࡧࡤࡨࠥࢁࡽ࠻ࠢࡾࢁࠧར").format(thread.name, e))
  for thread in threads:
    try:
      thread.join()
    except Exception as e:
      logger.debug(bstack1111l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡯ࡵࡩ࡯࡫ࡱ࡫ࠥࡺࡨࡳࡧࡤࡨࠥࢁࡽ࠻ࠢࡾࢁࠧལ").format(thread.name, e))
  bstack11l1lll1l_opy_(hashed_id)
  logger.info(bstack1111l_opy_ (u"࠭ࡓࡅࡍࠣࡶࡺࡴࠠࡦࡰࡧࡩࡩࠦࡦࡰࡴࠣ࡭ࡩࡀࠧཤ") + global_config.get_property(bstack1111l_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥࠩཥ"), bstack1111l_opy_ (u"ࠨࠩས")) + bstack1111l_opy_ (u"ࠩ࠯ࠤࡹ࡫ࡳࡵࡪࡸࡦࠥ࡯ࡤ࠻ࠢࠪཧ") + os.getenv(bstack1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨཨ"), bstack1111l_opy_ (u"ࠫࠬཀྵ")))
  if hashed_id is not None and bstack1l11l1lll_opy_() != -1:
    sessions = bstack1llllll1ll_opy_(hashed_id)
    bstack11lll1l11_opy_(sessions, bstack11ll1l1l1l_opy_)
  if bstack1l111ll1ll_opy_ == bstack1111l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬཪ") and bstack1ll1111ll1_opy_ != 0:
    sys.exit(bstack1ll1111ll1_opy_)
  if bstack1l111ll1ll_opy_ == bstack1111l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ཫ") and bstack11l1l1111_opy_ != 0:
    sys.exit(bstack11l1l1111_opy_)
def bstack11l1lll1l_opy_(new_id):
    global bstack1ll11l11l1_opy_
    bstack1ll11l11l1_opy_ = new_id
def bstack1111ll11l1_opy_(bstack1111ll11ll_opy_):
  if bstack1111ll11ll_opy_:
    return bstack1111ll11ll_opy_.capitalize()
  else:
    return bstack1111l_opy_ (u"ࠧࠨཬ")
@measure(event_name=EVENTS.bstack1lll1l1ll_opy_, stage=STAGE.bstack11lll111l_opy_, bstack11lll111_opy_=SESSION_NAME)
def bstack1ll1ll11_opy_(bstack111ll1lll1_opy_):
  if bstack1111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭཭") in bstack111ll1lll1_opy_ and bstack111ll1lll1_opy_[bstack1111l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ཮")] != bstack1111l_opy_ (u"ࠪࠫ཯"):
    return bstack111ll1lll1_opy_[bstack1111l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ཰")]
  else:
    bstack11lll111_opy_ = bstack1111l_opy_ (u"ࠧࠨཱ")
    if bstack1111l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪི࠭") in bstack111ll1lll1_opy_ and bstack111ll1lll1_opy_[bstack1111l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ཱིࠧ")] != None:
      bstack11lll111_opy_ += bstack111ll1lll1_opy_[bstack1111l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨུ")] + bstack1111l_opy_ (u"ࠤ࠯ࠤཱུࠧ")
      if bstack111ll1lll1_opy_[bstack1111l_opy_ (u"ࠪࡳࡸ࠭ྲྀ")] == bstack1111l_opy_ (u"ࠦ࡮ࡵࡳࠣཷ"):
        bstack11lll111_opy_ += bstack1111l_opy_ (u"ࠧ࡯ࡏࡔࠢࠥླྀ")
      bstack11lll111_opy_ += (bstack111ll1lll1_opy_[bstack1111l_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪཹ")] or bstack1111l_opy_ (u"ࠧࠨེ"))
      return bstack11lll111_opy_
    else:
      bstack11lll111_opy_ += bstack1111ll11l1_opy_(bstack111ll1lll1_opy_[bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳཻࠩ")]) + bstack1111l_opy_ (u"ࠤོࠣࠦ") + (
              bstack111ll1lll1_opy_[bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲཽࠬ")] or bstack1111l_opy_ (u"ࠫࠬཾ")) + bstack1111l_opy_ (u"ࠧ࠲ࠠࠣཿ")
      if bstack111ll1lll1_opy_[bstack1111l_opy_ (u"࠭࡯ࡴྀࠩ")] == bstack1111l_opy_ (u"ࠢࡘ࡫ࡱࡨࡴࡽࡳཱྀࠣ"):
        bstack11lll111_opy_ += bstack1111l_opy_ (u"࡙ࠣ࡬ࡲࠥࠨྂ")
      bstack11lll111_opy_ += bstack111ll1lll1_opy_[bstack1111l_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ྃ")] or bstack1111l_opy_ (u"྄ࠪࠫ")
      return bstack11lll111_opy_
@measure(event_name=EVENTS.bstack111l11ll_opy_, stage=STAGE.bstack11lll111l_opy_, bstack11lll111_opy_=SESSION_NAME)
def bstack1lll1111l1_opy_(bstack111lll1ll_opy_):
  if bstack111lll1ll_opy_ == bstack1111l_opy_ (u"ࠦࡩࡵ࡮ࡦࠤ྅"):
    return bstack1111l_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡨࡴࡨࡩࡳࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡨࡴࡨࡩࡳࠨ࠾ࡄࡱࡰࡴࡱ࡫ࡴࡦࡦ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨ྆")
  elif bstack111lll1ll_opy_ == bstack1111l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ྇"):
    return bstack1111l_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡵࡩࡩࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡳࡧࡧࠦࡃࡌࡡࡪ࡮ࡨࡨࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪྈ")
  elif bstack111lll1ll_opy_ == bstack1111l_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣྉ"):
    return bstack1111l_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾࡬ࡸࡥࡦࡰ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦ࡬ࡸࡥࡦࡰࠥࡂࡕࡧࡳࡴࡧࡧࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩྊ")
  elif bstack111lll1ll_opy_ == bstack1111l_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤྋ"):
    return bstack1111l_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡲࡦࡦ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡷ࡫ࡤࠣࡀࡈࡶࡷࡵࡲ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ྌ")
  elif bstack111lll1ll_opy_ == bstack1111l_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࠨྍ"):
    return bstack1111l_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࠥࡨࡩࡦ࠹࠲࠷࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࠧࡪ࡫ࡡ࠴࠴࠹ࠦࡃ࡚ࡩ࡮ࡧࡲࡹࡹࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫྎ")
  elif bstack111lll1ll_opy_ == bstack1111l_opy_ (u"ࠢࡳࡷࡱࡲ࡮ࡴࡧࠣྏ"):
    return bstack1111l_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡦࡱࡧࡣ࡬࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡦࡱࡧࡣ࡬ࠤࡁࡖࡺࡴ࡮ࡪࡰࡪࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩྐ")
  else:
    return bstack1111l_opy_ (u"ࠩ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡨ࡬ࡢࡥ࡮࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡨ࡬ࡢࡥ࡮ࠦࡃ࠭ྑ") + bstack1111ll11l1_opy_(
      bstack111lll1ll_opy_) + bstack1111l_opy_ (u"ࠪࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩྒ")
def bstack11l11111l1_opy_(session):
  return bstack1111l_opy_ (u"ࠫࡁࡺࡲࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡴࡲࡻࠧࡄ࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠡࡵࡨࡷࡸ࡯࡯࡯࠯ࡱࡥࡲ࡫ࠢ࠿࠾ࡤࠤ࡭ࡸࡥࡧ࠿ࠥࡿࢂࠨࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣࡡࡥࡰࡦࡴ࡫ࠣࡀࡾࢁࡁ࠵ࡡ࠿࠾࠲ࡸࡩࡄࡻࡾࡽࢀࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂ࠯ࡵࡴࡁࠫྒྷ").format(
    session[bstack1111l_opy_ (u"ࠬࡶࡵࡣ࡮࡬ࡧࡤࡻࡲ࡭ࠩྔ")], bstack1ll1ll11_opy_(session), bstack1lll1111l1_opy_(session[bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡹࡴࡢࡶࡸࡷࠬྕ")]),
    bstack1lll1111l1_opy_(session[bstack1111l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧྖ")]),
    bstack1111ll11l1_opy_(session[bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩྗ")] or session[bstack1111l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩ྘")] or bstack1111l_opy_ (u"ࠪࠫྙ")) + bstack1111l_opy_ (u"ࠦࠥࠨྚ") + (session[bstack1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧྛ")] or bstack1111l_opy_ (u"࠭ࠧྜ")),
    session[bstack1111l_opy_ (u"ࠧࡰࡵࠪྜྷ")] + bstack1111l_opy_ (u"ࠣࠢࠥྞ") + session[bstack1111l_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ྟ")], session[bstack1111l_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬྠ")] or bstack1111l_opy_ (u"ࠫࠬྡ"),
    session[bstack1111l_opy_ (u"ࠬࡩࡲࡦࡣࡷࡩࡩࡥࡡࡵࠩྡྷ")] if session[bstack1111l_opy_ (u"࠭ࡣࡳࡧࡤࡸࡪࡪ࡟ࡢࡶࠪྣ")] else bstack1111l_opy_ (u"ࠧࠨྤ"))
@measure(event_name=EVENTS.bstack11l111ll11_opy_, stage=STAGE.bstack11lll111l_opy_, bstack11lll111_opy_=SESSION_NAME)
def bstack11lll1l11_opy_(sessions, bstack11ll1l1l1l_opy_):
  try:
    bstack1l1l11lll_opy_ = bstack1111l_opy_ (u"ࠣࠤྥ")
    if not os.path.exists(bstack1lll11ll_opy_):
      os.mkdir(bstack1lll11ll_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1111l_opy_ (u"ࠩࡤࡷࡸ࡫ࡴࡴ࠱ࡵࡩࡵࡵࡲࡵ࠰࡫ࡸࡲࡲࠧྦ")), bstack1111l_opy_ (u"ࠪࡶࠬྦྷ")) as f:
      bstack1l1l11lll_opy_ = f.read()
    bstack1l1l11lll_opy_ = bstack1l1l11lll_opy_.replace(bstack1111l_opy_ (u"ࠫࢀࠫࡒࡆࡕࡘࡐ࡙࡙࡟ࡄࡑࡘࡒ࡙ࠫࡽࠨྨ"), str(len(sessions)))
    bstack1l1l11lll_opy_ = bstack1l1l11lll_opy_.replace(bstack1111l_opy_ (u"ࠬࢁࠥࡃࡗࡌࡐࡉࡥࡕࡓࡎࠨࢁࠬྩ"), bstack11ll1l1l1l_opy_)
    bstack1l1l11lll_opy_ = bstack1l1l11lll_opy_.replace(bstack1111l_opy_ (u"࠭ࡻࠦࡄࡘࡍࡑࡊ࡟ࡏࡃࡐࡉࠪࢃࠧྪ"),
                                              sessions[0].get(bstack1111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥ࡮ࡢ࡯ࡨࠫྫ")) if sessions[0] else bstack1111l_opy_ (u"ࠨࠩྫྷ"))
    with open(os.path.join(bstack1lll11ll_opy_, bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠮ࡴࡨࡴࡴࡸࡴ࠯ࡪࡷࡱࡱ࠭ྭ")), bstack1111l_opy_ (u"ࠪࡻࠬྮ")) as stream:
      stream.write(bstack1l1l11lll_opy_.split(bstack1111l_opy_ (u"ࠫࢀࠫࡓࡆࡕࡖࡍࡔࡔࡓࡠࡆࡄࡘࡆࠫࡽࠨྯ"))[0])
      for session in sessions:
        stream.write(bstack11l11111l1_opy_(session))
      stream.write(bstack1l1l11lll_opy_.split(bstack1111l_opy_ (u"ࠬࢁࠥࡔࡇࡖࡗࡎࡕࡎࡔࡡࡇࡅ࡙ࡇࠥࡾࠩྰ"))[1])
    logger.info(bstack1111l_opy_ (u"࠭ࡇࡦࡰࡨࡶࡦࡺࡥࡥࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡤࡸ࡭ࡱࡪࠠࡢࡴࡷ࡭࡫ࡧࡣࡵࡵࠣࡥࡹࠦࡻࡾࠩྱ").format(bstack1lll11ll_opy_));
  except Exception as e:
    logger.debug(bstack1l1l1l1111_opy_.format(str(e)))
def bstack1llllll1ll_opy_(hashed_id):
  global CONFIG
  try:
    bstack1lll1l11l_opy_ = datetime.datetime.now()
    host = bstack1111l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠲ࡩ࡬ࡰࡷࡧ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧྲ") if bstack1111l_opy_ (u"ࠨࡣࡳࡴࠬླ") in CONFIG else bstack1111l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡵ࡯࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪྴ")
    user = CONFIG[bstack1111l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬྵ")]
    key = CONFIG[bstack1111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧྶ")]
    bstack111lll1l1_opy_ = bstack1111l_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫྷ") if bstack1111l_opy_ (u"࠭ࡡࡱࡲࠪྸ") in CONFIG else (bstack1111l_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫྐྵ") if CONFIG.get(bstack1111l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬྺ")) else bstack1111l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫྻ"))
    host = bstack111l1lll1_opy_(cli.config, [bstack1111l_opy_ (u"ࠥࡥࡵ࡯ࡳࠣྼ"), bstack1111l_opy_ (u"ࠦࡦࡶࡰࡂࡷࡷࡳࡲࡧࡴࡦࠤ྽"), bstack1111l_opy_ (u"ࠧࡧࡰࡪࠤ྾")], host) if bstack1111l_opy_ (u"࠭ࡡࡱࡲࠪ྿") in CONFIG else bstack111l1lll1_opy_(cli.config, [bstack1111l_opy_ (u"ࠢࡢࡲ࡬ࡷࠧ࿀"), bstack1111l_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧࠥ࿁"), bstack1111l_opy_ (u"ࠤࡤࡴ࡮ࠨ࿂")], host)
    url = bstack1111l_opy_ (u"ࠪࡿࢂ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡹࡥࡴࡵ࡬ࡳࡳࡹ࠮࡫ࡵࡲࡲࠬ࿃").format(host, bstack111lll1l1_opy_, hashed_id)
    headers = {
      bstack1111l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪ࿄"): bstack1111l_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ࿅"),
    }
    proxies = bstack1l1l111l11_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies, auth=(user, key))
    if response.json():
      cli.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࡬࡫ࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࡢࡰ࡮ࡹࡴ࿆ࠣ"), datetime.datetime.now() - bstack1lll1l11l_opy_)
      return list(map(lambda session: session[bstack1111l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬ࿇")], response.json()))
  except Exception as e:
    logger.debug(bstack1ll111lll1_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack1111l1llll_opy_, stage=STAGE.bstack11lll111l_opy_, bstack11lll111_opy_=SESSION_NAME)
def get_build_link():
  global CONFIG
  global bstack1ll11l11l1_opy_
  try:
    if bstack1111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ࿈") in CONFIG:
      bstack1lll1l11l_opy_ = datetime.datetime.now()
      host = bstack1111l_opy_ (u"ࠩࡤࡴ࡮࠳ࡣ࡭ࡱࡸࡨࠬ࿉") if bstack1111l_opy_ (u"ࠪࡥࡵࡶࠧ࿊") in CONFIG else bstack1111l_opy_ (u"ࠫࡦࡶࡩࠨ࿋")
      user = CONFIG[bstack1111l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ࿌")]
      key = CONFIG[bstack1111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ࿍")]
      bstack111lll1l1_opy_ = bstack1111l_opy_ (u"ࠧࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭࿎") if bstack1111l_opy_ (u"ࠨࡣࡳࡴࠬ࿏") in CONFIG else bstack1111l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ࿐")
      url = bstack1111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࢀࢃ࠺ࡼࡿࡃࡿࢂ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡾࢁ࠴ࡨࡵࡪ࡮ࡧࡷ࠳ࡰࡳࡰࡰࠪ࿑").format(user, key, host, bstack111lll1l1_opy_)
      if cli.is_enabled(CONFIG):
        bstack11ll1l1l1l_opy_, hashed_id = cli.bstack1l1l1l1l_opy_()
        logger.info(bstack11ll1ll111_opy_.format(bstack11ll1l1l1l_opy_))
        return [hashed_id, bstack11ll1l1l1l_opy_]
      else:
        headers = {
          bstack1111l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪ࿒"): bstack1111l_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ࿓"),
        }
        if bstack1111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ࿔") in CONFIG:
          params = {bstack1111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ࿕"): CONFIG[bstack1111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ࿖")], bstack1111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ࿗"): CONFIG[bstack1111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ࿘")]}
        else:
          params = {bstack1111l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ࿙"): CONFIG[bstack1111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ࿚")]}
        proxies = bstack1l1l111l11_opy_(CONFIG, url)
        response = requests.get(url, params=params, headers=headers, proxies=proxies)
        if response.json():
          bstack1l11llllll_opy_ = response.json()[0][bstack1111l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡦࡺ࡯࡬ࡥࠩ࿛")]
          if bstack1l11llllll_opy_:
            bstack11ll1l1l1l_opy_ = bstack1l11llllll_opy_[bstack1111l_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࡟ࡶࡴ࡯ࠫ࿜")].split(bstack1111l_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣ࠮ࡤࡸ࡭ࡱࡪࠧ࿝"))[0] + bstack1111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡴ࠱ࠪ࿞") + bstack1l11llllll_opy_[
              bstack1111l_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭࿟")]
            logger.info(bstack11ll1ll111_opy_.format(bstack11ll1l1l1l_opy_))
            bstack1ll11l11l1_opy_ = bstack1l11llllll_opy_[bstack1111l_opy_ (u"ࠫ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ࿠")]
            bstack111l1l1l11_opy_ = CONFIG[bstack1111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ࿡")]
            if bstack1111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ࿢") in CONFIG:
              bstack111l1l1l11_opy_ += bstack1111l_opy_ (u"ࠧࠡࠩ࿣") + CONFIG[bstack1111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ࿤")]
            if bstack111l1l1l11_opy_ != bstack1l11llllll_opy_[bstack1111l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ࿥")]:
              logger.debug(bstack1l11l111l_opy_.format(bstack1l11llllll_opy_[bstack1111l_opy_ (u"ࠪࡲࡦࡳࡥࠨ࿦")], bstack111l1l1l11_opy_))
            cli.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼ࡪࡩࡹࡥࡢࡶ࡫࡯ࡨࡤࡲࡩ࡯࡭ࠥ࿧"), datetime.datetime.now() - bstack1lll1l11l_opy_)
            return [bstack1l11llllll_opy_[bstack1111l_opy_ (u"ࠬ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ࿨")], bstack11ll1l1l1l_opy_]
    else:
      logger.warning(bstack111lllll_opy_)
  except Exception as e:
    logger.debug(bstack11ll1llll1_opy_.format(str(e)))
  return [None, None]
def bstack1l11ll111l_opy_(url, bstack1ll11l1111_opy_=False):
  global CONFIG
  global bstack1l1111l1ll_opy_
  if not bstack1l1111l1ll_opy_:
    hostname = bstack11l11ll1l_opy_(url)
    is_private = bstack111ll1l111_opy_(hostname)
    if (bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ࿩") in CONFIG and not bstack1ll111llll_opy_(CONFIG[bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ࿪")])) and (is_private or bstack1ll11l1111_opy_):
      bstack1l1111l1ll_opy_ = hostname
def bstack11l11ll1l_opy_(url):
  return urlparse(url).hostname
def bstack111ll1l111_opy_(hostname):
  for bstack1lllll1lll_opy_ in bstack1l111l111_opy_:
    regex = re.compile(bstack1lllll1lll_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1ll111ll_opy_(bstack11ll111ll1_opy_):
  return True if bstack11ll111ll1_opy_ in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack11ll1lll1l_opy_, stage=STAGE.bstack11lll111l_opy_, bstack11lll111_opy_=SESSION_NAME)
def getAccessibilityResults(driver):
  global CONFIG
  global PLATFORM_INDEX
  bstack11111l1l_opy_ = not (bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬ࿫"), None) and bstack1l11l11l11_opy_(
          threading.current_thread(), bstack1111l_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ࿬"), None))
  bstack1ll111ll11_opy_ = getattr(driver, bstack1111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪ࿭"), None) != True
  bstack11l1llll1l_opy_ = bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ࿮"), None) and bstack1l11l11l11_opy_(
          threading.current_thread(), bstack1111l_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ࿯"), None)
  if bstack11l1llll1l_opy_:
    if not bstack11l1l11ll_opy_():
      logger.warning(bstack1111l_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡆࡶࡰࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴ࠰ࠥ࿰"))
      return {}
    logger.debug(bstack1111l_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠫ࿱"))
    logger.debug(perform_scan(driver, driver_command=bstack1111l_opy_ (u"ࠨࡧࡻࡩࡨࡻࡴࡦࡕࡦࡶ࡮ࡶࡴࠨ࿲")))
    results = bstack11lll1ll1l_opy_(bstack1111l_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡵࠥ࿳"))
    if results is not None and results.get(bstack1111l_opy_ (u"ࠥ࡭ࡸࡹࡵࡦࡵࠥ࿴")) is not None:
        return results[bstack1111l_opy_ (u"ࠦ࡮ࡹࡳࡶࡧࡶࠦ࿵")]
    logger.error(bstack1111l_opy_ (u"ࠧࡔ࡯ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡔࡨࡷࡺࡲࡴࡴࠢࡺࡩࡷ࡫ࠠࡧࡱࡸࡲࡩ࠴ࠢ࿶"))
    return []
  if not a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX) or (bstack1ll111ll11_opy_ and bstack11111l1l_opy_):
    logger.warning(bstack1111l_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳ࠯ࠤ࿷"))
    return {}
  try:
    logger.debug(bstack1111l_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠫ࿸"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(accessibility_scripts.get_results)
    return results
  except Exception:
    logger.error(bstack1111l_opy_ (u"ࠣࡐࡲࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡽࡥࡳࡧࠣࡪࡴࡻ࡮ࡥ࠰ࠥ࿹"))
    return {}
@measure(event_name=EVENTS.bstack1lllll11l1_opy_, stage=STAGE.bstack11lll111l_opy_, bstack11lll111_opy_=SESSION_NAME)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global PLATFORM_INDEX
  bstack11111l1l_opy_ = not (bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭࿺"), None) and bstack1l11l11l11_opy_(
          threading.current_thread(), bstack1111l_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ࿻"), None))
  bstack1ll111ll11_opy_ = getattr(driver, bstack1111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫ࿼"), None) != True
  bstack11l1llll1l_opy_ = bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠬ࡯ࡳࡂࡲࡳࡅ࠶࠷ࡹࡕࡧࡶࡸࠬ࿽"), None) and bstack1l11l11l11_opy_(
          threading.current_thread(), bstack1111l_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ࿾"), None)
  if bstack11l1llll1l_opy_:
    if not bstack11l1l11ll_opy_():
      logger.warning(bstack1111l_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡲࡳࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡪࡺࡲࡪࡧࡹࡩࠥࡇࡰࡱࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡷࡺࡳ࡭ࡢࡴࡼ࠲ࠧ࿿"))
      return {}
    logger.debug(bstack1111l_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡹࡵ࡮࡯ࡤࡶࡾ࠭က"))
    logger.debug(perform_scan(driver, driver_command=bstack1111l_opy_ (u"ࠩࡨࡼࡪࡩࡵࡵࡧࡖࡧࡷ࡯ࡰࡵࠩခ")))
    results = bstack11lll1ll1l_opy_(bstack1111l_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡖࡹࡲࡳࡡࡳࡻࠥဂ"))
    if results is not None and results.get(bstack1111l_opy_ (u"ࠦࡸࡻ࡭࡮ࡣࡵࡽࠧဃ")) is not None:
        return results[bstack1111l_opy_ (u"ࠧࡹࡵ࡮࡯ࡤࡶࡾࠨင")]
    logger.error(bstack1111l_opy_ (u"ࠨࡎࡰࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡕࡩࡸࡻ࡬ࡵࡵࠣࡗࡺࡳ࡭ࡢࡴࡼࠤࡼࡧࡳࠡࡨࡲࡹࡳࡪ࠮ࠣစ"))
    return {}
  if not a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX) or (bstack1ll111ll11_opy_ and bstack11111l1l_opy_):
    logger.warning(bstack1111l_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡶࡹࡲࡳࡡࡳࡻ࠱ࠦဆ"))
    return {}
  try:
    logger.debug(bstack1111l_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡹࡵ࡮࡯ࡤࡶࡾ࠭ဇ"))
    logger.debug(perform_scan(driver))
    bstack1l11l1l1l_opy_ = driver.execute_async_script(accessibility_scripts.get_results_summary)
    return bstack1l11l1l1l_opy_
  except Exception:
    logger.error(bstack1111l_opy_ (u"ࠤࡑࡳࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡵ࡮࡯ࡤࡶࡾࠦࡷࡢࡵࠣࡪࡴࡻ࡮ࡥ࠰ࠥဈ"))
    return {}
def bstack11l1l11ll_opy_():
  global CONFIG
  global PLATFORM_INDEX
  bstack1ll11ll1_opy_ = bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪဉ"), None) and bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ည"), None)
  if not a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX) or not bstack1ll11ll1_opy_:
        logger.warning(bstack1111l_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡰࡱࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡶࡪࡹࡵ࡭ࡶࡶ࠲ࠧဋ"))
        return False
  return True
def bstack11lll1ll1l_opy_(result_type):
    bstack111lll1111_opy_ = TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack11l11ll1l1_opy_.current_hook_uuid()
    with ThreadPoolExecutor() as executor:
        future = executor.submit(bstack1l11lll1_opy_(bstack111lll1111_opy_, result_type))
        try:
            return future.result(timeout=bstack1l1l1l11l1_opy_)
        except TimeoutError:
            logger.error(bstack1111l_opy_ (u"ࠨࡔࡪ࡯ࡨࡳࡺࡺࠠࡢࡨࡷࡩࡷࠦࡻࡾࡵࠣࡻ࡭࡯࡬ࡦࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡗ࡫ࡳࡶ࡮ࡷࡷࠧဌ").format(bstack1l1l1l11l1_opy_))
        except Exception as ex:
            logger.debug(bstack1111l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡲࡦࡶࡵ࡭ࡪࡼࡩ࡯ࡩࠣࡅࡵࡶࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࢀࢃ࠮ࠡࡇࡵࡶࡴࡸࠠ࠮ࠢࡾࢁࠧဍ").format(result_type, str(ex)))
    return {}
@measure(event_name=EVENTS.bstack1l11llll_opy_, stage=STAGE.bstack11lll111l_opy_, bstack11lll111_opy_=SESSION_NAME)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global PLATFORM_INDEX
  bstack11111l1l_opy_ = not (bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬဎ"), None) and bstack1l11l11l11_opy_(
          threading.current_thread(), bstack1111l_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨဏ"), None))
  bstack11ll1ll1l_opy_ = not (bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪတ"), None) and bstack1l11l11l11_opy_(
          threading.current_thread(), bstack1111l_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ထ"), None))
  bstack1ll111ll11_opy_ = getattr(driver, bstack1111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬဒ"), None) != True
  if not a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX) or (bstack1ll111ll11_opy_ and bstack11111l1l_opy_ and bstack11ll1ll1l_opy_):
    logger.warning(bstack1111l_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡵ࡯ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡧࡦࡴ࠮ࠣဓ"))
    return {}
  try:
    bstack11ll11lll1_opy_ = bstack1111l_opy_ (u"ࠧࡢࡲࡳࠫန") in CONFIG and CONFIG.get(bstack1111l_opy_ (u"ࠨࡣࡳࡴࠬပ"), bstack1111l_opy_ (u"ࠩࠪဖ"))
    session_id = getattr(driver, bstack1111l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠧဗ"), None)
    if not session_id:
      logger.warning(bstack1111l_opy_ (u"ࠦࡓࡵࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡋࡇࠤ࡫ࡵࡵ࡯ࡦࠣࡪࡴࡸࠠࡥࡴ࡬ࡺࡪࡸࠢဘ"))
      return {bstack1111l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦမ"): bstack1111l_opy_ (u"ࠨࡎࡰࠢࡶࡩࡸࡹࡩࡰࡰࠣࡍࡉࠦࡦࡰࡷࡱࡨࠧယ")}
    if bstack11ll11lll1_opy_:
      try:
        bstack1l11l11l1_opy_ = {
              bstack1111l_opy_ (u"ࠧࡵࡪࡍࡻࡹ࡚࡯࡬ࡧࡱࠫရ"): os.environ.get(bstack1111l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭လ"), os.environ.get(bstack1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ဝ"), bstack1111l_opy_ (u"ࠪࠫသ"))),
              bstack1111l_opy_ (u"ࠫࡹ࡮ࡔࡦࡵࡷࡖࡺࡴࡕࡶ࡫ࡧࠫဟ"): TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack11l11ll1l1_opy_.current_hook_uuid(),
              bstack1111l_opy_ (u"ࠬࡧࡵࡵࡪࡋࡩࡦࡪࡥࡳࠩဠ"): os.environ.get(bstack1111l_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫအ")),
              bstack1111l_opy_ (u"ࠧࡴࡥࡤࡲ࡙࡯࡭ࡦࡵࡷࡥࡲࡶࠧဢ"): str(int(datetime.datetime.now().timestamp() * 1000)),
              bstack1111l_opy_ (u"ࠨࡶ࡫ࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ဣ"): os.environ.get(bstack1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧဤ"), bstack1111l_opy_ (u"ࠪࠫဥ")),
              bstack1111l_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࠫဦ"): kwargs.get(bstack1111l_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࡤࡩ࡯࡮࡯ࡤࡲࡩ࠭ဧ"), None) or bstack1111l_opy_ (u"࠭ࠧဨ")
          }
        if not hasattr(thread_local, bstack1111l_opy_ (u"ࠧࡣࡣࡶࡩࡤࡧࡰࡱࡡࡤ࠵࠶ࡿ࡟ࡴࡥࡵ࡭ࡵࡺࠧဩ")):
            scripts = {bstack1111l_opy_ (u"ࠨࡵࡦࡥࡳ࠭ဪ"): accessibility_scripts.perform_scan}
            thread_local.base_app_a11y_script = scripts
        bstack1l11ll11l_opy_ = copy.deepcopy(thread_local.base_app_a11y_script)
        bstack1l11ll11l_opy_[bstack1111l_opy_ (u"ࠩࡶࡧࡦࡴࠧါ")] = bstack1l11ll11l_opy_[bstack1111l_opy_ (u"ࠪࡷࡨࡧ࡮ࠨာ")] % json.dumps(bstack1l11l11l1_opy_)
        accessibility_scripts.bstack1llll11ll1_opy_(bstack1l11ll11l_opy_)
        accessibility_scripts.store()
        bstack1lll11l1l1_opy_ = driver.execute_script(accessibility_scripts.perform_scan)
      except Exception as bstack111ll1ll_opy_:
        logger.info(bstack1111l_opy_ (u"ࠦࡆࡶࡰࡪࡷࡰࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸࡩࡡ࡯ࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࠦိ") + str(bstack111ll1ll_opy_))
        bstack1lll11l1l1_opy_ = {bstack1111l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦီ"): str(bstack111ll1ll_opy_)}
    else:
      bstack1lll11l1l1_opy_ = driver.execute_async_script(accessibility_scripts.perform_scan, {bstack1111l_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩ࠭ု"): kwargs.get(bstack1111l_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸ࡟ࡤࡱࡰࡱࡦࡴࡤࠨူ"), None) or bstack1111l_opy_ (u"ࠨࠩေ")})
    return bstack1lll11l1l1_opy_
  except Exception as err:
    logger.error(bstack1111l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡸࡵ࡯ࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡧࡦࡴ࠮ࠡࡽࢀࠦဲ").format(str(err)))
    return {}