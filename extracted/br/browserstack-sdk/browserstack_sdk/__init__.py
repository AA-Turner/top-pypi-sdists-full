# coding: UTF-8
import sys
bstack1ll11l1_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack11lll_opy_ = 7
def bstack1l11l11_opy_ (bstack1llll11_opy_):
    global bstack11ll1l1_opy_
    bstack111l111_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11lll11_opy_ = bstack1llll11_opy_ [:-1]
    bstack1ll11_opy_ = bstack111l111_opy_ % len (bstack11lll11_opy_)
    bstack1l1l_opy_ = bstack11lll11_opy_ [:bstack1ll11_opy_] + bstack11lll11_opy_ [bstack1ll11_opy_:]
    if bstack1ll11l1_opy_:
        bstack11l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    else:
        bstack11l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    return eval (bstack11l1l1_opy_)
import atexit
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
from browserstack_sdk.bstack1l11111ll1_opy_ import bstack1llll11l1_opy_
from browserstack_sdk.bstack11lll1ll1l_opy_ import *
import time
import requests
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.measure import measure
def bstack11l111l1ll_opy_():
  global CONFIG
  headers = {
        bstack1l11l11_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack1l11l11_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1lll1lll1_opy_(CONFIG, bstack1111lll1l_opy_)
  try:
    response = requests.get(bstack1111lll1l_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack11l1l1ll1_opy_ = response.json()[bstack1l11l11_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack11l1l1l1l1_opy_.format(response.json()))
      return bstack11l1l1ll1_opy_
    else:
      logger.debug(bstack1ll1llll1l_opy_.format(bstack1l11l11_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack1ll1llll1l_opy_.format(e))
def bstack1l11ll11l_opy_(hub_url):
  global CONFIG
  url = bstack1l11l11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack1l11l11_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack1l11l11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack1l11l11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1lll1lll1_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1ll1llllll_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack11lllll1l_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack1l1ll1l1ll_opy_, stage=STAGE.bstack1lll11l1_opy_)
def bstack1ll1lllll_opy_():
  try:
    global bstack11l1ll111_opy_
    bstack11l1l1ll1_opy_ = bstack11l111l1ll_opy_()
    bstack11ll11ll_opy_ = []
    results = []
    for bstack1l1l11111_opy_ in bstack11l1l1ll1_opy_:
      bstack11ll11ll_opy_.append(bstack111lllll1_opy_(target=bstack1l11ll11l_opy_,args=(bstack1l1l11111_opy_,)))
    for t in bstack11ll11ll_opy_:
      t.start()
    for t in bstack11ll11ll_opy_:
      results.append(t.join())
    bstack11111lll_opy_ = {}
    for item in results:
      hub_url = item[bstack1l11l11_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack1l11l11_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack11111lll_opy_[hub_url] = latency
    bstack1llll11lll_opy_ = min(bstack11111lll_opy_, key= lambda x: bstack11111lll_opy_[x])
    bstack11l1ll111_opy_ = bstack1llll11lll_opy_
    logger.debug(bstack1ll11l111l_opy_.format(bstack1llll11lll_opy_))
  except Exception as e:
    logger.debug(bstack1l111111l_opy_.format(e))
from browserstack_sdk.bstack1l1lllll11_opy_ import *
from browserstack_sdk.bstack1llll1l11_opy_ import *
from browserstack_sdk.bstack1ll111lll_opy_ import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.bstack1l1ll11lll_opy_ import get_logger
from bstack_utils.measure import measure
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack1l1l111l1_opy_, stage=STAGE.bstack1lll11l1_opy_)
def bstack1lll111l1_opy_():
    global bstack11l1ll111_opy_
    try:
        bstack11l11111l1_opy_ = bstack1l1ll1l1l_opy_()
        bstack1l1111ll1l_opy_(bstack11l11111l1_opy_)
        hub_url = bstack11l11111l1_opy_.get(bstack1l11l11_opy_ (u"ࠨࡵࡳ࡮ࠥࢀ"), bstack1l11l11_opy_ (u"ࠢࠣࢁ"))
        if hub_url.endswith(bstack1l11l11_opy_ (u"ࠨ࠱ࡺࡨ࠴࡮ࡵࡣࠩࢂ")):
            hub_url = hub_url.rsplit(bstack1l11l11_opy_ (u"ࠩ࠲ࡻࡩ࠵ࡨࡶࡤࠪࢃ"), 1)[0]
        if hub_url.startswith(bstack1l11l11_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫࢄ")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack1l11l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࠭ࢅ")):
            hub_url = hub_url[8:]
        bstack11l1ll111_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack1l1ll1l1l_opy_():
    global CONFIG
    bstack1l1l111ll1_opy_ = CONFIG.get(bstack1l11l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢆ"), {}).get(bstack1l11l11_opy_ (u"࠭ࡧࡳ࡫ࡧࡒࡦࡳࡥࠨࢇ"), bstack1l11l11_opy_ (u"ࠧࡏࡑࡢࡋࡗࡏࡄࡠࡐࡄࡑࡊࡥࡐࡂࡕࡖࡉࡉ࠭࢈"))
    if not isinstance(bstack1l1l111ll1_opy_, str):
        raise ValueError(bstack1l11l11_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡈࡴ࡬ࡨࠥࡴࡡ࡮ࡧࠣࡱࡺࡹࡴࠡࡤࡨࠤࡦࠦࡶࡢ࡮࡬ࡨࠥࡹࡴࡳ࡫ࡱ࡫ࠧࢉ"))
    try:
        bstack11l11111l1_opy_ = bstack11llll1lll_opy_(bstack1l1l111ll1_opy_)
        return bstack11l11111l1_opy_
    except Exception as e:
        logger.error(bstack1l11l11_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣࢊ").format(str(e)))
        return {}
def bstack11llll1lll_opy_(bstack1l1l111ll1_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack1l11l11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࢋ")] or not CONFIG[bstack1l11l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧࢌ")]:
            raise ValueError(bstack1l11l11_opy_ (u"ࠧࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠠࡰࡴࠣࡥࡨࡩࡥࡴࡵࠣ࡯ࡪࡿࠢࢍ"))
        url = bstack1lll11111l_opy_ + bstack1l1l111ll1_opy_
        auth = (CONFIG[bstack1l11l11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨࢎ")], CONFIG[bstack1l11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ࢏")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack1l1l11lll1_opy_ = json.loads(response.text)
            return bstack1l1l11lll1_opy_
    except ValueError as ve:
        logger.error(bstack1l11l11_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣ࢐").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack1l11l11_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥ࡭ࡲࡪࡦࠣࡨࡪࡺࡡࡪ࡮ࡶࠤ࠿ࠦࡻࡾࠤ࢑").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack1l1111ll1l_opy_(bstack1lll1l1lll_opy_):
    global CONFIG
    if bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ࢒") not in CONFIG or str(CONFIG[bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ࢓")]).lower() == bstack1l11l11_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ࢔"):
        CONFIG[bstack1l11l11_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬ࢕")] = False
    elif bstack1l11l11_opy_ (u"ࠧࡪࡵࡗࡶ࡮ࡧ࡬ࡈࡴ࡬ࡨࠬ࢖") in bstack1lll1l1lll_opy_:
        bstack1l11ll11l1_opy_ = CONFIG.get(bstack1l11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢗ"), {})
        logger.debug(bstack1l11l11_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡰࡴࡩࡡ࡭ࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࠪࡹࠢ࢘"), bstack1l11ll11l1_opy_)
        bstack1lll1ll1_opy_ = bstack1lll1l1lll_opy_.get(bstack1l11l11_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡕࡩࡵ࡫ࡡࡵࡧࡵࡷ࢙ࠧ"), [])
        bstack1ll1ll1lll_opy_ = bstack1l11l11_opy_ (u"ࠦ࠱ࠨ࢚").join(bstack1lll1ll1_opy_)
        logger.debug(bstack1l11l11_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡈࡻࡳࡵࡱࡰࠤࡷ࡫ࡰࡦࡣࡷࡩࡷࠦࡳࡵࡴ࡬ࡲ࡬ࡀࠠࠦࡵ࢛ࠥ"), bstack1ll1ll1lll_opy_)
        bstack11l11ll1l_opy_ = {
            bstack1l11l11_opy_ (u"ࠨ࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣ࢜"): bstack1l11l11_opy_ (u"ࠢࡢࡶࡶ࠱ࡷ࡫ࡰࡦࡣࡷࡩࡷࠨ࢝"),
            bstack1l11l11_opy_ (u"ࠣࡨࡲࡶࡨ࡫ࡌࡰࡥࡤࡰࠧ࢞"): bstack1l11l11_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ࢟"),
            bstack1l11l11_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠧࢠ"): bstack1ll1ll1lll_opy_
        }
        bstack1l11ll11l1_opy_.update(bstack11l11ll1l_opy_)
        logger.debug(bstack1l11l11_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼࡙ࠣࡵࡪࡡࡵࡧࡧࠤࡱࡵࡣࡢ࡮ࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࠫࡳࠣࢡ"), bstack1l11ll11l1_opy_)
        CONFIG[bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢢ")] = bstack1l11ll11l1_opy_
        logger.debug(bstack1l11l11_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡌࡩ࡯ࡣ࡯ࠤࡈࡕࡎࡇࡋࡊ࠾ࠥࠫࡳࠣࢣ"), CONFIG)
def bstack111ll11l1_opy_():
    bstack11l11111l1_opy_ = bstack1l1ll1l1l_opy_()
    if not bstack11l11111l1_opy_[bstack1l11l11_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࡙ࡷࡲࠧࢤ")]:
      raise ValueError(bstack1l11l11_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࡚ࡸ࡬ࠡ࡫ࡶࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࡬ࡲࡰ࡯ࠣ࡫ࡷ࡯ࡤࠡࡦࡨࡸࡦ࡯࡬ࡴ࠰ࠥࢥ"))
    return bstack11l11111l1_opy_[bstack1l11l11_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࡛ࡲ࡭ࠩࢦ")] + bstack1l11l11_opy_ (u"ࠪࡃࡨࡧࡰࡴ࠿ࠪࢧ")
@measure(event_name=EVENTS.bstack1l1111ll1_opy_, stage=STAGE.bstack1lll11l1_opy_)
def bstack111ll1l11_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack1l11l11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ࢨ")], CONFIG[bstack1l11l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࢩ")])
        url = bstack1ll1l1llll_opy_
        logger.debug(bstack1l11l11_opy_ (u"ࠨࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬ࡲࡰ࡯ࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡗࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࠦࡁࡑࡋࠥࢪ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack1l11l11_opy_ (u"ࠢࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪࠨࢫ"): bstack1l11l11_opy_ (u"ࠣࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠦࢬ")})
            if response.status_code == 200:
                bstack11ll1lll_opy_ = json.loads(response.text)
                bstack1l1ll1ll_opy_ = bstack11ll1lll_opy_.get(bstack1l11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡴࠩࢭ"), [])
                if bstack1l1ll1ll_opy_:
                    bstack1l11l111ll_opy_ = bstack1l1ll1ll_opy_[0]
                    build_hashed_id = bstack1l11l111ll_opy_.get(bstack1l11l11_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ࢮ"))
                    bstack111111ll1_opy_ = bstack1ll1l11l1_opy_ + build_hashed_id
                    result.extend([build_hashed_id, bstack111111ll1_opy_])
                    logger.info(bstack11ll11111l_opy_.format(bstack111111ll1_opy_))
                    bstack1l11ll1l1_opy_ = CONFIG[bstack1l11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧࢯ")]
                    if bstack1l11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢰ") in CONFIG:
                      bstack1l11ll1l1_opy_ += bstack1l11l11_opy_ (u"࠭ࠠࠨࢱ") + CONFIG[bstack1l11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࢲ")]
                    if bstack1l11ll1l1_opy_ != bstack1l11l111ll_opy_.get(bstack1l11l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ࢳ")):
                      logger.debug(bstack1l1l11l1l1_opy_.format(bstack1l11l111ll_opy_.get(bstack1l11l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧࢴ")), bstack1l11ll1l1_opy_))
                    return result
                else:
                    logger.debug(bstack1l11l11_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡑࡳࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡵࡪࡨࠤࡷ࡫ࡳࡱࡱࡱࡷࡪ࠴ࠢࢵ"))
            else:
                logger.debug(bstack1l11l11_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢶ"))
        except Exception as e:
            logger.error(bstack1l11l11_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࡹࠠ࠻ࠢࡾࢁࠧࢷ").format(str(e)))
    else:
        logger.debug(bstack1l11l11_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡉࡏࡏࡈࡌࡋࠥ࡯ࡳࠡࡰࡲࡸࠥࡹࡥࡵ࠰࡙ࠣࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢸ"))
    return [None, None]
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1llll1lll_opy_ import bstack1llll1lll_opy_, bstack11ll11l1l_opy_, bstack1111l1l11_opy_, bstack1ll1l1l1ll_opy_
from bstack_utils.measure import bstack1l1l11llll_opy_
from bstack_utils.measure import measure
from bstack_utils.percy import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1l1lll1lll_opy_ import bstack1lll11l11l_opy_
from bstack_utils.messages import *
from bstack_utils import bstack1l1ll11lll_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack11l11l1ll_opy_, bstack1l11lllll_opy_, bstack11l111l11_opy_, bstack1l111ll111_opy_, \
  bstack1ll111llll_opy_, \
  Notset, bstack1l11llllll_opy_, \
  bstack1l1111111_opy_, bstack11l11ll1l1_opy_, bstack11ll11l1l1_opy_, bstack1ll1ll1l_opy_, bstack1l1l11ll1_opy_, bstack1l11l1l1ll_opy_, \
  bstack11l11ll1ll_opy_, \
  bstack11lll111_opy_, bstack11l1l1111l_opy_, bstack1l1l1ll11l_opy_, bstack111111l11_opy_, \
  bstack1l1l1l111_opy_, bstack1l111111l1_opy_, bstack11lll11ll1_opy_, bstack1ll1ll1l1_opy_
from bstack_utils.bstack1ll11l1l1_opy_ import bstack11lll11l1l_opy_
from bstack_utils.bstack11ll1llll_opy_ import bstack11ll1ll1l1_opy_, bstack1l11l1111l_opy_
from bstack_utils.bstack1llll1l11l_opy_ import bstack11llll11l1_opy_
from bstack_utils.bstack1lll1ll1ll_opy_ import bstack1l1l11l1ll_opy_, bstack1l11111l1l_opy_
from bstack_utils.bstack11l1ll111l_opy_ import bstack11l1ll111l_opy_
from bstack_utils.bstack1l111lll1_opy_ import bstack1lll11l1ll_opy_
from bstack_utils.proxy import bstack111l1lll1_opy_, bstack1lll1lll1_opy_, bstack1l1111l1_opy_, bstack1l111l11_opy_
from bstack_utils.bstack111l111l1_opy_ import bstack1l1lllll1_opy_
import bstack_utils.bstack1111l1l1l_opy_ as bstack11111l1l_opy_
import bstack_utils.bstack1lll1111ll_opy_ as bstack1l1l111l_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.utils.bstack1ll11111l1_opy_ import bstack1l1l1llll_opy_
from bstack_utils.bstack1111111l_opy_ import bstack11l11l1lll_opy_
from bstack_utils.bstack1l1l111ll_opy_ import bstack1lll1ll1l1_opy_
if os.getenv(bstack1l11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡌࡔࡕࡋࡔࠩࢹ")):
  cli.bstack1ll1ll1ll1_opy_()
else:
  os.environ[bstack1l11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡍࡕࡏࡌࡕࠪࢺ")] = bstack1l11l11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧࢻ")
bstack1llll1ll1l_opy_ = bstack1l11l11_opy_ (u"ࠪࠤࠥ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࠣࠤ࡮࡬ࠨࡱࡣࡪࡩࠥࡃ࠽࠾ࠢࡹࡳ࡮ࡪࠠ࠱ࠫࠣࡿࡡࡴࠠࠡࠢࡷࡶࡾࢁ࡜࡯ࠢࡦࡳࡳࡹࡴࠡࡨࡶࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨ࡝ࠩࡩࡷࡡ࠭ࠩ࠼࡞ࡱࠤࠥࠦࠠࠡࡨࡶ࠲ࡦࡶࡰࡦࡰࡧࡊ࡮ࡲࡥࡔࡻࡱࡧ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪ࠯ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡶ࡟ࡪࡰࡧࡩࡽ࠯ࠠࠬࠢࠥ࠾ࠧࠦࠫࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࠨࡢࡹࡤ࡭ࡹࠦ࡮ࡦࡹࡓࡥ࡬࡫࠲࠯ࡧࡹࡥࡱࡻࡡࡵࡧࠫࠦ࠭࠯ࠠ࠾ࡀࠣࡿࢂࠨࠬࠡ࡞ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥ࡫ࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡄࡦࡶࡤ࡭ࡱࡹࠢࡾ࡞ࠪ࠭࠮࠯࡛ࠣࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠦࡢ࠯ࠠࠬࠢࠥ࠰ࡡࡢ࡮ࠣࠫ࡟ࡲࠥࠦࠠࠡࡿࡦࡥࡹࡩࡨࠩࡧࡻ࠭ࢀࡢ࡮ࠡࠢࠣࠤࢂࡢ࡮ࠡࠢࢀࡠࡳࠦࠠ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱ࠪࢼ")
bstack1lll111l1l_opy_ = bstack1l11l11_opy_ (u"ࠫࡡࡴ࠯ࠫࠢࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࠦࠪ࠰࡞ࡱࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠶ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡩࡡࡱࡵࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠷࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡲࡢ࡭ࡳࡪࡥࡹࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠷ࡣ࡜࡯ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯ࡵ࡯࡭ࡨ࡫ࠨ࠱࠮ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸࠯࡜࡯ࡥࡲࡲࡸࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯ࠥࡃࠠࡳࡧࡴࡹ࡮ࡸࡥࠩࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨࠩ࠼࡞ࡱ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡰࡦࡻ࡮ࡤࡪࠣࡁࠥࡧࡳࡺࡰࡦࠤ࠭ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷ࠮ࠦ࠽࠿ࠢࡾࡠࡳࡲࡥࡵࠢࡦࡥࡵࡹ࠻࡝ࡰࡷࡶࡾࠦࡻ࡝ࡰࡦࡥࡵࡹࠠ࠾ࠢࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࡢࡴࡶࡤࡧࡰࡥࡣࡢࡲࡶ࠭ࡡࡴࠠࠡࡿࠣࡧࡦࡺࡣࡩࠪࡨࡼ࠮ࠦࡻ࡝ࡰࠣࠤࠥࠦࡽ࡝ࡰࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࠻ࠢࡣࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠩࢁࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭ࢂࡦࠬ࡝ࡰࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴ࡞ࡱࠤࠥࢃࠩ࡝ࡰࢀࡠࡳ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࠪࢽ")
from ._version import __version__
bstack1lll111l11_opy_ = None
CONFIG = {}
bstack11l1ll1111_opy_ = {}
bstack111llll1l_opy_ = {}
bstack11111ll11_opy_ = None
bstack1llll111ll_opy_ = None
bstack1lllll1ll_opy_ = None
bstack1l1llll1ll_opy_ = -1
bstack1ll1l111l1_opy_ = 0
bstack111l1ll11_opy_ = bstack1ll1lll1_opy_
bstack11llll1ll1_opy_ = 1
bstack1ll1l1l1l1_opy_ = False
bstack1l11111lll_opy_ = False
bstack1ll1l111ll_opy_ = bstack1l11l11_opy_ (u"ࠬ࠭ࢾ")
bstack11ll111l1l_opy_ = bstack1l11l11_opy_ (u"࠭ࠧࢿ")
bstack1ll111111_opy_ = False
bstack1l1l11lll_opy_ = True
bstack1lll1ll11l_opy_ = bstack1l11l11_opy_ (u"ࠧࠨࣀ")
bstack111lll1l1_opy_ = []
bstack1l1lllllll_opy_ = threading.Lock()
bstack1ll1ll111_opy_ = threading.Lock()
bstack11l1ll111_opy_ = bstack1l11l11_opy_ (u"ࠨࠩࣁ")
bstack1llll1l111_opy_ = False
bstack1ll1l1l1_opy_ = None
bstack11llllll1_opy_ = None
bstack1lllllllll_opy_ = None
bstack1l1l11l11_opy_ = -1
bstack1l1l1l11_opy_ = os.path.join(os.path.expanduser(bstack1l11l11_opy_ (u"ࠩࢁࠫࣂ")), bstack1l11l11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪࣃ"), bstack1l11l11_opy_ (u"ࠫ࠳ࡸ࡯ࡣࡱࡷ࠱ࡷ࡫ࡰࡰࡴࡷ࠱࡭࡫࡬ࡱࡧࡵ࠲࡯ࡹ࡯࡯ࠩࣄ"))
bstack11l1llll1l_opy_ = 0
bstack11llllllll_opy_ = 0
bstack1l11111l_opy_ = []
bstack1l111l1ll_opy_ = []
bstack11l11ll11l_opy_ = []
bstack1lll1lll11_opy_ = []
bstack11lll1ll11_opy_ = bstack1l11l11_opy_ (u"ࠬ࠭ࣅ")
bstack11llll111_opy_ = bstack1l11l11_opy_ (u"࠭ࠧࣆ")
bstack1l1llllll1_opy_ = False
bstack11l111lll_opy_ = False
bstack1lllll1l1l_opy_ = {}
bstack1lll1l1ll_opy_ = None
bstack11ll1l1l1l_opy_ = None
bstack1111l1111_opy_ = None
bstack11111111_opy_ = None
bstack1lllll11ll_opy_ = None
bstack1llll1ll11_opy_ = None
bstack1l1111l11_opy_ = None
bstack1lll1l111_opy_ = None
bstack11l1l11ll_opy_ = None
bstack1ll111l11l_opy_ = None
bstack1l1ll1ll1l_opy_ = None
bstack1l1ll1l111_opy_ = None
bstack11ll1l111l_opy_ = None
bstack1l111ll1l_opy_ = None
bstack11l11l111l_opy_ = None
bstack1l1111lll1_opy_ = None
bstack11llll1l11_opy_ = None
bstack111ll1l1_opy_ = None
bstack1111l11ll_opy_ = None
bstack1ll11l1111_opy_ = None
bstack1ll111ll1_opy_ = None
bstack111lll111_opy_ = None
bstack1l11l1l11l_opy_ = None
thread_local = threading.local()
bstack11l1l1l1l_opy_ = False
bstack11111lll1_opy_ = bstack1l11l11_opy_ (u"ࠢࠣࣇ")
logger = bstack1l1ll11lll_opy_.get_logger(__name__, bstack111l1ll11_opy_)
bstack11l11llll_opy_ = Config.bstack11l111llll_opy_()
percy = bstack1l11l11l_opy_()
bstack1l1l1l1l1_opy_ = bstack1lll11l11l_opy_()
bstack1l1ll11111_opy_ = bstack1ll111lll_opy_()
def bstack1ll11ll1ll_opy_():
  global CONFIG
  global bstack1l1llllll1_opy_
  global bstack11l11llll_opy_
  testContextOptions = bstack1lll1l111l_opy_(CONFIG)
  if bstack1ll111llll_opy_(CONFIG):
    if (bstack1l11l11_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪࣈ") in testContextOptions and str(testContextOptions[bstack1l11l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫࣉ")]).lower() == bstack1l11l11_opy_ (u"ࠪࡸࡷࡻࡥࠨ࣊")):
      bstack1l1llllll1_opy_ = True
    bstack11l11llll_opy_.bstack11l11l11l1_opy_(testContextOptions.get(bstack1l11l11_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ࣋"), False))
  else:
    bstack1l1llllll1_opy_ = True
    bstack11l11llll_opy_.bstack11l11l11l1_opy_(True)
def bstack1ll1lll1l_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack11l1l111_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack11l11l1111_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1l11l11_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡩ࡯࡯ࡨ࡬࡫࡫࡯࡬ࡦࠤ࣌") == args[i].lower() or bstack1l11l11_opy_ (u"ࠨ࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡪ࡮࡭ࠢ࣍") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1lll1ll11l_opy_
      bstack1lll1ll11l_opy_ += bstack1l11l11_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠤࠧ࠭࣎") + path + bstack1l11l11_opy_ (u"ࠨࠤ࣏ࠪ")
      return path
  return None
bstack11l11l1l1_opy_ = re.compile(bstack1l11l11_opy_ (u"ࡴࠥ࠲࠯ࡅ࡜ࠥࡽࠫ࠲࠯ࡅࠩࡾ࠰࠭ࡃ࣐ࠧ"))
def bstack1lll11llll_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack11l11l1l1_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack1l11l11_opy_ (u"ࠥࠨࢀࠨ࣑") + group + bstack1l11l11_opy_ (u"ࠦࢂࠨ࣒"), os.environ.get(group))
  return value
def bstack1ll1ll1l1l_opy_():
  global bstack1l11l1l11l_opy_
  if bstack1l11l1l11l_opy_ is None:
        bstack1l11l1l11l_opy_ = bstack11l11l1111_opy_()
  bstack11l11llll1_opy_ = bstack1l11l1l11l_opy_
  if bstack11l11llll1_opy_ and os.path.exists(os.path.abspath(bstack11l11llll1_opy_)):
    fileName = bstack11l11llll1_opy_
  if bstack1l11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆ࣓ࠩ") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack1l11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࡤࡌࡉࡍࡇࠪࣔ")])) and not bstack1l11l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡓࡧ࡭ࡦࠩࣕ") in locals():
    fileName = os.environ[bstack1l11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬࣖ")]
  if bstack1l11l11_opy_ (u"ࠩࡩ࡭ࡱ࡫ࡎࡢ࡯ࡨࠫࣗ") in locals():
    bstack11ll111_opy_ = os.path.abspath(fileName)
  else:
    bstack11ll111_opy_ = bstack1l11l11_opy_ (u"ࠪࠫࣘ")
  bstack111111111_opy_ = os.getcwd()
  bstack1lll1l11l_opy_ = bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧࣙ")
  bstack1ll1111l_opy_ = bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡧ࡭࡭ࠩࣚ")
  while (not os.path.exists(bstack11ll111_opy_)) and bstack111111111_opy_ != bstack1l11l11_opy_ (u"ࠨࠢࣛ"):
    bstack11ll111_opy_ = os.path.join(bstack111111111_opy_, bstack1lll1l11l_opy_)
    if not os.path.exists(bstack11ll111_opy_):
      bstack11ll111_opy_ = os.path.join(bstack111111111_opy_, bstack1ll1111l_opy_)
    if bstack111111111_opy_ != os.path.dirname(bstack111111111_opy_):
      bstack111111111_opy_ = os.path.dirname(bstack111111111_opy_)
    else:
      bstack111111111_opy_ = bstack1l11l11_opy_ (u"ࠢࠣࣜ")
  bstack1l11l1l11l_opy_ = bstack11ll111_opy_ if os.path.exists(bstack11ll111_opy_) else None
  return bstack1l11l1l11l_opy_
def bstack1lll111lll_opy_():
  bstack11ll111_opy_ = bstack1ll1ll1l1l_opy_()
  if not os.path.exists(bstack11ll111_opy_):
    bstack11l11l1l11_opy_(
      bstack1ll111l1l1_opy_.format(os.getcwd()))
  try:
    with open(bstack11ll111_opy_, bstack1l11l11_opy_ (u"ࠨࡴࠪࣝ")) as stream:
      yaml.add_implicit_resolver(bstack1l11l11_opy_ (u"ࠤࠤࡴࡦࡺࡨࡦࡺࠥࣞ"), bstack11l11l1l1_opy_)
      yaml.add_constructor(bstack1l11l11_opy_ (u"ࠥࠥࡵࡧࡴࡩࡧࡻࠦࣟ"), bstack1lll11llll_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack11ll111_opy_, bstack1l11l11_opy_ (u"ࠫࡷ࠭࣠")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack11l11l1l11_opy_(bstack11ll111l_opy_.format(str(exc)))
def bstack1l111l11l_opy_(config):
  bstack1ll111l1_opy_ = bstack1l11l1lll_opy_(config)
  for option in list(bstack1ll111l1_opy_):
    if option.lower() in bstack111ll1111_opy_ and option != bstack111ll1111_opy_[option.lower()]:
      bstack1ll111l1_opy_[bstack111ll1111_opy_[option.lower()]] = bstack1ll111l1_opy_[option]
      del bstack1ll111l1_opy_[option]
  return config
def bstack1l1l1l1ll_opy_():
  global bstack111llll1l_opy_
  for key, bstack11l1lll1l_opy_ in bstack1l11ll11_opy_.items():
    if isinstance(bstack11l1lll1l_opy_, list):
      for var in bstack11l1lll1l_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack111llll1l_opy_[key] = os.environ[var]
          break
    elif bstack11l1lll1l_opy_ in os.environ and os.environ[bstack11l1lll1l_opy_] and str(os.environ[bstack11l1lll1l_opy_]).strip():
      bstack111llll1l_opy_[key] = os.environ[bstack11l1lll1l_opy_]
  if bstack1l11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ࣡") in os.environ:
    bstack111llll1l_opy_[bstack1l11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ࣢")] = {}
    bstack111llll1l_opy_[bstack1l11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࣣࠫ")][bstack1l11l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣤ")] = os.environ[bstack1l11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫࣥ")]
def bstack1l11lll1ll_opy_():
  global bstack11l1ll1111_opy_
  global bstack1lll1ll11l_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack1l11l11_opy_ (u"ࠪ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࣦ࠭").lower() == val.lower():
      bstack11l1ll1111_opy_[bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣧ")] = {}
      bstack11l1ll1111_opy_[bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣨ")][bstack1l11l11_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣩ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack1l11l111_opy_ in bstack1llllll1l1_opy_.items():
    if isinstance(bstack1l11l111_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1l11l111_opy_:
          if idx < len(sys.argv) and bstack1l11l11_opy_ (u"ࠧ࠮࠯ࠪ࣪") + var.lower() == val.lower() and not key in bstack11l1ll1111_opy_:
            bstack11l1ll1111_opy_[key] = sys.argv[idx + 1]
            bstack1lll1ll11l_opy_ += bstack1l11l11_opy_ (u"ࠨࠢ࠰࠱ࠬ࣫") + var + bstack1l11l11_opy_ (u"ࠩࠣࠫ࣬") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack1l11l11_opy_ (u"ࠪ࠱࠲࣭࠭") + bstack1l11l111_opy_.lower() == val.lower() and not key in bstack11l1ll1111_opy_:
          bstack11l1ll1111_opy_[key] = sys.argv[idx + 1]
          bstack1lll1ll11l_opy_ += bstack1l11l11_opy_ (u"ࠫࠥ࠳࠭ࠨ࣮") + bstack1l11l111_opy_ + bstack1l11l11_opy_ (u"࣯ࠬࠦࠧ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack11l1lll1_opy_(config):
  bstack1l1ll1l11l_opy_ = config.keys()
  for bstack1l1ll11ll1_opy_, bstack11ll111l1_opy_ in bstack1l1l1l1l11_opy_.items():
    if bstack11ll111l1_opy_ in bstack1l1ll1l11l_opy_:
      config[bstack1l1ll11ll1_opy_] = config[bstack11ll111l1_opy_]
      del config[bstack11ll111l1_opy_]
  for bstack1l1ll11ll1_opy_, bstack11ll111l1_opy_ in bstack1l111lll11_opy_.items():
    if isinstance(bstack11ll111l1_opy_, list):
      for bstack11l1l1ll1l_opy_ in bstack11ll111l1_opy_:
        if bstack11l1l1ll1l_opy_ in bstack1l1ll1l11l_opy_:
          config[bstack1l1ll11ll1_opy_] = config[bstack11l1l1ll1l_opy_]
          del config[bstack11l1l1ll1l_opy_]
          break
    elif bstack11ll111l1_opy_ in bstack1l1ll1l11l_opy_:
      config[bstack1l1ll11ll1_opy_] = config[bstack11ll111l1_opy_]
      del config[bstack11ll111l1_opy_]
  for bstack11l1l1ll1l_opy_ in list(config):
    for bstack11ll1ll1ll_opy_ in bstack11l111l111_opy_:
      if bstack11l1l1ll1l_opy_.lower() == bstack11ll1ll1ll_opy_.lower() and bstack11l1l1ll1l_opy_ != bstack11ll1ll1ll_opy_:
        config[bstack11ll1ll1ll_opy_] = config[bstack11l1l1ll1l_opy_]
        del config[bstack11l1l1ll1l_opy_]
  bstack11l1lll111_opy_ = [{}]
  if not config.get(bstack1l11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࣰࠩ")):
    config[bstack1l11l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࣱࠪ")] = [{}]
  bstack11l1lll111_opy_ = config[bstack1l11l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࣲࠫ")]
  for platform in bstack11l1lll111_opy_:
    for bstack11l1l1ll1l_opy_ in list(platform):
      for bstack11ll1ll1ll_opy_ in bstack11l111l111_opy_:
        if bstack11l1l1ll1l_opy_.lower() == bstack11ll1ll1ll_opy_.lower() and bstack11l1l1ll1l_opy_ != bstack11ll1ll1ll_opy_:
          platform[bstack11ll1ll1ll_opy_] = platform[bstack11l1l1ll1l_opy_]
          del platform[bstack11l1l1ll1l_opy_]
  for bstack1l1ll11ll1_opy_, bstack11ll111l1_opy_ in bstack1l111lll11_opy_.items():
    for platform in bstack11l1lll111_opy_:
      if isinstance(bstack11ll111l1_opy_, list):
        for bstack11l1l1ll1l_opy_ in bstack11ll111l1_opy_:
          if bstack11l1l1ll1l_opy_ in platform:
            platform[bstack1l1ll11ll1_opy_] = platform[bstack11l1l1ll1l_opy_]
            del platform[bstack11l1l1ll1l_opy_]
            break
      elif bstack11ll111l1_opy_ in platform:
        platform[bstack1l1ll11ll1_opy_] = platform[bstack11ll111l1_opy_]
        del platform[bstack11ll111l1_opy_]
  for bstack1l1111lll_opy_ in bstack11ll11ll11_opy_:
    if bstack1l1111lll_opy_ in config:
      if not bstack11ll11ll11_opy_[bstack1l1111lll_opy_] in config:
        config[bstack11ll11ll11_opy_[bstack1l1111lll_opy_]] = {}
      config[bstack11ll11ll11_opy_[bstack1l1111lll_opy_]].update(config[bstack1l1111lll_opy_])
      del config[bstack1l1111lll_opy_]
  for platform in bstack11l1lll111_opy_:
    for bstack1l1111lll_opy_ in bstack11ll11ll11_opy_:
      if bstack1l1111lll_opy_ in list(platform):
        if not bstack11ll11ll11_opy_[bstack1l1111lll_opy_] in platform:
          platform[bstack11ll11ll11_opy_[bstack1l1111lll_opy_]] = {}
        platform[bstack11ll11ll11_opy_[bstack1l1111lll_opy_]].update(platform[bstack1l1111lll_opy_])
        del platform[bstack1l1111lll_opy_]
  config = bstack1l111l11l_opy_(config)
  return config
def bstack11lll1l1l_opy_(config):
  global bstack11ll111l1l_opy_
  bstack1l11l1ll11_opy_ = False
  if bstack1l11l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ࣳ") in config and str(config[bstack1l11l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧࣴ")]).lower() != bstack1l11l11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪࣵ"):
    if bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࣶࠩ") not in config or str(config[bstack1l11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪࣷ")]).lower() == bstack1l11l11_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ࣸ"):
      config[bstack1l11l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࣹࠧ")] = False
    else:
      bstack11l11111l1_opy_ = bstack1l1ll1l1l_opy_()
      if bstack1l11l11_opy_ (u"ࠩ࡬ࡷ࡙ࡸࡩࡢ࡮ࡊࡶ࡮ࡪࣺࠧ") in bstack11l11111l1_opy_:
        if not bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࣻ") in config:
          config[bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣼ")] = {}
        config[bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣽ")][bstack1l11l11_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣾ")] = bstack1l11l11_opy_ (u"ࠧࡢࡶࡶ࠱ࡷ࡫ࡰࡦࡣࡷࡩࡷ࠭ࣿ")
        bstack1l11l1ll11_opy_ = True
        bstack11ll111l1l_opy_ = config[bstack1l11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬऀ")].get(bstack1l11l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫँ"))
  if bstack1ll111llll_opy_(config) and bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧं") in config and str(config[bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨः")]).lower() != bstack1l11l11_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫऄ") and not bstack1l11l1ll11_opy_:
    if not bstack1l11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪअ") in config:
      config[bstack1l11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫआ")] = {}
    if not config[bstack1l11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬइ")].get(bstack1l11l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡂࡪࡰࡤࡶࡾࡏ࡮ࡪࡶ࡬ࡥࡱ࡯ࡳࡢࡶ࡬ࡳࡳ࠭ई")) and not bstack1l11l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬउ") in config[bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऊ")]:
      bstack1ll11ll11l_opy_ = datetime.datetime.now()
      bstack11l1lll11_opy_ = bstack1ll11ll11l_opy_.strftime(bstack1l11l11_opy_ (u"ࠬࠫࡤࡠࠧࡥࡣࠪࡎࠥࡎࠩऋ"))
      hostname = socket.gethostname()
      bstack1ll1ll1ll_opy_ = bstack1l11l11_opy_ (u"࠭ࠧऌ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1l11l11_opy_ (u"ࠧࡼࡿࡢࡿࢂࡥࡻࡾࠩऍ").format(bstack11l1lll11_opy_, hostname, bstack1ll1ll1ll_opy_)
      config[bstack1l11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬऎ")][bstack1l11l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫए")] = identifier
    bstack11ll111l1l_opy_ = config[bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧऐ")].get(bstack1l11l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ऑ"))
  return config
def bstack11llll111l_opy_():
  bstack11l1ll1ll1_opy_ =  bstack1ll1ll1l_opy_()[bstack1l11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠫऒ")]
  return bstack11l1ll1ll1_opy_ if bstack11l1ll1ll1_opy_ else -1
def bstack11ll11111_opy_(bstack11l1ll1ll1_opy_):
  global CONFIG
  if not bstack1l11l11_opy_ (u"࠭ࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨओ") in CONFIG[bstack1l11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऔ")]:
    return
  CONFIG[bstack1l11l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪक")] = CONFIG[bstack1l11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫख")].replace(
    bstack1l11l11_opy_ (u"ࠪࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬग"),
    str(bstack11l1ll1ll1_opy_)
  )
def bstack1ll11llll1_opy_():
  global CONFIG
  if not bstack1l11l11_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪघ") in CONFIG[bstack1l11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧङ")]:
    return
  bstack1ll11ll11l_opy_ = datetime.datetime.now()
  bstack11l1lll11_opy_ = bstack1ll11ll11l_opy_.strftime(bstack1l11l11_opy_ (u"࠭ࠥࡥ࠯ࠨࡦ࠲ࠫࡈ࠻ࠧࡐࠫच"))
  CONFIG[bstack1l11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩछ")] = CONFIG[bstack1l11l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪज")].replace(
    bstack1l11l11_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨझ"),
    bstack11l1lll11_opy_
  )
def bstack1ll1l1l111_opy_():
  global CONFIG
  if bstack1l11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬञ") in CONFIG and not bool(CONFIG[bstack1l11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ट")]):
    del CONFIG[bstack1l11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧठ")]
    return
  if not bstack1l11l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨड") in CONFIG:
    CONFIG[bstack1l11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩढ")] = bstack1l11l11_opy_ (u"ࠨࠥࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫण")
  if bstack1l11l11_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨत") in CONFIG[bstack1l11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬथ")]:
    bstack1ll11llll1_opy_()
    os.environ[bstack1l11l11_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨद")] = CONFIG[bstack1l11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧध")]
  if not bstack1l11l11_opy_ (u"࠭ࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨन") in CONFIG[bstack1l11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऩ")]:
    return
  bstack11l1ll1ll1_opy_ = bstack1l11l11_opy_ (u"ࠨࠩप")
  bstack11ll11l11l_opy_ = bstack11llll111l_opy_()
  if bstack11ll11l11l_opy_ != -1:
    bstack11l1ll1ll1_opy_ = bstack1l11l11_opy_ (u"ࠩࡆࡍࠥ࠭फ") + str(bstack11ll11l11l_opy_)
  if bstack11l1ll1ll1_opy_ == bstack1l11l11_opy_ (u"ࠪࠫब"):
    bstack1llll11l_opy_ = bstack1ll1ll11ll_opy_(CONFIG[bstack1l11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧभ")])
    if bstack1llll11l_opy_ != -1:
      bstack11l1ll1ll1_opy_ = str(bstack1llll11l_opy_)
  if bstack11l1ll1ll1_opy_:
    bstack11ll11111_opy_(bstack11l1ll1ll1_opy_)
    os.environ[bstack1l11l11_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩम")] = CONFIG[bstack1l11l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨय")]
def bstack1111lll1_opy_(bstack1ll11lllll_opy_, bstack1ll1111l1l_opy_, path):
  bstack11l11l1l1l_opy_ = {
    bstack1l11l11_opy_ (u"ࠧࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫर"): bstack1ll1111l1l_opy_
  }
  if os.path.exists(path):
    bstack1l11l11ll_opy_ = json.load(open(path, bstack1l11l11_opy_ (u"ࠨࡴࡥࠫऱ")))
  else:
    bstack1l11l11ll_opy_ = {}
  bstack1l11l11ll_opy_[bstack1ll11lllll_opy_] = bstack11l11l1l1l_opy_
  with open(path, bstack1l11l11_opy_ (u"ࠤࡺ࠯ࠧल")) as outfile:
    json.dump(bstack1l11l11ll_opy_, outfile)
def bstack1ll1ll11ll_opy_(bstack1ll11lllll_opy_):
  bstack1ll11lllll_opy_ = str(bstack1ll11lllll_opy_)
  bstack1l111l1l_opy_ = os.path.join(os.path.expanduser(bstack1l11l11_opy_ (u"ࠪࢂࠬळ")), bstack1l11l11_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫऴ"))
  try:
    if not os.path.exists(bstack1l111l1l_opy_):
      os.makedirs(bstack1l111l1l_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1l11l11_opy_ (u"ࠬࢄࠧव")), bstack1l11l11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭श"), bstack1l11l11_opy_ (u"ࠧ࠯ࡤࡸ࡭ࡱࡪ࠭࡯ࡣࡰࡩ࠲ࡩࡡࡤࡪࡨ࠲࡯ࡹ࡯࡯ࠩष"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1l11l11_opy_ (u"ࠨࡹࠪस")):
        pass
      with open(file_path, bstack1l11l11_opy_ (u"ࠤࡺ࠯ࠧह")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1l11l11_opy_ (u"ࠪࡶࠬऺ")) as bstack1l1ll1l1_opy_:
      bstack1l1ll1ll11_opy_ = json.load(bstack1l1ll1l1_opy_)
    if bstack1ll11lllll_opy_ in bstack1l1ll1ll11_opy_:
      bstack111l11l11_opy_ = bstack1l1ll1ll11_opy_[bstack1ll11lllll_opy_][bstack1l11l11_opy_ (u"ࠫ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨऻ")]
      bstack111lllll_opy_ = int(bstack111l11l11_opy_) + 1
      bstack1111lll1_opy_(bstack1ll11lllll_opy_, bstack111lllll_opy_, file_path)
      return bstack111lllll_opy_
    else:
      bstack1111lll1_opy_(bstack1ll11lllll_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack11ll1111_opy_.format(str(e)))
    return -1
def bstack11lllllll_opy_(config):
  if not config[bstack1l11l11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫़ࠧ")] or not config[bstack1l11l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩऽ")]:
    return True
  else:
    return False
def bstack1lll111111_opy_(config, index=0):
  global bstack1ll111111_opy_
  bstack1l1lll1l_opy_ = {}
  caps = bstack1llll11l1l_opy_ + bstack11ll1l1l11_opy_
  if config.get(bstack1l11l11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫा"), False):
    bstack1l1lll1l_opy_[bstack1l11l11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬि")] = True
    bstack1l1lll1l_opy_[bstack1l11l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ी")] = config.get(bstack1l11l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧु"), {})
  if bstack1ll111111_opy_:
    caps += bstack1ll1l11lll_opy_
  for key in config:
    if key in caps + [bstack1l11l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧू")]:
      continue
    bstack1l1lll1l_opy_[key] = config[key]
  if bstack1l11l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨृ") in config:
    for bstack1l1lll11ll_opy_ in config[bstack1l11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩॄ")][index]:
      if bstack1l1lll11ll_opy_ in caps:
        continue
      bstack1l1lll1l_opy_[bstack1l1lll11ll_opy_] = config[bstack1l11l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪॅ")][index][bstack1l1lll11ll_opy_]
  bstack1l1lll1l_opy_[bstack1l11l11_opy_ (u"ࠨࡪࡲࡷࡹࡔࡡ࡮ࡧࠪॆ")] = socket.gethostname()
  if bstack1l11l11_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪे") in bstack1l1lll1l_opy_:
    del (bstack1l1lll1l_opy_[bstack1l11l11_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫै")])
  return bstack1l1lll1l_opy_
def bstack1ll11111l_opy_(config):
  global bstack1ll111111_opy_
  bstack1l1lllll_opy_ = {}
  caps = bstack11ll1l1l11_opy_
  if bstack1ll111111_opy_:
    caps += bstack1ll1l11lll_opy_
  for key in caps:
    if key in config:
      bstack1l1lllll_opy_[key] = config[key]
  return bstack1l1lllll_opy_
def bstack11l11l11ll_opy_(bstack1l1lll1l_opy_, bstack1l1lllll_opy_):
  bstack11lll11lll_opy_ = {}
  for key in bstack1l1lll1l_opy_.keys():
    if key in bstack1l1l1l1l11_opy_:
      bstack11lll11lll_opy_[bstack1l1l1l1l11_opy_[key]] = bstack1l1lll1l_opy_[key]
    else:
      bstack11lll11lll_opy_[key] = bstack1l1lll1l_opy_[key]
  for key in bstack1l1lllll_opy_:
    if key in bstack1l1l1l1l11_opy_:
      bstack11lll11lll_opy_[bstack1l1l1l1l11_opy_[key]] = bstack1l1lllll_opy_[key]
    else:
      bstack11lll11lll_opy_[key] = bstack1l1lllll_opy_[key]
  return bstack11lll11lll_opy_
def bstack11l11111l_opy_(config, index=0):
  global bstack1ll111111_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack11l1l1l1_opy_ = bstack11l11l1ll_opy_(bstack1l1111l1l1_opy_, config, logger)
  bstack1l1lllll_opy_ = bstack1ll11111l_opy_(config)
  bstack11l1llllll_opy_ = bstack11ll1l1l11_opy_
  bstack11l1llllll_opy_ += bstack1lllll11l_opy_
  bstack1l1lllll_opy_ = update(bstack1l1lllll_opy_, bstack11l1l1l1_opy_)
  if bstack1ll111111_opy_:
    bstack11l1llllll_opy_ += bstack1ll1l11lll_opy_
  if bstack1l11l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॉ") in config:
    if bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪॊ") in config[bstack1l11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩो")][index]:
      caps[bstack1l11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬौ")] = config[bstack1l11l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶ्ࠫ")][index][bstack1l11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧॎ")]
    if bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫॏ") in config[bstack1l11l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॐ")][index]:
      caps[bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭॑")] = str(config[bstack1l11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴ॒ࠩ")][index][bstack1l11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ॓")])
    bstack11ll1ll11_opy_ = bstack11l11l1ll_opy_(bstack1l1111l1l1_opy_, config[bstack1l11l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ॔")][index], logger)
    bstack11l1llllll_opy_ += list(bstack11ll1ll11_opy_.keys())
    for bstack11l111lll1_opy_ in bstack11l1llllll_opy_:
      if bstack11l111lll1_opy_ in config[bstack1l11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॕ")][index]:
        if bstack11l111lll1_opy_ == bstack1l11l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬॖ"):
          try:
            bstack11ll1ll11_opy_[bstack11l111lll1_opy_] = str(config[bstack1l11l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॗ")][index][bstack11l111lll1_opy_] * 1.0)
          except:
            bstack11ll1ll11_opy_[bstack11l111lll1_opy_] = str(config[bstack1l11l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨक़")][index][bstack11l111lll1_opy_])
        else:
          bstack11ll1ll11_opy_[bstack11l111lll1_opy_] = config[bstack1l11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩख़")][index][bstack11l111lll1_opy_]
        del (config[bstack1l11l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪग़")][index][bstack11l111lll1_opy_])
    bstack1l1lllll_opy_ = update(bstack1l1lllll_opy_, bstack11ll1ll11_opy_)
  bstack1l1lll1l_opy_ = bstack1lll111111_opy_(config, index)
  for bstack11l1l1ll1l_opy_ in bstack11ll1l1l11_opy_ + list(bstack11l1l1l1_opy_.keys()):
    if bstack11l1l1ll1l_opy_ in bstack1l1lll1l_opy_:
      bstack1l1lllll_opy_[bstack11l1l1ll1l_opy_] = bstack1l1lll1l_opy_[bstack11l1l1ll1l_opy_]
      del (bstack1l1lll1l_opy_[bstack11l1l1ll1l_opy_])
  if bstack1l11llllll_opy_(config):
    bstack1l1lll1l_opy_[bstack1l11l11_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨज़")] = True
    caps.update(bstack1l1lllll_opy_)
    caps[bstack1l11l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪड़")] = bstack1l1lll1l_opy_
  else:
    bstack1l1lll1l_opy_[bstack1l11l11_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪढ़")] = False
    caps.update(bstack11l11l11ll_opy_(bstack1l1lll1l_opy_, bstack1l1lllll_opy_))
    if bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩफ़") in caps:
      caps[bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭य़")] = caps[bstack1l11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫॠ")]
      del (caps[bstack1l11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬॡ")])
    if bstack1l11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩॢ") in caps:
      caps[bstack1l11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫॣ")] = caps[bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ।")]
      del (caps[bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ॥")])
  return caps
def bstack1l11ll1lll_opy_():
  global bstack11l1ll111_opy_
  global CONFIG
  if bstack11l1l111_opy_() <= version.parse(bstack1l11l11_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬ०")):
    if bstack11l1ll111_opy_ != bstack1l11l11_opy_ (u"࠭ࠧ१"):
      return bstack1l11l11_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ२") + bstack11l1ll111_opy_ + bstack1l11l11_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧ३")
    return bstack1llll1llll_opy_
  if bstack11l1ll111_opy_ != bstack1l11l11_opy_ (u"ࠩࠪ४"):
    return bstack1l11l11_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ५") + bstack11l1ll111_opy_ + bstack1l11l11_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧ६")
  return bstack1l111111ll_opy_
def bstack11lll1l1_opy_(options):
  return hasattr(options, bstack1l11l11_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭७"))
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
def bstack1ll1lll1ll_opy_(options, bstack11lll111ll_opy_):
  for bstack11l111111_opy_ in bstack11lll111ll_opy_:
    if bstack11l111111_opy_ in [bstack1l11l11_opy_ (u"࠭ࡡࡳࡩࡶࠫ८"), bstack1l11l11_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫ९")]:
      continue
    if bstack11l111111_opy_ in options._experimental_options:
      options._experimental_options[bstack11l111111_opy_] = update(options._experimental_options[bstack11l111111_opy_],
                                                         bstack11lll111ll_opy_[bstack11l111111_opy_])
    else:
      options.add_experimental_option(bstack11l111111_opy_, bstack11lll111ll_opy_[bstack11l111111_opy_])
  if bstack1l11l11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭॰") in bstack11lll111ll_opy_:
    for arg in bstack11lll111ll_opy_[bstack1l11l11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॱ")]:
      options.add_argument(arg)
    del (bstack11lll111ll_opy_[bstack1l11l11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨॲ")])
  if bstack1l11l11_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨॳ") in bstack11lll111ll_opy_:
    for ext in bstack11lll111ll_opy_[bstack1l11l11_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩॴ")]:
      try:
        options.add_extension(ext)
      except OSError:
        options.add_encoded_extension(ext)
    del (bstack11lll111ll_opy_[bstack1l11l11_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪॵ")])
def bstack1l1lll1l1l_opy_(options, bstack11l1l11ll1_opy_):
  if bstack1l11l11_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ॶ") in bstack11l1l11ll1_opy_:
    for bstack11lll1lll1_opy_ in bstack11l1l11ll1_opy_[bstack1l11l11_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧॷ")]:
      if bstack11lll1lll1_opy_ in options._preferences:
        options._preferences[bstack11lll1lll1_opy_] = update(options._preferences[bstack11lll1lll1_opy_], bstack11l1l11ll1_opy_[bstack1l11l11_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨॸ")][bstack11lll1lll1_opy_])
      else:
        options.set_preference(bstack11lll1lll1_opy_, bstack11l1l11ll1_opy_[bstack1l11l11_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩॹ")][bstack11lll1lll1_opy_])
  if bstack1l11l11_opy_ (u"ࠫࡦࡸࡧࡴࠩॺ") in bstack11l1l11ll1_opy_:
    for arg in bstack11l1l11ll1_opy_[bstack1l11l11_opy_ (u"ࠬࡧࡲࡨࡵࠪॻ")]:
      options.add_argument(arg)
def bstack1l1ll111ll_opy_(options, bstack11l1lll1l1_opy_):
  if bstack1l11l11_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࠧॼ") in bstack11l1lll1l1_opy_:
    options.use_webview(bool(bstack11l1lll1l1_opy_[bstack1l11l11_opy_ (u"ࠧࡸࡧࡥࡺ࡮࡫ࡷࠨॽ")]))
  bstack1ll1lll1ll_opy_(options, bstack11l1lll1l1_opy_)
def bstack1l11llll11_opy_(options, bstack1l1l1111l1_opy_):
  for bstack1l1l11l111_opy_ in bstack1l1l1111l1_opy_:
    if bstack1l1l11l111_opy_ in [bstack1l11l11_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬॾ"), bstack1l11l11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॿ")]:
      continue
    options.set_capability(bstack1l1l11l111_opy_, bstack1l1l1111l1_opy_[bstack1l1l11l111_opy_])
  if bstack1l11l11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨঀ") in bstack1l1l1111l1_opy_:
    for arg in bstack1l1l1111l1_opy_[bstack1l11l11_opy_ (u"ࠫࡦࡸࡧࡴࠩঁ")]:
      options.add_argument(arg)
  if bstack1l11l11_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩং") in bstack1l1l1111l1_opy_:
    options.bstack1ll1111lll_opy_(bool(bstack1l1l1111l1_opy_[bstack1l11l11_opy_ (u"࠭ࡴࡦࡥ࡫ࡲࡴࡲ࡯ࡨࡻࡓࡶࡪࡼࡩࡦࡹࠪঃ")]))
def bstack1l1llll11l_opy_(options, bstack11l1l1l1ll_opy_):
  for bstack11ll1lll1l_opy_ in bstack11l1l1l1ll_opy_:
    if bstack11ll1lll1l_opy_ in [bstack1l11l11_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ঄"), bstack1l11l11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭অ")]:
      continue
    options._options[bstack11ll1lll1l_opy_] = bstack11l1l1l1ll_opy_[bstack11ll1lll1l_opy_]
  if bstack1l11l11_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭আ") in bstack11l1l1l1ll_opy_:
    for bstack11l11lllll_opy_ in bstack11l1l1l1ll_opy_[bstack1l11l11_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧই")]:
      options.bstack1ll1llll1_opy_(
        bstack11l11lllll_opy_, bstack11l1l1l1ll_opy_[bstack1l11l11_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨঈ")][bstack11l11lllll_opy_])
  if bstack1l11l11_opy_ (u"ࠬࡧࡲࡨࡵࠪউ") in bstack11l1l1l1ll_opy_:
    for arg in bstack11l1l1l1ll_opy_[bstack1l11l11_opy_ (u"࠭ࡡࡳࡩࡶࠫঊ")]:
      options.add_argument(arg)
def bstack1ll1111l1_opy_(options, caps):
  if not hasattr(options, bstack1l11l11_opy_ (u"ࠧࡌࡇ࡜ࠫঋ")):
    return
  if options.KEY == bstack1l11l11_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ঌ"):
    options = bstack1ll1ll1l11_opy_.bstack11l1ll1l1_opy_(bstack11lll1ll1_opy_=options, config=CONFIG)
  if options.KEY == bstack1l11l11_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ঍") and options.KEY in caps:
    bstack1ll1lll1ll_opy_(options, caps[bstack1l11l11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ঎")])
  elif options.KEY == bstack1l11l11_opy_ (u"ࠫࡲࡵࡺ࠻ࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩএ") and options.KEY in caps:
    bstack1l1lll1l1l_opy_(options, caps[bstack1l11l11_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪঐ")])
  elif options.KEY == bstack1l11l11_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧ঑") and options.KEY in caps:
    bstack1l11llll11_opy_(options, caps[bstack1l11l11_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨ঒")])
  elif options.KEY == bstack1l11l11_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩও") and options.KEY in caps:
    bstack1l1ll111ll_opy_(options, caps[bstack1l11l11_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪঔ")])
  elif options.KEY == bstack1l11l11_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩক") and options.KEY in caps:
    bstack1l1llll11l_opy_(options, caps[bstack1l11l11_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪখ")])
def bstack1lll1llll_opy_(caps):
  global bstack1ll111111_opy_
  if isinstance(os.environ.get(bstack1l11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭গ")), str):
    bstack1ll111111_opy_ = eval(os.getenv(bstack1l11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧঘ")))
  if bstack1ll111111_opy_:
    if bstack1ll1lll1l_opy_() < version.parse(bstack1l11l11_opy_ (u"ࠧ࠳࠰࠶࠲࠵࠭ঙ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1l11l11_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨচ")
    if bstack1l11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧছ") in caps:
      browser = caps[bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨজ")]
    elif bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬঝ") in caps:
      browser = caps[bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ঞ")]
    browser = str(browser).lower()
    if browser == bstack1l11l11_opy_ (u"࠭ࡩࡱࡪࡲࡲࡪ࠭ট") or browser == bstack1l11l11_opy_ (u"ࠧࡪࡲࡤࡨࠬঠ"):
      browser = bstack1l11l11_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨড")
    if browser == bstack1l11l11_opy_ (u"ࠩࡶࡥࡲࡹࡵ࡯ࡩࠪঢ"):
      browser = bstack1l11l11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪণ")
    if browser not in [bstack1l11l11_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫত"), bstack1l11l11_opy_ (u"ࠬ࡫ࡤࡨࡧࠪথ"), bstack1l11l11_opy_ (u"࠭ࡩࡦࠩদ"), bstack1l11l11_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧধ"), bstack1l11l11_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩন")]:
      return None
    try:
      package = bstack1l11l11_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࠮ࡼࡿ࠱ࡳࡵࡺࡩࡰࡰࡶࠫ঩").format(browser)
      name = bstack1l11l11_opy_ (u"ࠪࡓࡵࡺࡩࡰࡰࡶࠫপ")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack11lll1l1_opy_(options):
        return None
      for bstack11l1l1ll1l_opy_ in caps.keys():
        options.set_capability(bstack11l1l1ll1l_opy_, caps[bstack11l1l1ll1l_opy_])
      bstack1ll1111l1_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1lllll1l1_opy_(options, bstack11l1ll1l1l_opy_):
  if not bstack11lll1l1_opy_(options):
    return
  for bstack11l1l1ll1l_opy_ in bstack11l1ll1l1l_opy_.keys():
    if bstack11l1l1ll1l_opy_ in bstack1lllll11l_opy_:
      continue
    if bstack11l1l1ll1l_opy_ in options._caps and type(options._caps[bstack11l1l1ll1l_opy_]) in [dict, list]:
      options._caps[bstack11l1l1ll1l_opy_] = update(options._caps[bstack11l1l1ll1l_opy_], bstack11l1ll1l1l_opy_[bstack11l1l1ll1l_opy_])
    else:
      options.set_capability(bstack11l1l1ll1l_opy_, bstack11l1ll1l1l_opy_[bstack11l1l1ll1l_opy_])
  bstack1ll1111l1_opy_(options, bstack11l1ll1l1l_opy_)
  if bstack1l11l11_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪফ") in options._caps:
    if options._caps[bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪব")] and options._caps[bstack1l11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫভ")].lower() != bstack1l11l11_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨম"):
      del options._caps[bstack1l11l11_opy_ (u"ࠨ࡯ࡲࡾ࠿ࡪࡥࡣࡷࡪ࡫ࡪࡸࡁࡥࡦࡵࡩࡸࡹࠧয")]
def bstack111l1ll1_opy_(proxy_config):
  if bstack1l11l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭র") in proxy_config:
    proxy_config[bstack1l11l11_opy_ (u"ࠪࡷࡸࡲࡐࡳࡱࡻࡽࠬ঱")] = proxy_config[bstack1l11l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨল")]
    del (proxy_config[bstack1l11l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ঳")])
  if bstack1l11l11_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩ঴") in proxy_config and proxy_config[bstack1l11l11_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪ঵")].lower() != bstack1l11l11_opy_ (u"ࠨࡦ࡬ࡶࡪࡩࡴࠨশ"):
    proxy_config[bstack1l11l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬষ")] = bstack1l11l11_opy_ (u"ࠪࡱࡦࡴࡵࡢ࡮ࠪস")
  if bstack1l11l11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡄࡹࡹࡵࡣࡰࡰࡩ࡭࡬࡛ࡲ࡭ࠩহ") in proxy_config:
    proxy_config[bstack1l11l11_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ঺")] = bstack1l11l11_opy_ (u"࠭ࡰࡢࡥࠪ঻")
  return proxy_config
def bstack1lll1l1ll1_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1l11l11_opy_ (u"ࠧࡱࡴࡲࡼࡾ়࠭") in config:
    return proxy
  config[bstack1l11l11_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧঽ")] = bstack111l1ll1_opy_(config[bstack1l11l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨা")])
  if proxy == None:
    proxy = Proxy(config[bstack1l11l11_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩি")])
  return proxy
def bstack1111ll111_opy_(self):
  global CONFIG
  global bstack1l1ll1l111_opy_
  try:
    proxy = bstack1l1111l1_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1l11l11_opy_ (u"ࠫ࠳ࡶࡡࡤࠩী")):
        proxies = bstack111l1lll1_opy_(proxy, bstack1l11ll1lll_opy_())
        if len(proxies) > 0:
          protocol, bstack1llll111_opy_ = proxies.popitem()
          if bstack1l11l11_opy_ (u"ࠧࡀ࠯࠰ࠤু") in bstack1llll111_opy_:
            return bstack1llll111_opy_
          else:
            return bstack1l11l11_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢূ") + bstack1llll111_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1l11l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡴࡷࡵࡸࡺࠢࡸࡶࡱࠦ࠺ࠡࡽࢀࠦৃ").format(str(e)))
  return bstack1l1ll1l111_opy_(self)
def bstack11l1111ll_opy_():
  global CONFIG
  return bstack1l111l11_opy_(CONFIG) and bstack1l11l1l1ll_opy_() and bstack11l1l111_opy_() >= version.parse(bstack111111l1l_opy_)
def bstack1l1l11ll1l_opy_():
  global CONFIG
  return (bstack1l11l11_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫৄ") in CONFIG or bstack1l11l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭৅") in CONFIG) and bstack11l11ll1ll_opy_()
def bstack1l11l1lll_opy_(config):
  bstack1ll111l1_opy_ = {}
  if bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ৆") in config:
    bstack1ll111l1_opy_ = config[bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨে")]
  if bstack1l11l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫৈ") in config:
    bstack1ll111l1_opy_ = config[bstack1l11l11_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ৉")]
  proxy = bstack1l1111l1_opy_(config)
  if proxy:
    if proxy.endswith(bstack1l11l11_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ৊")) and os.path.isfile(proxy):
      bstack1ll111l1_opy_[bstack1l11l11_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫো")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1l11l11_opy_ (u"ࠩ࠱ࡴࡦࡩࠧৌ")):
        proxies = bstack1lll1lll1_opy_(config, bstack1l11ll1lll_opy_())
        if len(proxies) > 0:
          protocol, bstack1llll111_opy_ = proxies.popitem()
          if bstack1l11l11_opy_ (u"ࠥ࠾࠴࠵্ࠢ") in bstack1llll111_opy_:
            parsed_url = urlparse(bstack1llll111_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1l11l11_opy_ (u"ࠦ࠿࠵࠯ࠣৎ") + bstack1llll111_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1ll111l1_opy_[bstack1l11l11_opy_ (u"ࠬࡶࡲࡰࡺࡼࡌࡴࡹࡴࠨ৏")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1ll111l1_opy_[bstack1l11l11_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵࠩ৐")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1ll111l1_opy_[bstack1l11l11_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪ৑")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1ll111l1_opy_[bstack1l11l11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫ৒")] = str(parsed_url.password)
  return bstack1ll111l1_opy_
def bstack1lll1l111l_opy_(config):
  if bstack1l11l11_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧ৓") in config:
    return config[bstack1l11l11_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨ৔")]
  return {}
def bstack11lll1l1ll_opy_(caps):
  global bstack11ll111l1l_opy_
  if bstack1l11l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ৕") in caps:
    caps[bstack1l11l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭৖")][bstack1l11l11_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬৗ")] = True
    if bstack11ll111l1l_opy_:
      caps[bstack1l11l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ৘")][bstack1l11l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ৙")] = bstack11ll111l1l_opy_
  else:
    caps[bstack1l11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࠧ৚")] = True
    if bstack11ll111l1l_opy_:
      caps[bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ৛")] = bstack11ll111l1l_opy_
@measure(event_name=EVENTS.bstack1l1ll1llll_opy_, stage=STAGE.bstack1lll11l1_opy_, bstack1l1lll11l_opy_=bstack1lllll1ll_opy_)
def bstack111l1111l_opy_():
  global CONFIG
  if not bstack1ll111llll_opy_(CONFIG) or cli.is_enabled(CONFIG):
    return
  if bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨড়") in CONFIG and bstack11lll11ll1_opy_(CONFIG[bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩঢ়")]):
    if (
      bstack1l11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ৞") in CONFIG
      and bstack11lll11ll1_opy_(CONFIG[bstack1l11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫয়")].get(bstack1l11l11_opy_ (u"ࠨࡵ࡮࡭ࡵࡈࡩ࡯ࡣࡵࡽࡎࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡡࡵ࡫ࡲࡲࠬৠ")))
    ):
      logger.debug(bstack1l11l11_opy_ (u"ࠤࡏࡳࡨࡧ࡬ࠡࡤ࡬ࡲࡦࡸࡹࠡࡰࡲࡸࠥࡹࡴࡢࡴࡷࡩࡩࠦࡡࡴࠢࡶ࡯࡮ࡶࡂࡪࡰࡤࡶࡾࡏ࡮ࡪࡶ࡬ࡥࡱ࡯ࡳࡢࡶ࡬ࡳࡳࠦࡩࡴࠢࡨࡲࡦࡨ࡬ࡦࡦࠥৡ"))
      return
    bstack1ll111l1_opy_ = bstack1l11l1lll_opy_(CONFIG)
    bstack1l1l1l1lll_opy_(CONFIG[bstack1l11l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ৢ")], bstack1ll111l1_opy_)
def bstack1l1l1l1lll_opy_(key, bstack1ll111l1_opy_):
  global bstack1lll111l11_opy_
  logger.info(bstack1ll11l111_opy_)
  try:
    bstack1lll111l11_opy_ = Local()
    bstack11lll1111_opy_ = {bstack1l11l11_opy_ (u"ࠫࡰ࡫ࡹࠨৣ"): key}
    bstack11lll1111_opy_.update(bstack1ll111l1_opy_)
    logger.debug(bstack1lllll111_opy_.format(str(bstack11lll1111_opy_)).replace(key, bstack1l11l11_opy_ (u"ࠬࡡࡒࡆࡆࡄࡇ࡙ࡋࡄ࡞ࠩ৤")))
    bstack1lll111l11_opy_.start(**bstack11lll1111_opy_)
    if bstack1lll111l11_opy_.isRunning():
      logger.info(bstack11ll111ll_opy_)
  except Exception as e:
    bstack11l11l1l11_opy_(bstack1llll1ll_opy_.format(str(e)))
def bstack1111l1ll1_opy_():
  global bstack1lll111l11_opy_
  if bstack1lll111l11_opy_.isRunning():
    logger.info(bstack11llll1l_opy_)
    bstack1lll111l11_opy_.stop()
  bstack1lll111l11_opy_ = None
def bstack1l1l11l1l_opy_(bstack11llllll_opy_=[]):
  global CONFIG
  bstack1l1llll11_opy_ = []
  bstack1l11lll1l_opy_ = [bstack1l11l11_opy_ (u"࠭࡯ࡴࠩ৥"), bstack1l11l11_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪ০"), bstack1l11l11_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬ১"), bstack1l11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ২"), bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ৩"), bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ৪")]
  try:
    for err in bstack11llllll_opy_:
      bstack1111ll1l_opy_ = {}
      for k in bstack1l11lll1l_opy_:
        val = CONFIG[bstack1l11l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ৫")][int(err[bstack1l11l11_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ৬")])].get(k)
        if val:
          bstack1111ll1l_opy_[k] = val
      if(err[bstack1l11l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭৭")] != bstack1l11l11_opy_ (u"ࠨࠩ৮")):
        bstack1111ll1l_opy_[bstack1l11l11_opy_ (u"ࠩࡷࡩࡸࡺࡳࠨ৯")] = {
          err[bstack1l11l11_opy_ (u"ࠪࡲࡦࡳࡥࠨৰ")]: err[bstack1l11l11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪৱ")]
        }
        bstack1l1llll11_opy_.append(bstack1111ll1l_opy_)
  except Exception as e:
    logger.debug(bstack1l11l11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧࡱࡵࡱࡦࡺࡴࡪࡰࡪࠤࡩࡧࡴࡢࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸ࠿ࠦࠧ৲") + str(e))
  finally:
    return bstack1l1llll11_opy_
def bstack1l1l1ll1l1_opy_(file_name):
  bstack11ll11lll_opy_ = []
  try:
    bstack11ll1111ll_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack11ll1111ll_opy_):
      with open(bstack11ll1111ll_opy_) as f:
        bstack11lllll11_opy_ = json.load(f)
        bstack11ll11lll_opy_ = bstack11lllll11_opy_
      os.remove(bstack11ll1111ll_opy_)
    return bstack11ll11lll_opy_
  except Exception as e:
    logger.debug(bstack1l11l11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡨ࡬ࡲࡩ࡯࡮ࡨࠢࡨࡶࡷࡵࡲࠡ࡮࡬ࡷࡹࡀࠠࠨ৳") + str(e))
    return bstack11ll11lll_opy_
def bstack1l1111111l_opy_():
  try:
      from bstack_utils.constants import bstack111l111l_opy_, EVENTS
      from bstack_utils.helper import bstack1l11lllll_opy_, get_host_info, bstack11l11llll_opy_
      from datetime import datetime
      from filelock import FileLock
      bstack1l111ll11_opy_ = os.path.join(os.getcwd(), bstack1l11l11_opy_ (u"ࠧ࡭ࡱࡪࠫ৴"), bstack1l11l11_opy_ (u"ࠨ࡭ࡨࡽ࠲ࡳࡥࡵࡴ࡬ࡧࡸ࠴ࡪࡴࡱࡱࠫ৵"))
      lock = FileLock(bstack1l111ll11_opy_+bstack1l11l11_opy_ (u"ࠤ࠱ࡰࡴࡩ࡫ࠣ৶"))
      def bstack1ll11l1ll_opy_():
          try:
              with lock:
                  with open(bstack1l111ll11_opy_, bstack1l11l11_opy_ (u"ࠥࡶࠧ৷"), encoding=bstack1l11l11_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥ৸")) as file:
                      data = json.load(file)
                      config = {
                          bstack1l11l11_opy_ (u"ࠧ࡮ࡥࡢࡦࡨࡶࡸࠨ৹"): {
                              bstack1l11l11_opy_ (u"ࠨࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠧ৺"): bstack1l11l11_opy_ (u"ࠢࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠥ৻"),
                          }
                      }
                      bstack1l1l11111l_opy_ = datetime.utcnow()
                      bstack1ll11ll11l_opy_ = bstack1l1l11111l_opy_.strftime(bstack1l11l11_opy_ (u"ࠣࠧ࡜࠱ࠪࡳ࠭ࠦࡦࡗࠩࡍࡀࠥࡎ࠼ࠨࡗ࠳ࠫࡦࠡࡗࡗࡇࠧৼ"))
                      bstack11111l11l_opy_ = os.environ.get(bstack1l11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ৽")) if os.environ.get(bstack1l11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ৾")) else bstack11l11llll_opy_.get_property(bstack1l11l11_opy_ (u"ࠦࡸࡪ࡫ࡓࡷࡱࡍࡩࠨ৿"))
                      payload = {
                          bstack1l11l11_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠤ਀"): bstack1l11l11_opy_ (u"ࠨࡳࡥ࡭ࡢࡩࡻ࡫࡮ࡵࡵࠥਁ"),
                          bstack1l11l11_opy_ (u"ࠢࡥࡣࡷࡥࠧਂ"): {
                              bstack1l11l11_opy_ (u"ࠣࡶࡨࡷࡹ࡮ࡵࡣࡡࡸࡹ࡮ࡪࠢਃ"): bstack11111l11l_opy_,
                              bstack1l11l11_opy_ (u"ࠤࡦࡶࡪࡧࡴࡦࡦࡢࡨࡦࡿࠢ਄"): bstack1ll11ll11l_opy_,
                              bstack1l11l11_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡱࡥࡲ࡫ࠢਅ"): bstack1l11l11_opy_ (u"ࠦࡘࡊࡋࡇࡧࡤࡸࡺࡸࡥࡑࡧࡵࡪࡴࡸ࡭ࡢࡰࡦࡩࠧਆ"),
                              bstack1l11l11_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣ࡯ࡹ࡯࡯ࠤਇ"): {
                                  bstack1l11l11_opy_ (u"ࠨ࡭ࡦࡣࡶࡹࡷ࡫ࡳࠣਈ"): data,
                                  bstack1l11l11_opy_ (u"ࠢࡴࡦ࡮ࡖࡺࡴࡉࡥࠤਉ"): bstack11l11llll_opy_.get_property(bstack1l11l11_opy_ (u"ࠣࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠥਊ"))
                              },
                              bstack1l11l11_opy_ (u"ࠤࡸࡷࡪࡸ࡟ࡥࡣࡷࡥࠧ਋"): bstack11l11llll_opy_.get_property(bstack1l11l11_opy_ (u"ࠥࡹࡸ࡫ࡲࡏࡣࡰࡩࠧ਌")),
                              bstack1l11l11_opy_ (u"ࠦ࡭ࡵࡳࡵࡡ࡬ࡲ࡫ࡵࠢ਍"): get_host_info()
                          }
                      }
                      bstack1ll11lll11_opy_ = bstack11l111l11_opy_(cli.config, [bstack1l11l11_opy_ (u"ࠧࡧࡰࡪࡵࠥ਎"), bstack1l11l11_opy_ (u"ࠨࡥࡥࡵࡌࡲࡸࡺࡲࡶ࡯ࡨࡲࡹࡧࡴࡪࡱࡱࠦਏ"), bstack1l11l11_opy_ (u"ࠢࡢࡲ࡬ࠦਐ")], bstack111l111l_opy_)
                      response = bstack1l11lllll_opy_(bstack1l11l11_opy_ (u"ࠣࡒࡒࡗ࡙ࠨ਑"), bstack1ll11lll11_opy_, payload, config)
                      if(response.status_code >= 200 and response.status_code < 300):
                          logger.debug(bstack1l11l11_opy_ (u"ࠤࡇࡥࡹࡧࠠࡴࡧࡱࡸࠥࡹࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡹࡵࠠࡼࡿࠣࡻ࡮ࡺࡨࠡࡦࡤࡸࡦࠦࡻࡾࠤ਒").format(bstack111l111l_opy_, payload))
                      else:
                          logger.debug(bstack1l11l11_opy_ (u"ࠥࡖࡪࡷࡵࡦࡵࡷࠤ࡫ࡧࡩ࡭ࡧࡧࠤ࡫ࡵࡲࠡࡽࢀࠤࡼ࡯ࡴࡩࠢࡧࡥࡹࡧࠠࡼࡿࠥਓ").format(bstack111l111l_opy_, payload))
          except Exception as e:
              logger.debug(bstack1l11l11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡱࡨࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵࠣࡨࡦࡺࡡࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶࠥࢁࡽࠣਔ").format(e))
      bstack1ll11l1ll_opy_()
      bstack11l11ll1l1_opy_(bstack1l111ll11_opy_, logger)
  except:
    pass
def bstack11lll11l1_opy_():
  global bstack11111lll1_opy_
  global bstack111lll1l1_opy_
  global bstack1l11111l_opy_
  global bstack1l111l1ll_opy_
  global bstack11l11ll11l_opy_
  global bstack11llll111_opy_
  global CONFIG
  bstack11ll1111l1_opy_ = os.environ.get(bstack1l11l11_opy_ (u"ࠬࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉ࠭ਕ"))
  if bstack11ll1111l1_opy_ in [bstack1l11l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬਖ"), bstack1l11l11_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ਗ")]:
    bstack11111l111_opy_()
  percy.shutdown()
  if bstack11111lll1_opy_:
    logger.warning(bstack111llll1_opy_.format(str(bstack11111lll1_opy_)))
  else:
    try:
      bstack1l11l11ll_opy_ = bstack1l1111111_opy_(bstack1l11l11_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧਘ"), logger)
      if bstack1l11l11ll_opy_.get(bstack1l11l11_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧਙ")) and bstack1l11l11ll_opy_.get(bstack1l11l11_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨਚ")).get(bstack1l11l11_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ਛ")):
        logger.warning(bstack111llll1_opy_.format(str(bstack1l11l11ll_opy_[bstack1l11l11_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪਜ")][bstack1l11l11_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨਝ")])))
    except Exception as e:
      logger.error(e)
  if cli.is_running():
    bstack1llll1lll_opy_.invoke(bstack11ll11l1l_opy_.bstack1lll1l1l1_opy_)
  logger.info(bstack1l11111ll_opy_)
  global bstack1lll111l11_opy_
  if bstack1lll111l11_opy_:
    bstack1111l1ll1_opy_()
  try:
    with bstack1l1lllllll_opy_:
      bstack1lll11ll_opy_ = bstack111lll1l1_opy_.copy()
    for driver in bstack1lll11ll_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack11lll1l11_opy_)
  if bstack11llll111_opy_ == bstack1l11l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ਞ"):
    bstack11l11ll11l_opy_ = bstack1l1l1ll1l1_opy_(bstack1l11l11_opy_ (u"ࠨࡴࡲࡦࡴࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩਟ"))
  if bstack11llll111_opy_ == bstack1l11l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩਠ") and len(bstack1l111l1ll_opy_) == 0:
    bstack1l111l1ll_opy_ = bstack1l1l1ll1l1_opy_(bstack1l11l11_opy_ (u"ࠪࡴࡼࡥࡰࡺࡶࡨࡷࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨਡ"))
    if len(bstack1l111l1ll_opy_) == 0:
      bstack1l111l1ll_opy_ = bstack1l1l1ll1l1_opy_(bstack1l11l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡵࡶࡰࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪਢ"))
  bstack1l111ll1_opy_ = bstack1l11l11_opy_ (u"ࠬ࠭ਣ")
  if len(bstack1l11111l_opy_) > 0:
    bstack1l111ll1_opy_ = bstack1l1l11l1l_opy_(bstack1l11111l_opy_)
  elif len(bstack1l111l1ll_opy_) > 0:
    bstack1l111ll1_opy_ = bstack1l1l11l1l_opy_(bstack1l111l1ll_opy_)
  elif len(bstack11l11ll11l_opy_) > 0:
    bstack1l111ll1_opy_ = bstack1l1l11l1l_opy_(bstack11l11ll11l_opy_)
  elif len(bstack1lll1lll11_opy_) > 0:
    bstack1l111ll1_opy_ = bstack1l1l11l1l_opy_(bstack1lll1lll11_opy_)
  if bool(bstack1l111ll1_opy_):
    bstack1l1111ll11_opy_(bstack1l111ll1_opy_)
  else:
    bstack1l1111ll11_opy_()
  bstack11l11ll1l1_opy_(bstack1llll1111_opy_, logger)
  if bstack11ll1111l1_opy_ not in [bstack1l11l11_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧਤ")]:
    bstack1l1111111l_opy_()
  bstack1l1ll11lll_opy_.bstack1l11lll1l1_opy_(CONFIG)
  if len(bstack11l11ll11l_opy_) > 0:
    sys.exit(len(bstack11l11ll11l_opy_))
def bstack11l11l1ll1_opy_(bstack11ll1l11ll_opy_, frame):
  global bstack11l11llll_opy_
  logger.error(bstack1ll1l11l11_opy_)
  bstack11l11llll_opy_.bstack11l11ll1_opy_(bstack1l11l11_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡏࡱࠪਥ"), bstack11ll1l11ll_opy_)
  if hasattr(signal, bstack1l11l11_opy_ (u"ࠨࡕ࡬࡫ࡳࡧ࡬ࡴࠩਦ")):
    bstack11l11llll_opy_.bstack11l11ll1_opy_(bstack1l11l11_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩਧ"), signal.Signals(bstack11ll1l11ll_opy_).name)
  else:
    bstack11l11llll_opy_.bstack11l11ll1_opy_(bstack1l11l11_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪਨ"), bstack1l11l11_opy_ (u"ࠫࡘࡏࡇࡖࡐࡎࡒࡔ࡝ࡎࠨ਩"))
  if cli.is_running():
    bstack1llll1lll_opy_.invoke(bstack11ll11l1l_opy_.bstack1lll1l1l1_opy_)
  bstack11ll1111l1_opy_ = os.environ.get(bstack1l11l11_opy_ (u"ࠬࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉ࠭ਪ"))
  if bstack11ll1111l1_opy_ == bstack1l11l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ਫ") and not cli.is_enabled(CONFIG):
    bstack11ll111ll1_opy_.stop(bstack11l11llll_opy_.get_property(bstack1l11l11_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡔ࡫ࡪࡲࡦࡲࠧਬ")))
  bstack11lll11l1_opy_()
  sys.exit(1)
def bstack11l11l1l11_opy_(err):
  logger.critical(bstack1lllll1111_opy_.format(str(err)))
  bstack1l1111ll11_opy_(bstack1lllll1111_opy_.format(str(err)), True)
  atexit.unregister(bstack11lll11l1_opy_)
  bstack11111l111_opy_()
  sys.exit(1)
def bstack1ll11111ll_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1l1111ll11_opy_(message, True)
  atexit.unregister(bstack11lll11l1_opy_)
  bstack11111l111_opy_()
  sys.exit(1)
def bstack11l1l11l1l_opy_():
  global CONFIG
  global bstack11l1ll1111_opy_
  global bstack111llll1l_opy_
  global bstack1l1l11lll_opy_
  CONFIG = bstack1lll111lll_opy_()
  load_dotenv(CONFIG.get(bstack1l11l11_opy_ (u"ࠨࡧࡱࡺࡋ࡯࡬ࡦࠩਭ")))
  bstack1l1l1l1ll_opy_()
  bstack1l11lll1ll_opy_()
  CONFIG = bstack11l1lll1_opy_(CONFIG)
  update(CONFIG, bstack111llll1l_opy_)
  update(CONFIG, bstack11l1ll1111_opy_)
  if not cli.is_enabled(CONFIG):
    CONFIG = bstack11lll1l1l_opy_(CONFIG)
  bstack1l1l11lll_opy_ = bstack1ll111llll_opy_(CONFIG)
  os.environ[bstack1l11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬਮ")] = bstack1l1l11lll_opy_.__str__().lower()
  bstack11l11llll_opy_.bstack11l11ll1_opy_(bstack1l11l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫਯ"), bstack1l1l11lll_opy_)
  if (bstack1l11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧਰ") in CONFIG and bstack1l11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ਱") in bstack11l1ll1111_opy_) or (
          bstack1l11l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩਲ") in CONFIG and bstack1l11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪਲ਼") not in bstack111llll1l_opy_):
    if os.getenv(bstack1l11l11_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬ਴")):
      CONFIG[bstack1l11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫਵ")] = os.getenv(bstack1l11l11_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧਸ਼"))
    else:
      if not CONFIG.get(bstack1l11l11_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠢ਷"), bstack1l11l11_opy_ (u"ࠧࠨਸ")) in bstack1l11l11l1_opy_:
        bstack1ll1l1l111_opy_()
  elif (bstack1l11l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩਹ") not in CONFIG and bstack1l11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ਺") in CONFIG) or (
          bstack1l11l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ਻") in bstack111llll1l_opy_ and bstack1l11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩ਼ࠬ") not in bstack11l1ll1111_opy_):
    del (CONFIG[bstack1l11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ਽")])
  if bstack11lllllll_opy_(CONFIG):
    bstack11l11l1l11_opy_(bstack111l11111_opy_)
  Config.bstack11l111llll_opy_().bstack11l11ll1_opy_(bstack1l11l11_opy_ (u"ࠦࡺࡹࡥࡳࡐࡤࡱࡪࠨਾ"), CONFIG[bstack1l11l11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧਿ")])
  bstack1llll11l11_opy_()
  bstack1llll11111_opy_()
  if bstack1ll111111_opy_ and not CONFIG.get(bstack1l11l11_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠤੀ"), bstack1l11l11_opy_ (u"ࠢࠣੁ")) in bstack1l11l11l1_opy_:
    CONFIG[bstack1l11l11_opy_ (u"ࠨࡣࡳࡴࠬੂ")] = bstack111ll1ll_opy_(CONFIG)
    logger.info(bstack1lll1l11ll_opy_.format(CONFIG[bstack1l11l11_opy_ (u"ࠩࡤࡴࡵ࠭੃")]))
  if not bstack1l1l11lll_opy_:
    CONFIG[bstack1l11l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭੄")] = [{}]
def bstack111ll11l_opy_(config, bstack1ll111ll11_opy_):
  global CONFIG
  global bstack1ll111111_opy_
  CONFIG = config
  bstack1ll111111_opy_ = bstack1ll111ll11_opy_
def bstack1llll11111_opy_():
  global CONFIG
  global bstack1ll111111_opy_
  if bstack1l11l11_opy_ (u"ࠫࡦࡶࡰࠨ੅") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1ll11111ll_opy_(e, bstack1lll11111_opy_)
    bstack1ll111111_opy_ = True
    bstack11l11llll_opy_.bstack11l11ll1_opy_(bstack1l11l11_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ੆"), True)
def bstack111ll1ll_opy_(config):
  bstack11lllll11l_opy_ = bstack1l11l11_opy_ (u"࠭ࠧੇ")
  app = config[bstack1l11l11_opy_ (u"ࠧࡢࡲࡳࠫੈ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack111111lll_opy_:
      if os.path.exists(app):
        bstack11lllll11l_opy_ = bstack1l1llll1_opy_(config, app)
      elif bstack1l1l1l111l_opy_(app):
        bstack11lllll11l_opy_ = app
      else:
        bstack11l11l1l11_opy_(bstack11111ll1_opy_.format(app))
    else:
      if bstack1l1l1l111l_opy_(app):
        bstack11lllll11l_opy_ = app
      elif os.path.exists(app):
        bstack11lllll11l_opy_ = bstack1l1llll1_opy_(app)
      else:
        bstack11l11l1l11_opy_(bstack11llll11l_opy_)
  else:
    if len(app) > 2:
      bstack11l11l1l11_opy_(bstack11111l11_opy_)
    elif len(app) == 2:
      if bstack1l11l11_opy_ (u"ࠨࡲࡤࡸ࡭࠭੉") in app and bstack1l11l11_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ੊") in app:
        if os.path.exists(app[bstack1l11l11_opy_ (u"ࠪࡴࡦࡺࡨࠨੋ")]):
          bstack11lllll11l_opy_ = bstack1l1llll1_opy_(config, app[bstack1l11l11_opy_ (u"ࠫࡵࡧࡴࡩࠩੌ")], app[bstack1l11l11_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨ੍")])
        else:
          bstack11l11l1l11_opy_(bstack11111ll1_opy_.format(app))
      else:
        bstack11l11l1l11_opy_(bstack11111l11_opy_)
    else:
      for key in app:
        if key in bstack11ll1l11_opy_:
          if key == bstack1l11l11_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ੎"):
            if os.path.exists(app[key]):
              bstack11lllll11l_opy_ = bstack1l1llll1_opy_(config, app[key])
            else:
              bstack11l11l1l11_opy_(bstack11111ll1_opy_.format(app))
          else:
            bstack11lllll11l_opy_ = app[key]
        else:
          bstack11l11l1l11_opy_(bstack1lll1l11_opy_)
  return bstack11lllll11l_opy_
def bstack1l1l1l111l_opy_(bstack11lllll11l_opy_):
  import re
  bstack1ll111lll1_opy_ = re.compile(bstack1l11l11_opy_ (u"ࡲࠣࡠ࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯ࠪࠢ੏"))
  bstack1lll1lllll_opy_ = re.compile(bstack1l11l11_opy_ (u"ࡳࠤࡡ࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰࠯࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭ࠨࠧ੐"))
  if bstack1l11l11_opy_ (u"ࠩࡥࡷ࠿࠵࠯ࠨੑ") in bstack11lllll11l_opy_ or re.fullmatch(bstack1ll111lll1_opy_, bstack11lllll11l_opy_) or re.fullmatch(bstack1lll1lllll_opy_, bstack11lllll11l_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack1l1l1l1111_opy_, stage=STAGE.bstack1lll11l1_opy_, bstack1l1lll11l_opy_=bstack1lllll1ll_opy_)
def bstack1l1llll1_opy_(config, path, bstack111ll1lll_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1l11l11_opy_ (u"ࠪࡶࡧ࠭੒")).read()).hexdigest()
  bstack1111l111l_opy_ = bstack1lllll11_opy_(md5_hash)
  bstack11lllll11l_opy_ = None
  if bstack1111l111l_opy_:
    logger.info(bstack1ll1ll11_opy_.format(bstack1111l111l_opy_, md5_hash))
    return bstack1111l111l_opy_
  bstack1l11l11111_opy_ = datetime.datetime.now()
  bstack111l11l1_opy_ = MultipartEncoder(
    fields={
      bstack1l11l11_opy_ (u"ࠫ࡫࡯࡬ࡦࠩ੓"): (os.path.basename(path), open(os.path.abspath(path), bstack1l11l11_opy_ (u"ࠬࡸࡢࠨ੔")), bstack1l11l11_opy_ (u"࠭ࡴࡦࡺࡷ࠳ࡵࡲࡡࡪࡰࠪ੕")),
      bstack1l11l11_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪ੖"): bstack111ll1lll_opy_
    }
  )
  response = requests.post(bstack1l11ll11ll_opy_, data=bstack111l11l1_opy_,
                           headers={bstack1l11l11_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ੗"): bstack111l11l1_opy_.content_type},
                           auth=(config[bstack1l11l11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ੘")], config[bstack1l11l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ਖ਼")]))
  try:
    res = json.loads(response.text)
    bstack11lllll11l_opy_ = res[bstack1l11l11_opy_ (u"ࠫࡦࡶࡰࡠࡷࡵࡰࠬਗ਼")]
    logger.info(bstack1l11lll11_opy_.format(bstack11lllll11l_opy_))
    bstack1lll1ll1l_opy_(md5_hash, bstack11lllll11l_opy_)
    cli.bstack1l1l1l1l1l_opy_(bstack1l11l11_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽ࡹࡵࡲ࡯ࡢࡦࡢࡥࡵࡶࠢਜ਼"), datetime.datetime.now() - bstack1l11l11111_opy_)
  except ValueError as err:
    bstack11l11l1l11_opy_(bstack1ll11l1ll1_opy_.format(str(err)))
  return bstack11lllll11l_opy_
def bstack1llll11l11_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack11llll1ll1_opy_
  bstack1l11l1l1l1_opy_ = 1
  bstack111l1l1l1_opy_ = 1
  if bstack1l11l11_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ੜ") in CONFIG:
    bstack111l1l1l1_opy_ = CONFIG[bstack1l11l11_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ੝")]
  else:
    bstack111l1l1l1_opy_ = bstack11l1llll11_opy_(framework_name, args) or 1
  if bstack1l11l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫਫ਼") in CONFIG:
    bstack1l11l1l1l1_opy_ = len(CONFIG[bstack1l11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ੟")])
  bstack11llll1ll1_opy_ = int(bstack111l1l1l1_opy_) * int(bstack1l11l1l1l1_opy_)
def bstack11l1llll11_opy_(framework_name, args):
  if framework_name == bstack1l11ll1l_opy_ and args and bstack1l11l11_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨ੠") in args:
      bstack111111l1_opy_ = args.index(bstack1l11l11_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩ੡"))
      return int(args[bstack111111l1_opy_ + 1]) or 1
  return 1
def bstack1lllll11_opy_(md5_hash):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l11l11_opy_ (u"ࠬ࡬ࡩ࡭ࡧ࡯ࡳࡨࡱࠠ࡯ࡱࡷࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠬࠡࡷࡶ࡭ࡳ࡭ࠠࡣࡣࡶ࡭ࡨࠦࡦࡪ࡮ࡨࠤࡴࡶࡥࡳࡣࡷ࡭ࡴࡴࡳࠨ੢"))
    bstack11ll1l1lll_opy_ = os.path.join(os.path.expanduser(bstack1l11l11_opy_ (u"࠭ࡾࠨ੣")), bstack1l11l11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ੤"), bstack1l11l11_opy_ (u"ࠨࡣࡳࡴ࡚ࡶ࡬ࡰࡣࡧࡑࡉ࠻ࡈࡢࡵ࡫࠲࡯ࡹ࡯࡯ࠩ੥"))
    if os.path.exists(bstack11ll1l1lll_opy_):
      try:
        bstack1l111lll1l_opy_ = json.load(open(bstack11ll1l1lll_opy_, bstack1l11l11_opy_ (u"ࠩࡵࡦࠬ੦")))
        if md5_hash in bstack1l111lll1l_opy_:
          bstack11l1l11lll_opy_ = bstack1l111lll1l_opy_[md5_hash]
          bstack11llllll1l_opy_ = datetime.datetime.now()
          bstack11l1l1111_opy_ = datetime.datetime.strptime(bstack11l1l11lll_opy_[bstack1l11l11_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭੧")], bstack1l11l11_opy_ (u"ࠫࠪࡪ࠯ࠦ࡯࠲ࠩ࡞ࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨ੨"))
          if (bstack11llllll1l_opy_ - bstack11l1l1111_opy_).days > 30:
            return None
          elif version.parse(str(__version__)) > version.parse(bstack11l1l11lll_opy_[bstack1l11l11_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ੩")]):
            return None
          return bstack11l1l11lll_opy_[bstack1l11l11_opy_ (u"࠭ࡩࡥࠩ੪")]
      except Exception as e:
        logger.debug(bstack1l11l11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡲࡦࡣࡧ࡭ࡳ࡭ࠠࡎࡆ࠸ࠤ࡭ࡧࡳࡩࠢࡩ࡭ࡱ࡫࠺ࠡࡽࢀࠫ੫").format(str(e)))
    return None
  bstack11ll1l1lll_opy_ = os.path.join(os.path.expanduser(bstack1l11l11_opy_ (u"ࠨࢀࠪ੬")), bstack1l11l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ੭"), bstack1l11l11_opy_ (u"ࠪࡥࡵࡶࡕࡱ࡮ࡲࡥࡩࡓࡄ࠶ࡊࡤࡷ࡭࠴ࡪࡴࡱࡱࠫ੮"))
  lock_file = bstack11ll1l1lll_opy_ + bstack1l11l11_opy_ (u"ࠫ࠳ࡲ࡯ࡤ࡭ࠪ੯")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack11ll1l1lll_opy_):
        with open(bstack11ll1l1lll_opy_, bstack1l11l11_opy_ (u"ࠬࡸࠧੰ")) as f:
          content = f.read().strip()
          if content:
            bstack1l111lll1l_opy_ = json.loads(content)
            if md5_hash in bstack1l111lll1l_opy_:
              bstack11l1l11lll_opy_ = bstack1l111lll1l_opy_[md5_hash]
              bstack11llllll1l_opy_ = datetime.datetime.now()
              bstack11l1l1111_opy_ = datetime.datetime.strptime(bstack11l1l11lll_opy_[bstack1l11l11_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩੱ")], bstack1l11l11_opy_ (u"ࠧࠦࡦ࠲ࠩࡲ࠵࡚ࠥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫੲ"))
              if (bstack11llllll1l_opy_ - bstack11l1l1111_opy_).days > 30:
                return None
              elif version.parse(str(__version__)) > version.parse(bstack11l1l11lll_opy_[bstack1l11l11_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ੳ")]):
                return None
              return bstack11l1l11lll_opy_[bstack1l11l11_opy_ (u"ࠩ࡬ࡨࠬੴ")]
      return None
  except Exception as e:
    logger.debug(bstack1l11l11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡺ࡭ࡹ࡮ࠠࡧ࡫࡯ࡩࠥࡲ࡯ࡤ࡭࡬ࡲ࡬ࠦࡦࡰࡴࠣࡑࡉ࠻ࠠࡩࡣࡶ࡬࠿ࠦࡻࡾࠩੵ").format(str(e)))
    return None
def bstack1lll1ll1l_opy_(md5_hash, bstack11lllll11l_opy_):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l11l11_opy_ (u"ࠫ࡫࡯࡬ࡦ࡮ࡲࡧࡰࠦ࡮ࡰࡶࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪ࠲ࠠࡶࡵ࡬ࡲ࡬ࠦࡢࡢࡵ࡬ࡧࠥ࡬ࡩ࡭ࡧࠣࡳࡵ࡫ࡲࡢࡶ࡬ࡳࡳࡹࠧ੶"))
    bstack1l111l1l_opy_ = os.path.join(os.path.expanduser(bstack1l11l11_opy_ (u"ࠬࢄࠧ੷")), bstack1l11l11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭੸"))
    if not os.path.exists(bstack1l111l1l_opy_):
      os.makedirs(bstack1l111l1l_opy_)
    bstack11ll1l1lll_opy_ = os.path.join(os.path.expanduser(bstack1l11l11_opy_ (u"ࠧࡿࠩ੹")), bstack1l11l11_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ੺"), bstack1l11l11_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪ੻"))
    bstack111lllll11_opy_ = {
      bstack1l11l11_opy_ (u"ࠪ࡭ࡩ࠭੼"): bstack11lllll11l_opy_,
      bstack1l11l11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ੽"): datetime.datetime.strftime(datetime.datetime.now(), bstack1l11l11_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩ੾")),
      bstack1l11l11_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ੿"): str(__version__)
    }
    try:
      bstack1l111lll1l_opy_ = {}
      if os.path.exists(bstack11ll1l1lll_opy_):
        bstack1l111lll1l_opy_ = json.load(open(bstack11ll1l1lll_opy_, bstack1l11l11_opy_ (u"ࠧࡳࡤࠪ઀")))
      bstack1l111lll1l_opy_[md5_hash] = bstack111lllll11_opy_
      with open(bstack11ll1l1lll_opy_, bstack1l11l11_opy_ (u"ࠣࡹ࠮ࠦઁ")) as outfile:
        json.dump(bstack1l111lll1l_opy_, outfile)
    except Exception as e:
      logger.debug(bstack1l11l11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡷࡳࡨࡦࡺࡩ࡯ࡩࠣࡑࡉ࠻ࠠࡩࡣࡶ࡬ࠥ࡬ࡩ࡭ࡧ࠽ࠤࢀࢃࠧં").format(str(e)))
    return
  bstack1l111l1l_opy_ = os.path.join(os.path.expanduser(bstack1l11l11_opy_ (u"ࠪࢂࠬઃ")), bstack1l11l11_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ઄"))
  if not os.path.exists(bstack1l111l1l_opy_):
    os.makedirs(bstack1l111l1l_opy_)
  bstack11ll1l1lll_opy_ = os.path.join(os.path.expanduser(bstack1l11l11_opy_ (u"ࠬࢄࠧઅ")), bstack1l11l11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭આ"), bstack1l11l11_opy_ (u"ࠧࡢࡲࡳ࡙ࡵࡲ࡯ࡢࡦࡐࡈ࠺ࡎࡡࡴࡪ࠱࡮ࡸࡵ࡮ࠨઇ"))
  lock_file = bstack11ll1l1lll_opy_ + bstack1l11l11_opy_ (u"ࠨ࠰࡯ࡳࡨࡱࠧઈ")
  bstack111lllll11_opy_ = {
    bstack1l11l11_opy_ (u"ࠩ࡬ࡨࠬઉ"): bstack11lllll11l_opy_,
    bstack1l11l11_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ઊ"): datetime.datetime.strftime(datetime.datetime.now(), bstack1l11l11_opy_ (u"ࠫࠪࡪ࠯ࠦ࡯࠲ࠩ࡞ࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨઋ")),
    bstack1l11l11_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪઌ"): str(__version__)
  }
  try:
    with FileLock(lock_file, timeout=10):
      bstack1l111lll1l_opy_ = {}
      if os.path.exists(bstack11ll1l1lll_opy_):
        with open(bstack11ll1l1lll_opy_, bstack1l11l11_opy_ (u"࠭ࡲࠨઍ")) as f:
          content = f.read().strip()
          if content:
            bstack1l111lll1l_opy_ = json.loads(content)
      bstack1l111lll1l_opy_[md5_hash] = bstack111lllll11_opy_
      with open(bstack11ll1l1lll_opy_, bstack1l11l11_opy_ (u"ࠢࡸࠤ઎")) as outfile:
        json.dump(bstack1l111lll1l_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1l11l11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡸ࡫ࡷ࡬ࠥ࡬ࡩ࡭ࡧࠣࡰࡴࡩ࡫ࡪࡰࡪࠤ࡫ࡵࡲࠡࡏࡇ࠹ࠥ࡮ࡡࡴࡪࠣࡹࡵࡪࡡࡵࡧ࠽ࠤࢀࢃࠧએ").format(str(e)))
def bstack1ll1l1ll_opy_(self):
  return
def bstack1111ll1ll_opy_(self):
  return
def bstack1l1ll111_opy_():
  global bstack1lllllllll_opy_
  bstack1lllllllll_opy_ = True
@measure(event_name=EVENTS.bstack1l11l11l1l_opy_, stage=STAGE.bstack1lll11l1_opy_, bstack1l1lll11l_opy_=bstack1lllll1ll_opy_)
def bstack1l1ll1ll1_opy_(self):
  global bstack1ll1l111ll_opy_
  global bstack11111ll11_opy_
  global bstack11ll1l1l1l_opy_
  try:
    if bstack1l11l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩઐ") in bstack1ll1l111ll_opy_ and self.session_id != None and bstack1l111ll111_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧઑ"), bstack1l11l11_opy_ (u"ࠫࠬ઒")) != bstack1l11l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ઓ"):
      bstack11l1l111ll_opy_ = bstack1l11l11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ઔ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1l11l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧક")
      if bstack11l1l111ll_opy_ == bstack1l11l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨખ"):
        bstack1l1l1l111_opy_(logger)
      if self != None:
        bstack1l1l11l1ll_opy_(self, bstack11l1l111ll_opy_, bstack1l11l11_opy_ (u"ࠩ࠯ࠤࠬગ").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack1l11l11_opy_ (u"ࠪࠫઘ")
    if bstack1l11l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫઙ") in bstack1ll1l111ll_opy_ and getattr(threading.current_thread(), bstack1l11l11_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫચ"), None):
      bstack1l111l11l1_opy_.bstack1ll1l111_opy_(self, bstack1lllll1l1l_opy_, logger, wait=True)
    if bstack1l11l11_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭છ") in bstack1ll1l111ll_opy_:
      if not threading.currentThread().behave_test_status:
        bstack1l1l11l1ll_opy_(self, bstack1l11l11_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢજ"))
      bstack1l1l111l_opy_.bstack1l111l111_opy_(self)
  except Exception as e:
    logger.debug(bstack1l11l11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࠤઝ") + str(e))
  bstack11ll1l1l1l_opy_(self)
  self.session_id = None
def bstack11ll11llll_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack1lll111ll_opy_
    global bstack1ll1l111ll_opy_
    command_executor = kwargs.get(bstack1l11l11_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠬઞ"), bstack1l11l11_opy_ (u"ࠪࠫટ"))
    bstack111ll1l1l_opy_ = False
    if type(command_executor) == str and bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧઠ") in command_executor:
      bstack111ll1l1l_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨડ") in str(getattr(command_executor, bstack1l11l11_opy_ (u"࠭࡟ࡶࡴ࡯ࠫઢ"), bstack1l11l11_opy_ (u"ࠧࠨણ"))):
      bstack111ll1l1l_opy_ = True
    else:
      kwargs = bstack1ll1ll1l11_opy_.bstack11l1ll1l1_opy_(bstack11lll1ll1_opy_=kwargs, config=CONFIG)
      return bstack1lll1l1ll_opy_(self, *args, **kwargs)
    if bstack111ll1l1l_opy_:
      bstack1lll11l111_opy_ = bstack11111l1l_opy_.bstack1lllllll1l_opy_(CONFIG, bstack1ll1l111ll_opy_)
      if kwargs.get(bstack1l11l11_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩત")):
        kwargs[bstack1l11l11_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪથ")] = bstack1lll111ll_opy_(kwargs[bstack1l11l11_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫદ")], bstack1ll1l111ll_opy_, CONFIG, bstack1lll11l111_opy_)
      elif kwargs.get(bstack1l11l11_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫધ")):
        kwargs[bstack1l11l11_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬન")] = bstack1lll111ll_opy_(kwargs[bstack1l11l11_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭઩")], bstack1ll1l111ll_opy_, CONFIG, bstack1lll11l111_opy_)
  except Exception as e:
    logger.error(bstack1l11l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩࡧࡱࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡕࡇࡏࠥࡩࡡࡱࡵ࠽ࠤࢀࢃࠢપ").format(str(e)))
  return bstack1lll1l1ll_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack1lll11lll_opy_, stage=STAGE.bstack1lll11l1_opy_, bstack1l1lll11l_opy_=bstack1lllll1ll_opy_)
def bstack11lll1l111_opy_(self, command_executor=bstack1l11l11_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰࠳࠵࠻࠳࠶࠮࠱࠰࠴࠾࠹࠺࠴࠵ࠤફ"), *args, **kwargs):
  global bstack11111ll11_opy_
  global bstack111lll1l1_opy_
  bstack1111l111_opy_ = bstack11ll11llll_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack1l1lllll1l_opy_.on():
    return bstack1111l111_opy_
  try:
    logger.debug(bstack1l11l11_opy_ (u"ࠩࡆࡳࡲࡳࡡ࡯ࡦࠣࡉࡽ࡫ࡣࡶࡶࡲࡶࠥࡽࡨࡦࡰࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡩࡴࠢࡩࡥࡱࡹࡥࠡ࠯ࠣࡿࢂ࠭બ").format(str(command_executor)))
    logger.debug(bstack1l11l11_opy_ (u"ࠪࡌࡺࡨࠠࡖࡔࡏࠤ࡮ࡹࠠ࠮ࠢࡾࢁࠬભ").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧમ") in command_executor._url:
      bstack11l11llll_opy_.bstack11l11ll1_opy_(bstack1l11l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ય"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack1l11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩર") in command_executor):
    bstack11l11llll_opy_.bstack11l11ll1_opy_(bstack1l11l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ઱"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1l1l1lll1l_opy_ = getattr(threading.current_thread(), bstack1l11l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡕࡧࡶࡸࡒ࡫ࡴࡢࠩલ"), None)
  bstack111l1111_opy_ = {}
  if self.capabilities is not None:
    bstack111l1111_opy_[bstack1l11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡲࡦࡳࡥࠨળ")] = self.capabilities.get(bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ઴"))
    bstack111l1111_opy_[bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭વ")] = self.capabilities.get(bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭શ"))
    bstack111l1111_opy_[bstack1l11l11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡥ࡯ࡱࡶ࡬ࡳࡳࡹࠧષ")] = self.capabilities.get(bstack1l11l11_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬસ"))
  if CONFIG.get(bstack1l11l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨહ"), False) and bstack1ll1ll1l11_opy_.bstack1llll111l_opy_(bstack111l1111_opy_):
    threading.current_thread().a11yPlatform = True
  if bstack1l11l11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ઺") in bstack1ll1l111ll_opy_ or bstack1l11l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ઻") in bstack1ll1l111ll_opy_:
    bstack11ll111ll1_opy_.bstack11ll1l11l_opy_(self)
  if bstack1l11l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ઼ࠫ") in bstack1ll1l111ll_opy_ and bstack1l1l1lll1l_opy_ and bstack1l1l1lll1l_opy_.get(bstack1l11l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬઽ"), bstack1l11l11_opy_ (u"࠭ࠧા")) == bstack1l11l11_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨિ"):
    bstack11ll111ll1_opy_.bstack11ll1l11l_opy_(self)
  bstack11111ll11_opy_ = self.session_id
  with bstack1l1lllllll_opy_:
    bstack111lll1l1_opy_.append(self)
  return bstack1111l111_opy_
def bstack1lll1l1111_opy_(args):
  return bstack1l11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠩી") in str(args)
def bstack1l1l1ll11_opy_(self, driver_command, *args, **kwargs):
  global bstack1ll11l1111_opy_
  global bstack11l1l1l1l_opy_
  bstack1lll1l11l1_opy_ = bstack1l111ll111_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ુ"), None) and bstack1l111ll111_opy_(
          threading.current_thread(), bstack1l11l11_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩૂ"), None)
  bstack111l1l11l_opy_ = bstack1l111ll111_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫૃ"), None) and bstack1l111ll111_opy_(
          threading.current_thread(), bstack1l11l11_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧૄ"), None)
  bstack1111lllll_opy_ = getattr(self, bstack1l11l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭ૅ"), None) != None and getattr(self, bstack1l11l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧ૆"), None) == True
  if not bstack11l1l1l1l_opy_ and bstack1l11l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨે") in CONFIG and CONFIG[bstack1l11l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩૈ")] == True and bstack11l1ll111l_opy_.bstack11ll111111_opy_(driver_command) and (bstack1111lllll_opy_ or bstack1lll1l11l1_opy_ or bstack111l1l11l_opy_) and not bstack1lll1l1111_opy_(args):
    try:
      bstack11l1l1l1l_opy_ = True
      logger.debug(bstack1l11l11_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡾࢁࠬૉ").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack1l11l11_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡧࡵࡪࡴࡸ࡭ࠡࡵࡦࡥࡳࠦࡻࡾࠩ૊").format(str(err)))
    bstack11l1l1l1l_opy_ = False
  response = bstack1ll11l1111_opy_(self, driver_command, *args, **kwargs)
  if (bstack1l11l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫો") in str(bstack1ll1l111ll_opy_).lower() or bstack1l11l11_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ૌ") in str(bstack1ll1l111ll_opy_).lower()) and bstack1l1lllll1l_opy_.on():
    try:
      if driver_command == bstack1l11l11_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷ્ࠫ"):
        bstack11ll111ll1_opy_.bstack11ll1lll11_opy_({
            bstack1l11l11_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧ૎"): response[bstack1l11l11_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨ૏")],
            bstack1l11l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪૐ"): bstack11ll111ll1_opy_.current_test_uuid() if bstack11ll111ll1_opy_.current_test_uuid() else bstack1l1lllll1l_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
@measure(event_name=EVENTS.bstack1l1l11ll11_opy_, stage=STAGE.bstack1lll11l1_opy_, bstack1l1lll11l_opy_=bstack1lllll1ll_opy_)
def bstack1l1l111lll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack11111ll11_opy_
  global bstack1l1llll1ll_opy_
  global bstack1lllll1ll_opy_
  global bstack1ll1l1l1l1_opy_
  global bstack1l11111lll_opy_
  global bstack1ll1l111ll_opy_
  global bstack1lll1l1ll_opy_
  global bstack111lll1l1_opy_
  global bstack1l1l11l11_opy_
  global bstack1lllll1l1l_opy_
  if os.getenv(bstack1l11l11_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ૑")) is not None and bstack1ll1ll1l11_opy_.bstack11l11l11l_opy_(CONFIG) is None:
    CONFIG[bstack1l11l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ૒")] = True
  CONFIG[bstack1l11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ૓")] = str(bstack1ll1l111ll_opy_) + str(__version__)
  bstack1ll1l1l11l_opy_ = os.environ[bstack1l11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ૔")]
  bstack1lll11l111_opy_ = bstack11111l1l_opy_.bstack1lllllll1l_opy_(CONFIG, bstack1ll1l111ll_opy_)
  CONFIG[bstack1l11l11_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ૕")] = bstack1ll1l1l11l_opy_
  CONFIG[bstack1l11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ૖")] = bstack1lll11l111_opy_
  if CONFIG.get(bstack1l11l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ૗"),bstack1l11l11_opy_ (u"ࠫࠬ૘")) and bstack1l11l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ૙") in bstack1ll1l111ll_opy_:
    CONFIG[bstack1l11l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭૚")].pop(bstack1l11l11_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬ૛"), None)
    CONFIG[bstack1l11l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ૜")].pop(bstack1l11l11_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ૝"), None)
  command_executor = bstack1l11ll1lll_opy_()
  logger.debug(bstack11ll1l111_opy_.format(command_executor))
  proxy = bstack1lll1l1ll1_opy_(CONFIG, proxy)
  bstack11lll1l11l_opy_ = 0 if bstack1l1llll1ll_opy_ < 0 else bstack1l1llll1ll_opy_
  try:
    if bstack1ll1l1l1l1_opy_ is True:
      bstack11lll1l11l_opy_ = int(multiprocessing.current_process().name)
    elif bstack1l11111lll_opy_ is True:
      bstack11lll1l11l_opy_ = int(threading.current_thread().name)
  except:
    bstack11lll1l11l_opy_ = 0
  bstack11l1ll1l1l_opy_ = bstack11l11111l_opy_(CONFIG, bstack11lll1l11l_opy_)
  logger.debug(bstack1ll1ll11l1_opy_.format(str(bstack11l1ll1l1l_opy_)))
  if bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ૞") in CONFIG and bstack11lll11ll1_opy_(CONFIG[bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ૟")]):
    bstack11lll1l1ll_opy_(bstack11l1ll1l1l_opy_)
  if bstack1ll1ll1l11_opy_.bstack11l1111l1_opy_(CONFIG, bstack11lll1l11l_opy_) and bstack1ll1ll1l11_opy_.bstack1l111ll1ll_opy_(bstack11l1ll1l1l_opy_, options, desired_capabilities, CONFIG):
    threading.current_thread().a11yPlatform = True
    if (cli.accessibility is None or not cli.accessibility.is_enabled()):
      bstack1ll1ll1l11_opy_.set_capabilities(bstack11l1ll1l1l_opy_, CONFIG)
  if desired_capabilities:
    bstack1111l11l_opy_ = bstack11l1lll1_opy_(desired_capabilities)
    bstack1111l11l_opy_[bstack1l11l11_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬૠ")] = bstack1l11llllll_opy_(CONFIG)
    bstack11llll11_opy_ = bstack11l11111l_opy_(bstack1111l11l_opy_)
    if bstack11llll11_opy_:
      bstack11l1ll1l1l_opy_ = update(bstack11llll11_opy_, bstack11l1ll1l1l_opy_)
    desired_capabilities = None
  if options:
    bstack1lllll1l1_opy_(options, bstack11l1ll1l1l_opy_)
  if not options:
    options = bstack1lll1llll_opy_(bstack11l1ll1l1l_opy_)
  bstack1lllll1l1l_opy_ = CONFIG.get(bstack1l11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩૡ"))[bstack11lll1l11l_opy_]
  if proxy and bstack11l1l111_opy_() >= version.parse(bstack1l11l11_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧૢ")):
    options.proxy(proxy)
  if options and bstack11l1l111_opy_() >= version.parse(bstack1l11l11_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧૣ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack11l1l111_opy_() < version.parse(bstack1l11l11_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ૤")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack11l1ll1l1l_opy_)
  logger.info(bstack1ll111l1l_opy_)
  bstack1l1l11llll_opy_.end(EVENTS.bstack11ll1ll1l_opy_.value, EVENTS.bstack11ll1ll1l_opy_.value + bstack1l11l11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ૥"), EVENTS.bstack11ll1ll1l_opy_.value + bstack1l11l11_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ૦"), status=True, failure=None, test_name=bstack1lllll1ll_opy_)
  if bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡰࡳࡱࡩ࡭ࡱ࡫ࠧ૧") in kwargs:
    del kwargs[bstack1l11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡱࡴࡲࡪ࡮ࡲࡥࠨ૨")]
  try:
    if bstack11l1l111_opy_() >= version.parse(bstack1l11l11_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧ૩")):
      bstack1lll1l1ll_opy_(self, command_executor=command_executor,
                options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
    elif bstack11l1l111_opy_() >= version.parse(bstack1l11l11_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ૪")):
      bstack1lll1l1ll_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities, options=options,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11l1l111_opy_() >= version.parse(bstack1l11l11_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩ૫")):
      bstack1lll1l1ll_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    else:
      bstack1lll1l1ll_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive)
  except Exception as bstack11l1111l_opy_:
    logger.error(bstack1ll1l11ll_opy_.format(bstack1l11l11_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠩ૬"), str(bstack11l1111l_opy_)))
    raise bstack11l1111l_opy_
  if bstack1ll1ll1l11_opy_.bstack11l1111l1_opy_(CONFIG, bstack11lll1l11l_opy_) and bstack1ll1ll1l11_opy_.bstack1l111ll1ll_opy_(self.caps, options, desired_capabilities):
    if CONFIG[bstack1l11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭૭")][bstack1l11l11_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ૮")] == True:
      threading.current_thread().appA11yPlatform = True
      if cli.accessibility is None or not cli.accessibility.is_enabled():
        bstack1ll1ll1l11_opy_.set_capabilities(bstack11l1ll1l1l_opy_, CONFIG)
  try:
    bstack1l111lll_opy_ = bstack1l11l11_opy_ (u"࠭ࠧ૯")
    if bstack11l1l111_opy_() >= version.parse(bstack1l11l11_opy_ (u"ࠧ࠵࠰࠳࠲࠵ࡨ࠱ࠨ૰")):
      if self.caps is not None:
        bstack1l111lll_opy_ = self.caps.get(bstack1l11l11_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣ૱"))
    else:
      if self.capabilities is not None:
        bstack1l111lll_opy_ = self.capabilities.get(bstack1l11l11_opy_ (u"ࠤࡲࡴࡹ࡯࡭ࡢ࡮ࡋࡹࡧ࡛ࡲ࡭ࠤ૲"))
    if bstack1l111lll_opy_:
      bstack1l1l1ll11l_opy_(bstack1l111lll_opy_)
      if bstack11l1l111_opy_() <= version.parse(bstack1l11l11_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪ૳")):
        self.command_executor._url = bstack1l11l11_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧ૴") + bstack11l1ll111_opy_ + bstack1l11l11_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤ૵")
      else:
        self.command_executor._url = bstack1l11l11_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣ૶") + bstack1l111lll_opy_ + bstack1l11l11_opy_ (u"ࠢ࠰ࡹࡧ࠳࡭ࡻࡢࠣ૷")
      logger.debug(bstack11lllll111_opy_.format(bstack1l111lll_opy_))
    else:
      logger.debug(bstack1l1l11l11l_opy_.format(bstack1l11l11_opy_ (u"ࠣࡑࡳࡸ࡮ࡳࡡ࡭ࠢࡋࡹࡧࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠤ૸")))
  except Exception as e:
    logger.debug(bstack1l1l11l11l_opy_.format(e))
  if bstack1l11l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨૹ") in bstack1ll1l111ll_opy_:
    bstack1l111l1l11_opy_(bstack1l1llll1ll_opy_, bstack1l1l11l11_opy_)
  bstack11111ll11_opy_ = self.session_id
  if bstack1l11l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪૺ") in bstack1ll1l111ll_opy_ or bstack1l11l11_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫૻ") in bstack1ll1l111ll_opy_ or bstack1l11l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫૼ") in bstack1ll1l111ll_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack1l1l1lll1l_opy_ = getattr(threading.current_thread(), bstack1l11l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡚ࡥࡴࡶࡐࡩࡹࡧࠧ૽"), None)
  if bstack1l11l11_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ૾") in bstack1ll1l111ll_opy_ or bstack1l11l11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ૿") in bstack1ll1l111ll_opy_:
    bstack11ll111ll1_opy_.bstack11ll1l11l_opy_(self)
  if bstack1l11l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ଀") in bstack1ll1l111ll_opy_ and bstack1l1l1lll1l_opy_ and bstack1l1l1lll1l_opy_.get(bstack1l11l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪଁ"), bstack1l11l11_opy_ (u"ࠫࠬଂ")) == bstack1l11l11_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭ଃ"):
    bstack11ll111ll1_opy_.bstack11ll1l11l_opy_(self)
  with bstack1l1lllllll_opy_:
    bstack111lll1l1_opy_.append(self)
  if bstack1l11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ଄") in CONFIG and bstack1l11l11_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬଅ") in CONFIG[bstack1l11l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫଆ")][bstack11lll1l11l_opy_]:
    bstack1lllll1ll_opy_ = CONFIG[bstack1l11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬଇ")][bstack11lll1l11l_opy_][bstack1l11l11_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨଈ")]
  logger.debug(bstack11ll1l1ll_opy_.format(bstack11111ll11_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    from browserstack_sdk.__init__ import bstack111ll11l1_opy_
    def bstack111ll111l_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1llll1l111_opy_
      if(bstack1l11l11_opy_ (u"ࠦ࡮ࡴࡤࡦࡺ࠱࡮ࡸࠨଉ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1l11l11_opy_ (u"ࠬࢄࠧଊ")), bstack1l11l11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ଋ"), bstack1l11l11_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩଌ")), bstack1l11l11_opy_ (u"ࠨࡹࠪ଍")) as fp:
          fp.write(bstack1l11l11_opy_ (u"ࠤࠥ଎"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1l11l11_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧଏ")))):
          with open(args[1], bstack1l11l11_opy_ (u"ࠫࡷ࠭ଐ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1l11l11_opy_ (u"ࠬࡧࡳࡺࡰࡦࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦ࡟࡯ࡧࡺࡔࡦ࡭ࡥࠩࡥࡲࡲࡹ࡫ࡸࡵ࠮ࠣࡴࡦ࡭ࡥࠡ࠿ࠣࡺࡴ࡯ࡤࠡ࠲ࠬࠫ଑") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1llll1ll1l_opy_)
            if bstack1l11l11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ଒") in CONFIG and str(CONFIG[bstack1l11l11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫଓ")]).lower() != bstack1l11l11_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧଔ"):
                bstack1lll11l11_opy_ = bstack111ll11l1_opy_()
                bstack1lll111l1l_opy_ = bstack1l11l11_opy_ (u"ࠩࠪࠫࠏ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯ࠋࡥࡲࡲࡸࡺࠠࡣࡵࡷࡥࡨࡱ࡟ࡱࡣࡷ࡬ࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴࡟࠾ࠎࡨࡵ࡮ࡴࡶࠣࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࡝ࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠵ࡢࡁࠊࡤࡱࡱࡷࡹࠦࡰࡠ࡫ࡱࡨࡪࡾࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠵ࡡࡀࠐࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴ࡳ࡭࡫ࡦࡩ࠭࠶ࠬࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠶࠭ࡀࠐࡣࡰࡰࡶࡸࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭ࠣࡁࠥࡸࡥࡲࡷ࡬ࡶࡪ࠮ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦ࠮ࡁࠊࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮࡭ࡣࡸࡲࡨ࡮ࠠ࠾ࠢࡤࡷࡾࡴࡣࠡࠪ࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴࠫࠣࡁࡃࠦࡻࡼࠌࠣࠤࡱ࡫ࡴࠡࡥࡤࡴࡸࡁࠊࠡࠢࡷࡶࡾࠦࡻࡼࠌࠣࠤࠥࠦࡣࡢࡲࡶࠤࡂࠦࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠪ࠽ࠍࠤࠥࢃࡽࠡࡥࡤࡸࡨ࡮ࠠࠩࡧࡻ࠭ࠥࢁࡻࠋࠢࠣࠤࠥࡩ࡯࡯ࡵࡲࡰࡪ࠴ࡥࡳࡴࡲࡶ࠭ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠺ࠣ࠮ࠣࡩࡽ࠯࠻ࠋࠢࠣࢁࢂࠐࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡣࡺࡥ࡮ࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮ࡤࡱࡱࡲࡪࡩࡴࠩࡽࡾࠎࠥࠦࠠࠡࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸ࠿ࠦࠧࡼࡥࡧࡴ࡚ࡸ࡬ࡾࠩࠣ࠯ࠥ࡫࡮ࡤࡱࡧࡩ࡚ࡘࡉࡄࡱࡰࡴࡴࡴࡥ࡯ࡶࠫࡎࡘࡕࡎ࠯ࡵࡷࡶ࡮ࡴࡧࡪࡨࡼࠬࡨࡧࡰࡴࠫࠬ࠰ࠏࠦࠠࠡࠢ࠱࠲࠳ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷࠏࠦࠠࡾࡿࠬ࠿ࠏࢃࡽ࠼ࠌ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࠏ࠭ࠧࠨକ").format(bstack1lll11l11_opy_=bstack1lll11l11_opy_)
            lines.insert(1, bstack1lll111l1l_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1l11l11_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧଖ")), bstack1l11l11_opy_ (u"ࠫࡼ࠭ଗ")) as bstack1ll11l11_opy_:
              bstack1ll11l11_opy_.writelines(lines)
        CONFIG[bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧଘ")] = str(bstack1ll1l111ll_opy_) + str(__version__)
        bstack1ll1l1l11l_opy_ = os.environ[bstack1l11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫଙ")]
        bstack1lll11l111_opy_ = bstack11111l1l_opy_.bstack1lllllll1l_opy_(CONFIG, bstack1ll1l111ll_opy_)
        CONFIG[bstack1l11l11_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪଚ")] = bstack1ll1l1l11l_opy_
        CONFIG[bstack1l11l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪଛ")] = bstack1lll11l111_opy_
        bstack11lll1l11l_opy_ = 0 if bstack1l1llll1ll_opy_ < 0 else bstack1l1llll1ll_opy_
        try:
          if bstack1ll1l1l1l1_opy_ is True:
            bstack11lll1l11l_opy_ = int(multiprocessing.current_process().name)
          elif bstack1l11111lll_opy_ is True:
            bstack11lll1l11l_opy_ = int(threading.current_thread().name)
        except:
          bstack11lll1l11l_opy_ = 0
        CONFIG[bstack1l11l11_opy_ (u"ࠤࡸࡷࡪ࡝࠳ࡄࠤଜ")] = False
        CONFIG[bstack1l11l11_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤଝ")] = True
        bstack11l1ll1l1l_opy_ = bstack11l11111l_opy_(CONFIG, bstack11lll1l11l_opy_)
        logger.debug(bstack1ll1ll11l1_opy_.format(str(bstack11l1ll1l1l_opy_)))
        if CONFIG.get(bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨଞ")):
          bstack11lll1l1ll_opy_(bstack11l1ll1l1l_opy_)
        if bstack1l11l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨଟ") in CONFIG and bstack1l11l11_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫଠ") in CONFIG[bstack1l11l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଡ")][bstack11lll1l11l_opy_]:
          bstack1lllll1ll_opy_ = CONFIG[bstack1l11l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫଢ")][bstack11lll1l11l_opy_][bstack1l11l11_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧଣ")]
        args.append(os.path.join(os.path.expanduser(bstack1l11l11_opy_ (u"ࠪࢂࠬତ")), bstack1l11l11_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫଥ"), bstack1l11l11_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧଦ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack11l1ll1l1l_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1l11l11_opy_ (u"ࠨࡩ࡯ࡦࡨࡼࡤࡨࡳࡵࡣࡦ࡯࠳ࡰࡳࠣଧ"))
      bstack1llll1l111_opy_ = True
      return bstack11l11l111l_opy_(self, args, bufsize=bufsize, executable=executable,
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
  def bstack11111111l_opy_(self,
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
    global bstack1l1llll1ll_opy_
    global bstack1lllll1ll_opy_
    global bstack1ll1l1l1l1_opy_
    global bstack1l11111lll_opy_
    global bstack1ll1l111ll_opy_
    CONFIG[bstack1l11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩନ")] = str(bstack1ll1l111ll_opy_) + str(__version__)
    bstack1ll1l1l11l_opy_ = os.environ[bstack1l11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭଩")]
    bstack1lll11l111_opy_ = bstack11111l1l_opy_.bstack1lllllll1l_opy_(CONFIG, bstack1ll1l111ll_opy_)
    CONFIG[bstack1l11l11_opy_ (u"ࠩࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬପ")] = bstack1ll1l1l11l_opy_
    CONFIG[bstack1l11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬଫ")] = bstack1lll11l111_opy_
    bstack11lll1l11l_opy_ = 0 if bstack1l1llll1ll_opy_ < 0 else bstack1l1llll1ll_opy_
    try:
      if bstack1ll1l1l1l1_opy_ is True:
        bstack11lll1l11l_opy_ = int(multiprocessing.current_process().name)
      elif bstack1l11111lll_opy_ is True:
        bstack11lll1l11l_opy_ = int(threading.current_thread().name)
    except:
      bstack11lll1l11l_opy_ = 0
    CONFIG[bstack1l11l11_opy_ (u"ࠦ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥବ")] = True
    bstack11l1ll1l1l_opy_ = bstack11l11111l_opy_(CONFIG, bstack11lll1l11l_opy_)
    logger.debug(bstack1ll1ll11l1_opy_.format(str(bstack11l1ll1l1l_opy_)))
    if CONFIG.get(bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩଭ")):
      bstack11lll1l1ll_opy_(bstack11l1ll1l1l_opy_)
    if bstack1l11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩମ") in CONFIG and bstack1l11l11_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬଯ") in CONFIG[bstack1l11l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫର")][bstack11lll1l11l_opy_]:
      bstack1lllll1ll_opy_ = CONFIG[bstack1l11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ଱")][bstack11lll1l11l_opy_][bstack1l11l11_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨଲ")]
    import urllib
    import json
    if bstack1l11l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨଳ") in CONFIG and str(CONFIG[bstack1l11l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ଴")]).lower() != bstack1l11l11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬଵ"):
        bstack1l1l1lll1_opy_ = bstack111ll11l1_opy_()
        bstack1lll11l11_opy_ = bstack1l1l1lll1_opy_ + urllib.parse.quote(json.dumps(bstack11l1ll1l1l_opy_))
    else:
        bstack1lll11l11_opy_ = bstack1l11l11_opy_ (u"ࠧࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠩଶ") + urllib.parse.quote(json.dumps(bstack11l1ll1l1l_opy_))
    browser = self.connect(bstack1lll11l11_opy_)
    return browser
except Exception as e:
    pass
def bstack1llll1l1l1_opy_():
    global bstack1llll1l111_opy_
    global bstack1ll1l111ll_opy_
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack11llllll11_opy_
        global bstack11l11llll_opy_
        if not bstack1l1l11lll_opy_:
          global bstack111lll111_opy_
          if not bstack111lll111_opy_:
            from bstack_utils.helper import bstack1l1ll111l1_opy_, bstack1ll1llll_opy_, bstack1lllll1l11_opy_
            bstack111lll111_opy_ = bstack1l1ll111l1_opy_()
            bstack1ll1llll_opy_(bstack1ll1l111ll_opy_)
            bstack1lll11l111_opy_ = bstack11111l1l_opy_.bstack1lllllll1l_opy_(CONFIG, bstack1ll1l111ll_opy_)
            bstack11l11llll_opy_.bstack11l11ll1_opy_(bstack1l11l11_opy_ (u"ࠣࡒࡏࡅ࡞࡝ࡒࡊࡉࡋࡘࡤࡖࡒࡐࡆࡘࡇ࡙ࡥࡍࡂࡒࠥଷ"), bstack1lll11l111_opy_)
          BrowserType.connect = bstack11llllll11_opy_
          return
        BrowserType.launch = bstack11111111l_opy_
        bstack1llll1l111_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack111ll111l_opy_
      bstack1llll1l111_opy_ = True
    except Exception as e:
      pass
def bstack1lll1l1l11_opy_(context, bstack1l111l111l_opy_):
  try:
    context.page.evaluate(bstack1l11l11_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥସ"), bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠧହ")+ json.dumps(bstack1l111l111l_opy_) + bstack1l11l11_opy_ (u"ࠦࢂࢃࠢ଺"))
  except Exception as e:
    logger.debug(bstack1l11l11_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡼࡿ࠽ࠤࢀࢃࠢ଻").format(str(e), traceback.format_exc()))
def bstack1l11llll1_opy_(context, message, level):
  try:
    context.page.evaluate(bstack1l11l11_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃ଼ࠢ"), bstack1l11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬଽ") + json.dumps(message) + bstack1l11l11_opy_ (u"ࠨ࠮ࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠫା") + json.dumps(level) + bstack1l11l11_opy_ (u"ࠩࢀࢁࠬି"))
  except Exception as e:
    logger.debug(bstack1l11l11_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡡ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠣࡿࢂࡀࠠࡼࡿࠥୀ").format(str(e), traceback.format_exc()))
@measure(event_name=EVENTS.bstack1ll11lll1_opy_, stage=STAGE.bstack1lll11l1_opy_, bstack1l1lll11l_opy_=bstack1lllll1ll_opy_)
def bstack1llllllll1_opy_(self, url):
  global bstack1l111ll1l_opy_
  try:
    bstack11111llll_opy_(url)
  except Exception as err:
    logger.debug(bstack1l11111l1_opy_.format(str(err)))
  try:
    bstack1l111ll1l_opy_(self, url)
  except Exception as e:
    try:
      bstack1ll1l1111_opy_ = str(e)
      if any(err_msg in bstack1ll1l1111_opy_ for err_msg in bstack11lll11111_opy_):
        bstack11111llll_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1l11111l1_opy_.format(str(err)))
    raise e
def bstack1ll1l11l_opy_(self):
  global bstack11llllll1_opy_
  bstack11llllll1_opy_ = self
  return
def bstack11l11ll111_opy_(self):
  global bstack1ll1l1l1_opy_
  bstack1ll1l1l1_opy_ = self
  return
def bstack11llll1111_opy_(test_name, bstack1l1ll11l11_opy_):
  global CONFIG
  if percy.bstack1l1lll1ll_opy_() == bstack1l11l11_opy_ (u"ࠦࡹࡸࡵࡦࠤୁ"):
    bstack1ll11ll1l_opy_ = os.path.relpath(bstack1l1ll11l11_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack1ll11ll1l_opy_)
    bstack1l1lll11l_opy_ = suite_name + bstack1l11l11_opy_ (u"ࠧ࠳ࠢୂ") + test_name
    threading.current_thread().percySessionName = bstack1l1lll11l_opy_
def bstack11l111l1_opy_(self, test, *args, **kwargs):
  global bstack1111l1111_opy_
  test_name = None
  bstack1l1ll11l11_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1l1ll11l11_opy_ = str(test.source)
  bstack11llll1111_opy_(test_name, bstack1l1ll11l11_opy_)
  bstack1111l1111_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.bstack1l1111l1l_opy_, stage=STAGE.bstack1lll11l1_opy_, bstack1l1lll11l_opy_=bstack1lllll1ll_opy_)
def bstack1l11111111_opy_(driver, bstack1l1lll11l_opy_):
  if not bstack1l1llllll1_opy_ and bstack1l1lll11l_opy_:
      bstack1llllll1l_opy_ = {
          bstack1l11l11_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭ୃ"): bstack1l11l11_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨୄ"),
          bstack1l11l11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ୅"): {
              bstack1l11l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ୆"): bstack1l1lll11l_opy_
          }
      }
      bstack1ll11l11ll_opy_ = bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨେ").format(json.dumps(bstack1llllll1l_opy_))
      driver.execute_script(bstack1ll11l11ll_opy_)
  if bstack1llll111ll_opy_:
      bstack111l1llll_opy_ = {
          bstack1l11l11_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫୈ"): bstack1l11l11_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧ୉"),
          bstack1l11l11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ୊"): {
              bstack1l11l11_opy_ (u"ࠧࡥࡣࡷࡥࠬୋ"): bstack1l1lll11l_opy_ + bstack1l11l11_opy_ (u"ࠨࠢࡳࡥࡸࡹࡥࡥࠣࠪୌ"),
              bstack1l11l11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ୍"): bstack1l11l11_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨ୎")
          }
      }
      if bstack1llll111ll_opy_.status == bstack1l11l11_opy_ (u"ࠫࡕࡇࡓࡔࠩ୏"):
          bstack1lll1lll_opy_ = bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪ୐").format(json.dumps(bstack111l1llll_opy_))
          driver.execute_script(bstack1lll1lll_opy_)
          bstack1l1l11l1ll_opy_(driver, bstack1l11l11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭୑"))
      elif bstack1llll111ll_opy_.status == bstack1l11l11_opy_ (u"ࠧࡇࡃࡌࡐࠬ୒"):
          reason = bstack1l11l11_opy_ (u"ࠣࠤ୓")
          bstack11l1111111_opy_ = bstack1l1lll11l_opy_ + bstack1l11l11_opy_ (u"ࠩࠣࡪࡦ࡯࡬ࡦࡦࠪ୔")
          if bstack1llll111ll_opy_.message:
              reason = str(bstack1llll111ll_opy_.message)
              bstack11l1111111_opy_ = bstack11l1111111_opy_ + bstack1l11l11_opy_ (u"ࠪࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲ࠻ࠢࠪ୕") + reason
          bstack111l1llll_opy_[bstack1l11l11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧୖ")] = {
              bstack1l11l11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫୗ"): bstack1l11l11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ୘"),
              bstack1l11l11_opy_ (u"ࠧࡥࡣࡷࡥࠬ୙"): bstack11l1111111_opy_
          }
          bstack1lll1lll_opy_ = bstack1l11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭୚").format(json.dumps(bstack111l1llll_opy_))
          driver.execute_script(bstack1lll1lll_opy_)
          bstack1l1l11l1ll_opy_(driver, bstack1l11l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ୛"), reason)
          bstack1l111111l1_opy_(reason, str(bstack1llll111ll_opy_), str(bstack1l1llll1ll_opy_), logger)
@measure(event_name=EVENTS.bstack1l1l1111_opy_, stage=STAGE.bstack1lll11l1_opy_, bstack1l1lll11l_opy_=bstack1lllll1ll_opy_)
def bstack1l1llllll_opy_(driver, test):
  if percy.bstack1l1lll1ll_opy_() == bstack1l11l11_opy_ (u"ࠥࡸࡷࡻࡥࠣଡ଼") and percy.bstack1l1ll111l_opy_() == bstack1l11l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨଢ଼"):
      bstack1l1ll11l1_opy_ = bstack1l111ll111_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ୞"), None)
      bstack11l1lll1ll_opy_(driver, bstack1l1ll11l1_opy_, test)
  if (bstack1l111ll111_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪୟ"), None) and
      bstack1l111ll111_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ୠ"), None)) or (
      bstack1l111ll111_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨୡ"), None) and
      bstack1l111ll111_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫୢ"), None)):
      logger.info(bstack1l11l11_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠡࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡭ࡸࠦࡵ࡯ࡦࡨࡶࡼࡧࡹ࠯ࠢࠥୣ"))
      bstack1ll1ll1l11_opy_.bstack11l1l1lll_opy_(driver, name=test.name, path=test.source)
def bstack1ll1111111_opy_(test, bstack1l1lll11l_opy_):
    try:
      bstack1l11l11111_opy_ = datetime.datetime.now()
      data = {}
      if test:
        data[bstack1l11l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ୤")] = bstack1l1lll11l_opy_
      if bstack1llll111ll_opy_:
        if bstack1llll111ll_opy_.status == bstack1l11l11_opy_ (u"ࠬࡖࡁࡔࡕࠪ୥"):
          data[bstack1l11l11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭୦")] = bstack1l11l11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ୧")
        elif bstack1llll111ll_opy_.status == bstack1l11l11_opy_ (u"ࠨࡈࡄࡍࡑ࠭୨"):
          data[bstack1l11l11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ୩")] = bstack1l11l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ୪")
          if bstack1llll111ll_opy_.message:
            data[bstack1l11l11_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫ୫")] = str(bstack1llll111ll_opy_.message)
      user = CONFIG[bstack1l11l11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ୬")]
      key = CONFIG[bstack1l11l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ୭")]
      host = bstack11l111l11_opy_(cli.config, [bstack1l11l11_opy_ (u"ࠢࡢࡲ࡬ࡷࠧ୮"), bstack1l11l11_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧࠥ୯"), bstack1l11l11_opy_ (u"ࠤࡤࡴ࡮ࠨ୰")], bstack1l11l11_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠦୱ"))
      url = bstack1l11l11_opy_ (u"ࠫࢀࢃ࠯ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡶࡩࡸࡹࡩࡰࡰࡶ࠳ࢀࢃ࠮࡫ࡵࡲࡲࠬ୲").format(host, bstack11111ll11_opy_)
      headers = {
        bstack1l11l11_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫ୳"): bstack1l11l11_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ୴"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers, auth=(user, key))
        cli.bstack1l1l1l1l1l_opy_(bstack1l11l11_opy_ (u"ࠢࡩࡶࡷࡴ࠿ࡻࡰࡥࡣࡷࡩࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡸࡺࡡࡵࡷࡶࠦ୵"), datetime.datetime.now() - bstack1l11l11111_opy_)
    except Exception as e:
      logger.error(bstack11lll1l1l1_opy_.format(str(e)))
def bstack11ll111l11_opy_(test, bstack1l1lll11l_opy_):
  global CONFIG
  global bstack1ll1l1l1_opy_
  global bstack11llllll1_opy_
  global bstack11111ll11_opy_
  global bstack1llll111ll_opy_
  global bstack1lllll1ll_opy_
  global bstack11111111_opy_
  global bstack1lllll11ll_opy_
  global bstack1llll1ll11_opy_
  global bstack1ll111ll1_opy_
  global bstack111lll1l1_opy_
  global bstack1lllll1l1l_opy_
  global bstack1ll1ll111_opy_
  try:
    if not bstack11111ll11_opy_:
      with bstack1ll1ll111_opy_:
        bstack1llll1l1_opy_ = os.path.join(os.path.expanduser(bstack1l11l11_opy_ (u"ࠨࢀࠪ୶")), bstack1l11l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ୷"), bstack1l11l11_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬ୸"))
        if os.path.exists(bstack1llll1l1_opy_):
          with open(bstack1llll1l1_opy_, bstack1l11l11_opy_ (u"ࠫࡷ࠭୹")) as f:
            content = f.read().strip()
            if content:
              bstack11l1llll1_opy_ = json.loads(bstack1l11l11_opy_ (u"ࠧࢁࠢ୺") + content + bstack1l11l11_opy_ (u"࠭ࠢࡹࠤ࠽ࠤࠧࡿࠢࠨ୻") + bstack1l11l11_opy_ (u"ࠢࡾࠤ୼"))
              bstack11111ll11_opy_ = bstack11l1llll1_opy_.get(str(threading.get_ident()))
  except Exception as e:
    logger.debug(bstack1l11l11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡳࡧࡤࡨ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡌࡈࡸࠦࡦࡪ࡮ࡨ࠾ࠥ࠭୽") + str(e))
  if bstack111lll1l1_opy_:
    with bstack1l1lllllll_opy_:
      bstack1ll11lll_opy_ = bstack111lll1l1_opy_.copy()
    for driver in bstack1ll11lll_opy_:
      if bstack11111ll11_opy_ == driver.session_id:
        if test:
          bstack1l1llllll_opy_(driver, test)
        bstack1l11111111_opy_(driver, bstack1l1lll11l_opy_)
  elif bstack11111ll11_opy_:
    bstack1ll1111111_opy_(test, bstack1l1lll11l_opy_)
  if bstack1ll1l1l1_opy_:
    bstack1lllll11ll_opy_(bstack1ll1l1l1_opy_)
  if bstack11llllll1_opy_:
    bstack1llll1ll11_opy_(bstack11llllll1_opy_)
  if bstack1lllllllll_opy_:
    bstack1ll111ll1_opy_()
def bstack1l111l1ll1_opy_(self, test, *args, **kwargs):
  bstack1l1lll11l_opy_ = None
  if test:
    bstack1l1lll11l_opy_ = str(test.name)
  bstack11ll111l11_opy_(test, bstack1l1lll11l_opy_)
  bstack11111111_opy_(self, test, *args, **kwargs)
def bstack1lll111ll1_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1l1111l11_opy_
  global CONFIG
  global bstack111lll1l1_opy_
  global bstack11111ll11_opy_
  global bstack1ll1ll111_opy_
  bstack11l11lll_opy_ = None
  try:
    if bstack1l111ll111_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ୾"), None) or bstack1l111ll111_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ୿"), None):
      try:
        if not bstack11111ll11_opy_:
          bstack1llll1l1_opy_ = os.path.join(os.path.expanduser(bstack1l11l11_opy_ (u"ࠫࢃ࠭஀")), bstack1l11l11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ஁"), bstack1l11l11_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨஂ"))
          with bstack1ll1ll111_opy_:
            if os.path.exists(bstack1llll1l1_opy_):
              with open(bstack1llll1l1_opy_, bstack1l11l11_opy_ (u"ࠧࡳࠩஃ")) as f:
                content = f.read().strip()
                if content:
                  bstack11l1llll1_opy_ = json.loads(bstack1l11l11_opy_ (u"ࠣࡽࠥ஄") + content + bstack1l11l11_opy_ (u"ࠩࠥࡼࠧࡀࠠࠣࡻࠥࠫஅ") + bstack1l11l11_opy_ (u"ࠥࢁࠧஆ"))
                  bstack11111ll11_opy_ = bstack11l1llll1_opy_.get(str(threading.get_ident()))
      except Exception as e:
        logger.debug(bstack1l11l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡶࡪࡧࡤࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡏࡄࡴࠢࡩ࡭ࡱ࡫ࠠࡪࡰࠣࡸࡪࡹࡴࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࠪஇ") + str(e))
      if bstack111lll1l1_opy_:
        with bstack1l1lllllll_opy_:
          bstack1ll11lll_opy_ = bstack111lll1l1_opy_.copy()
        for driver in bstack1ll11lll_opy_:
          if bstack11111ll11_opy_ == driver.session_id:
            bstack11l11lll_opy_ = driver
    bstack1l1ll1111_opy_ = bstack1ll1ll1l11_opy_.bstack11l1ll1lll_opy_(test.tags)
    if bstack11l11lll_opy_:
      threading.current_thread().isA11yTest = bstack1ll1ll1l11_opy_.bstack1111l11l1_opy_(bstack11l11lll_opy_, bstack1l1ll1111_opy_)
      threading.current_thread().isAppA11yTest = bstack1ll1ll1l11_opy_.bstack1111l11l1_opy_(bstack11l11lll_opy_, bstack1l1ll1111_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1l1ll1111_opy_
      threading.current_thread().isAppA11yTest = bstack1l1ll1111_opy_
  except:
    pass
  bstack1l1111l11_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1llll111ll_opy_
  try:
    bstack1llll111ll_opy_ = self._test
  except:
    bstack1llll111ll_opy_ = self.test
def bstack111llllll1_opy_():
  global bstack1l1l1l11_opy_
  try:
    if os.path.exists(bstack1l1l1l11_opy_):
      os.remove(bstack1l1l1l11_opy_)
  except Exception as e:
    logger.debug(bstack1l11l11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨஈ") + str(e))
def bstack11ll1111l_opy_():
  global bstack1l1l1l11_opy_
  bstack1l11l11ll_opy_ = {}
  lock_file = bstack1l1l1l11_opy_ + bstack1l11l11_opy_ (u"࠭࠮࡭ࡱࡦ࡯ࠬஉ")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l11l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡱࡵࡣ࡬ࠢࡱࡳࡹࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦ࠮ࠣࡹࡸ࡯࡮ࡨࠢࡥࡥࡸ࡯ࡣࠡࡨ࡬ࡰࡪࠦ࡯ࡱࡧࡵࡥࡹ࡯࡯࡯ࡵࠪஊ"))
    try:
      if not os.path.isfile(bstack1l1l1l11_opy_):
        with open(bstack1l1l1l11_opy_, bstack1l11l11_opy_ (u"ࠨࡹࠪ஋")) as f:
          json.dump({}, f)
      if os.path.exists(bstack1l1l1l11_opy_):
        with open(bstack1l1l1l11_opy_, bstack1l11l11_opy_ (u"ࠩࡵࠫ஌")) as f:
          content = f.read().strip()
          if content:
            bstack1l11l11ll_opy_ = json.loads(content)
    except Exception as e:
      logger.debug(bstack1l11l11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡸࡥࡢࡦ࡬ࡲ࡬ࠦࡲࡰࡤࡲࡸࠥࡸࡥࡱࡱࡵࡸࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬ஍") + str(e))
    return bstack1l11l11ll_opy_
  try:
    os.makedirs(os.path.dirname(bstack1l1l1l11_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      if not os.path.isfile(bstack1l1l1l11_opy_):
        with open(bstack1l1l1l11_opy_, bstack1l11l11_opy_ (u"ࠫࡼ࠭எ")) as f:
          json.dump({}, f)
      if os.path.exists(bstack1l1l1l11_opy_):
        with open(bstack1l1l1l11_opy_, bstack1l11l11_opy_ (u"ࠬࡸࠧஏ")) as f:
          content = f.read().strip()
          if content:
            bstack1l11l11ll_opy_ = json.loads(content)
  except Exception as e:
    logger.debug(bstack1l11l11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡴࡨࡥࡩ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨஐ") + str(e))
  finally:
    return bstack1l11l11ll_opy_
def bstack1l111l1l11_opy_(platform_index, item_index):
  global bstack1l1l1l11_opy_
  lock_file = bstack1l1l1l11_opy_ + bstack1l11l11_opy_ (u"ࠧ࠯࡮ࡲࡧࡰ࠭஑")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l11l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡲ࡯ࡤ࡭ࠣࡲࡴࡺࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧ࠯ࠤࡺࡹࡩ࡯ࡩࠣࡦࡦࡹࡩࡤࠢࡩ࡭ࡱ࡫ࠠࡰࡲࡨࡶࡦࡺࡩࡰࡰࡶࠫஒ"))
    try:
      bstack1l11l11ll_opy_ = {}
      if os.path.exists(bstack1l1l1l11_opy_):
        with open(bstack1l1l1l11_opy_, bstack1l11l11_opy_ (u"ࠩࡵࠫஓ")) as f:
          content = f.read().strip()
          if content:
            bstack1l11l11ll_opy_ = json.loads(content)
      bstack1l11l11ll_opy_[item_index] = platform_index
      with open(bstack1l1l1l11_opy_, bstack1l11l11_opy_ (u"ࠥࡻࠧஔ")) as outfile:
        json.dump(bstack1l11l11ll_opy_, outfile)
    except Exception as e:
      logger.debug(bstack1l11l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡷࡳ࡫ࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺ࠡࠩக") + str(e))
    return
  try:
    os.makedirs(os.path.dirname(bstack1l1l1l11_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      bstack1l11l11ll_opy_ = {}
      if os.path.exists(bstack1l1l1l11_opy_):
        with open(bstack1l1l1l11_opy_, bstack1l11l11_opy_ (u"ࠬࡸࠧ஖")) as f:
          content = f.read().strip()
          if content:
            bstack1l11l11ll_opy_ = json.loads(content)
      bstack1l11l11ll_opy_[item_index] = platform_index
      with open(bstack1l1l1l11_opy_, bstack1l11l11_opy_ (u"ࠨࡷࠣ஗")) as outfile:
        json.dump(bstack1l11l11ll_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1l11l11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡺࡶ࡮ࡺࡩ࡯ࡩࠣࡸࡴࠦࡲࡰࡤࡲࡸࠥࡸࡥࡱࡱࡵࡸࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬ஘") + str(e))
def bstack1llllll1ll_opy_(bstack1l111l1lll_opy_):
  global CONFIG
  bstack1l1111l11l_opy_ = bstack1l11l11_opy_ (u"ࠨࠩங")
  if not bstack1l11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬச") in CONFIG:
    logger.info(bstack1l11l11_opy_ (u"ࠪࡒࡴࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠢࡳࡥࡸࡹࡥࡥࠢࡸࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡳࡧࡳࡳࡷࡺࠠࡧࡱࡵࠤࡗࡵࡢࡰࡶࠣࡶࡺࡴࠧ஛"))
  try:
    platform = CONFIG[bstack1l11l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧஜ")][bstack1l111l1lll_opy_]
    if bstack1l11l11_opy_ (u"ࠬࡵࡳࠨ஝") in platform:
      bstack1l1111l11l_opy_ += str(platform[bstack1l11l11_opy_ (u"࠭࡯ࡴࠩஞ")]) + bstack1l11l11_opy_ (u"ࠧ࠭ࠢࠪட")
    if bstack1l11l11_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫ஠") in platform:
      bstack1l1111l11l_opy_ += str(platform[bstack1l11l11_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬ஡")]) + bstack1l11l11_opy_ (u"ࠪ࠰ࠥ࠭஢")
    if bstack1l11l11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨண") in platform:
      bstack1l1111l11l_opy_ += str(platform[bstack1l11l11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩத")]) + bstack1l11l11_opy_ (u"࠭ࠬࠡࠩ஥")
    if bstack1l11l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ஦") in platform:
      bstack1l1111l11l_opy_ += str(platform[bstack1l11l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪ஧")]) + bstack1l11l11_opy_ (u"ࠩ࠯ࠤࠬந")
    if bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨன") in platform:
      bstack1l1111l11l_opy_ += str(platform[bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩப")]) + bstack1l11l11_opy_ (u"ࠬ࠲ࠠࠨ஫")
    if bstack1l11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ஬") in platform:
      bstack1l1111l11l_opy_ += str(platform[bstack1l11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ஭")]) + bstack1l11l11_opy_ (u"ࠨ࠮ࠣࠫம")
  except Exception as e:
    logger.debug(bstack1l11l11_opy_ (u"ࠩࡖࡳࡲ࡫ࠠࡦࡴࡵࡳࡷࠦࡩ࡯ࠢࡪࡩࡳ࡫ࡲࡢࡶ࡬ࡲ࡬ࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡵࡷࡶ࡮ࡴࡧࠡࡨࡲࡶࠥࡸࡥࡱࡱࡵࡸࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡯࡯࡯ࠩய") + str(e))
  finally:
    if bstack1l1111l11l_opy_[len(bstack1l1111l11l_opy_) - 2:] == bstack1l11l11_opy_ (u"ࠪ࠰ࠥ࠭ர"):
      bstack1l1111l11l_opy_ = bstack1l1111l11l_opy_[:-2]
    return bstack1l1111l11l_opy_
def bstack1ll1l1111l_opy_(path, bstack1l1111l11l_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1l1llll111_opy_ = ET.parse(path)
    bstack1ll11ll1_opy_ = bstack1l1llll111_opy_.getroot()
    bstack11l1l11l1_opy_ = None
    for suite in bstack1ll11ll1_opy_.iter(bstack1l11l11_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪற")):
      if bstack1l11l11_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬல") in suite.attrib:
        suite.attrib[bstack1l11l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫள")] += bstack1l11l11_opy_ (u"ࠧࠡࠩழ") + bstack1l1111l11l_opy_
        bstack11l1l11l1_opy_ = suite
    bstack111lllllll_opy_ = None
    for robot in bstack1ll11ll1_opy_.iter(bstack1l11l11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧவ")):
      bstack111lllllll_opy_ = robot
    bstack1l11lll1_opy_ = len(bstack111lllllll_opy_.findall(bstack1l11l11_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨஶ")))
    if bstack1l11lll1_opy_ == 1:
      bstack111lllllll_opy_.remove(bstack111lllllll_opy_.findall(bstack1l11l11_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩஷ"))[0])
      bstack11llll1l1_opy_ = ET.Element(bstack1l11l11_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪஸ"), attrib={bstack1l11l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪஹ"): bstack1l11l11_opy_ (u"࠭ࡓࡶ࡫ࡷࡩࡸ࠭஺"), bstack1l11l11_opy_ (u"ࠧࡪࡦࠪ஻"): bstack1l11l11_opy_ (u"ࠨࡵ࠳ࠫ஼")})
      bstack111lllllll_opy_.insert(1, bstack11llll1l1_opy_)
      bstack11111l1l1_opy_ = None
      for suite in bstack111lllllll_opy_.iter(bstack1l11l11_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨ஽")):
        bstack11111l1l1_opy_ = suite
      bstack11111l1l1_opy_.append(bstack11l1l11l1_opy_)
      bstack11ll1l1ll1_opy_ = None
      for status in bstack11l1l11l1_opy_.iter(bstack1l11l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪா")):
        bstack11ll1l1ll1_opy_ = status
      bstack11111l1l1_opy_.append(bstack11ll1l1ll1_opy_)
    bstack1l1llll111_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1l11l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡢࡴࡶ࡭ࡳ࡭ࠠࡸࡪ࡬ࡰࡪࠦࡧࡦࡰࡨࡶࡦࡺࡩ࡯ࡩࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠩி") + str(e))
def bstack1l11l1lll1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack111ll1l1_opy_
  global CONFIG
  if bstack1l11l11_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡵࡧࡴࡩࠤீ") in options:
    del options[bstack1l11l11_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡶࡡࡵࡪࠥு")]
  bstack11l11l1l1l_opy_ = bstack11ll1111l_opy_()
  for bstack11l1ll11ll_opy_ in bstack11l11l1l1l_opy_.keys():
    path = os.path.join(os.getcwd(), bstack1l11l11_opy_ (u"ࠧࡱࡣࡥࡳࡹࡥࡲࡦࡵࡸࡰࡹࡹࠧூ"), str(bstack11l1ll11ll_opy_), bstack1l11l11_opy_ (u"ࠨࡱࡸࡸࡵࡻࡴ࠯ࡺࡰࡰࠬ௃"))
    bstack1ll1l1111l_opy_(path, bstack1llllll1ll_opy_(bstack11l11l1l1l_opy_[bstack11l1ll11ll_opy_]))
  bstack111llllll1_opy_()
  return bstack111ll1l1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1l11lll111_opy_(self, ff_profile_dir):
  global bstack1lll1l111_opy_
  if not ff_profile_dir:
    return None
  return bstack1lll1l111_opy_(self, ff_profile_dir)
def bstack1ll1lll1l1_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack11ll111l1l_opy_
  bstack11l111ll11_opy_ = []
  if bstack1l11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ௄") in CONFIG:
    bstack11l111ll11_opy_ = CONFIG[bstack1l11l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭௅")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1l11l11_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࠧெ")],
      pabot_args[bstack1l11l11_opy_ (u"ࠧࡼࡥࡳࡤࡲࡷࡪࠨே")],
      argfile,
      pabot_args.get(bstack1l11l11_opy_ (u"ࠨࡨࡪࡸࡨࠦை")),
      pabot_args[bstack1l11l11_opy_ (u"ࠢࡱࡴࡲࡧࡪࡹࡳࡦࡵࠥ௉")],
      platform[0],
      bstack11ll111l1l_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1l11l11_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡩ࡭ࡱ࡫ࡳࠣொ")] or [(bstack1l11l11_opy_ (u"ࠤࠥோ"), None)]
    for platform in enumerate(bstack11l111ll11_opy_)
  ]
def bstack11ll11lll1_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1l11l111l_opy_=bstack1l11l11_opy_ (u"ࠪࠫௌ")):
  global bstack1ll111l11l_opy_
  self.platform_index = platform_index
  self.bstack111llll1ll_opy_ = bstack1l11l111l_opy_
  bstack1ll111l11l_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1lllll1lll_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1l1ll1ll1l_opy_
  global bstack1lll1ll11l_opy_
  bstack11l1l1l11_opy_ = copy.deepcopy(item)
  if not bstack1l11l11_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ்࠭") in item.options:
    bstack11l1l1l11_opy_.options[bstack1l11l11_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ௎")] = []
  bstack11l11l11_opy_ = bstack11l1l1l11_opy_.options[bstack1l11l11_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨ௏")].copy()
  for v in bstack11l1l1l11_opy_.options[bstack1l11l11_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩௐ")]:
    if bstack1l11l11_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡑࡎࡄࡘࡋࡕࡒࡎࡋࡑࡈࡊ࡞ࠧ௑") in v:
      bstack11l11l11_opy_.remove(v)
    if bstack1l11l11_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡅࡏࡍࡆࡘࡇࡔࠩ௒") in v:
      bstack11l11l11_opy_.remove(v)
    if bstack1l11l11_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡇࡉࡋࡒࡏࡄࡃࡏࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ௓") in v:
      bstack11l11l11_opy_.remove(v)
  bstack11l11l11_opy_.insert(0, bstack1l11l11_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚࠽ࡿࢂ࠭௔").format(bstack11l1l1l11_opy_.platform_index))
  bstack11l11l11_opy_.insert(0, bstack1l11l11_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡉࡋࡆࡍࡑࡆࡅࡑࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓ࠼ࡾࢁࠬ௕").format(bstack11l1l1l11_opy_.bstack111llll1ll_opy_))
  bstack11l1l1l11_opy_.options[bstack1l11l11_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨ௖")] = bstack11l11l11_opy_
  if bstack1lll1ll11l_opy_:
    bstack11l1l1l11_opy_.options[bstack1l11l11_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩௗ")].insert(0, bstack1l11l11_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓ࠻ࡽࢀࠫ௘").format(bstack1lll1ll11l_opy_))
  return bstack1l1ll1ll1l_opy_(caller_id, datasources, is_last, bstack11l1l1l11_opy_, outs_dir)
def bstack1l1l111l1l_opy_(command, item_index):
  try:
    if bstack11l11llll_opy_.get_property(bstack1l11l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪ௙")):
      os.environ[bstack1l11l11_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫ௚")] = json.dumps(CONFIG[bstack1l11l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ௛")][item_index % bstack1ll1l111l1_opy_])
    global bstack1lll1ll11l_opy_
    if bstack1lll1ll11l_opy_:
      command[0] = command[0].replace(bstack1l11l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ௜"), bstack1l11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡹࡤ࡬ࠢࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠣ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠢࠪ௝") + str(
        item_index) + bstack1l11l11_opy_ (u"ࠧࠡࠩ௞") + bstack1lll1ll11l_opy_, 1)
    else:
      command[0] = command[0].replace(bstack1l11l11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ௟"),
                                      bstack1l11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠮ࡵࡧ࡯ࠥࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱࠦ࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠥ࠭௠") + str(item_index), 1)
  except Exception as e:
    logger.error(bstack1l11l11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡰࡳࡩ࡯ࡦࡺ࡫ࡱ࡫ࠥࡩ࡯࡮࡯ࡤࡲࡩࠦࡦࡰࡴࠣࡴࡦࡨ࡯ࡵࠢࡵࡹࡳࡀࠠࡼࡿࠪ௡").format(str(e)))
def bstack11l1lllll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack11l1l11ll_opy_
  try:
    bstack1l1l111l1l_opy_(command, item_index)
    return bstack11l1l11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
  except Exception as e:
    logger.error(bstack1l11l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡢࡤࡲࡸࠥࡸࡵ࡯࠼ࠣࡿࢂ࠭௢").format(str(e)))
    raise e
def bstack1lll11l1l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack11l1l11ll_opy_
  try:
    bstack1l1l111l1l_opy_(command, item_index)
    return bstack11l1l11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
  except Exception as e:
    logger.error(bstack1l11l11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡥࡳࡹࠦࡲࡶࡰࠣ࠶࠳࠷࠳࠻ࠢࡾࢁࠬ௣").format(str(e)))
    try:
      return bstack11l1l11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
    except Exception as e2:
      logger.error(bstack1l11l11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠ࠳࠰࠴࠷ࠥ࡬ࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࡽࢀࠫ௤").format(str(e2)))
      raise e
def bstack11ll11ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack11l1l11ll_opy_
  try:
    bstack1l1l111l1l_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    return bstack11l1l11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
  except Exception as e:
    logger.error(bstack1l11l11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡧࡵࡴࠡࡴࡸࡲࠥ࠸࠮࠲࠷࠽ࠤࢀࢃࠧ௥").format(str(e)))
    try:
      return bstack11l1l11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
    except Exception as e2:
      logger.error(bstack1l11l11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡦࡨ࡯ࡵࠢ࠵࠲࠶࠻ࠠࡧࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣࡿࢂ࠭௦").format(str(e2)))
      raise e
def bstack11ll1llll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack11l1l11ll_opy_
  try:
    bstack1l1l111l1l_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    if sleep_before_start and sleep_before_start > 0:
      import time
      time.sleep(min(sleep_before_start, 5))
    return bstack11l1l11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack1l11l11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡢࡰࡶࠣࡶࡺࡴࠠ࠵࠰࠵࠾ࠥࢁࡽࠨ௧").format(str(e)))
    try:
      return bstack11l1l11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack1l11l11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡣࡱࡷࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࡼࡿࠪ௨").format(str(e2)))
      raise e
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack1111l1lll_opy_(self, runner, quiet=False, capture=True):
  global bstack111lll1l_opy_
  bstack11ll1l1l1_opy_ = bstack111lll1l_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack1l11l11_opy_ (u"ࠫࡪࡾࡣࡦࡲࡷ࡭ࡴࡴ࡟ࡢࡴࡵࠫ௩")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1l11l11_opy_ (u"ࠬ࡫ࡸࡤࡡࡷࡶࡦࡩࡥࡣࡣࡦ࡯ࡤࡧࡲࡳࠩ௪")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack11ll1l1l1_opy_
def bstack1ll1l1lll1_opy_(runner, hook_name, context, element, bstack11ll11l1_opy_, *args):
  try:
    if runner.hooks.get(hook_name):
      bstack1l1ll11111_opy_.bstack111111ll_opy_(hook_name, element)
    bstack11ll11l1_opy_(runner, hook_name, context, *args)
    if runner.hooks.get(hook_name):
      bstack1l1ll11111_opy_.bstack11111l1ll_opy_(element)
      if hook_name not in [bstack1l11l11_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠪ௫"), bstack1l11l11_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪ௬")] and args and hasattr(args[0], bstack1l11l11_opy_ (u"ࠨࡧࡵࡶࡴࡸ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠨ௭")):
        args[0].error_message = bstack1l11l11_opy_ (u"ࠩࠪ௮")
  except Exception as e:
    logger.debug(bstack1l11l11_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡨࡢࡰࡧࡰࡪࠦࡨࡰࡱ࡮ࡷࠥ࡯࡮ࠡࡤࡨ࡬ࡦࡼࡥ࠻ࠢࡾࢁࠬ௯").format(str(e)))
@measure(event_name=EVENTS.bstack1111lll11_opy_, stage=STAGE.bstack1lll11l1_opy_, hook_type=bstack1l11l11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡅࡱࡲࠢ௰"), bstack1l1lll11l_opy_=bstack1lllll1ll_opy_)
def bstack1lll1111l1_opy_(runner, name, context, bstack11ll11l1_opy_, *args):
    if runner.hooks.get(bstack1l11l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤ௱")).__name__ != bstack1l11l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࡢࡨࡪ࡬ࡡࡶ࡮ࡷࡣ࡭ࡵ࡯࡬ࠤ௲"):
      bstack1ll1l1lll1_opy_(runner, name, context, runner, bstack11ll11l1_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack1l1111l111_opy_(bstack1l11l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭௳")) else context.browser
      runner.driver_initialised = bstack1l11l11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧ௴")
    except Exception as e:
      logger.debug(bstack1l11l11_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡧࡶ࡮ࡼࡥࡳࠢ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡷࡪࠦࡡࡵࡶࡵ࡭ࡧࡻࡴࡦ࠼ࠣࡿࢂ࠭௵").format(str(e)))
def bstack1111ll11l_opy_(runner, name, context, bstack11ll11l1_opy_, *args):
    bstack1ll1l1lll1_opy_(runner, name, context, context.feature, bstack11ll11l1_opy_, *args)
    try:
      if not bstack1l1llllll1_opy_:
        bstack11l11lll_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1111l111_opy_(bstack1l11l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ௶")) else context.browser
        if is_driver_active(bstack11l11lll_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack1l11l11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠧ௷")
          bstack1l111l111l_opy_ = str(runner.feature.name)
          bstack1lll1l1l11_opy_(context, bstack1l111l111l_opy_)
          bstack11l11lll_opy_.execute_script(bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ௸") + json.dumps(bstack1l111l111l_opy_) + bstack1l11l11_opy_ (u"࠭ࡽࡾࠩ௹"))
    except Exception as e:
      logger.debug(bstack1l11l11_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧ௺").format(str(e)))
def bstack1lllll111l_opy_(runner, name, context, bstack11ll11l1_opy_, *args):
    if hasattr(context, bstack1l11l11_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪ௻")):
        bstack1l1ll11111_opy_.start_test(context)
    target = context.scenario if hasattr(context, bstack1l11l11_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ௼")) else context.feature
    bstack1ll1l1lll1_opy_(runner, name, context, target, bstack11ll11l1_opy_, *args)
@measure(event_name=EVENTS.bstack1l1l1lllll_opy_, stage=STAGE.bstack1lll11l1_opy_, bstack1l1lll11l_opy_=bstack1lllll1ll_opy_)
def bstack1lll1111_opy_(runner, name, context, bstack11ll11l1_opy_, *args):
    if len(context.scenario.tags) == 0: bstack1l1ll11111_opy_.start_test(context)
    bstack1ll1l1lll1_opy_(runner, name, context, context.scenario, bstack11ll11l1_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack1l1l111l_opy_.bstack1lll1ll11_opy_(context, *args)
    try:
      bstack11l11lll_opy_ = bstack1l111ll111_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ௽"), context.browser)
      if is_driver_active(bstack11l11lll_opy_):
        bstack11ll111ll1_opy_.bstack11ll1l11l_opy_(bstack1l111ll111_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ௾"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack1l11l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢ௿")
        if (not bstack1l1llllll1_opy_):
          scenario_name = args[0].name
          feature_name = bstack1l111l111l_opy_ = str(runner.feature.name)
          bstack1l111l111l_opy_ = feature_name + bstack1l11l11_opy_ (u"࠭ࠠ࠮ࠢࠪఀ") + scenario_name
          if runner.driver_initialised == bstack1l11l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤఁ"):
            bstack1lll1l1l11_opy_(context, bstack1l111l111l_opy_)
            bstack11l11lll_opy_.execute_script(bstack1l11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭ం") + json.dumps(bstack1l111l111l_opy_) + bstack1l11l11_opy_ (u"ࠩࢀࢁࠬః"))
    except Exception as e:
      logger.debug(bstack1l11l11_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡦࡰࡤࡶ࡮ࡵ࠺ࠡࡽࢀࠫఄ").format(str(e)))
@measure(event_name=EVENTS.bstack1111lll11_opy_, stage=STAGE.bstack1lll11l1_opy_, hook_type=bstack1l11l11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡗࡹ࡫ࡰࠣఅ"), bstack1l1lll11l_opy_=bstack1lllll1ll_opy_)
def bstack1lll11l1l_opy_(runner, name, context, bstack11ll11l1_opy_, *args):
    bstack1ll1l1lll1_opy_(runner, name, context, args[0], bstack11ll11l1_opy_, *args)
    try:
      bstack11l11lll_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1111l111_opy_(bstack1l11l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫఆ")) else context.browser
      if is_driver_active(bstack11l11lll_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack1l11l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦఇ")
        bstack1l1ll11111_opy_.bstack111l11l1l_opy_(args[0])
        if runner.driver_initialised == bstack1l11l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧఈ"):
          feature_name = bstack1l111l111l_opy_ = str(runner.feature.name)
          bstack1l111l111l_opy_ = feature_name + bstack1l11l11_opy_ (u"ࠨࠢ࠰ࠤࠬఉ") + context.scenario.name
          bstack11l11lll_opy_.execute_script(bstack1l11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧఊ") + json.dumps(bstack1l111l111l_opy_) + bstack1l11l11_opy_ (u"ࠪࢁࢂ࠭ఋ"))
    except Exception as e:
      logger.debug(bstack1l11l11_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣ࡭ࡳࠦࡢࡦࡨࡲࡶࡪࠦࡳࡵࡧࡳ࠾ࠥࢁࡽࠨఌ").format(str(e)))
@measure(event_name=EVENTS.bstack1111lll11_opy_, stage=STAGE.bstack1lll11l1_opy_, hook_type=bstack1l11l11_opy_ (u"ࠧࡧࡦࡵࡧࡵࡗࡹ࡫ࡰࠣ఍"), bstack1l1lll11l_opy_=bstack1lllll1ll_opy_)
def bstack1l11ll111l_opy_(runner, name, context, bstack11ll11l1_opy_, *args):
  bstack1l1ll11111_opy_.bstack1l11l1ll1l_opy_(args[0])
  try:
    bstack11l1111l11_opy_ = args[0].status.name
    bstack11l11lll_opy_ = threading.current_thread().bstackSessionDriver if bstack1l11l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬఎ") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack11l11lll_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack1l11l11_opy_ (u"ࠧࡪࡰࡶࡸࡪࡶࠧఏ")
        feature_name = bstack1l111l111l_opy_ = str(runner.feature.name)
        bstack1l111l111l_opy_ = feature_name + bstack1l11l11_opy_ (u"ࠨࠢ࠰ࠤࠬఐ") + context.scenario.name
        bstack11l11lll_opy_.execute_script(bstack1l11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧ఑") + json.dumps(bstack1l111l111l_opy_) + bstack1l11l11_opy_ (u"ࠪࢁࢂ࠭ఒ"))
    if str(bstack11l1111l11_opy_).lower() == bstack1l11l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫఓ"):
      bstack11lllll1_opy_ = bstack1l11l11_opy_ (u"ࠬ࠭ఔ")
      bstack1l11ll111_opy_ = bstack1l11l11_opy_ (u"࠭ࠧక")
      bstack1ll11l1l1l_opy_ = bstack1l11l11_opy_ (u"ࠧࠨఖ")
      try:
        import traceback
        bstack11lllll1_opy_ = runner.exception.__class__.__name__
        bstack1l11l111l1_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1l11ll111_opy_ = bstack1l11l11_opy_ (u"ࠨࠢࠪగ").join(bstack1l11l111l1_opy_)
        bstack1ll11l1l1l_opy_ = bstack1l11l111l1_opy_[-1]
      except Exception as e:
        logger.debug(bstack1ll1l1l11_opy_.format(str(e)))
      bstack11lllll1_opy_ += bstack1ll11l1l1l_opy_
      bstack1l11llll1_opy_(context, json.dumps(str(args[0].name) + bstack1l11l11_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣఘ") + str(bstack1l11ll111_opy_)),
                          bstack1l11l11_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤఙ"))
      if runner.driver_initialised == bstack1l11l11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤచ"):
        bstack1l11111l1l_opy_(getattr(context, bstack1l11l11_opy_ (u"ࠬࡶࡡࡨࡧࠪఛ"), None), bstack1l11l11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨజ"), bstack11lllll1_opy_)
        bstack11l11lll_opy_.execute_script(bstack1l11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬఝ") + json.dumps(str(args[0].name) + bstack1l11l11_opy_ (u"ࠣࠢ࠰ࠤࡋࡧࡩ࡭ࡧࡧࠥࡡࡴࠢఞ") + str(bstack1l11ll111_opy_)) + bstack1l11l11_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࡽࡾࠩట"))
      if runner.driver_initialised == bstack1l11l11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣఠ"):
        bstack1l1l11l1ll_opy_(bstack11l11lll_opy_, bstack1l11l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫడ"), bstack1l11l11_opy_ (u"࡙ࠧࡣࡦࡰࡤࡶ࡮ࡵࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤఢ") + str(bstack11lllll1_opy_))
    else:
      bstack1l11llll1_opy_(context, bstack1l11l11_opy_ (u"ࠨࡐࡢࡵࡶࡩࡩࠧࠢణ"), bstack1l11l11_opy_ (u"ࠢࡪࡰࡩࡳࠧత"))
      if runner.driver_initialised == bstack1l11l11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨథ"):
        bstack1l11111l1l_opy_(getattr(context, bstack1l11l11_opy_ (u"ࠩࡳࡥ࡬࡫ࠧద"), None), bstack1l11l11_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥధ"))
      bstack11l11lll_opy_.execute_script(bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩన") + json.dumps(str(args[0].name) + bstack1l11l11_opy_ (u"ࠧࠦ࠭ࠡࡒࡤࡷࡸ࡫ࡤࠢࠤ఩")) + bstack1l11l11_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤࢀࢁࠬప"))
      if runner.driver_initialised == bstack1l11l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧఫ"):
        bstack1l1l11l1ll_opy_(bstack11l11lll_opy_, bstack1l11l11_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣబ"))
  except Exception as e:
    logger.debug(bstack1l11l11_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡳࡵࡧࡳ࠾ࠥࢁࡽࠨభ").format(str(e)))
  bstack1ll1l1lll1_opy_(runner, name, context, args[0], bstack11ll11l1_opy_, *args)
@measure(event_name=EVENTS.bstack1l11l11ll1_opy_, stage=STAGE.bstack1lll11l1_opy_, bstack1l1lll11l_opy_=bstack1lllll1ll_opy_)
def bstack11l1ll11_opy_(runner, name, context, bstack11ll11l1_opy_, *args):
  bstack1l1ll11111_opy_.end_test(args[0])
  try:
    bstack1111l1l1_opy_ = args[0].status.name
    bstack11l11lll_opy_ = bstack1l111ll111_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩమ"), context.browser)
    bstack1l1l111l_opy_.bstack1l111l111_opy_(bstack11l11lll_opy_)
    if str(bstack1111l1l1_opy_).lower() == bstack1l11l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫయ"):
      bstack11lllll1_opy_ = bstack1l11l11_opy_ (u"ࠬ࠭ర")
      bstack1l11ll111_opy_ = bstack1l11l11_opy_ (u"࠭ࠧఱ")
      bstack1ll11l1l1l_opy_ = bstack1l11l11_opy_ (u"ࠧࠨల")
      try:
        import traceback
        bstack11lllll1_opy_ = runner.exception.__class__.__name__
        bstack1l11l111l1_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1l11ll111_opy_ = bstack1l11l11_opy_ (u"ࠨࠢࠪళ").join(bstack1l11l111l1_opy_)
        bstack1ll11l1l1l_opy_ = bstack1l11l111l1_opy_[-1]
      except Exception as e:
        logger.debug(bstack1ll1l1l11_opy_.format(str(e)))
      bstack11lllll1_opy_ += bstack1ll11l1l1l_opy_
      bstack1l11llll1_opy_(context, json.dumps(str(args[0].name) + bstack1l11l11_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣఴ") + str(bstack1l11ll111_opy_)),
                          bstack1l11l11_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤవ"))
      if runner.driver_initialised == bstack1l11l11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨశ") or runner.driver_initialised == bstack1l11l11_opy_ (u"ࠬ࡯࡮ࡴࡶࡨࡴࠬష"):
        bstack1l11111l1l_opy_(getattr(context, bstack1l11l11_opy_ (u"࠭ࡰࡢࡩࡨࠫస"), None), bstack1l11l11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢహ"), bstack11lllll1_opy_)
        bstack11l11lll_opy_.execute_script(bstack1l11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭఺") + json.dumps(str(args[0].name) + bstack1l11l11_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣ఻") + str(bstack1l11ll111_opy_)) + bstack1l11l11_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿ఼ࠪ"))
      if runner.driver_initialised == bstack1l11l11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨఽ") or runner.driver_initialised == bstack1l11l11_opy_ (u"ࠬ࡯࡮ࡴࡶࡨࡴࠬా"):
        bstack1l1l11l1ll_opy_(bstack11l11lll_opy_, bstack1l11l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ి"), bstack1l11l11_opy_ (u"ࠢࡔࡥࡨࡲࡦࡸࡩࡰࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦీ") + str(bstack11lllll1_opy_))
    else:
      bstack1l11llll1_opy_(context, bstack1l11l11_opy_ (u"ࠣࡒࡤࡷࡸ࡫ࡤࠢࠤు"), bstack1l11l11_opy_ (u"ࠤ࡬ࡲ࡫ࡵࠢూ"))
      if runner.driver_initialised == bstack1l11l11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧృ") or runner.driver_initialised == bstack1l11l11_opy_ (u"ࠫ࡮ࡴࡳࡵࡧࡳࠫౄ"):
        bstack1l11111l1l_opy_(getattr(context, bstack1l11l11_opy_ (u"ࠬࡶࡡࡨࡧࠪ౅"), None), bstack1l11l11_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨె"))
      bstack11l11lll_opy_.execute_script(bstack1l11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬే") + json.dumps(str(args[0].name) + bstack1l11l11_opy_ (u"ࠣࠢ࠰ࠤࡕࡧࡳࡴࡧࡧࠥࠧై")) + bstack1l11l11_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧࢃࡽࠨ౉"))
      if runner.driver_initialised == bstack1l11l11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧొ") or runner.driver_initialised == bstack1l11l11_opy_ (u"ࠫ࡮ࡴࡳࡵࡧࡳࠫో"):
        bstack1l1l11l1ll_opy_(bstack11l11lll_opy_, bstack1l11l11_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧౌ"))
  except Exception as e:
    logger.debug(bstack1l11l11_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨ్").format(str(e)))
  bstack1ll1l1lll1_opy_(runner, name, context, context.scenario, bstack11ll11l1_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack1l1ll1l1l1_opy_(runner, name, context, bstack11ll11l1_opy_, *args):
    target = context.scenario if hasattr(context, bstack1l11l11_opy_ (u"ࠧࡴࡥࡨࡲࡦࡸࡩࡰࠩ౎")) else context.feature
    bstack1ll1l1lll1_opy_(runner, name, context, target, bstack11ll11l1_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack1ll1lll11_opy_(runner, name, context, bstack11ll11l1_opy_, *args):
    try:
      bstack11l11lll_opy_ = bstack1l111ll111_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ౏"), context.browser)
      bstack1llllll11_opy_ = bstack1l11l11_opy_ (u"ࠩࠪ౐")
      if context.failed is True:
        bstack11l1l1ll11_opy_ = []
        bstack1l1l1l11ll_opy_ = []
        bstack11ll11l1ll_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack11l1l1ll11_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1l11l111l1_opy_ = traceback.format_tb(exc_tb)
            bstack1ll11ll1l1_opy_ = bstack1l11l11_opy_ (u"ࠪࠤࠬ౑").join(bstack1l11l111l1_opy_)
            bstack1l1l1l11ll_opy_.append(bstack1ll11ll1l1_opy_)
            bstack11ll11l1ll_opy_.append(bstack1l11l111l1_opy_[-1])
        except Exception as e:
          logger.debug(bstack1ll1l1l11_opy_.format(str(e)))
        bstack11lllll1_opy_ = bstack1l11l11_opy_ (u"ࠫࠬ౒")
        for i in range(len(bstack11l1l1ll11_opy_)):
          bstack11lllll1_opy_ += bstack11l1l1ll11_opy_[i] + bstack11ll11l1ll_opy_[i] + bstack1l11l11_opy_ (u"ࠬࡢ࡮ࠨ౓")
        bstack1llllll11_opy_ = bstack1l11l11_opy_ (u"࠭ࠠࠨ౔").join(bstack1l1l1l11ll_opy_)
        if runner.driver_initialised in [bstack1l11l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥౕࠣ"), bstack1l11l11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰౖࠧ")]:
          bstack1l11llll1_opy_(context, bstack1llllll11_opy_, bstack1l11l11_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣ౗"))
          bstack1l11111l1l_opy_(getattr(context, bstack1l11l11_opy_ (u"ࠪࡴࡦ࡭ࡥࠨౘ"), None), bstack1l11l11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦౙ"), bstack11lllll1_opy_)
          bstack11l11lll_opy_.execute_script(bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪౚ") + json.dumps(bstack1llllll11_opy_) + bstack1l11l11_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥࢁࢂ࠭౛"))
          bstack1l1l11l1ll_opy_(bstack11l11lll_opy_, bstack1l11l11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ౜"), bstack1l11l11_opy_ (u"ࠣࡕࡲࡱࡪࠦࡳࡤࡧࡱࡥࡷ࡯࡯ࡴࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡠࡳࠨౝ") + str(bstack11lllll1_opy_))
          bstack1l1l1l11l1_opy_ = bstack111111l11_opy_(bstack1llllll11_opy_, runner.feature.name, logger)
          if (bstack1l1l1l11l1_opy_ != None):
            bstack1lll1lll11_opy_.append(bstack1l1l1l11l1_opy_)
      else:
        if runner.driver_initialised in [bstack1l11l11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠥ౞"), bstack1l11l11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢ౟")]:
          bstack1l11llll1_opy_(context, bstack1l11l11_opy_ (u"ࠦࡋ࡫ࡡࡵࡷࡵࡩ࠿ࠦࠢౠ") + str(runner.feature.name) + bstack1l11l11_opy_ (u"ࠧࠦࡰࡢࡵࡶࡩࡩࠧࠢౡ"), bstack1l11l11_opy_ (u"ࠨࡩ࡯ࡨࡲࠦౢ"))
          bstack1l11111l1l_opy_(getattr(context, bstack1l11l11_opy_ (u"ࠧࡱࡣࡪࡩࠬౣ"), None), bstack1l11l11_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ౤"))
          bstack11l11lll_opy_.execute_script(bstack1l11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ౥") + json.dumps(bstack1l11l11_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨ࠾ࠥࠨ౦") + str(runner.feature.name) + bstack1l11l11_opy_ (u"ࠦࠥࡶࡡࡴࡵࡨࡨࠦࠨ౧")) + bstack1l11l11_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫ౨"))
          bstack1l1l11l1ll_opy_(bstack11l11lll_opy_, bstack1l11l11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭౩"))
          bstack1l1l1l11l1_opy_ = bstack111111l11_opy_(bstack1llllll11_opy_, runner.feature.name, logger)
          if (bstack1l1l1l11l1_opy_ != None):
            bstack1lll1lll11_opy_.append(bstack1l1l1l11l1_opy_)
    except Exception as e:
      logger.debug(bstack1l11l11_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩ౪").format(str(e)))
    bstack1ll1l1lll1_opy_(runner, name, context, context.feature, bstack11ll11l1_opy_, *args)
@measure(event_name=EVENTS.bstack1111lll11_opy_, stage=STAGE.bstack1lll11l1_opy_, hook_type=bstack1l11l11_opy_ (u"ࠣࡣࡩࡸࡪࡸࡁ࡭࡮ࠥ౫"), bstack1l1lll11l_opy_=bstack1lllll1ll_opy_)
def bstack1l1ll1lll1_opy_(runner, name, context, bstack11ll11l1_opy_, *args):
    bstack1ll1l1lll1_opy_(runner, name, context, runner, bstack11ll11l1_opy_, *args)
def bstack111llll11_opy_(self, name, context, *args):
  try:
    if bstack1l1l11lll_opy_:
      platform_index = int(threading.current_thread()._name) % bstack1ll1l111l1_opy_
      bstack1l11ll1111_opy_ = CONFIG[bstack1l11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ౬")][platform_index]
      os.environ[bstack1l11l11_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫ౭")] = json.dumps(bstack1l11ll1111_opy_)
    global bstack11ll11l1_opy_
    if not hasattr(self, bstack1l11l11_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡥࡥࠩ౮")):
      self.driver_initialised = None
    bstack111l1l1l_opy_ = {
        bstack1l11l11_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠩ౯"): bstack1lll1111l1_opy_,
        bstack1l11l11_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠧ౰"): bstack1111ll11l_opy_,
        bstack1l11l11_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡵࡣࡪࠫ౱"): bstack1lllll111l_opy_,
        bstack1l11l11_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ౲"): bstack1lll1111_opy_,
        bstack1l11l11_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠧ౳"): bstack1lll11l1l_opy_,
        bstack1l11l11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡸࡪࡶࠧ౴"): bstack1l11ll111l_opy_,
        bstack1l11l11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ౵"): bstack11l1ll11_opy_,
        bstack1l11l11_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡹࡧࡧࠨ౶"): bstack1l1ll1l1l1_opy_,
        bstack1l11l11_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭౷"): bstack1ll1lll11_opy_,
        bstack1l11l11_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪ౸"): bstack1l1ll1lll1_opy_
    }
    handler = bstack111l1l1l_opy_.get(name, bstack11ll11l1_opy_)
    try:
      handler(self, name, context, bstack11ll11l1_opy_, *args)
    except Exception as e:
      logger.debug(bstack1l11l11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡦࡪ࡮ࡡࡷࡧࠣ࡬ࡴࡵ࡫ࠡࡪࡤࡲࡩࡲࡥࡳࠢࡾࢁ࠿ࠦࡻࡾࠩ౹").format(name, str(e)))
    if name in [bstack1l11l11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠩ౺"), bstack1l11l11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ౻"), bstack1l11l11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡥࡱࡲࠧ౼")]:
      try:
        bstack11l11lll_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1111l111_opy_(bstack1l11l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ౽")) else context.browser
        bstack1l111l11ll_opy_ = (
          (name == bstack1l11l11_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠩ౾") and self.driver_initialised == bstack1l11l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦ౿")) or
          (name == bstack1l11l11_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨಀ") and self.driver_initialised == bstack1l11l11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠥಁ")) or
          (name == bstack1l11l11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫಂ") and self.driver_initialised in [bstack1l11l11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨಃ"), bstack1l11l11_opy_ (u"ࠧ࡯࡮ࡴࡶࡨࡴࠧ಄")]) or
          (name == bstack1l11l11_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡴࡦࡲࠪಅ") and self.driver_initialised == bstack1l11l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧಆ"))
        )
        if bstack1l111l11ll_opy_:
          self.driver_initialised = None
          if bstack11l11lll_opy_ and hasattr(bstack11l11lll_opy_, bstack1l11l11_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠬಇ")):
            try:
              bstack11l11lll_opy_.quit()
            except Exception as e:
              logger.debug(bstack1l11l11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡳࡸ࡭ࡹࡺࡩ࡯ࡩࠣࡨࡷ࡯ࡶࡦࡴࠣ࡭ࡳࠦࡢࡦࡪࡤࡺࡪࠦࡨࡰࡱ࡮࠾ࠥࢁࡽࠨಈ").format(str(e)))
      except Exception as e:
        logger.debug(bstack1l11l11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡭ࡵ࡯࡬ࠢࡦࡰࡪࡧ࡮ࡶࡲࠣࡪࡴࡸࠠࡼࡿ࠽ࠤࢀࢃࠧಉ").format(name, str(e)))
  except Exception as e:
    logger.debug(bstack1l11l11_opy_ (u"ࠫࡈࡸࡩࡵ࡫ࡦࡥࡱࠦࡥࡳࡴࡲࡶࠥ࡯࡮ࠡࡤࡨ࡬ࡦࡼࡥࠡࡴࡸࡲࠥ࡮࡯ࡰ࡭ࠣࡿࢂࡀࠠࡼࡿࠪಊ").format(name, str(e)))
    try:
      bstack11ll11l1_opy_(self, name, context, *args)
    except Exception as e2:
      logger.debug(bstack1l11l11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡲࡶ࡮࡭ࡩ࡯ࡣ࡯ࠤࡧ࡫ࡨࡢࡸࡨࠤ࡭ࡵ࡯࡬ࠢࡾࢁ࠿ࠦࡻࡾࠩಋ").format(name, str(e2)))
def bstack111l1l11_opy_(config, startdir):
  return bstack1l11l11_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡀࠠࡼ࠲ࢀࠦಌ").format(bstack1l11l11_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨ಍"))
notset = Notset()
def bstack1ll11l1lll_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1l1111lll1_opy_
  if str(name).lower() == bstack1l11l11_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࠨಎ"):
    return bstack1l11l11_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣಏ")
  else:
    return bstack1l1111lll1_opy_(self, name, default, skip)
def bstack1l1ll11l_opy_(item, when):
  global bstack11llll1l11_opy_
  try:
    bstack11llll1l11_opy_(item, when)
  except Exception as e:
    pass
def bstack1l111lllll_opy_():
  return
def bstack1llll11ll1_opy_(type, name, status, reason, bstack1ll1111ll_opy_, bstack11llll1l1l_opy_):
  bstack1llllll1l_opy_ = {
    bstack1l11l11_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪಐ"): type,
    bstack1l11l11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ಑"): {}
  }
  if type == bstack1l11l11_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧಒ"):
    bstack1llllll1l_opy_[bstack1l11l11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩಓ")][bstack1l11l11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ಔ")] = bstack1ll1111ll_opy_
    bstack1llllll1l_opy_[bstack1l11l11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫಕ")][bstack1l11l11_opy_ (u"ࠩࡧࡥࡹࡧࠧಖ")] = json.dumps(str(bstack11llll1l1l_opy_))
  if type == bstack1l11l11_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫಗ"):
    bstack1llllll1l_opy_[bstack1l11l11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧಘ")][bstack1l11l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪಙ")] = name
  if type == bstack1l11l11_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩಚ"):
    bstack1llllll1l_opy_[bstack1l11l11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪಛ")][bstack1l11l11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨಜ")] = status
    if status == bstack1l11l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩಝ"):
      bstack1llllll1l_opy_[bstack1l11l11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ಞ")][bstack1l11l11_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫಟ")] = json.dumps(str(reason))
  bstack1ll11l11ll_opy_ = bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪಠ").format(json.dumps(bstack1llllll1l_opy_))
  return bstack1ll11l11ll_opy_
def bstack1ll1l1l1l_opy_(driver_command, response):
    if driver_command == bstack1l11l11_opy_ (u"࠭ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪಡ"):
        bstack11ll111ll1_opy_.bstack11ll1lll11_opy_({
            bstack1l11l11_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭ಢ"): response[bstack1l11l11_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧಣ")],
            bstack1l11l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩತ"): bstack11ll111ll1_opy_.current_test_uuid()
        })
def bstack11l1l111l1_opy_(item, call, rep):
  global bstack1111l11ll_opy_
  global bstack111lll1l1_opy_
  global bstack1l1llllll1_opy_
  name = bstack1l11l11_opy_ (u"ࠪࠫಥ")
  try:
    if rep.when == bstack1l11l11_opy_ (u"ࠫࡨࡧ࡬࡭ࠩದ"):
      bstack11111ll11_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1l1llllll1_opy_:
          name = str(rep.nodeid)
          bstack1lll11ll11_opy_ = bstack1llll11ll1_opy_(bstack1l11l11_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ಧ"), name, bstack1l11l11_opy_ (u"࠭ࠧನ"), bstack1l11l11_opy_ (u"ࠧࠨ಩"), bstack1l11l11_opy_ (u"ࠨࠩಪ"), bstack1l11l11_opy_ (u"ࠩࠪಫ"))
          threading.current_thread().bstack1l1l111111_opy_ = name
          for driver in bstack111lll1l1_opy_:
            if bstack11111ll11_opy_ == driver.session_id:
              driver.execute_script(bstack1lll11ll11_opy_)
      except Exception as e:
        logger.debug(bstack1l11l11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪಬ").format(str(e)))
      try:
        bstack1l1lllll1_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack1l11l11_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬಭ"):
          status = bstack1l11l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬಮ") if rep.outcome.lower() == bstack1l11l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ಯ") else bstack1l11l11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧರ")
          reason = bstack1l11l11_opy_ (u"ࠨࠩಱ")
          if status == bstack1l11l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩಲ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack1l11l11_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨಳ") if status == bstack1l11l11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ಴") else bstack1l11l11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫವ")
          data = name + bstack1l11l11_opy_ (u"࠭ࠠࡱࡣࡶࡷࡪࡪࠡࠨಶ") if status == bstack1l11l11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧಷ") else name + bstack1l11l11_opy_ (u"ࠨࠢࡩࡥ࡮ࡲࡥࡥࠣࠣࠫಸ") + reason
          bstack1l1llll1l1_opy_ = bstack1llll11ll1_opy_(bstack1l11l11_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫಹ"), bstack1l11l11_opy_ (u"ࠪࠫ಺"), bstack1l11l11_opy_ (u"ࠫࠬ಻"), bstack1l11l11_opy_ (u"಼ࠬ࠭"), level, data)
          for driver in bstack111lll1l1_opy_:
            if bstack11111ll11_opy_ == driver.session_id:
              driver.execute_script(bstack1l1llll1l1_opy_)
      except Exception as e:
        logger.debug(bstack1l11l11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡧࡴࡴࡴࡦࡺࡷࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪಽ").format(str(e)))
  except Exception as e:
    logger.debug(bstack1l11l11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡷࡹࡧࡴࡦࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࡽࢀࠫಾ").format(str(e)))
  bstack1111l11ll_opy_(item, call, rep)
def bstack11l1lll1ll_opy_(driver, bstack11l1ll11l1_opy_, test=None):
  global bstack1l1llll1ll_opy_
  if test != None:
    bstack111l11lll_opy_ = getattr(test, bstack1l11l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ಿ"), None)
    bstack1lll1ll111_opy_ = getattr(test, bstack1l11l11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧೀ"), None)
    PercySDK.screenshot(driver, bstack11l1ll11l1_opy_, bstack111l11lll_opy_=bstack111l11lll_opy_, bstack1lll1ll111_opy_=bstack1lll1ll111_opy_, bstack1ll11ll111_opy_=bstack1l1llll1ll_opy_)
  else:
    PercySDK.screenshot(driver, bstack11l1ll11l1_opy_)
@measure(event_name=EVENTS.bstack11ll11l111_opy_, stage=STAGE.bstack1lll11l1_opy_, bstack1l1lll11l_opy_=bstack1lllll1ll_opy_)
def bstack1l11llll1l_opy_(driver):
  if bstack1l1l1l1l1_opy_.bstack111l1l111_opy_() is True or bstack1l1l1l1l1_opy_.capturing() is True:
    return
  bstack1l1l1l1l1_opy_.bstack11lll1111l_opy_()
  while not bstack1l1l1l1l1_opy_.bstack111l1l111_opy_():
    bstack111lllll1l_opy_ = bstack1l1l1l1l1_opy_.bstack1llllll11l_opy_()
    bstack11l1lll1ll_opy_(driver, bstack111lllll1l_opy_)
  bstack1l1l1l1l1_opy_.bstack111lll11_opy_()
def bstack1lll11lll1_opy_(sequence, driver_command, response = None, bstack1l11l1l11_opy_ = None, args = None):
    try:
      if sequence != bstack1l11l11_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪು"):
        return
      if percy.bstack1l1lll1ll_opy_() == bstack1l11l11_opy_ (u"ࠦ࡫ࡧ࡬ࡴࡧࠥೂ"):
        return
      bstack111lllll1l_opy_ = bstack1l111ll111_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨೃ"), None)
      for command in bstack11ll11l11_opy_:
        if command == driver_command:
          with bstack1l1lllllll_opy_:
            bstack1ll11lll_opy_ = bstack111lll1l1_opy_.copy()
          for driver in bstack1ll11lll_opy_:
            bstack1l11llll1l_opy_(driver)
      bstack1ll1l11111_opy_ = percy.bstack1l1ll111l_opy_()
      if driver_command in bstack1l11l1111_opy_[bstack1ll1l11111_opy_]:
        bstack1l1l1l1l1_opy_.bstack1l1llll1l_opy_(bstack111lllll1l_opy_, driver_command)
    except Exception as e:
      pass
def bstack1ll111ll1l_opy_(framework_name):
  if bstack11l11llll_opy_.get_property(bstack1l11l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪೄ")):
      return
  bstack11l11llll_opy_.bstack11l11ll1_opy_(bstack1l11l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟࡮ࡱࡧࡣࡨࡧ࡬࡭ࡧࡧࠫ೅"), True)
  global bstack1ll1l111ll_opy_
  global bstack1llll1l111_opy_
  global bstack11l111lll_opy_
  bstack1ll1l111ll_opy_ = framework_name
  logger.info(bstack11l1l111l_opy_.format(bstack1ll1l111ll_opy_.split(bstack1l11l11_opy_ (u"ࠨ࠯ࠪೆ"))[0]))
  bstack1ll11ll1ll_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1l1l11lll_opy_:
      Service.start = bstack1ll1l1ll_opy_
      Service.stop = bstack1111ll1ll_opy_
      webdriver.Remote.get = bstack1llllllll1_opy_
      WebDriver.quit = bstack1l1ll1ll1_opy_
      webdriver.Remote.__init__ = bstack1l1l111lll_opy_
    if not bstack1l1l11lll_opy_:
        webdriver.Remote.__init__ = bstack11lll1l111_opy_
    WebDriver.getAccessibilityResults = getAccessibilityResults
    WebDriver.get_accessibility_results = getAccessibilityResults
    WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
    WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
    WebDriver.performScan = perform_scan
    WebDriver.perform_scan = perform_scan
    WebDriver.execute = bstack1l1l1ll11_opy_
    bstack1llll1l111_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack1l1l11lll_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1l1ll111_opy_
  except Exception as e:
    pass
  bstack1llll1l1l1_opy_()
  if not bstack1llll1l111_opy_:
    bstack1ll11111ll_opy_(bstack1l11l11_opy_ (u"ࠤࡓࡥࡨࡱࡡࡨࡧࡶࠤࡳࡵࡴࠡ࡫ࡱࡷࡹࡧ࡬࡭ࡧࡧࠦೇ"), bstack11l1111lll_opy_)
  if bstack11l1111ll_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      if hasattr(RemoteConnection, bstack1l11l11_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫೈ")) and callable(getattr(RemoteConnection, bstack1l11l11_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬ೉"))):
        RemoteConnection._get_proxy_url = bstack1111ll111_opy_
      else:
        from selenium.webdriver.remote.client_config import ClientConfig
        ClientConfig.get_proxy_url = bstack1111ll111_opy_
    except Exception as e:
      logger.error(bstack11l1l11111_opy_.format(str(e)))
  if bstack1l1l11ll1l_opy_():
    bstack11lll111_opy_(CONFIG, logger)
  if (bstack1l11l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫೊ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if percy.bstack1l1lll1ll_opy_() == bstack1l11l11_opy_ (u"ࠨࡴࡳࡷࡨࠦೋ"):
          bstack11llll11l1_opy_(bstack1lll11lll1_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1l11lll111_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack11l11ll111_opy_
      except Exception as e:
        logger.warn(bstack111l1lll_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1ll1l11l_opy_
      except Exception as e:
        logger.debug(bstack1l1ll11ll_opy_ + str(e))
    except Exception as e:
      bstack1ll11111ll_opy_(e, bstack111l1lll_opy_)
    Output.start_test = bstack11l111l1_opy_
    Output.end_test = bstack1l111l1ll1_opy_
    TestStatus.__init__ = bstack1lll111ll1_opy_
    QueueItem.__init__ = bstack11ll11lll1_opy_
    pabot._create_items = bstack1ll1lll1l1_opy_
    try:
      from pabot import __version__ as bstack11l1111ll1_opy_
      if version.parse(bstack11l1111ll1_opy_) >= version.parse(bstack1l11l11_opy_ (u"ࠧ࠵࠰࠵࠲࠵࠭ೌ")):
        pabot._run = bstack11ll1llll1_opy_
      elif version.parse(bstack11l1111ll1_opy_) >= version.parse(bstack1l11l11_opy_ (u"ࠨ࠴࠱࠵࠺࠴࠰ࠨ್")):
        pabot._run = bstack11ll11ll1_opy_
      elif version.parse(bstack11l1111ll1_opy_) >= version.parse(bstack1l11l11_opy_ (u"ࠩ࠵࠲࠶࠹࠮࠱ࠩ೎")):
        pabot._run = bstack1lll11l1l1_opy_
      else:
        pabot._run = bstack11l1lllll1_opy_
    except Exception as e:
      pabot._run = bstack11l1lllll1_opy_
    pabot._create_command_for_execution = bstack1lllll1lll_opy_
    pabot._report_results = bstack1l11l1lll1_opy_
  if bstack1l11l11_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ೏") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll11111ll_opy_(e, bstack1l11ll1l11_opy_)
    Runner.run_hook = bstack111llll11_opy_
    Step.run = bstack1111l1lll_opy_
  if bstack1l11l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ೐") in str(framework_name).lower():
    if not bstack1l1l11lll_opy_:
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack111l1l11_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1l111lllll_opy_
      Config.getoption = bstack1ll11l1lll_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack11l1l111l1_opy_
    except Exception as e:
      pass
def bstack1ll1l1ll1l_opy_():
  global CONFIG
  if bstack1l11l11_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ೑") in CONFIG and int(CONFIG[bstack1l11l11_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭೒")]) > 1:
    logger.warn(bstack1l11l1llll_opy_)
def bstack1l11llll_opy_(arg, bstack11ll1l1l_opy_, bstack11ll11lll_opy_=None):
  global CONFIG
  global bstack11l1ll111_opy_
  global bstack1ll111111_opy_
  global bstack1l1l11lll_opy_
  global bstack11l11llll_opy_
  bstack11ll1111l1_opy_ = bstack1l11l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ೓")
  if bstack11ll1l1l_opy_ and isinstance(bstack11ll1l1l_opy_, str):
    bstack11ll1l1l_opy_ = eval(bstack11ll1l1l_opy_)
  CONFIG = bstack11ll1l1l_opy_[bstack1l11l11_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨ೔")]
  bstack11l1ll111_opy_ = bstack11ll1l1l_opy_[bstack1l11l11_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪೕ")]
  bstack1ll111111_opy_ = bstack11ll1l1l_opy_[bstack1l11l11_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬೖ")]
  bstack1l1l11lll_opy_ = bstack11ll1l1l_opy_[bstack1l11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ೗")]
  bstack11l11llll_opy_.bstack11l11ll1_opy_(bstack1l11l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭೘"), bstack1l1l11lll_opy_)
  os.environ[bstack1l11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ೙")] = bstack11ll1111l1_opy_
  os.environ[bstack1l11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌ࠭೚")] = json.dumps(CONFIG)
  os.environ[bstack1l11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡉࡗࡅࡣ࡚ࡘࡌࠨ೛")] = bstack11l1ll111_opy_
  os.environ[bstack1l11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ೜")] = str(bstack1ll111111_opy_)
  os.environ[bstack1l11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡐ࡚ࡍࡉࡏࠩೝ")] = str(True)
  if bstack11ll11l1l1_opy_(arg, [bstack1l11l11_opy_ (u"ࠫ࠲ࡴࠧೞ"), bstack1l11l11_opy_ (u"ࠬ࠳࠭࡯ࡷࡰࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭೟")]) != -1:
    os.environ[bstack1l11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡁࡓࡃࡏࡐࡊࡒࠧೠ")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1ll1lll11l_opy_)
    return
  bstack111lll1ll_opy_()
  global bstack11llll1ll1_opy_
  global bstack1l1llll1ll_opy_
  global bstack11ll111l1l_opy_
  global bstack1lll1ll11l_opy_
  global bstack1l111l1ll_opy_
  global bstack11l111lll_opy_
  global bstack1ll1l1l1l1_opy_
  arg.append(bstack1l11l11_opy_ (u"ࠢ࠮࡙ࠥೡ"))
  arg.append(bstack1l11l11_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡥ࠻ࡏࡲࡨࡺࡲࡥࠡࡣ࡯ࡶࡪࡧࡤࡺࠢ࡬ࡱࡵࡵࡲࡵࡧࡧ࠾ࡵࡿࡴࡦࡵࡷ࠲ࡕࡿࡴࡦࡵࡷ࡛ࡦࡸ࡮ࡪࡰࡪࠦೢ"))
  arg.append(bstack1l11l11_opy_ (u"ࠤ࠰࡛ࠧೣ"))
  arg.append(bstack1l11l11_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧ࠽ࡘ࡭࡫ࠠࡩࡱࡲ࡯࡮ࡳࡰ࡭ࠤ೤"))
  global bstack1lll1l1ll_opy_
  global bstack11ll1l1l1l_opy_
  global bstack1ll11l1111_opy_
  global bstack1l1111l11_opy_
  global bstack1lll1l111_opy_
  global bstack1ll111l11l_opy_
  global bstack1l1ll1ll1l_opy_
  global bstack11ll1l111l_opy_
  global bstack1l111ll1l_opy_
  global bstack1l1ll1l111_opy_
  global bstack1l1111lll1_opy_
  global bstack11llll1l11_opy_
  global bstack1111l11ll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1lll1l1ll_opy_ = webdriver.Remote.__init__
    bstack11ll1l1l1l_opy_ = WebDriver.quit
    bstack11ll1l111l_opy_ = WebDriver.close
    bstack1l111ll1l_opy_ = WebDriver.get
    bstack1ll11l1111_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1l111l11_opy_(CONFIG) and bstack1l11l1l1ll_opy_():
    if bstack11l1l111_opy_() < version.parse(bstack111111l1l_opy_):
      logger.error(bstack1l1lll1l1_opy_.format(bstack11l1l111_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack1l11l11_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬ೥")) and callable(getattr(RemoteConnection, bstack1l11l11_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭೦"))):
          bstack1l1ll1l111_opy_ = RemoteConnection._get_proxy_url
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          bstack1l1ll1l111_opy_ = ClientConfig.get_proxy_url
      except Exception as e:
        logger.error(bstack11l1l11111_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1l1111lll1_opy_ = Config.getoption
    from _pytest import runner
    bstack11llll1l11_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack11lll1ll_opy_)
  try:
    from pytest_bdd import reporting
    bstack1111l11ll_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack1l11l11_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧ೧"))
  bstack11ll111l1l_opy_ = CONFIG.get(bstack1l11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ೨"), {}).get(bstack1l11l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ೩"))
  bstack1ll1l1l1l1_opy_ = True
  if cli.is_enabled(CONFIG):
    if cli.bstack11lll1lll_opy_():
      bstack1llll1lll_opy_.invoke(bstack11ll11l1l_opy_.CONNECT, bstack1ll1l1l1ll_opy_())
    platform_index = int(os.environ.get(bstack1l11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ೪"), bstack1l11l11_opy_ (u"ࠪ࠴ࠬ೫")))
  else:
    bstack1ll111ll1l_opy_(bstack11lll11ll_opy_)
  os.environ[bstack1l11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬ೬")] = CONFIG[bstack1l11l11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ೭")]
  os.environ[bstack1l11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩ೮")] = CONFIG[bstack1l11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ೯")]
  os.environ[bstack1l11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫ೰")] = bstack1l1l11lll_opy_.__str__()
  from _pytest.config import main as bstack1111ll1l1_opy_
  bstack1l11lll11l_opy_ = []
  try:
    exit_code = bstack1111ll1l1_opy_(arg)
    if cli.is_enabled(CONFIG):
      cli.bstack1lll1l1l_opy_()
    if bstack1l11l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠭ೱ") in multiprocessing.current_process().__dict__.keys():
      for bstack1ll11l11l1_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1l11lll11l_opy_.append(bstack1ll11l11l1_opy_)
    try:
      bstack1ll1ll111l_opy_ = (bstack1l11lll11l_opy_, int(exit_code))
      bstack11ll11lll_opy_.append(bstack1ll1ll111l_opy_)
    except:
      bstack11ll11lll_opy_.append((bstack1l11lll11l_opy_, exit_code))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack1l11lll11l_opy_.append({bstack1l11l11_opy_ (u"ࠪࡲࡦࡳࡥࠨೲ"): bstack1l11l11_opy_ (u"ࠫࡕࡸ࡯ࡤࡧࡶࡷࠥ࠭ೳ") + os.environ.get(bstack1l11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ೴")), bstack1l11l11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ೵"): traceback.format_exc(), bstack1l11l11_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭೶"): int(os.environ.get(bstack1l11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ೷")))})
    bstack11ll11lll_opy_.append((bstack1l11lll11l_opy_, 1))
def mod_behave_main(args, retries):
  try:
    from behave.configuration import Configuration
    from behave.__main__ import run_behave
    from browserstack_sdk.bstack_behave_runner import BehaveRunner
    config = Configuration(args)
    config.update_userdata({bstack1l11l11_opy_ (u"ࠤࡵࡩࡹࡸࡩࡦࡵࠥ೸"): str(retries)})
    return run_behave(config, runner_class=BehaveRunner)
  except Exception as e:
    bstack111ll111_opy_ = e.__class__.__name__
    print(bstack1l11l11_opy_ (u"ࠥࠩࡸࡀࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡵࡧࡶࡸࠥࠫࡳࠣ೹") % (bstack111ll111_opy_, e))
    return 1
def bstack1lll1llll1_opy_(arg):
  global bstack11llllllll_opy_
  bstack1ll111ll1l_opy_(bstack1l1l11ll_opy_)
  os.environ[bstack1l11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ೺")] = str(bstack1ll111111_opy_)
  retries = bstack11l11l1lll_opy_.bstack1l1lll11l1_opy_(CONFIG)
  status_code = 0
  if bstack11l11l1lll_opy_.bstack1l11ll1l1l_opy_(CONFIG):
    status_code = mod_behave_main(arg, retries)
  else:
    from behave.__main__ import main as bstack11lll1llll_opy_
    status_code = bstack11lll1llll_opy_(arg)
  if status_code != 0:
    bstack11llllllll_opy_ = status_code
def bstack1ll1111l11_opy_():
  logger.info(bstack1llll1ll1_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1l11l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ೻"), help=bstack1l11l11_opy_ (u"࠭ࡇࡦࡰࡨࡶࡦࡺࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡤࡱࡱࡪ࡮࡭ࠧ೼"))
  parser.add_argument(bstack1l11l11_opy_ (u"ࠧ࠮ࡷࠪ೽"), bstack1l11l11_opy_ (u"ࠨ࠯࠰ࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬ೾"), help=bstack1l11l11_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡵࡴࡧࡵࡲࡦࡳࡥࠨ೿"))
  parser.add_argument(bstack1l11l11_opy_ (u"ࠪ࠱ࡰ࠭ഀ"), bstack1l11l11_opy_ (u"ࠫ࠲࠳࡫ࡦࡻࠪഁ"), help=bstack1l11l11_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡤࡧࡨ࡫ࡳࡴࠢ࡮ࡩࡾ࠭ം"))
  parser.add_argument(bstack1l11l11_opy_ (u"࠭࠭ࡧࠩഃ"), bstack1l11l11_opy_ (u"ࠧ࠮࠯ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬഄ"), help=bstack1l11l11_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧഅ"))
  bstack11l1ll1l_opy_ = parser.parse_args()
  try:
    bstack11l1llll_opy_ = bstack1l11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡩࡨࡲࡪࡸࡩࡤ࠰ࡼࡱࡱ࠴ࡳࡢ࡯ࡳࡰࡪ࠭ആ")
    if bstack11l1ll1l_opy_.framework and bstack11l1ll1l_opy_.framework not in (bstack1l11l11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪഇ"), bstack1l11l11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬഈ")):
      bstack11l1llll_opy_ = bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠮ࡺ࡯࡯࠲ࡸࡧ࡭ࡱ࡮ࡨࠫഉ")
    bstack1ll1111ll1_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11l1llll_opy_)
    bstack11ll1ll1_opy_ = open(bstack1ll1111ll1_opy_, bstack1l11l11_opy_ (u"࠭ࡲࠨഊ"))
    bstack1l11lllll1_opy_ = bstack11ll1ll1_opy_.read()
    bstack11ll1ll1_opy_.close()
    if bstack11l1ll1l_opy_.username:
      bstack1l11lllll1_opy_ = bstack1l11lllll1_opy_.replace(bstack1l11l11_opy_ (u"࡚ࠧࡑࡘࡖࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧഋ"), bstack11l1ll1l_opy_.username)
    if bstack11l1ll1l_opy_.key:
      bstack1l11lllll1_opy_ = bstack1l11lllll1_opy_.replace(bstack1l11l11_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪഌ"), bstack11l1ll1l_opy_.key)
    if bstack11l1ll1l_opy_.framework:
      bstack1l11lllll1_opy_ = bstack1l11lllll1_opy_.replace(bstack1l11l11_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪ഍"), bstack11l1ll1l_opy_.framework)
    file_name = bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭എ")
    file_path = os.path.abspath(file_name)
    bstack11ll111lll_opy_ = open(file_path, bstack1l11l11_opy_ (u"ࠫࡼ࠭ഏ"))
    bstack11ll111lll_opy_.write(bstack1l11lllll1_opy_)
    bstack11ll111lll_opy_.close()
    logger.info(bstack1l111ll1l1_opy_)
    try:
      os.environ[bstack1l11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧഐ")] = bstack11l1ll1l_opy_.framework if bstack11l1ll1l_opy_.framework != None else bstack1l11l11_opy_ (u"ࠨࠢ഑")
      config = yaml.safe_load(bstack1l11lllll1_opy_)
      config[bstack1l11l11_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧഒ")] = bstack1l11l11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡵࡨࡸࡺࡶࠧഓ")
      bstack11l11lll11_opy_(bstack1ll11l1l11_opy_, config)
    except Exception as e:
      logger.debug(bstack1l1ll1lll_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1ll111ll_opy_.format(str(e)))
def bstack11l11lll11_opy_(bstack11l1l1ll_opy_, config, bstack11l11lll1l_opy_={}):
  global bstack1l1l11lll_opy_
  global bstack11llll111_opy_
  global bstack11l11llll_opy_
  if not config:
    return
  bstack1111llll_opy_ = bstack1lll1111l_opy_ if not bstack1l1l11lll_opy_ else (
    bstack1lll11ll1_opy_ if bstack1l11l11_opy_ (u"ࠩࡤࡴࡵ࠭ഔ") in config else (
        bstack1ll111111l_opy_ if config.get(bstack1l11l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧക")) else bstack1l1lll1111_opy_
    )
)
  bstack1l11ll1ll_opy_ = False
  bstack1ll11l1l_opy_ = False
  if bstack1l1l11lll_opy_ is True:
      if bstack1l11l11_opy_ (u"ࠫࡦࡶࡰࠨഖ") in config:
          bstack1l11ll1ll_opy_ = True
      else:
          bstack1ll11l1l_opy_ = True
  bstack1lll11l111_opy_ = bstack11111l1l_opy_.bstack1lllllll1l_opy_(config, bstack11llll111_opy_)
  bstack1l111llll_opy_ = bstack1l11l1111l_opy_()
  data = {
    bstack1l11l11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧഗ"): config[bstack1l11l11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨഘ")],
    bstack1l11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪങ"): config[bstack1l11l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫച")],
    bstack1l11l11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ഛ"): bstack11l1l1ll_opy_,
    bstack1l11l11_opy_ (u"ࠪࡨࡪࡺࡥࡤࡶࡨࡨࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧജ"): os.environ.get(bstack1l11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ഝ"), bstack11llll111_opy_),
    bstack1l11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧഞ"): bstack11lll1ll11_opy_,
    bstack1l11l11_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬ࠨട"): bstack11l1l1111l_opy_(),
    bstack1l11l11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪഠ"): {
      bstack1l11l11_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ഡ"): str(config[bstack1l11l11_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩഢ")]) if bstack1l11l11_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪണ") in config else bstack1l11l11_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧത"),
      bstack1l11l11_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࡖࡦࡴࡶ࡭ࡴࡴࠧഥ"): sys.version,
      bstack1l11l11_opy_ (u"࠭ࡲࡦࡨࡨࡶࡷ࡫ࡲࠨദ"): bstack1ll1l1lll_opy_(os.environ.get(bstack1l11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩധ"), bstack11llll111_opy_)),
      bstack1l11l11_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪന"): bstack1l11l11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩഩ"),
      bstack1l11l11_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫപ"): bstack1111llll_opy_,
      bstack1l11l11_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩഫ"): bstack1lll11l111_opy_,
      bstack1l11l11_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡥࡵࡶ࡫ࡧࠫബ"): os.environ[bstack1l11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫഭ")],
      bstack1l11l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪമ"): os.environ.get(bstack1l11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪയ"), bstack11llll111_opy_),
      bstack1l11l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬര"): bstack11ll1ll1l1_opy_(os.environ.get(bstack1l11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬറ"), bstack11llll111_opy_)),
      bstack1l11l11_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪല"): bstack1l111llll_opy_.get(bstack1l11l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪള")),
      bstack1l11l11_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬഴ"): bstack1l111llll_opy_.get(bstack1l11l11_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨവ")),
      bstack1l11l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫശ"): config[bstack1l11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬഷ")] if config[bstack1l11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭സ")] else bstack1l11l11_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧഹ"),
      bstack1l11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧഺ"): str(config[bstack1l11l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ഻")]) if bstack1l11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳ഼ࠩ") in config else bstack1l11l11_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤഽ"),
      bstack1l11l11_opy_ (u"ࠩࡲࡷࠬാ"): sys.platform,
      bstack1l11l11_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬി"): socket.gethostname(),
      bstack1l11l11_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭ീ"): bstack11l11llll_opy_.get_property(bstack1l11l11_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪࠧു"))
    }
  }
  if not bstack11l11llll_opy_.get_property(bstack1l11l11_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭ൂ")) is None:
    data[bstack1l11l11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪൃ")][bstack1l11l11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡐࡩࡹࡧࡤࡢࡶࡤࠫൄ")] = {
      bstack1l11l11_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩ൅"): bstack1l11l11_opy_ (u"ࠪࡹࡸ࡫ࡲࡠ࡭࡬ࡰࡱ࡫ࡤࠨെ"),
      bstack1l11l11_opy_ (u"ࠫࡸ࡯ࡧ࡯ࡣ࡯ࠫേ"): bstack11l11llll_opy_.get_property(bstack1l11l11_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬൈ")),
      bstack1l11l11_opy_ (u"࠭ࡳࡪࡩࡱࡥࡱࡔࡵ࡮ࡤࡨࡶࠬ൉"): bstack11l11llll_opy_.get_property(bstack1l11l11_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡏࡱࠪൊ"))
    }
  if bstack11l1l1ll_opy_ == bstack1111ll11_opy_:
    data[bstack1l11l11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫോ")][bstack1l11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡄࡱࡱࡪ࡮࡭ࠧൌ")] = bstack1ll1ll1l1_opy_(config)
    data[bstack1l11l11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ്࠭")][bstack1l11l11_opy_ (u"ࠫ࡮ࡹࡐࡦࡴࡦࡽࡆࡻࡴࡰࡇࡱࡥࡧࡲࡥࡥࠩൎ")] = percy.bstack11l111l1l1_opy_
    data[bstack1l11l11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨ൏")][bstack1l11l11_opy_ (u"࠭ࡰࡦࡴࡦࡽࡇࡻࡩ࡭ࡦࡌࡨࠬ൐")] = percy.percy_build_id
  if not bstack11l11l1lll_opy_.bstack11l111l11l_opy_(CONFIG):
    data[bstack1l11l11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪ൑")][bstack1l11l11_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠬ൒")] = bstack11l11l1lll_opy_.bstack11l111l11l_opy_(CONFIG)
  bstack1l1l1l11l_opy_ = bstack1ll1lll111_opy_.bstack11l111llll_opy_(CONFIG, logger)
  bstack1111111l_opy_ = bstack11l11l1lll_opy_.bstack11l111llll_opy_(config=CONFIG)
  if bstack1l1l1l11l_opy_ is not None and bstack1111111l_opy_ is not None and bstack1111111l_opy_.bstack11l1l1lll1_opy_():
    data[bstack1l11l11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬ൓")][bstack1111111l_opy_.bstack1ll11111_opy_()] = bstack1l1l1l11l_opy_.bstack1ll11l11l_opy_()
  update(data[bstack1l11l11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭ൔ")], bstack11l11lll1l_opy_)
  try:
    response = bstack1l11lllll_opy_(bstack1l11l11_opy_ (u"ࠫࡕࡕࡓࡕࠩൕ"), bstack11lll11l1l_opy_(bstack11ll1l11l1_opy_), data, {
      bstack1l11l11_opy_ (u"ࠬࡧࡵࡵࡪࠪൖ"): (config[bstack1l11l11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨൗ")], config[bstack1l11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ൘")])
    })
    if response:
      logger.debug(bstack11l111l1l_opy_.format(bstack11l1l1ll_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack111llllll_opy_.format(str(e)))
def bstack1ll1l1lll_opy_(framework):
  return bstack1l11l11_opy_ (u"ࠣࡽࢀ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࡾࢁࠧ൙").format(str(framework), __version__) if framework else bstack1l11l11_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࡼࡿࠥ൚").format(
    __version__)
def bstack111lll1ll_opy_():
  global CONFIG
  global bstack111l1ll11_opy_
  if bool(CONFIG):
    return
  try:
    bstack11l1l11l1l_opy_()
    logger.debug(bstack1lll1lll1l_opy_.format(str(CONFIG)))
    bstack111l1ll11_opy_ = bstack1l1ll11lll_opy_.bstack1llll111l1_opy_(CONFIG, bstack111l1ll11_opy_)
    bstack1ll11ll1ll_opy_()
  except Exception as e:
    logger.error(bstack1l11l11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࡸࡴ࠱ࠦࡥࡳࡴࡲࡶ࠿ࠦࠢ൛") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1llll11ll_opy_
  atexit.register(bstack11lll11l1_opy_)
  signal.signal(signal.SIGINT, bstack11l11l1ll1_opy_)
  signal.signal(signal.SIGTERM, bstack11l11l1ll1_opy_)
def bstack1llll11ll_opy_(exctype, value, traceback):
  global bstack111lll1l1_opy_
  try:
    for driver in bstack111lll1l1_opy_:
      bstack1l1l11l1ll_opy_(driver, bstack1l11l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ൜"), bstack1l11l11_opy_ (u"࡙ࠧࡥࡴࡵ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࡢ࡮ࠣ൝") + str(value))
  except Exception:
    pass
  logger.info(bstack11llll1ll_opy_)
  bstack1l1111ll11_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1l1111ll11_opy_(message=bstack1l11l11_opy_ (u"࠭ࠧ൞"), bstack11l11l1l_opy_ = False):
  global CONFIG
  bstack1l111l1l1l_opy_ = bstack1l11l11_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠩൟ") if bstack11l11l1l_opy_ else bstack1l11l11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧൠ")
  try:
    if message:
      bstack11l11lll1l_opy_ = {
        bstack1l111l1l1l_opy_ : str(message)
      }
      bstack11l11lll11_opy_(bstack1111ll11_opy_, CONFIG, bstack11l11lll1l_opy_)
    else:
      bstack11l11lll11_opy_(bstack1111ll11_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack11lllllll1_opy_.format(str(e)))
def bstack1ll1l11ll1_opy_(bstack1111111l1_opy_, size):
  bstack11ll1lllll_opy_ = []
  while len(bstack1111111l1_opy_) > size:
    bstack1lllll11l1_opy_ = bstack1111111l1_opy_[:size]
    bstack11ll1lllll_opy_.append(bstack1lllll11l1_opy_)
    bstack1111111l1_opy_ = bstack1111111l1_opy_[size:]
  bstack11ll1lllll_opy_.append(bstack1111111l1_opy_)
  return bstack11ll1lllll_opy_
def bstack1l11111l11_opy_(args):
  if bstack1l11l11_opy_ (u"ࠩ࠰ࡱࠬൡ") in args and bstack1l11l11_opy_ (u"ࠪࡴࡩࡨࠧൢ") in args:
    return True
  return False
@measure(event_name=EVENTS.bstack11ll1ll1l_opy_, stage=STAGE.bstack11l1l11l_opy_)
def run_on_browserstack(bstack11ll1ll11l_opy_=None, bstack11ll11lll_opy_=None, bstack1l1lll1l11_opy_=False):
  global CONFIG
  global bstack11l1ll111_opy_
  global bstack1ll111111_opy_
  global bstack11llll111_opy_
  global bstack11l11llll_opy_
  bstack11ll1111l1_opy_ = bstack1l11l11_opy_ (u"ࠫࠬൣ")
  bstack11l11ll1l1_opy_(bstack1llll1111_opy_, logger)
  if bstack11ll1ll11l_opy_ and isinstance(bstack11ll1ll11l_opy_, str):
    bstack11ll1ll11l_opy_ = eval(bstack11ll1ll11l_opy_)
  if bstack11ll1ll11l_opy_:
    CONFIG = bstack11ll1ll11l_opy_[bstack1l11l11_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬ൤")]
    bstack11l1ll111_opy_ = bstack11ll1ll11l_opy_[bstack1l11l11_opy_ (u"࠭ࡈࡖࡄࡢ࡙ࡗࡒࠧ൥")]
    bstack1ll111111_opy_ = bstack11ll1ll11l_opy_[bstack1l11l11_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ൦")]
    bstack11l11llll_opy_.bstack11l11ll1_opy_(bstack1l11l11_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ൧"), bstack1ll111111_opy_)
    bstack11ll1111l1_opy_ = bstack1l11l11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ൨")
  bstack11l11llll_opy_.bstack11l11ll1_opy_(bstack1l11l11_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࠬ൩"), uuid4().__str__())
  logger.info(bstack1l11l11_opy_ (u"ࠫࡘࡊࡋࠡࡴࡸࡲࠥࡹࡴࡢࡴࡷࡩࡩࠦࡷࡪࡶ࡫ࠤ࡮ࡪ࠺ࠡࠩ൪") + bstack11l11llll_opy_.get_property(bstack1l11l11_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪࠧ൫")));
  logger.debug(bstack1l11l11_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤ࠾ࠩ൬") + bstack11l11llll_opy_.get_property(bstack1l11l11_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥࠩ൭")))
  if not bstack1l1lll1l11_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1ll1lll11l_opy_)
      return
    if sys.argv[1] == bstack1l11l11_opy_ (u"ࠨ࠯࠰ࡺࡪࡸࡳࡪࡱࡱࠫ൮") or sys.argv[1] == bstack1l11l11_opy_ (u"ࠩ࠰ࡺࠬ൯"):
      logger.info(bstack1l11l11_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡓࡽࡹ࡮࡯࡯ࠢࡖࡈࡐࠦࡶࡼࡿࠪ൰").format(__version__))
      return
    if sys.argv[1] == bstack1l11l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ൱"):
      bstack1ll1111l11_opy_()
      return
  args = sys.argv
  bstack111lll1ll_opy_()
  global bstack11llll1ll1_opy_
  global bstack1ll1l111l1_opy_
  global bstack1ll1l1l1l1_opy_
  global bstack1l11111lll_opy_
  global bstack1l1llll1ll_opy_
  global bstack11ll111l1l_opy_
  global bstack1lll1ll11l_opy_
  global bstack1l11111l_opy_
  global bstack1l111l1ll_opy_
  global bstack11l111lll_opy_
  global bstack11l1llll1l_opy_
  bstack1ll1l111l1_opy_ = len(CONFIG.get(bstack1l11l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ൲"), []))
  if not bstack11ll1111l1_opy_:
    if args[1] == bstack1l11l11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭൳") or args[1] == bstack1l11l11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨ൴"):
      bstack11ll1111l1_opy_ = bstack1l11l11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ൵")
      args = args[2:]
    elif args[1] == bstack1l11l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ൶"):
      bstack11ll1111l1_opy_ = bstack1l11l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ൷")
      args = args[2:]
    elif args[1] == bstack1l11l11_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ൸"):
      bstack11ll1111l1_opy_ = bstack1l11l11_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ൹")
      args = args[2:]
    elif args[1] == bstack1l11l11_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧൺ"):
      bstack11ll1111l1_opy_ = bstack1l11l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨൻ")
      args = args[2:]
    elif args[1] == bstack1l11l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨർ"):
      bstack11ll1111l1_opy_ = bstack1l11l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩൽ")
      args = args[2:]
    elif args[1] == bstack1l11l11_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪൾ"):
      bstack11ll1111l1_opy_ = bstack1l11l11_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫൿ")
      args = args[2:]
    else:
      if not bstack1l11l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ඀") in CONFIG or str(CONFIG[bstack1l11l11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩඁ")]).lower() in [bstack1l11l11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧං"), bstack1l11l11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩඃ")]:
        bstack11ll1111l1_opy_ = bstack1l11l11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ඄")
        args = args[1:]
      elif str(CONFIG[bstack1l11l11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭අ")]).lower() == bstack1l11l11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪආ"):
        bstack11ll1111l1_opy_ = bstack1l11l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫඇ")
        args = args[1:]
      elif str(CONFIG[bstack1l11l11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩඈ")]).lower() == bstack1l11l11_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ඉ"):
        bstack11ll1111l1_opy_ = bstack1l11l11_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧඊ")
        args = args[1:]
      elif str(CONFIG[bstack1l11l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬඋ")]).lower() == bstack1l11l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪඌ"):
        bstack11ll1111l1_opy_ = bstack1l11l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫඍ")
        args = args[1:]
      elif str(CONFIG[bstack1l11l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨඎ")]).lower() == bstack1l11l11_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ඏ"):
        bstack11ll1111l1_opy_ = bstack1l11l11_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧඐ")
        args = args[1:]
      else:
        os.environ[bstack1l11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪඑ")] = bstack11ll1111l1_opy_
        bstack11l11l1l11_opy_(bstack1llll1lll1_opy_)
  os.environ[bstack1l11l11_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪඒ")] = bstack11ll1111l1_opy_
  bstack11llll111_opy_ = bstack11ll1111l1_opy_
  if cli.is_enabled(CONFIG):
    try:
      bstack1ll1llll11_opy_ = bstack111l11ll1_opy_[bstack1l11l11_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖ࠰ࡆࡉࡊࠧඓ")] if bstack11ll1111l1_opy_ == bstack1l11l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫඔ") and bstack1l1l11ll1_opy_() else bstack11ll1111l1_opy_
      bstack1llll1lll_opy_.invoke(bstack11ll11l1l_opy_.bstack1llll1l1l_opy_, bstack1111l1l11_opy_(
        sdk_version=__version__,
        path_config=bstack1ll1ll1l1l_opy_(),
        path_project=os.getcwd(),
        test_framework=bstack1ll1llll11_opy_,
        frameworks=[bstack1ll1llll11_opy_],
        framework_versions={
          bstack1ll1llll11_opy_: bstack11ll1ll1l1_opy_(bstack1l11l11_opy_ (u"ࠬࡘ࡯ࡣࡱࡷࠫඕ") if bstack11ll1111l1_opy_ in [bstack1l11l11_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬඖ"), bstack1l11l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭඗"), bstack1l11l11_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ඘")] else bstack11ll1111l1_opy_)
        },
        bs_config=CONFIG
      ))
      if cli.config.get(bstack1l11l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠦ඙"), None):
        CONFIG[bstack1l11l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧක")] = cli.config.get(bstack1l11l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࠨඛ"), None)
    except Exception as e:
      bstack1llll1lll_opy_.invoke(bstack11ll11l1l_opy_.bstack11lll11l_opy_, e.__traceback__, 1)
    if bstack1ll111111_opy_:
      CONFIG[bstack1l11l11_opy_ (u"ࠧࡧࡰࡱࠤග")] = cli.config[bstack1l11l11_opy_ (u"ࠨࡡࡱࡲࠥඝ")]
      logger.info(bstack1lll1l11ll_opy_.format(CONFIG[bstack1l11l11_opy_ (u"ࠧࡢࡲࡳࠫඞ")]))
  else:
    bstack1llll1lll_opy_.clear()
  global bstack11l11l111l_opy_
  global bstack111lll111_opy_
  if bstack11ll1ll11l_opy_:
    try:
      bstack1l11l11111_opy_ = datetime.datetime.now()
      os.environ[bstack1l11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪඟ")] = bstack11ll1111l1_opy_
      bstack11l11lll11_opy_(bstack1l1111llll_opy_, CONFIG)
      cli.bstack1l1l1l1l1l_opy_(bstack1l11l11_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺ࡴࡦ࡮ࡣࡹ࡫ࡳࡵࡡࡤࡸࡹ࡫࡭ࡱࡶࡨࡨࠧච"), datetime.datetime.now() - bstack1l11l11111_opy_)
    except Exception as e:
      logger.debug(bstack11l111111l_opy_.format(str(e)))
  global bstack1lll1l1ll_opy_
  global bstack11ll1l1l1l_opy_
  global bstack1111l1111_opy_
  global bstack11111111_opy_
  global bstack1llll1ll11_opy_
  global bstack1lllll11ll_opy_
  global bstack1l1111l11_opy_
  global bstack1lll1l111_opy_
  global bstack11l1l11ll_opy_
  global bstack1ll111l11l_opy_
  global bstack1l1ll1ll1l_opy_
  global bstack11ll1l111l_opy_
  global bstack11ll11l1_opy_
  global bstack111lll1l_opy_
  global bstack1l111ll1l_opy_
  global bstack1l1ll1l111_opy_
  global bstack1l1111lll1_opy_
  global bstack11llll1l11_opy_
  global bstack111ll1l1_opy_
  global bstack1111l11ll_opy_
  global bstack1ll11l1111_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1lll1l1ll_opy_ = webdriver.Remote.__init__
    bstack11ll1l1l1l_opy_ = WebDriver.quit
    bstack11ll1l111l_opy_ = WebDriver.close
    bstack1l111ll1l_opy_ = WebDriver.get
    bstack1ll11l1111_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack11l11l111l_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack1l1ll111l1_opy_
    bstack111lll111_opy_ = bstack1l1ll111l1_opy_()
  except Exception as e:
    pass
  try:
    global bstack1ll111ll1_opy_
    from QWeb.keywords import browser
    bstack1ll111ll1_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1l111l11_opy_(CONFIG) and bstack1l11l1l1ll_opy_():
    if bstack11l1l111_opy_() < version.parse(bstack111111l1l_opy_):
      logger.error(bstack1l1lll1l1_opy_.format(bstack11l1l111_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack1l11l11_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫඡ")) and callable(getattr(RemoteConnection, bstack1l11l11_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬජ"))):
          RemoteConnection._get_proxy_url = bstack1111ll111_opy_
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          ClientConfig.get_proxy_url = bstack1111ll111_opy_
      except Exception as e:
        logger.error(bstack11l1l11111_opy_.format(str(e)))
  if not CONFIG.get(bstack1l11l11_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧඣ"), False) and not bstack11ll1ll11l_opy_:
    logger.info(bstack11ll11ll1l_opy_)
  if not cli.is_enabled(CONFIG):
    if bstack1l11l11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪඤ") in CONFIG and str(CONFIG[bstack1l11l11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫඥ")]).lower() != bstack1l11l11_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧඦ"):
      bstack1lll111l1_opy_()
    elif bstack11ll1111l1_opy_ != bstack1l11l11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩට") or (bstack11ll1111l1_opy_ == bstack1l11l11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪඨ") and not bstack11ll1ll11l_opy_):
      bstack1ll1lllll_opy_()
  if (bstack11ll1111l1_opy_ in [bstack1l11l11_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪඩ"), bstack1l11l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫඪ"), bstack1l11l11_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧණ")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1l11lll111_opy_
        bstack1lllll11ll_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack111l1lll_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1llll1ll11_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1l1ll11ll_opy_ + str(e))
    except Exception as e:
      bstack1ll11111ll_opy_(e, bstack111l1lll_opy_)
    if bstack11ll1111l1_opy_ != bstack1l11l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨඬ"):
      bstack111llllll1_opy_()
    bstack1111l1111_opy_ = Output.start_test
    bstack11111111_opy_ = Output.end_test
    bstack1l1111l11_opy_ = TestStatus.__init__
    bstack11l1l11ll_opy_ = pabot._run
    bstack1ll111l11l_opy_ = QueueItem.__init__
    bstack1l1ll1ll1l_opy_ = pabot._create_command_for_execution
    bstack111ll1l1_opy_ = pabot._report_results
  if bstack11ll1111l1_opy_ == bstack1l11l11_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨත"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll11111ll_opy_(e, bstack1l11ll1l11_opy_)
    bstack11ll11l1_opy_ = Runner.run_hook
    bstack111lll1l_opy_ = Step.run
  if bstack11ll1111l1_opy_ == bstack1l11l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩථ"):
    try:
      from _pytest.config import Config
      bstack1l1111lll1_opy_ = Config.getoption
      from _pytest import runner
      bstack11llll1l11_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack11lll1ll_opy_)
    try:
      from pytest_bdd import reporting
      bstack1111l11ll_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1l11l11_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡲࠤࡷࡻ࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࡶࠫද"))
  try:
    framework_name = bstack1l11l11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪධ") if bstack11ll1111l1_opy_ in [bstack1l11l11_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫන"), bstack1l11l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ඲"), bstack1l11l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨඳ")] else bstack11l1lll11l_opy_(bstack11ll1111l1_opy_)
    bstack11llll11ll_opy_ = {
      bstack1l11l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࠩප"): bstack1l11l11_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫඵ") if bstack11ll1111l1_opy_ == bstack1l11l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪබ") and bstack1l1l11ll1_opy_() else framework_name,
      bstack1l11l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨභ"): bstack11ll1ll1l1_opy_(framework_name),
      bstack1l11l11_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪම"): __version__,
      bstack1l11l11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡸࡷࡪࡪࠧඹ"): bstack11ll1111l1_opy_
    }
    if bstack11ll1111l1_opy_ in bstack1111llll1_opy_ + bstack1l11l11lll_opy_:
      if bstack1ll1ll1l11_opy_.bstack1ll11ll11_opy_(CONFIG):
        if bstack1l11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧය") in CONFIG:
          os.environ[bstack1l11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩර")] = os.getenv(bstack1l11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ඼"), json.dumps(CONFIG[bstack1l11l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪල")]))
          CONFIG[bstack1l11l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ඾")].pop(bstack1l11l11_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ඿"), None)
          CONFIG[bstack1l11l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ව")].pop(bstack1l11l11_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬශ"), None)
        bstack11llll11ll_opy_[bstack1l11l11_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨෂ")] = {
          bstack1l11l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧස"): bstack1l11l11_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬහ"),
          bstack1l11l11_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬළ"): str(bstack11l1l111_opy_())
        }
    if bstack11ll1111l1_opy_ not in [bstack1l11l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ෆ")] and not cli.is_running():
      bstack1l11l1ll1_opy_, bstack1ll1l11l1l_opy_ = bstack11ll111ll1_opy_.launch(CONFIG, bstack11llll11ll_opy_)
      if bstack1ll1l11l1l_opy_.get(bstack1l11l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭෇")) is not None and bstack1ll1ll1l11_opy_.bstack11l11l11l_opy_(CONFIG) is None:
        value = bstack1ll1l11l1l_opy_[bstack1l11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ෈")].get(bstack1l11l11_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩ෉"))
        if value is not None:
            CONFIG[bstack1l11l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺ්ࠩ")] = value
        else:
          logger.debug(bstack1l11l11_opy_ (u"ࠥࡒࡴࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡤࡢࡶࡤࠤ࡫ࡵࡵ࡯ࡦࠣ࡭ࡳࠦࡲࡦࡵࡳࡳࡳࡹࡥࠣ෋"))
  except Exception as e:
    logger.debug(bstack1ll1l11ll_opy_.format(bstack1l11l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡊࡸࡦࠬ෌"), str(e)))
  if bstack11ll1111l1_opy_ == bstack1l11l11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ෍"):
    bstack1ll1l1l1l1_opy_ = True
    if bstack11ll1ll11l_opy_ and bstack1l1lll1l11_opy_:
      bstack11ll111l1l_opy_ = CONFIG.get(bstack1l11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ෎"), {}).get(bstack1l11l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩා"))
      bstack1ll111ll1l_opy_(bstack1l1l1111ll_opy_)
    elif bstack11ll1ll11l_opy_:
      bstack11ll111l1l_opy_ = CONFIG.get(bstack1l11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬැ"), {}).get(bstack1l11l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫෑ"))
      global bstack111lll1l1_opy_
      try:
        if bstack1l11111l11_opy_(bstack11ll1ll11l_opy_[bstack1l11l11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ි")]) and multiprocessing.current_process().name == bstack1l11l11_opy_ (u"ࠫ࠵࠭ී"):
          bstack11ll1ll11l_opy_[bstack1l11l11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨු")].remove(bstack1l11l11_opy_ (u"࠭࠭࡮ࠩ෕"))
          bstack11ll1ll11l_opy_[bstack1l11l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪූ")].remove(bstack1l11l11_opy_ (u"ࠨࡲࡧࡦࠬ෗"))
          bstack11ll1ll11l_opy_[bstack1l11l11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬෘ")] = bstack11ll1ll11l_opy_[bstack1l11l11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ෙ")][0]
          with open(bstack11ll1ll11l_opy_[bstack1l11l11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧේ")], bstack1l11l11_opy_ (u"ࠬࡸࠧෛ")) as f:
            bstack111l1l1ll_opy_ = f.read()
          bstack11lll111l_opy_ = bstack1l11l11_opy_ (u"ࠨࠢࠣࡨࡵࡳࡲࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡹࡤ࡬ࠢ࡬ࡱࡵࡵࡲࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩࡀࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦࠪࡾࢁ࠮ࡁࠠࡧࡴࡲࡱࠥࡶࡤࡣࠢ࡬ࡱࡵࡵࡲࡵࠢࡓࡨࡧࡁࠠࡰࡩࡢࡨࡧࠦ࠽ࠡࡒࡧࡦ࠳ࡪ࡯ࡠࡤࡵࡩࡦࡱ࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡩ࡫ࡦࠡ࡯ࡲࡨࡤࡨࡲࡦࡣ࡮ࠬࡸ࡫࡬ࡧ࠮ࠣࡥࡷ࡭ࠬࠡࡶࡨࡱࡵࡵࡲࡢࡴࡼࠤࡂࠦ࠰ࠪ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡶࡵࡽ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡡࡳࡩࠣࡁࠥࡹࡴࡳࠪ࡬ࡲࡹ࠮ࡡࡳࡩࠬ࠯࠶࠶ࠩࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡥࡹࡥࡨࡴࡹࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡤࡷࠥ࡫࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡲࡤࡷࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡴ࡭࡟ࡥࡤࠫࡷࡪࡲࡦ࠭ࡣࡵ࡫࠱ࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠪࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࠠ࠾ࠢࡰࡳࡩࡥࡢࡳࡧࡤ࡯ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡒࡧࡦ࠳ࡪ࡯ࡠࡤࡵࡩࡦࡱࠠ࠾ࠢࡰࡳࡩࡥࡢࡳࡧࡤ࡯ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡒࡧࡦ࠭࠯࠮ࡴࡧࡷࡣࡹࡸࡡࡤࡧࠫ࠭ࡡࡴࠢࠣࠤො").format(str(bstack11ll1ll11l_opy_))
          bstack1l1l1ll1l_opy_ = bstack11lll111l_opy_ + bstack111l1l1ll_opy_
          bstack1l1ll1111l_opy_ = bstack11ll1ll11l_opy_[bstack1l11l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪෝ")] + bstack1l11l11_opy_ (u"ࠨࡡࡥࡷࡹࡧࡣ࡬ࡡࡷࡩࡲࡶ࠮ࡱࡻࠪෞ")
          with open(bstack1l1ll1111l_opy_, bstack1l11l11_opy_ (u"ࠩࡺࠫෟ")):
            pass
          with open(bstack1l1ll1111l_opy_, bstack1l11l11_opy_ (u"ࠥࡻ࠰ࠨ෠")) as f:
            f.write(bstack1l1l1ll1l_opy_)
          import subprocess
          bstack1l1111l1ll_opy_ = subprocess.run([bstack1l11l11_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࠦ෡"), bstack1l1ll1111l_opy_])
          if os.path.exists(bstack1l1ll1111l_opy_):
            os.unlink(bstack1l1ll1111l_opy_)
          os._exit(bstack1l1111l1ll_opy_.returncode)
        else:
          if bstack1l11111l11_opy_(bstack11ll1ll11l_opy_[bstack1l11l11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ෢")]):
            bstack11ll1ll11l_opy_[bstack1l11l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ෣")].remove(bstack1l11l11_opy_ (u"ࠧ࠮࡯ࠪ෤"))
            bstack11ll1ll11l_opy_[bstack1l11l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ෥")].remove(bstack1l11l11_opy_ (u"ࠩࡳࡨࡧ࠭෦"))
            bstack11ll1ll11l_opy_[bstack1l11l11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭෧")] = bstack11ll1ll11l_opy_[bstack1l11l11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ෨")][0]
          bstack1ll111ll1l_opy_(bstack1l1l1111ll_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack11ll1ll11l_opy_[bstack1l11l11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ෩")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1l11l11_opy_ (u"࠭࡟ࡠࡰࡤࡱࡪࡥ࡟ࠨ෪")] = bstack1l11l11_opy_ (u"ࠧࡠࡡࡰࡥ࡮ࡴ࡟ࡠࠩ෫")
          mod_globals[bstack1l11l11_opy_ (u"ࠨࡡࡢࡪ࡮ࡲࡥࡠࡡࠪ෬")] = os.path.abspath(bstack11ll1ll11l_opy_[bstack1l11l11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ෭")])
          exec(open(bstack11ll1ll11l_opy_[bstack1l11l11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭෮")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1l11l11_opy_ (u"ࠫࡈࡧࡵࡨࡪࡷࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠫ෯").format(str(e)))
          for driver in bstack111lll1l1_opy_:
            bstack11ll11lll_opy_.append({
              bstack1l11l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ෰"): bstack11ll1ll11l_opy_[bstack1l11l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ෱")],
              bstack1l11l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ෲ"): str(e),
              bstack1l11l11_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧෳ"): multiprocessing.current_process().name
            })
            bstack1l1l11l1ll_opy_(driver, bstack1l11l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ෴"), bstack1l11l11_opy_ (u"ࠥࡗࡪࡹࡳࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨ෵") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack111lll1l1_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1ll111111_opy_, CONFIG, logger)
      bstack111l1111l_opy_()
      bstack1ll1l1ll1l_opy_()
      percy.bstack1l1l111l11_opy_()
      bstack11ll1l1l_opy_ = {
        bstack1l11l11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ෶"): args[0],
        bstack1l11l11_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬ෷"): CONFIG,
        bstack1l11l11_opy_ (u"࠭ࡈࡖࡄࡢ࡙ࡗࡒࠧ෸"): bstack11l1ll111_opy_,
        bstack1l11l11_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ෹"): bstack1ll111111_opy_
      }
      if bstack1l11l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ෺") in CONFIG:
        bstack1lll11ll1l_opy_ = bstack1llll11l1_opy_(args, logger, CONFIG, bstack1l1l11lll_opy_, bstack1ll1l111l1_opy_)
        bstack1l11111l_opy_ = bstack1lll11ll1l_opy_.bstack11l1l1llll_opy_(run_on_browserstack, bstack11ll1l1l_opy_, bstack1l11111l11_opy_(args))
      else:
        if bstack1l11111l11_opy_(args):
          bstack11ll1l1l_opy_[bstack1l11l11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ෻")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack11ll1l1l_opy_,))
          test.start()
          test.join()
        else:
          bstack1ll111ll1l_opy_(bstack1l1l1111ll_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1l11l11_opy_ (u"ࠪࡣࡤࡴࡡ࡮ࡧࡢࡣࠬ෼")] = bstack1l11l11_opy_ (u"ࠫࡤࡥ࡭ࡢ࡫ࡱࡣࡤ࠭෽")
          mod_globals[bstack1l11l11_opy_ (u"ࠬࡥ࡟ࡧ࡫࡯ࡩࡤࡥࠧ෾")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack11ll1111l1_opy_ == bstack1l11l11_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ෿") or bstack11ll1111l1_opy_ == bstack1l11l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭฀"):
    percy.init(bstack1ll111111_opy_, CONFIG, logger)
    percy.bstack1l1l111l11_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1ll11111ll_opy_(e, bstack111l1lll_opy_)
    bstack111l1111l_opy_()
    bstack1ll111ll1l_opy_(bstack1l11ll1l_opy_)
    if bstack1l1l11lll_opy_:
      bstack1llll11l11_opy_(bstack1l11ll1l_opy_, args)
      if bstack1l11l11_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ก") in args:
        i = args.index(bstack1l11l11_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧข"))
        args.pop(i)
        args.pop(i)
      if bstack1l11l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ฃ") not in CONFIG:
        CONFIG[bstack1l11l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧค")] = [{}]
        bstack1ll1l111l1_opy_ = 1
      if bstack11llll1ll1_opy_ == 0:
        bstack11llll1ll1_opy_ = 1
      args.insert(0, str(bstack11llll1ll1_opy_))
      args.insert(0, str(bstack1l11l11_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪฅ")))
    if bstack11ll111ll1_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack111ll11ll_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack111ll1ll1_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack1l11l11_opy_ (u"ࠨࡒࡐࡄࡒࡘࡤࡕࡐࡕࡋࡒࡒࡘࠨฆ"),
        ).parse_args(bstack111ll11ll_opy_)
        bstack11lllll1l1_opy_ = args.index(bstack111ll11ll_opy_[0]) if len(bstack111ll11ll_opy_) > 0 else len(args)
        args.insert(bstack11lllll1l1_opy_, str(bstack1l11l11_opy_ (u"ࠧ࠮࠯࡯࡭ࡸࡺࡥ࡯ࡧࡵࠫง")))
        args.insert(bstack11lllll1l1_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l11l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡴࡲࡦࡴࡺ࡟࡭࡫ࡶࡸࡪࡴࡥࡳ࠰ࡳࡽࠬจ"))))
        if bstack11l11l1lll_opy_.bstack1l11ll1l1l_opy_(CONFIG):
          args.insert(bstack11lllll1l1_opy_, str(bstack1l11l11_opy_ (u"ࠩ࠰࠱ࡱ࡯ࡳࡵࡧࡱࡩࡷ࠭ฉ")))
          args.insert(bstack11lllll1l1_opy_ + 1, str(bstack1l11l11_opy_ (u"ࠪࡖࡪࡺࡲࡺࡈࡤ࡭ࡱ࡫ࡤ࠻ࡽࢀࠫช").format(bstack11l11l1lll_opy_.bstack1l1lll11l1_opy_(CONFIG))))
        if bstack11lll11ll1_opy_(os.environ.get(bstack1l11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠩซ"))) and str(os.environ.get(bstack1l11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠩฌ"), bstack1l11l11_opy_ (u"࠭࡮ࡶ࡮࡯ࠫญ"))) != bstack1l11l11_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬฎ"):
          for bstack11l11111ll_opy_ in bstack111ll1ll1_opy_:
            args.remove(bstack11l11111ll_opy_)
          test_files = os.environ.get(bstack1l11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࡥࡔࡆࡕࡗࡗࠬฏ")).split(bstack1l11l11_opy_ (u"ࠩ࠯ࠫฐ"))
          for bstack1ll111l11_opy_ in test_files:
            args.append(bstack1ll111l11_opy_)
      except Exception as e:
        logger.error(bstack1l11l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡣࡷࡸࡦࡩࡨࡪࡰࡪࠤࡱ࡯ࡳࡵࡧࡱࡩࡷࠦࡦࡰࡴࠣࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࠤࡊࡸࡲࡰࡴࠣ࠱ࠥࠨฑ").format(e))
    pabot.main(args)
  elif bstack11ll1111l1_opy_ == bstack1l11l11_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬฒ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1ll11111ll_opy_(e, bstack111l1lll_opy_)
    for a in args:
      if bstack1l11l11_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡕࡒࡁࡕࡈࡒࡖࡒࡏࡎࡅࡇ࡛ࠫณ") in a:
        bstack1l1llll1ll_opy_ = int(a.split(bstack1l11l11_opy_ (u"࠭࠺ࠨด"))[1])
      if bstack1l11l11_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡄࡆࡈࡏࡓࡈࡇࡌࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫต") in a:
        bstack11ll111l1l_opy_ = str(a.split(bstack1l11l11_opy_ (u"ࠨ࠼ࠪถ"))[1])
      if bstack1l11l11_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡅࡏࡍࡆࡘࡇࡔࠩท") in a:
        bstack1lll1ll11l_opy_ = str(a.split(bstack1l11l11_opy_ (u"ࠪ࠾ࠬธ"))[1])
    bstack11lllll1ll_opy_ = None
    if bstack1l11l11_opy_ (u"ࠫ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠪน") in args:
      i = args.index(bstack1l11l11_opy_ (u"ࠬ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠫบ"))
      args.pop(i)
      bstack11lllll1ll_opy_ = args.pop(i)
    if bstack11lllll1ll_opy_ is not None:
      global bstack1l1l11l11_opy_
      bstack1l1l11l11_opy_ = bstack11lllll1ll_opy_
    bstack1ll111ll1l_opy_(bstack1l11ll1l_opy_)
    run_cli(args)
    if bstack1l11l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶࠪป") in multiprocessing.current_process().__dict__.keys():
      for bstack1ll11l11l1_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack11ll11lll_opy_.append(bstack1ll11l11l1_opy_)
  elif bstack11ll1111l1_opy_ == bstack1l11l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧผ"):
    bstack1l11l11l11_opy_ = bstack1l111l11l1_opy_(args, logger, CONFIG, bstack1l1l11lll_opy_)
    bstack1l11l11l11_opy_.bstack1ll1lllll1_opy_()
    bstack111l1111l_opy_()
    bstack1l11111lll_opy_ = True
    bstack11l111lll_opy_ = bstack1l11l11l11_opy_.bstack11l11ll11_opy_()
    bstack1l11l11l11_opy_.bstack11l1ll1l11_opy_()
    bstack1l11l11l11_opy_.bstack11ll1l1l_opy_(bstack1l1llllll1_opy_)
    bstack1lll1ll1l1_opy_(bstack11ll1111l1_opy_, CONFIG, bstack1l11l11l11_opy_.bstack1l1l1l1l_opy_())
    bstack1llllllll_opy_ = bstack1l11l11l11_opy_.bstack11l1l1llll_opy_(bstack1l11llll_opy_, {
      bstack1l11l11_opy_ (u"ࠨࡊࡘࡆࡤ࡛ࡒࡍࠩฝ"): bstack11l1ll111_opy_,
      bstack1l11l11_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫพ"): bstack1ll111111_opy_,
      bstack1l11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭ฟ"): bstack1l1l11lll_opy_
    })
    try:
      bstack1l11lll11l_opy_, bstack1ll1l1ll11_opy_ = map(list, zip(*bstack1llllllll_opy_))
      bstack1l111l1ll_opy_ = bstack1l11lll11l_opy_[0]
      for status_code in bstack1ll1l1ll11_opy_:
        if status_code != 0:
          bstack11l1llll1l_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack1l11l11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡣࡹࡩࠥ࡫ࡲࡳࡱࡵࡷࠥࡧ࡮ࡥࠢࡶࡸࡦࡺࡵࡴࠢࡦࡳࡩ࡫࠮ࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࠿ࠦࡻࡾࠤภ").format(str(e)))
  elif bstack11ll1111l1_opy_ == bstack1l11l11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬม"):
    try:
      from behave.__main__ import main as bstack11lll1llll_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1ll11111ll_opy_(e, bstack1l11ll1l11_opy_)
    bstack111l1111l_opy_()
    bstack1l11111lll_opy_ = True
    bstack11l111ll_opy_ = 1
    if bstack1l11l11_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ย") in CONFIG:
      bstack11l111ll_opy_ = CONFIG[bstack1l11l11_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧร")]
    if bstack1l11l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫฤ") in CONFIG:
      bstack11l111ll1l_opy_ = int(bstack11l111ll_opy_) * int(len(CONFIG[bstack1l11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬล")]))
    else:
      bstack11l111ll1l_opy_ = int(bstack11l111ll_opy_)
    config = Configuration(args)
    bstack1l1lll1ll1_opy_ = config.paths
    if len(bstack1l1lll1ll1_opy_) == 0:
      import glob
      pattern = bstack1l11l11_opy_ (u"ࠪ࠮࠯࠵ࠪ࠯ࡨࡨࡥࡹࡻࡲࡦࠩฦ")
      bstack1l111ll11l_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1l111ll11l_opy_)
      config = Configuration(args)
      bstack1l1lll1ll1_opy_ = config.paths
    bstack1ll11lll1l_opy_ = [os.path.normpath(item) for item in bstack1l1lll1ll1_opy_]
    bstack1l1lll11_opy_ = [os.path.normpath(item) for item in args]
    bstack11l1lllll_opy_ = [item for item in bstack1l1lll11_opy_ if item not in bstack1ll11lll1l_opy_]
    import platform as pf
    if pf.system().lower() == bstack1l11l11_opy_ (u"ࠫࡼ࡯࡮ࡥࡱࡺࡷࠬว"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1ll11lll1l_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l1lll111_opy_)))
                    for bstack1l1lll111_opy_ in bstack1ll11lll1l_opy_]
    bstack1lll111l_opy_ = []
    for spec in bstack1ll11lll1l_opy_:
      bstack11l1l1l111_opy_ = []
      bstack11l1l1l111_opy_ += bstack11l1lllll_opy_
      bstack11l1l1l111_opy_.append(spec)
      bstack1lll111l_opy_.append(bstack11l1l1l111_opy_)
    execution_items = []
    for bstack11l1l1l111_opy_ in bstack1lll111l_opy_:
      if bstack1l11l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨศ") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack1l11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩษ")]):
          item = {}
          item[bstack1l11l11_opy_ (u"ࠧࡢࡴࡪࠫส")] = bstack1l11l11_opy_ (u"ࠨࠢࠪห").join(bstack11l1l1l111_opy_)
          item[bstack1l11l11_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨฬ")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack1l11l11_opy_ (u"ࠪࡥࡷ࡭ࠧอ")] = bstack1l11l11_opy_ (u"ࠫࠥ࠭ฮ").join(bstack11l1l1l111_opy_)
        item[bstack1l11l11_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫฯ")] = 0
        execution_items.append(item)
    bstack1111l1ll_opy_ = bstack1ll1l11ll1_opy_(execution_items, bstack11l111ll1l_opy_)
    for execution_item in bstack1111l1ll_opy_:
      bstack1l1l1lll_opy_ = []
      for item in execution_item:
        bstack1l1l1lll_opy_.append(bstack111lllll1_opy_(name=str(item[bstack1l11l11_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬะ")]),
                                             target=bstack1lll1llll1_opy_,
                                             args=(item[bstack1l11l11_opy_ (u"ࠧࡢࡴࡪࠫั")],)))
      for t in bstack1l1l1lll_opy_:
        t.start()
      for t in bstack1l1l1lll_opy_:
        t.join()
  else:
    bstack11l11l1l11_opy_(bstack1llll1lll1_opy_)
  if not bstack11ll1ll11l_opy_:
    bstack11111l111_opy_()
    if(bstack11ll1111l1_opy_ in [bstack1l11l11_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨา"), bstack1l11l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩำ")]):
      bstack1l1111111l_opy_()
  bstack1l1ll11lll_opy_.bstack1lllllll11_opy_()
def browserstack_initialize(bstack1l111111_opy_=None):
  logger.info(bstack1l11l11_opy_ (u"ࠪࡖࡺࡴ࡮ࡪࡰࡪࠤࡘࡊࡋࠡࡹ࡬ࡸ࡭ࠦࡡࡳࡩࡶ࠾ࠥ࠭ิ") + str(bstack1l111111_opy_))
  run_on_browserstack(bstack1l111111_opy_, None, True)
@measure(event_name=EVENTS.bstack1ll1l111l_opy_, stage=STAGE.bstack1lll11l1_opy_, bstack1l1lll11l_opy_=bstack1lllll1ll_opy_)
def bstack11111l111_opy_():
  global CONFIG
  global bstack11llll111_opy_
  global bstack11l1llll1l_opy_
  global bstack11llllllll_opy_
  global bstack11l11llll_opy_
  bstack1l1l1llll_opy_.bstack1ll1l1ll1_opy_()
  if cli.is_running():
    bstack1llll1lll_opy_.invoke(bstack11ll11l1l_opy_.bstack1lll1l1l1_opy_)
  else:
    bstack1111111l_opy_ = bstack11l11l1lll_opy_.bstack11l111llll_opy_(config=CONFIG)
    bstack1111111l_opy_.bstack11lll11l11_opy_(CONFIG)
  if bstack11llll111_opy_ == bstack1l11l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫี"):
    if not cli.is_enabled(CONFIG):
      bstack11ll111ll1_opy_.stop()
  else:
    bstack11ll111ll1_opy_.stop()
  if not cli.is_enabled(CONFIG):
    bstack1l1lllll1l_opy_.bstack1l11l1ll_opy_()
  if bstack1l11l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩึ") in CONFIG and str(CONFIG[bstack1l11l11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪื")]).lower() != bstack1l11l11_opy_ (u"ࠧࡧࡣ࡯ࡷࡪุ࠭"):
    hashed_id, bstack111111ll1_opy_ = bstack111ll1l11_opy_()
  else:
    hashed_id, bstack111111ll1_opy_ = get_build_link()
  bstack1l11ll1ll1_opy_(hashed_id)
  logger.info(bstack1l11l11_opy_ (u"ࠨࡕࡇࡏࠥࡸࡵ࡯ࠢࡨࡲࡩ࡫ࡤࠡࡨࡲࡶࠥ࡯ࡤ࠻ูࠩ") + bstack11l11llll_opy_.get_property(bstack1l11l11_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧฺࠫ"), bstack1l11l11_opy_ (u"ࠪࠫ฻")) + bstack1l11l11_opy_ (u"ࠫ࠱ࠦࡴࡦࡵࡷ࡬ࡺࡨࠠࡪࡦ࠽ࠤࠬ฼") + os.getenv(bstack1l11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ฽"), bstack1l11l11_opy_ (u"࠭ࠧ฾")))
  if hashed_id is not None and bstack11llll111l_opy_() != -1:
    sessions = bstack11l111ll1_opy_(hashed_id)
    bstack1l1ll11l1l_opy_(sessions, bstack111111ll1_opy_)
  if bstack11llll111_opy_ == bstack1l11l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ฿") and bstack11l1llll1l_opy_ != 0:
    sys.exit(bstack11l1llll1l_opy_)
  if bstack11llll111_opy_ == bstack1l11l11_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨเ") and bstack11llllllll_opy_ != 0:
    sys.exit(bstack11llllllll_opy_)
def bstack1l11ll1ll1_opy_(new_id):
    global bstack11lll1ll11_opy_
    bstack11lll1ll11_opy_ = new_id
def bstack11l1lll11l_opy_(bstack11l11l111_opy_):
  if bstack11l11l111_opy_:
    return bstack11l11l111_opy_.capitalize()
  else:
    return bstack1l11l11_opy_ (u"ࠩࠪแ")
@measure(event_name=EVENTS.bstack1llll1l1ll_opy_, stage=STAGE.bstack1lll11l1_opy_, bstack1l1lll11l_opy_=bstack1lllll1ll_opy_)
def bstack11ll1l1111_opy_(bstack1l1l1llll1_opy_):
  if bstack1l11l11_opy_ (u"ࠪࡲࡦࡳࡥࠨโ") in bstack1l1l1llll1_opy_ and bstack1l1l1llll1_opy_[bstack1l11l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩใ")] != bstack1l11l11_opy_ (u"ࠬ࠭ไ"):
    return bstack1l1l1llll1_opy_[bstack1l11l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫๅ")]
  else:
    bstack1l1lll11l_opy_ = bstack1l11l11_opy_ (u"ࠢࠣๆ")
    if bstack1l11l11_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨ็") in bstack1l1l1llll1_opy_ and bstack1l1l1llll1_opy_[bstack1l11l11_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦ่ࠩ")] != None:
      bstack1l1lll11l_opy_ += bstack1l1l1llll1_opy_[bstack1l11l11_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧ้ࠪ")] + bstack1l11l11_opy_ (u"ࠦ࠱๊ࠦࠢ")
      if bstack1l1l1llll1_opy_[bstack1l11l11_opy_ (u"ࠬࡵࡳࠨ๋")] == bstack1l11l11_opy_ (u"ࠨࡩࡰࡵࠥ์"):
        bstack1l1lll11l_opy_ += bstack1l11l11_opy_ (u"ࠢࡪࡑࡖࠤࠧํ")
      bstack1l1lll11l_opy_ += (bstack1l1l1llll1_opy_[bstack1l11l11_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ๎")] or bstack1l11l11_opy_ (u"ࠩࠪ๏"))
      return bstack1l1lll11l_opy_
    else:
      bstack1l1lll11l_opy_ += bstack11l1lll11l_opy_(bstack1l1l1llll1_opy_[bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫ๐")]) + bstack1l11l11_opy_ (u"ࠦࠥࠨ๑") + (
              bstack1l1l1llll1_opy_[bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ๒")] or bstack1l11l11_opy_ (u"࠭ࠧ๓")) + bstack1l11l11_opy_ (u"ࠢ࠭ࠢࠥ๔")
      if bstack1l1l1llll1_opy_[bstack1l11l11_opy_ (u"ࠨࡱࡶࠫ๕")] == bstack1l11l11_opy_ (u"ࠤ࡚࡭ࡳࡪ࡯ࡸࡵࠥ๖"):
        bstack1l1lll11l_opy_ += bstack1l11l11_opy_ (u"࡛ࠥ࡮ࡴࠠࠣ๗")
      bstack1l1lll11l_opy_ += bstack1l1l1llll1_opy_[bstack1l11l11_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ๘")] or bstack1l11l11_opy_ (u"ࠬ࠭๙")
      return bstack1l1lll11l_opy_
@measure(event_name=EVENTS.bstack1l1lll111l_opy_, stage=STAGE.bstack1lll11l1_opy_, bstack1l1lll11l_opy_=bstack1lllll1ll_opy_)
def bstack1l1l11l1_opy_(bstack1lll1l1l1l_opy_):
  if bstack1lll1l1l1l_opy_ == bstack1l11l11_opy_ (u"ࠨࡤࡰࡰࡨࠦ๚"):
    return bstack1l11l11_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡪࡶࡪ࡫࡮࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡪࡶࡪ࡫࡮ࠣࡀࡆࡳࡲࡶ࡬ࡦࡶࡨࡨࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪ๛")
  elif bstack1lll1l1l1l_opy_ == bstack1l11l11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ๜"):
    return bstack1l11l11_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡷ࡫ࡤ࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡵࡩࡩࠨ࠾ࡇࡣ࡬ࡰࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ๝")
  elif bstack1lll1l1l1l_opy_ == bstack1l11l11_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ๞"):
    return bstack1l11l11_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡧࡳࡧࡨࡲࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡧࡳࡧࡨࡲࠧࡄࡐࡢࡵࡶࡩࡩࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫ๟")
  elif bstack1lll1l1l1l_opy_ == bstack1l11l11_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦ๠"):
    return bstack1l11l11_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡴࡨࡨࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡲࡦࡦࠥࡂࡊࡸࡲࡰࡴ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨ๡")
  elif bstack1lll1l1l1l_opy_ == bstack1l11l11_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࠣ๢"):
    return bstack1l11l11_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࠧࡪ࡫ࡡ࠴࠴࠹࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࠩࡥࡦࡣ࠶࠶࠻ࠨ࠾ࡕ࡫ࡰࡩࡴࡻࡴ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭๣")
  elif bstack1lll1l1l1l_opy_ == bstack1l11l11_opy_ (u"ࠤࡵࡹࡳࡴࡩ࡯ࡩࠥ๤"):
    return bstack1l11l11_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡨ࡬ࡢࡥ࡮࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡨ࡬ࡢࡥ࡮ࠦࡃࡘࡵ࡯ࡰ࡬ࡲ࡬ࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫ๥")
  else:
    return bstack1l11l11_opy_ (u"ࠫࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡣ࡮ࡤࡧࡰࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡣ࡮ࡤࡧࡰࠨ࠾ࠨ๦") + bstack11l1lll11l_opy_(
      bstack1lll1l1l1l_opy_) + bstack1l11l11_opy_ (u"ࠬࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫ๧")
def bstack11111ll1l_opy_(session):
  return bstack1l11l11_opy_ (u"࠭࠼ࡵࡴࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡶࡴࡽࠢ࠿࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠣࡷࡪࡹࡳࡪࡱࡱ࠱ࡳࡧ࡭ࡦࠤࡁࡀࡦࠦࡨࡳࡧࡩࡁࠧࢁࡽࠣࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥࡣࡧࡲࡡ࡯࡭ࠥࡂࢀࢃ࠼࠰ࡣࡁࡀ࠴ࡺࡤ࠿ࡽࢀࡿࢂࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽࠱ࡷࡶࡃ࠭๨").format(
    session[bstack1l11l11_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࡟ࡶࡴ࡯ࠫ๩")], bstack11ll1l1111_opy_(session), bstack1l1l11l1_opy_(session[bstack1l11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡴࡶࡤࡸࡺࡹࠧ๪")]),
    bstack1l1l11l1_opy_(session[bstack1l11l11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ๫")]),
    bstack11l1lll11l_opy_(session[bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫ๬")] or session[bstack1l11l11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫ๭")] or bstack1l11l11_opy_ (u"ࠬ࠭๮")) + bstack1l11l11_opy_ (u"ࠨࠠࠣ๯") + (session[bstack1l11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ๰")] or bstack1l11l11_opy_ (u"ࠨࠩ๱")),
    session[bstack1l11l11_opy_ (u"ࠩࡲࡷࠬ๲")] + bstack1l11l11_opy_ (u"ࠥࠤࠧ๳") + session[bstack1l11l11_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ๴")], session[bstack1l11l11_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧ๵")] or bstack1l11l11_opy_ (u"࠭ࠧ๶"),
    session[bstack1l11l11_opy_ (u"ࠧࡤࡴࡨࡥࡹ࡫ࡤࡠࡣࡷࠫ๷")] if session[bstack1l11l11_opy_ (u"ࠨࡥࡵࡩࡦࡺࡥࡥࡡࡤࡸࠬ๸")] else bstack1l11l11_opy_ (u"ࠩࠪ๹"))
@measure(event_name=EVENTS.bstack1l11l1l1_opy_, stage=STAGE.bstack1lll11l1_opy_, bstack1l1lll11l_opy_=bstack1lllll1ll_opy_)
def bstack1l1ll11l1l_opy_(sessions, bstack111111ll1_opy_):
  try:
    bstack111l111ll_opy_ = bstack1l11l11_opy_ (u"ࠥࠦ๺")
    if not os.path.exists(bstack1ll1ll1111_opy_):
      os.mkdir(bstack1ll1ll1111_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l11l11_opy_ (u"ࠫࡦࡹࡳࡦࡶࡶ࠳ࡷ࡫ࡰࡰࡴࡷ࠲࡭ࡺ࡭࡭ࠩ๻")), bstack1l11l11_opy_ (u"ࠬࡸࠧ๼")) as f:
      bstack111l111ll_opy_ = f.read()
    bstack111l111ll_opy_ = bstack111l111ll_opy_.replace(bstack1l11l11_opy_ (u"࠭ࡻࠦࡔࡈࡗ࡚ࡒࡔࡔࡡࡆࡓ࡚ࡔࡔࠦࡿࠪ๽"), str(len(sessions)))
    bstack111l111ll_opy_ = bstack111l111ll_opy_.replace(bstack1l11l11_opy_ (u"ࠧࡼࠧࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠪࢃࠧ๾"), bstack111111ll1_opy_)
    bstack111l111ll_opy_ = bstack111l111ll_opy_.replace(bstack1l11l11_opy_ (u"ࠨࡽࠨࡆ࡚ࡏࡌࡅࡡࡑࡅࡒࡋࠥࡾࠩ๿"),
                                              sessions[0].get(bstack1l11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡰࡤࡱࡪ࠭຀")) if sessions[0] else bstack1l11l11_opy_ (u"ࠪࠫກ"))
    with open(os.path.join(bstack1ll1ll1111_opy_, bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡶࡪࡶ࡯ࡳࡶ࠱࡬ࡹࡳ࡬ࠨຂ")), bstack1l11l11_opy_ (u"ࠬࡽࠧ຃")) as stream:
      stream.write(bstack111l111ll_opy_.split(bstack1l11l11_opy_ (u"࠭ࡻࠦࡕࡈࡗࡘࡏࡏࡏࡕࡢࡈࡆ࡚ࡁࠦࡿࠪຄ"))[0])
      for session in sessions:
        stream.write(bstack11111ll1l_opy_(session))
      stream.write(bstack111l111ll_opy_.split(bstack1l11l11_opy_ (u"ࠧࡼࠧࡖࡉࡘ࡙ࡉࡐࡐࡖࡣࡉࡇࡔࡂࠧࢀࠫ຅"))[1])
    logger.info(bstack1l11l11_opy_ (u"ࠨࡉࡨࡲࡪࡸࡡࡵࡧࡧࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡦࡺ࡯࡬ࡥࠢࡤࡶࡹ࡯ࡦࡢࡥࡷࡷࠥࡧࡴࠡࡽࢀࠫຆ").format(bstack1ll1ll1111_opy_));
  except Exception as e:
    logger.debug(bstack111l1ll1l_opy_.format(str(e)))
def bstack11l111ll1_opy_(hashed_id):
  global CONFIG
  try:
    bstack1l11l11111_opy_ = datetime.datetime.now()
    host = bstack1l11l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡵ࡯࠭ࡤ࡮ࡲࡹࡩ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩງ") if bstack1l11l11_opy_ (u"ࠪࡥࡵࡶࠧຈ") in CONFIG else bstack1l11l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬຉ")
    user = CONFIG[bstack1l11l11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧຊ")]
    key = CONFIG[bstack1l11l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ຋")]
    bstack1l1l1l1ll1_opy_ = bstack1l11l11_opy_ (u"ࠧࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ຌ") if bstack1l11l11_opy_ (u"ࠨࡣࡳࡴࠬຍ") in CONFIG else (bstack1l11l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭ຎ") if CONFIG.get(bstack1l11l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧຏ")) else bstack1l11l11_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ຐ"))
    host = bstack11l111l11_opy_(cli.config, [bstack1l11l11_opy_ (u"ࠧࡧࡰࡪࡵࠥຑ"), bstack1l11l11_opy_ (u"ࠨࡡࡱࡲࡄࡹࡹࡵ࡭ࡢࡶࡨࠦຒ"), bstack1l11l11_opy_ (u"ࠢࡢࡲ࡬ࠦຓ")], host) if bstack1l11l11_opy_ (u"ࠨࡣࡳࡴࠬດ") in CONFIG else bstack11l111l11_opy_(cli.config, [bstack1l11l11_opy_ (u"ࠤࡤࡴ࡮ࡹࠢຕ"), bstack1l11l11_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷࡩࠧຖ"), bstack1l11l11_opy_ (u"ࠦࡦࡶࡩࠣທ")], host)
    url = bstack1l11l11_opy_ (u"ࠬࢁࡽ࠰ࡽࢀ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃ࠯ࡴࡧࡶࡷ࡮ࡵ࡮ࡴ࠰࡭ࡷࡴࡴࠧຘ").format(host, bstack1l1l1l1ll1_opy_, hashed_id)
    headers = {
      bstack1l11l11_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡵࡻࡳࡩࠬນ"): bstack1l11l11_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪບ"),
    }
    proxies = bstack1lll1lll1_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies, auth=(user, key))
    if response.json():
      cli.bstack1l1l1l1l1l_opy_(bstack1l11l11_opy_ (u"ࠣࡪࡷࡸࡵࡀࡧࡦࡶࡢࡷࡪࡹࡳࡪࡱࡱࡷࡤࡲࡩࡴࡶࠥປ"), datetime.datetime.now() - bstack1l11l11111_opy_)
      return list(map(lambda session: session[bstack1l11l11_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠧຜ")], response.json()))
  except Exception as e:
    logger.debug(bstack1l11l1l111_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack1ll111l1ll_opy_, stage=STAGE.bstack1lll11l1_opy_, bstack1l1lll11l_opy_=bstack1lllll1ll_opy_)
def get_build_link():
  global CONFIG
  global bstack11lll1ll11_opy_
  try:
    if bstack1l11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ຝ") in CONFIG:
      bstack1l11l11111_opy_ = datetime.datetime.now()
      host = bstack1l11l11_opy_ (u"ࠫࡦࡶࡩ࠮ࡥ࡯ࡳࡺࡪࠧພ") if bstack1l11l11_opy_ (u"ࠬࡧࡰࡱࠩຟ") in CONFIG else bstack1l11l11_opy_ (u"࠭ࡡࡱ࡫ࠪຠ")
      user = CONFIG[bstack1l11l11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩມ")]
      key = CONFIG[bstack1l11l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫຢ")]
      bstack1l1l1l1ll1_opy_ = bstack1l11l11_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨຣ") if bstack1l11l11_opy_ (u"ࠪࡥࡵࡶࠧ຤") in CONFIG else bstack1l11l11_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ລ")
      url = bstack1l11l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡻࡾ࠼ࡾࢁࡅࢁࡽ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࢀࢃ࠯ࡣࡷ࡬ࡰࡩࡹ࠮࡫ࡵࡲࡲࠬ຦").format(user, key, host, bstack1l1l1l1ll1_opy_)
      if cli.is_enabled(CONFIG):
        bstack111111ll1_opy_, hashed_id = cli.bstack1l111l1l1_opy_()
        logger.info(bstack11ll11111l_opy_.format(bstack111111ll1_opy_))
        return [hashed_id, bstack111111ll1_opy_]
      else:
        headers = {
          bstack1l11l11_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡵࡻࡳࡩࠬວ"): bstack1l11l11_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪຨ"),
        }
        if bstack1l11l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪຩ") in CONFIG:
          params = {bstack1l11l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧສ"): CONFIG[bstack1l11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ຫ")], bstack1l11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧຬ"): CONFIG[bstack1l11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧອ")]}
        else:
          params = {bstack1l11l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫຮ"): CONFIG[bstack1l11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪຯ")]}
        proxies = bstack1lll1lll1_opy_(CONFIG, url)
        response = requests.get(url, params=params, headers=headers, proxies=proxies)
        if response.json():
          bstack1l1l1111l_opy_ = response.json()[0][bstack1l11l11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡨࡵࡪ࡮ࡧࠫະ")]
          if bstack1l1l1111l_opy_:
            bstack111111ll1_opy_ = bstack1l1l1111l_opy_[bstack1l11l11_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤࡡࡸࡶࡱ࠭ັ")].split(bstack1l11l11_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥ࠰ࡦࡺ࡯࡬ࡥࠩາ"))[0] + bstack1l11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡶ࠳ࠬຳ") + bstack1l1l1111l_opy_[
              bstack1l11l11_opy_ (u"ࠬ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨິ")]
            logger.info(bstack11ll11111l_opy_.format(bstack111111ll1_opy_))
            bstack11lll1ll11_opy_ = bstack1l1l1111l_opy_[bstack1l11l11_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩີ")]
            bstack1l11ll1l1_opy_ = CONFIG[bstack1l11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪຶ")]
            if bstack1l11l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪື") in CONFIG:
              bstack1l11ll1l1_opy_ += bstack1l11l11_opy_ (u"ຸࠩࠣࠫ") + CONFIG[bstack1l11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶູࠬ")]
            if bstack1l11ll1l1_opy_ != bstack1l1l1111l_opy_[bstack1l11l11_opy_ (u"ࠫࡳࡧ࡭ࡦ຺ࠩ")]:
              logger.debug(bstack1l1l11l1l1_opy_.format(bstack1l1l1111l_opy_[bstack1l11l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪົ")], bstack1l11ll1l1_opy_))
            cli.bstack1l1l1l1l1l_opy_(bstack1l11l11_opy_ (u"ࠨࡨࡵࡶࡳ࠾࡬࡫ࡴࡠࡤࡸ࡭ࡱࡪ࡟࡭࡫ࡱ࡯ࠧຼ"), datetime.datetime.now() - bstack1l11l11111_opy_)
            return [bstack1l1l1111l_opy_[bstack1l11l11_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪຽ")], bstack111111ll1_opy_]
    else:
      logger.warn(bstack1ll111l111_opy_)
  except Exception as e:
    logger.debug(bstack11ll1lll1_opy_.format(str(e)))
  return [None, None]
def bstack11111llll_opy_(url, bstack111l11ll_opy_=False):
  global CONFIG
  global bstack11111lll1_opy_
  if not bstack11111lll1_opy_:
    hostname = bstack1ll11llll_opy_(url)
    is_private = bstack11lll111l1_opy_(hostname)
    if (bstack1l11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ຾") in CONFIG and not bstack11lll11ll1_opy_(CONFIG[bstack1l11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭຿")])) and (is_private or bstack111l11ll_opy_):
      bstack11111lll1_opy_ = hostname
def bstack1ll11llll_opy_(url):
  return urlparse(url).hostname
def bstack11lll111l1_opy_(hostname):
  for bstack111lll11l_opy_ in bstack11l11111_opy_:
    regex = re.compile(bstack111lll11l_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1l1111l111_opy_(bstack1ll1ll11l_opy_):
  return True if bstack1ll1ll11l_opy_ in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack11l1l1l11l_opy_, stage=STAGE.bstack1lll11l1_opy_, bstack1l1lll11l_opy_=bstack1lllll1ll_opy_)
def getAccessibilityResults(driver):
  global CONFIG
  global bstack1l1llll1ll_opy_
  bstack1l1l1ll1ll_opy_ = not (bstack1l111ll111_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧເ"), None) and bstack1l111ll111_opy_(
          threading.current_thread(), bstack1l11l11_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪແ"), None))
  bstack1l111llll1_opy_ = getattr(driver, bstack1l11l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬໂ"), None) != True
  bstack111l1l11l_opy_ = bstack1l111ll111_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ໃ"), None) and bstack1l111ll111_opy_(
          threading.current_thread(), bstack1l11l11_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩໄ"), None)
  if bstack111l1l11l_opy_:
    if not bstack11l1l11l11_opy_():
      logger.warning(bstack1l11l11_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡳࡴࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶ࠲ࠧ໅"))
      return {}
    logger.debug(bstack1l11l11_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸ࠭ໆ"))
    logger.debug(perform_scan(driver, driver_command=bstack1l11l11_opy_ (u"ࠪࡩࡽ࡫ࡣࡶࡶࡨࡗࡨࡸࡩࡱࡶࠪ໇")))
    results = bstack1lllll1ll1_opy_(bstack1l11l11_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷࡷ່ࠧ"))
    if results is not None and results.get(bstack1l11l11_opy_ (u"ࠧ࡯ࡳࡴࡷࡨࡷ້ࠧ")) is not None:
        return results[bstack1l11l11_opy_ (u"ࠨࡩࡴࡵࡸࡩࡸࠨ໊")]
    logger.error(bstack1l11l11_opy_ (u"ࠢࡏࡱࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡖࡪࡹࡵ࡭ࡶࡶࠤࡼ࡫ࡲࡦࠢࡩࡳࡺࡴࡤ࠯ࠤ໋"))
    return []
  if not bstack1ll1ll1l11_opy_.bstack11l1111l1_opy_(CONFIG, bstack1l1llll1ll_opy_) or (bstack1l111llll1_opy_ and bstack1l1l1ll1ll_opy_):
    logger.warning(bstack1l11l11_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵ࠱ࠦ໌"))
    return {}
  try:
    logger.debug(bstack1l11l11_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸ࠭ໍ"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack11l1ll111l_opy_.bstack1l1ll1l11_opy_)
    return results
  except Exception:
    logger.error(bstack1l11l11_opy_ (u"ࠥࡒࡴࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡸࡧࡵࡩࠥ࡬࡯ࡶࡰࡧ࠲ࠧ໎"))
    return {}
@measure(event_name=EVENTS.bstack1l1111ll_opy_, stage=STAGE.bstack1lll11l1_opy_, bstack1l1lll11l_opy_=bstack1lllll1ll_opy_)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack1l1llll1ll_opy_
  bstack1l1l1ll1ll_opy_ = not (bstack1l111ll111_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ໏"), None) and bstack1l111ll111_opy_(
          threading.current_thread(), bstack1l11l11_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ໐"), None))
  bstack1l111llll1_opy_ = getattr(driver, bstack1l11l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭໑"), None) != True
  bstack111l1l11l_opy_ = bstack1l111ll111_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ໒"), None) and bstack1l111ll111_opy_(
          threading.current_thread(), bstack1l11l11_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ໓"), None)
  if bstack111l1l11l_opy_:
    if not bstack11l1l11l11_opy_():
      logger.warning(bstack1l11l11_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡴࡵࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡂࡲࡳࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡹࡵ࡮࡯ࡤࡶࡾ࠴ࠢ໔"))
      return {}
    logger.debug(bstack1l11l11_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡲࡦࡵࡸࡰࡹࡹࠠࡴࡷࡰࡱࡦࡸࡹࠨ໕"))
    logger.debug(perform_scan(driver, driver_command=bstack1l11l11_opy_ (u"ࠫࡪࡾࡥࡤࡷࡷࡩࡘࡩࡲࡪࡲࡷࠫ໖")))
    results = bstack1lllll1ll1_opy_(bstack1l11l11_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸࡘࡻ࡭࡮ࡣࡵࡽࠧ໗"))
    if results is not None and results.get(bstack1l11l11_opy_ (u"ࠨࡳࡶ࡯ࡰࡥࡷࡿࠢ໘")) is not None:
        return results[bstack1l11l11_opy_ (u"ࠢࡴࡷࡰࡱࡦࡸࡹࠣ໙")]
    logger.error(bstack1l11l11_opy_ (u"ࠣࡐࡲࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡗ࡫ࡳࡶ࡮ࡷࡷ࡙ࠥࡵ࡮࡯ࡤࡶࡾࠦࡷࡢࡵࠣࡪࡴࡻ࡮ࡥ࠰ࠥ໚"))
    return {}
  if not bstack1ll1ll1l11_opy_.bstack11l1111l1_opy_(CONFIG, bstack1l1llll1ll_opy_) or (bstack1l111llll1_opy_ and bstack1l1l1ll1ll_opy_):
    logger.warning(bstack1l11l11_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡸࡻ࡭࡮ࡣࡵࡽ࠳ࠨ໛"))
    return {}
  try:
    logger.debug(bstack1l11l11_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡲࡦࡵࡸࡰࡹࡹࠠࡴࡷࡰࡱࡦࡸࡹࠨໜ"))
    logger.debug(perform_scan(driver))
    bstack11l1ll1ll_opy_ = driver.execute_async_script(bstack11l1ll111l_opy_.bstack11ll1ll111_opy_)
    return bstack11l1ll1ll_opy_
  except Exception:
    logger.error(bstack1l11l11_opy_ (u"ࠦࡓࡵࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡷࡰࡱࡦࡸࡹࠡࡹࡤࡷࠥ࡬࡯ࡶࡰࡧ࠲ࠧໝ"))
    return {}
def bstack11l1l11l11_opy_():
  global CONFIG
  global bstack1l1llll1ll_opy_
  bstack1l11l1l1l_opy_ = bstack1l111ll111_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"ࠬ࡯ࡳࡂࡲࡳࡅ࠶࠷ࡹࡕࡧࡶࡸࠬໞ"), None) and bstack1l111ll111_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨໟ"), None)
  if not bstack1ll1ll1l11_opy_.bstack11l1111l1_opy_(CONFIG, bstack1l1llll1ll_opy_) or not bstack1l11l1l1l_opy_:
        logger.warning(bstack1l11l11_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡲࡳࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡪࡺࡲࡪࡧࡹࡩࠥࡸࡥࡴࡷ࡯ࡸࡸ࠴ࠢ໠"))
        return False
  return True
def bstack1lllll1ll1_opy_(bstack11l11lll1_opy_):
    bstack11l1ll11l_opy_ = bstack11ll111ll1_opy_.current_test_uuid() if bstack11ll111ll1_opy_.current_test_uuid() else bstack1l1lllll1l_opy_.current_hook_uuid()
    with ThreadPoolExecutor() as executor:
        future = executor.submit(bstack1lll11l1ll_opy_(bstack11l1ll11l_opy_, bstack11l11lll1_opy_))
        try:
            return future.result(timeout=bstack11l1111l1l_opy_)
        except TimeoutError:
            logger.error(bstack1l11l11_opy_ (u"ࠣࡖ࡬ࡱࡪࡵࡵࡵࠢࡤࡪࡹ࡫ࡲࠡࡽࢀࡷࠥࡽࡨࡪ࡮ࡨࠤ࡫࡫ࡴࡤࡪ࡬ࡲ࡬ࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡒࡦࡵࡸࡰࡹࡹࠢ໡").format(bstack11l1111l1l_opy_))
        except Exception as ex:
            logger.debug(bstack1l11l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡴࡨࡸࡷ࡯ࡥࡷ࡫ࡱ࡫ࠥࡇࡰࡱࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡻࡾ࠰ࠣࡉࡷࡸ࡯ࡳࠢ࠰ࠤࢀࢃࠢ໢").format(bstack11l11lll1_opy_, str(ex)))
    return {}
@measure(event_name=EVENTS.bstack1l1l1ll111_opy_, stage=STAGE.bstack1lll11l1_opy_, bstack1l1lll11l_opy_=bstack1lllll1ll_opy_)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack1l1llll1ll_opy_
  bstack1l1l1ll1ll_opy_ = not (bstack1l111ll111_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ໣"), None) and bstack1l111ll111_opy_(
          threading.current_thread(), bstack1l11l11_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ໤"), None))
  bstack1l1l1ll1_opy_ = not (bstack1l111ll111_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"ࠬ࡯ࡳࡂࡲࡳࡅ࠶࠷ࡹࡕࡧࡶࡸࠬ໥"), None) and bstack1l111ll111_opy_(
          threading.current_thread(), bstack1l11l11_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ໦"), None))
  bstack1l111llll1_opy_ = getattr(driver, bstack1l11l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧ໧"), None) != True
  if not bstack1ll1ll1l11_opy_.bstack11l1111l1_opy_(CONFIG, bstack1l1llll1ll_opy_) or (bstack1l111llll1_opy_ and bstack1l1l1ll1ll_opy_ and bstack1l1l1ll1_opy_):
    logger.warning(bstack1l11l11_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡷࡱࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸࡩࡡ࡯࠰ࠥ໨"))
    return {}
  try:
    bstack1lllllll1_opy_ = bstack1l11l11_opy_ (u"ࠩࡤࡴࡵ࠭໩") in CONFIG and CONFIG.get(bstack1l11l11_opy_ (u"ࠪࡥࡵࡶࠧ໪"), bstack1l11l11_opy_ (u"ࠫࠬ໫"))
    session_id = getattr(driver, bstack1l11l11_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠩ໬"), None)
    if not session_id:
      logger.warning(bstack1l11l11_opy_ (u"ࠨࡎࡰࠢࡶࡩࡸࡹࡩࡰࡰࠣࡍࡉࠦࡦࡰࡷࡱࡨࠥ࡬࡯ࡳࠢࡧࡶ࡮ࡼࡥࡳࠤ໭"))
      return {bstack1l11l11_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨ໮"): bstack1l11l11_opy_ (u"ࠣࡐࡲࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡏࡄࠡࡨࡲࡹࡳࡪࠢ໯")}
    if bstack1lllllll1_opy_:
      try:
        bstack1l111l1111_opy_ = {
              bstack1l11l11_opy_ (u"ࠩࡷ࡬ࡏࡽࡴࡕࡱ࡮ࡩࡳ࠭໰"): os.environ.get(bstack1l11l11_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ໱"), os.environ.get(bstack1l11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ໲"), bstack1l11l11_opy_ (u"ࠬ࠭໳"))),
              bstack1l11l11_opy_ (u"࠭ࡴࡩࡖࡨࡷࡹࡘࡵ࡯ࡗࡸ࡭ࡩ࠭໴"): bstack11ll111ll1_opy_.current_test_uuid() if bstack11ll111ll1_opy_.current_test_uuid() else bstack1l1lllll1l_opy_.current_hook_uuid(),
              bstack1l11l11_opy_ (u"ࠧࡢࡷࡷ࡬ࡍ࡫ࡡࡥࡧࡵࠫ໵"): os.environ.get(bstack1l11l11_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭໶")),
              bstack1l11l11_opy_ (u"ࠩࡶࡧࡦࡴࡔࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ໷"): str(int(datetime.datetime.now().timestamp() * 1000)),
              bstack1l11l11_opy_ (u"ࠪࡸ࡭ࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ໸"): os.environ.get(bstack1l11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ໹"), bstack1l11l11_opy_ (u"ࠬ࠭໺")),
              bstack1l11l11_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩ࠭໻"): kwargs.get(bstack1l11l11_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸ࡟ࡤࡱࡰࡱࡦࡴࡤࠨ໼"), None) or bstack1l11l11_opy_ (u"ࠨࠩ໽")
          }
        if not hasattr(thread_local, bstack1l11l11_opy_ (u"ࠩࡥࡥࡸ࡫࡟ࡢࡲࡳࡣࡦ࠷࠱ࡺࡡࡶࡧࡷ࡯ࡰࡵࠩ໾")):
            scripts = {bstack1l11l11_opy_ (u"ࠪࡷࡨࡧ࡮ࠨ໿"): bstack11l1ll111l_opy_.perform_scan}
            thread_local.base_app_a11y_script = scripts
        bstack1l1l1lll11_opy_ = copy.deepcopy(thread_local.base_app_a11y_script)
        bstack1l1l1lll11_opy_[bstack1l11l11_opy_ (u"ࠫࡸࡩࡡ࡯ࠩༀ")] = bstack1l1l1lll11_opy_[bstack1l11l11_opy_ (u"ࠬࡹࡣࡢࡰࠪ༁")] % json.dumps(bstack1l111l1111_opy_)
        bstack11l1ll111l_opy_.bstack1llll1111l_opy_(bstack1l1l1lll11_opy_)
        bstack11l1ll111l_opy_.store()
        bstack1llllll111_opy_ = driver.execute_script(bstack11l1ll111l_opy_.perform_scan)
      except Exception as bstack1111111ll_opy_:
        logger.info(bstack1l11l11_opy_ (u"ࠨࡁࡱࡲ࡬ࡹࡲࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡤࡣࡱࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࠨ༂") + str(bstack1111111ll_opy_))
        bstack1llllll111_opy_ = {bstack1l11l11_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨ༃"): str(bstack1111111ll_opy_)}
    else:
      bstack1llllll111_opy_ = driver.execute_async_script(bstack11l1ll111l_opy_.perform_scan, {bstack1l11l11_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࠨ༄"): kwargs.get(bstack1l11l11_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࡡࡦࡳࡲࡳࡡ࡯ࡦࠪ༅"), None) or bstack1l11l11_opy_ (u"ࠪࠫ༆")})
    return bstack1llllll111_opy_
  except Exception as err:
    logger.error(bstack1l11l11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡳࡷࡱࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸࡩࡡ࡯࠰ࠣࡿࢂࠨ༇").format(str(err)))
    return {}