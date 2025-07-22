# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
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
from browserstack_sdk.bstack1l1l1l11_opy_ import bstack1l1l111l1_opy_
from browserstack_sdk.bstack11ll1ll1ll_opy_ import *
import time
import requests
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.measure import measure
def bstack1lll1l11_opy_():
  global CONFIG
  headers = {
        bstack111l111_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack111l111_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1lllll11l1_opy_(CONFIG, bstack11111l11_opy_)
  try:
    response = requests.get(bstack11111l11_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1ll1ll1l_opy_ = response.json()[bstack111l111_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack11l1l1l1ll_opy_.format(response.json()))
      return bstack1ll1ll1l_opy_
    else:
      logger.debug(bstack1l111l1l1_opy_.format(bstack111l111_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack1l111l1l1_opy_.format(e))
def bstack11ll1lll_opy_(hub_url):
  global CONFIG
  url = bstack111l111_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack111l111_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack111l111_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack111l111_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1lllll11l1_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack11l11l11l_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack11l1l111l_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack11111ll1l_opy_, stage=STAGE.bstack11l1llll1_opy_)
def bstack1l111lllll_opy_():
  try:
    global bstack1l11111l1l_opy_
    bstack1ll1ll1l_opy_ = bstack1lll1l11_opy_()
    bstack1l11l1ll1_opy_ = []
    results = []
    for bstack11l1l11l11_opy_ in bstack1ll1ll1l_opy_:
      bstack1l11l1ll1_opy_.append(bstack1llll1ll1l_opy_(target=bstack11ll1lll_opy_,args=(bstack11l1l11l11_opy_,)))
    for t in bstack1l11l1ll1_opy_:
      t.start()
    for t in bstack1l11l1ll1_opy_:
      results.append(t.join())
    bstack111l1l1l_opy_ = {}
    for item in results:
      hub_url = item[bstack111l111_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack111l111_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack111l1l1l_opy_[hub_url] = latency
    bstack1l11l11111_opy_ = min(bstack111l1l1l_opy_, key= lambda x: bstack111l1l1l_opy_[x])
    bstack1l11111l1l_opy_ = bstack1l11l11111_opy_
    logger.debug(bstack111l1l111_opy_.format(bstack1l11l11111_opy_))
  except Exception as e:
    logger.debug(bstack1ll1l1111_opy_.format(e))
from browserstack_sdk.bstack1l1ll11ll_opy_ import *
from browserstack_sdk.bstack1ll111l111_opy_ import *
from browserstack_sdk.bstack11ll1l1lll_opy_ import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.bstack1l1111ll_opy_ import get_logger
from bstack_utils.measure import measure
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack1111lll11_opy_, stage=STAGE.bstack11l1llll1_opy_)
def bstack11lll111ll_opy_():
    global bstack1l11111l1l_opy_
    try:
        bstack1l111ll1l1_opy_ = bstack1lll11lll_opy_()
        bstack1l1llll1l_opy_(bstack1l111ll1l1_opy_)
        hub_url = bstack1l111ll1l1_opy_.get(bstack111l111_opy_ (u"ࠨࡵࡳ࡮ࠥࢀ"), bstack111l111_opy_ (u"ࠢࠣࢁ"))
        if hub_url.endswith(bstack111l111_opy_ (u"ࠨ࠱ࡺࡨ࠴࡮ࡵࡣࠩࢂ")):
            hub_url = hub_url.rsplit(bstack111l111_opy_ (u"ࠩ࠲ࡻࡩ࠵ࡨࡶࡤࠪࢃ"), 1)[0]
        if hub_url.startswith(bstack111l111_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫࢄ")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack111l111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࠭ࢅ")):
            hub_url = hub_url[8:]
        bstack1l11111l1l_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack1lll11lll_opy_():
    global CONFIG
    bstack1l11l11l1_opy_ = CONFIG.get(bstack111l111_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢆ"), {}).get(bstack111l111_opy_ (u"࠭ࡧࡳ࡫ࡧࡒࡦࡳࡥࠨࢇ"), bstack111l111_opy_ (u"ࠧࡏࡑࡢࡋࡗࡏࡄࡠࡐࡄࡑࡊࡥࡐࡂࡕࡖࡉࡉ࠭࢈"))
    if not isinstance(bstack1l11l11l1_opy_, str):
        raise ValueError(bstack111l111_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡈࡴ࡬ࡨࠥࡴࡡ࡮ࡧࠣࡱࡺࡹࡴࠡࡤࡨࠤࡦࠦࡶࡢ࡮࡬ࡨࠥࡹࡴࡳ࡫ࡱ࡫ࠧࢉ"))
    try:
        bstack1l111ll1l1_opy_ = bstack11llll11l1_opy_(bstack1l11l11l1_opy_)
        return bstack1l111ll1l1_opy_
    except Exception as e:
        logger.error(bstack111l111_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣࢊ").format(str(e)))
        return {}
def bstack11llll11l1_opy_(bstack1l11l11l1_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack111l111_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࢋ")] or not CONFIG[bstack111l111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧࢌ")]:
            raise ValueError(bstack111l111_opy_ (u"ࠧࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠠࡰࡴࠣࡥࡨࡩࡥࡴࡵࠣ࡯ࡪࡿࠢࢍ"))
        url = bstack11lll11l_opy_ + bstack1l11l11l1_opy_
        auth = (CONFIG[bstack111l111_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨࢎ")], CONFIG[bstack111l111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ࢏")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack11ll1ll1l1_opy_ = json.loads(response.text)
            return bstack11ll1ll1l1_opy_
    except ValueError as ve:
        logger.error(bstack111l111_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣ࢐").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack111l111_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥ࡭ࡲࡪࡦࠣࡨࡪࡺࡡࡪ࡮ࡶࠤ࠿ࠦࡻࡾࠤ࢑").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack1l1llll1l_opy_(bstack11l11ll11_opy_):
    global CONFIG
    if bstack111l111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ࢒") not in CONFIG or str(CONFIG[bstack111l111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ࢓")]).lower() == bstack111l111_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ࢔"):
        CONFIG[bstack111l111_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬ࢕")] = False
    elif bstack111l111_opy_ (u"ࠧࡪࡵࡗࡶ࡮ࡧ࡬ࡈࡴ࡬ࡨࠬ࢖") in bstack11l11ll11_opy_:
        bstack1l11l111l_opy_ = CONFIG.get(bstack111l111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢗ"), {})
        logger.debug(bstack111l111_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡰࡴࡩࡡ࡭ࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࠪࡹࠢ࢘"), bstack1l11l111l_opy_)
        bstack1l1111llll_opy_ = bstack11l11ll11_opy_.get(bstack111l111_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡕࡩࡵ࡫ࡡࡵࡧࡵࡷ࢙ࠧ"), [])
        bstack111111ll1_opy_ = bstack111l111_opy_ (u"ࠦ࠱ࠨ࢚").join(bstack1l1111llll_opy_)
        logger.debug(bstack111l111_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡈࡻࡳࡵࡱࡰࠤࡷ࡫ࡰࡦࡣࡷࡩࡷࠦࡳࡵࡴ࡬ࡲ࡬ࡀࠠࠦࡵ࢛ࠥ"), bstack111111ll1_opy_)
        bstack1l1ll111l_opy_ = {
            bstack111l111_opy_ (u"ࠨ࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣ࢜"): bstack111l111_opy_ (u"ࠢࡢࡶࡶ࠱ࡷ࡫ࡰࡦࡣࡷࡩࡷࠨ࢝"),
            bstack111l111_opy_ (u"ࠣࡨࡲࡶࡨ࡫ࡌࡰࡥࡤࡰࠧ࢞"): bstack111l111_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ࢟"),
            bstack111l111_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠧࢠ"): bstack111111ll1_opy_
        }
        bstack1l11l111l_opy_.update(bstack1l1ll111l_opy_)
        logger.debug(bstack111l111_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼࡙ࠣࡵࡪࡡࡵࡧࡧࠤࡱࡵࡣࡢ࡮ࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࠫࡳࠣࢡ"), bstack1l11l111l_opy_)
        CONFIG[bstack111l111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢢ")] = bstack1l11l111l_opy_
        logger.debug(bstack111l111_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡌࡩ࡯ࡣ࡯ࠤࡈࡕࡎࡇࡋࡊ࠾ࠥࠫࡳࠣࢣ"), CONFIG)
def bstack1l1ll11lll_opy_():
    bstack1l111ll1l1_opy_ = bstack1lll11lll_opy_()
    if not bstack1l111ll1l1_opy_[bstack111l111_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࡙ࡷࡲࠧࢤ")]:
      raise ValueError(bstack111l111_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࡚ࡸ࡬ࠡ࡫ࡶࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࡬ࡲࡰ࡯ࠣ࡫ࡷ࡯ࡤࠡࡦࡨࡸࡦ࡯࡬ࡴ࠰ࠥࢥ"))
    return bstack1l111ll1l1_opy_[bstack111l111_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࡛ࡲ࡭ࠩࢦ")] + bstack111l111_opy_ (u"ࠪࡃࡨࡧࡰࡴ࠿ࠪࢧ")
@measure(event_name=EVENTS.bstack1l1ll111_opy_, stage=STAGE.bstack11l1llll1_opy_)
def bstack1ll111l1l_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack111l111_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ࢨ")], CONFIG[bstack111l111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࢩ")])
        url = bstack11l1l1lll_opy_
        logger.debug(bstack111l111_opy_ (u"ࠨࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬ࡲࡰ࡯ࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡗࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࠦࡁࡑࡋࠥࢪ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack111l111_opy_ (u"ࠢࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪࠨࢫ"): bstack111l111_opy_ (u"ࠣࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠦࢬ")})
            if response.status_code == 200:
                bstack1ll1lllll1_opy_ = json.loads(response.text)
                bstack1ll11111ll_opy_ = bstack1ll1lllll1_opy_.get(bstack111l111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡴࠩࢭ"), [])
                if bstack1ll11111ll_opy_:
                    bstack1l1l1ll11l_opy_ = bstack1ll11111ll_opy_[0]
                    build_hashed_id = bstack1l1l1ll11l_opy_.get(bstack111l111_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ࢮ"))
                    bstack1l11l11lll_opy_ = bstack1ll1lll111_opy_ + build_hashed_id
                    result.extend([build_hashed_id, bstack1l11l11lll_opy_])
                    logger.info(bstack11lll1ll11_opy_.format(bstack1l11l11lll_opy_))
                    bstack1l1l1ll1_opy_ = CONFIG[bstack111l111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧࢯ")]
                    if bstack111l111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢰ") in CONFIG:
                      bstack1l1l1ll1_opy_ += bstack111l111_opy_ (u"࠭ࠠࠨࢱ") + CONFIG[bstack111l111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࢲ")]
                    if bstack1l1l1ll1_opy_ != bstack1l1l1ll11l_opy_.get(bstack111l111_opy_ (u"ࠨࡰࡤࡱࡪ࠭ࢳ")):
                      logger.debug(bstack11ll11ll1_opy_.format(bstack1l1l1ll11l_opy_.get(bstack111l111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧࢴ")), bstack1l1l1ll1_opy_))
                    return result
                else:
                    logger.debug(bstack111l111_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡑࡳࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡵࡪࡨࠤࡷ࡫ࡳࡱࡱࡱࡷࡪ࠴ࠢࢵ"))
            else:
                logger.debug(bstack111l111_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢶ"))
        except Exception as e:
            logger.error(bstack111l111_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࡹࠠ࠻ࠢࡾࢁࠧࢷ").format(str(e)))
    else:
        logger.debug(bstack111l111_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡉࡏࡏࡈࡌࡋࠥ࡯ࡳࠡࡰࡲࡸࠥࡹࡥࡵ࠰࡙ࠣࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢸ"))
    return [None, None]
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1ll1l1ll1l_opy_ import bstack1ll1l1ll1l_opy_, bstack111ll1ll_opy_, bstack11ll1l11l1_opy_, bstack1l11ll1l11_opy_
from bstack_utils.measure import bstack1ll11l1lll_opy_
from bstack_utils.measure import measure
from bstack_utils.percy import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack11llllllll_opy_ import bstack1ll11l11l_opy_
from bstack_utils.messages import *
from bstack_utils import bstack1l1111ll_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1l1111l1ll_opy_, bstack1llll111l_opy_, bstack1l1ll11l1_opy_, bstack1ll11lllll_opy_, \
  bstack1lllll1lll_opy_, \
  Notset, bstack1l11ll11l_opy_, \
  bstack111ll11ll_opy_, bstack1l1llll111_opy_, bstack1l1111l11_opy_, bstack1ll1l11111_opy_, bstack11l1l11l_opy_, bstack1l1llll1l1_opy_, \
  bstack1ll1l1l11_opy_, \
  bstack1llll1ll11_opy_, bstack11lll1l1_opy_, bstack11l111111_opy_, bstack1l1l1l1ll1_opy_, \
  bstack1ll1ll1111_opy_, bstack11l111l1l_opy_, bstack1ll111l11l_opy_, bstack11ll11l11_opy_
from bstack_utils.bstack111111ll_opy_ import bstack1ll1l1ll_opy_
from bstack_utils.bstack1ll1ll1l1l_opy_ import bstack1l1111l1l1_opy_, bstack11l11l1ll_opy_
from bstack_utils.bstack11l11l11_opy_ import bstack1ll11l1l1l_opy_
from bstack_utils.bstack1l1lllllll_opy_ import bstack1l11ll11ll_opy_, bstack1lllllll1_opy_
from bstack_utils.bstack111lll1ll_opy_ import bstack111lll1ll_opy_
from bstack_utils.bstack1l1l1lllll_opy_ import bstack11111llll_opy_
from bstack_utils.proxy import bstack1111ll11_opy_, bstack1lllll11l1_opy_, bstack1l111ll111_opy_, bstack11ll11l1_opy_
from bstack_utils.bstack1l1l11111_opy_ import bstack11ll1llll1_opy_
import bstack_utils.bstack1ll11ll11l_opy_ as bstack1l1ll1l1ll_opy_
import bstack_utils.bstack1ll111l11_opy_ as bstack1llll1ll_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.utils.bstack1111lll1l_opy_ import bstack1lll1ll1ll_opy_
from bstack_utils.bstack1lll1111ll_opy_ import bstack11llllll_opy_
from bstack_utils.bstack11ll11ll11_opy_ import bstack1ll1lll1_opy_
if os.getenv(bstack111l111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡌࡔࡕࡋࡔࠩࢹ")):
  cli.bstack1ll1111lll_opy_()
else:
  os.environ[bstack111l111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡍࡕࡏࡌࡕࠪࢺ")] = bstack111l111_opy_ (u"ࠩࡷࡶࡺ࡫ࠧࢻ")
bstack11l111l1ll_opy_ = bstack111l111_opy_ (u"ࠪࠤࠥ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࠣࠤ࡮࡬ࠨࡱࡣࡪࡩࠥࡃ࠽࠾ࠢࡹࡳ࡮ࡪࠠ࠱ࠫࠣࡿࡡࡴࠠࠡࠢࡷࡶࡾࢁ࡜࡯ࠢࡦࡳࡳࡹࡴࠡࡨࡶࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨ࡝ࠩࡩࡷࡡ࠭ࠩ࠼࡞ࡱࠤࠥࠦࠠࠡࡨࡶ࠲ࡦࡶࡰࡦࡰࡧࡊ࡮ࡲࡥࡔࡻࡱࡧ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪ࠯ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡶ࡟ࡪࡰࡧࡩࡽ࠯ࠠࠬࠢࠥ࠾ࠧࠦࠫࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࠨࡢࡹࡤ࡭ࡹࠦ࡮ࡦࡹࡓࡥ࡬࡫࠲࠯ࡧࡹࡥࡱࡻࡡࡵࡧࠫࠦ࠭࠯ࠠ࠾ࡀࠣࡿࢂࠨࠬࠡ࡞ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥ࡫ࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡄࡦࡶࡤ࡭ࡱࡹࠢࡾ࡞ࠪ࠭࠮࠯࡛ࠣࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠦࡢ࠯ࠠࠬࠢࠥ࠰ࡡࡢ࡮ࠣࠫ࡟ࡲࠥࠦࠠࠡࡿࡦࡥࡹࡩࡨࠩࡧࡻ࠭ࢀࡢ࡮ࠡࠢࠣࠤࢂࡢ࡮ࠡࠢࢀࡠࡳࠦࠠ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱ࠪࢼ")
bstack11l1111l1_opy_ = bstack111l111_opy_ (u"ࠫࡡࡴ࠯ࠫࠢࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࠦࠪ࠰࡞ࡱࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠶ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡩࡡࡱࡵࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠷࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡲࡢ࡭ࡳࡪࡥࡹࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠷ࡣ࡜࡯ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯ࡵ࡯࡭ࡨ࡫ࠨ࠱࠮ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸࠯࡜࡯ࡥࡲࡲࡸࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯ࠥࡃࠠࡳࡧࡴࡹ࡮ࡸࡥࠩࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨࠩ࠼࡞ࡱ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡰࡦࡻ࡮ࡤࡪࠣࡁࠥࡧࡳࡺࡰࡦࠤ࠭ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷ࠮ࠦ࠽࠿ࠢࡾࡠࡳࡲࡥࡵࠢࡦࡥࡵࡹ࠻࡝ࡰࡷࡶࡾࠦࡻ࡝ࡰࡦࡥࡵࡹࠠ࠾ࠢࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࡢࡴࡶࡤࡧࡰࡥࡣࡢࡲࡶ࠭ࡡࡴࠠࠡࡿࠣࡧࡦࡺࡣࡩࠪࡨࡼ࠮ࠦࡻ࡝ࡰࠣࠤࠥࠦࡽ࡝ࡰࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࠻ࠢࡣࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠩࢁࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭ࢂࡦࠬ࡝ࡰࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴ࡞ࡱࠤࠥࢃࠩ࡝ࡰࢀࡠࡳ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࠪࢽ")
from ._version import __version__
bstack111111111_opy_ = None
CONFIG = {}
bstack11ll111111_opy_ = {}
bstack1l11l11l_opy_ = {}
bstack11l11ll11l_opy_ = None
bstack111lll11_opy_ = None
bstack1ll1l11l1l_opy_ = None
bstack1l11lllll_opy_ = -1
bstack1l1l11l1l1_opy_ = 0
bstack1ll1l111l_opy_ = bstack11l1ll11ll_opy_
bstack1l111ll1ll_opy_ = 1
bstack1l11l11l1l_opy_ = False
bstack1lll1lll11_opy_ = False
bstack11l1l1ll1l_opy_ = bstack111l111_opy_ (u"ࠬ࠭ࢾ")
bstack1l11ll1ll1_opy_ = bstack111l111_opy_ (u"࠭ࠧࢿ")
bstack1l11111lll_opy_ = False
bstack11l1l111_opy_ = True
bstack1lll1l1ll1_opy_ = bstack111l111_opy_ (u"ࠧࠨࣀ")
bstack11ll1lllll_opy_ = []
bstack11lllllll_opy_ = threading.Lock()
bstack1llll11lll_opy_ = threading.Lock()
bstack1l11111l1l_opy_ = bstack111l111_opy_ (u"ࠨࠩࣁ")
bstack1lllllll11_opy_ = False
bstack11l1ll1l11_opy_ = None
bstack1ll1ll111l_opy_ = None
bstack1l11l1lll1_opy_ = None
bstack11l1ll1111_opy_ = -1
bstack1l111111ll_opy_ = os.path.join(os.path.expanduser(bstack111l111_opy_ (u"ࠩࢁࠫࣂ")), bstack111l111_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪࣃ"), bstack111l111_opy_ (u"ࠫ࠳ࡸ࡯ࡣࡱࡷ࠱ࡷ࡫ࡰࡰࡴࡷ࠱࡭࡫࡬ࡱࡧࡵ࠲࡯ࡹ࡯࡯ࠩࣄ"))
bstack11l1ll1ll_opy_ = 0
bstack11llll1l1_opy_ = 0
bstack11lll1ll_opy_ = []
bstack1111l1l1l_opy_ = []
bstack1111ll1ll_opy_ = []
bstack1llll1l1_opy_ = []
bstack11llll1ll1_opy_ = bstack111l111_opy_ (u"ࠬ࠭ࣅ")
bstack1ll1111ll_opy_ = bstack111l111_opy_ (u"࠭ࠧࣆ")
bstack1l111l1l_opy_ = False
bstack1111111l1_opy_ = False
bstack1llll1l111_opy_ = {}
bstack1lll1ll1_opy_ = None
bstack111l1ll1l_opy_ = None
bstack1l1l11lll1_opy_ = None
bstack1l1l1l1l11_opy_ = None
bstack11l11lll11_opy_ = None
bstack11ll1ll11_opy_ = None
bstack11l1ll111_opy_ = None
bstack1ll111111_opy_ = None
bstack1l1l11l1_opy_ = None
bstack1l1lll11ll_opy_ = None
bstack1l1llll1ll_opy_ = None
bstack1l1ll11l_opy_ = None
bstack1llll11l1l_opy_ = None
bstack1111ll1l1_opy_ = None
bstack1lll11l111_opy_ = None
bstack1l1lll11l_opy_ = None
bstack1ll11l1111_opy_ = None
bstack1l1ll1lll_opy_ = None
bstack11l1l1111l_opy_ = None
bstack1lll1l111_opy_ = None
bstack11ll1lll1l_opy_ = None
bstack1l11111l11_opy_ = None
bstack1l1llll11l_opy_ = None
thread_local = threading.local()
bstack11ll1l1l1l_opy_ = False
bstack1ll1ll1lll_opy_ = bstack111l111_opy_ (u"ࠢࠣࣇ")
logger = bstack1l1111ll_opy_.get_logger(__name__, bstack1ll1l111l_opy_)
bstack1ll1ll11_opy_ = Config.bstack1ll11ll1_opy_()
percy = bstack1111l11l1_opy_()
bstack1111l11l_opy_ = bstack1ll11l11l_opy_()
bstack11l1ll1l1l_opy_ = bstack11ll1l1lll_opy_()
def bstack1l1ll1ll1l_opy_():
  global CONFIG
  global bstack1l111l1l_opy_
  global bstack1ll1ll11_opy_
  testContextOptions = bstack11ll11lll1_opy_(CONFIG)
  if bstack1lllll1lll_opy_(CONFIG):
    if (bstack111l111_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪࣈ") in testContextOptions and str(testContextOptions[bstack111l111_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫࣉ")]).lower() == bstack111l111_opy_ (u"ࠪࡸࡷࡻࡥࠨ࣊")):
      bstack1l111l1l_opy_ = True
    bstack1ll1ll11_opy_.bstack111llll1l_opy_(testContextOptions.get(bstack111l111_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ࣋"), False))
  else:
    bstack1l111l1l_opy_ = True
    bstack1ll1ll11_opy_.bstack111llll1l_opy_(True)
def bstack1l11ll1111_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1llllll1l_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack11llll11ll_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack111l111_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡩ࡯࡯ࡨ࡬࡫࡫࡯࡬ࡦࠤ࣌") == args[i].lower() or bstack111l111_opy_ (u"ࠨ࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡪ࡮࡭ࠢ࣍") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1lll1l1ll1_opy_
      bstack1lll1l1ll1_opy_ += bstack111l111_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠤࠧ࠭࣎") + path + bstack111l111_opy_ (u"ࠨࠤ࣏ࠪ")
      return path
  return None
bstack1l1l11l1l_opy_ = re.compile(bstack111l111_opy_ (u"ࡴࠥ࠲࠯ࡅ࡜ࠥࡽࠫ࠲࠯ࡅࠩࡾ࠰࠭ࡃ࣐ࠧ"))
def bstack11llll1l_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1l1l11l1l_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack111l111_opy_ (u"ࠥࠨࢀࠨ࣑") + group + bstack111l111_opy_ (u"ࠦࢂࠨ࣒"), os.environ.get(group))
  return value
def bstack11l111llll_opy_():
  global bstack1l1llll11l_opy_
  if bstack1l1llll11l_opy_ is None:
        bstack1l1llll11l_opy_ = bstack11llll11ll_opy_()
  bstack1lll11l1ll_opy_ = bstack1l1llll11l_opy_
  if bstack1lll11l1ll_opy_ and os.path.exists(os.path.abspath(bstack1lll11l1ll_opy_)):
    fileName = bstack1lll11l1ll_opy_
  if bstack111l111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆ࣓ࠩ") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack111l111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࡤࡌࡉࡍࡇࠪࣔ")])) and not bstack111l111_opy_ (u"ࠧࡧ࡫࡯ࡩࡓࡧ࡭ࡦࠩࣕ") in locals():
    fileName = os.environ[bstack111l111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬࣖ")]
  if bstack111l111_opy_ (u"ࠩࡩ࡭ࡱ࡫ࡎࡢ࡯ࡨࠫࣗ") in locals():
    bstack11l111_opy_ = os.path.abspath(fileName)
  else:
    bstack11l111_opy_ = bstack111l111_opy_ (u"ࠪࠫࣘ")
  bstack1lll1l11l_opy_ = os.getcwd()
  bstack1l11111ll1_opy_ = bstack111l111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧࣙ")
  bstack11l111l111_opy_ = bstack111l111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡧ࡭࡭ࠩࣚ")
  while (not os.path.exists(bstack11l111_opy_)) and bstack1lll1l11l_opy_ != bstack111l111_opy_ (u"ࠨࠢࣛ"):
    bstack11l111_opy_ = os.path.join(bstack1lll1l11l_opy_, bstack1l11111ll1_opy_)
    if not os.path.exists(bstack11l111_opy_):
      bstack11l111_opy_ = os.path.join(bstack1lll1l11l_opy_, bstack11l111l111_opy_)
    if bstack1lll1l11l_opy_ != os.path.dirname(bstack1lll1l11l_opy_):
      bstack1lll1l11l_opy_ = os.path.dirname(bstack1lll1l11l_opy_)
    else:
      bstack1lll1l11l_opy_ = bstack111l111_opy_ (u"ࠢࠣࣜ")
  bstack1l1llll11l_opy_ = bstack11l111_opy_ if os.path.exists(bstack11l111_opy_) else None
  return bstack1l1llll11l_opy_
def bstack1l1111111_opy_():
  bstack11l111_opy_ = bstack11l111llll_opy_()
  if not os.path.exists(bstack11l111_opy_):
    bstack11l11ll1ll_opy_(
      bstack11lll11ll_opy_.format(os.getcwd()))
  try:
    with open(bstack11l111_opy_, bstack111l111_opy_ (u"ࠨࡴࠪࣝ")) as stream:
      yaml.add_implicit_resolver(bstack111l111_opy_ (u"ࠤࠤࡴࡦࡺࡨࡦࡺࠥࣞ"), bstack1l1l11l1l_opy_)
      yaml.add_constructor(bstack111l111_opy_ (u"ࠥࠥࡵࡧࡴࡩࡧࡻࠦࣟ"), bstack11llll1l_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack11l111_opy_, bstack111l111_opy_ (u"ࠫࡷ࠭࣠")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack11l11ll1ll_opy_(bstack1lll1l1111_opy_.format(str(exc)))
def bstack11111lll_opy_(config):
  bstack1l1l1l11l_opy_ = bstack11ll11l1ll_opy_(config)
  for option in list(bstack1l1l1l11l_opy_):
    if option.lower() in bstack11111ll11_opy_ and option != bstack11111ll11_opy_[option.lower()]:
      bstack1l1l1l11l_opy_[bstack11111ll11_opy_[option.lower()]] = bstack1l1l1l11l_opy_[option]
      del bstack1l1l1l11l_opy_[option]
  return config
def bstack1l1ll1l1_opy_():
  global bstack1l11l11l_opy_
  for key, bstack1l1l111ll1_opy_ in bstack11lllllll1_opy_.items():
    if isinstance(bstack1l1l111ll1_opy_, list):
      for var in bstack1l1l111ll1_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1l11l11l_opy_[key] = os.environ[var]
          break
    elif bstack1l1l111ll1_opy_ in os.environ and os.environ[bstack1l1l111ll1_opy_] and str(os.environ[bstack1l1l111ll1_opy_]).strip():
      bstack1l11l11l_opy_[key] = os.environ[bstack1l1l111ll1_opy_]
  if bstack111l111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ࣡") in os.environ:
    bstack1l11l11l_opy_[bstack111l111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ࣢")] = {}
    bstack1l11l11l_opy_[bstack111l111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࣣࠫ")][bstack111l111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣤ")] = os.environ[bstack111l111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫࣥ")]
def bstack1l1111ll11_opy_():
  global bstack11ll111111_opy_
  global bstack1lll1l1ll1_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack111l111_opy_ (u"ࠪ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࣦ࠭").lower() == val.lower():
      bstack11ll111111_opy_[bstack111l111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣧ")] = {}
      bstack11ll111111_opy_[bstack111l111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣨ")][bstack111l111_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣩ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack1l1l111l_opy_ in bstack1l1l1111ll_opy_.items():
    if isinstance(bstack1l1l111l_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1l1l111l_opy_:
          if idx < len(sys.argv) and bstack111l111_opy_ (u"ࠧ࠮࠯ࠪ࣪") + var.lower() == val.lower() and not key in bstack11ll111111_opy_:
            bstack11ll111111_opy_[key] = sys.argv[idx + 1]
            bstack1lll1l1ll1_opy_ += bstack111l111_opy_ (u"ࠨࠢ࠰࠱ࠬ࣫") + var + bstack111l111_opy_ (u"ࠩࠣࠫ࣬") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack111l111_opy_ (u"ࠪ࠱࠲࣭࠭") + bstack1l1l111l_opy_.lower() == val.lower() and not key in bstack11ll111111_opy_:
          bstack11ll111111_opy_[key] = sys.argv[idx + 1]
          bstack1lll1l1ll1_opy_ += bstack111l111_opy_ (u"ࠫࠥ࠳࠭ࠨ࣮") + bstack1l1l111l_opy_ + bstack111l111_opy_ (u"࣯ࠬࠦࠧ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1llll1lll1_opy_(config):
  bstack1lll1llll1_opy_ = config.keys()
  for bstack1l1ll1111l_opy_, bstack11l1lll1ll_opy_ in bstack11lllll111_opy_.items():
    if bstack11l1lll1ll_opy_ in bstack1lll1llll1_opy_:
      config[bstack1l1ll1111l_opy_] = config[bstack11l1lll1ll_opy_]
      del config[bstack11l1lll1ll_opy_]
  for bstack1l1ll1111l_opy_, bstack11l1lll1ll_opy_ in bstack1ll111l1l1_opy_.items():
    if isinstance(bstack11l1lll1ll_opy_, list):
      for bstack1l11l111l1_opy_ in bstack11l1lll1ll_opy_:
        if bstack1l11l111l1_opy_ in bstack1lll1llll1_opy_:
          config[bstack1l1ll1111l_opy_] = config[bstack1l11l111l1_opy_]
          del config[bstack1l11l111l1_opy_]
          break
    elif bstack11l1lll1ll_opy_ in bstack1lll1llll1_opy_:
      config[bstack1l1ll1111l_opy_] = config[bstack11l1lll1ll_opy_]
      del config[bstack11l1lll1ll_opy_]
  for bstack1l11l111l1_opy_ in list(config):
    for bstack11l1ll1l_opy_ in bstack111ll1l1_opy_:
      if bstack1l11l111l1_opy_.lower() == bstack11l1ll1l_opy_.lower() and bstack1l11l111l1_opy_ != bstack11l1ll1l_opy_:
        config[bstack11l1ll1l_opy_] = config[bstack1l11l111l1_opy_]
        del config[bstack1l11l111l1_opy_]
  bstack1ll11lll1l_opy_ = [{}]
  if not config.get(bstack111l111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࣰࠩ")):
    config[bstack111l111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࣱࠪ")] = [{}]
  bstack1ll11lll1l_opy_ = config[bstack111l111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࣲࠫ")]
  for platform in bstack1ll11lll1l_opy_:
    for bstack1l11l111l1_opy_ in list(platform):
      for bstack11l1ll1l_opy_ in bstack111ll1l1_opy_:
        if bstack1l11l111l1_opy_.lower() == bstack11l1ll1l_opy_.lower() and bstack1l11l111l1_opy_ != bstack11l1ll1l_opy_:
          platform[bstack11l1ll1l_opy_] = platform[bstack1l11l111l1_opy_]
          del platform[bstack1l11l111l1_opy_]
  for bstack1l1ll1111l_opy_, bstack11l1lll1ll_opy_ in bstack1ll111l1l1_opy_.items():
    for platform in bstack1ll11lll1l_opy_:
      if isinstance(bstack11l1lll1ll_opy_, list):
        for bstack1l11l111l1_opy_ in bstack11l1lll1ll_opy_:
          if bstack1l11l111l1_opy_ in platform:
            platform[bstack1l1ll1111l_opy_] = platform[bstack1l11l111l1_opy_]
            del platform[bstack1l11l111l1_opy_]
            break
      elif bstack11l1lll1ll_opy_ in platform:
        platform[bstack1l1ll1111l_opy_] = platform[bstack11l1lll1ll_opy_]
        del platform[bstack11l1lll1ll_opy_]
  for bstack11l11l1lll_opy_ in bstack1lll11111l_opy_:
    if bstack11l11l1lll_opy_ in config:
      if not bstack1lll11111l_opy_[bstack11l11l1lll_opy_] in config:
        config[bstack1lll11111l_opy_[bstack11l11l1lll_opy_]] = {}
      config[bstack1lll11111l_opy_[bstack11l11l1lll_opy_]].update(config[bstack11l11l1lll_opy_])
      del config[bstack11l11l1lll_opy_]
  for platform in bstack1ll11lll1l_opy_:
    for bstack11l11l1lll_opy_ in bstack1lll11111l_opy_:
      if bstack11l11l1lll_opy_ in list(platform):
        if not bstack1lll11111l_opy_[bstack11l11l1lll_opy_] in platform:
          platform[bstack1lll11111l_opy_[bstack11l11l1lll_opy_]] = {}
        platform[bstack1lll11111l_opy_[bstack11l11l1lll_opy_]].update(platform[bstack11l11l1lll_opy_])
        del platform[bstack11l11l1lll_opy_]
  config = bstack11111lll_opy_(config)
  return config
def bstack11l11ll1l_opy_(config):
  global bstack1l11ll1ll1_opy_
  bstack11lll111l1_opy_ = False
  if bstack111l111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ࣳ") in config and str(config[bstack111l111_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧࣴ")]).lower() != bstack111l111_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪࣵ"):
    if bstack111l111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࣶࠩ") not in config or str(config[bstack111l111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪࣷ")]).lower() == bstack111l111_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ࣸ"):
      config[bstack111l111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࣹࠧ")] = False
    else:
      bstack1l111ll1l1_opy_ = bstack1lll11lll_opy_()
      if bstack111l111_opy_ (u"ࠩ࡬ࡷ࡙ࡸࡩࡢ࡮ࡊࡶ࡮ࡪࣺࠧ") in bstack1l111ll1l1_opy_:
        if not bstack111l111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࣻ") in config:
          config[bstack111l111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣼ")] = {}
        config[bstack111l111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣽ")][bstack111l111_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣾ")] = bstack111l111_opy_ (u"ࠧࡢࡶࡶ࠱ࡷ࡫ࡰࡦࡣࡷࡩࡷ࠭ࣿ")
        bstack11lll111l1_opy_ = True
        bstack1l11ll1ll1_opy_ = config[bstack111l111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬऀ")].get(bstack111l111_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫँ"))
  if bstack1lllll1lll_opy_(config) and bstack111l111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧं") in config and str(config[bstack111l111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨः")]).lower() != bstack111l111_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫऄ") and not bstack11lll111l1_opy_:
    if not bstack111l111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪअ") in config:
      config[bstack111l111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫआ")] = {}
    if not config[bstack111l111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬइ")].get(bstack111l111_opy_ (u"ࠩࡶ࡯࡮ࡶࡂࡪࡰࡤࡶࡾࡏ࡮ࡪࡶ࡬ࡥࡱ࡯ࡳࡢࡶ࡬ࡳࡳ࠭ई")) and not bstack111l111_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬउ") in config[bstack111l111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऊ")]:
      bstack1ll1ll1l1_opy_ = datetime.datetime.now()
      bstack11ll11l11l_opy_ = bstack1ll1ll1l1_opy_.strftime(bstack111l111_opy_ (u"ࠬࠫࡤࡠࠧࡥࡣࠪࡎࠥࡎࠩऋ"))
      hostname = socket.gethostname()
      bstack1ll11l111l_opy_ = bstack111l111_opy_ (u"࠭ࠧऌ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack111l111_opy_ (u"ࠧࡼࡿࡢࡿࢂࡥࡻࡾࠩऍ").format(bstack11ll11l11l_opy_, hostname, bstack1ll11l111l_opy_)
      config[bstack111l111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬऎ")][bstack111l111_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫए")] = identifier
    bstack1l11ll1ll1_opy_ = config[bstack111l111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧऐ")].get(bstack111l111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ऑ"))
  return config
def bstack1l11l1l1ll_opy_():
  bstack1l1l11111l_opy_ =  bstack1ll1l11111_opy_()[bstack111l111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠫऒ")]
  return bstack1l1l11111l_opy_ if bstack1l1l11111l_opy_ else -1
def bstack1ll1l1ll11_opy_(bstack1l1l11111l_opy_):
  global CONFIG
  if not bstack111l111_opy_ (u"࠭ࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨओ") in CONFIG[bstack111l111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऔ")]:
    return
  CONFIG[bstack111l111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪक")] = CONFIG[bstack111l111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫख")].replace(
    bstack111l111_opy_ (u"ࠪࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬग"),
    str(bstack1l1l11111l_opy_)
  )
def bstack1l111l111l_opy_():
  global CONFIG
  if not bstack111l111_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪघ") in CONFIG[bstack111l111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧङ")]:
    return
  bstack1ll1ll1l1_opy_ = datetime.datetime.now()
  bstack11ll11l11l_opy_ = bstack1ll1ll1l1_opy_.strftime(bstack111l111_opy_ (u"࠭ࠥࡥ࠯ࠨࡦ࠲ࠫࡈ࠻ࠧࡐࠫच"))
  CONFIG[bstack111l111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩछ")] = CONFIG[bstack111l111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪज")].replace(
    bstack111l111_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨझ"),
    bstack11ll11l11l_opy_
  )
def bstack1l1ll111l1_opy_():
  global CONFIG
  if bstack111l111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬञ") in CONFIG and not bool(CONFIG[bstack111l111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ट")]):
    del CONFIG[bstack111l111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧठ")]
    return
  if not bstack111l111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨड") in CONFIG:
    CONFIG[bstack111l111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩढ")] = bstack111l111_opy_ (u"ࠨࠥࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫण")
  if bstack111l111_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨत") in CONFIG[bstack111l111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬथ")]:
    bstack1l111l111l_opy_()
    os.environ[bstack111l111_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨद")] = CONFIG[bstack111l111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧध")]
  if not bstack111l111_opy_ (u"࠭ࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨन") in CONFIG[bstack111l111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऩ")]:
    return
  bstack1l1l11111l_opy_ = bstack111l111_opy_ (u"ࠨࠩप")
  bstack11ll11ll_opy_ = bstack1l11l1l1ll_opy_()
  if bstack11ll11ll_opy_ != -1:
    bstack1l1l11111l_opy_ = bstack111l111_opy_ (u"ࠩࡆࡍࠥ࠭फ") + str(bstack11ll11ll_opy_)
  if bstack1l1l11111l_opy_ == bstack111l111_opy_ (u"ࠪࠫब"):
    bstack111l111ll_opy_ = bstack1l11111111_opy_(CONFIG[bstack111l111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧभ")])
    if bstack111l111ll_opy_ != -1:
      bstack1l1l11111l_opy_ = str(bstack111l111ll_opy_)
  if bstack1l1l11111l_opy_:
    bstack1ll1l1ll11_opy_(bstack1l1l11111l_opy_)
    os.environ[bstack111l111_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩम")] = CONFIG[bstack111l111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨय")]
def bstack1l1l1l1ll_opy_(bstack1l111l1111_opy_, bstack111l1ll1_opy_, path):
  bstack11lll111_opy_ = {
    bstack111l111_opy_ (u"ࠧࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫर"): bstack111l1ll1_opy_
  }
  if os.path.exists(path):
    bstack1lllll1ll1_opy_ = json.load(open(path, bstack111l111_opy_ (u"ࠨࡴࡥࠫऱ")))
  else:
    bstack1lllll1ll1_opy_ = {}
  bstack1lllll1ll1_opy_[bstack1l111l1111_opy_] = bstack11lll111_opy_
  with open(path, bstack111l111_opy_ (u"ࠤࡺ࠯ࠧल")) as outfile:
    json.dump(bstack1lllll1ll1_opy_, outfile)
def bstack1l11111111_opy_(bstack1l111l1111_opy_):
  bstack1l111l1111_opy_ = str(bstack1l111l1111_opy_)
  bstack11l1l1l1l1_opy_ = os.path.join(os.path.expanduser(bstack111l111_opy_ (u"ࠪࢂࠬळ")), bstack111l111_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫऴ"))
  try:
    if not os.path.exists(bstack11l1l1l1l1_opy_):
      os.makedirs(bstack11l1l1l1l1_opy_)
    file_path = os.path.join(os.path.expanduser(bstack111l111_opy_ (u"ࠬࢄࠧव")), bstack111l111_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭श"), bstack111l111_opy_ (u"ࠧ࠯ࡤࡸ࡭ࡱࡪ࠭࡯ࡣࡰࡩ࠲ࡩࡡࡤࡪࡨ࠲࡯ࡹ࡯࡯ࠩष"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack111l111_opy_ (u"ࠨࡹࠪस")):
        pass
      with open(file_path, bstack111l111_opy_ (u"ࠤࡺ࠯ࠧह")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack111l111_opy_ (u"ࠪࡶࠬऺ")) as bstack111llll11_opy_:
      bstack11l11l111l_opy_ = json.load(bstack111llll11_opy_)
    if bstack1l111l1111_opy_ in bstack11l11l111l_opy_:
      bstack1l1llllll1_opy_ = bstack11l11l111l_opy_[bstack1l111l1111_opy_][bstack111l111_opy_ (u"ࠫ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨऻ")]
      bstack11l1lll1_opy_ = int(bstack1l1llllll1_opy_) + 1
      bstack1l1l1l1ll_opy_(bstack1l111l1111_opy_, bstack11l1lll1_opy_, file_path)
      return bstack11l1lll1_opy_
    else:
      bstack1l1l1l1ll_opy_(bstack1l111l1111_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack11l1l1lll1_opy_.format(str(e)))
    return -1
def bstack1lll111111_opy_(config):
  if not config[bstack111l111_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫़ࠧ")] or not config[bstack111l111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩऽ")]:
    return True
  else:
    return False
def bstack11ll11111_opy_(config, index=0):
  global bstack1l11111lll_opy_
  bstack1l11lllll1_opy_ = {}
  caps = bstack111111l1l_opy_ + bstack1l11l1l1l1_opy_
  if config.get(bstack111l111_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫा"), False):
    bstack1l11lllll1_opy_[bstack111l111_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬि")] = True
    bstack1l11lllll1_opy_[bstack111l111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ी")] = config.get(bstack111l111_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧु"), {})
  if bstack1l11111lll_opy_:
    caps += bstack1ll1111l1l_opy_
  for key in config:
    if key in caps + [bstack111l111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧू")]:
      continue
    bstack1l11lllll1_opy_[key] = config[key]
  if bstack111l111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨृ") in config:
    for bstack11llll11l_opy_ in config[bstack111l111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩॄ")][index]:
      if bstack11llll11l_opy_ in caps:
        continue
      bstack1l11lllll1_opy_[bstack11llll11l_opy_] = config[bstack111l111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪॅ")][index][bstack11llll11l_opy_]
  bstack1l11lllll1_opy_[bstack111l111_opy_ (u"ࠨࡪࡲࡷࡹࡔࡡ࡮ࡧࠪॆ")] = socket.gethostname()
  if bstack111l111_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪे") in bstack1l11lllll1_opy_:
    del (bstack1l11lllll1_opy_[bstack111l111_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫै")])
  return bstack1l11lllll1_opy_
def bstack111l1lll1_opy_(config):
  global bstack1l11111lll_opy_
  bstack11lll1lll_opy_ = {}
  caps = bstack1l11l1l1l1_opy_
  if bstack1l11111lll_opy_:
    caps += bstack1ll1111l1l_opy_
  for key in caps:
    if key in config:
      bstack11lll1lll_opy_[key] = config[key]
  return bstack11lll1lll_opy_
def bstack1ll1l1ll1_opy_(bstack1l11lllll1_opy_, bstack11lll1lll_opy_):
  bstack1lll1lll_opy_ = {}
  for key in bstack1l11lllll1_opy_.keys():
    if key in bstack11lllll111_opy_:
      bstack1lll1lll_opy_[bstack11lllll111_opy_[key]] = bstack1l11lllll1_opy_[key]
    else:
      bstack1lll1lll_opy_[key] = bstack1l11lllll1_opy_[key]
  for key in bstack11lll1lll_opy_:
    if key in bstack11lllll111_opy_:
      bstack1lll1lll_opy_[bstack11lllll111_opy_[key]] = bstack11lll1lll_opy_[key]
    else:
      bstack1lll1lll_opy_[key] = bstack11lll1lll_opy_[key]
  return bstack1lll1lll_opy_
def bstack1l1l1ll1l_opy_(config, index=0):
  global bstack1l11111lll_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack1111lll1_opy_ = bstack1l1111l1ll_opy_(bstack1l11lll1ll_opy_, config, logger)
  bstack11lll1lll_opy_ = bstack111l1lll1_opy_(config)
  bstack11l1lll111_opy_ = bstack1l11l1l1l1_opy_
  bstack11l1lll111_opy_ += bstack11ll111l1_opy_
  bstack11lll1lll_opy_ = update(bstack11lll1lll_opy_, bstack1111lll1_opy_)
  if bstack1l11111lll_opy_:
    bstack11l1lll111_opy_ += bstack1ll1111l1l_opy_
  if bstack111l111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॉ") in config:
    if bstack111l111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪॊ") in config[bstack111l111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩो")][index]:
      caps[bstack111l111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬौ")] = config[bstack111l111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶ्ࠫ")][index][bstack111l111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧॎ")]
    if bstack111l111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫॏ") in config[bstack111l111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॐ")][index]:
      caps[bstack111l111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭॑")] = str(config[bstack111l111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴ॒ࠩ")][index][bstack111l111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ॓")])
    bstack1ll1111l1_opy_ = bstack1l1111l1ll_opy_(bstack1l11lll1ll_opy_, config[bstack111l111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ॔")][index], logger)
    bstack11l1lll111_opy_ += list(bstack1ll1111l1_opy_.keys())
    for bstack11111l111_opy_ in bstack11l1lll111_opy_:
      if bstack11111l111_opy_ in config[bstack111l111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॕ")][index]:
        if bstack11111l111_opy_ == bstack111l111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬॖ"):
          try:
            bstack1ll1111l1_opy_[bstack11111l111_opy_] = str(config[bstack111l111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॗ")][index][bstack11111l111_opy_] * 1.0)
          except:
            bstack1ll1111l1_opy_[bstack11111l111_opy_] = str(config[bstack111l111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨक़")][index][bstack11111l111_opy_])
        else:
          bstack1ll1111l1_opy_[bstack11111l111_opy_] = config[bstack111l111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩख़")][index][bstack11111l111_opy_]
        del (config[bstack111l111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪग़")][index][bstack11111l111_opy_])
    bstack11lll1lll_opy_ = update(bstack11lll1lll_opy_, bstack1ll1111l1_opy_)
  bstack1l11lllll1_opy_ = bstack11ll11111_opy_(config, index)
  for bstack1l11l111l1_opy_ in bstack1l11l1l1l1_opy_ + list(bstack1111lll1_opy_.keys()):
    if bstack1l11l111l1_opy_ in bstack1l11lllll1_opy_:
      bstack11lll1lll_opy_[bstack1l11l111l1_opy_] = bstack1l11lllll1_opy_[bstack1l11l111l1_opy_]
      del (bstack1l11lllll1_opy_[bstack1l11l111l1_opy_])
  if bstack1l11ll11l_opy_(config):
    bstack1l11lllll1_opy_[bstack111l111_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨज़")] = True
    caps.update(bstack11lll1lll_opy_)
    caps[bstack111l111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪड़")] = bstack1l11lllll1_opy_
  else:
    bstack1l11lllll1_opy_[bstack111l111_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪढ़")] = False
    caps.update(bstack1ll1l1ll1_opy_(bstack1l11lllll1_opy_, bstack11lll1lll_opy_))
    if bstack111l111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩफ़") in caps:
      caps[bstack111l111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭य़")] = caps[bstack111l111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫॠ")]
      del (caps[bstack111l111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬॡ")])
    if bstack111l111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩॢ") in caps:
      caps[bstack111l111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫॣ")] = caps[bstack111l111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ।")]
      del (caps[bstack111l111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ॥")])
  return caps
def bstack1l11l11ll1_opy_():
  global bstack1l11111l1l_opy_
  global CONFIG
  if bstack1llllll1l_opy_() <= version.parse(bstack111l111_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬ०")):
    if bstack1l11111l1l_opy_ != bstack111l111_opy_ (u"࠭ࠧ१"):
      return bstack111l111_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ२") + bstack1l11111l1l_opy_ + bstack111l111_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧ३")
    return bstack11l1ll11l1_opy_
  if bstack1l11111l1l_opy_ != bstack111l111_opy_ (u"ࠩࠪ४"):
    return bstack111l111_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ५") + bstack1l11111l1l_opy_ + bstack111l111_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧ६")
  return bstack11l1l11l1l_opy_
def bstack11l1l1l1l_opy_(options):
  return hasattr(options, bstack111l111_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭७"))
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
def bstack1ll1lll1ll_opy_(options, bstack1lll111l_opy_):
  for bstack1l11l11l11_opy_ in bstack1lll111l_opy_:
    if bstack1l11l11l11_opy_ in [bstack111l111_opy_ (u"࠭ࡡࡳࡩࡶࠫ८"), bstack111l111_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫ९")]:
      continue
    if bstack1l11l11l11_opy_ in options._experimental_options:
      options._experimental_options[bstack1l11l11l11_opy_] = update(options._experimental_options[bstack1l11l11l11_opy_],
                                                         bstack1lll111l_opy_[bstack1l11l11l11_opy_])
    else:
      options.add_experimental_option(bstack1l11l11l11_opy_, bstack1lll111l_opy_[bstack1l11l11l11_opy_])
  if bstack111l111_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭॰") in bstack1lll111l_opy_:
    for arg in bstack1lll111l_opy_[bstack111l111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॱ")]:
      options.add_argument(arg)
    del (bstack1lll111l_opy_[bstack111l111_opy_ (u"ࠪࡥࡷ࡭ࡳࠨॲ")])
  if bstack111l111_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨॳ") in bstack1lll111l_opy_:
    for ext in bstack1lll111l_opy_[bstack111l111_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩॴ")]:
      try:
        options.add_extension(ext)
      except OSError:
        options.add_encoded_extension(ext)
    del (bstack1lll111l_opy_[bstack111l111_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪॵ")])
def bstack1llll1l1l1_opy_(options, bstack1l1111l11l_opy_):
  if bstack111l111_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ॶ") in bstack1l1111l11l_opy_:
    for bstack11ll1ll1l_opy_ in bstack1l1111l11l_opy_[bstack111l111_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧॷ")]:
      if bstack11ll1ll1l_opy_ in options._preferences:
        options._preferences[bstack11ll1ll1l_opy_] = update(options._preferences[bstack11ll1ll1l_opy_], bstack1l1111l11l_opy_[bstack111l111_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨॸ")][bstack11ll1ll1l_opy_])
      else:
        options.set_preference(bstack11ll1ll1l_opy_, bstack1l1111l11l_opy_[bstack111l111_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩॹ")][bstack11ll1ll1l_opy_])
  if bstack111l111_opy_ (u"ࠫࡦࡸࡧࡴࠩॺ") in bstack1l1111l11l_opy_:
    for arg in bstack1l1111l11l_opy_[bstack111l111_opy_ (u"ࠬࡧࡲࡨࡵࠪॻ")]:
      options.add_argument(arg)
def bstack1ll1l111_opy_(options, bstack1lll1l1l11_opy_):
  if bstack111l111_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࠧॼ") in bstack1lll1l1l11_opy_:
    options.use_webview(bool(bstack1lll1l1l11_opy_[bstack111l111_opy_ (u"ࠧࡸࡧࡥࡺ࡮࡫ࡷࠨॽ")]))
  bstack1ll1lll1ll_opy_(options, bstack1lll1l1l11_opy_)
def bstack111l11ll_opy_(options, bstack11l1llll1l_opy_):
  for bstack1l11111l_opy_ in bstack11l1llll1l_opy_:
    if bstack1l11111l_opy_ in [bstack111l111_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬॾ"), bstack111l111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॿ")]:
      continue
    options.set_capability(bstack1l11111l_opy_, bstack11l1llll1l_opy_[bstack1l11111l_opy_])
  if bstack111l111_opy_ (u"ࠪࡥࡷ࡭ࡳࠨঀ") in bstack11l1llll1l_opy_:
    for arg in bstack11l1llll1l_opy_[bstack111l111_opy_ (u"ࠫࡦࡸࡧࡴࠩঁ")]:
      options.add_argument(arg)
  if bstack111l111_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩং") in bstack11l1llll1l_opy_:
    options.bstack1ll111ll_opy_(bool(bstack11l1llll1l_opy_[bstack111l111_opy_ (u"࠭ࡴࡦࡥ࡫ࡲࡴࡲ࡯ࡨࡻࡓࡶࡪࡼࡩࡦࡹࠪঃ")]))
def bstack111l111l1_opy_(options, bstack11ll1l11_opy_):
  for bstack11l11ll111_opy_ in bstack11ll1l11_opy_:
    if bstack11l11ll111_opy_ in [bstack111l111_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ঄"), bstack111l111_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭অ")]:
      continue
    options._options[bstack11l11ll111_opy_] = bstack11ll1l11_opy_[bstack11l11ll111_opy_]
  if bstack111l111_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭আ") in bstack11ll1l11_opy_:
    for bstack1l1l111111_opy_ in bstack11ll1l11_opy_[bstack111l111_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧই")]:
      options.bstack111l1111_opy_(
        bstack1l1l111111_opy_, bstack11ll1l11_opy_[bstack111l111_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨঈ")][bstack1l1l111111_opy_])
  if bstack111l111_opy_ (u"ࠬࡧࡲࡨࡵࠪউ") in bstack11ll1l11_opy_:
    for arg in bstack11ll1l11_opy_[bstack111l111_opy_ (u"࠭ࡡࡳࡩࡶࠫঊ")]:
      options.add_argument(arg)
def bstack1l1ll1111_opy_(options, caps):
  if not hasattr(options, bstack111l111_opy_ (u"ࠧࡌࡇ࡜ࠫঋ")):
    return
  if options.KEY == bstack111l111_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ঌ"):
    options = bstack1l1ll11l1l_opy_.bstack11l1ll1lll_opy_(bstack1l1lll1l11_opy_=options, config=CONFIG)
  if options.KEY == bstack111l111_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ঍") and options.KEY in caps:
    bstack1ll1lll1ll_opy_(options, caps[bstack111l111_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ঎")])
  elif options.KEY == bstack111l111_opy_ (u"ࠫࡲࡵࡺ࠻ࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩএ") and options.KEY in caps:
    bstack1llll1l1l1_opy_(options, caps[bstack111l111_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪঐ")])
  elif options.KEY == bstack111l111_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧ঑") and options.KEY in caps:
    bstack111l11ll_opy_(options, caps[bstack111l111_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨ঒")])
  elif options.KEY == bstack111l111_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩও") and options.KEY in caps:
    bstack1ll1l111_opy_(options, caps[bstack111l111_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪঔ")])
  elif options.KEY == bstack111l111_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩক") and options.KEY in caps:
    bstack111l111l1_opy_(options, caps[bstack111l111_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪখ")])
def bstack1l11l1ll1l_opy_(caps):
  global bstack1l11111lll_opy_
  if isinstance(os.environ.get(bstack111l111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭গ")), str):
    bstack1l11111lll_opy_ = eval(os.getenv(bstack111l111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧঘ")))
  if bstack1l11111lll_opy_:
    if bstack1l11ll1111_opy_() < version.parse(bstack111l111_opy_ (u"ࠧ࠳࠰࠶࠲࠵࠭ঙ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack111l111_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨচ")
    if bstack111l111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧছ") in caps:
      browser = caps[bstack111l111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨজ")]
    elif bstack111l111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬঝ") in caps:
      browser = caps[bstack111l111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ঞ")]
    browser = str(browser).lower()
    if browser == bstack111l111_opy_ (u"࠭ࡩࡱࡪࡲࡲࡪ࠭ট") or browser == bstack111l111_opy_ (u"ࠧࡪࡲࡤࡨࠬঠ"):
      browser = bstack111l111_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨড")
    if browser == bstack111l111_opy_ (u"ࠩࡶࡥࡲࡹࡵ࡯ࡩࠪঢ"):
      browser = bstack111l111_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪণ")
    if browser not in [bstack111l111_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫত"), bstack111l111_opy_ (u"ࠬ࡫ࡤࡨࡧࠪথ"), bstack111l111_opy_ (u"࠭ࡩࡦࠩদ"), bstack111l111_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧধ"), bstack111l111_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩন")]:
      return None
    try:
      package = bstack111l111_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࠮ࡼࡿ࠱ࡳࡵࡺࡩࡰࡰࡶࠫ঩").format(browser)
      name = bstack111l111_opy_ (u"ࠪࡓࡵࡺࡩࡰࡰࡶࠫপ")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack11l1l1l1l_opy_(options):
        return None
      for bstack1l11l111l1_opy_ in caps.keys():
        options.set_capability(bstack1l11l111l1_opy_, caps[bstack1l11l111l1_opy_])
      bstack1l1ll1111_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack11lllll1l_opy_(options, bstack1l1l1llll1_opy_):
  if not bstack11l1l1l1l_opy_(options):
    return
  for bstack1l11l111l1_opy_ in bstack1l1l1llll1_opy_.keys():
    if bstack1l11l111l1_opy_ in bstack11ll111l1_opy_:
      continue
    if bstack1l11l111l1_opy_ in options._caps and type(options._caps[bstack1l11l111l1_opy_]) in [dict, list]:
      options._caps[bstack1l11l111l1_opy_] = update(options._caps[bstack1l11l111l1_opy_], bstack1l1l1llll1_opy_[bstack1l11l111l1_opy_])
    else:
      options.set_capability(bstack1l11l111l1_opy_, bstack1l1l1llll1_opy_[bstack1l11l111l1_opy_])
  bstack1l1ll1111_opy_(options, bstack1l1l1llll1_opy_)
  if bstack111l111_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪফ") in options._caps:
    if options._caps[bstack111l111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪব")] and options._caps[bstack111l111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫভ")].lower() != bstack111l111_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨম"):
      del options._caps[bstack111l111_opy_ (u"ࠨ࡯ࡲࡾ࠿ࡪࡥࡣࡷࡪ࡫ࡪࡸࡁࡥࡦࡵࡩࡸࡹࠧয")]
def bstack1l1lll111l_opy_(proxy_config):
  if bstack111l111_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭র") in proxy_config:
    proxy_config[bstack111l111_opy_ (u"ࠪࡷࡸࡲࡐࡳࡱࡻࡽࠬ঱")] = proxy_config[bstack111l111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨল")]
    del (proxy_config[bstack111l111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ঳")])
  if bstack111l111_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩ঴") in proxy_config and proxy_config[bstack111l111_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪ঵")].lower() != bstack111l111_opy_ (u"ࠨࡦ࡬ࡶࡪࡩࡴࠨশ"):
    proxy_config[bstack111l111_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬষ")] = bstack111l111_opy_ (u"ࠪࡱࡦࡴࡵࡢ࡮ࠪস")
  if bstack111l111_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡄࡹࡹࡵࡣࡰࡰࡩ࡭࡬࡛ࡲ࡭ࠩহ") in proxy_config:
    proxy_config[bstack111l111_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ঺")] = bstack111l111_opy_ (u"࠭ࡰࡢࡥࠪ঻")
  return proxy_config
def bstack1l1l1l1lll_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack111l111_opy_ (u"ࠧࡱࡴࡲࡼࡾ়࠭") in config:
    return proxy
  config[bstack111l111_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧঽ")] = bstack1l1lll111l_opy_(config[bstack111l111_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨা")])
  if proxy == None:
    proxy = Proxy(config[bstack111l111_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩি")])
  return proxy
def bstack111ll1lll_opy_(self):
  global CONFIG
  global bstack1l1ll11l_opy_
  try:
    proxy = bstack1l111ll111_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack111l111_opy_ (u"ࠫ࠳ࡶࡡࡤࠩী")):
        proxies = bstack1111ll11_opy_(proxy, bstack1l11l11ll1_opy_())
        if len(proxies) > 0:
          protocol, bstack11lll1lll1_opy_ = proxies.popitem()
          if bstack111l111_opy_ (u"ࠧࡀ࠯࠰ࠤু") in bstack11lll1lll1_opy_:
            return bstack11lll1lll1_opy_
          else:
            return bstack111l111_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢূ") + bstack11lll1lll1_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack111l111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡴࡷࡵࡸࡺࠢࡸࡶࡱࠦ࠺ࠡࡽࢀࠦৃ").format(str(e)))
  return bstack1l1ll11l_opy_(self)
def bstack1l1111111l_opy_():
  global CONFIG
  return bstack11ll11l1_opy_(CONFIG) and bstack1l1llll1l1_opy_() and bstack1llllll1l_opy_() >= version.parse(bstack1ll1l11l11_opy_)
def bstack1ll1l11lll_opy_():
  global CONFIG
  return (bstack111l111_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫৄ") in CONFIG or bstack111l111_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭৅") in CONFIG) and bstack1ll1l1l11_opy_()
def bstack11ll11l1ll_opy_(config):
  bstack1l1l1l11l_opy_ = {}
  if bstack111l111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ৆") in config:
    bstack1l1l1l11l_opy_ = config[bstack111l111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨে")]
  if bstack111l111_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫৈ") in config:
    bstack1l1l1l11l_opy_ = config[bstack111l111_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ৉")]
  proxy = bstack1l111ll111_opy_(config)
  if proxy:
    if proxy.endswith(bstack111l111_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ৊")) and os.path.isfile(proxy):
      bstack1l1l1l11l_opy_[bstack111l111_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫো")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack111l111_opy_ (u"ࠩ࠱ࡴࡦࡩࠧৌ")):
        proxies = bstack1lllll11l1_opy_(config, bstack1l11l11ll1_opy_())
        if len(proxies) > 0:
          protocol, bstack11lll1lll1_opy_ = proxies.popitem()
          if bstack111l111_opy_ (u"ࠥ࠾࠴࠵্ࠢ") in bstack11lll1lll1_opy_:
            parsed_url = urlparse(bstack11lll1lll1_opy_)
          else:
            parsed_url = urlparse(protocol + bstack111l111_opy_ (u"ࠦ࠿࠵࠯ࠣৎ") + bstack11lll1lll1_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1l1l1l11l_opy_[bstack111l111_opy_ (u"ࠬࡶࡲࡰࡺࡼࡌࡴࡹࡴࠨ৏")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1l1l1l11l_opy_[bstack111l111_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵࠩ৐")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1l1l1l11l_opy_[bstack111l111_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪ৑")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1l1l1l11l_opy_[bstack111l111_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫ৒")] = str(parsed_url.password)
  return bstack1l1l1l11l_opy_
def bstack11ll11lll1_opy_(config):
  if bstack111l111_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧ৓") in config:
    return config[bstack111l111_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨ৔")]
  return {}
def bstack1l111l1l11_opy_(caps):
  global bstack1l11ll1ll1_opy_
  if bstack111l111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ৕") in caps:
    caps[bstack111l111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭৖")][bstack111l111_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬৗ")] = True
    if bstack1l11ll1ll1_opy_:
      caps[bstack111l111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ৘")][bstack111l111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ৙")] = bstack1l11ll1ll1_opy_
  else:
    caps[bstack111l111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࠧ৚")] = True
    if bstack1l11ll1ll1_opy_:
      caps[bstack111l111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ৛")] = bstack1l11ll1ll1_opy_
@measure(event_name=EVENTS.bstack1lll1l11l1_opy_, stage=STAGE.bstack11l1llll1_opy_, bstack11llll1lll_opy_=bstack1ll1l11l1l_opy_)
def bstack1lll11l1l_opy_():
  global CONFIG
  if not bstack1lllll1lll_opy_(CONFIG) or cli.is_enabled(CONFIG):
    return
  if bstack111l111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨড়") in CONFIG and bstack1ll111l11l_opy_(CONFIG[bstack111l111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩঢ়")]):
    if (
      bstack111l111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ৞") in CONFIG
      and bstack1ll111l11l_opy_(CONFIG[bstack111l111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫয়")].get(bstack111l111_opy_ (u"ࠨࡵ࡮࡭ࡵࡈࡩ࡯ࡣࡵࡽࡎࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡡࡵ࡫ࡲࡲࠬৠ")))
    ):
      logger.debug(bstack111l111_opy_ (u"ࠤࡏࡳࡨࡧ࡬ࠡࡤ࡬ࡲࡦࡸࡹࠡࡰࡲࡸࠥࡹࡴࡢࡴࡷࡩࡩࠦࡡࡴࠢࡶ࡯࡮ࡶࡂࡪࡰࡤࡶࡾࡏ࡮ࡪࡶ࡬ࡥࡱ࡯ࡳࡢࡶ࡬ࡳࡳࠦࡩࡴࠢࡨࡲࡦࡨ࡬ࡦࡦࠥৡ"))
      return
    bstack1l1l1l11l_opy_ = bstack11ll11l1ll_opy_(CONFIG)
    bstack11l1l1l111_opy_(CONFIG[bstack111l111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ৢ")], bstack1l1l1l11l_opy_)
def bstack11l1l1l111_opy_(key, bstack1l1l1l11l_opy_):
  global bstack111111111_opy_
  logger.info(bstack11ll1ll1_opy_)
  try:
    bstack111111111_opy_ = Local()
    bstack11ll1111_opy_ = {bstack111l111_opy_ (u"ࠫࡰ࡫ࡹࠨৣ"): key}
    bstack11ll1111_opy_.update(bstack1l1l1l11l_opy_)
    logger.debug(bstack11l11lll1l_opy_.format(str(bstack11ll1111_opy_)).replace(key, bstack111l111_opy_ (u"ࠬࡡࡒࡆࡆࡄࡇ࡙ࡋࡄ࡞ࠩ৤")))
    bstack111111111_opy_.start(**bstack11ll1111_opy_)
    if bstack111111111_opy_.isRunning():
      logger.info(bstack11l1lllll_opy_)
  except Exception as e:
    bstack11l11ll1ll_opy_(bstack1l1l111lll_opy_.format(str(e)))
def bstack1lll11ll1_opy_():
  global bstack111111111_opy_
  if bstack111111111_opy_.isRunning():
    logger.info(bstack1l1ll1lll1_opy_)
    bstack111111111_opy_.stop()
  bstack111111111_opy_ = None
def bstack11l11llll_opy_(bstack1l1l1111l1_opy_=[]):
  global CONFIG
  bstack11l11111l_opy_ = []
  bstack11ll111ll1_opy_ = [bstack111l111_opy_ (u"࠭࡯ࡴࠩ৥"), bstack111l111_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪ০"), bstack111l111_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬ১"), bstack111l111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ২"), bstack111l111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ৩"), bstack111l111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ৪")]
  try:
    for err in bstack1l1l1111l1_opy_:
      bstack1lll111l11_opy_ = {}
      for k in bstack11ll111ll1_opy_:
        val = CONFIG[bstack111l111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ৫")][int(err[bstack111l111_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ৬")])].get(k)
        if val:
          bstack1lll111l11_opy_[k] = val
      if(err[bstack111l111_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭৭")] != bstack111l111_opy_ (u"ࠨࠩ৮")):
        bstack1lll111l11_opy_[bstack111l111_opy_ (u"ࠩࡷࡩࡸࡺࡳࠨ৯")] = {
          err[bstack111l111_opy_ (u"ࠪࡲࡦࡳࡥࠨৰ")]: err[bstack111l111_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪৱ")]
        }
        bstack11l11111l_opy_.append(bstack1lll111l11_opy_)
  except Exception as e:
    logger.debug(bstack111l111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧࡱࡵࡱࡦࡺࡴࡪࡰࡪࠤࡩࡧࡴࡢࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸ࠿ࠦࠧ৲") + str(e))
  finally:
    return bstack11l11111l_opy_
def bstack11l11lllll_opy_(file_name):
  bstack111lllll_opy_ = []
  try:
    bstack1l1lll11_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1l1lll11_opy_):
      with open(bstack1l1lll11_opy_) as f:
        bstack11l1llll11_opy_ = json.load(f)
        bstack111lllll_opy_ = bstack11l1llll11_opy_
      os.remove(bstack1l1lll11_opy_)
    return bstack111lllll_opy_
  except Exception as e:
    logger.debug(bstack111l111_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡨ࡬ࡲࡩ࡯࡮ࡨࠢࡨࡶࡷࡵࡲࠡ࡮࡬ࡷࡹࡀࠠࠨ৳") + str(e))
    return bstack111lllll_opy_
def bstack1ll111111l_opy_():
  try:
      from bstack_utils.constants import bstack1llll11l11_opy_, EVENTS
      from bstack_utils.helper import bstack1llll111l_opy_, get_host_info, bstack1ll1ll11_opy_
      from datetime import datetime
      from filelock import FileLock
      bstack1llllll1ll_opy_ = os.path.join(os.getcwd(), bstack111l111_opy_ (u"ࠧ࡭ࡱࡪࠫ৴"), bstack111l111_opy_ (u"ࠨ࡭ࡨࡽ࠲ࡳࡥࡵࡴ࡬ࡧࡸ࠴ࡪࡴࡱࡱࠫ৵"))
      lock = FileLock(bstack1llllll1ll_opy_+bstack111l111_opy_ (u"ࠤ࠱ࡰࡴࡩ࡫ࠣ৶"))
      def bstack1ll1ll1ll1_opy_():
          try:
              with lock:
                  with open(bstack1llllll1ll_opy_, bstack111l111_opy_ (u"ࠥࡶࠧ৷"), encoding=bstack111l111_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥ৸")) as file:
                      data = json.load(file)
                      config = {
                          bstack111l111_opy_ (u"ࠧ࡮ࡥࡢࡦࡨࡶࡸࠨ৹"): {
                              bstack111l111_opy_ (u"ࠨࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠧ৺"): bstack111l111_opy_ (u"ࠢࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠥ৻"),
                          }
                      }
                      bstack111ll1111_opy_ = datetime.utcnow()
                      bstack1ll1ll1l1_opy_ = bstack111ll1111_opy_.strftime(bstack111l111_opy_ (u"ࠣࠧ࡜࠱ࠪࡳ࠭ࠦࡦࡗࠩࡍࡀࠥࡎ࠼ࠨࡗ࠳ࠫࡦࠡࡗࡗࡇࠧৼ"))
                      bstack11l1111l_opy_ = os.environ.get(bstack111l111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ৽")) if os.environ.get(bstack111l111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ৾")) else bstack1ll1ll11_opy_.get_property(bstack111l111_opy_ (u"ࠦࡸࡪ࡫ࡓࡷࡱࡍࡩࠨ৿"))
                      payload = {
                          bstack111l111_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠤ਀"): bstack111l111_opy_ (u"ࠨࡳࡥ࡭ࡢࡩࡻ࡫࡮ࡵࡵࠥਁ"),
                          bstack111l111_opy_ (u"ࠢࡥࡣࡷࡥࠧਂ"): {
                              bstack111l111_opy_ (u"ࠣࡶࡨࡷࡹ࡮ࡵࡣࡡࡸࡹ࡮ࡪࠢਃ"): bstack11l1111l_opy_,
                              bstack111l111_opy_ (u"ࠤࡦࡶࡪࡧࡴࡦࡦࡢࡨࡦࡿࠢ਄"): bstack1ll1ll1l1_opy_,
                              bstack111l111_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡱࡥࡲ࡫ࠢਅ"): bstack111l111_opy_ (u"ࠦࡘࡊࡋࡇࡧࡤࡸࡺࡸࡥࡑࡧࡵࡪࡴࡸ࡭ࡢࡰࡦࡩࠧਆ"),
                              bstack111l111_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣ࡯ࡹ࡯࡯ࠤਇ"): {
                                  bstack111l111_opy_ (u"ࠨ࡭ࡦࡣࡶࡹࡷ࡫ࡳࠣਈ"): data,
                                  bstack111l111_opy_ (u"ࠢࡴࡦ࡮ࡖࡺࡴࡉࡥࠤਉ"): bstack1ll1ll11_opy_.get_property(bstack111l111_opy_ (u"ࠣࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠥਊ"))
                              },
                              bstack111l111_opy_ (u"ࠤࡸࡷࡪࡸ࡟ࡥࡣࡷࡥࠧ਋"): bstack1ll1ll11_opy_.get_property(bstack111l111_opy_ (u"ࠥࡹࡸ࡫ࡲࡏࡣࡰࡩࠧ਌")),
                              bstack111l111_opy_ (u"ࠦ࡭ࡵࡳࡵࡡ࡬ࡲ࡫ࡵࠢ਍"): get_host_info()
                          }
                      }
                      bstack1l1ll111ll_opy_ = bstack1l1ll11l1_opy_(cli.config, [bstack111l111_opy_ (u"ࠧࡧࡰࡪࡵࠥ਎"), bstack111l111_opy_ (u"ࠨࡥࡥࡵࡌࡲࡸࡺࡲࡶ࡯ࡨࡲࡹࡧࡴࡪࡱࡱࠦਏ"), bstack111l111_opy_ (u"ࠢࡢࡲ࡬ࠦਐ")], bstack1llll11l11_opy_)
                      response = bstack1llll111l_opy_(bstack111l111_opy_ (u"ࠣࡒࡒࡗ࡙ࠨ਑"), bstack1l1ll111ll_opy_, payload, config)
                      if(response.status_code >= 200 and response.status_code < 300):
                          logger.debug(bstack111l111_opy_ (u"ࠤࡇࡥࡹࡧࠠࡴࡧࡱࡸࠥࡹࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡹࡵࠠࡼࡿࠣࡻ࡮ࡺࡨࠡࡦࡤࡸࡦࠦࡻࡾࠤ਒").format(bstack1llll11l11_opy_, payload))
                      else:
                          logger.debug(bstack111l111_opy_ (u"ࠥࡖࡪࡷࡵࡦࡵࡷࠤ࡫ࡧࡩ࡭ࡧࡧࠤ࡫ࡵࡲࠡࡽࢀࠤࡼ࡯ࡴࡩࠢࡧࡥࡹࡧࠠࡼࡿࠥਓ").format(bstack1llll11l11_opy_, payload))
          except Exception as e:
              logger.debug(bstack111l111_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡱࡨࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵࠣࡨࡦࡺࡡࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶࠥࢁࡽࠣਔ").format(e))
      bstack1ll1ll1ll1_opy_()
      bstack1l1llll111_opy_(bstack1llllll1ll_opy_, logger)
  except:
    pass
def bstack111ll1l11_opy_():
  global bstack1ll1ll1lll_opy_
  global bstack11ll1lllll_opy_
  global bstack11lll1ll_opy_
  global bstack1111l1l1l_opy_
  global bstack1111ll1ll_opy_
  global bstack1ll1111ll_opy_
  global CONFIG
  bstack11l1l11111_opy_ = os.environ.get(bstack111l111_opy_ (u"ࠬࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉ࠭ਕ"))
  if bstack11l1l11111_opy_ in [bstack111l111_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬਖ"), bstack111l111_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ਗ")]:
    bstack11l11ll1l1_opy_()
  percy.shutdown()
  if bstack1ll1ll1lll_opy_:
    logger.warning(bstack1l11111l1_opy_.format(str(bstack1ll1ll1lll_opy_)))
  else:
    try:
      bstack1lllll1ll1_opy_ = bstack111ll11ll_opy_(bstack111l111_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧਘ"), logger)
      if bstack1lllll1ll1_opy_.get(bstack111l111_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧਙ")) and bstack1lllll1ll1_opy_.get(bstack111l111_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨਚ")).get(bstack111l111_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ਛ")):
        logger.warning(bstack1l11111l1_opy_.format(str(bstack1lllll1ll1_opy_[bstack111l111_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪਜ")][bstack111l111_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨਝ")])))
    except Exception as e:
      logger.error(e)
  if cli.is_running():
    bstack1ll1l1ll1l_opy_.invoke(bstack111ll1ll_opy_.bstack111llll1_opy_)
  logger.info(bstack111lll1l_opy_)
  global bstack111111111_opy_
  if bstack111111111_opy_:
    bstack1lll11ll1_opy_()
  try:
    with bstack11lllllll_opy_:
      bstack11lllll1l1_opy_ = bstack11ll1lllll_opy_.copy()
    for driver in bstack11lllll1l1_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack11111l1l_opy_)
  if bstack1ll1111ll_opy_ == bstack111l111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ਞ"):
    bstack1111ll1ll_opy_ = bstack11l11lllll_opy_(bstack111l111_opy_ (u"ࠨࡴࡲࡦࡴࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩਟ"))
  if bstack1ll1111ll_opy_ == bstack111l111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩਠ") and len(bstack1111l1l1l_opy_) == 0:
    bstack1111l1l1l_opy_ = bstack11l11lllll_opy_(bstack111l111_opy_ (u"ࠪࡴࡼࡥࡰࡺࡶࡨࡷࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨਡ"))
    if len(bstack1111l1l1l_opy_) == 0:
      bstack1111l1l1l_opy_ = bstack11l11lllll_opy_(bstack111l111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡵࡶࡰࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪਢ"))
  bstack1lll1lllll_opy_ = bstack111l111_opy_ (u"ࠬ࠭ਣ")
  if len(bstack11lll1ll_opy_) > 0:
    bstack1lll1lllll_opy_ = bstack11l11llll_opy_(bstack11lll1ll_opy_)
  elif len(bstack1111l1l1l_opy_) > 0:
    bstack1lll1lllll_opy_ = bstack11l11llll_opy_(bstack1111l1l1l_opy_)
  elif len(bstack1111ll1ll_opy_) > 0:
    bstack1lll1lllll_opy_ = bstack11l11llll_opy_(bstack1111ll1ll_opy_)
  elif len(bstack1llll1l1_opy_) > 0:
    bstack1lll1lllll_opy_ = bstack11l11llll_opy_(bstack1llll1l1_opy_)
  if bool(bstack1lll1lllll_opy_):
    bstack1l1ll1llll_opy_(bstack1lll1lllll_opy_)
  else:
    bstack1l1ll1llll_opy_()
  bstack1l1llll111_opy_(bstack11llll1l1l_opy_, logger)
  if bstack11l1l11111_opy_ not in [bstack111l111_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧਤ")]:
    bstack1ll111111l_opy_()
  bstack1l1111ll_opy_.bstack1l1111ll1l_opy_(CONFIG)
  if len(bstack1111ll1ll_opy_) > 0:
    sys.exit(len(bstack1111ll1ll_opy_))
def bstack1ll111ll11_opy_(bstack11lll1111_opy_, frame):
  global bstack1ll1ll11_opy_
  logger.error(bstack11ll1lll1_opy_)
  bstack1ll1ll11_opy_.bstack1ll11l1l_opy_(bstack111l111_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡏࡱࠪਥ"), bstack11lll1111_opy_)
  if hasattr(signal, bstack111l111_opy_ (u"ࠨࡕ࡬࡫ࡳࡧ࡬ࡴࠩਦ")):
    bstack1ll1ll11_opy_.bstack1ll11l1l_opy_(bstack111l111_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩਧ"), signal.Signals(bstack11lll1111_opy_).name)
  else:
    bstack1ll1ll11_opy_.bstack1ll11l1l_opy_(bstack111l111_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪਨ"), bstack111l111_opy_ (u"ࠫࡘࡏࡇࡖࡐࡎࡒࡔ࡝ࡎࠨ਩"))
  if cli.is_running():
    bstack1ll1l1ll1l_opy_.invoke(bstack111ll1ll_opy_.bstack111llll1_opy_)
  bstack11l1l11111_opy_ = os.environ.get(bstack111l111_opy_ (u"ࠬࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉ࠭ਪ"))
  if bstack11l1l11111_opy_ == bstack111l111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ਫ") and not cli.is_enabled(CONFIG):
    bstack1l1ll1l11_opy_.stop(bstack1ll1ll11_opy_.get_property(bstack111l111_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡔ࡫ࡪࡲࡦࡲࠧਬ")))
  bstack111ll1l11_opy_()
  sys.exit(1)
def bstack11l11ll1ll_opy_(err):
  logger.critical(bstack11ll1l1111_opy_.format(str(err)))
  bstack1l1ll1llll_opy_(bstack11ll1l1111_opy_.format(str(err)), True)
  atexit.unregister(bstack111ll1l11_opy_)
  bstack11l11ll1l1_opy_()
  sys.exit(1)
def bstack1l1lll1ll_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1l1ll1llll_opy_(message, True)
  atexit.unregister(bstack111ll1l11_opy_)
  bstack11l11ll1l1_opy_()
  sys.exit(1)
def bstack11l1ll1ll1_opy_():
  global CONFIG
  global bstack11ll111111_opy_
  global bstack1l11l11l_opy_
  global bstack11l1l111_opy_
  CONFIG = bstack1l1111111_opy_()
  load_dotenv(CONFIG.get(bstack111l111_opy_ (u"ࠨࡧࡱࡺࡋ࡯࡬ࡦࠩਭ")))
  bstack1l1ll1l1_opy_()
  bstack1l1111ll11_opy_()
  CONFIG = bstack1llll1lll1_opy_(CONFIG)
  update(CONFIG, bstack1l11l11l_opy_)
  update(CONFIG, bstack11ll111111_opy_)
  if not cli.is_enabled(CONFIG):
    CONFIG = bstack11l11ll1l_opy_(CONFIG)
  bstack11l1l111_opy_ = bstack1lllll1lll_opy_(CONFIG)
  os.environ[bstack111l111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬਮ")] = bstack11l1l111_opy_.__str__().lower()
  bstack1ll1ll11_opy_.bstack1ll11l1l_opy_(bstack111l111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫਯ"), bstack11l1l111_opy_)
  if (bstack111l111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧਰ") in CONFIG and bstack111l111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ਱") in bstack11ll111111_opy_) or (
          bstack111l111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩਲ") in CONFIG and bstack111l111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪਲ਼") not in bstack1l11l11l_opy_):
    if os.getenv(bstack111l111_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬ਴")):
      CONFIG[bstack111l111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫਵ")] = os.getenv(bstack111l111_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧਸ਼"))
    else:
      if not CONFIG.get(bstack111l111_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠢ਷"), bstack111l111_opy_ (u"ࠧࠨਸ")) in bstack1lllll1l11_opy_:
        bstack1l1ll111l1_opy_()
  elif (bstack111l111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩਹ") not in CONFIG and bstack111l111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ਺") in CONFIG) or (
          bstack111l111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ਻") in bstack1l11l11l_opy_ and bstack111l111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩ਼ࠬ") not in bstack11ll111111_opy_):
    del (CONFIG[bstack111l111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ਽")])
  if bstack1lll111111_opy_(CONFIG):
    bstack11l11ll1ll_opy_(bstack1ll11ll1l_opy_)
  Config.bstack1ll11ll1_opy_().bstack1ll11l1l_opy_(bstack111l111_opy_ (u"ࠦࡺࡹࡥࡳࡐࡤࡱࡪࠨਾ"), CONFIG[bstack111l111_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧਿ")])
  bstack1l11l111ll_opy_()
  bstack1lll1lll1l_opy_()
  if bstack1l11111lll_opy_ and not CONFIG.get(bstack111l111_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠤੀ"), bstack111l111_opy_ (u"ࠢࠣੁ")) in bstack1lllll1l11_opy_:
    CONFIG[bstack111l111_opy_ (u"ࠨࡣࡳࡴࠬੂ")] = bstack1lll1111_opy_(CONFIG)
    logger.info(bstack11l111ll1_opy_.format(CONFIG[bstack111l111_opy_ (u"ࠩࡤࡴࡵ࠭੃")]))
  if not bstack11l1l111_opy_:
    CONFIG[bstack111l111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭੄")] = [{}]
def bstack11ll1lll11_opy_(config, bstack1lll11111_opy_):
  global CONFIG
  global bstack1l11111lll_opy_
  CONFIG = config
  bstack1l11111lll_opy_ = bstack1lll11111_opy_
def bstack1lll1lll1l_opy_():
  global CONFIG
  global bstack1l11111lll_opy_
  if bstack111l111_opy_ (u"ࠫࡦࡶࡰࠨ੅") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1l1lll1ll_opy_(e, bstack1111lllll_opy_)
    bstack1l11111lll_opy_ = True
    bstack1ll1ll11_opy_.bstack1ll11l1l_opy_(bstack111l111_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ੆"), True)
def bstack1lll1111_opy_(config):
  bstack11lll1l11_opy_ = bstack111l111_opy_ (u"࠭ࠧੇ")
  app = config[bstack111l111_opy_ (u"ࠧࡢࡲࡳࠫੈ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack11111l11l_opy_:
      if os.path.exists(app):
        bstack11lll1l11_opy_ = bstack1l111l11ll_opy_(config, app)
      elif bstack11l1l1ll11_opy_(app):
        bstack11lll1l11_opy_ = app
      else:
        bstack11l11ll1ll_opy_(bstack1111l1lll_opy_.format(app))
    else:
      if bstack11l1l1ll11_opy_(app):
        bstack11lll1l11_opy_ = app
      elif os.path.exists(app):
        bstack11lll1l11_opy_ = bstack1l111l11ll_opy_(app)
      else:
        bstack11l11ll1ll_opy_(bstack1111l11ll_opy_)
  else:
    if len(app) > 2:
      bstack11l11ll1ll_opy_(bstack111l1ll11_opy_)
    elif len(app) == 2:
      if bstack111l111_opy_ (u"ࠨࡲࡤࡸ࡭࠭੉") in app and bstack111l111_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ੊") in app:
        if os.path.exists(app[bstack111l111_opy_ (u"ࠪࡴࡦࡺࡨࠨੋ")]):
          bstack11lll1l11_opy_ = bstack1l111l11ll_opy_(config, app[bstack111l111_opy_ (u"ࠫࡵࡧࡴࡩࠩੌ")], app[bstack111l111_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨ੍")])
        else:
          bstack11l11ll1ll_opy_(bstack1111l1lll_opy_.format(app))
      else:
        bstack11l11ll1ll_opy_(bstack111l1ll11_opy_)
    else:
      for key in app:
        if key in bstack1111ll11l_opy_:
          if key == bstack111l111_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ੎"):
            if os.path.exists(app[key]):
              bstack11lll1l11_opy_ = bstack1l111l11ll_opy_(config, app[key])
            else:
              bstack11l11ll1ll_opy_(bstack1111l1lll_opy_.format(app))
          else:
            bstack11lll1l11_opy_ = app[key]
        else:
          bstack11l11ll1ll_opy_(bstack1l11l11ll_opy_)
  return bstack11lll1l11_opy_
def bstack11l1l1ll11_opy_(bstack11lll1l11_opy_):
  import re
  bstack1l11ll111l_opy_ = re.compile(bstack111l111_opy_ (u"ࡲࠣࡠ࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯ࠪࠢ੏"))
  bstack1lll11l11_opy_ = re.compile(bstack111l111_opy_ (u"ࡳࠤࡡ࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰࠯࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭ࠨࠧ੐"))
  if bstack111l111_opy_ (u"ࠩࡥࡷ࠿࠵࠯ࠨੑ") in bstack11lll1l11_opy_ or re.fullmatch(bstack1l11ll111l_opy_, bstack11lll1l11_opy_) or re.fullmatch(bstack1lll11l11_opy_, bstack11lll1l11_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack1l11llll_opy_, stage=STAGE.bstack11l1llll1_opy_, bstack11llll1lll_opy_=bstack1ll1l11l1l_opy_)
def bstack1l111l11ll_opy_(config, path, bstack111ll11l1_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack111l111_opy_ (u"ࠪࡶࡧ࠭੒")).read()).hexdigest()
  bstack1l1ll1l1l_opy_ = bstack1l1l1l1l1_opy_(md5_hash)
  bstack11lll1l11_opy_ = None
  if bstack1l1ll1l1l_opy_:
    logger.info(bstack1llll1l1l_opy_.format(bstack1l1ll1l1l_opy_, md5_hash))
    return bstack1l1ll1l1l_opy_
  bstack1l1111lll_opy_ = datetime.datetime.now()
  bstack1l11l1l1_opy_ = MultipartEncoder(
    fields={
      bstack111l111_opy_ (u"ࠫ࡫࡯࡬ࡦࠩ੓"): (os.path.basename(path), open(os.path.abspath(path), bstack111l111_opy_ (u"ࠬࡸࡢࠨ੔")), bstack111l111_opy_ (u"࠭ࡴࡦࡺࡷ࠳ࡵࡲࡡࡪࡰࠪ੕")),
      bstack111l111_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪ੖"): bstack111ll11l1_opy_
    }
  )
  response = requests.post(bstack1llllll1l1_opy_, data=bstack1l11l1l1_opy_,
                           headers={bstack111l111_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ੗"): bstack1l11l1l1_opy_.content_type},
                           auth=(config[bstack111l111_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ੘")], config[bstack111l111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ਖ਼")]))
  try:
    res = json.loads(response.text)
    bstack11lll1l11_opy_ = res[bstack111l111_opy_ (u"ࠫࡦࡶࡰࡠࡷࡵࡰࠬਗ਼")]
    logger.info(bstack1l1lll1111_opy_.format(bstack11lll1l11_opy_))
    bstack1ll11l1ll_opy_(md5_hash, bstack11lll1l11_opy_)
    cli.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽ࡹࡵࡲ࡯ࡢࡦࡢࡥࡵࡶࠢਜ਼"), datetime.datetime.now() - bstack1l1111lll_opy_)
  except ValueError as err:
    bstack11l11ll1ll_opy_(bstack11llll111_opy_.format(str(err)))
  return bstack11lll1l11_opy_
def bstack1l11l111ll_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack1l111ll1ll_opy_
  bstack1lllll11ll_opy_ = 1
  bstack1ll11ll11_opy_ = 1
  if bstack111l111_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ੜ") in CONFIG:
    bstack1ll11ll11_opy_ = CONFIG[bstack111l111_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ੝")]
  else:
    bstack1ll11ll11_opy_ = bstack1l11l1ll_opy_(framework_name, args) or 1
  if bstack111l111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫਫ਼") in CONFIG:
    bstack1lllll11ll_opy_ = len(CONFIG[bstack111l111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ੟")])
  bstack1l111ll1ll_opy_ = int(bstack1ll11ll11_opy_) * int(bstack1lllll11ll_opy_)
def bstack1l11l1ll_opy_(framework_name, args):
  if framework_name == bstack1lll11ll11_opy_ and args and bstack111l111_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨ੠") in args:
      bstack1lll1111l1_opy_ = args.index(bstack111l111_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩ੡"))
      return int(args[bstack1lll1111l1_opy_ + 1]) or 1
  return 1
def bstack1l1l1l1l1_opy_(md5_hash):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack111l111_opy_ (u"ࠬ࡬ࡩ࡭ࡧ࡯ࡳࡨࡱࠠ࡯ࡱࡷࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠬࠡࡷࡶ࡭ࡳ࡭ࠠࡣࡣࡶ࡭ࡨࠦࡦࡪ࡮ࡨࠤࡴࡶࡥࡳࡣࡷ࡭ࡴࡴࡳࠨ੢"))
    bstack1l1l1ll1l1_opy_ = os.path.join(os.path.expanduser(bstack111l111_opy_ (u"࠭ࡾࠨ੣")), bstack111l111_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ੤"), bstack111l111_opy_ (u"ࠨࡣࡳࡴ࡚ࡶ࡬ࡰࡣࡧࡑࡉ࠻ࡈࡢࡵ࡫࠲࡯ࡹ࡯࡯ࠩ੥"))
    if os.path.exists(bstack1l1l1ll1l1_opy_):
      try:
        bstack1ll11l11ll_opy_ = json.load(open(bstack1l1l1ll1l1_opy_, bstack111l111_opy_ (u"ࠩࡵࡦࠬ੦")))
        if md5_hash in bstack1ll11l11ll_opy_:
          bstack1ll1lll11_opy_ = bstack1ll11l11ll_opy_[md5_hash]
          bstack11l11l111_opy_ = datetime.datetime.now()
          bstack1ll111l1_opy_ = datetime.datetime.strptime(bstack1ll1lll11_opy_[bstack111l111_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭੧")], bstack111l111_opy_ (u"ࠫࠪࡪ࠯ࠦ࡯࠲ࠩ࡞ࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨ੨"))
          if (bstack11l11l111_opy_ - bstack1ll111l1_opy_).days > 30:
            return None
          elif version.parse(str(__version__)) > version.parse(bstack1ll1lll11_opy_[bstack111l111_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ੩")]):
            return None
          return bstack1ll1lll11_opy_[bstack111l111_opy_ (u"࠭ࡩࡥࠩ੪")]
      except Exception as e:
        logger.debug(bstack111l111_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡲࡦࡣࡧ࡭ࡳ࡭ࠠࡎࡆ࠸ࠤ࡭ࡧࡳࡩࠢࡩ࡭ࡱ࡫࠺ࠡࡽࢀࠫ੫").format(str(e)))
    return None
  bstack1l1l1ll1l1_opy_ = os.path.join(os.path.expanduser(bstack111l111_opy_ (u"ࠨࢀࠪ੬")), bstack111l111_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ੭"), bstack111l111_opy_ (u"ࠪࡥࡵࡶࡕࡱ࡮ࡲࡥࡩࡓࡄ࠶ࡊࡤࡷ࡭࠴ࡪࡴࡱࡱࠫ੮"))
  lock_file = bstack1l1l1ll1l1_opy_ + bstack111l111_opy_ (u"ࠫ࠳ࡲ࡯ࡤ࡭ࠪ੯")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack1l1l1ll1l1_opy_):
        with open(bstack1l1l1ll1l1_opy_, bstack111l111_opy_ (u"ࠬࡸࠧੰ")) as f:
          content = f.read().strip()
          if content:
            bstack1ll11l11ll_opy_ = json.loads(content)
            if md5_hash in bstack1ll11l11ll_opy_:
              bstack1ll1lll11_opy_ = bstack1ll11l11ll_opy_[md5_hash]
              bstack11l11l111_opy_ = datetime.datetime.now()
              bstack1ll111l1_opy_ = datetime.datetime.strptime(bstack1ll1lll11_opy_[bstack111l111_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩੱ")], bstack111l111_opy_ (u"ࠧࠦࡦ࠲ࠩࡲ࠵࡚ࠥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫੲ"))
              if (bstack11l11l111_opy_ - bstack1ll111l1_opy_).days > 30:
                return None
              elif version.parse(str(__version__)) > version.parse(bstack1ll1lll11_opy_[bstack111l111_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ੳ")]):
                return None
              return bstack1ll1lll11_opy_[bstack111l111_opy_ (u"ࠩ࡬ࡨࠬੴ")]
      return None
  except Exception as e:
    logger.debug(bstack111l111_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡺ࡭ࡹ࡮ࠠࡧ࡫࡯ࡩࠥࡲ࡯ࡤ࡭࡬ࡲ࡬ࠦࡦࡰࡴࠣࡑࡉ࠻ࠠࡩࡣࡶ࡬࠿ࠦࡻࡾࠩੵ").format(str(e)))
    return None
def bstack1ll11l1ll_opy_(md5_hash, bstack11lll1l11_opy_):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack111l111_opy_ (u"ࠫ࡫࡯࡬ࡦ࡮ࡲࡧࡰࠦ࡮ࡰࡶࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪ࠲ࠠࡶࡵ࡬ࡲ࡬ࠦࡢࡢࡵ࡬ࡧࠥ࡬ࡩ࡭ࡧࠣࡳࡵ࡫ࡲࡢࡶ࡬ࡳࡳࡹࠧ੶"))
    bstack11l1l1l1l1_opy_ = os.path.join(os.path.expanduser(bstack111l111_opy_ (u"ࠬࢄࠧ੷")), bstack111l111_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭੸"))
    if not os.path.exists(bstack11l1l1l1l1_opy_):
      os.makedirs(bstack11l1l1l1l1_opy_)
    bstack1l1l1ll1l1_opy_ = os.path.join(os.path.expanduser(bstack111l111_opy_ (u"ࠧࡿࠩ੹")), bstack111l111_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ੺"), bstack111l111_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪ੻"))
    bstack1ll111l1ll_opy_ = {
      bstack111l111_opy_ (u"ࠪ࡭ࡩ࠭੼"): bstack11lll1l11_opy_,
      bstack111l111_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ੽"): datetime.datetime.strftime(datetime.datetime.now(), bstack111l111_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩ੾")),
      bstack111l111_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ੿"): str(__version__)
    }
    try:
      bstack1ll11l11ll_opy_ = {}
      if os.path.exists(bstack1l1l1ll1l1_opy_):
        bstack1ll11l11ll_opy_ = json.load(open(bstack1l1l1ll1l1_opy_, bstack111l111_opy_ (u"ࠧࡳࡤࠪ઀")))
      bstack1ll11l11ll_opy_[md5_hash] = bstack1ll111l1ll_opy_
      with open(bstack1l1l1ll1l1_opy_, bstack111l111_opy_ (u"ࠣࡹ࠮ࠦઁ")) as outfile:
        json.dump(bstack1ll11l11ll_opy_, outfile)
    except Exception as e:
      logger.debug(bstack111l111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡷࡳࡨࡦࡺࡩ࡯ࡩࠣࡑࡉ࠻ࠠࡩࡣࡶ࡬ࠥ࡬ࡩ࡭ࡧ࠽ࠤࢀࢃࠧં").format(str(e)))
    return
  bstack11l1l1l1l1_opy_ = os.path.join(os.path.expanduser(bstack111l111_opy_ (u"ࠪࢂࠬઃ")), bstack111l111_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ઄"))
  if not os.path.exists(bstack11l1l1l1l1_opy_):
    os.makedirs(bstack11l1l1l1l1_opy_)
  bstack1l1l1ll1l1_opy_ = os.path.join(os.path.expanduser(bstack111l111_opy_ (u"ࠬࢄࠧઅ")), bstack111l111_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭આ"), bstack111l111_opy_ (u"ࠧࡢࡲࡳ࡙ࡵࡲ࡯ࡢࡦࡐࡈ࠺ࡎࡡࡴࡪ࠱࡮ࡸࡵ࡮ࠨઇ"))
  lock_file = bstack1l1l1ll1l1_opy_ + bstack111l111_opy_ (u"ࠨ࠰࡯ࡳࡨࡱࠧઈ")
  bstack1ll111l1ll_opy_ = {
    bstack111l111_opy_ (u"ࠩ࡬ࡨࠬઉ"): bstack11lll1l11_opy_,
    bstack111l111_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ઊ"): datetime.datetime.strftime(datetime.datetime.now(), bstack111l111_opy_ (u"ࠫࠪࡪ࠯ࠦ࡯࠲ࠩ࡞ࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨઋ")),
    bstack111l111_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪઌ"): str(__version__)
  }
  try:
    with FileLock(lock_file, timeout=10):
      bstack1ll11l11ll_opy_ = {}
      if os.path.exists(bstack1l1l1ll1l1_opy_):
        with open(bstack1l1l1ll1l1_opy_, bstack111l111_opy_ (u"࠭ࡲࠨઍ")) as f:
          content = f.read().strip()
          if content:
            bstack1ll11l11ll_opy_ = json.loads(content)
      bstack1ll11l11ll_opy_[md5_hash] = bstack1ll111l1ll_opy_
      with open(bstack1l1l1ll1l1_opy_, bstack111l111_opy_ (u"ࠢࡸࠤ઎")) as outfile:
        json.dump(bstack1ll11l11ll_opy_, outfile)
  except Exception as e:
    logger.debug(bstack111l111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡸ࡫ࡷ࡬ࠥ࡬ࡩ࡭ࡧࠣࡰࡴࡩ࡫ࡪࡰࡪࠤ࡫ࡵࡲࠡࡏࡇ࠹ࠥ࡮ࡡࡴࡪࠣࡹࡵࡪࡡࡵࡧ࠽ࠤࢀࢃࠧએ").format(str(e)))
def bstack11111lll1_opy_(self):
  return
def bstack1l1111l111_opy_(self):
  return
def bstack11l1llllll_opy_():
  global bstack1l11l1lll1_opy_
  bstack1l11l1lll1_opy_ = True
@measure(event_name=EVENTS.bstack11ll1ll11l_opy_, stage=STAGE.bstack11l1llll1_opy_, bstack11llll1lll_opy_=bstack1ll1l11l1l_opy_)
def bstack11l11111ll_opy_(self):
  global bstack11l1l1ll1l_opy_
  global bstack11l11ll11l_opy_
  global bstack111l1ll1l_opy_
  try:
    if bstack111l111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩઐ") in bstack11l1l1ll1l_opy_ and self.session_id != None and bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧઑ"), bstack111l111_opy_ (u"ࠫࠬ઒")) != bstack111l111_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ઓ"):
      bstack1ll1111ll1_opy_ = bstack111l111_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ઔ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack111l111_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧક")
      if bstack1ll1111ll1_opy_ == bstack111l111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨખ"):
        bstack1ll1ll1111_opy_(logger)
      if self != None:
        bstack1l11ll11ll_opy_(self, bstack1ll1111ll1_opy_, bstack111l111_opy_ (u"ࠩ࠯ࠤࠬગ").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack111l111_opy_ (u"ࠪࠫઘ")
    if bstack111l111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫઙ") in bstack11l1l1ll1l_opy_ and getattr(threading.current_thread(), bstack111l111_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫચ"), None):
      bstack1l1l11l111_opy_.bstack1ll1lll11l_opy_(self, bstack1llll1l111_opy_, logger, wait=True)
    if bstack111l111_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭છ") in bstack11l1l1ll1l_opy_:
      if not threading.currentThread().behave_test_status:
        bstack1l11ll11ll_opy_(self, bstack111l111_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢજ"))
      bstack1llll1ll_opy_.bstack111ll1ll1_opy_(self)
  except Exception as e:
    logger.debug(bstack111l111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࠤઝ") + str(e))
  bstack111l1ll1l_opy_(self)
  self.session_id = None
def bstack1lllll1l1l_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack11ll1111ll_opy_
    global bstack11l1l1ll1l_opy_
    command_executor = kwargs.get(bstack111l111_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠬઞ"), bstack111l111_opy_ (u"ࠪࠫટ"))
    bstack1111l1ll1_opy_ = False
    if type(command_executor) == str and bstack111l111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧઠ") in command_executor:
      bstack1111l1ll1_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack111l111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨડ") in str(getattr(command_executor, bstack111l111_opy_ (u"࠭࡟ࡶࡴ࡯ࠫઢ"), bstack111l111_opy_ (u"ࠧࠨણ"))):
      bstack1111l1ll1_opy_ = True
    else:
      kwargs = bstack1l1ll11l1l_opy_.bstack11l1ll1lll_opy_(bstack1l1lll1l11_opy_=kwargs, config=CONFIG)
      return bstack1lll1ll1_opy_(self, *args, **kwargs)
    if bstack1111l1ll1_opy_:
      bstack1ll11llll1_opy_ = bstack1l1ll1l1ll_opy_.bstack11l111ll_opy_(CONFIG, bstack11l1l1ll1l_opy_)
      if kwargs.get(bstack111l111_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩત")):
        kwargs[bstack111l111_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪથ")] = bstack11ll1111ll_opy_(kwargs[bstack111l111_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫદ")], bstack11l1l1ll1l_opy_, CONFIG, bstack1ll11llll1_opy_)
      elif kwargs.get(bstack111l111_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫધ")):
        kwargs[bstack111l111_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬન")] = bstack11ll1111ll_opy_(kwargs[bstack111l111_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭઩")], bstack11l1l1ll1l_opy_, CONFIG, bstack1ll11llll1_opy_)
  except Exception as e:
    logger.error(bstack111l111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩࡧࡱࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡕࡇࡏࠥࡩࡡࡱࡵ࠽ࠤࢀࢃࠢપ").format(str(e)))
  return bstack1lll1ll1_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack1l1lllll11_opy_, stage=STAGE.bstack11l1llll1_opy_, bstack11llll1lll_opy_=bstack1ll1l11l1l_opy_)
def bstack1l1l11ll11_opy_(self, command_executor=bstack111l111_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰࠳࠵࠻࠳࠶࠮࠱࠰࠴࠾࠹࠺࠴࠵ࠤફ"), *args, **kwargs):
  global bstack11l11ll11l_opy_
  global bstack11ll1lllll_opy_
  bstack1ll1ll1ll_opy_ = bstack1lllll1l1l_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack11llll1l11_opy_.on():
    return bstack1ll1ll1ll_opy_
  try:
    logger.debug(bstack111l111_opy_ (u"ࠩࡆࡳࡲࡳࡡ࡯ࡦࠣࡉࡽ࡫ࡣࡶࡶࡲࡶࠥࡽࡨࡦࡰࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡩࡴࠢࡩࡥࡱࡹࡥࠡ࠯ࠣࡿࢂ࠭બ").format(str(command_executor)))
    logger.debug(bstack111l111_opy_ (u"ࠪࡌࡺࡨࠠࡖࡔࡏࠤ࡮ࡹࠠ࠮ࠢࡾࢁࠬભ").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack111l111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧમ") in command_executor._url:
      bstack1ll1ll11_opy_.bstack1ll11l1l_opy_(bstack111l111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ય"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack111l111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩર") in command_executor):
    bstack1ll1ll11_opy_.bstack1ll11l1l_opy_(bstack111l111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ઱"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1l11lll1l1_opy_ = getattr(threading.current_thread(), bstack111l111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡕࡧࡶࡸࡒ࡫ࡴࡢࠩલ"), None)
  bstack11l1l1111_opy_ = {}
  if self.capabilities is not None:
    bstack11l1l1111_opy_[bstack111l111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡲࡦࡳࡥࠨળ")] = self.capabilities.get(bstack111l111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ઴"))
    bstack11l1l1111_opy_[bstack111l111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭વ")] = self.capabilities.get(bstack111l111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭શ"))
    bstack11l1l1111_opy_[bstack111l111_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡥ࡯ࡱࡶ࡬ࡳࡳࡹࠧષ")] = self.capabilities.get(bstack111l111_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬસ"))
  if CONFIG.get(bstack111l111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨહ"), False) and bstack1l1ll11l1l_opy_.bstack1l1llll1_opy_(bstack11l1l1111_opy_):
    threading.current_thread().a11yPlatform = True
  if bstack111l111_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ઺") in bstack11l1l1ll1l_opy_ or bstack111l111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ઻") in bstack11l1l1ll1l_opy_:
    bstack1l1ll1l11_opy_.bstack1l11l1llll_opy_(self)
  if bstack111l111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ઼ࠫ") in bstack11l1l1ll1l_opy_ and bstack1l11lll1l1_opy_ and bstack1l11lll1l1_opy_.get(bstack111l111_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬઽ"), bstack111l111_opy_ (u"࠭ࠧા")) == bstack111l111_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨિ"):
    bstack1l1ll1l11_opy_.bstack1l11l1llll_opy_(self)
  bstack11l11ll11l_opy_ = self.session_id
  with bstack11lllllll_opy_:
    bstack11ll1lllll_opy_.append(self)
  return bstack1ll1ll1ll_opy_
def bstack1ll111llll_opy_(args):
  return bstack111l111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠩી") in str(args)
def bstack1l1l1llll_opy_(self, driver_command, *args, **kwargs):
  global bstack1lll1l111_opy_
  global bstack11ll1l1l1l_opy_
  bstack1lll1lll1_opy_ = bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ુ"), None) and bstack1ll11lllll_opy_(
          threading.current_thread(), bstack111l111_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩૂ"), None)
  bstack1ll1l1lll1_opy_ = bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫૃ"), None) and bstack1ll11lllll_opy_(
          threading.current_thread(), bstack111l111_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧૄ"), None)
  bstack11ll1l1ll_opy_ = getattr(self, bstack111l111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭ૅ"), None) != None and getattr(self, bstack111l111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧ૆"), None) == True
  if not bstack11ll1l1l1l_opy_ and bstack111l111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨે") in CONFIG and CONFIG[bstack111l111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩૈ")] == True and bstack111lll1ll_opy_.bstack11l11l1l_opy_(driver_command) and (bstack11ll1l1ll_opy_ or bstack1lll1lll1_opy_ or bstack1ll1l1lll1_opy_) and not bstack1ll111llll_opy_(args):
    try:
      bstack11ll1l1l1l_opy_ = True
      logger.debug(bstack111l111_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡾࢁࠬૉ").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack111l111_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡧࡵࡪࡴࡸ࡭ࠡࡵࡦࡥࡳࠦࡻࡾࠩ૊").format(str(err)))
    bstack11ll1l1l1l_opy_ = False
  response = bstack1lll1l111_opy_(self, driver_command, *args, **kwargs)
  if (bstack111l111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫો") in str(bstack11l1l1ll1l_opy_).lower() or bstack111l111_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ૌ") in str(bstack11l1l1ll1l_opy_).lower()) and bstack11llll1l11_opy_.on():
    try:
      if driver_command == bstack111l111_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷ્ࠫ"):
        bstack1l1ll1l11_opy_.bstack1ll1l1lll_opy_({
            bstack111l111_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧ૎"): response[bstack111l111_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨ૏")],
            bstack111l111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪૐ"): bstack1l1ll1l11_opy_.current_test_uuid() if bstack1l1ll1l11_opy_.current_test_uuid() else bstack11llll1l11_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
@measure(event_name=EVENTS.bstack11l111l1l1_opy_, stage=STAGE.bstack11l1llll1_opy_, bstack11llll1lll_opy_=bstack1ll1l11l1l_opy_)
def bstack11ll1l1ll1_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack11l11ll11l_opy_
  global bstack1l11lllll_opy_
  global bstack1ll1l11l1l_opy_
  global bstack1l11l11l1l_opy_
  global bstack1lll1lll11_opy_
  global bstack11l1l1ll1l_opy_
  global bstack1lll1ll1_opy_
  global bstack11ll1lllll_opy_
  global bstack11l1ll1111_opy_
  global bstack1llll1l111_opy_
  if os.getenv(bstack111l111_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ૑")) is not None and bstack1l1ll11l1l_opy_.bstack11l1l1ll_opy_(CONFIG) is None:
    CONFIG[bstack111l111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ૒")] = True
  CONFIG[bstack111l111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ૓")] = str(bstack11l1l1ll1l_opy_) + str(__version__)
  bstack1l1ll1ll1_opy_ = os.environ[bstack111l111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ૔")]
  bstack1ll11llll1_opy_ = bstack1l1ll1l1ll_opy_.bstack11l111ll_opy_(CONFIG, bstack11l1l1ll1l_opy_)
  CONFIG[bstack111l111_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ૕")] = bstack1l1ll1ll1_opy_
  CONFIG[bstack111l111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ૖")] = bstack1ll11llll1_opy_
  if CONFIG.get(bstack111l111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ૗"),bstack111l111_opy_ (u"ࠫࠬ૘")) and bstack111l111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ૙") in bstack11l1l1ll1l_opy_:
    CONFIG[bstack111l111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭૚")].pop(bstack111l111_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬ૛"), None)
    CONFIG[bstack111l111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ૜")].pop(bstack111l111_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ૝"), None)
  command_executor = bstack1l11l11ll1_opy_()
  logger.debug(bstack1l111l11l_opy_.format(command_executor))
  proxy = bstack1l1l1l1lll_opy_(CONFIG, proxy)
  bstack11ll11l111_opy_ = 0 if bstack1l11lllll_opy_ < 0 else bstack1l11lllll_opy_
  try:
    if bstack1l11l11l1l_opy_ is True:
      bstack11ll11l111_opy_ = int(multiprocessing.current_process().name)
    elif bstack1lll1lll11_opy_ is True:
      bstack11ll11l111_opy_ = int(threading.current_thread().name)
  except:
    bstack11ll11l111_opy_ = 0
  bstack1l1l1llll1_opy_ = bstack1l1l1ll1l_opy_(CONFIG, bstack11ll11l111_opy_)
  logger.debug(bstack1l1lllll1_opy_.format(str(bstack1l1l1llll1_opy_)))
  if bstack111l111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ૞") in CONFIG and bstack1ll111l11l_opy_(CONFIG[bstack111l111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ૟")]):
    bstack1l111l1l11_opy_(bstack1l1l1llll1_opy_)
  if bstack1l1ll11l1l_opy_.bstack11l111lll_opy_(CONFIG, bstack11ll11l111_opy_) and bstack1l1ll11l1l_opy_.bstack1l11llll1l_opy_(bstack1l1l1llll1_opy_, options, desired_capabilities, CONFIG):
    threading.current_thread().a11yPlatform = True
    if (cli.accessibility is None or not cli.accessibility.is_enabled()):
      bstack1l1ll11l1l_opy_.set_capabilities(bstack1l1l1llll1_opy_, CONFIG)
  if desired_capabilities:
    bstack1l11lll11l_opy_ = bstack1llll1lll1_opy_(desired_capabilities)
    bstack1l11lll11l_opy_[bstack111l111_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬૠ")] = bstack1l11ll11l_opy_(CONFIG)
    bstack1lllll11_opy_ = bstack1l1l1ll1l_opy_(bstack1l11lll11l_opy_)
    if bstack1lllll11_opy_:
      bstack1l1l1llll1_opy_ = update(bstack1lllll11_opy_, bstack1l1l1llll1_opy_)
    desired_capabilities = None
  if options:
    bstack11lllll1l_opy_(options, bstack1l1l1llll1_opy_)
  if not options:
    options = bstack1l11l1ll1l_opy_(bstack1l1l1llll1_opy_)
  bstack1llll1l111_opy_ = CONFIG.get(bstack111l111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩૡ"))[bstack11ll11l111_opy_]
  if proxy and bstack1llllll1l_opy_() >= version.parse(bstack111l111_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧૢ")):
    options.proxy(proxy)
  if options and bstack1llllll1l_opy_() >= version.parse(bstack111l111_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧૣ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1llllll1l_opy_() < version.parse(bstack111l111_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ૤")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1l1l1llll1_opy_)
  logger.info(bstack1l11ll1l1l_opy_)
  bstack1ll11l1lll_opy_.end(EVENTS.bstack1ll11l11l1_opy_.value, EVENTS.bstack1ll11l11l1_opy_.value + bstack111l111_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ૥"), EVENTS.bstack1ll11l11l1_opy_.value + bstack111l111_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ૦"), status=True, failure=None, test_name=bstack1ll1l11l1l_opy_)
  if bstack111l111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡰࡳࡱࡩ࡭ࡱ࡫ࠧ૧") in kwargs:
    del kwargs[bstack111l111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡱࡴࡲࡪ࡮ࡲࡥࠨ૨")]
  if bstack1llllll1l_opy_() >= version.parse(bstack111l111_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧ૩")):
    bstack1lll1ll1_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
  elif bstack1llllll1l_opy_() >= version.parse(bstack111l111_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ૪")):
    bstack1lll1ll1_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1llllll1l_opy_() >= version.parse(bstack111l111_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩ૫")):
    bstack1lll1ll1_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1lll1ll1_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive)
  if bstack1l1ll11l1l_opy_.bstack11l111lll_opy_(CONFIG, bstack11ll11l111_opy_) and bstack1l1ll11l1l_opy_.bstack1l11llll1l_opy_(self.caps, options, desired_capabilities):
    if CONFIG[bstack111l111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬ૬")][bstack111l111_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪ૭")] == True:
      threading.current_thread().appA11yPlatform = True
      if cli.accessibility is None or not cli.accessibility.is_enabled():
        bstack1l1ll11l1l_opy_.set_capabilities(bstack1l1l1llll1_opy_, CONFIG)
  try:
    bstack1l111l1ll1_opy_ = bstack111l111_opy_ (u"ࠬ࠭૮")
    if bstack1llllll1l_opy_() >= version.parse(bstack111l111_opy_ (u"࠭࠴࠯࠲࠱࠴ࡧ࠷ࠧ૯")):
      if self.caps is not None:
        bstack1l111l1ll1_opy_ = self.caps.get(bstack111l111_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢ૰"))
    else:
      if self.capabilities is not None:
        bstack1l111l1ll1_opy_ = self.capabilities.get(bstack111l111_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣ૱"))
    if bstack1l111l1ll1_opy_:
      bstack11l111111_opy_(bstack1l111l1ll1_opy_)
      if bstack1llllll1l_opy_() <= version.parse(bstack111l111_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩ૲")):
        self.command_executor._url = bstack111l111_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦ૳") + bstack1l11111l1l_opy_ + bstack111l111_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣ૴")
      else:
        self.command_executor._url = bstack111l111_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢ૵") + bstack1l111l1ll1_opy_ + bstack111l111_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢ૶")
      logger.debug(bstack111111l11_opy_.format(bstack1l111l1ll1_opy_))
    else:
      logger.debug(bstack1l1111lll1_opy_.format(bstack111l111_opy_ (u"ࠢࡐࡲࡷ࡭ࡲࡧ࡬ࠡࡊࡸࡦࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠣ૷")))
  except Exception as e:
    logger.debug(bstack1l1111lll1_opy_.format(e))
  if bstack111l111_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ૸") in bstack11l1l1ll1l_opy_:
    bstack111lllll1l_opy_(bstack1l11lllll_opy_, bstack11l1ll1111_opy_)
  bstack11l11ll11l_opy_ = self.session_id
  if bstack111l111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩૹ") in bstack11l1l1ll1l_opy_ or bstack111l111_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪૺ") in bstack11l1l1ll1l_opy_ or bstack111l111_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪૻ") in bstack11l1l1ll1l_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack1l11lll1l1_opy_ = getattr(threading.current_thread(), bstack111l111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࡙࡫ࡳࡵࡏࡨࡸࡦ࠭ૼ"), None)
  if bstack111l111_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭૽") in bstack11l1l1ll1l_opy_ or bstack111l111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭૾") in bstack11l1l1ll1l_opy_:
    bstack1l1ll1l11_opy_.bstack1l11l1llll_opy_(self)
  if bstack111l111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ૿") in bstack11l1l1ll1l_opy_ and bstack1l11lll1l1_opy_ and bstack1l11lll1l1_opy_.get(bstack111l111_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ଀"), bstack111l111_opy_ (u"ࠪࠫଁ")) == bstack111l111_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬଂ"):
    bstack1l1ll1l11_opy_.bstack1l11l1llll_opy_(self)
  with bstack11lllllll_opy_:
    bstack11ll1lllll_opy_.append(self)
  if bstack111l111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨଃ") in CONFIG and bstack111l111_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ଄") in CONFIG[bstack111l111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଅ")][bstack11ll11l111_opy_]:
    bstack1ll1l11l1l_opy_ = CONFIG[bstack111l111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫଆ")][bstack11ll11l111_opy_][bstack111l111_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧଇ")]
  logger.debug(bstack11ll11l1l1_opy_.format(bstack11l11ll11l_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    from browserstack_sdk.__init__ import bstack1l1ll11lll_opy_
    def bstack111l1l1ll_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1lllllll11_opy_
      if(bstack111l111_opy_ (u"ࠥ࡭ࡳࡪࡥࡹ࠰࡭ࡷࠧଈ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack111l111_opy_ (u"ࠫࢃ࠭ଉ")), bstack111l111_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬଊ"), bstack111l111_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨଋ")), bstack111l111_opy_ (u"ࠧࡸࠩଌ")) as fp:
          fp.write(bstack111l111_opy_ (u"ࠣࠤ଍"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack111l111_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸࡠࡤࡶࡸࡦࡩ࡫࠯࡬ࡶࠦ଎")))):
          with open(args[1], bstack111l111_opy_ (u"ࠪࡶࠬଏ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack111l111_opy_ (u"ࠫࡦࡹࡹ࡯ࡥࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࡥ࡮ࡦࡹࡓࡥ࡬࡫ࠨࡤࡱࡱࡸࡪࡾࡴ࠭ࠢࡳࡥ࡬࡫ࠠ࠾ࠢࡹࡳ࡮ࡪࠠ࠱ࠫࠪଐ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack11l111l1ll_opy_)
            if bstack111l111_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ଑") in CONFIG and str(CONFIG[bstack111l111_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ଒")]).lower() != bstack111l111_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ଓ"):
                bstack11ll1l1l11_opy_ = bstack1l1ll11lll_opy_()
                bstack11l1111l1_opy_ = bstack111l111_opy_ (u"ࠨࠩࠪࠎ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠊࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡰࡢࡶ࡫ࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳࡞࠽ࠍࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠴ࡡࡀࠐࡣࡰࡰࡶࡸࠥࡶ࡟ࡪࡰࡧࡩࡽࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠴ࡠ࠿ࠏࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡹ࡬ࡪࡥࡨࠬ࠵࠲ࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࠬ࠿ࠏࡩ࡯࡯ࡵࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬ࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ࠭ࡀࠐࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴࡬ࡢࡷࡱࡧ࡭ࠦ࠽ࠡࡣࡶࡽࡳࡩࠠࠩ࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁࡻࠋࠢࠣࡰࡪࡺࠠࡤࡣࡳࡷࡀࠐࠠࠡࡶࡵࡽࠥࢁࡻࠋࠢࠣࠤࠥࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࠼ࠌࠣࠤࢂࢃࠠࡤࡣࡷࡧ࡭ࠦࠨࡦࡺࠬࠤࢀࢁࠊࠡࠢࠣࠤࡨࡵ࡮ࡴࡱ࡯ࡩ࠳࡫ࡲࡳࡱࡵࠬࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࡀࠢ࠭ࠢࡨࡼ࠮ࡁࠊࠡࠢࢀࢁࠏࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠨࡼࡽࠍࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥ࠭ࡻࡤࡦࡳ࡙ࡷࡲࡽࠨࠢ࠮ࠤࡪࡴࡣࡰࡦࡨ࡙ࡗࡏࡃࡰ࡯ࡳࡳࡳ࡫࡮ࡵࠪࡍࡗࡔࡔ࠮ࡴࡶࡵ࡭ࡳ࡭ࡩࡧࡻࠫࡧࡦࡶࡳࠪࠫ࠯ࠎࠥࠦࠠࠡ࠰࠱࠲ࡱࡧࡵ࡯ࡥ࡫ࡓࡵࡺࡩࡰࡰࡶࠎࠥࠦࡽࡾࠫ࠾ࠎࢂࢃ࠻ࠋ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࠎࠬ࠭ࠧଔ").format(bstack11ll1l1l11_opy_=bstack11ll1l1l11_opy_)
            lines.insert(1, bstack11l1111l1_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack111l111_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸࡠࡤࡶࡸࡦࡩ࡫࠯࡬ࡶࠦକ")), bstack111l111_opy_ (u"ࠪࡻࠬଖ")) as bstack1ll11111_opy_:
              bstack1ll11111_opy_.writelines(lines)
        CONFIG[bstack111l111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ଗ")] = str(bstack11l1l1ll1l_opy_) + str(__version__)
        bstack1l1ll1ll1_opy_ = os.environ[bstack111l111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪଘ")]
        bstack1ll11llll1_opy_ = bstack1l1ll1l1ll_opy_.bstack11l111ll_opy_(CONFIG, bstack11l1l1ll1l_opy_)
        CONFIG[bstack111l111_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩଙ")] = bstack1l1ll1ll1_opy_
        CONFIG[bstack111l111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩଚ")] = bstack1ll11llll1_opy_
        bstack11ll11l111_opy_ = 0 if bstack1l11lllll_opy_ < 0 else bstack1l11lllll_opy_
        try:
          if bstack1l11l11l1l_opy_ is True:
            bstack11ll11l111_opy_ = int(multiprocessing.current_process().name)
          elif bstack1lll1lll11_opy_ is True:
            bstack11ll11l111_opy_ = int(threading.current_thread().name)
        except:
          bstack11ll11l111_opy_ = 0
        CONFIG[bstack111l111_opy_ (u"ࠣࡷࡶࡩ࡜࠹ࡃࠣଛ")] = False
        CONFIG[bstack111l111_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣଜ")] = True
        bstack1l1l1llll1_opy_ = bstack1l1l1ll1l_opy_(CONFIG, bstack11ll11l111_opy_)
        logger.debug(bstack1l1lllll1_opy_.format(str(bstack1l1l1llll1_opy_)))
        if CONFIG.get(bstack111l111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧଝ")):
          bstack1l111l1l11_opy_(bstack1l1l1llll1_opy_)
        if bstack111l111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଞ") in CONFIG and bstack111l111_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪଟ") in CONFIG[bstack111l111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଠ")][bstack11ll11l111_opy_]:
          bstack1ll1l11l1l_opy_ = CONFIG[bstack111l111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଡ")][bstack11ll11l111_opy_][bstack111l111_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ଢ")]
        args.append(os.path.join(os.path.expanduser(bstack111l111_opy_ (u"ࠩࢁࠫଣ")), bstack111l111_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪତ"), bstack111l111_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭ଥ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1l1l1llll1_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack111l111_opy_ (u"ࠧ࡯࡮ࡥࡧࡻࡣࡧࡹࡴࡢࡥ࡮࠲࡯ࡹࠢଦ"))
      bstack1lllllll11_opy_ = True
      return bstack1lll11l111_opy_(self, args, bufsize=bufsize, executable=executable,
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
  def bstack111111lll_opy_(self,
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
    global bstack1l11lllll_opy_
    global bstack1ll1l11l1l_opy_
    global bstack1l11l11l1l_opy_
    global bstack1lll1lll11_opy_
    global bstack11l1l1ll1l_opy_
    CONFIG[bstack111l111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨଧ")] = str(bstack11l1l1ll1l_opy_) + str(__version__)
    bstack1l1ll1ll1_opy_ = os.environ[bstack111l111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬନ")]
    bstack1ll11llll1_opy_ = bstack1l1ll1l1ll_opy_.bstack11l111ll_opy_(CONFIG, bstack11l1l1ll1l_opy_)
    CONFIG[bstack111l111_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ଩")] = bstack1l1ll1ll1_opy_
    CONFIG[bstack111l111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫପ")] = bstack1ll11llll1_opy_
    bstack11ll11l111_opy_ = 0 if bstack1l11lllll_opy_ < 0 else bstack1l11lllll_opy_
    try:
      if bstack1l11l11l1l_opy_ is True:
        bstack11ll11l111_opy_ = int(multiprocessing.current_process().name)
      elif bstack1lll1lll11_opy_ is True:
        bstack11ll11l111_opy_ = int(threading.current_thread().name)
    except:
      bstack11ll11l111_opy_ = 0
    CONFIG[bstack111l111_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤଫ")] = True
    bstack1l1l1llll1_opy_ = bstack1l1l1ll1l_opy_(CONFIG, bstack11ll11l111_opy_)
    logger.debug(bstack1l1lllll1_opy_.format(str(bstack1l1l1llll1_opy_)))
    if CONFIG.get(bstack111l111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨବ")):
      bstack1l111l1l11_opy_(bstack1l1l1llll1_opy_)
    if bstack111l111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨଭ") in CONFIG and bstack111l111_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫମ") in CONFIG[bstack111l111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଯ")][bstack11ll11l111_opy_]:
      bstack1ll1l11l1l_opy_ = CONFIG[bstack111l111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫର")][bstack11ll11l111_opy_][bstack111l111_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ଱")]
    import urllib
    import json
    if bstack111l111_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧଲ") in CONFIG and str(CONFIG[bstack111l111_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨଳ")]).lower() != bstack111l111_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ଴"):
        bstack1111l111_opy_ = bstack1l1ll11lll_opy_()
        bstack11ll1l1l11_opy_ = bstack1111l111_opy_ + urllib.parse.quote(json.dumps(bstack1l1l1llll1_opy_))
    else:
        bstack11ll1l1l11_opy_ = bstack111l111_opy_ (u"࠭ࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠨଵ") + urllib.parse.quote(json.dumps(bstack1l1l1llll1_opy_))
    browser = self.connect(bstack11ll1l1l11_opy_)
    return browser
except Exception as e:
    pass
def bstack11lll1l11l_opy_():
    global bstack1lllllll11_opy_
    global bstack11l1l1ll1l_opy_
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1lll11l1_opy_
        global bstack1ll1ll11_opy_
        if not bstack11l1l111_opy_:
          global bstack1l11111l11_opy_
          if not bstack1l11111l11_opy_:
            from bstack_utils.helper import bstack111l11111_opy_, bstack1lll1l1ll_opy_, bstack1ll1l11ll1_opy_
            bstack1l11111l11_opy_ = bstack111l11111_opy_()
            bstack1lll1l1ll_opy_(bstack11l1l1ll1l_opy_)
            bstack1ll11llll1_opy_ = bstack1l1ll1l1ll_opy_.bstack11l111ll_opy_(CONFIG, bstack11l1l1ll1l_opy_)
            bstack1ll1ll11_opy_.bstack1ll11l1l_opy_(bstack111l111_opy_ (u"ࠢࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡕࡘࡏࡅࡗࡆࡘࡤࡓࡁࡑࠤଶ"), bstack1ll11llll1_opy_)
          BrowserType.connect = bstack1lll11l1_opy_
          return
        BrowserType.launch = bstack111111lll_opy_
        bstack1lllllll11_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack111l1l1ll_opy_
      bstack1lllllll11_opy_ = True
    except Exception as e:
      pass
def bstack1llll11ll_opy_(context, bstack11l1l11lll_opy_):
  try:
    context.page.evaluate(bstack111l111_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤଷ"), bstack111l111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿࠭ସ")+ json.dumps(bstack11l1l11lll_opy_) + bstack111l111_opy_ (u"ࠥࢁࢂࠨହ"))
  except Exception as e:
    logger.debug(bstack111l111_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡻࡾ࠼ࠣࡿࢂࠨ଺").format(str(e), traceback.format_exc()))
def bstack1ll1llllll_opy_(context, message, level):
  try:
    context.page.evaluate(bstack111l111_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨ଻"), bstack111l111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽଼ࠫ") + json.dumps(message) + bstack111l111_opy_ (u"ࠧ࠭ࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠪଽ") + json.dumps(level) + bstack111l111_opy_ (u"ࠨࡿࢀࠫା"))
  except Exception as e:
    logger.debug(bstack111l111_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠢࡾࢁ࠿ࠦࡻࡾࠤି").format(str(e), traceback.format_exc()))
@measure(event_name=EVENTS.bstack1lllll11l_opy_, stage=STAGE.bstack11l1llll1_opy_, bstack11llll1lll_opy_=bstack1ll1l11l1l_opy_)
def bstack1l1l1lll11_opy_(self, url):
  global bstack1111ll1l1_opy_
  try:
    bstack111l1llll_opy_(url)
  except Exception as err:
    logger.debug(bstack11l1ll11l_opy_.format(str(err)))
  try:
    bstack1111ll1l1_opy_(self, url)
  except Exception as e:
    try:
      bstack1ll1llll11_opy_ = str(e)
      if any(err_msg in bstack1ll1llll11_opy_ for err_msg in bstack11ll1l111_opy_):
        bstack111l1llll_opy_(url, True)
    except Exception as err:
      logger.debug(bstack11l1ll11l_opy_.format(str(err)))
    raise e
def bstack11111ll1_opy_(self):
  global bstack1ll1ll111l_opy_
  bstack1ll1ll111l_opy_ = self
  return
def bstack1l11lll1l_opy_(self):
  global bstack11l1ll1l11_opy_
  bstack11l1ll1l11_opy_ = self
  return
def bstack1ll11lll11_opy_(test_name, bstack11l11l11ll_opy_):
  global CONFIG
  if percy.bstack1l11ll111_opy_() == bstack111l111_opy_ (u"ࠥࡸࡷࡻࡥࠣୀ"):
    bstack11l111l1_opy_ = os.path.relpath(bstack11l11l11ll_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack11l111l1_opy_)
    bstack11llll1lll_opy_ = suite_name + bstack111l111_opy_ (u"ࠦ࠲ࠨୁ") + test_name
    threading.current_thread().percySessionName = bstack11llll1lll_opy_
def bstack1ll11l11_opy_(self, test, *args, **kwargs):
  global bstack1l1l11lll1_opy_
  test_name = None
  bstack11l11l11ll_opy_ = None
  if test:
    test_name = str(test.name)
    bstack11l11l11ll_opy_ = str(test.source)
  bstack1ll11lll11_opy_(test_name, bstack11l11l11ll_opy_)
  bstack1l1l11lll1_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.bstack11l1l11ll_opy_, stage=STAGE.bstack11l1llll1_opy_, bstack11llll1lll_opy_=bstack1ll1l11l1l_opy_)
def bstack111l1111l_opy_(driver, bstack11llll1lll_opy_):
  if not bstack1l111l1l_opy_ and bstack11llll1lll_opy_:
      bstack11ll111l11_opy_ = {
          bstack111l111_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬୂ"): bstack111l111_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧୃ"),
          bstack111l111_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪୄ"): {
              bstack111l111_opy_ (u"ࠨࡰࡤࡱࡪ࠭୅"): bstack11llll1lll_opy_
          }
      }
      bstack111lllllll_opy_ = bstack111l111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧ୆").format(json.dumps(bstack11ll111l11_opy_))
      driver.execute_script(bstack111lllllll_opy_)
  if bstack111lll11_opy_:
      bstack1ll11ll1ll_opy_ = {
          bstack111l111_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪେ"): bstack111l111_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭ୈ"),
          bstack111l111_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ୉"): {
              bstack111l111_opy_ (u"࠭ࡤࡢࡶࡤࠫ୊"): bstack11llll1lll_opy_ + bstack111l111_opy_ (u"ࠧࠡࡲࡤࡷࡸ࡫ࡤࠢࠩୋ"),
              bstack111l111_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧୌ"): bstack111l111_opy_ (u"ࠩ࡬ࡲ࡫ࡵ୍ࠧ")
          }
      }
      if bstack111lll11_opy_.status == bstack111l111_opy_ (u"ࠪࡔࡆ࡙ࡓࠨ୎"):
          bstack1llll111l1_opy_ = bstack111l111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩ୏").format(json.dumps(bstack1ll11ll1ll_opy_))
          driver.execute_script(bstack1llll111l1_opy_)
          bstack1l11ll11ll_opy_(driver, bstack111l111_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ୐"))
      elif bstack111lll11_opy_.status == bstack111l111_opy_ (u"࠭ࡆࡂࡋࡏࠫ୑"):
          reason = bstack111l111_opy_ (u"ࠢࠣ୒")
          bstack11lll1111l_opy_ = bstack11llll1lll_opy_ + bstack111l111_opy_ (u"ࠨࠢࡩࡥ࡮ࡲࡥࡥࠩ୓")
          if bstack111lll11_opy_.message:
              reason = str(bstack111lll11_opy_.message)
              bstack11lll1111l_opy_ = bstack11lll1111l_opy_ + bstack111l111_opy_ (u"ࠩࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸ࠺ࠡࠩ୔") + reason
          bstack1ll11ll1ll_opy_[bstack111l111_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭୕")] = {
              bstack111l111_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪୖ"): bstack111l111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫୗ"),
              bstack111l111_opy_ (u"࠭ࡤࡢࡶࡤࠫ୘"): bstack11lll1111l_opy_
          }
          bstack1llll111l1_opy_ = bstack111l111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬ୙").format(json.dumps(bstack1ll11ll1ll_opy_))
          driver.execute_script(bstack1llll111l1_opy_)
          bstack1l11ll11ll_opy_(driver, bstack111l111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ୚"), reason)
          bstack11l111l1l_opy_(reason, str(bstack111lll11_opy_), str(bstack1l11lllll_opy_), logger)
@measure(event_name=EVENTS.bstack11ll1111l_opy_, stage=STAGE.bstack11l1llll1_opy_, bstack11llll1lll_opy_=bstack1ll1l11l1l_opy_)
def bstack1111l111l_opy_(driver, test):
  if percy.bstack1l11ll111_opy_() == bstack111l111_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ୛") and percy.bstack1l111llll1_opy_() == bstack111l111_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧଡ଼"):
      bstack11ll11111l_opy_ = bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧଢ଼"), None)
      bstack11l11111_opy_(driver, bstack11ll11111l_opy_, test)
  if (bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ୞"), None) and
      bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬୟ"), None)) or (
      bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧୠ"), None) and
      bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪୡ"), None)):
      logger.info(bstack111l111_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠠࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡵࡻࡦࡿ࠮ࠡࠤୢ"))
      bstack1l1ll11l1l_opy_.bstack1llllll11_opy_(driver, name=test.name, path=test.source)
def bstack1ll1lllll_opy_(test, bstack11llll1lll_opy_):
    try:
      bstack1l1111lll_opy_ = datetime.datetime.now()
      data = {}
      if test:
        data[bstack111l111_opy_ (u"ࠪࡲࡦࡳࡥࠨୣ")] = bstack11llll1lll_opy_
      if bstack111lll11_opy_:
        if bstack111lll11_opy_.status == bstack111l111_opy_ (u"ࠫࡕࡇࡓࡔࠩ୤"):
          data[bstack111l111_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ୥")] = bstack111l111_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭୦")
        elif bstack111lll11_opy_.status == bstack111l111_opy_ (u"ࠧࡇࡃࡌࡐࠬ୧"):
          data[bstack111l111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ୨")] = bstack111l111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ୩")
          if bstack111lll11_opy_.message:
            data[bstack111l111_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪ୪")] = str(bstack111lll11_opy_.message)
      user = CONFIG[bstack111l111_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭୫")]
      key = CONFIG[bstack111l111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ୬")]
      host = bstack1l1ll11l1_opy_(cli.config, [bstack111l111_opy_ (u"ࠨࡡࡱ࡫ࡶࠦ୭"), bstack111l111_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡦࠤ୮"), bstack111l111_opy_ (u"ࠣࡣࡳ࡭ࠧ୯")], bstack111l111_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡵ࡯࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠥ୰"))
      url = bstack111l111_opy_ (u"ࠪࡿࢂ࠵ࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡵࡨࡷࡸ࡯࡯࡯ࡵ࠲ࡿࢂ࠴ࡪࡴࡱࡱࠫୱ").format(host, bstack11l11ll11l_opy_)
      headers = {
        bstack111l111_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪ୲"): bstack111l111_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ୳"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers, auth=(user, key))
        cli.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠨࡨࡵࡶࡳ࠾ࡺࡶࡤࡢࡶࡨࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡷࡹࡧࡴࡶࡵࠥ୴"), datetime.datetime.now() - bstack1l1111lll_opy_)
    except Exception as e:
      logger.error(bstack1ll1ll1l11_opy_.format(str(e)))
def bstack11ll1l11ll_opy_(test, bstack11llll1lll_opy_):
  global CONFIG
  global bstack11l1ll1l11_opy_
  global bstack1ll1ll111l_opy_
  global bstack11l11ll11l_opy_
  global bstack111lll11_opy_
  global bstack1ll1l11l1l_opy_
  global bstack1l1l1l1l11_opy_
  global bstack11l11lll11_opy_
  global bstack11ll1ll11_opy_
  global bstack11ll1lll1l_opy_
  global bstack11ll1lllll_opy_
  global bstack1llll1l111_opy_
  global bstack1llll11lll_opy_
  try:
    if not bstack11l11ll11l_opy_:
      with bstack1llll11lll_opy_:
        bstack1llll111_opy_ = os.path.join(os.path.expanduser(bstack111l111_opy_ (u"ࠧࡿࠩ୵")), bstack111l111_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ୶"), bstack111l111_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫ୷"))
        if os.path.exists(bstack1llll111_opy_):
          with open(bstack1llll111_opy_, bstack111l111_opy_ (u"ࠪࡶࠬ୸")) as f:
            content = f.read().strip()
            if content:
              bstack11l11llll1_opy_ = json.loads(bstack111l111_opy_ (u"ࠦࢀࠨ୹") + content + bstack111l111_opy_ (u"ࠬࠨࡸࠣ࠼ࠣࠦࡾࠨࠧ୺") + bstack111l111_opy_ (u"ࠨࡽࠣ୻"))
              bstack11l11ll11l_opy_ = bstack11l11llll1_opy_.get(str(threading.get_ident()))
  except Exception as e:
    logger.debug(bstack111l111_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡲࡦࡣࡧ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡋࡇࡷࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬ୼") + str(e))
  if bstack11ll1lllll_opy_:
    with bstack11lllllll_opy_:
      bstack1lll1ll111_opy_ = bstack11ll1lllll_opy_.copy()
    for driver in bstack1lll1ll111_opy_:
      if bstack11l11ll11l_opy_ == driver.session_id:
        if test:
          bstack1111l111l_opy_(driver, test)
        bstack111l1111l_opy_(driver, bstack11llll1lll_opy_)
  elif bstack11l11ll11l_opy_:
    bstack1ll1lllll_opy_(test, bstack11llll1lll_opy_)
  if bstack11l1ll1l11_opy_:
    bstack11l11lll11_opy_(bstack11l1ll1l11_opy_)
  if bstack1ll1ll111l_opy_:
    bstack11ll1ll11_opy_(bstack1ll1ll111l_opy_)
  if bstack1l11l1lll1_opy_:
    bstack11ll1lll1l_opy_()
def bstack1ll1l1l1ll_opy_(self, test, *args, **kwargs):
  bstack11llll1lll_opy_ = None
  if test:
    bstack11llll1lll_opy_ = str(test.name)
  bstack11ll1l11ll_opy_(test, bstack11llll1lll_opy_)
  bstack1l1l1l1l11_opy_(self, test, *args, **kwargs)
def bstack11l1ll111l_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack11l1ll111_opy_
  global CONFIG
  global bstack11ll1lllll_opy_
  global bstack11l11ll11l_opy_
  global bstack1llll11lll_opy_
  bstack11lll11l1l_opy_ = None
  try:
    if bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ୽"), None) or bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ୾"), None):
      try:
        if not bstack11l11ll11l_opy_:
          bstack1llll111_opy_ = os.path.join(os.path.expanduser(bstack111l111_opy_ (u"ࠪࢂࠬ୿")), bstack111l111_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ஀"), bstack111l111_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧ஁"))
          with bstack1llll11lll_opy_:
            if os.path.exists(bstack1llll111_opy_):
              with open(bstack1llll111_opy_, bstack111l111_opy_ (u"࠭ࡲࠨஂ")) as f:
                content = f.read().strip()
                if content:
                  bstack11l11llll1_opy_ = json.loads(bstack111l111_opy_ (u"ࠢࡼࠤஃ") + content + bstack111l111_opy_ (u"ࠨࠤࡻࠦ࠿ࠦࠢࡺࠤࠪ஄") + bstack111l111_opy_ (u"ࠤࢀࠦஅ"))
                  bstack11l11ll11l_opy_ = bstack11l11llll1_opy_.get(str(threading.get_ident()))
      except Exception as e:
        logger.debug(bstack111l111_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡵࡩࡦࡪࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡎࡊࡳࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢࡷࡩࡸࡺࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࠩஆ") + str(e))
      if bstack11ll1lllll_opy_:
        with bstack11lllllll_opy_:
          bstack1lll1ll111_opy_ = bstack11ll1lllll_opy_.copy()
        for driver in bstack1lll1ll111_opy_:
          if bstack11l11ll11l_opy_ == driver.session_id:
            bstack11lll11l1l_opy_ = driver
    bstack1ll1ll11l_opy_ = bstack1l1ll11l1l_opy_.bstack11ll111lll_opy_(test.tags)
    if bstack11lll11l1l_opy_:
      threading.current_thread().isA11yTest = bstack1l1ll11l1l_opy_.bstack111l11l1_opy_(bstack11lll11l1l_opy_, bstack1ll1ll11l_opy_)
      threading.current_thread().isAppA11yTest = bstack1l1ll11l1l_opy_.bstack111l11l1_opy_(bstack11lll11l1l_opy_, bstack1ll1ll11l_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1ll1ll11l_opy_
      threading.current_thread().isAppA11yTest = bstack1ll1ll11l_opy_
  except:
    pass
  bstack11l1ll111_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack111lll11_opy_
  try:
    bstack111lll11_opy_ = self._test
  except:
    bstack111lll11_opy_ = self.test
def bstack11llllll1l_opy_():
  global bstack1l111111ll_opy_
  try:
    if os.path.exists(bstack1l111111ll_opy_):
      os.remove(bstack1l111111ll_opy_)
  except Exception as e:
    logger.debug(bstack111l111_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧஇ") + str(e))
def bstack1llll1l1ll_opy_():
  global bstack1l111111ll_opy_
  bstack1lllll1ll1_opy_ = {}
  lock_file = bstack1l111111ll_opy_ + bstack111l111_opy_ (u"ࠬ࠴࡬ࡰࡥ࡮ࠫஈ")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack111l111_opy_ (u"࠭ࡦࡪ࡮ࡨࡰࡴࡩ࡫ࠡࡰࡲࡸࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥ࠭ࠢࡸࡷ࡮ࡴࡧࠡࡤࡤࡷ࡮ࡩࠠࡧ࡫࡯ࡩࠥࡵࡰࡦࡴࡤࡸ࡮ࡵ࡮ࡴࠩஉ"))
    try:
      if not os.path.isfile(bstack1l111111ll_opy_):
        with open(bstack1l111111ll_opy_, bstack111l111_opy_ (u"ࠧࡸࠩஊ")) as f:
          json.dump({}, f)
      if os.path.exists(bstack1l111111ll_opy_):
        with open(bstack1l111111ll_opy_, bstack111l111_opy_ (u"ࠨࡴࠪ஋")) as f:
          content = f.read().strip()
          if content:
            bstack1lllll1ll1_opy_ = json.loads(content)
    except Exception as e:
      logger.debug(bstack111l111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡷ࡫ࡡࡥ࡫ࡱ࡫ࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫ஌") + str(e))
    return bstack1lllll1ll1_opy_
  try:
    os.makedirs(os.path.dirname(bstack1l111111ll_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      if not os.path.isfile(bstack1l111111ll_opy_):
        with open(bstack1l111111ll_opy_, bstack111l111_opy_ (u"ࠪࡻࠬ஍")) as f:
          json.dump({}, f)
      if os.path.exists(bstack1l111111ll_opy_):
        with open(bstack1l111111ll_opy_, bstack111l111_opy_ (u"ࠫࡷ࠭எ")) as f:
          content = f.read().strip()
          if content:
            bstack1lllll1ll1_opy_ = json.loads(content)
  except Exception as e:
    logger.debug(bstack111l111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡳࡧࡤࡨ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧஏ") + str(e))
  finally:
    return bstack1lllll1ll1_opy_
def bstack111lllll1l_opy_(platform_index, item_index):
  global bstack1l111111ll_opy_
  lock_file = bstack1l111111ll_opy_ + bstack111l111_opy_ (u"࠭࠮࡭ࡱࡦ࡯ࠬஐ")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack111l111_opy_ (u"ࠧࡧ࡫࡯ࡩࡱࡵࡣ࡬ࠢࡱࡳࡹࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦ࠮ࠣࡹࡸ࡯࡮ࡨࠢࡥࡥࡸ࡯ࡣࠡࡨ࡬ࡰࡪࠦ࡯ࡱࡧࡵࡥࡹ࡯࡯࡯ࡵࠪ஑"))
    try:
      bstack1lllll1ll1_opy_ = {}
      if os.path.exists(bstack1l111111ll_opy_):
        with open(bstack1l111111ll_opy_, bstack111l111_opy_ (u"ࠨࡴࠪஒ")) as f:
          content = f.read().strip()
          if content:
            bstack1lllll1ll1_opy_ = json.loads(content)
      bstack1lllll1ll1_opy_[item_index] = platform_index
      with open(bstack1l111111ll_opy_, bstack111l111_opy_ (u"ࠤࡺࠦஓ")) as outfile:
        json.dump(bstack1lllll1ll1_opy_, outfile)
    except Exception as e:
      logger.debug(bstack111l111_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡽࡲࡪࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨஔ") + str(e))
    return
  try:
    os.makedirs(os.path.dirname(bstack1l111111ll_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      bstack1lllll1ll1_opy_ = {}
      if os.path.exists(bstack1l111111ll_opy_):
        with open(bstack1l111111ll_opy_, bstack111l111_opy_ (u"ࠫࡷ࠭க")) as f:
          content = f.read().strip()
          if content:
            bstack1lllll1ll1_opy_ = json.loads(content)
      bstack1lllll1ll1_opy_[item_index] = platform_index
      with open(bstack1l111111ll_opy_, bstack111l111_opy_ (u"ࠧࡽࠢ஖")) as outfile:
        json.dump(bstack1lllll1ll1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack111l111_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡹࡵ࡭ࡹ࡯࡮ࡨࠢࡷࡳࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫ஗") + str(e))
def bstack1ll11l1ll1_opy_(bstack11l11lll_opy_):
  global CONFIG
  bstack1l1llll11_opy_ = bstack111l111_opy_ (u"ࠧࠨ஘")
  if not bstack111l111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫங") in CONFIG:
    logger.info(bstack111l111_opy_ (u"ࠩࡑࡳࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠡࡲࡤࡷࡸ࡫ࡤࠡࡷࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࠦࡲࡦࡲࡲࡶࡹࠦࡦࡰࡴࠣࡖࡴࡨ࡯ࡵࠢࡵࡹࡳ࠭ச"))
  try:
    platform = CONFIG[bstack111l111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭஛")][bstack11l11lll_opy_]
    if bstack111l111_opy_ (u"ࠫࡴࡹࠧஜ") in platform:
      bstack1l1llll11_opy_ += str(platform[bstack111l111_opy_ (u"ࠬࡵࡳࠨ஝")]) + bstack111l111_opy_ (u"࠭ࠬࠡࠩஞ")
    if bstack111l111_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪட") in platform:
      bstack1l1llll11_opy_ += str(platform[bstack111l111_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫ஠")]) + bstack111l111_opy_ (u"ࠩ࠯ࠤࠬ஡")
    if bstack111l111_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧ஢") in platform:
      bstack1l1llll11_opy_ += str(platform[bstack111l111_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨண")]) + bstack111l111_opy_ (u"ࠬ࠲ࠠࠨத")
    if bstack111l111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ஥") in platform:
      bstack1l1llll11_opy_ += str(platform[bstack111l111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ஦")]) + bstack111l111_opy_ (u"ࠨ࠮ࠣࠫ஧")
    if bstack111l111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧந") in platform:
      bstack1l1llll11_opy_ += str(platform[bstack111l111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨன")]) + bstack111l111_opy_ (u"ࠫ࠱ࠦࠧப")
    if bstack111l111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭஫") in platform:
      bstack1l1llll11_opy_ += str(platform[bstack111l111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ஬")]) + bstack111l111_opy_ (u"ࠧ࠭ࠢࠪ஭")
  except Exception as e:
    logger.debug(bstack111l111_opy_ (u"ࠨࡕࡲࡱࡪࠦࡥࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡱ࡫ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡴࡶࡵ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡷ࡫ࡰࡰࡴࡷࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡵ࡮ࠨம") + str(e))
  finally:
    if bstack1l1llll11_opy_[len(bstack1l1llll11_opy_) - 2:] == bstack111l111_opy_ (u"ࠩ࠯ࠤࠬய"):
      bstack1l1llll11_opy_ = bstack1l1llll11_opy_[:-2]
    return bstack1l1llll11_opy_
def bstack1l11lll1_opy_(path, bstack1l1llll11_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1l1llllll_opy_ = ET.parse(path)
    bstack11ll111ll_opy_ = bstack1l1llllll_opy_.getroot()
    bstack1l1111l1l_opy_ = None
    for suite in bstack11ll111ll_opy_.iter(bstack111l111_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩர")):
      if bstack111l111_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫற") in suite.attrib:
        suite.attrib[bstack111l111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪல")] += bstack111l111_opy_ (u"࠭ࠠࠨள") + bstack1l1llll11_opy_
        bstack1l1111l1l_opy_ = suite
    bstack11l111l11_opy_ = None
    for robot in bstack11ll111ll_opy_.iter(bstack111l111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ழ")):
      bstack11l111l11_opy_ = robot
    bstack1l11ll11_opy_ = len(bstack11l111l11_opy_.findall(bstack111l111_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧவ")))
    if bstack1l11ll11_opy_ == 1:
      bstack11l111l11_opy_.remove(bstack11l111l11_opy_.findall(bstack111l111_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨஶ"))[0])
      bstack1l11l1l11l_opy_ = ET.Element(bstack111l111_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩஷ"), attrib={bstack111l111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩஸ"): bstack111l111_opy_ (u"࡙ࠬࡵࡪࡶࡨࡷࠬஹ"), bstack111l111_opy_ (u"࠭ࡩࡥࠩ஺"): bstack111l111_opy_ (u"ࠧࡴ࠲ࠪ஻")})
      bstack11l111l11_opy_.insert(1, bstack1l11l1l11l_opy_)
      bstack11ll111l_opy_ = None
      for suite in bstack11l111l11_opy_.iter(bstack111l111_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧ஼")):
        bstack11ll111l_opy_ = suite
      bstack11ll111l_opy_.append(bstack1l1111l1l_opy_)
      bstack1lll1l11ll_opy_ = None
      for status in bstack1l1111l1l_opy_.iter(bstack111l111_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ஽")):
        bstack1lll1l11ll_opy_ = status
      bstack11ll111l_opy_.append(bstack1lll1l11ll_opy_)
    bstack1l1llllll_opy_.write(path)
  except Exception as e:
    logger.debug(bstack111l111_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡳࡵ࡬ࡲ࡬ࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠨா") + str(e))
def bstack11l11ll1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1l1ll1lll_opy_
  global CONFIG
  if bstack111l111_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡴࡦࡺࡨࠣி") in options:
    del options[bstack111l111_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡵࡧࡴࡩࠤீ")]
  bstack11lll111_opy_ = bstack1llll1l1ll_opy_()
  for bstack11l111ll11_opy_ in bstack11lll111_opy_.keys():
    path = os.path.join(os.getcwd(), bstack111l111_opy_ (u"࠭ࡰࡢࡤࡲࡸࡤࡸࡥࡴࡷ࡯ࡸࡸ࠭ு"), str(bstack11l111ll11_opy_), bstack111l111_opy_ (u"ࠧࡰࡷࡷࡴࡺࡺ࠮ࡹ࡯࡯ࠫூ"))
    bstack1l11lll1_opy_(path, bstack1ll11l1ll1_opy_(bstack11lll111_opy_[bstack11l111ll11_opy_]))
  bstack11llllll1l_opy_()
  return bstack1l1ll1lll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1llll11l_opy_(self, ff_profile_dir):
  global bstack1ll111111_opy_
  if not ff_profile_dir:
    return None
  return bstack1ll111111_opy_(self, ff_profile_dir)
def bstack1l1lllll1l_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1l11ll1ll1_opy_
  bstack1l111lll1l_opy_ = []
  if bstack111l111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ௃") in CONFIG:
    bstack1l111lll1l_opy_ = CONFIG[bstack111l111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ௄")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack111l111_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࠦ௅")],
      pabot_args[bstack111l111_opy_ (u"ࠦࡻ࡫ࡲࡣࡱࡶࡩࠧெ")],
      argfile,
      pabot_args.get(bstack111l111_opy_ (u"ࠧ࡮ࡩࡷࡧࠥே")),
      pabot_args[bstack111l111_opy_ (u"ࠨࡰࡳࡱࡦࡩࡸࡹࡥࡴࠤை")],
      platform[0],
      bstack1l11ll1ll1_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack111l111_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡨ࡬ࡰࡪࡹࠢ௉")] or [(bstack111l111_opy_ (u"ࠣࠤொ"), None)]
    for platform in enumerate(bstack1l111lll1l_opy_)
  ]
def bstack11l1l1llll_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1ll1lll1l_opy_=bstack111l111_opy_ (u"ࠩࠪோ")):
  global bstack1l1lll11ll_opy_
  self.platform_index = platform_index
  self.bstack1l111lll_opy_ = bstack1ll1lll1l_opy_
  bstack1l1lll11ll_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1l1l1l1l1l_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1l1llll1ll_opy_
  global bstack1lll1l1ll1_opy_
  bstack1l1l11l11_opy_ = copy.deepcopy(item)
  if not bstack111l111_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬௌ") in item.options:
    bstack1l1l11l11_opy_.options[bstack111l111_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ்࠭")] = []
  bstack1ll1lll1l1_opy_ = bstack1l1l11l11_opy_.options[bstack111l111_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ௎")].copy()
  for v in bstack1l1l11l11_opy_.options[bstack111l111_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨ௏")]:
    if bstack111l111_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝࠭ௐ") in v:
      bstack1ll1lll1l1_opy_.remove(v)
    if bstack111l111_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓࠨ௑") in v:
      bstack1ll1lll1l1_opy_.remove(v)
    if bstack111l111_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡆࡈࡊࡑࡕࡃࡂࡎࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭௒") in v:
      bstack1ll1lll1l1_opy_.remove(v)
  bstack1ll1lll1l1_opy_.insert(0, bstack111l111_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡓࡐࡆ࡚ࡆࡐࡔࡐࡍࡓࡊࡅ࡙࠼ࡾࢁࠬ௓").format(bstack1l1l11l11_opy_.platform_index))
  bstack1ll1lll1l1_opy_.insert(0, bstack111l111_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒ࠻ࡽࢀࠫ௔").format(bstack1l1l11l11_opy_.bstack1l111lll_opy_))
  bstack1l1l11l11_opy_.options[bstack111l111_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ௕")] = bstack1ll1lll1l1_opy_
  if bstack1lll1l1ll1_opy_:
    bstack1l1l11l11_opy_.options[bstack111l111_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨ௖")].insert(0, bstack111l111_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙࠺ࡼࡿࠪௗ").format(bstack1lll1l1ll1_opy_))
  return bstack1l1llll1ll_opy_(caller_id, datasources, is_last, bstack1l1l11l11_opy_, outs_dir)
def bstack1l1l1l1l_opy_(command, item_index):
  try:
    if bstack1ll1ll11_opy_.get_property(bstack111l111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩ௘")):
      os.environ[bstack111l111_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪ௙")] = json.dumps(CONFIG[bstack111l111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭௚")][item_index % bstack1l1l11l1l1_opy_])
    global bstack1lll1l1ll1_opy_
    if bstack1lll1l1ll1_opy_:
      command[0] = command[0].replace(bstack111l111_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ௛"), bstack111l111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡸࡪ࡫ࠡࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠢ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠡࠩ௜") + str(
        item_index) + bstack111l111_opy_ (u"࠭ࠠࠨ௝") + bstack1lll1l1ll1_opy_, 1)
    else:
      command[0] = command[0].replace(bstack111l111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭௞"),
                                      bstack111l111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡴࡦ࡮ࠤࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠥ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠤࠬ௟") + str(item_index), 1)
  except Exception as e:
    logger.error(bstack111l111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡯ࡲࡨ࡮࡬ࡹࡪࡰࡪࠤࡨࡵ࡭࡮ࡣࡱࡨࠥ࡬࡯ࡳࠢࡳࡥࡧࡵࡴࠡࡴࡸࡲ࠿ࠦࡻࡾࠩ௠").format(str(e)))
def bstack1l1ll1l111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1l1l11l1_opy_
  try:
    bstack1l1l1l1l_opy_(command, item_index)
    return bstack1l1l11l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
  except Exception as e:
    logger.error(bstack111l111_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡣࡱࡷࠤࡷࡻ࡮࠻ࠢࡾࢁࠬ௡").format(str(e)))
    raise e
def bstack11l1l1ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1l1l11l1_opy_
  try:
    bstack1l1l1l1l_opy_(command, item_index)
    return bstack1l1l11l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
  except Exception as e:
    logger.error(bstack111l111_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡢࡤࡲࡸࠥࡸࡵ࡯ࠢ࠵࠲࠶࠹࠺ࠡࡽࢀࠫ௢").format(str(e)))
    try:
      return bstack1l1l11l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
    except Exception as e2:
      logger.error(bstack111l111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡥࡳࡹࠦ࠲࠯࠳࠶ࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࡼࡿࠪ௣").format(str(e2)))
      raise e
def bstack11l1111l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1l1l11l1_opy_
  try:
    bstack1l1l1l1l_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    return bstack1l1l11l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
  except Exception as e:
    logger.error(bstack111l111_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠࡳࡷࡱࠤ࠷࠴࠱࠶࠼ࠣࡿࢂ࠭௤").format(str(e)))
    try:
      return bstack1l1l11l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
    except Exception as e2:
      logger.error(bstack111l111_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡧࡵࡴࠡ࠴࠱࠵࠺ࠦࡦࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢࡾࢁࠬ௥").format(str(e2)))
      raise e
def bstack1lllllllll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack1l1l11l1_opy_
  try:
    bstack1l1l1l1l_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    if sleep_before_start and sleep_before_start > 0:
      import time
      time.sleep(min(sleep_before_start, 5))
    return bstack1l1l11l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack111l111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡦࡨ࡯ࡵࠢࡵࡹࡳࠦ࠴࠯࠴࠽ࠤࢀࢃࠧ௦").format(str(e)))
    try:
      return bstack1l1l11l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack111l111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡢࡰࡶࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࡻࡾࠩ௧").format(str(e2)))
      raise e
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack11111111_opy_(self, runner, quiet=False, capture=True):
  global bstack11lll11ll1_opy_
  bstack1ll1l11l1_opy_ = bstack11lll11ll1_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack111l111_opy_ (u"ࠪࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࡥࡡࡳࡴࠪ௨")):
      runner.exception_arr = []
    if not hasattr(runner, bstack111l111_opy_ (u"ࠫࡪࡾࡣࡠࡶࡵࡥࡨ࡫ࡢࡢࡥ࡮ࡣࡦࡸࡲࠨ௩")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1ll1l11l1_opy_
def bstack1ll1l1l1_opy_(runner, hook_name, context, element, bstack11lllll1ll_opy_, *args):
  try:
    if runner.hooks.get(hook_name):
      bstack11l1ll1l1l_opy_.bstack1lll1l1l_opy_(hook_name, element)
    bstack11lllll1ll_opy_(runner, hook_name, context, *args)
    if runner.hooks.get(hook_name):
      bstack11l1ll1l1l_opy_.bstack1ll111lll1_opy_(element)
      if hook_name not in [bstack111l111_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠩ௪"), bstack111l111_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠩ௫")] and args and hasattr(args[0], bstack111l111_opy_ (u"ࠧࡦࡴࡵࡳࡷࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠧ௬")):
        args[0].error_message = bstack111l111_opy_ (u"ࠨࠩ௭")
  except Exception as e:
    logger.debug(bstack111l111_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡮ࡡ࡯ࡦ࡯ࡩࠥ࡮࡯ࡰ࡭ࡶࠤ࡮ࡴࠠࡣࡧ࡫ࡥࡻ࡫࠺ࠡࡽࢀࠫ௮").format(str(e)))
@measure(event_name=EVENTS.bstack11ll1l11l_opy_, stage=STAGE.bstack11l1llll1_opy_, hook_type=bstack111l111_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡄࡰࡱࠨ௯"), bstack11llll1lll_opy_=bstack1ll1l11l1l_opy_)
def bstack11l1lllll1_opy_(runner, name, context, bstack11lllll1ll_opy_, *args):
    if runner.hooks.get(bstack111l111_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣ௰")).__name__ != bstack111l111_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࡡࡧࡩ࡫ࡧࡵ࡭ࡶࡢ࡬ࡴࡵ࡫ࠣ௱"):
      bstack1ll1l1l1_opy_(runner, name, context, runner, bstack11lllll1ll_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack1111ll1l_opy_(bstack111l111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ௲")) else context.browser
      runner.driver_initialised = bstack111l111_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦ௳")
    except Exception as e:
      logger.debug(bstack111l111_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡦࡵ࡭ࡻ࡫ࡲࠡ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡶࡩࠥࡧࡴࡵࡴ࡬ࡦࡺࡺࡥ࠻ࠢࡾࢁࠬ௴").format(str(e)))
def bstack1ll1ll11ll_opy_(runner, name, context, bstack11lllll1ll_opy_, *args):
    bstack1ll1l1l1_opy_(runner, name, context, context.feature, bstack11lllll1ll_opy_, *args)
    try:
      if not bstack1l111l1l_opy_:
        bstack11lll11l1l_opy_ = threading.current_thread().bstackSessionDriver if bstack1111ll1l_opy_(bstack111l111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ௵")) else context.browser
        if is_driver_active(bstack11lll11l1l_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack111l111_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦ௶")
          bstack11l1l11lll_opy_ = str(runner.feature.name)
          bstack1llll11ll_opy_(context, bstack11l1l11lll_opy_)
          bstack11lll11l1l_opy_.execute_script(bstack111l111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩ௷") + json.dumps(bstack11l1l11lll_opy_) + bstack111l111_opy_ (u"ࠬࢃࡽࠨ௸"))
    except Exception as e:
      logger.debug(bstack111l111_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭௹").format(str(e)))
def bstack1llll1ll1_opy_(runner, name, context, bstack11lllll1ll_opy_, *args):
    if hasattr(context, bstack111l111_opy_ (u"ࠧࡴࡥࡨࡲࡦࡸࡩࡰࠩ௺")):
        bstack11l1ll1l1l_opy_.start_test(context)
    target = context.scenario if hasattr(context, bstack111l111_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪ௻")) else context.feature
    bstack1ll1l1l1_opy_(runner, name, context, target, bstack11lllll1ll_opy_, *args)
@measure(event_name=EVENTS.bstack1l1lll11l1_opy_, stage=STAGE.bstack11l1llll1_opy_, bstack11llll1lll_opy_=bstack1ll1l11l1l_opy_)
def bstack111lll1l1_opy_(runner, name, context, bstack11lllll1ll_opy_, *args):
    if len(context.scenario.tags) == 0: bstack11l1ll1l1l_opy_.start_test(context)
    bstack1ll1l1l1_opy_(runner, name, context, context.scenario, bstack11lllll1ll_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack1llll1ll_opy_.bstack1l1111l1_opy_(context, *args)
    try:
      bstack11lll11l1l_opy_ = bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ௼"), context.browser)
      if is_driver_active(bstack11lll11l1l_opy_):
        bstack1l1ll1l11_opy_.bstack1l11l1llll_opy_(bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ௽"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack111l111_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨ௾")
        if (not bstack1l111l1l_opy_):
          scenario_name = args[0].name
          feature_name = bstack11l1l11lll_opy_ = str(runner.feature.name)
          bstack11l1l11lll_opy_ = feature_name + bstack111l111_opy_ (u"ࠬࠦ࠭ࠡࠩ௿") + scenario_name
          if runner.driver_initialised == bstack111l111_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣఀ"):
            bstack1llll11ll_opy_(context, bstack11l1l11lll_opy_)
            bstack11lll11l1l_opy_.execute_script(bstack111l111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬఁ") + json.dumps(bstack11l1l11lll_opy_) + bstack111l111_opy_ (u"ࠨࡿࢀࠫం"))
    except Exception as e:
      logger.debug(bstack111l111_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡ࡫ࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡀࠠࡼࡿࠪః").format(str(e)))
@measure(event_name=EVENTS.bstack11ll1l11l_opy_, stage=STAGE.bstack11l1llll1_opy_, hook_type=bstack111l111_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡖࡸࡪࡶࠢఄ"), bstack11llll1lll_opy_=bstack1ll1l11l1l_opy_)
def bstack111lllll1_opy_(runner, name, context, bstack11lllll1ll_opy_, *args):
    bstack1ll1l1l1_opy_(runner, name, context, args[0], bstack11lllll1ll_opy_, *args)
    try:
      bstack11lll11l1l_opy_ = threading.current_thread().bstackSessionDriver if bstack1111ll1l_opy_(bstack111l111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪఅ")) else context.browser
      if is_driver_active(bstack11lll11l1l_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack111l111_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥఆ")
        bstack11l1ll1l1l_opy_.bstack1l1l1l11l1_opy_(args[0])
        if runner.driver_initialised == bstack111l111_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦఇ"):
          feature_name = bstack11l1l11lll_opy_ = str(runner.feature.name)
          bstack11l1l11lll_opy_ = feature_name + bstack111l111_opy_ (u"ࠧࠡ࠯ࠣࠫఈ") + context.scenario.name
          bstack11lll11l1l_opy_.execute_script(bstack111l111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭ఉ") + json.dumps(bstack11l1l11lll_opy_) + bstack111l111_opy_ (u"ࠩࢀࢁࠬఊ"))
    except Exception as e:
      logger.debug(bstack111l111_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡴࡦࡲ࠽ࠤࢀࢃࠧఋ").format(str(e)))
@measure(event_name=EVENTS.bstack11ll1l11l_opy_, stage=STAGE.bstack11l1llll1_opy_, hook_type=bstack111l111_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࡖࡸࡪࡶࠢఌ"), bstack11llll1lll_opy_=bstack1ll1l11l1l_opy_)
def bstack1l1ll11l11_opy_(runner, name, context, bstack11lllll1ll_opy_, *args):
  bstack11l1ll1l1l_opy_.bstack1l1l1111_opy_(args[0])
  try:
    bstack1lll111lll_opy_ = args[0].status.name
    bstack11lll11l1l_opy_ = threading.current_thread().bstackSessionDriver if bstack111l111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ఍") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack11lll11l1l_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack111l111_opy_ (u"࠭ࡩ࡯ࡵࡷࡩࡵ࠭ఎ")
        feature_name = bstack11l1l11lll_opy_ = str(runner.feature.name)
        bstack11l1l11lll_opy_ = feature_name + bstack111l111_opy_ (u"ࠧࠡ࠯ࠣࠫఏ") + context.scenario.name
        bstack11lll11l1l_opy_.execute_script(bstack111l111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭ఐ") + json.dumps(bstack11l1l11lll_opy_) + bstack111l111_opy_ (u"ࠩࢀࢁࠬ఑"))
    if str(bstack1lll111lll_opy_).lower() == bstack111l111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪఒ"):
      bstack1lll1llll_opy_ = bstack111l111_opy_ (u"ࠫࠬఓ")
      bstack1lll1ll1l_opy_ = bstack111l111_opy_ (u"ࠬ࠭ఔ")
      bstack1ll1l1l11l_opy_ = bstack111l111_opy_ (u"࠭ࠧక")
      try:
        import traceback
        bstack1lll1llll_opy_ = runner.exception.__class__.__name__
        bstack1l11l1lll_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1lll1ll1l_opy_ = bstack111l111_opy_ (u"ࠧࠡࠩఖ").join(bstack1l11l1lll_opy_)
        bstack1ll1l1l11l_opy_ = bstack1l11l1lll_opy_[-1]
      except Exception as e:
        logger.debug(bstack1l1l11ll1l_opy_.format(str(e)))
      bstack1lll1llll_opy_ += bstack1ll1l1l11l_opy_
      bstack1ll1llllll_opy_(context, json.dumps(str(args[0].name) + bstack111l111_opy_ (u"ࠣࠢ࠰ࠤࡋࡧࡩ࡭ࡧࡧࠥࡡࡴࠢగ") + str(bstack1lll1ll1l_opy_)),
                          bstack111l111_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣఘ"))
      if runner.driver_initialised == bstack111l111_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣఙ"):
        bstack1lllllll1_opy_(getattr(context, bstack111l111_opy_ (u"ࠫࡵࡧࡧࡦࠩచ"), None), bstack111l111_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧఛ"), bstack1lll1llll_opy_)
        bstack11lll11l1l_opy_.execute_script(bstack111l111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫజ") + json.dumps(str(args[0].name) + bstack111l111_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨఝ") + str(bstack1lll1ll1l_opy_)) + bstack111l111_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨఞ"))
      if runner.driver_initialised == bstack111l111_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢట"):
        bstack1l11ll11ll_opy_(bstack11lll11l1l_opy_, bstack111l111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪఠ"), bstack111l111_opy_ (u"ࠦࡘࡩࡥ࡯ࡣࡵ࡭ࡴࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࡢ࡮ࠣడ") + str(bstack1lll1llll_opy_))
    else:
      bstack1ll1llllll_opy_(context, bstack111l111_opy_ (u"ࠧࡖࡡࡴࡵࡨࡨࠦࠨఢ"), bstack111l111_opy_ (u"ࠨࡩ࡯ࡨࡲࠦణ"))
      if runner.driver_initialised == bstack111l111_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧత"):
        bstack1lllllll1_opy_(getattr(context, bstack111l111_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭థ"), None), bstack111l111_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤద"))
      bstack11lll11l1l_opy_.execute_script(bstack111l111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨధ") + json.dumps(str(args[0].name) + bstack111l111_opy_ (u"ࠦࠥ࠳ࠠࡑࡣࡶࡷࡪࡪࠡࠣన")) + bstack111l111_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫ఩"))
      if runner.driver_initialised == bstack111l111_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦప"):
        bstack1l11ll11ll_opy_(bstack11lll11l1l_opy_, bstack111l111_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢఫ"))
  except Exception as e:
    logger.debug(bstack111l111_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࠥࡹࡴࡦࡲ࠽ࠤࢀࢃࠧబ").format(str(e)))
  bstack1ll1l1l1_opy_(runner, name, context, args[0], bstack11lllll1ll_opy_, *args)
@measure(event_name=EVENTS.bstack1l1l111ll_opy_, stage=STAGE.bstack11l1llll1_opy_, bstack11llll1lll_opy_=bstack1ll1l11l1l_opy_)
def bstack1ll11111l1_opy_(runner, name, context, bstack11lllll1ll_opy_, *args):
  bstack11l1ll1l1l_opy_.end_test(args[0])
  try:
    bstack1l1ll11ll1_opy_ = args[0].status.name
    bstack11lll11l1l_opy_ = bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨభ"), context.browser)
    bstack1llll1ll_opy_.bstack111ll1ll1_opy_(bstack11lll11l1l_opy_)
    if str(bstack1l1ll11ll1_opy_).lower() == bstack111l111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪమ"):
      bstack1lll1llll_opy_ = bstack111l111_opy_ (u"ࠫࠬయ")
      bstack1lll1ll1l_opy_ = bstack111l111_opy_ (u"ࠬ࠭ర")
      bstack1ll1l1l11l_opy_ = bstack111l111_opy_ (u"࠭ࠧఱ")
      try:
        import traceback
        bstack1lll1llll_opy_ = runner.exception.__class__.__name__
        bstack1l11l1lll_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1lll1ll1l_opy_ = bstack111l111_opy_ (u"ࠧࠡࠩల").join(bstack1l11l1lll_opy_)
        bstack1ll1l1l11l_opy_ = bstack1l11l1lll_opy_[-1]
      except Exception as e:
        logger.debug(bstack1l1l11ll1l_opy_.format(str(e)))
      bstack1lll1llll_opy_ += bstack1ll1l1l11l_opy_
      bstack1ll1llllll_opy_(context, json.dumps(str(args[0].name) + bstack111l111_opy_ (u"ࠣࠢ࠰ࠤࡋࡧࡩ࡭ࡧࡧࠥࡡࡴࠢళ") + str(bstack1lll1ll1l_opy_)),
                          bstack111l111_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣఴ"))
      if runner.driver_initialised == bstack111l111_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧవ") or runner.driver_initialised == bstack111l111_opy_ (u"ࠫ࡮ࡴࡳࡵࡧࡳࠫశ"):
        bstack1lllllll1_opy_(getattr(context, bstack111l111_opy_ (u"ࠬࡶࡡࡨࡧࠪష"), None), bstack111l111_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨస"), bstack1lll1llll_opy_)
        bstack11lll11l1l_opy_.execute_script(bstack111l111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬహ") + json.dumps(str(args[0].name) + bstack111l111_opy_ (u"ࠣࠢ࠰ࠤࡋࡧࡩ࡭ࡧࡧࠥࡡࡴࠢ఺") + str(bstack1lll1ll1l_opy_)) + bstack111l111_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࡽࡾࠩ఻"))
      if runner.driver_initialised == bstack111l111_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳ఼ࠧ") or runner.driver_initialised == bstack111l111_opy_ (u"ࠫ࡮ࡴࡳࡵࡧࡳࠫఽ"):
        bstack1l11ll11ll_opy_(bstack11lll11l1l_opy_, bstack111l111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬా"), bstack111l111_opy_ (u"ࠨࡓࡤࡧࡱࡥࡷ࡯࡯ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥి") + str(bstack1lll1llll_opy_))
    else:
      bstack1ll1llllll_opy_(context, bstack111l111_opy_ (u"ࠢࡑࡣࡶࡷࡪࡪࠡࠣీ"), bstack111l111_opy_ (u"ࠣ࡫ࡱࡪࡴࠨు"))
      if runner.driver_initialised == bstack111l111_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦూ") or runner.driver_initialised == bstack111l111_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪృ"):
        bstack1lllllll1_opy_(getattr(context, bstack111l111_opy_ (u"ࠫࡵࡧࡧࡦࠩౄ"), None), bstack111l111_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ౅"))
      bstack11lll11l1l_opy_.execute_script(bstack111l111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫె") + json.dumps(str(args[0].name) + bstack111l111_opy_ (u"ࠢࠡ࠯ࠣࡔࡦࡹࡳࡦࡦࠤࠦే")) + bstack111l111_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦࢂࢃࠧై"))
      if runner.driver_initialised == bstack111l111_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦ౉") or runner.driver_initialised == bstack111l111_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪొ"):
        bstack1l11ll11ll_opy_(bstack11lll11l1l_opy_, bstack111l111_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦో"))
  except Exception as e:
    logger.debug(bstack111l111_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧౌ").format(str(e)))
  bstack1ll1l1l1_opy_(runner, name, context, context.scenario, bstack11lllll1ll_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack1l1l11lll_opy_(runner, name, context, bstack11lllll1ll_opy_, *args):
    target = context.scenario if hasattr(context, bstack111l111_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨ్")) else context.feature
    bstack1ll1l1l1_opy_(runner, name, context, target, bstack11lllll1ll_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack1ll1l11ll_opy_(runner, name, context, bstack11lllll1ll_opy_, *args):
    try:
      bstack11lll11l1l_opy_ = bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭౎"), context.browser)
      bstack1l1ll1l11l_opy_ = bstack111l111_opy_ (u"ࠨࠩ౏")
      if context.failed is True:
        bstack1l1lll1l_opy_ = []
        bstack11l111ll1l_opy_ = []
        bstack1lll11l1l1_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack1l1lll1l_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1l11l1lll_opy_ = traceback.format_tb(exc_tb)
            bstack111ll11l_opy_ = bstack111l111_opy_ (u"ࠩࠣࠫ౐").join(bstack1l11l1lll_opy_)
            bstack11l111ll1l_opy_.append(bstack111ll11l_opy_)
            bstack1lll11l1l1_opy_.append(bstack1l11l1lll_opy_[-1])
        except Exception as e:
          logger.debug(bstack1l1l11ll1l_opy_.format(str(e)))
        bstack1lll1llll_opy_ = bstack111l111_opy_ (u"ࠪࠫ౑")
        for i in range(len(bstack1l1lll1l_opy_)):
          bstack1lll1llll_opy_ += bstack1l1lll1l_opy_[i] + bstack1lll11l1l1_opy_[i] + bstack111l111_opy_ (u"ࠫࡡࡴࠧ౒")
        bstack1l1ll1l11l_opy_ = bstack111l111_opy_ (u"ࠬࠦࠧ౓").join(bstack11l111ll1l_opy_)
        if runner.driver_initialised in [bstack111l111_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠢ౔"), bstack111l111_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ౕࠦ")]:
          bstack1ll1llllll_opy_(context, bstack1l1ll1l11l_opy_, bstack111l111_opy_ (u"ࠣࡧࡵࡶࡴࡸౖࠢ"))
          bstack1lllllll1_opy_(getattr(context, bstack111l111_opy_ (u"ࠩࡳࡥ࡬࡫ࠧ౗"), None), bstack111l111_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥౘ"), bstack1lll1llll_opy_)
          bstack11lll11l1l_opy_.execute_script(bstack111l111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩౙ") + json.dumps(bstack1l1ll1l11l_opy_) + bstack111l111_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥࡩࡷࡸ࡯ࡳࠤࢀࢁࠬౚ"))
          bstack1l11ll11ll_opy_(bstack11lll11l1l_opy_, bstack111l111_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ౛"), bstack111l111_opy_ (u"ࠢࡔࡱࡰࡩࠥࡹࡣࡦࡰࡤࡶ࡮ࡵࡳࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢ࡟ࡲࠧ౜") + str(bstack1lll1llll_opy_))
          bstack11l1111111_opy_ = bstack1l1l1l1ll1_opy_(bstack1l1ll1l11l_opy_, runner.feature.name, logger)
          if (bstack11l1111111_opy_ != None):
            bstack1llll1l1_opy_.append(bstack11l1111111_opy_)
      else:
        if runner.driver_initialised in [bstack111l111_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠤౝ"), bstack111l111_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨ౞")]:
          bstack1ll1llllll_opy_(context, bstack111l111_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨ࠾ࠥࠨ౟") + str(runner.feature.name) + bstack111l111_opy_ (u"ࠦࠥࡶࡡࡴࡵࡨࡨࠦࠨౠ"), bstack111l111_opy_ (u"ࠧ࡯࡮ࡧࡱࠥౡ"))
          bstack1lllllll1_opy_(getattr(context, bstack111l111_opy_ (u"࠭ࡰࡢࡩࡨࠫౢ"), None), bstack111l111_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢౣ"))
          bstack11lll11l1l_opy_.execute_script(bstack111l111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭౤") + json.dumps(bstack111l111_opy_ (u"ࠤࡉࡩࡦࡺࡵࡳࡧ࠽ࠤࠧ౥") + str(runner.feature.name) + bstack111l111_opy_ (u"ࠥࠤࡵࡧࡳࡴࡧࡧࠥࠧ౦")) + bstack111l111_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢࡾࡿࠪ౧"))
          bstack1l11ll11ll_opy_(bstack11lll11l1l_opy_, bstack111l111_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ౨"))
          bstack11l1111111_opy_ = bstack1l1l1l1ll1_opy_(bstack1l1ll1l11l_opy_, runner.feature.name, logger)
          if (bstack11l1111111_opy_ != None):
            bstack1llll1l1_opy_.append(bstack11l1111111_opy_)
    except Exception as e:
      logger.debug(bstack111l111_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨ౩").format(str(e)))
    bstack1ll1l1l1_opy_(runner, name, context, context.feature, bstack11lllll1ll_opy_, *args)
@measure(event_name=EVENTS.bstack11ll1l11l_opy_, stage=STAGE.bstack11l1llll1_opy_, hook_type=bstack111l111_opy_ (u"ࠢࡢࡨࡷࡩࡷࡇ࡬࡭ࠤ౪"), bstack11llll1lll_opy_=bstack1ll1l11l1l_opy_)
def bstack111l11lll_opy_(runner, name, context, bstack11lllll1ll_opy_, *args):
    bstack1ll1l1l1_opy_(runner, name, context, runner, bstack11lllll1ll_opy_, *args)
def bstack11l1l111ll_opy_(self, name, context, *args):
  try:
    if bstack11l1l111_opy_:
      platform_index = int(threading.current_thread()._name) % bstack1l1l11l1l1_opy_
      bstack1l11llllll_opy_ = CONFIG[bstack111l111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ౫")][platform_index]
      os.environ[bstack111l111_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪ౬")] = json.dumps(bstack1l11llllll_opy_)
    global bstack11lllll1ll_opy_
    if not hasattr(self, bstack111l111_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡸ࡫ࡤࠨ౭")):
      self.driver_initialised = None
    bstack11l1lll1l_opy_ = {
        bstack111l111_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠨ౮"): bstack11l1lllll1_opy_,
        bstack111l111_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭౯"): bstack1ll1ll11ll_opy_,
        bstack111l111_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡴࡢࡩࠪ౰"): bstack1llll1ll1_opy_,
        bstack111l111_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩ౱"): bstack111lll1l1_opy_,
        bstack111l111_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵ࠭౲"): bstack111lllll1_opy_,
        bstack111l111_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡷࡩࡵ࠭౳"): bstack1l1ll11l11_opy_,
        bstack111l111_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ౴"): bstack1ll11111l1_opy_,
        bstack111l111_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡸࡦ࡭ࠧ౵"): bstack1l1l11lll_opy_,
        bstack111l111_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬ౶"): bstack1ll1l11ll_opy_,
        bstack111l111_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠩ౷"): bstack111l11lll_opy_
    }
    handler = bstack11l1lll1l_opy_.get(name, bstack11lllll1ll_opy_)
    try:
      handler(self, name, context, bstack11lllll1ll_opy_, *args)
    except Exception as e:
      logger.debug(bstack111l111_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡥࡩ࡭ࡧࡶࡦࠢ࡫ࡳࡴࡱࠠࡩࡣࡱࡨࡱ࡫ࡲࠡࡽࢀ࠾ࠥࢁࡽࠨ౸").format(name, str(e)))
    if name in [bstack111l111_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨ౹"), bstack111l111_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ౺"), bstack111l111_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ࠭౻")]:
      try:
        bstack11lll11l1l_opy_ = threading.current_thread().bstackSessionDriver if bstack1111ll1l_opy_(bstack111l111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ౼")) else context.browser
        bstack1lllll1111_opy_ = (
          (name == bstack111l111_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠨ౽") and self.driver_initialised == bstack111l111_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥ౾")) or
          (name == bstack111l111_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡦࡦࡣࡷࡹࡷ࡫ࠧ౿") and self.driver_initialised == bstack111l111_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠤಀ")) or
          (name == bstack111l111_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪಁ") and self.driver_initialised in [bstack111l111_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧಂ"), bstack111l111_opy_ (u"ࠦ࡮ࡴࡳࡵࡧࡳࠦಃ")]) or
          (name == bstack111l111_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡺࡥࡱࠩ಄") and self.driver_initialised == bstack111l111_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦಅ"))
        )
        if bstack1lllll1111_opy_:
          self.driver_initialised = None
          if bstack11lll11l1l_opy_ and hasattr(bstack11lll11l1l_opy_, bstack111l111_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠫಆ")):
            try:
              bstack11lll11l1l_opy_.quit()
            except Exception as e:
              logger.debug(bstack111l111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡲࡷ࡬ࡸࡹ࡯࡮ࡨࠢࡧࡶ࡮ࡼࡥࡳࠢ࡬ࡲࠥࡨࡥࡩࡣࡹࡩࠥ࡮࡯ࡰ࡭࠽ࠤࢀࢃࠧಇ").format(str(e)))
      except Exception as e:
        logger.debug(bstack111l111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࠣ࡬ࡴࡵ࡫ࠡࡥ࡯ࡩࡦࡴࡵࡱࠢࡩࡳࡷࠦࡻࡾ࠼ࠣࡿࢂ࠭ಈ").format(name, str(e)))
  except Exception as e:
    logger.debug(bstack111l111_opy_ (u"ࠪࡇࡷ࡯ࡴࡪࡥࡤࡰࠥ࡫ࡲࡳࡱࡵࠤ࡮ࡴࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡳࡷࡱࠤ࡭ࡵ࡯࡬ࠢࡾࢁ࠿ࠦࡻࡾࠩಉ").format(name, str(e)))
    try:
      bstack11lllll1ll_opy_(self, name, context, *args)
    except Exception as e2:
      logger.debug(bstack111l111_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࠣࡦࡪ࡮ࡡࡷࡧࠣ࡬ࡴࡵ࡫ࠡࡽࢀ࠾ࠥࢁࡽࠨಊ").format(name, str(e2)))
def bstack11ll11ll1l_opy_(config, startdir):
  return bstack111l111_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶ࠿ࠦࡻ࠱ࡿࠥಋ").format(bstack111l111_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧಌ"))
notset = Notset()
def bstack1l11111ll_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1l1lll11l_opy_
  if str(name).lower() == bstack111l111_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸࠧ಍"):
    return bstack111l111_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢಎ")
  else:
    return bstack1l1lll11l_opy_(self, name, default, skip)
def bstack11ll1l1l_opy_(item, when):
  global bstack1ll11l1111_opy_
  try:
    bstack1ll11l1111_opy_(item, when)
  except Exception as e:
    pass
def bstack1l111l1ll_opy_():
  return
def bstack1llll1111l_opy_(type, name, status, reason, bstack1l1l11ll_opy_, bstack1ll1l1l111_opy_):
  bstack11ll111l11_opy_ = {
    bstack111l111_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩಏ"): type,
    bstack111l111_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ಐ"): {}
  }
  if type == bstack111l111_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭಑"):
    bstack11ll111l11_opy_[bstack111l111_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨಒ")][bstack111l111_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬಓ")] = bstack1l1l11ll_opy_
    bstack11ll111l11_opy_[bstack111l111_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪಔ")][bstack111l111_opy_ (u"ࠨࡦࡤࡸࡦ࠭ಕ")] = json.dumps(str(bstack1ll1l1l111_opy_))
  if type == bstack111l111_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪಖ"):
    bstack11ll111l11_opy_[bstack111l111_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ಗ")][bstack111l111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩಘ")] = name
  if type == bstack111l111_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨಙ"):
    bstack11ll111l11_opy_[bstack111l111_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩಚ")][bstack111l111_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧಛ")] = status
    if status == bstack111l111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨಜ"):
      bstack11ll111l11_opy_[bstack111l111_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬಝ")][bstack111l111_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪಞ")] = json.dumps(str(reason))
  bstack111lllllll_opy_ = bstack111l111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩಟ").format(json.dumps(bstack11ll111l11_opy_))
  return bstack111lllllll_opy_
def bstack1ll111ll1l_opy_(driver_command, response):
    if driver_command == bstack111l111_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠩಠ"):
        bstack1l1ll1l11_opy_.bstack1ll1l1lll_opy_({
            bstack111l111_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬಡ"): response[bstack111l111_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭ಢ")],
            bstack111l111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨಣ"): bstack1l1ll1l11_opy_.current_test_uuid()
        })
def bstack1l1l1l111l_opy_(item, call, rep):
  global bstack11l1l1111l_opy_
  global bstack11ll1lllll_opy_
  global bstack1l111l1l_opy_
  name = bstack111l111_opy_ (u"ࠩࠪತ")
  try:
    if rep.when == bstack111l111_opy_ (u"ࠪࡧࡦࡲ࡬ࠨಥ"):
      bstack11l11ll11l_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1l111l1l_opy_:
          name = str(rep.nodeid)
          bstack1l11llll1_opy_ = bstack1llll1111l_opy_(bstack111l111_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬದ"), name, bstack111l111_opy_ (u"ࠬ࠭ಧ"), bstack111l111_opy_ (u"࠭ࠧನ"), bstack111l111_opy_ (u"ࠧࠨ಩"), bstack111l111_opy_ (u"ࠨࠩಪ"))
          threading.current_thread().bstack1ll1l1llll_opy_ = name
          for driver in bstack11ll1lllll_opy_:
            if bstack11l11ll11l_opy_ == driver.session_id:
              driver.execute_script(bstack1l11llll1_opy_)
      except Exception as e:
        logger.debug(bstack111l111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩಫ").format(str(e)))
      try:
        bstack11ll1llll1_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack111l111_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫಬ"):
          status = bstack111l111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫಭ") if rep.outcome.lower() == bstack111l111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬಮ") else bstack111l111_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ಯ")
          reason = bstack111l111_opy_ (u"ࠧࠨರ")
          if status == bstack111l111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨಱ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack111l111_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧಲ") if status == bstack111l111_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪಳ") else bstack111l111_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ಴")
          data = name + bstack111l111_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧವ") if status == bstack111l111_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ಶ") else name + bstack111l111_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠢࠢࠪಷ") + reason
          bstack11ll11l1l_opy_ = bstack1llll1111l_opy_(bstack111l111_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪಸ"), bstack111l111_opy_ (u"ࠩࠪಹ"), bstack111l111_opy_ (u"ࠪࠫ಺"), bstack111l111_opy_ (u"ࠫࠬ಻"), level, data)
          for driver in bstack11ll1lllll_opy_:
            if bstack11l11ll11l_opy_ == driver.session_id:
              driver.execute_script(bstack11ll11l1l_opy_)
      except Exception as e:
        logger.debug(bstack111l111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡦࡳࡳࡺࡥࡹࡶࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾ಼ࠩ").format(str(e)))
  except Exception as e:
    logger.debug(bstack111l111_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡶࡸࡦࡺࡥࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼࡿࠪಽ").format(str(e)))
  bstack11l1l1111l_opy_(item, call, rep)
def bstack11l11111_opy_(driver, bstack1l111l11_opy_, test=None):
  global bstack1l11lllll_opy_
  if test != None:
    bstack1l111l11l1_opy_ = getattr(test, bstack111l111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬಾ"), None)
    bstack11l11l1l1_opy_ = getattr(test, bstack111l111_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ಿ"), None)
    PercySDK.screenshot(driver, bstack1l111l11_opy_, bstack1l111l11l1_opy_=bstack1l111l11l1_opy_, bstack11l11l1l1_opy_=bstack11l11l1l1_opy_, bstack111llllll1_opy_=bstack1l11lllll_opy_)
  else:
    PercySDK.screenshot(driver, bstack1l111l11_opy_)
@measure(event_name=EVENTS.bstack1l1ll1ll11_opy_, stage=STAGE.bstack11l1llll1_opy_, bstack11llll1lll_opy_=bstack1ll1l11l1l_opy_)
def bstack1l1lll1lll_opy_(driver):
  if bstack1111l11l_opy_.bstack1l111llll_opy_() is True or bstack1111l11l_opy_.capturing() is True:
    return
  bstack1111l11l_opy_.bstack1111l1ll_opy_()
  while not bstack1111l11l_opy_.bstack1l111llll_opy_():
    bstack1ll11lll1_opy_ = bstack1111l11l_opy_.bstack1l1l1111l_opy_()
    bstack11l11111_opy_(driver, bstack1ll11lll1_opy_)
  bstack1111l11l_opy_.bstack1ll1ll111_opy_()
def bstack1l1111ll1_opy_(sequence, driver_command, response = None, bstack1lllll1l1_opy_ = None, args = None):
    try:
      if sequence != bstack111l111_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩೀ"):
        return
      if percy.bstack1l11ll111_opy_() == bstack111l111_opy_ (u"ࠥࡪࡦࡲࡳࡦࠤು"):
        return
      bstack1ll11lll1_opy_ = bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧೂ"), None)
      for command in bstack1l1l1l111_opy_:
        if command == driver_command:
          with bstack11lllllll_opy_:
            bstack1lll1ll111_opy_ = bstack11ll1lllll_opy_.copy()
          for driver in bstack1lll1ll111_opy_:
            bstack1l1lll1lll_opy_(driver)
      bstack11lllll11l_opy_ = percy.bstack1l111llll1_opy_()
      if driver_command in bstack1111111ll_opy_[bstack11lllll11l_opy_]:
        bstack1111l11l_opy_.bstack1lll1111l_opy_(bstack1ll11lll1_opy_, driver_command)
    except Exception as e:
      pass
def bstack1ll11l111_opy_(framework_name):
  if bstack1ll1ll11_opy_.get_property(bstack111l111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩೃ")):
      return
  bstack1ll1ll11_opy_.bstack1ll11l1l_opy_(bstack111l111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪೄ"), True)
  global bstack11l1l1ll1l_opy_
  global bstack1lllllll11_opy_
  global bstack1111111l1_opy_
  bstack11l1l1ll1l_opy_ = framework_name
  logger.info(bstack1lll1ll11_opy_.format(bstack11l1l1ll1l_opy_.split(bstack111l111_opy_ (u"ࠧ࠮ࠩ೅"))[0]))
  bstack1l1ll1ll1l_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack11l1l111_opy_:
      Service.start = bstack11111lll1_opy_
      Service.stop = bstack1l1111l111_opy_
      webdriver.Remote.get = bstack1l1l1lll11_opy_
      WebDriver.quit = bstack11l11111ll_opy_
      webdriver.Remote.__init__ = bstack11ll1l1ll1_opy_
    if not bstack11l1l111_opy_:
        webdriver.Remote.__init__ = bstack1l1l11ll11_opy_
    WebDriver.getAccessibilityResults = getAccessibilityResults
    WebDriver.get_accessibility_results = getAccessibilityResults
    WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
    WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
    WebDriver.performScan = perform_scan
    WebDriver.perform_scan = perform_scan
    WebDriver.execute = bstack1l1l1llll_opy_
    bstack1lllllll11_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack11l1l111_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack11l1llllll_opy_
  except Exception as e:
    pass
  bstack11lll1l11l_opy_()
  if not bstack1lllllll11_opy_:
    bstack1l1lll1ll_opy_(bstack111l111_opy_ (u"ࠣࡒࡤࡧࡰࡧࡧࡦࡵࠣࡲࡴࡺࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠥೆ"), bstack11lll1l1l1_opy_)
  if bstack1l1111111l_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      if hasattr(RemoteConnection, bstack111l111_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪೇ")) and callable(getattr(RemoteConnection, bstack111l111_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫೈ"))):
        RemoteConnection._get_proxy_url = bstack111ll1lll_opy_
      else:
        from selenium.webdriver.remote.client_config import ClientConfig
        ClientConfig.get_proxy_url = bstack111ll1lll_opy_
    except Exception as e:
      logger.error(bstack11l111l11l_opy_.format(str(e)))
  if bstack1ll1l11lll_opy_():
    bstack1llll1ll11_opy_(CONFIG, logger)
  if (bstack111l111_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ೉") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if percy.bstack1l11ll111_opy_() == bstack111l111_opy_ (u"ࠧࡺࡲࡶࡧࠥೊ"):
          bstack1ll11l1l1l_opy_(bstack1l1111ll1_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1llll11l_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1l11lll1l_opy_
      except Exception as e:
        logger.warn(bstack1l111l1lll_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack11111ll1_opy_
      except Exception as e:
        logger.debug(bstack1l11l1111_opy_ + str(e))
    except Exception as e:
      bstack1l1lll1ll_opy_(e, bstack1l111l1lll_opy_)
    Output.start_test = bstack1ll11l11_opy_
    Output.end_test = bstack1ll1l1l1ll_opy_
    TestStatus.__init__ = bstack11l1ll111l_opy_
    QueueItem.__init__ = bstack11l1l1llll_opy_
    pabot._create_items = bstack1l1lllll1l_opy_
    try:
      from pabot import __version__ as bstack1ll1l1l1l1_opy_
      if version.parse(bstack1ll1l1l1l1_opy_) >= version.parse(bstack111l111_opy_ (u"࠭࠴࠯࠴࠱࠴ࠬೋ")):
        pabot._run = bstack1lllllllll_opy_
      elif version.parse(bstack1ll1l1l1l1_opy_) >= version.parse(bstack111l111_opy_ (u"ࠧ࠳࠰࠴࠹࠳࠶ࠧೌ")):
        pabot._run = bstack11l1111l1l_opy_
      elif version.parse(bstack1ll1l1l1l1_opy_) >= version.parse(bstack111l111_opy_ (u"ࠨ࠴࠱࠵࠸࠴࠰ࠨ್")):
        pabot._run = bstack11l1l1ll1_opy_
      else:
        pabot._run = bstack1l1ll1l111_opy_
    except Exception as e:
      pabot._run = bstack1l1ll1l111_opy_
    pabot._create_command_for_execution = bstack1l1l1l1l1l_opy_
    pabot._report_results = bstack11l11ll1_opy_
  if bstack111l111_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ೎") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l1lll1ll_opy_(e, bstack1l11llll11_opy_)
    Runner.run_hook = bstack11l1l111ll_opy_
    Step.run = bstack11111111_opy_
  if bstack111l111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ೏") in str(framework_name).lower():
    if not bstack11l1l111_opy_:
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack11ll11ll1l_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1l111l1ll_opy_
      Config.getoption = bstack1l11111ll_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1l1l1l111l_opy_
    except Exception as e:
      pass
def bstack1lll1ll1l1_opy_():
  global CONFIG
  if bstack111l111_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ೐") in CONFIG and int(CONFIG[bstack111l111_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ೑")]) > 1:
    logger.warn(bstack111l11l1l_opy_)
def bstack11l1111ll_opy_(arg, bstack1l1l1l11ll_opy_, bstack111lllll_opy_=None):
  global CONFIG
  global bstack1l11111l1l_opy_
  global bstack1l11111lll_opy_
  global bstack11l1l111_opy_
  global bstack1ll1ll11_opy_
  bstack11l1l11111_opy_ = bstack111l111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭೒")
  if bstack1l1l1l11ll_opy_ and isinstance(bstack1l1l1l11ll_opy_, str):
    bstack1l1l1l11ll_opy_ = eval(bstack1l1l1l11ll_opy_)
  CONFIG = bstack1l1l1l11ll_opy_[bstack111l111_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧ೓")]
  bstack1l11111l1l_opy_ = bstack1l1l1l11ll_opy_[bstack111l111_opy_ (u"ࠨࡊࡘࡆࡤ࡛ࡒࡍࠩ೔")]
  bstack1l11111lll_opy_ = bstack1l1l1l11ll_opy_[bstack111l111_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫೕ")]
  bstack11l1l111_opy_ = bstack1l1l1l11ll_opy_[bstack111l111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭ೖ")]
  bstack1ll1ll11_opy_.bstack1ll11l1l_opy_(bstack111l111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬ೗"), bstack11l1l111_opy_)
  os.environ[bstack111l111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ೘")] = bstack11l1l11111_opy_
  os.environ[bstack111l111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࠬ೙")] = json.dumps(CONFIG)
  os.environ[bstack111l111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡈࡖࡄࡢ࡙ࡗࡒࠧ೚")] = bstack1l11111l1l_opy_
  os.environ[bstack111l111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ೛")] = str(bstack1l11111lll_opy_)
  os.environ[bstack111l111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡏ࡙ࡌࡏࡎࠨ೜")] = str(True)
  if bstack1l1111l11_opy_(arg, [bstack111l111_opy_ (u"ࠪ࠱ࡳ࠭ೝ"), bstack111l111_opy_ (u"ࠫ࠲࠳࡮ࡶ࡯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬೞ")]) != -1:
    os.environ[bstack111l111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡇࡒࡂࡎࡏࡉࡑ࠭೟")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack11ll1111l1_opy_)
    return
  bstack1l11l1l111_opy_()
  global bstack1l111ll1ll_opy_
  global bstack1l11lllll_opy_
  global bstack1l11ll1ll1_opy_
  global bstack1lll1l1ll1_opy_
  global bstack1111l1l1l_opy_
  global bstack1111111l1_opy_
  global bstack1l11l11l1l_opy_
  arg.append(bstack111l111_opy_ (u"ࠨ࠭ࡘࠤೠ"))
  arg.append(bstack111l111_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫࠺ࡎࡱࡧࡹࡱ࡫ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡ࡫ࡰࡴࡴࡸࡴࡦࡦ࠽ࡴࡾࡺࡥࡴࡶ࠱ࡔࡾࡺࡥࡴࡶ࡚ࡥࡷࡴࡩ࡯ࡩࠥೡ"))
  arg.append(bstack111l111_opy_ (u"ࠣ࠯࡚ࠦೢ"))
  arg.append(bstack111l111_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡦ࠼ࡗ࡬ࡪࠦࡨࡰࡱ࡮࡭ࡲࡶ࡬ࠣೣ"))
  global bstack1lll1ll1_opy_
  global bstack111l1ll1l_opy_
  global bstack1lll1l111_opy_
  global bstack11l1ll111_opy_
  global bstack1ll111111_opy_
  global bstack1l1lll11ll_opy_
  global bstack1l1llll1ll_opy_
  global bstack1llll11l1l_opy_
  global bstack1111ll1l1_opy_
  global bstack1l1ll11l_opy_
  global bstack1l1lll11l_opy_
  global bstack1ll11l1111_opy_
  global bstack11l1l1111l_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1lll1ll1_opy_ = webdriver.Remote.__init__
    bstack111l1ll1l_opy_ = WebDriver.quit
    bstack1llll11l1l_opy_ = WebDriver.close
    bstack1111ll1l1_opy_ = WebDriver.get
    bstack1lll1l111_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack11ll11l1_opy_(CONFIG) and bstack1l1llll1l1_opy_():
    if bstack1llllll1l_opy_() < version.parse(bstack1ll1l11l11_opy_):
      logger.error(bstack1ll1l111ll_opy_.format(bstack1llllll1l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack111l111_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫ೤")) and callable(getattr(RemoteConnection, bstack111l111_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬ೥"))):
          bstack1l1ll11l_opy_ = RemoteConnection._get_proxy_url
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          bstack1l1ll11l_opy_ = ClientConfig.get_proxy_url
      except Exception as e:
        logger.error(bstack11l111l11l_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1l1lll11l_opy_ = Config.getoption
    from _pytest import runner
    bstack1ll11l1111_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack11l1ll11_opy_)
  try:
    from pytest_bdd import reporting
    bstack11l1l1111l_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack111l111_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡴࠦࡲࡶࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࡸ࠭೦"))
  bstack1l11ll1ll1_opy_ = CONFIG.get(bstack111l111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ೧"), {}).get(bstack111l111_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ೨"))
  bstack1l11l11l1l_opy_ = True
  if cli.is_enabled(CONFIG):
    if cli.bstack1l1l1lll1l_opy_():
      bstack1ll1l1ll1l_opy_.invoke(bstack111ll1ll_opy_.CONNECT, bstack1l11ll1l11_opy_())
    platform_index = int(os.environ.get(bstack111l111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ೩"), bstack111l111_opy_ (u"ࠩ࠳ࠫ೪")))
  else:
    bstack1ll11l111_opy_(bstack11ll11llll_opy_)
  os.environ[bstack111l111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫ೫")] = CONFIG[bstack111l111_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭೬")]
  os.environ[bstack111l111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨ೭")] = CONFIG[bstack111l111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ೮")]
  os.environ[bstack111l111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪ೯")] = bstack11l1l111_opy_.__str__()
  from _pytest.config import main as bstack1l11ll1l1_opy_
  bstack1l1ll1ll_opy_ = []
  try:
    exit_code = bstack1l11ll1l1_opy_(arg)
    if cli.is_enabled(CONFIG):
      cli.bstack1llllllll_opy_()
    if bstack111l111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬ೰") in multiprocessing.current_process().__dict__.keys():
      for bstack1ll111ll1_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1l1ll1ll_opy_.append(bstack1ll111ll1_opy_)
    try:
      bstack1l111l111_opy_ = (bstack1l1ll1ll_opy_, int(exit_code))
      bstack111lllll_opy_.append(bstack1l111l111_opy_)
    except:
      bstack111lllll_opy_.append((bstack1l1ll1ll_opy_, exit_code))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack1l1ll1ll_opy_.append({bstack111l111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧೱ"): bstack111l111_opy_ (u"ࠪࡔࡷࡵࡣࡦࡵࡶࠤࠬೲ") + os.environ.get(bstack111l111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫೳ")), bstack111l111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ೴"): traceback.format_exc(), bstack111l111_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ೵"): int(os.environ.get(bstack111l111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ೶")))})
    bstack111lllll_opy_.append((bstack1l1ll1ll_opy_, 1))
def mod_behave_main(args, retries):
  try:
    from behave.configuration import Configuration
    from behave.__main__ import run_behave
    from browserstack_sdk.bstack_behave_runner import BehaveRunner
    config = Configuration(args)
    config.update_userdata({bstack111l111_opy_ (u"ࠣࡴࡨࡸࡷ࡯ࡥࡴࠤ೷"): str(retries)})
    return run_behave(config, runner_class=BehaveRunner)
  except Exception as e:
    bstack1lll11llll_opy_ = e.__class__.__name__
    print(bstack111l111_opy_ (u"ࠤࠨࡷ࠿ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡢࡦࡪࡤࡺࡪࠦࡴࡦࡵࡷࠤࠪࡹࠢ೸") % (bstack1lll11llll_opy_, e))
    return 1
def bstack1l1lll111_opy_(arg):
  global bstack11llll1l1_opy_
  bstack1ll11l111_opy_(bstack1ll11l1l1_opy_)
  os.environ[bstack111l111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ೹")] = str(bstack1l11111lll_opy_)
  retries = bstack11llllll_opy_.bstack1l111ll1l_opy_(CONFIG)
  status_code = 0
  if bstack11llllll_opy_.bstack1lll1l1lll_opy_(CONFIG):
    status_code = mod_behave_main(arg, retries)
  else:
    from behave.__main__ import main as bstack11l1lll11l_opy_
    status_code = bstack11l1lll11l_opy_(arg)
  if status_code != 0:
    bstack11llll1l1_opy_ = status_code
def bstack1l111lll1_opy_():
  logger.info(bstack1l11ll11l1_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack111l111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ೺"), help=bstack111l111_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡣࡰࡰࡩ࡭࡬࠭೻"))
  parser.add_argument(bstack111l111_opy_ (u"࠭࠭ࡶࠩ೼"), bstack111l111_opy_ (u"ࠧ࠮࠯ࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫ೽"), help=bstack111l111_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠧ೾"))
  parser.add_argument(bstack111l111_opy_ (u"ࠩ࠰࡯ࠬ೿"), bstack111l111_opy_ (u"ࠪ࠱࠲ࡱࡥࡺࠩഀ"), help=bstack111l111_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡣࡦࡧࡪࡹࡳࠡ࡭ࡨࡽࠬഁ"))
  parser.add_argument(bstack111l111_opy_ (u"ࠬ࠳ࡦࠨം"), bstack111l111_opy_ (u"࠭࠭࠮ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫഃ"), help=bstack111l111_opy_ (u"࡚ࠧࡱࡸࡶࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ഄ"))
  bstack11l1l11l1_opy_ = parser.parse_args()
  try:
    bstack11l1l1l11_opy_ = bstack111l111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡨࡧࡱࡩࡷ࡯ࡣ࠯ࡻࡰࡰ࠳ࡹࡡ࡮ࡲ࡯ࡩࠬഅ")
    if bstack11l1l11l1_opy_.framework and bstack11l1l11l1_opy_.framework not in (bstack111l111_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩആ"), bstack111l111_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫഇ")):
      bstack11l1l1l11_opy_ = bstack111l111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠴ࡹ࡮࡮࠱ࡷࡦࡳࡰ࡭ࡧࠪഈ")
    bstack1l11l111_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11l1l1l11_opy_)
    bstack1llll1l11l_opy_ = open(bstack1l11l111_opy_, bstack111l111_opy_ (u"ࠬࡸࠧഉ"))
    bstack111l111l_opy_ = bstack1llll1l11l_opy_.read()
    bstack1llll1l11l_opy_.close()
    if bstack11l1l11l1_opy_.username:
      bstack111l111l_opy_ = bstack111l111l_opy_.replace(bstack111l111_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭ഊ"), bstack11l1l11l1_opy_.username)
    if bstack11l1l11l1_opy_.key:
      bstack111l111l_opy_ = bstack111l111l_opy_.replace(bstack111l111_opy_ (u"࡚ࠧࡑࡘࡖࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩഋ"), bstack11l1l11l1_opy_.key)
    if bstack11l1l11l1_opy_.framework:
      bstack111l111l_opy_ = bstack111l111l_opy_.replace(bstack111l111_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩഌ"), bstack11l1l11l1_opy_.framework)
    file_name = bstack111l111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬ഍")
    file_path = os.path.abspath(file_name)
    bstack1l1l11llll_opy_ = open(file_path, bstack111l111_opy_ (u"ࠪࡻࠬഎ"))
    bstack1l1l11llll_opy_.write(bstack111l111l_opy_)
    bstack1l1l11llll_opy_.close()
    logger.info(bstack1ll1111111_opy_)
    try:
      os.environ[bstack111l111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ഏ")] = bstack11l1l11l1_opy_.framework if bstack11l1l11l1_opy_.framework != None else bstack111l111_opy_ (u"ࠧࠨഐ")
      config = yaml.safe_load(bstack111l111l_opy_)
      config[bstack111l111_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭഑")] = bstack111l111_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡴࡧࡷࡹࡵ࠭ഒ")
      bstack1ll11l1l11_opy_(bstack111lll111_opy_, config)
    except Exception as e:
      logger.debug(bstack1lllll111_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1lllllll1l_opy_.format(str(e)))
def bstack1ll11l1l11_opy_(bstack1l1l11l1ll_opy_, config, bstack1l11l1l11_opy_={}):
  global bstack11l1l111_opy_
  global bstack1ll1111ll_opy_
  global bstack1ll1ll11_opy_
  if not config:
    return
  bstack11lll11l11_opy_ = bstack1lll111ll1_opy_ if not bstack11l1l111_opy_ else (
    bstack1l11lll111_opy_ if bstack111l111_opy_ (u"ࠨࡣࡳࡴࠬഓ") in config else (
        bstack11llll1111_opy_ if config.get(bstack111l111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ഔ")) else bstack1l1ll11111_opy_
    )
)
  bstack1l1l1ll11_opy_ = False
  bstack111ll111l_opy_ = False
  if bstack11l1l111_opy_ is True:
      if bstack111l111_opy_ (u"ࠪࡥࡵࡶࠧക") in config:
          bstack1l1l1ll11_opy_ = True
      else:
          bstack111ll111l_opy_ = True
  bstack1ll11llll1_opy_ = bstack1l1ll1l1ll_opy_.bstack11l111ll_opy_(config, bstack1ll1111ll_opy_)
  bstack1l111ll11_opy_ = bstack11l11l1ll_opy_()
  data = {
    bstack111l111_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ഖ"): config[bstack111l111_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧഗ")],
    bstack111l111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩഘ"): config[bstack111l111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪങ")],
    bstack111l111_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬച"): bstack1l1l11l1ll_opy_,
    bstack111l111_opy_ (u"ࠩࡧࡩࡹ࡫ࡣࡵࡧࡧࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ഛ"): os.environ.get(bstack111l111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬജ"), bstack1ll1111ll_opy_),
    bstack111l111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ഝ"): bstack11llll1ll1_opy_,
    bstack111l111_opy_ (u"ࠬࡵࡰࡵ࡫ࡰࡥࡱࡥࡨࡶࡤࡢࡹࡷࡲࠧഞ"): bstack11lll1l1_opy_(),
    bstack111l111_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩട"): {
      bstack111l111_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬഠ"): str(config[bstack111l111_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨഡ")]) if bstack111l111_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩഢ") in config else bstack111l111_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦണ"),
      bstack111l111_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ത"): sys.version,
      bstack111l111_opy_ (u"ࠬࡸࡥࡧࡧࡵࡶࡪࡸࠧഥ"): bstack1l1lll1l1l_opy_(os.environ.get(bstack111l111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨദ"), bstack1ll1111ll_opy_)),
      bstack111l111_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩധ"): bstack111l111_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨന"),
      bstack111l111_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪഩ"): bstack11lll11l11_opy_,
      bstack111l111_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨപ"): bstack1ll11llll1_opy_,
      bstack111l111_opy_ (u"ࠫࡹ࡫ࡳࡵࡪࡸࡦࡤࡻࡵࡪࡦࠪഫ"): os.environ[bstack111l111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪബ")],
      bstack111l111_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩഭ"): os.environ.get(bstack111l111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩമ"), bstack1ll1111ll_opy_),
      bstack111l111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫയ"): bstack1l1111l1l1_opy_(os.environ.get(bstack111l111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫര"), bstack1ll1111ll_opy_)),
      bstack111l111_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩറ"): bstack1l111ll11_opy_.get(bstack111l111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩല")),
      bstack111l111_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫള"): bstack1l111ll11_opy_.get(bstack111l111_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧഴ")),
      bstack111l111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪവ"): config[bstack111l111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫശ")] if config[bstack111l111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬഷ")] else bstack111l111_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦസ"),
      bstack111l111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ഹ"): str(config[bstack111l111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧഺ")]) if bstack111l111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ഻") in config else bstack111l111_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮഼ࠣ"),
      bstack111l111_opy_ (u"ࠨࡱࡶࠫഽ"): sys.platform,
      bstack111l111_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫാ"): socket.gethostname(),
      bstack111l111_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࠬി"): bstack1ll1ll11_opy_.get_property(bstack111l111_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭ീ"))
    }
  }
  if not bstack1ll1ll11_opy_.get_property(bstack111l111_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬു")) is None:
    data[bstack111l111_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩൂ")][bstack111l111_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡏࡨࡸࡦࡪࡡࡵࡣࠪൃ")] = {
      bstack111l111_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨൄ"): bstack111l111_opy_ (u"ࠩࡸࡷࡪࡸ࡟࡬࡫࡯ࡰࡪࡪࠧ൅"),
      bstack111l111_opy_ (u"ࠪࡷ࡮࡭࡮ࡢ࡮ࠪെ"): bstack1ll1ll11_opy_.get_property(bstack111l111_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡘ࡯ࡧ࡯ࡣ࡯ࠫേ")),
      bstack111l111_opy_ (u"ࠬࡹࡩࡨࡰࡤࡰࡓࡻ࡭ࡣࡧࡵࠫൈ"): bstack1ll1ll11_opy_.get_property(bstack111l111_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡎࡰࠩ൉"))
    }
  if bstack1l1l11l1ll_opy_ == bstack111lll11l_opy_:
    data[bstack111l111_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪൊ")][bstack111l111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡃࡰࡰࡩ࡭࡬࠭ോ")] = bstack11ll11l11_opy_(config)
    data[bstack111l111_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬൌ")][bstack111l111_opy_ (u"ࠪ࡭ࡸࡖࡥࡳࡥࡼࡅࡺࡺ࡯ࡆࡰࡤࡦࡱ࡫ࡤࠨ്")] = percy.bstack1ll11llll_opy_
    data[bstack111l111_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧൎ")][bstack111l111_opy_ (u"ࠬࡶࡥࡳࡥࡼࡆࡺ࡯࡬ࡥࡋࡧࠫ൏")] = percy.percy_build_id
  if not bstack11llllll_opy_.bstack11lll11lll_opy_(CONFIG):
    data[bstack111l111_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩ൐")][bstack111l111_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠫ൑")] = bstack11llllll_opy_.bstack11lll11lll_opy_(CONFIG)
  bstack1lll11ll_opy_ = bstack1l1l111l11_opy_.bstack1ll11ll1_opy_(CONFIG, logger)
  bstack1lll1111ll_opy_ = bstack11llllll_opy_.bstack1ll11ll1_opy_(config=CONFIG)
  if bstack1lll11ll_opy_ is not None and bstack1lll1111ll_opy_ is not None and bstack1lll1111ll_opy_.bstack1l111l1l1l_opy_():
    data[bstack111l111_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫ൒")][bstack1lll1111ll_opy_.bstack11llll11_opy_()] = bstack1lll11ll_opy_.bstack1l1lllll_opy_()
  update(data[bstack111l111_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬ൓")], bstack1l11l1l11_opy_)
  try:
    response = bstack1llll111l_opy_(bstack111l111_opy_ (u"ࠪࡔࡔ࡙ࡔࠨൔ"), bstack1ll1l1ll_opy_(bstack1111ll111_opy_), data, {
      bstack111l111_opy_ (u"ࠫࡦࡻࡴࡩࠩൕ"): (config[bstack111l111_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧൖ")], config[bstack111l111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩൗ")])
    })
    if response:
      logger.debug(bstack1ll1llll1_opy_.format(bstack1l1l11l1ll_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack11l111lll1_opy_.format(str(e)))
def bstack1l1lll1l1l_opy_(framework):
  return bstack111l111_opy_ (u"ࠢࡼࡿ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࡽࢀࠦ൘").format(str(framework), __version__) if framework else bstack111l111_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࡻࡾࠤ൙").format(
    __version__)
def bstack1l11l1l111_opy_():
  global CONFIG
  global bstack1ll1l111l_opy_
  if bool(CONFIG):
    return
  try:
    bstack11l1ll1ll1_opy_()
    logger.debug(bstack1111111l_opy_.format(str(CONFIG)))
    bstack1ll1l111l_opy_ = bstack1l1111ll_opy_.bstack11ll1l1l1_opy_(CONFIG, bstack1ll1l111l_opy_)
    bstack1l1ll1ll1l_opy_()
  except Exception as e:
    logger.error(bstack111l111_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࡷࡳ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࠨ൚") + str(e))
    sys.exit(1)
  sys.excepthook = bstack11lll11l1_opy_
  atexit.register(bstack111ll1l11_opy_)
  signal.signal(signal.SIGINT, bstack1ll111ll11_opy_)
  signal.signal(signal.SIGTERM, bstack1ll111ll11_opy_)
def bstack11lll11l1_opy_(exctype, value, traceback):
  global bstack11ll1lllll_opy_
  try:
    for driver in bstack11ll1lllll_opy_:
      bstack1l11ll11ll_opy_(driver, bstack111l111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ൛"), bstack111l111_opy_ (u"ࠦࡘ࡫ࡳࡴ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢ൜") + str(value))
  except Exception:
    pass
  logger.info(bstack1l1l1lll_opy_)
  bstack1l1ll1llll_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1l1ll1llll_opy_(message=bstack111l111_opy_ (u"ࠬ࠭൝"), bstack11lll11111_opy_ = False):
  global CONFIG
  bstack11llll1ll_opy_ = bstack111l111_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠨ൞") if bstack11lll11111_opy_ else bstack111l111_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ൟ")
  try:
    if message:
      bstack1l11l1l11_opy_ = {
        bstack11llll1ll_opy_ : str(message)
      }
      bstack1ll11l1l11_opy_(bstack111lll11l_opy_, CONFIG, bstack1l11l1l11_opy_)
    else:
      bstack1ll11l1l11_opy_(bstack111lll11l_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1l11lll11_opy_.format(str(e)))
def bstack1l11l1ll11_opy_(bstack1l11ll1ll_opy_, size):
  bstack11lll1l1ll_opy_ = []
  while len(bstack1l11ll1ll_opy_) > size:
    bstack1ll1l1111l_opy_ = bstack1l11ll1ll_opy_[:size]
    bstack11lll1l1ll_opy_.append(bstack1ll1l1111l_opy_)
    bstack1l11ll1ll_opy_ = bstack1l11ll1ll_opy_[size:]
  bstack11lll1l1ll_opy_.append(bstack1l11ll1ll_opy_)
  return bstack11lll1l1ll_opy_
def bstack1ll1llll_opy_(args):
  if bstack111l111_opy_ (u"ࠨ࠯ࡰࠫൠ") in args and bstack111l111_opy_ (u"ࠩࡳࡨࡧ࠭ൡ") in args:
    return True
  return False
@measure(event_name=EVENTS.bstack1ll11l11l1_opy_, stage=STAGE.bstack1ll11111l_opy_)
def run_on_browserstack(bstack11l11l1111_opy_=None, bstack111lllll_opy_=None, bstack1l1l1l1111_opy_=False):
  global CONFIG
  global bstack1l11111l1l_opy_
  global bstack1l11111lll_opy_
  global bstack1ll1111ll_opy_
  global bstack1ll1ll11_opy_
  bstack11l1l11111_opy_ = bstack111l111_opy_ (u"ࠪࠫൢ")
  bstack1l1llll111_opy_(bstack11llll1l1l_opy_, logger)
  if bstack11l11l1111_opy_ and isinstance(bstack11l11l1111_opy_, str):
    bstack11l11l1111_opy_ = eval(bstack11l11l1111_opy_)
  if bstack11l11l1111_opy_:
    CONFIG = bstack11l11l1111_opy_[bstack111l111_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫൣ")]
    bstack1l11111l1l_opy_ = bstack11l11l1111_opy_[bstack111l111_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭൤")]
    bstack1l11111lll_opy_ = bstack11l11l1111_opy_[bstack111l111_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ൥")]
    bstack1ll1ll11_opy_.bstack1ll11l1l_opy_(bstack111l111_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ൦"), bstack1l11111lll_opy_)
    bstack11l1l11111_opy_ = bstack111l111_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ൧")
  bstack1ll1ll11_opy_.bstack1ll11l1l_opy_(bstack111l111_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫ൨"), uuid4().__str__())
  logger.info(bstack111l111_opy_ (u"ࠪࡗࡉࡑࠠࡳࡷࡱࠤࡸࡺࡡࡳࡶࡨࡨࠥࡽࡩࡵࡪࠣ࡭ࡩࡀࠠࠨ൩") + bstack1ll1ll11_opy_.get_property(bstack111l111_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭൪")));
  logger.debug(bstack111l111_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪ࠽ࠨ൫") + bstack1ll1ll11_opy_.get_property(bstack111l111_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨ൬")))
  if not bstack1l1l1l1111_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack11ll1111l1_opy_)
      return
    if sys.argv[1] == bstack111l111_opy_ (u"ࠧ࠮࠯ࡹࡩࡷࡹࡩࡰࡰࠪ൭") or sys.argv[1] == bstack111l111_opy_ (u"ࠨ࠯ࡹࠫ൮"):
      logger.info(bstack111l111_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡒࡼࡸ࡭ࡵ࡮ࠡࡕࡇࡏࠥࡼࡻࡾࠩ൯").format(__version__))
      return
    if sys.argv[1] == bstack111l111_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ൰"):
      bstack1l111lll1_opy_()
      return
  args = sys.argv
  bstack1l11l1l111_opy_()
  global bstack1l111ll1ll_opy_
  global bstack1l1l11l1l1_opy_
  global bstack1l11l11l1l_opy_
  global bstack1lll1lll11_opy_
  global bstack1l11lllll_opy_
  global bstack1l11ll1ll1_opy_
  global bstack1lll1l1ll1_opy_
  global bstack11lll1ll_opy_
  global bstack1111l1l1l_opy_
  global bstack1111111l1_opy_
  global bstack11l1ll1ll_opy_
  bstack1l1l11l1l1_opy_ = len(CONFIG.get(bstack111l111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ൱"), []))
  if not bstack11l1l11111_opy_:
    if args[1] == bstack111l111_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ൲") or args[1] == bstack111l111_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧ൳"):
      bstack11l1l11111_opy_ = bstack111l111_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ൴")
      args = args[2:]
    elif args[1] == bstack111l111_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ൵"):
      bstack11l1l11111_opy_ = bstack111l111_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ൶")
      args = args[2:]
    elif args[1] == bstack111l111_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ൷"):
      bstack11l1l11111_opy_ = bstack111l111_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ൸")
      args = args[2:]
    elif args[1] == bstack111l111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭൹"):
      bstack11l1l11111_opy_ = bstack111l111_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧൺ")
      args = args[2:]
    elif args[1] == bstack111l111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧൻ"):
      bstack11l1l11111_opy_ = bstack111l111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨർ")
      args = args[2:]
    elif args[1] == bstack111l111_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩൽ"):
      bstack11l1l11111_opy_ = bstack111l111_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪൾ")
      args = args[2:]
    else:
      if not bstack111l111_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧൿ") in CONFIG or str(CONFIG[bstack111l111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ඀")]).lower() in [bstack111l111_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ඁ"), bstack111l111_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨං")]:
        bstack11l1l11111_opy_ = bstack111l111_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨඃ")
        args = args[1:]
      elif str(CONFIG[bstack111l111_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ඄")]).lower() == bstack111l111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩඅ"):
        bstack11l1l11111_opy_ = bstack111l111_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪආ")
        args = args[1:]
      elif str(CONFIG[bstack111l111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨඇ")]).lower() == bstack111l111_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬඈ"):
        bstack11l1l11111_opy_ = bstack111l111_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ඉ")
        args = args[1:]
      elif str(CONFIG[bstack111l111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫඊ")]).lower() == bstack111l111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩඋ"):
        bstack11l1l11111_opy_ = bstack111l111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪඌ")
        args = args[1:]
      elif str(CONFIG[bstack111l111_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧඍ")]).lower() == bstack111l111_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬඎ"):
        bstack11l1l11111_opy_ = bstack111l111_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ඏ")
        args = args[1:]
      else:
        os.environ[bstack111l111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩඐ")] = bstack11l1l11111_opy_
        bstack11l11ll1ll_opy_(bstack1lllll111l_opy_)
  os.environ[bstack111l111_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩඑ")] = bstack11l1l11111_opy_
  bstack1ll1111ll_opy_ = bstack11l1l11111_opy_
  if cli.is_enabled(CONFIG):
    try:
      bstack1ll1111l_opy_ = bstack1111l1l11_opy_[bstack111l111_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕ࠯ࡅࡈࡉ࠭ඒ")] if bstack11l1l11111_opy_ == bstack111l111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪඓ") and bstack11l1l11l_opy_() else bstack11l1l11111_opy_
      bstack1ll1l1ll1l_opy_.invoke(bstack111ll1ll_opy_.bstack1llllll111_opy_, bstack11ll1l11l1_opy_(
        sdk_version=__version__,
        path_config=bstack11l111llll_opy_(),
        path_project=os.getcwd(),
        test_framework=bstack1ll1111l_opy_,
        frameworks=[bstack1ll1111l_opy_],
        framework_versions={
          bstack1ll1111l_opy_: bstack1l1111l1l1_opy_(bstack111l111_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪඔ") if bstack11l1l11111_opy_ in [bstack111l111_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫඕ"), bstack111l111_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬඖ"), bstack111l111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ඗")] else bstack11l1l11111_opy_)
        },
        bs_config=CONFIG
      ))
      if cli.config.get(bstack111l111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠥ඘"), None):
        CONFIG[bstack111l111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠦ඙")] = cli.config.get(bstack111l111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧක"), None)
    except Exception as e:
      bstack1ll1l1ll1l_opy_.invoke(bstack111ll1ll_opy_.bstack1lll111ll_opy_, e.__traceback__, 1)
    if bstack1l11111lll_opy_:
      CONFIG[bstack111l111_opy_ (u"ࠦࡦࡶࡰࠣඛ")] = cli.config[bstack111l111_opy_ (u"ࠧࡧࡰࡱࠤග")]
      logger.info(bstack11l111ll1_opy_.format(CONFIG[bstack111l111_opy_ (u"࠭ࡡࡱࡲࠪඝ")]))
  else:
    bstack1ll1l1ll1l_opy_.clear()
  global bstack1lll11l111_opy_
  global bstack1l11111l11_opy_
  if bstack11l11l1111_opy_:
    try:
      bstack1l1111lll_opy_ = datetime.datetime.now()
      os.environ[bstack111l111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩඞ")] = bstack11l1l11111_opy_
      bstack1ll11l1l11_opy_(bstack1l1ll1l1l1_opy_, CONFIG)
      cli.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠣࡪࡷࡸࡵࡀࡳࡥ࡭ࡢࡸࡪࡹࡴࡠࡣࡷࡸࡪࡳࡰࡵࡧࡧࠦඟ"), datetime.datetime.now() - bstack1l1111lll_opy_)
    except Exception as e:
      logger.debug(bstack11l1111ll1_opy_.format(str(e)))
  global bstack1lll1ll1_opy_
  global bstack111l1ll1l_opy_
  global bstack1l1l11lll1_opy_
  global bstack1l1l1l1l11_opy_
  global bstack11ll1ll11_opy_
  global bstack11l11lll11_opy_
  global bstack11l1ll111_opy_
  global bstack1ll111111_opy_
  global bstack1l1l11l1_opy_
  global bstack1l1lll11ll_opy_
  global bstack1l1llll1ll_opy_
  global bstack1llll11l1l_opy_
  global bstack11lllll1ll_opy_
  global bstack11lll11ll1_opy_
  global bstack1111ll1l1_opy_
  global bstack1l1ll11l_opy_
  global bstack1l1lll11l_opy_
  global bstack1ll11l1111_opy_
  global bstack1l1ll1lll_opy_
  global bstack11l1l1111l_opy_
  global bstack1lll1l111_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1lll1ll1_opy_ = webdriver.Remote.__init__
    bstack111l1ll1l_opy_ = WebDriver.quit
    bstack1llll11l1l_opy_ = WebDriver.close
    bstack1111ll1l1_opy_ = WebDriver.get
    bstack1lll1l111_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1lll11l111_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack111l11111_opy_
    bstack1l11111l11_opy_ = bstack111l11111_opy_()
  except Exception as e:
    pass
  try:
    global bstack11ll1lll1l_opy_
    from QWeb.keywords import browser
    bstack11ll1lll1l_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack11ll11l1_opy_(CONFIG) and bstack1l1llll1l1_opy_():
    if bstack1llllll1l_opy_() < version.parse(bstack1ll1l11l11_opy_):
      logger.error(bstack1ll1l111ll_opy_.format(bstack1llllll1l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack111l111_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪච")) and callable(getattr(RemoteConnection, bstack111l111_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫඡ"))):
          RemoteConnection._get_proxy_url = bstack111ll1lll_opy_
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          ClientConfig.get_proxy_url = bstack111ll1lll_opy_
      except Exception as e:
        logger.error(bstack11l111l11l_opy_.format(str(e)))
  if not CONFIG.get(bstack111l111_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭ජ"), False) and not bstack11l11l1111_opy_:
    logger.info(bstack11l11l1ll1_opy_)
  if not cli.is_enabled(CONFIG):
    if bstack111l111_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩඣ") in CONFIG and str(CONFIG[bstack111l111_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪඤ")]).lower() != bstack111l111_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ඥ"):
      bstack11lll111ll_opy_()
    elif bstack11l1l11111_opy_ != bstack111l111_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨඦ") or (bstack11l1l11111_opy_ == bstack111l111_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩට") and not bstack11l11l1111_opy_):
      bstack1l111lllll_opy_()
  if (bstack11l1l11111_opy_ in [bstack111l111_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩඨ"), bstack111l111_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪඩ"), bstack111l111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ඪ")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1llll11l_opy_
        bstack11l11lll11_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1l111l1lll_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack11ll1ll11_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1l11l1111_opy_ + str(e))
    except Exception as e:
      bstack1l1lll1ll_opy_(e, bstack1l111l1lll_opy_)
    if bstack11l1l11111_opy_ != bstack111l111_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧණ"):
      bstack11llllll1l_opy_()
    bstack1l1l11lll1_opy_ = Output.start_test
    bstack1l1l1l1l11_opy_ = Output.end_test
    bstack11l1ll111_opy_ = TestStatus.__init__
    bstack1l1l11l1_opy_ = pabot._run
    bstack1l1lll11ll_opy_ = QueueItem.__init__
    bstack1l1llll1ll_opy_ = pabot._create_command_for_execution
    bstack1l1ll1lll_opy_ = pabot._report_results
  if bstack11l1l11111_opy_ == bstack111l111_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧඬ"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l1lll1ll_opy_(e, bstack1l11llll11_opy_)
    bstack11lllll1ll_opy_ = Runner.run_hook
    bstack11lll11ll1_opy_ = Step.run
  if bstack11l1l11111_opy_ == bstack111l111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨත"):
    try:
      from _pytest.config import Config
      bstack1l1lll11l_opy_ = Config.getoption
      from _pytest import runner
      bstack1ll11l1111_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack11l1ll11_opy_)
    try:
      from pytest_bdd import reporting
      bstack11l1l1111l_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack111l111_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡱࠣࡶࡺࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࡵࠪථ"))
  try:
    framework_name = bstack111l111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩද") if bstack11l1l11111_opy_ in [bstack111l111_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪධ"), bstack111l111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫන"), bstack111l111_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧ඲")] else bstack11lll1ll1_opy_(bstack11l1l11111_opy_)
    bstack11l1l1l11l_opy_ = {
      bstack111l111_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠨඳ"): bstack111l111_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪප") if bstack11l1l11111_opy_ == bstack111l111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩඵ") and bstack11l1l11l_opy_() else framework_name,
      bstack111l111_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧබ"): bstack1l1111l1l1_opy_(framework_name),
      bstack111l111_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩභ"): __version__,
      bstack111l111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡷࡶࡩࡩ࠭ම"): bstack11l1l11111_opy_
    }
    if bstack11l1l11111_opy_ in bstack11lll1llll_opy_ + bstack11lllll1_opy_:
      if bstack1l1ll11l1l_opy_.bstack1ll1l1l1l_opy_(CONFIG):
        if bstack111l111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ඹ") in CONFIG:
          os.environ[bstack111l111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨය")] = os.getenv(bstack111l111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩර"), json.dumps(CONFIG[bstack111l111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ඼")]))
          CONFIG[bstack111l111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪල")].pop(bstack111l111_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ඾"), None)
          CONFIG[bstack111l111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ඿")].pop(bstack111l111_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫව"), None)
        bstack11l1l1l11l_opy_[bstack111l111_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧශ")] = {
          bstack111l111_opy_ (u"ࠨࡰࡤࡱࡪ࠭ෂ"): bstack111l111_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫස"),
          bstack111l111_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫහ"): str(bstack1llllll1l_opy_())
        }
    if bstack11l1l11111_opy_ not in [bstack111l111_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬළ")] and not cli.is_running():
      bstack1llll1l11_opy_, bstack11l1111l11_opy_ = bstack1l1ll1l11_opy_.launch(CONFIG, bstack11l1l1l11l_opy_)
      if bstack11l1111l11_opy_.get(bstack111l111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬෆ")) is not None and bstack1l1ll11l1l_opy_.bstack11l1l1ll_opy_(CONFIG) is None:
        value = bstack11l1111l11_opy_[bstack111l111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭෇")].get(bstack111l111_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨ෈"))
        if value is not None:
            CONFIG[bstack111l111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ෉")] = value
        else:
          logger.debug(bstack111l111_opy_ (u"ࠤࡑࡳࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡪࡡࡵࡣࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࡸࡥࡴࡲࡲࡲࡸ࡫්ࠢ"))
  except Exception as e:
    logger.debug(bstack1llll1111_opy_.format(bstack111l111_opy_ (u"ࠪࡘࡪࡹࡴࡉࡷࡥࠫ෋"), str(e)))
  if bstack11l1l11111_opy_ == bstack111l111_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ෌"):
    bstack1l11l11l1l_opy_ = True
    if bstack11l11l1111_opy_ and bstack1l1l1l1111_opy_:
      bstack1l11ll1ll1_opy_ = CONFIG.get(bstack111l111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ෍"), {}).get(bstack111l111_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ෎"))
      bstack1ll11l111_opy_(bstack1l1lll1ll1_opy_)
    elif bstack11l11l1111_opy_:
      bstack1l11ll1ll1_opy_ = CONFIG.get(bstack111l111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫා"), {}).get(bstack111l111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪැ"))
      global bstack11ll1lllll_opy_
      try:
        if bstack1ll1llll_opy_(bstack11l11l1111_opy_[bstack111l111_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬෑ")]) and multiprocessing.current_process().name == bstack111l111_opy_ (u"ࠪ࠴ࠬි"):
          bstack11l11l1111_opy_[bstack111l111_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧී")].remove(bstack111l111_opy_ (u"ࠬ࠳࡭ࠨු"))
          bstack11l11l1111_opy_[bstack111l111_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ෕")].remove(bstack111l111_opy_ (u"ࠧࡱࡦࡥࠫූ"))
          bstack11l11l1111_opy_[bstack111l111_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ෗")] = bstack11l11l1111_opy_[bstack111l111_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬෘ")][0]
          with open(bstack11l11l1111_opy_[bstack111l111_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ෙ")], bstack111l111_opy_ (u"ࠫࡷ࠭ේ")) as f:
            bstack1l111111l_opy_ = f.read()
          bstack1lll11ll1l_opy_ = bstack111l111_opy_ (u"ࠧࠨࠢࡧࡴࡲࡱࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡸࡪ࡫ࠡ࡫ࡰࡴࡴࡸࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡨ࠿ࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥࠩࡽࢀ࠭ࡀࠦࡦࡳࡱࡰࠤࡵࡪࡢࠡ࡫ࡰࡴࡴࡸࡴࠡࡒࡧࡦࡀࠦ࡯ࡨࡡࡧࡦࠥࡃࠠࡑࡦࡥ࠲ࡩࡵ࡟ࡣࡴࡨࡥࡰࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡨࡪ࡬ࠠ࡮ࡱࡧࡣࡧࡸࡥࡢ࡭ࠫࡷࡪࡲࡦ࠭ࠢࡤࡶ࡬࠲ࠠࡵࡧࡰࡴࡴࡸࡡࡳࡻࠣࡁࠥ࠶ࠩ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡵࡴࡼ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡧࡲࡨࠢࡀࠤࡸࡺࡲࠩ࡫ࡱࡸ࠭ࡧࡲࡨࠫ࠮࠵࠵࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡫ࡸࡤࡧࡳࡸࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡣࡶࠤࡪࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡱࡣࡶࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡳ࡬ࡥࡤࡣࠪࡶࡩࡱ࡬ࠬࡢࡴࡪ࠰ࡹ࡫࡭ࡱࡱࡵࡥࡷࡿࠩࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡕࡪࡢ࠯ࡦࡲࡣࡧࠦ࠽ࠡ࡯ࡲࡨࡤࡨࡲࡦࡣ࡮ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡑࡦࡥ࠲ࡩࡵ࡟ࡣࡴࡨࡥࡰࠦ࠽ࠡ࡯ࡲࡨࡤࡨࡲࡦࡣ࡮ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡑࡦࡥࠬ࠮࠴ࡳࡦࡶࡢࡸࡷࡧࡣࡦࠪࠬࡠࡳࠨࠢࠣෛ").format(str(bstack11l11l1111_opy_))
          bstack11l1lll11_opy_ = bstack1lll11ll1l_opy_ + bstack1l111111l_opy_
          bstack11l1l11ll1_opy_ = bstack11l11l1111_opy_[bstack111l111_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩො")] + bstack111l111_opy_ (u"ࠧࡠࡤࡶࡸࡦࡩ࡫ࡠࡶࡨࡱࡵ࠴ࡰࡺࠩෝ")
          with open(bstack11l1l11ll1_opy_, bstack111l111_opy_ (u"ࠨࡹࠪෞ")):
            pass
          with open(bstack11l1l11ll1_opy_, bstack111l111_opy_ (u"ࠤࡺ࠯ࠧෟ")) as f:
            f.write(bstack11l1lll11_opy_)
          import subprocess
          bstack11l11lll1_opy_ = subprocess.run([bstack111l111_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࠥ෠"), bstack11l1l11ll1_opy_])
          if os.path.exists(bstack11l1l11ll1_opy_):
            os.unlink(bstack11l1l11ll1_opy_)
          os._exit(bstack11l11lll1_opy_.returncode)
        else:
          if bstack1ll1llll_opy_(bstack11l11l1111_opy_[bstack111l111_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ෡")]):
            bstack11l11l1111_opy_[bstack111l111_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ෢")].remove(bstack111l111_opy_ (u"࠭࠭࡮ࠩ෣"))
            bstack11l11l1111_opy_[bstack111l111_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ෤")].remove(bstack111l111_opy_ (u"ࠨࡲࡧࡦࠬ෥"))
            bstack11l11l1111_opy_[bstack111l111_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ෦")] = bstack11l11l1111_opy_[bstack111l111_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭෧")][0]
          bstack1ll11l111_opy_(bstack1l1lll1ll1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack11l11l1111_opy_[bstack111l111_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ෨")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack111l111_opy_ (u"ࠬࡥ࡟࡯ࡣࡰࡩࡤࡥࠧ෩")] = bstack111l111_opy_ (u"࠭࡟ࡠ࡯ࡤ࡭ࡳࡥ࡟ࠨ෪")
          mod_globals[bstack111l111_opy_ (u"ࠧࡠࡡࡩ࡭ࡱ࡫࡟ࡠࠩ෫")] = os.path.abspath(bstack11l11l1111_opy_[bstack111l111_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ෬")])
          exec(open(bstack11l11l1111_opy_[bstack111l111_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ෭")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack111l111_opy_ (u"ࠪࡇࡦࡻࡧࡩࡶࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࡼࡿࠪ෮").format(str(e)))
          for driver in bstack11ll1lllll_opy_:
            bstack111lllll_opy_.append({
              bstack111l111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ෯"): bstack11l11l1111_opy_[bstack111l111_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ෰")],
              bstack111l111_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ෱"): str(e),
              bstack111l111_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ෲ"): multiprocessing.current_process().name
            })
            bstack1l11ll11ll_opy_(driver, bstack111l111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨෳ"), bstack111l111_opy_ (u"ࠤࡖࡩࡸࡹࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧ෴") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack11ll1lllll_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1l11111lll_opy_, CONFIG, logger)
      bstack1lll11l1l_opy_()
      bstack1lll1ll1l1_opy_()
      percy.bstack11ll111l1l_opy_()
      bstack1l1l1l11ll_opy_ = {
        bstack111l111_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭෵"): args[0],
        bstack111l111_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫ෶"): CONFIG,
        bstack111l111_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭෷"): bstack1l11111l1l_opy_,
        bstack111l111_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ෸"): bstack1l11111lll_opy_
      }
      if bstack111l111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ෹") in CONFIG:
        bstack111l1l1l1_opy_ = bstack1l1l111l1_opy_(args, logger, CONFIG, bstack11l1l111_opy_, bstack1l1l11l1l1_opy_)
        bstack11lll1ll_opy_ = bstack111l1l1l1_opy_.bstack1llll11ll1_opy_(run_on_browserstack, bstack1l1l1l11ll_opy_, bstack1ll1llll_opy_(args))
      else:
        if bstack1ll1llll_opy_(args):
          bstack1l1l1l11ll_opy_[bstack111l111_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ෺")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1l1l1l11ll_opy_,))
          test.start()
          test.join()
        else:
          bstack1ll11l111_opy_(bstack1l1lll1ll1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack111l111_opy_ (u"ࠩࡢࡣࡳࡧ࡭ࡦࡡࡢࠫ෻")] = bstack111l111_opy_ (u"ࠪࡣࡤࡳࡡࡪࡰࡢࡣࠬ෼")
          mod_globals[bstack111l111_opy_ (u"ࠫࡤࡥࡦࡪ࡮ࡨࡣࡤ࠭෽")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack11l1l11111_opy_ == bstack111l111_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ෾") or bstack11l1l11111_opy_ == bstack111l111_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ෿"):
    percy.init(bstack1l11111lll_opy_, CONFIG, logger)
    percy.bstack11ll111l1l_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1l1lll1ll_opy_(e, bstack1l111l1lll_opy_)
    bstack1lll11l1l_opy_()
    bstack1ll11l111_opy_(bstack1lll11ll11_opy_)
    if bstack11l1l111_opy_:
      bstack1l11l111ll_opy_(bstack1lll11ll11_opy_, args)
      if bstack111l111_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ฀") in args:
        i = args.index(bstack111l111_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ก"))
        args.pop(i)
        args.pop(i)
      if bstack111l111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬข") not in CONFIG:
        CONFIG[bstack111l111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ฃ")] = [{}]
        bstack1l1l11l1l1_opy_ = 1
      if bstack1l111ll1ll_opy_ == 0:
        bstack1l111ll1ll_opy_ = 1
      args.insert(0, str(bstack1l111ll1ll_opy_))
      args.insert(0, str(bstack111l111_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩค")))
    if bstack1l1ll1l11_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1l11ll1l_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1ll11ll1l1_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack111l111_opy_ (u"ࠧࡘࡏࡃࡑࡗࡣࡔࡖࡔࡊࡑࡑࡗࠧฅ"),
        ).parse_args(bstack1l11ll1l_opy_)
        bstack1lll1ll11l_opy_ = args.index(bstack1l11ll1l_opy_[0]) if len(bstack1l11ll1l_opy_) > 0 else len(args)
        args.insert(bstack1lll1ll11l_opy_, str(bstack111l111_opy_ (u"࠭࠭࠮࡮࡬ࡷࡹ࡫࡮ࡦࡴࠪฆ")))
        args.insert(bstack1lll1ll11l_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack111l111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡳࡱࡥࡳࡹࡥ࡬ࡪࡵࡷࡩࡳ࡫ࡲ࠯ࡲࡼࠫง"))))
        if bstack11llllll_opy_.bstack1lll1l1lll_opy_(CONFIG):
          args.insert(bstack1lll1ll11l_opy_, str(bstack111l111_opy_ (u"ࠨ࠯࠰ࡰ࡮ࡹࡴࡦࡰࡨࡶࠬจ")))
          args.insert(bstack1lll1ll11l_opy_ + 1, str(bstack111l111_opy_ (u"ࠩࡕࡩࡹࡸࡹࡇࡣ࡬ࡰࡪࡪ࠺ࡼࡿࠪฉ").format(bstack11llllll_opy_.bstack1l111ll1l_opy_(CONFIG))))
        if bstack1ll111l11l_opy_(os.environ.get(bstack111l111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠨช"))) and str(os.environ.get(bstack111l111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠨซ"), bstack111l111_opy_ (u"ࠬࡴࡵ࡭࡮ࠪฌ"))) != bstack111l111_opy_ (u"࠭࡮ࡶ࡮࡯ࠫญ"):
          for bstack11lllll11_opy_ in bstack1ll11ll1l1_opy_:
            args.remove(bstack11lllll11_opy_)
          test_files = os.environ.get(bstack111l111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠫฎ")).split(bstack111l111_opy_ (u"ࠨ࠮ࠪฏ"))
          for bstack111llllll_opy_ in test_files:
            args.append(bstack111llllll_opy_)
      except Exception as e:
        logger.error(bstack111l111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡢࡶࡷࡥࡨ࡮ࡩ࡯ࡩࠣࡰ࡮ࡹࡴࡦࡰࡨࡶࠥ࡬࡯ࡳࠢࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࠣࡉࡷࡸ࡯ࡳࠢ࠰ࠤࠧฐ").format(e))
    pabot.main(args)
  elif bstack11l1l11111_opy_ == bstack111l111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫฑ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1l1lll1ll_opy_(e, bstack1l111l1lll_opy_)
    for a in args:
      if bstack111l111_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚ࠪฒ") in a:
        bstack1l11lllll_opy_ = int(a.split(bstack111l111_opy_ (u"ࠬࡀࠧณ"))[1])
      if bstack111l111_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪด") in a:
        bstack1l11ll1ll1_opy_ = str(a.split(bstack111l111_opy_ (u"ࠧ࠻ࠩต"))[1])
      if bstack111l111_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓࠨถ") in a:
        bstack1lll1l1ll1_opy_ = str(a.split(bstack111l111_opy_ (u"ࠩ࠽ࠫท"))[1])
    bstack11l11l1l1l_opy_ = None
    if bstack111l111_opy_ (u"ࠪ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠩธ") in args:
      i = args.index(bstack111l111_opy_ (u"ࠫ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠪน"))
      args.pop(i)
      bstack11l11l1l1l_opy_ = args.pop(i)
    if bstack11l11l1l1l_opy_ is not None:
      global bstack11l1ll1111_opy_
      bstack11l1ll1111_opy_ = bstack11l11l1l1l_opy_
    bstack1ll11l111_opy_(bstack1lll11ll11_opy_)
    run_cli(args)
    if bstack111l111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩบ") in multiprocessing.current_process().__dict__.keys():
      for bstack1ll111ll1_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack111lllll_opy_.append(bstack1ll111ll1_opy_)
  elif bstack11l1l11111_opy_ == bstack111l111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ป"):
    bstack1ll111lll_opy_ = bstack1l1l11l111_opy_(args, logger, CONFIG, bstack11l1l111_opy_)
    bstack1ll111lll_opy_.bstack1llll11l1_opy_()
    bstack1lll11l1l_opy_()
    bstack1lll1lll11_opy_ = True
    bstack1111111l1_opy_ = bstack1ll111lll_opy_.bstack1ll1l111l1_opy_()
    bstack1ll111lll_opy_.bstack11111111l_opy_()
    bstack1ll111lll_opy_.bstack1l1l1l11ll_opy_(bstack1l111l1l_opy_)
    bstack1ll1lll1_opy_(bstack11l1l11111_opy_, CONFIG, bstack1ll111lll_opy_.bstack1llll111ll_opy_())
    bstack1l111ll1_opy_ = bstack1ll111lll_opy_.bstack1llll11ll1_opy_(bstack11l1111ll_opy_, {
      bstack111l111_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨผ"): bstack1l11111l1l_opy_,
      bstack111l111_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪฝ"): bstack1l11111lll_opy_,
      bstack111l111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬพ"): bstack11l1l111_opy_
    })
    try:
      bstack1l1ll1ll_opy_, bstack11l1111lll_opy_ = map(list, zip(*bstack1l111ll1_opy_))
      bstack1111l1l1l_opy_ = bstack1l1ll1ll_opy_[0]
      for status_code in bstack11l1111lll_opy_:
        if status_code != 0:
          bstack11l1ll1ll_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack111l111_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡢࡸࡨࠤࡪࡸࡲࡰࡴࡶࠤࡦࡴࡤࠡࡵࡷࡥࡹࡻࡳࠡࡥࡲࡨࡪ࠴ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࠾ࠥࢁࡽࠣฟ").format(str(e)))
  elif bstack11l1l11111_opy_ == bstack111l111_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫภ"):
    try:
      from behave.__main__ import main as bstack11l1lll11l_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1l1lll1ll_opy_(e, bstack1l11llll11_opy_)
    bstack1lll11l1l_opy_()
    bstack1lll1lll11_opy_ = True
    bstack11111l1l1_opy_ = 1
    if bstack111l111_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬม") in CONFIG:
      bstack11111l1l1_opy_ = CONFIG[bstack111l111_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ย")]
    if bstack111l111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪร") in CONFIG:
      bstack11lll1ll1l_opy_ = int(bstack11111l1l1_opy_) * int(len(CONFIG[bstack111l111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫฤ")]))
    else:
      bstack11lll1ll1l_opy_ = int(bstack11111l1l1_opy_)
    config = Configuration(args)
    bstack1lll111l1l_opy_ = config.paths
    if len(bstack1lll111l1l_opy_) == 0:
      import glob
      pattern = bstack111l111_opy_ (u"ࠩ࠭࠮࠴࠰࠮ࡧࡧࡤࡸࡺࡸࡥࠨล")
      bstack11l11l1l11_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack11l11l1l11_opy_)
      config = Configuration(args)
      bstack1lll111l1l_opy_ = config.paths
    bstack1l111lll11_opy_ = [os.path.normpath(item) for item in bstack1lll111l1l_opy_]
    bstack11l11111l1_opy_ = [os.path.normpath(item) for item in args]
    bstack1ll11ll111_opy_ = [item for item in bstack11l11111l1_opy_ if item not in bstack1l111lll11_opy_]
    import platform as pf
    if pf.system().lower() == bstack111l111_opy_ (u"ࠪࡻ࡮ࡴࡤࡰࡹࡶࠫฦ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1l111lll11_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l1l11l11l_opy_)))
                    for bstack1l1l11l11l_opy_ in bstack1l111lll11_opy_]
    bstack1llll1lll_opy_ = []
    for spec in bstack1l111lll11_opy_:
      bstack1llllll11l_opy_ = []
      bstack1llllll11l_opy_ += bstack1ll11ll111_opy_
      bstack1llllll11l_opy_.append(spec)
      bstack1llll1lll_opy_.append(bstack1llllll11l_opy_)
    execution_items = []
    for bstack1llllll11l_opy_ in bstack1llll1lll_opy_:
      if bstack111l111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧว") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack111l111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨศ")]):
          item = {}
          item[bstack111l111_opy_ (u"࠭ࡡࡳࡩࠪษ")] = bstack111l111_opy_ (u"ࠧࠡࠩส").join(bstack1llllll11l_opy_)
          item[bstack111l111_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧห")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack111l111_opy_ (u"ࠩࡤࡶ࡬࠭ฬ")] = bstack111l111_opy_ (u"ࠪࠤࠬอ").join(bstack1llllll11l_opy_)
        item[bstack111l111_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪฮ")] = 0
        execution_items.append(item)
    bstack1ll1ll11l1_opy_ = bstack1l11l1ll11_opy_(execution_items, bstack11lll1ll1l_opy_)
    for execution_item in bstack1ll1ll11l1_opy_:
      bstack11ll1l111l_opy_ = []
      for item in execution_item:
        bstack11ll1l111l_opy_.append(bstack1llll1ll1l_opy_(name=str(item[bstack111l111_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫฯ")]),
                                             target=bstack1l1lll111_opy_,
                                             args=(item[bstack111l111_opy_ (u"࠭ࡡࡳࡩࠪะ")],)))
      for t in bstack11ll1l111l_opy_:
        t.start()
      for t in bstack11ll1l111l_opy_:
        t.join()
  else:
    bstack11l11ll1ll_opy_(bstack1lllll111l_opy_)
  if not bstack11l11l1111_opy_:
    bstack11l11ll1l1_opy_()
    if(bstack11l1l11111_opy_ in [bstack111l111_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧั"), bstack111l111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨา")]):
      bstack1ll111111l_opy_()
  bstack1l1111ll_opy_.bstack1l1l11ll1_opy_()
def browserstack_initialize(bstack1ll1llll1l_opy_=None):
  logger.info(bstack111l111_opy_ (u"ࠩࡕࡹࡳࡴࡩ࡯ࡩࠣࡗࡉࡑࠠࡸ࡫ࡷ࡬ࠥࡧࡲࡨࡵ࠽ࠤࠬำ") + str(bstack1ll1llll1l_opy_))
  run_on_browserstack(bstack1ll1llll1l_opy_, None, True)
@measure(event_name=EVENTS.bstack1l11l1111l_opy_, stage=STAGE.bstack11l1llll1_opy_, bstack11llll1lll_opy_=bstack1ll1l11l1l_opy_)
def bstack11l11ll1l1_opy_():
  global CONFIG
  global bstack1ll1111ll_opy_
  global bstack11l1ll1ll_opy_
  global bstack11llll1l1_opy_
  global bstack1ll1ll11_opy_
  bstack1lll1ll1ll_opy_.bstack1l1l1ll111_opy_()
  if cli.is_running():
    bstack1ll1l1ll1l_opy_.invoke(bstack111ll1ll_opy_.bstack111llll1_opy_)
  if bstack1ll1111ll_opy_ == bstack111l111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪิ"):
    if not cli.is_enabled(CONFIG):
      bstack1l1ll1l11_opy_.stop()
  else:
    bstack1l1ll1l11_opy_.stop()
  if not cli.is_enabled(CONFIG):
    bstack11llll1l11_opy_.bstack11l1lll1l1_opy_()
  if bstack111l111_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨี") in CONFIG and str(CONFIG[bstack111l111_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩึ")]).lower() != bstack111l111_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬื"):
    hashed_id, bstack1l11l11lll_opy_ = bstack1ll111l1l_opy_()
  else:
    hashed_id, bstack1l11l11lll_opy_ = get_build_link()
  bstack1111llll1_opy_(hashed_id)
  logger.info(bstack111l111_opy_ (u"ࠧࡔࡆࡎࠤࡷࡻ࡮ࠡࡧࡱࡨࡪࡪࠠࡧࡱࡵࠤ࡮ࡪ࠺ࠨุ") + bstack1ll1ll11_opy_.get_property(bstack111l111_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦูࠪ"), bstack111l111_opy_ (u"ฺࠩࠪ")) + bstack111l111_opy_ (u"ࠪ࠰ࠥࡺࡥࡴࡶ࡫ࡹࡧࠦࡩࡥ࠼ࠣࠫ฻") + os.getenv(bstack111l111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ฼"), bstack111l111_opy_ (u"ࠬ࠭฽")))
  if hashed_id is not None and bstack1l11l1l1ll_opy_() != -1:
    sessions = bstack11llll111l_opy_(hashed_id)
    bstack1lll11lll1_opy_(sessions, bstack1l11l11lll_opy_)
  if bstack1ll1111ll_opy_ == bstack111l111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭฾") and bstack11l1ll1ll_opy_ != 0:
    sys.exit(bstack11l1ll1ll_opy_)
  if bstack1ll1111ll_opy_ == bstack111l111_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ฿") and bstack11llll1l1_opy_ != 0:
    sys.exit(bstack11llll1l1_opy_)
def bstack1111llll1_opy_(new_id):
    global bstack11llll1ll1_opy_
    bstack11llll1ll1_opy_ = new_id
def bstack11lll1ll1_opy_(bstack1ll1111l11_opy_):
  if bstack1ll1111l11_opy_:
    return bstack1ll1111l11_opy_.capitalize()
  else:
    return bstack111l111_opy_ (u"ࠨࠩเ")
@measure(event_name=EVENTS.bstack11llllll11_opy_, stage=STAGE.bstack11l1llll1_opy_, bstack11llll1lll_opy_=bstack1ll1l11l1l_opy_)
def bstack11l1llll_opy_(bstack11llllll1_opy_):
  if bstack111l111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧแ") in bstack11llllll1_opy_ and bstack11llllll1_opy_[bstack111l111_opy_ (u"ࠪࡲࡦࡳࡥࠨโ")] != bstack111l111_opy_ (u"ࠫࠬใ"):
    return bstack11llllll1_opy_[bstack111l111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪไ")]
  else:
    bstack11llll1lll_opy_ = bstack111l111_opy_ (u"ࠨࠢๅ")
    if bstack111l111_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧๆ") in bstack11llllll1_opy_ and bstack11llllll1_opy_[bstack111l111_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨ็")] != None:
      bstack11llll1lll_opy_ += bstack11llllll1_opy_[bstack111l111_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦ่ࠩ")] + bstack111l111_opy_ (u"ࠥ࠰ࠥࠨ้")
      if bstack11llllll1_opy_[bstack111l111_opy_ (u"ࠫࡴࡹ๊ࠧ")] == bstack111l111_opy_ (u"ࠧ࡯࡯ࡴࠤ๋"):
        bstack11llll1lll_opy_ += bstack111l111_opy_ (u"ࠨࡩࡐࡕࠣࠦ์")
      bstack11llll1lll_opy_ += (bstack11llllll1_opy_[bstack111l111_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫํ")] or bstack111l111_opy_ (u"ࠨࠩ๎"))
      return bstack11llll1lll_opy_
    else:
      bstack11llll1lll_opy_ += bstack11lll1ll1_opy_(bstack11llllll1_opy_[bstack111l111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪ๏")]) + bstack111l111_opy_ (u"ࠥࠤࠧ๐") + (
              bstack11llllll1_opy_[bstack111l111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭๑")] or bstack111l111_opy_ (u"ࠬ࠭๒")) + bstack111l111_opy_ (u"ࠨࠬࠡࠤ๓")
      if bstack11llllll1_opy_[bstack111l111_opy_ (u"ࠧࡰࡵࠪ๔")] == bstack111l111_opy_ (u"࡙ࠣ࡬ࡲࡩࡵࡷࡴࠤ๕"):
        bstack11llll1lll_opy_ += bstack111l111_opy_ (u"ࠤ࡚࡭ࡳࠦࠢ๖")
      bstack11llll1lll_opy_ += bstack11llllll1_opy_[bstack111l111_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ๗")] or bstack111l111_opy_ (u"ࠫࠬ๘")
      return bstack11llll1lll_opy_
@measure(event_name=EVENTS.bstack11l11l11l1_opy_, stage=STAGE.bstack11l1llll1_opy_, bstack11llll1lll_opy_=bstack1ll1l11l1l_opy_)
def bstack1111llll_opy_(bstack1111l1l1_opy_):
  if bstack1111l1l1_opy_ == bstack111l111_opy_ (u"ࠧࡪ࡯࡯ࡧࠥ๙"):
    return bstack111l111_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡩࡵࡩࡪࡴ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡩࡵࡩࡪࡴࠢ࠿ࡅࡲࡱࡵࡲࡥࡵࡧࡧࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩ๚")
  elif bstack1111l1l1_opy_ == bstack111l111_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ๛"):
    return bstack111l111_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡶࡪࡪ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡴࡨࡨࠧࡄࡆࡢ࡫࡯ࡩࡩࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫ๜")
  elif bstack1111l1l1_opy_ == bstack111l111_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ๝"):
    return bstack111l111_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿࡭ࡲࡦࡧࡱ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧ࡭ࡲࡦࡧࡱࠦࡃࡖࡡࡴࡵࡨࡨࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪ๞")
  elif bstack1111l1l1_opy_ == bstack111l111_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥ๟"):
    return bstack111l111_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡳࡧࡧ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡸࡥࡥࠤࡁࡉࡷࡸ࡯ࡳ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ๠")
  elif bstack1111l1l1_opy_ == bstack111l111_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࠢ๡"):
    return bstack111l111_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࠦࡩࡪࡧ࠳࠳࠸࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࠨ࡫ࡥࡢ࠵࠵࠺ࠧࡄࡔࡪ࡯ࡨࡳࡺࡺ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ๢")
  elif bstack1111l1l1_opy_ == bstack111l111_opy_ (u"ࠣࡴࡸࡲࡳ࡯࡮ࡨࠤ๣"):
    return bstack111l111_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡧࡲࡡࡤ࡭࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡧࡲࡡࡤ࡭ࠥࡂࡗࡻ࡮࡯࡫ࡱ࡫ࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪ๤")
  else:
    return bstack111l111_opy_ (u"ࠪࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡢ࡭ࡣࡦ࡯ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡢ࡭ࡣࡦ࡯ࠧࡄࠧ๥") + bstack11lll1ll1_opy_(
      bstack1111l1l1_opy_) + bstack111l111_opy_ (u"ࠫࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪ๦")
def bstack1llll11111_opy_(session):
  return bstack111l111_opy_ (u"ࠬࡂࡴࡳࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡵࡳࡼࠨ࠾࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠢࡶࡩࡸࡹࡩࡰࡰ࠰ࡲࡦࡳࡥࠣࡀ࠿ࡥࠥ࡮ࡲࡦࡨࡀࠦࢀࢃࠢࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤࡢࡦࡱࡧ࡮࡬ࠤࡁࡿࢂࡂ࠯ࡢࡀ࠿࠳ࡹࡪ࠾ࡼࡿࡾࢁࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼࠰ࡶࡵࡂࠬ๧").format(
    session[bstack111l111_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨࡥࡵࡳ࡮ࠪ๨")], bstack11l1llll_opy_(session), bstack1111llll_opy_(session[bstack111l111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡳࡵࡣࡷࡹࡸ࠭๩")]),
    bstack1111llll_opy_(session[bstack111l111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ๪")]),
    bstack11lll1ll1_opy_(session[bstack111l111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪ๫")] or session[bstack111l111_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪ๬")] or bstack111l111_opy_ (u"ࠫࠬ๭")) + bstack111l111_opy_ (u"ࠧࠦࠢ๮") + (session[bstack111l111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ๯")] or bstack111l111_opy_ (u"ࠧࠨ๰")),
    session[bstack111l111_opy_ (u"ࠨࡱࡶࠫ๱")] + bstack111l111_opy_ (u"ࠤࠣࠦ๲") + session[bstack111l111_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ๳")], session[bstack111l111_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭๴")] or bstack111l111_opy_ (u"ࠬ࠭๵"),
    session[bstack111l111_opy_ (u"࠭ࡣࡳࡧࡤࡸࡪࡪ࡟ࡢࡶࠪ๶")] if session[bstack111l111_opy_ (u"ࠧࡤࡴࡨࡥࡹ࡫ࡤࡠࡣࡷࠫ๷")] else bstack111l111_opy_ (u"ࠨࠩ๸"))
@measure(event_name=EVENTS.bstack1ll1l11l_opy_, stage=STAGE.bstack11l1llll1_opy_, bstack11llll1lll_opy_=bstack1ll1l11l1l_opy_)
def bstack1lll11lll1_opy_(sessions, bstack1l11l11lll_opy_):
  try:
    bstack11ll11lll_opy_ = bstack111l111_opy_ (u"ࠤࠥ๹")
    if not os.path.exists(bstack1l11ll1lll_opy_):
      os.mkdir(bstack1l11ll1lll_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack111l111_opy_ (u"ࠪࡥࡸࡹࡥࡵࡵ࠲ࡶࡪࡶ࡯ࡳࡶ࠱࡬ࡹࡳ࡬ࠨ๺")), bstack111l111_opy_ (u"ࠫࡷ࠭๻")) as f:
      bstack11ll11lll_opy_ = f.read()
    bstack11ll11lll_opy_ = bstack11ll11lll_opy_.replace(bstack111l111_opy_ (u"ࠬࢁࠥࡓࡇࡖ࡙ࡑ࡚ࡓࡠࡅࡒ࡙ࡓ࡚ࠥࡾࠩ๼"), str(len(sessions)))
    bstack11ll11lll_opy_ = bstack11ll11lll_opy_.replace(bstack111l111_opy_ (u"࠭ࡻࠦࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠩࢂ࠭๽"), bstack1l11l11lll_opy_)
    bstack11ll11lll_opy_ = bstack11ll11lll_opy_.replace(bstack111l111_opy_ (u"ࠧࡼࠧࡅ࡙ࡎࡒࡄࡠࡐࡄࡑࡊࠫࡽࠨ๾"),
                                              sessions[0].get(bstack111l111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟࡯ࡣࡰࡩࠬ๿")) if sessions[0] else bstack111l111_opy_ (u"ࠩࠪ຀"))
    with open(os.path.join(bstack1l11ll1lll_opy_, bstack111l111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡵࡩࡵࡵࡲࡵ࠰࡫ࡸࡲࡲࠧກ")), bstack111l111_opy_ (u"ࠫࡼ࠭ຂ")) as stream:
      stream.write(bstack11ll11lll_opy_.split(bstack111l111_opy_ (u"ࠬࢁࠥࡔࡇࡖࡗࡎࡕࡎࡔࡡࡇࡅ࡙ࡇࠥࡾࠩ຃"))[0])
      for session in sessions:
        stream.write(bstack1llll11111_opy_(session))
      stream.write(bstack11ll11lll_opy_.split(bstack111l111_opy_ (u"࠭ࡻࠦࡕࡈࡗࡘࡏࡏࡏࡕࡢࡈࡆ࡚ࡁࠦࡿࠪຄ"))[1])
    logger.info(bstack111l111_opy_ (u"ࠧࡈࡧࡱࡩࡷࡧࡴࡦࡦࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡥࡹ࡮ࡲࡤࠡࡣࡵࡸ࡮࡬ࡡࡤࡶࡶࠤࡦࡺࠠࡼࡿࠪ຅").format(bstack1l11ll1lll_opy_));
  except Exception as e:
    logger.debug(bstack111l11ll1_opy_.format(str(e)))
def bstack11llll111l_opy_(hashed_id):
  global CONFIG
  try:
    bstack1l1111lll_opy_ = datetime.datetime.now()
    host = bstack111l111_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡴ࡮࠳ࡣ࡭ࡱࡸࡨ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨຆ") if bstack111l111_opy_ (u"ࠩࡤࡴࡵ࠭ງ") in CONFIG else bstack111l111_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫຈ")
    user = CONFIG[bstack111l111_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ຉ")]
    key = CONFIG[bstack111l111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨຊ")]
    bstack111ll111_opy_ = bstack111l111_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ຋") if bstack111l111_opy_ (u"ࠧࡢࡲࡳࠫຌ") in CONFIG else (bstack111l111_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬຍ") if CONFIG.get(bstack111l111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭ຎ")) else bstack111l111_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬຏ"))
    host = bstack1l1ll11l1_opy_(cli.config, [bstack111l111_opy_ (u"ࠦࡦࡶࡩࡴࠤຐ"), bstack111l111_opy_ (u"ࠧࡧࡰࡱࡃࡸࡸࡴࡳࡡࡵࡧࠥຑ"), bstack111l111_opy_ (u"ࠨࡡࡱ࡫ࠥຒ")], host) if bstack111l111_opy_ (u"ࠧࡢࡲࡳࠫຓ") in CONFIG else bstack1l1ll11l1_opy_(cli.config, [bstack111l111_opy_ (u"ࠣࡣࡳ࡭ࡸࠨດ"), bstack111l111_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨࠦຕ"), bstack111l111_opy_ (u"ࠥࡥࡵ࡯ࠢຖ")], host)
    url = bstack111l111_opy_ (u"ࠫࢀࢃ࠯ࡼࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂ࠵ࡳࡦࡵࡶ࡭ࡴࡴࡳ࠯࡬ࡶࡳࡳ࠭ທ").format(host, bstack111ll111_opy_, hashed_id)
    headers = {
      bstack111l111_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫຘ"): bstack111l111_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩນ"),
    }
    proxies = bstack1lllll11l1_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies, auth=(user, key))
    if response.json():
      cli.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠢࡩࡶࡷࡴ࠿࡭ࡥࡵࡡࡶࡩࡸࡹࡩࡰࡰࡶࡣࡱ࡯ࡳࡵࠤບ"), datetime.datetime.now() - bstack1l1111lll_opy_)
      return list(map(lambda session: session[bstack111l111_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ປ")], response.json()))
  except Exception as e:
    logger.debug(bstack1lll111l1_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack1ll11lll_opy_, stage=STAGE.bstack11l1llll1_opy_, bstack11llll1lll_opy_=bstack1ll1l11l1l_opy_)
def get_build_link():
  global CONFIG
  global bstack11llll1ll1_opy_
  try:
    if bstack111l111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬຜ") in CONFIG:
      bstack1l1111lll_opy_ = datetime.datetime.now()
      host = bstack111l111_opy_ (u"ࠪࡥࡵ࡯࠭ࡤ࡮ࡲࡹࡩ࠭ຝ") if bstack111l111_opy_ (u"ࠫࡦࡶࡰࠨພ") in CONFIG else bstack111l111_opy_ (u"ࠬࡧࡰࡪࠩຟ")
      user = CONFIG[bstack111l111_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨຠ")]
      key = CONFIG[bstack111l111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪມ")]
      bstack111ll111_opy_ = bstack111l111_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧຢ") if bstack111l111_opy_ (u"ࠩࡤࡴࡵ࠭ຣ") in CONFIG else bstack111l111_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ຤")
      url = bstack111l111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࢀࢃ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠴ࡪࡴࡱࡱࠫລ").format(user, key, host, bstack111ll111_opy_)
      if cli.is_enabled(CONFIG):
        bstack1l11l11lll_opy_, hashed_id = cli.bstack11l1l1l1_opy_()
        logger.info(bstack11lll1ll11_opy_.format(bstack1l11l11lll_opy_))
        return [hashed_id, bstack1l11l11lll_opy_]
      else:
        headers = {
          bstack111l111_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫ຦"): bstack111l111_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩວ"),
        }
        if bstack111l111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩຨ") in CONFIG:
          params = {bstack111l111_opy_ (u"ࠨࡰࡤࡱࡪ࠭ຩ"): CONFIG[bstack111l111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬສ")], bstack111l111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ຫ"): CONFIG[bstack111l111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ຬ")]}
        else:
          params = {bstack111l111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪອ"): CONFIG[bstack111l111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩຮ")]}
        proxies = bstack1lllll11l1_opy_(CONFIG, url)
        response = requests.get(url, params=params, headers=headers, proxies=proxies)
        if response.json():
          bstack1l111111_opy_ = response.json()[0][bstack111l111_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡧࡻࡩ࡭ࡦࠪຯ")]
          if bstack1l111111_opy_:
            bstack1l11l11lll_opy_ = bstack1l111111_opy_[bstack111l111_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣࡠࡷࡵࡰࠬະ")].split(bstack111l111_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤ࠯ࡥࡹ࡮ࡲࡤࠨັ"))[0] + bstack111l111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡵ࠲ࠫາ") + bstack1l111111_opy_[
              bstack111l111_opy_ (u"ࠫ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧຳ")]
            logger.info(bstack11lll1ll11_opy_.format(bstack1l11l11lll_opy_))
            bstack11llll1ll1_opy_ = bstack1l111111_opy_[bstack111l111_opy_ (u"ࠬ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨິ")]
            bstack1l1l1ll1_opy_ = CONFIG[bstack111l111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩີ")]
            if bstack111l111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩຶ") in CONFIG:
              bstack1l1l1ll1_opy_ += bstack111l111_opy_ (u"ࠨࠢࠪື") + CONFIG[bstack111l111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵຸࠫ")]
            if bstack1l1l1ll1_opy_ != bstack1l111111_opy_[bstack111l111_opy_ (u"ࠪࡲࡦࡳࡥࠨູ")]:
              logger.debug(bstack11ll11ll1_opy_.format(bstack1l111111_opy_[bstack111l111_opy_ (u"ࠫࡳࡧ࡭ࡦ຺ࠩ")], bstack1l1l1ll1_opy_))
            cli.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࡫ࡪࡺ࡟ࡣࡷ࡬ࡰࡩࡥ࡬ࡪࡰ࡮ࠦົ"), datetime.datetime.now() - bstack1l1111lll_opy_)
            return [bstack1l111111_opy_[bstack111l111_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩຼ")], bstack1l11l11lll_opy_]
    else:
      logger.warn(bstack111l1l11_opy_)
  except Exception as e:
    logger.debug(bstack11l111111l_opy_.format(str(e)))
  return [None, None]
def bstack111l1llll_opy_(url, bstack1lll1l111l_opy_=False):
  global CONFIG
  global bstack1ll1ll1lll_opy_
  if not bstack1ll1ll1lll_opy_:
    hostname = bstack11lll1l1l_opy_(url)
    is_private = bstack11l1l111l1_opy_(hostname)
    if (bstack111l111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫຽ") in CONFIG and not bstack1ll111l11l_opy_(CONFIG[bstack111l111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ຾")])) and (is_private or bstack1lll1l111l_opy_):
      bstack1ll1ll1lll_opy_ = hostname
def bstack11lll1l1l_opy_(url):
  return urlparse(url).hostname
def bstack11l1l111l1_opy_(hostname):
  for bstack1l1l1ll1ll_opy_ in bstack11ll1llll_opy_:
    regex = re.compile(bstack1l1l1ll1ll_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1111ll1l_opy_(bstack1l1l111l1l_opy_):
  return True if bstack1l1l111l1l_opy_ in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack11ll1ll111_opy_, stage=STAGE.bstack11l1llll1_opy_, bstack11llll1lll_opy_=bstack1ll1l11l1l_opy_)
def getAccessibilityResults(driver):
  global CONFIG
  global bstack1l11lllll_opy_
  bstack111ll1l1l_opy_ = not (bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭຿"), None) and bstack1ll11lllll_opy_(
          threading.current_thread(), bstack111l111_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩເ"), None))
  bstack1llllllll1_opy_ = getattr(driver, bstack111l111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫແ"), None) != True
  bstack1ll1l1lll1_opy_ = bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠬ࡯ࡳࡂࡲࡳࡅ࠶࠷ࡹࡕࡧࡶࡸࠬໂ"), None) and bstack1ll11lllll_opy_(
          threading.current_thread(), bstack111l111_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨໃ"), None)
  if bstack1ll1l1lll1_opy_:
    if not bstack111l1lll_opy_():
      logger.warning(bstack111l111_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡲࡳࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡪࡺࡲࡪࡧࡹࡩࠥࡇࡰࡱࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵ࠱ࠦໄ"))
      return {}
    logger.debug(bstack111l111_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠬ໅"))
    logger.debug(perform_scan(driver, driver_command=bstack111l111_opy_ (u"ࠩࡨࡼࡪࡩࡵࡵࡧࡖࡧࡷ࡯ࡰࡵࠩໆ")))
    results = bstack1lll1l1l1_opy_(bstack111l111_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡶࠦ໇"))
    if results is not None and results.get(bstack111l111_opy_ (u"ࠦ࡮ࡹࡳࡶࡧࡶ່ࠦ")) is not None:
        return results[bstack111l111_opy_ (u"ࠧ࡯ࡳࡴࡷࡨࡷ້ࠧ")]
    logger.error(bstack111l111_opy_ (u"ࠨࡎࡰࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡕࡩࡸࡻ࡬ࡵࡵࠣࡻࡪࡸࡥࠡࡨࡲࡹࡳࡪ࠮໊ࠣ"))
    return []
  if not bstack1l1ll11l1l_opy_.bstack11l111lll_opy_(CONFIG, bstack1l11lllll_opy_) or (bstack1llllllll1_opy_ and bstack111ll1l1l_opy_):
    logger.warning(bstack111l111_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴ࠰໋ࠥ"))
    return {}
  try:
    logger.debug(bstack111l111_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠬ໌"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack111lll1ll_opy_.bstack11l1ll1l1_opy_)
    return results
  except Exception:
    logger.error(bstack111l111_opy_ (u"ࠤࡑࡳࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡷࡦࡴࡨࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦໍ"))
    return {}
@measure(event_name=EVENTS.bstack1111l1111_opy_, stage=STAGE.bstack11l1llll1_opy_, bstack11llll1lll_opy_=bstack1ll1l11l1l_opy_)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack1l11lllll_opy_
  bstack111ll1l1l_opy_ = not (bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ໎"), None) and bstack1ll11lllll_opy_(
          threading.current_thread(), bstack111l111_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ໏"), None))
  bstack1llllllll1_opy_ = getattr(driver, bstack111l111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬ໐"), None) != True
  bstack1ll1l1lll1_opy_ = bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭໑"), None) and bstack1ll11lllll_opy_(
          threading.current_thread(), bstack111l111_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ໒"), None)
  if bstack1ll1l1lll1_opy_:
    if not bstack111l1lll_opy_():
      logger.warning(bstack111l111_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡳࡴࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡸࡻ࡭࡮ࡣࡵࡽ࠳ࠨ໓"))
      return {}
    logger.debug(bstack111l111_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡳࡶ࡯ࡰࡥࡷࡿࠧ໔"))
    logger.debug(perform_scan(driver, driver_command=bstack111l111_opy_ (u"ࠪࡩࡽ࡫ࡣࡶࡶࡨࡗࡨࡸࡩࡱࡶࠪ໕")))
    results = bstack1lll1l1l1_opy_(bstack111l111_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷࡗࡺࡳ࡭ࡢࡴࡼࠦ໖"))
    if results is not None and results.get(bstack111l111_opy_ (u"ࠧࡹࡵ࡮࡯ࡤࡶࡾࠨ໗")) is not None:
        return results[bstack111l111_opy_ (u"ࠨࡳࡶ࡯ࡰࡥࡷࡿࠢ໘")]
    logger.error(bstack111l111_opy_ (u"ࠢࡏࡱࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡖࡪࡹࡵ࡭ࡶࡶࠤࡘࡻ࡭࡮ࡣࡵࡽࠥࡽࡡࡴࠢࡩࡳࡺࡴࡤ࠯ࠤ໙"))
    return {}
  if not bstack1l1ll11l1l_opy_.bstack11l111lll_opy_(CONFIG, bstack1l11lllll_opy_) or (bstack1llllllll1_opy_ and bstack111ll1l1l_opy_):
    logger.warning(bstack111l111_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡷࡺࡳ࡭ࡢࡴࡼ࠲ࠧ໚"))
    return {}
  try:
    logger.debug(bstack111l111_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡳࡶ࡯ࡰࡥࡷࡿࠧ໛"))
    logger.debug(perform_scan(driver))
    bstack1lll11l11l_opy_ = driver.execute_async_script(bstack111lll1ll_opy_.bstack1lllll1ll_opy_)
    return bstack1lll11l11l_opy_
  except Exception:
    logger.error(bstack111l111_opy_ (u"ࠥࡒࡴࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡶ࡯ࡰࡥࡷࡿࠠࡸࡣࡶࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦໜ"))
    return {}
def bstack111l1lll_opy_():
  global CONFIG
  global bstack1l11lllll_opy_
  bstack111l11l11_opy_ = bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫໝ"), None) and bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧໞ"), None)
  if not bstack1l1ll11l1l_opy_.bstack11l111lll_opy_(CONFIG, bstack1l11lllll_opy_) or not bstack111l11l11_opy_:
        logger.warning(bstack111l111_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡷ࡫ࡳࡶ࡮ࡷࡷ࠳ࠨໟ"))
        return False
  return True
def bstack1lll1l1l1_opy_(bstack1lll1l1l1l_opy_):
    bstack1l111111l1_opy_ = bstack1l1ll1l11_opy_.current_test_uuid() if bstack1l1ll1l11_opy_.current_test_uuid() else bstack11llll1l11_opy_.current_hook_uuid()
    with ThreadPoolExecutor() as executor:
        future = executor.submit(bstack11111llll_opy_(bstack1l111111l1_opy_, bstack1lll1l1l1l_opy_))
        try:
            return future.result(timeout=bstack11111l1ll_opy_)
        except TimeoutError:
            logger.error(bstack111l111_opy_ (u"ࠢࡕ࡫ࡰࡩࡴࡻࡴࠡࡣࡩࡸࡪࡸࠠࡼࡿࡶࠤࡼ࡮ࡩ࡭ࡧࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡘࡥࡴࡷ࡯ࡸࡸࠨ໠").format(bstack11111l1ll_opy_))
        except Exception as ex:
            logger.debug(bstack111l111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡳࡧࡷࡶ࡮࡫ࡶࡪࡰࡪࠤࡆࡶࡰࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࢁࡽ࠯ࠢࡈࡶࡷࡵࡲࠡ࠯ࠣࡿࢂࠨ໡").format(bstack1lll1l1l1l_opy_, str(ex)))
    return {}
@measure(event_name=EVENTS.bstack1l1l1lll1_opy_, stage=STAGE.bstack11l1llll1_opy_, bstack11llll1lll_opy_=bstack1ll1l11l1l_opy_)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack1l11lllll_opy_
  bstack111ll1l1l_opy_ = not (bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭໢"), None) and bstack1ll11lllll_opy_(
          threading.current_thread(), bstack111l111_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ໣"), None))
  bstack1l11l1l1l_opy_ = not (bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ໤"), None) and bstack1ll11lllll_opy_(
          threading.current_thread(), bstack111l111_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ໥"), None))
  bstack1llllllll1_opy_ = getattr(driver, bstack111l111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭໦"), None) != True
  if not bstack1l1ll11l1l_opy_.bstack11l111lll_opy_(CONFIG, bstack1l11lllll_opy_) or (bstack1llllllll1_opy_ and bstack111ll1l1l_opy_ and bstack1l11l1l1l_opy_):
    logger.warning(bstack111l111_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡶࡰࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮࠯ࠤ໧"))
    return {}
  try:
    bstack1l1lll1l1_opy_ = bstack111l111_opy_ (u"ࠨࡣࡳࡴࠬ໨") in CONFIG and CONFIG.get(bstack111l111_opy_ (u"ࠩࡤࡴࡵ࠭໩"), bstack111l111_opy_ (u"ࠪࠫ໪"))
    session_id = getattr(driver, bstack111l111_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨ໫"), None)
    if not session_id:
      logger.warning(bstack111l111_opy_ (u"ࠧࡔ࡯ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡌࡈࠥ࡬࡯ࡶࡰࡧࠤ࡫ࡵࡲࠡࡦࡵ࡭ࡻ࡫ࡲࠣ໬"))
      return {bstack111l111_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ໭"): bstack111l111_opy_ (u"ࠢࡏࡱࠣࡷࡪࡹࡳࡪࡱࡱࠤࡎࡊࠠࡧࡱࡸࡲࡩࠨ໮")}
    if bstack1l1lll1l1_opy_:
      try:
        bstack11lll1l111_opy_ = {
              bstack111l111_opy_ (u"ࠨࡶ࡫ࡎࡼࡺࡔࡰ࡭ࡨࡲࠬ໯"): os.environ.get(bstack111l111_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ໰"), os.environ.get(bstack111l111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ໱"), bstack111l111_opy_ (u"ࠫࠬ໲"))),
              bstack111l111_opy_ (u"ࠬࡺࡨࡕࡧࡶࡸࡗࡻ࡮ࡖࡷ࡬ࡨࠬ໳"): bstack1l1ll1l11_opy_.current_test_uuid() if bstack1l1ll1l11_opy_.current_test_uuid() else bstack11llll1l11_opy_.current_hook_uuid(),
              bstack111l111_opy_ (u"࠭ࡡࡶࡶ࡫ࡌࡪࡧࡤࡦࡴࠪ໴"): os.environ.get(bstack111l111_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ໵")),
              bstack111l111_opy_ (u"ࠨࡵࡦࡥࡳ࡚ࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ໶"): str(int(datetime.datetime.now().timestamp() * 1000)),
              bstack111l111_opy_ (u"ࠩࡷ࡬ࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧ໷"): os.environ.get(bstack111l111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ໸"), bstack111l111_opy_ (u"ࠫࠬ໹")),
              bstack111l111_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬ໺"): kwargs.get(bstack111l111_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡣࡰ࡯ࡰࡥࡳࡪࠧ໻"), None) or bstack111l111_opy_ (u"ࠧࠨ໼")
          }
        if not hasattr(thread_local, bstack111l111_opy_ (u"ࠨࡤࡤࡷࡪࡥࡡࡱࡲࡢࡥ࠶࠷ࡹࡠࡵࡦࡶ࡮ࡶࡴࠨ໽")):
            scripts = {bstack111l111_opy_ (u"ࠩࡶࡧࡦࡴࠧ໾"): bstack111lll1ll_opy_.perform_scan}
            thread_local.base_app_a11y_script = scripts
        bstack1l111ll11l_opy_ = copy.deepcopy(thread_local.base_app_a11y_script)
        bstack1l111ll11l_opy_[bstack111l111_opy_ (u"ࠪࡷࡨࡧ࡮ࠨ໿")] = bstack1l111ll11l_opy_[bstack111l111_opy_ (u"ࠫࡸࡩࡡ࡯ࠩༀ")] % json.dumps(bstack11lll1l111_opy_)
        bstack111lll1ll_opy_.bstack11lll111l_opy_(bstack1l111ll11l_opy_)
        bstack111lll1ll_opy_.store()
        bstack111l1l11l_opy_ = driver.execute_script(bstack111lll1ll_opy_.perform_scan)
      except Exception as bstack1llll1llll_opy_:
        logger.info(bstack111l111_opy_ (u"ࠧࡇࡰࡱ࡫ࡸࡱࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡣࡢࡰࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࠧ༁") + str(bstack1llll1llll_opy_))
        bstack111l1l11l_opy_ = {bstack111l111_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ༂"): str(bstack1llll1llll_opy_)}
    else:
      bstack111l1l11l_opy_ = driver.execute_async_script(bstack111lll1ll_opy_.perform_scan, {bstack111l111_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪࠧ༃"): kwargs.get(bstack111l111_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࡠࡥࡲࡱࡲࡧ࡮ࡥࠩ༄"), None) or bstack111l111_opy_ (u"ࠩࠪ༅")})
    return bstack111l1l11l_opy_
  except Exception as err:
    logger.error(bstack111l111_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡲࡶࡰࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮࠯ࠢࡾࢁࠧ༆").format(str(err)))
    return {}