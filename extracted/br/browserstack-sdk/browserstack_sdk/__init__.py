# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
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
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import json
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from browserstack_sdk.bstack11l1l11lll_opy_ import bstack1ll1l1l11_opy_
from browserstack_sdk.bstack11l1l1lll_opy_ import *
import time
import requests
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.measure import measure
def bstack1l1l1lllll_opy_():
  global CONFIG
  headers = {
        bstack1ll11ll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack1ll11ll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1llll11lll_opy_(CONFIG, bstack11ll1l11ll_opy_)
  try:
    response = requests.get(bstack11ll1l11ll_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack11l1111lll_opy_ = response.json()[bstack1ll11ll_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack11llll1l1l_opy_.format(response.json()))
      return bstack11l1111lll_opy_
    else:
      logger.debug(bstack1ll11lllll_opy_.format(bstack1ll11ll_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack1ll11lllll_opy_.format(e))
def bstack1l1lll1l11_opy_(hub_url):
  global CONFIG
  url = bstack1ll11ll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack1ll11ll_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack1ll11ll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack1ll11ll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1llll11lll_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1lll111l1l_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack11lll1l1l_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack11lll1ll11_opy_, stage=STAGE.bstack11lll1ll1l_opy_)
def bstack1lllll1lll_opy_():
  try:
    global bstack11lll1lll_opy_
    bstack11l1111lll_opy_ = bstack1l1l1lllll_opy_()
    bstack11llllll_opy_ = []
    results = []
    for bstack1ll1lll111_opy_ in bstack11l1111lll_opy_:
      bstack11llllll_opy_.append(bstack111111111_opy_(target=bstack1l1lll1l11_opy_,args=(bstack1ll1lll111_opy_,)))
    for t in bstack11llllll_opy_:
      t.start()
    for t in bstack11llllll_opy_:
      results.append(t.join())
    bstack1ll11llll1_opy_ = {}
    for item in results:
      hub_url = item[bstack1ll11ll_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack1ll11ll_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack1ll11llll1_opy_[hub_url] = latency
    bstack1ll1ll11l_opy_ = min(bstack1ll11llll1_opy_, key= lambda x: bstack1ll11llll1_opy_[x])
    bstack11lll1lll_opy_ = bstack1ll1ll11l_opy_
    logger.debug(bstack1l1ll1ll_opy_.format(bstack1ll1ll11l_opy_))
  except Exception as e:
    logger.debug(bstack1111l11ll_opy_.format(e))
from browserstack_sdk.bstack11ll1l1l1l_opy_ import *
from browserstack_sdk.bstack1ll111ll1l_opy_ import *
from browserstack_sdk.bstack11l111l11l_opy_ import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.bstack1lll1llll_opy_ import get_logger
from bstack_utils.measure import measure
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack1l1l11ll11_opy_, stage=STAGE.bstack11lll1ll1l_opy_)
def bstack1lllll11_opy_():
    global bstack11lll1lll_opy_
    try:
        bstack1llll1ll1l_opy_ = bstack11ll111111_opy_()
        bstack1l1lll1ll1_opy_(bstack1llll1ll1l_opy_)
        hub_url = bstack1llll1ll1l_opy_.get(bstack1ll11ll_opy_ (u"ࠨࡵࡳ࡮ࠥࢀ"), bstack1ll11ll_opy_ (u"ࠢࠣࢁ"))
        if hub_url.endswith(bstack1ll11ll_opy_ (u"ࠨ࠱ࡺࡨ࠴࡮ࡵࡣࠩࢂ")):
            hub_url = hub_url.rsplit(bstack1ll11ll_opy_ (u"ࠩ࠲ࡻࡩ࠵ࡨࡶࡤࠪࢃ"), 1)[0]
        if hub_url.startswith(bstack1ll11ll_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫࢄ")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack1ll11ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࠭ࢅ")):
            hub_url = hub_url[8:]
        bstack11lll1lll_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack11ll111111_opy_():
    global CONFIG
    bstack11l11l1ll1_opy_ = CONFIG.get(bstack1ll11ll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢆ"), {}).get(bstack1ll11ll_opy_ (u"࠭ࡧࡳ࡫ࡧࡒࡦࡳࡥࠨࢇ"), bstack1ll11ll_opy_ (u"ࠧࡏࡑࡢࡋࡗࡏࡄࡠࡐࡄࡑࡊࡥࡐࡂࡕࡖࡉࡉ࠭࢈"))
    if not isinstance(bstack11l11l1ll1_opy_, str):
        raise ValueError(bstack1ll11ll_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡈࡴ࡬ࡨࠥࡴࡡ࡮ࡧࠣࡱࡺࡹࡴࠡࡤࡨࠤࡦࠦࡶࡢ࡮࡬ࡨࠥࡹࡴࡳ࡫ࡱ࡫ࠧࢉ"))
    try:
        bstack1llll1ll1l_opy_ = bstack1l11llllll_opy_(bstack11l11l1ll1_opy_)
        return bstack1llll1ll1l_opy_
    except Exception as e:
        logger.error(bstack1ll11ll_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣࢊ").format(str(e)))
        return {}
def bstack1l11llllll_opy_(bstack11l11l1ll1_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack1ll11ll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࢋ")] or not CONFIG[bstack1ll11ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧࢌ")]:
            raise ValueError(bstack1ll11ll_opy_ (u"ࠧࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠠࡰࡴࠣࡥࡨࡩࡥࡴࡵࠣ࡯ࡪࡿࠢࢍ"))
        url = bstack11ll1l11l1_opy_ + bstack11l11l1ll1_opy_
        auth = (CONFIG[bstack1ll11ll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨࢎ")], CONFIG[bstack1ll11ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ࢏")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack1ll111l1_opy_ = json.loads(response.text)
            return bstack1ll111l1_opy_
    except ValueError as ve:
        logger.error(bstack1ll11ll_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣ࢐").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack1ll11ll_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥ࡭ࡲࡪࡦࠣࡨࡪࡺࡡࡪ࡮ࡶࠤ࠿ࠦࡻࡾࠤ࢑").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack1l1lll1ll1_opy_(bstack1llll11l1l_opy_):
    global CONFIG
    if bstack1ll11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ࢒") not in CONFIG or str(CONFIG[bstack1ll11ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ࢓")]).lower() == bstack1ll11ll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ࢔"):
        CONFIG[bstack1ll11ll_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬ࢕")] = False
    elif bstack1ll11ll_opy_ (u"ࠧࡪࡵࡗࡶ࡮ࡧ࡬ࡈࡴ࡬ࡨࠬ࢖") in bstack1llll11l1l_opy_:
        bstack1l1ll1ll1l_opy_ = CONFIG.get(bstack1ll11ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢗ"), {})
        logger.debug(bstack1ll11ll_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡰࡴࡩࡡ࡭ࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࠪࡹࠢ࢘"), bstack1l1ll1ll1l_opy_)
        bstack1l11lll1_opy_ = bstack1llll11l1l_opy_.get(bstack1ll11ll_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡕࡩࡵ࡫ࡡࡵࡧࡵࡷ࢙ࠧ"), [])
        bstack1lll11l111_opy_ = bstack1ll11ll_opy_ (u"ࠦ࠱ࠨ࢚").join(bstack1l11lll1_opy_)
        logger.debug(bstack1ll11ll_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡈࡻࡳࡵࡱࡰࠤࡷ࡫ࡰࡦࡣࡷࡩࡷࠦࡳࡵࡴ࡬ࡲ࡬ࡀࠠࠦࡵ࢛ࠥ"), bstack1lll11l111_opy_)
        bstack1ll11l1lll_opy_ = {
            bstack1ll11ll_opy_ (u"ࠨ࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣ࢜"): bstack1ll11ll_opy_ (u"ࠢࡢࡶࡶ࠱ࡷ࡫ࡰࡦࡣࡷࡩࡷࠨ࢝"),
            bstack1ll11ll_opy_ (u"ࠣࡨࡲࡶࡨ࡫ࡌࡰࡥࡤࡰࠧ࢞"): bstack1ll11ll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ࢟"),
            bstack1ll11ll_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠧࢠ"): bstack1lll11l111_opy_
        }
        bstack1l1ll1ll1l_opy_.update(bstack1ll11l1lll_opy_)
        logger.debug(bstack1ll11ll_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼࡙ࠣࡵࡪࡡࡵࡧࡧࠤࡱࡵࡣࡢ࡮ࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࠫࡳࠣࢡ"), bstack1l1ll1ll1l_opy_)
        CONFIG[bstack1ll11ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢢ")] = bstack1l1ll1ll1l_opy_
        logger.debug(bstack1ll11ll_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡌࡩ࡯ࡣ࡯ࠤࡈࡕࡎࡇࡋࡊ࠾ࠥࠫࡳࠣࢣ"), CONFIG)
def bstack11ll1llll_opy_():
    bstack1llll1ll1l_opy_ = bstack11ll111111_opy_()
    if not bstack1llll1ll1l_opy_[bstack1ll11ll_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࡙ࡷࡲࠧࢤ")]:
      raise ValueError(bstack1ll11ll_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࡚ࡸ࡬ࠡ࡫ࡶࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࡬ࡲࡰ࡯ࠣ࡫ࡷ࡯ࡤࠡࡦࡨࡸࡦ࡯࡬ࡴ࠰ࠥࢥ"))
    return bstack1llll1ll1l_opy_[bstack1ll11ll_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࡛ࡲ࡭ࠩࢦ")] + bstack1ll11ll_opy_ (u"ࠪࡃࡨࡧࡰࡴ࠿ࠪࢧ")
@measure(event_name=EVENTS.bstack11lll11ll_opy_, stage=STAGE.bstack11lll1ll1l_opy_)
def bstack1l1ll111ll_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack1ll11ll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ࢨ")], CONFIG[bstack1ll11ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࢩ")])
        url = bstack11llll11ll_opy_
        logger.debug(bstack1ll11ll_opy_ (u"ࠨࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬ࡲࡰ࡯ࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡗࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࠦࡁࡑࡋࠥࢪ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack1ll11ll_opy_ (u"ࠢࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪࠨࢫ"): bstack1ll11ll_opy_ (u"ࠣࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠦࢬ")})
            if response.status_code == 200:
                bstack1ll11l11ll_opy_ = json.loads(response.text)
                bstack11ll11l11l_opy_ = bstack1ll11l11ll_opy_.get(bstack1ll11ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡴࠩࢭ"), [])
                if bstack11ll11l11l_opy_:
                    bstack111ll1l1_opy_ = bstack11ll11l11l_opy_[0]
                    build_hashed_id = bstack111ll1l1_opy_.get(bstack1ll11ll_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ࢮ"))
                    bstack111l1l1l1_opy_ = bstack11l1ll111l_opy_ + build_hashed_id
                    result.extend([build_hashed_id, bstack111l1l1l1_opy_])
                    logger.info(bstack1ll11l1l_opy_.format(bstack111l1l1l1_opy_))
                    bstack11lll1ll_opy_ = CONFIG[bstack1ll11ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧࢯ")]
                    if bstack1ll11ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢰ") in CONFIG:
                      bstack11lll1ll_opy_ += bstack1ll11ll_opy_ (u"࠭ࠠࠨࢱ") + CONFIG[bstack1ll11ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࢲ")]
                    if bstack11lll1ll_opy_ != bstack111ll1l1_opy_.get(bstack1ll11ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ࢳ")):
                      logger.debug(bstack1l11l1l11l_opy_.format(bstack111ll1l1_opy_.get(bstack1ll11ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧࢴ")), bstack11lll1ll_opy_))
                    return result
                else:
                    logger.debug(bstack1ll11ll_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡑࡳࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡵࡪࡨࠤࡷ࡫ࡳࡱࡱࡱࡷࡪ࠴ࠢࢵ"))
            else:
                logger.debug(bstack1ll11ll_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢶ"))
        except Exception as e:
            logger.error(bstack1ll11ll_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࡹࠠ࠻ࠢࡾࢁࠧࢷ").format(str(e)))
    else:
        logger.debug(bstack1ll11ll_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡉࡏࡏࡈࡌࡋࠥ࡯ࡳࠡࡰࡲࡸࠥࡹࡥࡵ࠰࡙ࠣࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢸ"))
    return [None, None]
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1111ll1l_opy_ import bstack1111ll1l_opy_, bstack11l1lll1l_opy_, bstack1ll111l1ll_opy_, bstack1l1llllll_opy_
from bstack_utils.measure import bstack1l1ll11l1l_opy_
from bstack_utils.measure import measure
from bstack_utils.percy import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1l11l111l_opy_ import bstack1l1l111l_opy_
from bstack_utils.messages import *
from bstack_utils import bstack1lll1llll_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1ll1ll1lll_opy_, bstack1lllll1111_opy_, bstack1111lllll_opy_, bstack1111l1l11_opy_, \
  bstack11l1lll1ll_opy_, \
  Notset, bstack1l11l1llll_opy_, \
  bstack1lll1lll1l_opy_, bstack1l111l11ll_opy_, bstack1l11ll1l1_opy_, bstack1l1llll111_opy_, bstack1llll1l11_opy_, bstack111111ll_opy_, \
  bstack11l111l11_opy_, \
  bstack1l111ll111_opy_, bstack11ll11l1l_opy_, bstack1l1l11lll1_opy_, bstack11l11l1l1_opy_, \
  bstack1ll1l11l_opy_, bstack1l1ll1l11l_opy_, bstack1l1l1llll1_opy_, bstack1llll1l1l_opy_
from bstack_utils.bstack1l1lll11l_opy_ import bstack11ll11111_opy_
from bstack_utils.bstack1l11l1l11_opy_ import bstack1l1111l1_opy_, bstack11ll1l1l11_opy_
from bstack_utils.bstack11l11l1l_opy_ import bstack1ll11l11_opy_
from bstack_utils.bstack11l1111111_opy_ import bstack1l11lllll1_opy_, bstack1l11ll11l_opy_
from bstack_utils.bstack1llll111_opy_ import bstack1llll111_opy_
from bstack_utils.bstack11l11111_opy_ import bstack11ll11lll1_opy_
from bstack_utils.proxy import bstack11ll11ll_opy_, bstack1llll11lll_opy_, bstack11l1l1ll1l_opy_, bstack11l11lll1l_opy_
from bstack_utils.bstack11lll1l111_opy_ import bstack111llll11_opy_
import bstack_utils.bstack1l1ll111_opy_ as bstack111llll11l_opy_
import bstack_utils.bstack11l1l111l_opy_ as bstack1ll1l111l_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.utils.bstack11ll1lll11_opy_ import bstack111lll1ll_opy_
from bstack_utils.bstack11l1l11l11_opy_ import bstack1ll1l111_opy_
from bstack_utils.bstack1ll1ll1l11_opy_ import bstack11llll1lll_opy_
if os.getenv(bstack1ll11ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡌࡔࡕࡋࡔࠩࢹ")):
  cli.bstack111l11ll1_opy_()
else:
  os.environ[bstack1ll11ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡍࡕࡏࡌࡕࠪࢺ")] = bstack1ll11ll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧࢻ")
bstack1111l11l_opy_ = bstack1ll11ll_opy_ (u"ࠪࠤࠥ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࠣࠤ࡮࡬ࠨࡱࡣࡪࡩࠥࡃ࠽࠾ࠢࡹࡳ࡮ࡪࠠ࠱ࠫࠣࡿࡡࡴࠠࠡࠢࡷࡶࡾࢁ࡜࡯ࠢࡦࡳࡳࡹࡴࠡࡨࡶࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨ࡝ࠩࡩࡷࡡ࠭ࠩ࠼࡞ࡱࠤࠥࠦࠠࠡࡨࡶ࠲ࡦࡶࡰࡦࡰࡧࡊ࡮ࡲࡥࡔࡻࡱࡧ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪ࠯ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡶ࡟ࡪࡰࡧࡩࡽ࠯ࠠࠬࠢࠥ࠾ࠧࠦࠫࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࠨࡢࡹࡤ࡭ࡹࠦ࡮ࡦࡹࡓࡥ࡬࡫࠲࠯ࡧࡹࡥࡱࡻࡡࡵࡧࠫࠦ࠭࠯ࠠ࠾ࡀࠣࡿࢂࠨࠬࠡ࡞ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥ࡫ࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡄࡦࡶࡤ࡭ࡱࡹࠢࡾ࡞ࠪ࠭࠮࠯࡛ࠣࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠦࡢ࠯ࠠࠬࠢࠥ࠰ࡡࡢ࡮ࠣࠫ࡟ࡲࠥࠦࠠࠡࡿࡦࡥࡹࡩࡨࠩࡧࡻ࠭ࢀࡢ࡮ࠡࠢࠣࠤࢂࡢ࡮ࠡࠢࢀࡠࡳࠦࠠ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱ࠪࢼ")
bstack1l11l111l1_opy_ = bstack1ll11ll_opy_ (u"ࠫࡡࡴ࠯ࠫࠢࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࠦࠪ࠰࡞ࡱࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠶ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡩࡡࡱࡵࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠷࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡲࡢ࡭ࡳࡪࡥࡹࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠷ࡣ࡜࡯ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯ࡵ࡯࡭ࡨ࡫ࠨ࠱࠮ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸࠯࡜࡯ࡥࡲࡲࡸࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯ࠥࡃࠠࡳࡧࡴࡹ࡮ࡸࡥࠩࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨࠩ࠼࡞ࡱ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡰࡦࡻ࡮ࡤࡪࠣࡁࠥࡧࡳࡺࡰࡦࠤ࠭ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷ࠮ࠦ࠽࠿ࠢࡾࡠࡳࡲࡥࡵࠢࡦࡥࡵࡹ࠻࡝ࡰࡷࡶࡾࠦࡻ࡝ࡰࡦࡥࡵࡹࠠ࠾ࠢࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࡢࡴࡶࡤࡧࡰࡥࡣࡢࡲࡶ࠭ࡡࡴࠠࠡࡿࠣࡧࡦࡺࡣࡩࠪࡨࡼ࠮ࠦࡻ࡝ࡰࠣࠤࠥࠦࡽ࡝ࡰࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࠻ࠢࡣࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠩࢁࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭ࢂࡦࠬ࡝ࡰࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴ࡞ࡱࠤࠥࢃࠩ࡝ࡰࢀࡠࡳ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࠪࢽ")
from ._version import __version__
bstack111l11lll_opy_ = None
CONFIG = {}
bstack1l111lllll_opy_ = {}
bstack1ll111llll_opy_ = {}
bstack1ll1111ll1_opy_ = None
bstack1l1l1l1l1_opy_ = None
bstack111l1l11_opy_ = None
bstack11l111lll_opy_ = -1
bstack11ll1lllll_opy_ = 0
bstack11l111l111_opy_ = bstack1ll1l1lll_opy_
bstack11l11ll1_opy_ = 1
bstack111llll1ll_opy_ = False
bstack111llll1l1_opy_ = False
bstack11l1lll1l1_opy_ = bstack1ll11ll_opy_ (u"ࠬ࠭ࢾ")
bstack1lll11lll1_opy_ = bstack1ll11ll_opy_ (u"࠭ࠧࢿ")
bstack1l1lll1l1l_opy_ = False
bstack11l1ll11l_opy_ = True
bstack11ll1111_opy_ = bstack1ll11ll_opy_ (u"ࠧࠨࣀ")
bstack1lll1ll1l1_opy_ = []
bstack11ll111l_opy_ = threading.Lock()
bstack11l11ll111_opy_ = threading.Lock()
bstack11lll1lll_opy_ = bstack1ll11ll_opy_ (u"ࠨࠩࣁ")
bstack1l1l1lll1_opy_ = False
bstack1ll11111l_opy_ = None
bstack1l1l1ll11l_opy_ = None
bstack1ll1l1ll11_opy_ = None
bstack1l1lll1l_opy_ = -1
bstack11ll11l1l1_opy_ = os.path.join(os.path.expanduser(bstack1ll11ll_opy_ (u"ࠩࢁࠫࣂ")), bstack1ll11ll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪࣃ"), bstack1ll11ll_opy_ (u"ࠫ࠳ࡸ࡯ࡣࡱࡷ࠱ࡷ࡫ࡰࡰࡴࡷ࠱࡭࡫࡬ࡱࡧࡵ࠲࡯ࡹ࡯࡯ࠩࣄ"))
bstack1111111l1_opy_ = 0
bstack11l1l1l11_opy_ = 0
bstack1l111l1l11_opy_ = []
bstack11l1l1lll1_opy_ = []
bstack1ll1111l1_opy_ = []
bstack1l111lll_opy_ = []
bstack1l1lll1lll_opy_ = bstack1ll11ll_opy_ (u"ࠬ࠭ࣅ")
bstack11lll11111_opy_ = bstack1ll11ll_opy_ (u"࠭ࠧࣆ")
bstack11l1111ll_opy_ = False
bstack11llll11_opy_ = False
bstack11l11l11l1_opy_ = {}
bstack1lll11ll11_opy_ = None
bstack11l1111l1l_opy_ = None
bstack111111ll1_opy_ = None
bstack1lll1ll11l_opy_ = None
bstack1l111l111_opy_ = None
bstack11l1llll1_opy_ = None
bstack11l1l1l1l_opy_ = None
bstack1llllllll_opy_ = None
bstack1l11l11111_opy_ = None
bstack1lll111l1_opy_ = None
bstack1lllll1l11_opy_ = None
bstack111lllll11_opy_ = None
bstack1l1llllll1_opy_ = None
bstack111l11l1l_opy_ = None
bstack11l1111ll1_opy_ = None
bstack1ll1ll1111_opy_ = None
bstack11ll111lll_opy_ = None
bstack1l11ll1111_opy_ = None
bstack1lll111111_opy_ = None
bstack1ll1llll1_opy_ = None
bstack1lll11ll1_opy_ = None
bstack11l1l111_opy_ = None
bstack1ll1l1111l_opy_ = None
thread_local = threading.local()
bstack1111l111l_opy_ = False
bstack111l11l1_opy_ = bstack1ll11ll_opy_ (u"ࠢࠣࣇ")
logger = bstack1lll1llll_opy_.get_logger(__name__, bstack11l111l111_opy_)
bstack1l111111l1_opy_ = Config.bstack11l11lllll_opy_()
percy = bstack11ll1l1111_opy_()
bstack11ll1111l_opy_ = bstack1l1l111l_opy_()
bstack1l11ll1lll_opy_ = bstack11l111l11l_opy_()
def bstack1lllll1l1_opy_():
  global CONFIG
  global bstack11l1111ll_opy_
  global bstack1l111111l1_opy_
  testContextOptions = bstack1111l1l1_opy_(CONFIG)
  if bstack11l1lll1ll_opy_(CONFIG):
    if (bstack1ll11ll_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪࣈ") in testContextOptions and str(testContextOptions[bstack1ll11ll_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫࣉ")]).lower() == bstack1ll11ll_opy_ (u"ࠪࡸࡷࡻࡥࠨ࣊")):
      bstack11l1111ll_opy_ = True
    bstack1l111111l1_opy_.bstack11ll111ll1_opy_(testContextOptions.get(bstack1ll11ll_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ࣋"), False))
  else:
    bstack11l1111ll_opy_ = True
    bstack1l111111l1_opy_.bstack11ll111ll1_opy_(True)
def bstack1lllll1l1l_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1l11111111_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack11l1lll11l_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1ll11ll_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡩ࡯࡯ࡨ࡬࡫࡫࡯࡬ࡦࠤ࣌") == args[i].lower() or bstack1ll11ll_opy_ (u"ࠨ࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡪ࡮࡭ࠢ࣍") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack11ll1111_opy_
      bstack11ll1111_opy_ += bstack1ll11ll_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠤࠬ࣎") + shlex.quote(path)
      return path
  return None
bstack1ll111l1l1_opy_ = re.compile(bstack1ll11ll_opy_ (u"ࡳࠤ࠱࠮ࡄࡢࠤࡼࠪ࠱࠮ࡄ࠯ࡽ࠯ࠬࡂ࣏ࠦ"))
def bstack11111ll11_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1ll111l1l1_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack1ll11ll_opy_ (u"ࠤࠧࡿ࣐ࠧ") + group + bstack1ll11ll_opy_ (u"ࠥࢁ࣑ࠧ"), os.environ.get(group))
  return value
def bstack1l1l1l1ll1_opy_():
  global bstack1ll1l1111l_opy_
  if bstack1ll1l1111l_opy_ is None:
        bstack1ll1l1111l_opy_ = bstack11l1lll11l_opy_()
  bstack11ll1ll1l1_opy_ = bstack1ll1l1111l_opy_
  if bstack11ll1ll1l1_opy_ and os.path.exists(os.path.abspath(bstack11ll1ll1l1_opy_)):
    fileName = bstack11ll1ll1l1_opy_
  if bstack1ll11ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ࣒") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack1ll11ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆ࣓ࠩ")])) and not bstack1ll11ll_opy_ (u"࠭ࡦࡪ࡮ࡨࡒࡦࡳࡥࠨࣔ") in locals():
    fileName = os.environ[bstack1ll11ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫࣕ")]
  if bstack1ll11ll_opy_ (u"ࠨࡨ࡬ࡰࡪࡔࡡ࡮ࡧࠪࣖ") in locals():
    bstack11l111l_opy_ = os.path.abspath(fileName)
  else:
    bstack11l111l_opy_ = bstack1ll11ll_opy_ (u"ࠩࠪࣗ")
  bstack111lllll1_opy_ = os.getcwd()
  bstack1l11l1l1ll_opy_ = bstack1ll11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ࣘ")
  bstack111l11l11_opy_ = bstack1ll11ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡦࡳ࡬ࠨࣙ")
  while (not os.path.exists(bstack11l111l_opy_)) and bstack111lllll1_opy_ != bstack1ll11ll_opy_ (u"ࠧࠨࣚ"):
    bstack11l111l_opy_ = os.path.join(bstack111lllll1_opy_, bstack1l11l1l1ll_opy_)
    if not os.path.exists(bstack11l111l_opy_):
      bstack11l111l_opy_ = os.path.join(bstack111lllll1_opy_, bstack111l11l11_opy_)
    if bstack111lllll1_opy_ != os.path.dirname(bstack111lllll1_opy_):
      bstack111lllll1_opy_ = os.path.dirname(bstack111lllll1_opy_)
    else:
      bstack111lllll1_opy_ = bstack1ll11ll_opy_ (u"ࠨࠢࣛ")
  bstack1ll1l1111l_opy_ = bstack11l111l_opy_ if os.path.exists(bstack11l111l_opy_) else None
  return bstack1ll1l1111l_opy_
def bstack11l111111_opy_(config):
    if bstack1ll11ll_opy_ (u"ࠧࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭ࠧࣜ") in config:
      config[bstack1ll11ll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬࣝ")] = config[bstack1ll11ll_opy_ (u"ࠩࡷࡩࡸࡺࡒࡦࡲࡲࡶࡹ࡯࡮ࡨࠩࣞ")]
    if bstack1ll11ll_opy_ (u"ࠪࡸࡪࡹࡴࡓࡧࡳࡳࡷࡺࡩ࡯ࡩࡒࡴࡹ࡯࡯࡯ࡵࠪࣟ") in config:
      config[bstack1ll11ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ࣠")] = config[bstack1ll11ll_opy_ (u"ࠬࡺࡥࡴࡶࡕࡩࡵࡵࡲࡵ࡫ࡱ࡫ࡔࡶࡴࡪࡱࡱࡷࠬ࣡")]
def bstack1l111ll1ll_opy_():
  bstack11l111l_opy_ = bstack1l1l1l1ll1_opy_()
  if not os.path.exists(bstack11l111l_opy_):
    bstack1l1111111l_opy_(
      bstack11ll11llll_opy_.format(os.getcwd()))
  try:
    with open(bstack11l111l_opy_, bstack1ll11ll_opy_ (u"࠭ࡲࠨ࣢")) as stream:
      yaml.add_implicit_resolver(bstack1ll11ll_opy_ (u"ࠢࠢࡲࡤࡸ࡭࡫ࡸࣣࠣ"), bstack1ll111l1l1_opy_)
      yaml.add_constructor(bstack1ll11ll_opy_ (u"ࠣࠣࡳࡥࡹ࡮ࡥࡹࠤࣤ"), bstack11111ll11_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      bstack11l111111_opy_(config)
      return config
  except:
    with open(bstack11l111l_opy_, bstack1ll11ll_opy_ (u"ࠩࡵࠫࣥ")) as stream:
      try:
        config = yaml.safe_load(stream)
        bstack11l111111_opy_(config)
        return config
      except yaml.YAMLError as exc:
        bstack1l1111111l_opy_(bstack11lllll1_opy_.format(str(exc)))
def bstack11l1ll1l1_opy_(config):
  bstack11llllll11_opy_ = bstack1l1lll111_opy_(config)
  for option in list(bstack11llllll11_opy_):
    if option.lower() in bstack1ll11llll_opy_ and option != bstack1ll11llll_opy_[option.lower()]:
      bstack11llllll11_opy_[bstack1ll11llll_opy_[option.lower()]] = bstack11llllll11_opy_[option]
      del bstack11llllll11_opy_[option]
  return config
def bstack11l1l1ll1_opy_():
  global bstack1ll111llll_opy_
  for key, bstack1ll1l11ll_opy_ in bstack11lll1l1l1_opy_.items():
    if isinstance(bstack1ll1l11ll_opy_, list):
      for var in bstack1ll1l11ll_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1ll111llll_opy_[key] = os.environ[var]
          break
    elif bstack1ll1l11ll_opy_ in os.environ and os.environ[bstack1ll1l11ll_opy_] and str(os.environ[bstack1ll1l11ll_opy_]).strip():
      bstack1ll111llll_opy_[key] = os.environ[bstack1ll1l11ll_opy_]
  if bstack1ll11ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࣦࠬ") in os.environ:
    bstack1ll111llll_opy_[bstack1ll11ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣧ")] = {}
    bstack1ll111llll_opy_[bstack1ll11ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣨ")][bstack1ll11ll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣩ")] = os.environ[bstack1ll11ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩ࣪")]
def bstack1lll1ll1_opy_():
  global bstack1l111lllll_opy_
  global bstack11ll1111_opy_
  bstack1l11111l1_opy_ = []
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) - 1 and bstack1ll11ll_opy_ (u"ࠨ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ࣫").lower() == val.lower():
      bstack1l111lllll_opy_[bstack1ll11ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭࣬")] = {}
      bstack1l111lllll_opy_[bstack1ll11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹ࣭ࠧ")][bstack1ll11ll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࣮࠭")] = sys.argv[idx + 1]
      bstack1l11111l1_opy_.extend([idx, idx + 1])
      break
  for key, bstack1lllll111_opy_ in bstack11ll1lll1l_opy_.items():
    if isinstance(bstack1lllll111_opy_, list):
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        for var in bstack1lllll111_opy_:
          if bstack1ll11ll_opy_ (u"ࠬ࠳࠭ࠨ࣯") + var.lower() == val.lower() and key not in bstack1l111lllll_opy_:
            bstack1l111lllll_opy_[key] = sys.argv[idx + 1]
            bstack11ll1111_opy_ += bstack1ll11ll_opy_ (u"࠭ࠠ࠮࠯ࣰࠪ") + var + bstack1ll11ll_opy_ (u"ࣱࠧࠡࠩ") + shlex.quote(sys.argv[idx + 1])
            bstack1l11111l1_opy_.extend([idx, idx + 1])
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        if bstack1ll11ll_opy_ (u"ࠨ࠯࠰ࣲࠫ") + bstack1lllll111_opy_.lower() == val.lower() and key not in bstack1l111lllll_opy_:
          bstack1l111lllll_opy_[key] = sys.argv[idx + 1]
          bstack11ll1111_opy_ += bstack1ll11ll_opy_ (u"ࠩࠣ࠱࠲࠭ࣳ") + bstack1lllll111_opy_ + bstack1ll11ll_opy_ (u"ࠪࠤࠬࣴ") + shlex.quote(sys.argv[idx + 1])
          bstack1l11111l1_opy_.extend([idx, idx + 1])
  for idx in sorted(set(bstack1l11111l1_opy_), reverse=True):
    if idx < len(sys.argv):
      del sys.argv[idx]
def bstack1lll11l1l_opy_(config):
  bstack11l111ll_opy_ = config.keys()
  for bstack1llll1l1ll_opy_, bstack11l11lll11_opy_ in bstack1ll1l1111_opy_.items():
    if bstack11l11lll11_opy_ in bstack11l111ll_opy_:
      config[bstack1llll1l1ll_opy_] = config[bstack11l11lll11_opy_]
      del config[bstack11l11lll11_opy_]
  for bstack1llll1l1ll_opy_, bstack11l11lll11_opy_ in bstack1l11l11lll_opy_.items():
    if isinstance(bstack11l11lll11_opy_, list):
      for bstack1lll1111_opy_ in bstack11l11lll11_opy_:
        if bstack1lll1111_opy_ in bstack11l111ll_opy_:
          config[bstack1llll1l1ll_opy_] = config[bstack1lll1111_opy_]
          del config[bstack1lll1111_opy_]
          break
    elif bstack11l11lll11_opy_ in bstack11l111ll_opy_:
      config[bstack1llll1l1ll_opy_] = config[bstack11l11lll11_opy_]
      del config[bstack11l11lll11_opy_]
  for bstack1lll1111_opy_ in list(config):
    for bstack1l11l1l1l1_opy_ in bstack1ll111l111_opy_:
      if bstack1lll1111_opy_.lower() == bstack1l11l1l1l1_opy_.lower() and bstack1lll1111_opy_ != bstack1l11l1l1l1_opy_:
        config[bstack1l11l1l1l1_opy_] = config[bstack1lll1111_opy_]
        del config[bstack1lll1111_opy_]
  bstack11l111lll1_opy_ = [{}]
  if not config.get(bstack1ll11ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣵ")):
    config[bstack1ll11ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨࣶ")] = [{}]
  bstack11l111lll1_opy_ = config[bstack1ll11ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩࣷ")]
  for platform in bstack11l111lll1_opy_:
    for bstack1lll1111_opy_ in list(platform):
      for bstack1l11l1l1l1_opy_ in bstack1ll111l111_opy_:
        if bstack1lll1111_opy_.lower() == bstack1l11l1l1l1_opy_.lower() and bstack1lll1111_opy_ != bstack1l11l1l1l1_opy_:
          platform[bstack1l11l1l1l1_opy_] = platform[bstack1lll1111_opy_]
          del platform[bstack1lll1111_opy_]
  for bstack1llll1l1ll_opy_, bstack11l11lll11_opy_ in bstack1l11l11lll_opy_.items():
    for platform in bstack11l111lll1_opy_:
      if isinstance(bstack11l11lll11_opy_, list):
        for bstack1lll1111_opy_ in bstack11l11lll11_opy_:
          if bstack1lll1111_opy_ in platform:
            platform[bstack1llll1l1ll_opy_] = platform[bstack1lll1111_opy_]
            del platform[bstack1lll1111_opy_]
            break
      elif bstack11l11lll11_opy_ in platform:
        platform[bstack1llll1l1ll_opy_] = platform[bstack11l11lll11_opy_]
        del platform[bstack11l11lll11_opy_]
  for bstack1lllll111l_opy_ in bstack11ll1l1ll_opy_:
    if bstack1lllll111l_opy_ in config:
      if not bstack11ll1l1ll_opy_[bstack1lllll111l_opy_] in config:
        config[bstack11ll1l1ll_opy_[bstack1lllll111l_opy_]] = {}
      config[bstack11ll1l1ll_opy_[bstack1lllll111l_opy_]].update(config[bstack1lllll111l_opy_])
      del config[bstack1lllll111l_opy_]
  for platform in bstack11l111lll1_opy_:
    for bstack1lllll111l_opy_ in bstack11ll1l1ll_opy_:
      if bstack1lllll111l_opy_ in list(platform):
        if not bstack11ll1l1ll_opy_[bstack1lllll111l_opy_] in platform:
          platform[bstack11ll1l1ll_opy_[bstack1lllll111l_opy_]] = {}
        platform[bstack11ll1l1ll_opy_[bstack1lllll111l_opy_]].update(platform[bstack1lllll111l_opy_])
        del platform[bstack1lllll111l_opy_]
  config = bstack11l1ll1l1_opy_(config)
  return config
def bstack1lll11l1l1_opy_(config):
  global bstack1lll11lll1_opy_
  bstack1l11111l11_opy_ = False
  if bstack1ll11ll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫࣸ") in config and str(config[bstack1ll11ll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࣹࠬ")]).lower() != bstack1ll11ll_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨࣺ"):
    if bstack1ll11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧࣻ") not in config or str(config[bstack1ll11ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨࣼ")]).lower() == bstack1ll11ll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫࣽ"):
      config[bstack1ll11ll_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬࣾ")] = False
    else:
      bstack1llll1ll1l_opy_ = bstack11ll111111_opy_()
      if bstack1ll11ll_opy_ (u"ࠧࡪࡵࡗࡶ࡮ࡧ࡬ࡈࡴ࡬ࡨࠬࣿ") in bstack1llll1ll1l_opy_:
        if not bstack1ll11ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬऀ") in config:
          config[bstack1ll11ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ँ")] = {}
        config[bstack1ll11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧं")][bstack1ll11ll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ः")] = bstack1ll11ll_opy_ (u"ࠬࡧࡴࡴ࠯ࡵࡩࡵ࡫ࡡࡵࡧࡵࠫऄ")
        bstack1l11111l11_opy_ = True
        bstack1lll11lll1_opy_ = config[bstack1ll11ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪअ")].get(bstack1ll11ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩआ"))
  if bstack11l1lll1ll_opy_(config) and bstack1ll11ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬइ") in config and str(config[bstack1ll11ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ई")]).lower() != bstack1ll11ll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩउ") and not bstack1l11111l11_opy_:
    if not bstack1ll11ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऊ") in config:
      config[bstack1ll11ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩऋ")] = {}
    if not config[bstack1ll11ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪऌ")].get(bstack1ll11ll_opy_ (u"ࠧࡴ࡭࡬ࡴࡇ࡯࡮ࡢࡴࡼࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡸࡧࡴࡪࡱࡱࠫऍ")) and not bstack1ll11ll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪऎ") in config[bstack1ll11ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ए")]:
      bstack11l1l1l1l1_opy_ = datetime.datetime.now()
      bstack1lll111l11_opy_ = bstack11l1l1l1l1_opy_.strftime(bstack1ll11ll_opy_ (u"ࠪࠩࡩࡥࠥࡣࡡࠨࡌࠪࡓࠧऐ"))
      hostname = socket.gethostname()
      bstack1l1l11ll_opy_ = bstack1ll11ll_opy_ (u"ࠫࠬऑ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1ll11ll_opy_ (u"ࠬࢁࡽࡠࡽࢀࡣࢀࢃࠧऒ").format(bstack1lll111l11_opy_, hostname, bstack1l1l11ll_opy_)
      config[bstack1ll11ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪओ")][bstack1ll11ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऔ")] = identifier
    bstack1lll11lll1_opy_ = config[bstack1ll11ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬक")].get(bstack1ll11ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫख"))
  return config
def bstack1l111ll11_opy_():
  bstack1l1l1l1111_opy_ =  bstack1l1llll111_opy_()[bstack1ll11ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠩग")]
  return bstack1l1l1l1111_opy_ if bstack1l1l1l1111_opy_ else -1
def bstack1l11lll1l_opy_(bstack1l1l1l1111_opy_):
  global CONFIG
  if not bstack1ll11ll_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭घ") in CONFIG[bstack1ll11ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧङ")]:
    return
  CONFIG[bstack1ll11ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨच")] = CONFIG[bstack1ll11ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩछ")].replace(
    bstack1ll11ll_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪज"),
    str(bstack1l1l1l1111_opy_)
  )
def bstack11l1ll1l11_opy_():
  global CONFIG
  if not bstack1ll11ll_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨझ") in CONFIG[bstack1ll11ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬञ")]:
    return
  bstack11l1l1l1l1_opy_ = datetime.datetime.now()
  bstack1lll111l11_opy_ = bstack11l1l1l1l1_opy_.strftime(bstack1ll11ll_opy_ (u"ࠫࠪࡪ࠭ࠦࡤ࠰ࠩࡍࡀࠥࡎࠩट"))
  CONFIG[bstack1ll11ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧठ")] = CONFIG[bstack1ll11ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨड")].replace(
    bstack1ll11ll_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭ढ"),
    bstack1lll111l11_opy_
  )
def bstack1l111111ll_opy_():
  global CONFIG
  if bstack1ll11ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪण") in CONFIG and not bool(CONFIG[bstack1ll11ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫत")]):
    del CONFIG[bstack1ll11ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬथ")]
    return
  if not bstack1ll11ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭द") in CONFIG:
    CONFIG[bstack1ll11ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧध")] = bstack1ll11ll_opy_ (u"࠭ࠣࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩन")
  if bstack1ll11ll_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭ऩ") in CONFIG[bstack1ll11ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪप")]:
    bstack11l1ll1l11_opy_()
    os.environ[bstack1ll11ll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭फ")] = CONFIG[bstack1ll11ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬब")]
  if not bstack1ll11ll_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭भ") in CONFIG[bstack1ll11ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧम")]:
    return
  bstack1l1l1l1111_opy_ = bstack1ll11ll_opy_ (u"࠭ࠧय")
  bstack11l1lllll1_opy_ = bstack1l111ll11_opy_()
  if bstack11l1lllll1_opy_ != -1:
    bstack1l1l1l1111_opy_ = bstack1ll11ll_opy_ (u"ࠧࡄࡋࠣࠫर") + str(bstack11l1lllll1_opy_)
  if bstack1l1l1l1111_opy_ == bstack1ll11ll_opy_ (u"ࠨࠩऱ"):
    bstack1l11l1111l_opy_ = bstack11l1l1llll_opy_(CONFIG[bstack1ll11ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬल")])
    if bstack1l11l1111l_opy_ != -1:
      bstack1l1l1l1111_opy_ = str(bstack1l11l1111l_opy_)
  if bstack1l1l1l1111_opy_:
    bstack1l11lll1l_opy_(bstack1l1l1l1111_opy_)
    os.environ[bstack1ll11ll_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧळ")] = CONFIG[bstack1ll11ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ऴ")]
def bstack11111l1ll_opy_(bstack1ll111lll1_opy_, bstack1l1ll11ll1_opy_, path):
  bstack1l1lllll1_opy_ = {
    bstack1ll11ll_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩव"): bstack1l1ll11ll1_opy_
  }
  if os.path.exists(path):
    bstack111l111l1_opy_ = json.load(open(path, bstack1ll11ll_opy_ (u"࠭ࡲࡣࠩश")))
  else:
    bstack111l111l1_opy_ = {}
  bstack111l111l1_opy_[bstack1ll111lll1_opy_] = bstack1l1lllll1_opy_
  with open(path, bstack1ll11ll_opy_ (u"ࠢࡸ࠭ࠥष")) as outfile:
    json.dump(bstack111l111l1_opy_, outfile)
def bstack11l1l1llll_opy_(bstack1ll111lll1_opy_):
  bstack1ll111lll1_opy_ = str(bstack1ll111lll1_opy_)
  bstack1l1111lll1_opy_ = os.path.join(os.path.expanduser(bstack1ll11ll_opy_ (u"ࠨࢀࠪस")), bstack1ll11ll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩह"))
  try:
    if not os.path.exists(bstack1l1111lll1_opy_):
      os.makedirs(bstack1l1111lll1_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1ll11ll_opy_ (u"ࠪࢂࠬऺ")), bstack1ll11ll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫऻ"), bstack1ll11ll_opy_ (u"ࠬ࠴ࡢࡶ࡫࡯ࡨ࠲ࡴࡡ࡮ࡧ࠰ࡧࡦࡩࡨࡦ࠰࡭ࡷࡴࡴ़ࠧ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1ll11ll_opy_ (u"࠭ࡷࠨऽ")):
        pass
      with open(file_path, bstack1ll11ll_opy_ (u"ࠢࡸ࠭ࠥा")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1ll11ll_opy_ (u"ࠨࡴࠪि")) as bstack1l11ll11_opy_:
      bstack1l1l1l1lll_opy_ = json.load(bstack1l11ll11_opy_)
    if bstack1ll111lll1_opy_ in bstack1l1l1l1lll_opy_:
      bstack1l111ll1_opy_ = bstack1l1l1l1lll_opy_[bstack1ll111lll1_opy_][bstack1ll11ll_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ी")]
      bstack1l11ll11ll_opy_ = int(bstack1l111ll1_opy_) + 1
      bstack11111l1ll_opy_(bstack1ll111lll1_opy_, bstack1l11ll11ll_opy_, file_path)
      return bstack1l11ll11ll_opy_
    else:
      bstack11111l1ll_opy_(bstack1ll111lll1_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1l11l111ll_opy_.format(str(e)))
    return -1
def bstack1l1llll11l_opy_(config):
  if not config[bstack1ll11ll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬु")] or not config[bstack1ll11ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧू")]:
    return True
  else:
    return False
def bstack1l1llll1l_opy_(config, index=0):
  global bstack1l1lll1l1l_opy_
  bstack1l1l11l11l_opy_ = {}
  caps = bstack1llllllll1_opy_ + bstack1l1l11l111_opy_
  if config.get(bstack1ll11ll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩृ"), False):
    bstack1l1l11l11l_opy_[bstack1ll11ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪॄ")] = True
    bstack1l1l11l11l_opy_[bstack1ll11ll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࡓࡵࡺࡩࡰࡰࡶࠫॅ")] = config.get(bstack1ll11ll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࡔࡶࡴࡪࡱࡱࡷࠬॆ"), {})
  if bstack1l1lll1l1l_opy_:
    caps += bstack1l11llll1l_opy_
  for key in config:
    if key in caps + [bstack1ll11ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬे")]:
      continue
    bstack1l1l11l11l_opy_[key] = config[key]
  if bstack1ll11ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ै") in config:
    for bstack1l1l1lll11_opy_ in config[bstack1ll11ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॉ")][index]:
      if bstack1l1l1lll11_opy_ in caps:
        continue
      bstack1l1l11l11l_opy_[bstack1l1l1lll11_opy_] = config[bstack1ll11ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨॊ")][index][bstack1l1l1lll11_opy_]
  bstack1l1l11l11l_opy_[bstack1ll11ll_opy_ (u"࠭ࡨࡰࡵࡷࡒࡦࡳࡥࠨो")] = socket.gethostname()
  if bstack1ll11ll_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨौ") in bstack1l1l11l11l_opy_:
    del (bstack1l1l11l11l_opy_[bstack1ll11ll_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯्ࠩ")])
  return bstack1l1l11l11l_opy_
def bstack11111l1l1_opy_(config):
  global bstack1l1lll1l1l_opy_
  bstack1llll1l1_opy_ = {}
  caps = bstack1l1l11l111_opy_
  if bstack1l1lll1l1l_opy_:
    caps += bstack1l11llll1l_opy_
  for key in caps:
    if key in config:
      bstack1llll1l1_opy_[key] = config[key]
  return bstack1llll1l1_opy_
def bstack111lll1l1_opy_(bstack1l1l11l11l_opy_, bstack1llll1l1_opy_):
  bstack1l111ll1l_opy_ = {}
  for key in bstack1l1l11l11l_opy_.keys():
    if key in bstack1ll1l1111_opy_:
      bstack1l111ll1l_opy_[bstack1ll1l1111_opy_[key]] = bstack1l1l11l11l_opy_[key]
    else:
      bstack1l111ll1l_opy_[key] = bstack1l1l11l11l_opy_[key]
  for key in bstack1llll1l1_opy_:
    if key in bstack1ll1l1111_opy_:
      bstack1l111ll1l_opy_[bstack1ll1l1111_opy_[key]] = bstack1llll1l1_opy_[key]
    else:
      bstack1l111ll1l_opy_[key] = bstack1llll1l1_opy_[key]
  return bstack1l111ll1l_opy_
def bstack11lllllll_opy_(config, index=0):
  global bstack1l1lll1l1l_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack1l111lll11_opy_ = bstack1ll1ll1lll_opy_(bstack1lll1l1lll_opy_, config, logger)
  bstack1llll1l1_opy_ = bstack11111l1l1_opy_(config)
  bstack1l1l11l1_opy_ = bstack1l1l11l111_opy_
  bstack1l1l11l1_opy_ += bstack1111l1ll1_opy_
  bstack1llll1l1_opy_ = update(bstack1llll1l1_opy_, bstack1l111lll11_opy_)
  if bstack1l1lll1l1l_opy_:
    bstack1l1l11l1_opy_ += bstack1l11llll1l_opy_
  if bstack1ll11ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॎ") in config:
    if bstack1ll11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨॏ") in config[bstack1ll11ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॐ")][index]:
      caps[bstack1ll11ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ॑")] = config[bstack1ll11ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴ॒ࠩ")][index][bstack1ll11ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ॓")]
    if bstack1ll11ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ॔") in config[bstack1ll11ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॕ")][index]:
      caps[bstack1ll11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫॖ")] = str(config[bstack1ll11ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॗ")][index][bstack1ll11ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭क़")])
    bstack1l1111l1l1_opy_ = bstack1ll1ll1lll_opy_(bstack1lll1l1lll_opy_, config[bstack1ll11ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩख़")][index], logger)
    bstack1l1l11l1_opy_ += list(bstack1l1111l1l1_opy_.keys())
    for bstack1l11l1ll_opy_ in bstack1l1l11l1_opy_:
      if bstack1l11l1ll_opy_ in config[bstack1ll11ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪग़")][index]:
        if bstack1l11l1ll_opy_ == bstack1ll11ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪज़"):
          try:
            bstack1l1111l1l1_opy_[bstack1l11l1ll_opy_] = str(config[bstack1ll11ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬड़")][index][bstack1l11l1ll_opy_] * 1.0)
          except:
            bstack1l1111l1l1_opy_[bstack1l11l1ll_opy_] = str(config[bstack1ll11ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ढ़")][index][bstack1l11l1ll_opy_])
        else:
          bstack1l1111l1l1_opy_[bstack1l11l1ll_opy_] = config[bstack1ll11ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧफ़")][index][bstack1l11l1ll_opy_]
        del (config[bstack1ll11ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨय़")][index][bstack1l11l1ll_opy_])
    bstack1llll1l1_opy_ = update(bstack1llll1l1_opy_, bstack1l1111l1l1_opy_)
  bstack1l1l11l11l_opy_ = bstack1l1llll1l_opy_(config, index)
  for bstack1lll1111_opy_ in bstack1l1l11l111_opy_ + list(bstack1l111lll11_opy_.keys()):
    if bstack1lll1111_opy_ in bstack1l1l11l11l_opy_:
      bstack1llll1l1_opy_[bstack1lll1111_opy_] = bstack1l1l11l11l_opy_[bstack1lll1111_opy_]
      del (bstack1l1l11l11l_opy_[bstack1lll1111_opy_])
  if bstack1l11l1llll_opy_(config):
    bstack1l1l11l11l_opy_[bstack1ll11ll_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ॠ")] = True
    caps.update(bstack1llll1l1_opy_)
    caps[bstack1ll11ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨॡ")] = bstack1l1l11l11l_opy_
  else:
    bstack1l1l11l11l_opy_[bstack1ll11ll_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨॢ")] = False
    caps.update(bstack111lll1l1_opy_(bstack1l1l11l11l_opy_, bstack1llll1l1_opy_))
    if bstack1ll11ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧॣ") in caps:
      caps[bstack1ll11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫ।")] = caps[bstack1ll11ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ॥")]
      del (caps[bstack1ll11ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ०")])
    if bstack1ll11ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ१") in caps:
      caps[bstack1ll11ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ२")] = caps[bstack1ll11ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ३")]
      del (caps[bstack1ll11ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ४")])
  return caps
def bstack11lll111l1_opy_():
  global bstack11lll1lll_opy_
  global CONFIG
  if bstack1l11111111_opy_() <= version.parse(bstack1ll11ll_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪ५")):
    if bstack11lll1lll_opy_ != bstack1ll11ll_opy_ (u"ࠫࠬ६"):
      return bstack1ll11ll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨ७") + bstack11lll1lll_opy_ + bstack1ll11ll_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥ८")
    return bstack11ll1ll11_opy_
  if bstack11lll1lll_opy_ != bstack1ll11ll_opy_ (u"ࠧࠨ९"):
    return bstack1ll11ll_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥ॰") + bstack11lll1lll_opy_ + bstack1ll11ll_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥॱ")
  return bstack11lllll1ll_opy_
def bstack11l1lllll_opy_(options):
  return hasattr(options, bstack1ll11ll_opy_ (u"ࠪࡷࡪࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠫॲ"))
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
def bstack111lllllll_opy_(options, bstack1l1l11ll1_opy_):
  for bstack1ll11l1ll1_opy_ in bstack1l1l11ll1_opy_:
    if bstack1ll11l1ll1_opy_ in [bstack1ll11ll_opy_ (u"ࠫࡦࡸࡧࡴࠩॳ"), bstack1ll11ll_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩॴ")]:
      continue
    if bstack1ll11l1ll1_opy_ in options._experimental_options:
      options._experimental_options[bstack1ll11l1ll1_opy_] = update(options._experimental_options[bstack1ll11l1ll1_opy_],
                                                         bstack1l1l11ll1_opy_[bstack1ll11l1ll1_opy_])
    else:
      options.add_experimental_option(bstack1ll11l1ll1_opy_, bstack1l1l11ll1_opy_[bstack1ll11l1ll1_opy_])
  if bstack1ll11ll_opy_ (u"࠭ࡡࡳࡩࡶࠫॵ") in bstack1l1l11ll1_opy_:
    for arg in bstack1l1l11ll1_opy_[bstack1ll11ll_opy_ (u"ࠧࡢࡴࡪࡷࠬॶ")]:
      options.add_argument(arg)
    del (bstack1l1l11ll1_opy_[bstack1ll11ll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ॷ")])
  if bstack1ll11ll_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ॸ") in bstack1l1l11ll1_opy_:
    for ext in bstack1l1l11ll1_opy_[bstack1ll11ll_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧॹ")]:
      try:
        options.add_extension(ext)
      except OSError:
        options.add_encoded_extension(ext)
    del (bstack1l1l11ll1_opy_[bstack1ll11ll_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨॺ")])
def bstack1ll1ll111l_opy_(options, bstack1l11l1l1l_opy_):
  if bstack1ll11ll_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫॻ") in bstack1l11l1l1l_opy_:
    for bstack1l1ll1lll1_opy_ in bstack1l11l1l1l_opy_[bstack1ll11ll_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬॼ")]:
      if bstack1l1ll1lll1_opy_ in options._preferences:
        options._preferences[bstack1l1ll1lll1_opy_] = update(options._preferences[bstack1l1ll1lll1_opy_], bstack1l11l1l1l_opy_[bstack1ll11ll_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ॽ")][bstack1l1ll1lll1_opy_])
      else:
        options.set_preference(bstack1l1ll1lll1_opy_, bstack1l11l1l1l_opy_[bstack1ll11ll_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧॾ")][bstack1l1ll1lll1_opy_])
  if bstack1ll11ll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॿ") in bstack1l11l1l1l_opy_:
    for arg in bstack1l11l1l1l_opy_[bstack1ll11ll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨঀ")]:
      options.add_argument(arg)
def bstack1l11l1lll1_opy_(options, bstack1llllll111_opy_):
  if bstack1ll11ll_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࠬঁ") in bstack1llllll111_opy_:
    options.use_webview(bool(bstack1llllll111_opy_[bstack1ll11ll_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼ࠭ং")]))
  bstack111lllllll_opy_(options, bstack1llllll111_opy_)
def bstack111lll1l_opy_(options, bstack1llll111l1_opy_):
  for bstack1l11111l1l_opy_ in bstack1llll111l1_opy_:
    if bstack1l11111l1l_opy_ in [bstack1ll11ll_opy_ (u"࠭ࡴࡦࡥ࡫ࡲࡴࡲ࡯ࡨࡻࡓࡶࡪࡼࡩࡦࡹࠪঃ"), bstack1ll11ll_opy_ (u"ࠧࡢࡴࡪࡷࠬ঄")]:
      continue
    options.set_capability(bstack1l11111l1l_opy_, bstack1llll111l1_opy_[bstack1l11111l1l_opy_])
  if bstack1ll11ll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭অ") in bstack1llll111l1_opy_:
    for arg in bstack1llll111l1_opy_[bstack1ll11ll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧআ")]:
      options.add_argument(arg)
  if bstack1ll11ll_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧই") in bstack1llll111l1_opy_:
    options.bstack1ll1111ll_opy_(bool(bstack1llll111l1_opy_[bstack1ll11ll_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨঈ")]))
def bstack1l1l11111_opy_(options, bstack1111l1lll_opy_):
  for bstack1l111l1ll1_opy_ in bstack1111l1lll_opy_:
    if bstack1l111l1ll1_opy_ in [bstack1ll11ll_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩউ"), bstack1ll11ll_opy_ (u"࠭ࡡࡳࡩࡶࠫঊ")]:
      continue
    options._options[bstack1l111l1ll1_opy_] = bstack1111l1lll_opy_[bstack1l111l1ll1_opy_]
  if bstack1ll11ll_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫঋ") in bstack1111l1lll_opy_:
    for bstack11l11l1l1l_opy_ in bstack1111l1lll_opy_[bstack1ll11ll_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬঌ")]:
      options.bstack1lll11llll_opy_(
        bstack11l11l1l1l_opy_, bstack1111l1lll_opy_[bstack1ll11ll_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭঍")][bstack11l11l1l1l_opy_])
  if bstack1ll11ll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ঎") in bstack1111l1lll_opy_:
    for arg in bstack1111l1lll_opy_[bstack1ll11ll_opy_ (u"ࠫࡦࡸࡧࡴࠩএ")]:
      options.add_argument(arg)
def bstack11lllll111_opy_(options, caps):
  if not hasattr(options, bstack1ll11ll_opy_ (u"ࠬࡑࡅ࡚ࠩঐ")):
    return
  if options.KEY == bstack1ll11ll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ঑"):
    options = bstack1l1l11l1l1_opy_.bstack11ll111ll_opy_(bstack1l111lll1_opy_=options, config=CONFIG)
  if options.KEY == bstack1ll11ll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ঒") and options.KEY in caps:
    bstack111lllllll_opy_(options, caps[bstack1ll11ll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ও")])
  elif options.KEY == bstack1ll11ll_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧঔ") and options.KEY in caps:
    bstack1ll1ll111l_opy_(options, caps[bstack1ll11ll_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨক")])
  elif options.KEY == bstack1ll11ll_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬখ") and options.KEY in caps:
    bstack111lll1l_opy_(options, caps[bstack1ll11ll_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭গ")])
  elif options.KEY == bstack1ll11ll_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧঘ") and options.KEY in caps:
    bstack1l11l1lll1_opy_(options, caps[bstack1ll11ll_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨঙ")])
  elif options.KEY == bstack1ll11ll_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧচ") and options.KEY in caps:
    bstack1l1l11111_opy_(options, caps[bstack1ll11ll_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨছ")])
def bstack1ll11111ll_opy_(caps):
  global bstack1l1lll1l1l_opy_
  if isinstance(os.environ.get(bstack1ll11ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫজ")), str):
    bstack1l1lll1l1l_opy_ = eval(os.getenv(bstack1ll11ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬঝ")))
  if bstack1l1lll1l1l_opy_:
    if bstack1lllll1l1l_opy_() < version.parse(bstack1ll11ll_opy_ (u"ࠬ࠸࠮࠴࠰࠳ࠫঞ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1ll11ll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ট")
    if bstack1ll11ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬঠ") in caps:
      browser = caps[bstack1ll11ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ড")]
    elif bstack1ll11ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪঢ") in caps:
      browser = caps[bstack1ll11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫণ")]
    browser = str(browser).lower()
    if browser == bstack1ll11ll_opy_ (u"ࠫ࡮ࡶࡨࡰࡰࡨࠫত") or browser == bstack1ll11ll_opy_ (u"ࠬ࡯ࡰࡢࡦࠪথ"):
      browser = bstack1ll11ll_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭দ")
    if browser == bstack1ll11ll_opy_ (u"ࠧࡴࡣࡰࡷࡺࡴࡧࠨধ"):
      browser = bstack1ll11ll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨন")
    if browser not in [bstack1ll11ll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩ঩"), bstack1ll11ll_opy_ (u"ࠪࡩࡩ࡭ࡥࠨপ"), bstack1ll11ll_opy_ (u"ࠫ࡮࡫ࠧফ"), bstack1ll11ll_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬব"), bstack1ll11ll_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧভ")]:
      return None
    try:
      package = bstack1ll11ll_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࠰ࡺࡩࡧࡪࡲࡪࡸࡨࡶ࠳ࢁࡽ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩম").format(browser)
      name = bstack1ll11ll_opy_ (u"ࠨࡑࡳࡸ࡮ࡵ࡮ࡴࠩয")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack11l1lllll_opy_(options):
        return None
      for bstack1lll1111_opy_ in caps.keys():
        options.set_capability(bstack1lll1111_opy_, caps[bstack1lll1111_opy_])
      bstack11lllll111_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack111111l11_opy_(options, bstack1l111llll_opy_):
  if not bstack11l1lllll_opy_(options):
    return
  for bstack1lll1111_opy_ in bstack1l111llll_opy_.keys():
    if bstack1lll1111_opy_ in bstack1111l1ll1_opy_:
      continue
    if bstack1lll1111_opy_ in options._caps and type(options._caps[bstack1lll1111_opy_]) in [dict, list]:
      options._caps[bstack1lll1111_opy_] = update(options._caps[bstack1lll1111_opy_], bstack1l111llll_opy_[bstack1lll1111_opy_])
    else:
      options.set_capability(bstack1lll1111_opy_, bstack1l111llll_opy_[bstack1lll1111_opy_])
  bstack11lllll111_opy_(options, bstack1l111llll_opy_)
  if bstack1ll11ll_opy_ (u"ࠩࡰࡳࡿࡀࡤࡦࡤࡸ࡫࡬࡫ࡲࡂࡦࡧࡶࡪࡹࡳࠨর") in options._caps:
    if options._caps[bstack1ll11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ঱")] and options._caps[bstack1ll11ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩল")].lower() != bstack1ll11ll_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭঳"):
      del options._caps[bstack1ll11ll_opy_ (u"࠭࡭ࡰࡼ࠽ࡨࡪࡨࡵࡨࡩࡨࡶࡆࡪࡤࡳࡧࡶࡷࠬ঴")]
def bstack11ll1l1lll_opy_(proxy_config):
  if bstack1ll11ll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ঵") in proxy_config:
    proxy_config[bstack1ll11ll_opy_ (u"ࠨࡵࡶࡰࡕࡸ࡯ࡹࡻࠪশ")] = proxy_config[bstack1ll11ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ষ")]
    del (proxy_config[bstack1ll11ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧস")])
  if bstack1ll11ll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧহ") in proxy_config and proxy_config[bstack1ll11ll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ঺")].lower() != bstack1ll11ll_opy_ (u"࠭ࡤࡪࡴࡨࡧࡹ࠭঻"):
    proxy_config[bstack1ll11ll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧ়ࠪ")] = bstack1ll11ll_opy_ (u"ࠨ࡯ࡤࡲࡺࡧ࡬ࠨঽ")
  if bstack1ll11ll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡂࡷࡷࡳࡨࡵ࡮ࡧ࡫ࡪ࡙ࡷࡲࠧা") in proxy_config:
    proxy_config[bstack1ll11ll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭ি")] = bstack1ll11ll_opy_ (u"ࠫࡵࡧࡣࠨী")
  return proxy_config
def bstack1ll1llll1l_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1ll11ll_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫু") in config:
    return proxy
  config[bstack1ll11ll_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬূ")] = bstack11ll1l1lll_opy_(config[bstack1ll11ll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭ৃ")])
  if proxy == None:
    proxy = Proxy(config[bstack1ll11ll_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧৄ")])
  return proxy
def bstack1l1lllllll_opy_(self):
  global CONFIG
  global bstack111lllll11_opy_
  try:
    proxy = bstack11l1l1ll1l_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1ll11ll_opy_ (u"ࠩ࠱ࡴࡦࡩࠧ৅")):
        proxies = bstack11ll11ll_opy_(proxy, bstack11lll111l1_opy_())
        if len(proxies) > 0:
          protocol, bstack111l11111_opy_ = proxies.popitem()
          if bstack1ll11ll_opy_ (u"ࠥ࠾࠴࠵ࠢ৆") in bstack111l11111_opy_:
            return bstack111l11111_opy_
          else:
            return bstack1ll11ll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧে") + bstack111l11111_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1ll11ll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡲࡵࡳࡽࡿࠠࡶࡴ࡯ࠤ࠿ࠦࡻࡾࠤৈ").format(str(e)))
  return bstack111lllll11_opy_(self)
def bstack1l1ll1lll_opy_():
  global CONFIG
  return bstack11l11lll1l_opy_(CONFIG) and bstack111111ll_opy_() and bstack1l11111111_opy_() >= version.parse(bstack111l1lll_opy_)
def bstack1llll11l11_opy_():
  global CONFIG
  return (bstack1ll11ll_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ৉") in CONFIG or bstack1ll11ll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ৊") in CONFIG) and bstack11l111l11_opy_()
def bstack1l1lll111_opy_(config):
  bstack11llllll11_opy_ = {}
  if bstack1ll11ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬো") in config:
    bstack11llllll11_opy_ = config[bstack1ll11ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ৌ")]
  if bstack1ll11ll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴ্ࠩ") in config:
    bstack11llllll11_opy_ = config[bstack1ll11ll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪৎ")]
  proxy = bstack11l1l1ll1l_opy_(config)
  if proxy:
    if proxy.endswith(bstack1ll11ll_opy_ (u"ࠬ࠴ࡰࡢࡥࠪ৏")) and os.path.isfile(proxy):
      bstack11llllll11_opy_[bstack1ll11ll_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩ৐")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1ll11ll_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ৑")):
        proxies = bstack1llll11lll_opy_(config, bstack11lll111l1_opy_())
        if len(proxies) > 0:
          protocol, bstack111l11111_opy_ = proxies.popitem()
          if bstack1ll11ll_opy_ (u"ࠣ࠼࠲࠳ࠧ৒") in bstack111l11111_opy_:
            parsed_url = urlparse(bstack111l11111_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1ll11ll_opy_ (u"ࠤ࠽࠳࠴ࠨ৓") + bstack111l11111_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack11llllll11_opy_[bstack1ll11ll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ࠭৔")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack11llllll11_opy_[bstack1ll11ll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡳࡷࡺࠧ৕")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack11llllll11_opy_[bstack1ll11ll_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨ৖")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack11llllll11_opy_[bstack1ll11ll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡧࡳࡴࠩৗ")] = str(parsed_url.password)
  return bstack11llllll11_opy_
def bstack1111l1l1_opy_(config):
  if bstack1ll11ll_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬ৘") in config:
    return config[bstack1ll11ll_opy_ (u"ࠨࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸ࠭৙")]
  return {}
def bstack11ll1l111_opy_(caps):
  global bstack1lll11lll1_opy_
  if bstack1ll11ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ৚") in caps:
    caps[bstack1ll11ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ৛")][bstack1ll11ll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࠪড়")] = True
    if bstack1lll11lll1_opy_:
      caps[bstack1ll11ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ঢ়")][bstack1ll11ll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ৞")] = bstack1lll11lll1_opy_
  else:
    caps[bstack1ll11ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࠬয়")] = True
    if bstack1lll11lll1_opy_:
      caps[bstack1ll11ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩৠ")] = bstack1lll11lll1_opy_
@measure(event_name=EVENTS.bstack11l1111l_opy_, stage=STAGE.bstack11lll1ll1l_opy_, bstack11ll1l1l_opy_=bstack111l1l11_opy_)
def bstack1l1ll1l1l_opy_():
  global CONFIG
  if not bstack11l1lll1ll_opy_(CONFIG) or cli.is_enabled(CONFIG):
    return
  if bstack1ll11ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ৡ") in CONFIG and bstack1l1l1llll1_opy_(CONFIG[bstack1ll11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧৢ")]):
    if (
      bstack1ll11ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨৣ") in CONFIG
      and bstack1l1l1llll1_opy_(CONFIG[bstack1ll11ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ৤")].get(bstack1ll11ll_opy_ (u"࠭ࡳ࡬࡫ࡳࡆ࡮ࡴࡡࡳࡻࡌࡲ࡮ࡺࡩࡢ࡮࡬ࡷࡦࡺࡩࡰࡰࠪ৥")))
    ):
      logger.debug(bstack1ll11ll_opy_ (u"ࠢࡍࡱࡦࡥࡱࠦࡢࡪࡰࡤࡶࡾࠦ࡮ࡰࡶࠣࡷࡹࡧࡲࡵࡧࡧࠤࡦࡹࠠࡴ࡭࡬ࡴࡇ࡯࡮ࡢࡴࡼࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡸࡧࡴࡪࡱࡱࠤ࡮ࡹࠠࡦࡰࡤࡦࡱ࡫ࡤࠣ০"))
      return
    bstack11llllll11_opy_ = bstack1l1lll111_opy_(CONFIG)
    bstack11l1111l1_opy_(CONFIG[bstack1ll11ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ১")], bstack11llllll11_opy_)
def bstack11l1111l1_opy_(key, bstack11llllll11_opy_):
  global bstack111l11lll_opy_
  logger.info(bstack11l1l1111l_opy_)
  try:
    bstack111l11lll_opy_ = Local()
    bstack1l1111l1l_opy_ = {bstack1ll11ll_opy_ (u"ࠩ࡮ࡩࡾ࠭২"): key}
    bstack1l1111l1l_opy_.update(bstack11llllll11_opy_)
    logger.debug(bstack111lllll_opy_.format(str(bstack1l1111l1l_opy_)).replace(key, bstack1ll11ll_opy_ (u"ࠪ࡟ࡗࡋࡄࡂࡅࡗࡉࡉࡣࠧ৩")))
    bstack111l11lll_opy_.start(**bstack1l1111l1l_opy_)
    if bstack111l11lll_opy_.isRunning():
      logger.info(bstack1111llll_opy_)
  except Exception as e:
    bstack1l1111111l_opy_(bstack1ll11ll1_opy_.format(str(e)))
def bstack1ll1llll_opy_():
  global bstack111l11lll_opy_
  if bstack111l11lll_opy_.isRunning():
    logger.info(bstack11lllll11_opy_)
    bstack111l11lll_opy_.stop()
  bstack111l11lll_opy_ = None
def bstack1lllll11l_opy_(bstack1l11111ll1_opy_=[]):
  global CONFIG
  bstack1l1lllll1l_opy_ = []
  bstack11ll11lll_opy_ = [bstack1ll11ll_opy_ (u"ࠫࡴࡹࠧ৪"), bstack1ll11ll_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨ৫"), bstack1ll11ll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪ৬"), bstack1ll11ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ৭"), bstack1ll11ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭৮"), bstack1ll11ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ৯")]
  try:
    for err in bstack1l11111ll1_opy_:
      bstack1l1lll1l1_opy_ = {}
      for k in bstack11ll11lll_opy_:
        val = CONFIG[bstack1ll11ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ৰ")][int(err[bstack1ll11ll_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪৱ")])].get(k)
        if val:
          bstack1l1lll1l1_opy_[k] = val
      if(err[bstack1ll11ll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ৲")] != bstack1ll11ll_opy_ (u"࠭ࠧ৳")):
        bstack1l1lll1l1_opy_[bstack1ll11ll_opy_ (u"ࠧࡵࡧࡶࡸࡸ࠭৴")] = {
          err[bstack1ll11ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭৵")]: err[bstack1ll11ll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ৶")]
        }
        bstack1l1lllll1l_opy_.append(bstack1l1lll1l1_opy_)
  except Exception as e:
    logger.debug(bstack1ll11ll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡬࡯ࡳ࡯ࡤࡸࡹ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶ࠽ࠤࠬ৷") + str(e))
  finally:
    return bstack1l1lllll1l_opy_
def bstack1111ll111_opy_(file_name):
  bstack1ll11lll1_opy_ = []
  try:
    bstack11l11lll_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack11l11lll_opy_):
      with open(bstack11l11lll_opy_) as f:
        bstack1ll111111l_opy_ = json.load(f)
        bstack1ll11lll1_opy_ = bstack1ll111111l_opy_
      os.remove(bstack11l11lll_opy_)
    return bstack1ll11lll1_opy_
  except Exception as e:
    logger.debug(bstack1ll11ll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡪࡰࡧ࡭ࡳ࡭ࠠࡦࡴࡵࡳࡷࠦ࡬ࡪࡵࡷ࠾ࠥ࠭৸") + str(e))
    return bstack1ll11lll1_opy_
def bstack111ll11l1_opy_():
  try:
      from bstack_utils.constants import bstack11111l11l_opy_, EVENTS
      from bstack_utils.helper import bstack1lllll1111_opy_, get_host_info, bstack1l111111l1_opy_
      from datetime import datetime
      from filelock import FileLock
      bstack111l1l111_opy_ = os.path.join(os.getcwd(), bstack1ll11ll_opy_ (u"ࠬࡲ࡯ࡨࠩ৹"), bstack1ll11ll_opy_ (u"࠭࡫ࡦࡻ࠰ࡱࡪࡺࡲࡪࡥࡶ࠲࡯ࡹ࡯࡯ࠩ৺"))
      lock = FileLock(bstack111l1l111_opy_+bstack1ll11ll_opy_ (u"ࠢ࠯࡮ࡲࡧࡰࠨ৻"))
      def bstack11l11l1l11_opy_():
          try:
              with lock:
                  with open(bstack111l1l111_opy_, bstack1ll11ll_opy_ (u"ࠣࡴࠥৼ"), encoding=bstack1ll11ll_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣ৽")) as file:
                      data = json.load(file)
                      config = {
                          bstack1ll11ll_opy_ (u"ࠥ࡬ࡪࡧࡤࡦࡴࡶࠦ৾"): {
                              bstack1ll11ll_opy_ (u"ࠦࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠥ৿"): bstack1ll11ll_opy_ (u"ࠧࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠣ਀"),
                          }
                      }
                      bstack1l1l1l1l1l_opy_ = datetime.utcnow()
                      bstack11l1l1l1l1_opy_ = bstack1l1l1l1l1l_opy_.strftime(bstack1ll11ll_opy_ (u"ࠨ࡚ࠥ࠯ࠨࡱ࠲ࠫࡤࡕࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࠱ࠩ࡫ࠦࡕࡕࡅࠥਁ"))
                      bstack1l1l1ll1l1_opy_ = os.environ.get(bstack1ll11ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬਂ")) if os.environ.get(bstack1ll11ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ਃ")) else bstack1l111111l1_opy_.get_property(bstack1ll11ll_opy_ (u"ࠤࡶࡨࡰࡘࡵ࡯ࡋࡧࠦ਄"))
                      payload = {
                          bstack1ll11ll_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠢਅ"): bstack1ll11ll_opy_ (u"ࠦࡸࡪ࡫ࡠࡧࡹࡩࡳࡺࡳࠣਆ"),
                          bstack1ll11ll_opy_ (u"ࠧࡪࡡࡵࡣࠥਇ"): {
                              bstack1ll11ll_opy_ (u"ࠨࡴࡦࡵࡷ࡬ࡺࡨ࡟ࡶࡷ࡬ࡨࠧਈ"): bstack1l1l1ll1l1_opy_,
                              bstack1ll11ll_opy_ (u"ࠢࡤࡴࡨࡥࡹ࡫ࡤࡠࡦࡤࡽࠧਉ"): bstack11l1l1l1l1_opy_,
                              bstack1ll11ll_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟࡯ࡣࡰࡩࠧਊ"): bstack1ll11ll_opy_ (u"ࠤࡖࡈࡐࡌࡥࡢࡶࡸࡶࡪࡖࡥࡳࡨࡲࡶࡲࡧ࡮ࡤࡧࠥ਋"),
                              bstack1ll11ll_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡ࡭ࡷࡴࡴࠢ਌"): {
                                  bstack1ll11ll_opy_ (u"ࠦࡲ࡫ࡡࡴࡷࡵࡩࡸࠨ਍"): data,
                                  bstack1ll11ll_opy_ (u"ࠧࡹࡤ࡬ࡔࡸࡲࡎࡪࠢ਎"): bstack1l111111l1_opy_.get_property(bstack1ll11ll_opy_ (u"ࠨࡳࡥ࡭ࡕࡹࡳࡏࡤࠣਏ"))
                              },
                              bstack1ll11ll_opy_ (u"ࠢࡶࡵࡨࡶࡤࡪࡡࡵࡣࠥਐ"): bstack1l111111l1_opy_.get_property(bstack1ll11ll_opy_ (u"ࠣࡷࡶࡩࡷࡔࡡ࡮ࡧࠥ਑")),
                              bstack1ll11ll_opy_ (u"ࠤ࡫ࡳࡸࡺ࡟ࡪࡰࡩࡳࠧ਒"): get_host_info()
                          }
                      }
                      bstack11l111ll11_opy_ = bstack1111lllll_opy_(cli.config, [bstack1ll11ll_opy_ (u"ࠥࡥࡵ࡯ࡳࠣਓ"), bstack1ll11ll_opy_ (u"ࠦࡪࡪࡳࡊࡰࡶࡸࡷࡻ࡭ࡦࡰࡷࡥࡹ࡯࡯࡯ࠤਔ"), bstack1ll11ll_opy_ (u"ࠧࡧࡰࡪࠤਕ")], bstack11111l11l_opy_)
                      response = bstack1lllll1111_opy_(bstack1ll11ll_opy_ (u"ࠨࡐࡐࡕࡗࠦਖ"), bstack11l111ll11_opy_, payload, config)
                      if(response.status_code >= 200 and response.status_code < 300):
                          logger.debug(bstack1ll11ll_opy_ (u"ࠢࡅࡣࡷࡥࠥࡹࡥ࡯ࡶࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺࠢࡷࡳࠥࢁࡽࠡࡹ࡬ࡸ࡭ࠦࡤࡢࡶࡤࠤࢀࢃࠢਗ").format(bstack11111l11l_opy_, payload))
                      else:
                          logger.debug(bstack1ll11ll_opy_ (u"ࠣࡔࡨࡵࡺ࡫ࡳࡵࠢࡩࡥ࡮ࡲࡥࡥࠢࡩࡳࡷࠦࡻࡾࠢࡺ࡭ࡹ࡮ࠠࡥࡣࡷࡥࠥࢁࡽࠣਘ").format(bstack11111l11l_opy_, payload))
          except Exception as e:
              logger.debug(bstack1ll11ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥ࡯ࡦࠣ࡯ࡪࡿࠠ࡮ࡧࡷࡶ࡮ࡩࡳࠡࡦࡤࡸࡦࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴࠣࡿࢂࠨਙ").format(e))
      bstack11l11l1l11_opy_()
      bstack1l111l11ll_opy_(bstack111l1l111_opy_, logger)
  except:
    pass
def bstack11l111ll1l_opy_():
  global bstack111l11l1_opy_
  global bstack1lll1ll1l1_opy_
  global bstack1l111l1l11_opy_
  global bstack11l1l1lll1_opy_
  global bstack1ll1111l1_opy_
  global bstack11lll11111_opy_
  global CONFIG
  bstack1l1llll1l1_opy_ = os.environ.get(bstack1ll11ll_opy_ (u"ࠪࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡕࡔࡇࡇࠫਚ"))
  if bstack1l1llll1l1_opy_ in [bstack1ll11ll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪਛ"), bstack1ll11ll_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫਜ")]:
    bstack1l1l11lll_opy_()
  percy.shutdown()
  if bstack111l11l1_opy_:
    logger.warning(bstack11llll1111_opy_.format(str(bstack111l11l1_opy_)))
  else:
    try:
      bstack111l111l1_opy_ = bstack1lll1lll1l_opy_(bstack1ll11ll_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬਝ"), logger)
      if bstack111l111l1_opy_.get(bstack1ll11ll_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬਞ")) and bstack111l111l1_opy_.get(bstack1ll11ll_opy_ (u"ࠨࡰࡸࡨ࡬࡫࡟࡭ࡱࡦࡥࡱ࠭ਟ")).get(bstack1ll11ll_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫਠ")):
        logger.warning(bstack11llll1111_opy_.format(str(bstack111l111l1_opy_[bstack1ll11ll_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨਡ")][bstack1ll11ll_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ਢ")])))
    except Exception as e:
      logger.error(e)
  if cli.is_running():
    bstack1111ll1l_opy_.invoke(bstack11l1lll1l_opy_.bstack1l111l1lll_opy_)
  logger.info(bstack1l1l111l1l_opy_)
  global bstack111l11lll_opy_
  if bstack111l11lll_opy_:
    bstack1ll1llll_opy_()
  try:
    with bstack11ll111l_opy_:
      bstack1l1ll11l11_opy_ = bstack1lll1ll1l1_opy_.copy()
    for driver in bstack1l1ll11l11_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1ll1l1l1l1_opy_)
  if bstack11lll11111_opy_ == bstack1ll11ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫਣ"):
    bstack1ll1111l1_opy_ = bstack1111ll111_opy_(bstack1ll11ll_opy_ (u"࠭ࡲࡰࡤࡲࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧਤ"))
  if bstack11lll11111_opy_ == bstack1ll11ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧਥ") and len(bstack11l1l1lll1_opy_) == 0:
    bstack11l1l1lll1_opy_ = bstack1111ll111_opy_(bstack1ll11ll_opy_ (u"ࠨࡲࡺࡣࡵࡿࡴࡦࡵࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ਦ"))
    if len(bstack11l1l1lll1_opy_) == 0:
      bstack11l1l1lll1_opy_ = bstack1111ll111_opy_(bstack1ll11ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡳࡴࡵࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨਧ"))
  bstack11llll11l1_opy_ = bstack1ll11ll_opy_ (u"ࠪࠫਨ")
  if len(bstack1l111l1l11_opy_) > 0:
    bstack11llll11l1_opy_ = bstack1lllll11l_opy_(bstack1l111l1l11_opy_)
  elif len(bstack11l1l1lll1_opy_) > 0:
    bstack11llll11l1_opy_ = bstack1lllll11l_opy_(bstack11l1l1lll1_opy_)
  elif len(bstack1ll1111l1_opy_) > 0:
    bstack11llll11l1_opy_ = bstack1lllll11l_opy_(bstack1ll1111l1_opy_)
  elif len(bstack1l111lll_opy_) > 0:
    bstack11llll11l1_opy_ = bstack1lllll11l_opy_(bstack1l111lll_opy_)
  if bool(bstack11llll11l1_opy_):
    bstack11l11111ll_opy_(bstack11llll11l1_opy_)
  else:
    bstack11l11111ll_opy_()
  bstack1l111l11ll_opy_(bstack1l1l11111l_opy_, logger)
  if bstack1l1llll1l1_opy_ not in [bstack1ll11ll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ਩")]:
    bstack111ll11l1_opy_()
  bstack1lll1llll_opy_.bstack11lllll11l_opy_(CONFIG)
  if len(bstack1ll1111l1_opy_) > 0:
    sys.exit(len(bstack1ll1111l1_opy_))
def bstack1l111l111l_opy_(bstack11l11ll1l1_opy_, frame):
  global bstack1l111111l1_opy_
  logger.error(bstack111ll1l1l_opy_)
  bstack1l111111l1_opy_.bstack11l111l1l_opy_(bstack1ll11ll_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱࡔ࡯ࠨਪ"), bstack11l11ll1l1_opy_)
  if hasattr(signal, bstack1ll11ll_opy_ (u"࠭ࡓࡪࡩࡱࡥࡱࡹࠧਫ")):
    bstack1l111111l1_opy_.bstack11l111l1l_opy_(bstack1ll11ll_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡔ࡫ࡪࡲࡦࡲࠧਬ"), signal.Signals(bstack11l11ll1l1_opy_).name)
  else:
    bstack1l111111l1_opy_.bstack11l111l1l_opy_(bstack1ll11ll_opy_ (u"ࠨࡵࡧ࡯ࡐ࡯࡬࡭ࡕ࡬࡫ࡳࡧ࡬ࠨਭ"), bstack1ll11ll_opy_ (u"ࠩࡖࡍࡌ࡛ࡎࡌࡐࡒ࡛ࡓ࠭ਮ"))
  if cli.is_running():
    bstack1111ll1l_opy_.invoke(bstack11l1lll1l_opy_.bstack1l111l1lll_opy_)
  bstack1l1llll1l1_opy_ = os.environ.get(bstack1ll11ll_opy_ (u"ࠪࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡕࡔࡇࡇࠫਯ"))
  if bstack1l1llll1l1_opy_ == bstack1ll11ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫਰ") and not cli.is_enabled(CONFIG):
    bstack1l11ll1l_opy_.stop(bstack1l111111l1_opy_.get_property(bstack1ll11ll_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬ਱")))
  bstack11l111ll1l_opy_()
  sys.exit(1)
def bstack1l1111111l_opy_(err):
  logger.critical(bstack11ll111l1l_opy_.format(str(err)))
  bstack11l11111ll_opy_(bstack11ll111l1l_opy_.format(str(err)), True)
  atexit.unregister(bstack11l111ll1l_opy_)
  bstack1l1l11lll_opy_()
  sys.exit(1)
def bstack1ll1l1l1_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack11l11111ll_opy_(message, True)
  atexit.unregister(bstack11l111ll1l_opy_)
  bstack1l1l11lll_opy_()
  sys.exit(1)
def bstack1l1lll1ll_opy_():
  global CONFIG
  global bstack1l111lllll_opy_
  global bstack1ll111llll_opy_
  global bstack11l1ll11l_opy_
  CONFIG = bstack1l111ll1ll_opy_()
  load_dotenv(CONFIG.get(bstack1ll11ll_opy_ (u"࠭ࡥ࡯ࡸࡉ࡭ࡱ࡫ࠧਲ")))
  bstack11l1l1ll1_opy_()
  bstack1lll1ll1_opy_()
  CONFIG = bstack1lll11l1l_opy_(CONFIG)
  update(CONFIG, bstack1ll111llll_opy_)
  update(CONFIG, bstack1l111lllll_opy_)
  if not cli.is_enabled(CONFIG):
    CONFIG = bstack1lll11l1l1_opy_(CONFIG)
  bstack11l1ll11l_opy_ = bstack11l1lll1ll_opy_(CONFIG)
  os.environ[bstack1ll11ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪਲ਼")] = bstack11l1ll11l_opy_.__str__().lower()
  bstack1l111111l1_opy_.bstack11l111l1l_opy_(bstack1ll11ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩ਴"), bstack11l1ll11l_opy_)
  if (bstack1ll11ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬਵ") in CONFIG and bstack1ll11ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ਸ਼") in bstack1l111lllll_opy_) or (
          bstack1ll11ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ਷") in CONFIG and bstack1ll11ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨਸ") not in bstack1ll111llll_opy_):
    if os.getenv(bstack1ll11ll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪਹ")):
      CONFIG[bstack1ll11ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ਺")] = os.getenv(bstack1ll11ll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬ਻"))
    else:
      if not CONFIG.get(bstack1ll11ll_opy_ (u"ࠤࡩࡶࡦࡳࡥࡸࡱࡵ࡯਼ࠧ"), bstack1ll11ll_opy_ (u"ࠥࠦ਽")) in bstack111l1ll1l_opy_:
        bstack1l111111ll_opy_()
  elif (bstack1ll11ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧਾ") not in CONFIG and bstack1ll11ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧਿ") in CONFIG) or (
          bstack1ll11ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩੀ") in bstack1ll111llll_opy_ and bstack1ll11ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪੁ") not in bstack1l111lllll_opy_):
    del (CONFIG[bstack1ll11ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪੂ")])
  if bstack1l1llll11l_opy_(CONFIG):
    bstack1l1111111l_opy_(bstack1lll111ll_opy_)
  Config.bstack11l11lllll_opy_().bstack11l111l1l_opy_(bstack1ll11ll_opy_ (u"ࠤࡸࡷࡪࡸࡎࡢ࡯ࡨࠦ੃"), CONFIG[bstack1ll11ll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ੄")])
  bstack11l11l1ll_opy_()
  bstack1l1ll111l_opy_()
  if bstack1l1lll1l1l_opy_ and not CONFIG.get(bstack1ll11ll_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠢ੅"), bstack1ll11ll_opy_ (u"ࠧࠨ੆")) in bstack111l1ll1l_opy_:
    CONFIG[bstack1ll11ll_opy_ (u"࠭ࡡࡱࡲࠪੇ")] = bstack1l111l11l1_opy_(CONFIG)
    logger.info(bstack11l11111l_opy_.format(CONFIG[bstack1ll11ll_opy_ (u"ࠧࡢࡲࡳࠫੈ")]))
  if not bstack11l1ll11l_opy_:
    CONFIG[bstack1ll11ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ੉")] = [{}]
def bstack1l1111ll_opy_(config, bstack11ll11ll1l_opy_):
  global CONFIG
  global bstack1l1lll1l1l_opy_
  CONFIG = config
  bstack1l1lll1l1l_opy_ = bstack11ll11ll1l_opy_
def bstack1l1ll111l_opy_():
  global CONFIG
  global bstack1l1lll1l1l_opy_
  if bstack1ll11ll_opy_ (u"ࠩࡤࡴࡵ࠭੊") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1ll1l1l1_opy_(e, bstack1l111lll1l_opy_)
    bstack1l1lll1l1l_opy_ = True
    bstack1l111111l1_opy_.bstack11l111l1l_opy_(bstack1ll11ll_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩੋ"), True)
def bstack1l111l11l1_opy_(config):
  bstack11ll11ll1_opy_ = bstack1ll11ll_opy_ (u"ࠫࠬੌ")
  app = config[bstack1ll11ll_opy_ (u"ࠬࡧࡰࡱ੍ࠩ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1lll1lll_opy_:
      if os.path.exists(app):
        bstack11ll11ll1_opy_ = bstack1ll111ll_opy_(config, app)
      elif bstack1ll1ll111_opy_(app):
        bstack11ll11ll1_opy_ = app
      else:
        bstack1l1111111l_opy_(bstack11ll1l11_opy_.format(app))
    else:
      if bstack1ll1ll111_opy_(app):
        bstack11ll11ll1_opy_ = app
      elif os.path.exists(app):
        bstack11ll11ll1_opy_ = bstack1ll111ll_opy_(app)
      else:
        bstack1l1111111l_opy_(bstack11lll1lll1_opy_)
  else:
    if len(app) > 2:
      bstack1l1111111l_opy_(bstack11l1llll1l_opy_)
    elif len(app) == 2:
      if bstack1ll11ll_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ੎") in app and bstack1ll11ll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪ੏") in app:
        if os.path.exists(app[bstack1ll11ll_opy_ (u"ࠨࡲࡤࡸ࡭࠭੐")]):
          bstack11ll11ll1_opy_ = bstack1ll111ll_opy_(config, app[bstack1ll11ll_opy_ (u"ࠩࡳࡥࡹ࡮ࠧੑ")], app[bstack1ll11ll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭੒")])
        else:
          bstack1l1111111l_opy_(bstack11ll1l11_opy_.format(app))
      else:
        bstack1l1111111l_opy_(bstack11l1llll1l_opy_)
    else:
      for key in app:
        if key in bstack111l1ll11_opy_:
          if key == bstack1ll11ll_opy_ (u"ࠫࡵࡧࡴࡩࠩ੓"):
            if os.path.exists(app[key]):
              bstack11ll11ll1_opy_ = bstack1ll111ll_opy_(config, app[key])
            else:
              bstack1l1111111l_opy_(bstack11ll1l11_opy_.format(app))
          else:
            bstack11ll11ll1_opy_ = app[key]
        else:
          bstack1l1111111l_opy_(bstack11lll1l1ll_opy_)
  return bstack11ll11ll1_opy_
def bstack1ll1ll111_opy_(bstack11ll11ll1_opy_):
  import re
  bstack1ll1l11l11_opy_ = re.compile(bstack1ll11ll_opy_ (u"ࡷࠨ࡞࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭ࠨࠧ੔"))
  bstack1ll11lll_opy_ = re.compile(bstack1ll11ll_opy_ (u"ࡸࠢ࡟࡝ࡤ࠱ࡿࡇ࡛࠭࠲࠰࠽ࡡࡥ࠮࡝࠯ࡠ࠮࠴ࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫࠦࠥ੕"))
  if bstack1ll11ll_opy_ (u"ࠧࡣࡵ࠽࠳࠴࠭੖") in bstack11ll11ll1_opy_ or re.fullmatch(bstack1ll1l11l11_opy_, bstack11ll11ll1_opy_) or re.fullmatch(bstack1ll11lll_opy_, bstack11ll11ll1_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack11ll1l11l_opy_, stage=STAGE.bstack11lll1ll1l_opy_, bstack11ll1l1l_opy_=bstack111l1l11_opy_)
def bstack1ll111ll_opy_(config, path, bstack1ll1lllll1_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1ll11ll_opy_ (u"ࠨࡴࡥࠫ੗")).read()).hexdigest()
  bstack1l1111lll_opy_ = bstack111ll1ll1_opy_(md5_hash)
  bstack11ll11ll1_opy_ = None
  if bstack1l1111lll_opy_:
    logger.info(bstack11ll1ll11l_opy_.format(bstack1l1111lll_opy_, md5_hash))
    return bstack1l1111lll_opy_
  bstack1ll111l11_opy_ = datetime.datetime.now()
  bstack11llll11l_opy_ = MultipartEncoder(
    fields={
      bstack1ll11ll_opy_ (u"ࠩࡩ࡭ࡱ࡫ࠧ੘"): (os.path.basename(path), open(os.path.abspath(path), bstack1ll11ll_opy_ (u"ࠪࡶࡧ࠭ਖ਼")), bstack1ll11ll_opy_ (u"ࠫࡹ࡫ࡸࡵ࠱ࡳࡰࡦ࡯࡮ࠨਗ਼")),
      bstack1ll11ll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨਜ਼"): bstack1ll1lllll1_opy_
    }
  )
  response = requests.post(bstack11l11l111l_opy_, data=bstack11llll11l_opy_,
                           headers={bstack1ll11ll_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬੜ"): bstack11llll11l_opy_.content_type},
                           auth=(config[bstack1ll11ll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ੝")], config[bstack1ll11ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫਫ਼")]))
  try:
    res = json.loads(response.text)
    bstack11ll11ll1_opy_ = res[bstack1ll11ll_opy_ (u"ࠩࡤࡴࡵࡥࡵࡳ࡮ࠪ੟")]
    logger.info(bstack1l1lll11ll_opy_.format(bstack11ll11ll1_opy_))
    bstack1ll11l1111_opy_(md5_hash, bstack11ll11ll1_opy_)
    cli.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻ࡷࡳࡰࡴࡧࡤࡠࡣࡳࡴࠧ੠"), datetime.datetime.now() - bstack1ll111l11_opy_)
  except ValueError as err:
    bstack1l1111111l_opy_(bstack11ll1lll_opy_.format(str(err)))
  return bstack11ll11ll1_opy_
def bstack11l11l1ll_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack11l11ll1_opy_
  bstack1l111l1l_opy_ = 1
  bstack11l1l1l111_opy_ = 1
  if bstack1ll11ll_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ੡") in CONFIG:
    bstack11l1l1l111_opy_ = CONFIG[bstack1ll11ll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ੢")]
  else:
    bstack11l1l1l111_opy_ = bstack1l1l1ll111_opy_(framework_name, args) or 1
  if bstack1ll11ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ੣") in CONFIG:
    bstack1l111l1l_opy_ = len(CONFIG[bstack1ll11ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ੤")])
  bstack11l11ll1_opy_ = int(bstack11l1l1l111_opy_) * int(bstack1l111l1l_opy_)
def bstack1l1l1ll111_opy_(framework_name, args):
  if framework_name == bstack1ll1l111l1_opy_ and args and bstack1ll11ll_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭੥") in args:
      bstack11l1l1111_opy_ = args.index(bstack1ll11ll_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ੦"))
      return int(args[bstack11l1l1111_opy_ + 1]) or 1
  return 1
def bstack111ll1ll1_opy_(md5_hash):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1ll11ll_opy_ (u"ࠪࡪ࡮ࡲࡥ࡭ࡱࡦ࡯ࠥࡴ࡯ࡵࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩ࠱ࠦࡵࡴ࡫ࡱ࡫ࠥࡨࡡࡴ࡫ࡦࠤ࡫࡯࡬ࡦࠢࡲࡴࡪࡸࡡࡵ࡫ࡲࡲࡸ࠭੧"))
    bstack11111l111_opy_ = os.path.join(os.path.expanduser(bstack1ll11ll_opy_ (u"ࠫࢃ࠭੨")), bstack1ll11ll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ੩"), bstack1ll11ll_opy_ (u"࠭ࡡࡱࡲࡘࡴࡱࡵࡡࡥࡏࡇ࠹ࡍࡧࡳࡩ࠰࡭ࡷࡴࡴࠧ੪"))
    if os.path.exists(bstack11111l111_opy_):
      try:
        bstack1l1l1111l1_opy_ = json.load(open(bstack11111l111_opy_, bstack1ll11ll_opy_ (u"ࠧࡳࡤࠪ੫")))
        if md5_hash in bstack1l1l1111l1_opy_:
          bstack1ll111l11l_opy_ = bstack1l1l1111l1_opy_[md5_hash]
          bstack1ll1lll1l_opy_ = datetime.datetime.now()
          bstack1l1l1ll1l_opy_ = datetime.datetime.strptime(bstack1ll111l11l_opy_[bstack1ll11ll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ੬")], bstack1ll11ll_opy_ (u"ࠩࠨࡨ࠴ࠫ࡭࠰ࠧ࡜ࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭੭"))
          if (bstack1ll1lll1l_opy_ - bstack1l1l1ll1l_opy_).days > 30:
            return None
          elif version.parse(str(__version__)) > version.parse(bstack1ll111l11l_opy_[bstack1ll11ll_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ੮")]):
            return None
          return bstack1ll111l11l_opy_[bstack1ll11ll_opy_ (u"ࠫ࡮ࡪࠧ੯")]
      except Exception as e:
        logger.debug(bstack1ll11ll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡷ࡫ࡡࡥ࡫ࡱ࡫ࠥࡓࡄ࠶ࠢ࡫ࡥࡸ࡮ࠠࡧ࡫࡯ࡩ࠿ࠦࡻࡾࠩੰ").format(str(e)))
    return None
  bstack11111l111_opy_ = os.path.join(os.path.expanduser(bstack1ll11ll_opy_ (u"࠭ࡾࠨੱ")), bstack1ll11ll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧੲ"), bstack1ll11ll_opy_ (u"ࠨࡣࡳࡴ࡚ࡶ࡬ࡰࡣࡧࡑࡉ࠻ࡈࡢࡵ࡫࠲࡯ࡹ࡯࡯ࠩੳ"))
  lock_file = bstack11111l111_opy_ + bstack1ll11ll_opy_ (u"ࠩ࠱ࡰࡴࡩ࡫ࠨੴ")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack11111l111_opy_):
        with open(bstack11111l111_opy_, bstack1ll11ll_opy_ (u"ࠪࡶࠬੵ")) as f:
          content = f.read().strip()
          if content:
            bstack1l1l1111l1_opy_ = json.loads(content)
            if md5_hash in bstack1l1l1111l1_opy_:
              bstack1ll111l11l_opy_ = bstack1l1l1111l1_opy_[md5_hash]
              bstack1ll1lll1l_opy_ = datetime.datetime.now()
              bstack1l1l1ll1l_opy_ = datetime.datetime.strptime(bstack1ll111l11l_opy_[bstack1ll11ll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ੶")], bstack1ll11ll_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩ੷"))
              if (bstack1ll1lll1l_opy_ - bstack1l1l1ll1l_opy_).days > 30:
                return None
              elif version.parse(str(__version__)) > version.parse(bstack1ll111l11l_opy_[bstack1ll11ll_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ੸")]):
                return None
              return bstack1ll111l11l_opy_[bstack1ll11ll_opy_ (u"ࠧࡪࡦࠪ੹")]
      return None
  except Exception as e:
    logger.debug(bstack1ll11ll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡸ࡫ࡷ࡬ࠥ࡬ࡩ࡭ࡧࠣࡰࡴࡩ࡫ࡪࡰࡪࠤ࡫ࡵࡲࠡࡏࡇ࠹ࠥ࡮ࡡࡴࡪ࠽ࠤࢀࢃࠧ੺").format(str(e)))
    return None
def bstack1ll11l1111_opy_(md5_hash, bstack11ll11ll1_opy_):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1ll11ll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡬ࡰࡥ࡮ࠤࡳࡵࡴࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨ࠰ࠥࡻࡳࡪࡰࡪࠤࡧࡧࡳࡪࡥࠣࡪ࡮ࡲࡥࠡࡱࡳࡩࡷࡧࡴࡪࡱࡱࡷࠬ੻"))
    bstack1l1111lll1_opy_ = os.path.join(os.path.expanduser(bstack1ll11ll_opy_ (u"ࠪࢂࠬ੼")), bstack1ll11ll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ੽"))
    if not os.path.exists(bstack1l1111lll1_opy_):
      os.makedirs(bstack1l1111lll1_opy_)
    bstack11111l111_opy_ = os.path.join(os.path.expanduser(bstack1ll11ll_opy_ (u"ࠬࢄࠧ੾")), bstack1ll11ll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭੿"), bstack1ll11ll_opy_ (u"ࠧࡢࡲࡳ࡙ࡵࡲ࡯ࡢࡦࡐࡈ࠺ࡎࡡࡴࡪ࠱࡮ࡸࡵ࡮ࠨ઀"))
    bstack1111ll11_opy_ = {
      bstack1ll11ll_opy_ (u"ࠨ࡫ࡧࠫઁ"): bstack11ll11ll1_opy_,
      bstack1ll11ll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬં"): datetime.datetime.strftime(datetime.datetime.now(), bstack1ll11ll_opy_ (u"ࠪࠩࡩ࠵ࠥ࡮࠱ࠨ࡝ࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧઃ")),
      bstack1ll11ll_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ઄"): str(__version__)
    }
    try:
      bstack1l1l1111l1_opy_ = {}
      if os.path.exists(bstack11111l111_opy_):
        bstack1l1l1111l1_opy_ = json.load(open(bstack11111l111_opy_, bstack1ll11ll_opy_ (u"ࠬࡸࡢࠨઅ")))
      bstack1l1l1111l1_opy_[md5_hash] = bstack1111ll11_opy_
      with open(bstack11111l111_opy_, bstack1ll11ll_opy_ (u"ࠨࡷࠬࠤઆ")) as outfile:
        json.dump(bstack1l1l1111l1_opy_, outfile)
    except Exception as e:
      logger.debug(bstack1ll11ll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡵࡱࡦࡤࡸ࡮ࡴࡧࠡࡏࡇ࠹ࠥ࡮ࡡࡴࡪࠣࡪ࡮ࡲࡥ࠻ࠢࡾࢁࠬઇ").format(str(e)))
    return
  bstack1l1111lll1_opy_ = os.path.join(os.path.expanduser(bstack1ll11ll_opy_ (u"ࠨࢀࠪઈ")), bstack1ll11ll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩઉ"))
  if not os.path.exists(bstack1l1111lll1_opy_):
    os.makedirs(bstack1l1111lll1_opy_)
  bstack11111l111_opy_ = os.path.join(os.path.expanduser(bstack1ll11ll_opy_ (u"ࠪࢂࠬઊ")), bstack1ll11ll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫઋ"), bstack1ll11ll_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭ઌ"))
  lock_file = bstack11111l111_opy_ + bstack1ll11ll_opy_ (u"࠭࠮࡭ࡱࡦ࡯ࠬઍ")
  bstack1111ll11_opy_ = {
    bstack1ll11ll_opy_ (u"ࠧࡪࡦࠪ઎"): bstack11ll11ll1_opy_,
    bstack1ll11ll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫએ"): datetime.datetime.strftime(datetime.datetime.now(), bstack1ll11ll_opy_ (u"ࠩࠨࡨ࠴ࠫ࡭࠰ࠧ࡜ࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭ઐ")),
    bstack1ll11ll_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨઑ"): str(__version__)
  }
  try:
    with FileLock(lock_file, timeout=10):
      bstack1l1l1111l1_opy_ = {}
      if os.path.exists(bstack11111l111_opy_):
        with open(bstack11111l111_opy_, bstack1ll11ll_opy_ (u"ࠫࡷ࠭઒")) as f:
          content = f.read().strip()
          if content:
            bstack1l1l1111l1_opy_ = json.loads(content)
      bstack1l1l1111l1_opy_[md5_hash] = bstack1111ll11_opy_
      with open(bstack11111l111_opy_, bstack1ll11ll_opy_ (u"ࠧࡽࠢઓ")) as outfile:
        json.dump(bstack1l1l1111l1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1ll11ll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡽࡩࡵࡪࠣࡪ࡮ࡲࡥࠡ࡮ࡲࡧࡰ࡯࡮ࡨࠢࡩࡳࡷࠦࡍࡅ࠷ࠣ࡬ࡦࡹࡨࠡࡷࡳࡨࡦࡺࡥ࠻ࠢࡾࢁࠬઔ").format(str(e)))
def bstack11lll11l1l_opy_(self):
  return
def bstack11l1l11ll1_opy_(self):
  return
def bstack111lll1ll1_opy_():
  global bstack1ll1l1ll11_opy_
  bstack1ll1l1ll11_opy_ = True
@measure(event_name=EVENTS.bstack11l1l11l1l_opy_, stage=STAGE.bstack11lll1ll1l_opy_, bstack11ll1l1l_opy_=bstack111l1l11_opy_)
def bstack1llll1l11l_opy_(self):
  global bstack11l1lll1l1_opy_
  global bstack1ll1111ll1_opy_
  global bstack11l1111l1l_opy_
  try:
    if bstack1ll11ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧક") in bstack11l1lll1l1_opy_ and self.session_id != None and bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬખ"), bstack1ll11ll_opy_ (u"ࠩࠪગ")) != bstack1ll11ll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫઘ"):
      bstack1l1ll1l11_opy_ = bstack1ll11ll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫઙ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1ll11ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬચ")
      if bstack1l1ll1l11_opy_ == bstack1ll11ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭છ"):
        bstack1ll1l11l_opy_(logger)
      if self != None:
        bstack1l11lllll1_opy_(self, bstack1l1ll1l11_opy_, bstack1ll11ll_opy_ (u"ࠧ࠭ࠢࠪજ").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack1ll11ll_opy_ (u"ࠨࠩઝ")
    if bstack1ll11ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩઞ") in bstack11l1lll1l1_opy_ and getattr(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩટ"), None):
      bstack1l11l11l1l_opy_.bstack1llll11l_opy_(self, bstack11l11l11l1_opy_, logger, wait=True)
    if bstack1ll11ll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫઠ") in bstack11l1lll1l1_opy_:
      if not threading.currentThread().behave_test_status:
        bstack1l11lllll1_opy_(self, bstack1ll11ll_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧડ"))
      bstack1ll1l111l_opy_.bstack1l1111111_opy_(self)
  except Exception as e:
    logger.debug(bstack1ll11ll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࠢઢ") + str(e))
  bstack11l1111l1l_opy_(self)
  self.session_id = None
def bstack11l1ll1l_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack1l1l11l1ll_opy_
    global bstack11l1lll1l1_opy_
    command_executor = kwargs.get(bstack1ll11ll_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠪણ"), bstack1ll11ll_opy_ (u"ࠨࠩત"))
    bstack1llll11l1_opy_ = False
    if type(command_executor) == str and bstack1ll11ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬથ") in command_executor:
      bstack1llll11l1_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack1ll11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭દ") in str(getattr(command_executor, bstack1ll11ll_opy_ (u"ࠫࡤࡻࡲ࡭ࠩધ"), bstack1ll11ll_opy_ (u"ࠬ࠭ન"))):
      bstack1llll11l1_opy_ = True
    else:
      kwargs = bstack1l1l11l1l1_opy_.bstack11ll111ll_opy_(bstack1l111lll1_opy_=kwargs, config=CONFIG)
      return bstack1lll11ll11_opy_(self, *args, **kwargs)
    if bstack1llll11l1_opy_:
      bstack1l1l1111l_opy_ = bstack111llll11l_opy_.bstack111lll11l_opy_(CONFIG, bstack11l1lll1l1_opy_)
      if kwargs.get(bstack1ll11ll_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧ઩")):
        kwargs[bstack1ll11ll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨપ")] = bstack1l1l11l1ll_opy_(kwargs[bstack1ll11ll_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩફ")], bstack11l1lll1l1_opy_, CONFIG, bstack1l1l1111l_opy_)
      elif kwargs.get(bstack1ll11ll_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩબ")):
        kwargs[bstack1ll11ll_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪભ")] = bstack1l1l11l1ll_opy_(kwargs[bstack1ll11ll_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫમ")], bstack11l1lll1l1_opy_, CONFIG, bstack1l1l1111l_opy_)
  except Exception as e:
    logger.error(bstack1ll11ll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡥ࡯ࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡓࡅࡍࠣࡧࡦࡶࡳ࠻ࠢࡾࢁࠧય").format(str(e)))
  return bstack1lll11ll11_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack11l11lll1_opy_, stage=STAGE.bstack11lll1ll1l_opy_, bstack11ll1l1l_opy_=bstack111l1l11_opy_)
def bstack11lll1111_opy_(self, command_executor=bstack1ll11ll_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵࠱࠳࠹࠱࠴࠳࠶࠮࠲࠼࠷࠸࠹࠺ࠢર"), *args, **kwargs):
  global bstack1ll1111ll1_opy_
  global bstack1lll1ll1l1_opy_
  bstack1ll11l111_opy_ = bstack11l1ll1l_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack11lllllll1_opy_.on():
    return bstack1ll11l111_opy_
  try:
    logger.debug(bstack1ll11ll_opy_ (u"ࠧࡄࡱࡰࡱࡦࡴࡤࠡࡇࡻࡩࡨࡻࡴࡰࡴࠣࡻ࡭࡫࡮ࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤ࡮ࡹࠠࡧࡣ࡯ࡷࡪࠦ࠭ࠡࡽࢀࠫ઱").format(str(command_executor)))
    logger.debug(bstack1ll11ll_opy_ (u"ࠨࡊࡸࡦ࡛ࠥࡒࡍࠢ࡬ࡷࠥ࠳ࠠࡼࡿࠪલ").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack1ll11ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬળ") in command_executor._url:
      bstack1l111111l1_opy_.bstack11l111l1l_opy_(bstack1ll11ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫ઴"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack1ll11ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧવ") in command_executor):
    bstack1l111111l1_opy_.bstack11l111l1l_opy_(bstack1ll11ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭શ"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1l1l1l1l_opy_ = getattr(threading.current_thread(), bstack1ll11ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡚ࡥࡴࡶࡐࡩࡹࡧࠧષ"), None)
  bstack11llllllll_opy_ = {}
  if self.capabilities is not None:
    bstack11llllllll_opy_[bstack1ll11ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡰࡤࡱࡪ࠭સ")] = self.capabilities.get(bstack1ll11ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭હ"))
    bstack11llllllll_opy_[bstack1ll11ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫ઺")] = self.capabilities.get(bstack1ll11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ઻"))
    bstack11llllllll_opy_[bstack1ll11ll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡣࡴࡶࡴࡪࡱࡱࡷ઼ࠬ")] = self.capabilities.get(bstack1ll11ll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪઽ"))
  if CONFIG.get(bstack1ll11ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ા"), False) and bstack1l1l11l1l1_opy_.bstack1l111l1l1_opy_(bstack11llllllll_opy_):
    threading.current_thread().a11yPlatform = True
  if bstack1ll11ll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧિ") in bstack11l1lll1l1_opy_ or bstack1ll11ll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧી") in bstack11l1lll1l1_opy_:
    bstack1l11ll1l_opy_.bstack111llll1_opy_(self)
  if bstack1ll11ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩુ") in bstack11l1lll1l1_opy_ and bstack1l1l1l1l_opy_ and bstack1l1l1l1l_opy_.get(bstack1ll11ll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪૂ"), bstack1ll11ll_opy_ (u"ࠫࠬૃ")) == bstack1ll11ll_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭ૄ"):
    bstack1l11ll1l_opy_.bstack111llll1_opy_(self)
  bstack1ll1111ll1_opy_ = self.session_id
  with bstack11ll111l_opy_:
    bstack1lll1ll1l1_opy_.append(self)
  return bstack1ll11l111_opy_
def bstack11l111111l_opy_(args):
  return bstack1ll11ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠧૅ") in str(args)
def bstack111lll111_opy_(self, driver_command, *args, **kwargs):
  global bstack1ll1llll1_opy_
  global bstack1111l111l_opy_
  bstack11l1111l11_opy_ = bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ૆"), None) and bstack1111l1l11_opy_(
          threading.current_thread(), bstack1ll11ll_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧે"), None)
  bstack1111l111_opy_ = bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩૈ"), None) and bstack1111l1l11_opy_(
          threading.current_thread(), bstack1ll11ll_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬૉ"), None)
  bstack1l11lll11l_opy_ = getattr(self, bstack1ll11ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫ૊"), None) != None and getattr(self, bstack1ll11ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬો"), None) == True
  if not bstack1111l111l_opy_ and bstack1ll11ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ૌ") in CONFIG and CONFIG[bstack1ll11ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ્ࠧ")] == True and bstack1llll111_opy_.bstack1ll1l1llll_opy_(driver_command) and (bstack1l11lll11l_opy_ or bstack11l1111l11_opy_ or bstack1111l111_opy_) and not bstack11l111111l_opy_(args):
    try:
      bstack1111l111l_opy_ = True
      logger.debug(bstack1ll11ll_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡪࡴࡸࠠࡼࡿࠪ૎").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack1ll11ll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡥࡳࡨࡲࡶࡲࠦࡳࡤࡣࡱࠤࢀࢃࠧ૏").format(str(err)))
    bstack1111l111l_opy_ = False
  response = bstack1ll1llll1_opy_(self, driver_command, *args, **kwargs)
  if (bstack1ll11ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩૐ") in str(bstack11l1lll1l1_opy_).lower() or bstack1ll11ll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ૑") in str(bstack11l1lll1l1_opy_).lower()) and bstack11lllllll1_opy_.on():
    try:
      if driver_command == bstack1ll11ll_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠩ૒"):
        bstack1l11ll1l_opy_.bstack1111l1111_opy_({
            bstack1ll11ll_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬ૓"): response[bstack1ll11ll_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭૔")],
            bstack1ll11ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ૕"): bstack1l11ll1l_opy_.current_test_uuid() if bstack1l11ll1l_opy_.current_test_uuid() else bstack11lllllll1_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
@measure(event_name=EVENTS.bstack11l11ll1l_opy_, stage=STAGE.bstack11lll1ll1l_opy_, bstack11ll1l1l_opy_=bstack111l1l11_opy_)
def bstack11ll1ll111_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack1ll1111ll1_opy_
  global bstack11l111lll_opy_
  global bstack111l1l11_opy_
  global bstack111llll1ll_opy_
  global bstack111llll1l1_opy_
  global bstack11l1lll1l1_opy_
  global bstack1lll11ll11_opy_
  global bstack1lll1ll1l1_opy_
  global bstack1l1lll1l_opy_
  global bstack11l11l11l1_opy_
  if os.getenv(bstack1ll11ll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ૖")) is not None and bstack1l1l11l1l1_opy_.bstack1llllll1ll_opy_(CONFIG) is None:
    CONFIG[bstack1ll11ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ૗")] = True
  CONFIG[bstack1ll11ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭૘")] = str(bstack11l1lll1l1_opy_) + str(__version__)
  bstack11ll11l11_opy_ = os.environ[bstack1ll11ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ૙")]
  bstack1l1l1111l_opy_ = bstack111llll11l_opy_.bstack111lll11l_opy_(CONFIG, bstack11l1lll1l1_opy_)
  CONFIG[bstack1ll11ll_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ૚")] = bstack11ll11l11_opy_
  CONFIG[bstack1ll11ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩ૛")] = bstack1l1l1111l_opy_
  if CONFIG.get(bstack1ll11ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ૜"),bstack1ll11ll_opy_ (u"ࠩࠪ૝")) and bstack1ll11ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ૞") in bstack11l1lll1l1_opy_:
    CONFIG[bstack1ll11ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ૟")].pop(bstack1ll11ll_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪૠ"), None)
    CONFIG[bstack1ll11ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ૡ")].pop(bstack1ll11ll_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬૢ"), None)
  command_executor = bstack11lll111l1_opy_()
  logger.debug(bstack11111111_opy_.format(command_executor))
  proxy = bstack1ll1llll1l_opy_(CONFIG, proxy)
  bstack11llll111l_opy_ = 0 if bstack11l111lll_opy_ < 0 else bstack11l111lll_opy_
  try:
    if bstack111llll1ll_opy_ is True:
      bstack11llll111l_opy_ = int(multiprocessing.current_process().name)
    elif bstack111llll1l1_opy_ is True:
      bstack11llll111l_opy_ = int(threading.current_thread().name)
  except:
    bstack11llll111l_opy_ = 0
  bstack1l111llll_opy_ = bstack11lllllll_opy_(CONFIG, bstack11llll111l_opy_)
  logger.debug(bstack1l11ll1ll_opy_.format(str(bstack1l111llll_opy_)))
  if bstack1ll11ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬૣ") in CONFIG and bstack1l1l1llll1_opy_(CONFIG[bstack1ll11ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭૤")]):
    bstack11ll1l111_opy_(bstack1l111llll_opy_)
  if bstack1l1l11l1l1_opy_.bstack1l1l1lll1l_opy_(CONFIG, bstack11llll111l_opy_) and bstack1l1l11l1l1_opy_.bstack11ll1l1l1_opy_(bstack1l111llll_opy_, options, desired_capabilities, CONFIG):
    threading.current_thread().a11yPlatform = True
    if (cli.accessibility is None or not cli.accessibility.is_enabled()):
      bstack1l1l11l1l1_opy_.set_capabilities(bstack1l111llll_opy_, CONFIG)
  if desired_capabilities:
    bstack1lllll11l1_opy_ = bstack1lll11l1l_opy_(desired_capabilities)
    bstack1lllll11l1_opy_[bstack1ll11ll_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ૥")] = bstack1l11l1llll_opy_(CONFIG)
    bstack1l1111l11l_opy_ = bstack11lllllll_opy_(bstack1lllll11l1_opy_)
    if bstack1l1111l11l_opy_:
      bstack1l111llll_opy_ = update(bstack1l1111l11l_opy_, bstack1l111llll_opy_)
    desired_capabilities = None
  if options:
    bstack111111l11_opy_(options, bstack1l111llll_opy_)
  if not options:
    options = bstack1ll11111ll_opy_(bstack1l111llll_opy_)
  bstack11l11l11l1_opy_ = CONFIG.get(bstack1ll11ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ૦"))[bstack11llll111l_opy_]
  if proxy and bstack1l11111111_opy_() >= version.parse(bstack1ll11ll_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬ૧")):
    options.proxy(proxy)
  if options and bstack1l11111111_opy_() >= version.parse(bstack1ll11ll_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ૨")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1l11111111_opy_() < version.parse(bstack1ll11ll_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭૩")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1l111llll_opy_)
  logger.info(bstack1lll1ll1ll_opy_)
  bstack1l1ll11l1l_opy_.end(EVENTS.bstack11ll1l111l_opy_.value, EVENTS.bstack11ll1l111l_opy_.value + bstack1ll11ll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ૪"), EVENTS.bstack11ll1l111l_opy_.value + bstack1ll11ll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ૫"), status=True, failure=None, test_name=bstack111l1l11_opy_)
  if bstack1ll11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡵࡸ࡯ࡧ࡫࡯ࡩࠬ૬") in kwargs:
    del kwargs[bstack1ll11ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡶࡲࡰࡨ࡬ࡰࡪ࠭૭")]
  try:
    if bstack1l11111111_opy_() >= version.parse(bstack1ll11ll_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬ૮")):
      bstack1lll11ll11_opy_(self, command_executor=command_executor,
                options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
    elif bstack1l11111111_opy_() >= version.parse(bstack1ll11ll_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ૯")):
      bstack1lll11ll11_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities, options=options,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l11111111_opy_() >= version.parse(bstack1ll11ll_opy_ (u"ࠧ࠳࠰࠸࠷࠳࠶ࠧ૰")):
      bstack1lll11ll11_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    else:
      bstack1lll11ll11_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive)
  except Exception as bstack1l1l111l1_opy_:
    logger.error(bstack11l11l111_opy_.format(bstack1ll11ll_opy_ (u"ࠨࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠧ૱"), str(bstack1l1l111l1_opy_)))
    raise bstack1l1l111l1_opy_
  if bstack1l1l11l1l1_opy_.bstack1l1l1lll1l_opy_(CONFIG, bstack11llll111l_opy_) and bstack1l1l11l1l1_opy_.bstack11ll1l1l1_opy_(self.caps, options, desired_capabilities):
    if CONFIG[bstack1ll11ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ૲")][bstack1ll11ll_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩ૳")] == True:
      threading.current_thread().appA11yPlatform = True
      if cli.accessibility is None or not cli.accessibility.is_enabled():
        bstack1l1l11l1l1_opy_.set_capabilities(bstack1l111llll_opy_, CONFIG)
  try:
    bstack111l1l11l_opy_ = bstack1ll11ll_opy_ (u"ࠫࠬ૴")
    if bstack1l11111111_opy_() >= version.parse(bstack1ll11ll_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭૵")):
      if self.caps is not None:
        bstack111l1l11l_opy_ = self.caps.get(bstack1ll11ll_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨ૶"))
    else:
      if self.capabilities is not None:
        bstack111l1l11l_opy_ = self.capabilities.get(bstack1ll11ll_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢ૷"))
    if bstack111l1l11l_opy_:
      bstack1l1l11lll1_opy_(bstack111l1l11l_opy_)
      if bstack1l11111111_opy_() <= version.parse(bstack1ll11ll_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨ૸")):
        self.command_executor._url = bstack1ll11ll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥૹ") + bstack11lll1lll_opy_ + bstack1ll11ll_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢૺ")
      else:
        self.command_executor._url = bstack1ll11ll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨૻ") + bstack111l1l11l_opy_ + bstack1ll11ll_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨૼ")
      logger.debug(bstack1lll11lll_opy_.format(bstack111l1l11l_opy_))
    else:
      logger.debug(bstack1llll11ll_opy_.format(bstack1ll11ll_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢ૽")))
  except Exception as e:
    logger.debug(bstack1llll11ll_opy_.format(e))
  if bstack1ll11ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭૾") in bstack11l1lll1l1_opy_:
    bstack1lllll1ll_opy_(bstack11l111lll_opy_, bstack1l1lll1l_opy_)
  bstack1ll1111ll1_opy_ = self.session_id
  if bstack1ll11ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ૿") in bstack11l1lll1l1_opy_ or bstack1ll11ll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ଀") in bstack11l1lll1l1_opy_ or bstack1ll11ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩଁ") in bstack11l1lll1l1_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack1l1l1l1l_opy_ = getattr(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡘࡪࡹࡴࡎࡧࡷࡥࠬଂ"), None)
  if bstack1ll11ll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬଃ") in bstack11l1lll1l1_opy_ or bstack1ll11ll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ଄") in bstack11l1lll1l1_opy_:
    bstack1l11ll1l_opy_.bstack111llll1_opy_(self)
  if bstack1ll11ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧଅ") in bstack11l1lll1l1_opy_ and bstack1l1l1l1l_opy_ and bstack1l1l1l1l_opy_.get(bstack1ll11ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨଆ"), bstack1ll11ll_opy_ (u"ࠩࠪଇ")) == bstack1ll11ll_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫଈ"):
    bstack1l11ll1l_opy_.bstack111llll1_opy_(self)
  with bstack11ll111l_opy_:
    bstack1lll1ll1l1_opy_.append(self)
  if bstack1ll11ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଉ") in CONFIG and bstack1ll11ll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪଊ") in CONFIG[bstack1ll11ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଋ")][bstack11llll111l_opy_]:
    bstack111l1l11_opy_ = CONFIG[bstack1ll11ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଌ")][bstack11llll111l_opy_][bstack1ll11ll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭଍")]
  logger.debug(bstack1l1l111l11_opy_.format(bstack1ll1111ll1_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    from browserstack_sdk.__init__ import bstack11ll1llll_opy_
    def bstack1lll1l1l_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1l1l1lll1_opy_
      if(bstack1ll11ll_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸ࠯࡬ࡶࠦ଎") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1ll11ll_opy_ (u"ࠪࢂࠬଏ")), bstack1ll11ll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫଐ"), bstack1ll11ll_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧ଑")), bstack1ll11ll_opy_ (u"࠭ࡷࠨ଒")) as fp:
          fp.write(bstack1ll11ll_opy_ (u"ࠢࠣଓ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1ll11ll_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥଔ")))):
          with open(args[1], bstack1ll11ll_opy_ (u"ࠩࡵࠫକ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1ll11ll_opy_ (u"ࠪࡥࡸࡿ࡮ࡤࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࡤࡴࡥࡸࡒࡤ࡫ࡪ࠮ࡣࡰࡰࡷࡩࡽࡺࠬࠡࡲࡤ࡫ࡪࠦ࠽ࠡࡸࡲ࡭ࡩࠦ࠰ࠪࠩଖ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1111l11l_opy_)
            if bstack1ll11ll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨଗ") in CONFIG and str(CONFIG[bstack1ll11ll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩଘ")]).lower() != bstack1ll11ll_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬଙ"):
                bstack1l11l1lll_opy_ = bstack11ll1llll_opy_()
                bstack1l11l111l1_opy_ = bstack1ll11ll_opy_ (u"ࠧࠨࠩࠍ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࠐࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹࡝࠼ࠌࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠ࠿ࠏࡩ࡯࡯ࡵࡷࠤࡵࡥࡩ࡯ࡦࡨࡼࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠳࡟࠾ࠎࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡸࡲࡩࡤࡧࠫ࠴࠱ࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴ࠫ࠾ࠎࡨࡵ࡮ࡴࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫ࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤࠬ࠿ࠏ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡲࡡࡶࡰࡦ࡬ࠥࡃࠠࡢࡵࡼࡲࡨࠦࠨ࡭ࡣࡸࡲࡨ࡮ࡏࡱࡶ࡬ࡳࡳࡹࠩࠡ࠿ࡁࠤࢀࢁࠊࠡࠢ࡯ࡩࡹࠦࡣࡢࡲࡶ࠿ࠏࠦࠠࡵࡴࡼࠤࢀࢁࠊࠡࠢࠣࠤࡨࡧࡰࡴࠢࡀࠤࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸ࠯࠻ࠋࠢࠣࢁࢂࠦࡣࡢࡶࡦ࡬ࠥ࠮ࡥࡹࠫࠣࡿࢀࠐࠠࠡࠢࠣࡧࡴࡴࡳࡰ࡮ࡨ࠲ࡪࡸࡲࡰࡴࠫࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷ࠿ࠨࠬࠡࡧࡻ࠭ࡀࠐࠠࠡࡿࢀࠎࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡩ࡯࡯ࡰࡨࡧࡹ࠮ࡻࡼࠌࠣࠤࠥࠦࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶ࠽ࠤࠬࢁࡣࡥࡲࡘࡶࡱࢃࠧࠡ࠭ࠣࡩࡳࡩ࡯ࡥࡧࡘࡖࡎࡉ࡯࡮ࡲࡲࡲࡪࡴࡴࠩࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡦࡥࡵࡹࠩࠪ࠮ࠍࠤࠥࠦࠠ࠯࠰࠱ࡰࡦࡻ࡮ࡤࡪࡒࡴࡹ࡯࡯࡯ࡵࠍࠤࠥࢃࡽࠪ࠽ࠍࢁࢂࡁࠊ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱ࠍࠫࠬ࠭ଚ").format(bstack1l11l1lll_opy_=bstack1l11l1lll_opy_)
            lines.insert(1, bstack1l11l111l1_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1ll11ll_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥଛ")), bstack1ll11ll_opy_ (u"ࠩࡺࠫଜ")) as bstack1lll1111ll_opy_:
              bstack1lll1111ll_opy_.writelines(lines)
        CONFIG[bstack1ll11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬଝ")] = str(bstack11l1lll1l1_opy_) + str(__version__)
        bstack11ll11l11_opy_ = os.environ[bstack1ll11ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩଞ")]
        bstack1l1l1111l_opy_ = bstack111llll11l_opy_.bstack111lll11l_opy_(CONFIG, bstack11l1lll1l1_opy_)
        CONFIG[bstack1ll11ll_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨଟ")] = bstack11ll11l11_opy_
        CONFIG[bstack1ll11ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨଠ")] = bstack1l1l1111l_opy_
        bstack11llll111l_opy_ = 0 if bstack11l111lll_opy_ < 0 else bstack11l111lll_opy_
        try:
          if bstack111llll1ll_opy_ is True:
            bstack11llll111l_opy_ = int(multiprocessing.current_process().name)
          elif bstack111llll1l1_opy_ is True:
            bstack11llll111l_opy_ = int(threading.current_thread().name)
        except:
          bstack11llll111l_opy_ = 0
        CONFIG[bstack1ll11ll_opy_ (u"ࠢࡶࡵࡨ࡛࠸ࡉࠢଡ")] = False
        CONFIG[bstack1ll11ll_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢଢ")] = True
        bstack1l111llll_opy_ = bstack11lllllll_opy_(CONFIG, bstack11llll111l_opy_)
        logger.debug(bstack1l11ll1ll_opy_.format(str(bstack1l111llll_opy_)))
        if CONFIG.get(bstack1ll11ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ଣ")):
          bstack11ll1l111_opy_(bstack1l111llll_opy_)
        if bstack1ll11ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ତ") in CONFIG and bstack1ll11ll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩଥ") in CONFIG[bstack1ll11ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨଦ")][bstack11llll111l_opy_]:
          bstack111l1l11_opy_ = CONFIG[bstack1ll11ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଧ")][bstack11llll111l_opy_][bstack1ll11ll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬନ")]
        args.append(os.path.join(os.path.expanduser(bstack1ll11ll_opy_ (u"ࠨࢀࠪ଩")), bstack1ll11ll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩପ"), bstack1ll11ll_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬଫ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1l111llll_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1ll11ll_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨବ"))
      bstack1l1l1lll1_opy_ = True
      return bstack11l1111ll1_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1ll11l1l1l_opy_(self,
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
    global bstack11l111lll_opy_
    global bstack111l1l11_opy_
    global bstack111llll1ll_opy_
    global bstack111llll1l1_opy_
    global bstack11l1lll1l1_opy_
    CONFIG[bstack1ll11ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧଭ")] = str(bstack11l1lll1l1_opy_) + str(__version__)
    bstack11ll11l11_opy_ = os.environ[bstack1ll11ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫମ")]
    bstack1l1l1111l_opy_ = bstack111llll11l_opy_.bstack111lll11l_opy_(CONFIG, bstack11l1lll1l1_opy_)
    CONFIG[bstack1ll11ll_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪଯ")] = bstack11ll11l11_opy_
    CONFIG[bstack1ll11ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪର")] = bstack1l1l1111l_opy_
    bstack11llll111l_opy_ = 0 if bstack11l111lll_opy_ < 0 else bstack11l111lll_opy_
    try:
      if bstack111llll1ll_opy_ is True:
        bstack11llll111l_opy_ = int(multiprocessing.current_process().name)
      elif bstack111llll1l1_opy_ is True:
        bstack11llll111l_opy_ = int(threading.current_thread().name)
    except:
      bstack11llll111l_opy_ = 0
    CONFIG[bstack1ll11ll_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ଱")] = True
    bstack1l111llll_opy_ = bstack11lllllll_opy_(CONFIG, bstack11llll111l_opy_)
    logger.debug(bstack1l11ll1ll_opy_.format(str(bstack1l111llll_opy_)))
    if CONFIG.get(bstack1ll11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧଲ")):
      bstack11ll1l111_opy_(bstack1l111llll_opy_)
    if bstack1ll11ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଳ") in CONFIG and bstack1ll11ll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ଴") in CONFIG[bstack1ll11ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଵ")][bstack11llll111l_opy_]:
      bstack111l1l11_opy_ = CONFIG[bstack1ll11ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଶ")][bstack11llll111l_opy_][bstack1ll11ll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ଷ")]
    import urllib
    import json
    if bstack1ll11ll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ସ") in CONFIG and str(CONFIG[bstack1ll11ll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧହ")]).lower() != bstack1ll11ll_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪ଺"):
        bstack11lll1l11_opy_ = bstack11ll1llll_opy_()
        bstack1l11l1lll_opy_ = bstack11lll1l11_opy_ + urllib.parse.quote(json.dumps(bstack1l111llll_opy_))
    else:
        bstack1l11l1lll_opy_ = bstack1ll11ll_opy_ (u"ࠬࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠧ଻") + urllib.parse.quote(json.dumps(bstack1l111llll_opy_))
    browser = self.connect(bstack1l11l1lll_opy_)
    return browser
except Exception as e:
    pass
def bstack111ll1ll_opy_():
    global bstack1l1l1lll1_opy_
    global bstack11l1lll1l1_opy_
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack11111111l_opy_
        global bstack1l111111l1_opy_
        if not bstack11l1ll11l_opy_:
          global bstack11l1l111_opy_
          if not bstack11l1l111_opy_:
            from bstack_utils.helper import bstack1ll1l1lll1_opy_, bstack11ll1l1ll1_opy_, bstack1l111l1l1l_opy_
            bstack11l1l111_opy_ = bstack1ll1l1lll1_opy_()
            bstack11ll1l1ll1_opy_(bstack11l1lll1l1_opy_)
            bstack1l1l1111l_opy_ = bstack111llll11l_opy_.bstack111lll11l_opy_(CONFIG, bstack11l1lll1l1_opy_)
            bstack1l111111l1_opy_.bstack11l111l1l_opy_(bstack1ll11ll_opy_ (u"ࠨࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡔࡗࡕࡄࡖࡅࡗࡣࡒࡇࡐ଼ࠣ"), bstack1l1l1111l_opy_)
          BrowserType.connect = bstack11111111l_opy_
          return
        BrowserType.launch = bstack1ll11l1l1l_opy_
        bstack1l1l1lll1_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1lll1l1l_opy_
      bstack1l1l1lll1_opy_ = True
    except Exception as e:
      pass
def bstack11l1l11111_opy_(context, bstack11l1l111ll_opy_):
  try:
    context.page.evaluate(bstack1ll11ll_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣଽ"), bstack1ll11ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬା")+ json.dumps(bstack11l1l111ll_opy_) + bstack1ll11ll_opy_ (u"ࠤࢀࢁࠧି"))
  except Exception as e:
    logger.debug(bstack1ll11ll_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽ࠻ࠢࡾࢁࠧୀ").format(str(e), traceback.format_exc()))
def bstack1ll11lll11_opy_(context, message, level):
  try:
    context.page.evaluate(bstack1ll11ll_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧୁ"), bstack1ll11ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪୂ") + json.dumps(message) + bstack1ll11ll_opy_ (u"࠭ࠬࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠩୃ") + json.dumps(level) + bstack1ll11ll_opy_ (u"ࠧࡾࡿࠪୄ"))
  except Exception as e:
    logger.debug(bstack1ll11ll_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡࡽࢀ࠾ࠥࢁࡽࠣ୅").format(str(e), traceback.format_exc()))
@measure(event_name=EVENTS.bstack11ll1ll1_opy_, stage=STAGE.bstack11lll1ll1l_opy_, bstack11ll1l1l_opy_=bstack111l1l11_opy_)
def bstack1llllll1l1_opy_(self, url):
  global bstack111l11l1l_opy_
  try:
    bstack1ll1ll1l1l_opy_(url)
  except Exception as err:
    logger.debug(bstack1l1l1111_opy_.format(str(err)))
  try:
    bstack111l11l1l_opy_(self, url)
  except Exception as e:
    try:
      bstack1l111l1111_opy_ = str(e)
      if any(err_msg in bstack1l111l1111_opy_ for err_msg in bstack1l1l1l111l_opy_):
        bstack1ll1ll1l1l_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1l1l1111_opy_.format(str(err)))
    raise e
def bstack1l1l11llll_opy_(self):
  global bstack1l1l1ll11l_opy_
  bstack1l1l1ll11l_opy_ = self
  return
def bstack11l1l11ll_opy_(self):
  global bstack1ll11111l_opy_
  bstack1ll11111l_opy_ = self
  return
def bstack111lll11_opy_(test_name, bstack1l1lll1111_opy_):
  global CONFIG
  if percy.bstack11ll1ll1l_opy_() == bstack1ll11ll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ୆"):
    bstack11l1l111l1_opy_ = os.path.relpath(bstack1l1lll1111_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack11l1l111l1_opy_)
    bstack11ll1l1l_opy_ = suite_name + bstack1ll11ll_opy_ (u"ࠥ࠱ࠧେ") + test_name
    threading.current_thread().percySessionName = bstack11ll1l1l_opy_
def bstack11lll1111l_opy_(self, test, *args, **kwargs):
  global bstack111111ll1_opy_
  test_name = None
  bstack1l1lll1111_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1l1lll1111_opy_ = str(test.source)
  bstack111lll11_opy_(test_name, bstack1l1lll1111_opy_)
  bstack111111ll1_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.bstack1ll1111l_opy_, stage=STAGE.bstack11lll1ll1l_opy_, bstack11ll1l1l_opy_=bstack111l1l11_opy_)
def bstack11lll11ll1_opy_(driver, bstack11ll1l1l_opy_):
  if not bstack11l1111ll_opy_ and bstack11ll1l1l_opy_:
      bstack111ll111l_opy_ = {
          bstack1ll11ll_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫୈ"): bstack1ll11ll_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭୉"),
          bstack1ll11ll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ୊"): {
              bstack1ll11ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬୋ"): bstack11ll1l1l_opy_
          }
      }
      bstack111111l1_opy_ = bstack1ll11ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ୌ").format(json.dumps(bstack111ll111l_opy_))
      driver.execute_script(bstack111111l1_opy_)
  if bstack1l1l1l1l1_opy_:
      bstack11l1lll1_opy_ = {
          bstack1ll11ll_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯୍ࠩ"): bstack1ll11ll_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬ୎"),
          bstack1ll11ll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ୏"): {
              bstack1ll11ll_opy_ (u"ࠬࡪࡡࡵࡣࠪ୐"): bstack11ll1l1l_opy_ + bstack1ll11ll_opy_ (u"࠭ࠠࡱࡣࡶࡷࡪࡪࠡࠨ୑"),
              bstack1ll11ll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭୒"): bstack1ll11ll_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭୓")
          }
      }
      if bstack1l1l1l1l1_opy_.status == bstack1ll11ll_opy_ (u"ࠩࡓࡅࡘ࡙ࠧ୔"):
          bstack1ll11ll1l1_opy_ = bstack1ll11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨ୕").format(json.dumps(bstack11l1lll1_opy_))
          driver.execute_script(bstack1ll11ll1l1_opy_)
          bstack1l11lllll1_opy_(driver, bstack1ll11ll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫୖ"))
      elif bstack1l1l1l1l1_opy_.status == bstack1ll11ll_opy_ (u"ࠬࡌࡁࡊࡎࠪୗ"):
          reason = bstack1ll11ll_opy_ (u"ࠨࠢ୘")
          bstack111l1111_opy_ = bstack11ll1l1l_opy_ + bstack1ll11ll_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠨ୙")
          if bstack1l1l1l1l1_opy_.message:
              reason = str(bstack1l1l1l1l1_opy_.message)
              bstack111l1111_opy_ = bstack111l1111_opy_ + bstack1ll11ll_opy_ (u"ࠨࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࡀࠠࠨ୚") + reason
          bstack11l1lll1_opy_[bstack1ll11ll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ୛")] = {
              bstack1ll11ll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩଡ଼"): bstack1ll11ll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪଢ଼"),
              bstack1ll11ll_opy_ (u"ࠬࡪࡡࡵࡣࠪ୞"): bstack111l1111_opy_
          }
          bstack1ll11ll1l1_opy_ = bstack1ll11ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫୟ").format(json.dumps(bstack11l1lll1_opy_))
          driver.execute_script(bstack1ll11ll1l1_opy_)
          bstack1l11lllll1_opy_(driver, bstack1ll11ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧୠ"), reason)
          bstack1l1ll1l11l_opy_(reason, str(bstack1l1l1l1l1_opy_), str(bstack11l111lll_opy_), logger)
@measure(event_name=EVENTS.bstack1llll1l1l1_opy_, stage=STAGE.bstack11lll1ll1l_opy_, bstack11ll1l1l_opy_=bstack111l1l11_opy_)
def bstack1l1l111ll1_opy_(driver, test):
  if percy.bstack11ll1ll1l_opy_() == bstack1ll11ll_opy_ (u"ࠣࡶࡵࡹࡪࠨୡ") and percy.bstack1l11ll1ll1_opy_() == bstack1ll11ll_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦୢ"):
      bstack11l111l1l1_opy_ = bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠪࡴࡪࡸࡣࡺࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ୣ"), None)
      bstack1lll1l11ll_opy_(driver, bstack11l111l1l1_opy_, test)
  if (bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ୤"), None) and
      bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ୥"), None)) or (
      bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭୦"), None) and
      bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ୧"), None)):
      logger.info(bstack1ll11ll_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠦࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡ࡫ࡶࠤࡺࡴࡤࡦࡴࡺࡥࡾ࠴ࠠࠣ୨"))
      bstack1l1l11l1l1_opy_.bstack1l11ll1l11_opy_(driver, name=test.name, path=test.source)
def bstack111ll1l11_opy_(test, bstack11ll1l1l_opy_):
    try:
      bstack1ll111l11_opy_ = datetime.datetime.now()
      data = {}
      if test:
        data[bstack1ll11ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ୩")] = bstack11ll1l1l_opy_
      if bstack1l1l1l1l1_opy_:
        if bstack1l1l1l1l1_opy_.status == bstack1ll11ll_opy_ (u"ࠪࡔࡆ࡙ࡓࠨ୪"):
          data[bstack1ll11ll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ୫")] = bstack1ll11ll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ୬")
        elif bstack1l1l1l1l1_opy_.status == bstack1ll11ll_opy_ (u"࠭ࡆࡂࡋࡏࠫ୭"):
          data[bstack1ll11ll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ୮")] = bstack1ll11ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ୯")
          if bstack1l1l1l1l1_opy_.message:
            data[bstack1ll11ll_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩ୰")] = str(bstack1l1l1l1l1_opy_.message)
      user = CONFIG[bstack1ll11ll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬୱ")]
      key = CONFIG[bstack1ll11ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ୲")]
      host = bstack1111lllll_opy_(cli.config, [bstack1ll11ll_opy_ (u"ࠧࡧࡰࡪࡵࠥ୳"), bstack1ll11ll_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥࠣ୴"), bstack1ll11ll_opy_ (u"ࠢࡢࡲ࡬ࠦ୵")], bstack1ll11ll_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠤ୶"))
      url = bstack1ll11ll_opy_ (u"ࠩࡾࢁ࠴ࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡴࡧࡶࡷ࡮ࡵ࡮ࡴ࠱ࡾࢁ࠳ࡰࡳࡰࡰࠪ୷").format(host, bstack1ll1111ll1_opy_)
      headers = {
        bstack1ll11ll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩ୸"): bstack1ll11ll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ୹"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers, auth=(user, key))
        cli.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽ࡹࡵࡪࡡࡵࡧࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡸࡦࡺࡵࡴࠤ୺"), datetime.datetime.now() - bstack1ll111l11_opy_)
    except Exception as e:
      logger.error(bstack1lll1l1111_opy_.format(str(e)))
def bstack1ll11111l1_opy_(test, bstack11ll1l1l_opy_):
  global CONFIG
  global bstack1ll11111l_opy_
  global bstack1l1l1ll11l_opy_
  global bstack1ll1111ll1_opy_
  global bstack1l1l1l1l1_opy_
  global bstack111l1l11_opy_
  global bstack1lll1ll11l_opy_
  global bstack1l111l111_opy_
  global bstack11l1llll1_opy_
  global bstack1lll11ll1_opy_
  global bstack1lll1ll1l1_opy_
  global bstack11l11l11l1_opy_
  global bstack11l11ll111_opy_
  try:
    if not bstack1ll1111ll1_opy_:
      with bstack11l11ll111_opy_:
        bstack11lllll1l1_opy_ = os.path.join(os.path.expanduser(bstack1ll11ll_opy_ (u"࠭ࡾࠨ୻")), bstack1ll11ll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ୼"), bstack1ll11ll_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪ୽"))
        if os.path.exists(bstack11lllll1l1_opy_):
          with open(bstack11lllll1l1_opy_, bstack1ll11ll_opy_ (u"ࠩࡵࠫ୾")) as f:
            content = f.read().strip()
            if content:
              bstack1l11ll111_opy_ = json.loads(bstack1ll11ll_opy_ (u"ࠥࡿࠧ୿") + content + bstack1ll11ll_opy_ (u"ࠫࠧࡾࠢ࠻ࠢࠥࡽࠧ࠭஀") + bstack1ll11ll_opy_ (u"ࠧࢃࠢ஁"))
              bstack1ll1111ll1_opy_ = bstack1l11ll111_opy_.get(str(threading.get_ident()))
  except Exception as e:
    logger.debug(bstack1ll11ll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡸࡥࡢࡦ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡊࡆࡶࠤ࡫࡯࡬ࡦ࠼ࠣࠫஂ") + str(e))
  if bstack1lll1ll1l1_opy_:
    with bstack11ll111l_opy_:
      bstack1l1l1l1ll_opy_ = bstack1lll1ll1l1_opy_.copy()
    for driver in bstack1l1l1l1ll_opy_:
      if bstack1ll1111ll1_opy_ == driver.session_id:
        if test:
          bstack1l1l111ll1_opy_(driver, test)
        bstack11lll11ll1_opy_(driver, bstack11ll1l1l_opy_)
  elif bstack1ll1111ll1_opy_:
    bstack111ll1l11_opy_(test, bstack11ll1l1l_opy_)
  if bstack1ll11111l_opy_:
    bstack1l111l111_opy_(bstack1ll11111l_opy_)
  if bstack1l1l1ll11l_opy_:
    bstack11l1llll1_opy_(bstack1l1l1ll11l_opy_)
  if bstack1ll1l1ll11_opy_:
    bstack1lll11ll1_opy_()
def bstack11llll1l1_opy_(self, test, *args, **kwargs):
  bstack11ll1l1l_opy_ = None
  if test:
    bstack11ll1l1l_opy_ = str(test.name)
  bstack1ll11111l1_opy_(test, bstack11ll1l1l_opy_)
  bstack1lll1ll11l_opy_(self, test, *args, **kwargs)
def bstack11ll11l1ll_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack11l1l1l1l_opy_
  global CONFIG
  global bstack1lll1ll1l1_opy_
  global bstack1ll1111ll1_opy_
  global bstack11l11ll111_opy_
  bstack1l1111l11_opy_ = None
  try:
    if bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ஃ"), None) or bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ஄"), None):
      try:
        if not bstack1ll1111ll1_opy_:
          bstack11lllll1l1_opy_ = os.path.join(os.path.expanduser(bstack1ll11ll_opy_ (u"ࠩࢁࠫஅ")), bstack1ll11ll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪஆ"), bstack1ll11ll_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭இ"))
          with bstack11l11ll111_opy_:
            if os.path.exists(bstack11lllll1l1_opy_):
              with open(bstack11lllll1l1_opy_, bstack1ll11ll_opy_ (u"ࠬࡸࠧஈ")) as f:
                content = f.read().strip()
                if content:
                  bstack1l11ll111_opy_ = json.loads(bstack1ll11ll_opy_ (u"ࠨࡻࠣஉ") + content + bstack1ll11ll_opy_ (u"ࠧࠣࡺࠥ࠾ࠥࠨࡹࠣࠩஊ") + bstack1ll11ll_opy_ (u"ࠣࡿࠥ஋"))
                  bstack1ll1111ll1_opy_ = bstack1l11ll111_opy_.get(str(threading.get_ident()))
      except Exception as e:
        logger.debug(bstack1ll11ll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡴࡨࡥࡩ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡍࡉࡹࠠࡧ࡫࡯ࡩࠥ࡯࡮ࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࡀࠠࠨ஌") + str(e))
      if bstack1lll1ll1l1_opy_:
        with bstack11ll111l_opy_:
          bstack1l1l1l1ll_opy_ = bstack1lll1ll1l1_opy_.copy()
        for driver in bstack1l1l1l1ll_opy_:
          if bstack1ll1111ll1_opy_ == driver.session_id:
            bstack1l1111l11_opy_ = driver
    bstack1111llll1_opy_ = bstack1l1l11l1l1_opy_.bstack1l1l1l11ll_opy_(test.tags)
    if bstack1l1111l11_opy_:
      threading.current_thread().isA11yTest = bstack1l1l11l1l1_opy_.bstack111ll1111_opy_(bstack1l1111l11_opy_, bstack1111llll1_opy_)
      threading.current_thread().isAppA11yTest = bstack1l1l11l1l1_opy_.bstack111ll1111_opy_(bstack1l1111l11_opy_, bstack1111llll1_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1111llll1_opy_
      threading.current_thread().isAppA11yTest = bstack1111llll1_opy_
  except:
    pass
  bstack11l1l1l1l_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1l1l1l1l1_opy_
  try:
    bstack1l1l1l1l1_opy_ = self._test
  except:
    bstack1l1l1l1l1_opy_ = self.test
def bstack1ll1lll11l_opy_():
  global bstack11ll11l1l1_opy_
  try:
    if os.path.exists(bstack11ll11l1l1_opy_):
      os.remove(bstack11ll11l1l1_opy_)
  except Exception as e:
    logger.debug(bstack1ll11ll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭஍") + str(e))
def bstack11l11ll1ll_opy_():
  global bstack11ll11l1l1_opy_
  bstack111l111l1_opy_ = {}
  lock_file = bstack11ll11l1l1_opy_ + bstack1ll11ll_opy_ (u"ࠫ࠳ࡲ࡯ࡤ࡭ࠪஎ")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1ll11ll_opy_ (u"ࠬ࡬ࡩ࡭ࡧ࡯ࡳࡨࡱࠠ࡯ࡱࡷࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠬࠡࡷࡶ࡭ࡳ࡭ࠠࡣࡣࡶ࡭ࡨࠦࡦࡪ࡮ࡨࠤࡴࡶࡥࡳࡣࡷ࡭ࡴࡴࡳࠨஏ"))
    try:
      if not os.path.isfile(bstack11ll11l1l1_opy_):
        with open(bstack11ll11l1l1_opy_, bstack1ll11ll_opy_ (u"࠭ࡷࠨஐ")) as f:
          json.dump({}, f)
      if os.path.exists(bstack11ll11l1l1_opy_):
        with open(bstack11ll11l1l1_opy_, bstack1ll11ll_opy_ (u"ࠧࡳࠩ஑")) as f:
          content = f.read().strip()
          if content:
            bstack111l111l1_opy_ = json.loads(content)
    except Exception as e:
      logger.debug(bstack1ll11ll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡶࡪࡧࡤࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪஒ") + str(e))
    return bstack111l111l1_opy_
  try:
    os.makedirs(os.path.dirname(bstack11ll11l1l1_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      if not os.path.isfile(bstack11ll11l1l1_opy_):
        with open(bstack11ll11l1l1_opy_, bstack1ll11ll_opy_ (u"ࠩࡺࠫஓ")) as f:
          json.dump({}, f)
      if os.path.exists(bstack11ll11l1l1_opy_):
        with open(bstack11ll11l1l1_opy_, bstack1ll11ll_opy_ (u"ࠪࡶࠬஔ")) as f:
          content = f.read().strip()
          if content:
            bstack111l111l1_opy_ = json.loads(content)
  except Exception as e:
    logger.debug(bstack1ll11ll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡲࡦࡣࡧ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭க") + str(e))
  finally:
    return bstack111l111l1_opy_
def bstack1lllll1ll_opy_(platform_index, item_index):
  global bstack11ll11l1l1_opy_
  lock_file = bstack11ll11l1l1_opy_ + bstack1ll11ll_opy_ (u"ࠬ࠴࡬ࡰࡥ࡮ࠫ஖")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1ll11ll_opy_ (u"࠭ࡦࡪ࡮ࡨࡰࡴࡩ࡫ࠡࡰࡲࡸࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥ࠭ࠢࡸࡷ࡮ࡴࡧࠡࡤࡤࡷ࡮ࡩࠠࡧ࡫࡯ࡩࠥࡵࡰࡦࡴࡤࡸ࡮ࡵ࡮ࡴࠩ஗"))
    try:
      bstack111l111l1_opy_ = {}
      if os.path.exists(bstack11ll11l1l1_opy_):
        with open(bstack11ll11l1l1_opy_, bstack1ll11ll_opy_ (u"ࠧࡳࠩ஘")) as f:
          content = f.read().strip()
          if content:
            bstack111l111l1_opy_ = json.loads(content)
      bstack111l111l1_opy_[item_index] = platform_index
      with open(bstack11ll11l1l1_opy_, bstack1ll11ll_opy_ (u"ࠣࡹࠥங")) as outfile:
        json.dump(bstack111l111l1_opy_, outfile)
    except Exception as e:
      logger.debug(bstack1ll11ll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡼࡸࡩࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧச") + str(e))
    return
  try:
    os.makedirs(os.path.dirname(bstack11ll11l1l1_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      bstack111l111l1_opy_ = {}
      if os.path.exists(bstack11ll11l1l1_opy_):
        with open(bstack11ll11l1l1_opy_, bstack1ll11ll_opy_ (u"ࠪࡶࠬ஛")) as f:
          content = f.read().strip()
          if content:
            bstack111l111l1_opy_ = json.loads(content)
      bstack111l111l1_opy_[item_index] = platform_index
      with open(bstack11ll11l1l1_opy_, bstack1ll11ll_opy_ (u"ࠦࡼࠨஜ")) as outfile:
        json.dump(bstack111l111l1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1ll11ll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡸࡴ࡬ࡸ࡮ࡴࡧࠡࡶࡲࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪ஝") + str(e))
def bstack1llll1lll1_opy_(bstack1l1l1ll1ll_opy_):
  global CONFIG
  bstack1l1l11ll1l_opy_ = bstack1ll11ll_opy_ (u"࠭ࠧஞ")
  if not bstack1ll11ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪட") in CONFIG:
    logger.info(bstack1ll11ll_opy_ (u"ࠨࡐࡲࠤࡵࡲࡡࡵࡨࡲࡶࡲࡹࠠࡱࡣࡶࡷࡪࡪࠠࡶࡰࡤࡦࡱ࡫ࠠࡵࡱࠣ࡫ࡪࡴࡥࡳࡣࡷࡩࠥࡸࡥࡱࡱࡵࡸࠥ࡬࡯ࡳࠢࡕࡳࡧࡵࡴࠡࡴࡸࡲࠬ஠"))
  try:
    platform = CONFIG[bstack1ll11ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ஡")][bstack1l1l1ll1ll_opy_]
    if bstack1ll11ll_opy_ (u"ࠪࡳࡸ࠭஢") in platform:
      bstack1l1l11ll1l_opy_ += str(platform[bstack1ll11ll_opy_ (u"ࠫࡴࡹࠧண")]) + bstack1ll11ll_opy_ (u"ࠬ࠲ࠠࠨத")
    if bstack1ll11ll_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ஥") in platform:
      bstack1l1l11ll1l_opy_ += str(platform[bstack1ll11ll_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪ஦")]) + bstack1ll11ll_opy_ (u"ࠨ࠮ࠣࠫ஧")
    if bstack1ll11ll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ந") in platform:
      bstack1l1l11ll1l_opy_ += str(platform[bstack1ll11ll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧன")]) + bstack1ll11ll_opy_ (u"ࠫ࠱ࠦࠧப")
    if bstack1ll11ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ஫") in platform:
      bstack1l1l11ll1l_opy_ += str(platform[bstack1ll11ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ஬")]) + bstack1ll11ll_opy_ (u"ࠧ࠭ࠢࠪ஭")
    if bstack1ll11ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ம") in platform:
      bstack1l1l11ll1l_opy_ += str(platform[bstack1ll11ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧய")]) + bstack1ll11ll_opy_ (u"ࠪ࠰ࠥ࠭ர")
    if bstack1ll11ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬற") in platform:
      bstack1l1l11ll1l_opy_ += str(platform[bstack1ll11ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ல")]) + bstack1ll11ll_opy_ (u"࠭ࠬࠡࠩள")
  except Exception as e:
    logger.debug(bstack1ll11ll_opy_ (u"ࠧࡔࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡱࡩࡷࡧࡴࡪࡰࡪࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡳࡵࡴ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡶࡪࡶ࡯ࡳࡶࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡴࡴࠧழ") + str(e))
  finally:
    if bstack1l1l11ll1l_opy_[len(bstack1l1l11ll1l_opy_) - 2:] == bstack1ll11ll_opy_ (u"ࠨ࠮ࠣࠫவ"):
      bstack1l1l11ll1l_opy_ = bstack1l1l11ll1l_opy_[:-2]
    return bstack1l1l11ll1l_opy_
def bstack11lll111_opy_(path, bstack1l1l11ll1l_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack11ll1111l1_opy_ = ET.parse(path)
    bstack11l11l1111_opy_ = bstack11ll1111l1_opy_.getroot()
    bstack1l11llll11_opy_ = None
    for suite in bstack11l11l1111_opy_.iter(bstack1ll11ll_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨஶ")):
      if bstack1ll11ll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪஷ") in suite.attrib:
        suite.attrib[bstack1ll11ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩஸ")] += bstack1ll11ll_opy_ (u"ࠬࠦࠧஹ") + bstack1l1l11ll1l_opy_
        bstack1l11llll11_opy_ = suite
    bstack1l11l1l111_opy_ = None
    for robot in bstack11l11l1111_opy_.iter(bstack1ll11ll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ஺")):
      bstack1l11l1l111_opy_ = robot
    bstack1llll11ll1_opy_ = len(bstack1l11l1l111_opy_.findall(bstack1ll11ll_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭஻")))
    if bstack1llll11ll1_opy_ == 1:
      bstack1l11l1l111_opy_.remove(bstack1l11l1l111_opy_.findall(bstack1ll11ll_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧ஼"))[0])
      bstack1llll1lll_opy_ = ET.Element(bstack1ll11ll_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨ஽"), attrib={bstack1ll11ll_opy_ (u"ࠪࡲࡦࡳࡥࠨா"): bstack1ll11ll_opy_ (u"ࠫࡘࡻࡩࡵࡧࡶࠫி"), bstack1ll11ll_opy_ (u"ࠬ࡯ࡤࠨீ"): bstack1ll11ll_opy_ (u"࠭ࡳ࠱ࠩு")})
      bstack1l11l1l111_opy_.insert(1, bstack1llll1lll_opy_)
      bstack1l1ll1llll_opy_ = None
      for suite in bstack1l11l1l111_opy_.iter(bstack1ll11ll_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭ூ")):
        bstack1l1ll1llll_opy_ = suite
      bstack1l1ll1llll_opy_.append(bstack1l11llll11_opy_)
      bstack11llll1l_opy_ = None
      for status in bstack1l11llll11_opy_.iter(bstack1ll11ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ௃")):
        bstack11llll1l_opy_ = status
      bstack1l1ll1llll_opy_.append(bstack11llll1l_opy_)
    bstack11ll1111l1_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1ll11ll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡲࡴ࡫ࡱ࡫ࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠧ௄") + str(e))
def bstack111llll1l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1l11ll1111_opy_
  global CONFIG
  if bstack1ll11ll_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࡳࡥࡹ࡮ࠢ௅") in options:
    del options[bstack1ll11ll_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡴࡦࡺࡨࠣெ")]
  bstack1l1lllll1_opy_ = bstack11l11ll1ll_opy_()
  for item_id in bstack1l1lllll1_opy_.keys():
    path = os.path.join(os.getcwd(), bstack1ll11ll_opy_ (u"ࠬࡶࡡࡣࡱࡷࡣࡷ࡫ࡳࡶ࡮ࡷࡷࠬே"), str(item_id), bstack1ll11ll_opy_ (u"࠭࡯ࡶࡶࡳࡹࡹ࠴ࡸ࡮࡮ࠪை"))
    bstack11lll111_opy_(path, bstack1llll1lll1_opy_(bstack1l1lllll1_opy_[item_id]))
  bstack1ll1lll11l_opy_()
  return bstack1l11ll1111_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1ll11ll111_opy_(self, ff_profile_dir):
  global bstack1llllllll_opy_
  if not ff_profile_dir:
    return None
  return bstack1llllllll_opy_(self, ff_profile_dir)
def bstack111111l1l_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1lll11lll1_opy_
  bstack11ll11ll11_opy_ = []
  if bstack1ll11ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ௉") in CONFIG:
    bstack11ll11ll11_opy_ = CONFIG[bstack1ll11ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫொ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1ll11ll_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࠥோ")],
      pabot_args[bstack1ll11ll_opy_ (u"ࠥࡺࡪࡸࡢࡰࡵࡨࠦௌ")],
      argfile,
      pabot_args.get(bstack1ll11ll_opy_ (u"ࠦ࡭࡯ࡶࡦࠤ்")),
      pabot_args[bstack1ll11ll_opy_ (u"ࠧࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠣ௎")],
      platform[0],
      bstack1lll11lll1_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1ll11ll_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡧ࡫࡯ࡩࡸࠨ௏")] or [(bstack1ll11ll_opy_ (u"ࠢࠣௐ"), None)]
    for platform in enumerate(bstack11ll11ll11_opy_)
  ]
def bstack1ll11l1ll_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1lll1l1l11_opy_=bstack1ll11ll_opy_ (u"ࠨࠩ௑")):
  global bstack1lll111l1_opy_
  self.platform_index = platform_index
  self.bstack1l111111l_opy_ = bstack1lll1l1l11_opy_
  bstack1lll111l1_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1ll1111l11_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1lllll1l11_opy_
  global bstack11ll1111_opy_
  bstack1ll1lllll_opy_ = copy.deepcopy(item)
  if not bstack1ll11ll_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ௒") in item.options:
    bstack1ll1lllll_opy_.options[bstack1ll11ll_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ௓")] = []
  bstack11l11llll_opy_ = bstack1ll1lllll_opy_.options[bstack1ll11ll_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭௔")].copy()
  for v in bstack1ll1lllll_opy_.options[bstack1ll11ll_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ௕")]:
    if bstack1ll11ll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬ௖") in v:
      bstack11l11llll_opy_.remove(v)
    if bstack1ll11ll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙ࠧௗ") in v:
      bstack11l11llll_opy_.remove(v)
    if bstack1ll11ll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡅࡇࡉࡐࡔࡉࡁࡍࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬ௘") in v:
      bstack11l11llll_opy_.remove(v)
  bstack11l11llll_opy_.insert(0, bstack1ll11ll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘ࠻ࡽࢀࠫ௙").format(bstack1ll1lllll_opy_.platform_index))
  bstack11l11llll_opy_.insert(0, bstack1ll11ll_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡇࡉࡋࡒࡏࡄࡃࡏࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘ࠺ࡼࡿࠪ௚").format(bstack1ll1lllll_opy_.bstack1l111111l_opy_))
  bstack1ll1lllll_opy_.options[bstack1ll11ll_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭௛")] = bstack11l11llll_opy_
  if bstack11ll1111_opy_:
    bstack1ll1lllll_opy_.options[bstack1ll11ll_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ௜")].insert(0, bstack1ll11ll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘࡀࡻࡾࠩ௝").format(bstack11ll1111_opy_))
  return bstack1lllll1l11_opy_(caller_id, datasources, is_last, bstack1ll1lllll_opy_, outs_dir)
def bstack1l1l1lll_opy_(command, item_index):
  try:
    if bstack1l111111l1_opy_.get_property(bstack1ll11ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ௞")):
      os.environ[bstack1ll11ll_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩ௟")] = json.dumps(CONFIG[bstack1ll11ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ௠")][item_index % bstack11ll1lllll_opy_])
    global bstack11ll1111_opy_
    if bstack11ll1111_opy_:
      command[0] = command[0].replace(bstack1ll11ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ௡"), bstack1ll11ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡷࡩࡱࠠࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠡ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠠࠨ௢") + str(
        item_index) + bstack1ll11ll_opy_ (u"ࠬࠦࠧ௣") + bstack11ll1111_opy_, 1)
    else:
      command[0] = command[0].replace(bstack1ll11ll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ௤"),
                                      bstack1ll11ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡳࡥ࡭ࠣࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠤ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠣࠫ௥") + str(item_index), 1)
  except Exception as e:
    logger.error(bstack1ll11ll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠ࡮ࡱࡧ࡭࡫ࡿࡩ࡯ࡩࠣࡧࡴࡳ࡭ࡢࡰࡧࠤ࡫ࡵࡲࠡࡲࡤࡦࡴࡺࠠࡳࡷࡱ࠾ࠥࢁࡽࠨ௦").format(str(e)))
def bstack11llllll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1l11l11111_opy_
  try:
    bstack1l1l1lll_opy_(command, item_index)
    return bstack1l11l11111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
  except Exception as e:
    logger.error(bstack1ll11ll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡢࡰࡶࠣࡶࡺࡴ࠺ࠡࡽࢀࠫ௧").format(str(e)))
    raise e
def bstack1lllllll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1l11l11111_opy_
  try:
    bstack1l1l1lll_opy_(command, item_index)
    return bstack1l11l11111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
  except Exception as e:
    logger.error(bstack1ll11ll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡣࡱࡷࠤࡷࡻ࡮ࠡ࠴࠱࠵࠸ࡀࠠࡼࡿࠪ௨").format(str(e)))
    try:
      return bstack1l11l11111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
    except Exception as e2:
      logger.error(bstack1ll11ll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡢࡤࡲࡸࠥ࠸࠮࠲࠵ࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࡻࡾࠩ௩").format(str(e2)))
      raise e
def bstack1lll11l11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1l11l11111_opy_
  try:
    bstack1l1l1lll_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    return bstack1l11l11111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
  except Exception as e:
    logger.error(bstack1ll11ll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡥࡳࡹࠦࡲࡶࡰࠣ࠶࠳࠷࠵࠻ࠢࡾࢁࠬ௪").format(str(e)))
    try:
      return bstack1l11l11111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
    except Exception as e2:
      logger.error(bstack1ll11ll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠ࠳࠰࠴࠹ࠥ࡬ࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࡽࢀࠫ௫").format(str(e2)))
      raise e
def _1l1lll11l1_opy_(bstack1ll1111lll_opy_, item_index, process_timeout, sleep_before_start, bstack11l11ll11l_opy_):
  bstack1l1l1lll_opy_(bstack1ll1111lll_opy_, item_index)
  if process_timeout is None:
    process_timeout = 3600
  if sleep_before_start and sleep_before_start > 0:
    import time
    time.sleep(min(sleep_before_start, 5))
  return process_timeout
def bstack111l1llll_opy_(command, bstack11l1ll1lll_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack1l11l11111_opy_
  try:
    process_timeout = _1l1lll11l1_opy_(command + bstack11l1ll1lll_opy_, item_index, process_timeout, sleep_before_start, bstack1ll11ll_opy_ (u"ࠧ࠶࠰࠳ࠫ௬"))
    return bstack1l11l11111_opy_(command, bstack11l1ll1lll_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
  except Exception as e:
    logger.error(bstack1ll11ll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡦࡨ࡯ࡵࠢࡵࡹࡳࠦ࠵࠯࠲࠽ࠤࢀࢃࠧ௭").format(str(e)))
    try:
      return bstack1l11l11111_opy_(command, bstack11l1ll1lll_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack1ll11ll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡢࡰࡶࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࡻࡾࠩ௮").format(str(e2)))
      raise e
def bstack1ll1l1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack1l11l11111_opy_
  try:
    process_timeout = _1l1lll11l1_opy_(command, item_index, process_timeout, sleep_before_start, bstack1ll11ll_opy_ (u"ࠪ࠸࠳࠸ࠧ௯"))
    return bstack1l11l11111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack1ll11ll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡢࡤࡲࡸࠥࡸࡵ࡯ࠢ࠷࠲࠷ࡀࠠࡼࡿࠪ௰").format(str(e)))
    try:
      return bstack1l11l11111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack1ll11ll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡥࡳࡹࠦࡦࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢࡾࢁࠬ௱").format(str(e2)))
      raise e
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack1ll1llllll_opy_(self, runner, quiet=False, capture=True):
  global bstack11l1ll11l1_opy_
  bstack1111lll11_opy_ = bstack11l1ll11l1_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack1ll11ll_opy_ (u"࠭ࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࡡࡤࡶࡷ࠭௲")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1ll11ll_opy_ (u"ࠧࡦࡺࡦࡣࡹࡸࡡࡤࡧࡥࡥࡨࡱ࡟ࡢࡴࡵࠫ௳")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1111lll11_opy_
def bstack11lllll1l_opy_(runner, hook_name, context, element, bstack1lllllll11_opy_, *args):
  try:
    if runner.hooks.get(hook_name):
      bstack1l11ll1lll_opy_.bstack1lllll1ll1_opy_(hook_name, element)
    bstack1lllllll11_opy_(runner, hook_name, context, *args)
    if runner.hooks.get(hook_name):
      bstack1l11ll1lll_opy_.bstack1ll11lll1l_opy_(element)
      if hook_name not in [bstack1ll11ll_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠬ௴"), bstack1ll11ll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠬ௵")] and args and hasattr(args[0], bstack1ll11ll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡡࡰࡩࡸࡹࡡࡨࡧࠪ௶")):
        args[0].error_message = bstack1ll11ll_opy_ (u"ࠫࠬ௷")
  except Exception as e:
    logger.debug(bstack1ll11ll_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡪࡤࡲࡩࡲࡥࠡࡪࡲࡳࡰࡹࠠࡪࡰࠣࡦࡪ࡮ࡡࡷࡧ࠽ࠤࢀࢃࠧ௸").format(str(e)))
@measure(event_name=EVENTS.bstack1ll11l111l_opy_, stage=STAGE.bstack11lll1ll1l_opy_, hook_type=bstack1ll11ll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡇ࡬࡭ࠤ௹"), bstack11ll1l1l_opy_=bstack111l1l11_opy_)
def bstack1l11l11ll_opy_(runner, name, context, bstack1lllllll11_opy_, *args):
    if runner.hooks.get(bstack1ll11ll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦ௺")).__name__ != bstack1ll11ll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࡤࡪࡥࡧࡣࡸࡰࡹࡥࡨࡰࡱ࡮ࠦ௻"):
      bstack11lllll1l_opy_(runner, name, context, runner, bstack1lllllll11_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack11llllll1l_opy_(bstack1ll11ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ௼")) else context.browser
      runner.driver_initialised = bstack1ll11ll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢ௽")
    except Exception as e:
      logger.debug(bstack1ll11ll_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡩࡸࡩࡷࡧࡵࠤ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡥࠡࡣࡷࡸࡷ࡯ࡢࡶࡶࡨ࠾ࠥࢁࡽࠨ௾").format(str(e)))
def bstack11l1ll11ll_opy_(runner, name, context, bstack1lllllll11_opy_, *args):
    bstack11lllll1l_opy_(runner, name, context, context.feature, bstack1lllllll11_opy_, *args)
    try:
      if not bstack11l1111ll_opy_:
        bstack1l1111l11_opy_ = threading.current_thread().bstackSessionDriver if bstack11llllll1l_opy_(bstack1ll11ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ௿")) else context.browser
        if is_driver_active(bstack1l1111l11_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack1ll11ll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠢఀ")
          bstack11l1l111ll_opy_ = str(runner.feature.name)
          bstack11l1l11111_opy_(context, bstack11l1l111ll_opy_)
          bstack1l1111l11_opy_.execute_script(bstack1ll11ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬఁ") + json.dumps(bstack11l1l111ll_opy_) + bstack1ll11ll_opy_ (u"ࠨࡿࢀࠫం"))
    except Exception as e:
      logger.debug(bstack1ll11ll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡ࡫ࡱࠤࡧ࡫ࡦࡰࡴࡨࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩః").format(str(e)))
def bstack11ll1llll1_opy_(runner, name, context, bstack1lllllll11_opy_, *args):
    if hasattr(context, bstack1ll11ll_opy_ (u"ࠪࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬఄ")):
        bstack1l11ll1lll_opy_.start_test(context)
    target = context.scenario if hasattr(context, bstack1ll11ll_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭అ")) else context.feature
    bstack11lllll1l_opy_(runner, name, context, target, bstack1lllllll11_opy_, *args)
@measure(event_name=EVENTS.bstack11lll11lll_opy_, stage=STAGE.bstack11lll1ll1l_opy_, bstack11ll1l1l_opy_=bstack111l1l11_opy_)
def bstack1lll11ll_opy_(runner, name, context, bstack1lllllll11_opy_, *args):
    if len(context.scenario.tags) == 0: bstack1l11ll1lll_opy_.start_test(context)
    bstack11lllll1l_opy_(runner, name, context, context.scenario, bstack1lllllll11_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack1ll1l111l_opy_.bstack1lll111l_opy_(context, *args)
    try:
      bstack1l1111l11_opy_ = bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫఆ"), context.browser)
      if is_driver_active(bstack1l1111l11_opy_):
        bstack1l11ll1l_opy_.bstack111llll1_opy_(bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬఇ"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack1ll11ll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤఈ")
        if (not bstack11l1111ll_opy_):
          scenario_name = args[0].name
          feature_name = bstack11l1l111ll_opy_ = str(runner.feature.name)
          bstack11l1l111ll_opy_ = feature_name + bstack1ll11ll_opy_ (u"ࠨࠢ࠰ࠤࠬఉ") + scenario_name
          if runner.driver_initialised == bstack1ll11ll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦఊ"):
            bstack11l1l11111_opy_(context, bstack11l1l111ll_opy_)
            bstack1l1111l11_opy_.execute_script(bstack1ll11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨఋ") + json.dumps(bstack11l1l111ll_opy_) + bstack1ll11ll_opy_ (u"ࠫࢂࢃࠧఌ"))
    except Exception as e:
      logger.debug(bstack1ll11ll_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤ࡮ࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡥࡨࡲࡦࡸࡩࡰ࠼ࠣࡿࢂ࠭఍").format(str(e)))
@measure(event_name=EVENTS.bstack1ll11l111l_opy_, stage=STAGE.bstack11lll1ll1l_opy_, hook_type=bstack1ll11ll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪ࡙ࡴࡦࡲࠥఎ"), bstack11ll1l1l_opy_=bstack111l1l11_opy_)
def bstack11lll11l1_opy_(runner, name, context, bstack1lllllll11_opy_, *args):
    bstack11lllll1l_opy_(runner, name, context, args[0], bstack1lllllll11_opy_, *args)
    try:
      bstack1l1111l11_opy_ = threading.current_thread().bstackSessionDriver if bstack11llllll1l_opy_(bstack1ll11ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ఏ")) else context.browser
      if is_driver_active(bstack1l1111l11_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack1ll11ll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨఐ")
        bstack1l11ll1lll_opy_.bstack11llll1ll_opy_(args[0])
        if runner.driver_initialised == bstack1ll11ll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢ఑"):
          feature_name = bstack11l1l111ll_opy_ = str(runner.feature.name)
          bstack11l1l111ll_opy_ = feature_name + bstack1ll11ll_opy_ (u"ࠪࠤ࠲ࠦࠧఒ") + context.scenario.name
          bstack1l1111l11_opy_.execute_script(bstack1ll11ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩఓ") + json.dumps(bstack11l1l111ll_opy_) + bstack1ll11ll_opy_ (u"ࠬࢃࡽࠨఔ"))
    except Exception as e:
      logger.debug(bstack1ll11ll_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡷࡩࡵࡀࠠࡼࡿࠪక").format(str(e)))
@measure(event_name=EVENTS.bstack1ll11l111l_opy_, stage=STAGE.bstack11lll1ll1l_opy_, hook_type=bstack1ll11ll_opy_ (u"ࠢࡢࡨࡷࡩࡷ࡙ࡴࡦࡲࠥఖ"), bstack11ll1l1l_opy_=bstack111l1l11_opy_)
def bstack11ll11111l_opy_(runner, name, context, bstack1lllllll11_opy_, *args):
  bstack1l11ll1lll_opy_.bstack1ll111ll1_opy_(args[0])
  try:
    step_status = args[0].status.name
    bstack1l1111l11_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll11ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧగ") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack1l1111l11_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack1ll11ll_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩఘ")
        feature_name = bstack11l1l111ll_opy_ = str(runner.feature.name)
        bstack11l1l111ll_opy_ = feature_name + bstack1ll11ll_opy_ (u"ࠪࠤ࠲ࠦࠧఙ") + context.scenario.name
        bstack1l1111l11_opy_.execute_script(bstack1ll11ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩచ") + json.dumps(bstack11l1l111ll_opy_) + bstack1ll11ll_opy_ (u"ࠬࢃࡽࠨఛ"))
    if str(step_status).lower() == bstack1ll11ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭జ"):
      bstack11l1ll11_opy_ = bstack1ll11ll_opy_ (u"ࠧࠨఝ")
      bstack11l1llll_opy_ = bstack1ll11ll_opy_ (u"ࠨࠩఞ")
      bstack1l11111l_opy_ = bstack1ll11ll_opy_ (u"ࠩࠪట")
      try:
        import traceback
        bstack11l1ll11_opy_ = runner.exception.__class__.__name__
        bstack11lll11l_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack11l1llll_opy_ = bstack1ll11ll_opy_ (u"ࠪࠤࠬఠ").join(bstack11lll11l_opy_)
        bstack1l11111l_opy_ = bstack11lll11l_opy_[-1]
      except Exception as e:
        logger.debug(bstack1111l11l1_opy_.format(str(e)))
      bstack11l1ll11_opy_ += bstack1l11111l_opy_
      bstack1ll11lll11_opy_(context, json.dumps(str(args[0].name) + bstack1ll11ll_opy_ (u"ࠦࠥ࠳ࠠࡇࡣ࡬ࡰࡪࡪࠡ࡝ࡰࠥడ") + str(bstack11l1llll_opy_)),
                          bstack1ll11ll_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦఢ"))
      if runner.driver_initialised == bstack1ll11ll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦణ"):
        bstack1l11ll11l_opy_(getattr(context, bstack1ll11ll_opy_ (u"ࠧࡱࡣࡪࡩࠬత"), None), bstack1ll11ll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣథ"), bstack11l1ll11_opy_)
        bstack1l1111l11_opy_.execute_script(bstack1ll11ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧద") + json.dumps(str(args[0].name) + bstack1ll11ll_opy_ (u"ࠥࠤ࠲ࠦࡆࡢ࡫࡯ࡩࡩࠧ࡜࡯ࠤధ") + str(bstack11l1llll_opy_)) + bstack1ll11ll_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣࡿࢀࠫన"))
      if runner.driver_initialised == bstack1ll11ll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥ఩"):
        bstack1l11lllll1_opy_(bstack1l1111l11_opy_, bstack1ll11ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ప"), bstack1ll11ll_opy_ (u"ࠢࡔࡥࡨࡲࡦࡸࡩࡰࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦఫ") + str(bstack11l1ll11_opy_))
    else:
      bstack1ll11lll11_opy_(context, bstack1ll11ll_opy_ (u"ࠣࡒࡤࡷࡸ࡫ࡤࠢࠤబ"), bstack1ll11ll_opy_ (u"ࠤ࡬ࡲ࡫ࡵࠢభ"))
      if runner.driver_initialised == bstack1ll11ll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣమ"):
        bstack1l11ll11l_opy_(getattr(context, bstack1ll11ll_opy_ (u"ࠫࡵࡧࡧࡦࠩయ"), None), bstack1ll11ll_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧర"))
      bstack1l1111l11_opy_.execute_script(bstack1ll11ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫఱ") + json.dumps(str(args[0].name) + bstack1ll11ll_opy_ (u"ࠢࠡ࠯ࠣࡔࡦࡹࡳࡦࡦࠤࠦల")) + bstack1ll11ll_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦࢂࢃࠧళ"))
      if runner.driver_initialised == bstack1ll11ll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢఴ"):
        bstack1l11lllll1_opy_(bstack1l1111l11_opy_, bstack1ll11ll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥవ"))
  except Exception as e:
    logger.debug(bstack1ll11ll_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࠡࡵࡷࡩࡵࡀࠠࡼࡿࠪశ").format(str(e)))
  bstack11lllll1l_opy_(runner, name, context, args[0], bstack1lllllll11_opy_, *args)
@measure(event_name=EVENTS.bstack1llllll1l_opy_, stage=STAGE.bstack11lll1ll1l_opy_, bstack11ll1l1l_opy_=bstack111l1l11_opy_)
def bstack11ll1lll1_opy_(runner, name, context, bstack1lllllll11_opy_, *args):
  bstack1l11ll1lll_opy_.end_test(args[0])
  try:
    bstack1l111llll1_opy_ = args[0].status.name
    bstack1l1111l11_opy_ = bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫష"), context.browser)
    bstack1ll1l111l_opy_.bstack1l1111111_opy_(bstack1l1111l11_opy_)
    if str(bstack1l111llll1_opy_).lower() == bstack1ll11ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭స"):
      bstack11l1ll11_opy_ = bstack1ll11ll_opy_ (u"ࠧࠨహ")
      bstack11l1llll_opy_ = bstack1ll11ll_opy_ (u"ࠨࠩ఺")
      bstack1l11111l_opy_ = bstack1ll11ll_opy_ (u"ࠩࠪ఻")
      try:
        import traceback
        bstack11l1ll11_opy_ = runner.exception.__class__.__name__
        bstack11lll11l_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack11l1llll_opy_ = bstack1ll11ll_opy_ (u"ࠪࠤ఼ࠬ").join(bstack11lll11l_opy_)
        bstack1l11111l_opy_ = bstack11lll11l_opy_[-1]
      except Exception as e:
        logger.debug(bstack1111l11l1_opy_.format(str(e)))
      bstack11l1ll11_opy_ += bstack1l11111l_opy_
      bstack1ll11lll11_opy_(context, json.dumps(str(args[0].name) + bstack1ll11ll_opy_ (u"ࠦࠥ࠳ࠠࡇࡣ࡬ࡰࡪࡪࠡ࡝ࡰࠥఽ") + str(bstack11l1llll_opy_)),
                          bstack1ll11ll_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦా"))
      if runner.driver_initialised == bstack1ll11ll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣి") or runner.driver_initialised == bstack1ll11ll_opy_ (u"ࠧࡪࡰࡶࡸࡪࡶࠧీ"):
        bstack1l11ll11l_opy_(getattr(context, bstack1ll11ll_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭ు"), None), bstack1ll11ll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤూ"), bstack11l1ll11_opy_)
        bstack1l1111l11_opy_.execute_script(bstack1ll11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨృ") + json.dumps(str(args[0].name) + bstack1ll11ll_opy_ (u"ࠦࠥ࠳ࠠࡇࡣ࡬ࡰࡪࡪࠡ࡝ࡰࠥౄ") + str(bstack11l1llll_opy_)) + bstack1ll11ll_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥࡩࡷࡸ࡯ࡳࠤࢀࢁࠬ౅"))
      if runner.driver_initialised == bstack1ll11ll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣె") or runner.driver_initialised == bstack1ll11ll_opy_ (u"ࠧࡪࡰࡶࡸࡪࡶࠧే"):
        bstack1l11lllll1_opy_(bstack1l1111l11_opy_, bstack1ll11ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨై"), bstack1ll11ll_opy_ (u"ࠤࡖࡧࡪࡴࡡࡳ࡫ࡲࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨ౉") + str(bstack11l1ll11_opy_))
    else:
      bstack1ll11lll11_opy_(context, bstack1ll11ll_opy_ (u"ࠥࡔࡦࡹࡳࡦࡦࠤࠦొ"), bstack1ll11ll_opy_ (u"ࠦ࡮ࡴࡦࡰࠤో"))
      if runner.driver_initialised == bstack1ll11ll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢౌ") or runner.driver_initialised == bstack1ll11ll_opy_ (u"࠭ࡩ࡯ࡵࡷࡩࡵ్࠭"):
        bstack1l11ll11l_opy_(getattr(context, bstack1ll11ll_opy_ (u"ࠧࡱࡣࡪࡩࠬ౎"), None), bstack1ll11ll_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ౏"))
      bstack1l1111l11_opy_.execute_script(bstack1ll11ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ౐") + json.dumps(str(args[0].name) + bstack1ll11ll_opy_ (u"ࠥࠤ࠲ࠦࡐࡢࡵࡶࡩࡩࠧࠢ౑")) + bstack1ll11ll_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢࡾࡿࠪ౒"))
      if runner.driver_initialised == bstack1ll11ll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢ౓") or runner.driver_initialised == bstack1ll11ll_opy_ (u"࠭ࡩ࡯ࡵࡷࡩࡵ࠭౔"):
        bstack1l11lllll1_opy_(bstack1l1111l11_opy_, bstack1ll11ll_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪౕࠢ"))
  except Exception as e:
    logger.debug(bstack1ll11ll_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࠥ࡬ࡥࡢࡶࡸࡶࡪࡀࠠࡼࡿౖࠪ").format(str(e)))
  bstack11lllll1l_opy_(runner, name, context, context.scenario, bstack1lllllll11_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack1l1lllll11_opy_(runner, name, context, bstack1lllllll11_opy_, *args):
    target = context.scenario if hasattr(context, bstack1ll11ll_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ౗")) else context.feature
    bstack11lllll1l_opy_(runner, name, context, target, bstack1lllllll11_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack1ll1l1ll1l_opy_(runner, name, context, bstack1lllllll11_opy_, *args):
    try:
      bstack1l1111l11_opy_ = bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩౘ"), context.browser)
      bstack1lll1lll11_opy_ = bstack1ll11ll_opy_ (u"ࠫࠬౙ")
      if context.failed is True:
        bstack1ll1l1l111_opy_ = []
        bstack1l1l1111ll_opy_ = []
        bstack11ll11l1_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack1ll1l1l111_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack11lll11l_opy_ = traceback.format_tb(exc_tb)
            bstack1l11l1111_opy_ = bstack1ll11ll_opy_ (u"ࠬࠦࠧౚ").join(bstack11lll11l_opy_)
            bstack1l1l1111ll_opy_.append(bstack1l11l1111_opy_)
            bstack11ll11l1_opy_.append(bstack11lll11l_opy_[-1])
        except Exception as e:
          logger.debug(bstack1111l11l1_opy_.format(str(e)))
        bstack11l1ll11_opy_ = bstack1ll11ll_opy_ (u"࠭ࠧ౛")
        for i in range(len(bstack1ll1l1l111_opy_)):
          bstack11l1ll11_opy_ += bstack1ll1l1l111_opy_[i] + bstack11ll11l1_opy_[i] + bstack1ll11ll_opy_ (u"ࠧ࡝ࡰࠪ౜")
        bstack1lll1lll11_opy_ = bstack1ll11ll_opy_ (u"ࠨࠢࠪౝ").join(bstack1l1l1111ll_opy_)
        if runner.driver_initialised in [bstack1ll11ll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠥ౞"), bstack1ll11ll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢ౟")]:
          bstack1ll11lll11_opy_(context, bstack1lll1lll11_opy_, bstack1ll11ll_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥౠ"))
          bstack1l11ll11l_opy_(getattr(context, bstack1ll11ll_opy_ (u"ࠬࡶࡡࡨࡧࠪౡ"), None), bstack1ll11ll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨౢ"), bstack11l1ll11_opy_)
          bstack1l1111l11_opy_.execute_script(bstack1ll11ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬౣ") + json.dumps(bstack1lll1lll11_opy_) + bstack1ll11ll_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨ౤"))
          bstack1l11lllll1_opy_(bstack1l1111l11_opy_, bstack1ll11ll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ౥"), bstack1ll11ll_opy_ (u"ࠥࡗࡴࡳࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱࡶࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࡢ࡮ࠣ౦") + str(bstack11l1ll11_opy_))
          bstack11llll1ll1_opy_ = bstack11l11l1l1_opy_(bstack1lll1lll11_opy_, runner.feature.name, logger)
          if (bstack11llll1ll1_opy_ != None):
            bstack1l111lll_opy_.append(bstack11llll1ll1_opy_)
      else:
        if runner.driver_initialised in [bstack1ll11ll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠧ౧"), bstack1ll11ll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤ౨")]:
          bstack1ll11lll11_opy_(context, bstack1ll11ll_opy_ (u"ࠨࡆࡦࡣࡷࡹࡷ࡫࠺ࠡࠤ౩") + str(runner.feature.name) + bstack1ll11ll_opy_ (u"ࠢࠡࡲࡤࡷࡸ࡫ࡤࠢࠤ౪"), bstack1ll11ll_opy_ (u"ࠣ࡫ࡱࡪࡴࠨ౫"))
          bstack1l11ll11l_opy_(getattr(context, bstack1ll11ll_opy_ (u"ࠩࡳࡥ࡬࡫ࠧ౬"), None), bstack1ll11ll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ౭"))
          bstack1l1111l11_opy_.execute_script(bstack1ll11ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ౮") + json.dumps(bstack1ll11ll_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࡀࠠࠣ౯") + str(runner.feature.name) + bstack1ll11ll_opy_ (u"ࠨࠠࡱࡣࡶࡷࡪࡪࠡࠣ౰")) + bstack1ll11ll_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥࢁࢂ࠭౱"))
          bstack1l11lllll1_opy_(bstack1l1111l11_opy_, bstack1ll11ll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ౲"))
          bstack11llll1ll1_opy_ = bstack11l11l1l1_opy_(bstack1lll1lll11_opy_, runner.feature.name, logger)
          if (bstack11llll1ll1_opy_ != None):
            bstack1l111lll_opy_.append(bstack11llll1ll1_opy_)
    except Exception as e:
      logger.debug(bstack1ll11ll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫ౳").format(str(e)))
    bstack11lllll1l_opy_(runner, name, context, context.feature, bstack1lllllll11_opy_, *args)
@measure(event_name=EVENTS.bstack1ll11l111l_opy_, stage=STAGE.bstack11lll1ll1l_opy_, hook_type=bstack1ll11ll_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࡃ࡯ࡰࠧ౴"), bstack11ll1l1l_opy_=bstack111l1l11_opy_)
def bstack1l1l1ll11_opy_(runner, name, context, bstack1lllllll11_opy_, *args):
    bstack11lllll1l_opy_(runner, name, context, runner, bstack1lllllll11_opy_, *args)
def bstack1l1ll11ll_opy_(self, name, context, *args):
  try:
    if bstack11l1ll11l_opy_:
      platform_index = int(threading.current_thread()._name) % bstack11ll1lllll_opy_
      bstack1l11ll111l_opy_ = CONFIG[bstack1ll11ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ౵")][platform_index]
      os.environ[bstack1ll11ll_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭౶")] = json.dumps(bstack1l11ll111l_opy_)
    global bstack1lllllll11_opy_
    if not hasattr(self, bstack1ll11ll_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡧࡧࠫ౷")):
      self.driver_initialised = None
    bstack1l1l1l111_opy_ = {
        bstack1ll11ll_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠫ౸"): bstack1l11l11ll_opy_,
        bstack1ll11ll_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠩ౹"): bstack11l1ll11ll_opy_,
        bstack1ll11ll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡷࡥ࡬࠭౺"): bstack11ll1llll1_opy_,
        bstack1ll11ll_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ౻"): bstack1lll11ll_opy_,
        bstack1ll11ll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠩ౼"): bstack11lll11l1_opy_,
        bstack1ll11ll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡺࡥࡱࠩ౽"): bstack11ll11111l_opy_,
        bstack1ll11ll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧ౾"): bstack11ll1lll1_opy_,
        bstack1ll11ll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡴࡢࡩࠪ౿"): bstack1l1lllll11_opy_,
        bstack1ll11ll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨಀ"): bstack1ll1l1ll1l_opy_,
        bstack1ll11ll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠬಁ"): bstack1l1l1ll11_opy_
    }
    handler = bstack1l1l1l111_opy_.get(name, bstack1lllllll11_opy_)
    try:
      handler(self, name, context, bstack1lllllll11_opy_, *args)
    except Exception as e:
      logger.debug(bstack1ll11ll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡨࡥࡩࡣࡹࡩࠥ࡮࡯ࡰ࡭ࠣ࡬ࡦࡴࡤ࡭ࡧࡵࠤࢀࢃ࠺ࠡࡽࢀࠫಂ").format(name, str(e)))
    if name in [bstack1ll11ll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫಃ"), bstack1ll11ll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭಄"), bstack1ll11ll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠩಅ")]:
      try:
        bstack1l1111l11_opy_ = threading.current_thread().bstackSessionDriver if bstack11llllll1l_opy_(bstack1ll11ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ಆ")) else context.browser
        bstack1lll1llll1_opy_ = (
          (name == bstack1ll11ll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠫಇ") and self.driver_initialised == bstack1ll11ll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨಈ")) or
          (name == bstack1ll11ll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪಉ") and self.driver_initialised == bstack1ll11ll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠧಊ")) or
          (name == bstack1ll11ll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ಋ") and self.driver_initialised in [bstack1ll11ll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣಌ"), bstack1ll11ll_opy_ (u"ࠢࡪࡰࡶࡸࡪࡶࠢ಍")]) or
          (name == bstack1ll11ll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡴࡶࡨࡴࠬಎ") and self.driver_initialised == bstack1ll11ll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢಏ"))
        )
        if bstack1lll1llll1_opy_:
          self.driver_initialised = None
          if bstack1l1111l11_opy_ and hasattr(bstack1l1111l11_opy_, bstack1ll11ll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠧಐ")):
            try:
              bstack1l1111l11_opy_.quit()
            except Exception as e:
              logger.debug(bstack1ll11ll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡵࡺ࡯ࡴࡵ࡫ࡱ࡫ࠥࡪࡲࡪࡸࡨࡶࠥ࡯࡮ࠡࡤࡨ࡬ࡦࡼࡥࠡࡪࡲࡳࡰࡀࠠࡼࡿࠪ಑").format(str(e)))
      except Exception as e:
        logger.debug(bstack1ll11ll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡨࡰࡱ࡮ࠤࡨࡲࡥࡢࡰࡸࡴࠥ࡬࡯ࡳࠢࡾࢁ࠿ࠦࡻࡾࠩಒ").format(name, str(e)))
  except Exception as e:
    logger.debug(bstack1ll11ll_opy_ (u"࠭ࡃࡳ࡫ࡷ࡭ࡨࡧ࡬ࠡࡧࡵࡶࡴࡸࠠࡪࡰࠣࡦࡪ࡮ࡡࡷࡧࠣࡶࡺࡴࠠࡩࡱࡲ࡯ࠥࢁࡽ࠻ࠢࡾࢁࠬಓ").format(name, str(e)))
    try:
      bstack1lllllll11_opy_(self, name, context, *args)
    except Exception as e2:
      logger.debug(bstack1ll11ll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡥࡱࡲࡢࡢࡥ࡮ࠤࡴࡸࡩࡨ࡫ࡱࡥࡱࠦࡢࡦࡪࡤࡺࡪࠦࡨࡰࡱ࡮ࠤࢀࢃ࠺ࠡࡽࢀࠫಔ").format(name, str(e2)))
def bstack11l111l1ll_opy_(config, startdir):
  return bstack1ll11ll_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾ࠴ࢂࠨಕ").format(bstack1ll11ll_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣಖ"))
notset = Notset()
def bstack1l11l11l11_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1ll1ll1111_opy_
  if str(name).lower() == bstack1ll11ll_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪಗ"):
    return bstack1ll11ll_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥಘ")
  else:
    return bstack1ll1ll1111_opy_(self, name, default, skip)
def bstack1l11llll1_opy_(item, when):
  global bstack11ll111lll_opy_
  try:
    bstack11ll111lll_opy_(item, when)
  except Exception as e:
    pass
def bstack11l1ll1ll_opy_():
  return
def bstack1ll1ll1ll_opy_(type, name, status, reason, bstack1llll1llll_opy_, bstack1l1ll111l1_opy_):
  bstack111ll111l_opy_ = {
    bstack1ll11ll_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬಙ"): type,
    bstack1ll11ll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩಚ"): {}
  }
  if type == bstack1ll11ll_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩಛ"):
    bstack111ll111l_opy_[bstack1ll11ll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫಜ")][bstack1ll11ll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨಝ")] = bstack1llll1llll_opy_
    bstack111ll111l_opy_[bstack1ll11ll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ಞ")][bstack1ll11ll_opy_ (u"ࠫࡩࡧࡴࡢࠩಟ")] = json.dumps(str(bstack1l1ll111l1_opy_))
  if type == bstack1ll11ll_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ಠ"):
    bstack111ll111l_opy_[bstack1ll11ll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩಡ")][bstack1ll11ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬಢ")] = name
  if type == bstack1ll11ll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫಣ"):
    bstack111ll111l_opy_[bstack1ll11ll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬತ")][bstack1ll11ll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪಥ")] = status
    if status == bstack1ll11ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫದ"):
      bstack111ll111l_opy_[bstack1ll11ll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨಧ")][bstack1ll11ll_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ನ")] = json.dumps(str(reason))
  bstack111111l1_opy_ = bstack1ll11ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬ಩").format(json.dumps(bstack111ll111l_opy_))
  return bstack111111l1_opy_
def bstack1lll1lll1_opy_(driver_command, response):
    if driver_command == bstack1ll11ll_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬಪ"):
        bstack1l11ll1l_opy_.bstack1111l1111_opy_({
            bstack1ll11ll_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨಫ"): response[bstack1ll11ll_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩಬ")],
            bstack1ll11ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫಭ"): bstack1l11ll1l_opy_.current_test_uuid()
        })
def bstack1lll1l1ll_opy_(item, call, rep):
  global bstack1lll111111_opy_
  global bstack1lll1ll1l1_opy_
  global bstack11l1111ll_opy_
  name = bstack1ll11ll_opy_ (u"ࠬ࠭ಮ")
  try:
    if rep.when == bstack1ll11ll_opy_ (u"࠭ࡣࡢ࡮࡯ࠫಯ"):
      bstack1ll1111ll1_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack11l1111ll_opy_:
          name = str(rep.nodeid)
          bstack1l11lllll_opy_ = bstack1ll1ll1ll_opy_(bstack1ll11ll_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨರ"), name, bstack1ll11ll_opy_ (u"ࠨࠩಱ"), bstack1ll11ll_opy_ (u"ࠩࠪಲ"), bstack1ll11ll_opy_ (u"ࠪࠫಳ"), bstack1ll11ll_opy_ (u"ࠫࠬ಴"))
          threading.current_thread().bstack11l1l1ll_opy_ = name
          for driver in bstack1lll1ll1l1_opy_:
            if bstack1ll1111ll1_opy_ == driver.session_id:
              driver.execute_script(bstack1l11lllll_opy_)
      except Exception as e:
        logger.debug(bstack1ll11ll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬವ").format(str(e)))
      try:
        bstack111llll11_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack1ll11ll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧಶ"):
          status = bstack1ll11ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧಷ") if rep.outcome.lower() == bstack1ll11ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨಸ") else bstack1ll11ll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩಹ")
          reason = bstack1ll11ll_opy_ (u"ࠪࠫ಺")
          if status == bstack1ll11ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ಻"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack1ll11ll_opy_ (u"ࠬ࡯࡮ࡧࡱ಼ࠪ") if status == bstack1ll11ll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ಽ") else bstack1ll11ll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ಾ")
          data = name + bstack1ll11ll_opy_ (u"ࠨࠢࡳࡥࡸࡹࡥࡥࠣࠪಿ") if status == bstack1ll11ll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩೀ") else name + bstack1ll11ll_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠥࠥ࠭ು") + reason
          bstack11l11ll11_opy_ = bstack1ll1ll1ll_opy_(bstack1ll11ll_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭ೂ"), bstack1ll11ll_opy_ (u"ࠬ࠭ೃ"), bstack1ll11ll_opy_ (u"࠭ࠧೄ"), bstack1ll11ll_opy_ (u"ࠧࠨ೅"), level, data)
          for driver in bstack1lll1ll1l1_opy_:
            if bstack1ll1111ll1_opy_ == driver.session_id:
              driver.execute_script(bstack11l11ll11_opy_)
      except Exception as e:
        logger.debug(bstack1ll11ll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡩ࡯࡯ࡶࡨࡼࡹࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬೆ").format(str(e)))
  except Exception as e:
    logger.debug(bstack1ll11ll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡴࡢࡶࡨࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿࢂ࠭ೇ").format(str(e)))
  bstack1lll111111_opy_(item, call, rep)
def bstack1lll1l11ll_opy_(driver, bstack11lll111l_opy_, test=None):
  global bstack11l111lll_opy_
  if test != None:
    bstack1l1llll1ll_opy_ = getattr(test, bstack1ll11ll_opy_ (u"ࠪࡲࡦࡳࡥࠨೈ"), None)
    bstack11l1l11l_opy_ = getattr(test, bstack1ll11ll_opy_ (u"ࠫࡺࡻࡩࡥࠩ೉"), None)
    PercySDK.screenshot(driver, bstack11lll111l_opy_, bstack1l1llll1ll_opy_=bstack1l1llll1ll_opy_, bstack11l1l11l_opy_=bstack11l1l11l_opy_, bstack1ll11l1l11_opy_=bstack11l111lll_opy_)
  else:
    PercySDK.screenshot(driver, bstack11lll111l_opy_)
@measure(event_name=EVENTS.bstack1llll1ll11_opy_, stage=STAGE.bstack11lll1ll1l_opy_, bstack11ll1l1l_opy_=bstack111l1l11_opy_)
def bstack11l1l11l1_opy_(driver):
  if bstack11ll1111l_opy_.bstack111llll111_opy_() is True or bstack11ll1111l_opy_.capturing() is True:
    return
  bstack11ll1111l_opy_.bstack1l11l11l_opy_()
  while not bstack11ll1111l_opy_.bstack111llll111_opy_():
    bstack1l1ll1l1l1_opy_ = bstack11ll1111l_opy_.bstack1ll1111111_opy_()
    bstack1lll1l11ll_opy_(driver, bstack1l1ll1l1l1_opy_)
  bstack11ll1111l_opy_.bstack1ll11l1l1_opy_()
def bstack111llllll_opy_(sequence, driver_command, response = None, bstack1l1l1llll_opy_ = None, args = None):
    try:
      if sequence != bstack1ll11ll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬೊ"):
        return
      if percy.bstack11ll1ll1l_opy_() == bstack1ll11ll_opy_ (u"ࠨࡦࡢ࡮ࡶࡩࠧೋ"):
        return
      bstack1l1ll1l1l1_opy_ = bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪೌ"), None)
      for command in bstack1111lll1l_opy_:
        if command == driver_command:
          with bstack11ll111l_opy_:
            bstack1l1l1l1ll_opy_ = bstack1lll1ll1l1_opy_.copy()
          for driver in bstack1l1l1l1ll_opy_:
            bstack11l1l11l1_opy_(driver)
      bstack11l1lll111_opy_ = percy.bstack1l11ll1ll1_opy_()
      if driver_command in bstack11111lll1_opy_[bstack11l1lll111_opy_]:
        bstack11ll1111l_opy_.bstack1111111ll_opy_(bstack1l1ll1l1l1_opy_, driver_command)
    except Exception as e:
      pass
def bstack1l1l111ll_opy_(framework_name):
  if bstack1l111111l1_opy_.get_property(bstack1ll11ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨ್ࠬ")):
      return
  bstack1l111111l1_opy_.bstack11l111l1l_opy_(bstack1ll11ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡰࡳࡩࡥࡣࡢ࡮࡯ࡩࡩ࠭೎"), True)
  global bstack11l1lll1l1_opy_
  global bstack1l1l1lll1_opy_
  global bstack11llll11_opy_
  bstack11l1lll1l1_opy_ = framework_name
  logger.info(bstack1l11lll1l1_opy_.format(bstack11l1lll1l1_opy_.split(bstack1ll11ll_opy_ (u"ࠪ࠱ࠬ೏"))[0]))
  bstack1lllll1l1_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack11l1ll11l_opy_:
      Service.start = bstack11lll11l1l_opy_
      Service.stop = bstack11l1l11ll1_opy_
      webdriver.Remote.get = bstack1llllll1l1_opy_
      WebDriver.quit = bstack1llll1l11l_opy_
      webdriver.Remote.__init__ = bstack11ll1ll111_opy_
    if not bstack11l1ll11l_opy_:
        webdriver.Remote.__init__ = bstack11lll1111_opy_
    WebDriver.getAccessibilityResults = getAccessibilityResults
    WebDriver.get_accessibility_results = getAccessibilityResults
    WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
    WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
    WebDriver.performScan = perform_scan
    WebDriver.perform_scan = perform_scan
    WebDriver.execute = bstack111lll111_opy_
    bstack1l1l1lll1_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack11l1ll11l_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack111lll1ll1_opy_
  except Exception as e:
    pass
  bstack111ll1ll_opy_()
  if not bstack1l1l1lll1_opy_:
    bstack1ll1l1l1_opy_(bstack1ll11ll_opy_ (u"ࠦࡕࡧࡣ࡬ࡣࡪࡩࡸࠦ࡮ࡰࡶࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠨ೐"), bstack1111ll11l_opy_)
  if bstack1l1ll1lll_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      if hasattr(RemoteConnection, bstack1ll11ll_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭೑")) and callable(getattr(RemoteConnection, bstack1ll11ll_opy_ (u"࠭࡟ࡨࡧࡷࡣࡵࡸ࡯ࡹࡻࡢࡹࡷࡲࠧ೒"))):
        RemoteConnection._get_proxy_url = bstack1l1lllllll_opy_
      else:
        from selenium.webdriver.remote.client_config import ClientConfig
        ClientConfig.get_proxy_url = bstack1l1lllllll_opy_
    except Exception as e:
      logger.error(bstack11l11llll1_opy_.format(str(e)))
  if bstack1llll11l11_opy_():
    bstack1l111ll111_opy_(CONFIG, logger)
  if (bstack1ll11ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭೓") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if percy.bstack11ll1ll1l_opy_() == bstack1ll11ll_opy_ (u"ࠣࡶࡵࡹࡪࠨ೔"):
          bstack1ll11l11_opy_(bstack111llllll_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1ll11ll111_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack11l1l11ll_opy_
      except Exception as e:
        logger.warn(bstack1l1ll1l1_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1l1l11llll_opy_
      except Exception as e:
        logger.debug(bstack1lll1l1l1_opy_ + str(e))
    except Exception as e:
      bstack1ll1l1l1_opy_(e, bstack1l1ll1l1_opy_)
    Output.start_test = bstack11lll1111l_opy_
    Output.end_test = bstack11llll1l1_opy_
    TestStatus.__init__ = bstack11ll11l1ll_opy_
    QueueItem.__init__ = bstack1ll11l1ll_opy_
    pabot._create_items = bstack111111l1l_opy_
    try:
      from pabot import __version__ as bstack1ll11l11l_opy_
      if version.parse(bstack1ll11l11l_opy_) >= version.parse(bstack1ll11ll_opy_ (u"ࠩ࠸࠲࠵࠴࠰ࠨೕ")):
        pabot._run = bstack111l1llll_opy_
      elif version.parse(bstack1ll11l11l_opy_) >= version.parse(bstack1ll11ll_opy_ (u"ࠪ࠸࠳࠸࠮࠱ࠩೖ")):
        pabot._run = bstack1ll1l1ll_opy_
      elif version.parse(bstack1ll11l11l_opy_) >= version.parse(bstack1ll11ll_opy_ (u"ࠫ࠷࠴࠱࠶࠰࠳ࠫ೗")):
        pabot._run = bstack1lll11l11l_opy_
      elif version.parse(bstack1ll11l11l_opy_) >= version.parse(bstack1ll11ll_opy_ (u"ࠬ࠸࠮࠲࠵࠱࠴ࠬ೘")):
        pabot._run = bstack1lllllll1l_opy_
      else:
        pabot._run = bstack11llllll1_opy_
    except Exception as e:
      pabot._run = bstack11llllll1_opy_
    pabot._create_command_for_execution = bstack1ll1111l11_opy_
    pabot._report_results = bstack111llll1l_opy_
  if bstack1ll11ll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭೙") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll1l1l1_opy_(e, bstack111l111l_opy_)
    Runner.run_hook = bstack1l1ll11ll_opy_
    Step.run = bstack1ll1llllll_opy_
  if bstack1ll11ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ೚") in str(framework_name).lower():
    if not bstack11l1ll11l_opy_:
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack11l111l1ll_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack11l1ll1ll_opy_
      Config.getoption = bstack1l11l11l11_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1lll1l1ll_opy_
    except Exception as e:
      pass
def bstack1l1l11l1l_opy_():
  global CONFIG
  if bstack1ll11ll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ೛") in CONFIG and int(CONFIG[bstack1ll11ll_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ೜")]) > 1:
    logger.warn(bstack1ll1l11l1l_opy_)
def bstack1ll1ll1ll1_opy_(arg, bstack11lll111ll_opy_, bstack1ll11lll1_opy_=None):
  global CONFIG
  global bstack11lll1lll_opy_
  global bstack1l1lll1l1l_opy_
  global bstack11l1ll11l_opy_
  global bstack1l111111l1_opy_
  bstack1l1llll1l1_opy_ = bstack1ll11ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪೝ")
  if bstack11lll111ll_opy_ and isinstance(bstack11lll111ll_opy_, str):
    bstack11lll111ll_opy_ = eval(bstack11lll111ll_opy_)
  CONFIG = bstack11lll111ll_opy_[bstack1ll11ll_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫೞ")]
  bstack11lll1lll_opy_ = bstack11lll111ll_opy_[bstack1ll11ll_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭೟")]
  bstack1l1lll1l1l_opy_ = bstack11lll111ll_opy_[bstack1ll11ll_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨೠ")]
  bstack11l1ll11l_opy_ = bstack11lll111ll_opy_[bstack1ll11ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪೡ")]
  bstack1l111111l1_opy_.bstack11l111l1l_opy_(bstack1ll11ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩೢ"), bstack11l1ll11l_opy_)
  os.environ[bstack1ll11ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫೣ")] = bstack1l1llll1l1_opy_
  os.environ[bstack1ll11ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠩ೤")] = json.dumps(CONFIG)
  os.environ[bstack1ll11ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡌ࡚ࡈ࡟ࡖࡔࡏࠫ೥")] = bstack11lll1lll_opy_
  os.environ[bstack1ll11ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭೦")] = str(bstack1l1lll1l1l_opy_)
  os.environ[bstack1ll11ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡌࡖࡉࡌࡒࠬ೧")] = str(True)
  if bstack1l11ll1l1_opy_(arg, [bstack1ll11ll_opy_ (u"ࠧ࠮ࡰࠪ೨"), bstack1ll11ll_opy_ (u"ࠨ࠯࠰ࡲࡺࡳࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩ೩")]) != -1:
    os.environ[bstack1ll11ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡄࡖࡆࡒࡌࡆࡎࠪ೪")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1ll11ll11l_opy_)
    return
  bstack1ll1l11l1_opy_()
  global bstack11l11ll1_opy_
  global bstack11l111lll_opy_
  global bstack1lll11lll1_opy_
  global bstack11ll1111_opy_
  global bstack11l1l1lll1_opy_
  global bstack11llll11_opy_
  global bstack111llll1ll_opy_
  arg.append(bstack1ll11ll_opy_ (u"ࠥ࠱࡜ࠨ೫"))
  arg.append(bstack1ll11ll_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨ࠾ࡒࡵࡤࡶ࡮ࡨࠤࡦࡲࡲࡦࡣࡧࡽࠥ࡯࡭ࡱࡱࡵࡸࡪࡪ࠺ࡱࡻࡷࡩࡸࡺ࠮ࡑࡻࡷࡩࡸࡺࡗࡢࡴࡱ࡭ࡳ࡭ࠢ೬"))
  arg.append(bstack1ll11ll_opy_ (u"ࠧ࠳ࡗࠣ೭"))
  arg.append(bstack1ll11ll_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡀࡔࡩࡧࠣ࡬ࡴࡵ࡫ࡪ࡯ࡳࡰࠧ೮"))
  global bstack1lll11ll11_opy_
  global bstack11l1111l1l_opy_
  global bstack1ll1llll1_opy_
  global bstack11l1l1l1l_opy_
  global bstack1llllllll_opy_
  global bstack1lll111l1_opy_
  global bstack1lllll1l11_opy_
  global bstack1l1llllll1_opy_
  global bstack111l11l1l_opy_
  global bstack111lllll11_opy_
  global bstack1ll1ll1111_opy_
  global bstack11ll111lll_opy_
  global bstack1lll111111_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1lll11ll11_opy_ = webdriver.Remote.__init__
    bstack11l1111l1l_opy_ = WebDriver.quit
    bstack1l1llllll1_opy_ = WebDriver.close
    bstack111l11l1l_opy_ = WebDriver.get
    bstack1ll1llll1_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack11l11lll1l_opy_(CONFIG) and bstack111111ll_opy_():
    if bstack1l11111111_opy_() < version.parse(bstack111l1lll_opy_):
      logger.error(bstack1lll1l1l1l_opy_.format(bstack1l11111111_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack1ll11ll_opy_ (u"ࠧࡠࡩࡨࡸࡤࡶࡲࡰࡺࡼࡣࡺࡸ࡬ࠨ೯")) and callable(getattr(RemoteConnection, bstack1ll11ll_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩ೰"))):
          bstack111lllll11_opy_ = RemoteConnection._get_proxy_url
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          bstack111lllll11_opy_ = ClientConfig.get_proxy_url
      except Exception as e:
        logger.error(bstack11l11llll1_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1ll1ll1111_opy_ = Config.getoption
    from _pytest import runner
    bstack11ll111lll_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack1llll1111_opy_)
  try:
    from pytest_bdd import reporting
    bstack1lll111111_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack1ll11ll_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡱࠣࡶࡺࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࡵࠪೱ"))
  bstack1lll11lll1_opy_ = CONFIG.get(bstack1ll11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧೲ"), {}).get(bstack1ll11ll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ೳ"))
  bstack111llll1ll_opy_ = True
  if cli.is_enabled(CONFIG):
    if cli.bstack11l1l1l1ll_opy_():
      bstack1111ll1l_opy_.invoke(bstack11l1lll1l_opy_.CONNECT, bstack1l1llllll_opy_())
    platform_index = int(os.environ.get(bstack1ll11ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ೴"), bstack1ll11ll_opy_ (u"࠭࠰ࠨ೵")))
  else:
    bstack1l1l111ll_opy_(bstack1l11l11ll1_opy_)
  os.environ[bstack1ll11ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨ೶")] = CONFIG[bstack1ll11ll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ೷")]
  os.environ[bstack1ll11ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬ೸")] = CONFIG[bstack1ll11ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭೹")]
  os.environ[bstack1ll11ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ೺")] = bstack11l1ll11l_opy_.__str__()
  from _pytest.config import main as bstack1l1lll11_opy_
  bstack1l1ll1ll1_opy_ = []
  try:
    exit_code = bstack1l1lll11_opy_(arg)
    if cli.is_enabled(CONFIG):
      cli.bstack1l11l1ll1l_opy_()
    if bstack1ll11ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩ೻") in multiprocessing.current_process().__dict__.keys():
      for bstack11l1ll1111_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1l1ll1ll1_opy_.append(bstack11l1ll1111_opy_)
    try:
      bstack111111lll_opy_ = (bstack1l1ll1ll1_opy_, int(exit_code))
      bstack1ll11lll1_opy_.append(bstack111111lll_opy_)
    except:
      bstack1ll11lll1_opy_.append((bstack1l1ll1ll1_opy_, exit_code))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack1l1ll1ll1_opy_.append({bstack1ll11ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ೼"): bstack1ll11ll_opy_ (u"ࠧࡑࡴࡲࡧࡪࡹࡳࠡࠩ೽") + os.environ.get(bstack1ll11ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ೾")), bstack1ll11ll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ೿"): traceback.format_exc(), bstack1ll11ll_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩഀ"): int(os.environ.get(bstack1ll11ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫഁ")))})
    bstack1ll11lll1_opy_.append((bstack1l1ll1ll1_opy_, 1))
def mod_behave_main(args, retries):
  try:
    from behave.configuration import Configuration
    from behave.__main__ import run_behave
    from browserstack_sdk.bstack_behave_runner import BehaveRunner
    config = Configuration(args)
    config.update_userdata({bstack1ll11ll_opy_ (u"ࠧࡸࡥࡵࡴ࡬ࡩࡸࠨം"): str(retries)})
    return run_behave(config, runner_class=BehaveRunner)
  except Exception as e:
    bstack11ll111l1_opy_ = e.__class__.__name__
    print(bstack1ll11ll_opy_ (u"ࠨࠥࡴ࠼ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡦࡪ࡮ࡡࡷࡧࠣࡸࡪࡹࡴࠡࠧࡶࠦഃ") % (bstack11ll111l1_opy_, e))
    return 1
def bstack111l111ll_opy_(arg):
  global bstack11l1l1l11_opy_
  bstack1l1l111ll_opy_(bstack1lll11ll1l_opy_)
  os.environ[bstack1ll11ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨഄ")] = str(bstack1l1lll1l1l_opy_)
  retries = bstack1ll1l111_opy_.bstack1ll11ll1l_opy_(CONFIG)
  status_code = 0
  if bstack1ll1l111_opy_.bstack11l1lll11_opy_(CONFIG):
    status_code = mod_behave_main(arg, retries)
  else:
    from behave.__main__ import main as bstack11l1l1ll11_opy_
    status_code = bstack11l1l1ll11_opy_(arg)
  if status_code != 0:
    bstack11l1l1l11_opy_ = status_code
def bstack1lll1ll1l_opy_():
  logger.info(bstack11l1l1l1_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1ll11ll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧഅ"), help=bstack1ll11ll_opy_ (u"ࠩࡊࡩࡳ࡫ࡲࡢࡶࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡧࡴࡴࡦࡪࡩࠪആ"))
  parser.add_argument(bstack1ll11ll_opy_ (u"ࠪ࠱ࡺ࠭ഇ"), bstack1ll11ll_opy_ (u"ࠫ࠲࠳ࡵࡴࡧࡵࡲࡦࡳࡥࠨഈ"), help=bstack1ll11ll_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫഉ"))
  parser.add_argument(bstack1ll11ll_opy_ (u"࠭࠭࡬ࠩഊ"), bstack1ll11ll_opy_ (u"ࠧ࠮࠯࡮ࡩࡾ࠭ഋ"), help=bstack1ll11ll_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡧࡣࡤࡧࡶࡷࠥࡱࡥࡺࠩഌ"))
  parser.add_argument(bstack1ll11ll_opy_ (u"ࠩ࠰ࡪࠬ഍"), bstack1ll11ll_opy_ (u"ࠪ࠱࠲࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨഎ"), help=bstack1ll11ll_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪഏ"))
  bstack1lll11111_opy_ = parser.parse_args()
  try:
    bstack1llll1111l_opy_ = bstack1ll11ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡬࡫࡮ࡦࡴ࡬ࡧ࠳ࡿ࡭࡭࠰ࡶࡥࡲࡶ࡬ࡦࠩഐ")
    if bstack1lll11111_opy_.framework and bstack1lll11111_opy_.framework not in (bstack1ll11ll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭഑"), bstack1ll11ll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨഒ")):
      bstack1llll1111l_opy_ = bstack1ll11ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࠱ࡽࡲࡲ࠮ࡴࡣࡰࡴࡱ࡫ࠧഓ")
    bstack111l1111l_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1llll1111l_opy_)
    bstack1llll1ll_opy_ = open(bstack111l1111l_opy_, bstack1ll11ll_opy_ (u"ࠩࡵࠫഔ"))
    bstack1l1111ll11_opy_ = bstack1llll1ll_opy_.read()
    bstack1llll1ll_opy_.close()
    if bstack1lll11111_opy_.username:
      bstack1l1111ll11_opy_ = bstack1l1111ll11_opy_.replace(bstack1ll11ll_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪക"), bstack1lll11111_opy_.username)
    if bstack1lll11111_opy_.key:
      bstack1l1111ll11_opy_ = bstack1l1111ll11_opy_.replace(bstack1ll11ll_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭ഖ"), bstack1lll11111_opy_.key)
    if bstack1lll11111_opy_.framework:
      bstack1l1111ll11_opy_ = bstack1l1111ll11_opy_.replace(bstack1ll11ll_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ഗ"), bstack1lll11111_opy_.framework)
    file_name = bstack1ll11ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩഘ")
    file_path = os.path.abspath(file_name)
    bstack111l1lll1_opy_ = open(file_path, bstack1ll11ll_opy_ (u"ࠧࡸࠩങ"))
    bstack111l1lll1_opy_.write(bstack1l1111ll11_opy_)
    bstack111l1lll1_opy_.close()
    logger.info(bstack1lll1lllll_opy_)
    try:
      os.environ[bstack1ll11ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪച")] = bstack1lll11111_opy_.framework if bstack1lll11111_opy_.framework != None else bstack1ll11ll_opy_ (u"ࠤࠥഛ")
      config = yaml.safe_load(bstack1l1111ll11_opy_)
      config[bstack1ll11ll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪജ")] = bstack1ll11ll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱ࡸ࡫ࡴࡶࡲࠪഝ")
      bstack111l1ll1_opy_(bstack1llll111l_opy_, config)
    except Exception as e:
      logger.debug(bstack1l1111llll_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1llllll11l_opy_.format(str(e)))
def bstack111l1ll1_opy_(bstack1ll1l11ll1_opy_, config, bstack1lll111ll1_opy_={}):
  global bstack11l1ll11l_opy_
  global bstack11lll11111_opy_
  global bstack1l111111l1_opy_
  if not config:
    return
  bstack11l1ll111_opy_ = bstack1ll1ll1l_opy_ if not bstack11l1ll11l_opy_ else (
    bstack1lll1ll11_opy_ if bstack1ll11ll_opy_ (u"ࠬࡧࡰࡱࠩഞ") in config else (
        bstack1l1ll1l1ll_opy_ if config.get(bstack1ll11ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪട")) else bstack1ll1lll1ll_opy_
    )
)
  bstack1111l1ll_opy_ = False
  bstack111l11ll_opy_ = False
  if bstack11l1ll11l_opy_ is True:
      if bstack1ll11ll_opy_ (u"ࠧࡢࡲࡳࠫഠ") in config:
          bstack1111l1ll_opy_ = True
      else:
          bstack111l11ll_opy_ = True
  bstack1l1l1111l_opy_ = bstack111llll11l_opy_.bstack111lll11l_opy_(config, bstack11lll11111_opy_)
  bstack1l1l1l11l1_opy_ = bstack11ll1l1l11_opy_()
  data = {
    bstack1ll11ll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪഡ"): config[bstack1ll11ll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫഢ")],
    bstack1ll11ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ണ"): config[bstack1ll11ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧത")],
    bstack1ll11ll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩഥ"): bstack1ll1l11ll1_opy_,
    bstack1ll11ll_opy_ (u"࠭ࡤࡦࡶࡨࡧࡹ࡫ࡤࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪദ"): os.environ.get(bstack1ll11ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩധ"), bstack11lll11111_opy_),
    bstack1ll11ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪന"): bstack1l1lll1lll_opy_,
    bstack1ll11ll_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯ࠫഩ"): bstack11ll11l1l_opy_(),
    bstack1ll11ll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭പ"): {
      bstack1ll11ll_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩഫ"): str(config[bstack1ll11ll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬബ")]) if bstack1ll11ll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ഭ") in config else bstack1ll11ll_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣമ"),
      bstack1ll11ll_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧ࡙ࡩࡷࡹࡩࡰࡰࠪയ"): sys.version,
      bstack1ll11ll_opy_ (u"ࠩࡵࡩ࡫࡫ࡲࡳࡧࡵࠫര"): bstack1l1l111lll_opy_(os.environ.get(bstack1ll11ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬറ"), bstack11lll11111_opy_)),
      bstack1ll11ll_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭ല"): bstack1ll11ll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬള"),
      bstack1ll11ll_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧഴ"): bstack11l1ll111_opy_,
      bstack1ll11ll_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬവ"): bstack1l1l1111l_opy_,
      bstack1ll11ll_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡡࡸࡹ࡮ࡪࠧശ"): os.environ[bstack1ll11ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧഷ")],
      bstack1ll11ll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭സ"): os.environ.get(bstack1ll11ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ഹ"), bstack11lll11111_opy_),
      bstack1ll11ll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨഺ"): bstack1l1111l1_opy_(os.environ.get(bstack1ll11ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ഻"), bstack11lll11111_opy_)),
      bstack1ll11ll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ഼࠭"): bstack1l1l1l11l1_opy_.get(bstack1ll11ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ഽ")),
      bstack1ll11ll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨാ"): bstack1l1l1l11l1_opy_.get(bstack1ll11ll_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫി")),
      bstack1ll11ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧീ"): config[bstack1ll11ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨു")] if config[bstack1ll11ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩൂ")] else bstack1ll11ll_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣൃ"),
      bstack1ll11ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪൄ"): str(config[bstack1ll11ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ൅")]) if bstack1ll11ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬെ") in config else bstack1ll11ll_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧേ"),
      bstack1ll11ll_opy_ (u"ࠬࡵࡳࠨൈ"): sys.platform,
      bstack1ll11ll_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨ൉"): socket.gethostname(),
      bstack1ll11ll_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥࠩൊ"): bstack1l111111l1_opy_.get_property(bstack1ll11ll_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪോ"))
    }
  }
  if not bstack1l111111l1_opy_.get_property(bstack1ll11ll_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩൌ")) is None:
    data[bstack1ll11ll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ്࠭")][bstack1ll11ll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡓࡥࡵࡣࡧࡥࡹࡧࠧൎ")] = {
      bstack1ll11ll_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ൏"): bstack1ll11ll_opy_ (u"࠭ࡵࡴࡧࡵࡣࡰ࡯࡬࡭ࡧࡧࠫ൐"),
      bstack1ll11ll_opy_ (u"ࠧࡴ࡫ࡪࡲࡦࡲࠧ൑"): bstack1l111111l1_opy_.get_property(bstack1ll11ll_opy_ (u"ࠨࡵࡧ࡯ࡐ࡯࡬࡭ࡕ࡬࡫ࡳࡧ࡬ࠨ൒")),
      bstack1ll11ll_opy_ (u"ࠩࡶ࡭࡬ࡴࡡ࡭ࡐࡸࡱࡧ࡫ࡲࠨ൓"): bstack1l111111l1_opy_.get_property(bstack1ll11ll_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡒࡴ࠭ൔ"))
    }
  if bstack1ll1l11ll1_opy_ == bstack1l1lll111l_opy_:
    data[bstack1ll11ll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧൕ")][bstack1ll11ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡇࡴࡴࡦࡪࡩࠪൖ")] = bstack1llll1l1l_opy_(config)
    data[bstack1ll11ll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩൗ")][bstack1ll11ll_opy_ (u"ࠧࡪࡵࡓࡩࡷࡩࡹࡂࡷࡷࡳࡊࡴࡡࡣ࡮ࡨࡨࠬ൘")] = percy.bstack11l11l1lll_opy_
    data[bstack1ll11ll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫ൙")][bstack1ll11ll_opy_ (u"ࠩࡳࡩࡷࡩࡹࡃࡷ࡬ࡰࡩࡏࡤࠨ൚")] = percy.percy_build_id
  if not bstack1ll1l111_opy_.bstack11l1ll1l1l_opy_(CONFIG):
    data[bstack1ll11ll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭൛")][bstack1ll11ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠨ൜")] = bstack1ll1l111_opy_.bstack11l1ll1l1l_opy_(CONFIG)
  bstack1l1l1l11_opy_ = bstack1ll1l1ll1_opy_.bstack11l11lllll_opy_(CONFIG, logger)
  bstack11l1l11l11_opy_ = bstack1ll1l111_opy_.bstack11l11lllll_opy_(config=CONFIG)
  if bstack1l1l1l11_opy_ is not None and bstack11l1l11l11_opy_ is not None and bstack11l1l11l11_opy_.bstack11l11l11ll_opy_():
    data[bstack1ll11ll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨ൝")][bstack11l1l11l11_opy_.bstack1l1ll1l111_opy_()] = bstack1l1l1l11_opy_.bstack11l11111l1_opy_()
  update(data[bstack1ll11ll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩ൞")], bstack1lll111ll1_opy_)
  try:
    response = bstack1lllll1111_opy_(bstack1ll11ll_opy_ (u"ࠧࡑࡑࡖࡘࠬൟ"), bstack11ll11111_opy_(bstack111lll1lll_opy_), data, {
      bstack1ll11ll_opy_ (u"ࠨࡣࡸࡸ࡭࠭ൠ"): (config[bstack1ll11ll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫൡ")], config[bstack1ll11ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ൢ")])
    })
    if response:
      logger.debug(bstack1l11llll_opy_.format(bstack1ll1l11ll1_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1ll1ll11_opy_.format(str(e)))
def bstack1l1l111lll_opy_(framework):
  return bstack1ll11ll_opy_ (u"ࠦࢀࢃ࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴ࢁࡽࠣൣ").format(str(framework), __version__) if framework else bstack1ll11ll_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࡿࢂࠨ൤").format(
    __version__)
def bstack1ll1l11l1_opy_():
  global CONFIG
  global bstack11l111l111_opy_
  if bool(CONFIG):
    return
  try:
    bstack1l1lll1ll_opy_()
    logger.debug(bstack1ll1l11111_opy_.format(str(CONFIG)))
    bstack11l111l111_opy_ = bstack1lll1llll_opy_.configure_logger(CONFIG, bstack11l111l111_opy_)
    bstack1lllll1l1_opy_()
  except Exception as e:
    logger.error(bstack1ll11ll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࠥ൥") + str(e))
    sys.exit(1)
  sys.excepthook = bstack11lll1llll_opy_
  atexit.register(bstack11l111ll1l_opy_)
  signal.signal(signal.SIGINT, bstack1l111l111l_opy_)
  signal.signal(signal.SIGTERM, bstack1l111l111l_opy_)
def bstack11lll1llll_opy_(exctype, value, traceback):
  global bstack1lll1ll1l1_opy_
  try:
    for driver in bstack1lll1ll1l1_opy_:
      bstack1l11lllll1_opy_(driver, bstack1ll11ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ൦"), bstack1ll11ll_opy_ (u"ࠣࡕࡨࡷࡸ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦ൧") + str(value))
  except Exception:
    pass
  logger.info(bstack1lll1l11_opy_)
  bstack11l11111ll_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack11l11111ll_opy_(message=bstack1ll11ll_opy_ (u"ࠩࠪ൨"), bstack1ll1lll1_opy_ = False):
  global CONFIG
  bstack11111lll_opy_ = bstack1ll11ll_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠬ൩") if bstack1ll1lll1_opy_ else bstack1ll11ll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ൪")
  try:
    if message:
      bstack1lll111ll1_opy_ = {
        bstack11111lll_opy_ : str(message)
      }
      bstack111l1ll1_opy_(bstack1l1lll111l_opy_, CONFIG, bstack1lll111ll1_opy_)
    else:
      bstack111l1ll1_opy_(bstack1l1lll111l_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack11llll111_opy_.format(str(e)))
def bstack1l1l11l11_opy_(bstack1l1ll1ll11_opy_, size):
  bstack1l1ll1111_opy_ = []
  while len(bstack1l1ll1ll11_opy_) > size:
    bstack11l11l11_opy_ = bstack1l1ll1ll11_opy_[:size]
    bstack1l1ll1111_opy_.append(bstack11l11l11_opy_)
    bstack1l1ll1ll11_opy_ = bstack1l1ll1ll11_opy_[size:]
  bstack1l1ll1111_opy_.append(bstack1l1ll1ll11_opy_)
  return bstack1l1ll1111_opy_
def bstack1llll1ll1_opy_(args):
  if bstack1ll11ll_opy_ (u"ࠬ࠳࡭ࠨ൫") in args and bstack1ll11ll_opy_ (u"࠭ࡰࡥࡤࠪ൬") in args:
    return True
  return False
@measure(event_name=EVENTS.bstack11ll1l111l_opy_, stage=STAGE.bstack1l1ll1111l_opy_)
def run_on_browserstack(bstack11lll1l11l_opy_=None, bstack1ll11lll1_opy_=None, bstack11l1llll11_opy_=False):
  global CONFIG
  global bstack11lll1lll_opy_
  global bstack1l1lll1l1l_opy_
  global bstack11lll11111_opy_
  global bstack1l111111l1_opy_
  bstack1l1llll1l1_opy_ = bstack1ll11ll_opy_ (u"ࠧࠨ൭")
  bstack1l111l11ll_opy_(bstack1l1l11111l_opy_, logger)
  if bstack11lll1l11l_opy_ and isinstance(bstack11lll1l11l_opy_, str):
    bstack11lll1l11l_opy_ = eval(bstack11lll1l11l_opy_)
  if bstack11lll1l11l_opy_:
    CONFIG = bstack11lll1l11l_opy_[bstack1ll11ll_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨ൮")]
    bstack11lll1lll_opy_ = bstack11lll1l11l_opy_[bstack1ll11ll_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪ൯")]
    bstack1l1lll1l1l_opy_ = bstack11lll1l11l_opy_[bstack1ll11ll_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ൰")]
    bstack1l111111l1_opy_.bstack11l111l1l_opy_(bstack1ll11ll_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭൱"), bstack1l1lll1l1l_opy_)
    bstack1l1llll1l1_opy_ = bstack1ll11ll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ൲")
  bstack1l111111l1_opy_.bstack11l111l1l_opy_(bstack1ll11ll_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨ൳"), uuid4().__str__())
  logger.info(bstack1ll11ll_opy_ (u"ࠧࡔࡆࡎࠤࡷࡻ࡮ࠡࡵࡷࡥࡷࡺࡥࡥࠢࡺ࡭ࡹ࡮ࠠࡪࡦ࠽ࠤࠬ൴") + bstack1l111111l1_opy_.get_property(bstack1ll11ll_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪ൵")));
  logger.debug(bstack1ll11ll_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࡁࠬ൶") + bstack1l111111l1_opy_.get_property(bstack1ll11ll_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࠬ൷")))
  if not bstack11l1llll11_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1ll11ll11l_opy_)
      return
    if sys.argv[1] == bstack1ll11ll_opy_ (u"ࠫ࠲࠳ࡶࡦࡴࡶ࡭ࡴࡴࠧ൸") or sys.argv[1] == bstack1ll11ll_opy_ (u"ࠬ࠳ࡶࠨ൹"):
      logger.info(bstack1ll11ll_opy_ (u"࠭ࡂࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡖࡹࡵࡪࡲࡲ࡙ࠥࡄࡌࠢࡹࡿࢂ࠭ൺ").format(__version__))
      return
    if sys.argv[1] == bstack1ll11ll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ൻ"):
      bstack1lll1ll1l_opy_()
      return
  args = sys.argv
  bstack1ll1l11l1_opy_()
  global bstack11l11ll1_opy_
  global bstack11ll1lllll_opy_
  global bstack111llll1ll_opy_
  global bstack111llll1l1_opy_
  global bstack11l111lll_opy_
  global bstack1lll11lll1_opy_
  global bstack11ll1111_opy_
  global bstack1l111l1l11_opy_
  global bstack11l1l1lll1_opy_
  global bstack11llll11_opy_
  global bstack1111111l1_opy_
  bstack11ll1lllll_opy_ = len(CONFIG.get(bstack1ll11ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫർ"), []))
  if not bstack1l1llll1l1_opy_:
    if args[1] == bstack1ll11ll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩൽ") or args[1] == bstack1ll11ll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫൾ"):
      bstack1l1llll1l1_opy_ = bstack1ll11ll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫൿ")
      args = args[2:]
    elif args[1] == bstack1ll11ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ඀"):
      bstack1l1llll1l1_opy_ = bstack1ll11ll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬඁ")
      args = args[2:]
    elif args[1] == bstack1ll11ll_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ං"):
      bstack1l1llll1l1_opy_ = bstack1ll11ll_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧඃ")
      args = args[2:]
    elif args[1] == bstack1ll11ll_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ඄"):
      bstack1l1llll1l1_opy_ = bstack1ll11ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫඅ")
      args = args[2:]
    elif args[1] == bstack1ll11ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫආ"):
      bstack1l1llll1l1_opy_ = bstack1ll11ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬඇ")
      args = args[2:]
    elif args[1] == bstack1ll11ll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ඈ"):
      bstack1l1llll1l1_opy_ = bstack1ll11ll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧඉ")
      args = args[2:]
    else:
      if not bstack1ll11ll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫඊ") in CONFIG or str(CONFIG[bstack1ll11ll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬඋ")]).lower() in [bstack1ll11ll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪඌ"), bstack1ll11ll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬඍ")]:
        bstack1l1llll1l1_opy_ = bstack1ll11ll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬඎ")
        args = args[1:]
      elif str(CONFIG[bstack1ll11ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩඏ")]).lower() == bstack1ll11ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ඐ"):
        bstack1l1llll1l1_opy_ = bstack1ll11ll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧඑ")
        args = args[1:]
      elif str(CONFIG[bstack1ll11ll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬඒ")]).lower() == bstack1ll11ll_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩඓ"):
        bstack1l1llll1l1_opy_ = bstack1ll11ll_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪඔ")
        args = args[1:]
      elif str(CONFIG[bstack1ll11ll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨඕ")]).lower() == bstack1ll11ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ඖ"):
        bstack1l1llll1l1_opy_ = bstack1ll11ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ඗")
        args = args[1:]
      elif str(CONFIG[bstack1ll11ll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ඘")]).lower() == bstack1ll11ll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ඙"):
        bstack1l1llll1l1_opy_ = bstack1ll11ll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪක")
        args = args[1:]
      else:
        os.environ[bstack1ll11ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ඛ")] = bstack1l1llll1l1_opy_
        bstack1l1111111l_opy_(bstack1l11l1ll11_opy_)
  os.environ[bstack1ll11ll_opy_ (u"ࠬࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉ࠭ග")] = bstack1l1llll1l1_opy_
  bstack11lll11111_opy_ = bstack1l1llll1l1_opy_
  if cli.is_enabled(CONFIG):
    try:
      bstack1ll1lll1l1_opy_ = bstack11111l1l_opy_[bstack1ll11ll_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙࠳ࡂࡅࡆࠪඝ")] if bstack1l1llll1l1_opy_ == bstack1ll11ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧඞ") and bstack1llll1l11_opy_() else bstack1l1llll1l1_opy_
      bstack1111ll1l_opy_.invoke(bstack11l1lll1l_opy_.bstack1l1l111111_opy_, bstack1ll111l1ll_opy_(
        sdk_version=__version__,
        path_config=bstack1l1l1l1ll1_opy_(),
        path_project=os.getcwd(),
        test_framework=bstack1ll1lll1l1_opy_,
        frameworks=[bstack1ll1lll1l1_opy_],
        framework_versions={
          bstack1ll1lll1l1_opy_: bstack1l1111l1_opy_(bstack1ll11ll_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧඟ") if bstack1l1llll1l1_opy_ in [bstack1ll11ll_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨච"), bstack1ll11ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩඡ"), bstack1ll11ll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬජ")] else bstack1l1llll1l1_opy_)
        },
        bs_config=CONFIG
      ))
      if cli.config.get(bstack1ll11ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠢඣ"), None):
        CONFIG[bstack1ll11ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣඤ")] = cli.config.get(bstack1ll11ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤඥ"), None)
    except Exception as e:
      bstack1111ll1l_opy_.invoke(bstack11l1lll1l_opy_.bstack1ll1l1l1ll_opy_, e.__traceback__, 1)
    if bstack1l1lll1l1l_opy_:
      CONFIG[bstack1ll11ll_opy_ (u"ࠣࡣࡳࡴࠧඦ")] = cli.config[bstack1ll11ll_opy_ (u"ࠤࡤࡴࡵࠨට")]
      logger.info(bstack11l11111l_opy_.format(CONFIG[bstack1ll11ll_opy_ (u"ࠪࡥࡵࡶࠧඨ")]))
  else:
    bstack1111ll1l_opy_.clear()
  global bstack11l1111ll1_opy_
  global bstack11l1l111_opy_
  if bstack11lll1l11l_opy_:
    try:
      bstack1ll111l11_opy_ = datetime.datetime.now()
      os.environ[bstack1ll11ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ඩ")] = bstack1l1llll1l1_opy_
      bstack111l1ll1_opy_(bstack1l1111l1ll_opy_, CONFIG)
      cli.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽ࡷࡩࡱ࡟ࡵࡧࡶࡸࡤࡧࡴࡵࡧࡰࡴࡹ࡫ࡤࠣඪ"), datetime.datetime.now() - bstack1ll111l11_opy_)
    except Exception as e:
      logger.debug(bstack11l111llll_opy_.format(str(e)))
  global bstack1lll11ll11_opy_
  global bstack11l1111l1l_opy_
  global bstack111111ll1_opy_
  global bstack1lll1ll11l_opy_
  global bstack11l1llll1_opy_
  global bstack1l111l111_opy_
  global bstack11l1l1l1l_opy_
  global bstack1llllllll_opy_
  global bstack1l11l11111_opy_
  global bstack1lll111l1_opy_
  global bstack1lllll1l11_opy_
  global bstack1l1llllll1_opy_
  global bstack1lllllll11_opy_
  global bstack11l1ll11l1_opy_
  global bstack111l11l1l_opy_
  global bstack111lllll11_opy_
  global bstack1ll1ll1111_opy_
  global bstack11ll111lll_opy_
  global bstack1l11ll1111_opy_
  global bstack1lll111111_opy_
  global bstack1ll1llll1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1lll11ll11_opy_ = webdriver.Remote.__init__
    bstack11l1111l1l_opy_ = WebDriver.quit
    bstack1l1llllll1_opy_ = WebDriver.close
    bstack111l11l1l_opy_ = WebDriver.get
    bstack1ll1llll1_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack11l1111ll1_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack1ll1l1lll1_opy_
    bstack11l1l111_opy_ = bstack1ll1l1lll1_opy_()
  except Exception as e:
    pass
  try:
    global bstack1lll11ll1_opy_
    from QWeb.keywords import browser
    bstack1lll11ll1_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack11l11lll1l_opy_(CONFIG) and bstack111111ll_opy_():
    if bstack1l11111111_opy_() < version.parse(bstack111l1lll_opy_):
      logger.error(bstack1lll1l1l1l_opy_.format(bstack1l11111111_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack1ll11ll_opy_ (u"࠭࡟ࡨࡧࡷࡣࡵࡸ࡯ࡹࡻࡢࡹࡷࡲࠧණ")) and callable(getattr(RemoteConnection, bstack1ll11ll_opy_ (u"ࠧࡠࡩࡨࡸࡤࡶࡲࡰࡺࡼࡣࡺࡸ࡬ࠨඬ"))):
          RemoteConnection._get_proxy_url = bstack1l1lllllll_opy_
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          ClientConfig.get_proxy_url = bstack1l1lllllll_opy_
      except Exception as e:
        logger.error(bstack11l11llll1_opy_.format(str(e)))
  if not CONFIG.get(bstack1ll11ll_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪත"), False) and not bstack11lll1l11l_opy_:
    logger.info(bstack1lll111lll_opy_)
  if not cli.is_enabled(CONFIG):
    if bstack1ll11ll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ථ") in CONFIG and str(CONFIG[bstack1ll11ll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧද")]).lower() != bstack1ll11ll_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪධ"):
      bstack1lllll11_opy_()
    elif bstack1l1llll1l1_opy_ != bstack1ll11ll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬන") or (bstack1l1llll1l1_opy_ == bstack1ll11ll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭඲") and not bstack11lll1l11l_opy_):
      bstack1lllll1lll_opy_()
  if (bstack1l1llll1l1_opy_ in [bstack1ll11ll_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ඳ"), bstack1ll11ll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧප"), bstack1ll11ll_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪඵ")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1ll11ll111_opy_
        bstack1l111l111_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1l1ll1l1_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack11l1llll1_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1lll1l1l1_opy_ + str(e))
    except Exception as e:
      bstack1ll1l1l1_opy_(e, bstack1l1ll1l1_opy_)
    if bstack1l1llll1l1_opy_ != bstack1ll11ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫබ"):
      bstack1ll1lll11l_opy_()
    bstack111111ll1_opy_ = Output.start_test
    bstack1lll1ll11l_opy_ = Output.end_test
    bstack11l1l1l1l_opy_ = TestStatus.__init__
    bstack1l11l11111_opy_ = pabot._run
    bstack1lll111l1_opy_ = QueueItem.__init__
    bstack1lllll1l11_opy_ = pabot._create_command_for_execution
    bstack1l11ll1111_opy_ = pabot._report_results
  if bstack1l1llll1l1_opy_ == bstack1ll11ll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫභ"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll1l1l1_opy_(e, bstack111l111l_opy_)
    bstack1lllllll11_opy_ = Runner.run_hook
    bstack11l1ll11l1_opy_ = Step.run
  if bstack1l1llll1l1_opy_ == bstack1ll11ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬම"):
    try:
      from _pytest.config import Config
      bstack1ll1ll1111_opy_ = Config.getoption
      from _pytest import runner
      bstack11ll111lll_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack1llll1111_opy_)
    try:
      from pytest_bdd import reporting
      bstack1lll111111_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1ll11ll_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧඹ"))
  try:
    framework_name = bstack1ll11ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ය") if bstack1l1llll1l1_opy_ in [bstack1ll11ll_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧර"), bstack1ll11ll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ඼"), bstack1ll11ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫල")] else bstack1111ll1ll_opy_(bstack1l1llll1l1_opy_)
    bstack1111l1l1l_opy_ = {
      bstack1ll11ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࠬ඾"): bstack1ll11ll_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧ඿") if bstack1l1llll1l1_opy_ == bstack1ll11ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ව") and bstack1llll1l11_opy_() else framework_name,
      bstack1ll11ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫශ"): bstack1l1111l1_opy_(framework_name),
      bstack1ll11ll_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ෂ"): __version__,
      bstack1ll11ll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦࠪස"): bstack1l1llll1l1_opy_
    }
    if bstack1l1llll1l1_opy_ in bstack11111ll1l_opy_ + bstack1l1ll11l_opy_:
      if bstack1l1l11l1l1_opy_.bstack1ll1l11lll_opy_(CONFIG):
        if bstack1ll11ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪහ") in CONFIG:
          os.environ[bstack1ll11ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬළ")] = os.getenv(bstack1ll11ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ෆ"), json.dumps(CONFIG[bstack1ll11ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭෇")]))
          CONFIG[bstack1ll11ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ෈")].pop(bstack1ll11ll_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭෉"), None)
          CONFIG[bstack1ll11ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴ්ࠩ")].pop(bstack1ll11ll_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨ෋"), None)
        bstack1111l1l1l_opy_[bstack1ll11ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ෌")] = {
          bstack1ll11ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ෍"): bstack1ll11ll_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨ෎"),
          bstack1ll11ll_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨා"): str(bstack1l11111111_opy_())
        }
    if bstack1l1llll1l1_opy_ not in [bstack1ll11ll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩැ")] and not cli.is_running():
      bstack1ll11ll11_opy_, bstack1llll111ll_opy_ = bstack1l11ll1l_opy_.launch(CONFIG, bstack1111l1l1l_opy_)
      if bstack1llll111ll_opy_.get(bstack1ll11ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩෑ")) is not None and bstack1l1l11l1l1_opy_.bstack1llllll1ll_opy_(CONFIG) is None:
        value = bstack1llll111ll_opy_[bstack1ll11ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪි")].get(bstack1ll11ll_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬී"))
        if value is not None:
            CONFIG[bstack1ll11ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬු")] = value
        else:
          logger.debug(bstack1ll11ll_opy_ (u"ࠨࡎࡰࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡧࡥࡹࡧࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠦ෕"))
  except Exception as e:
    logger.debug(bstack11l11l111_opy_.format(bstack1ll11ll_opy_ (u"ࠧࡕࡧࡶࡸࡍࡻࡢࠨූ"), str(e)))
  if bstack1l1llll1l1_opy_ == bstack1ll11ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ෗"):
    bstack111llll1ll_opy_ = True
    if bstack11lll1l11l_opy_ and bstack11l1llll11_opy_:
      bstack1lll11lll1_opy_ = CONFIG.get(bstack1ll11ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ෘ"), {}).get(bstack1ll11ll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬෙ"))
      bstack1l1l111ll_opy_(bstack1l1111ll1_opy_)
    elif bstack11lll1l11l_opy_:
      bstack1lll11lll1_opy_ = CONFIG.get(bstack1ll11ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨේ"), {}).get(bstack1ll11ll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧෛ"))
      global bstack1lll1ll1l1_opy_
      try:
        if bstack1llll1ll1_opy_(bstack11lll1l11l_opy_[bstack1ll11ll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩො")]) and multiprocessing.current_process().name == bstack1ll11ll_opy_ (u"ࠧ࠱ࠩෝ"):
          bstack11lll1l11l_opy_[bstack1ll11ll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫෞ")].remove(bstack1ll11ll_opy_ (u"ࠩ࠰ࡱࠬෟ"))
          bstack11lll1l11l_opy_[bstack1ll11ll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭෠")].remove(bstack1ll11ll_opy_ (u"ࠫࡵࡪࡢࠨ෡"))
          bstack11lll1l11l_opy_[bstack1ll11ll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ෢")] = bstack11lll1l11l_opy_[bstack1ll11ll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ෣")][0]
          with open(bstack11lll1l11l_opy_[bstack1ll11ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ෤")], bstack1ll11ll_opy_ (u"ࠨࡴࠪ෥")) as f:
            bstack11lll11l11_opy_ = f.read()
          bstack111lllll1l_opy_ = bstack1ll11ll_opy_ (u"ࠤࠥࠦ࡫ࡸ࡯࡮ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡵࡧ࡯ࠥ࡯࡭ࡱࡱࡵࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥ࠼ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩ࠭ࢁࡽࠪ࠽ࠣࡪࡷࡵ࡭ࠡࡲࡧࡦࠥ࡯࡭ࡱࡱࡵࡸࠥࡖࡤࡣ࠽ࠣࡳ࡬ࡥࡤࡣࠢࡀࠤࡕࡪࡢ࠯ࡦࡲࡣࡧࡸࡥࡢ࡭࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡥࡧࡩࠤࡲࡵࡤࡠࡤࡵࡩࡦࡱࠨࡴࡧ࡯ࡪ࠱ࠦࡡࡳࡩ࠯ࠤࡹ࡫࡭ࡱࡱࡵࡥࡷࡿࠠ࠾ࠢ࠳࠭࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡹࡸࡹ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡤࡶ࡬ࠦ࠽ࠡࡵࡷࡶ࠭࡯࡮ࡵࠪࡤࡶ࡬࠯ࠫ࠲࠲ࠬࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡨࡼࡨ࡫ࡰࡵࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡧࡳࠡࡧ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡵࡧࡳࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡰࡩࡢࡨࡧ࠮ࡳࡦ࡮ࡩ࠰ࡦࡸࡧ࠭ࡶࡨࡱࡵࡵࡲࡢࡴࡼ࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡒࡧࡦ࠳ࡪ࡯ࡠࡤࠣࡁࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡕࡪࡢ࠯ࡦࡲࡣࡧࡸࡥࡢ࡭ࠣࡁࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡕࡪࡢࠩࠫ࠱ࡷࡪࡺ࡟ࡵࡴࡤࡧࡪ࠮ࠩ࡝ࡰࠥࠦࠧ෦").format(str(bstack11lll1l11l_opy_))
          bstack1ll11l11l1_opy_ = bstack111lllll1l_opy_ + bstack11lll11l11_opy_
          bstack11ll1111ll_opy_ = bstack11lll1l11l_opy_[bstack1ll11ll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭෧")] + bstack1ll11ll_opy_ (u"ࠫࡤࡨࡳࡵࡣࡦ࡯ࡤࡺࡥ࡮ࡲ࠱ࡴࡾ࠭෨")
          with open(bstack11ll1111ll_opy_, bstack1ll11ll_opy_ (u"ࠬࡽࠧ෩")):
            pass
          with open(bstack11ll1111ll_opy_, bstack1ll11ll_opy_ (u"ࠨࡷࠬࠤ෪")) as f:
            f.write(bstack1ll11l11l1_opy_)
          import subprocess
          bstack11l111ll1_opy_ = subprocess.run([bstack1ll11ll_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢ෫"), bstack11ll1111ll_opy_])
          if os.path.exists(bstack11ll1111ll_opy_):
            os.unlink(bstack11ll1111ll_opy_)
          os._exit(bstack11l111ll1_opy_.returncode)
        else:
          if bstack1llll1ll1_opy_(bstack11lll1l11l_opy_[bstack1ll11ll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ෬")]):
            bstack11lll1l11l_opy_[bstack1ll11ll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ෭")].remove(bstack1ll11ll_opy_ (u"ࠪ࠱ࡲ࠭෮"))
            bstack11lll1l11l_opy_[bstack1ll11ll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ෯")].remove(bstack1ll11ll_opy_ (u"ࠬࡶࡤࡣࠩ෰"))
            bstack11lll1l11l_opy_[bstack1ll11ll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ෱")] = bstack11lll1l11l_opy_[bstack1ll11ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪෲ")][0]
          bstack1l1l111ll_opy_(bstack1l1111ll1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack11lll1l11l_opy_[bstack1ll11ll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫෳ")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1ll11ll_opy_ (u"ࠩࡢࡣࡳࡧ࡭ࡦࡡࡢࠫ෴")] = bstack1ll11ll_opy_ (u"ࠪࡣࡤࡳࡡࡪࡰࡢࡣࠬ෵")
          mod_globals[bstack1ll11ll_opy_ (u"ࠫࡤࡥࡦࡪ࡮ࡨࡣࡤ࠭෶")] = os.path.abspath(bstack11lll1l11l_opy_[bstack1ll11ll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ෷")])
          exec(open(bstack11lll1l11l_opy_[bstack1ll11ll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ෸")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1ll11ll_opy_ (u"ࠧࡄࡣࡸ࡫࡭ࡺࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃࠧ෹").format(str(e)))
          for driver in bstack1lll1ll1l1_opy_:
            bstack1ll11lll1_opy_.append({
              bstack1ll11ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭෺"): bstack11lll1l11l_opy_[bstack1ll11ll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ෻")],
              bstack1ll11ll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ෼"): str(e),
              bstack1ll11ll_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ෽"): multiprocessing.current_process().name
            })
            bstack1l11lllll1_opy_(driver, bstack1ll11ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ෾"), bstack1ll11ll_opy_ (u"ࠨࡓࡦࡵࡶ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤ෿") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1lll1ll1l1_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1l1lll1l1l_opy_, CONFIG, logger)
      bstack1l1ll1l1l_opy_()
      bstack1l1l11l1l_opy_()
      percy.bstack1l1ll11l1_opy_()
      bstack11lll111ll_opy_ = {
        bstack1ll11ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ฀"): args[0],
        bstack1ll11ll_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨก"): CONFIG,
        bstack1ll11ll_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪข"): bstack11lll1lll_opy_,
        bstack1ll11ll_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬฃ"): bstack1l1lll1l1l_opy_
      }
      if bstack1ll11ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧค") in CONFIG:
        bstack1l11ll1l1l_opy_ = bstack1ll1l1l11_opy_(args, logger, CONFIG, bstack11l1ll11l_opy_, bstack11ll1lllll_opy_)
        bstack1l111l1l11_opy_ = bstack1l11ll1l1l_opy_.bstack1l111ll1l1_opy_(run_on_browserstack, bstack11lll111ll_opy_, bstack1llll1ll1_opy_(args))
      else:
        if bstack1llll1ll1_opy_(args):
          bstack11lll111ll_opy_[bstack1ll11ll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨฅ")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack11lll111ll_opy_,))
          test.start()
          test.join()
        else:
          bstack1l1l111ll_opy_(bstack1l1111ll1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1ll11ll_opy_ (u"࠭࡟ࡠࡰࡤࡱࡪࡥ࡟ࠨฆ")] = bstack1ll11ll_opy_ (u"ࠧࡠࡡࡰࡥ࡮ࡴ࡟ࡠࠩง")
          mod_globals[bstack1ll11ll_opy_ (u"ࠨࡡࡢࡪ࡮ࡲࡥࡠࡡࠪจ")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1l1llll1l1_opy_ == bstack1ll11ll_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨฉ") or bstack1l1llll1l1_opy_ == bstack1ll11ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩช"):
    percy.init(bstack1l1lll1l1l_opy_, CONFIG, logger)
    percy.bstack1l1ll11l1_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1ll1l1l1_opy_(e, bstack1l1ll1l1_opy_)
    bstack1l1ll1l1l_opy_()
    bstack1l1l111ll_opy_(bstack1ll1l111l1_opy_)
    if bstack11l1ll11l_opy_:
      bstack11l11l1ll_opy_(bstack1ll1l111l1_opy_, args)
      if bstack1ll11ll_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩซ") in args:
        i = args.index(bstack1ll11ll_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪฌ"))
        args.pop(i)
        args.pop(i)
      if bstack1ll11ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩญ") not in CONFIG:
        CONFIG[bstack1ll11ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪฎ")] = [{}]
        bstack11ll1lllll_opy_ = 1
      if bstack11l11ll1_opy_ == 0:
        bstack11l11ll1_opy_ = 1
      args.insert(0, str(bstack11l11ll1_opy_))
      args.insert(0, str(bstack1ll11ll_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ฏ")))
    if bstack1l11ll1l_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1ll1111l1l_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack11111l11_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack1ll11ll_opy_ (u"ࠤࡕࡓࡇࡕࡔࡠࡑࡓࡘࡎࡕࡎࡔࠤฐ"),
        ).parse_args(bstack1ll1111l1l_opy_)
        bstack11lll1ll1_opy_ = args.index(bstack1ll1111l1l_opy_[0]) if len(bstack1ll1111l1l_opy_) > 0 else len(args)
        args.insert(bstack11lll1ll1_opy_, str(bstack1ll11ll_opy_ (u"ࠪ࠱࠲ࡲࡩࡴࡶࡨࡲࡪࡸࠧฑ")))
        args.insert(bstack11lll1ll1_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll11ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡷࡵࡢࡰࡶࡢࡰ࡮ࡹࡴࡦࡰࡨࡶ࠳ࡶࡹࠨฒ"))))
        if bstack1ll1l111_opy_.bstack11l1lll11_opy_(CONFIG):
          args.insert(bstack11lll1ll1_opy_, str(bstack1ll11ll_opy_ (u"ࠬ࠳࠭࡭࡫ࡶࡸࡪࡴࡥࡳࠩณ")))
          args.insert(bstack11lll1ll1_opy_ + 1, str(bstack1ll11ll_opy_ (u"࠭ࡒࡦࡶࡵࡽࡋࡧࡩ࡭ࡧࡧ࠾ࢀࢃࠧด").format(bstack1ll1l111_opy_.bstack1ll11ll1l_opy_(CONFIG))))
        if bstack1l1l1llll1_opy_(os.environ.get(bstack1ll11ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠬต"))) and str(os.environ.get(bstack1ll11ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࡥࡔࡆࡕࡗࡗࠬถ"), bstack1ll11ll_opy_ (u"ࠩࡱࡹࡱࡲࠧท"))) != bstack1ll11ll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨธ"):
          for bstack11l1ll1ll1_opy_ in bstack11111l11_opy_:
            args.remove(bstack11l1ll1ll1_opy_)
          test_files = os.environ.get(bstack1ll11ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠨน")).split(bstack1ll11ll_opy_ (u"ࠬ࠲ࠧบ"))
          for bstack11111llll_opy_ in test_files:
            args.append(bstack11111llll_opy_)
      except Exception as e:
        logger.error(bstack1ll11ll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡦࡺࡴࡢࡥ࡫࡭ࡳ࡭ࠠ࡭࡫ࡶࡸࡪࡴࡥࡳࠢࡩࡳࡷࠦࡻࡾ࠰ࠣࡉࡷࡸ࡯ࡳࠢ࠰ࠤࢀࢃࠢป").format(bstack1l1llll11_opy_, e))
    pabot.main(args)
  elif bstack1l1llll1l1_opy_ == bstack1ll11ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨผ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1ll1l1l1_opy_(e, bstack1l1ll1l1_opy_)
    for a in args:
      if bstack1ll11ll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡑࡎࡄࡘࡋࡕࡒࡎࡋࡑࡈࡊ࡞ࠧฝ") in a:
        bstack11l111lll_opy_ = int(a.split(bstack1ll11ll_opy_ (u"ࠩ࠽ࠫพ"))[1])
      if bstack1ll11ll_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡇࡉࡋࡒࡏࡄࡃࡏࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧฟ") in a:
        bstack1lll11lll1_opy_ = str(a.split(bstack1ll11ll_opy_ (u"ࠫ࠿࠭ภ"))[1])
      if bstack1ll11ll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡒࡉࡂࡔࡊࡗࠬม") in a:
        bstack11ll1111_opy_ = str(a.split(bstack1ll11ll_opy_ (u"࠭࠺ࠨย"))[1])
    bstack1llll1l111_opy_ = None
    if bstack1ll11ll_opy_ (u"ࠧ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽ࠭ร") in args:
      i = args.index(bstack1ll11ll_opy_ (u"ࠨ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠧฤ"))
      args.pop(i)
      bstack1llll1l111_opy_ = args.pop(i)
    if bstack1llll1l111_opy_ is not None:
      global bstack1l1lll1l_opy_
      bstack1l1lll1l_opy_ = bstack1llll1l111_opy_
    bstack1l1l111ll_opy_(bstack1ll1l111l1_opy_)
    run_cli(args)
    if bstack1ll11ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠭ล") in multiprocessing.current_process().__dict__.keys():
      for bstack11l1ll1111_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1ll11lll1_opy_.append(bstack11l1ll1111_opy_)
  elif bstack1l1llll1l1_opy_ == bstack1ll11ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪฦ"):
    bstack111llllll1_opy_ = bstack1l11l11l1l_opy_(args, logger, CONFIG, bstack11l1ll11l_opy_)
    bstack111llllll1_opy_.bstack1ll11ll1ll_opy_()
    bstack1l1ll1l1l_opy_()
    bstack111llll1l1_opy_ = True
    bstack11llll11_opy_ = bstack111llllll1_opy_.bstack1l11lll1ll_opy_()
    bstack111llllll1_opy_.bstack1l1111l111_opy_()
    bstack111llllll1_opy_.bstack11lll111ll_opy_(bstack11l1111ll_opy_)
    bstack11llll1lll_opy_(bstack1l1llll1l1_opy_, CONFIG, bstack111llllll1_opy_.bstack11ll1ll1ll_opy_())
    bstack1llllll11_opy_ = bstack111llllll1_opy_.bstack1l111ll1l1_opy_(bstack1ll1ll1ll1_opy_, {
      bstack1ll11ll_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬว"): bstack11lll1lll_opy_,
      bstack1ll11ll_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧศ"): bstack1l1lll1l1l_opy_,
      bstack1ll11ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩษ"): bstack11l1ll11l_opy_
    })
    try:
      bstack1l1ll1ll1_opy_, bstack1l11l1l1_opy_ = map(list, zip(*bstack1llllll11_opy_))
      bstack11l1l1lll1_opy_ = bstack1l1ll1ll1_opy_[0]
      for status_code in bstack1l11l1l1_opy_:
        if status_code != 0:
          bstack1111111l1_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack1ll11ll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡦࡼࡥࠡࡧࡵࡶࡴࡸࡳࠡࡣࡱࡨࠥࡹࡴࡢࡶࡸࡷࠥࡩ࡯ࡥࡧ࠱ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠ࠻ࠢࡾࢁࠧส").format(str(e)))
  elif bstack1l1llll1l1_opy_ == bstack1ll11ll_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨห"):
    try:
      from behave.__main__ import main as bstack11l1l1ll11_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1ll1l1l1_opy_(e, bstack111l111l_opy_)
    bstack1l1ll1l1l_opy_()
    bstack111llll1l1_opy_ = True
    bstack1ll111lll_opy_ = 1
    if bstack1ll11ll_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩฬ") in CONFIG:
      bstack1ll111lll_opy_ = CONFIG[bstack1ll11ll_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪอ")]
    if bstack1ll11ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧฮ") in CONFIG:
      bstack1l11111lll_opy_ = int(bstack1ll111lll_opy_) * int(len(CONFIG[bstack1ll11ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨฯ")]))
    else:
      bstack1l11111lll_opy_ = int(bstack1ll111lll_opy_)
    config = Configuration(args)
    bstack11llll1l11_opy_ = config.paths
    if len(bstack11llll1l11_opy_) == 0:
      import glob
      pattern = bstack1ll11ll_opy_ (u"࠭ࠪࠫ࠱࠭࠲࡫࡫ࡡࡵࡷࡵࡩࠬะ")
      bstack1l1llll1_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1l1llll1_opy_)
      config = Configuration(args)
      bstack11llll1l11_opy_ = config.paths
    bstack11l1l1l11l_opy_ = [os.path.normpath(item) for item in bstack11llll1l11_opy_]
    bstack1l11l1ll1_opy_ = [os.path.normpath(item) for item in args]
    bstack1111lll1_opy_ = [item for item in bstack1l11l1ll1_opy_ if item not in bstack11l1l1l11l_opy_]
    import platform as pf
    if pf.system().lower() == bstack1ll11ll_opy_ (u"ࠧࡸ࡫ࡱࡨࡴࡽࡳࠨั"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack11l1l1l11l_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l11ll11l1_opy_)))
                    for bstack1l11ll11l1_opy_ in bstack11l1l1l11l_opy_]
    bstack11l111l1_opy_ = []
    for spec in bstack11l1l1l11l_opy_:
      bstack1ll1l1l1l_opy_ = []
      bstack1ll1l1l1l_opy_ += bstack1111lll1_opy_
      bstack1ll1l1l1l_opy_.append(spec)
      bstack11l111l1_opy_.append(bstack1ll1l1l1l_opy_)
    execution_items = []
    for bstack1ll1l1l1l_opy_ in bstack11l111l1_opy_:
      if bstack1ll11ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫา") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack1ll11ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬำ")]):
          item = {}
          item[bstack1ll11ll_opy_ (u"ࠪࡥࡷ࡭ࠧิ")] = bstack1ll11ll_opy_ (u"ࠫࠥ࠭ี").join(bstack1ll1l1l1l_opy_)
          item[bstack1ll11ll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫึ")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack1ll11ll_opy_ (u"࠭ࡡࡳࡩࠪื")] = bstack1ll11ll_opy_ (u"ุࠧࠡࠩ").join(bstack1ll1l1l1l_opy_)
        item[bstack1ll11ll_opy_ (u"ࠨ࡫ࡱࡨࡪࡾูࠧ")] = 0
        execution_items.append(item)
    bstack111l1l1l_opy_ = bstack1l1l11l11_opy_(execution_items, bstack1l11111lll_opy_)
    for execution_item in bstack111l1l1l_opy_:
      bstack1l111111_opy_ = []
      for item in execution_item:
        bstack1l111111_opy_.append(bstack111111111_opy_(name=str(item[bstack1ll11ll_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨฺ")]),
                                             target=bstack111l111ll_opy_,
                                             args=(item[bstack1ll11ll_opy_ (u"ࠪࡥࡷ࡭ࠧ฻")],)))
      for t in bstack1l111111_opy_:
        t.start()
      for t in bstack1l111111_opy_:
        t.join()
  else:
    bstack1l1111111l_opy_(bstack1l11l1ll11_opy_)
  if not bstack11lll1l11l_opy_:
    bstack1l1l11lll_opy_()
    if(bstack1l1llll1l1_opy_ in [bstack1ll11ll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ฼"), bstack1ll11ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ฽")]):
      bstack111ll11l1_opy_()
  bstack1lll1llll_opy_.bstack1lll1l111_opy_()
def browserstack_initialize(bstack1l11l11l1_opy_=None):
  logger.info(bstack1ll11ll_opy_ (u"࠭ࡒࡶࡰࡱ࡭ࡳ࡭ࠠࡔࡆࡎࠤࡼ࡯ࡴࡩࠢࡤࡶ࡬ࡹ࠺ࠡࠩ฾") + str(bstack1l11l11l1_opy_))
  run_on_browserstack(bstack1l11l11l1_opy_, None, True)
@measure(event_name=EVENTS.bstack1ll1l111ll_opy_, stage=STAGE.bstack11lll1ll1l_opy_, bstack11ll1l1l_opy_=bstack111l1l11_opy_)
def bstack1l1l11lll_opy_():
  global CONFIG
  global bstack11lll11111_opy_
  global bstack1111111l1_opy_
  global bstack11l1l1l11_opy_
  global bstack1l111111l1_opy_
  bstack111lll1ll_opy_.bstack1lllll11ll_opy_()
  if cli.is_running():
    bstack1111ll1l_opy_.invoke(bstack11l1lll1l_opy_.bstack1l111l1lll_opy_)
  else:
    bstack11l1l11l11_opy_ = bstack1ll1l111_opy_.bstack11l11lllll_opy_(config=CONFIG)
    bstack11l1l11l11_opy_.bstack111ll11ll_opy_(CONFIG)
  if bstack11lll11111_opy_ == bstack1ll11ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ฿"):
    if not cli.is_enabled(CONFIG):
      bstack1l11ll1l_opy_.stop()
  else:
    bstack1l11ll1l_opy_.stop()
  if not cli.is_enabled(CONFIG):
    bstack11lllllll1_opy_.bstack1ll1ll11l1_opy_()
  if bstack1ll11ll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬเ") in CONFIG and str(CONFIG[bstack1ll11ll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭แ")]).lower() != bstack1ll11ll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩโ"):
    hashed_id, bstack111l1l1l1_opy_ = bstack1l1ll111ll_opy_()
  else:
    hashed_id, bstack111l1l1l1_opy_ = get_build_link()
  bstack1lll1l11l_opy_(hashed_id)
  logger.info(bstack1ll11ll_opy_ (u"ࠫࡘࡊࡋࠡࡴࡸࡲࠥ࡫࡮ࡥࡧࡧࠤ࡫ࡵࡲࠡ࡫ࡧ࠾ࠬใ") + bstack1l111111l1_opy_.get_property(bstack1ll11ll_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪࠧไ"), bstack1ll11ll_opy_ (u"࠭ࠧๅ")) + bstack1ll11ll_opy_ (u"ࠧ࠭ࠢࡷࡩࡸࡺࡨࡶࡤࠣ࡭ࡩࡀࠠࠨๆ") + os.getenv(bstack1ll11ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭็"), bstack1ll11ll_opy_ (u"่ࠩࠪ")))
  if hashed_id is not None and bstack1l111ll11_opy_() != -1:
    sessions = bstack1lll1111l_opy_(hashed_id)
    bstack11lll1l1_opy_(sessions, bstack111l1l1l1_opy_)
  if bstack11lll11111_opy_ == bstack1ll11ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ้ࠪ") and bstack1111111l1_opy_ != 0:
    sys.exit(bstack1111111l1_opy_)
  if bstack11lll11111_opy_ == bstack1ll11ll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨ๊ࠫ") and bstack11l1l1l11_opy_ != 0:
    sys.exit(bstack11l1l1l11_opy_)
def bstack1lll1l11l_opy_(new_id):
    global bstack1l1lll1lll_opy_
    bstack1l1lll1lll_opy_ = new_id
def bstack1111ll1ll_opy_(bstack1lll1l11l1_opy_):
  if bstack1lll1l11l1_opy_:
    return bstack1lll1l11l1_opy_.capitalize()
  else:
    return bstack1ll11ll_opy_ (u"๋ࠬ࠭")
@measure(event_name=EVENTS.bstack1ll111ll11_opy_, stage=STAGE.bstack11lll1ll1l_opy_, bstack11ll1l1l_opy_=bstack111l1l11_opy_)
def bstack1l1ll11lll_opy_(bstack1lllllll1_opy_):
  if bstack1ll11ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ์") in bstack1lllllll1_opy_ and bstack1lllllll1_opy_[bstack1ll11ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬํ")] != bstack1ll11ll_opy_ (u"ࠨࠩ๎"):
    return bstack1lllllll1_opy_[bstack1ll11ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ๏")]
  else:
    bstack11ll1l1l_opy_ = bstack1ll11ll_opy_ (u"ࠥࠦ๐")
    if bstack1ll11ll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫ๑") in bstack1lllllll1_opy_ and bstack1lllllll1_opy_[bstack1ll11ll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬ๒")] != None:
      bstack11ll1l1l_opy_ += bstack1lllllll1_opy_[bstack1ll11ll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭๓")] + bstack1ll11ll_opy_ (u"ࠢ࠭ࠢࠥ๔")
      if bstack1lllllll1_opy_[bstack1ll11ll_opy_ (u"ࠨࡱࡶࠫ๕")] == bstack1ll11ll_opy_ (u"ࠤ࡬ࡳࡸࠨ๖"):
        bstack11ll1l1l_opy_ += bstack1ll11ll_opy_ (u"ࠥ࡭ࡔ࡙ࠠࠣ๗")
      bstack11ll1l1l_opy_ += (bstack1lllllll1_opy_[bstack1ll11ll_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ๘")] or bstack1ll11ll_opy_ (u"ࠬ࠭๙"))
      return bstack11ll1l1l_opy_
    else:
      bstack11ll1l1l_opy_ += bstack1111ll1ll_opy_(bstack1lllllll1_opy_[bstack1ll11ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ๚")]) + bstack1ll11ll_opy_ (u"ࠢࠡࠤ๛") + (
              bstack1lllllll1_opy_[bstack1ll11ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪ๜")] or bstack1ll11ll_opy_ (u"ࠩࠪ๝")) + bstack1ll11ll_opy_ (u"ࠥ࠰ࠥࠨ๞")
      if bstack1lllllll1_opy_[bstack1ll11ll_opy_ (u"ࠫࡴࡹࠧ๟")] == bstack1ll11ll_opy_ (u"ࠧ࡝ࡩ࡯ࡦࡲࡻࡸࠨ๠"):
        bstack11ll1l1l_opy_ += bstack1ll11ll_opy_ (u"ࠨࡗࡪࡰࠣࠦ๡")
      bstack11ll1l1l_opy_ += bstack1lllllll1_opy_[bstack1ll11ll_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫ๢")] or bstack1ll11ll_opy_ (u"ࠨࠩ๣")
      return bstack11ll1l1l_opy_
@measure(event_name=EVENTS.bstack1l1111ll1l_opy_, stage=STAGE.bstack11lll1ll1l_opy_, bstack11ll1l1l_opy_=bstack111l1l11_opy_)
def bstack1ll1lll11_opy_(bstack1lll11111l_opy_):
  if bstack1lll11111l_opy_ == bstack1ll11ll_opy_ (u"ࠤࡧࡳࡳ࡫ࠢ๤"):
    return bstack1ll11ll_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿࡭ࡲࡦࡧࡱ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧ࡭ࡲࡦࡧࡱࠦࡃࡉ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭๥")
  elif bstack1lll11111l_opy_ == bstack1ll11ll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ๦"):
    return bstack1ll11ll_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡳࡧࡧ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡸࡥࡥࠤࡁࡊࡦ࡯࡬ࡦࡦ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨ๧")
  elif bstack1lll11111l_opy_ == bstack1ll11ll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ๨"):
    return bstack1ll11ll_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡪࡶࡪ࡫࡮࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡪࡶࡪ࡫࡮ࠣࡀࡓࡥࡸࡹࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ๩")
  elif bstack1lll11111l_opy_ == bstack1ll11ll_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢ๪"):
    return bstack1ll11ll_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡷ࡫ࡤ࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡵࡩࡩࠨ࠾ࡆࡴࡵࡳࡷࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫ๫")
  elif bstack1lll11111l_opy_ == bstack1ll11ll_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࠦ๬"):
    return bstack1ll11ll_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࠣࡦࡧࡤ࠷࠷࠼࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࠥࡨࡩࡦ࠹࠲࠷ࠤࡁࡘ࡮ࡳࡥࡰࡷࡷࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩ๭")
  elif bstack1lll11111l_opy_ == bstack1ll11ll_opy_ (u"ࠧࡸࡵ࡯ࡰ࡬ࡲ࡬ࠨ๮"):
    return bstack1ll11ll_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡤ࡯ࡥࡨࡱ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡤ࡯ࡥࡨࡱࠢ࠿ࡔࡸࡲࡳ࡯࡮ࡨ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ๯")
  else:
    return bstack1ll11ll_opy_ (u"ࠧ࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡦࡱࡧࡣ࡬࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡦࡱࡧࡣ࡬ࠤࡁࠫ๰") + bstack1111ll1ll_opy_(
      bstack1lll11111l_opy_) + bstack1ll11ll_opy_ (u"ࠨ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ๱")
def bstack1l111ll11l_opy_(session):
  return bstack1ll11ll_opy_ (u"ࠩ࠿ࡸࡷࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡲࡰࡹࠥࡂࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠦࡳࡦࡵࡶ࡭ࡴࡴ࠭࡯ࡣࡰࡩࠧࡄ࠼ࡢࠢ࡫ࡶࡪ࡬࠽ࠣࡽࢀࠦࠥࡺࡡࡳࡩࡨࡸࡂࠨ࡟ࡣ࡮ࡤࡲࡰࠨ࠾ࡼࡿ࠿࠳ࡦࡄ࠼࠰ࡶࡧࡂࢀࢃࡻࡾ࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀ࠴ࡺࡲ࠿ࠩ๲").format(
    session[bstack1ll11ll_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥࡢࡹࡷࡲࠧ๳")], bstack1l1ll11lll_opy_(session), bstack1ll1lll11_opy_(session[bstack1ll11ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡷࡹࡧࡴࡶࡵࠪ๴")]),
    bstack1ll1lll11_opy_(session[bstack1ll11ll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ๵")]),
    bstack1111ll1ll_opy_(session[bstack1ll11ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ๶")] or session[bstack1ll11ll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ๷")] or bstack1ll11ll_opy_ (u"ࠨࠩ๸")) + bstack1ll11ll_opy_ (u"ࠤࠣࠦ๹") + (session[bstack1ll11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ๺")] or bstack1ll11ll_opy_ (u"ࠫࠬ๻")),
    session[bstack1ll11ll_opy_ (u"ࠬࡵࡳࠨ๼")] + bstack1ll11ll_opy_ (u"ࠨࠠࠣ๽") + session[bstack1ll11ll_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫ๾")], session[bstack1ll11ll_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪ๿")] or bstack1ll11ll_opy_ (u"ࠩࠪ຀"),
    session[bstack1ll11ll_opy_ (u"ࠪࡧࡷ࡫ࡡࡵࡧࡧࡣࡦࡺࠧກ")] if session[bstack1ll11ll_opy_ (u"ࠫࡨࡸࡥࡢࡶࡨࡨࡤࡧࡴࠨຂ")] else bstack1ll11ll_opy_ (u"ࠬ࠭຃"))
@measure(event_name=EVENTS.bstack1lll1l1ll1_opy_, stage=STAGE.bstack11lll1ll1l_opy_, bstack11ll1l1l_opy_=bstack111l1l11_opy_)
def bstack11lll1l1_opy_(sessions, bstack111l1l1l1_opy_):
  try:
    bstack1ll1llll11_opy_ = bstack1ll11ll_opy_ (u"ࠨࠢຄ")
    if not os.path.exists(bstack111ll111_opy_):
      os.mkdir(bstack111ll111_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll11ll_opy_ (u"ࠧࡢࡵࡶࡩࡹࡹ࠯ࡳࡧࡳࡳࡷࡺ࠮ࡩࡶࡰࡰࠬ຅")), bstack1ll11ll_opy_ (u"ࠨࡴࠪຆ")) as f:
      bstack1ll1llll11_opy_ = f.read()
    bstack1ll1llll11_opy_ = bstack1ll1llll11_opy_.replace(bstack1ll11ll_opy_ (u"ࠩࡾࠩࡗࡋࡓࡖࡎࡗࡗࡤࡉࡏࡖࡐࡗࠩࢂ࠭ງ"), str(len(sessions)))
    bstack1ll1llll11_opy_ = bstack1ll1llll11_opy_.replace(bstack1ll11ll_opy_ (u"ࠪࡿࠪࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠦࡿࠪຈ"), bstack111l1l1l1_opy_)
    bstack1ll1llll11_opy_ = bstack1ll1llll11_opy_.replace(bstack1ll11ll_opy_ (u"ࠫࢀࠫࡂࡖࡋࡏࡈࡤࡔࡁࡎࡇࠨࢁࠬຉ"),
                                              sessions[0].get(bstack1ll11ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣࡳࡧ࡭ࡦࠩຊ")) if sessions[0] else bstack1ll11ll_opy_ (u"࠭ࠧ຋"))
    with open(os.path.join(bstack111ll111_opy_, bstack1ll11ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡲࡦࡲࡲࡶࡹ࠴ࡨࡵ࡯࡯ࠫຌ")), bstack1ll11ll_opy_ (u"ࠨࡹࠪຍ")) as stream:
      stream.write(bstack1ll1llll11_opy_.split(bstack1ll11ll_opy_ (u"ࠩࡾࠩࡘࡋࡓࡔࡋࡒࡒࡘࡥࡄࡂࡖࡄࠩࢂ࠭ຎ"))[0])
      for session in sessions:
        stream.write(bstack1l111ll11l_opy_(session))
      stream.write(bstack1ll1llll11_opy_.split(bstack1ll11ll_opy_ (u"ࠪࡿ࡙ࠪࡅࡔࡕࡌࡓࡓ࡙࡟ࡅࡃࡗࡅࠪࢃࠧຏ"))[1])
    logger.info(bstack1ll11ll_opy_ (u"ࠫࡌ࡫࡮ࡦࡴࡤࡸࡪࡪࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡢࡶ࡫࡯ࡨࠥࡧࡲࡵ࡫ࡩࡥࡨࡺࡳࠡࡣࡷࠤࢀࢃࠧຐ").format(bstack111ll111_opy_));
  except Exception as e:
    logger.debug(bstack1lll11l1ll_opy_.format(str(e)))
def bstack1lll1111l_opy_(hashed_id):
  global CONFIG
  try:
    bstack1ll111l11_opy_ = datetime.datetime.now()
    host = bstack1ll11ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡱ࡫࠰ࡧࡱࡵࡵࡥ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬຑ") if bstack1ll11ll_opy_ (u"࠭ࡡࡱࡲࠪຒ") in CONFIG else bstack1ll11ll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨຓ")
    user = CONFIG[bstack1ll11ll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪດ")]
    key = CONFIG[bstack1ll11ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬຕ")]
    bstack1ll1l1l11l_opy_ = bstack1ll11ll_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩຖ") if bstack1ll11ll_opy_ (u"ࠫࡦࡶࡰࠨທ") in CONFIG else (bstack1ll11ll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩຘ") if CONFIG.get(bstack1ll11ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪນ")) else bstack1ll11ll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩບ"))
    host = bstack1111lllll_opy_(cli.config, [bstack1ll11ll_opy_ (u"ࠣࡣࡳ࡭ࡸࠨປ"), bstack1ll11ll_opy_ (u"ࠤࡤࡴࡵࡇࡵࡵࡱࡰࡥࡹ࡫ࠢຜ"), bstack1ll11ll_opy_ (u"ࠥࡥࡵ࡯ࠢຝ")], host) if bstack1ll11ll_opy_ (u"ࠫࡦࡶࡰࠨພ") in CONFIG else bstack1111lllll_opy_(cli.config, [bstack1ll11ll_opy_ (u"ࠧࡧࡰࡪࡵࠥຟ"), bstack1ll11ll_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥࠣຠ"), bstack1ll11ll_opy_ (u"ࠢࡢࡲ࡬ࠦມ")], host)
    url = bstack1ll11ll_opy_ (u"ࠨࡽࢀ࠳ࢀࢃ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡷࡪࡹࡳࡪࡱࡱࡷ࠳ࡰࡳࡰࡰࠪຢ").format(host, bstack1ll1l1l11l_opy_, hashed_id)
    headers = {
      bstack1ll11ll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨຣ"): bstack1ll11ll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭຤"),
    }
    proxies = bstack1llll11lll_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies, auth=(user, key))
    if response.json():
      cli.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼ࡪࡩࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࡠ࡮࡬ࡷࡹࠨລ"), datetime.datetime.now() - bstack1ll111l11_opy_)
      return list(map(lambda session: session[bstack1ll11ll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡩࡸࡹࡩࡰࡰࠪ຦")], response.json()))
  except Exception as e:
    logger.debug(bstack1l11lll111_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack1lll11l11_opy_, stage=STAGE.bstack11lll1ll1l_opy_, bstack11ll1l1l_opy_=bstack111l1l11_opy_)
def get_build_link():
  global CONFIG
  global bstack1l1lll1lll_opy_
  try:
    if bstack1ll11ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩວ") in CONFIG:
      bstack1ll111l11_opy_ = datetime.datetime.now()
      host = bstack1ll11ll_opy_ (u"ࠧࡢࡲ࡬࠱ࡨࡲ࡯ࡶࡦࠪຨ") if bstack1ll11ll_opy_ (u"ࠨࡣࡳࡴࠬຩ") in CONFIG else bstack1ll11ll_opy_ (u"ࠩࡤࡴ࡮࠭ສ")
      user = CONFIG[bstack1ll11ll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬຫ")]
      key = CONFIG[bstack1ll11ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧຬ")]
      bstack1ll1l1l11l_opy_ = bstack1ll11ll_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫອ") if bstack1ll11ll_opy_ (u"࠭ࡡࡱࡲࠪຮ") in CONFIG else bstack1ll11ll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩຯ")
      url = bstack1ll11ll_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡾࢁ࠿ࢁࡽࡁࡽࢀ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡼࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠱࡮ࡸࡵ࡮ࠨະ").format(user, key, host, bstack1ll1l1l11l_opy_)
      if cli.is_enabled(CONFIG):
        bstack111l1l1l1_opy_, hashed_id = cli.bstack1ll1ll11ll_opy_()
        logger.info(bstack1ll11l1l_opy_.format(bstack111l1l1l1_opy_))
        return [hashed_id, bstack111l1l1l1_opy_]
      else:
        headers = {
          bstack1ll11ll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨັ"): bstack1ll11ll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭າ"),
        }
        if bstack1ll11ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ຳ") in CONFIG:
          params = {bstack1ll11ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪິ"): CONFIG[bstack1ll11ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩີ")], bstack1ll11ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪຶ"): CONFIG[bstack1ll11ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪື")]}
        else:
          params = {bstack1ll11ll_opy_ (u"ࠩࡱࡥࡲ࡫ຸࠧ"): CONFIG[bstack1ll11ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪູ࠭")]}
        proxies = bstack1llll11lll_opy_(CONFIG, url)
        response = requests.get(url, params=params, headers=headers, proxies=proxies)
        if response.json():
          bstack1l1l1l1l11_opy_ = response.json()[0][bstack1ll11ll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡤࡸ࡭ࡱࡪ຺ࠧ")]
          if bstack1l1l1l1l11_opy_:
            bstack111l1l1l1_opy_ = bstack1l1l1l1l11_opy_[bstack1ll11ll_opy_ (u"ࠬࡶࡵࡣ࡮࡬ࡧࡤࡻࡲ࡭ࠩົ")].split(bstack1ll11ll_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨ࠳ࡢࡶ࡫࡯ࡨࠬຼ"))[0] + bstack1ll11ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡹ࠯ࠨຽ") + bstack1l1l1l1l11_opy_[
              bstack1ll11ll_opy_ (u"ࠨࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ຾")]
            logger.info(bstack1ll11l1l_opy_.format(bstack111l1l1l1_opy_))
            bstack1l1lll1lll_opy_ = bstack1l1l1l1l11_opy_[bstack1ll11ll_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ຿")]
            bstack11lll1ll_opy_ = CONFIG[bstack1ll11ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ເ")]
            if bstack1ll11ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ແ") in CONFIG:
              bstack11lll1ll_opy_ += bstack1ll11ll_opy_ (u"ࠬࠦࠧໂ") + CONFIG[bstack1ll11ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨໃ")]
            if bstack11lll1ll_opy_ != bstack1l1l1l1l11_opy_[bstack1ll11ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬໄ")]:
              logger.debug(bstack1l11l1l11l_opy_.format(bstack1l1l1l1l11_opy_[bstack1ll11ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭໅")], bstack11lll1ll_opy_))
            cli.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺ࡨࡧࡷࡣࡧࡻࡩ࡭ࡦࡢࡰ࡮ࡴ࡫ࠣໆ"), datetime.datetime.now() - bstack1ll111l11_opy_)
            return [bstack1l1l1l1l11_opy_[bstack1ll11ll_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭໇")], bstack111l1l1l1_opy_]
    else:
      logger.warn(bstack1l111l11l_opy_)
  except Exception as e:
    logger.debug(bstack1l11111ll_opy_.format(str(e)))
  return [None, None]
def bstack1ll1ll1l1l_opy_(url, bstack1lll1ll111_opy_=False):
  global CONFIG
  global bstack111l11l1_opy_
  if not bstack111l11l1_opy_:
    hostname = bstack1111111l_opy_(url)
    is_private = bstack1l1l1l11l_opy_(hostname)
    if (bstack1ll11ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ່") in CONFIG and not bstack1l1l1llll1_opy_(CONFIG[bstack1ll11ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭້ࠩ")])) and (is_private or bstack1lll1ll111_opy_):
      bstack111l11l1_opy_ = hostname
def bstack1111111l_opy_(url):
  return urlparse(url).hostname
def bstack1l1l1l11l_opy_(hostname):
  for bstack1ll111l1l_opy_ in bstack1l1lllll_opy_:
    regex = re.compile(bstack1ll111l1l_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack11llllll1l_opy_(bstack111ll1lll_opy_):
  return True if bstack111ll1lll_opy_ in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack1l11lll11_opy_, stage=STAGE.bstack11lll1ll1l_opy_, bstack11ll1l1l_opy_=bstack111l1l11_opy_)
def getAccessibilityResults(driver):
  global CONFIG
  global bstack11l111lll_opy_
  bstack1ll11111_opy_ = not (bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶ໊ࠪ"), None) and bstack1111l1l11_opy_(
          threading.current_thread(), bstack1ll11ll_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ໋࠭"), None))
  bstack11l11l11l_opy_ = getattr(driver, bstack1ll11ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ໌"), None) != True
  bstack1111l111_opy_ = bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩໍ"), None) and bstack1111l1l11_opy_(
          threading.current_thread(), bstack1ll11ll_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ໎"), None)
  if bstack1111l111_opy_:
    if not bstack1l111l1ll_opy_():
      logger.warning(bstack1ll11ll_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡶࡰࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡄࡴࡵࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹ࠮ࠣ໏"))
      return {}
    logger.debug(bstack1ll11ll_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡴࡨࡷࡺࡲࡴࡴࠩ໐"))
    logger.debug(perform_scan(driver, driver_command=bstack1ll11ll_opy_ (u"࠭ࡥࡹࡧࡦࡹࡹ࡫ࡓࡤࡴ࡬ࡴࡹ࠭໑")))
    results = bstack1llll11111_opy_(bstack1ll11ll_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡳࠣ໒"))
    if results is not None and results.get(bstack1ll11ll_opy_ (u"ࠣ࡫ࡶࡷࡺ࡫ࡳࠣ໓")) is not None:
        return results[bstack1ll11ll_opy_ (u"ࠤ࡬ࡷࡸࡻࡥࡴࠤ໔")]
    logger.error(bstack1ll11ll_opy_ (u"ࠥࡒࡴࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡒࡦࡵࡸࡰࡹࡹࠠࡸࡧࡵࡩࠥ࡬࡯ࡶࡰࡧ࠲ࠧ໕"))
    return []
  if not bstack1l1l11l1l1_opy_.bstack1l1l1lll1l_opy_(CONFIG, bstack11l111lll_opy_) or (bstack11l11l11l_opy_ and bstack1ll11111_opy_):
    logger.warning(bstack1ll11ll_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡪࡺࡲࡪࡧࡹࡩࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸ࠴ࠢ໖"))
    return {}
  try:
    logger.debug(bstack1ll11ll_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡴࡨࡷࡺࡲࡴࡴࠩ໗"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack1llll111_opy_.bstack1l11l111_opy_)
    return results
  except Exception:
    logger.error(bstack1ll11ll_opy_ (u"ࠨࡎࡰࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡻࡪࡸࡥࠡࡨࡲࡹࡳࡪ࠮ࠣ໘"))
    return {}
@measure(event_name=EVENTS.bstack11111ll1_opy_, stage=STAGE.bstack11lll1ll1l_opy_, bstack11ll1l1l_opy_=bstack111l1l11_opy_)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack11l111lll_opy_
  bstack1ll11111_opy_ = not (bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ໙"), None) and bstack1111l1l11_opy_(
          threading.current_thread(), bstack1ll11ll_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ໚"), None))
  bstack11l11l11l_opy_ = getattr(driver, bstack1ll11ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩ໛"), None) != True
  bstack1111l111_opy_ = bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪໜ"), None) and bstack1111l1l11_opy_(
          threading.current_thread(), bstack1ll11ll_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ໝ"), None)
  if bstack1111l111_opy_:
    if not bstack1l111l1ll_opy_():
      logger.warning(bstack1ll11ll_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡰࡱࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡅࡵࡶࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡵࡸࡱࡲࡧࡲࡺ࠰ࠥໞ"))
      return {}
    logger.debug(bstack1ll11ll_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡷࡺࡳ࡭ࡢࡴࡼࠫໟ"))
    logger.debug(perform_scan(driver, driver_command=bstack1ll11ll_opy_ (u"ࠧࡦࡺࡨࡧࡺࡺࡥࡔࡥࡵ࡭ࡵࡺࠧ໠")))
    results = bstack1llll11111_opy_(bstack1ll11ll_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࡔࡷࡰࡱࡦࡸࡹࠣ໡"))
    if results is not None and results.get(bstack1ll11ll_opy_ (u"ࠤࡶࡹࡲࡳࡡࡳࡻࠥ໢")) is not None:
        return results[bstack1ll11ll_opy_ (u"ࠥࡷࡺࡳ࡭ࡢࡴࡼࠦ໣")]
    logger.error(bstack1ll11ll_opy_ (u"ࠦࡓࡵࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡓࡧࡶࡹࡱࡺࡳࠡࡕࡸࡱࡲࡧࡲࡺࠢࡺࡥࡸࠦࡦࡰࡷࡱࡨ࠳ࠨ໤"))
    return {}
  if not bstack1l1l11l1l1_opy_.bstack1l1l1lll1l_opy_(CONFIG, bstack11l111lll_opy_) or (bstack11l11l11l_opy_ and bstack1ll11111_opy_):
    logger.warning(bstack1ll11ll_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡴࡷࡰࡱࡦࡸࡹ࠯ࠤ໥"))
    return {}
  try:
    logger.debug(bstack1ll11ll_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡷࡺࡳ࡭ࡢࡴࡼࠫ໦"))
    logger.debug(perform_scan(driver))
    bstack1ll111111_opy_ = driver.execute_async_script(bstack1llll111_opy_.bstack1lll11l1_opy_)
    return bstack1ll111111_opy_
  except Exception:
    logger.error(bstack1ll11ll_opy_ (u"ࠢࡏࡱࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡺࡳ࡭ࡢࡴࡼࠤࡼࡧࡳࠡࡨࡲࡹࡳࡪ࠮ࠣ໧"))
    return {}
def bstack1l111l1ll_opy_():
  global CONFIG
  global bstack11l111lll_opy_
  bstack1ll1ll1l1_opy_ = bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ໨"), None) and bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ໩"), None)
  if not bstack1l1l11l1l1_opy_.bstack1l1l1lll1l_opy_(CONFIG, bstack11l111lll_opy_) or not bstack1ll1ll1l1_opy_:
        logger.warning(bstack1ll11ll_opy_ (u"ࠥࡒࡴࡺࠠࡢࡰࠣࡅࡵࡶࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࠡࡴࡨࡷࡺࡲࡴࡴ࠰ࠥ໪"))
        return False
  return True
def bstack1llll11111_opy_(bstack111l1l1ll_opy_):
    bstack1lllllllll_opy_ = bstack1l11ll1l_opy_.current_test_uuid() if bstack1l11ll1l_opy_.current_test_uuid() else bstack11lllllll1_opy_.current_hook_uuid()
    with ThreadPoolExecutor() as executor:
        future = executor.submit(bstack11ll11lll1_opy_(bstack1lllllllll_opy_, bstack111l1l1ll_opy_))
        try:
            return future.result(timeout=bstack1111ll1l1_opy_)
        except TimeoutError:
            logger.error(bstack1ll11ll_opy_ (u"࡙ࠦ࡯࡭ࡦࡱࡸࡸࠥࡧࡦࡵࡧࡵࠤࢀࢃࡳࠡࡹ࡫࡭ࡱ࡫ࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡕࡩࡸࡻ࡬ࡵࡵࠥ໫").format(bstack1111ll1l1_opy_))
        except Exception as ex:
            logger.debug(bstack1ll11ll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡷ࡫ࡴࡳ࡫ࡨࡺ࡮ࡴࡧࠡࡃࡳࡴࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡾࢁ࠳ࠦࡅࡳࡴࡲࡶࠥ࠳ࠠࡼࡿࠥ໬").format(bstack111l1l1ll_opy_, str(ex)))
    return {}
@measure(event_name=EVENTS.bstack11ll111l11_opy_, stage=STAGE.bstack11lll1ll1l_opy_, bstack11ll1l1l_opy_=bstack111l1l11_opy_)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack11l111lll_opy_
  bstack1ll11111_opy_ = not (bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ໭"), None) and bstack1111l1l11_opy_(
          threading.current_thread(), bstack1ll11ll_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭໮"), None))
  bstack1lll1l111l_opy_ = not (bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ໯"), None) and bstack1111l1l11_opy_(
          threading.current_thread(), bstack1ll11ll_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ໰"), None))
  bstack11l11l11l_opy_ = getattr(driver, bstack1ll11ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪ໱"), None) != True
  if not bstack1l1l11l1l1_opy_.bstack1l1l1lll1l_opy_(CONFIG, bstack11l111lll_opy_) or (bstack11l11l11l_opy_ and bstack1ll11111_opy_ and bstack1lll1l111l_opy_):
    logger.warning(bstack1ll11ll_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡺࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡥࡤࡲ࠳ࠨ໲"))
    return {}
  try:
    bstack1l1ll11111_opy_ = bstack1ll11ll_opy_ (u"ࠬࡧࡰࡱࠩ໳") in CONFIG and CONFIG.get(bstack1ll11ll_opy_ (u"࠭ࡡࡱࡲࠪ໴"), bstack1ll11ll_opy_ (u"ࠧࠨ໵"))
    session_id = getattr(driver, bstack1ll11ll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠬ໶"), None)
    if not session_id:
      logger.warning(bstack1ll11ll_opy_ (u"ࠤࡑࡳࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡉࡅࠢࡩࡳࡺࡴࡤࠡࡨࡲࡶࠥࡪࡲࡪࡸࡨࡶࠧ໷"))
      return {bstack1ll11ll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤ໸"): bstack1ll11ll_opy_ (u"ࠦࡓࡵࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡋࡇࠤ࡫ࡵࡵ࡯ࡦࠥ໹")}
    if bstack1l1ll11111_opy_:
      try:
        bstack111ll11l_opy_ = {
              bstack1ll11ll_opy_ (u"ࠬࡺࡨࡋࡹࡷࡘࡴࡱࡥ࡯ࠩ໺"): os.environ.get(bstack1ll11ll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ໻"), os.environ.get(bstack1ll11ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ໼"), bstack1ll11ll_opy_ (u"ࠨࠩ໽"))),
              bstack1ll11ll_opy_ (u"ࠩࡷ࡬࡙࡫ࡳࡵࡔࡸࡲ࡚ࡻࡩࡥࠩ໾"): bstack1l11ll1l_opy_.current_test_uuid() if bstack1l11ll1l_opy_.current_test_uuid() else bstack11lllllll1_opy_.current_hook_uuid(),
              bstack1ll11ll_opy_ (u"ࠪࡥࡺࡺࡨࡉࡧࡤࡨࡪࡸࠧ໿"): os.environ.get(bstack1ll11ll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩༀ")),
              bstack1ll11ll_opy_ (u"ࠬࡹࡣࡢࡰࡗ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ༁"): str(int(datetime.datetime.now().timestamp() * 1000)),
              bstack1ll11ll_opy_ (u"࠭ࡴࡩࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ༂"): os.environ.get(bstack1ll11ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ༃"), bstack1ll11ll_opy_ (u"ࠨࠩ༄")),
              bstack1ll11ll_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࠩ༅"): kwargs.get(bstack1ll11ll_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࡢࡧࡴࡳ࡭ࡢࡰࡧࠫ༆"), None) or bstack1ll11ll_opy_ (u"ࠫࠬ༇")
          }
        if not hasattr(thread_local, bstack1ll11ll_opy_ (u"ࠬࡨࡡࡴࡧࡢࡥࡵࡶ࡟ࡢ࠳࠴ࡽࡤࡹࡣࡳ࡫ࡳࡸࠬ༈")):
            scripts = {bstack1ll11ll_opy_ (u"࠭ࡳࡤࡣࡱࠫ༉"): bstack1llll111_opy_.perform_scan}
            thread_local.base_app_a11y_script = scripts
        bstack11l1llllll_opy_ = copy.deepcopy(thread_local.base_app_a11y_script)
        bstack11l1llllll_opy_[bstack1ll11ll_opy_ (u"ࠧࡴࡥࡤࡲࠬ༊")] = bstack11l1llllll_opy_[bstack1ll11ll_opy_ (u"ࠨࡵࡦࡥࡳ࠭་")] % json.dumps(bstack111ll11l_opy_)
        bstack1llll111_opy_.bstack1l111l11_opy_(bstack11l1llllll_opy_)
        bstack1llll111_opy_.store()
        bstack1l1l1ll1_opy_ = driver.execute_script(bstack1llll111_opy_.perform_scan)
      except Exception as bstack11ll11l111_opy_:
        logger.info(bstack1ll11ll_opy_ (u"ࠤࡄࡴࡵ࡯ࡵ࡮ࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡧࡦࡴࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࠤ༌") + str(bstack11ll11l111_opy_))
        bstack1l1l1ll1_opy_ = {bstack1ll11ll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤ།"): str(bstack11ll11l111_opy_)}
    else:
      bstack1l1l1ll1_opy_ = driver.execute_async_script(bstack1llll111_opy_.perform_scan, {bstack1ll11ll_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࠫ༎"): kwargs.get(bstack1ll11ll_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࡤࡩ࡯࡮࡯ࡤࡲࡩ࠭༏"), None) or bstack1ll11ll_opy_ (u"࠭ࠧ༐")})
    return bstack1l1l1ll1_opy_
  except Exception as err:
    logger.error(bstack1ll11ll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡶࡺࡴࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡥࡤࡲ࠳ࠦࡻࡾࠤ༑").format(str(err)))
    return {}