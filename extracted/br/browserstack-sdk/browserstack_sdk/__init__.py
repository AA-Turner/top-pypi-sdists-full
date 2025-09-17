# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
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
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import json
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from browserstack_sdk.bstack11l111lll_opy_ import bstack1llll111_opy_
from browserstack_sdk.bstack1lll1l11l_opy_ import *
import time
import requests
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.measure import measure
def bstack1l11l1lll1_opy_():
  global CONFIG
  headers = {
        bstack1l11ll1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack1l11ll1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack11llllll11_opy_(CONFIG, bstack1l1lllll1l_opy_)
  try:
    response = requests.get(bstack1l1lllll1l_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1l1111llll_opy_ = response.json()[bstack1l11ll1_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1l11111l_opy_.format(response.json()))
      return bstack1l1111llll_opy_
    else:
      logger.debug(bstack11l1l1ll11_opy_.format(bstack1l11ll1_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack11l1l1ll11_opy_.format(e))
def bstack1111ll11_opy_(hub_url):
  global CONFIG
  url = bstack1l11ll1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack1l11ll1_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack1l11ll1_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack1l11ll1_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack11llllll11_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack111lllll_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1l11ll1111_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack11llll1l1_opy_, stage=STAGE.bstack11lllll111_opy_)
def bstack1ll1ll111l_opy_():
  try:
    global bstack11lll1ll11_opy_
    bstack1l1111llll_opy_ = bstack1l11l1lll1_opy_()
    bstack1l1l1l1l1_opy_ = []
    results = []
    for bstack1llllll11_opy_ in bstack1l1111llll_opy_:
      bstack1l1l1l1l1_opy_.append(bstack1l1ll11l1l_opy_(target=bstack1111ll11_opy_,args=(bstack1llllll11_opy_,)))
    for t in bstack1l1l1l1l1_opy_:
      t.start()
    for t in bstack1l1l1l1l1_opy_:
      results.append(t.join())
    bstack11l111l11l_opy_ = {}
    for item in results:
      hub_url = item[bstack1l11ll1_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack1l11ll1_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack11l111l11l_opy_[hub_url] = latency
    bstack1lllll1l11_opy_ = min(bstack11l111l11l_opy_, key= lambda x: bstack11l111l11l_opy_[x])
    bstack11lll1ll11_opy_ = bstack1lllll1l11_opy_
    logger.debug(bstack11l111l1l_opy_.format(bstack1lllll1l11_opy_))
  except Exception as e:
    logger.debug(bstack11l11ll1l1_opy_.format(e))
from browserstack_sdk.bstack1111l11l1_opy_ import *
from browserstack_sdk.bstack1ll1l1lll1_opy_ import *
from browserstack_sdk.bstack11ll111l1l_opy_ import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.bstack1lll1l1l1l_opy_ import get_logger
from bstack_utils.measure import measure
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack1lll1l1111_opy_, stage=STAGE.bstack11lllll111_opy_)
def bstack11l1lll11_opy_():
    global bstack11lll1ll11_opy_
    try:
        bstack11lll111l_opy_ = bstack11l111ll1_opy_()
        bstack11lll11ll_opy_(bstack11lll111l_opy_)
        hub_url = bstack11lll111l_opy_.get(bstack1l11ll1_opy_ (u"ࠨࡵࡳ࡮ࠥࢀ"), bstack1l11ll1_opy_ (u"ࠢࠣࢁ"))
        if hub_url.endswith(bstack1l11ll1_opy_ (u"ࠨ࠱ࡺࡨ࠴࡮ࡵࡣࠩࢂ")):
            hub_url = hub_url.rsplit(bstack1l11ll1_opy_ (u"ࠩ࠲ࡻࡩ࠵ࡨࡶࡤࠪࢃ"), 1)[0]
        if hub_url.startswith(bstack1l11ll1_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫࢄ")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack1l11ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࠭ࢅ")):
            hub_url = hub_url[8:]
        bstack11lll1ll11_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack11l111ll1_opy_():
    global CONFIG
    bstack1lllll11l1_opy_ = CONFIG.get(bstack1l11ll1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢆ"), {}).get(bstack1l11ll1_opy_ (u"࠭ࡧࡳ࡫ࡧࡒࡦࡳࡥࠨࢇ"), bstack1l11ll1_opy_ (u"ࠧࡏࡑࡢࡋࡗࡏࡄࡠࡐࡄࡑࡊࡥࡐࡂࡕࡖࡉࡉ࠭࢈"))
    if not isinstance(bstack1lllll11l1_opy_, str):
        raise ValueError(bstack1l11ll1_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡈࡴ࡬ࡨࠥࡴࡡ࡮ࡧࠣࡱࡺࡹࡴࠡࡤࡨࠤࡦࠦࡶࡢ࡮࡬ࡨࠥࡹࡴࡳ࡫ࡱ࡫ࠧࢉ"))
    try:
        bstack11lll111l_opy_ = bstack1lll11ll1_opy_(bstack1lllll11l1_opy_)
        return bstack11lll111l_opy_
    except Exception as e:
        logger.error(bstack1l11ll1_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣࢊ").format(str(e)))
        return {}
def bstack1lll11ll1_opy_(bstack1lllll11l1_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack1l11ll1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࢋ")] or not CONFIG[bstack1l11ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧࢌ")]:
            raise ValueError(bstack1l11ll1_opy_ (u"ࠧࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠠࡰࡴࠣࡥࡨࡩࡥࡴࡵࠣ࡯ࡪࡿࠢࢍ"))
        url = bstack1l1l1ll11_opy_ + bstack1lllll11l1_opy_
        auth = (CONFIG[bstack1l11ll1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨࢎ")], CONFIG[bstack1l11ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ࢏")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack1l11lll11_opy_ = json.loads(response.text)
            return bstack1l11lll11_opy_
    except ValueError as ve:
        logger.error(bstack1l11ll1_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣ࢐").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack1l11ll1_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥ࡭ࡲࡪࡦࠣࡨࡪࡺࡡࡪ࡮ࡶࠤ࠿ࠦࡻࡾࠤ࢑").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack11lll11ll_opy_(bstack11ll11l11l_opy_):
    global CONFIG
    if bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ࢒") not in CONFIG or str(CONFIG[bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ࢓")]).lower() == bstack1l11ll1_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ࢔"):
        CONFIG[bstack1l11ll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬ࢕")] = False
    elif bstack1l11ll1_opy_ (u"ࠧࡪࡵࡗࡶ࡮ࡧ࡬ࡈࡴ࡬ࡨࠬ࢖") in bstack11ll11l11l_opy_:
        bstack1llll1ll1_opy_ = CONFIG.get(bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢗ"), {})
        logger.debug(bstack1l11ll1_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡰࡴࡩࡡ࡭ࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࠪࡹࠢ࢘"), bstack1llll1ll1_opy_)
        bstack11ll1ll1l1_opy_ = bstack11ll11l11l_opy_.get(bstack1l11ll1_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡕࡩࡵ࡫ࡡࡵࡧࡵࡷ࢙ࠧ"), [])
        bstack1l1ll11l_opy_ = bstack1l11ll1_opy_ (u"ࠦ࠱ࠨ࢚").join(bstack11ll1ll1l1_opy_)
        logger.debug(bstack1l11ll1_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡈࡻࡳࡵࡱࡰࠤࡷ࡫ࡰࡦࡣࡷࡩࡷࠦࡳࡵࡴ࡬ࡲ࡬ࡀࠠࠦࡵ࢛ࠥ"), bstack1l1ll11l_opy_)
        bstack1l1l111l11_opy_ = {
            bstack1l11ll1_opy_ (u"ࠨ࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣ࢜"): bstack1l11ll1_opy_ (u"ࠢࡢࡶࡶ࠱ࡷ࡫ࡰࡦࡣࡷࡩࡷࠨ࢝"),
            bstack1l11ll1_opy_ (u"ࠣࡨࡲࡶࡨ࡫ࡌࡰࡥࡤࡰࠧ࢞"): bstack1l11ll1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ࢟"),
            bstack1l11ll1_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠧࢠ"): bstack1l1ll11l_opy_
        }
        bstack1llll1ll1_opy_.update(bstack1l1l111l11_opy_)
        logger.debug(bstack1l11ll1_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼࡙ࠣࡵࡪࡡࡵࡧࡧࠤࡱࡵࡣࡢ࡮ࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࠫࡳࠣࢡ"), bstack1llll1ll1_opy_)
        CONFIG[bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢢ")] = bstack1llll1ll1_opy_
        logger.debug(bstack1l11ll1_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡌࡩ࡯ࡣ࡯ࠤࡈࡕࡎࡇࡋࡊ࠾ࠥࠫࡳࠣࢣ"), CONFIG)
def bstack1ll1lll11l_opy_():
    bstack11lll111l_opy_ = bstack11l111ll1_opy_()
    if not bstack11lll111l_opy_[bstack1l11ll1_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࡙ࡷࡲࠧࢤ")]:
      raise ValueError(bstack1l11ll1_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࡚ࡸ࡬ࠡ࡫ࡶࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࡬ࡲࡰ࡯ࠣ࡫ࡷ࡯ࡤࠡࡦࡨࡸࡦ࡯࡬ࡴ࠰ࠥࢥ"))
    return bstack11lll111l_opy_[bstack1l11ll1_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࡛ࡲ࡭ࠩࢦ")] + bstack1l11ll1_opy_ (u"ࠪࡃࡨࡧࡰࡴ࠿ࠪࢧ")
@measure(event_name=EVENTS.bstack11ll1l1l1l_opy_, stage=STAGE.bstack11lllll111_opy_)
def bstack1ll1111ll_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack1l11ll1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ࢨ")], CONFIG[bstack1l11ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࢩ")])
        url = bstack1l1111l111_opy_
        logger.debug(bstack1l11ll1_opy_ (u"ࠨࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬ࡲࡰ࡯ࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡗࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࠦࡁࡑࡋࠥࢪ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack1l11ll1_opy_ (u"ࠢࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪࠨࢫ"): bstack1l11ll1_opy_ (u"ࠣࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠦࢬ")})
            if response.status_code == 200:
                bstack1l1l1111_opy_ = json.loads(response.text)
                bstack1l1l111111_opy_ = bstack1l1l1111_opy_.get(bstack1l11ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡴࠩࢭ"), [])
                if bstack1l1l111111_opy_:
                    bstack1l1l1l11l_opy_ = bstack1l1l111111_opy_[0]
                    build_hashed_id = bstack1l1l1l11l_opy_.get(bstack1l11ll1_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ࢮ"))
                    bstack1lllll111_opy_ = bstack1l1ll1l1l_opy_ + build_hashed_id
                    result.extend([build_hashed_id, bstack1lllll111_opy_])
                    logger.info(bstack1l111l1l1_opy_.format(bstack1lllll111_opy_))
                    bstack1ll111l11l_opy_ = CONFIG[bstack1l11ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧࢯ")]
                    if bstack1l11ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢰ") in CONFIG:
                      bstack1ll111l11l_opy_ += bstack1l11ll1_opy_ (u"࠭ࠠࠨࢱ") + CONFIG[bstack1l11ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࢲ")]
                    if bstack1ll111l11l_opy_ != bstack1l1l1l11l_opy_.get(bstack1l11ll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ࢳ")):
                      logger.debug(bstack1ll1lll11_opy_.format(bstack1l1l1l11l_opy_.get(bstack1l11ll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧࢴ")), bstack1ll111l11l_opy_))
                    return result
                else:
                    logger.debug(bstack1l11ll1_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡑࡳࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡵࡪࡨࠤࡷ࡫ࡳࡱࡱࡱࡷࡪ࠴ࠢࢵ"))
            else:
                logger.debug(bstack1l11ll1_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢶ"))
        except Exception as e:
            logger.error(bstack1l11ll1_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࡹࠠ࠻ࠢࡾࢁࠧࢷ").format(str(e)))
    else:
        logger.debug(bstack1l11ll1_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡉࡏࡏࡈࡌࡋࠥ࡯ࡳࠡࡰࡲࡸࠥࡹࡥࡵ࠰࡙ࠣࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢸ"))
    return [None, None]
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1l1111l1_opy_ import bstack1l1111l1_opy_, bstack1l11lll111_opy_, bstack1l111111l_opy_, bstack1ll1111l1_opy_
from bstack_utils.measure import bstack1lll11l1_opy_
from bstack_utils.measure import measure
from bstack_utils.percy import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1lll1lllll_opy_ import bstack111ll1111_opy_
from bstack_utils.messages import *
from bstack_utils import bstack1lll1l1l1l_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack11l1llll_opy_, bstack1l1ll1ll1l_opy_, bstack1ll1111l1l_opy_, bstack1l11111ll_opy_, \
  bstack1llll1llll_opy_, \
  Notset, bstack11lll11111_opy_, \
  bstack1l1ll1111l_opy_, bstack1l111l1ll_opy_, bstack11ll1111l1_opy_, bstack1lll11ll1l_opy_, bstack1l11llll11_opy_, bstack1l11l1l1ll_opy_, \
  bstack1ll1l1ll1l_opy_, \
  bstack1l1ll111_opy_, bstack111111l11_opy_, bstack1ll111ll11_opy_, bstack11ll1lll1l_opy_, \
  bstack1l1111l11_opy_, bstack11ll11111l_opy_, bstack11l1ll11l1_opy_, bstack1l11ll1ll1_opy_
from bstack_utils.bstack11l1l111l1_opy_ import bstack1111l1lll_opy_
from bstack_utils.bstack1l11l1111l_opy_ import bstack11ll11l111_opy_, bstack11l1l1l1l1_opy_
from bstack_utils.bstack11lll1l111_opy_ import bstack1ll1l11l11_opy_
from bstack_utils.bstack11l1111111_opy_ import bstack1l1l111l1_opy_, bstack1llllll11l_opy_
from bstack_utils.bstack1l11l11l_opy_ import bstack1l11l11l_opy_
from bstack_utils.bstack1l11l111l_opy_ import bstack11lll111l1_opy_
from bstack_utils.proxy import bstack111lll1lll_opy_, bstack11llllll11_opy_, bstack111l1l1l_opy_, bstack1l111ll11_opy_
from bstack_utils.bstack1l1llll111_opy_ import bstack111ll1l1l_opy_
import bstack_utils.bstack11l111llll_opy_ as bstack1ll111ll_opy_
import bstack_utils.bstack1ll1111ll1_opy_ as bstack11ll11ll_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.utils.bstack1l1lll1ll_opy_ import bstack1111l1l11_opy_
from bstack_utils.bstack11ll1lll1_opy_ import bstack11llll1111_opy_
from bstack_utils.bstack1l111lll1_opy_ import bstack1llllll1l_opy_
if os.getenv(bstack1l11ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡌࡔࡕࡋࡔࠩࢹ")):
  cli.bstack1111llll_opy_()
else:
  os.environ[bstack1l11ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡍࡕࡏࡌࡕࠪࢺ")] = bstack1l11ll1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧࢻ")
bstack11ll111l1_opy_ = bstack1l11ll1_opy_ (u"ࠪࠤࠥ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࠣࠤ࡮࡬ࠨࡱࡣࡪࡩࠥࡃ࠽࠾ࠢࡹࡳ࡮ࡪࠠ࠱ࠫࠣࡿࡡࡴࠠࠡࠢࡷࡶࡾࢁ࡜࡯ࠢࡦࡳࡳࡹࡴࠡࡨࡶࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨ࡝ࠩࡩࡷࡡ࠭ࠩ࠼࡞ࡱࠤࠥࠦࠠࠡࡨࡶ࠲ࡦࡶࡰࡦࡰࡧࡊ࡮ࡲࡥࡔࡻࡱࡧ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪ࠯ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡶ࡟ࡪࡰࡧࡩࡽ࠯ࠠࠬࠢࠥ࠾ࠧࠦࠫࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࠨࡢࡹࡤ࡭ࡹࠦ࡮ࡦࡹࡓࡥ࡬࡫࠲࠯ࡧࡹࡥࡱࡻࡡࡵࡧࠫࠦ࠭࠯ࠠ࠾ࡀࠣࡿࢂࠨࠬࠡ࡞ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥ࡫ࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡄࡦࡶࡤ࡭ࡱࡹࠢࡾ࡞ࠪ࠭࠮࠯࡛ࠣࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠦࡢ࠯ࠠࠬࠢࠥ࠰ࡡࡢ࡮ࠣࠫ࡟ࡲࠥࠦࠠࠡࡿࡦࡥࡹࡩࡨࠩࡧࡻ࠭ࢀࡢ࡮ࠡࠢࠣࠤࢂࡢ࡮ࠡࠢࢀࡠࡳࠦࠠ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱ࠪࢼ")
bstack1l1ll1ll1_opy_ = bstack1l11ll1_opy_ (u"ࠫࡡࡴ࠯ࠫࠢࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࠦࠪ࠰࡞ࡱࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠶ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡩࡡࡱࡵࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠷࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡲࡢ࡭ࡳࡪࡥࡹࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠷ࡣ࡜࡯ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯ࡵ࡯࡭ࡨ࡫ࠨ࠱࠮ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸࠯࡜࡯ࡥࡲࡲࡸࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯ࠥࡃࠠࡳࡧࡴࡹ࡮ࡸࡥࠩࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨࠩ࠼࡞ࡱ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡰࡦࡻ࡮ࡤࡪࠣࡁࠥࡧࡳࡺࡰࡦࠤ࠭ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷ࠮ࠦ࠽࠿ࠢࡾࡠࡳࡲࡥࡵࠢࡦࡥࡵࡹ࠻࡝ࡰࡷࡶࡾࠦࡻ࡝ࡰࡦࡥࡵࡹࠠ࠾ࠢࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࡢࡴࡶࡤࡧࡰࡥࡣࡢࡲࡶ࠭ࡡࡴࠠࠡࡿࠣࡧࡦࡺࡣࡩࠪࡨࡼ࠮ࠦࡻ࡝ࡰࠣࠤࠥࠦࡽ࡝ࡰࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࠻ࠢࡣࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠩࢁࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭ࢂࡦࠬ࡝ࡰࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴ࡞ࡱࠤࠥࢃࠩ࡝ࡰࢀࡠࡳ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࠪࢽ")
from ._version import __version__
bstack11ll11l1_opy_ = None
CONFIG = {}
bstack1lll111l11_opy_ = {}
bstack1l1lllll11_opy_ = {}
bstack1l111l1lll_opy_ = None
bstack1llll11l1_opy_ = None
bstack1l11111l1l_opy_ = None
bstack11ll1llll_opy_ = -1
bstack11l1l11ll_opy_ = 0
bstack111111ll1_opy_ = bstack11lllll1l1_opy_
bstack11ll11ll1_opy_ = 1
bstack11llll111_opy_ = False
bstack11lllll1l_opy_ = False
bstack11ll1l1l11_opy_ = bstack1l11ll1_opy_ (u"ࠬ࠭ࢾ")
bstack1l1111111l_opy_ = bstack1l11ll1_opy_ (u"࠭ࠧࢿ")
bstack1lllll11l_opy_ = False
bstack1111lll1_opy_ = True
bstack1lll1ll11l_opy_ = bstack1l11ll1_opy_ (u"ࠧࠨࣀ")
bstack11l11lll1l_opy_ = []
bstack111ll111_opy_ = threading.Lock()
bstack11l1l11l1l_opy_ = threading.Lock()
bstack11lll1ll11_opy_ = bstack1l11ll1_opy_ (u"ࠨࠩࣁ")
bstack1ll11ll111_opy_ = False
bstack1l111111_opy_ = None
bstack1lllll1ll1_opy_ = None
bstack1l1ll1ll11_opy_ = None
bstack11l1l1111_opy_ = -1
bstack1ll11l11ll_opy_ = os.path.join(os.path.expanduser(bstack1l11ll1_opy_ (u"ࠩࢁࠫࣂ")), bstack1l11ll1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪࣃ"), bstack1l11ll1_opy_ (u"ࠫ࠳ࡸ࡯ࡣࡱࡷ࠱ࡷ࡫ࡰࡰࡴࡷ࠱࡭࡫࡬ࡱࡧࡵ࠲࡯ࡹ࡯࡯ࠩࣄ"))
bstack1l11l11l11_opy_ = 0
bstack11l1lll1_opy_ = 0
bstack1lll11llll_opy_ = []
bstack11l1111l_opy_ = []
bstack1lll1lll1l_opy_ = []
bstack1l1lll1l1l_opy_ = []
bstack1l11l11lll_opy_ = bstack1l11ll1_opy_ (u"ࠬ࠭ࣅ")
bstack1ll1l11l1l_opy_ = bstack1l11ll1_opy_ (u"࠭ࠧࣆ")
bstack1ll11111ll_opy_ = False
bstack1l1l1ll1l1_opy_ = False
bstack11ll1l1ll1_opy_ = {}
bstack1ll11lll_opy_ = None
bstack1l1l1ll1_opy_ = None
bstack1ll11l111l_opy_ = None
bstack1ll111lll1_opy_ = None
bstack1l1ll11111_opy_ = None
bstack11ll1llll1_opy_ = None
bstack11l111l1_opy_ = None
bstack1111l1l1l_opy_ = None
bstack1l1ll111l_opy_ = None
bstack11l1l11l1_opy_ = None
bstack11ll111111_opy_ = None
bstack11ll11l1l_opy_ = None
bstack111lll111_opy_ = None
bstack11lll1ll1_opy_ = None
bstack1l1lll1111_opy_ = None
bstack1lll1llll_opy_ = None
bstack111l11l11_opy_ = None
bstack1l1l1l1l_opy_ = None
bstack1111l1ll1_opy_ = None
bstack1ll1l111ll_opy_ = None
bstack1ll111111_opy_ = None
bstack11ll1l11ll_opy_ = None
bstack1l1111lll_opy_ = None
thread_local = threading.local()
bstack111l11ll1_opy_ = False
bstack1lll1l1ll_opy_ = bstack1l11ll1_opy_ (u"ࠢࠣࣇ")
logger = bstack1lll1l1l1l_opy_.get_logger(__name__, bstack111111ll1_opy_)
bstack111lllll11_opy_ = Config.bstack1lll111l1l_opy_()
percy = bstack1111l11l_opy_()
bstack11ll11ll1l_opy_ = bstack111ll1111_opy_()
bstack1lllll1111_opy_ = bstack11ll111l1l_opy_()
def bstack11l1111l1l_opy_():
  global CONFIG
  global bstack1ll11111ll_opy_
  global bstack111lllll11_opy_
  testContextOptions = bstack1ll11ll1l1_opy_(CONFIG)
  if bstack1llll1llll_opy_(CONFIG):
    if (bstack1l11ll1_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪࣈ") in testContextOptions and str(testContextOptions[bstack1l11ll1_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫࣉ")]).lower() == bstack1l11ll1_opy_ (u"ࠪࡸࡷࡻࡥࠨ࣊")):
      bstack1ll11111ll_opy_ = True
    bstack111lllll11_opy_.bstack1l11ll1l_opy_(testContextOptions.get(bstack1l11ll1_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ࣋"), False))
  else:
    bstack1ll11111ll_opy_ = True
    bstack111lllll11_opy_.bstack1l11ll1l_opy_(True)
def bstack1l1lll1l_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack11llll11ll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1ll1ll1l11_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1l11ll1_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡩ࡯࡯ࡨ࡬࡫࡫࡯࡬ࡦࠤ࣌") == args[i].lower() or bstack1l11ll1_opy_ (u"ࠨ࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡪ࡮࡭ࠢ࣍") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1lll1ll11l_opy_
      bstack1lll1ll11l_opy_ += bstack1l11ll1_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠤࠬ࣎") + shlex.quote(path)
      return path
  return None
bstack1l11lll1l1_opy_ = re.compile(bstack1l11ll1_opy_ (u"ࡳࠤ࠱࠮ࡄࡢࠤࡼࠪ࠱࠮ࡄ࠯ࡽ࠯ࠬࡂ࣏ࠦ"))
def bstack111lll1l_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1l11lll1l1_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack1l11ll1_opy_ (u"ࠤࠧࡿ࣐ࠧ") + group + bstack1l11ll1_opy_ (u"ࠥࢁ࣑ࠧ"), os.environ.get(group))
  return value
def bstack1ll1l111_opy_():
  global bstack1l1111lll_opy_
  if bstack1l1111lll_opy_ is None:
        bstack1l1111lll_opy_ = bstack1ll1ll1l11_opy_()
  bstack1ll11llll_opy_ = bstack1l1111lll_opy_
  if bstack1ll11llll_opy_ and os.path.exists(os.path.abspath(bstack1ll11llll_opy_)):
    fileName = bstack1ll11llll_opy_
  if bstack1l11ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ࣒") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack1l11ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆ࣓ࠩ")])) and not bstack1l11ll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡒࡦࡳࡥࠨࣔ") in locals():
    fileName = os.environ[bstack1l11ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫࣕ")]
  if bstack1l11ll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡔࡡ࡮ࡧࠪࣖ") in locals():
    bstack111l111_opy_ = os.path.abspath(fileName)
  else:
    bstack111l111_opy_ = bstack1l11ll1_opy_ (u"ࠩࠪࣗ")
  bstack1ll1l1l1_opy_ = os.getcwd()
  bstack1l1lll111_opy_ = bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ࣘ")
  bstack111111l1_opy_ = bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡦࡳ࡬ࠨࣙ")
  while (not os.path.exists(bstack111l111_opy_)) and bstack1ll1l1l1_opy_ != bstack1l11ll1_opy_ (u"ࠧࠨࣚ"):
    bstack111l111_opy_ = os.path.join(bstack1ll1l1l1_opy_, bstack1l1lll111_opy_)
    if not os.path.exists(bstack111l111_opy_):
      bstack111l111_opy_ = os.path.join(bstack1ll1l1l1_opy_, bstack111111l1_opy_)
    if bstack1ll1l1l1_opy_ != os.path.dirname(bstack1ll1l1l1_opy_):
      bstack1ll1l1l1_opy_ = os.path.dirname(bstack1ll1l1l1_opy_)
    else:
      bstack1ll1l1l1_opy_ = bstack1l11ll1_opy_ (u"ࠨࠢࣛ")
  bstack1l1111lll_opy_ = bstack111l111_opy_ if os.path.exists(bstack111l111_opy_) else None
  return bstack1l1111lll_opy_
def bstack1l1ll11l11_opy_(config):
    if bstack1l11ll1_opy_ (u"ࠧࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭ࠧࣜ") in config:
      config[bstack1l11ll1_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬࣝ")] = config[bstack1l11ll1_opy_ (u"ࠩࡷࡩࡸࡺࡒࡦࡲࡲࡶࡹ࡯࡮ࡨࠩࣞ")]
    if bstack1l11ll1_opy_ (u"ࠪࡸࡪࡹࡴࡓࡧࡳࡳࡷࡺࡩ࡯ࡩࡒࡴࡹ࡯࡯࡯ࡵࠪࣟ") in config:
      config[bstack1l11ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ࣠")] = config[bstack1l11ll1_opy_ (u"ࠬࡺࡥࡴࡶࡕࡩࡵࡵࡲࡵ࡫ࡱ࡫ࡔࡶࡴࡪࡱࡱࡷࠬ࣡")]
def bstack11lllllll1_opy_():
  bstack111l111_opy_ = bstack1ll1l111_opy_()
  if not os.path.exists(bstack111l111_opy_):
    bstack1ll1l1l11_opy_(
      bstack11ll1ll11_opy_.format(os.getcwd()))
  try:
    with open(bstack111l111_opy_, bstack1l11ll1_opy_ (u"࠭ࡲࠨ࣢")) as stream:
      yaml.add_implicit_resolver(bstack1l11ll1_opy_ (u"ࠢࠢࡲࡤࡸ࡭࡫ࡸࣣࠣ"), bstack1l11lll1l1_opy_)
      yaml.add_constructor(bstack1l11ll1_opy_ (u"ࠣࠣࡳࡥࡹ࡮ࡥࡹࠤࣤ"), bstack111lll1l_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      bstack1l1ll11l11_opy_(config)
      return config
  except:
    with open(bstack111l111_opy_, bstack1l11ll1_opy_ (u"ࠩࡵࠫࣥ")) as stream:
      try:
        config = yaml.safe_load(stream)
        bstack1l1ll11l11_opy_(config)
        return config
      except yaml.YAMLError as exc:
        bstack1ll1l1l11_opy_(bstack1ll1lllll1_opy_.format(str(exc)))
def bstack1l1l1ll1l_opy_(config):
  bstack11lll1l1_opy_ = bstack1ll1lllll_opy_(config)
  for option in list(bstack11lll1l1_opy_):
    if option.lower() in bstack1l11ll1l1_opy_ and option != bstack1l11ll1l1_opy_[option.lower()]:
      bstack11lll1l1_opy_[bstack1l11ll1l1_opy_[option.lower()]] = bstack11lll1l1_opy_[option]
      del bstack11lll1l1_opy_[option]
  return config
def bstack111l1l11l_opy_():
  global bstack1l1lllll11_opy_
  for key, bstack11ll1ll1ll_opy_ in bstack1l11111111_opy_.items():
    if isinstance(bstack11ll1ll1ll_opy_, list):
      for var in bstack11ll1ll1ll_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1l1lllll11_opy_[key] = os.environ[var]
          break
    elif bstack11ll1ll1ll_opy_ in os.environ and os.environ[bstack11ll1ll1ll_opy_] and str(os.environ[bstack11ll1ll1ll_opy_]).strip():
      bstack1l1lllll11_opy_[key] = os.environ[bstack11ll1ll1ll_opy_]
  if bstack1l11ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࣦࠬ") in os.environ:
    bstack1l1lllll11_opy_[bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣧ")] = {}
    bstack1l1lllll11_opy_[bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣨ")][bstack1l11ll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣩ")] = os.environ[bstack1l11ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩ࣪")]
def bstack1l111lll1l_opy_():
  global bstack1lll111l11_opy_
  global bstack1lll1ll11l_opy_
  bstack1l1l1l111l_opy_ = []
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) - 1 and bstack1l11ll1_opy_ (u"ࠨ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ࣫").lower() == val.lower():
      bstack1lll111l11_opy_[bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭࣬")] = {}
      bstack1lll111l11_opy_[bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹ࣭ࠧ")][bstack1l11ll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࣮࠭")] = sys.argv[idx + 1]
      bstack1l1l1l111l_opy_.extend([idx, idx + 1])
      break
  for key, bstack1l1l11111l_opy_ in bstack11l11111ll_opy_.items():
    if isinstance(bstack1l1l11111l_opy_, list):
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        for var in bstack1l1l11111l_opy_:
          if bstack1l11ll1_opy_ (u"ࠬ࠳࠭ࠨ࣯") + var.lower() == val.lower() and key not in bstack1lll111l11_opy_:
            bstack1lll111l11_opy_[key] = sys.argv[idx + 1]
            bstack1lll1ll11l_opy_ += bstack1l11ll1_opy_ (u"࠭ࠠ࠮࠯ࣰࠪ") + var + bstack1l11ll1_opy_ (u"ࣱࠧࠡࠩ") + shlex.quote(sys.argv[idx + 1])
            bstack1l1l1l111l_opy_.extend([idx, idx + 1])
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        if bstack1l11ll1_opy_ (u"ࠨ࠯࠰ࣲࠫ") + bstack1l1l11111l_opy_.lower() == val.lower() and key not in bstack1lll111l11_opy_:
          bstack1lll111l11_opy_[key] = sys.argv[idx + 1]
          bstack1lll1ll11l_opy_ += bstack1l11ll1_opy_ (u"ࠩࠣ࠱࠲࠭ࣳ") + bstack1l1l11111l_opy_ + bstack1l11ll1_opy_ (u"ࠪࠤࠬࣴ") + shlex.quote(sys.argv[idx + 1])
          bstack1l1l1l111l_opy_.extend([idx, idx + 1])
  for idx in sorted(set(bstack1l1l1l111l_opy_), reverse=True):
    if idx < len(sys.argv):
      del sys.argv[idx]
def bstack1l1l111ll1_opy_(config):
  bstack111llll1l1_opy_ = config.keys()
  for bstack111ll1l11_opy_, bstack11l111l111_opy_ in bstack1ll1ll111_opy_.items():
    if bstack11l111l111_opy_ in bstack111llll1l1_opy_:
      config[bstack111ll1l11_opy_] = config[bstack11l111l111_opy_]
      del config[bstack11l111l111_opy_]
  for bstack111ll1l11_opy_, bstack11l111l111_opy_ in bstack11l1l1111l_opy_.items():
    if isinstance(bstack11l111l111_opy_, list):
      for bstack111111l1l_opy_ in bstack11l111l111_opy_:
        if bstack111111l1l_opy_ in bstack111llll1l1_opy_:
          config[bstack111ll1l11_opy_] = config[bstack111111l1l_opy_]
          del config[bstack111111l1l_opy_]
          break
    elif bstack11l111l111_opy_ in bstack111llll1l1_opy_:
      config[bstack111ll1l11_opy_] = config[bstack11l111l111_opy_]
      del config[bstack11l111l111_opy_]
  for bstack111111l1l_opy_ in list(config):
    for bstack111111ll_opy_ in bstack1111lll11_opy_:
      if bstack111111l1l_opy_.lower() == bstack111111ll_opy_.lower() and bstack111111l1l_opy_ != bstack111111ll_opy_:
        config[bstack111111ll_opy_] = config[bstack111111l1l_opy_]
        del config[bstack111111l1l_opy_]
  bstack1l11llll1l_opy_ = [{}]
  if not config.get(bstack1l11ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣵ")):
    config[bstack1l11ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨࣶ")] = [{}]
  bstack1l11llll1l_opy_ = config[bstack1l11ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩࣷ")]
  for platform in bstack1l11llll1l_opy_:
    for bstack111111l1l_opy_ in list(platform):
      for bstack111111ll_opy_ in bstack1111lll11_opy_:
        if bstack111111l1l_opy_.lower() == bstack111111ll_opy_.lower() and bstack111111l1l_opy_ != bstack111111ll_opy_:
          platform[bstack111111ll_opy_] = platform[bstack111111l1l_opy_]
          del platform[bstack111111l1l_opy_]
  for bstack111ll1l11_opy_, bstack11l111l111_opy_ in bstack11l1l1111l_opy_.items():
    for platform in bstack1l11llll1l_opy_:
      if isinstance(bstack11l111l111_opy_, list):
        for bstack111111l1l_opy_ in bstack11l111l111_opy_:
          if bstack111111l1l_opy_ in platform:
            platform[bstack111ll1l11_opy_] = platform[bstack111111l1l_opy_]
            del platform[bstack111111l1l_opy_]
            break
      elif bstack11l111l111_opy_ in platform:
        platform[bstack111ll1l11_opy_] = platform[bstack11l111l111_opy_]
        del platform[bstack11l111l111_opy_]
  for bstack11lll111ll_opy_ in bstack1ll1lll1ll_opy_:
    if bstack11lll111ll_opy_ in config:
      if not bstack1ll1lll1ll_opy_[bstack11lll111ll_opy_] in config:
        config[bstack1ll1lll1ll_opy_[bstack11lll111ll_opy_]] = {}
      config[bstack1ll1lll1ll_opy_[bstack11lll111ll_opy_]].update(config[bstack11lll111ll_opy_])
      del config[bstack11lll111ll_opy_]
  for platform in bstack1l11llll1l_opy_:
    for bstack11lll111ll_opy_ in bstack1ll1lll1ll_opy_:
      if bstack11lll111ll_opy_ in list(platform):
        if not bstack1ll1lll1ll_opy_[bstack11lll111ll_opy_] in platform:
          platform[bstack1ll1lll1ll_opy_[bstack11lll111ll_opy_]] = {}
        platform[bstack1ll1lll1ll_opy_[bstack11lll111ll_opy_]].update(platform[bstack11lll111ll_opy_])
        del platform[bstack11lll111ll_opy_]
  config = bstack1l1l1ll1l_opy_(config)
  return config
def bstack1l1l11ll_opy_(config):
  global bstack1l1111111l_opy_
  bstack1l111l1l_opy_ = False
  if bstack1l11ll1_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫࣸ") in config and str(config[bstack1l11ll1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࣹࠬ")]).lower() != bstack1l11ll1_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨࣺ"):
    if bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧࣻ") not in config or str(config[bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨࣼ")]).lower() == bstack1l11ll1_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫࣽ"):
      config[bstack1l11ll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬࣾ")] = False
    else:
      bstack11lll111l_opy_ = bstack11l111ll1_opy_()
      if bstack1l11ll1_opy_ (u"ࠧࡪࡵࡗࡶ࡮ࡧ࡬ࡈࡴ࡬ࡨࠬࣿ") in bstack11lll111l_opy_:
        if not bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬऀ") in config:
          config[bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ँ")] = {}
        config[bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧं")][bstack1l11ll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ः")] = bstack1l11ll1_opy_ (u"ࠬࡧࡴࡴ࠯ࡵࡩࡵ࡫ࡡࡵࡧࡵࠫऄ")
        bstack1l111l1l_opy_ = True
        bstack1l1111111l_opy_ = config[bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪअ")].get(bstack1l11ll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩआ"))
  if bstack1llll1llll_opy_(config) and bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬइ") in config and str(config[bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ई")]).lower() != bstack1l11ll1_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩउ") and not bstack1l111l1l_opy_:
    if not bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऊ") in config:
      config[bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩऋ")] = {}
    if not config[bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪऌ")].get(bstack1l11ll1_opy_ (u"ࠧࡴ࡭࡬ࡴࡇ࡯࡮ࡢࡴࡼࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡸࡧࡴࡪࡱࡱࠫऍ")) and not bstack1l11ll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪऎ") in config[bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ए")]:
      bstack1ll11l1ll1_opy_ = datetime.datetime.now()
      bstack11ll1l1l1_opy_ = bstack1ll11l1ll1_opy_.strftime(bstack1l11ll1_opy_ (u"ࠪࠩࡩࡥࠥࡣࡡࠨࡌࠪࡓࠧऐ"))
      hostname = socket.gethostname()
      bstack111l11lll_opy_ = bstack1l11ll1_opy_ (u"ࠫࠬऑ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1l11ll1_opy_ (u"ࠬࢁࡽࡠࡽࢀࡣࢀࢃࠧऒ").format(bstack11ll1l1l1_opy_, hostname, bstack111l11lll_opy_)
      config[bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪओ")][bstack1l11ll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऔ")] = identifier
    bstack1l1111111l_opy_ = config[bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬक")].get(bstack1l11ll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫख"))
  return config
def bstack1111l1l1_opy_():
  bstack111lll1ll1_opy_ =  bstack1lll11ll1l_opy_()[bstack1l11ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠩग")]
  return bstack111lll1ll1_opy_ if bstack111lll1ll1_opy_ else -1
def bstack1l1111111_opy_(bstack111lll1ll1_opy_):
  global CONFIG
  if not bstack1l11ll1_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭घ") in CONFIG[bstack1l11ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧङ")]:
    return
  CONFIG[bstack1l11ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨच")] = CONFIG[bstack1l11ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩछ")].replace(
    bstack1l11ll1_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪज"),
    str(bstack111lll1ll1_opy_)
  )
def bstack1l1l1ll11l_opy_():
  global CONFIG
  if not bstack1l11ll1_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨझ") in CONFIG[bstack1l11ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬञ")]:
    return
  bstack1ll11l1ll1_opy_ = datetime.datetime.now()
  bstack11ll1l1l1_opy_ = bstack1ll11l1ll1_opy_.strftime(bstack1l11ll1_opy_ (u"ࠫࠪࡪ࠭ࠦࡤ࠰ࠩࡍࡀࠥࡎࠩट"))
  CONFIG[bstack1l11ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧठ")] = CONFIG[bstack1l11ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨड")].replace(
    bstack1l11ll1_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭ढ"),
    bstack11ll1l1l1_opy_
  )
def bstack1ll1ll1l1_opy_():
  global CONFIG
  if bstack1l11ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪण") in CONFIG and not bool(CONFIG[bstack1l11ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫत")]):
    del CONFIG[bstack1l11ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬथ")]
    return
  if not bstack1l11ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭द") in CONFIG:
    CONFIG[bstack1l11ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧध")] = bstack1l11ll1_opy_ (u"࠭ࠣࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩन")
  if bstack1l11ll1_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭ऩ") in CONFIG[bstack1l11ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪप")]:
    bstack1l1l1ll11l_opy_()
    os.environ[bstack1l11ll1_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭फ")] = CONFIG[bstack1l11ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬब")]
  if not bstack1l11ll1_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭भ") in CONFIG[bstack1l11ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧम")]:
    return
  bstack111lll1ll1_opy_ = bstack1l11ll1_opy_ (u"࠭ࠧय")
  bstack1lll1ll1l_opy_ = bstack1111l1l1_opy_()
  if bstack1lll1ll1l_opy_ != -1:
    bstack111lll1ll1_opy_ = bstack1l11ll1_opy_ (u"ࠧࡄࡋࠣࠫर") + str(bstack1lll1ll1l_opy_)
  if bstack111lll1ll1_opy_ == bstack1l11ll1_opy_ (u"ࠨࠩऱ"):
    bstack1ll1l1lll_opy_ = bstack11l111111l_opy_(CONFIG[bstack1l11ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬल")])
    if bstack1ll1l1lll_opy_ != -1:
      bstack111lll1ll1_opy_ = str(bstack1ll1l1lll_opy_)
  if bstack111lll1ll1_opy_:
    bstack1l1111111_opy_(bstack111lll1ll1_opy_)
    os.environ[bstack1l11ll1_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧळ")] = CONFIG[bstack1l11ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ऴ")]
def bstack1l11111ll1_opy_(bstack1l11llll_opy_, bstack11l1ll1ll_opy_, path):
  bstack1lll111ll1_opy_ = {
    bstack1l11ll1_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩव"): bstack11l1ll1ll_opy_
  }
  if os.path.exists(path):
    bstack1l1l11ll11_opy_ = json.load(open(path, bstack1l11ll1_opy_ (u"࠭ࡲࡣࠩश")))
  else:
    bstack1l1l11ll11_opy_ = {}
  bstack1l1l11ll11_opy_[bstack1l11llll_opy_] = bstack1lll111ll1_opy_
  with open(path, bstack1l11ll1_opy_ (u"ࠢࡸ࠭ࠥष")) as outfile:
    json.dump(bstack1l1l11ll11_opy_, outfile)
def bstack11l111111l_opy_(bstack1l11llll_opy_):
  bstack1l11llll_opy_ = str(bstack1l11llll_opy_)
  bstack1ll11l111_opy_ = os.path.join(os.path.expanduser(bstack1l11ll1_opy_ (u"ࠨࢀࠪस")), bstack1l11ll1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩह"))
  try:
    if not os.path.exists(bstack1ll11l111_opy_):
      os.makedirs(bstack1ll11l111_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1l11ll1_opy_ (u"ࠪࢂࠬऺ")), bstack1l11ll1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫऻ"), bstack1l11ll1_opy_ (u"ࠬ࠴ࡢࡶ࡫࡯ࡨ࠲ࡴࡡ࡮ࡧ࠰ࡧࡦࡩࡨࡦ࠰࡭ࡷࡴࡴ़ࠧ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1l11ll1_opy_ (u"࠭ࡷࠨऽ")):
        pass
      with open(file_path, bstack1l11ll1_opy_ (u"ࠢࡸ࠭ࠥा")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1l11ll1_opy_ (u"ࠨࡴࠪि")) as bstack11111ll1l_opy_:
      bstack1llll11ll_opy_ = json.load(bstack11111ll1l_opy_)
    if bstack1l11llll_opy_ in bstack1llll11ll_opy_:
      bstack1l11ll11l1_opy_ = bstack1llll11ll_opy_[bstack1l11llll_opy_][bstack1l11ll1_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ी")]
      bstack111ll1ll1_opy_ = int(bstack1l11ll11l1_opy_) + 1
      bstack1l11111ll1_opy_(bstack1l11llll_opy_, bstack111ll1ll1_opy_, file_path)
      return bstack111ll1ll1_opy_
    else:
      bstack1l11111ll1_opy_(bstack1l11llll_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1l111l1l1l_opy_.format(str(e)))
    return -1
def bstack11l1l1l1l_opy_(config):
  if not config[bstack1l11ll1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬु")] or not config[bstack1l11ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧू")]:
    return True
  else:
    return False
def bstack1l1l11l11l_opy_(config, index=0):
  global bstack1lllll11l_opy_
  bstack11l111ll_opy_ = {}
  caps = bstack1ll11lll1_opy_ + bstack1ll11lllll_opy_
  if config.get(bstack1l11ll1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩृ"), False):
    bstack11l111ll_opy_[bstack1l11ll1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪॄ")] = True
    bstack11l111ll_opy_[bstack1l11ll1_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࡓࡵࡺࡩࡰࡰࡶࠫॅ")] = config.get(bstack1l11ll1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࡔࡶࡴࡪࡱࡱࡷࠬॆ"), {})
  if bstack1lllll11l_opy_:
    caps += bstack1l1lll1ll1_opy_
  for key in config:
    if key in caps + [bstack1l11ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬे")]:
      continue
    bstack11l111ll_opy_[key] = config[key]
  if bstack1l11ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ै") in config:
    for bstack11llllll1_opy_ in config[bstack1l11ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॉ")][index]:
      if bstack11llllll1_opy_ in caps:
        continue
      bstack11l111ll_opy_[bstack11llllll1_opy_] = config[bstack1l11ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨॊ")][index][bstack11llllll1_opy_]
  bstack11l111ll_opy_[bstack1l11ll1_opy_ (u"࠭ࡨࡰࡵࡷࡒࡦࡳࡥࠨो")] = socket.gethostname()
  if bstack1l11ll1_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨौ") in bstack11l111ll_opy_:
    del (bstack11l111ll_opy_[bstack1l11ll1_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯्ࠩ")])
  return bstack11l111ll_opy_
def bstack1ll1l1l11l_opy_(config):
  global bstack1lllll11l_opy_
  bstack1ll1l1l1l1_opy_ = {}
  caps = bstack1ll11lllll_opy_
  if bstack1lllll11l_opy_:
    caps += bstack1l1lll1ll1_opy_
  for key in caps:
    if key in config:
      bstack1ll1l1l1l1_opy_[key] = config[key]
  return bstack1ll1l1l1l1_opy_
def bstack1ll11111_opy_(bstack11l111ll_opy_, bstack1ll1l1l1l1_opy_):
  bstack11l11ll11l_opy_ = {}
  for key in bstack11l111ll_opy_.keys():
    if key in bstack1ll1ll111_opy_:
      bstack11l11ll11l_opy_[bstack1ll1ll111_opy_[key]] = bstack11l111ll_opy_[key]
    else:
      bstack11l11ll11l_opy_[key] = bstack11l111ll_opy_[key]
  for key in bstack1ll1l1l1l1_opy_:
    if key in bstack1ll1ll111_opy_:
      bstack11l11ll11l_opy_[bstack1ll1ll111_opy_[key]] = bstack1ll1l1l1l1_opy_[key]
    else:
      bstack11l11ll11l_opy_[key] = bstack1ll1l1l1l1_opy_[key]
  return bstack11l11ll11l_opy_
def bstack11l1111ll1_opy_(config, index=0):
  global bstack1lllll11l_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack1l11l1ll11_opy_ = bstack11l1llll_opy_(bstack1lll11l11l_opy_, config, logger)
  bstack1ll1l1l1l1_opy_ = bstack1ll1l1l11l_opy_(config)
  bstack1l11l11ll1_opy_ = bstack1ll11lllll_opy_
  bstack1l11l11ll1_opy_ += bstack1ll1l11lll_opy_
  bstack1ll1l1l1l1_opy_ = update(bstack1ll1l1l1l1_opy_, bstack1l11l1ll11_opy_)
  if bstack1lllll11l_opy_:
    bstack1l11l11ll1_opy_ += bstack1l1lll1ll1_opy_
  if bstack1l11ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॎ") in config:
    if bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨॏ") in config[bstack1l11ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॐ")][index]:
      caps[bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ॑")] = config[bstack1l11ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴ॒ࠩ")][index][bstack1l11ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ॓")]
    if bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ॔") in config[bstack1l11ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॕ")][index]:
      caps[bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫॖ")] = str(config[bstack1l11ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॗ")][index][bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭क़")])
    bstack1111l111l_opy_ = bstack11l1llll_opy_(bstack1lll11l11l_opy_, config[bstack1l11ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩख़")][index], logger)
    bstack1l11l11ll1_opy_ += list(bstack1111l111l_opy_.keys())
    for bstack1l111l11l_opy_ in bstack1l11l11ll1_opy_:
      if bstack1l111l11l_opy_ in config[bstack1l11ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪग़")][index]:
        if bstack1l111l11l_opy_ == bstack1l11ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪज़"):
          try:
            bstack1111l111l_opy_[bstack1l111l11l_opy_] = str(config[bstack1l11ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬड़")][index][bstack1l111l11l_opy_] * 1.0)
          except:
            bstack1111l111l_opy_[bstack1l111l11l_opy_] = str(config[bstack1l11ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ढ़")][index][bstack1l111l11l_opy_])
        else:
          bstack1111l111l_opy_[bstack1l111l11l_opy_] = config[bstack1l11ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧफ़")][index][bstack1l111l11l_opy_]
        del (config[bstack1l11ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨय़")][index][bstack1l111l11l_opy_])
    bstack1ll1l1l1l1_opy_ = update(bstack1ll1l1l1l1_opy_, bstack1111l111l_opy_)
  bstack11l111ll_opy_ = bstack1l1l11l11l_opy_(config, index)
  for bstack111111l1l_opy_ in bstack1ll11lllll_opy_ + list(bstack1l11l1ll11_opy_.keys()):
    if bstack111111l1l_opy_ in bstack11l111ll_opy_:
      bstack1ll1l1l1l1_opy_[bstack111111l1l_opy_] = bstack11l111ll_opy_[bstack111111l1l_opy_]
      del (bstack11l111ll_opy_[bstack111111l1l_opy_])
  if bstack11lll11111_opy_(config):
    bstack11l111ll_opy_[bstack1l11ll1_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ॠ")] = True
    caps.update(bstack1ll1l1l1l1_opy_)
    caps[bstack1l11ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨॡ")] = bstack11l111ll_opy_
  else:
    bstack11l111ll_opy_[bstack1l11ll1_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨॢ")] = False
    caps.update(bstack1ll11111_opy_(bstack11l111ll_opy_, bstack1ll1l1l1l1_opy_))
    if bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧॣ") in caps:
      caps[bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫ।")] = caps[bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ॥")]
      del (caps[bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ०")])
    if bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ१") in caps:
      caps[bstack1l11ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ२")] = caps[bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ३")]
      del (caps[bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ४")])
  return caps
def bstack111111111_opy_():
  global bstack11lll1ll11_opy_
  global CONFIG
  if bstack11llll11ll_opy_() <= version.parse(bstack1l11ll1_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪ५")):
    if bstack11lll1ll11_opy_ != bstack1l11ll1_opy_ (u"ࠫࠬ६"):
      return bstack1l11ll1_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨ७") + bstack11lll1ll11_opy_ + bstack1l11ll1_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥ८")
    return bstack1ll11lll1l_opy_
  if bstack11lll1ll11_opy_ != bstack1l11ll1_opy_ (u"ࠧࠨ९"):
    return bstack1l11ll1_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥ॰") + bstack11lll1ll11_opy_ + bstack1l11ll1_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥॱ")
  return bstack11111l1l_opy_
def bstack11ll1l111l_opy_(options):
  return hasattr(options, bstack1l11ll1_opy_ (u"ࠪࡷࡪࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠫॲ"))
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
def bstack1l111l11ll_opy_(options, bstack1l1l1lll1_opy_):
  for bstack1ll1ll11ll_opy_ in bstack1l1l1lll1_opy_:
    if bstack1ll1ll11ll_opy_ in [bstack1l11ll1_opy_ (u"ࠫࡦࡸࡧࡴࠩॳ"), bstack1l11ll1_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩॴ")]:
      continue
    if bstack1ll1ll11ll_opy_ in options._experimental_options:
      options._experimental_options[bstack1ll1ll11ll_opy_] = update(options._experimental_options[bstack1ll1ll11ll_opy_],
                                                         bstack1l1l1lll1_opy_[bstack1ll1ll11ll_opy_])
    else:
      options.add_experimental_option(bstack1ll1ll11ll_opy_, bstack1l1l1lll1_opy_[bstack1ll1ll11ll_opy_])
  if bstack1l11ll1_opy_ (u"࠭ࡡࡳࡩࡶࠫॵ") in bstack1l1l1lll1_opy_:
    for arg in bstack1l1l1lll1_opy_[bstack1l11ll1_opy_ (u"ࠧࡢࡴࡪࡷࠬॶ")]:
      options.add_argument(arg)
    del (bstack1l1l1lll1_opy_[bstack1l11ll1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ॷ")])
  if bstack1l11ll1_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ॸ") in bstack1l1l1lll1_opy_:
    for ext in bstack1l1l1lll1_opy_[bstack1l11ll1_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧॹ")]:
      try:
        options.add_extension(ext)
      except OSError:
        options.add_encoded_extension(ext)
    del (bstack1l1l1lll1_opy_[bstack1l11ll1_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨॺ")])
def bstack11l1lll1l1_opy_(options, bstack1llll1ll1l_opy_):
  if bstack1l11ll1_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫॻ") in bstack1llll1ll1l_opy_:
    for bstack1111ll1l1_opy_ in bstack1llll1ll1l_opy_[bstack1l11ll1_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬॼ")]:
      if bstack1111ll1l1_opy_ in options._preferences:
        options._preferences[bstack1111ll1l1_opy_] = update(options._preferences[bstack1111ll1l1_opy_], bstack1llll1ll1l_opy_[bstack1l11ll1_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ॽ")][bstack1111ll1l1_opy_])
      else:
        options.set_preference(bstack1111ll1l1_opy_, bstack1llll1ll1l_opy_[bstack1l11ll1_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧॾ")][bstack1111ll1l1_opy_])
  if bstack1l11ll1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॿ") in bstack1llll1ll1l_opy_:
    for arg in bstack1llll1ll1l_opy_[bstack1l11ll1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨঀ")]:
      options.add_argument(arg)
def bstack11lllll1ll_opy_(options, bstack11l11l1l1_opy_):
  if bstack1l11ll1_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࠬঁ") in bstack11l11l1l1_opy_:
    options.use_webview(bool(bstack11l11l1l1_opy_[bstack1l11ll1_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼ࠭ং")]))
  bstack1l111l11ll_opy_(options, bstack11l11l1l1_opy_)
def bstack1ll1ll1l1l_opy_(options, bstack1ll11ll1ll_opy_):
  for bstack11l1ll11l_opy_ in bstack1ll11ll1ll_opy_:
    if bstack11l1ll11l_opy_ in [bstack1l11ll1_opy_ (u"࠭ࡴࡦࡥ࡫ࡲࡴࡲ࡯ࡨࡻࡓࡶࡪࡼࡩࡦࡹࠪঃ"), bstack1l11ll1_opy_ (u"ࠧࡢࡴࡪࡷࠬ঄")]:
      continue
    options.set_capability(bstack11l1ll11l_opy_, bstack1ll11ll1ll_opy_[bstack11l1ll11l_opy_])
  if bstack1l11ll1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭অ") in bstack1ll11ll1ll_opy_:
    for arg in bstack1ll11ll1ll_opy_[bstack1l11ll1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧআ")]:
      options.add_argument(arg)
  if bstack1l11ll1_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧই") in bstack1ll11ll1ll_opy_:
    options.bstack1l1lll111l_opy_(bool(bstack1ll11ll1ll_opy_[bstack1l11ll1_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨঈ")]))
def bstack1lll1111ll_opy_(options, bstack11lll11l1_opy_):
  for bstack11l11llll_opy_ in bstack11lll11l1_opy_:
    if bstack11l11llll_opy_ in [bstack1l11ll1_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩউ"), bstack1l11ll1_opy_ (u"࠭ࡡࡳࡩࡶࠫঊ")]:
      continue
    options._options[bstack11l11llll_opy_] = bstack11lll11l1_opy_[bstack11l11llll_opy_]
  if bstack1l11ll1_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫঋ") in bstack11lll11l1_opy_:
    for bstack1ll1111lll_opy_ in bstack11lll11l1_opy_[bstack1l11ll1_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬঌ")]:
      options.bstack11llll1lll_opy_(
        bstack1ll1111lll_opy_, bstack11lll11l1_opy_[bstack1l11ll1_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭঍")][bstack1ll1111lll_opy_])
  if bstack1l11ll1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ঎") in bstack11lll11l1_opy_:
    for arg in bstack11lll11l1_opy_[bstack1l11ll1_opy_ (u"ࠫࡦࡸࡧࡴࠩএ")]:
      options.add_argument(arg)
def bstack11l11l11l_opy_(options, caps):
  if not hasattr(options, bstack1l11ll1_opy_ (u"ࠬࡑࡅ࡚ࠩঐ")):
    return
  if options.KEY == bstack1l11ll1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ঑"):
    options = bstack11lll1ll1l_opy_.bstack1111111ll_opy_(bstack1l1l111l_opy_=options, config=CONFIG)
  if options.KEY == bstack1l11ll1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ঒") and options.KEY in caps:
    bstack1l111l11ll_opy_(options, caps[bstack1l11ll1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ও")])
  elif options.KEY == bstack1l11ll1_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧঔ") and options.KEY in caps:
    bstack11l1lll1l1_opy_(options, caps[bstack1l11ll1_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨক")])
  elif options.KEY == bstack1l11ll1_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬখ") and options.KEY in caps:
    bstack1ll1ll1l1l_opy_(options, caps[bstack1l11ll1_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭গ")])
  elif options.KEY == bstack1l11ll1_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧঘ") and options.KEY in caps:
    bstack11lllll1ll_opy_(options, caps[bstack1l11ll1_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨঙ")])
  elif options.KEY == bstack1l11ll1_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧচ") and options.KEY in caps:
    bstack1lll1111ll_opy_(options, caps[bstack1l11ll1_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨছ")])
def bstack11111l111_opy_(caps):
  global bstack1lllll11l_opy_
  if isinstance(os.environ.get(bstack1l11ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫজ")), str):
    bstack1lllll11l_opy_ = eval(os.getenv(bstack1l11ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬঝ")))
  if bstack1lllll11l_opy_:
    if bstack1l1lll1l_opy_() < version.parse(bstack1l11ll1_opy_ (u"ࠬ࠸࠮࠴࠰࠳ࠫঞ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1l11ll1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ট")
    if bstack1l11ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬঠ") in caps:
      browser = caps[bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ড")]
    elif bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪঢ") in caps:
      browser = caps[bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫণ")]
    browser = str(browser).lower()
    if browser == bstack1l11ll1_opy_ (u"ࠫ࡮ࡶࡨࡰࡰࡨࠫত") or browser == bstack1l11ll1_opy_ (u"ࠬ࡯ࡰࡢࡦࠪথ"):
      browser = bstack1l11ll1_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭দ")
    if browser == bstack1l11ll1_opy_ (u"ࠧࡴࡣࡰࡷࡺࡴࡧࠨধ"):
      browser = bstack1l11ll1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨন")
    if browser not in [bstack1l11ll1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩ঩"), bstack1l11ll1_opy_ (u"ࠪࡩࡩ࡭ࡥࠨপ"), bstack1l11ll1_opy_ (u"ࠫ࡮࡫ࠧফ"), bstack1l11ll1_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬব"), bstack1l11ll1_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧভ")]:
      return None
    try:
      package = bstack1l11ll1_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࠰ࡺࡩࡧࡪࡲࡪࡸࡨࡶ࠳ࢁࡽ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩম").format(browser)
      name = bstack1l11ll1_opy_ (u"ࠨࡑࡳࡸ࡮ࡵ࡮ࡴࠩয")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack11ll1l111l_opy_(options):
        return None
      for bstack111111l1l_opy_ in caps.keys():
        options.set_capability(bstack111111l1l_opy_, caps[bstack111111l1l_opy_])
      bstack11l11l11l_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1l111lll11_opy_(options, bstack1l1lll1l11_opy_):
  if not bstack11ll1l111l_opy_(options):
    return
  for bstack111111l1l_opy_ in bstack1l1lll1l11_opy_.keys():
    if bstack111111l1l_opy_ in bstack1ll1l11lll_opy_:
      continue
    if bstack111111l1l_opy_ in options._caps and type(options._caps[bstack111111l1l_opy_]) in [dict, list]:
      options._caps[bstack111111l1l_opy_] = update(options._caps[bstack111111l1l_opy_], bstack1l1lll1l11_opy_[bstack111111l1l_opy_])
    else:
      options.set_capability(bstack111111l1l_opy_, bstack1l1lll1l11_opy_[bstack111111l1l_opy_])
  bstack11l11l11l_opy_(options, bstack1l1lll1l11_opy_)
  if bstack1l11ll1_opy_ (u"ࠩࡰࡳࡿࡀࡤࡦࡤࡸ࡫࡬࡫ࡲࡂࡦࡧࡶࡪࡹࡳࠨর") in options._caps:
    if options._caps[bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ঱")] and options._caps[bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩল")].lower() != bstack1l11ll1_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭঳"):
      del options._caps[bstack1l11ll1_opy_ (u"࠭࡭ࡰࡼ࠽ࡨࡪࡨࡵࡨࡩࡨࡶࡆࡪࡤࡳࡧࡶࡷࠬ঴")]
def bstack11lll1l11l_opy_(proxy_config):
  if bstack1l11ll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ঵") in proxy_config:
    proxy_config[bstack1l11ll1_opy_ (u"ࠨࡵࡶࡰࡕࡸ࡯ࡹࡻࠪশ")] = proxy_config[bstack1l11ll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ষ")]
    del (proxy_config[bstack1l11ll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧস")])
  if bstack1l11ll1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧহ") in proxy_config and proxy_config[bstack1l11ll1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ঺")].lower() != bstack1l11ll1_opy_ (u"࠭ࡤࡪࡴࡨࡧࡹ࠭঻"):
    proxy_config[bstack1l11ll1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧ়ࠪ")] = bstack1l11ll1_opy_ (u"ࠨ࡯ࡤࡲࡺࡧ࡬ࠨঽ")
  if bstack1l11ll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡂࡷࡷࡳࡨࡵ࡮ࡧ࡫ࡪ࡙ࡷࡲࠧা") in proxy_config:
    proxy_config[bstack1l11ll1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭ি")] = bstack1l11ll1_opy_ (u"ࠫࡵࡧࡣࠨী")
  return proxy_config
def bstack111llll1l_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1l11ll1_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫু") in config:
    return proxy
  config[bstack1l11ll1_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬূ")] = bstack11lll1l11l_opy_(config[bstack1l11ll1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭ৃ")])
  if proxy == None:
    proxy = Proxy(config[bstack1l11ll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧৄ")])
  return proxy
def bstack1lllll1ll_opy_(self):
  global CONFIG
  global bstack11ll11l1l_opy_
  try:
    proxy = bstack111l1l1l_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1l11ll1_opy_ (u"ࠩ࠱ࡴࡦࡩࠧ৅")):
        proxies = bstack111lll1lll_opy_(proxy, bstack111111111_opy_())
        if len(proxies) > 0:
          protocol, bstack1ll11llll1_opy_ = proxies.popitem()
          if bstack1l11ll1_opy_ (u"ࠥ࠾࠴࠵ࠢ৆") in bstack1ll11llll1_opy_:
            return bstack1ll11llll1_opy_
          else:
            return bstack1l11ll1_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧে") + bstack1ll11llll1_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1l11ll1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡲࡵࡳࡽࡿࠠࡶࡴ࡯ࠤ࠿ࠦࡻࡾࠤৈ").format(str(e)))
  return bstack11ll11l1l_opy_(self)
def bstack1llllll111_opy_():
  global CONFIG
  return bstack1l111ll11_opy_(CONFIG) and bstack1l11l1l1ll_opy_() and bstack11llll11ll_opy_() >= version.parse(bstack1ll1l11l1_opy_)
def bstack11l1l1ll1_opy_():
  global CONFIG
  return (bstack1l11ll1_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ৉") in CONFIG or bstack1l11ll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ৊") in CONFIG) and bstack1ll1l1ll1l_opy_()
def bstack1ll1lllll_opy_(config):
  bstack11lll1l1_opy_ = {}
  if bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬো") in config:
    bstack11lll1l1_opy_ = config[bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ৌ")]
  if bstack1l11ll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴ্ࠩ") in config:
    bstack11lll1l1_opy_ = config[bstack1l11ll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪৎ")]
  proxy = bstack111l1l1l_opy_(config)
  if proxy:
    if proxy.endswith(bstack1l11ll1_opy_ (u"ࠬ࠴ࡰࡢࡥࠪ৏")) and os.path.isfile(proxy):
      bstack11lll1l1_opy_[bstack1l11ll1_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩ৐")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1l11ll1_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ৑")):
        proxies = bstack11llllll11_opy_(config, bstack111111111_opy_())
        if len(proxies) > 0:
          protocol, bstack1ll11llll1_opy_ = proxies.popitem()
          if bstack1l11ll1_opy_ (u"ࠣ࠼࠲࠳ࠧ৒") in bstack1ll11llll1_opy_:
            parsed_url = urlparse(bstack1ll11llll1_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1l11ll1_opy_ (u"ࠤ࠽࠳࠴ࠨ৓") + bstack1ll11llll1_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack11lll1l1_opy_[bstack1l11ll1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ࠭৔")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack11lll1l1_opy_[bstack1l11ll1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡳࡷࡺࠧ৕")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack11lll1l1_opy_[bstack1l11ll1_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨ৖")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack11lll1l1_opy_[bstack1l11ll1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡧࡳࡴࠩৗ")] = str(parsed_url.password)
  return bstack11lll1l1_opy_
def bstack1ll11ll1l1_opy_(config):
  if bstack1l11ll1_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬ৘") in config:
    return config[bstack1l11ll1_opy_ (u"ࠨࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸ࠭৙")]
  return {}
def bstack1l1l11lll_opy_(caps):
  global bstack1l1111111l_opy_
  if bstack1l11ll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ৚") in caps:
    caps[bstack1l11ll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ৛")][bstack1l11ll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࠪড়")] = True
    if bstack1l1111111l_opy_:
      caps[bstack1l11ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ঢ়")][bstack1l11ll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ৞")] = bstack1l1111111l_opy_
  else:
    caps[bstack1l11ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࠬয়")] = True
    if bstack1l1111111l_opy_:
      caps[bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩৠ")] = bstack1l1111111l_opy_
@measure(event_name=EVENTS.bstack1l11l111l1_opy_, stage=STAGE.bstack11lllll111_opy_, bstack1l11111l1_opy_=bstack1l11111l1l_opy_)
def bstack111111lll_opy_():
  global CONFIG
  if not bstack1llll1llll_opy_(CONFIG) or cli.is_enabled(CONFIG):
    return
  if bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ৡ") in CONFIG and bstack11l1ll11l1_opy_(CONFIG[bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧৢ")]):
    if (
      bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨৣ") in CONFIG
      and bstack11l1ll11l1_opy_(CONFIG[bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ৤")].get(bstack1l11ll1_opy_ (u"࠭ࡳ࡬࡫ࡳࡆ࡮ࡴࡡࡳࡻࡌࡲ࡮ࡺࡩࡢ࡮࡬ࡷࡦࡺࡩࡰࡰࠪ৥")))
    ):
      logger.debug(bstack1l11ll1_opy_ (u"ࠢࡍࡱࡦࡥࡱࠦࡢࡪࡰࡤࡶࡾࠦ࡮ࡰࡶࠣࡷࡹࡧࡲࡵࡧࡧࠤࡦࡹࠠࡴ࡭࡬ࡴࡇ࡯࡮ࡢࡴࡼࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡸࡧࡴࡪࡱࡱࠤ࡮ࡹࠠࡦࡰࡤࡦࡱ࡫ࡤࠣ০"))
      return
    bstack11lll1l1_opy_ = bstack1ll1lllll_opy_(CONFIG)
    bstack1lll1l111l_opy_(CONFIG[bstack1l11ll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ১")], bstack11lll1l1_opy_)
def bstack1lll1l111l_opy_(key, bstack11lll1l1_opy_):
  global bstack11ll11l1_opy_
  logger.info(bstack1l11lll1ll_opy_)
  try:
    bstack11ll11l1_opy_ = Local()
    bstack111ll1l1_opy_ = {bstack1l11ll1_opy_ (u"ࠩ࡮ࡩࡾ࠭২"): key}
    bstack111ll1l1_opy_.update(bstack11lll1l1_opy_)
    logger.debug(bstack1l1l1ll1ll_opy_.format(str(bstack111ll1l1_opy_)).replace(key, bstack1l11ll1_opy_ (u"ࠪ࡟ࡗࡋࡄࡂࡅࡗࡉࡉࡣࠧ৩")))
    bstack11ll11l1_opy_.start(**bstack111ll1l1_opy_)
    if bstack11ll11l1_opy_.isRunning():
      logger.info(bstack11l1llllll_opy_)
  except Exception as e:
    bstack1ll1l1l11_opy_(bstack1l1111lll1_opy_.format(str(e)))
def bstack1l11llll1_opy_():
  global bstack11ll11l1_opy_
  if bstack11ll11l1_opy_.isRunning():
    logger.info(bstack11l11lll_opy_)
    bstack11ll11l1_opy_.stop()
  bstack11ll11l1_opy_ = None
def bstack1lll1lll11_opy_(bstack11l1ll11ll_opy_=[]):
  global CONFIG
  bstack1lllll1l1l_opy_ = []
  bstack1l11l1llll_opy_ = [bstack1l11ll1_opy_ (u"ࠫࡴࡹࠧ৪"), bstack1l11ll1_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨ৫"), bstack1l11ll1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪ৬"), bstack1l11ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ৭"), bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭৮"), bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ৯")]
  try:
    for err in bstack11l1ll11ll_opy_:
      bstack1ll111l1l_opy_ = {}
      for k in bstack1l11l1llll_opy_:
        val = CONFIG[bstack1l11ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ৰ")][int(err[bstack1l11ll1_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪৱ")])].get(k)
        if val:
          bstack1ll111l1l_opy_[k] = val
      if(err[bstack1l11ll1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ৲")] != bstack1l11ll1_opy_ (u"࠭ࠧ৳")):
        bstack1ll111l1l_opy_[bstack1l11ll1_opy_ (u"ࠧࡵࡧࡶࡸࡸ࠭৴")] = {
          err[bstack1l11ll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭৵")]: err[bstack1l11ll1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ৶")]
        }
        bstack1lllll1l1l_opy_.append(bstack1ll111l1l_opy_)
  except Exception as e:
    logger.debug(bstack1l11ll1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡬࡯ࡳ࡯ࡤࡸࡹ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶ࠽ࠤࠬ৷") + str(e))
  finally:
    return bstack1lllll1l1l_opy_
def bstack11l1ll1111_opy_(file_name):
  bstack11ll1ll1_opy_ = []
  try:
    bstack111ll111l_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack111ll111l_opy_):
      with open(bstack111ll111l_opy_) as f:
        bstack1l11l1l111_opy_ = json.load(f)
        bstack11ll1ll1_opy_ = bstack1l11l1l111_opy_
      os.remove(bstack111ll111l_opy_)
    return bstack11ll1ll1_opy_
  except Exception as e:
    logger.debug(bstack1l11ll1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡪࡰࡧ࡭ࡳ࡭ࠠࡦࡴࡵࡳࡷࠦ࡬ࡪࡵࡷ࠾ࠥ࠭৸") + str(e))
    return bstack11ll1ll1_opy_
def bstack1llll1lll1_opy_():
  try:
      from bstack_utils.constants import bstack1lll11lll1_opy_, EVENTS
      from bstack_utils.helper import bstack1l1ll1ll1l_opy_, get_host_info, bstack111lllll11_opy_
      from datetime import datetime
      from filelock import FileLock
      bstack1l11l1l11_opy_ = os.path.join(os.getcwd(), bstack1l11ll1_opy_ (u"ࠬࡲ࡯ࡨࠩ৹"), bstack1l11ll1_opy_ (u"࠭࡫ࡦࡻ࠰ࡱࡪࡺࡲࡪࡥࡶ࠲࡯ࡹ࡯࡯ࠩ৺"))
      lock = FileLock(bstack1l11l1l11_opy_+bstack1l11ll1_opy_ (u"ࠢ࠯࡮ࡲࡧࡰࠨ৻"))
      def bstack1l111ll1l1_opy_():
          try:
              with lock:
                  with open(bstack1l11l1l11_opy_, bstack1l11ll1_opy_ (u"ࠣࡴࠥৼ"), encoding=bstack1l11ll1_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣ৽")) as file:
                      data = json.load(file)
                      config = {
                          bstack1l11ll1_opy_ (u"ࠥ࡬ࡪࡧࡤࡦࡴࡶࠦ৾"): {
                              bstack1l11ll1_opy_ (u"ࠦࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠥ৿"): bstack1l11ll1_opy_ (u"ࠧࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠣ਀"),
                          }
                      }
                      bstack11l111lll1_opy_ = datetime.utcnow()
                      bstack1ll11l1ll1_opy_ = bstack11l111lll1_opy_.strftime(bstack1l11ll1_opy_ (u"ࠨ࡚ࠥ࠯ࠨࡱ࠲ࠫࡤࡕࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࠱ࠩ࡫ࠦࡕࡕࡅࠥਁ"))
                      bstack111lllll1_opy_ = os.environ.get(bstack1l11ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬਂ")) if os.environ.get(bstack1l11ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ਃ")) else bstack111lllll11_opy_.get_property(bstack1l11ll1_opy_ (u"ࠤࡶࡨࡰࡘࡵ࡯ࡋࡧࠦ਄"))
                      payload = {
                          bstack1l11ll1_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠢਅ"): bstack1l11ll1_opy_ (u"ࠦࡸࡪ࡫ࡠࡧࡹࡩࡳࡺࡳࠣਆ"),
                          bstack1l11ll1_opy_ (u"ࠧࡪࡡࡵࡣࠥਇ"): {
                              bstack1l11ll1_opy_ (u"ࠨࡴࡦࡵࡷ࡬ࡺࡨ࡟ࡶࡷ࡬ࡨࠧਈ"): bstack111lllll1_opy_,
                              bstack1l11ll1_opy_ (u"ࠢࡤࡴࡨࡥࡹ࡫ࡤࡠࡦࡤࡽࠧਉ"): bstack1ll11l1ll1_opy_,
                              bstack1l11ll1_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟࡯ࡣࡰࡩࠧਊ"): bstack1l11ll1_opy_ (u"ࠤࡖࡈࡐࡌࡥࡢࡶࡸࡶࡪࡖࡥࡳࡨࡲࡶࡲࡧ࡮ࡤࡧࠥ਋"),
                              bstack1l11ll1_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡ࡭ࡷࡴࡴࠢ਌"): {
                                  bstack1l11ll1_opy_ (u"ࠦࡲ࡫ࡡࡴࡷࡵࡩࡸࠨ਍"): data,
                                  bstack1l11ll1_opy_ (u"ࠧࡹࡤ࡬ࡔࡸࡲࡎࡪࠢ਎"): bstack111lllll11_opy_.get_property(bstack1l11ll1_opy_ (u"ࠨࡳࡥ࡭ࡕࡹࡳࡏࡤࠣਏ"))
                              },
                              bstack1l11ll1_opy_ (u"ࠢࡶࡵࡨࡶࡤࡪࡡࡵࡣࠥਐ"): bstack111lllll11_opy_.get_property(bstack1l11ll1_opy_ (u"ࠣࡷࡶࡩࡷࡔࡡ࡮ࡧࠥ਑")),
                              bstack1l11ll1_opy_ (u"ࠤ࡫ࡳࡸࡺ࡟ࡪࡰࡩࡳࠧ਒"): get_host_info()
                          }
                      }
                      bstack1l11llllll_opy_ = bstack1ll1111l1l_opy_(cli.config, [bstack1l11ll1_opy_ (u"ࠥࡥࡵ࡯ࡳࠣਓ"), bstack1l11ll1_opy_ (u"ࠦࡪࡪࡳࡊࡰࡶࡸࡷࡻ࡭ࡦࡰࡷࡥࡹ࡯࡯࡯ࠤਔ"), bstack1l11ll1_opy_ (u"ࠧࡧࡰࡪࠤਕ")], bstack1lll11lll1_opy_)
                      response = bstack1l1ll1ll1l_opy_(bstack1l11ll1_opy_ (u"ࠨࡐࡐࡕࡗࠦਖ"), bstack1l11llllll_opy_, payload, config)
                      if(response.status_code >= 200 and response.status_code < 300):
                          logger.debug(bstack1l11ll1_opy_ (u"ࠢࡅࡣࡷࡥࠥࡹࡥ࡯ࡶࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺࠢࡷࡳࠥࢁࡽࠡࡹ࡬ࡸ࡭ࠦࡤࡢࡶࡤࠤࢀࢃࠢਗ").format(bstack1lll11lll1_opy_, payload))
                      else:
                          logger.debug(bstack1l11ll1_opy_ (u"ࠣࡔࡨࡵࡺ࡫ࡳࡵࠢࡩࡥ࡮ࡲࡥࡥࠢࡩࡳࡷࠦࡻࡾࠢࡺ࡭ࡹ࡮ࠠࡥࡣࡷࡥࠥࢁࡽࠣਘ").format(bstack1lll11lll1_opy_, payload))
          except Exception as e:
              logger.debug(bstack1l11ll1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥ࡯ࡦࠣ࡯ࡪࡿࠠ࡮ࡧࡷࡶ࡮ࡩࡳࠡࡦࡤࡸࡦࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴࠣࡿࢂࠨਙ").format(e))
      bstack1l111ll1l1_opy_()
      bstack1l111l1ll_opy_(bstack1l11l1l11_opy_, logger)
  except:
    pass
def bstack1l11l1ll_opy_():
  global bstack1lll1l1ll_opy_
  global bstack11l11lll1l_opy_
  global bstack1lll11llll_opy_
  global bstack11l1111l_opy_
  global bstack1lll1lll1l_opy_
  global bstack1ll1l11l1l_opy_
  global CONFIG
  bstack11ll111ll_opy_ = os.environ.get(bstack1l11ll1_opy_ (u"ࠪࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡕࡔࡇࡇࠫਚ"))
  if bstack11ll111ll_opy_ in [bstack1l11ll1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪਛ"), bstack1l11ll1_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫਜ")]:
    bstack1l1ll11ll1_opy_()
  percy.shutdown()
  if bstack1lll1l1ll_opy_:
    logger.warning(bstack1l1ll1l111_opy_.format(str(bstack1lll1l1ll_opy_)))
  else:
    try:
      bstack1l1l11ll11_opy_ = bstack1l1ll1111l_opy_(bstack1l11ll1_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬਝ"), logger)
      if bstack1l1l11ll11_opy_.get(bstack1l11ll1_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬਞ")) and bstack1l1l11ll11_opy_.get(bstack1l11ll1_opy_ (u"ࠨࡰࡸࡨ࡬࡫࡟࡭ࡱࡦࡥࡱ࠭ਟ")).get(bstack1l11ll1_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫਠ")):
        logger.warning(bstack1l1ll1l111_opy_.format(str(bstack1l1l11ll11_opy_[bstack1l11ll1_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨਡ")][bstack1l11ll1_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ਢ")])))
    except Exception as e:
      logger.error(e)
  if cli.is_running():
    bstack1l1111l1_opy_.invoke(bstack1l11lll111_opy_.bstack1l1111ll_opy_)
  logger.info(bstack1l1l1111l1_opy_)
  global bstack11ll11l1_opy_
  if bstack11ll11l1_opy_:
    bstack1l11llll1_opy_()
  try:
    with bstack111ll111_opy_:
      bstack1lll1l1lll_opy_ = bstack11l11lll1l_opy_.copy()
    for driver in bstack1lll1l1lll_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1111llll1_opy_)
  if bstack1ll1l11l1l_opy_ == bstack1l11ll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫਣ"):
    bstack1lll1lll1l_opy_ = bstack11l1ll1111_opy_(bstack1l11ll1_opy_ (u"࠭ࡲࡰࡤࡲࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧਤ"))
  if bstack1ll1l11l1l_opy_ == bstack1l11ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧਥ") and len(bstack11l1111l_opy_) == 0:
    bstack11l1111l_opy_ = bstack11l1ll1111_opy_(bstack1l11ll1_opy_ (u"ࠨࡲࡺࡣࡵࡿࡴࡦࡵࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ਦ"))
    if len(bstack11l1111l_opy_) == 0:
      bstack11l1111l_opy_ = bstack11l1ll1111_opy_(bstack1l11ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡳࡴࡵࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨਧ"))
  bstack1ll11l11l1_opy_ = bstack1l11ll1_opy_ (u"ࠪࠫਨ")
  if len(bstack1lll11llll_opy_) > 0:
    bstack1ll11l11l1_opy_ = bstack1lll1lll11_opy_(bstack1lll11llll_opy_)
  elif len(bstack11l1111l_opy_) > 0:
    bstack1ll11l11l1_opy_ = bstack1lll1lll11_opy_(bstack11l1111l_opy_)
  elif len(bstack1lll1lll1l_opy_) > 0:
    bstack1ll11l11l1_opy_ = bstack1lll1lll11_opy_(bstack1lll1lll1l_opy_)
  elif len(bstack1l1lll1l1l_opy_) > 0:
    bstack1ll11l11l1_opy_ = bstack1lll1lll11_opy_(bstack1l1lll1l1l_opy_)
  if bool(bstack1ll11l11l1_opy_):
    bstack1lllll111l_opy_(bstack1ll11l11l1_opy_)
  else:
    bstack1lllll111l_opy_()
  bstack1l111l1ll_opy_(bstack1l1ll1l1_opy_, logger)
  if bstack11ll111ll_opy_ not in [bstack1l11ll1_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ਩")]:
    bstack1llll1lll1_opy_()
  bstack1lll1l1l1l_opy_.bstack1l1lll1l1_opy_(CONFIG)
  if len(bstack1lll1lll1l_opy_) > 0:
    sys.exit(len(bstack1lll1lll1l_opy_))
def bstack1l11l1l1_opy_(bstack11lll11lll_opy_, frame):
  global bstack111lllll11_opy_
  logger.error(bstack1111ll11l_opy_)
  bstack111lllll11_opy_.bstack11l111l1ll_opy_(bstack1l11ll1_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱࡔ࡯ࠨਪ"), bstack11lll11lll_opy_)
  if hasattr(signal, bstack1l11ll1_opy_ (u"࠭ࡓࡪࡩࡱࡥࡱࡹࠧਫ")):
    bstack111lllll11_opy_.bstack11l111l1ll_opy_(bstack1l11ll1_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡔ࡫ࡪࡲࡦࡲࠧਬ"), signal.Signals(bstack11lll11lll_opy_).name)
  else:
    bstack111lllll11_opy_.bstack11l111l1ll_opy_(bstack1l11ll1_opy_ (u"ࠨࡵࡧ࡯ࡐ࡯࡬࡭ࡕ࡬࡫ࡳࡧ࡬ࠨਭ"), bstack1l11ll1_opy_ (u"ࠩࡖࡍࡌ࡛ࡎࡌࡐࡒ࡛ࡓ࠭ਮ"))
  if cli.is_running():
    bstack1l1111l1_opy_.invoke(bstack1l11lll111_opy_.bstack1l1111ll_opy_)
  bstack11ll111ll_opy_ = os.environ.get(bstack1l11ll1_opy_ (u"ࠪࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡕࡔࡇࡇࠫਯ"))
  if bstack11ll111ll_opy_ == bstack1l11ll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫਰ") and not cli.is_enabled(CONFIG):
    bstack1l111111l1_opy_.stop(bstack111lllll11_opy_.get_property(bstack1l11ll1_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬ਱")))
  bstack1l11l1ll_opy_()
  sys.exit(1)
def bstack1ll1l1l11_opy_(err):
  logger.critical(bstack1ll1llll1l_opy_.format(str(err)))
  bstack1lllll111l_opy_(bstack1ll1llll1l_opy_.format(str(err)), True)
  atexit.unregister(bstack1l11l1ll_opy_)
  bstack1l1ll11ll1_opy_()
  sys.exit(1)
def bstack11l1l1ll_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1lllll111l_opy_(message, True)
  atexit.unregister(bstack1l11l1ll_opy_)
  bstack1l1ll11ll1_opy_()
  sys.exit(1)
def bstack1l1ll1ll_opy_():
  global CONFIG
  global bstack1lll111l11_opy_
  global bstack1l1lllll11_opy_
  global bstack1111lll1_opy_
  CONFIG = bstack11lllllll1_opy_()
  load_dotenv(CONFIG.get(bstack1l11ll1_opy_ (u"࠭ࡥ࡯ࡸࡉ࡭ࡱ࡫ࠧਲ")))
  bstack111l1l11l_opy_()
  bstack1l111lll1l_opy_()
  CONFIG = bstack1l1l111ll1_opy_(CONFIG)
  update(CONFIG, bstack1l1lllll11_opy_)
  update(CONFIG, bstack1lll111l11_opy_)
  if not cli.is_enabled(CONFIG):
    CONFIG = bstack1l1l11ll_opy_(CONFIG)
  bstack1111lll1_opy_ = bstack1llll1llll_opy_(CONFIG)
  os.environ[bstack1l11ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪਲ਼")] = bstack1111lll1_opy_.__str__().lower()
  bstack111lllll11_opy_.bstack11l111l1ll_opy_(bstack1l11ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩ਴"), bstack1111lll1_opy_)
  if (bstack1l11ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬਵ") in CONFIG and bstack1l11ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ਸ਼") in bstack1lll111l11_opy_) or (
          bstack1l11ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ਷") in CONFIG and bstack1l11ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨਸ") not in bstack1l1lllll11_opy_):
    if os.getenv(bstack1l11ll1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪਹ")):
      CONFIG[bstack1l11ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ਺")] = os.getenv(bstack1l11ll1_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬ਻"))
    else:
      if not CONFIG.get(bstack1l11ll1_opy_ (u"ࠤࡩࡶࡦࡳࡥࡸࡱࡵ࡯਼ࠧ"), bstack1l11ll1_opy_ (u"ࠥࠦ਽")) in bstack11l11lllll_opy_:
        bstack1ll1ll1l1_opy_()
  elif (bstack1l11ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧਾ") not in CONFIG and bstack1l11ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧਿ") in CONFIG) or (
          bstack1l11ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩੀ") in bstack1l1lllll11_opy_ and bstack1l11ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪੁ") not in bstack1lll111l11_opy_):
    del (CONFIG[bstack1l11ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪੂ")])
  if bstack11l1l1l1l_opy_(CONFIG):
    bstack1ll1l1l11_opy_(bstack1l1111ll1l_opy_)
  Config.bstack1lll111l1l_opy_().bstack11l111l1ll_opy_(bstack1l11ll1_opy_ (u"ࠤࡸࡷࡪࡸࡎࡢ࡯ࡨࠦ੃"), CONFIG[bstack1l11ll1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ੄")])
  bstack1l111l11_opy_()
  bstack111ll1lll_opy_()
  if bstack1lllll11l_opy_ and not CONFIG.get(bstack1l11ll1_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠢ੅"), bstack1l11ll1_opy_ (u"ࠧࠨ੆")) in bstack11l11lllll_opy_:
    CONFIG[bstack1l11ll1_opy_ (u"࠭ࡡࡱࡲࠪੇ")] = bstack11l11l111l_opy_(CONFIG)
    logger.info(bstack11lll1111l_opy_.format(CONFIG[bstack1l11ll1_opy_ (u"ࠧࡢࡲࡳࠫੈ")]))
  if not bstack1111lll1_opy_:
    CONFIG[bstack1l11ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ੉")] = [{}]
def bstack11l1l1l111_opy_(config, bstack111l1111_opy_):
  global CONFIG
  global bstack1lllll11l_opy_
  CONFIG = config
  bstack1lllll11l_opy_ = bstack111l1111_opy_
def bstack111ll1lll_opy_():
  global CONFIG
  global bstack1lllll11l_opy_
  if bstack1l11ll1_opy_ (u"ࠩࡤࡴࡵ࠭੊") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack11l1l1ll_opy_(e, bstack1l1llll1l1_opy_)
    bstack1lllll11l_opy_ = True
    bstack111lllll11_opy_.bstack11l111l1ll_opy_(bstack1l11ll1_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩੋ"), True)
def bstack11l11l111l_opy_(config):
  bstack1l1ll1l11l_opy_ = bstack1l11ll1_opy_ (u"ࠫࠬੌ")
  app = config[bstack1l11ll1_opy_ (u"ࠬࡧࡰࡱ੍ࠩ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack11111l11_opy_:
      if os.path.exists(app):
        bstack1l1ll1l11l_opy_ = bstack1llllll1ll_opy_(config, app)
      elif bstack11111l1ll_opy_(app):
        bstack1l1ll1l11l_opy_ = app
      else:
        bstack1ll1l1l11_opy_(bstack1llll11l_opy_.format(app))
    else:
      if bstack11111l1ll_opy_(app):
        bstack1l1ll1l11l_opy_ = app
      elif os.path.exists(app):
        bstack1l1ll1l11l_opy_ = bstack1llllll1ll_opy_(app)
      else:
        bstack1ll1l1l11_opy_(bstack1l1l1l1ll1_opy_)
  else:
    if len(app) > 2:
      bstack1ll1l1l11_opy_(bstack1lll111111_opy_)
    elif len(app) == 2:
      if bstack1l11ll1_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ੎") in app and bstack1l11ll1_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪ੏") in app:
        if os.path.exists(app[bstack1l11ll1_opy_ (u"ࠨࡲࡤࡸ࡭࠭੐")]):
          bstack1l1ll1l11l_opy_ = bstack1llllll1ll_opy_(config, app[bstack1l11ll1_opy_ (u"ࠩࡳࡥࡹ࡮ࠧੑ")], app[bstack1l11ll1_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭੒")])
        else:
          bstack1ll1l1l11_opy_(bstack1llll11l_opy_.format(app))
      else:
        bstack1ll1l1l11_opy_(bstack1lll111111_opy_)
    else:
      for key in app:
        if key in bstack11lll11l11_opy_:
          if key == bstack1l11ll1_opy_ (u"ࠫࡵࡧࡴࡩࠩ੓"):
            if os.path.exists(app[key]):
              bstack1l1ll1l11l_opy_ = bstack1llllll1ll_opy_(config, app[key])
            else:
              bstack1ll1l1l11_opy_(bstack1llll11l_opy_.format(app))
          else:
            bstack1l1ll1l11l_opy_ = app[key]
        else:
          bstack1ll1l1l11_opy_(bstack1l11ll1lll_opy_)
  return bstack1l1ll1l11l_opy_
def bstack11111l1ll_opy_(bstack1l1ll1l11l_opy_):
  import re
  bstack11ll111ll1_opy_ = re.compile(bstack1l11ll1_opy_ (u"ࡷࠨ࡞࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭ࠨࠧ੔"))
  bstack1111ll1l_opy_ = re.compile(bstack1l11ll1_opy_ (u"ࡸࠢ࡟࡝ࡤ࠱ࡿࡇ࡛࠭࠲࠰࠽ࡡࡥ࠮࡝࠯ࡠ࠮࠴ࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫࠦࠥ੕"))
  if bstack1l11ll1_opy_ (u"ࠧࡣࡵ࠽࠳࠴࠭੖") in bstack1l1ll1l11l_opy_ or re.fullmatch(bstack11ll111ll1_opy_, bstack1l1ll1l11l_opy_) or re.fullmatch(bstack1111ll1l_opy_, bstack1l1ll1l11l_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack1ll1l1llll_opy_, stage=STAGE.bstack11lllll111_opy_, bstack1l11111l1_opy_=bstack1l11111l1l_opy_)
def bstack1llllll1ll_opy_(config, path, bstack11l11ll1ll_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1l11ll1_opy_ (u"ࠨࡴࡥࠫ੗")).read()).hexdigest()
  bstack1llll111ll_opy_ = bstack1ll1ll1lll_opy_(md5_hash)
  bstack1l1ll1l11l_opy_ = None
  if bstack1llll111ll_opy_:
    logger.info(bstack1l1ll1lll_opy_.format(bstack1llll111ll_opy_, md5_hash))
    return bstack1llll111ll_opy_
  bstack1l11ll1ll_opy_ = datetime.datetime.now()
  bstack1l1ll111l1_opy_ = MultipartEncoder(
    fields={
      bstack1l11ll1_opy_ (u"ࠩࡩ࡭ࡱ࡫ࠧ੘"): (os.path.basename(path), open(os.path.abspath(path), bstack1l11ll1_opy_ (u"ࠪࡶࡧ࠭ਖ਼")), bstack1l11ll1_opy_ (u"ࠫࡹ࡫ࡸࡵ࠱ࡳࡰࡦ࡯࡮ࠨਗ਼")),
      bstack1l11ll1_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨਜ਼"): bstack11l11ll1ll_opy_
    }
  )
  response = requests.post(bstack1l1111ll11_opy_, data=bstack1l1ll111l1_opy_,
                           headers={bstack1l11ll1_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬੜ"): bstack1l1ll111l1_opy_.content_type},
                           auth=(config[bstack1l11ll1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ੝")], config[bstack1l11ll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫਫ਼")]))
  try:
    res = json.loads(response.text)
    bstack1l1ll1l11l_opy_ = res[bstack1l11ll1_opy_ (u"ࠩࡤࡴࡵࡥࡵࡳ࡮ࠪ੟")]
    logger.info(bstack11ll11ll11_opy_.format(bstack1l1ll1l11l_opy_))
    bstack1l11l1lll_opy_(md5_hash, bstack1l1ll1l11l_opy_)
    cli.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻ࡷࡳࡰࡴࡧࡤࡠࡣࡳࡴࠧ੠"), datetime.datetime.now() - bstack1l11ll1ll_opy_)
  except ValueError as err:
    bstack1ll1l1l11_opy_(bstack1l11l11l1l_opy_.format(str(err)))
  return bstack1l1ll1l11l_opy_
def bstack1l111l11_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack11ll11ll1_opy_
  bstack1ll1lll111_opy_ = 1
  bstack11l1l1lll_opy_ = 1
  if bstack1l11ll1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ੡") in CONFIG:
    bstack11l1l1lll_opy_ = CONFIG[bstack1l11ll1_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ੢")]
  else:
    bstack11l1l1lll_opy_ = bstack111ll1ll_opy_(framework_name, args) or 1
  if bstack1l11ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ੣") in CONFIG:
    bstack1ll1lll111_opy_ = len(CONFIG[bstack1l11ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ੤")])
  bstack11ll11ll1_opy_ = int(bstack11l1l1lll_opy_) * int(bstack1ll1lll111_opy_)
def bstack111ll1ll_opy_(framework_name, args):
  if framework_name == bstack1l1111l11l_opy_ and args and bstack1l11ll1_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭੥") in args:
      bstack111l111l1_opy_ = args.index(bstack1l11ll1_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ੦"))
      return int(args[bstack111l111l1_opy_ + 1]) or 1
  return 1
def bstack1ll1ll1lll_opy_(md5_hash):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l11ll1_opy_ (u"ࠪࡪ࡮ࡲࡥ࡭ࡱࡦ࡯ࠥࡴ࡯ࡵࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩ࠱ࠦࡵࡴ࡫ࡱ࡫ࠥࡨࡡࡴ࡫ࡦࠤ࡫࡯࡬ࡦࠢࡲࡴࡪࡸࡡࡵ࡫ࡲࡲࡸ࠭੧"))
    bstack1l1llllll1_opy_ = os.path.join(os.path.expanduser(bstack1l11ll1_opy_ (u"ࠫࢃ࠭੨")), bstack1l11ll1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ੩"), bstack1l11ll1_opy_ (u"࠭ࡡࡱࡲࡘࡴࡱࡵࡡࡥࡏࡇ࠹ࡍࡧࡳࡩ࠰࡭ࡷࡴࡴࠧ੪"))
    if os.path.exists(bstack1l1llllll1_opy_):
      try:
        bstack1l11ll1l1l_opy_ = json.load(open(bstack1l1llllll1_opy_, bstack1l11ll1_opy_ (u"ࠧࡳࡤࠪ੫")))
        if md5_hash in bstack1l11ll1l1l_opy_:
          bstack11llll111l_opy_ = bstack1l11ll1l1l_opy_[md5_hash]
          bstack1l1llll11_opy_ = datetime.datetime.now()
          bstack11l1llll1l_opy_ = datetime.datetime.strptime(bstack11llll111l_opy_[bstack1l11ll1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ੬")], bstack1l11ll1_opy_ (u"ࠩࠨࡨ࠴ࠫ࡭࠰ࠧ࡜ࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭੭"))
          if (bstack1l1llll11_opy_ - bstack11l1llll1l_opy_).days > 30:
            return None
          elif version.parse(str(__version__)) > version.parse(bstack11llll111l_opy_[bstack1l11ll1_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ੮")]):
            return None
          return bstack11llll111l_opy_[bstack1l11ll1_opy_ (u"ࠫ࡮ࡪࠧ੯")]
      except Exception as e:
        logger.debug(bstack1l11ll1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡷ࡫ࡡࡥ࡫ࡱ࡫ࠥࡓࡄ࠶ࠢ࡫ࡥࡸ࡮ࠠࡧ࡫࡯ࡩ࠿ࠦࡻࡾࠩੰ").format(str(e)))
    return None
  bstack1l1llllll1_opy_ = os.path.join(os.path.expanduser(bstack1l11ll1_opy_ (u"࠭ࡾࠨੱ")), bstack1l11ll1_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧੲ"), bstack1l11ll1_opy_ (u"ࠨࡣࡳࡴ࡚ࡶ࡬ࡰࡣࡧࡑࡉ࠻ࡈࡢࡵ࡫࠲࡯ࡹ࡯࡯ࠩੳ"))
  lock_file = bstack1l1llllll1_opy_ + bstack1l11ll1_opy_ (u"ࠩ࠱ࡰࡴࡩ࡫ࠨੴ")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack1l1llllll1_opy_):
        with open(bstack1l1llllll1_opy_, bstack1l11ll1_opy_ (u"ࠪࡶࠬੵ")) as f:
          content = f.read().strip()
          if content:
            bstack1l11ll1l1l_opy_ = json.loads(content)
            if md5_hash in bstack1l11ll1l1l_opy_:
              bstack11llll111l_opy_ = bstack1l11ll1l1l_opy_[md5_hash]
              bstack1l1llll11_opy_ = datetime.datetime.now()
              bstack11l1llll1l_opy_ = datetime.datetime.strptime(bstack11llll111l_opy_[bstack1l11ll1_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ੶")], bstack1l11ll1_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩ੷"))
              if (bstack1l1llll11_opy_ - bstack11l1llll1l_opy_).days > 30:
                return None
              elif version.parse(str(__version__)) > version.parse(bstack11llll111l_opy_[bstack1l11ll1_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ੸")]):
                return None
              return bstack11llll111l_opy_[bstack1l11ll1_opy_ (u"ࠧࡪࡦࠪ੹")]
      return None
  except Exception as e:
    logger.debug(bstack1l11ll1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡸ࡫ࡷ࡬ࠥ࡬ࡩ࡭ࡧࠣࡰࡴࡩ࡫ࡪࡰࡪࠤ࡫ࡵࡲࠡࡏࡇ࠹ࠥ࡮ࡡࡴࡪ࠽ࠤࢀࢃࠧ੺").format(str(e)))
    return None
def bstack1l11l1lll_opy_(md5_hash, bstack1l1ll1l11l_opy_):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l11ll1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡬ࡰࡥ࡮ࠤࡳࡵࡴࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨ࠰ࠥࡻࡳࡪࡰࡪࠤࡧࡧࡳࡪࡥࠣࡪ࡮ࡲࡥࠡࡱࡳࡩࡷࡧࡴࡪࡱࡱࡷࠬ੻"))
    bstack1ll11l111_opy_ = os.path.join(os.path.expanduser(bstack1l11ll1_opy_ (u"ࠪࢂࠬ੼")), bstack1l11ll1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ੽"))
    if not os.path.exists(bstack1ll11l111_opy_):
      os.makedirs(bstack1ll11l111_opy_)
    bstack1l1llllll1_opy_ = os.path.join(os.path.expanduser(bstack1l11ll1_opy_ (u"ࠬࢄࠧ੾")), bstack1l11ll1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭੿"), bstack1l11ll1_opy_ (u"ࠧࡢࡲࡳ࡙ࡵࡲ࡯ࡢࡦࡐࡈ࠺ࡎࡡࡴࡪ࠱࡮ࡸࡵ࡮ࠨ઀"))
    bstack1ll11lll11_opy_ = {
      bstack1l11ll1_opy_ (u"ࠨ࡫ࡧࠫઁ"): bstack1l1ll1l11l_opy_,
      bstack1l11ll1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬં"): datetime.datetime.strftime(datetime.datetime.now(), bstack1l11ll1_opy_ (u"ࠪࠩࡩ࠵ࠥ࡮࠱ࠨ࡝ࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧઃ")),
      bstack1l11ll1_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ઄"): str(__version__)
    }
    try:
      bstack1l11ll1l1l_opy_ = {}
      if os.path.exists(bstack1l1llllll1_opy_):
        bstack1l11ll1l1l_opy_ = json.load(open(bstack1l1llllll1_opy_, bstack1l11ll1_opy_ (u"ࠬࡸࡢࠨઅ")))
      bstack1l11ll1l1l_opy_[md5_hash] = bstack1ll11lll11_opy_
      with open(bstack1l1llllll1_opy_, bstack1l11ll1_opy_ (u"ࠨࡷࠬࠤઆ")) as outfile:
        json.dump(bstack1l11ll1l1l_opy_, outfile)
    except Exception as e:
      logger.debug(bstack1l11ll1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡵࡱࡦࡤࡸ࡮ࡴࡧࠡࡏࡇ࠹ࠥ࡮ࡡࡴࡪࠣࡪ࡮ࡲࡥ࠻ࠢࡾࢁࠬઇ").format(str(e)))
    return
  bstack1ll11l111_opy_ = os.path.join(os.path.expanduser(bstack1l11ll1_opy_ (u"ࠨࢀࠪઈ")), bstack1l11ll1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩઉ"))
  if not os.path.exists(bstack1ll11l111_opy_):
    os.makedirs(bstack1ll11l111_opy_)
  bstack1l1llllll1_opy_ = os.path.join(os.path.expanduser(bstack1l11ll1_opy_ (u"ࠪࢂࠬઊ")), bstack1l11ll1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫઋ"), bstack1l11ll1_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭ઌ"))
  lock_file = bstack1l1llllll1_opy_ + bstack1l11ll1_opy_ (u"࠭࠮࡭ࡱࡦ࡯ࠬઍ")
  bstack1ll11lll11_opy_ = {
    bstack1l11ll1_opy_ (u"ࠧࡪࡦࠪ઎"): bstack1l1ll1l11l_opy_,
    bstack1l11ll1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫએ"): datetime.datetime.strftime(datetime.datetime.now(), bstack1l11ll1_opy_ (u"ࠩࠨࡨ࠴ࠫ࡭࠰ࠧ࡜ࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭ઐ")),
    bstack1l11ll1_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨઑ"): str(__version__)
  }
  try:
    with FileLock(lock_file, timeout=10):
      bstack1l11ll1l1l_opy_ = {}
      if os.path.exists(bstack1l1llllll1_opy_):
        with open(bstack1l1llllll1_opy_, bstack1l11ll1_opy_ (u"ࠫࡷ࠭઒")) as f:
          content = f.read().strip()
          if content:
            bstack1l11ll1l1l_opy_ = json.loads(content)
      bstack1l11ll1l1l_opy_[md5_hash] = bstack1ll11lll11_opy_
      with open(bstack1l1llllll1_opy_, bstack1l11ll1_opy_ (u"ࠧࡽࠢઓ")) as outfile:
        json.dump(bstack1l11ll1l1l_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1l11ll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡽࡩࡵࡪࠣࡪ࡮ࡲࡥࠡ࡮ࡲࡧࡰ࡯࡮ࡨࠢࡩࡳࡷࠦࡍࡅ࠷ࠣ࡬ࡦࡹࡨࠡࡷࡳࡨࡦࡺࡥ࠻ࠢࡾࢁࠬઔ").format(str(e)))
def bstack11111ll1_opy_(self):
  return
def bstack1lll111l1_opy_(self):
  return
def bstack1lll1ll1ll_opy_():
  global bstack1l1ll1ll11_opy_
  bstack1l1ll1ll11_opy_ = True
@measure(event_name=EVENTS.bstack1ll1llll1_opy_, stage=STAGE.bstack11lllll111_opy_, bstack1l11111l1_opy_=bstack1l11111l1l_opy_)
def bstack11ll1l1l_opy_(self):
  global bstack11ll1l1l11_opy_
  global bstack1l111l1lll_opy_
  global bstack1l1l1ll1_opy_
  try:
    if bstack1l11ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧક") in bstack11ll1l1l11_opy_ and self.session_id != None and bstack1l11111ll_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬખ"), bstack1l11ll1_opy_ (u"ࠩࠪગ")) != bstack1l11ll1_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫઘ"):
      bstack1lll11l1l_opy_ = bstack1l11ll1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫઙ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1l11ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬચ")
      if bstack1lll11l1l_opy_ == bstack1l11ll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭છ"):
        bstack1l1111l11_opy_(logger)
      if self != None:
        bstack1l1l111l1_opy_(self, bstack1lll11l1l_opy_, bstack1l11ll1_opy_ (u"ࠧ࠭ࠢࠪજ").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack1l11ll1_opy_ (u"ࠨࠩઝ")
    if bstack1l11ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩઞ") in bstack11ll1l1l11_opy_ and getattr(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩટ"), None):
      bstack1ll11l1l11_opy_.bstack111l111l_opy_(self, bstack11ll1l1ll1_opy_, logger, wait=True)
    if bstack1l11ll1_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫઠ") in bstack11ll1l1l11_opy_:
      if not threading.currentThread().behave_test_status:
        bstack1l1l111l1_opy_(self, bstack1l11ll1_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧડ"))
      bstack11ll11ll_opy_.bstack1111111l1_opy_(self)
  except Exception as e:
    logger.debug(bstack1l11ll1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࠢઢ") + str(e))
  bstack1l1l1ll1_opy_(self)
  self.session_id = None
def bstack1l111111ll_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack1l11l11ll_opy_
    global bstack11ll1l1l11_opy_
    command_executor = kwargs.get(bstack1l11ll1_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠪણ"), bstack1l11ll1_opy_ (u"ࠨࠩત"))
    bstack1l11lll1_opy_ = False
    if type(command_executor) == str and bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬથ") in command_executor:
      bstack1l11lll1_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭દ") in str(getattr(command_executor, bstack1l11ll1_opy_ (u"ࠫࡤࡻࡲ࡭ࠩધ"), bstack1l11ll1_opy_ (u"ࠬ࠭ન"))):
      bstack1l11lll1_opy_ = True
    else:
      kwargs = bstack11lll1ll1l_opy_.bstack1111111ll_opy_(bstack1l1l111l_opy_=kwargs, config=CONFIG)
      return bstack1ll11lll_opy_(self, *args, **kwargs)
    if bstack1l11lll1_opy_:
      bstack1ll1ll1111_opy_ = bstack1ll111ll_opy_.bstack1ll1l1l1l_opy_(CONFIG, bstack11ll1l1l11_opy_)
      if kwargs.get(bstack1l11ll1_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧ઩")):
        kwargs[bstack1l11ll1_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨપ")] = bstack1l11l11ll_opy_(kwargs[bstack1l11ll1_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩફ")], bstack11ll1l1l11_opy_, CONFIG, bstack1ll1ll1111_opy_)
      elif kwargs.get(bstack1l11ll1_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩબ")):
        kwargs[bstack1l11ll1_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪભ")] = bstack1l11l11ll_opy_(kwargs[bstack1l11ll1_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫમ")], bstack11ll1l1l11_opy_, CONFIG, bstack1ll1ll1111_opy_)
  except Exception as e:
    logger.error(bstack1l11ll1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡥ࡯ࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡓࡅࡍࠣࡧࡦࡶࡳ࠻ࠢࡾࢁࠧય").format(str(e)))
  return bstack1ll11lll_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack11l1l1ll1l_opy_, stage=STAGE.bstack11lllll111_opy_, bstack1l11111l1_opy_=bstack1l11111l1l_opy_)
def bstack111lll11_opy_(self, command_executor=bstack1l11ll1_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵࠱࠳࠹࠱࠴࠳࠶࠮࠲࠼࠷࠸࠹࠺ࠢર"), *args, **kwargs):
  global bstack1l111l1lll_opy_
  global bstack11l11lll1l_opy_
  bstack1l1111l1ll_opy_ = bstack1l111111ll_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack11llllllll_opy_.on():
    return bstack1l1111l1ll_opy_
  try:
    logger.debug(bstack1l11ll1_opy_ (u"ࠧࡄࡱࡰࡱࡦࡴࡤࠡࡇࡻࡩࡨࡻࡴࡰࡴࠣࡻ࡭࡫࡮ࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤ࡮ࡹࠠࡧࡣ࡯ࡷࡪࠦ࠭ࠡࡽࢀࠫ઱").format(str(command_executor)))
    logger.debug(bstack1l11ll1_opy_ (u"ࠨࡊࡸࡦ࡛ࠥࡒࡍࠢ࡬ࡷࠥ࠳ࠠࡼࡿࠪલ").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬળ") in command_executor._url:
      bstack111lllll11_opy_.bstack11l111l1ll_opy_(bstack1l11ll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫ઴"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧવ") in command_executor):
    bstack111lllll11_opy_.bstack11l111l1ll_opy_(bstack1l11ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭શ"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1ll11l1l1l_opy_ = getattr(threading.current_thread(), bstack1l11ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡚ࡥࡴࡶࡐࡩࡹࡧࠧષ"), None)
  bstack11lll1111_opy_ = {}
  if self.capabilities is not None:
    bstack11lll1111_opy_[bstack1l11ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡰࡤࡱࡪ࠭સ")] = self.capabilities.get(bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭હ"))
    bstack11lll1111_opy_[bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫ઺")] = self.capabilities.get(bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ઻"))
    bstack11lll1111_opy_[bstack1l11ll1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡣࡴࡶࡴࡪࡱࡱࡷ઼ࠬ")] = self.capabilities.get(bstack1l11ll1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪઽ"))
  if CONFIG.get(bstack1l11ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ા"), False) and bstack11lll1ll1l_opy_.bstack11l1lll11l_opy_(bstack11lll1111_opy_):
    threading.current_thread().a11yPlatform = True
  if bstack1l11ll1_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧિ") in bstack11ll1l1l11_opy_ or bstack1l11ll1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧી") in bstack11ll1l1l11_opy_:
    bstack1l111111l1_opy_.bstack111llllll_opy_(self)
  if bstack1l11ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩુ") in bstack11ll1l1l11_opy_ and bstack1ll11l1l1l_opy_ and bstack1ll11l1l1l_opy_.get(bstack1l11ll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪૂ"), bstack1l11ll1_opy_ (u"ࠫࠬૃ")) == bstack1l11ll1_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭ૄ"):
    bstack1l111111l1_opy_.bstack111llllll_opy_(self)
  bstack1l111l1lll_opy_ = self.session_id
  with bstack111ll111_opy_:
    bstack11l11lll1l_opy_.append(self)
  return bstack1l1111l1ll_opy_
def bstack11l11lll11_opy_(args):
  return bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠧૅ") in str(args)
def bstack1l1l1l11_opy_(self, driver_command, *args, **kwargs):
  global bstack1ll1l111ll_opy_
  global bstack111l11ll1_opy_
  bstack1lll1l1l1_opy_ = bstack1l11111ll_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ૆"), None) and bstack1l11111ll_opy_(
          threading.current_thread(), bstack1l11ll1_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧે"), None)
  bstack11llll1ll_opy_ = bstack1l11111ll_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩૈ"), None) and bstack1l11111ll_opy_(
          threading.current_thread(), bstack1l11ll1_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬૉ"), None)
  bstack11lll111_opy_ = getattr(self, bstack1l11ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫ૊"), None) != None and getattr(self, bstack1l11ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬો"), None) == True
  if not bstack111l11ll1_opy_ and bstack1l11ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ૌ") in CONFIG and CONFIG[bstack1l11ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ્ࠧ")] == True and bstack1l11l11l_opy_.bstack11llll1l11_opy_(driver_command) and (bstack11lll111_opy_ or bstack1lll1l1l1_opy_ or bstack11llll1ll_opy_) and not bstack11l11lll11_opy_(args):
    try:
      bstack111l11ll1_opy_ = True
      logger.debug(bstack1l11ll1_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡪࡴࡸࠠࡼࡿࠪ૎").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack1l11ll1_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡥࡳࡨࡲࡶࡲࠦࡳࡤࡣࡱࠤࢀࢃࠧ૏").format(str(err)))
    bstack111l11ll1_opy_ = False
  response = bstack1ll1l111ll_opy_(self, driver_command, *args, **kwargs)
  if (bstack1l11ll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩૐ") in str(bstack11ll1l1l11_opy_).lower() or bstack1l11ll1_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ૑") in str(bstack11ll1l1l11_opy_).lower()) and bstack11llllllll_opy_.on():
    try:
      if driver_command == bstack1l11ll1_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠩ૒"):
        bstack1l111111l1_opy_.bstack1l1l1111ll_opy_({
            bstack1l11ll1_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬ૓"): response[bstack1l11ll1_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭૔")],
            bstack1l11ll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ૕"): bstack1l111111l1_opy_.current_test_uuid() if bstack1l111111l1_opy_.current_test_uuid() else bstack11llllllll_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
@measure(event_name=EVENTS.bstack1111111l_opy_, stage=STAGE.bstack11lllll111_opy_, bstack1l11111l1_opy_=bstack1l11111l1l_opy_)
def bstack11lllll11_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack1l111l1lll_opy_
  global bstack11ll1llll_opy_
  global bstack1l11111l1l_opy_
  global bstack11llll111_opy_
  global bstack11lllll1l_opy_
  global bstack11ll1l1l11_opy_
  global bstack1ll11lll_opy_
  global bstack11l11lll1l_opy_
  global bstack11l1l1111_opy_
  global bstack11ll1l1ll1_opy_
  if os.getenv(bstack1l11ll1_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ૖")) is not None and bstack11lll1ll1l_opy_.bstack1l111l11l1_opy_(CONFIG) is None:
    CONFIG[bstack1l11ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ૗")] = True
  CONFIG[bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭૘")] = str(bstack11ll1l1l11_opy_) + str(__version__)
  bstack11l11l1111_opy_ = os.environ[bstack1l11ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ૙")]
  bstack1ll1ll1111_opy_ = bstack1ll111ll_opy_.bstack1ll1l1l1l_opy_(CONFIG, bstack11ll1l1l11_opy_)
  CONFIG[bstack1l11ll1_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ૚")] = bstack11l11l1111_opy_
  CONFIG[bstack1l11ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩ૛")] = bstack1ll1ll1111_opy_
  if CONFIG.get(bstack1l11ll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ૜"),bstack1l11ll1_opy_ (u"ࠩࠪ૝")) and bstack1l11ll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ૞") in bstack11ll1l1l11_opy_:
    CONFIG[bstack1l11ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ૟")].pop(bstack1l11ll1_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪૠ"), None)
    CONFIG[bstack1l11ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ૡ")].pop(bstack1l11ll1_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬૢ"), None)
  command_executor = bstack111111111_opy_()
  logger.debug(bstack1l111l1111_opy_.format(command_executor))
  proxy = bstack111llll1l_opy_(CONFIG, proxy)
  bstack1lll1ll111_opy_ = 0 if bstack11ll1llll_opy_ < 0 else bstack11ll1llll_opy_
  try:
    if bstack11llll111_opy_ is True:
      bstack1lll1ll111_opy_ = int(multiprocessing.current_process().name)
    elif bstack11lllll1l_opy_ is True:
      bstack1lll1ll111_opy_ = int(threading.current_thread().name)
  except:
    bstack1lll1ll111_opy_ = 0
  bstack1l1lll1l11_opy_ = bstack11l1111ll1_opy_(CONFIG, bstack1lll1ll111_opy_)
  logger.debug(bstack111llll11_opy_.format(str(bstack1l1lll1l11_opy_)))
  if bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬૣ") in CONFIG and bstack11l1ll11l1_opy_(CONFIG[bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭૤")]):
    bstack1l1l11lll_opy_(bstack1l1lll1l11_opy_)
  if bstack11lll1ll1l_opy_.bstack1l1l11l111_opy_(CONFIG, bstack1lll1ll111_opy_) and bstack11lll1ll1l_opy_.bstack11l1l11111_opy_(bstack1l1lll1l11_opy_, options, desired_capabilities, CONFIG):
    threading.current_thread().a11yPlatform = True
    if (cli.accessibility is None or not cli.accessibility.is_enabled()):
      bstack11lll1ll1l_opy_.set_capabilities(bstack1l1lll1l11_opy_, CONFIG)
  if desired_capabilities:
    bstack1l1111ll1_opy_ = bstack1l1l111ll1_opy_(desired_capabilities)
    bstack1l1111ll1_opy_[bstack1l11ll1_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ૥")] = bstack11lll11111_opy_(CONFIG)
    bstack1ll1l11ll_opy_ = bstack11l1111ll1_opy_(bstack1l1111ll1_opy_)
    if bstack1ll1l11ll_opy_:
      bstack1l1lll1l11_opy_ = update(bstack1ll1l11ll_opy_, bstack1l1lll1l11_opy_)
    desired_capabilities = None
  if options:
    bstack1l111lll11_opy_(options, bstack1l1lll1l11_opy_)
  if not options:
    options = bstack11111l111_opy_(bstack1l1lll1l11_opy_)
  bstack11ll1l1ll1_opy_ = CONFIG.get(bstack1l11ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ૦"))[bstack1lll1ll111_opy_]
  if proxy and bstack11llll11ll_opy_() >= version.parse(bstack1l11ll1_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬ૧")):
    options.proxy(proxy)
  if options and bstack11llll11ll_opy_() >= version.parse(bstack1l11ll1_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ૨")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack11llll11ll_opy_() < version.parse(bstack1l11ll1_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭૩")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1l1lll1l11_opy_)
  logger.info(bstack11lll1lll1_opy_)
  bstack1lll11l1_opy_.end(EVENTS.bstack1l111lll_opy_.value, EVENTS.bstack1l111lll_opy_.value + bstack1l11ll1_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ૪"), EVENTS.bstack1l111lll_opy_.value + bstack1l11ll1_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ૫"), status=True, failure=None, test_name=bstack1l11111l1l_opy_)
  if bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡵࡸ࡯ࡧ࡫࡯ࡩࠬ૬") in kwargs:
    del kwargs[bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡶࡲࡰࡨ࡬ࡰࡪ࠭૭")]
  try:
    if bstack11llll11ll_opy_() >= version.parse(bstack1l11ll1_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬ૮")):
      bstack1ll11lll_opy_(self, command_executor=command_executor,
                options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
    elif bstack11llll11ll_opy_() >= version.parse(bstack1l11ll1_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ૯")):
      bstack1ll11lll_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities, options=options,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11llll11ll_opy_() >= version.parse(bstack1l11ll1_opy_ (u"ࠧ࠳࠰࠸࠷࠳࠶ࠧ૰")):
      bstack1ll11lll_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    else:
      bstack1ll11lll_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive)
  except Exception as bstack1l1l1lll1l_opy_:
    logger.error(bstack1lll1ll1_opy_.format(bstack1l11ll1_opy_ (u"ࠨࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠧ૱"), str(bstack1l1l1lll1l_opy_)))
    raise bstack1l1l1lll1l_opy_
  if bstack11lll1ll1l_opy_.bstack1l1l11l111_opy_(CONFIG, bstack1lll1ll111_opy_) and bstack11lll1ll1l_opy_.bstack11l1l11111_opy_(self.caps, options, desired_capabilities):
    if CONFIG[bstack1l11ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ૲")][bstack1l11ll1_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩ૳")] == True:
      threading.current_thread().appA11yPlatform = True
      if cli.accessibility is None or not cli.accessibility.is_enabled():
        bstack11lll1ll1l_opy_.set_capabilities(bstack1l1lll1l11_opy_, CONFIG)
  try:
    bstack11lll1l1ll_opy_ = bstack1l11ll1_opy_ (u"ࠫࠬ૴")
    if bstack11llll11ll_opy_() >= version.parse(bstack1l11ll1_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭૵")):
      if self.caps is not None:
        bstack11lll1l1ll_opy_ = self.caps.get(bstack1l11ll1_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨ૶"))
    else:
      if self.capabilities is not None:
        bstack11lll1l1ll_opy_ = self.capabilities.get(bstack1l11ll1_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢ૷"))
    if bstack11lll1l1ll_opy_:
      bstack1ll111ll11_opy_(bstack11lll1l1ll_opy_)
      if bstack11llll11ll_opy_() <= version.parse(bstack1l11ll1_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨ૸")):
        self.command_executor._url = bstack1l11ll1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥૹ") + bstack11lll1ll11_opy_ + bstack1l11ll1_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢૺ")
      else:
        self.command_executor._url = bstack1l11ll1_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨૻ") + bstack11lll1l1ll_opy_ + bstack1l11ll1_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨૼ")
      logger.debug(bstack11111lll1_opy_.format(bstack11lll1l1ll_opy_))
    else:
      logger.debug(bstack11111lll_opy_.format(bstack1l11ll1_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢ૽")))
  except Exception as e:
    logger.debug(bstack11111lll_opy_.format(e))
  if bstack1l11ll1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭૾") in bstack11ll1l1l11_opy_:
    bstack1ll11l11l_opy_(bstack11ll1llll_opy_, bstack11l1l1111_opy_)
  bstack1l111l1lll_opy_ = self.session_id
  if bstack1l11ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ૿") in bstack11ll1l1l11_opy_ or bstack1l11ll1_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ଀") in bstack11ll1l1l11_opy_ or bstack1l11ll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩଁ") in bstack11ll1l1l11_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack1ll11l1l1l_opy_ = getattr(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡘࡪࡹࡴࡎࡧࡷࡥࠬଂ"), None)
  if bstack1l11ll1_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬଃ") in bstack11ll1l1l11_opy_ or bstack1l11ll1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ଄") in bstack11ll1l1l11_opy_:
    bstack1l111111l1_opy_.bstack111llllll_opy_(self)
  if bstack1l11ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧଅ") in bstack11ll1l1l11_opy_ and bstack1ll11l1l1l_opy_ and bstack1ll11l1l1l_opy_.get(bstack1l11ll1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨଆ"), bstack1l11ll1_opy_ (u"ࠩࠪଇ")) == bstack1l11ll1_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫଈ"):
    bstack1l111111l1_opy_.bstack111llllll_opy_(self)
  with bstack111ll111_opy_:
    bstack11l11lll1l_opy_.append(self)
  if bstack1l11ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଉ") in CONFIG and bstack1l11ll1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪଊ") in CONFIG[bstack1l11ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଋ")][bstack1lll1ll111_opy_]:
    bstack1l11111l1l_opy_ = CONFIG[bstack1l11ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଌ")][bstack1lll1ll111_opy_][bstack1l11ll1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭଍")]
  logger.debug(bstack1lll11l1l1_opy_.format(bstack1l111l1lll_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    from browserstack_sdk.__init__ import bstack1ll1lll11l_opy_
    def bstack1lllll1l1_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1ll11ll111_opy_
      if(bstack1l11ll1_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸ࠯࡬ࡶࠦ଎") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1l11ll1_opy_ (u"ࠪࢂࠬଏ")), bstack1l11ll1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫଐ"), bstack1l11ll1_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧ଑")), bstack1l11ll1_opy_ (u"࠭ࡷࠨ଒")) as fp:
          fp.write(bstack1l11ll1_opy_ (u"ࠢࠣଓ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1l11ll1_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥଔ")))):
          with open(args[1], bstack1l11ll1_opy_ (u"ࠩࡵࠫକ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1l11ll1_opy_ (u"ࠪࡥࡸࡿ࡮ࡤࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࡤࡴࡥࡸࡒࡤ࡫ࡪ࠮ࡣࡰࡰࡷࡩࡽࡺࠬࠡࡲࡤ࡫ࡪࠦ࠽ࠡࡸࡲ࡭ࡩࠦ࠰ࠪࠩଖ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack11ll111l1_opy_)
            if bstack1l11ll1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨଗ") in CONFIG and str(CONFIG[bstack1l11ll1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩଘ")]).lower() != bstack1l11ll1_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬଙ"):
                bstack1l111llll1_opy_ = bstack1ll1lll11l_opy_()
                bstack1l1ll1ll1_opy_ = bstack1l11ll1_opy_ (u"ࠧࠨࠩࠍ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࠐࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹࡝࠼ࠌࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠ࠿ࠏࡩ࡯࡯ࡵࡷࠤࡵࡥࡩ࡯ࡦࡨࡼࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠳࡟࠾ࠎࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡸࡲࡩࡤࡧࠫ࠴࠱ࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴ࠫ࠾ࠎࡨࡵ࡮ࡴࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫ࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤࠬ࠿ࠏ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡲࡡࡶࡰࡦ࡬ࠥࡃࠠࡢࡵࡼࡲࡨࠦࠨ࡭ࡣࡸࡲࡨ࡮ࡏࡱࡶ࡬ࡳࡳࡹࠩࠡ࠿ࡁࠤࢀࢁࠊࠡࠢ࡯ࡩࡹࠦࡣࡢࡲࡶ࠿ࠏࠦࠠࡵࡴࡼࠤࢀࢁࠊࠡࠢࠣࠤࡨࡧࡰࡴࠢࡀࠤࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸ࠯࠻ࠋࠢࠣࢁࢂࠦࡣࡢࡶࡦ࡬ࠥ࠮ࡥࡹࠫࠣࡿࢀࠐࠠࠡࠢࠣࡧࡴࡴࡳࡰ࡮ࡨ࠲ࡪࡸࡲࡰࡴࠫࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷ࠿ࠨࠬࠡࡧࡻ࠭ࡀࠐࠠࠡࡿࢀࠎࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡩ࡯࡯ࡰࡨࡧࡹ࠮ࡻࡼࠌࠣࠤࠥࠦࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶ࠽ࠤࠬࢁࡣࡥࡲࡘࡶࡱࢃࠧࠡ࠭ࠣࡩࡳࡩ࡯ࡥࡧࡘࡖࡎࡉ࡯࡮ࡲࡲࡲࡪࡴࡴࠩࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡦࡥࡵࡹࠩࠪ࠮ࠍࠤࠥࠦࠠ࠯࠰࠱ࡰࡦࡻ࡮ࡤࡪࡒࡴࡹ࡯࡯࡯ࡵࠍࠤࠥࢃࡽࠪ࠽ࠍࢁࢂࡁࠊ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱ࠍࠫࠬ࠭ଚ").format(bstack1l111llll1_opy_=bstack1l111llll1_opy_)
            lines.insert(1, bstack1l1ll1ll1_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1l11ll1_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥଛ")), bstack1l11ll1_opy_ (u"ࠩࡺࠫଜ")) as bstack1ll1lll1_opy_:
              bstack1ll1lll1_opy_.writelines(lines)
        CONFIG[bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬଝ")] = str(bstack11ll1l1l11_opy_) + str(__version__)
        bstack11l11l1111_opy_ = os.environ[bstack1l11ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩଞ")]
        bstack1ll1ll1111_opy_ = bstack1ll111ll_opy_.bstack1ll1l1l1l_opy_(CONFIG, bstack11ll1l1l11_opy_)
        CONFIG[bstack1l11ll1_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨଟ")] = bstack11l11l1111_opy_
        CONFIG[bstack1l11ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨଠ")] = bstack1ll1ll1111_opy_
        bstack1lll1ll111_opy_ = 0 if bstack11ll1llll_opy_ < 0 else bstack11ll1llll_opy_
        try:
          if bstack11llll111_opy_ is True:
            bstack1lll1ll111_opy_ = int(multiprocessing.current_process().name)
          elif bstack11lllll1l_opy_ is True:
            bstack1lll1ll111_opy_ = int(threading.current_thread().name)
        except:
          bstack1lll1ll111_opy_ = 0
        CONFIG[bstack1l11ll1_opy_ (u"ࠢࡶࡵࡨ࡛࠸ࡉࠢଡ")] = False
        CONFIG[bstack1l11ll1_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢଢ")] = True
        bstack1l1lll1l11_opy_ = bstack11l1111ll1_opy_(CONFIG, bstack1lll1ll111_opy_)
        logger.debug(bstack111llll11_opy_.format(str(bstack1l1lll1l11_opy_)))
        if CONFIG.get(bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ଣ")):
          bstack1l1l11lll_opy_(bstack1l1lll1l11_opy_)
        if bstack1l11ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ତ") in CONFIG and bstack1l11ll1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩଥ") in CONFIG[bstack1l11ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨଦ")][bstack1lll1ll111_opy_]:
          bstack1l11111l1l_opy_ = CONFIG[bstack1l11ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଧ")][bstack1lll1ll111_opy_][bstack1l11ll1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬନ")]
        args.append(os.path.join(os.path.expanduser(bstack1l11ll1_opy_ (u"ࠨࢀࠪ଩")), bstack1l11ll1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩପ"), bstack1l11ll1_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬଫ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1l1lll1l11_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1l11ll1_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨବ"))
      bstack1ll11ll111_opy_ = True
      return bstack1l1lll1111_opy_(self, args, bufsize=bufsize, executable=executable,
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
  def bstack111l1l111_opy_(self,
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
    global bstack11ll1llll_opy_
    global bstack1l11111l1l_opy_
    global bstack11llll111_opy_
    global bstack11lllll1l_opy_
    global bstack11ll1l1l11_opy_
    CONFIG[bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧଭ")] = str(bstack11ll1l1l11_opy_) + str(__version__)
    bstack11l11l1111_opy_ = os.environ[bstack1l11ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫମ")]
    bstack1ll1ll1111_opy_ = bstack1ll111ll_opy_.bstack1ll1l1l1l_opy_(CONFIG, bstack11ll1l1l11_opy_)
    CONFIG[bstack1l11ll1_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪଯ")] = bstack11l11l1111_opy_
    CONFIG[bstack1l11ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪର")] = bstack1ll1ll1111_opy_
    bstack1lll1ll111_opy_ = 0 if bstack11ll1llll_opy_ < 0 else bstack11ll1llll_opy_
    try:
      if bstack11llll111_opy_ is True:
        bstack1lll1ll111_opy_ = int(multiprocessing.current_process().name)
      elif bstack11lllll1l_opy_ is True:
        bstack1lll1ll111_opy_ = int(threading.current_thread().name)
    except:
      bstack1lll1ll111_opy_ = 0
    CONFIG[bstack1l11ll1_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ଱")] = True
    bstack1l1lll1l11_opy_ = bstack11l1111ll1_opy_(CONFIG, bstack1lll1ll111_opy_)
    logger.debug(bstack111llll11_opy_.format(str(bstack1l1lll1l11_opy_)))
    if CONFIG.get(bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧଲ")):
      bstack1l1l11lll_opy_(bstack1l1lll1l11_opy_)
    if bstack1l11ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଳ") in CONFIG and bstack1l11ll1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ଴") in CONFIG[bstack1l11ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଵ")][bstack1lll1ll111_opy_]:
      bstack1l11111l1l_opy_ = CONFIG[bstack1l11ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଶ")][bstack1lll1ll111_opy_][bstack1l11ll1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ଷ")]
    import urllib
    import json
    if bstack1l11ll1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ସ") in CONFIG and str(CONFIG[bstack1l11ll1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧହ")]).lower() != bstack1l11ll1_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪ଺"):
        bstack1lll1l11_opy_ = bstack1ll1lll11l_opy_()
        bstack1l111llll1_opy_ = bstack1lll1l11_opy_ + urllib.parse.quote(json.dumps(bstack1l1lll1l11_opy_))
    else:
        bstack1l111llll1_opy_ = bstack1l11ll1_opy_ (u"ࠬࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠧ଻") + urllib.parse.quote(json.dumps(bstack1l1lll1l11_opy_))
    browser = self.connect(bstack1l111llll1_opy_)
    return browser
except Exception as e:
    pass
def bstack1ll1l1l111_opy_():
    global bstack1ll11ll111_opy_
    global bstack11ll1l1l11_opy_
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1llll11l1l_opy_
        global bstack111lllll11_opy_
        if not bstack1111lll1_opy_:
          global bstack11ll1l11ll_opy_
          if not bstack11ll1l11ll_opy_:
            from bstack_utils.helper import bstack1l11ll11l_opy_, bstack1l1llll1l_opy_, bstack1ll1l11l_opy_
            bstack11ll1l11ll_opy_ = bstack1l11ll11l_opy_()
            bstack1l1llll1l_opy_(bstack11ll1l1l11_opy_)
            bstack1ll1ll1111_opy_ = bstack1ll111ll_opy_.bstack1ll1l1l1l_opy_(CONFIG, bstack11ll1l1l11_opy_)
            bstack111lllll11_opy_.bstack11l111l1ll_opy_(bstack1l11ll1_opy_ (u"ࠨࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡔࡗࡕࡄࡖࡅࡗࡣࡒࡇࡐ଼ࠣ"), bstack1ll1ll1111_opy_)
          BrowserType.connect = bstack1llll11l1l_opy_
          return
        BrowserType.launch = bstack111l1l111_opy_
        bstack1ll11ll111_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1lllll1l1_opy_
      bstack1ll11ll111_opy_ = True
    except Exception as e:
      pass
def bstack11l11111l_opy_(context, bstack1lll11lll_opy_):
  try:
    context.page.evaluate(bstack1l11ll1_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣଽ"), bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬା")+ json.dumps(bstack1lll11lll_opy_) + bstack1l11ll1_opy_ (u"ࠤࢀࢁࠧି"))
  except Exception as e:
    logger.debug(bstack1l11ll1_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽ࠻ࠢࡾࢁࠧୀ").format(str(e), traceback.format_exc()))
def bstack1l11l1ll1_opy_(context, message, level):
  try:
    context.page.evaluate(bstack1l11ll1_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧୁ"), bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪୂ") + json.dumps(message) + bstack1l11ll1_opy_ (u"࠭ࠬࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠩୃ") + json.dumps(level) + bstack1l11ll1_opy_ (u"ࠧࡾࡿࠪୄ"))
  except Exception as e:
    logger.debug(bstack1l11ll1_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡࡽࢀ࠾ࠥࢁࡽࠣ୅").format(str(e), traceback.format_exc()))
@measure(event_name=EVENTS.bstack1l1111l1l_opy_, stage=STAGE.bstack11lllll111_opy_, bstack1l11111l1_opy_=bstack1l11111l1l_opy_)
def bstack1l111ll1ll_opy_(self, url):
  global bstack11lll1ll1_opy_
  try:
    bstack1l11l111_opy_(url)
  except Exception as err:
    logger.debug(bstack11llll1ll1_opy_.format(str(err)))
  try:
    bstack11lll1ll1_opy_(self, url)
  except Exception as e:
    try:
      bstack1l1lllll_opy_ = str(e)
      if any(err_msg in bstack1l1lllll_opy_ for err_msg in bstack1ll11ll1_opy_):
        bstack1l11l111_opy_(url, True)
    except Exception as err:
      logger.debug(bstack11llll1ll1_opy_.format(str(err)))
    raise e
def bstack1ll11l1lll_opy_(self):
  global bstack1lllll1ll1_opy_
  bstack1lllll1ll1_opy_ = self
  return
def bstack1ll11111l_opy_(self):
  global bstack1l111111_opy_
  bstack1l111111_opy_ = self
  return
def bstack1llllllll1_opy_(test_name, bstack11ll1l11_opy_):
  global CONFIG
  if percy.bstack1ll1l11111_opy_() == bstack1l11ll1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ୆"):
    bstack1llllllll_opy_ = os.path.relpath(bstack11ll1l11_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack1llllllll_opy_)
    bstack1l11111l1_opy_ = suite_name + bstack1l11ll1_opy_ (u"ࠥ࠱ࠧେ") + test_name
    threading.current_thread().percySessionName = bstack1l11111l1_opy_
def bstack1l1l11l1ll_opy_(self, test, *args, **kwargs):
  global bstack1ll11l111l_opy_
  test_name = None
  bstack11ll1l11_opy_ = None
  if test:
    test_name = str(test.name)
    bstack11ll1l11_opy_ = str(test.source)
  bstack1llllllll1_opy_(test_name, bstack11ll1l11_opy_)
  bstack1ll11l111l_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.bstack11l111ll11_opy_, stage=STAGE.bstack11lllll111_opy_, bstack1l11111l1_opy_=bstack1l11111l1l_opy_)
def bstack1lll1l11ll_opy_(driver, bstack1l11111l1_opy_):
  if not bstack1ll11111ll_opy_ and bstack1l11111l1_opy_:
      bstack1ll1ll11_opy_ = {
          bstack1l11ll1_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫୈ"): bstack1l11ll1_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭୉"),
          bstack1l11ll1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ୊"): {
              bstack1l11ll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬୋ"): bstack1l11111l1_opy_
          }
      }
      bstack11111ll11_opy_ = bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ୌ").format(json.dumps(bstack1ll1ll11_opy_))
      driver.execute_script(bstack11111ll11_opy_)
  if bstack1llll11l1_opy_:
      bstack11llll1l1l_opy_ = {
          bstack1l11ll1_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯୍ࠩ"): bstack1l11ll1_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬ୎"),
          bstack1l11ll1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ୏"): {
              bstack1l11ll1_opy_ (u"ࠬࡪࡡࡵࡣࠪ୐"): bstack1l11111l1_opy_ + bstack1l11ll1_opy_ (u"࠭ࠠࡱࡣࡶࡷࡪࡪࠡࠨ୑"),
              bstack1l11ll1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭୒"): bstack1l11ll1_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭୓")
          }
      }
      if bstack1llll11l1_opy_.status == bstack1l11ll1_opy_ (u"ࠩࡓࡅࡘ࡙ࠧ୔"):
          bstack1l1llll1_opy_ = bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨ୕").format(json.dumps(bstack11llll1l1l_opy_))
          driver.execute_script(bstack1l1llll1_opy_)
          bstack1l1l111l1_opy_(driver, bstack1l11ll1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫୖ"))
      elif bstack1llll11l1_opy_.status == bstack1l11ll1_opy_ (u"ࠬࡌࡁࡊࡎࠪୗ"):
          reason = bstack1l11ll1_opy_ (u"ࠨࠢ୘")
          bstack111l11111_opy_ = bstack1l11111l1_opy_ + bstack1l11ll1_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠨ୙")
          if bstack1llll11l1_opy_.message:
              reason = str(bstack1llll11l1_opy_.message)
              bstack111l11111_opy_ = bstack111l11111_opy_ + bstack1l11ll1_opy_ (u"ࠨࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࡀࠠࠨ୚") + reason
          bstack11llll1l1l_opy_[bstack1l11ll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ୛")] = {
              bstack1l11ll1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩଡ଼"): bstack1l11ll1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪଢ଼"),
              bstack1l11ll1_opy_ (u"ࠬࡪࡡࡵࡣࠪ୞"): bstack111l11111_opy_
          }
          bstack1l1llll1_opy_ = bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫୟ").format(json.dumps(bstack11llll1l1l_opy_))
          driver.execute_script(bstack1l1llll1_opy_)
          bstack1l1l111l1_opy_(driver, bstack1l11ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧୠ"), reason)
          bstack11ll11111l_opy_(reason, str(bstack1llll11l1_opy_), str(bstack11ll1llll_opy_), logger)
@measure(event_name=EVENTS.bstack1ll11l1ll_opy_, stage=STAGE.bstack11lllll111_opy_, bstack1l11111l1_opy_=bstack1l11111l1l_opy_)
def bstack111llll111_opy_(driver, test):
  if percy.bstack1ll1l11111_opy_() == bstack1l11ll1_opy_ (u"ࠣࡶࡵࡹࡪࠨୡ") and percy.bstack11l1111l11_opy_() == bstack1l11ll1_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦୢ"):
      bstack1l1l1lll_opy_ = bstack1l11111ll_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠪࡴࡪࡸࡣࡺࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ୣ"), None)
      bstack1llll1ll_opy_(driver, bstack1l1l1lll_opy_, test)
  if (bstack1l11111ll_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ୤"), None) and
      bstack1l11111ll_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ୥"), None)) or (
      bstack1l11111ll_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭୦"), None) and
      bstack1l11111ll_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ୧"), None)):
      logger.info(bstack1l11ll1_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠦࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡ࡫ࡶࠤࡺࡴࡤࡦࡴࡺࡥࡾ࠴ࠠࠣ୨"))
      bstack11lll1ll1l_opy_.bstack1l1ll1111_opy_(driver, name=test.name, path=test.source)
def bstack1lllllll1l_opy_(test, bstack1l11111l1_opy_):
    try:
      bstack1l11ll1ll_opy_ = datetime.datetime.now()
      data = {}
      if test:
        data[bstack1l11ll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ୩")] = bstack1l11111l1_opy_
      if bstack1llll11l1_opy_:
        if bstack1llll11l1_opy_.status == bstack1l11ll1_opy_ (u"ࠪࡔࡆ࡙ࡓࠨ୪"):
          data[bstack1l11ll1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ୫")] = bstack1l11ll1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ୬")
        elif bstack1llll11l1_opy_.status == bstack1l11ll1_opy_ (u"࠭ࡆࡂࡋࡏࠫ୭"):
          data[bstack1l11ll1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ୮")] = bstack1l11ll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ୯")
          if bstack1llll11l1_opy_.message:
            data[bstack1l11ll1_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩ୰")] = str(bstack1llll11l1_opy_.message)
      user = CONFIG[bstack1l11ll1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬୱ")]
      key = CONFIG[bstack1l11ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ୲")]
      host = bstack1ll1111l1l_opy_(cli.config, [bstack1l11ll1_opy_ (u"ࠧࡧࡰࡪࡵࠥ୳"), bstack1l11ll1_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥࠣ୴"), bstack1l11ll1_opy_ (u"ࠢࡢࡲ࡬ࠦ୵")], bstack1l11ll1_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠤ୶"))
      url = bstack1l11ll1_opy_ (u"ࠩࡾࢁ࠴ࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡴࡧࡶࡷ࡮ࡵ࡮ࡴ࠱ࡾࢁ࠳ࡰࡳࡰࡰࠪ୷").format(host, bstack1l111l1lll_opy_)
      headers = {
        bstack1l11ll1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩ୸"): bstack1l11ll1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ୹"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers, auth=(user, key))
        cli.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽ࡹࡵࡪࡡࡵࡧࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡸࡦࡺࡵࡴࠤ୺"), datetime.datetime.now() - bstack1l11ll1ll_opy_)
    except Exception as e:
      logger.error(bstack11llll11l1_opy_.format(str(e)))
def bstack1l1l1l1l1l_opy_(test, bstack1l11111l1_opy_):
  global CONFIG
  global bstack1l111111_opy_
  global bstack1lllll1ll1_opy_
  global bstack1l111l1lll_opy_
  global bstack1llll11l1_opy_
  global bstack1l11111l1l_opy_
  global bstack1ll111lll1_opy_
  global bstack1l1ll11111_opy_
  global bstack11ll1llll1_opy_
  global bstack1ll111111_opy_
  global bstack11l11lll1l_opy_
  global bstack11ll1l1ll1_opy_
  global bstack11l1l11l1l_opy_
  try:
    if not bstack1l111l1lll_opy_:
      with bstack11l1l11l1l_opy_:
        bstack1ll1lll1l_opy_ = os.path.join(os.path.expanduser(bstack1l11ll1_opy_ (u"࠭ࡾࠨ୻")), bstack1l11ll1_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ୼"), bstack1l11ll1_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪ୽"))
        if os.path.exists(bstack1ll1lll1l_opy_):
          with open(bstack1ll1lll1l_opy_, bstack1l11ll1_opy_ (u"ࠩࡵࠫ୾")) as f:
            content = f.read().strip()
            if content:
              bstack1lll1l11l1_opy_ = json.loads(bstack1l11ll1_opy_ (u"ࠥࡿࠧ୿") + content + bstack1l11ll1_opy_ (u"ࠫࠧࡾࠢ࠻ࠢࠥࡽࠧ࠭஀") + bstack1l11ll1_opy_ (u"ࠧࢃࠢ஁"))
              bstack1l111l1lll_opy_ = bstack1lll1l11l1_opy_.get(str(threading.get_ident()))
  except Exception as e:
    logger.debug(bstack1l11ll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡸࡥࡢࡦ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡊࡆࡶࠤ࡫࡯࡬ࡦ࠼ࠣࠫஂ") + str(e))
  if bstack11l11lll1l_opy_:
    with bstack111ll111_opy_:
      bstack11l1l11ll1_opy_ = bstack11l11lll1l_opy_.copy()
    for driver in bstack11l1l11ll1_opy_:
      if bstack1l111l1lll_opy_ == driver.session_id:
        if test:
          bstack111llll111_opy_(driver, test)
        bstack1lll1l11ll_opy_(driver, bstack1l11111l1_opy_)
  elif bstack1l111l1lll_opy_:
    bstack1lllllll1l_opy_(test, bstack1l11111l1_opy_)
  if bstack1l111111_opy_:
    bstack1l1ll11111_opy_(bstack1l111111_opy_)
  if bstack1lllll1ll1_opy_:
    bstack11ll1llll1_opy_(bstack1lllll1ll1_opy_)
  if bstack1l1ll1ll11_opy_:
    bstack1ll111111_opy_()
def bstack11l1ll1l11_opy_(self, test, *args, **kwargs):
  bstack1l11111l1_opy_ = None
  if test:
    bstack1l11111l1_opy_ = str(test.name)
  bstack1l1l1l1l1l_opy_(test, bstack1l11111l1_opy_)
  bstack1ll111lll1_opy_(self, test, *args, **kwargs)
def bstack11ll1l1111_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack11l111l1_opy_
  global CONFIG
  global bstack11l11lll1l_opy_
  global bstack1l111l1lll_opy_
  global bstack11l1l11l1l_opy_
  bstack1l1l11l11_opy_ = None
  try:
    if bstack1l11111ll_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ஃ"), None) or bstack1l11111ll_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ஄"), None):
      try:
        if not bstack1l111l1lll_opy_:
          bstack1ll1lll1l_opy_ = os.path.join(os.path.expanduser(bstack1l11ll1_opy_ (u"ࠩࢁࠫஅ")), bstack1l11ll1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪஆ"), bstack1l11ll1_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭இ"))
          with bstack11l1l11l1l_opy_:
            if os.path.exists(bstack1ll1lll1l_opy_):
              with open(bstack1ll1lll1l_opy_, bstack1l11ll1_opy_ (u"ࠬࡸࠧஈ")) as f:
                content = f.read().strip()
                if content:
                  bstack1lll1l11l1_opy_ = json.loads(bstack1l11ll1_opy_ (u"ࠨࡻࠣஉ") + content + bstack1l11ll1_opy_ (u"ࠧࠣࡺࠥ࠾ࠥࠨࡹࠣࠩஊ") + bstack1l11ll1_opy_ (u"ࠣࡿࠥ஋"))
                  bstack1l111l1lll_opy_ = bstack1lll1l11l1_opy_.get(str(threading.get_ident()))
      except Exception as e:
        logger.debug(bstack1l11ll1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡴࡨࡥࡩ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡍࡉࡹࠠࡧ࡫࡯ࡩࠥ࡯࡮ࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࡀࠠࠨ஌") + str(e))
      if bstack11l11lll1l_opy_:
        with bstack111ll111_opy_:
          bstack11l1l11ll1_opy_ = bstack11l11lll1l_opy_.copy()
        for driver in bstack11l1l11ll1_opy_:
          if bstack1l111l1lll_opy_ == driver.session_id:
            bstack1l1l11l11_opy_ = driver
    bstack11llll11l_opy_ = bstack11lll1ll1l_opy_.bstack11l1lllll_opy_(test.tags)
    if bstack1l1l11l11_opy_:
      threading.current_thread().isA11yTest = bstack11lll1ll1l_opy_.bstack1lllll11_opy_(bstack1l1l11l11_opy_, bstack11llll11l_opy_)
      threading.current_thread().isAppA11yTest = bstack11lll1ll1l_opy_.bstack1lllll11_opy_(bstack1l1l11l11_opy_, bstack11llll11l_opy_)
    else:
      threading.current_thread().isA11yTest = bstack11llll11l_opy_
      threading.current_thread().isAppA11yTest = bstack11llll11l_opy_
  except:
    pass
  bstack11l111l1_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1llll11l1_opy_
  try:
    bstack1llll11l1_opy_ = self._test
  except:
    bstack1llll11l1_opy_ = self.test
def bstack111lll11l_opy_():
  global bstack1ll11l11ll_opy_
  try:
    if os.path.exists(bstack1ll11l11ll_opy_):
      os.remove(bstack1ll11l11ll_opy_)
  except Exception as e:
    logger.debug(bstack1l11ll1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭஍") + str(e))
def bstack1ll1l111l1_opy_():
  global bstack1ll11l11ll_opy_
  bstack1l1l11ll11_opy_ = {}
  lock_file = bstack1ll11l11ll_opy_ + bstack1l11ll1_opy_ (u"ࠫ࠳ࡲ࡯ࡤ࡭ࠪஎ")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l11ll1_opy_ (u"ࠬ࡬ࡩ࡭ࡧ࡯ࡳࡨࡱࠠ࡯ࡱࡷࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠬࠡࡷࡶ࡭ࡳ࡭ࠠࡣࡣࡶ࡭ࡨࠦࡦࡪ࡮ࡨࠤࡴࡶࡥࡳࡣࡷ࡭ࡴࡴࡳࠨஏ"))
    try:
      if not os.path.isfile(bstack1ll11l11ll_opy_):
        with open(bstack1ll11l11ll_opy_, bstack1l11ll1_opy_ (u"࠭ࡷࠨஐ")) as f:
          json.dump({}, f)
      if os.path.exists(bstack1ll11l11ll_opy_):
        with open(bstack1ll11l11ll_opy_, bstack1l11ll1_opy_ (u"ࠧࡳࠩ஑")) as f:
          content = f.read().strip()
          if content:
            bstack1l1l11ll11_opy_ = json.loads(content)
    except Exception as e:
      logger.debug(bstack1l11ll1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡶࡪࡧࡤࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪஒ") + str(e))
    return bstack1l1l11ll11_opy_
  try:
    os.makedirs(os.path.dirname(bstack1ll11l11ll_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      if not os.path.isfile(bstack1ll11l11ll_opy_):
        with open(bstack1ll11l11ll_opy_, bstack1l11ll1_opy_ (u"ࠩࡺࠫஓ")) as f:
          json.dump({}, f)
      if os.path.exists(bstack1ll11l11ll_opy_):
        with open(bstack1ll11l11ll_opy_, bstack1l11ll1_opy_ (u"ࠪࡶࠬஔ")) as f:
          content = f.read().strip()
          if content:
            bstack1l1l11ll11_opy_ = json.loads(content)
  except Exception as e:
    logger.debug(bstack1l11ll1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡲࡦࡣࡧ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭க") + str(e))
  finally:
    return bstack1l1l11ll11_opy_
def bstack1ll11l11l_opy_(platform_index, item_index):
  global bstack1ll11l11ll_opy_
  lock_file = bstack1ll11l11ll_opy_ + bstack1l11ll1_opy_ (u"ࠬ࠴࡬ࡰࡥ࡮ࠫ஖")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l11ll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡰࡴࡩ࡫ࠡࡰࡲࡸࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥ࠭ࠢࡸࡷ࡮ࡴࡧࠡࡤࡤࡷ࡮ࡩࠠࡧ࡫࡯ࡩࠥࡵࡰࡦࡴࡤࡸ࡮ࡵ࡮ࡴࠩ஗"))
    try:
      bstack1l1l11ll11_opy_ = {}
      if os.path.exists(bstack1ll11l11ll_opy_):
        with open(bstack1ll11l11ll_opy_, bstack1l11ll1_opy_ (u"ࠧࡳࠩ஘")) as f:
          content = f.read().strip()
          if content:
            bstack1l1l11ll11_opy_ = json.loads(content)
      bstack1l1l11ll11_opy_[item_index] = platform_index
      with open(bstack1ll11l11ll_opy_, bstack1l11ll1_opy_ (u"ࠣࡹࠥங")) as outfile:
        json.dump(bstack1l1l11ll11_opy_, outfile)
    except Exception as e:
      logger.debug(bstack1l11ll1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡼࡸࡩࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧச") + str(e))
    return
  try:
    os.makedirs(os.path.dirname(bstack1ll11l11ll_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      bstack1l1l11ll11_opy_ = {}
      if os.path.exists(bstack1ll11l11ll_opy_):
        with open(bstack1ll11l11ll_opy_, bstack1l11ll1_opy_ (u"ࠪࡶࠬ஛")) as f:
          content = f.read().strip()
          if content:
            bstack1l1l11ll11_opy_ = json.loads(content)
      bstack1l1l11ll11_opy_[item_index] = platform_index
      with open(bstack1ll11l11ll_opy_, bstack1l11ll1_opy_ (u"ࠦࡼࠨஜ")) as outfile:
        json.dump(bstack1l1l11ll11_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1l11ll1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡸࡴ࡬ࡸ࡮ࡴࡧࠡࡶࡲࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪ஝") + str(e))
def bstack1l11l1ll1l_opy_(bstack1l1l11l1_opy_):
  global CONFIG
  bstack11l111l1l1_opy_ = bstack1l11ll1_opy_ (u"࠭ࠧஞ")
  if not bstack1l11ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪட") in CONFIG:
    logger.info(bstack1l11ll1_opy_ (u"ࠨࡐࡲࠤࡵࡲࡡࡵࡨࡲࡶࡲࡹࠠࡱࡣࡶࡷࡪࡪࠠࡶࡰࡤࡦࡱ࡫ࠠࡵࡱࠣ࡫ࡪࡴࡥࡳࡣࡷࡩࠥࡸࡥࡱࡱࡵࡸࠥ࡬࡯ࡳࠢࡕࡳࡧࡵࡴࠡࡴࡸࡲࠬ஠"))
  try:
    platform = CONFIG[bstack1l11ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ஡")][bstack1l1l11l1_opy_]
    if bstack1l11ll1_opy_ (u"ࠪࡳࡸ࠭஢") in platform:
      bstack11l111l1l1_opy_ += str(platform[bstack1l11ll1_opy_ (u"ࠫࡴࡹࠧண")]) + bstack1l11ll1_opy_ (u"ࠬ࠲ࠠࠨத")
    if bstack1l11ll1_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ஥") in platform:
      bstack11l111l1l1_opy_ += str(platform[bstack1l11ll1_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪ஦")]) + bstack1l11ll1_opy_ (u"ࠨ࠮ࠣࠫ஧")
    if bstack1l11ll1_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ந") in platform:
      bstack11l111l1l1_opy_ += str(platform[bstack1l11ll1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧன")]) + bstack1l11ll1_opy_ (u"ࠫ࠱ࠦࠧப")
    if bstack1l11ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ஫") in platform:
      bstack11l111l1l1_opy_ += str(platform[bstack1l11ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ஬")]) + bstack1l11ll1_opy_ (u"ࠧ࠭ࠢࠪ஭")
    if bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ம") in platform:
      bstack11l111l1l1_opy_ += str(platform[bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧய")]) + bstack1l11ll1_opy_ (u"ࠪ࠰ࠥ࠭ர")
    if bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬற") in platform:
      bstack11l111l1l1_opy_ += str(platform[bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ல")]) + bstack1l11ll1_opy_ (u"࠭ࠬࠡࠩள")
  except Exception as e:
    logger.debug(bstack1l11ll1_opy_ (u"ࠧࡔࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡱࡩࡷࡧࡴࡪࡰࡪࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡳࡵࡴ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡶࡪࡶ࡯ࡳࡶࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡴࡴࠧழ") + str(e))
  finally:
    if bstack11l111l1l1_opy_[len(bstack11l111l1l1_opy_) - 2:] == bstack1l11ll1_opy_ (u"ࠨ࠮ࠣࠫவ"):
      bstack11l111l1l1_opy_ = bstack11l111l1l1_opy_[:-2]
    return bstack11l111l1l1_opy_
def bstack1l1l111lll_opy_(path, bstack11l111l1l1_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1l11lllll1_opy_ = ET.parse(path)
    bstack11ll1l111_opy_ = bstack1l11lllll1_opy_.getroot()
    bstack111ll11ll_opy_ = None
    for suite in bstack11ll1l111_opy_.iter(bstack1l11ll1_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨஶ")):
      if bstack1l11ll1_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪஷ") in suite.attrib:
        suite.attrib[bstack1l11ll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩஸ")] += bstack1l11ll1_opy_ (u"ࠬࠦࠧஹ") + bstack11l111l1l1_opy_
        bstack111ll11ll_opy_ = suite
    bstack1l1lll11_opy_ = None
    for robot in bstack11ll1l111_opy_.iter(bstack1l11ll1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ஺")):
      bstack1l1lll11_opy_ = robot
    bstack1l11l11l1_opy_ = len(bstack1l1lll11_opy_.findall(bstack1l11ll1_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭஻")))
    if bstack1l11l11l1_opy_ == 1:
      bstack1l1lll11_opy_.remove(bstack1l1lll11_opy_.findall(bstack1l11ll1_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧ஼"))[0])
      bstack11l1l1lll1_opy_ = ET.Element(bstack1l11ll1_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨ஽"), attrib={bstack1l11ll1_opy_ (u"ࠪࡲࡦࡳࡥࠨா"): bstack1l11ll1_opy_ (u"ࠫࡘࡻࡩࡵࡧࡶࠫி"), bstack1l11ll1_opy_ (u"ࠬ࡯ࡤࠨீ"): bstack1l11ll1_opy_ (u"࠭ࡳ࠱ࠩு")})
      bstack1l1lll11_opy_.insert(1, bstack11l1l1lll1_opy_)
      bstack11lll1ll_opy_ = None
      for suite in bstack1l1lll11_opy_.iter(bstack1l11ll1_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭ூ")):
        bstack11lll1ll_opy_ = suite
      bstack11lll1ll_opy_.append(bstack111ll11ll_opy_)
      bstack1ll111ll1_opy_ = None
      for status in bstack111ll11ll_opy_.iter(bstack1l11ll1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ௃")):
        bstack1ll111ll1_opy_ = status
      bstack11lll1ll_opy_.append(bstack1ll111ll1_opy_)
    bstack1l11lllll1_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1l11ll1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡲࡴ࡫ࡱ࡫ࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠧ௄") + str(e))
def bstack1l1lll11l1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1l1l1l1l_opy_
  global CONFIG
  if bstack1l11ll1_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࡳࡥࡹ࡮ࠢ௅") in options:
    del options[bstack1l11ll1_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡴࡦࡺࡨࠣெ")]
  bstack1lll111ll1_opy_ = bstack1ll1l111l1_opy_()
  for item_id in bstack1lll111ll1_opy_.keys():
    path = os.path.join(os.getcwd(), bstack1l11ll1_opy_ (u"ࠬࡶࡡࡣࡱࡷࡣࡷ࡫ࡳࡶ࡮ࡷࡷࠬே"), str(item_id), bstack1l11ll1_opy_ (u"࠭࡯ࡶࡶࡳࡹࡹ࠴ࡸ࡮࡮ࠪை"))
    bstack1l1l111lll_opy_(path, bstack1l11l1ll1l_opy_(bstack1lll111ll1_opy_[item_id]))
  bstack111lll11l_opy_()
  return bstack1l1l1l1l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1lll11ll11_opy_(self, ff_profile_dir):
  global bstack1111l1l1l_opy_
  if not ff_profile_dir:
    return None
  return bstack1111l1l1l_opy_(self, ff_profile_dir)
def bstack11llll11_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1l1111111l_opy_
  bstack1lll11l11_opy_ = []
  if bstack1l11ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ௉") in CONFIG:
    bstack1lll11l11_opy_ = CONFIG[bstack1l11ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫொ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1l11ll1_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࠥோ")],
      pabot_args[bstack1l11ll1_opy_ (u"ࠥࡺࡪࡸࡢࡰࡵࡨࠦௌ")],
      argfile,
      pabot_args.get(bstack1l11ll1_opy_ (u"ࠦ࡭࡯ࡶࡦࠤ்")),
      pabot_args[bstack1l11ll1_opy_ (u"ࠧࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠣ௎")],
      platform[0],
      bstack1l1111111l_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1l11ll1_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡧ࡫࡯ࡩࡸࠨ௏")] or [(bstack1l11ll1_opy_ (u"ࠢࠣௐ"), None)]
    for platform in enumerate(bstack1lll11l11_opy_)
  ]
def bstack1l11ll111_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1lll1111_opy_=bstack1l11ll1_opy_ (u"ࠨࠩ௑")):
  global bstack11l1l11l1_opy_
  self.platform_index = platform_index
  self.bstack11l11l11_opy_ = bstack1lll1111_opy_
  bstack11l1l11l1_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1l11lll1l_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack11ll111111_opy_
  global bstack1lll1ll11l_opy_
  bstack1l1l1llll_opy_ = copy.deepcopy(item)
  if not bstack1l11ll1_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ௒") in item.options:
    bstack1l1l1llll_opy_.options[bstack1l11ll1_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ௓")] = []
  bstack1l1l11ll1_opy_ = bstack1l1l1llll_opy_.options[bstack1l11ll1_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭௔")].copy()
  for v in bstack1l1l1llll_opy_.options[bstack1l11ll1_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ௕")]:
    if bstack1l11ll1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬ௖") in v:
      bstack1l1l11ll1_opy_.remove(v)
    if bstack1l11ll1_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙ࠧௗ") in v:
      bstack1l1l11ll1_opy_.remove(v)
    if bstack1l11ll1_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡅࡇࡉࡐࡔࡉࡁࡍࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬ௘") in v:
      bstack1l1l11ll1_opy_.remove(v)
  bstack1l1l11ll1_opy_.insert(0, bstack1l11ll1_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘ࠻ࡽࢀࠫ௙").format(bstack1l1l1llll_opy_.platform_index))
  bstack1l1l11ll1_opy_.insert(0, bstack1l11ll1_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡇࡉࡋࡒࡏࡄࡃࡏࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘ࠺ࡼࡿࠪ௚").format(bstack1l1l1llll_opy_.bstack11l11l11_opy_))
  bstack1l1l1llll_opy_.options[bstack1l11ll1_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭௛")] = bstack1l1l11ll1_opy_
  if bstack1lll1ll11l_opy_:
    bstack1l1l1llll_opy_.options[bstack1l11ll1_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ௜")].insert(0, bstack1l11ll1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘࡀࡻࡾࠩ௝").format(bstack1lll1ll11l_opy_))
  return bstack11ll111111_opy_(caller_id, datasources, is_last, bstack1l1l1llll_opy_, outs_dir)
def bstack111llllll1_opy_(command, item_index):
  try:
    if bstack111lllll11_opy_.get_property(bstack1l11ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ௞")):
      os.environ[bstack1l11ll1_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩ௟")] = json.dumps(CONFIG[bstack1l11ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ௠")][item_index % bstack11l1l11ll_opy_])
    global bstack1lll1ll11l_opy_
    if bstack1lll1ll11l_opy_:
      command[0] = command[0].replace(bstack1l11ll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ௡"), bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡷࡩࡱࠠࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠡ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠠࠨ௢") + str(
        item_index) + bstack1l11ll1_opy_ (u"ࠬࠦࠧ௣") + bstack1lll1ll11l_opy_, 1)
    else:
      command[0] = command[0].replace(bstack1l11ll1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ௤"),
                                      bstack1l11ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡳࡥ࡭ࠣࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠤ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠣࠫ௥") + str(item_index), 1)
  except Exception as e:
    logger.error(bstack1l11ll1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠ࡮ࡱࡧ࡭࡫ࡿࡩ࡯ࡩࠣࡧࡴࡳ࡭ࡢࡰࡧࠤ࡫ࡵࡲࠡࡲࡤࡦࡴࡺࠠࡳࡷࡱ࠾ࠥࢁࡽࠨ௦").format(str(e)))
def bstack1l1llll11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1l1ll111l_opy_
  try:
    bstack111llllll1_opy_(command, item_index)
    return bstack1l1ll111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
  except Exception as e:
    logger.error(bstack1l11ll1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡢࡰࡶࠣࡶࡺࡴ࠺ࠡࡽࢀࠫ௧").format(str(e)))
    raise e
def bstack1l1l1l1111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1l1ll111l_opy_
  try:
    bstack111llllll1_opy_(command, item_index)
    return bstack1l1ll111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
  except Exception as e:
    logger.error(bstack1l11ll1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡣࡱࡷࠤࡷࡻ࡮ࠡ࠴࠱࠵࠸ࡀࠠࡼࡿࠪ௨").format(str(e)))
    try:
      return bstack1l1ll111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
    except Exception as e2:
      logger.error(bstack1l11ll1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡢࡤࡲࡸࠥ࠸࠮࠲࠵ࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࡻࡾࠩ௩").format(str(e2)))
      raise e
def bstack11l1l11l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1l1ll111l_opy_
  try:
    bstack111llllll1_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    return bstack1l1ll111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
  except Exception as e:
    logger.error(bstack1l11ll1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡥࡳࡹࠦࡲࡶࡰࠣ࠶࠳࠷࠵࠻ࠢࡾࢁࠬ௪").format(str(e)))
    try:
      return bstack1l1ll111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
    except Exception as e2:
      logger.error(bstack1l11ll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠ࠳࠰࠴࠹ࠥ࡬ࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࡽࢀࠫ௫").format(str(e2)))
      raise e
def _1lll1l111_opy_(bstack1lll11ll_opy_, item_index, process_timeout, sleep_before_start, bstack11l1111l1_opy_):
  bstack111llllll1_opy_(bstack1lll11ll_opy_, item_index)
  if process_timeout is None:
    process_timeout = 3600
  if sleep_before_start and sleep_before_start > 0:
    time.sleep(min(sleep_before_start, 5))
  return process_timeout
def bstack11l11l1ll_opy_(command, bstack1l1l1lllll_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack1l1ll111l_opy_
  try:
    bstack111llllll1_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    if sleep_before_start and sleep_before_start > 0:
      time.sleep(min(sleep_before_start, 5))
    return bstack1l1ll111l_opy_(command, bstack1l1l1lllll_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack1l11ll1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡧࡵࡴࠡࡴࡸࡲࠥ࠻࠮࠱࠼ࠣࡿࢂ࠭௬").format(str(e)))
    try:
      return bstack1l1ll111l_opy_(command, bstack1l1l1lllll_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack1l11ll1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡦࡨ࡯ࡵࠢࡩࡥࡱࡲࡢࡢࡥ࡮࠾ࠥࢁࡽࠨ௭").format(str(e2)))
      raise e
def bstack1l1l11l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack1l1ll111l_opy_
  try:
    process_timeout = _1lll1l111_opy_(command, item_index, process_timeout, sleep_before_start, bstack1l11ll1_opy_ (u"ࠩ࠷࠲࠷࠭௮"))
    return bstack1l1ll111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack1l11ll1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡣࡱࡷࠤࡷࡻ࡮ࠡ࠶࠱࠶࠿ࠦࡻࡾࠩ௯").format(str(e)))
    try:
      return bstack1l1ll111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack1l11ll1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡢࡤࡲࡸࠥ࡬ࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࡽࢀࠫ௰").format(str(e2)))
      raise e
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack1l1l11ll1l_opy_(self, runner, quiet=False, capture=True):
  global bstack1l1lll11l_opy_
  bstack1l1ll111ll_opy_ = bstack1l1lll11l_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack1l11ll1_opy_ (u"ࠬ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࡠࡣࡵࡶࠬ௱")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1l11ll1_opy_ (u"࠭ࡥࡹࡥࡢࡸࡷࡧࡣࡦࡤࡤࡧࡰࡥࡡࡳࡴࠪ௲")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1l1ll111ll_opy_
def bstack1lll11l1ll_opy_(runner, hook_name, context, element, bstack11l1ll1ll1_opy_, *args):
  try:
    if runner.hooks.get(hook_name):
      bstack1lllll1111_opy_.bstack1ll1ll1l_opy_(hook_name, element)
    bstack11l1ll1ll1_opy_(runner, hook_name, context, *args)
    if runner.hooks.get(hook_name):
      bstack1lllll1111_opy_.bstack1l11l1l1l1_opy_(element)
      if hook_name not in [bstack1l11ll1_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠫ௳"), bstack1l11ll1_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠫ௴")] and args and hasattr(args[0], bstack1l11ll1_opy_ (u"ࠩࡨࡶࡷࡵࡲࡠ࡯ࡨࡷࡸࡧࡧࡦࠩ௵")):
        args[0].error_message = bstack1l11ll1_opy_ (u"ࠪࠫ௶")
  except Exception as e:
    logger.debug(bstack1l11ll1_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡩࡣࡱࡨࡱ࡫ࠠࡩࡱࡲ࡯ࡸࠦࡩ࡯ࠢࡥࡩ࡭ࡧࡶࡦ࠼ࠣࡿࢂ࠭௷").format(str(e)))
@measure(event_name=EVENTS.bstack1l111ll1_opy_, stage=STAGE.bstack11lllll111_opy_, hook_type=bstack1l11ll1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡆࡲ࡬ࠣ௸"), bstack1l11111l1_opy_=bstack1l11111l1l_opy_)
def bstack11ll11111_opy_(runner, name, context, bstack11l1ll1ll1_opy_, *args):
    if runner.hooks.get(bstack1l11ll1_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥ௹")).__name__ != bstack1l11ll1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࡣࡩ࡫ࡦࡢࡷ࡯ࡸࡤ࡮࡯ࡰ࡭ࠥ௺"):
      bstack1lll11l1ll_opy_(runner, name, context, runner, bstack11l1ll1ll1_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack1ll1l1ll1_opy_(bstack1l11ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ௻")) else context.browser
      runner.driver_initialised = bstack1l11ll1_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨ௼")
    except Exception as e:
      logger.debug(bstack1l11ll1_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡨࡷ࡯ࡶࡦࡴࠣ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡸ࡫ࠠࡢࡶࡷࡶ࡮ࡨࡵࡵࡧ࠽ࠤࢀࢃࠧ௽").format(str(e)))
def bstack1lllllll11_opy_(runner, name, context, bstack11l1ll1ll1_opy_, *args):
    bstack1lll11l1ll_opy_(runner, name, context, context.feature, bstack11l1ll1ll1_opy_, *args)
    try:
      if not bstack1ll11111ll_opy_:
        bstack1l1l11l11_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll1l1ll1_opy_(bstack1l11ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ௾")) else context.browser
        if is_driver_active(bstack1l1l11l11_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack1l11ll1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨ௿")
          bstack1lll11lll_opy_ = str(runner.feature.name)
          bstack11l11111l_opy_(context, bstack1lll11lll_opy_)
          bstack1l1l11l11_opy_.execute_script(bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫఀ") + json.dumps(bstack1lll11lll_opy_) + bstack1l11ll1_opy_ (u"ࠧࡾࡿࠪఁ"))
    except Exception as e:
      logger.debug(bstack1l11ll1_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨం").format(str(e)))
def bstack1llll1ll11_opy_(runner, name, context, bstack11l1ll1ll1_opy_, *args):
    if hasattr(context, bstack1l11ll1_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫః")):
        bstack1lllll1111_opy_.start_test(context)
    target = context.scenario if hasattr(context, bstack1l11ll1_opy_ (u"ࠪࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬఄ")) else context.feature
    bstack1lll11l1ll_opy_(runner, name, context, target, bstack11l1ll1ll1_opy_, *args)
@measure(event_name=EVENTS.bstack11111l11l_opy_, stage=STAGE.bstack11lllll111_opy_, bstack1l11111l1_opy_=bstack1l11111l1l_opy_)
def bstack1ll111l1_opy_(runner, name, context, bstack11l1ll1ll1_opy_, *args):
    if len(context.scenario.tags) == 0: bstack1lllll1111_opy_.start_test(context)
    bstack1lll11l1ll_opy_(runner, name, context, context.scenario, bstack11l1ll1ll1_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack11ll11ll_opy_.bstack11111111l_opy_(context, *args)
    try:
      bstack1l1l11l11_opy_ = bstack1l11111ll_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪఅ"), context.browser)
      if is_driver_active(bstack1l1l11l11_opy_):
        bstack1l111111l1_opy_.bstack111llllll_opy_(bstack1l11111ll_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫఆ"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack1l11ll1_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣఇ")
        if (not bstack1ll11111ll_opy_):
          scenario_name = args[0].name
          feature_name = bstack1lll11lll_opy_ = str(runner.feature.name)
          bstack1lll11lll_opy_ = feature_name + bstack1l11ll1_opy_ (u"ࠧࠡ࠯ࠣࠫఈ") + scenario_name
          if runner.driver_initialised == bstack1l11ll1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥఉ"):
            bstack11l11111l_opy_(context, bstack1lll11lll_opy_)
            bstack1l1l11l11_opy_.execute_script(bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧఊ") + json.dumps(bstack1lll11lll_opy_) + bstack1l11ll1_opy_ (u"ࠪࢁࢂ࠭ఋ"))
    except Exception as e:
      logger.debug(bstack1l11ll1_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣ࡭ࡳࠦࡢࡦࡨࡲࡶࡪࠦࡳࡤࡧࡱࡥࡷ࡯࡯࠻ࠢࡾࢁࠬఌ").format(str(e)))
@measure(event_name=EVENTS.bstack1l111ll1_opy_, stage=STAGE.bstack11lllll111_opy_, hook_type=bstack1l11ll1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡘࡺࡥࡱࠤ఍"), bstack1l11111l1_opy_=bstack1l11111l1l_opy_)
def bstack1ll1ll11l1_opy_(runner, name, context, bstack11l1ll1ll1_opy_, *args):
    bstack1lll11l1ll_opy_(runner, name, context, args[0], bstack11l1ll1ll1_opy_, *args)
    try:
      bstack1l1l11l11_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll1l1ll1_opy_(bstack1l11ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬఎ")) else context.browser
      if is_driver_active(bstack1l1l11l11_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack1l11ll1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧఏ")
        bstack1lllll1111_opy_.bstack1llll11lll_opy_(args[0])
        if runner.driver_initialised == bstack1l11ll1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨఐ"):
          feature_name = bstack1lll11lll_opy_ = str(runner.feature.name)
          bstack1lll11lll_opy_ = feature_name + bstack1l11ll1_opy_ (u"ࠩࠣ࠱ࠥ࠭఑") + context.scenario.name
          bstack1l1l11l11_opy_.execute_script(bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨఒ") + json.dumps(bstack1lll11lll_opy_) + bstack1l11ll1_opy_ (u"ࠫࢂࢃࠧఓ"))
    except Exception as e:
      logger.debug(bstack1l11ll1_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤ࡮ࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡶࡨࡴ࠿ࠦࡻࡾࠩఔ").format(str(e)))
@measure(event_name=EVENTS.bstack1l111ll1_opy_, stage=STAGE.bstack11lllll111_opy_, hook_type=bstack1l11ll1_opy_ (u"ࠨࡡࡧࡶࡨࡶࡘࡺࡥࡱࠤక"), bstack1l11111l1_opy_=bstack1l11111l1l_opy_)
def bstack1llll1l1l_opy_(runner, name, context, bstack11l1ll1ll1_opy_, *args):
  bstack1lllll1111_opy_.bstack1ll1l1111l_opy_(args[0])
  try:
    step_status = args[0].status.name
    bstack1l1l11l11_opy_ = threading.current_thread().bstackSessionDriver if bstack1l11ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ఖ") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack1l1l11l11_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack1l11ll1_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨగ")
        feature_name = bstack1lll11lll_opy_ = str(runner.feature.name)
        bstack1lll11lll_opy_ = feature_name + bstack1l11ll1_opy_ (u"ࠩࠣ࠱ࠥ࠭ఘ") + context.scenario.name
        bstack1l1l11l11_opy_.execute_script(bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨఙ") + json.dumps(bstack1lll11lll_opy_) + bstack1l11ll1_opy_ (u"ࠫࢂࢃࠧచ"))
    if str(step_status).lower() == bstack1l11ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬఛ"):
      bstack11l1ll1lll_opy_ = bstack1l11ll1_opy_ (u"࠭ࠧజ")
      bstack11l1lll1l_opy_ = bstack1l11ll1_opy_ (u"ࠧࠨఝ")
      bstack1lll11111l_opy_ = bstack1l11ll1_opy_ (u"ࠨࠩఞ")
      try:
        import traceback
        bstack11l1ll1lll_opy_ = runner.exception.__class__.__name__
        bstack1l1l111ll_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack11l1lll1l_opy_ = bstack1l11ll1_opy_ (u"ࠩࠣࠫట").join(bstack1l1l111ll_opy_)
        bstack1lll11111l_opy_ = bstack1l1l111ll_opy_[-1]
      except Exception as e:
        logger.debug(bstack111l1lll_opy_.format(str(e)))
      bstack11l1ll1lll_opy_ += bstack1lll11111l_opy_
      bstack1l11l1ll1_opy_(context, json.dumps(str(args[0].name) + bstack1l11ll1_opy_ (u"ࠥࠤ࠲ࠦࡆࡢ࡫࡯ࡩࡩࠧ࡜࡯ࠤఠ") + str(bstack11l1lll1l_opy_)),
                          bstack1l11ll1_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥడ"))
      if runner.driver_initialised == bstack1l11ll1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥఢ"):
        bstack1llllll11l_opy_(getattr(context, bstack1l11ll1_opy_ (u"࠭ࡰࡢࡩࡨࠫణ"), None), bstack1l11ll1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢత"), bstack11l1ll1lll_opy_)
        bstack1l1l11l11_opy_.execute_script(bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭థ") + json.dumps(str(args[0].name) + bstack1l11ll1_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣద") + str(bstack11l1lll1l_opy_)) + bstack1l11ll1_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪధ"))
      if runner.driver_initialised == bstack1l11ll1_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤన"):
        bstack1l1l111l1_opy_(bstack1l1l11l11_opy_, bstack1l11ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ఩"), bstack1l11ll1_opy_ (u"ࠨࡓࡤࡧࡱࡥࡷ࡯࡯ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥప") + str(bstack11l1ll1lll_opy_))
    else:
      bstack1l11l1ll1_opy_(context, bstack1l11ll1_opy_ (u"ࠢࡑࡣࡶࡷࡪࡪࠡࠣఫ"), bstack1l11ll1_opy_ (u"ࠣ࡫ࡱࡪࡴࠨబ"))
      if runner.driver_initialised == bstack1l11ll1_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢభ"):
        bstack1llllll11l_opy_(getattr(context, bstack1l11ll1_opy_ (u"ࠪࡴࡦ࡭ࡥࠨమ"), None), bstack1l11ll1_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦయ"))
      bstack1l1l11l11_opy_.execute_script(bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪర") + json.dumps(str(args[0].name) + bstack1l11ll1_opy_ (u"ࠨࠠ࠮ࠢࡓࡥࡸࡹࡥࡥࠣࠥఱ")) + bstack1l11ll1_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥࢁࢂ࠭ల"))
      if runner.driver_initialised == bstack1l11ll1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨళ"):
        bstack1l1l111l1_opy_(bstack1l1l11l11_opy_, bstack1l11ll1_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤఴ"))
  except Exception as e:
    logger.debug(bstack1l11ll1_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡯࡮ࠡࡣࡩࡸࡪࡸࠠࡴࡶࡨࡴ࠿ࠦࡻࡾࠩవ").format(str(e)))
  bstack1lll11l1ll_opy_(runner, name, context, args[0], bstack11l1ll1ll1_opy_, *args)
@measure(event_name=EVENTS.bstack1ll111l1l1_opy_, stage=STAGE.bstack11lllll111_opy_, bstack1l11111l1_opy_=bstack1l11111l1l_opy_)
def bstack1111lll1l_opy_(runner, name, context, bstack11l1ll1ll1_opy_, *args):
  bstack1lllll1111_opy_.end_test(args[0])
  try:
    bstack11ll111l11_opy_ = args[0].status.name
    bstack1l1l11l11_opy_ = bstack1l11111ll_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪశ"), context.browser)
    bstack11ll11ll_opy_.bstack1111111l1_opy_(bstack1l1l11l11_opy_)
    if str(bstack11ll111l11_opy_).lower() == bstack1l11ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬష"):
      bstack11l1ll1lll_opy_ = bstack1l11ll1_opy_ (u"࠭ࠧస")
      bstack11l1lll1l_opy_ = bstack1l11ll1_opy_ (u"ࠧࠨహ")
      bstack1lll11111l_opy_ = bstack1l11ll1_opy_ (u"ࠨࠩ఺")
      try:
        import traceback
        bstack11l1ll1lll_opy_ = runner.exception.__class__.__name__
        bstack1l1l111ll_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack11l1lll1l_opy_ = bstack1l11ll1_opy_ (u"ࠩࠣࠫ఻").join(bstack1l1l111ll_opy_)
        bstack1lll11111l_opy_ = bstack1l1l111ll_opy_[-1]
      except Exception as e:
        logger.debug(bstack111l1lll_opy_.format(str(e)))
      bstack11l1ll1lll_opy_ += bstack1lll11111l_opy_
      bstack1l11l1ll1_opy_(context, json.dumps(str(args[0].name) + bstack1l11ll1_opy_ (u"ࠥࠤ࠲ࠦࡆࡢ࡫࡯ࡩࡩࠧ࡜࡯ࠤ఼") + str(bstack11l1lll1l_opy_)),
                          bstack1l11ll1_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥఽ"))
      if runner.driver_initialised == bstack1l11ll1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢా") or runner.driver_initialised == bstack1l11ll1_opy_ (u"࠭ࡩ࡯ࡵࡷࡩࡵ࠭ి"):
        bstack1llllll11l_opy_(getattr(context, bstack1l11ll1_opy_ (u"ࠧࡱࡣࡪࡩࠬీ"), None), bstack1l11ll1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣు"), bstack11l1ll1lll_opy_)
        bstack1l1l11l11_opy_.execute_script(bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧూ") + json.dumps(str(args[0].name) + bstack1l11ll1_opy_ (u"ࠥࠤ࠲ࠦࡆࡢ࡫࡯ࡩࡩࠧ࡜࡯ࠤృ") + str(bstack11l1lll1l_opy_)) + bstack1l11ll1_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣࡿࢀࠫౄ"))
      if runner.driver_initialised == bstack1l11ll1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢ౅") or runner.driver_initialised == bstack1l11ll1_opy_ (u"࠭ࡩ࡯ࡵࡷࡩࡵ࠭ె"):
        bstack1l1l111l1_opy_(bstack1l1l11l11_opy_, bstack1l11ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧే"), bstack1l11ll1_opy_ (u"ࠣࡕࡦࡩࡳࡧࡲࡪࡱࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧై") + str(bstack11l1ll1lll_opy_))
    else:
      bstack1l11l1ll1_opy_(context, bstack1l11ll1_opy_ (u"ࠤࡓࡥࡸࡹࡥࡥࠣࠥ౉"), bstack1l11ll1_opy_ (u"ࠥ࡭ࡳ࡬࡯ࠣొ"))
      if runner.driver_initialised == bstack1l11ll1_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨో") or runner.driver_initialised == bstack1l11ll1_opy_ (u"ࠬ࡯࡮ࡴࡶࡨࡴࠬౌ"):
        bstack1llllll11l_opy_(getattr(context, bstack1l11ll1_opy_ (u"࠭ࡰࡢࡩࡨ్ࠫ"), None), bstack1l11ll1_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ౎"))
      bstack1l1l11l11_opy_.execute_script(bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭౏") + json.dumps(str(args[0].name) + bstack1l11ll1_opy_ (u"ࠤࠣ࠱ࠥࡖࡡࡴࡵࡨࡨࠦࠨ౐")) + bstack1l11ll1_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩ౑"))
      if runner.driver_initialised == bstack1l11ll1_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨ౒") or runner.driver_initialised == bstack1l11ll1_opy_ (u"ࠬ࡯࡮ࡴࡶࡨࡴࠬ౓"):
        bstack1l1l111l1_opy_(bstack1l1l11l11_opy_, bstack1l11ll1_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ౔"))
  except Exception as e:
    logger.debug(bstack1l11ll1_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾౕࠩ").format(str(e)))
  bstack1lll11l1ll_opy_(runner, name, context, context.scenario, bstack11l1ll1ll1_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack1111ll1ll_opy_(runner, name, context, bstack11l1ll1ll1_opy_, *args):
    target = context.scenario if hasattr(context, bstack1l11ll1_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱౖࠪ")) else context.feature
    bstack1lll11l1ll_opy_(runner, name, context, target, bstack11l1ll1ll1_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack11l11l11l1_opy_(runner, name, context, bstack11l1ll1ll1_opy_, *args):
    try:
      bstack1l1l11l11_opy_ = bstack1l11111ll_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ౗"), context.browser)
      bstack1lll1l1ll1_opy_ = bstack1l11ll1_opy_ (u"ࠪࠫౘ")
      if context.failed is True:
        bstack11111l1l1_opy_ = []
        bstack1ll1l11ll1_opy_ = []
        bstack11l1llll11_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack11111l1l1_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1l1l111ll_opy_ = traceback.format_tb(exc_tb)
            bstack11ll11lll1_opy_ = bstack1l11ll1_opy_ (u"ࠫࠥ࠭ౙ").join(bstack1l1l111ll_opy_)
            bstack1ll1l11ll1_opy_.append(bstack11ll11lll1_opy_)
            bstack11l1llll11_opy_.append(bstack1l1l111ll_opy_[-1])
        except Exception as e:
          logger.debug(bstack111l1lll_opy_.format(str(e)))
        bstack11l1ll1lll_opy_ = bstack1l11ll1_opy_ (u"ࠬ࠭ౚ")
        for i in range(len(bstack11111l1l1_opy_)):
          bstack11l1ll1lll_opy_ += bstack11111l1l1_opy_[i] + bstack11l1llll11_opy_[i] + bstack1l11ll1_opy_ (u"࠭࡜࡯ࠩ౛")
        bstack1lll1l1ll1_opy_ = bstack1l11ll1_opy_ (u"ࠧࠡࠩ౜").join(bstack1ll1l11ll1_opy_)
        if runner.driver_initialised in [bstack1l11ll1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠤౝ"), bstack1l11ll1_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨ౞")]:
          bstack1l11l1ll1_opy_(context, bstack1lll1l1ll1_opy_, bstack1l11ll1_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤ౟"))
          bstack1llllll11l_opy_(getattr(context, bstack1l11ll1_opy_ (u"ࠫࡵࡧࡧࡦࠩౠ"), None), bstack1l11ll1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧౡ"), bstack11l1ll1lll_opy_)
          bstack1l1l11l11_opy_.execute_script(bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫౢ") + json.dumps(bstack1lll1l1ll1_opy_) + bstack1l11ll1_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦࢂࢃࠧౣ"))
          bstack1l1l111l1_opy_(bstack1l1l11l11_opy_, bstack1l11ll1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ౤"), bstack1l11ll1_opy_ (u"ࠤࡖࡳࡲ࡫ࠠࡴࡥࡨࡲࡦࡸࡩࡰࡵࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࡡࡴࠢ౥") + str(bstack11l1ll1lll_opy_))
          bstack1ll1111l_opy_ = bstack11ll1lll1l_opy_(bstack1lll1l1ll1_opy_, runner.feature.name, logger)
          if (bstack1ll1111l_opy_ != None):
            bstack1l1lll1l1l_opy_.append(bstack1ll1111l_opy_)
      else:
        if runner.driver_initialised in [bstack1l11ll1_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦ౦"), bstack1l11ll1_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣ౧")]:
          bstack1l11l1ll1_opy_(context, bstack1l11ll1_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࡀࠠࠣ౨") + str(runner.feature.name) + bstack1l11ll1_opy_ (u"ࠨࠠࡱࡣࡶࡷࡪࡪࠡࠣ౩"), bstack1l11ll1_opy_ (u"ࠢࡪࡰࡩࡳࠧ౪"))
          bstack1llllll11l_opy_(getattr(context, bstack1l11ll1_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭౫"), None), bstack1l11ll1_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ౬"))
          bstack1l1l11l11_opy_.execute_script(bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨ౭") + json.dumps(bstack1l11ll1_opy_ (u"ࠦࡋ࡫ࡡࡵࡷࡵࡩ࠿ࠦࠢ౮") + str(runner.feature.name) + bstack1l11ll1_opy_ (u"ࠧࠦࡰࡢࡵࡶࡩࡩࠧࠢ౯")) + bstack1l11ll1_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤࢀࢁࠬ౰"))
          bstack1l1l111l1_opy_(bstack1l1l11l11_opy_, bstack1l11ll1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ౱"))
          bstack1ll1111l_opy_ = bstack11ll1lll1l_opy_(bstack1lll1l1ll1_opy_, runner.feature.name, logger)
          if (bstack1ll1111l_opy_ != None):
            bstack1l1lll1l1l_opy_.append(bstack1ll1111l_opy_)
    except Exception as e:
      logger.debug(bstack1l11ll1_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࠥ࡬ࡥࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪ౲").format(str(e)))
    bstack1lll11l1ll_opy_(runner, name, context, context.feature, bstack11l1ll1ll1_opy_, *args)
@measure(event_name=EVENTS.bstack1l111ll1_opy_, stage=STAGE.bstack11lllll111_opy_, hook_type=bstack1l11ll1_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࡂ࡮࡯ࠦ౳"), bstack1l11111l1_opy_=bstack1l11111l1l_opy_)
def bstack1llll1111l_opy_(runner, name, context, bstack11l1ll1ll1_opy_, *args):
    bstack1lll11l1ll_opy_(runner, name, context, runner, bstack11l1ll1ll1_opy_, *args)
def bstack1l11ll111l_opy_(self, name, context, *args):
  try:
    if bstack1111lll1_opy_:
      platform_index = int(threading.current_thread()._name) % bstack11l1l11ll_opy_
      bstack11l1ll1l_opy_ = CONFIG[bstack1l11ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭౴")][platform_index]
      os.environ[bstack1l11ll1_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬ౵")] = json.dumps(bstack11l1ll1l_opy_)
    global bstack11l1ll1ll1_opy_
    if not hasattr(self, bstack1l11ll1_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡳࡦࡦࠪ౶")):
      self.driver_initialised = None
    bstack11l11lll1_opy_ = {
        bstack1l11ll1_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠪ౷"): bstack11ll11111_opy_,
        bstack1l11ll1_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠨ౸"): bstack1lllllll11_opy_,
        bstack1l11ll1_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡶࡤ࡫ࠬ౹"): bstack1llll1ll11_opy_,
        bstack1l11ll1_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ౺"): bstack1ll111l1_opy_,
        bstack1l11ll1_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠨ౻"): bstack1ll1ll11l1_opy_,
        bstack1l11ll1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡹ࡫ࡰࠨ౼"): bstack1llll1l1l_opy_,
        bstack1l11ll1_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭౽"): bstack1111lll1l_opy_,
        bstack1l11ll1_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡺࡡࡨࠩ౾"): bstack1111ll1ll_opy_,
        bstack1l11ll1_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡦࡦࡣࡷࡹࡷ࡫ࠧ౿"): bstack11l11l11l1_opy_,
        bstack1l11ll1_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠫಀ"): bstack1llll1111l_opy_
    }
    handler = bstack11l11lll1_opy_.get(name, bstack11l1ll1ll1_opy_)
    try:
      handler(self, name, context, bstack11l1ll1ll1_opy_, *args)
    except Exception as e:
      logger.debug(bstack1l11ll1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡧ࡫ࡨࡢࡸࡨࠤ࡭ࡵ࡯࡬ࠢ࡫ࡥࡳࡪ࡬ࡦࡴࠣࡿࢂࡀࠠࡼࡿࠪಁ").format(name, str(e)))
    if name in [bstack1l11ll1_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪಂ"), bstack1l11ll1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬಃ"), bstack1l11ll1_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠨ಄")]:
      try:
        bstack1l1l11l11_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll1l1ll1_opy_(bstack1l11ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬಅ")) else context.browser
        bstack11l1ll111_opy_ = (
          (name == bstack1l11ll1_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪಆ") and self.driver_initialised == bstack1l11ll1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧಇ")) or
          (name == bstack1l11ll1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠩಈ") and self.driver_initialised == bstack1l11ll1_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦಉ")) or
          (name == bstack1l11ll1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬಊ") and self.driver_initialised in [bstack1l11ll1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢಋ"), bstack1l11ll1_opy_ (u"ࠨࡩ࡯ࡵࡷࡩࡵࠨಌ")]) or
          (name == bstack1l11ll1_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡵࡧࡳࠫ಍") and self.driver_initialised == bstack1l11ll1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨಎ"))
        )
        if bstack11l1ll111_opy_:
          self.driver_initialised = None
          if bstack1l1l11l11_opy_ and hasattr(bstack1l1l11l11_opy_, bstack1l11ll1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩ࠭ಏ")):
            try:
              bstack1l1l11l11_opy_.quit()
            except Exception as e:
              logger.debug(bstack1l11ll1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡴࡹ࡮ࡺࡴࡪࡰࡪࠤࡩࡸࡩࡷࡧࡵࠤ࡮ࡴࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡩࡱࡲ࡯࠿ࠦࡻࡾࠩಐ").format(str(e)))
      except Exception as e:
        logger.debug(bstack1l11ll1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࠥ࡮࡯ࡰ࡭ࠣࡧࡱ࡫ࡡ࡯ࡷࡳࠤ࡫ࡵࡲࠡࡽࢀ࠾ࠥࢁࡽࠨ಑").format(name, str(e)))
  except Exception as e:
    logger.debug(bstack1l11ll1_opy_ (u"ࠬࡉࡲࡪࡶ࡬ࡧࡦࡲࠠࡦࡴࡵࡳࡷࠦࡩ࡯ࠢࡥࡩ࡭ࡧࡶࡦࠢࡵࡹࡳࠦࡨࡰࡱ࡮ࠤࢀࢃ࠺ࠡࡽࢀࠫಒ").format(name, str(e)))
    try:
      bstack11l1ll1ll1_opy_(self, name, context, *args)
    except Exception as e2:
      logger.debug(bstack1l11ll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡨࡤࡰࡱࡨࡡࡤ࡭ࠣࡳࡷ࡯ࡧࡪࡰࡤࡰࠥࡨࡥࡩࡣࡹࡩࠥ࡮࡯ࡰ࡭ࠣࡿࢂࡀࠠࡼࡿࠪಓ").format(name, str(e2)))
def bstack1l111l1ll1_opy_(config, startdir):
  return bstack1l11ll1_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࠳ࢁࠧಔ").format(bstack1l11ll1_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢಕ"))
notset = Notset()
def bstack11ll1l1ll_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1lll1llll_opy_
  if str(name).lower() == bstack1l11ll1_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࠩಖ"):
    return bstack1l11ll1_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤಗ")
  else:
    return bstack1lll1llll_opy_(self, name, default, skip)
def bstack11l1l111l_opy_(item, when):
  global bstack111l11l11_opy_
  try:
    bstack111l11l11_opy_(item, when)
  except Exception as e:
    pass
def bstack11lllll1_opy_():
  return
def bstack1ll1llllll_opy_(type, name, status, reason, bstack11l1l11l_opy_, bstack1l1ll1l11_opy_):
  bstack1ll1ll11_opy_ = {
    bstack1l11ll1_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫಘ"): type,
    bstack1l11ll1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨಙ"): {}
  }
  if type == bstack1l11ll1_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨಚ"):
    bstack1ll1ll11_opy_[bstack1l11ll1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪಛ")][bstack1l11ll1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧಜ")] = bstack11l1l11l_opy_
    bstack1ll1ll11_opy_[bstack1l11ll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬಝ")][bstack1l11ll1_opy_ (u"ࠪࡨࡦࡺࡡࠨಞ")] = json.dumps(str(bstack1l1ll1l11_opy_))
  if type == bstack1l11ll1_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬಟ"):
    bstack1ll1ll11_opy_[bstack1l11ll1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨಠ")][bstack1l11ll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫಡ")] = name
  if type == bstack1l11ll1_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪಢ"):
    bstack1ll1ll11_opy_[bstack1l11ll1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫಣ")][bstack1l11ll1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩತ")] = status
    if status == bstack1l11ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪಥ"):
      bstack1ll1ll11_opy_[bstack1l11ll1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧದ")][bstack1l11ll1_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬಧ")] = json.dumps(str(reason))
  bstack11111ll11_opy_ = bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫನ").format(json.dumps(bstack1ll1ll11_opy_))
  return bstack11111ll11_opy_
def bstack11lll1l11_opy_(driver_command, response):
    if driver_command == bstack1l11ll1_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫ಩"):
        bstack1l111111l1_opy_.bstack1l1l1111ll_opy_({
            bstack1l11ll1_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧಪ"): response[bstack1l11ll1_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨಫ")],
            bstack1l11ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪಬ"): bstack1l111111l1_opy_.current_test_uuid()
        })
def bstack111llll1ll_opy_(item, call, rep):
  global bstack1111l1ll1_opy_
  global bstack11l11lll1l_opy_
  global bstack1ll11111ll_opy_
  name = bstack1l11ll1_opy_ (u"ࠫࠬಭ")
  try:
    if rep.when == bstack1l11ll1_opy_ (u"ࠬࡩࡡ࡭࡮ࠪಮ"):
      bstack1l111l1lll_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1ll11111ll_opy_:
          name = str(rep.nodeid)
          bstack11llllll_opy_ = bstack1ll1llllll_opy_(bstack1l11ll1_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧಯ"), name, bstack1l11ll1_opy_ (u"ࠧࠨರ"), bstack1l11ll1_opy_ (u"ࠨࠩಱ"), bstack1l11ll1_opy_ (u"ࠩࠪಲ"), bstack1l11ll1_opy_ (u"ࠪࠫಳ"))
          threading.current_thread().bstack11ll11lll_opy_ = name
          for driver in bstack11l11lll1l_opy_:
            if bstack1l111l1lll_opy_ == driver.session_id:
              driver.execute_script(bstack11llllll_opy_)
      except Exception as e:
        logger.debug(bstack1l11ll1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫ಴").format(str(e)))
      try:
        bstack111ll1l1l_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack1l11ll1_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ವ"):
          status = bstack1l11ll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ಶ") if rep.outcome.lower() == bstack1l11ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧಷ") else bstack1l11ll1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨಸ")
          reason = bstack1l11ll1_opy_ (u"ࠩࠪಹ")
          if status == bstack1l11ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ಺"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack1l11ll1_opy_ (u"ࠫ࡮ࡴࡦࡰࠩ಻") if status == bstack1l11ll1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨ಼ࠬ") else bstack1l11ll1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬಽ")
          data = name + bstack1l11ll1_opy_ (u"ࠧࠡࡲࡤࡷࡸ࡫ࡤࠢࠩಾ") if status == bstack1l11ll1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨಿ") else name + bstack1l11ll1_opy_ (u"ࠩࠣࡪࡦ࡯࡬ࡦࡦࠤࠤࠬೀ") + reason
          bstack1l1l1111l_opy_ = bstack1ll1llllll_opy_(bstack1l11ll1_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬು"), bstack1l11ll1_opy_ (u"ࠫࠬೂ"), bstack1l11ll1_opy_ (u"ࠬ࠭ೃ"), bstack1l11ll1_opy_ (u"࠭ࠧೄ"), level, data)
          for driver in bstack11l11lll1l_opy_:
            if bstack1l111l1lll_opy_ == driver.session_id:
              driver.execute_script(bstack1l1l1111l_opy_)
      except Exception as e:
        logger.debug(bstack1l11ll1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡨࡵ࡮ࡵࡧࡻࡸࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫ೅").format(str(e)))
  except Exception as e:
    logger.debug(bstack1l11ll1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡸࡺࡡࡵࡧࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾࢁࠬೆ").format(str(e)))
  bstack1111l1ll1_opy_(item, call, rep)
def bstack1llll1ll_opy_(driver, bstack1l1l1ll111_opy_, test=None):
  global bstack11ll1llll_opy_
  if test != None:
    bstack1llllll1l1_opy_ = getattr(test, bstack1l11ll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧೇ"), None)
    bstack1ll111ll1l_opy_ = getattr(test, bstack1l11ll1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨೈ"), None)
    PercySDK.screenshot(driver, bstack1l1l1ll111_opy_, bstack1llllll1l1_opy_=bstack1llllll1l1_opy_, bstack1ll111ll1l_opy_=bstack1ll111ll1l_opy_, bstack1ll11l11_opy_=bstack11ll1llll_opy_)
  else:
    PercySDK.screenshot(driver, bstack1l1l1ll111_opy_)
@measure(event_name=EVENTS.bstack1lll1lll_opy_, stage=STAGE.bstack11lllll111_opy_, bstack1l11111l1_opy_=bstack1l11111l1l_opy_)
def bstack11l111l11_opy_(driver):
  if bstack11ll11ll1l_opy_.bstack11lll1l1l1_opy_() is True or bstack11ll11ll1l_opy_.capturing() is True:
    return
  bstack11ll11ll1l_opy_.bstack1ll1llll11_opy_()
  while not bstack11ll11ll1l_opy_.bstack11lll1l1l1_opy_():
    bstack11ll11l11_opy_ = bstack11ll11ll1l_opy_.bstack1ll111l1ll_opy_()
    bstack1llll1ll_opy_(driver, bstack11ll11l11_opy_)
  bstack11ll11ll1l_opy_.bstack1llll1l1_opy_()
def bstack11l1l1l1_opy_(sequence, driver_command, response = None, bstack111l11l1_opy_ = None, args = None):
    try:
      if sequence != bstack1l11ll1_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫ೉"):
        return
      if percy.bstack1ll1l11111_opy_() == bstack1l11ll1_opy_ (u"ࠧ࡬ࡡ࡭ࡵࡨࠦೊ"):
        return
      bstack11ll11l11_opy_ = bstack1l11111ll_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"࠭ࡰࡦࡴࡦࡽࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩೋ"), None)
      for command in bstack111l1ll11_opy_:
        if command == driver_command:
          with bstack111ll111_opy_:
            bstack11l1l11ll1_opy_ = bstack11l11lll1l_opy_.copy()
          for driver in bstack11l1l11ll1_opy_:
            bstack11l111l11_opy_(driver)
      bstack1ll111l111_opy_ = percy.bstack11l1111l11_opy_()
      if driver_command in bstack111ll11l1_opy_[bstack1ll111l111_opy_]:
        bstack11ll11ll1l_opy_.bstack11111111_opy_(bstack11ll11l11_opy_, driver_command)
    except Exception as e:
      pass
def bstack11l11llll1_opy_(framework_name):
  if bstack111lllll11_opy_.get_property(bstack1l11ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟࡮ࡱࡧࡣࡨࡧ࡬࡭ࡧࡧࠫೌ")):
      return
  bstack111lllll11_opy_.bstack11l111l1ll_opy_(bstack1l11ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨ್ࠬ"), True)
  global bstack11ll1l1l11_opy_
  global bstack1ll11ll111_opy_
  global bstack1l1l1ll1l1_opy_
  bstack11ll1l1l11_opy_ = framework_name
  logger.info(bstack1l1ll1llll_opy_.format(bstack11ll1l1l11_opy_.split(bstack1l11ll1_opy_ (u"ࠩ࠰ࠫ೎"))[0]))
  bstack11l1111l1l_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1111lll1_opy_:
      Service.start = bstack11111ll1_opy_
      Service.stop = bstack1lll111l1_opy_
      webdriver.Remote.get = bstack1l111ll1ll_opy_
      WebDriver.quit = bstack11ll1l1l_opy_
      webdriver.Remote.__init__ = bstack11lllll11_opy_
    if not bstack1111lll1_opy_:
        webdriver.Remote.__init__ = bstack111lll11_opy_
    WebDriver.getAccessibilityResults = getAccessibilityResults
    WebDriver.get_accessibility_results = getAccessibilityResults
    WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
    WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
    WebDriver.performScan = perform_scan
    WebDriver.perform_scan = perform_scan
    WebDriver.execute = bstack1l1l1l11_opy_
    bstack1ll11ll111_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack1111lll1_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1lll1ll1ll_opy_
  except Exception as e:
    pass
  bstack1ll1l1l111_opy_()
  if not bstack1ll11ll111_opy_:
    bstack11l1l1ll_opy_(bstack1l11ll1_opy_ (u"ࠥࡔࡦࡩ࡫ࡢࡩࡨࡷࠥࡴ࡯ࡵࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠧ೏"), bstack1l11ll1l11_opy_)
  if bstack1llllll111_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      if hasattr(RemoteConnection, bstack1l11ll1_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬ೐")) and callable(getattr(RemoteConnection, bstack1l11ll1_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭೑"))):
        RemoteConnection._get_proxy_url = bstack1lllll1ll_opy_
      else:
        from selenium.webdriver.remote.client_config import ClientConfig
        ClientConfig.get_proxy_url = bstack1lllll1ll_opy_
    except Exception as e:
      logger.error(bstack111llll11l_opy_.format(str(e)))
  if bstack11l1l1ll1_opy_():
    bstack1l1ll111_opy_(CONFIG, logger)
  if (bstack1l11ll1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ೒") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if percy.bstack1ll1l11111_opy_() == bstack1l11ll1_opy_ (u"ࠢࡵࡴࡸࡩࠧ೓"):
          bstack1ll1l11l11_opy_(bstack11l1l1l1_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1lll11ll11_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1ll11111l_opy_
      except Exception as e:
        logger.warn(bstack11l11l1ll1_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1ll11l1lll_opy_
      except Exception as e:
        logger.debug(bstack111lll1ll_opy_ + str(e))
    except Exception as e:
      bstack11l1l1ll_opy_(e, bstack11l11l1ll1_opy_)
    Output.start_test = bstack1l1l11l1ll_opy_
    Output.end_test = bstack11l1ll1l11_opy_
    TestStatus.__init__ = bstack11ll1l1111_opy_
    QueueItem.__init__ = bstack1l11ll111_opy_
    pabot._create_items = bstack11llll11_opy_
    try:
      from pabot import __version__ as bstack11ll1l11l1_opy_
      if version.parse(bstack11ll1l11l1_opy_) >= version.parse(bstack1l11ll1_opy_ (u"ࠨ࠷࠱࠴࠳࠶ࠧ೔")):
        pabot._run = bstack11l11l1ll_opy_
      elif version.parse(bstack11ll1l11l1_opy_) >= version.parse(bstack1l11ll1_opy_ (u"ࠩ࠷࠲࠷࠴࠰ࠨೕ")):
        pabot._run = bstack1l1l11l1l_opy_
      elif version.parse(bstack11ll1l11l1_opy_) >= version.parse(bstack1l11ll1_opy_ (u"ࠪ࠶࠳࠷࠵࠯࠲ࠪೖ")):
        pabot._run = bstack11l1l11l11_opy_
      elif version.parse(bstack11ll1l11l1_opy_) >= version.parse(bstack1l11ll1_opy_ (u"ࠫ࠷࠴࠱࠴࠰࠳ࠫ೗")):
        pabot._run = bstack1l1l1l1111_opy_
      else:
        pabot._run = bstack1l1llll11l_opy_
    except Exception as e:
      pabot._run = bstack1l1llll11l_opy_
    pabot._create_command_for_execution = bstack1l11lll1l_opy_
    pabot._report_results = bstack1l1lll11l1_opy_
  if bstack1l11ll1_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ೘") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11l1l1ll_opy_(e, bstack1111l11ll_opy_)
    Runner.run_hook = bstack1l11ll111l_opy_
    Step.run = bstack1l1l11ll1l_opy_
  if bstack1l11ll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭೙") in str(framework_name).lower():
    if not bstack1111lll1_opy_:
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack1l111l1ll1_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack11lllll1_opy_
      Config.getoption = bstack11ll1l1ll_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack111llll1ll_opy_
    except Exception as e:
      pass
def bstack11lll1l1l_opy_():
  global CONFIG
  if bstack1l11ll1_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ೚") in CONFIG and int(CONFIG[bstack1l11ll1_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ೛")]) > 1:
    logger.warn(bstack111l1111l_opy_)
def bstack1l1llll1ll_opy_(arg, bstack111lllllll_opy_, bstack11ll1ll1_opy_=None):
  global CONFIG
  global bstack11lll1ll11_opy_
  global bstack1lllll11l_opy_
  global bstack1111lll1_opy_
  global bstack111lllll11_opy_
  bstack11ll111ll_opy_ = bstack1l11ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ೜")
  if bstack111lllllll_opy_ and isinstance(bstack111lllllll_opy_, str):
    bstack111lllllll_opy_ = eval(bstack111lllllll_opy_)
  CONFIG = bstack111lllllll_opy_[bstack1l11ll1_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪೝ")]
  bstack11lll1ll11_opy_ = bstack111lllllll_opy_[bstack1l11ll1_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬೞ")]
  bstack1lllll11l_opy_ = bstack111lllllll_opy_[bstack1l11ll1_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ೟")]
  bstack1111lll1_opy_ = bstack111lllllll_opy_[bstack1l11ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩೠ")]
  bstack111lllll11_opy_.bstack11l111l1ll_opy_(bstack1l11ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨೡ"), bstack1111lll1_opy_)
  os.environ[bstack1l11ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪೢ")] = bstack11ll111ll_opy_
  os.environ[bstack1l11ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࠨೣ")] = json.dumps(CONFIG)
  os.environ[bstack1l11ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡋ࡙ࡇࡥࡕࡓࡎࠪ೤")] = bstack11lll1ll11_opy_
  os.environ[bstack1l11ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ೥")] = str(bstack1lllll11l_opy_)
  os.environ[bstack1l11ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡒࡕࡈࡋࡑࠫ೦")] = str(True)
  if bstack11ll1111l1_opy_(arg, [bstack1l11ll1_opy_ (u"࠭࠭࡯ࠩ೧"), bstack1l11ll1_opy_ (u"ࠧ࠮࠯ࡱࡹࡲࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨ೨")]) != -1:
    os.environ[bstack1l11ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡃࡕࡅࡑࡒࡅࡍࠩ೩")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack11ll11l1l1_opy_)
    return
  bstack11l1ll11_opy_()
  global bstack11ll11ll1_opy_
  global bstack11ll1llll_opy_
  global bstack1l1111111l_opy_
  global bstack1lll1ll11l_opy_
  global bstack11l1111l_opy_
  global bstack1l1l1ll1l1_opy_
  global bstack11llll111_opy_
  arg.append(bstack1l11ll1_opy_ (u"ࠤ࠰࡛ࠧ೪"))
  arg.append(bstack1l11ll1_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧ࠽ࡑࡴࡪࡵ࡭ࡧࠣࡥࡱࡸࡥࡢࡦࡼࠤ࡮ࡳࡰࡰࡴࡷࡩࡩࡀࡰࡺࡶࡨࡷࡹ࠴ࡐࡺࡶࡨࡷࡹ࡝ࡡࡳࡰ࡬ࡲ࡬ࠨ೫"))
  arg.append(bstack1l11ll1_opy_ (u"ࠦ࠲࡝ࠢ೬"))
  arg.append(bstack1l11ll1_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩ࠿࡚ࡨࡦࠢ࡫ࡳࡴࡱࡩ࡮ࡲ࡯ࠦ೭"))
  global bstack1ll11lll_opy_
  global bstack1l1l1ll1_opy_
  global bstack1ll1l111ll_opy_
  global bstack11l111l1_opy_
  global bstack1111l1l1l_opy_
  global bstack11l1l11l1_opy_
  global bstack11ll111111_opy_
  global bstack111lll111_opy_
  global bstack11lll1ll1_opy_
  global bstack11ll11l1l_opy_
  global bstack1lll1llll_opy_
  global bstack111l11l11_opy_
  global bstack1111l1ll1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1ll11lll_opy_ = webdriver.Remote.__init__
    bstack1l1l1ll1_opy_ = WebDriver.quit
    bstack111lll111_opy_ = WebDriver.close
    bstack11lll1ll1_opy_ = WebDriver.get
    bstack1ll1l111ll_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1l111ll11_opy_(CONFIG) and bstack1l11l1l1ll_opy_():
    if bstack11llll11ll_opy_() < version.parse(bstack1ll1l11l1_opy_):
      logger.error(bstack11l111111_opy_.format(bstack11llll11ll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack1l11ll1_opy_ (u"࠭࡟ࡨࡧࡷࡣࡵࡸ࡯ࡹࡻࡢࡹࡷࡲࠧ೮")) and callable(getattr(RemoteConnection, bstack1l11ll1_opy_ (u"ࠧࡠࡩࡨࡸࡤࡶࡲࡰࡺࡼࡣࡺࡸ࡬ࠨ೯"))):
          bstack11ll11l1l_opy_ = RemoteConnection._get_proxy_url
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          bstack11ll11l1l_opy_ = ClientConfig.get_proxy_url
      except Exception as e:
        logger.error(bstack111llll11l_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1lll1llll_opy_ = Config.getoption
    from _pytest import runner
    bstack111l11l11_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack1l11ll11ll_opy_)
  try:
    from pytest_bdd import reporting
    bstack1111l1ll1_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack1l11ll1_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡰࠢࡵࡹࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࡴࠩ೰"))
  bstack1l1111111l_opy_ = CONFIG.get(bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ೱ"), {}).get(bstack1l11ll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬೲ"))
  bstack11llll111_opy_ = True
  if cli.is_enabled(CONFIG):
    if cli.bstack1ll1l1ll_opy_():
      bstack1l1111l1_opy_.invoke(bstack1l11lll111_opy_.CONNECT, bstack1ll1111l1_opy_())
    platform_index = int(os.environ.get(bstack1l11ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫೳ"), bstack1l11ll1_opy_ (u"ࠬ࠶ࠧ೴")))
  else:
    bstack11l11llll1_opy_(bstack1l11lll11l_opy_)
  os.environ[bstack1l11ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧ೵")] = CONFIG[bstack1l11ll1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ೶")]
  os.environ[bstack1l11ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫ೷")] = CONFIG[bstack1l11ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ೸")]
  os.environ[bstack1l11ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭೹")] = bstack1111lll1_opy_.__str__()
  from _pytest.config import main as bstack1llll1l11_opy_
  bstack11ll1ll111_opy_ = []
  try:
    exit_code = bstack1llll1l11_opy_(arg)
    if cli.is_enabled(CONFIG):
      cli.bstack1ll11l1l_opy_()
    if bstack1l11ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴࠨ೺") in multiprocessing.current_process().__dict__.keys():
      for bstack1l111l1l11_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack11ll1ll111_opy_.append(bstack1l111l1l11_opy_)
    try:
      bstack11l1l111ll_opy_ = (bstack11ll1ll111_opy_, int(exit_code))
      bstack11ll1ll1_opy_.append(bstack11l1l111ll_opy_)
    except:
      bstack11ll1ll1_opy_.append((bstack11ll1ll111_opy_, exit_code))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack11ll1ll111_opy_.append({bstack1l11ll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ೻"): bstack1l11ll1_opy_ (u"࠭ࡐࡳࡱࡦࡩࡸࡹࠠࠨ೼") + os.environ.get(bstack1l11ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ೽")), bstack1l11ll1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ೾"): traceback.format_exc(), bstack1l11ll1_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ೿"): int(os.environ.get(bstack1l11ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪഀ")))})
    bstack11ll1ll1_opy_.append((bstack11ll1ll111_opy_, 1))
def mod_behave_main(args, retries):
  try:
    from behave.configuration import Configuration
    from behave.__main__ import run_behave
    from browserstack_sdk.bstack_behave_runner import BehaveRunner
    config = Configuration(args)
    config.update_userdata({bstack1l11ll1_opy_ (u"ࠦࡷ࡫ࡴࡳ࡫ࡨࡷࠧഁ"): str(retries)})
    return run_behave(config, runner_class=BehaveRunner)
  except Exception as e:
    bstack1ll1llll_opy_ = e.__class__.__name__
    print(bstack1l11ll1_opy_ (u"ࠧࠫࡳ࠻ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡴࡸࡲࡳ࡯࡮ࡨࠢࡥࡩ࡭ࡧࡶࡦࠢࡷࡩࡸࡺࠠࠦࡵࠥം") % (bstack1ll1llll_opy_, e))
    return 1
def bstack111l111ll_opy_(arg):
  global bstack11l1lll1_opy_
  bstack11l11llll1_opy_(bstack1l1ll11ll_opy_)
  os.environ[bstack1l11ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧഃ")] = str(bstack1lllll11l_opy_)
  retries = bstack11llll1111_opy_.bstack11l1l1l1ll_opy_(CONFIG)
  status_code = 0
  if bstack11llll1111_opy_.bstack1ll1l111l_opy_(CONFIG):
    status_code = mod_behave_main(arg, retries)
  else:
    from behave.__main__ import main as bstack1l11l1111_opy_
    status_code = bstack1l11l1111_opy_(arg)
  if status_code != 0:
    bstack11l1lll1_opy_ = status_code
def bstack11l1lllll1_opy_():
  logger.info(bstack11l1lll111_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1l11ll1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ഄ"), help=bstack1l11ll1_opy_ (u"ࠨࡉࡨࡲࡪࡸࡡࡵࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡦࡳࡳ࡬ࡩࡨࠩഅ"))
  parser.add_argument(bstack1l11ll1_opy_ (u"ࠩ࠰ࡹࠬആ"), bstack1l11ll1_opy_ (u"ࠪ࠱࠲ࡻࡳࡦࡴࡱࡥࡲ࡫ࠧഇ"), help=bstack1l11ll1_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡷࡶࡩࡷࡴࡡ࡮ࡧࠪഈ"))
  parser.add_argument(bstack1l11ll1_opy_ (u"ࠬ࠳࡫ࠨഉ"), bstack1l11ll1_opy_ (u"࠭࠭࠮࡭ࡨࡽࠬഊ"), help=bstack1l11ll1_opy_ (u"࡚ࠧࡱࡸࡶࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡦࡩࡣࡦࡵࡶࠤࡰ࡫ࡹࠨഋ"))
  parser.add_argument(bstack1l11ll1_opy_ (u"ࠨ࠯ࡩࠫഌ"), bstack1l11ll1_opy_ (u"ࠩ࠰࠱࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ഍"), help=bstack1l11ll1_opy_ (u"ࠪ࡝ࡴࡻࡲࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩഎ"))
  bstack11lllll11l_opy_ = parser.parse_args()
  try:
    bstack11l11111_opy_ = bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡫ࡪࡴࡥࡳ࡫ࡦ࠲ࡾࡳ࡬࠯ࡵࡤࡱࡵࡲࡥࠨഏ")
    if bstack11lllll11l_opy_.framework and bstack11lllll11l_opy_.framework not in (bstack1l11ll1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬഐ"), bstack1l11ll1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧ഑")):
      bstack11l11111_opy_ = bstack1l11ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠰ࡼࡱࡱ࠴ࡳࡢ࡯ࡳࡰࡪ࠭ഒ")
    bstack11l1llll1_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11l11111_opy_)
    bstack1lll1lll1_opy_ = open(bstack11l1llll1_opy_, bstack1l11ll1_opy_ (u"ࠨࡴࠪഓ"))
    bstack1ll1l1l1ll_opy_ = bstack1lll1lll1_opy_.read()
    bstack1lll1lll1_opy_.close()
    if bstack11lllll11l_opy_.username:
      bstack1ll1l1l1ll_opy_ = bstack1ll1l1l1ll_opy_.replace(bstack1l11ll1_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩഔ"), bstack11lllll11l_opy_.username)
    if bstack11lllll11l_opy_.key:
      bstack1ll1l1l1ll_opy_ = bstack1ll1l1l1ll_opy_.replace(bstack1l11ll1_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬക"), bstack11lllll11l_opy_.key)
    if bstack11lllll11l_opy_.framework:
      bstack1ll1l1l1ll_opy_ = bstack1ll1l1l1ll_opy_.replace(bstack1l11ll1_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬഖ"), bstack11lllll11l_opy_.framework)
    file_name = bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨഗ")
    file_path = os.path.abspath(file_name)
    bstack1l111lllll_opy_ = open(file_path, bstack1l11ll1_opy_ (u"࠭ࡷࠨഘ"))
    bstack1l111lllll_opy_.write(bstack1ll1l1l1ll_opy_)
    bstack1l111lllll_opy_.close()
    logger.info(bstack11ll11l1ll_opy_)
    try:
      os.environ[bstack1l11ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩങ")] = bstack11lllll11l_opy_.framework if bstack11lllll11l_opy_.framework != None else bstack1l11ll1_opy_ (u"ࠣࠤച")
      config = yaml.safe_load(bstack1ll1l1l1ll_opy_)
      config[bstack1l11ll1_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩഛ")] = bstack1l11ll1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰ࡷࡪࡺࡵࡱࠩജ")
      bstack1l111ll11l_opy_(bstack11ll1111ll_opy_, config)
    except Exception as e:
      logger.debug(bstack11ll11llll_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1ll11l1l1_opy_.format(str(e)))
def bstack1l111ll11l_opy_(bstack111lllll1l_opy_, config, bstack11llllll1l_opy_={}):
  global bstack1111lll1_opy_
  global bstack1ll1l11l1l_opy_
  global bstack111lllll11_opy_
  if not config:
    return
  bstack1l1l1lll11_opy_ = bstack1l1l11111_opy_ if not bstack1111lll1_opy_ else (
    bstack11ll111lll_opy_ if bstack1l11ll1_opy_ (u"ࠫࡦࡶࡰࠨഝ") in config else (
        bstack111l1ll1_opy_ if config.get(bstack1l11ll1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩഞ")) else bstack1lll1l1l_opy_
    )
)
  bstack1llll111l1_opy_ = False
  bstack11lll11ll1_opy_ = False
  if bstack1111lll1_opy_ is True:
      if bstack1l11ll1_opy_ (u"࠭ࡡࡱࡲࠪട") in config:
          bstack1llll111l1_opy_ = True
      else:
          bstack11lll11ll1_opy_ = True
  bstack1ll1ll1111_opy_ = bstack1ll111ll_opy_.bstack1ll1l1l1l_opy_(config, bstack1ll1l11l1l_opy_)
  bstack1l1l1l1lll_opy_ = bstack11l1l1l1l1_opy_()
  data = {
    bstack1l11ll1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩഠ"): config[bstack1l11ll1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪഡ")],
    bstack1l11ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬഢ"): config[bstack1l11ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ണ")],
    bstack1l11ll1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨത"): bstack111lllll1l_opy_,
    bstack1l11ll1_opy_ (u"ࠬࡪࡥࡵࡧࡦࡸࡪࡪࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩഥ"): os.environ.get(bstack1l11ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨദ"), bstack1ll1l11l1l_opy_),
    bstack1l11ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩധ"): bstack1l11l11lll_opy_,
    bstack1l11ll1_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮ࠪന"): bstack111111l11_opy_(),
    bstack1l11ll1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬഩ"): {
      bstack1l11ll1_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨപ"): str(config[bstack1l11ll1_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫഫ")]) if bstack1l11ll1_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬബ") in config else bstack1l11ll1_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢഭ"),
      bstack1l11ll1_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࡘࡨࡶࡸ࡯࡯࡯ࠩമ"): sys.version,
      bstack1l11ll1_opy_ (u"ࠨࡴࡨࡪࡪࡸࡲࡦࡴࠪയ"): bstack111l1l1ll_opy_(os.environ.get(bstack1l11ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫര"), bstack1ll1l11l1l_opy_)),
      bstack1l11ll1_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬറ"): bstack1l11ll1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫല"),
      bstack1l11ll1_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭ള"): bstack1l1l1lll11_opy_,
      bstack1l11ll1_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ࡟࡮ࡣࡳࠫഴ"): bstack1ll1ll1111_opy_,
      bstack1l11ll1_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡠࡷࡸ࡭ࡩ࠭വ"): os.environ[bstack1l11ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ശ")],
      bstack1l11ll1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬഷ"): os.environ.get(bstack1l11ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬസ"), bstack1ll1l11l1l_opy_),
      bstack1l11ll1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧഹ"): bstack11ll11l111_opy_(os.environ.get(bstack1l11ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧഺ"), bstack1ll1l11l1l_opy_)),
      bstack1l11ll1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯഻ࠬ"): bstack1l1l1l1lll_opy_.get(bstack1l11ll1_opy_ (u"ࠧ࡯ࡣࡰࡩ഼ࠬ")),
      bstack1l11ll1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧഽ"): bstack1l1l1l1lll_opy_.get(bstack1l11ll1_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪാ")),
      bstack1l11ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ി"): config[bstack1l11ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧീ")] if config[bstack1l11ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨു")] else bstack1l11ll1_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢൂ"),
      bstack1l11ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩൃ"): str(config[bstack1l11ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪൄ")]) if bstack1l11ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ൅") in config else bstack1l11ll1_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦെ"),
      bstack1l11ll1_opy_ (u"ࠫࡴࡹࠧേ"): sys.platform,
      bstack1l11ll1_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧൈ"): socket.gethostname(),
      bstack1l11ll1_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨ൉"): bstack111lllll11_opy_.get_property(bstack1l11ll1_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥࠩൊ"))
    }
  }
  if not bstack111lllll11_opy_.get_property(bstack1l11ll1_opy_ (u"ࠨࡵࡧ࡯ࡐ࡯࡬࡭ࡕ࡬࡫ࡳࡧ࡬ࠨോ")) is None:
    data[bstack1l11ll1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬൌ")][bstack1l11ll1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡒ࡫ࡴࡢࡦࡤࡸࡦ്࠭")] = {
      bstack1l11ll1_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫൎ"): bstack1l11ll1_opy_ (u"ࠬࡻࡳࡦࡴࡢ࡯࡮ࡲ࡬ࡦࡦࠪ൏"),
      bstack1l11ll1_opy_ (u"࠭ࡳࡪࡩࡱࡥࡱ࠭൐"): bstack111lllll11_opy_.get_property(bstack1l11ll1_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡔ࡫ࡪࡲࡦࡲࠧ൑")),
      bstack1l11ll1_opy_ (u"ࠨࡵ࡬࡫ࡳࡧ࡬ࡏࡷࡰࡦࡪࡸࠧ൒"): bstack111lllll11_opy_.get_property(bstack1l11ll1_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡑࡳࠬ൓"))
    }
  if bstack111lllll1l_opy_ == bstack1l1111l1l1_opy_:
    data[bstack1l11ll1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭ൔ")][bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡆࡳࡳ࡬ࡩࡨࠩൕ")] = bstack1l11ll1ll1_opy_(config)
    data[bstack1l11ll1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨൖ")][bstack1l11ll1_opy_ (u"࠭ࡩࡴࡒࡨࡶࡨࡿࡁࡶࡶࡲࡉࡳࡧࡢ࡭ࡧࡧࠫൗ")] = percy.bstack1ll11ll1l_opy_
    data[bstack1l11ll1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪ൘")][bstack1l11ll1_opy_ (u"ࠨࡲࡨࡶࡨࡿࡂࡶ࡫࡯ࡨࡎࡪࠧ൙")] = percy.percy_build_id
  if not bstack11llll1111_opy_.bstack111lll1l1_opy_(CONFIG):
    data[bstack1l11ll1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬ൚")][bstack1l11ll1_opy_ (u"ࠪࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠧ൛")] = bstack11llll1111_opy_.bstack111lll1l1_opy_(CONFIG)
  bstack1lllllllll_opy_ = bstack1lll111lll_opy_.bstack1lll111l1l_opy_(CONFIG, logger)
  bstack11ll1lll1_opy_ = bstack11llll1111_opy_.bstack1lll111l1l_opy_(config=CONFIG)
  if bstack1lllllllll_opy_ is not None and bstack11ll1lll1_opy_ is not None and bstack11ll1lll1_opy_.bstack1l1lll1lll_opy_():
    data[bstack1l11ll1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧ൜")][bstack11ll1lll1_opy_.bstack111l1llll_opy_()] = bstack1lllllllll_opy_.bstack1l1ll1l1l1_opy_()
  update(data[bstack1l11ll1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨ൝")], bstack11llllll1l_opy_)
  try:
    response = bstack1l1ll1ll1l_opy_(bstack1l11ll1_opy_ (u"࠭ࡐࡐࡕࡗࠫ൞"), bstack1111l1lll_opy_(bstack11l1l11lll_opy_), data, {
      bstack1l11ll1_opy_ (u"ࠧࡢࡷࡷ࡬ࠬൟ"): (config[bstack1l11ll1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪൠ")], config[bstack1l11ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬൡ")])
    })
    if response:
      logger.debug(bstack1l1ll1l1ll_opy_.format(bstack111lllll1l_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack11l1111lll_opy_.format(str(e)))
def bstack111l1l1ll_opy_(framework):
  return bstack1l11ll1_opy_ (u"ࠥࡿࢂ࠳ࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࢀࢃࠢൢ").format(str(framework), __version__) if framework else bstack1l11ll1_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࡾࢁࠧൣ").format(
    __version__)
def bstack11l1ll11_opy_():
  global CONFIG
  global bstack111111ll1_opy_
  if bool(CONFIG):
    return
  try:
    bstack1l1ll1ll_opy_()
    logger.debug(bstack1lllllll1_opy_.format(str(CONFIG)))
    bstack111111ll1_opy_ = bstack1lll1l1l1l_opy_.configure_logger(CONFIG, bstack111111ll1_opy_)
    bstack11l1111l1l_opy_()
  except Exception as e:
    logger.error(bstack1l11ll1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࠤ൤") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1ll11111l1_opy_
  atexit.register(bstack1l11l1ll_opy_)
  signal.signal(signal.SIGINT, bstack1l11l1l1_opy_)
  signal.signal(signal.SIGTERM, bstack1l11l1l1_opy_)
def bstack1ll11111l1_opy_(exctype, value, traceback):
  global bstack11l11lll1l_opy_
  try:
    for driver in bstack11l11lll1l_opy_:
      bstack1l1l111l1_opy_(driver, bstack1l11ll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭൥"), bstack1l11ll1_opy_ (u"ࠢࡔࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥ൦") + str(value))
  except Exception:
    pass
  logger.info(bstack1lll1111l_opy_)
  bstack1lllll111l_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1lllll111l_opy_(message=bstack1l11ll1_opy_ (u"ࠨࠩ൧"), bstack11l11l1l11_opy_ = False):
  global CONFIG
  bstack1111l1111_opy_ = bstack1l11ll1_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡇࡻࡧࡪࡶࡴࡪࡱࡱࠫ൨") if bstack11l11l1l11_opy_ else bstack1l11ll1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ൩")
  try:
    if message:
      bstack11llllll1l_opy_ = {
        bstack1111l1111_opy_ : str(message)
      }
      bstack1l111ll11l_opy_(bstack1l1111l1l1_opy_, CONFIG, bstack11llllll1l_opy_)
    else:
      bstack1l111ll11l_opy_(bstack1l1111l1l1_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack11ll111l_opy_.format(str(e)))
def bstack11ll1lllll_opy_(bstack1llll11l11_opy_, size):
  bstack1ll1111l11_opy_ = []
  while len(bstack1llll11l11_opy_) > size:
    bstack1l1l11llll_opy_ = bstack1llll11l11_opy_[:size]
    bstack1ll1111l11_opy_.append(bstack1l1l11llll_opy_)
    bstack1llll11l11_opy_ = bstack1llll11l11_opy_[size:]
  bstack1ll1111l11_opy_.append(bstack1llll11l11_opy_)
  return bstack1ll1111l11_opy_
def bstack1l11111lll_opy_(args):
  if bstack1l11ll1_opy_ (u"ࠫ࠲ࡳࠧ൪") in args and bstack1l11ll1_opy_ (u"ࠬࡶࡤࡣࠩ൫") in args:
    return True
  return False
@measure(event_name=EVENTS.bstack1l111lll_opy_, stage=STAGE.bstack1l1lll11ll_opy_)
def run_on_browserstack(bstack1l111ll111_opy_=None, bstack11ll1ll1_opy_=None, bstack11l11ll11_opy_=False):
  global CONFIG
  global bstack11lll1ll11_opy_
  global bstack1lllll11l_opy_
  global bstack1ll1l11l1l_opy_
  global bstack111lllll11_opy_
  bstack11ll111ll_opy_ = bstack1l11ll1_opy_ (u"࠭ࠧ൬")
  bstack1l111l1ll_opy_(bstack1l1ll1l1_opy_, logger)
  if bstack1l111ll111_opy_ and isinstance(bstack1l111ll111_opy_, str):
    bstack1l111ll111_opy_ = eval(bstack1l111ll111_opy_)
  if bstack1l111ll111_opy_:
    CONFIG = bstack1l111ll111_opy_[bstack1l11ll1_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧ൭")]
    bstack11lll1ll11_opy_ = bstack1l111ll111_opy_[bstack1l11ll1_opy_ (u"ࠨࡊࡘࡆࡤ࡛ࡒࡍࠩ൮")]
    bstack1lllll11l_opy_ = bstack1l111ll111_opy_[bstack1l11ll1_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ൯")]
    bstack111lllll11_opy_.bstack11l111l1ll_opy_(bstack1l11ll1_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ൰"), bstack1lllll11l_opy_)
    bstack11ll111ll_opy_ = bstack1l11ll1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ൱")
  bstack111lllll11_opy_.bstack11l111l1ll_opy_(bstack1l11ll1_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪࠧ൲"), uuid4().__str__())
  logger.info(bstack1l11ll1_opy_ (u"࠭ࡓࡅࡍࠣࡶࡺࡴࠠࡴࡶࡤࡶࡹ࡫ࡤࠡࡹ࡬ࡸ࡭ࠦࡩࡥ࠼ࠣࠫ൳") + bstack111lllll11_opy_.get_property(bstack1l11ll1_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥࠩ൴")));
  logger.debug(bstack1l11ll1_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࡀࠫ൵") + bstack111lllll11_opy_.get_property(bstack1l11ll1_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫ൶")))
  if not bstack11l11ll11_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack11ll11l1l1_opy_)
      return
    if sys.argv[1] == bstack1l11ll1_opy_ (u"ࠪ࠱࠲ࡼࡥࡳࡵ࡬ࡳࡳ࠭൷") or sys.argv[1] == bstack1l11ll1_opy_ (u"ࠫ࠲ࡼࠧ൸"):
      logger.info(bstack1l11ll1_opy_ (u"ࠬࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡕࡿࡴࡩࡱࡱࠤࡘࡊࡋࠡࡸࡾࢁࠬ൹").format(__version__))
      return
    if sys.argv[1] == bstack1l11ll1_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬൺ"):
      bstack11l1lllll1_opy_()
      return
  args = sys.argv
  bstack11l1ll11_opy_()
  global bstack11ll11ll1_opy_
  global bstack11l1l11ll_opy_
  global bstack11llll111_opy_
  global bstack11lllll1l_opy_
  global bstack11ll1llll_opy_
  global bstack1l1111111l_opy_
  global bstack1lll1ll11l_opy_
  global bstack1lll11llll_opy_
  global bstack11l1111l_opy_
  global bstack1l1l1ll1l1_opy_
  global bstack1l11l11l11_opy_
  bstack11l1l11ll_opy_ = len(CONFIG.get(bstack1l11ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪൻ"), []))
  if not bstack11ll111ll_opy_:
    if args[1] == bstack1l11ll1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨർ") or args[1] == bstack1l11ll1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪൽ"):
      bstack11ll111ll_opy_ = bstack1l11ll1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪൾ")
      args = args[2:]
    elif args[1] == bstack1l11ll1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪൿ"):
      bstack11ll111ll_opy_ = bstack1l11ll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ඀")
      args = args[2:]
    elif args[1] == bstack1l11ll1_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬඁ"):
      bstack11ll111ll_opy_ = bstack1l11ll1_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ං")
      args = args[2:]
    elif args[1] == bstack1l11ll1_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩඃ"):
      bstack11ll111ll_opy_ = bstack1l11ll1_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ඄")
      args = args[2:]
    elif args[1] == bstack1l11ll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪඅ"):
      bstack11ll111ll_opy_ = bstack1l11ll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫආ")
      args = args[2:]
    elif args[1] == bstack1l11ll1_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬඇ"):
      bstack11ll111ll_opy_ = bstack1l11ll1_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ඈ")
      args = args[2:]
    else:
      if not bstack1l11ll1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪඉ") in CONFIG or str(CONFIG[bstack1l11ll1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫඊ")]).lower() in [bstack1l11ll1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩඋ"), bstack1l11ll1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫඌ")]:
        bstack11ll111ll_opy_ = bstack1l11ll1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫඍ")
        args = args[1:]
      elif str(CONFIG[bstack1l11ll1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨඎ")]).lower() == bstack1l11ll1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬඏ"):
        bstack11ll111ll_opy_ = bstack1l11ll1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ඐ")
        args = args[1:]
      elif str(CONFIG[bstack1l11ll1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫඑ")]).lower() == bstack1l11ll1_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨඒ"):
        bstack11ll111ll_opy_ = bstack1l11ll1_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩඓ")
        args = args[1:]
      elif str(CONFIG[bstack1l11ll1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧඔ")]).lower() == bstack1l11ll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬඕ"):
        bstack11ll111ll_opy_ = bstack1l11ll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ඖ")
        args = args[1:]
      elif str(CONFIG[bstack1l11ll1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ඗")]).lower() == bstack1l11ll1_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ඘"):
        bstack11ll111ll_opy_ = bstack1l11ll1_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ඙")
        args = args[1:]
      else:
        os.environ[bstack1l11ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬක")] = bstack11ll111ll_opy_
        bstack1ll1l1l11_opy_(bstack1lll11111_opy_)
  os.environ[bstack1l11ll1_opy_ (u"ࠫࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ࡟ࡖࡕࡈࡈࠬඛ")] = bstack11ll111ll_opy_
  bstack1ll1l11l1l_opy_ = bstack11ll111ll_opy_
  if cli.is_enabled(CONFIG):
    try:
      bstack1l1l11l1l1_opy_ = bstack1111ll111_opy_[bstack1l11ll1_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘ࠲ࡈࡄࡅࠩග")] if bstack11ll111ll_opy_ == bstack1l11ll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ඝ") and bstack1l11llll11_opy_() else bstack11ll111ll_opy_
      bstack1l1111l1_opy_.invoke(bstack1l11lll111_opy_.bstack11lll11l_opy_, bstack1l111111l_opy_(
        sdk_version=__version__,
        path_config=bstack1ll1l111_opy_(),
        path_project=os.getcwd(),
        test_framework=bstack1l1l11l1l1_opy_,
        frameworks=[bstack1l1l11l1l1_opy_],
        framework_versions={
          bstack1l1l11l1l1_opy_: bstack11ll11l111_opy_(bstack1l11ll1_opy_ (u"ࠧࡓࡱࡥࡳࡹ࠭ඞ") if bstack11ll111ll_opy_ in [bstack1l11ll1_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧඟ"), bstack1l11ll1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨච"), bstack1l11ll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫඡ")] else bstack11ll111ll_opy_)
        },
        bs_config=CONFIG
      ))
      if cli.config.get(bstack1l11ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࠨජ"), None):
        CONFIG[bstack1l11ll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠢඣ")] = cli.config.get(bstack1l11ll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣඤ"), None)
    except Exception as e:
      bstack1l1111l1_opy_.invoke(bstack1l11lll111_opy_.bstack1l11ll11_opy_, e.__traceback__, 1)
    if bstack1lllll11l_opy_:
      CONFIG[bstack1l11ll1_opy_ (u"ࠢࡢࡲࡳࠦඥ")] = cli.config[bstack1l11ll1_opy_ (u"ࠣࡣࡳࡴࠧඦ")]
      logger.info(bstack11lll1111l_opy_.format(CONFIG[bstack1l11ll1_opy_ (u"ࠩࡤࡴࡵ࠭ට")]))
  else:
    bstack1l1111l1_opy_.clear()
  global bstack1l1lll1111_opy_
  global bstack11ll1l11ll_opy_
  if bstack1l111ll111_opy_:
    try:
      bstack1l11ll1ll_opy_ = datetime.datetime.now()
      os.environ[bstack1l11ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬඨ")] = bstack11ll111ll_opy_
      bstack1l111ll11l_opy_(bstack11ll1111l_opy_, CONFIG)
      cli.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼ࡶࡨࡰࡥࡴࡦࡵࡷࡣࡦࡺࡴࡦ࡯ࡳࡸࡪࡪࠢඩ"), datetime.datetime.now() - bstack1l11ll1ll_opy_)
    except Exception as e:
      logger.debug(bstack1l1l1l111_opy_.format(str(e)))
  global bstack1ll11lll_opy_
  global bstack1l1l1ll1_opy_
  global bstack1ll11l111l_opy_
  global bstack1ll111lll1_opy_
  global bstack11ll1llll1_opy_
  global bstack1l1ll11111_opy_
  global bstack11l111l1_opy_
  global bstack1111l1l1l_opy_
  global bstack1l1ll111l_opy_
  global bstack11l1l11l1_opy_
  global bstack11ll111111_opy_
  global bstack111lll111_opy_
  global bstack11l1ll1ll1_opy_
  global bstack1l1lll11l_opy_
  global bstack11lll1ll1_opy_
  global bstack11ll11l1l_opy_
  global bstack1lll1llll_opy_
  global bstack111l11l11_opy_
  global bstack1l1l1l1l_opy_
  global bstack1111l1ll1_opy_
  global bstack1ll1l111ll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1ll11lll_opy_ = webdriver.Remote.__init__
    bstack1l1l1ll1_opy_ = WebDriver.quit
    bstack111lll111_opy_ = WebDriver.close
    bstack11lll1ll1_opy_ = WebDriver.get
    bstack1ll1l111ll_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1l1lll1111_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack1l11ll11l_opy_
    bstack11ll1l11ll_opy_ = bstack1l11ll11l_opy_()
  except Exception as e:
    pass
  try:
    global bstack1ll111111_opy_
    from QWeb.keywords import browser
    bstack1ll111111_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1l111ll11_opy_(CONFIG) and bstack1l11l1l1ll_opy_():
    if bstack11llll11ll_opy_() < version.parse(bstack1ll1l11l1_opy_):
      logger.error(bstack11l111111_opy_.format(bstack11llll11ll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack1l11ll1_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭ඪ")) and callable(getattr(RemoteConnection, bstack1l11ll1_opy_ (u"࠭࡟ࡨࡧࡷࡣࡵࡸ࡯ࡹࡻࡢࡹࡷࡲࠧණ"))):
          RemoteConnection._get_proxy_url = bstack1lllll1ll_opy_
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          ClientConfig.get_proxy_url = bstack1lllll1ll_opy_
      except Exception as e:
        logger.error(bstack111llll11l_opy_.format(str(e)))
  if not CONFIG.get(bstack1l11ll1_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡷࡷࡳࡈࡧࡰࡵࡷࡵࡩࡑࡵࡧࡴࠩඬ"), False) and not bstack1l111ll111_opy_:
    logger.info(bstack1ll111111l_opy_)
  if not cli.is_enabled(CONFIG):
    if bstack1l11ll1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬත") in CONFIG and str(CONFIG[bstack1l11ll1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ථ")]).lower() != bstack1l11ll1_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩද"):
      bstack11l1lll11_opy_()
    elif bstack11ll111ll_opy_ != bstack1l11ll1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫධ") or (bstack11ll111ll_opy_ == bstack1l11ll1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬන") and not bstack1l111ll111_opy_):
      bstack1ll1ll111l_opy_()
  if (bstack11ll111ll_opy_ in [bstack1l11ll1_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ඲"), bstack1l11ll1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ඳ"), bstack1l11ll1_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩප")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1lll11ll11_opy_
        bstack1l1ll11111_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack11l11l1ll1_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack11ll1llll1_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack111lll1ll_opy_ + str(e))
    except Exception as e:
      bstack11l1l1ll_opy_(e, bstack11l11l1ll1_opy_)
    if bstack11ll111ll_opy_ != bstack1l11ll1_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪඵ"):
      bstack111lll11l_opy_()
    bstack1ll11l111l_opy_ = Output.start_test
    bstack1ll111lll1_opy_ = Output.end_test
    bstack11l111l1_opy_ = TestStatus.__init__
    bstack1l1ll111l_opy_ = pabot._run
    bstack11l1l11l1_opy_ = QueueItem.__init__
    bstack11ll111111_opy_ = pabot._create_command_for_execution
    bstack1l1l1l1l_opy_ = pabot._report_results
  if bstack11ll111ll_opy_ == bstack1l11ll1_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪබ"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11l1l1ll_opy_(e, bstack1111l11ll_opy_)
    bstack11l1ll1ll1_opy_ = Runner.run_hook
    bstack1l1lll11l_opy_ = Step.run
  if bstack11ll111ll_opy_ == bstack1l11ll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫභ"):
    try:
      from _pytest.config import Config
      bstack1lll1llll_opy_ = Config.getoption
      from _pytest import runner
      bstack111l11l11_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack1l11ll11ll_opy_)
    try:
      from pytest_bdd import reporting
      bstack1111l1ll1_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1l11ll1_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡴࠦࡲࡶࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࡸ࠭ම"))
  try:
    framework_name = bstack1l11ll1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬඹ") if bstack11ll111ll_opy_ in [bstack1l11ll1_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ය"), bstack1l11ll1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧර"), bstack1l11ll1_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ඼")] else bstack11ll1ll1l_opy_(bstack11ll111ll_opy_)
    bstack11l1ll1l1l_opy_ = {
      bstack1l11ll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࠫල"): bstack1l11ll1_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷ࠱ࡨࡻࡣࡶ࡯ࡥࡩࡷ࠭඾") if bstack11ll111ll_opy_ == bstack1l11ll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ඿") and bstack1l11llll11_opy_() else framework_name,
      bstack1l11ll1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪව"): bstack11ll11l111_opy_(framework_name),
      bstack1l11ll1_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬශ"): __version__,
      bstack1l11ll1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡺࡹࡥࡥࠩෂ"): bstack11ll111ll_opy_
    }
    if bstack11ll111ll_opy_ in bstack1llll11ll1_opy_ + bstack1lll1llll1_opy_:
      if bstack11lll1ll1l_opy_.bstack11l11l1l1l_opy_(CONFIG):
        if bstack1l11ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩස") in CONFIG:
          os.environ[bstack1l11ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫහ")] = os.getenv(bstack1l11ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬළ"), json.dumps(CONFIG[bstack1l11ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬෆ")]))
          CONFIG[bstack1l11ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭෇")].pop(bstack1l11ll1_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬ෈"), None)
          CONFIG[bstack1l11ll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ෉")].pop(bstack1l11ll1_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫්ࠧ"), None)
        bstack11l1ll1l1l_opy_[bstack1l11ll1_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ෋")] = {
          bstack1l11ll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ෌"): bstack1l11ll1_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧ෍"),
          bstack1l11ll1_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧ෎"): str(bstack11llll11ll_opy_())
        }
    if bstack11ll111ll_opy_ not in [bstack1l11ll1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨා")] and not cli.is_running():
      bstack1l11l111ll_opy_, bstack1lll111ll_opy_ = bstack1l111111l1_opy_.launch(CONFIG, bstack11l1ll1l1l_opy_)
      if bstack1lll111ll_opy_.get(bstack1l11ll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨැ")) is not None and bstack11lll1ll1l_opy_.bstack1l111l11l1_opy_(CONFIG) is None:
        value = bstack1lll111ll_opy_[bstack1l11ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩෑ")].get(bstack1l11ll1_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫි"))
        if value is not None:
            CONFIG[bstack1l11ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫී")] = value
        else:
          logger.debug(bstack1l11ll1_opy_ (u"ࠧࡔ࡯ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡦࡤࡸࡦࠦࡦࡰࡷࡱࡨࠥ࡯࡮ࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠥු"))
  except Exception as e:
    logger.debug(bstack1lll1ll1_opy_.format(bstack1l11ll1_opy_ (u"࠭ࡔࡦࡵࡷࡌࡺࡨࠧ෕"), str(e)))
  if bstack11ll111ll_opy_ == bstack1l11ll1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧූ"):
    bstack11llll111_opy_ = True
    if bstack1l111ll111_opy_ and bstack11l11ll11_opy_:
      bstack1l1111111l_opy_ = CONFIG.get(bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ෗"), {}).get(bstack1l11ll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫෘ"))
      bstack11l11llll1_opy_(bstack1llll11111_opy_)
    elif bstack1l111ll111_opy_:
      bstack1l1111111l_opy_ = CONFIG.get(bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧෙ"), {}).get(bstack1l11ll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ේ"))
      global bstack11l11lll1l_opy_
      try:
        if bstack1l11111lll_opy_(bstack1l111ll111_opy_[bstack1l11ll1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨෛ")]) and multiprocessing.current_process().name == bstack1l11ll1_opy_ (u"࠭࠰ࠨො"):
          bstack1l111ll111_opy_[bstack1l11ll1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪෝ")].remove(bstack1l11ll1_opy_ (u"ࠨ࠯ࡰࠫෞ"))
          bstack1l111ll111_opy_[bstack1l11ll1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬෟ")].remove(bstack1l11ll1_opy_ (u"ࠪࡴࡩࡨࠧ෠"))
          bstack1l111ll111_opy_[bstack1l11ll1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ෡")] = bstack1l111ll111_opy_[bstack1l11ll1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ෢")][0]
          with open(bstack1l111ll111_opy_[bstack1l11ll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ෣")], bstack1l11ll1_opy_ (u"ࠧࡳࠩ෤")) as f:
            bstack1ll111l11_opy_ = f.read()
          bstack1ll1ll1ll_opy_ = bstack1l11ll1_opy_ (u"ࠣࠤࠥࡪࡷࡵ࡭ࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡴࡦ࡮ࠤ࡮ࡳࡰࡰࡴࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿ࡫࠻ࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡨࠬࢀࢃࠩ࠼ࠢࡩࡶࡴࡳࠠࡱࡦࡥࠤ࡮ࡳࡰࡰࡴࡷࠤࡕࡪࡢ࠼ࠢࡲ࡫ࡤࡪࡢࠡ࠿ࠣࡔࡩࡨ࠮ࡥࡱࡢࡦࡷ࡫ࡡ࡬࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡤࡦࡨࠣࡱࡴࡪ࡟ࡣࡴࡨࡥࡰ࠮ࡳࡦ࡮ࡩ࠰ࠥࡧࡲࡨ࠮ࠣࡸࡪࡳࡰࡰࡴࡤࡶࡾࠦ࠽ࠡ࠲ࠬ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡸࡷࡿ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡣࡵ࡫ࠥࡃࠠࡴࡶࡵࠬ࡮ࡴࡴࠩࡣࡵ࡫࠮࠱࠱࠱ࠫࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡧࡻࡧࡪࡶࡴࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡦࡹࠠࡦ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡴࡦࡹࡳࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࡯ࡨࡡࡧࡦ࠭ࡹࡥ࡭ࡨ࠯ࡥࡷ࡭ࠬࡵࡧࡰࡴࡴࡸࡡࡳࡻࠬࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡑࡦࡥ࠲ࡩࡵ࡟ࡣࠢࡀࠤࡲࡵࡤࡠࡤࡵࡩࡦࡱࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡔࡩࡨ࠮ࡥࡱࡢࡦࡷ࡫ࡡ࡬ࠢࡀࠤࡲࡵࡤࡠࡤࡵࡩࡦࡱࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡔࡩࡨࠨࠪ࠰ࡶࡩࡹࡥࡴࡳࡣࡦࡩ࠭࠯࡜࡯ࠤࠥࠦ෥").format(str(bstack1l111ll111_opy_))
          bstack1llll1l1ll_opy_ = bstack1ll1ll1ll_opy_ + bstack1ll111l11_opy_
          bstack11l11ll111_opy_ = bstack1l111ll111_opy_[bstack1l11ll1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ෦")] + bstack1l11ll1_opy_ (u"ࠪࡣࡧࡹࡴࡢࡥ࡮ࡣࡹ࡫࡭ࡱ࠰ࡳࡽࠬ෧")
          with open(bstack11l11ll111_opy_, bstack1l11ll1_opy_ (u"ࠫࡼ࠭෨")):
            pass
          with open(bstack11l11ll111_opy_, bstack1l11ll1_opy_ (u"ࠧࡽࠫࠣ෩")) as f:
            f.write(bstack1llll1l1ll_opy_)
          import subprocess
          bstack11l11ll1_opy_ = subprocess.run([bstack1l11ll1_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࠨ෪"), bstack11l11ll111_opy_])
          if os.path.exists(bstack11l11ll111_opy_):
            os.unlink(bstack11l11ll111_opy_)
          os._exit(bstack11l11ll1_opy_.returncode)
        else:
          if bstack1l11111lll_opy_(bstack1l111ll111_opy_[bstack1l11ll1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ෫")]):
            bstack1l111ll111_opy_[bstack1l11ll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ෬")].remove(bstack1l11ll1_opy_ (u"ࠩ࠰ࡱࠬ෭"))
            bstack1l111ll111_opy_[bstack1l11ll1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭෮")].remove(bstack1l11ll1_opy_ (u"ࠫࡵࡪࡢࠨ෯"))
            bstack1l111ll111_opy_[bstack1l11ll1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ෰")] = bstack1l111ll111_opy_[bstack1l11ll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ෱")][0]
          bstack11l11llll1_opy_(bstack1llll11111_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1l111ll111_opy_[bstack1l11ll1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪෲ")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1l11ll1_opy_ (u"ࠨࡡࡢࡲࡦࡳࡥࡠࡡࠪෳ")] = bstack1l11ll1_opy_ (u"ࠩࡢࡣࡲࡧࡩ࡯ࡡࡢࠫ෴")
          mod_globals[bstack1l11ll1_opy_ (u"ࠪࡣࡤ࡬ࡩ࡭ࡧࡢࡣࠬ෵")] = os.path.abspath(bstack1l111ll111_opy_[bstack1l11ll1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ෶")])
          exec(open(bstack1l111ll111_opy_[bstack1l11ll1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ෷")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1l11ll1_opy_ (u"࠭ࡃࡢࡷࡪ࡬ࡹࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡿࢂ࠭෸").format(str(e)))
          for driver in bstack11l11lll1l_opy_:
            bstack11ll1ll1_opy_.append({
              bstack1l11ll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ෹"): bstack1l111ll111_opy_[bstack1l11ll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ෺")],
              bstack1l11ll1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ෻"): str(e),
              bstack1l11ll1_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ෼"): multiprocessing.current_process().name
            })
            bstack1l1l111l1_opy_(driver, bstack1l11ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ෽"), bstack1l11ll1_opy_ (u"࡙ࠧࡥࡴࡵ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࡢ࡮ࠣ෾") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack11l11lll1l_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1lllll11l_opy_, CONFIG, logger)
      bstack111111lll_opy_()
      bstack11lll1l1l_opy_()
      percy.bstack11l1l1llll_opy_()
      bstack111lllllll_opy_ = {
        bstack1l11ll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ෿"): args[0],
        bstack1l11ll1_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧ฀"): CONFIG,
        bstack1l11ll1_opy_ (u"ࠨࡊࡘࡆࡤ࡛ࡒࡍࠩก"): bstack11lll1ll11_opy_,
        bstack1l11ll1_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫข"): bstack1lllll11l_opy_
      }
      if bstack1l11ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ฃ") in CONFIG:
        bstack1ll111lll_opy_ = bstack1llll111_opy_(args, logger, CONFIG, bstack1111lll1_opy_, bstack11l1l11ll_opy_)
        bstack1lll11llll_opy_ = bstack1ll111lll_opy_.bstack11l11l11ll_opy_(run_on_browserstack, bstack111lllllll_opy_, bstack1l11111lll_opy_(args))
      else:
        if bstack1l11111lll_opy_(args):
          bstack111lllllll_opy_[bstack1l11ll1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧค")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack111lllllll_opy_,))
          test.start()
          test.join()
        else:
          bstack11l11llll1_opy_(bstack1llll11111_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1l11ll1_opy_ (u"ࠬࡥ࡟࡯ࡣࡰࡩࡤࡥࠧฅ")] = bstack1l11ll1_opy_ (u"࠭࡟ࡠ࡯ࡤ࡭ࡳࡥ࡟ࠨฆ")
          mod_globals[bstack1l11ll1_opy_ (u"ࠧࡠࡡࡩ࡭ࡱ࡫࡟ࡠࠩง")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack11ll111ll_opy_ == bstack1l11ll1_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧจ") or bstack11ll111ll_opy_ == bstack1l11ll1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨฉ"):
    percy.init(bstack1lllll11l_opy_, CONFIG, logger)
    percy.bstack11l1l1llll_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack11l1l1ll_opy_(e, bstack11l11l1ll1_opy_)
    bstack111111lll_opy_()
    bstack11l11llll1_opy_(bstack1l1111l11l_opy_)
    if bstack1111lll1_opy_:
      bstack1l111l11_opy_(bstack1l1111l11l_opy_, args)
      if bstack1l11ll1_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨช") in args:
        i = args.index(bstack1l11ll1_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩซ"))
        args.pop(i)
        args.pop(i)
      if bstack1l11ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨฌ") not in CONFIG:
        CONFIG[bstack1l11ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩญ")] = [{}]
        bstack11l1l11ll_opy_ = 1
      if bstack11ll11ll1_opy_ == 0:
        bstack11ll11ll1_opy_ = 1
      args.insert(0, str(bstack11ll11ll1_opy_))
      args.insert(0, str(bstack1l11ll1_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬฎ")))
    if bstack1l111111l1_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack11ll1l1lll_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1l11111l11_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack1l11ll1_opy_ (u"ࠣࡔࡒࡆࡔ࡚࡟ࡐࡒࡗࡍࡔࡔࡓࠣฏ"),
        ).parse_args(bstack11ll1l1lll_opy_)
        bstack1111l111_opy_ = args.index(bstack11ll1l1lll_opy_[0]) if len(bstack11ll1l1lll_opy_) > 0 else len(args)
        args.insert(bstack1111l111_opy_, str(bstack1l11ll1_opy_ (u"ࠩ࠰࠱ࡱ࡯ࡳࡵࡧࡱࡩࡷ࠭ฐ")))
        args.insert(bstack1111l111_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l11ll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡶࡴࡨ࡯ࡵࡡ࡯࡭ࡸࡺࡥ࡯ࡧࡵ࠲ࡵࡿࠧฑ"))))
        if bstack11llll1111_opy_.bstack1ll1l111l_opy_(CONFIG):
          args.insert(bstack1111l111_opy_, str(bstack1l11ll1_opy_ (u"ࠫ࠲࠳࡬ࡪࡵࡷࡩࡳ࡫ࡲࠨฒ")))
          args.insert(bstack1111l111_opy_ + 1, str(bstack1l11ll1_opy_ (u"ࠬࡘࡥࡵࡴࡼࡊࡦ࡯࡬ࡦࡦ࠽ࡿࢂ࠭ณ").format(bstack11llll1111_opy_.bstack11l1l1l1ll_opy_(CONFIG))))
        if bstack11l1ll11l1_opy_(os.environ.get(bstack1l11ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠫด"))) and str(os.environ.get(bstack1l11ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠫต"), bstack1l11ll1_opy_ (u"ࠨࡰࡸࡰࡱ࠭ถ"))) != bstack1l11ll1_opy_ (u"ࠩࡱࡹࡱࡲࠧท"):
          for bstack1l1l1llll1_opy_ in bstack1l11111l11_opy_:
            args.remove(bstack1l1l1llll1_opy_)
          test_files = os.environ.get(bstack1l11ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠧธ")).split(bstack1l11ll1_opy_ (u"ࠫ࠱࠭น"))
          for bstack111l1ll1l_opy_ in test_files:
            args.append(bstack111l1ll1l_opy_)
      except Exception as e:
        logger.error(bstack1l11ll1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡥࡹࡺࡡࡤࡪ࡬ࡲ࡬ࠦ࡬ࡪࡵࡷࡩࡳ࡫ࡲࠡࡨࡲࡶࠥࢁࡽ࠯ࠢࡈࡶࡷࡵࡲࠡ࠯ࠣࡿࢂࠨบ").format(bstack1l111l111l_opy_, e))
    pabot.main(args)
  elif bstack11ll111ll_opy_ == bstack1l11ll1_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧป"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack11l1l1ll_opy_(e, bstack11l11l1ll1_opy_)
    for a in args:
      if bstack1l11ll1_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝࠭ผ") in a:
        bstack11ll1llll_opy_ = int(a.split(bstack1l11ll1_opy_ (u"ࠨ࠼ࠪฝ"))[1])
      if bstack1l11ll1_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡆࡈࡊࡑࡕࡃࡂࡎࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭พ") in a:
        bstack1l1111111l_opy_ = str(a.split(bstack1l11ll1_opy_ (u"ࠪ࠾ࠬฟ"))[1])
      if bstack1l11ll1_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡇࡑࡏࡁࡓࡉࡖࠫภ") in a:
        bstack1lll1ll11l_opy_ = str(a.split(bstack1l11ll1_opy_ (u"ࠬࡀࠧม"))[1])
    bstack1lllll11ll_opy_ = None
    if bstack1l11ll1_opy_ (u"࠭࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠬย") in args:
      i = args.index(bstack1l11ll1_opy_ (u"ࠧ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽ࠭ร"))
      args.pop(i)
      bstack1lllll11ll_opy_ = args.pop(i)
    if bstack1lllll11ll_opy_ is not None:
      global bstack11l1l1111_opy_
      bstack11l1l1111_opy_ = bstack1lllll11ll_opy_
    bstack11l11llll1_opy_(bstack1l1111l11l_opy_)
    run_cli(args)
    if bstack1l11ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬฤ") in multiprocessing.current_process().__dict__.keys():
      for bstack1l111l1l11_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack11ll1ll1_opy_.append(bstack1l111l1l11_opy_)
  elif bstack11ll111ll_opy_ == bstack1l11ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩล"):
    bstack1ll1l1111_opy_ = bstack1ll11l1l11_opy_(args, logger, CONFIG, bstack1111lll1_opy_)
    bstack1ll1l1111_opy_.bstack11lll1llll_opy_()
    bstack111111lll_opy_()
    bstack11lllll1l_opy_ = True
    bstack1l1l1ll1l1_opy_ = bstack1ll1l1111_opy_.bstack11ll1111_opy_()
    bstack1ll1l1111_opy_.bstack1l11lllll_opy_()
    bstack1ll1l1111_opy_.bstack111lllllll_opy_(bstack1ll11111ll_opy_)
    bstack1llllll1l_opy_(bstack11ll111ll_opy_, CONFIG, bstack1ll1l1111_opy_.bstack1l111ll1l_opy_())
    bstack11l111ll1l_opy_ = bstack1ll1l1111_opy_.bstack11l11l11ll_opy_(bstack1l1llll1ll_opy_, {
      bstack1l11ll1_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫฦ"): bstack11lll1ll11_opy_,
      bstack1l11ll1_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ว"): bstack1lllll11l_opy_,
      bstack1l11ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨศ"): bstack1111lll1_opy_
    })
    try:
      bstack11ll1ll111_opy_, bstack1llll1l111_opy_ = map(list, zip(*bstack11l111ll1l_opy_))
      bstack11l1111l_opy_ = bstack11ll1ll111_opy_[0]
      for status_code in bstack1llll1l111_opy_:
        if status_code != 0:
          bstack1l11l11l11_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack1l11ll1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡥࡻ࡫ࠠࡦࡴࡵࡳࡷࡹࠠࡢࡰࡧࠤࡸࡺࡡࡵࡷࡶࠤࡨࡵࡤࡦ࠰ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦ࠺ࠡࡽࢀࠦษ").format(str(e)))
  elif bstack11ll111ll_opy_ == bstack1l11ll1_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧส"):
    try:
      from behave.__main__ import main as bstack1l11l1111_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack11l1l1ll_opy_(e, bstack1111l11ll_opy_)
    bstack111111lll_opy_()
    bstack11lllll1l_opy_ = True
    bstack1lllll1lll_opy_ = 1
    if bstack1l11ll1_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨห") in CONFIG:
      bstack1lllll1lll_opy_ = CONFIG[bstack1l11ll1_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩฬ")]
    if bstack1l11ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭อ") in CONFIG:
      bstack1ll1lll1l1_opy_ = int(bstack1lllll1lll_opy_) * int(len(CONFIG[bstack1l11ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧฮ")]))
    else:
      bstack1ll1lll1l1_opy_ = int(bstack1lllll1lll_opy_)
    config = Configuration(args)
    bstack1llll1lll_opy_ = config.paths
    if len(bstack1llll1lll_opy_) == 0:
      import glob
      pattern = bstack1l11ll1_opy_ (u"ࠬ࠰ࠪ࠰ࠬ࠱ࡪࡪࡧࡴࡶࡴࡨࠫฯ")
      bstack111l11ll_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack111l11ll_opy_)
      config = Configuration(args)
      bstack1llll1lll_opy_ = config.paths
    bstack1l1ll1lll1_opy_ = [os.path.normpath(item) for item in bstack1llll1lll_opy_]
    bstack1l1ll11lll_opy_ = [os.path.normpath(item) for item in args]
    bstack1lll1ll11_opy_ = [item for item in bstack1l1ll11lll_opy_ if item not in bstack1l1ll1lll1_opy_]
    import platform as pf
    if pf.system().lower() == bstack1l11ll1_opy_ (u"࠭ࡷࡪࡰࡧࡳࡼࡹࠧะ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1l1ll1lll1_opy_ = [str(PurePosixPath(PureWindowsPath(bstack11l11ll1l_opy_)))
                    for bstack11l11ll1l_opy_ in bstack1l1ll1lll1_opy_]
    bstack11ll1lll11_opy_ = []
    for spec in bstack1l1ll1lll1_opy_:
      bstack1lll11l111_opy_ = []
      bstack1lll11l111_opy_ += bstack1lll1ll11_opy_
      bstack1lll11l111_opy_.append(spec)
      bstack11ll1lll11_opy_.append(bstack1lll11l111_opy_)
    execution_items = []
    for bstack1lll11l111_opy_ in bstack11ll1lll11_opy_:
      if bstack1l11ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪั") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack1l11ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫา")]):
          item = {}
          item[bstack1l11ll1_opy_ (u"ࠩࡤࡶ࡬࠭ำ")] = bstack1l11ll1_opy_ (u"ࠪࠤࠬิ").join(bstack1lll11l111_opy_)
          item[bstack1l11ll1_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪี")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack1l11ll1_opy_ (u"ࠬࡧࡲࡨࠩึ")] = bstack1l11ll1_opy_ (u"࠭ࠠࠨื").join(bstack1lll11l111_opy_)
        item[bstack1l11ll1_opy_ (u"ࠧࡪࡰࡧࡩࡽุ࠭")] = 0
        execution_items.append(item)
    bstack1ll1ll1ll1_opy_ = bstack11ll1lllll_opy_(execution_items, bstack1ll1lll1l1_opy_)
    for execution_item in bstack1ll1ll1ll1_opy_:
      bstack11111llll_opy_ = []
      for item in execution_item:
        bstack11111llll_opy_.append(bstack1l1ll11l1l_opy_(name=str(item[bstack1l11ll1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾูࠧ")]),
                                             target=bstack111l111ll_opy_,
                                             args=(item[bstack1l11ll1_opy_ (u"ࠩࡤࡶ࡬ฺ࠭")],)))
      for t in bstack11111llll_opy_:
        t.start()
      for t in bstack11111llll_opy_:
        t.join()
  else:
    bstack1ll1l1l11_opy_(bstack1lll11111_opy_)
  if not bstack1l111ll111_opy_:
    bstack1l1ll11ll1_opy_()
    if(bstack11ll111ll_opy_ in [bstack1l11ll1_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ฻"), bstack1l11ll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ฼")]):
      bstack1llll1lll1_opy_()
  bstack1lll1l1l1l_opy_.bstack1l1ll11l1_opy_()
def browserstack_initialize(bstack1l1lllllll_opy_=None):
  logger.info(bstack1l11ll1_opy_ (u"ࠬࡘࡵ࡯ࡰ࡬ࡲ࡬ࠦࡓࡅࡍࠣࡻ࡮ࡺࡨࠡࡣࡵ࡫ࡸࡀࠠࠨ฽") + str(bstack1l1lllllll_opy_))
  run_on_browserstack(bstack1l1lllllll_opy_, None, True)
@measure(event_name=EVENTS.bstack1lll1ll1l1_opy_, stage=STAGE.bstack11lllll111_opy_, bstack1l11111l1_opy_=bstack1l11111l1l_opy_)
def bstack1l1ll11ll1_opy_():
  global CONFIG
  global bstack1ll1l11l1l_opy_
  global bstack1l11l11l11_opy_
  global bstack11l1lll1_opy_
  global bstack111lllll11_opy_
  bstack1111l1l11_opy_.bstack1l1llllll_opy_()
  if cli.is_running():
    bstack1l1111l1_opy_.invoke(bstack1l11lll111_opy_.bstack1l1111ll_opy_)
  else:
    bstack11ll1lll1_opy_ = bstack11llll1111_opy_.bstack1lll111l1l_opy_(config=CONFIG)
    bstack11ll1lll1_opy_.bstack1llll1l1l1_opy_(CONFIG)
  if bstack1ll1l11l1l_opy_ == bstack1l11ll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭฾"):
    if not cli.is_enabled(CONFIG):
      bstack1l111111l1_opy_.stop()
  else:
    bstack1l111111l1_opy_.stop()
  if not cli.is_enabled(CONFIG):
    bstack11llllllll_opy_.bstack11l1111ll_opy_()
  if bstack1l11ll1_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ฿") in CONFIG and str(CONFIG[bstack1l11ll1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬเ")]).lower() != bstack1l11ll1_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨแ"):
    hashed_id, bstack1lllll111_opy_ = bstack1ll1111ll_opy_()
  else:
    hashed_id, bstack1lllll111_opy_ = get_build_link()
  bstack11l1lll1ll_opy_(hashed_id)
  logger.info(bstack1l11ll1_opy_ (u"ࠪࡗࡉࡑࠠࡳࡷࡱࠤࡪࡴࡤࡦࡦࠣࡪࡴࡸࠠࡪࡦ࠽ࠫโ") + bstack111lllll11_opy_.get_property(bstack1l11ll1_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭ใ"), bstack1l11ll1_opy_ (u"ࠬ࠭ไ")) + bstack1l11ll1_opy_ (u"࠭ࠬࠡࡶࡨࡷࡹ࡮ࡵࡣࠢ࡬ࡨ࠿ࠦࠧๅ") + os.getenv(bstack1l11ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬๆ"), bstack1l11ll1_opy_ (u"ࠨࠩ็")))
  if hashed_id is not None and bstack1111l1l1_opy_() != -1:
    sessions = bstack1llll1l11l_opy_(hashed_id)
    bstack1l11l11111_opy_(sessions, bstack1lllll111_opy_)
  if bstack1ll1l11l1l_opy_ == bstack1l11ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ่ࠩ") and bstack1l11l11l11_opy_ != 0:
    sys.exit(bstack1l11l11l11_opy_)
  if bstack1ll1l11l1l_opy_ == bstack1l11ll1_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧ้ࠪ") and bstack11l1lll1_opy_ != 0:
    sys.exit(bstack11l1lll1_opy_)
def bstack11l1lll1ll_opy_(new_id):
    global bstack1l11l11lll_opy_
    bstack1l11l11lll_opy_ = new_id
def bstack11ll1ll1l_opy_(bstack11lllllll_opy_):
  if bstack11lllllll_opy_:
    return bstack11lllllll_opy_.capitalize()
  else:
    return bstack1l11ll1_opy_ (u"๊ࠫࠬ")
@measure(event_name=EVENTS.bstack11l1l1l11l_opy_, stage=STAGE.bstack11lllll111_opy_, bstack1l11111l1_opy_=bstack1l11111l1l_opy_)
def bstack1ll1ll11l_opy_(bstack111l11l1l_opy_):
  if bstack1l11ll1_opy_ (u"ࠬࡴࡡ࡮ࡧ๋ࠪ") in bstack111l11l1l_opy_ and bstack111l11l1l_opy_[bstack1l11ll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ์")] != bstack1l11ll1_opy_ (u"ࠧࠨํ"):
    return bstack111l11l1l_opy_[bstack1l11ll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭๎")]
  else:
    bstack1l11111l1_opy_ = bstack1l11ll1_opy_ (u"ࠤࠥ๏")
    if bstack1l11ll1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪ๐") in bstack111l11l1l_opy_ and bstack111l11l1l_opy_[bstack1l11ll1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫ๑")] != None:
      bstack1l11111l1_opy_ += bstack111l11l1l_opy_[bstack1l11ll1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬ๒")] + bstack1l11ll1_opy_ (u"ࠨࠬࠡࠤ๓")
      if bstack111l11l1l_opy_[bstack1l11ll1_opy_ (u"ࠧࡰࡵࠪ๔")] == bstack1l11ll1_opy_ (u"ࠣ࡫ࡲࡷࠧ๕"):
        bstack1l11111l1_opy_ += bstack1l11ll1_opy_ (u"ࠤ࡬ࡓࡘࠦࠢ๖")
      bstack1l11111l1_opy_ += (bstack111l11l1l_opy_[bstack1l11ll1_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ๗")] or bstack1l11ll1_opy_ (u"ࠫࠬ๘"))
      return bstack1l11111l1_opy_
    else:
      bstack1l11111l1_opy_ += bstack11ll1ll1l_opy_(bstack111l11l1l_opy_[bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭๙")]) + bstack1l11ll1_opy_ (u"ࠨࠠࠣ๚") + (
              bstack111l11l1l_opy_[bstack1l11ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ๛")] or bstack1l11ll1_opy_ (u"ࠨࠩ๜")) + bstack1l11ll1_opy_ (u"ࠤ࠯ࠤࠧ๝")
      if bstack111l11l1l_opy_[bstack1l11ll1_opy_ (u"ࠪࡳࡸ࠭๞")] == bstack1l11ll1_opy_ (u"ࠦ࡜࡯࡮ࡥࡱࡺࡷࠧ๟"):
        bstack1l11111l1_opy_ += bstack1l11ll1_opy_ (u"ࠧ࡝ࡩ࡯ࠢࠥ๠")
      bstack1l11111l1_opy_ += bstack111l11l1l_opy_[bstack1l11ll1_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪ๡")] or bstack1l11ll1_opy_ (u"ࠧࠨ๢")
      return bstack1l11111l1_opy_
@measure(event_name=EVENTS.bstack1llll1111_opy_, stage=STAGE.bstack11lllll111_opy_, bstack1l11111l1_opy_=bstack1l11111l1l_opy_)
def bstack11ll1l11l_opy_(bstack11llll1l_opy_):
  if bstack11llll1l_opy_ == bstack1l11ll1_opy_ (u"ࠣࡦࡲࡲࡪࠨ๣"):
    return bstack1l11ll1_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾࡬ࡸࡥࡦࡰ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦ࡬ࡸࡥࡦࡰࠥࡂࡈࡵ࡭ࡱ࡮ࡨࡸࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ๤")
  elif bstack11llll1l_opy_ == bstack1l11ll1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ๥"):
    return bstack1l11ll1_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡲࡦࡦ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡷ࡫ࡤࠣࡀࡉࡥ࡮ࡲࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ๦")
  elif bstack11llll1l_opy_ == bstack1l11ll1_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ๧"):
    return bstack1l11ll1_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡩࡵࡩࡪࡴ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡩࡵࡩࡪࡴࠢ࠿ࡒࡤࡷࡸ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭๨")
  elif bstack11llll1l_opy_ == bstack1l11ll1_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨ๩"):
    return bstack1l11ll1_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡶࡪࡪ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡴࡨࡨࠧࡄࡅࡳࡴࡲࡶࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪ๪")
  elif bstack11llll1l_opy_ == bstack1l11ll1_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥ๫"):
    return bstack1l11ll1_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࠩࡥࡦࡣ࠶࠶࠻ࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࠤࡧࡨࡥ࠸࠸࠶ࠣࡀࡗ࡭ࡲ࡫࡯ࡶࡶ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨ๬")
  elif bstack11llll1l_opy_ == bstack1l11ll1_opy_ (u"ࠦࡷࡻ࡮࡯࡫ࡱ࡫ࠧ๭"):
    return bstack1l11ll1_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡣ࡮ࡤࡧࡰࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡣ࡮ࡤࡧࡰࠨ࠾ࡓࡷࡱࡲ࡮ࡴࡧ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭๮")
  else:
    return bstack1l11ll1_opy_ (u"࠭࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡥࡰࡦࡩ࡫࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡥࡰࡦࡩ࡫ࠣࡀࠪ๯") + bstack11ll1ll1l_opy_(
      bstack11llll1l_opy_) + bstack1l11ll1_opy_ (u"ࠧ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭๰")
def bstack11l1l1l11_opy_(session):
  return bstack1l11ll1_opy_ (u"ࠨ࠾ࡷࡶࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡸ࡯ࡸࠤࡁࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠥࡹࡥࡴࡵ࡬ࡳࡳ࠳࡮ࡢ࡯ࡨࠦࡃࡂࡡࠡࡪࡵࡩ࡫ࡃࠢࡼࡿࠥࠤࡹࡧࡲࡨࡧࡷࡁࠧࡥࡢ࡭ࡣࡱ࡯ࠧࡄࡻࡾ࠾࠲ࡥࡃࡂ࠯ࡵࡦࡁࡿࢂࢁࡽ࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿࠳ࡹࡸ࠾ࠨ๱").format(
    session[bstack1l11ll1_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤࡡࡸࡶࡱ࠭๲")], bstack1ll1ll11l_opy_(session), bstack11ll1l11l_opy_(session[bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡸࡦࡺࡵࡴࠩ๳")]),
    bstack11ll1l11l_opy_(session[bstack1l11ll1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ๴")]),
    bstack11ll1ll1l_opy_(session[bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭๵")] or session[bstack1l11ll1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭๶")] or bstack1l11ll1_opy_ (u"ࠧࠨ๷")) + bstack1l11ll1_opy_ (u"ࠣࠢࠥ๸") + (session[bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫ๹")] or bstack1l11ll1_opy_ (u"ࠪࠫ๺")),
    session[bstack1l11ll1_opy_ (u"ࠫࡴࡹࠧ๻")] + bstack1l11ll1_opy_ (u"ࠧࠦࠢ๼") + session[bstack1l11ll1_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪ๽")], session[bstack1l11ll1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩ๾")] or bstack1l11ll1_opy_ (u"ࠨࠩ๿"),
    session[bstack1l11ll1_opy_ (u"ࠩࡦࡶࡪࡧࡴࡦࡦࡢࡥࡹ࠭຀")] if session[bstack1l11ll1_opy_ (u"ࠪࡧࡷ࡫ࡡࡵࡧࡧࡣࡦࡺࠧກ")] else bstack1l11ll1_opy_ (u"ࠫࠬຂ"))
@measure(event_name=EVENTS.bstack1l1l1l1l11_opy_, stage=STAGE.bstack11lllll111_opy_, bstack1l11111l1_opy_=bstack1l11111l1l_opy_)
def bstack1l11l11111_opy_(sessions, bstack1lllll111_opy_):
  try:
    bstack11lll1lll_opy_ = bstack1l11ll1_opy_ (u"ࠧࠨ຃")
    if not os.path.exists(bstack11l1ll111l_opy_):
      os.mkdir(bstack11l1ll111l_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l11ll1_opy_ (u"࠭ࡡࡴࡵࡨࡸࡸ࠵ࡲࡦࡲࡲࡶࡹ࠴ࡨࡵ࡯࡯ࠫຄ")), bstack1l11ll1_opy_ (u"ࠧࡳࠩ຅")) as f:
      bstack11lll1lll_opy_ = f.read()
    bstack11lll1lll_opy_ = bstack11lll1lll_opy_.replace(bstack1l11ll1_opy_ (u"ࠨࡽࠨࡖࡊ࡙ࡕࡍࡖࡖࡣࡈࡕࡕࡏࡖࠨࢁࠬຆ"), str(len(sessions)))
    bstack11lll1lll_opy_ = bstack11lll1lll_opy_.replace(bstack1l11ll1_opy_ (u"ࠩࡾࠩࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠥࡾࠩງ"), bstack1lllll111_opy_)
    bstack11lll1lll_opy_ = bstack11lll1lll_opy_.replace(bstack1l11ll1_opy_ (u"ࠪࡿࠪࡈࡕࡊࡎࡇࡣࡓࡇࡍࡆࠧࢀࠫຈ"),
                                              sessions[0].get(bstack1l11ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡲࡦࡳࡥࠨຉ")) if sessions[0] else bstack1l11ll1_opy_ (u"ࠬ࠭ຊ"))
    with open(os.path.join(bstack11l1ll111l_opy_, bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡸࡥࡱࡱࡵࡸ࠳࡮ࡴ࡮࡮ࠪ຋")), bstack1l11ll1_opy_ (u"ࠧࡸࠩຌ")) as stream:
      stream.write(bstack11lll1lll_opy_.split(bstack1l11ll1_opy_ (u"ࠨࡽࠨࡗࡊ࡙ࡓࡊࡑࡑࡗࡤࡊࡁࡕࡃࠨࢁࠬຍ"))[0])
      for session in sessions:
        stream.write(bstack11l1l1l11_opy_(session))
      stream.write(bstack11lll1lll_opy_.split(bstack1l11ll1_opy_ (u"ࠩࡾࠩࡘࡋࡓࡔࡋࡒࡒࡘࡥࡄࡂࡖࡄࠩࢂ࠭ຎ"))[1])
    logger.info(bstack1l11ll1_opy_ (u"ࠪࡋࡪࡴࡥࡳࡣࡷࡩࡩࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡨࡵࡪ࡮ࡧࠤࡦࡸࡴࡪࡨࡤࡧࡹࡹࠠࡢࡶࠣࡿࢂ࠭ຏ").format(bstack11l1ll111l_opy_));
  except Exception as e:
    logger.debug(bstack1ll11ll11l_opy_.format(str(e)))
def bstack1llll1l11l_opy_(hashed_id):
  global CONFIG
  try:
    bstack1l11ll1ll_opy_ = datetime.datetime.now()
    host = bstack1l11ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠯ࡦࡰࡴࡻࡤ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫຐ") if bstack1l11ll1_opy_ (u"ࠬࡧࡰࡱࠩຑ") in CONFIG else bstack1l11ll1_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡲ࡬࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧຒ")
    user = CONFIG[bstack1l11ll1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩຓ")]
    key = CONFIG[bstack1l11ll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫດ")]
    bstack11ll1lll_opy_ = bstack1l11ll1_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨຕ") if bstack1l11ll1_opy_ (u"ࠪࡥࡵࡶࠧຖ") in CONFIG else (bstack1l11ll1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨທ") if CONFIG.get(bstack1l11ll1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩຘ")) else bstack1l11ll1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨນ"))
    host = bstack1ll1111l1l_opy_(cli.config, [bstack1l11ll1_opy_ (u"ࠢࡢࡲ࡬ࡷࠧບ"), bstack1l11ll1_opy_ (u"ࠣࡣࡳࡴࡆࡻࡴࡰ࡯ࡤࡸࡪࠨປ"), bstack1l11ll1_opy_ (u"ࠤࡤࡴ࡮ࠨຜ")], host) if bstack1l11ll1_opy_ (u"ࠪࡥࡵࡶࠧຝ") in CONFIG else bstack1ll1111l1l_opy_(cli.config, [bstack1l11ll1_opy_ (u"ࠦࡦࡶࡩࡴࠤພ"), bstack1l11ll1_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫ࠢຟ"), bstack1l11ll1_opy_ (u"ࠨࡡࡱ࡫ࠥຠ")], host)
    url = bstack1l11ll1_opy_ (u"ࠧࡼࡿ࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾ࠱ࡶࡩࡸࡹࡩࡰࡰࡶ࠲࡯ࡹ࡯࡯ࠩມ").format(host, bstack11ll1lll_opy_, hashed_id)
    headers = {
      bstack1l11ll1_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧຢ"): bstack1l11ll1_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬຣ"),
    }
    proxies = bstack11llllll11_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies, auth=(user, key))
    if response.json():
      cli.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻ࡩࡨࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡹ࡟࡭࡫ࡶࡸࠧ຤"), datetime.datetime.now() - bstack1l11ll1ll_opy_)
      return list(map(lambda session: session[bstack1l11ll1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩລ")], response.json()))
  except Exception as e:
    logger.debug(bstack111llll1_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack1ll1111111_opy_, stage=STAGE.bstack11lllll111_opy_, bstack1l11111l1_opy_=bstack1l11111l1l_opy_)
def get_build_link():
  global CONFIG
  global bstack1l11l11lll_opy_
  try:
    if bstack1l11ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ຦") in CONFIG:
      bstack1l11ll1ll_opy_ = datetime.datetime.now()
      host = bstack1l11ll1_opy_ (u"࠭ࡡࡱ࡫࠰ࡧࡱࡵࡵࡥࠩວ") if bstack1l11ll1_opy_ (u"ࠧࡢࡲࡳࠫຨ") in CONFIG else bstack1l11ll1_opy_ (u"ࠨࡣࡳ࡭ࠬຩ")
      user = CONFIG[bstack1l11ll1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫສ")]
      key = CONFIG[bstack1l11ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ຫ")]
      bstack11ll1lll_opy_ = bstack1l11ll1_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪຬ") if bstack1l11ll1_opy_ (u"ࠬࡧࡰࡱࠩອ") in CONFIG else bstack1l11ll1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨຮ")
      url = bstack1l11ll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡽࢀ࠾ࢀࢃࡀࡼࡿ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠰࡭ࡷࡴࡴࠧຯ").format(user, key, host, bstack11ll1lll_opy_)
      if cli.is_enabled(CONFIG):
        bstack1lllll111_opy_, hashed_id = cli.bstack1l111llll_opy_()
        logger.info(bstack1l111l1l1_opy_.format(bstack1lllll111_opy_))
        return [hashed_id, bstack1lllll111_opy_]
      else:
        headers = {
          bstack1l11ll1_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧະ"): bstack1l11ll1_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬັ"),
        }
        if bstack1l11ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬາ") in CONFIG:
          params = {bstack1l11ll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩຳ"): CONFIG[bstack1l11ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨິ")], bstack1l11ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩີ"): CONFIG[bstack1l11ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩຶ")]}
        else:
          params = {bstack1l11ll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ື"): CONFIG[bstack1l11ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩຸࠬ")]}
        proxies = bstack11llllll11_opy_(CONFIG, url)
        response = requests.get(url, params=params, headers=headers, proxies=proxies)
        if response.json():
          bstack11l1ll1l1_opy_ = response.json()[0][bstack1l11ll1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡣࡷ࡬ࡰࡩູ࠭")]
          if bstack11l1ll1l1_opy_:
            bstack1lllll111_opy_ = bstack11l1ll1l1_opy_[bstack1l11ll1_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦࡣࡺࡸ࡬ࠨ຺")].split(bstack1l11ll1_opy_ (u"ࠬࡶࡵࡣ࡮࡬ࡧ࠲ࡨࡵࡪ࡮ࡧࠫົ"))[0] + bstack1l11ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡸ࠵ࠧຼ") + bstack11l1ll1l1_opy_[
              bstack1l11ll1_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪຽ")]
            logger.info(bstack1l111l1l1_opy_.format(bstack1lllll111_opy_))
            bstack1l11l11lll_opy_ = bstack11l1ll1l1_opy_[bstack1l11ll1_opy_ (u"ࠨࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ຾")]
            bstack1ll111l11l_opy_ = CONFIG[bstack1l11ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ຿")]
            if bstack1l11ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬເ") in CONFIG:
              bstack1ll111l11l_opy_ += bstack1l11ll1_opy_ (u"ࠫࠥ࠭ແ") + CONFIG[bstack1l11ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧໂ")]
            if bstack1ll111l11l_opy_ != bstack11l1ll1l1_opy_[bstack1l11ll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫໃ")]:
              logger.debug(bstack1ll1lll11_opy_.format(bstack11l1ll1l1_opy_[bstack1l11ll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬໄ")], bstack1ll111l11l_opy_))
            cli.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠣࡪࡷࡸࡵࡀࡧࡦࡶࡢࡦࡺ࡯࡬ࡥࡡ࡯࡭ࡳࡱࠢ໅"), datetime.datetime.now() - bstack1l11ll1ll_opy_)
            return [bstack11l1ll1l1_opy_[bstack1l11ll1_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬໆ")], bstack1lllll111_opy_]
    else:
      logger.warn(bstack1ll111llll_opy_)
  except Exception as e:
    logger.debug(bstack11lll11l1l_opy_.format(str(e)))
  return [None, None]
def bstack1l11l111_opy_(url, bstack1lll111l_opy_=False):
  global CONFIG
  global bstack1lll1l1ll_opy_
  if not bstack1lll1l1ll_opy_:
    hostname = bstack1l1l1l11ll_opy_(url)
    is_private = bstack111l1l1l1_opy_(hostname)
    if (bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ໇") in CONFIG and not bstack11l1ll11l1_opy_(CONFIG[bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ່")])) and (is_private or bstack1lll111l_opy_):
      bstack1lll1l1ll_opy_ = hostname
def bstack1l1l1l11ll_opy_(url):
  return urlparse(url).hostname
def bstack111l1l1l1_opy_(hostname):
  for bstack1l1l11lll1_opy_ in bstack11l11l1lll_opy_:
    regex = re.compile(bstack1l1l11lll1_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1ll1l1ll1_opy_(bstack1111l1ll_opy_):
  return True if bstack1111l1ll_opy_ in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack1ll11l1111_opy_, stage=STAGE.bstack11lllll111_opy_, bstack1l11111l1_opy_=bstack1l11111l1l_opy_)
def getAccessibilityResults(driver):
  global CONFIG
  global bstack11ll1llll_opy_
  bstack11ll1ll11l_opy_ = not (bstack1l11111ll_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵ້ࠩ"), None) and bstack1l11111ll_opy_(
          threading.current_thread(), bstack1l11ll1_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱ໊ࠬ"), None))
  bstack1l1l1l11l1_opy_ = getattr(driver, bstack1l11ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴ໋ࠧ"), None) != True
  bstack11llll1ll_opy_ = bstack1l11111ll_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ໌"), None) and bstack1l11111ll_opy_(
          threading.current_thread(), bstack1l11ll1_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫໍ"), None)
  if bstack11llll1ll_opy_:
    if not bstack1l11l1l11l_opy_():
      logger.warning(bstack1l11ll1_opy_ (u"ࠥࡒࡴࡺࠠࡢࡰࠣࡅࡵࡶࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࠡࡃࡳࡴࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸ࠴ࠢ໎"))
      return {}
    logger.debug(bstack1l11ll1_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡢࡦࡨࡲࡶࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡳࡧࡶࡹࡱࡺࡳࠨ໏"))
    logger.debug(perform_scan(driver, driver_command=bstack1l11ll1_opy_ (u"ࠬ࡫ࡸࡦࡥࡸࡸࡪ࡙ࡣࡳ࡫ࡳࡸࠬ໐")))
    results = bstack1ll1l1ll11_opy_(bstack1l11ll1_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹࡹࠢ໑"))
    if results is not None and results.get(bstack1l11ll1_opy_ (u"ࠢࡪࡵࡶࡹࡪࡹࠢ໒")) is not None:
        return results[bstack1l11ll1_opy_ (u"ࠣ࡫ࡶࡷࡺ࡫ࡳࠣ໓")]
    logger.error(bstack1l11ll1_opy_ (u"ࠤࡑࡳࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡘࡥࡴࡷ࡯ࡸࡸࠦࡷࡦࡴࡨࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦ໔"))
    return []
  if not bstack11lll1ll1l_opy_.bstack1l1l11l111_opy_(CONFIG, bstack11ll1llll_opy_) or (bstack1l1l1l11l1_opy_ and bstack11ll1ll11l_opy_):
    logger.warning(bstack1l11ll1_opy_ (u"ࠥࡒࡴࡺࠠࡢࡰࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷ࠳ࠨ໕"))
    return {}
  try:
    logger.debug(bstack1l11ll1_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡢࡦࡨࡲࡶࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡳࡧࡶࡹࡱࡺࡳࠨ໖"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack1l11l11l_opy_.bstack1l1l111l1l_opy_)
    return results
  except Exception:
    logger.error(bstack1l11ll1_opy_ (u"ࠧࡔ࡯ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡺࡩࡷ࡫ࠠࡧࡱࡸࡲࡩ࠴ࠢ໗"))
    return {}
@measure(event_name=EVENTS.bstack111l1lll1_opy_, stage=STAGE.bstack11lllll111_opy_, bstack1l11111l1_opy_=bstack1l11111l1l_opy_)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack11ll1llll_opy_
  bstack11ll1ll11l_opy_ = not (bstack1l11111ll_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ໘"), None) and bstack1l11111ll_opy_(
          threading.current_thread(), bstack1l11ll1_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭໙"), None))
  bstack1l1l1l11l1_opy_ = getattr(driver, bstack1l11ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ໚"), None) != True
  bstack11llll1ll_opy_ = bstack1l11111ll_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ໛"), None) and bstack1l11111ll_opy_(
          threading.current_thread(), bstack1l11ll1_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬໜ"), None)
  if bstack11llll1ll_opy_:
    if not bstack1l11l1l11l_opy_():
      logger.warning(bstack1l11ll1_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡶࡰࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡄࡴࡵࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡴࡷࡰࡱࡦࡸࡹ࠯ࠤໝ"))
      return {}
    logger.debug(bstack1l11ll1_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡴࡨࡷࡺࡲࡴࡴࠢࡶࡹࡲࡳࡡࡳࡻࠪໞ"))
    logger.debug(perform_scan(driver, driver_command=bstack1l11ll1_opy_ (u"࠭ࡥࡹࡧࡦࡹࡹ࡫ࡓࡤࡴ࡬ࡴࡹ࠭ໟ")))
    results = bstack1ll1l1ll11_opy_(bstack1l11ll1_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡓࡶ࡯ࡰࡥࡷࡿࠢ໠"))
    if results is not None and results.get(bstack1l11ll1_opy_ (u"ࠣࡵࡸࡱࡲࡧࡲࡺࠤ໡")) is not None:
        return results[bstack1l11ll1_opy_ (u"ࠤࡶࡹࡲࡳࡡࡳࡻࠥ໢")]
    logger.error(bstack1l11ll1_opy_ (u"ࠥࡒࡴࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡒࡦࡵࡸࡰࡹࡹࠠࡔࡷࡰࡱࡦࡸࡹࠡࡹࡤࡷࠥ࡬࡯ࡶࡰࡧ࠲ࠧ໣"))
    return {}
  if not bstack11lll1ll1l_opy_.bstack1l1l11l111_opy_(CONFIG, bstack11ll1llll_opy_) or (bstack1l1l1l11l1_opy_ and bstack11ll1ll11l_opy_):
    logger.warning(bstack1l11ll1_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡪࡺࡲࡪࡧࡹࡩࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡳࡶ࡯ࡰࡥࡷࡿ࠮ࠣ໤"))
    return {}
  try:
    logger.debug(bstack1l11ll1_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡴࡨࡷࡺࡲࡴࡴࠢࡶࡹࡲࡳࡡࡳࡻࠪ໥"))
    logger.debug(perform_scan(driver))
    bstack1111lllll_opy_ = driver.execute_async_script(bstack1l11l11l_opy_.bstack11l11111l1_opy_)
    return bstack1111lllll_opy_
  except Exception:
    logger.error(bstack1l11ll1_opy_ (u"ࠨࡎࡰࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡹࡲࡳࡡࡳࡻࠣࡻࡦࡹࠠࡧࡱࡸࡲࡩ࠴ࠢ໦"))
    return {}
def bstack1l11l1l11l_opy_():
  global CONFIG
  global bstack11ll1llll_opy_
  bstack1ll11ll11_opy_ = bstack1l11111ll_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ໧"), None) and bstack1l11111ll_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ໨"), None)
  if not bstack11lll1ll1l_opy_.bstack1l1l11l111_opy_(CONFIG, bstack11ll1llll_opy_) or not bstack1ll11ll11_opy_:
        logger.warning(bstack1l11ll1_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡴࡵࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡳࡧࡶࡹࡱࡺࡳ࠯ࠤ໩"))
        return False
  return True
def bstack1ll1l1ll11_opy_(bstack1l11l1l1l_opy_):
    bstack111ll11l_opy_ = bstack1l111111l1_opy_.current_test_uuid() if bstack1l111111l1_opy_.current_test_uuid() else bstack11llllllll_opy_.current_hook_uuid()
    with ThreadPoolExecutor() as executor:
        future = executor.submit(bstack11lll111l1_opy_(bstack111ll11l_opy_, bstack1l11l1l1l_opy_))
        try:
            return future.result(timeout=bstack1llll111l_opy_)
        except TimeoutError:
            logger.error(bstack1l11ll1_opy_ (u"ࠥࡘ࡮ࡳࡥࡰࡷࡷࠤࡦ࡬ࡴࡦࡴࠣࡿࢂࡹࠠࡸࡪ࡬ࡰࡪࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡔࡨࡷࡺࡲࡴࡴࠤ໪").format(bstack1llll111l_opy_))
        except Exception as ex:
            logger.debug(bstack1l11ll1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡶࡪࡺࡲࡪࡧࡹ࡭ࡳ࡭ࠠࡂࡲࡳࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡽࢀ࠲ࠥࡋࡲࡳࡱࡵࠤ࠲ࠦࡻࡾࠤ໫").format(bstack1l11l1l1l_opy_, str(ex)))
    return {}
@measure(event_name=EVENTS.bstack1l1l1l1ll_opy_, stage=STAGE.bstack11lllll111_opy_, bstack1l11111l1_opy_=bstack1l11111l1l_opy_)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack11ll1llll_opy_
  bstack11ll1ll11l_opy_ = not (bstack1l11111ll_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ໬"), None) and bstack1l11111ll_opy_(
          threading.current_thread(), bstack1l11ll1_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ໭"), None))
  bstack11l11l111_opy_ = not (bstack1l11111ll_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ໮"), None) and bstack1l11111ll_opy_(
          threading.current_thread(), bstack1l11ll1_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ໯"), None))
  bstack1l1l1l11l1_opy_ = getattr(driver, bstack1l11ll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩ໰"), None) != True
  if not bstack11lll1ll1l_opy_.bstack1l1l11l111_opy_(CONFIG, bstack11ll1llll_opy_) or (bstack1l1l1l11l1_opy_ and bstack11ll1ll11l_opy_ and bstack11l11l111_opy_):
    logger.warning(bstack1l11ll1_opy_ (u"ࠥࡒࡴࡺࠠࡢࡰࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡹࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡤࡣࡱ࠲ࠧ໱"))
    return {}
  try:
    bstack11l11l1l_opy_ = bstack1l11ll1_opy_ (u"ࠫࡦࡶࡰࠨ໲") in CONFIG and CONFIG.get(bstack1l11ll1_opy_ (u"ࠬࡧࡰࡱࠩ໳"), bstack1l11ll1_opy_ (u"࠭ࠧ໴"))
    session_id = getattr(driver, bstack1l11ll1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠫ໵"), None)
    if not session_id:
      logger.warning(bstack1l11ll1_opy_ (u"ࠣࡐࡲࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡏࡄࠡࡨࡲࡹࡳࡪࠠࡧࡱࡵࠤࡩࡸࡩࡷࡧࡵࠦ໶"))
      return {bstack1l11ll1_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣ໷"): bstack1l11ll1_opy_ (u"ࠥࡒࡴࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡊࡆࠣࡪࡴࡻ࡮ࡥࠤ໸")}
    if bstack11l11l1l_opy_:
      try:
        bstack1l1lllll1_opy_ = {
              bstack1l11ll1_opy_ (u"ࠫࡹ࡮ࡊࡸࡶࡗࡳࡰ࡫࡮ࠨ໹"): os.environ.get(bstack1l11ll1_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ໺"), os.environ.get(bstack1l11ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ໻"), bstack1l11ll1_opy_ (u"ࠧࠨ໼"))),
              bstack1l11ll1_opy_ (u"ࠨࡶ࡫ࡘࡪࡹࡴࡓࡷࡱ࡙ࡺ࡯ࡤࠨ໽"): bstack1l111111l1_opy_.current_test_uuid() if bstack1l111111l1_opy_.current_test_uuid() else bstack11llllllll_opy_.current_hook_uuid(),
              bstack1l11ll1_opy_ (u"ࠩࡤࡹࡹ࡮ࡈࡦࡣࡧࡩࡷ࠭໾"): os.environ.get(bstack1l11ll1_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ໿")),
              bstack1l11ll1_opy_ (u"ࠫࡸࡩࡡ࡯ࡖ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫༀ"): str(int(datetime.datetime.now().timestamp() * 1000)),
              bstack1l11ll1_opy_ (u"ࠬࡺࡨࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ༁"): os.environ.get(bstack1l11ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ༂"), bstack1l11ll1_opy_ (u"ࠧࠨ༃")),
              bstack1l11ll1_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࠨ༄"): kwargs.get(bstack1l11ll1_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࡡࡦࡳࡲࡳࡡ࡯ࡦࠪ༅"), None) or bstack1l11ll1_opy_ (u"ࠪࠫ༆")
          }
        if not hasattr(thread_local, bstack1l11ll1_opy_ (u"ࠫࡧࡧࡳࡦࡡࡤࡴࡵࡥࡡ࠲࠳ࡼࡣࡸࡩࡲࡪࡲࡷࠫ༇")):
            scripts = {bstack1l11ll1_opy_ (u"ࠬࡹࡣࡢࡰࠪ༈"): bstack1l11l11l_opy_.perform_scan}
            thread_local.base_app_a11y_script = scripts
        bstack11l1l111_opy_ = copy.deepcopy(thread_local.base_app_a11y_script)
        bstack11l1l111_opy_[bstack1l11ll1_opy_ (u"࠭ࡳࡤࡣࡱࠫ༉")] = bstack11l1l111_opy_[bstack1l11ll1_opy_ (u"ࠧࡴࡥࡤࡲࠬ༊")] % json.dumps(bstack1l1lllll1_opy_)
        bstack1l11l11l_opy_.bstack1lll1l1l11_opy_(bstack11l1l111_opy_)
        bstack1l11l11l_opy_.store()
        bstack1l111l111_opy_ = driver.execute_script(bstack1l11l11l_opy_.perform_scan)
      except Exception as bstack1lll1111l1_opy_:
        logger.info(bstack1l11ll1_opy_ (u"ࠣࡃࡳࡴ࡮ࡻ࡭ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࠣ་") + str(bstack1lll1111l1_opy_))
        bstack1l111l111_opy_ = {bstack1l11ll1_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣ༌"): str(bstack1lll1111l1_opy_)}
    else:
      bstack1l111l111_opy_ = driver.execute_async_script(bstack1l11l11l_opy_.perform_scan, {bstack1l11ll1_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࠪ།"): kwargs.get(bstack1l11ll1_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࡣࡨࡵ࡭࡮ࡣࡱࡨࠬ༎"), None) or bstack1l11ll1_opy_ (u"ࠬ࠭༏")})
    return bstack1l111l111_opy_
  except Exception as err:
    logger.error(bstack1l11ll1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡵࡹࡳࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡤࡣࡱ࠲ࠥࢁࡽࠣ༐").format(str(err)))
    return {}