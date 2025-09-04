# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
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
from browserstack_sdk.bstack1ll111l1ll_opy_ import bstack11lll111_opy_
from browserstack_sdk.bstack1111111l_opy_ import *
import time
import requests
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.measure import measure
def bstack1lll11l111_opy_():
  global CONFIG
  headers = {
        bstack1111l1l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack1111l1l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack11l1l111ll_opy_(CONFIG, bstack1ll11lll1l_opy_)
  try:
    response = requests.get(bstack1ll11lll1l_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1l11ll1ll1_opy_ = response.json()[bstack1111l1l_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack11lll1lll_opy_.format(response.json()))
      return bstack1l11ll1ll1_opy_
    else:
      logger.debug(bstack111llll11l_opy_.format(bstack1111l1l_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack111llll11l_opy_.format(e))
def bstack1l11111ll_opy_(hub_url):
  global CONFIG
  url = bstack1111l1l_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack1111l1l_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack1111l1l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack1111l1l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack11l1l111ll_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1lll111ll1_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1l1111ll_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack1l111lll11_opy_, stage=STAGE.bstack1l1111l1ll_opy_)
def bstack1ll1111111_opy_():
  try:
    global bstack1l111l1ll_opy_
    bstack1l11ll1ll1_opy_ = bstack1lll11l111_opy_()
    bstack111l1l1l_opy_ = []
    results = []
    for bstack11ll111ll1_opy_ in bstack1l11ll1ll1_opy_:
      bstack111l1l1l_opy_.append(bstack111l1111l_opy_(target=bstack1l11111ll_opy_,args=(bstack11ll111ll1_opy_,)))
    for t in bstack111l1l1l_opy_:
      t.start()
    for t in bstack111l1l1l_opy_:
      results.append(t.join())
    bstack11ll1lllll_opy_ = {}
    for item in results:
      hub_url = item[bstack1111l1l_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack1111l1l_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack11ll1lllll_opy_[hub_url] = latency
    bstack1l1llllll_opy_ = min(bstack11ll1lllll_opy_, key= lambda x: bstack11ll1lllll_opy_[x])
    bstack1l111l1ll_opy_ = bstack1l1llllll_opy_
    logger.debug(bstack1l111lll1_opy_.format(bstack1l1llllll_opy_))
  except Exception as e:
    logger.debug(bstack1l1l1l1lll_opy_.format(e))
from browserstack_sdk.bstack1l111llll1_opy_ import *
from browserstack_sdk.bstack1llll11l11_opy_ import *
from browserstack_sdk.bstack1lll1ll1_opy_ import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.bstack11l1111l1_opy_ import get_logger
from bstack_utils.measure import measure
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack1l111lll1l_opy_, stage=STAGE.bstack1l1111l1ll_opy_)
def bstack1l1ll1l111_opy_():
    global bstack1l111l1ll_opy_
    try:
        bstack1ll11l1lll_opy_ = bstack1ll1l11l_opy_()
        bstack1l11lll1l_opy_(bstack1ll11l1lll_opy_)
        hub_url = bstack1ll11l1lll_opy_.get(bstack1111l1l_opy_ (u"ࠨࡵࡳ࡮ࠥࢀ"), bstack1111l1l_opy_ (u"ࠢࠣࢁ"))
        if hub_url.endswith(bstack1111l1l_opy_ (u"ࠨ࠱ࡺࡨ࠴࡮ࡵࡣࠩࢂ")):
            hub_url = hub_url.rsplit(bstack1111l1l_opy_ (u"ࠩ࠲ࡻࡩ࠵ࡨࡶࡤࠪࢃ"), 1)[0]
        if hub_url.startswith(bstack1111l1l_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫࢄ")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack1111l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࠭ࢅ")):
            hub_url = hub_url[8:]
        bstack1l111l1ll_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack1ll1l11l_opy_():
    global CONFIG
    bstack1l111l11_opy_ = CONFIG.get(bstack1111l1l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢆ"), {}).get(bstack1111l1l_opy_ (u"࠭ࡧࡳ࡫ࡧࡒࡦࡳࡥࠨࢇ"), bstack1111l1l_opy_ (u"ࠧࡏࡑࡢࡋࡗࡏࡄࡠࡐࡄࡑࡊࡥࡐࡂࡕࡖࡉࡉ࠭࢈"))
    if not isinstance(bstack1l111l11_opy_, str):
        raise ValueError(bstack1111l1l_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡈࡴ࡬ࡨࠥࡴࡡ࡮ࡧࠣࡱࡺࡹࡴࠡࡤࡨࠤࡦࠦࡶࡢ࡮࡬ࡨࠥࡹࡴࡳ࡫ࡱ࡫ࠧࢉ"))
    try:
        bstack1ll11l1lll_opy_ = bstack1ll1111ll_opy_(bstack1l111l11_opy_)
        return bstack1ll11l1lll_opy_
    except Exception as e:
        logger.error(bstack1111l1l_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣࢊ").format(str(e)))
        return {}
def bstack1ll1111ll_opy_(bstack1l111l11_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack1111l1l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࢋ")] or not CONFIG[bstack1111l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧࢌ")]:
            raise ValueError(bstack1111l1l_opy_ (u"ࠧࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠠࡰࡴࠣࡥࡨࡩࡥࡴࡵࠣ࡯ࡪࡿࠢࢍ"))
        url = bstack1ll1ll1lll_opy_ + bstack1l111l11_opy_
        auth = (CONFIG[bstack1111l1l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨࢎ")], CONFIG[bstack1111l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ࢏")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack1ll11l1l1_opy_ = json.loads(response.text)
            return bstack1ll11l1l1_opy_
    except ValueError as ve:
        logger.error(bstack1111l1l_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣ࢐").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack1111l1l_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥ࡭ࡲࡪࡦࠣࡨࡪࡺࡡࡪ࡮ࡶࠤ࠿ࠦࡻࡾࠤ࢑").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack1l11lll1l_opy_(bstack1ll11ll11_opy_):
    global CONFIG
    if bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ࢒") not in CONFIG or str(CONFIG[bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ࢓")]).lower() == bstack1111l1l_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ࢔"):
        CONFIG[bstack1111l1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬ࢕")] = False
    elif bstack1111l1l_opy_ (u"ࠧࡪࡵࡗࡶ࡮ࡧ࡬ࡈࡴ࡬ࡨࠬ࢖") in bstack1ll11ll11_opy_:
        bstack1ll11l111_opy_ = CONFIG.get(bstack1111l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢗ"), {})
        logger.debug(bstack1111l1l_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡰࡴࡩࡡ࡭ࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࠪࡹࠢ࢘"), bstack1ll11l111_opy_)
        bstack1l1ll1l1ll_opy_ = bstack1ll11ll11_opy_.get(bstack1111l1l_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡕࡩࡵ࡫ࡡࡵࡧࡵࡷ࢙ࠧ"), [])
        bstack11111111_opy_ = bstack1111l1l_opy_ (u"ࠦ࠱ࠨ࢚").join(bstack1l1ll1l1ll_opy_)
        logger.debug(bstack1111l1l_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡈࡻࡳࡵࡱࡰࠤࡷ࡫ࡰࡦࡣࡷࡩࡷࠦࡳࡵࡴ࡬ࡲ࡬ࡀࠠࠦࡵ࢛ࠥ"), bstack11111111_opy_)
        bstack1ll111l11l_opy_ = {
            bstack1111l1l_opy_ (u"ࠨ࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣ࢜"): bstack1111l1l_opy_ (u"ࠢࡢࡶࡶ࠱ࡷ࡫ࡰࡦࡣࡷࡩࡷࠨ࢝"),
            bstack1111l1l_opy_ (u"ࠣࡨࡲࡶࡨ࡫ࡌࡰࡥࡤࡰࠧ࢞"): bstack1111l1l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ࢟"),
            bstack1111l1l_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠧࢠ"): bstack11111111_opy_
        }
        bstack1ll11l111_opy_.update(bstack1ll111l11l_opy_)
        logger.debug(bstack1111l1l_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼࡙ࠣࡵࡪࡡࡵࡧࡧࠤࡱࡵࡣࡢ࡮ࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࠫࡳࠣࢡ"), bstack1ll11l111_opy_)
        CONFIG[bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢢ")] = bstack1ll11l111_opy_
        logger.debug(bstack1111l1l_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡌࡩ࡯ࡣ࡯ࠤࡈࡕࡎࡇࡋࡊ࠾ࠥࠫࡳࠣࢣ"), CONFIG)
def bstack11l11l1111_opy_():
    bstack1ll11l1lll_opy_ = bstack1ll1l11l_opy_()
    if not bstack1ll11l1lll_opy_[bstack1111l1l_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࡙ࡷࡲࠧࢤ")]:
      raise ValueError(bstack1111l1l_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࡚ࡸ࡬ࠡ࡫ࡶࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࡬ࡲࡰ࡯ࠣ࡫ࡷ࡯ࡤࠡࡦࡨࡸࡦ࡯࡬ࡴ࠰ࠥࢥ"))
    return bstack1ll11l1lll_opy_[bstack1111l1l_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࡛ࡲ࡭ࠩࢦ")] + bstack1111l1l_opy_ (u"ࠪࡃࡨࡧࡰࡴ࠿ࠪࢧ")
@measure(event_name=EVENTS.bstack1l11ll11_opy_, stage=STAGE.bstack1l1111l1ll_opy_)
def bstack111l11111_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack1111l1l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ࢨ")], CONFIG[bstack1111l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࢩ")])
        url = bstack11ll1llll1_opy_
        logger.debug(bstack1111l1l_opy_ (u"ࠨࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬ࡲࡰ࡯ࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡗࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࠦࡁࡑࡋࠥࢪ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack1111l1l_opy_ (u"ࠢࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪࠨࢫ"): bstack1111l1l_opy_ (u"ࠣࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠦࢬ")})
            if response.status_code == 200:
                bstack1lll1l1lll_opy_ = json.loads(response.text)
                bstack1l11llll1l_opy_ = bstack1lll1l1lll_opy_.get(bstack1111l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡴࠩࢭ"), [])
                if bstack1l11llll1l_opy_:
                    bstack1l1l1l1l_opy_ = bstack1l11llll1l_opy_[0]
                    build_hashed_id = bstack1l1l1l1l_opy_.get(bstack1111l1l_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ࢮ"))
                    bstack11ll1l111l_opy_ = bstack11ll1ll11l_opy_ + build_hashed_id
                    result.extend([build_hashed_id, bstack11ll1l111l_opy_])
                    logger.info(bstack1l1llll1l_opy_.format(bstack11ll1l111l_opy_))
                    bstack1ll11l11ll_opy_ = CONFIG[bstack1111l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧࢯ")]
                    if bstack1111l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢰ") in CONFIG:
                      bstack1ll11l11ll_opy_ += bstack1111l1l_opy_ (u"࠭ࠠࠨࢱ") + CONFIG[bstack1111l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࢲ")]
                    if bstack1ll11l11ll_opy_ != bstack1l1l1l1l_opy_.get(bstack1111l1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ࢳ")):
                      logger.debug(bstack1l11ll111l_opy_.format(bstack1l1l1l1l_opy_.get(bstack1111l1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧࢴ")), bstack1ll11l11ll_opy_))
                    return result
                else:
                    logger.debug(bstack1111l1l_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡑࡳࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡵࡪࡨࠤࡷ࡫ࡳࡱࡱࡱࡷࡪ࠴ࠢࢵ"))
            else:
                logger.debug(bstack1111l1l_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢶ"))
        except Exception as e:
            logger.error(bstack1111l1l_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࡹࠠ࠻ࠢࡾࢁࠧࢷ").format(str(e)))
    else:
        logger.debug(bstack1111l1l_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡉࡏࡏࡈࡌࡋࠥ࡯ࡳࠡࡰࡲࡸࠥࡹࡥࡵ࠰࡙ࠣࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢸ"))
    return [None, None]
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack11lllll1ll_opy_ import bstack11lllll1ll_opy_, bstack1l111l1111_opy_, bstack11l1lll1l_opy_, bstack11l11l11l1_opy_
from bstack_utils.measure import bstack1lllll1ll_opy_
from bstack_utils.measure import measure
from bstack_utils.percy import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack111ll111_opy_ import bstack11l1ll11ll_opy_
from bstack_utils.messages import *
from bstack_utils import bstack11l1111l1_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1l1111ll1l_opy_, bstack1ll111l111_opy_, bstack1l11lll111_opy_, bstack1l11l1lll_opy_, \
  bstack111l1l11_opy_, \
  Notset, bstack11l1l1l11_opy_, \
  bstack1l1111lll1_opy_, bstack1lll11111_opy_, bstack1l1ll1ll1_opy_, bstack1ll111ll_opy_, bstack1ll1l1l1l1_opy_, bstack1l11l111l1_opy_, \
  bstack11llll111l_opy_, \
  bstack1l1111l11_opy_, bstack1lllll1lll_opy_, bstack11lllll1l1_opy_, bstack1ll1l1l1_opy_, \
  bstack111111ll_opy_, bstack1l1ll1l1l_opy_, bstack1lll1l11l_opy_, bstack11l1llll11_opy_
from bstack_utils.bstack1llll111ll_opy_ import bstack11l11l11_opy_
from bstack_utils.bstack1l1lll11_opy_ import bstack11llll11l1_opy_, bstack1ll11l11l1_opy_
from bstack_utils.bstack1ll11l111l_opy_ import bstack11llllll1_opy_
from bstack_utils.bstack1ll1l11l11_opy_ import bstack1l11111l1l_opy_, bstack1l11l11l1l_opy_
from bstack_utils.bstack1ll1ll1ll1_opy_ import bstack1ll1ll1ll1_opy_
from bstack_utils.bstack1l1l1llll1_opy_ import bstack11llllllll_opy_
from bstack_utils.proxy import bstack111ll11l1_opy_, bstack11l1l111ll_opy_, bstack1l11l11ll_opy_, bstack1llll111_opy_
from bstack_utils.bstack1l1l11111l_opy_ import bstack11l1llllll_opy_
import bstack_utils.bstack1l111ll11_opy_ as bstack1l11ll1l1l_opy_
import bstack_utils.bstack1lll111l_opy_ as bstack111lll1l1_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.utils.bstack1l1l1ll11_opy_ import bstack1llllllll_opy_
from bstack_utils.bstack11llllll_opy_ import bstack111l1llll_opy_
from bstack_utils.bstack1l1ll11ll1_opy_ import bstack1111l111_opy_
if os.getenv(bstack1111l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡌࡔࡕࡋࡔࠩࢹ")):
  cli.bstack1lllll11l1_opy_()
else:
  os.environ[bstack1111l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡍࡕࡏࡌࡕࠪࢺ")] = bstack1111l1l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧࢻ")
bstack1ll11llll_opy_ = bstack1111l1l_opy_ (u"ࠪࠤࠥ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࠣࠤ࡮࡬ࠨࡱࡣࡪࡩࠥࡃ࠽࠾ࠢࡹࡳ࡮ࡪࠠ࠱ࠫࠣࡿࡡࡴࠠࠡࠢࡷࡶࡾࢁ࡜࡯ࠢࡦࡳࡳࡹࡴࠡࡨࡶࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨ࡝ࠩࡩࡷࡡ࠭ࠩ࠼࡞ࡱࠤࠥࠦࠠࠡࡨࡶ࠲ࡦࡶࡰࡦࡰࡧࡊ࡮ࡲࡥࡔࡻࡱࡧ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪ࠯ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡶ࡟ࡪࡰࡧࡩࡽ࠯ࠠࠬࠢࠥ࠾ࠧࠦࠫࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࠨࡢࡹࡤ࡭ࡹࠦ࡮ࡦࡹࡓࡥ࡬࡫࠲࠯ࡧࡹࡥࡱࡻࡡࡵࡧࠫࠦ࠭࠯ࠠ࠾ࡀࠣࡿࢂࠨࠬࠡ࡞ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥ࡫ࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡄࡦࡶࡤ࡭ࡱࡹࠢࡾ࡞ࠪ࠭࠮࠯࡛ࠣࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠦࡢ࠯ࠠࠬࠢࠥ࠰ࡡࡢ࡮ࠣࠫ࡟ࡲࠥࠦࠠࠡࡿࡦࡥࡹࡩࡨࠩࡧࡻ࠭ࢀࡢ࡮ࠡࠢࠣࠤࢂࡢ࡮ࠡࠢࢀࡠࡳࠦࠠ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱ࠪࢼ")
bstack1ll1l1ll1_opy_ = bstack1111l1l_opy_ (u"ࠫࡡࡴ࠯ࠫࠢࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࠦࠪ࠰࡞ࡱࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠶ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡩࡡࡱࡵࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠷࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡲࡢ࡭ࡳࡪࡥࡹࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠷ࡣ࡜࡯ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯ࡵ࡯࡭ࡨ࡫ࠨ࠱࠮ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸࠯࡜࡯ࡥࡲࡲࡸࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯ࠥࡃࠠࡳࡧࡴࡹ࡮ࡸࡥࠩࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨࠩ࠼࡞ࡱ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡰࡦࡻ࡮ࡤࡪࠣࡁࠥࡧࡳࡺࡰࡦࠤ࠭ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷ࠮ࠦ࠽࠿ࠢࡾࡠࡳࡲࡥࡵࠢࡦࡥࡵࡹ࠻࡝ࡰࡷࡶࡾࠦࡻ࡝ࡰࡦࡥࡵࡹࠠ࠾ࠢࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࡢࡴࡶࡤࡧࡰࡥࡣࡢࡲࡶ࠭ࡡࡴࠠࠡࡿࠣࡧࡦࡺࡣࡩࠪࡨࡼ࠮ࠦࡻ࡝ࡰࠣࠤࠥࠦࡽ࡝ࡰࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࠻ࠢࡣࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠩࢁࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭ࢂࡦࠬ࡝ࡰࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴ࡞ࡱࠤࠥࢃࠩ࡝ࡰࢀࡠࡳ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࠪࢽ")
from ._version import __version__
bstack1ll11111_opy_ = None
CONFIG = {}
bstack11lllll11_opy_ = {}
bstack1ll1lll1_opy_ = {}
bstack11111l1ll_opy_ = None
bstack111l11l11_opy_ = None
bstack1lllllllll_opy_ = None
bstack1l1ll11lll_opy_ = -1
bstack1l1l1ll1l1_opy_ = 0
bstack1l1ll11l1l_opy_ = bstack1ll111ll11_opy_
bstack1l11l11111_opy_ = 1
bstack11llll1lll_opy_ = False
bstack11l11l11ll_opy_ = False
bstack1l111l11l1_opy_ = bstack1111l1l_opy_ (u"ࠬ࠭ࢾ")
bstack1lll1ll11_opy_ = bstack1111l1l_opy_ (u"࠭ࠧࢿ")
bstack111lll111_opy_ = False
bstack11111l11l_opy_ = True
bstack1lllll111l_opy_ = bstack1111l1l_opy_ (u"ࠧࠨࣀ")
bstack1l11l11l1_opy_ = []
bstack1ll11l1l11_opy_ = threading.Lock()
bstack11l1l1l1l_opy_ = threading.Lock()
bstack1l111l1ll_opy_ = bstack1111l1l_opy_ (u"ࠨࠩࣁ")
bstack11ll11l1l_opy_ = False
bstack11l1l1l1ll_opy_ = None
bstack11ll1ll1l1_opy_ = None
bstack11lll11lll_opy_ = None
bstack1l1ll1lll1_opy_ = -1
bstack11ll111l1l_opy_ = os.path.join(os.path.expanduser(bstack1111l1l_opy_ (u"ࠩࢁࠫࣂ")), bstack1111l1l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪࣃ"), bstack1111l1l_opy_ (u"ࠫ࠳ࡸ࡯ࡣࡱࡷ࠱ࡷ࡫ࡰࡰࡴࡷ࠱࡭࡫࡬ࡱࡧࡵ࠲࡯ࡹ࡯࡯ࠩࣄ"))
bstack111ll11ll_opy_ = 0
bstack1l1llllll1_opy_ = 0
bstack11l1lllll_opy_ = []
bstack1lllll11_opy_ = []
bstack1llll11111_opy_ = []
bstack1lll11llll_opy_ = []
bstack1ll11ll111_opy_ = bstack1111l1l_opy_ (u"ࠬ࠭ࣅ")
bstack1lll1l1l1l_opy_ = bstack1111l1l_opy_ (u"࠭ࠧࣆ")
bstack11ll1l1ll_opy_ = False
bstack1l1l1ll111_opy_ = False
bstack111111ll1_opy_ = {}
bstack1l1llll11_opy_ = None
bstack11lllll11l_opy_ = None
bstack1l11111l1_opy_ = None
bstack11l11l1l1_opy_ = None
bstack11l11lllll_opy_ = None
bstack11lll1l11l_opy_ = None
bstack1llll1l1ll_opy_ = None
bstack1ll1111l11_opy_ = None
bstack1l11ll11l_opy_ = None
bstack11l11ll1l1_opy_ = None
bstack1l1ll1l1l1_opy_ = None
bstack1ll1l1llll_opy_ = None
bstack1ll1ll1111_opy_ = None
bstack1111l11l1_opy_ = None
bstack1lll1llll1_opy_ = None
bstack11lll111l1_opy_ = None
bstack1l1llll11l_opy_ = None
bstack1ll1l1l1ll_opy_ = None
bstack1l111111l1_opy_ = None
bstack1l1lllll1l_opy_ = None
bstack1ll1ll11ll_opy_ = None
bstack1l1l111ll1_opy_ = None
bstack111l1l1ll_opy_ = None
thread_local = threading.local()
bstack11111l111_opy_ = False
bstack1ll1l11l1l_opy_ = bstack1111l1l_opy_ (u"ࠢࠣࣇ")
logger = bstack11l1111l1_opy_.get_logger(__name__, bstack1l1ll11l1l_opy_)
bstack1l1ll11l1_opy_ = Config.bstack1l11llll1_opy_()
percy = bstack1llll111l1_opy_()
bstack11l1lll11_opy_ = bstack11l1ll11ll_opy_()
bstack11l1l11l1_opy_ = bstack1lll1ll1_opy_()
def bstack11l11111l1_opy_():
  global CONFIG
  global bstack11ll1l1ll_opy_
  global bstack1l1ll11l1_opy_
  testContextOptions = bstack1ll1ll111_opy_(CONFIG)
  if bstack111l1l11_opy_(CONFIG):
    if (bstack1111l1l_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪࣈ") in testContextOptions and str(testContextOptions[bstack1111l1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫࣉ")]).lower() == bstack1111l1l_opy_ (u"ࠪࡸࡷࡻࡥࠨ࣊")):
      bstack11ll1l1ll_opy_ = True
    bstack1l1ll11l1_opy_.bstack11l1l1lll_opy_(testContextOptions.get(bstack1111l1l_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ࣋"), False))
  else:
    bstack11ll1l1ll_opy_ = True
    bstack1l1ll11l1_opy_.bstack11l1l1lll_opy_(True)
def bstack11l111l1l_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1ll1l1lll1_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack11ll1l1111_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1111l1l_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡩ࡯࡯ࡨ࡬࡫࡫࡯࡬ࡦࠤ࣌") == args[i].lower() or bstack1111l1l_opy_ (u"ࠨ࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡪ࡮࡭ࠢ࣍") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1lllll111l_opy_
      bstack1lllll111l_opy_ += bstack1111l1l_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠤࠧ࠭࣎") + path + bstack1111l1l_opy_ (u"ࠨࠤ࣏ࠪ")
      return path
  return None
bstack1ll1llll_opy_ = re.compile(bstack1111l1l_opy_ (u"ࡴࠥ࠲࠯ࡅ࡜ࠥࡽࠫ࠲࠯ࡅࠩࡾ࠰࠭ࡃ࣐ࠧ"))
def bstack111llll111_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1ll1llll_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack1111l1l_opy_ (u"ࠥࠨࢀࠨ࣑") + group + bstack1111l1l_opy_ (u"ࠦࢂࠨ࣒"), os.environ.get(group))
  return value
def bstack1llll1ll1_opy_():
  global bstack111l1l1ll_opy_
  if bstack111l1l1ll_opy_ is None:
        bstack111l1l1ll_opy_ = bstack11ll1l1111_opy_()
  bstack1l1l11l1ll_opy_ = bstack111l1l1ll_opy_
  if bstack1l1l11l1ll_opy_ and os.path.exists(os.path.abspath(bstack1l1l11l1ll_opy_)):
    fileName = bstack1l1l11l1ll_opy_
  if bstack1111l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆ࣓ࠩ") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack1111l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࡤࡌࡉࡍࡇࠪࣔ")])) and not bstack1111l1l_opy_ (u"ࠧࡧ࡫࡯ࡩࡓࡧ࡭ࡦࠩࣕ") in locals():
    fileName = os.environ[bstack1111l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬࣖ")]
  if bstack1111l1l_opy_ (u"ࠩࡩ࡭ࡱ࡫ࡎࡢ࡯ࡨࠫࣗ") in locals():
    bstack1l1llll_opy_ = os.path.abspath(fileName)
  else:
    bstack1l1llll_opy_ = bstack1111l1l_opy_ (u"ࠪࠫࣘ")
  bstack11lll1l1ll_opy_ = os.getcwd()
  bstack11l1l1l11l_opy_ = bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧࣙ")
  bstack1l1lll1l1l_opy_ = bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡧ࡭࡭ࠩࣚ")
  while (not os.path.exists(bstack1l1llll_opy_)) and bstack11lll1l1ll_opy_ != bstack1111l1l_opy_ (u"ࠨࠢࣛ"):
    bstack1l1llll_opy_ = os.path.join(bstack11lll1l1ll_opy_, bstack11l1l1l11l_opy_)
    if not os.path.exists(bstack1l1llll_opy_):
      bstack1l1llll_opy_ = os.path.join(bstack11lll1l1ll_opy_, bstack1l1lll1l1l_opy_)
    if bstack11lll1l1ll_opy_ != os.path.dirname(bstack11lll1l1ll_opy_):
      bstack11lll1l1ll_opy_ = os.path.dirname(bstack11lll1l1ll_opy_)
    else:
      bstack11lll1l1ll_opy_ = bstack1111l1l_opy_ (u"ࠢࠣࣜ")
  bstack111l1l1ll_opy_ = bstack1l1llll_opy_ if os.path.exists(bstack1l1llll_opy_) else None
  return bstack111l1l1ll_opy_
def bstack1lll1l1l_opy_(config):
    if bstack1111l1l_opy_ (u"ࠨࡶࡨࡷࡹࡘࡥࡱࡱࡵࡸ࡮ࡴࡧࠨࣝ") in config:
      config[bstack1111l1l_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ࣞ")] = config[bstack1111l1l_opy_ (u"ࠪࡸࡪࡹࡴࡓࡧࡳࡳࡷࡺࡩ࡯ࡩࠪࣟ")]
    if bstack1111l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࡓࡵࡺࡩࡰࡰࡶࠫ࣠") in config:
      config[bstack1111l1l_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ࣡")] = config[bstack1111l1l_opy_ (u"࠭ࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬ࡕࡰࡵ࡫ࡲࡲࡸ࠭࣢")]
def bstack1l1l111l_opy_():
  bstack1l1llll_opy_ = bstack1llll1ll1_opy_()
  if not os.path.exists(bstack1l1llll_opy_):
    bstack1111ll1l1_opy_(
      bstack1l1lll111l_opy_.format(os.getcwd()))
  try:
    with open(bstack1l1llll_opy_, bstack1111l1l_opy_ (u"ࠧࡳࣣࠩ")) as stream:
      yaml.add_implicit_resolver(bstack1111l1l_opy_ (u"ࠣࠣࡳࡥࡹ࡮ࡥࡹࠤࣤ"), bstack1ll1llll_opy_)
      yaml.add_constructor(bstack1111l1l_opy_ (u"ࠤࠤࡴࡦࡺࡨࡦࡺࠥࣥ"), bstack111llll111_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      bstack1lll1l1l_opy_(config)
      return config
  except:
    with open(bstack1l1llll_opy_, bstack1111l1l_opy_ (u"ࠪࡶࣦࠬ")) as stream:
      try:
        config = yaml.safe_load(stream)
        bstack1lll1l1l_opy_(config)
        return config
      except yaml.YAMLError as exc:
        bstack1111ll1l1_opy_(bstack111lllll_opy_.format(str(exc)))
def bstack1l11l1l1_opy_(config):
  bstack11llll1l_opy_ = bstack1l1l1111l_opy_(config)
  for option in list(bstack11llll1l_opy_):
    if option.lower() in bstack111ll1l1l_opy_ and option != bstack111ll1l1l_opy_[option.lower()]:
      bstack11llll1l_opy_[bstack111ll1l1l_opy_[option.lower()]] = bstack11llll1l_opy_[option]
      del bstack11llll1l_opy_[option]
  return config
def bstack1lll111lll_opy_():
  global bstack1ll1lll1_opy_
  for key, bstack1l1111l11l_opy_ in bstack11lll1l1_opy_.items():
    if isinstance(bstack1l1111l11l_opy_, list):
      for var in bstack1l1111l11l_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1ll1lll1_opy_[key] = os.environ[var]
          break
    elif bstack1l1111l11l_opy_ in os.environ and os.environ[bstack1l1111l11l_opy_] and str(os.environ[bstack1l1111l11l_opy_]).strip():
      bstack1ll1lll1_opy_[key] = os.environ[bstack1l1111l11l_opy_]
  if bstack1111l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ࣧ") in os.environ:
    bstack1ll1lll1_opy_[bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣨ")] = {}
    bstack1ll1lll1_opy_[bstack1111l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࣩࠪ")][bstack1111l1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ࣪")] = os.environ[bstack1111l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪ࣫")]
def bstack11l111lll_opy_():
  global bstack11lllll11_opy_
  global bstack1lllll111l_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack1111l1l_opy_ (u"ࠩ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ࣬").lower() == val.lower():
      bstack11lllll11_opy_[bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹ࣭ࠧ")] = {}
      bstack11lllll11_opy_[bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ࣮")][bstack1111l1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣯ࠧ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack1l1ll11111_opy_ in bstack1lll11l1l_opy_.items():
    if isinstance(bstack1l1ll11111_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1l1ll11111_opy_:
          if idx < len(sys.argv) and bstack1111l1l_opy_ (u"࠭࠭࠮ࣰࠩ") + var.lower() == val.lower() and not key in bstack11lllll11_opy_:
            bstack11lllll11_opy_[key] = sys.argv[idx + 1]
            bstack1lllll111l_opy_ += bstack1111l1l_opy_ (u"ࠧࠡ࠯࠰ࣱࠫ") + var + bstack1111l1l_opy_ (u"ࠨࣲࠢࠪ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack1111l1l_opy_ (u"ࠩ࠰࠱ࠬࣳ") + bstack1l1ll11111_opy_.lower() == val.lower() and not key in bstack11lllll11_opy_:
          bstack11lllll11_opy_[key] = sys.argv[idx + 1]
          bstack1lllll111l_opy_ += bstack1111l1l_opy_ (u"ࠪࠤ࠲࠳ࠧࣴ") + bstack1l1ll11111_opy_ + bstack1111l1l_opy_ (u"ࠫࠥ࠭ࣵ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1l111111l_opy_(config):
  bstack1lll11lll1_opy_ = config.keys()
  for bstack11lll1ll_opy_, bstack11l1111ll_opy_ in bstack1lll11ll11_opy_.items():
    if bstack11l1111ll_opy_ in bstack1lll11lll1_opy_:
      config[bstack11lll1ll_opy_] = config[bstack11l1111ll_opy_]
      del config[bstack11l1111ll_opy_]
  for bstack11lll1ll_opy_, bstack11l1111ll_opy_ in bstack1ll1ll11_opy_.items():
    if isinstance(bstack11l1111ll_opy_, list):
      for bstack1lll11lll_opy_ in bstack11l1111ll_opy_:
        if bstack1lll11lll_opy_ in bstack1lll11lll1_opy_:
          config[bstack11lll1ll_opy_] = config[bstack1lll11lll_opy_]
          del config[bstack1lll11lll_opy_]
          break
    elif bstack11l1111ll_opy_ in bstack1lll11lll1_opy_:
      config[bstack11lll1ll_opy_] = config[bstack11l1111ll_opy_]
      del config[bstack11l1111ll_opy_]
  for bstack1lll11lll_opy_ in list(config):
    for bstack11l1llll1_opy_ in bstack1l11lllll1_opy_:
      if bstack1lll11lll_opy_.lower() == bstack11l1llll1_opy_.lower() and bstack1lll11lll_opy_ != bstack11l1llll1_opy_:
        config[bstack11l1llll1_opy_] = config[bstack1lll11lll_opy_]
        del config[bstack1lll11lll_opy_]
  bstack1ll11111l1_opy_ = [{}]
  if not config.get(bstack1111l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨࣶ")):
    config[bstack1111l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩࣷ")] = [{}]
  bstack1ll11111l1_opy_ = config[bstack1111l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪࣸ")]
  for platform in bstack1ll11111l1_opy_:
    for bstack1lll11lll_opy_ in list(platform):
      for bstack11l1llll1_opy_ in bstack1l11lllll1_opy_:
        if bstack1lll11lll_opy_.lower() == bstack11l1llll1_opy_.lower() and bstack1lll11lll_opy_ != bstack11l1llll1_opy_:
          platform[bstack11l1llll1_opy_] = platform[bstack1lll11lll_opy_]
          del platform[bstack1lll11lll_opy_]
  for bstack11lll1ll_opy_, bstack11l1111ll_opy_ in bstack1ll1ll11_opy_.items():
    for platform in bstack1ll11111l1_opy_:
      if isinstance(bstack11l1111ll_opy_, list):
        for bstack1lll11lll_opy_ in bstack11l1111ll_opy_:
          if bstack1lll11lll_opy_ in platform:
            platform[bstack11lll1ll_opy_] = platform[bstack1lll11lll_opy_]
            del platform[bstack1lll11lll_opy_]
            break
      elif bstack11l1111ll_opy_ in platform:
        platform[bstack11lll1ll_opy_] = platform[bstack11l1111ll_opy_]
        del platform[bstack11l1111ll_opy_]
  for bstack1l11l111_opy_ in bstack1l1ll11ll_opy_:
    if bstack1l11l111_opy_ in config:
      if not bstack1l1ll11ll_opy_[bstack1l11l111_opy_] in config:
        config[bstack1l1ll11ll_opy_[bstack1l11l111_opy_]] = {}
      config[bstack1l1ll11ll_opy_[bstack1l11l111_opy_]].update(config[bstack1l11l111_opy_])
      del config[bstack1l11l111_opy_]
  for platform in bstack1ll11111l1_opy_:
    for bstack1l11l111_opy_ in bstack1l1ll11ll_opy_:
      if bstack1l11l111_opy_ in list(platform):
        if not bstack1l1ll11ll_opy_[bstack1l11l111_opy_] in platform:
          platform[bstack1l1ll11ll_opy_[bstack1l11l111_opy_]] = {}
        platform[bstack1l1ll11ll_opy_[bstack1l11l111_opy_]].update(platform[bstack1l11l111_opy_])
        del platform[bstack1l11l111_opy_]
  config = bstack1l11l1l1_opy_(config)
  return config
def bstack1l11l1l11_opy_(config):
  global bstack1lll1ll11_opy_
  bstack1111l111l_opy_ = False
  if bstack1111l1l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࣹࠬ") in config and str(config[bstack1111l1l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࣺ࠭")]).lower() != bstack1111l1l_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩࣻ"):
    if bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨࣼ") not in config or str(config[bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩࣽ")]).lower() == bstack1111l1l_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬࣾ"):
      config[bstack1111l1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭ࣿ")] = False
    else:
      bstack1ll11l1lll_opy_ = bstack1ll1l11l_opy_()
      if bstack1111l1l_opy_ (u"ࠨ࡫ࡶࡘࡷ࡯ࡡ࡭ࡉࡵ࡭ࡩ࠭ऀ") in bstack1ll11l1lll_opy_:
        if not bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ँ") in config:
          config[bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧं")] = {}
        config[bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨः")][bstack1111l1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऄ")] = bstack1111l1l_opy_ (u"࠭ࡡࡵࡵ࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠬअ")
        bstack1111l111l_opy_ = True
        bstack1lll1ll11_opy_ = config[bstack1111l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫआ")].get(bstack1111l1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪइ"))
  if bstack111l1l11_opy_(config) and bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ई") in config and str(config[bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧउ")]).lower() != bstack1111l1l_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪऊ") and not bstack1111l111l_opy_:
    if not bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩऋ") in config:
      config[bstack1111l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪऌ")] = {}
    if not config[bstack1111l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫऍ")].get(bstack1111l1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡈࡩ࡯ࡣࡵࡽࡎࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡡࡵ࡫ࡲࡲࠬऎ")) and not bstack1111l1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫए") in config[bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧऐ")]:
      bstack1ll111ll1l_opy_ = datetime.datetime.now()
      bstack11llll1l1l_opy_ = bstack1ll111ll1l_opy_.strftime(bstack1111l1l_opy_ (u"ࠫࠪࡪ࡟ࠦࡤࡢࠩࡍࠫࡍࠨऑ"))
      hostname = socket.gethostname()
      bstack11llll1ll1_opy_ = bstack1111l1l_opy_ (u"ࠬ࠭ऒ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1111l1l_opy_ (u"࠭ࡻࡾࡡࡾࢁࡤࢁࡽࠨओ").format(bstack11llll1l1l_opy_, hostname, bstack11llll1ll1_opy_)
      config[bstack1111l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫऔ")][bstack1111l1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪक")] = identifier
    bstack1lll1ll11_opy_ = config[bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ख")].get(bstack1111l1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬग"))
  return config
def bstack1l11l1111_opy_():
  bstack11lll11l11_opy_ =  bstack1ll111ll_opy_()[bstack1111l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠪघ")]
  return bstack11lll11l11_opy_ if bstack11lll11l11_opy_ else -1
def bstack1l1l1l111l_opy_(bstack11lll11l11_opy_):
  global CONFIG
  if not bstack1111l1l_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧङ") in CONFIG[bstack1111l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨच")]:
    return
  CONFIG[bstack1111l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩछ")] = CONFIG[bstack1111l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪज")].replace(
    bstack1111l1l_opy_ (u"ࠩࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫझ"),
    str(bstack11lll11l11_opy_)
  )
def bstack1l11l11l_opy_():
  global CONFIG
  if not bstack1111l1l_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾࠩञ") in CONFIG[bstack1111l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ट")]:
    return
  bstack1ll111ll1l_opy_ = datetime.datetime.now()
  bstack11llll1l1l_opy_ = bstack1ll111ll1l_opy_.strftime(bstack1111l1l_opy_ (u"ࠬࠫࡤ࠮ࠧࡥ࠱ࠪࡎ࠺ࠦࡏࠪठ"))
  CONFIG[bstack1111l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨड")] = CONFIG[bstack1111l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩढ")].replace(
    bstack1111l1l_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧण"),
    bstack11llll1l1l_opy_
  )
def bstack111l111l1_opy_():
  global CONFIG
  if bstack1111l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫत") in CONFIG and not bool(CONFIG[bstack1111l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬथ")]):
    del CONFIG[bstack1111l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭द")]
    return
  if not bstack1111l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧध") in CONFIG:
    CONFIG[bstack1111l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨन")] = bstack1111l1l_opy_ (u"ࠧࠤࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪऩ")
  if bstack1111l1l_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧप") in CONFIG[bstack1111l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫफ")]:
    bstack1l11l11l_opy_()
    os.environ[bstack1111l1l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧब")] = CONFIG[bstack1111l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭भ")]
  if not bstack1111l1l_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧम") in CONFIG[bstack1111l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨय")]:
    return
  bstack11lll11l11_opy_ = bstack1111l1l_opy_ (u"ࠧࠨर")
  bstack11ll1l1l1_opy_ = bstack1l11l1111_opy_()
  if bstack11ll1l1l1_opy_ != -1:
    bstack11lll11l11_opy_ = bstack1111l1l_opy_ (u"ࠨࡅࡌࠤࠬऱ") + str(bstack11ll1l1l1_opy_)
  if bstack11lll11l11_opy_ == bstack1111l1l_opy_ (u"ࠩࠪल"):
    bstack11ll1l11ll_opy_ = bstack1ll111l1l1_opy_(CONFIG[bstack1111l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ळ")])
    if bstack11ll1l11ll_opy_ != -1:
      bstack11lll11l11_opy_ = str(bstack11ll1l11ll_opy_)
  if bstack11lll11l11_opy_:
    bstack1l1l1l111l_opy_(bstack11lll11l11_opy_)
    os.environ[bstack1111l1l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨऴ")] = CONFIG[bstack1111l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧव")]
def bstack1l11l1ll1l_opy_(bstack1l111l11l_opy_, bstack11l1ll11l1_opy_, path):
  bstack1l1ll111l1_opy_ = {
    bstack1111l1l_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪश"): bstack11l1ll11l1_opy_
  }
  if os.path.exists(path):
    bstack1llll11l1_opy_ = json.load(open(path, bstack1111l1l_opy_ (u"ࠧࡳࡤࠪष")))
  else:
    bstack1llll11l1_opy_ = {}
  bstack1llll11l1_opy_[bstack1l111l11l_opy_] = bstack1l1ll111l1_opy_
  with open(path, bstack1111l1l_opy_ (u"ࠣࡹ࠮ࠦस")) as outfile:
    json.dump(bstack1llll11l1_opy_, outfile)
def bstack1ll111l1l1_opy_(bstack1l111l11l_opy_):
  bstack1l111l11l_opy_ = str(bstack1l111l11l_opy_)
  bstack1lllllll1l_opy_ = os.path.join(os.path.expanduser(bstack1111l1l_opy_ (u"ࠩࢁࠫह")), bstack1111l1l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪऺ"))
  try:
    if not os.path.exists(bstack1lllllll1l_opy_):
      os.makedirs(bstack1lllllll1l_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1111l1l_opy_ (u"ࠫࢃ࠭ऻ")), bstack1111l1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯़ࠬ"), bstack1111l1l_opy_ (u"࠭࠮ࡣࡷ࡬ࡰࡩ࠳࡮ࡢ࡯ࡨ࠱ࡨࡧࡣࡩࡧ࠱࡮ࡸࡵ࡮ࠨऽ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1111l1l_opy_ (u"ࠧࡸࠩा")):
        pass
      with open(file_path, bstack1111l1l_opy_ (u"ࠣࡹ࠮ࠦि")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1111l1l_opy_ (u"ࠩࡵࠫी")) as bstack111ll1lll_opy_:
      bstack1llllll11l_opy_ = json.load(bstack111ll1lll_opy_)
    if bstack1l111l11l_opy_ in bstack1llllll11l_opy_:
      bstack1l1111l1l_opy_ = bstack1llllll11l_opy_[bstack1l111l11l_opy_][bstack1111l1l_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧु")]
      bstack1l1l1l11ll_opy_ = int(bstack1l1111l1l_opy_) + 1
      bstack1l11l1ll1l_opy_(bstack1l111l11l_opy_, bstack1l1l1l11ll_opy_, file_path)
      return bstack1l1l1l11ll_opy_
    else:
      bstack1l11l1ll1l_opy_(bstack1l111l11l_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1ll1ll11l1_opy_.format(str(e)))
    return -1
def bstack1ll1lllll_opy_(config):
  if not config[bstack1111l1l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ू")] or not config[bstack1111l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨृ")]:
    return True
  else:
    return False
def bstack1l1l1ll1_opy_(config, index=0):
  global bstack111lll111_opy_
  bstack1l11llll_opy_ = {}
  caps = bstack11111llll_opy_ + bstack1ll1l11111_opy_
  if config.get(bstack1111l1l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪॄ"), False):
    bstack1l11llll_opy_[bstack1111l1l_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫॅ")] = True
    bstack1l11llll_opy_[bstack1111l1l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࡔࡶࡴࡪࡱࡱࡷࠬॆ")] = config.get(bstack1111l1l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭े"), {})
  if bstack111lll111_opy_:
    caps += bstack1lll1l1ll_opy_
  for key in config:
    if key in caps + [bstack1111l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ै")]:
      continue
    bstack1l11llll_opy_[key] = config[key]
  if bstack1111l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॉ") in config:
    for bstack11ll11llll_opy_ in config[bstack1111l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨॊ")][index]:
      if bstack11ll11llll_opy_ in caps:
        continue
      bstack1l11llll_opy_[bstack11ll11llll_opy_] = config[bstack1111l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩो")][index][bstack11ll11llll_opy_]
  bstack1l11llll_opy_[bstack1111l1l_opy_ (u"ࠧࡩࡱࡶࡸࡓࡧ࡭ࡦࠩौ")] = socket.gethostname()
  if bstack1111l1l_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯्ࠩ") in bstack1l11llll_opy_:
    del (bstack1l11llll_opy_[bstack1111l1l_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪॎ")])
  return bstack1l11llll_opy_
def bstack1l1l11ll1_opy_(config):
  global bstack111lll111_opy_
  bstack1lll1lll1_opy_ = {}
  caps = bstack1ll1l11111_opy_
  if bstack111lll111_opy_:
    caps += bstack1lll1l1ll_opy_
  for key in caps:
    if key in config:
      bstack1lll1lll1_opy_[key] = config[key]
  return bstack1lll1lll1_opy_
def bstack11lll11111_opy_(bstack1l11llll_opy_, bstack1lll1lll1_opy_):
  bstack111lll11_opy_ = {}
  for key in bstack1l11llll_opy_.keys():
    if key in bstack1lll11ll11_opy_:
      bstack111lll11_opy_[bstack1lll11ll11_opy_[key]] = bstack1l11llll_opy_[key]
    else:
      bstack111lll11_opy_[key] = bstack1l11llll_opy_[key]
  for key in bstack1lll1lll1_opy_:
    if key in bstack1lll11ll11_opy_:
      bstack111lll11_opy_[bstack1lll11ll11_opy_[key]] = bstack1lll1lll1_opy_[key]
    else:
      bstack111lll11_opy_[key] = bstack1lll1lll1_opy_[key]
  return bstack111lll11_opy_
def bstack1lll1111_opy_(config, index=0):
  global bstack111lll111_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack1l11l11lll_opy_ = bstack1l1111ll1l_opy_(bstack1111l1l1_opy_, config, logger)
  bstack1lll1lll1_opy_ = bstack1l1l11ll1_opy_(config)
  bstack1l111ll1l_opy_ = bstack1ll1l11111_opy_
  bstack1l111ll1l_opy_ += bstack1lllll11ll_opy_
  bstack1lll1lll1_opy_ = update(bstack1lll1lll1_opy_, bstack1l11l11lll_opy_)
  if bstack111lll111_opy_:
    bstack1l111ll1l_opy_ += bstack1lll1l1ll_opy_
  if bstack1111l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॏ") in config:
    if bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩॐ") in config[bstack1111l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ॑")][index]:
      caps[bstack1111l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨ॒ࠫ")] = config[bstack1111l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ॓")][index][bstack1111l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭॔")]
    if bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪॕ") in config[bstack1111l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॖ")][index]:
      caps[bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬॗ")] = str(config[bstack1111l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨक़")][index][bstack1111l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧख़")])
    bstack1l1l111l1_opy_ = bstack1l1111ll1l_opy_(bstack1111l1l1_opy_, config[bstack1111l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪग़")][index], logger)
    bstack1l111ll1l_opy_ += list(bstack1l1l111l1_opy_.keys())
    for bstack1l111111_opy_ in bstack1l111ll1l_opy_:
      if bstack1l111111_opy_ in config[bstack1111l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫज़")][index]:
        if bstack1l111111_opy_ == bstack1111l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫड़"):
          try:
            bstack1l1l111l1_opy_[bstack1l111111_opy_] = str(config[bstack1111l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ढ़")][index][bstack1l111111_opy_] * 1.0)
          except:
            bstack1l1l111l1_opy_[bstack1l111111_opy_] = str(config[bstack1111l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧफ़")][index][bstack1l111111_opy_])
        else:
          bstack1l1l111l1_opy_[bstack1l111111_opy_] = config[bstack1111l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨय़")][index][bstack1l111111_opy_]
        del (config[bstack1111l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩॠ")][index][bstack1l111111_opy_])
    bstack1lll1lll1_opy_ = update(bstack1lll1lll1_opy_, bstack1l1l111l1_opy_)
  bstack1l11llll_opy_ = bstack1l1l1ll1_opy_(config, index)
  for bstack1lll11lll_opy_ in bstack1ll1l11111_opy_ + list(bstack1l11l11lll_opy_.keys()):
    if bstack1lll11lll_opy_ in bstack1l11llll_opy_:
      bstack1lll1lll1_opy_[bstack1lll11lll_opy_] = bstack1l11llll_opy_[bstack1lll11lll_opy_]
      del (bstack1l11llll_opy_[bstack1lll11lll_opy_])
  if bstack11l1l1l11_opy_(config):
    bstack1l11llll_opy_[bstack1111l1l_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧॡ")] = True
    caps.update(bstack1lll1lll1_opy_)
    caps[bstack1111l1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩॢ")] = bstack1l11llll_opy_
  else:
    bstack1l11llll_opy_[bstack1111l1l_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩॣ")] = False
    caps.update(bstack11lll11111_opy_(bstack1l11llll_opy_, bstack1lll1lll1_opy_))
    if bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ।") in caps:
      caps[bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬ॥")] = caps[bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ०")]
      del (caps[bstack1111l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ१")])
    if bstack1111l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ२") in caps:
      caps[bstack1111l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪ३")] = caps[bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ४")]
      del (caps[bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ५")])
  return caps
def bstack111llllll1_opy_():
  global bstack1l111l1ll_opy_
  global CONFIG
  if bstack1ll1l1lll1_opy_() <= version.parse(bstack1111l1l_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫ६")):
    if bstack1l111l1ll_opy_ != bstack1111l1l_opy_ (u"ࠬ࠭७"):
      return bstack1111l1l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ८") + bstack1l111l1ll_opy_ + bstack1111l1l_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦ९")
    return bstack1ll1ll11l_opy_
  if bstack1l111l1ll_opy_ != bstack1111l1l_opy_ (u"ࠨࠩ॰"):
    return bstack1111l1l_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦॱ") + bstack1l111l1ll_opy_ + bstack1111l1l_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦॲ")
  return bstack1l1ll1111l_opy_
def bstack111llll1l_opy_(options):
  return hasattr(options, bstack1111l1l_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬॳ"))
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
def bstack11lll1111l_opy_(options, bstack1l1lll11l_opy_):
  for bstack1l1l1lll1_opy_ in bstack1l1lll11l_opy_:
    if bstack1l1l1lll1_opy_ in [bstack1111l1l_opy_ (u"ࠬࡧࡲࡨࡵࠪॴ"), bstack1111l1l_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪॵ")]:
      continue
    if bstack1l1l1lll1_opy_ in options._experimental_options:
      options._experimental_options[bstack1l1l1lll1_opy_] = update(options._experimental_options[bstack1l1l1lll1_opy_],
                                                         bstack1l1lll11l_opy_[bstack1l1l1lll1_opy_])
    else:
      options.add_experimental_option(bstack1l1l1lll1_opy_, bstack1l1lll11l_opy_[bstack1l1l1lll1_opy_])
  if bstack1111l1l_opy_ (u"ࠧࡢࡴࡪࡷࠬॶ") in bstack1l1lll11l_opy_:
    for arg in bstack1l1lll11l_opy_[bstack1111l1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ॷ")]:
      options.add_argument(arg)
    del (bstack1l1lll11l_opy_[bstack1111l1l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॸ")])
  if bstack1111l1l_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧॹ") in bstack1l1lll11l_opy_:
    for ext in bstack1l1lll11l_opy_[bstack1111l1l_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨॺ")]:
      try:
        options.add_extension(ext)
      except OSError:
        options.add_encoded_extension(ext)
    del (bstack1l1lll11l_opy_[bstack1111l1l_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩॻ")])
def bstack11l1l111l_opy_(options, bstack111l1lll1_opy_):
  if bstack1111l1l_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬॼ") in bstack111l1lll1_opy_:
    for bstack11llll11ll_opy_ in bstack111l1lll1_opy_[bstack1111l1l_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ॽ")]:
      if bstack11llll11ll_opy_ in options._preferences:
        options._preferences[bstack11llll11ll_opy_] = update(options._preferences[bstack11llll11ll_opy_], bstack111l1lll1_opy_[bstack1111l1l_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧॾ")][bstack11llll11ll_opy_])
      else:
        options.set_preference(bstack11llll11ll_opy_, bstack111l1lll1_opy_[bstack1111l1l_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨॿ")][bstack11llll11ll_opy_])
  if bstack1111l1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨঀ") in bstack111l1lll1_opy_:
    for arg in bstack111l1lll1_opy_[bstack1111l1l_opy_ (u"ࠫࡦࡸࡧࡴࠩঁ")]:
      options.add_argument(arg)
def bstack1lll11l1ll_opy_(options, bstack1l111l1l11_opy_):
  if bstack1111l1l_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼ࠭ং") in bstack1l111l1l11_opy_:
    options.use_webview(bool(bstack1l111l1l11_opy_[bstack1111l1l_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࠧঃ")]))
  bstack11lll1111l_opy_(options, bstack1l111l1l11_opy_)
def bstack1ll1l1l111_opy_(options, bstack111l1ll1l_opy_):
  for bstack1ll1lll1l1_opy_ in bstack111l1ll1l_opy_:
    if bstack1ll1lll1l1_opy_ in [bstack1111l1l_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫ঄"), bstack1111l1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭অ")]:
      continue
    options.set_capability(bstack1ll1lll1l1_opy_, bstack111l1ll1l_opy_[bstack1ll1lll1l1_opy_])
  if bstack1111l1l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧআ") in bstack111l1ll1l_opy_:
    for arg in bstack111l1ll1l_opy_[bstack1111l1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨই")]:
      options.add_argument(arg)
  if bstack1111l1l_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨঈ") in bstack111l1ll1l_opy_:
    options.bstack1l1l1lll_opy_(bool(bstack111l1ll1l_opy_[bstack1111l1l_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩউ")]))
def bstack1lll111l1l_opy_(options, bstack1111111ll_opy_):
  for bstack11ll11l11_opy_ in bstack1111111ll_opy_:
    if bstack11ll11l11_opy_ in [bstack1111l1l_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪঊ"), bstack1111l1l_opy_ (u"ࠧࡢࡴࡪࡷࠬঋ")]:
      continue
    options._options[bstack11ll11l11_opy_] = bstack1111111ll_opy_[bstack11ll11l11_opy_]
  if bstack1111l1l_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬঌ") in bstack1111111ll_opy_:
    for bstack1l1l1lll1l_opy_ in bstack1111111ll_opy_[bstack1111l1l_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭঍")]:
      options.bstack111ll1111_opy_(
        bstack1l1l1lll1l_opy_, bstack1111111ll_opy_[bstack1111l1l_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ঎")][bstack1l1l1lll1l_opy_])
  if bstack1111l1l_opy_ (u"ࠫࡦࡸࡧࡴࠩএ") in bstack1111111ll_opy_:
    for arg in bstack1111111ll_opy_[bstack1111l1l_opy_ (u"ࠬࡧࡲࡨࡵࠪঐ")]:
      options.add_argument(arg)
def bstack11ll111111_opy_(options, caps):
  if not hasattr(options, bstack1111l1l_opy_ (u"࠭ࡋࡆ࡛ࠪ঑")):
    return
  if options.KEY == bstack1111l1l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ঒"):
    options = bstack1lll1111l1_opy_.bstack1llll1ll_opy_(bstack1ll1llll1l_opy_=options, config=CONFIG)
  if options.KEY == bstack1111l1l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ও") and options.KEY in caps:
    bstack11lll1111l_opy_(options, caps[bstack1111l1l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧঔ")])
  elif options.KEY == bstack1111l1l_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨক") and options.KEY in caps:
    bstack11l1l111l_opy_(options, caps[bstack1111l1l_opy_ (u"ࠫࡲࡵࡺ࠻ࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩখ")])
  elif options.KEY == bstack1111l1l_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭গ") and options.KEY in caps:
    bstack1ll1l1l111_opy_(options, caps[bstack1111l1l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧঘ")])
  elif options.KEY == bstack1111l1l_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨঙ") and options.KEY in caps:
    bstack1lll11l1ll_opy_(options, caps[bstack1111l1l_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩচ")])
  elif options.KEY == bstack1111l1l_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨছ") and options.KEY in caps:
    bstack1lll111l1l_opy_(options, caps[bstack1111l1l_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩজ")])
def bstack1l1l1l1l1l_opy_(caps):
  global bstack111lll111_opy_
  if isinstance(os.environ.get(bstack1111l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬঝ")), str):
    bstack111lll111_opy_ = eval(os.getenv(bstack1111l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ঞ")))
  if bstack111lll111_opy_:
    if bstack11l111l1l_opy_() < version.parse(bstack1111l1l_opy_ (u"࠭࠲࠯࠵࠱࠴ࠬট")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1111l1l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧঠ")
    if bstack1111l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ড") in caps:
      browser = caps[bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧঢ")]
    elif bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫণ") in caps:
      browser = caps[bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬত")]
    browser = str(browser).lower()
    if browser == bstack1111l1l_opy_ (u"ࠬ࡯ࡰࡩࡱࡱࡩࠬথ") or browser == bstack1111l1l_opy_ (u"࠭ࡩࡱࡣࡧࠫদ"):
      browser = bstack1111l1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧধ")
    if browser == bstack1111l1l_opy_ (u"ࠨࡵࡤࡱࡸࡻ࡮ࡨࠩন"):
      browser = bstack1111l1l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩ঩")
    if browser not in [bstack1111l1l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪপ"), bstack1111l1l_opy_ (u"ࠫࡪࡪࡧࡦࠩফ"), bstack1111l1l_opy_ (u"ࠬ࡯ࡥࠨব"), bstack1111l1l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭ভ"), bstack1111l1l_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨম")]:
      return None
    try:
      package = bstack1111l1l_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷ࠴ࡻࡾ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪয").format(browser)
      name = bstack1111l1l_opy_ (u"ࠩࡒࡴࡹ࡯࡯࡯ࡵࠪর")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack111llll1l_opy_(options):
        return None
      for bstack1lll11lll_opy_ in caps.keys():
        options.set_capability(bstack1lll11lll_opy_, caps[bstack1lll11lll_opy_])
      bstack11ll111111_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1l111lll_opy_(options, bstack1l1ll1ll1l_opy_):
  if not bstack111llll1l_opy_(options):
    return
  for bstack1lll11lll_opy_ in bstack1l1ll1ll1l_opy_.keys():
    if bstack1lll11lll_opy_ in bstack1lllll11ll_opy_:
      continue
    if bstack1lll11lll_opy_ in options._caps and type(options._caps[bstack1lll11lll_opy_]) in [dict, list]:
      options._caps[bstack1lll11lll_opy_] = update(options._caps[bstack1lll11lll_opy_], bstack1l1ll1ll1l_opy_[bstack1lll11lll_opy_])
    else:
      options.set_capability(bstack1lll11lll_opy_, bstack1l1ll1ll1l_opy_[bstack1lll11lll_opy_])
  bstack11ll111111_opy_(options, bstack1l1ll1ll1l_opy_)
  if bstack1111l1l_opy_ (u"ࠪࡱࡴࢀ࠺ࡥࡧࡥࡹ࡬࡭ࡥࡳࡃࡧࡨࡷ࡫ࡳࡴࠩ঱") in options._caps:
    if options._caps[bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩল")] and options._caps[bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ঳")].lower() != bstack1111l1l_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧ঴"):
      del options._caps[bstack1111l1l_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ࠭঵")]
def bstack11ll1l1lll_opy_(proxy_config):
  if bstack1111l1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬশ") in proxy_config:
    proxy_config[bstack1111l1l_opy_ (u"ࠩࡶࡷࡱࡖࡲࡰࡺࡼࠫষ")] = proxy_config[bstack1111l1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧস")]
    del (proxy_config[bstack1111l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨহ")])
  if bstack1111l1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ঺") in proxy_config and proxy_config[bstack1111l1l_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩ঻")].lower() != bstack1111l1l_opy_ (u"ࠧࡥ࡫ࡵࡩࡨࡺ়ࠧ"):
    proxy_config[bstack1111l1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫঽ")] = bstack1111l1l_opy_ (u"ࠩࡰࡥࡳࡻࡡ࡭ࠩা")
  if bstack1111l1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡃࡸࡸࡴࡩ࡯࡯ࡨ࡬࡫࡚ࡸ࡬ࠨি") in proxy_config:
    proxy_config[bstack1111l1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧী")] = bstack1111l1l_opy_ (u"ࠬࡶࡡࡤࠩু")
  return proxy_config
def bstack11lll111ll_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1111l1l_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬূ") in config:
    return proxy
  config[bstack1111l1l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭ৃ")] = bstack11ll1l1lll_opy_(config[bstack1111l1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧৄ")])
  if proxy == None:
    proxy = Proxy(config[bstack1111l1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨ৅")])
  return proxy
def bstack1l1l1l111_opy_(self):
  global CONFIG
  global bstack1ll1l1llll_opy_
  try:
    proxy = bstack1l11l11ll_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1111l1l_opy_ (u"ࠪ࠲ࡵࡧࡣࠨ৆")):
        proxies = bstack111ll11l1_opy_(proxy, bstack111llllll1_opy_())
        if len(proxies) > 0:
          protocol, bstack1l111l111l_opy_ = proxies.popitem()
          if bstack1111l1l_opy_ (u"ࠦ࠿࠵࠯ࠣে") in bstack1l111l111l_opy_:
            return bstack1l111l111l_opy_
          else:
            return bstack1111l1l_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨৈ") + bstack1l111l111l_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1111l1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡳࡶࡴࡾࡹࠡࡷࡵࡰࠥࡀࠠࡼࡿࠥ৉").format(str(e)))
  return bstack1ll1l1llll_opy_(self)
def bstack111llllll_opy_():
  global CONFIG
  return bstack1llll111_opy_(CONFIG) and bstack1l11l111l1_opy_() and bstack1ll1l1lll1_opy_() >= version.parse(bstack1lllll11l_opy_)
def bstack1l1lll1ll_opy_():
  global CONFIG
  return (bstack1111l1l_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ৊") in CONFIG or bstack1111l1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬো") in CONFIG) and bstack11llll111l_opy_()
def bstack1l1l1111l_opy_(config):
  bstack11llll1l_opy_ = {}
  if bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ৌ") in config:
    bstack11llll1l_opy_ = config[bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹ্ࠧ")]
  if bstack1111l1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪৎ") in config:
    bstack11llll1l_opy_ = config[bstack1111l1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ৏")]
  proxy = bstack1l11l11ll_opy_(config)
  if proxy:
    if proxy.endswith(bstack1111l1l_opy_ (u"࠭࠮ࡱࡣࡦࠫ৐")) and os.path.isfile(proxy):
      bstack11llll1l_opy_[bstack1111l1l_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪ৑")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1111l1l_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭৒")):
        proxies = bstack11l1l111ll_opy_(config, bstack111llllll1_opy_())
        if len(proxies) > 0:
          protocol, bstack1l111l111l_opy_ = proxies.popitem()
          if bstack1111l1l_opy_ (u"ࠤ࠽࠳࠴ࠨ৓") in bstack1l111l111l_opy_:
            parsed_url = urlparse(bstack1l111l111l_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1111l1l_opy_ (u"ࠥ࠾࠴࠵ࠢ৔") + bstack1l111l111l_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack11llll1l_opy_[bstack1111l1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡋࡳࡸࡺࠧ৕")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack11llll1l_opy_[bstack1111l1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡴࡸࡴࠨ৖")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack11llll1l_opy_[bstack1111l1l_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡚ࡹࡥࡳࠩৗ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack11llll1l_opy_[bstack1111l1l_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖࡡࡴࡵࠪ৘")] = str(parsed_url.password)
  return bstack11llll1l_opy_
def bstack1ll1ll111_opy_(config):
  if bstack1111l1l_opy_ (u"ࠨࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸ࠭৙") in config:
    return config[bstack1111l1l_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧ৚")]
  return {}
def bstack1l1lll1l1_opy_(caps):
  global bstack1lll1ll11_opy_
  if bstack1111l1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ৛") in caps:
    caps[bstack1111l1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬড়")][bstack1111l1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫঢ়")] = True
    if bstack1lll1ll11_opy_:
      caps[bstack1111l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ৞")][bstack1111l1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩয়")] = bstack1lll1ll11_opy_
  else:
    caps[bstack1111l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭ৠ")] = True
    if bstack1lll1ll11_opy_:
      caps[bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪৡ")] = bstack1lll1ll11_opy_
@measure(event_name=EVENTS.bstack1l1llll1l1_opy_, stage=STAGE.bstack1l1111l1ll_opy_, bstack1ll1l1ll_opy_=bstack1lllllllll_opy_)
def bstack11l1lll111_opy_():
  global CONFIG
  if not bstack111l1l11_opy_(CONFIG) or cli.is_enabled(CONFIG):
    return
  if bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧৢ") in CONFIG and bstack1lll1l11l_opy_(CONFIG[bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨৣ")]):
    if (
      bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ৤") in CONFIG
      and bstack1lll1l11l_opy_(CONFIG[bstack1111l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ৥")].get(bstack1111l1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡇ࡯࡮ࡢࡴࡼࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡸࡧࡴࡪࡱࡱࠫ০")))
    ):
      logger.debug(bstack1111l1l_opy_ (u"ࠣࡎࡲࡧࡦࡲࠠࡣ࡫ࡱࡥࡷࡿࠠ࡯ࡱࡷࠤࡸࡺࡡࡳࡶࡨࡨࠥࡧࡳࠡࡵ࡮࡭ࡵࡈࡩ࡯ࡣࡵࡽࡎࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡡࡵ࡫ࡲࡲࠥ࡯ࡳࠡࡧࡱࡥࡧࡲࡥࡥࠤ১"))
      return
    bstack11llll1l_opy_ = bstack1l1l1111l_opy_(CONFIG)
    bstack11l1l1111_opy_(CONFIG[bstack1111l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ২")], bstack11llll1l_opy_)
def bstack11l1l1111_opy_(key, bstack11llll1l_opy_):
  global bstack1ll11111_opy_
  logger.info(bstack11ll1ll1ll_opy_)
  try:
    bstack1ll11111_opy_ = Local()
    bstack11111ll11_opy_ = {bstack1111l1l_opy_ (u"ࠪ࡯ࡪࡿࠧ৩"): key}
    bstack11111ll11_opy_.update(bstack11llll1l_opy_)
    logger.debug(bstack11l111llll_opy_.format(str(bstack11111ll11_opy_)).replace(key, bstack1111l1l_opy_ (u"ࠫࡠࡘࡅࡅࡃࡆࡘࡊࡊ࡝ࠨ৪")))
    bstack1ll11111_opy_.start(**bstack11111ll11_opy_)
    if bstack1ll11111_opy_.isRunning():
      logger.info(bstack1lll1l111_opy_)
  except Exception as e:
    bstack1111ll1l1_opy_(bstack11lllllll1_opy_.format(str(e)))
def bstack1ll11ll1l_opy_():
  global bstack1ll11111_opy_
  if bstack1ll11111_opy_.isRunning():
    logger.info(bstack111l111l_opy_)
    bstack1ll11111_opy_.stop()
  bstack1ll11111_opy_ = None
def bstack1lll1111l_opy_(bstack1lll1lll11_opy_=[]):
  global CONFIG
  bstack1lll1lll_opy_ = []
  bstack1ll1lllll1_opy_ = [bstack1111l1l_opy_ (u"ࠬࡵࡳࠨ৫"), bstack1111l1l_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ৬"), bstack1111l1l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ৭"), bstack1111l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪ৮"), bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ৯"), bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫৰ")]
  try:
    for err in bstack1lll1lll11_opy_:
      bstack1ll1111ll1_opy_ = {}
      for k in bstack1ll1lllll1_opy_:
        val = CONFIG[bstack1111l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧৱ")][int(err[bstack1111l1l_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ৲")])].get(k)
        if val:
          bstack1ll1111ll1_opy_[k] = val
      if(err[bstack1111l1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ৳")] != bstack1111l1l_opy_ (u"ࠧࠨ৴")):
        bstack1ll1111ll1_opy_[bstack1111l1l_opy_ (u"ࠨࡶࡨࡷࡹࡹࠧ৵")] = {
          err[bstack1111l1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ৶")]: err[bstack1111l1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ৷")]
        }
        bstack1lll1lll_opy_.append(bstack1ll1111ll1_opy_)
  except Exception as e:
    logger.debug(bstack1111l1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡰࡴࡰࡥࡹࡺࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷ࠾ࠥ࠭৸") + str(e))
  finally:
    return bstack1lll1lll_opy_
def bstack1l1ll11l11_opy_(file_name):
  bstack1llllll1l1_opy_ = []
  try:
    bstack1llll11ll1_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1llll11ll1_opy_):
      with open(bstack1llll11ll1_opy_) as f:
        bstack1111ll1ll_opy_ = json.load(f)
        bstack1llllll1l1_opy_ = bstack1111ll1ll_opy_
      os.remove(bstack1llll11ll1_opy_)
    return bstack1llllll1l1_opy_
  except Exception as e:
    logger.debug(bstack1111l1l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧ࡫ࡱࡨ࡮ࡴࡧࠡࡧࡵࡶࡴࡸࠠ࡭࡫ࡶࡸ࠿ࠦࠧ৹") + str(e))
    return bstack1llllll1l1_opy_
def bstack1l111ll111_opy_():
  try:
      from bstack_utils.constants import bstack1ll1ll1ll_opy_, EVENTS
      from bstack_utils.helper import bstack1ll111l111_opy_, get_host_info, bstack1l1ll11l1_opy_
      from datetime import datetime
      from filelock import FileLock
      bstack1llll11l_opy_ = os.path.join(os.getcwd(), bstack1111l1l_opy_ (u"࠭࡬ࡰࡩࠪ৺"), bstack1111l1l_opy_ (u"ࠧ࡬ࡧࡼ࠱ࡲ࡫ࡴࡳ࡫ࡦࡷ࠳ࡰࡳࡰࡰࠪ৻"))
      lock = FileLock(bstack1llll11l_opy_+bstack1111l1l_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢৼ"))
      def bstack111lll1l_opy_():
          try:
              with lock:
                  with open(bstack1llll11l_opy_, bstack1111l1l_opy_ (u"ࠤࡵࠦ৽"), encoding=bstack1111l1l_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤ৾")) as file:
                      data = json.load(file)
                      config = {
                          bstack1111l1l_opy_ (u"ࠦ࡭࡫ࡡࡥࡧࡵࡷࠧ৿"): {
                              bstack1111l1l_opy_ (u"ࠧࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠦ਀"): bstack1111l1l_opy_ (u"ࠨࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠤਁ"),
                          }
                      }
                      bstack11lllll1_opy_ = datetime.utcnow()
                      bstack1ll111ll1l_opy_ = bstack11lllll1_opy_.strftime(bstack1111l1l_opy_ (u"࡛ࠢࠦ࠰ࠩࡲ࠳ࠥࡥࡖࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࠲ࠪ࡬ࠠࡖࡖࡆࠦਂ"))
                      bstack1111ll11l_opy_ = os.environ.get(bstack1111l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ਃ")) if os.environ.get(bstack1111l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ਄")) else bstack1l1ll11l1_opy_.get_property(bstack1111l1l_opy_ (u"ࠥࡷࡩࡱࡒࡶࡰࡌࡨࠧਅ"))
                      payload = {
                          bstack1111l1l_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠣਆ"): bstack1111l1l_opy_ (u"ࠧࡹࡤ࡬ࡡࡨࡺࡪࡴࡴࡴࠤਇ"),
                          bstack1111l1l_opy_ (u"ࠨࡤࡢࡶࡤࠦਈ"): {
                              bstack1111l1l_opy_ (u"ࠢࡵࡧࡶࡸ࡭ࡻࡢࡠࡷࡸ࡭ࡩࠨਉ"): bstack1111ll11l_opy_,
                              bstack1111l1l_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡥࡡࡧࡥࡾࠨਊ"): bstack1ll111ll1l_opy_,
                              bstack1111l1l_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡰࡤࡱࡪࠨ਋"): bstack1111l1l_opy_ (u"ࠥࡗࡉࡑࡆࡦࡣࡷࡹࡷ࡫ࡐࡦࡴࡩࡳࡷࡳࡡ࡯ࡥࡨࠦ਌"),
                              bstack1111l1l_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢ࡮ࡸࡵ࡮ࠣ਍"): {
                                  bstack1111l1l_opy_ (u"ࠧࡳࡥࡢࡵࡸࡶࡪࡹࠢ਎"): data,
                                  bstack1111l1l_opy_ (u"ࠨࡳࡥ࡭ࡕࡹࡳࡏࡤࠣਏ"): bstack1l1ll11l1_opy_.get_property(bstack1111l1l_opy_ (u"ࠢࡴࡦ࡮ࡖࡺࡴࡉࡥࠤਐ"))
                              },
                              bstack1111l1l_opy_ (u"ࠣࡷࡶࡩࡷࡥࡤࡢࡶࡤࠦ਑"): bstack1l1ll11l1_opy_.get_property(bstack1111l1l_opy_ (u"ࠤࡸࡷࡪࡸࡎࡢ࡯ࡨࠦ਒")),
                              bstack1111l1l_opy_ (u"ࠥ࡬ࡴࡹࡴࡠ࡫ࡱࡪࡴࠨਓ"): get_host_info()
                          }
                      }
                      bstack1lll1ll1l_opy_ = bstack1l11lll111_opy_(cli.config, [bstack1111l1l_opy_ (u"ࠦࡦࡶࡩࡴࠤਔ"), bstack1111l1l_opy_ (u"ࠧ࡫ࡤࡴࡋࡱࡷࡹࡸࡵ࡮ࡧࡱࡸࡦࡺࡩࡰࡰࠥਕ"), bstack1111l1l_opy_ (u"ࠨࡡࡱ࡫ࠥਖ")], bstack1ll1ll1ll_opy_)
                      response = bstack1ll111l111_opy_(bstack1111l1l_opy_ (u"ࠢࡑࡑࡖࡘࠧਗ"), bstack1lll1ll1l_opy_, payload, config)
                      if(response.status_code >= 200 and response.status_code < 300):
                          logger.debug(bstack1111l1l_opy_ (u"ࠣࡆࡤࡸࡦࠦࡳࡦࡰࡷࠤࡸࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻࠣࡸࡴࠦࡻࡾࠢࡺ࡭ࡹ࡮ࠠࡥࡣࡷࡥࠥࢁࡽࠣਘ").format(bstack1ll1ll1ll_opy_, payload))
                      else:
                          logger.debug(bstack1111l1l_opy_ (u"ࠤࡕࡩࡶࡻࡥࡴࡶࠣࡪࡦ࡯࡬ࡦࡦࠣࡪࡴࡸࠠࡼࡿࠣࡻ࡮ࡺࡨࠡࡦࡤࡸࡦࠦࡻࡾࠤਙ").format(bstack1ll1ll1ll_opy_, payload))
          except Exception as e:
              logger.debug(bstack1111l1l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡰࡧࠤࡰ࡫ࡹࠡ࡯ࡨࡸࡷ࡯ࡣࡴࠢࡧࡥࡹࡧࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵࠤࢀࢃࠢਚ").format(e))
      bstack111lll1l_opy_()
      bstack1lll11111_opy_(bstack1llll11l_opy_, logger)
  except:
    pass
def bstack11l11l111_opy_():
  global bstack1ll1l11l1l_opy_
  global bstack1l11l11l1_opy_
  global bstack11l1lllll_opy_
  global bstack1lllll11_opy_
  global bstack1llll11111_opy_
  global bstack1lll1l1l1l_opy_
  global CONFIG
  bstack1l1lllllll_opy_ = os.environ.get(bstack1111l1l_opy_ (u"ࠫࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ࡟ࡖࡕࡈࡈࠬਛ"))
  if bstack1l1lllllll_opy_ in [bstack1111l1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫਜ"), bstack1111l1l_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬਝ")]:
    bstack1ll11111l_opy_()
  percy.shutdown()
  if bstack1ll1l11l1l_opy_:
    logger.warning(bstack11l1l11ll1_opy_.format(str(bstack1ll1l11l1l_opy_)))
  else:
    try:
      bstack1llll11l1_opy_ = bstack1l1111lll1_opy_(bstack1111l1l_opy_ (u"ࠧ࠯ࡤࡶࡸࡦࡩ࡫࠮ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭ਞ"), logger)
      if bstack1llll11l1_opy_.get(bstack1111l1l_opy_ (u"ࠨࡰࡸࡨ࡬࡫࡟࡭ࡱࡦࡥࡱ࠭ਟ")) and bstack1llll11l1_opy_.get(bstack1111l1l_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧਠ")).get(bstack1111l1l_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬਡ")):
        logger.warning(bstack11l1l11ll1_opy_.format(str(bstack1llll11l1_opy_[bstack1111l1l_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩਢ")][bstack1111l1l_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧਣ")])))
    except Exception as e:
      logger.error(e)
  if cli.is_running():
    bstack11lllll1ll_opy_.invoke(bstack1l111l1111_opy_.bstack1l11111ll1_opy_)
  logger.info(bstack111ll111l_opy_)
  global bstack1ll11111_opy_
  if bstack1ll11111_opy_:
    bstack1ll11ll1l_opy_()
  try:
    with bstack1ll11l1l11_opy_:
      bstack11llll1l11_opy_ = bstack1l11l11l1_opy_.copy()
    for driver in bstack11llll1l11_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack111lll11l_opy_)
  if bstack1lll1l1l1l_opy_ == bstack1111l1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬਤ"):
    bstack1llll11111_opy_ = bstack1l1ll11l11_opy_(bstack1111l1l_opy_ (u"ࠧࡳࡱࡥࡳࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨਥ"))
  if bstack1lll1l1l1l_opy_ == bstack1111l1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨਦ") and len(bstack1lllll11_opy_) == 0:
    bstack1lllll11_opy_ = bstack1l1ll11l11_opy_(bstack1111l1l_opy_ (u"ࠩࡳࡻࡤࡶࡹࡵࡧࡶࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧਧ"))
    if len(bstack1lllll11_opy_) == 0:
      bstack1lllll11_opy_ = bstack1l1ll11l11_opy_(bstack1111l1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡴࡵࡶ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩਨ"))
  bstack11l11llll_opy_ = bstack1111l1l_opy_ (u"ࠫࠬ਩")
  if len(bstack11l1lllll_opy_) > 0:
    bstack11l11llll_opy_ = bstack1lll1111l_opy_(bstack11l1lllll_opy_)
  elif len(bstack1lllll11_opy_) > 0:
    bstack11l11llll_opy_ = bstack1lll1111l_opy_(bstack1lllll11_opy_)
  elif len(bstack1llll11111_opy_) > 0:
    bstack11l11llll_opy_ = bstack1lll1111l_opy_(bstack1llll11111_opy_)
  elif len(bstack1lll11llll_opy_) > 0:
    bstack11l11llll_opy_ = bstack1lll1111l_opy_(bstack1lll11llll_opy_)
  if bool(bstack11l11llll_opy_):
    bstack1ll1lll11l_opy_(bstack11l11llll_opy_)
  else:
    bstack1ll1lll11l_opy_()
  bstack1lll11111_opy_(bstack11llll111_opy_, logger)
  if bstack1l1lllllll_opy_ not in [bstack1111l1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ਪ")]:
    bstack1l111ll111_opy_()
  bstack11l1111l1_opy_.bstack11l11l1l1l_opy_(CONFIG)
  if len(bstack1llll11111_opy_) > 0:
    sys.exit(len(bstack1llll11111_opy_))
def bstack11l11ll1_opy_(bstack1l11ll1l1_opy_, frame):
  global bstack1l1ll11l1_opy_
  logger.error(bstack11ll1111l_opy_)
  bstack1l1ll11l1_opy_.bstack1ll1l111l1_opy_(bstack1111l1l_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡎࡰࠩਫ"), bstack1l11ll1l1_opy_)
  if hasattr(signal, bstack1111l1l_opy_ (u"ࠧࡔ࡫ࡪࡲࡦࡲࡳࠨਬ")):
    bstack1l1ll11l1_opy_.bstack1ll1l111l1_opy_(bstack1111l1l_opy_ (u"ࠨࡵࡧ࡯ࡐ࡯࡬࡭ࡕ࡬࡫ࡳࡧ࡬ࠨਭ"), signal.Signals(bstack1l11ll1l1_opy_).name)
  else:
    bstack1l1ll11l1_opy_.bstack1ll1l111l1_opy_(bstack1111l1l_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩਮ"), bstack1111l1l_opy_ (u"ࠪࡗࡎࡍࡕࡏࡍࡑࡓ࡜ࡔࠧਯ"))
  if cli.is_running():
    bstack11lllll1ll_opy_.invoke(bstack1l111l1111_opy_.bstack1l11111ll1_opy_)
  bstack1l1lllllll_opy_ = os.environ.get(bstack1111l1l_opy_ (u"ࠫࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ࡟ࡖࡕࡈࡈࠬਰ"))
  if bstack1l1lllllll_opy_ == bstack1111l1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ਱") and not cli.is_enabled(CONFIG):
    bstack11l1lllll1_opy_.stop(bstack1l1ll11l1_opy_.get_property(bstack1111l1l_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭ਲ")))
  bstack11l11l111_opy_()
  sys.exit(1)
def bstack1111ll1l1_opy_(err):
  logger.critical(bstack11l1l11l1l_opy_.format(str(err)))
  bstack1ll1lll11l_opy_(bstack11l1l11l1l_opy_.format(str(err)), True)
  atexit.unregister(bstack11l11l111_opy_)
  bstack1ll11111l_opy_()
  sys.exit(1)
def bstack11l1111ll1_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1ll1lll11l_opy_(message, True)
  atexit.unregister(bstack11l11l111_opy_)
  bstack1ll11111l_opy_()
  sys.exit(1)
def bstack1l11lll1l1_opy_():
  global CONFIG
  global bstack11lllll11_opy_
  global bstack1ll1lll1_opy_
  global bstack11111l11l_opy_
  CONFIG = bstack1l1l111l_opy_()
  load_dotenv(CONFIG.get(bstack1111l1l_opy_ (u"ࠧࡦࡰࡹࡊ࡮ࡲࡥࠨਲ਼")))
  bstack1lll111lll_opy_()
  bstack11l111lll_opy_()
  CONFIG = bstack1l111111l_opy_(CONFIG)
  update(CONFIG, bstack1ll1lll1_opy_)
  update(CONFIG, bstack11lllll11_opy_)
  if not cli.is_enabled(CONFIG):
    CONFIG = bstack1l11l1l11_opy_(CONFIG)
  bstack11111l11l_opy_ = bstack111l1l11_opy_(CONFIG)
  os.environ[bstack1111l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫ਴")] = bstack11111l11l_opy_.__str__().lower()
  bstack1l1ll11l1_opy_.bstack1ll1l111l1_opy_(bstack1111l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪਵ"), bstack11111l11l_opy_)
  if (bstack1111l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ਸ਼") in CONFIG and bstack1111l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ਷") in bstack11lllll11_opy_) or (
          bstack1111l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨਸ") in CONFIG and bstack1111l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩਹ") not in bstack1ll1lll1_opy_):
    if os.getenv(bstack1111l1l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫ਺")):
      CONFIG[bstack1111l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ਻")] = os.getenv(bstack1111l1l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ਼࠭"))
    else:
      if not CONFIG.get(bstack1111l1l_opy_ (u"ࠥࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠨ਽"), bstack1111l1l_opy_ (u"ࠦࠧਾ")) in bstack1ll1111l_opy_:
        bstack111l111l1_opy_()
  elif (bstack1111l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨਿ") not in CONFIG and bstack1111l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨੀ") in CONFIG) or (
          bstack1111l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪੁ") in bstack1ll1lll1_opy_ and bstack1111l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫੂ") not in bstack11lllll11_opy_):
    del (CONFIG[bstack1111l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ੃")])
  if bstack1ll1lllll_opy_(CONFIG):
    bstack1111ll1l1_opy_(bstack111l11l1_opy_)
  Config.bstack1l11llll1_opy_().bstack1ll1l111l1_opy_(bstack1111l1l_opy_ (u"ࠥࡹࡸ࡫ࡲࡏࡣࡰࡩࠧ੄"), CONFIG[bstack1111l1l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭੅")])
  bstack1ll111l1l_opy_()
  bstack11l111111l_opy_()
  if bstack111lll111_opy_ and not CONFIG.get(bstack1111l1l_opy_ (u"ࠧ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠣ੆"), bstack1111l1l_opy_ (u"ࠨࠢੇ")) in bstack1ll1111l_opy_:
    CONFIG[bstack1111l1l_opy_ (u"ࠧࡢࡲࡳࠫੈ")] = bstack1l11lll1_opy_(CONFIG)
    logger.info(bstack1lll11ll1l_opy_.format(CONFIG[bstack1111l1l_opy_ (u"ࠨࡣࡳࡴࠬ੉")]))
  if not bstack11111l11l_opy_:
    CONFIG[bstack1111l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ੊")] = [{}]
def bstack1lll1l11_opy_(config, bstack111l1lll_opy_):
  global CONFIG
  global bstack111lll111_opy_
  CONFIG = config
  bstack111lll111_opy_ = bstack111l1lll_opy_
def bstack11l111111l_opy_():
  global CONFIG
  global bstack111lll111_opy_
  if bstack1111l1l_opy_ (u"ࠪࡥࡵࡶࠧੋ") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack11l1111ll1_opy_(e, bstack11l1lll1l1_opy_)
    bstack111lll111_opy_ = True
    bstack1l1ll11l1_opy_.bstack1ll1l111l1_opy_(bstack1111l1l_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪੌ"), True)
def bstack1l11lll1_opy_(config):
  bstack1llllll1l_opy_ = bstack1111l1l_opy_ (u"੍ࠬ࠭")
  app = config[bstack1111l1l_opy_ (u"࠭ࡡࡱࡲࠪ੎")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1l1l111l11_opy_:
      if os.path.exists(app):
        bstack1llllll1l_opy_ = bstack1l1lll1l11_opy_(config, app)
      elif bstack11ll111ll_opy_(app):
        bstack1llllll1l_opy_ = app
      else:
        bstack1111ll1l1_opy_(bstack11111l1l1_opy_.format(app))
    else:
      if bstack11ll111ll_opy_(app):
        bstack1llllll1l_opy_ = app
      elif os.path.exists(app):
        bstack1llllll1l_opy_ = bstack1l1lll1l11_opy_(app)
      else:
        bstack1111ll1l1_opy_(bstack1l1l11ll11_opy_)
  else:
    if len(app) > 2:
      bstack1111ll1l1_opy_(bstack1l11111lll_opy_)
    elif len(app) == 2:
      if bstack1111l1l_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ੏") in app and bstack1111l1l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫ੐") in app:
        if os.path.exists(app[bstack1111l1l_opy_ (u"ࠩࡳࡥࡹ࡮ࠧੑ")]):
          bstack1llllll1l_opy_ = bstack1l1lll1l11_opy_(config, app[bstack1111l1l_opy_ (u"ࠪࡴࡦࡺࡨࠨ੒")], app[bstack1111l1l_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧ੓")])
        else:
          bstack1111ll1l1_opy_(bstack11111l1l1_opy_.format(app))
      else:
        bstack1111ll1l1_opy_(bstack1l11111lll_opy_)
    else:
      for key in app:
        if key in bstack11llll1l1_opy_:
          if key == bstack1111l1l_opy_ (u"ࠬࡶࡡࡵࡪࠪ੔"):
            if os.path.exists(app[key]):
              bstack1llllll1l_opy_ = bstack1l1lll1l11_opy_(config, app[key])
            else:
              bstack1111ll1l1_opy_(bstack11111l1l1_opy_.format(app))
          else:
            bstack1llllll1l_opy_ = app[key]
        else:
          bstack1111ll1l1_opy_(bstack1l111l1l1_opy_)
  return bstack1llllll1l_opy_
def bstack11ll111ll_opy_(bstack1llllll1l_opy_):
  import re
  bstack11ll11ll1_opy_ = re.compile(bstack1111l1l_opy_ (u"ࡸࠢ࡟࡝ࡤ࠱ࡿࡇ࡛࠭࠲࠰࠽ࡡࡥ࠮࡝࠯ࡠ࠮ࠩࠨ੕"))
  bstack1ll11lll_opy_ = re.compile(bstack1111l1l_opy_ (u"ࡲࠣࡠ࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯࠵࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬࠧࠦ੖"))
  if bstack1111l1l_opy_ (u"ࠨࡤࡶ࠾࠴࠵ࠧ੗") in bstack1llllll1l_opy_ or re.fullmatch(bstack11ll11ll1_opy_, bstack1llllll1l_opy_) or re.fullmatch(bstack1ll11lll_opy_, bstack1llllll1l_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack1l111l11ll_opy_, stage=STAGE.bstack1l1111l1ll_opy_, bstack1ll1l1ll_opy_=bstack1lllllllll_opy_)
def bstack1l1lll1l11_opy_(config, path, bstack11l11l1l11_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1111l1l_opy_ (u"ࠩࡵࡦࠬ੘")).read()).hexdigest()
  bstack11lll1ll11_opy_ = bstack1llllll1ll_opy_(md5_hash)
  bstack1llllll1l_opy_ = None
  if bstack11lll1ll11_opy_:
    logger.info(bstack11ll1l11l_opy_.format(bstack11lll1ll11_opy_, md5_hash))
    return bstack11lll1ll11_opy_
  bstack1ll1l1lll_opy_ = datetime.datetime.now()
  bstack11l11l1lll_opy_ = MultipartEncoder(
    fields={
      bstack1111l1l_opy_ (u"ࠪࡪ࡮ࡲࡥࠨਖ਼"): (os.path.basename(path), open(os.path.abspath(path), bstack1111l1l_opy_ (u"ࠫࡷࡨࠧਗ਼")), bstack1111l1l_opy_ (u"ࠬࡺࡥࡹࡶ࠲ࡴࡱࡧࡩ࡯ࠩਜ਼")),
      bstack1111l1l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩੜ"): bstack11l11l1l11_opy_
    }
  )
  response = requests.post(bstack1ll11l1111_opy_, data=bstack11l11l1lll_opy_,
                           headers={bstack1111l1l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭੝"): bstack11l11l1lll_opy_.content_type},
                           auth=(config[bstack1111l1l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪਫ਼")], config[bstack1111l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ੟")]))
  try:
    res = json.loads(response.text)
    bstack1llllll1l_opy_ = res[bstack1111l1l_opy_ (u"ࠪࡥࡵࡶ࡟ࡶࡴ࡯ࠫ੠")]
    logger.info(bstack11l1lll1ll_opy_.format(bstack1llllll1l_opy_))
    bstack11l11111ll_opy_(md5_hash, bstack1llllll1l_opy_)
    cli.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼ࡸࡴࡱࡵࡡࡥࡡࡤࡴࡵࠨ੡"), datetime.datetime.now() - bstack1ll1l1lll_opy_)
  except ValueError as err:
    bstack1111ll1l1_opy_(bstack1l1l11l1l_opy_.format(str(err)))
  return bstack1llllll1l_opy_
def bstack1ll111l1l_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack1l11l11111_opy_
  bstack1lllll1l1l_opy_ = 1
  bstack11l1ll111_opy_ = 1
  if bstack1111l1l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ੢") in CONFIG:
    bstack11l1ll111_opy_ = CONFIG[bstack1111l1l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭੣")]
  else:
    bstack11l1ll111_opy_ = bstack1l1111111l_opy_(framework_name, args) or 1
  if bstack1111l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ੤") in CONFIG:
    bstack1lllll1l1l_opy_ = len(CONFIG[bstack1111l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ੥")])
  bstack1l11l11111_opy_ = int(bstack11l1ll111_opy_) * int(bstack1lllll1l1l_opy_)
def bstack1l1111111l_opy_(framework_name, args):
  if framework_name == bstack11l1l1l111_opy_ and args and bstack1111l1l_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ੦") in args:
      bstack1l1l1llll_opy_ = args.index(bstack1111l1l_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨ੧"))
      return int(args[bstack1l1l1llll_opy_ + 1]) or 1
  return 1
def bstack1llllll1ll_opy_(md5_hash):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1111l1l_opy_ (u"ࠫ࡫࡯࡬ࡦ࡮ࡲࡧࡰࠦ࡮ࡰࡶࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪ࠲ࠠࡶࡵ࡬ࡲ࡬ࠦࡢࡢࡵ࡬ࡧࠥ࡬ࡩ࡭ࡧࠣࡳࡵ࡫ࡲࡢࡶ࡬ࡳࡳࡹࠧ੨"))
    bstack1ll1lll11_opy_ = os.path.join(os.path.expanduser(bstack1111l1l_opy_ (u"ࠬࢄࠧ੩")), bstack1111l1l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭੪"), bstack1111l1l_opy_ (u"ࠧࡢࡲࡳ࡙ࡵࡲ࡯ࡢࡦࡐࡈ࠺ࡎࡡࡴࡪ࠱࡮ࡸࡵ࡮ࠨ੫"))
    if os.path.exists(bstack1ll1lll11_opy_):
      try:
        bstack111lllll1l_opy_ = json.load(open(bstack1ll1lll11_opy_, bstack1111l1l_opy_ (u"ࠨࡴࡥࠫ੬")))
        if md5_hash in bstack111lllll1l_opy_:
          bstack1ll1ll111l_opy_ = bstack111lllll1l_opy_[md5_hash]
          bstack11ll11l11l_opy_ = datetime.datetime.now()
          bstack11llll1ll_opy_ = datetime.datetime.strptime(bstack1ll1ll111l_opy_[bstack1111l1l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ੭")], bstack1111l1l_opy_ (u"ࠪࠩࡩ࠵ࠥ࡮࠱ࠨ࡝ࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧ੮"))
          if (bstack11ll11l11l_opy_ - bstack11llll1ll_opy_).days > 30:
            return None
          elif version.parse(str(__version__)) > version.parse(bstack1ll1ll111l_opy_[bstack1111l1l_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ੯")]):
            return None
          return bstack1ll1ll111l_opy_[bstack1111l1l_opy_ (u"ࠬ࡯ࡤࠨੰ")]
      except Exception as e:
        logger.debug(bstack1111l1l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡸࡥࡢࡦ࡬ࡲ࡬ࠦࡍࡅ࠷ࠣ࡬ࡦࡹࡨࠡࡨ࡬ࡰࡪࡀࠠࡼࡿࠪੱ").format(str(e)))
    return None
  bstack1ll1lll11_opy_ = os.path.join(os.path.expanduser(bstack1111l1l_opy_ (u"ࠧࡿࠩੲ")), bstack1111l1l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨੳ"), bstack1111l1l_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪੴ"))
  lock_file = bstack1ll1lll11_opy_ + bstack1111l1l_opy_ (u"ࠪ࠲ࡱࡵࡣ࡬ࠩੵ")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack1ll1lll11_opy_):
        with open(bstack1ll1lll11_opy_, bstack1111l1l_opy_ (u"ࠫࡷ࠭੶")) as f:
          content = f.read().strip()
          if content:
            bstack111lllll1l_opy_ = json.loads(content)
            if md5_hash in bstack111lllll1l_opy_:
              bstack1ll1ll111l_opy_ = bstack111lllll1l_opy_[md5_hash]
              bstack11ll11l11l_opy_ = datetime.datetime.now()
              bstack11llll1ll_opy_ = datetime.datetime.strptime(bstack1ll1ll111l_opy_[bstack1111l1l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ੷")], bstack1111l1l_opy_ (u"࠭ࠥࡥ࠱ࠨࡱ࠴࡙ࠫࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪ੸"))
              if (bstack11ll11l11l_opy_ - bstack11llll1ll_opy_).days > 30:
                return None
              elif version.parse(str(__version__)) > version.parse(bstack1ll1ll111l_opy_[bstack1111l1l_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ੹")]):
                return None
              return bstack1ll1ll111l_opy_[bstack1111l1l_opy_ (u"ࠨ࡫ࡧࠫ੺")]
      return None
  except Exception as e:
    logger.debug(bstack1111l1l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡹ࡬ࡸ࡭ࠦࡦࡪ࡮ࡨࠤࡱࡵࡣ࡬࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡐࡈ࠺ࠦࡨࡢࡵ࡫࠾ࠥࢁࡽࠨ੻").format(str(e)))
    return None
def bstack11l11111ll_opy_(md5_hash, bstack1llllll1l_opy_):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1111l1l_opy_ (u"ࠪࡪ࡮ࡲࡥ࡭ࡱࡦ࡯ࠥࡴ࡯ࡵࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩ࠱ࠦࡵࡴ࡫ࡱ࡫ࠥࡨࡡࡴ࡫ࡦࠤ࡫࡯࡬ࡦࠢࡲࡴࡪࡸࡡࡵ࡫ࡲࡲࡸ࠭੼"))
    bstack1lllllll1l_opy_ = os.path.join(os.path.expanduser(bstack1111l1l_opy_ (u"ࠫࢃ࠭੽")), bstack1111l1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ੾"))
    if not os.path.exists(bstack1lllllll1l_opy_):
      os.makedirs(bstack1lllllll1l_opy_)
    bstack1ll1lll11_opy_ = os.path.join(os.path.expanduser(bstack1111l1l_opy_ (u"࠭ࡾࠨ੿")), bstack1111l1l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ઀"), bstack1111l1l_opy_ (u"ࠨࡣࡳࡴ࡚ࡶ࡬ࡰࡣࡧࡑࡉ࠻ࡈࡢࡵ࡫࠲࡯ࡹ࡯࡯ࠩઁ"))
    bstack111111111_opy_ = {
      bstack1111l1l_opy_ (u"ࠩ࡬ࡨࠬં"): bstack1llllll1l_opy_,
      bstack1111l1l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ઃ"): datetime.datetime.strftime(datetime.datetime.now(), bstack1111l1l_opy_ (u"ࠫࠪࡪ࠯ࠦ࡯࠲ࠩ࡞ࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨ઄")),
      bstack1111l1l_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪઅ"): str(__version__)
    }
    try:
      bstack111lllll1l_opy_ = {}
      if os.path.exists(bstack1ll1lll11_opy_):
        bstack111lllll1l_opy_ = json.load(open(bstack1ll1lll11_opy_, bstack1111l1l_opy_ (u"࠭ࡲࡣࠩઆ")))
      bstack111lllll1l_opy_[md5_hash] = bstack111111111_opy_
      with open(bstack1ll1lll11_opy_, bstack1111l1l_opy_ (u"ࠢࡸ࠭ࠥઇ")) as outfile:
        json.dump(bstack111lllll1l_opy_, outfile)
    except Exception as e:
      logger.debug(bstack1111l1l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡶࡲࡧࡥࡹ࡯࡮ࡨࠢࡐࡈ࠺ࠦࡨࡢࡵ࡫ࠤ࡫࡯࡬ࡦ࠼ࠣࡿࢂ࠭ઈ").format(str(e)))
    return
  bstack1lllllll1l_opy_ = os.path.join(os.path.expanduser(bstack1111l1l_opy_ (u"ࠩࢁࠫઉ")), bstack1111l1l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪઊ"))
  if not os.path.exists(bstack1lllllll1l_opy_):
    os.makedirs(bstack1lllllll1l_opy_)
  bstack1ll1lll11_opy_ = os.path.join(os.path.expanduser(bstack1111l1l_opy_ (u"ࠫࢃ࠭ઋ")), bstack1111l1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬઌ"), bstack1111l1l_opy_ (u"࠭ࡡࡱࡲࡘࡴࡱࡵࡡࡥࡏࡇ࠹ࡍࡧࡳࡩ࠰࡭ࡷࡴࡴࠧઍ"))
  lock_file = bstack1ll1lll11_opy_ + bstack1111l1l_opy_ (u"ࠧ࠯࡮ࡲࡧࡰ࠭઎")
  bstack111111111_opy_ = {
    bstack1111l1l_opy_ (u"ࠨ࡫ࡧࠫએ"): bstack1llllll1l_opy_,
    bstack1111l1l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬઐ"): datetime.datetime.strftime(datetime.datetime.now(), bstack1111l1l_opy_ (u"ࠪࠩࡩ࠵ࠥ࡮࠱ࠨ࡝ࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧઑ")),
    bstack1111l1l_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ઒"): str(__version__)
  }
  try:
    with FileLock(lock_file, timeout=10):
      bstack111lllll1l_opy_ = {}
      if os.path.exists(bstack1ll1lll11_opy_):
        with open(bstack1ll1lll11_opy_, bstack1111l1l_opy_ (u"ࠬࡸࠧઓ")) as f:
          content = f.read().strip()
          if content:
            bstack111lllll1l_opy_ = json.loads(content)
      bstack111lllll1l_opy_[md5_hash] = bstack111111111_opy_
      with open(bstack1ll1lll11_opy_, bstack1111l1l_opy_ (u"ࠨࡷࠣઔ")) as outfile:
        json.dump(bstack111lllll1l_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1111l1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡷࡪࡶ࡫ࠤ࡫࡯࡬ࡦࠢ࡯ࡳࡨࡱࡩ࡯ࡩࠣࡪࡴࡸࠠࡎࡆ࠸ࠤ࡭ࡧࡳࡩࠢࡸࡴࡩࡧࡴࡦ࠼ࠣࡿࢂ࠭ક").format(str(e)))
def bstack111l1l11l_opy_(self):
  return
def bstack1llll1l1l1_opy_(self):
  return
def bstack1l1llll111_opy_():
  global bstack11lll11lll_opy_
  bstack11lll11lll_opy_ = True
@measure(event_name=EVENTS.bstack11ll1lll1l_opy_, stage=STAGE.bstack1l1111l1ll_opy_, bstack1ll1l1ll_opy_=bstack1lllllllll_opy_)
def bstack1llll11l1l_opy_(self):
  global bstack1l111l11l1_opy_
  global bstack11111l1ll_opy_
  global bstack11lllll11l_opy_
  try:
    if bstack1111l1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨખ") in bstack1l111l11l1_opy_ and self.session_id != None and bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠩࡷࡩࡸࡺࡓࡵࡣࡷࡹࡸ࠭ગ"), bstack1111l1l_opy_ (u"ࠪࠫઘ")) != bstack1111l1l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬઙ"):
      bstack1l1l11l11l_opy_ = bstack1111l1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬચ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1111l1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭છ")
      if bstack1l1l11l11l_opy_ == bstack1111l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧજ"):
        bstack111111ll_opy_(logger)
      if self != None:
        bstack1l11111l1l_opy_(self, bstack1l1l11l11l_opy_, bstack1111l1l_opy_ (u"ࠨ࠮ࠣࠫઝ").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack1111l1l_opy_ (u"ࠩࠪઞ")
    if bstack1111l1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪટ") in bstack1l111l11l1_opy_ and getattr(threading.current_thread(), bstack1111l1l_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪઠ"), None):
      bstack11l1ll1ll1_opy_.bstack1l1l11llll_opy_(self, bstack111111ll1_opy_, logger, wait=True)
    if bstack1111l1l_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬડ") in bstack1l111l11l1_opy_:
      if not threading.currentThread().behave_test_status:
        bstack1l11111l1l_opy_(self, bstack1111l1l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨઢ"))
      bstack111lll1l1_opy_.bstack1l11l11l11_opy_(self)
  except Exception as e:
    logger.debug(bstack1111l1l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡳࡵࡣࡷࡹࡸࡀࠠࠣણ") + str(e))
  bstack11lllll11l_opy_(self)
  self.session_id = None
def bstack1lll1ll111_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack1l11l111l_opy_
    global bstack1l111l11l1_opy_
    command_executor = kwargs.get(bstack1111l1l_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠫત"), bstack1111l1l_opy_ (u"ࠩࠪથ"))
    bstack11l1l1lll1_opy_ = False
    if type(command_executor) == str and bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭દ") in command_executor:
      bstack11l1l1lll1_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧધ") in str(getattr(command_executor, bstack1111l1l_opy_ (u"ࠬࡥࡵࡳ࡮ࠪન"), bstack1111l1l_opy_ (u"࠭ࠧ઩"))):
      bstack11l1l1lll1_opy_ = True
    else:
      kwargs = bstack1lll1111l1_opy_.bstack1llll1ll_opy_(bstack1ll1llll1l_opy_=kwargs, config=CONFIG)
      return bstack1l1llll11_opy_(self, *args, **kwargs)
    if bstack11l1l1lll1_opy_:
      bstack1l1lllll_opy_ = bstack1l11ll1l1l_opy_.bstack1l1llll1_opy_(CONFIG, bstack1l111l11l1_opy_)
      if kwargs.get(bstack1111l1l_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨપ")):
        kwargs[bstack1111l1l_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩફ")] = bstack1l11l111l_opy_(kwargs[bstack1111l1l_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪબ")], bstack1l111l11l1_opy_, CONFIG, bstack1l1lllll_opy_)
      elif kwargs.get(bstack1111l1l_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪભ")):
        kwargs[bstack1111l1l_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫમ")] = bstack1l11l111l_opy_(kwargs[bstack1111l1l_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬય")], bstack1l111l11l1_opy_, CONFIG, bstack1l1lllll_opy_)
  except Exception as e:
    logger.error(bstack1111l1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡦࡰࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡔࡆࡎࠤࡨࡧࡰࡴ࠼ࠣࡿࢂࠨર").format(str(e)))
  return bstack1l1llll11_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack11111lll1_opy_, stage=STAGE.bstack1l1111l1ll_opy_, bstack1ll1l1ll_opy_=bstack1lllllllll_opy_)
def bstack1l11l1l111_opy_(self, command_executor=bstack1111l1l_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯࠲࠴࠺࠲࠵࠴࠰࠯࠳࠽࠸࠹࠺࠴ࠣ઱"), *args, **kwargs):
  global bstack11111l1ll_opy_
  global bstack1l11l11l1_opy_
  bstack11l1l11lll_opy_ = bstack1lll1ll111_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack1ll11lll1_opy_.on():
    return bstack11l1l11lll_opy_
  try:
    logger.debug(bstack1111l1l_opy_ (u"ࠨࡅࡲࡱࡲࡧ࡮ࡥࠢࡈࡼࡪࡩࡵࡵࡱࡵࠤࡼ࡮ࡥ࡯ࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥ࡯ࡳࠡࡨࡤࡰࡸ࡫ࠠ࠮ࠢࡾࢁࠬલ").format(str(command_executor)))
    logger.debug(bstack1111l1l_opy_ (u"ࠩࡋࡹࡧࠦࡕࡓࡎࠣ࡭ࡸࠦ࠭ࠡࡽࢀࠫળ").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭઴") in command_executor._url:
      bstack1l1ll11l1_opy_.bstack1ll1l111l1_opy_(bstack1111l1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬવ"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨશ") in command_executor):
    bstack1l1ll11l1_opy_.bstack1ll1l111l1_opy_(bstack1111l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧષ"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1llll1l1_opy_ = getattr(threading.current_thread(), bstack1111l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡔࡦࡵࡷࡑࡪࡺࡡࠨસ"), None)
  bstack11l1l1ll11_opy_ = {}
  if self.capabilities is not None:
    bstack11l1l1ll11_opy_[bstack1111l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧહ")] = self.capabilities.get(bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ઺"))
    bstack11l1l1ll11_opy_[bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ઻")] = self.capabilities.get(bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲ઼ࠬ"))
    bstack11l1l1ll11_opy_[bstack1111l1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡤࡵࡰࡵ࡫ࡲࡲࡸ࠭ઽ")] = self.capabilities.get(bstack1111l1l_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫા"))
  if CONFIG.get(bstack1111l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧિ"), False) and bstack1lll1111l1_opy_.bstack11l1l11l11_opy_(bstack11l1l1ll11_opy_):
    threading.current_thread().a11yPlatform = True
  if bstack1111l1l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨી") in bstack1l111l11l1_opy_ or bstack1111l1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨુ") in bstack1l111l11l1_opy_:
    bstack11l1lllll1_opy_.bstack111lll1ll_opy_(self)
  if bstack1111l1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪૂ") in bstack1l111l11l1_opy_ and bstack1llll1l1_opy_ and bstack1llll1l1_opy_.get(bstack1111l1l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫૃ"), bstack1111l1l_opy_ (u"ࠬ࠭ૄ")) == bstack1111l1l_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧૅ"):
    bstack11l1lllll1_opy_.bstack111lll1ll_opy_(self)
  bstack11111l1ll_opy_ = self.session_id
  with bstack1ll11l1l11_opy_:
    bstack1l11l11l1_opy_.append(self)
  return bstack11l1l11lll_opy_
def bstack1111111l1_opy_(args):
  return bstack1111l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲࠨ૆") in str(args)
def bstack1l1lll11ll_opy_(self, driver_command, *args, **kwargs):
  global bstack1l1lllll1l_opy_
  global bstack11111l111_opy_
  bstack11l1111111_opy_ = bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬે"), None) and bstack1l11l1lll_opy_(
          threading.current_thread(), bstack1111l1l_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨૈ"), None)
  bstack1l1ll1lll_opy_ = bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪૉ"), None) and bstack1l11l1lll_opy_(
          threading.current_thread(), bstack1111l1l_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭૊"), None)
  bstack1ll1l111l_opy_ = getattr(self, bstack1111l1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬો"), None) != None and getattr(self, bstack1111l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭ૌ"), None) == True
  if not bstack11111l111_opy_ and bstack1111l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ્ࠧ") in CONFIG and CONFIG[bstack1111l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ૎")] == True and bstack1ll1ll1ll1_opy_.bstack1ll111l11_opy_(driver_command) and (bstack1ll1l111l_opy_ or bstack11l1111111_opy_ or bstack1l1ll1lll_opy_) and not bstack1111111l1_opy_(args):
    try:
      bstack11111l111_opy_ = True
      logger.debug(bstack1111l1l_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡽࢀࠫ૏").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack1111l1l_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡦࡴࡩࡳࡷࡳࠠࡴࡥࡤࡲࠥࢁࡽࠨૐ").format(str(err)))
    bstack11111l111_opy_ = False
  response = bstack1l1lllll1l_opy_(self, driver_command, *args, **kwargs)
  if (bstack1111l1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ૑") in str(bstack1l111l11l1_opy_).lower() or bstack1111l1l_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ૒") in str(bstack1l111l11l1_opy_).lower()) and bstack1ll11lll1_opy_.on():
    try:
      if driver_command == bstack1111l1l_opy_ (u"࠭ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪ૓"):
        bstack11l1lllll1_opy_.bstack1111l1ll_opy_({
            bstack1111l1l_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭૔"): response[bstack1111l1l_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧ૕")],
            bstack1111l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ૖"): bstack11l1lllll1_opy_.current_test_uuid() if bstack11l1lllll1_opy_.current_test_uuid() else bstack1ll11lll1_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
@measure(event_name=EVENTS.bstack1l1l11ll_opy_, stage=STAGE.bstack1l1111l1ll_opy_, bstack1ll1l1ll_opy_=bstack1lllllllll_opy_)
def bstack11l1lll1_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack11111l1ll_opy_
  global bstack1l1ll11lll_opy_
  global bstack1lllllllll_opy_
  global bstack11llll1lll_opy_
  global bstack11l11l11ll_opy_
  global bstack1l111l11l1_opy_
  global bstack1l1llll11_opy_
  global bstack1l11l11l1_opy_
  global bstack1l1ll1lll1_opy_
  global bstack111111ll1_opy_
  if os.getenv(bstack1111l1l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ૗")) is not None and bstack1lll1111l1_opy_.bstack1llllllll1_opy_(CONFIG) is None:
    CONFIG[bstack1111l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ૘")] = True
  CONFIG[bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ૙")] = str(bstack1l111l11l1_opy_) + str(__version__)
  bstack1lll1l1l1_opy_ = os.environ[bstack1111l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ૚")]
  bstack1l1lllll_opy_ = bstack1l11ll1l1l_opy_.bstack1l1llll1_opy_(CONFIG, bstack1l111l11l1_opy_)
  CONFIG[bstack1111l1l_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ૛")] = bstack1lll1l1l1_opy_
  CONFIG[bstack1111l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ૜")] = bstack1l1lllll_opy_
  if CONFIG.get(bstack1111l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ૝"),bstack1111l1l_opy_ (u"ࠪࠫ૞")) and bstack1111l1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ૟") in bstack1l111l11l1_opy_:
    CONFIG[bstack1111l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬૠ")].pop(bstack1111l1l_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫૡ"), None)
    CONFIG[bstack1111l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧૢ")].pop(bstack1111l1l_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ૣ"), None)
  command_executor = bstack111llllll1_opy_()
  logger.debug(bstack1l1111ll11_opy_.format(command_executor))
  proxy = bstack11lll111ll_opy_(CONFIG, proxy)
  bstack11lll11l_opy_ = 0 if bstack1l1ll11lll_opy_ < 0 else bstack1l1ll11lll_opy_
  try:
    if bstack11llll1lll_opy_ is True:
      bstack11lll11l_opy_ = int(multiprocessing.current_process().name)
    elif bstack11l11l11ll_opy_ is True:
      bstack11lll11l_opy_ = int(threading.current_thread().name)
  except:
    bstack11lll11l_opy_ = 0
  bstack1l1ll1ll1l_opy_ = bstack1lll1111_opy_(CONFIG, bstack11lll11l_opy_)
  logger.debug(bstack1ll1ll1l11_opy_.format(str(bstack1l1ll1ll1l_opy_)))
  if bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭૤") in CONFIG and bstack1lll1l11l_opy_(CONFIG[bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ૥")]):
    bstack1l1lll1l1_opy_(bstack1l1ll1ll1l_opy_)
  if bstack1lll1111l1_opy_.bstack1llll1l1l_opy_(CONFIG, bstack11lll11l_opy_) and bstack1lll1111l1_opy_.bstack1l1lll1lll_opy_(bstack1l1ll1ll1l_opy_, options, desired_capabilities, CONFIG):
    threading.current_thread().a11yPlatform = True
    if (cli.accessibility is None or not cli.accessibility.is_enabled()):
      bstack1lll1111l1_opy_.set_capabilities(bstack1l1ll1ll1l_opy_, CONFIG)
  if desired_capabilities:
    bstack11ll1l1l11_opy_ = bstack1l111111l_opy_(desired_capabilities)
    bstack11ll1l1l11_opy_[bstack1111l1l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫ૦")] = bstack11l1l1l11_opy_(CONFIG)
    bstack1llll11ll_opy_ = bstack1lll1111_opy_(bstack11ll1l1l11_opy_)
    if bstack1llll11ll_opy_:
      bstack1l1ll1ll1l_opy_ = update(bstack1llll11ll_opy_, bstack1l1ll1ll1l_opy_)
    desired_capabilities = None
  if options:
    bstack1l111lll_opy_(options, bstack1l1ll1ll1l_opy_)
  if not options:
    options = bstack1l1l1l1l1l_opy_(bstack1l1ll1ll1l_opy_)
  bstack111111ll1_opy_ = CONFIG.get(bstack1111l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ૧"))[bstack11lll11l_opy_]
  if proxy and bstack1ll1l1lll1_opy_() >= version.parse(bstack1111l1l_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭૨")):
    options.proxy(proxy)
  if options and bstack1ll1l1lll1_opy_() >= version.parse(bstack1111l1l_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭૩")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1ll1l1lll1_opy_() < version.parse(bstack1111l1l_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ૪")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1l1ll1ll1l_opy_)
  logger.info(bstack1ll111l1_opy_)
  bstack1lllll1ll_opy_.end(EVENTS.bstack1l111l111_opy_.value, EVENTS.bstack1l111l111_opy_.value + bstack1111l1l_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ૫"), EVENTS.bstack1l111l111_opy_.value + bstack1111l1l_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ૬"), status=True, failure=None, test_name=bstack1lllllllll_opy_)
  if bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡶࡲࡰࡨ࡬ࡰࡪ࠭૭") in kwargs:
    del kwargs[bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡰࡳࡱࡩ࡭ࡱ࡫ࠧ૮")]
  try:
    if bstack1ll1l1lll1_opy_() >= version.parse(bstack1111l1l_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭૯")):
      bstack1l1llll11_opy_(self, command_executor=command_executor,
                options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
    elif bstack1ll1l1lll1_opy_() >= version.parse(bstack1111l1l_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭૰")):
      bstack1l1llll11_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities, options=options,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1ll1l1lll1_opy_() >= version.parse(bstack1111l1l_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨ૱")):
      bstack1l1llll11_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    else:
      bstack1l1llll11_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive)
  except Exception as bstack11l1111l_opy_:
    logger.error(bstack11ll1lll1_opy_.format(bstack1111l1l_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠨ૲"), str(bstack11l1111l_opy_)))
    raise bstack11l1111l_opy_
  if bstack1lll1111l1_opy_.bstack1llll1l1l_opy_(CONFIG, bstack11lll11l_opy_) and bstack1lll1111l1_opy_.bstack1l1lll1lll_opy_(self.caps, options, desired_capabilities):
    if CONFIG[bstack1111l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬ૳")][bstack1111l1l_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪ૴")] == True:
      threading.current_thread().appA11yPlatform = True
      if cli.accessibility is None or not cli.accessibility.is_enabled():
        bstack1lll1111l1_opy_.set_capabilities(bstack1l1ll1ll1l_opy_, CONFIG)
  try:
    bstack1lllll1ll1_opy_ = bstack1111l1l_opy_ (u"ࠬ࠭૵")
    if bstack1ll1l1lll1_opy_() >= version.parse(bstack1111l1l_opy_ (u"࠭࠴࠯࠲࠱࠴ࡧ࠷ࠧ૶")):
      if self.caps is not None:
        bstack1lllll1ll1_opy_ = self.caps.get(bstack1111l1l_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢ૷"))
    else:
      if self.capabilities is not None:
        bstack1lllll1ll1_opy_ = self.capabilities.get(bstack1111l1l_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣ૸"))
    if bstack1lllll1ll1_opy_:
      bstack11lllll1l1_opy_(bstack1lllll1ll1_opy_)
      if bstack1ll1l1lll1_opy_() <= version.parse(bstack1111l1l_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩૹ")):
        self.command_executor._url = bstack1111l1l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦૺ") + bstack1l111l1ll_opy_ + bstack1111l1l_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣૻ")
      else:
        self.command_executor._url = bstack1111l1l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢૼ") + bstack1lllll1ll1_opy_ + bstack1111l1l_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢ૽")
      logger.debug(bstack1lllll1l11_opy_.format(bstack1lllll1ll1_opy_))
    else:
      logger.debug(bstack1l1l111l1l_opy_.format(bstack1111l1l_opy_ (u"ࠢࡐࡲࡷ࡭ࡲࡧ࡬ࠡࡊࡸࡦࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠣ૾")))
  except Exception as e:
    logger.debug(bstack1l1l111l1l_opy_.format(e))
  if bstack1111l1l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ૿") in bstack1l111l11l1_opy_:
    bstack1l1l1l1ll1_opy_(bstack1l1ll11lll_opy_, bstack1l1ll1lll1_opy_)
  bstack11111l1ll_opy_ = self.session_id
  if bstack1111l1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ଀") in bstack1l111l11l1_opy_ or bstack1111l1l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪଁ") in bstack1l111l11l1_opy_ or bstack1111l1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪଂ") in bstack1l111l11l1_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack1llll1l1_opy_ = getattr(threading.current_thread(), bstack1111l1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࡙࡫ࡳࡵࡏࡨࡸࡦ࠭ଃ"), None)
  if bstack1111l1l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭଄") in bstack1l111l11l1_opy_ or bstack1111l1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ଅ") in bstack1l111l11l1_opy_:
    bstack11l1lllll1_opy_.bstack111lll1ll_opy_(self)
  if bstack1111l1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨଆ") in bstack1l111l11l1_opy_ and bstack1llll1l1_opy_ and bstack1llll1l1_opy_.get(bstack1111l1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩଇ"), bstack1111l1l_opy_ (u"ࠪࠫଈ")) == bstack1111l1l_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬଉ"):
    bstack11l1lllll1_opy_.bstack111lll1ll_opy_(self)
  with bstack1ll11l1l11_opy_:
    bstack1l11l11l1_opy_.append(self)
  if bstack1111l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨଊ") in CONFIG and bstack1111l1l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫଋ") in CONFIG[bstack1111l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଌ")][bstack11lll11l_opy_]:
    bstack1lllllllll_opy_ = CONFIG[bstack1111l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ଍")][bstack11lll11l_opy_][bstack1111l1l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ଎")]
  logger.debug(bstack1l1l1l11l_opy_.format(bstack11111l1ll_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    from browserstack_sdk.__init__ import bstack11l11l1111_opy_
    def bstack1l11l1l1l_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack11ll11l1l_opy_
      if(bstack1111l1l_opy_ (u"ࠥ࡭ࡳࡪࡥࡹ࠰࡭ࡷࠧଏ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1111l1l_opy_ (u"ࠫࢃ࠭ଐ")), bstack1111l1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ଑"), bstack1111l1l_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨ଒")), bstack1111l1l_opy_ (u"ࠧࡸࠩଓ")) as fp:
          fp.write(bstack1111l1l_opy_ (u"ࠣࠤଔ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1111l1l_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸࡠࡤࡶࡸࡦࡩ࡫࠯࡬ࡶࠦକ")))):
          with open(args[1], bstack1111l1l_opy_ (u"ࠪࡶࠬଖ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1111l1l_opy_ (u"ࠫࡦࡹࡹ࡯ࡥࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࡥ࡮ࡦࡹࡓࡥ࡬࡫ࠨࡤࡱࡱࡸࡪࡾࡴ࠭ࠢࡳࡥ࡬࡫ࠠ࠾ࠢࡹࡳ࡮ࡪࠠ࠱ࠫࠪଗ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1ll11llll_opy_)
            if bstack1111l1l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩଘ") in CONFIG and str(CONFIG[bstack1111l1l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪଙ")]).lower() != bstack1111l1l_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ଚ"):
                bstack1lll11l11l_opy_ = bstack11l11l1111_opy_()
                bstack1ll1l1ll1_opy_ = bstack1111l1l_opy_ (u"ࠨࠩࠪࠎ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠊࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡰࡢࡶ࡫ࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳࡞࠽ࠍࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠴ࡡࡀࠐࡣࡰࡰࡶࡸࠥࡶ࡟ࡪࡰࡧࡩࡽࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠴ࡠ࠿ࠏࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡹ࡬ࡪࡥࡨࠬ࠵࠲ࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࠬ࠿ࠏࡩ࡯࡯ࡵࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬ࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ࠭ࡀࠐࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴࡬ࡢࡷࡱࡧ࡭ࠦ࠽ࠡࡣࡶࡽࡳࡩࠠࠩ࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁࡻࠋࠢࠣࡰࡪࡺࠠࡤࡣࡳࡷࡀࠐࠠࠡࡶࡵࡽࠥࢁࡻࠋࠢࠣࠤࠥࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࠼ࠌࠣࠤࢂࢃࠠࡤࡣࡷࡧ࡭ࠦࠨࡦࡺࠬࠤࢀࢁࠊࠡࠢࠣࠤࡨࡵ࡮ࡴࡱ࡯ࡩ࠳࡫ࡲࡳࡱࡵࠬࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࡀࠢ࠭ࠢࡨࡼ࠮ࡁࠊࠡࠢࢀࢁࠏࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠨࡼࡽࠍࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥ࠭ࡻࡤࡦࡳ࡙ࡷࡲࡽࠨࠢ࠮ࠤࡪࡴࡣࡰࡦࡨ࡙ࡗࡏࡃࡰ࡯ࡳࡳࡳ࡫࡮ࡵࠪࡍࡗࡔࡔ࠮ࡴࡶࡵ࡭ࡳ࡭ࡩࡧࡻࠫࡧࡦࡶࡳࠪࠫ࠯ࠎࠥࠦࠠࠡ࠰࠱࠲ࡱࡧࡵ࡯ࡥ࡫ࡓࡵࡺࡩࡰࡰࡶࠎࠥࠦࡽࡾࠫ࠾ࠎࢂࢃ࠻ࠋ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࠎࠬ࠭ࠧଛ").format(bstack1lll11l11l_opy_=bstack1lll11l11l_opy_)
            lines.insert(1, bstack1ll1l1ll1_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1111l1l_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸࡠࡤࡶࡸࡦࡩ࡫࠯࡬ࡶࠦଜ")), bstack1111l1l_opy_ (u"ࠪࡻࠬଝ")) as bstack1ll1llllll_opy_:
              bstack1ll1llllll_opy_.writelines(lines)
        CONFIG[bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ଞ")] = str(bstack1l111l11l1_opy_) + str(__version__)
        bstack1lll1l1l1_opy_ = os.environ[bstack1111l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪଟ")]
        bstack1l1lllll_opy_ = bstack1l11ll1l1l_opy_.bstack1l1llll1_opy_(CONFIG, bstack1l111l11l1_opy_)
        CONFIG[bstack1111l1l_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩଠ")] = bstack1lll1l1l1_opy_
        CONFIG[bstack1111l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩଡ")] = bstack1l1lllll_opy_
        bstack11lll11l_opy_ = 0 if bstack1l1ll11lll_opy_ < 0 else bstack1l1ll11lll_opy_
        try:
          if bstack11llll1lll_opy_ is True:
            bstack11lll11l_opy_ = int(multiprocessing.current_process().name)
          elif bstack11l11l11ll_opy_ is True:
            bstack11lll11l_opy_ = int(threading.current_thread().name)
        except:
          bstack11lll11l_opy_ = 0
        CONFIG[bstack1111l1l_opy_ (u"ࠣࡷࡶࡩ࡜࠹ࡃࠣଢ")] = False
        CONFIG[bstack1111l1l_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣଣ")] = True
        bstack1l1ll1ll1l_opy_ = bstack1lll1111_opy_(CONFIG, bstack11lll11l_opy_)
        logger.debug(bstack1ll1ll1l11_opy_.format(str(bstack1l1ll1ll1l_opy_)))
        if CONFIG.get(bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧତ")):
          bstack1l1lll1l1_opy_(bstack1l1ll1ll1l_opy_)
        if bstack1111l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଥ") in CONFIG and bstack1111l1l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪଦ") in CONFIG[bstack1111l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଧ")][bstack11lll11l_opy_]:
          bstack1lllllllll_opy_ = CONFIG[bstack1111l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪନ")][bstack11lll11l_opy_][bstack1111l1l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭଩")]
        args.append(os.path.join(os.path.expanduser(bstack1111l1l_opy_ (u"ࠩࢁࠫପ")), bstack1111l1l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪଫ"), bstack1111l1l_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭ବ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1l1ll1ll1l_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1111l1l_opy_ (u"ࠧ࡯࡮ࡥࡧࡻࡣࡧࡹࡴࡢࡥ࡮࠲࡯ࡹࠢଭ"))
      bstack11ll11l1l_opy_ = True
      return bstack1lll1llll1_opy_(self, args, bufsize=bufsize, executable=executable,
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
  def bstack1l1ll1l11_opy_(self,
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
    global bstack1l1ll11lll_opy_
    global bstack1lllllllll_opy_
    global bstack11llll1lll_opy_
    global bstack11l11l11ll_opy_
    global bstack1l111l11l1_opy_
    CONFIG[bstack1111l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨମ")] = str(bstack1l111l11l1_opy_) + str(__version__)
    bstack1lll1l1l1_opy_ = os.environ[bstack1111l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬଯ")]
    bstack1l1lllll_opy_ = bstack1l11ll1l1l_opy_.bstack1l1llll1_opy_(CONFIG, bstack1l111l11l1_opy_)
    CONFIG[bstack1111l1l_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫର")] = bstack1lll1l1l1_opy_
    CONFIG[bstack1111l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ଱")] = bstack1l1lllll_opy_
    bstack11lll11l_opy_ = 0 if bstack1l1ll11lll_opy_ < 0 else bstack1l1ll11lll_opy_
    try:
      if bstack11llll1lll_opy_ is True:
        bstack11lll11l_opy_ = int(multiprocessing.current_process().name)
      elif bstack11l11l11ll_opy_ is True:
        bstack11lll11l_opy_ = int(threading.current_thread().name)
    except:
      bstack11lll11l_opy_ = 0
    CONFIG[bstack1111l1l_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤଲ")] = True
    bstack1l1ll1ll1l_opy_ = bstack1lll1111_opy_(CONFIG, bstack11lll11l_opy_)
    logger.debug(bstack1ll1ll1l11_opy_.format(str(bstack1l1ll1ll1l_opy_)))
    if CONFIG.get(bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨଳ")):
      bstack1l1lll1l1_opy_(bstack1l1ll1ll1l_opy_)
    if bstack1111l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ଴") in CONFIG and bstack1111l1l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫଵ") in CONFIG[bstack1111l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଶ")][bstack11lll11l_opy_]:
      bstack1lllllllll_opy_ = CONFIG[bstack1111l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫଷ")][bstack11lll11l_opy_][bstack1111l1l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧସ")]
    import urllib
    import json
    if bstack1111l1l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧହ") in CONFIG and str(CONFIG[bstack1111l1l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ଺")]).lower() != bstack1111l1l_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ଻"):
        bstack11l11lll1l_opy_ = bstack11l11l1111_opy_()
        bstack1lll11l11l_opy_ = bstack11l11lll1l_opy_ + urllib.parse.quote(json.dumps(bstack1l1ll1ll1l_opy_))
    else:
        bstack1lll11l11l_opy_ = bstack1111l1l_opy_ (u"࠭ࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠨ଼") + urllib.parse.quote(json.dumps(bstack1l1ll1ll1l_opy_))
    browser = self.connect(bstack1lll11l11l_opy_)
    return browser
except Exception as e:
    pass
def bstack11ll1l1l1l_opy_():
    global bstack11ll11l1l_opy_
    global bstack1l111l11l1_opy_
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1llll1lll1_opy_
        global bstack1l1ll11l1_opy_
        if not bstack11111l11l_opy_:
          global bstack1l1l111ll1_opy_
          if not bstack1l1l111ll1_opy_:
            from bstack_utils.helper import bstack11l1l1ll1_opy_, bstack1lll111l11_opy_, bstack11llllll1l_opy_
            bstack1l1l111ll1_opy_ = bstack11l1l1ll1_opy_()
            bstack1lll111l11_opy_(bstack1l111l11l1_opy_)
            bstack1l1lllll_opy_ = bstack1l11ll1l1l_opy_.bstack1l1llll1_opy_(CONFIG, bstack1l111l11l1_opy_)
            bstack1l1ll11l1_opy_.bstack1ll1l111l1_opy_(bstack1111l1l_opy_ (u"ࠢࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡕࡘࡏࡅࡗࡆࡘࡤࡓࡁࡑࠤଽ"), bstack1l1lllll_opy_)
          BrowserType.connect = bstack1llll1lll1_opy_
          return
        BrowserType.launch = bstack1l1ll1l11_opy_
        bstack11ll11l1l_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1l11l1l1l_opy_
      bstack11ll11l1l_opy_ = True
    except Exception as e:
      pass
def bstack1lll1ll1ll_opy_(context, bstack1ll1lll1ll_opy_):
  try:
    context.page.evaluate(bstack1111l1l_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤା"), bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿࠭ି")+ json.dumps(bstack1ll1lll1ll_opy_) + bstack1111l1l_opy_ (u"ࠥࢁࢂࠨୀ"))
  except Exception as e:
    logger.debug(bstack1111l1l_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡻࡾ࠼ࠣࡿࢂࠨୁ").format(str(e), traceback.format_exc()))
def bstack11l1l1ll1l_opy_(context, message, level):
  try:
    context.page.evaluate(bstack1111l1l_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨୂ"), bstack1111l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫୃ") + json.dumps(message) + bstack1111l1l_opy_ (u"ࠧ࠭ࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠪୄ") + json.dumps(level) + bstack1111l1l_opy_ (u"ࠨࡿࢀࠫ୅"))
  except Exception as e:
    logger.debug(bstack1111l1l_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠢࡾࢁ࠿ࠦࡻࡾࠤ୆").format(str(e), traceback.format_exc()))
@measure(event_name=EVENTS.bstack11l11111l_opy_, stage=STAGE.bstack1l1111l1ll_opy_, bstack1ll1l1ll_opy_=bstack1lllllllll_opy_)
def bstack11ll11lll1_opy_(self, url):
  global bstack1111l11l1_opy_
  try:
    bstack1l1l1111l1_opy_(url)
  except Exception as err:
    logger.debug(bstack1l111ll1_opy_.format(str(err)))
  try:
    bstack1111l11l1_opy_(self, url)
  except Exception as e:
    try:
      bstack1ll1llll11_opy_ = str(e)
      if any(err_msg in bstack1ll1llll11_opy_ for err_msg in bstack11ll11111_opy_):
        bstack1l1l1111l1_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1l111ll1_opy_.format(str(err)))
    raise e
def bstack11ll1llll_opy_(self):
  global bstack11ll1ll1l1_opy_
  bstack11ll1ll1l1_opy_ = self
  return
def bstack1lll11l1_opy_(self):
  global bstack11l1l1l1ll_opy_
  bstack11l1l1l1ll_opy_ = self
  return
def bstack1ll111lll1_opy_(test_name, bstack11l11l1ll_opy_):
  global CONFIG
  if percy.bstack11lll1l1l_opy_() == bstack1111l1l_opy_ (u"ࠥࡸࡷࡻࡥࠣେ"):
    bstack1ll1ll1l1_opy_ = os.path.relpath(bstack11l11l1ll_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack1ll1ll1l1_opy_)
    bstack1ll1l1ll_opy_ = suite_name + bstack1111l1l_opy_ (u"ࠦ࠲ࠨୈ") + test_name
    threading.current_thread().percySessionName = bstack1ll1l1ll_opy_
def bstack1l1111llll_opy_(self, test, *args, **kwargs):
  global bstack1l11111l1_opy_
  test_name = None
  bstack11l11l1ll_opy_ = None
  if test:
    test_name = str(test.name)
    bstack11l11l1ll_opy_ = str(test.source)
  bstack1ll111lll1_opy_(test_name, bstack11l11l1ll_opy_)
  bstack1l11111l1_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.bstack11l1lll11l_opy_, stage=STAGE.bstack1l1111l1ll_opy_, bstack1ll1l1ll_opy_=bstack1lllllllll_opy_)
def bstack11l11ll1l_opy_(driver, bstack1ll1l1ll_opy_):
  if not bstack11ll1l1ll_opy_ and bstack1ll1l1ll_opy_:
      bstack11llll11l_opy_ = {
          bstack1111l1l_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬ୉"): bstack1111l1l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ୊"),
          bstack1111l1l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪୋ"): {
              bstack1111l1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ୌ"): bstack1ll1l1ll_opy_
          }
      }
      bstack1111l1l11_opy_ = bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃ୍ࠧ").format(json.dumps(bstack11llll11l_opy_))
      driver.execute_script(bstack1111l1l11_opy_)
  if bstack111l11l11_opy_:
      bstack1l11llllll_opy_ = {
          bstack1111l1l_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪ୎"): bstack1111l1l_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭୏"),
          bstack1111l1l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ୐"): {
              bstack1111l1l_opy_ (u"࠭ࡤࡢࡶࡤࠫ୑"): bstack1ll1l1ll_opy_ + bstack1111l1l_opy_ (u"ࠧࠡࡲࡤࡷࡸ࡫ࡤࠢࠩ୒"),
              bstack1111l1l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ୓"): bstack1111l1l_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧ୔")
          }
      }
      if bstack111l11l11_opy_.status == bstack1111l1l_opy_ (u"ࠪࡔࡆ࡙ࡓࠨ୕"):
          bstack1l1ll11l_opy_ = bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩୖ").format(json.dumps(bstack1l11llllll_opy_))
          driver.execute_script(bstack1l1ll11l_opy_)
          bstack1l11111l1l_opy_(driver, bstack1111l1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬୗ"))
      elif bstack111l11l11_opy_.status == bstack1111l1l_opy_ (u"࠭ࡆࡂࡋࡏࠫ୘"):
          reason = bstack1111l1l_opy_ (u"ࠢࠣ୙")
          bstack1l1111l111_opy_ = bstack1ll1l1ll_opy_ + bstack1111l1l_opy_ (u"ࠨࠢࡩࡥ࡮ࡲࡥࡥࠩ୚")
          if bstack111l11l11_opy_.message:
              reason = str(bstack111l11l11_opy_.message)
              bstack1l1111l111_opy_ = bstack1l1111l111_opy_ + bstack1111l1l_opy_ (u"ࠩࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸ࠺ࠡࠩ୛") + reason
          bstack1l11llllll_opy_[bstack1111l1l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ଡ଼")] = {
              bstack1111l1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪଢ଼"): bstack1111l1l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ୞"),
              bstack1111l1l_opy_ (u"࠭ࡤࡢࡶࡤࠫୟ"): bstack1l1111l111_opy_
          }
          bstack1l1ll11l_opy_ = bstack1111l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬୠ").format(json.dumps(bstack1l11llllll_opy_))
          driver.execute_script(bstack1l1ll11l_opy_)
          bstack1l11111l1l_opy_(driver, bstack1111l1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨୡ"), reason)
          bstack1l1ll1l1l_opy_(reason, str(bstack111l11l11_opy_), str(bstack1l1ll11lll_opy_), logger)
@measure(event_name=EVENTS.bstack1llll1l11_opy_, stage=STAGE.bstack1l1111l1ll_opy_, bstack1ll1l1ll_opy_=bstack1lllllllll_opy_)
def bstack1l1llll1ll_opy_(driver, test):
  if percy.bstack11lll1l1l_opy_() == bstack1111l1l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢୢ") and percy.bstack1l1l1l11_opy_() == bstack1111l1l_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧୣ"):
      bstack11l1ll1111_opy_ = bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ୤"), None)
      bstack1l1ll1ll_opy_(driver, bstack11l1ll1111_opy_, test)
  if (bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ୥"), None) and
      bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ୦"), None)) or (
      bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ୧"), None) and
      bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ୨"), None)):
      logger.info(bstack1111l1l_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠠࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡵࡻࡦࡿ࠮ࠡࠤ୩"))
      bstack1lll1111l1_opy_.bstack11ll1l11_opy_(driver, name=test.name, path=test.source)
def bstack111lllllll_opy_(test, bstack1ll1l1ll_opy_):
    try:
      bstack1ll1l1lll_opy_ = datetime.datetime.now()
      data = {}
      if test:
        data[bstack1111l1l_opy_ (u"ࠪࡲࡦࡳࡥࠨ୪")] = bstack1ll1l1ll_opy_
      if bstack111l11l11_opy_:
        if bstack111l11l11_opy_.status == bstack1111l1l_opy_ (u"ࠫࡕࡇࡓࡔࠩ୫"):
          data[bstack1111l1l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ୬")] = bstack1111l1l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭୭")
        elif bstack111l11l11_opy_.status == bstack1111l1l_opy_ (u"ࠧࡇࡃࡌࡐࠬ୮"):
          data[bstack1111l1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ୯")] = bstack1111l1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ୰")
          if bstack111l11l11_opy_.message:
            data[bstack1111l1l_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪୱ")] = str(bstack111l11l11_opy_.message)
      user = CONFIG[bstack1111l1l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭୲")]
      key = CONFIG[bstack1111l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ୳")]
      host = bstack1l11lll111_opy_(cli.config, [bstack1111l1l_opy_ (u"ࠨࡡࡱ࡫ࡶࠦ୴"), bstack1111l1l_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡦࠤ୵"), bstack1111l1l_opy_ (u"ࠣࡣࡳ࡭ࠧ୶")], bstack1111l1l_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡵ࡯࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠥ୷"))
      url = bstack1111l1l_opy_ (u"ࠪࡿࢂ࠵ࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡵࡨࡷࡸ࡯࡯࡯ࡵ࠲ࡿࢂ࠴ࡪࡴࡱࡱࠫ୸").format(host, bstack11111l1ll_opy_)
      headers = {
        bstack1111l1l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪ୹"): bstack1111l1l_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ୺"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers, auth=(user, key))
        cli.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠨࡨࡵࡶࡳ࠾ࡺࡶࡤࡢࡶࡨࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡷࡹࡧࡴࡶࡵࠥ୻"), datetime.datetime.now() - bstack1ll1l1lll_opy_)
    except Exception as e:
      logger.error(bstack11111111l_opy_.format(str(e)))
def bstack11111l11_opy_(test, bstack1ll1l1ll_opy_):
  global CONFIG
  global bstack11l1l1l1ll_opy_
  global bstack11ll1ll1l1_opy_
  global bstack11111l1ll_opy_
  global bstack111l11l11_opy_
  global bstack1lllllllll_opy_
  global bstack11l11l1l1_opy_
  global bstack11l11lllll_opy_
  global bstack11lll1l11l_opy_
  global bstack1ll1ll11ll_opy_
  global bstack1l11l11l1_opy_
  global bstack111111ll1_opy_
  global bstack11l1l1l1l_opy_
  try:
    if not bstack11111l1ll_opy_:
      with bstack11l1l1l1l_opy_:
        bstack11111lll_opy_ = os.path.join(os.path.expanduser(bstack1111l1l_opy_ (u"ࠧࡿࠩ୼")), bstack1111l1l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ୽"), bstack1111l1l_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫ୾"))
        if os.path.exists(bstack11111lll_opy_):
          with open(bstack11111lll_opy_, bstack1111l1l_opy_ (u"ࠪࡶࠬ୿")) as f:
            content = f.read().strip()
            if content:
              bstack1l11llll11_opy_ = json.loads(bstack1111l1l_opy_ (u"ࠦࢀࠨ஀") + content + bstack1111l1l_opy_ (u"ࠬࠨࡸࠣ࠼ࠣࠦࡾࠨࠧ஁") + bstack1111l1l_opy_ (u"ࠨࡽࠣஂ"))
              bstack11111l1ll_opy_ = bstack1l11llll11_opy_.get(str(threading.get_ident()))
  except Exception as e:
    logger.debug(bstack1111l1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡲࡦࡣࡧ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡋࡇࡷࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬஃ") + str(e))
  if bstack1l11l11l1_opy_:
    with bstack1ll11l1l11_opy_:
      bstack1l111111ll_opy_ = bstack1l11l11l1_opy_.copy()
    for driver in bstack1l111111ll_opy_:
      if bstack11111l1ll_opy_ == driver.session_id:
        if test:
          bstack1l1llll1ll_opy_(driver, test)
        bstack11l11ll1l_opy_(driver, bstack1ll1l1ll_opy_)
  elif bstack11111l1ll_opy_:
    bstack111lllllll_opy_(test, bstack1ll1l1ll_opy_)
  if bstack11l1l1l1ll_opy_:
    bstack11l11lllll_opy_(bstack11l1l1l1ll_opy_)
  if bstack11ll1ll1l1_opy_:
    bstack11lll1l11l_opy_(bstack11ll1ll1l1_opy_)
  if bstack11lll11lll_opy_:
    bstack1ll1ll11ll_opy_()
def bstack1l1111l1l1_opy_(self, test, *args, **kwargs):
  bstack1ll1l1ll_opy_ = None
  if test:
    bstack1ll1l1ll_opy_ = str(test.name)
  bstack11111l11_opy_(test, bstack1ll1l1ll_opy_)
  bstack11l11l1l1_opy_(self, test, *args, **kwargs)
def bstack11ll1lll11_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1llll1l1ll_opy_
  global CONFIG
  global bstack1l11l11l1_opy_
  global bstack11111l1ll_opy_
  global bstack11l1l1l1l_opy_
  bstack11l111111_opy_ = None
  try:
    if bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ஄"), None) or bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫஅ"), None):
      try:
        if not bstack11111l1ll_opy_:
          bstack11111lll_opy_ = os.path.join(os.path.expanduser(bstack1111l1l_opy_ (u"ࠪࢂࠬஆ")), bstack1111l1l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫஇ"), bstack1111l1l_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧஈ"))
          with bstack11l1l1l1l_opy_:
            if os.path.exists(bstack11111lll_opy_):
              with open(bstack11111lll_opy_, bstack1111l1l_opy_ (u"࠭ࡲࠨஉ")) as f:
                content = f.read().strip()
                if content:
                  bstack1l11llll11_opy_ = json.loads(bstack1111l1l_opy_ (u"ࠢࡼࠤஊ") + content + bstack1111l1l_opy_ (u"ࠨࠤࡻࠦ࠿ࠦࠢࡺࠤࠪ஋") + bstack1111l1l_opy_ (u"ࠤࢀࠦ஌"))
                  bstack11111l1ll_opy_ = bstack1l11llll11_opy_.get(str(threading.get_ident()))
      except Exception as e:
        logger.debug(bstack1111l1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡵࡩࡦࡪࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡎࡊࡳࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢࡷࡩࡸࡺࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࠩ஍") + str(e))
      if bstack1l11l11l1_opy_:
        with bstack1ll11l1l11_opy_:
          bstack1l111111ll_opy_ = bstack1l11l11l1_opy_.copy()
        for driver in bstack1l111111ll_opy_:
          if bstack11111l1ll_opy_ == driver.session_id:
            bstack11l111111_opy_ = driver
    bstack1ll1l111_opy_ = bstack1lll1111l1_opy_.bstack11l111ll_opy_(test.tags)
    if bstack11l111111_opy_:
      threading.current_thread().isA11yTest = bstack1lll1111l1_opy_.bstack11l1ll1l1l_opy_(bstack11l111111_opy_, bstack1ll1l111_opy_)
      threading.current_thread().isAppA11yTest = bstack1lll1111l1_opy_.bstack11l1ll1l1l_opy_(bstack11l111111_opy_, bstack1ll1l111_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1ll1l111_opy_
      threading.current_thread().isAppA11yTest = bstack1ll1l111_opy_
  except:
    pass
  bstack1llll1l1ll_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack111l11l11_opy_
  try:
    bstack111l11l11_opy_ = self._test
  except:
    bstack111l11l11_opy_ = self.test
def bstack1lll1ll1l1_opy_():
  global bstack11ll111l1l_opy_
  try:
    if os.path.exists(bstack11ll111l1l_opy_):
      os.remove(bstack11ll111l1l_opy_)
  except Exception as e:
    logger.debug(bstack1111l1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧஎ") + str(e))
def bstack11l1ll1l1_opy_():
  global bstack11ll111l1l_opy_
  bstack1llll11l1_opy_ = {}
  lock_file = bstack11ll111l1l_opy_ + bstack1111l1l_opy_ (u"ࠬ࠴࡬ࡰࡥ࡮ࠫஏ")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1111l1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡰࡴࡩ࡫ࠡࡰࡲࡸࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥ࠭ࠢࡸࡷ࡮ࡴࡧࠡࡤࡤࡷ࡮ࡩࠠࡧ࡫࡯ࡩࠥࡵࡰࡦࡴࡤࡸ࡮ࡵ࡮ࡴࠩஐ"))
    try:
      if not os.path.isfile(bstack11ll111l1l_opy_):
        with open(bstack11ll111l1l_opy_, bstack1111l1l_opy_ (u"ࠧࡸࠩ஑")) as f:
          json.dump({}, f)
      if os.path.exists(bstack11ll111l1l_opy_):
        with open(bstack11ll111l1l_opy_, bstack1111l1l_opy_ (u"ࠨࡴࠪஒ")) as f:
          content = f.read().strip()
          if content:
            bstack1llll11l1_opy_ = json.loads(content)
    except Exception as e:
      logger.debug(bstack1111l1l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡷ࡫ࡡࡥ࡫ࡱ࡫ࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫஓ") + str(e))
    return bstack1llll11l1_opy_
  try:
    os.makedirs(os.path.dirname(bstack11ll111l1l_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      if not os.path.isfile(bstack11ll111l1l_opy_):
        with open(bstack11ll111l1l_opy_, bstack1111l1l_opy_ (u"ࠪࡻࠬஔ")) as f:
          json.dump({}, f)
      if os.path.exists(bstack11ll111l1l_opy_):
        with open(bstack11ll111l1l_opy_, bstack1111l1l_opy_ (u"ࠫࡷ࠭க")) as f:
          content = f.read().strip()
          if content:
            bstack1llll11l1_opy_ = json.loads(content)
  except Exception as e:
    logger.debug(bstack1111l1l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡳࡧࡤࡨ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧ஖") + str(e))
  finally:
    return bstack1llll11l1_opy_
def bstack1l1l1l1ll1_opy_(platform_index, item_index):
  global bstack11ll111l1l_opy_
  lock_file = bstack11ll111l1l_opy_ + bstack1111l1l_opy_ (u"࠭࠮࡭ࡱࡦ࡯ࠬ஗")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1111l1l_opy_ (u"ࠧࡧ࡫࡯ࡩࡱࡵࡣ࡬ࠢࡱࡳࡹࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦ࠮ࠣࡹࡸ࡯࡮ࡨࠢࡥࡥࡸ࡯ࡣࠡࡨ࡬ࡰࡪࠦ࡯ࡱࡧࡵࡥࡹ࡯࡯࡯ࡵࠪ஘"))
    try:
      bstack1llll11l1_opy_ = {}
      if os.path.exists(bstack11ll111l1l_opy_):
        with open(bstack11ll111l1l_opy_, bstack1111l1l_opy_ (u"ࠨࡴࠪங")) as f:
          content = f.read().strip()
          if content:
            bstack1llll11l1_opy_ = json.loads(content)
      bstack1llll11l1_opy_[item_index] = platform_index
      with open(bstack11ll111l1l_opy_, bstack1111l1l_opy_ (u"ࠤࡺࠦச")) as outfile:
        json.dump(bstack1llll11l1_opy_, outfile)
    except Exception as e:
      logger.debug(bstack1111l1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡽࡲࡪࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨ஛") + str(e))
    return
  try:
    os.makedirs(os.path.dirname(bstack11ll111l1l_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      bstack1llll11l1_opy_ = {}
      if os.path.exists(bstack11ll111l1l_opy_):
        with open(bstack11ll111l1l_opy_, bstack1111l1l_opy_ (u"ࠫࡷ࠭ஜ")) as f:
          content = f.read().strip()
          if content:
            bstack1llll11l1_opy_ = json.loads(content)
      bstack1llll11l1_opy_[item_index] = platform_index
      with open(bstack11ll111l1l_opy_, bstack1111l1l_opy_ (u"ࠧࡽࠢ஝")) as outfile:
        json.dump(bstack1llll11l1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1111l1l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡹࡵ࡭ࡹ࡯࡮ࡨࠢࡷࡳࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫஞ") + str(e))
def bstack11ll11l111_opy_(bstack1lll1l111l_opy_):
  global CONFIG
  bstack111l1ll11_opy_ = bstack1111l1l_opy_ (u"ࠧࠨட")
  if not bstack1111l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ஠") in CONFIG:
    logger.info(bstack1111l1l_opy_ (u"ࠩࡑࡳࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠡࡲࡤࡷࡸ࡫ࡤࠡࡷࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࠦࡲࡦࡲࡲࡶࡹࠦࡦࡰࡴࠣࡖࡴࡨ࡯ࡵࠢࡵࡹࡳ࠭஡"))
  try:
    platform = CONFIG[bstack1111l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭஢")][bstack1lll1l111l_opy_]
    if bstack1111l1l_opy_ (u"ࠫࡴࡹࠧண") in platform:
      bstack111l1ll11_opy_ += str(platform[bstack1111l1l_opy_ (u"ࠬࡵࡳࠨத")]) + bstack1111l1l_opy_ (u"࠭ࠬࠡࠩ஥")
    if bstack1111l1l_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪ஦") in platform:
      bstack111l1ll11_opy_ += str(platform[bstack1111l1l_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫ஧")]) + bstack1111l1l_opy_ (u"ࠩ࠯ࠤࠬந")
    if bstack1111l1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧன") in platform:
      bstack111l1ll11_opy_ += str(platform[bstack1111l1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨப")]) + bstack1111l1l_opy_ (u"ࠬ࠲ࠠࠨ஫")
    if bstack1111l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ஬") in platform:
      bstack111l1ll11_opy_ += str(platform[bstack1111l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ஭")]) + bstack1111l1l_opy_ (u"ࠨ࠮ࠣࠫம")
    if bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧய") in platform:
      bstack111l1ll11_opy_ += str(platform[bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨர")]) + bstack1111l1l_opy_ (u"ࠫ࠱ࠦࠧற")
    if bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ல") in platform:
      bstack111l1ll11_opy_ += str(platform[bstack1111l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧள")]) + bstack1111l1l_opy_ (u"ࠧ࠭ࠢࠪழ")
  except Exception as e:
    logger.debug(bstack1111l1l_opy_ (u"ࠨࡕࡲࡱࡪࠦࡥࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡱ࡫ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡴࡶࡵ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡷ࡫ࡰࡰࡴࡷࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡵ࡮ࠨவ") + str(e))
  finally:
    if bstack111l1ll11_opy_[len(bstack111l1ll11_opy_) - 2:] == bstack1111l1l_opy_ (u"ࠩ࠯ࠤࠬஶ"):
      bstack111l1ll11_opy_ = bstack111l1ll11_opy_[:-2]
    return bstack111l1ll11_opy_
def bstack1l1111l1_opy_(path, bstack111l1ll11_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1ll1111l1_opy_ = ET.parse(path)
    bstack1111l1ll1_opy_ = bstack1ll1111l1_opy_.getroot()
    bstack1l11ll111_opy_ = None
    for suite in bstack1111l1ll1_opy_.iter(bstack1111l1l_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩஷ")):
      if bstack1111l1l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫஸ") in suite.attrib:
        suite.attrib[bstack1111l1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪஹ")] += bstack1111l1l_opy_ (u"࠭ࠠࠨ஺") + bstack111l1ll11_opy_
        bstack1l11ll111_opy_ = suite
    bstack1l11l1llll_opy_ = None
    for robot in bstack1111l1ll1_opy_.iter(bstack1111l1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭஻")):
      bstack1l11l1llll_opy_ = robot
    bstack1111llll1_opy_ = len(bstack1l11l1llll_opy_.findall(bstack1111l1l_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧ஼")))
    if bstack1111llll1_opy_ == 1:
      bstack1l11l1llll_opy_.remove(bstack1l11l1llll_opy_.findall(bstack1111l1l_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨ஽"))[0])
      bstack1l1ll1l11l_opy_ = ET.Element(bstack1111l1l_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩா"), attrib={bstack1111l1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩி"): bstack1111l1l_opy_ (u"࡙ࠬࡵࡪࡶࡨࡷࠬீ"), bstack1111l1l_opy_ (u"࠭ࡩࡥࠩு"): bstack1111l1l_opy_ (u"ࠧࡴ࠲ࠪூ")})
      bstack1l11l1llll_opy_.insert(1, bstack1l1ll1l11l_opy_)
      bstack1ll11ll1_opy_ = None
      for suite in bstack1l11l1llll_opy_.iter(bstack1111l1l_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧ௃")):
        bstack1ll11ll1_opy_ = suite
      bstack1ll11ll1_opy_.append(bstack1l11ll111_opy_)
      bstack1111lll11_opy_ = None
      for status in bstack1l11ll111_opy_.iter(bstack1111l1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ௄")):
        bstack1111lll11_opy_ = status
      bstack1ll11ll1_opy_.append(bstack1111lll11_opy_)
    bstack1ll1111l1_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1111l1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡳࡵ࡬ࡲ࡬ࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠨ௅") + str(e))
def bstack11llll1111_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1ll1l1l1ll_opy_
  global CONFIG
  if bstack1111l1l_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡴࡦࡺࡨࠣெ") in options:
    del options[bstack1111l1l_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡵࡧࡴࡩࠤே")]
  bstack1l1ll111l1_opy_ = bstack11l1ll1l1_opy_()
  for item_id in bstack1l1ll111l1_opy_.keys():
    path = os.path.join(os.getcwd(), bstack1111l1l_opy_ (u"࠭ࡰࡢࡤࡲࡸࡤࡸࡥࡴࡷ࡯ࡸࡸ࠭ை"), str(item_id), bstack1111l1l_opy_ (u"ࠧࡰࡷࡷࡴࡺࡺ࠮ࡹ࡯࡯ࠫ௉"))
    bstack1l1111l1_opy_(path, bstack11ll11l111_opy_(bstack1l1ll111l1_opy_[item_id]))
  bstack1lll1ll1l1_opy_()
  return bstack1ll1l1l1ll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1llllll111_opy_(self, ff_profile_dir):
  global bstack1ll1111l11_opy_
  if not ff_profile_dir:
    return None
  return bstack1ll1111l11_opy_(self, ff_profile_dir)
def bstack1ll111lll_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1lll1ll11_opy_
  bstack11l1llll_opy_ = []
  if bstack1111l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫொ") in CONFIG:
    bstack11l1llll_opy_ = CONFIG[bstack1111l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬோ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1111l1l_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࠦௌ")],
      pabot_args[bstack1111l1l_opy_ (u"ࠦࡻ࡫ࡲࡣࡱࡶࡩ்ࠧ")],
      argfile,
      pabot_args.get(bstack1111l1l_opy_ (u"ࠧ࡮ࡩࡷࡧࠥ௎")),
      pabot_args[bstack1111l1l_opy_ (u"ࠨࡰࡳࡱࡦࡩࡸࡹࡥࡴࠤ௏")],
      platform[0],
      bstack1lll1ll11_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1111l1l_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡨ࡬ࡰࡪࡹࠢௐ")] or [(bstack1111l1l_opy_ (u"ࠣࠤ௑"), None)]
    for platform in enumerate(bstack11l1llll_opy_)
  ]
def bstack1lll1l1111_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1lll1l11ll_opy_=bstack1111l1l_opy_ (u"ࠩࠪ௒")):
  global bstack11l11ll1l1_opy_
  self.platform_index = platform_index
  self.bstack1l11ll1l_opy_ = bstack1lll1l11ll_opy_
  bstack11l11ll1l1_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1lll111ll_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1l1ll1l1l1_opy_
  global bstack1lllll111l_opy_
  bstack1l1ll1ll11_opy_ = copy.deepcopy(item)
  if not bstack1111l1l_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ௓") in item.options:
    bstack1l1ll1ll11_opy_.options[bstack1111l1l_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭௔")] = []
  bstack1l111ll11l_opy_ = bstack1l1ll1ll11_opy_.options[bstack1111l1l_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ௕")].copy()
  for v in bstack1l1ll1ll11_opy_.options[bstack1111l1l_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨ௖")]:
    if bstack1111l1l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝࠭ௗ") in v:
      bstack1l111ll11l_opy_.remove(v)
    if bstack1111l1l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓࠨ௘") in v:
      bstack1l111ll11l_opy_.remove(v)
    if bstack1111l1l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡆࡈࡊࡑࡕࡃࡂࡎࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭௙") in v:
      bstack1l111ll11l_opy_.remove(v)
  bstack1l111ll11l_opy_.insert(0, bstack1111l1l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡓࡐࡆ࡚ࡆࡐࡔࡐࡍࡓࡊࡅ࡙࠼ࡾࢁࠬ௚").format(bstack1l1ll1ll11_opy_.platform_index))
  bstack1l111ll11l_opy_.insert(0, bstack1111l1l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒ࠻ࡽࢀࠫ௛").format(bstack1l1ll1ll11_opy_.bstack1l11ll1l_opy_))
  bstack1l1ll1ll11_opy_.options[bstack1111l1l_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ௜")] = bstack1l111ll11l_opy_
  if bstack1lllll111l_opy_:
    bstack1l1ll1ll11_opy_.options[bstack1111l1l_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨ௝")].insert(0, bstack1111l1l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙࠺ࡼࡿࠪ௞").format(bstack1lllll111l_opy_))
  return bstack1l1ll1l1l1_opy_(caller_id, datasources, is_last, bstack1l1ll1ll11_opy_, outs_dir)
def bstack1l1ll1111_opy_(command, item_index):
  try:
    if bstack1l1ll11l1_opy_.get_property(bstack1111l1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩ௟")):
      os.environ[bstack1111l1l_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪ௠")] = json.dumps(CONFIG[bstack1111l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭௡")][item_index % bstack1l1l1ll1l1_opy_])
    global bstack1lllll111l_opy_
    if bstack1lllll111l_opy_:
      command[0] = command[0].replace(bstack1111l1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ௢"), bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡸࡪ࡫ࠡࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠢ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠡࠩ௣") + str(
        item_index) + bstack1111l1l_opy_ (u"࠭ࠠࠨ௤") + bstack1lllll111l_opy_, 1)
    else:
      command[0] = command[0].replace(bstack1111l1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭௥"),
                                      bstack1111l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡴࡦ࡮ࠤࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠥ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠤࠬ௦") + str(item_index), 1)
  except Exception as e:
    logger.error(bstack1111l1l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡯ࡲࡨ࡮࡬ࡹࡪࡰࡪࠤࡨࡵ࡭࡮ࡣࡱࡨࠥ࡬࡯ࡳࠢࡳࡥࡧࡵࡴࠡࡴࡸࡲ࠿ࠦࡻࡾࠩ௧").format(str(e)))
def bstack11lll1111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1l11ll11l_opy_
  try:
    bstack1l1ll1111_opy_(command, item_index)
    return bstack1l11ll11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
  except Exception as e:
    logger.error(bstack1111l1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡣࡱࡷࠤࡷࡻ࡮࠻ࠢࡾࢁࠬ௨").format(str(e)))
    raise e
def bstack1ll1llll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1l11ll11l_opy_
  try:
    bstack1l1ll1111_opy_(command, item_index)
    return bstack1l11ll11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
  except Exception as e:
    logger.error(bstack1111l1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡢࡤࡲࡸࠥࡸࡵ࡯ࠢ࠵࠲࠶࠹࠺ࠡࡽࢀࠫ௩").format(str(e)))
    try:
      return bstack1l11ll11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
    except Exception as e2:
      logger.error(bstack1111l1l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡥࡳࡹࠦ࠲࠯࠳࠶ࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࡼࡿࠪ௪").format(str(e2)))
      raise e
def bstack11l11l11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1l11ll11l_opy_
  try:
    bstack1l1ll1111_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    return bstack1l11ll11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
  except Exception as e:
    logger.error(bstack1111l1l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠࡳࡷࡱࠤ࠷࠴࠱࠶࠼ࠣࡿࢂ࠭௫").format(str(e)))
    try:
      return bstack1l11ll11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
    except Exception as e2:
      logger.error(bstack1111l1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡧࡵࡴࠡ࠴࠱࠵࠺ࠦࡦࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢࡾࢁࠬ௬").format(str(e2)))
      raise e
def _11ll111l1_opy_(bstack11l111l111_opy_, item_index, process_timeout, sleep_before_start, bstack1l1lll111_opy_):
  bstack1l1ll1111_opy_(bstack11l111l111_opy_, item_index)
  if process_timeout is None:
    process_timeout = 3600
  if sleep_before_start and sleep_before_start > 0:
    import time
    time.sleep(min(sleep_before_start, 5))
  return process_timeout
def bstack111111l1l_opy_(command, bstack11ll1l111_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack1l11ll11l_opy_
  try:
    process_timeout = _11ll111l1_opy_(command + bstack11ll1l111_opy_, item_index, process_timeout, sleep_before_start, bstack1111l1l_opy_ (u"ࠨ࠷࠱࠴ࠬ௭"))
    return bstack1l11ll11l_opy_(command, bstack11ll1l111_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
  except Exception as e:
    logger.error(bstack1111l1l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡢࡰࡶࠣࡶࡺࡴࠠ࠶࠰࠳࠾ࠥࢁࡽࠨ௮").format(str(e)))
    try:
      return bstack1l11ll11l_opy_(command, bstack11ll1l111_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack1111l1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡣࡱࡷࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࡼࡿࠪ௯").format(str(e2)))
      raise e
def bstack1l1l1l1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack1l11ll11l_opy_
  try:
    process_timeout = _11ll111l1_opy_(command, item_index, process_timeout, sleep_before_start, bstack1111l1l_opy_ (u"ࠫ࠹࠴࠲ࠨ௰"))
    return bstack1l11ll11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack1111l1l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡥࡳࡹࠦࡲࡶࡰࠣ࠸࠳࠸࠺ࠡࡽࢀࠫ௱").format(str(e)))
    try:
      return bstack1l11ll11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack1111l1l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠࡧࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣࡿࢂ࠭௲").format(str(e2)))
      raise e
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack11ll11l1ll_opy_(self, runner, quiet=False, capture=True):
  global bstack1l11ll11l1_opy_
  bstack1l1l111ll_opy_ = bstack1l11ll11l1_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack1111l1l_opy_ (u"ࠧࡦࡺࡦࡩࡵࡺࡩࡰࡰࡢࡥࡷࡸࠧ௳")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1111l1l_opy_ (u"ࠨࡧࡻࡧࡤࡺࡲࡢࡥࡨࡦࡦࡩ࡫ࡠࡣࡵࡶࠬ௴")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1l1l111ll_opy_
def bstack1l1l111111_opy_(runner, hook_name, context, element, bstack1llll1lll_opy_, *args):
  try:
    if runner.hooks.get(hook_name):
      bstack11l1l11l1_opy_.bstack1l1ll111_opy_(hook_name, element)
    bstack1llll1lll_opy_(runner, hook_name, context, *args)
    if runner.hooks.get(hook_name):
      bstack11l1l11l1_opy_.bstack11l1llll1l_opy_(element)
      if hook_name not in [bstack1111l1l_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱ࠭௵"), bstack1111l1l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ࠭௶")] and args and hasattr(args[0], bstack1111l1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࡢࡱࡪࡹࡳࡢࡩࡨࠫ௷")):
        args[0].error_message = bstack1111l1l_opy_ (u"ࠬ࠭௸")
  except Exception as e:
    logger.debug(bstack1111l1l_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢ࡫ࡥࡳࡪ࡬ࡦࠢ࡫ࡳࡴࡱࡳࠡ࡫ࡱࠤࡧ࡫ࡨࡢࡸࡨ࠾ࠥࢁࡽࠨ௹").format(str(e)))
@measure(event_name=EVENTS.bstack11l1l1l1_opy_, stage=STAGE.bstack1l1111l1ll_opy_, hook_type=bstack1111l1l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࡁ࡭࡮ࠥ௺"), bstack1ll1l1ll_opy_=bstack1lllllllll_opy_)
def bstack1l1111ll1_opy_(runner, name, context, bstack1llll1lll_opy_, *args):
    if runner.hooks.get(bstack1111l1l_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧ௻")).__name__ != bstack1111l1l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࡥࡤࡦࡨࡤࡹࡱࡺ࡟ࡩࡱࡲ࡯ࠧ௼"):
      bstack1l1l111111_opy_(runner, name, context, runner, bstack1llll1lll_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack111111l11_opy_(bstack1111l1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ௽")) else context.browser
      runner.driver_initialised = bstack1111l1l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣ௾")
    except Exception as e:
      logger.debug(bstack1111l1l_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡪࡲࡪࡸࡨࡶࠥ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡳࡦࠢࡤࡸࡹࡸࡩࡣࡷࡷࡩ࠿ࠦࡻࡾࠩ௿").format(str(e)))
def bstack1l11ll11ll_opy_(runner, name, context, bstack1llll1lll_opy_, *args):
    bstack1l1l111111_opy_(runner, name, context, context.feature, bstack1llll1lll_opy_, *args)
    try:
      if not bstack11ll1l1ll_opy_:
        bstack11l111111_opy_ = threading.current_thread().bstackSessionDriver if bstack111111l11_opy_(bstack1111l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬఀ")) else context.browser
        if is_driver_active(bstack11l111111_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack1111l1l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣఁ")
          bstack1ll1lll1ll_opy_ = str(runner.feature.name)
          bstack1lll1ll1ll_opy_(context, bstack1ll1lll1ll_opy_)
          bstack11l111111_opy_.execute_script(bstack1111l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭ం") + json.dumps(bstack1ll1lll1ll_opy_) + bstack1111l1l_opy_ (u"ࠩࢀࢁࠬః"))
    except Exception as e:
      logger.debug(bstack1111l1l_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡬ࡥࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪఄ").format(str(e)))
def bstack1l111l1l_opy_(runner, name, context, bstack1llll1lll_opy_, *args):
    if hasattr(context, bstack1111l1l_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭అ")):
        bstack11l1l11l1_opy_.start_test(context)
    target = context.scenario if hasattr(context, bstack1111l1l_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧఆ")) else context.feature
    bstack1l1l111111_opy_(runner, name, context, target, bstack1llll1lll_opy_, *args)
@measure(event_name=EVENTS.bstack1ll1111l1l_opy_, stage=STAGE.bstack1l1111l1ll_opy_, bstack1ll1l1ll_opy_=bstack1lllllllll_opy_)
def bstack1lll1l1ll1_opy_(runner, name, context, bstack1llll1lll_opy_, *args):
    if len(context.scenario.tags) == 0: bstack11l1l11l1_opy_.start_test(context)
    bstack1l1l111111_opy_(runner, name, context, context.scenario, bstack1llll1lll_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack111lll1l1_opy_.bstack1111ll11_opy_(context, *args)
    try:
      bstack11l111111_opy_ = bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬఇ"), context.browser)
      if is_driver_active(bstack11l111111_opy_):
        bstack11l1lllll1_opy_.bstack111lll1ll_opy_(bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ఈ"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack1111l1l_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥఉ")
        if (not bstack11ll1l1ll_opy_):
          scenario_name = args[0].name
          feature_name = bstack1ll1lll1ll_opy_ = str(runner.feature.name)
          bstack1ll1lll1ll_opy_ = feature_name + bstack1111l1l_opy_ (u"ࠩࠣ࠱ࠥ࠭ఊ") + scenario_name
          if runner.driver_initialised == bstack1111l1l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧఋ"):
            bstack1lll1ll1ll_opy_(context, bstack1ll1lll1ll_opy_)
            bstack11l111111_opy_.execute_script(bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩఌ") + json.dumps(bstack1ll1lll1ll_opy_) + bstack1111l1l_opy_ (u"ࠬࢃࡽࠨ఍"))
    except Exception as e:
      logger.debug(bstack1111l1l_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱ࠽ࠤࢀࢃࠧఎ").format(str(e)))
@measure(event_name=EVENTS.bstack11l1l1l1_opy_, stage=STAGE.bstack1l1111l1ll_opy_, hook_type=bstack1111l1l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࡓࡵࡧࡳࠦఏ"), bstack1ll1l1ll_opy_=bstack1lllllllll_opy_)
def bstack1ll11ll11l_opy_(runner, name, context, bstack1llll1lll_opy_, *args):
    bstack1l1l111111_opy_(runner, name, context, args[0], bstack1llll1lll_opy_, *args)
    try:
      bstack11l111111_opy_ = threading.current_thread().bstackSessionDriver if bstack111111l11_opy_(bstack1111l1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧఐ")) else context.browser
      if is_driver_active(bstack11l111111_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack1111l1l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢ఑")
        bstack11l1l11l1_opy_.bstack11ll11l1_opy_(args[0])
        if runner.driver_initialised == bstack1111l1l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣఒ"):
          feature_name = bstack1ll1lll1ll_opy_ = str(runner.feature.name)
          bstack1ll1lll1ll_opy_ = feature_name + bstack1111l1l_opy_ (u"ࠫࠥ࠳ࠠࠨఓ") + context.scenario.name
          bstack11l111111_opy_.execute_script(bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪఔ") + json.dumps(bstack1ll1lll1ll_opy_) + bstack1111l1l_opy_ (u"࠭ࡽࡾࠩక"))
    except Exception as e:
      logger.debug(bstack1111l1l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡸࡪࡶ࠺ࠡࡽࢀࠫఖ").format(str(e)))
@measure(event_name=EVENTS.bstack11l1l1l1_opy_, stage=STAGE.bstack1l1111l1ll_opy_, hook_type=bstack1111l1l_opy_ (u"ࠣࡣࡩࡸࡪࡸࡓࡵࡧࡳࠦగ"), bstack1ll1l1ll_opy_=bstack1lllllllll_opy_)
def bstack1ll11l11_opy_(runner, name, context, bstack1llll1lll_opy_, *args):
  bstack11l1l11l1_opy_.bstack11l11lll11_opy_(args[0])
  try:
    step_status = args[0].status.name
    bstack11l111111_opy_ = threading.current_thread().bstackSessionDriver if bstack1111l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨఘ") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack11l111111_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack1111l1l_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪఙ")
        feature_name = bstack1ll1lll1ll_opy_ = str(runner.feature.name)
        bstack1ll1lll1ll_opy_ = feature_name + bstack1111l1l_opy_ (u"ࠫࠥ࠳ࠠࠨచ") + context.scenario.name
        bstack11l111111_opy_.execute_script(bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪఛ") + json.dumps(bstack1ll1lll1ll_opy_) + bstack1111l1l_opy_ (u"࠭ࡽࡾࠩజ"))
    if str(step_status).lower() == bstack1111l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧఝ"):
      bstack11ll111lll_opy_ = bstack1111l1l_opy_ (u"ࠨࠩఞ")
      bstack1l111l1lll_opy_ = bstack1111l1l_opy_ (u"ࠩࠪట")
      bstack11l1ll11l_opy_ = bstack1111l1l_opy_ (u"ࠪࠫఠ")
      try:
        import traceback
        bstack11ll111lll_opy_ = runner.exception.__class__.__name__
        bstack1llllll11_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1l111l1lll_opy_ = bstack1111l1l_opy_ (u"ࠫࠥ࠭డ").join(bstack1llllll11_opy_)
        bstack11l1ll11l_opy_ = bstack1llllll11_opy_[-1]
      except Exception as e:
        logger.debug(bstack1ll11111ll_opy_.format(str(e)))
      bstack11ll111lll_opy_ += bstack11l1ll11l_opy_
      bstack11l1l1ll1l_opy_(context, json.dumps(str(args[0].name) + bstack1111l1l_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦఢ") + str(bstack1l111l1lll_opy_)),
                          bstack1111l1l_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧణ"))
      if runner.driver_initialised == bstack1111l1l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧత"):
        bstack1l11l11l1l_opy_(getattr(context, bstack1111l1l_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭థ"), None), bstack1111l1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤద"), bstack11ll111lll_opy_)
        bstack11l111111_opy_.execute_script(bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨధ") + json.dumps(str(args[0].name) + bstack1111l1l_opy_ (u"ࠦࠥ࠳ࠠࡇࡣ࡬ࡰࡪࡪࠡ࡝ࡰࠥన") + str(bstack1l111l1lll_opy_)) + bstack1111l1l_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥࡩࡷࡸ࡯ࡳࠤࢀࢁࠬ఩"))
      if runner.driver_initialised == bstack1111l1l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦప"):
        bstack1l11111l1l_opy_(bstack11l111111_opy_, bstack1111l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧఫ"), bstack1111l1l_opy_ (u"ࠣࡕࡦࡩࡳࡧࡲࡪࡱࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧబ") + str(bstack11ll111lll_opy_))
    else:
      bstack11l1l1ll1l_opy_(context, bstack1111l1l_opy_ (u"ࠤࡓࡥࡸࡹࡥࡥࠣࠥభ"), bstack1111l1l_opy_ (u"ࠥ࡭ࡳ࡬࡯ࠣమ"))
      if runner.driver_initialised == bstack1111l1l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤయ"):
        bstack1l11l11l1l_opy_(getattr(context, bstack1111l1l_opy_ (u"ࠬࡶࡡࡨࡧࠪర"), None), bstack1111l1l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨఱ"))
      bstack11l111111_opy_.execute_script(bstack1111l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬల") + json.dumps(str(args[0].name) + bstack1111l1l_opy_ (u"ࠣࠢ࠰ࠤࡕࡧࡳࡴࡧࡧࠥࠧళ")) + bstack1111l1l_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧࢃࡽࠨఴ"))
      if runner.driver_initialised == bstack1111l1l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣవ"):
        bstack1l11111l1l_opy_(bstack11l111111_opy_, bstack1111l1l_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦశ"))
  except Exception as e:
    logger.debug(bstack1111l1l_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡶࡸࡪࡶ࠺ࠡࡽࢀࠫష").format(str(e)))
  bstack1l1l111111_opy_(runner, name, context, args[0], bstack1llll1lll_opy_, *args)
@measure(event_name=EVENTS.bstack11ll1ll1l_opy_, stage=STAGE.bstack1l1111l1ll_opy_, bstack1ll1l1ll_opy_=bstack1lllllllll_opy_)
def bstack111l1l1l1_opy_(runner, name, context, bstack1llll1lll_opy_, *args):
  bstack11l1l11l1_opy_.end_test(args[0])
  try:
    bstack1111ll1l_opy_ = args[0].status.name
    bstack11l111111_opy_ = bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬస"), context.browser)
    bstack111lll1l1_opy_.bstack1l11l11l11_opy_(bstack11l111111_opy_)
    if str(bstack1111ll1l_opy_).lower() == bstack1111l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧహ"):
      bstack11ll111lll_opy_ = bstack1111l1l_opy_ (u"ࠨࠩ఺")
      bstack1l111l1lll_opy_ = bstack1111l1l_opy_ (u"ࠩࠪ఻")
      bstack11l1ll11l_opy_ = bstack1111l1l_opy_ (u"఼ࠪࠫ")
      try:
        import traceback
        bstack11ll111lll_opy_ = runner.exception.__class__.__name__
        bstack1llllll11_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1l111l1lll_opy_ = bstack1111l1l_opy_ (u"ࠫࠥ࠭ఽ").join(bstack1llllll11_opy_)
        bstack11l1ll11l_opy_ = bstack1llllll11_opy_[-1]
      except Exception as e:
        logger.debug(bstack1ll11111ll_opy_.format(str(e)))
      bstack11ll111lll_opy_ += bstack11l1ll11l_opy_
      bstack11l1l1ll1l_opy_(context, json.dumps(str(args[0].name) + bstack1111l1l_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦా") + str(bstack1l111l1lll_opy_)),
                          bstack1111l1l_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧి"))
      if runner.driver_initialised == bstack1111l1l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤీ") or runner.driver_initialised == bstack1111l1l_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨు"):
        bstack1l11l11l1l_opy_(getattr(context, bstack1111l1l_opy_ (u"ࠩࡳࡥ࡬࡫ࠧూ"), None), bstack1111l1l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥృ"), bstack11ll111lll_opy_)
        bstack11l111111_opy_.execute_script(bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩౄ") + json.dumps(str(args[0].name) + bstack1111l1l_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦ౅") + str(bstack1l111l1lll_opy_)) + bstack1111l1l_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥࢁࢂ࠭ె"))
      if runner.driver_initialised == bstack1111l1l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤే") or runner.driver_initialised == bstack1111l1l_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨై"):
        bstack1l11111l1l_opy_(bstack11l111111_opy_, bstack1111l1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ౉"), bstack1111l1l_opy_ (u"ࠥࡗࡨ࡫࡮ࡢࡴ࡬ࡳࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢొ") + str(bstack11ll111lll_opy_))
    else:
      bstack11l1l1ll1l_opy_(context, bstack1111l1l_opy_ (u"ࠦࡕࡧࡳࡴࡧࡧࠥࠧో"), bstack1111l1l_opy_ (u"ࠧ࡯࡮ࡧࡱࠥౌ"))
      if runner.driver_initialised == bstack1111l1l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯్ࠣ") or runner.driver_initialised == bstack1111l1l_opy_ (u"ࠧࡪࡰࡶࡸࡪࡶࠧ౎"):
        bstack1l11l11l1l_opy_(getattr(context, bstack1111l1l_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭౏"), None), bstack1111l1l_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ౐"))
      bstack11l111111_opy_.execute_script(bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨ౑") + json.dumps(str(args[0].name) + bstack1111l1l_opy_ (u"ࠦࠥ࠳ࠠࡑࡣࡶࡷࡪࡪࠡࠣ౒")) + bstack1111l1l_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫ౓"))
      if runner.driver_initialised == bstack1111l1l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣ౔") or runner.driver_initialised == bstack1111l1l_opy_ (u"ࠧࡪࡰࡶࡸࡪࡶౕࠧ"):
        bstack1l11111l1l_opy_(bstack11l111111_opy_, bstack1111l1l_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤౖࠣ"))
  except Exception as e:
    logger.debug(bstack1111l1l_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫ౗").format(str(e)))
  bstack1l1l111111_opy_(runner, name, context, context.scenario, bstack1llll1lll_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack11l111lll1_opy_(runner, name, context, bstack1llll1lll_opy_, *args):
    target = context.scenario if hasattr(context, bstack1111l1l_opy_ (u"ࠪࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬౘ")) else context.feature
    bstack1l1l111111_opy_(runner, name, context, target, bstack1llll1lll_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack11l1ll1lll_opy_(runner, name, context, bstack1llll1lll_opy_, *args):
    try:
      bstack11l111111_opy_ = bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪౙ"), context.browser)
      bstack11lllll1l_opy_ = bstack1111l1l_opy_ (u"ࠬ࠭ౚ")
      if context.failed is True:
        bstack11lll1ll1l_opy_ = []
        bstack11l1l11111_opy_ = []
        bstack111ll1ll_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack11lll1ll1l_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1llllll11_opy_ = traceback.format_tb(exc_tb)
            bstack11ll11lll_opy_ = bstack1111l1l_opy_ (u"࠭ࠠࠨ౛").join(bstack1llllll11_opy_)
            bstack11l1l11111_opy_.append(bstack11ll11lll_opy_)
            bstack111ll1ll_opy_.append(bstack1llllll11_opy_[-1])
        except Exception as e:
          logger.debug(bstack1ll11111ll_opy_.format(str(e)))
        bstack11ll111lll_opy_ = bstack1111l1l_opy_ (u"ࠧࠨ౜")
        for i in range(len(bstack11lll1ll1l_opy_)):
          bstack11ll111lll_opy_ += bstack11lll1ll1l_opy_[i] + bstack111ll1ll_opy_[i] + bstack1111l1l_opy_ (u"ࠨ࡞ࡱࠫౝ")
        bstack11lllll1l_opy_ = bstack1111l1l_opy_ (u"ࠩࠣࠫ౞").join(bstack11l1l11111_opy_)
        if runner.driver_initialised in [bstack1111l1l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦ౟"), bstack1111l1l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣౠ")]:
          bstack11l1l1ll1l_opy_(context, bstack11lllll1l_opy_, bstack1111l1l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦౡ"))
          bstack1l11l11l1l_opy_(getattr(context, bstack1111l1l_opy_ (u"࠭ࡰࡢࡩࡨࠫౢ"), None), bstack1111l1l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢౣ"), bstack11ll111lll_opy_)
          bstack11l111111_opy_.execute_script(bstack1111l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭౤") + json.dumps(bstack11lllll1l_opy_) + bstack1111l1l_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࡽࡾࠩ౥"))
          bstack1l11111l1l_opy_(bstack11l111111_opy_, bstack1111l1l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ౦"), bstack1111l1l_opy_ (u"ࠦࡘࡵ࡭ࡦࠢࡶࡧࡪࡴࡡࡳ࡫ࡲࡷࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦ࡜࡯ࠤ౧") + str(bstack11ll111lll_opy_))
          bstack1lll1lllll_opy_ = bstack1ll1l1l1_opy_(bstack11lllll1l_opy_, runner.feature.name, logger)
          if (bstack1lll1lllll_opy_ != None):
            bstack1lll11llll_opy_.append(bstack1lll1lllll_opy_)
      else:
        if runner.driver_initialised in [bstack1111l1l_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨ౨"), bstack1111l1l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥ౩")]:
          bstack11l1l1ll1l_opy_(context, bstack1111l1l_opy_ (u"ࠢࡇࡧࡤࡸࡺࡸࡥ࠻ࠢࠥ౪") + str(runner.feature.name) + bstack1111l1l_opy_ (u"ࠣࠢࡳࡥࡸࡹࡥࡥࠣࠥ౫"), bstack1111l1l_opy_ (u"ࠤ࡬ࡲ࡫ࡵࠢ౬"))
          bstack1l11l11l1l_opy_(getattr(context, bstack1111l1l_opy_ (u"ࠪࡴࡦ࡭ࡥࠨ౭"), None), bstack1111l1l_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ౮"))
          bstack11l111111_opy_.execute_script(bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ౯") + json.dumps(bstack1111l1l_opy_ (u"ࠨࡆࡦࡣࡷࡹࡷ࡫࠺ࠡࠤ౰") + str(runner.feature.name) + bstack1111l1l_opy_ (u"ࠢࠡࡲࡤࡷࡸ࡫ࡤࠢࠤ౱")) + bstack1111l1l_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦࢂࢃࠧ౲"))
          bstack1l11111l1l_opy_(bstack11l111111_opy_, bstack1111l1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ౳"))
          bstack1lll1lllll_opy_ = bstack1ll1l1l1_opy_(bstack11lllll1l_opy_, runner.feature.name, logger)
          if (bstack1lll1lllll_opy_ != None):
            bstack1lll11llll_opy_.append(bstack1lll1lllll_opy_)
    except Exception as e:
      logger.debug(bstack1111l1l_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡯࡮ࠡࡣࡩࡸࡪࡸࠠࡧࡧࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬ౴").format(str(e)))
    bstack1l1l111111_opy_(runner, name, context, context.feature, bstack1llll1lll_opy_, *args)
@measure(event_name=EVENTS.bstack11l1l1l1_opy_, stage=STAGE.bstack1l1111l1ll_opy_, hook_type=bstack1111l1l_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࡄࡰࡱࠨ౵"), bstack1ll1l1ll_opy_=bstack1lllllllll_opy_)
def bstack1ll11ll1ll_opy_(runner, name, context, bstack1llll1lll_opy_, *args):
    bstack1l1l111111_opy_(runner, name, context, runner, bstack1llll1lll_opy_, *args)
def bstack11ll1ll1_opy_(self, name, context, *args):
  try:
    if bstack11111l11l_opy_:
      platform_index = int(threading.current_thread()._name) % bstack1l1l1ll1l1_opy_
      bstack1ll111111l_opy_ = CONFIG[bstack1111l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ౶")][platform_index]
      os.environ[bstack1111l1l_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧ౷")] = json.dumps(bstack1ll111111l_opy_)
    global bstack1llll1lll_opy_
    if not hasattr(self, bstack1111l1l_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡨࡨࠬ౸")):
      self.driver_initialised = None
    bstack1111ll111_opy_ = {
        bstack1111l1l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠬ౹"): bstack1l1111ll1_opy_,
        bstack1111l1l_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠪ౺"): bstack1l11ll11ll_opy_,
        bstack1111l1l_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡸࡦ࡭ࠧ౻"): bstack1l111l1l_opy_,
        bstack1111l1l_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭౼"): bstack1lll1l1ll1_opy_,
        bstack1111l1l_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠪ౽"): bstack1ll11ll11l_opy_,
        bstack1111l1l_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡴࡦࡲࠪ౾"): bstack1ll11l11_opy_,
        bstack1111l1l_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨ౿"): bstack111l1l1l1_opy_,
        bstack1111l1l_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡵࡣࡪࠫಀ"): bstack11l111lll1_opy_,
        bstack1111l1l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠩಁ"): bstack11l1ll1lll_opy_,
        bstack1111l1l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ࠭ಂ"): bstack1ll11ll1ll_opy_
    }
    handler = bstack1111ll111_opy_.get(name, bstack1llll1lll_opy_)
    try:
      handler(self, name, context, bstack1llll1lll_opy_, *args)
    except Exception as e:
      logger.debug(bstack1111l1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡢࡦࡪࡤࡺࡪࠦࡨࡰࡱ࡮ࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶࠥࢁࡽ࠻ࠢࡾࢁࠬಃ").format(name, str(e)))
    if name in [bstack1111l1l_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬ಄"), bstack1111l1l_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧಅ"), bstack1111l1l_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪಆ")]:
      try:
        bstack11l111111_opy_ = threading.current_thread().bstackSessionDriver if bstack111111l11_opy_(bstack1111l1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧಇ")) else context.browser
        bstack11lll11l1_opy_ = (
          (name == bstack1111l1l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠬಈ") and self.driver_initialised == bstack1111l1l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢಉ")) or
          (name == bstack1111l1l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫಊ") and self.driver_initialised == bstack1111l1l_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨಋ")) or
          (name == bstack1111l1l_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧಌ") and self.driver_initialised in [bstack1111l1l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤ಍"), bstack1111l1l_opy_ (u"ࠣ࡫ࡱࡷࡹ࡫ࡰࠣಎ")]) or
          (name == bstack1111l1l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡷࡩࡵ࠭ಏ") and self.driver_initialised == bstack1111l1l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣಐ"))
        )
        if bstack11lll11l1_opy_:
          self.driver_initialised = None
          if bstack11l111111_opy_ and hasattr(bstack11l111111_opy_, bstack1111l1l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨ಑")):
            try:
              bstack11l111111_opy_.quit()
            except Exception as e:
              logger.debug(bstack1111l1l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡶࡻࡩࡵࡶ࡬ࡲ࡬ࠦࡤࡳ࡫ࡹࡩࡷࠦࡩ࡯ࠢࡥࡩ࡭ࡧࡶࡦࠢ࡫ࡳࡴࡱ࠺ࠡࡽࢀࠫಒ").format(str(e)))
      except Exception as e:
        logger.debug(bstack1111l1l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡣࡩࡸࡪࡸࠠࡩࡱࡲ࡯ࠥࡩ࡬ࡦࡣࡱࡹࡵࠦࡦࡰࡴࠣࡿࢂࡀࠠࡼࡿࠪಓ").format(name, str(e)))
  except Exception as e:
    logger.debug(bstack1111l1l_opy_ (u"ࠧࡄࡴ࡬ࡸ࡮ࡩࡡ࡭ࠢࡨࡶࡷࡵࡲࠡ࡫ࡱࠤࡧ࡫ࡨࡢࡸࡨࠤࡷࡻ࡮ࠡࡪࡲࡳࡰࠦࡻࡾ࠼ࠣࡿࢂ࠭ಔ").format(name, str(e)))
    try:
      bstack1llll1lll_opy_(self, name, context, *args)
    except Exception as e2:
      logger.debug(bstack1111l1l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡵࡲࡪࡩ࡬ࡲࡦࡲࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡩࡱࡲ࡯ࠥࢁࡽ࠻ࠢࡾࢁࠬಕ").format(name, str(e2)))
def bstack1111l1lll_opy_(config, startdir):
  return bstack1111l1l_opy_ (u"ࠤࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡿ࠵ࢃࠢಖ").format(bstack1111l1l_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤಗ"))
notset = Notset()
def bstack11l11llll1_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack11lll111l1_opy_
  if str(name).lower() == bstack1111l1l_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࠫಘ"):
    return bstack1111l1l_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦಙ")
  else:
    return bstack11lll111l1_opy_(self, name, default, skip)
def bstack11l111ll11_opy_(item, when):
  global bstack1l1llll11l_opy_
  try:
    bstack1l1llll11l_opy_(item, when)
  except Exception as e:
    pass
def bstack111ll1l1_opy_():
  return
def bstack1ll1l1l1l_opy_(type, name, status, reason, bstack1lll111l1_opy_, bstack1l1l1ll1ll_opy_):
  bstack11llll11l_opy_ = {
    bstack1111l1l_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭ಚ"): type,
    bstack1111l1l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪಛ"): {}
  }
  if type == bstack1111l1l_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪಜ"):
    bstack11llll11l_opy_[bstack1111l1l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬಝ")][bstack1111l1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩಞ")] = bstack1lll111l1_opy_
    bstack11llll11l_opy_[bstack1111l1l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧಟ")][bstack1111l1l_opy_ (u"ࠬࡪࡡࡵࡣࠪಠ")] = json.dumps(str(bstack1l1l1ll1ll_opy_))
  if type == bstack1111l1l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧಡ"):
    bstack11llll11l_opy_[bstack1111l1l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪಢ")][bstack1111l1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ಣ")] = name
  if type == bstack1111l1l_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬತ"):
    bstack11llll11l_opy_[bstack1111l1l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ಥ")][bstack1111l1l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫದ")] = status
    if status == bstack1111l1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬಧ"):
      bstack11llll11l_opy_[bstack1111l1l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩನ")][bstack1111l1l_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧ಩")] = json.dumps(str(reason))
  bstack1111l1l11_opy_ = bstack1111l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ಪ").format(json.dumps(bstack11llll11l_opy_))
  return bstack1111l1l11_opy_
def bstack1l11lllll_opy_(driver_command, response):
    if driver_command == bstack1111l1l_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭ಫ"):
        bstack11l1lllll1_opy_.bstack1111l1ll_opy_({
            bstack1111l1l_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩಬ"): response[bstack1111l1l_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪಭ")],
            bstack1111l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬಮ"): bstack11l1lllll1_opy_.current_test_uuid()
        })
def bstack1l11l1ll1_opy_(item, call, rep):
  global bstack1l111111l1_opy_
  global bstack1l11l11l1_opy_
  global bstack11ll1l1ll_opy_
  name = bstack1111l1l_opy_ (u"࠭ࠧಯ")
  try:
    if rep.when == bstack1111l1l_opy_ (u"ࠧࡤࡣ࡯ࡰࠬರ"):
      bstack11111l1ll_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack11ll1l1ll_opy_:
          name = str(rep.nodeid)
          bstack11lll11ll1_opy_ = bstack1ll1l1l1l_opy_(bstack1111l1l_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩಱ"), name, bstack1111l1l_opy_ (u"ࠩࠪಲ"), bstack1111l1l_opy_ (u"ࠪࠫಳ"), bstack1111l1l_opy_ (u"ࠫࠬ಴"), bstack1111l1l_opy_ (u"ࠬ࠭ವ"))
          threading.current_thread().bstack11l1111l1l_opy_ = name
          for driver in bstack1l11l11l1_opy_:
            if bstack11111l1ll_opy_ == driver.session_id:
              driver.execute_script(bstack11lll11ll1_opy_)
      except Exception as e:
        logger.debug(bstack1111l1l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭ಶ").format(str(e)))
      try:
        bstack11l1llllll_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack1111l1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨಷ"):
          status = bstack1111l1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨಸ") if rep.outcome.lower() == bstack1111l1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩಹ") else bstack1111l1l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ಺")
          reason = bstack1111l1l_opy_ (u"ࠫࠬ಻")
          if status == bstack1111l1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨ಼ࠬ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack1111l1l_opy_ (u"࠭ࡩ࡯ࡨࡲࠫಽ") if status == bstack1111l1l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧಾ") else bstack1111l1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧಿ")
          data = name + bstack1111l1l_opy_ (u"ࠩࠣࡴࡦࡹࡳࡦࡦࠤࠫೀ") if status == bstack1111l1l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪು") else name + bstack1111l1l_opy_ (u"ࠫࠥ࡬ࡡࡪ࡮ࡨࡨࠦࠦࠧೂ") + reason
          bstack11l1ll111l_opy_ = bstack1ll1l1l1l_opy_(bstack1111l1l_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧೃ"), bstack1111l1l_opy_ (u"࠭ࠧೄ"), bstack1111l1l_opy_ (u"ࠧࠨ೅"), bstack1111l1l_opy_ (u"ࠨࠩೆ"), level, data)
          for driver in bstack1l11l11l1_opy_:
            if bstack11111l1ll_opy_ == driver.session_id:
              driver.execute_script(bstack11l1ll111l_opy_)
      except Exception as e:
        logger.debug(bstack1111l1l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡣࡰࡰࡷࡩࡽࡺࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭ೇ").format(str(e)))
  except Exception as e:
    logger.debug(bstack1111l1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡵࡣࡷࡩࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࢀࢃࠧೈ").format(str(e)))
  bstack1l111111l1_opy_(item, call, rep)
def bstack1l1ll1ll_opy_(driver, bstack1lll11l11_opy_, test=None):
  global bstack1l1ll11lll_opy_
  if test != None:
    bstack1ll1l1111l_opy_ = getattr(test, bstack1111l1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ೉"), None)
    bstack1l1l11l11_opy_ = getattr(test, bstack1111l1l_opy_ (u"ࠬࡻࡵࡪࡦࠪೊ"), None)
    PercySDK.screenshot(driver, bstack1lll11l11_opy_, bstack1ll1l1111l_opy_=bstack1ll1l1111l_opy_, bstack1l1l11l11_opy_=bstack1l1l11l11_opy_, bstack1l11l11ll1_opy_=bstack1l1ll11lll_opy_)
  else:
    PercySDK.screenshot(driver, bstack1lll11l11_opy_)
@measure(event_name=EVENTS.bstack1ll1l11l1_opy_, stage=STAGE.bstack1l1111l1ll_opy_, bstack1ll1l1ll_opy_=bstack1lllllllll_opy_)
def bstack111ll1ll1_opy_(driver):
  if bstack11l1lll11_opy_.bstack1l1lll1l_opy_() is True or bstack11l1lll11_opy_.capturing() is True:
    return
  bstack11l1lll11_opy_.bstack1lll11l1l1_opy_()
  while not bstack11l1lll11_opy_.bstack1l1lll1l_opy_():
    bstack11lll111l_opy_ = bstack11l1lll11_opy_.bstack11lll11ll_opy_()
    bstack1l1ll1ll_opy_(driver, bstack11lll111l_opy_)
  bstack11l1lll11_opy_.bstack1ll1ll1l1l_opy_()
def bstack11l1l1llll_opy_(sequence, driver_command, response = None, bstack11l111l1_opy_ = None, args = None):
    try:
      if sequence != bstack1111l1l_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭ೋ"):
        return
      if percy.bstack11lll1l1l_opy_() == bstack1111l1l_opy_ (u"ࠢࡧࡣ࡯ࡷࡪࠨೌ"):
        return
      bstack11lll111l_opy_ = bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠨࡲࡨࡶࡨࡿࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨ್ࠫ"), None)
      for command in bstack1111lllll_opy_:
        if command == driver_command:
          with bstack1ll11l1l11_opy_:
            bstack1l111111ll_opy_ = bstack1l11l11l1_opy_.copy()
          for driver in bstack1l111111ll_opy_:
            bstack111ll1ll1_opy_(driver)
      bstack11111ll1_opy_ = percy.bstack1l1l1l11_opy_()
      if driver_command in bstack1l1l11lll1_opy_[bstack11111ll1_opy_]:
        bstack11l1lll11_opy_.bstack111111l1_opy_(bstack11lll111l_opy_, driver_command)
    except Exception as e:
      pass
def bstack1l11l1ll11_opy_(framework_name):
  if bstack1l1ll11l1_opy_.get_property(bstack1111l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡰࡳࡩࡥࡣࡢ࡮࡯ࡩࡩ࠭೎")):
      return
  bstack1l1ll11l1_opy_.bstack1ll1l111l1_opy_(bstack1111l1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡱࡴࡪ࡟ࡤࡣ࡯ࡰࡪࡪࠧ೏"), True)
  global bstack1l111l11l1_opy_
  global bstack11ll11l1l_opy_
  global bstack1l1l1ll111_opy_
  bstack1l111l11l1_opy_ = framework_name
  logger.info(bstack1l11ll1lll_opy_.format(bstack1l111l11l1_opy_.split(bstack1111l1l_opy_ (u"ࠫ࠲࠭೐"))[0]))
  bstack11l11111l1_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack11111l11l_opy_:
      Service.start = bstack111l1l11l_opy_
      Service.stop = bstack1llll1l1l1_opy_
      webdriver.Remote.get = bstack11ll11lll1_opy_
      WebDriver.quit = bstack1llll11l1l_opy_
      webdriver.Remote.__init__ = bstack11l1lll1_opy_
    if not bstack11111l11l_opy_:
        webdriver.Remote.__init__ = bstack1l11l1l111_opy_
    WebDriver.getAccessibilityResults = getAccessibilityResults
    WebDriver.get_accessibility_results = getAccessibilityResults
    WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
    WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
    WebDriver.performScan = perform_scan
    WebDriver.perform_scan = perform_scan
    WebDriver.execute = bstack1l1lll11ll_opy_
    bstack11ll11l1l_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack11111l11l_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1l1llll111_opy_
  except Exception as e:
    pass
  bstack11ll1l1l1l_opy_()
  if not bstack11ll11l1l_opy_:
    bstack11l1111ll1_opy_(bstack1111l1l_opy_ (u"ࠧࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠠ࡯ࡱࡷࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪࠢ೑"), bstack111l1ll1_opy_)
  if bstack111llllll_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      if hasattr(RemoteConnection, bstack1111l1l_opy_ (u"࠭࡟ࡨࡧࡷࡣࡵࡸ࡯ࡹࡻࡢࡹࡷࡲࠧ೒")) and callable(getattr(RemoteConnection, bstack1111l1l_opy_ (u"ࠧࡠࡩࡨࡸࡤࡶࡲࡰࡺࡼࡣࡺࡸ࡬ࠨ೓"))):
        RemoteConnection._get_proxy_url = bstack1l1l1l111_opy_
      else:
        from selenium.webdriver.remote.client_config import ClientConfig
        ClientConfig.get_proxy_url = bstack1l1l1l111_opy_
    except Exception as e:
      logger.error(bstack1ll1l1111_opy_.format(str(e)))
  if bstack1l1lll1ll_opy_():
    bstack1l1111l11_opy_(CONFIG, logger)
  if (bstack1111l1l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ೔") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if percy.bstack11lll1l1l_opy_() == bstack1111l1l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢೕ"):
          bstack11llllll1_opy_(bstack11l1l1llll_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1llllll111_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1lll11l1_opy_
      except Exception as e:
        logger.warn(bstack11ll11111l_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack11ll1llll_opy_
      except Exception as e:
        logger.debug(bstack1l1lll1ll1_opy_ + str(e))
    except Exception as e:
      bstack11l1111ll1_opy_(e, bstack11ll11111l_opy_)
    Output.start_test = bstack1l1111llll_opy_
    Output.end_test = bstack1l1111l1l1_opy_
    TestStatus.__init__ = bstack11ll1lll11_opy_
    QueueItem.__init__ = bstack1lll1l1111_opy_
    pabot._create_items = bstack1ll111lll_opy_
    try:
      from pabot import __version__ as bstack111111lll_opy_
      if version.parse(bstack111111lll_opy_) >= version.parse(bstack1111l1l_opy_ (u"ࠪ࠹࠳࠶࠮࠱ࠩೖ")):
        pabot._run = bstack111111l1l_opy_
      elif version.parse(bstack111111lll_opy_) >= version.parse(bstack1111l1l_opy_ (u"ࠫ࠹࠴࠲࠯࠲ࠪ೗")):
        pabot._run = bstack1l1l1l1ll_opy_
      elif version.parse(bstack111111lll_opy_) >= version.parse(bstack1111l1l_opy_ (u"ࠬ࠸࠮࠲࠷࠱࠴ࠬ೘")):
        pabot._run = bstack11l11l11l_opy_
      elif version.parse(bstack111111lll_opy_) >= version.parse(bstack1111l1l_opy_ (u"࠭࠲࠯࠳࠶࠲࠵࠭೙")):
        pabot._run = bstack1ll1llll1_opy_
      else:
        pabot._run = bstack11lll1111_opy_
    except Exception as e:
      pabot._run = bstack11lll1111_opy_
    pabot._create_command_for_execution = bstack1lll111ll_opy_
    pabot._report_results = bstack11llll1111_opy_
  if bstack1111l1l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ೚") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11l1111ll1_opy_(e, bstack1l1l1lllll_opy_)
    Runner.run_hook = bstack11ll1ll1_opy_
    Step.run = bstack11ll11l1ll_opy_
  if bstack1111l1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ೛") in str(framework_name).lower():
    if not bstack11111l11l_opy_:
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack1111l1lll_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack111ll1l1_opy_
      Config.getoption = bstack11l11llll1_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1l11l1ll1_opy_
    except Exception as e:
      pass
def bstack1ll11l1ll_opy_():
  global CONFIG
  if bstack1111l1l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ೜") in CONFIG and int(CONFIG[bstack1111l1l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪೝ")]) > 1:
    logger.warn(bstack11ll1l11l1_opy_)
def bstack1llll111l_opy_(arg, bstack1l111l1l1l_opy_, bstack1llllll1l1_opy_=None):
  global CONFIG
  global bstack1l111l1ll_opy_
  global bstack111lll111_opy_
  global bstack11111l11l_opy_
  global bstack1l1ll11l1_opy_
  bstack1l1lllllll_opy_ = bstack1111l1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫೞ")
  if bstack1l111l1l1l_opy_ and isinstance(bstack1l111l1l1l_opy_, str):
    bstack1l111l1l1l_opy_ = eval(bstack1l111l1l1l_opy_)
  CONFIG = bstack1l111l1l1l_opy_[bstack1111l1l_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬ೟")]
  bstack1l111l1ll_opy_ = bstack1l111l1l1l_opy_[bstack1111l1l_opy_ (u"࠭ࡈࡖࡄࡢ࡙ࡗࡒࠧೠ")]
  bstack111lll111_opy_ = bstack1l111l1l1l_opy_[bstack1111l1l_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩೡ")]
  bstack11111l11l_opy_ = bstack1l111l1l1l_opy_[bstack1111l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫೢ")]
  bstack1l1ll11l1_opy_.bstack1ll1l111l1_opy_(bstack1111l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪೣ"), bstack11111l11l_opy_)
  os.environ[bstack1111l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬ೤")] = bstack1l1lllllll_opy_
  os.environ[bstack1111l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠪ೥")] = json.dumps(CONFIG)
  os.environ[bstack1111l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡍ࡛ࡂࡠࡗࡕࡐࠬ೦")] = bstack1l111l1ll_opy_
  os.environ[bstack1111l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ೧")] = str(bstack111lll111_opy_)
  os.environ[bstack1111l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡍࡗࡊࡍࡓ࠭೨")] = str(True)
  if bstack1l1ll1ll1_opy_(arg, [bstack1111l1l_opy_ (u"ࠨ࠯ࡱࠫ೩"), bstack1111l1l_opy_ (u"ࠩ࠰࠱ࡳࡻ࡭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ೪")]) != -1:
    os.environ[bstack1111l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡅࡗࡇࡌࡍࡇࡏࠫ೫")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack11ll1ll11_opy_)
    return
  bstack1l1l1l1l11_opy_()
  global bstack1l11l11111_opy_
  global bstack1l1ll11lll_opy_
  global bstack1lll1ll11_opy_
  global bstack1lllll111l_opy_
  global bstack1lllll11_opy_
  global bstack1l1l1ll111_opy_
  global bstack11llll1lll_opy_
  arg.append(bstack1111l1l_opy_ (u"ࠦ࠲࡝ࠢ೬"))
  arg.append(bstack1111l1l_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩ࠿ࡓ࡯ࡥࡷ࡯ࡩࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡩ࡮ࡲࡲࡶࡹ࡫ࡤ࠻ࡲࡼࡸࡪࡹࡴ࠯ࡒࡼࡸࡪࡹࡴࡘࡣࡵࡲ࡮ࡴࡧࠣ೭"))
  arg.append(bstack1111l1l_opy_ (u"ࠨ࠭ࡘࠤ೮"))
  arg.append(bstack1111l1l_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫࠺ࡕࡪࡨࠤ࡭ࡵ࡯࡬࡫ࡰࡴࡱࠨ೯"))
  global bstack1l1llll11_opy_
  global bstack11lllll11l_opy_
  global bstack1l1lllll1l_opy_
  global bstack1llll1l1ll_opy_
  global bstack1ll1111l11_opy_
  global bstack11l11ll1l1_opy_
  global bstack1l1ll1l1l1_opy_
  global bstack1ll1ll1111_opy_
  global bstack1111l11l1_opy_
  global bstack1ll1l1llll_opy_
  global bstack11lll111l1_opy_
  global bstack1l1llll11l_opy_
  global bstack1l111111l1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l1llll11_opy_ = webdriver.Remote.__init__
    bstack11lllll11l_opy_ = WebDriver.quit
    bstack1ll1ll1111_opy_ = WebDriver.close
    bstack1111l11l1_opy_ = WebDriver.get
    bstack1l1lllll1l_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1llll111_opy_(CONFIG) and bstack1l11l111l1_opy_():
    if bstack1ll1l1lll1_opy_() < version.parse(bstack1lllll11l_opy_):
      logger.error(bstack11l1111l11_opy_.format(bstack1ll1l1lll1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack1111l1l_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩ೰")) and callable(getattr(RemoteConnection, bstack1111l1l_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪೱ"))):
          bstack1ll1l1llll_opy_ = RemoteConnection._get_proxy_url
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          bstack1ll1l1llll_opy_ = ClientConfig.get_proxy_url
      except Exception as e:
        logger.error(bstack1ll1l1111_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack11lll111l1_opy_ = Config.getoption
    from _pytest import runner
    bstack1l1llll11l_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack11ll1l1l_opy_)
  try:
    from pytest_bdd import reporting
    bstack1l111111l1_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack1111l1l_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡲࠤࡷࡻ࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࡶࠫೲ"))
  bstack1lll1ll11_opy_ = CONFIG.get(bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨೳ"), {}).get(bstack1111l1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ೴"))
  bstack11llll1lll_opy_ = True
  if cli.is_enabled(CONFIG):
    if cli.bstack111llll1l1_opy_():
      bstack11lllll1ll_opy_.invoke(bstack1l111l1111_opy_.CONNECT, bstack11l11l11l1_opy_())
    platform_index = int(os.environ.get(bstack1111l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭೵"), bstack1111l1l_opy_ (u"ࠧ࠱ࠩ೶")))
  else:
    bstack1l11l1ll11_opy_(bstack11l11111_opy_)
  os.environ[bstack1111l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩ೷")] = CONFIG[bstack1111l1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ೸")]
  os.environ[bstack1111l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭೹")] = CONFIG[bstack1111l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ೺")]
  os.environ[bstack1111l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ೻")] = bstack11111l11l_opy_.__str__()
  from _pytest.config import main as bstack1l1l1l1111_opy_
  bstack11l1l111_opy_ = []
  try:
    exit_code = bstack1l1l1l1111_opy_(arg)
    if cli.is_enabled(CONFIG):
      cli.bstack11lll1l111_opy_()
    if bstack1111l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶࠪ೼") in multiprocessing.current_process().__dict__.keys():
      for bstack11l1ll1l_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack11l1l111_opy_.append(bstack11l1ll1l_opy_)
    try:
      bstack11llll11_opy_ = (bstack11l1l111_opy_, int(exit_code))
      bstack1llllll1l1_opy_.append(bstack11llll11_opy_)
    except:
      bstack1llllll1l1_opy_.append((bstack11l1l111_opy_, exit_code))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack11l1l111_opy_.append({bstack1111l1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ೽"): bstack1111l1l_opy_ (u"ࠨࡒࡵࡳࡨ࡫ࡳࡴࠢࠪ೾") + os.environ.get(bstack1111l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ೿")), bstack1111l1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩഀ"): traceback.format_exc(), bstack1111l1l_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪഁ"): int(os.environ.get(bstack1111l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬം")))})
    bstack1llllll1l1_opy_.append((bstack11l1l111_opy_, 1))
def mod_behave_main(args, retries):
  try:
    from behave.configuration import Configuration
    from behave.__main__ import run_behave
    from browserstack_sdk.bstack_behave_runner import BehaveRunner
    config = Configuration(args)
    config.update_userdata({bstack1111l1l_opy_ (u"ࠨࡲࡦࡶࡵ࡭ࡪࡹࠢഃ"): str(retries)})
    return run_behave(config, runner_class=BehaveRunner)
  except Exception as e:
    bstack1l1l11l1l1_opy_ = e.__class__.__name__
    print(bstack1111l1l_opy_ (u"ࠢࠦࡵ࠽ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡶࡺࡴ࡮ࡪࡰࡪࠤࡧ࡫ࡨࡢࡸࡨࠤࡹ࡫ࡳࡵࠢࠨࡷࠧഄ") % (bstack1l1l11l1l1_opy_, e))
    return 1
def bstack1l111ll1l1_opy_(arg):
  global bstack1l1llllll1_opy_
  bstack1l11l1ll11_opy_(bstack1l1lllll1_opy_)
  os.environ[bstack1111l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩഅ")] = str(bstack111lll111_opy_)
  retries = bstack111l1llll_opy_.bstack1l1ll1llll_opy_(CONFIG)
  status_code = 0
  if bstack111l1llll_opy_.bstack11111ll1l_opy_(CONFIG):
    status_code = mod_behave_main(arg, retries)
  else:
    from behave.__main__ import main as bstack11l1ll1ll_opy_
    status_code = bstack11l1ll1ll_opy_(arg)
  if status_code != 0:
    bstack1l1llllll1_opy_ = status_code
def bstack1l1l11l1_opy_():
  logger.info(bstack111l11l1l_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1111l1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨആ"), help=bstack1111l1l_opy_ (u"ࠪࡋࡪࡴࡥࡳࡣࡷࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡨࡵ࡮ࡧ࡫ࡪࠫഇ"))
  parser.add_argument(bstack1111l1l_opy_ (u"ࠫ࠲ࡻࠧഈ"), bstack1111l1l_opy_ (u"ࠬ࠳࠭ࡶࡵࡨࡶࡳࡧ࡭ࡦࠩഉ"), help=bstack1111l1l_opy_ (u"࡙࠭ࡰࡷࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬഊ"))
  parser.add_argument(bstack1111l1l_opy_ (u"ࠧ࠮࡭ࠪഋ"), bstack1111l1l_opy_ (u"ࠨ࠯࠰࡯ࡪࡿࠧഌ"), help=bstack1111l1l_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡡࡤࡥࡨࡷࡸࠦ࡫ࡦࡻࠪ഍"))
  parser.add_argument(bstack1111l1l_opy_ (u"ࠪ࠱࡫࠭എ"), bstack1111l1l_opy_ (u"ࠫ࠲࠳ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩഏ"), help=bstack1111l1l_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫഐ"))
  bstack1lll1l11l1_opy_ = parser.parse_args()
  try:
    bstack1l11lll11_opy_ = bstack1111l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥ࡯ࡧࡵ࡭ࡨ࠴ࡹ࡮࡮࠱ࡷࡦࡳࡰ࡭ࡧࠪ഑")
    if bstack1lll1l11l1_opy_.framework and bstack1lll1l11l1_opy_.framework not in (bstack1111l1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧഒ"), bstack1111l1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩഓ")):
      bstack1l11lll11_opy_ = bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠲ࡾࡳ࡬࠯ࡵࡤࡱࡵࡲࡥࠨഔ")
    bstack1ll111ll1_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l11lll11_opy_)
    bstack1l11l1lll1_opy_ = open(bstack1ll111ll1_opy_, bstack1111l1l_opy_ (u"ࠪࡶࠬക"))
    bstack111l11lll_opy_ = bstack1l11l1lll1_opy_.read()
    bstack1l11l1lll1_opy_.close()
    if bstack1lll1l11l1_opy_.username:
      bstack111l11lll_opy_ = bstack111l11lll_opy_.replace(bstack1111l1l_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫഖ"), bstack1lll1l11l1_opy_.username)
    if bstack1lll1l11l1_opy_.key:
      bstack111l11lll_opy_ = bstack111l11lll_opy_.replace(bstack1111l1l_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧഗ"), bstack1lll1l11l1_opy_.key)
    if bstack1lll1l11l1_opy_.framework:
      bstack111l11lll_opy_ = bstack111l11lll_opy_.replace(bstack1111l1l_opy_ (u"࡙࠭ࡐࡗࡕࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧഘ"), bstack1lll1l11l1_opy_.framework)
    file_name = bstack1111l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪങ")
    file_path = os.path.abspath(file_name)
    bstack1ll1l11ll_opy_ = open(file_path, bstack1111l1l_opy_ (u"ࠨࡹࠪച"))
    bstack1ll1l11ll_opy_.write(bstack111l11lll_opy_)
    bstack1ll1l11ll_opy_.close()
    logger.info(bstack1l1lll1111_opy_)
    try:
      os.environ[bstack1111l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫഛ")] = bstack1lll1l11l1_opy_.framework if bstack1lll1l11l1_opy_.framework != None else bstack1111l1l_opy_ (u"ࠥࠦജ")
      config = yaml.safe_load(bstack111l11lll_opy_)
      config[bstack1111l1l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫഝ")] = bstack1111l1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲ࡹࡥࡵࡷࡳࠫഞ")
      bstack1l1l1111_opy_(bstack111l111ll_opy_, config)
    except Exception as e:
      logger.debug(bstack1llll1l11l_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1l1l1l1l1_opy_.format(str(e)))
def bstack1l1l1111_opy_(bstack1llll1111_opy_, config, bstack1ll1lll111_opy_={}):
  global bstack11111l11l_opy_
  global bstack1lll1l1l1l_opy_
  global bstack1l1ll11l1_opy_
  if not config:
    return
  bstack1lllllll1_opy_ = bstack11111l1l_opy_ if not bstack11111l11l_opy_ else (
    bstack1ll1l11lll_opy_ if bstack1111l1l_opy_ (u"࠭ࡡࡱࡲࠪട") in config else (
        bstack1ll1ll1l_opy_ if config.get(bstack1111l1l_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫഠ")) else bstack11lll11l1l_opy_
    )
)
  bstack1l11111l11_opy_ = False
  bstack1l111ll1ll_opy_ = False
  if bstack11111l11l_opy_ is True:
      if bstack1111l1l_opy_ (u"ࠨࡣࡳࡴࠬഡ") in config:
          bstack1l11111l11_opy_ = True
      else:
          bstack1l111ll1ll_opy_ = True
  bstack1l1lllll_opy_ = bstack1l11ll1l1l_opy_.bstack1l1llll1_opy_(config, bstack1lll1l1l1l_opy_)
  bstack11l111ll1l_opy_ = bstack1ll11l11l1_opy_()
  data = {
    bstack1111l1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫഢ"): config[bstack1111l1l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬണ")],
    bstack1111l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧത"): config[bstack1111l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨഥ")],
    bstack1111l1l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪദ"): bstack1llll1111_opy_,
    bstack1111l1l_opy_ (u"ࠧࡥࡧࡷࡩࡨࡺࡥࡥࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫധ"): os.environ.get(bstack1111l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪന"), bstack1lll1l1l1l_opy_),
    bstack1111l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫഩ"): bstack1ll11ll111_opy_,
    bstack1111l1l_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰࠬപ"): bstack1lllll1lll_opy_(),
    bstack1111l1l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧഫ"): {
      bstack1111l1l_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪബ"): str(config[bstack1111l1l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ഭ")]) if bstack1111l1l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧമ") in config else bstack1111l1l_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤയ"),
      bstack1111l1l_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨ࡚ࡪࡸࡳࡪࡱࡱࠫര"): sys.version,
      bstack1111l1l_opy_ (u"ࠪࡶࡪ࡬ࡥࡳࡴࡨࡶࠬറ"): bstack11lll1l11_opy_(os.environ.get(bstack1111l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ല"), bstack1lll1l1l1l_opy_)),
      bstack1111l1l_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠧള"): bstack1111l1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ഴ"),
      bstack1111l1l_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨവ"): bstack1lllllll1_opy_,
      bstack1111l1l_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭ശ"): bstack1l1lllll_opy_,
      bstack1111l1l_opy_ (u"ࠩࡷࡩࡸࡺࡨࡶࡤࡢࡹࡺ࡯ࡤࠨഷ"): os.environ[bstack1111l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨസ")],
      bstack1111l1l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧഹ"): os.environ.get(bstack1111l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧഺ"), bstack1lll1l1l1l_opy_),
      bstack1111l1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯഻ࠩ"): bstack11llll11l1_opy_(os.environ.get(bstack1111l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌ഼ࠩ"), bstack1lll1l1l1l_opy_)),
      bstack1111l1l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧഽ"): bstack11l111ll1l_opy_.get(bstack1111l1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧാ")),
      bstack1111l1l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩി"): bstack11l111ll1l_opy_.get(bstack1111l1l_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬീ")),
      bstack1111l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨു"): config[bstack1111l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩൂ")] if config[bstack1111l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪൃ")] else bstack1111l1l_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤൄ"),
      bstack1111l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ൅"): str(config[bstack1111l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬെ")]) if bstack1111l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭േ") in config else bstack1111l1l_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨൈ"),
      bstack1111l1l_opy_ (u"࠭࡯ࡴࠩ൉"): sys.platform,
      bstack1111l1l_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩൊ"): socket.gethostname(),
      bstack1111l1l_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪോ"): bstack1l1ll11l1_opy_.get_property(bstack1111l1l_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫൌ"))
    }
  }
  if not bstack1l1ll11l1_opy_.get_property(bstack1111l1l_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮്ࠪ")) is None:
    data[bstack1111l1l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧൎ")][bstack1111l1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࡍࡦࡶࡤࡨࡦࡺࡡࠨ൏")] = {
      bstack1111l1l_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭൐"): bstack1111l1l_opy_ (u"ࠧࡶࡵࡨࡶࡤࡱࡩ࡭࡮ࡨࡨࠬ൑"),
      bstack1111l1l_opy_ (u"ࠨࡵ࡬࡫ࡳࡧ࡬ࠨ൒"): bstack1l1ll11l1_opy_.get_property(bstack1111l1l_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩ൓")),
      bstack1111l1l_opy_ (u"ࠪࡷ࡮࡭࡮ࡢ࡮ࡑࡹࡲࡨࡥࡳࠩൔ"): bstack1l1ll11l1_opy_.get_property(bstack1111l1l_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡓࡵࠧൕ"))
    }
  if bstack1llll1111_opy_ == bstack11ll11l1l1_opy_:
    data[bstack1111l1l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨൖ")][bstack1111l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡈࡵ࡮ࡧ࡫ࡪࠫൗ")] = bstack11l1llll11_opy_(config)
    data[bstack1111l1l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪ൘")][bstack1111l1l_opy_ (u"ࠨ࡫ࡶࡔࡪࡸࡣࡺࡃࡸࡸࡴࡋ࡮ࡢࡤ࡯ࡩࡩ࠭൙")] = percy.bstack1l111lllll_opy_
    data[bstack1111l1l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬ൚")][bstack1111l1l_opy_ (u"ࠪࡴࡪࡸࡣࡺࡄࡸ࡭ࡱࡪࡉࡥࠩ൛")] = percy.percy_build_id
  if not bstack111l1llll_opy_.bstack1l11l1111l_opy_(CONFIG):
    data[bstack1111l1l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧ൜")][bstack1111l1l_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠩ൝")] = bstack111l1llll_opy_.bstack1l11l1111l_opy_(CONFIG)
  bstack11ll1111ll_opy_ = bstack11l11l111l_opy_.bstack1l11llll1_opy_(CONFIG, logger)
  bstack11llllll_opy_ = bstack111l1llll_opy_.bstack1l11llll1_opy_(config=CONFIG)
  if bstack11ll1111ll_opy_ is not None and bstack11llllll_opy_ is not None and bstack11llllll_opy_.bstack1ll11llll1_opy_():
    data[bstack1111l1l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩ൞")][bstack11llllll_opy_.bstack1lll111111_opy_()] = bstack11ll1111ll_opy_.bstack11ll11ll_opy_()
  update(data[bstack1111l1l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪൟ")], bstack1ll1lll111_opy_)
  try:
    response = bstack1ll111l111_opy_(bstack1111l1l_opy_ (u"ࠨࡒࡒࡗ࡙࠭ൠ"), bstack11l11l11_opy_(bstack1ll11lllll_opy_), data, {
      bstack1111l1l_opy_ (u"ࠩࡤࡹࡹ࡮ࠧൡ"): (config[bstack1111l1l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬൢ")], config[bstack1111l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧൣ")])
    })
    if response:
      logger.debug(bstack11lllllll_opy_.format(bstack1llll1111_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack11lllll111_opy_.format(str(e)))
def bstack11lll1l11_opy_(framework):
  return bstack1111l1l_opy_ (u"ࠧࢁࡽ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࡻࡾࠤ൤").format(str(framework), __version__) if framework else bstack1111l1l_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࢀࢃࠢ൥").format(
    __version__)
def bstack1l1l1l1l11_opy_():
  global CONFIG
  global bstack1l1ll11l1l_opy_
  if bool(CONFIG):
    return
  try:
    bstack1l11lll1l1_opy_()
    logger.debug(bstack1l1l1ll1l_opy_.format(str(CONFIG)))
    bstack1l1ll11l1l_opy_ = bstack11l1111l1_opy_.configure_logger(CONFIG, bstack1l1ll11l1l_opy_)
    bstack11l11111l1_opy_()
  except Exception as e:
    logger.error(bstack1111l1l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱ࠮ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠦ൦") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1l1l11lll_opy_
  atexit.register(bstack11l11l111_opy_)
  signal.signal(signal.SIGINT, bstack11l11ll1_opy_)
  signal.signal(signal.SIGTERM, bstack11l11ll1_opy_)
def bstack1l1l11lll_opy_(exctype, value, traceback):
  global bstack1l11l11l1_opy_
  try:
    for driver in bstack1l11l11l1_opy_:
      bstack1l11111l1l_opy_(driver, bstack1111l1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ൧"), bstack1111l1l_opy_ (u"ࠤࡖࡩࡸࡹࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧ൨") + str(value))
  except Exception:
    pass
  logger.info(bstack1l1111111_opy_)
  bstack1ll1lll11l_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1ll1lll11l_opy_(message=bstack1111l1l_opy_ (u"ࠪࠫ൩"), bstack111l11ll_opy_ = False):
  global CONFIG
  bstack11ll1111l1_opy_ = bstack1111l1l_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡉࡽࡩࡥࡱࡶ࡬ࡳࡳ࠭൪") if bstack111l11ll_opy_ else bstack1111l1l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ൫")
  try:
    if message:
      bstack1ll1lll111_opy_ = {
        bstack11ll1111l1_opy_ : str(message)
      }
      bstack1l1l1111_opy_(bstack11ll11l1l1_opy_, CONFIG, bstack1ll1lll111_opy_)
    else:
      bstack1l1l1111_opy_(bstack11ll11l1l1_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack111ll1l11_opy_.format(str(e)))
def bstack11lll1l1l1_opy_(bstack1lll11111l_opy_, size):
  bstack1ll11l1l_opy_ = []
  while len(bstack1lll11111l_opy_) > size:
    bstack11ll1l1ll1_opy_ = bstack1lll11111l_opy_[:size]
    bstack1ll11l1l_opy_.append(bstack11ll1l1ll1_opy_)
    bstack1lll11111l_opy_ = bstack1lll11111l_opy_[size:]
  bstack1ll11l1l_opy_.append(bstack1lll11111l_opy_)
  return bstack1ll11l1l_opy_
def bstack1111l1111_opy_(args):
  if bstack1111l1l_opy_ (u"࠭࠭࡮ࠩ൬") in args and bstack1111l1l_opy_ (u"ࠧࡱࡦࡥࠫ൭") in args:
    return True
  return False
@measure(event_name=EVENTS.bstack1l111l111_opy_, stage=STAGE.bstack1111l11ll_opy_)
def run_on_browserstack(bstack1l111l1ll1_opy_=None, bstack1llllll1l1_opy_=None, bstack1l1l1111ll_opy_=False):
  global CONFIG
  global bstack1l111l1ll_opy_
  global bstack111lll111_opy_
  global bstack1lll1l1l1l_opy_
  global bstack1l1ll11l1_opy_
  bstack1l1lllllll_opy_ = bstack1111l1l_opy_ (u"ࠨࠩ൮")
  bstack1lll11111_opy_(bstack11llll111_opy_, logger)
  if bstack1l111l1ll1_opy_ and isinstance(bstack1l111l1ll1_opy_, str):
    bstack1l111l1ll1_opy_ = eval(bstack1l111l1ll1_opy_)
  if bstack1l111l1ll1_opy_:
    CONFIG = bstack1l111l1ll1_opy_[bstack1111l1l_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩ൯")]
    bstack1l111l1ll_opy_ = bstack1l111l1ll1_opy_[bstack1111l1l_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫ൰")]
    bstack111lll111_opy_ = bstack1l111l1ll1_opy_[bstack1111l1l_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭൱")]
    bstack1l1ll11l1_opy_.bstack1ll1l111l1_opy_(bstack1111l1l_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ൲"), bstack111lll111_opy_)
    bstack1l1lllllll_opy_ = bstack1111l1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭൳")
  bstack1l1ll11l1_opy_.bstack1ll1l111l1_opy_(bstack1111l1l_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥࠩ൴"), uuid4().__str__())
  logger.info(bstack1111l1l_opy_ (u"ࠨࡕࡇࡏࠥࡸࡵ࡯ࠢࡶࡸࡦࡸࡴࡦࡦࠣࡻ࡮ࡺࡨࠡ࡫ࡧ࠾ࠥ࠭൵") + bstack1l1ll11l1_opy_.get_property(bstack1111l1l_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫ൶")));
  logger.debug(bstack1111l1l_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࡂ࠭൷") + bstack1l1ll11l1_opy_.get_property(bstack1111l1l_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭൸")))
  if not bstack1l1l1111ll_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack11ll1ll11_opy_)
      return
    if sys.argv[1] == bstack1111l1l_opy_ (u"ࠬ࠳࠭ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ൹") or sys.argv[1] == bstack1111l1l_opy_ (u"࠭࠭ࡷࠩൺ"):
      logger.info(bstack1111l1l_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡐࡺࡶ࡫ࡳࡳࠦࡓࡅࡍࠣࡺࢀࢃࠧൻ").format(__version__))
      return
    if sys.argv[1] == bstack1111l1l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧർ"):
      bstack1l1l11l1_opy_()
      return
  args = sys.argv
  bstack1l1l1l1l11_opy_()
  global bstack1l11l11111_opy_
  global bstack1l1l1ll1l1_opy_
  global bstack11llll1lll_opy_
  global bstack11l11l11ll_opy_
  global bstack1l1ll11lll_opy_
  global bstack1lll1ll11_opy_
  global bstack1lllll111l_opy_
  global bstack11l1lllll_opy_
  global bstack1lllll11_opy_
  global bstack1l1l1ll111_opy_
  global bstack111ll11ll_opy_
  bstack1l1l1ll1l1_opy_ = len(CONFIG.get(bstack1111l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬൽ"), []))
  if not bstack1l1lllllll_opy_:
    if args[1] == bstack1111l1l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪൾ") or args[1] == bstack1111l1l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬൿ"):
      bstack1l1lllllll_opy_ = bstack1111l1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ඀")
      args = args[2:]
    elif args[1] == bstack1111l1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬඁ"):
      bstack1l1lllllll_opy_ = bstack1111l1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ං")
      args = args[2:]
    elif args[1] == bstack1111l1l_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧඃ"):
      bstack1l1lllllll_opy_ = bstack1111l1l_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ඄")
      args = args[2:]
    elif args[1] == bstack1111l1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫඅ"):
      bstack1l1lllllll_opy_ = bstack1111l1l_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬආ")
      args = args[2:]
    elif args[1] == bstack1111l1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬඇ"):
      bstack1l1lllllll_opy_ = bstack1111l1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ඈ")
      args = args[2:]
    elif args[1] == bstack1111l1l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧඉ"):
      bstack1l1lllllll_opy_ = bstack1111l1l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨඊ")
      args = args[2:]
    else:
      if not bstack1111l1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬඋ") in CONFIG or str(CONFIG[bstack1111l1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ඌ")]).lower() in [bstack1111l1l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫඍ"), bstack1111l1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠸࠭ඎ")]:
        bstack1l1lllllll_opy_ = bstack1111l1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ඏ")
        args = args[1:]
      elif str(CONFIG[bstack1111l1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪඐ")]).lower() == bstack1111l1l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧඑ"):
        bstack1l1lllllll_opy_ = bstack1111l1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨඒ")
        args = args[1:]
      elif str(CONFIG[bstack1111l1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ඓ")]).lower() == bstack1111l1l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪඔ"):
        bstack1l1lllllll_opy_ = bstack1111l1l_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫඕ")
        args = args[1:]
      elif str(CONFIG[bstack1111l1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩඖ")]).lower() == bstack1111l1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ඗"):
        bstack1l1lllllll_opy_ = bstack1111l1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ඘")
        args = args[1:]
      elif str(CONFIG[bstack1111l1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ඙")]).lower() == bstack1111l1l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪක"):
        bstack1l1lllllll_opy_ = bstack1111l1l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫඛ")
        args = args[1:]
      else:
        os.environ[bstack1111l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧග")] = bstack1l1lllllll_opy_
        bstack1111ll1l1_opy_(bstack1l1l1lll11_opy_)
  os.environ[bstack1111l1l_opy_ (u"࠭ࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࡡࡘࡗࡊࡊࠧඝ")] = bstack1l1lllllll_opy_
  bstack1lll1l1l1l_opy_ = bstack1l1lllllll_opy_
  if cli.is_enabled(CONFIG):
    try:
      bstack1l11lll1ll_opy_ = bstack11l111l11_opy_[bstack1111l1l_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࠭ࡃࡆࡇࠫඞ")] if bstack1l1lllllll_opy_ == bstack1111l1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨඟ") and bstack1ll1l1l1l1_opy_() else bstack1l1lllllll_opy_
      bstack11lllll1ll_opy_.invoke(bstack1l111l1111_opy_.bstack11l11ll1ll_opy_, bstack11l1lll1l_opy_(
        sdk_version=__version__,
        path_config=bstack1llll1ll1_opy_(),
        path_project=os.getcwd(),
        test_framework=bstack1l11lll1ll_opy_,
        frameworks=[bstack1l11lll1ll_opy_],
        framework_versions={
          bstack1l11lll1ll_opy_: bstack11llll11l1_opy_(bstack1111l1l_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨච") if bstack1l1lllllll_opy_ in [bstack1111l1l_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩඡ"), bstack1111l1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪජ"), bstack1111l1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ඣ")] else bstack1l1lllllll_opy_)
        },
        bs_config=CONFIG
      ))
      if cli.config.get(bstack1111l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣඤ"), None):
        CONFIG[bstack1111l1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤඥ")] = cli.config.get(bstack1111l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠥඦ"), None)
    except Exception as e:
      bstack11lllll1ll_opy_.invoke(bstack1l111l1111_opy_.bstack1l11111l_opy_, e.__traceback__, 1)
    if bstack111lll111_opy_:
      CONFIG[bstack1111l1l_opy_ (u"ࠤࡤࡴࡵࠨට")] = cli.config[bstack1111l1l_opy_ (u"ࠥࡥࡵࡶࠢඨ")]
      logger.info(bstack1lll11ll1l_opy_.format(CONFIG[bstack1111l1l_opy_ (u"ࠫࡦࡶࡰࠨඩ")]))
  else:
    bstack11lllll1ll_opy_.clear()
  global bstack1lll1llll1_opy_
  global bstack1l1l111ll1_opy_
  if bstack1l111l1ll1_opy_:
    try:
      bstack1ll1l1lll_opy_ = datetime.datetime.now()
      os.environ[bstack1111l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧඪ")] = bstack1l1lllllll_opy_
      bstack1l1l1111_opy_(bstack1111l1l1l_opy_, CONFIG)
      cli.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠨࡨࡵࡶࡳ࠾ࡸࡪ࡫ࡠࡶࡨࡷࡹࡥࡡࡵࡶࡨࡱࡵࡺࡥࡥࠤණ"), datetime.datetime.now() - bstack1ll1l1lll_opy_)
    except Exception as e:
      logger.debug(bstack11ll1111_opy_.format(str(e)))
  global bstack1l1llll11_opy_
  global bstack11lllll11l_opy_
  global bstack1l11111l1_opy_
  global bstack11l11l1l1_opy_
  global bstack11lll1l11l_opy_
  global bstack11l11lllll_opy_
  global bstack1llll1l1ll_opy_
  global bstack1ll1111l11_opy_
  global bstack1l11ll11l_opy_
  global bstack11l11ll1l1_opy_
  global bstack1l1ll1l1l1_opy_
  global bstack1ll1ll1111_opy_
  global bstack1llll1lll_opy_
  global bstack1l11ll11l1_opy_
  global bstack1111l11l1_opy_
  global bstack1ll1l1llll_opy_
  global bstack11lll111l1_opy_
  global bstack1l1llll11l_opy_
  global bstack1ll1l1l1ll_opy_
  global bstack1l111111l1_opy_
  global bstack1l1lllll1l_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l1llll11_opy_ = webdriver.Remote.__init__
    bstack11lllll11l_opy_ = WebDriver.quit
    bstack1ll1ll1111_opy_ = WebDriver.close
    bstack1111l11l1_opy_ = WebDriver.get
    bstack1l1lllll1l_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1lll1llll1_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack11l1l1ll1_opy_
    bstack1l1l111ll1_opy_ = bstack11l1l1ll1_opy_()
  except Exception as e:
    pass
  try:
    global bstack1ll1ll11ll_opy_
    from QWeb.keywords import browser
    bstack1ll1ll11ll_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1llll111_opy_(CONFIG) and bstack1l11l111l1_opy_():
    if bstack1ll1l1lll1_opy_() < version.parse(bstack1lllll11l_opy_):
      logger.error(bstack11l1111l11_opy_.format(bstack1ll1l1lll1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack1111l1l_opy_ (u"ࠧࡠࡩࡨࡸࡤࡶࡲࡰࡺࡼࡣࡺࡸ࡬ࠨඬ")) and callable(getattr(RemoteConnection, bstack1111l1l_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩත"))):
          RemoteConnection._get_proxy_url = bstack1l1l1l111_opy_
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          ClientConfig.get_proxy_url = bstack1l1l1l111_opy_
      except Exception as e:
        logger.error(bstack1ll1l1111_opy_.format(str(e)))
  if not CONFIG.get(bstack1111l1l_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫථ"), False) and not bstack1l111l1ll1_opy_:
    logger.info(bstack1lll11ll1_opy_)
  if not cli.is_enabled(CONFIG):
    if bstack1111l1l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧද") in CONFIG and str(CONFIG[bstack1111l1l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨධ")]).lower() != bstack1111l1l_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫන"):
      bstack1l1ll1l111_opy_()
    elif bstack1l1lllllll_opy_ != bstack1111l1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭඲") or (bstack1l1lllllll_opy_ == bstack1111l1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧඳ") and not bstack1l111l1ll1_opy_):
      bstack1ll1111111_opy_()
  if (bstack1l1lllllll_opy_ in [bstack1111l1l_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧප"), bstack1111l1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨඵ"), bstack1111l1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫබ")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1llllll111_opy_
        bstack11l11lllll_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack11ll11111l_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack11lll1l11l_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1l1lll1ll1_opy_ + str(e))
    except Exception as e:
      bstack11l1111ll1_opy_(e, bstack11ll11111l_opy_)
    if bstack1l1lllllll_opy_ != bstack1111l1l_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬභ"):
      bstack1lll1ll1l1_opy_()
    bstack1l11111l1_opy_ = Output.start_test
    bstack11l11l1l1_opy_ = Output.end_test
    bstack1llll1l1ll_opy_ = TestStatus.__init__
    bstack1l11ll11l_opy_ = pabot._run
    bstack11l11ll1l1_opy_ = QueueItem.__init__
    bstack1l1ll1l1l1_opy_ = pabot._create_command_for_execution
    bstack1ll1l1l1ll_opy_ = pabot._report_results
  if bstack1l1lllllll_opy_ == bstack1111l1l_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬම"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11l1111ll1_opy_(e, bstack1l1l1lllll_opy_)
    bstack1llll1lll_opy_ = Runner.run_hook
    bstack1l11ll11l1_opy_ = Step.run
  if bstack1l1lllllll_opy_ == bstack1111l1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ඹ"):
    try:
      from _pytest.config import Config
      bstack11lll111l1_opy_ = Config.getoption
      from _pytest import runner
      bstack1l1llll11l_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack11ll1l1l_opy_)
    try:
      from pytest_bdd import reporting
      bstack1l111111l1_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1111l1l_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨය"))
  try:
    framework_name = bstack1111l1l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧර") if bstack1l1lllllll_opy_ in [bstack1111l1l_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ඼"), bstack1111l1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩල"), bstack1111l1l_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ඾")] else bstack1lllllll11_opy_(bstack1l1lllllll_opy_)
    bstack1l1ll1l1_opy_ = {
      bstack1111l1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪ࠭඿"): bstack1111l1l_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨව") if bstack1l1lllllll_opy_ == bstack1111l1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧශ") and bstack1ll1l1l1l1_opy_() else framework_name,
      bstack1111l1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬෂ"): bstack11llll11l1_opy_(framework_name),
      bstack1111l1l_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧස"): __version__,
      bstack1111l1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡵࡴࡧࡧࠫහ"): bstack1l1lllllll_opy_
    }
    if bstack1l1lllllll_opy_ in bstack11ll111l11_opy_ + bstack1l11ll1ll_opy_:
      if bstack1lll1111l1_opy_.bstack11l1l11ll_opy_(CONFIG):
        if bstack1111l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫළ") in CONFIG:
          os.environ[bstack1111l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ෆ")] = os.getenv(bstack1111l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ෇"), json.dumps(CONFIG[bstack1111l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ෈")]))
          CONFIG[bstack1111l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ෉")].pop(bstack1111l1l_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫්ࠧ"), None)
          CONFIG[bstack1111l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ෋")].pop(bstack1111l1l_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ෌"), None)
        bstack1l1ll1l1_opy_[bstack1111l1l_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ෍")] = {
          bstack1111l1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ෎"): bstack1111l1l_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩා"),
          bstack1111l1l_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩැ"): str(bstack1ll1l1lll1_opy_())
        }
    if bstack1l1lllllll_opy_ not in [bstack1111l1l_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪෑ")] and not cli.is_running():
      bstack111llll11_opy_, bstack11ll11ll11_opy_ = bstack11l1lllll1_opy_.launch(CONFIG, bstack1l1ll1l1_opy_)
      if bstack11ll11ll11_opy_.get(bstack1111l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪි")) is not None and bstack1lll1111l1_opy_.bstack1llllllll1_opy_(CONFIG) is None:
        value = bstack11ll11ll11_opy_[bstack1111l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫී")].get(bstack1111l1l_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ු"))
        if value is not None:
            CONFIG[bstack1111l1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭෕")] = value
        else:
          logger.debug(bstack1111l1l_opy_ (u"ࠢࡏࡱࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡨࡦࡺࡡࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡶࡪࡹࡰࡰࡰࡶࡩࠧූ"))
  except Exception as e:
    logger.debug(bstack11ll1lll1_opy_.format(bstack1111l1l_opy_ (u"ࠨࡖࡨࡷࡹࡎࡵࡣࠩ෗"), str(e)))
  if bstack1l1lllllll_opy_ == bstack1111l1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩෘ"):
    bstack11llll1lll_opy_ = True
    if bstack1l111l1ll1_opy_ and bstack1l1l1111ll_opy_:
      bstack1lll1ll11_opy_ = CONFIG.get(bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧෙ"), {}).get(bstack1111l1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ේ"))
      bstack1l11l1ll11_opy_(bstack1ll1lll1l_opy_)
    elif bstack1l111l1ll1_opy_:
      bstack1lll1ll11_opy_ = CONFIG.get(bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩෛ"), {}).get(bstack1111l1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨො"))
      global bstack1l11l11l1_opy_
      try:
        if bstack1111l1111_opy_(bstack1l111l1ll1_opy_[bstack1111l1l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪෝ")]) and multiprocessing.current_process().name == bstack1111l1l_opy_ (u"ࠨ࠲ࠪෞ"):
          bstack1l111l1ll1_opy_[bstack1111l1l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬෟ")].remove(bstack1111l1l_opy_ (u"ࠪ࠱ࡲ࠭෠"))
          bstack1l111l1ll1_opy_[bstack1111l1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ෡")].remove(bstack1111l1l_opy_ (u"ࠬࡶࡤࡣࠩ෢"))
          bstack1l111l1ll1_opy_[bstack1111l1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ෣")] = bstack1l111l1ll1_opy_[bstack1111l1l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ෤")][0]
          with open(bstack1l111l1ll1_opy_[bstack1111l1l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ෥")], bstack1111l1l_opy_ (u"ࠩࡵࠫ෦")) as f:
            bstack1ll11lll11_opy_ = f.read()
          bstack1ll1l111ll_opy_ = bstack1111l1l_opy_ (u"ࠥࠦࠧ࡬ࡲࡰ࡯ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡨࡰࠦࡩ࡮ࡲࡲࡶࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦ࠽ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪ࠮ࡻࡾࠫ࠾ࠤ࡫ࡸ࡯࡮ࠢࡳࡨࡧࠦࡩ࡮ࡲࡲࡶࡹࠦࡐࡥࡤ࠾ࠤࡴ࡭࡟ࡥࡤࠣࡁࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡦࡨࡪࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠩࡵࡨࡰ࡫࠲ࠠࡢࡴࡪ࠰ࠥࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠡ࠿ࠣ࠴࠮ࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺࡲࡺ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡥࡷ࡭ࠠ࠾ࠢࡶࡸࡷ࠮ࡩ࡯ࡶࠫࡥࡷ࡭ࠩࠬ࠳࠳࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡩࡽࡩࡥࡱࡶࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡡࡴࠢࡨ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡶࡡࡴࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡱࡪࡣࡩࡨࠨࡴࡧ࡯ࡪ࠱ࡧࡲࡨ࠮ࡷࡩࡲࡶ࡯ࡳࡣࡵࡽ࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡓࡨࡧ࠴ࡤࡰࡡࡥࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮ࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣࠪࠬ࠲ࡸ࡫ࡴࡠࡶࡵࡥࡨ࡫ࠨࠪ࡞ࡱࠦࠧࠨ෧").format(str(bstack1l111l1ll1_opy_))
          bstack111llll1ll_opy_ = bstack1ll1l111ll_opy_ + bstack1ll11lll11_opy_
          bstack11lll1lll1_opy_ = bstack1l111l1ll1_opy_[bstack1111l1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ෨")] + bstack1111l1l_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥࡴࡦ࡯ࡳ࠲ࡵࡿࠧ෩")
          with open(bstack11lll1lll1_opy_, bstack1111l1l_opy_ (u"࠭ࡷࠨ෪")):
            pass
          with open(bstack11lll1lll1_opy_, bstack1111l1l_opy_ (u"ࠢࡸ࠭ࠥ෫")) as f:
            f.write(bstack111llll1ll_opy_)
          import subprocess
          bstack111lllll11_opy_ = subprocess.run([bstack1111l1l_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࠣ෬"), bstack11lll1lll1_opy_])
          if os.path.exists(bstack11lll1lll1_opy_):
            os.unlink(bstack11lll1lll1_opy_)
          os._exit(bstack111lllll11_opy_.returncode)
        else:
          if bstack1111l1111_opy_(bstack1l111l1ll1_opy_[bstack1111l1l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ෭")]):
            bstack1l111l1ll1_opy_[bstack1111l1l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭෮")].remove(bstack1111l1l_opy_ (u"ࠫ࠲ࡳࠧ෯"))
            bstack1l111l1ll1_opy_[bstack1111l1l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ෰")].remove(bstack1111l1l_opy_ (u"࠭ࡰࡥࡤࠪ෱"))
            bstack1l111l1ll1_opy_[bstack1111l1l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪෲ")] = bstack1l111l1ll1_opy_[bstack1111l1l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫෳ")][0]
          bstack1l11l1ll11_opy_(bstack1ll1lll1l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1l111l1ll1_opy_[bstack1111l1l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ෴")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1111l1l_opy_ (u"ࠪࡣࡤࡴࡡ࡮ࡧࡢࡣࠬ෵")] = bstack1111l1l_opy_ (u"ࠫࡤࡥ࡭ࡢ࡫ࡱࡣࡤ࠭෶")
          mod_globals[bstack1111l1l_opy_ (u"ࠬࡥ࡟ࡧ࡫࡯ࡩࡤࡥࠧ෷")] = os.path.abspath(bstack1l111l1ll1_opy_[bstack1111l1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ෸")])
          exec(open(bstack1l111l1ll1_opy_[bstack1111l1l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ෹")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1111l1l_opy_ (u"ࠨࡅࡤࡹ࡬࡮ࡴࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠨ෺").format(str(e)))
          for driver in bstack1l11l11l1_opy_:
            bstack1llllll1l1_opy_.append({
              bstack1111l1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ෻"): bstack1l111l1ll1_opy_[bstack1111l1l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭෼")],
              bstack1111l1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ෽"): str(e),
              bstack1111l1l_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ෾"): multiprocessing.current_process().name
            })
            bstack1l11111l1l_opy_(driver, bstack1111l1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭෿"), bstack1111l1l_opy_ (u"ࠢࡔࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥ฀") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1l11l11l1_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack111lll111_opy_, CONFIG, logger)
      bstack11l1lll111_opy_()
      bstack1ll11l1ll_opy_()
      percy.bstack11l1ll11_opy_()
      bstack1l111l1l1l_opy_ = {
        bstack1111l1l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫก"): args[0],
        bstack1111l1l_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩข"): CONFIG,
        bstack1111l1l_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫฃ"): bstack1l111l1ll_opy_,
        bstack1111l1l_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ค"): bstack111lll111_opy_
      }
      if bstack1111l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨฅ") in CONFIG:
        bstack1111llll_opy_ = bstack11lll111_opy_(args, logger, CONFIG, bstack11111l11l_opy_, bstack1l1l1ll1l1_opy_)
        bstack11l1lllll_opy_ = bstack1111llll_opy_.bstack11l1l1ll_opy_(run_on_browserstack, bstack1l111l1l1l_opy_, bstack1111l1111_opy_(args))
      else:
        if bstack1111l1111_opy_(args):
          bstack1l111l1l1l_opy_[bstack1111l1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩฆ")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1l111l1l1l_opy_,))
          test.start()
          test.join()
        else:
          bstack1l11l1ll11_opy_(bstack1ll1lll1l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1111l1l_opy_ (u"ࠧࡠࡡࡱࡥࡲ࡫࡟ࡠࠩง")] = bstack1111l1l_opy_ (u"ࠨࡡࡢࡱࡦ࡯࡮ࡠࡡࠪจ")
          mod_globals[bstack1111l1l_opy_ (u"ࠩࡢࡣ࡫࡯࡬ࡦࡡࡢࠫฉ")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1l1lllllll_opy_ == bstack1111l1l_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩช") or bstack1l1lllllll_opy_ == bstack1111l1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪซ"):
    percy.init(bstack111lll111_opy_, CONFIG, logger)
    percy.bstack11l1ll11_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack11l1111ll1_opy_(e, bstack11ll11111l_opy_)
    bstack11l1lll111_opy_()
    bstack1l11l1ll11_opy_(bstack11l1l1l111_opy_)
    if bstack11111l11l_opy_:
      bstack1ll111l1l_opy_(bstack11l1l1l111_opy_, args)
      if bstack1111l1l_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪฌ") in args:
        i = args.index(bstack1111l1l_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫญ"))
        args.pop(i)
        args.pop(i)
      if bstack1111l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪฎ") not in CONFIG:
        CONFIG[bstack1111l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫฏ")] = [{}]
        bstack1l1l1ll1l1_opy_ = 1
      if bstack1l11l11111_opy_ == 0:
        bstack1l11l11111_opy_ = 1
      args.insert(0, str(bstack1l11l11111_opy_))
      args.insert(0, str(bstack1111l1l_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧฐ")))
    if bstack11l1lllll1_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack11l111ll1_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1ll1l1l11_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack1111l1l_opy_ (u"ࠥࡖࡔࡈࡏࡕࡡࡒࡔ࡙ࡏࡏࡏࡕࠥฑ"),
        ).parse_args(bstack11l111ll1_opy_)
        bstack1lllll111_opy_ = args.index(bstack11l111ll1_opy_[0]) if len(bstack11l111ll1_opy_) > 0 else len(args)
        args.insert(bstack1lllll111_opy_, str(bstack1111l1l_opy_ (u"ࠫ࠲࠳࡬ࡪࡵࡷࡩࡳ࡫ࡲࠨฒ")))
        args.insert(bstack1lllll111_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1111l1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡸ࡯ࡣࡱࡷࡣࡱ࡯ࡳࡵࡧࡱࡩࡷ࠴ࡰࡺࠩณ"))))
        if bstack111l1llll_opy_.bstack11111ll1l_opy_(CONFIG):
          args.insert(bstack1lllll111_opy_, str(bstack1111l1l_opy_ (u"࠭࠭࠮࡮࡬ࡷࡹ࡫࡮ࡦࡴࠪด")))
          args.insert(bstack1lllll111_opy_ + 1, str(bstack1111l1l_opy_ (u"ࠧࡓࡧࡷࡶࡾࡌࡡࡪ࡮ࡨࡨ࠿ࢁࡽࠨต").format(bstack111l1llll_opy_.bstack1l1ll1llll_opy_(CONFIG))))
        if bstack1lll1l11l_opy_(os.environ.get(bstack1111l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓ࠭ถ"))) and str(os.environ.get(bstack1111l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭ท"), bstack1111l1l_opy_ (u"ࠪࡲࡺࡲ࡬ࠨธ"))) != bstack1111l1l_opy_ (u"ࠫࡳࡻ࡬࡭ࠩน"):
          for bstack1l11l1l11l_opy_ in bstack1ll1l1l11_opy_:
            args.remove(bstack1l11l1l11l_opy_)
          test_files = os.environ.get(bstack1111l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠩบ")).split(bstack1111l1l_opy_ (u"࠭ࠬࠨป"))
          for bstack11l11ll11l_opy_ in test_files:
            args.append(bstack11l11ll11l_opy_)
      except Exception as e:
        logger.error(bstack1111l1l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡧࡴࡵࡣࡦ࡬࡮ࡴࡧࠡ࡮࡬ࡷࡹ࡫࡮ࡦࡴࠣࡪࡴࡸࠠࡼࡿ࠱ࠤࡊࡸࡲࡰࡴࠣ࠱ࠥࢁࡽࠣผ").format(bstack11l1l1111l_opy_, e))
    pabot.main(args)
  elif bstack1l1lllllll_opy_ == bstack1111l1l_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩฝ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack11l1111ll1_opy_(e, bstack11ll11111l_opy_)
    for a in args:
      if bstack1111l1l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘࠨพ") in a:
        bstack1l1ll11lll_opy_ = int(a.split(bstack1111l1l_opy_ (u"ࠪ࠾ࠬฟ"))[1])
      if bstack1111l1l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨภ") in a:
        bstack1lll1ll11_opy_ = str(a.split(bstack1111l1l_opy_ (u"ࠬࡀࠧม"))[1])
      if bstack1111l1l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘ࠭ย") in a:
        bstack1lllll111l_opy_ = str(a.split(bstack1111l1l_opy_ (u"ࠧ࠻ࠩร"))[1])
    bstack1lllll1111_opy_ = None
    if bstack1111l1l_opy_ (u"ࠨ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠧฤ") in args:
      i = args.index(bstack1111l1l_opy_ (u"ࠩ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠨล"))
      args.pop(i)
      bstack1lllll1111_opy_ = args.pop(i)
    if bstack1lllll1111_opy_ is not None:
      global bstack1l1ll1lll1_opy_
      bstack1l1ll1lll1_opy_ = bstack1lllll1111_opy_
    bstack1l11l1ll11_opy_(bstack11l1l1l111_opy_)
    run_cli(args)
    if bstack1111l1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺࠧฦ") in multiprocessing.current_process().__dict__.keys():
      for bstack11l1ll1l_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1llllll1l1_opy_.append(bstack11l1ll1l_opy_)
  elif bstack1l1lllllll_opy_ == bstack1111l1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫว"):
    bstack1l11l1l1l1_opy_ = bstack11l1ll1ll1_opy_(args, logger, CONFIG, bstack11111l11l_opy_)
    bstack1l11l1l1l1_opy_.bstack11lll1llll_opy_()
    bstack11l1lll111_opy_()
    bstack11l11l11ll_opy_ = True
    bstack1l1l1ll111_opy_ = bstack1l11l1l1l1_opy_.bstack11lll1ll1_opy_()
    bstack1l11l1l1l1_opy_.bstack11l1l111l1_opy_()
    bstack1l11l1l1l1_opy_.bstack1l111l1l1l_opy_(bstack11ll1l1ll_opy_)
    bstack1111l111_opy_(bstack1l1lllllll_opy_, CONFIG, bstack1l11l1l1l1_opy_.bstack1lll11ll_opy_())
    bstack1l1111lll_opy_ = bstack1l11l1l1l1_opy_.bstack11l1l1ll_opy_(bstack1llll111l_opy_, {
      bstack1111l1l_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭ศ"): bstack1l111l1ll_opy_,
      bstack1111l1l_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨษ"): bstack111lll111_opy_,
      bstack1111l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪส"): bstack11111l11l_opy_
    })
    try:
      bstack11l1l111_opy_, bstack1l1l1ll11l_opy_ = map(list, zip(*bstack1l1111lll_opy_))
      bstack1lllll11_opy_ = bstack11l1l111_opy_[0]
      for status_code in bstack1l1l1ll11l_opy_:
        if status_code != 0:
          bstack111ll11ll_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack1111l1l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡧࡶࡦࠢࡨࡶࡷࡵࡲࡴࠢࡤࡲࡩࠦࡳࡵࡣࡷࡹࡸࠦࡣࡰࡦࡨ࠲ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࠼ࠣࡿࢂࠨห").format(str(e)))
  elif bstack1l1lllllll_opy_ == bstack1111l1l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩฬ"):
    try:
      from behave.__main__ import main as bstack11l1ll1ll_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack11l1111ll1_opy_(e, bstack1l1l1lllll_opy_)
    bstack11l1lll111_opy_()
    bstack11l11l11ll_opy_ = True
    bstack11l11ll11_opy_ = 1
    if bstack1111l1l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪอ") in CONFIG:
      bstack11l11ll11_opy_ = CONFIG[bstack1111l1l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫฮ")]
    if bstack1111l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨฯ") in CONFIG:
      bstack1llll1ll1l_opy_ = int(bstack11l11ll11_opy_) * int(len(CONFIG[bstack1111l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩะ")]))
    else:
      bstack1llll1ll1l_opy_ = int(bstack11l11ll11_opy_)
    config = Configuration(args)
    bstack1l1lll11l1_opy_ = config.paths
    if len(bstack1l1lll11l1_opy_) == 0:
      import glob
      pattern = bstack1111l1l_opy_ (u"ࠧࠫࠬ࠲࠮࠳࡬ࡥࡢࡶࡸࡶࡪ࠭ั")
      bstack1l1l111lll_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1l1l111lll_opy_)
      config = Configuration(args)
      bstack1l1lll11l1_opy_ = config.paths
    bstack1l11ll1111_opy_ = [os.path.normpath(item) for item in bstack1l1lll11l1_opy_]
    bstack11l11ll111_opy_ = [os.path.normpath(item) for item in args]
    bstack11l111l1l1_opy_ = [item for item in bstack11l11ll111_opy_ if item not in bstack1l11ll1111_opy_]
    import platform as pf
    if pf.system().lower() == bstack1111l1l_opy_ (u"ࠨࡹ࡬ࡲࡩࡵࡷࡴࠩา"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1l11ll1111_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l11lll11l_opy_)))
                    for bstack1l11lll11l_opy_ in bstack1l11ll1111_opy_]
    bstack1lll1l1l11_opy_ = []
    for spec in bstack1l11ll1111_opy_:
      bstack1lll1llll_opy_ = []
      bstack1lll1llll_opy_ += bstack11l111l1l1_opy_
      bstack1lll1llll_opy_.append(spec)
      bstack1lll1l1l11_opy_.append(bstack1lll1llll_opy_)
    execution_items = []
    for bstack1lll1llll_opy_ in bstack1lll1l1l11_opy_:
      if bstack1111l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬำ") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack1111l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ิ")]):
          item = {}
          item[bstack1111l1l_opy_ (u"ࠫࡦࡸࡧࠨี")] = bstack1111l1l_opy_ (u"ࠬࠦࠧึ").join(bstack1lll1llll_opy_)
          item[bstack1111l1l_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬื")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack1111l1l_opy_ (u"ࠧࡢࡴࡪุࠫ")] = bstack1111l1l_opy_ (u"ࠨูࠢࠪ").join(bstack1lll1llll_opy_)
        item[bstack1111l1l_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨฺ")] = 0
        execution_items.append(item)
    bstack1111lll1l_opy_ = bstack11lll1l1l1_opy_(execution_items, bstack1llll1ll1l_opy_)
    for execution_item in bstack1111lll1l_opy_:
      bstack11l1l1l1l1_opy_ = []
      for item in execution_item:
        bstack11l1l1l1l1_opy_.append(bstack111l1111l_opy_(name=str(item[bstack1111l1l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ฻")]),
                                             target=bstack1l111ll1l1_opy_,
                                             args=(item[bstack1111l1l_opy_ (u"ࠫࡦࡸࡧࠨ฼")],)))
      for t in bstack11l1l1l1l1_opy_:
        t.start()
      for t in bstack11l1l1l1l1_opy_:
        t.join()
  else:
    bstack1111ll1l1_opy_(bstack1l1l1lll11_opy_)
  if not bstack1l111l1ll1_opy_:
    bstack1ll11111l_opy_()
    if(bstack1l1lllllll_opy_ in [bstack1111l1l_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ฽"), bstack1111l1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭฾")]):
      bstack1l111ll111_opy_()
  bstack11l1111l1_opy_.bstack1l11ll1l11_opy_()
def browserstack_initialize(bstack1llll1ll11_opy_=None):
  logger.info(bstack1111l1l_opy_ (u"ࠧࡓࡷࡱࡲ࡮ࡴࡧࠡࡕࡇࡏࠥࡽࡩࡵࡪࠣࡥࡷ࡭ࡳ࠻ࠢࠪ฿") + str(bstack1llll1ll11_opy_))
  run_on_browserstack(bstack1llll1ll11_opy_, None, True)
@measure(event_name=EVENTS.bstack111lllll1_opy_, stage=STAGE.bstack1l1111l1ll_opy_, bstack1ll1l1ll_opy_=bstack1lllllllll_opy_)
def bstack1ll11111l_opy_():
  global CONFIG
  global bstack1lll1l1l1l_opy_
  global bstack111ll11ll_opy_
  global bstack1l1llllll1_opy_
  global bstack1l1ll11l1_opy_
  bstack1llllllll_opy_.bstack11l111l1ll_opy_()
  if cli.is_running():
    bstack11lllll1ll_opy_.invoke(bstack1l111l1111_opy_.bstack1l11111ll1_opy_)
  else:
    bstack11llllll_opy_ = bstack111l1llll_opy_.bstack1l11llll1_opy_(config=CONFIG)
    bstack11llllll_opy_.bstack1l1l1l11l1_opy_(CONFIG)
  if bstack1lll1l1l1l_opy_ == bstack1111l1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨเ"):
    if not cli.is_enabled(CONFIG):
      bstack11l1lllll1_opy_.stop()
  else:
    bstack11l1lllll1_opy_.stop()
  if not cli.is_enabled(CONFIG):
    bstack1ll11lll1_opy_.bstack1ll1l1l11l_opy_()
  if bstack1111l1l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭แ") in CONFIG and str(CONFIG[bstack1111l1l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧโ")]).lower() != bstack1111l1l_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪใ"):
    hashed_id, bstack11ll1l111l_opy_ = bstack111l11111_opy_()
  else:
    hashed_id, bstack11ll1l111l_opy_ = get_build_link()
  bstack1ll11l1l1l_opy_(hashed_id)
  logger.info(bstack1111l1l_opy_ (u"࡙ࠬࡄࡌࠢࡵࡹࡳࠦࡥ࡯ࡦࡨࡨࠥ࡬࡯ࡳࠢ࡬ࡨ࠿࠭ไ") + bstack1l1ll11l1_opy_.get_property(bstack1111l1l_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨๅ"), bstack1111l1l_opy_ (u"ࠧࠨๆ")) + bstack1111l1l_opy_ (u"ࠨ࠮ࠣࡸࡪࡹࡴࡩࡷࡥࠤ࡮ࡪ࠺ࠡࠩ็") + os.getenv(bstack1111l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊ่ࠧ"), bstack1111l1l_opy_ (u"้ࠪࠫ")))
  if hashed_id is not None and bstack1l11l1111_opy_() != -1:
    sessions = bstack1llll1111l_opy_(hashed_id)
    bstack1l111llll_opy_(sessions, bstack11ll1l111l_opy_)
  if bstack1lll1l1l1l_opy_ == bstack1111l1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ๊ࠫ") and bstack111ll11ll_opy_ != 0:
    sys.exit(bstack111ll11ll_opy_)
  if bstack1lll1l1l1l_opy_ == bstack1111l1l_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩ๋ࠬ") and bstack1l1llllll1_opy_ != 0:
    sys.exit(bstack1l1llllll1_opy_)
def bstack1ll11l1l1l_opy_(new_id):
    global bstack1ll11ll111_opy_
    bstack1ll11ll111_opy_ = new_id
def bstack1lllllll11_opy_(bstack11l1l11l_opy_):
  if bstack11l1l11l_opy_:
    return bstack11l1l11l_opy_.capitalize()
  else:
    return bstack1111l1l_opy_ (u"࠭ࠧ์")
@measure(event_name=EVENTS.bstack1111lll1_opy_, stage=STAGE.bstack1l1111l1ll_opy_, bstack1ll1l1ll_opy_=bstack1lllllllll_opy_)
def bstack1l11l1l1ll_opy_(bstack11ll111l_opy_):
  if bstack1111l1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬํ") in bstack11ll111l_opy_ and bstack11ll111l_opy_[bstack1111l1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭๎")] != bstack1111l1l_opy_ (u"ࠩࠪ๏"):
    return bstack11ll111l_opy_[bstack1111l1l_opy_ (u"ࠪࡲࡦࡳࡥࠨ๐")]
  else:
    bstack1ll1l1ll_opy_ = bstack1111l1l_opy_ (u"ࠦࠧ๑")
    if bstack1111l1l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬ๒") in bstack11ll111l_opy_ and bstack11ll111l_opy_[bstack1111l1l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭๓")] != None:
      bstack1ll1l1ll_opy_ += bstack11ll111l_opy_[bstack1111l1l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ๔")] + bstack1111l1l_opy_ (u"ࠣ࠮ࠣࠦ๕")
      if bstack11ll111l_opy_[bstack1111l1l_opy_ (u"ࠩࡲࡷࠬ๖")] == bstack1111l1l_opy_ (u"ࠥ࡭ࡴࡹࠢ๗"):
        bstack1ll1l1ll_opy_ += bstack1111l1l_opy_ (u"ࠦ࡮ࡕࡓࠡࠤ๘")
      bstack1ll1l1ll_opy_ += (bstack11ll111l_opy_[bstack1111l1l_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ๙")] or bstack1111l1l_opy_ (u"࠭ࠧ๚"))
      return bstack1ll1l1ll_opy_
    else:
      bstack1ll1l1ll_opy_ += bstack1lllllll11_opy_(bstack11ll111l_opy_[bstack1111l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ๛")]) + bstack1111l1l_opy_ (u"ࠣࠢࠥ๜") + (
              bstack11ll111l_opy_[bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫ๝")] or bstack1111l1l_opy_ (u"ࠪࠫ๞")) + bstack1111l1l_opy_ (u"ࠦ࠱ࠦࠢ๟")
      if bstack11ll111l_opy_[bstack1111l1l_opy_ (u"ࠬࡵࡳࠨ๠")] == bstack1111l1l_opy_ (u"ࠨࡗࡪࡰࡧࡳࡼࡹࠢ๡"):
        bstack1ll1l1ll_opy_ += bstack1111l1l_opy_ (u"ࠢࡘ࡫ࡱࠤࠧ๢")
      bstack1ll1l1ll_opy_ += bstack11ll111l_opy_[bstack1111l1l_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ๣")] or bstack1111l1l_opy_ (u"ࠩࠪ๤")
      return bstack1ll1l1ll_opy_
@measure(event_name=EVENTS.bstack1ll1l1ll1l_opy_, stage=STAGE.bstack1l1111l1ll_opy_, bstack1ll1l1ll_opy_=bstack1lllllllll_opy_)
def bstack11l11l1l_opy_(bstack111ll11l_opy_):
  if bstack111ll11l_opy_ == bstack1111l1l_opy_ (u"ࠥࡨࡴࡴࡥࠣ๥"):
    return bstack1111l1l_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡧࡳࡧࡨࡲࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡧࡳࡧࡨࡲࠧࡄࡃࡰ࡯ࡳࡰࡪࡺࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ๦")
  elif bstack111ll11l_opy_ == bstack1111l1l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ๧"):
    return bstack1111l1l_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡴࡨࡨࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡲࡦࡦࠥࡂࡋࡧࡩ࡭ࡧࡧࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩ๨")
  elif bstack111ll11l_opy_ == bstack1111l1l_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ๩"):
    return bstack1111l1l_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽࡫ࡷ࡫ࡥ࡯࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥ࡫ࡷ࡫ࡥ࡯ࠤࡁࡔࡦࡹࡳࡦࡦ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨ๪")
  elif bstack111ll11l_opy_ == bstack1111l1l_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣ๫"):
    return bstack1111l1l_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡸࡥࡥ࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡶࡪࡪࠢ࠿ࡇࡵࡶࡴࡸ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ๬")
  elif bstack111ll11l_opy_ == bstack1111l1l_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࠧ๭"):
    return bstack1111l1l_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࠤࡧࡨࡥ࠸࠸࠶࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࠦࡩࡪࡧ࠳࠳࠸ࠥࡂ࡙࡯࡭ࡦࡱࡸࡸࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪ๮")
  elif bstack111ll11l_opy_ == bstack1111l1l_opy_ (u"ࠨࡲࡶࡰࡱ࡭ࡳ࡭ࠢ๯"):
    return bstack1111l1l_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡥࡰࡦࡩ࡫࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡥࡰࡦࡩ࡫ࠣࡀࡕࡹࡳࡴࡩ࡯ࡩ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨ๰")
  else:
    return bstack1111l1l_opy_ (u"ࠨ࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡧࡲࡡࡤ࡭࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡧࡲࡡࡤ࡭ࠥࡂࠬ๱") + bstack1lllllll11_opy_(
      bstack111ll11l_opy_) + bstack1111l1l_opy_ (u"ࠩ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨ๲")
def bstack11ll1lll_opy_(session):
  return bstack1111l1l_opy_ (u"ࠪࡀࡹࡸࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡳࡱࡺࠦࡃࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠠࡴࡧࡶࡷ࡮ࡵ࡮࠮ࡰࡤࡱࡪࠨ࠾࠽ࡣࠣ࡬ࡷ࡫ࡦ࠾ࠤࡾࢁࠧࠦࡴࡢࡴࡪࡩࡹࡃࠢࡠࡤ࡯ࡥࡳࡱࠢ࠿ࡽࢀࡀ࠴ࡧ࠾࠽࠱ࡷࡨࡃࢁࡽࡼࡿ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁ࠵ࡴࡳࡀࠪ๳").format(
    session[bstack1111l1l_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦࡣࡺࡸ࡬ࠨ๴")], bstack1l11l1l1ll_opy_(session), bstack11l11l1l_opy_(session[bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡸࡺࡡࡵࡷࡶࠫ๵")]),
    bstack11l11l1l_opy_(session[bstack1111l1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭๶")]),
    bstack1lllllll11_opy_(session[bstack1111l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ๷")] or session[bstack1111l1l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨ๸")] or bstack1111l1l_opy_ (u"ࠩࠪ๹")) + bstack1111l1l_opy_ (u"ࠥࠤࠧ๺") + (session[bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭๻")] or bstack1111l1l_opy_ (u"ࠬ࠭๼")),
    session[bstack1111l1l_opy_ (u"࠭࡯ࡴࠩ๽")] + bstack1111l1l_opy_ (u"ࠢࠡࠤ๾") + session[bstack1111l1l_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ๿")], session[bstack1111l1l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫ຀")] or bstack1111l1l_opy_ (u"ࠪࠫກ"),
    session[bstack1111l1l_opy_ (u"ࠫࡨࡸࡥࡢࡶࡨࡨࡤࡧࡴࠨຂ")] if session[bstack1111l1l_opy_ (u"ࠬࡩࡲࡦࡣࡷࡩࡩࡥࡡࡵࠩ຃")] else bstack1111l1l_opy_ (u"࠭ࠧຄ"))
@measure(event_name=EVENTS.bstack1llll1llll_opy_, stage=STAGE.bstack1l1111l1ll_opy_, bstack1ll1l1ll_opy_=bstack1lllllllll_opy_)
def bstack1l111llll_opy_(sessions, bstack11ll1l111l_opy_):
  try:
    bstack1ll111111_opy_ = bstack1111l1l_opy_ (u"ࠢࠣ຅")
    if not os.path.exists(bstack1ll11l1ll1_opy_):
      os.mkdir(bstack1ll11l1ll1_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1111l1l_opy_ (u"ࠨࡣࡶࡷࡪࡺࡳ࠰ࡴࡨࡴࡴࡸࡴ࠯ࡪࡷࡱࡱ࠭ຆ")), bstack1111l1l_opy_ (u"ࠩࡵࠫງ")) as f:
      bstack1ll111111_opy_ = f.read()
    bstack1ll111111_opy_ = bstack1ll111111_opy_.replace(bstack1111l1l_opy_ (u"ࠪࡿࠪࡘࡅࡔࡗࡏࡘࡘࡥࡃࡐࡗࡑࡘࠪࢃࠧຈ"), str(len(sessions)))
    bstack1ll111111_opy_ = bstack1ll111111_opy_.replace(bstack1111l1l_opy_ (u"ࠫࢀࠫࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠧࢀࠫຉ"), bstack11ll1l111l_opy_)
    bstack1ll111111_opy_ = bstack1ll111111_opy_.replace(bstack1111l1l_opy_ (u"ࠬࢁࠥࡃࡗࡌࡐࡉࡥࡎࡂࡏࡈࠩࢂ࠭ຊ"),
                                              sessions[0].get(bstack1111l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡴࡡ࡮ࡧࠪ຋")) if sessions[0] else bstack1111l1l_opy_ (u"ࠧࠨຌ"))
    with open(os.path.join(bstack1ll11l1ll1_opy_, bstack1111l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡳࡧࡳࡳࡷࡺ࠮ࡩࡶࡰࡰࠬຍ")), bstack1111l1l_opy_ (u"ࠩࡺࠫຎ")) as stream:
      stream.write(bstack1ll111111_opy_.split(bstack1111l1l_opy_ (u"ࠪࡿ࡙ࠪࡅࡔࡕࡌࡓࡓ࡙࡟ࡅࡃࡗࡅࠪࢃࠧຏ"))[0])
      for session in sessions:
        stream.write(bstack11ll1lll_opy_(session))
      stream.write(bstack1ll111111_opy_.split(bstack1111l1l_opy_ (u"ࠫࢀࠫࡓࡆࡕࡖࡍࡔࡔࡓࡠࡆࡄࡘࡆࠫࡽࠨຐ"))[1])
    logger.info(bstack1111l1l_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡫ࡤࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡣࡷ࡬ࡰࡩࠦࡡࡳࡶ࡬ࡪࡦࡩࡴࡴࠢࡤࡸࠥࢁࡽࠨຑ").format(bstack1ll11l1ll1_opy_));
  except Exception as e:
    logger.debug(bstack111lll1lll_opy_.format(str(e)))
def bstack1llll1111l_opy_(hashed_id):
  global CONFIG
  try:
    bstack1ll1l1lll_opy_ = datetime.datetime.now()
    host = bstack1111l1l_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡲ࡬࠱ࡨࡲ࡯ࡶࡦ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ຒ") if bstack1111l1l_opy_ (u"ࠧࡢࡲࡳࠫຓ") in CONFIG else bstack1111l1l_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩດ")
    user = CONFIG[bstack1111l1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫຕ")]
    key = CONFIG[bstack1111l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ຖ")]
    bstack1ll1l11ll1_opy_ = bstack1111l1l_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪທ") if bstack1111l1l_opy_ (u"ࠬࡧࡰࡱࠩຘ") in CONFIG else (bstack1111l1l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪນ") if CONFIG.get(bstack1111l1l_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫບ")) else bstack1111l1l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪປ"))
    host = bstack1l11lll111_opy_(cli.config, [bstack1111l1l_opy_ (u"ࠤࡤࡴ࡮ࡹࠢຜ"), bstack1111l1l_opy_ (u"ࠥࡥࡵࡶࡁࡶࡶࡲࡱࡦࡺࡥࠣຝ"), bstack1111l1l_opy_ (u"ࠦࡦࡶࡩࠣພ")], host) if bstack1111l1l_opy_ (u"ࠬࡧࡰࡱࠩຟ") in CONFIG else bstack1l11lll111_opy_(cli.config, [bstack1111l1l_opy_ (u"ࠨࡡࡱ࡫ࡶࠦຠ"), bstack1111l1l_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡦࠤມ"), bstack1111l1l_opy_ (u"ࠣࡣࡳ࡭ࠧຢ")], host)
    url = bstack1111l1l_opy_ (u"ࠩࡾࢁ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀ࠳ࡸ࡫ࡳࡴ࡫ࡲࡲࡸ࠴ࡪࡴࡱࡱࠫຣ").format(host, bstack1ll1l11ll1_opy_, hashed_id)
    headers = {
      bstack1111l1l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩ຤"): bstack1111l1l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧລ"),
    }
    proxies = bstack11l1l111ll_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies, auth=(user, key))
    if response.json():
      cli.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࡫ࡪࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࡡ࡯࡭ࡸࡺࠢ຦"), datetime.datetime.now() - bstack1ll1l1lll_opy_)
      return list(map(lambda session: session[bstack1111l1l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࠫວ")], response.json()))
  except Exception as e:
    logger.debug(bstack1ll111llll_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack1ll1l1ll11_opy_, stage=STAGE.bstack1l1111l1ll_opy_, bstack1ll1l1ll_opy_=bstack1lllllllll_opy_)
def get_build_link():
  global CONFIG
  global bstack1ll11ll111_opy_
  try:
    if bstack1111l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪຨ") in CONFIG:
      bstack1ll1l1lll_opy_ = datetime.datetime.now()
      host = bstack1111l1l_opy_ (u"ࠨࡣࡳ࡭࠲ࡩ࡬ࡰࡷࡧࠫຩ") if bstack1111l1l_opy_ (u"ࠩࡤࡴࡵ࠭ສ") in CONFIG else bstack1111l1l_opy_ (u"ࠪࡥࡵ࡯ࠧຫ")
      user = CONFIG[bstack1111l1l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ຬ")]
      key = CONFIG[bstack1111l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨອ")]
      bstack1ll1l11ll1_opy_ = bstack1111l1l_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬຮ") if bstack1111l1l_opy_ (u"ࠧࡢࡲࡳࠫຯ") in CONFIG else bstack1111l1l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪະ")
      url = bstack1111l1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡾࢁ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀ࠳ࡧࡻࡩ࡭ࡦࡶ࠲࡯ࡹ࡯࡯ࠩັ").format(user, key, host, bstack1ll1l11ll1_opy_)
      if cli.is_enabled(CONFIG):
        bstack11ll1l111l_opy_, hashed_id = cli.bstack1l1l11l111_opy_()
        logger.info(bstack1l1llll1l_opy_.format(bstack11ll1l111l_opy_))
        return [hashed_id, bstack11ll1l111l_opy_]
      else:
        headers = {
          bstack1111l1l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩາ"): bstack1111l1l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧຳ"),
        }
        if bstack1111l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧິ") in CONFIG:
          params = {bstack1111l1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫີ"): CONFIG[bstack1111l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪຶ")], bstack1111l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫື"): CONFIG[bstack1111l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵຸࠫ")]}
        else:
          params = {bstack1111l1l_opy_ (u"ࠪࡲࡦࡳࡥࠨູ"): CONFIG[bstack1111l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫຺ࠧ")]}
        proxies = bstack11l1l111ll_opy_(CONFIG, url)
        response = requests.get(url, params=params, headers=headers, proxies=proxies)
        if response.json():
          bstack11l1111lll_opy_ = response.json()[0][bstack1111l1l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡥࡹ࡮ࡲࡤࠨົ")]
          if bstack11l1111lll_opy_:
            bstack11ll1l111l_opy_ = bstack11l1111lll_opy_[bstack1111l1l_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨࡥࡵࡳ࡮ࠪຼ")].split(bstack1111l1l_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࠭ࡣࡷ࡬ࡰࡩ࠭ຽ"))[0] + bstack1111l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡳ࠰ࠩ຾") + bstack11l1111lll_opy_[
              bstack1111l1l_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ຿")]
            logger.info(bstack1l1llll1l_opy_.format(bstack11ll1l111l_opy_))
            bstack1ll11ll111_opy_ = bstack11l1111lll_opy_[bstack1111l1l_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ເ")]
            bstack1ll11l11ll_opy_ = CONFIG[bstack1111l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧແ")]
            if bstack1111l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧໂ") in CONFIG:
              bstack1ll11l11ll_opy_ += bstack1111l1l_opy_ (u"࠭ࠠࠨໃ") + CONFIG[bstack1111l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩໄ")]
            if bstack1ll11l11ll_opy_ != bstack11l1111lll_opy_[bstack1111l1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭໅")]:
              logger.debug(bstack1l11ll111l_opy_.format(bstack11l1111lll_opy_[bstack1111l1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧໆ")], bstack1ll11l11ll_opy_))
            cli.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻ࡩࡨࡸࡤࡨࡵࡪ࡮ࡧࡣࡱ࡯࡮࡬ࠤ໇"), datetime.datetime.now() - bstack1ll1l1lll_opy_)
            return [bstack11l1111lll_opy_[bstack1111l1l_opy_ (u"ࠫ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪ່ࠧ")], bstack11ll1l111l_opy_]
    else:
      logger.warn(bstack1111l11l_opy_)
  except Exception as e:
    logger.debug(bstack1llll1l111_opy_.format(str(e)))
  return [None, None]
def bstack1l1l1111l1_opy_(url, bstack111llll1_opy_=False):
  global CONFIG
  global bstack1ll1l11l1l_opy_
  if not bstack1ll1l11l1l_opy_:
    hostname = bstack1l1ll111ll_opy_(url)
    is_private = bstack1l1ll111l_opy_(hostname)
    if (bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭້ࠩ") in CONFIG and not bstack1lll1l11l_opy_(CONFIG[bstack1111l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮໊ࠪ")])) and (is_private or bstack111llll1_opy_):
      bstack1ll1l11l1l_opy_ = hostname
def bstack1l1ll111ll_opy_(url):
  return urlparse(url).hostname
def bstack1l1ll111l_opy_(hostname):
  for bstack11ll1ll111_opy_ in bstack11ll11ll1l_opy_:
    regex = re.compile(bstack11ll1ll111_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack111111l11_opy_(bstack11l11l1ll1_opy_):
  return True if bstack11l11l1ll1_opy_ in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack1l1l11ll1l_opy_, stage=STAGE.bstack1l1111l1ll_opy_, bstack1ll1l1ll_opy_=bstack1lllllllll_opy_)
def getAccessibilityResults(driver):
  global CONFIG
  global bstack1l1ll11lll_opy_
  bstack11l111l11l_opy_ = not (bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷ໋ࠫ"), None) and bstack1l11l1lll_opy_(
          threading.current_thread(), bstack1111l1l_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ໌"), None))
  bstack1lll1111ll_opy_ = getattr(driver, bstack1111l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩໍ"), None) != True
  bstack1l1ll1lll_opy_ = bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ໎"), None) and bstack1l11l1lll_opy_(
          threading.current_thread(), bstack1111l1l_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭໏"), None)
  if bstack1l1ll1lll_opy_:
    if not bstack1l1l11111_opy_():
      logger.warning(bstack1111l1l_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡰࡱࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡅࡵࡶࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳ࠯ࠤ໐"))
      return {}
    logger.debug(bstack1111l1l_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪ໑"))
    logger.debug(perform_scan(driver, driver_command=bstack1111l1l_opy_ (u"ࠧࡦࡺࡨࡧࡺࡺࡥࡔࡥࡵ࡭ࡵࡺࠧ໒")))
    results = bstack1lll1lll1l_opy_(bstack1111l1l_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࡴࠤ໓"))
    if results is not None and results.get(bstack1111l1l_opy_ (u"ࠤ࡬ࡷࡸࡻࡥࡴࠤ໔")) is not None:
        return results[bstack1111l1l_opy_ (u"ࠥ࡭ࡸࡹࡵࡦࡵࠥ໕")]
    logger.error(bstack1111l1l_opy_ (u"ࠦࡓࡵࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡓࡧࡶࡹࡱࡺࡳࠡࡹࡨࡶࡪࠦࡦࡰࡷࡱࡨ࠳ࠨ໖"))
    return []
  if not bstack1lll1111l1_opy_.bstack1llll1l1l_opy_(CONFIG, bstack1l1ll11lll_opy_) or (bstack1lll1111ll_opy_ and bstack11l111l11l_opy_):
    logger.warning(bstack1111l1l_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹ࠮ࠣ໗"))
    return {}
  try:
    logger.debug(bstack1111l1l_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪ໘"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack1ll1ll1ll1_opy_.bstack111l11ll1_opy_)
    return results
  except Exception:
    logger.error(bstack1111l1l_opy_ (u"ࠢࡏࡱࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡼ࡫ࡲࡦࠢࡩࡳࡺࡴࡤ࠯ࠤ໙"))
    return {}
@measure(event_name=EVENTS.bstack1l11l111ll_opy_, stage=STAGE.bstack1l1111l1ll_opy_, bstack1ll1l1ll_opy_=bstack1lllllllll_opy_)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack1l1ll11lll_opy_
  bstack11l111l11l_opy_ = not (bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬ໚"), None) and bstack1l11l1lll_opy_(
          threading.current_thread(), bstack1111l1l_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ໛"), None))
  bstack1lll1111ll_opy_ = getattr(driver, bstack1111l1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪໜ"), None) != True
  bstack1l1ll1lll_opy_ = bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫໝ"), None) and bstack1l11l1lll_opy_(
          threading.current_thread(), bstack1111l1l_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧໞ"), None)
  if bstack1l1ll1lll_opy_:
    if not bstack1l1l11111_opy_():
      logger.warning(bstack1111l1l_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡆࡶࡰࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡶࡹࡲࡳࡡࡳࡻ࠱ࠦໟ"))
      return {}
    logger.debug(bstack1111l1l_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡸࡻ࡭࡮ࡣࡵࡽࠬ໠"))
    logger.debug(perform_scan(driver, driver_command=bstack1111l1l_opy_ (u"ࠨࡧࡻࡩࡨࡻࡴࡦࡕࡦࡶ࡮ࡶࡴࠨ໡")))
    results = bstack1lll1lll1l_opy_(bstack1111l1l_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡕࡸࡱࡲࡧࡲࡺࠤ໢"))
    if results is not None and results.get(bstack1111l1l_opy_ (u"ࠥࡷࡺࡳ࡭ࡢࡴࡼࠦ໣")) is not None:
        return results[bstack1111l1l_opy_ (u"ࠦࡸࡻ࡭࡮ࡣࡵࡽࠧ໤")]
    logger.error(bstack1111l1l_opy_ (u"ࠧࡔ࡯ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡔࡨࡷࡺࡲࡴࡴࠢࡖࡹࡲࡳࡡࡳࡻࠣࡻࡦࡹࠠࡧࡱࡸࡲࡩ࠴ࠢ໥"))
    return {}
  if not bstack1lll1111l1_opy_.bstack1llll1l1l_opy_(CONFIG, bstack1l1ll11lll_opy_) or (bstack1lll1111ll_opy_ and bstack11l111l11l_opy_):
    logger.warning(bstack1111l1l_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡵࡸࡱࡲࡧࡲࡺ࠰ࠥ໦"))
    return {}
  try:
    logger.debug(bstack1111l1l_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡸࡻ࡭࡮ࡣࡵࡽࠬ໧"))
    logger.debug(perform_scan(driver))
    bstack1ll1111lll_opy_ = driver.execute_async_script(bstack1ll1ll1ll1_opy_.bstack111l1l111_opy_)
    return bstack1ll1111lll_opy_
  except Exception:
    logger.error(bstack1111l1l_opy_ (u"ࠣࡐࡲࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸࡻ࡭࡮ࡣࡵࡽࠥࡽࡡࡴࠢࡩࡳࡺࡴࡤ࠯ࠤ໨"))
    return {}
def bstack1l1l11111_opy_():
  global CONFIG
  global bstack1l1ll11lll_opy_
  bstack1llll11lll_opy_ = bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ໩"), None) and bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ໪"), None)
  if not bstack1lll1111l1_opy_.bstack1llll1l1l_opy_(CONFIG, bstack1l1ll11lll_opy_) or not bstack1llll11lll_opy_:
        logger.warning(bstack1111l1l_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡶࡰࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡵࡩࡸࡻ࡬ࡵࡵ࠱ࠦ໫"))
        return False
  return True
def bstack1lll1lll1l_opy_(bstack1ll11l11l_opy_):
    bstack1lll1ll11l_opy_ = bstack11l1lllll1_opy_.current_test_uuid() if bstack11l1lllll1_opy_.current_test_uuid() else bstack1ll11lll1_opy_.current_hook_uuid()
    with ThreadPoolExecutor() as executor:
        future = executor.submit(bstack11llllllll_opy_(bstack1lll1ll11l_opy_, bstack1ll11l11l_opy_))
        try:
            return future.result(timeout=bstack1l1lllll11_opy_)
        except TimeoutError:
            logger.error(bstack1111l1l_opy_ (u"࡚ࠧࡩ࡮ࡧࡲࡹࡹࠦࡡࡧࡶࡨࡶࠥࢁࡽࡴࠢࡺ࡬࡮ࡲࡥࠡࡨࡨࡸࡨ࡮ࡩ࡯ࡩࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡖࡪࡹࡵ࡭ࡶࡶࠦ໬").format(bstack1l1lllll11_opy_))
        except Exception as ex:
            logger.debug(bstack1111l1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡸࡥࡵࡴ࡬ࡩࡻ࡯࡮ࡨࠢࡄࡴࡵࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡿࢂ࠴ࠠࡆࡴࡵࡳࡷࠦ࠭ࠡࡽࢀࠦ໭").format(bstack1ll11l11l_opy_, str(ex)))
    return {}
@measure(event_name=EVENTS.bstack1ll11ll1l1_opy_, stage=STAGE.bstack1l1111l1ll_opy_, bstack1ll1l1ll_opy_=bstack1lllllllll_opy_)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack1l1ll11lll_opy_
  bstack11l111l11l_opy_ = not (bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ໮"), None) and bstack1l11l1lll_opy_(
          threading.current_thread(), bstack1111l1l_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ໯"), None))
  bstack11l1ll1l11_opy_ = not (bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ໰"), None) and bstack1l11l1lll_opy_(
          threading.current_thread(), bstack1111l1l_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ໱"), None))
  bstack1lll1111ll_opy_ = getattr(driver, bstack1111l1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫ໲"), None) != True
  if not bstack1lll1111l1_opy_.bstack1llll1l1l_opy_(CONFIG, bstack1l1ll11lll_opy_) or (bstack1lll1111ll_opy_ and bstack11l111l11l_opy_ and bstack11l1ll1l11_opy_):
    logger.warning(bstack1111l1l_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷࡻ࡮ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳ࠴ࠢ໳"))
    return {}
  try:
    bstack1l11111111_opy_ = bstack1111l1l_opy_ (u"࠭ࡡࡱࡲࠪ໴") in CONFIG and CONFIG.get(bstack1111l1l_opy_ (u"ࠧࡢࡲࡳࠫ໵"), bstack1111l1l_opy_ (u"ࠨࠩ໶"))
    session_id = getattr(driver, bstack1111l1l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩ࠭໷"), None)
    if not session_id:
      logger.warning(bstack1111l1l_opy_ (u"ࠥࡒࡴࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡊࡆࠣࡪࡴࡻ࡮ࡥࠢࡩࡳࡷࠦࡤࡳ࡫ࡹࡩࡷࠨ໸"))
      return {bstack1111l1l_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥ໹"): bstack1111l1l_opy_ (u"ࠧࡔ࡯ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡌࡈࠥ࡬࡯ࡶࡰࡧࠦ໺")}
    if bstack1l11111111_opy_:
      try:
        bstack111l1111_opy_ = {
              bstack1111l1l_opy_ (u"࠭ࡴࡩࡌࡺࡸ࡙ࡵ࡫ࡦࡰࠪ໻"): os.environ.get(bstack1111l1l_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ໼"), os.environ.get(bstack1111l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ໽"), bstack1111l1l_opy_ (u"ࠩࠪ໾"))),
              bstack1111l1l_opy_ (u"ࠪࡸ࡭࡚ࡥࡴࡶࡕࡹࡳ࡛ࡵࡪࡦࠪ໿"): bstack11l1lllll1_opy_.current_test_uuid() if bstack11l1lllll1_opy_.current_test_uuid() else bstack1ll11lll1_opy_.current_hook_uuid(),
              bstack1111l1l_opy_ (u"ࠫࡦࡻࡴࡩࡊࡨࡥࡩ࡫ࡲࠨༀ"): os.environ.get(bstack1111l1l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ༁")),
              bstack1111l1l_opy_ (u"࠭ࡳࡤࡣࡱࡘ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭༂"): str(int(datetime.datetime.now().timestamp() * 1000)),
              bstack1111l1l_opy_ (u"ࠧࡵࡪࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬ༃"): os.environ.get(bstack1111l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭༄"), bstack1111l1l_opy_ (u"ࠩࠪ༅")),
              bstack1111l1l_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࠪ༆"): kwargs.get(bstack1111l1l_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࡣࡨࡵ࡭࡮ࡣࡱࡨࠬ༇"), None) or bstack1111l1l_opy_ (u"ࠬ࠭༈")
          }
        if not hasattr(thread_local, bstack1111l1l_opy_ (u"࠭ࡢࡢࡵࡨࡣࡦࡶࡰࡠࡣ࠴࠵ࡾࡥࡳࡤࡴ࡬ࡴࡹ࠭༉")):
            scripts = {bstack1111l1l_opy_ (u"ࠧࡴࡥࡤࡲࠬ༊"): bstack1ll1ll1ll1_opy_.perform_scan}
            thread_local.base_app_a11y_script = scripts
        bstack11llllll11_opy_ = copy.deepcopy(thread_local.base_app_a11y_script)
        bstack11llllll11_opy_[bstack1111l1l_opy_ (u"ࠨࡵࡦࡥࡳ࠭་")] = bstack11llllll11_opy_[bstack1111l1l_opy_ (u"ࠩࡶࡧࡦࡴࠧ༌")] % json.dumps(bstack111l1111_opy_)
        bstack1ll1ll1ll1_opy_.bstack1l11l1ll_opy_(bstack11llllll11_opy_)
        bstack1ll1ll1ll1_opy_.store()
        bstack11l11lll1_opy_ = driver.execute_script(bstack1ll1ll1ll1_opy_.perform_scan)
      except Exception as bstack1lllll1l1_opy_:
        logger.info(bstack1111l1l_opy_ (u"ࠥࡅࡵࡶࡩࡶ࡯ࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࠥ།") + str(bstack1lllll1l1_opy_))
        bstack11l11lll1_opy_ = {bstack1111l1l_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥ༎"): str(bstack1lllll1l1_opy_)}
    else:
      bstack11l11lll1_opy_ = driver.execute_async_script(bstack1ll1ll1ll1_opy_.perform_scan, {bstack1111l1l_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬ༏"): kwargs.get(bstack1111l1l_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡣࡰ࡯ࡰࡥࡳࡪࠧ༐"), None) or bstack1111l1l_opy_ (u"ࠧࠨ༑")})
    return bstack11l11lll1_opy_
  except Exception as err:
    logger.error(bstack1111l1l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡷࡻ࡮ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳ࠴ࠠࡼࡿࠥ༒").format(str(err)))
    return {}