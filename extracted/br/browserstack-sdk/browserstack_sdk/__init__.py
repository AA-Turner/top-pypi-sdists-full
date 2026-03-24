# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
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
from browserstack_sdk.sdk_cli.bstack11ll111lll_opy_ import bstack1llll1ll1l_opy_
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from browserstack_sdk.bstack1111l1l11_opy_ import bstack1lllll1ll1_opy_
from browserstack_sdk.bstack1lll1ll1_opy_ import *
import time
import requests
from bstack_utils.constants import EVENTS, STAGE, bstack1llll1l11l_opy_
from bstack_utils.messages import bstack11lll11111_opy_, bstack1ll1lll1_opy_, bstack1l11lll1l1_opy_, bstack11l11ll1_opy_, bstack1l1l1ll111_opy_, bstack1ll11ll11l_opy_
from bstack_utils.measure import measure
from bstack_utils.logger_utils import get_logger
from bstack_utils.helper import bstack11ll1l111l_opy_
from browserstack_sdk.bstack1111l11l11_opy_ import bstack1lll1l1l1l_opy_
logger = get_logger(__name__)
def bstack1l111lll1_opy_():
  global CONFIG
  headers = {
        bstack1ll1lll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack1ll1lll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack11ll1l111l_opy_(CONFIG, bstack1llll1l11l_opy_)
  try:
    response = requests.get(bstack1llll1l11l_opy_, headers=headers, proxies=proxies, timeout=2)
    if response.json():
      bstack1l1l1l1l11_opy_ = response.json()[bstack1ll1lll_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack11lll11111_opy_.format(response.json()))
      return bstack1l1l1l1l11_opy_
    else:
      logger.debug(bstack1ll1lll1_opy_.format(bstack1ll1lll_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack1ll1lll1_opy_.format(e))
def bstack1ll1l1llll_opy_(hub_url):
  global CONFIG
  url = bstack1ll1lll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack1ll1lll_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack1ll1lll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack1ll1lll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack11ll1l111l_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=(0.5, 1.0))
    latency = time.perf_counter() - start_time
    logger.debug(bstack1l11lll1l1_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack11l11ll1_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack1lll1l11ll_opy_, stage=STAGE.bstack1ll1llll_opy_)
def bstack11llll1ll1_opy_():
  try:
    global bstack1lllll111_opy_
    global CONFIG
    if bstack1ll1lll_opy_ (u"ࠫ࡭ࡻࡢࡓࡧࡪ࡭ࡴࡴࠧࡾ") in CONFIG and CONFIG[bstack1ll1lll_opy_ (u"ࠬ࡮ࡵࡣࡔࡨ࡫࡮ࡵ࡮ࠨࡿ")]:
      from bstack_utils.constants import bstack1ll1l1ll_opy_
      bstack11ll11ll1_opy_ = CONFIG[bstack1ll1lll_opy_ (u"࠭ࡨࡶࡤࡕࡩ࡬࡯࡯࡯ࠩࢀ")]
      if bstack11ll11ll1_opy_ in bstack1ll1l1ll_opy_:
        bstack1lllll111_opy_ = bstack1ll1l1ll_opy_[bstack11ll11ll1_opy_]
        logger.debug(bstack1l1l1ll111_opy_.format(bstack1lllll111_opy_))
        return
      else:
        logger.debug(bstack1ll1lll_opy_ (u"ࠢࡉࡷࡥࠤࡰ࡫ࡹࠡࠩࡾࢁࠬࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࡎࡕࡃࡡࡘࡖࡑࡥࡍࡂࡒ࠯ࠤ࡫ࡧ࡬࡭࡫ࡱ࡫ࠥࡨࡡࡤ࡭ࠣࡸࡴࠦ࡯ࡱࡶ࡬ࡱࡦࡲࠠࡩࡷࡥࠤࡩ࡫ࡴࡦࡥࡷ࡭ࡴࡴࠢࢁ").format(bstack11ll11ll1_opy_))
    bstack1l1l1l1l11_opy_ = bstack1l111lll1_opy_()
    from concurrent.futures import ThreadPoolExecutor, as_completed
    if bstack1l1l1l1l11_opy_:
        with ThreadPoolExecutor(max_workers=len(bstack1l1l1l1l11_opy_)) as executor:
            bstack1lll1ll1l1_opy_ = {executor.submit(bstack1ll1l1llll_opy_, bstack1ll11l111l_opy_): bstack1ll11l111l_opy_ for bstack1ll11l111l_opy_ in bstack1l1l1l1l11_opy_}
            for future in as_completed(bstack1lll1ll1l1_opy_):
                result = future.result()
                if result and result.get(bstack1ll1lll_opy_ (u"ࠨ࡮ࡤࡸࡪࡴࡣࡺࠩࢂ")) is not None:
                    bstack1lllll111_opy_ = result[bstack1ll1lll_opy_ (u"ࠩ࡫ࡹࡧࡥࡵࡳ࡮ࠪࢃ")]
                    logger.debug(bstack1l1l1ll111_opy_.format(bstack1lllll111_opy_))
                    return
        bstack1lllll111_opy_ = bstack1l1l1l1l11_opy_[0]
        logger.debug(bstack1l1l1ll111_opy_.format(bstack1lllll111_opy_))
        return
  except Exception as e:
    logger.debug(bstack1ll11ll11l_opy_.format(e))
from browserstack_sdk.bstack11llllll1l_opy_ import *
from browserstack_sdk.bstack1111l11l11_opy_ import *
from browserstack_sdk.bstack1l111l1l_opy_ import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.logger_utils import get_logger
from bstack_utils.measure import measure
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack1l11ll11l_opy_, stage=STAGE.bstack1ll1llll_opy_)
def bstack11lll111l_opy_():
    global bstack1lllll111_opy_
    try:
        bstack1l11111l_opy_ = bstack1ll11ll11_opy_()
        bstack1ll111l1ll_opy_(bstack1l11111l_opy_)
        hub_url = bstack1l11111l_opy_.get(bstack1ll1lll_opy_ (u"ࠥࡹࡷࡲࠢࢄ"), bstack1ll1lll_opy_ (u"ࠦࠧࢅ"))
        if hub_url.endswith(bstack1ll1lll_opy_ (u"ࠬ࠵ࡷࡥ࠱࡫ࡹࡧ࠭ࢆ")):
            hub_url = hub_url.rsplit(bstack1ll1lll_opy_ (u"࠭࠯ࡸࡦ࠲࡬ࡺࡨࠧࢇ"), 1)[0]
        if hub_url.startswith(bstack1ll1lll_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࠨ࢈")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack1ll1lll_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࠪࢉ")):
            hub_url = hub_url[8:]
        bstack1lllll111_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack1ll11ll11_opy_():
    global CONFIG
    bstack11l111lll1_opy_ = CONFIG.get(bstack1ll1lll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢊ"), {}).get(bstack1ll1lll_opy_ (u"ࠪ࡫ࡷ࡯ࡤࡏࡣࡰࡩࠬࢋ"), bstack1ll1lll_opy_ (u"ࠫࡓࡕ࡟ࡈࡔࡌࡈࡤࡔࡁࡎࡇࡢࡔࡆ࡙ࡓࡆࡆࠪࢌ"))
    if not isinstance(bstack11l111lll1_opy_, str):
        raise ValueError(bstack1ll1lll_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡌࡸࡩࡥࠢࡱࡥࡲ࡫ࠠ࡮ࡷࡶࡸࠥࡨࡥࠡࡣࠣࡺࡦࡲࡩࡥࠢࡶࡸࡷ࡯࡮ࡨࠤࢍ"))
    try:
        bstack1l11111l_opy_ = bstack11ll11lll1_opy_(bstack11l111lll1_opy_)
        return bstack1l11111l_opy_
    except Exception as e:
        logger.error(bstack1ll1lll_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡩࡵ࡭ࡩࠦࡤࡦࡶࡤ࡭ࡱࡹࠠ࠻ࠢࡾࢁࠧࢎ").format(str(e)))
        return {}
def bstack11ll11lll1_opy_(bstack11l111lll1_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack1ll1lll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ࢏")] or not CONFIG[bstack1ll1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ࢐")]:
            raise ValueError(bstack1ll1lll_opy_ (u"ࠤࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠤࡴࡸࠠࡢࡥࡦࡩࡸࡹࠠ࡬ࡧࡼࠦ࢑"))
        url = bstack11l1l11ll1_opy_ + bstack11l111lll1_opy_
        auth = (CONFIG[bstack1ll1lll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ࢒")], CONFIG[bstack1ll1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ࢓")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack1lll111l_opy_ = json.loads(response.text)
            return bstack1lll111l_opy_
    except ValueError as ve:
        logger.error(bstack1ll1lll_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡩࡵ࡭ࡩࠦࡤࡦࡶࡤ࡭ࡱࡹࠠ࠻ࠢࡾࢁࠧ࢔").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack1ll1lll_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡪࡶ࡮ࡪࠠࡥࡧࡷࡥ࡮ࡲࡳࠡ࠼ࠣࡿࢂࠨ࢕").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack1ll111l1ll_opy_(bstack11111l1l11_opy_):
    global CONFIG
    if bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ࢖") not in CONFIG or str(CONFIG[bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬࢗ")]).lower() == bstack1ll1lll_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ࢘"):
        CONFIG[bstack1ll1lll_opy_ (u"ࠪࡰࡴࡩࡡ࡭࢙ࠩ")] = False
    elif bstack1ll1lll_opy_ (u"ࠫ࡮ࡹࡔࡳ࡫ࡤࡰࡌࡸࡩࡥ࢚ࠩ") in bstack11111l1l11_opy_:
        bstack1ll1l1111l_opy_ = CONFIG.get(bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴ࢛ࠩ"), {})
        logger.debug(bstack1ll1lll_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡸࡪࡵࡷ࡭ࡳ࡭ࠠ࡭ࡱࡦࡥࡱࠦ࡯ࡱࡶ࡬ࡳࡳࡹ࠺ࠡࠧࡶࠦ࢜"), bstack1ll1l1111l_opy_)
        bstack1111l11111_opy_ = bstack11111l1l11_opy_.get(bstack1ll1lll_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡒࡦࡲࡨࡥࡹ࡫ࡲࡴࠤ࢝"), [])
        bstack1111111l_opy_ = bstack1ll1lll_opy_ (u"ࠣ࠮ࠥ࢞").join(bstack1111l11111_opy_)
        logger.debug(bstack1ll1lll_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡅࡸࡷࡹࡵ࡭ࠡࡴࡨࡴࡪࡧࡴࡦࡴࠣࡷࡹࡸࡩ࡯ࡩ࠽ࠤࠪࡹࠢ࢟"), bstack1111111l_opy_)
        bstack1l1111111_opy_ = {
            bstack1ll1lll_opy_ (u"ࠥࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧࢠ"): bstack1ll1lll_opy_ (u"ࠦࡦࡺࡳ࠮ࡴࡨࡴࡪࡧࡴࡦࡴࠥࢡ"),
            bstack1ll1lll_opy_ (u"ࠧ࡬࡯ࡳࡥࡨࡐࡴࡩࡡ࡭ࠤࢢ"): bstack1ll1lll_opy_ (u"ࠨࡴࡳࡷࡨࠦࢣ"),
            bstack1ll1lll_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࠭ࡳࡧࡳࡩࡦࡺࡥࡳࠤࢤ"): bstack1111111l_opy_
        }
        bstack1ll1l1111l_opy_.update(bstack1l1111111_opy_)
        logger.debug(bstack1ll1lll_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡖࡲࡧࡥࡹ࡫ࡤࠡ࡮ࡲࡧࡦࡲࠠࡰࡲࡷ࡭ࡴࡴࡳ࠻ࠢࠨࡷࠧࢥ"), bstack1ll1l1111l_opy_)
        CONFIG[bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢦ")] = bstack1ll1l1111l_opy_
        logger.debug(bstack1ll1lll_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡉ࡭ࡳࡧ࡬ࠡࡅࡒࡒࡋࡏࡇ࠻ࠢࠨࡷࠧࢧ"), CONFIG)
def get_turboscale_playwright_url():
    bstack1l11111l_opy_ = bstack1ll11ll11_opy_()
    if not bstack1l11111l_opy_[bstack1ll1lll_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡖࡴ࡯ࠫࢨ")]:
      raise ValueError(bstack1ll1lll_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡗࡵࡰࠥ࡯ࡳࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡩࡶࡴࡳࠠࡨࡴ࡬ࡨࠥࡪࡥࡵࡣ࡬ࡰࡸ࠴ࠢࢩ"))
    return bstack1l11111l_opy_[bstack1ll1lll_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡘࡶࡱ࠭ࢪ")] + bstack1ll1lll_opy_ (u"ࠧࡀࡥࡤࡴࡸࡃࠧࢫ")
@measure(event_name=EVENTS.bstack11l11111l_opy_, stage=STAGE.bstack1ll1llll_opy_)
def bstack1l1l1l1ll_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack1ll1lll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪࢬ")], CONFIG[bstack1ll1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬࢭ")])
        url = bstack1l11lllll_opy_
        logger.debug(bstack1ll1lll_opy_ (u"ࠥࡅࡹࡺࡥ࡮ࡲࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴࠢࡩࡶࡴࡳࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡔࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠣࡅࡕࡏࠢࢮ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack1ll1lll_opy_ (u"ࠦࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠥࢯ"): bstack1ll1lll_opy_ (u"ࠧࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠣࢰ")})
            if response.status_code == 200:
                bstack111l1lll1_opy_ = json.loads(response.text)
                bstack1l1l1111l1_opy_ = bstack111l1lll1_opy_.get(bstack1ll1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡸ࠭ࢱ"), [])
                if bstack1l1l1111l1_opy_:
                    bstack11l11ll111_opy_ = bstack1l1l1111l1_opy_[0]
                    build_hashed_id = bstack11l11ll111_opy_.get(bstack1ll1lll_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪࢲ"))
                    bstack1ll1111l11_opy_ = bstack111l11ll11_opy_ + build_hashed_id
                    result.extend([build_hashed_id, bstack1ll1111l11_opy_])
                    logger.info(bstack11lllll1l_opy_.format(bstack1ll1111l11_opy_))
                    bstack11l1l1llll_opy_ = CONFIG[bstack1ll1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫࢳ")]
                    if bstack1ll1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࢴ") in CONFIG:
                      bstack11l1l1llll_opy_ += bstack1ll1lll_opy_ (u"ࠪࠤࠬࢵ") + CONFIG[bstack1ll1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࢶ")]
                    if bstack11l1l1llll_opy_ != bstack11l11ll111_opy_.get(bstack1ll1lll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪࢷ")):
                      logger.debug(bstack1lll111l1l_opy_.format(bstack11l11ll111_opy_.get(bstack1ll1lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫࢸ")), bstack11l1l1llll_opy_))
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
from browserstack_sdk.sdk_cli.bstack1l111111ll_opy_ import bstack1l111111ll_opy_, Events, bstack1111lll11l_opy_, bstack11lll111_opy_
from bstack_utils.measure import bstack1ll11111_opy_
from bstack_utils.measure import measure
from bstack_utils.percy import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1l11111l11_opy_ import bstack1l1111lll1_opy_
from bstack_utils.messages import *
from bstack_utils import logger_utils
from bstack_utils.constants import *
from bstack_utils.helper import bstack1l1llll1ll_opy_, bstack111l1l111l_opy_, bstack1l11llll1l_opy_, bstack111l1lll11_opy_, \
  bstack1l111llll_opy_, \
  Notset, is_robot_playwright_installed, bstack11l11l1111_opy_, \
  bstack1l1111lll_opy_, bstack1l11l1l1l1_opy_, bstack1l1lllllll_opy_, bstack1l1l1ll1l_opy_, bstack1l11ll1lll_opy_, bstack11llllll_opy_, \
  bstack11lllll11l_opy_, \
  bstack1ll11ll1l_opy_, bstack1l111lllll_opy_, bstack11l1111l11_opy_, bstack11ll1l111_opy_, \
  bstack1l111llll1_opy_, bstack1l11llll1_opy_, bstack11llll111l_opy_, bstack11l111l1_opy_, bstack1lll11lll_opy_
from bstack_utils.bstack11l1l1111l_opy_ import bstack11l1l1111_opy_
from bstack_utils.bstack1l111lll_opy_ import bstack11l1llll11_opy_, bstack1l1l1l11l_opy_
from bstack_utils.bstack11ll1l1l11_opy_ import bstack1lll11111_opy_
from bstack_utils.session_utils import bstack1111lll1l1_opy_, bstack11ll11ll11_opy_
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.bstack1lll1l1lll_opy_ import bstack11l1l1ll11_opy_
from bstack_utils.proxy import bstack1l1ll11l_opy_, bstack11ll1l111l_opy_, bstack111ll1ll11_opy_, bstack1ll1ll11l_opy_
from bstack_utils.bstack1l11ll111l_opy_ import bstack1lll11l1_opy_, bstack11lll11l1_opy_
import bstack_utils.bstack1l1l1ll11_opy_ as TestHubUtils
import bstack_utils.bstack1111l1l111_opy_ as bstack1l11l1ll11_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.utils.bstack111l1ll1ll_opy_ import bstack11l1l11l_opy_
from bstack_utils.bstack1lll11llll_opy_ import bstack1l11ll1ll1_opy_
from bstack_utils.bstack111l11l11l_opy_ import bstack11lll1ll1_opy_
from bstack_utils.bstack1ll11111_opy_ import bstack1lll1lll11_opy_
if os.getenv(bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡉࡑࡒࡏࡘ࠭ࢽ")):
  cli.bstack11lll11ll1_opy_()
else:
  os.environ[bstack1ll1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡊࡒࡓࡐ࡙ࠧࢾ")] = bstack1ll1lll_opy_ (u"࠭ࡴࡳࡷࡨࠫࢿ")
bstack1l1ll1l1l_opy_ = bstack1ll1lll_opy_ (u"ࠧࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠠࠡ࡫ࡩࠬࡵࡧࡧࡦࠢࡀࡁࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠠࡼ࡞ࡱࠤࠥࠦࡴࡳࡻࡾࡠࡳࠦࡣࡰࡰࡶࡸࠥ࡬ࡳࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࡡ࠭ࡦࡴ࡞ࠪ࠭ࡀࡢ࡮ࠡࠢࠣࠤࠥ࡬ࡳ࠯ࡣࡳࡴࡪࡴࡤࡇ࡫࡯ࡩࡘࡿ࡮ࡤࠪࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠬࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡳࡣ࡮ࡴࡤࡦࡺࠬࠤ࠰ࠦࠢ࠻ࠤࠣ࠯ࠥࡐࡓࡐࡐ࠱ࡷࡹࡸࡩ࡯ࡩ࡬ࡪࡾ࠮ࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࠬࡦࡽࡡࡪࡶࠣࡲࡪࡽࡐࡢࡩࡨ࠶࠳࡫ࡶࡢ࡮ࡸࡥࡹ࡫ࠨࠣࠪࠬࠤࡂࡄࠠࡼࡿࠥ࠰ࠥࡢࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡨࡧࡷࡗࡪࡹࡳࡪࡱࡱࡈࡪࡺࡡࡪ࡮ࡶࠦࢂࡢࠧࠪࠫࠬ࡟ࠧ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠣ࡟ࠬࠤ࠰ࠦࠢ࠭࡞࡟ࡲࠧ࠯࡜࡯ࠢࠣࠤࠥࢃࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡽ࡝ࡰࠣࠤ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠧࣀ")
LAUNCH_PATCH_ROBOT_PLAYWRIGHT = bstack1ll1lll_opy_ (u"ࠨ࡞ࡱ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࡢ࡮ࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠻࡝ࠡ࠿ࡀࡁࠥࡢࠧࡵࡴࡸࡩࡡ࠭࡜࡯ࡥࡲࡲࡸࡺࠠࡣࡵࡷࡥࡨࡱ࡟ࡱࡣࡷ࡬ࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴࡟࡟ࡲࡨࡵ࡮ࡴࡶࠣࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࡝ࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠵ࡢࡢ࡮ࡤࡱࡱࡷࡹࠦࡰࡠ࡫ࡱࡨࡪࡾࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠵ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠵࡟ࠣࡁࡂࡃࠠ࡝ࠩࡷࡶࡺ࡫࡜ࠨ࡞ࡱࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡷࡱ࡯ࡣࡦࠪ࠳࠰ࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠵ࠪ࡞ࡱࡧࡴࡴࡳࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣࠫ࠾ࡠࡳࡩ࡯࡯ࡵࡷࠤࡴࡸࡩࡨ࡫ࡱࡥࡱࡥࡣࡩࡴࡲࡱ࡮ࡻ࡭ࡠ࡮ࡤࡹࡳࡩࡨࠡ࠿ࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡰࡦࡻ࡮ࡤࡪ࠱ࡦ࡮ࡴࡤࠩ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭ࠪ࠽࡟ࡲ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡱࡧࡵ࡯ࡥ࡫ࠤࡂࠦࡡࡴࡻࡱࡧࠥ࠮࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸ࠯ࠠ࠾ࡀࠣࡿࡡࡴࡩࡧࠢࠫࠥࡧࡹࡴࡢࡥ࡮ࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠪࠢࡾࡠࡳࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦ࡯ࡳ࡫ࡪ࡭ࡳࡧ࡬ࡠࡥ࡫ࡶࡴࡳࡩࡶ࡯ࡢࡰࡦࡻ࡮ࡤࡪࠫࡰࡦࡻ࡮ࡤࡪࡒࡴࡹ࡯࡯࡯ࡵࠬ࠿ࡡࡴࡽ࡝ࡰ࡯ࡩࡹࠦࡣࡢࡲࡶ࠿ࡡࡴࡴࡳࡻࠣࡿࡡࡴࡣࡢࡲࡶࠤࡂࠦࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠪ࡞ࡱࠤࠥࢃࠠࡤࡣࡷࡧ࡭࠮ࡥࡹࠫࠣࡿࡡࡴࠠࠡࠢࠣࢁࡡࡴࠠࠡ࡫ࡩࠤ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࠮ࠦࡻ࡝ࡰࠣࠤࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡩ࡯࡯ࡰࡨࡧࡹࡕࡶࡦࡴࡆࡈࡕ࠮ࡻ࡝ࡰࠣࠤࠥࠦࠠࠡࡧࡱࡨࡵࡵࡩ࡯ࡶࡘࡖࡑࡀࠠࡡࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠧࡿࡪࡴࡣࡰࡦࡨ࡙ࡗࡏࡃࡰ࡯ࡳࡳࡳ࡫࡮ࡵࠪࡍࡗࡔࡔ࠮ࡴࡶࡵ࡭ࡳ࡭ࡩࡧࡻࠫࡧࡦࡶࡳࠪࠫࢀࡤ࠱ࡢ࡮ࠡࠢࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴ࡞ࡱࠤࠥࠦࠠࡾࠫ࡟ࡲࠥࠦࡽ࡝ࡰࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࠻ࠢࡣࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠩࢁࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭ࢂࡦࠬ࡝ࡰࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴ࡞ࡱࠤࠥࢃࠩ࡝ࡰࢀࡠࡳࡩ࡯࡯ࡵࡷࠤࡴࡸࡩࡨ࡫ࡱࡥࡱࡥࡣࡰࡰࡱࡩࡨࡺࠠ࠾ࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱ࠮ࡤࡪࡵࡳࡲ࡯ࡵ࡮࠰ࡦࡳࡳࡴࡥࡤࡶ࠱ࡦ࡮ࡴࡤࠩ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭ࠪ࠽࡟ࡲ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡨࡵ࡮࡯ࡧࡦࡸࠥࡃࠠࡢࡵࡼࡲࡨࠦࠨࡤࡱࡱࡲࡪࡩࡴࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁ࡜࡯ࠢࠣ࡭࡫ࠦࠨࠢࡤࡶࡸࡦࡩ࡫ࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠮ࠦࡻ࡝ࡰࠣࠤࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥࡵࡲࡪࡩ࡬ࡲࡦࡲ࡟ࡤࡱࡱࡲࡪࡩࡴࠩࡥࡲࡲࡳ࡫ࡣࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠫ࠾ࡠࡳࠦࠠࡾ࡞ࡱࠤࠥࡲࡥࡵࠢࡦࡥࡵࡹ࠻࡝ࡰࠣࠤࡹࡸࡹࠡࡽ࡟ࡲࠥࠦࠠࠡࡥࡤࡴࡸࠦ࠽ࠡࡌࡖࡓࡓ࠴ࡰࡢࡴࡶࡩ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡩࡡࡱࡵࠬࡠࡳࠦࠠࡾࠢࡦࡥࡹࡩࡨࠩࡧࡻ࠭ࠥࢁ࡜࡯ࠢࠣࢁࡡࡴࠠࠡࡥࡲࡲࡸࡺࠠ࡮ࡱࡧ࡭࡫࡯ࡥࡥࡇࡱࡨࡵࡵࡩ࡯ࡶࠣࡁࠥࡦࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࡡࠢ࠮ࠤࡪࡴࡣࡰࡦࡨ࡙ࡗࡏࡃࡰ࡯ࡳࡳࡳ࡫࡮ࡵࠪࡍࡗࡔࡔ࠮ࡴࡶࡵ࡭ࡳ࡭ࡩࡧࡻࠫࡧࡦࡶࡳࠪࠫ࠾ࡠࡳࠦࠠࡪࡨࠣࠬࡧࡹࡴࡢࡥ࡮ࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ࠭ࠥࢁ࡜࡯ࠢࠣࠤࠥࡸࡥࡵࡷࡵࡲࠥࡧࡷࡢ࡫ࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡨࡵ࡮࡯ࡧࡦࡸࡔࡼࡥࡳࡅࡇࡔ࠭ࢁ࡜࡯ࠢࠣࠤࠥࠦࠠࡦࡰࡧࡴࡴ࡯࡮ࡵࡗࡕࡐ࠿ࠦ࡭ࡰࡦ࡬ࡪ࡮࡫ࡤࡆࡰࡧࡴࡴ࡯࡮ࡵ࠮࡟ࡲࠥࠦࠠࠡࠢࠣ࠲࠳࠴ࡣࡰࡰࡱࡩࡨࡺࡏࡱࡶ࡬ࡳࡳࡹ࡜࡯ࠢࠣࠤࠥࢃࠩ࡝ࡰࠣࠤࢂࡢ࡮ࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤ࠳࠴࠮ࡤࡱࡱࡲࡪࡩࡴࡐࡲࡷ࡭ࡴࡴࡳ࠭࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࡝ࡰࠣࠤࢂ࠯࡜࡯ࡿ࡟ࡲࡱ࡫ࡴࠡࡄࡵࡳࡼࡹࡥࡳࡅࡲࡲࡹ࡫ࡸࡵ࠽࡟ࡲࡹࡸࡹࠡࡽ࡟ࡲࠥࠦࡣࡰࡰࡶࡸࠥࡶࡡࡵࡪࡐࡳࡩࡻ࡬ࡦࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭ࠨࡰࡢࡶ࡫ࠦ࠮ࡁ࡜࡯ࠢࠣࡧࡴࡴࡳࡵࠢࡳࡻࡈࡵࡲࡦࡒࡤࡸ࡭ࠦ࠽ࠡࡲࡤࡸ࡭ࡓ࡯ࡥࡷ࡯ࡩ࠳ࡪࡩࡳࡰࡤࡱࡪ࠮ࡲࡦࡳࡸ࡭ࡷ࡫࠮ࡳࡧࡶࡳࡱࡼࡥࠩࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠳ࡣࡰࡴࡨ࠳ࡵࡧࡣ࡬ࡣࡪࡩ࠳ࡰࡳࡰࡰࠥ࠭࠮ࡁ࡜࡯ࠢࠣࡆࡷࡵࡷࡴࡧࡵࡇࡴࡴࡴࡦࡺࡷࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨࡱࡣࡷ࡬ࡒࡵࡤࡶ࡮ࡨ࠲࡯ࡵࡩ࡯ࠪࡳࡻࡈࡵࡲࡦࡒࡤࡸ࡭࠲ࠠࠣ࡮࡬ࡦ࠴ࡩ࡬ࡪࡧࡱࡸ࠴ࡨࡲࡰࡹࡶࡩࡷࡉ࡯࡯ࡶࡨࡼࡹࠨࠩࠪ࠰ࡅࡶࡴࡽࡳࡦࡴࡆࡳࡳࡺࡥࡹࡶ࠾ࡠࡳࢃࠠࡤࡣࡷࡧ࡭ࠦࠨࡦࠫࠣࡿࡡࡴࠠࠡࡥࡲࡲࡸࡵ࡬ࡦ࠰ࡺࡥࡷࡴࠨࠣࡅࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡱࡵࡡࡥࠢࡅࡶࡴࡽࡳࡦࡴࡆࡳࡳࡺࡥࡹࡶࠣࡪࡷࡵ࡭ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠲ࡩ࡯ࡳࡧ࠽ࠦ࠱ࠦࡥ࠯࡯ࡨࡷࡸࡧࡧࡦࠫ࠾ࡠࡳࢃ࡜࡯ࡥࡲࡲࡸࡺࠠࡰࡴ࡬࡫࡮ࡴࡡ࡭ࡡࡱࡩࡼࡖࡡࡨࡧࠣࡁࠥࡈࡲࡰࡹࡶࡩࡷࡉ࡯࡯ࡶࡨࡼࡹ࠴ࡰࡳࡱࡷࡳࡹࡿࡰࡦ࠰ࡱࡩࡼࡖࡡࡨࡧ࠾ࡠࡳࡈࡲࡰࡹࡶࡩࡷࡉ࡯࡯ࡶࡨࡼࡹ࠴ࡰࡳࡱࡷࡳࡹࡿࡰࡦ࠰ࡱࡩࡼࡖࡡࡨࡧࠣࡁࠥࡧࡳࡺࡰࡦࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠮ࠩࠡࡽ࡟ࡲࠥࠦࡩࡧࠢࠫࡦࡸࡺࡡࡤ࡭ࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠬࠤࢀࡢ࡮ࠡࠢࠣࠤࡹࡸࡹࠡࡽ࡟ࡲࠥࠦࠠࠡࠢࠣࡧࡴࡴࡳࡵࠢࡥࡶࡴࡽࡳࡦࡴࠣࡁࠥࡺࡨࡪࡵ࠱ࡦࡷࡵࡷࡴࡧࡵࠤࠫࠬࠠࡵࡪ࡬ࡷ࠳ࡨࡲࡰࡹࡶࡩࡷ࠮ࠩ࠼࡞ࡱࠤࠥࠦࠠࠡࠢ࡯ࡩࡹࠦࡰࡳ࡫ࡰࡥࡷࡿࡃࡰࡰࡷࡩࡽࡺࠠ࠾ࠢࡥࡶࡴࡽࡳࡦࡴࠣࠪࠫࠦࡴࡺࡲࡨࡳ࡫ࠦࡢࡳࡱࡺࡷࡪࡸ࠮ࡤࡱࡱࡸࡪࡾࡴࡴࠢࡀࡁࡂࠦ࡜ࠨࡨࡸࡲࡨࡺࡩࡰࡰ࡟ࠫࠥࡅࠠࡣࡴࡲࡻࡸ࡫ࡲ࠯ࡥࡲࡲࡹ࡫ࡸࡵࡵࠫ࠭ࡠ࠶࡝ࠡ࠼ࠣࡲࡺࡲ࡬࠼࡞ࡱࠤࠥࠦࠠࠡࠢ࡬ࡪࠥ࠮ࠡࡱࡴ࡬ࡱࡦࡸࡹࡄࡱࡱࡸࡪࡾࡴࠡࠨࠩࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࠬࠦࠡࡶࡼࡴࡪࡵࡦࠡࡤࡵࡳࡼࡹࡥࡳ࠰ࡱࡩࡼࡉ࡯࡯ࡶࡨࡼࡹࠦ࠽࠾࠿ࠣࡠࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡜ࠨࠫࠣࡿࡡࡴࠠࠡࠢࠣࠤࠥࠦࠠࡱࡴ࡬ࡱࡦࡸࡹࡄࡱࡱࡸࡪࡾࡴࠡ࠿ࠣࡥࡼࡧࡩࡵࠢࡥࡶࡴࡽࡳࡦࡴ࠱ࡲࡪࡽࡃࡰࡰࡷࡩࡽࡺࠨࠪ࠽࡟ࡲࠥࠦࠠࠡࠢࠣࢁࡡࡴࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡵࡷࠤࡹࡧࡲࡨࡧࡷࡇࡴࡴࡴࡦࡺࡷࠤࡂࠦࡰࡳ࡫ࡰࡥࡷࡿࡃࡰࡰࡷࡩࡽࡺࠠࡽࡾࠣࡸ࡭࡯ࡳ࠼࡞ࡱࠤࠥࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡲࡪࡽࡐࡢࡩࡨ࠲ࡨࡧ࡬࡭ࠪࡷࡥࡷ࡭ࡥࡵࡅࡲࡲࡹ࡫ࡸࡵࠫ࠾ࡠࡳࠦࠠࠡࠢࢀࠤࡨࡧࡴࡤࡪࠣࠬࡪ࠯ࠠࡼ࡞ࡱࠤࠥࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡲࡪࡽࡐࡢࡩࡨ࠲ࡨࡧ࡬࡭ࠪࡷ࡬࡮ࡹࠩ࠼࡞ࡱࠤࠥࠦࠠࡾ࡞ࡱࠤࠥࢃࠠ࡝ࡰࠣࠤࡪࡲࡳࡦࠢࡾࡠࡳࠦࠠࠡࠢࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣࡳࡷ࡯ࡧࡪࡰࡤࡰࡤࡴࡥࡸࡒࡤ࡫ࡪ࠴ࡣࡢ࡮࡯ࠬࡹ࡮ࡩࡴࠫ࠾ࡠࡳࠦࠠࡾ࡞ࡱࢁࡀࡢ࡮࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱࡟ࡲࠬࣁ")
from ._version import __version__
bstack111l1l1ll_opy_ = None
CONFIG = {}
bstack1llll1111l_opy_ = {}
bstack11lll1l1l_opy_ = {}
bstack1llll1ll1_opy_ = None
bstack11111l1l_opy_ = None
SESSION_NAME = None
PLATFORM_INDEX = -1
bstack1ll1ll1111_opy_ = 0
bstack1l1ll1l111_opy_ = bstack1111lll111_opy_
bstack1111ll11l1_opy_ = 1
PARALLELISE_VANILLA_PYTHON = False
PARALLELISE_THREADING_PYTHON = False
FRAMEWORK_NAME = bstack1ll1lll_opy_ (u"ࠩࠪࣂ")
bstack11llllll1_opy_ = bstack1ll1lll_opy_ (u"ࠪࠫࣃ")
bstack1ll1ll1l1_opy_ = False
BROWSERSTACK_AUTOMATION = True
bstack1111l1l1l1_opy_ = False
bstack1lll111ll_opy_ = bstack1ll1lll_opy_ (u"ࠫࠬࣄ")
bstack1lllllllll_opy_ = []
bstack1ll111ll11_opy_ = threading.Lock()
bstack1l1l111ll_opy_ = threading.Lock()
bstack1ll111llll_opy_ = None
bstack1lllll111_opy_ = bstack1ll1lll_opy_ (u"ࠬ࠭ࣅ")
SELENIUM_OR_PLAYWRIGHT_INSTALLED = False
bstack1ll1l1l1ll_opy_ = None
bstack11ll1111l1_opy_ = None
bstack111llll11l_opy_ = None
bstack1l1l11ll1l_opy_ = -1
bstack11l111l11_opy_ = os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"࠭ࡾࠨࣆ")), bstack1ll1lll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧࣇ"), bstack1ll1lll_opy_ (u"ࠨ࠰ࡵࡳࡧࡵࡴ࠮ࡴࡨࡴࡴࡸࡴ࠮ࡪࡨࡰࡵ࡫ࡲ࠯࡬ࡶࡳࡳ࠭ࣈ"))
bstack11111lll_opy_ = 0
bstack1l11ll1ll_opy_ = 0
bstack111l11llll_opy_ = []
bstack1ll11l11_opy_ = []
ROBOT_PYTHON_ERRORS = []
bstack1lll111lll_opy_ = []
bstack1ll111l11l_opy_ = bstack1ll1lll_opy_ (u"ࠩࠪࣉ")
bstack11111lllll_opy_ = bstack1ll1lll_opy_ (u"ࠪࠫ࣊")
bstack1111111l1_opy_ = False
bstack11l1llll1l_opy_ = False
bstack1l1llllll1_opy_ = {}
bstack1lllllll11_opy_ = {}
bstack111llll111_opy_ = None
bstack1l1lll1111_opy_ = None
bstack11ll111ll_opy_ = None
bstack11lll1lll1_opy_ = None
bstack1llllll1l_opy_ = None
bstack1l111ll1l_opy_ = None
bstack11l1ll1l1_opy_ = None
bstack11l1l1lll1_opy_ = None
bstack1ll1111ll_opy_ = None
bstack1l1ll111l1_opy_ = None
bstack1ll1lllll_opy_ = None
bstack1l1l11l11_opy_ = None
bstack11111l1111_opy_ = None
bstack11l1l11111_opy_ = None
bstack111l111l11_opy_ = None
bstack1ll1ll1l_opy_ = None
bstack111l111111_opy_ = None
bstack111lllll1_opy_ = None
bstack111ll11lll_opy_ = None
bstack1ll1l111_opy_ = None
bstack1l1l11l11l_opy_ = None
bstack11lll1ll1l_opy_ = None
bstack1l11l11l1_opy_ = None
thread_local = threading.local()
bstack1llll1ll_opy_ = False
bstack1111lllll_opy_ = bstack1ll1lll_opy_ (u"ࠦࠧ࣋")
_11l11l111_opy_ = None
logger = logger_utils.get_logger(__name__, bstack1l1ll1l111_opy_)
automation_logger = logger_utils.get_automation_logger(__name__)
global_config = Config.get_instance()
percy = bstack1l11lll1ll_opy_()
bstack1111l11l_opy_ = bstack1l1111lll1_opy_()
bstack1ll1l1lll1_opy_ = bstack1l111l1l_opy_()
def bstack1llll1ll11_opy_():
  global CONFIG
  global bstack1111111l1_opy_
  global global_config
  testContextOptions = bstack1l1111ll11_opy_(CONFIG)
  if bstack1l111llll_opy_(CONFIG):
    if (bstack1ll1lll_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ࣌") in testContextOptions and str(testContextOptions[bstack1ll1lll_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ࣍")]).lower() == bstack1ll1lll_opy_ (u"ࠧࡵࡴࡸࡩࠬ࣎")):
      bstack1111111l1_opy_ = True
      global_config.bstack1l111111_opy_(True)
    if (bstack1ll1lll_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷ࣏ࠬ") in testContextOptions and str(testContextOptions[bstack1ll1lll_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࣐࠭")]).lower() == bstack1ll1lll_opy_ (u"ࠪࡸࡷࡻࡥࠨ࣑")):
      global_config.bstack11lll1llll_opy_(True)
  else:
    bstack1111111l1_opy_ = True
    global_config.bstack1l111111_opy_(True)
    global_config.bstack11lll1llll_opy_(True)
def bstack1l1l1l1111_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1l11ll1l1l_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1ll11l1l1_opy_():
  global bstack1lllllll11_opy_
  args = sys.argv
  for i in range(len(args)):
    if bstack1ll1lll_opy_ (u"ࠦ࠲࠳ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡨࡵ࡮ࡧ࡫ࡪࡪ࡮ࡲࡥ࣒ࠣ") == args[i].lower() or bstack1ll1lll_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰࡰࡩ࡭࡬ࠨ࣓") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      bstack1lllllll11_opy_[bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࡤࡌࡉࡍࡇࠪࣔ")] = path
      return path
  return None
bstack1l11l11lll_opy_ = re.compile(bstack1ll1lll_opy_ (u"ࡲࠣ࠰࠭ࡃࡡࠪࡻࠩ࠰࠭ࡃ࠮ࢃ࠮ࠫࡁࠥࣕ"))
def bstack1l1lllll1_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1l11l11lll_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack1ll1lll_opy_ (u"ࠣࠦࡾࠦࣖ") + group + bstack1ll1lll_opy_ (u"ࠤࢀࠦࣗ"), os.environ.get(group))
  return value
def bstack1l111l1lll_opy_():
  global bstack1l11l11l1_opy_
  if bstack1l11l11l1_opy_ is None:
        bstack1l11l11l1_opy_ = bstack1ll11l1l1_opy_()
  bstack11l1111l1_opy_ = bstack1l11l11l1_opy_
  if bstack11l1111l1_opy_ and os.path.exists(os.path.abspath(bstack11l1111l1_opy_)):
    fileName = bstack11l1111l1_opy_
  if bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋࠧࣘ") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨࣙ")])) and not bstack1ll1lll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡑࡥࡲ࡫ࠧࣚ") in locals():
    fileName = os.environ[bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࡤࡌࡉࡍࡇࠪࣛ")]
  if bstack1ll1lll_opy_ (u"ࠧࡧ࡫࡯ࡩࡓࡧ࡭ࡦࠩࣜ") in locals():
    bstack1l11111_opy_ = os.path.abspath(fileName)
  else:
    bstack1l11111_opy_ = bstack1ll1lll_opy_ (u"ࠨࠩࣝ")
  bstack1l111111l1_opy_ = os.getcwd()
  bstack1l1l11llll_opy_ = bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬࣞ")
  bstack11l1ll11l1_opy_ = bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡥࡲࡲࠧࣟ")
  while (not os.path.exists(bstack1l11111_opy_)) and bstack1l111111l1_opy_ != bstack1ll1lll_opy_ (u"ࠦࠧ࣠"):
    bstack1l11111_opy_ = os.path.join(bstack1l111111l1_opy_, bstack1l1l11llll_opy_)
    if not os.path.exists(bstack1l11111_opy_):
      bstack1l11111_opy_ = os.path.join(bstack1l111111l1_opy_, bstack11l1ll11l1_opy_)
    if bstack1l111111l1_opy_ != os.path.dirname(bstack1l111111l1_opy_):
      bstack1l111111l1_opy_ = os.path.dirname(bstack1l111111l1_opy_)
    else:
      bstack1l111111l1_opy_ = bstack1ll1lll_opy_ (u"ࠧࠨ࣡")
  bstack1l11l11l1_opy_ = bstack1l11111_opy_ if os.path.exists(bstack1l11111_opy_) else None
  return bstack1l11l11l1_opy_
def bstack1l1lll1l1_opy_(config):
    if bstack1ll1lll_opy_ (u"࠭ࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬࠭࣢") in config:
      config[bstack1ll1lll_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࣣࠫ")] = config[bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹࡘࡥࡱࡱࡵࡸ࡮ࡴࡧࠨࣤ")]
    if bstack1ll1lll_opy_ (u"ࠩࡷࡩࡸࡺࡒࡦࡲࡲࡶࡹ࡯࡮ࡨࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣥ") in config:
      config[bstack1ll1lll_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࣦࠧ")] = config[bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࡓࡵࡺࡩࡰࡰࡶࠫࣧ")]
def bstack1ll11ll1l1_opy_():
  bstack1l11111_opy_ = bstack1l111l1lll_opy_()
  if not os.path.exists(bstack1l11111_opy_):
    bstack1l1111ll_opy_(
      bstack1l11l111l1_opy_.format(os.getcwd()))
  try:
    with open(bstack1l11111_opy_, bstack1ll1lll_opy_ (u"ࠬࡸࠧࣨ")) as stream:
      yaml.add_implicit_resolver(bstack1ll1lll_opy_ (u"ࠨࠡࡱࡣࡷ࡬ࡪࡾࣩࠢ"), bstack1l11l11lll_opy_)
      yaml.add_constructor(bstack1ll1lll_opy_ (u"ࠢࠢࡲࡤࡸ࡭࡫ࡸࠣ࣪"), bstack1l1lllll1_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      bstack1l1lll1l1_opy_(config)
      return config
  except:
    with open(bstack1l11111_opy_, bstack1ll1lll_opy_ (u"ࠨࡴࠪ࣫")) as stream:
      try:
        config = yaml.safe_load(stream)
        bstack1l1lll1l1_opy_(config)
        return config
      except yaml.YAMLError as exc:
        bstack1l1111ll_opy_(bstack1lll11l1l_opy_.format(str(exc)))
def bstack1l1111l1l_opy_(config):
  bstack1llll1lll_opy_ = bstack11l1l1l1l1_opy_(config)
  for option in list(bstack1llll1lll_opy_):
    if option.lower() in bstack1ll1ll1l1l_opy_ and option != bstack1ll1ll1l1l_opy_[option.lower()]:
      bstack1llll1lll_opy_[bstack1ll1ll1l1l_opy_[option.lower()]] = bstack1llll1lll_opy_[option]
      del bstack1llll1lll_opy_[option]
  return config
def bstack1l1ll1111_opy_():
  global bstack11lll1l1l_opy_
  for key, bstack11llll1lll_opy_ in bstack11111l11l1_opy_.items():
    if isinstance(bstack11llll1lll_opy_, list):
      for var in bstack11llll1lll_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack11lll1l1l_opy_[key] = os.environ[var]
          break
    elif bstack11llll1lll_opy_ in os.environ and os.environ[bstack11llll1lll_opy_] and str(os.environ[bstack11llll1lll_opy_]).strip():
      bstack11lll1l1l_opy_[key] = os.environ[bstack11llll1lll_opy_]
  if bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ࣬") in os.environ:
    bstack11lll1l1l_opy_[bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹ࣭ࠧ")] = {}
    bstack11lll1l1l_opy_[bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ࣮")][bstack1ll1lll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣯ࠧ")] = os.environ[bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨࣰ")]
def bstack1l1ll11lll_opy_():
  global bstack1llll1111l_opy_
  global bstack1lll111ll_opy_
  global bstack1lllllll11_opy_
  bstack1lllllll1_opy_ = []
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) - 1 and bstack1ll1lll_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࣱࠪ").lower() == val.lower():
      bstack1llll1111l_opy_[bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࣲࠬ")] = {}
      bstack1llll1111l_opy_[bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࣳ")][bstack1ll1lll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣴ")] = sys.argv[idx + 1]
      bstack1lllllll1_opy_.extend([idx, idx + 1])
      break
  for key, bstack1l11l11l11_opy_ in bstack11llll111_opy_.items():
    if isinstance(bstack1l11l11l11_opy_, list):
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        for var in bstack1l11l11l11_opy_:
          if bstack1ll1lll_opy_ (u"ࠫ࠲࠳ࠧࣵ") + var.lower() == val.lower() and key not in bstack1llll1111l_opy_:
            bstack1llll1111l_opy_[key] = sys.argv[idx + 1]
            bstack1lll111ll_opy_ += bstack1ll1lll_opy_ (u"ࠬࠦ࠭࠮ࣶࠩ") + var + bstack1ll1lll_opy_ (u"࠭ࠠࠨࣷ") + shlex.quote(sys.argv[idx + 1])
            bstack1lll11lll_opy_(bstack1lllllll11_opy_, key, sys.argv[idx + 1])
            bstack1lllllll1_opy_.extend([idx, idx + 1])
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        if bstack1ll1lll_opy_ (u"ࠧ࠮࠯ࠪࣸ") + bstack1l11l11l11_opy_.lower() == val.lower() and key not in bstack1llll1111l_opy_:
          bstack1llll1111l_opy_[key] = sys.argv[idx + 1]
          bstack1lll111ll_opy_ += bstack1ll1lll_opy_ (u"ࠨࠢ࠰࠱ࣹࠬ") + bstack1l11l11l11_opy_ + bstack1ll1lll_opy_ (u"ࣺࠩࠣࠫ") + shlex.quote(sys.argv[idx + 1])
          bstack1lll11lll_opy_(bstack1lllllll11_opy_, key, sys.argv[idx + 1])
          bstack1lllllll1_opy_.extend([idx, idx + 1])
  for idx in sorted(set(bstack1lllllll1_opy_), reverse=True):
    if idx < len(sys.argv):
      del sys.argv[idx]
def bstack1ll11l1ll1_opy_(config):
  bstack111lll11ll_opy_ = config.keys()
  for bstack111ll1l1ll_opy_, bstack1llll1l1_opy_ in bstack1lll111ll1_opy_.items():
    if bstack1llll1l1_opy_ in bstack111lll11ll_opy_:
      config[bstack111ll1l1ll_opy_] = config[bstack1llll1l1_opy_]
      del config[bstack1llll1l1_opy_]
  for bstack111ll1l1ll_opy_, bstack1llll1l1_opy_ in bstack11111ll111_opy_.items():
    if isinstance(bstack1llll1l1_opy_, list):
      for bstack1l1lllll_opy_ in bstack1llll1l1_opy_:
        if bstack1l1lllll_opy_ in bstack111lll11ll_opy_:
          config[bstack111ll1l1ll_opy_] = config[bstack1l1lllll_opy_]
          del config[bstack1l1lllll_opy_]
          break
    elif bstack1llll1l1_opy_ in bstack111lll11ll_opy_:
      config[bstack111ll1l1ll_opy_] = config[bstack1llll1l1_opy_]
      del config[bstack1llll1l1_opy_]
  for bstack1l1lllll_opy_ in list(config):
    for bstack111ll11l11_opy_ in bstack11llll1l11_opy_:
      if bstack1l1lllll_opy_.lower() == bstack111ll11l11_opy_.lower() and bstack1l1lllll_opy_ != bstack111ll11l11_opy_:
        config[bstack111ll11l11_opy_] = config[bstack1l1lllll_opy_]
        del config[bstack1l1lllll_opy_]
  bstack11l1ll1lll_opy_ = [{}]
  if not config.get(bstack1ll1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣻ")):
    config[bstack1ll1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣼ")] = [{}]
  bstack11l1ll1lll_opy_ = config[bstack1ll1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨࣽ")]
  for platform in bstack11l1ll1lll_opy_:
    for bstack1l1lllll_opy_ in list(platform):
      for bstack111ll11l11_opy_ in bstack11llll1l11_opy_:
        if bstack1l1lllll_opy_.lower() == bstack111ll11l11_opy_.lower() and bstack1l1lllll_opy_ != bstack111ll11l11_opy_:
          platform[bstack111ll11l11_opy_] = platform[bstack1l1lllll_opy_]
          del platform[bstack1l1lllll_opy_]
  for bstack111ll1l1ll_opy_, bstack1llll1l1_opy_ in bstack11111ll111_opy_.items():
    for platform in bstack11l1ll1lll_opy_:
      if isinstance(bstack1llll1l1_opy_, list):
        for bstack1l1lllll_opy_ in bstack1llll1l1_opy_:
          if bstack1l1lllll_opy_ in platform:
            platform[bstack111ll1l1ll_opy_] = platform[bstack1l1lllll_opy_]
            del platform[bstack1l1lllll_opy_]
            break
      elif bstack1llll1l1_opy_ in platform:
        platform[bstack111ll1l1ll_opy_] = platform[bstack1llll1l1_opy_]
        del platform[bstack1llll1l1_opy_]
  for bstack1l11111ll1_opy_ in bstack1ll1111111_opy_:
    if bstack1l11111ll1_opy_ in config:
      if not bstack1ll1111111_opy_[bstack1l11111ll1_opy_] in config:
        config[bstack1ll1111111_opy_[bstack1l11111ll1_opy_]] = {}
      config[bstack1ll1111111_opy_[bstack1l11111ll1_opy_]].update(config[bstack1l11111ll1_opy_])
      del config[bstack1l11111ll1_opy_]
  for platform in bstack11l1ll1lll_opy_:
    for bstack1l11111ll1_opy_ in bstack1ll1111111_opy_:
      if bstack1l11111ll1_opy_ in list(platform):
        if not bstack1ll1111111_opy_[bstack1l11111ll1_opy_] in platform:
          platform[bstack1ll1111111_opy_[bstack1l11111ll1_opy_]] = {}
        platform[bstack1ll1111111_opy_[bstack1l11111ll1_opy_]].update(platform[bstack1l11111ll1_opy_])
        del platform[bstack1l11111ll1_opy_]
  config = bstack1l1111l1l_opy_(config)
  return config
def bstack111ll1111_opy_(config):
  global bstack11llllll1_opy_
  bstack1l1l111ll1_opy_ = False
  if bstack1ll1lll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪࣾ") in config and str(config[bstack1ll1lll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫࣿ")]).lower() != bstack1ll1lll_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧऀ"):
    if bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ँ") not in config or str(config[bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧं")]).lower() == bstack1ll1lll_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪः"):
      config[bstack1ll1lll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫऄ")] = False
    else:
      bstack1l11111l_opy_ = bstack1ll11ll11_opy_()
      if bstack1ll1lll_opy_ (u"࠭ࡩࡴࡖࡵ࡭ࡦࡲࡇࡳ࡫ࡧࠫअ") in bstack1l11111l_opy_:
        if not bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫआ") in config:
          config[bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬइ")] = {}
        config[bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ई")][bstack1ll1lll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬउ")] = bstack1ll1lll_opy_ (u"ࠫࡦࡺࡳ࠮ࡴࡨࡴࡪࡧࡴࡦࡴࠪऊ")
        bstack1l1l111ll1_opy_ = True
        bstack11llllll1_opy_ = config[bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩऋ")].get(bstack1ll1lll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨऌ"))
  if bstack1l111llll_opy_(config) and bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫऍ") in config and str(config[bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬऎ")]).lower() != bstack1ll1lll_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨए") and not bstack1l1l111ll1_opy_:
    if not bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧऐ") in config:
      config[bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऑ")] = {}
    if not config[bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩऒ")].get(bstack1ll1lll_opy_ (u"࠭ࡳ࡬࡫ࡳࡆ࡮ࡴࡡࡳࡻࡌࡲ࡮ࡺࡩࡢ࡮࡬ࡷࡦࡺࡩࡰࡰࠪओ")) and not bstack1ll1lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऔ") in config[bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬक")]:
      current_time = datetime.datetime.now()
      bstack1ll1ll1lll_opy_ = current_time.strftime(bstack1ll1lll_opy_ (u"ࠩࠨࡨࡤࠫࡢࡠࠧࡋࠩࡒ࠭ख"))
      hostname = socket.gethostname()
      bstack1l1lll1lll_opy_ = bstack1ll1lll_opy_ (u"ࠪࠫग").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1ll1lll_opy_ (u"ࠫࢀࢃ࡟ࡼࡿࡢࡿࢂ࠭घ").format(bstack1ll1ll1lll_opy_, hostname, bstack1l1lll1lll_opy_)
      config[bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩङ")][bstack1ll1lll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨच")] = identifier
    bstack11llllll1_opy_ = config[bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫछ")].get(bstack1ll1lll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪज"))
  return config
def bstack1l1l11111_opy_():
  bstack111lllll_opy_ =  bstack1l1l1ll1l_opy_()[bstack1ll1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠨझ")]
  return bstack111lllll_opy_ if bstack111lllll_opy_ else -1
def bstack1l1ll1l1ll_opy_(bstack111lllll_opy_):
  global CONFIG
  if not bstack1ll1lll_opy_ (u"ࠪࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬञ") in CONFIG[bstack1ll1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ट")]:
    return
  CONFIG[bstack1ll1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧठ")] = CONFIG[bstack1ll1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨड")].replace(
    bstack1ll1lll_opy_ (u"ࠧࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩढ"),
    str(bstack111lllll_opy_)
  )
def bstack1l111ll1_opy_():
  global CONFIG
  if not bstack1ll1lll_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧण") in CONFIG[bstack1ll1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫत")]:
    return
  current_time = datetime.datetime.now()
  bstack1ll1ll1lll_opy_ = current_time.strftime(bstack1ll1lll_opy_ (u"ࠪࠩࡩ࠳ࠥࡣ࠯ࠨࡌ࠿ࠫࡍࠨथ"))
  CONFIG[bstack1ll1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭द")] = CONFIG[bstack1ll1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧध")].replace(
    bstack1ll1lll_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬन"),
    bstack1ll1ll1lll_opy_
  )
def bstack111l1ll1_opy_():
  global CONFIG
  if bstack1ll1lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऩ") in CONFIG and not bool(CONFIG[bstack1ll1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪप")]):
    del CONFIG[bstack1ll1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫफ")]
    return
  if not bstack1ll1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬब") in CONFIG:
    CONFIG[bstack1ll1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭भ")] = bstack1ll1lll_opy_ (u"ࠬࠩࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨम")
  if bstack1ll1lll_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬय") in CONFIG[bstack1ll1lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩर")]:
    bstack1l111ll1_opy_()
    os.environ[bstack1ll1lll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬऱ")] = CONFIG[bstack1ll1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫल")]
  if not bstack1ll1lll_opy_ (u"ࠪࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬळ") in CONFIG[bstack1ll1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ऴ")]:
    return
  bstack111lllll_opy_ = bstack1ll1lll_opy_ (u"ࠬ࠭व")
  bstack1lll11l111_opy_ = bstack1l1l11111_opy_()
  if bstack1lll11l111_opy_ != -1:
    bstack111lllll_opy_ = bstack1ll1lll_opy_ (u"࠭ࡃࡊࠢࠪश") + str(bstack1lll11l111_opy_)
  if bstack111lllll_opy_ == bstack1ll1lll_opy_ (u"ࠧࠨष"):
    bstack1l1l1lll1l_opy_ = bstack1l11lll111_opy_(CONFIG[bstack1ll1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫस")])
    if bstack1l1l1lll1l_opy_ != -1:
      bstack111lllll_opy_ = str(bstack1l1l1lll1l_opy_)
  if bstack111lllll_opy_:
    bstack1l1ll1l1ll_opy_(bstack111lllll_opy_)
    os.environ[bstack1ll1lll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ह")] = CONFIG[bstack1ll1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬऺ")]
def bstack1ll11l1l11_opy_(bstack1ll1ll1ll_opy_, bstack111lll1111_opy_, path):
  json_data = {
    bstack1ll1lll_opy_ (u"ࠫ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨऻ"): bstack111lll1111_opy_
  }
  if os.path.exists(path):
    bstack1l111lll11_opy_ = json.load(open(path, bstack1ll1lll_opy_ (u"ࠬࡸࡢࠨ़")))
  else:
    bstack1l111lll11_opy_ = {}
  bstack1l111lll11_opy_[bstack1ll1ll1ll_opy_] = json_data
  with open(path, bstack1ll1lll_opy_ (u"ࠨࡷࠬࠤऽ")) as outfile:
    json.dump(bstack1l111lll11_opy_, outfile)
def bstack1l11lll111_opy_(bstack1ll1ll1ll_opy_):
  bstack1ll1ll1ll_opy_ = str(bstack1ll1ll1ll_opy_)
  bstack111l11l11_opy_ = os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"ࠧࡿࠩा")), bstack1ll1lll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨि"))
  try:
    if not os.path.exists(bstack111l11l11_opy_):
      os.makedirs(bstack111l11l11_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"ࠩࢁࠫी")), bstack1ll1lll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪु"), bstack1ll1lll_opy_ (u"ࠫ࠳ࡨࡵࡪ࡮ࡧ࠱ࡳࡧ࡭ࡦ࠯ࡦࡥࡨ࡮ࡥ࠯࡬ࡶࡳࡳ࠭ू"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1ll1lll_opy_ (u"ࠬࡽࠧृ")):
        pass
      with open(file_path, bstack1ll1lll_opy_ (u"ࠨࡷࠬࠤॄ")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1ll1lll_opy_ (u"ࠧࡳࠩॅ")) as bstack1lll1111ll_opy_:
      bstack11l11ll11l_opy_ = json.load(bstack1lll1111ll_opy_)
    if bstack1ll1ll1ll_opy_ in bstack11l11ll11l_opy_:
      bstack1lll1lll_opy_ = bstack11l11ll11l_opy_[bstack1ll1ll1ll_opy_][bstack1ll1lll_opy_ (u"ࠨ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬॆ")]
      bstack1l1l11lll1_opy_ = int(bstack1lll1lll_opy_) + 1
      bstack1ll11l1l11_opy_(bstack1ll1ll1ll_opy_, bstack1l1l11lll1_opy_, file_path)
      return bstack1l1l11lll1_opy_
    else:
      bstack1ll11l1l11_opy_(bstack1ll1ll1ll_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warning(bstack11l1ll1l11_opy_.format(str(e)))
    return -1
def bstack1ll1l1ll1_opy_(config):
  if not config[bstack1ll1lll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫे")] or not config[bstack1ll1lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ै")]:
    return True
  else:
    return False
def bstack1lllllll1l_opy_(config, index=0):
  global bstack1ll1ll1l1_opy_
  bstack1llllllll1_opy_ = {}
  caps = bstack11111l1ll1_opy_ + bstack1l11l1ll1_opy_
  if config.get(bstack1ll1lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨॉ"), False):
    bstack1llllllll1_opy_[bstack1ll1lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩॊ")] = True
    bstack1llllllll1_opy_[bstack1ll1lll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪो")] = config.get(bstack1ll1lll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࡓࡵࡺࡩࡰࡰࡶࠫौ"), {})
  if bstack1ll1ll1l1_opy_:
    caps += bstack11l11111_opy_
  for key in config:
    if key in caps + [bstack1ll1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶ्ࠫ")]:
      continue
    bstack1llllllll1_opy_[key] = config[key]
  if bstack1ll1lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॎ") in config:
    for bstack1l1l1l11ll_opy_ in config[bstack1ll1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॏ")][index]:
      if bstack1l1l1l11ll_opy_ in caps:
        continue
      bstack1llllllll1_opy_[bstack1l1l1l11ll_opy_] = config[bstack1ll1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॐ")][index][bstack1l1l1l11ll_opy_]
  bstack1llllllll1_opy_[bstack1ll1lll_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧ॑")] = socket.gethostname()
  if bstack1ll1lll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴ॒ࠧ") in bstack1llllllll1_opy_:
    del (bstack1llllllll1_opy_[bstack1ll1lll_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨ॓")])
  return bstack1llllllll1_opy_
def bstack1lllll111l_opy_(config):
  global bstack1ll1ll1l1_opy_
  bstack1lll1l1l1_opy_ = {}
  caps = bstack1l11l1ll1_opy_
  if bstack1ll1ll1l1_opy_:
    caps += bstack11l11111_opy_
  for key in caps:
    if key in config:
      bstack1lll1l1l1_opy_[key] = config[key]
  return bstack1lll1l1l1_opy_
def bstack1lllll11ll_opy_(bstack1llllllll1_opy_, bstack1lll1l1l1_opy_):
  bstack11lll1111_opy_ = {}
  for key in bstack1llllllll1_opy_.keys():
    if key in bstack1lll111ll1_opy_:
      bstack11lll1111_opy_[bstack1lll111ll1_opy_[key]] = bstack1llllllll1_opy_[key]
    else:
      bstack11lll1111_opy_[key] = bstack1llllllll1_opy_[key]
  for key in bstack1lll1l1l1_opy_:
    if key in bstack1lll111ll1_opy_:
      bstack11lll1111_opy_[bstack1lll111ll1_opy_[key]] = bstack1lll1l1l1_opy_[key]
    else:
      bstack11lll1111_opy_[key] = bstack1lll1l1l1_opy_[key]
  return bstack11lll1111_opy_
def get_caps(config, index=0):
  global bstack1ll1ll1l1_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack1lll11111l_opy_ = bstack1l1llll1ll_opy_(bstack1l1lll111l_opy_, config, logger)
  bstack1lll1l1l1_opy_ = bstack1lllll111l_opy_(config)
  bstack1lll111111_opy_ = bstack1l11l1ll1_opy_
  bstack1lll111111_opy_ += bstack11ll1lll11_opy_
  bstack1lll1l1l1_opy_ = update(bstack1lll1l1l1_opy_, bstack1lll11111l_opy_)
  if bstack1ll1ll1l1_opy_:
    bstack1lll111111_opy_ += bstack11l11111_opy_
  if bstack1ll1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ॔") in config:
    if bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧॕ") in config[bstack1ll1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॖ")][index]:
      caps[bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩॗ")] = config[bstack1ll1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨक़")][index][bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫख़")]
    if bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨग़") in config[bstack1ll1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫज़")][index]:
      caps[bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪड़")] = str(config[bstack1ll1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ढ़")][index][bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬफ़")])
    bstack11llll1111_opy_ = bstack1l1llll1ll_opy_(bstack1l1lll111l_opy_, config[bstack1ll1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨय़")][index], logger)
    bstack1lll111111_opy_ += list(bstack11llll1111_opy_.keys())
    for bstack1l11lll1_opy_ in bstack1lll111111_opy_:
      if bstack1l11lll1_opy_ in config[bstack1ll1lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩॠ")][index]:
        if bstack1l11lll1_opy_ == bstack1ll1lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩॡ"):
          try:
            bstack11llll1111_opy_[bstack1l11lll1_opy_] = str(config[bstack1ll1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫॢ")][index][bstack1l11lll1_opy_] * 1.0)
          except:
            bstack11llll1111_opy_[bstack1l11lll1_opy_] = str(config[bstack1ll1lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॣ")][index][bstack1l11lll1_opy_])
        else:
          bstack11llll1111_opy_[bstack1l11lll1_opy_] = config[bstack1ll1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭।")][index][bstack1l11lll1_opy_]
        del (config[bstack1ll1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ॥")][index][bstack1l11lll1_opy_])
    bstack1lll1l1l1_opy_ = update(bstack1lll1l1l1_opy_, bstack11llll1111_opy_)
  bstack1llllllll1_opy_ = bstack1lllllll1l_opy_(config, index)
  for bstack1l1lllll_opy_ in bstack1l11l1ll1_opy_ + list(bstack1lll11111l_opy_.keys()):
    if bstack1l1lllll_opy_ in bstack1llllllll1_opy_:
      bstack1lll1l1l1_opy_[bstack1l1lllll_opy_] = bstack1llllllll1_opy_[bstack1l1lllll_opy_]
      del (bstack1llllllll1_opy_[bstack1l1lllll_opy_])
  if bstack11l11l1111_opy_(config):
    bstack1llllllll1_opy_[bstack1ll1lll_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ०")] = True
    caps.update(bstack1lll1l1l1_opy_)
    caps[bstack1ll1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ१")] = bstack1llllllll1_opy_
  else:
    bstack1llllllll1_opy_[bstack1ll1lll_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧ२")] = False
    caps.update(bstack1lllll11ll_opy_(bstack1llllllll1_opy_, bstack1lll1l1l1_opy_))
    if bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭३") in caps:
      caps[bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪ४")] = caps[bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ५")]
      del (caps[bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ६")])
    if bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭७") in caps:
      caps[bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ८")] = caps[bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ९")]
      del (caps[bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ॰")])
  return caps
def bstack1ll111lll_opy_():
  global bstack1lllll111_opy_
  global CONFIG
  if bstack1lllll111_opy_ != bstack1ll1lll_opy_ (u"ࠩࠪॱ") and (bstack1lllll111_opy_.startswith(bstack1ll1lll_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫॲ")) or bstack1lllll111_opy_.startswith(bstack1ll1lll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࠭ॳ"))):
    return bstack1lllll111_opy_
  if bstack1l11ll1l1l_opy_() <= version.parse(bstack1ll1lll_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬॴ")):
    if bstack1lllll111_opy_ != bstack1ll1lll_opy_ (u"࠭ࠧॵ"):
      return bstack1ll1lll_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣॶ") + bstack1lllll111_opy_ + bstack1ll1lll_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧॷ")
    return bstack1l1l11l111_opy_
  if bstack1lllll111_opy_ != bstack1ll1lll_opy_ (u"ࠩࠪॸ"):
    return bstack1ll1lll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧॹ") + bstack1lllll111_opy_ + bstack1ll1lll_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧॺ")
  return HTTPS_HUB
def bstack11l1l1ll1_opy_(options):
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
def bstack1l11ll1l11_opy_(options, bstack11l11lll_opy_):
  for bstack1l11l1ll1l_opy_ in bstack11l11lll_opy_:
    if bstack1l11l1ll1l_opy_ in [bstack1ll1lll_opy_ (u"࠭ࡡࡳࡩࡶࠫॼ"), bstack1ll1lll_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫॽ")]:
      continue
    if bstack1l11l1ll1l_opy_ in options._experimental_options:
      options._experimental_options[bstack1l11l1ll1l_opy_] = update(options._experimental_options[bstack1l11l1ll1l_opy_],
                                                         bstack11l11lll_opy_[bstack1l11l1ll1l_opy_])
    else:
      options.add_experimental_option(bstack1l11l1ll1l_opy_, bstack11l11lll_opy_[bstack1l11l1ll1l_opy_])
  if bstack1ll1lll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ॾ") in bstack11l11lll_opy_:
    for arg in bstack11l11lll_opy_[bstack1ll1lll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॿ")]:
      options.add_argument(arg)
    del (bstack11l11lll_opy_[bstack1ll1lll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨঀ")])
  if bstack1ll1lll_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨঁ") in bstack11l11lll_opy_:
    for ext in bstack11l11lll_opy_[bstack1ll1lll_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩং")]:
      try:
        options.add_extension(ext)
      except OSError:
        options.add_encoded_extension(ext)
    del (bstack11l11lll_opy_[bstack1ll1lll_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪঃ")])
def bstack11111ll1l_opy_(options):
  global CONFIG
  global bstack1111l1l1l1_opy_
  try:
    if not bstack1111l1l1l1_opy_ or not options:
      return options
    from bstack_utils.bstack1lllll1lll_opy_ import bstack1l1ll1111l_opy_
    bstack1l11l1lll_opy_ = bstack1l1ll1111l_opy_(options, bstack111ll1lll_opy_=bstack1ll1lll_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢ঄"))
    if bstack1l11l1lll_opy_ > 0:
      logger.debug(bstack1ll1lll_opy_ (u"ࠣࡎࡲࡥࡩࠦࡴࡦࡵࡷ࡭ࡳ࡭࠺ࠡࡃࡧࡨࡪࡪࠠࡼࡿࠣࡨࡪ࡬ࡡࡶ࡮ࡷࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠠࡧࡱࡵࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠦঅ").format(bstack1l11l1lll_opy_))
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡯࡮࡫ࡧࡦࡸࠥࡲ࡯ࡢࡦࠣࡸࡪࡹࡴࡪࡰࡪࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡴࡶࡴࡪࡱࡱࡷ࠿ࠦࡻࡾࠤআ").format(e))
  return options
def bstack1ll11l11ll_opy_(options, bstack111l1l1l_opy_):
  if bstack1ll1lll_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩই") in bstack111l1l1l_opy_:
    for bstack1111l111_opy_ in bstack111l1l1l_opy_[bstack1ll1lll_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪঈ")]:
      if bstack1111l111_opy_ in options._preferences:
        options._preferences[bstack1111l111_opy_] = update(options._preferences[bstack1111l111_opy_], bstack111l1l1l_opy_[bstack1ll1lll_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫউ")][bstack1111l111_opy_])
      else:
        options.set_preference(bstack1111l111_opy_, bstack111l1l1l_opy_[bstack1ll1lll_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬঊ")][bstack1111l111_opy_])
  if bstack1ll1lll_opy_ (u"ࠧࡢࡴࡪࡷࠬঋ") in bstack111l1l1l_opy_:
    for arg in bstack111l1l1l_opy_[bstack1ll1lll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ঌ")]:
      options.add_argument(arg)
def bstack1ll1l11ll_opy_(options, bstack11l1lll1_opy_):
  if bstack1ll1lll_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࠪ঍") in bstack11l1lll1_opy_:
    options.use_webview(bool(bstack11l1lll1_opy_[bstack1ll1lll_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࠫ঎")]))
  bstack1l11ll1l11_opy_(options, bstack11l1lll1_opy_)
def bstack1llllllll_opy_(options, bstack11ll1111ll_opy_):
  for bstack1111lll1l_opy_ in bstack11ll1111ll_opy_:
    if bstack1111lll1l_opy_ in [bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨএ"), bstack1ll1lll_opy_ (u"ࠬࡧࡲࡨࡵࠪঐ")]:
      continue
    options.set_capability(bstack1111lll1l_opy_, bstack11ll1111ll_opy_[bstack1111lll1l_opy_])
  if bstack1ll1lll_opy_ (u"࠭ࡡࡳࡩࡶࠫ঑") in bstack11ll1111ll_opy_:
    for arg in bstack11ll1111ll_opy_[bstack1ll1lll_opy_ (u"ࠧࡢࡴࡪࡷࠬ঒")]:
      options.add_argument(arg)
  if bstack1ll1lll_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬও") in bstack11ll1111ll_opy_:
    options.bstack11111ll1l1_opy_(bool(bstack11ll1111ll_opy_[bstack1ll1lll_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭ঔ")]))
def bstack11lll1l1ll_opy_(options, bstack1l111l11l_opy_):
  for bstack11llll11_opy_ in bstack1l111l11l_opy_:
    if bstack11llll11_opy_ in [bstack1ll1lll_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧক"), bstack1ll1lll_opy_ (u"ࠫࡦࡸࡧࡴࠩখ")]:
      continue
    options._options[bstack11llll11_opy_] = bstack1l111l11l_opy_[bstack11llll11_opy_]
  if bstack1ll1lll_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩগ") in bstack1l111l11l_opy_:
    for bstack1l11l11111_opy_ in bstack1l111l11l_opy_[bstack1ll1lll_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪঘ")]:
      options.bstack11l11l1lll_opy_(
        bstack1l11l11111_opy_, bstack1l111l11l_opy_[bstack1ll1lll_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫঙ")][bstack1l11l11111_opy_])
  if bstack1ll1lll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭চ") in bstack1l111l11l_opy_:
    for arg in bstack1l111l11l_opy_[bstack1ll1lll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧছ")]:
      options.add_argument(arg)
def bstack11ll1ll1_opy_(options, caps):
  if not hasattr(options, bstack1ll1lll_opy_ (u"ࠪࡏࡊ࡟ࠧজ")):
    return
  if options.KEY == bstack1ll1lll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩঝ"):
    options = a11y.bstack1lll1l111_opy_(bstack1ll1llll11_opy_=options, config=CONFIG)
  if options.KEY == bstack1ll1lll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪঞ") and options.KEY in caps:
    bstack1l11ll1l11_opy_(options, caps[bstack1ll1lll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫট")])
  elif options.KEY == bstack1ll1lll_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬঠ") and options.KEY in caps:
    bstack1ll11l11ll_opy_(options, caps[bstack1ll1lll_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ড")])
  elif options.KEY == bstack1ll1lll_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪঢ") and options.KEY in caps:
    bstack1llllllll_opy_(options, caps[bstack1ll1lll_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫণ")])
  elif options.KEY == bstack1ll1lll_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬত") and options.KEY in caps:
    bstack1ll1l11ll_opy_(options, caps[bstack1ll1lll_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭থ")])
  elif options.KEY == bstack1ll1lll_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬদ") and options.KEY in caps:
    bstack11lll1l1ll_opy_(options, caps[bstack1ll1lll_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ধ")])
def bstack1l11l11ll1_opy_(caps):
  global bstack1ll1ll1l1_opy_
  if isinstance(os.environ.get(bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩন")), str):
    bstack1ll1ll1l1_opy_ = eval(os.getenv(bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ঩")))
  if bstack1ll1ll1l1_opy_:
    if bstack1l1l1l1111_opy_() < version.parse(bstack1ll1lll_opy_ (u"ࠪ࠶࠳࠹࠮࠱ࠩপ")):
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
      if not bstack11l1l1ll1_opy_(options):
        return None
      for bstack1l1lllll_opy_ in caps.keys():
        options.set_capability(bstack1l1lllll_opy_, caps[bstack1l1lllll_opy_])
      bstack11ll1ll1_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1l1l1111ll_opy_(options, bstack1111lll1ll_opy_):
  if not bstack11l1l1ll1_opy_(options):
    return
  for bstack1l1lllll_opy_ in bstack1111lll1ll_opy_.keys():
    if bstack1l1lllll_opy_ in bstack11ll1lll11_opy_:
      continue
    if bstack1l1lllll_opy_ in options._caps and type(options._caps[bstack1l1lllll_opy_]) in [dict, list]:
      options._caps[bstack1l1lllll_opy_] = update(options._caps[bstack1l1lllll_opy_], bstack1111lll1ll_opy_[bstack1l1lllll_opy_])
    else:
      options.set_capability(bstack1l1lllll_opy_, bstack1111lll1ll_opy_[bstack1l1lllll_opy_])
  bstack11ll1ll1_opy_(options, bstack1111lll1ll_opy_)
  if bstack1ll1lll_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ়࠭") in options._caps:
    if options._caps[bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ঽ")] and options._caps[bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧা")].lower() != bstack1ll1lll_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫি"):
      del options._caps[bstack1ll1lll_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪী")]
def bstack1l1l1l1ll1_opy_(proxy_config):
  if bstack1ll1lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩু") in proxy_config:
    proxy_config[bstack1ll1lll_opy_ (u"࠭ࡳࡴ࡮ࡓࡶࡴࡾࡹࠨূ")] = proxy_config[bstack1ll1lll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫৃ")]
    del (proxy_config[bstack1ll1lll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬৄ")])
  if bstack1ll1lll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬ৅") in proxy_config and proxy_config[bstack1ll1lll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭৆")].lower() != bstack1ll1lll_opy_ (u"ࠫࡩ࡯ࡲࡦࡥࡷࠫে"):
    proxy_config[bstack1ll1lll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨৈ")] = bstack1ll1lll_opy_ (u"࠭࡭ࡢࡰࡸࡥࡱ࠭৉")
  if bstack1ll1lll_opy_ (u"ࠧࡱࡴࡲࡼࡾࡇࡵࡵࡱࡦࡳࡳ࡬ࡩࡨࡗࡵࡰࠬ৊") in proxy_config:
    proxy_config[bstack1ll1lll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫো")] = bstack1ll1lll_opy_ (u"ࠩࡳࡥࡨ࠭ৌ")
  return proxy_config
def bstack1111l11ll1_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1ll1lll_opy_ (u"ࠪࡴࡷࡵࡸࡺ্ࠩ") in config:
    return proxy
  config[bstack1ll1lll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪৎ")] = bstack1l1l1l1ll1_opy_(config[bstack1ll1lll_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ৏")])
  if proxy == None:
    proxy = Proxy(config[bstack1ll1lll_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ৐")])
  return proxy
def bstack111llllll1_opy_(self):
  global CONFIG
  global bstack1l1l11l11_opy_
  try:
    proxy = bstack111ll1ll11_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1ll1lll_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ৑")):
        proxies = bstack1l1ll11l_opy_(proxy, bstack1ll111lll_opy_())
        if len(proxies) > 0:
          protocol, bstack1lll11ll11_opy_ = proxies.popitem()
          if bstack1ll1lll_opy_ (u"ࠣ࠼࠲࠳ࠧ৒") in bstack1lll11ll11_opy_:
            return bstack1lll11ll11_opy_
          else:
            return bstack1ll1lll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ৓") + bstack1lll11ll11_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1ll1lll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡰࡳࡱࡻࡽࠥࡻࡲ࡭ࠢ࠽ࠤࢀࢃࠢ৔").format(str(e)))
  return bstack1l1l11l11_opy_(self)
def bstack1l1ll1lll_opy_():
  global CONFIG
  return bstack1ll1ll11l_opy_(CONFIG) and bstack11llllll_opy_() and bstack1l11ll1l1l_opy_() >= version.parse(bstack111l1lll_opy_)
def bstack1ll1ll11l1_opy_():
  global CONFIG
  return (bstack1ll1lll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ৕") in CONFIG or bstack1ll1lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ৖") in CONFIG) and bstack11lllll11l_opy_()
def bstack11l1l1l1l1_opy_(config):
  bstack1llll1lll_opy_ = {}
  if bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪৗ") in config:
    bstack1llll1lll_opy_ = config[bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ৘")]
  if bstack1ll1lll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ৙") in config:
    bstack1llll1lll_opy_ = config[bstack1ll1lll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ৚")]
  proxy = bstack111ll1ll11_opy_(config)
  if proxy:
    if proxy.endswith(bstack1ll1lll_opy_ (u"ࠪ࠲ࡵࡧࡣࠨ৛")) and os.path.isfile(proxy):
      bstack1llll1lll_opy_[bstack1ll1lll_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧড়")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1ll1lll_opy_ (u"ࠬ࠴ࡰࡢࡥࠪঢ়")):
        proxies = bstack11ll1l111l_opy_(config, bstack1ll111lll_opy_())
        if len(proxies) > 0:
          protocol, bstack1lll11ll11_opy_ = proxies.popitem()
          if bstack1ll1lll_opy_ (u"ࠨ࠺࠰࠱ࠥ৞") in bstack1lll11ll11_opy_:
            parsed_url = urlparse(bstack1lll11ll11_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1ll1lll_opy_ (u"ࠢ࠻࠱࠲ࠦয়") + bstack1lll11ll11_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1llll1lll_opy_[bstack1ll1lll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡈࡰࡵࡷࠫৠ")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1llll1lll_opy_[bstack1ll1lll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬৡ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1llll1lll_opy_[bstack1ll1lll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭ৢ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1llll1lll_opy_[bstack1ll1lll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧৣ")] = str(parsed_url.password)
  return bstack1llll1lll_opy_
def bstack1l1111ll11_opy_(config):
  if bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪ৤") in config:
    return config[bstack1ll1lll_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫ৥")]
  return {}
def update_caps_for_local(caps):
  global bstack11llllll1_opy_
  if bstack1ll1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ০") in caps:
    caps[bstack1ll1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ১")][bstack1ll1lll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨ২")] = True
    if bstack11llllll1_opy_:
      caps[bstack1ll1lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ৩")][bstack1ll1lll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭৪")] = bstack11llllll1_opy_
  else:
    caps[bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪ৫")] = True
    if bstack11llllll1_opy_:
      caps[bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ৬")] = bstack11llllll1_opy_
@measure(event_name=EVENTS.bstack11ll1lll_opy_, stage=STAGE.bstack1ll1llll_opy_, bstack1ll1l11l1l_opy_=SESSION_NAME)
def bstack1ll111111_opy_():
  global CONFIG
  if not bstack1l111llll_opy_(CONFIG) or cli.is_enabled(CONFIG):
    return
  if bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ৭") in CONFIG and bstack11llll111l_opy_(CONFIG[bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ৮")]):
    if (
      bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭৯") in CONFIG
      and bstack11llll111l_opy_(CONFIG[bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧৰ")].get(bstack1ll1lll_opy_ (u"ࠫࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠨৱ")))
    ):
      logger.debug(bstack1ll1lll_opy_ (u"ࠧࡒ࡯ࡤࡣ࡯ࠤࡧ࡯࡮ࡢࡴࡼࠤࡳࡵࡴࠡࡵࡷࡥࡷࡺࡥࡥࠢࡤࡷࠥࡹ࡫ࡪࡲࡅ࡭ࡳࡧࡲࡺࡋࡱ࡭ࡹ࡯ࡡ࡭࡫ࡶࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠨ৲"))
      return
    bstack1llll1lll_opy_ = bstack11l1l1l1l1_opy_(CONFIG)
    bstack11ll11111_opy_(CONFIG[bstack1ll1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ৳")], bstack1llll1lll_opy_)
def bstack11ll11111_opy_(key, bstack1llll1lll_opy_):
  global bstack111l1l1ll_opy_
  logger.info(bstack1l1111llll_opy_)
  try:
    bstack111l1l1ll_opy_ = Local()
    bstack111l1l1lll_opy_ = {bstack1ll1lll_opy_ (u"ࠧ࡬ࡧࡼࠫ৴"): key}
    bstack111l1l1lll_opy_.update(bstack1llll1lll_opy_)
    logger.debug(bstack1l11llllll_opy_.format(str(bstack111l1l1lll_opy_)).replace(key, bstack1ll1lll_opy_ (u"ࠨ࡝ࡕࡉࡉࡇࡃࡕࡇࡇࡡࠬ৵")))
    bstack111l1l1ll_opy_.start(**bstack111l1l1lll_opy_)
    if bstack111l1l1ll_opy_.isRunning():
      logger.info(bstack1l1111111l_opy_)
  except Exception as e:
    bstack1l1111ll_opy_(bstack111l1l11l1_opy_.format(str(e)))
def bstack1111111ll1_opy_():
  global bstack111l1l1ll_opy_
  if bstack111l1l1ll_opy_.isRunning():
    logger.info(bstack1111l1lll1_opy_)
    bstack111l1l1ll_opy_.stop()
  bstack111l1l1ll_opy_ = None
def bstack1ll11l1ll_opy_(bstack1ll111l111_opy_=[]):
  global CONFIG
  bstack1111l111l_opy_ = []
  bstack1ll1l1l11l_opy_ = [bstack1ll1lll_opy_ (u"ࠩࡲࡷࠬ৶"), bstack1ll1lll_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭৷"), bstack1ll1lll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨ৸"), bstack1ll1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ৹"), bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ৺"), bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ৻")]
  try:
    for err in bstack1ll111l111_opy_:
      bstack11ll11l11l_opy_ = {}
      for k in bstack1ll1l1l11l_opy_:
        val = CONFIG[bstack1ll1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫৼ")][int(err[bstack1ll1lll_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ৽")])].get(k)
        if val:
          bstack11ll11l11l_opy_[k] = val
      if(err[bstack1ll1lll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ৾")] != bstack1ll1lll_opy_ (u"ࠫࠬ৿")):
        bstack11ll11l11l_opy_[bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶࡶࠫ਀")] = {
          err[bstack1ll1lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫਁ")]: err[bstack1ll1lll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ਂ")]
        }
        bstack1111l111l_opy_.append(bstack11ll11l11l_opy_)
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪࡴࡸ࡭ࡢࡶࡷ࡭ࡳ࡭ࠠࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴ࠻ࠢࠪਃ") + str(e))
  finally:
    return bstack1111l111l_opy_
def bstack11l1l11ll_opy_(file_name):
  bstack111l1l111_opy_ = []
  try:
    bstack1l111ll1ll_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1l111ll1ll_opy_):
      with open(bstack1l111ll1ll_opy_) as f:
        bstack1ll111lll1_opy_ = json.load(f)
        bstack111l1l111_opy_ = bstack1ll111lll1_opy_
      os.remove(bstack1l111ll1ll_opy_)
    return bstack111l1l111_opy_
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡫࡯࡮ࡥ࡫ࡱ࡫ࠥ࡫ࡲࡳࡱࡵࠤࡱ࡯ࡳࡵ࠼ࠣࠫ਄") + str(e))
    return bstack111l1l111_opy_
def bstack11111l1ll_opy_():
  try:
      import time
      from bstack_utils.constants import bstack1111ll1l1l_opy_, EVENTS
      from bstack_utils.helper import bstack111l1l111l_opy_, get_host_info, global_config
      from datetime import datetime
      from filelock import FileLock
      from bstack_utils.bstack1ll11111_opy_ import bstack1lll1lll11_opy_
      bstack1lll1lll11_opy_.bstack1ll11l111_opy_()
      bstack1111ll1lll_opy_ = os.path.join(os.getcwd(), bstack1ll1lll_opy_ (u"ࠪࡰࡴ࡭ࠧਅ"), bstack1ll1lll_opy_ (u"ࠫࡰ࡫ࡹ࠮࡯ࡨࡸࡷ࡯ࡣࡴ࠰࡭ࡷࡴࡴࠧਆ"))
      data = None
      lock = FileLock(bstack1111ll1lll_opy_+bstack1ll1lll_opy_ (u"ࠧ࠴࡬ࡰࡥ࡮ࠦਇ"), timeout=2)
      try:
          with lock:
              with open(bstack1111ll1lll_opy_, bstack1ll1lll_opy_ (u"ࠨࡲࠣਈ"), encoding=bstack1ll1lll_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨਉ")) as file:
                  data = json.load(file)
      except Exception as e:
          logger.debug(bstack1ll1lll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡷ࡫ࡡࡥࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹࠠࡧ࡫࡯ࡩ࠿ࠦࡻࡾࠤਊ").format(e))
          return
      if not data:
          return
      def bstack11l1ll111l_opy_():
          try:
              config = {
                  bstack1ll1lll_opy_ (u"ࠤ࡫ࡩࡦࡪࡥࡳࡵࠥ਋"): {
                      bstack1ll1lll_opy_ (u"ࠥࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠤ਌"): bstack1ll1lll_opy_ (u"ࠦࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠢ਍"),
                  }
              }
              bstack1ll11lllll_opy_ = datetime.utcnow()
              current_time = bstack1ll11lllll_opy_.strftime(bstack1ll1lll_opy_ (u"࡙ࠧࠫ࠮ࠧࡰ࠱ࠪࡪࡔࠦࡊ࠽ࠩࡒࡀࠥࡔ࠰ࠨࡪ࡛ࠥࡔࡄࠤ਎"))
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
              bstack1l11111lll_opy_ = bstack1l11llll1l_opy_(cli.config, [bstack1ll1lll_opy_ (u"ࠤࡤࡴ࡮ࡹࠢਠ"), bstack1ll1lll_opy_ (u"ࠥࡩࡩࡹࡉ࡯ࡵࡷࡶࡺࡳࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠣਡ"), bstack1ll1lll_opy_ (u"ࠦࡦࡶࡩࠣਢ")], bstack1111ll1l1l_opy_)
              response = bstack111l1l111l_opy_(bstack1ll1lll_opy_ (u"ࠧࡖࡏࡔࡖࠥਣ"), bstack1l11111lll_opy_, payload, config)
              if response.status_code >= 200 and response.status_code < 300:
                  logger.info(bstack1ll1lll_opy_ (u"ࠨࡋࡦࡻࠣࡱࡪࡺࡲࡪࡥࡶࠤࡸ࡫࡮ࡵࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡶࡲࠤࢀࢃࠢਤ").format(bstack1111ll1l1l_opy_))
              else:
                  logger.debug(bstack1ll1lll_opy_ (u"ࠢࡌࡧࡼࠤࡲ࡫ࡴࡳ࡫ࡦࡷࠥࡸࡥࡲࡷࡨࡷࡹࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫ࠤࡸࡺࡡࡵࡷࡶࠤࢀࢃࠢਥ").format(response.status_code))
          except Exception as e:
              logger.debug(bstack1ll1lll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫࡮ࡥࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹ࠺ࠡࡽࢀࠦਦ").format(e))
      bstack11l1ll111l_opy_()
  except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫࡮ࡥࡡ࡮ࡩࡾࡥ࡭ࡦࡶࡵ࡭ࡨࡹ࠺ࠡࡽࢀࠦਧ").format(e))
def bstack111ll1l11l_opy_(bstack1lllll11_opy_=False):
  bstack1ll11lll1l_opy_ = bstack1ll1lll_opy_ (u"ࠥࠦਨ")
  global bstack1111lllll_opy_
  global bstack1lllllllll_opy_
  global bstack111l11llll_opy_
  global bstack1ll11l11_opy_
  global ROBOT_PYTHON_ERRORS
  global bstack11111lllll_opy_
  global CONFIG
  bstack1lll1l111l_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠫࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ࡟ࡖࡕࡈࡈࠬ਩"))
  if bstack1lll1l111l_opy_ not in [bstack1ll1lll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ਪ")]:
    bstack1ll11lll1l_opy_ = bstack1lll1lll11_opy_.bstack11l1llllll_opy_(EVENTS.bstack11111l11ll_opy_)
  percy.shutdown()
  if bstack1111lllll_opy_:
    logger.warning(bstack1l1l111l11_opy_.format(str(bstack1111lllll_opy_)))
  else:
    try:
      bstack1l111lll11_opy_ = bstack1l1111lll_opy_(bstack1ll1lll_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬਫ"), logger)
      if bstack1l111lll11_opy_.get(bstack1ll1lll_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬਬ")) and bstack1l111lll11_opy_.get(bstack1ll1lll_opy_ (u"ࠨࡰࡸࡨ࡬࡫࡟࡭ࡱࡦࡥࡱ࠭ਭ")).get(bstack1ll1lll_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫਮ")):
        logger.warning(bstack1l1l111l11_opy_.format(str(bstack1l111lll11_opy_[bstack1ll1lll_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨਯ")][bstack1ll1lll_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ਰ")])))
    except Exception as e:
      logger.error(e)
  if cli.is_running() and bstack1lll1l111l_opy_ not in [bstack1ll1lll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭਱")]:
    if _11l11l111_opy_ is not None:
      bstack1lllll11_opy_ = _11l11l111_opy_
    else:
      bstack1lllll11_opy_ = cli.is_running()
    bstack1l111111ll_opy_.invoke(Events.bstack11l11ll1ll_opy_)
  elif _11l11l111_opy_ is not None:
    bstack1lllll11_opy_ = _11l11l111_opy_
  logger.info(bstack1l1l1llll_opy_)
  global bstack111l1l1ll_opy_
  if bstack111l1l1ll_opy_:
    bstack1111111ll1_opy_()
  try:
    with bstack1ll111ll11_opy_:
      bstack1ll1111l1l_opy_ = bstack1lllllllll_opy_.copy()
    for driver in bstack1ll1111l1l_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1lll1l11l_opy_)
  ROBOT_PYTHON_ERRORS = []
  if bstack11111lllll_opy_ == bstack1ll1lll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬਲ"):
    ROBOT_PYTHON_ERRORS = bstack11l1l11ll_opy_(bstack1ll1lll_opy_ (u"ࠧࡳࡱࡥࡳࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨਲ਼"))
  if bstack11111lllll_opy_ == bstack1ll1lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ਴") and len(bstack1ll11l11_opy_) == 0:
    bstack1ll11l11_opy_ = bstack11l1l11ll_opy_(bstack1ll1lll_opy_ (u"ࠩࡳࡻࡤࡶࡹࡵࡧࡶࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧਵ"))
    if len(bstack1ll11l11_opy_) == 0:
      bstack1ll11l11_opy_ = bstack11l1l11ll_opy_(bstack1ll1lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡴࡵࡶ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩਸ਼"))
  bstack1llll11l11_opy_ = bstack1ll1lll_opy_ (u"ࠫࠬ਷")
  if len(bstack111l11llll_opy_) > 0:
    bstack1llll11l11_opy_ = bstack1ll11l1ll_opy_(bstack111l11llll_opy_)
  elif len(bstack1ll11l11_opy_) > 0:
    bstack1llll11l11_opy_ = bstack1ll11l1ll_opy_(bstack1ll11l11_opy_)
  elif len(ROBOT_PYTHON_ERRORS) > 0:
    bstack1llll11l11_opy_ = bstack1ll11l1ll_opy_(ROBOT_PYTHON_ERRORS)
  elif len(bstack1lll111lll_opy_) > 0:
    bstack1llll11l11_opy_ = bstack1ll11l1ll_opy_(bstack1lll111lll_opy_)
  if bstack1lll1l111l_opy_ not in [bstack1ll1lll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ਸ")]:
    def bstack11l111l111_opy_():
      try:
        if bstack1lll1l111l_opy_ in [bstack1ll1lll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬਹ"), bstack1ll1lll_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭਺")]:
          bstack111ll1l1l_opy_()
      except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪ࡮ࡴࡡ࡭ࡡࡨࡼࡪࡩࡵࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤ਻").format(e))
    def bstack1l11111l1l_opy_():
      try:
        if bool(bstack1llll11l11_opy_):
          bstack1l1lll11ll_opy_(bstack1llll11l11_opy_, bstack1lllll11_opy_=bstack1lllll11_opy_)
        else:
          bstack1l1lll11ll_opy_(bstack1lllll11_opy_=bstack1lllll11_opy_)
      except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡵࡨࡲࡩ࡯࡮ࡨࠢࡨࡺࡪࡴࡴ࠻ࠢࡾࢁ਼ࠧ").format(e))
    def bstack11l1l1ll_opy_():
      try:
        logger_utils.bstack11lllll111_opy_(CONFIG)
      except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡶࡩࡳࡪࡩ࡯ࡩࠣࡰࡴ࡭ࡳ࠻ࠢࡾࢁࠧ਽").format(e))
    bstack1lllll1l11_opy_ = threading.Thread(target=bstack11l111l111_opy_)
    bstack1lll1111l1_opy_ = threading.Thread(target=bstack1l11111l1l_opy_)
    bstack111lll1ll_opy_ = threading.Thread(target=bstack11l1l1ll_opy_)
    threads = [bstack1lllll1l11_opy_, bstack1lll1111l1_opy_, bstack111lll1ll_opy_]
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
    bstack1l11l1l1l1_opy_(bstack111l11ll1_opy_, logger)
    bstack1l11l1l1l1_opy_(os.path.join(os.getcwd(), bstack1ll1lll_opy_ (u"࠭࡬ࡰࡩࠪੀ"), bstack1ll1lll_opy_ (u"ࠧ࡬ࡧࡼ࠱ࡲ࡫ࡴࡳ࡫ࡦࡷ࠳ࡰࡳࡰࡰࠪੁ")), logger)
  if bstack1lll1l111l_opy_ not in [bstack1ll1lll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩੂ")]:
    bstack1lll1lll11_opy_.end(EVENTS.bstack11111l11ll_opy_.value, bstack1ll11lll1l_opy_ + bstack1ll1lll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ੃"), bstack1ll11lll1l_opy_ + bstack1ll1lll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ੄"), status=True, failure=None, test_name=None)
    bstack11111l1ll_opy_()
    logger_utils.bstack1llll111_opy_()
    logging.shutdown()
  if len(ROBOT_PYTHON_ERRORS) > 0:
    sys.exit(len(ROBOT_PYTHON_ERRORS))
def bstack111l11lll_opy_(bstack1ll1l1ll11_opy_, frame):
  global global_config
  logger.error(bstack1l1ll1ll11_opy_)
  global_config.bstack11lll11l11_opy_(bstack1ll1lll_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡓࡵࠧ੅"), bstack1ll1l1ll11_opy_)
  if hasattr(signal, bstack1ll1lll_opy_ (u"࡙ࠬࡩࡨࡰࡤࡰࡸ࠭੆")):
    global_config.bstack11lll11l11_opy_(bstack1ll1lll_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭ੇ"), signal.Signals(bstack1ll1l1ll11_opy_).name)
  else:
    global_config.bstack11lll11l11_opy_(bstack1ll1lll_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡔ࡫ࡪࡲࡦࡲࠧੈ"), bstack1ll1lll_opy_ (u"ࠨࡕࡌࡋ࡚ࡔࡋࡏࡑ࡚ࡒࠬ੉"))
  bstack1lllll11_opy_ = cli.is_running()
  if bstack1lllll11_opy_:
    bstack1l111111ll_opy_.invoke(Events.bstack11l11ll1ll_opy_)
  bstack1lll1l111l_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪ੊"))
  if bstack1lll1l111l_opy_ == bstack1ll1lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪੋ") and not cli.is_enabled(CONFIG):
    TestHubHandler.stop(global_config.get_property(bstack1ll1lll_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡘ࡯ࡧ࡯ࡣ࡯ࠫੌ")))
  bstack111ll1l11l_opy_(bstack1lllll11_opy_)
  sys.exit(1)
def bstack1l1111ll_opy_(err):
  logger.critical(bstack111ll111ll_opy_.format(str(err)))
  bstack1l1lll11ll_opy_(bstack111ll111ll_opy_.format(str(err)), True)
  atexit.unregister(bstack111ll1l11l_opy_)
  bstack111ll1l1l_opy_()
  sys.exit(1)
def bstack1l1l1ll1ll_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1l1lll11ll_opy_(message, True)
  atexit.unregister(bstack111ll1l11l_opy_)
  bstack111ll1l1l_opy_()
  sys.exit(1)
def bstack11ll1ll1ll_opy_():
  global CONFIG
  global bstack1llll1111l_opy_
  global bstack11lll1l1l_opy_
  global BROWSERSTACK_AUTOMATION
  CONFIG = bstack1ll11ll1l1_opy_()
  load_dotenv(CONFIG.get(bstack1ll1lll_opy_ (u"ࠬ࡫࡮ࡷࡈ࡬ࡰࡪ੍࠭")))
  bstack1l1ll1111_opy_()
  bstack1l1ll11lll_opy_()
  CONFIG = bstack1ll11l1ll1_opy_(CONFIG)
  update(CONFIG, bstack11lll1l1l_opy_)
  update(CONFIG, bstack1llll1111l_opy_)
  if not cli.is_enabled(CONFIG):
    CONFIG = bstack111ll1111_opy_(CONFIG)
  BROWSERSTACK_AUTOMATION = bstack1l111llll_opy_(CONFIG)
  os.environ[bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ੎")] = BROWSERSTACK_AUTOMATION.__str__().lower()
  global_config.bstack11lll11l11_opy_(bstack1ll1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ੏"), BROWSERSTACK_AUTOMATION)
  if (bstack1ll1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ੐") in CONFIG and bstack1ll1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬੑ") in bstack1llll1111l_opy_) or (
          bstack1ll1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭੒") in CONFIG and bstack1ll1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ੓") not in bstack11lll1l1l_opy_):
    if os.getenv(bstack1ll1lll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩ੔")):
      CONFIG[bstack1ll1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ੕")] = os.getenv(bstack1ll1lll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫ੖"))
    else:
      if not CONFIG.get(bstack1ll1lll_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠦ੗"), bstack1ll1lll_opy_ (u"ࠤࠥ੘")) in bstack11l1l111_opy_:
        bstack111l1ll1_opy_()
  elif (bstack1ll1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ਖ਼") not in CONFIG and bstack1ll1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ਗ਼") in CONFIG) or (
          bstack1ll1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨਜ਼") in bstack11lll1l1l_opy_ and bstack1ll1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩੜ") not in bstack1llll1111l_opy_):
    del (CONFIG[bstack1ll1lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ੝")])
  if bstack1ll1l1ll1_opy_(CONFIG):
    bstack1l1111ll_opy_(bstack1ll1l1l1l1_opy_)
  Config.get_instance().bstack11lll11l11_opy_(bstack1ll1lll_opy_ (u"ࠣࡷࡶࡩࡷࡔࡡ࡮ࡧࠥਫ਼"), CONFIG[bstack1ll1lll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ੟")])
  bstack11l1111l1l_opy_()
  bstack111l1111_opy_()
  if bstack1ll1ll1l1_opy_ and not CONFIG.get(bstack1ll1lll_opy_ (u"ࠥࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠨ੠"), bstack1ll1lll_opy_ (u"ࠦࠧ੡")) in bstack11l1l111_opy_:
    CONFIG[bstack1ll1lll_opy_ (u"ࠬࡧࡰࡱࠩ੢")] = bstack1lll111l11_opy_(CONFIG)
    logger.info(bstack1lllll1ll_opy_.format(CONFIG[bstack1ll1lll_opy_ (u"࠭ࡡࡱࡲࠪ੣")]))
  if not BROWSERSTACK_AUTOMATION:
    CONFIG[bstack1ll1lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ੤")] = [{}]
def bstack1lll1l11l1_opy_(config, bstack1ll1l11111_opy_):
  global CONFIG
  global bstack1ll1ll1l1_opy_
  CONFIG = config
  bstack1ll1ll1l1_opy_ = bstack1ll1l11111_opy_
def bstack111l1111_opy_():
  global CONFIG
  global bstack1ll1ll1l1_opy_
  if bstack1ll1lll_opy_ (u"ࠨࡣࡳࡴࠬ੥") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1l1l1ll1ll_opy_(e, bstack1l1l1l1l1_opy_)
    bstack1ll1ll1l1_opy_ = True
    global_config.bstack11lll11l11_opy_(bstack1ll1lll_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨ੦"), True)
def bstack1lll111l11_opy_(config):
  bstack1l1l11l1_opy_ = bstack1ll1lll_opy_ (u"ࠪࠫ੧")
  app = config[bstack1ll1lll_opy_ (u"ࠫࡦࡶࡰࠨ੨")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack111l111ll1_opy_:
      if os.path.exists(app):
        bstack1l1l11l1_opy_ = bstack11ll1ll11l_opy_(config, app)
      elif bstack11llll11ll_opy_(app):
        bstack1l1l11l1_opy_ = app
      else:
        bstack1l1111ll_opy_(bstack1l1ll111_opy_.format(app))
    else:
      if bstack11llll11ll_opy_(app):
        bstack1l1l11l1_opy_ = app
      elif os.path.exists(app):
        bstack1l1l11l1_opy_ = bstack11ll1ll11l_opy_(app)
      else:
        bstack1l1111ll_opy_(bstack111ll1l1l1_opy_)
  else:
    if len(app) > 2:
      bstack1l1111ll_opy_(bstack1l1lll1l11_opy_)
    elif len(app) == 2:
      if bstack1ll1lll_opy_ (u"ࠬࡶࡡࡵࡪࠪ੩") in app and bstack1ll1lll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩ੪") in app:
        if os.path.exists(app[bstack1ll1lll_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ੫")]):
          bstack1l1l11l1_opy_ = bstack11ll1ll11l_opy_(config, app[bstack1ll1lll_opy_ (u"ࠨࡲࡤࡸ࡭࠭੬")], app[bstack1ll1lll_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ੭")])
        else:
          bstack1l1111ll_opy_(bstack1l1ll111_opy_.format(app))
      else:
        bstack1l1111ll_opy_(bstack1l1lll1l11_opy_)
    else:
      for key in app:
        if key in bstack11l1ll1l_opy_:
          if key == bstack1ll1lll_opy_ (u"ࠪࡴࡦࡺࡨࠨ੮"):
            if os.path.exists(app[key]):
              bstack1l1l11l1_opy_ = bstack11ll1ll11l_opy_(config, app[key])
            else:
              bstack1l1111ll_opy_(bstack1l1ll111_opy_.format(app))
          else:
            bstack1l1l11l1_opy_ = app[key]
        else:
          bstack1l1111ll_opy_(bstack11l1111ll1_opy_)
  return bstack1l1l11l1_opy_
def bstack11llll11ll_opy_(bstack1l1l11l1_opy_):
  import re
  bstack1111l1111_opy_ = re.compile(bstack1ll1lll_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬࠧࠦ੯"))
  bstack11l11lll1l_opy_ = re.compile(bstack1ll1lll_opy_ (u"ࡷࠨ࡞࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭࠳ࡠࡧ࠭ࡻࡃ࠰࡞࠵࠳࠹࡝ࡡ࠱ࡠ࠲ࡣࠪࠥࠤੰ"))
  if bstack1ll1lll_opy_ (u"࠭ࡢࡴ࠼࠲࠳ࠬੱ") in bstack1l1l11l1_opy_ or re.fullmatch(bstack1111l1111_opy_, bstack1l1l11l1_opy_) or re.fullmatch(bstack11l11lll1l_opy_, bstack1l1l11l1_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack11l11l11l_opy_, stage=STAGE.bstack1ll1llll_opy_, bstack1ll1l11l1l_opy_=SESSION_NAME)
def bstack11ll1ll11l_opy_(config, path, bstack1l1l1l1lll_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1ll1lll_opy_ (u"ࠧࡳࡤࠪੲ")).read()).hexdigest()
  bstack1l1llll1l1_opy_ = bstack1l1l1l1l1l_opy_(md5_hash)
  bstack1l1l11l1_opy_ = None
  if bstack1l1llll1l1_opy_:
    logger.info(bstack11111ll11_opy_.format(bstack1l1llll1l1_opy_, md5_hash))
    return bstack1l1llll1l1_opy_
  bstack1ll1l111l_opy_ = datetime.datetime.now()
  multipart_data = MultipartEncoder(
    fields={
      bstack1ll1lll_opy_ (u"ࠨࡨ࡬ࡰࡪ࠭ੳ"): (os.path.basename(path), open(os.path.abspath(path), bstack1ll1lll_opy_ (u"ࠩࡵࡦࠬੴ")), bstack1ll1lll_opy_ (u"ࠪࡸࡪࡾࡴ࠰ࡲ࡯ࡥ࡮ࡴࠧੵ")),
      bstack1ll1lll_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧ੶"): bstack1l1l1l1lll_opy_
    }
  )
  response = requests.post(bstack11l11l11l1_opy_, data=multipart_data,
                           headers={bstack1ll1lll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ੷"): multipart_data.content_type},
                           auth=(config[bstack1ll1lll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ੸")], config[bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ੹")]))
  try:
    res = json.loads(response.text)
    bstack1l1l11l1_opy_ = res[bstack1ll1lll_opy_ (u"ࠨࡣࡳࡴࡤࡻࡲ࡭ࠩ੺")]
    logger.info(bstack1ll111ll1l_opy_.format(bstack1l1l11l1_opy_))
    bstack1lll1lllll_opy_(md5_hash, bstack1l1l11l1_opy_)
    cli.bstack1111lll11_opy_(bstack1ll1lll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺ࡶࡲ࡯ࡳࡦࡪ࡟ࡢࡲࡳࠦ੻"), datetime.datetime.now() - bstack1ll1l111l_opy_)
  except ValueError as err:
    bstack1l1111ll_opy_(bstack1111llll1l_opy_.format(str(err)))
  return bstack1l1l11l1_opy_
def bstack11l1111l1l_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack1111ll11l1_opy_
  bstack111lll1lll_opy_ = 1
  bstack111lllllll_opy_ = 1
  if bstack1ll1lll_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ੼") in CONFIG:
    bstack111lllllll_opy_ = CONFIG[bstack1ll1lll_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ੽")]
  else:
    bstack111lllllll_opy_ = bstack11l111l1l1_opy_(framework_name, args) or 1
  if bstack1ll1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ੾") in CONFIG:
    bstack111lll1lll_opy_ = len(CONFIG[bstack1ll1lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ੿")])
  bstack1111ll11l1_opy_ = int(bstack111lllllll_opy_) * int(bstack111lll1lll_opy_)
def bstack11l111l1l1_opy_(framework_name, args):
  if framework_name == bstack111l1lllll_opy_ and args and bstack1ll1lll_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ઀") in args:
      bstack1ll1l1ll1l_opy_ = args.index(bstack1ll1lll_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ઁ"))
      return int(args[bstack1ll1l1ll1l_opy_ + 1]) or 1
  return 1
def bstack1l1l1l1l1l_opy_(md5_hash):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1ll1lll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡬ࡰࡥ࡮ࠤࡳࡵࡴࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨ࠰ࠥࡻࡳࡪࡰࡪࠤࡧࡧࡳࡪࡥࠣࡪ࡮ࡲࡥࠡࡱࡳࡩࡷࡧࡴࡪࡱࡱࡷࠬં"))
    bstack1lll111l1_opy_ = os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"ࠪࢂࠬઃ")), bstack1ll1lll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ઄"), bstack1ll1lll_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭અ"))
    if os.path.exists(bstack1lll111l1_opy_):
      try:
        bstack11ll11l1l_opy_ = json.load(open(bstack1lll111l1_opy_, bstack1ll1lll_opy_ (u"࠭ࡲࡣࠩઆ")))
        if md5_hash in bstack11ll11l1l_opy_:
          bstack1l111l1l1l_opy_ = bstack11ll11l1l_opy_[md5_hash]
          bstack1l1l1lllll_opy_ = datetime.datetime.now()
          bstack1llll111l_opy_ = datetime.datetime.strptime(bstack1l111l1l1l_opy_[bstack1ll1lll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪઇ")], bstack1ll1lll_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬઈ"))
          if (bstack1l1l1lllll_opy_ - bstack1llll111l_opy_).days > 30:
            return None
          elif version.parse(str(__version__)) > version.parse(bstack1l111l1l1l_opy_[bstack1ll1lll_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧઉ")]):
            return None
          return bstack1l111l1l1l_opy_[bstack1ll1lll_opy_ (u"ࠪ࡭ࡩ࠭ઊ")]
      except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡶࡪࡧࡤࡪࡰࡪࠤࡒࡊ࠵ࠡࡪࡤࡷ࡭ࠦࡦࡪ࡮ࡨ࠾ࠥࢁࡽࠨઋ").format(str(e)))
    return None
  bstack1lll111l1_opy_ = os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"ࠬࢄࠧઌ")), bstack1ll1lll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ઍ"), bstack1ll1lll_opy_ (u"ࠧࡢࡲࡳ࡙ࡵࡲ࡯ࡢࡦࡐࡈ࠺ࡎࡡࡴࡪ࠱࡮ࡸࡵ࡮ࠨ઎"))
  lock_file = bstack1lll111l1_opy_ + bstack1ll1lll_opy_ (u"ࠨ࠰࡯ࡳࡨࡱࠧએ")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack1lll111l1_opy_):
        with open(bstack1lll111l1_opy_, bstack1ll1lll_opy_ (u"ࠩࡵࠫઐ")) as f:
          content = f.read().strip()
          if content:
            bstack11ll11l1l_opy_ = json.loads(content)
            if md5_hash in bstack11ll11l1l_opy_:
              bstack1l111l1l1l_opy_ = bstack11ll11l1l_opy_[md5_hash]
              bstack1l1l1lllll_opy_ = datetime.datetime.now()
              bstack1llll111l_opy_ = datetime.datetime.strptime(bstack1l111l1l1l_opy_[bstack1ll1lll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ઑ")], bstack1ll1lll_opy_ (u"ࠫࠪࡪ࠯ࠦ࡯࠲ࠩ࡞ࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨ઒"))
              if (bstack1l1l1lllll_opy_ - bstack1llll111l_opy_).days > 30:
                return None
              elif version.parse(str(__version__)) > version.parse(bstack1l111l1l1l_opy_[bstack1ll1lll_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪઓ")]):
                return None
              return bstack1l111l1l1l_opy_[bstack1ll1lll_opy_ (u"࠭ࡩࡥࠩઔ")]
      return None
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡷࡪࡶ࡫ࠤ࡫࡯࡬ࡦࠢ࡯ࡳࡨࡱࡩ࡯ࡩࠣࡪࡴࡸࠠࡎࡆ࠸ࠤ࡭ࡧࡳࡩ࠼ࠣࡿࢂ࠭ક").format(str(e)))
    return None
def bstack1lll1lllll_opy_(md5_hash, bstack1l1l11l1_opy_):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1ll1lll_opy_ (u"ࠨࡨ࡬ࡰࡪࡲ࡯ࡤ࡭ࠣࡲࡴࡺࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧ࠯ࠤࡺࡹࡩ࡯ࡩࠣࡦࡦࡹࡩࡤࠢࡩ࡭ࡱ࡫ࠠࡰࡲࡨࡶࡦࡺࡩࡰࡰࡶࠫખ"))
    bstack111l11l11_opy_ = os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"ࠩࢁࠫગ")), bstack1ll1lll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪઘ"))
    if not os.path.exists(bstack111l11l11_opy_):
      os.makedirs(bstack111l11l11_opy_)
    bstack1lll111l1_opy_ = os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"ࠫࢃ࠭ઙ")), bstack1ll1lll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬચ"), bstack1ll1lll_opy_ (u"࠭ࡡࡱࡲࡘࡴࡱࡵࡡࡥࡏࡇ࠹ࡍࡧࡳࡩ࠰࡭ࡷࡴࡴࠧછ"))
    bstack1l111l11_opy_ = {
      bstack1ll1lll_opy_ (u"ࠧࡪࡦࠪજ"): bstack1l1l11l1_opy_,
      bstack1ll1lll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫઝ"): datetime.datetime.strftime(datetime.datetime.now(), bstack1ll1lll_opy_ (u"ࠩࠨࡨ࠴ࠫ࡭࠰ࠧ࡜ࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭ઞ")),
      bstack1ll1lll_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨટ"): str(__version__)
    }
    try:
      bstack11ll11l1l_opy_ = {}
      if os.path.exists(bstack1lll111l1_opy_):
        bstack11ll11l1l_opy_ = json.load(open(bstack1lll111l1_opy_, bstack1ll1lll_opy_ (u"ࠫࡷࡨࠧઠ")))
      bstack11ll11l1l_opy_[md5_hash] = bstack1l111l11_opy_
      with open(bstack1lll111l1_opy_, bstack1ll1lll_opy_ (u"ࠧࡽࠫࠣડ")) as outfile:
        json.dump(bstack11ll11l1l_opy_, outfile)
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡻࡰࡥࡣࡷ࡭ࡳ࡭ࠠࡎࡆ࠸ࠤ࡭ࡧࡳࡩࠢࡩ࡭ࡱ࡫࠺ࠡࡽࢀࠫઢ").format(str(e)))
    return
  bstack111l11l11_opy_ = os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"ࠧࡿࠩણ")), bstack1ll1lll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨત"))
  if not os.path.exists(bstack111l11l11_opy_):
    os.makedirs(bstack111l11l11_opy_)
  bstack1lll111l1_opy_ = os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"ࠩࢁࠫથ")), bstack1ll1lll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪદ"), bstack1ll1lll_opy_ (u"ࠫࡦࡶࡰࡖࡲ࡯ࡳࡦࡪࡍࡅ࠷ࡋࡥࡸ࡮࠮࡫ࡵࡲࡲࠬધ"))
  lock_file = bstack1lll111l1_opy_ + bstack1ll1lll_opy_ (u"ࠬ࠴࡬ࡰࡥ࡮ࠫન")
  bstack1l111l11_opy_ = {
    bstack1ll1lll_opy_ (u"࠭ࡩࡥࠩ઩"): bstack1l1l11l1_opy_,
    bstack1ll1lll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪપ"): datetime.datetime.strftime(datetime.datetime.now(), bstack1ll1lll_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬફ")),
    bstack1ll1lll_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧબ"): str(__version__)
  }
  try:
    with FileLock(lock_file, timeout=10):
      bstack11ll11l1l_opy_ = {}
      if os.path.exists(bstack1lll111l1_opy_):
        with open(bstack1lll111l1_opy_, bstack1ll1lll_opy_ (u"ࠪࡶࠬભ")) as f:
          content = f.read().strip()
          if content:
            bstack11ll11l1l_opy_ = json.loads(content)
      bstack11ll11l1l_opy_[md5_hash] = bstack1l111l11_opy_
      with open(bstack1lll111l1_opy_, bstack1ll1lll_opy_ (u"ࠦࡼࠨમ")) as outfile:
        json.dump(bstack11ll11l1l_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡼ࡯ࡴࡩࠢࡩ࡭ࡱ࡫ࠠ࡭ࡱࡦ࡯࡮ࡴࡧࠡࡨࡲࡶࠥࡓࡄ࠶ࠢ࡫ࡥࡸ࡮ࠠࡶࡲࡧࡥࡹ࡫࠺ࠡࡽࢀࠫય").format(str(e)))
def bstack1111ll1ll1_opy_(self):
  return
def bstack111llll11_opy_(self):
  return
def bstack111111llll_opy_():
  global bstack111llll11l_opy_
  bstack111llll11l_opy_ = True
def bstack1ll111l1l_opy_(self):
  global FRAMEWORK_NAME
  global bstack1llll1ll1_opy_
  global bstack1l1lll1111_opy_
  bstack11ll1ll1l_opy_ = bstack1lll1lll11_opy_.bstack11l1llllll_opy_(EVENTS.bstack1lll1ll111_opy_)
  try:
    if bstack1ll1lll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ર") in FRAMEWORK_NAME and self.session_id != None and bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫ઱"), bstack1ll1lll_opy_ (u"ࠨࠩલ")) != bstack1ll1lll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪળ"):
      bstack1l1llll11l_opy_ = bstack1ll1lll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ઴") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1ll1lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫવ")
      if bstack1l1llll11l_opy_ == bstack1ll1lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬશ"):
        bstack1l111llll1_opy_(logger)
      if self != None:
        bstack1111lll1l1_opy_(self, bstack1l1llll11l_opy_, bstack1ll1lll_opy_ (u"࠭ࠬࠡࠩષ").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack1ll1lll_opy_ (u"ࠧࠨસ")
    if bstack1ll1lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨહ") in FRAMEWORK_NAME and getattr(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ઺"), None):
      bstack1llll1111_opy_.bstack11l111ll1_opy_(self, bstack1l1llllll1_opy_, logger, wait=True)
    if bstack1ll1lll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ઻") in FRAMEWORK_NAME:
      bstack1l11l1ll11_opy_.bstack1111l1111l_opy_(self)
    bstack1lll1lll11_opy_.end(EVENTS.bstack1lll1ll111_opy_.value, bstack11ll1ll1l_opy_ + bstack1ll1lll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷ઼ࠦ"), bstack11ll1ll1l_opy_ + bstack1ll1lll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥઽ"), status=True, failure=None, test_name=None)
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࠢા") + str(e))
    bstack1lll1lll11_opy_.end(EVENTS.bstack1lll1ll111_opy_.value, bstack11ll1ll1l_opy_ + bstack1ll1lll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢિ"), bstack11ll1ll1l_opy_ + bstack1ll1lll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨી"), status=False, failure=str(e), test_name=None)
  bstack1l1lll1111_opy_(self)
  self.session_id = None
def bstack11l111l1ll_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack11ll111111_opy_
    global FRAMEWORK_NAME
    command_executor = kwargs.get(bstack1ll1lll_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠬુ"), bstack1ll1lll_opy_ (u"ࠪࠫૂ"))
    bstack11ll111l1_opy_ = False
    if type(command_executor) == str and bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧૃ") in command_executor:
      bstack11ll111l1_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨૄ") in str(getattr(command_executor, bstack1ll1lll_opy_ (u"࠭࡟ࡶࡴ࡯ࠫૅ"), bstack1ll1lll_opy_ (u"ࠧࠨ૆"))):
      bstack11ll111l1_opy_ = True
    else:
      kwargs = a11y.bstack1lll1l111_opy_(bstack1ll1llll11_opy_=kwargs, config=CONFIG)
      return bstack111llll111_opy_(self, *args, **kwargs)
    if bstack11ll111l1_opy_:
      bstack11l11l111l_opy_ = TestHubUtils.bstack11ll111ll1_opy_(CONFIG, FRAMEWORK_NAME)
      if kwargs.get(bstack1ll1lll_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩે")):
        kwargs[bstack1ll1lll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪૈ")] = bstack11ll111111_opy_(kwargs[bstack1ll1lll_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫૉ")], FRAMEWORK_NAME, CONFIG, bstack11l11l111l_opy_)
      elif kwargs.get(bstack1ll1lll_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ૊")):
        kwargs[bstack1ll1lll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬો")] = bstack11ll111111_opy_(kwargs[bstack1ll1lll_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ૌ")], FRAMEWORK_NAME, CONFIG, bstack11l11l111l_opy_)
  except Exception as e:
    logger.error(bstack1ll1lll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩࡧࡱࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡕࡇࡏࠥࡩࡡࡱࡵ࠽ࠤࢀࢃ્ࠢ").format(str(e)))
  return bstack111llll111_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack11ll1l1ll_opy_, stage=STAGE.bstack1ll1llll_opy_, bstack1ll1l11l1l_opy_=SESSION_NAME)
def bstack1l1l111lll_opy_(self, command_executor=bstack1ll1lll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰࠳࠵࠻࠳࠶࠮࠱࠰࠴࠾࠹࠺࠴࠵ࠤ૎"), *args, **kwargs):
  global bstack1llll1ll1_opy_
  global bstack1lllllllll_opy_
  bstack11lllll1l1_opy_ = bstack11l111l1ll_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack11lll1l11_opy_.on():
    return bstack11lllll1l1_opy_
  try:
    logger.debug(bstack1ll1lll_opy_ (u"ࠩࡆࡳࡲࡳࡡ࡯ࡦࠣࡉࡽ࡫ࡣࡶࡶࡲࡶࠥࡽࡨࡦࡰࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡩࡴࠢࡩࡥࡱࡹࡥࠡ࠯ࠣࡿࢂ࠭૏").format(str(command_executor)))
    logger.debug(bstack1ll1lll_opy_ (u"ࠪࡌࡺࡨࠠࡖࡔࡏࠤ࡮ࡹࠠ࠮ࠢࡾࢁࠬૐ").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧ૑") in command_executor._url:
      global_config.bstack11lll11l11_opy_(bstack1ll1lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭૒"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩ૓") in command_executor):
    global_config.bstack11lll11l11_opy_(bstack1ll1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ૔"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1111l1ll1_opy_ = getattr(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡕࡧࡶࡸࡒ࡫ࡴࡢࠩ૕"), None)
  bstack1l1llll1_opy_ = {}
  if self.capabilities is not None:
    bstack1l1llll1_opy_[bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡲࡦࡳࡥࠨ૖")] = self.capabilities.get(bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ૗"))
    bstack1l1llll1_opy_[bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭૘")] = self.capabilities.get(bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭૙"))
    bstack1l1llll1_opy_[bstack1ll1lll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡥ࡯ࡱࡶ࡬ࡳࡳࡹࠧ૚")] = self.capabilities.get(bstack1ll1lll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ૛"))
  if CONFIG.get(bstack1ll1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ૜"), False) and a11y.bstack1111l1ll11_opy_(bstack1l1llll1_opy_):
    threading.current_thread().a11yPlatform = True
  if bstack1ll1lll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ૝") in FRAMEWORK_NAME or bstack1ll1lll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ૞") in FRAMEWORK_NAME:
    TestHubHandler.send_cbt_info(self)
  if bstack1ll1lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ૟") in FRAMEWORK_NAME and bstack1111l1ll1_opy_ and bstack1111l1ll1_opy_.get(bstack1ll1lll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬૠ"), bstack1ll1lll_opy_ (u"࠭ࠧૡ")) == bstack1ll1lll_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨૢ"):
    TestHubHandler.send_cbt_info(self)
  bstack1llll1ll1_opy_ = self.session_id
  with bstack1ll111ll11_opy_:
    bstack1lllllllll_opy_.append(self)
  return bstack11lllll1l1_opy_
def bstack11ll11l1l1_opy_(args):
  return bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠩૣ") in str(args)
def bstack11l1l11l1l_opy_(self, driver_command, *args, **kwargs):
  global bstack1ll1l111_opy_
  global bstack1llll1ll_opy_
  bstack1llllll1l1_opy_ = bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭૤"), None) and bstack111l1lll11_opy_(
          threading.current_thread(), bstack1ll1lll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ૥"), None)
  bstack11111ll1_opy_ = bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ૦"), None) and bstack111l1lll11_opy_(
          threading.current_thread(), bstack1ll1lll_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ૧"), None)
  bstack1l1l1lll11_opy_ = getattr(self, bstack1ll1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭૨"), None) != None and getattr(self, bstack1ll1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧ૩"), None) == True
  if not bstack1llll1ll_opy_ and bstack1ll1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ૪") in CONFIG and CONFIG[bstack1ll1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ૫")] == True and accessibility_scripts.bstack1111lll1_opy_(driver_command) and (bstack1l1l1lll11_opy_ or bstack1llllll1l1_opy_ or bstack11111ll1_opy_) and not bstack11ll11l1l1_opy_(args):
    try:
      bstack1llll1ll_opy_ = True
      logger.debug(bstack1ll1lll_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡾࢁࠬ૬").format(driver_command))
      bstack11l111111l_opy_ = perform_scan(self, driver_command=driver_command)
      logger.debug(bstack11l111111l_opy_)
      try:
        log_data = {
          bstack1ll1lll_opy_ (u"ࠦࡷ࡫ࡱࡶࡧࡶࡸࠧ૭"): {
            bstack1ll1lll_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࠨ૮"): bstack1ll1lll_opy_ (u"ࠨࡁ࠲࠳࡜ࡣࡘࡉࡁࡏࠤ૯"),
            bstack1ll1lll_opy_ (u"ࠢࡱࡣࡵࡥࡲ࡫ࡴࡦࡴࡶࠦ૰"): [
              {
                bstack1ll1lll_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠣ૱"): driver_command
              }
            ]
          },
          bstack1ll1lll_opy_ (u"ࠤࡵࡩࡸࡶ࡯࡯ࡵࡨࠦ૲"): {
            bstack1ll1lll_opy_ (u"ࠥࡦࡴࡪࡹࠣ૳"): {
              bstack1ll1lll_opy_ (u"ࠦࡲࡹࡧࠣ૴"): bstack11l111111l_opy_.get(bstack1ll1lll_opy_ (u"ࠧࡳࡳࡨࠤ૵"), bstack1ll1lll_opy_ (u"ࠨࠢ૶")) if isinstance(bstack11l111111l_opy_, dict) else bstack1ll1lll_opy_ (u"ࠢࠣ૷"),
              bstack1ll1lll_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴࠤ૸"): bstack11l111111l_opy_.get(bstack1ll1lll_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥૹ"), True) if isinstance(bstack11l111111l_opy_, dict) else True
            }
          }
        }
        logger.debug(bstack1ll1lll_opy_ (u"ࠪࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮ࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡲ࡯ࡨࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠫૺ").format(log_data))
        automation_logger.info(json.dumps(log_data, separators=(bstack1ll1lll_opy_ (u"ࠫ࠱࠭ૻ"), bstack1ll1lll_opy_ (u"ࠬࡀࠧૼ"))))
      except Exception as bstack1l1l1ll1l1_opy_:
        logger.debug(bstack1ll1lll_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢ࡯ࡳ࡬ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡤࡣࡱࠤࡩࡧࡴࡢ࠼ࠣࡿࢂ࠭૽").format(str(bstack1l1l1ll1l1_opy_)))
    except Exception as err:
      logger.debug(bstack1ll1lll_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡪࡸࡦࡰࡴࡰࠤࡸࡩࡡ࡯ࠢࡾࢁࠬ૾").format(str(err)))
    bstack1llll1ll_opy_ = False
  response = bstack1ll1l111_opy_(self, driver_command, *args, **kwargs)
  if (bstack1ll1lll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ૿") in str(FRAMEWORK_NAME).lower() or bstack1ll1lll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ଀") in str(FRAMEWORK_NAME).lower()) and bstack11lll1l11_opy_.on():
    try:
      if driver_command == bstack1ll1lll_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧଁ"):
        TestHubHandler.bstack11lll1l11l_opy_({
            bstack1ll1lll_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪଂ"): response[bstack1ll1lll_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫଃ")],
            bstack1ll1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭଄"): TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack11lll1l11_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
def bstack1l11ll11_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack1llll1ll1_opy_
  global PLATFORM_INDEX
  global SESSION_NAME
  global PARALLELISE_VANILLA_PYTHON
  global PARALLELISE_THREADING_PYTHON
  global FRAMEWORK_NAME
  global bstack111llll111_opy_
  global bstack1lllllllll_opy_
  global bstack1l1l11ll1l_opy_
  global bstack1l1llllll1_opy_
  bstack11ll1ll1l_opy_ = bstack1lll1lll11_opy_.bstack11l1llllll_opy_(EVENTS.bstack1l1l1111l_opy_.value)
  if os.getenv(bstack1ll1lll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬଅ")) is not None and a11y.bstack1l1ll111ll_opy_(CONFIG) is None:
    CONFIG[bstack1ll1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨଆ")] = True
  CONFIG[bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫଇ")] = str(FRAMEWORK_NAME) + str(__version__)
  bstack111ll11l_opy_ = os.environ[bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨଈ")]
  bstack11l11l111l_opy_ = TestHubUtils.bstack11ll111ll1_opy_(CONFIG, FRAMEWORK_NAME)
  CONFIG[bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧଉ")] = bstack111ll11l_opy_
  CONFIG[bstack1ll1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧଊ")] = bstack11l11l111l_opy_
  if CONFIG.get(bstack1ll1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ଋ"),bstack1ll1lll_opy_ (u"ࠧࠨଌ")) and bstack1ll1lll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ଍") in FRAMEWORK_NAME:
    CONFIG[bstack1ll1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ଎")].pop(bstack1ll1lll_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨଏ"), None)
    CONFIG[bstack1ll1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫଐ")].pop(bstack1ll1lll_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ଑"), None)
  command_executor = bstack1ll111lll_opy_()
  logger.debug(bstack11111llll_opy_.format(command_executor))
  proxy = bstack1111l11ll1_opy_(CONFIG, proxy)
  bstack111111lll1_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
  try:
    if PARALLELISE_VANILLA_PYTHON is True:
      bstack111111lll1_opy_ = int(multiprocessing.current_process().name)
    elif PARALLELISE_THREADING_PYTHON is True:
      bstack111111lll1_opy_ = int(threading.current_thread().name)
  except:
    bstack111111lll1_opy_ = 0
  bstack1111lll1ll_opy_ = get_caps(CONFIG, bstack111111lll1_opy_)
  logger.debug(CONFIG_FILE_CONTENT.format(str(bstack1111lll1ll_opy_)))
  if bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ଒") in CONFIG and bstack11llll111l_opy_(CONFIG[bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫଓ")]):
    update_caps_for_local(bstack1111lll1ll_opy_)
  if a11y.is_enabled_platform(CONFIG, bstack111111lll1_opy_) and a11y.is_platform_supported(bstack1111lll1ll_opy_, options, desired_capabilities, CONFIG):
    threading.current_thread().a11yPlatform = True
    if (cli.accessibility is None or not cli.accessibility.is_enabled()):
      a11y.set_capabilities(bstack1111lll1ll_opy_, CONFIG)
  if desired_capabilities:
    bstack1ll1lll1ll_opy_ = bstack1ll11l1ll1_opy_(desired_capabilities)
    bstack1ll1lll1ll_opy_[bstack1ll1lll_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨଔ")] = bstack11l11l1111_opy_(CONFIG)
    bstack1l1llll11_opy_ = get_caps(bstack1ll1lll1ll_opy_)
    if bstack1l1llll11_opy_:
      bstack1111lll1ll_opy_ = update(bstack1l1llll11_opy_, bstack1111lll1ll_opy_)
    desired_capabilities = None
  if options:
    bstack1l1l1111ll_opy_(options, bstack1111lll1ll_opy_)
  if not options:
    options = bstack1l11l11ll1_opy_(bstack1111lll1ll_opy_)
  try:
    if bstack1111l1l1l1_opy_:
      def _1ll111ll1_opy_(bstack1lll1l11_opy_):
        if not isinstance(bstack1lll1l11_opy_, dict):
          return
        for _1l11l11ll_opy_ in list(bstack1lll1l11_opy_.keys()):
          _111lll111_opy_ = bstack1lll1l11_opy_[_1l11l11ll_opy_]
          if _111lll111_opy_ is None:
            bstack1lll1l11_opy_.pop(_1l11l11ll_opy_, None)
          elif isinstance(_111lll111_opy_, dict):
            _1ll111ll1_opy_(_111lll111_opy_)
      _1ll111ll1_opy_(bstack1111lll1ll_opy_)
      _1ll111ll1_opy_(desired_capabilities)
      if options is not None and hasattr(options, bstack1ll1lll_opy_ (u"ࠩࡢࡧࡦࡶࡳࠨକ")):
        _1ll111ll1_opy_(options._caps)
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠥࡱࡴࡪ࡟ࡪࡰ࡬ࡸ࠭࠯ࠠࡱࡱࡶࡸ࠲ࡵࡰࡵ࡫ࡲࡲࡸࠦࡰࡳࡷࡱࡩࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡾࠤଖ").format(e))
  if bstack1111l1l1l1_opy_:
    options = bstack11111ll1l_opy_(options)
  bstack1l1llllll1_opy_ = CONFIG.get(bstack1ll1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଗ"))[bstack111111lll1_opy_]
  if proxy and bstack1l11ll1l1l_opy_() >= version.parse(bstack1ll1lll_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬଘ")):
    options.proxy(proxy)
  if options and bstack1l11ll1l1l_opy_() >= version.parse(bstack1ll1lll_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬଙ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1l11ll1l1l_opy_() < version.parse(bstack1ll1lll_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ଚ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1111lll1ll_opy_)
  logger.info(bstack111ll1ll_opy_)
  bstack1ll11111_opy_.end(EVENTS.bstack111lll1l11_opy_.value, EVENTS.bstack111lll1l11_opy_.value + bstack1ll1lll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣଛ"), EVENTS.bstack111lll1l11_opy_.value + bstack1ll1lll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢଜ"), status=True, failure=None, test_name=SESSION_NAME)
  if bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡵࡸ࡯ࡧ࡫࡯ࡩࠬଝ") in kwargs:
    del kwargs[bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡶࡲࡰࡨ࡬ࡰࡪ࠭ଞ")]
  bstack1lll1lll11_opy_.end(EVENTS.bstack1l1l1111l_opy_.value, bstack11ll1ll1l_opy_ + bstack1ll1lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧଟ"), bstack11ll1ll1l_opy_ + bstack1ll1lll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦଠ"), status=True, failure=None, test_name=SESSION_NAME)
  try:
    if bstack1l11ll1l1l_opy_() >= version.parse(bstack1ll1lll_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧଡ")):
      bstack111llll111_opy_(self, command_executor=command_executor,
                options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
    elif bstack1l11ll1l1l_opy_() >= version.parse(bstack1ll1lll_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧଢ")):
      bstack111llll111_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities, options=options,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l11ll1l1l_opy_() >= version.parse(bstack1ll1lll_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩଣ")):
      bstack111llll111_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    else:
      bstack111llll111_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive)
  except Exception as bstack1ll1llll1l_opy_:
    logger.error(bstack1ll111111l_opy_.format(bstack1ll1lll_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠩତ"), str(bstack1ll1llll1l_opy_)))
    raise bstack1ll1llll1l_opy_
  bstack11ll1ll1l_opy_ = bstack1lll1lll11_opy_.bstack11l1llllll_opy_(EVENTS.bstack11ll1l1ll_opy_.value)
  if a11y.is_enabled_platform(CONFIG, bstack111111lll1_opy_) and a11y.is_platform_supported(self.caps, options, desired_capabilities):
    if CONFIG[bstack1ll1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ଥ")][bstack1ll1lll_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫଦ")] == True:
      threading.current_thread().appA11yPlatform = True
      if cli.accessibility is None or not cli.accessibility.is_enabled():
        a11y.set_capabilities(bstack1111lll1ll_opy_, CONFIG)
  try:
    bstack111l111l1l_opy_ = bstack1ll1lll_opy_ (u"࠭ࠧଧ")
    if bstack1l11ll1l1l_opy_() >= version.parse(bstack1ll1lll_opy_ (u"ࠧ࠵࠰࠳࠲࠵ࡨ࠱ࠨନ")):
      if self.caps is not None:
        bstack111l111l1l_opy_ = self.caps.get(bstack1ll1lll_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣ଩"))
    else:
      if self.capabilities is not None:
        bstack111l111l1l_opy_ = self.capabilities.get(bstack1ll1lll_opy_ (u"ࠤࡲࡴࡹ࡯࡭ࡢ࡮ࡋࡹࡧ࡛ࡲ࡭ࠤପ"))
    if bstack111l111l1l_opy_:
      bstack11l1111l11_opy_(bstack111l111l1l_opy_)
      if bstack1l11ll1l1l_opy_() <= version.parse(bstack1ll1lll_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪଫ")):
        if bstack1lllll111_opy_.startswith(bstack1ll1lll_opy_ (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࠬବ")) or bstack1lllll111_opy_.startswith(bstack1ll1lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠧଭ")):
          self.command_executor._url = bstack1lllll111_opy_
        else:
          self.command_executor._url = bstack1ll1lll_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢମ") + bstack1lllll111_opy_ + bstack1ll1lll_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦଯ")
      else:
        self.command_executor._url = bstack1ll1lll_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥର") + bstack111l111l1l_opy_ + bstack1ll1lll_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥ଱")
      logger.debug(bstack11111lll11_opy_.format(bstack111l111l1l_opy_))
    else:
      logger.debug(bstack11lll11lll_opy_.format(bstack1ll1lll_opy_ (u"ࠥࡓࡵࡺࡩ࡮ࡣ࡯ࠤࡍࡻࡢࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧࠦଲ")))
  except Exception as e:
    logger.debug(bstack11lll11lll_opy_.format(e))
  if bstack1ll1lll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪଳ") in FRAMEWORK_NAME:
    bstack11l1ll1111_opy_(PLATFORM_INDEX, bstack1l1l11ll1l_opy_)
  bstack1llll1ll1_opy_ = self.session_id
  if bstack1ll1lll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ଴") in FRAMEWORK_NAME or bstack1ll1lll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ଵ") in FRAMEWORK_NAME or bstack1ll1lll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ଶ") in FRAMEWORK_NAME or bstack1ll1lll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩଷ") in FRAMEWORK_NAME:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack1111l1ll1_opy_ = getattr(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡖࡨࡷࡹࡓࡥࡵࡣࠪସ"), None)
  if bstack1ll1lll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪହ") in FRAMEWORK_NAME or bstack1ll1lll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ଺") in FRAMEWORK_NAME:
    TestHubHandler.send_cbt_info(self)
  if bstack1ll1lll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ଻") in FRAMEWORK_NAME and bstack1111l1ll1_opy_ and bstack1111l1ll1_opy_.get(bstack1ll1lll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ଼࠭"), bstack1ll1lll_opy_ (u"ࠧࠨଽ")) == bstack1ll1lll_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩା"):
    TestHubHandler.send_cbt_info(self)
  with bstack1ll111ll11_opy_:
    bstack1lllllllll_opy_.append(self)
  if bstack1ll1lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬି") in CONFIG and bstack1ll1lll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨୀ") in CONFIG[bstack1ll1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧୁ")][bstack111111lll1_opy_]:
    SESSION_NAME = CONFIG[bstack1ll1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨୂ")][bstack111111lll1_opy_][bstack1ll1lll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫୃ")]
  logger.debug(bstack1111l111l1_opy_.format(bstack1llll1ll1_opy_))
  bstack1lll1lll11_opy_.end(EVENTS.bstack11ll1l1ll_opy_.value, bstack11ll1ll1l_opy_ + bstack1ll1lll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢୄ"), bstack11ll1ll1l_opy_ + bstack1ll1lll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ୅"), status=True, failure=None, test_name=SESSION_NAME)
ROBOT_PLAYWRIGHT_CDP_URL = None
bstack111ll11l1l_opy_ = False
bstack11lll1ll1l_opy_ = None
def set_playwright_globals(**kwargs):
    bstack1ll1lll_opy_ (u"ࠤࠥࠦࡎࡴࡪࡦࡥࡷࠤ࡬ࡲ࡯ࡣࡣ࡯ࡷࠥ࡬ࡲࡰ࡯ࠣࡣࡤ࡯࡮ࡪࡶࡢࡣ࠳ࡶࡹࠡ࡫ࡱࡸࡴࠦࡴࡩ࡫ࡶࠤࡲࡵࡤࡶ࡮ࡨࠫࡸࠦ࡮ࡢ࡯ࡨࡷࡵࡧࡣࡦ࠰ࠍࠤࠥࠦࠠࡄࡣ࡯ࡰࡪࡪࠠࡣࡻࠣࡣࡤ࡯࡮ࡪࡶࡢࡣ࠳ࡶࡹࠡࡤࡨࡪࡴࡸࡥࠡࡲࡤࡸࡨ࡮࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠬ࠮ࠦࡳࡰࠢࡷ࡬ࡦࡺࠠ࡮ࡱࡧࡣࡱࡧࡵ࡯ࡥ࡫ࠎࠥࠦࠠࠡࡣࡱࡨࠥࡶࡡࡵࡥ࡫ࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡥࡤࡲࠥࡧࡣࡤࡧࡶࡷࠥࡉࡏࡏࡈࡌࡋ࠱ࠦࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࡡࡑࡅࡒࡋࠬࠡࡧࡷࡧ࠳ࠨࠢࠣ୆")
    g = globals()
    for key, value in kwargs.items():
        g[key] = value
try:
  try:
    import Browser
    import os
    from subprocess import Popen
    from browserstack_sdk.__init__ import get_turboscale_playwright_url
    from browserstack_sdk.sdk_cli.utils.bstack1lll11ll_opy_ import bstack1ll1l1l1_opy_
    def bstack1l1111l1l1_opy_(self, args, **kwargs):
      global CONFIG
      global SELENIUM_OR_PLAYWRIGHT_INSTALLED
      global ROBOT_PLAYWRIGHT_CDP_URL
      global bstack111ll11l1l_opy_
      from browserstack_sdk.__init__ import LAUNCH_PATCH_ROBOT_PLAYWRIGHT
      if(bstack1ll1lll_opy_ (u"ࠥ࡭ࡳࡪࡥࡹ࠰࡭ࡷࠧେ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"ࠫࢃ࠭ୈ")), bstack1ll1lll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ୉"), bstack1ll1lll_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨ୊")), bstack1ll1lll_opy_ (u"ࠧࡸࠩୋ")) as fp:
          fp.write(bstack1ll1lll_opy_ (u"ࠣࠤୌ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1ll1lll_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸࡠࡤࡶࡸࡦࡩ࡫࠯࡬ࡶ୍ࠦ")))):
          with open(args[1], bstack1ll1lll_opy_ (u"ࠪࡶࠬ୎")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1ll1lll_opy_ (u"ࠫࡦࡹࡹ࡯ࡥࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࡥ࡮ࡦࡹࡓࡥ࡬࡫ࠨࡤࡱࡱࡸࡪࡾࡴ࠭ࠢࡳࡥ࡬࡫ࠠ࠾ࠢࡹࡳ࡮ࡪࠠ࠱ࠫࠪ୏") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1l1ll1l1l_opy_)
            if bstack1ll1lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ୐") in CONFIG and str(CONFIG[bstack1ll1lll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ୑")]).lower() != bstack1ll1lll_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭୒"):
                cdpUrl = get_turboscale_playwright_url()
                LAUNCH_PATCH_ROBOT_PLAYWRIGHT = bstack1ll1lll_opy_ (u"ࠨࠩࠪࠎ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠊࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠻࡝ࠡ࠿ࡀࡁࠥ࠭ࡴࡳࡷࡨࠫࡀࠐࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹࡝࠼ࠌࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠ࠿ࠏࡩ࡯࡯ࡵࡷࠤࡵࡥࡩ࡯ࡦࡨࡼࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠳࡟࠾ࠎࡨࡵ࡮ࡴࡶࠣࡦࡸࡺࡡࡤ࡭ࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠺࡝ࠡ࠿ࡀࡁࠥ࠭ࡴࡳࡷࡨࠫࡀࠐࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴ࡳ࡭࡫ࡦࡩ࠭࠶ࠬࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠸࠭ࡀࠐࡣࡰࡰࡶࡸࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭ࠣࡁࠥࡸࡥࡲࡷ࡬ࡶࡪ࠮ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦ࠮ࡁࠊࡤࡱࡱࡷࡹࠦ࡯ࡳ࡫ࡪ࡭ࡳࡧ࡬ࡠࡥ࡫ࡶࡴࡳࡩࡶ࡯ࡢࡰࡦࡻ࡮ࡤࡪࠣࡁࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡲࡡࡶࡰࡦ࡬࠳ࡨࡩ࡯ࡦࠫ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯ࠬ࠿ࠏ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡲࡡࡶࡰࡦ࡬ࠥࡃࠠࡢࡵࡼࡲࡨࠦࠨ࡭ࡣࡸࡲࡨ࡮ࡏࡱࡶ࡬ࡳࡳࡹࠩࠡ࠿ࡁࠤࢀࢁࠊࠡࠢ࡬ࡪࠥ࠮ࠡࡣࡵࡷࡥࡨࡱ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠭ࠥࢁࡻࠋࠢࠣࠤࠥࡸࡥࡵࡷࡵࡲࠥࡧࡷࡢ࡫ࡷࠤࡴࡸࡩࡨ࡫ࡱࡥࡱࡥࡣࡩࡴࡲࡱ࡮ࡻ࡭ࡠ࡮ࡤࡹࡳࡩࡨࠩ࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠪ࠽ࠍࠤࠥࢃࡽࠋࠢࠣࡰࡪࡺࠠࡤࡣࡳࡷࡀࠐࠠࠡࡶࡵࡽࠥࢁࡻࠋࠢࠣࠤࠥࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࠼ࠌࠣࠤࢂࢃࠠࡤࡣࡷࡧ࡭ࠦࠨࡦࡺࠬࠤࢀࢁࠊࠡࠢࠣࠤࡨࡵ࡮ࡴࡱ࡯ࡩ࠳࡫ࡲࡳࡱࡵࠬࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࡀࠢ࠭ࠢࡨࡼ࠮ࡁࠊࠡࠢࢀࢁࠏࠦࠠࡪࡨࠣࠬࡧࡹࡴࡢࡥ࡮ࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ࠭ࠥࢁࡻࠋࠢࠣࠤࠥࡸࡥࡵࡷࡵࡲࠥࡧࡷࡢ࡫ࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡨࡵ࡮࡯ࡧࡦࡸࡔࡼࡥࡳࡅࡇࡔ࠭ࢁࡻࠋࠢࠣࠤࠥࠦࠠࡦࡰࡧࡴࡴ࡯࡮ࡵࡗࡕࡐ࠿ࠦࠧࡼࡥࡧࡴ࡚ࡸ࡬ࡾࠩࠣ࠯ࠥ࡫࡮ࡤࡱࡧࡩ࡚ࡘࡉࡄࡱࡰࡴࡴࡴࡥ࡯ࡶࠫࡎࡘࡕࡎ࠯ࡵࡷࡶ࡮ࡴࡧࡪࡨࡼࠬࡨࡧࡰࡴࠫࠬ࠰ࠏࠦࠠࠡࠢࠣࠤ࠳࠴࠮࡭ࡣࡸࡲࡨ࡮ࡏࡱࡶ࡬ࡳࡳࡹࠊࠡࠢࠣࠤࢂࢃࠩ࠼ࠌࠣࠤࢂࢃࠊࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭࠯ࡥࡲࡲࡳ࡫ࡣࡵࠪࡾࡿࠏࠦࠠࠡࠢࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹࡀࠠࠨࡽࡦࡨࡵ࡛ࡲ࡭ࡿࠪࠤ࠰ࠦࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭࠱ࠐࠠࠡࠢࠣ࠲࠳࠴࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸࠐࠠࠡࡿࢀ࠭ࡀࠐࡽࡾ࠽ࠍࡧࡴࡴࡳࡵࠢࡲࡶ࡮࡭ࡩ࡯ࡣ࡯ࡣࡨࡵ࡮࡯ࡧࡦࡸࠥࡃࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮ࡤࡱࡱࡲࡪࡩࡴ࠯ࡤ࡬ࡲࡩ࠮ࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠯࠻ࠋ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭࠯ࡥࡲࡲࡳ࡫ࡣࡵࠢࡀࠤࡦࡹࡹ࡯ࡥࠣࠬࡨࡵ࡮࡯ࡧࡦࡸࡔࡶࡴࡪࡱࡱࡷ࠮ࠦ࠽࠿ࠢࡾࡿࠏࠦࠠࡪࡨࠣࠬࠦࡨࡳࡵࡣࡦ࡯ࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠫࠣࡿࢀࠐࠠࠡࠢࠣࡶࡪࡺࡵࡳࡰࠣࡥࡼࡧࡩࡵࠢࡲࡶ࡮࡭ࡩ࡯ࡣ࡯ࡣࡨࡵ࡮࡯ࡧࡦࡸ࠭ࡩ࡯࡯ࡰࡨࡧࡹࡕࡰࡵ࡫ࡲࡲࡸ࠯࠻ࠋࠢࠣࢁࢂࠐࠠࠡ࡮ࡨࡸࠥࡩࡡࡱࡵ࠾ࠎࠥࠦࡴࡳࡻࠣࡿࢀࠐࠠࠡࠢࠣࡧࡦࡶࡳࠡ࠿ࠣࡎࡘࡕࡎ࠯ࡲࡤࡶࡸ࡫ࠨࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷ࠮ࡁࠊࠡࠢࢀࢁࠥࡩࡡࡵࡥ࡫ࠤ࠭࡫ࡸࠪࠢࡾࡿࠏࠦࠠࡾࡿࠍࠤࠥࡩ࡯࡯ࡵࡷࠤࡲࡵࡤࡪࡨ࡬ࡩࡩࡋ࡮ࡥࡲࡲ࡭ࡳࡺࠠ࠾ࠢࠪࡿࡨࡪࡰࡖࡴ࡯ࢁࠬࠦࠫࠡࡧࡱࡧࡴࡪࡥࡖࡔࡌࡇࡴࡳࡰࡰࡰࡨࡲࡹ࠮ࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡤࡣࡳࡷ࠮࠯࠻ࠋࠢࠣ࡭࡫ࠦࠨࡣࡵࡷࡥࡨࡱ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠩࠡࡽࡾࠎࠥࠦࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡣࡺࡥ࡮ࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮ࡤࡱࡱࡲࡪࡩࡴࡐࡸࡨࡶࡈࡊࡐࠩࡽࡾࠎࠥࠦࠠࠡࠢࠣࡩࡳࡪࡰࡰ࡫ࡱࡸ࡚ࡘࡌ࠻ࠢࡰࡳࡩ࡯ࡦࡪࡧࡧࡉࡳࡪࡰࡰ࡫ࡱࡸ࠱ࠐࠠࠡࠢࠣࠤࠥ࠴࠮࠯ࡥࡲࡲࡳ࡫ࡣࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠌࠣࠤࠥࠦࡽࡾࠫ࠾ࠎࠥࠦࡽࡾࠌࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣࡳࡷ࡯ࡧࡪࡰࡤࡰࡤࡩ࡯࡯ࡰࡨࡧࡹ࠮ࡻࡼࠌࠣࠤࠥࠦ࠮࠯࠰ࡦࡳࡳࡴࡥࡤࡶࡒࡴࡹ࡯࡯࡯ࡵ࠯ࠎࠥࠦࠠࠡࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸ࠿ࠦ࡭ࡰࡦ࡬ࡪ࡮࡫ࡤࡆࡰࡧࡴࡴ࡯࡮ࡵࠌࠣࠤࢂࢃࠩ࠼ࠌࢀࢁࡀࠐ࠯ࠫࠢࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࠦࠪ࠰ࠌࠪࠫࠬ୓").format(cdpUrl=cdpUrl)
            lines.insert(1, LAUNCH_PATCH_ROBOT_PLAYWRIGHT)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1ll1lll_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸࡠࡤࡶࡸࡦࡩ࡫࠯࡬ࡶࠦ୔")), bstack1ll1lll_opy_ (u"ࠪࡻࠬ୕")) as bstack111l11lll1_opy_:
              bstack111l11lll1_opy_.writelines(lines)
        CONFIG[bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ୖ")] = str(FRAMEWORK_NAME) + str(__version__)
        bstack111ll11l_opy_ = os.environ[bstack1ll1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪୗ")]
        bstack11l11l111l_opy_ = TestHubUtils.bstack11ll111ll1_opy_(CONFIG, FRAMEWORK_NAME)
        CONFIG[bstack1ll1lll_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ୘")] = bstack111ll11l_opy_
        CONFIG[bstack1ll1lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩ୙")] = bstack11l11l111l_opy_
        bstack111111lll1_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
        try:
          if PARALLELISE_VANILLA_PYTHON is True:
            bstack111111lll1_opy_ = int(multiprocessing.current_process().name)
          elif PARALLELISE_THREADING_PYTHON is True:
            bstack111111lll1_opy_ = int(threading.current_thread().name)
        except Exception:
          bstack111111lll1_opy_ = 0
        CONFIG[bstack1ll1lll_opy_ (u"ࠣࡷࡶࡩ࡜࠹ࡃࠣ୚")] = False
        CONFIG[bstack1ll1lll_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ୛")] = True
        bstack1ll1111lll_opy_ = bstack1ll1l1l1_opy_(bstack111111lll1_opy_)
        if bstack1ll1111lll_opy_ is not None:
          import bstack_utils.constants as _11ll1l1l1l_opy_
          _111l111ll_opy_ = bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫଡ଼") if bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬଢ଼") in bstack1ll1111lll_opy_ else bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ୞")
          _11ll1l11ll_opy_ = bstack1ll1111lll_opy_.get(_111l111ll_opy_, bstack1ll1lll_opy_ (u"࠭ࠧୟ")).strip().lower()
          _1lll1ll1l_opy_ = _11ll1l11ll_opy_ in _11ll1l1l1l_opy_.bstack11l1111lll_opy_
          if bstack1ll1111lll_opy_.get(bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ୠ")) and not _1lll1ll1l_opy_:
            bstack1ll1111lll_opy_[bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧୡ")] = False
            _111l1ll11l_opy_ = [k for k in bstack1ll1111lll_opy_ if k.startswith(bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨୢ"))]
            for k in _111l1ll11l_opy_:
              del bstack1ll1111lll_opy_[k]
          bstack11ll11l1_opy_ = bstack1ll1111lll_opy_
          import urllib.parse
          if bstack1ll1lll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧୣ") in CONFIG and str(CONFIG[bstack1ll1lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ୤")]).lower() != bstack1ll1lll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ୥"):
            ROBOT_PLAYWRIGHT_CDP_URL = get_turboscale_playwright_url() + urllib.parse.quote(json.dumps(bstack11ll11l1_opy_))
          else:
            ROBOT_PLAYWRIGHT_CDP_URL = bstack1ll1lll_opy_ (u"࠭ࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠨ୦") + urllib.parse.quote(json.dumps(bstack11ll11l1_opy_))
          os.environ[bstack1ll1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡐࡄࡒࡘࡤࡖࡗࡠࡅࡇࡔࡤ࡛ࡒࡍࠩ୧")] = ROBOT_PLAYWRIGHT_CDP_URL
          bstack111ll11l1l_opy_ = True
          from browserstack_sdk.sdk_cli.bstack1ll11ll1_opy_ import bstack111lll11l_opy_
          from browserstack_sdk.sdk_cli.bstack11llll11l1_opy_ import bstack11ll1l1l_opy_
          instance = next(iter(bstack111lll11l_opy_.bstack111llll1l_opy_.values()), None)
          if instance:
            bstack11ll1l1l_opy_.bstack1l1l11lll_opy_(instance, bstack11ll1l1l_opy_.bstack11111l11l_opy_, bstack1ll1111lll_opy_)
            bstack11ll1l1l_opy_.bstack1l1l11lll_opy_(instance, bstack11ll1l1l_opy_.bstack1l111ll111_opy_, ROBOT_PLAYWRIGHT_CDP_URL)
          try:
            from browserstack_sdk.sdk_cli.cli import cli as _1ll11l1l_opy_
            from browserstack_sdk.sdk_cli.bstack1ll11ll1_opy_ import bstack111l11ll_opy_, bstack1lll1ll11_opy_
            _1ll11l1l_opy_.bstack1ll11ll1_opy_.bstack11111lll1l_opy_(
              None,
              (instance, bstack1ll1lll_opy_ (u"ࠨ࡯ࡲࡨࡤࡶ࡯ࡱࡧࡱࠫ୨")),
              (bstack111l11ll_opy_.bstack11ll1lll1_opy_, bstack1lll1ll11_opy_.PRE),
              None,
            )
          except Exception as e:
            logger.debug(bstack1ll1lll_opy_ (u"ࠤࡰࡳࡩࡥࡰࡰࡲࡨࡲ࠿ࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡩ࡭ࡷ࡫ࠠࡄࡔࡈࡅ࡙ࡋ࠮ࡑࡔࡈ࠾ࠥࢁࡽࠣ୩").format(e))
          logger.debug(bstack1ll1lll_opy_ (u"ࠥࡱࡴࡪ࡟ࡱࡱࡳࡩࡳࡀࠠࡶࡵ࡬ࡲ࡬ࠦࡦࡪࡰࡤࡰࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠤ࡫ࡸ࡯࡮ࠢࡇࡶ࡮ࡼࡥࡳࡋࡱ࡭ࡹࠨ୪"))
        else:
          bstack11ll11l1_opy_ = get_caps(CONFIG, bstack111111lll1_opy_)
          if CONFIG.get(bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ୫")):
            update_caps_for_local(bstack11ll11l1_opy_)
            bstack11ll11l1_opy_[bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭୬")] = os.environ[bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨ୭")]
          logger.debug(bstack1ll1lll_opy_ (u"ࠢ࡮ࡱࡧࡣࡵࡵࡰࡦࡰ࠽ࠤࡉࡸࡩࡷࡧࡵࡍࡳ࡯ࡴࠡࡷࡱࡥࡻࡧࡩ࡭ࡣࡥࡰࡪ࠲ࠠࡧࡣ࡯ࡰ࡮ࡴࡧࠡࡤࡤࡧࡰࠦࡴࡰࠢࡪࡩࡹࡥࡣࡢࡲࡶࠦ୮"))
        logger.debug(CONFIG_FILE_CONTENT.format(str(bstack11ll11l1_opy_)))
        if bstack1ll1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ୯") in CONFIG and bstack1ll1lll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ୰") in CONFIG[bstack1ll1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ୱ")][bstack111111lll1_opy_]:
          SESSION_NAME = CONFIG[bstack1ll1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ୲")][bstack111111lll1_opy_][bstack1ll1lll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ୳")]
        from bstack_utils.helper import bstack1l111llll_opy_
        args.append(bstack1ll1lll_opy_ (u"࠭ࡴࡳࡷࡨࠫ୴") if bstack1l111llll_opy_(CONFIG) else bstack1ll1lll_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭୵"))
        args.append(str(bstack11ll11l1_opy_.get(bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ୶"), False)).lower())
        args.append(os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"ࠩࢁࠫ୷")), bstack1ll1lll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ୸"), bstack1ll1lll_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭୹")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack11ll11l1_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1ll1lll_opy_ (u"ࠧ࡯࡮ࡥࡧࡻࡣࡧࡹࡴࡢࡥ࡮࠲࡯ࡹࠢ୺"))
      SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
      return bstack111l111l11_opy_(self, args, **kwargs)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1ll1111l1_opy_(self,
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
    CONFIG[bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ୻")] = str(FRAMEWORK_NAME) + str(__version__)
    bstack111ll11l_opy_ = os.environ[bstack1ll1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ୼")]
    bstack11l11l111l_opy_ = TestHubUtils.bstack11ll111ll1_opy_(CONFIG, FRAMEWORK_NAME)
    CONFIG[bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ୽")] = bstack111ll11l_opy_
    CONFIG[bstack1ll1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ୾")] = bstack11l11l111l_opy_
    bstack111111lll1_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
    try:
      if PARALLELISE_VANILLA_PYTHON is True:
        bstack111111lll1_opy_ = int(multiprocessing.current_process().name)
      elif PARALLELISE_THREADING_PYTHON is True:
        bstack111111lll1_opy_ = int(threading.current_thread().name)
    except Exception:
      bstack111111lll1_opy_ = 0
    CONFIG[bstack1ll1lll_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤ୿")] = True
    bstack1111lll1ll_opy_ = get_caps(CONFIG, bstack111111lll1_opy_)
    bstack11l1ll11_opy_ = bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬ஀") if bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭஁") in bstack1111lll1ll_opy_ else bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫஂ")
    bstack11l111ll_opy_ = False
    try:
        from bstack_utils import accessibility as a11y
        import bstack_utils.constants as bstack11ll11llll_opy_
        bstack11llll1l_opy_ = bstack1111lll1ll_opy_.get(bstack11l1ll11_opy_, bstack1ll1lll_opy_ (u"ࠧࠨஃ")).strip().lower()
        browser_version = str(bstack1111lll1ll_opy_.get(bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪ஄"), bstack1111lll1ll_opy_.get(bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪஅ"), bstack1ll1lll_opy_ (u"ࠪࠫஆ")))).strip()
        bstack1llll1l11_opy_ = bstack11llll1l_opy_ in bstack11ll11llll_opy_.bstack11l1111lll_opy_
        min_version = bstack11ll11llll_opy_.MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION
        if not browser_version or browser_version.lower().startswith(bstack1ll1lll_opy_ (u"ࠫࡱࡧࡴࡦࡵࡷࠫஇ")):
            bstack1l11l11l1l_opy_ = True
        else:
            major = browser_version.split(bstack1ll1lll_opy_ (u"ࠬ࠴ࠧஈ"))[0]
            bstack1l11l11l1l_opy_ = major.isdigit() and int(major) > min_version
        if not bstack1l11l11l1l_opy_:
            logger.warning(bstack1ll1lll_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡩࡵࡩࡦࡺࡥࡳࠢࡷ࡬ࡦࡴࠠࡼࡿ࠱ࠤࡈࡻࡲࡳࡧࡱࡸࠥࡼࡥࡳࡵ࡬ࡳࡳࡀࠠࡼࡿࠥஉ").format(min_version, browser_version))
        if a11y.is_enabled_platform(CONFIG, bstack111111lll1_opy_) and bstack1llll1l11_opy_ and bstack1l11l11l1l_opy_ and a11y.is_platform_supported(bstack1111lll1ll_opy_, options=None, config=CONFIG):
            bstack11l111ll_opy_ = True
            import browserstack_sdk
            browserstack_sdk.CONFIG[bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ஊ")] = True
            bstack1111lll1ll_opy_[bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ஋")] = True
            if CONFIG.get(bstack1ll1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ஌")):
                bstack1111lll1ll_opy_[bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ஍")] = CONFIG[bstack1ll1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭எ")]
            import json as _json
            bstack11lllll11_opy_ = os.getenv(bstack1ll1lll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪஏ"))
            bstack11lll1111l_opy_ = bstack1111lll1ll_opy_.get(bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷ࠳ࡧࡵࡵࡪࡗࡳࡰ࡫࡮ࠨஐ"))
            if not bstack11lllll11_opy_ and bstack11lll1111l_opy_:
                os.environ[bstack1ll1lll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ஑")] = bstack11lll1111l_opy_
                bstack11lllll11_opy_ = bstack11lll1111l_opy_
            if bstack11lllll11_opy_:
                bstack1111lll1ll_opy_[bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹ࠮ࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪஒ")] = bstack11lllll11_opy_
            bstack1llll111ll_opy_ = _json.loads(os.getenv(bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪஓ"), bstack1ll1lll_opy_ (u"ࠪࡿࢂ࠭ஔ"))).get(bstack1ll1lll_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬக"))
            if bstack1llll111ll_opy_:
                bstack1111lll1ll_opy_[bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶ࠲ࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ஖")] = bstack1llll111ll_opy_
            bstack1111lll1ll_opy_.pop(bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ஗"), None)
            bstack1111lll1ll_opy_.pop(bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ஘"), None)
            bstack1111lll1ll_opy_.pop(bstack1ll1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨங"), None)
            logger.debug(bstack1ll1lll_opy_ (u"ࠤࡄ࠵࠶ࡿࠠࡦࡰࡤࡦࡱ࡫ࡤࠡࡨࡲࡶࠥࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࠬࢀࢃࠠࡼࡿࠬࠦச").format(
                bstack11llll1l_opy_, browser_version))
    except Exception as e:
        bstack11l111ll_opy_ = False
        logger.debug(bstack1ll1lll_opy_ (u"ࠥࡅ࠶࠷ࡹࠡࡦࡨࡸࡪࡩࡴࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽࠣ஛").format(str(e)))
    logger.debug(CONFIG_FILE_CONTENT.format(str(bstack1111lll1ll_opy_)))
    if CONFIG.get(bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨஜ")):
      update_caps_for_local(bstack1111lll1ll_opy_)
    if bstack1ll1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ஝") in CONFIG and bstack1ll1lll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫஞ") in CONFIG[bstack1ll1lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪட")][bstack111111lll1_opy_]:
      SESSION_NAME = CONFIG[bstack1ll1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ஠")][bstack111111lll1_opy_][bstack1ll1lll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ஡")]
    import urllib
    import json
    if bstack1ll1lll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ஢") in CONFIG and str(CONFIG[bstack1ll1lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨண")]).lower() != bstack1ll1lll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫத"):
        bstack1ll1ll1l11_opy_ = get_turboscale_playwright_url()
        cdpUrl = bstack1ll1ll1l11_opy_ + urllib.parse.quote(json.dumps(bstack1111lll1ll_opy_))
    else:
        cdpUrl = bstack1ll1lll_opy_ (u"࠭ࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠨ஥") + urllib.parse.quote(json.dumps(bstack1111lll1ll_opy_))
    try:
        from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
        PlaywrightDriverWrapperDirect.setup_dispatch_capture()
    except Exception as exc:
        logger.debug(bstack1ll1lll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠤࡨࡧࡰࡵࡷࡵࡩࠥ࡬࡯ࡳࠢࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࡀࠠࠦࡵࠥ஦"), exc)
    if bstack11l111ll_opy_:
        browser = self.connect_over_cdp(cdpUrl)
    else:
        browser = bstack11lll1ll1l_opy_(self, cdpUrl)
    try:
        from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
        wrapper = PlaywrightDriverWrapperDirect(browser, page=None, capabilities=bstack1111lll1ll_opy_, config=CONFIG)
        threading.current_thread().bstackSessionDriver = wrapper
        logger.debug(bstack1ll1lll_opy_ (u"ࠣࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡉࡸࡩࡷࡧࡵ࡛ࡷࡧࡰࡱࡧࡵࡈ࡮ࡸࡥࡤࡶࠣࡷࡪࡺࡵࡱࠢࡦࡳࡲࡶ࡬ࡦࡶࡨࠤ࡫ࡵࡲࠡࡶ࡫ࡶࡪࡧࡤࠡࠧࡶࠦ஧"), threading.get_ident())
        threading.current_thread().bstackTestErrorMessages = []
        if bstack11l111ll_opy_:
            threading.current_thread().a11yPlatform = True
            wrapper.bstackA11yShouldScan = True
        if wrapper.session_id and not wrapper._cbt_info_sent:
            PlaywrightDriverWrapperDirect._send_cbt_info_on_session()
        try:
            from playwright.sync_api import Browser as bstack1111ll1l11_opy_
            if not hasattr(bstack1111ll1l11_opy_, bstack1ll1lll_opy_ (u"ࠩࡢࡦࡸࡺࡡࡤ࡭ࡢࡲࡪࡽ࡟ࡱࡣࡪࡩࡤࡶࡡࡵࡥ࡫ࡩࡩ࠭ந")):
                _111ll11ll1_opy_ = bstack1111ll1l11_opy_.new_page
                def _11lll1l111_opy_(bstack11l1l1l1_opy_, *bstack11l111l1l_opy_, **bstack11l1llll_opy_):
                    if getattr(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩன"), None):
                        try:
                            bstack1ll1lll111_opy_ = bstack11l1l1l1_opy_.contexts[0] if bstack11l1l1l1_opy_.contexts else None
                            if bstack1ll1lll111_opy_ and bstack1ll1lll111_opy_.pages:
                                page = None
                                for _1ll1l111ll_opy_ in bstack1ll1lll111_opy_.pages:
                                    if bstack1ll1lll_opy_ (u"ࠦࡦࡨ࡯ࡶࡶ࠽ࡦࡱࡧ࡮࡬ࠤப") in _1ll1l111ll_opy_.url:
                                        page = _1ll1l111ll_opy_
                                        logger.debug(bstack1ll1lll_opy_ (u"ࠧࡇ࠱࠲ࡻ࠽ࠤࡷ࡫ࡵࡴ࡫ࡱ࡫ࠥࡧࡢࡰࡷࡷ࠾ࡧࡲࡡ࡯࡭ࠣࡴࡦ࡭ࡥࠡࡨࡵࡳࡲࠦࡤࡦࡨࡤࡹࡱࡺࠠࡤࡱࡱࡸࡪࡾࡴࠣ஫"))
                                        break
                                if page is None:
                                    page = bstack1ll1lll111_opy_.new_page(*bstack11l111l1l_opy_, **bstack11l1llll_opy_)
                                    logger.debug(bstack1ll1lll_opy_ (u"ࠨࡁ࠲࠳ࡼ࠾ࠥࡴ࡯ࠡࡤ࡯ࡥࡳࡱࠠࡱࡣࡪࡩࠥ࡬࡯ࡶࡰࡧ࠰ࠥࡩࡲࡦࡣࡷࡩࡩࠦ࡮ࡦࡹࠣࡴࡦ࡭ࡥࠡ࡫ࡱࠤࡩ࡫ࡦࡢࡷ࡯ࡸࠥࡩ࡯࡯ࡶࡨࡼࡹࠨ஬"))
                            elif bstack1ll1lll111_opy_:
                                page = bstack1ll1lll111_opy_.new_page(*bstack11l111l1l_opy_, **bstack11l1llll_opy_)
                                logger.debug(bstack1ll1lll_opy_ (u"ࠢࡂ࠳࠴ࡽ࠿ࠦࡣࡳࡧࡤࡸࡪࡪࠠ࡯ࡧࡺࠤࡵࡧࡧࡦࠢ࡬ࡲࠥࡪࡥࡧࡣࡸࡰࡹࠦࡣࡰࡰࡷࡩࡽࡺࠢ஭"))
                            else:
                                page = _111ll11ll1_opy_(bstack11l1l1l1_opy_, *bstack11l111l1l_opy_, **bstack11l1llll_opy_)
                                logger.debug(bstack1ll1lll_opy_ (u"ࠣࡃ࠴࠵ࡾࡀࠠ࡯ࡱࠣࡨࡪ࡬ࡡࡶ࡮ࡷࠤࡨࡵ࡮ࡵࡧࡻࡸ࠱ࠦࡦࡢ࡮࡯࡭ࡳ࡭ࠠࡣࡣࡦ࡯ࠥࡺ࡯ࠡࡰࡨࡻࡤࡶࡡࡨࡧࠫ࠭ࠧம"))
                        except Exception as bstack1ll1llllll_opy_:
                            logger.debug(bstack1ll1lll_opy_ (u"ࠤࡄ࠵࠶ࡿ࠺ࠡࡦࡨࡪࡦࡻ࡬ࡵࠢࡦࡳࡳࡺࡥࡹࡶࠣࡴࡦ࡭ࡥࠡࡴࡨࡹࡸ࡫ࠠࡧࡣ࡬ࡰࡪࡪࠠࠩࠧࡶ࠭࠱ࠦࡦࡢ࡮࡯࡭ࡳ࡭ࠠࡣࡣࡦ࡯ࠧய"), bstack1ll1llllll_opy_)
                            page = _111ll11ll1_opy_(bstack11l1l1l1_opy_, *bstack11l111l1l_opy_, **bstack11l1llll_opy_)
                    else:
                        page = _111ll11ll1_opy_(bstack11l1l1l1_opy_, *bstack11l111l1l_opy_, **bstack11l1llll_opy_)
                    try:
                        _w = getattr(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩர"), None)
                        if _w and hasattr(_w, bstack1ll1lll_opy_ (u"ࠫࡺࡶࡤࡢࡶࡨࡣࡵࡧࡧࡦࠩற")):
                            _w.update_page(page)
                        if _w and not _w.session_id:
                            try:
                                import json as _json
                                result = page.evaluate(
                                    bstack1ll1lll_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨல"), bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠥࢁࠬள"))
                                if isinstance(result, str):
                                    result = _json.loads(result)
                                if isinstance(result, dict):
                                    sid = result.get(bstack1ll1lll_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪழ")) or result.get(bstack1ll1lll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠬவ")) or result.get(bstack1ll1lll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡌࡨࠬஶ"))
                                    if sid:
                                        import threading as _1111l1l11l_opy_
                                        from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
                                        with PlaywrightDriverWrapperDirect._session_ids_lock:
                                            PlaywrightDriverWrapperDirect._session_ids[_1111l1l11l_opy_.get_ident()] = sid
                                        logger.debug(bstack1ll1lll_opy_ (u"ࠥࡇࡦࡶࡴࡶࡴࡨࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠢࡹ࡭ࡦࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࠧࡶࠦஷ"), sid)
                                        PlaywrightDriverWrapperDirect._send_cbt_info_on_session()
                                    else:
                                        logger.debug(bstack1ll1lll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠥ࡭ࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡆࡨࡸࡦ࡯࡬ࡴࠢࡵࡩࡹࡻࡲ࡯ࡧࡧࠤࡳࡵࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧ࠾ࠥࠫࡳࠣஸ"), result)
                                else:
                                    logger.debug(bstack1ll1lll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࠦࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠣࡶࡪࡹࡵ࡭ࡶ࠽ࠤࠪࡹࠢஹ"), result)
                            except Exception as _1l11ll11l1_opy_:
                                logger.debug(bstack1ll1lll_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡼࡩࡢࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࠪࡹࠢ஺"), _1l11ll11l1_opy_)
                        if (getattr(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭஻"), None)
                                and not getattr(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠨࡣ࠴࠵ࡾࡥࡳࡵࡣࡵࡸࡪࡪࠧ஼"), False)):
                            threading.current_thread().a11y_started = True
                            try:
                                from bstack_utils import accessibility as _1lll1lll1l_opy_
                                bstack111ll1l111_opy_ = getattr(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭஽"), True)
                                _1lll1lll1l_opy_.start_test_capture(_w, bstack111ll1l111_opy_)
                            except Exception:
                                logger.debug(bstack1ll1lll_opy_ (u"ࠥࡈࡪ࡬ࡥࡳࡴࡨࡨࠥࡇ࠱࠲ࡻࠣࡷࡹࡧࡲࡵࡡࡷࡩࡸࡺ࡟ࡤࡣࡳࡸࡺࡸࡥࠡࡨࡤ࡭ࡱ࡫ࡤࠣா"))
                    except Exception as exc:
                        logger.debug(bstack1ll1lll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡶࡲࡧࡥࡹ࡫ࠠࡱࡣࡪࡩࠥ࡯࡮ࠡࡹࡵࡥࡵࡶࡥࡳ࠼ࠣࠩࡸࠨி"), exc)
                    return page
                bstack1111ll1l11_opy_.new_page = _11lll1l111_opy_
                bstack1111ll1l11_opy_._bstack_new_page_patched = True
        except Exception as exc:
            logger.debug(bstack1ll1lll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡸࡨ࡮ࠠࡔࡻࡱࡧࡇࡸ࡯ࡸࡵࡨࡶ࠳ࡴࡥࡸࡡࡳࡥ࡬࡫ࠠࡧࡱࡵࠤࡵࡧࡧࡦࠢࡦࡥࡵࡺࡵࡳࡧ࠽ࠤࠪࡹࠢீ"), exc)
        try:
            from playwright.sync_api import Page as bstack11ll111l_opy_, Browser as _1lll11ll1_opy_
            if not hasattr(bstack11ll111l_opy_, bstack1ll1lll_opy_ (u"࠭࡟ࡣࡵࡷࡥࡨࡱ࡟ࡱࡣࡪࡩࡤࡩ࡬ࡰࡵࡨࡣࡵࡧࡴࡤࡪࡨࡨࠬு")):
                _1lllll1l1l_opy_ = bstack11ll111l_opy_.close
                def _1111llll1_opy_(bstack11l111l11l_opy_, *bstack11ll1l11l_opy_, _bstack_sdk_close=False, **bstack1l111111l_opy_):
                    if not _bstack_sdk_close:
                        logger.debug(bstack1ll1lll_opy_ (u"ࠢࡅࡧࡩࡩࡷࡸࡥࡥࠢࡳࡥ࡬࡫࠮ࡤ࡮ࡲࡷࡪ࠮ࠩࠡ⠖ࠣࡻ࡮ࡲ࡬ࠡࡥ࡯ࡳࡸ࡫ࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦூ"))
                        threading.current_thread().bstack_deferred_page_close = True
                        threading.current_thread().bstack_deferred_page_ref = bstack11l111l11l_opy_
                        return
                    return _1lllll1l1l_opy_(bstack11l111l11l_opy_, *bstack11ll1l11l_opy_, **bstack1l111111l_opy_)
                bstack11ll111l_opy_.close = _1111llll1_opy_
                bstack11ll111l_opy_._bstack_page_close_patched = True
            if not hasattr(_1lll11ll1_opy_, bstack1ll1lll_opy_ (u"ࠨࡡࡥࡷࡹࡧࡣ࡬ࡡࡥࡶࡴࡽࡳࡦࡴࡢࡧࡱࡵࡳࡦࡡࡳࡥࡹࡩࡨࡦࡦࠪ௃")):
                _11ll1llll1_opy_ = _1lll11ll1_opy_.close
                def _1l11ll111_opy_(bstack11l1l1l1_opy_, *bstack111l1111ll_opy_, _bstack_sdk_close=False, **bstack1ll1111ll1_opy_):
                    if not _bstack_sdk_close:
                        logger.debug(bstack1ll1lll_opy_ (u"ࠤࡇࡩ࡫࡫ࡲࡳࡧࡧࠤࡧࡸ࡯ࡸࡵࡨࡶ࠳ࡩ࡬ࡰࡵࡨࠬ࠮ࠦ⠔ࠡࡹ࡬ࡰࡱࠦࡣ࡭ࡱࡶࡩࠥ࡯࡮ࠡࡣࡩࡸࡪࡸ࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤ௄"))
                        threading.current_thread().bstack_deferred_browser_close = True
                        threading.current_thread().bstack_deferred_browser_ref = bstack11l1l1l1_opy_
                        return
                    return _11ll1llll1_opy_(bstack11l1l1l1_opy_, *bstack111l1111ll_opy_, **bstack1ll1111ll1_opy_)
                _1lll11ll1_opy_.close = _1l11ll111_opy_
                _1lll11ll1_opy_._bstack_browser_close_patched = True
            if not hasattr(bstack11ll111l_opy_, bstack1ll1lll_opy_ (u"ࠪࡣࡧࡹࡴࡢࡥ࡮ࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡠࡲࡤࡸࡨ࡮ࡥࡥࠩ௅")):
                _11ll11ll_opy_ = bstack11ll111l_opy_.screenshot
                def _1ll1l111l1_opy_(bstack11l111l11l_opy_, *bstack1lll1l1l_opy_, **bstack1l1l1ll1_opy_):
                    result = _11ll11ll_opy_(bstack11l111l11l_opy_, *bstack1lll1l1l_opy_, **bstack1l1l1ll1_opy_)
                    try:
                        from bstack_utils.testhub_handler import TestHubHandler
                        from bstack_utils.bstack11111l11_opy_ import bstack11lll1l11_opy_
                        if bstack11lll1l11_opy_.on():
                            import base64
                            if isinstance(result, bytes):
                                bstack1llll1l111_opy_ = base64.b64encode(result).decode(bstack1ll1lll_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪெ"))
                            else:
                                bstack1llll1l111_opy_ = str(result)
                            test_uuid = TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack11lll1l11_opy_.current_hook_uuid()
                            if test_uuid and bstack1llll1l111_opy_:
                                TestHubHandler.bstack11lll1l11l_opy_({
                                    bstack1ll1lll_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫே"): bstack1llll1l111_opy_,
                                    bstack1ll1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ை"): test_uuid
                                })
                                logger.debug(bstack1ll1lll_opy_ (u"ࠢࡔࡧࡱࡸࠥࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠦࡴࡰࠢࡒ࠵࠶ࡿࠠࡧࡱࡵࠤࡹ࡫ࡳࡵࠢࡾࢁࠧ௉").format(test_uuid))
                    except Exception as bstack1lllll11l_opy_:
                        logger.debug(bstack1ll1lll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫࡮ࡥࠢࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠣࡸࡴࠦࡏ࠲࠳ࡼ࠾ࠥࢁࡽࠣொ").format(str(bstack1lllll11l_opy_)))
                    return result
                bstack11ll111l_opy_.screenshot = _1ll1l111l1_opy_
                bstack11ll111l_opy_._bstack_screenshot_patched = True
        except Exception as exc:
            logger.debug(bstack1ll1lll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡥࠡࡦࡨࡪࡪࡸࡲࡦࡦࠣࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡤ࡮ࡲࡷࡪࠦࡨࡰࡱ࡮ࡷ࠿ࠦࠥࡴࠤோ"), exc)
        logger.debug(bstack1ll1lll_opy_ (u"ࠥࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࡄࡳ࡫ࡹࡩࡷ࡝ࡲࡢࡲࡳࡩࡷࡊࡩࡳࡧࡦࡸࠥࡹࡥࡵࡷࡳࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࠦࡦࡰࡴࠣࡸ࡭ࡸࡥࡢࡦࠣࡿࢂࠨௌ").format(threading.get_ident()))
    except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡻࡷࡧࡰࡱࡧࡵ࠾ࠥࢁࡽ்ࠣ").format(str(e)))
    return browser
  async def bstack1111llllll_opy_(self, *args, **kwargs):
    global bstack11lll1ll1l_opy_, CONFIG, FRAMEWORK_NAME, __version__, BROWSERSTACK_AUTOMATION
    global PLATFORM_INDEX, PARALLELISE_VANILLA_PYTHON, PARALLELISE_THREADING_PYTHON, SESSION_NAME
    import urllib.parse as _111l11111_opy_
    import json
    ws_endpoint = args[0] if args else kwargs.get(bstack1ll1lll_opy_ (u"ࠬࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵࠩ௎"), kwargs.get(bstack1ll1lll_opy_ (u"࠭ࡷࡴࡡࡨࡲࡩࡶ࡯ࡪࡰࡷࠫ௏"), bstack1ll1lll_opy_ (u"ࠧࠨௐ")))
    bstack1l1lllll1l_opy_ = (ws_endpoint
                 and bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫ௑") in str(ws_endpoint)
                 and bstack1ll1lll_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨ௒") in str(ws_endpoint))
    bstack1ll1111l_opy_ = {}
    if bstack1l1lllll1l_opy_:
        from bstack_utils.helper import bstack1l11l1111l_opy_
        bstack11l11lll1_opy_ = bstack1l11l1111l_opy_()
        try:
            if bstack11l11lll1_opy_:
                CONFIG[bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ௓")] = str(FRAMEWORK_NAME) + str(__version__)
                bstack111ll11l_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ௔"), bstack1ll1lll_opy_ (u"ࠬ࠭௕"))
                if bstack111ll11l_opy_:
                    CONFIG[bstack1ll1lll_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ௖")] = bstack111ll11l_opy_
                CONFIG[bstack1ll1lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩௗ")] = TestHubUtils.bstack11ll111ll1_opy_(CONFIG, FRAMEWORK_NAME)
                bstack111111lll1_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
                try:
                    if PARALLELISE_VANILLA_PYTHON is True:
                        bstack111111lll1_opy_ = int(multiprocessing.current_process().name)
                    elif PARALLELISE_THREADING_PYTHON is True:
                        bstack111111lll1_opy_ = int(threading.current_thread().name)
                except Exception:
                    bstack111111lll1_opy_ = 0
                CONFIG[bstack1ll1lll_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢ௘")] = True
                bstack1ll1111l_opy_ = get_caps(CONFIG, bstack111111lll1_opy_)
                if CONFIG.get(bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭௙")):
                    update_caps_for_local(bstack1ll1111l_opy_)
                if bstack1ll1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭௚") in CONFIG and bstack1ll1lll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ௛") in CONFIG[bstack1ll1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ௜")][bstack111111lll1_opy_]:
                    SESSION_NAME = CONFIG[bstack1ll1lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ௝")][bstack111111lll1_opy_][bstack1ll1lll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ௞")]
                logger.debug(bstack1ll1lll_opy_ (u"ࠣࡅࡤࡷࡪࠦࡁ࠻ࠢࡕࡩࡵࡲࡡࡤࡧࡧࠤࡺࡹࡥࡳࠢࡦࡥࡵࡹࠠࡸ࡫ࡷ࡬ࠥࡿ࡭࡭ࠢࡦࡥࡵࡹ࠺ࠡࡽࢀࠦ௟").format(str(bstack1ll1111l_opy_)))
            else:
                bstack1l1lll1l_opy_ = str(ws_endpoint).split(bstack1ll1lll_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨ௠"))[1]
                bstack1ll1111l_opy_ = json.loads(_111l11111_opy_.unquote(bstack1l1lll1l_opy_))
                bstack1ll1111l_opy_ = bstack1ll1111l_opy_ or {}
                bstack111ll11l_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ௡"), bstack1ll1lll_opy_ (u"ࠫࠬ௢"))
                bstack11l11l111l_opy_ = TestHubUtils.bstack11ll111ll1_opy_(CONFIG, FRAMEWORK_NAME)
                bstack1ll1111l_opy_[bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭௣")] = str(FRAMEWORK_NAME) + str(__version__)
                bstack1ll1111l_opy_[bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ௤")] = BROWSERSTACK_AUTOMATION
                if bstack111ll11l_opy_:
                    bstack1ll1111l_opy_[bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ௥")] = bstack111ll11l_opy_
                bstack1ll1111l_opy_[bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩ௦")] = bstack11l11l111l_opy_
                logger.debug(bstack1ll1lll_opy_ (u"ࠤࡆࡥࡸ࡫ࠠࡅ࠼ࠣࡑࡪࡸࡧࡦࡦࠣࡗࡉࡑࠠࡵࡧ࡯ࡩࡲ࡫ࡴࡳࡻࠣ࡭ࡳࡺ࡯ࠡࡷࡶࡩࡷࠦࡣࡢࡲࡶࠦ௧"))
            ws_url = str(ws_endpoint).split(bstack1ll1lll_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩ௨"))[0]
            ws_endpoint = ws_url + bstack1ll1lll_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ௩") + _111l11111_opy_.quote(json.dumps(bstack1ll1111l_opy_))
            if args:
                args = (ws_endpoint,) + args[1:]
            else:
                if bstack1ll1lll_opy_ (u"ࠬࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵࠩ௪") in kwargs:
                    kwargs[bstack1ll1lll_opy_ (u"࠭ࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶࠪ௫")] = ws_endpoint
                else:
                    kwargs[bstack1ll1lll_opy_ (u"ࠧࡸࡵࡢࡩࡳࡪࡰࡰ࡫ࡱࡸࠬ௬")] = ws_endpoint
            logger.debug(bstack1ll1lll_opy_ (u"ࠣࡎࡨ࡫ࡦࡩࡹࠡࡥࡲࡲࡳ࡫ࡣࡵࠢࡘࡖࡑࠦࡵࡱࡦࡤࡸࡪࡪࠠࡸ࡫ࡷ࡬ࠥࢁࡽࠡࡥࡤࡴࡸࠨ௭").format(bstack1ll1lll_opy_ (u"ࠤࡼࡱࡱࠨ௮") if bstack11l11lll1_opy_ else bstack1ll1lll_opy_ (u"ࠥࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࠨ௯")))
        except Exception as e:
            logger.debug(bstack1ll1lll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡧࡵ࡫ࡪࠦࡣࡢࡲࡶࠤ࡮ࡴࡴࡰࠢࡦࡳࡳࡴࡥࡤࡶ࡙ࠣࡗࡒ࠺ࠡࡽࢀࠦ௰").format(str(e)))
        try:
            from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
            PlaywrightDriverWrapperDirect.setup_dispatch_capture()
        except Exception as exc:
            logger.debug(bstack1ll1lll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠࡥ࡫ࡶࡴࡦࡺࡣࡩࠢࡦࡥࡵࡺࡵࡳࡧࠣ࡭ࡳࠦ࡭ࡰࡦࡢࡧࡴࡴ࡮ࡦࡥࡷ࠾ࠥࠫࡳࠣ௱"), exc)
    browser = await bstack11lll1ll1l_opy_(self, *args, **kwargs)
    if bstack1l1lllll1l_opy_:
        try:
            from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
            wrapper = PlaywrightDriverWrapperDirect(browser, page=None, capabilities=bstack1ll1111l_opy_, config=CONFIG)
            threading.current_thread().bstackSessionDriver = wrapper
            logger.debug(bstack1ll1lll_opy_ (u"ࠨࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡇࡶ࡮ࡼࡥࡳ࡙ࡵࡥࡵࡶࡥࡳࡆ࡬ࡶࡪࡩࡴࠡࡵࡨࡸࡺࡶࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࠢࡩࡳࡷࠦࡴࡩࡴࡨࡥࡩࠦࠥࡴࠤ௲"), threading.get_ident())
            threading.current_thread().bstackTestErrorMessages = []
            if wrapper.session_id and not wrapper._cbt_info_sent:
                PlaywrightDriverWrapperDirect._send_cbt_info_on_session()
            try:
                from playwright.sync_api import Browser as bstack1111ll1l11_opy_
                if not hasattr(bstack1111ll1l11_opy_, bstack1ll1lll_opy_ (u"ࠧࡠࡤࡶࡸࡦࡩ࡫ࡠࡰࡨࡻࡤࡶࡡࡨࡧࡢࡴࡦࡺࡣࡩࡧࡧࠫ௳")):
                    _111ll11ll1_opy_ = bstack1111ll1l11_opy_.new_page
                    def _11lll1l111_opy_(bstack11l1l1l1_opy_, *bstack11l111l1l_opy_, **bstack11l1llll_opy_):
                        page = _111ll11ll1_opy_(bstack11l1l1l1_opy_, *bstack11l111l1l_opy_, **bstack11l1llll_opy_)
                        try:
                            _w = getattr(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ௴"), None)
                            if _w and hasattr(_w, bstack1ll1lll_opy_ (u"ࠩࡸࡴࡩࡧࡴࡦࡡࡳࡥ࡬࡫ࠧ௵")):
                                _w.update_page(page)
                        except Exception as exc:
                            logger.debug(bstack1ll1lll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡵࡱࡦࡤࡸࡪࠦࡰࡢࡩࡨࠤ࡮ࡴࠠࡸࡴࡤࡴࡵ࡫ࡲࠡࠪࡰࡳࡩࡥࡣࡰࡰࡱࡩࡨࡺࠩ࠻ࠢࠨࡷࠧ௶"), exc)
                        return page
                    bstack1111ll1l11_opy_.new_page = _11lll1l111_opy_
                    bstack1111ll1l11_opy_._bstack_new_page_patched = True
            except Exception as exc:
                logger.debug(bstack1ll1lll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡷࡧ࡭ࠦࡓࡺࡰࡦࡆࡷࡵࡷࡴࡧࡵ࠲ࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠦࡩ࡯ࠢࡰࡳࡩࡥࡣࡰࡰࡱࡩࡨࡺ࠺ࠡࠧࡶࠦ௷"), exc)
            try:
                from playwright.sync_api import Page as bstack11ll111l_opy_, Browser as _1lll11ll1_opy_
                if not hasattr(bstack11ll111l_opy_, bstack1ll1lll_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥࡰࡢࡩࡨࡣࡨࡲ࡯ࡴࡧࡢࡴࡦࡺࡣࡩࡧࡧࠫ௸")):
                    _1lllll1l1l_opy_ = bstack11ll111l_opy_.close
                    def _1111llll1_opy_(bstack11l111l11l_opy_, *bstack11ll1l11l_opy_, _bstack_sdk_close=False, **bstack1l111111l_opy_):
                        if not _bstack_sdk_close:
                            logger.debug(bstack1ll1lll_opy_ (u"ࠨࡄࡦࡨࡨࡶࡷ࡫ࡤࠡࡲࡤ࡫ࡪ࠴ࡣ࡭ࡱࡶࡩ࠭࠯ࠠ⠕ࠢࡺ࡭ࡱࡲࠠࡤ࡮ࡲࡷࡪࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥ௹"))
                            threading.current_thread().bstack_deferred_page_close = True
                            threading.current_thread().bstack_deferred_page_ref = bstack11l111l11l_opy_
                            return
                        return _1lllll1l1l_opy_(bstack11l111l11l_opy_, *bstack11ll1l11l_opy_, **bstack1l111111l_opy_)
                    bstack11ll111l_opy_.close = _1111llll1_opy_
                    bstack11ll111l_opy_._bstack_page_close_patched = True
                if not hasattr(_1lll11ll1_opy_, bstack1ll1lll_opy_ (u"ࠧࡠࡤࡶࡸࡦࡩ࡫ࡠࡤࡵࡳࡼࡹࡥࡳࡡࡦࡰࡴࡹࡥࡠࡲࡤࡸࡨ࡮ࡥࡥࠩ௺")):
                    _11ll1llll1_opy_ = _1lll11ll1_opy_.close
                    def _1l11ll111_opy_(bstack11l1l1l1_opy_, *bstack111l1111ll_opy_, _bstack_sdk_close=False, **bstack1ll1111ll1_opy_):
                        if not _bstack_sdk_close:
                            logger.debug(bstack1ll1lll_opy_ (u"ࠣࡆࡨࡪࡪࡸࡲࡦࡦࠣࡦࡷࡵࡷࡴࡧࡵ࠲ࡨࡲ࡯ࡴࡧࠫ࠭ࠥ⠚ࠠࡸ࡫࡯ࡰࠥࡩ࡬ࡰࡵࡨࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣ௻"))
                            threading.current_thread().bstack_deferred_browser_close = True
                            threading.current_thread().bstack_deferred_browser_ref = bstack11l1l1l1_opy_
                            return
                        return _11ll1llll1_opy_(bstack11l1l1l1_opy_, *bstack111l1111ll_opy_, **bstack1ll1111ll1_opy_)
                    _1lll11ll1_opy_.close = _1l11ll111_opy_
                    _1lll11ll1_opy_._bstack_browser_close_patched = True
                if not hasattr(bstack11ll111l_opy_, bstack1ll1lll_opy_ (u"ࠩࡢࡦࡸࡺࡡࡤ࡭ࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺ࡟ࡱࡣࡷࡧ࡭࡫ࡤࠨ௼")):
                    _11ll11ll_opy_ = bstack11ll111l_opy_.screenshot
                    def _1ll1l111l1_opy_(bstack11l111l11l_opy_, *bstack1lll1l1l_opy_, **bstack1l1l1ll1_opy_):
                        result = _11ll11ll_opy_(bstack11l111l11l_opy_, *bstack1lll1l1l_opy_, **bstack1l1l1ll1_opy_)
                        try:
                            from bstack_utils.testhub_handler import TestHubHandler
                            from bstack_utils.bstack11111l11_opy_ import bstack11lll1l11_opy_
                            if bstack11lll1l11_opy_.on():
                                import base64
                                if isinstance(result, bytes):
                                    bstack1llll1l111_opy_ = base64.b64encode(result).decode(bstack1ll1lll_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ௽"))
                                else:
                                    bstack1llll1l111_opy_ = str(result)
                                test_uuid = TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack11lll1l11_opy_.current_hook_uuid()
                                if test_uuid and bstack1llll1l111_opy_:
                                    TestHubHandler.bstack11lll1l11l_opy_({
                                        bstack1ll1lll_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪ௾"): bstack1llll1l111_opy_,
                                        bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ௿"): test_uuid
                                    })
                        except Exception as bstack1lllll11l_opy_:
                            logger.debug(bstack1ll1lll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡳࡪࠠࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠡࡶࡲࠤࡔ࠷࠱ࡺࠢࠫࡱࡴࡪ࡟ࡤࡱࡱࡲࡪࡩࡴࠪ࠼ࠣࠩࡸࠨఀ"), bstack1lllll11l_opy_)
                        return result
                    bstack11ll111l_opy_.screenshot = _1ll1l111l1_opy_
                    bstack11ll111l_opy_._bstack_screenshot_patched = True
            except Exception as exc:
                logger.debug(bstack1ll1lll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡧࡴࡴࡦࡪࡩࡸࡶࡪࠦࡤࡦࡨࡨࡶࡷ࡫ࡤࠡࡥ࡯ࡳࡸ࡫ࠠࡩࡱࡲ࡯ࡸࠦࡩ࡯ࠢࡰࡳࡩࡥࡣࡰࡰࡱࡩࡨࡺ࠺ࠡࠧࡶࠦఁ"), exc)
            logger.debug(bstack1ll1lll_opy_ (u"ࠣࡎࡨ࡫ࡦࡩࡹࠡࡥࡲࡲࡳ࡫ࡣࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡸࡷࡧࡣ࡬࡫ࡱ࡫ࠥࡹࡥࡵࡷࡳࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࠦࡦࡰࡴࠣࡸ࡭ࡸࡥࡢࡦࠣࡿࢂࠨం").format(threading.get_ident()))
        except Exception as e:
            logger.debug(bstack1ll1lll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࡷࡳࠤࡱ࡫ࡧࡢࡥࡼࠤࡨࡵ࡮࡯ࡧࡦࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡴࡳࡣࡦ࡯࡮ࡴࡧ࠻ࠢࡾࢁࠧః").format(str(e)))
    return browser
except Exception as e:
    pass
def patch_playwright():
    global SELENIUM_OR_PLAYWRIGHT_INSTALLED
    global FRAMEWORK_NAME
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l11l1111l_opy_
        global bstack11lll1ll1l_opy_
        if not bstack11lll1ll1l_opy_:
            bstack11lll1ll1l_opy_ = BrowserType.connect
        BrowserType.connect = bstack1111llllll_opy_
        if bstack1l11l1111l_opy_():
            BrowserType.launch = bstack1ll1111l1_opy_
            SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
        try:
            from playwright.sync_api._context_manager import PlaywrightContextManager
            if not hasattr(PlaywrightContextManager, bstack1ll1lll_opy_ (u"ࠪࡣࡧࡹࡴࡢࡥ࡮ࡣࡪࡴࡴࡦࡴࡢࡴࡦࡺࡣࡩࡧࡧࠫఄ")):
                _11l11111ll_opy_ = PlaywrightContextManager.__enter__
                def _111111l1l_opy_(bstack111ll1111l_opy_):
                    pw = _11l11111ll_opy_(bstack111ll1111l_opy_)
                    _11l1l1l11_opy_ = pw.stop
                    _1111l11lll_opy_ = threading.current_thread()
                    _1111l11lll_opy_.bstack_deferred_pw_ref = pw
                    _1111l11lll_opy_.bstack_deferred_pw_stop_fn = _11l1l1l11_opy_
                    def _1l111lll1l_opy_(*args, _bstack_sdk_close=False, **kwargs):
                        if not _bstack_sdk_close:
                            logger.debug(bstack1ll1lll_opy_ (u"ࠦࡉ࡫ࡦࡦࡴࡵࡩࡩࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠱ࡷࡹࡵࡰࠩࠫࠣ⠘ࠥࡽࡩ࡭࡮ࠣࡷࡹࡵࡰࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧఅ"))
                            threading.current_thread().bstack_deferred_pw_stop = True
                            return
                        return _11l1l1l11_opy_()
                    pw.stop = _1l111lll1l_opy_
                    return pw
                PlaywrightContextManager.__enter__ = _111111l1l_opy_
                PlaywrightContextManager._bstack_enter_patched = True
        except Exception as e:
            logger.debug(bstack1ll1lll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡸࡨ࡮ࠠࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡇࡴࡴࡴࡦࡺࡷࡑࡦࡴࡡࡨࡧࡵ࠲ࡤࡥࡥ࡯ࡶࡨࡶࡤࡥ࠺ࠡࠧࡶࠦఆ"), e)
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1l1111l1l1_opy_
      SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
    except Exception as e:
      pass
def playwright_set_session_name(context, bstack1l1ll11ll_opy_):
  try:
    if getattr(context, bstack1ll1lll_opy_ (u"࠭ࡰࡢࡩࡨࠫఇ"), None):
      context.page.evaluate(bstack1ll1lll_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣఈ"), bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬఉ")+ json.dumps(bstack1l1ll11ll_opy_) + bstack1ll1lll_opy_ (u"ࠤࢀࢁࠧఊ"))
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽ࠻ࠢࡾࢁࠧఋ").format(str(e), traceback.format_exc()))
def playwright_annotate(context, message, level):
  try:
    if getattr(context, bstack1ll1lll_opy_ (u"ࠫࡵࡧࡧࡦࠩఌ"), None):
      context.page.evaluate(bstack1ll1lll_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨ఍"), bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫఎ") + json.dumps(message) + bstack1ll1lll_opy_ (u"ࠧ࠭ࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠪఏ") + json.dumps(level) + bstack1ll1lll_opy_ (u"ࠨࡿࢀࠫఐ"))
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠢࡾࢁ࠿ࠦࡻࡾࠤ఑").format(str(e), traceback.format_exc()))
@measure(event_name=EVENTS.bstack111ll1l11_opy_, stage=STAGE.bstack1ll1llll_opy_, bstack1ll1l11l1l_opy_=SESSION_NAME)
def bstack1ll11llll1_opy_(self, url):
  global bstack11l1l11111_opy_
  try:
    bstack11l11ll11_opy_(url)
  except Exception as err:
    logger.debug(bstack1111l1ll_opy_.format(str(err)))
  try:
    bstack11l1l11111_opy_(self, url)
  except Exception as e:
    try:
      parsed_error = str(e)
      if any(err_msg in parsed_error for err_msg in bstack111ll1l1_opy_):
        bstack11l11ll11_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1111l1ll_opy_.format(str(err)))
    raise e
def bstack1lll1l1l11_opy_(self):
  global bstack11ll1111l1_opy_
  bstack11ll1111l1_opy_ = self
  return
def bstack1ll11lll_opy_(self):
  global bstack1ll1l1l1ll_opy_
  bstack1ll1l1l1ll_opy_ = self
  return
def bstack111l1l1l11_opy_(test_name, bstack1l1111l111_opy_):
  global CONFIG
  if percy.bstack1l1l11ll11_opy_() == bstack1ll1lll_opy_ (u"ࠥࡸࡷࡻࡥࠣఒ"):
    bstack11l11l1ll_opy_ = os.path.relpath(bstack1l1111l111_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack11l11l1ll_opy_)
    bstack1ll1l11l1l_opy_ = suite_name + bstack1ll1lll_opy_ (u"ࠦ࠲ࠨఓ") + test_name
    threading.current_thread().percySessionName = bstack1ll1l11l1l_opy_
def bstack11llllll11_opy_(self, test, *args, **kwargs):
  global bstack11ll111ll_opy_
  test_name = None
  bstack1l1111l111_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1l1111l111_opy_ = str(test.source)
  bstack111l1l1l11_opy_(test_name, bstack1l1111l111_opy_)
  bstack11ll111ll_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.bstack111l1l1l1_opy_, stage=STAGE.bstack1ll1llll_opy_, bstack1ll1l11l1l_opy_=SESSION_NAME)
def bstack1l1l11ll_opy_(driver, bstack1ll1l11l1l_opy_):
  if not bstack1111111l1_opy_ and bstack1ll1l11l1l_opy_:
      bstack111ll1ll1l_opy_ = {
          bstack1ll1lll_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬఔ"): bstack1ll1lll_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧక"),
          bstack1ll1lll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪఖ"): {
              bstack1ll1lll_opy_ (u"ࠨࡰࡤࡱࡪ࠭గ"): bstack1ll1l11l1l_opy_
          }
      }
      bstack111ll111_opy_ = bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧఘ").format(json.dumps(bstack111ll1ll1l_opy_))
      driver.execute_script(bstack111ll111_opy_)
  if bstack11111l1l_opy_:
      bstack111111ll1_opy_ = {
          bstack1ll1lll_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪఙ"): bstack1ll1lll_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭చ"),
          bstack1ll1lll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨఛ"): {
              bstack1ll1lll_opy_ (u"࠭ࡤࡢࡶࡤࠫజ"): bstack1ll1l11l1l_opy_ + bstack1ll1lll_opy_ (u"ࠧࠡࡲࡤࡷࡸ࡫ࡤࠢࠩఝ"),
              bstack1ll1lll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧఞ"): bstack1ll1lll_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧట")
          }
      }
      if bstack11111l1l_opy_.status == bstack1ll1lll_opy_ (u"ࠪࡔࡆ࡙ࡓࠨఠ"):
          bstack11ll1l1111_opy_ = bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩడ").format(json.dumps(bstack111111ll1_opy_))
          driver.execute_script(bstack11ll1l1111_opy_)
          bstack1111lll1l1_opy_(driver, bstack1ll1lll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬఢ"))
      elif bstack11111l1l_opy_.status == bstack1ll1lll_opy_ (u"࠭ࡆࡂࡋࡏࠫణ"):
          reason = bstack1ll1lll_opy_ (u"ࠢࠣత")
          bstack11l1l1ll1l_opy_ = bstack1ll1l11l1l_opy_ + bstack1ll1lll_opy_ (u"ࠨࠢࡩࡥ࡮ࡲࡥࡥࠩథ")
          if bstack11111l1l_opy_.message:
              reason = str(bstack11111l1l_opy_.message)
              bstack11l1l1ll1l_opy_ = bstack11l1l1ll1l_opy_ + bstack1ll1lll_opy_ (u"ࠩࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸ࠺ࠡࠩద") + reason
          bstack111111ll1_opy_[bstack1ll1lll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ధ")] = {
              bstack1ll1lll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪన"): bstack1ll1lll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ఩"),
              bstack1ll1lll_opy_ (u"࠭ࡤࡢࡶࡤࠫప"): bstack11l1l1ll1l_opy_
          }
          bstack11ll1l1111_opy_ = bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬఫ").format(json.dumps(bstack111111ll1_opy_))
          driver.execute_script(bstack11ll1l1111_opy_)
          bstack1111lll1l1_opy_(driver, bstack1ll1lll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨబ"), reason)
          bstack1l11llll1_opy_(reason, str(bstack11111l1l_opy_), str(PLATFORM_INDEX), logger)
@measure(event_name=EVENTS.bstack111111ll_opy_, stage=STAGE.bstack1ll1llll_opy_, bstack1ll1l11l1l_opy_=SESSION_NAME)
def bstack1l11111111_opy_(driver, test):
  if percy.bstack1l1l11ll11_opy_() == bstack1ll1lll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢభ") and percy.bstack1lll11ll1l_opy_() == bstack1ll1lll_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧమ"):
      bstack11ll1lllll_opy_ = bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧయ"), None)
      bstack1l111l111_opy_(driver, bstack11ll1lllll_opy_, test)
  if (bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩర"), None) and
      bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬఱ"), None)) or (
      bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧల"), None) and
      bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪళ"), None)):
      logger.info(bstack1ll1lll_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠠࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡵࡻࡦࡿ࠮ࠡࠤఴ"))
      a11y.bstack1ll1ll11ll_opy_(driver, name=test.name, path=test.source)
def bstack111111111_opy_(test, bstack1ll1l11l1l_opy_):
    try:
      bstack1ll1l111l_opy_ = datetime.datetime.now()
      data = {}
      if test:
        data[bstack1ll1lll_opy_ (u"ࠪࡲࡦࡳࡥࠨవ")] = bstack1ll1l11l1l_opy_
      if bstack11111l1l_opy_:
        if bstack11111l1l_opy_.status == bstack1ll1lll_opy_ (u"ࠫࡕࡇࡓࡔࠩశ"):
          data[bstack1ll1lll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬష")] = bstack1ll1lll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭స")
        elif bstack11111l1l_opy_.status == bstack1ll1lll_opy_ (u"ࠧࡇࡃࡌࡐࠬహ"):
          data[bstack1ll1lll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ఺")] = bstack1ll1lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ఻")
          if bstack11111l1l_opy_.message:
            data[bstack1ll1lll_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰ఼ࠪ")] = str(bstack11111l1l_opy_.message)
      user = CONFIG[bstack1ll1lll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ఽ")]
      key = CONFIG[bstack1ll1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨా")]
      host = bstack1l11llll1l_opy_(cli.config, [bstack1ll1lll_opy_ (u"ࠨࡡࡱ࡫ࡶࠦి"), bstack1ll1lll_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡦࠤీ"), bstack1ll1lll_opy_ (u"ࠣࡣࡳ࡭ࠧు")], bstack1ll1lll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡵ࡯࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠥూ"))
      url = bstack1ll1lll_opy_ (u"ࠪࡿࢂ࠵ࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡵࡨࡷࡸ࡯࡯࡯ࡵ࠲ࡿࢂ࠴ࡪࡴࡱࡱࠫృ").format(host, bstack1llll1ll1_opy_)
      headers = {
        bstack1ll1lll_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪౄ"): bstack1ll1lll_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ౅"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers, auth=(user, key))
        cli.bstack1111lll11_opy_(bstack1ll1lll_opy_ (u"ࠨࡨࡵࡶࡳ࠾ࡺࡶࡤࡢࡶࡨࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡷࡹࡧࡴࡶࡵࠥె"), datetime.datetime.now() - bstack1ll1l111l_opy_)
    except Exception as e:
      logger.error(bstack11l1l11l11_opy_.format(str(e)))
def bstack11ll11111l_opy_(test, bstack1ll1l11l1l_opy_):
  global CONFIG
  global bstack1ll1l1l1ll_opy_
  global bstack11ll1111l1_opy_
  global bstack1llll1ll1_opy_
  global bstack11111l1l_opy_
  global SESSION_NAME
  global bstack11lll1lll1_opy_
  global bstack1llllll1l_opy_
  global bstack1l111ll1l_opy_
  global bstack1l1l11l11l_opy_
  global bstack1lllllllll_opy_
  global bstack1l1llllll1_opy_
  global bstack1l1l111ll_opy_
  try:
    if not bstack1llll1ll1_opy_:
      with bstack1l1l111ll_opy_:
        bstack11l1l111l_opy_ = os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"ࠧࡿࠩే")), bstack1ll1lll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨై"), bstack1ll1lll_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫ౉"))
        if os.path.exists(bstack11l1l111l_opy_):
          with open(bstack11l1l111l_opy_, bstack1ll1lll_opy_ (u"ࠪࡶࠬొ")) as f:
            content = f.read().strip()
            if content:
              bstack1lll1ll1ll_opy_ = json.loads(bstack1ll1lll_opy_ (u"ࠦࢀࠨో") + content + bstack1ll1lll_opy_ (u"ࠬࠨࡸࠣ࠼ࠣࠦࡾࠨࠧౌ") + bstack1ll1lll_opy_ (u"ࠨࡽ్ࠣ"))
              bstack1llll1ll1_opy_ = bstack1lll1ll1ll_opy_.get(str(threading.get_ident()))
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡲࡦࡣࡧ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡋࡇࡷࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬ౎") + str(e))
  if not is_robot_playwright_installed():
    if bstack1lllllllll_opy_:
      with bstack1ll111ll11_opy_:
        bstack1llllll11_opy_ = bstack1lllllllll_opy_.copy()
      for driver in bstack1llllll11_opy_:
        if bstack1llll1ll1_opy_ == driver.session_id:
          if test:
            bstack1l11111111_opy_(driver, test)
          bstack1l1l11ll_opy_(driver, bstack1ll1l11l1l_opy_)
    elif bstack1llll1ll1_opy_:
      bstack111111111_opy_(test, bstack1ll1l11l1l_opy_)
    if bstack1ll1l1l1ll_opy_:
      bstack1llllll1l_opy_(bstack1ll1l1l1ll_opy_)
    if bstack11ll1111l1_opy_:
      bstack1l111ll1l_opy_(bstack11ll1111l1_opy_)
    if bstack111llll11l_opy_:
      bstack1l1l11l11l_opy_()
def bstack111111ll1l_opy_(self, test, *args, **kwargs):
  bstack1ll1l11l1l_opy_ = None
  if test:
    bstack1ll1l11l1l_opy_ = str(test.name)
  bstack11ll11111l_opy_(test, bstack1ll1l11l1l_opy_)
  bstack11lll1lll1_opy_(self, test, *args, **kwargs)
def bstack1l111l1ll_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack11l1ll1l1_opy_
  global CONFIG
  global bstack1lllllllll_opy_
  global bstack1llll1ll1_opy_
  global bstack1l1l111ll_opy_
  bstack1l1l1ll11l_opy_ = None
  try:
    if bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ౏"), None) or bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ౐"), None):
      try:
        if not bstack1llll1ll1_opy_:
          bstack11l1l111l_opy_ = os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"ࠪࢂࠬ౑")), bstack1ll1lll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ౒"), bstack1ll1lll_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧ౓"))
          with bstack1l1l111ll_opy_:
            if os.path.exists(bstack11l1l111l_opy_):
              with open(bstack11l1l111l_opy_, bstack1ll1lll_opy_ (u"࠭ࡲࠨ౔")) as f:
                content = f.read().strip()
                if content:
                  bstack1lll1ll1ll_opy_ = json.loads(bstack1ll1lll_opy_ (u"ࠢࡼࠤౕ") + content + bstack1ll1lll_opy_ (u"ࠨࠤࡻࠦ࠿ࠦࠢࡺࠤౖࠪ") + bstack1ll1lll_opy_ (u"ࠤࢀࠦ౗"))
                  bstack1llll1ll1_opy_ = bstack1lll1ll1ll_opy_.get(str(threading.get_ident()))
      except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡵࡩࡦࡪࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡎࡊࡳࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢࡷࡩࡸࡺࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࠩౘ") + str(e))
      if bstack1lllllllll_opy_:
        with bstack1ll111ll11_opy_:
          bstack1llllll11_opy_ = bstack1lllllllll_opy_.copy()
        for driver in bstack1llllll11_opy_:
          if bstack1llll1ll1_opy_ == driver.session_id:
            bstack1l1l1ll11l_opy_ = driver
    bstack111ll1l111_opy_ = a11y.is_enabled_testcase(test.tags)
    if bstack1l1l1ll11l_opy_:
      threading.current_thread().isA11yTest = a11y.start_test_capture(bstack1l1l1ll11l_opy_, bstack111ll1l111_opy_)
      threading.current_thread().isAppA11yTest = a11y.start_test_capture(bstack1l1l1ll11l_opy_, bstack111ll1l111_opy_)
    else:
      threading.current_thread().isA11yTest = bstack111ll1l111_opy_
      threading.current_thread().isAppA11yTest = bstack111ll1l111_opy_
  except:
    pass
  bstack11l1ll1l1_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack11111l1l_opy_
  try:
    bstack11111l1l_opy_ = self._test
  except:
    bstack11111l1l_opy_ = self.test
def bstack1l11111l1_opy_():
  global bstack11l111l11_opy_
  try:
    if os.path.exists(bstack11l111l11_opy_):
      os.remove(bstack11l111l11_opy_)
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧౙ") + str(e))
def bstack11lll1l1l1_opy_():
  global bstack11l111l11_opy_
  bstack1l111lll11_opy_ = {}
  lock_file = bstack11l111l11_opy_ + bstack1ll1lll_opy_ (u"ࠬ࠴࡬ࡰࡥ࡮ࠫౚ")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1ll1lll_opy_ (u"࠭ࡦࡪ࡮ࡨࡰࡴࡩ࡫ࠡࡰࡲࡸࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥ࠭ࠢࡸࡷ࡮ࡴࡧࠡࡤࡤࡷ࡮ࡩࠠࡧ࡫࡯ࡩࠥࡵࡰࡦࡴࡤࡸ࡮ࡵ࡮ࡴࠩ౛"))
    try:
      if not os.path.isfile(bstack11l111l11_opy_):
        with open(bstack11l111l11_opy_, bstack1ll1lll_opy_ (u"ࠧࡸࠩ౜")) as f:
          json.dump({}, f)
      if os.path.exists(bstack11l111l11_opy_):
        with open(bstack11l111l11_opy_, bstack1ll1lll_opy_ (u"ࠨࡴࠪౝ")) as f:
          content = f.read().strip()
          if content:
            bstack1l111lll11_opy_ = json.loads(content)
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡷ࡫ࡡࡥ࡫ࡱ࡫ࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫ౞") + str(e))
    return bstack1l111lll11_opy_
  try:
    os.makedirs(os.path.dirname(bstack11l111l11_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      if not os.path.isfile(bstack11l111l11_opy_):
        with open(bstack11l111l11_opy_, bstack1ll1lll_opy_ (u"ࠪࡻࠬ౟")) as f:
          json.dump({}, f)
      if os.path.exists(bstack11l111l11_opy_):
        with open(bstack11l111l11_opy_, bstack1ll1lll_opy_ (u"ࠫࡷ࠭ౠ")) as f:
          content = f.read().strip()
          if content:
            bstack1l111lll11_opy_ = json.loads(content)
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡳࡧࡤࡨ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧౡ") + str(e))
  finally:
    return bstack1l111lll11_opy_
def bstack11l1ll1111_opy_(platform_index, item_index):
  global bstack11l111l11_opy_
  lock_file = bstack11l111l11_opy_ + bstack1ll1lll_opy_ (u"࠭࠮࡭ࡱࡦ࡯ࠬౢ")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1ll1lll_opy_ (u"ࠧࡧ࡫࡯ࡩࡱࡵࡣ࡬ࠢࡱࡳࡹࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦ࠮ࠣࡹࡸ࡯࡮ࡨࠢࡥࡥࡸ࡯ࡣࠡࡨ࡬ࡰࡪࠦ࡯ࡱࡧࡵࡥࡹ࡯࡯࡯ࡵࠪౣ"))
    try:
      bstack1l111lll11_opy_ = {}
      if os.path.exists(bstack11l111l11_opy_):
        with open(bstack11l111l11_opy_, bstack1ll1lll_opy_ (u"ࠨࡴࠪ౤")) as f:
          content = f.read().strip()
          if content:
            bstack1l111lll11_opy_ = json.loads(content)
      bstack1l111lll11_opy_[item_index] = platform_index
      with open(bstack11l111l11_opy_, bstack1ll1lll_opy_ (u"ࠤࡺࠦ౥")) as outfile:
        json.dump(bstack1l111lll11_opy_, outfile)
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡽࡲࡪࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨ౦") + str(e))
    return
  try:
    os.makedirs(os.path.dirname(bstack11l111l11_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      bstack1l111lll11_opy_ = {}
      if os.path.exists(bstack11l111l11_opy_):
        with open(bstack11l111l11_opy_, bstack1ll1lll_opy_ (u"ࠫࡷ࠭౧")) as f:
          content = f.read().strip()
          if content:
            bstack1l111lll11_opy_ = json.loads(content)
      bstack1l111lll11_opy_[item_index] = platform_index
      with open(bstack11l111l11_opy_, bstack1ll1lll_opy_ (u"ࠧࡽࠢ౨")) as outfile:
        json.dump(bstack1l111lll11_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡹࡵ࡭ࡹ࡯࡮ࡨࠢࡷࡳࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫ౩") + str(e))
def bstack1l111l1ll1_opy_(bstack11l11l1l11_opy_):
  global CONFIG
  bstack111ll111l_opy_ = bstack1ll1lll_opy_ (u"ࠧࠨ౪")
  if not bstack1ll1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ౫") in CONFIG:
    logger.info(bstack1ll1lll_opy_ (u"ࠩࡑࡳࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠡࡲࡤࡷࡸ࡫ࡤࠡࡷࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࠦࡲࡦࡲࡲࡶࡹࠦࡦࡰࡴࠣࡖࡴࡨ࡯ࡵࠢࡵࡹࡳ࠭౬"))
  try:
    platform = CONFIG[bstack1ll1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭౭")][bstack11l11l1l11_opy_]
    if bstack1ll1lll_opy_ (u"ࠫࡴࡹࠧ౮") in platform:
      bstack111ll111l_opy_ += str(platform[bstack1ll1lll_opy_ (u"ࠬࡵࡳࠨ౯")]) + bstack1ll1lll_opy_ (u"࠭ࠬࠡࠩ౰")
    if bstack1ll1lll_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪ౱") in platform:
      bstack111ll111l_opy_ += str(platform[bstack1ll1lll_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫ౲")]) + bstack1ll1lll_opy_ (u"ࠩ࠯ࠤࠬ౳")
    if bstack1ll1lll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧ౴") in platform:
      bstack111ll111l_opy_ += str(platform[bstack1ll1lll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨ౵")]) + bstack1ll1lll_opy_ (u"ࠬ࠲ࠠࠨ౶")
    if bstack1ll1lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ౷") in platform:
      bstack111ll111l_opy_ += str(platform[bstack1ll1lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ౸")]) + bstack1ll1lll_opy_ (u"ࠨ࠮ࠣࠫ౹")
    if bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ౺") in platform:
      bstack111ll111l_opy_ += str(platform[bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ౻")]) + bstack1ll1lll_opy_ (u"ࠫ࠱ࠦࠧ౼")
    if bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭౽") in platform:
      bstack111ll111l_opy_ += str(platform[bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ౾")]) + bstack1ll1lll_opy_ (u"ࠧ࠭ࠢࠪ౿")
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠨࡕࡲࡱࡪࠦࡥࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡱ࡫ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡴࡶࡵ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡷ࡫ࡰࡰࡴࡷࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡵ࡮ࠨಀ") + str(e))
  finally:
    if bstack111ll111l_opy_[len(bstack111ll111l_opy_) - 2:] == bstack1ll1lll_opy_ (u"ࠩ࠯ࠤࠬಁ"):
      bstack111ll111l_opy_ = bstack111ll111l_opy_[:-2]
    return bstack111ll111l_opy_
def bstack111ll11l1_opy_(path, bstack111ll111l_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack111lll1l1l_opy_ = ET.parse(path)
    bstack111ll11111_opy_ = bstack111lll1l1l_opy_.getroot()
    bstack1llll11l1_opy_ = None
    for suite in bstack111ll11111_opy_.iter(bstack1ll1lll_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩಂ")):
      if bstack1ll1lll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫಃ") in suite.attrib:
        suite.attrib[bstack1ll1lll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ಄")] += bstack1ll1lll_opy_ (u"࠭ࠠࠨಅ") + bstack111ll111l_opy_
        bstack1llll11l1_opy_ = suite
    bstack111lll1l1_opy_ = None
    for robot in bstack111ll11111_opy_.iter(bstack1ll1lll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ಆ")):
      bstack111lll1l1_opy_ = robot
    bstack11ll1111l_opy_ = len(bstack111lll1l1_opy_.findall(bstack1ll1lll_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧಇ")))
    if bstack11ll1111l_opy_ == 1:
      bstack111lll1l1_opy_.remove(bstack111lll1l1_opy_.findall(bstack1ll1lll_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨಈ"))[0])
      bstack111lll11_opy_ = ET.Element(bstack1ll1lll_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩಉ"), attrib={bstack1ll1lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩಊ"): bstack1ll1lll_opy_ (u"࡙ࠬࡵࡪࡶࡨࡷࠬಋ"), bstack1ll1lll_opy_ (u"࠭ࡩࡥࠩಌ"): bstack1ll1lll_opy_ (u"ࠧࡴ࠲ࠪ಍")})
      bstack111lll1l1_opy_.insert(1, bstack111lll11_opy_)
      bstack11111l1l1_opy_ = None
      for suite in bstack111lll1l1_opy_.iter(bstack1ll1lll_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧಎ")):
        bstack11111l1l1_opy_ = suite
      bstack11111l1l1_opy_.append(bstack1llll11l1_opy_)
      bstack111l1l1ll1_opy_ = None
      for status in bstack1llll11l1_opy_.iter(bstack1ll1lll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩಏ")):
        bstack111l1l1ll1_opy_ = status
      bstack11111l1l1_opy_.append(bstack111l1l1ll1_opy_)
    bstack111lll1l1l_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡳࡵ࡬ࡲ࡬ࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠨಐ") + str(e))
def bstack111l1111l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack111lllll1_opy_
  global CONFIG
  if bstack1ll1lll_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡴࡦࡺࡨࠣ಑") in options:
    del options[bstack1ll1lll_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡵࡧࡴࡩࠤಒ")]
  json_data = bstack11lll1l1l1_opy_()
  for item_id in json_data.keys():
    path = os.path.join(outs_dir, str(item_id), bstack1ll1lll_opy_ (u"࠭࡯ࡶࡶࡳࡹࡹ࠴ࡸ࡮࡮ࠪಓ"))
    bstack111ll11l1_opy_(path, bstack1l111l1ll1_opy_(json_data[item_id]))
  bstack1l11111l1_opy_()
  return bstack111lllll1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack11llll1l1l_opy_(self, ff_profile_dir):
  global bstack11l1l1lll1_opy_
  if not ff_profile_dir:
    return None
  return bstack11l1l1lll1_opy_(self, ff_profile_dir)
def bstack111lll1ll1_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack11llllll1_opy_
  bstack11lll1ll11_opy_ = []
  if bstack1ll1lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪಔ") in CONFIG:
    bstack11lll1ll11_opy_ = CONFIG[bstack1ll1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫಕ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1ll1lll_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࠥಖ")],
      pabot_args[bstack1ll1lll_opy_ (u"ࠥࡺࡪࡸࡢࡰࡵࡨࠦಗ")],
      argfile,
      pabot_args.get(bstack1ll1lll_opy_ (u"ࠦ࡭࡯ࡶࡦࠤಘ")),
      pabot_args[bstack1ll1lll_opy_ (u"ࠧࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠣಙ")],
      platform[0],
      bstack11llllll1_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1ll1lll_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡧ࡫࡯ࡩࡸࠨಚ")] or [(bstack1ll1lll_opy_ (u"ࠢࠣಛ"), None)]
    for platform in enumerate(bstack11lll1ll11_opy_)
  ]
def bstack11l11l11_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack11111l111l_opy_=bstack1ll1lll_opy_ (u"ࠨࠩಜ")):
  global bstack1l1ll111l1_opy_
  self.platform_index = platform_index
  self.bstack1l111l11ll_opy_ = bstack11111l111l_opy_
  bstack1l1ll111l1_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1l1ll1l11_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1ll1lllll_opy_
  global bstack1lll111ll_opy_
  bstack111l1ll1l_opy_ = copy.deepcopy(item)
  if not bstack1ll1lll_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫಝ") in item.options:
    bstack111l1ll1l_opy_.options[bstack1ll1lll_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬಞ")] = []
  bstack1lll11lll1_opy_ = bstack111l1ll1l_opy_.options[bstack1ll1lll_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ಟ")].copy()
  for v in bstack111l1ll1l_opy_.options[bstack1ll1lll_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧಠ")]:
    if bstack1ll1lll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬಡ") in v:
      bstack1lll11lll1_opy_.remove(v)
    if bstack1ll1lll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙ࠧಢ") in v:
      bstack1lll11lll1_opy_.remove(v)
    if bstack1ll1lll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡅࡇࡉࡐࡔࡉࡁࡍࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬಣ") in v:
      bstack1lll11lll1_opy_.remove(v)
  bstack1lll11lll1_opy_.insert(0, bstack1ll1lll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘ࠻ࡽࢀࠫತ").format(bstack111l1ll1l_opy_.platform_index))
  bstack1lll11lll1_opy_.insert(0, bstack1ll1lll_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡇࡉࡋࡒࡏࡄࡃࡏࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘ࠺ࡼࡿࠪಥ").format(bstack111l1ll1l_opy_.bstack1l111l11ll_opy_))
  bstack111l1ll1l_opy_.options[bstack1ll1lll_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ದ")] = bstack1lll11lll1_opy_
  if bstack1lll111ll_opy_:
    bstack111l1ll1l_opy_.options[bstack1ll1lll_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧಧ")].insert(0, bstack1ll1lll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘࡀࡻࡾࠩನ").format(bstack1lll111ll_opy_))
  return bstack1ll1lllll_opy_(caller_id, datasources, is_last, bstack111l1ll1l_opy_, outs_dir)
def bstack1l1llllll_opy_(command, item_index):
  try:
    if global_config.get_property(bstack1ll1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ಩")):
      os.environ[bstack1ll1lll_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩಪ")] = json.dumps(CONFIG[bstack1ll1lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬಫ")][item_index % bstack1ll1ll1111_opy_])
    global bstack1lll111ll_opy_
    os.environ[bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪಬ")] = str(item_index % bstack1ll1ll1111_opy_)
    listener_arg = bstack1ll1lll_opy_ (u"ࠫࠬಭ")
    if is_robot_playwright_installed() and cli.is_enabled(CONFIG):
      listener_arg = bstack1ll1lll_opy_ (u"ࠬࠦ࠭࠮࡮࡬ࡷࡹ࡫࡮ࡦࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡨࡰ࠴ࡲࡰࡤࡲࡸࡤࡲࡩࡴࡶࡨࡲࡪࡸ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠲ࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡑࡣࡷࡧ࡭࡫ࡲࠨಮ")
      logger.debug(bstack1ll1lll_opy_ (u"ࠨࡁࡥࡦ࡬ࡲ࡬ࠦࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡓࡥࡹࡩࡨࡦࡴࠣࡰ࡮ࡹࡴࡦࡰࡨࡶࠥ࡬࡯ࡳࠢ࡬ࡸࡪࡳࠠࡼࡿࠥಯ").format(item_index))
    bstack1lllll1111_opy_ = bstack1ll1lll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡳࡥ࡭ࠣࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠤ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࠠࠣರ") + \
              str(item_index % bstack1ll1ll1111_opy_) + \
              bstack1ll1lll_opy_ (u"ࠣࠢ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠡࠤಱ") + \
              str(item_index) + \
              listener_arg
    if bstack1lll111ll_opy_:
        bstack1lllll1111_opy_ += bstack1ll1lll_opy_ (u"ࠤࠣࠦಲ") + bstack1lll111ll_opy_
    command[0:1] = bstack1lllll1111_opy_.split()
  except Exception as e:
    logger.error(bstack1ll1lll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡰࡳࡩ࡯ࡦࡺ࡫ࡱ࡫ࠥࡩ࡯࡮࡯ࡤࡲࡩࠦࡦࡰࡴࠣࡴࡦࡨ࡯ࡵࠢࡵࡹࡳࡀࠠࡼࡿࠪಳ").format(str(e)))
def bstack1l1ll1l1l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1ll1111ll_opy_
  try:
    bstack1l1llllll_opy_(command, item_index)
    return bstack1ll1111ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
  except Exception as e:
    logger.error(bstack1ll1lll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡢࡤࡲࡸࠥࡸࡵ࡯࠼ࠣࡿࢂ࠭಴").format(str(e)))
    raise e
def bstack1l1l11111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1ll1111ll_opy_
  try:
    bstack1l1llllll_opy_(command, item_index)
    return bstack1ll1111ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
  except Exception as e:
    logger.error(bstack1ll1lll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡥࡳࡹࠦࡲࡶࡰࠣ࠶࠳࠷࠳࠻ࠢࡾࢁࠬವ").format(str(e)))
    try:
      return bstack1ll1111ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
    except Exception as e2:
      logger.error(bstack1ll1lll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠ࠳࠰࠴࠷ࠥ࡬ࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࡽࢀࠫಶ").format(str(e2)))
      raise e
def bstack111l1l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1ll1111ll_opy_
  try:
    bstack1l1llllll_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    return bstack1ll1111ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
  except Exception as e:
    logger.error(bstack1ll1lll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡧࡵࡴࠡࡴࡸࡲࠥ࠸࠮࠲࠷࠽ࠤࢀࢃࠧಷ").format(str(e)))
    try:
      return bstack1ll1111ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
    except Exception as e2:
      logger.error(bstack1ll1lll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡦࡨ࡯ࡵࠢ࠵࠲࠶࠻ࠠࡧࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣࡿࢂ࠭ಸ").format(str(e2)))
      raise e
def _1l1l1l111_opy_(bstack1l11l1l11l_opy_, item_index, process_timeout, sleep_before_start, bstack1ll11111ll_opy_):
  bstack1l1llllll_opy_(bstack1l11l1l11l_opy_, item_index)
  if process_timeout is None:
    process_timeout = 3600
  if sleep_before_start and sleep_before_start > 0:
    time.sleep(min(sleep_before_start, 5))
  return process_timeout
def bstack111lll1l_opy_(command, bstack111l1ll111_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack1ll1111ll_opy_
  global bstack1lllllll11_opy_
  global bstack1lll111ll_opy_
  try:
    for env_name, bstack1l1ll1lll1_opy_ in bstack1lllllll11_opy_.items():
      os.environ[env_name] = bstack1l1ll1lll1_opy_
    bstack1lll111ll_opy_ = bstack1ll1lll_opy_ (u"ࠤࠥಹ")
    bstack1l1llllll_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    if sleep_before_start and sleep_before_start > 0:
      time.sleep(min(sleep_before_start, 5))
    return bstack1ll1111ll_opy_(command, bstack111l1ll111_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack1ll1lll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡣࡱࡷࠤࡷࡻ࡮ࠡ࠷࠱࠴࠿ࠦࡻࡾࠩ಺").format(str(e)))
    try:
      return bstack1ll1111ll_opy_(command, bstack111l1ll111_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack1ll1lll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡢࡤࡲࡸࠥ࡬ࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࡽࢀࠫ಻").format(str(e2)))
      raise e
def bstack1ll1ll111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack1ll1111ll_opy_
  try:
    process_timeout = _1l1l1l111_opy_(command, item_index, process_timeout, sleep_before_start, bstack1ll1lll_opy_ (u"ࠬ࠺࠮࠳಼ࠩ"))
    return bstack1ll1111ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack1ll1lll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠࡳࡷࡱࠤ࠹࠴࠲࠻ࠢࡾࢁࠬಽ").format(str(e)))
    try:
      return bstack1ll1111ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack1ll1lll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡧࡵࡴࠡࡨࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࢀࢃࠧಾ").format(str(e2)))
      raise e
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack1111ll11_opy_(self, runner, quiet=False, capture=True):
  global bstack11lll1l1_opy_
  bstack1lll1111_opy_ = bstack11lll1l1_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack1ll1lll_opy_ (u"ࠨࡧࡻࡧࡪࡶࡴࡪࡱࡱࡣࡦࡸࡲࠨಿ")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1ll1lll_opy_ (u"ࠩࡨࡼࡨࡥࡴࡳࡣࡦࡩࡧࡧࡣ࡬ࡡࡤࡶࡷ࠭ೀ")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1lll1111_opy_
def bstack1l111ll11_opy_(runner, hook_name, context, element, bstack1l1llll111_opy_, *args):
  global bstack1ll111llll_opy_
  try:
    if runner.hooks.get(hook_name):
      bstack1ll1l1lll1_opy_.bstack1l111l1l11_opy_(hook_name, element)
    if bstack1ll111llll_opy_ is None or bstack1ll111llll_opy_:
      bstack1l1llll111_opy_(runner, hook_name, context, *args)
    else:
      bstack1l11l1l111_opy_ = (context,) + args
      bstack1l1llll111_opy_(runner, hook_name, *bstack1l11l1l111_opy_)
    if runner.hooks.get(hook_name):
      bstack1ll1l1lll1_opy_.bstack111111l1l1_opy_(element)
      if hook_name not in [bstack1ll1lll_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠧು"), bstack1ll1lll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡥࡱࡲࠧೂ")] and args and hasattr(args[0], bstack1ll1lll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡣࡲ࡫ࡳࡴࡣࡪࡩࠬೃ")):
        args[0].error_message = bstack1ll1lll_opy_ (u"࠭ࠧೄ")
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣ࡬ࡦࡴࡤ࡭ࡧࠣ࡬ࡴࡵ࡫ࡴࠢ࡬ࡲࠥࡨࡥࡩࡣࡹࡩ࠿ࠦࡻࡾࠩ೅").format(str(e)))
@measure(event_name=EVENTS.bstack1l11lll11l_opy_, stage=STAGE.bstack1ll1llll_opy_, hook_type=bstack1ll1lll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡂ࡮࡯ࠦೆ"), bstack1ll1l11l1l_opy_=SESSION_NAME)
def bstack11lllllll1_opy_(runner, name, context, bstack1l1llll111_opy_, *args):
    if runner.hooks.get(bstack1ll1lll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨೇ")).__name__ != bstack1ll1lll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲ࡟ࡥࡧࡩࡥࡺࡲࡴࡠࡪࡲࡳࡰࠨೈ"):
      bstack1l111ll11_opy_(runner, name, context, runner, bstack1l1llll111_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack11l11l1l_opy_(bstack1ll1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ೉")) else context.browser
      runner.driver_initialised = bstack1ll1lll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤೊ")
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡤࡳ࡫ࡹࡩࡷࠦࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡧࠣࡥࡹࡺࡲࡪࡤࡸࡸࡪࡀࠠࡼࡿࠪೋ").format(str(e)))
def bstack11ll1ll1l1_opy_(runner, name, context, bstack1l1llll111_opy_, *args):
    bstack1l111ll11_opy_(runner, name, context, context.feature, bstack1l1llll111_opy_, *args)
    try:
      if not bstack1111111l1_opy_:
        bstack1l1l1ll11l_opy_ = threading.current_thread().bstackSessionDriver if bstack11l11l1l_opy_(bstack1ll1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ೌ")) else context.browser
        if is_driver_active(bstack1l1l1ll11l_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack1ll1lll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠤ್")
          bstack1l1ll11ll_opy_ = str(runner.feature.name)
          playwright_set_session_name(context, bstack1l1ll11ll_opy_)
          bstack1l1l1ll11l_opy_.execute_script(bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧ೎") + json.dumps(bstack1l1ll11ll_opy_) + bstack1ll1lll_opy_ (u"ࠪࢁࢂ࠭೏"))
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣ࡭ࡳࠦࡢࡦࡨࡲࡶࡪࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫ೐").format(str(e)))
def bstack11lllll1_opy_(runner, name, context, bstack1l1llll111_opy_, *args):
    target = context.scenario if hasattr(context, bstack1ll1lll_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧ೑")) else context.feature
    bstack1l111ll11_opy_(runner, name, context, target, bstack1l1llll111_opy_, *args)
@measure(event_name=EVENTS.bstack11ll1111_opy_, stage=STAGE.bstack1ll1llll_opy_, bstack1ll1l11l1l_opy_=SESSION_NAME)
def bstack111l111l_opy_(runner, name, context, bstack1l1llll111_opy_, *args):
    bstack1ll1l1lll1_opy_.start_test(context)
    bstack1l111ll11_opy_(runner, name, context, context.scenario, bstack1l1llll111_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack1l11l1ll11_opy_.bstack1l1lll111_opy_(context, *args)
    try:
      bstack1l1l1ll11l_opy_ = bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ೒"), context.browser)
      if is_driver_active(bstack1l1l1ll11l_opy_):
        TestHubHandler.send_cbt_info(bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭೓"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack1ll1lll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥ೔")
        if (not bstack1111111l1_opy_):
          scenario_name = args[0].name
          feature_name = bstack1l1ll11ll_opy_ = str(runner.feature.name)
          bstack1l1ll11ll_opy_ = feature_name + bstack1ll1lll_opy_ (u"ࠩࠣ࠱ࠥ࠭ೕ") + scenario_name
          if runner.driver_initialised == bstack1ll1lll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧೖ"):
            playwright_set_session_name(context, bstack1l1ll11ll_opy_)
            bstack1l1l1ll11l_opy_.execute_script(bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩ೗") + json.dumps(bstack1l1ll11ll_opy_) + bstack1ll1lll_opy_ (u"ࠬࢃࡽࠨ೘"))
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱ࠽ࠤࢀࢃࠧ೙").format(str(e)))
@measure(event_name=EVENTS.bstack1l11lll11l_opy_, stage=STAGE.bstack1ll1llll_opy_, hook_type=bstack1ll1lll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࡓࡵࡧࡳࠦ೚"), bstack1ll1l11l1l_opy_=SESSION_NAME)
def bstack1l1llll1l_opy_(runner, name, context, bstack1l1llll111_opy_, *args):
    bstack1l111ll11_opy_(runner, name, context, args[0], bstack1l1llll111_opy_, *args)
    try:
      bstack1l1l1ll11l_opy_ = threading.current_thread().bstackSessionDriver if bstack11l11l1l_opy_(bstack1ll1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ೛")) else context.browser
      if is_driver_active(bstack1l1l1ll11l_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack1ll1lll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢ೜")
        bstack1ll1l1lll1_opy_.bstack1l11ll1111_opy_(args[0])
        if runner.driver_initialised == bstack1ll1lll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣೝ") and not bstack1111111l1_opy_:
          feature_name = bstack1l1ll11ll_opy_ = str(runner.feature.name)
          bstack1l1ll11ll_opy_ = feature_name + bstack1ll1lll_opy_ (u"ࠫࠥ࠳ࠠࠨೞ") + context.scenario.name
          playwright_set_session_name(context, bstack1l1ll11ll_opy_)
          bstack1l1l1ll11l_opy_.execute_script(bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ೟") + json.dumps(bstack1l1ll11ll_opy_) + bstack1ll1lll_opy_ (u"࠭ࡽࡾࠩೠ"))
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡸࡪࡶ࠺ࠡࡽࢀࠫೡ").format(str(e)))
@measure(event_name=EVENTS.bstack1l11lll11l_opy_, stage=STAGE.bstack1ll1llll_opy_, hook_type=bstack1ll1lll_opy_ (u"ࠣࡣࡩࡸࡪࡸࡓࡵࡧࡳࠦೢ"), bstack1ll1l11l1l_opy_=SESSION_NAME)
def bstack1l1l1llll1_opy_(runner, name, context, bstack1l1llll111_opy_, *args):
  bstack1ll1l1lll1_opy_.bstack11ll111l11_opy_(args[0])
  try:
    step_status = args[0].status.name
    bstack1l1l1ll11l_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll1lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨೣ") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack1l1l1ll11l_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack1ll1lll_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪ೤")
        if not bstack1111111l1_opy_:
          feature_name = bstack1l1ll11ll_opy_ = str(runner.feature.name)
          bstack1l1ll11ll_opy_ = feature_name + bstack1ll1lll_opy_ (u"ࠫࠥ࠳ࠠࠨ೥") + context.scenario.name
          playwright_set_session_name(context, bstack1l1ll11ll_opy_)
          bstack1l1l1ll11l_opy_.execute_script(bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ೦") + json.dumps(bstack1l1ll11ll_opy_) + bstack1ll1lll_opy_ (u"࠭ࡽࡾࠩ೧"))
    if str(step_status).lower() in [bstack1ll1lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ೨"), bstack1ll1lll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ೩")]:
      bstack1111l1lll_opy_ = bstack1ll1lll_opy_ (u"ࠩࠪ೪")
      bstack1llll11ll1_opy_ = bstack1ll1lll_opy_ (u"ࠪࠫ೫")
      bstack111111l1_opy_ = bstack1ll1lll_opy_ (u"ࠫࠬ೬")
      try:
        import traceback
        bstack1111l1lll_opy_ = runner.exception.__class__.__name__
        bstack1l1l11l1l_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1llll11ll1_opy_ = bstack1ll1lll_opy_ (u"ࠬࠦࠧ೭").join(bstack1l1l11l1l_opy_)
        bstack111111l1_opy_ = bstack1l1l11l1l_opy_[-1]
      except Exception as e:
        logger.debug(bstack1ll1lllll1_opy_.format(str(e)))
      bstack1111l1lll_opy_ += bstack111111l1_opy_
      playwright_annotate(context, json.dumps(str(args[0].name) + bstack1ll1lll_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧ೮") + str(bstack1llll11ll1_opy_)),
                          bstack1ll1lll_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨ೯"))
      if runner.driver_initialised == bstack1ll1lll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨ೰"):
        bstack11ll11ll11_opy_(getattr(context, bstack1ll1lll_opy_ (u"ࠩࡳࡥ࡬࡫ࠧೱ"), None), bstack1ll1lll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥೲ"), bstack1111l1lll_opy_)
        bstack1l1l1ll11l_opy_.execute_script(bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩೳ") + json.dumps(str(args[0].name) + bstack1ll1lll_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦ೴") + str(bstack1llll11ll1_opy_)) + bstack1ll1lll_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥࢁࢂ࠭೵"))
      if runner.driver_initialised == bstack1ll1lll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧ೶"):
        bstack1111lll1l1_opy_(bstack1l1l1ll11l_opy_, bstack1ll1lll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ೷"), bstack1ll1lll_opy_ (u"ࠤࡖࡧࡪࡴࡡࡳ࡫ࡲࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨ೸") + str(bstack1111l1lll_opy_))
    else:
      playwright_annotate(context, bstack1ll1lll_opy_ (u"ࠥࡔࡦࡹࡳࡦࡦࠤࠦ೹"), bstack1ll1lll_opy_ (u"ࠦ࡮ࡴࡦࡰࠤ೺"))
      if runner.driver_initialised == bstack1ll1lll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥ೻"):
        bstack11ll11ll11_opy_(getattr(context, bstack1ll1lll_opy_ (u"࠭ࡰࡢࡩࡨࠫ೼"), None), bstack1ll1lll_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ೽"))
      bstack1l1l1ll11l_opy_.execute_script(bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭೾") + json.dumps(str(args[0].name) + bstack1ll1lll_opy_ (u"ࠤࠣ࠱ࠥࡖࡡࡴࡵࡨࡨࠦࠨ೿")) + bstack1ll1lll_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩഀ"))
      if runner.driver_initialised == bstack1ll1lll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤഁ"):
        bstack1111lll1l1_opy_(bstack1l1l1ll11l_opy_, bstack1ll1lll_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧം"))
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࠣࡷࡹ࡫ࡰ࠻ࠢࡾࢁࠬഃ").format(str(e)))
  bstack1l111ll11_opy_(runner, name, context, args[0], bstack1l1llll111_opy_, *args)
@measure(event_name=EVENTS.bstack111l11l1l_opy_, stage=STAGE.bstack1ll1llll_opy_, bstack1ll1l11l1l_opy_=SESSION_NAME)
def bstack1111l1llll_opy_(runner, name, context, bstack1l1llll111_opy_, *args):
  bstack1ll1l1lll1_opy_.end_test(args[0])
  try:
    bstack111l1llll1_opy_ = args[0].status.name
    bstack1l1l1ll11l_opy_ = bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ഄ"), context.browser)
    bstack1l11l1ll11_opy_.bstack1111l1111l_opy_(bstack1l1l1ll11l_opy_)
    if str(bstack111l1llll1_opy_).lower() in [bstack1ll1lll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨഅ"), bstack1ll1lll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨആ")]:
      bstack1111l1lll_opy_ = bstack1ll1lll_opy_ (u"ࠪࠫഇ")
      bstack1llll11ll1_opy_ = bstack1ll1lll_opy_ (u"ࠫࠬഈ")
      bstack111111l1_opy_ = bstack1ll1lll_opy_ (u"ࠬ࠭ഉ")
      try:
        import traceback
        bstack1111l1lll_opy_ = runner.exception.__class__.__name__
        bstack1l1l11l1l_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1llll11ll1_opy_ = bstack1ll1lll_opy_ (u"࠭ࠠࠨഊ").join(bstack1l1l11l1l_opy_)
        bstack111111l1_opy_ = bstack1l1l11l1l_opy_[-1]
      except Exception as e:
        logger.debug(bstack1ll1lllll1_opy_.format(str(e)))
      bstack1111l1lll_opy_ += bstack111111l1_opy_
      playwright_annotate(context, json.dumps(str(args[0].name) + bstack1ll1lll_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨഋ") + str(bstack1llll11ll1_opy_)),
                          bstack1ll1lll_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢഌ"))
      if runner.driver_initialised == bstack1ll1lll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦ഍") or runner.driver_initialised == bstack1ll1lll_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪഎ"):
        bstack11ll11ll11_opy_(getattr(context, bstack1ll1lll_opy_ (u"ࠫࡵࡧࡧࡦࠩഏ"), None), bstack1ll1lll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧഐ"), bstack1111l1lll_opy_)
        bstack1l1l1ll11l_opy_.execute_script(bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ഑") + json.dumps(str(args[0].name) + bstack1ll1lll_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨഒ") + str(bstack1llll11ll1_opy_)) + bstack1ll1lll_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨഓ"))
      if runner.driver_initialised == bstack1ll1lll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦഔ") or runner.driver_initialised == bstack1ll1lll_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪക"):
        bstack1111lll1l1_opy_(bstack1l1l1ll11l_opy_, bstack1ll1lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫഖ"), bstack1ll1lll_opy_ (u"࡙ࠧࡣࡦࡰࡤࡶ࡮ࡵࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤഗ") + str(bstack1111l1lll_opy_))
    else:
      playwright_annotate(context, bstack1ll1lll_opy_ (u"ࠨࡐࡢࡵࡶࡩࡩࠧࠢഘ"), bstack1ll1lll_opy_ (u"ࠢࡪࡰࡩࡳࠧങ"))
      if runner.driver_initialised == bstack1ll1lll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥച") or runner.driver_initialised == bstack1ll1lll_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩഛ"):
        bstack11ll11ll11_opy_(getattr(context, bstack1ll1lll_opy_ (u"ࠪࡴࡦ࡭ࡥࠨജ"), None), bstack1ll1lll_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦഝ"))
      bstack1l1l1ll11l_opy_.execute_script(bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪഞ") + json.dumps(str(args[0].name) + bstack1ll1lll_opy_ (u"ࠨࠠ࠮ࠢࡓࡥࡸࡹࡥࡥࠣࠥട")) + bstack1ll1lll_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥࢁࢂ࠭ഠ"))
      if runner.driver_initialised == bstack1ll1lll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥഡ") or runner.driver_initialised == bstack1ll1lll_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩഢ"):
        bstack1111lll1l1_opy_(bstack1l1l1ll11l_opy_, bstack1ll1lll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥണ"))
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭ത").format(str(e)))
  bstack1l111ll11_opy_(runner, name, context, context.scenario, bstack1l1llll111_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack1lll1l1ll1_opy_(runner, name, context, bstack1l1llll111_opy_, *args):
    target = context.scenario if hasattr(context, bstack1ll1lll_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧഥ")) else context.feature
    bstack1l111ll11_opy_(runner, name, context, target, bstack1l1llll111_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack111ll111l1_opy_(runner, name, context, bstack1l1llll111_opy_, *args):
    try:
      bstack1l1l1ll11l_opy_ = bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬദ"), context.browser)
      bstack11l1111ll_opy_ = bstack1ll1lll_opy_ (u"ࠧࠨധ")
      if context.failed is True:
        bstack11l111111_opy_ = []
        bstack1111ll1l1_opy_ = []
        bstack11l1lll11l_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack11l111111_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1l1l11l1l_opy_ = traceback.format_tb(exc_tb)
            bstack1l11ll1l1_opy_ = bstack1ll1lll_opy_ (u"ࠨࠢࠪന").join(bstack1l1l11l1l_opy_)
            bstack1111ll1l1_opy_.append(bstack1l11ll1l1_opy_)
            bstack11l1lll11l_opy_.append(bstack1l1l11l1l_opy_[-1])
        except Exception as e:
          logger.debug(bstack1ll1lllll1_opy_.format(str(e)))
        bstack1111l1lll_opy_ = bstack1ll1lll_opy_ (u"ࠩࠪഩ")
        for i in range(len(bstack11l111111_opy_)):
          bstack1111l1lll_opy_ += bstack11l111111_opy_[i] + bstack11l1lll11l_opy_[i] + bstack1ll1lll_opy_ (u"ࠪࡠࡳ࠭പ")
        bstack11l1111ll_opy_ = bstack1ll1lll_opy_ (u"ࠫࠥ࠭ഫ").join(bstack1111ll1l1_opy_)
        if runner.driver_initialised in [bstack1ll1lll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨബ"), bstack1ll1lll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥഭ")]:
          playwright_annotate(context, bstack11l1111ll_opy_, bstack1ll1lll_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨമ"))
          bstack11ll11ll11_opy_(getattr(context, bstack1ll1lll_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭യ"), None), bstack1ll1lll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤര"), bstack1111l1lll_opy_)
          bstack1l1l1ll11l_opy_.execute_script(bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨറ") + json.dumps(bstack11l1111ll_opy_) + bstack1ll1lll_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣࡿࢀࠫല"))
          bstack1111lll1l1_opy_(bstack1l1l1ll11l_opy_, bstack1ll1lll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧള"), bstack1ll1lll_opy_ (u"ࠨࡓࡰ࡯ࡨࠤࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡹࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡ࡞ࡱࠦഴ") + str(bstack1111l1lll_opy_))
          bstack111l11l1ll_opy_ = bstack11ll1l111_opy_(bstack11l1111ll_opy_, runner.feature.name, logger)
          if (bstack111l11l1ll_opy_ != None):
            bstack1lll111lll_opy_.append(bstack111l11l1ll_opy_)
      else:
        if runner.driver_initialised in [bstack1ll1lll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣവ"), bstack1ll1lll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧശ")]:
          playwright_annotate(context, bstack1ll1lll_opy_ (u"ࠤࡉࡩࡦࡺࡵࡳࡧ࠽ࠤࠧഷ") + str(runner.feature.name) + bstack1ll1lll_opy_ (u"ࠥࠤࡵࡧࡳࡴࡧࡧࠥࠧസ"), bstack1ll1lll_opy_ (u"ࠦ࡮ࡴࡦࡰࠤഹ"))
          bstack11ll11ll11_opy_(getattr(context, bstack1ll1lll_opy_ (u"ࠬࡶࡡࡨࡧࠪഺ"), None), bstack1ll1lll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ഻"))
          bstack1l1l1ll11l_opy_.execute_script(bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾഼ࠬ") + json.dumps(bstack1ll1lll_opy_ (u"ࠣࡈࡨࡥࡹࡻࡲࡦ࠼ࠣࠦഽ") + str(runner.feature.name) + bstack1ll1lll_opy_ (u"ࠤࠣࡴࡦࡹࡳࡦࡦࠤࠦാ")) + bstack1ll1lll_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩി"))
          bstack1111lll1l1_opy_(bstack1l1l1ll11l_opy_, bstack1ll1lll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫീ"))
          bstack111l11l1ll_opy_ = bstack11ll1l111_opy_(bstack11l1111ll_opy_, runner.feature.name, logger)
          if (bstack111l11l1ll_opy_ != None):
            bstack1lll111lll_opy_.append(bstack111l11l1ll_opy_)
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧു").format(str(e)))
    bstack1l111ll11_opy_(runner, name, context, context.feature, bstack1l1llll111_opy_, *args)
@measure(event_name=EVENTS.bstack1l11lll11l_opy_, stage=STAGE.bstack1ll1llll_opy_, hook_type=bstack1ll1lll_opy_ (u"ࠨࡡࡧࡶࡨࡶࡆࡲ࡬ࠣൂ"), bstack1ll1l11l1l_opy_=SESSION_NAME)
def bstack11llll1ll_opy_(runner, name, context, bstack1l1llll111_opy_, *args):
    bstack1l111ll11_opy_(runner, name, context, runner, bstack1l1llll111_opy_, *args)
def bstack1ll11lll1_opy_(self, filename=None):
  global bstack11l1lllll1_opy_
  bstack11l1lllll1_opy_(self, filename)
  bstack1l11llll11_opy_ = []
  bstack1lll11l1l1_opy_ = [bstack1ll1lll_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠨൃ"), bstack1ll1lll_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡶࡤ࡫ࠬൄ"), bstack1ll1lll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ൅"), bstack1ll1lll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫെ"), bstack1ll1lll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡸࡦ࡭ࠧേ"), bstack1ll1lll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬൈ")]
  bstack1llll11111_opy_ = lambda *_: None
  for hook_name in bstack1lll11l1l1_opy_:
    if hook_name not in self.hooks:
      self.hooks[hook_name] = bstack1llll11111_opy_
      bstack1l11llll11_opy_.append(hook_name)
  if bstack1l11llll11_opy_:
    os.environ[bstack1ll1lll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡓࡅࡍࡢࡈࡊࡌࡁࡖࡎࡗࡣࡍࡕࡏࡌࡕࠪ൉")] = bstack1ll1lll_opy_ (u"ࠧ࠭ࠩൊ").join(bstack1l11llll11_opy_)
def _execute_deferred_playwright_close():
  try:
    _1111l11lll_opy_ = threading.current_thread()
    _1ll11l1lll_opy_ = getattr(_1111l11lll_opy_, bstack1ll1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡦࡨࡪࡪࡸࡲࡦࡦࡢࡴࡦ࡭ࡥࡠࡴࡨࡪࠬോ"), None)
    _1l1l11l1ll_opy_ = getattr(_1111l11lll_opy_, bstack1ll1lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡧࡩ࡫࡫ࡲࡳࡧࡧࡣࡧࡸ࡯ࡸࡵࡨࡶࡤࡸࡥࡧࠩൌ"), None)
    _1ll1lll1l1_opy_ = getattr(_1111l11lll_opy_, bstack1ll1lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡨࡪ࡬ࡥࡳࡴࡨࡨࡤࡶࡷࡠࡵࡷࡳࡵࡥࡦ࡯്ࠩ"), None)
    _wrapper = getattr(_1111l11lll_opy_, bstack1ll1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪൎ"), None)
    if not _1l1l11l1ll_opy_ and _wrapper and hasattr(_wrapper, bstack1ll1lll_opy_ (u"ࠬࡥࡢࡳࡱࡺࡷࡪࡸࠧ൏")):
      _1l1l11l1ll_opy_ = _wrapper._browser
    if not _1ll11l1lll_opy_ and _wrapper and hasattr(_wrapper, bstack1ll1lll_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬ൐")):
      _1ll11l1lll_opy_ = _wrapper._page
    if not _1ll1lll1l1_opy_:
      _11111111l_opy_ = getattr(_1111l11lll_opy_, bstack1ll1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡥࡧࡩࡩࡷࡸࡥࡥࡡࡳࡻࡤࡸࡥࡧࠩ൑"), None)
      if _11111111l_opy_ and hasattr(_11111111l_opy_, bstack1ll1lll_opy_ (u"ࠨࡵࡷࡳࡵ࠭൒")):
        _1ll1lll1l1_opy_ = _11111111l_opy_.stop
    _1l1111l1_opy_ = _1ll11l1lll_opy_ or _1l1l11l1ll_opy_ or _1ll1lll1l1_opy_
    if not _1l1111l1_opy_:
      return
    if _1ll11l1lll_opy_ and hasattr(_1ll11l1lll_opy_, bstack1ll1lll_opy_ (u"ࠩࡦࡰࡴࡹࡥࠨ൓")):
      try:
        _1ll11l1lll_opy_.close(_bstack_sdk_close=True)
      except TypeError:
        try:
          _1ll11l1lll_opy_.close()
        except Exception:
          pass
      except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠪࡈࡪ࡬ࡥࡳࡴࡨࡨࠥࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡳࡥ࡬࡫࠮ࡤ࡮ࡲࡷࡪࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࡼࡿࠪൔ").format(str(e)))
    if _1l1l11l1ll_opy_ and hasattr(_1l1l11l1ll_opy_, bstack1ll1lll_opy_ (u"ࠫࡨࡲ࡯ࡴࡧࠪൕ")):
      try:
        _1l1l11l1ll_opy_.close(_bstack_sdk_close=True)
      except TypeError:
        try:
          _1l1l11l1ll_opy_.close()
        except Exception:
          pass
      except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠬࡊࡥࡧࡧࡵࡶࡪࡪࠠࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡧࡸ࡯ࡸࡵࡨࡶ࠳ࡩ࡬ࡰࡵࡨࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽࠨൖ").format(str(e)))
    if _1ll1lll1l1_opy_:
      try:
        _1ll1lll1l1_opy_(_bstack_sdk_close=True)
      except TypeError:
        try:
          _1ll1lll1l1_opy_()
        except Exception:
          pass
      except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"࠭ࡄࡦࡨࡨࡶࡷ࡫ࡤࠡࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡴࡰࡲࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࢀࢃࠧൗ").format(str(e)))
    for attr in (bstack1ll1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡥࡧࡩࡩࡷࡸࡥࡥࡡࡳࡥ࡬࡫࡟ࡤ࡮ࡲࡷࡪ࠭൘"), bstack1ll1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡦࡨࡪࡪࡸࡲࡦࡦࡢࡴࡦ࡭ࡥࡠࡴࡨࡪࠬ൙"),
                 bstack1ll1lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡧࡩ࡫࡫ࡲࡳࡧࡧࡣࡧࡸ࡯ࡸࡵࡨࡶࡤࡩ࡬ࡰࡵࡨࠫ൚"), bstack1ll1lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡨࡪ࡬ࡥࡳࡴࡨࡨࡤࡨࡲࡰࡹࡶࡩࡷࡥࡲࡦࡨࠪ൛"),
                 bstack1ll1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡩ࡫ࡦࡦࡴࡵࡩࡩࡥࡰࡸࡡࡶࡸࡴࡶࠧ൜"), bstack1ll1lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡪࡥࡧࡧࡵࡶࡪࡪ࡟ࡱࡹࡢࡷࡹࡵࡰࡠࡨࡱࠫ൝"),
                 bstack1ll1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡤࡦࡨࡨࡶࡷ࡫ࡤࡠࡲࡺࡣࡷ࡫ࡦࠨ൞")):
      try:
        delattr(_1111l11lll_opy_, attr)
      except AttributeError:
        pass
    if _wrapper:
      try:
        _wrapper._page = None
        _wrapper._browser = None
      except Exception:
        pass
    logger.debug(bstack1ll1lll_opy_ (u"ࠧࡅࡧࡩࡩࡷࡸࡥࡥࠢࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡣ࡭ࡱࡶࡩࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠡࡨࡲࡶࠥࡺࡨࡳࡧࡤࡨࠥࢁࡽࠨൟ").format(_1111l11lll_opy_.ident))
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠨࡆࡨࡪࡪࡸࡲࡦࡦࠣࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡤ࡮ࡲࡷࡪࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࡼࡿࠪൠ").format(str(e)))
def bstack11l1ll111_opy_(self, name, *args):
  global bstack1l1llll111_opy_
  global bstack1ll111llll_opy_
  try:
    if BROWSERSTACK_AUTOMATION:
      platform_index = int(threading.current_thread()._name) % bstack1ll1ll1111_opy_
      bstack1l1l11ll1_opy_ = CONFIG[bstack1ll1lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬൡ")][platform_index]
      os.environ[bstack1ll1lll_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫൢ")] = json.dumps(bstack1l1l11ll1_opy_)
    if not hasattr(self, bstack1ll1lll_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡥࡥࠩൣ")):
      self.driver_initialised = None
    bstack1l1lll11l_opy_ = {
        bstack1ll1lll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠩ൤"): bstack11lllllll1_opy_,
        bstack1ll1lll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠧ൥"): bstack11ll1ll1l1_opy_,
        bstack1ll1lll_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡵࡣࡪࠫ൦"): bstack11lllll1_opy_,
        bstack1ll1lll_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ൧"): bstack111l111l_opy_,
        bstack1ll1lll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠧ൨"): bstack1l1llll1l_opy_,
        bstack1ll1lll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡸࡪࡶࠧ൩"): bstack1l1l1llll1_opy_,
        bstack1ll1lll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ൪"): bstack1111l1llll_opy_,
        bstack1ll1lll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡹࡧࡧࠨ൫"): bstack1lll1l1ll1_opy_,
        bstack1ll1lll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭൬"): bstack111ll111l1_opy_,
        bstack1ll1lll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪ൭"): bstack11llll1ll_opy_
    }
    handler = bstack1l1lll11l_opy_.get(name, bstack1l1llll111_opy_)
    try:
      if args:
        context = args[0]
        remaining_args = args[1:]
        if bstack1ll111llll_opy_ is None or not bstack1ll111llll_opy_:
          context = self.context
          remaining_args = args
      else:
        context = self.context
        remaining_args = ()
      handler(self, name, context, bstack1l1llll111_opy_, *remaining_args)
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡦࡪ࡮ࡡࡷࡧࠣ࡬ࡴࡵ࡫ࠡࡪࡤࡲࡩࡲࡥࡳࠢࡾࢁ࠿ࠦࡻࡾࠩ൮").format(name, str(e)))
    if name == bstack1ll1lll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ൯"):
      _execute_deferred_playwright_close()
    if name in [bstack1ll1lll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪ൰"), bstack1ll1lll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ൱"), bstack1ll1lll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠨ൲")]:
      try:
        bstack1l1l1ll11l_opy_ = threading.current_thread().bstackSessionDriver if bstack11l11l1l_opy_(bstack1ll1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ൳")) else context.browser
        bstack11l1l1lll_opy_ = (
          (name == bstack1ll1lll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪ൴") and self.driver_initialised == bstack1ll1lll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧ൵")) or
          (name == bstack1ll1lll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠩ൶") and self.driver_initialised == bstack1ll1lll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦ൷")) or
          (name == bstack1ll1lll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ൸") and self.driver_initialised in [bstack1ll1lll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢ൹"), bstack1ll1lll_opy_ (u"ࠨࡩ࡯ࡵࡷࡩࡵࠨൺ")]) or
          (name == bstack1ll1lll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡵࡧࡳࠫൻ") and self.driver_initialised == bstack1ll1lll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨർ"))
        )
        if bstack11l1l1lll_opy_:
          self.driver_initialised = None
          if bstack1l1l1ll11l_opy_ and hasattr(bstack1l1l1ll11l_opy_, bstack1ll1lll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩ࠭ൽ")):
            try:
              bstack1l1l1ll11l_opy_.quit()
            except Exception as e:
              logger.debug(bstack1ll1lll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡴࡹ࡮ࡺࡴࡪࡰࡪࠤࡩࡸࡩࡷࡧࡵࠤ࡮ࡴࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡩࡱࡲ࡯࠿ࠦࡻࡾࠩൾ").format(str(e)))
      except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࠥ࡮࡯ࡰ࡭ࠣࡧࡱ࡫ࡡ࡯ࡷࡳࠤ࡫ࡵࡲࠡࡽࢀ࠾ࠥࢁࡽࠨൿ").format(name, str(e)))
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠬࡉࡲࡪࡶ࡬ࡧࡦࡲࠠࡦࡴࡵࡳࡷࠦࡩ࡯ࠢࡥࡩ࡭ࡧࡶࡦࠢࡵࡹࡳࠦࡨࡰࡱ࡮ࠤࢀࢃ࠺ࠡࡽࢀࠫ඀").format(name, str(e)))
    try:
      if bstack1ll111llll_opy_ is None or bstack1ll111llll_opy_:
        try:
          bstack1l1llll111_opy_(self, name, self.context, *args)
        except TypeError:
          bstack1l1llll111_opy_(self, name, *args)
      else:
        bstack1l1llll111_opy_(self, name, *args)
    except Exception as e2:
      logger.debug(bstack1ll1lll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡨࡤࡰࡱࡨࡡࡤ࡭ࠣࡳࡷ࡯ࡧࡪࡰࡤࡰࠥࡨࡥࡩࡣࡹࡩࠥ࡮࡯ࡰ࡭ࠣࡿࢂࡀࠠࡼࡿࠪඁ").format(name, str(e2)))
  finally:
    if name == bstack1ll1lll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨං"):
      _execute_deferred_playwright_close()
def bstack11l1l11lll_opy_(config, startdir):
  return bstack1ll1lll_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾ࠴ࢂࠨඃ").format(bstack1ll1lll_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣ඄"))
notset = Notset()
def bstack11ll11l11_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1ll1ll1l_opy_
  if str(name).lower() == bstack1ll1lll_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪඅ"):
    return bstack1ll1lll_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥආ")
  else:
    return bstack1ll1ll1l_opy_(self, name, default, skip)
def bstack11ll111l1l_opy_(item, when):
  global bstack111l111111_opy_
  try:
    bstack111l111111_opy_(item, when)
  except Exception as e:
    pass
def bstack1l1l1111_opy_():
  return
def browserstack_executor_helper(type, name, status, reason, bstack11l1lll1l1_opy_, bstack1l11l1ll_opy_):
  bstack111ll1ll1l_opy_ = {
    bstack1ll1lll_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬඇ"): type,
    bstack1ll1lll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩඈ"): {}
  }
  if type == bstack1ll1lll_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩඉ"):
    bstack111ll1ll1l_opy_[bstack1ll1lll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫඊ")][bstack1ll1lll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨඋ")] = bstack11l1lll1l1_opy_
    bstack111ll1ll1l_opy_[bstack1ll1lll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ඌ")][bstack1ll1lll_opy_ (u"ࠫࡩࡧࡴࡢࠩඍ")] = json.dumps(str(bstack1l11l1ll_opy_))
  if type == bstack1ll1lll_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ඎ"):
    bstack111ll1ll1l_opy_[bstack1ll1lll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩඏ")][bstack1ll1lll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬඐ")] = name
  if type == bstack1ll1lll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫඑ"):
    bstack111ll1ll1l_opy_[bstack1ll1lll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬඒ")][bstack1ll1lll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪඓ")] = status
    if status == bstack1ll1lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫඔ"):
      bstack111ll1ll1l_opy_[bstack1ll1lll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨඕ")][bstack1ll1lll_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ඖ")] = json.dumps(str(reason))
  bstack111ll111_opy_ = bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬ඗").format(json.dumps(bstack111ll1ll1l_opy_))
  return bstack111ll111_opy_
def bstack1l11l11l_opy_(driver_command, response):
    if driver_command == bstack1ll1lll_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬ඘"):
        TestHubHandler.bstack11lll1l11l_opy_({
            bstack1ll1lll_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨ඙"): response[bstack1ll1lll_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩක")],
            bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫඛ"): TestHubHandler.current_test_uuid()
        })
def bstack11ll1ll11_opy_(item, call, rep):
  global bstack111ll11lll_opy_
  global bstack1lllllllll_opy_
  global bstack1111111l1_opy_
  name = bstack1ll1lll_opy_ (u"ࠬ࠭ග")
  try:
    if rep.when == bstack1ll1lll_opy_ (u"࠭ࡣࡢ࡮࡯ࠫඝ"):
      bstack1llll1ll1_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1111111l1_opy_:
          name = str(rep.nodeid)
          executor_string = browserstack_executor_helper(bstack1ll1lll_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨඞ"), name, bstack1ll1lll_opy_ (u"ࠨࠩඟ"), bstack1ll1lll_opy_ (u"ࠩࠪච"), bstack1ll1lll_opy_ (u"ࠪࠫඡ"), bstack1ll1lll_opy_ (u"ࠫࠬජ"))
          threading.current_thread().bstack1ll1l11l11_opy_ = name
          for driver in bstack1lllllllll_opy_:
            if bstack1llll1ll1_opy_ == driver.session_id:
              driver.execute_script(executor_string)
      except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬඣ").format(str(e)))
      try:
        bstack1lll11l1_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack1ll1lll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧඤ"):
          status = bstack1ll1lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧඥ") if rep.outcome.lower() == bstack1ll1lll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨඦ") else bstack1ll1lll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩට")
          reason = bstack1ll1lll_opy_ (u"ࠪࠫඨ")
          if status == bstack1ll1lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫඩ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack1ll1lll_opy_ (u"ࠬ࡯࡮ࡧࡱࠪඪ") if status == bstack1ll1lll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ණ") else bstack1ll1lll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ඬ")
          data = name + bstack1ll1lll_opy_ (u"ࠨࠢࡳࡥࡸࡹࡥࡥࠣࠪත") if status == bstack1ll1lll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩථ") else name + bstack1ll1lll_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠥࠥ࠭ද") + reason
          bstack1l1ll1llll_opy_ = browserstack_executor_helper(bstack1ll1lll_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭ධ"), bstack1ll1lll_opy_ (u"ࠬ࠭න"), bstack1ll1lll_opy_ (u"࠭ࠧ඲"), bstack1ll1lll_opy_ (u"ࠧࠨඳ"), level, data)
          for driver in bstack1lllllllll_opy_:
            if bstack1llll1ll1_opy_ == driver.session_id:
              driver.execute_script(bstack1l1ll1llll_opy_)
      except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡩ࡯࡯ࡶࡨࡼࡹࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬප").format(str(e)))
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡴࡢࡶࡨࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿࢂ࠭ඵ").format(str(e)))
  bstack111ll11lll_opy_(item, call, rep)
def bstack1l111l111_opy_(driver, bstack1ll1ll111_opy_, test=None):
  global PLATFORM_INDEX
  if test != None:
    bstack11llll11l_opy_ = getattr(test, bstack1ll1lll_opy_ (u"ࠪࡲࡦࡳࡥࠨබ"), None)
    bstack1l111l1111_opy_ = getattr(test, bstack1ll1lll_opy_ (u"ࠫࡺࡻࡩࡥࠩභ"), None)
    PercySDK.screenshot(driver, bstack1ll1ll111_opy_, bstack11llll11l_opy_=bstack11llll11l_opy_, bstack1l111l1111_opy_=bstack1l111l1111_opy_, bstack1l111l11l1_opy_=PLATFORM_INDEX)
  else:
    PercySDK.screenshot(driver, bstack1ll1ll111_opy_)
@measure(event_name=EVENTS.bstack111l11111l_opy_, stage=STAGE.bstack1ll1llll_opy_, bstack1ll1l11l1l_opy_=SESSION_NAME)
def bstack11lll1lll_opy_(driver):
  if bstack1111l11l_opy_.bstack11ll1l1ll1_opy_() is True or bstack1111l11l_opy_.capturing() is True:
    return
  bstack1111l11l_opy_.bstack1l1ll1ll1_opy_()
  while not bstack1111l11l_opy_.bstack11ll1l1ll1_opy_():
    bstack1ll1llll1_opy_ = bstack1111l11l_opy_.bstack11l111ll1l_opy_()
    bstack1l111l111_opy_(driver, bstack1ll1llll1_opy_)
  bstack1111l11l_opy_.bstack11l1l111l1_opy_()
def bstack1l1111l11l_opy_(sequence, driver_command, response = None, bstack11l1l1l1l_opy_ = None, args = None):
    try:
      if sequence != bstack1ll1lll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬම"):
        return
      if percy.bstack1l1l11ll11_opy_() == bstack1ll1lll_opy_ (u"ࠨࡦࡢ࡮ࡶࡩࠧඹ"):
        return
      bstack1ll1llll1_opy_ = bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪය"), None)
      for command in bstack1ll1l11lll_opy_:
        if command == driver_command:
          with bstack1ll111ll11_opy_:
            bstack1llllll11_opy_ = bstack1lllllllll_opy_.copy()
          for driver in bstack1llllll11_opy_:
            bstack11lll1lll_opy_(driver)
      bstack11ll1l11_opy_ = percy.bstack1lll11ll1l_opy_()
      if driver_command in bstack11ll11lll_opy_[bstack11ll1l11_opy_]:
        bstack1111l11l_opy_.bstack1lll1lll1_opy_(bstack1ll1llll1_opy_, driver_command)
    except Exception as e:
      pass
_11l1ll11l_opy_ = threading.Event()
def bstack1111l1l1l_opy_(framework_name):
  if global_config.get_property(bstack1ll1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬර")):
      _11l1ll11l_opy_.wait(timeout=30)
      return
  global_config.bstack11lll11l11_opy_(bstack1ll1lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡰࡳࡩࡥࡣࡢ࡮࡯ࡩࡩ࠭඼"), True)
  global FRAMEWORK_NAME
  global SELENIUM_OR_PLAYWRIGHT_INSTALLED
  global bstack11l1llll1l_opy_
  FRAMEWORK_NAME = framework_name
  logger.info(bstack1111l1ll1l_opy_.format(FRAMEWORK_NAME.split(bstack1ll1lll_opy_ (u"ࠪ࠱ࠬල"))[0]))
  bstack1llll1ll11_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    global bstack1111l1l1l1_opy_
    bstack1llll11l1l_opy_ = BROWSERSTACK_AUTOMATION or bstack1111l1l1l1_opy_
    if bstack1llll11l1l_opy_:
      Service.start = bstack1111ll1ll1_opy_
      Service.stop = bstack111llll11_opy_
      webdriver.Remote.get = bstack1ll11llll1_opy_
      WebDriver.quit = bstack1ll111l1l_opy_
      webdriver.Remote.__init__ = bstack1l11ll11_opy_
    if not BROWSERSTACK_AUTOMATION and not bstack1111l1l1l1_opy_:
        webdriver.Remote.__init__ = bstack1l1l111lll_opy_
    WebDriver.getAccessibilityResults = getAccessibilityResults
    WebDriver.get_accessibility_results = getAccessibilityResults
    WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
    WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
    WebDriver.performScan = perform_scan
    WebDriver.perform_scan = perform_scan
    WebDriver.execute = bstack11l1l11l1l_opy_
    SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
  except Exception as e:
    pass
  try:
    bstack1llll11l1l_opy_ = BROWSERSTACK_AUTOMATION or bstack1111l1l1l1_opy_
    if bstack1llll11l1l_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack111111llll_opy_
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
    logger.debug(bstack1ll1lll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡩ࡯ࡳࡧࡧ࡬ࡴ࠼ࠣࡿࢂࠨ඾").format(str(e)))
  patch_playwright()
  if not SELENIUM_OR_PLAYWRIGHT_INSTALLED:
    bstack1l1l1ll1ll_opy_(bstack1ll1lll_opy_ (u"ࠧࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠠ࡯ࡱࡷࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪࠢ඿"), bstack1l1ll1ll1l_opy_)
  if bstack1l1ll1lll_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      if hasattr(RemoteConnection, bstack1ll1lll_opy_ (u"࠭࡟ࡨࡧࡷࡣࡵࡸ࡯ࡹࡻࡢࡹࡷࡲࠧව")) and callable(getattr(RemoteConnection, bstack1ll1lll_opy_ (u"ࠧࡠࡩࡨࡸࡤࡶࡲࡰࡺࡼࡣࡺࡸ࡬ࠨශ"))):
        RemoteConnection._get_proxy_url = bstack111llllll1_opy_
      else:
        from selenium.webdriver.remote.client_config import ClientConfig
        ClientConfig.get_proxy_url = bstack111llllll1_opy_
    except Exception as e:
      logger.error(bstack1lll1111l_opy_.format(str(e)))
  if bstack1ll1ll11l1_opy_():
    bstack1ll11ll1l_opy_(CONFIG, logger)
  if (bstack1ll1lll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧෂ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      try:
        from pabot.pabot import QueueItem
        from pabot import pabot
      except Exception as e:
        logger.warning(bstack111l111l1_opy_ + str(e))
      if not is_robot_playwright_installed():
        try:
          if percy.bstack1l1l11ll11_opy_() == bstack1ll1lll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢස"):
            bstack1lll11111_opy_(bstack1l1111l11l_opy_)
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
          WebDriverCreator._get_ff_profile = bstack11llll1l1l_opy_
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
          WebDriverCache.close = bstack1ll11lll_opy_
        except Exception as e:
          logger.warning(bstack1ll111l1l1_opy_ + str(e))
        try:
          from AppiumLibrary.utils.applicationcache import ApplicationCache
          ApplicationCache.close = bstack1lll1l1l11_opy_
        except Exception as e:
          logger.debug(bstack1ll11111l_opy_ + str(e))
    except Exception as e:
      bstack1l1l1ll1ll_opy_(e, bstack1ll111l1l1_opy_)
    Output.start_test = bstack11llllll11_opy_
    Output.end_test = bstack111111ll1l_opy_
    TestStatus.__init__ = bstack1l111l1ll_opy_
    QueueItem.__init__ = bstack11l11l11_opy_
    pabot._create_items = bstack111lll1ll1_opy_
    try:
      from pabot import __version__ as bstack1l1l11l1l1_opy_
      if version.parse(bstack1l1l11l1l1_opy_) >= version.parse(bstack1ll1lll_opy_ (u"ࠪ࠹࠳࠶࠮࠱ࠩහ")):
        pabot._run = bstack111lll1l_opy_
      elif version.parse(bstack1l1l11l1l1_opy_) >= version.parse(bstack1ll1lll_opy_ (u"ࠫ࠹࠴࠲࠯࠲ࠪළ")):
        pabot._run = bstack1ll1ll111l_opy_
      elif version.parse(bstack1l1l11l1l1_opy_) >= version.parse(bstack1ll1lll_opy_ (u"ࠬ࠸࠮࠲࠷࠱࠴ࠬෆ")):
        pabot._run = bstack111l1l11_opy_
      elif version.parse(bstack1l1l11l1l1_opy_) >= version.parse(bstack1ll1lll_opy_ (u"࠭࠲࠯࠳࠶࠲࠵࠭෇")):
        pabot._run = bstack1l1l11111l_opy_
      else:
        pabot._run = bstack1l1ll1l1l1_opy_
    except Exception as e:
      pabot._run = bstack1l1ll1l1l1_opy_
    pabot._create_command_for_execution = bstack1l1ll1l11_opy_
    pabot._report_results = bstack111l1111l_opy_
  if bstack1ll1lll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ෈") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l1l1ll1ll_opy_(e, bstack1l11l1111_opy_)
    Runner.run_hook = bstack11l1ll111_opy_
    try:
      from behave import __version__ as bstack11l1ll1l1l_opy_
      if version.parse(bstack11l1ll1l1l_opy_) >= version.parse(bstack1ll1lll_opy_ (u"ࠨ࠳࠱࠷࠳࠶ࠧ෉")):
        Runner.load_hooks = bstack1ll11lll1_opy_
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"ࠩࡆࡳࡺࡲࡤࠡࡰࡲࡸࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡤࡨ࡬ࡦࡼࡥࠡࡸࡨࡶࡸ࡯࡯࡯࠼ࠣࡿࢂ්࠭").format(str(e)))
    Step.run = bstack1111ll11_opy_
  if bstack1ll1lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ෋") in str(framework_name).lower():
    if not BROWSERSTACK_AUTOMATION:
      _11l1ll11l_opy_.set()
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack11l1l11lll_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1l1l1111_opy_
      Config.getoption = bstack11ll11l11_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack11ll1ll11_opy_
    except Exception as e:
      pass
  _11l1ll11l_opy_.set()
def bstack11lll11ll_opy_():
  global CONFIG
  if bstack1ll1lll_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ෌") in CONFIG and int(CONFIG[bstack1ll1lll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ෍")]) > 1:
    logger.warning(bstack1l11111ll_opy_)
def bstack11l111ll11_opy_(arg, bstack1l1ll111l_opy_, bstack111l1l111_opy_=None):
  global CONFIG
  global bstack1lllll111_opy_
  global bstack1ll1ll1l1_opy_
  global BROWSERSTACK_AUTOMATION
  global bstack1111l1l1l1_opy_
  global global_config
  bstack1lll1l111l_opy_ = bstack1ll1lll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭෎")
  if bstack1l1ll111l_opy_ and isinstance(bstack1l1ll111l_opy_, str):
    bstack1l1ll111l_opy_ = eval(bstack1l1ll111l_opy_)
  CONFIG = bstack1l1ll111l_opy_[bstack1ll1lll_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧා")]
  bstack1lllll111_opy_ = bstack1l1ll111l_opy_[bstack1ll1lll_opy_ (u"ࠨࡊࡘࡆࡤ࡛ࡒࡍࠩැ")]
  bstack1ll1ll1l1_opy_ = bstack1l1ll111l_opy_[bstack1ll1lll_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫෑ")]
  BROWSERSTACK_AUTOMATION = bstack1l1ll111l_opy_[bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭ි")]
  try:
    bstack11111l1lll_opy_ = bstack1l1ll111l_opy_.get(bstack1ll1lll_opy_ (u"ࠫࡔ࡜ࡅࡓࡔࡌࡈࡊࡥࡌࡐࡃࡇࡣ࡙ࡋࡓࡕࡋࡑࡋࠬී"), False)
    bstack1111l1l1l1_opy_ = bool(bstack11111l1lll_opy_)
    os.environ[bstack1ll1lll_opy_ (u"ࠬࡕࡖࡆࡔࡕࡍࡉࡋ࡟ࡍࡑࡄࡈࡤ࡚ࡅࡔࡖࡌࡒࡌ࠭ු")] = str(bstack1111l1l1l1_opy_).lower()
  except Exception as e:
    logger.error(bstack1ll1lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡓ࡛ࡋࡒࡓࡋࡇࡉࡤࡒࡏࡂࡆࡢࡘࡊ࡙ࡔࡊࡐࡊ࠾ࠥࢁࡽࠣ෕").format(e))
    bstack1111l1l1l1_opy_ = False
    os.environ[bstack1ll1lll_opy_ (u"ࠧࡐࡘࡈࡖࡗࡏࡄࡆࡡࡏࡓࡆࡊ࡟ࡕࡇࡖࡘࡎࡔࡇࠨූ")] = bstack1ll1lll_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧ෗")
  global_config.bstack11lll11l11_opy_(bstack1ll1lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪෘ"), BROWSERSTACK_AUTOMATION)
  os.environ[bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬෙ")] = bstack1lll1l111l_opy_
  os.environ[bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠪේ")] = json.dumps(CONFIG)
  os.environ[bstack1ll1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡍ࡛ࡂࡠࡗࡕࡐࠬෛ")] = bstack1lllll111_opy_
  os.environ[bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧො")] = str(bstack1ll1ll1l1_opy_)
  os.environ[bstack1ll1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡍࡗࡊࡍࡓ࠭ෝ")] = str(True)
  if bstack1l1lllllll_opy_(arg, [bstack1ll1lll_opy_ (u"ࠨ࠯ࡱࠫෞ"), bstack1ll1lll_opy_ (u"ࠩ࠰࠱ࡳࡻ࡭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪෟ")]) != -1:
    os.environ[bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡅࡗࡇࡌࡍࡇࡏࠫ෠")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack111l1l11ll_opy_)
    return
  bstack11ll11l1ll_opy_()
  global bstack1111ll11l1_opy_
  global PLATFORM_INDEX
  global bstack11llllll1_opy_
  global bstack1lll111ll_opy_
  global bstack1ll11l11_opy_
  global bstack11l1llll1l_opy_
  global PARALLELISE_VANILLA_PYTHON
  arg.append(bstack1ll1lll_opy_ (u"ࠦ࠲࡝ࠢ෡"))
  arg.append(bstack1ll1lll_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩ࠿ࡓ࡯ࡥࡷ࡯ࡩࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡩ࡮ࡲࡲࡶࡹ࡫ࡤ࠻ࡲࡼࡸࡪࡹࡴ࠯ࡒࡼࡸࡪࡹࡴࡘࡣࡵࡲ࡮ࡴࡧࠣ෢"))
  arg.append(bstack1ll1lll_opy_ (u"ࠨ࠭ࡘࠤ෣"))
  arg.append(bstack1ll1lll_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫࠺ࡕࡪࡨࠤ࡭ࡵ࡯࡬࡫ࡰࡴࡱࠨ෤"))
  global bstack111llll111_opy_
  global bstack1l1lll1111_opy_
  global bstack1ll1l111_opy_
  global bstack11l1ll1l1_opy_
  global bstack11l1l1lll1_opy_
  global bstack1l1ll111l1_opy_
  global bstack1ll1lllll_opy_
  global bstack11111l1111_opy_
  global bstack11l1l11111_opy_
  global bstack1l1l11l11_opy_
  global bstack1ll1ll1l_opy_
  global bstack111l111111_opy_
  global bstack111ll11lll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack111llll111_opy_ = webdriver.Remote.__init__
    bstack1l1lll1111_opy_ = WebDriver.quit
    bstack11111l1111_opy_ = WebDriver.close
    bstack11l1l11111_opy_ = WebDriver.get
    bstack1ll1l111_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1ll1ll11l_opy_(CONFIG) and bstack11llllll_opy_():
    if bstack1l11ll1l1l_opy_() < version.parse(bstack111l1lll_opy_):
      logger.error(bstack111l1l11l_opy_.format(bstack1l11ll1l1l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack1ll1lll_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩ෥")) and callable(getattr(RemoteConnection, bstack1ll1lll_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪ෦"))):
          bstack1l1l11l11_opy_ = RemoteConnection._get_proxy_url
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          bstack1l1l11l11_opy_ = ClientConfig.get_proxy_url
      except Exception as e:
        logger.error(bstack1lll1111l_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1ll1ll1l_opy_ = Config.getoption
    from _pytest import runner
    bstack111l111111_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warning(bstack1ll1lll_opy_ (u"ࠥࠩࡸࡀࠠࠦࡵࠥ෧"), bstack111l1ll1l1_opy_, str(e))
  try:
    from pytest_bdd import reporting
    bstack111ll11lll_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack1ll1lll_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡳࠥࡸࡵ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࡷࠬ෨"))
  if cli.is_enabled(CONFIG) and cli.config:
    bstack11llllll1_opy_ = cli.config.get(bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ෩"), {}).get(bstack1ll1lll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ෪"))
  else:
    bstack11llllll1_opy_ = CONFIG.get(bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ෫"), {}).get(bstack1ll1lll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ෬"))
  PARALLELISE_VANILLA_PYTHON = True
  if cli.is_enabled(CONFIG):
    if cli.bstack111llllll_opy_():
      bstack1l111111ll_opy_.invoke(Events.CONNECT, bstack11lll111_opy_())
    platform_index = int(os.environ.get(bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ෭"), bstack1ll1lll_opy_ (u"ࠪ࠴ࠬ෮")))
  else:
    bstack1111l1l1l_opy_(bstack1lll1l1111_opy_)
  os.environ[bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬ෯")] = CONFIG[bstack1ll1lll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ෰")]
  os.environ[bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩ෱")] = CONFIG[bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪෲ")]
  os.environ[bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫෳ")] = BROWSERSTACK_AUTOMATION.__str__()
  from _pytest.config import main as bstack1l11l1llll_opy_
  bstack1ll1lll11_opy_ = []
  try:
    exit_code = bstack1l11l1llll_opy_(arg)
    if cli.is_enabled(CONFIG):
      cli.bstack111ll1ll1_opy_()
    if bstack1ll1lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠭෴") in multiprocessing.current_process().__dict__.keys():
      for bstack11l1l1l1ll_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1ll1lll11_opy_.append(bstack11l1l1l1ll_opy_)
    try:
      bstack1l111l111l_opy_ = (bstack1ll1lll11_opy_, int(exit_code))
      bstack111l1l111_opy_.append(bstack1l111l111l_opy_)
    except:
      bstack111l1l111_opy_.append((bstack1ll1lll11_opy_, exit_code))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack1ll1lll11_opy_.append({bstack1ll1lll_opy_ (u"ࠪࡲࡦࡳࡥࠨ෵"): bstack1ll1lll_opy_ (u"ࠫࡕࡸ࡯ࡤࡧࡶࡷࠥ࠭෶") + os.environ.get(bstack1ll1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ෷")), bstack1ll1lll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ෸"): traceback.format_exc(), bstack1ll1lll_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭෹"): int(os.environ.get(bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ෺")))})
    bstack111l1l111_opy_.append((bstack1ll1lll11_opy_, 1))
def mod_behave_main(args, retries):
  try:
    from behave.configuration import Configuration
    from behave.__main__ import run_behave
    from browserstack_sdk.bstack_behave_runner import BehaveRunner
    config = Configuration(args)
    config.update_userdata({bstack1ll1lll_opy_ (u"ࠤࡵࡩࡹࡸࡩࡦࡵࠥ෻"): str(retries)})
    return run_behave(config, runner_class=BehaveRunner)
  except Exception as e:
    bstack1l111ll1l1_opy_ = e.__class__.__name__
    print(bstack1ll1lll_opy_ (u"ࠥࠩࡸࡀࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡵࡧࡶࡸࠥࠫࡳࠣ෼") % (bstack1l111ll1l1_opy_, e))
    return 1
def bstack1111ll1l_opy_(arg):
  global bstack1l11ll1ll_opy_
  bstack1111l1l1l_opy_(bstack111l11ll1l_opy_)
  os.environ[bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ෽")] = str(bstack1ll1ll1l1_opy_)
  retries = bstack1l11ll1ll1_opy_.bstack1ll111l1_opy_(CONFIG)
  status_code = 0
  if bstack1l11ll1ll1_opy_.bstack1llll1lll1_opy_(CONFIG):
    status_code = mod_behave_main(arg, retries)
  else:
    from behave.__main__ import main as bstack1ll1l11ll1_opy_
    status_code = bstack1ll1l11ll1_opy_(arg)
  if status_code != 0:
    bstack1l11ll1ll_opy_ = status_code
def bstack11l1l111ll_opy_():
  logger.info(bstack11l1lll11_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1ll1lll_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ෾"), help=bstack1ll1lll_opy_ (u"࠭ࡇࡦࡰࡨࡶࡦࡺࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡤࡱࡱࡪ࡮࡭ࠧ෿"))
  parser.add_argument(bstack1ll1lll_opy_ (u"ࠧ࠮ࡷࠪ฀"), bstack1ll1lll_opy_ (u"ࠨ࠯࠰ࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬก"), help=bstack1ll1lll_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡵࡴࡧࡵࡲࡦࡳࡥࠨข"))
  parser.add_argument(bstack1ll1lll_opy_ (u"ࠪ࠱ࡰ࠭ฃ"), bstack1ll1lll_opy_ (u"ࠫ࠲࠳࡫ࡦࡻࠪค"), help=bstack1ll1lll_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡤࡧࡨ࡫ࡳࡴࠢ࡮ࡩࡾ࠭ฅ"))
  parser.add_argument(bstack1ll1lll_opy_ (u"࠭࠭ࡧࠩฆ"), bstack1ll1lll_opy_ (u"ࠧ࠮࠯ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬง"), help=bstack1ll1lll_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧจ"))
  bstack1111l11l1_opy_ = parser.parse_args()
  try:
    bstack1l11l111l_opy_ = bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡩࡨࡲࡪࡸࡩࡤ࠰ࡼࡱࡱ࠴ࡳࡢ࡯ࡳࡰࡪ࠭ฉ")
    if bstack1111l11l1_opy_.framework and bstack1111l11l1_opy_.framework not in (bstack1ll1lll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪช"), bstack1ll1lll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬซ")):
      bstack1l11l111l_opy_ = bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠮ࡺ࡯࡯࠲ࡸࡧ࡭ࡱ࡮ࡨࠫฌ")
    bstack11l1lll1l_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l11l111l_opy_)
    bstack11ll11l111_opy_ = open(bstack11l1lll1l_opy_, bstack1ll1lll_opy_ (u"࠭ࡲࠨญ"))
    bstack1llll1l1l_opy_ = bstack11ll11l111_opy_.read()
    bstack11ll11l111_opy_.close()
    if bstack1111l11l1_opy_.username:
      bstack1llll1l1l_opy_ = bstack1llll1l1l_opy_.replace(bstack1ll1lll_opy_ (u"࡚ࠧࡑࡘࡖࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧฎ"), bstack1111l11l1_opy_.username)
    if bstack1111l11l1_opy_.key:
      bstack1llll1l1l_opy_ = bstack1llll1l1l_opy_.replace(bstack1ll1lll_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪฏ"), bstack1111l11l1_opy_.key)
    if bstack1111l11l1_opy_.framework:
      bstack1llll1l1l_opy_ = bstack1llll1l1l_opy_.replace(bstack1ll1lll_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪฐ"), bstack1111l11l1_opy_.framework)
    file_name = bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ฑ")
    file_path = os.path.abspath(file_name)
    bstack1111l111ll_opy_ = open(file_path, bstack1ll1lll_opy_ (u"ࠫࡼ࠭ฒ"))
    bstack1111l111ll_opy_.write(bstack1llll1l1l_opy_)
    bstack1111l111ll_opy_.close()
    logger.info(bstack1l11l111ll_opy_)
    try:
      os.environ[bstack1ll1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧณ")] = bstack1111l11l1_opy_.framework if bstack1111l11l1_opy_.framework != None else bstack1ll1lll_opy_ (u"ࠨࠢด")
      config = yaml.safe_load(bstack1llll1l1l_opy_)
      config[bstack1ll1lll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧต")] = bstack1ll1lll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡵࡨࡸࡺࡶࠧถ")
      bstack111l1l1l1l_opy_(bstack1lll11l11_opy_, config)
    except Exception as e:
      logger.debug(bstack1l11l1l11_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack111l11l111_opy_.format(str(e)))
def bstack111l1l1l1l_opy_(bstack111111ll11_opy_, config, bstack11ll1l1l1_opy_=None, bstack1lllll11_opy_=False):
  global BROWSERSTACK_AUTOMATION
  global bstack11111lllll_opy_
  global global_config
  if not config:
    return
  if bstack11ll1l1l1_opy_ is None:
    bstack11ll1l1l1_opy_ = {}
  bstack1l1ll1l1_opy_ = bstack1ll111l11_opy_ if not BROWSERSTACK_AUTOMATION else (
    bstack111lllll1l_opy_ if bstack1ll1lll_opy_ (u"ࠩࡤࡴࡵ࠭ท") in config else (
        bstack1l11l1l1l_opy_ if config.get(bstack1ll1lll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧธ")) else bstack1l1l1l1l_opy_
    )
)
  bstack1ll11111l1_opy_ = False
  bstack1l1111ll1l_opy_ = False
  if BROWSERSTACK_AUTOMATION is True:
      if bstack1ll1lll_opy_ (u"ࠫࡦࡶࡰࠨน") in config:
          bstack1ll11111l1_opy_ = True
      else:
          bstack1l1111ll1l_opy_ = True
  bstack11l11l111l_opy_ = TestHubUtils.bstack11ll111ll1_opy_(config, bstack11111lllll_opy_)
  bstack11ll1lll1l_opy_ = bstack1l1l1l11l_opy_()
  data = {
    bstack1ll1lll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧบ"): config[bstack1ll1lll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨป")],
    bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪผ"): config[bstack1ll1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫฝ")],
    bstack1ll1lll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭พ"): bstack111111ll11_opy_,
    bstack1ll1lll_opy_ (u"ࠪࡨࡪࡺࡥࡤࡶࡨࡨࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧฟ"): os.environ.get(bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ภ"), bstack11111lllll_opy_),
    bstack1ll1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧม"): bstack1ll111l11l_opy_,
    bstack1ll1lll_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬ࠨย"): bstack1l111lllll_opy_(),
    bstack1ll1lll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪร"): {
      bstack1ll1lll_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ฤ"): str(config[bstack1ll1lll_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩล")]) if bstack1ll1lll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪฦ") in config else bstack1ll1lll_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧว"),
      bstack1ll1lll_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࡖࡦࡴࡶ࡭ࡴࡴࠧศ"): sys.version,
      bstack1ll1lll_opy_ (u"࠭ࡲࡦࡨࡨࡶࡷ࡫ࡲࠨษ"): bstack1l1l111111_opy_(os.environ.get(bstack1ll1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩส"), bstack11111lllll_opy_)),
      bstack1ll1lll_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪห"): bstack1ll1lll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩฬ"),
      bstack1ll1lll_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫอ"): bstack1l1ll1l1_opy_,
      bstack1ll1lll_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩฮ"): bstack11l11l111l_opy_,
      bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡥࡵࡶ࡫ࡧࠫฯ"): os.environ[bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫะ")],
      bstack1ll1lll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪั"): os.environ.get(bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪา"), bstack11111lllll_opy_),
      bstack1ll1lll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬำ"): bstack11l1llll11_opy_(os.environ.get(bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬิ"), bstack11111lllll_opy_)),
      bstack1ll1lll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪี"): bstack11ll1lll1l_opy_.get(bstack1ll1lll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪึ")),
      bstack1ll1lll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬื"): bstack11ll1lll1l_opy_.get(bstack1ll1lll_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨุ")),
      bstack1ll1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨูࠫ"): config[bstack1ll1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩฺࠬ")] if config[bstack1ll1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭฻")] else bstack1ll1lll_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧ฼"),
      bstack1ll1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ฽"): str(config[bstack1ll1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ฾")]) if bstack1ll1lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ฿") in config else bstack1ll1lll_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤเ"),
      bstack1ll1lll_opy_ (u"ࠩࡲࡷࠬแ"): sys.platform,
      bstack1ll1lll_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬโ"): socket.gethostname(),
      bstack1ll1lll_opy_ (u"ࠫ࡮ࡹࡃࡍࡋࡈࡲࡦࡨ࡬ࡦࡦࠪใ"): bstack1lllll11_opy_,
      bstack1ll1lll_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪࠧไ"): global_config.get_property(bstack1ll1lll_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨๅ"))
    }
  }
  if not global_config.get_property(bstack1ll1lll_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡔ࡫ࡪࡲࡦࡲࠧๆ")) is None:
    data[bstack1ll1lll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫ็")][bstack1ll1lll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡑࡪࡺࡡࡥࡣࡷࡥ่ࠬ")] = {
      bstack1ll1lll_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰ้ࠪ"): bstack1ll1lll_opy_ (u"ࠫࡺࡹࡥࡳࡡ࡮࡭ࡱࡲࡥࡥ๊ࠩ"),
      bstack1ll1lll_opy_ (u"ࠬࡹࡩࡨࡰࡤࡰ๋ࠬ"): global_config.get_property(bstack1ll1lll_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭์")),
      bstack1ll1lll_opy_ (u"ࠧࡴ࡫ࡪࡲࡦࡲࡎࡶ࡯ࡥࡩࡷ࠭ํ"): global_config.get_property(bstack1ll1lll_opy_ (u"ࠨࡵࡧ࡯ࡐ࡯࡬࡭ࡐࡲࠫ๎"))
    }
  if bstack111111ll11_opy_ == bstack1ll1l1l111_opy_:
    data[bstack1ll1lll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬ๏")][bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡅࡲࡲ࡫࡯ࡧࠨ๐")] = bstack11l111l1_opy_(config)
    data[bstack1ll1lll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧ๑")][bstack1ll1lll_opy_ (u"ࠬ࡯ࡳࡑࡧࡵࡧࡾࡇࡵࡵࡱࡈࡲࡦࡨ࡬ࡦࡦࠪ๒")] = percy.bstack1llll1llll_opy_
    data[bstack1ll1lll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩ๓")][bstack1ll1lll_opy_ (u"ࠧࡱࡧࡵࡧࡾࡈࡵࡪ࡮ࡧࡍࡩ࠭๔")] = percy.percy_build_id
  if not bstack1l11ll1ll1_opy_.bstack1lllll11l1_opy_(CONFIG):
    data[bstack1ll1lll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫ๕")][bstack1ll1lll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠭๖")] = bstack1l11ll1ll1_opy_.bstack1lllll11l1_opy_(CONFIG)
  bstack1l1l111l1l_opy_ = bstack1111ll11ll_opy_.get_instance(CONFIG, logger)
  bstack1lll11llll_opy_ = bstack1l11ll1ll1_opy_.get_instance(config=CONFIG)
  if bstack1l1l111l1l_opy_ is not None and bstack1lll11llll_opy_ is not None and bstack1lll11llll_opy_.bstack1l11lll11_opy_():
    data[bstack1ll1lll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭๗")][bstack1lll11llll_opy_.bstack1111llll_opy_()] = bstack1l1l111l1l_opy_.bstack1llll111l1_opy_()
  update(data[bstack1ll1lll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧ๘")], bstack11ll1l1l1_opy_)
  try:
    response = bstack111l1l111l_opy_(bstack1ll1lll_opy_ (u"ࠬࡖࡏࡔࡖࠪ๙"), bstack11l1l1111_opy_(bstack1111ll111_opy_), data, {
      bstack1ll1lll_opy_ (u"࠭ࡡࡶࡶ࡫ࠫ๚"): (config[bstack1ll1lll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ๛")], config[bstack1ll1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ๜")])
    })
    if response:
      logger.debug(bstack1ll11ll1ll_opy_.format(bstack111111ll11_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1lllll1l1_opy_.format(str(e)))
def bstack1l1l111111_opy_(framework):
  return bstack1ll1lll_opy_ (u"ࠤࡾࢁ࠲ࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࡿࢂࠨ๝").format(str(framework), __version__) if framework else bstack1ll1lll_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࡽࢀࠦ๞").format(
    __version__)
def bstack11ll11l1ll_opy_():
  global CONFIG
  global bstack1l1ll1l111_opy_
  if bool(CONFIG):
    return
  try:
    bstack11ll1ll1ll_opy_()
    logger.debug(bstack1ll11l11l_opy_.format(str(CONFIG)))
    bstack1l1ll1l111_opy_ = logger_utils.configure_logger(CONFIG, bstack1l1ll1l111_opy_)
    bstack1llll1ll11_opy_()
  except Exception as e:
    logger.error(bstack1ll1lll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࡹࡵ࠲ࠠࡦࡴࡵࡳࡷࡀࠠࠣ๟") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1llllll111_opy_
  atexit.register(bstack111ll1l11l_opy_)
  signal.signal(signal.SIGINT, bstack111l11lll_opy_)
  signal.signal(signal.SIGTERM, bstack111l11lll_opy_)
def bstack1llllll111_opy_(exctype, value, traceback):
  global bstack1lllllllll_opy_
  try:
    for driver in bstack1lllllllll_opy_:
      bstack1111lll1l1_opy_(driver, bstack1ll1lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ๠"), bstack1ll1lll_opy_ (u"ࠨࡓࡦࡵࡶ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤ๡") + str(value))
  except Exception:
    pass
  logger.info(bstack111l1lll1l_opy_)
  bstack1l1lll11ll_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1l1lll11ll_opy_(message=bstack1ll1lll_opy_ (u"ࠧࠨ๢"), bstack1111ll1111_opy_ = False, bstack1lllll11_opy_ = False):
  global CONFIG
  bstack11l1ll1ll1_opy_ = bstack1ll1lll_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡆࡺࡦࡩࡵࡺࡩࡰࡰࠪ๣") if bstack1111ll1111_opy_ else bstack1ll1lll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ๤")
  bstack1l1l111l_opy_ = bstack1lll1lll11_opy_.bstack11l1llllll_opy_(EVENTS.bstack1ll1l11l_opy_)
  try:
    if message:
      bstack11ll1l1l1_opy_ = {
        bstack11l1ll1ll1_opy_ : str(message)
      }
      try:
        bstack111l1l1l1l_opy_(bstack1ll1l1l111_opy_, CONFIG, bstack11ll1l1l1_opy_, bstack1lllll11_opy_)
      finally:
        bstack1lll1lll11_opy_.end(EVENTS.bstack1ll1l11l_opy_.value, bstack1l1l111l_opy_ + bstack1ll1lll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ๥"), bstack1l1l111l_opy_ + bstack1ll1lll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ๦"), status=True, failure=None, test_name=None)
    else:
      try:
        bstack111l1l1l1l_opy_(bstack1ll1l1l111_opy_, CONFIG, bstack1lllll11_opy_=bstack1lllll11_opy_)
      finally:
        bstack1lll1lll11_opy_.end(EVENTS.bstack1ll1l11l_opy_.value, bstack1l1l111l_opy_ + bstack1ll1lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ๧"), bstack1l1l111l_opy_ + bstack1ll1lll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ๨"), status=True, failure=None, test_name=None)
  except Exception as e:
    logger.debug(bstack11l1lllll_opy_.format(str(e)))
def bstack1l11l1lll1_opy_(bstack1111llll11_opy_, size):
  bstack11lll11l_opy_ = []
  while len(bstack1111llll11_opy_) > size:
    bstack11ll1llll_opy_ = bstack1111llll11_opy_[:size]
    bstack11lll11l_opy_.append(bstack11ll1llll_opy_)
    bstack1111llll11_opy_ = bstack1111llll11_opy_[size:]
  bstack11lll11l_opy_.append(bstack1111llll11_opy_)
  return bstack11lll11l_opy_
def bstack111111l1ll_opy_(args):
  if bstack1ll1lll_opy_ (u"ࠧ࠮࡯ࠪ๩") in args and bstack1ll1lll_opy_ (u"ࠨࡲࡧࡦࠬ๪") in args:
    return True
  return False
@measure(event_name=EVENTS.bstack111lll1l11_opy_, stage=STAGE.bstack11l11l1l1_opy_)
def run_on_browserstack(bstack11l1lll111_opy_=None, bstack111l1l111_opy_=None, bstack1l11ll1l_opy_=False):
  global CONFIG
  global bstack1lllll111_opy_
  global bstack1ll1ll1l1_opy_
  global bstack11111lllll_opy_
  global global_config
  bstack1lll1l111l_opy_ = bstack1ll1lll_opy_ (u"ࠩࠪ๫")
  bstack111ll1lll1_opy_ = bstack1ll1lll_opy_ (u"ࠥࠦ๬")
  bstack1l11l1l1l1_opy_(bstack111l11ll1_opy_, logger)
  if bstack11l1lll111_opy_ and isinstance(bstack11l1lll111_opy_, str):
    bstack11l1lll111_opy_ = eval(bstack11l1lll111_opy_)
  if bstack11l1lll111_opy_:
    CONFIG = bstack11l1lll111_opy_[bstack1ll1lll_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫ๭")]
    bstack1lllll111_opy_ = bstack11l1lll111_opy_[bstack1ll1lll_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭๮")]
    bstack1ll1ll1l1_opy_ = bstack11l1lll111_opy_[bstack1ll1lll_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ๯")]
    global_config.bstack11lll11l11_opy_(bstack1ll1lll_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ๰"), bstack1ll1ll1l1_opy_)
    bstack1lll1l111l_opy_ = bstack1ll1lll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩ๱")
  global_config.bstack11lll11l11_opy_(bstack1ll1lll_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫ๲"), uuid4().__str__())
  logger.info(bstack1ll1lll_opy_ (u"ࠪࡗࡉࡑࠠࡳࡷࡱࠤࡸࡺࡡࡳࡶࡨࡨࠥࡽࡩࡵࡪࠣ࡭ࡩࡀࠠࠨ๳") + global_config.get_property(bstack1ll1lll_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭๴")));
  logger.debug(bstack1ll1lll_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪ࠽ࠨ๵") + global_config.get_property(bstack1ll1lll_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨ๶")))
  if not bstack1l11ll1l_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack111l1l11ll_opy_)
      return
    if sys.argv[1] == bstack1ll1lll_opy_ (u"ࠧ࠮࠯ࡹࡩࡷࡹࡩࡰࡰࠪ๷") or sys.argv[1] == bstack1ll1lll_opy_ (u"ࠨ࠯ࡹࠫ๸"):
      logger.info(bstack1ll1lll_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡒࡼࡸ࡭ࡵ࡮ࠡࡕࡇࡏࠥࡼࡻࡾࠩ๹").format(__version__))
      return
    if sys.argv[1] == bstack1ll1lll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ๺"):
      bstack11l1l111ll_opy_()
      return
    if sys.argv[1] == bstack1ll1lll_opy_ (u"ࠫࡱࡵࡡࡥࠩ๻"):
      from browserstack_sdk.bstack11l11l1l1l_opy_ import bstack1l1l1l111l_opy_
      bstack11ll11l1ll_opy_()
      bstack1l1l1l111l_opy_(CONFIG)
      return
  args = sys.argv
  bstack11ll11l1ll_opy_()
  global bstack1111l1l1l1_opy_
  try:
    from bstack_utils import constants as bstack11111ll11l_opy_
    override_value = CONFIG.get(bstack1ll1lll_opy_ (u"ࠬࡵࡶࡦࡴࡵ࡭ࡩ࡫ࡌࡰࡣࡧࡘࡪࡹࡴࡪࡰࡪࠫ๼"), False)
    bstack1111l1l1l1_opy_ = bool(override_value)
  except Exception as e:
    logger.error(bstack1ll1lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡓ࡛ࡋࡒࡓࡋࡇࡉࡤࡒࡏࡂࡆࡢࡘࡊ࡙ࡔࡊࡐࡊ࠾ࠥࢁࡽࠣ๽").format(e))
    bstack1111l1l1l1_opy_ = False
  if bstack1111l1l1l1_opy_:
    bstack11l1l1l11l_opy_ = CONFIG.get(bstack1ll1lll_opy_ (u"ࠧ࡭ࡱࡤࡨ࡙࡫ࡳࡵ࡫ࡱ࡫ࡍࡻࡢࡖࡔࡏࠫ๾")) or bstack11111ll11l_opy_.bstack111l11l1l1_opy_
    logger.info(bstack1ll1lll_opy_ (u"ࠣࡉ࡯ࡳࡧࡧ࡬ࠡࡱࡹࡩࡷࡸࡩࡥࡧ࡯ࡳࡦࡪࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡦࡰࡤࡦࡱ࡫ࡤ࠭ࠢࡸࡷ࡮ࡴࡧࠡࡪࡸࡦ࠿ࠦࡻࡾࠤ๿").format(bstack11l1l1l11l_opy_))
    bstack1lllll111_opy_ = bstack11l1l1l11l_opy_
    try:
      bstack11111ll11l_opy_.HTTPS_HUB = bstack11l1l1l11l_opy_
      bstack11111ll11l_opy_.bstack1l1l11l111_opy_ = bstack11l1l1l11l_opy_
    except Exception:
      pass
  global bstack1111ll11l1_opy_
  global bstack1ll1ll1111_opy_
  global PARALLELISE_VANILLA_PYTHON
  global PARALLELISE_THREADING_PYTHON
  global PLATFORM_INDEX
  global bstack11llllll1_opy_
  global bstack1lll111ll_opy_
  global bstack111l11llll_opy_
  global bstack1ll11l11_opy_
  global bstack11l1llll1l_opy_
  global bstack11111lll_opy_
  bstack1ll1ll1111_opy_ = len(CONFIG.get(bstack1ll1lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ຀"), []))
  if not bstack1lll1l111l_opy_:
    if args[1] == bstack1ll1lll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪກ") or args[1] == bstack1ll1lll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬຂ") or args[1] == bstack1ll1lll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨ࠭຃"):
      bstack1lll1l111l_opy_ = bstack1ll1lll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡧࡦࡰࡨࡶ࡮ࡩࠧຄ")
      args = args[2:]
    elif args[1] == bstack1ll1lll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭຅"):
      bstack1lll1l111l_opy_ = bstack1ll1lll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧຆ")
      args = args[2:]
    elif args[1] == bstack1ll1lll_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨງ"):
      bstack1lll1l111l_opy_ = bstack1ll1lll_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩຈ")
      args = args[2:]
    elif args[1] == bstack1ll1lll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬຉ"):
      bstack1lll1l111l_opy_ = bstack1ll1lll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ຊ")
      args = args[2:]
    elif args[1] == bstack1ll1lll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭຋"):
      bstack1lll1l111l_opy_ = bstack1ll1lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧຌ")
      args = args[2:]
    elif args[1] == bstack1ll1lll_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨຍ"):
      bstack1lll1l111l_opy_ = bstack1ll1lll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩຎ")
      args = args[2:]
    else:
      if not bstack1ll1lll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ຏ") in CONFIG or str(CONFIG[bstack1ll1lll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧຐ")]).lower() in [bstack1ll1lll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬຑ"), bstack1ll1lll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧຒ"), bstack1ll1lll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡨࡧࡱࡩࡷ࡯ࡣࠨຓ")]:
        bstack1lll1l111l_opy_ = bstack1ll1lll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩດ")
        args = args[1:]
      elif str(CONFIG[bstack1ll1lll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬຕ")]).lower() == bstack1ll1lll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩຖ"):
        bstack1lll1l111l_opy_ = bstack1ll1lll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪທ")
        args = args[1:]
      elif str(CONFIG[bstack1ll1lll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨຘ")]).lower() == bstack1ll1lll_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬນ"):
        bstack1lll1l111l_opy_ = bstack1ll1lll_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ບ")
        args = args[1:]
      elif str(CONFIG[bstack1ll1lll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫປ")]).lower() == bstack1ll1lll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩຜ"):
        bstack1lll1l111l_opy_ = bstack1ll1lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪຝ")
        args = args[1:]
      elif str(CONFIG[bstack1ll1lll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧພ")]).lower() == bstack1ll1lll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬຟ"):
        bstack1lll1l111l_opy_ = bstack1ll1lll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ຠ")
        args = args[1:]
      else:
        os.environ[bstack1ll1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩມ")] = bstack1lll1l111l_opy_
        bstack1l1111ll_opy_(bstack11111l111_opy_)
  os.environ[bstack1ll1lll_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩຢ")] = bstack1lll1l111l_opy_
  bstack11111lllll_opy_ = bstack1lll1l111l_opy_
  if cli.is_enabled(CONFIG):
    try:
      if bstack1lll1l111l_opy_ == bstack1ll1lll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩຣ") and bstack1l11ll1lll_opy_():
        bstack1l1ll11111_opy_ = bstack111l111lll_opy_[bstack1ll1lll_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖ࠰ࡆࡉࡊࠧ຤")]
      elif bstack1lll1l111l_opy_ in [bstack1ll1lll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬລ"), bstack1ll1lll_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ຦")]:
        bstack1l1ll11111_opy_ = bstack1ll1lll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬວ")
      else:
        bstack1l1ll11111_opy_ = bstack1lll1l111l_opy_
      bstack1l111111ll_opy_.invoke(Events.bstack1lll11l11l_opy_, bstack1111lll11l_opy_(
        sdk_version=__version__,
        path_config=bstack1l111l1lll_opy_(),
        path_project=os.getcwd(),
        test_framework=bstack1l1ll11111_opy_,
        frameworks=[bstack1l1ll11111_opy_],
        framework_versions={
          bstack1l1ll11111_opy_: bstack11l1llll11_opy_(bstack1ll1lll_opy_ (u"ࠧࡓࡱࡥࡳࡹ࠭ຨ") if bstack1lll1l111l_opy_ in [bstack1ll1lll_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧຩ"), bstack1ll1lll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨສ"), bstack1ll1lll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫຫ")] else bstack1lll1l111l_opy_)
        },
        bs_config=CONFIG
      ))
      if cli.config and cli.config.get(bstack1ll1lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࠨຬ"), None):
        CONFIG[bstack1ll1lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠢອ")] = cli.config.get(bstack1ll1lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣຮ"), None)
    except Exception as e:
      bstack1l111111ll_opy_.invoke(Events.bstack111l1l1111_opy_, e.__traceback__, 1)
    if bstack1ll1ll1l1_opy_:
      CONFIG[bstack1ll1lll_opy_ (u"ࠢࡢࡲࡳࠦຯ")] = cli.config[bstack1ll1lll_opy_ (u"ࠣࡣࡳࡴࠧະ")]
      logger.info(bstack1lllll1ll_opy_.format(CONFIG[bstack1ll1lll_opy_ (u"ࠩࡤࡴࡵ࠭ັ")]))
  else:
    bstack1l111111ll_opy_.clear()
  global bstack111l111l11_opy_
  global bstack11lll1ll1l_opy_
  if bstack11l1lll111_opy_:
    try:
      bstack1ll1l111l_opy_ = datetime.datetime.now()
      os.environ[bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬາ")] = bstack1lll1l111l_opy_
      bstack11llllllll_opy_ = bstack1lll1lll11_opy_.bstack11l1llllll_opy_(EVENTS.bstack1l1lll11l1_opy_)
      try:
        logger.info(bstack1ll1lll_opy_ (u"ࠦࡘ࡫࡮ࡥ࡫ࡱ࡫࡙ࠥࡄࡌࠢࡗࡩࡸࡺࠠࡂࡶࡷࡩࡲࡶࡴࡦࡦࠣࡩࡻ࡫࡮ࡵࠤຳ"))
        bstack111l1l1l1l_opy_(bstack11111111_opy_, CONFIG)
      finally:
        bstack1lll1lll11_opy_.end(EVENTS.bstack1l1lll11l1_opy_.value, bstack11llllllll_opy_ + bstack1ll1lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧິ"), bstack11llllllll_opy_ + bstack1ll1lll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦີ"), status=True, failure=None, test_name=None)
      cli.bstack1111lll11_opy_(bstack1ll1lll_opy_ (u"ࠢࡩࡶࡷࡴ࠿ࡹࡤ࡬ࡡࡷࡩࡸࡺ࡟ࡢࡶࡷࡩࡲࡶࡴࡦࡦࠥຶ"), datetime.datetime.now() - bstack1ll1l111l_opy_)
    except Exception as e:
      logger.debug(bstack1ll1ll1ll1_opy_.format(str(e)))
  global bstack111llll111_opy_
  global bstack1l1lll1111_opy_
  global bstack11ll111ll_opy_
  global bstack11lll1lll1_opy_
  global bstack1l111ll1l_opy_
  global bstack1llllll1l_opy_
  global bstack11l1ll1l1_opy_
  global bstack11l1l1lll1_opy_
  global bstack1ll1111ll_opy_
  global bstack1l1ll111l1_opy_
  global bstack1ll1lllll_opy_
  global bstack11111l1111_opy_
  global bstack1l1llll111_opy_
  global bstack11l1lllll1_opy_
  global bstack11lll1l1_opy_
  global bstack11l1l11111_opy_
  global bstack1l1l11l11_opy_
  global bstack1ll1ll1l_opy_
  global bstack111l111111_opy_
  global bstack111lllll1_opy_
  global bstack111ll11lll_opy_
  global bstack1ll1l111_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack111llll111_opy_ = webdriver.Remote.__init__
    bstack1l1lll1111_opy_ = WebDriver.quit
    bstack11111l1111_opy_ = WebDriver.close
    bstack11l1l11111_opy_ = WebDriver.get
    bstack1ll1l111_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack111l111l11_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack11l1lll1ll_opy_
    bstack11lll1ll1l_opy_ = bstack11l1lll1ll_opy_()
  except Exception as e:
    pass
  try:
    global bstack1l1l11l11l_opy_
    from QWeb.keywords import browser
    bstack1l1l11l11l_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1ll1ll11l_opy_(CONFIG) and bstack11llllll_opy_():
    if bstack1l11ll1l1l_opy_() < version.parse(bstack111l1lll_opy_):
      logger.error(bstack111l1l11l_opy_.format(bstack1l11ll1l1l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack1ll1lll_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩື")) and callable(getattr(RemoteConnection, bstack1ll1lll_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ຸࠪ"))):
          RemoteConnection._get_proxy_url = bstack111llllll1_opy_
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          ClientConfig.get_proxy_url = bstack111llllll1_opy_
      except Exception as e:
        logger.error(bstack1lll1111l_opy_.format(str(e)))
  if not CONFIG.get(bstack1ll1lll_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷູࠬ"), False) and not bstack11l1lll111_opy_:
    logger.info(bstack111l1ll11_opy_)
  bstack11111lll1_opy_ = not cli.is_enabled(CONFIG) and bstack1lll1l111l_opy_ not in [bstack1ll1lll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰ຺ࠬ")]
  bstack1lll1llll1_opy_ = bstack11111lll1_opy_ and bstack1ll1lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩົ") in CONFIG and str(CONFIG[bstack1ll1lll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪຼ")]).lower() != bstack1ll1lll_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ຽ")
  bstack11111l1l1l_opy_ = bstack11111lll1_opy_ and not bstack1lll1llll1_opy_ and (bstack1lll1l111l_opy_ != bstack1ll1lll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩ຾") or (bstack1lll1l111l_opy_ == bstack1ll1lll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠪ຿") and not bstack11l1lll111_opy_))
  if bstack1lll1l111l_opy_ not in [bstack1ll1lll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫເ")]:
    bstack1l11l1l1l1_opy_(os.path.join(os.getcwd(), bstack1ll1lll_opy_ (u"ࠫࡱࡵࡧࠨແ"), bstack1ll1lll_opy_ (u"ࠬࡱࡥࡺ࠯ࡰࡩࡹࡸࡩࡤࡵ࠱࡮ࡸࡵ࡮ࠨໂ")), logger)
  if (bstack1lll1l111l_opy_ in [bstack1ll1lll_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬໃ"), bstack1ll1lll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ໄ"), bstack1ll1lll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ໅")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      try:
        from pabot.pabot import QueueItem
        from pabot import pabot
      except Exception as e:
        logger.warning(bstack111l111l1_opy_ + str(e))
      if not is_robot_playwright_installed():
        try:
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
          WebDriverCreator._get_ff_profile = bstack11llll1l1l_opy_
          bstack1llllll1l_opy_ = WebDriverCache.close
        except Exception as e:
          logger.warning(bstack1ll111l1l1_opy_ + str(e))
        try:
          from AppiumLibrary.utils.applicationcache import ApplicationCache
          bstack1l111ll1l_opy_ = ApplicationCache.close
        except Exception as e:
          logger.debug(bstack1ll11111l_opy_ + str(e))
    except Exception as e:
      bstack1l1l1ll1ll_opy_(e, bstack1ll111l1l1_opy_)
    if bstack1lll1l111l_opy_ != bstack1ll1lll_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪໆ"):
      bstack1l11111l1_opy_()
    bstack11ll111ll_opy_ = Output.start_test
    bstack11lll1lll1_opy_ = Output.end_test
    bstack11l1ll1l1_opy_ = TestStatus.__init__
    bstack1ll1111ll_opy_ = pabot._run
    bstack1l1ll111l1_opy_ = QueueItem.__init__
    bstack1ll1lllll_opy_ = pabot._create_command_for_execution
    bstack111lllll1_opy_ = pabot._report_results
  if bstack1lll1l111l_opy_ == bstack1ll1lll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ໇"):
    global bstack1ll111llll_opy_
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l1l1ll1ll_opy_(e, bstack1l11l1111_opy_)
    bstack1l1llll111_opy_ = Runner.run_hook
    bstack11l1lllll1_opy_ = Runner.load_hooks
    bstack11lll1l1_opy_ = Step.run
    try:
      sig = inspect.signature(bstack1l1llll111_opy_)
      params = list(sig.parameters.keys())
      bstack1ll111llll_opy_ = bstack1ll1lll_opy_ (u"ࠫࡨࡵ࡮ࡵࡧࡻࡸ່ࠬ") in params
      logger.info(bstack1ll1lll_opy_ (u"ࠬࡊࡥࡵࡧࡦࡸࡪࡪࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡳࡷࡱࡣ࡭ࡵ࡯࡬ࠢࡶ࡭࡬ࡴࡡࡵࡷࡵࡩ࠿ࠦࡻࡾ້ࠩ").format(bstack1ll1lll_opy_ (u"࠭࠱࠯࠴࠱࠺ࠥ࠮ࡷࡪࡶ࡫ࠤࡨࡵ࡮ࡵࡧࡻࡸ࠮໊࠭") if bstack1ll111llll_opy_ else bstack1ll1lll_opy_ (u"ࠧ࠲࠰࠶࠯ࠥ࠮ࡷࡪࡶ࡫ࡳࡺࡺࠠࡤࡱࡱࡸࡪࡾࡴ໋ࠪࠩ")))
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡥࡷࠤࡧ࡫ࡨࡢࡸࡨࠤࡷࡻ࡮ࡠࡪࡲࡳࡰࠦࡳࡪࡩࡱࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭໌").format(str(e)))
      bstack1ll111llll_opy_ = None
  if bstack1lll1l111l_opy_ == bstack1ll1lll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩໍ"):
    try:
      from _pytest.config import Config
      bstack1ll1ll1l_opy_ = Config.getoption
      from _pytest import runner
      bstack111l111111_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warning(bstack1ll1lll_opy_ (u"ࠥࠩࡸࡀࠠࠦࡵࠥ໎"), bstack111l1ll1l1_opy_, str(e))
    try:
      from pytest_bdd import reporting
      bstack111ll11lll_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡳࠥࡸࡵ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࡷࠬ໏"))
    if bstack11lll11l1_opy_():
      logger.warning(bstack11l111llll_opy_[bstack1ll1lll_opy_ (u"࡙ࠬࡄࡌ࠯ࡊࡉࡓ࠳࠰࠱࠷ࠪ໐")])
  try:
    framework_name = bstack1ll1lll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ໑") if bstack1lll1l111l_opy_ in [bstack1ll1lll_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭໒"), bstack1ll1lll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ໓"), bstack1ll1lll_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ໔")] else bstack111lll11l1_opy_(bstack1lll1l111l_opy_)
    bstack1l1ll11l11_opy_ = {
      bstack1ll1lll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࠫ໕"): bstack1ll1lll_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷ࠱ࡨࡻࡣࡶ࡯ࡥࡩࡷ࠭໖") if bstack1lll1l111l_opy_ == bstack1ll1lll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ໗") and bstack1l11ll1lll_opy_() else framework_name,
      bstack1ll1lll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ໘"): bstack11l1llll11_opy_(framework_name),
      bstack1ll1lll_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ໙"): __version__,
      bstack1ll1lll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡺࡹࡥࡥࠩ໚"): bstack1lll1l111l_opy_
    }
    if bstack1lll1l111l_opy_ in bstack1ll1l1l1l_opy_ + bstack1l1ll1ll_opy_:
      if a11y.is_enabled_root(CONFIG):
        if bstack1ll1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ໛") in CONFIG:
          os.environ[bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫໜ")] = os.getenv(bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬໝ"), json.dumps(CONFIG[bstack1ll1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬໞ")]))
          CONFIG[bstack1ll1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ໟ")].pop(bstack1ll1lll_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬ໠"), None)
          CONFIG[bstack1ll1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ໡")].pop(bstack1ll1lll_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ໢"), None)
        bstack1ll1lll11l_opy_ = bstack1ll1lll_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧ໣") if CONFIG.get(bstack1ll1lll_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪ໤")) or bstack11lllll11l_opy_() else bstack1ll1lll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧ໥")
        if bstack1ll1lll11l_opy_ == bstack1ll1lll_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪ໦"):
          try:
            import importlib.metadata as _1ll1lll1l_opy_
            bstack11ll1ll111_opy_ = _1ll1lll1l_opy_.version(bstack1ll1lll_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦ໧"))
          except Exception:
            bstack11ll1ll111_opy_ = bstack1ll1lll_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࠩ໨")
        else:
          bstack11ll1ll111_opy_ = str(bstack1l11ll1l1l_opy_())
        bstack1l1ll11l11_opy_[bstack1ll1lll_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ໩")] = {
          bstack1ll1lll_opy_ (u"ࠪࡲࡦࡳࡥࠨ໪"): bstack1ll1lll11l_opy_,
          bstack1ll1lll_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬ໫"): bstack11ll1ll111_opy_
        }
    bstack11l11ll1l1_opy_, bstack11lll11l1l_opy_ = None, {}
    bstack1ll11ll111_opy_ = None
    bstack1l1111l11_opy_ = None
    def bstack11ll1l1lll_opy_():
      if bstack1lll1llll1_opy_:
        bstack11lll111l_opy_()
      elif bstack11111l1l1l_opy_:
        bstack11llll1ll1_opy_()
    def bstack1111l11l1l_opy_():
      nonlocal bstack11l11ll1l1_opy_, bstack11lll11l1l_opy_
      if bstack1lll1l111l_opy_ not in [bstack1ll1lll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭໬")] and not cli.is_running():
        bstack11l11ll1l1_opy_, bstack11lll11l1l_opy_ = TestHubHandler.launch(CONFIG, bstack1l1ll11l11_opy_)
    if bstack1lll1llll1_opy_ or bstack11111l1l1l_opy_:
      bstack1ll11ll111_opy_ = threading.Thread(target=bstack11ll1l1lll_opy_)
      bstack1ll11ll111_opy_.start()
    if bstack1lll1l111l_opy_ not in [bstack1ll1lll_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧ໭")] and not cli.is_running():
      bstack1l1111l11_opy_ = threading.Thread(target=bstack1111l11l1l_opy_)
      bstack1l1111l11_opy_.start()
    if bstack1ll11ll111_opy_:
      bstack1ll11ll111_opy_.join()
    if bstack1l1111l11_opy_:
      bstack1l1111l11_opy_.join()
    if bstack11lll11l1l_opy_.get(bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ໮")) is not None and a11y.bstack1l1ll111ll_opy_(CONFIG) is None:
      value = bstack11lll11l1l_opy_[bstack1ll1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ໯")].get(bstack1ll1lll_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪ໰"))
      if value is not None:
          CONFIG[bstack1ll1lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ໱")] = value
      else:
        logger.debug(bstack1ll1lll_opy_ (u"ࠦࡓࡵࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡥࡣࡷࡥࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡳࡧࡶࡴࡴࡴࡳࡦࠤ໲"))
  except Exception as e:
    logger.debug(bstack1ll111111l_opy_.format(bstack1ll1lll_opy_ (u"࡚ࠬࡥࡴࡶࡋࡹࡧ࠭໳"), str(e)))
  if bstack1lll1l111l_opy_ == bstack1ll1lll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡧࡦࡰࡨࡶ࡮ࡩࠧ໴"):
    PARALLELISE_VANILLA_PYTHON = True
    if bstack11l1lll111_opy_ and bstack1l11ll1l_opy_:
      if cli.is_enabled(CONFIG):
        bstack11llllll1_opy_ = cli.config.get(bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ໵"), {}).get(bstack1ll1lll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ໶")) if cli.config else None
      else:
        bstack11llllll1_opy_ = CONFIG.get(bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭໷"), {}).get(bstack1ll1lll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ໸"))
      bstack1111l1l1l_opy_(bstack1l1lll11_opy_)
    elif bstack11l1lll111_opy_:
      if cli.is_enabled(CONFIG):
        bstack11llllll1_opy_ = cli.config.get(bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ໹"), {}).get(bstack1ll1lll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ໺")) if cli.config else None
      else:
        bstack11llllll1_opy_ = CONFIG.get(bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ໻"), {}).get(bstack1ll1lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ໼"))
      global bstack1lllllllll_opy_
      try:
        if bstack111111l1ll_opy_(bstack11l1lll111_opy_[bstack1ll1lll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ໽")]) and multiprocessing.current_process().name == bstack1ll1lll_opy_ (u"ࠩ࠳ࠫ໾"):
          bstack11l1lll111_opy_[bstack1ll1lll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭໿")].remove(bstack1ll1lll_opy_ (u"ࠫ࠲ࡳࠧༀ"))
          bstack11l1lll111_opy_[bstack1ll1lll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ༁")].remove(bstack1ll1lll_opy_ (u"࠭ࡰࡥࡤࠪ༂"))
          bstack11l1lll111_opy_[bstack1ll1lll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ༃")] = bstack11l1lll111_opy_[bstack1ll1lll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ༄")][0]
          with open(bstack11l1lll111_opy_[bstack1ll1lll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ༅")], bstack1ll1lll_opy_ (u"ࠪࡶࠬ༆")) as f:
            file_content = f.read()
          bstack1llllll1ll_opy_ = bstack1ll1lll_opy_ (u"ࠦࠧࠨࡦࡳࡱࡰࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡷࡩࡱࠠࡪ࡯ࡳࡳࡷࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡧ࠾ࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿ࡫ࠨࡼࡿࠬ࠿ࠥ࡬ࡲࡰ࡯ࠣࡴࡩࡨࠠࡪ࡯ࡳࡳࡷࡺࠠࡑࡦࡥ࠿ࠥࡵࡧࡠࡦࡥࠤࡂࠦࡐࡥࡤ࠱ࡨࡴࡥࡢࡳࡧࡤ࡯ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡧࡩ࡫ࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠪࡶࡩࡱ࡬ࠬࠡࡣࡵ࡫࠱ࠦࡴࡦ࡯ࡳࡳࡷࡧࡲࡺࠢࡀࠤ࠵࠯࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡴࡳࡻ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡦࡸࡧࠡ࠿ࠣࡷࡹࡸࠨࡪࡰࡷࠬࡦࡸࡧࠪ࠭࠴࠴࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡪࡾࡣࡦࡲࡷࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡢࡵࠣࡩ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡰࡢࡵࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡲ࡫ࡤࡪࡢࠩࡵࡨࡰ࡫࠲ࡡࡳࡩ࠯ࡸࡪࡳࡰࡰࡴࡤࡶࡾ࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡔࡩࡨ࠮ࡥࡱࡢࡦࠥࡃࠠ࡮ࡱࡧࡣࡧࡸࡥࡢ࡭ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡐࡥࡤ࠱ࡨࡴࡥࡢࡳࡧࡤ࡯ࠥࡃࠠ࡮ࡱࡧࡣࡧࡸࡥࡢ࡭ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡐࡥࡤࠫ࠭࠳ࡹࡥࡵࡡࡷࡶࡦࡩࡥࠩࠫ࡟ࡲࠧࠨࠢ༇").format(str(bstack11l1lll111_opy_))
          bstack1111l11ll_opy_ = bstack1llllll1ll_opy_ + file_content
          bstack1111l1l1ll_opy_ = bstack11l1lll111_opy_[bstack1ll1lll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ༈")] + bstack1ll1lll_opy_ (u"࠭࡟ࡣࡵࡷࡥࡨࡱ࡟ࡵࡧࡰࡴ࠳ࡶࡹࠨ༉")
          with open(bstack1111l1l1ll_opy_, bstack1ll1lll_opy_ (u"ࠧࡸࠩ༊")):
            pass
          with open(bstack1111l1l1ll_opy_, bstack1ll1lll_opy_ (u"ࠣࡹ࠮ࠦ་")) as f:
            f.write(bstack1111l11ll_opy_)
          import subprocess
          bstack1111lllll1_opy_ = subprocess.run([bstack1ll1lll_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࠤ༌"), bstack1111l1l1ll_opy_])
          if os.path.exists(bstack1111l1l1ll_opy_):
            os.unlink(bstack1111l1l1ll_opy_)
          os._exit(bstack1111lllll1_opy_.returncode)
        else:
          if bstack111111l1ll_opy_(bstack11l1lll111_opy_[bstack1ll1lll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭།")]):
            bstack11l1lll111_opy_[bstack1ll1lll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ༎")].remove(bstack1ll1lll_opy_ (u"ࠬ࠳࡭ࠨ༏"))
            bstack11l1lll111_opy_[bstack1ll1lll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ༐")].remove(bstack1ll1lll_opy_ (u"ࠧࡱࡦࡥࠫ༑"))
            bstack11l1lll111_opy_[bstack1ll1lll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ༒")] = bstack11l1lll111_opy_[bstack1ll1lll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ༓")][0]
          bstack1111l1l1l_opy_(bstack1l1lll11_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack11l1lll111_opy_[bstack1ll1lll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭༔")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1ll1lll_opy_ (u"ࠫࡤࡥ࡮ࡢ࡯ࡨࡣࡤ࠭༕")] = bstack1ll1lll_opy_ (u"ࠬࡥ࡟࡮ࡣ࡬ࡲࡤࡥࠧ༖")
          mod_globals[bstack1ll1lll_opy_ (u"࠭࡟ࡠࡨ࡬ࡰࡪࡥ࡟ࠨ༗")] = os.path.abspath(bstack11l1lll111_opy_[bstack1ll1lll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧ༘ࠪ")])
          exec(open(bstack11l1lll111_opy_[bstack1ll1lll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨ༙ࠫ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1ll1lll_opy_ (u"ࠩࡆࡥࡺ࡭ࡨࡵࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠩ༚").format(str(e)))
          for driver in bstack1lllllllll_opy_:
            bstack111l1l111_opy_.append({
              bstack1ll1lll_opy_ (u"ࠪࡲࡦࡳࡥࠨ༛"): bstack11l1lll111_opy_[bstack1ll1lll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ༜")],
              bstack1ll1lll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ༝"): str(e),
              bstack1ll1lll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ༞"): multiprocessing.current_process().name
            })
            bstack1111lll1l1_opy_(driver, bstack1ll1lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ༟"), bstack1ll1lll_opy_ (u"ࠣࡕࡨࡷࡸ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦ༠") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1lllllllll_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1ll1ll1l1_opy_, CONFIG, logger)
      bstack1ll111111_opy_()
      bstack11lll11ll_opy_()
      percy.bstack111llll1ll_opy_()
      bstack1l1ll111l_opy_ = {
        bstack1ll1lll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ༡"): args[0],
        bstack1ll1lll_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪ༢"): CONFIG,
        bstack1ll1lll_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬ༣"): bstack1lllll111_opy_,
        bstack1ll1lll_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ༤"): bstack1ll1ll1l1_opy_
      }
      if bstack1ll1lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ༥") in CONFIG:
        bstack11lll111l1_opy_ = bstack1lllll1ll1_opy_(args, logger, CONFIG, BROWSERSTACK_AUTOMATION, bstack1ll1ll1111_opy_)
        bstack111l11llll_opy_ = bstack11lll111l1_opy_.bstack1111ll1ll_opy_(run_on_browserstack, bstack1l1ll111l_opy_, bstack111111l1ll_opy_(args))
      else:
        if bstack111111l1ll_opy_(args):
          bstack1l1ll111l_opy_[bstack1ll1lll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ༦")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1l1ll111l_opy_,))
          test.start()
          test.join()
        else:
          bstack1111l1l1l_opy_(bstack1l1lll11_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1ll1lll_opy_ (u"ࠨࡡࡢࡲࡦࡳࡥࡠࡡࠪ༧")] = bstack1ll1lll_opy_ (u"ࠩࡢࡣࡲࡧࡩ࡯ࡡࡢࠫ༨")
          mod_globals[bstack1ll1lll_opy_ (u"ࠪࡣࡤ࡬ࡩ࡭ࡧࡢࡣࠬ༩")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1lll1l111l_opy_ == bstack1ll1lll_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ༪") or bstack1lll1l111l_opy_ == bstack1ll1lll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ༫"):
    percy.init(bstack1ll1ll1l1_opy_, CONFIG, logger)
    percy.bstack111llll1ll_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1l1l1ll1ll_opy_(e, bstack1ll111l1l1_opy_)
    bstack1ll111111_opy_()
    bstack1111l1l1l_opy_(bstack111l1lllll_opy_)
    if BROWSERSTACK_AUTOMATION:
      bstack11l1111l1l_opy_(bstack111l1lllll_opy_, args)
      if bstack1ll1lll_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ༬") in args:
        i = args.index(bstack1ll1lll_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ༭"))
        args.pop(i)
        args.pop(i)
      if bstack1ll1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ༮") not in CONFIG:
        CONFIG[bstack1ll1lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ༯")] = [{}]
        bstack1ll1ll1111_opy_ = 1
      if bstack1111ll11l1_opy_ == 0:
        bstack1111ll11l1_opy_ = 1
      args.insert(0, str(bstack1111ll11l1_opy_))
      args.insert(0, str(bstack1ll1lll_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨ༰")))
    if TestHubHandler.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack11l11lllll_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack11l1llll1_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack1ll1lll_opy_ (u"ࠦࡗࡕࡂࡐࡖࡢࡓࡕ࡚ࡉࡐࡐࡖࠦ༱"),
        ).parse_args(bstack11l11lllll_opy_)
        bstack11l11ll1l_opy_ = args.index(bstack11l11lllll_opy_[0]) if len(bstack11l11lllll_opy_) > 0 else len(args)
        args.insert(bstack11l11ll1l_opy_, str(bstack1ll1lll_opy_ (u"ࠬ࠳࠭࡭࡫ࡶࡸࡪࡴࡥࡳࠩ༲")))
        args.insert(bstack11l11ll1l_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡲࡰࡤࡲࡸࡤࡲࡩࡴࡶࡨࡲࡪࡸ࠮ࡱࡻࠪ༳"))))
        if bstack1l11ll1ll1_opy_.bstack1llll1lll1_opy_(CONFIG):
          args.insert(bstack11l11ll1l_opy_, str(bstack1ll1lll_opy_ (u"ࠧ࠮࠯࡯࡭ࡸࡺࡥ࡯ࡧࡵࠫ༴")))
          args.insert(bstack11l11ll1l_opy_ + 1, str(bstack1ll1lll_opy_ (u"ࠨࡔࡨࡸࡷࡿࡆࡢ࡫࡯ࡩࡩࡀࡻࡾ༵ࠩ").format(bstack1l11ll1ll1_opy_.bstack1ll111l1_opy_(CONFIG))))
        if bstack11llll111l_opy_(os.environ.get(bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠧ༶"))) and str(os.environ.get(bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙༷ࠧ"), bstack1ll1lll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ༸"))) != bstack1ll1lll_opy_ (u"ࠬࡴࡵ࡭࡮༹ࠪ"):
          for bstack1lll1llll_opy_ in bstack11l1llll1_opy_:
            args.remove(bstack1lll1llll_opy_)
          test_files = os.environ.get(bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࡣ࡙ࡋࡓࡕࡕࠪ༺")).split(bstack1ll1lll_opy_ (u"ࠧ࠭ࠩ༻"))
          for bstack111111l11l_opy_ in test_files:
            args.append(bstack111111l11l_opy_)
      except Exception as e:
        logger.error(bstack1ll1lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡡࡵࡶࡤࡧ࡭࡯࡮ࡨࠢ࡯࡭ࡸࡺࡥ࡯ࡧࡵࠤ࡫ࡵࡲࠡࡽࢀ࠲ࠥࡋࡲࡳࡱࡵࠤ࠲ࠦࡻࡾࠤ༼").format(bstack11l11lll11_opy_, e))
    pabot.main(args)
  elif bstack1lll1l111l_opy_ == bstack1ll1lll_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ༽"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1l1l1ll1ll_opy_(e, bstack1ll111l1l1_opy_)
    for a in args:
      if bstack1ll1lll_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡓࡐࡆ࡚ࡆࡐࡔࡐࡍࡓࡊࡅ࡙ࠩ༾") in a:
        PLATFORM_INDEX = int(a.split(bstack1ll1lll_opy_ (u"ࠫ࠿࠭༿"))[1])
      if bstack1ll1lll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡉࡋࡆࡍࡑࡆࡅࡑࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩཀ") in a:
        bstack11llllll1_opy_ = str(a.split(bstack1ll1lll_opy_ (u"࠭࠺ࠨཁ"))[1])
      if bstack1ll1lll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙ࠧག") in a:
        bstack1lll111ll_opy_ = str(a.split(bstack1ll1lll_opy_ (u"ࠨ࠼ࠪགྷ"))[1])
    bstack1111ll111l_opy_ = None
    bstack11l1111l_opy_ = None
    if bstack1ll1lll_opy_ (u"ࠩ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠨང") in args:
      i = args.index(bstack1ll1lll_opy_ (u"ࠪ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠩཅ"))
      args.pop(i)
      bstack1111ll111l_opy_ = args.pop(i)
    if bstack1ll1lll_opy_ (u"ࠫ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࠧཆ") in args:
      i = args.index(bstack1ll1lll_opy_ (u"ࠬ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸࠨཇ"))
      args.pop(i)
      bstack11l1111l_opy_ = args.pop(i)
    if bstack1111ll111l_opy_ is not None:
      global bstack1l1l11ll1l_opy_
      bstack1l1l11ll1l_opy_ = bstack1111ll111l_opy_
    if bstack11l1111l_opy_ is not None and int(PLATFORM_INDEX) < 0:
      PLATFORM_INDEX = int(bstack11l1111l_opy_)
    if cli.is_enabled(CONFIG):
      if cli.bstack111llllll_opy_():
        bstack1l111111ll_opy_.invoke(Events.CONNECT, bstack11lll111_opy_())
        cli.bstack1l1lll1ll1_opy_(PLATFORM_INDEX)
      if cli.bstack1llll11ll_opy_(bstack1llll1ll1l_opy_):
        cli.bstack1lll1l1ll_opy_()
    bstack1111l1l1l_opy_(bstack111l1lllll_opy_)
    run_cli(args)
    if bstack1ll1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶࠪ཈") in multiprocessing.current_process().__dict__.keys():
      for bstack11l1l1l1ll_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack111l1l111_opy_.append(bstack11l1l1l1ll_opy_)
  elif bstack1lll1l111l_opy_ == bstack1ll1lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧཉ"):
    bstack1ll1ll11_opy_ = bstack1llll1111_opy_(args, logger, CONFIG, BROWSERSTACK_AUTOMATION)
    bstack1ll1ll11_opy_.bstack11l11llll1_opy_()
    bstack1ll111111_opy_()
    PARALLELISE_THREADING_PYTHON = True
    bstack11l1llll1l_opy_ = bstack1ll1ll11_opy_.bstack11l1ll11ll_opy_()
    bstack1ll1ll11_opy_.bstack1l1ll111l_opy_(bstack1111111l1_opy_)
    bstack1ll1ll11_opy_.bstack111l1llll_opy_()
    bstack11lll1ll1_opy_(bstack1lll1l111l_opy_, CONFIG, bstack1ll1ll11_opy_.bstack111111lll_opy_())
    bstack1ll11111_opy_.end(EVENTS.bstack111lll1l11_opy_.value, EVENTS.bstack111lll1l11_opy_.value + bstack1ll1lll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣཊ"), EVENTS.bstack111lll1l11_opy_.value + bstack1ll1lll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢཋ"), status=True, failure=None, test_name=SESSION_NAME)
    bstack1llll11lll_opy_ = bstack1ll1ll11_opy_.bstack1111ll1ll_opy_(bstack11l111ll11_opy_, {
      bstack1ll1lll_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪཌ"): CONFIG,
      bstack1ll1lll_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬཌྷ"): bstack1lllll111_opy_,
      bstack1ll1lll_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧཎ"): bstack1ll1ll1l1_opy_,
      bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩཏ"): BROWSERSTACK_AUTOMATION,
      bstack1ll1lll_opy_ (u"ࠧࡐࡘࡈࡖࡗࡏࡄࡆࡡࡏࡓࡆࡊ࡟ࡕࡇࡖࡘࡎࡔࡇࠨཐ"): bstack1111l1l1l1_opy_
    })
    if not bstack11l1lll111_opy_:
      bstack111ll1lll1_opy_ = bstack1lll1lll11_opy_.bstack11l1llllll_opy_(EVENTS.bstack11ll11ll1l_opy_.value)
    try:
      bstack1ll1lll11_opy_, bstack11l1l1l111_opy_ = map(list, zip(*bstack1llll11lll_opy_))
      bstack1ll11l11_opy_ = bstack1ll1lll11_opy_[0]
      for status_code in bstack11l1l1l111_opy_:
        if status_code != 0:
          bstack11111lll_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡧࡶࡦࠢࡨࡶࡷࡵࡲࡴࠢࡤࡲࡩࠦࡳࡵࡣࡷࡹࡸࠦࡣࡰࡦࡨ࠲ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࠼ࠣࡿࢂࠨད").format(str(e)))
  elif bstack1lll1l111l_opy_ == bstack1ll1lll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩདྷ"):
    try:
      from behave.__main__ import main as bstack1ll1l11ll1_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1l1l1ll1ll_opy_(e, bstack1l11l1111_opy_)
    bstack1ll111111_opy_()
    PARALLELISE_THREADING_PYTHON = True
    bstack11l111lll_opy_ = 1
    if bstack1ll1lll_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪན") in CONFIG:
      bstack11l111lll_opy_ = CONFIG[bstack1ll1lll_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫཔ")]
    if bstack1ll1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨཕ") in CONFIG:
      bstack11ll1l11l1_opy_ = int(bstack11l111lll_opy_) * int(len(CONFIG[bstack1ll1lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩབ")]))
    else:
      bstack11ll1l11l1_opy_ = int(bstack11l111lll_opy_)
    config = Configuration(args)
    bstack1l1111ll1_opy_ = config.paths
    if len(bstack1l1111ll1_opy_) == 0:
      import glob
      pattern = bstack1ll1lll_opy_ (u"ࠧࠫࠬ࠲࠮࠳࡬ࡥࡢࡶࡸࡶࡪ࠭བྷ")
      bstack1l11l1l1_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1l11l1l1_opy_)
      config = Configuration(args)
      bstack1l1111ll1_opy_ = config.paths
    bstack111ll1llll_opy_ = [os.path.normpath(item) for item in bstack1l1111ll1_opy_]
    bstack11l11l1ll1_opy_ = [os.path.normpath(item) for item in args]
    bstack1l11lll1l_opy_ = [item for item in bstack11l11l1ll1_opy_ if item not in bstack111ll1llll_opy_]
    import platform as pf
    if pf.system().lower() == bstack1ll1lll_opy_ (u"ࠨࡹ࡬ࡲࡩࡵࡷࡴࠩམ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack111ll1llll_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l11ll11ll_opy_)))
                    for bstack1l11ll11ll_opy_ in bstack111ll1llll_opy_]
    bstack1111l1l1_opy_ = []
    for spec in bstack111ll1llll_opy_:
      bstack1ll11llll_opy_ = []
      bstack1ll11llll_opy_ += bstack1l11lll1l_opy_
      bstack1ll11llll_opy_.append(spec)
      bstack1111l1l1_opy_.append(bstack1ll11llll_opy_)
    execution_items = []
    for bstack1ll11llll_opy_ in bstack1111l1l1_opy_:
      if bstack1ll1lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬཙ") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack1ll1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ཚ")]):
          item = {}
          item[bstack1ll1lll_opy_ (u"ࠫࡦࡸࡧࠨཛ")] = bstack1ll1lll_opy_ (u"ࠬࠦࠧཛྷ").join(bstack1ll11llll_opy_)
          item[bstack1ll1lll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬཝ")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack1ll1lll_opy_ (u"ࠧࡢࡴࡪࠫཞ")] = bstack1ll1lll_opy_ (u"ࠨࠢࠪཟ").join(bstack1ll11llll_opy_)
        item[bstack1ll1lll_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨའ")] = 0
        execution_items.append(item)
    bstack1llll1l1l1_opy_ = bstack1l11l1lll1_opy_(execution_items, bstack11ll1l11l1_opy_)
    for execution_item in bstack1llll1l1l1_opy_:
      bstack1111111lll_opy_ = []
      for item in execution_item:
        bstack1111111lll_opy_.append(bstack1lll1l1l1l_opy_(name=str(item[bstack1ll1lll_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩཡ")]),
                                             target=bstack1111ll1l_opy_,
                                             args=(item[bstack1ll1lll_opy_ (u"ࠫࡦࡸࡧࠨར")],)))
      for t in bstack1111111lll_opy_:
        t.start()
      for t in bstack1111111lll_opy_:
        t.join()
  else:
    bstack1l1111ll_opy_(bstack11111l111_opy_)
  if not bstack11l1lll111_opy_:
    bstack111ll1l1l_opy_()
    if bstack111ll1lll1_opy_:
      bstack1lll1lll11_opy_.end(EVENTS.bstack11ll11ll1l_opy_.value, bstack111ll1lll1_opy_ + bstack1ll1lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧལ"), bstack111ll1lll1_opy_ + bstack1ll1lll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦཤ"), status=True, failure=None, test_name=None)
  logger_utils.bstack1llll111_opy_()
def browserstack_initialize(bstack1l1ll11l1_opy_=None):
  logger.info(bstack1ll1lll_opy_ (u"ࠧࡓࡷࡱࡲ࡮ࡴࡧࠡࡕࡇࡏࠥࡽࡩࡵࡪࠣࡥࡷ࡭ࡳ࠻ࠢࠪཥ") + str(bstack1l1ll11l1_opy_))
  run_on_browserstack(bstack1l1ll11l1_opy_, None, True)
@measure(event_name=EVENTS.bstack111llll1l1_opy_, stage=STAGE.bstack1ll1llll_opy_, bstack1ll1l11l1l_opy_=SESSION_NAME)
def bstack111ll1l1l_opy_():
  global CONFIG
  global bstack11111lllll_opy_
  global bstack11111lll_opy_
  global bstack1l11ll1ll_opy_
  global global_config
  global _11l11l111_opy_
  bstack11l1l11l_opy_.bstack1l1ll11ll1_opy_()
  _11l11l111_opy_ = cli.is_running()
  if _11l11l111_opy_:
    bstack1l111111ll_opy_.invoke(Events.bstack11l11ll1ll_opy_)
  else:
    bstack1lll11llll_opy_ = bstack1l11ll1ll1_opy_.get_instance(config=CONFIG)
    bstack1lll11llll_opy_.bstack111llll1_opy_(CONFIG)
  hashed_id = None
  bstack1ll1111l11_opy_ = None
  def bstack1lll11l1ll_opy_():
    try:
      if bstack11111lllll_opy_ == bstack1ll1lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨས"):
        if not cli.is_enabled(CONFIG):
          TestHubHandler.stop()
      else:
        TestHubHandler.stop()
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡵࡷࡳࡵࡶࡩ࡯ࡩࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࢁࡽࠣཧ").format(e))
  def bstack1ll111ll_opy_():
    try:
      if not cli.is_enabled(CONFIG):
        bstack11lll1l11_opy_.bstack1111ll11l_opy_()
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡳࡶ࡮ࡴࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࠣࡰ࡮ࡴ࡫࠻ࠢࡾࢁࠧཨ").format(e))
  def bstack11lllll1ll_opy_():
    nonlocal hashed_id, bstack1ll1111l11_opy_
    try:
      if bstack1ll1lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨཀྵ") in CONFIG and str(CONFIG[bstack1ll1lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩཪ")]).lower() != bstack1ll1lll_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬཫ"):
        hashed_id, bstack1ll1111l11_opy_ = bstack1l1l1l1ll_opy_()
      else:
        hashed_id, bstack1ll1111l11_opy_ = get_build_link()
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࠦ࡬ࡪࡰ࡮࠾ࠥࢁࡽࠣཬ").format(e))
  bstack11111llll1_opy_ = threading.Thread(target=bstack1lll11l1ll_opy_)
  bstack11l1111111_opy_ = threading.Thread(target=bstack1ll111ll_opy_)
  bstack1l1l1lll_opy_ = threading.Thread(target=bstack11lllll1ll_opy_)
  threads = [bstack11111llll1_opy_, bstack11l1111111_opy_, bstack1l1l1lll_opy_]
  for thread in threads:
    try:
      thread.start()
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡴࡶࡤࡶࡹ࡯࡮ࡨࠢࡷ࡬ࡷ࡫ࡡࡥࠢࡾࢁ࠿ࠦࡻࡾࠤ཭").format(thread.name, e))
  for thread in threads:
    try:
      thread.join()
    except Exception as e:
      logger.debug(bstack1ll1lll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡬ࡲ࡭ࡳ࡯࡮ࡨࠢࡷ࡬ࡷ࡫ࡡࡥࠢࡾࢁ࠿ࠦࡻࡾࠤ཮").format(thread.name, e))
  bstack11l11111l1_opy_(hashed_id)
  logger.info(bstack1ll1lll_opy_ (u"ࠪࡗࡉࡑࠠࡳࡷࡱࠤࡪࡴࡤࡦࡦࠣࡪࡴࡸࠠࡪࡦ࠽ࠫ཯") + global_config.get_property(bstack1ll1lll_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭཰"), bstack1ll1lll_opy_ (u"ཱࠬ࠭")) + bstack1ll1lll_opy_ (u"࠭ࠬࠡࡶࡨࡷࡹ࡮ࡵࡣࠢ࡬ࡨ࠿ིࠦࠧ") + os.getenv(bstack1ll1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈཱིࠬ"), bstack1ll1lll_opy_ (u"ࠨུࠩ")))
  if hashed_id is not None and bstack1l1l11111_opy_() != -1:
    sessions = bstack11lll111ll_opy_(hashed_id)
    bstack1l11l111_opy_(sessions, bstack1ll1111l11_opy_)
  if bstack11111lllll_opy_ == bstack1ll1lll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵཱུࠩ") and bstack11111lll_opy_ != 0:
    sys.exit(bstack11111lll_opy_)
  if bstack11111lllll_opy_ == bstack1ll1lll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪྲྀ") and bstack1l11ll1ll_opy_ != 0:
    sys.exit(bstack1l11ll1ll_opy_)
def bstack11l11111l1_opy_(new_id):
    global bstack1ll111l11l_opy_
    bstack1ll111l11l_opy_ = new_id
def bstack111lll11l1_opy_(bstack1ll11lll11_opy_):
  if bstack1ll11lll11_opy_:
    return bstack1ll11lll11_opy_.capitalize()
  else:
    return bstack1ll1lll_opy_ (u"ࠫࠬཷ")
@measure(event_name=EVENTS.bstack1l1l1l11l1_opy_, stage=STAGE.bstack1ll1llll_opy_, bstack1ll1l11l1l_opy_=SESSION_NAME)
def bstack1l1lll1l1l_opy_(bstack1llll11l_opy_):
  if bstack1ll1lll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪླྀ") in bstack1llll11l_opy_ and bstack1llll11l_opy_[bstack1ll1lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫཹ")] != bstack1ll1lll_opy_ (u"ࠧࠨེ"):
    return bstack1llll11l_opy_[bstack1ll1lll_opy_ (u"ࠨࡰࡤࡱࡪཻ࠭")]
  else:
    bstack1ll1l11l1l_opy_ = bstack1ll1lll_opy_ (u"ࠤོࠥ")
    if bstack1ll1lll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧཽࠪ") in bstack1llll11l_opy_ and bstack1llll11l_opy_[bstack1ll1lll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫཾ")] != None:
      bstack1ll1l11l1l_opy_ += bstack1llll11l_opy_[bstack1ll1lll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬཿ")] + bstack1ll1lll_opy_ (u"ࠨࠬࠡࠤྀ")
      if bstack1llll11l_opy_[bstack1ll1lll_opy_ (u"ࠧࡰࡵཱྀࠪ")] == bstack1ll1lll_opy_ (u"ࠣ࡫ࡲࡷࠧྂ"):
        bstack1ll1l11l1l_opy_ += bstack1ll1lll_opy_ (u"ࠤ࡬ࡓࡘࠦࠢྃ")
      bstack1ll1l11l1l_opy_ += (bstack1llll11l_opy_[bstack1ll1lll_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴ྄ࠧ")] or bstack1ll1lll_opy_ (u"ࠫࠬ྅"))
      return bstack1ll1l11l1l_opy_
    else:
      bstack1ll1l11l1l_opy_ += bstack111lll11l1_opy_(bstack1llll11l_opy_[bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭྆")]) + bstack1ll1lll_opy_ (u"ࠨࠠࠣ྇") + (
              bstack1llll11l_opy_[bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩྈ")] or bstack1ll1lll_opy_ (u"ࠨࠩྉ")) + bstack1ll1lll_opy_ (u"ࠤ࠯ࠤࠧྊ")
      if bstack1llll11l_opy_[bstack1ll1lll_opy_ (u"ࠪࡳࡸ࠭ྋ")] == bstack1ll1lll_opy_ (u"ࠦ࡜࡯࡮ࡥࡱࡺࡷࠧྌ"):
        bstack1ll1l11l1l_opy_ += bstack1ll1lll_opy_ (u"ࠧ࡝ࡩ࡯ࠢࠥྍ")
      bstack1ll1l11l1l_opy_ += bstack1llll11l_opy_[bstack1ll1lll_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪྎ")] or bstack1ll1lll_opy_ (u"ࠧࠨྏ")
      return bstack1ll1l11l1l_opy_
@measure(event_name=EVENTS.bstack11l1ll1ll_opy_, stage=STAGE.bstack1ll1llll_opy_, bstack1ll1l11l1l_opy_=SESSION_NAME)
def bstack1111111ll_opy_(bstack1l1l1l11_opy_):
  if bstack1l1l1l11_opy_ == bstack1ll1lll_opy_ (u"ࠣࡦࡲࡲࡪࠨྐ"):
    return bstack1ll1lll_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾࡬ࡸࡥࡦࡰ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦ࡬ࡸࡥࡦࡰࠥࡂࡈࡵ࡭ࡱ࡮ࡨࡸࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬྑ")
  elif bstack1l1l1l11_opy_ == bstack1ll1lll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥྒ"):
    return bstack1ll1lll_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡲࡦࡦ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡷ࡫ࡤࠣࡀࡉࡥ࡮ࡲࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧྒྷ")
  elif bstack1l1l1l11_opy_ == bstack1ll1lll_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧྔ"):
    return bstack1ll1lll_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡩࡵࡩࡪࡴ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡩࡵࡩࡪࡴࠢ࠿ࡒࡤࡷࡸ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ྕ")
  elif bstack1l1l1l11_opy_ == bstack1ll1lll_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨྖ"):
    return bstack1ll1lll_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡶࡪࡪ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡴࡨࡨࠧࡄࡅࡳࡴࡲࡶࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪྗ")
  elif bstack1l1l1l11_opy_ == bstack1ll1lll_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥ྘"):
    return bstack1ll1lll_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࠩࡥࡦࡣ࠶࠶࠻ࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࠤࡧࡨࡥ࠸࠸࠶ࠣࡀࡗ࡭ࡲ࡫࡯ࡶࡶ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨྙ")
  elif bstack1l1l1l11_opy_ == bstack1ll1lll_opy_ (u"ࠦࡷࡻ࡮࡯࡫ࡱ࡫ࠧྚ"):
    return bstack1ll1lll_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡣ࡮ࡤࡧࡰࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡣ࡮ࡤࡧࡰࠨ࠾ࡓࡷࡱࡲ࡮ࡴࡧ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ྛ")
  else:
    return bstack1ll1lll_opy_ (u"࠭࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡥࡰࡦࡩ࡫࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡥࡰࡦࡩ࡫ࠣࡀࠪྜ") + bstack111lll11l1_opy_(
      bstack1l1l1l11_opy_) + bstack1ll1lll_opy_ (u"ࠧ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ྜྷ")
def bstack1l1l1lll1_opy_(session):
  return bstack1ll1lll_opy_ (u"ࠨ࠾ࡷࡶࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡸ࡯ࡸࠤࡁࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠥࡹࡥࡴࡵ࡬ࡳࡳ࠳࡮ࡢ࡯ࡨࠦࡃࡂࡡࠡࡪࡵࡩ࡫ࡃࠢࡼࡿࠥࠤࡹࡧࡲࡨࡧࡷࡁࠧࡥࡢ࡭ࡣࡱ࡯ࠧࡄࡻࡾ࠾࠲ࡥࡃࡂ࠯ࡵࡦࡁࡿࢂࢁࡽ࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿࠳ࡹࡸ࠾ࠨྞ").format(
    session[bstack1ll1lll_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤࡡࡸࡶࡱ࠭ྟ")], bstack1l1lll1l1l_opy_(session), bstack1111111ll_opy_(session[bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡸࡦࡺࡵࡴࠩྠ")]),
    bstack1111111ll_opy_(session[bstack1ll1lll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫྡ")]),
    bstack111lll11l1_opy_(session[bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ྡྷ")] or session[bstack1ll1lll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ྣ")] or bstack1ll1lll_opy_ (u"ࠧࠨྤ")) + bstack1ll1lll_opy_ (u"ࠣࠢࠥྥ") + (session[bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫྦ")] or bstack1ll1lll_opy_ (u"ࠪࠫྦྷ")),
    session[bstack1ll1lll_opy_ (u"ࠫࡴࡹࠧྨ")] + bstack1ll1lll_opy_ (u"ࠧࠦࠢྩ") + session[bstack1ll1lll_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪྪ")], session[bstack1ll1lll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩྫ")] or bstack1ll1lll_opy_ (u"ࠨࠩྫྷ"),
    session[bstack1ll1lll_opy_ (u"ࠩࡦࡶࡪࡧࡴࡦࡦࡢࡥࡹ࠭ྭ")] if session[bstack1ll1lll_opy_ (u"ࠪࡧࡷ࡫ࡡࡵࡧࡧࡣࡦࡺࠧྮ")] else bstack1ll1lll_opy_ (u"ࠫࠬྯ"))
@measure(event_name=EVENTS.bstack11111ll1ll_opy_, stage=STAGE.bstack1ll1llll_opy_, bstack1ll1l11l1l_opy_=SESSION_NAME)
def bstack1l11l111_opy_(sessions, bstack1ll1111l11_opy_):
  try:
    bstack11l11l11ll_opy_ = bstack1ll1lll_opy_ (u"ࠧࠨྰ")
    if not os.path.exists(bstack111l11l1_opy_):
      os.mkdir(bstack111l11l1_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll1lll_opy_ (u"࠭ࡡࡴࡵࡨࡸࡸ࠵ࡲࡦࡲࡲࡶࡹ࠴ࡨࡵ࡯࡯ࠫྱ")), bstack1ll1lll_opy_ (u"ࠧࡳࠩྲ")) as f:
      bstack11l11l11ll_opy_ = f.read()
    bstack11l11l11ll_opy_ = bstack11l11l11ll_opy_.replace(bstack1ll1lll_opy_ (u"ࠨࡽࠨࡖࡊ࡙ࡕࡍࡖࡖࡣࡈࡕࡕࡏࡖࠨࢁࠬླ"), str(len(sessions)))
    bstack11l11l11ll_opy_ = bstack11l11l11ll_opy_.replace(bstack1ll1lll_opy_ (u"ࠩࡾࠩࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠥࡾࠩྴ"), bstack1ll1111l11_opy_)
    bstack11l11l11ll_opy_ = bstack11l11l11ll_opy_.replace(bstack1ll1lll_opy_ (u"ࠪࡿࠪࡈࡕࡊࡎࡇࡣࡓࡇࡍࡆࠧࢀࠫྵ"),
                                              sessions[0].get(bstack1ll1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡲࡦࡳࡥࠨྶ")) if sessions[0] else bstack1ll1lll_opy_ (u"ࠬ࠭ྷ"))
    with open(os.path.join(bstack111l11l1_opy_, bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡸࡥࡱࡱࡵࡸ࠳࡮ࡴ࡮࡮ࠪྸ")), bstack1ll1lll_opy_ (u"ࠧࡸࠩྐྵ")) as stream:
      stream.write(bstack11l11l11ll_opy_.split(bstack1ll1lll_opy_ (u"ࠨࡽࠨࡗࡊ࡙ࡓࡊࡑࡑࡗࡤࡊࡁࡕࡃࠨࢁࠬྺ"))[0])
      for session in sessions:
        stream.write(bstack1l1l1lll1_opy_(session))
      stream.write(bstack11l11l11ll_opy_.split(bstack1ll1lll_opy_ (u"ࠩࡾࠩࡘࡋࡓࡔࡋࡒࡒࡘࡥࡄࡂࡖࡄࠩࢂ࠭ྻ"))[1])
    logger.info(bstack1ll1lll_opy_ (u"ࠪࡋࡪࡴࡥࡳࡣࡷࡩࡩࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡨࡵࡪ࡮ࡧࠤࡦࡸࡴࡪࡨࡤࡧࡹࡹࠠࡢࡶࠣࡿࢂ࠭ྼ").format(bstack111l11l1_opy_));
  except Exception as e:
    logger.debug(bstack111lllll11_opy_.format(str(e)))
def bstack11lll111ll_opy_(hashed_id):
  global CONFIG
  try:
    bstack1ll1l111l_opy_ = datetime.datetime.now()
    host = bstack1ll1lll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠯ࡦࡰࡴࡻࡤ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫ྽") if bstack1ll1lll_opy_ (u"ࠬࡧࡰࡱࠩ྾") in CONFIG else bstack1ll1lll_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡲ࡬࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧ྿")
    user = CONFIG[bstack1ll1lll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ࿀")]
    key = CONFIG[bstack1ll1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ࿁")]
    bstack1l1l111l1_opy_ = bstack1ll1lll_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨ࿂") if bstack1ll1lll_opy_ (u"ࠪࡥࡵࡶࠧ࿃") in CONFIG else (bstack1ll1lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨ࿄") if CONFIG.get(bstack1ll1lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩ࿅")) else bstack1ll1lll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ࿆"))
    host = bstack1l11llll1l_opy_(cli.config, [bstack1ll1lll_opy_ (u"ࠢࡢࡲ࡬ࡷࠧ࿇"), bstack1ll1lll_opy_ (u"ࠣࡣࡳࡴࡆࡻࡴࡰ࡯ࡤࡸࡪࠨ࿈"), bstack1ll1lll_opy_ (u"ࠤࡤࡴ࡮ࠨ࿉")], host) if bstack1ll1lll_opy_ (u"ࠪࡥࡵࡶࠧ࿊") in CONFIG else bstack1l11llll1l_opy_(cli.config, [bstack1ll1lll_opy_ (u"ࠦࡦࡶࡩࡴࠤ࿋"), bstack1ll1lll_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫ࠢ࿌"), bstack1ll1lll_opy_ (u"ࠨࡡࡱ࡫ࠥ࿍")], host)
    url = bstack1ll1lll_opy_ (u"ࠧࡼࡿ࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾ࠱ࡶࡩࡸࡹࡩࡰࡰࡶ࠲࡯ࡹ࡯࡯ࠩ࿎").format(host, bstack1l1l111l1_opy_, hashed_id)
    headers = {
      bstack1ll1lll_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧ࿏"): bstack1ll1lll_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬ࿐"),
    }
    proxies = bstack11ll1l111l_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies, auth=(user, key))
    if response.json():
      cli.bstack1111lll11_opy_(bstack1ll1lll_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻ࡩࡨࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡹ࡟࡭࡫ࡶࡸࠧ࿑"), datetime.datetime.now() - bstack1ll1l111l_opy_)
      return list(map(lambda session: session[bstack1ll1lll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩ࿒")], response.json()))
  except Exception as e:
    logger.debug(bstack1ll11l11l1_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack1l11l1l1ll_opy_, stage=STAGE.bstack1ll1llll_opy_, bstack1ll1l11l1l_opy_=SESSION_NAME)
def get_build_link():
  global CONFIG
  global bstack1ll111l11l_opy_
  try:
    if bstack1ll1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ࿓") in CONFIG:
      bstack1ll1l111l_opy_ = datetime.datetime.now()
      host = bstack1ll1lll_opy_ (u"࠭ࡡࡱ࡫࠰ࡧࡱࡵࡵࡥࠩ࿔") if bstack1ll1lll_opy_ (u"ࠧࡢࡲࡳࠫ࿕") in CONFIG else bstack1ll1lll_opy_ (u"ࠨࡣࡳ࡭ࠬ࿖")
      user = CONFIG[bstack1ll1lll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ࿗")]
      key = CONFIG[bstack1ll1lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭࿘")]
      bstack1l1l111l1_opy_ = bstack1ll1lll_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪ࿙") if bstack1ll1lll_opy_ (u"ࠬࡧࡰࡱࠩ࿚") in CONFIG else bstack1ll1lll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ࿛")
      url = bstack1ll1lll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡽࢀ࠾ࢀࢃࡀࡼࡿ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠰࡭ࡷࡴࡴࠧ࿜").format(user, key, host, bstack1l1l111l1_opy_)
      if cli.is_enabled(CONFIG):
        bstack1ll1111l11_opy_, hashed_id = cli.bstack1l11llll_opy_()
        logger.info(bstack11lllll1l_opy_.format(bstack1ll1111l11_opy_))
        return [hashed_id, bstack1ll1111l11_opy_]
      else:
        headers = {
          bstack1ll1lll_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧ࿝"): bstack1ll1lll_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬ࿞"),
        }
        if bstack1ll1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ࿟") in CONFIG:
          params = {bstack1ll1lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ࿠"): CONFIG[bstack1ll1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ࿡")], bstack1ll1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ࿢"): CONFIG[bstack1ll1lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ࿣")]}
        else:
          params = {bstack1ll1lll_opy_ (u"ࠨࡰࡤࡱࡪ࠭࿤"): CONFIG[bstack1ll1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ࿥")]}
        proxies = bstack11ll1l111l_opy_(CONFIG, url)
        response = requests.get(url, params=params, headers=headers, proxies=proxies)
        if response.json():
          bstack11l11llll_opy_ = response.json()[0][bstack1ll1lll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡣࡷ࡬ࡰࡩ࠭࿦")]
          if bstack11l11llll_opy_:
            bstack1ll1111l11_opy_ = bstack11l11llll_opy_[bstack1ll1lll_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦࡣࡺࡸ࡬ࠨ࿧")].split(bstack1ll1lll_opy_ (u"ࠬࡶࡵࡣ࡮࡬ࡧ࠲ࡨࡵࡪ࡮ࡧࠫ࿨"))[0] + bstack1ll1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡸ࠵ࠧ࿩") + bstack11l11llll_opy_[
              bstack1ll1lll_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ࿪")]
            logger.info(bstack11lllll1l_opy_.format(bstack1ll1111l11_opy_))
            bstack1ll111l11l_opy_ = bstack11l11llll_opy_[bstack1ll1lll_opy_ (u"ࠨࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ࿫")]
            bstack11l1l1llll_opy_ = CONFIG[bstack1ll1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ࿬")]
            if bstack1ll1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ࿭") in CONFIG:
              bstack11l1l1llll_opy_ += bstack1ll1lll_opy_ (u"ࠫࠥ࠭࿮") + CONFIG[bstack1ll1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ࿯")]
            if bstack11l1l1llll_opy_ != bstack11l11llll_opy_[bstack1ll1lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ࿰")]:
              logger.debug(bstack1lll111l1l_opy_.format(bstack11l11llll_opy_[bstack1ll1lll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ࿱")], bstack11l1l1llll_opy_))
            cli.bstack1111lll11_opy_(bstack1ll1lll_opy_ (u"ࠣࡪࡷࡸࡵࡀࡧࡦࡶࡢࡦࡺ࡯࡬ࡥࡡ࡯࡭ࡳࡱࠢ࿲"), datetime.datetime.now() - bstack1ll1l111l_opy_)
            return [bstack11l11llll_opy_[bstack1ll1lll_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ࿳")], bstack1ll1111l11_opy_]
    else:
      logger.warning(bstack1l1lll1ll_opy_)
  except Exception as e:
    logger.debug(bstack1ll11l1l1l_opy_.format(str(e)))
  return [None, None]
def bstack11l11ll11_opy_(url, bstack1l1111l1ll_opy_=False):
  global CONFIG
  global bstack1111lllll_opy_
  if not bstack1111lllll_opy_:
    hostname = bstack1ll1l1111_opy_(url)
    is_private = bstack1ll1l1l11_opy_(hostname)
    if (bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ࿴") in CONFIG and not bstack11llll111l_opy_(CONFIG[bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ࿵")])) and (is_private or bstack1l1111l1ll_opy_):
      bstack1111lllll_opy_ = hostname
def bstack1ll1l1111_opy_(url):
  return urlparse(url).hostname
def bstack1ll1l1l11_opy_(hostname):
  for bstack1ll1l11l1_opy_ in bstack1llllll11l_opy_:
    regex = re.compile(bstack1ll1l11l1_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack11l11l1l_opy_(bstack111ll11ll_opy_):
  return True if bstack111ll11ll_opy_ in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack1l1ll11l1l_opy_, stage=STAGE.bstack1ll1llll_opy_, bstack1ll1l11l1l_opy_=SESSION_NAME)
def getAccessibilityResults(driver):
  global CONFIG
  global PLATFORM_INDEX
  bstack1ll1l1lll_opy_ = not (bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ࿶"), None) and bstack111l1lll11_opy_(
          threading.current_thread(), bstack1ll1lll_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ࿷"), None))
  bstack111111l11_opy_ = getattr(driver, bstack1ll1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧ࿸"), None) != True
  bstack11111ll1_opy_ = bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ࿹"), None) and bstack111l1lll11_opy_(
          threading.current_thread(), bstack1ll1lll_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ࿺"), None)
  if bstack11111ll1_opy_:
    if not bstack1l111l1l1_opy_():
      logger.warning(bstack1ll1lll_opy_ (u"ࠥࡒࡴࡺࠠࡢࡰࠣࡅࡵࡶࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࠡࡃࡳࡴࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸ࠴ࠢ࿻"))
      return {}
    logger.debug(bstack1ll1lll_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡢࡦࡨࡲࡶࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡳࡧࡶࡹࡱࡺࡳࠨ࿼"))
    logger.debug(perform_scan(driver, driver_command=bstack1ll1lll_opy_ (u"ࠬ࡫ࡸࡦࡥࡸࡸࡪ࡙ࡣࡳ࡫ࡳࡸࠬ࿽")))
    results = bstack11lllllll_opy_(bstack1ll1lll_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹࡹࠢ࿾"))
    if results is not None and results.get(bstack1ll1lll_opy_ (u"ࠢࡪࡵࡶࡹࡪࡹࠢ࿿")) is not None:
        return results[bstack1ll1lll_opy_ (u"ࠣ࡫ࡶࡷࡺ࡫ࡳࠣက")]
    logger.error(bstack1ll1lll_opy_ (u"ࠤࡑࡳࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡘࡥࡴࡷ࡯ࡸࡸࠦࡷࡦࡴࡨࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦခ"))
    return []
  if not a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX) or (bstack111111l11_opy_ and bstack1ll1l1lll_opy_):
    logger.warning(bstack1ll1lll_opy_ (u"ࠥࡒࡴࡺࠠࡢࡰࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷ࠳ࠨဂ"))
    return {}
  try:
    logger.debug(bstack1ll1lll_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡢࡦࡨࡲࡶࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡳࡧࡶࡹࡱࡺࡳࠨဃ"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(accessibility_scripts.get_results)
    return results
  except Exception:
    logger.error(bstack1ll1lll_opy_ (u"ࠧࡔ࡯ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡺࡩࡷ࡫ࠠࡧࡱࡸࡲࡩ࠴ࠢင"))
    return {}
@measure(event_name=EVENTS.bstack1l1ll1l11l_opy_, stage=STAGE.bstack1ll1llll_opy_, bstack1ll1l11l1l_opy_=SESSION_NAME)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global PLATFORM_INDEX
  bstack1ll1l1lll_opy_ = not (bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪစ"), None) and bstack111l1lll11_opy_(
          threading.current_thread(), bstack1ll1lll_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ဆ"), None))
  bstack111111l11_opy_ = getattr(driver, bstack1ll1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨဇ"), None) != True
  bstack11111ll1_opy_ = bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩဈ"), None) and bstack111l1lll11_opy_(
          threading.current_thread(), bstack1ll1lll_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬဉ"), None)
  if bstack11111ll1_opy_:
    if not bstack1l111l1l1_opy_():
      logger.warning(bstack1ll1lll_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡶࡰࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡄࡴࡵࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡴࡷࡰࡱࡦࡸࡹ࠯ࠤည"))
      return {}
    logger.debug(bstack1ll1lll_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡴࡨࡷࡺࡲࡴࡴࠢࡶࡹࡲࡳࡡࡳࡻࠪဋ"))
    logger.debug(perform_scan(driver, driver_command=bstack1ll1lll_opy_ (u"࠭ࡥࡹࡧࡦࡹࡹ࡫ࡓࡤࡴ࡬ࡴࡹ࠭ဌ")))
    results = bstack11lllllll_opy_(bstack1ll1lll_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡓࡶ࡯ࡰࡥࡷࡿࠢဍ"))
    if results is not None and results.get(bstack1ll1lll_opy_ (u"ࠣࡵࡸࡱࡲࡧࡲࡺࠤဎ")) is not None:
        return results[bstack1ll1lll_opy_ (u"ࠤࡶࡹࡲࡳࡡࡳࡻࠥဏ")]
    logger.error(bstack1ll1lll_opy_ (u"ࠥࡒࡴࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡒࡦࡵࡸࡰࡹࡹࠠࡔࡷࡰࡱࡦࡸࡹࠡࡹࡤࡷࠥ࡬࡯ࡶࡰࡧ࠲ࠧတ"))
    return {}
  if not a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX) or (bstack111111l11_opy_ and bstack1ll1l1lll_opy_):
    logger.warning(bstack1ll1lll_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡪࡺࡲࡪࡧࡹࡩࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡳࡶ࡯ࡰࡥࡷࡿ࠮ࠣထ"))
    return {}
  try:
    logger.debug(bstack1ll1lll_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡴࡨࡷࡺࡲࡴࡴࠢࡶࡹࡲࡳࡡࡳࡻࠪဒ"))
    logger.debug(perform_scan(driver))
    bstack111lll111l_opy_ = driver.execute_async_script(accessibility_scripts.get_results_summary)
    return bstack111lll111l_opy_
  except Exception:
    logger.error(bstack1ll1lll_opy_ (u"ࠨࡎࡰࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡹࡲࡳࡡࡳࡻࠣࡻࡦࡹࠠࡧࡱࡸࡲࡩ࠴ࠢဓ"))
    return {}
def bstack1l111l1l1_opy_():
  global CONFIG
  global PLATFORM_INDEX
  bstack1l1lllll11_opy_ = bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧန"), None) and bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪပ"), None)
  if not a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX) or not bstack1l1lllll11_opy_:
        logger.warning(bstack1ll1lll_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡴࡵࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡳࡧࡶࡹࡱࡺࡳ࠯ࠤဖ"))
        return False
  return True
def bstack11lllllll_opy_(result_type):
    bstack11l1l11l1_opy_ = TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack11lll1l11_opy_.current_hook_uuid()
    with ThreadPoolExecutor() as executor:
        future = executor.submit(bstack11l1l1ll11_opy_(bstack11l1l11l1_opy_, result_type))
        try:
            return future.result(timeout=bstack1llll1l1ll_opy_)
        except TimeoutError:
            logger.error(bstack1ll1lll_opy_ (u"ࠥࡘ࡮ࡳࡥࡰࡷࡷࠤࡦ࡬ࡴࡦࡴࠣࡿࢂࡹࠠࡸࡪ࡬ࡰࡪࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡔࡨࡷࡺࡲࡴࡴࠤဗ").format(bstack1llll1l1ll_opy_))
        except Exception as ex:
            logger.debug(bstack1ll1lll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡶࡪࡺࡲࡪࡧࡹ࡭ࡳ࡭ࠠࡂࡲࡳࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡽࢀ࠲ࠥࡋࡲࡳࡱࡵࠤ࠲ࠦࡻࡾࠤဘ").format(result_type, str(ex)))
    return {}
@measure(event_name=EVENTS.bstack11llll1l1_opy_, stage=STAGE.bstack1ll1llll_opy_, bstack1ll1l11l1l_opy_=SESSION_NAME)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global PLATFORM_INDEX
  bstack1ll1l1lll_opy_ = not (bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩမ"), None) and bstack111l1lll11_opy_(
          threading.current_thread(), bstack1ll1lll_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬယ"), None))
  bstack1l111ll11l_opy_ = not (bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧရ"), None) and bstack111l1lll11_opy_(
          threading.current_thread(), bstack1ll1lll_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪလ"), None))
  bstack111111l11_opy_ = getattr(driver, bstack1ll1lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩဝ"), None) != True
  if not a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX) or (bstack111111l11_opy_ and bstack1ll1l1lll_opy_ and bstack1l111ll11l_opy_):
    logger.warning(bstack1ll1lll_opy_ (u"ࠥࡒࡴࡺࠠࡢࡰࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡹࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡤࡣࡱ࠲ࠧသ"))
    return {}
  try:
    bstack1l11lllll1_opy_ = bstack1ll1lll_opy_ (u"ࠫࡦࡶࡰࠨဟ") in CONFIG and CONFIG.get(bstack1ll1lll_opy_ (u"ࠬࡧࡰࡱࠩဠ"), bstack1ll1lll_opy_ (u"࠭ࠧအ"))
    session_id = getattr(driver, bstack1ll1lll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠫဢ"), None)
    if not session_id:
      logger.warning(bstack1ll1lll_opy_ (u"ࠣࡐࡲࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡏࡄࠡࡨࡲࡹࡳࡪࠠࡧࡱࡵࠤࡩࡸࡩࡷࡧࡵࠦဣ"))
      return {bstack1ll1lll_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣဤ"): bstack1ll1lll_opy_ (u"ࠥࡒࡴࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡊࡆࠣࡪࡴࡻ࡮ࡥࠤဥ")}
    if bstack1l11lllll1_opy_:
      try:
        bstack111111l111_opy_ = {
              bstack1ll1lll_opy_ (u"ࠫࡹ࡮ࡊࡸࡶࡗࡳࡰ࡫࡮ࠨဦ"): os.environ.get(bstack1ll1lll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪဧ"), os.environ.get(bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪဨ"), bstack1ll1lll_opy_ (u"ࠧࠨဩ"))),
              bstack1ll1lll_opy_ (u"ࠨࡶ࡫ࡘࡪࡹࡴࡓࡷࡱ࡙ࡺ࡯ࡤࠨဪ"): TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack11lll1l11_opy_.current_hook_uuid(),
              bstack1ll1lll_opy_ (u"ࠩࡤࡹࡹ࡮ࡈࡦࡣࡧࡩࡷ࠭ါ"): os.environ.get(bstack1ll1lll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨာ")),
              bstack1ll1lll_opy_ (u"ࠫࡸࡩࡡ࡯ࡖ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫိ"): str(int(datetime.datetime.now().timestamp() * 1000)),
              bstack1ll1lll_opy_ (u"ࠬࡺࡨࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪီ"): os.environ.get(bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫု"), bstack1ll1lll_opy_ (u"ࠧࠨူ")),
              bstack1ll1lll_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࠨေ"): kwargs.get(bstack1ll1lll_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࡡࡦࡳࡲࡳࡡ࡯ࡦࠪဲ"), None) or bstack1ll1lll_opy_ (u"ࠪࠫဳ")
          }
        if not hasattr(thread_local, bstack1ll1lll_opy_ (u"ࠫࡧࡧࡳࡦࡡࡤࡴࡵࡥࡡ࠲࠳ࡼࡣࡸࡩࡲࡪࡲࡷࠫဴ")):
            scripts = {bstack1ll1lll_opy_ (u"ࠬࡹࡣࡢࡰࠪဵ"): accessibility_scripts.perform_scan}
            thread_local.base_app_a11y_script = scripts
        bstack1ll11l1111_opy_ = copy.deepcopy(thread_local.base_app_a11y_script)
        bstack1ll11l1111_opy_[bstack1ll1lll_opy_ (u"࠭ࡳࡤࡣࡱࠫံ")] = bstack1ll11l1111_opy_[bstack1ll1lll_opy_ (u"ࠧࡴࡥࡤࡲ့ࠬ")] % json.dumps(bstack111111l111_opy_)
        accessibility_scripts.bstack11lll1ll_opy_(bstack1ll11l1111_opy_)
        accessibility_scripts.store()
        bstack1lll1ll11l_opy_ = driver.execute_script(accessibility_scripts.perform_scan)
      except Exception as bstack111l1111l1_opy_:
        logger.info(bstack1ll1lll_opy_ (u"ࠣࡃࡳࡴ࡮ࡻ࡭ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࠣး") + str(bstack111l1111l1_opy_))
        bstack1lll1ll11l_opy_ = {bstack1ll1lll_opy_ (u"ࠤࡨࡶࡷࡵࡲ္ࠣ"): str(bstack111l1111l1_opy_)}
    else:
      bstack1lll1ll11l_opy_ = driver.execute_async_script(accessibility_scripts.perform_scan, {bstack1ll1lll_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦ်ࠪ"): kwargs.get(bstack1ll1lll_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࡣࡨࡵ࡭࡮ࡣࡱࡨࠬျ"), None) or bstack1ll1lll_opy_ (u"ࠬ࠭ြ")})
    return bstack1lll1ll11l_opy_
  except Exception as err:
    logger.error(bstack1ll1lll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡵࡹࡳࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡤࡣࡱ࠲ࠥࢁࡽࠣွ").format(str(err)))
    return {}