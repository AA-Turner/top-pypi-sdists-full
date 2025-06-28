# coding: UTF-8
import sys
bstack1l1l11l_opy_ = sys.version_info [0] == 2
bstack1ll11l_opy_ = 2048
bstack1l11ll1_opy_ = 7
def bstack1l1ll1_opy_ (bstack111ll1l_opy_):
    global bstack111ll1_opy_
    bstack11ll1ll_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack1l11ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11l1l11_opy_ = bstack11ll1ll_opy_ % len (bstack1l11ll_opy_)
    bstack11ll1_opy_ = bstack1l11ll_opy_ [:bstack11l1l11_opy_] + bstack1l11ll_opy_ [bstack11l1l11_opy_:]
    if bstack1l1l11l_opy_:
        bstack111ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack111ll11_opy_ = str () .join ([chr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack111ll11_opy_)
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
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import json
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from browserstack_sdk.bstack111llll1l_opy_ import bstack1l1lll1ll_opy_
from browserstack_sdk.bstack1lll111l11_opy_ import *
import time
import requests
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.measure import measure
def bstack1l1111111l_opy_():
  global CONFIG
  headers = {
        bstack1l1ll1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack1l1ll1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack11l111ll_opy_(CONFIG, bstack11llll1lll_opy_)
  try:
    response = requests.get(bstack11llll1lll_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1111l11l1_opy_ = response.json()[bstack1l1ll1_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1l111l1111_opy_.format(response.json()))
      return bstack1111l11l1_opy_
    else:
      logger.debug(bstack111ll1l11_opy_.format(bstack1l1ll1_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack111ll1l11_opy_.format(e))
def bstack1ll11ll11_opy_(hub_url):
  global CONFIG
  url = bstack1l1ll1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack1l1ll1_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack1l1ll1_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack1l1ll1_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack11l111ll_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1l1l11ll1_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1llll11l1_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack1ll11ll1l_opy_, stage=STAGE.bstack1l1ll11ll1_opy_)
def bstack1ll111lll1_opy_():
  try:
    global bstack1l1ll1l11l_opy_
    bstack1111l11l1_opy_ = bstack1l1111111l_opy_()
    bstack1l111lll11_opy_ = []
    results = []
    for bstack11lllllll1_opy_ in bstack1111l11l1_opy_:
      bstack1l111lll11_opy_.append(bstack1lll11l1_opy_(target=bstack1ll11ll11_opy_,args=(bstack11lllllll1_opy_,)))
    for t in bstack1l111lll11_opy_:
      t.start()
    for t in bstack1l111lll11_opy_:
      results.append(t.join())
    bstack1lll1l111l_opy_ = {}
    for item in results:
      hub_url = item[bstack1l1ll1_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack1l1ll1_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack1lll1l111l_opy_[hub_url] = latency
    bstack1llll1l1l1_opy_ = min(bstack1lll1l111l_opy_, key= lambda x: bstack1lll1l111l_opy_[x])
    bstack1l1ll1l11l_opy_ = bstack1llll1l1l1_opy_
    logger.debug(bstack1lllll111_opy_.format(bstack1llll1l1l1_opy_))
  except Exception as e:
    logger.debug(bstack11lll1l11l_opy_.format(e))
from browserstack_sdk.bstack1l11l1l1ll_opy_ import *
from browserstack_sdk.bstack1111ll1l_opy_ import *
from browserstack_sdk.bstack1l11l1l1l1_opy_ import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.bstack11lll1ll_opy_ import get_logger
from bstack_utils.measure import measure
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack11llll1l_opy_, stage=STAGE.bstack1l1ll11ll1_opy_)
def bstack1ll1lll111_opy_():
    global bstack1l1ll1l11l_opy_
    try:
        bstack11l1l1lll1_opy_ = bstack11ll1lll1l_opy_()
        bstack1l11l1ll1l_opy_(bstack11l1l1lll1_opy_)
        hub_url = bstack11l1l1lll1_opy_.get(bstack1l1ll1_opy_ (u"ࠨࡵࡳ࡮ࠥࢀ"), bstack1l1ll1_opy_ (u"ࠢࠣࢁ"))
        if hub_url.endswith(bstack1l1ll1_opy_ (u"ࠨ࠱ࡺࡨ࠴࡮ࡵࡣࠩࢂ")):
            hub_url = hub_url.rsplit(bstack1l1ll1_opy_ (u"ࠩ࠲ࡻࡩ࠵ࡨࡶࡤࠪࢃ"), 1)[0]
        if hub_url.startswith(bstack1l1ll1_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫࢄ")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack1l1ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࠭ࢅ")):
            hub_url = hub_url[8:]
        bstack1l1ll1l11l_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack11ll1lll1l_opy_():
    global CONFIG
    bstack11l111111_opy_ = CONFIG.get(bstack1l1ll1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢆ"), {}).get(bstack1l1ll1_opy_ (u"࠭ࡧࡳ࡫ࡧࡒࡦࡳࡥࠨࢇ"), bstack1l1ll1_opy_ (u"ࠧࡏࡑࡢࡋࡗࡏࡄࡠࡐࡄࡑࡊࡥࡐࡂࡕࡖࡉࡉ࠭࢈"))
    if not isinstance(bstack11l111111_opy_, str):
        raise ValueError(bstack1l1ll1_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡈࡴ࡬ࡨࠥࡴࡡ࡮ࡧࠣࡱࡺࡹࡴࠡࡤࡨࠤࡦࠦࡶࡢ࡮࡬ࡨࠥࡹࡴࡳ࡫ࡱ࡫ࠧࢉ"))
    try:
        bstack11l1l1lll1_opy_ = bstack1l1l11l1_opy_(bstack11l111111_opy_)
        return bstack11l1l1lll1_opy_
    except Exception as e:
        logger.error(bstack1l1ll1_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣࢊ").format(str(e)))
        return {}
def bstack1l1l11l1_opy_(bstack11l111111_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack1l1ll1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࢋ")] or not CONFIG[bstack1l1ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧࢌ")]:
            raise ValueError(bstack1l1ll1_opy_ (u"ࠧࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠠࡰࡴࠣࡥࡨࡩࡥࡴࡵࠣ࡯ࡪࡿࠢࢍ"))
        url = bstack11lll1111_opy_ + bstack11l111111_opy_
        auth = (CONFIG[bstack1l1ll1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨࢎ")], CONFIG[bstack1l1ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ࢏")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack1ll1lll11l_opy_ = json.loads(response.text)
            return bstack1ll1lll11l_opy_
    except ValueError as ve:
        logger.error(bstack1l1ll1_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣ࢐").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack1l1ll1_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥ࡭ࡲࡪࡦࠣࡨࡪࡺࡡࡪ࡮ࡶࠤ࠿ࠦࡻࡾࠤ࢑").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack1l11l1ll1l_opy_(bstack11lll1l1l_opy_):
    global CONFIG
    if bstack1l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ࢒") not in CONFIG or str(CONFIG[bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ࢓")]).lower() == bstack1l1ll1_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ࢔"):
        CONFIG[bstack1l1ll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬ࢕")] = False
    elif bstack1l1ll1_opy_ (u"ࠧࡪࡵࡗࡶ࡮ࡧ࡬ࡈࡴ࡬ࡨࠬ࢖") in bstack11lll1l1l_opy_:
        bstack111l111l1_opy_ = CONFIG.get(bstack1l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢗ"), {})
        logger.debug(bstack1l1ll1_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡰࡴࡩࡡ࡭ࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࠪࡹࠢ࢘"), bstack111l111l1_opy_)
        bstack1ll11l1l1_opy_ = bstack11lll1l1l_opy_.get(bstack1l1ll1_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡕࡩࡵ࡫ࡡࡵࡧࡵࡷ࢙ࠧ"), [])
        bstack1l11l1l11l_opy_ = bstack1l1ll1_opy_ (u"ࠦ࠱ࠨ࢚").join(bstack1ll11l1l1_opy_)
        logger.debug(bstack1l1ll1_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡈࡻࡳࡵࡱࡰࠤࡷ࡫ࡰࡦࡣࡷࡩࡷࠦࡳࡵࡴ࡬ࡲ࡬ࡀࠠࠦࡵ࢛ࠥ"), bstack1l11l1l11l_opy_)
        bstack1lll1111l_opy_ = {
            bstack1l1ll1_opy_ (u"ࠨ࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣ࢜"): bstack1l1ll1_opy_ (u"ࠢࡢࡶࡶ࠱ࡷ࡫ࡰࡦࡣࡷࡩࡷࠨ࢝"),
            bstack1l1ll1_opy_ (u"ࠣࡨࡲࡶࡨ࡫ࡌࡰࡥࡤࡰࠧ࢞"): bstack1l1ll1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ࢟"),
            bstack1l1ll1_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠧࢠ"): bstack1l11l1l11l_opy_
        }
        bstack111l111l1_opy_.update(bstack1lll1111l_opy_)
        logger.debug(bstack1l1ll1_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼࡙ࠣࡵࡪࡡࡵࡧࡧࠤࡱࡵࡣࡢ࡮ࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࠫࡳࠣࢡ"), bstack111l111l1_opy_)
        CONFIG[bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢢ")] = bstack111l111l1_opy_
        logger.debug(bstack1l1ll1_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡌࡩ࡯ࡣ࡯ࠤࡈࡕࡎࡇࡋࡊ࠾ࠥࠫࡳࠣࢣ"), CONFIG)
def bstack1l1l1ll1l_opy_():
    bstack11l1l1lll1_opy_ = bstack11ll1lll1l_opy_()
    if not bstack11l1l1lll1_opy_[bstack1l1ll1_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࡙ࡷࡲࠧࢤ")]:
      raise ValueError(bstack1l1ll1_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࡚ࡸ࡬ࠡ࡫ࡶࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࡬ࡲࡰ࡯ࠣ࡫ࡷ࡯ࡤࠡࡦࡨࡸࡦ࡯࡬ࡴ࠰ࠥࢥ"))
    return bstack11l1l1lll1_opy_[bstack1l1ll1_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࡛ࡲ࡭ࠩࢦ")] + bstack1l1ll1_opy_ (u"ࠪࡃࡨࡧࡰࡴ࠿ࠪࢧ")
@measure(event_name=EVENTS.bstack11llllllll_opy_, stage=STAGE.bstack1l1ll11ll1_opy_)
def bstack11111lll_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack1l1ll1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ࢨ")], CONFIG[bstack1l1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࢩ")])
        url = bstack11lll1llll_opy_
        logger.debug(bstack1l1ll1_opy_ (u"ࠨࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬ࡲࡰ࡯ࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡗࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࠦࡁࡑࡋࠥࢪ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack1l1ll1_opy_ (u"ࠢࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪࠨࢫ"): bstack1l1ll1_opy_ (u"ࠣࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠦࢬ")})
            if response.status_code == 200:
                bstack111l11111_opy_ = json.loads(response.text)
                bstack1l1lll11l_opy_ = bstack111l11111_opy_.get(bstack1l1ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡴࠩࢭ"), [])
                if bstack1l1lll11l_opy_:
                    bstack1ll111l1l_opy_ = bstack1l1lll11l_opy_[0]
                    build_hashed_id = bstack1ll111l1l_opy_.get(bstack1l1ll1_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ࢮ"))
                    bstack1l1ll11l1l_opy_ = bstack1111ll11_opy_ + build_hashed_id
                    result.extend([build_hashed_id, bstack1l1ll11l1l_opy_])
                    logger.info(bstack11l1l11lll_opy_.format(bstack1l1ll11l1l_opy_))
                    bstack11ll11l1l1_opy_ = CONFIG[bstack1l1ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧࢯ")]
                    if bstack1l1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢰ") in CONFIG:
                      bstack11ll11l1l1_opy_ += bstack1l1ll1_opy_ (u"࠭ࠠࠨࢱ") + CONFIG[bstack1l1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࢲ")]
                    if bstack11ll11l1l1_opy_ != bstack1ll111l1l_opy_.get(bstack1l1ll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ࢳ")):
                      logger.debug(bstack11ll11l11_opy_.format(bstack1ll111l1l_opy_.get(bstack1l1ll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧࢴ")), bstack11ll11l1l1_opy_))
                    return result
                else:
                    logger.debug(bstack1l1ll1_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡑࡳࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡵࡪࡨࠤࡷ࡫ࡳࡱࡱࡱࡷࡪ࠴ࠢࢵ"))
            else:
                logger.debug(bstack1l1ll1_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢶ"))
        except Exception as e:
            logger.error(bstack1l1ll1_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࡹࠠ࠻ࠢࡾࢁࠧࢷ").format(str(e)))
    else:
        logger.debug(bstack1l1ll1_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡉࡏࡏࡈࡌࡋࠥ࡯ࡳࠡࡰࡲࡸࠥࡹࡥࡵ࠰࡙ࠣࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢸ"))
    return [None, None]
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1l1l111l_opy_ import bstack1l1l111l_opy_, bstack1l11111l1l_opy_, bstack1lll1111ll_opy_, bstack1l1l1lll1l_opy_
from bstack_utils.measure import bstack1l11l1llll_opy_
from bstack_utils.measure import measure
from bstack_utils.percy import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1ll1l1ll1_opy_ import bstack11ll1lll_opy_
from bstack_utils.messages import *
from bstack_utils import bstack11lll1ll_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack11l1ll11l1_opy_, bstack1l1ll1ll1l_opy_, bstack111lll1l1_opy_, bstack11l1ll11ll_opy_, \
  bstack11ll1ll11_opy_, \
  Notset, bstack1l1l111l11_opy_, \
  bstack1ll111ll1l_opy_, bstack1l1l11l111_opy_, bstack111ll1lll_opy_, bstack11ll11ll1_opy_, bstack1ll11l111l_opy_, bstack11l1l1l1l_opy_, \
  bstack111111l1_opy_, \
  bstack11ll11l11l_opy_, bstack1l11lll11l_opy_, bstack1l11l1ll1_opy_, bstack1llllll1l1_opy_, \
  bstack11lll11l1_opy_, bstack1ll1ll1l_opy_, bstack11lll1lll1_opy_, bstack111l11ll1_opy_
from bstack_utils.bstack11l11lll1_opy_ import bstack1l11l1l1_opy_
from bstack_utils.bstack1l111l11l1_opy_ import bstack11l111l1_opy_, bstack11ll1l1l11_opy_
from bstack_utils.bstack1ll11ll1_opy_ import bstack11l1l1111_opy_
from bstack_utils.bstack1llll1111l_opy_ import bstack1l1ll1lll1_opy_, bstack1ll1111l11_opy_
from bstack_utils.bstack1ll1l1l1l_opy_ import bstack1ll1l1l1l_opy_
from bstack_utils.bstack1111ll1l1_opy_ import bstack11ll11l111_opy_
from bstack_utils.proxy import bstack11l1l11ll1_opy_, bstack11l111ll_opy_, bstack11l1lll11_opy_, bstack1l1lll111l_opy_
from bstack_utils.bstack111l1l1l_opy_ import bstack1l111l1lll_opy_
import bstack_utils.bstack11l11lllll_opy_ as bstack1lllll11_opy_
import bstack_utils.bstack1ll11lll1l_opy_ as bstack11ll1lll1_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.utils.bstack1llll11l_opy_ import bstack1l1ll11l11_opy_
from bstack_utils.bstack111l11ll_opy_ import bstack11l1ll1l1_opy_
from bstack_utils.bstack11lllll1l_opy_ import bstack1l11ll1111_opy_
if os.getenv(bstack1l1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡌࡔࡕࡋࡔࠩࢹ")):
  cli.bstack11ll111111_opy_()
else:
  os.environ[bstack1l1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡍࡕࡏࡌࡕࠪࢺ")] = bstack1l1ll1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧࢻ")
bstack11ll11l1ll_opy_ = bstack1l1ll1_opy_ (u"ࠪࠤࠥ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࠣࠤ࡮࡬ࠨࡱࡣࡪࡩࠥࡃ࠽࠾ࠢࡹࡳ࡮ࡪࠠ࠱ࠫࠣࡿࡡࡴࠠࠡࠢࡷࡶࡾࢁ࡜࡯ࠢࡦࡳࡳࡹࡴࠡࡨࡶࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨ࡝ࠩࡩࡷࡡ࠭ࠩ࠼࡞ࡱࠤࠥࠦࠠࠡࡨࡶ࠲ࡦࡶࡰࡦࡰࡧࡊ࡮ࡲࡥࡔࡻࡱࡧ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪ࠯ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡶ࡟ࡪࡰࡧࡩࡽ࠯ࠠࠬࠢࠥ࠾ࠧࠦࠫࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࠨࡢࡹࡤ࡭ࡹࠦ࡮ࡦࡹࡓࡥ࡬࡫࠲࠯ࡧࡹࡥࡱࡻࡡࡵࡧࠫࠦ࠭࠯ࠠ࠾ࡀࠣࡿࢂࠨࠬࠡ࡞ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥ࡫ࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡄࡦࡶࡤ࡭ࡱࡹࠢࡾ࡞ࠪ࠭࠮࠯࡛ࠣࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠦࡢ࠯ࠠࠬࠢࠥ࠰ࡡࡢ࡮ࠣࠫ࡟ࡲࠥࠦࠠࠡࡿࡦࡥࡹࡩࡨࠩࡧࡻ࠭ࢀࡢ࡮ࠡࠢࠣࠤࢂࡢ࡮ࠡࠢࢀࡠࡳࠦࠠ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱ࠪࢼ")
bstack1l1l11lll_opy_ = bstack1l1ll1_opy_ (u"ࠫࡡࡴ࠯ࠫࠢࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࠦࠪ࠰࡞ࡱࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠶ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡩࡡࡱࡵࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠷࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡲࡢ࡭ࡳࡪࡥࡹࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠷ࡣ࡜࡯ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯ࡵ࡯࡭ࡨ࡫ࠨ࠱࠮ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸࠯࡜࡯ࡥࡲࡲࡸࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯ࠥࡃࠠࡳࡧࡴࡹ࡮ࡸࡥࠩࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨࠩ࠼࡞ࡱ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡰࡦࡻ࡮ࡤࡪࠣࡁࠥࡧࡳࡺࡰࡦࠤ࠭ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷ࠮ࠦ࠽࠿ࠢࡾࡠࡳࡲࡥࡵࠢࡦࡥࡵࡹ࠻࡝ࡰࡷࡶࡾࠦࡻ࡝ࡰࡦࡥࡵࡹࠠ࠾ࠢࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࡢࡴࡶࡤࡧࡰࡥࡣࡢࡲࡶ࠭ࡡࡴࠠࠡࡿࠣࡧࡦࡺࡣࡩࠪࡨࡼ࠮ࠦࡻ࡝ࡰࠣࠤࠥࠦࡽ࡝ࡰࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࠻ࠢࡣࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠩࢁࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭ࢂࡦࠬ࡝ࡰࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴ࡞ࡱࠤࠥࢃࠩ࡝ࡰࢀࡠࡳ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࠪࢽ")
from ._version import __version__
bstack1l1l111l1_opy_ = None
CONFIG = {}
bstack1l1ll1l111_opy_ = {}
bstack1l11l111l_opy_ = {}
bstack1l11l11ll_opy_ = None
bstack11l1lll1l_opy_ = None
bstack11111ll1_opy_ = None
bstack111l1111_opy_ = -1
bstack1l111l11_opy_ = 0
bstack111111l11_opy_ = bstack11lll111_opy_
bstack1l1l11l11l_opy_ = 1
bstack11111ll1l_opy_ = False
bstack111lllll1_opy_ = False
bstack1l11lll1l_opy_ = bstack1l1ll1_opy_ (u"ࠬ࠭ࢾ")
bstack1111ll11l_opy_ = bstack1l1ll1_opy_ (u"࠭ࠧࢿ")
bstack1l1lllllll_opy_ = False
bstack11l11l111_opy_ = True
bstack1ll1ll1l1_opy_ = bstack1l1ll1_opy_ (u"ࠧࠨࣀ")
bstack1ll1l11lll_opy_ = []
bstack1l1ll1l11l_opy_ = bstack1l1ll1_opy_ (u"ࠨࠩࣁ")
bstack11l1l1ll11_opy_ = False
bstack11l11lll1l_opy_ = None
bstack111l1lll_opy_ = None
bstack1l11lll1l1_opy_ = None
bstack11ll111ll1_opy_ = -1
bstack1l1l1lll11_opy_ = os.path.join(os.path.expanduser(bstack1l1ll1_opy_ (u"ࠩࢁࠫࣂ")), bstack1l1ll1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪࣃ"), bstack1l1ll1_opy_ (u"ࠫ࠳ࡸ࡯ࡣࡱࡷ࠱ࡷ࡫ࡰࡰࡴࡷ࠱࡭࡫࡬ࡱࡧࡵ࠲࡯ࡹ࡯࡯ࠩࣄ"))
bstack11ll1l11ll_opy_ = 0
bstack1l1lll1111_opy_ = 0
bstack1l1llll1l_opy_ = []
bstack1l1111ll_opy_ = []
bstack1ll1ll111_opy_ = []
bstack1l1ll111ll_opy_ = []
bstack11l1ll1l1l_opy_ = bstack1l1ll1_opy_ (u"ࠬ࠭ࣅ")
bstack11lll111l1_opy_ = bstack1l1ll1_opy_ (u"࠭ࠧࣆ")
bstack1l111llll1_opy_ = False
bstack11l1ll1ll1_opy_ = False
bstack1ll111l11_opy_ = {}
bstack11llllll11_opy_ = None
bstack111l11l1l_opy_ = None
bstack1ll111111l_opy_ = None
bstack1ll1ll1ll_opy_ = None
bstack1ll1llll1_opy_ = None
bstack11lllll11_opy_ = None
bstack1lll11111_opy_ = None
bstack11l111l1l1_opy_ = None
bstack1l111lll1l_opy_ = None
bstack11l1111l11_opy_ = None
bstack11l1l11ll_opy_ = None
bstack1lll1llll_opy_ = None
bstack11ll11lll1_opy_ = None
bstack1lll1ll11_opy_ = None
bstack11lllll1_opy_ = None
bstack1lll1lll1l_opy_ = None
bstack1l11l1lll_opy_ = None
bstack1lll111111_opy_ = None
bstack1l1lll1l11_opy_ = None
bstack11l11l1ll1_opy_ = None
bstack11l1111l1_opy_ = None
bstack1l11111111_opy_ = None
bstack1l11111l11_opy_ = None
thread_local = threading.local()
bstack1ll1ll1l11_opy_ = False
bstack1ll11ll11l_opy_ = bstack1l1ll1_opy_ (u"ࠢࠣࣇ")
logger = bstack11lll1ll_opy_.get_logger(__name__, bstack111111l11_opy_)
bstack11lll111ll_opy_ = Config.bstack11ll1l11l_opy_()
percy = bstack11llll1111_opy_()
bstack1lll11l1l1_opy_ = bstack11ll1lll_opy_()
bstack1ll1111l1_opy_ = bstack1l11l1l1l1_opy_()
def bstack1lll1lll1_opy_():
  global CONFIG
  global bstack1l111llll1_opy_
  global bstack11lll111ll_opy_
  testContextOptions = bstack1l1llll1_opy_(CONFIG)
  if bstack11ll1ll11_opy_(CONFIG):
    if (bstack1l1ll1_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪࣈ") in testContextOptions and str(testContextOptions[bstack1l1ll1_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫࣉ")]).lower() == bstack1l1ll1_opy_ (u"ࠪࡸࡷࡻࡥࠨ࣊")):
      bstack1l111llll1_opy_ = True
    bstack11lll111ll_opy_.bstack1lll111l1l_opy_(testContextOptions.get(bstack1l1ll1_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ࣋"), False))
  else:
    bstack1l111llll1_opy_ = True
    bstack11lll111ll_opy_.bstack1lll111l1l_opy_(True)
def bstack1llll111ll_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1111l1l1l_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l11l1lll1_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1l1ll1_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡩ࡯࡯ࡨ࡬࡫࡫࡯࡬ࡦࠤ࣌") == args[i].lower() or bstack1l1ll1_opy_ (u"ࠨ࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡪ࡮࡭ࠢ࣍") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1ll1ll1l1_opy_
      bstack1ll1ll1l1_opy_ += bstack1l1ll1_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠤࠧ࠭࣎") + path + bstack1l1ll1_opy_ (u"ࠨࠤ࣏ࠪ")
      return path
  return None
bstack11l1llll_opy_ = re.compile(bstack1l1ll1_opy_ (u"ࡴࠥ࠲࠯ࡅ࡜ࠥࡽࠫ࠲࠯ࡅࠩࡾ࠰࠭ࡃ࣐ࠧ"))
def bstack11l1ll11_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack11l1llll_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack1l1ll1_opy_ (u"ࠥࠨࢀࠨ࣑") + group + bstack1l1ll1_opy_ (u"ࠦࢂࠨ࣒"), os.environ.get(group))
  return value
def bstack11llll111_opy_():
  global bstack1l11111l11_opy_
  if bstack1l11111l11_opy_ is None:
        bstack1l11111l11_opy_ = bstack1l11l1lll1_opy_()
  bstack1lll11ll1_opy_ = bstack1l11111l11_opy_
  if bstack1lll11ll1_opy_ and os.path.exists(os.path.abspath(bstack1lll11ll1_opy_)):
    fileName = bstack1lll11ll1_opy_
  if bstack1l1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆ࣓ࠩ") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack1l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࡤࡌࡉࡍࡇࠪࣔ")])) and not bstack1l1ll1_opy_ (u"ࠧࡧ࡫࡯ࡩࡓࡧ࡭ࡦࠩࣕ") in locals():
    fileName = os.environ[bstack1l1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬࣖ")]
  if bstack1l1ll1_opy_ (u"ࠩࡩ࡭ࡱ࡫ࡎࡢ࡯ࡨࠫࣗ") in locals():
    bstack1llllll1_opy_ = os.path.abspath(fileName)
  else:
    bstack1llllll1_opy_ = bstack1l1ll1_opy_ (u"ࠪࠫࣘ")
  bstack1l11ll1l1l_opy_ = os.getcwd()
  bstack1llll1l1l_opy_ = bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧࣙ")
  bstack1ll1ll11ll_opy_ = bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡧ࡭࡭ࠩࣚ")
  while (not os.path.exists(bstack1llllll1_opy_)) and bstack1l11ll1l1l_opy_ != bstack1l1ll1_opy_ (u"ࠨࠢࣛ"):
    bstack1llllll1_opy_ = os.path.join(bstack1l11ll1l1l_opy_, bstack1llll1l1l_opy_)
    if not os.path.exists(bstack1llllll1_opy_):
      bstack1llllll1_opy_ = os.path.join(bstack1l11ll1l1l_opy_, bstack1ll1ll11ll_opy_)
    if bstack1l11ll1l1l_opy_ != os.path.dirname(bstack1l11ll1l1l_opy_):
      bstack1l11ll1l1l_opy_ = os.path.dirname(bstack1l11ll1l1l_opy_)
    else:
      bstack1l11ll1l1l_opy_ = bstack1l1ll1_opy_ (u"ࠢࠣࣜ")
  bstack1l11111l11_opy_ = bstack1llllll1_opy_ if os.path.exists(bstack1llllll1_opy_) else None
  return bstack1l11111l11_opy_
def bstack1l1l1ll11l_opy_():
  bstack1llllll1_opy_ = bstack11llll111_opy_()
  if not os.path.exists(bstack1llllll1_opy_):
    bstack1ll1ll11_opy_(
      bstack1l1111ll1_opy_.format(os.getcwd()))
  try:
    with open(bstack1llllll1_opy_, bstack1l1ll1_opy_ (u"ࠨࡴࠪࣝ")) as stream:
      yaml.add_implicit_resolver(bstack1l1ll1_opy_ (u"ࠤࠤࡴࡦࡺࡨࡦࡺࠥࣞ"), bstack11l1llll_opy_)
      yaml.add_constructor(bstack1l1ll1_opy_ (u"ࠥࠥࡵࡧࡴࡩࡧࡻࠦࣟ"), bstack11l1ll11_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack1llllll1_opy_, bstack1l1ll1_opy_ (u"ࠫࡷ࠭࣠")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack1ll1ll11_opy_(bstack1ll1111l1l_opy_.format(str(exc)))
def bstack1l1lll1l1l_opy_(config):
  bstack1lll11l111_opy_ = bstack1l11l11ll1_opy_(config)
  for option in list(bstack1lll11l111_opy_):
    if option.lower() in bstack1l1ll1ll1_opy_ and option != bstack1l1ll1ll1_opy_[option.lower()]:
      bstack1lll11l111_opy_[bstack1l1ll1ll1_opy_[option.lower()]] = bstack1lll11l111_opy_[option]
      del bstack1lll11l111_opy_[option]
  return config
def bstack1l11ll1l_opy_():
  global bstack1l11l111l_opy_
  for key, bstack11ll1ll11l_opy_ in bstack1l1lllll_opy_.items():
    if isinstance(bstack11ll1ll11l_opy_, list):
      for var in bstack11ll1ll11l_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1l11l111l_opy_[key] = os.environ[var]
          break
    elif bstack11ll1ll11l_opy_ in os.environ and os.environ[bstack11ll1ll11l_opy_] and str(os.environ[bstack11ll1ll11l_opy_]).strip():
      bstack1l11l111l_opy_[key] = os.environ[bstack11ll1ll11l_opy_]
  if bstack1l1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ࣡") in os.environ:
    bstack1l11l111l_opy_[bstack1l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ࣢")] = {}
    bstack1l11l111l_opy_[bstack1l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࣣࠫ")][bstack1l1ll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣤ")] = os.environ[bstack1l1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫࣥ")]
def bstack11ll1l111l_opy_():
  global bstack1l1ll1l111_opy_
  global bstack1ll1ll1l1_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack1l1ll1_opy_ (u"ࠪ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࣦ࠭").lower() == val.lower():
      bstack1l1ll1l111_opy_[bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣧ")] = {}
      bstack1l1ll1l111_opy_[bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣨ")][bstack1l1ll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣩ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack1lllll1111_opy_ in bstack11llll1ll1_opy_.items():
    if isinstance(bstack1lllll1111_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1lllll1111_opy_:
          if idx < len(sys.argv) and bstack1l1ll1_opy_ (u"ࠧ࠮࠯ࠪ࣪") + var.lower() == val.lower() and not key in bstack1l1ll1l111_opy_:
            bstack1l1ll1l111_opy_[key] = sys.argv[idx + 1]
            bstack1ll1ll1l1_opy_ += bstack1l1ll1_opy_ (u"ࠨࠢ࠰࠱ࠬ࣫") + var + bstack1l1ll1_opy_ (u"ࠩࠣࠫ࣬") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack1l1ll1_opy_ (u"ࠪ࠱࠲࣭࠭") + bstack1lllll1111_opy_.lower() == val.lower() and not key in bstack1l1ll1l111_opy_:
          bstack1l1ll1l111_opy_[key] = sys.argv[idx + 1]
          bstack1ll1ll1l1_opy_ += bstack1l1ll1_opy_ (u"ࠫࠥ࠳࠭ࠨ࣮") + bstack1lllll1111_opy_ + bstack1l1ll1_opy_ (u"࣯ࠬࠦࠧ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1l1l1l1l1l_opy_(config):
  bstack1l1l1l11_opy_ = config.keys()
  for bstack1ll11l1111_opy_, bstack1l11ll1l11_opy_ in bstack11ll11ll11_opy_.items():
    if bstack1l11ll1l11_opy_ in bstack1l1l1l11_opy_:
      config[bstack1ll11l1111_opy_] = config[bstack1l11ll1l11_opy_]
      del config[bstack1l11ll1l11_opy_]
  for bstack1ll11l1111_opy_, bstack1l11ll1l11_opy_ in bstack11ll1l1ll1_opy_.items():
    if isinstance(bstack1l11ll1l11_opy_, list):
      for bstack1l1111ll11_opy_ in bstack1l11ll1l11_opy_:
        if bstack1l1111ll11_opy_ in bstack1l1l1l11_opy_:
          config[bstack1ll11l1111_opy_] = config[bstack1l1111ll11_opy_]
          del config[bstack1l1111ll11_opy_]
          break
    elif bstack1l11ll1l11_opy_ in bstack1l1l1l11_opy_:
      config[bstack1ll11l1111_opy_] = config[bstack1l11ll1l11_opy_]
      del config[bstack1l11ll1l11_opy_]
  for bstack1l1111ll11_opy_ in list(config):
    for bstack11l111l11_opy_ in bstack11ll11111_opy_:
      if bstack1l1111ll11_opy_.lower() == bstack11l111l11_opy_.lower() and bstack1l1111ll11_opy_ != bstack11l111l11_opy_:
        config[bstack11l111l11_opy_] = config[bstack1l1111ll11_opy_]
        del config[bstack1l1111ll11_opy_]
  bstack1l11l111_opy_ = [{}]
  if not config.get(bstack1l1ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࣰࠩ")):
    config[bstack1l1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࣱࠪ")] = [{}]
  bstack1l11l111_opy_ = config[bstack1l1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࣲࠫ")]
  for platform in bstack1l11l111_opy_:
    for bstack1l1111ll11_opy_ in list(platform):
      for bstack11l111l11_opy_ in bstack11ll11111_opy_:
        if bstack1l1111ll11_opy_.lower() == bstack11l111l11_opy_.lower() and bstack1l1111ll11_opy_ != bstack11l111l11_opy_:
          platform[bstack11l111l11_opy_] = platform[bstack1l1111ll11_opy_]
          del platform[bstack1l1111ll11_opy_]
  for bstack1ll11l1111_opy_, bstack1l11ll1l11_opy_ in bstack11ll1l1ll1_opy_.items():
    for platform in bstack1l11l111_opy_:
      if isinstance(bstack1l11ll1l11_opy_, list):
        for bstack1l1111ll11_opy_ in bstack1l11ll1l11_opy_:
          if bstack1l1111ll11_opy_ in platform:
            platform[bstack1ll11l1111_opy_] = platform[bstack1l1111ll11_opy_]
            del platform[bstack1l1111ll11_opy_]
            break
      elif bstack1l11ll1l11_opy_ in platform:
        platform[bstack1ll11l1111_opy_] = platform[bstack1l11ll1l11_opy_]
        del platform[bstack1l11ll1l11_opy_]
  for bstack1111111l1_opy_ in bstack1l111ll111_opy_:
    if bstack1111111l1_opy_ in config:
      if not bstack1l111ll111_opy_[bstack1111111l1_opy_] in config:
        config[bstack1l111ll111_opy_[bstack1111111l1_opy_]] = {}
      config[bstack1l111ll111_opy_[bstack1111111l1_opy_]].update(config[bstack1111111l1_opy_])
      del config[bstack1111111l1_opy_]
  for platform in bstack1l11l111_opy_:
    for bstack1111111l1_opy_ in bstack1l111ll111_opy_:
      if bstack1111111l1_opy_ in list(platform):
        if not bstack1l111ll111_opy_[bstack1111111l1_opy_] in platform:
          platform[bstack1l111ll111_opy_[bstack1111111l1_opy_]] = {}
        platform[bstack1l111ll111_opy_[bstack1111111l1_opy_]].update(platform[bstack1111111l1_opy_])
        del platform[bstack1111111l1_opy_]
  config = bstack1l1lll1l1l_opy_(config)
  return config
def bstack1l1111ll1l_opy_(config):
  global bstack1111ll11l_opy_
  bstack1ll111ll_opy_ = False
  if bstack1l1ll1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ࣳ") in config and str(config[bstack1l1ll1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧࣴ")]).lower() != bstack1l1ll1_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪࣵ"):
    if bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࣶࠩ") not in config or str(config[bstack1l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪࣷ")]).lower() == bstack1l1ll1_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ࣸ"):
      config[bstack1l1ll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࣹࠧ")] = False
    else:
      bstack11l1l1lll1_opy_ = bstack11ll1lll1l_opy_()
      if bstack1l1ll1_opy_ (u"ࠩ࡬ࡷ࡙ࡸࡩࡢ࡮ࡊࡶ࡮ࡪࣺࠧ") in bstack11l1l1lll1_opy_:
        if not bstack1l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࣻ") in config:
          config[bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣼ")] = {}
        config[bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣽ")][bstack1l1ll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣾ")] = bstack1l1ll1_opy_ (u"ࠧࡢࡶࡶ࠱ࡷ࡫ࡰࡦࡣࡷࡩࡷ࠭ࣿ")
        bstack1ll111ll_opy_ = True
        bstack1111ll11l_opy_ = config[bstack1l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬऀ")].get(bstack1l1ll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫँ"))
  if bstack11ll1ll11_opy_(config) and bstack1l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧं") in config and str(config[bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨः")]).lower() != bstack1l1ll1_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫऄ") and not bstack1ll111ll_opy_:
    if not bstack1l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪअ") in config:
      config[bstack1l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫआ")] = {}
    if not config[bstack1l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬइ")].get(bstack1l1ll1_opy_ (u"ࠩࡶ࡯࡮ࡶࡂࡪࡰࡤࡶࡾࡏ࡮ࡪࡶ࡬ࡥࡱ࡯ࡳࡢࡶ࡬ࡳࡳ࠭ई")) and not bstack1l1ll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬउ") in config[bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऊ")]:
      bstack1llllll1l_opy_ = datetime.datetime.now()
      bstack1lllllll1_opy_ = bstack1llllll1l_opy_.strftime(bstack1l1ll1_opy_ (u"ࠬࠫࡤࡠࠧࡥࡣࠪࡎࠥࡎࠩऋ"))
      hostname = socket.gethostname()
      bstack11ll111ll_opy_ = bstack1l1ll1_opy_ (u"࠭ࠧऌ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1l1ll1_opy_ (u"ࠧࡼࡿࡢࡿࢂࡥࡻࡾࠩऍ").format(bstack1lllllll1_opy_, hostname, bstack11ll111ll_opy_)
      config[bstack1l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬऎ")][bstack1l1ll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫए")] = identifier
    bstack1111ll11l_opy_ = config[bstack1l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧऐ")].get(bstack1l1ll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ऑ"))
  return config
def bstack1ll11l11l_opy_():
  bstack1l1ll11lll_opy_ =  bstack11ll11ll1_opy_()[bstack1l1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠫऒ")]
  return bstack1l1ll11lll_opy_ if bstack1l1ll11lll_opy_ else -1
def bstack11ll1lll11_opy_(bstack1l1ll11lll_opy_):
  global CONFIG
  if not bstack1l1ll1_opy_ (u"࠭ࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨओ") in CONFIG[bstack1l1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऔ")]:
    return
  CONFIG[bstack1l1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪक")] = CONFIG[bstack1l1ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫख")].replace(
    bstack1l1ll1_opy_ (u"ࠪࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬग"),
    str(bstack1l1ll11lll_opy_)
  )
def bstack1l1l1l1111_opy_():
  global CONFIG
  if not bstack1l1ll1_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪघ") in CONFIG[bstack1l1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧङ")]:
    return
  bstack1llllll1l_opy_ = datetime.datetime.now()
  bstack1lllllll1_opy_ = bstack1llllll1l_opy_.strftime(bstack1l1ll1_opy_ (u"࠭ࠥࡥ࠯ࠨࡦ࠲ࠫࡈ࠻ࠧࡐࠫच"))
  CONFIG[bstack1l1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩछ")] = CONFIG[bstack1l1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪज")].replace(
    bstack1l1ll1_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨझ"),
    bstack1lllllll1_opy_
  )
def bstack1ll1111ll_opy_():
  global CONFIG
  if bstack1l1ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬञ") in CONFIG and not bool(CONFIG[bstack1l1ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ट")]):
    del CONFIG[bstack1l1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧठ")]
    return
  if not bstack1l1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨड") in CONFIG:
    CONFIG[bstack1l1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩढ")] = bstack1l1ll1_opy_ (u"ࠨࠥࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫण")
  if bstack1l1ll1_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨत") in CONFIG[bstack1l1ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬथ")]:
    bstack1l1l1l1111_opy_()
    os.environ[bstack1l1ll1_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨद")] = CONFIG[bstack1l1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧध")]
  if not bstack1l1ll1_opy_ (u"࠭ࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨन") in CONFIG[bstack1l1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऩ")]:
    return
  bstack1l1ll11lll_opy_ = bstack1l1ll1_opy_ (u"ࠨࠩप")
  bstack1l1l11l1ll_opy_ = bstack1ll11l11l_opy_()
  if bstack1l1l11l1ll_opy_ != -1:
    bstack1l1ll11lll_opy_ = bstack1l1ll1_opy_ (u"ࠩࡆࡍࠥ࠭फ") + str(bstack1l1l11l1ll_opy_)
  if bstack1l1ll11lll_opy_ == bstack1l1ll1_opy_ (u"ࠪࠫब"):
    bstack1ll111llll_opy_ = bstack1ll1l1ll_opy_(CONFIG[bstack1l1ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧभ")])
    if bstack1ll111llll_opy_ != -1:
      bstack1l1ll11lll_opy_ = str(bstack1ll111llll_opy_)
  if bstack1l1ll11lll_opy_:
    bstack11ll1lll11_opy_(bstack1l1ll11lll_opy_)
    os.environ[bstack1l1ll1_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩम")] = CONFIG[bstack1l1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨय")]
def bstack1l1l111ll1_opy_(bstack11l11111l_opy_, bstack11lll11l_opy_, path):
  bstack1ll1l1llll_opy_ = {
    bstack1l1ll1_opy_ (u"ࠧࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫर"): bstack11lll11l_opy_
  }
  if os.path.exists(path):
    bstack1lllll1l1l_opy_ = json.load(open(path, bstack1l1ll1_opy_ (u"ࠨࡴࡥࠫऱ")))
  else:
    bstack1lllll1l1l_opy_ = {}
  bstack1lllll1l1l_opy_[bstack11l11111l_opy_] = bstack1ll1l1llll_opy_
  with open(path, bstack1l1ll1_opy_ (u"ࠤࡺ࠯ࠧल")) as outfile:
    json.dump(bstack1lllll1l1l_opy_, outfile)
def bstack1ll1l1ll_opy_(bstack11l11111l_opy_):
  bstack11l11111l_opy_ = str(bstack11l11111l_opy_)
  bstack11l1llll11_opy_ = os.path.join(os.path.expanduser(bstack1l1ll1_opy_ (u"ࠪࢂࠬळ")), bstack1l1ll1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫऴ"))
  try:
    if not os.path.exists(bstack11l1llll11_opy_):
      os.makedirs(bstack11l1llll11_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1l1ll1_opy_ (u"ࠬࢄࠧव")), bstack1l1ll1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭श"), bstack1l1ll1_opy_ (u"ࠧ࠯ࡤࡸ࡭ࡱࡪ࠭࡯ࡣࡰࡩ࠲ࡩࡡࡤࡪࡨ࠲࡯ࡹ࡯࡯ࠩष"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1l1ll1_opy_ (u"ࠨࡹࠪस")):
        pass
      with open(file_path, bstack1l1ll1_opy_ (u"ࠤࡺ࠯ࠧह")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1l1ll1_opy_ (u"ࠪࡶࠬऺ")) as bstack1l1l1ll111_opy_:
      bstack1lll1l11l1_opy_ = json.load(bstack1l1l1ll111_opy_)
    if bstack11l11111l_opy_ in bstack1lll1l11l1_opy_:
      bstack1lll1ll11l_opy_ = bstack1lll1l11l1_opy_[bstack11l11111l_opy_][bstack1l1ll1_opy_ (u"ࠫ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨऻ")]
      bstack11l1l1l11_opy_ = int(bstack1lll1ll11l_opy_) + 1
      bstack1l1l111ll1_opy_(bstack11l11111l_opy_, bstack11l1l1l11_opy_, file_path)
      return bstack11l1l1l11_opy_
    else:
      bstack1l1l111ll1_opy_(bstack11l11111l_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack11lll111l_opy_.format(str(e)))
    return -1
def bstack1lll11ll_opy_(config):
  if not config[bstack1l1ll1_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫़ࠧ")] or not config[bstack1l1ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩऽ")]:
    return True
  else:
    return False
def bstack1l1lllll11_opy_(config, index=0):
  global bstack1l1lllllll_opy_
  bstack1ll1lllll1_opy_ = {}
  caps = bstack111ll11l1_opy_ + bstack1llll1l11l_opy_
  if config.get(bstack1l1ll1_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫा"), False):
    bstack1ll1lllll1_opy_[bstack1l1ll1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬि")] = True
    bstack1ll1lllll1_opy_[bstack1l1ll1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ी")] = config.get(bstack1l1ll1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧु"), {})
  if bstack1l1lllllll_opy_:
    caps += bstack1ll1l111l_opy_
  for key in config:
    if key in caps + [bstack1l1ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧू")]:
      continue
    bstack1ll1lllll1_opy_[key] = config[key]
  if bstack1l1ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨृ") in config:
    for bstack1l1ll111l1_opy_ in config[bstack1l1ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩॄ")][index]:
      if bstack1l1ll111l1_opy_ in caps:
        continue
      bstack1ll1lllll1_opy_[bstack1l1ll111l1_opy_] = config[bstack1l1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪॅ")][index][bstack1l1ll111l1_opy_]
  bstack1ll1lllll1_opy_[bstack1l1ll1_opy_ (u"ࠨࡪࡲࡷࡹࡔࡡ࡮ࡧࠪॆ")] = socket.gethostname()
  if bstack1l1ll1_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪे") in bstack1ll1lllll1_opy_:
    del (bstack1ll1lllll1_opy_[bstack1l1ll1_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫै")])
  return bstack1ll1lllll1_opy_
def bstack1lll11ll1l_opy_(config):
  global bstack1l1lllllll_opy_
  bstack111l111l_opy_ = {}
  caps = bstack1llll1l11l_opy_
  if bstack1l1lllllll_opy_:
    caps += bstack1ll1l111l_opy_
  for key in caps:
    if key in config:
      bstack111l111l_opy_[key] = config[key]
  return bstack111l111l_opy_
def bstack11lll1l1_opy_(bstack1ll1lllll1_opy_, bstack111l111l_opy_):
  bstack11l11l11ll_opy_ = {}
  for key in bstack1ll1lllll1_opy_.keys():
    if key in bstack11ll11ll11_opy_:
      bstack11l11l11ll_opy_[bstack11ll11ll11_opy_[key]] = bstack1ll1lllll1_opy_[key]
    else:
      bstack11l11l11ll_opy_[key] = bstack1ll1lllll1_opy_[key]
  for key in bstack111l111l_opy_:
    if key in bstack11ll11ll11_opy_:
      bstack11l11l11ll_opy_[bstack11ll11ll11_opy_[key]] = bstack111l111l_opy_[key]
    else:
      bstack11l11l11ll_opy_[key] = bstack111l111l_opy_[key]
  return bstack11l11l11ll_opy_
def bstack11lll1l1ll_opy_(config, index=0):
  global bstack1l1lllllll_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack1llll11l11_opy_ = bstack11l1ll11l1_opy_(bstack11l1l1ll1l_opy_, config, logger)
  bstack111l111l_opy_ = bstack1lll11ll1l_opy_(config)
  bstack11lll1ll1l_opy_ = bstack1llll1l11l_opy_
  bstack11lll1ll1l_opy_ += bstack1l11l1111l_opy_
  bstack111l111l_opy_ = update(bstack111l111l_opy_, bstack1llll11l11_opy_)
  if bstack1l1lllllll_opy_:
    bstack11lll1ll1l_opy_ += bstack1ll1l111l_opy_
  if bstack1l1ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॉ") in config:
    if bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪॊ") in config[bstack1l1ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩो")][index]:
      caps[bstack1l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬौ")] = config[bstack1l1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶ्ࠫ")][index][bstack1l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧॎ")]
    if bstack1l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫॏ") in config[bstack1l1ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॐ")][index]:
      caps[bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭॑")] = str(config[bstack1l1ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴ॒ࠩ")][index][bstack1l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ॓")])
    bstack1l1l11l11_opy_ = bstack11l1ll11l1_opy_(bstack11l1l1ll1l_opy_, config[bstack1l1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ॔")][index], logger)
    bstack11lll1ll1l_opy_ += list(bstack1l1l11l11_opy_.keys())
    for bstack1l1l1l11ll_opy_ in bstack11lll1ll1l_opy_:
      if bstack1l1l1l11ll_opy_ in config[bstack1l1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॕ")][index]:
        if bstack1l1l1l11ll_opy_ == bstack1l1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬॖ"):
          try:
            bstack1l1l11l11_opy_[bstack1l1l1l11ll_opy_] = str(config[bstack1l1ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॗ")][index][bstack1l1l1l11ll_opy_] * 1.0)
          except:
            bstack1l1l11l11_opy_[bstack1l1l1l11ll_opy_] = str(config[bstack1l1ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨक़")][index][bstack1l1l1l11ll_opy_])
        else:
          bstack1l1l11l11_opy_[bstack1l1l1l11ll_opy_] = config[bstack1l1ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩख़")][index][bstack1l1l1l11ll_opy_]
        del (config[bstack1l1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪग़")][index][bstack1l1l1l11ll_opy_])
    bstack111l111l_opy_ = update(bstack111l111l_opy_, bstack1l1l11l11_opy_)
  bstack1ll1lllll1_opy_ = bstack1l1lllll11_opy_(config, index)
  for bstack1l1111ll11_opy_ in bstack1llll1l11l_opy_ + list(bstack1llll11l11_opy_.keys()):
    if bstack1l1111ll11_opy_ in bstack1ll1lllll1_opy_:
      bstack111l111l_opy_[bstack1l1111ll11_opy_] = bstack1ll1lllll1_opy_[bstack1l1111ll11_opy_]
      del (bstack1ll1lllll1_opy_[bstack1l1111ll11_opy_])
  if bstack1l1l111l11_opy_(config):
    bstack1ll1lllll1_opy_[bstack1l1ll1_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨज़")] = True
    caps.update(bstack111l111l_opy_)
    caps[bstack1l1ll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪड़")] = bstack1ll1lllll1_opy_
  else:
    bstack1ll1lllll1_opy_[bstack1l1ll1_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪढ़")] = False
    caps.update(bstack11lll1l1_opy_(bstack1ll1lllll1_opy_, bstack111l111l_opy_))
    if bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩफ़") in caps:
      caps[bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭य़")] = caps[bstack1l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫॠ")]
      del (caps[bstack1l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬॡ")])
    if bstack1l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩॢ") in caps:
      caps[bstack1l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫॣ")] = caps[bstack1l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ।")]
      del (caps[bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ॥")])
  return caps
def bstack1llll1llll_opy_():
  global bstack1l1ll1l11l_opy_
  global CONFIG
  if bstack1111l1l1l_opy_() <= version.parse(bstack1l1ll1_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬ०")):
    if bstack1l1ll1l11l_opy_ != bstack1l1ll1_opy_ (u"࠭ࠧ१"):
      return bstack1l1ll1_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ२") + bstack1l1ll1l11l_opy_ + bstack1l1ll1_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧ३")
    return bstack1ll11lll1_opy_
  if bstack1l1ll1l11l_opy_ != bstack1l1ll1_opy_ (u"ࠩࠪ४"):
    return bstack1l1ll1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ५") + bstack1l1ll1l11l_opy_ + bstack1l1ll1_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧ६")
  return bstack1111ll111_opy_
def bstack1lll1ll1l1_opy_(options):
  return hasattr(options, bstack1l1ll1_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭७"))
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
def bstack11ll1ll1_opy_(options, bstack1ll111ll1_opy_):
  for bstack1l11l11l11_opy_ in bstack1ll111ll1_opy_:
    if bstack1l11l11l11_opy_ in [bstack1l1ll1_opy_ (u"࠭ࡡࡳࡩࡶࠫ८"), bstack1l1ll1_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫ९")]:
      continue
    if bstack1l11l11l11_opy_ in options._experimental_options:
      options._experimental_options[bstack1l11l11l11_opy_] = update(options._experimental_options[bstack1l11l11l11_opy_],
                                                         bstack1ll111ll1_opy_[bstack1l11l11l11_opy_])
    else:
      options.add_experimental_option(bstack1l11l11l11_opy_, bstack1ll111ll1_opy_[bstack1l11l11l11_opy_])
  if bstack1l1ll1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭॰") in bstack1ll111ll1_opy_:
    for arg in bstack1ll111ll1_opy_[bstack1l1ll1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॱ")]:
      options.add_argument(arg)
    del (bstack1ll111ll1_opy_[bstack1l1ll1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨॲ")])
  if bstack1l1ll1_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨॳ") in bstack1ll111ll1_opy_:
    for ext in bstack1ll111ll1_opy_[bstack1l1ll1_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩॴ")]:
      try:
        options.add_extension(ext)
      except OSError:
        options.add_encoded_extension(ext)
    del (bstack1ll111ll1_opy_[bstack1l1ll1_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪॵ")])
def bstack11lll11lll_opy_(options, bstack1lll1l1lll_opy_):
  if bstack1l1ll1_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ॶ") in bstack1lll1l1lll_opy_:
    for bstack1111lll1l_opy_ in bstack1lll1l1lll_opy_[bstack1l1ll1_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧॷ")]:
      if bstack1111lll1l_opy_ in options._preferences:
        options._preferences[bstack1111lll1l_opy_] = update(options._preferences[bstack1111lll1l_opy_], bstack1lll1l1lll_opy_[bstack1l1ll1_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨॸ")][bstack1111lll1l_opy_])
      else:
        options.set_preference(bstack1111lll1l_opy_, bstack1lll1l1lll_opy_[bstack1l1ll1_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩॹ")][bstack1111lll1l_opy_])
  if bstack1l1ll1_opy_ (u"ࠫࡦࡸࡧࡴࠩॺ") in bstack1lll1l1lll_opy_:
    for arg in bstack1lll1l1lll_opy_[bstack1l1ll1_opy_ (u"ࠬࡧࡲࡨࡵࠪॻ")]:
      options.add_argument(arg)
def bstack1lll1l1111_opy_(options, bstack11l111lll_opy_):
  if bstack1l1ll1_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࠧॼ") in bstack11l111lll_opy_:
    options.use_webview(bool(bstack11l111lll_opy_[bstack1l1ll1_opy_ (u"ࠧࡸࡧࡥࡺ࡮࡫ࡷࠨॽ")]))
  bstack11ll1ll1_opy_(options, bstack11l111lll_opy_)
def bstack1l111111l_opy_(options, bstack1llll11111_opy_):
  for bstack1l1lll11l1_opy_ in bstack1llll11111_opy_:
    if bstack1l1lll11l1_opy_ in [bstack1l1ll1_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬॾ"), bstack1l1ll1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॿ")]:
      continue
    options.set_capability(bstack1l1lll11l1_opy_, bstack1llll11111_opy_[bstack1l1lll11l1_opy_])
  if bstack1l1ll1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨঀ") in bstack1llll11111_opy_:
    for arg in bstack1llll11111_opy_[bstack1l1ll1_opy_ (u"ࠫࡦࡸࡧࡴࠩঁ")]:
      options.add_argument(arg)
  if bstack1l1ll1_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩং") in bstack1llll11111_opy_:
    options.bstack1l11l1ll11_opy_(bool(bstack1llll11111_opy_[bstack1l1ll1_opy_ (u"࠭ࡴࡦࡥ࡫ࡲࡴࡲ࡯ࡨࡻࡓࡶࡪࡼࡩࡦࡹࠪঃ")]))
def bstack11111l1l1_opy_(options, bstack11llllll1l_opy_):
  for bstack11llll11l1_opy_ in bstack11llllll1l_opy_:
    if bstack11llll11l1_opy_ in [bstack1l1ll1_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ঄"), bstack1l1ll1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭অ")]:
      continue
    options._options[bstack11llll11l1_opy_] = bstack11llllll1l_opy_[bstack11llll11l1_opy_]
  if bstack1l1ll1_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭আ") in bstack11llllll1l_opy_:
    for bstack1llllll11_opy_ in bstack11llllll1l_opy_[bstack1l1ll1_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧই")]:
      options.bstack11111ll11_opy_(
        bstack1llllll11_opy_, bstack11llllll1l_opy_[bstack1l1ll1_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨঈ")][bstack1llllll11_opy_])
  if bstack1l1ll1_opy_ (u"ࠬࡧࡲࡨࡵࠪউ") in bstack11llllll1l_opy_:
    for arg in bstack11llllll1l_opy_[bstack1l1ll1_opy_ (u"࠭ࡡࡳࡩࡶࠫঊ")]:
      options.add_argument(arg)
def bstack111l1l1l1_opy_(options, caps):
  if not hasattr(options, bstack1l1ll1_opy_ (u"ࠧࡌࡇ࡜ࠫঋ")):
    return
  if options.KEY == bstack1l1ll1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ঌ"):
    options = bstack1l11ll1lll_opy_.bstack1ll1111l_opy_(bstack1ll1lll1_opy_=options, config=CONFIG)
  if options.KEY == bstack1l1ll1_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ঍") and options.KEY in caps:
    bstack11ll1ll1_opy_(options, caps[bstack1l1ll1_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ঎")])
  elif options.KEY == bstack1l1ll1_opy_ (u"ࠫࡲࡵࡺ࠻ࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩএ") and options.KEY in caps:
    bstack11lll11lll_opy_(options, caps[bstack1l1ll1_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪঐ")])
  elif options.KEY == bstack1l1ll1_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧ঑") and options.KEY in caps:
    bstack1l111111l_opy_(options, caps[bstack1l1ll1_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨ঒")])
  elif options.KEY == bstack1l1ll1_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩও") and options.KEY in caps:
    bstack1lll1l1111_opy_(options, caps[bstack1l1ll1_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪঔ")])
  elif options.KEY == bstack1l1ll1_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩক") and options.KEY in caps:
    bstack11111l1l1_opy_(options, caps[bstack1l1ll1_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪখ")])
def bstack1ll1l1111l_opy_(caps):
  global bstack1l1lllllll_opy_
  if isinstance(os.environ.get(bstack1l1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭গ")), str):
    bstack1l1lllllll_opy_ = eval(os.getenv(bstack1l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧঘ")))
  if bstack1l1lllllll_opy_:
    if bstack1llll111ll_opy_() < version.parse(bstack1l1ll1_opy_ (u"ࠧ࠳࠰࠶࠲࠵࠭ঙ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1l1ll1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨচ")
    if bstack1l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧছ") in caps:
      browser = caps[bstack1l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨজ")]
    elif bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬঝ") in caps:
      browser = caps[bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ঞ")]
    browser = str(browser).lower()
    if browser == bstack1l1ll1_opy_ (u"࠭ࡩࡱࡪࡲࡲࡪ࠭ট") or browser == bstack1l1ll1_opy_ (u"ࠧࡪࡲࡤࡨࠬঠ"):
      browser = bstack1l1ll1_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨড")
    if browser == bstack1l1ll1_opy_ (u"ࠩࡶࡥࡲࡹࡵ࡯ࡩࠪঢ"):
      browser = bstack1l1ll1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪণ")
    if browser not in [bstack1l1ll1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫত"), bstack1l1ll1_opy_ (u"ࠬ࡫ࡤࡨࡧࠪথ"), bstack1l1ll1_opy_ (u"࠭ࡩࡦࠩদ"), bstack1l1ll1_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧধ"), bstack1l1ll1_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩন")]:
      return None
    try:
      package = bstack1l1ll1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࠮ࡼࡿ࠱ࡳࡵࡺࡩࡰࡰࡶࠫ঩").format(browser)
      name = bstack1l1ll1_opy_ (u"ࠪࡓࡵࡺࡩࡰࡰࡶࠫপ")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1lll1ll1l1_opy_(options):
        return None
      for bstack1l1111ll11_opy_ in caps.keys():
        options.set_capability(bstack1l1111ll11_opy_, caps[bstack1l1111ll11_opy_])
      bstack111l1l1l1_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1lllll11ll_opy_(options, bstack1l1lll1ll1_opy_):
  if not bstack1lll1ll1l1_opy_(options):
    return
  for bstack1l1111ll11_opy_ in bstack1l1lll1ll1_opy_.keys():
    if bstack1l1111ll11_opy_ in bstack1l11l1111l_opy_:
      continue
    if bstack1l1111ll11_opy_ in options._caps and type(options._caps[bstack1l1111ll11_opy_]) in [dict, list]:
      options._caps[bstack1l1111ll11_opy_] = update(options._caps[bstack1l1111ll11_opy_], bstack1l1lll1ll1_opy_[bstack1l1111ll11_opy_])
    else:
      options.set_capability(bstack1l1111ll11_opy_, bstack1l1lll1ll1_opy_[bstack1l1111ll11_opy_])
  bstack111l1l1l1_opy_(options, bstack1l1lll1ll1_opy_)
  if bstack1l1ll1_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪফ") in options._caps:
    if options._caps[bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪব")] and options._caps[bstack1l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫভ")].lower() != bstack1l1ll1_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨম"):
      del options._caps[bstack1l1ll1_opy_ (u"ࠨ࡯ࡲࡾ࠿ࡪࡥࡣࡷࡪ࡫ࡪࡸࡁࡥࡦࡵࡩࡸࡹࠧয")]
def bstack11lll1l111_opy_(proxy_config):
  if bstack1l1ll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭র") in proxy_config:
    proxy_config[bstack1l1ll1_opy_ (u"ࠪࡷࡸࡲࡐࡳࡱࡻࡽࠬ঱")] = proxy_config[bstack1l1ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨল")]
    del (proxy_config[bstack1l1ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ঳")])
  if bstack1l1ll1_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩ঴") in proxy_config and proxy_config[bstack1l1ll1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪ঵")].lower() != bstack1l1ll1_opy_ (u"ࠨࡦ࡬ࡶࡪࡩࡴࠨশ"):
    proxy_config[bstack1l1ll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬষ")] = bstack1l1ll1_opy_ (u"ࠪࡱࡦࡴࡵࡢ࡮ࠪস")
  if bstack1l1ll1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡄࡹࡹࡵࡣࡰࡰࡩ࡭࡬࡛ࡲ࡭ࠩহ") in proxy_config:
    proxy_config[bstack1l1ll1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ঺")] = bstack1l1ll1_opy_ (u"࠭ࡰࡢࡥࠪ঻")
  return proxy_config
def bstack1lll1l11l_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1l1ll1_opy_ (u"ࠧࡱࡴࡲࡼࡾ়࠭") in config:
    return proxy
  config[bstack1l1ll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧঽ")] = bstack11lll1l111_opy_(config[bstack1l1ll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨা")])
  if proxy == None:
    proxy = Proxy(config[bstack1l1ll1_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩি")])
  return proxy
def bstack1l111ll11l_opy_(self):
  global CONFIG
  global bstack1lll1llll_opy_
  try:
    proxy = bstack11l1lll11_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1l1ll1_opy_ (u"ࠫ࠳ࡶࡡࡤࠩী")):
        proxies = bstack11l1l11ll1_opy_(proxy, bstack1llll1llll_opy_())
        if len(proxies) > 0:
          protocol, bstack111l11l11_opy_ = proxies.popitem()
          if bstack1l1ll1_opy_ (u"ࠧࡀ࠯࠰ࠤু") in bstack111l11l11_opy_:
            return bstack111l11l11_opy_
          else:
            return bstack1l1ll1_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢূ") + bstack111l11l11_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1l1ll1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡴࡷࡵࡸࡺࠢࡸࡶࡱࠦ࠺ࠡࡽࢀࠦৃ").format(str(e)))
  return bstack1lll1llll_opy_(self)
def bstack11ll11111l_opy_():
  global CONFIG
  return bstack1l1lll111l_opy_(CONFIG) and bstack11l1l1l1l_opy_() and bstack1111l1l1l_opy_() >= version.parse(bstack1ll1ll1111_opy_)
def bstack1ll1l1ll11_opy_():
  global CONFIG
  return (bstack1l1ll1_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫৄ") in CONFIG or bstack1l1ll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭৅") in CONFIG) and bstack111111l1_opy_()
def bstack1l11l11ll1_opy_(config):
  bstack1lll11l111_opy_ = {}
  if bstack1l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ৆") in config:
    bstack1lll11l111_opy_ = config[bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨে")]
  if bstack1l1ll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫৈ") in config:
    bstack1lll11l111_opy_ = config[bstack1l1ll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ৉")]
  proxy = bstack11l1lll11_opy_(config)
  if proxy:
    if proxy.endswith(bstack1l1ll1_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ৊")) and os.path.isfile(proxy):
      bstack1lll11l111_opy_[bstack1l1ll1_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫো")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1l1ll1_opy_ (u"ࠩ࠱ࡴࡦࡩࠧৌ")):
        proxies = bstack11l111ll_opy_(config, bstack1llll1llll_opy_())
        if len(proxies) > 0:
          protocol, bstack111l11l11_opy_ = proxies.popitem()
          if bstack1l1ll1_opy_ (u"ࠥ࠾࠴࠵্ࠢ") in bstack111l11l11_opy_:
            parsed_url = urlparse(bstack111l11l11_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1l1ll1_opy_ (u"ࠦ࠿࠵࠯ࠣৎ") + bstack111l11l11_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1lll11l111_opy_[bstack1l1ll1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡌࡴࡹࡴࠨ৏")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1lll11l111_opy_[bstack1l1ll1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵࠩ৐")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1lll11l111_opy_[bstack1l1ll1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪ৑")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1lll11l111_opy_[bstack1l1ll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫ৒")] = str(parsed_url.password)
  return bstack1lll11l111_opy_
def bstack1l1llll1_opy_(config):
  if bstack1l1ll1_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧ৓") in config:
    return config[bstack1l1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨ৔")]
  return {}
def bstack11lll11l1l_opy_(caps):
  global bstack1111ll11l_opy_
  if bstack1l1ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ৕") in caps:
    caps[bstack1l1ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭৖")][bstack1l1ll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬৗ")] = True
    if bstack1111ll11l_opy_:
      caps[bstack1l1ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ৘")][bstack1l1ll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ৙")] = bstack1111ll11l_opy_
  else:
    caps[bstack1l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࠧ৚")] = True
    if bstack1111ll11l_opy_:
      caps[bstack1l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ৛")] = bstack1111ll11l_opy_
@measure(event_name=EVENTS.bstack11l1ll111l_opy_, stage=STAGE.bstack1l1ll11ll1_opy_, bstack1llll1ll1l_opy_=bstack11111ll1_opy_)
def bstack1l111lll1_opy_():
  global CONFIG
  if not bstack11ll1ll11_opy_(CONFIG) or cli.is_enabled(CONFIG):
    return
  if bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨড়") in CONFIG and bstack11lll1lll1_opy_(CONFIG[bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩঢ়")]):
    if (
      bstack1l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ৞") in CONFIG
      and bstack11lll1lll1_opy_(CONFIG[bstack1l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫয়")].get(bstack1l1ll1_opy_ (u"ࠨࡵ࡮࡭ࡵࡈࡩ࡯ࡣࡵࡽࡎࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡡࡵ࡫ࡲࡲࠬৠ")))
    ):
      logger.debug(bstack1l1ll1_opy_ (u"ࠤࡏࡳࡨࡧ࡬ࠡࡤ࡬ࡲࡦࡸࡹࠡࡰࡲࡸࠥࡹࡴࡢࡴࡷࡩࡩࠦࡡࡴࠢࡶ࡯࡮ࡶࡂࡪࡰࡤࡶࡾࡏ࡮ࡪࡶ࡬ࡥࡱ࡯ࡳࡢࡶ࡬ࡳࡳࠦࡩࡴࠢࡨࡲࡦࡨ࡬ࡦࡦࠥৡ"))
      return
    bstack1lll11l111_opy_ = bstack1l11l11ll1_opy_(CONFIG)
    bstack11ll1l11l1_opy_(CONFIG[bstack1l1ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ৢ")], bstack1lll11l111_opy_)
def bstack11ll1l11l1_opy_(key, bstack1lll11l111_opy_):
  global bstack1l1l111l1_opy_
  logger.info(bstack1l111l1l_opy_)
  try:
    bstack1l1l111l1_opy_ = Local()
    bstack11l11ll1l1_opy_ = {bstack1l1ll1_opy_ (u"ࠫࡰ࡫ࡹࠨৣ"): key}
    bstack11l11ll1l1_opy_.update(bstack1lll11l111_opy_)
    logger.debug(bstack1ll1l11111_opy_.format(str(bstack11l11ll1l1_opy_)).replace(key, bstack1l1ll1_opy_ (u"ࠬࡡࡒࡆࡆࡄࡇ࡙ࡋࡄ࡞ࠩ৤")))
    bstack1l1l111l1_opy_.start(**bstack11l11ll1l1_opy_)
    if bstack1l1l111l1_opy_.isRunning():
      logger.info(bstack11l111l111_opy_)
  except Exception as e:
    bstack1ll1ll11_opy_(bstack1111l111l_opy_.format(str(e)))
def bstack1ll111111_opy_():
  global bstack1l1l111l1_opy_
  if bstack1l1l111l1_opy_.isRunning():
    logger.info(bstack1l1ll1lll_opy_)
    bstack1l1l111l1_opy_.stop()
  bstack1l1l111l1_opy_ = None
def bstack11ll111l1_opy_(bstack11l1l1l111_opy_=[]):
  global CONFIG
  bstack1l1ll1ll_opy_ = []
  bstack1ll111l1_opy_ = [bstack1l1ll1_opy_ (u"࠭࡯ࡴࠩ৥"), bstack1l1ll1_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪ০"), bstack1l1ll1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬ১"), bstack1l1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ২"), bstack1l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ৩"), bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ৪")]
  try:
    for err in bstack11l1l1l111_opy_:
      bstack1l1ll1l1ll_opy_ = {}
      for k in bstack1ll111l1_opy_:
        val = CONFIG[bstack1l1ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ৫")][int(err[bstack1l1ll1_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ৬")])].get(k)
        if val:
          bstack1l1ll1l1ll_opy_[k] = val
      if(err[bstack1l1ll1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭৭")] != bstack1l1ll1_opy_ (u"ࠨࠩ৮")):
        bstack1l1ll1l1ll_opy_[bstack1l1ll1_opy_ (u"ࠩࡷࡩࡸࡺࡳࠨ৯")] = {
          err[bstack1l1ll1_opy_ (u"ࠪࡲࡦࡳࡥࠨৰ")]: err[bstack1l1ll1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪৱ")]
        }
        bstack1l1ll1ll_opy_.append(bstack1l1ll1l1ll_opy_)
  except Exception as e:
    logger.debug(bstack1l1ll1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧࡱࡵࡱࡦࡺࡴࡪࡰࡪࠤࡩࡧࡴࡢࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸ࠿ࠦࠧ৲") + str(e))
  finally:
    return bstack1l1ll1ll_opy_
def bstack1ll1111111_opy_(file_name):
  bstack1lll1ll111_opy_ = []
  try:
    bstack1lll11l11_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1lll11l11_opy_):
      with open(bstack1lll11l11_opy_) as f:
        bstack111l1l11l_opy_ = json.load(f)
        bstack1lll1ll111_opy_ = bstack111l1l11l_opy_
      os.remove(bstack1lll11l11_opy_)
    return bstack1lll1ll111_opy_
  except Exception as e:
    logger.debug(bstack1l1ll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡨ࡬ࡲࡩ࡯࡮ࡨࠢࡨࡶࡷࡵࡲࠡ࡮࡬ࡷࡹࡀࠠࠨ৳") + str(e))
    return bstack1lll1ll111_opy_
def bstack1llll1l111_opy_():
  try:
      from bstack_utils.constants import bstack11ll1111l_opy_, EVENTS
      from bstack_utils.helper import bstack1l1ll1ll1l_opy_, get_host_info, bstack11lll111ll_opy_
      from datetime import datetime
      from filelock import FileLock
      bstack1lll111ll_opy_ = os.path.join(os.getcwd(), bstack1l1ll1_opy_ (u"ࠧ࡭ࡱࡪࠫ৴"), bstack1l1ll1_opy_ (u"ࠨ࡭ࡨࡽ࠲ࡳࡥࡵࡴ࡬ࡧࡸ࠴ࡪࡴࡱࡱࠫ৵"))
      lock = FileLock(bstack1lll111ll_opy_+bstack1l1ll1_opy_ (u"ࠤ࠱ࡰࡴࡩ࡫ࠣ৶"))
      def bstack11l1111l_opy_():
          try:
              with lock:
                  with open(bstack1lll111ll_opy_, bstack1l1ll1_opy_ (u"ࠥࡶࠧ৷"), encoding=bstack1l1ll1_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥ৸")) as file:
                      data = json.load(file)
                      config = {
                          bstack1l1ll1_opy_ (u"ࠧ࡮ࡥࡢࡦࡨࡶࡸࠨ৹"): {
                              bstack1l1ll1_opy_ (u"ࠨࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠧ৺"): bstack1l1ll1_opy_ (u"ࠢࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠥ৻"),
                          }
                      }
                      bstack1l1l1ll1l1_opy_ = datetime.utcnow()
                      bstack1llllll1l_opy_ = bstack1l1l1ll1l1_opy_.strftime(bstack1l1ll1_opy_ (u"ࠣࠧ࡜࠱ࠪࡳ࠭ࠦࡦࡗࠩࡍࡀࠥࡎ࠼ࠨࡗ࠳ࠫࡦࠡࡗࡗࡇࠧৼ"))
                      bstack11ll11ll_opy_ = os.environ.get(bstack1l1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ৽")) if os.environ.get(bstack1l1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ৾")) else bstack11lll111ll_opy_.get_property(bstack1l1ll1_opy_ (u"ࠦࡸࡪ࡫ࡓࡷࡱࡍࡩࠨ৿"))
                      payload = {
                          bstack1l1ll1_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠤ਀"): bstack1l1ll1_opy_ (u"ࠨࡳࡥ࡭ࡢࡩࡻ࡫࡮ࡵࡵࠥਁ"),
                          bstack1l1ll1_opy_ (u"ࠢࡥࡣࡷࡥࠧਂ"): {
                              bstack1l1ll1_opy_ (u"ࠣࡶࡨࡷࡹ࡮ࡵࡣࡡࡸࡹ࡮ࡪࠢਃ"): bstack11ll11ll_opy_,
                              bstack1l1ll1_opy_ (u"ࠤࡦࡶࡪࡧࡴࡦࡦࡢࡨࡦࡿࠢ਄"): bstack1llllll1l_opy_,
                              bstack1l1ll1_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡱࡥࡲ࡫ࠢਅ"): bstack1l1ll1_opy_ (u"ࠦࡘࡊࡋࡇࡧࡤࡸࡺࡸࡥࡑࡧࡵࡪࡴࡸ࡭ࡢࡰࡦࡩࠧਆ"),
                              bstack1l1ll1_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣ࡯ࡹ࡯࡯ࠤਇ"): {
                                  bstack1l1ll1_opy_ (u"ࠨ࡭ࡦࡣࡶࡹࡷ࡫ࡳࠣਈ"): data,
                                  bstack1l1ll1_opy_ (u"ࠢࡴࡦ࡮ࡖࡺࡴࡉࡥࠤਉ"): bstack11lll111ll_opy_.get_property(bstack1l1ll1_opy_ (u"ࠣࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠥਊ"))
                              },
                              bstack1l1ll1_opy_ (u"ࠤࡸࡷࡪࡸ࡟ࡥࡣࡷࡥࠧ਋"): bstack11lll111ll_opy_.get_property(bstack1l1ll1_opy_ (u"ࠥࡹࡸ࡫ࡲࡏࡣࡰࡩࠧ਌")),
                              bstack1l1ll1_opy_ (u"ࠦ࡭ࡵࡳࡵࡡ࡬ࡲ࡫ࡵࠢ਍"): get_host_info()
                          }
                      }
                      bstack11ll11l1l_opy_ = bstack111lll1l1_opy_(cli.config, [bstack1l1ll1_opy_ (u"ࠧࡧࡰࡪࡵࠥ਎"), bstack1l1ll1_opy_ (u"ࠨࡥࡥࡵࡌࡲࡸࡺࡲࡶ࡯ࡨࡲࡹࡧࡴࡪࡱࡱࠦਏ"), bstack1l1ll1_opy_ (u"ࠢࡢࡲ࡬ࠦਐ")], bstack11ll1111l_opy_)
                      response = bstack1l1ll1ll1l_opy_(bstack1l1ll1_opy_ (u"ࠣࡒࡒࡗ࡙ࠨ਑"), bstack11ll11l1l_opy_, payload, config)
                      if(response.status_code >= 200 and response.status_code < 300):
                          logger.debug(bstack1l1ll1_opy_ (u"ࠤࡇࡥࡹࡧࠠࡴࡧࡱࡸࠥࡹࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡹࡵࠠࡼࡿࠣࡻ࡮ࡺࡨࠡࡦࡤࡸࡦࠦࡻࡾࠤ਒").format(bstack11ll1111l_opy_, payload))
                      else:
                          logger.debug(bstack1l1ll1_opy_ (u"ࠥࡖࡪࡷࡵࡦࡵࡷࠤ࡫ࡧࡩ࡭ࡧࡧࠤ࡫ࡵࡲࠡࡽࢀࠤࡼ࡯ࡴࡩࠢࡧࡥࡹࡧࠠࡼࡿࠥਓ").format(bstack11ll1111l_opy_, payload))
          except Exception as e:
              logger.debug(bstack1l1ll1_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡱࡨࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵࠣࡨࡦࡺࡡࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶࠥࢁࡽࠣਔ").format(e))
      bstack11l1111l_opy_()
      bstack1l1l11l111_opy_(bstack1lll111ll_opy_, logger)
  except:
    pass
def bstack11ll1l1ll_opy_():
  global bstack1ll11ll11l_opy_
  global bstack1ll1l11lll_opy_
  global bstack1l1llll1l_opy_
  global bstack1l1111ll_opy_
  global bstack1ll1ll111_opy_
  global bstack11lll111l1_opy_
  global CONFIG
  bstack11ll1l111_opy_ = os.environ.get(bstack1l1ll1_opy_ (u"ࠬࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉ࠭ਕ"))
  if bstack11ll1l111_opy_ in [bstack1l1ll1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬਖ"), bstack1l1ll1_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ਗ")]:
    bstack111ll11l_opy_()
  percy.shutdown()
  if bstack1ll11ll11l_opy_:
    logger.warning(bstack1l11l11l_opy_.format(str(bstack1ll11ll11l_opy_)))
  else:
    try:
      bstack1lllll1l1l_opy_ = bstack1ll111ll1l_opy_(bstack1l1ll1_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧਘ"), logger)
      if bstack1lllll1l1l_opy_.get(bstack1l1ll1_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧਙ")) and bstack1lllll1l1l_opy_.get(bstack1l1ll1_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨਚ")).get(bstack1l1ll1_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ਛ")):
        logger.warning(bstack1l11l11l_opy_.format(str(bstack1lllll1l1l_opy_[bstack1l1ll1_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪਜ")][bstack1l1ll1_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨਝ")])))
    except Exception as e:
      logger.error(e)
  if cli.is_running():
    bstack1l1l111l_opy_.invoke(bstack1l11111l1l_opy_.bstack11l1111ll1_opy_)
  logger.info(bstack1l111l1ll_opy_)
  global bstack1l1l111l1_opy_
  if bstack1l1l111l1_opy_:
    bstack1ll111111_opy_()
  try:
    for driver in bstack1ll1l11lll_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1l1l11111l_opy_)
  if bstack11lll111l1_opy_ == bstack1l1ll1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ਞ"):
    bstack1ll1ll111_opy_ = bstack1ll1111111_opy_(bstack1l1ll1_opy_ (u"ࠨࡴࡲࡦࡴࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩਟ"))
  if bstack11lll111l1_opy_ == bstack1l1ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩਠ") and len(bstack1l1111ll_opy_) == 0:
    bstack1l1111ll_opy_ = bstack1ll1111111_opy_(bstack1l1ll1_opy_ (u"ࠪࡴࡼࡥࡰࡺࡶࡨࡷࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨਡ"))
    if len(bstack1l1111ll_opy_) == 0:
      bstack1l1111ll_opy_ = bstack1ll1111111_opy_(bstack1l1ll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡵࡶࡰࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪਢ"))
  bstack11lll11ll1_opy_ = bstack1l1ll1_opy_ (u"ࠬ࠭ਣ")
  if len(bstack1l1llll1l_opy_) > 0:
    bstack11lll11ll1_opy_ = bstack11ll111l1_opy_(bstack1l1llll1l_opy_)
  elif len(bstack1l1111ll_opy_) > 0:
    bstack11lll11ll1_opy_ = bstack11ll111l1_opy_(bstack1l1111ll_opy_)
  elif len(bstack1ll1ll111_opy_) > 0:
    bstack11lll11ll1_opy_ = bstack11ll111l1_opy_(bstack1ll1ll111_opy_)
  elif len(bstack1l1ll111ll_opy_) > 0:
    bstack11lll11ll1_opy_ = bstack11ll111l1_opy_(bstack1l1ll111ll_opy_)
  if bool(bstack11lll11ll1_opy_):
    bstack11lll11l11_opy_(bstack11lll11ll1_opy_)
  else:
    bstack11lll11l11_opy_()
  bstack1l1l11l111_opy_(bstack1ll11l1lll_opy_, logger)
  if bstack11ll1l111_opy_ not in [bstack1l1ll1_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧਤ")]:
    bstack1llll1l111_opy_()
  bstack11lll1ll_opy_.bstack11llll1l1_opy_(CONFIG)
  if len(bstack1ll1ll111_opy_) > 0:
    sys.exit(len(bstack1ll1ll111_opy_))
def bstack1l11ll11l_opy_(bstack11111llll_opy_, frame):
  global bstack11lll111ll_opy_
  logger.error(bstack1l111l1l1_opy_)
  bstack11lll111ll_opy_.bstack11l1l1ll_opy_(bstack1l1ll1_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡏࡱࠪਥ"), bstack11111llll_opy_)
  if hasattr(signal, bstack1l1ll1_opy_ (u"ࠨࡕ࡬࡫ࡳࡧ࡬ࡴࠩਦ")):
    bstack11lll111ll_opy_.bstack11l1l1ll_opy_(bstack1l1ll1_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩਧ"), signal.Signals(bstack11111llll_opy_).name)
  else:
    bstack11lll111ll_opy_.bstack11l1l1ll_opy_(bstack1l1ll1_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪਨ"), bstack1l1ll1_opy_ (u"ࠫࡘࡏࡇࡖࡐࡎࡒࡔ࡝ࡎࠨ਩"))
  if cli.is_running():
    bstack1l1l111l_opy_.invoke(bstack1l11111l1l_opy_.bstack11l1111ll1_opy_)
  bstack11ll1l111_opy_ = os.environ.get(bstack1l1ll1_opy_ (u"ࠬࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉ࠭ਪ"))
  if bstack11ll1l111_opy_ == bstack1l1ll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ਫ") and not cli.is_enabled(CONFIG):
    bstack1l1lll1l_opy_.stop(bstack11lll111ll_opy_.get_property(bstack1l1ll1_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡔ࡫ࡪࡲࡦࡲࠧਬ")))
  bstack11ll1l1ll_opy_()
  sys.exit(1)
def bstack1ll1ll11_opy_(err):
  logger.critical(bstack11l1l1llll_opy_.format(str(err)))
  bstack11lll11l11_opy_(bstack11l1l1llll_opy_.format(str(err)), True)
  atexit.unregister(bstack11ll1l1ll_opy_)
  bstack111ll11l_opy_()
  sys.exit(1)
def bstack1l1l1llll1_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack11lll11l11_opy_(message, True)
  atexit.unregister(bstack11ll1l1ll_opy_)
  bstack111ll11l_opy_()
  sys.exit(1)
def bstack1ll11llll_opy_():
  global CONFIG
  global bstack1l1ll1l111_opy_
  global bstack1l11l111l_opy_
  global bstack11l11l111_opy_
  CONFIG = bstack1l1l1ll11l_opy_()
  load_dotenv(CONFIG.get(bstack1l1ll1_opy_ (u"ࠨࡧࡱࡺࡋ࡯࡬ࡦࠩਭ")))
  bstack1l11ll1l_opy_()
  bstack11ll1l111l_opy_()
  CONFIG = bstack1l1l1l1l1l_opy_(CONFIG)
  update(CONFIG, bstack1l11l111l_opy_)
  update(CONFIG, bstack1l1ll1l111_opy_)
  if not cli.is_enabled(CONFIG):
    CONFIG = bstack1l1111ll1l_opy_(CONFIG)
  bstack11l11l111_opy_ = bstack11ll1ll11_opy_(CONFIG)
  os.environ[bstack1l1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬਮ")] = bstack11l11l111_opy_.__str__().lower()
  bstack11lll111ll_opy_.bstack11l1l1ll_opy_(bstack1l1ll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫਯ"), bstack11l11l111_opy_)
  if (bstack1l1ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧਰ") in CONFIG and bstack1l1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ਱") in bstack1l1ll1l111_opy_) or (
          bstack1l1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩਲ") in CONFIG and bstack1l1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪਲ਼") not in bstack1l11l111l_opy_):
    if os.getenv(bstack1l1ll1_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬ਴")):
      CONFIG[bstack1l1ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫਵ")] = os.getenv(bstack1l1ll1_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧਸ਼"))
    else:
      if not CONFIG.get(bstack1l1ll1_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠢ਷"), bstack1l1ll1_opy_ (u"ࠧࠨਸ")) in bstack1ll11l111_opy_:
        bstack1ll1111ll_opy_()
  elif (bstack1l1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩਹ") not in CONFIG and bstack1l1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ਺") in CONFIG) or (
          bstack1l1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ਻") in bstack1l11l111l_opy_ and bstack1l1ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩ਼ࠬ") not in bstack1l1ll1l111_opy_):
    del (CONFIG[bstack1l1ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ਽")])
  if bstack1lll11ll_opy_(CONFIG):
    bstack1ll1ll11_opy_(bstack1llll111l1_opy_)
  Config.bstack11ll1l11l_opy_().bstack11l1l1ll_opy_(bstack1l1ll1_opy_ (u"ࠦࡺࡹࡥࡳࡐࡤࡱࡪࠨਾ"), CONFIG[bstack1l1ll1_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧਿ")])
  bstack1l1l1llll_opy_()
  bstack111l1ll11_opy_()
  if bstack1l1lllllll_opy_ and not CONFIG.get(bstack1l1ll1_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠤੀ"), bstack1l1ll1_opy_ (u"ࠢࠣੁ")) in bstack1ll11l111_opy_:
    CONFIG[bstack1l1ll1_opy_ (u"ࠨࡣࡳࡴࠬੂ")] = bstack1l1llll111_opy_(CONFIG)
    logger.info(bstack1l111lll_opy_.format(CONFIG[bstack1l1ll1_opy_ (u"ࠩࡤࡴࡵ࠭੃")]))
  if not bstack11l11l111_opy_:
    CONFIG[bstack1l1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭੄")] = [{}]
def bstack11ll111l1l_opy_(config, bstack11111l111_opy_):
  global CONFIG
  global bstack1l1lllllll_opy_
  CONFIG = config
  bstack1l1lllllll_opy_ = bstack11111l111_opy_
def bstack111l1ll11_opy_():
  global CONFIG
  global bstack1l1lllllll_opy_
  if bstack1l1ll1_opy_ (u"ࠫࡦࡶࡰࠨ੅") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1l1l1llll1_opy_(e, bstack1l1l1l1ll1_opy_)
    bstack1l1lllllll_opy_ = True
    bstack11lll111ll_opy_.bstack11l1l1ll_opy_(bstack1l1ll1_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ੆"), True)
def bstack1l1llll111_opy_(config):
  bstack11llllll1_opy_ = bstack1l1ll1_opy_ (u"࠭ࠧੇ")
  app = config[bstack1l1ll1_opy_ (u"ࠧࡢࡲࡳࠫੈ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1l1ll1llll_opy_:
      if os.path.exists(app):
        bstack11llllll1_opy_ = bstack11l111111l_opy_(config, app)
      elif bstack1lllll111l_opy_(app):
        bstack11llllll1_opy_ = app
      else:
        bstack1ll1ll11_opy_(bstack1111llll_opy_.format(app))
    else:
      if bstack1lllll111l_opy_(app):
        bstack11llllll1_opy_ = app
      elif os.path.exists(app):
        bstack11llllll1_opy_ = bstack11l111111l_opy_(app)
      else:
        bstack1ll1ll11_opy_(bstack1l11l11111_opy_)
  else:
    if len(app) > 2:
      bstack1ll1ll11_opy_(bstack1ll1l1l11_opy_)
    elif len(app) == 2:
      if bstack1l1ll1_opy_ (u"ࠨࡲࡤࡸ࡭࠭੉") in app and bstack1l1ll1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ੊") in app:
        if os.path.exists(app[bstack1l1ll1_opy_ (u"ࠪࡴࡦࡺࡨࠨੋ")]):
          bstack11llllll1_opy_ = bstack11l111111l_opy_(config, app[bstack1l1ll1_opy_ (u"ࠫࡵࡧࡴࡩࠩੌ")], app[bstack1l1ll1_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨ੍")])
        else:
          bstack1ll1ll11_opy_(bstack1111llll_opy_.format(app))
      else:
        bstack1ll1ll11_opy_(bstack1ll1l1l11_opy_)
    else:
      for key in app:
        if key in bstack11l11111l1_opy_:
          if key == bstack1l1ll1_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ੎"):
            if os.path.exists(app[key]):
              bstack11llllll1_opy_ = bstack11l111111l_opy_(config, app[key])
            else:
              bstack1ll1ll11_opy_(bstack1111llll_opy_.format(app))
          else:
            bstack11llllll1_opy_ = app[key]
        else:
          bstack1ll1ll11_opy_(bstack1l11ll111_opy_)
  return bstack11llllll1_opy_
def bstack1lllll111l_opy_(bstack11llllll1_opy_):
  import re
  bstack1ll1l1ll1l_opy_ = re.compile(bstack1l1ll1_opy_ (u"ࡲࠣࡠ࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯ࠪࠢ੏"))
  bstack1ll11111l_opy_ = re.compile(bstack1l1ll1_opy_ (u"ࡳࠤࡡ࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰࠯࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭ࠨࠧ੐"))
  if bstack1l1ll1_opy_ (u"ࠩࡥࡷ࠿࠵࠯ࠨੑ") in bstack11llllll1_opy_ or re.fullmatch(bstack1ll1l1ll1l_opy_, bstack11llllll1_opy_) or re.fullmatch(bstack1ll11111l_opy_, bstack11llllll1_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack11l1l11111_opy_, stage=STAGE.bstack1l1ll11ll1_opy_, bstack1llll1ll1l_opy_=bstack11111ll1_opy_)
def bstack11l111111l_opy_(config, path, bstack11l1l11l_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1l1ll1_opy_ (u"ࠪࡶࡧ࠭੒")).read()).hexdigest()
  bstack1lllll1l11_opy_ = bstack11lll1lll_opy_(md5_hash)
  bstack11llllll1_opy_ = None
  if bstack1lllll1l11_opy_:
    logger.info(bstack11lll1111l_opy_.format(bstack1lllll1l11_opy_, md5_hash))
    return bstack1lllll1l11_opy_
  bstack1l1l1lll1_opy_ = datetime.datetime.now()
  bstack11111111_opy_ = MultipartEncoder(
    fields={
      bstack1l1ll1_opy_ (u"ࠫ࡫࡯࡬ࡦࠩ੓"): (os.path.basename(path), open(os.path.abspath(path), bstack1l1ll1_opy_ (u"ࠬࡸࡢࠨ੔")), bstack1l1ll1_opy_ (u"࠭ࡴࡦࡺࡷ࠳ࡵࡲࡡࡪࡰࠪ੕")),
      bstack1l1ll1_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪ੖"): bstack11l1l11l_opy_
    }
  )
  response = requests.post(bstack1l11l111ll_opy_, data=bstack11111111_opy_,
                           headers={bstack1l1ll1_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ੗"): bstack11111111_opy_.content_type},
                           auth=(config[bstack1l1ll1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ੘")], config[bstack1l1ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ਖ਼")]))
  try:
    res = json.loads(response.text)
    bstack11llllll1_opy_ = res[bstack1l1ll1_opy_ (u"ࠫࡦࡶࡰࡠࡷࡵࡰࠬਗ਼")]
    logger.info(bstack1ll1l1lll1_opy_.format(bstack11llllll1_opy_))
    bstack1l111111_opy_(md5_hash, bstack11llllll1_opy_)
    cli.bstack11l1l1111l_opy_(bstack1l1ll1_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽ࡹࡵࡲ࡯ࡢࡦࡢࡥࡵࡶࠢਜ਼"), datetime.datetime.now() - bstack1l1l1lll1_opy_)
  except ValueError as err:
    bstack1ll1ll11_opy_(bstack1l11ll11ll_opy_.format(str(err)))
  return bstack11llllll1_opy_
def bstack1l1l1llll_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack1l1l11l11l_opy_
  bstack11l11l11l_opy_ = 1
  bstack1l1l11111_opy_ = 1
  if bstack1l1ll1_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ੜ") in CONFIG:
    bstack1l1l11111_opy_ = CONFIG[bstack1l1ll1_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ੝")]
  else:
    bstack1l1l11111_opy_ = bstack1l1l1l11l1_opy_(framework_name, args) or 1
  if bstack1l1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫਫ਼") in CONFIG:
    bstack11l11l11l_opy_ = len(CONFIG[bstack1l1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ੟")])
  bstack1l1l11l11l_opy_ = int(bstack1l1l11111_opy_) * int(bstack11l11l11l_opy_)
def bstack1l1l1l11l1_opy_(framework_name, args):
  if framework_name == bstack11l1lll11l_opy_ and args and bstack1l1ll1_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨ੠") in args:
      bstack1ll111ll11_opy_ = args.index(bstack1l1ll1_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩ੡"))
      return int(args[bstack1ll111ll11_opy_ + 1]) or 1
  return 1
def bstack11lll1lll_opy_(md5_hash):
  bstack1l1l111l1l_opy_ = os.path.join(os.path.expanduser(bstack1l1ll1_opy_ (u"ࠬࢄࠧ੢")), bstack1l1ll1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭੣"), bstack1l1ll1_opy_ (u"ࠧࡢࡲࡳ࡙ࡵࡲ࡯ࡢࡦࡐࡈ࠺ࡎࡡࡴࡪ࠱࡮ࡸࡵ࡮ࠨ੤"))
  if os.path.exists(bstack1l1l111l1l_opy_):
    bstack11ll11ll1l_opy_ = json.load(open(bstack1l1l111l1l_opy_, bstack1l1ll1_opy_ (u"ࠨࡴࡥࠫ੥")))
    if md5_hash in bstack11ll11ll1l_opy_:
      bstack1l1111l1_opy_ = bstack11ll11ll1l_opy_[md5_hash]
      bstack1ll1llll11_opy_ = datetime.datetime.now()
      bstack1ll111l1ll_opy_ = datetime.datetime.strptime(bstack1l1111l1_opy_[bstack1l1ll1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ੦")], bstack1l1ll1_opy_ (u"ࠪࠩࡩ࠵ࠥ࡮࠱ࠨ࡝ࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧ੧"))
      if (bstack1ll1llll11_opy_ - bstack1ll111l1ll_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1l1111l1_opy_[bstack1l1ll1_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ੨")]):
        return None
      return bstack1l1111l1_opy_[bstack1l1ll1_opy_ (u"ࠬ࡯ࡤࠨ੩")]
  else:
    return None
def bstack1l111111_opy_(md5_hash, bstack11llllll1_opy_):
  bstack11l1llll11_opy_ = os.path.join(os.path.expanduser(bstack1l1ll1_opy_ (u"࠭ࡾࠨ੪")), bstack1l1ll1_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ੫"))
  if not os.path.exists(bstack11l1llll11_opy_):
    os.makedirs(bstack11l1llll11_opy_)
  bstack1l1l111l1l_opy_ = os.path.join(os.path.expanduser(bstack1l1ll1_opy_ (u"ࠨࢀࠪ੬")), bstack1l1ll1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ੭"), bstack1l1ll1_opy_ (u"ࠪࡥࡵࡶࡕࡱ࡮ࡲࡥࡩࡓࡄ࠶ࡊࡤࡷ࡭࠴ࡪࡴࡱࡱࠫ੮"))
  bstack11l111ll11_opy_ = {
    bstack1l1ll1_opy_ (u"ࠫ࡮ࡪࠧ੯"): bstack11llllll1_opy_,
    bstack1l1ll1_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨੰ"): datetime.datetime.strftime(datetime.datetime.now(), bstack1l1ll1_opy_ (u"࠭ࠥࡥ࠱ࠨࡱ࠴࡙ࠫࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪੱ")),
    bstack1l1ll1_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬੲ"): str(__version__)
  }
  if os.path.exists(bstack1l1l111l1l_opy_):
    bstack11ll11ll1l_opy_ = json.load(open(bstack1l1l111l1l_opy_, bstack1l1ll1_opy_ (u"ࠨࡴࡥࠫੳ")))
  else:
    bstack11ll11ll1l_opy_ = {}
  bstack11ll11ll1l_opy_[md5_hash] = bstack11l111ll11_opy_
  with open(bstack1l1l111l1l_opy_, bstack1l1ll1_opy_ (u"ࠤࡺ࠯ࠧੴ")) as outfile:
    json.dump(bstack11ll11ll1l_opy_, outfile)
def bstack1l1ll11l_opy_(self):
  return
def bstack1lll1l11_opy_(self):
  return
def bstack1lll11lll1_opy_():
  global bstack1l11lll1l1_opy_
  bstack1l11lll1l1_opy_ = True
@measure(event_name=EVENTS.bstack11l11l1l11_opy_, stage=STAGE.bstack1l1ll11ll1_opy_, bstack1llll1ll1l_opy_=bstack11111ll1_opy_)
def bstack11lll1ll11_opy_(self):
  global bstack1l11lll1l_opy_
  global bstack1l11l11ll_opy_
  global bstack111l11l1l_opy_
  try:
    if bstack1l1ll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪੵ") in bstack1l11lll1l_opy_ and self.session_id != None and bstack11l1ll11ll_opy_(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡕࡷࡥࡹࡻࡳࠨ੶"), bstack1l1ll1_opy_ (u"ࠬ࠭੷")) != bstack1l1ll1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ੸"):
      bstack11l11ll111_opy_ = bstack1l1ll1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ੹") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1l1ll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ੺")
      if bstack11l11ll111_opy_ == bstack1l1ll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ੻"):
        bstack11lll11l1_opy_(logger)
      if self != None:
        bstack1l1ll1lll1_opy_(self, bstack11l11ll111_opy_, bstack1l1ll1_opy_ (u"ࠪ࠰ࠥ࠭੼").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack1l1ll1_opy_ (u"ࠫࠬ੽")
    if bstack1l1ll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ੾") in bstack1l11lll1l_opy_ and getattr(threading.current_thread(), bstack1l1ll1_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ੿"), None):
      bstack1llll111_opy_.bstack1llll1lll_opy_(self, bstack1ll111l11_opy_, logger, wait=True)
    if bstack1l1ll1_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ઀") in bstack1l11lll1l_opy_:
      if not threading.currentThread().behave_test_status:
        bstack1l1ll1lll1_opy_(self, bstack1l1ll1_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣઁ"))
      bstack11ll1lll1_opy_.bstack1l1l11l1l1_opy_(self)
  except Exception as e:
    logger.debug(bstack1l1ll1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࠥં") + str(e))
  bstack111l11l1l_opy_(self)
  self.session_id = None
def bstack1l11ll1ll_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack1l1ll1l11_opy_
    global bstack1l11lll1l_opy_
    command_executor = kwargs.get(bstack1l1ll1_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷ࠭ઃ"), bstack1l1ll1_opy_ (u"ࠫࠬ઄"))
    bstack1l1lll1lll_opy_ = False
    if type(command_executor) == str and bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨઅ") in command_executor:
      bstack1l1lll1lll_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack1l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩઆ") in str(getattr(command_executor, bstack1l1ll1_opy_ (u"ࠧࡠࡷࡵࡰࠬઇ"), bstack1l1ll1_opy_ (u"ࠨࠩઈ"))):
      bstack1l1lll1lll_opy_ = True
    else:
      kwargs = bstack1l11ll1lll_opy_.bstack1ll1111l_opy_(bstack1ll1lll1_opy_=kwargs, config=CONFIG)
      return bstack11llllll11_opy_(self, *args, **kwargs)
    if bstack1l1lll1lll_opy_:
      bstack1lll1l1l11_opy_ = bstack1lllll11_opy_.bstack11l1lllll1_opy_(CONFIG, bstack1l11lll1l_opy_)
      if kwargs.get(bstack1l1ll1_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪઉ")):
        kwargs[bstack1l1ll1_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫઊ")] = bstack1l1ll1l11_opy_(kwargs[bstack1l1ll1_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬઋ")], bstack1l11lll1l_opy_, CONFIG, bstack1lll1l1l11_opy_)
      elif kwargs.get(bstack1l1ll1_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬઌ")):
        kwargs[bstack1l1ll1_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ઍ")] = bstack1l1ll1l11_opy_(kwargs[bstack1l1ll1_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ઎")], bstack1l11lll1l_opy_, CONFIG, bstack1lll1l1l11_opy_)
  except Exception as e:
    logger.error(bstack1l1ll1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪࡨࡲࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡖࡈࡐࠦࡣࡢࡲࡶ࠾ࠥࢁࡽࠣએ").format(str(e)))
  return bstack11llllll11_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack1l11lllll_opy_, stage=STAGE.bstack1l1ll11ll1_opy_, bstack1llll1ll1l_opy_=bstack11111ll1_opy_)
def bstack1l11l1l111_opy_(self, command_executor=bstack1l1ll1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱࠴࠶࠼࠴࠰࠯࠲࠱࠵࠿࠺࠴࠵࠶ࠥઐ"), *args, **kwargs):
  global bstack1l11l11ll_opy_
  global bstack1ll1l11lll_opy_
  bstack1lll11lll_opy_ = bstack1l11ll1ll_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack111l1ll1l_opy_.on():
    return bstack1lll11lll_opy_
  try:
    logger.debug(bstack1l1ll1_opy_ (u"ࠪࡇࡴࡳ࡭ࡢࡰࡧࠤࡊࡾࡥࡤࡷࡷࡳࡷࠦࡷࡩࡧࡱࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡪࡵࠣࡪࡦࡲࡳࡦࠢ࠰ࠤࢀࢃࠧઑ").format(str(command_executor)))
    logger.debug(bstack1l1ll1_opy_ (u"ࠫࡍࡻࡢࠡࡗࡕࡐࠥ࡯ࡳࠡ࠯ࠣࡿࢂ࠭઒").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨઓ") in command_executor._url:
      bstack11lll111ll_opy_.bstack11l1l1ll_opy_(bstack1l1ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧઔ"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack1l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪક") in command_executor):
    bstack11lll111ll_opy_.bstack11l1l1ll_opy_(bstack1l1ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩખ"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1l11l111l1_opy_ = getattr(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡖࡨࡷࡹࡓࡥࡵࡣࠪગ"), None)
  bstack11lll11111_opy_ = {}
  if self.capabilities is not None:
    bstack11lll11111_opy_[bstack1l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩઘ")] = self.capabilities.get(bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩઙ"))
    bstack11lll11111_opy_[bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧચ")] = self.capabilities.get(bstack1l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧછ"))
    bstack11lll11111_opy_[bstack1l1ll1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫࡟ࡰࡲࡷ࡭ࡴࡴࡳࠨજ")] = self.capabilities.get(bstack1l1ll1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ઝ"))
  if CONFIG.get(bstack1l1ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩઞ"), False) and bstack1l11ll1lll_opy_.bstack11ll1111_opy_(bstack11lll11111_opy_):
    threading.current_thread().a11yPlatform = True
  if bstack1l1ll1_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪટ") in bstack1l11lll1l_opy_ or bstack1l1ll1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪઠ") in bstack1l11lll1l_opy_:
    bstack1l1lll1l_opy_.bstack11l11l1l_opy_(self)
  if bstack1l1ll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬડ") in bstack1l11lll1l_opy_ and bstack1l11l111l1_opy_ and bstack1l11l111l1_opy_.get(bstack1l1ll1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ઢ"), bstack1l1ll1_opy_ (u"ࠧࠨણ")) == bstack1l1ll1_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩત"):
    bstack1l1lll1l_opy_.bstack11l11l1l_opy_(self)
  bstack1l11l11ll_opy_ = self.session_id
  bstack1ll1l11lll_opy_.append(self)
  return bstack1lll11lll_opy_
def bstack11l111l1ll_opy_(args):
  return bstack1l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴࠪથ") in str(args)
def bstack11ll1ll1l_opy_(self, driver_command, *args, **kwargs):
  global bstack11l11l1ll1_opy_
  global bstack1ll1ll1l11_opy_
  bstack111l1111l_opy_ = bstack11l1ll11ll_opy_(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧદ"), None) and bstack11l1ll11ll_opy_(
          threading.current_thread(), bstack1l1ll1_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪધ"), None)
  bstack1l1llll11l_opy_ = bstack11l1ll11ll_opy_(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠬ࡯ࡳࡂࡲࡳࡅ࠶࠷ࡹࡕࡧࡶࡸࠬન"), None) and bstack11l1ll11ll_opy_(
          threading.current_thread(), bstack1l1ll1_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ઩"), None)
  bstack1ll1llll_opy_ = getattr(self, bstack1l1ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧપ"), None) != None and getattr(self, bstack1l1ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨફ"), None) == True
  if not bstack1ll1ll1l11_opy_ and bstack1l1ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩબ") in CONFIG and CONFIG[bstack1l1ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪભ")] == True and bstack1ll1l1l1l_opy_.bstack11l11lll_opy_(driver_command) and (bstack1ll1llll_opy_ or bstack111l1111l_opy_ or bstack1l1llll11l_opy_) and not bstack11l111l1ll_opy_(args):
    try:
      bstack1ll1ll1l11_opy_ = True
      logger.debug(bstack1l1ll1_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡿࢂ࠭મ").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack1l1ll1_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡨࡶ࡫ࡵࡲ࡮ࠢࡶࡧࡦࡴࠠࡼࡿࠪય").format(str(err)))
    bstack1ll1ll1l11_opy_ = False
  response = bstack11l11l1ll1_opy_(self, driver_command, *args, **kwargs)
  if (bstack1l1ll1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬર") in str(bstack1l11lll1l_opy_).lower() or bstack1l1ll1_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ઱") in str(bstack1l11lll1l_opy_).lower()) and bstack111l1ll1l_opy_.on():
    try:
      if driver_command == bstack1l1ll1_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬલ"):
        bstack1l1lll1l_opy_.bstack1l1l1111ll_opy_({
            bstack1l1ll1_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨળ"): response[bstack1l1ll1_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩ઴")],
            bstack1l1ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫવ"): bstack1l1lll1l_opy_.current_test_uuid() if bstack1l1lll1l_opy_.current_test_uuid() else bstack111l1ll1l_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
@measure(event_name=EVENTS.bstack11l11l1111_opy_, stage=STAGE.bstack1l1ll11ll1_opy_, bstack1llll1ll1l_opy_=bstack11111ll1_opy_)
def bstack11llll1ll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack1l11l11ll_opy_
  global bstack111l1111_opy_
  global bstack11111ll1_opy_
  global bstack11111ll1l_opy_
  global bstack111lllll1_opy_
  global bstack1l11lll1l_opy_
  global bstack11llllll11_opy_
  global bstack1ll1l11lll_opy_
  global bstack11ll111ll1_opy_
  global bstack1ll111l11_opy_
  CONFIG[bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧશ")] = str(bstack1l11lll1l_opy_) + str(__version__)
  bstack1l111l1l11_opy_ = os.environ[bstack1l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫષ")]
  bstack1lll1l1l11_opy_ = bstack1lllll11_opy_.bstack11l1lllll1_opy_(CONFIG, bstack1l11lll1l_opy_)
  CONFIG[bstack1l1ll1_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪસ")] = bstack1l111l1l11_opy_
  CONFIG[bstack1l1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪહ")] = bstack1lll1l1l11_opy_
  if CONFIG.get(bstack1l1ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ઺"),bstack1l1ll1_opy_ (u"ࠪࠫ઻")) and bstack1l1ll1_opy_ (u"ࠫࡷࡵࡢࡰࡶ઼ࠪ") in bstack1l11lll1l_opy_:
    CONFIG[bstack1l1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬઽ")].pop(bstack1l1ll1_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫા"), None)
    CONFIG[bstack1l1ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧિ")].pop(bstack1l1ll1_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ી"), None)
  command_executor = bstack1llll1llll_opy_()
  logger.debug(bstack1l1111111_opy_.format(command_executor))
  proxy = bstack1lll1l11l_opy_(CONFIG, proxy)
  bstack1l11llll1_opy_ = 0 if bstack111l1111_opy_ < 0 else bstack111l1111_opy_
  try:
    if bstack11111ll1l_opy_ is True:
      bstack1l11llll1_opy_ = int(multiprocessing.current_process().name)
    elif bstack111lllll1_opy_ is True:
      bstack1l11llll1_opy_ = int(threading.current_thread().name)
  except:
    bstack1l11llll1_opy_ = 0
  bstack1l1lll1ll1_opy_ = bstack11lll1l1ll_opy_(CONFIG, bstack1l11llll1_opy_)
  logger.debug(bstack111ll1111_opy_.format(str(bstack1l1lll1ll1_opy_)))
  if bstack1l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ુ") in CONFIG and bstack11lll1lll1_opy_(CONFIG[bstack1l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧૂ")]):
    bstack11lll11l1l_opy_(bstack1l1lll1ll1_opy_)
  if bstack1l11ll1lll_opy_.bstack11ll1111l1_opy_(CONFIG, bstack1l11llll1_opy_) and bstack1l11ll1lll_opy_.bstack111111l1l_opy_(bstack1l1lll1ll1_opy_, options, desired_capabilities, CONFIG):
    threading.current_thread().a11yPlatform = True
    if (cli.accessibility is None or not cli.accessibility.is_enabled()):
      bstack1l11ll1lll_opy_.set_capabilities(bstack1l1lll1ll1_opy_, CONFIG)
  if desired_capabilities:
    bstack1lll1llll1_opy_ = bstack1l1l1l1l1l_opy_(desired_capabilities)
    bstack1lll1llll1_opy_[bstack1l1ll1_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫૃ")] = bstack1l1l111l11_opy_(CONFIG)
    bstack11l1l11l1l_opy_ = bstack11lll1l1ll_opy_(bstack1lll1llll1_opy_)
    if bstack11l1l11l1l_opy_:
      bstack1l1lll1ll1_opy_ = update(bstack11l1l11l1l_opy_, bstack1l1lll1ll1_opy_)
    desired_capabilities = None
  if options:
    bstack1lllll11ll_opy_(options, bstack1l1lll1ll1_opy_)
  if not options:
    options = bstack1ll1l1111l_opy_(bstack1l1lll1ll1_opy_)
  bstack1ll111l11_opy_ = CONFIG.get(bstack1l1ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨૄ"))[bstack1l11llll1_opy_]
  if proxy and bstack1111l1l1l_opy_() >= version.parse(bstack1l1ll1_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ૅ")):
    options.proxy(proxy)
  if options and bstack1111l1l1l_opy_() >= version.parse(bstack1l1ll1_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭૆")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1111l1l1l_opy_() < version.parse(bstack1l1ll1_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧે")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1l1lll1ll1_opy_)
  logger.info(bstack1l1llll1ll_opy_)
  bstack1l11l1llll_opy_.end(EVENTS.bstack1l1l11ll11_opy_.value, EVENTS.bstack1l1l11ll11_opy_.value + bstack1l1ll1_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤૈ"), EVENTS.bstack1l1l11ll11_opy_.value + bstack1l1ll1_opy_ (u"ࠥ࠾ࡪࡴࡤࠣૉ"), status=True, failure=None, test_name=bstack11111ll1_opy_)
  if bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡶࡲࡰࡨ࡬ࡰࡪ࠭૊") in kwargs:
    del kwargs[bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡰࡳࡱࡩ࡭ࡱ࡫ࠧો")]
  if bstack1111l1l1l_opy_() >= version.parse(bstack1l1ll1_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ૌ")):
    bstack11llllll11_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
  elif bstack1111l1l1l_opy_() >= version.parse(bstack1l1ll1_opy_ (u"ࠧ࠴࠰࠻࠲࠵્࠭")):
    bstack11llllll11_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1111l1l1l_opy_() >= version.parse(bstack1l1ll1_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨ૎")):
    bstack11llllll11_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack11llllll11_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive)
  if bstack1l11ll1lll_opy_.bstack11ll1111l1_opy_(CONFIG, bstack1l11llll1_opy_) and bstack1l11ll1lll_opy_.bstack111111l1l_opy_(self.caps, options, desired_capabilities):
    if CONFIG[bstack1l1ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ૏")][bstack1l1ll1_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩૐ")] == True:
      threading.current_thread().appA11yPlatform = True
      if cli.accessibility is None or not cli.accessibility.is_enabled():
        bstack1l11ll1lll_opy_.set_capabilities(bstack1l1lll1ll1_opy_, CONFIG)
  try:
    bstack11lll1l1l1_opy_ = bstack1l1ll1_opy_ (u"ࠫࠬ૑")
    if bstack1111l1l1l_opy_() >= version.parse(bstack1l1ll1_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭૒")):
      if self.caps is not None:
        bstack11lll1l1l1_opy_ = self.caps.get(bstack1l1ll1_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨ૓"))
    else:
      if self.capabilities is not None:
        bstack11lll1l1l1_opy_ = self.capabilities.get(bstack1l1ll1_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢ૔"))
    if bstack11lll1l1l1_opy_:
      bstack1l11l1ll1_opy_(bstack11lll1l1l1_opy_)
      if bstack1111l1l1l_opy_() <= version.parse(bstack1l1ll1_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨ૕")):
        self.command_executor._url = bstack1l1ll1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ૖") + bstack1l1ll1l11l_opy_ + bstack1l1ll1_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢ૗")
      else:
        self.command_executor._url = bstack1l1ll1_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨ૘") + bstack11lll1l1l1_opy_ + bstack1l1ll1_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨ૙")
      logger.debug(bstack1l1l111111_opy_.format(bstack11lll1l1l1_opy_))
    else:
      logger.debug(bstack1llll1ll_opy_.format(bstack1l1ll1_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢ૚")))
  except Exception as e:
    logger.debug(bstack1llll1ll_opy_.format(e))
  if bstack1l1ll1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭૛") in bstack1l11lll1l_opy_:
    bstack1lllll1ll1_opy_(bstack111l1111_opy_, bstack11ll111ll1_opy_)
  bstack1l11l11ll_opy_ = self.session_id
  if bstack1l1ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ૜") in bstack1l11lll1l_opy_ or bstack1l1ll1_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ૝") in bstack1l11lll1l_opy_ or bstack1l1ll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ૞") in bstack1l11lll1l_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack1l11l111l1_opy_ = getattr(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡘࡪࡹࡴࡎࡧࡷࡥࠬ૟"), None)
  if bstack1l1ll1_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬૠ") in bstack1l11lll1l_opy_ or bstack1l1ll1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬૡ") in bstack1l11lll1l_opy_:
    bstack1l1lll1l_opy_.bstack11l11l1l_opy_(self)
  if bstack1l1ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧૢ") in bstack1l11lll1l_opy_ and bstack1l11l111l1_opy_ and bstack1l11l111l1_opy_.get(bstack1l1ll1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨૣ"), bstack1l1ll1_opy_ (u"ࠩࠪ૤")) == bstack1l1ll1_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ૥"):
    bstack1l1lll1l_opy_.bstack11l11l1l_opy_(self)
  bstack1ll1l11lll_opy_.append(self)
  if bstack1l1ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ૦") in CONFIG and bstack1l1ll1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ૧") in CONFIG[bstack1l1ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ૨")][bstack1l11llll1_opy_]:
    bstack11111ll1_opy_ = CONFIG[bstack1l1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ૩")][bstack1l11llll1_opy_][bstack1l1ll1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭૪")]
  logger.debug(bstack1l1l11ll_opy_.format(bstack1l11l11ll_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    from browserstack_sdk.__init__ import bstack1l1l1ll1l_opy_
    def bstack1llllll1ll_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack11l1l1ll11_opy_
      if(bstack1l1ll1_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸ࠯࡬ࡶࠦ૫") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1l1ll1_opy_ (u"ࠪࢂࠬ૬")), bstack1l1ll1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ૭"), bstack1l1ll1_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧ૮")), bstack1l1ll1_opy_ (u"࠭ࡷࠨ૯")) as fp:
          fp.write(bstack1l1ll1_opy_ (u"ࠢࠣ૰"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1l1ll1_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥ૱")))):
          with open(args[1], bstack1l1ll1_opy_ (u"ࠩࡵࠫ૲")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1l1ll1_opy_ (u"ࠪࡥࡸࡿ࡮ࡤࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࡤࡴࡥࡸࡒࡤ࡫ࡪ࠮ࡣࡰࡰࡷࡩࡽࡺࠬࠡࡲࡤ࡫ࡪࠦ࠽ࠡࡸࡲ࡭ࡩࠦ࠰ࠪࠩ૳") in line), None)
            if index is not None:
                lines.insert(index+2, bstack11ll11l1ll_opy_)
            if bstack1l1ll1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ૴") in CONFIG and str(CONFIG[bstack1l1ll1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ૵")]).lower() != bstack1l1ll1_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ૶"):
                bstack1111l1l11_opy_ = bstack1l1l1ll1l_opy_()
                bstack1l1l11lll_opy_ = bstack1l1ll1_opy_ (u"ࠧࠨࠩࠍ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࠐࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹࡝࠼ࠌࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠ࠿ࠏࡩ࡯࡯ࡵࡷࠤࡵࡥࡩ࡯ࡦࡨࡼࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠳࡟࠾ࠎࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡸࡲࡩࡤࡧࠫ࠴࠱ࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴ࠫ࠾ࠎࡨࡵ࡮ࡴࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫ࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤࠬ࠿ࠏ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡲࡡࡶࡰࡦ࡬ࠥࡃࠠࡢࡵࡼࡲࡨࠦࠨ࡭ࡣࡸࡲࡨ࡮ࡏࡱࡶ࡬ࡳࡳࡹࠩࠡ࠿ࡁࠤࢀࢁࠊࠡࠢ࡯ࡩࡹࠦࡣࡢࡲࡶ࠿ࠏࠦࠠࡵࡴࡼࠤࢀࢁࠊࠡࠢࠣࠤࡨࡧࡰࡴࠢࡀࠤࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸ࠯࠻ࠋࠢࠣࢁࢂࠦࡣࡢࡶࡦ࡬ࠥ࠮ࡥࡹࠫࠣࡿࢀࠐࠠࠡࠢࠣࡧࡴࡴࡳࡰ࡮ࡨ࠲ࡪࡸࡲࡰࡴࠫࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷ࠿ࠨࠬࠡࡧࡻ࠭ࡀࠐࠠࠡࡿࢀࠎࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡩ࡯࡯ࡰࡨࡧࡹ࠮ࡻࡼࠌࠣࠤࠥࠦࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶ࠽ࠤࠬࢁࡣࡥࡲࡘࡶࡱࢃࠧࠡ࠭ࠣࡩࡳࡩ࡯ࡥࡧࡘࡖࡎࡉ࡯࡮ࡲࡲࡲࡪࡴࡴࠩࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡦࡥࡵࡹࠩࠪ࠮ࠍࠤࠥࠦࠠ࠯࠰࠱ࡰࡦࡻ࡮ࡤࡪࡒࡴࡹ࡯࡯࡯ࡵࠍࠤࠥࢃࡽࠪ࠽ࠍࢁࢂࡁࠊ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱ࠍࠫࠬ࠭૷").format(bstack1111l1l11_opy_=bstack1111l1l11_opy_)
            lines.insert(1, bstack1l1l11lll_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1l1ll1_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥ૸")), bstack1l1ll1_opy_ (u"ࠩࡺࠫૹ")) as bstack1ll11l1l11_opy_:
              bstack1ll11l1l11_opy_.writelines(lines)
        CONFIG[bstack1l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬૺ")] = str(bstack1l11lll1l_opy_) + str(__version__)
        bstack1l111l1l11_opy_ = os.environ[bstack1l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩૻ")]
        bstack1lll1l1l11_opy_ = bstack1lllll11_opy_.bstack11l1lllll1_opy_(CONFIG, bstack1l11lll1l_opy_)
        CONFIG[bstack1l1ll1_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨૼ")] = bstack1l111l1l11_opy_
        CONFIG[bstack1l1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨ૽")] = bstack1lll1l1l11_opy_
        bstack1l11llll1_opy_ = 0 if bstack111l1111_opy_ < 0 else bstack111l1111_opy_
        try:
          if bstack11111ll1l_opy_ is True:
            bstack1l11llll1_opy_ = int(multiprocessing.current_process().name)
          elif bstack111lllll1_opy_ is True:
            bstack1l11llll1_opy_ = int(threading.current_thread().name)
        except:
          bstack1l11llll1_opy_ = 0
        CONFIG[bstack1l1ll1_opy_ (u"ࠢࡶࡵࡨ࡛࠸ࡉࠢ૾")] = False
        CONFIG[bstack1l1ll1_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢ૿")] = True
        bstack1l1lll1ll1_opy_ = bstack11lll1l1ll_opy_(CONFIG, bstack1l11llll1_opy_)
        logger.debug(bstack111ll1111_opy_.format(str(bstack1l1lll1ll1_opy_)))
        if CONFIG.get(bstack1l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭଀")):
          bstack11lll11l1l_opy_(bstack1l1lll1ll1_opy_)
        if bstack1l1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ଁ") in CONFIG and bstack1l1ll1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩଂ") in CONFIG[bstack1l1ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨଃ")][bstack1l11llll1_opy_]:
          bstack11111ll1_opy_ = CONFIG[bstack1l1ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ଄")][bstack1l11llll1_opy_][bstack1l1ll1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬଅ")]
        args.append(os.path.join(os.path.expanduser(bstack1l1ll1_opy_ (u"ࠨࢀࠪଆ")), bstack1l1ll1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩଇ"), bstack1l1ll1_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬଈ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1l1lll1ll1_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1l1ll1_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨଉ"))
      bstack11l1l1ll11_opy_ = True
      return bstack11lllll1_opy_(self, args, bufsize=bufsize, executable=executable,
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
    global bstack111l1111_opy_
    global bstack11111ll1_opy_
    global bstack11111ll1l_opy_
    global bstack111lllll1_opy_
    global bstack1l11lll1l_opy_
    CONFIG[bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧଊ")] = str(bstack1l11lll1l_opy_) + str(__version__)
    bstack1l111l1l11_opy_ = os.environ[bstack1l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫଋ")]
    bstack1lll1l1l11_opy_ = bstack1lllll11_opy_.bstack11l1lllll1_opy_(CONFIG, bstack1l11lll1l_opy_)
    CONFIG[bstack1l1ll1_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪଌ")] = bstack1l111l1l11_opy_
    CONFIG[bstack1l1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ଍")] = bstack1lll1l1l11_opy_
    bstack1l11llll1_opy_ = 0 if bstack111l1111_opy_ < 0 else bstack111l1111_opy_
    try:
      if bstack11111ll1l_opy_ is True:
        bstack1l11llll1_opy_ = int(multiprocessing.current_process().name)
      elif bstack111lllll1_opy_ is True:
        bstack1l11llll1_opy_ = int(threading.current_thread().name)
    except:
      bstack1l11llll1_opy_ = 0
    CONFIG[bstack1l1ll1_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ଎")] = True
    bstack1l1lll1ll1_opy_ = bstack11lll1l1ll_opy_(CONFIG, bstack1l11llll1_opy_)
    logger.debug(bstack111ll1111_opy_.format(str(bstack1l1lll1ll1_opy_)))
    if CONFIG.get(bstack1l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧଏ")):
      bstack11lll11l1l_opy_(bstack1l1lll1ll1_opy_)
    if bstack1l1ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଐ") in CONFIG and bstack1l1ll1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ଑") in CONFIG[bstack1l1ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ଒")][bstack1l11llll1_opy_]:
      bstack11111ll1_opy_ = CONFIG[bstack1l1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଓ")][bstack1l11llll1_opy_][bstack1l1ll1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ଔ")]
    import urllib
    import json
    if bstack1l1ll1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭କ") in CONFIG and str(CONFIG[bstack1l1ll1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧଖ")]).lower() != bstack1l1ll1_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪଗ"):
        bstack1lll1lllll_opy_ = bstack1l1l1ll1l_opy_()
        bstack1111l1l11_opy_ = bstack1lll1lllll_opy_ + urllib.parse.quote(json.dumps(bstack1l1lll1ll1_opy_))
    else:
        bstack1111l1l11_opy_ = bstack1l1ll1_opy_ (u"ࠬࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠧଘ") + urllib.parse.quote(json.dumps(bstack1l1lll1ll1_opy_))
    browser = self.connect(bstack1111l1l11_opy_)
    return browser
except Exception as e:
    pass
def bstack1l1l1lllll_opy_():
    global bstack11l1l1ll11_opy_
    global bstack1l11lll1l_opy_
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l1ll1111l_opy_
        global bstack11lll111ll_opy_
        if not bstack11l11l111_opy_:
          global bstack1l11111111_opy_
          if not bstack1l11111111_opy_:
            from bstack_utils.helper import bstack1l111l11l_opy_, bstack1l11ll111l_opy_, bstack1llllll111_opy_
            bstack1l11111111_opy_ = bstack1l111l11l_opy_()
            bstack1l11ll111l_opy_(bstack1l11lll1l_opy_)
            bstack1lll1l1l11_opy_ = bstack1lllll11_opy_.bstack11l1lllll1_opy_(CONFIG, bstack1l11lll1l_opy_)
            bstack11lll111ll_opy_.bstack11l1l1ll_opy_(bstack1l1ll1_opy_ (u"ࠨࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡔࡗࡕࡄࡖࡅࡗࡣࡒࡇࡐࠣଙ"), bstack1lll1l1l11_opy_)
          BrowserType.connect = bstack1l1ll1111l_opy_
          return
        BrowserType.launch = bstack1l11ll11l1_opy_
        bstack11l1l1ll11_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1llllll1ll_opy_
      bstack11l1l1ll11_opy_ = True
    except Exception as e:
      pass
def bstack11l11l1lll_opy_(context, bstack11l11ll1_opy_):
  try:
    context.page.evaluate(bstack1l1ll1_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣଚ"), bstack1l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬଛ")+ json.dumps(bstack11l11ll1_opy_) + bstack1l1ll1_opy_ (u"ࠤࢀࢁࠧଜ"))
  except Exception as e:
    logger.debug(bstack1l1ll1_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽ࠻ࠢࡾࢁࠧଝ").format(str(e), traceback.format_exc()))
def bstack1ll11lllll_opy_(context, message, level):
  try:
    context.page.evaluate(bstack1l1ll1_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧଞ"), bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪଟ") + json.dumps(message) + bstack1l1ll1_opy_ (u"࠭ࠬࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠩଠ") + json.dumps(level) + bstack1l1ll1_opy_ (u"ࠧࡾࡿࠪଡ"))
  except Exception as e:
    logger.debug(bstack1l1ll1_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡࡽࢀ࠾ࠥࢁࡽࠣଢ").format(str(e), traceback.format_exc()))
@measure(event_name=EVENTS.bstack1ll11111l1_opy_, stage=STAGE.bstack1l1ll11ll1_opy_, bstack1llll1ll1l_opy_=bstack11111ll1_opy_)
def bstack1lllll1ll_opy_(self, url):
  global bstack1lll1ll11_opy_
  try:
    bstack11ll1lllll_opy_(url)
  except Exception as err:
    logger.debug(bstack11l1ll1l_opy_.format(str(err)))
  try:
    bstack1lll1ll11_opy_(self, url)
  except Exception as e:
    try:
      bstack1ll11l1ll_opy_ = str(e)
      if any(err_msg in bstack1ll11l1ll_opy_ for err_msg in bstack1l1lllll1l_opy_):
        bstack11ll1lllll_opy_(url, True)
    except Exception as err:
      logger.debug(bstack11l1ll1l_opy_.format(str(err)))
    raise e
def bstack111l1l111_opy_(self):
  global bstack111l1lll_opy_
  bstack111l1lll_opy_ = self
  return
def bstack1l11111ll_opy_(self):
  global bstack11l11lll1l_opy_
  bstack11l11lll1l_opy_ = self
  return
def bstack11l11lll11_opy_(test_name, bstack1ll111l1l1_opy_):
  global CONFIG
  if percy.bstack1ll1111lll_opy_() == bstack1l1ll1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢଣ"):
    bstack111ll111l_opy_ = os.path.relpath(bstack1ll111l1l1_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack111ll111l_opy_)
    bstack1llll1ll1l_opy_ = suite_name + bstack1l1ll1_opy_ (u"ࠥ࠱ࠧତ") + test_name
    threading.current_thread().percySessionName = bstack1llll1ll1l_opy_
def bstack111lll1ll_opy_(self, test, *args, **kwargs):
  global bstack1ll111111l_opy_
  test_name = None
  bstack1ll111l1l1_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1ll111l1l1_opy_ = str(test.source)
  bstack11l11lll11_opy_(test_name, bstack1ll111l1l1_opy_)
  bstack1ll111111l_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.bstack1lll1l111_opy_, stage=STAGE.bstack1l1ll11ll1_opy_, bstack1llll1ll1l_opy_=bstack11111ll1_opy_)
def bstack11111l1ll_opy_(driver, bstack1llll1ll1l_opy_):
  if not bstack1l111llll1_opy_ and bstack1llll1ll1l_opy_:
      bstack1llllllll1_opy_ = {
          bstack1l1ll1_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫଥ"): bstack1l1ll1_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ଦ"),
          bstack1l1ll1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩଧ"): {
              bstack1l1ll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬନ"): bstack1llll1ll1l_opy_
          }
      }
      bstack11lllllll_opy_ = bstack1l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭଩").format(json.dumps(bstack1llllllll1_opy_))
      driver.execute_script(bstack11lllllll_opy_)
  if bstack11l1lll1l_opy_:
      bstack11l1l111l_opy_ = {
          bstack1l1ll1_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩପ"): bstack1l1ll1_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬଫ"),
          bstack1l1ll1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧବ"): {
              bstack1l1ll1_opy_ (u"ࠬࡪࡡࡵࡣࠪଭ"): bstack1llll1ll1l_opy_ + bstack1l1ll1_opy_ (u"࠭ࠠࡱࡣࡶࡷࡪࡪࠡࠨମ"),
              bstack1l1ll1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ଯ"): bstack1l1ll1_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭ର")
          }
      }
      if bstack11l1lll1l_opy_.status == bstack1l1ll1_opy_ (u"ࠩࡓࡅࡘ࡙ࠧ଱"):
          bstack1l11llll11_opy_ = bstack1l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨଲ").format(json.dumps(bstack11l1l111l_opy_))
          driver.execute_script(bstack1l11llll11_opy_)
          bstack1l1ll1lll1_opy_(driver, bstack1l1ll1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫଳ"))
      elif bstack11l1lll1l_opy_.status == bstack1l1ll1_opy_ (u"ࠬࡌࡁࡊࡎࠪ଴"):
          reason = bstack1l1ll1_opy_ (u"ࠨࠢଵ")
          bstack111lll11l_opy_ = bstack1llll1ll1l_opy_ + bstack1l1ll1_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠨଶ")
          if bstack11l1lll1l_opy_.message:
              reason = str(bstack11l1lll1l_opy_.message)
              bstack111lll11l_opy_ = bstack111lll11l_opy_ + bstack1l1ll1_opy_ (u"ࠨࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࡀࠠࠨଷ") + reason
          bstack11l1l111l_opy_[bstack1l1ll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬସ")] = {
              bstack1l1ll1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩହ"): bstack1l1ll1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ଺"),
              bstack1l1ll1_opy_ (u"ࠬࡪࡡࡵࡣࠪ଻"): bstack111lll11l_opy_
          }
          bstack1l11llll11_opy_ = bstack1l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀ଼ࠫ").format(json.dumps(bstack11l1l111l_opy_))
          driver.execute_script(bstack1l11llll11_opy_)
          bstack1l1ll1lll1_opy_(driver, bstack1l1ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧଽ"), reason)
          bstack1ll1ll1l_opy_(reason, str(bstack11l1lll1l_opy_), str(bstack111l1111_opy_), logger)
@measure(event_name=EVENTS.bstack1lll11llll_opy_, stage=STAGE.bstack1l1ll11ll1_opy_, bstack1llll1ll1l_opy_=bstack11111ll1_opy_)
def bstack1ll1l1l111_opy_(driver, test):
  if percy.bstack1ll1111lll_opy_() == bstack1l1ll1_opy_ (u"ࠣࡶࡵࡹࡪࠨା") and percy.bstack11llll1l11_opy_() == bstack1l1ll1_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦି"):
      bstack1l1llllll_opy_ = bstack11l1ll11ll_opy_(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠪࡴࡪࡸࡣࡺࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ୀ"), None)
      bstack111l1ll1_opy_(driver, bstack1l1llllll_opy_, test)
  if (bstack11l1ll11ll_opy_(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨୁ"), None) and
      bstack11l1ll11ll_opy_(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫୂ"), None)) or (
      bstack11l1ll11ll_opy_(threading.current_thread(), bstack1l1ll1_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ୃ"), None) and
      bstack11l1ll11ll_opy_(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩୄ"), None)):
      logger.info(bstack1l1ll1_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠦࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡ࡫ࡶࠤࡺࡴࡤࡦࡴࡺࡥࡾ࠴ࠠࠣ୅"))
      bstack1l11ll1lll_opy_.bstack11ll11l1_opy_(driver, name=test.name, path=test.source)
def bstack1l1ll1l1_opy_(test, bstack1llll1ll1l_opy_):
    try:
      bstack1l1l1lll1_opy_ = datetime.datetime.now()
      data = {}
      if test:
        data[bstack1l1ll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ୆")] = bstack1llll1ll1l_opy_
      if bstack11l1lll1l_opy_:
        if bstack11l1lll1l_opy_.status == bstack1l1ll1_opy_ (u"ࠪࡔࡆ࡙ࡓࠨେ"):
          data[bstack1l1ll1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫୈ")] = bstack1l1ll1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ୉")
        elif bstack11l1lll1l_opy_.status == bstack1l1ll1_opy_ (u"࠭ࡆࡂࡋࡏࠫ୊"):
          data[bstack1l1ll1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧୋ")] = bstack1l1ll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨୌ")
          if bstack11l1lll1l_opy_.message:
            data[bstack1l1ll1_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯୍ࠩ")] = str(bstack11l1lll1l_opy_.message)
      user = CONFIG[bstack1l1ll1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ୎")]
      key = CONFIG[bstack1l1ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ୏")]
      host = bstack111lll1l1_opy_(cli.config, [bstack1l1ll1_opy_ (u"ࠧࡧࡰࡪࡵࠥ୐"), bstack1l1ll1_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥࠣ୑"), bstack1l1ll1_opy_ (u"ࠢࡢࡲ࡬ࠦ୒")], bstack1l1ll1_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠤ୓"))
      url = bstack1l1ll1_opy_ (u"ࠩࡾࢁ࠴ࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡴࡧࡶࡷ࡮ࡵ࡮ࡴ࠱ࡾࢁ࠳ࡰࡳࡰࡰࠪ୔").format(host, bstack1l11l11ll_opy_)
      headers = {
        bstack1l1ll1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩ୕"): bstack1l1ll1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧୖ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers, auth=(user, key))
        cli.bstack11l1l1111l_opy_(bstack1l1ll1_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽ࡹࡵࡪࡡࡵࡧࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡸࡦࡺࡵࡴࠤୗ"), datetime.datetime.now() - bstack1l1l1lll1_opy_)
    except Exception as e:
      logger.error(bstack11l1ll11l_opy_.format(str(e)))
def bstack11111lll1_opy_(test, bstack1llll1ll1l_opy_):
  global CONFIG
  global bstack11l11lll1l_opy_
  global bstack111l1lll_opy_
  global bstack1l11l11ll_opy_
  global bstack11l1lll1l_opy_
  global bstack11111ll1_opy_
  global bstack1ll1ll1ll_opy_
  global bstack1ll1llll1_opy_
  global bstack11lllll11_opy_
  global bstack11l1111l1_opy_
  global bstack1ll1l11lll_opy_
  global bstack1ll111l11_opy_
  try:
    if not bstack1l11l11ll_opy_:
      with open(os.path.join(os.path.expanduser(bstack1l1ll1_opy_ (u"࠭ࡾࠨ୘")), bstack1l1ll1_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ୙"), bstack1l1ll1_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪ୚"))) as f:
        bstack111lll11_opy_ = json.loads(bstack1l1ll1_opy_ (u"ࠤࡾࠦ୛") + f.read().strip() + bstack1l1ll1_opy_ (u"ࠪࠦࡽࠨ࠺ࠡࠤࡼࠦࠬଡ଼") + bstack1l1ll1_opy_ (u"ࠦࢂࠨଢ଼"))
        bstack1l11l11ll_opy_ = bstack111lll11_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1ll1l11lll_opy_:
    for driver in bstack1ll1l11lll_opy_:
      if bstack1l11l11ll_opy_ == driver.session_id:
        if test:
          bstack1ll1l1l111_opy_(driver, test)
        bstack11111l1ll_opy_(driver, bstack1llll1ll1l_opy_)
  elif bstack1l11l11ll_opy_:
    bstack1l1ll1l1_opy_(test, bstack1llll1ll1l_opy_)
  if bstack11l11lll1l_opy_:
    bstack1ll1llll1_opy_(bstack11l11lll1l_opy_)
  if bstack111l1lll_opy_:
    bstack11lllll11_opy_(bstack111l1lll_opy_)
  if bstack1l11lll1l1_opy_:
    bstack11l1111l1_opy_()
def bstack1l111l1ll1_opy_(self, test, *args, **kwargs):
  bstack1llll1ll1l_opy_ = None
  if test:
    bstack1llll1ll1l_opy_ = str(test.name)
  bstack11111lll1_opy_(test, bstack1llll1ll1l_opy_)
  bstack1ll1ll1ll_opy_(self, test, *args, **kwargs)
def bstack1ll1ll11l_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1lll11111_opy_
  global CONFIG
  global bstack1ll1l11lll_opy_
  global bstack1l11l11ll_opy_
  bstack1llll1l1_opy_ = None
  try:
    if bstack11l1ll11ll_opy_(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ୞"), None) or bstack11l1ll11ll_opy_(threading.current_thread(), bstack1l1ll1_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨୟ"), None):
      try:
        if not bstack1l11l11ll_opy_:
          with open(os.path.join(os.path.expanduser(bstack1l1ll1_opy_ (u"ࠧࡿࠩୠ")), bstack1l1ll1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨୡ"), bstack1l1ll1_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫୢ"))) as f:
            bstack111lll11_opy_ = json.loads(bstack1l1ll1_opy_ (u"ࠥࡿࠧୣ") + f.read().strip() + bstack1l1ll1_opy_ (u"ࠫࠧࡾࠢ࠻ࠢࠥࡽࠧ࠭୤") + bstack1l1ll1_opy_ (u"ࠧࢃࠢ୥"))
            bstack1l11l11ll_opy_ = bstack111lll11_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack1ll1l11lll_opy_:
        for driver in bstack1ll1l11lll_opy_:
          if bstack1l11l11ll_opy_ == driver.session_id:
            bstack1llll1l1_opy_ = driver
    bstack1l1111l11l_opy_ = bstack1l11ll1lll_opy_.bstack11l11l11_opy_(test.tags)
    if bstack1llll1l1_opy_:
      threading.current_thread().isA11yTest = bstack1l11ll1lll_opy_.bstack1llll1l11_opy_(bstack1llll1l1_opy_, bstack1l1111l11l_opy_)
      threading.current_thread().isAppA11yTest = bstack1l11ll1lll_opy_.bstack1llll1l11_opy_(bstack1llll1l1_opy_, bstack1l1111l11l_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1l1111l11l_opy_
      threading.current_thread().isAppA11yTest = bstack1l1111l11l_opy_
  except:
    pass
  bstack1lll11111_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack11l1lll1l_opy_
  try:
    bstack11l1lll1l_opy_ = self._test
  except:
    bstack11l1lll1l_opy_ = self.test
def bstack1l1l1l11l_opy_():
  global bstack1l1l1lll11_opy_
  try:
    if os.path.exists(bstack1l1l1lll11_opy_):
      os.remove(bstack1l1l1lll11_opy_)
  except Exception as e:
    logger.debug(bstack1l1ll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡦࡨࡰࡪࡺࡩ࡯ࡩࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺ࠡࠩ୦") + str(e))
def bstack11ll1l1lll_opy_():
  global bstack1l1l1lll11_opy_
  bstack1lllll1l1l_opy_ = {}
  try:
    if not os.path.isfile(bstack1l1l1lll11_opy_):
      with open(bstack1l1l1lll11_opy_, bstack1l1ll1_opy_ (u"ࠧࡸࠩ୧")):
        pass
      with open(bstack1l1l1lll11_opy_, bstack1l1ll1_opy_ (u"ࠣࡹ࠮ࠦ୨")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1l1l1lll11_opy_):
      bstack1lllll1l1l_opy_ = json.load(open(bstack1l1l1lll11_opy_, bstack1l1ll1_opy_ (u"ࠩࡵࡦࠬ୩")))
  except Exception as e:
    logger.debug(bstack1l1ll1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡸࡥࡢࡦ࡬ࡲ࡬ࠦࡲࡰࡤࡲࡸࠥࡸࡥࡱࡱࡵࡸࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬ୪") + str(e))
  finally:
    return bstack1lllll1l1l_opy_
def bstack1lllll1ll1_opy_(platform_index, item_index):
  global bstack1l1l1lll11_opy_
  try:
    bstack1lllll1l1l_opy_ = bstack11ll1l1lll_opy_()
    bstack1lllll1l1l_opy_[item_index] = platform_index
    with open(bstack1l1l1lll11_opy_, bstack1l1ll1_opy_ (u"ࠦࡼ࠱ࠢ୫")) as outfile:
      json.dump(bstack1lllll1l1l_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1l1ll1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡸࡴ࡬ࡸ࡮ࡴࡧࠡࡶࡲࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪ୬") + str(e))
def bstack111111111_opy_(bstack1l1l11l1l_opy_):
  global CONFIG
  bstack1l111111l1_opy_ = bstack1l1ll1_opy_ (u"࠭ࠧ୭")
  if not bstack1l1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ୮") in CONFIG:
    logger.info(bstack1l1ll1_opy_ (u"ࠨࡐࡲࠤࡵࡲࡡࡵࡨࡲࡶࡲࡹࠠࡱࡣࡶࡷࡪࡪࠠࡶࡰࡤࡦࡱ࡫ࠠࡵࡱࠣ࡫ࡪࡴࡥࡳࡣࡷࡩࠥࡸࡥࡱࡱࡵࡸࠥ࡬࡯ࡳࠢࡕࡳࡧࡵࡴࠡࡴࡸࡲࠬ୯"))
  try:
    platform = CONFIG[bstack1l1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ୰")][bstack1l1l11l1l_opy_]
    if bstack1l1ll1_opy_ (u"ࠪࡳࡸ࠭ୱ") in platform:
      bstack1l111111l1_opy_ += str(platform[bstack1l1ll1_opy_ (u"ࠫࡴࡹࠧ୲")]) + bstack1l1ll1_opy_ (u"ࠬ࠲ࠠࠨ୳")
    if bstack1l1ll1_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ୴") in platform:
      bstack1l111111l1_opy_ += str(platform[bstack1l1ll1_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪ୵")]) + bstack1l1ll1_opy_ (u"ࠨ࠮ࠣࠫ୶")
    if bstack1l1ll1_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭୷") in platform:
      bstack1l111111l1_opy_ += str(platform[bstack1l1ll1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧ୸")]) + bstack1l1ll1_opy_ (u"ࠫ࠱ࠦࠧ୹")
    if bstack1l1ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ୺") in platform:
      bstack1l111111l1_opy_ += str(platform[bstack1l1ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ୻")]) + bstack1l1ll1_opy_ (u"ࠧ࠭ࠢࠪ୼")
    if bstack1l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭୽") in platform:
      bstack1l111111l1_opy_ += str(platform[bstack1l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ୾")]) + bstack1l1ll1_opy_ (u"ࠪ࠰ࠥ࠭୿")
    if bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ஀") in platform:
      bstack1l111111l1_opy_ += str(platform[bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭஁")]) + bstack1l1ll1_opy_ (u"࠭ࠬࠡࠩஂ")
  except Exception as e:
    logger.debug(bstack1l1ll1_opy_ (u"ࠧࡔࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡱࡩࡷࡧࡴࡪࡰࡪࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡳࡵࡴ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡶࡪࡶ࡯ࡳࡶࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡴࡴࠧஃ") + str(e))
  finally:
    if bstack1l111111l1_opy_[len(bstack1l111111l1_opy_) - 2:] == bstack1l1ll1_opy_ (u"ࠨ࠮ࠣࠫ஄"):
      bstack1l111111l1_opy_ = bstack1l111111l1_opy_[:-2]
    return bstack1l111111l1_opy_
def bstack1ll11lll_opy_(path, bstack1l111111l1_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1l1111llll_opy_ = ET.parse(path)
    bstack11l11ll1l_opy_ = bstack1l1111llll_opy_.getroot()
    bstack1ll1ll1lll_opy_ = None
    for suite in bstack11l11ll1l_opy_.iter(bstack1l1ll1_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨஅ")):
      if bstack1l1ll1_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪஆ") in suite.attrib:
        suite.attrib[bstack1l1ll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩஇ")] += bstack1l1ll1_opy_ (u"ࠬࠦࠧஈ") + bstack1l111111l1_opy_
        bstack1ll1ll1lll_opy_ = suite
    bstack1l1l111lll_opy_ = None
    for robot in bstack11l11ll1l_opy_.iter(bstack1l1ll1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬஉ")):
      bstack1l1l111lll_opy_ = robot
    bstack11l111llll_opy_ = len(bstack1l1l111lll_opy_.findall(bstack1l1ll1_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭ஊ")))
    if bstack11l111llll_opy_ == 1:
      bstack1l1l111lll_opy_.remove(bstack1l1l111lll_opy_.findall(bstack1l1ll1_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧ஋"))[0])
      bstack1111lllll_opy_ = ET.Element(bstack1l1ll1_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨ஌"), attrib={bstack1l1ll1_opy_ (u"ࠪࡲࡦࡳࡥࠨ஍"): bstack1l1ll1_opy_ (u"ࠫࡘࡻࡩࡵࡧࡶࠫஎ"), bstack1l1ll1_opy_ (u"ࠬ࡯ࡤࠨஏ"): bstack1l1ll1_opy_ (u"࠭ࡳ࠱ࠩஐ")})
      bstack1l1l111lll_opy_.insert(1, bstack1111lllll_opy_)
      bstack1l1ll1ll11_opy_ = None
      for suite in bstack1l1l111lll_opy_.iter(bstack1l1ll1_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭஑")):
        bstack1l1ll1ll11_opy_ = suite
      bstack1l1ll1ll11_opy_.append(bstack1ll1ll1lll_opy_)
      bstack1l111ll1l1_opy_ = None
      for status in bstack1ll1ll1lll_opy_.iter(bstack1l1ll1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨஒ")):
        bstack1l111ll1l1_opy_ = status
      bstack1l1ll1ll11_opy_.append(bstack1l111ll1l1_opy_)
    bstack1l1111llll_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1l1ll1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡲࡴ࡫ࡱ࡫ࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠧஓ") + str(e))
def bstack1lll1l1l1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1lll111111_opy_
  global CONFIG
  if bstack1l1ll1_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࡳࡥࡹ࡮ࠢஔ") in options:
    del options[bstack1l1ll1_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡴࡦࡺࡨࠣக")]
  bstack1ll1l1llll_opy_ = bstack11ll1l1lll_opy_()
  for bstack11ll1l1111_opy_ in bstack1ll1l1llll_opy_.keys():
    path = os.path.join(os.getcwd(), bstack1l1ll1_opy_ (u"ࠬࡶࡡࡣࡱࡷࡣࡷ࡫ࡳࡶ࡮ࡷࡷࠬ஖"), str(bstack11ll1l1111_opy_), bstack1l1ll1_opy_ (u"࠭࡯ࡶࡶࡳࡹࡹ࠴ࡸ࡮࡮ࠪ஗"))
    bstack1ll11lll_opy_(path, bstack111111111_opy_(bstack1ll1l1llll_opy_[bstack11ll1l1111_opy_]))
  bstack1l1l1l11l_opy_()
  return bstack1lll111111_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack11llllll_opy_(self, ff_profile_dir):
  global bstack11l111l1l1_opy_
  if not ff_profile_dir:
    return None
  return bstack11l111l1l1_opy_(self, ff_profile_dir)
def bstack11ll1ll111_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1111ll11l_opy_
  bstack1ll1lll1ll_opy_ = []
  if bstack1l1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ஘") in CONFIG:
    bstack1ll1lll1ll_opy_ = CONFIG[bstack1l1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫங")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1l1ll1_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࠥச")],
      pabot_args[bstack1l1ll1_opy_ (u"ࠥࡺࡪࡸࡢࡰࡵࡨࠦ஛")],
      argfile,
      pabot_args.get(bstack1l1ll1_opy_ (u"ࠦ࡭࡯ࡶࡦࠤஜ")),
      pabot_args[bstack1l1ll1_opy_ (u"ࠧࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠣ஝")],
      platform[0],
      bstack1111ll11l_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1l1ll1_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡧ࡫࡯ࡩࡸࠨஞ")] or [(bstack1l1ll1_opy_ (u"ࠢࠣட"), None)]
    for platform in enumerate(bstack1ll1lll1ll_opy_)
  ]
def bstack11llll111l_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1111111ll_opy_=bstack1l1ll1_opy_ (u"ࠨࠩ஠")):
  global bstack11l1111l11_opy_
  self.platform_index = platform_index
  self.bstack111ll1ll_opy_ = bstack1111111ll_opy_
  bstack11l1111l11_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1ll1l1l1ll_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack11l1l11ll_opy_
  global bstack1ll1ll1l1_opy_
  bstack1l1l11lll1_opy_ = copy.deepcopy(item)
  if not bstack1l1ll1_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ஡") in item.options:
    bstack1l1l11lll1_opy_.options[bstack1l1ll1_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ஢")] = []
  bstack1llll11l1l_opy_ = bstack1l1l11lll1_opy_.options[bstack1l1ll1_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ண")].copy()
  for v in bstack1l1l11lll1_opy_.options[bstack1l1ll1_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧத")]:
    if bstack1l1ll1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬ஥") in v:
      bstack1llll11l1l_opy_.remove(v)
    if bstack1l1ll1_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙ࠧ஦") in v:
      bstack1llll11l1l_opy_.remove(v)
    if bstack1l1ll1_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡅࡇࡉࡐࡔࡉࡁࡍࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬ஧") in v:
      bstack1llll11l1l_opy_.remove(v)
  bstack1llll11l1l_opy_.insert(0, bstack1l1ll1_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘ࠻ࡽࢀࠫந").format(bstack1l1l11lll1_opy_.platform_index))
  bstack1llll11l1l_opy_.insert(0, bstack1l1ll1_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡇࡉࡋࡒࡏࡄࡃࡏࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘ࠺ࡼࡿࠪன").format(bstack1l1l11lll1_opy_.bstack111ll1ll_opy_))
  bstack1l1l11lll1_opy_.options[bstack1l1ll1_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ப")] = bstack1llll11l1l_opy_
  if bstack1ll1ll1l1_opy_:
    bstack1l1l11lll1_opy_.options[bstack1l1ll1_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ஫")].insert(0, bstack1l1ll1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘࡀࡻࡾࠩ஬").format(bstack1ll1ll1l1_opy_))
  return bstack11l1l11ll_opy_(caller_id, datasources, is_last, bstack1l1l11lll1_opy_, outs_dir)
def bstack1111l11ll_opy_(command, item_index):
  if bstack11lll111ll_opy_.get_property(bstack1l1ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ஭")):
    os.environ[bstack1l1ll1_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩம")] = json.dumps(CONFIG[bstack1l1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬய")][item_index % bstack1l111l11_opy_])
  global bstack1ll1ll1l1_opy_
  if bstack1ll1ll1l1_opy_:
    command[0] = command[0].replace(bstack1l1ll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩர"), bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡷࡩࡱࠠࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠡ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠠࠨற") + str(
      item_index) + bstack1l1ll1_opy_ (u"ࠬࠦࠧல") + bstack1ll1ll1l1_opy_, 1)
  else:
    command[0] = command[0].replace(bstack1l1ll1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬள"),
                                    bstack1l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡳࡥ࡭ࠣࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠤ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠣࠫழ") + str(item_index), 1)
def bstack1l1ll11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1l111lll1l_opy_
  bstack1111l11ll_opy_(command, item_index)
  return bstack1l111lll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack11l1ll1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1l111lll1l_opy_
  bstack1111l11ll_opy_(command, item_index)
  return bstack1l111lll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1l11llllll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1l111lll1l_opy_
  bstack1111l11ll_opy_(command, item_index)
  return bstack1l111lll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack1llll11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack1l111lll1l_opy_
  bstack1111l11ll_opy_(command, item_index)
  return bstack1l111lll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack1lll111l1_opy_(self, runner, quiet=False, capture=True):
  global bstack1l1l1l111_opy_
  bstack1ll1l111ll_opy_ = bstack1l1l1l111_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack1l1ll1_opy_ (u"ࠨࡧࡻࡧࡪࡶࡴࡪࡱࡱࡣࡦࡸࡲࠨவ")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1l1ll1_opy_ (u"ࠩࡨࡼࡨࡥࡴࡳࡣࡦࡩࡧࡧࡣ࡬ࡡࡤࡶࡷ࠭ஶ")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1ll1l111ll_opy_
def bstack1lllllll1l_opy_(runner, hook_name, context, element, bstack1llll11ll1_opy_, *args):
  try:
    if runner.hooks.get(hook_name):
      bstack1ll1111l1_opy_.bstack111ll1ll1_opy_(hook_name, element)
    bstack1llll11ll1_opy_(runner, hook_name, context, *args)
    if runner.hooks.get(hook_name):
      bstack1ll1111l1_opy_.bstack11l1lllll_opy_(element)
      if hook_name not in [bstack1l1ll1_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠧஷ"), bstack1l1ll1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡥࡱࡲࠧஸ")] and args and hasattr(args[0], bstack1l1ll1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡣࡲ࡫ࡳࡴࡣࡪࡩࠬஹ")):
        args[0].error_message = bstack1l1ll1_opy_ (u"࠭ࠧ஺")
  except Exception as e:
    logger.debug(bstack1l1ll1_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣ࡬ࡦࡴࡤ࡭ࡧࠣ࡬ࡴࡵ࡫ࡴࠢ࡬ࡲࠥࡨࡥࡩࡣࡹࡩ࠿ࠦࡻࡾࠩ஻").format(str(e)))
@measure(event_name=EVENTS.bstack1l1lll11ll_opy_, stage=STAGE.bstack1l1ll11ll1_opy_, hook_type=bstack1l1ll1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡂ࡮࡯ࠦ஼"), bstack1llll1ll1l_opy_=bstack11111ll1_opy_)
def bstack11l11l1l1l_opy_(runner, name, context, bstack1llll11ll1_opy_, *args):
    if runner.hooks.get(bstack1l1ll1_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨ஽")).__name__ != bstack1l1ll1_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲ࡟ࡥࡧࡩࡥࡺࡲࡴࡠࡪࡲࡳࡰࠨா"):
      bstack1lllllll1l_opy_(runner, name, context, runner, bstack1llll11ll1_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack1ll1lll1l_opy_(bstack1l1ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪி")) else context.browser
      runner.driver_initialised = bstack1l1ll1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤீ")
    except Exception as e:
      logger.debug(bstack1l1ll1_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡤࡳ࡫ࡹࡩࡷࠦࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡧࠣࡥࡹࡺࡲࡪࡤࡸࡸࡪࡀࠠࡼࡿࠪு").format(str(e)))
def bstack1ll1lll11_opy_(runner, name, context, bstack1llll11ll1_opy_, *args):
    bstack1lllllll1l_opy_(runner, name, context, context.feature, bstack1llll11ll1_opy_, *args)
    try:
      if not bstack1l111llll1_opy_:
        bstack1llll1l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll1lll1l_opy_(bstack1l1ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ூ")) else context.browser
        if is_driver_active(bstack1llll1l1_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack1l1ll1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠤ௃")
          bstack11l11ll1_opy_ = str(runner.feature.name)
          bstack11l11l1lll_opy_(context, bstack11l11ll1_opy_)
          bstack1llll1l1_opy_.execute_script(bstack1l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧ௄") + json.dumps(bstack11l11ll1_opy_) + bstack1l1ll1_opy_ (u"ࠪࢁࢂ࠭௅"))
    except Exception as e:
      logger.debug(bstack1l1ll1_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣ࡭ࡳࠦࡢࡦࡨࡲࡶࡪࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫெ").format(str(e)))
def bstack11ll1llll1_opy_(runner, name, context, bstack1llll11ll1_opy_, *args):
    if hasattr(context, bstack1l1ll1_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧே")):
        bstack1ll1111l1_opy_.start_test(context)
    target = context.scenario if hasattr(context, bstack1l1ll1_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨை")) else context.feature
    bstack1lllllll1l_opy_(runner, name, context, target, bstack1llll11ll1_opy_, *args)
@measure(event_name=EVENTS.bstack1l1ll1l1l_opy_, stage=STAGE.bstack1l1ll11ll1_opy_, bstack1llll1ll1l_opy_=bstack11111ll1_opy_)
def bstack11l1l1l1ll_opy_(runner, name, context, bstack1llll11ll1_opy_, *args):
    if len(context.scenario.tags) == 0: bstack1ll1111l1_opy_.start_test(context)
    bstack1lllllll1l_opy_(runner, name, context, context.scenario, bstack1llll11ll1_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack11ll1lll1_opy_.bstack111llll1_opy_(context, *args)
    try:
      bstack1llll1l1_opy_ = bstack11l1ll11ll_opy_(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭௉"), context.browser)
      if is_driver_active(bstack1llll1l1_opy_):
        bstack1l1lll1l_opy_.bstack11l11l1l_opy_(bstack11l1ll11ll_opy_(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧொ"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack1l1ll1_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦோ")
        if (not bstack1l111llll1_opy_):
          scenario_name = args[0].name
          feature_name = bstack11l11ll1_opy_ = str(runner.feature.name)
          bstack11l11ll1_opy_ = feature_name + bstack1l1ll1_opy_ (u"ࠪࠤ࠲ࠦࠧௌ") + scenario_name
          if runner.driver_initialised == bstack1l1ll1_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨ்"):
            bstack11l11l1lll_opy_(context, bstack11l11ll1_opy_)
            bstack1llll1l1_opy_.execute_script(bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ௎") + json.dumps(bstack11l11ll1_opy_) + bstack1l1ll1_opy_ (u"࠭ࡽࡾࠩ௏"))
    except Exception as e:
      logger.debug(bstack1l1ll1_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡧࡪࡴࡡࡳ࡫ࡲ࠾ࠥࢁࡽࠨௐ").format(str(e)))
@measure(event_name=EVENTS.bstack1l1lll11ll_opy_, stage=STAGE.bstack1l1ll11ll1_opy_, hook_type=bstack1l1ll1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡔࡶࡨࡴࠧ௑"), bstack1llll1ll1l_opy_=bstack11111ll1_opy_)
def bstack11ll11lll_opy_(runner, name, context, bstack1llll11ll1_opy_, *args):
    bstack1lllllll1l_opy_(runner, name, context, args[0], bstack1llll11ll1_opy_, *args)
    try:
      bstack1llll1l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll1lll1l_opy_(bstack1l1ll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ௒")) else context.browser
      if is_driver_active(bstack1llll1l1_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack1l1ll1_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣ௓")
        bstack1ll1111l1_opy_.bstack111ll11ll_opy_(args[0])
        if runner.driver_initialised == bstack1l1ll1_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤ௔"):
          feature_name = bstack11l11ll1_opy_ = str(runner.feature.name)
          bstack11l11ll1_opy_ = feature_name + bstack1l1ll1_opy_ (u"ࠬࠦ࠭ࠡࠩ௕") + context.scenario.name
          bstack1llll1l1_opy_.execute_script(bstack1l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫ௖") + json.dumps(bstack11l11ll1_opy_) + bstack1l1ll1_opy_ (u"ࠧࡾࡿࠪௗ"))
    except Exception as e:
      logger.debug(bstack1l1ll1_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡹ࡫ࡰ࠻ࠢࡾࢁࠬ௘").format(str(e)))
@measure(event_name=EVENTS.bstack1l1lll11ll_opy_, stage=STAGE.bstack1l1ll11ll1_opy_, hook_type=bstack1l1ll1_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࡔࡶࡨࡴࠧ௙"), bstack1llll1ll1l_opy_=bstack11111ll1_opy_)
def bstack111l11lll_opy_(runner, name, context, bstack1llll11ll1_opy_, *args):
  bstack1ll1111l1_opy_.bstack1l111ll1ll_opy_(args[0])
  try:
    bstack11l1111ll_opy_ = args[0].status.name
    bstack1llll1l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1ll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ௚") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack1llll1l1_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack1l1ll1_opy_ (u"ࠫ࡮ࡴࡳࡵࡧࡳࠫ௛")
        feature_name = bstack11l11ll1_opy_ = str(runner.feature.name)
        bstack11l11ll1_opy_ = feature_name + bstack1l1ll1_opy_ (u"ࠬࠦ࠭ࠡࠩ௜") + context.scenario.name
        bstack1llll1l1_opy_.execute_script(bstack1l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫ௝") + json.dumps(bstack11l11ll1_opy_) + bstack1l1ll1_opy_ (u"ࠧࡾࡿࠪ௞"))
    if str(bstack11l1111ll_opy_).lower() == bstack1l1ll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ௟"):
      bstack11l111l11l_opy_ = bstack1l1ll1_opy_ (u"ࠩࠪ௠")
      bstack11l11111ll_opy_ = bstack1l1ll1_opy_ (u"ࠪࠫ௡")
      bstack11l1lll1l1_opy_ = bstack1l1ll1_opy_ (u"ࠫࠬ௢")
      try:
        import traceback
        bstack11l111l11l_opy_ = runner.exception.__class__.__name__
        bstack11l111ll1l_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack11l11111ll_opy_ = bstack1l1ll1_opy_ (u"ࠬࠦࠧ௣").join(bstack11l111ll1l_opy_)
        bstack11l1lll1l1_opy_ = bstack11l111ll1l_opy_[-1]
      except Exception as e:
        logger.debug(bstack1lllllllll_opy_.format(str(e)))
      bstack11l111l11l_opy_ += bstack11l1lll1l1_opy_
      bstack1ll11lllll_opy_(context, json.dumps(str(args[0].name) + bstack1l1ll1_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧ௤") + str(bstack11l11111ll_opy_)),
                          bstack1l1ll1_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨ௥"))
      if runner.driver_initialised == bstack1l1ll1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨ௦"):
        bstack1ll1111l11_opy_(getattr(context, bstack1l1ll1_opy_ (u"ࠩࡳࡥ࡬࡫ࠧ௧"), None), bstack1l1ll1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ௨"), bstack11l111l11l_opy_)
        bstack1llll1l1_opy_.execute_script(bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ௩") + json.dumps(str(args[0].name) + bstack1l1ll1_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦ௪") + str(bstack11l11111ll_opy_)) + bstack1l1ll1_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥࢁࢂ࠭௫"))
      if runner.driver_initialised == bstack1l1ll1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧ௬"):
        bstack1l1ll1lll1_opy_(bstack1llll1l1_opy_, bstack1l1ll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ௭"), bstack1l1ll1_opy_ (u"ࠤࡖࡧࡪࡴࡡࡳ࡫ࡲࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨ௮") + str(bstack11l111l11l_opy_))
    else:
      bstack1ll11lllll_opy_(context, bstack1l1ll1_opy_ (u"ࠥࡔࡦࡹࡳࡦࡦࠤࠦ௯"), bstack1l1ll1_opy_ (u"ࠦ࡮ࡴࡦࡰࠤ௰"))
      if runner.driver_initialised == bstack1l1ll1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥ௱"):
        bstack1ll1111l11_opy_(getattr(context, bstack1l1ll1_opy_ (u"࠭ࡰࡢࡩࡨࠫ௲"), None), bstack1l1ll1_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ௳"))
      bstack1llll1l1_opy_.execute_script(bstack1l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭௴") + json.dumps(str(args[0].name) + bstack1l1ll1_opy_ (u"ࠤࠣ࠱ࠥࡖࡡࡴࡵࡨࡨࠦࠨ௵")) + bstack1l1ll1_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩ௶"))
      if runner.driver_initialised == bstack1l1ll1_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤ௷"):
        bstack1l1ll1lll1_opy_(bstack1llll1l1_opy_, bstack1l1ll1_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ௸"))
  except Exception as e:
    logger.debug(bstack1l1ll1_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࠣࡷࡹ࡫ࡰ࠻ࠢࡾࢁࠬ௹").format(str(e)))
  bstack1lllllll1l_opy_(runner, name, context, args[0], bstack1llll11ll1_opy_, *args)
@measure(event_name=EVENTS.bstack1111ll1ll_opy_, stage=STAGE.bstack1l1ll11ll1_opy_, bstack1llll1ll1l_opy_=bstack11111ll1_opy_)
def bstack111l1llll_opy_(runner, name, context, bstack1llll11ll1_opy_, *args):
  bstack1ll1111l1_opy_.end_test(args[0])
  try:
    bstack1lll11l11l_opy_ = args[0].status.name
    bstack1llll1l1_opy_ = bstack11l1ll11ll_opy_(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭௺"), context.browser)
    bstack11ll1lll1_opy_.bstack1l1l11l1l1_opy_(bstack1llll1l1_opy_)
    if str(bstack1lll11l11l_opy_).lower() == bstack1l1ll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ௻"):
      bstack11l111l11l_opy_ = bstack1l1ll1_opy_ (u"ࠩࠪ௼")
      bstack11l11111ll_opy_ = bstack1l1ll1_opy_ (u"ࠪࠫ௽")
      bstack11l1lll1l1_opy_ = bstack1l1ll1_opy_ (u"ࠫࠬ௾")
      try:
        import traceback
        bstack11l111l11l_opy_ = runner.exception.__class__.__name__
        bstack11l111ll1l_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack11l11111ll_opy_ = bstack1l1ll1_opy_ (u"ࠬࠦࠧ௿").join(bstack11l111ll1l_opy_)
        bstack11l1lll1l1_opy_ = bstack11l111ll1l_opy_[-1]
      except Exception as e:
        logger.debug(bstack1lllllllll_opy_.format(str(e)))
      bstack11l111l11l_opy_ += bstack11l1lll1l1_opy_
      bstack1ll11lllll_opy_(context, json.dumps(str(args[0].name) + bstack1l1ll1_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧఀ") + str(bstack11l11111ll_opy_)),
                          bstack1l1ll1_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨఁ"))
      if runner.driver_initialised == bstack1l1ll1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥం") or runner.driver_initialised == bstack1l1ll1_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩః"):
        bstack1ll1111l11_opy_(getattr(context, bstack1l1ll1_opy_ (u"ࠪࡴࡦ࡭ࡥࠨఄ"), None), bstack1l1ll1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦఅ"), bstack11l111l11l_opy_)
        bstack1llll1l1_opy_.execute_script(bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪఆ") + json.dumps(str(args[0].name) + bstack1l1ll1_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧఇ") + str(bstack11l11111ll_opy_)) + bstack1l1ll1_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦࢂࢃࠧఈ"))
      if runner.driver_initialised == bstack1l1ll1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥఉ") or runner.driver_initialised == bstack1l1ll1_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩఊ"):
        bstack1l1ll1lll1_opy_(bstack1llll1l1_opy_, bstack1l1ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪఋ"), bstack1l1ll1_opy_ (u"ࠦࡘࡩࡥ࡯ࡣࡵ࡭ࡴࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࡢ࡮ࠣఌ") + str(bstack11l111l11l_opy_))
    else:
      bstack1ll11lllll_opy_(context, bstack1l1ll1_opy_ (u"ࠧࡖࡡࡴࡵࡨࡨࠦࠨ఍"), bstack1l1ll1_opy_ (u"ࠨࡩ࡯ࡨࡲࠦఎ"))
      if runner.driver_initialised == bstack1l1ll1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤఏ") or runner.driver_initialised == bstack1l1ll1_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨఐ"):
        bstack1ll1111l11_opy_(getattr(context, bstack1l1ll1_opy_ (u"ࠩࡳࡥ࡬࡫ࠧ఑"), None), bstack1l1ll1_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥఒ"))
      bstack1llll1l1_opy_.execute_script(bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩఓ") + json.dumps(str(args[0].name) + bstack1l1ll1_opy_ (u"ࠧࠦ࠭ࠡࡒࡤࡷࡸ࡫ࡤࠢࠤఔ")) + bstack1l1ll1_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤࢀࢁࠬక"))
      if runner.driver_initialised == bstack1l1ll1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤఖ") or runner.driver_initialised == bstack1l1ll1_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨగ"):
        bstack1l1ll1lll1_opy_(bstack1llll1l1_opy_, bstack1l1ll1_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤఘ"))
  except Exception as e:
    logger.debug(bstack1l1ll1_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡯࡮ࠡࡣࡩࡸࡪࡸࠠࡧࡧࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬఙ").format(str(e)))
  bstack1lllllll1l_opy_(runner, name, context, context.scenario, bstack1llll11ll1_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack1ll11lll11_opy_(runner, name, context, bstack1llll11ll1_opy_, *args):
    target = context.scenario if hasattr(context, bstack1l1ll1_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭చ")) else context.feature
    bstack1lllllll1l_opy_(runner, name, context, target, bstack1llll11ll1_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack1l111ll1_opy_(runner, name, context, bstack1llll11ll1_opy_, *args):
    try:
      bstack1llll1l1_opy_ = bstack11l1ll11ll_opy_(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫఛ"), context.browser)
      bstack1l1l1lll_opy_ = bstack1l1ll1_opy_ (u"࠭ࠧజ")
      if context.failed is True:
        bstack1ll11111_opy_ = []
        bstack1lll1ll1ll_opy_ = []
        bstack11l1lll111_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack1ll11111_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack11l111ll1l_opy_ = traceback.format_tb(exc_tb)
            bstack11l11111_opy_ = bstack1l1ll1_opy_ (u"ࠧࠡࠩఝ").join(bstack11l111ll1l_opy_)
            bstack1lll1ll1ll_opy_.append(bstack11l11111_opy_)
            bstack11l1lll111_opy_.append(bstack11l111ll1l_opy_[-1])
        except Exception as e:
          logger.debug(bstack1lllllllll_opy_.format(str(e)))
        bstack11l111l11l_opy_ = bstack1l1ll1_opy_ (u"ࠨࠩఞ")
        for i in range(len(bstack1ll11111_opy_)):
          bstack11l111l11l_opy_ += bstack1ll11111_opy_[i] + bstack11l1lll111_opy_[i] + bstack1l1ll1_opy_ (u"ࠩ࡟ࡲࠬట")
        bstack1l1l1lll_opy_ = bstack1l1ll1_opy_ (u"ࠪࠤࠬఠ").join(bstack1lll1ll1ll_opy_)
        if runner.driver_initialised in [bstack1l1ll1_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠧడ"), bstack1l1ll1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤఢ")]:
          bstack1ll11lllll_opy_(context, bstack1l1l1lll_opy_, bstack1l1ll1_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧణ"))
          bstack1ll1111l11_opy_(getattr(context, bstack1l1ll1_opy_ (u"ࠧࡱࡣࡪࡩࠬత"), None), bstack1l1ll1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣథ"), bstack11l111l11l_opy_)
          bstack1llll1l1_opy_.execute_script(bstack1l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧద") + json.dumps(bstack1l1l1lll_opy_) + bstack1l1ll1_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪధ"))
          bstack1l1ll1lll1_opy_(bstack1llll1l1_opy_, bstack1l1ll1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦన"), bstack1l1ll1_opy_ (u"࡙ࠧ࡯࡮ࡧࠣࡷࡨ࡫࡮ࡢࡴ࡬ࡳࡸࠦࡦࡢ࡫࡯ࡩࡩࡀࠠ࡝ࡰࠥ఩") + str(bstack11l111l11l_opy_))
          bstack111l1l1ll_opy_ = bstack1llllll1l1_opy_(bstack1l1l1lll_opy_, runner.feature.name, logger)
          if (bstack111l1l1ll_opy_ != None):
            bstack1l1ll111ll_opy_.append(bstack111l1l1ll_opy_)
      else:
        if runner.driver_initialised in [bstack1l1ll1_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠢప"), bstack1l1ll1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦఫ")]:
          bstack1ll11lllll_opy_(context, bstack1l1ll1_opy_ (u"ࠣࡈࡨࡥࡹࡻࡲࡦ࠼ࠣࠦబ") + str(runner.feature.name) + bstack1l1ll1_opy_ (u"ࠤࠣࡴࡦࡹࡳࡦࡦࠤࠦభ"), bstack1l1ll1_opy_ (u"ࠥ࡭ࡳ࡬࡯ࠣమ"))
          bstack1ll1111l11_opy_(getattr(context, bstack1l1ll1_opy_ (u"ࠫࡵࡧࡧࡦࠩయ"), None), bstack1l1ll1_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧర"))
          bstack1llll1l1_opy_.execute_script(bstack1l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫఱ") + json.dumps(bstack1l1ll1_opy_ (u"ࠢࡇࡧࡤࡸࡺࡸࡥ࠻ࠢࠥల") + str(runner.feature.name) + bstack1l1ll1_opy_ (u"ࠣࠢࡳࡥࡸࡹࡥࡥࠣࠥళ")) + bstack1l1ll1_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧࢃࡽࠨఴ"))
          bstack1l1ll1lll1_opy_(bstack1llll1l1_opy_, bstack1l1ll1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪవ"))
          bstack111l1l1ll_opy_ = bstack1llllll1l1_opy_(bstack1l1l1lll_opy_, runner.feature.name, logger)
          if (bstack111l1l1ll_opy_ != None):
            bstack1l1ll111ll_opy_.append(bstack111l1l1ll_opy_)
    except Exception as e:
      logger.debug(bstack1l1ll1_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭శ").format(str(e)))
    bstack1lllllll1l_opy_(runner, name, context, context.feature, bstack1llll11ll1_opy_, *args)
@measure(event_name=EVENTS.bstack1l1lll11ll_opy_, stage=STAGE.bstack1l1ll11ll1_opy_, hook_type=bstack1l1ll1_opy_ (u"ࠧࡧࡦࡵࡧࡵࡅࡱࡲࠢష"), bstack1llll1ll1l_opy_=bstack11111ll1_opy_)
def bstack1lllll1lll_opy_(runner, name, context, bstack1llll11ll1_opy_, *args):
    bstack1lllllll1l_opy_(runner, name, context, runner, bstack1llll11ll1_opy_, *args)
def bstack11llll1l1l_opy_(self, name, context, *args):
  if bstack11l11l111_opy_:
    platform_index = int(threading.current_thread()._name) % bstack1l111l11_opy_
    bstack1l1l1l1lll_opy_ = CONFIG[bstack1l1ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩస")][platform_index]
    os.environ[bstack1l1ll1_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨహ")] = json.dumps(bstack1l1l1l1lll_opy_)
  global bstack1llll11ll1_opy_
  if not hasattr(self, bstack1l1ll1_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡶࡩࡩ࠭఺")):
    self.driver_initialised = None
  bstack1ll1l11l1l_opy_ = {
      bstack1l1ll1_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱ࠭఻"): bstack11l11l1l1l_opy_,
      bstack1l1ll1_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨ఼ࠫ"): bstack1ll1lll11_opy_,
      bstack1l1ll1_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡹࡧࡧࠨఽ"): bstack11ll1llll1_opy_,
      bstack1l1ll1_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧా"): bstack11l1l1l1ll_opy_,
      bstack1l1ll1_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠫి"): bstack11ll11lll_opy_,
      bstack1l1ll1_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡵࡧࡳࠫీ"): bstack111l11lll_opy_,
      bstack1l1ll1_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩు"): bstack111l1llll_opy_,
      bstack1l1ll1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡶࡤ࡫ࠬూ"): bstack1ll11lll11_opy_,
      bstack1l1ll1_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪృ"): bstack1l111ll1_opy_,
      bstack1l1ll1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡥࡱࡲࠧౄ"): bstack1lllll1lll_opy_
  }
  handler = bstack1ll1l11l1l_opy_.get(name, bstack1llll11ll1_opy_)
  handler(self, name, context, bstack1llll11ll1_opy_, *args)
  if name in [bstack1l1ll1_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬ౅"), bstack1l1ll1_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧె"), bstack1l1ll1_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪే")]:
    try:
      bstack1llll1l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll1lll1l_opy_(bstack1l1ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧై")) else context.browser
      bstack1l11ll1l1_opy_ = (
        (name == bstack1l1ll1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠬ౉") and self.driver_initialised == bstack1l1ll1_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢొ")) or
        (name == bstack1l1ll1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫో") and self.driver_initialised == bstack1l1ll1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨౌ")) or
        (name == bstack1l1ll1_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵ్ࠧ") and self.driver_initialised in [bstack1l1ll1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤ౎"), bstack1l1ll1_opy_ (u"ࠣ࡫ࡱࡷࡹ࡫ࡰࠣ౏")]) or
        (name == bstack1l1ll1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡷࡩࡵ࠭౐") and self.driver_initialised == bstack1l1ll1_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣ౑"))
      )
      if bstack1l11ll1l1_opy_:
        self.driver_initialised = None
        bstack1llll1l1_opy_.quit()
    except Exception:
      pass
def bstack1ll11llll1_opy_(config, startdir):
  return bstack1l1ll1_opy_ (u"ࠦࡩࡸࡩࡷࡧࡵ࠾ࠥࢁ࠰ࡾࠤ౒").format(bstack1l1ll1_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦ౓"))
notset = Notset()
def bstack11l1l1l1l1_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1lll1lll1l_opy_
  if str(name).lower() == bstack1l1ll1_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷ࠭౔"):
    return bstack1l1ll1_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨౕ")
  else:
    return bstack1lll1lll1l_opy_(self, name, default, skip)
def bstack1111llll1_opy_(item, when):
  global bstack1l11l1lll_opy_
  try:
    bstack1l11l1lll_opy_(item, when)
  except Exception as e:
    pass
def bstack1ll11l11l1_opy_():
  return
def bstack111111ll1_opy_(type, name, status, reason, bstack1lll1111_opy_, bstack11ll1111ll_opy_):
  bstack1llllllll1_opy_ = {
    bstack1l1ll1_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨౖ"): type,
    bstack1l1ll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ౗"): {}
  }
  if type == bstack1l1ll1_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬౘ"):
    bstack1llllllll1_opy_[bstack1l1ll1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧౙ")][bstack1l1ll1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫౚ")] = bstack1lll1111_opy_
    bstack1llllllll1_opy_[bstack1l1ll1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ౛")][bstack1l1ll1_opy_ (u"ࠧࡥࡣࡷࡥࠬ౜")] = json.dumps(str(bstack11ll1111ll_opy_))
  if type == bstack1l1ll1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩౝ"):
    bstack1llllllll1_opy_[bstack1l1ll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ౞")][bstack1l1ll1_opy_ (u"ࠪࡲࡦࡳࡥࠨ౟")] = name
  if type == bstack1l1ll1_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧౠ"):
    bstack1llllllll1_opy_[bstack1l1ll1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨౡ")][bstack1l1ll1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ౢ")] = status
    if status == bstack1l1ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧౣ"):
      bstack1llllllll1_opy_[bstack1l1ll1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ౤")][bstack1l1ll1_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩ౥")] = json.dumps(str(reason))
  bstack11lllllll_opy_ = bstack1l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨ౦").format(json.dumps(bstack1llllllll1_opy_))
  return bstack11lllllll_opy_
def bstack11l11l11l1_opy_(driver_command, response):
    if driver_command == bstack1l1ll1_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨ౧"):
        bstack1l1lll1l_opy_.bstack1l1l1111ll_opy_({
            bstack1l1ll1_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫ౨"): response[bstack1l1ll1_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬ౩")],
            bstack1l1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ౪"): bstack1l1lll1l_opy_.current_test_uuid()
        })
def bstack11l1l1lll_opy_(item, call, rep):
  global bstack1l1lll1l11_opy_
  global bstack1ll1l11lll_opy_
  global bstack1l111llll1_opy_
  name = bstack1l1ll1_opy_ (u"ࠨࠩ౫")
  try:
    if rep.when == bstack1l1ll1_opy_ (u"ࠩࡦࡥࡱࡲࠧ౬"):
      bstack1l11l11ll_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1l111llll1_opy_:
          name = str(rep.nodeid)
          bstack1lllllll11_opy_ = bstack111111ll1_opy_(bstack1l1ll1_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ౭"), name, bstack1l1ll1_opy_ (u"ࠫࠬ౮"), bstack1l1ll1_opy_ (u"ࠬ࠭౯"), bstack1l1ll1_opy_ (u"࠭ࠧ౰"), bstack1l1ll1_opy_ (u"ࠧࠨ౱"))
          threading.current_thread().bstack11l11ll11l_opy_ = name
          for driver in bstack1ll1l11lll_opy_:
            if bstack1l11l11ll_opy_ == driver.session_id:
              driver.execute_script(bstack1lllllll11_opy_)
      except Exception as e:
        logger.debug(bstack1l1ll1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨ౲").format(str(e)))
      try:
        bstack1l111l1lll_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack1l1ll1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ౳"):
          status = bstack1l1ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ౴") if rep.outcome.lower() == bstack1l1ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ౵") else bstack1l1ll1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ౶")
          reason = bstack1l1ll1_opy_ (u"࠭ࠧ౷")
          if status == bstack1l1ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ౸"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack1l1ll1_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭౹") if status == bstack1l1ll1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ౺") else bstack1l1ll1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ౻")
          data = name + bstack1l1ll1_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭౼") if status == bstack1l1ll1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ౽") else name + bstack1l1ll1_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠡࠡࠩ౾") + reason
          bstack1ll1lllll_opy_ = bstack111111ll1_opy_(bstack1l1ll1_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩ౿"), bstack1l1ll1_opy_ (u"ࠨࠩಀ"), bstack1l1ll1_opy_ (u"ࠩࠪಁ"), bstack1l1ll1_opy_ (u"ࠪࠫಂ"), level, data)
          for driver in bstack1ll1l11lll_opy_:
            if bstack1l11l11ll_opy_ == driver.session_id:
              driver.execute_script(bstack1ll1lllll_opy_)
      except Exception as e:
        logger.debug(bstack1l1ll1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡥࡲࡲࡹ࡫ࡸࡵࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨಃ").format(str(e)))
  except Exception as e:
    logger.debug(bstack1l1ll1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡵࡷࡥࡹ࡫ࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻࡾࠩ಄").format(str(e)))
  bstack1l1lll1l11_opy_(item, call, rep)
def bstack111l1ll1_opy_(driver, bstack1111111l_opy_, test=None):
  global bstack111l1111_opy_
  if test != None:
    bstack1l111l111_opy_ = getattr(test, bstack1l1ll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫಅ"), None)
    bstack1lll11l1ll_opy_ = getattr(test, bstack1l1ll1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬಆ"), None)
    PercySDK.screenshot(driver, bstack1111111l_opy_, bstack1l111l111_opy_=bstack1l111l111_opy_, bstack1lll11l1ll_opy_=bstack1lll11l1ll_opy_, bstack1l1l1l1l11_opy_=bstack111l1111_opy_)
  else:
    PercySDK.screenshot(driver, bstack1111111l_opy_)
@measure(event_name=EVENTS.bstack11l1l11l1_opy_, stage=STAGE.bstack1l1ll11ll1_opy_, bstack1llll1ll1l_opy_=bstack11111ll1_opy_)
def bstack1lll1ll1_opy_(driver):
  if bstack1lll11l1l1_opy_.bstack1l1lllll1_opy_() is True or bstack1lll11l1l1_opy_.capturing() is True:
    return
  bstack1lll11l1l1_opy_.bstack1l1l11llll_opy_()
  while not bstack1lll11l1l1_opy_.bstack1l1lllll1_opy_():
    bstack1l111lllll_opy_ = bstack1lll11l1l1_opy_.bstack1lll111l_opy_()
    bstack111l1ll1_opy_(driver, bstack1l111lllll_opy_)
  bstack1lll11l1l1_opy_.bstack1111l11l_opy_()
def bstack1l111l111l_opy_(sequence, driver_command, response = None, bstack1lllll11l1_opy_ = None, args = None):
    try:
      if sequence != bstack1l1ll1_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨಇ"):
        return
      if percy.bstack1ll1111lll_opy_() == bstack1l1ll1_opy_ (u"ࠤࡩࡥࡱࡹࡥࠣಈ"):
        return
      bstack1l111lllll_opy_ = bstack11l1ll11ll_opy_(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠪࡴࡪࡸࡣࡺࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ಉ"), None)
      for command in bstack11111l1l_opy_:
        if command == driver_command:
          for driver in bstack1ll1l11lll_opy_:
            bstack1lll1ll1_opy_(driver)
      bstack11l1ll1l11_opy_ = percy.bstack11llll1l11_opy_()
      if driver_command in bstack1lll11l1l_opy_[bstack11l1ll1l11_opy_]:
        bstack1lll11l1l1_opy_.bstack1llllllll_opy_(bstack1l111lllll_opy_, driver_command)
    except Exception as e:
      pass
def bstack111ll1l1l_opy_(framework_name):
  if bstack11lll111ll_opy_.get_property(bstack1l1ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨಊ")):
      return
  bstack11lll111ll_opy_.bstack11l1l1ll_opy_(bstack1l1ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩಋ"), True)
  global bstack1l11lll1l_opy_
  global bstack11l1l1ll11_opy_
  global bstack11l1ll1ll1_opy_
  bstack1l11lll1l_opy_ = framework_name
  logger.info(bstack11l111l1l_opy_.format(bstack1l11lll1l_opy_.split(bstack1l1ll1_opy_ (u"࠭࠭ࠨಌ"))[0]))
  bstack1lll1lll1_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack11l11l111_opy_:
      Service.start = bstack1l1ll11l_opy_
      Service.stop = bstack1lll1l11_opy_
      webdriver.Remote.get = bstack1lllll1ll_opy_
      WebDriver.quit = bstack11lll1ll11_opy_
      webdriver.Remote.__init__ = bstack11llll1ll_opy_
    if not bstack11l11l111_opy_:
        webdriver.Remote.__init__ = bstack1l11l1l111_opy_
    WebDriver.getAccessibilityResults = getAccessibilityResults
    WebDriver.get_accessibility_results = getAccessibilityResults
    WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
    WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
    WebDriver.performScan = perform_scan
    WebDriver.perform_scan = perform_scan
    WebDriver.execute = bstack11ll1ll1l_opy_
    bstack11l1l1ll11_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack11l11l111_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1lll11lll1_opy_
  except Exception as e:
    pass
  bstack1l1l1lllll_opy_()
  if not bstack11l1l1ll11_opy_:
    bstack1l1l1llll1_opy_(bstack1l1ll1_opy_ (u"ࠢࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠢࡱࡳࡹࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠤ಍"), bstack1l1l1111l1_opy_)
  if bstack11ll11111l_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      if hasattr(RemoteConnection, bstack1l1ll1_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩಎ")) and callable(getattr(RemoteConnection, bstack1l1ll1_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪಏ"))):
        RemoteConnection._get_proxy_url = bstack1l111ll11l_opy_
      else:
        from selenium.webdriver.remote.client_config import ClientConfig
        ClientConfig.get_proxy_url = bstack1l111ll11l_opy_
    except Exception as e:
      logger.error(bstack11lll1l11_opy_.format(str(e)))
  if bstack1ll1l1ll11_opy_():
    bstack11ll11l11l_opy_(CONFIG, logger)
  if (bstack1l1ll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩಐ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if percy.bstack1ll1111lll_opy_() == bstack1l1ll1_opy_ (u"ࠦࡹࡸࡵࡦࠤ಑"):
          bstack11l1l1111_opy_(bstack1l111l111l_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack11llllll_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1l11111ll_opy_
      except Exception as e:
        logger.warn(bstack1l1ll11l1_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack111l1l111_opy_
      except Exception as e:
        logger.debug(bstack1ll11ll111_opy_ + str(e))
    except Exception as e:
      bstack1l1l1llll1_opy_(e, bstack1l1ll11l1_opy_)
    Output.start_test = bstack111lll1ll_opy_
    Output.end_test = bstack1l111l1ll1_opy_
    TestStatus.__init__ = bstack1ll1ll11l_opy_
    QueueItem.__init__ = bstack11llll111l_opy_
    pabot._create_items = bstack11ll1ll111_opy_
    try:
      from pabot import __version__ as bstack1ll1l11l11_opy_
      if version.parse(bstack1ll1l11l11_opy_) >= version.parse(bstack1l1ll1_opy_ (u"ࠬ࠺࠮࠳࠰࠳ࠫಒ")):
        pabot._run = bstack1llll11ll_opy_
      elif version.parse(bstack1ll1l11l11_opy_) >= version.parse(bstack1l1ll1_opy_ (u"࠭࠲࠯࠳࠸࠲࠵࠭ಓ")):
        pabot._run = bstack1l11llllll_opy_
      elif version.parse(bstack1ll1l11l11_opy_) >= version.parse(bstack1l1ll1_opy_ (u"ࠧ࠳࠰࠴࠷࠳࠶ࠧಔ")):
        pabot._run = bstack11l1ll1ll_opy_
      else:
        pabot._run = bstack1l1ll11ll_opy_
    except Exception as e:
      pabot._run = bstack1l1ll11ll_opy_
    pabot._create_command_for_execution = bstack1ll1l1l1ll_opy_
    pabot._report_results = bstack1lll1l1l1_opy_
  if bstack1l1ll1_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨಕ") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l1l1llll1_opy_(e, bstack1l1l1ll11_opy_)
    Runner.run_hook = bstack11llll1l1l_opy_
    Step.run = bstack1lll111l1_opy_
  if bstack1l1ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩಖ") in str(framework_name).lower():
    if not bstack11l11l111_opy_:
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack1ll11llll1_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1ll11l11l1_opy_
      Config.getoption = bstack11l1l1l1l1_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack11l1l1lll_opy_
    except Exception as e:
      pass
def bstack111ll111_opy_():
  global CONFIG
  if bstack1l1ll1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪಗ") in CONFIG and int(CONFIG[bstack1l1ll1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫಘ")]) > 1:
    logger.warn(bstack1llll1ll1_opy_)
def bstack11ll1l1l1_opy_(arg, bstack1ll11l1l_opy_, bstack1lll1ll111_opy_=None):
  global CONFIG
  global bstack1l1ll1l11l_opy_
  global bstack1l1lllllll_opy_
  global bstack11l11l111_opy_
  global bstack11lll111ll_opy_
  bstack11ll1l111_opy_ = bstack1l1ll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬಙ")
  if bstack1ll11l1l_opy_ and isinstance(bstack1ll11l1l_opy_, str):
    bstack1ll11l1l_opy_ = eval(bstack1ll11l1l_opy_)
  CONFIG = bstack1ll11l1l_opy_[bstack1l1ll1_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭ಚ")]
  bstack1l1ll1l11l_opy_ = bstack1ll11l1l_opy_[bstack1l1ll1_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨಛ")]
  bstack1l1lllllll_opy_ = bstack1ll11l1l_opy_[bstack1l1ll1_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪಜ")]
  bstack11l11l111_opy_ = bstack1ll11l1l_opy_[bstack1l1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬಝ")]
  bstack11lll111ll_opy_.bstack11l1l1ll_opy_(bstack1l1ll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫಞ"), bstack11l11l111_opy_)
  os.environ[bstack1l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ಟ")] = bstack11ll1l111_opy_
  os.environ[bstack1l1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࠫಠ")] = json.dumps(CONFIG)
  os.environ[bstack1l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡎࡕࡃࡡࡘࡖࡑ࠭ಡ")] = bstack1l1ll1l11l_opy_
  os.environ[bstack1l1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨಢ")] = str(bstack1l1lllllll_opy_)
  os.environ[bstack1l1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡎࡘࡋࡎࡔࠧಣ")] = str(True)
  if bstack111ll1lll_opy_(arg, [bstack1l1ll1_opy_ (u"ࠩ࠰ࡲࠬತ"), bstack1l1ll1_opy_ (u"ࠪ࠱࠲ࡴࡵ࡮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫಥ")]) != -1:
    os.environ[bstack1l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡆࡘࡁࡍࡎࡈࡐࠬದ")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack111llll11_opy_)
    return
  bstack1l1111l1l_opy_()
  global bstack1l1l11l11l_opy_
  global bstack111l1111_opy_
  global bstack1111ll11l_opy_
  global bstack1ll1ll1l1_opy_
  global bstack1l1111ll_opy_
  global bstack11l1ll1ll1_opy_
  global bstack11111ll1l_opy_
  arg.append(bstack1l1ll1_opy_ (u"ࠧ࠳ࡗࠣಧ"))
  arg.append(bstack1l1ll1_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡀࡍࡰࡦࡸࡰࡪࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡪ࡯ࡳࡳࡷࡺࡥࡥ࠼ࡳࡽࡹ࡫ࡳࡵ࠰ࡓࡽࡹ࡫ࡳࡵ࡙ࡤࡶࡳ࡯࡮ࡨࠤನ"))
  arg.append(bstack1l1ll1_opy_ (u"ࠢ࠮࡙ࠥ಩"))
  arg.append(bstack1l1ll1_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡥ࠻ࡖ࡫ࡩࠥ࡮࡯ࡰ࡭࡬ࡱࡵࡲࠢಪ"))
  global bstack11llllll11_opy_
  global bstack111l11l1l_opy_
  global bstack11l11l1ll1_opy_
  global bstack1lll11111_opy_
  global bstack11l111l1l1_opy_
  global bstack11l1111l11_opy_
  global bstack11l1l11ll_opy_
  global bstack11ll11lll1_opy_
  global bstack1lll1ll11_opy_
  global bstack1lll1llll_opy_
  global bstack1lll1lll1l_opy_
  global bstack1l11l1lll_opy_
  global bstack1l1lll1l11_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11llllll11_opy_ = webdriver.Remote.__init__
    bstack111l11l1l_opy_ = WebDriver.quit
    bstack11ll11lll1_opy_ = WebDriver.close
    bstack1lll1ll11_opy_ = WebDriver.get
    bstack11l11l1ll1_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1l1lll111l_opy_(CONFIG) and bstack11l1l1l1l_opy_():
    if bstack1111l1l1l_opy_() < version.parse(bstack1ll1ll1111_opy_):
      logger.error(bstack1l1l1111l_opy_.format(bstack1111l1l1l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack1l1ll1_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪಫ")) and callable(getattr(RemoteConnection, bstack1l1ll1_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫಬ"))):
          bstack1lll1llll_opy_ = RemoteConnection._get_proxy_url
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          bstack1lll1llll_opy_ = ClientConfig.get_proxy_url
      except Exception as e:
        logger.error(bstack11lll1l11_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1lll1lll1l_opy_ = Config.getoption
    from _pytest import runner
    bstack1l11l1lll_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack1l111l11ll_opy_)
  try:
    from pytest_bdd import reporting
    bstack1l1lll1l11_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack1l1ll1_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡳࠥࡸࡵ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࡷࠬಭ"))
  bstack1111ll11l_opy_ = CONFIG.get(bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩಮ"), {}).get(bstack1l1ll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨಯ"))
  bstack11111ll1l_opy_ = True
  if cli.is_enabled(CONFIG):
    if cli.bstack1ll1lll1l1_opy_():
      bstack1l1l111l_opy_.invoke(bstack1l11111l1l_opy_.CONNECT, bstack1l1l1lll1l_opy_())
    platform_index = int(os.environ.get(bstack1l1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧರ"), bstack1l1ll1_opy_ (u"ࠨ࠲ࠪಱ")))
  else:
    bstack111ll1l1l_opy_(bstack11llll11ll_opy_)
  os.environ[bstack1l1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪಲ")] = CONFIG[bstack1l1ll1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬಳ")]
  os.environ[bstack1l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧ಴")] = CONFIG[bstack1l1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨವ")]
  os.environ[bstack1l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩಶ")] = bstack11l11l111_opy_.__str__()
  from _pytest.config import main as bstack1llll1ll11_opy_
  bstack1l1111l1ll_opy_ = []
  try:
    bstack1l1111l11_opy_ = bstack1llll1ll11_opy_(arg)
    if cli.is_enabled(CONFIG):
      cli.bstack1l11111l_opy_()
    if bstack1l1ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷࠫಷ") in multiprocessing.current_process().__dict__.keys():
      for bstack1ll111lll_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1l1111l1ll_opy_.append(bstack1ll111lll_opy_)
    try:
      bstack1lll1l1l_opy_ = (bstack1l1111l1ll_opy_, int(bstack1l1111l11_opy_))
      bstack1lll1ll111_opy_.append(bstack1lll1l1l_opy_)
    except:
      bstack1lll1ll111_opy_.append((bstack1l1111l1ll_opy_, bstack1l1111l11_opy_))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack1l1111l1ll_opy_.append({bstack1l1ll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ಸ"): bstack1l1ll1_opy_ (u"ࠩࡓࡶࡴࡩࡥࡴࡵࠣࠫಹ") + os.environ.get(bstack1l1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ಺")), bstack1l1ll1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ಻"): traceback.format_exc(), bstack1l1ll1_opy_ (u"ࠬ࡯࡮ࡥࡧࡻ಼ࠫ"): int(os.environ.get(bstack1l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ಽ")))})
    bstack1lll1ll111_opy_.append((bstack1l1111l1ll_opy_, 1))
def mod_behave_main(args, retries):
  try:
    from behave.configuration import Configuration
    from behave.__main__ import run_behave
    from browserstack_sdk.bstack_behave_runner import BehaveRunner
    config = Configuration(args)
    config.update_userdata({bstack1l1ll1_opy_ (u"ࠢࡳࡧࡷࡶ࡮࡫ࡳࠣಾ"): str(retries)})
    return run_behave(config, runner_class=BehaveRunner)
  except Exception as e:
    bstack111ll1l1_opy_ = e.__class__.__name__
    print(bstack1l1ll1_opy_ (u"ࠣࠧࡶ࠾ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡨࡥࡩࡣࡹࡩࠥࡺࡥࡴࡶࠣࠩࡸࠨಿ") % (bstack111ll1l1_opy_, e))
    return 1
def bstack1l11llll_opy_(arg):
  global bstack1l1lll1111_opy_
  bstack111ll1l1l_opy_(bstack1ll111l11l_opy_)
  os.environ[bstack1l1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪೀ")] = str(bstack1l1lllllll_opy_)
  retries = bstack11l1ll1l1_opy_.bstack1l1111l111_opy_(CONFIG)
  status_code = 0
  if bstack11l1ll1l1_opy_.bstack1ll1ll1ll1_opy_(CONFIG):
    status_code = mod_behave_main(arg, retries)
  else:
    from behave.__main__ import main as bstack1llll111l_opy_
    status_code = bstack1llll111l_opy_(arg)
  if status_code != 0:
    bstack1l1lll1111_opy_ = status_code
def bstack11l1lll1ll_opy_():
  logger.info(bstack1ll1ll11l1_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1l1ll1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩು"), help=bstack1l1ll1_opy_ (u"ࠫࡌ࡫࡮ࡦࡴࡤࡸࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡩ࡯࡯ࡨ࡬࡫ࠬೂ"))
  parser.add_argument(bstack1l1ll1_opy_ (u"ࠬ࠳ࡵࠨೃ"), bstack1l1ll1_opy_ (u"࠭࠭࠮ࡷࡶࡩࡷࡴࡡ࡮ࡧࠪೄ"), help=bstack1l1ll1_opy_ (u"࡚ࠧࡱࡸࡶࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡺࡹࡥࡳࡰࡤࡱࡪ࠭೅"))
  parser.add_argument(bstack1l1ll1_opy_ (u"ࠨ࠯࡮ࠫೆ"), bstack1l1ll1_opy_ (u"ࠩ࠰࠱ࡰ࡫ࡹࠨೇ"), help=bstack1l1ll1_opy_ (u"ࠪ࡝ࡴࡻࡲࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡢࡥࡦࡩࡸࡹࠠ࡬ࡧࡼࠫೈ"))
  parser.add_argument(bstack1l1ll1_opy_ (u"ࠫ࠲࡬ࠧ೉"), bstack1l1ll1_opy_ (u"ࠬ࠳࠭ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪೊ"), help=bstack1l1ll1_opy_ (u"࡙࠭ࡰࡷࡵࠤࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬೋ"))
  bstack11l1l111l1_opy_ = parser.parse_args()
  try:
    bstack1ll11ll1ll_opy_ = bstack1l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡧࡦࡰࡨࡶ࡮ࡩ࠮ࡺ࡯࡯࠲ࡸࡧ࡭ࡱ࡮ࡨࠫೌ")
    if bstack11l1l111l1_opy_.framework and bstack11l1l111l1_opy_.framework not in (bstack1l1ll1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ್"), bstack1l1ll1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪ೎")):
      bstack1ll11ll1ll_opy_ = bstack1l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯࠳ࡿ࡭࡭࠰ࡶࡥࡲࡶ࡬ࡦࠩ೏")
    bstack1l11l1l11_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll11ll1ll_opy_)
    bstack1ll1111ll1_opy_ = open(bstack1l11l1l11_opy_, bstack1l1ll1_opy_ (u"ࠫࡷ࠭೐"))
    bstack11l11l1l1_opy_ = bstack1ll1111ll1_opy_.read()
    bstack1ll1111ll1_opy_.close()
    if bstack11l1l111l1_opy_.username:
      bstack11l11l1l1_opy_ = bstack11l11l1l1_opy_.replace(bstack1l1ll1_opy_ (u"ࠬ࡟ࡏࡖࡔࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬ೑"), bstack11l1l111l1_opy_.username)
    if bstack11l1l111l1_opy_.key:
      bstack11l11l1l1_opy_ = bstack11l11l1l1_opy_.replace(bstack1l1ll1_opy_ (u"࡙࠭ࡐࡗࡕࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨ೒"), bstack11l1l111l1_opy_.key)
    if bstack11l1l111l1_opy_.framework:
      bstack11l11l1l1_opy_ = bstack11l11l1l1_opy_.replace(bstack1l1ll1_opy_ (u"࡚ࠧࡑࡘࡖࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ೓"), bstack11l1l111l1_opy_.framework)
    file_name = bstack1l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫ೔")
    file_path = os.path.abspath(file_name)
    bstack11l1ll1111_opy_ = open(file_path, bstack1l1ll1_opy_ (u"ࠩࡺࠫೕ"))
    bstack11l1ll1111_opy_.write(bstack11l11l1l1_opy_)
    bstack11l1ll1111_opy_.close()
    logger.info(bstack1ll1l1l1_opy_)
    try:
      os.environ[bstack1l1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬೖ")] = bstack11l1l111l1_opy_.framework if bstack11l1l111l1_opy_.framework != None else bstack1l1ll1_opy_ (u"ࠦࠧ೗")
      config = yaml.safe_load(bstack11l11l1l1_opy_)
      config[bstack1l1ll1_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ೘")] = bstack1l1ll1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡳࡦࡶࡸࡴࠬ೙")
      bstack1lll1l1ll1_opy_(bstack1l11lll1_opy_, config)
    except Exception as e:
      logger.debug(bstack1l1lll111_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack111lllll_opy_.format(str(e)))
def bstack1lll1l1ll1_opy_(bstack1111l1ll1_opy_, config, bstack1l1l1ll1ll_opy_={}):
  global bstack11l11l111_opy_
  global bstack11lll111l1_opy_
  global bstack11lll111ll_opy_
  if not config:
    return
  bstack1ll1l1111_opy_ = bstack1l111ll1l_opy_ if not bstack11l11l111_opy_ else (
    bstack1lllll11l_opy_ if bstack1l1ll1_opy_ (u"ࠧࡢࡲࡳࠫ೚") in config else (
        bstack11l11llll1_opy_ if config.get(bstack1l1ll1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ೛")) else bstack1l1ll1l1l1_opy_
    )
)
  bstack1lll111lll_opy_ = False
  bstack111l1l11_opy_ = False
  if bstack11l11l111_opy_ is True:
      if bstack1l1ll1_opy_ (u"ࠩࡤࡴࡵ࠭೜") in config:
          bstack1lll111lll_opy_ = True
      else:
          bstack111l1l11_opy_ = True
  bstack1lll1l1l11_opy_ = bstack1lllll11_opy_.bstack11l1lllll1_opy_(config, bstack11lll111l1_opy_)
  bstack1l1l1111_opy_ = bstack11ll1l1l11_opy_()
  data = {
    bstack1l1ll1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬೝ"): config[bstack1l1ll1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ೞ")],
    bstack1l1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ೟"): config[bstack1l1ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩೠ")],
    bstack1l1ll1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫೡ"): bstack1111l1ll1_opy_,
    bstack1l1ll1_opy_ (u"ࠨࡦࡨࡸࡪࡩࡴࡦࡦࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬೢ"): os.environ.get(bstack1l1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫೣ"), bstack11lll111l1_opy_),
    bstack1l1ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ೤"): bstack11l1ll1l1l_opy_,
    bstack1l1ll1_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠭೥"): bstack1l11lll11l_opy_(),
    bstack1l1ll1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨ೦"): {
      bstack1l1ll1_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ೧"): str(config[bstack1l1ll1_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ೨")]) if bstack1l1ll1_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ೩") in config else bstack1l1ll1_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࠥ೪"),
      bstack1l1ll1_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩ࡛࡫ࡲࡴ࡫ࡲࡲࠬ೫"): sys.version,
      bstack1l1ll1_opy_ (u"ࠫࡷ࡫ࡦࡦࡴࡵࡩࡷ࠭೬"): bstack11111l11l_opy_(os.environ.get(bstack1l1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ೭"), bstack11lll111l1_opy_)),
      bstack1l1ll1_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨ೮"): bstack1l1ll1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ೯"),
      bstack1l1ll1_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩ೰"): bstack1ll1l1111_opy_,
      bstack1l1ll1_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧೱ"): bstack1lll1l1l11_opy_,
      bstack1l1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡣࡺࡻࡩࡥࠩೲ"): os.environ[bstack1l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩೳ")],
      bstack1l1ll1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ೴"): os.environ.get(bstack1l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ೵"), bstack11lll111l1_opy_),
      bstack1l1ll1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪ೶"): bstack11l111l1_opy_(os.environ.get(bstack1l1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪ೷"), bstack11lll111l1_opy_)),
      bstack1l1ll1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ೸"): bstack1l1l1111_opy_.get(bstack1l1ll1_opy_ (u"ࠪࡲࡦࡳࡥࠨ೹")),
      bstack1l1ll1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪ೺"): bstack1l1l1111_opy_.get(bstack1l1ll1_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭೻")),
      bstack1l1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ೼"): config[bstack1l1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ೽")] if config[bstack1l1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ೾")] else bstack1l1ll1_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࠥ೿"),
      bstack1l1ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬഀ"): str(config[bstack1l1ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ഁ")]) if bstack1l1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧം") in config else bstack1l1ll1_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢഃ"),
      bstack1l1ll1_opy_ (u"ࠧࡰࡵࠪഄ"): sys.platform,
      bstack1l1ll1_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪഅ"): socket.gethostname(),
      bstack1l1ll1_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫആ"): bstack11lll111ll_opy_.get_property(bstack1l1ll1_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࠬഇ"))
    }
  }
  if not bstack11lll111ll_opy_.get_property(bstack1l1ll1_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡘ࡯ࡧ࡯ࡣ࡯ࠫഈ")) is None:
    data[bstack1l1ll1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨഉ")][bstack1l1ll1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡎࡧࡷࡥࡩࡧࡴࡢࠩഊ")] = {
      bstack1l1ll1_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧഋ"): bstack1l1ll1_opy_ (u"ࠨࡷࡶࡩࡷࡥ࡫ࡪ࡮࡯ࡩࡩ࠭ഌ"),
      bstack1l1ll1_opy_ (u"ࠩࡶ࡭࡬ࡴࡡ࡭ࠩ഍"): bstack11lll111ll_opy_.get_property(bstack1l1ll1_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪഎ")),
      bstack1l1ll1_opy_ (u"ࠫࡸ࡯ࡧ࡯ࡣ࡯ࡒࡺࡳࡢࡦࡴࠪഏ"): bstack11lll111ll_opy_.get_property(bstack1l1ll1_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱࡔ࡯ࠨഐ"))
    }
  if bstack1111l1ll1_opy_ == bstack11ll1ll1ll_opy_:
    data[bstack1l1ll1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩ഑")][bstack1l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡉ࡯࡯ࡨ࡬࡫ࠬഒ")] = bstack111l11ll1_opy_(config)
    data[bstack1l1ll1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫഓ")][bstack1l1ll1_opy_ (u"ࠩ࡬ࡷࡕ࡫ࡲࡤࡻࡄࡹࡹࡵࡅ࡯ࡣࡥࡰࡪࡪࠧഔ")] = percy.bstack11l1llll1l_opy_
    data[bstack1l1ll1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭ക")][bstack1l1ll1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡅࡹ࡮ࡲࡤࡊࡦࠪഖ")] = percy.percy_build_id
  if not bstack11l1ll1l1_opy_.bstack1ll111l111_opy_(CONFIG):
    data[bstack1l1ll1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨഗ")][bstack1l1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠪഘ")] = bstack11l1ll1l1_opy_.bstack1ll111l111_opy_(CONFIG)
  bstack1l1l111ll_opy_ = bstack11l111lll1_opy_.bstack11ll1l11l_opy_(CONFIG, logger)
  bstack111l11ll_opy_ = bstack11l1ll1l1_opy_.bstack11ll1l11l_opy_(config=CONFIG)
  if bstack1l1l111ll_opy_ is not None and bstack111l11ll_opy_ is not None and bstack111l11ll_opy_.bstack1l1l1ll1_opy_():
    data[bstack1l1ll1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪങ")][bstack111l11ll_opy_.bstack1lll1lll11_opy_()] = bstack1l1l111ll_opy_.bstack1lll111ll1_opy_()
  update(data[bstack1l1ll1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫച")], bstack1l1l1ll1ll_opy_)
  try:
    response = bstack1l1ll1ll1l_opy_(bstack1l1ll1_opy_ (u"ࠩࡓࡓࡘ࡚ࠧഛ"), bstack1l11l1l1_opy_(bstack1l1l1l1l1_opy_), data, {
      bstack1l1ll1_opy_ (u"ࠪࡥࡺࡺࡨࠨജ"): (config[bstack1l1ll1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ഝ")], config[bstack1l1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨഞ")])
    })
    if response:
      logger.debug(bstack1ll1l1lll_opy_.format(bstack1111l1ll1_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack11111111l_opy_.format(str(e)))
def bstack11111l11l_opy_(framework):
  return bstack1l1ll1_opy_ (u"ࠨࡻࡾ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࡼࡿࠥട").format(str(framework), __version__) if framework else bstack1l1ll1_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴ࢁࡽࠣഠ").format(
    __version__)
def bstack1l1111l1l_opy_():
  global CONFIG
  global bstack111111l11_opy_
  if bool(CONFIG):
    return
  try:
    bstack1ll11llll_opy_()
    logger.debug(bstack11lllll1ll_opy_.format(str(CONFIG)))
    bstack111111l11_opy_ = bstack11lll1ll_opy_.bstack111l1lll1_opy_(CONFIG, bstack111111l11_opy_)
    bstack1lll1lll1_opy_()
  except Exception as e:
    logger.error(bstack1l1ll1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࡶࡲ࠯ࠤࡪࡸࡲࡰࡴ࠽ࠤࠧഡ") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1l11lllll1_opy_
  atexit.register(bstack11ll1l1ll_opy_)
  signal.signal(signal.SIGINT, bstack1l11ll11l_opy_)
  signal.signal(signal.SIGTERM, bstack1l11ll11l_opy_)
def bstack1l11lllll1_opy_(exctype, value, traceback):
  global bstack1ll1l11lll_opy_
  try:
    for driver in bstack1ll1l11lll_opy_:
      bstack1l1ll1lll1_opy_(driver, bstack1l1ll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩഢ"), bstack1l1ll1_opy_ (u"ࠥࡗࡪࡹࡳࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨണ") + str(value))
  except Exception:
    pass
  logger.info(bstack11ll11llll_opy_)
  bstack11lll11l11_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack11lll11l11_opy_(message=bstack1l1ll1_opy_ (u"ࠫࠬത"), bstack1llll1111_opy_ = False):
  global CONFIG
  bstack11l1ll1lll_opy_ = bstack1l1ll1_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠧഥ") if bstack1llll1111_opy_ else bstack1l1ll1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬദ")
  try:
    if message:
      bstack1l1l1ll1ll_opy_ = {
        bstack11l1ll1lll_opy_ : str(message)
      }
      bstack1lll1l1ll1_opy_(bstack11ll1ll1ll_opy_, CONFIG, bstack1l1l1ll1ll_opy_)
    else:
      bstack1lll1l1ll1_opy_(bstack11ll1ll1ll_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack11l11ll11_opy_.format(str(e)))
def bstack1l1l1l1l_opy_(bstack1ll1llll1l_opy_, size):
  bstack1l11l1l1l_opy_ = []
  while len(bstack1ll1llll1l_opy_) > size:
    bstack111l111ll_opy_ = bstack1ll1llll1l_opy_[:size]
    bstack1l11l1l1l_opy_.append(bstack111l111ll_opy_)
    bstack1ll1llll1l_opy_ = bstack1ll1llll1l_opy_[size:]
  bstack1l11l1l1l_opy_.append(bstack1ll1llll1l_opy_)
  return bstack1l11l1l1l_opy_
def bstack11lll11ll_opy_(args):
  if bstack1l1ll1_opy_ (u"ࠧ࠮࡯ࠪധ") in args and bstack1l1ll1_opy_ (u"ࠨࡲࡧࡦࠬന") in args:
    return True
  return False
@measure(event_name=EVENTS.bstack1l1l11ll11_opy_, stage=STAGE.bstack111lll111_opy_)
def run_on_browserstack(bstack1l1111l1l1_opy_=None, bstack1lll1ll111_opy_=None, bstack11l1l11l11_opy_=False):
  global CONFIG
  global bstack1l1ll1l11l_opy_
  global bstack1l1lllllll_opy_
  global bstack11lll111l1_opy_
  global bstack11lll111ll_opy_
  bstack11ll1l111_opy_ = bstack1l1ll1_opy_ (u"ࠩࠪഩ")
  bstack1l1l11l111_opy_(bstack1ll11l1lll_opy_, logger)
  if bstack1l1111l1l1_opy_ and isinstance(bstack1l1111l1l1_opy_, str):
    bstack1l1111l1l1_opy_ = eval(bstack1l1111l1l1_opy_)
  if bstack1l1111l1l1_opy_:
    CONFIG = bstack1l1111l1l1_opy_[bstack1l1ll1_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪപ")]
    bstack1l1ll1l11l_opy_ = bstack1l1111l1l1_opy_[bstack1l1ll1_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬഫ")]
    bstack1l1lllllll_opy_ = bstack1l1111l1l1_opy_[bstack1l1ll1_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧബ")]
    bstack11lll111ll_opy_.bstack11l1l1ll_opy_(bstack1l1ll1_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨഭ"), bstack1l1lllllll_opy_)
    bstack11ll1l111_opy_ = bstack1l1ll1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧമ")
  bstack11lll111ll_opy_.bstack11l1l1ll_opy_(bstack1l1ll1_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪയ"), uuid4().__str__())
  logger.info(bstack1l1ll1_opy_ (u"ࠩࡖࡈࡐࠦࡲࡶࡰࠣࡷࡹࡧࡲࡵࡧࡧࠤࡼ࡯ࡴࡩࠢ࡬ࡨ࠿ࠦࠧര") + bstack11lll111ll_opy_.get_property(bstack1l1ll1_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࠬറ")));
  logger.debug(bstack1l1ll1_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩࡃࠧല") + bstack11lll111ll_opy_.get_property(bstack1l1ll1_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪࠧള")))
  if not bstack11l1l11l11_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack111llll11_opy_)
      return
    if sys.argv[1] == bstack1l1ll1_opy_ (u"࠭࠭࠮ࡸࡨࡶࡸ࡯࡯࡯ࠩഴ") or sys.argv[1] == bstack1l1ll1_opy_ (u"ࠧ࠮ࡸࠪവ"):
      logger.info(bstack1l1ll1_opy_ (u"ࠨࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡑࡻࡷ࡬ࡴࡴࠠࡔࡆࡎࠤࡻࢁࡽࠨശ").format(__version__))
      return
    if sys.argv[1] == bstack1l1ll1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨഷ"):
      bstack11l1lll1ll_opy_()
      return
  args = sys.argv
  bstack1l1111l1l_opy_()
  global bstack1l1l11l11l_opy_
  global bstack1l111l11_opy_
  global bstack11111ll1l_opy_
  global bstack111lllll1_opy_
  global bstack111l1111_opy_
  global bstack1111ll11l_opy_
  global bstack1ll1ll1l1_opy_
  global bstack1l1llll1l_opy_
  global bstack1l1111ll_opy_
  global bstack11l1ll1ll1_opy_
  global bstack11ll1l11ll_opy_
  bstack1l111l11_opy_ = len(CONFIG.get(bstack1l1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭സ"), []))
  if not bstack11ll1l111_opy_:
    if args[1] == bstack1l1ll1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫഹ") or args[1] == bstack1l1ll1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠸࠭ഺ"):
      bstack11ll1l111_opy_ = bstack1l1ll1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ഻࠭")
      args = args[2:]
    elif args[1] == bstack1l1ll1_opy_ (u"ࠧࡳࡱࡥࡳࡹ഼࠭"):
      bstack11ll1l111_opy_ = bstack1l1ll1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧഽ")
      args = args[2:]
    elif args[1] == bstack1l1ll1_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨാ"):
      bstack11ll1l111_opy_ = bstack1l1ll1_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩി")
      args = args[2:]
    elif args[1] == bstack1l1ll1_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬീ"):
      bstack11ll1l111_opy_ = bstack1l1ll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ു")
      args = args[2:]
    elif args[1] == bstack1l1ll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ൂ"):
      bstack11ll1l111_opy_ = bstack1l1ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧൃ")
      args = args[2:]
    elif args[1] == bstack1l1ll1_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨൄ"):
      bstack11ll1l111_opy_ = bstack1l1ll1_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ൅")
      args = args[2:]
    else:
      if not bstack1l1ll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭െ") in CONFIG or str(CONFIG[bstack1l1ll1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧേ")]).lower() in [bstack1l1ll1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬൈ"), bstack1l1ll1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧ൉")]:
        bstack11ll1l111_opy_ = bstack1l1ll1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧൊ")
        args = args[1:]
      elif str(CONFIG[bstack1l1ll1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫോ")]).lower() == bstack1l1ll1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨൌ"):
        bstack11ll1l111_opy_ = bstack1l1ll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ്ࠩ")
        args = args[1:]
      elif str(CONFIG[bstack1l1ll1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧൎ")]).lower() == bstack1l1ll1_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ൏"):
        bstack11ll1l111_opy_ = bstack1l1ll1_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ൐")
        args = args[1:]
      elif str(CONFIG[bstack1l1ll1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ൑")]).lower() == bstack1l1ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ൒"):
        bstack11ll1l111_opy_ = bstack1l1ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ൓")
        args = args[1:]
      elif str(CONFIG[bstack1l1ll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ൔ")]).lower() == bstack1l1ll1_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫൕ"):
        bstack11ll1l111_opy_ = bstack1l1ll1_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬൖ")
        args = args[1:]
      else:
        os.environ[bstack1l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨൗ")] = bstack11ll1l111_opy_
        bstack1ll1ll11_opy_(bstack1ll1l111l1_opy_)
  os.environ[bstack1l1ll1_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨ൘")] = bstack11ll1l111_opy_
  bstack11lll111l1_opy_ = bstack11ll1l111_opy_
  if cli.is_enabled(CONFIG):
    try:
      bstack1l11l1ll_opy_ = bstack1l111ll11_opy_[bstack1l1ll1_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔ࠮ࡄࡇࡈࠬ൙")] if bstack11ll1l111_opy_ == bstack1l1ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ൚") and bstack1ll11l111l_opy_() else bstack11ll1l111_opy_
      bstack1l1l111l_opy_.invoke(bstack1l11111l1l_opy_.bstack11l11ll1ll_opy_, bstack1lll1111ll_opy_(
        sdk_version=__version__,
        path_config=bstack11llll111_opy_(),
        path_project=os.getcwd(),
        test_framework=bstack1l11l1ll_opy_,
        frameworks=[bstack1l11l1ll_opy_],
        framework_versions={
          bstack1l11l1ll_opy_: bstack11l111l1_opy_(bstack1l1ll1_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩ൛") if bstack11ll1l111_opy_ in [bstack1l1ll1_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ൜"), bstack1l1ll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ൝"), bstack1l1ll1_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧ൞")] else bstack11ll1l111_opy_)
        },
        bs_config=CONFIG
      ))
      if cli.config.get(bstack1l1ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤൟ"), None):
        CONFIG[bstack1l1ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠥൠ")] = cli.config.get(bstack1l1ll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠦൡ"), None)
    except Exception as e:
      bstack1l1l111l_opy_.invoke(bstack1l11111l1l_opy_.bstack1l11l11l1l_opy_, e.__traceback__, 1)
    if bstack1l1lllllll_opy_:
      CONFIG[bstack1l1ll1_opy_ (u"ࠥࡥࡵࡶࠢൢ")] = cli.config[bstack1l1ll1_opy_ (u"ࠦࡦࡶࡰࠣൣ")]
      logger.info(bstack1l111lll_opy_.format(CONFIG[bstack1l1ll1_opy_ (u"ࠬࡧࡰࡱࠩ൤")]))
  else:
    bstack1l1l111l_opy_.clear()
  global bstack11lllll1_opy_
  global bstack1l11111111_opy_
  if bstack1l1111l1l1_opy_:
    try:
      bstack1l1l1lll1_opy_ = datetime.datetime.now()
      os.environ[bstack1l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ൥")] = bstack11ll1l111_opy_
      bstack1lll1l1ll1_opy_(bstack1ll1l1l11l_opy_, CONFIG)
      cli.bstack11l1l1111l_opy_(bstack1l1ll1_opy_ (u"ࠢࡩࡶࡷࡴ࠿ࡹࡤ࡬ࡡࡷࡩࡸࡺ࡟ࡢࡶࡷࡩࡲࡶࡴࡦࡦࠥ൦"), datetime.datetime.now() - bstack1l1l1lll1_opy_)
    except Exception as e:
      logger.debug(bstack1l1l11ll1l_opy_.format(str(e)))
  global bstack11llllll11_opy_
  global bstack111l11l1l_opy_
  global bstack1ll111111l_opy_
  global bstack1ll1ll1ll_opy_
  global bstack11lllll11_opy_
  global bstack1ll1llll1_opy_
  global bstack1lll11111_opy_
  global bstack11l111l1l1_opy_
  global bstack1l111lll1l_opy_
  global bstack11l1111l11_opy_
  global bstack11l1l11ll_opy_
  global bstack11ll11lll1_opy_
  global bstack1llll11ll1_opy_
  global bstack1l1l1l111_opy_
  global bstack1lll1ll11_opy_
  global bstack1lll1llll_opy_
  global bstack1lll1lll1l_opy_
  global bstack1l11l1lll_opy_
  global bstack1lll111111_opy_
  global bstack1l1lll1l11_opy_
  global bstack11l11l1ll1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11llllll11_opy_ = webdriver.Remote.__init__
    bstack111l11l1l_opy_ = WebDriver.quit
    bstack11ll11lll1_opy_ = WebDriver.close
    bstack1lll1ll11_opy_ = WebDriver.get
    bstack11l11l1ll1_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack11lllll1_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack1l111l11l_opy_
    bstack1l11111111_opy_ = bstack1l111l11l_opy_()
  except Exception as e:
    pass
  try:
    global bstack11l1111l1_opy_
    from QWeb.keywords import browser
    bstack11l1111l1_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1l1lll111l_opy_(CONFIG) and bstack11l1l1l1l_opy_():
    if bstack1111l1l1l_opy_() < version.parse(bstack1ll1ll1111_opy_):
      logger.error(bstack1l1l1111l_opy_.format(bstack1111l1l1l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack1l1ll1_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩ൧")) and callable(getattr(RemoteConnection, bstack1l1ll1_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪ൨"))):
          RemoteConnection._get_proxy_url = bstack1l111ll11l_opy_
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          ClientConfig.get_proxy_url = bstack1l111ll11l_opy_
      except Exception as e:
        logger.error(bstack11lll1l11_opy_.format(str(e)))
  if not CONFIG.get(bstack1l1ll1_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬ൩"), False) and not bstack1l1111l1l1_opy_:
    logger.info(bstack11l1l1l11l_opy_)
  if not cli.is_enabled(CONFIG):
    if bstack1l1ll1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ൪") in CONFIG and str(CONFIG[bstack1l1ll1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ൫")]).lower() != bstack1l1ll1_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ൬"):
      bstack1ll1lll111_opy_()
    elif bstack11ll1l111_opy_ != bstack1l1ll1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ൭") or (bstack11ll1l111_opy_ == bstack1l1ll1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ൮") and not bstack1l1111l1l1_opy_):
      bstack1ll111lll1_opy_()
  if (bstack11ll1l111_opy_ in [bstack1l1ll1_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ൯"), bstack1l1ll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ൰"), bstack1l1ll1_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ൱")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack11llllll_opy_
        bstack1ll1llll1_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1l1ll11l1_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack11lllll11_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1ll11ll111_opy_ + str(e))
    except Exception as e:
      bstack1l1l1llll1_opy_(e, bstack1l1ll11l1_opy_)
    if bstack11ll1l111_opy_ != bstack1l1ll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭൲"):
      bstack1l1l1l11l_opy_()
    bstack1ll111111l_opy_ = Output.start_test
    bstack1ll1ll1ll_opy_ = Output.end_test
    bstack1lll11111_opy_ = TestStatus.__init__
    bstack1l111lll1l_opy_ = pabot._run
    bstack11l1111l11_opy_ = QueueItem.__init__
    bstack11l1l11ll_opy_ = pabot._create_command_for_execution
    bstack1lll111111_opy_ = pabot._report_results
  if bstack11ll1l111_opy_ == bstack1l1ll1_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭൳"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l1l1llll1_opy_(e, bstack1l1l1ll11_opy_)
    bstack1llll11ll1_opy_ = Runner.run_hook
    bstack1l1l1l111_opy_ = Step.run
  if bstack11ll1l111_opy_ == bstack1l1ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ൴"):
    try:
      from _pytest.config import Config
      bstack1lll1lll1l_opy_ = Config.getoption
      from _pytest import runner
      bstack1l11l1lll_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack1l111l11ll_opy_)
    try:
      from pytest_bdd import reporting
      bstack1l1lll1l11_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1l1ll1_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡰࠢࡵࡹࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࡴࠩ൵"))
  try:
    framework_name = bstack1l1ll1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ൶") if bstack11ll1l111_opy_ in [bstack1l1ll1_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ൷"), bstack1l1ll1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ൸"), bstack1l1ll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭൹")] else bstack11l1111lll_opy_(bstack11ll1l111_opy_)
    bstack1lll11111l_opy_ = {
      bstack1l1ll1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࠧൺ"): bstack1l1ll1_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩൻ") if bstack11ll1l111_opy_ == bstack1l1ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨർ") and bstack1ll11l111l_opy_() else framework_name,
      bstack1l1ll1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ൽ"): bstack11l111l1_opy_(framework_name),
      bstack1l1ll1_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨൾ"): __version__,
      bstack1l1ll1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬൿ"): bstack11ll1l111_opy_
    }
    if bstack11ll1l111_opy_ in bstack11lll1ll1_opy_ + bstack11lllll111_opy_:
      if bstack1l11ll1lll_opy_.bstack111llllll_opy_(CONFIG):
        if bstack1l1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ඀") in CONFIG:
          os.environ[bstack1l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧඁ")] = os.getenv(bstack1l1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨං"), json.dumps(CONFIG[bstack1l1ll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨඃ")]))
          CONFIG[bstack1l1ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ඄")].pop(bstack1l1ll1_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨඅ"), None)
          CONFIG[bstack1l1ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫආ")].pop(bstack1l1ll1_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪඇ"), None)
        bstack1lll11111l_opy_[bstack1l1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ඈ")] = {
          bstack1l1ll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬඉ"): bstack1l1ll1_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࠪඊ"),
          bstack1l1ll1_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪඋ"): str(bstack1111l1l1l_opy_())
        }
    if bstack11ll1l111_opy_ not in [bstack1l1ll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫඌ")] and not cli.is_running():
      bstack1ll1ll1l1l_opy_, bstack111lll1l_opy_ = bstack1l1lll1l_opy_.launch(CONFIG, bstack1lll11111l_opy_)
      if bstack111lll1l_opy_.get(bstack1l1ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫඍ")) is not None and bstack1l11ll1lll_opy_.bstack1111l1lll_opy_(CONFIG) is None:
        value = bstack111lll1l_opy_[bstack1l1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬඎ")].get(bstack1l1ll1_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧඏ"))
        if value is not None:
            CONFIG[bstack1l1ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧඐ")] = value
        else:
          logger.debug(bstack1l1ll1_opy_ (u"ࠣࡐࡲࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡩࡧࡴࡢࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠨඑ"))
  except Exception as e:
    logger.debug(bstack11l11l1ll_opy_.format(bstack1l1ll1_opy_ (u"ࠩࡗࡩࡸࡺࡈࡶࡤࠪඒ"), str(e)))
  if bstack11ll1l111_opy_ == bstack1l1ll1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪඓ"):
    bstack11111ll1l_opy_ = True
    if bstack1l1111l1l1_opy_ and bstack11l1l11l11_opy_:
      bstack1111ll11l_opy_ = CONFIG.get(bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨඔ"), {}).get(bstack1l1ll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧඕ"))
      bstack111ll1l1l_opy_(bstack11ll111l11_opy_)
    elif bstack1l1111l1l1_opy_:
      bstack1111ll11l_opy_ = CONFIG.get(bstack1l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪඖ"), {}).get(bstack1l1ll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ඗"))
      global bstack1ll1l11lll_opy_
      try:
        if bstack11lll11ll_opy_(bstack1l1111l1l1_opy_[bstack1l1ll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ඘")]) and multiprocessing.current_process().name == bstack1l1ll1_opy_ (u"ࠩ࠳ࠫ඙"):
          bstack1l1111l1l1_opy_[bstack1l1ll1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ක")].remove(bstack1l1ll1_opy_ (u"ࠫ࠲ࡳࠧඛ"))
          bstack1l1111l1l1_opy_[bstack1l1ll1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨග")].remove(bstack1l1ll1_opy_ (u"࠭ࡰࡥࡤࠪඝ"))
          bstack1l1111l1l1_opy_[bstack1l1ll1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪඞ")] = bstack1l1111l1l1_opy_[bstack1l1ll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫඟ")][0]
          with open(bstack1l1111l1l1_opy_[bstack1l1ll1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬච")], bstack1l1ll1_opy_ (u"ࠪࡶࠬඡ")) as f:
            bstack1l1l1l1ll_opy_ = f.read()
          bstack11ll1l11_opy_ = bstack1l1ll1_opy_ (u"ࠦࠧࠨࡦࡳࡱࡰࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡷࡩࡱࠠࡪ࡯ࡳࡳࡷࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡧ࠾ࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿ࡫ࠨࡼࡿࠬ࠿ࠥ࡬ࡲࡰ࡯ࠣࡴࡩࡨࠠࡪ࡯ࡳࡳࡷࡺࠠࡑࡦࡥ࠿ࠥࡵࡧࡠࡦࡥࠤࡂࠦࡐࡥࡤ࠱ࡨࡴࡥࡢࡳࡧࡤ࡯ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡧࡩ࡫ࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠪࡶࡩࡱ࡬ࠬࠡࡣࡵ࡫࠱ࠦࡴࡦ࡯ࡳࡳࡷࡧࡲࡺࠢࡀࠤ࠵࠯࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡴࡳࡻ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡦࡸࡧࠡ࠿ࠣࡷࡹࡸࠨࡪࡰࡷࠬࡦࡸࡧࠪ࠭࠴࠴࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡪࡾࡣࡦࡲࡷࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡢࡵࠣࡩ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡰࡢࡵࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡲ࡫ࡤࡪࡢࠩࡵࡨࡰ࡫࠲ࡡࡳࡩ࠯ࡸࡪࡳࡰࡰࡴࡤࡶࡾ࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡔࡩࡨ࠮ࡥࡱࡢࡦࠥࡃࠠ࡮ࡱࡧࡣࡧࡸࡥࡢ࡭ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡐࡥࡤ࠱ࡨࡴࡥࡢࡳࡧࡤ࡯ࠥࡃࠠ࡮ࡱࡧࡣࡧࡸࡥࡢ࡭ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡐࡥࡤࠫ࠭࠳ࡹࡥࡵࡡࡷࡶࡦࡩࡥࠩࠫ࡟ࡲࠧࠨࠢජ").format(str(bstack1l1111l1l1_opy_))
          bstack1lll1ll1l_opy_ = bstack11ll1l11_opy_ + bstack1l1l1l1ll_opy_
          bstack1ll1l11l1_opy_ = bstack1l1111l1l1_opy_[bstack1l1ll1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨඣ")] + bstack1l1ll1_opy_ (u"࠭࡟ࡣࡵࡷࡥࡨࡱ࡟ࡵࡧࡰࡴ࠳ࡶࡹࠨඤ")
          with open(bstack1ll1l11l1_opy_, bstack1l1ll1_opy_ (u"ࠧࡸࠩඥ")):
            pass
          with open(bstack1ll1l11l1_opy_, bstack1l1ll1_opy_ (u"ࠣࡹ࠮ࠦඦ")) as f:
            f.write(bstack1lll1ll1l_opy_)
          import subprocess
          bstack1l11111lll_opy_ = subprocess.run([bstack1l1ll1_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࠤට"), bstack1ll1l11l1_opy_])
          if os.path.exists(bstack1ll1l11l1_opy_):
            os.unlink(bstack1ll1l11l1_opy_)
          os._exit(bstack1l11111lll_opy_.returncode)
        else:
          if bstack11lll11ll_opy_(bstack1l1111l1l1_opy_[bstack1l1ll1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ඨ")]):
            bstack1l1111l1l1_opy_[bstack1l1ll1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧඩ")].remove(bstack1l1ll1_opy_ (u"ࠬ࠳࡭ࠨඪ"))
            bstack1l1111l1l1_opy_[bstack1l1ll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩණ")].remove(bstack1l1ll1_opy_ (u"ࠧࡱࡦࡥࠫඬ"))
            bstack1l1111l1l1_opy_[bstack1l1ll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫත")] = bstack1l1111l1l1_opy_[bstack1l1ll1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬථ")][0]
          bstack111ll1l1l_opy_(bstack11ll111l11_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1l1111l1l1_opy_[bstack1l1ll1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ද")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1l1ll1_opy_ (u"ࠫࡤࡥ࡮ࡢ࡯ࡨࡣࡤ࠭ධ")] = bstack1l1ll1_opy_ (u"ࠬࡥ࡟࡮ࡣ࡬ࡲࡤࡥࠧන")
          mod_globals[bstack1l1ll1_opy_ (u"࠭࡟ࡠࡨ࡬ࡰࡪࡥ࡟ࠨ඲")] = os.path.abspath(bstack1l1111l1l1_opy_[bstack1l1ll1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪඳ")])
          exec(open(bstack1l1111l1l1_opy_[bstack1l1ll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫප")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1l1ll1_opy_ (u"ࠩࡆࡥࡺ࡭ࡨࡵࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠩඵ").format(str(e)))
          for driver in bstack1ll1l11lll_opy_:
            bstack1lll1ll111_opy_.append({
              bstack1l1ll1_opy_ (u"ࠪࡲࡦࡳࡥࠨබ"): bstack1l1111l1l1_opy_[bstack1l1ll1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧභ")],
              bstack1l1ll1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫම"): str(e),
              bstack1l1ll1_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬඹ"): multiprocessing.current_process().name
            })
            bstack1l1ll1lll1_opy_(driver, bstack1l1ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧය"), bstack1l1ll1_opy_ (u"ࠣࡕࡨࡷࡸ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦර") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1ll1l11lll_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1l1lllllll_opy_, CONFIG, logger)
      bstack1l111lll1_opy_()
      bstack111ll111_opy_()
      percy.bstack11l1llllll_opy_()
      bstack1ll11l1l_opy_ = {
        bstack1l1ll1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ඼"): args[0],
        bstack1l1ll1_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪල"): CONFIG,
        bstack1l1ll1_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬ඾"): bstack1l1ll1l11l_opy_,
        bstack1l1ll1_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ඿"): bstack1l1lllllll_opy_
      }
      if bstack1l1ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩව") in CONFIG:
        bstack1l111111ll_opy_ = bstack1l1lll1ll_opy_(args, logger, CONFIG, bstack11l11l111_opy_, bstack1l111l11_opy_)
        bstack1l1llll1l_opy_ = bstack1l111111ll_opy_.bstack1llll1lll1_opy_(run_on_browserstack, bstack1ll11l1l_opy_, bstack11lll11ll_opy_(args))
      else:
        if bstack11lll11ll_opy_(args):
          bstack1ll11l1l_opy_[bstack1l1ll1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪශ")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1ll11l1l_opy_,))
          test.start()
          test.join()
        else:
          bstack111ll1l1l_opy_(bstack11ll111l11_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1l1ll1_opy_ (u"ࠨࡡࡢࡲࡦࡳࡥࡠࡡࠪෂ")] = bstack1l1ll1_opy_ (u"ࠩࡢࡣࡲࡧࡩ࡯ࡡࡢࠫස")
          mod_globals[bstack1l1ll1_opy_ (u"ࠪࡣࡤ࡬ࡩ࡭ࡧࡢࡣࠬහ")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack11ll1l111_opy_ == bstack1l1ll1_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪළ") or bstack11ll1l111_opy_ == bstack1l1ll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫෆ"):
    percy.init(bstack1l1lllllll_opy_, CONFIG, logger)
    percy.bstack11l1llllll_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1l1l1llll1_opy_(e, bstack1l1ll11l1_opy_)
    bstack1l111lll1_opy_()
    bstack111ll1l1l_opy_(bstack11l1lll11l_opy_)
    if bstack11l11l111_opy_:
      bstack1l1l1llll_opy_(bstack11l1lll11l_opy_, args)
      if bstack1l1ll1_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ෇") in args:
        i = args.index(bstack1l1ll1_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ෈"))
        args.pop(i)
        args.pop(i)
      if bstack1l1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ෉") not in CONFIG:
        CONFIG[bstack1l1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷ්ࠬ")] = [{}]
        bstack1l111l11_opy_ = 1
      if bstack1l1l11l11l_opy_ == 0:
        bstack1l1l11l11l_opy_ = 1
      args.insert(0, str(bstack1l1l11l11l_opy_))
      args.insert(0, str(bstack1l1ll1_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨ෋")))
    if bstack1l1lll1l_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack11l111ll1_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack11l1llll1_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack1l1ll1_opy_ (u"ࠦࡗࡕࡂࡐࡖࡢࡓࡕ࡚ࡉࡐࡐࡖࠦ෌"),
        ).parse_args(bstack11l111ll1_opy_)
        bstack1lll1lll_opy_ = args.index(bstack11l111ll1_opy_[0]) if len(bstack11l111ll1_opy_) > 0 else len(args)
        args.insert(bstack1lll1lll_opy_, str(bstack1l1ll1_opy_ (u"ࠬ࠳࠭࡭࡫ࡶࡸࡪࡴࡥࡳࠩ෍")))
        args.insert(bstack1lll1lll_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l1ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡲࡰࡤࡲࡸࡤࡲࡩࡴࡶࡨࡲࡪࡸ࠮ࡱࡻࠪ෎"))))
        if bstack11l1ll1l1_opy_.bstack1ll1ll1ll1_opy_(CONFIG):
          args.insert(bstack1lll1lll_opy_, str(bstack1l1ll1_opy_ (u"ࠧ࠮࠯࡯࡭ࡸࡺࡥ࡯ࡧࡵࠫා")))
          args.insert(bstack1lll1lll_opy_ + 1, str(bstack1l1ll1_opy_ (u"ࠨࡔࡨࡸࡷࡿࡆࡢ࡫࡯ࡩࡩࡀࡻࡾࠩැ").format(bstack11l1ll1l1_opy_.bstack1l1111l111_opy_(CONFIG))))
        if bstack11lll1lll1_opy_(os.environ.get(bstack1l1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠧෑ"))) and str(os.environ.get(bstack1l1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠧි"), bstack1l1ll1_opy_ (u"ࠫࡳࡻ࡬࡭ࠩී"))) != bstack1l1ll1_opy_ (u"ࠬࡴࡵ࡭࡮ࠪු"):
          for bstack1l1111lll1_opy_ in bstack11l1llll1_opy_:
            args.remove(bstack1l1111lll1_opy_)
          test_files = os.environ.get(bstack1l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࡣ࡙ࡋࡓࡕࡕࠪ෕")).split(bstack1l1ll1_opy_ (u"ࠧ࠭ࠩූ"))
          for bstack1l11l1111_opy_ in test_files:
            args.append(bstack1l11l1111_opy_)
      except Exception as e:
        logger.error(bstack1l1ll1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡡࡵࡶࡤࡧ࡭࡯࡮ࡨࠢ࡯࡭ࡸࡺࡥ࡯ࡧࡵࠤ࡫ࡵࡲࠡࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࠢࡈࡶࡷࡵࡲࠡ࠯ࠣࠦ෗").format(e))
    pabot.main(args)
  elif bstack11ll1l111_opy_ == bstack1l1ll1_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪෘ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1l1l1llll1_opy_(e, bstack1l1ll11l1_opy_)
    for a in args:
      if bstack1l1ll1_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡓࡐࡆ࡚ࡆࡐࡔࡐࡍࡓࡊࡅ࡙ࠩෙ") in a:
        bstack111l1111_opy_ = int(a.split(bstack1l1ll1_opy_ (u"ࠫ࠿࠭ේ"))[1])
      if bstack1l1ll1_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡉࡋࡆࡍࡑࡆࡅࡑࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩෛ") in a:
        bstack1111ll11l_opy_ = str(a.split(bstack1l1ll1_opy_ (u"࠭࠺ࠨො"))[1])
      if bstack1l1ll1_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙ࠧෝ") in a:
        bstack1ll1ll1l1_opy_ = str(a.split(bstack1l1ll1_opy_ (u"ࠨ࠼ࠪෞ"))[1])
    bstack11l1l111ll_opy_ = None
    if bstack1l1ll1_opy_ (u"ࠩ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠨෟ") in args:
      i = args.index(bstack1l1ll1_opy_ (u"ࠪ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠩ෠"))
      args.pop(i)
      bstack11l1l111ll_opy_ = args.pop(i)
    if bstack11l1l111ll_opy_ is not None:
      global bstack11ll111ll1_opy_
      bstack11ll111ll1_opy_ = bstack11l1l111ll_opy_
    bstack111ll1l1l_opy_(bstack11l1lll11l_opy_)
    run_cli(args)
    if bstack1l1ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴࠨ෡") in multiprocessing.current_process().__dict__.keys():
      for bstack1ll111lll_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1lll1ll111_opy_.append(bstack1ll111lll_opy_)
  elif bstack11ll1l111_opy_ == bstack1l1ll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ෢"):
    bstack1ll1l1l1l1_opy_ = bstack1llll111_opy_(args, logger, CONFIG, bstack11l11l111_opy_)
    bstack1ll1l1l1l1_opy_.bstack1111l1ll_opy_()
    bstack1l111lll1_opy_()
    bstack111lllll1_opy_ = True
    bstack11l1ll1ll1_opy_ = bstack1ll1l1l1l1_opy_.bstack1l1llll11_opy_()
    bstack1ll1l1l1l1_opy_.bstack1llllll11l_opy_()
    bstack1ll1l1l1l1_opy_.bstack1ll11l1l_opy_(bstack1l111llll1_opy_)
    bstack1l11ll1111_opy_(bstack11ll1l111_opy_, CONFIG, bstack1ll1l1l1l1_opy_.bstack1111lll11_opy_())
    bstack11l1l1l1_opy_ = bstack1ll1l1l1l1_opy_.bstack1llll1lll1_opy_(bstack11ll1l1l1_opy_, {
      bstack1l1ll1_opy_ (u"࠭ࡈࡖࡄࡢ࡙ࡗࡒࠧ෣"): bstack1l1ll1l11l_opy_,
      bstack1l1ll1_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ෤"): bstack1l1lllllll_opy_,
      bstack1l1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫ෥"): bstack11l11l111_opy_
    })
    try:
      bstack1l1111l1ll_opy_, bstack1l1lll1l1_opy_ = map(list, zip(*bstack11l1l1l1_opy_))
      bstack1l1111ll_opy_ = bstack1l1111l1ll_opy_[0]
      for status_code in bstack1l1lll1l1_opy_:
        if status_code != 0:
          bstack11ll1l11ll_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack1l1ll1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡡࡷࡧࠣࡩࡷࡸ࡯ࡳࡵࠣࡥࡳࡪࠠࡴࡶࡤࡸࡺࡹࠠࡤࡱࡧࡩ࠳ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࠽ࠤࢀࢃࠢ෦").format(str(e)))
  elif bstack11ll1l111_opy_ == bstack1l1ll1_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ෧"):
    try:
      from behave.__main__ import main as bstack1llll111l_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1l1l1llll1_opy_(e, bstack1l1l1ll11_opy_)
    bstack1l111lll1_opy_()
    bstack111lllll1_opy_ = True
    bstack111l11l1_opy_ = 1
    if bstack1l1ll1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ෨") in CONFIG:
      bstack111l11l1_opy_ = CONFIG[bstack1l1ll1_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ෩")]
    if bstack1l1ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ෪") in CONFIG:
      bstack1l1lll11_opy_ = int(bstack111l11l1_opy_) * int(len(CONFIG[bstack1l1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ෫")]))
    else:
      bstack1l1lll11_opy_ = int(bstack111l11l1_opy_)
    config = Configuration(args)
    bstack1l11ll11_opy_ = config.paths
    if len(bstack1l11ll11_opy_) == 0:
      import glob
      pattern = bstack1l1ll1_opy_ (u"ࠨࠬ࠭࠳࠯࠴ࡦࡦࡣࡷࡹࡷ࡫ࠧ෬")
      bstack1l1ll11111_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1l1ll11111_opy_)
      config = Configuration(args)
      bstack1l11ll11_opy_ = config.paths
    bstack1l1111lll_opy_ = [os.path.normpath(item) for item in bstack1l11ll11_opy_]
    bstack1ll11l1l1l_opy_ = [os.path.normpath(item) for item in args]
    bstack1lllll1l1_opy_ = [item for item in bstack1ll11l1l1l_opy_ if item not in bstack1l1111lll_opy_]
    import platform as pf
    if pf.system().lower() == bstack1l1ll1_opy_ (u"ࠩࡺ࡭ࡳࡪ࡯ࡸࡵࠪ෭"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1l1111lll_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1111l111_opy_)))
                    for bstack1111l111_opy_ in bstack1l1111lll_opy_]
    bstack11ll1llll_opy_ = []
    for spec in bstack1l1111lll_opy_:
      bstack1llll11lll_opy_ = []
      bstack1llll11lll_opy_ += bstack1lllll1l1_opy_
      bstack1llll11lll_opy_.append(spec)
      bstack11ll1llll_opy_.append(bstack1llll11lll_opy_)
    execution_items = []
    for bstack1llll11lll_opy_ in bstack11ll1llll_opy_:
      if bstack1l1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭෮") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack1l1ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ෯")]):
          item = {}
          item[bstack1l1ll1_opy_ (u"ࠬࡧࡲࡨࠩ෰")] = bstack1l1ll1_opy_ (u"࠭ࠠࠨ෱").join(bstack1llll11lll_opy_)
          item[bstack1l1ll1_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ෲ")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack1l1ll1_opy_ (u"ࠨࡣࡵ࡫ࠬෳ")] = bstack1l1ll1_opy_ (u"ࠩࠣࠫ෴").join(bstack1llll11lll_opy_)
        item[bstack1l1ll1_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ෵")] = 0
        execution_items.append(item)
    bstack1ll11111ll_opy_ = bstack1l1l1l1l_opy_(execution_items, bstack1l1lll11_opy_)
    for execution_item in bstack1ll11111ll_opy_:
      bstack1l1l1l111l_opy_ = []
      for item in execution_item:
        bstack1l1l1l111l_opy_.append(bstack1lll11l1_opy_(name=str(item[bstack1l1ll1_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ෶")]),
                                             target=bstack1l11llll_opy_,
                                             args=(item[bstack1l1ll1_opy_ (u"ࠬࡧࡲࡨࠩ෷")],)))
      for t in bstack1l1l1l111l_opy_:
        t.start()
      for t in bstack1l1l1l111l_opy_:
        t.join()
  else:
    bstack1ll1ll11_opy_(bstack1ll1l111l1_opy_)
  if not bstack1l1111l1l1_opy_:
    bstack111ll11l_opy_()
    if(bstack11ll1l111_opy_ in [bstack1l1ll1_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭෸"), bstack1l1ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ෹")]):
      bstack1llll1l111_opy_()
  bstack11lll1ll_opy_.bstack1111l1l1_opy_()
def browserstack_initialize(bstack11l1111l1l_opy_=None):
  logger.info(bstack1l1ll1_opy_ (u"ࠨࡔࡸࡲࡳ࡯࡮ࡨࠢࡖࡈࡐࠦࡷࡪࡶ࡫ࠤࡦࡸࡧࡴ࠼ࠣࠫ෺") + str(bstack11l1111l1l_opy_))
  run_on_browserstack(bstack11l1111l1l_opy_, None, True)
@measure(event_name=EVENTS.bstack1l11llll1l_opy_, stage=STAGE.bstack1l1ll11ll1_opy_, bstack1llll1ll1l_opy_=bstack11111ll1_opy_)
def bstack111ll11l_opy_():
  global CONFIG
  global bstack11lll111l1_opy_
  global bstack11ll1l11ll_opy_
  global bstack1l1lll1111_opy_
  global bstack11lll111ll_opy_
  bstack1l1ll11l11_opy_.bstack1l1ll111_opy_()
  if cli.is_running():
    bstack1l1l111l_opy_.invoke(bstack1l11111l1l_opy_.bstack11l1111ll1_opy_)
  if bstack11lll111l1_opy_ == bstack1l1ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ෻"):
    if not cli.is_enabled(CONFIG):
      bstack1l1lll1l_opy_.stop()
  else:
    bstack1l1lll1l_opy_.stop()
  if not cli.is_enabled(CONFIG):
    bstack111l1ll1l_opy_.bstack1l11ll1ll1_opy_()
  if bstack1l1ll1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ෼") in CONFIG and str(CONFIG[bstack1l1ll1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ෽")]).lower() != bstack1l1ll1_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ෾"):
    hashed_id, bstack1l1ll11l1l_opy_ = bstack11111lll_opy_()
  else:
    hashed_id, bstack1l1ll11l1l_opy_ = get_build_link()
  bstack1lll1l11ll_opy_(hashed_id)
  logger.info(bstack1l1ll1_opy_ (u"࠭ࡓࡅࡍࠣࡶࡺࡴࠠࡦࡰࡧࡩࡩࠦࡦࡰࡴࠣ࡭ࡩࡀࠧ෿") + bstack11lll111ll_opy_.get_property(bstack1l1ll1_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥࠩ฀"), bstack1l1ll1_opy_ (u"ࠨࠩก")) + bstack1l1ll1_opy_ (u"ࠩ࠯ࠤࡹ࡫ࡳࡵࡪࡸࡦࠥ࡯ࡤ࠻ࠢࠪข") + os.getenv(bstack1l1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨฃ"), bstack1l1ll1_opy_ (u"ࠫࠬค")))
  if hashed_id is not None and bstack1ll11l11l_opy_() != -1:
    sessions = bstack1ll1l11ll_opy_(hashed_id)
    bstack1l11111l1_opy_(sessions, bstack1l1ll11l1l_opy_)
  if bstack11lll111l1_opy_ == bstack1l1ll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬฅ") and bstack11ll1l11ll_opy_ != 0:
    sys.exit(bstack11ll1l11ll_opy_)
  if bstack11lll111l1_opy_ == bstack1l1ll1_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ฆ") and bstack1l1lll1111_opy_ != 0:
    sys.exit(bstack1l1lll1111_opy_)
def bstack1lll1l11ll_opy_(new_id):
    global bstack11l1ll1l1l_opy_
    bstack11l1ll1l1l_opy_ = new_id
def bstack11l1111lll_opy_(bstack1llll1l1ll_opy_):
  if bstack1llll1l1ll_opy_:
    return bstack1llll1l1ll_opy_.capitalize()
  else:
    return bstack1l1ll1_opy_ (u"ࠧࠨง")
@measure(event_name=EVENTS.bstack1ll11ll1l1_opy_, stage=STAGE.bstack1l1ll11ll1_opy_, bstack1llll1ll1l_opy_=bstack11111ll1_opy_)
def bstack1l1llll1l1_opy_(bstack111111ll_opy_):
  if bstack1l1ll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭จ") in bstack111111ll_opy_ and bstack111111ll_opy_[bstack1l1ll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧฉ")] != bstack1l1ll1_opy_ (u"ࠪࠫช"):
    return bstack111111ll_opy_[bstack1l1ll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩซ")]
  else:
    bstack1llll1ll1l_opy_ = bstack1l1ll1_opy_ (u"ࠧࠨฌ")
    if bstack1l1ll1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ญ") in bstack111111ll_opy_ and bstack111111ll_opy_[bstack1l1ll1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧฎ")] != None:
      bstack1llll1ll1l_opy_ += bstack111111ll_opy_[bstack1l1ll1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨฏ")] + bstack1l1ll1_opy_ (u"ࠤ࠯ࠤࠧฐ")
      if bstack111111ll_opy_[bstack1l1ll1_opy_ (u"ࠪࡳࡸ࠭ฑ")] == bstack1l1ll1_opy_ (u"ࠦ࡮ࡵࡳࠣฒ"):
        bstack1llll1ll1l_opy_ += bstack1l1ll1_opy_ (u"ࠧ࡯ࡏࡔࠢࠥณ")
      bstack1llll1ll1l_opy_ += (bstack111111ll_opy_[bstack1l1ll1_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪด")] or bstack1l1ll1_opy_ (u"ࠧࠨต"))
      return bstack1llll1ll1l_opy_
    else:
      bstack1llll1ll1l_opy_ += bstack11l1111lll_opy_(bstack111111ll_opy_[bstack1l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩถ")]) + bstack1l1ll1_opy_ (u"ࠤࠣࠦท") + (
              bstack111111ll_opy_[bstack1l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬธ")] or bstack1l1ll1_opy_ (u"ࠫࠬน")) + bstack1l1ll1_opy_ (u"ࠧ࠲ࠠࠣบ")
      if bstack111111ll_opy_[bstack1l1ll1_opy_ (u"࠭࡯ࡴࠩป")] == bstack1l1ll1_opy_ (u"ࠢࡘ࡫ࡱࡨࡴࡽࡳࠣผ"):
        bstack1llll1ll1l_opy_ += bstack1l1ll1_opy_ (u"࡙ࠣ࡬ࡲࠥࠨฝ")
      bstack1llll1ll1l_opy_ += bstack111111ll_opy_[bstack1l1ll1_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭พ")] or bstack1l1ll1_opy_ (u"ࠪࠫฟ")
      return bstack1llll1ll1l_opy_
@measure(event_name=EVENTS.bstack1ll1llllll_opy_, stage=STAGE.bstack1l1ll11ll1_opy_, bstack1llll1ll1l_opy_=bstack11111ll1_opy_)
def bstack11l1l1ll1_opy_(bstack11l11llll_opy_):
  if bstack11l11llll_opy_ == bstack1l1ll1_opy_ (u"ࠦࡩࡵ࡮ࡦࠤภ"):
    return bstack1l1ll1_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡨࡴࡨࡩࡳࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡨࡴࡨࡩࡳࠨ࠾ࡄࡱࡰࡴࡱ࡫ࡴࡦࡦ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨม")
  elif bstack11l11llll_opy_ == bstack1l1ll1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨย"):
    return bstack1l1ll1_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡵࡩࡩࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡳࡧࡧࠦࡃࡌࡡࡪ࡮ࡨࡨࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪร")
  elif bstack11l11llll_opy_ == bstack1l1ll1_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣฤ"):
    return bstack1l1ll1_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾࡬ࡸࡥࡦࡰ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦ࡬ࡸࡥࡦࡰࠥࡂࡕࡧࡳࡴࡧࡧࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩล")
  elif bstack11l11llll_opy_ == bstack1l1ll1_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤฦ"):
    return bstack1l1ll1_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡲࡦࡦ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡷ࡫ࡤࠣࡀࡈࡶࡷࡵࡲ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ว")
  elif bstack11l11llll_opy_ == bstack1l1ll1_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࠨศ"):
    return bstack1l1ll1_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࠥࡨࡩࡦ࠹࠲࠷࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࠧࡪ࡫ࡡ࠴࠴࠹ࠦࡃ࡚ࡩ࡮ࡧࡲࡹࡹࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫษ")
  elif bstack11l11llll_opy_ == bstack1l1ll1_opy_ (u"ࠢࡳࡷࡱࡲ࡮ࡴࡧࠣส"):
    return bstack1l1ll1_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡦࡱࡧࡣ࡬࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡦࡱࡧࡣ࡬ࠤࡁࡖࡺࡴ࡮ࡪࡰࡪࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩห")
  else:
    return bstack1l1ll1_opy_ (u"ࠩ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡨ࡬ࡢࡥ࡮࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡨ࡬ࡢࡥ࡮ࠦࡃ࠭ฬ") + bstack11l1111lll_opy_(
      bstack11l11llll_opy_) + bstack1l1ll1_opy_ (u"ࠪࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩอ")
def bstack11llll11_opy_(session):
  return bstack1l1ll1_opy_ (u"ࠫࡁࡺࡲࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡴࡲࡻࠧࡄ࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠡࡵࡨࡷࡸ࡯࡯࡯࠯ࡱࡥࡲ࡫ࠢ࠿࠾ࡤࠤ࡭ࡸࡥࡧ࠿ࠥࡿࢂࠨࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣࡡࡥࡰࡦࡴ࡫ࠣࡀࡾࢁࡁ࠵ࡡ࠿࠾࠲ࡸࡩࡄࡻࡾࡽࢀࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂ࠯ࡵࡴࡁࠫฮ").format(
    session[bstack1l1ll1_opy_ (u"ࠬࡶࡵࡣ࡮࡬ࡧࡤࡻࡲ࡭ࠩฯ")], bstack1l1llll1l1_opy_(session), bstack11l1l1ll1_opy_(session[bstack1l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡹࡴࡢࡶࡸࡷࠬะ")]),
    bstack11l1l1ll1_opy_(session[bstack1l1ll1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧั")]),
    bstack11l1111lll_opy_(session[bstack1l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩา")] or session[bstack1l1ll1_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩำ")] or bstack1l1ll1_opy_ (u"ࠪࠫิ")) + bstack1l1ll1_opy_ (u"ࠦࠥࠨี") + (session[bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧึ")] or bstack1l1ll1_opy_ (u"࠭ࠧื")),
    session[bstack1l1ll1_opy_ (u"ࠧࡰࡵุࠪ")] + bstack1l1ll1_opy_ (u"ูࠣࠢࠥ") + session[bstack1l1ll1_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳฺ࠭")], session[bstack1l1ll1_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬ฻")] or bstack1l1ll1_opy_ (u"ࠫࠬ฼"),
    session[bstack1l1ll1_opy_ (u"ࠬࡩࡲࡦࡣࡷࡩࡩࡥࡡࡵࠩ฽")] if session[bstack1l1ll1_opy_ (u"࠭ࡣࡳࡧࡤࡸࡪࡪ࡟ࡢࡶࠪ฾")] else bstack1l1ll1_opy_ (u"ࠧࠨ฿"))
@measure(event_name=EVENTS.bstack11l1ll111_opy_, stage=STAGE.bstack1l1ll11ll1_opy_, bstack1llll1ll1l_opy_=bstack11111ll1_opy_)
def bstack1l11111l1_opy_(sessions, bstack1l1ll11l1l_opy_):
  try:
    bstack11lllll11l_opy_ = bstack1l1ll1_opy_ (u"ࠣࠤเ")
    if not os.path.exists(bstack1l1llllll1_opy_):
      os.mkdir(bstack1l1llllll1_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l1ll1_opy_ (u"ࠩࡤࡷࡸ࡫ࡴࡴ࠱ࡵࡩࡵࡵࡲࡵ࠰࡫ࡸࡲࡲࠧแ")), bstack1l1ll1_opy_ (u"ࠪࡶࠬโ")) as f:
      bstack11lllll11l_opy_ = f.read()
    bstack11lllll11l_opy_ = bstack11lllll11l_opy_.replace(bstack1l1ll1_opy_ (u"ࠫࢀࠫࡒࡆࡕࡘࡐ࡙࡙࡟ࡄࡑࡘࡒ࡙ࠫࡽࠨใ"), str(len(sessions)))
    bstack11lllll11l_opy_ = bstack11lllll11l_opy_.replace(bstack1l1ll1_opy_ (u"ࠬࢁࠥࡃࡗࡌࡐࡉࡥࡕࡓࡎࠨࢁࠬไ"), bstack1l1ll11l1l_opy_)
    bstack11lllll11l_opy_ = bstack11lllll11l_opy_.replace(bstack1l1ll1_opy_ (u"࠭ࡻࠦࡄࡘࡍࡑࡊ࡟ࡏࡃࡐࡉࠪࢃࠧๅ"),
                                              sessions[0].get(bstack1l1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥ࡮ࡢ࡯ࡨࠫๆ")) if sessions[0] else bstack1l1ll1_opy_ (u"ࠨࠩ็"))
    with open(os.path.join(bstack1l1llllll1_opy_, bstack1l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠮ࡴࡨࡴࡴࡸࡴ࠯ࡪࡷࡱࡱ่࠭")), bstack1l1ll1_opy_ (u"ࠪࡻ้ࠬ")) as stream:
      stream.write(bstack11lllll11l_opy_.split(bstack1l1ll1_opy_ (u"ࠫࢀࠫࡓࡆࡕࡖࡍࡔࡔࡓࡠࡆࡄࡘࡆࠫࡽࠨ๊"))[0])
      for session in sessions:
        stream.write(bstack11llll11_opy_(session))
      stream.write(bstack11lllll11l_opy_.split(bstack1l1ll1_opy_ (u"ࠬࢁࠥࡔࡇࡖࡗࡎࡕࡎࡔࡡࡇࡅ࡙ࡇࠥࡾ๋ࠩ"))[1])
    logger.info(bstack1l1ll1_opy_ (u"࠭ࡇࡦࡰࡨࡶࡦࡺࡥࡥࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡤࡸ࡭ࡱࡪࠠࡢࡴࡷ࡭࡫ࡧࡣࡵࡵࠣࡥࡹࠦࡻࡾࠩ์").format(bstack1l1llllll1_opy_));
  except Exception as e:
    logger.debug(bstack1l111l1l1l_opy_.format(str(e)))
def bstack1ll1l11ll_opy_(hashed_id):
  global CONFIG
  try:
    bstack1l1l1lll1_opy_ = datetime.datetime.now()
    host = bstack1l1ll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠲ࡩ࡬ࡰࡷࡧ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧํ") if bstack1l1ll1_opy_ (u"ࠨࡣࡳࡴࠬ๎") in CONFIG else bstack1l1ll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡵ࡯࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ๏")
    user = CONFIG[bstack1l1ll1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ๐")]
    key = CONFIG[bstack1l1ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ๑")]
    bstack1111l1111_opy_ = bstack1l1ll1_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ๒") if bstack1l1ll1_opy_ (u"࠭ࡡࡱࡲࠪ๓") in CONFIG else (bstack1l1ll1_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫ๔") if CONFIG.get(bstack1l1ll1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬ๕")) else bstack1l1ll1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ๖"))
    host = bstack111lll1l1_opy_(cli.config, [bstack1l1ll1_opy_ (u"ࠥࡥࡵ࡯ࡳࠣ๗"), bstack1l1ll1_opy_ (u"ࠦࡦࡶࡰࡂࡷࡷࡳࡲࡧࡴࡦࠤ๘"), bstack1l1ll1_opy_ (u"ࠧࡧࡰࡪࠤ๙")], host) if bstack1l1ll1_opy_ (u"࠭ࡡࡱࡲࠪ๚") in CONFIG else bstack111lll1l1_opy_(cli.config, [bstack1l1ll1_opy_ (u"ࠢࡢࡲ࡬ࡷࠧ๛"), bstack1l1ll1_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧࠥ๜"), bstack1l1ll1_opy_ (u"ࠤࡤࡴ࡮ࠨ๝")], host)
    url = bstack1l1ll1_opy_ (u"ࠪࡿࢂ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡹࡥࡴࡵ࡬ࡳࡳࡹ࠮࡫ࡵࡲࡲࠬ๞").format(host, bstack1111l1111_opy_, hashed_id)
    headers = {
      bstack1l1ll1_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪ๟"): bstack1l1ll1_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ๠"),
    }
    proxies = bstack11l111ll_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies, auth=(user, key))
    if response.json():
      cli.bstack11l1l1111l_opy_(bstack1l1ll1_opy_ (u"ࠨࡨࡵࡶࡳ࠾࡬࡫ࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࡢࡰ࡮ࡹࡴࠣ๡"), datetime.datetime.now() - bstack1l1l1lll1_opy_)
      return list(map(lambda session: session[bstack1l1ll1_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬ๢")], response.json()))
  except Exception as e:
    logger.debug(bstack1111lll1_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack11ll111l_opy_, stage=STAGE.bstack1l1ll11ll1_opy_, bstack1llll1ll1l_opy_=bstack11111ll1_opy_)
def get_build_link():
  global CONFIG
  global bstack11l1ll1l1l_opy_
  try:
    if bstack1l1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ๣") in CONFIG:
      bstack1l1l1lll1_opy_ = datetime.datetime.now()
      host = bstack1l1ll1_opy_ (u"ࠩࡤࡴ࡮࠳ࡣ࡭ࡱࡸࡨࠬ๤") if bstack1l1ll1_opy_ (u"ࠪࡥࡵࡶࠧ๥") in CONFIG else bstack1l1ll1_opy_ (u"ࠫࡦࡶࡩࠨ๦")
      user = CONFIG[bstack1l1ll1_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ๧")]
      key = CONFIG[bstack1l1ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ๨")]
      bstack1111l1111_opy_ = bstack1l1ll1_opy_ (u"ࠧࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭๩") if bstack1l1ll1_opy_ (u"ࠨࡣࡳࡴࠬ๪") in CONFIG else bstack1l1ll1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ๫")
      url = bstack1l1ll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࢀࢃ࠺ࡼࡿࡃࡿࢂ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡾࢁ࠴ࡨࡵࡪ࡮ࡧࡷ࠳ࡰࡳࡰࡰࠪ๬").format(user, key, host, bstack1111l1111_opy_)
      if cli.is_enabled(CONFIG):
        bstack1l1ll11l1l_opy_, hashed_id = cli.bstack1ll11l11_opy_()
        logger.info(bstack11l1l11lll_opy_.format(bstack1l1ll11l1l_opy_))
        return [hashed_id, bstack1l1ll11l1l_opy_]
      else:
        headers = {
          bstack1l1ll1_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪ๭"): bstack1l1ll1_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ๮"),
        }
        if bstack1l1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ๯") in CONFIG:
          params = {bstack1l1ll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ๰"): CONFIG[bstack1l1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ๱")], bstack1l1ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ๲"): CONFIG[bstack1l1ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ๳")]}
        else:
          params = {bstack1l1ll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ๴"): CONFIG[bstack1l1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ๵")]}
        proxies = bstack11l111ll_opy_(CONFIG, url)
        response = requests.get(url, params=params, headers=headers, proxies=proxies)
        if response.json():
          bstack1l1ll111l_opy_ = response.json()[0][bstack1l1ll1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡦࡺ࡯࡬ࡥࠩ๶")]
          if bstack1l1ll111l_opy_:
            bstack1l1ll11l1l_opy_ = bstack1l1ll111l_opy_[bstack1l1ll1_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࡟ࡶࡴ࡯ࠫ๷")].split(bstack1l1ll1_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣ࠮ࡤࡸ࡭ࡱࡪࠧ๸"))[0] + bstack1l1ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡴ࠱ࠪ๹") + bstack1l1ll111l_opy_[
              bstack1l1ll1_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭๺")]
            logger.info(bstack11l1l11lll_opy_.format(bstack1l1ll11l1l_opy_))
            bstack11l1ll1l1l_opy_ = bstack1l1ll111l_opy_[bstack1l1ll1_opy_ (u"ࠫ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ๻")]
            bstack11ll11l1l1_opy_ = CONFIG[bstack1l1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ๼")]
            if bstack1l1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ๽") in CONFIG:
              bstack11ll11l1l1_opy_ += bstack1l1ll1_opy_ (u"ࠧࠡࠩ๾") + CONFIG[bstack1l1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ๿")]
            if bstack11ll11l1l1_opy_ != bstack1l1ll111l_opy_[bstack1l1ll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ຀")]:
              logger.debug(bstack11ll11l11_opy_.format(bstack1l1ll111l_opy_[bstack1l1ll1_opy_ (u"ࠪࡲࡦࡳࡥࠨກ")], bstack11ll11l1l1_opy_))
            cli.bstack11l1l1111l_opy_(bstack1l1ll1_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼ࡪࡩࡹࡥࡢࡶ࡫࡯ࡨࡤࡲࡩ࡯࡭ࠥຂ"), datetime.datetime.now() - bstack1l1l1lll1_opy_)
            return [bstack1l1ll111l_opy_[bstack1l1ll1_opy_ (u"ࠬ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ຃")], bstack1l1ll11l1l_opy_]
    else:
      logger.warn(bstack1l11l11lll_opy_)
  except Exception as e:
    logger.debug(bstack11111l11_opy_.format(str(e)))
  return [None, None]
def bstack11ll1lllll_opy_(url, bstack1ll1l11l_opy_=False):
  global CONFIG
  global bstack1ll11ll11l_opy_
  if not bstack1ll11ll11l_opy_:
    hostname = bstack11lllll1l1_opy_(url)
    is_private = bstack1lll1111l1_opy_(hostname)
    if (bstack1l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪຄ") in CONFIG and not bstack11lll1lll1_opy_(CONFIG[bstack1l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ຅")])) and (is_private or bstack1ll1l11l_opy_):
      bstack1ll11ll11l_opy_ = hostname
def bstack11lllll1l1_opy_(url):
  return urlparse(url).hostname
def bstack1lll1111l1_opy_(hostname):
  for bstack1l1ll1111_opy_ in bstack11llll11l_opy_:
    regex = re.compile(bstack1l1ll1111_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1ll1lll1l_opy_(bstack1ll1l111_opy_):
  return True if bstack1ll1l111_opy_ in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack1ll1l11ll1_opy_, stage=STAGE.bstack1l1ll11ll1_opy_, bstack1llll1ll1l_opy_=bstack11111ll1_opy_)
def getAccessibilityResults(driver):
  global CONFIG
  global bstack111l1111_opy_
  bstack1lll1l1l1l_opy_ = not (bstack11l1ll11ll_opy_(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬຆ"), None) and bstack11l1ll11ll_opy_(
          threading.current_thread(), bstack1l1ll1_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨງ"), None))
  bstack111111lll_opy_ = getattr(driver, bstack1l1ll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪຈ"), None) != True
  bstack1l1llll11l_opy_ = bstack11l1ll11ll_opy_(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫຉ"), None) and bstack11l1ll11ll_opy_(
          threading.current_thread(), bstack1l1ll1_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧຊ"), None)
  if bstack1l1llll11l_opy_:
    if not bstack11ll1l1l1l_opy_():
      logger.warning(bstack1l1ll1_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡆࡶࡰࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴ࠰ࠥ຋"))
      return {}
    logger.debug(bstack1l1ll1_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠫຌ"))
    logger.debug(perform_scan(driver, driver_command=bstack1l1ll1_opy_ (u"ࠨࡧࡻࡩࡨࡻࡴࡦࡕࡦࡶ࡮ࡶࡴࠨຍ")))
    results = bstack1l11lll11_opy_(bstack1l1ll1_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡵࠥຎ"))
    if results is not None and results.get(bstack1l1ll1_opy_ (u"ࠥ࡭ࡸࡹࡵࡦࡵࠥຏ")) is not None:
        return results[bstack1l1ll1_opy_ (u"ࠦ࡮ࡹࡳࡶࡧࡶࠦຐ")]
    logger.error(bstack1l1ll1_opy_ (u"ࠧࡔ࡯ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡔࡨࡷࡺࡲࡴࡴࠢࡺࡩࡷ࡫ࠠࡧࡱࡸࡲࡩ࠴ࠢຑ"))
    return []
  if not bstack1l11ll1lll_opy_.bstack11ll1111l1_opy_(CONFIG, bstack111l1111_opy_) or (bstack111111lll_opy_ and bstack1lll1l1l1l_opy_):
    logger.warning(bstack1l1ll1_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳ࠯ࠤຒ"))
    return {}
  try:
    logger.debug(bstack1l1ll1_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠫຓ"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack1ll1l1l1l_opy_.bstack11l1l111_opy_)
    return results
  except Exception:
    logger.error(bstack1l1ll1_opy_ (u"ࠣࡐࡲࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡽࡥࡳࡧࠣࡪࡴࡻ࡮ࡥ࠰ࠥດ"))
    return {}
@measure(event_name=EVENTS.bstack11l1lll1_opy_, stage=STAGE.bstack1l1ll11ll1_opy_, bstack1llll1ll1l_opy_=bstack11111ll1_opy_)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack111l1111_opy_
  bstack1lll1l1l1l_opy_ = not (bstack11l1ll11ll_opy_(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ຕ"), None) and bstack11l1ll11ll_opy_(
          threading.current_thread(), bstack1l1ll1_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩຖ"), None))
  bstack111111lll_opy_ = getattr(driver, bstack1l1ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫທ"), None) != True
  bstack1l1llll11l_opy_ = bstack11l1ll11ll_opy_(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠬ࡯ࡳࡂࡲࡳࡅ࠶࠷ࡹࡕࡧࡶࡸࠬຘ"), None) and bstack11l1ll11ll_opy_(
          threading.current_thread(), bstack1l1ll1_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨນ"), None)
  if bstack1l1llll11l_opy_:
    if not bstack11ll1l1l1l_opy_():
      logger.warning(bstack1l1ll1_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡲࡳࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡪࡺࡲࡪࡧࡹࡩࠥࡇࡰࡱࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡷࡺࡳ࡭ࡢࡴࡼ࠲ࠧບ"))
      return {}
    logger.debug(bstack1l1ll1_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡹࡵ࡮࡯ࡤࡶࡾ࠭ປ"))
    logger.debug(perform_scan(driver, driver_command=bstack1l1ll1_opy_ (u"ࠩࡨࡼࡪࡩࡵࡵࡧࡖࡧࡷ࡯ࡰࡵࠩຜ")))
    results = bstack1l11lll11_opy_(bstack1l1ll1_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡖࡹࡲࡳࡡࡳࡻࠥຝ"))
    if results is not None and results.get(bstack1l1ll1_opy_ (u"ࠦࡸࡻ࡭࡮ࡣࡵࡽࠧພ")) is not None:
        return results[bstack1l1ll1_opy_ (u"ࠧࡹࡵ࡮࡯ࡤࡶࡾࠨຟ")]
    logger.error(bstack1l1ll1_opy_ (u"ࠨࡎࡰࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡕࡩࡸࡻ࡬ࡵࡵࠣࡗࡺࡳ࡭ࡢࡴࡼࠤࡼࡧࡳࠡࡨࡲࡹࡳࡪ࠮ࠣຠ"))
    return {}
  if not bstack1l11ll1lll_opy_.bstack11ll1111l1_opy_(CONFIG, bstack111l1111_opy_) or (bstack111111lll_opy_ and bstack1lll1l1l1l_opy_):
    logger.warning(bstack1l1ll1_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡶࡹࡲࡳࡡࡳࡻ࠱ࠦມ"))
    return {}
  try:
    logger.debug(bstack1l1ll1_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡹࡵ࡮࡯ࡤࡶࡾ࠭ຢ"))
    logger.debug(perform_scan(driver))
    bstack11ll1ll1l1_opy_ = driver.execute_async_script(bstack1ll1l1l1l_opy_.bstack1ll11l1ll1_opy_)
    return bstack11ll1ll1l1_opy_
  except Exception:
    logger.error(bstack1l1ll1_opy_ (u"ࠤࡑࡳࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡵ࡮࡯ࡤࡶࡾࠦࡷࡢࡵࠣࡪࡴࡻ࡮ࡥ࠰ࠥຣ"))
    return {}
def bstack11ll1l1l1l_opy_():
  global CONFIG
  global bstack111l1111_opy_
  bstack1lll11ll11_opy_ = bstack11l1ll11ll_opy_(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ຤"), None) and bstack11l1ll11ll_opy_(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ລ"), None)
  if not bstack1l11ll1lll_opy_.bstack11ll1111l1_opy_(CONFIG, bstack111l1111_opy_) or not bstack1lll11ll11_opy_:
        logger.warning(bstack1l1ll1_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡰࡱࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡶࡪࡹࡵ࡭ࡶࡶ࠲ࠧ຦"))
        return False
  return True
def bstack1l11lll11_opy_(bstack1l111llll_opy_):
    bstack1l11l11l1_opy_ = bstack1l1lll1l_opy_.current_test_uuid() if bstack1l1lll1l_opy_.current_test_uuid() else bstack111l1ll1l_opy_.current_hook_uuid()
    with ThreadPoolExecutor() as executor:
        future = executor.submit(bstack11ll11l111_opy_(bstack1l11l11l1_opy_, bstack1l111llll_opy_))
        try:
            return future.result(timeout=bstack1ll1ll111l_opy_)
        except TimeoutError:
            logger.error(bstack1l1ll1_opy_ (u"ࠨࡔࡪ࡯ࡨࡳࡺࡺࠠࡢࡨࡷࡩࡷࠦࡻࡾࡵࠣࡻ࡭࡯࡬ࡦࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡗ࡫ࡳࡶ࡮ࡷࡷࠧວ").format(bstack1ll1ll111l_opy_))
        except Exception as ex:
            logger.debug(bstack1l1ll1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡲࡦࡶࡵ࡭ࡪࡼࡩ࡯ࡩࠣࡅࡵࡶࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࢀࢃ࠮ࠡࡇࡵࡶࡴࡸࠠ࠮ࠢࡾࢁࠧຨ").format(bstack1l111llll_opy_, str(ex)))
    return {}
@measure(event_name=EVENTS.bstack1lll1l1ll_opy_, stage=STAGE.bstack1l1ll11ll1_opy_, bstack1llll1ll1l_opy_=bstack11111ll1_opy_)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack111l1111_opy_
  bstack1lll1l1l1l_opy_ = not (bstack11l1ll11ll_opy_(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬຩ"), None) and bstack11l1ll11ll_opy_(
          threading.current_thread(), bstack1l1ll1_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨສ"), None))
  bstack1ll11l11ll_opy_ = not (bstack11l1ll11ll_opy_(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪຫ"), None) and bstack11l1ll11ll_opy_(
          threading.current_thread(), bstack1l1ll1_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ຬ"), None))
  bstack111111lll_opy_ = getattr(driver, bstack1l1ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬອ"), None) != True
  if not bstack1l11ll1lll_opy_.bstack11ll1111l1_opy_(CONFIG, bstack111l1111_opy_) or (bstack111111lll_opy_ and bstack1lll1l1l1l_opy_ and bstack1ll11l11ll_opy_):
    logger.warning(bstack1l1ll1_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡵ࡯ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡧࡦࡴ࠮ࠣຮ"))
    return {}
  try:
    bstack11ll111lll_opy_ = bstack1l1ll1_opy_ (u"ࠧࡢࡲࡳࠫຯ") in CONFIG and CONFIG.get(bstack1l1ll1_opy_ (u"ࠨࡣࡳࡴࠬະ"), bstack1l1ll1_opy_ (u"ࠩࠪັ"))
    session_id = getattr(driver, bstack1l1ll1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠧາ"), None)
    if not session_id:
      logger.warning(bstack1l1ll1_opy_ (u"ࠦࡓࡵࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡋࡇࠤ࡫ࡵࡵ࡯ࡦࠣࡪࡴࡸࠠࡥࡴ࡬ࡺࡪࡸࠢຳ"))
      return {bstack1l1ll1_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦິ"): bstack1l1ll1_opy_ (u"ࠨࡎࡰࠢࡶࡩࡸࡹࡩࡰࡰࠣࡍࡉࠦࡦࡰࡷࡱࡨࠧີ")}
    if bstack11ll111lll_opy_:
      try:
        bstack1l11111ll1_opy_ = {
              bstack1l1ll1_opy_ (u"ࠧࡵࡪࡍࡻࡹ࡚࡯࡬ࡧࡱࠫຶ"): os.environ.get(bstack1l1ll1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ື"), os.environ.get(bstack1l1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍຸ࡛࡙࠭"), bstack1l1ll1_opy_ (u"ູࠪࠫ"))),
              bstack1l1ll1_opy_ (u"ࠫࡹ࡮ࡔࡦࡵࡷࡖࡺࡴࡕࡶ࡫ࡧ຺ࠫ"): bstack1l1lll1l_opy_.current_test_uuid() if bstack1l1lll1l_opy_.current_test_uuid() else bstack111l1ll1l_opy_.current_hook_uuid(),
              bstack1l1ll1_opy_ (u"ࠬࡧࡵࡵࡪࡋࡩࡦࡪࡥࡳࠩົ"): os.environ.get(bstack1l1ll1_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫຼ")),
              bstack1l1ll1_opy_ (u"ࠧࡴࡥࡤࡲ࡙࡯࡭ࡦࡵࡷࡥࡲࡶࠧຽ"): str(int(datetime.datetime.now().timestamp() * 1000)),
              bstack1l1ll1_opy_ (u"ࠨࡶ࡫ࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭຾"): os.environ.get(bstack1l1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ຿"), bstack1l1ll1_opy_ (u"ࠪࠫເ")),
              bstack1l1ll1_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࠫແ"): kwargs.get(bstack1l1ll1_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࡤࡩ࡯࡮࡯ࡤࡲࡩ࠭ໂ"), None) or bstack1l1ll1_opy_ (u"࠭ࠧໃ")
          }
        if not hasattr(thread_local, bstack1l1ll1_opy_ (u"ࠧࡣࡣࡶࡩࡤࡧࡰࡱࡡࡤ࠵࠶ࡿ࡟ࡴࡥࡵ࡭ࡵࡺࠧໄ")):
            scripts = {bstack1l1ll1_opy_ (u"ࠨࡵࡦࡥࡳ࠭໅"): bstack1ll1l1l1l_opy_.perform_scan}
            thread_local.base_app_a11y_script = scripts
        bstack1l11lll1ll_opy_ = copy.deepcopy(thread_local.base_app_a11y_script)
        bstack1l11lll1ll_opy_[bstack1l1ll1_opy_ (u"ࠩࡶࡧࡦࡴࠧໆ")] = bstack1l11lll1ll_opy_[bstack1l1ll1_opy_ (u"ࠪࡷࡨࡧ࡮ࠨ໇")] % json.dumps(bstack1l11111ll1_opy_)
        bstack1ll1l1l1l_opy_.bstack1l11lll111_opy_(bstack1l11lll1ll_opy_)
        bstack1ll1l1l1l_opy_.store()
        bstack11ll1l1l_opy_ = driver.execute_script(bstack1ll1l1l1l_opy_.perform_scan)
      except Exception as bstack11l11l111l_opy_:
        logger.info(bstack1l1ll1_opy_ (u"ࠦࡆࡶࡰࡪࡷࡰࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸࡩࡡ࡯ࠢࡩࡥ࡮ࡲࡥࡥ࠼່ࠣࠦ") + str(bstack11l11l111l_opy_))
        bstack11ll1l1l_opy_ = {bstack1l1ll1_opy_ (u"ࠧ࡫ࡲࡳࡱࡵ້ࠦ"): str(bstack11l11l111l_opy_)}
    else:
      bstack11ll1l1l_opy_ = driver.execute_async_script(bstack1ll1l1l1l_opy_.perform_scan, {bstack1l1ll1_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩ໊࠭"): kwargs.get(bstack1l1ll1_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸ࡟ࡤࡱࡰࡱࡦࡴࡤࠨ໋"), None) or bstack1l1ll1_opy_ (u"ࠨࠩ໌")})
    return bstack11ll1l1l_opy_
  except Exception as err:
    logger.error(bstack1l1ll1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡸࡵ࡯ࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡧࡦࡴ࠮ࠡࡽࢀࠦໍ").format(str(err)))
    return {}