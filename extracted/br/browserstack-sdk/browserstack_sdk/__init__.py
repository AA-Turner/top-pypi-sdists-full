# coding: UTF-8
import sys
bstack111_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1llll1_opy_ = 7
def bstack1l1l1ll_opy_ (bstack1l1llll_opy_):
    global bstack11l1l11_opy_
    bstack1l11ll1_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack1l1l111_opy_ = bstack1l1llll_opy_ [:-1]
    bstack1111l11_opy_ = bstack1l11ll1_opy_ % len (bstack1l1l111_opy_)
    bstack11l11ll_opy_ = bstack1l1l111_opy_ [:bstack1111l11_opy_] + bstack1l1l111_opy_ [bstack1111l11_opy_:]
    if bstack111_opy_:
        bstack1lll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1lll1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1lll1l1_opy_)
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
from browserstack_sdk.bstack11l1l111l_opy_ import bstack11l11111ll_opy_
from browserstack_sdk.bstack1l1ll11lll_opy_ import *
import time
import requests
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.measure import measure
def bstack1l11l1l11_opy_():
  global CONFIG
  headers = {
        bstack1l1l1ll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack1l1l1ll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1lll1ll1_opy_(CONFIG, bstack1l1ll1111_opy_)
  try:
    response = requests.get(bstack1l1ll1111_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1l111ll11l_opy_ = response.json()[bstack1l1l1ll_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1l1l1l1l11_opy_.format(response.json()))
      return bstack1l111ll11l_opy_
    else:
      logger.debug(bstack11l11l1111_opy_.format(bstack1l1l1ll_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack11l11l1111_opy_.format(e))
def bstack1111111l_opy_(hub_url):
  global CONFIG
  url = bstack1l1l1ll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack1l1l1ll_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack1l1l1ll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack1l1l1ll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1lll1ll1_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack11lll11l11_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack11lll11l1_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack1l1llll1l1_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
def bstack11l11l11l1_opy_():
  try:
    global bstack1lll1l1ll_opy_
    bstack1l111ll11l_opy_ = bstack1l11l1l11_opy_()
    bstack11ll111l1l_opy_ = []
    results = []
    for bstack111l1l1l_opy_ in bstack1l111ll11l_opy_:
      bstack11ll111l1l_opy_.append(bstack1lll1l1ll1_opy_(target=bstack1111111l_opy_,args=(bstack111l1l1l_opy_,)))
    for t in bstack11ll111l1l_opy_:
      t.start()
    for t in bstack11ll111l1l_opy_:
      results.append(t.join())
    bstack1ll11111ll_opy_ = {}
    for item in results:
      hub_url = item[bstack1l1l1ll_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack1l1l1ll_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack1ll11111ll_opy_[hub_url] = latency
    bstack11l11ll1_opy_ = min(bstack1ll11111ll_opy_, key= lambda x: bstack1ll11111ll_opy_[x])
    bstack1lll1l1ll_opy_ = bstack11l11ll1_opy_
    logger.debug(bstack1l1ll1ll1l_opy_.format(bstack11l11ll1_opy_))
  except Exception as e:
    logger.debug(bstack1lllll111_opy_.format(e))
from browserstack_sdk.bstack1111l11ll_opy_ import *
from browserstack_sdk.bstack1l11l11ll_opy_ import *
from browserstack_sdk.bstack111l1l1ll_opy_ import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.bstack1l1l11lll1_opy_ import get_logger
from bstack_utils.measure import measure
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack1l111llll1_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
def bstack1l11lll111_opy_():
    global bstack1lll1l1ll_opy_
    try:
        bstack11l111l11l_opy_ = bstack1l1lll1111_opy_()
        bstack11ll1l1l1l_opy_(bstack11l111l11l_opy_)
        hub_url = bstack11l111l11l_opy_.get(bstack1l1l1ll_opy_ (u"ࠨࡵࡳ࡮ࠥࢀ"), bstack1l1l1ll_opy_ (u"ࠢࠣࢁ"))
        if hub_url.endswith(bstack1l1l1ll_opy_ (u"ࠨ࠱ࡺࡨ࠴࡮ࡵࡣࠩࢂ")):
            hub_url = hub_url.rsplit(bstack1l1l1ll_opy_ (u"ࠩ࠲ࡻࡩ࠵ࡨࡶࡤࠪࢃ"), 1)[0]
        if hub_url.startswith(bstack1l1l1ll_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫࢄ")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack1l1l1ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࠭ࢅ")):
            hub_url = hub_url[8:]
        bstack1lll1l1ll_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack1l1lll1111_opy_():
    global CONFIG
    bstack1ll111lll1_opy_ = CONFIG.get(bstack1l1l1ll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢆ"), {}).get(bstack1l1l1ll_opy_ (u"࠭ࡧࡳ࡫ࡧࡒࡦࡳࡥࠨࢇ"), bstack1l1l1ll_opy_ (u"ࠧࡏࡑࡢࡋࡗࡏࡄࡠࡐࡄࡑࡊࡥࡐࡂࡕࡖࡉࡉ࠭࢈"))
    if not isinstance(bstack1ll111lll1_opy_, str):
        raise ValueError(bstack1l1l1ll_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡈࡴ࡬ࡨࠥࡴࡡ࡮ࡧࠣࡱࡺࡹࡴࠡࡤࡨࠤࡦࠦࡶࡢ࡮࡬ࡨࠥࡹࡴࡳ࡫ࡱ࡫ࠧࢉ"))
    try:
        bstack11l111l11l_opy_ = bstack1llllll1l_opy_(bstack1ll111lll1_opy_)
        return bstack11l111l11l_opy_
    except Exception as e:
        logger.error(bstack1l1l1ll_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣࢊ").format(str(e)))
        return {}
def bstack1llllll1l_opy_(bstack1ll111lll1_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack1l1l1ll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࢋ")] or not CONFIG[bstack1l1l1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧࢌ")]:
            raise ValueError(bstack1l1l1ll_opy_ (u"ࠧࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠠࡰࡴࠣࡥࡨࡩࡥࡴࡵࠣ࡯ࡪࡿࠢࢍ"))
        url = bstack1l1l1111l_opy_ + bstack1ll111lll1_opy_
        auth = (CONFIG[bstack1l1l1ll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨࢎ")], CONFIG[bstack1l1l1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ࢏")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack1l1lll1l1l_opy_ = json.loads(response.text)
            return bstack1l1lll1l1l_opy_
    except ValueError as ve:
        logger.error(bstack1l1l1ll_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣ࢐").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack1l1l1ll_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥ࡭ࡲࡪࡦࠣࡨࡪࡺࡡࡪ࡮ࡶࠤ࠿ࠦࡻࡾࠤ࢑").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack11ll1l1l1l_opy_(bstack111lllll11_opy_):
    global CONFIG
    if bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ࢒") not in CONFIG or str(CONFIG[bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ࢓")]).lower() == bstack1l1l1ll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ࢔"):
        CONFIG[bstack1l1l1ll_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬ࢕")] = False
    elif bstack1l1l1ll_opy_ (u"ࠧࡪࡵࡗࡶ࡮ࡧ࡬ࡈࡴ࡬ࡨࠬ࢖") in bstack111lllll11_opy_:
        bstack11ll111l11_opy_ = CONFIG.get(bstack1l1l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢗ"), {})
        logger.debug(bstack1l1l1ll_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡰࡴࡩࡡ࡭ࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࠪࡹࠢ࢘"), bstack11ll111l11_opy_)
        bstack11ll1ll11l_opy_ = bstack111lllll11_opy_.get(bstack1l1l1ll_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡕࡩࡵ࡫ࡡࡵࡧࡵࡷ࢙ࠧ"), [])
        bstack11l11l1lll_opy_ = bstack1l1l1ll_opy_ (u"ࠦ࠱ࠨ࢚").join(bstack11ll1ll11l_opy_)
        logger.debug(bstack1l1l1ll_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡈࡻࡳࡵࡱࡰࠤࡷ࡫ࡰࡦࡣࡷࡩࡷࠦࡳࡵࡴ࡬ࡲ࡬ࡀࠠࠦࡵ࢛ࠥ"), bstack11l11l1lll_opy_)
        bstack11l1l11ll1_opy_ = {
            bstack1l1l1ll_opy_ (u"ࠨ࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣ࢜"): bstack1l1l1ll_opy_ (u"ࠢࡢࡶࡶ࠱ࡷ࡫ࡰࡦࡣࡷࡩࡷࠨ࢝"),
            bstack1l1l1ll_opy_ (u"ࠣࡨࡲࡶࡨ࡫ࡌࡰࡥࡤࡰࠧ࢞"): bstack1l1l1ll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ࢟"),
            bstack1l1l1ll_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠧࢠ"): bstack11l11l1lll_opy_
        }
        bstack11ll111l11_opy_.update(bstack11l1l11ll1_opy_)
        logger.debug(bstack1l1l1ll_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼࡙ࠣࡵࡪࡡࡵࡧࡧࠤࡱࡵࡣࡢ࡮ࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࠫࡳࠣࢡ"), bstack11ll111l11_opy_)
        CONFIG[bstack1l1l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢢ")] = bstack11ll111l11_opy_
        logger.debug(bstack1l1l1ll_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡌࡩ࡯ࡣ࡯ࠤࡈࡕࡎࡇࡋࡊ࠾ࠥࠫࡳࠣࢣ"), CONFIG)
def bstack11ll111lll_opy_():
    bstack11l111l11l_opy_ = bstack1l1lll1111_opy_()
    if not bstack11l111l11l_opy_[bstack1l1l1ll_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࡙ࡷࡲࠧࢤ")]:
      raise ValueError(bstack1l1l1ll_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࡚ࡸ࡬ࠡ࡫ࡶࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࡬ࡲࡰ࡯ࠣ࡫ࡷ࡯ࡤࠡࡦࡨࡸࡦ࡯࡬ࡴ࠰ࠥࢥ"))
    return bstack11l111l11l_opy_[bstack1l1l1ll_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࡛ࡲ࡭ࠩࢦ")] + bstack1l1l1ll_opy_ (u"ࠪࡃࡨࡧࡰࡴ࠿ࠪࢧ")
@measure(event_name=EVENTS.bstack11l1l1llll_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
def bstack1lll1lllll_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack1l1l1ll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ࢨ")], CONFIG[bstack1l1l1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࢩ")])
        url = bstack1llll1l1l_opy_
        logger.debug(bstack1l1l1ll_opy_ (u"ࠨࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬ࡲࡰ࡯ࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡗࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࠦࡁࡑࡋࠥࢪ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack1l1l1ll_opy_ (u"ࠢࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪࠨࢫ"): bstack1l1l1ll_opy_ (u"ࠣࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠦࢬ")})
            if response.status_code == 200:
                bstack1l11111ll_opy_ = json.loads(response.text)
                bstack11lll1lll1_opy_ = bstack1l11111ll_opy_.get(bstack1l1l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡴࠩࢭ"), [])
                if bstack11lll1lll1_opy_:
                    bstack11ll11l11_opy_ = bstack11lll1lll1_opy_[0]
                    build_hashed_id = bstack11ll11l11_opy_.get(bstack1l1l1ll_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ࢮ"))
                    bstack1ll1l11l1l_opy_ = bstack1lll1l11ll_opy_ + build_hashed_id
                    result.extend([build_hashed_id, bstack1ll1l11l1l_opy_])
                    logger.info(bstack1l1ll1l111_opy_.format(bstack1ll1l11l1l_opy_))
                    bstack1l1lll111l_opy_ = CONFIG[bstack1l1l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧࢯ")]
                    if bstack1l1l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢰ") in CONFIG:
                      bstack1l1lll111l_opy_ += bstack1l1l1ll_opy_ (u"࠭ࠠࠨࢱ") + CONFIG[bstack1l1l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࢲ")]
                    if bstack1l1lll111l_opy_ != bstack11ll11l11_opy_.get(bstack1l1l1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ࢳ")):
                      logger.debug(bstack11ll1llll1_opy_.format(bstack11ll11l11_opy_.get(bstack1l1l1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧࢴ")), bstack1l1lll111l_opy_))
                    return result
                else:
                    logger.debug(bstack1l1l1ll_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡑࡳࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡵࡪࡨࠤࡷ࡫ࡳࡱࡱࡱࡷࡪ࠴ࠢࢵ"))
            else:
                logger.debug(bstack1l1l1ll_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢶ"))
        except Exception as e:
            logger.error(bstack1l1l1ll_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࡹࠠ࠻ࠢࡾࢁࠧࢷ").format(str(e)))
    else:
        logger.debug(bstack1l1l1ll_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡉࡏࡏࡈࡌࡋࠥ࡯ࡳࠡࡰࡲࡸࠥࡹࡥࡵ࠰࡙ࠣࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢸ"))
    return [None, None]
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1111lll11_opy_ import bstack1111lll11_opy_, bstack11ll1111ll_opy_, bstack11llllllll_opy_, bstack11l111lll_opy_
from bstack_utils.measure import bstack111ll111l_opy_
from bstack_utils.measure import measure
from bstack_utils.percy import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1ll1l1ll1l_opy_ import bstack1ll1ll1lll_opy_
from bstack_utils.messages import *
from bstack_utils import bstack1l1l11lll1_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1111l1l1l_opy_, bstack1llll11ll1_opy_, bstack1ll11llll_opy_, bstack1l111l1l_opy_, \
  bstack1l1l11llll_opy_, \
  Notset, bstack1l1ll111l_opy_, \
  bstack1lllll1l11_opy_, bstack1l1lll11l1_opy_, bstack11ll1l1111_opy_, bstack1llll1llll_opy_, bstack111ll1ll1_opy_, bstack1ll1lll11l_opy_, \
  bstack1ll1l11111_opy_, \
  bstack11ll1ll1ll_opy_, bstack11llllll11_opy_, bstack111ll1l1l_opy_, bstack11l11llll_opy_, \
  bstack11llll11ll_opy_, bstack1lll1l111_opy_, bstack11lll1ll11_opy_, bstack1ll11ll1_opy_
from bstack_utils.bstack1ll1l1llll_opy_ import bstack1llll1111l_opy_
from bstack_utils.bstack1ll111ll1_opy_ import bstack1l1ll1l1ll_opy_, bstack1ll1l111l1_opy_
from bstack_utils.bstack1lll1111_opy_ import bstack1l11lllll_opy_
from bstack_utils.bstack11lll11ll1_opy_ import bstack11ll111111_opy_, bstack1llll111ll_opy_
from bstack_utils.bstack1lll11l1l1_opy_ import bstack1lll11l1l1_opy_
from bstack_utils.bstack1l11ll11ll_opy_ import bstack111111111_opy_
from bstack_utils.proxy import bstack11ll111l1_opy_, bstack1lll1ll1_opy_, bstack11l111ll1l_opy_, bstack1l11l1ll1_opy_
from bstack_utils.bstack11ll1l1lll_opy_ import bstack1lll11ll1_opy_
import bstack_utils.bstack1ll1l1ll1_opy_ as bstack111lllll1l_opy_
import bstack_utils.bstack1l111l1l11_opy_ as bstack1l111l1ll1_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.utils.bstack11l11lllll_opy_ import bstack1l11lll1ll_opy_
from bstack_utils.bstack11l1l111l1_opy_ import bstack1l1l1llll1_opy_
from bstack_utils.bstack11l11l11l_opy_ import bstack1l1l1llll_opy_
if os.getenv(bstack1l1l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡌࡔࡕࡋࡔࠩࢹ")):
  cli.bstack1l1lll111_opy_()
else:
  os.environ[bstack1l1l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡍࡕࡏࡌࡕࠪࢺ")] = bstack1l1l1ll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧࢻ")
bstack11l1l111_opy_ = bstack1l1l1ll_opy_ (u"ࠪࠤࠥ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࠣࠤ࡮࡬ࠨࡱࡣࡪࡩࠥࡃ࠽࠾ࠢࡹࡳ࡮ࡪࠠ࠱ࠫࠣࡿࡡࡴࠠࠡࠢࡷࡶࡾࢁ࡜࡯ࠢࡦࡳࡳࡹࡴࠡࡨࡶࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨ࡝ࠩࡩࡷࡡ࠭ࠩ࠼࡞ࡱࠤࠥࠦࠠࠡࡨࡶ࠲ࡦࡶࡰࡦࡰࡧࡊ࡮ࡲࡥࡔࡻࡱࡧ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪ࠯ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡶ࡟ࡪࡰࡧࡩࡽ࠯ࠠࠬࠢࠥ࠾ࠧࠦࠫࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࠨࡢࡹࡤ࡭ࡹࠦ࡮ࡦࡹࡓࡥ࡬࡫࠲࠯ࡧࡹࡥࡱࡻࡡࡵࡧࠫࠦ࠭࠯ࠠ࠾ࡀࠣࡿࢂࠨࠬࠡ࡞ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥ࡫ࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡄࡦࡶࡤ࡭ࡱࡹࠢࡾ࡞ࠪ࠭࠮࠯࡛ࠣࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠦࡢ࠯ࠠࠬࠢࠥ࠰ࡡࡢ࡮ࠣࠫ࡟ࡲࠥࠦࠠࠡࡿࡦࡥࡹࡩࡨࠩࡧࡻ࠭ࢀࡢ࡮ࠡࠢࠣࠤࢂࡢ࡮ࠡࠢࢀࡠࡳࠦࠠ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱ࠪࢼ")
bstack1llll1lll1_opy_ = bstack1l1l1ll_opy_ (u"ࠫࡡࡴ࠯ࠫࠢࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࠦࠪ࠰࡞ࡱࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠶ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡩࡡࡱࡵࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠷࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡲࡢ࡭ࡳࡪࡥࡹࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠷ࡣ࡜࡯ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯ࡵ࡯࡭ࡨ࡫ࠨ࠱࠮ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸࠯࡜࡯ࡥࡲࡲࡸࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯ࠥࡃࠠࡳࡧࡴࡹ࡮ࡸࡥࠩࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨࠩ࠼࡞ࡱ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡰࡦࡻ࡮ࡤࡪࠣࡁࠥࡧࡳࡺࡰࡦࠤ࠭ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷ࠮ࠦ࠽࠿ࠢࡾࡠࡳࡲࡥࡵࠢࡦࡥࡵࡹ࠻࡝ࡰࡷࡶࡾࠦࡻ࡝ࡰࡦࡥࡵࡹࠠ࠾ࠢࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࡢࡴࡶࡤࡧࡰࡥࡣࡢࡲࡶ࠭ࡡࡴࠠࠡࡿࠣࡧࡦࡺࡣࡩࠪࡨࡼ࠮ࠦࡻ࡝ࡰࠣࠤࠥࠦࡽ࡝ࡰࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࠻ࠢࡣࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠩࢁࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭ࢂࡦࠬ࡝ࡰࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴ࡞ࡱࠤࠥࢃࠩ࡝ࡰࢀࡠࡳ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࠪࢽ")
from ._version import __version__
bstack1llll1l11_opy_ = None
CONFIG = {}
bstack1ll11ll11_opy_ = {}
bstack11l1lll1_opy_ = {}
bstack11lllll1ll_opy_ = None
bstack1ll1ll1l1_opy_ = None
bstack1llll111_opy_ = None
bstack1l11lll1_opy_ = -1
bstack1lll11ll11_opy_ = 0
bstack1l1ll1l1l1_opy_ = bstack1l111lll11_opy_
bstack1ll1l1l1l1_opy_ = 1
bstack1lll11l11_opy_ = False
bstack1lllll11l_opy_ = False
bstack11ll1111_opy_ = bstack1l1l1ll_opy_ (u"ࠬ࠭ࢾ")
bstack11l11lll11_opy_ = bstack1l1l1ll_opy_ (u"࠭ࠧࢿ")
bstack1l111111l1_opy_ = False
bstack1lllll111l_opy_ = True
bstack1l1l1ll1l1_opy_ = bstack1l1l1ll_opy_ (u"ࠧࠨࣀ")
bstack1lll1l1l1l_opy_ = []
bstack1l1l111l1_opy_ = threading.Lock()
bstack11l111ll11_opy_ = threading.Lock()
bstack1lll1l1ll_opy_ = bstack1l1l1ll_opy_ (u"ࠨࠩࣁ")
bstack1l1ll1llll_opy_ = False
bstack11llll1l11_opy_ = None
bstack1lll1l1l_opy_ = None
bstack1l11ll11l_opy_ = None
bstack1ll11llll1_opy_ = -1
bstack1l11ll11l1_opy_ = os.path.join(os.path.expanduser(bstack1l1l1ll_opy_ (u"ࠩࢁࠫࣂ")), bstack1l1l1ll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪࣃ"), bstack1l1l1ll_opy_ (u"ࠫ࠳ࡸ࡯ࡣࡱࡷ࠱ࡷ࡫ࡰࡰࡴࡷ࠱࡭࡫࡬ࡱࡧࡵ࠲࡯ࡹ࡯࡯ࠩࣄ"))
bstack1llll1l1_opy_ = 0
bstack11ll1l1l1_opy_ = 0
bstack1l1l11l1l1_opy_ = []
bstack1ll1111l1_opy_ = []
bstack1l11111l_opy_ = []
bstack1l1lll1l1_opy_ = []
bstack11lll1l111_opy_ = bstack1l1l1ll_opy_ (u"ࠬ࠭ࣅ")
bstack1l1l1l11l_opy_ = bstack1l1l1ll_opy_ (u"࠭ࠧࣆ")
bstack1lll1lll1l_opy_ = False
bstack11llll1l1_opy_ = False
bstack1ll1ll1l_opy_ = {}
bstack1lllll1lll_opy_ = None
bstack1l1ll1l1l_opy_ = None
bstack1ll1l1l11l_opy_ = None
bstack11l11111_opy_ = None
bstack11l1ll1l_opy_ = None
bstack1l1111llll_opy_ = None
bstack1l111lll1_opy_ = None
bstack11111l111_opy_ = None
bstack1lll11lll_opy_ = None
bstack1ll11ll111_opy_ = None
bstack1llll1ll_opy_ = None
bstack1llllll1l1_opy_ = None
bstack111l1l11l_opy_ = None
bstack1ll11l11l_opy_ = None
bstack11l11lll1_opy_ = None
bstack1lll111111_opy_ = None
bstack11ll1111l_opy_ = None
bstack1111l11l_opy_ = None
bstack11111l1l_opy_ = None
bstack1111111ll_opy_ = None
bstack11l11l1l1_opy_ = None
bstack1l1l1l1l1_opy_ = None
bstack11llllll1l_opy_ = None
thread_local = threading.local()
bstack1l1111lll1_opy_ = False
bstack1llll1l11l_opy_ = bstack1l1l1ll_opy_ (u"ࠢࠣࣇ")
logger = bstack1l1l11lll1_opy_.get_logger(__name__, bstack1l1ll1l1l1_opy_)
bstack1l1l1111l1_opy_ = Config.bstack11l1lllll1_opy_()
percy = bstack1lllllll1_opy_()
bstack1lll1llll1_opy_ = bstack1ll1ll1lll_opy_()
bstack1ll1l1ll11_opy_ = bstack111l1l1ll_opy_()
def bstack11ll11lll1_opy_():
  global CONFIG
  global bstack1lll1lll1l_opy_
  global bstack1l1l1111l1_opy_
  testContextOptions = bstack1ll11l1ll_opy_(CONFIG)
  if bstack1l1l11llll_opy_(CONFIG):
    if (bstack1l1l1ll_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪࣈ") in testContextOptions and str(testContextOptions[bstack1l1l1ll_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫࣉ")]).lower() == bstack1l1l1ll_opy_ (u"ࠪࡸࡷࡻࡥࠨ࣊")):
      bstack1lll1lll1l_opy_ = True
    bstack1l1l1111l1_opy_.bstack11l1111l1l_opy_(testContextOptions.get(bstack1l1l1ll_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ࣋"), False))
  else:
    bstack1lll1lll1l_opy_ = True
    bstack1l1l1111l1_opy_.bstack11l1111l1l_opy_(True)
def bstack111lll11l_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1l111111l_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1lllllll11_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1l1l1ll_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡩ࡯࡯ࡨ࡬࡫࡫࡯࡬ࡦࠤ࣌") == args[i].lower() or bstack1l1l1ll_opy_ (u"ࠨ࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡪ࡮࡭ࠢ࣍") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1l1l1ll1l1_opy_
      bstack1l1l1ll1l1_opy_ += bstack1l1l1ll_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠤࠧ࠭࣎") + path + bstack1l1l1ll_opy_ (u"ࠨࠤ࣏ࠪ")
      return path
  return None
bstack11l11111l1_opy_ = re.compile(bstack1l1l1ll_opy_ (u"ࡴࠥ࠲࠯ࡅ࡜ࠥࡽࠫ࠲࠯ࡅࠩࡾ࠰࠭ࡃ࣐ࠧ"))
def bstack11111l1l1_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack11l11111l1_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack1l1l1ll_opy_ (u"ࠥࠨࢀࠨ࣑") + group + bstack1l1l1ll_opy_ (u"ࠦࢂࠨ࣒"), os.environ.get(group))
  return value
def bstack1l11l111l1_opy_():
  global bstack11llllll1l_opy_
  if bstack11llllll1l_opy_ is None:
        bstack11llllll1l_opy_ = bstack1lllllll11_opy_()
  bstack11ll11l1l_opy_ = bstack11llllll1l_opy_
  if bstack11ll11l1l_opy_ and os.path.exists(os.path.abspath(bstack11ll11l1l_opy_)):
    fileName = bstack11ll11l1l_opy_
  if bstack1l1l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆ࣓ࠩ") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack1l1l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࡤࡌࡉࡍࡇࠪࣔ")])) and not bstack1l1l1ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡓࡧ࡭ࡦࠩࣕ") in locals():
    fileName = os.environ[bstack1l1l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬࣖ")]
  if bstack1l1l1ll_opy_ (u"ࠩࡩ࡭ࡱ࡫ࡎࡢ࡯ࡨࠫࣗ") in locals():
    bstack11l1l1_opy_ = os.path.abspath(fileName)
  else:
    bstack11l1l1_opy_ = bstack1l1l1ll_opy_ (u"ࠪࠫࣘ")
  bstack1l1l1l111_opy_ = os.getcwd()
  bstack11l1ll1l11_opy_ = bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧࣙ")
  bstack1l1l11ll11_opy_ = bstack1l1l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡧ࡭࡭ࠩࣚ")
  while (not os.path.exists(bstack11l1l1_opy_)) and bstack1l1l1l111_opy_ != bstack1l1l1ll_opy_ (u"ࠨࠢࣛ"):
    bstack11l1l1_opy_ = os.path.join(bstack1l1l1l111_opy_, bstack11l1ll1l11_opy_)
    if not os.path.exists(bstack11l1l1_opy_):
      bstack11l1l1_opy_ = os.path.join(bstack1l1l1l111_opy_, bstack1l1l11ll11_opy_)
    if bstack1l1l1l111_opy_ != os.path.dirname(bstack1l1l1l111_opy_):
      bstack1l1l1l111_opy_ = os.path.dirname(bstack1l1l1l111_opy_)
    else:
      bstack1l1l1l111_opy_ = bstack1l1l1ll_opy_ (u"ࠢࠣࣜ")
  bstack11llllll1l_opy_ = bstack11l1l1_opy_ if os.path.exists(bstack11l1l1_opy_) else None
  return bstack11llllll1l_opy_
def bstack1ll11l1l11_opy_(config):
    if bstack1l1l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡘࡥࡱࡱࡵࡸ࡮ࡴࡧࠨࣝ") in config:
      config[bstack1l1l1ll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ࣞ")] = config[bstack1l1l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡓࡧࡳࡳࡷࡺࡩ࡯ࡩࠪࣟ")]
    if bstack1l1l1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࡓࡵࡺࡩࡰࡰࡶࠫ࣠") in config:
      config[bstack1l1l1ll_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ࣡")] = config[bstack1l1l1ll_opy_ (u"࠭ࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬ࡕࡰࡵ࡫ࡲࡲࡸ࠭࣢")]
def bstack1ll11l111_opy_():
  bstack11l1l1_opy_ = bstack1l11l111l1_opy_()
  if not os.path.exists(bstack11l1l1_opy_):
    bstack1l1l11l111_opy_(
      bstack11lllllll_opy_.format(os.getcwd()))
  try:
    with open(bstack11l1l1_opy_, bstack1l1l1ll_opy_ (u"ࠧࡳࣣࠩ")) as stream:
      yaml.add_implicit_resolver(bstack1l1l1ll_opy_ (u"ࠣࠣࡳࡥࡹ࡮ࡥࡹࠤࣤ"), bstack11l11111l1_opy_)
      yaml.add_constructor(bstack1l1l1ll_opy_ (u"ࠤࠤࡴࡦࡺࡨࡦࡺࠥࣥ"), bstack11111l1l1_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      bstack1ll11l1l11_opy_(config)
      return config
  except:
    with open(bstack11l1l1_opy_, bstack1l1l1ll_opy_ (u"ࠪࡶࣦࠬ")) as stream:
      try:
        config = yaml.safe_load(stream)
        bstack1ll11l1l11_opy_(config)
        return config
      except yaml.YAMLError as exc:
        bstack1l1l11l111_opy_(bstack1ll1l1lll_opy_.format(str(exc)))
def bstack1llll11lll_opy_(config):
  bstack1111l1111_opy_ = bstack1ll1llllll_opy_(config)
  for option in list(bstack1111l1111_opy_):
    if option.lower() in bstack1ll1l1l1_opy_ and option != bstack1ll1l1l1_opy_[option.lower()]:
      bstack1111l1111_opy_[bstack1ll1l1l1_opy_[option.lower()]] = bstack1111l1111_opy_[option]
      del bstack1111l1111_opy_[option]
  return config
def bstack11l1l1ll1l_opy_():
  global bstack11l1lll1_opy_
  for key, bstack1l1l1111_opy_ in bstack111lllll_opy_.items():
    if isinstance(bstack1l1l1111_opy_, list):
      for var in bstack1l1l1111_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack11l1lll1_opy_[key] = os.environ[var]
          break
    elif bstack1l1l1111_opy_ in os.environ and os.environ[bstack1l1l1111_opy_] and str(os.environ[bstack1l1l1111_opy_]).strip():
      bstack11l1lll1_opy_[key] = os.environ[bstack1l1l1111_opy_]
  if bstack1l1l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ࣧ") in os.environ:
    bstack11l1lll1_opy_[bstack1l1l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣨ")] = {}
    bstack11l1lll1_opy_[bstack1l1l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࣩࠪ")][bstack1l1l1ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ࣪")] = os.environ[bstack1l1l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪ࣫")]
def bstack1l1l111l11_opy_():
  global bstack1ll11ll11_opy_
  global bstack1l1l1ll1l1_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack1l1l1ll_opy_ (u"ࠩ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ࣬").lower() == val.lower():
      bstack1ll11ll11_opy_[bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹ࣭ࠧ")] = {}
      bstack1ll11ll11_opy_[bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ࣮")][bstack1l1l1ll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣯ࠧ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack11l11111l_opy_ in bstack111ll1l11_opy_.items():
    if isinstance(bstack11l11111l_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack11l11111l_opy_:
          if idx < len(sys.argv) and bstack1l1l1ll_opy_ (u"࠭࠭࠮ࣰࠩ") + var.lower() == val.lower() and not key in bstack1ll11ll11_opy_:
            bstack1ll11ll11_opy_[key] = sys.argv[idx + 1]
            bstack1l1l1ll1l1_opy_ += bstack1l1l1ll_opy_ (u"ࠧࠡ࠯࠰ࣱࠫ") + var + bstack1l1l1ll_opy_ (u"ࠨࣲࠢࠪ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack1l1l1ll_opy_ (u"ࠩ࠰࠱ࠬࣳ") + bstack11l11111l_opy_.lower() == val.lower() and not key in bstack1ll11ll11_opy_:
          bstack1ll11ll11_opy_[key] = sys.argv[idx + 1]
          bstack1l1l1ll1l1_opy_ += bstack1l1l1ll_opy_ (u"ࠪࠤ࠲࠳ࠧࣴ") + bstack11l11111l_opy_ + bstack1l1l1ll_opy_ (u"ࠫࠥ࠭ࣵ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack11lll1ll1_opy_(config):
  bstack1ll1l1l1ll_opy_ = config.keys()
  for bstack11111l11_opy_, bstack1l11ll1111_opy_ in bstack11l111l1_opy_.items():
    if bstack1l11ll1111_opy_ in bstack1ll1l1l1ll_opy_:
      config[bstack11111l11_opy_] = config[bstack1l11ll1111_opy_]
      del config[bstack1l11ll1111_opy_]
  for bstack11111l11_opy_, bstack1l11ll1111_opy_ in bstack1l1111ll1l_opy_.items():
    if isinstance(bstack1l11ll1111_opy_, list):
      for bstack1ll1l111ll_opy_ in bstack1l11ll1111_opy_:
        if bstack1ll1l111ll_opy_ in bstack1ll1l1l1ll_opy_:
          config[bstack11111l11_opy_] = config[bstack1ll1l111ll_opy_]
          del config[bstack1ll1l111ll_opy_]
          break
    elif bstack1l11ll1111_opy_ in bstack1ll1l1l1ll_opy_:
      config[bstack11111l11_opy_] = config[bstack1l11ll1111_opy_]
      del config[bstack1l11ll1111_opy_]
  for bstack1ll1l111ll_opy_ in list(config):
    for bstack11l1l11l1_opy_ in bstack1l11l1lll1_opy_:
      if bstack1ll1l111ll_opy_.lower() == bstack11l1l11l1_opy_.lower() and bstack1ll1l111ll_opy_ != bstack11l1l11l1_opy_:
        config[bstack11l1l11l1_opy_] = config[bstack1ll1l111ll_opy_]
        del config[bstack1ll1l111ll_opy_]
  bstack1l1llll11l_opy_ = [{}]
  if not config.get(bstack1l1l1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨࣶ")):
    config[bstack1l1l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩࣷ")] = [{}]
  bstack1l1llll11l_opy_ = config[bstack1l1l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪࣸ")]
  for platform in bstack1l1llll11l_opy_:
    for bstack1ll1l111ll_opy_ in list(platform):
      for bstack11l1l11l1_opy_ in bstack1l11l1lll1_opy_:
        if bstack1ll1l111ll_opy_.lower() == bstack11l1l11l1_opy_.lower() and bstack1ll1l111ll_opy_ != bstack11l1l11l1_opy_:
          platform[bstack11l1l11l1_opy_] = platform[bstack1ll1l111ll_opy_]
          del platform[bstack1ll1l111ll_opy_]
  for bstack11111l11_opy_, bstack1l11ll1111_opy_ in bstack1l1111ll1l_opy_.items():
    for platform in bstack1l1llll11l_opy_:
      if isinstance(bstack1l11ll1111_opy_, list):
        for bstack1ll1l111ll_opy_ in bstack1l11ll1111_opy_:
          if bstack1ll1l111ll_opy_ in platform:
            platform[bstack11111l11_opy_] = platform[bstack1ll1l111ll_opy_]
            del platform[bstack1ll1l111ll_opy_]
            break
      elif bstack1l11ll1111_opy_ in platform:
        platform[bstack11111l11_opy_] = platform[bstack1l11ll1111_opy_]
        del platform[bstack1l11ll1111_opy_]
  for bstack1ll1l1111_opy_ in bstack11l1l11lll_opy_:
    if bstack1ll1l1111_opy_ in config:
      if not bstack11l1l11lll_opy_[bstack1ll1l1111_opy_] in config:
        config[bstack11l1l11lll_opy_[bstack1ll1l1111_opy_]] = {}
      config[bstack11l1l11lll_opy_[bstack1ll1l1111_opy_]].update(config[bstack1ll1l1111_opy_])
      del config[bstack1ll1l1111_opy_]
  for platform in bstack1l1llll11l_opy_:
    for bstack1ll1l1111_opy_ in bstack11l1l11lll_opy_:
      if bstack1ll1l1111_opy_ in list(platform):
        if not bstack11l1l11lll_opy_[bstack1ll1l1111_opy_] in platform:
          platform[bstack11l1l11lll_opy_[bstack1ll1l1111_opy_]] = {}
        platform[bstack11l1l11lll_opy_[bstack1ll1l1111_opy_]].update(platform[bstack1ll1l1111_opy_])
        del platform[bstack1ll1l1111_opy_]
  config = bstack1llll11lll_opy_(config)
  return config
def bstack1llll11l1_opy_(config):
  global bstack11l11lll11_opy_
  bstack1ll111l1l_opy_ = False
  if bstack1l1l1ll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࣹࠬ") in config and str(config[bstack1l1l1ll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࣺ࠭")]).lower() != bstack1l1l1ll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩࣻ"):
    if bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨࣼ") not in config or str(config[bstack1l1l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩࣽ")]).lower() == bstack1l1l1ll_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬࣾ"):
      config[bstack1l1l1ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭ࣿ")] = False
    else:
      bstack11l111l11l_opy_ = bstack1l1lll1111_opy_()
      if bstack1l1l1ll_opy_ (u"ࠨ࡫ࡶࡘࡷ࡯ࡡ࡭ࡉࡵ࡭ࡩ࠭ऀ") in bstack11l111l11l_opy_:
        if not bstack1l1l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ँ") in config:
          config[bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧं")] = {}
        config[bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨः")][bstack1l1l1ll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऄ")] = bstack1l1l1ll_opy_ (u"࠭ࡡࡵࡵ࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠬअ")
        bstack1ll111l1l_opy_ = True
        bstack11l11lll11_opy_ = config[bstack1l1l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫआ")].get(bstack1l1l1ll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪइ"))
  if bstack1l1l11llll_opy_(config) and bstack1l1l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ई") in config and str(config[bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧउ")]).lower() != bstack1l1l1ll_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪऊ") and not bstack1ll111l1l_opy_:
    if not bstack1l1l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩऋ") in config:
      config[bstack1l1l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪऌ")] = {}
    if not config[bstack1l1l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫऍ")].get(bstack1l1l1ll_opy_ (u"ࠨࡵ࡮࡭ࡵࡈࡩ࡯ࡣࡵࡽࡎࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡡࡵ࡫ࡲࡲࠬऎ")) and not bstack1l1l1ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫए") in config[bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧऐ")]:
      bstack11lllll1_opy_ = datetime.datetime.now()
      bstack11ll1lllll_opy_ = bstack11lllll1_opy_.strftime(bstack1l1l1ll_opy_ (u"ࠫࠪࡪ࡟ࠦࡤࡢࠩࡍࠫࡍࠨऑ"))
      hostname = socket.gethostname()
      bstack1111ll111_opy_ = bstack1l1l1ll_opy_ (u"ࠬ࠭ऒ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1l1l1ll_opy_ (u"࠭ࡻࡾࡡࡾࢁࡤࢁࡽࠨओ").format(bstack11ll1lllll_opy_, hostname, bstack1111ll111_opy_)
      config[bstack1l1l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫऔ")][bstack1l1l1ll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪक")] = identifier
    bstack11l11lll11_opy_ = config[bstack1l1l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ख")].get(bstack1l1l1ll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬग"))
  return config
def bstack1l111llll_opy_():
  bstack11111lll_opy_ =  bstack1llll1llll_opy_()[bstack1l1l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠪघ")]
  return bstack11111lll_opy_ if bstack11111lll_opy_ else -1
def bstack11l11l111_opy_(bstack11111lll_opy_):
  global CONFIG
  if not bstack1l1l1ll_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧङ") in CONFIG[bstack1l1l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨच")]:
    return
  CONFIG[bstack1l1l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩछ")] = CONFIG[bstack1l1l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪज")].replace(
    bstack1l1l1ll_opy_ (u"ࠩࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫझ"),
    str(bstack11111lll_opy_)
  )
def bstack1l1l111l1l_opy_():
  global CONFIG
  if not bstack1l1l1ll_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾࠩञ") in CONFIG[bstack1l1l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ट")]:
    return
  bstack11lllll1_opy_ = datetime.datetime.now()
  bstack11ll1lllll_opy_ = bstack11lllll1_opy_.strftime(bstack1l1l1ll_opy_ (u"ࠬࠫࡤ࠮ࠧࡥ࠱ࠪࡎ࠺ࠦࡏࠪठ"))
  CONFIG[bstack1l1l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨड")] = CONFIG[bstack1l1l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩढ")].replace(
    bstack1l1l1ll_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧण"),
    bstack11ll1lllll_opy_
  )
def bstack1l1lll1l_opy_():
  global CONFIG
  if bstack1l1l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫत") in CONFIG and not bool(CONFIG[bstack1l1l1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬथ")]):
    del CONFIG[bstack1l1l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭द")]
    return
  if not bstack1l1l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧध") in CONFIG:
    CONFIG[bstack1l1l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨन")] = bstack1l1l1ll_opy_ (u"ࠧࠤࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪऩ")
  if bstack1l1l1ll_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧप") in CONFIG[bstack1l1l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫफ")]:
    bstack1l1l111l1l_opy_()
    os.environ[bstack1l1l1ll_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧब")] = CONFIG[bstack1l1l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭भ")]
  if not bstack1l1l1ll_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧम") in CONFIG[bstack1l1l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨय")]:
    return
  bstack11111lll_opy_ = bstack1l1l1ll_opy_ (u"ࠧࠨर")
  bstack11lll1l1l1_opy_ = bstack1l111llll_opy_()
  if bstack11lll1l1l1_opy_ != -1:
    bstack11111lll_opy_ = bstack1l1l1ll_opy_ (u"ࠨࡅࡌࠤࠬऱ") + str(bstack11lll1l1l1_opy_)
  if bstack11111lll_opy_ == bstack1l1l1ll_opy_ (u"ࠩࠪल"):
    bstack11l11ll1ll_opy_ = bstack1l11l1l1l_opy_(CONFIG[bstack1l1l1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ळ")])
    if bstack11l11ll1ll_opy_ != -1:
      bstack11111lll_opy_ = str(bstack11l11ll1ll_opy_)
  if bstack11111lll_opy_:
    bstack11l11l111_opy_(bstack11111lll_opy_)
    os.environ[bstack1l1l1ll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨऴ")] = CONFIG[bstack1l1l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧव")]
def bstack1ll1ll1l1l_opy_(bstack11l1ll1ll1_opy_, bstack1l1l11l1_opy_, path):
  bstack1l111l11_opy_ = {
    bstack1l1l1ll_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪश"): bstack1l1l11l1_opy_
  }
  if os.path.exists(path):
    bstack1ll1l111_opy_ = json.load(open(path, bstack1l1l1ll_opy_ (u"ࠧࡳࡤࠪष")))
  else:
    bstack1ll1l111_opy_ = {}
  bstack1ll1l111_opy_[bstack11l1ll1ll1_opy_] = bstack1l111l11_opy_
  with open(path, bstack1l1l1ll_opy_ (u"ࠣࡹ࠮ࠦस")) as outfile:
    json.dump(bstack1ll1l111_opy_, outfile)
def bstack1l11l1l1l_opy_(bstack11l1ll1ll1_opy_):
  bstack11l1ll1ll1_opy_ = str(bstack11l1ll1ll1_opy_)
  bstack1lll11llll_opy_ = os.path.join(os.path.expanduser(bstack1l1l1ll_opy_ (u"ࠩࢁࠫह")), bstack1l1l1ll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪऺ"))
  try:
    if not os.path.exists(bstack1lll11llll_opy_):
      os.makedirs(bstack1lll11llll_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1l1l1ll_opy_ (u"ࠫࢃ࠭ऻ")), bstack1l1l1ll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯़ࠬ"), bstack1l1l1ll_opy_ (u"࠭࠮ࡣࡷ࡬ࡰࡩ࠳࡮ࡢ࡯ࡨ࠱ࡨࡧࡣࡩࡧ࠱࡮ࡸࡵ࡮ࠨऽ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1l1l1ll_opy_ (u"ࠧࡸࠩा")):
        pass
      with open(file_path, bstack1l1l1ll_opy_ (u"ࠣࡹ࠮ࠦि")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1l1l1ll_opy_ (u"ࠩࡵࠫी")) as bstack11l111l111_opy_:
      bstack1l111ll1l_opy_ = json.load(bstack11l111l111_opy_)
    if bstack11l1ll1ll1_opy_ in bstack1l111ll1l_opy_:
      bstack1ll1ll11l1_opy_ = bstack1l111ll1l_opy_[bstack11l1ll1ll1_opy_][bstack1l1l1ll_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧु")]
      bstack1lll1l1l1_opy_ = int(bstack1ll1ll11l1_opy_) + 1
      bstack1ll1ll1l1l_opy_(bstack11l1ll1ll1_opy_, bstack1lll1l1l1_opy_, file_path)
      return bstack1lll1l1l1_opy_
    else:
      bstack1ll1ll1l1l_opy_(bstack11l1ll1ll1_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1ll111l111_opy_.format(str(e)))
    return -1
def bstack1ll11111l_opy_(config):
  if not config[bstack1l1l1ll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ू")] or not config[bstack1l1l1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨृ")]:
    return True
  else:
    return False
def bstack111l1ll1_opy_(config, index=0):
  global bstack1l111111l1_opy_
  bstack1111l1l1_opy_ = {}
  caps = bstack1l1l11ll1_opy_ + bstack11l1lll111_opy_
  if config.get(bstack1l1l1ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪॄ"), False):
    bstack1111l1l1_opy_[bstack1l1l1ll_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫॅ")] = True
    bstack1111l1l1_opy_[bstack1l1l1ll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࡔࡶࡴࡪࡱࡱࡷࠬॆ")] = config.get(bstack1l1l1ll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭े"), {})
  if bstack1l111111l1_opy_:
    caps += bstack1l1llll1_opy_
  for key in config:
    if key in caps + [bstack1l1l1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ै")]:
      continue
    bstack1111l1l1_opy_[key] = config[key]
  if bstack1l1l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॉ") in config:
    for bstack1l1ll1lll1_opy_ in config[bstack1l1l1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨॊ")][index]:
      if bstack1l1ll1lll1_opy_ in caps:
        continue
      bstack1111l1l1_opy_[bstack1l1ll1lll1_opy_] = config[bstack1l1l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩो")][index][bstack1l1ll1lll1_opy_]
  bstack1111l1l1_opy_[bstack1l1l1ll_opy_ (u"ࠧࡩࡱࡶࡸࡓࡧ࡭ࡦࠩौ")] = socket.gethostname()
  if bstack1l1l1ll_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯्ࠩ") in bstack1111l1l1_opy_:
    del (bstack1111l1l1_opy_[bstack1l1l1ll_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪॎ")])
  return bstack1111l1l1_opy_
def bstack1l11ll11_opy_(config):
  global bstack1l111111l1_opy_
  bstack11l1lllll_opy_ = {}
  caps = bstack11l1lll111_opy_
  if bstack1l111111l1_opy_:
    caps += bstack1l1llll1_opy_
  for key in caps:
    if key in config:
      bstack11l1lllll_opy_[key] = config[key]
  return bstack11l1lllll_opy_
def bstack11llllll1_opy_(bstack1111l1l1_opy_, bstack11l1lllll_opy_):
  bstack11ll1l111_opy_ = {}
  for key in bstack1111l1l1_opy_.keys():
    if key in bstack11l111l1_opy_:
      bstack11ll1l111_opy_[bstack11l111l1_opy_[key]] = bstack1111l1l1_opy_[key]
    else:
      bstack11ll1l111_opy_[key] = bstack1111l1l1_opy_[key]
  for key in bstack11l1lllll_opy_:
    if key in bstack11l111l1_opy_:
      bstack11ll1l111_opy_[bstack11l111l1_opy_[key]] = bstack11l1lllll_opy_[key]
    else:
      bstack11ll1l111_opy_[key] = bstack11l1lllll_opy_[key]
  return bstack11ll1l111_opy_
def bstack1l11l11l11_opy_(config, index=0):
  global bstack1l111111l1_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack1l111111ll_opy_ = bstack1111l1l1l_opy_(bstack11ll1l1ll_opy_, config, logger)
  bstack11l1lllll_opy_ = bstack1l11ll11_opy_(config)
  bstack11l1llll1l_opy_ = bstack11l1lll111_opy_
  bstack11l1llll1l_opy_ += bstack11ll1lll1_opy_
  bstack11l1lllll_opy_ = update(bstack11l1lllll_opy_, bstack1l111111ll_opy_)
  if bstack1l111111l1_opy_:
    bstack11l1llll1l_opy_ += bstack1l1llll1_opy_
  if bstack1l1l1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॏ") in config:
    if bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩॐ") in config[bstack1l1l1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ॑")][index]:
      caps[bstack1l1l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨ॒ࠫ")] = config[bstack1l1l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ॓")][index][bstack1l1l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭॔")]
    if bstack1l1l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪॕ") in config[bstack1l1l1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॖ")][index]:
      caps[bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬॗ")] = str(config[bstack1l1l1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨक़")][index][bstack1l1l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧख़")])
    bstack1ll1lll1l1_opy_ = bstack1111l1l1l_opy_(bstack11ll1l1ll_opy_, config[bstack1l1l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪग़")][index], logger)
    bstack11l1llll1l_opy_ += list(bstack1ll1lll1l1_opy_.keys())
    for bstack111l1l111_opy_ in bstack11l1llll1l_opy_:
      if bstack111l1l111_opy_ in config[bstack1l1l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫज़")][index]:
        if bstack111l1l111_opy_ == bstack1l1l1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫड़"):
          try:
            bstack1ll1lll1l1_opy_[bstack111l1l111_opy_] = str(config[bstack1l1l1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ढ़")][index][bstack111l1l111_opy_] * 1.0)
          except:
            bstack1ll1lll1l1_opy_[bstack111l1l111_opy_] = str(config[bstack1l1l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧफ़")][index][bstack111l1l111_opy_])
        else:
          bstack1ll1lll1l1_opy_[bstack111l1l111_opy_] = config[bstack1l1l1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨय़")][index][bstack111l1l111_opy_]
        del (config[bstack1l1l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩॠ")][index][bstack111l1l111_opy_])
    bstack11l1lllll_opy_ = update(bstack11l1lllll_opy_, bstack1ll1lll1l1_opy_)
  bstack1111l1l1_opy_ = bstack111l1ll1_opy_(config, index)
  for bstack1ll1l111ll_opy_ in bstack11l1lll111_opy_ + list(bstack1l111111ll_opy_.keys()):
    if bstack1ll1l111ll_opy_ in bstack1111l1l1_opy_:
      bstack11l1lllll_opy_[bstack1ll1l111ll_opy_] = bstack1111l1l1_opy_[bstack1ll1l111ll_opy_]
      del (bstack1111l1l1_opy_[bstack1ll1l111ll_opy_])
  if bstack1l1ll111l_opy_(config):
    bstack1111l1l1_opy_[bstack1l1l1ll_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧॡ")] = True
    caps.update(bstack11l1lllll_opy_)
    caps[bstack1l1l1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩॢ")] = bstack1111l1l1_opy_
  else:
    bstack1111l1l1_opy_[bstack1l1l1ll_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩॣ")] = False
    caps.update(bstack11llllll1_opy_(bstack1111l1l1_opy_, bstack11l1lllll_opy_))
    if bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ।") in caps:
      caps[bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬ॥")] = caps[bstack1l1l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ०")]
      del (caps[bstack1l1l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ१")])
    if bstack1l1l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ२") in caps:
      caps[bstack1l1l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪ३")] = caps[bstack1l1l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ४")]
      del (caps[bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ५")])
  return caps
def bstack11lll1lll_opy_():
  global bstack1lll1l1ll_opy_
  global CONFIG
  if bstack1l111111l_opy_() <= version.parse(bstack1l1l1ll_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫ६")):
    if bstack1lll1l1ll_opy_ != bstack1l1l1ll_opy_ (u"ࠬ࠭७"):
      return bstack1l1l1ll_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ८") + bstack1lll1l1ll_opy_ + bstack1l1l1ll_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦ९")
    return bstack11l11l1l_opy_
  if bstack1lll1l1ll_opy_ != bstack1l1l1ll_opy_ (u"ࠨࠩ॰"):
    return bstack1l1l1ll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦॱ") + bstack1lll1l1ll_opy_ + bstack1l1l1ll_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦॲ")
  return bstack1lllllllll_opy_
def bstack1l1111ll1_opy_(options):
  return hasattr(options, bstack1l1l1ll_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬॳ"))
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
def bstack1l1l1lllll_opy_(options, bstack1l1ll1l11_opy_):
  for bstack1lll11111l_opy_ in bstack1l1ll1l11_opy_:
    if bstack1lll11111l_opy_ in [bstack1l1l1ll_opy_ (u"ࠬࡧࡲࡨࡵࠪॴ"), bstack1l1l1ll_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪॵ")]:
      continue
    if bstack1lll11111l_opy_ in options._experimental_options:
      options._experimental_options[bstack1lll11111l_opy_] = update(options._experimental_options[bstack1lll11111l_opy_],
                                                         bstack1l1ll1l11_opy_[bstack1lll11111l_opy_])
    else:
      options.add_experimental_option(bstack1lll11111l_opy_, bstack1l1ll1l11_opy_[bstack1lll11111l_opy_])
  if bstack1l1l1ll_opy_ (u"ࠧࡢࡴࡪࡷࠬॶ") in bstack1l1ll1l11_opy_:
    for arg in bstack1l1ll1l11_opy_[bstack1l1l1ll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ॷ")]:
      options.add_argument(arg)
    del (bstack1l1ll1l11_opy_[bstack1l1l1ll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॸ")])
  if bstack1l1l1ll_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧॹ") in bstack1l1ll1l11_opy_:
    for ext in bstack1l1ll1l11_opy_[bstack1l1l1ll_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨॺ")]:
      try:
        options.add_extension(ext)
      except OSError:
        options.add_encoded_extension(ext)
    del (bstack1l1ll1l11_opy_[bstack1l1l1ll_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩॻ")])
def bstack1lll111l_opy_(options, bstack1l111l1l1l_opy_):
  if bstack1l1l1ll_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬॼ") in bstack1l111l1l1l_opy_:
    for bstack1111ll11_opy_ in bstack1l111l1l1l_opy_[bstack1l1l1ll_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ॽ")]:
      if bstack1111ll11_opy_ in options._preferences:
        options._preferences[bstack1111ll11_opy_] = update(options._preferences[bstack1111ll11_opy_], bstack1l111l1l1l_opy_[bstack1l1l1ll_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧॾ")][bstack1111ll11_opy_])
      else:
        options.set_preference(bstack1111ll11_opy_, bstack1l111l1l1l_opy_[bstack1l1l1ll_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨॿ")][bstack1111ll11_opy_])
  if bstack1l1l1ll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨঀ") in bstack1l111l1l1l_opy_:
    for arg in bstack1l111l1l1l_opy_[bstack1l1l1ll_opy_ (u"ࠫࡦࡸࡧࡴࠩঁ")]:
      options.add_argument(arg)
def bstack1l1111l1l_opy_(options, bstack11llllll_opy_):
  if bstack1l1l1ll_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼ࠭ং") in bstack11llllll_opy_:
    options.use_webview(bool(bstack11llllll_opy_[bstack1l1l1ll_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࠧঃ")]))
  bstack1l1l1lllll_opy_(options, bstack11llllll_opy_)
def bstack11l1l11111_opy_(options, bstack11llll1l1l_opy_):
  for bstack11lll11ll_opy_ in bstack11llll1l1l_opy_:
    if bstack11lll11ll_opy_ in [bstack1l1l1ll_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫ঄"), bstack1l1l1ll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭অ")]:
      continue
    options.set_capability(bstack11lll11ll_opy_, bstack11llll1l1l_opy_[bstack11lll11ll_opy_])
  if bstack1l1l1ll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧআ") in bstack11llll1l1l_opy_:
    for arg in bstack11llll1l1l_opy_[bstack1l1l1ll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨই")]:
      options.add_argument(arg)
  if bstack1l1l1ll_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨঈ") in bstack11llll1l1l_opy_:
    options.bstack1l1111l11_opy_(bool(bstack11llll1l1l_opy_[bstack1l1l1ll_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩউ")]))
def bstack1l1lll1lll_opy_(options, bstack1l1111111l_opy_):
  for bstack1l1ll111l1_opy_ in bstack1l1111111l_opy_:
    if bstack1l1ll111l1_opy_ in [bstack1l1l1ll_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪঊ"), bstack1l1l1ll_opy_ (u"ࠧࡢࡴࡪࡷࠬঋ")]:
      continue
    options._options[bstack1l1ll111l1_opy_] = bstack1l1111111l_opy_[bstack1l1ll111l1_opy_]
  if bstack1l1l1ll_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬঌ") in bstack1l1111111l_opy_:
    for bstack1111lll1l_opy_ in bstack1l1111111l_opy_[bstack1l1l1ll_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭঍")]:
      options.bstack1l11l1ll11_opy_(
        bstack1111lll1l_opy_, bstack1l1111111l_opy_[bstack1l1l1ll_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ঎")][bstack1111lll1l_opy_])
  if bstack1l1l1ll_opy_ (u"ࠫࡦࡸࡧࡴࠩএ") in bstack1l1111111l_opy_:
    for arg in bstack1l1111111l_opy_[bstack1l1l1ll_opy_ (u"ࠬࡧࡲࡨࡵࠪঐ")]:
      options.add_argument(arg)
def bstack1l1lllll11_opy_(options, caps):
  if not hasattr(options, bstack1l1l1ll_opy_ (u"࠭ࡋࡆ࡛ࠪ঑")):
    return
  if options.KEY == bstack1l1l1ll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ঒"):
    options = bstack1lll11l1ll_opy_.bstack11llll1ll_opy_(bstack1l1l1ll11_opy_=options, config=CONFIG)
  if options.KEY == bstack1l1l1ll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ও") and options.KEY in caps:
    bstack1l1l1lllll_opy_(options, caps[bstack1l1l1ll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧঔ")])
  elif options.KEY == bstack1l1l1ll_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨক") and options.KEY in caps:
    bstack1lll111l_opy_(options, caps[bstack1l1l1ll_opy_ (u"ࠫࡲࡵࡺ࠻ࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩখ")])
  elif options.KEY == bstack1l1l1ll_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭গ") and options.KEY in caps:
    bstack11l1l11111_opy_(options, caps[bstack1l1l1ll_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧঘ")])
  elif options.KEY == bstack1l1l1ll_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨঙ") and options.KEY in caps:
    bstack1l1111l1l_opy_(options, caps[bstack1l1l1ll_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩচ")])
  elif options.KEY == bstack1l1l1ll_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨছ") and options.KEY in caps:
    bstack1l1lll1lll_opy_(options, caps[bstack1l1l1ll_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩজ")])
def bstack1lllll11ll_opy_(caps):
  global bstack1l111111l1_opy_
  if isinstance(os.environ.get(bstack1l1l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬঝ")), str):
    bstack1l111111l1_opy_ = eval(os.getenv(bstack1l1l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ঞ")))
  if bstack1l111111l1_opy_:
    if bstack111lll11l_opy_() < version.parse(bstack1l1l1ll_opy_ (u"࠭࠲࠯࠵࠱࠴ࠬট")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1l1l1ll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧঠ")
    if bstack1l1l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ড") in caps:
      browser = caps[bstack1l1l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧঢ")]
    elif bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫণ") in caps:
      browser = caps[bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬত")]
    browser = str(browser).lower()
    if browser == bstack1l1l1ll_opy_ (u"ࠬ࡯ࡰࡩࡱࡱࡩࠬথ") or browser == bstack1l1l1ll_opy_ (u"࠭ࡩࡱࡣࡧࠫদ"):
      browser = bstack1l1l1ll_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧধ")
    if browser == bstack1l1l1ll_opy_ (u"ࠨࡵࡤࡱࡸࡻ࡮ࡨࠩন"):
      browser = bstack1l1l1ll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩ঩")
    if browser not in [bstack1l1l1ll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪপ"), bstack1l1l1ll_opy_ (u"ࠫࡪࡪࡧࡦࠩফ"), bstack1l1l1ll_opy_ (u"ࠬ࡯ࡥࠨব"), bstack1l1l1ll_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭ভ"), bstack1l1l1ll_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨম")]:
      return None
    try:
      package = bstack1l1l1ll_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷ࠴ࡻࡾ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪয").format(browser)
      name = bstack1l1l1ll_opy_ (u"ࠩࡒࡴࡹ࡯࡯࡯ࡵࠪর")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1l1111ll1_opy_(options):
        return None
      for bstack1ll1l111ll_opy_ in caps.keys():
        options.set_capability(bstack1ll1l111ll_opy_, caps[bstack1ll1l111ll_opy_])
      bstack1l1lllll11_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1l1111l11l_opy_(options, bstack1lll1111ll_opy_):
  if not bstack1l1111ll1_opy_(options):
    return
  for bstack1ll1l111ll_opy_ in bstack1lll1111ll_opy_.keys():
    if bstack1ll1l111ll_opy_ in bstack11ll1lll1_opy_:
      continue
    if bstack1ll1l111ll_opy_ in options._caps and type(options._caps[bstack1ll1l111ll_opy_]) in [dict, list]:
      options._caps[bstack1ll1l111ll_opy_] = update(options._caps[bstack1ll1l111ll_opy_], bstack1lll1111ll_opy_[bstack1ll1l111ll_opy_])
    else:
      options.set_capability(bstack1ll1l111ll_opy_, bstack1lll1111ll_opy_[bstack1ll1l111ll_opy_])
  bstack1l1lllll11_opy_(options, bstack1lll1111ll_opy_)
  if bstack1l1l1ll_opy_ (u"ࠪࡱࡴࢀ࠺ࡥࡧࡥࡹ࡬࡭ࡥࡳࡃࡧࡨࡷ࡫ࡳࡴࠩ঱") in options._caps:
    if options._caps[bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩল")] and options._caps[bstack1l1l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ঳")].lower() != bstack1l1l1ll_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧ঴"):
      del options._caps[bstack1l1l1ll_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ࠭঵")]
def bstack1lll1l11l_opy_(proxy_config):
  if bstack1l1l1ll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬশ") in proxy_config:
    proxy_config[bstack1l1l1ll_opy_ (u"ࠩࡶࡷࡱࡖࡲࡰࡺࡼࠫষ")] = proxy_config[bstack1l1l1ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧস")]
    del (proxy_config[bstack1l1l1ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨহ")])
  if bstack1l1l1ll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ঺") in proxy_config and proxy_config[bstack1l1l1ll_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩ঻")].lower() != bstack1l1l1ll_opy_ (u"ࠧࡥ࡫ࡵࡩࡨࡺ়ࠧ"):
    proxy_config[bstack1l1l1ll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫঽ")] = bstack1l1l1ll_opy_ (u"ࠩࡰࡥࡳࡻࡡ࡭ࠩা")
  if bstack1l1l1ll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡃࡸࡸࡴࡩ࡯࡯ࡨ࡬࡫࡚ࡸ࡬ࠨি") in proxy_config:
    proxy_config[bstack1l1l1ll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧী")] = bstack1l1l1ll_opy_ (u"ࠬࡶࡡࡤࠩু")
  return proxy_config
def bstack1ll1l11lll_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1l1l1ll_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬূ") in config:
    return proxy
  config[bstack1l1l1ll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭ৃ")] = bstack1lll1l11l_opy_(config[bstack1l1l1ll_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧৄ")])
  if proxy == None:
    proxy = Proxy(config[bstack1l1l1ll_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨ৅")])
  return proxy
def bstack11l1ll11l_opy_(self):
  global CONFIG
  global bstack1llllll1l1_opy_
  try:
    proxy = bstack11l111ll1l_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1l1l1ll_opy_ (u"ࠪ࠲ࡵࡧࡣࠨ৆")):
        proxies = bstack11ll111l1_opy_(proxy, bstack11lll1lll_opy_())
        if len(proxies) > 0:
          protocol, bstack1l111l1l1_opy_ = proxies.popitem()
          if bstack1l1l1ll_opy_ (u"ࠦ࠿࠵࠯ࠣে") in bstack1l111l1l1_opy_:
            return bstack1l111l1l1_opy_
          else:
            return bstack1l1l1ll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨৈ") + bstack1l111l1l1_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1l1l1ll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡳࡶࡴࡾࡹࠡࡷࡵࡰࠥࡀࠠࡼࡿࠥ৉").format(str(e)))
  return bstack1llllll1l1_opy_(self)
def bstack1lll111l1l_opy_():
  global CONFIG
  return bstack1l11l1ll1_opy_(CONFIG) and bstack1ll1lll11l_opy_() and bstack1l111111l_opy_() >= version.parse(bstack1111l1l11_opy_)
def bstack11ll11111l_opy_():
  global CONFIG
  return (bstack1l1l1ll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ৊") in CONFIG or bstack1l1l1ll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬো") in CONFIG) and bstack1ll1l11111_opy_()
def bstack1ll1llllll_opy_(config):
  bstack1111l1111_opy_ = {}
  if bstack1l1l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ৌ") in config:
    bstack1111l1111_opy_ = config[bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹ্ࠧ")]
  if bstack1l1l1ll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪৎ") in config:
    bstack1111l1111_opy_ = config[bstack1l1l1ll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ৏")]
  proxy = bstack11l111ll1l_opy_(config)
  if proxy:
    if proxy.endswith(bstack1l1l1ll_opy_ (u"࠭࠮ࡱࡣࡦࠫ৐")) and os.path.isfile(proxy):
      bstack1111l1111_opy_[bstack1l1l1ll_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪ৑")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1l1l1ll_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭৒")):
        proxies = bstack1lll1ll1_opy_(config, bstack11lll1lll_opy_())
        if len(proxies) > 0:
          protocol, bstack1l111l1l1_opy_ = proxies.popitem()
          if bstack1l1l1ll_opy_ (u"ࠤ࠽࠳࠴ࠨ৓") in bstack1l111l1l1_opy_:
            parsed_url = urlparse(bstack1l111l1l1_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1l1l1ll_opy_ (u"ࠥ࠾࠴࠵ࠢ৔") + bstack1l111l1l1_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1111l1111_opy_[bstack1l1l1ll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡋࡳࡸࡺࠧ৕")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1111l1111_opy_[bstack1l1l1ll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡴࡸࡴࠨ৖")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1111l1111_opy_[bstack1l1l1ll_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡚ࡹࡥࡳࠩৗ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1111l1111_opy_[bstack1l1l1ll_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖࡡࡴࡵࠪ৘")] = str(parsed_url.password)
  return bstack1111l1111_opy_
def bstack1ll11l1ll_opy_(config):
  if bstack1l1l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸ࠭৙") in config:
    return config[bstack1l1l1ll_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧ৚")]
  return {}
def bstack1l11l1l1ll_opy_(caps):
  global bstack11l11lll11_opy_
  if bstack1l1l1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ৛") in caps:
    caps[bstack1l1l1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬড়")][bstack1l1l1ll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫঢ়")] = True
    if bstack11l11lll11_opy_:
      caps[bstack1l1l1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ৞")][bstack1l1l1ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩয়")] = bstack11l11lll11_opy_
  else:
    caps[bstack1l1l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭ৠ")] = True
    if bstack11l11lll11_opy_:
      caps[bstack1l1l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪৡ")] = bstack11l11lll11_opy_
@measure(event_name=EVENTS.bstack11lllll11l_opy_, stage=STAGE.bstack1l1ll11l1_opy_, bstack111l1llll_opy_=bstack1llll111_opy_)
def bstack11l1l1111_opy_():
  global CONFIG
  if not bstack1l1l11llll_opy_(CONFIG) or cli.is_enabled(CONFIG):
    return
  if bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧৢ") in CONFIG and bstack11lll1ll11_opy_(CONFIG[bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨৣ")]):
    if (
      bstack1l1l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ৤") in CONFIG
      and bstack11lll1ll11_opy_(CONFIG[bstack1l1l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ৥")].get(bstack1l1l1ll_opy_ (u"ࠧࡴ࡭࡬ࡴࡇ࡯࡮ࡢࡴࡼࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡸࡧࡴࡪࡱࡱࠫ০")))
    ):
      logger.debug(bstack1l1l1ll_opy_ (u"ࠣࡎࡲࡧࡦࡲࠠࡣ࡫ࡱࡥࡷࡿࠠ࡯ࡱࡷࠤࡸࡺࡡࡳࡶࡨࡨࠥࡧࡳࠡࡵ࡮࡭ࡵࡈࡩ࡯ࡣࡵࡽࡎࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡡࡵ࡫ࡲࡲࠥ࡯ࡳࠡࡧࡱࡥࡧࡲࡥࡥࠤ১"))
      return
    bstack1111l1111_opy_ = bstack1ll1llllll_opy_(CONFIG)
    bstack1ll1l1l11_opy_(CONFIG[bstack1l1l1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ২")], bstack1111l1111_opy_)
def bstack1ll1l1l11_opy_(key, bstack1111l1111_opy_):
  global bstack1llll1l11_opy_
  logger.info(bstack111ll11l_opy_)
  try:
    bstack1llll1l11_opy_ = Local()
    bstack11l11ll111_opy_ = {bstack1l1l1ll_opy_ (u"ࠪ࡯ࡪࡿࠧ৩"): key}
    bstack11l11ll111_opy_.update(bstack1111l1111_opy_)
    logger.debug(bstack111lll11_opy_.format(str(bstack11l11ll111_opy_)).replace(key, bstack1l1l1ll_opy_ (u"ࠫࡠࡘࡅࡅࡃࡆࡘࡊࡊ࡝ࠨ৪")))
    bstack1llll1l11_opy_.start(**bstack11l11ll111_opy_)
    if bstack1llll1l11_opy_.isRunning():
      logger.info(bstack1lllllll1l_opy_)
  except Exception as e:
    bstack1l1l11l111_opy_(bstack11lll1ll_opy_.format(str(e)))
def bstack11ll11lll_opy_():
  global bstack1llll1l11_opy_
  if bstack1llll1l11_opy_.isRunning():
    logger.info(bstack11lllll111_opy_)
    bstack1llll1l11_opy_.stop()
  bstack1llll1l11_opy_ = None
def bstack1ll1111ll1_opy_(bstack1l11lll11_opy_=[]):
  global CONFIG
  bstack1l1l1lll_opy_ = []
  bstack1l111lll_opy_ = [bstack1l1l1ll_opy_ (u"ࠬࡵࡳࠨ৫"), bstack1l1l1ll_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ৬"), bstack1l1l1ll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ৭"), bstack1l1l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪ৮"), bstack1l1l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ৯"), bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫৰ")]
  try:
    for err in bstack1l11lll11_opy_:
      bstack11lll111_opy_ = {}
      for k in bstack1l111lll_opy_:
        val = CONFIG[bstack1l1l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧৱ")][int(err[bstack1l1l1ll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ৲")])].get(k)
        if val:
          bstack11lll111_opy_[k] = val
      if(err[bstack1l1l1ll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ৳")] != bstack1l1l1ll_opy_ (u"ࠧࠨ৴")):
        bstack11lll111_opy_[bstack1l1l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡹࠧ৵")] = {
          err[bstack1l1l1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ৶")]: err[bstack1l1l1ll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ৷")]
        }
        bstack1l1l1lll_opy_.append(bstack11lll111_opy_)
  except Exception as e:
    logger.debug(bstack1l1l1ll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡰࡴࡰࡥࡹࡺࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷ࠾ࠥ࠭৸") + str(e))
  finally:
    return bstack1l1l1lll_opy_
def bstack1ll1llll11_opy_(file_name):
  bstack1l11l1llll_opy_ = []
  try:
    bstack11ll11ll11_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack11ll11ll11_opy_):
      with open(bstack11ll11ll11_opy_) as f:
        bstack1ll1ll111_opy_ = json.load(f)
        bstack1l11l1llll_opy_ = bstack1ll1ll111_opy_
      os.remove(bstack11ll11ll11_opy_)
    return bstack1l11l1llll_opy_
  except Exception as e:
    logger.debug(bstack1l1l1ll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧ࡫ࡱࡨ࡮ࡴࡧࠡࡧࡵࡶࡴࡸࠠ࡭࡫ࡶࡸ࠿ࠦࠧ৹") + str(e))
    return bstack1l11l1llll_opy_
def bstack1ll1lllll_opy_():
  try:
      from bstack_utils.constants import bstack1111lllll_opy_, EVENTS
      from bstack_utils.helper import bstack1llll11ll1_opy_, get_host_info, bstack1l1l1111l1_opy_
      from datetime import datetime
      from filelock import FileLock
      bstack1lll1ll1l1_opy_ = os.path.join(os.getcwd(), bstack1l1l1ll_opy_ (u"࠭࡬ࡰࡩࠪ৺"), bstack1l1l1ll_opy_ (u"ࠧ࡬ࡧࡼ࠱ࡲ࡫ࡴࡳ࡫ࡦࡷ࠳ࡰࡳࡰࡰࠪ৻"))
      lock = FileLock(bstack1lll1ll1l1_opy_+bstack1l1l1ll_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢৼ"))
      def bstack11ll11l1ll_opy_():
          try:
              with lock:
                  with open(bstack1lll1ll1l1_opy_, bstack1l1l1ll_opy_ (u"ࠤࡵࠦ৽"), encoding=bstack1l1l1ll_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤ৾")) as file:
                      data = json.load(file)
                      config = {
                          bstack1l1l1ll_opy_ (u"ࠦ࡭࡫ࡡࡥࡧࡵࡷࠧ৿"): {
                              bstack1l1l1ll_opy_ (u"ࠧࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠦ਀"): bstack1l1l1ll_opy_ (u"ࠨࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠤਁ"),
                          }
                      }
                      bstack1l1l111ll_opy_ = datetime.utcnow()
                      bstack11lllll1_opy_ = bstack1l1l111ll_opy_.strftime(bstack1l1l1ll_opy_ (u"࡛ࠢࠦ࠰ࠩࡲ࠳ࠥࡥࡖࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࠲ࠪ࡬ࠠࡖࡖࡆࠦਂ"))
                      bstack11l1l1l11_opy_ = os.environ.get(bstack1l1l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ਃ")) if os.environ.get(bstack1l1l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ਄")) else bstack1l1l1111l1_opy_.get_property(bstack1l1l1ll_opy_ (u"ࠥࡷࡩࡱࡒࡶࡰࡌࡨࠧਅ"))
                      payload = {
                          bstack1l1l1ll_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠣਆ"): bstack1l1l1ll_opy_ (u"ࠧࡹࡤ࡬ࡡࡨࡺࡪࡴࡴࡴࠤਇ"),
                          bstack1l1l1ll_opy_ (u"ࠨࡤࡢࡶࡤࠦਈ"): {
                              bstack1l1l1ll_opy_ (u"ࠢࡵࡧࡶࡸ࡭ࡻࡢࡠࡷࡸ࡭ࡩࠨਉ"): bstack11l1l1l11_opy_,
                              bstack1l1l1ll_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡥࡡࡧࡥࡾࠨਊ"): bstack11lllll1_opy_,
                              bstack1l1l1ll_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡰࡤࡱࡪࠨ਋"): bstack1l1l1ll_opy_ (u"ࠥࡗࡉࡑࡆࡦࡣࡷࡹࡷ࡫ࡐࡦࡴࡩࡳࡷࡳࡡ࡯ࡥࡨࠦ਌"),
                              bstack1l1l1ll_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢ࡮ࡸࡵ࡮ࠣ਍"): {
                                  bstack1l1l1ll_opy_ (u"ࠧࡳࡥࡢࡵࡸࡶࡪࡹࠢ਎"): data,
                                  bstack1l1l1ll_opy_ (u"ࠨࡳࡥ࡭ࡕࡹࡳࡏࡤࠣਏ"): bstack1l1l1111l1_opy_.get_property(bstack1l1l1ll_opy_ (u"ࠢࡴࡦ࡮ࡖࡺࡴࡉࡥࠤਐ"))
                              },
                              bstack1l1l1ll_opy_ (u"ࠣࡷࡶࡩࡷࡥࡤࡢࡶࡤࠦ਑"): bstack1l1l1111l1_opy_.get_property(bstack1l1l1ll_opy_ (u"ࠤࡸࡷࡪࡸࡎࡢ࡯ࡨࠦ਒")),
                              bstack1l1l1ll_opy_ (u"ࠥ࡬ࡴࡹࡴࡠ࡫ࡱࡪࡴࠨਓ"): get_host_info()
                          }
                      }
                      bstack1l1l111111_opy_ = bstack1ll11llll_opy_(cli.config, [bstack1l1l1ll_opy_ (u"ࠦࡦࡶࡩࡴࠤਔ"), bstack1l1l1ll_opy_ (u"ࠧ࡫ࡤࡴࡋࡱࡷࡹࡸࡵ࡮ࡧࡱࡸࡦࡺࡩࡰࡰࠥਕ"), bstack1l1l1ll_opy_ (u"ࠨࡡࡱ࡫ࠥਖ")], bstack1111lllll_opy_)
                      response = bstack1llll11ll1_opy_(bstack1l1l1ll_opy_ (u"ࠢࡑࡑࡖࡘࠧਗ"), bstack1l1l111111_opy_, payload, config)
                      if(response.status_code >= 200 and response.status_code < 300):
                          logger.debug(bstack1l1l1ll_opy_ (u"ࠣࡆࡤࡸࡦࠦࡳࡦࡰࡷࠤࡸࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻࠣࡸࡴࠦࡻࡾࠢࡺ࡭ࡹ࡮ࠠࡥࡣࡷࡥࠥࢁࡽࠣਘ").format(bstack1111lllll_opy_, payload))
                      else:
                          logger.debug(bstack1l1l1ll_opy_ (u"ࠤࡕࡩࡶࡻࡥࡴࡶࠣࡪࡦ࡯࡬ࡦࡦࠣࡪࡴࡸࠠࡼࡿࠣࡻ࡮ࡺࡨࠡࡦࡤࡸࡦࠦࡻࡾࠤਙ").format(bstack1111lllll_opy_, payload))
          except Exception as e:
              logger.debug(bstack1l1l1ll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡰࡧࠤࡰ࡫ࡹࠡ࡯ࡨࡸࡷ࡯ࡣࡴࠢࡧࡥࡹࡧࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵࠤࢀࢃࠢਚ").format(e))
      bstack11ll11l1ll_opy_()
      bstack1l1lll11l1_opy_(bstack1lll1ll1l1_opy_, logger)
  except:
    pass
def bstack1ll11lll11_opy_():
  global bstack1llll1l11l_opy_
  global bstack1lll1l1l1l_opy_
  global bstack1l1l11l1l1_opy_
  global bstack1ll1111l1_opy_
  global bstack1l11111l_opy_
  global bstack1l1l1l11l_opy_
  global CONFIG
  bstack1l1lll1ll_opy_ = os.environ.get(bstack1l1l1ll_opy_ (u"ࠫࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ࡟ࡖࡕࡈࡈࠬਛ"))
  if bstack1l1lll1ll_opy_ in [bstack1l1l1ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫਜ"), bstack1l1l1ll_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬਝ")]:
    bstack11ll1ll11_opy_()
  percy.shutdown()
  if bstack1llll1l11l_opy_:
    logger.warning(bstack1ll11l1l1l_opy_.format(str(bstack1llll1l11l_opy_)))
  else:
    try:
      bstack1ll1l111_opy_ = bstack1lllll1l11_opy_(bstack1l1l1ll_opy_ (u"ࠧ࠯ࡤࡶࡸࡦࡩ࡫࠮ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭ਞ"), logger)
      if bstack1ll1l111_opy_.get(bstack1l1l1ll_opy_ (u"ࠨࡰࡸࡨ࡬࡫࡟࡭ࡱࡦࡥࡱ࠭ਟ")) and bstack1ll1l111_opy_.get(bstack1l1l1ll_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧਠ")).get(bstack1l1l1ll_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬਡ")):
        logger.warning(bstack1ll11l1l1l_opy_.format(str(bstack1ll1l111_opy_[bstack1l1l1ll_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩਢ")][bstack1l1l1ll_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧਣ")])))
    except Exception as e:
      logger.error(e)
  if cli.is_running():
    bstack1111lll11_opy_.invoke(bstack11ll1111ll_opy_.bstack1ll1l1lll1_opy_)
  logger.info(bstack1lll11ll1l_opy_)
  global bstack1llll1l11_opy_
  if bstack1llll1l11_opy_:
    bstack11ll11lll_opy_()
  try:
    with bstack1l1l111l1_opy_:
      bstack1ll111l1l1_opy_ = bstack1lll1l1l1l_opy_.copy()
    for driver in bstack1ll111l1l1_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1lllll1l1_opy_)
  if bstack1l1l1l11l_opy_ == bstack1l1l1ll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬਤ"):
    bstack1l11111l_opy_ = bstack1ll1llll11_opy_(bstack1l1l1ll_opy_ (u"ࠧࡳࡱࡥࡳࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨਥ"))
  if bstack1l1l1l11l_opy_ == bstack1l1l1ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨਦ") and len(bstack1ll1111l1_opy_) == 0:
    bstack1ll1111l1_opy_ = bstack1ll1llll11_opy_(bstack1l1l1ll_opy_ (u"ࠩࡳࡻࡤࡶࡹࡵࡧࡶࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧਧ"))
    if len(bstack1ll1111l1_opy_) == 0:
      bstack1ll1111l1_opy_ = bstack1ll1llll11_opy_(bstack1l1l1ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡴࡵࡶ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩਨ"))
  bstack1l11lll1l1_opy_ = bstack1l1l1ll_opy_ (u"ࠫࠬ਩")
  if len(bstack1l1l11l1l1_opy_) > 0:
    bstack1l11lll1l1_opy_ = bstack1ll1111ll1_opy_(bstack1l1l11l1l1_opy_)
  elif len(bstack1ll1111l1_opy_) > 0:
    bstack1l11lll1l1_opy_ = bstack1ll1111ll1_opy_(bstack1ll1111l1_opy_)
  elif len(bstack1l11111l_opy_) > 0:
    bstack1l11lll1l1_opy_ = bstack1ll1111ll1_opy_(bstack1l11111l_opy_)
  elif len(bstack1l1lll1l1_opy_) > 0:
    bstack1l11lll1l1_opy_ = bstack1ll1111ll1_opy_(bstack1l1lll1l1_opy_)
  if bool(bstack1l11lll1l1_opy_):
    bstack11l111ll_opy_(bstack1l11lll1l1_opy_)
  else:
    bstack11l111ll_opy_()
  bstack1l1lll11l1_opy_(bstack1ll1ll1l11_opy_, logger)
  if bstack1l1lll1ll_opy_ not in [bstack1l1l1ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ਪ")]:
    bstack1ll1lllll_opy_()
  bstack1l1l11lll1_opy_.bstack1lll1ll11l_opy_(CONFIG)
  if len(bstack1l11111l_opy_) > 0:
    sys.exit(len(bstack1l11111l_opy_))
def bstack111ll1111_opy_(bstack11ll1l11_opy_, frame):
  global bstack1l1l1111l1_opy_
  logger.error(bstack111111l11_opy_)
  bstack1l1l1111l1_opy_.bstack1l1ll11111_opy_(bstack1l1l1ll_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡎࡰࠩਫ"), bstack11ll1l11_opy_)
  if hasattr(signal, bstack1l1l1ll_opy_ (u"ࠧࡔ࡫ࡪࡲࡦࡲࡳࠨਬ")):
    bstack1l1l1111l1_opy_.bstack1l1ll11111_opy_(bstack1l1l1ll_opy_ (u"ࠨࡵࡧ࡯ࡐ࡯࡬࡭ࡕ࡬࡫ࡳࡧ࡬ࠨਭ"), signal.Signals(bstack11ll1l11_opy_).name)
  else:
    bstack1l1l1111l1_opy_.bstack1l1ll11111_opy_(bstack1l1l1ll_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩਮ"), bstack1l1l1ll_opy_ (u"ࠪࡗࡎࡍࡕࡏࡍࡑࡓ࡜ࡔࠧਯ"))
  if cli.is_running():
    bstack1111lll11_opy_.invoke(bstack11ll1111ll_opy_.bstack1ll1l1lll1_opy_)
  bstack1l1lll1ll_opy_ = os.environ.get(bstack1l1l1ll_opy_ (u"ࠫࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ࡟ࡖࡕࡈࡈࠬਰ"))
  if bstack1l1lll1ll_opy_ == bstack1l1l1ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ਱") and not cli.is_enabled(CONFIG):
    bstack1llllll11l_opy_.stop(bstack1l1l1111l1_opy_.get_property(bstack1l1l1ll_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭ਲ")))
  bstack1ll11lll11_opy_()
  sys.exit(1)
def bstack1l1l11l111_opy_(err):
  logger.critical(bstack1lll111l11_opy_.format(str(err)))
  bstack11l111ll_opy_(bstack1lll111l11_opy_.format(str(err)), True)
  atexit.unregister(bstack1ll11lll11_opy_)
  bstack11ll1ll11_opy_()
  sys.exit(1)
def bstack1ll111lll_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack11l111ll_opy_(message, True)
  atexit.unregister(bstack1ll11lll11_opy_)
  bstack11ll1ll11_opy_()
  sys.exit(1)
def bstack11l1l1ll11_opy_():
  global CONFIG
  global bstack1ll11ll11_opy_
  global bstack11l1lll1_opy_
  global bstack1lllll111l_opy_
  CONFIG = bstack1ll11l111_opy_()
  load_dotenv(CONFIG.get(bstack1l1l1ll_opy_ (u"ࠧࡦࡰࡹࡊ࡮ࡲࡥࠨਲ਼")))
  bstack11l1l1ll1l_opy_()
  bstack1l1l111l11_opy_()
  CONFIG = bstack11lll1ll1_opy_(CONFIG)
  update(CONFIG, bstack11l1lll1_opy_)
  update(CONFIG, bstack1ll11ll11_opy_)
  if not cli.is_enabled(CONFIG):
    CONFIG = bstack1llll11l1_opy_(CONFIG)
  bstack1lllll111l_opy_ = bstack1l1l11llll_opy_(CONFIG)
  os.environ[bstack1l1l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫ਴")] = bstack1lllll111l_opy_.__str__().lower()
  bstack1l1l1111l1_opy_.bstack1l1ll11111_opy_(bstack1l1l1ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪਵ"), bstack1lllll111l_opy_)
  if (bstack1l1l1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ਸ਼") in CONFIG and bstack1l1l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ਷") in bstack1ll11ll11_opy_) or (
          bstack1l1l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨਸ") in CONFIG and bstack1l1l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩਹ") not in bstack11l1lll1_opy_):
    if os.getenv(bstack1l1l1ll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫ਺")):
      CONFIG[bstack1l1l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ਻")] = os.getenv(bstack1l1l1ll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ਼࠭"))
    else:
      if not CONFIG.get(bstack1l1l1ll_opy_ (u"ࠥࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠨ਽"), bstack1l1l1ll_opy_ (u"ࠦࠧਾ")) in bstack1l1111l1l1_opy_:
        bstack1l1lll1l_opy_()
  elif (bstack1l1l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨਿ") not in CONFIG and bstack1l1l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨੀ") in CONFIG) or (
          bstack1l1l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪੁ") in bstack11l1lll1_opy_ and bstack1l1l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫੂ") not in bstack1ll11ll11_opy_):
    del (CONFIG[bstack1l1l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ੃")])
  if bstack1ll11111l_opy_(CONFIG):
    bstack1l1l11l111_opy_(bstack11ll111l_opy_)
  Config.bstack11l1lllll1_opy_().bstack1l1ll11111_opy_(bstack1l1l1ll_opy_ (u"ࠥࡹࡸ࡫ࡲࡏࡣࡰࡩࠧ੄"), CONFIG[bstack1l1l1ll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭੅")])
  bstack11lll1l11l_opy_()
  bstack111ll111_opy_()
  if bstack1l111111l1_opy_ and not CONFIG.get(bstack1l1l1ll_opy_ (u"ࠧ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠣ੆"), bstack1l1l1ll_opy_ (u"ࠨࠢੇ")) in bstack1l1111l1l1_opy_:
    CONFIG[bstack1l1l1ll_opy_ (u"ࠧࡢࡲࡳࠫੈ")] = bstack11lll111l_opy_(CONFIG)
    logger.info(bstack11l1111l_opy_.format(CONFIG[bstack1l1l1ll_opy_ (u"ࠨࡣࡳࡴࠬ੉")]))
  if not bstack1lllll111l_opy_:
    CONFIG[bstack1l1l1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ੊")] = [{}]
def bstack1l11ll1l_opy_(config, bstack1ll111ll1l_opy_):
  global CONFIG
  global bstack1l111111l1_opy_
  CONFIG = config
  bstack1l111111l1_opy_ = bstack1ll111ll1l_opy_
def bstack111ll111_opy_():
  global CONFIG
  global bstack1l111111l1_opy_
  if bstack1l1l1ll_opy_ (u"ࠪࡥࡵࡶࠧੋ") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1ll111lll_opy_(e, bstack1l1ll111ll_opy_)
    bstack1l111111l1_opy_ = True
    bstack1l1l1111l1_opy_.bstack1l1ll11111_opy_(bstack1l1l1ll_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪੌ"), True)
def bstack11lll111l_opy_(config):
  bstack1ll1ll11_opy_ = bstack1l1l1ll_opy_ (u"੍ࠬ࠭")
  app = config[bstack1l1l1ll_opy_ (u"࠭ࡡࡱࡲࠪ੎")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1l111ll1l1_opy_:
      if os.path.exists(app):
        bstack1ll1ll11_opy_ = bstack1l11l111ll_opy_(config, app)
      elif bstack1ll1l11ll1_opy_(app):
        bstack1ll1ll11_opy_ = app
      else:
        bstack1l1l11l111_opy_(bstack111l11l11_opy_.format(app))
    else:
      if bstack1ll1l11ll1_opy_(app):
        bstack1ll1ll11_opy_ = app
      elif os.path.exists(app):
        bstack1ll1ll11_opy_ = bstack1l11l111ll_opy_(app)
      else:
        bstack1l1l11l111_opy_(bstack11l111lll1_opy_)
  else:
    if len(app) > 2:
      bstack1l1l11l111_opy_(bstack1l11ll1ll1_opy_)
    elif len(app) == 2:
      if bstack1l1l1ll_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ੏") in app and bstack1l1l1ll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫ੐") in app:
        if os.path.exists(app[bstack1l1l1ll_opy_ (u"ࠩࡳࡥࡹ࡮ࠧੑ")]):
          bstack1ll1ll11_opy_ = bstack1l11l111ll_opy_(config, app[bstack1l1l1ll_opy_ (u"ࠪࡴࡦࡺࡨࠨ੒")], app[bstack1l1l1ll_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧ੓")])
        else:
          bstack1l1l11l111_opy_(bstack111l11l11_opy_.format(app))
      else:
        bstack1l1l11l111_opy_(bstack1l11ll1ll1_opy_)
    else:
      for key in app:
        if key in bstack1l1l1ll1ll_opy_:
          if key == bstack1l1l1ll_opy_ (u"ࠬࡶࡡࡵࡪࠪ੔"):
            if os.path.exists(app[key]):
              bstack1ll1ll11_opy_ = bstack1l11l111ll_opy_(config, app[key])
            else:
              bstack1l1l11l111_opy_(bstack111l11l11_opy_.format(app))
          else:
            bstack1ll1ll11_opy_ = app[key]
        else:
          bstack1l1l11l111_opy_(bstack11l1ll1l1l_opy_)
  return bstack1ll1ll11_opy_
def bstack1ll1l11ll1_opy_(bstack1ll1ll11_opy_):
  import re
  bstack1lll11l1_opy_ = re.compile(bstack1l1l1ll_opy_ (u"ࡸࠢ࡟࡝ࡤ࠱ࡿࡇ࡛࠭࠲࠰࠽ࡡࡥ࠮࡝࠯ࡠ࠮ࠩࠨ੕"))
  bstack11l1111ll_opy_ = re.compile(bstack1l1l1ll_opy_ (u"ࡲࠣࡠ࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯࠵࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬࠧࠦ੖"))
  if bstack1l1l1ll_opy_ (u"ࠨࡤࡶ࠾࠴࠵ࠧ੗") in bstack1ll1ll11_opy_ or re.fullmatch(bstack1lll11l1_opy_, bstack1ll1ll11_opy_) or re.fullmatch(bstack11l1111ll_opy_, bstack1ll1ll11_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack1111llll_opy_, stage=STAGE.bstack1l1ll11l1_opy_, bstack111l1llll_opy_=bstack1llll111_opy_)
def bstack1l11l111ll_opy_(config, path, bstack1l11llll1l_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1l1l1ll_opy_ (u"ࠩࡵࡦࠬ੘")).read()).hexdigest()
  bstack11l1l1lll1_opy_ = bstack1111llll1_opy_(md5_hash)
  bstack1ll1ll11_opy_ = None
  if bstack11l1l1lll1_opy_:
    logger.info(bstack1ll11l1l_opy_.format(bstack11l1l1lll1_opy_, md5_hash))
    return bstack11l1l1lll1_opy_
  bstack1lll111ll1_opy_ = datetime.datetime.now()
  bstack11ll11ll1l_opy_ = MultipartEncoder(
    fields={
      bstack1l1l1ll_opy_ (u"ࠪࡪ࡮ࡲࡥࠨਖ਼"): (os.path.basename(path), open(os.path.abspath(path), bstack1l1l1ll_opy_ (u"ࠫࡷࡨࠧਗ਼")), bstack1l1l1ll_opy_ (u"ࠬࡺࡥࡹࡶ࠲ࡴࡱࡧࡩ࡯ࠩਜ਼")),
      bstack1l1l1ll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩੜ"): bstack1l11llll1l_opy_
    }
  )
  response = requests.post(bstack1l11ll1l11_opy_, data=bstack11ll11ll1l_opy_,
                           headers={bstack1l1l1ll_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭੝"): bstack11ll11ll1l_opy_.content_type},
                           auth=(config[bstack1l1l1ll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪਫ਼")], config[bstack1l1l1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ੟")]))
  try:
    res = json.loads(response.text)
    bstack1ll1ll11_opy_ = res[bstack1l1l1ll_opy_ (u"ࠪࡥࡵࡶ࡟ࡶࡴ࡯ࠫ੠")]
    logger.info(bstack11ll11l1l1_opy_.format(bstack1ll1ll11_opy_))
    bstack11l1111ll1_opy_(md5_hash, bstack1ll1ll11_opy_)
    cli.bstack1ll1ll11ll_opy_(bstack1l1l1ll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼ࡸࡴࡱࡵࡡࡥࡡࡤࡴࡵࠨ੡"), datetime.datetime.now() - bstack1lll111ll1_opy_)
  except ValueError as err:
    bstack1l1l11l111_opy_(bstack1llllll111_opy_.format(str(err)))
  return bstack1ll1ll11_opy_
def bstack11lll1l11l_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack1ll1l1l1l1_opy_
  bstack1111l1ll_opy_ = 1
  bstack1llll11l11_opy_ = 1
  if bstack1l1l1ll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ੢") in CONFIG:
    bstack1llll11l11_opy_ = CONFIG[bstack1l1l1ll_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭੣")]
  else:
    bstack1llll11l11_opy_ = bstack111l111l_opy_(framework_name, args) or 1
  if bstack1l1l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ੤") in CONFIG:
    bstack1111l1ll_opy_ = len(CONFIG[bstack1l1l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ੥")])
  bstack1ll1l1l1l1_opy_ = int(bstack1llll11l11_opy_) * int(bstack1111l1ll_opy_)
def bstack111l111l_opy_(framework_name, args):
  if framework_name == bstack11l1lll1l_opy_ and args and bstack1l1l1ll_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ੦") in args:
      bstack1l11l1ll_opy_ = args.index(bstack1l1l1ll_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨ੧"))
      return int(args[bstack1l11l1ll_opy_ + 1]) or 1
  return 1
def bstack1111llll1_opy_(md5_hash):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l1l1ll_opy_ (u"ࠫ࡫࡯࡬ࡦ࡮ࡲࡧࡰࠦ࡮ࡰࡶࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪ࠲ࠠࡶࡵ࡬ࡲ࡬ࠦࡢࡢࡵ࡬ࡧࠥ࡬ࡩ࡭ࡧࠣࡳࡵ࡫ࡲࡢࡶ࡬ࡳࡳࡹࠧ੨"))
    bstack11l11ll1l1_opy_ = os.path.join(os.path.expanduser(bstack1l1l1ll_opy_ (u"ࠬࢄࠧ੩")), bstack1l1l1ll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭੪"), bstack1l1l1ll_opy_ (u"ࠧࡢࡲࡳ࡙ࡵࡲ࡯ࡢࡦࡐࡈ࠺ࡎࡡࡴࡪ࠱࡮ࡸࡵ࡮ࠨ੫"))
    if os.path.exists(bstack11l11ll1l1_opy_):
      try:
        bstack111llll1l_opy_ = json.load(open(bstack11l11ll1l1_opy_, bstack1l1l1ll_opy_ (u"ࠨࡴࡥࠫ੬")))
        if md5_hash in bstack111llll1l_opy_:
          bstack1l1111ll11_opy_ = bstack111llll1l_opy_[md5_hash]
          bstack1111lll1_opy_ = datetime.datetime.now()
          bstack1111l1ll1_opy_ = datetime.datetime.strptime(bstack1l1111ll11_opy_[bstack1l1l1ll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ੭")], bstack1l1l1ll_opy_ (u"ࠪࠩࡩ࠵ࠥ࡮࠱ࠨ࡝ࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧ੮"))
          if (bstack1111lll1_opy_ - bstack1111l1ll1_opy_).days > 30:
            return None
          elif version.parse(str(__version__)) > version.parse(bstack1l1111ll11_opy_[bstack1l1l1ll_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ੯")]):
            return None
          return bstack1l1111ll11_opy_[bstack1l1l1ll_opy_ (u"ࠬ࡯ࡤࠨੰ")]
      except Exception as e:
        logger.debug(bstack1l1l1ll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡸࡥࡢࡦ࡬ࡲ࡬ࠦࡍࡅ࠷ࠣ࡬ࡦࡹࡨࠡࡨ࡬ࡰࡪࡀࠠࡼࡿࠪੱ").format(str(e)))
    return None
  bstack11l11ll1l1_opy_ = os.path.join(os.path.expanduser(bstack1l1l1ll_opy_ (u"ࠧࡿࠩੲ")), bstack1l1l1ll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨੳ"), bstack1l1l1ll_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪੴ"))
  lock_file = bstack11l11ll1l1_opy_ + bstack1l1l1ll_opy_ (u"ࠪ࠲ࡱࡵࡣ࡬ࠩੵ")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack11l11ll1l1_opy_):
        with open(bstack11l11ll1l1_opy_, bstack1l1l1ll_opy_ (u"ࠫࡷ࠭੶")) as f:
          content = f.read().strip()
          if content:
            bstack111llll1l_opy_ = json.loads(content)
            if md5_hash in bstack111llll1l_opy_:
              bstack1l1111ll11_opy_ = bstack111llll1l_opy_[md5_hash]
              bstack1111lll1_opy_ = datetime.datetime.now()
              bstack1111l1ll1_opy_ = datetime.datetime.strptime(bstack1l1111ll11_opy_[bstack1l1l1ll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ੷")], bstack1l1l1ll_opy_ (u"࠭ࠥࡥ࠱ࠨࡱ࠴࡙ࠫࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪ੸"))
              if (bstack1111lll1_opy_ - bstack1111l1ll1_opy_).days > 30:
                return None
              elif version.parse(str(__version__)) > version.parse(bstack1l1111ll11_opy_[bstack1l1l1ll_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ੹")]):
                return None
              return bstack1l1111ll11_opy_[bstack1l1l1ll_opy_ (u"ࠨ࡫ࡧࠫ੺")]
      return None
  except Exception as e:
    logger.debug(bstack1l1l1ll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡹ࡬ࡸ࡭ࠦࡦࡪ࡮ࡨࠤࡱࡵࡣ࡬࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡐࡈ࠺ࠦࡨࡢࡵ࡫࠾ࠥࢁࡽࠨ੻").format(str(e)))
    return None
def bstack11l1111ll1_opy_(md5_hash, bstack1ll1ll11_opy_):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l1l1ll_opy_ (u"ࠪࡪ࡮ࡲࡥ࡭ࡱࡦ࡯ࠥࡴ࡯ࡵࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩ࠱ࠦࡵࡴ࡫ࡱ࡫ࠥࡨࡡࡴ࡫ࡦࠤ࡫࡯࡬ࡦࠢࡲࡴࡪࡸࡡࡵ࡫ࡲࡲࡸ࠭੼"))
    bstack1lll11llll_opy_ = os.path.join(os.path.expanduser(bstack1l1l1ll_opy_ (u"ࠫࢃ࠭੽")), bstack1l1l1ll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ੾"))
    if not os.path.exists(bstack1lll11llll_opy_):
      os.makedirs(bstack1lll11llll_opy_)
    bstack11l11ll1l1_opy_ = os.path.join(os.path.expanduser(bstack1l1l1ll_opy_ (u"࠭ࡾࠨ੿")), bstack1l1l1ll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ઀"), bstack1l1l1ll_opy_ (u"ࠨࡣࡳࡴ࡚ࡶ࡬ࡰࡣࡧࡑࡉ࠻ࡈࡢࡵ࡫࠲࡯ࡹ࡯࡯ࠩઁ"))
    bstack1l1lllll1_opy_ = {
      bstack1l1l1ll_opy_ (u"ࠩ࡬ࡨࠬં"): bstack1ll1ll11_opy_,
      bstack1l1l1ll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ઃ"): datetime.datetime.strftime(datetime.datetime.now(), bstack1l1l1ll_opy_ (u"ࠫࠪࡪ࠯ࠦ࡯࠲ࠩ࡞ࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨ઄")),
      bstack1l1l1ll_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪઅ"): str(__version__)
    }
    try:
      bstack111llll1l_opy_ = {}
      if os.path.exists(bstack11l11ll1l1_opy_):
        bstack111llll1l_opy_ = json.load(open(bstack11l11ll1l1_opy_, bstack1l1l1ll_opy_ (u"࠭ࡲࡣࠩઆ")))
      bstack111llll1l_opy_[md5_hash] = bstack1l1lllll1_opy_
      with open(bstack11l11ll1l1_opy_, bstack1l1l1ll_opy_ (u"ࠢࡸ࠭ࠥઇ")) as outfile:
        json.dump(bstack111llll1l_opy_, outfile)
    except Exception as e:
      logger.debug(bstack1l1l1ll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡶࡲࡧࡥࡹ࡯࡮ࡨࠢࡐࡈ࠺ࠦࡨࡢࡵ࡫ࠤ࡫࡯࡬ࡦ࠼ࠣࡿࢂ࠭ઈ").format(str(e)))
    return
  bstack1lll11llll_opy_ = os.path.join(os.path.expanduser(bstack1l1l1ll_opy_ (u"ࠩࢁࠫઉ")), bstack1l1l1ll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪઊ"))
  if not os.path.exists(bstack1lll11llll_opy_):
    os.makedirs(bstack1lll11llll_opy_)
  bstack11l11ll1l1_opy_ = os.path.join(os.path.expanduser(bstack1l1l1ll_opy_ (u"ࠫࢃ࠭ઋ")), bstack1l1l1ll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬઌ"), bstack1l1l1ll_opy_ (u"࠭ࡡࡱࡲࡘࡴࡱࡵࡡࡥࡏࡇ࠹ࡍࡧࡳࡩ࠰࡭ࡷࡴࡴࠧઍ"))
  lock_file = bstack11l11ll1l1_opy_ + bstack1l1l1ll_opy_ (u"ࠧ࠯࡮ࡲࡧࡰ࠭઎")
  bstack1l1lllll1_opy_ = {
    bstack1l1l1ll_opy_ (u"ࠨ࡫ࡧࠫએ"): bstack1ll1ll11_opy_,
    bstack1l1l1ll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬઐ"): datetime.datetime.strftime(datetime.datetime.now(), bstack1l1l1ll_opy_ (u"ࠪࠩࡩ࠵ࠥ࡮࠱ࠨ࡝ࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧઑ")),
    bstack1l1l1ll_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ઒"): str(__version__)
  }
  try:
    with FileLock(lock_file, timeout=10):
      bstack111llll1l_opy_ = {}
      if os.path.exists(bstack11l11ll1l1_opy_):
        with open(bstack11l11ll1l1_opy_, bstack1l1l1ll_opy_ (u"ࠬࡸࠧઓ")) as f:
          content = f.read().strip()
          if content:
            bstack111llll1l_opy_ = json.loads(content)
      bstack111llll1l_opy_[md5_hash] = bstack1l1lllll1_opy_
      with open(bstack11l11ll1l1_opy_, bstack1l1l1ll_opy_ (u"ࠨࡷࠣઔ")) as outfile:
        json.dump(bstack111llll1l_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1l1l1ll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡷࡪࡶ࡫ࠤ࡫࡯࡬ࡦࠢ࡯ࡳࡨࡱࡩ࡯ࡩࠣࡪࡴࡸࠠࡎࡆ࠸ࠤ࡭ࡧࡳࡩࠢࡸࡴࡩࡧࡴࡦ࠼ࠣࡿࢂ࠭ક").format(str(e)))
def bstack1ll111l11_opy_(self):
  return
def bstack1l1111111_opy_(self):
  return
def bstack11l1l1l111_opy_():
  global bstack1l11ll11l_opy_
  bstack1l11ll11l_opy_ = True
@measure(event_name=EVENTS.bstack11lll111l1_opy_, stage=STAGE.bstack1l1ll11l1_opy_, bstack111l1llll_opy_=bstack1llll111_opy_)
def bstack1lll11lll1_opy_(self):
  global bstack11ll1111_opy_
  global bstack11lllll1ll_opy_
  global bstack1l1ll1l1l_opy_
  try:
    if bstack1l1l1ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨખ") in bstack11ll1111_opy_ and self.session_id != None and bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠩࡷࡩࡸࡺࡓࡵࡣࡷࡹࡸ࠭ગ"), bstack1l1l1ll_opy_ (u"ࠪࠫઘ")) != bstack1l1l1ll_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬઙ"):
      bstack1lllll11l1_opy_ = bstack1l1l1ll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬચ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1l1l1ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭છ")
      if bstack1lllll11l1_opy_ == bstack1l1l1ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧજ"):
        bstack11llll11ll_opy_(logger)
      if self != None:
        bstack11ll111111_opy_(self, bstack1lllll11l1_opy_, bstack1l1l1ll_opy_ (u"ࠨ࠮ࠣࠫઝ").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack1l1l1ll_opy_ (u"ࠩࠪઞ")
    if bstack1l1l1ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪટ") in bstack11ll1111_opy_ and getattr(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪઠ"), None):
      bstack11111ll1l_opy_.bstack1l11llll1_opy_(self, bstack1ll1ll1l_opy_, logger, wait=True)
    if bstack1l1l1ll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬડ") in bstack11ll1111_opy_:
      if not threading.currentThread().behave_test_status:
        bstack11ll111111_opy_(self, bstack1l1l1ll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨઢ"))
      bstack1l111l1ll1_opy_.bstack1l11l1l111_opy_(self)
  except Exception as e:
    logger.debug(bstack1l1l1ll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡳࡵࡣࡷࡹࡸࡀࠠࠣણ") + str(e))
  bstack1l1ll1l1l_opy_(self)
  self.session_id = None
def bstack1111111l1_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack1ll11l1ll1_opy_
    global bstack11ll1111_opy_
    command_executor = kwargs.get(bstack1l1l1ll_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠫત"), bstack1l1l1ll_opy_ (u"ࠩࠪથ"))
    bstack1111ll11l_opy_ = False
    if type(command_executor) == str and bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭દ") in command_executor:
      bstack1111ll11l_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧધ") in str(getattr(command_executor, bstack1l1l1ll_opy_ (u"ࠬࡥࡵࡳ࡮ࠪન"), bstack1l1l1ll_opy_ (u"࠭ࠧ઩"))):
      bstack1111ll11l_opy_ = True
    else:
      kwargs = bstack1lll11l1ll_opy_.bstack11llll1ll_opy_(bstack1l1l1ll11_opy_=kwargs, config=CONFIG)
      return bstack1lllll1lll_opy_(self, *args, **kwargs)
    if bstack1111ll11l_opy_:
      bstack1lll1l1lll_opy_ = bstack111lllll1l_opy_.bstack1l1l111ll1_opy_(CONFIG, bstack11ll1111_opy_)
      if kwargs.get(bstack1l1l1ll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨપ")):
        kwargs[bstack1l1l1ll_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩફ")] = bstack1ll11l1ll1_opy_(kwargs[bstack1l1l1ll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪબ")], bstack11ll1111_opy_, CONFIG, bstack1lll1l1lll_opy_)
      elif kwargs.get(bstack1l1l1ll_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪભ")):
        kwargs[bstack1l1l1ll_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫમ")] = bstack1ll11l1ll1_opy_(kwargs[bstack1l1l1ll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬય")], bstack11ll1111_opy_, CONFIG, bstack1lll1l1lll_opy_)
  except Exception as e:
    logger.error(bstack1l1l1ll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡦࡰࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡔࡆࡎࠤࡨࡧࡰࡴ࠼ࠣࡿࢂࠨર").format(str(e)))
  return bstack1lllll1lll_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack111l1l1l1_opy_, stage=STAGE.bstack1l1ll11l1_opy_, bstack111l1llll_opy_=bstack1llll111_opy_)
def bstack1lllll1ll_opy_(self, command_executor=bstack1l1l1ll_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯࠲࠴࠺࠲࠵࠴࠰࠯࠳࠽࠸࠹࠺࠴ࠣ઱"), *args, **kwargs):
  global bstack11lllll1ll_opy_
  global bstack1lll1l1l1l_opy_
  bstack11ll1ll1l1_opy_ = bstack1111111l1_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack1l1ll1l11l_opy_.on():
    return bstack11ll1ll1l1_opy_
  try:
    logger.debug(bstack1l1l1ll_opy_ (u"ࠨࡅࡲࡱࡲࡧ࡮ࡥࠢࡈࡼࡪࡩࡵࡵࡱࡵࠤࡼ࡮ࡥ࡯ࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥ࡯ࡳࠡࡨࡤࡰࡸ࡫ࠠ࠮ࠢࡾࢁࠬલ").format(str(command_executor)))
    logger.debug(bstack1l1l1ll_opy_ (u"ࠩࡋࡹࡧࠦࡕࡓࡎࠣ࡭ࡸࠦ࠭ࠡࡽࢀࠫળ").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭઴") in command_executor._url:
      bstack1l1l1111l1_opy_.bstack1l1ll11111_opy_(bstack1l1l1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬવ"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack1l1l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨશ") in command_executor):
    bstack1l1l1111l1_opy_.bstack1l1ll11111_opy_(bstack1l1l1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧષ"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1l1ll1111l_opy_ = getattr(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡔࡦࡵࡷࡑࡪࡺࡡࠨસ"), None)
  bstack11l111l1l1_opy_ = {}
  if self.capabilities is not None:
    bstack11l111l1l1_opy_[bstack1l1l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧહ")] = self.capabilities.get(bstack1l1l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ઺"))
    bstack11l111l1l1_opy_[bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ઻")] = self.capabilities.get(bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲ઼ࠬ"))
    bstack11l111l1l1_opy_[bstack1l1l1ll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡤࡵࡰࡵ࡫ࡲࡲࡸ࠭ઽ")] = self.capabilities.get(bstack1l1l1ll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫા"))
  if CONFIG.get(bstack1l1l1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧિ"), False) and bstack1lll11l1ll_opy_.bstack1l11l1111_opy_(bstack11l111l1l1_opy_):
    threading.current_thread().a11yPlatform = True
  if bstack1l1l1ll_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨી") in bstack11ll1111_opy_ or bstack1l1l1ll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨુ") in bstack11ll1111_opy_:
    bstack1llllll11l_opy_.bstack11l1l1111l_opy_(self)
  if bstack1l1l1ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪૂ") in bstack11ll1111_opy_ and bstack1l1ll1111l_opy_ and bstack1l1ll1111l_opy_.get(bstack1l1l1ll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫૃ"), bstack1l1l1ll_opy_ (u"ࠬ࠭ૄ")) == bstack1l1l1ll_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧૅ"):
    bstack1llllll11l_opy_.bstack11l1l1111l_opy_(self)
  bstack11lllll1ll_opy_ = self.session_id
  with bstack1l1l111l1_opy_:
    bstack1lll1l1l1l_opy_.append(self)
  return bstack11ll1ll1l1_opy_
def bstack1lll1l1l11_opy_(args):
  return bstack1l1l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲࠨ૆") in str(args)
def bstack1l111ll111_opy_(self, driver_command, *args, **kwargs):
  global bstack1111111ll_opy_
  global bstack1l1111lll1_opy_
  bstack111llll11_opy_ = bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬે"), None) and bstack1l111l1l_opy_(
          threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨૈ"), None)
  bstack11lll1l11_opy_ = bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪૉ"), None) and bstack1l111l1l_opy_(
          threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭૊"), None)
  bstack1l1l11111_opy_ = getattr(self, bstack1l1l1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬો"), None) != None and getattr(self, bstack1l1l1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭ૌ"), None) == True
  if not bstack1l1111lll1_opy_ and bstack1l1l1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ્ࠧ") in CONFIG and CONFIG[bstack1l1l1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ૎")] == True and bstack1lll11l1l1_opy_.bstack1l1lll1ll1_opy_(driver_command) and (bstack1l1l11111_opy_ or bstack111llll11_opy_ or bstack11lll1l11_opy_) and not bstack1lll1l1l11_opy_(args):
    try:
      bstack1l1111lll1_opy_ = True
      logger.debug(bstack1l1l1ll_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡽࢀࠫ૏").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack1l1l1ll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡦࡴࡩࡳࡷࡳࠠࡴࡥࡤࡲࠥࢁࡽࠨૐ").format(str(err)))
    bstack1l1111lll1_opy_ = False
  response = bstack1111111ll_opy_(self, driver_command, *args, **kwargs)
  if (bstack1l1l1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ૑") in str(bstack11ll1111_opy_).lower() or bstack1l1l1ll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ૒") in str(bstack11ll1111_opy_).lower()) and bstack1l1ll1l11l_opy_.on():
    try:
      if driver_command == bstack1l1l1ll_opy_ (u"࠭ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪ૓"):
        bstack1llllll11l_opy_.bstack1111l111l_opy_({
            bstack1l1l1ll_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭૔"): response[bstack1l1l1ll_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧ૕")],
            bstack1l1l1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ૖"): bstack1llllll11l_opy_.current_test_uuid() if bstack1llllll11l_opy_.current_test_uuid() else bstack1l1ll1l11l_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
@measure(event_name=EVENTS.bstack1lll111ll_opy_, stage=STAGE.bstack1l1ll11l1_opy_, bstack111l1llll_opy_=bstack1llll111_opy_)
def bstack1l1l1l1l_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack11lllll1ll_opy_
  global bstack1l11lll1_opy_
  global bstack1llll111_opy_
  global bstack1lll11l11_opy_
  global bstack1lllll11l_opy_
  global bstack11ll1111_opy_
  global bstack1lllll1lll_opy_
  global bstack1lll1l1l1l_opy_
  global bstack1ll11llll1_opy_
  global bstack1ll1ll1l_opy_
  if os.getenv(bstack1l1l1ll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ૗")) is not None and bstack1lll11l1ll_opy_.bstack11l1111111_opy_(CONFIG) is None:
    CONFIG[bstack1l1l1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ૘")] = True
  CONFIG[bstack1l1l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ૙")] = str(bstack11ll1111_opy_) + str(__version__)
  bstack1l1lll1l11_opy_ = os.environ[bstack1l1l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ૚")]
  bstack1lll1l1lll_opy_ = bstack111lllll1l_opy_.bstack1l1l111ll1_opy_(CONFIG, bstack11ll1111_opy_)
  CONFIG[bstack1l1l1ll_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ૛")] = bstack1l1lll1l11_opy_
  CONFIG[bstack1l1l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ૜")] = bstack1lll1l1lll_opy_
  if CONFIG.get(bstack1l1l1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ૝"),bstack1l1l1ll_opy_ (u"ࠪࠫ૞")) and bstack1l1l1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ૟") in bstack11ll1111_opy_:
    CONFIG[bstack1l1l1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬૠ")].pop(bstack1l1l1ll_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫૡ"), None)
    CONFIG[bstack1l1l1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧૢ")].pop(bstack1l1l1ll_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ૣ"), None)
  command_executor = bstack11lll1lll_opy_()
  logger.debug(bstack11l111l11_opy_.format(command_executor))
  proxy = bstack1ll1l11lll_opy_(CONFIG, proxy)
  bstack11l1llll_opy_ = 0 if bstack1l11lll1_opy_ < 0 else bstack1l11lll1_opy_
  try:
    if bstack1lll11l11_opy_ is True:
      bstack11l1llll_opy_ = int(multiprocessing.current_process().name)
    elif bstack1lllll11l_opy_ is True:
      bstack11l1llll_opy_ = int(threading.current_thread().name)
  except:
    bstack11l1llll_opy_ = 0
  bstack1lll1111ll_opy_ = bstack1l11l11l11_opy_(CONFIG, bstack11l1llll_opy_)
  logger.debug(bstack1ll1lllll1_opy_.format(str(bstack1lll1111ll_opy_)))
  if bstack1l1l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭૤") in CONFIG and bstack11lll1ll11_opy_(CONFIG[bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ૥")]):
    bstack1l11l1l1ll_opy_(bstack1lll1111ll_opy_)
  if bstack1lll11l1ll_opy_.bstack11ll1111l1_opy_(CONFIG, bstack11l1llll_opy_) and bstack1lll11l1ll_opy_.bstack1ll1llll_opy_(bstack1lll1111ll_opy_, options, desired_capabilities, CONFIG):
    threading.current_thread().a11yPlatform = True
    if (cli.accessibility is None or not cli.accessibility.is_enabled()):
      bstack1lll11l1ll_opy_.set_capabilities(bstack1lll1111ll_opy_, CONFIG)
  if desired_capabilities:
    bstack1l11ll111_opy_ = bstack11lll1ll1_opy_(desired_capabilities)
    bstack1l11ll111_opy_[bstack1l1l1ll_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫ૦")] = bstack1l1ll111l_opy_(CONFIG)
    bstack1l11l1ll1l_opy_ = bstack1l11l11l11_opy_(bstack1l11ll111_opy_)
    if bstack1l11l1ll1l_opy_:
      bstack1lll1111ll_opy_ = update(bstack1l11l1ll1l_opy_, bstack1lll1111ll_opy_)
    desired_capabilities = None
  if options:
    bstack1l1111l11l_opy_(options, bstack1lll1111ll_opy_)
  if not options:
    options = bstack1lllll11ll_opy_(bstack1lll1111ll_opy_)
  bstack1ll1ll1l_opy_ = CONFIG.get(bstack1l1l1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ૧"))[bstack11l1llll_opy_]
  if proxy and bstack1l111111l_opy_() >= version.parse(bstack1l1l1ll_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭૨")):
    options.proxy(proxy)
  if options and bstack1l111111l_opy_() >= version.parse(bstack1l1l1ll_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭૩")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1l111111l_opy_() < version.parse(bstack1l1l1ll_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ૪")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1lll1111ll_opy_)
  logger.info(bstack1l111ll1ll_opy_)
  bstack111ll111l_opy_.end(EVENTS.bstack1l1111l1_opy_.value, EVENTS.bstack1l1111l1_opy_.value + bstack1l1l1ll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ૫"), EVENTS.bstack1l1111l1_opy_.value + bstack1l1l1ll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ૬"), status=True, failure=None, test_name=bstack1llll111_opy_)
  if bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡶࡲࡰࡨ࡬ࡰࡪ࠭૭") in kwargs:
    del kwargs[bstack1l1l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡰࡳࡱࡩ࡭ࡱ࡫ࠧ૮")]
  try:
    if bstack1l111111l_opy_() >= version.parse(bstack1l1l1ll_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭૯")):
      bstack1lllll1lll_opy_(self, command_executor=command_executor,
                options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
    elif bstack1l111111l_opy_() >= version.parse(bstack1l1l1ll_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭૰")):
      bstack1lllll1lll_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities, options=options,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l111111l_opy_() >= version.parse(bstack1l1l1ll_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨ૱")):
      bstack1lllll1lll_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    else:
      bstack1lllll1lll_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive)
  except Exception as bstack1lll1ll1l_opy_:
    logger.error(bstack111lllllll_opy_.format(bstack1l1l1ll_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠨ૲"), str(bstack1lll1ll1l_opy_)))
    raise bstack1lll1ll1l_opy_
  if bstack1lll11l1ll_opy_.bstack11ll1111l1_opy_(CONFIG, bstack11l1llll_opy_) and bstack1lll11l1ll_opy_.bstack1ll1llll_opy_(self.caps, options, desired_capabilities):
    if CONFIG[bstack1l1l1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬ૳")][bstack1l1l1ll_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪ૴")] == True:
      threading.current_thread().appA11yPlatform = True
      if cli.accessibility is None or not cli.accessibility.is_enabled():
        bstack1lll11l1ll_opy_.set_capabilities(bstack1lll1111ll_opy_, CONFIG)
  try:
    bstack11l1lll11_opy_ = bstack1l1l1ll_opy_ (u"ࠬ࠭૵")
    if bstack1l111111l_opy_() >= version.parse(bstack1l1l1ll_opy_ (u"࠭࠴࠯࠲࠱࠴ࡧ࠷ࠧ૶")):
      if self.caps is not None:
        bstack11l1lll11_opy_ = self.caps.get(bstack1l1l1ll_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢ૷"))
    else:
      if self.capabilities is not None:
        bstack11l1lll11_opy_ = self.capabilities.get(bstack1l1l1ll_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣ૸"))
    if bstack11l1lll11_opy_:
      bstack111ll1l1l_opy_(bstack11l1lll11_opy_)
      if bstack1l111111l_opy_() <= version.parse(bstack1l1l1ll_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩૹ")):
        self.command_executor._url = bstack1l1l1ll_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦૺ") + bstack1lll1l1ll_opy_ + bstack1l1l1ll_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣૻ")
      else:
        self.command_executor._url = bstack1l1l1ll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢૼ") + bstack11l1lll11_opy_ + bstack1l1l1ll_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢ૽")
      logger.debug(bstack1lll1llll_opy_.format(bstack11l1lll11_opy_))
    else:
      logger.debug(bstack1ll1lll1ll_opy_.format(bstack1l1l1ll_opy_ (u"ࠢࡐࡲࡷ࡭ࡲࡧ࡬ࠡࡊࡸࡦࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠣ૾")))
  except Exception as e:
    logger.debug(bstack1ll1lll1ll_opy_.format(e))
  if bstack1l1l1ll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ૿") in bstack11ll1111_opy_:
    bstack1lll1lll11_opy_(bstack1l11lll1_opy_, bstack1ll11llll1_opy_)
  bstack11lllll1ll_opy_ = self.session_id
  if bstack1l1l1ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ଀") in bstack11ll1111_opy_ or bstack1l1l1ll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪଁ") in bstack11ll1111_opy_ or bstack1l1l1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪଂ") in bstack11ll1111_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack1l1ll1111l_opy_ = getattr(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࡙࡫ࡳࡵࡏࡨࡸࡦ࠭ଃ"), None)
  if bstack1l1l1ll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭଄") in bstack11ll1111_opy_ or bstack1l1l1ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ଅ") in bstack11ll1111_opy_:
    bstack1llllll11l_opy_.bstack11l1l1111l_opy_(self)
  if bstack1l1l1ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨଆ") in bstack11ll1111_opy_ and bstack1l1ll1111l_opy_ and bstack1l1ll1111l_opy_.get(bstack1l1l1ll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩଇ"), bstack1l1l1ll_opy_ (u"ࠪࠫଈ")) == bstack1l1l1ll_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬଉ"):
    bstack1llllll11l_opy_.bstack11l1l1111l_opy_(self)
  with bstack1l1l111l1_opy_:
    bstack1lll1l1l1l_opy_.append(self)
  if bstack1l1l1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨଊ") in CONFIG and bstack1l1l1ll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫଋ") in CONFIG[bstack1l1l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଌ")][bstack11l1llll_opy_]:
    bstack1llll111_opy_ = CONFIG[bstack1l1l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ଍")][bstack11l1llll_opy_][bstack1l1l1ll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ଎")]
  logger.debug(bstack1l1l11l1l_opy_.format(bstack11lllll1ll_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    from browserstack_sdk.__init__ import bstack11ll111lll_opy_
    def bstack11l111l1l_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1l1ll1llll_opy_
      if(bstack1l1l1ll_opy_ (u"ࠥ࡭ࡳࡪࡥࡹ࠰࡭ࡷࠧଏ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1l1l1ll_opy_ (u"ࠫࢃ࠭ଐ")), bstack1l1l1ll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ଑"), bstack1l1l1ll_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨ଒")), bstack1l1l1ll_opy_ (u"ࠧࡸࠩଓ")) as fp:
          fp.write(bstack1l1l1ll_opy_ (u"ࠣࠤଔ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1l1l1ll_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸࡠࡤࡶࡸࡦࡩ࡫࠯࡬ࡶࠦକ")))):
          with open(args[1], bstack1l1l1ll_opy_ (u"ࠪࡶࠬଖ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1l1l1ll_opy_ (u"ࠫࡦࡹࡹ࡯ࡥࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࡥ࡮ࡦࡹࡓࡥ࡬࡫ࠨࡤࡱࡱࡸࡪࡾࡴ࠭ࠢࡳࡥ࡬࡫ࠠ࠾ࠢࡹࡳ࡮ࡪࠠ࠱ࠫࠪଗ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack11l1l111_opy_)
            if bstack1l1l1ll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩଘ") in CONFIG and str(CONFIG[bstack1l1l1ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪଙ")]).lower() != bstack1l1l1ll_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ଚ"):
                bstack11l11ll1l_opy_ = bstack11ll111lll_opy_()
                bstack1llll1lll1_opy_ = bstack1l1l1ll_opy_ (u"ࠨࠩࠪࠎ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠊࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡰࡢࡶ࡫ࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳࡞࠽ࠍࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠴ࡡࡀࠐࡣࡰࡰࡶࡸࠥࡶ࡟ࡪࡰࡧࡩࡽࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠴ࡠ࠿ࠏࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡹ࡬ࡪࡥࡨࠬ࠵࠲ࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࠬ࠿ࠏࡩ࡯࡯ࡵࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬ࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ࠭ࡀࠐࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴࡬ࡢࡷࡱࡧ࡭ࠦ࠽ࠡࡣࡶࡽࡳࡩࠠࠩ࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁࡻࠋࠢࠣࡰࡪࡺࠠࡤࡣࡳࡷࡀࠐࠠࠡࡶࡵࡽࠥࢁࡻࠋࠢࠣࠤࠥࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࠼ࠌࠣࠤࢂࢃࠠࡤࡣࡷࡧ࡭ࠦࠨࡦࡺࠬࠤࢀࢁࠊࠡࠢࠣࠤࡨࡵ࡮ࡴࡱ࡯ࡩ࠳࡫ࡲࡳࡱࡵࠬࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࡀࠢ࠭ࠢࡨࡼ࠮ࡁࠊࠡࠢࢀࢁࠏࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠨࡼࡽࠍࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥ࠭ࡻࡤࡦࡳ࡙ࡷࡲࡽࠨࠢ࠮ࠤࡪࡴࡣࡰࡦࡨ࡙ࡗࡏࡃࡰ࡯ࡳࡳࡳ࡫࡮ࡵࠪࡍࡗࡔࡔ࠮ࡴࡶࡵ࡭ࡳ࡭ࡩࡧࡻࠫࡧࡦࡶࡳࠪࠫ࠯ࠎࠥࠦࠠࠡ࠰࠱࠲ࡱࡧࡵ࡯ࡥ࡫ࡓࡵࡺࡩࡰࡰࡶࠎࠥࠦࡽࡾࠫ࠾ࠎࢂࢃ࠻ࠋ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࠎࠬ࠭ࠧଛ").format(bstack11l11ll1l_opy_=bstack11l11ll1l_opy_)
            lines.insert(1, bstack1llll1lll1_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1l1l1ll_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸࡠࡤࡶࡸࡦࡩ࡫࠯࡬ࡶࠦଜ")), bstack1l1l1ll_opy_ (u"ࠪࡻࠬଝ")) as bstack11l11llll1_opy_:
              bstack11l11llll1_opy_.writelines(lines)
        CONFIG[bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ଞ")] = str(bstack11ll1111_opy_) + str(__version__)
        bstack1l1lll1l11_opy_ = os.environ[bstack1l1l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪଟ")]
        bstack1lll1l1lll_opy_ = bstack111lllll1l_opy_.bstack1l1l111ll1_opy_(CONFIG, bstack11ll1111_opy_)
        CONFIG[bstack1l1l1ll_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩଠ")] = bstack1l1lll1l11_opy_
        CONFIG[bstack1l1l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩଡ")] = bstack1lll1l1lll_opy_
        bstack11l1llll_opy_ = 0 if bstack1l11lll1_opy_ < 0 else bstack1l11lll1_opy_
        try:
          if bstack1lll11l11_opy_ is True:
            bstack11l1llll_opy_ = int(multiprocessing.current_process().name)
          elif bstack1lllll11l_opy_ is True:
            bstack11l1llll_opy_ = int(threading.current_thread().name)
        except:
          bstack11l1llll_opy_ = 0
        CONFIG[bstack1l1l1ll_opy_ (u"ࠣࡷࡶࡩ࡜࠹ࡃࠣଢ")] = False
        CONFIG[bstack1l1l1ll_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣଣ")] = True
        bstack1lll1111ll_opy_ = bstack1l11l11l11_opy_(CONFIG, bstack11l1llll_opy_)
        logger.debug(bstack1ll1lllll1_opy_.format(str(bstack1lll1111ll_opy_)))
        if CONFIG.get(bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧତ")):
          bstack1l11l1l1ll_opy_(bstack1lll1111ll_opy_)
        if bstack1l1l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଥ") in CONFIG and bstack1l1l1ll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪଦ") in CONFIG[bstack1l1l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଧ")][bstack11l1llll_opy_]:
          bstack1llll111_opy_ = CONFIG[bstack1l1l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪନ")][bstack11l1llll_opy_][bstack1l1l1ll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭଩")]
        args.append(os.path.join(os.path.expanduser(bstack1l1l1ll_opy_ (u"ࠩࢁࠫପ")), bstack1l1l1ll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪଫ"), bstack1l1l1ll_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭ବ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1lll1111ll_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1l1l1ll_opy_ (u"ࠧ࡯࡮ࡥࡧࡻࡣࡧࡹࡴࡢࡥ࡮࠲࡯ࡹࠢଭ"))
      bstack1l1ll1llll_opy_ = True
      return bstack11l11lll1_opy_(self, args, bufsize=bufsize, executable=executable,
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
  def bstack1lll1lll1_opy_(self,
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
    global bstack1l11lll1_opy_
    global bstack1llll111_opy_
    global bstack1lll11l11_opy_
    global bstack1lllll11l_opy_
    global bstack11ll1111_opy_
    CONFIG[bstack1l1l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨମ")] = str(bstack11ll1111_opy_) + str(__version__)
    bstack1l1lll1l11_opy_ = os.environ[bstack1l1l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬଯ")]
    bstack1lll1l1lll_opy_ = bstack111lllll1l_opy_.bstack1l1l111ll1_opy_(CONFIG, bstack11ll1111_opy_)
    CONFIG[bstack1l1l1ll_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫର")] = bstack1l1lll1l11_opy_
    CONFIG[bstack1l1l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ଱")] = bstack1lll1l1lll_opy_
    bstack11l1llll_opy_ = 0 if bstack1l11lll1_opy_ < 0 else bstack1l11lll1_opy_
    try:
      if bstack1lll11l11_opy_ is True:
        bstack11l1llll_opy_ = int(multiprocessing.current_process().name)
      elif bstack1lllll11l_opy_ is True:
        bstack11l1llll_opy_ = int(threading.current_thread().name)
    except:
      bstack11l1llll_opy_ = 0
    CONFIG[bstack1l1l1ll_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤଲ")] = True
    bstack1lll1111ll_opy_ = bstack1l11l11l11_opy_(CONFIG, bstack11l1llll_opy_)
    logger.debug(bstack1ll1lllll1_opy_.format(str(bstack1lll1111ll_opy_)))
    if CONFIG.get(bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨଳ")):
      bstack1l11l1l1ll_opy_(bstack1lll1111ll_opy_)
    if bstack1l1l1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ଴") in CONFIG and bstack1l1l1ll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫଵ") in CONFIG[bstack1l1l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଶ")][bstack11l1llll_opy_]:
      bstack1llll111_opy_ = CONFIG[bstack1l1l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫଷ")][bstack11l1llll_opy_][bstack1l1l1ll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧସ")]
    import urllib
    import json
    if bstack1l1l1ll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧହ") in CONFIG and str(CONFIG[bstack1l1l1ll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ଺")]).lower() != bstack1l1l1ll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ଻"):
        bstack1ll1ll1ll_opy_ = bstack11ll111lll_opy_()
        bstack11l11ll1l_opy_ = bstack1ll1ll1ll_opy_ + urllib.parse.quote(json.dumps(bstack1lll1111ll_opy_))
    else:
        bstack11l11ll1l_opy_ = bstack1l1l1ll_opy_ (u"࠭ࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠨ଼") + urllib.parse.quote(json.dumps(bstack1lll1111ll_opy_))
    browser = self.connect(bstack11l11ll1l_opy_)
    return browser
except Exception as e:
    pass
def bstack11lll111ll_opy_():
    global bstack1l1ll1llll_opy_
    global bstack11ll1111_opy_
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack11111111_opy_
        global bstack1l1l1111l1_opy_
        if not bstack1lllll111l_opy_:
          global bstack1l1l1l1l1_opy_
          if not bstack1l1l1l1l1_opy_:
            from bstack_utils.helper import bstack11ll1lll_opy_, bstack1l111l11ll_opy_, bstack1l11l1l11l_opy_
            bstack1l1l1l1l1_opy_ = bstack11ll1lll_opy_()
            bstack1l111l11ll_opy_(bstack11ll1111_opy_)
            bstack1lll1l1lll_opy_ = bstack111lllll1l_opy_.bstack1l1l111ll1_opy_(CONFIG, bstack11ll1111_opy_)
            bstack1l1l1111l1_opy_.bstack1l1ll11111_opy_(bstack1l1l1ll_opy_ (u"ࠢࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡕࡘࡏࡅࡗࡆࡘࡤࡓࡁࡑࠤଽ"), bstack1lll1l1lll_opy_)
          BrowserType.connect = bstack11111111_opy_
          return
        BrowserType.launch = bstack1lll1lll1_opy_
        bstack1l1ll1llll_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack11l111l1l_opy_
      bstack1l1ll1llll_opy_ = True
    except Exception as e:
      pass
def bstack1ll11l11_opy_(context, bstack1l11111111_opy_):
  try:
    context.page.evaluate(bstack1l1l1ll_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤା"), bstack1l1l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿࠭ି")+ json.dumps(bstack1l11111111_opy_) + bstack1l1l1ll_opy_ (u"ࠥࢁࢂࠨୀ"))
  except Exception as e:
    logger.debug(bstack1l1l1ll_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡻࡾ࠼ࠣࡿࢂࠨୁ").format(str(e), traceback.format_exc()))
def bstack1llllll1ll_opy_(context, message, level):
  try:
    context.page.evaluate(bstack1l1l1ll_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨୂ"), bstack1l1l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫୃ") + json.dumps(message) + bstack1l1l1ll_opy_ (u"ࠧ࠭ࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠪୄ") + json.dumps(level) + bstack1l1l1ll_opy_ (u"ࠨࡿࢀࠫ୅"))
  except Exception as e:
    logger.debug(bstack1l1l1ll_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠢࡾࢁ࠿ࠦࡻࡾࠤ୆").format(str(e), traceback.format_exc()))
@measure(event_name=EVENTS.bstack11ll1lll11_opy_, stage=STAGE.bstack1l1ll11l1_opy_, bstack111l1llll_opy_=bstack1llll111_opy_)
def bstack1ll11111_opy_(self, url):
  global bstack1ll11l11l_opy_
  try:
    bstack11l11lll_opy_(url)
  except Exception as err:
    logger.debug(bstack111l11111_opy_.format(str(err)))
  try:
    bstack1ll11l11l_opy_(self, url)
  except Exception as e:
    try:
      bstack1llll1ll11_opy_ = str(e)
      if any(err_msg in bstack1llll1ll11_opy_ for err_msg in bstack11lll1l1l_opy_):
        bstack11l11lll_opy_(url, True)
    except Exception as err:
      logger.debug(bstack111l11111_opy_.format(str(err)))
    raise e
def bstack11ll1l1ll1_opy_(self):
  global bstack1lll1l1l_opy_
  bstack1lll1l1l_opy_ = self
  return
def bstack11l1l1l1l_opy_(self):
  global bstack11llll1l11_opy_
  bstack11llll1l11_opy_ = self
  return
def bstack111111l1_opy_(test_name, bstack1ll11lll1l_opy_):
  global CONFIG
  if percy.bstack111l1111l_opy_() == bstack1l1l1ll_opy_ (u"ࠥࡸࡷࡻࡥࠣେ"):
    bstack11l1l1lll_opy_ = os.path.relpath(bstack1ll11lll1l_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack11l1l1lll_opy_)
    bstack111l1llll_opy_ = suite_name + bstack1l1l1ll_opy_ (u"ࠦ࠲ࠨୈ") + test_name
    threading.current_thread().percySessionName = bstack111l1llll_opy_
def bstack1ll1111111_opy_(self, test, *args, **kwargs):
  global bstack1ll1l1l11l_opy_
  test_name = None
  bstack1ll11lll1l_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1ll11lll1l_opy_ = str(test.source)
  bstack111111l1_opy_(test_name, bstack1ll11lll1l_opy_)
  bstack1ll1l1l11l_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.bstack1llll1l1ll_opy_, stage=STAGE.bstack1l1ll11l1_opy_, bstack111l1llll_opy_=bstack1llll111_opy_)
def bstack1111ll1ll_opy_(driver, bstack111l1llll_opy_):
  if not bstack1lll1lll1l_opy_ and bstack111l1llll_opy_:
      bstack111llllll_opy_ = {
          bstack1l1l1ll_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬ୉"): bstack1l1l1ll_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ୊"),
          bstack1l1l1ll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪୋ"): {
              bstack1l1l1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ୌ"): bstack111l1llll_opy_
          }
      }
      bstack1lll11ll_opy_ = bstack1l1l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃ୍ࠧ").format(json.dumps(bstack111llllll_opy_))
      driver.execute_script(bstack1lll11ll_opy_)
  if bstack1ll1ll1l1_opy_:
      bstack11l1ll111_opy_ = {
          bstack1l1l1ll_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪ୎"): bstack1l1l1ll_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭୏"),
          bstack1l1l1ll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ୐"): {
              bstack1l1l1ll_opy_ (u"࠭ࡤࡢࡶࡤࠫ୑"): bstack111l1llll_opy_ + bstack1l1l1ll_opy_ (u"ࠧࠡࡲࡤࡷࡸ࡫ࡤࠢࠩ୒"),
              bstack1l1l1ll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ୓"): bstack1l1l1ll_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧ୔")
          }
      }
      if bstack1ll1ll1l1_opy_.status == bstack1l1l1ll_opy_ (u"ࠪࡔࡆ࡙ࡓࠨ୕"):
          bstack1lll11l1l_opy_ = bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩୖ").format(json.dumps(bstack11l1ll111_opy_))
          driver.execute_script(bstack1lll11l1l_opy_)
          bstack11ll111111_opy_(driver, bstack1l1l1ll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬୗ"))
      elif bstack1ll1ll1l1_opy_.status == bstack1l1l1ll_opy_ (u"࠭ࡆࡂࡋࡏࠫ୘"):
          reason = bstack1l1l1ll_opy_ (u"ࠢࠣ୙")
          bstack11l111l1ll_opy_ = bstack111l1llll_opy_ + bstack1l1l1ll_opy_ (u"ࠨࠢࡩࡥ࡮ࡲࡥࡥࠩ୚")
          if bstack1ll1ll1l1_opy_.message:
              reason = str(bstack1ll1ll1l1_opy_.message)
              bstack11l111l1ll_opy_ = bstack11l111l1ll_opy_ + bstack1l1l1ll_opy_ (u"ࠩࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸ࠺ࠡࠩ୛") + reason
          bstack11l1ll111_opy_[bstack1l1l1ll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ଡ଼")] = {
              bstack1l1l1ll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪଢ଼"): bstack1l1l1ll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ୞"),
              bstack1l1l1ll_opy_ (u"࠭ࡤࡢࡶࡤࠫୟ"): bstack11l111l1ll_opy_
          }
          bstack1lll11l1l_opy_ = bstack1l1l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬୠ").format(json.dumps(bstack11l1ll111_opy_))
          driver.execute_script(bstack1lll11l1l_opy_)
          bstack11ll111111_opy_(driver, bstack1l1l1ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨୡ"), reason)
          bstack1lll1l111_opy_(reason, str(bstack1ll1ll1l1_opy_), str(bstack1l11lll1_opy_), logger)
@measure(event_name=EVENTS.bstack1l11l1111l_opy_, stage=STAGE.bstack1l1ll11l1_opy_, bstack111l1llll_opy_=bstack1llll111_opy_)
def bstack11l11l11ll_opy_(driver, test):
  if percy.bstack111l1111l_opy_() == bstack1l1l1ll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢୢ") and percy.bstack11lll1l1_opy_() == bstack1l1l1ll_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧୣ"):
      bstack11l1l11l_opy_ = bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ୤"), None)
      bstack1ll1111l11_opy_(driver, bstack11l1l11l_opy_, test)
  if (bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ୥"), None) and
      bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ୦"), None)) or (
      bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ୧"), None) and
      bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ୨"), None)):
      logger.info(bstack1l1l1ll_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠠࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡵࡻࡦࡿ࠮ࠡࠤ୩"))
      bstack1lll11l1ll_opy_.bstack1ll1l11ll_opy_(driver, name=test.name, path=test.source)
def bstack1l1111l111_opy_(test, bstack111l1llll_opy_):
    try:
      bstack1lll111ll1_opy_ = datetime.datetime.now()
      data = {}
      if test:
        data[bstack1l1l1ll_opy_ (u"ࠪࡲࡦࡳࡥࠨ୪")] = bstack111l1llll_opy_
      if bstack1ll1ll1l1_opy_:
        if bstack1ll1ll1l1_opy_.status == bstack1l1l1ll_opy_ (u"ࠫࡕࡇࡓࡔࠩ୫"):
          data[bstack1l1l1ll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ୬")] = bstack1l1l1ll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭୭")
        elif bstack1ll1ll1l1_opy_.status == bstack1l1l1ll_opy_ (u"ࠧࡇࡃࡌࡐࠬ୮"):
          data[bstack1l1l1ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ୯")] = bstack1l1l1ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ୰")
          if bstack1ll1ll1l1_opy_.message:
            data[bstack1l1l1ll_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪୱ")] = str(bstack1ll1ll1l1_opy_.message)
      user = CONFIG[bstack1l1l1ll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭୲")]
      key = CONFIG[bstack1l1l1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ୳")]
      host = bstack1ll11llll_opy_(cli.config, [bstack1l1l1ll_opy_ (u"ࠨࡡࡱ࡫ࡶࠦ୴"), bstack1l1l1ll_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡦࠤ୵"), bstack1l1l1ll_opy_ (u"ࠣࡣࡳ࡭ࠧ୶")], bstack1l1l1ll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡵ࡯࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠥ୷"))
      url = bstack1l1l1ll_opy_ (u"ࠪࡿࢂ࠵ࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡵࡨࡷࡸ࡯࡯࡯ࡵ࠲ࡿࢂ࠴ࡪࡴࡱࡱࠫ୸").format(host, bstack11lllll1ll_opy_)
      headers = {
        bstack1l1l1ll_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪ୹"): bstack1l1l1ll_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ୺"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers, auth=(user, key))
        cli.bstack1ll1ll11ll_opy_(bstack1l1l1ll_opy_ (u"ࠨࡨࡵࡶࡳ࠾ࡺࡶࡤࡢࡶࡨࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡷࡹࡧࡴࡶࡵࠥ୻"), datetime.datetime.now() - bstack1lll111ll1_opy_)
    except Exception as e:
      logger.error(bstack11llll11_opy_.format(str(e)))
def bstack1lll11l11l_opy_(test, bstack111l1llll_opy_):
  global CONFIG
  global bstack11llll1l11_opy_
  global bstack1lll1l1l_opy_
  global bstack11lllll1ll_opy_
  global bstack1ll1ll1l1_opy_
  global bstack1llll111_opy_
  global bstack11l11111_opy_
  global bstack11l1ll1l_opy_
  global bstack1l1111llll_opy_
  global bstack11l11l1l1_opy_
  global bstack1lll1l1l1l_opy_
  global bstack1ll1ll1l_opy_
  global bstack11l111ll11_opy_
  try:
    if not bstack11lllll1ll_opy_:
      with bstack11l111ll11_opy_:
        bstack1lll11l111_opy_ = os.path.join(os.path.expanduser(bstack1l1l1ll_opy_ (u"ࠧࡿࠩ୼")), bstack1l1l1ll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ୽"), bstack1l1l1ll_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫ୾"))
        if os.path.exists(bstack1lll11l111_opy_):
          with open(bstack1lll11l111_opy_, bstack1l1l1ll_opy_ (u"ࠪࡶࠬ୿")) as f:
            content = f.read().strip()
            if content:
              bstack1ll1l111l_opy_ = json.loads(bstack1l1l1ll_opy_ (u"ࠦࢀࠨ஀") + content + bstack1l1l1ll_opy_ (u"ࠬࠨࡸࠣ࠼ࠣࠦࡾࠨࠧ஁") + bstack1l1l1ll_opy_ (u"ࠨࡽࠣஂ"))
              bstack11lllll1ll_opy_ = bstack1ll1l111l_opy_.get(str(threading.get_ident()))
  except Exception as e:
    logger.debug(bstack1l1l1ll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡲࡦࡣࡧ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡋࡇࡷࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬஃ") + str(e))
  if bstack1lll1l1l1l_opy_:
    with bstack1l1l111l1_opy_:
      bstack11l11lll1l_opy_ = bstack1lll1l1l1l_opy_.copy()
    for driver in bstack11l11lll1l_opy_:
      if bstack11lllll1ll_opy_ == driver.session_id:
        if test:
          bstack11l11l11ll_opy_(driver, test)
        bstack1111ll1ll_opy_(driver, bstack111l1llll_opy_)
  elif bstack11lllll1ll_opy_:
    bstack1l1111l111_opy_(test, bstack111l1llll_opy_)
  if bstack11llll1l11_opy_:
    bstack11l1ll1l_opy_(bstack11llll1l11_opy_)
  if bstack1lll1l1l_opy_:
    bstack1l1111llll_opy_(bstack1lll1l1l_opy_)
  if bstack1l11ll11l_opy_:
    bstack11l11l1l1_opy_()
def bstack1l11llllll_opy_(self, test, *args, **kwargs):
  bstack111l1llll_opy_ = None
  if test:
    bstack111l1llll_opy_ = str(test.name)
  bstack1lll11l11l_opy_(test, bstack111l1llll_opy_)
  bstack11l11111_opy_(self, test, *args, **kwargs)
def bstack1ll11l1lll_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1l111lll1_opy_
  global CONFIG
  global bstack1lll1l1l1l_opy_
  global bstack11lllll1ll_opy_
  global bstack11l111ll11_opy_
  bstack11111ll11_opy_ = None
  try:
    if bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ஄"), None) or bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫஅ"), None):
      try:
        if not bstack11lllll1ll_opy_:
          bstack1lll11l111_opy_ = os.path.join(os.path.expanduser(bstack1l1l1ll_opy_ (u"ࠪࢂࠬஆ")), bstack1l1l1ll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫஇ"), bstack1l1l1ll_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧஈ"))
          with bstack11l111ll11_opy_:
            if os.path.exists(bstack1lll11l111_opy_):
              with open(bstack1lll11l111_opy_, bstack1l1l1ll_opy_ (u"࠭ࡲࠨஉ")) as f:
                content = f.read().strip()
                if content:
                  bstack1ll1l111l_opy_ = json.loads(bstack1l1l1ll_opy_ (u"ࠢࡼࠤஊ") + content + bstack1l1l1ll_opy_ (u"ࠨࠤࡻࠦ࠿ࠦࠢࡺࠤࠪ஋") + bstack1l1l1ll_opy_ (u"ࠤࢀࠦ஌"))
                  bstack11lllll1ll_opy_ = bstack1ll1l111l_opy_.get(str(threading.get_ident()))
      except Exception as e:
        logger.debug(bstack1l1l1ll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡵࡩࡦࡪࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡎࡊࡳࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢࡷࡩࡸࡺࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࠩ஍") + str(e))
      if bstack1lll1l1l1l_opy_:
        with bstack1l1l111l1_opy_:
          bstack11l11lll1l_opy_ = bstack1lll1l1l1l_opy_.copy()
        for driver in bstack11l11lll1l_opy_:
          if bstack11lllll1ll_opy_ == driver.session_id:
            bstack11111ll11_opy_ = driver
    bstack1l11ll111l_opy_ = bstack1lll11l1ll_opy_.bstack111l1lll1_opy_(test.tags)
    if bstack11111ll11_opy_:
      threading.current_thread().isA11yTest = bstack1lll11l1ll_opy_.bstack1l1l1l11_opy_(bstack11111ll11_opy_, bstack1l11ll111l_opy_)
      threading.current_thread().isAppA11yTest = bstack1lll11l1ll_opy_.bstack1l1l1l11_opy_(bstack11111ll11_opy_, bstack1l11ll111l_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1l11ll111l_opy_
      threading.current_thread().isAppA11yTest = bstack1l11ll111l_opy_
  except:
    pass
  bstack1l111lll1_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1ll1ll1l1_opy_
  try:
    bstack1ll1ll1l1_opy_ = self._test
  except:
    bstack1ll1ll1l1_opy_ = self.test
def bstack111l11lll_opy_():
  global bstack1l11ll11l1_opy_
  try:
    if os.path.exists(bstack1l11ll11l1_opy_):
      os.remove(bstack1l11ll11l1_opy_)
  except Exception as e:
    logger.debug(bstack1l1l1ll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧஎ") + str(e))
def bstack111l1ll11_opy_():
  global bstack1l11ll11l1_opy_
  bstack1ll1l111_opy_ = {}
  lock_file = bstack1l11ll11l1_opy_ + bstack1l1l1ll_opy_ (u"ࠬ࠴࡬ࡰࡥ࡮ࠫஏ")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l1l1ll_opy_ (u"࠭ࡦࡪ࡮ࡨࡰࡴࡩ࡫ࠡࡰࡲࡸࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥ࠭ࠢࡸࡷ࡮ࡴࡧࠡࡤࡤࡷ࡮ࡩࠠࡧ࡫࡯ࡩࠥࡵࡰࡦࡴࡤࡸ࡮ࡵ࡮ࡴࠩஐ"))
    try:
      if not os.path.isfile(bstack1l11ll11l1_opy_):
        with open(bstack1l11ll11l1_opy_, bstack1l1l1ll_opy_ (u"ࠧࡸࠩ஑")) as f:
          json.dump({}, f)
      if os.path.exists(bstack1l11ll11l1_opy_):
        with open(bstack1l11ll11l1_opy_, bstack1l1l1ll_opy_ (u"ࠨࡴࠪஒ")) as f:
          content = f.read().strip()
          if content:
            bstack1ll1l111_opy_ = json.loads(content)
    except Exception as e:
      logger.debug(bstack1l1l1ll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡷ࡫ࡡࡥ࡫ࡱ࡫ࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫஓ") + str(e))
    return bstack1ll1l111_opy_
  try:
    os.makedirs(os.path.dirname(bstack1l11ll11l1_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      if not os.path.isfile(bstack1l11ll11l1_opy_):
        with open(bstack1l11ll11l1_opy_, bstack1l1l1ll_opy_ (u"ࠪࡻࠬஔ")) as f:
          json.dump({}, f)
      if os.path.exists(bstack1l11ll11l1_opy_):
        with open(bstack1l11ll11l1_opy_, bstack1l1l1ll_opy_ (u"ࠫࡷ࠭க")) as f:
          content = f.read().strip()
          if content:
            bstack1ll1l111_opy_ = json.loads(content)
  except Exception as e:
    logger.debug(bstack1l1l1ll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡳࡧࡤࡨ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧ஖") + str(e))
  finally:
    return bstack1ll1l111_opy_
def bstack1lll1lll11_opy_(platform_index, item_index):
  global bstack1l11ll11l1_opy_
  lock_file = bstack1l11ll11l1_opy_ + bstack1l1l1ll_opy_ (u"࠭࠮࡭ࡱࡦ࡯ࠬ஗")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l1l1ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡱࡵࡣ࡬ࠢࡱࡳࡹࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦ࠮ࠣࡹࡸ࡯࡮ࡨࠢࡥࡥࡸ࡯ࡣࠡࡨ࡬ࡰࡪࠦ࡯ࡱࡧࡵࡥࡹ࡯࡯࡯ࡵࠪ஘"))
    try:
      bstack1ll1l111_opy_ = {}
      if os.path.exists(bstack1l11ll11l1_opy_):
        with open(bstack1l11ll11l1_opy_, bstack1l1l1ll_opy_ (u"ࠨࡴࠪங")) as f:
          content = f.read().strip()
          if content:
            bstack1ll1l111_opy_ = json.loads(content)
      bstack1ll1l111_opy_[item_index] = platform_index
      with open(bstack1l11ll11l1_opy_, bstack1l1l1ll_opy_ (u"ࠤࡺࠦச")) as outfile:
        json.dump(bstack1ll1l111_opy_, outfile)
    except Exception as e:
      logger.debug(bstack1l1l1ll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡽࡲࡪࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨ஛") + str(e))
    return
  try:
    os.makedirs(os.path.dirname(bstack1l11ll11l1_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      bstack1ll1l111_opy_ = {}
      if os.path.exists(bstack1l11ll11l1_opy_):
        with open(bstack1l11ll11l1_opy_, bstack1l1l1ll_opy_ (u"ࠫࡷ࠭ஜ")) as f:
          content = f.read().strip()
          if content:
            bstack1ll1l111_opy_ = json.loads(content)
      bstack1ll1l111_opy_[item_index] = platform_index
      with open(bstack1l11ll11l1_opy_, bstack1l1l1ll_opy_ (u"ࠧࡽࠢ஝")) as outfile:
        json.dump(bstack1ll1l111_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1l1l1ll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡹࡵ࡭ࡹ࡯࡮ࡨࠢࡷࡳࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫஞ") + str(e))
def bstack1ll1111lll_opy_(bstack11111l1ll_opy_):
  global CONFIG
  bstack1lllll1111_opy_ = bstack1l1l1ll_opy_ (u"ࠧࠨட")
  if not bstack1l1l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ஠") in CONFIG:
    logger.info(bstack1l1l1ll_opy_ (u"ࠩࡑࡳࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠡࡲࡤࡷࡸ࡫ࡤࠡࡷࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࠦࡲࡦࡲࡲࡶࡹࠦࡦࡰࡴࠣࡖࡴࡨ࡯ࡵࠢࡵࡹࡳ࠭஡"))
  try:
    platform = CONFIG[bstack1l1l1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭஢")][bstack11111l1ll_opy_]
    if bstack1l1l1ll_opy_ (u"ࠫࡴࡹࠧண") in platform:
      bstack1lllll1111_opy_ += str(platform[bstack1l1l1ll_opy_ (u"ࠬࡵࡳࠨத")]) + bstack1l1l1ll_opy_ (u"࠭ࠬࠡࠩ஥")
    if bstack1l1l1ll_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪ஦") in platform:
      bstack1lllll1111_opy_ += str(platform[bstack1l1l1ll_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫ஧")]) + bstack1l1l1ll_opy_ (u"ࠩ࠯ࠤࠬந")
    if bstack1l1l1ll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧன") in platform:
      bstack1lllll1111_opy_ += str(platform[bstack1l1l1ll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨப")]) + bstack1l1l1ll_opy_ (u"ࠬ࠲ࠠࠨ஫")
    if bstack1l1l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ஬") in platform:
      bstack1lllll1111_opy_ += str(platform[bstack1l1l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ஭")]) + bstack1l1l1ll_opy_ (u"ࠨ࠮ࠣࠫம")
    if bstack1l1l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧய") in platform:
      bstack1lllll1111_opy_ += str(platform[bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨர")]) + bstack1l1l1ll_opy_ (u"ࠫ࠱ࠦࠧற")
    if bstack1l1l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ல") in platform:
      bstack1lllll1111_opy_ += str(platform[bstack1l1l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧள")]) + bstack1l1l1ll_opy_ (u"ࠧ࠭ࠢࠪழ")
  except Exception as e:
    logger.debug(bstack1l1l1ll_opy_ (u"ࠨࡕࡲࡱࡪࠦࡥࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡱ࡫ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡴࡶࡵ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡷ࡫ࡰࡰࡴࡷࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡵ࡮ࠨவ") + str(e))
  finally:
    if bstack1lllll1111_opy_[len(bstack1lllll1111_opy_) - 2:] == bstack1l1l1ll_opy_ (u"ࠩ࠯ࠤࠬஶ"):
      bstack1lllll1111_opy_ = bstack1lllll1111_opy_[:-2]
    return bstack1lllll1111_opy_
def bstack1ll11l1111_opy_(path, bstack1lllll1111_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack11l1lll1l1_opy_ = ET.parse(path)
    bstack11lll1ll1l_opy_ = bstack11l1lll1l1_opy_.getroot()
    bstack1l1l111l_opy_ = None
    for suite in bstack11lll1ll1l_opy_.iter(bstack1l1l1ll_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩஷ")):
      if bstack1l1l1ll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫஸ") in suite.attrib:
        suite.attrib[bstack1l1l1ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪஹ")] += bstack1l1l1ll_opy_ (u"࠭ࠠࠨ஺") + bstack1lllll1111_opy_
        bstack1l1l111l_opy_ = suite
    bstack1l1l1l111l_opy_ = None
    for robot in bstack11lll1ll1l_opy_.iter(bstack1l1l1ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭஻")):
      bstack1l1l1l111l_opy_ = robot
    bstack1l1l11lll_opy_ = len(bstack1l1l1l111l_opy_.findall(bstack1l1l1ll_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧ஼")))
    if bstack1l1l11lll_opy_ == 1:
      bstack1l1l1l111l_opy_.remove(bstack1l1l1l111l_opy_.findall(bstack1l1l1ll_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨ஽"))[0])
      bstack1l1l11l1ll_opy_ = ET.Element(bstack1l1l1ll_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩா"), attrib={bstack1l1l1ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩி"): bstack1l1l1ll_opy_ (u"࡙ࠬࡵࡪࡶࡨࡷࠬீ"), bstack1l1l1ll_opy_ (u"࠭ࡩࡥࠩு"): bstack1l1l1ll_opy_ (u"ࠧࡴ࠲ࠪூ")})
      bstack1l1l1l111l_opy_.insert(1, bstack1l1l11l1ll_opy_)
      bstack11lll1l1ll_opy_ = None
      for suite in bstack1l1l1l111l_opy_.iter(bstack1l1l1ll_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧ௃")):
        bstack11lll1l1ll_opy_ = suite
      bstack11lll1l1ll_opy_.append(bstack1l1l111l_opy_)
      bstack1lll1l11_opy_ = None
      for status in bstack1l1l111l_opy_.iter(bstack1l1l1ll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ௄")):
        bstack1lll1l11_opy_ = status
      bstack11lll1l1ll_opy_.append(bstack1lll1l11_opy_)
    bstack11l1lll1l1_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1l1l1ll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡳࡵ࡬ࡲ࡬ࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠨ௅") + str(e))
def bstack11ll1l1l11_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1111l11l_opy_
  global CONFIG
  if bstack1l1l1ll_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡴࡦࡺࡨࠣெ") in options:
    del options[bstack1l1l1ll_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡵࡧࡴࡩࠤே")]
  bstack1l111l11_opy_ = bstack111l1ll11_opy_()
  for item_id in bstack1l111l11_opy_.keys():
    path = os.path.join(os.getcwd(), bstack1l1l1ll_opy_ (u"࠭ࡰࡢࡤࡲࡸࡤࡸࡥࡴࡷ࡯ࡸࡸ࠭ை"), str(item_id), bstack1l1l1ll_opy_ (u"ࠧࡰࡷࡷࡴࡺࡺ࠮ࡹ࡯࡯ࠫ௉"))
    bstack1ll11l1111_opy_(path, bstack1ll1111lll_opy_(bstack1l111l11_opy_[item_id]))
  bstack111l11lll_opy_()
  return bstack1111l11l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack11l1ll11_opy_(self, ff_profile_dir):
  global bstack11111l111_opy_
  if not ff_profile_dir:
    return None
  return bstack11111l111_opy_(self, ff_profile_dir)
def bstack11ll1l11ll_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack11l11lll11_opy_
  bstack1l1l11111l_opy_ = []
  if bstack1l1l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫொ") in CONFIG:
    bstack1l1l11111l_opy_ = CONFIG[bstack1l1l1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬோ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1l1l1ll_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࠦௌ")],
      pabot_args[bstack1l1l1ll_opy_ (u"ࠦࡻ࡫ࡲࡣࡱࡶࡩ்ࠧ")],
      argfile,
      pabot_args.get(bstack1l1l1ll_opy_ (u"ࠧ࡮ࡩࡷࡧࠥ௎")),
      pabot_args[bstack1l1l1ll_opy_ (u"ࠨࡰࡳࡱࡦࡩࡸࡹࡥࡴࠤ௏")],
      platform[0],
      bstack11l11lll11_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1l1l1ll_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡨ࡬ࡰࡪࡹࠢௐ")] or [(bstack1l1l1ll_opy_ (u"ࠣࠤ௑"), None)]
    for platform in enumerate(bstack1l1l11111l_opy_)
  ]
def bstack1l1l1l1lll_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack11l111111l_opy_=bstack1l1l1ll_opy_ (u"ࠩࠪ௒")):
  global bstack1ll11ll111_opy_
  self.platform_index = platform_index
  self.bstack11l1llll1_opy_ = bstack11l111111l_opy_
  bstack1ll11ll111_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack11l1llllll_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1llll1ll_opy_
  global bstack1l1l1ll1l1_opy_
  bstack1l11ll1lll_opy_ = copy.deepcopy(item)
  if not bstack1l1l1ll_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ௓") in item.options:
    bstack1l11ll1lll_opy_.options[bstack1l1l1ll_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭௔")] = []
  bstack1ll1ll1ll1_opy_ = bstack1l11ll1lll_opy_.options[bstack1l1l1ll_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ௕")].copy()
  for v in bstack1l11ll1lll_opy_.options[bstack1l1l1ll_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨ௖")]:
    if bstack1l1l1ll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝࠭ௗ") in v:
      bstack1ll1ll1ll1_opy_.remove(v)
    if bstack1l1l1ll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓࠨ௘") in v:
      bstack1ll1ll1ll1_opy_.remove(v)
    if bstack1l1l1ll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡆࡈࡊࡑࡕࡃࡂࡎࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭௙") in v:
      bstack1ll1ll1ll1_opy_.remove(v)
  bstack1ll1ll1ll1_opy_.insert(0, bstack1l1l1ll_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡓࡐࡆ࡚ࡆࡐࡔࡐࡍࡓࡊࡅ࡙࠼ࡾࢁࠬ௚").format(bstack1l11ll1lll_opy_.platform_index))
  bstack1ll1ll1ll1_opy_.insert(0, bstack1l1l1ll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒ࠻ࡽࢀࠫ௛").format(bstack1l11ll1lll_opy_.bstack11l1llll1_opy_))
  bstack1l11ll1lll_opy_.options[bstack1l1l1ll_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ௜")] = bstack1ll1ll1ll1_opy_
  if bstack1l1l1ll1l1_opy_:
    bstack1l11ll1lll_opy_.options[bstack1l1l1ll_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨ௝")].insert(0, bstack1l1l1ll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙࠺ࡼࡿࠪ௞").format(bstack1l1l1ll1l1_opy_))
  return bstack1llll1ll_opy_(caller_id, datasources, is_last, bstack1l11ll1lll_opy_, outs_dir)
def bstack1ll1lll1l_opy_(command, item_index):
  try:
    if bstack1l1l1111l1_opy_.get_property(bstack1l1l1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩ௟")):
      os.environ[bstack1l1l1ll_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪ௠")] = json.dumps(CONFIG[bstack1l1l1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭௡")][item_index % bstack1lll11ll11_opy_])
    global bstack1l1l1ll1l1_opy_
    if bstack1l1l1ll1l1_opy_:
      command[0] = command[0].replace(bstack1l1l1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ௢"), bstack1l1l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡸࡪ࡫ࠡࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠢ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠡࠩ௣") + str(
        item_index) + bstack1l1l1ll_opy_ (u"࠭ࠠࠨ௤") + bstack1l1l1ll1l1_opy_, 1)
    else:
      command[0] = command[0].replace(bstack1l1l1ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭௥"),
                                      bstack1l1l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡴࡦ࡮ࠤࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠥ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠤࠬ௦") + str(item_index), 1)
  except Exception as e:
    logger.error(bstack1l1l1ll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡯ࡲࡨ࡮࡬ࡹࡪࡰࡪࠤࡨࡵ࡭࡮ࡣࡱࡨࠥ࡬࡯ࡳࠢࡳࡥࡧࡵࡴࠡࡴࡸࡲ࠿ࠦࡻࡾࠩ௧").format(str(e)))
def bstack1l1l11l11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1lll11lll_opy_
  try:
    bstack1ll1lll1l_opy_(command, item_index)
    return bstack1lll11lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
  except Exception as e:
    logger.error(bstack1l1l1ll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡣࡱࡷࠤࡷࡻ࡮࠻ࠢࡾࢁࠬ௨").format(str(e)))
    raise e
def bstack1l1ll11l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1lll11lll_opy_
  try:
    bstack1ll1lll1l_opy_(command, item_index)
    return bstack1lll11lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
  except Exception as e:
    logger.error(bstack1l1l1ll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡢࡤࡲࡸࠥࡸࡵ࡯ࠢ࠵࠲࠶࠹࠺ࠡࡽࢀࠫ௩").format(str(e)))
    try:
      return bstack1lll11lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
    except Exception as e2:
      logger.error(bstack1l1l1ll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡥࡳࡹࠦ࠲࠯࠳࠶ࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࡼࡿࠪ௪").format(str(e2)))
      raise e
def bstack1l1lllll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1lll11lll_opy_
  try:
    bstack1ll1lll1l_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    return bstack1lll11lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
  except Exception as e:
    logger.error(bstack1l1l1ll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠࡳࡷࡱࠤ࠷࠴࠱࠶࠼ࠣࡿࢂ࠭௫").format(str(e)))
    try:
      return bstack1lll11lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
    except Exception as e2:
      logger.error(bstack1l1l1ll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡧࡵࡴࠡ࠴࠱࠵࠺ࠦࡦࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢࡾࢁࠬ௬").format(str(e2)))
      raise e
def bstack111l11ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack1lll11lll_opy_
  try:
    bstack1ll1lll1l_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    if sleep_before_start and sleep_before_start > 0:
      import time
      time.sleep(min(sleep_before_start, 5))
    return bstack1lll11lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack1l1l1ll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡦࡨ࡯ࡵࠢࡵࡹࡳࠦ࠴࠯࠴࠽ࠤࢀࢃࠧ௭").format(str(e)))
    try:
      return bstack1lll11lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack1l1l1ll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡢࡰࡶࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࡻࡾࠩ௮").format(str(e2)))
      raise e
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack11ll1llll_opy_(self, runner, quiet=False, capture=True):
  global bstack1ll111llll_opy_
  bstack11ll1l111l_opy_ = bstack1ll111llll_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack1l1l1ll_opy_ (u"ࠪࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࡥࡡࡳࡴࠪ௯")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1l1l1ll_opy_ (u"ࠫࡪࡾࡣࡠࡶࡵࡥࡨ࡫ࡢࡢࡥ࡮ࡣࡦࡸࡲࠨ௰")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack11ll1l111l_opy_
def bstack111l111l1_opy_(runner, hook_name, context, element, bstack1ll1lll1_opy_, *args):
  try:
    if runner.hooks.get(hook_name):
      bstack1ll1l1ll11_opy_.bstack1ll11l11l1_opy_(hook_name, element)
    bstack1ll1lll1_opy_(runner, hook_name, context, *args)
    if runner.hooks.get(hook_name):
      bstack1ll1l1ll11_opy_.bstack1111l11l1_opy_(element)
      if hook_name not in [bstack1l1l1ll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠩ௱"), bstack1l1l1ll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠩ௲")] and args and hasattr(args[0], bstack1l1l1ll_opy_ (u"ࠧࡦࡴࡵࡳࡷࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠧ௳")):
        args[0].error_message = bstack1l1l1ll_opy_ (u"ࠨࠩ௴")
  except Exception as e:
    logger.debug(bstack1l1l1ll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡮ࡡ࡯ࡦ࡯ࡩࠥ࡮࡯ࡰ࡭ࡶࠤ࡮ࡴࠠࡣࡧ࡫ࡥࡻ࡫࠺ࠡࡽࢀࠫ௵").format(str(e)))
@measure(event_name=EVENTS.bstack11l1lll11l_opy_, stage=STAGE.bstack1l1ll11l1_opy_, hook_type=bstack1l1l1ll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡄࡰࡱࠨ௶"), bstack111l1llll_opy_=bstack1llll111_opy_)
def bstack1l1l1l11ll_opy_(runner, name, context, bstack1ll1lll1_opy_, *args):
    if runner.hooks.get(bstack1l1l1ll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣ௷")).__name__ != bstack1l1l1ll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࡡࡧࡩ࡫ࡧࡵ࡭ࡶࡢ࡬ࡴࡵ࡫ࠣ௸"):
      bstack111l111l1_opy_(runner, name, context, runner, bstack1ll1lll1_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack11l1ll11l1_opy_(bstack1l1l1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ௹")) else context.browser
      runner.driver_initialised = bstack1l1l1ll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦ௺")
    except Exception as e:
      logger.debug(bstack1l1l1ll_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡦࡵ࡭ࡻ࡫ࡲࠡ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡶࡩࠥࡧࡴࡵࡴ࡬ࡦࡺࡺࡥ࠻ࠢࡾࢁࠬ௻").format(str(e)))
def bstack1l1llllll_opy_(runner, name, context, bstack1ll1lll1_opy_, *args):
    bstack111l111l1_opy_(runner, name, context, context.feature, bstack1ll1lll1_opy_, *args)
    try:
      if not bstack1lll1lll1l_opy_:
        bstack11111ll11_opy_ = threading.current_thread().bstackSessionDriver if bstack11l1ll11l1_opy_(bstack1l1l1ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ௼")) else context.browser
        if is_driver_active(bstack11111ll11_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack1l1l1ll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦ௽")
          bstack1l11111111_opy_ = str(runner.feature.name)
          bstack1ll11l11_opy_(context, bstack1l11111111_opy_)
          bstack11111ll11_opy_.execute_script(bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩ௾") + json.dumps(bstack1l11111111_opy_) + bstack1l1l1ll_opy_ (u"ࠬࢃࡽࠨ௿"))
    except Exception as e:
      logger.debug(bstack1l1l1ll_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭ఀ").format(str(e)))
def bstack1ll111ll11_opy_(runner, name, context, bstack1ll1lll1_opy_, *args):
    if hasattr(context, bstack1l1l1ll_opy_ (u"ࠧࡴࡥࡨࡲࡦࡸࡩࡰࠩఁ")):
        bstack1ll1l1ll11_opy_.start_test(context)
    target = context.scenario if hasattr(context, bstack1l1l1ll_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪం")) else context.feature
    bstack111l111l1_opy_(runner, name, context, target, bstack1ll1lll1_opy_, *args)
@measure(event_name=EVENTS.bstack1l1l111lll_opy_, stage=STAGE.bstack1l1ll11l1_opy_, bstack111l1llll_opy_=bstack1llll111_opy_)
def bstack111lll1ll_opy_(runner, name, context, bstack1ll1lll1_opy_, *args):
    if len(context.scenario.tags) == 0: bstack1ll1l1ll11_opy_.start_test(context)
    bstack111l111l1_opy_(runner, name, context, context.scenario, bstack1ll1lll1_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack1l111l1ll1_opy_.bstack1l111lll1l_opy_(context, *args)
    try:
      bstack11111ll11_opy_ = bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨః"), context.browser)
      if is_driver_active(bstack11111ll11_opy_):
        bstack1llllll11l_opy_.bstack11l1l1111l_opy_(bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩఄ"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack1l1l1ll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨఅ")
        if (not bstack1lll1lll1l_opy_):
          scenario_name = args[0].name
          feature_name = bstack1l11111111_opy_ = str(runner.feature.name)
          bstack1l11111111_opy_ = feature_name + bstack1l1l1ll_opy_ (u"ࠬࠦ࠭ࠡࠩఆ") + scenario_name
          if runner.driver_initialised == bstack1l1l1ll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣఇ"):
            bstack1ll11l11_opy_(context, bstack1l11111111_opy_)
            bstack11111ll11_opy_.execute_script(bstack1l1l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬఈ") + json.dumps(bstack1l11111111_opy_) + bstack1l1l1ll_opy_ (u"ࠨࡿࢀࠫఉ"))
    except Exception as e:
      logger.debug(bstack1l1l1ll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡ࡫ࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡀࠠࡼࡿࠪఊ").format(str(e)))
@measure(event_name=EVENTS.bstack11l1lll11l_opy_, stage=STAGE.bstack1l1ll11l1_opy_, hook_type=bstack1l1l1ll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡖࡸࡪࡶࠢఋ"), bstack111l1llll_opy_=bstack1llll111_opy_)
def bstack1l1llll1l_opy_(runner, name, context, bstack1ll1lll1_opy_, *args):
    bstack111l111l1_opy_(runner, name, context, args[0], bstack1ll1lll1_opy_, *args)
    try:
      bstack11111ll11_opy_ = threading.current_thread().bstackSessionDriver if bstack11l1ll11l1_opy_(bstack1l1l1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪఌ")) else context.browser
      if is_driver_active(bstack11111ll11_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack1l1l1ll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥ఍")
        bstack1ll1l1ll11_opy_.bstack11111ll1_opy_(args[0])
        if runner.driver_initialised == bstack1l1l1ll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦఎ"):
          feature_name = bstack1l11111111_opy_ = str(runner.feature.name)
          bstack1l11111111_opy_ = feature_name + bstack1l1l1ll_opy_ (u"ࠧࠡ࠯ࠣࠫఏ") + context.scenario.name
          bstack11111ll11_opy_.execute_script(bstack1l1l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭ఐ") + json.dumps(bstack1l11111111_opy_) + bstack1l1l1ll_opy_ (u"ࠩࢀࢁࠬ఑"))
    except Exception as e:
      logger.debug(bstack1l1l1ll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡴࡦࡲ࠽ࠤࢀࢃࠧఒ").format(str(e)))
@measure(event_name=EVENTS.bstack11l1lll11l_opy_, stage=STAGE.bstack1l1ll11l1_opy_, hook_type=bstack1l1l1ll_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࡖࡸࡪࡶࠢఓ"), bstack111l1llll_opy_=bstack1llll111_opy_)
def bstack111llllll1_opy_(runner, name, context, bstack1ll1lll1_opy_, *args):
  bstack1ll1l1ll11_opy_.bstack1ll1ll111l_opy_(args[0])
  try:
    step_status = args[0].status.name
    bstack11111ll11_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1l1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫఔ") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack11111ll11_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack1l1l1ll_opy_ (u"࠭ࡩ࡯ࡵࡷࡩࡵ࠭క")
        feature_name = bstack1l11111111_opy_ = str(runner.feature.name)
        bstack1l11111111_opy_ = feature_name + bstack1l1l1ll_opy_ (u"ࠧࠡ࠯ࠣࠫఖ") + context.scenario.name
        bstack11111ll11_opy_.execute_script(bstack1l1l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭గ") + json.dumps(bstack1l11111111_opy_) + bstack1l1l1ll_opy_ (u"ࠩࢀࢁࠬఘ"))
    if str(step_status).lower() == bstack1l1l1ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪఙ"):
      bstack1l11lllll1_opy_ = bstack1l1l1ll_opy_ (u"ࠫࠬచ")
      bstack11l1l1l1ll_opy_ = bstack1l1l1ll_opy_ (u"ࠬ࠭ఛ")
      bstack1l11l11ll1_opy_ = bstack1l1l1ll_opy_ (u"࠭ࠧజ")
      try:
        import traceback
        bstack1l11lllll1_opy_ = runner.exception.__class__.__name__
        bstack1l11llll_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack11l1l1l1ll_opy_ = bstack1l1l1ll_opy_ (u"ࠧࠡࠩఝ").join(bstack1l11llll_opy_)
        bstack1l11l11ll1_opy_ = bstack1l11llll_opy_[-1]
      except Exception as e:
        logger.debug(bstack11ll1ll111_opy_.format(str(e)))
      bstack1l11lllll1_opy_ += bstack1l11l11ll1_opy_
      bstack1llllll1ll_opy_(context, json.dumps(str(args[0].name) + bstack1l1l1ll_opy_ (u"ࠣࠢ࠰ࠤࡋࡧࡩ࡭ࡧࡧࠥࡡࡴࠢఞ") + str(bstack11l1l1l1ll_opy_)),
                          bstack1l1l1ll_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣట"))
      if runner.driver_initialised == bstack1l1l1ll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣఠ"):
        bstack1llll111ll_opy_(getattr(context, bstack1l1l1ll_opy_ (u"ࠫࡵࡧࡧࡦࠩడ"), None), bstack1l1l1ll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧఢ"), bstack1l11lllll1_opy_)
        bstack11111ll11_opy_.execute_script(bstack1l1l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫణ") + json.dumps(str(args[0].name) + bstack1l1l1ll_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨత") + str(bstack11l1l1l1ll_opy_)) + bstack1l1l1ll_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨథ"))
      if runner.driver_initialised == bstack1l1l1ll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢద"):
        bstack11ll111111_opy_(bstack11111ll11_opy_, bstack1l1l1ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪధ"), bstack1l1l1ll_opy_ (u"ࠦࡘࡩࡥ࡯ࡣࡵ࡭ࡴࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࡢ࡮ࠣన") + str(bstack1l11lllll1_opy_))
    else:
      bstack1llllll1ll_opy_(context, bstack1l1l1ll_opy_ (u"ࠧࡖࡡࡴࡵࡨࡨࠦࠨ఩"), bstack1l1l1ll_opy_ (u"ࠨࡩ࡯ࡨࡲࠦప"))
      if runner.driver_initialised == bstack1l1l1ll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧఫ"):
        bstack1llll111ll_opy_(getattr(context, bstack1l1l1ll_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭బ"), None), bstack1l1l1ll_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤభ"))
      bstack11111ll11_opy_.execute_script(bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨమ") + json.dumps(str(args[0].name) + bstack1l1l1ll_opy_ (u"ࠦࠥ࠳ࠠࡑࡣࡶࡷࡪࡪࠡࠣయ")) + bstack1l1l1ll_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫర"))
      if runner.driver_initialised == bstack1l1l1ll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦఱ"):
        bstack11ll111111_opy_(bstack11111ll11_opy_, bstack1l1l1ll_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢల"))
  except Exception as e:
    logger.debug(bstack1l1l1ll_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࠥࡹࡴࡦࡲ࠽ࠤࢀࢃࠧళ").format(str(e)))
  bstack111l111l1_opy_(runner, name, context, args[0], bstack1ll1lll1_opy_, *args)
@measure(event_name=EVENTS.bstack111lll111_opy_, stage=STAGE.bstack1l1ll11l1_opy_, bstack111l1llll_opy_=bstack1llll111_opy_)
def bstack1lllll1ll1_opy_(runner, name, context, bstack1ll1lll1_opy_, *args):
  bstack1ll1l1ll11_opy_.end_test(args[0])
  try:
    bstack1l11l11l_opy_ = args[0].status.name
    bstack11111ll11_opy_ = bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨఴ"), context.browser)
    bstack1l111l1ll1_opy_.bstack1l11l1l111_opy_(bstack11111ll11_opy_)
    if str(bstack1l11l11l_opy_).lower() == bstack1l1l1ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪవ"):
      bstack1l11lllll1_opy_ = bstack1l1l1ll_opy_ (u"ࠫࠬశ")
      bstack11l1l1l1ll_opy_ = bstack1l1l1ll_opy_ (u"ࠬ࠭ష")
      bstack1l11l11ll1_opy_ = bstack1l1l1ll_opy_ (u"࠭ࠧస")
      try:
        import traceback
        bstack1l11lllll1_opy_ = runner.exception.__class__.__name__
        bstack1l11llll_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack11l1l1l1ll_opy_ = bstack1l1l1ll_opy_ (u"ࠧࠡࠩహ").join(bstack1l11llll_opy_)
        bstack1l11l11ll1_opy_ = bstack1l11llll_opy_[-1]
      except Exception as e:
        logger.debug(bstack11ll1ll111_opy_.format(str(e)))
      bstack1l11lllll1_opy_ += bstack1l11l11ll1_opy_
      bstack1llllll1ll_opy_(context, json.dumps(str(args[0].name) + bstack1l1l1ll_opy_ (u"ࠣࠢ࠰ࠤࡋࡧࡩ࡭ࡧࡧࠥࡡࡴࠢ఺") + str(bstack11l1l1l1ll_opy_)),
                          bstack1l1l1ll_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣ఻"))
      if runner.driver_initialised == bstack1l1l1ll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳ఼ࠧ") or runner.driver_initialised == bstack1l1l1ll_opy_ (u"ࠫ࡮ࡴࡳࡵࡧࡳࠫఽ"):
        bstack1llll111ll_opy_(getattr(context, bstack1l1l1ll_opy_ (u"ࠬࡶࡡࡨࡧࠪా"), None), bstack1l1l1ll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨి"), bstack1l11lllll1_opy_)
        bstack11111ll11_opy_.execute_script(bstack1l1l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬీ") + json.dumps(str(args[0].name) + bstack1l1l1ll_opy_ (u"ࠣࠢ࠰ࠤࡋࡧࡩ࡭ࡧࡧࠥࡡࡴࠢు") + str(bstack11l1l1l1ll_opy_)) + bstack1l1l1ll_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࡽࡾࠩూ"))
      if runner.driver_initialised == bstack1l1l1ll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧృ") or runner.driver_initialised == bstack1l1l1ll_opy_ (u"ࠫ࡮ࡴࡳࡵࡧࡳࠫౄ"):
        bstack11ll111111_opy_(bstack11111ll11_opy_, bstack1l1l1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ౅"), bstack1l1l1ll_opy_ (u"ࠨࡓࡤࡧࡱࡥࡷ࡯࡯ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥె") + str(bstack1l11lllll1_opy_))
    else:
      bstack1llllll1ll_opy_(context, bstack1l1l1ll_opy_ (u"ࠢࡑࡣࡶࡷࡪࡪࠡࠣే"), bstack1l1l1ll_opy_ (u"ࠣ࡫ࡱࡪࡴࠨై"))
      if runner.driver_initialised == bstack1l1l1ll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦ౉") or runner.driver_initialised == bstack1l1l1ll_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪొ"):
        bstack1llll111ll_opy_(getattr(context, bstack1l1l1ll_opy_ (u"ࠫࡵࡧࡧࡦࠩో"), None), bstack1l1l1ll_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧౌ"))
      bstack11111ll11_opy_.execute_script(bstack1l1l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽్ࠫ") + json.dumps(str(args[0].name) + bstack1l1l1ll_opy_ (u"ࠢࠡ࠯ࠣࡔࡦࡹࡳࡦࡦࠤࠦ౎")) + bstack1l1l1ll_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦࢂࢃࠧ౏"))
      if runner.driver_initialised == bstack1l1l1ll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦ౐") or runner.driver_initialised == bstack1l1l1ll_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪ౑"):
        bstack11ll111111_opy_(bstack11111ll11_opy_, bstack1l1l1ll_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ౒"))
  except Exception as e:
    logger.debug(bstack1l1l1ll_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧ౓").format(str(e)))
  bstack111l111l1_opy_(runner, name, context, context.scenario, bstack1ll1lll1_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack1l1ll11l1l_opy_(runner, name, context, bstack1ll1lll1_opy_, *args):
    target = context.scenario if hasattr(context, bstack1l1l1ll_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨ౔")) else context.feature
    bstack111l111l1_opy_(runner, name, context, target, bstack1ll1lll1_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack1ll11lllll_opy_(runner, name, context, bstack1ll1lll1_opy_, *args):
    try:
      bstack11111ll11_opy_ = bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷౕ࠭"), context.browser)
      bstack111l11ll_opy_ = bstack1l1l1ll_opy_ (u"ࠨౖࠩ")
      if context.failed is True:
        bstack11llll111_opy_ = []
        bstack1ll1l1l111_opy_ = []
        bstack1llll1ll1l_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack11llll111_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1l11llll_opy_ = traceback.format_tb(exc_tb)
            bstack111l11l1l_opy_ = bstack1l1l1ll_opy_ (u"ࠩࠣࠫ౗").join(bstack1l11llll_opy_)
            bstack1ll1l1l111_opy_.append(bstack111l11l1l_opy_)
            bstack1llll1ll1l_opy_.append(bstack1l11llll_opy_[-1])
        except Exception as e:
          logger.debug(bstack11ll1ll111_opy_.format(str(e)))
        bstack1l11lllll1_opy_ = bstack1l1l1ll_opy_ (u"ࠪࠫౘ")
        for i in range(len(bstack11llll111_opy_)):
          bstack1l11lllll1_opy_ += bstack11llll111_opy_[i] + bstack1llll1ll1l_opy_[i] + bstack1l1l1ll_opy_ (u"ࠫࡡࡴࠧౙ")
        bstack111l11ll_opy_ = bstack1l1l1ll_opy_ (u"ࠬࠦࠧౚ").join(bstack1ll1l1l111_opy_)
        if runner.driver_initialised in [bstack1l1l1ll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠢ౛"), bstack1l1l1ll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦ౜")]:
          bstack1llllll1ll_opy_(context, bstack111l11ll_opy_, bstack1l1l1ll_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢౝ"))
          bstack1llll111ll_opy_(getattr(context, bstack1l1l1ll_opy_ (u"ࠩࡳࡥ࡬࡫ࠧ౞"), None), bstack1l1l1ll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ౟"), bstack1l11lllll1_opy_)
          bstack11111ll11_opy_.execute_script(bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩౠ") + json.dumps(bstack111l11ll_opy_) + bstack1l1l1ll_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥࡩࡷࡸ࡯ࡳࠤࢀࢁࠬౡ"))
          bstack11ll111111_opy_(bstack11111ll11_opy_, bstack1l1l1ll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨౢ"), bstack1l1l1ll_opy_ (u"ࠢࡔࡱࡰࡩࠥࡹࡣࡦࡰࡤࡶ࡮ࡵࡳࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢ࡟ࡲࠧౣ") + str(bstack1l11lllll1_opy_))
          bstack1ll11lll_opy_ = bstack11l11llll_opy_(bstack111l11ll_opy_, runner.feature.name, logger)
          if (bstack1ll11lll_opy_ != None):
            bstack1l1lll1l1_opy_.append(bstack1ll11lll_opy_)
      else:
        if runner.driver_initialised in [bstack1l1l1ll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠤ౤"), bstack1l1l1ll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨ౥")]:
          bstack1llllll1ll_opy_(context, bstack1l1l1ll_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨ࠾ࠥࠨ౦") + str(runner.feature.name) + bstack1l1l1ll_opy_ (u"ࠦࠥࡶࡡࡴࡵࡨࡨࠦࠨ౧"), bstack1l1l1ll_opy_ (u"ࠧ࡯࡮ࡧࡱࠥ౨"))
          bstack1llll111ll_opy_(getattr(context, bstack1l1l1ll_opy_ (u"࠭ࡰࡢࡩࡨࠫ౩"), None), bstack1l1l1ll_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ౪"))
          bstack11111ll11_opy_.execute_script(bstack1l1l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭౫") + json.dumps(bstack1l1l1ll_opy_ (u"ࠤࡉࡩࡦࡺࡵࡳࡧ࠽ࠤࠧ౬") + str(runner.feature.name) + bstack1l1l1ll_opy_ (u"ࠥࠤࡵࡧࡳࡴࡧࡧࠥࠧ౭")) + bstack1l1l1ll_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢࡾࡿࠪ౮"))
          bstack11ll111111_opy_(bstack11111ll11_opy_, bstack1l1l1ll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ౯"))
          bstack1ll11lll_opy_ = bstack11l11llll_opy_(bstack111l11ll_opy_, runner.feature.name, logger)
          if (bstack1ll11lll_opy_ != None):
            bstack1l1lll1l1_opy_.append(bstack1ll11lll_opy_)
    except Exception as e:
      logger.debug(bstack1l1l1ll_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨ౰").format(str(e)))
    bstack111l111l1_opy_(runner, name, context, context.feature, bstack1ll1lll1_opy_, *args)
@measure(event_name=EVENTS.bstack11l1lll11l_opy_, stage=STAGE.bstack1l1ll11l1_opy_, hook_type=bstack1l1l1ll_opy_ (u"ࠢࡢࡨࡷࡩࡷࡇ࡬࡭ࠤ౱"), bstack111l1llll_opy_=bstack1llll111_opy_)
def bstack11llll1lll_opy_(runner, name, context, bstack1ll1lll1_opy_, *args):
    bstack111l111l1_opy_(runner, name, context, runner, bstack1ll1lll1_opy_, *args)
def bstack1l1lllllll_opy_(self, name, context, *args):
  try:
    if bstack1lllll111l_opy_:
      platform_index = int(threading.current_thread()._name) % bstack1lll11ll11_opy_
      bstack1ll1l1ll_opy_ = CONFIG[bstack1l1l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ౲")][platform_index]
      os.environ[bstack1l1l1ll_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪ౳")] = json.dumps(bstack1ll1l1ll_opy_)
    global bstack1ll1lll1_opy_
    if not hasattr(self, bstack1l1l1ll_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡸ࡫ࡤࠨ౴")):
      self.driver_initialised = None
    bstack1111ll1l1_opy_ = {
        bstack1l1l1ll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠨ౵"): bstack1l1l1l11ll_opy_,
        bstack1l1l1ll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭౶"): bstack1l1llllll_opy_,
        bstack1l1l1ll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡴࡢࡩࠪ౷"): bstack1ll111ll11_opy_,
        bstack1l1l1ll_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩ౸"): bstack111lll1ll_opy_,
        bstack1l1l1ll_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵ࠭౹"): bstack1l1llll1l_opy_,
        bstack1l1l1ll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡷࡩࡵ࠭౺"): bstack111llllll1_opy_,
        bstack1l1l1ll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ౻"): bstack1lllll1ll1_opy_,
        bstack1l1l1ll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡸࡦ࡭ࠧ౼"): bstack1l1ll11l1l_opy_,
        bstack1l1l1ll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬ౽"): bstack1ll11lllll_opy_,
        bstack1l1l1ll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠩ౾"): bstack11llll1lll_opy_
    }
    handler = bstack1111ll1l1_opy_.get(name, bstack1ll1lll1_opy_)
    try:
      handler(self, name, context, bstack1ll1lll1_opy_, *args)
    except Exception as e:
      logger.debug(bstack1l1l1ll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡥࡩ࡭ࡧࡶࡦࠢ࡫ࡳࡴࡱࠠࡩࡣࡱࡨࡱ࡫ࡲࠡࡽࢀ࠾ࠥࢁࡽࠨ౿").format(name, str(e)))
    if name in [bstack1l1l1ll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨಀ"), bstack1l1l1ll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪಁ"), bstack1l1l1ll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ࠭ಂ")]:
      try:
        bstack11111ll11_opy_ = threading.current_thread().bstackSessionDriver if bstack11l1ll11l1_opy_(bstack1l1l1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪಃ")) else context.browser
        bstack111ll1ll_opy_ = (
          (name == bstack1l1l1ll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠨ಄") and self.driver_initialised == bstack1l1l1ll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥಅ")) or
          (name == bstack1l1l1ll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡦࡦࡣࡷࡹࡷ࡫ࠧಆ") and self.driver_initialised == bstack1l1l1ll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠤಇ")) or
          (name == bstack1l1l1ll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪಈ") and self.driver_initialised in [bstack1l1l1ll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧಉ"), bstack1l1l1ll_opy_ (u"ࠦ࡮ࡴࡳࡵࡧࡳࠦಊ")]) or
          (name == bstack1l1l1ll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡺࡥࡱࠩಋ") and self.driver_initialised == bstack1l1l1ll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦಌ"))
        )
        if bstack111ll1ll_opy_:
          self.driver_initialised = None
          if bstack11111ll11_opy_ and hasattr(bstack11111ll11_opy_, bstack1l1l1ll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠫ಍")):
            try:
              bstack11111ll11_opy_.quit()
            except Exception as e:
              logger.debug(bstack1l1l1ll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡲࡷ࡬ࡸࡹ࡯࡮ࡨࠢࡧࡶ࡮ࡼࡥࡳࠢ࡬ࡲࠥࡨࡥࡩࡣࡹࡩࠥ࡮࡯ࡰ࡭࠽ࠤࢀࢃࠧಎ").format(str(e)))
      except Exception as e:
        logger.debug(bstack1l1l1ll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࠣ࡬ࡴࡵ࡫ࠡࡥ࡯ࡩࡦࡴࡵࡱࠢࡩࡳࡷࠦࡻࡾ࠼ࠣࡿࢂ࠭ಏ").format(name, str(e)))
  except Exception as e:
    logger.debug(bstack1l1l1ll_opy_ (u"ࠪࡇࡷ࡯ࡴࡪࡥࡤࡰࠥ࡫ࡲࡳࡱࡵࠤ࡮ࡴࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡳࡷࡱࠤ࡭ࡵ࡯࡬ࠢࡾࢁ࠿ࠦࡻࡾࠩಐ").format(name, str(e)))
    try:
      bstack1ll1lll1_opy_(self, name, context, *args)
    except Exception as e2:
      logger.debug(bstack1l1l1ll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࠣࡦࡪ࡮ࡡࡷࡧࠣ࡬ࡴࡵ࡫ࠡࡽࢀ࠾ࠥࢁࡽࠨ಑").format(name, str(e2)))
def bstack111lllll1_opy_(config, startdir):
  return bstack1l1l1ll_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶ࠿ࠦࡻ࠱ࡿࠥಒ").format(bstack1l1l1ll_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧಓ"))
notset = Notset()
def bstack1l1l1lll1_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1lll111111_opy_
  if str(name).lower() == bstack1l1l1ll_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸࠧಔ"):
    return bstack1l1l1ll_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢಕ")
  else:
    return bstack1lll111111_opy_(self, name, default, skip)
def bstack1ll1l11l1_opy_(item, when):
  global bstack11ll1111l_opy_
  try:
    bstack11ll1111l_opy_(item, when)
  except Exception as e:
    pass
def bstack11l111llll_opy_():
  return
def bstack111ll1l1_opy_(type, name, status, reason, bstack111111ll1_opy_, bstack1l1ll11ll1_opy_):
  bstack111llllll_opy_ = {
    bstack1l1l1ll_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩಖ"): type,
    bstack1l1l1ll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ಗ"): {}
  }
  if type == bstack1l1l1ll_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭ಘ"):
    bstack111llllll_opy_[bstack1l1l1ll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨಙ")][bstack1l1l1ll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬಚ")] = bstack111111ll1_opy_
    bstack111llllll_opy_[bstack1l1l1ll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪಛ")][bstack1l1l1ll_opy_ (u"ࠨࡦࡤࡸࡦ࠭ಜ")] = json.dumps(str(bstack1l1ll11ll1_opy_))
  if type == bstack1l1l1ll_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪಝ"):
    bstack111llllll_opy_[bstack1l1l1ll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ಞ")][bstack1l1l1ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩಟ")] = name
  if type == bstack1l1l1ll_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨಠ"):
    bstack111llllll_opy_[bstack1l1l1ll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩಡ")][bstack1l1l1ll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧಢ")] = status
    if status == bstack1l1l1ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨಣ"):
      bstack111llllll_opy_[bstack1l1l1ll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬತ")][bstack1l1l1ll_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪಥ")] = json.dumps(str(reason))
  bstack1lll11ll_opy_ = bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩದ").format(json.dumps(bstack111llllll_opy_))
  return bstack1lll11ll_opy_
def bstack1l1ll1ll11_opy_(driver_command, response):
    if driver_command == bstack1l1l1ll_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠩಧ"):
        bstack1llllll11l_opy_.bstack1111l111l_opy_({
            bstack1l1l1ll_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬನ"): response[bstack1l1l1ll_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭಩")],
            bstack1l1l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨಪ"): bstack1llllll11l_opy_.current_test_uuid()
        })
def bstack11lll1111_opy_(item, call, rep):
  global bstack11111l1l_opy_
  global bstack1lll1l1l1l_opy_
  global bstack1lll1lll1l_opy_
  name = bstack1l1l1ll_opy_ (u"ࠩࠪಫ")
  try:
    if rep.when == bstack1l1l1ll_opy_ (u"ࠪࡧࡦࡲ࡬ࠨಬ"):
      bstack11lllll1ll_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1lll1lll1l_opy_:
          name = str(rep.nodeid)
          bstack1l1l1lll1l_opy_ = bstack111ll1l1_opy_(bstack1l1l1ll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬಭ"), name, bstack1l1l1ll_opy_ (u"ࠬ࠭ಮ"), bstack1l1l1ll_opy_ (u"࠭ࠧಯ"), bstack1l1l1ll_opy_ (u"ࠧࠨರ"), bstack1l1l1ll_opy_ (u"ࠨࠩಱ"))
          threading.current_thread().bstack1l1ll1lll_opy_ = name
          for driver in bstack1lll1l1l1l_opy_:
            if bstack11lllll1ll_opy_ == driver.session_id:
              driver.execute_script(bstack1l1l1lll1l_opy_)
      except Exception as e:
        logger.debug(bstack1l1l1ll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩಲ").format(str(e)))
      try:
        bstack1lll11ll1_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack1l1l1ll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫಳ"):
          status = bstack1l1l1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ಴") if rep.outcome.lower() == bstack1l1l1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬವ") else bstack1l1l1ll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ಶ")
          reason = bstack1l1l1ll_opy_ (u"ࠧࠨಷ")
          if status == bstack1l1l1ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨಸ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack1l1l1ll_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧಹ") if status == bstack1l1l1ll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ಺") else bstack1l1l1ll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ಻")
          data = name + bstack1l1l1ll_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩ಼ࠧࠧ") if status == bstack1l1l1ll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ಽ") else name + bstack1l1l1ll_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠢࠢࠪಾ") + reason
          bstack1l1lll11ll_opy_ = bstack111ll1l1_opy_(bstack1l1l1ll_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪಿ"), bstack1l1l1ll_opy_ (u"ࠩࠪೀ"), bstack1l1l1ll_opy_ (u"ࠪࠫು"), bstack1l1l1ll_opy_ (u"ࠫࠬೂ"), level, data)
          for driver in bstack1lll1l1l1l_opy_:
            if bstack11lllll1ll_opy_ == driver.session_id:
              driver.execute_script(bstack1l1lll11ll_opy_)
      except Exception as e:
        logger.debug(bstack1l1l1ll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡦࡳࡳࡺࡥࡹࡶࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩೃ").format(str(e)))
  except Exception as e:
    logger.debug(bstack1l1l1ll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡶࡸࡦࡺࡥࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼࡿࠪೄ").format(str(e)))
  bstack11111l1l_opy_(item, call, rep)
def bstack1ll1111l11_opy_(driver, bstack111ll1lll_opy_, test=None):
  global bstack1l11lll1_opy_
  if test != None:
    bstack1l1l1lll11_opy_ = getattr(test, bstack1l1l1ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ೅"), None)
    bstack1l1llll1ll_opy_ = getattr(test, bstack1l1l1ll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ೆ"), None)
    PercySDK.screenshot(driver, bstack111ll1lll_opy_, bstack1l1l1lll11_opy_=bstack1l1l1lll11_opy_, bstack1l1llll1ll_opy_=bstack1l1llll1ll_opy_, bstack1l1l1l1111_opy_=bstack1l11lll1_opy_)
  else:
    PercySDK.screenshot(driver, bstack111ll1lll_opy_)
@measure(event_name=EVENTS.bstack1l11111l1_opy_, stage=STAGE.bstack1l1ll11l1_opy_, bstack111l1llll_opy_=bstack1llll111_opy_)
def bstack11ll111ll1_opy_(driver):
  if bstack1lll1llll1_opy_.bstack1l1111l1ll_opy_() is True or bstack1lll1llll1_opy_.capturing() is True:
    return
  bstack1lll1llll1_opy_.bstack1ll11lll1_opy_()
  while not bstack1lll1llll1_opy_.bstack1l1111l1ll_opy_():
    bstack1ll1111ll_opy_ = bstack1lll1llll1_opy_.bstack11l1ll1ll_opy_()
    bstack1ll1111l11_opy_(driver, bstack1ll1111ll_opy_)
  bstack1lll1llll1_opy_.bstack11lllllll1_opy_()
def bstack11l11ll11l_opy_(sequence, driver_command, response = None, bstack11ll11llll_opy_ = None, args = None):
    try:
      if sequence != bstack1l1l1ll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩೇ"):
        return
      if percy.bstack111l1111l_opy_() == bstack1l1l1ll_opy_ (u"ࠥࡪࡦࡲࡳࡦࠤೈ"):
        return
      bstack1ll1111ll_opy_ = bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ೉"), None)
      for command in bstack11l11l11_opy_:
        if command == driver_command:
          with bstack1l1l111l1_opy_:
            bstack11l11lll1l_opy_ = bstack1lll1l1l1l_opy_.copy()
          for driver in bstack11l11lll1l_opy_:
            bstack11ll111ll1_opy_(driver)
      bstack1ll11ll11l_opy_ = percy.bstack11lll1l1_opy_()
      if driver_command in bstack11ll1l11l1_opy_[bstack1ll11ll11l_opy_]:
        bstack1lll1llll1_opy_.bstack1llll1111_opy_(bstack1ll1111ll_opy_, driver_command)
    except Exception as e:
      pass
def bstack1ll1111l1l_opy_(framework_name):
  if bstack1l1l1111l1_opy_.get_property(bstack1l1l1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩೊ")):
      return
  bstack1l1l1111l1_opy_.bstack1l1ll11111_opy_(bstack1l1l1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪೋ"), True)
  global bstack11ll1111_opy_
  global bstack1l1ll1llll_opy_
  global bstack11llll1l1_opy_
  bstack11ll1111_opy_ = framework_name
  logger.info(bstack111lll1l_opy_.format(bstack11ll1111_opy_.split(bstack1l1l1ll_opy_ (u"ࠧ࠮ࠩೌ"))[0]))
  bstack11ll11lll1_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1lllll111l_opy_:
      Service.start = bstack1ll111l11_opy_
      Service.stop = bstack1l1111111_opy_
      webdriver.Remote.get = bstack1ll11111_opy_
      WebDriver.quit = bstack1lll11lll1_opy_
      webdriver.Remote.__init__ = bstack1l1l1l1l_opy_
    if not bstack1lllll111l_opy_:
        webdriver.Remote.__init__ = bstack1lllll1ll_opy_
    WebDriver.getAccessibilityResults = getAccessibilityResults
    WebDriver.get_accessibility_results = getAccessibilityResults
    WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
    WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
    WebDriver.performScan = perform_scan
    WebDriver.perform_scan = perform_scan
    WebDriver.execute = bstack1l111ll111_opy_
    bstack1l1ll1llll_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack1lllll111l_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack11l1l1l111_opy_
  except Exception as e:
    pass
  bstack11lll111ll_opy_()
  if not bstack1l1ll1llll_opy_:
    bstack1ll111lll_opy_(bstack1l1l1ll_opy_ (u"ࠣࡒࡤࡧࡰࡧࡧࡦࡵࠣࡲࡴࡺࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦ್ࠥ"), bstack1l11111l1l_opy_)
  if bstack1lll111l1l_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      if hasattr(RemoteConnection, bstack1l1l1ll_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪ೎")) and callable(getattr(RemoteConnection, bstack1l1l1ll_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫ೏"))):
        RemoteConnection._get_proxy_url = bstack11l1ll11l_opy_
      else:
        from selenium.webdriver.remote.client_config import ClientConfig
        ClientConfig.get_proxy_url = bstack11l1ll11l_opy_
    except Exception as e:
      logger.error(bstack11lll11lll_opy_.format(str(e)))
  if bstack11ll11111l_opy_():
    bstack11ll1ll1ll_opy_(CONFIG, logger)
  if (bstack1l1l1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ೐") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if percy.bstack111l1111l_opy_() == bstack1l1l1ll_opy_ (u"ࠧࡺࡲࡶࡧࠥ೑"):
          bstack1l11lllll_opy_(bstack11l11ll11l_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack11l1ll11_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack11l1l1l1l_opy_
      except Exception as e:
        logger.warn(bstack1l1ll1ll_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack11ll1l1ll1_opy_
      except Exception as e:
        logger.debug(bstack1l11l11l1l_opy_ + str(e))
    except Exception as e:
      bstack1ll111lll_opy_(e, bstack1l1ll1ll_opy_)
    Output.start_test = bstack1ll1111111_opy_
    Output.end_test = bstack1l11llllll_opy_
    TestStatus.__init__ = bstack1ll11l1lll_opy_
    QueueItem.__init__ = bstack1l1l1l1lll_opy_
    pabot._create_items = bstack11ll1l11ll_opy_
    try:
      from pabot import __version__ as bstack1l1l1l11l1_opy_
      if version.parse(bstack1l1l1l11l1_opy_) >= version.parse(bstack1l1l1ll_opy_ (u"࠭࠴࠯࠴࠱࠴ࠬ೒")):
        pabot._run = bstack111l11ll1_opy_
      elif version.parse(bstack1l1l1l11l1_opy_) >= version.parse(bstack1l1l1ll_opy_ (u"ࠧ࠳࠰࠴࠹࠳࠶ࠧ೓")):
        pabot._run = bstack1l1lllll_opy_
      elif version.parse(bstack1l1l1l11l1_opy_) >= version.parse(bstack1l1l1ll_opy_ (u"ࠨ࠴࠱࠵࠸࠴࠰ࠨ೔")):
        pabot._run = bstack1l1ll11l11_opy_
      else:
        pabot._run = bstack1l1l11l11l_opy_
    except Exception as e:
      pabot._run = bstack1l1l11l11l_opy_
    pabot._create_command_for_execution = bstack11l1llllll_opy_
    pabot._report_results = bstack11ll1l1l11_opy_
  if bstack1l1l1ll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩೕ") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll111lll_opy_(e, bstack1l111ll11_opy_)
    Runner.run_hook = bstack1l1lllllll_opy_
    Step.run = bstack11ll1llll_opy_
  if bstack1l1l1ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪೖ") in str(framework_name).lower():
    if not bstack1lllll111l_opy_:
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack111lllll1_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack11l111llll_opy_
      Config.getoption = bstack1l1l1lll1_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack11lll1111_opy_
    except Exception as e:
      pass
def bstack11l1ll1111_opy_():
  global CONFIG
  if bstack1l1l1ll_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ೗") in CONFIG and int(CONFIG[bstack1l1l1ll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ೘")]) > 1:
    logger.warn(bstack111l1111_opy_)
def bstack11l11l1l1l_opy_(arg, bstack1l11l1l1l1_opy_, bstack1l11l1llll_opy_=None):
  global CONFIG
  global bstack1lll1l1ll_opy_
  global bstack1l111111l1_opy_
  global bstack1lllll111l_opy_
  global bstack1l1l1111l1_opy_
  bstack1l1lll1ll_opy_ = bstack1l1l1ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭೙")
  if bstack1l11l1l1l1_opy_ and isinstance(bstack1l11l1l1l1_opy_, str):
    bstack1l11l1l1l1_opy_ = eval(bstack1l11l1l1l1_opy_)
  CONFIG = bstack1l11l1l1l1_opy_[bstack1l1l1ll_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧ೚")]
  bstack1lll1l1ll_opy_ = bstack1l11l1l1l1_opy_[bstack1l1l1ll_opy_ (u"ࠨࡊࡘࡆࡤ࡛ࡒࡍࠩ೛")]
  bstack1l111111l1_opy_ = bstack1l11l1l1l1_opy_[bstack1l1l1ll_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ೜")]
  bstack1lllll111l_opy_ = bstack1l11l1l1l1_opy_[bstack1l1l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭ೝ")]
  bstack1l1l1111l1_opy_.bstack1l1ll11111_opy_(bstack1l1l1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬೞ"), bstack1lllll111l_opy_)
  os.environ[bstack1l1l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ೟")] = bstack1l1lll1ll_opy_
  os.environ[bstack1l1l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࠬೠ")] = json.dumps(CONFIG)
  os.environ[bstack1l1l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡈࡖࡄࡢ࡙ࡗࡒࠧೡ")] = bstack1lll1l1ll_opy_
  os.environ[bstack1l1l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩೢ")] = str(bstack1l111111l1_opy_)
  os.environ[bstack1l1l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡏ࡙ࡌࡏࡎࠨೣ")] = str(True)
  if bstack11ll1l1111_opy_(arg, [bstack1l1l1ll_opy_ (u"ࠪ࠱ࡳ࠭೤"), bstack1l1l1ll_opy_ (u"ࠫ࠲࠳࡮ࡶ࡯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ೥")]) != -1:
    os.environ[bstack1l1l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡇࡒࡂࡎࡏࡉࡑ࠭೦")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1lllll11_opy_)
    return
  bstack11llll1ll1_opy_()
  global bstack1ll1l1l1l1_opy_
  global bstack1l11lll1_opy_
  global bstack11l11lll11_opy_
  global bstack1l1l1ll1l1_opy_
  global bstack1ll1111l1_opy_
  global bstack11llll1l1_opy_
  global bstack1lll11l11_opy_
  arg.append(bstack1l1l1ll_opy_ (u"ࠨ࠭ࡘࠤ೧"))
  arg.append(bstack1l1l1ll_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫࠺ࡎࡱࡧࡹࡱ࡫ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡ࡫ࡰࡴࡴࡸࡴࡦࡦ࠽ࡴࡾࡺࡥࡴࡶ࠱ࡔࡾࡺࡥࡴࡶ࡚ࡥࡷࡴࡩ࡯ࡩࠥ೨"))
  arg.append(bstack1l1l1ll_opy_ (u"ࠣ࠯࡚ࠦ೩"))
  arg.append(bstack1l1l1ll_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡦ࠼ࡗ࡬ࡪࠦࡨࡰࡱ࡮࡭ࡲࡶ࡬ࠣ೪"))
  global bstack1lllll1lll_opy_
  global bstack1l1ll1l1l_opy_
  global bstack1111111ll_opy_
  global bstack1l111lll1_opy_
  global bstack11111l111_opy_
  global bstack1ll11ll111_opy_
  global bstack1llll1ll_opy_
  global bstack111l1l11l_opy_
  global bstack1ll11l11l_opy_
  global bstack1llllll1l1_opy_
  global bstack1lll111111_opy_
  global bstack11ll1111l_opy_
  global bstack11111l1l_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1lllll1lll_opy_ = webdriver.Remote.__init__
    bstack1l1ll1l1l_opy_ = WebDriver.quit
    bstack111l1l11l_opy_ = WebDriver.close
    bstack1ll11l11l_opy_ = WebDriver.get
    bstack1111111ll_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1l11l1ll1_opy_(CONFIG) and bstack1ll1lll11l_opy_():
    if bstack1l111111l_opy_() < version.parse(bstack1111l1l11_opy_):
      logger.error(bstack1l1ll1ll1_opy_.format(bstack1l111111l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack1l1l1ll_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫ೫")) and callable(getattr(RemoteConnection, bstack1l1l1ll_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬ೬"))):
          bstack1llllll1l1_opy_ = RemoteConnection._get_proxy_url
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          bstack1llllll1l1_opy_ = ClientConfig.get_proxy_url
      except Exception as e:
        logger.error(bstack11lll11lll_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1lll111111_opy_ = Config.getoption
    from _pytest import runner
    bstack11ll1111l_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack1l1l1111ll_opy_)
  try:
    from pytest_bdd import reporting
    bstack11111l1l_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack1l1l1ll_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡴࠦࡲࡶࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࡸ࠭೭"))
  bstack11l11lll11_opy_ = CONFIG.get(bstack1l1l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ೮"), {}).get(bstack1l1l1ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ೯"))
  bstack1lll11l11_opy_ = True
  if cli.is_enabled(CONFIG):
    if cli.bstack11ll1lll1l_opy_():
      bstack1111lll11_opy_.invoke(bstack11ll1111ll_opy_.CONNECT, bstack11l111lll_opy_())
    platform_index = int(os.environ.get(bstack1l1l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ೰"), bstack1l1l1ll_opy_ (u"ࠩ࠳ࠫೱ")))
  else:
    bstack1ll1111l1l_opy_(bstack1l1111ll_opy_)
  os.environ[bstack1l1l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫೲ")] = CONFIG[bstack1l1l1ll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ೳ")]
  os.environ[bstack1l1l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨ೴")] = CONFIG[bstack1l1l1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ೵")]
  os.environ[bstack1l1l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪ೶")] = bstack1lllll111l_opy_.__str__()
  from _pytest.config import main as bstack111l1lll_opy_
  bstack1llll111l_opy_ = []
  try:
    exit_code = bstack111l1lll_opy_(arg)
    if cli.is_enabled(CONFIG):
      cli.bstack11lllll1l_opy_()
    if bstack1l1l1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬ೷") in multiprocessing.current_process().__dict__.keys():
      for bstack1l111111_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1llll111l_opy_.append(bstack1l111111_opy_)
    try:
      bstack1l11l11l1_opy_ = (bstack1llll111l_opy_, int(exit_code))
      bstack1l11l1llll_opy_.append(bstack1l11l11l1_opy_)
    except:
      bstack1l11l1llll_opy_.append((bstack1llll111l_opy_, exit_code))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack1llll111l_opy_.append({bstack1l1l1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ೸"): bstack1l1l1ll_opy_ (u"ࠪࡔࡷࡵࡣࡦࡵࡶࠤࠬ೹") + os.environ.get(bstack1l1l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ೺")), bstack1l1l1ll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ೻"): traceback.format_exc(), bstack1l1l1ll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ೼"): int(os.environ.get(bstack1l1l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ೽")))})
    bstack1l11l1llll_opy_.append((bstack1llll111l_opy_, 1))
def mod_behave_main(args, retries):
  try:
    from behave.configuration import Configuration
    from behave.__main__ import run_behave
    from browserstack_sdk.bstack_behave_runner import BehaveRunner
    config = Configuration(args)
    config.update_userdata({bstack1l1l1ll_opy_ (u"ࠣࡴࡨࡸࡷ࡯ࡥࡴࠤ೾"): str(retries)})
    return run_behave(config, runner_class=BehaveRunner)
  except Exception as e:
    bstack1ll11l1l1_opy_ = e.__class__.__name__
    print(bstack1l1l1ll_opy_ (u"ࠤࠨࡷ࠿ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡢࡦࡪࡤࡺࡪࠦࡴࡦࡵࡷࠤࠪࡹࠢ೿") % (bstack1ll11l1l1_opy_, e))
    return 1
def bstack11l1l1ll_opy_(arg):
  global bstack11ll1l1l1_opy_
  bstack1ll1111l1l_opy_(bstack1l111l111_opy_)
  os.environ[bstack1l1l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫഀ")] = str(bstack1l111111l1_opy_)
  retries = bstack1l1l1llll1_opy_.bstack1l11l111_opy_(CONFIG)
  status_code = 0
  if bstack1l1l1llll1_opy_.bstack11111llll_opy_(CONFIG):
    status_code = mod_behave_main(arg, retries)
  else:
    from behave.__main__ import main as bstack111l11l1_opy_
    status_code = bstack111l11l1_opy_(arg)
  if status_code != 0:
    bstack11ll1l1l1_opy_ = status_code
def bstack11ll11ll1_opy_():
  logger.info(bstack1l11ll1l1l_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1l1l1ll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪഁ"), help=bstack1l1l1ll_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡣࡰࡰࡩ࡭࡬࠭ം"))
  parser.add_argument(bstack1l1l1ll_opy_ (u"࠭࠭ࡶࠩഃ"), bstack1l1l1ll_opy_ (u"ࠧ࠮࠯ࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫഄ"), help=bstack1l1l1ll_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠧഅ"))
  parser.add_argument(bstack1l1l1ll_opy_ (u"ࠩ࠰࡯ࠬആ"), bstack1l1l1ll_opy_ (u"ࠪ࠱࠲ࡱࡥࡺࠩഇ"), help=bstack1l1l1ll_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡣࡦࡧࡪࡹࡳࠡ࡭ࡨࡽࠬഈ"))
  parser.add_argument(bstack1l1l1ll_opy_ (u"ࠬ࠳ࡦࠨഉ"), bstack1l1l1ll_opy_ (u"࠭࠭࠮ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫഊ"), help=bstack1l1l1ll_opy_ (u"࡚ࠧࡱࡸࡶࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ഋ"))
  bstack1ll111111_opy_ = parser.parse_args()
  try:
    bstack1lll1l1111_opy_ = bstack1l1l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡨࡧࡱࡩࡷ࡯ࡣ࠯ࡻࡰࡰ࠳ࡹࡡ࡮ࡲ࡯ࡩࠬഌ")
    if bstack1ll111111_opy_.framework and bstack1ll111111_opy_.framework not in (bstack1l1l1ll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ഍"), bstack1l1l1ll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫഎ")):
      bstack1lll1l1111_opy_ = bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠴ࡹ࡮࡮࠱ࡷࡦࡳࡰ࡭ࡧࠪഏ")
    bstack1llll1l111_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1lll1l1111_opy_)
    bstack1l1llllll1_opy_ = open(bstack1llll1l111_opy_, bstack1l1l1ll_opy_ (u"ࠬࡸࠧഐ"))
    bstack1llll1l1l1_opy_ = bstack1l1llllll1_opy_.read()
    bstack1l1llllll1_opy_.close()
    if bstack1ll111111_opy_.username:
      bstack1llll1l1l1_opy_ = bstack1llll1l1l1_opy_.replace(bstack1l1l1ll_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭഑"), bstack1ll111111_opy_.username)
    if bstack1ll111111_opy_.key:
      bstack1llll1l1l1_opy_ = bstack1llll1l1l1_opy_.replace(bstack1l1l1ll_opy_ (u"࡚ࠧࡑࡘࡖࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩഒ"), bstack1ll111111_opy_.key)
    if bstack1ll111111_opy_.framework:
      bstack1llll1l1l1_opy_ = bstack1llll1l1l1_opy_.replace(bstack1l1l1ll_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩഓ"), bstack1ll111111_opy_.framework)
    file_name = bstack1l1l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬഔ")
    file_path = os.path.abspath(file_name)
    bstack11ll11ll_opy_ = open(file_path, bstack1l1l1ll_opy_ (u"ࠪࡻࠬക"))
    bstack11ll11ll_opy_.write(bstack1llll1l1l1_opy_)
    bstack11ll11ll_opy_.close()
    logger.info(bstack1llllll11_opy_)
    try:
      os.environ[bstack1l1l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ഖ")] = bstack1ll111111_opy_.framework if bstack1ll111111_opy_.framework != None else bstack1l1l1ll_opy_ (u"ࠧࠨഗ")
      config = yaml.safe_load(bstack1llll1l1l1_opy_)
      config[bstack1l1l1ll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ഘ")] = bstack1l1l1ll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡴࡧࡷࡹࡵ࠭ങ")
      bstack11lll1llll_opy_(bstack11l1ll111l_opy_, config)
    except Exception as e:
      logger.debug(bstack1ll1lll11_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1l1ll11l_opy_.format(str(e)))
def bstack11lll1llll_opy_(bstack1l1l1ll1_opy_, config, bstack11l1ll1l1_opy_={}):
  global bstack1lllll111l_opy_
  global bstack1l1l1l11l_opy_
  global bstack1l1l1111l1_opy_
  if not config:
    return
  bstack11llll11l_opy_ = bstack11l1111l1_opy_ if not bstack1lllll111l_opy_ else (
    bstack1ll11ll1l1_opy_ if bstack1l1l1ll_opy_ (u"ࠨࡣࡳࡴࠬച") in config else (
        bstack1llll11ll_opy_ if config.get(bstack1l1l1ll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ഛ")) else bstack1l1llll11_opy_
    )
)
  bstack11l1llll11_opy_ = False
  bstack1ll1l1l1l_opy_ = False
  if bstack1lllll111l_opy_ is True:
      if bstack1l1l1ll_opy_ (u"ࠪࡥࡵࡶࠧജ") in config:
          bstack11l1llll11_opy_ = True
      else:
          bstack1ll1l1l1l_opy_ = True
  bstack1lll1l1lll_opy_ = bstack111lllll1l_opy_.bstack1l1l111ll1_opy_(config, bstack1l1l1l11l_opy_)
  bstack1lll1ll1ll_opy_ = bstack1ll1l111l1_opy_()
  data = {
    bstack1l1l1ll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ഝ"): config[bstack1l1l1ll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧഞ")],
    bstack1l1l1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩട"): config[bstack1l1l1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪഠ")],
    bstack1l1l1ll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬഡ"): bstack1l1l1ll1_opy_,
    bstack1l1l1ll_opy_ (u"ࠩࡧࡩࡹ࡫ࡣࡵࡧࡧࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ഢ"): os.environ.get(bstack1l1l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬണ"), bstack1l1l1l11l_opy_),
    bstack1l1l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ത"): bstack11lll1l111_opy_,
    bstack1l1l1ll_opy_ (u"ࠬࡵࡰࡵ࡫ࡰࡥࡱࡥࡨࡶࡤࡢࡹࡷࡲࠧഥ"): bstack11llllll11_opy_(),
    bstack1l1l1ll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩദ"): {
      bstack1l1l1ll_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬധ"): str(config[bstack1l1l1ll_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨന")]) if bstack1l1l1ll_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩഩ") in config else bstack1l1l1ll_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦപ"),
      bstack1l1l1ll_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ഫ"): sys.version,
      bstack1l1l1ll_opy_ (u"ࠬࡸࡥࡧࡧࡵࡶࡪࡸࠧബ"): bstack1l1llll111_opy_(os.environ.get(bstack1l1l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨഭ"), bstack1l1l1l11l_opy_)),
      bstack1l1l1ll_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩമ"): bstack1l1l1ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨയ"),
      bstack1l1l1ll_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪര"): bstack11llll11l_opy_,
      bstack1l1l1ll_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨറ"): bstack1lll1l1lll_opy_,
      bstack1l1l1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡪࡸࡦࡤࡻࡵࡪࡦࠪല"): os.environ[bstack1l1l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪള")],
      bstack1l1l1ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩഴ"): os.environ.get(bstack1l1l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩവ"), bstack1l1l1l11l_opy_),
      bstack1l1l1ll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫശ"): bstack1l1ll1l1ll_opy_(os.environ.get(bstack1l1l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫഷ"), bstack1l1l1l11l_opy_)),
      bstack1l1l1ll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩസ"): bstack1lll1ll1ll_opy_.get(bstack1l1l1ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩഹ")),
      bstack1l1l1ll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫഺ"): bstack1lll1ll1ll_opy_.get(bstack1l1l1ll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴ഻ࠧ")),
      bstack1l1l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧ഼ࠪ"): config[bstack1l1l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫഽ")] if config[bstack1l1l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬാ")] else bstack1l1l1ll_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦി"),
      bstack1l1l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ീ"): str(config[bstack1l1l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧു")]) if bstack1l1l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨൂ") in config else bstack1l1l1ll_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣൃ"),
      bstack1l1l1ll_opy_ (u"ࠨࡱࡶࠫൄ"): sys.platform,
      bstack1l1l1ll_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫ൅"): socket.gethostname(),
      bstack1l1l1ll_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࠬെ"): bstack1l1l1111l1_opy_.get_property(bstack1l1l1ll_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭േ"))
    }
  }
  if not bstack1l1l1111l1_opy_.get_property(bstack1l1l1ll_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬൈ")) is None:
    data[bstack1l1l1ll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩ൉")][bstack1l1l1ll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡏࡨࡸࡦࡪࡡࡵࡣࠪൊ")] = {
      bstack1l1l1ll_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨോ"): bstack1l1l1ll_opy_ (u"ࠩࡸࡷࡪࡸ࡟࡬࡫࡯ࡰࡪࡪࠧൌ"),
      bstack1l1l1ll_opy_ (u"ࠪࡷ࡮࡭࡮ࡢ࡮്ࠪ"): bstack1l1l1111l1_opy_.get_property(bstack1l1l1ll_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡘ࡯ࡧ࡯ࡣ࡯ࠫൎ")),
      bstack1l1l1ll_opy_ (u"ࠬࡹࡩࡨࡰࡤࡰࡓࡻ࡭ࡣࡧࡵࠫ൏"): bstack1l1l1111l1_opy_.get_property(bstack1l1l1ll_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡎࡰࠩ൐"))
    }
  if bstack1l1l1ll1_opy_ == bstack1lll1ll11_opy_:
    data[bstack1l1l1ll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪ൑")][bstack1l1l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡃࡰࡰࡩ࡭࡬࠭൒")] = bstack1ll11ll1_opy_(config)
    data[bstack1l1l1ll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬ൓")][bstack1l1l1ll_opy_ (u"ࠪ࡭ࡸࡖࡥࡳࡥࡼࡅࡺࡺ࡯ࡆࡰࡤࡦࡱ࡫ࡤࠨൔ")] = percy.bstack1l1lll11_opy_
    data[bstack1l1l1ll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧൕ")][bstack1l1l1ll_opy_ (u"ࠬࡶࡥࡳࡥࡼࡆࡺ࡯࡬ࡥࡋࡧࠫൖ")] = percy.percy_build_id
  if not bstack1l1l1llll1_opy_.bstack1l1lllll1l_opy_(CONFIG):
    data[bstack1l1l1ll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩൗ")][bstack1l1l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠫ൘")] = bstack1l1l1llll1_opy_.bstack1l1lllll1l_opy_(CONFIG)
  bstack1ll111l1_opy_ = bstack1l11111l11_opy_.bstack11l1lllll1_opy_(CONFIG, logger)
  bstack11l1l111l1_opy_ = bstack1l1l1llll1_opy_.bstack11l1lllll1_opy_(config=CONFIG)
  if bstack1ll111l1_opy_ is not None and bstack11l1l111l1_opy_ is not None and bstack11l1l111l1_opy_.bstack111111lll_opy_():
    data[bstack1l1l1ll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫ൙")][bstack11l1l111l1_opy_.bstack11llll1l_opy_()] = bstack1ll111l1_opy_.bstack1l11l11lll_opy_()
  update(data[bstack1l1l1ll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬ൚")], bstack11l1ll1l1_opy_)
  try:
    response = bstack1llll11ll1_opy_(bstack1l1l1ll_opy_ (u"ࠪࡔࡔ࡙ࡔࠨ൛"), bstack1llll1111l_opy_(bstack1l1l1ll111_opy_), data, {
      bstack1l1l1ll_opy_ (u"ࠫࡦࡻࡴࡩࠩ൜"): (config[bstack1l1l1ll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ൝")], config[bstack1l1l1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ൞")])
    })
    if response:
      logger.debug(bstack1lll1l11l1_opy_.format(bstack1l1l1ll1_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1l1l11l11_opy_.format(str(e)))
def bstack1l1llll111_opy_(framework):
  return bstack1l1l1ll_opy_ (u"ࠢࡼࡿ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࡽࢀࠦൟ").format(str(framework), __version__) if framework else bstack1l1l1ll_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࡻࡾࠤൠ").format(
    __version__)
def bstack11llll1ll1_opy_():
  global CONFIG
  global bstack1l1ll1l1l1_opy_
  if bool(CONFIG):
    return
  try:
    bstack11l1l1ll11_opy_()
    logger.debug(bstack1l1l11ll_opy_.format(str(CONFIG)))
    bstack1l1ll1l1l1_opy_ = bstack1l1l11lll1_opy_.configure_logger(CONFIG, bstack1l1ll1l1l1_opy_)
    bstack11ll11lll1_opy_()
  except Exception as e:
    logger.error(bstack1l1l1ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࡷࡳ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࠨൡ") + str(e))
    sys.exit(1)
  sys.excepthook = bstack111ll11l1_opy_
  atexit.register(bstack1ll11lll11_opy_)
  signal.signal(signal.SIGINT, bstack111ll1111_opy_)
  signal.signal(signal.SIGTERM, bstack111ll1111_opy_)
def bstack111ll11l1_opy_(exctype, value, traceback):
  global bstack1lll1l1l1l_opy_
  try:
    for driver in bstack1lll1l1l1l_opy_:
      bstack11ll111111_opy_(driver, bstack1l1l1ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪൢ"), bstack1l1l1ll_opy_ (u"ࠦࡘ࡫ࡳࡴ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢൣ") + str(value))
  except Exception:
    pass
  logger.info(bstack1ll1lll111_opy_)
  bstack11l111ll_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack11l111ll_opy_(message=bstack1l1l1ll_opy_ (u"ࠬ࠭൤"), bstack1l1111lll_opy_ = False):
  global CONFIG
  bstack1l111l11l1_opy_ = bstack1l1l1ll_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠨ൥") if bstack1l1111lll_opy_ else bstack1l1l1ll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭൦")
  try:
    if message:
      bstack11l1ll1l1_opy_ = {
        bstack1l111l11l1_opy_ : str(message)
      }
      bstack11lll1llll_opy_(bstack1lll1ll11_opy_, CONFIG, bstack11l1ll1l1_opy_)
    else:
      bstack11lll1llll_opy_(bstack1lll1ll11_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack11l11l111l_opy_.format(str(e)))
def bstack11111lll1_opy_(bstack1l1l1ll11l_opy_, size):
  bstack1l11ll1ll_opy_ = []
  while len(bstack1l1l1ll11l_opy_) > size:
    bstack1lll1111l_opy_ = bstack1l1l1ll11l_opy_[:size]
    bstack1l11ll1ll_opy_.append(bstack1lll1111l_opy_)
    bstack1l1l1ll11l_opy_ = bstack1l1l1ll11l_opy_[size:]
  bstack1l11ll1ll_opy_.append(bstack1l1l1ll11l_opy_)
  return bstack1l11ll1ll_opy_
def bstack1llll1ll1_opy_(args):
  if bstack1l1l1ll_opy_ (u"ࠨ࠯ࡰࠫ൧") in args and bstack1l1l1ll_opy_ (u"ࠩࡳࡨࡧ࠭൨") in args:
    return True
  return False
@measure(event_name=EVENTS.bstack1l1111l1_opy_, stage=STAGE.bstack11llll11l1_opy_)
def run_on_browserstack(bstack11lll11l1l_opy_=None, bstack1l11l1llll_opy_=None, bstack1ll1l11l11_opy_=False):
  global CONFIG
  global bstack1lll1l1ll_opy_
  global bstack1l111111l1_opy_
  global bstack1l1l1l11l_opy_
  global bstack1l1l1111l1_opy_
  bstack1l1lll1ll_opy_ = bstack1l1l1ll_opy_ (u"ࠪࠫ൩")
  bstack1l1lll11l1_opy_(bstack1ll1ll1l11_opy_, logger)
  if bstack11lll11l1l_opy_ and isinstance(bstack11lll11l1l_opy_, str):
    bstack11lll11l1l_opy_ = eval(bstack11lll11l1l_opy_)
  if bstack11lll11l1l_opy_:
    CONFIG = bstack11lll11l1l_opy_[bstack1l1l1ll_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫ൪")]
    bstack1lll1l1ll_opy_ = bstack11lll11l1l_opy_[bstack1l1l1ll_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭൫")]
    bstack1l111111l1_opy_ = bstack11lll11l1l_opy_[bstack1l1l1ll_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ൬")]
    bstack1l1l1111l1_opy_.bstack1l1ll11111_opy_(bstack1l1l1ll_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ൭"), bstack1l111111l1_opy_)
    bstack1l1lll1ll_opy_ = bstack1l1l1ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ൮")
  bstack1l1l1111l1_opy_.bstack1l1ll11111_opy_(bstack1l1l1ll_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫ൯"), uuid4().__str__())
  logger.info(bstack1l1l1ll_opy_ (u"ࠪࡗࡉࡑࠠࡳࡷࡱࠤࡸࡺࡡࡳࡶࡨࡨࠥࡽࡩࡵࡪࠣ࡭ࡩࡀࠠࠨ൰") + bstack1l1l1111l1_opy_.get_property(bstack1l1l1ll_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭൱")));
  logger.debug(bstack1l1l1ll_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪ࠽ࠨ൲") + bstack1l1l1111l1_opy_.get_property(bstack1l1l1ll_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨ൳")))
  if not bstack1ll1l11l11_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1lllll11_opy_)
      return
    if sys.argv[1] == bstack1l1l1ll_opy_ (u"ࠧ࠮࠯ࡹࡩࡷࡹࡩࡰࡰࠪ൴") or sys.argv[1] == bstack1l1l1ll_opy_ (u"ࠨ࠯ࡹࠫ൵"):
      logger.info(bstack1l1l1ll_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡒࡼࡸ࡭ࡵ࡮ࠡࡕࡇࡏࠥࡼࡻࡾࠩ൶").format(__version__))
      return
    if sys.argv[1] == bstack1l1l1ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ൷"):
      bstack11ll11ll1_opy_()
      return
  args = sys.argv
  bstack11llll1ll1_opy_()
  global bstack1ll1l1l1l1_opy_
  global bstack1lll11ll11_opy_
  global bstack1lll11l11_opy_
  global bstack1lllll11l_opy_
  global bstack1l11lll1_opy_
  global bstack11l11lll11_opy_
  global bstack1l1l1ll1l1_opy_
  global bstack1l1l11l1l1_opy_
  global bstack1ll1111l1_opy_
  global bstack11llll1l1_opy_
  global bstack1llll1l1_opy_
  bstack1lll11ll11_opy_ = len(CONFIG.get(bstack1l1l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ൸"), []))
  if not bstack1l1lll1ll_opy_:
    if args[1] == bstack1l1l1ll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ൹") or args[1] == bstack1l1l1ll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧൺ"):
      bstack1l1lll1ll_opy_ = bstack1l1l1ll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧൻ")
      args = args[2:]
    elif args[1] == bstack1l1l1ll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧർ"):
      bstack1l1lll1ll_opy_ = bstack1l1l1ll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨൽ")
      args = args[2:]
    elif args[1] == bstack1l1l1ll_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩൾ"):
      bstack1l1lll1ll_opy_ = bstack1l1l1ll_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪൿ")
      args = args[2:]
    elif args[1] == bstack1l1l1ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭඀"):
      bstack1l1lll1ll_opy_ = bstack1l1l1ll_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧඁ")
      args = args[2:]
    elif args[1] == bstack1l1l1ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧං"):
      bstack1l1lll1ll_opy_ = bstack1l1l1ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨඃ")
      args = args[2:]
    elif args[1] == bstack1l1l1ll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ඄"):
      bstack1l1lll1ll_opy_ = bstack1l1l1ll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪඅ")
      args = args[2:]
    else:
      if not bstack1l1l1ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧආ") in CONFIG or str(CONFIG[bstack1l1l1ll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨඇ")]).lower() in [bstack1l1l1ll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ඈ"), bstack1l1l1ll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨඉ")]:
        bstack1l1lll1ll_opy_ = bstack1l1l1ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨඊ")
        args = args[1:]
      elif str(CONFIG[bstack1l1l1ll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬඋ")]).lower() == bstack1l1l1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩඌ"):
        bstack1l1lll1ll_opy_ = bstack1l1l1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪඍ")
        args = args[1:]
      elif str(CONFIG[bstack1l1l1ll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨඎ")]).lower() == bstack1l1l1ll_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬඏ"):
        bstack1l1lll1ll_opy_ = bstack1l1l1ll_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ඐ")
        args = args[1:]
      elif str(CONFIG[bstack1l1l1ll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫඑ")]).lower() == bstack1l1l1ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩඒ"):
        bstack1l1lll1ll_opy_ = bstack1l1l1ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪඓ")
        args = args[1:]
      elif str(CONFIG[bstack1l1l1ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧඔ")]).lower() == bstack1l1l1ll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬඕ"):
        bstack1l1lll1ll_opy_ = bstack1l1l1ll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ඖ")
        args = args[1:]
      else:
        os.environ[bstack1l1l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩ඗")] = bstack1l1lll1ll_opy_
        bstack1l1l11l111_opy_(bstack1lll1lll_opy_)
  os.environ[bstack1l1l1ll_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩ඘")] = bstack1l1lll1ll_opy_
  bstack1l1l1l11l_opy_ = bstack1l1lll1ll_opy_
  if cli.is_enabled(CONFIG):
    try:
      bstack111lll1l1_opy_ = bstack1llll1lll_opy_[bstack1l1l1ll_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕ࠯ࡅࡈࡉ࠭඙")] if bstack1l1lll1ll_opy_ == bstack1l1l1ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪක") and bstack111ll1ll1_opy_() else bstack1l1lll1ll_opy_
      bstack1111lll11_opy_.invoke(bstack11ll1111ll_opy_.bstack1ll111l1ll_opy_, bstack11llllllll_opy_(
        sdk_version=__version__,
        path_config=bstack1l11l111l1_opy_(),
        path_project=os.getcwd(),
        test_framework=bstack111lll1l1_opy_,
        frameworks=[bstack111lll1l1_opy_],
        framework_versions={
          bstack111lll1l1_opy_: bstack1l1ll1l1ll_opy_(bstack1l1l1ll_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪඛ") if bstack1l1lll1ll_opy_ in [bstack1l1l1ll_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫග"), bstack1l1l1ll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬඝ"), bstack1l1l1ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨඞ")] else bstack1l1lll1ll_opy_)
        },
        bs_config=CONFIG
      ))
      if cli.config.get(bstack1l1l1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠥඟ"), None):
        CONFIG[bstack1l1l1ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠦච")] = cli.config.get(bstack1l1l1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧඡ"), None)
    except Exception as e:
      bstack1111lll11_opy_.invoke(bstack11ll1111ll_opy_.bstack1ll111ll_opy_, e.__traceback__, 1)
    if bstack1l111111l1_opy_:
      CONFIG[bstack1l1l1ll_opy_ (u"ࠦࡦࡶࡰࠣජ")] = cli.config[bstack1l1l1ll_opy_ (u"ࠧࡧࡰࡱࠤඣ")]
      logger.info(bstack11l1111l_opy_.format(CONFIG[bstack1l1l1ll_opy_ (u"࠭ࡡࡱࡲࠪඤ")]))
  else:
    bstack1111lll11_opy_.clear()
  global bstack11l11lll1_opy_
  global bstack1l1l1l1l1_opy_
  if bstack11lll11l1l_opy_:
    try:
      bstack1lll111ll1_opy_ = datetime.datetime.now()
      os.environ[bstack1l1l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩඥ")] = bstack1l1lll1ll_opy_
      bstack11lll1llll_opy_(bstack1l1l1ll1l_opy_, CONFIG)
      cli.bstack1ll1ll11ll_opy_(bstack1l1l1ll_opy_ (u"ࠣࡪࡷࡸࡵࡀࡳࡥ࡭ࡢࡸࡪࡹࡴࡠࡣࡷࡸࡪࡳࡰࡵࡧࡧࠦඦ"), datetime.datetime.now() - bstack1lll111ll1_opy_)
    except Exception as e:
      logger.debug(bstack11ll1ll1_opy_.format(str(e)))
  global bstack1lllll1lll_opy_
  global bstack1l1ll1l1l_opy_
  global bstack1ll1l1l11l_opy_
  global bstack11l11111_opy_
  global bstack1l1111llll_opy_
  global bstack11l1ll1l_opy_
  global bstack1l111lll1_opy_
  global bstack11111l111_opy_
  global bstack1lll11lll_opy_
  global bstack1ll11ll111_opy_
  global bstack1llll1ll_opy_
  global bstack111l1l11l_opy_
  global bstack1ll1lll1_opy_
  global bstack1ll111llll_opy_
  global bstack1ll11l11l_opy_
  global bstack1llllll1l1_opy_
  global bstack1lll111111_opy_
  global bstack11ll1111l_opy_
  global bstack1111l11l_opy_
  global bstack11111l1l_opy_
  global bstack1111111ll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1lllll1lll_opy_ = webdriver.Remote.__init__
    bstack1l1ll1l1l_opy_ = WebDriver.quit
    bstack111l1l11l_opy_ = WebDriver.close
    bstack1ll11l11l_opy_ = WebDriver.get
    bstack1111111ll_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack11l11lll1_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack11ll1lll_opy_
    bstack1l1l1l1l1_opy_ = bstack11ll1lll_opy_()
  except Exception as e:
    pass
  try:
    global bstack11l11l1l1_opy_
    from QWeb.keywords import browser
    bstack11l11l1l1_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1l11l1ll1_opy_(CONFIG) and bstack1ll1lll11l_opy_():
    if bstack1l111111l_opy_() < version.parse(bstack1111l1l11_opy_):
      logger.error(bstack1l1ll1ll1_opy_.format(bstack1l111111l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack1l1l1ll_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪට")) and callable(getattr(RemoteConnection, bstack1l1l1ll_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫඨ"))):
          RemoteConnection._get_proxy_url = bstack11l1ll11l_opy_
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          ClientConfig.get_proxy_url = bstack11l1ll11l_opy_
      except Exception as e:
        logger.error(bstack11lll11lll_opy_.format(str(e)))
  if not CONFIG.get(bstack1l1l1ll_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭ඩ"), False) and not bstack11lll11l1l_opy_:
    logger.info(bstack1l11ll1l1_opy_)
  if not cli.is_enabled(CONFIG):
    if bstack1l1l1ll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩඪ") in CONFIG and str(CONFIG[bstack1l1l1ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪණ")]).lower() != bstack1l1l1ll_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ඬ"):
      bstack1l11lll111_opy_()
    elif bstack1l1lll1ll_opy_ != bstack1l1l1ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨත") or (bstack1l1lll1ll_opy_ == bstack1l1l1ll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩථ") and not bstack11lll11l1l_opy_):
      bstack11l11l11l1_opy_()
  if (bstack1l1lll1ll_opy_ in [bstack1l1l1ll_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩද"), bstack1l1l1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪධ"), bstack1l1l1ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭න")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack11l1ll11_opy_
        bstack11l1ll1l_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1l1ll1ll_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1l1111llll_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1l11l11l1l_opy_ + str(e))
    except Exception as e:
      bstack1ll111lll_opy_(e, bstack1l1ll1ll_opy_)
    if bstack1l1lll1ll_opy_ != bstack1l1l1ll_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧ඲"):
      bstack111l11lll_opy_()
    bstack1ll1l1l11l_opy_ = Output.start_test
    bstack11l11111_opy_ = Output.end_test
    bstack1l111lll1_opy_ = TestStatus.__init__
    bstack1lll11lll_opy_ = pabot._run
    bstack1ll11ll111_opy_ = QueueItem.__init__
    bstack1llll1ll_opy_ = pabot._create_command_for_execution
    bstack1111l11l_opy_ = pabot._report_results
  if bstack1l1lll1ll_opy_ == bstack1l1l1ll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧඳ"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll111lll_opy_(e, bstack1l111ll11_opy_)
    bstack1ll1lll1_opy_ = Runner.run_hook
    bstack1ll111llll_opy_ = Step.run
  if bstack1l1lll1ll_opy_ == bstack1l1l1ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨප"):
    try:
      from _pytest.config import Config
      bstack1lll111111_opy_ = Config.getoption
      from _pytest import runner
      bstack11ll1111l_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack1l1l1111ll_opy_)
    try:
      from pytest_bdd import reporting
      bstack11111l1l_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1l1l1ll_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡱࠣࡶࡺࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࡵࠪඵ"))
  try:
    framework_name = bstack1l1l1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩබ") if bstack1l1lll1ll_opy_ in [bstack1l1l1ll_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪභ"), bstack1l1l1ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫම"), bstack1l1l1ll_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧඹ")] else bstack1lll1l111l_opy_(bstack1l1lll1ll_opy_)
    bstack11ll11111_opy_ = {
      bstack1l1l1ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠨය"): bstack1l1l1ll_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪර") if bstack1l1lll1ll_opy_ == bstack1l1l1ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ඼") and bstack111ll1ll1_opy_() else framework_name,
      bstack1l1l1ll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧල"): bstack1l1ll1l1ll_opy_(framework_name),
      bstack1l1l1ll_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ඾"): __version__,
      bstack1l1l1ll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡷࡶࡩࡩ࠭඿"): bstack1l1lll1ll_opy_
    }
    if bstack1l1lll1ll_opy_ in bstack11l1l11ll_opy_ + bstack11l11l1ll1_opy_:
      if bstack1lll11l1ll_opy_.bstack11l11ll11_opy_(CONFIG):
        if bstack1l1l1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ව") in CONFIG:
          os.environ[bstack1l1l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨශ")] = os.getenv(bstack1l1l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩෂ"), json.dumps(CONFIG[bstack1l1l1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩස")]))
          CONFIG[bstack1l1l1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪහ")].pop(bstack1l1l1ll_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩළ"), None)
          CONFIG[bstack1l1l1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬෆ")].pop(bstack1l1l1ll_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫ෇"), None)
        bstack11ll11111_opy_[bstack1l1l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ෈")] = {
          bstack1l1l1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭෉"): bstack1l1l1ll_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ්ࠫ"),
          bstack1l1l1ll_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫ෋"): str(bstack1l111111l_opy_())
        }
    if bstack1l1lll1ll_opy_ not in [bstack1l1l1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ෌")] and not cli.is_running():
      bstack11l11l1l11_opy_, bstack1111l1lll_opy_ = bstack1llllll11l_opy_.launch(CONFIG, bstack11ll11111_opy_)
      if bstack1111l1lll_opy_.get(bstack1l1l1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ෍")) is not None and bstack1lll11l1ll_opy_.bstack11l1111111_opy_(CONFIG) is None:
        value = bstack1111l1lll_opy_[bstack1l1l1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭෎")].get(bstack1l1l1ll_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨා"))
        if value is not None:
            CONFIG[bstack1l1l1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨැ")] = value
        else:
          logger.debug(bstack1l1l1ll_opy_ (u"ࠤࡑࡳࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡪࡡࡵࡣࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠢෑ"))
  except Exception as e:
    logger.debug(bstack111lllllll_opy_.format(bstack1l1l1ll_opy_ (u"ࠪࡘࡪࡹࡴࡉࡷࡥࠫි"), str(e)))
  if bstack1l1lll1ll_opy_ == bstack1l1l1ll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫී"):
    bstack1lll11l11_opy_ = True
    if bstack11lll11l1l_opy_ and bstack1ll1l11l11_opy_:
      bstack11l11lll11_opy_ = CONFIG.get(bstack1l1l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩු"), {}).get(bstack1l1l1ll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ෕"))
      bstack1ll1111l1l_opy_(bstack11111111l_opy_)
    elif bstack11lll11l1l_opy_:
      bstack11l11lll11_opy_ = CONFIG.get(bstack1l1l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫූ"), {}).get(bstack1l1l1ll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ෗"))
      global bstack1lll1l1l1l_opy_
      try:
        if bstack1llll1ll1_opy_(bstack11lll11l1l_opy_[bstack1l1l1ll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬෘ")]) and multiprocessing.current_process().name == bstack1l1l1ll_opy_ (u"ࠪ࠴ࠬෙ"):
          bstack11lll11l1l_opy_[bstack1l1l1ll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧේ")].remove(bstack1l1l1ll_opy_ (u"ࠬ࠳࡭ࠨෛ"))
          bstack11lll11l1l_opy_[bstack1l1l1ll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩො")].remove(bstack1l1l1ll_opy_ (u"ࠧࡱࡦࡥࠫෝ"))
          bstack11lll11l1l_opy_[bstack1l1l1ll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫෞ")] = bstack11lll11l1l_opy_[bstack1l1l1ll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬෟ")][0]
          with open(bstack11lll11l1l_opy_[bstack1l1l1ll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭෠")], bstack1l1l1ll_opy_ (u"ࠫࡷ࠭෡")) as f:
            bstack11llll111l_opy_ = f.read()
          bstack1llll11l1l_opy_ = bstack1l1l1ll_opy_ (u"ࠧࠨࠢࡧࡴࡲࡱࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡸࡪ࡫ࠡ࡫ࡰࡴࡴࡸࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡨ࠿ࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥࠩࡽࢀ࠭ࡀࠦࡦࡳࡱࡰࠤࡵࡪࡢࠡ࡫ࡰࡴࡴࡸࡴࠡࡒࡧࡦࡀࠦ࡯ࡨࡡࡧࡦࠥࡃࠠࡑࡦࡥ࠲ࡩࡵ࡟ࡣࡴࡨࡥࡰࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡨࡪ࡬ࠠ࡮ࡱࡧࡣࡧࡸࡥࡢ࡭ࠫࡷࡪࡲࡦ࠭ࠢࡤࡶ࡬࠲ࠠࡵࡧࡰࡴࡴࡸࡡࡳࡻࠣࡁࠥ࠶ࠩ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡵࡴࡼ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡧࡲࡨࠢࡀࠤࡸࡺࡲࠩ࡫ࡱࡸ࠭ࡧࡲࡨࠫ࠮࠵࠵࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡫ࡸࡤࡧࡳࡸࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡣࡶࠤࡪࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡱࡣࡶࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡳ࡬ࡥࡤࡣࠪࡶࡩࡱ࡬ࠬࡢࡴࡪ࠰ࡹ࡫࡭ࡱࡱࡵࡥࡷࡿࠩࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡕࡪࡢ࠯ࡦࡲࡣࡧࠦ࠽ࠡ࡯ࡲࡨࡤࡨࡲࡦࡣ࡮ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡑࡦࡥ࠲ࡩࡵ࡟ࡣࡴࡨࡥࡰࠦ࠽ࠡ࡯ࡲࡨࡤࡨࡲࡦࡣ࡮ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡑࡦࡥࠬ࠮࠴ࡳࡦࡶࡢࡸࡷࡧࡣࡦࠪࠬࡠࡳࠨࠢࠣ෢").format(str(bstack11lll11l1l_opy_))
          bstack111111l1l_opy_ = bstack1llll11l1l_opy_ + bstack11llll111l_opy_
          bstack1l111lllll_opy_ = bstack11lll11l1l_opy_[bstack1l1l1ll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ෣")] + bstack1l1l1ll_opy_ (u"ࠧࡠࡤࡶࡸࡦࡩ࡫ࡠࡶࡨࡱࡵ࠴ࡰࡺࠩ෤")
          with open(bstack1l111lllll_opy_, bstack1l1l1ll_opy_ (u"ࠨࡹࠪ෥")):
            pass
          with open(bstack1l111lllll_opy_, bstack1l1l1ll_opy_ (u"ࠤࡺ࠯ࠧ෦")) as f:
            f.write(bstack111111l1l_opy_)
          import subprocess
          bstack1l1l1l1l1l_opy_ = subprocess.run([bstack1l1l1ll_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࠥ෧"), bstack1l111lllll_opy_])
          if os.path.exists(bstack1l111lllll_opy_):
            os.unlink(bstack1l111lllll_opy_)
          os._exit(bstack1l1l1l1l1l_opy_.returncode)
        else:
          if bstack1llll1ll1_opy_(bstack11lll11l1l_opy_[bstack1l1l1ll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ෨")]):
            bstack11lll11l1l_opy_[bstack1l1l1ll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ෩")].remove(bstack1l1l1ll_opy_ (u"࠭࠭࡮ࠩ෪"))
            bstack11lll11l1l_opy_[bstack1l1l1ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ෫")].remove(bstack1l1l1ll_opy_ (u"ࠨࡲࡧࡦࠬ෬"))
            bstack11lll11l1l_opy_[bstack1l1l1ll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ෭")] = bstack11lll11l1l_opy_[bstack1l1l1ll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭෮")][0]
          bstack1ll1111l1l_opy_(bstack11111111l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack11lll11l1l_opy_[bstack1l1l1ll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ෯")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1l1l1ll_opy_ (u"ࠬࡥ࡟࡯ࡣࡰࡩࡤࡥࠧ෰")] = bstack1l1l1ll_opy_ (u"࠭࡟ࡠ࡯ࡤ࡭ࡳࡥ࡟ࠨ෱")
          mod_globals[bstack1l1l1ll_opy_ (u"ࠧࡠࡡࡩ࡭ࡱ࡫࡟ࡠࠩෲ")] = os.path.abspath(bstack11lll11l1l_opy_[bstack1l1l1ll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫෳ")])
          exec(open(bstack11lll11l1l_opy_[bstack1l1l1ll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ෴")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1l1l1ll_opy_ (u"ࠪࡇࡦࡻࡧࡩࡶࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࡼࡿࠪ෵").format(str(e)))
          for driver in bstack1lll1l1l1l_opy_:
            bstack1l11l1llll_opy_.append({
              bstack1l1l1ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ෶"): bstack11lll11l1l_opy_[bstack1l1l1ll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ෷")],
              bstack1l1l1ll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ෸"): str(e),
              bstack1l1l1ll_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭෹"): multiprocessing.current_process().name
            })
            bstack11ll111111_opy_(driver, bstack1l1l1ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ෺"), bstack1l1l1ll_opy_ (u"ࠤࡖࡩࡸࡹࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧ෻") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1lll1l1l1l_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1l111111l1_opy_, CONFIG, logger)
      bstack11l1l1111_opy_()
      bstack11l1ll1111_opy_()
      percy.bstack11l1ll1lll_opy_()
      bstack1l11l1l1l1_opy_ = {
        bstack1l1l1ll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭෼"): args[0],
        bstack1l1l1ll_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫ෽"): CONFIG,
        bstack1l1l1ll_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭෾"): bstack1lll1l1ll_opy_,
        bstack1l1l1ll_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ෿"): bstack1l111111l1_opy_
      }
      if bstack1l1l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ฀") in CONFIG:
        bstack1l11llll11_opy_ = bstack11l11111ll_opy_(args, logger, CONFIG, bstack1lllll111l_opy_, bstack1lll11ll11_opy_)
        bstack1l1l11l1l1_opy_ = bstack1l11llll11_opy_.bstack1l11l1lll_opy_(run_on_browserstack, bstack1l11l1l1l1_opy_, bstack1llll1ll1_opy_(args))
      else:
        if bstack1llll1ll1_opy_(args):
          bstack1l11l1l1l1_opy_[bstack1l1l1ll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫก")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1l11l1l1l1_opy_,))
          test.start()
          test.join()
        else:
          bstack1ll1111l1l_opy_(bstack11111111l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1l1l1ll_opy_ (u"ࠩࡢࡣࡳࡧ࡭ࡦࡡࡢࠫข")] = bstack1l1l1ll_opy_ (u"ࠪࡣࡤࡳࡡࡪࡰࡢࡣࠬฃ")
          mod_globals[bstack1l1l1ll_opy_ (u"ࠫࡤࡥࡦࡪ࡮ࡨࡣࡤ࠭ค")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1l1lll1ll_opy_ == bstack1l1l1ll_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫฅ") or bstack1l1lll1ll_opy_ == bstack1l1l1ll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬฆ"):
    percy.init(bstack1l111111l1_opy_, CONFIG, logger)
    percy.bstack11l1ll1lll_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1ll111lll_opy_(e, bstack1l1ll1ll_opy_)
    bstack11l1l1111_opy_()
    bstack1ll1111l1l_opy_(bstack11l1lll1l_opy_)
    if bstack1lllll111l_opy_:
      bstack11lll1l11l_opy_(bstack11l1lll1l_opy_, args)
      if bstack1l1l1ll_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬง") in args:
        i = args.index(bstack1l1l1ll_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭จ"))
        args.pop(i)
        args.pop(i)
      if bstack1l1l1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬฉ") not in CONFIG:
        CONFIG[bstack1l1l1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ช")] = [{}]
        bstack1lll11ll11_opy_ = 1
      if bstack1ll1l1l1l1_opy_ == 0:
        bstack1ll1l1l1l1_opy_ = 1
      args.insert(0, str(bstack1ll1l1l1l1_opy_))
      args.insert(0, str(bstack1l1l1ll_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩซ")))
    if bstack1llllll11l_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1l11lll11l_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1l1lll11l_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack1l1l1ll_opy_ (u"ࠧࡘࡏࡃࡑࡗࡣࡔࡖࡔࡊࡑࡑࡗࠧฌ"),
        ).parse_args(bstack1l11lll11l_opy_)
        bstack111llll1_opy_ = args.index(bstack1l11lll11l_opy_[0]) if len(bstack1l11lll11l_opy_) > 0 else len(args)
        args.insert(bstack111llll1_opy_, str(bstack1l1l1ll_opy_ (u"࠭࠭࠮࡮࡬ࡷࡹ࡫࡮ࡦࡴࠪญ")))
        args.insert(bstack111llll1_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l1l1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡳࡱࡥࡳࡹࡥ࡬ࡪࡵࡷࡩࡳ࡫ࡲ࠯ࡲࡼࠫฎ"))))
        if bstack1l1l1llll1_opy_.bstack11111llll_opy_(CONFIG):
          args.insert(bstack111llll1_opy_, str(bstack1l1l1ll_opy_ (u"ࠨ࠯࠰ࡰ࡮ࡹࡴࡦࡰࡨࡶࠬฏ")))
          args.insert(bstack111llll1_opy_ + 1, str(bstack1l1l1ll_opy_ (u"ࠩࡕࡩࡹࡸࡹࡇࡣ࡬ࡰࡪࡪ࠺ࡼࡿࠪฐ").format(bstack1l1l1llll1_opy_.bstack1l11l111_opy_(CONFIG))))
        if bstack11lll1ll11_opy_(os.environ.get(bstack1l1l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠨฑ"))) and str(os.environ.get(bstack1l1l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠨฒ"), bstack1l1l1ll_opy_ (u"ࠬࡴࡵ࡭࡮ࠪณ"))) != bstack1l1l1ll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫด"):
          for bstack1111ll1l_opy_ in bstack1l1lll11l_opy_:
            args.remove(bstack1111ll1l_opy_)
          test_files = os.environ.get(bstack1l1l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠫต")).split(bstack1l1l1ll_opy_ (u"ࠨ࠮ࠪถ"))
          for bstack1ll11ll1ll_opy_ in test_files:
            args.append(bstack1ll11ll1ll_opy_)
      except Exception as e:
        logger.error(bstack1l1l1ll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡢࡶࡷࡥࡨ࡮ࡩ࡯ࡩࠣࡰ࡮ࡹࡴࡦࡰࡨࡶࠥ࡬࡯ࡳࠢࡾࢁ࠳ࠦࡅࡳࡴࡲࡶࠥ࠳ࠠࡼࡿࠥท").format(bstack1l11l11111_opy_, e))
    pabot.main(args)
  elif bstack1l1lll1ll_opy_ == bstack1l1l1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫธ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1ll111lll_opy_(e, bstack1l1ll1ll_opy_)
    for a in args:
      if bstack1l1l1ll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚ࠪน") in a:
        bstack1l11lll1_opy_ = int(a.split(bstack1l1l1ll_opy_ (u"ࠬࡀࠧบ"))[1])
      if bstack1l1l1ll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪป") in a:
        bstack11l11lll11_opy_ = str(a.split(bstack1l1l1ll_opy_ (u"ࠧ࠻ࠩผ"))[1])
      if bstack1l1l1ll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓࠨฝ") in a:
        bstack1l1l1ll1l1_opy_ = str(a.split(bstack1l1l1ll_opy_ (u"ࠩ࠽ࠫพ"))[1])
    bstack1l11l111l_opy_ = None
    if bstack1l1l1ll_opy_ (u"ࠪ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠩฟ") in args:
      i = args.index(bstack1l1l1ll_opy_ (u"ࠫ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠪภ"))
      args.pop(i)
      bstack1l11l111l_opy_ = args.pop(i)
    if bstack1l11l111l_opy_ is not None:
      global bstack1ll11llll1_opy_
      bstack1ll11llll1_opy_ = bstack1l11l111l_opy_
    bstack1ll1111l1l_opy_(bstack11l1lll1l_opy_)
    run_cli(args)
    if bstack1l1l1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩม") in multiprocessing.current_process().__dict__.keys():
      for bstack1l111111_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1l11l1llll_opy_.append(bstack1l111111_opy_)
  elif bstack1l1lll1ll_opy_ == bstack1l1l1ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ย"):
    bstack11l1lll1ll_opy_ = bstack11111ll1l_opy_(args, logger, CONFIG, bstack1lllll111l_opy_)
    bstack11l1lll1ll_opy_.bstack11111l11l_opy_()
    bstack11l1l1111_opy_()
    bstack1lllll11l_opy_ = True
    bstack11llll1l1_opy_ = bstack11l1lll1ll_opy_.bstack1lll1ll111_opy_()
    bstack11l1lll1ll_opy_.bstack1l11l1l1_opy_()
    bstack11l1lll1ll_opy_.bstack1l11l1l1l1_opy_(bstack1lll1lll1l_opy_)
    bstack1l1l1llll_opy_(bstack1l1lll1ll_opy_, CONFIG, bstack11l1lll1ll_opy_.bstack111l111ll_opy_())
    bstack11l1ll11ll_opy_ = bstack11l1lll1ll_opy_.bstack1l11l1lll_opy_(bstack11l11l1l1l_opy_, {
      bstack1l1l1ll_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨร"): bstack1lll1l1ll_opy_,
      bstack1l1l1ll_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪฤ"): bstack1l111111l1_opy_,
      bstack1l1l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬล"): bstack1lllll111l_opy_
    })
    try:
      bstack1llll111l_opy_, bstack1l111l1lll_opy_ = map(list, zip(*bstack11l1ll11ll_opy_))
      bstack1ll1111l1_opy_ = bstack1llll111l_opy_[0]
      for status_code in bstack1l111l1lll_opy_:
        if status_code != 0:
          bstack1llll1l1_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack1l1l1ll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡢࡸࡨࠤࡪࡸࡲࡰࡴࡶࠤࡦࡴࡤࠡࡵࡷࡥࡹࡻࡳࠡࡥࡲࡨࡪ࠴ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࠾ࠥࢁࡽࠣฦ").format(str(e)))
  elif bstack1l1lll1ll_opy_ == bstack1l1l1ll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫว"):
    try:
      from behave.__main__ import main as bstack111l11l1_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1ll111lll_opy_(e, bstack1l111ll11_opy_)
    bstack11l1l1111_opy_()
    bstack1lllll11l_opy_ = True
    bstack1ll11ll1l_opy_ = 1
    if bstack1l1l1ll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬศ") in CONFIG:
      bstack1ll11ll1l_opy_ = CONFIG[bstack1l1l1ll_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ษ")]
    if bstack1l1l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪส") in CONFIG:
      bstack1l111l11l_opy_ = int(bstack1ll11ll1l_opy_) * int(len(CONFIG[bstack1l1l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫห")]))
    else:
      bstack1l111l11l_opy_ = int(bstack1ll11ll1l_opy_)
    config = Configuration(args)
    bstack11l1l1l1_opy_ = config.paths
    if len(bstack11l1l1l1_opy_) == 0:
      import glob
      pattern = bstack1l1l1ll_opy_ (u"ࠩ࠭࠮࠴࠰࠮ࡧࡧࡤࡸࡺࡸࡥࠨฬ")
      bstack1lll1111l1_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1lll1111l1_opy_)
      config = Configuration(args)
      bstack11l1l1l1_opy_ = config.paths
    bstack11llll1111_opy_ = [os.path.normpath(item) for item in bstack11l1l1l1_opy_]
    bstack1ll111l11l_opy_ = [os.path.normpath(item) for item in args]
    bstack1ll1ll11l_opy_ = [item for item in bstack1ll111l11l_opy_ if item not in bstack11llll1111_opy_]
    import platform as pf
    if pf.system().lower() == bstack1l1l1ll_opy_ (u"ࠪࡻ࡮ࡴࡤࡰࡹࡶࠫอ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack11llll1111_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1llll11l_opy_)))
                    for bstack1llll11l_opy_ in bstack11llll1111_opy_]
    bstack11lll11l_opy_ = []
    for spec in bstack11llll1111_opy_:
      bstack1ll1l1111l_opy_ = []
      bstack1ll1l1111l_opy_ += bstack1ll1ll11l_opy_
      bstack1ll1l1111l_opy_.append(spec)
      bstack11lll11l_opy_.append(bstack1ll1l1111l_opy_)
    execution_items = []
    for bstack1ll1l1111l_opy_ in bstack11lll11l_opy_:
      if bstack1l1l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧฮ") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack1l1l1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨฯ")]):
          item = {}
          item[bstack1l1l1ll_opy_ (u"࠭ࡡࡳࡩࠪะ")] = bstack1l1l1ll_opy_ (u"ࠧࠡࠩั").join(bstack1ll1l1111l_opy_)
          item[bstack1l1l1ll_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧา")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack1l1l1ll_opy_ (u"ࠩࡤࡶ࡬࠭ำ")] = bstack1l1l1ll_opy_ (u"ࠪࠤࠬิ").join(bstack1ll1l1111l_opy_)
        item[bstack1l1l1ll_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪี")] = 0
        execution_items.append(item)
    bstack11ll11l11l_opy_ = bstack11111lll1_opy_(execution_items, bstack1l111l11l_opy_)
    for execution_item in bstack11ll11l11l_opy_:
      bstack11l1l111ll_opy_ = []
      for item in execution_item:
        bstack11l1l111ll_opy_.append(bstack1lll1l1ll1_opy_(name=str(item[bstack1l1l1ll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫึ")]),
                                             target=bstack11l1l1ll_opy_,
                                             args=(item[bstack1l1l1ll_opy_ (u"࠭ࡡࡳࡩࠪื")],)))
      for t in bstack11l1l111ll_opy_:
        t.start()
      for t in bstack11l1l111ll_opy_:
        t.join()
  else:
    bstack1l1l11l111_opy_(bstack1lll1lll_opy_)
  if not bstack11lll11l1l_opy_:
    bstack11ll1ll11_opy_()
    if(bstack1l1lll1ll_opy_ in [bstack1l1l1ll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ุࠧ"), bstack1l1l1ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨู")]):
      bstack1ll1lllll_opy_()
  bstack1l1l11lll1_opy_.bstack1llll111l1_opy_()
def browserstack_initialize(bstack11ll11l111_opy_=None):
  logger.info(bstack1l1l1ll_opy_ (u"ࠩࡕࡹࡳࡴࡩ࡯ࡩࠣࡗࡉࡑࠠࡸ࡫ࡷ࡬ࠥࡧࡲࡨࡵ࠽ࠤฺࠬ") + str(bstack11ll11l111_opy_))
  run_on_browserstack(bstack11ll11l111_opy_, None, True)
@measure(event_name=EVENTS.bstack111l1ll1l_opy_, stage=STAGE.bstack1l1ll11l1_opy_, bstack111l1llll_opy_=bstack1llll111_opy_)
def bstack11ll1ll11_opy_():
  global CONFIG
  global bstack1l1l1l11l_opy_
  global bstack1llll1l1_opy_
  global bstack11ll1l1l1_opy_
  global bstack1l1l1111l1_opy_
  bstack1l11lll1ll_opy_.bstack1l1ll111_opy_()
  if cli.is_running():
    bstack1111lll11_opy_.invoke(bstack11ll1111ll_opy_.bstack1ll1l1lll1_opy_)
  else:
    bstack11l1l111l1_opy_ = bstack1l1l1llll1_opy_.bstack11l1lllll1_opy_(config=CONFIG)
    bstack11l1l111l1_opy_.bstack1ll1111l_opy_(CONFIG)
  if bstack1l1l1l11l_opy_ == bstack1l1l1ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ฻"):
    if not cli.is_enabled(CONFIG):
      bstack1llllll11l_opy_.stop()
  else:
    bstack1llllll11l_opy_.stop()
  if not cli.is_enabled(CONFIG):
    bstack1l1ll1l11l_opy_.bstack1l11lll1l_opy_()
  if bstack1l1l1ll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ฼") in CONFIG and str(CONFIG[bstack1l1l1ll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ฽")]).lower() != bstack1l1l1ll_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ฾"):
    hashed_id, bstack1ll1l11l1l_opy_ = bstack1lll1lllll_opy_()
  else:
    hashed_id, bstack1ll1l11l1l_opy_ = get_build_link()
  bstack1lllll1l1l_opy_(hashed_id)
  logger.info(bstack1l1l1ll_opy_ (u"ࠧࡔࡆࡎࠤࡷࡻ࡮ࠡࡧࡱࡨࡪࡪࠠࡧࡱࡵࠤ࡮ࡪ࠺ࠨ฿") + bstack1l1l1111l1_opy_.get_property(bstack1l1l1ll_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪเ"), bstack1l1l1ll_opy_ (u"ࠩࠪแ")) + bstack1l1l1ll_opy_ (u"ࠪ࠰ࠥࡺࡥࡴࡶ࡫ࡹࡧࠦࡩࡥ࠼ࠣࠫโ") + os.getenv(bstack1l1l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩใ"), bstack1l1l1ll_opy_ (u"ࠬ࠭ไ")))
  if hashed_id is not None and bstack1l111llll_opy_() != -1:
    sessions = bstack1ll11l11ll_opy_(hashed_id)
    bstack11ll11l1_opy_(sessions, bstack1ll1l11l1l_opy_)
  if bstack1l1l1l11l_opy_ == bstack1l1l1ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ๅ") and bstack1llll1l1_opy_ != 0:
    sys.exit(bstack1llll1l1_opy_)
  if bstack1l1l1l11l_opy_ == bstack1l1l1ll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧๆ") and bstack11ll1l1l1_opy_ != 0:
    sys.exit(bstack11ll1l1l1_opy_)
def bstack1lllll1l1l_opy_(new_id):
    global bstack11lll1l111_opy_
    bstack11lll1l111_opy_ = new_id
def bstack1lll1l111l_opy_(bstack1ll11111l1_opy_):
  if bstack1ll11111l1_opy_:
    return bstack1ll11111l1_opy_.capitalize()
  else:
    return bstack1l1l1ll_opy_ (u"ࠨࠩ็")
@measure(event_name=EVENTS.bstack11lllll1l1_opy_, stage=STAGE.bstack1l1ll11l1_opy_, bstack111l1llll_opy_=bstack1llll111_opy_)
def bstack1l111ll1_opy_(bstack11l1l1ll1_opy_):
  if bstack1l1l1ll_opy_ (u"ࠩࡱࡥࡲ࡫่ࠧ") in bstack11l1l1ll1_opy_ and bstack11l1l1ll1_opy_[bstack1l1l1ll_opy_ (u"ࠪࡲࡦࡳࡥࠨ้")] != bstack1l1l1ll_opy_ (u"๊ࠫࠬ"):
    return bstack11l1l1ll1_opy_[bstack1l1l1ll_opy_ (u"ࠬࡴࡡ࡮ࡧ๋ࠪ")]
  else:
    bstack111l1llll_opy_ = bstack1l1l1ll_opy_ (u"ࠨࠢ์")
    if bstack1l1l1ll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧํ") in bstack11l1l1ll1_opy_ and bstack11l1l1ll1_opy_[bstack1l1l1ll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨ๎")] != None:
      bstack111l1llll_opy_ += bstack11l1l1ll1_opy_[bstack1l1l1ll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩ๏")] + bstack1l1l1ll_opy_ (u"ࠥ࠰ࠥࠨ๐")
      if bstack11l1l1ll1_opy_[bstack1l1l1ll_opy_ (u"ࠫࡴࡹࠧ๑")] == bstack1l1l1ll_opy_ (u"ࠧ࡯࡯ࡴࠤ๒"):
        bstack111l1llll_opy_ += bstack1l1l1ll_opy_ (u"ࠨࡩࡐࡕࠣࠦ๓")
      bstack111l1llll_opy_ += (bstack11l1l1ll1_opy_[bstack1l1l1ll_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫ๔")] or bstack1l1l1ll_opy_ (u"ࠨࠩ๕"))
      return bstack111l1llll_opy_
    else:
      bstack111l1llll_opy_ += bstack1lll1l111l_opy_(bstack11l1l1ll1_opy_[bstack1l1l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪ๖")]) + bstack1l1l1ll_opy_ (u"ࠥࠤࠧ๗") + (
              bstack11l1l1ll1_opy_[bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭๘")] or bstack1l1l1ll_opy_ (u"ࠬ࠭๙")) + bstack1l1l1ll_opy_ (u"ࠨࠬࠡࠤ๚")
      if bstack11l1l1ll1_opy_[bstack1l1l1ll_opy_ (u"ࠧࡰࡵࠪ๛")] == bstack1l1l1ll_opy_ (u"࡙ࠣ࡬ࡲࡩࡵࡷࡴࠤ๜"):
        bstack111l1llll_opy_ += bstack1l1l1ll_opy_ (u"ࠤ࡚࡭ࡳࠦࠢ๝")
      bstack111l1llll_opy_ += bstack11l1l1ll1_opy_[bstack1l1l1ll_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ๞")] or bstack1l1l1ll_opy_ (u"ࠫࠬ๟")
      return bstack111l1llll_opy_
@measure(event_name=EVENTS.bstack1lll11111_opy_, stage=STAGE.bstack1l1ll11l1_opy_, bstack111l1llll_opy_=bstack1llll111_opy_)
def bstack11l11l1ll_opy_(bstack1l1ll1l1_opy_):
  if bstack1l1ll1l1_opy_ == bstack1l1l1ll_opy_ (u"ࠧࡪ࡯࡯ࡧࠥ๠"):
    return bstack1l1l1ll_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡩࡵࡩࡪࡴ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡩࡵࡩࡪࡴࠢ࠿ࡅࡲࡱࡵࡲࡥࡵࡧࡧࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩ๡")
  elif bstack1l1ll1l1_opy_ == bstack1l1l1ll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ๢"):
    return bstack1l1l1ll_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡶࡪࡪ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡴࡨࡨࠧࡄࡆࡢ࡫࡯ࡩࡩࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫ๣")
  elif bstack1l1ll1l1_opy_ == bstack1l1l1ll_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ๤"):
    return bstack1l1l1ll_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿࡭ࡲࡦࡧࡱ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧ࡭ࡲࡦࡧࡱࠦࡃࡖࡡࡴࡵࡨࡨࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪ๥")
  elif bstack1l1ll1l1_opy_ == bstack1l1l1ll_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥ๦"):
    return bstack1l1l1ll_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡳࡧࡧ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡸࡥࡥࠤࡁࡉࡷࡸ࡯ࡳ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ๧")
  elif bstack1l1ll1l1_opy_ == bstack1l1l1ll_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࠢ๨"):
    return bstack1l1l1ll_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࠦࡩࡪࡧ࠳࠳࠸࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࠨ࡫ࡥࡢ࠵࠵࠺ࠧࡄࡔࡪ࡯ࡨࡳࡺࡺ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ๩")
  elif bstack1l1ll1l1_opy_ == bstack1l1l1ll_opy_ (u"ࠣࡴࡸࡲࡳ࡯࡮ࡨࠤ๪"):
    return bstack1l1l1ll_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡧࡲࡡࡤ࡭࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡧࡲࡡࡤ࡭ࠥࡂࡗࡻ࡮࡯࡫ࡱ࡫ࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪ๫")
  else:
    return bstack1l1l1ll_opy_ (u"ࠪࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡢ࡭ࡣࡦ࡯ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡢ࡭ࡣࡦ࡯ࠧࡄࠧ๬") + bstack1lll1l111l_opy_(
      bstack1l1ll1l1_opy_) + bstack1l1l1ll_opy_ (u"ࠫࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪ๭")
def bstack1ll11l111l_opy_(session):
  return bstack1l1l1ll_opy_ (u"ࠬࡂࡴࡳࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡵࡳࡼࠨ࠾࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠢࡶࡩࡸࡹࡩࡰࡰ࠰ࡲࡦࡳࡥࠣࡀ࠿ࡥࠥ࡮ࡲࡦࡨࡀࠦࢀࢃࠢࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤࡢࡦࡱࡧ࡮࡬ࠤࡁࡿࢂࡂ࠯ࡢࡀ࠿࠳ࡹࡪ࠾ࡼࡿࡾࢁࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼࠰ࡶࡵࡂࠬ๮").format(
    session[bstack1l1l1ll_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨࡥࡵࡳ࡮ࠪ๯")], bstack1l111ll1_opy_(session), bstack11l11l1ll_opy_(session[bstack1l1l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡳࡵࡣࡷࡹࡸ࠭๰")]),
    bstack11l11l1ll_opy_(session[bstack1l1l1ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ๱")]),
    bstack1lll1l111l_opy_(session[bstack1l1l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪ๲")] or session[bstack1l1l1ll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪ๳")] or bstack1l1l1ll_opy_ (u"ࠫࠬ๴")) + bstack1l1l1ll_opy_ (u"ࠧࠦࠢ๵") + (session[bstack1l1l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ๶")] or bstack1l1l1ll_opy_ (u"ࠧࠨ๷")),
    session[bstack1l1l1ll_opy_ (u"ࠨࡱࡶࠫ๸")] + bstack1l1l1ll_opy_ (u"ࠤࠣࠦ๹") + session[bstack1l1l1ll_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ๺")], session[bstack1l1l1ll_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭๻")] or bstack1l1l1ll_opy_ (u"ࠬ࠭๼"),
    session[bstack1l1l1ll_opy_ (u"࠭ࡣࡳࡧࡤࡸࡪࡪ࡟ࡢࡶࠪ๽")] if session[bstack1l1l1ll_opy_ (u"ࠧࡤࡴࡨࡥࡹ࡫ࡤࡠࡣࡷࠫ๾")] else bstack1l1l1ll_opy_ (u"ࠨࠩ๿"))
@measure(event_name=EVENTS.bstack1l11111ll1_opy_, stage=STAGE.bstack1l1ll11l1_opy_, bstack111l1llll_opy_=bstack1llll111_opy_)
def bstack11ll11l1_opy_(sessions, bstack1ll1l11l1l_opy_):
  try:
    bstack1l1l11ll1l_opy_ = bstack1l1l1ll_opy_ (u"ࠤࠥ຀")
    if not os.path.exists(bstack1l111l111l_opy_):
      os.mkdir(bstack1l111l111l_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l1l1ll_opy_ (u"ࠪࡥࡸࡹࡥࡵࡵ࠲ࡶࡪࡶ࡯ࡳࡶ࠱࡬ࡹࡳ࡬ࠨກ")), bstack1l1l1ll_opy_ (u"ࠫࡷ࠭ຂ")) as f:
      bstack1l1l11ll1l_opy_ = f.read()
    bstack1l1l11ll1l_opy_ = bstack1l1l11ll1l_opy_.replace(bstack1l1l1ll_opy_ (u"ࠬࢁࠥࡓࡇࡖ࡙ࡑ࡚ࡓࡠࡅࡒ࡙ࡓ࡚ࠥࡾࠩ຃"), str(len(sessions)))
    bstack1l1l11ll1l_opy_ = bstack1l1l11ll1l_opy_.replace(bstack1l1l1ll_opy_ (u"࠭ࡻࠦࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠩࢂ࠭ຄ"), bstack1ll1l11l1l_opy_)
    bstack1l1l11ll1l_opy_ = bstack1l1l11ll1l_opy_.replace(bstack1l1l1ll_opy_ (u"ࠧࡼࠧࡅ࡙ࡎࡒࡄࡠࡐࡄࡑࡊࠫࡽࠨ຅"),
                                              sessions[0].get(bstack1l1l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟࡯ࡣࡰࡩࠬຆ")) if sessions[0] else bstack1l1l1ll_opy_ (u"ࠩࠪງ"))
    with open(os.path.join(bstack1l111l111l_opy_, bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡵࡩࡵࡵࡲࡵ࠰࡫ࡸࡲࡲࠧຈ")), bstack1l1l1ll_opy_ (u"ࠫࡼ࠭ຉ")) as stream:
      stream.write(bstack1l1l11ll1l_opy_.split(bstack1l1l1ll_opy_ (u"ࠬࢁࠥࡔࡇࡖࡗࡎࡕࡎࡔࡡࡇࡅ࡙ࡇࠥࡾࠩຊ"))[0])
      for session in sessions:
        stream.write(bstack1ll11l111l_opy_(session))
      stream.write(bstack1l1l11ll1l_opy_.split(bstack1l1l1ll_opy_ (u"࠭ࡻࠦࡕࡈࡗࡘࡏࡏࡏࡕࡢࡈࡆ࡚ࡁࠦࡿࠪ຋"))[1])
    logger.info(bstack1l1l1ll_opy_ (u"ࠧࡈࡧࡱࡩࡷࡧࡴࡦࡦࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡥࡹ࡮ࡲࡤࠡࡣࡵࡸ࡮࡬ࡡࡤࡶࡶࠤࡦࡺࠠࡼࡿࠪຌ").format(bstack1l111l111l_opy_));
  except Exception as e:
    logger.debug(bstack1ll1llll1l_opy_.format(str(e)))
def bstack1ll11l11ll_opy_(hashed_id):
  global CONFIG
  try:
    bstack1lll111ll1_opy_ = datetime.datetime.now()
    host = bstack1l1l1ll_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡴ࡮࠳ࡣ࡭ࡱࡸࡨ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨຍ") if bstack1l1l1ll_opy_ (u"ࠩࡤࡴࡵ࠭ຎ") in CONFIG else bstack1l1l1ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫຏ")
    user = CONFIG[bstack1l1l1ll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ຐ")]
    key = CONFIG[bstack1l1l1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨຑ")]
    bstack11lll11111_opy_ = bstack1l1l1ll_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬຒ") if bstack1l1l1ll_opy_ (u"ࠧࡢࡲࡳࠫຓ") in CONFIG else (bstack1l1l1ll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬດ") if CONFIG.get(bstack1l1l1ll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭ຕ")) else bstack1l1l1ll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬຖ"))
    host = bstack1ll11llll_opy_(cli.config, [bstack1l1l1ll_opy_ (u"ࠦࡦࡶࡩࡴࠤທ"), bstack1l1l1ll_opy_ (u"ࠧࡧࡰࡱࡃࡸࡸࡴࡳࡡࡵࡧࠥຘ"), bstack1l1l1ll_opy_ (u"ࠨࡡࡱ࡫ࠥນ")], host) if bstack1l1l1ll_opy_ (u"ࠧࡢࡲࡳࠫບ") in CONFIG else bstack1ll11llll_opy_(cli.config, [bstack1l1l1ll_opy_ (u"ࠣࡣࡳ࡭ࡸࠨປ"), bstack1l1l1ll_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨࠦຜ"), bstack1l1l1ll_opy_ (u"ࠥࡥࡵ࡯ࠢຝ")], host)
    url = bstack1l1l1ll_opy_ (u"ࠫࢀࢃ࠯ࡼࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂ࠵ࡳࡦࡵࡶ࡭ࡴࡴࡳ࠯࡬ࡶࡳࡳ࠭ພ").format(host, bstack11lll11111_opy_, hashed_id)
    headers = {
      bstack1l1l1ll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫຟ"): bstack1l1l1ll_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩຠ"),
    }
    proxies = bstack1lll1ll1_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies, auth=(user, key))
    if response.json():
      cli.bstack1ll1ll11ll_opy_(bstack1l1l1ll_opy_ (u"ࠢࡩࡶࡷࡴ࠿࡭ࡥࡵࡡࡶࡩࡸࡹࡩࡰࡰࡶࡣࡱ࡯ࡳࡵࠤມ"), datetime.datetime.now() - bstack1lll111ll1_opy_)
      return list(map(lambda session: session[bstack1l1l1ll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ຢ")], response.json()))
  except Exception as e:
    logger.debug(bstack1ll1l11l_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack1ll111111l_opy_, stage=STAGE.bstack1l1ll11l1_opy_, bstack111l1llll_opy_=bstack1llll111_opy_)
def get_build_link():
  global CONFIG
  global bstack11lll1l111_opy_
  try:
    if bstack1l1l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬຣ") in CONFIG:
      bstack1lll111ll1_opy_ = datetime.datetime.now()
      host = bstack1l1l1ll_opy_ (u"ࠪࡥࡵ࡯࠭ࡤ࡮ࡲࡹࡩ࠭຤") if bstack1l1l1ll_opy_ (u"ࠫࡦࡶࡰࠨລ") in CONFIG else bstack1l1l1ll_opy_ (u"ࠬࡧࡰࡪࠩ຦")
      user = CONFIG[bstack1l1l1ll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨວ")]
      key = CONFIG[bstack1l1l1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪຨ")]
      bstack11lll11111_opy_ = bstack1l1l1ll_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧຩ") if bstack1l1l1ll_opy_ (u"ࠩࡤࡴࡵ࠭ສ") in CONFIG else bstack1l1l1ll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬຫ")
      url = bstack1l1l1ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࢀࢃ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠴ࡪࡴࡱࡱࠫຬ").format(user, key, host, bstack11lll11111_opy_)
      if cli.is_enabled(CONFIG):
        bstack1ll1l11l1l_opy_, hashed_id = cli.bstack1l11111lll_opy_()
        logger.info(bstack1l1ll1l111_opy_.format(bstack1ll1l11l1l_opy_))
        return [hashed_id, bstack1ll1l11l1l_opy_]
      else:
        headers = {
          bstack1l1l1ll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫອ"): bstack1l1l1ll_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩຮ"),
        }
        if bstack1l1l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩຯ") in CONFIG:
          params = {bstack1l1l1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ະ"): CONFIG[bstack1l1l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬັ")], bstack1l1l1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭າ"): CONFIG[bstack1l1l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ຳ")]}
        else:
          params = {bstack1l1l1ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪິ"): CONFIG[bstack1l1l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩີ")]}
        proxies = bstack1lll1ll1_opy_(CONFIG, url)
        response = requests.get(url, params=params, headers=headers, proxies=proxies)
        if response.json():
          bstack11ll1l11l_opy_ = response.json()[0][bstack1l1l1ll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡧࡻࡩ࡭ࡦࠪຶ")]
          if bstack11ll1l11l_opy_:
            bstack1ll1l11l1l_opy_ = bstack11ll1l11l_opy_[bstack1l1l1ll_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣࡠࡷࡵࡰࠬື")].split(bstack1l1l1ll_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤ࠯ࡥࡹ࡮ࡲࡤࠨຸ"))[0] + bstack1l1l1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡵ࠲ູࠫ") + bstack11ll1l11l_opy_[
              bstack1l1l1ll_opy_ (u"ࠫ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪ຺ࠧ")]
            logger.info(bstack1l1ll1l111_opy_.format(bstack1ll1l11l1l_opy_))
            bstack11lll1l111_opy_ = bstack11ll1l11l_opy_[bstack1l1l1ll_opy_ (u"ࠬ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨົ")]
            bstack1l1lll111l_opy_ = CONFIG[bstack1l1l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩຼ")]
            if bstack1l1l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩຽ") in CONFIG:
              bstack1l1lll111l_opy_ += bstack1l1l1ll_opy_ (u"ࠨࠢࠪ຾") + CONFIG[bstack1l1l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ຿")]
            if bstack1l1lll111l_opy_ != bstack11ll1l11l_opy_[bstack1l1l1ll_opy_ (u"ࠪࡲࡦࡳࡥࠨເ")]:
              logger.debug(bstack11ll1llll1_opy_.format(bstack11ll1l11l_opy_[bstack1l1l1ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩແ")], bstack1l1lll111l_opy_))
            cli.bstack1ll1ll11ll_opy_(bstack1l1l1ll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࡫ࡪࡺ࡟ࡣࡷ࡬ࡰࡩࡥ࡬ࡪࡰ࡮ࠦໂ"), datetime.datetime.now() - bstack1lll111ll1_opy_)
            return [bstack11ll1l11l_opy_[bstack1l1l1ll_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩໃ")], bstack1ll1l11l1l_opy_]
    else:
      logger.warn(bstack11l111ll1_opy_)
  except Exception as e:
    logger.debug(bstack1llllllll_opy_.format(str(e)))
  return [None, None]
def bstack11l11lll_opy_(url, bstack1ll1llll1_opy_=False):
  global CONFIG
  global bstack1llll1l11l_opy_
  if not bstack1llll1l11l_opy_:
    hostname = bstack1l1l1l1ll_opy_(url)
    is_private = bstack11l1l1l1l1_opy_(hostname)
    if (bstack1l1l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫໄ") in CONFIG and not bstack11lll1ll11_opy_(CONFIG[bstack1l1l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ໅")])) and (is_private or bstack1ll1llll1_opy_):
      bstack1llll1l11l_opy_ = hostname
def bstack1l1l1l1ll_opy_(url):
  return urlparse(url).hostname
def bstack11l1l1l1l1_opy_(hostname):
  for bstack111ll11ll_opy_ in bstack11lllll11_opy_:
    regex = re.compile(bstack111ll11ll_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack11l1ll11l1_opy_(bstack1lll111l1_opy_):
  return True if bstack1lll111l1_opy_ in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack1l111l1ll_opy_, stage=STAGE.bstack1l1ll11l1_opy_, bstack111l1llll_opy_=bstack1llll111_opy_)
def getAccessibilityResults(driver):
  global CONFIG
  global bstack1l11lll1_opy_
  bstack11lll1111l_opy_ = not (bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ໆ"), None) and bstack1l111l1l_opy_(
          threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ໇"), None))
  bstack11l1111lll_opy_ = getattr(driver, bstack1l1l1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱ່ࠫ"), None) != True
  bstack11lll1l11_opy_ = bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠬ࡯ࡳࡂࡲࡳࡅ࠶࠷ࡹࡕࡧࡶࡸ້ࠬ"), None) and bstack1l111l1l_opy_(
          threading.current_thread(), bstack1l1l1ll_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ໊"), None)
  if bstack11lll1l11_opy_:
    if not bstack111l1l11_opy_():
      logger.warning(bstack1l1l1ll_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡲࡳࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡪࡺࡲࡪࡧࡹࡩࠥࡇࡰࡱࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵ࠱໋ࠦ"))
      return {}
    logger.debug(bstack1l1l1ll_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠬ໌"))
    logger.debug(perform_scan(driver, driver_command=bstack1l1l1ll_opy_ (u"ࠩࡨࡼࡪࡩࡵࡵࡧࡖࡧࡷ࡯ࡰࡵࠩໍ")))
    results = bstack11l1111l11_opy_(bstack1l1l1ll_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡶࠦ໎"))
    if results is not None and results.get(bstack1l1l1ll_opy_ (u"ࠦ࡮ࡹࡳࡶࡧࡶࠦ໏")) is not None:
        return results[bstack1l1l1ll_opy_ (u"ࠧ࡯ࡳࡴࡷࡨࡷࠧ໐")]
    logger.error(bstack1l1l1ll_opy_ (u"ࠨࡎࡰࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡕࡩࡸࡻ࡬ࡵࡵࠣࡻࡪࡸࡥࠡࡨࡲࡹࡳࡪ࠮ࠣ໑"))
    return []
  if not bstack1lll11l1ll_opy_.bstack11ll1111l1_opy_(CONFIG, bstack1l11lll1_opy_) or (bstack11l1111lll_opy_ and bstack11lll1111l_opy_):
    logger.warning(bstack1l1l1ll_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴ࠰ࠥ໒"))
    return {}
  try:
    logger.debug(bstack1l1l1ll_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠬ໓"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack1lll11l1l1_opy_.bstack11l1l1l11l_opy_)
    return results
  except Exception:
    logger.error(bstack1l1l1ll_opy_ (u"ࠤࡑࡳࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡷࡦࡴࡨࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦ໔"))
    return {}
@measure(event_name=EVENTS.bstack11l1l11l11_opy_, stage=STAGE.bstack1l1ll11l1_opy_, bstack111l1llll_opy_=bstack1llll111_opy_)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack1l11lll1_opy_
  bstack11lll1111l_opy_ = not (bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ໕"), None) and bstack1l111l1l_opy_(
          threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ໖"), None))
  bstack11l1111lll_opy_ = getattr(driver, bstack1l1l1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬ໗"), None) != True
  bstack11lll1l11_opy_ = bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭໘"), None) and bstack1l111l1l_opy_(
          threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ໙"), None)
  if bstack11lll1l11_opy_:
    if not bstack111l1l11_opy_():
      logger.warning(bstack1l1l1ll_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡳࡴࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡸࡻ࡭࡮ࡣࡵࡽ࠳ࠨ໚"))
      return {}
    logger.debug(bstack1l1l1ll_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡳࡶ࡯ࡰࡥࡷࡿࠧ໛"))
    logger.debug(perform_scan(driver, driver_command=bstack1l1l1ll_opy_ (u"ࠪࡩࡽ࡫ࡣࡶࡶࡨࡗࡨࡸࡩࡱࡶࠪໜ")))
    results = bstack11l1111l11_opy_(bstack1l1l1ll_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷࡗࡺࡳ࡭ࡢࡴࡼࠦໝ"))
    if results is not None and results.get(bstack1l1l1ll_opy_ (u"ࠧࡹࡵ࡮࡯ࡤࡶࡾࠨໞ")) is not None:
        return results[bstack1l1l1ll_opy_ (u"ࠨࡳࡶ࡯ࡰࡥࡷࡿࠢໟ")]
    logger.error(bstack1l1l1ll_opy_ (u"ࠢࡏࡱࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡖࡪࡹࡵ࡭ࡶࡶࠤࡘࡻ࡭࡮ࡣࡵࡽࠥࡽࡡࡴࠢࡩࡳࡺࡴࡤ࠯ࠤ໠"))
    return {}
  if not bstack1lll11l1ll_opy_.bstack11ll1111l1_opy_(CONFIG, bstack1l11lll1_opy_) or (bstack11l1111lll_opy_ and bstack11lll1111l_opy_):
    logger.warning(bstack1l1l1ll_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡷࡺࡳ࡭ࡢࡴࡼ࠲ࠧ໡"))
    return {}
  try:
    logger.debug(bstack1l1l1ll_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡳࡶ࡯ࡰࡥࡷࡿࠧ໢"))
    logger.debug(perform_scan(driver))
    bstack11ll1l1l_opy_ = driver.execute_async_script(bstack1lll11l1l1_opy_.bstack111111ll_opy_)
    return bstack11ll1l1l_opy_
  except Exception:
    logger.error(bstack1l1l1ll_opy_ (u"ࠥࡒࡴࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡶ࡯ࡰࡥࡷࡿࠠࡸࡣࡶࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦ໣"))
    return {}
def bstack111l1l11_opy_():
  global CONFIG
  global bstack1l11lll1_opy_
  bstack1ll1ll1111_opy_ = bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ໤"), None) and bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ໥"), None)
  if not bstack1lll11l1ll_opy_.bstack11ll1111l1_opy_(CONFIG, bstack1l11lll1_opy_) or not bstack1ll1ll1111_opy_:
        logger.warning(bstack1l1l1ll_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡷ࡫ࡳࡶ࡮ࡷࡷ࠳ࠨ໦"))
        return False
  return True
def bstack11l1111l11_opy_(bstack1l1ll11ll_opy_):
    bstack1llllllll1_opy_ = bstack1llllll11l_opy_.current_test_uuid() if bstack1llllll11l_opy_.current_test_uuid() else bstack1l1ll1l11l_opy_.current_hook_uuid()
    with ThreadPoolExecutor() as executor:
        future = executor.submit(bstack111111111_opy_(bstack1llllllll1_opy_, bstack1l1ll11ll_opy_))
        try:
            return future.result(timeout=bstack11l111111_opy_)
        except TimeoutError:
            logger.error(bstack1l1l1ll_opy_ (u"ࠢࡕ࡫ࡰࡩࡴࡻࡴࠡࡣࡩࡸࡪࡸࠠࡼࡿࡶࠤࡼ࡮ࡩ࡭ࡧࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡘࡥࡴࡷ࡯ࡸࡸࠨ໧").format(bstack11l111111_opy_))
        except Exception as ex:
            logger.debug(bstack1l1l1ll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡳࡧࡷࡶ࡮࡫ࡶࡪࡰࡪࠤࡆࡶࡰࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࢁࡽ࠯ࠢࡈࡶࡷࡵࡲࠡ࠯ࠣࡿࢂࠨ໨").format(bstack1l1ll11ll_opy_, str(ex)))
    return {}
@measure(event_name=EVENTS.bstack1l1l1l1ll1_opy_, stage=STAGE.bstack1l1ll11l1_opy_, bstack111l1llll_opy_=bstack1llll111_opy_)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack1l11lll1_opy_
  bstack11lll1111l_opy_ = not (bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭໩"), None) and bstack1l111l1l_opy_(
          threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ໪"), None))
  bstack1111l111_opy_ = not (bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ໫"), None) and bstack1l111l1l_opy_(
          threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ໬"), None))
  bstack11l1111lll_opy_ = getattr(driver, bstack1l1l1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭໭"), None) != True
  if not bstack1lll11l1ll_opy_.bstack11ll1111l1_opy_(CONFIG, bstack1l11lll1_opy_) or (bstack11l1111lll_opy_ and bstack11lll1111l_opy_ and bstack1111l111_opy_):
    logger.warning(bstack1l1l1ll_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡶࡰࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮࠯ࠤ໮"))
    return {}
  try:
    bstack11ll111ll_opy_ = bstack1l1l1ll_opy_ (u"ࠨࡣࡳࡴࠬ໯") in CONFIG and CONFIG.get(bstack1l1l1ll_opy_ (u"ࠩࡤࡴࡵ࠭໰"), bstack1l1l1ll_opy_ (u"ࠪࠫ໱"))
    session_id = getattr(driver, bstack1l1l1ll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨ໲"), None)
    if not session_id:
      logger.warning(bstack1l1l1ll_opy_ (u"ࠧࡔ࡯ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡌࡈࠥ࡬࡯ࡶࡰࡧࠤ࡫ࡵࡲࠡࡦࡵ࡭ࡻ࡫ࡲࠣ໳"))
      return {bstack1l1l1ll_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ໴"): bstack1l1l1ll_opy_ (u"ࠢࡏࡱࠣࡷࡪࡹࡳࡪࡱࡱࠤࡎࡊࠠࡧࡱࡸࡲࡩࠨ໵")}
    if bstack11ll111ll_opy_:
      try:
        bstack11l1l11l1l_opy_ = {
              bstack1l1l1ll_opy_ (u"ࠨࡶ࡫ࡎࡼࡺࡔࡰ࡭ࡨࡲࠬ໶"): os.environ.get(bstack1l1l1ll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ໷"), os.environ.get(bstack1l1l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ໸"), bstack1l1l1ll_opy_ (u"ࠫࠬ໹"))),
              bstack1l1l1ll_opy_ (u"ࠬࡺࡨࡕࡧࡶࡸࡗࡻ࡮ࡖࡷ࡬ࡨࠬ໺"): bstack1llllll11l_opy_.current_test_uuid() if bstack1llllll11l_opy_.current_test_uuid() else bstack1l1ll1l11l_opy_.current_hook_uuid(),
              bstack1l1l1ll_opy_ (u"࠭ࡡࡶࡶ࡫ࡌࡪࡧࡤࡦࡴࠪ໻"): os.environ.get(bstack1l1l1ll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ໼")),
              bstack1l1l1ll_opy_ (u"ࠨࡵࡦࡥࡳ࡚ࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ໽"): str(int(datetime.datetime.now().timestamp() * 1000)),
              bstack1l1l1ll_opy_ (u"ࠩࡷ࡬ࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧ໾"): os.environ.get(bstack1l1l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ໿"), bstack1l1l1ll_opy_ (u"ࠫࠬༀ")),
              bstack1l1l1ll_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬ༁"): kwargs.get(bstack1l1l1ll_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡣࡰ࡯ࡰࡥࡳࡪࠧ༂"), None) or bstack1l1l1ll_opy_ (u"ࠧࠨ༃")
          }
        if not hasattr(thread_local, bstack1l1l1ll_opy_ (u"ࠨࡤࡤࡷࡪࡥࡡࡱࡲࡢࡥ࠶࠷ࡹࡠࡵࡦࡶ࡮ࡶࡴࠨ༄")):
            scripts = {bstack1l1l1ll_opy_ (u"ࠩࡶࡧࡦࡴࠧ༅"): bstack1lll11l1l1_opy_.perform_scan}
            thread_local.base_app_a11y_script = scripts
        bstack1lll111lll_opy_ = copy.deepcopy(thread_local.base_app_a11y_script)
        bstack1lll111lll_opy_[bstack1l1l1ll_opy_ (u"ࠪࡷࡨࡧ࡮ࠨ༆")] = bstack1lll111lll_opy_[bstack1l1l1ll_opy_ (u"ࠫࡸࡩࡡ࡯ࠩ༇")] % json.dumps(bstack11l1l11l1l_opy_)
        bstack1lll11l1l1_opy_.bstack1l111l1111_opy_(bstack1lll111lll_opy_)
        bstack1lll11l1l1_opy_.store()
        bstack1llll11111_opy_ = driver.execute_script(bstack1lll11l1l1_opy_.perform_scan)
      except Exception as bstack11ll1ll1l_opy_:
        logger.info(bstack1l1l1ll_opy_ (u"ࠧࡇࡰࡱ࡫ࡸࡱࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡣࡢࡰࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࠧ༈") + str(bstack11ll1ll1l_opy_))
        bstack1llll11111_opy_ = {bstack1l1l1ll_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ༉"): str(bstack11ll1ll1l_opy_)}
    else:
      bstack1llll11111_opy_ = driver.execute_async_script(bstack1lll11l1l1_opy_.perform_scan, {bstack1l1l1ll_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪࠧ༊"): kwargs.get(bstack1l1l1ll_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࡠࡥࡲࡱࡲࡧ࡮ࡥࠩ་"), None) or bstack1l1l1ll_opy_ (u"ࠩࠪ༌")})
    return bstack1llll11111_opy_
  except Exception as err:
    logger.error(bstack1l1l1ll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡲࡶࡰࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮࠯ࠢࡾࢁࠧ།").format(str(err)))
    return {}