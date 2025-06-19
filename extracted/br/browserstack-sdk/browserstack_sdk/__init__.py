# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
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
from browserstack_sdk.bstack1l1l1111l1_opy_ import bstack11111l11_opy_
from browserstack_sdk.bstack111l1l1ll_opy_ import *
import time
import requests
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.measure import measure
def bstack1l111111l_opy_():
  global CONFIG
  headers = {
        bstack111lll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack111lll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1llll1ll11_opy_(CONFIG, bstack11111l1l_opy_)
  try:
    response = requests.get(bstack11111l1l_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack11l11111l_opy_ = response.json()[bstack111lll_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1ll111l11_opy_.format(response.json()))
      return bstack11l11111l_opy_
    else:
      logger.debug(bstack1lll1l11l_opy_.format(bstack111lll_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack1lll1l11l_opy_.format(e))
def bstack11l1ll1l1_opy_(hub_url):
  global CONFIG
  url = bstack111lll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack111lll_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack111lll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack111lll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1llll1ll11_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack11l1l1l1l_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1lll1ll1_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack1l1llll1_opy_, stage=STAGE.bstack111ll11l1_opy_)
def bstack1ll111l1l1_opy_():
  try:
    global bstack11ll1111ll_opy_
    bstack11l11111l_opy_ = bstack1l111111l_opy_()
    bstack1l1l1l111l_opy_ = []
    results = []
    for bstack1ll111l1_opy_ in bstack11l11111l_opy_:
      bstack1l1l1l111l_opy_.append(bstack1l11llll1l_opy_(target=bstack11l1ll1l1_opy_,args=(bstack1ll111l1_opy_,)))
    for t in bstack1l1l1l111l_opy_:
      t.start()
    for t in bstack1l1l1l111l_opy_:
      results.append(t.join())
    bstack1l1lll1l11_opy_ = {}
    for item in results:
      hub_url = item[bstack111lll_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack111lll_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack1l1lll1l11_opy_[hub_url] = latency
    bstack1ll1111111_opy_ = min(bstack1l1lll1l11_opy_, key= lambda x: bstack1l1lll1l11_opy_[x])
    bstack11ll1111ll_opy_ = bstack1ll1111111_opy_
    logger.debug(bstack1ll1llll_opy_.format(bstack1ll1111111_opy_))
  except Exception as e:
    logger.debug(bstack1l111111_opy_.format(e))
from browserstack_sdk.bstack1l1l1lllll_opy_ import *
from browserstack_sdk.bstack1l11111l1_opy_ import *
from browserstack_sdk.bstack1l1111l1l_opy_ import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.bstack1111ll111_opy_ import get_logger
from bstack_utils.measure import measure
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack1l11111l11_opy_, stage=STAGE.bstack111ll11l1_opy_)
def bstack1l111ll1l1_opy_():
    global bstack11ll1111ll_opy_
    try:
        bstack1l1ll1l1l1_opy_ = bstack1l111ll111_opy_()
        bstack1l1l1lll_opy_(bstack1l1ll1l1l1_opy_)
        hub_url = bstack1l1ll1l1l1_opy_.get(bstack111lll_opy_ (u"ࠨࡵࡳ࡮ࠥࢀ"), bstack111lll_opy_ (u"ࠢࠣࢁ"))
        if hub_url.endswith(bstack111lll_opy_ (u"ࠨ࠱ࡺࡨ࠴࡮ࡵࡣࠩࢂ")):
            hub_url = hub_url.rsplit(bstack111lll_opy_ (u"ࠩ࠲ࡻࡩ࠵ࡨࡶࡤࠪࢃ"), 1)[0]
        if hub_url.startswith(bstack111lll_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫࢄ")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack111lll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࠭ࢅ")):
            hub_url = hub_url[8:]
        bstack11ll1111ll_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack1l111ll111_opy_():
    global CONFIG
    bstack1ll1l11111_opy_ = CONFIG.get(bstack111lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢆ"), {}).get(bstack111lll_opy_ (u"࠭ࡧࡳ࡫ࡧࡒࡦࡳࡥࠨࢇ"), bstack111lll_opy_ (u"ࠧࡏࡑࡢࡋࡗࡏࡄࡠࡐࡄࡑࡊࡥࡐࡂࡕࡖࡉࡉ࠭࢈"))
    if not isinstance(bstack1ll1l11111_opy_, str):
        raise ValueError(bstack111lll_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡈࡴ࡬ࡨࠥࡴࡡ࡮ࡧࠣࡱࡺࡹࡴࠡࡤࡨࠤࡦࠦࡶࡢ࡮࡬ࡨࠥࡹࡴࡳ࡫ࡱ࡫ࠧࢉ"))
    try:
        bstack1l1ll1l1l1_opy_ = bstack1l111lllll_opy_(bstack1ll1l11111_opy_)
        return bstack1l1ll1l1l1_opy_
    except Exception as e:
        logger.error(bstack111lll_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣࢊ").format(str(e)))
        return {}
def bstack1l111lllll_opy_(bstack1ll1l11111_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack111lll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࢋ")] or not CONFIG[bstack111lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧࢌ")]:
            raise ValueError(bstack111lll_opy_ (u"ࠧࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠠࡰࡴࠣࡥࡨࡩࡥࡴࡵࠣ࡯ࡪࡿࠢࢍ"))
        url = bstack1l111ll11l_opy_ + bstack1ll1l11111_opy_
        auth = (CONFIG[bstack111lll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨࢎ")], CONFIG[bstack111lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ࢏")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack1l11l1llll_opy_ = json.loads(response.text)
            return bstack1l11l1llll_opy_
    except ValueError as ve:
        logger.error(bstack111lll_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣ࢐").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack111lll_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥ࡭ࡲࡪࡦࠣࡨࡪࡺࡡࡪ࡮ࡶࠤ࠿ࠦࡻࡾࠤ࢑").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack1l1l1lll_opy_(bstack1l1111ll_opy_):
    global CONFIG
    if bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ࢒") not in CONFIG or str(CONFIG[bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ࢓")]).lower() == bstack111lll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ࢔"):
        CONFIG[bstack111lll_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬ࢕")] = False
    elif bstack111lll_opy_ (u"ࠧࡪࡵࡗࡶ࡮ࡧ࡬ࡈࡴ࡬ࡨࠬ࢖") in bstack1l1111ll_opy_:
        bstack11l1l1l111_opy_ = CONFIG.get(bstack111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢗ"), {})
        logger.debug(bstack111lll_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡰࡴࡩࡡ࡭ࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࠪࡹࠢ࢘"), bstack11l1l1l111_opy_)
        bstack1l1lll1lll_opy_ = bstack1l1111ll_opy_.get(bstack111lll_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡕࡩࡵ࡫ࡡࡵࡧࡵࡷ࢙ࠧ"), [])
        bstack11lll111_opy_ = bstack111lll_opy_ (u"ࠦ࠱ࠨ࢚").join(bstack1l1lll1lll_opy_)
        logger.debug(bstack111lll_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡈࡻࡳࡵࡱࡰࠤࡷ࡫ࡰࡦࡣࡷࡩࡷࠦࡳࡵࡴ࡬ࡲ࡬ࡀࠠࠦࡵ࢛ࠥ"), bstack11lll111_opy_)
        bstack11111lll_opy_ = {
            bstack111lll_opy_ (u"ࠨ࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣ࢜"): bstack111lll_opy_ (u"ࠢࡢࡶࡶ࠱ࡷ࡫ࡰࡦࡣࡷࡩࡷࠨ࢝"),
            bstack111lll_opy_ (u"ࠣࡨࡲࡶࡨ࡫ࡌࡰࡥࡤࡰࠧ࢞"): bstack111lll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ࢟"),
            bstack111lll_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠧࢠ"): bstack11lll111_opy_
        }
        bstack11l1l1l111_opy_.update(bstack11111lll_opy_)
        logger.debug(bstack111lll_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼࡙ࠣࡵࡪࡡࡵࡧࡧࠤࡱࡵࡣࡢ࡮ࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࠫࡳࠣࢡ"), bstack11l1l1l111_opy_)
        CONFIG[bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢢ")] = bstack11l1l1l111_opy_
        logger.debug(bstack111lll_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡌࡩ࡯ࡣ࡯ࠤࡈࡕࡎࡇࡋࡊ࠾ࠥࠫࡳࠣࢣ"), CONFIG)
def bstack1ll1111lll_opy_():
    bstack1l1ll1l1l1_opy_ = bstack1l111ll111_opy_()
    if not bstack1l1ll1l1l1_opy_[bstack111lll_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࡙ࡷࡲࠧࢤ")]:
      raise ValueError(bstack111lll_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࡚ࡸ࡬ࠡ࡫ࡶࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࡬ࡲࡰ࡯ࠣ࡫ࡷ࡯ࡤࠡࡦࡨࡸࡦ࡯࡬ࡴ࠰ࠥࢥ"))
    return bstack1l1ll1l1l1_opy_[bstack111lll_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࡛ࡲ࡭ࠩࢦ")] + bstack111lll_opy_ (u"ࠪࡃࡨࡧࡰࡴ࠿ࠪࢧ")
@measure(event_name=EVENTS.bstack11l11lll11_opy_, stage=STAGE.bstack111ll11l1_opy_)
def bstack11lll1l1l1_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack111lll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ࢨ")], CONFIG[bstack111lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࢩ")])
        url = bstack1l1ll11lll_opy_
        logger.debug(bstack111lll_opy_ (u"ࠨࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬ࡲࡰ࡯ࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡗࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࠦࡁࡑࡋࠥࢪ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack111lll_opy_ (u"ࠢࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪࠨࢫ"): bstack111lll_opy_ (u"ࠣࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠦࢬ")})
            if response.status_code == 200:
                bstack11ll1ll111_opy_ = json.loads(response.text)
                bstack1l11l11l1_opy_ = bstack11ll1ll111_opy_.get(bstack111lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡴࠩࢭ"), [])
                if bstack1l11l11l1_opy_:
                    bstack11llllllll_opy_ = bstack1l11l11l1_opy_[0]
                    build_hashed_id = bstack11llllllll_opy_.get(bstack111lll_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ࢮ"))
                    bstack1l111lll1_opy_ = bstack1l111l11l1_opy_ + build_hashed_id
                    result.extend([build_hashed_id, bstack1l111lll1_opy_])
                    logger.info(bstack1ll1111l_opy_.format(bstack1l111lll1_opy_))
                    bstack11l111l1l_opy_ = CONFIG[bstack111lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧࢯ")]
                    if bstack111lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢰ") in CONFIG:
                      bstack11l111l1l_opy_ += bstack111lll_opy_ (u"࠭ࠠࠨࢱ") + CONFIG[bstack111lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࢲ")]
                    if bstack11l111l1l_opy_ != bstack11llllllll_opy_.get(bstack111lll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ࢳ")):
                      logger.debug(bstack1lll1l1l1l_opy_.format(bstack11llllllll_opy_.get(bstack111lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧࢴ")), bstack11l111l1l_opy_))
                    return result
                else:
                    logger.debug(bstack111lll_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡑࡳࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡵࡪࡨࠤࡷ࡫ࡳࡱࡱࡱࡷࡪ࠴ࠢࢵ"))
            else:
                logger.debug(bstack111lll_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢶ"))
        except Exception as e:
            logger.error(bstack111lll_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࡹࠠ࠻ࠢࡾࢁࠧࢷ").format(str(e)))
    else:
        logger.debug(bstack111lll_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡉࡏࡏࡈࡌࡋࠥ࡯ࡳࠡࡰࡲࡸࠥࡹࡥࡵ࠰࡙ࠣࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢸ"))
    return [None, None]
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1l1ll11ll_opy_ import bstack1l1ll11ll_opy_, bstack11ll1l111_opy_, bstack1ll11l11_opy_, bstack11ll1111l_opy_
from bstack_utils.measure import bstack1ll1l111ll_opy_
from bstack_utils.measure import measure
from bstack_utils.percy import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1ll1lll1l_opy_ import bstack1llll11l_opy_
from bstack_utils.messages import *
from bstack_utils import bstack1111ll111_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1ll1l1111_opy_, bstack1l1ll1l111_opy_, bstack111llll1l_opy_, bstack1ll11l1l1l_opy_, \
  bstack1l1l111l1_opy_, \
  Notset, bstack1ll1lll1ll_opy_, \
  bstack111111l1l_opy_, bstack1ll11l11l1_opy_, bstack1l111ll11_opy_, bstack1lll111lll_opy_, bstack111ll111_opy_, bstack1l1l1l1l1l_opy_, \
  bstack1l1ll1l1_opy_, \
  bstack11l1l11ll_opy_, bstack1lllll111l_opy_, bstack111l11lll_opy_, bstack1111ll1ll_opy_, \
  bstack11l111ll1_opy_, bstack1l1111lll1_opy_, bstack1ll111ll1_opy_, bstack1lll1ll111_opy_
from bstack_utils.bstack11l111l1_opy_ import bstack11l1l111_opy_
from bstack_utils.bstack1ll11llll1_opy_ import bstack11l111ll1l_opy_, bstack1l11ll1lll_opy_
from bstack_utils.bstack1l1ll11l11_opy_ import bstack1llll1l1l_opy_
from bstack_utils.bstack111ll1ll_opy_ import bstack1lll11l1ll_opy_, bstack1l1ll1ll11_opy_
from bstack_utils.bstack11ll1l1ll_opy_ import bstack11ll1l1ll_opy_
from bstack_utils.bstack1l11l11l_opy_ import bstack11ll111l_opy_
from bstack_utils.proxy import bstack11l111l11l_opy_, bstack1llll1ll11_opy_, bstack11l1l1lll_opy_, bstack1l11lllll1_opy_
from bstack_utils.bstack1lll1l1111_opy_ import bstack1l1lll11l_opy_
import bstack_utils.bstack11l111lll_opy_ as bstack1lll1l1l_opy_
import bstack_utils.bstack1llll1lll_opy_ as bstack111111l1_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.utils.bstack1ll1ll111_opy_ import bstack1lllllll1l_opy_
from bstack_utils.bstack1ll1ll1l_opy_ import bstack1lllll1l11_opy_
from bstack_utils.bstack1l11l1l1l_opy_ import bstack1111ll1l1_opy_
if os.getenv(bstack111lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡌࡔࡕࡋࡔࠩࢹ")):
  cli.bstack1ll1l1l11l_opy_()
else:
  os.environ[bstack111lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡍࡕࡏࡌࡕࠪࢺ")] = bstack111lll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧࢻ")
bstack111l1ll11_opy_ = bstack111lll_opy_ (u"ࠪࠤࠥ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࠣࠤ࡮࡬ࠨࡱࡣࡪࡩࠥࡃ࠽࠾ࠢࡹࡳ࡮ࡪࠠ࠱ࠫࠣࡿࡡࡴࠠࠡࠢࡷࡶࡾࢁ࡜࡯ࠢࡦࡳࡳࡹࡴࠡࡨࡶࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨ࡝ࠩࡩࡷࡡ࠭ࠩ࠼࡞ࡱࠤࠥࠦࠠࠡࡨࡶ࠲ࡦࡶࡰࡦࡰࡧࡊ࡮ࡲࡥࡔࡻࡱࡧ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪ࠯ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡶ࡟ࡪࡰࡧࡩࡽ࠯ࠠࠬࠢࠥ࠾ࠧࠦࠫࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࠨࡢࡹࡤ࡭ࡹࠦ࡮ࡦࡹࡓࡥ࡬࡫࠲࠯ࡧࡹࡥࡱࡻࡡࡵࡧࠫࠦ࠭࠯ࠠ࠾ࡀࠣࡿࢂࠨࠬࠡ࡞ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥ࡫ࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡄࡦࡶࡤ࡭ࡱࡹࠢࡾ࡞ࠪ࠭࠮࠯࡛ࠣࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠦࡢ࠯ࠠࠬࠢࠥ࠰ࡡࡢ࡮ࠣࠫ࡟ࡲࠥࠦࠠࠡࡿࡦࡥࡹࡩࡨࠩࡧࡻ࠭ࢀࡢ࡮ࠡࠢࠣࠤࢂࡢ࡮ࠡࠢࢀࡠࡳࠦࠠ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱ࠪࢼ")
bstack1lllll1ll1_opy_ = bstack111lll_opy_ (u"ࠫࡡࡴ࠯ࠫࠢࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࠦࠪ࠰࡞ࡱࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠶ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡩࡡࡱࡵࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠷࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡲࡢ࡭ࡳࡪࡥࡹࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠷ࡣ࡜࡯ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯ࡵ࡯࡭ࡨ࡫ࠨ࠱࠮ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸࠯࡜࡯ࡥࡲࡲࡸࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯ࠥࡃࠠࡳࡧࡴࡹ࡮ࡸࡥࠩࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨࠩ࠼࡞ࡱ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡰࡦࡻ࡮ࡤࡪࠣࡁࠥࡧࡳࡺࡰࡦࠤ࠭ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷ࠮ࠦ࠽࠿ࠢࡾࡠࡳࡲࡥࡵࠢࡦࡥࡵࡹ࠻࡝ࡰࡷࡶࡾࠦࡻ࡝ࡰࡦࡥࡵࡹࠠ࠾ࠢࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࡢࡴࡶࡤࡧࡰࡥࡣࡢࡲࡶ࠭ࡡࡴࠠࠡࡿࠣࡧࡦࡺࡣࡩࠪࡨࡼ࠮ࠦࡻ࡝ࡰࠣࠤࠥࠦࡽ࡝ࡰࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࠻ࠢࡣࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠩࢁࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭ࢂࡦࠬ࡝ࡰࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴ࡞ࡱࠤࠥࢃࠩ࡝ࡰࢀࡠࡳ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࠪࢽ")
from ._version import __version__
bstack11l1ll1l_opy_ = None
CONFIG = {}
bstack11lll1llll_opy_ = {}
bstack11lll1111_opy_ = {}
bstack1l11ll11l1_opy_ = None
bstack1ll11111l1_opy_ = None
bstack11l1l1llll_opy_ = None
bstack11l1l11ll1_opy_ = -1
bstack111ll1ll1_opy_ = 0
bstack11llll1lll_opy_ = bstack11llll111_opy_
bstack11l1ll1l1l_opy_ = 1
bstack1lllll111_opy_ = False
bstack1ll11ll11_opy_ = False
bstack1lllll11l_opy_ = bstack111lll_opy_ (u"ࠬ࠭ࢾ")
bstack1l1lll11l1_opy_ = bstack111lll_opy_ (u"࠭ࠧࢿ")
bstack11lll111l_opy_ = False
bstack111lll111_opy_ = True
bstack1111l11l_opy_ = bstack111lll_opy_ (u"ࠧࠨࣀ")
bstack1ll11111l_opy_ = []
bstack11ll1111ll_opy_ = bstack111lll_opy_ (u"ࠨࠩࣁ")
bstack1lll1111_opy_ = False
bstack1l1l1l1ll1_opy_ = None
bstack11l11l1ll_opy_ = None
bstack11l11llll1_opy_ = None
bstack1l1l11llll_opy_ = -1
bstack111llll1_opy_ = os.path.join(os.path.expanduser(bstack111lll_opy_ (u"ࠩࢁࠫࣂ")), bstack111lll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪࣃ"), bstack111lll_opy_ (u"ࠫ࠳ࡸ࡯ࡣࡱࡷ࠱ࡷ࡫ࡰࡰࡴࡷ࠱࡭࡫࡬ࡱࡧࡵ࠲࡯ࡹ࡯࡯ࠩࣄ"))
bstack1ll1ll1ll1_opy_ = 0
bstack1llll11ll1_opy_ = 0
bstack1l111llll_opy_ = []
bstack11ll11l1_opy_ = []
bstack1l11lll11_opy_ = []
bstack1ll111111_opy_ = []
bstack1l1l1l1l_opy_ = bstack111lll_opy_ (u"ࠬ࠭ࣅ")
bstack11ll11ll1_opy_ = bstack111lll_opy_ (u"࠭ࠧࣆ")
bstack1l11ll111l_opy_ = False
bstack11l11ll11_opy_ = False
bstack1111llll_opy_ = {}
bstack1l1l11111l_opy_ = None
bstack1l1ll11111_opy_ = None
bstack1l1l111ll_opy_ = None
bstack1lll11lll1_opy_ = None
bstack11ll1l111l_opy_ = None
bstack11lll111ll_opy_ = None
bstack1ll1l11lll_opy_ = None
bstack11ll1llll_opy_ = None
bstack11lll1l11l_opy_ = None
bstack11l1ll11_opy_ = None
bstack1l111l1l1_opy_ = None
bstack1l1111l1ll_opy_ = None
bstack11l11l1lll_opy_ = None
bstack1llll11ll_opy_ = None
bstack1ll11ll1l_opy_ = None
bstack1ll1l11ll1_opy_ = None
bstack1l1111l1_opy_ = None
bstack11ll111l1_opy_ = None
bstack1ll11l1111_opy_ = None
bstack1l111l111_opy_ = None
bstack11l1l11l1l_opy_ = None
bstack1lll1lllll_opy_ = None
bstack11lllll1l_opy_ = None
thread_local = threading.local()
bstack1l1l1l1l1_opy_ = False
bstack1l11ll111_opy_ = bstack111lll_opy_ (u"ࠢࠣࣇ")
logger = bstack1111ll111_opy_.get_logger(__name__, bstack11llll1lll_opy_)
bstack1ll1l11ll_opy_ = Config.bstack1ll11lll1l_opy_()
percy = bstack11l1ll1l11_opy_()
bstack1l1ll1ll1_opy_ = bstack1llll11l_opy_()
bstack1llllll11_opy_ = bstack1l1111l1l_opy_()
def bstack1l11l1l111_opy_():
  global CONFIG
  global bstack1l11ll111l_opy_
  global bstack1ll1l11ll_opy_
  testContextOptions = bstack1llllll11l_opy_(CONFIG)
  if bstack1l1l111l1_opy_(CONFIG):
    if (bstack111lll_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪࣈ") in testContextOptions and str(testContextOptions[bstack111lll_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫࣉ")]).lower() == bstack111lll_opy_ (u"ࠪࡸࡷࡻࡥࠨ࣊")):
      bstack1l11ll111l_opy_ = True
    bstack1ll1l11ll_opy_.bstack11ll111ll1_opy_(testContextOptions.get(bstack111lll_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ࣋"), False))
  else:
    bstack1l11ll111l_opy_ = True
    bstack1ll1l11ll_opy_.bstack11ll111ll1_opy_(True)
def bstack1l11l1111l_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack11l1ll1ll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l11ll11_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack111lll_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡩ࡯࡯ࡨ࡬࡫࡫࡯࡬ࡦࠤ࣌") == args[i].lower() or bstack111lll_opy_ (u"ࠨ࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡪ࡮࡭ࠢ࣍") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1111l11l_opy_
      bstack1111l11l_opy_ += bstack111lll_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠤࠬ࣎") + path
      return path
  return None
bstack11l1111l1l_opy_ = re.compile(bstack111lll_opy_ (u"ࡳࠤ࠱࠮ࡄࡢࠤࡼࠪ࠱࠮ࡄ࠯ࡽ࠯ࠬࡂ࣏ࠦ"))
def bstack1l11ll1ll1_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack11l1111l1l_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack111lll_opy_ (u"ࠤࠧࡿ࣐ࠧ") + group + bstack111lll_opy_ (u"ࠥࢁ࣑ࠧ"), os.environ.get(group))
  return value
def bstack1ll11ll1_opy_():
  global bstack11lllll1l_opy_
  if bstack11lllll1l_opy_ is None:
        bstack11lllll1l_opy_ = bstack1l11ll11_opy_()
  bstack1ll1llll1l_opy_ = bstack11lllll1l_opy_
  if bstack1ll1llll1l_opy_ and os.path.exists(os.path.abspath(bstack1ll1llll1l_opy_)):
    fileName = bstack1ll1llll1l_opy_
  if bstack111lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ࣒") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack111lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆ࣓ࠩ")])) and not bstack111lll_opy_ (u"࠭ࡦࡪ࡮ࡨࡒࡦࡳࡥࠨࣔ") in locals():
    fileName = os.environ[bstack111lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫࣕ")]
  if bstack111lll_opy_ (u"ࠨࡨ࡬ࡰࡪࡔࡡ࡮ࡧࠪࣖ") in locals():
    bstack11ll1_opy_ = os.path.abspath(fileName)
  else:
    bstack11ll1_opy_ = bstack111lll_opy_ (u"ࠩࠪࣗ")
  bstack11l11l11ll_opy_ = os.getcwd()
  bstack11llllll_opy_ = bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ࣘ")
  bstack1ll1l1ll_opy_ = bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡦࡳ࡬ࠨࣙ")
  while (not os.path.exists(bstack11ll1_opy_)) and bstack11l11l11ll_opy_ != bstack111lll_opy_ (u"ࠧࠨࣚ"):
    bstack11ll1_opy_ = os.path.join(bstack11l11l11ll_opy_, bstack11llllll_opy_)
    if not os.path.exists(bstack11ll1_opy_):
      bstack11ll1_opy_ = os.path.join(bstack11l11l11ll_opy_, bstack1ll1l1ll_opy_)
    if bstack11l11l11ll_opy_ != os.path.dirname(bstack11l11l11ll_opy_):
      bstack11l11l11ll_opy_ = os.path.dirname(bstack11l11l11ll_opy_)
    else:
      bstack11l11l11ll_opy_ = bstack111lll_opy_ (u"ࠨࠢࣛ")
  bstack11lllll1l_opy_ = bstack11ll1_opy_ if os.path.exists(bstack11ll1_opy_) else None
  return bstack11lllll1l_opy_
def bstack1lll11l111_opy_():
  bstack11ll1_opy_ = bstack1ll11ll1_opy_()
  if not os.path.exists(bstack11ll1_opy_):
    bstack11l11111_opy_(
      bstack1l11llll1_opy_.format(os.getcwd()))
  try:
    with open(bstack11ll1_opy_, bstack111lll_opy_ (u"ࠧࡳࠩࣜ")) as stream:
      yaml.add_implicit_resolver(bstack111lll_opy_ (u"ࠣࠣࡳࡥࡹ࡮ࡥࡹࠤࣝ"), bstack11l1111l1l_opy_)
      yaml.add_constructor(bstack111lll_opy_ (u"ࠤࠤࡴࡦࡺࡨࡦࡺࠥࣞ"), bstack1l11ll1ll1_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack11ll1_opy_, bstack111lll_opy_ (u"ࠪࡶࠬࣟ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack11l11111_opy_(bstack1lll1111ll_opy_.format(str(exc)))
def bstack1l111l11l_opy_(config):
  bstack111ll1l1_opy_ = bstack11ll1111_opy_(config)
  for option in list(bstack111ll1l1_opy_):
    if option.lower() in bstack1111ll11_opy_ and option != bstack1111ll11_opy_[option.lower()]:
      bstack111ll1l1_opy_[bstack1111ll11_opy_[option.lower()]] = bstack111ll1l1_opy_[option]
      del bstack111ll1l1_opy_[option]
  return config
def bstack1lllll11_opy_():
  global bstack11lll1111_opy_
  for key, bstack11l111l11_opy_ in bstack1111l11l1_opy_.items():
    if isinstance(bstack11l111l11_opy_, list):
      for var in bstack11l111l11_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack11lll1111_opy_[key] = os.environ[var]
          break
    elif bstack11l111l11_opy_ in os.environ and os.environ[bstack11l111l11_opy_] and str(os.environ[bstack11l111l11_opy_]).strip():
      bstack11lll1111_opy_[key] = os.environ[bstack11l111l11_opy_]
  if bstack111lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭࣠") in os.environ:
    bstack11lll1111_opy_[bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ࣡")] = {}
    bstack11lll1111_opy_[bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ࣢")][bstack111lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࣣࠩ")] = os.environ[bstack111lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪࣤ")]
def bstack1llll1l11_opy_():
  global bstack11lll1llll_opy_
  global bstack1111l11l_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack111lll_opy_ (u"ࠩ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣥ").lower() == val.lower():
      bstack11lll1llll_opy_[bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࣦࠧ")] = {}
      bstack11lll1llll_opy_[bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣧ")][bstack111lll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣨ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack11ll11lll_opy_ in bstack1l11l1ll1_opy_.items():
    if isinstance(bstack11ll11lll_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack11ll11lll_opy_:
          if idx < len(sys.argv) and bstack111lll_opy_ (u"࠭࠭࠮ࣩࠩ") + var.lower() == val.lower() and not key in bstack11lll1llll_opy_:
            bstack11lll1llll_opy_[key] = sys.argv[idx + 1]
            bstack1111l11l_opy_ += bstack111lll_opy_ (u"ࠧࠡ࠯࠰ࠫ࣪") + var + bstack111lll_opy_ (u"ࠨࠢࠪ࣫") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack111lll_opy_ (u"ࠩ࠰࠱ࠬ࣬") + bstack11ll11lll_opy_.lower() == val.lower() and not key in bstack11lll1llll_opy_:
          bstack11lll1llll_opy_[key] = sys.argv[idx + 1]
          bstack1111l11l_opy_ += bstack111lll_opy_ (u"ࠪࠤ࠲࠳࣭ࠧ") + bstack11ll11lll_opy_ + bstack111lll_opy_ (u"࣮ࠫࠥ࠭") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1lllllll1_opy_(config):
  bstack11lll1ll1_opy_ = config.keys()
  for bstack1ll1l1ll1l_opy_, bstack111l1111_opy_ in bstack11ll1l1l1l_opy_.items():
    if bstack111l1111_opy_ in bstack11lll1ll1_opy_:
      config[bstack1ll1l1ll1l_opy_] = config[bstack111l1111_opy_]
      del config[bstack111l1111_opy_]
  for bstack1ll1l1ll1l_opy_, bstack111l1111_opy_ in bstack1lll1l1l11_opy_.items():
    if isinstance(bstack111l1111_opy_, list):
      for bstack1ll11111_opy_ in bstack111l1111_opy_:
        if bstack1ll11111_opy_ in bstack11lll1ll1_opy_:
          config[bstack1ll1l1ll1l_opy_] = config[bstack1ll11111_opy_]
          del config[bstack1ll11111_opy_]
          break
    elif bstack111l1111_opy_ in bstack11lll1ll1_opy_:
      config[bstack1ll1l1ll1l_opy_] = config[bstack111l1111_opy_]
      del config[bstack111l1111_opy_]
  for bstack1ll11111_opy_ in list(config):
    for bstack11l111llll_opy_ in bstack1l11ll1l11_opy_:
      if bstack1ll11111_opy_.lower() == bstack11l111llll_opy_.lower() and bstack1ll11111_opy_ != bstack11l111llll_opy_:
        config[bstack11l111llll_opy_] = config[bstack1ll11111_opy_]
        del config[bstack1ll11111_opy_]
  bstack1ll11l1l1_opy_ = [{}]
  if not config.get(bstack111lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ࣯")):
    config[bstack111lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࣰࠩ")] = [{}]
  bstack1ll11l1l1_opy_ = config[bstack111lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࣱࠪ")]
  for platform in bstack1ll11l1l1_opy_:
    for bstack1ll11111_opy_ in list(platform):
      for bstack11l111llll_opy_ in bstack1l11ll1l11_opy_:
        if bstack1ll11111_opy_.lower() == bstack11l111llll_opy_.lower() and bstack1ll11111_opy_ != bstack11l111llll_opy_:
          platform[bstack11l111llll_opy_] = platform[bstack1ll11111_opy_]
          del platform[bstack1ll11111_opy_]
  for bstack1ll1l1ll1l_opy_, bstack111l1111_opy_ in bstack1lll1l1l11_opy_.items():
    for platform in bstack1ll11l1l1_opy_:
      if isinstance(bstack111l1111_opy_, list):
        for bstack1ll11111_opy_ in bstack111l1111_opy_:
          if bstack1ll11111_opy_ in platform:
            platform[bstack1ll1l1ll1l_opy_] = platform[bstack1ll11111_opy_]
            del platform[bstack1ll11111_opy_]
            break
      elif bstack111l1111_opy_ in platform:
        platform[bstack1ll1l1ll1l_opy_] = platform[bstack111l1111_opy_]
        del platform[bstack111l1111_opy_]
  for bstack11lllll1_opy_ in bstack11l1l111l_opy_:
    if bstack11lllll1_opy_ in config:
      if not bstack11l1l111l_opy_[bstack11lllll1_opy_] in config:
        config[bstack11l1l111l_opy_[bstack11lllll1_opy_]] = {}
      config[bstack11l1l111l_opy_[bstack11lllll1_opy_]].update(config[bstack11lllll1_opy_])
      del config[bstack11lllll1_opy_]
  for platform in bstack1ll11l1l1_opy_:
    for bstack11lllll1_opy_ in bstack11l1l111l_opy_:
      if bstack11lllll1_opy_ in list(platform):
        if not bstack11l1l111l_opy_[bstack11lllll1_opy_] in platform:
          platform[bstack11l1l111l_opy_[bstack11lllll1_opy_]] = {}
        platform[bstack11l1l111l_opy_[bstack11lllll1_opy_]].update(platform[bstack11lllll1_opy_])
        del platform[bstack11lllll1_opy_]
  config = bstack1l111l11l_opy_(config)
  return config
def bstack11llll11l1_opy_(config):
  global bstack1l1lll11l1_opy_
  bstack1ll1ll11ll_opy_ = False
  if bstack111lll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࣲࠬ") in config and str(config[bstack111lll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ࣳ")]).lower() != bstack111lll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩࣴ"):
    if bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨࣵ") not in config or str(config[bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࣶࠩ")]).lower() == bstack111lll_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬࣷ"):
      config[bstack111lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭ࣸ")] = False
    else:
      bstack1l1ll1l1l1_opy_ = bstack1l111ll111_opy_()
      if bstack111lll_opy_ (u"ࠨ࡫ࡶࡘࡷ࡯ࡡ࡭ࡉࡵ࡭ࡩࣹ࠭") in bstack1l1ll1l1l1_opy_:
        if not bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸࣺ࠭") in config:
          config[bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࣻ")] = {}
        config[bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣼ")][bstack111lll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣽ")] = bstack111lll_opy_ (u"࠭ࡡࡵࡵ࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠬࣾ")
        bstack1ll1ll11ll_opy_ = True
        bstack1l1lll11l1_opy_ = config[bstack111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࣿ")].get(bstack111lll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪऀ"))
  if bstack1l1l111l1_opy_(config) and bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ँ") in config and str(config[bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧं")]).lower() != bstack111lll_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪः") and not bstack1ll1ll11ll_opy_:
    if not bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩऄ") in config:
      config[bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪअ")] = {}
    if not config[bstack111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫआ")].get(bstack111lll_opy_ (u"ࠨࡵ࡮࡭ࡵࡈࡩ࡯ࡣࡵࡽࡎࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡡࡵ࡫ࡲࡲࠬइ")) and not bstack111lll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫई") in config[bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧउ")]:
      bstack1llllllll1_opy_ = datetime.datetime.now()
      bstack1llll1l1l1_opy_ = bstack1llllllll1_opy_.strftime(bstack111lll_opy_ (u"ࠫࠪࡪ࡟ࠦࡤࡢࠩࡍࠫࡍࠨऊ"))
      hostname = socket.gethostname()
      bstack111llllll_opy_ = bstack111lll_opy_ (u"ࠬ࠭ऋ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack111lll_opy_ (u"࠭ࡻࡾࡡࡾࢁࡤࢁࡽࠨऌ").format(bstack1llll1l1l1_opy_, hostname, bstack111llllll_opy_)
      config[bstack111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫऍ")][bstack111lll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪऎ")] = identifier
    bstack1l1lll11l1_opy_ = config[bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ए")].get(bstack111lll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬऐ"))
  return config
def bstack1l11llll11_opy_():
  bstack1l1ll11l1l_opy_ =  bstack1lll111lll_opy_()[bstack111lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠪऑ")]
  return bstack1l1ll11l1l_opy_ if bstack1l1ll11l1l_opy_ else -1
def bstack11l1l1l11l_opy_(bstack1l1ll11l1l_opy_):
  global CONFIG
  if not bstack111lll_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧऒ") in CONFIG[bstack111lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨओ")]:
    return
  CONFIG[bstack111lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऔ")] = CONFIG[bstack111lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪक")].replace(
    bstack111lll_opy_ (u"ࠩࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫख"),
    str(bstack1l1ll11l1l_opy_)
  )
def bstack111l11ll1_opy_():
  global CONFIG
  if not bstack111lll_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾࠩग") in CONFIG[bstack111lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭घ")]:
    return
  bstack1llllllll1_opy_ = datetime.datetime.now()
  bstack1llll1l1l1_opy_ = bstack1llllllll1_opy_.strftime(bstack111lll_opy_ (u"ࠬࠫࡤ࠮ࠧࡥ࠱ࠪࡎ࠺ࠦࡏࠪङ"))
  CONFIG[bstack111lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨच")] = CONFIG[bstack111lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩछ")].replace(
    bstack111lll_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧज"),
    bstack1llll1l1l1_opy_
  )
def bstack11ll1l1l1_opy_():
  global CONFIG
  if bstack111lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫझ") in CONFIG and not bool(CONFIG[bstack111lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬञ")]):
    del CONFIG[bstack111lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ट")]
    return
  if not bstack111lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧठ") in CONFIG:
    CONFIG[bstack111lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨड")] = bstack111lll_opy_ (u"ࠧࠤࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪढ")
  if bstack111lll_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧण") in CONFIG[bstack111lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫत")]:
    bstack111l11ll1_opy_()
    os.environ[bstack111lll_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧथ")] = CONFIG[bstack111lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭द")]
  if not bstack111lll_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧध") in CONFIG[bstack111lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨन")]:
    return
  bstack1l1ll11l1l_opy_ = bstack111lll_opy_ (u"ࠧࠨऩ")
  bstack1l1ll11l1_opy_ = bstack1l11llll11_opy_()
  if bstack1l1ll11l1_opy_ != -1:
    bstack1l1ll11l1l_opy_ = bstack111lll_opy_ (u"ࠨࡅࡌࠤࠬप") + str(bstack1l1ll11l1_opy_)
  if bstack1l1ll11l1l_opy_ == bstack111lll_opy_ (u"ࠩࠪफ"):
    bstack11l1l1l1l1_opy_ = bstack11llll1l11_opy_(CONFIG[bstack111lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ब")])
    if bstack11l1l1l1l1_opy_ != -1:
      bstack1l1ll11l1l_opy_ = str(bstack11l1l1l1l1_opy_)
  if bstack1l1ll11l1l_opy_:
    bstack11l1l1l11l_opy_(bstack1l1ll11l1l_opy_)
    os.environ[bstack111lll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨभ")] = CONFIG[bstack111lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧम")]
def bstack1l11lllll_opy_(bstack1l1ll11ll1_opy_, bstack1l111111l1_opy_, path):
  bstack11l1l1111l_opy_ = {
    bstack111lll_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪय"): bstack1l111111l1_opy_
  }
  if os.path.exists(path):
    bstack11l1l1l1_opy_ = json.load(open(path, bstack111lll_opy_ (u"ࠧࡳࡤࠪर")))
  else:
    bstack11l1l1l1_opy_ = {}
  bstack11l1l1l1_opy_[bstack1l1ll11ll1_opy_] = bstack11l1l1111l_opy_
  with open(path, bstack111lll_opy_ (u"ࠣࡹ࠮ࠦऱ")) as outfile:
    json.dump(bstack11l1l1l1_opy_, outfile)
def bstack11llll1l11_opy_(bstack1l1ll11ll1_opy_):
  bstack1l1ll11ll1_opy_ = str(bstack1l1ll11ll1_opy_)
  bstack11lllllll_opy_ = os.path.join(os.path.expanduser(bstack111lll_opy_ (u"ࠩࢁࠫल")), bstack111lll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪळ"))
  try:
    if not os.path.exists(bstack11lllllll_opy_):
      os.makedirs(bstack11lllllll_opy_)
    file_path = os.path.join(os.path.expanduser(bstack111lll_opy_ (u"ࠫࢃ࠭ऴ")), bstack111lll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬव"), bstack111lll_opy_ (u"࠭࠮ࡣࡷ࡬ࡰࡩ࠳࡮ࡢ࡯ࡨ࠱ࡨࡧࡣࡩࡧ࠱࡮ࡸࡵ࡮ࠨश"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack111lll_opy_ (u"ࠧࡸࠩष")):
        pass
      with open(file_path, bstack111lll_opy_ (u"ࠣࡹ࠮ࠦस")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack111lll_opy_ (u"ࠩࡵࠫह")) as bstack1l1lll1l_opy_:
      bstack11ll1ll11l_opy_ = json.load(bstack1l1lll1l_opy_)
    if bstack1l1ll11ll1_opy_ in bstack11ll1ll11l_opy_:
      bstack1llll1l11l_opy_ = bstack11ll1ll11l_opy_[bstack1l1ll11ll1_opy_][bstack111lll_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऺ")]
      bstack1l1ll1l11_opy_ = int(bstack1llll1l11l_opy_) + 1
      bstack1l11lllll_opy_(bstack1l1ll11ll1_opy_, bstack1l1ll1l11_opy_, file_path)
      return bstack1l1ll1l11_opy_
    else:
      bstack1l11lllll_opy_(bstack1l1ll11ll1_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1ll1l1llll_opy_.format(str(e)))
    return -1
def bstack1111lll11_opy_(config):
  if not config[bstack111lll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ऻ")] or not config[bstack111lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ़")]:
    return True
  else:
    return False
def bstack1111l1l1_opy_(config, index=0):
  global bstack11lll111l_opy_
  bstack11ll11l1l_opy_ = {}
  caps = bstack11ll1l11l1_opy_ + bstack11ll1l1l_opy_
  if config.get(bstack111lll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪऽ"), False):
    bstack11ll11l1l_opy_[bstack111lll_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫा")] = True
    bstack11ll11l1l_opy_[bstack111lll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࡔࡶࡴࡪࡱࡱࡷࠬि")] = config.get(bstack111lll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ी"), {})
  if bstack11lll111l_opy_:
    caps += bstack1llll11lll_opy_
  for key in config:
    if key in caps + [bstack111lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ु")]:
      continue
    bstack11ll11l1l_opy_[key] = config[key]
  if bstack111lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧू") in config:
    for bstack1ll111ll_opy_ in config[bstack111lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨृ")][index]:
      if bstack1ll111ll_opy_ in caps:
        continue
      bstack11ll11l1l_opy_[bstack1ll111ll_opy_] = config[bstack111lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩॄ")][index][bstack1ll111ll_opy_]
  bstack11ll11l1l_opy_[bstack111lll_opy_ (u"ࠧࡩࡱࡶࡸࡓࡧ࡭ࡦࠩॅ")] = socket.gethostname()
  if bstack111lll_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩॆ") in bstack11ll11l1l_opy_:
    del (bstack11ll11l1l_opy_[bstack111lll_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪे")])
  return bstack11ll11l1l_opy_
def bstack11l11l11_opy_(config):
  global bstack11lll111l_opy_
  bstack1l11111111_opy_ = {}
  caps = bstack11ll1l1l_opy_
  if bstack11lll111l_opy_:
    caps += bstack1llll11lll_opy_
  for key in caps:
    if key in config:
      bstack1l11111111_opy_[key] = config[key]
  return bstack1l11111111_opy_
def bstack11llllll11_opy_(bstack11ll11l1l_opy_, bstack1l11111111_opy_):
  bstack11ll11l111_opy_ = {}
  for key in bstack11ll11l1l_opy_.keys():
    if key in bstack11ll1l1l1l_opy_:
      bstack11ll11l111_opy_[bstack11ll1l1l1l_opy_[key]] = bstack11ll11l1l_opy_[key]
    else:
      bstack11ll11l111_opy_[key] = bstack11ll11l1l_opy_[key]
  for key in bstack1l11111111_opy_:
    if key in bstack11ll1l1l1l_opy_:
      bstack11ll11l111_opy_[bstack11ll1l1l1l_opy_[key]] = bstack1l11111111_opy_[key]
    else:
      bstack11ll11l111_opy_[key] = bstack1l11111111_opy_[key]
  return bstack11ll11l111_opy_
def bstack1l1lllllll_opy_(config, index=0):
  global bstack11lll111l_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack11l11l1ll1_opy_ = bstack1ll1l1111_opy_(bstack1l1lll111l_opy_, config, logger)
  bstack1l11111111_opy_ = bstack11l11l11_opy_(config)
  bstack1lll1lll1l_opy_ = bstack11ll1l1l_opy_
  bstack1lll1lll1l_opy_ += bstack11lllll11_opy_
  bstack1l11111111_opy_ = update(bstack1l11111111_opy_, bstack11l11l1ll1_opy_)
  if bstack11lll111l_opy_:
    bstack1lll1lll1l_opy_ += bstack1llll11lll_opy_
  if bstack111lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ै") in config:
    if bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩॉ") in config[bstack111lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨॊ")][index]:
      caps[bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫो")] = config[bstack111lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪौ")][index][bstack111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ्࠭")]
    if bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪॎ") in config[bstack111lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॏ")][index]:
      caps[bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬॐ")] = str(config[bstack111lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ॑")][index][bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴ॒ࠧ")])
    bstack1l1l1ll1ll_opy_ = bstack1ll1l1111_opy_(bstack1l1lll111l_opy_, config[bstack111lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ॓")][index], logger)
    bstack1lll1lll1l_opy_ += list(bstack1l1l1ll1ll_opy_.keys())
    for bstack11l111l1l1_opy_ in bstack1lll1lll1l_opy_:
      if bstack11l111l1l1_opy_ in config[bstack111lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ॔")][index]:
        if bstack11l111l1l1_opy_ == bstack111lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫॕ"):
          try:
            bstack1l1l1ll1ll_opy_[bstack11l111l1l1_opy_] = str(config[bstack111lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॖ")][index][bstack11l111l1l1_opy_] * 1.0)
          except:
            bstack1l1l1ll1ll_opy_[bstack11l111l1l1_opy_] = str(config[bstack111lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॗ")][index][bstack11l111l1l1_opy_])
        else:
          bstack1l1l1ll1ll_opy_[bstack11l111l1l1_opy_] = config[bstack111lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨक़")][index][bstack11l111l1l1_opy_]
        del (config[bstack111lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩख़")][index][bstack11l111l1l1_opy_])
    bstack1l11111111_opy_ = update(bstack1l11111111_opy_, bstack1l1l1ll1ll_opy_)
  bstack11ll11l1l_opy_ = bstack1111l1l1_opy_(config, index)
  for bstack1ll11111_opy_ in bstack11ll1l1l_opy_ + list(bstack11l11l1ll1_opy_.keys()):
    if bstack1ll11111_opy_ in bstack11ll11l1l_opy_:
      bstack1l11111111_opy_[bstack1ll11111_opy_] = bstack11ll11l1l_opy_[bstack1ll11111_opy_]
      del (bstack11ll11l1l_opy_[bstack1ll11111_opy_])
  if bstack1ll1lll1ll_opy_(config):
    bstack11ll11l1l_opy_[bstack111lll_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧग़")] = True
    caps.update(bstack1l11111111_opy_)
    caps[bstack111lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩज़")] = bstack11ll11l1l_opy_
  else:
    bstack11ll11l1l_opy_[bstack111lll_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩड़")] = False
    caps.update(bstack11llllll11_opy_(bstack11ll11l1l_opy_, bstack1l11111111_opy_))
    if bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨढ़") in caps:
      caps[bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬफ़")] = caps[bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪय़")]
      del (caps[bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫॠ")])
    if bstack111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨॡ") in caps:
      caps[bstack111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪॢ")] = caps[bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪॣ")]
      del (caps[bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ।")])
  return caps
def bstack11llll1l1l_opy_():
  global bstack11ll1111ll_opy_
  global CONFIG
  if bstack11l1ll1ll_opy_() <= version.parse(bstack111lll_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫ॥")):
    if bstack11ll1111ll_opy_ != bstack111lll_opy_ (u"ࠬ࠭०"):
      return bstack111lll_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ१") + bstack11ll1111ll_opy_ + bstack111lll_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦ२")
    return bstack11ll1lll_opy_
  if bstack11ll1111ll_opy_ != bstack111lll_opy_ (u"ࠨࠩ३"):
    return bstack111lll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦ४") + bstack11ll1111ll_opy_ + bstack111lll_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦ५")
  return bstack1l1ll1ll_opy_
def bstack1lll111l_opy_(options):
  return hasattr(options, bstack111lll_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬ६"))
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
def bstack11lll1lll_opy_(options, bstack111111ll1_opy_):
  for bstack1l1l1l11ll_opy_ in bstack111111ll1_opy_:
    if bstack1l1l1l11ll_opy_ in [bstack111lll_opy_ (u"ࠬࡧࡲࡨࡵࠪ७"), bstack111lll_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪ८")]:
      continue
    if bstack1l1l1l11ll_opy_ in options._experimental_options:
      options._experimental_options[bstack1l1l1l11ll_opy_] = update(options._experimental_options[bstack1l1l1l11ll_opy_],
                                                         bstack111111ll1_opy_[bstack1l1l1l11ll_opy_])
    else:
      options.add_experimental_option(bstack1l1l1l11ll_opy_, bstack111111ll1_opy_[bstack1l1l1l11ll_opy_])
  if bstack111lll_opy_ (u"ࠧࡢࡴࡪࡷࠬ९") in bstack111111ll1_opy_:
    for arg in bstack111111ll1_opy_[bstack111lll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭॰")]:
      options.add_argument(arg)
    del (bstack111111ll1_opy_[bstack111lll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॱ")])
  if bstack111lll_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧॲ") in bstack111111ll1_opy_:
    for ext in bstack111111ll1_opy_[bstack111lll_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨॳ")]:
      try:
        options.add_extension(ext)
      except OSError:
        options.add_encoded_extension(ext)
    del (bstack111111ll1_opy_[bstack111lll_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩॴ")])
def bstack111ll11ll_opy_(options, bstack1l11l1l11_opy_):
  if bstack111lll_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬॵ") in bstack1l11l1l11_opy_:
    for bstack111l1llll_opy_ in bstack1l11l1l11_opy_[bstack111lll_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ॶ")]:
      if bstack111l1llll_opy_ in options._preferences:
        options._preferences[bstack111l1llll_opy_] = update(options._preferences[bstack111l1llll_opy_], bstack1l11l1l11_opy_[bstack111lll_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧॷ")][bstack111l1llll_opy_])
      else:
        options.set_preference(bstack111l1llll_opy_, bstack1l11l1l11_opy_[bstack111lll_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨॸ")][bstack111l1llll_opy_])
  if bstack111lll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨॹ") in bstack1l11l1l11_opy_:
    for arg in bstack1l11l1l11_opy_[bstack111lll_opy_ (u"ࠫࡦࡸࡧࡴࠩॺ")]:
      options.add_argument(arg)
def bstack1l11l11l11_opy_(options, bstack1lll1ll1ll_opy_):
  if bstack111lll_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼ࠭ॻ") in bstack1lll1ll1ll_opy_:
    options.use_webview(bool(bstack1lll1ll1ll_opy_[bstack111lll_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࠧॼ")]))
  bstack11lll1lll_opy_(options, bstack1lll1ll1ll_opy_)
def bstack1lll111l1_opy_(options, bstack1ll1l11l11_opy_):
  for bstack11l11l11l1_opy_ in bstack1ll1l11l11_opy_:
    if bstack11l11l11l1_opy_ in [bstack111lll_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫॽ"), bstack111lll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ॾ")]:
      continue
    options.set_capability(bstack11l11l11l1_opy_, bstack1ll1l11l11_opy_[bstack11l11l11l1_opy_])
  if bstack111lll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॿ") in bstack1ll1l11l11_opy_:
    for arg in bstack1ll1l11l11_opy_[bstack111lll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨঀ")]:
      options.add_argument(arg)
  if bstack111lll_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨঁ") in bstack1ll1l11l11_opy_:
    options.bstack1l1lll11ll_opy_(bool(bstack1ll1l11l11_opy_[bstack111lll_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩং")]))
def bstack1l1ll1111_opy_(options, bstack1ll1l1l1l_opy_):
  for bstack1l11111ll1_opy_ in bstack1ll1l1l1l_opy_:
    if bstack1l11111ll1_opy_ in [bstack111lll_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪঃ"), bstack111lll_opy_ (u"ࠧࡢࡴࡪࡷࠬ঄")]:
      continue
    options._options[bstack1l11111ll1_opy_] = bstack1ll1l1l1l_opy_[bstack1l11111ll1_opy_]
  if bstack111lll_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬঅ") in bstack1ll1l1l1l_opy_:
    for bstack1l1l11ll1l_opy_ in bstack1ll1l1l1l_opy_[bstack111lll_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭আ")]:
      options.bstack11l1lll1ll_opy_(
        bstack1l1l11ll1l_opy_, bstack1ll1l1l1l_opy_[bstack111lll_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧই")][bstack1l1l11ll1l_opy_])
  if bstack111lll_opy_ (u"ࠫࡦࡸࡧࡴࠩঈ") in bstack1ll1l1l1l_opy_:
    for arg in bstack1ll1l1l1l_opy_[bstack111lll_opy_ (u"ࠬࡧࡲࡨࡵࠪউ")]:
      options.add_argument(arg)
def bstack1llll11l1_opy_(options, caps):
  if not hasattr(options, bstack111lll_opy_ (u"࠭ࡋࡆ࡛ࠪঊ")):
    return
  if options.KEY == bstack111lll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬঋ"):
    options = bstack1l11l11ll1_opy_.bstack1ll11111ll_opy_(bstack11l11l111_opy_=options, config=CONFIG)
  if options.KEY == bstack111lll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ঌ") and options.KEY in caps:
    bstack11lll1lll_opy_(options, caps[bstack111lll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ঍")])
  elif options.KEY == bstack111lll_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨ঎") and options.KEY in caps:
    bstack111ll11ll_opy_(options, caps[bstack111lll_opy_ (u"ࠫࡲࡵࡺ࠻ࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩএ")])
  elif options.KEY == bstack111lll_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ঐ") and options.KEY in caps:
    bstack1lll111l1_opy_(options, caps[bstack111lll_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧ঑")])
  elif options.KEY == bstack111lll_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ঒") and options.KEY in caps:
    bstack1l11l11l11_opy_(options, caps[bstack111lll_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩও")])
  elif options.KEY == bstack111lll_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨঔ") and options.KEY in caps:
    bstack1l1ll1111_opy_(options, caps[bstack111lll_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩক")])
def bstack1ll11l1l11_opy_(caps):
  global bstack11lll111l_opy_
  if isinstance(os.environ.get(bstack111lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬখ")), str):
    bstack11lll111l_opy_ = eval(os.getenv(bstack111lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭গ")))
  if bstack11lll111l_opy_:
    if bstack1l11l1111l_opy_() < version.parse(bstack111lll_opy_ (u"࠭࠲࠯࠵࠱࠴ࠬঘ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack111lll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧঙ")
    if bstack111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭চ") in caps:
      browser = caps[bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧছ")]
    elif bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫজ") in caps:
      browser = caps[bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬঝ")]
    browser = str(browser).lower()
    if browser == bstack111lll_opy_ (u"ࠬ࡯ࡰࡩࡱࡱࡩࠬঞ") or browser == bstack111lll_opy_ (u"࠭ࡩࡱࡣࡧࠫট"):
      browser = bstack111lll_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧঠ")
    if browser == bstack111lll_opy_ (u"ࠨࡵࡤࡱࡸࡻ࡮ࡨࠩড"):
      browser = bstack111lll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩঢ")
    if browser not in [bstack111lll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪণ"), bstack111lll_opy_ (u"ࠫࡪࡪࡧࡦࠩত"), bstack111lll_opy_ (u"ࠬ࡯ࡥࠨথ"), bstack111lll_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭দ"), bstack111lll_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨধ")]:
      return None
    try:
      package = bstack111lll_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷ࠴ࡻࡾ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪন").format(browser)
      name = bstack111lll_opy_ (u"ࠩࡒࡴࡹ࡯࡯࡯ࡵࠪ঩")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1lll111l_opy_(options):
        return None
      for bstack1ll11111_opy_ in caps.keys():
        options.set_capability(bstack1ll11111_opy_, caps[bstack1ll11111_opy_])
      bstack1llll11l1_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1111ll11l_opy_(options, bstack11llll1ll1_opy_):
  if not bstack1lll111l_opy_(options):
    return
  for bstack1ll11111_opy_ in bstack11llll1ll1_opy_.keys():
    if bstack1ll11111_opy_ in bstack11lllll11_opy_:
      continue
    if bstack1ll11111_opy_ in options._caps and type(options._caps[bstack1ll11111_opy_]) in [dict, list]:
      options._caps[bstack1ll11111_opy_] = update(options._caps[bstack1ll11111_opy_], bstack11llll1ll1_opy_[bstack1ll11111_opy_])
    else:
      options.set_capability(bstack1ll11111_opy_, bstack11llll1ll1_opy_[bstack1ll11111_opy_])
  bstack1llll11l1_opy_(options, bstack11llll1ll1_opy_)
  if bstack111lll_opy_ (u"ࠪࡱࡴࢀ࠺ࡥࡧࡥࡹ࡬࡭ࡥࡳࡃࡧࡨࡷ࡫ࡳࡴࠩপ") in options._caps:
    if options._caps[bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩফ")] and options._caps[bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪব")].lower() != bstack111lll_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧভ"):
      del options._caps[bstack111lll_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ࠭ম")]
def bstack11lll1l111_opy_(proxy_config):
  if bstack111lll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬয") in proxy_config:
    proxy_config[bstack111lll_opy_ (u"ࠩࡶࡷࡱࡖࡲࡰࡺࡼࠫর")] = proxy_config[bstack111lll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ঱")]
    del (proxy_config[bstack111lll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨল")])
  if bstack111lll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ঳") in proxy_config and proxy_config[bstack111lll_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩ঴")].lower() != bstack111lll_opy_ (u"ࠧࡥ࡫ࡵࡩࡨࡺࠧ঵"):
    proxy_config[bstack111lll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫশ")] = bstack111lll_opy_ (u"ࠩࡰࡥࡳࡻࡡ࡭ࠩষ")
  if bstack111lll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡃࡸࡸࡴࡩ࡯࡯ࡨ࡬࡫࡚ࡸ࡬ࠨস") in proxy_config:
    proxy_config[bstack111lll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧহ")] = bstack111lll_opy_ (u"ࠬࡶࡡࡤࠩ঺")
  return proxy_config
def bstack1l1l1ll111_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack111lll_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ঻") in config:
    return proxy
  config[bstack111lll_opy_ (u"ࠧࡱࡴࡲࡼࡾ়࠭")] = bstack11lll1l111_opy_(config[bstack111lll_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧঽ")])
  if proxy == None:
    proxy = Proxy(config[bstack111lll_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨা")])
  return proxy
def bstack1lll11ll_opy_(self):
  global CONFIG
  global bstack1l1111l1ll_opy_
  try:
    proxy = bstack11l1l1lll_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack111lll_opy_ (u"ࠪ࠲ࡵࡧࡣࠨি")):
        proxies = bstack11l111l11l_opy_(proxy, bstack11llll1l1l_opy_())
        if len(proxies) > 0:
          protocol, bstack1lllll1111_opy_ = proxies.popitem()
          if bstack111lll_opy_ (u"ࠦ࠿࠵࠯ࠣী") in bstack1lllll1111_opy_:
            return bstack1lllll1111_opy_
          else:
            return bstack111lll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨু") + bstack1lllll1111_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack111lll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡳࡶࡴࡾࡹࠡࡷࡵࡰࠥࡀࠠࡼࡿࠥূ").format(str(e)))
  return bstack1l1111l1ll_opy_(self)
def bstack1l1111ll1_opy_():
  global CONFIG
  return bstack1l11lllll1_opy_(CONFIG) and bstack1l1l1l1l1l_opy_() and bstack11l1ll1ll_opy_() >= version.parse(bstack11l1l1111_opy_)
def bstack1ll11l11ll_opy_():
  global CONFIG
  return (bstack111lll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪৃ") in CONFIG or bstack111lll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬৄ") in CONFIG) and bstack1l1ll1l1_opy_()
def bstack11ll1111_opy_(config):
  bstack111ll1l1_opy_ = {}
  if bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭৅") in config:
    bstack111ll1l1_opy_ = config[bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ৆")]
  if bstack111lll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪে") in config:
    bstack111ll1l1_opy_ = config[bstack111lll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫৈ")]
  proxy = bstack11l1l1lll_opy_(config)
  if proxy:
    if proxy.endswith(bstack111lll_opy_ (u"࠭࠮ࡱࡣࡦࠫ৉")) and os.path.isfile(proxy):
      bstack111ll1l1_opy_[bstack111lll_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪ৊")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack111lll_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭ো")):
        proxies = bstack1llll1ll11_opy_(config, bstack11llll1l1l_opy_())
        if len(proxies) > 0:
          protocol, bstack1lllll1111_opy_ = proxies.popitem()
          if bstack111lll_opy_ (u"ࠤ࠽࠳࠴ࠨৌ") in bstack1lllll1111_opy_:
            parsed_url = urlparse(bstack1lllll1111_opy_)
          else:
            parsed_url = urlparse(protocol + bstack111lll_opy_ (u"ࠥ࠾࠴࠵্ࠢ") + bstack1lllll1111_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack111ll1l1_opy_[bstack111lll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡋࡳࡸࡺࠧৎ")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack111ll1l1_opy_[bstack111lll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡴࡸࡴࠨ৏")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack111ll1l1_opy_[bstack111lll_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡚ࡹࡥࡳࠩ৐")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack111ll1l1_opy_[bstack111lll_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖࡡࡴࡵࠪ৑")] = str(parsed_url.password)
  return bstack111ll1l1_opy_
def bstack1llllll11l_opy_(config):
  if bstack111lll_opy_ (u"ࠨࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸ࠭৒") in config:
    return config[bstack111lll_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧ৓")]
  return {}
def bstack1lll111l1l_opy_(caps):
  global bstack1l1lll11l1_opy_
  if bstack111lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ৔") in caps:
    caps[bstack111lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ৕")][bstack111lll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫ৖")] = True
    if bstack1l1lll11l1_opy_:
      caps[bstack111lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧৗ")][bstack111lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ৘")] = bstack1l1lll11l1_opy_
  else:
    caps[bstack111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭৙")] = True
    if bstack1l1lll11l1_opy_:
      caps[bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ৚")] = bstack1l1lll11l1_opy_
@measure(event_name=EVENTS.bstack11lll1ll1l_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l11l11l_opy_=bstack11l1l1llll_opy_)
def bstack1l1llll111_opy_():
  global CONFIG
  if not bstack1l1l111l1_opy_(CONFIG) or cli.is_enabled(CONFIG):
    return
  if bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ৛") in CONFIG and bstack1ll111ll1_opy_(CONFIG[bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨড়")]):
    if (
      bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩঢ়") in CONFIG
      and bstack1ll111ll1_opy_(CONFIG[bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ৞")].get(bstack111lll_opy_ (u"ࠧࡴ࡭࡬ࡴࡇ࡯࡮ࡢࡴࡼࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡸࡧࡴࡪࡱࡱࠫয়")))
    ):
      logger.debug(bstack111lll_opy_ (u"ࠣࡎࡲࡧࡦࡲࠠࡣ࡫ࡱࡥࡷࡿࠠ࡯ࡱࡷࠤࡸࡺࡡࡳࡶࡨࡨࠥࡧࡳࠡࡵ࡮࡭ࡵࡈࡩ࡯ࡣࡵࡽࡎࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡡࡵ࡫ࡲࡲࠥ࡯ࡳࠡࡧࡱࡥࡧࡲࡥࡥࠤৠ"))
      return
    bstack111ll1l1_opy_ = bstack11ll1111_opy_(CONFIG)
    bstack1llll1llll_opy_(CONFIG[bstack111lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬৡ")], bstack111ll1l1_opy_)
def bstack1llll1llll_opy_(key, bstack111ll1l1_opy_):
  global bstack11l1ll1l_opy_
  logger.info(bstack1l11l1l11l_opy_)
  try:
    bstack11l1ll1l_opy_ = Local()
    bstack1l1l11ll1_opy_ = {bstack111lll_opy_ (u"ࠪ࡯ࡪࡿࠧৢ"): key}
    bstack1l1l11ll1_opy_.update(bstack111ll1l1_opy_)
    logger.debug(bstack11ll1l11ll_opy_.format(str(bstack1l1l11ll1_opy_)).replace(key, bstack111lll_opy_ (u"ࠫࡠࡘࡅࡅࡃࡆࡘࡊࡊ࡝ࠨৣ")))
    bstack11l1ll1l_opy_.start(**bstack1l1l11ll1_opy_)
    if bstack11l1ll1l_opy_.isRunning():
      logger.info(bstack1lll11111l_opy_)
  except Exception as e:
    bstack11l11111_opy_(bstack11llll1111_opy_.format(str(e)))
def bstack1111lll1_opy_():
  global bstack11l1ll1l_opy_
  if bstack11l1ll1l_opy_.isRunning():
    logger.info(bstack1l1l11lll_opy_)
    bstack11l1ll1l_opy_.stop()
  bstack11l1ll1l_opy_ = None
def bstack11111l111_opy_(bstack1l1llllll1_opy_=[]):
  global CONFIG
  bstack111l111l_opy_ = []
  bstack11ll11ll_opy_ = [bstack111lll_opy_ (u"ࠬࡵࡳࠨ৤"), bstack111lll_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ৥"), bstack111lll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ০"), bstack111lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪ১"), bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ২"), bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ৩")]
  try:
    for err in bstack1l1llllll1_opy_:
      bstack1lll1l1ll_opy_ = {}
      for k in bstack11ll11ll_opy_:
        val = CONFIG[bstack111lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ৪")][int(err[bstack111lll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ৫")])].get(k)
        if val:
          bstack1lll1l1ll_opy_[k] = val
      if(err[bstack111lll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ৬")] != bstack111lll_opy_ (u"ࠧࠨ৭")):
        bstack1lll1l1ll_opy_[bstack111lll_opy_ (u"ࠨࡶࡨࡷࡹࡹࠧ৮")] = {
          err[bstack111lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ৯")]: err[bstack111lll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩৰ")]
        }
        bstack111l111l_opy_.append(bstack1lll1l1ll_opy_)
  except Exception as e:
    logger.debug(bstack111lll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡰࡴࡰࡥࡹࡺࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷ࠾ࠥ࠭ৱ") + str(e))
  finally:
    return bstack111l111l_opy_
def bstack11l111l111_opy_(file_name):
  bstack1l111llll1_opy_ = []
  try:
    bstack1l1l11l1l1_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1l1l11l1l1_opy_):
      with open(bstack1l1l11l1l1_opy_) as f:
        bstack1l11l1111_opy_ = json.load(f)
        bstack1l111llll1_opy_ = bstack1l11l1111_opy_
      os.remove(bstack1l1l11l1l1_opy_)
    return bstack1l111llll1_opy_
  except Exception as e:
    logger.debug(bstack111lll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧ࡫ࡱࡨ࡮ࡴࡧࠡࡧࡵࡶࡴࡸࠠ࡭࡫ࡶࡸ࠿ࠦࠧ৲") + str(e))
    return bstack1l111llll1_opy_
def bstack1llllll1ll_opy_():
  try:
      from bstack_utils.constants import bstack111l11l11_opy_, EVENTS
      from bstack_utils.helper import bstack1l1ll1l111_opy_, get_host_info, bstack1ll1l11ll_opy_
      from datetime import datetime
      from filelock import FileLock
      bstack11lll111l1_opy_ = os.path.join(os.getcwd(), bstack111lll_opy_ (u"࠭࡬ࡰࡩࠪ৳"), bstack111lll_opy_ (u"ࠧ࡬ࡧࡼ࠱ࡲ࡫ࡴࡳ࡫ࡦࡷ࠳ࡰࡳࡰࡰࠪ৴"))
      lock = FileLock(bstack11lll111l1_opy_+bstack111lll_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢ৵"))
      def bstack11111111l_opy_():
          try:
              with lock:
                  with open(bstack11lll111l1_opy_, bstack111lll_opy_ (u"ࠤࡵࠦ৶"), encoding=bstack111lll_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤ৷")) as file:
                      data = json.load(file)
                      config = {
                          bstack111lll_opy_ (u"ࠦ࡭࡫ࡡࡥࡧࡵࡷࠧ৸"): {
                              bstack111lll_opy_ (u"ࠧࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠦ৹"): bstack111lll_opy_ (u"ࠨࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠤ৺"),
                          }
                      }
                      bstack11l11lll1_opy_ = datetime.utcnow()
                      bstack1llllllll1_opy_ = bstack11l11lll1_opy_.strftime(bstack111lll_opy_ (u"࡛ࠢࠦ࠰ࠩࡲ࠳ࠥࡥࡖࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࠲ࠪ࡬ࠠࡖࡖࡆࠦ৻"))
                      bstack11lll1111l_opy_ = os.environ.get(bstack111lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ৼ")) if os.environ.get(bstack111lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ৽")) else bstack1ll1l11ll_opy_.get_property(bstack111lll_opy_ (u"ࠥࡷࡩࡱࡒࡶࡰࡌࡨࠧ৾"))
                      payload = {
                          bstack111lll_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠣ৿"): bstack111lll_opy_ (u"ࠧࡹࡤ࡬ࡡࡨࡺࡪࡴࡴࡴࠤ਀"),
                          bstack111lll_opy_ (u"ࠨࡤࡢࡶࡤࠦਁ"): {
                              bstack111lll_opy_ (u"ࠢࡵࡧࡶࡸ࡭ࡻࡢࡠࡷࡸ࡭ࡩࠨਂ"): bstack11lll1111l_opy_,
                              bstack111lll_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡥࡡࡧࡥࡾࠨਃ"): bstack1llllllll1_opy_,
                              bstack111lll_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡰࡤࡱࡪࠨ਄"): bstack111lll_opy_ (u"ࠥࡗࡉࡑࡆࡦࡣࡷࡹࡷ࡫ࡐࡦࡴࡩࡳࡷࡳࡡ࡯ࡥࡨࠦਅ"),
                              bstack111lll_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢ࡮ࡸࡵ࡮ࠣਆ"): {
                                  bstack111lll_opy_ (u"ࠧࡳࡥࡢࡵࡸࡶࡪࡹࠢਇ"): data,
                                  bstack111lll_opy_ (u"ࠨࡳࡥ࡭ࡕࡹࡳࡏࡤࠣਈ"): bstack1ll1l11ll_opy_.get_property(bstack111lll_opy_ (u"ࠢࡴࡦ࡮ࡖࡺࡴࡉࡥࠤਉ"))
                              },
                              bstack111lll_opy_ (u"ࠣࡷࡶࡩࡷࡥࡤࡢࡶࡤࠦਊ"): bstack1ll1l11ll_opy_.get_property(bstack111lll_opy_ (u"ࠤࡸࡷࡪࡸࡎࡢ࡯ࡨࠦ਋")),
                              bstack111lll_opy_ (u"ࠥ࡬ࡴࡹࡴࡠ࡫ࡱࡪࡴࠨ਌"): get_host_info()
                          }
                      }
                      bstack1ll11llll_opy_ = bstack111llll1l_opy_(cli.config, [bstack111lll_opy_ (u"ࠦࡦࡶࡩࡴࠤ਍"), bstack111lll_opy_ (u"ࠧ࡫ࡤࡴࡋࡱࡷࡹࡸࡵ࡮ࡧࡱࡸࡦࡺࡩࡰࡰࠥ਎"), bstack111lll_opy_ (u"ࠨࡡࡱ࡫ࠥਏ")], bstack111l11l11_opy_) if cli.is_running() else bstack111l11l11_opy_
                      response = bstack1l1ll1l111_opy_(bstack111lll_opy_ (u"ࠢࡑࡑࡖࡘࠧਐ"), bstack1ll11llll_opy_, payload, config)
                      if(response.status_code >= 200 and response.status_code < 300):
                          logger.debug(bstack111lll_opy_ (u"ࠣࡆࡤࡸࡦࠦࡳࡦࡰࡷࠤࡸࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻࠣࡸࡴࠦࡻࡾࠢࡺ࡭ࡹ࡮ࠠࡥࡣࡷࡥࠥࢁࡽࠣ਑").format(bstack111l11l11_opy_, payload))
                      else:
                          logger.debug(bstack111lll_opy_ (u"ࠤࡕࡩࡶࡻࡥࡴࡶࠣࡪࡦ࡯࡬ࡦࡦࠣࡪࡴࡸࠠࡼࡿࠣࡻ࡮ࡺࡨࠡࡦࡤࡸࡦࠦࡻࡾࠤ਒").format(bstack111l11l11_opy_, payload))
          except Exception as e:
              logger.debug(bstack111lll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡰࡧࠤࡰ࡫ࡹࠡ࡯ࡨࡸࡷ࡯ࡣࡴࠢࡧࡥࡹࡧࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵࠤࢀࢃࠢਓ").format(e))
      bstack11111111l_opy_()
      bstack1ll11l11l1_opy_(bstack11lll111l1_opy_, logger)
  except:
    pass
def bstack1ll1lll111_opy_():
  global bstack1l11ll111_opy_
  global bstack1ll11111l_opy_
  global bstack1l111llll_opy_
  global bstack11ll11l1_opy_
  global bstack1l11lll11_opy_
  global bstack11ll11ll1_opy_
  global CONFIG
  bstack1l11lll11l_opy_ = os.environ.get(bstack111lll_opy_ (u"ࠫࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ࡟ࡖࡕࡈࡈࠬਔ"))
  if bstack1l11lll11l_opy_ in [bstack111lll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫਕ"), bstack111lll_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬਖ")]:
    bstack1ll11lll11_opy_()
  percy.shutdown()
  if bstack1l11ll111_opy_:
    logger.warning(bstack1ll1111ll_opy_.format(str(bstack1l11ll111_opy_)))
  else:
    try:
      bstack11l1l1l1_opy_ = bstack111111l1l_opy_(bstack111lll_opy_ (u"ࠧ࠯ࡤࡶࡸࡦࡩ࡫࠮ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭ਗ"), logger)
      if bstack11l1l1l1_opy_.get(bstack111lll_opy_ (u"ࠨࡰࡸࡨ࡬࡫࡟࡭ࡱࡦࡥࡱ࠭ਘ")) and bstack11l1l1l1_opy_.get(bstack111lll_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧਙ")).get(bstack111lll_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬਚ")):
        logger.warning(bstack1ll1111ll_opy_.format(str(bstack11l1l1l1_opy_[bstack111lll_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩਛ")][bstack111lll_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧਜ")])))
    except Exception as e:
      logger.error(e)
  if cli.is_running():
    bstack1l1ll11ll_opy_.invoke(bstack11ll1l111_opy_.bstack11l1l1l11_opy_)
  logger.info(bstack1l1llll1ll_opy_)
  global bstack11l1ll1l_opy_
  if bstack11l1ll1l_opy_:
    bstack1111lll1_opy_()
  try:
    for driver in bstack1ll11111l_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1l11lll1_opy_)
  if bstack11ll11ll1_opy_ == bstack111lll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬਝ"):
    bstack1l11lll11_opy_ = bstack11l111l111_opy_(bstack111lll_opy_ (u"ࠧࡳࡱࡥࡳࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨਞ"))
  if bstack11ll11ll1_opy_ == bstack111lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨਟ") and len(bstack11ll11l1_opy_) == 0:
    bstack11ll11l1_opy_ = bstack11l111l111_opy_(bstack111lll_opy_ (u"ࠩࡳࡻࡤࡶࡹࡵࡧࡶࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧਠ"))
    if len(bstack11ll11l1_opy_) == 0:
      bstack11ll11l1_opy_ = bstack11l111l111_opy_(bstack111lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡴࡵࡶ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩਡ"))
  bstack11ll1l1111_opy_ = bstack111lll_opy_ (u"ࠫࠬਢ")
  if len(bstack1l111llll_opy_) > 0:
    bstack11ll1l1111_opy_ = bstack11111l111_opy_(bstack1l111llll_opy_)
  elif len(bstack11ll11l1_opy_) > 0:
    bstack11ll1l1111_opy_ = bstack11111l111_opy_(bstack11ll11l1_opy_)
  elif len(bstack1l11lll11_opy_) > 0:
    bstack11ll1l1111_opy_ = bstack11111l111_opy_(bstack1l11lll11_opy_)
  elif len(bstack1ll111111_opy_) > 0:
    bstack11ll1l1111_opy_ = bstack11111l111_opy_(bstack1ll111111_opy_)
  if bool(bstack11ll1l1111_opy_):
    bstack1ll1llllll_opy_(bstack11ll1l1111_opy_)
  else:
    bstack1ll1llllll_opy_()
  bstack1ll11l11l1_opy_(bstack1l1llll1l_opy_, logger)
  if bstack1l11lll11l_opy_ not in [bstack111lll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ਣ")]:
    bstack1llllll1ll_opy_()
  bstack1111ll111_opy_.bstack11l1111ll_opy_(CONFIG)
  if len(bstack1l11lll11_opy_) > 0:
    sys.exit(len(bstack1l11lll11_opy_))
def bstack1lll1l11l1_opy_(bstack1l1lll1l1l_opy_, frame):
  global bstack1ll1l11ll_opy_
  logger.error(bstack1l111l11_opy_)
  bstack1ll1l11ll_opy_.bstack1lll1llll1_opy_(bstack111lll_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡎࡰࠩਤ"), bstack1l1lll1l1l_opy_)
  if hasattr(signal, bstack111lll_opy_ (u"ࠧࡔ࡫ࡪࡲࡦࡲࡳࠨਥ")):
    bstack1ll1l11ll_opy_.bstack1lll1llll1_opy_(bstack111lll_opy_ (u"ࠨࡵࡧ࡯ࡐ࡯࡬࡭ࡕ࡬࡫ࡳࡧ࡬ࠨਦ"), signal.Signals(bstack1l1lll1l1l_opy_).name)
  else:
    bstack1ll1l11ll_opy_.bstack1lll1llll1_opy_(bstack111lll_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩਧ"), bstack111lll_opy_ (u"ࠪࡗࡎࡍࡕࡏࡍࡑࡓ࡜ࡔࠧਨ"))
  if cli.is_running():
    bstack1l1ll11ll_opy_.invoke(bstack11ll1l111_opy_.bstack11l1l1l11_opy_)
  bstack1l11lll11l_opy_ = os.environ.get(bstack111lll_opy_ (u"ࠫࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ࡟ࡖࡕࡈࡈࠬ਩"))
  if bstack1l11lll11l_opy_ == bstack111lll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬਪ") and not cli.is_enabled(CONFIG):
    bstack11111ll1l_opy_.stop(bstack1ll1l11ll_opy_.get_property(bstack111lll_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭ਫ")))
  bstack1ll1lll111_opy_()
  sys.exit(1)
def bstack11l11111_opy_(err):
  logger.critical(bstack1111111l_opy_.format(str(err)))
  bstack1ll1llllll_opy_(bstack1111111l_opy_.format(str(err)), True)
  atexit.unregister(bstack1ll1lll111_opy_)
  bstack1ll11lll11_opy_()
  sys.exit(1)
def bstack1l1l1l1ll_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1ll1llllll_opy_(message, True)
  atexit.unregister(bstack1ll1lll111_opy_)
  bstack1ll11lll11_opy_()
  sys.exit(1)
def bstack11l11lllll_opy_():
  global CONFIG
  global bstack11lll1llll_opy_
  global bstack11lll1111_opy_
  global bstack111lll111_opy_
  CONFIG = bstack1lll11l111_opy_()
  load_dotenv(CONFIG.get(bstack111lll_opy_ (u"ࠧࡦࡰࡹࡊ࡮ࡲࡥࠨਬ")))
  bstack1lllll11_opy_()
  bstack1llll1l11_opy_()
  CONFIG = bstack1lllllll1_opy_(CONFIG)
  update(CONFIG, bstack11lll1111_opy_)
  update(CONFIG, bstack11lll1llll_opy_)
  if not cli.is_enabled(CONFIG):
    CONFIG = bstack11llll11l1_opy_(CONFIG)
  bstack111lll111_opy_ = bstack1l1l111l1_opy_(CONFIG)
  os.environ[bstack111lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫਭ")] = bstack111lll111_opy_.__str__().lower()
  bstack1ll1l11ll_opy_.bstack1lll1llll1_opy_(bstack111lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪਮ"), bstack111lll111_opy_)
  if (bstack111lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ਯ") in CONFIG and bstack111lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧਰ") in bstack11lll1llll_opy_) or (
          bstack111lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ਱") in CONFIG and bstack111lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩਲ") not in bstack11lll1111_opy_):
    if os.getenv(bstack111lll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫਲ਼")):
      CONFIG[bstack111lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ਴")] = os.getenv(bstack111lll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ਵ"))
    else:
      if not CONFIG.get(bstack111lll_opy_ (u"ࠥࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠨਸ਼"), bstack111lll_opy_ (u"ࠦࠧ਷")) in bstack1l1111ll11_opy_:
        bstack11ll1l1l1_opy_()
  elif (bstack111lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨਸ") not in CONFIG and bstack111lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨਹ") in CONFIG) or (
          bstack111lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ਺") in bstack11lll1111_opy_ and bstack111lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ਻") not in bstack11lll1llll_opy_):
    del (CONFIG[bstack111lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ਼ࠫ")])
  if bstack1111lll11_opy_(CONFIG):
    bstack11l11111_opy_(bstack11ll1l1l11_opy_)
  Config.bstack1ll11lll1l_opy_().bstack1lll1llll1_opy_(bstack111lll_opy_ (u"ࠥࡹࡸ࡫ࡲࡏࡣࡰࡩࠧ਽"), CONFIG[bstack111lll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ਾ")])
  bstack1l1l1lll11_opy_()
  bstack111l111l1_opy_()
  if bstack11lll111l_opy_ and not CONFIG.get(bstack111lll_opy_ (u"ࠧ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠣਿ"), bstack111lll_opy_ (u"ࠨࠢੀ")) in bstack1l1111ll11_opy_:
    CONFIG[bstack111lll_opy_ (u"ࠧࡢࡲࡳࠫੁ")] = bstack111ll111l_opy_(CONFIG)
    logger.info(bstack1ll1ll11_opy_.format(CONFIG[bstack111lll_opy_ (u"ࠨࡣࡳࡴࠬੂ")]))
  if not bstack111lll111_opy_:
    CONFIG[bstack111lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ੃")] = [{}]
def bstack1l111l1l1l_opy_(config, bstack1111l1lll_opy_):
  global CONFIG
  global bstack11lll111l_opy_
  CONFIG = config
  bstack11lll111l_opy_ = bstack1111l1lll_opy_
def bstack111l111l1_opy_():
  global CONFIG
  global bstack11lll111l_opy_
  if bstack111lll_opy_ (u"ࠪࡥࡵࡶࠧ੄") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1l1l1l1ll_opy_(e, bstack1l111l1lll_opy_)
    bstack11lll111l_opy_ = True
    bstack1ll1l11ll_opy_.bstack1lll1llll1_opy_(bstack111lll_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪ੅"), True)
def bstack111ll111l_opy_(config):
  bstack1llll1ll_opy_ = bstack111lll_opy_ (u"ࠬ࠭੆")
  app = config[bstack111lll_opy_ (u"࠭ࡡࡱࡲࠪੇ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack11l11l1l1_opy_:
      if os.path.exists(app):
        bstack1llll1ll_opy_ = bstack1lll1l11ll_opy_(config, app)
      elif bstack1l1l1l111_opy_(app):
        bstack1llll1ll_opy_ = app
      else:
        bstack11l11111_opy_(bstack1l1ll1111l_opy_.format(app))
    else:
      if bstack1l1l1l111_opy_(app):
        bstack1llll1ll_opy_ = app
      elif os.path.exists(app):
        bstack1llll1ll_opy_ = bstack1lll1l11ll_opy_(app)
      else:
        bstack11l11111_opy_(bstack1ll1111l1_opy_)
  else:
    if len(app) > 2:
      bstack11l11111_opy_(bstack11lll11l_opy_)
    elif len(app) == 2:
      if bstack111lll_opy_ (u"ࠧࡱࡣࡷ࡬ࠬੈ") in app and bstack111lll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫ੉") in app:
        if os.path.exists(app[bstack111lll_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ੊")]):
          bstack1llll1ll_opy_ = bstack1lll1l11ll_opy_(config, app[bstack111lll_opy_ (u"ࠪࡴࡦࡺࡨࠨੋ")], app[bstack111lll_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧੌ")])
        else:
          bstack11l11111_opy_(bstack1l1ll1111l_opy_.format(app))
      else:
        bstack11l11111_opy_(bstack11lll11l_opy_)
    else:
      for key in app:
        if key in bstack11111ll1_opy_:
          if key == bstack111lll_opy_ (u"ࠬࡶࡡࡵࡪ੍ࠪ"):
            if os.path.exists(app[key]):
              bstack1llll1ll_opy_ = bstack1lll1l11ll_opy_(config, app[key])
            else:
              bstack11l11111_opy_(bstack1l1ll1111l_opy_.format(app))
          else:
            bstack1llll1ll_opy_ = app[key]
        else:
          bstack11l11111_opy_(bstack1l1lll1111_opy_)
  return bstack1llll1ll_opy_
def bstack1l1l1l111_opy_(bstack1llll1ll_opy_):
  import re
  bstack1l11l1lll1_opy_ = re.compile(bstack111lll_opy_ (u"ࡸࠢ࡟࡝ࡤ࠱ࡿࡇ࡛࠭࠲࠰࠽ࡡࡥ࠮࡝࠯ࡠ࠮ࠩࠨ੎"))
  bstack1l11l111ll_opy_ = re.compile(bstack111lll_opy_ (u"ࡲࠣࡠ࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯࠵࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬࠧࠦ੏"))
  if bstack111lll_opy_ (u"ࠨࡤࡶ࠾࠴࠵ࠧ੐") in bstack1llll1ll_opy_ or re.fullmatch(bstack1l11l1lll1_opy_, bstack1llll1ll_opy_) or re.fullmatch(bstack1l11l111ll_opy_, bstack1llll1ll_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack11lllll1ll_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l11l11l_opy_=bstack11l1l1llll_opy_)
def bstack1lll1l11ll_opy_(config, path, bstack111lll11l_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack111lll_opy_ (u"ࠩࡵࡦࠬੑ")).read()).hexdigest()
  bstack1l1111l11_opy_ = bstack1111lllll_opy_(md5_hash)
  bstack1llll1ll_opy_ = None
  if bstack1l1111l11_opy_:
    logger.info(bstack1llll111l1_opy_.format(bstack1l1111l11_opy_, md5_hash))
    return bstack1l1111l11_opy_
  bstack11ll1ll1_opy_ = datetime.datetime.now()
  bstack11l1ll11l_opy_ = MultipartEncoder(
    fields={
      bstack111lll_opy_ (u"ࠪࡪ࡮ࡲࡥࠨ੒"): (os.path.basename(path), open(os.path.abspath(path), bstack111lll_opy_ (u"ࠫࡷࡨࠧ੓")), bstack111lll_opy_ (u"ࠬࡺࡥࡹࡶ࠲ࡴࡱࡧࡩ࡯ࠩ੔")),
      bstack111lll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩ੕"): bstack111lll11l_opy_
    }
  )
  response = requests.post(bstack1l11l111l_opy_, data=bstack11l1ll11l_opy_,
                           headers={bstack111lll_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭੖"): bstack11l1ll11l_opy_.content_type},
                           auth=(config[bstack111lll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ੗")], config[bstack111lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ੘")]))
  try:
    res = json.loads(response.text)
    bstack1llll1ll_opy_ = res[bstack111lll_opy_ (u"ࠪࡥࡵࡶ࡟ࡶࡴ࡯ࠫਖ਼")]
    logger.info(bstack11l11ll111_opy_.format(bstack1llll1ll_opy_))
    bstack1l1l11l1ll_opy_(md5_hash, bstack1llll1ll_opy_)
    cli.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼ࡸࡴࡱࡵࡡࡥࡡࡤࡴࡵࠨਗ਼"), datetime.datetime.now() - bstack11ll1ll1_opy_)
  except ValueError as err:
    bstack11l11111_opy_(bstack1111l1l1l_opy_.format(str(err)))
  return bstack1llll1ll_opy_
def bstack1l1l1lll11_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack11l1ll1l1l_opy_
  bstack11ll1l1lll_opy_ = 1
  bstack11l1ll11ll_opy_ = 1
  if bstack111lll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬਜ਼") in CONFIG:
    bstack11l1ll11ll_opy_ = CONFIG[bstack111lll_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ੜ")]
  else:
    bstack11l1ll11ll_opy_ = bstack1l1ll111ll_opy_(framework_name, args) or 1
  if bstack111lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ੝") in CONFIG:
    bstack11ll1l1lll_opy_ = len(CONFIG[bstack111lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫਫ਼")])
  bstack11l1ll1l1l_opy_ = int(bstack11l1ll11ll_opy_) * int(bstack11ll1l1lll_opy_)
def bstack1l1ll111ll_opy_(framework_name, args):
  if framework_name == bstack1l111l1l_opy_ and args and bstack111lll_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ੟") in args:
      bstack111l111ll_opy_ = args.index(bstack111lll_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨ੠"))
      return int(args[bstack111l111ll_opy_ + 1]) or 1
  return 1
def bstack1111lllll_opy_(md5_hash):
  bstack11ll11l1ll_opy_ = os.path.join(os.path.expanduser(bstack111lll_opy_ (u"ࠫࢃ࠭੡")), bstack111lll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ੢"), bstack111lll_opy_ (u"࠭ࡡࡱࡲࡘࡴࡱࡵࡡࡥࡏࡇ࠹ࡍࡧࡳࡩ࠰࡭ࡷࡴࡴࠧ੣"))
  if os.path.exists(bstack11ll11l1ll_opy_):
    bstack1l1111l1l1_opy_ = json.load(open(bstack11ll11l1ll_opy_, bstack111lll_opy_ (u"ࠧࡳࡤࠪ੤")))
    if md5_hash in bstack1l1111l1l1_opy_:
      bstack1l11111ll_opy_ = bstack1l1111l1l1_opy_[md5_hash]
      bstack111l1l1l1_opy_ = datetime.datetime.now()
      bstack11l11ll1_opy_ = datetime.datetime.strptime(bstack1l11111ll_opy_[bstack111lll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ੥")], bstack111lll_opy_ (u"ࠩࠨࡨ࠴ࠫ࡭࠰ࠧ࡜ࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭੦"))
      if (bstack111l1l1l1_opy_ - bstack11l11ll1_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1l11111ll_opy_[bstack111lll_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ੧")]):
        return None
      return bstack1l11111ll_opy_[bstack111lll_opy_ (u"ࠫ࡮ࡪࠧ੨")]
  else:
    return None
def bstack1l1l11l1ll_opy_(md5_hash, bstack1llll1ll_opy_):
  bstack11lllllll_opy_ = os.path.join(os.path.expanduser(bstack111lll_opy_ (u"ࠬࢄࠧ੩")), bstack111lll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭੪"))
  if not os.path.exists(bstack11lllllll_opy_):
    os.makedirs(bstack11lllllll_opy_)
  bstack11ll11l1ll_opy_ = os.path.join(os.path.expanduser(bstack111lll_opy_ (u"ࠧࡿࠩ੫")), bstack111lll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ੬"), bstack111lll_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪ੭"))
  bstack11l11l1l11_opy_ = {
    bstack111lll_opy_ (u"ࠪ࡭ࡩ࠭੮"): bstack1llll1ll_opy_,
    bstack111lll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ੯"): datetime.datetime.strftime(datetime.datetime.now(), bstack111lll_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩੰ")),
    bstack111lll_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫੱ"): str(__version__)
  }
  if os.path.exists(bstack11ll11l1ll_opy_):
    bstack1l1111l1l1_opy_ = json.load(open(bstack11ll11l1ll_opy_, bstack111lll_opy_ (u"ࠧࡳࡤࠪੲ")))
  else:
    bstack1l1111l1l1_opy_ = {}
  bstack1l1111l1l1_opy_[md5_hash] = bstack11l11l1l11_opy_
  with open(bstack11ll11l1ll_opy_, bstack111lll_opy_ (u"ࠣࡹ࠮ࠦੳ")) as outfile:
    json.dump(bstack1l1111l1l1_opy_, outfile)
def bstack1l111lll11_opy_(self):
  return
def bstack11l1l1ll1_opy_(self):
  return
def bstack1111111ll_opy_():
  global bstack11l11llll1_opy_
  bstack11l11llll1_opy_ = True
@measure(event_name=EVENTS.bstack111l11ll_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l11l11l_opy_=bstack11l1l1llll_opy_)
def bstack1ll1ll11l_opy_(self):
  global bstack1lllll11l_opy_
  global bstack1l11ll11l1_opy_
  global bstack1l1ll11111_opy_
  try:
    if bstack111lll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩੴ") in bstack1lllll11l_opy_ and self.session_id != None and bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧੵ"), bstack111lll_opy_ (u"ࠫࠬ੶")) != bstack111lll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭੷"):
      bstack11lll11l11_opy_ = bstack111lll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭੸") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack111lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ੹")
      if bstack11lll11l11_opy_ == bstack111lll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ੺"):
        bstack11l111ll1_opy_(logger)
      if self != None:
        bstack1lll11l1ll_opy_(self, bstack11lll11l11_opy_, bstack111lll_opy_ (u"ࠩ࠯ࠤࠬ੻").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack111lll_opy_ (u"ࠪࠫ੼")
    if bstack111lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ੽") in bstack1lllll11l_opy_ and getattr(threading.current_thread(), bstack111lll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ੾"), None):
      bstack1llll1l111_opy_.bstack1ll1ll1ll_opy_(self, bstack1111llll_opy_, logger, wait=True)
    if bstack111lll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭੿") in bstack1lllll11l_opy_:
      if not threading.currentThread().behave_test_status:
        bstack1lll11l1ll_opy_(self, bstack111lll_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ઀"))
      bstack111111l1_opy_.bstack111l1l111_opy_(self)
  except Exception as e:
    logger.debug(bstack111lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࠤઁ") + str(e))
  bstack1l1ll11111_opy_(self)
  self.session_id = None
def bstack1ll1l1ll1_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack1ll11l1lll_opy_
    global bstack1lllll11l_opy_
    command_executor = kwargs.get(bstack111lll_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠬં"), bstack111lll_opy_ (u"ࠪࠫઃ"))
    bstack1l1llll1l1_opy_ = False
    if type(command_executor) == str and bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧ઄") in command_executor:
      bstack1l1llll1l1_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨઅ") in str(getattr(command_executor, bstack111lll_opy_ (u"࠭࡟ࡶࡴ࡯ࠫઆ"), bstack111lll_opy_ (u"ࠧࠨઇ"))):
      bstack1l1llll1l1_opy_ = True
    else:
      kwargs = bstack1l11l11ll1_opy_.bstack1ll11111ll_opy_(bstack11l11l111_opy_=kwargs, config=CONFIG)
      return bstack1l1l11111l_opy_(self, *args, **kwargs)
    if bstack1l1llll1l1_opy_:
      bstack11ll1ll1ll_opy_ = bstack1lll1l1l_opy_.bstack1l1ll1lll1_opy_(CONFIG, bstack1lllll11l_opy_)
      if kwargs.get(bstack111lll_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩઈ")):
        kwargs[bstack111lll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪઉ")] = bstack1ll11l1lll_opy_(kwargs[bstack111lll_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫઊ")], bstack1lllll11l_opy_, CONFIG, bstack11ll1ll1ll_opy_)
      elif kwargs.get(bstack111lll_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫઋ")):
        kwargs[bstack111lll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬઌ")] = bstack1ll11l1lll_opy_(kwargs[bstack111lll_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ઍ")], bstack1lllll11l_opy_, CONFIG, bstack11ll1ll1ll_opy_)
  except Exception as e:
    logger.error(bstack111lll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩࡧࡱࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡕࡇࡏࠥࡩࡡࡱࡵ࠽ࠤࢀࢃࠢ઎").format(str(e)))
  return bstack1l1l11111l_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack111ll11l_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l11l11l_opy_=bstack11l1l1llll_opy_)
def bstack1ll11l1ll1_opy_(self, command_executor=bstack111lll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰࠳࠵࠻࠳࠶࠮࠱࠰࠴࠾࠹࠺࠴࠵ࠤએ"), *args, **kwargs):
  global bstack1l11ll11l1_opy_
  global bstack1ll11111l_opy_
  bstack1l1l1llll_opy_ = bstack1ll1l1ll1_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack11l1ll111_opy_.on():
    return bstack1l1l1llll_opy_
  try:
    logger.debug(bstack111lll_opy_ (u"ࠩࡆࡳࡲࡳࡡ࡯ࡦࠣࡉࡽ࡫ࡣࡶࡶࡲࡶࠥࡽࡨࡦࡰࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡩࡴࠢࡩࡥࡱࡹࡥࠡ࠯ࠣࡿࢂ࠭ઐ").format(str(command_executor)))
    logger.debug(bstack111lll_opy_ (u"ࠪࡌࡺࡨࠠࡖࡔࡏࠤ࡮ࡹࠠ࠮ࠢࡾࢁࠬઑ").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧ઒") in command_executor._url:
      bstack1ll1l11ll_opy_.bstack1lll1llll1_opy_(bstack111lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ઓ"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩઔ") in command_executor):
    bstack1ll1l11ll_opy_.bstack1lll1llll1_opy_(bstack111lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨક"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack111l1lll1_opy_ = getattr(threading.current_thread(), bstack111lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡕࡧࡶࡸࡒ࡫ࡴࡢࠩખ"), None)
  bstack1lll1lll11_opy_ = {}
  if self.capabilities is not None:
    bstack1lll1lll11_opy_[bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡲࡦࡳࡥࠨગ")] = self.capabilities.get(bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨઘ"))
    bstack1lll1lll11_opy_[bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ઙ")] = self.capabilities.get(bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ચ"))
    bstack1lll1lll11_opy_[bstack111lll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡥ࡯ࡱࡶ࡬ࡳࡳࡹࠧછ")] = self.capabilities.get(bstack111lll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬજ"))
  if CONFIG.get(bstack111lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨઝ"), False) and bstack1l11l11ll1_opy_.bstack1lll11llll_opy_(bstack1lll1lll11_opy_):
    threading.current_thread().a11yPlatform = True
  if bstack111lll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩઞ") in bstack1lllll11l_opy_ or bstack111lll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩટ") in bstack1lllll11l_opy_:
    bstack11111ll1l_opy_.bstack111111lll_opy_(self)
  if bstack111lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫઠ") in bstack1lllll11l_opy_ and bstack111l1lll1_opy_ and bstack111l1lll1_opy_.get(bstack111lll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬડ"), bstack111lll_opy_ (u"࠭ࠧઢ")) == bstack111lll_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨણ"):
    bstack11111ll1l_opy_.bstack111111lll_opy_(self)
  bstack1l11ll11l1_opy_ = self.session_id
  bstack1ll11111l_opy_.append(self)
  return bstack1l1l1llll_opy_
def bstack111lll1ll_opy_(args):
  return bstack111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠩત") in str(args)
def bstack1ll1ll11l1_opy_(self, driver_command, *args, **kwargs):
  global bstack1l111l111_opy_
  global bstack1l1l1l1l1_opy_
  bstack1lll11l1_opy_ = bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭થ"), None) and bstack1ll11l1l1l_opy_(
          threading.current_thread(), bstack111lll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩદ"), None)
  bstack1ll1l11l_opy_ = bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫધ"), None) and bstack1ll11l1l1l_opy_(
          threading.current_thread(), bstack111lll_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧન"), None)
  bstack1l1l11ll11_opy_ = getattr(self, bstack111lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭઩"), None) != None and getattr(self, bstack111lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧપ"), None) == True
  if not bstack1l1l1l1l1_opy_ and bstack111lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨફ") in CONFIG and CONFIG[bstack111lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩબ")] == True and bstack11ll1l1ll_opy_.bstack1l1ll1lll_opy_(driver_command) and (bstack1l1l11ll11_opy_ or bstack1lll11l1_opy_) and not bstack111lll1ll_opy_(args):
    try:
      bstack1l1l1l1l1_opy_ = True
      logger.debug(bstack111lll_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡾࢁࠬભ").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack111lll_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡧࡵࡪࡴࡸ࡭ࠡࡵࡦࡥࡳࠦࡻࡾࠩમ").format(str(err)))
    bstack1l1l1l1l1_opy_ = False
  response = bstack1l111l111_opy_(self, driver_command, *args, **kwargs)
  if (bstack111lll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫય") in str(bstack1lllll11l_opy_).lower() or bstack111lll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ર") in str(bstack1lllll11l_opy_).lower()) and bstack11l1ll111_opy_.on():
    try:
      if driver_command == bstack111lll_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫ઱"):
        bstack11111ll1l_opy_.bstack1l111lll_opy_({
            bstack111lll_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧલ"): response[bstack111lll_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨળ")],
            bstack111lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ઴"): bstack11111ll1l_opy_.current_test_uuid() if bstack11111ll1l_opy_.current_test_uuid() else bstack11l1ll111_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
@measure(event_name=EVENTS.bstack1l1l1l11l_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l11l11l_opy_=bstack11l1l1llll_opy_)
def bstack11ll111111_opy_(self, command_executor,
             desired_capabilities=None, bstack1ll1l111_opy_=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack1l11ll11l1_opy_
  global bstack11l1l11ll1_opy_
  global bstack11l1l1llll_opy_
  global bstack1lllll111_opy_
  global bstack1ll11ll11_opy_
  global bstack1lllll11l_opy_
  global bstack1l1l11111l_opy_
  global bstack1ll11111l_opy_
  global bstack1l1l11llll_opy_
  global bstack1111llll_opy_
  CONFIG[bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭વ")] = str(bstack1lllll11l_opy_) + str(__version__)
  bstack11ll1lll11_opy_ = os.environ[bstack111lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪશ")]
  bstack11ll1ll1ll_opy_ = bstack1lll1l1l_opy_.bstack1l1ll1lll1_opy_(CONFIG, bstack1lllll11l_opy_)
  CONFIG[bstack111lll_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩષ")] = bstack11ll1lll11_opy_
  CONFIG[bstack111lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩસ")] = bstack11ll1ll1ll_opy_
  if CONFIG.get(bstack111lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨહ"),bstack111lll_opy_ (u"ࠩࠪ઺")) and bstack111lll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ઻") in bstack1lllll11l_opy_:
    CONFIG[bstack111lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶ઼ࠫ")].pop(bstack111lll_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪઽ"), None)
    CONFIG[bstack111lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ા")].pop(bstack111lll_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬિ"), None)
  command_executor = bstack11llll1l1l_opy_()
  logger.debug(bstack11l1ll1ll1_opy_.format(command_executor))
  proxy = bstack1l1l1ll111_opy_(CONFIG, proxy)
  bstack1l11l11l1l_opy_ = 0 if bstack11l1l11ll1_opy_ < 0 else bstack11l1l11ll1_opy_
  try:
    if bstack1lllll111_opy_ is True:
      bstack1l11l11l1l_opy_ = int(multiprocessing.current_process().name)
    elif bstack1ll11ll11_opy_ is True:
      bstack1l11l11l1l_opy_ = int(threading.current_thread().name)
  except:
    bstack1l11l11l1l_opy_ = 0
  bstack11llll1ll1_opy_ = bstack1l1lllllll_opy_(CONFIG, bstack1l11l11l1l_opy_)
  logger.debug(bstack11lll11lll_opy_.format(str(bstack11llll1ll1_opy_)))
  if bstack111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬી") in CONFIG and bstack1ll111ll1_opy_(CONFIG[bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ુ")]):
    bstack1lll111l1l_opy_(bstack11llll1ll1_opy_)
  if bstack1l11l11ll1_opy_.bstack1111111l1_opy_(CONFIG, bstack1l11l11l1l_opy_) and bstack1l11l11ll1_opy_.bstack111l1111l_opy_(bstack11llll1ll1_opy_, options, desired_capabilities, CONFIG):
    threading.current_thread().a11yPlatform = True
    if (cli.accessibility is None or not cli.accessibility.is_enabled()):
      bstack1l11l11ll1_opy_.set_capabilities(bstack11llll1ll1_opy_, CONFIG)
  if desired_capabilities:
    bstack1llll111ll_opy_ = bstack1lllllll1_opy_(desired_capabilities)
    bstack1llll111ll_opy_[bstack111lll_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪૂ")] = bstack1ll1lll1ll_opy_(CONFIG)
    bstack11l1l111l1_opy_ = bstack1l1lllllll_opy_(bstack1llll111ll_opy_)
    if bstack11l1l111l1_opy_:
      bstack11llll1ll1_opy_ = update(bstack11l1l111l1_opy_, bstack11llll1ll1_opy_)
    desired_capabilities = None
  if options:
    bstack1111ll11l_opy_(options, bstack11llll1ll1_opy_)
  if not options:
    options = bstack1ll11l1l11_opy_(bstack11llll1ll1_opy_)
  bstack1111llll_opy_ = CONFIG.get(bstack111lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧૃ"))[bstack1l11l11l1l_opy_]
  if proxy and bstack11l1ll1ll_opy_() >= version.parse(bstack111lll_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬૄ")):
    options.proxy(proxy)
  if options and bstack11l1ll1ll_opy_() >= version.parse(bstack111lll_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬૅ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack11l1ll1ll_opy_() < version.parse(bstack111lll_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭૆")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack11llll1ll1_opy_)
  logger.info(bstack11lll11l1l_opy_)
  bstack1ll1l111ll_opy_.end(EVENTS.bstack1l1ll1llll_opy_.value, EVENTS.bstack1l1ll1llll_opy_.value + bstack111lll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣે"), EVENTS.bstack1l1ll1llll_opy_.value + bstack111lll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢૈ"), status=True, failure=None, test_name=bstack11l1l1llll_opy_)
  if bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡵࡸ࡯ࡧ࡫࡯ࡩࠬૉ") in kwargs:
    del kwargs[bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡶࡲࡰࡨ࡬ࡰࡪ࠭૊")]
  if bstack11l1ll1ll_opy_() >= version.parse(bstack111lll_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬો")):
    bstack1l1l11111l_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
  elif bstack11l1ll1ll_opy_() >= version.parse(bstack111lll_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬૌ")):
    bstack1l1l11111l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              bstack1ll1l111_opy_=bstack1ll1l111_opy_, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack11l1ll1ll_opy_() >= version.parse(bstack111lll_opy_ (u"ࠧ࠳࠰࠸࠷࠳࠶્ࠧ")):
    bstack1l1l11111l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              bstack1ll1l111_opy_=bstack1ll1l111_opy_, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1l1l11111l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              bstack1ll1l111_opy_=bstack1ll1l111_opy_, proxy=proxy,
              keep_alive=keep_alive)
  if bstack1l11l11ll1_opy_.bstack1111111l1_opy_(CONFIG, bstack1l11l11l1l_opy_) and bstack1l11l11ll1_opy_.bstack111l1111l_opy_(self.caps, options, desired_capabilities):
    if CONFIG[bstack111lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ૎")][bstack111lll_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨ૏")] == True:
      threading.current_thread().appA11yPlatform = True
      if cli.accessibility is None or not cli.accessibility.is_enabled():
        bstack1l11l11ll1_opy_.set_capabilities(bstack11llll1ll1_opy_, CONFIG)
  try:
    bstack1llll1ll1l_opy_ = bstack111lll_opy_ (u"ࠪࠫૐ")
    if bstack11l1ll1ll_opy_() >= version.parse(bstack111lll_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࡥ࠵ࠬ૑")):
      if self.caps is not None:
        bstack1llll1ll1l_opy_ = self.caps.get(bstack111lll_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧ૒"))
    else:
      if self.capabilities is not None:
        bstack1llll1ll1l_opy_ = self.capabilities.get(bstack111lll_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨ૓"))
    if bstack1llll1ll1l_opy_:
      bstack111l11lll_opy_(bstack1llll1ll1l_opy_)
      if bstack11l1ll1ll_opy_() <= version.parse(bstack111lll_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧ૔")):
        self.command_executor._url = bstack111lll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ૕") + bstack11ll1111ll_opy_ + bstack111lll_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨ૖")
      else:
        self.command_executor._url = bstack111lll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ૗") + bstack1llll1ll1l_opy_ + bstack111lll_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧ૘")
      logger.debug(bstack11lll11l1_opy_.format(bstack1llll1ll1l_opy_))
    else:
      logger.debug(bstack1111l111l_opy_.format(bstack111lll_opy_ (u"ࠧࡕࡰࡵ࡫ࡰࡥࡱࠦࡈࡶࡤࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨ૙")))
  except Exception as e:
    logger.debug(bstack1111l111l_opy_.format(e))
  if bstack111lll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ૚") in bstack1lllll11l_opy_:
    bstack1l1l1llll1_opy_(bstack11l1l11ll1_opy_, bstack1l1l11llll_opy_)
  bstack1l11ll11l1_opy_ = self.session_id
  if bstack111lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ૛") in bstack1lllll11l_opy_ or bstack111lll_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ૜") in bstack1lllll11l_opy_ or bstack111lll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ૝") in bstack1lllll11l_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack111l1lll1_opy_ = getattr(threading.current_thread(), bstack111lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡗࡩࡸࡺࡍࡦࡶࡤࠫ૞"), None)
  if bstack111lll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ૟") in bstack1lllll11l_opy_ or bstack111lll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫૠ") in bstack1lllll11l_opy_:
    bstack11111ll1l_opy_.bstack111111lll_opy_(self)
  if bstack111lll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ૡ") in bstack1lllll11l_opy_ and bstack111l1lll1_opy_ and bstack111l1lll1_opy_.get(bstack111lll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧૢ"), bstack111lll_opy_ (u"ࠨࠩૣ")) == bstack111lll_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ૤"):
    bstack11111ll1l_opy_.bstack111111lll_opy_(self)
  bstack1ll11111l_opy_.append(self)
  if bstack111lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭૥") in CONFIG and bstack111lll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ૦") in CONFIG[bstack111lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ૧")][bstack1l11l11l1l_opy_]:
    bstack11l1l1llll_opy_ = CONFIG[bstack111lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ૨")][bstack1l11l11l1l_opy_][bstack111lll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ૩")]
  logger.debug(bstack1l1l1lll1l_opy_.format(bstack1l11ll11l1_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    from browserstack_sdk.__init__ import bstack1ll1111lll_opy_
    def bstack11ll11llll_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1lll1111_opy_
      if(bstack111lll_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࠮࡫ࡵࠥ૪") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack111lll_opy_ (u"ࠩࢁࠫ૫")), bstack111lll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ૬"), bstack111lll_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭૭")), bstack111lll_opy_ (u"ࠬࡽࠧ૮")) as fp:
          fp.write(bstack111lll_opy_ (u"ࠨࠢ૯"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack111lll_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤ૰")))):
          with open(args[1], bstack111lll_opy_ (u"ࠨࡴࠪ૱")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack111lll_opy_ (u"ࠩࡤࡷࡾࡴࡣࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡣࡳ࡫ࡷࡑࡣࡪࡩ࠭ࡩ࡯࡯ࡶࡨࡼࡹ࠲ࠠࡱࡣࡪࡩࠥࡃࠠࡷࡱ࡬ࡨࠥ࠶ࠩࠨ૲") in line), None)
            if index is not None:
                lines.insert(index+2, bstack111l1ll11_opy_)
            if bstack111lll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ૳") in CONFIG and str(CONFIG[bstack111lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ૴")]).lower() != bstack111lll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ૵"):
                bstack11ll111l11_opy_ = bstack1ll1111lll_opy_()
                bstack1lllll1ll1_opy_ = bstack111lll_opy_ (u"࠭ࠧࠨࠌ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࠏࡩ࡯࡯ࡵࡷࠤࡧࡹࡴࡢࡥ࡮ࡣࡵࡧࡴࡩࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸ࡣ࠻ࠋࡥࡲࡲࡸࡺࠠࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠲࡟࠾ࠎࡨࡵ࡮ࡴࡶࠣࡴࡤ࡯࡮ࡥࡧࡻࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠲࡞࠽ࠍࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡷࡱ࡯ࡣࡦࠪ࠳࠰ࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳ࠪ࠽ࠍࡧࡴࡴࡳࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣࠫ࠾ࠎ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡱࡧࡵ࡯ࡥ࡫ࠤࡂࠦࡡࡴࡻࡱࡧࠥ࠮࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸ࠯ࠠ࠾ࡀࠣࡿࢀࠐࠠࠡ࡮ࡨࡸࠥࡩࡡࡱࡵ࠾ࠎࠥࠦࡴࡳࡻࠣࡿࢀࠐࠠࠡࠢࠣࡧࡦࡶࡳࠡ࠿ࠣࡎࡘࡕࡎ࠯ࡲࡤࡶࡸ࡫ࠨࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷ࠮ࡁࠊࠡࠢࢀࢁࠥࡩࡡࡵࡥ࡫ࠤ࠭࡫ࡸࠪࠢࡾࡿࠏࠦࠠࠡࠢࡦࡳࡳࡹ࡯࡭ࡧ࠱ࡩࡷࡸ࡯ࡳࠪࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ࠾ࠧ࠲ࠠࡦࡺࠬ࠿ࠏࠦࠠࡾࡿࠍࠤࠥࡸࡥࡵࡷࡵࡲࠥࡧࡷࡢ࡫ࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡨࡵ࡮࡯ࡧࡦࡸ࠭ࢁࡻࠋࠢࠣࠤࠥࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵ࠼ࠣࠫࢀࡩࡤࡱࡗࡵࡰࢂ࠭ࠠࠬࠢࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩ࠭ࠌࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴࠌࠣࠤࢂࢃࠩ࠼ࠌࢀࢁࡀࠐ࠯ࠫࠢࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࠦࠪ࠰ࠌࠪࠫࠬ૶").format(bstack11ll111l11_opy_=bstack11ll111l11_opy_)
            lines.insert(1, bstack1lllll1ll1_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack111lll_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤ૷")), bstack111lll_opy_ (u"ࠨࡹࠪ૸")) as bstack1111ll1l_opy_:
              bstack1111ll1l_opy_.writelines(lines)
        CONFIG[bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫૹ")] = str(bstack1lllll11l_opy_) + str(__version__)
        bstack11ll1lll11_opy_ = os.environ[bstack111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨૺ")]
        bstack11ll1ll1ll_opy_ = bstack1lll1l1l_opy_.bstack1l1ll1lll1_opy_(CONFIG, bstack1lllll11l_opy_)
        CONFIG[bstack111lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧૻ")] = bstack11ll1lll11_opy_
        CONFIG[bstack111lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧૼ")] = bstack11ll1ll1ll_opy_
        bstack1l11l11l1l_opy_ = 0 if bstack11l1l11ll1_opy_ < 0 else bstack11l1l11ll1_opy_
        try:
          if bstack1lllll111_opy_ is True:
            bstack1l11l11l1l_opy_ = int(multiprocessing.current_process().name)
          elif bstack1ll11ll11_opy_ is True:
            bstack1l11l11l1l_opy_ = int(threading.current_thread().name)
        except:
          bstack1l11l11l1l_opy_ = 0
        CONFIG[bstack111lll_opy_ (u"ࠨࡵࡴࡧ࡚࠷ࡈࠨ૽")] = False
        CONFIG[bstack111lll_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ૾")] = True
        bstack11llll1ll1_opy_ = bstack1l1lllllll_opy_(CONFIG, bstack1l11l11l1l_opy_)
        logger.debug(bstack11lll11lll_opy_.format(str(bstack11llll1ll1_opy_)))
        if CONFIG.get(bstack111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ૿")):
          bstack1lll111l1l_opy_(bstack11llll1ll1_opy_)
        if bstack111lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ଀") in CONFIG and bstack111lll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨଁ") in CONFIG[bstack111lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଂ")][bstack1l11l11l1l_opy_]:
          bstack11l1l1llll_opy_ = CONFIG[bstack111lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨଃ")][bstack1l11l11l1l_opy_][bstack111lll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ଄")]
        args.append(os.path.join(os.path.expanduser(bstack111lll_opy_ (u"ࠧࡿࠩଅ")), bstack111lll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨଆ"), bstack111lll_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫଇ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack11llll1ll1_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack111lll_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧଈ"))
      bstack1lll1111_opy_ = True
      return bstack1ll11ll1l_opy_(self, args, bufsize=bufsize, executable=executable,
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
  def bstack1l1l1l1lll_opy_(self,
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
    global bstack11l1l11ll1_opy_
    global bstack11l1l1llll_opy_
    global bstack1lllll111_opy_
    global bstack1ll11ll11_opy_
    global bstack1lllll11l_opy_
    CONFIG[bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ଉ")] = str(bstack1lllll11l_opy_) + str(__version__)
    bstack11ll1lll11_opy_ = os.environ[bstack111lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪଊ")]
    bstack11ll1ll1ll_opy_ = bstack1lll1l1l_opy_.bstack1l1ll1lll1_opy_(CONFIG, bstack1lllll11l_opy_)
    CONFIG[bstack111lll_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩଋ")] = bstack11ll1lll11_opy_
    CONFIG[bstack111lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩଌ")] = bstack11ll1ll1ll_opy_
    bstack1l11l11l1l_opy_ = 0 if bstack11l1l11ll1_opy_ < 0 else bstack11l1l11ll1_opy_
    try:
      if bstack1lllll111_opy_ is True:
        bstack1l11l11l1l_opy_ = int(multiprocessing.current_process().name)
      elif bstack1ll11ll11_opy_ is True:
        bstack1l11l11l1l_opy_ = int(threading.current_thread().name)
    except:
      bstack1l11l11l1l_opy_ = 0
    CONFIG[bstack111lll_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢ଍")] = True
    bstack11llll1ll1_opy_ = bstack1l1lllllll_opy_(CONFIG, bstack1l11l11l1l_opy_)
    logger.debug(bstack11lll11lll_opy_.format(str(bstack11llll1ll1_opy_)))
    if CONFIG.get(bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭଎")):
      bstack1lll111l1l_opy_(bstack11llll1ll1_opy_)
    if bstack111lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ଏ") in CONFIG and bstack111lll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩଐ") in CONFIG[bstack111lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ଑")][bstack1l11l11l1l_opy_]:
      bstack11l1l1llll_opy_ = CONFIG[bstack111lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ଒")][bstack1l11l11l1l_opy_][bstack111lll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬଓ")]
    import urllib
    import json
    if bstack111lll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬଔ") in CONFIG and str(CONFIG[bstack111lll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭କ")]).lower() != bstack111lll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩଖ"):
        bstack1ll1l1111l_opy_ = bstack1ll1111lll_opy_()
        bstack11ll111l11_opy_ = bstack1ll1l1111l_opy_ + urllib.parse.quote(json.dumps(bstack11llll1ll1_opy_))
    else:
        bstack11ll111l11_opy_ = bstack111lll_opy_ (u"ࠫࡼࡹࡳ࠻࠱࠲ࡧࡩࡶ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠿ࡤࡣࡳࡷࡂ࠭ଗ") + urllib.parse.quote(json.dumps(bstack11llll1ll1_opy_))
    browser = self.connect(bstack11ll111l11_opy_)
    return browser
except Exception as e:
    pass
def bstack1ll1lll11l_opy_():
    global bstack1lll1111_opy_
    global bstack1lllll11l_opy_
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1ll1lll11_opy_
        global bstack1ll1l11ll_opy_
        if not bstack111lll111_opy_:
          global bstack1lll1lllll_opy_
          if not bstack1lll1lllll_opy_:
            from bstack_utils.helper import bstack11l1llll1_opy_, bstack1lll11ll11_opy_, bstack1ll11l111_opy_
            bstack1lll1lllll_opy_ = bstack11l1llll1_opy_()
            bstack1lll11ll11_opy_(bstack1lllll11l_opy_)
            bstack11ll1ll1ll_opy_ = bstack1lll1l1l_opy_.bstack1l1ll1lll1_opy_(CONFIG, bstack1lllll11l_opy_)
            bstack1ll1l11ll_opy_.bstack1lll1llll1_opy_(bstack111lll_opy_ (u"ࠧࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡓࡖࡔࡊࡕࡄࡖࡢࡑࡆࡖࠢଘ"), bstack11ll1ll1ll_opy_)
          BrowserType.connect = bstack1ll1lll11_opy_
          return
        BrowserType.launch = bstack1l1l1l1lll_opy_
        bstack1lll1111_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack11ll11llll_opy_
      bstack1lll1111_opy_ = True
    except Exception as e:
      pass
def bstack1ll111l1l_opy_(context, bstack1111llll1_opy_):
  try:
    context.page.evaluate(bstack111lll_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢଙ"), bstack111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫଚ")+ json.dumps(bstack1111llll1_opy_) + bstack111lll_opy_ (u"ࠣࡿࢀࠦଛ"))
  except Exception as e:
    logger.debug(bstack111lll_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃ࠺ࠡࡽࢀࠦଜ").format(str(e), traceback.format_exc()))
def bstack111lllll1_opy_(context, message, level):
  try:
    context.page.evaluate(bstack111lll_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦଝ"), bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩଞ") + json.dumps(message) + bstack111lll_opy_ (u"ࠬ࠲ࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠨଟ") + json.dumps(level) + bstack111lll_opy_ (u"࠭ࡽࡾࠩଠ"))
  except Exception as e:
    logger.debug(bstack111lll_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠࡼࡿ࠽ࠤࢀࢃࠢଡ").format(str(e), traceback.format_exc()))
@measure(event_name=EVENTS.bstack11l1l111ll_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l11l11l_opy_=bstack11l1l1llll_opy_)
def bstack1ll111lll1_opy_(self, url):
  global bstack1llll11ll_opy_
  try:
    bstack11ll111l1l_opy_(url)
  except Exception as err:
    logger.debug(bstack11ll11l11_opy_.format(str(err)))
  try:
    bstack1llll11ll_opy_(self, url)
  except Exception as e:
    try:
      bstack111l1lll_opy_ = str(e)
      if any(err_msg in bstack111l1lll_opy_ for err_msg in bstack1ll11ll11l_opy_):
        bstack11ll111l1l_opy_(url, True)
    except Exception as err:
      logger.debug(bstack11ll11l11_opy_.format(str(err)))
    raise e
def bstack1ll1ll111l_opy_(self):
  global bstack11l11l1ll_opy_
  bstack11l11l1ll_opy_ = self
  return
def bstack1lllll1ll_opy_(self):
  global bstack1l1l1l1ll1_opy_
  bstack1l1l1l1ll1_opy_ = self
  return
def bstack111ll1111_opy_(test_name, bstack11l1l11l11_opy_):
  global CONFIG
  if percy.bstack11l1ll11l1_opy_() == bstack111lll_opy_ (u"ࠣࡶࡵࡹࡪࠨଢ"):
    bstack11ll11l1l1_opy_ = os.path.relpath(bstack11l1l11l11_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack11ll11l1l1_opy_)
    bstack11l11l11l_opy_ = suite_name + bstack111lll_opy_ (u"ࠤ࠰ࠦଣ") + test_name
    threading.current_thread().percySessionName = bstack11l11l11l_opy_
def bstack1l11l11ll_opy_(self, test, *args, **kwargs):
  global bstack1l1l111ll_opy_
  test_name = None
  bstack11l1l11l11_opy_ = None
  if test:
    test_name = str(test.name)
    bstack11l1l11l11_opy_ = str(test.source)
  bstack111ll1111_opy_(test_name, bstack11l1l11l11_opy_)
  bstack1l1l111ll_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.bstack111l1l1l_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l11l11l_opy_=bstack11l1l1llll_opy_)
def bstack1l1l111l1l_opy_(driver, bstack11l11l11l_opy_):
  if not bstack1l11ll111l_opy_ and bstack11l11l11l_opy_:
      bstack1lll1lll_opy_ = {
          bstack111lll_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪତ"): bstack111lll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬଥ"),
          bstack111lll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨଦ"): {
              bstack111lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫଧ"): bstack11l11l11l_opy_
          }
      }
      bstack11l1ll1lll_opy_ = bstack111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬନ").format(json.dumps(bstack1lll1lll_opy_))
      driver.execute_script(bstack11l1ll1lll_opy_)
  if bstack1ll11111l1_opy_:
      bstack11l1ll111l_opy_ = {
          bstack111lll_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨ଩"): bstack111lll_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫପ"),
          bstack111lll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ଫ"): {
              bstack111lll_opy_ (u"ࠫࡩࡧࡴࡢࠩବ"): bstack11l11l11l_opy_ + bstack111lll_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧଭ"),
              bstack111lll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬମ"): bstack111lll_opy_ (u"ࠧࡪࡰࡩࡳࠬଯ")
          }
      }
      if bstack1ll11111l1_opy_.status == bstack111lll_opy_ (u"ࠨࡒࡄࡗࡘ࠭ର"):
          bstack1l111111ll_opy_ = bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧ଱").format(json.dumps(bstack11l1ll111l_opy_))
          driver.execute_script(bstack1l111111ll_opy_)
          bstack1lll11l1ll_opy_(driver, bstack111lll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪଲ"))
      elif bstack1ll11111l1_opy_.status == bstack111lll_opy_ (u"ࠫࡋࡇࡉࡍࠩଳ"):
          reason = bstack111lll_opy_ (u"ࠧࠨ଴")
          bstack11ll1lll1_opy_ = bstack11l11l11l_opy_ + bstack111lll_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠧଵ")
          if bstack1ll11111l1_opy_.message:
              reason = str(bstack1ll11111l1_opy_.message)
              bstack11ll1lll1_opy_ = bstack11ll1lll1_opy_ + bstack111lll_opy_ (u"ࠧࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶ࠿ࠦࠧଶ") + reason
          bstack11l1ll111l_opy_[bstack111lll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫଷ")] = {
              bstack111lll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨସ"): bstack111lll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩହ"),
              bstack111lll_opy_ (u"ࠫࡩࡧࡴࡢࠩ଺"): bstack11ll1lll1_opy_
          }
          bstack1l111111ll_opy_ = bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪ଻").format(json.dumps(bstack11l1ll111l_opy_))
          driver.execute_script(bstack1l111111ll_opy_)
          bstack1lll11l1ll_opy_(driver, bstack111lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ଼࠭"), reason)
          bstack1l1111lll1_opy_(reason, str(bstack1ll11111l1_opy_), str(bstack11l1l11ll1_opy_), logger)
@measure(event_name=EVENTS.bstack11l1111ll1_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l11l11l_opy_=bstack11l1l1llll_opy_)
def bstack111111111_opy_(driver, test):
  if percy.bstack11l1ll11l1_opy_() == bstack111lll_opy_ (u"ࠢࡵࡴࡸࡩࠧଽ") and percy.bstack1ll111ll11_opy_() == bstack111lll_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥା"):
      bstack1l1ll111l1_opy_ = bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠩࡳࡩࡷࡩࡹࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬି"), None)
      bstack1l1111l11l_opy_(driver, bstack1l1ll111l1_opy_, test)
  if (bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧୀ"), None) and
      bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪୁ"), None)) or (
      bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠬ࡯ࡳࡂࡲࡳࡅ࠶࠷ࡹࡕࡧࡶࡸࠬୂ"), None) and
      bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨୃ"), None)):
      logger.info(bstack111lll_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠥࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡪࡵࠣࡹࡳࡪࡥࡳࡹࡤࡽ࠳ࠦࠢୄ"))
      bstack1l11l11ll1_opy_.bstack1ll1ll1l11_opy_(driver, name=test.name, path=test.source)
def bstack1lll1lll1_opy_(test, bstack11l11l11l_opy_):
    try:
      bstack11ll1ll1_opy_ = datetime.datetime.now()
      data = {}
      if test:
        data[bstack111lll_opy_ (u"ࠨࡰࡤࡱࡪ࠭୅")] = bstack11l11l11l_opy_
      if bstack1ll11111l1_opy_:
        if bstack1ll11111l1_opy_.status == bstack111lll_opy_ (u"ࠩࡓࡅࡘ࡙ࠧ୆"):
          data[bstack111lll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪେ")] = bstack111lll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫୈ")
        elif bstack1ll11111l1_opy_.status == bstack111lll_opy_ (u"ࠬࡌࡁࡊࡎࠪ୉"):
          data[bstack111lll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭୊")] = bstack111lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧୋ")
          if bstack1ll11111l1_opy_.message:
            data[bstack111lll_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨୌ")] = str(bstack1ll11111l1_opy_.message)
      user = CONFIG[bstack111lll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨ୍ࠫ")]
      key = CONFIG[bstack111lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭୎")]
      host = bstack111llll1l_opy_(cli.config, [bstack111lll_opy_ (u"ࠦࡦࡶࡩࡴࠤ୏"), bstack111lll_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫ࠢ୐"), bstack111lll_opy_ (u"ࠨࡡࡱ࡫ࠥ୑")], bstack111lll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠣ୒"))
      url = bstack111lll_opy_ (u"ࠨࡽࢀ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡳࡦࡵࡶ࡭ࡴࡴࡳ࠰ࡽࢀ࠲࡯ࡹ࡯࡯ࠩ୓").format(host, bstack1l11ll11l1_opy_)
      headers = {
        bstack111lll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨ୔"): bstack111lll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭୕"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers, auth=(user, key))
        cli.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼ࡸࡴࡩࡧࡴࡦࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡵࡷࡥࡹࡻࡳࠣୖ"), datetime.datetime.now() - bstack11ll1ll1_opy_)
    except Exception as e:
      logger.error(bstack1l11l1lll_opy_.format(str(e)))
def bstack11ll11111_opy_(test, bstack11l11l11l_opy_):
  global CONFIG
  global bstack1l1l1l1ll1_opy_
  global bstack11l11l1ll_opy_
  global bstack1l11ll11l1_opy_
  global bstack1ll11111l1_opy_
  global bstack11l1l1llll_opy_
  global bstack1lll11lll1_opy_
  global bstack11ll1l111l_opy_
  global bstack11lll111ll_opy_
  global bstack11l1l11l1l_opy_
  global bstack1ll11111l_opy_
  global bstack1111llll_opy_
  try:
    if not bstack1l11ll11l1_opy_:
      with open(os.path.join(os.path.expanduser(bstack111lll_opy_ (u"ࠬࢄࠧୗ")), bstack111lll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭୘"), bstack111lll_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩ୙"))) as f:
        bstack1llllll1l_opy_ = json.loads(bstack111lll_opy_ (u"ࠣࡽࠥ୚") + f.read().strip() + bstack111lll_opy_ (u"ࠩࠥࡼࠧࡀࠠࠣࡻࠥࠫ୛") + bstack111lll_opy_ (u"ࠥࢁࠧଡ଼"))
        bstack1l11ll11l1_opy_ = bstack1llllll1l_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1ll11111l_opy_:
    for driver in bstack1ll11111l_opy_:
      if bstack1l11ll11l1_opy_ == driver.session_id:
        if test:
          bstack111111111_opy_(driver, test)
        bstack1l1l111l1l_opy_(driver, bstack11l11l11l_opy_)
  elif bstack1l11ll11l1_opy_:
    bstack1lll1lll1_opy_(test, bstack11l11l11l_opy_)
  if bstack1l1l1l1ll1_opy_:
    bstack11ll1l111l_opy_(bstack1l1l1l1ll1_opy_)
  if bstack11l11l1ll_opy_:
    bstack11lll111ll_opy_(bstack11l11l1ll_opy_)
  if bstack11l11llll1_opy_:
    bstack11l1l11l1l_opy_()
def bstack1l111ll1ll_opy_(self, test, *args, **kwargs):
  bstack11l11l11l_opy_ = None
  if test:
    bstack11l11l11l_opy_ = str(test.name)
  bstack11ll11111_opy_(test, bstack11l11l11l_opy_)
  bstack1lll11lll1_opy_(self, test, *args, **kwargs)
def bstack11lll1l11_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1ll1l11lll_opy_
  global CONFIG
  global bstack1ll11111l_opy_
  global bstack1l11ll11l1_opy_
  bstack111l1ll1l_opy_ = None
  try:
    if bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪଢ଼"), None) or bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ୞"), None):
      try:
        if not bstack1l11ll11l1_opy_:
          with open(os.path.join(os.path.expanduser(bstack111lll_opy_ (u"࠭ࡾࠨୟ")), bstack111lll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧୠ"), bstack111lll_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪୡ"))) as f:
            bstack1llllll1l_opy_ = json.loads(bstack111lll_opy_ (u"ࠤࡾࠦୢ") + f.read().strip() + bstack111lll_opy_ (u"ࠪࠦࡽࠨ࠺ࠡࠤࡼࠦࠬୣ") + bstack111lll_opy_ (u"ࠦࢂࠨ୤"))
            bstack1l11ll11l1_opy_ = bstack1llllll1l_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack1ll11111l_opy_:
        for driver in bstack1ll11111l_opy_:
          if bstack1l11ll11l1_opy_ == driver.session_id:
            bstack111l1ll1l_opy_ = driver
    bstack111l11l1l_opy_ = bstack1l11l11ll1_opy_.bstack11lllllll1_opy_(test.tags)
    if bstack111l1ll1l_opy_:
      threading.current_thread().isA11yTest = bstack1l11l11ll1_opy_.bstack1ll1l1l1l1_opy_(bstack111l1ll1l_opy_, bstack111l11l1l_opy_)
      threading.current_thread().isAppA11yTest = bstack1l11l11ll1_opy_.bstack1ll1l1l1l1_opy_(bstack111l1ll1l_opy_, bstack111l11l1l_opy_)
    else:
      threading.current_thread().isA11yTest = bstack111l11l1l_opy_
      threading.current_thread().isAppA11yTest = bstack111l11l1l_opy_
  except:
    pass
  bstack1ll1l11lll_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1ll11111l1_opy_
  try:
    bstack1ll11111l1_opy_ = self._test
  except:
    bstack1ll11111l1_opy_ = self.test
def bstack11ll1l11l_opy_():
  global bstack111llll1_opy_
  try:
    if os.path.exists(bstack111llll1_opy_):
      os.remove(bstack111llll1_opy_)
  except Exception as e:
    logger.debug(bstack111lll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨ୥") + str(e))
def bstack1l111l1ll1_opy_():
  global bstack111llll1_opy_
  bstack11l1l1l1_opy_ = {}
  try:
    if not os.path.isfile(bstack111llll1_opy_):
      with open(bstack111llll1_opy_, bstack111lll_opy_ (u"࠭ࡷࠨ୦")):
        pass
      with open(bstack111llll1_opy_, bstack111lll_opy_ (u"ࠢࡸ࠭ࠥ୧")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack111llll1_opy_):
      bstack11l1l1l1_opy_ = json.load(open(bstack111llll1_opy_, bstack111lll_opy_ (u"ࠨࡴࡥࠫ୨")))
  except Exception as e:
    logger.debug(bstack111lll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡷ࡫ࡡࡥ࡫ࡱ࡫ࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫ୩") + str(e))
  finally:
    return bstack11l1l1l1_opy_
def bstack1l1l1llll1_opy_(platform_index, item_index):
  global bstack111llll1_opy_
  try:
    bstack11l1l1l1_opy_ = bstack1l111l1ll1_opy_()
    bstack11l1l1l1_opy_[item_index] = platform_index
    with open(bstack111llll1_opy_, bstack111lll_opy_ (u"ࠥࡻ࠰ࠨ୪")) as outfile:
      json.dump(bstack11l1l1l1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack111lll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡷࡳ࡫ࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺ࠡࠩ୫") + str(e))
def bstack11l1lll11l_opy_(bstack1l11l1l1ll_opy_):
  global CONFIG
  bstack1l1l1ll1_opy_ = bstack111lll_opy_ (u"ࠬ࠭୬")
  if not bstack111lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ୭") in CONFIG:
    logger.info(bstack111lll_opy_ (u"ࠧࡏࡱࠣࡴࡱࡧࡴࡧࡱࡵࡱࡸࠦࡰࡢࡵࡶࡩࡩࠦࡵ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡪࡩࡳ࡫ࡲࡢࡶࡨࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫ࡵࡲࠡࡔࡲࡦࡴࡺࠠࡳࡷࡱࠫ୮"))
  try:
    platform = CONFIG[bstack111lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ୯")][bstack1l11l1l1ll_opy_]
    if bstack111lll_opy_ (u"ࠩࡲࡷࠬ୰") in platform:
      bstack1l1l1ll1_opy_ += str(platform[bstack111lll_opy_ (u"ࠪࡳࡸ࠭ୱ")]) + bstack111lll_opy_ (u"ࠫ࠱ࠦࠧ୲")
    if bstack111lll_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨ୳") in platform:
      bstack1l1l1ll1_opy_ += str(platform[bstack111lll_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ୴")]) + bstack111lll_opy_ (u"ࠧ࠭ࠢࠪ୵")
    if bstack111lll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬ୶") in platform:
      bstack1l1l1ll1_opy_ += str(platform[bstack111lll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭୷")]) + bstack111lll_opy_ (u"ࠪ࠰ࠥ࠭୸")
    if bstack111lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭୹") in platform:
      bstack1l1l1ll1_opy_ += str(platform[bstack111lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ୺")]) + bstack111lll_opy_ (u"࠭ࠬࠡࠩ୻")
    if bstack111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ୼") in platform:
      bstack1l1l1ll1_opy_ += str(platform[bstack111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭୽")]) + bstack111lll_opy_ (u"ࠩ࠯ࠤࠬ୾")
    if bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ୿") in platform:
      bstack1l1l1ll1_opy_ += str(platform[bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ஀")]) + bstack111lll_opy_ (u"ࠬ࠲ࠠࠨ஁")
  except Exception as e:
    logger.debug(bstack111lll_opy_ (u"࠭ࡓࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡰࡨࡶࡦࡺࡩ࡯ࡩࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡹࡴࡳ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡵࡩࡵࡵࡲࡵࠢࡪࡩࡳ࡫ࡲࡢࡶ࡬ࡳࡳ࠭ஂ") + str(e))
  finally:
    if bstack1l1l1ll1_opy_[len(bstack1l1l1ll1_opy_) - 2:] == bstack111lll_opy_ (u"ࠧ࠭ࠢࠪஃ"):
      bstack1l1l1ll1_opy_ = bstack1l1l1ll1_opy_[:-2]
    return bstack1l1l1ll1_opy_
def bstack11lllll11l_opy_(path, bstack1l1l1ll1_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1l11ll11ll_opy_ = ET.parse(path)
    bstack1lll1llll_opy_ = bstack1l11ll11ll_opy_.getroot()
    bstack111l1l11_opy_ = None
    for suite in bstack1lll1llll_opy_.iter(bstack111lll_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧ஄")):
      if bstack111lll_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩஅ") in suite.attrib:
        suite.attrib[bstack111lll_opy_ (u"ࠪࡲࡦࡳࡥࠨஆ")] += bstack111lll_opy_ (u"ࠫࠥ࠭இ") + bstack1l1l1ll1_opy_
        bstack111l1l11_opy_ = suite
    bstack1lll11l1l1_opy_ = None
    for robot in bstack1lll1llll_opy_.iter(bstack111lll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫஈ")):
      bstack1lll11l1l1_opy_ = robot
    bstack1lll11l11l_opy_ = len(bstack1lll11l1l1_opy_.findall(bstack111lll_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬஉ")))
    if bstack1lll11l11l_opy_ == 1:
      bstack1lll11l1l1_opy_.remove(bstack1lll11l1l1_opy_.findall(bstack111lll_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭ஊ"))[0])
      bstack11l1l11lll_opy_ = ET.Element(bstack111lll_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧ஋"), attrib={bstack111lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ஌"): bstack111lll_opy_ (u"ࠪࡗࡺ࡯ࡴࡦࡵࠪ஍"), bstack111lll_opy_ (u"ࠫ࡮ࡪࠧஎ"): bstack111lll_opy_ (u"ࠬࡹ࠰ࠨஏ")})
      bstack1lll11l1l1_opy_.insert(1, bstack11l1l11lll_opy_)
      bstack111lll1l1_opy_ = None
      for suite in bstack1lll11l1l1_opy_.iter(bstack111lll_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬஐ")):
        bstack111lll1l1_opy_ = suite
      bstack111lll1l1_opy_.append(bstack111l1l11_opy_)
      bstack11ll1lll1l_opy_ = None
      for status in bstack111l1l11_opy_.iter(bstack111lll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ஑")):
        bstack11ll1lll1l_opy_ = status
      bstack111lll1l1_opy_.append(bstack11ll1lll1l_opy_)
    bstack1l11ll11ll_opy_.write(path)
  except Exception as e:
    logger.debug(bstack111lll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡦࡸࡳࡪࡰࡪࠤࡼ࡮ࡩ࡭ࡧࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹ࠭ஒ") + str(e))
def bstack1l1l1ll1l1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack11ll111l1_opy_
  global CONFIG
  if bstack111lll_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡲࡤࡸ࡭ࠨஓ") in options:
    del options[bstack111lll_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࡳࡥࡹ࡮ࠢஔ")]
  bstack11l1l1111l_opy_ = bstack1l111l1ll1_opy_()
  for bstack11ll11ll1l_opy_ in bstack11l1l1111l_opy_.keys():
    path = os.path.join(os.getcwd(), bstack111lll_opy_ (u"ࠫࡵࡧࡢࡰࡶࡢࡶࡪࡹࡵ࡭ࡶࡶࠫக"), str(bstack11ll11ll1l_opy_), bstack111lll_opy_ (u"ࠬࡵࡵࡵࡲࡸࡸ࠳ࡾ࡭࡭ࠩ஖"))
    bstack11lllll11l_opy_(path, bstack11l1lll11l_opy_(bstack11l1l1111l_opy_[bstack11ll11ll1l_opy_]))
  bstack11ll1l11l_opy_()
  return bstack11ll111l1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1l1l1ll1l_opy_(self, ff_profile_dir):
  global bstack11ll1llll_opy_
  if not ff_profile_dir:
    return None
  return bstack11ll1llll_opy_(self, ff_profile_dir)
def bstack1l11l111_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1l1lll11l1_opy_
  bstack1llll111_opy_ = []
  if bstack111lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ஗") in CONFIG:
    bstack1llll111_opy_ = CONFIG[bstack111lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ஘")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack111lll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤங")],
      pabot_args[bstack111lll_opy_ (u"ࠤࡹࡩࡷࡨ࡯ࡴࡧࠥச")],
      argfile,
      pabot_args.get(bstack111lll_opy_ (u"ࠥ࡬࡮ࡼࡥࠣ஛")),
      pabot_args[bstack111lll_opy_ (u"ࠦࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠢஜ")],
      platform[0],
      bstack1l1lll11l1_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack111lll_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡦࡪ࡮ࡨࡷࠧ஝")] or [(bstack111lll_opy_ (u"ࠨࠢஞ"), None)]
    for platform in enumerate(bstack1llll111_opy_)
  ]
def bstack1l111l1ll_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1l1lll1ll1_opy_=bstack111lll_opy_ (u"ࠧࠨட")):
  global bstack11l1ll11_opy_
  self.platform_index = platform_index
  self.bstack1llll11l1l_opy_ = bstack1l1lll1ll1_opy_
  bstack11l1ll11_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1l11lll1l1_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1l111l1l1_opy_
  global bstack1111l11l_opy_
  bstack1l1l111l_opy_ = copy.deepcopy(item)
  if not bstack111lll_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ஠") in item.options:
    bstack1l1l111l_opy_.options[bstack111lll_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ஡")] = []
  bstack1ll11lll_opy_ = bstack1l1l111l_opy_.options[bstack111lll_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ஢")].copy()
  for v in bstack1l1l111l_opy_.options[bstack111lll_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ண")]:
    if bstack111lll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡕࡒࡁࡕࡈࡒࡖࡒࡏࡎࡅࡇ࡛ࠫத") in v:
      bstack1ll11lll_opy_.remove(v)
    if bstack111lll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘ࠭஥") in v:
      bstack1ll11lll_opy_.remove(v)
    if bstack111lll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡄࡆࡈࡏࡓࡈࡇࡌࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ஦") in v:
      bstack1ll11lll_opy_.remove(v)
  bstack1ll11lll_opy_.insert(0, bstack111lll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡑࡎࡄࡘࡋࡕࡒࡎࡋࡑࡈࡊ࡞࠺ࡼࡿࠪ஧").format(bstack1l1l111l_opy_.platform_index))
  bstack1ll11lll_opy_.insert(0, bstack111lll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡆࡈࡊࡑࡕࡃࡂࡎࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗࡀࡻࡾࠩந").format(bstack1l1l111l_opy_.bstack1llll11l1l_opy_))
  bstack1l1l111l_opy_.options[bstack111lll_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬன")] = bstack1ll11lll_opy_
  if bstack1111l11l_opy_:
    bstack1l1l111l_opy_.options[bstack111lll_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ப")].insert(0, bstack111lll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡒࡉࡂࡔࡊࡗ࠿ࢁࡽࠨ஫").format(bstack1111l11l_opy_))
  return bstack1l111l1l1_opy_(caller_id, datasources, is_last, bstack1l1l111l_opy_, outs_dir)
def bstack11l1l1ll11_opy_(command, item_index):
  if bstack1ll1l11ll_opy_.get_property(bstack111lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ஬")):
    os.environ[bstack111lll_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨ஭")] = json.dumps(CONFIG[bstack111lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫம")][item_index % bstack111ll1ll1_opy_])
  global bstack1111l11l_opy_
  if bstack1111l11l_opy_:
    command[0] = command[0].replace(bstack111lll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨய"), bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡶࡨࡰࠦࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠠ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽࠦࠧர") + str(
      item_index) + bstack111lll_opy_ (u"ࠫࠥ࠭ற") + bstack1111l11l_opy_, 1)
  else:
    command[0] = command[0].replace(bstack111lll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫல"),
                                    bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡹࡤ࡬ࠢࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠣ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠢࠪள") + str(item_index), 1)
def bstack1l11ll1111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack11lll1l11l_opy_
  bstack11l1l1ll11_opy_(command, item_index)
  return bstack11lll1l11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack111ll1l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack11lll1l11l_opy_
  bstack11l1l1ll11_opy_(command, item_index)
  return bstack11lll1l11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack11111lll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack11lll1l11l_opy_
  bstack11l1l1ll11_opy_(command, item_index)
  return bstack11lll1l11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack11l111lll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack11lll1l11l_opy_
  bstack11l1l1ll11_opy_(command, item_index)
  return bstack11lll1l11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack1l11111l1l_opy_(self, runner, quiet=False, capture=True):
  global bstack11l111ll_opy_
  bstack11lll1l1ll_opy_ = bstack11l111ll_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack111lll_opy_ (u"ࠧࡦࡺࡦࡩࡵࡺࡩࡰࡰࡢࡥࡷࡸࠧழ")):
      runner.exception_arr = []
    if not hasattr(runner, bstack111lll_opy_ (u"ࠨࡧࡻࡧࡤࡺࡲࡢࡥࡨࡦࡦࡩ࡫ࡠࡣࡵࡶࠬவ")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack11lll1l1ll_opy_
def bstack11lll11ll_opy_(runner, hook_name, context, element, bstack1llll1l1ll_opy_, *args):
  try:
    if runner.hooks.get(hook_name):
      bstack1llllll11_opy_.bstack1l1l111l11_opy_(hook_name, element)
    bstack1llll1l1ll_opy_(runner, hook_name, context, *args)
    if runner.hooks.get(hook_name):
      bstack1llllll11_opy_.bstack1lll11l1l_opy_(element)
      if hook_name not in [bstack111lll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱ࠭ஶ"), bstack111lll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ࠭ஷ")] and args and hasattr(args[0], bstack111lll_opy_ (u"ࠫࡪࡸࡲࡰࡴࡢࡱࡪࡹࡳࡢࡩࡨࠫஸ")):
        args[0].error_message = bstack111lll_opy_ (u"ࠬ࠭ஹ")
  except Exception as e:
    logger.debug(bstack111lll_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢ࡫ࡥࡳࡪ࡬ࡦࠢ࡫ࡳࡴࡱࡳࠡ࡫ࡱࠤࡧ࡫ࡨࡢࡸࡨ࠾ࠥࢁࡽࠨ஺").format(str(e)))
@measure(event_name=EVENTS.bstack1lll111l11_opy_, stage=STAGE.bstack111ll11l1_opy_, hook_type=bstack111lll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࡁ࡭࡮ࠥ஻"), bstack11l11l11l_opy_=bstack11l1l1llll_opy_)
def bstack1l11l11111_opy_(runner, name, context, bstack1llll1l1ll_opy_, *args):
    if runner.hooks.get(bstack111lll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧ஼")).__name__ != bstack111lll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࡥࡤࡦࡨࡤࡹࡱࡺ࡟ࡩࡱࡲ࡯ࠧ஽"):
      bstack11lll11ll_opy_(runner, name, context, runner, bstack1llll1l1ll_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack11ll1llll1_opy_(bstack111lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩா")) else context.browser
      runner.driver_initialised = bstack111lll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣி")
    except Exception as e:
      logger.debug(bstack111lll_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡪࡲࡪࡸࡨࡶࠥ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡳࡦࠢࡤࡸࡹࡸࡩࡣࡷࡷࡩ࠿ࠦࡻࡾࠩீ").format(str(e)))
def bstack1111l1l11_opy_(runner, name, context, bstack1llll1l1ll_opy_, *args):
    bstack11lll11ll_opy_(runner, name, context, context.feature, bstack1llll1l1ll_opy_, *args)
    try:
      if not bstack1l11ll111l_opy_:
        bstack111l1ll1l_opy_ = threading.current_thread().bstackSessionDriver if bstack11ll1llll1_opy_(bstack111lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬு")) else context.browser
        if is_driver_active(bstack111l1ll1l_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack111lll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣூ")
          bstack1111llll1_opy_ = str(runner.feature.name)
          bstack1ll111l1l_opy_(context, bstack1111llll1_opy_)
          bstack111l1ll1l_opy_.execute_script(bstack111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭௃") + json.dumps(bstack1111llll1_opy_) + bstack111lll_opy_ (u"ࠩࢀࢁࠬ௄"))
    except Exception as e:
      logger.debug(bstack111lll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡬ࡥࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪ௅").format(str(e)))
def bstack1lll1l1ll1_opy_(runner, name, context, bstack1llll1l1ll_opy_, *args):
    if hasattr(context, bstack111lll_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ெ")):
        bstack1llllll11_opy_.start_test(context)
    target = context.scenario if hasattr(context, bstack111lll_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧே")) else context.feature
    bstack11lll11ll_opy_(runner, name, context, target, bstack1llll1l1ll_opy_, *args)
@measure(event_name=EVENTS.bstack1l11lll1l_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l11l11l_opy_=bstack11l1l1llll_opy_)
def bstack1lll11l11_opy_(runner, name, context, bstack1llll1l1ll_opy_, *args):
    if len(context.scenario.tags) == 0: bstack1llllll11_opy_.start_test(context)
    bstack11lll11ll_opy_(runner, name, context, context.scenario, bstack1llll1l1ll_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack111111l1_opy_.bstack1l1lll11_opy_(context, *args)
    try:
      bstack111l1ll1l_opy_ = bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬை"), context.browser)
      if is_driver_active(bstack111l1ll1l_opy_):
        bstack11111ll1l_opy_.bstack111111lll_opy_(bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭௉"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack111lll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥொ")
        if (not bstack1l11ll111l_opy_):
          scenario_name = args[0].name
          feature_name = bstack1111llll1_opy_ = str(runner.feature.name)
          bstack1111llll1_opy_ = feature_name + bstack111lll_opy_ (u"ࠩࠣ࠱ࠥ࠭ோ") + scenario_name
          if runner.driver_initialised == bstack111lll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧௌ"):
            bstack1ll111l1l_opy_(context, bstack1111llll1_opy_)
            bstack111l1ll1l_opy_.execute_script(bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺்ࠡࠩ") + json.dumps(bstack1111llll1_opy_) + bstack111lll_opy_ (u"ࠬࢃࡽࠨ௎"))
    except Exception as e:
      logger.debug(bstack111lll_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱ࠽ࠤࢀࢃࠧ௏").format(str(e)))
@measure(event_name=EVENTS.bstack1lll111l11_opy_, stage=STAGE.bstack111ll11l1_opy_, hook_type=bstack111lll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࡓࡵࡧࡳࠦௐ"), bstack11l11l11l_opy_=bstack11l1l1llll_opy_)
def bstack11l1llll_opy_(runner, name, context, bstack1llll1l1ll_opy_, *args):
    bstack11lll11ll_opy_(runner, name, context, args[0], bstack1llll1l1ll_opy_, *args)
    try:
      bstack111l1ll1l_opy_ = threading.current_thread().bstackSessionDriver if bstack11ll1llll1_opy_(bstack111lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ௑")) else context.browser
      if is_driver_active(bstack111l1ll1l_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack111lll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢ௒")
        bstack1llllll11_opy_.bstack11l11l1l1l_opy_(args[0])
        if runner.driver_initialised == bstack111lll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣ௓"):
          feature_name = bstack1111llll1_opy_ = str(runner.feature.name)
          bstack1111llll1_opy_ = feature_name + bstack111lll_opy_ (u"ࠫࠥ࠳ࠠࠨ௔") + context.scenario.name
          bstack111l1ll1l_opy_.execute_script(bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ௕") + json.dumps(bstack1111llll1_opy_) + bstack111lll_opy_ (u"࠭ࡽࡾࠩ௖"))
    except Exception as e:
      logger.debug(bstack111lll_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡸࡪࡶ࠺ࠡࡽࢀࠫௗ").format(str(e)))
@measure(event_name=EVENTS.bstack1lll111l11_opy_, stage=STAGE.bstack111ll11l1_opy_, hook_type=bstack111lll_opy_ (u"ࠣࡣࡩࡸࡪࡸࡓࡵࡧࡳࠦ௘"), bstack11l11l11l_opy_=bstack11l1l1llll_opy_)
def bstack1lll1l111_opy_(runner, name, context, bstack1llll1l1ll_opy_, *args):
  bstack1llllll11_opy_.bstack1ll1ll1lll_opy_(args[0])
  try:
    bstack1ll11l1ll_opy_ = args[0].status.name
    bstack111l1ll1l_opy_ = threading.current_thread().bstackSessionDriver if bstack111lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ௙") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack111l1ll1l_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack111lll_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪ௚")
        feature_name = bstack1111llll1_opy_ = str(runner.feature.name)
        bstack1111llll1_opy_ = feature_name + bstack111lll_opy_ (u"ࠫࠥ࠳ࠠࠨ௛") + context.scenario.name
        bstack111l1ll1l_opy_.execute_script(bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ௜") + json.dumps(bstack1111llll1_opy_) + bstack111lll_opy_ (u"࠭ࡽࡾࠩ௝"))
    if str(bstack1ll11l1ll_opy_).lower() == bstack111lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ௞"):
      bstack11ll11l11l_opy_ = bstack111lll_opy_ (u"ࠨࠩ௟")
      bstack1l1llllll_opy_ = bstack111lll_opy_ (u"ࠩࠪ௠")
      bstack111111l11_opy_ = bstack111lll_opy_ (u"ࠪࠫ௡")
      try:
        import traceback
        bstack11ll11l11l_opy_ = runner.exception.__class__.__name__
        bstack11ll1l11_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1l1llllll_opy_ = bstack111lll_opy_ (u"ࠫࠥ࠭௢").join(bstack11ll1l11_opy_)
        bstack111111l11_opy_ = bstack11ll1l11_opy_[-1]
      except Exception as e:
        logger.debug(bstack11l111ll11_opy_.format(str(e)))
      bstack11ll11l11l_opy_ += bstack111111l11_opy_
      bstack111lllll1_opy_(context, json.dumps(str(args[0].name) + bstack111lll_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦ௣") + str(bstack1l1llllll_opy_)),
                          bstack111lll_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ௤"))
      if runner.driver_initialised == bstack111lll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧ௥"):
        bstack1l1ll1ll11_opy_(getattr(context, bstack111lll_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭௦"), None), bstack111lll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ௧"), bstack11ll11l11l_opy_)
        bstack111l1ll1l_opy_.execute_script(bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨ௨") + json.dumps(str(args[0].name) + bstack111lll_opy_ (u"ࠦࠥ࠳ࠠࡇࡣ࡬ࡰࡪࡪࠡ࡝ࡰࠥ௩") + str(bstack1l1llllll_opy_)) + bstack111lll_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥࡩࡷࡸ࡯ࡳࠤࢀࢁࠬ௪"))
      if runner.driver_initialised == bstack111lll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦ௫"):
        bstack1lll11l1ll_opy_(bstack111l1ll1l_opy_, bstack111lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ௬"), bstack111lll_opy_ (u"ࠣࡕࡦࡩࡳࡧࡲࡪࡱࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧ௭") + str(bstack11ll11l11l_opy_))
    else:
      bstack111lllll1_opy_(context, bstack111lll_opy_ (u"ࠤࡓࡥࡸࡹࡥࡥࠣࠥ௮"), bstack111lll_opy_ (u"ࠥ࡭ࡳ࡬࡯ࠣ௯"))
      if runner.driver_initialised == bstack111lll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤ௰"):
        bstack1l1ll1ll11_opy_(getattr(context, bstack111lll_opy_ (u"ࠬࡶࡡࡨࡧࠪ௱"), None), bstack111lll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ௲"))
      bstack111l1ll1l_opy_.execute_script(bstack111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ௳") + json.dumps(str(args[0].name) + bstack111lll_opy_ (u"ࠣࠢ࠰ࠤࡕࡧࡳࡴࡧࡧࠥࠧ௴")) + bstack111lll_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧࢃࡽࠨ௵"))
      if runner.driver_initialised == bstack111lll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣ௶"):
        bstack1lll11l1ll_opy_(bstack111l1ll1l_opy_, bstack111lll_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ௷"))
  except Exception as e:
    logger.debug(bstack111lll_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡶࡸࡪࡶ࠺ࠡࡽࢀࠫ௸").format(str(e)))
  bstack11lll11ll_opy_(runner, name, context, args[0], bstack1llll1l1ll_opy_, *args)
@measure(event_name=EVENTS.bstack1l1l11lll1_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l11l11l_opy_=bstack11l1l1llll_opy_)
def bstack11ll1l1ll1_opy_(runner, name, context, bstack1llll1l1ll_opy_, *args):
  bstack1llllll11_opy_.end_test(args[0])
  try:
    bstack1l1lll1ll_opy_ = args[0].status.name
    bstack111l1ll1l_opy_ = bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ௹"), context.browser)
    bstack111111l1_opy_.bstack111l1l111_opy_(bstack111l1ll1l_opy_)
    if str(bstack1l1lll1ll_opy_).lower() == bstack111lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ௺"):
      bstack11ll11l11l_opy_ = bstack111lll_opy_ (u"ࠨࠩ௻")
      bstack1l1llllll_opy_ = bstack111lll_opy_ (u"ࠩࠪ௼")
      bstack111111l11_opy_ = bstack111lll_opy_ (u"ࠪࠫ௽")
      try:
        import traceback
        bstack11ll11l11l_opy_ = runner.exception.__class__.__name__
        bstack11ll1l11_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1l1llllll_opy_ = bstack111lll_opy_ (u"ࠫࠥ࠭௾").join(bstack11ll1l11_opy_)
        bstack111111l11_opy_ = bstack11ll1l11_opy_[-1]
      except Exception as e:
        logger.debug(bstack11l111ll11_opy_.format(str(e)))
      bstack11ll11l11l_opy_ += bstack111111l11_opy_
      bstack111lllll1_opy_(context, json.dumps(str(args[0].name) + bstack111lll_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦ௿") + str(bstack1l1llllll_opy_)),
                          bstack111lll_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧఀ"))
      if runner.driver_initialised == bstack111lll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤఁ") or runner.driver_initialised == bstack111lll_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨం"):
        bstack1l1ll1ll11_opy_(getattr(context, bstack111lll_opy_ (u"ࠩࡳࡥ࡬࡫ࠧః"), None), bstack111lll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥఄ"), bstack11ll11l11l_opy_)
        bstack111l1ll1l_opy_.execute_script(bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩఅ") + json.dumps(str(args[0].name) + bstack111lll_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦఆ") + str(bstack1l1llllll_opy_)) + bstack111lll_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥࢁࢂ࠭ఇ"))
      if runner.driver_initialised == bstack111lll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤఈ") or runner.driver_initialised == bstack111lll_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨఉ"):
        bstack1lll11l1ll_opy_(bstack111l1ll1l_opy_, bstack111lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩఊ"), bstack111lll_opy_ (u"ࠥࡗࡨ࡫࡮ࡢࡴ࡬ࡳࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢఋ") + str(bstack11ll11l11l_opy_))
    else:
      bstack111lllll1_opy_(context, bstack111lll_opy_ (u"ࠦࡕࡧࡳࡴࡧࡧࠥࠧఌ"), bstack111lll_opy_ (u"ࠧ࡯࡮ࡧࡱࠥ఍"))
      if runner.driver_initialised == bstack111lll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣఎ") or runner.driver_initialised == bstack111lll_opy_ (u"ࠧࡪࡰࡶࡸࡪࡶࠧఏ"):
        bstack1l1ll1ll11_opy_(getattr(context, bstack111lll_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭ఐ"), None), bstack111lll_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ఑"))
      bstack111l1ll1l_opy_.execute_script(bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨఒ") + json.dumps(str(args[0].name) + bstack111lll_opy_ (u"ࠦࠥ࠳ࠠࡑࡣࡶࡷࡪࡪࠡࠣఓ")) + bstack111lll_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫఔ"))
      if runner.driver_initialised == bstack111lll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣక") or runner.driver_initialised == bstack111lll_opy_ (u"ࠧࡪࡰࡶࡸࡪࡶࠧఖ"):
        bstack1lll11l1ll_opy_(bstack111l1ll1l_opy_, bstack111lll_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣగ"))
  except Exception as e:
    logger.debug(bstack111lll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫఘ").format(str(e)))
  bstack11lll11ll_opy_(runner, name, context, context.scenario, bstack1llll1l1ll_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack1l11l1ll_opy_(runner, name, context, bstack1llll1l1ll_opy_, *args):
    target = context.scenario if hasattr(context, bstack111lll_opy_ (u"ࠪࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬఙ")) else context.feature
    bstack11lll11ll_opy_(runner, name, context, target, bstack1llll1l1ll_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack11l111l1ll_opy_(runner, name, context, bstack1llll1l1ll_opy_, *args):
    try:
      bstack111l1ll1l_opy_ = bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪచ"), context.browser)
      bstack11llll1ll_opy_ = bstack111lll_opy_ (u"ࠬ࠭ఛ")
      if context.failed is True:
        bstack1llll1lll1_opy_ = []
        bstack1lllll11l1_opy_ = []
        bstack1ll1lllll_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack1llll1lll1_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack11ll1l11_opy_ = traceback.format_tb(exc_tb)
            bstack1l1l11l111_opy_ = bstack111lll_opy_ (u"࠭ࠠࠨజ").join(bstack11ll1l11_opy_)
            bstack1lllll11l1_opy_.append(bstack1l1l11l111_opy_)
            bstack1ll1lllll_opy_.append(bstack11ll1l11_opy_[-1])
        except Exception as e:
          logger.debug(bstack11l111ll11_opy_.format(str(e)))
        bstack11ll11l11l_opy_ = bstack111lll_opy_ (u"ࠧࠨఝ")
        for i in range(len(bstack1llll1lll1_opy_)):
          bstack11ll11l11l_opy_ += bstack1llll1lll1_opy_[i] + bstack1ll1lllll_opy_[i] + bstack111lll_opy_ (u"ࠨ࡞ࡱࠫఞ")
        bstack11llll1ll_opy_ = bstack111lll_opy_ (u"ࠩࠣࠫట").join(bstack1lllll11l1_opy_)
        if runner.driver_initialised in [bstack111lll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦఠ"), bstack111lll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣడ")]:
          bstack111lllll1_opy_(context, bstack11llll1ll_opy_, bstack111lll_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦఢ"))
          bstack1l1ll1ll11_opy_(getattr(context, bstack111lll_opy_ (u"࠭ࡰࡢࡩࡨࠫణ"), None), bstack111lll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢత"), bstack11ll11l11l_opy_)
          bstack111l1ll1l_opy_.execute_script(bstack111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭థ") + json.dumps(bstack11llll1ll_opy_) + bstack111lll_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࡽࡾࠩద"))
          bstack1lll11l1ll_opy_(bstack111l1ll1l_opy_, bstack111lll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥధ"), bstack111lll_opy_ (u"ࠦࡘࡵ࡭ࡦࠢࡶࡧࡪࡴࡡࡳ࡫ࡲࡷࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦ࡜࡯ࠤన") + str(bstack11ll11l11l_opy_))
          bstack11l1l1l1ll_opy_ = bstack1111ll1ll_opy_(bstack11llll1ll_opy_, runner.feature.name, logger)
          if (bstack11l1l1l1ll_opy_ != None):
            bstack1ll111111_opy_.append(bstack11l1l1l1ll_opy_)
      else:
        if runner.driver_initialised in [bstack111lll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨ఩"), bstack111lll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥప")]:
          bstack111lllll1_opy_(context, bstack111lll_opy_ (u"ࠢࡇࡧࡤࡸࡺࡸࡥ࠻ࠢࠥఫ") + str(runner.feature.name) + bstack111lll_opy_ (u"ࠣࠢࡳࡥࡸࡹࡥࡥࠣࠥబ"), bstack111lll_opy_ (u"ࠤ࡬ࡲ࡫ࡵࠢభ"))
          bstack1l1ll1ll11_opy_(getattr(context, bstack111lll_opy_ (u"ࠪࡴࡦ࡭ࡥࠨమ"), None), bstack111lll_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦయ"))
          bstack111l1ll1l_opy_.execute_script(bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪర") + json.dumps(bstack111lll_opy_ (u"ࠨࡆࡦࡣࡷࡹࡷ࡫࠺ࠡࠤఱ") + str(runner.feature.name) + bstack111lll_opy_ (u"ࠢࠡࡲࡤࡷࡸ࡫ࡤࠢࠤల")) + bstack111lll_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦࢂࢃࠧళ"))
          bstack1lll11l1ll_opy_(bstack111l1ll1l_opy_, bstack111lll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩఴ"))
          bstack11l1l1l1ll_opy_ = bstack1111ll1ll_opy_(bstack11llll1ll_opy_, runner.feature.name, logger)
          if (bstack11l1l1l1ll_opy_ != None):
            bstack1ll111111_opy_.append(bstack11l1l1l1ll_opy_)
    except Exception as e:
      logger.debug(bstack111lll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡯࡮ࠡࡣࡩࡸࡪࡸࠠࡧࡧࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬవ").format(str(e)))
    bstack11lll11ll_opy_(runner, name, context, context.feature, bstack1llll1l1ll_opy_, *args)
@measure(event_name=EVENTS.bstack1lll111l11_opy_, stage=STAGE.bstack111ll11l1_opy_, hook_type=bstack111lll_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࡄࡰࡱࠨశ"), bstack11l11l11l_opy_=bstack11l1l1llll_opy_)
def bstack1l11lll111_opy_(runner, name, context, bstack1llll1l1ll_opy_, *args):
    bstack11lll11ll_opy_(runner, name, context, runner, bstack1llll1l1ll_opy_, *args)
def bstack1l1ll111l_opy_(self, name, context, *args):
  if bstack111lll111_opy_:
    platform_index = int(threading.current_thread()._name) % bstack111ll1ll1_opy_
    bstack1ll1lll1_opy_ = CONFIG[bstack111lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨష")][platform_index]
    os.environ[bstack111lll_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧస")] = json.dumps(bstack1ll1lll1_opy_)
  global bstack1llll1l1ll_opy_
  if not hasattr(self, bstack111lll_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡨࡨࠬహ")):
    self.driver_initialised = None
  bstack1lll1ll1l1_opy_ = {
      bstack111lll_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠬ఺"): bstack1l11l11111_opy_,
      bstack111lll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠪ఻"): bstack1111l1l11_opy_,
      bstack111lll_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡸࡦ࡭఼ࠧ"): bstack1lll1l1ll1_opy_,
      bstack111lll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ఽ"): bstack1lll11l11_opy_,
      bstack111lll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠪా"): bstack11l1llll_opy_,
      bstack111lll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡴࡦࡲࠪి"): bstack1lll1l111_opy_,
      bstack111lll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨీ"): bstack11ll1l1ll1_opy_,
      bstack111lll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡵࡣࡪࠫు"): bstack1l11l1ll_opy_,
      bstack111lll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠩూ"): bstack11l111l1ll_opy_,
      bstack111lll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ࠭ృ"): bstack1l11lll111_opy_
  }
  handler = bstack1lll1ll1l1_opy_.get(name, bstack1llll1l1ll_opy_)
  handler(self, name, context, bstack1llll1l1ll_opy_, *args)
  if name in [bstack111lll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫౄ"), bstack111lll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭౅"), bstack111lll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠩె")]:
    try:
      bstack111l1ll1l_opy_ = threading.current_thread().bstackSessionDriver if bstack11ll1llll1_opy_(bstack111lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ే")) else context.browser
      bstack11111l11l_opy_ = (
        (name == bstack111lll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠫై") and self.driver_initialised == bstack111lll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨ౉")) or
        (name == bstack111lll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪొ") and self.driver_initialised == bstack111lll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠧో")) or
        (name == bstack111lll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ౌ") and self.driver_initialised in [bstack111lll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯్ࠣ"), bstack111lll_opy_ (u"ࠢࡪࡰࡶࡸࡪࡶࠢ౎")]) or
        (name == bstack111lll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡴࡶࡨࡴࠬ౏") and self.driver_initialised == bstack111lll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢ౐"))
      )
      if bstack11111l11l_opy_:
        self.driver_initialised = None
        bstack111l1ll1l_opy_.quit()
    except Exception:
      pass
def bstack1l1ll1ll1l_opy_(config, startdir):
  return bstack111lll_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀ࠶ࡽࠣ౑").format(bstack111lll_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥ౒"))
notset = Notset()
def bstack1l1lllll_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1ll1l11ll1_opy_
  if str(name).lower() == bstack111lll_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࠬ౓"):
    return bstack111lll_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧ౔")
  else:
    return bstack1ll1l11ll1_opy_(self, name, default, skip)
def bstack1l1l1ll11_opy_(item, when):
  global bstack1l1111l1_opy_
  try:
    bstack1l1111l1_opy_(item, when)
  except Exception as e:
    pass
def bstack11ll1lllll_opy_():
  return
def bstack1lll1ll11_opy_(type, name, status, reason, bstack1llllll111_opy_, bstack1ll111lll_opy_):
  bstack1lll1lll_opy_ = {
    bstack111lll_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴౕࠧ"): type,
    bstack111lll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶౖࠫ"): {}
  }
  if type == bstack111lll_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫ౗"):
    bstack1lll1lll_opy_[bstack111lll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ౘ")][bstack111lll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪౙ")] = bstack1llllll111_opy_
    bstack1lll1lll_opy_[bstack111lll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨౚ")][bstack111lll_opy_ (u"࠭ࡤࡢࡶࡤࠫ౛")] = json.dumps(str(bstack1ll111lll_opy_))
  if type == bstack111lll_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ౜"):
    bstack1lll1lll_opy_[bstack111lll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫౝ")][bstack111lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ౞")] = name
  if type == bstack111lll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭౟"):
    bstack1lll1lll_opy_[bstack111lll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧౠ")][bstack111lll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬౡ")] = status
    if status == bstack111lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ౢ"):
      bstack1lll1lll_opy_[bstack111lll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪౣ")][bstack111lll_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨ౤")] = json.dumps(str(reason))
  bstack11l1ll1lll_opy_ = bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧ౥").format(json.dumps(bstack1lll1lll_opy_))
  return bstack11l1ll1lll_opy_
def bstack11lll1ll11_opy_(driver_command, response):
    if driver_command == bstack111lll_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧ౦"):
        bstack11111ll1l_opy_.bstack1l111lll_opy_({
            bstack111lll_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪ౧"): response[bstack111lll_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫ౨")],
            bstack111lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭౩"): bstack11111ll1l_opy_.current_test_uuid()
        })
def bstack1lll111111_opy_(item, call, rep):
  global bstack1ll11l1111_opy_
  global bstack1ll11111l_opy_
  global bstack1l11ll111l_opy_
  name = bstack111lll_opy_ (u"ࠧࠨ౪")
  try:
    if rep.when == bstack111lll_opy_ (u"ࠨࡥࡤࡰࡱ࠭౫"):
      bstack1l11ll11l1_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1l11ll111l_opy_:
          name = str(rep.nodeid)
          bstack11ll1111l1_opy_ = bstack1lll1ll11_opy_(bstack111lll_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ౬"), name, bstack111lll_opy_ (u"ࠪࠫ౭"), bstack111lll_opy_ (u"ࠫࠬ౮"), bstack111lll_opy_ (u"ࠬ࠭౯"), bstack111lll_opy_ (u"࠭ࠧ౰"))
          threading.current_thread().bstack11l1lllll1_opy_ = name
          for driver in bstack1ll11111l_opy_:
            if bstack1l11ll11l1_opy_ == driver.session_id:
              driver.execute_script(bstack11ll1111l1_opy_)
      except Exception as e:
        logger.debug(bstack111lll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧ౱").format(str(e)))
      try:
        bstack1l1lll11l_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack111lll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ౲"):
          status = bstack111lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ౳") if rep.outcome.lower() == bstack111lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ౴") else bstack111lll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ౵")
          reason = bstack111lll_opy_ (u"ࠬ࠭౶")
          if status == bstack111lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭౷"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack111lll_opy_ (u"ࠧࡪࡰࡩࡳࠬ౸") if status == bstack111lll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ౹") else bstack111lll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ౺")
          data = name + bstack111lll_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬ౻") if status == bstack111lll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ౼") else name + bstack111lll_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩࠧࠠࠨ౽") + reason
          bstack1l1111l111_opy_ = bstack1lll1ll11_opy_(bstack111lll_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨ౾"), bstack111lll_opy_ (u"ࠧࠨ౿"), bstack111lll_opy_ (u"ࠨࠩಀ"), bstack111lll_opy_ (u"ࠩࠪಁ"), level, data)
          for driver in bstack1ll11111l_opy_:
            if bstack1l11ll11l1_opy_ == driver.session_id:
              driver.execute_script(bstack1l1111l111_opy_)
      except Exception as e:
        logger.debug(bstack111lll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡤࡱࡱࡸࡪࡾࡴࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧಂ").format(str(e)))
  except Exception as e:
    logger.debug(bstack111lll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡶࡤࡸࡪࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁࡽࠨಃ").format(str(e)))
  bstack1ll11l1111_opy_(item, call, rep)
def bstack1l1111l11l_opy_(driver, bstack11l1lll1l_opy_, test=None):
  global bstack11l1l11ll1_opy_
  if test != None:
    bstack1lllllll11_opy_ = getattr(test, bstack111lll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ಄"), None)
    bstack111111ll_opy_ = getattr(test, bstack111lll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫಅ"), None)
    PercySDK.screenshot(driver, bstack11l1lll1l_opy_, bstack1lllllll11_opy_=bstack1lllllll11_opy_, bstack111111ll_opy_=bstack111111ll_opy_, bstack1lll1l1lll_opy_=bstack11l1l11ll1_opy_)
  else:
    PercySDK.screenshot(driver, bstack11l1lll1l_opy_)
@measure(event_name=EVENTS.bstack1ll111l11l_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l11l11l_opy_=bstack11l1l1llll_opy_)
def bstack1l1llll11_opy_(driver):
  if bstack1l1ll1ll1_opy_.bstack1l11l1ll11_opy_() is True or bstack1l1ll1ll1_opy_.capturing() is True:
    return
  bstack1l1ll1ll1_opy_.bstack1l1l1111l_opy_()
  while not bstack1l1ll1ll1_opy_.bstack1l11l1ll11_opy_():
    bstack11l1lllll_opy_ = bstack1l1ll1ll1_opy_.bstack11ll111lll_opy_()
    bstack1l1111l11l_opy_(driver, bstack11l1lllll_opy_)
  bstack1l1ll1ll1_opy_.bstack11lll1l1_opy_()
def bstack1l1l1l11l1_opy_(sequence, driver_command, response = None, bstack1lll11ll1l_opy_ = None, args = None):
    try:
      if sequence != bstack111lll_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧಆ"):
        return
      if percy.bstack11l1ll11l1_opy_() == bstack111lll_opy_ (u"ࠣࡨࡤࡰࡸ࡫ࠢಇ"):
        return
      bstack11l1lllll_opy_ = bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠩࡳࡩࡷࡩࡹࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬಈ"), None)
      for command in bstack1llll111l_opy_:
        if command == driver_command:
          for driver in bstack1ll11111l_opy_:
            bstack1l1llll11_opy_(driver)
      bstack1l11llll_opy_ = percy.bstack1ll111ll11_opy_()
      if driver_command in bstack1l11111lll_opy_[bstack1l11llll_opy_]:
        bstack1l1ll1ll1_opy_.bstack1l1lllll1_opy_(bstack11l1lllll_opy_, driver_command)
    except Exception as e:
      pass
def bstack1ll1ll1l1l_opy_(framework_name):
  if bstack1ll1l11ll_opy_.get_property(bstack111lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡱࡴࡪ࡟ࡤࡣ࡯ࡰࡪࡪࠧಉ")):
      return
  bstack1ll1l11ll_opy_.bstack1lll1llll1_opy_(bstack111lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨಊ"), True)
  global bstack1lllll11l_opy_
  global bstack1lll1111_opy_
  global bstack11l11ll11_opy_
  bstack1lllll11l_opy_ = framework_name
  logger.info(bstack1llllllll_opy_.format(bstack1lllll11l_opy_.split(bstack111lll_opy_ (u"ࠬ࠳ࠧಋ"))[0]))
  bstack1l11l1l111_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack111lll111_opy_:
      Service.start = bstack1l111lll11_opy_
      Service.stop = bstack11l1l1ll1_opy_
      webdriver.Remote.get = bstack1ll111lll1_opy_
      WebDriver.quit = bstack1ll1ll11l_opy_
      webdriver.Remote.__init__ = bstack11ll111111_opy_
    if not bstack111lll111_opy_:
        webdriver.Remote.__init__ = bstack1ll11l1ll1_opy_
    WebDriver.getAccessibilityResults = getAccessibilityResults
    WebDriver.get_accessibility_results = getAccessibilityResults
    WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
    WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
    WebDriver.performScan = perform_scan
    WebDriver.perform_scan = perform_scan
    WebDriver.execute = bstack1ll1ll11l1_opy_
    bstack1lll1111_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack111lll111_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1111111ll_opy_
  except Exception as e:
    pass
  bstack1ll1lll11l_opy_()
  if not bstack1lll1111_opy_:
    bstack1l1l1l1ll_opy_(bstack111lll_opy_ (u"ࠨࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠡࡰࡲࡸࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠣಌ"), bstack1l1l1111_opy_)
  if bstack1l1111ll1_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      if hasattr(RemoteConnection, bstack111lll_opy_ (u"ࠧࡠࡩࡨࡸࡤࡶࡲࡰࡺࡼࡣࡺࡸ࡬ࠨ಍")) and callable(getattr(RemoteConnection, bstack111lll_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩಎ"))):
        RemoteConnection._get_proxy_url = bstack1lll11ll_opy_
      else:
        from selenium.webdriver.remote.client_config import ClientConfig
        ClientConfig.get_proxy_url = bstack1lll11ll_opy_
    except Exception as e:
      logger.error(bstack1l1l111ll1_opy_.format(str(e)))
  if bstack1ll11l11ll_opy_():
    bstack11l1l11ll_opy_(CONFIG, logger)
  if (bstack111lll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨಏ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if percy.bstack11l1ll11l1_opy_() == bstack111lll_opy_ (u"ࠥࡸࡷࡻࡥࠣಐ"):
          bstack1llll1l1l_opy_(bstack1l1l1l11l1_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1l1l1ll1l_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1lllll1ll_opy_
      except Exception as e:
        logger.warn(bstack11lll1l1l_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1ll1ll111l_opy_
      except Exception as e:
        logger.debug(bstack11l1lll111_opy_ + str(e))
    except Exception as e:
      bstack1l1l1l1ll_opy_(e, bstack11lll1l1l_opy_)
    Output.start_test = bstack1l11l11ll_opy_
    Output.end_test = bstack1l111ll1ll_opy_
    TestStatus.__init__ = bstack11lll1l11_opy_
    QueueItem.__init__ = bstack1l111l1ll_opy_
    pabot._create_items = bstack1l11l111_opy_
    try:
      from pabot import __version__ as bstack1lllll1l1_opy_
      if version.parse(bstack1lllll1l1_opy_) >= version.parse(bstack111lll_opy_ (u"ࠫ࠹࠴࠲࠯࠲ࠪ಑")):
        pabot._run = bstack11l111lll1_opy_
      elif version.parse(bstack1lllll1l1_opy_) >= version.parse(bstack111lll_opy_ (u"ࠬ࠸࠮࠲࠷࠱࠴ࠬಒ")):
        pabot._run = bstack11111lll1_opy_
      elif version.parse(bstack1lllll1l1_opy_) >= version.parse(bstack111lll_opy_ (u"࠭࠲࠯࠳࠶࠲࠵࠭ಓ")):
        pabot._run = bstack111ll1l11_opy_
      else:
        pabot._run = bstack1l11ll1111_opy_
    except Exception as e:
      pabot._run = bstack1l11ll1111_opy_
    pabot._create_command_for_execution = bstack1l11lll1l1_opy_
    pabot._report_results = bstack1l1l1ll1l1_opy_
  if bstack111lll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧಔ") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l1l1l1ll_opy_(e, bstack11lll11111_opy_)
    Runner.run_hook = bstack1l1ll111l_opy_
    Step.run = bstack1l11111l1l_opy_
  if bstack111lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨಕ") in str(framework_name).lower():
    if not bstack111lll111_opy_:
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack1l1ll1ll1l_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack11ll1lllll_opy_
      Config.getoption = bstack1l1lllll_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1lll111111_opy_
    except Exception as e:
      pass
def bstack11111ll11_opy_():
  global CONFIG
  if bstack111lll_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩಖ") in CONFIG and int(CONFIG[bstack111lll_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪಗ")]) > 1:
    logger.warn(bstack1l1l111lll_opy_)
def bstack1ll1l111l_opy_(arg, bstack1lll1l11_opy_, bstack1l111llll1_opy_=None):
  global CONFIG
  global bstack11ll1111ll_opy_
  global bstack11lll111l_opy_
  global bstack111lll111_opy_
  global bstack1ll1l11ll_opy_
  bstack1l11lll11l_opy_ = bstack111lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫಘ")
  if bstack1lll1l11_opy_ and isinstance(bstack1lll1l11_opy_, str):
    bstack1lll1l11_opy_ = eval(bstack1lll1l11_opy_)
  CONFIG = bstack1lll1l11_opy_[bstack111lll_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬಙ")]
  bstack11ll1111ll_opy_ = bstack1lll1l11_opy_[bstack111lll_opy_ (u"࠭ࡈࡖࡄࡢ࡙ࡗࡒࠧಚ")]
  bstack11lll111l_opy_ = bstack1lll1l11_opy_[bstack111lll_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩಛ")]
  bstack111lll111_opy_ = bstack1lll1l11_opy_[bstack111lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫಜ")]
  bstack1ll1l11ll_opy_.bstack1lll1llll1_opy_(bstack111lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪಝ"), bstack111lll111_opy_)
  os.environ[bstack111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬಞ")] = bstack1l11lll11l_opy_
  os.environ[bstack111lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠪಟ")] = json.dumps(CONFIG)
  os.environ[bstack111lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡍ࡛ࡂࡠࡗࡕࡐࠬಠ")] = bstack11ll1111ll_opy_
  os.environ[bstack111lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧಡ")] = str(bstack11lll111l_opy_)
  os.environ[bstack111lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡍࡗࡊࡍࡓ࠭ಢ")] = str(True)
  if bstack1l111ll11_opy_(arg, [bstack111lll_opy_ (u"ࠨ࠯ࡱࠫಣ"), bstack111lll_opy_ (u"ࠩ࠰࠱ࡳࡻ࡭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪತ")]) != -1:
    os.environ[bstack111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡅࡗࡇࡌࡍࡇࡏࠫಥ")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack11ll111ll_opy_)
    return
  bstack1ll1ll1l1_opy_()
  global bstack11l1ll1l1l_opy_
  global bstack11l1l11ll1_opy_
  global bstack1l1lll11l1_opy_
  global bstack1111l11l_opy_
  global bstack11ll11l1_opy_
  global bstack11l11ll11_opy_
  global bstack1lllll111_opy_
  arg.append(bstack111lll_opy_ (u"ࠦ࠲࡝ࠢದ"))
  arg.append(bstack111lll_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩ࠿ࡓ࡯ࡥࡷ࡯ࡩࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡩ࡮ࡲࡲࡶࡹ࡫ࡤ࠻ࡲࡼࡸࡪࡹࡴ࠯ࡒࡼࡸࡪࡹࡴࡘࡣࡵࡲ࡮ࡴࡧࠣಧ"))
  arg.append(bstack111lll_opy_ (u"ࠨ࠭ࡘࠤನ"))
  arg.append(bstack111lll_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫࠺ࡕࡪࡨࠤ࡭ࡵ࡯࡬࡫ࡰࡴࡱࠨ಩"))
  global bstack1l1l11111l_opy_
  global bstack1l1ll11111_opy_
  global bstack1l111l111_opy_
  global bstack1ll1l11lll_opy_
  global bstack11ll1llll_opy_
  global bstack11l1ll11_opy_
  global bstack1l111l1l1_opy_
  global bstack11l11l1lll_opy_
  global bstack1llll11ll_opy_
  global bstack1l1111l1ll_opy_
  global bstack1ll1l11ll1_opy_
  global bstack1l1111l1_opy_
  global bstack1ll11l1111_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l1l11111l_opy_ = webdriver.Remote.__init__
    bstack1l1ll11111_opy_ = WebDriver.quit
    bstack11l11l1lll_opy_ = WebDriver.close
    bstack1llll11ll_opy_ = WebDriver.get
    bstack1l111l111_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1l11lllll1_opy_(CONFIG) and bstack1l1l1l1l1l_opy_():
    if bstack11l1ll1ll_opy_() < version.parse(bstack11l1l1111_opy_):
      logger.error(bstack1l11ll1ll_opy_.format(bstack11l1ll1ll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack111lll_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩಪ")) and callable(getattr(RemoteConnection, bstack111lll_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪಫ"))):
          bstack1l1111l1ll_opy_ = RemoteConnection._get_proxy_url
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          bstack1l1111l1ll_opy_ = ClientConfig.get_proxy_url
      except Exception as e:
        logger.error(bstack1l1l111ll1_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1ll1l11ll1_opy_ = Config.getoption
    from _pytest import runner
    bstack1l1111l1_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack11l1l1ll1l_opy_)
  try:
    from pytest_bdd import reporting
    bstack1ll11l1111_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack111lll_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡲࠤࡷࡻ࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࡶࠫಬ"))
  bstack1l1lll11l1_opy_ = CONFIG.get(bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨಭ"), {}).get(bstack111lll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧಮ"))
  bstack1lllll111_opy_ = True
  if cli.is_enabled(CONFIG):
    if cli.bstack11l11l111l_opy_():
      bstack1l1ll11ll_opy_.invoke(bstack11ll1l111_opy_.CONNECT, bstack11ll1111l_opy_())
    platform_index = int(os.environ.get(bstack111lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ಯ"), bstack111lll_opy_ (u"ࠧ࠱ࠩರ")))
  else:
    bstack1ll1ll1l1l_opy_(bstack111lllll_opy_)
  os.environ[bstack111lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩಱ")] = CONFIG[bstack111lll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫಲ")]
  os.environ[bstack111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭ಳ")] = CONFIG[bstack111lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ಴")]
  os.environ[bstack111lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨವ")] = bstack111lll111_opy_.__str__()
  from _pytest.config import main as bstack1ll111111l_opy_
  bstack1ll1l1l1ll_opy_ = []
  try:
    bstack1l1l1l1111_opy_ = bstack1ll111111l_opy_(arg)
    if cli.is_enabled(CONFIG):
      cli.bstack11l1llll1l_opy_()
    if bstack111lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶࠪಶ") in multiprocessing.current_process().__dict__.keys():
      for bstack1lll1ll1l_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1ll1l1l1ll_opy_.append(bstack1lll1ll1l_opy_)
    try:
      bstack11llll111l_opy_ = (bstack1ll1l1l1ll_opy_, int(bstack1l1l1l1111_opy_))
      bstack1l111llll1_opy_.append(bstack11llll111l_opy_)
    except:
      bstack1l111llll1_opy_.append((bstack1ll1l1l1ll_opy_, bstack1l1l1l1111_opy_))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack1ll1l1l1ll_opy_.append({bstack111lll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬಷ"): bstack111lll_opy_ (u"ࠨࡒࡵࡳࡨ࡫ࡳࡴࠢࠪಸ") + os.environ.get(bstack111lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩಹ")), bstack111lll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ಺"): traceback.format_exc(), bstack111lll_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ಻"): int(os.environ.get(bstack111lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜಼ࠬ")))})
    bstack1l111llll1_opy_.append((bstack1ll1l1l1ll_opy_, 1))
def mod_behave_main(args, retries):
  try:
    from behave.configuration import Configuration
    from behave.__main__ import run_behave
    from browserstack_sdk.bstack_behave_runner import BehaveRunner
    config = Configuration(args)
    config.update_userdata({bstack111lll_opy_ (u"ࠨࡲࡦࡶࡵ࡭ࡪࡹࠢಽ"): str(retries)})
    return run_behave(config, runner_class=BehaveRunner)
  except Exception as e:
    bstack1l1l11l11l_opy_ = e.__class__.__name__
    print(bstack111lll_opy_ (u"ࠢࠦࡵ࠽ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡶࡺࡴ࡮ࡪࡰࡪࠤࡧ࡫ࡨࡢࡸࡨࠤࡹ࡫ࡳࡵࠢࠨࡷࠧಾ") % (bstack1l1l11l11l_opy_, e))
    return 1
def bstack1l1l1ll11l_opy_(arg):
  global bstack1llll11ll1_opy_
  bstack1ll1ll1l1l_opy_(bstack111l1ll1_opy_)
  os.environ[bstack111lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩಿ")] = str(bstack11lll111l_opy_)
  retries = bstack1lllll1l11_opy_.bstack1l1ll1l1l_opy_(CONFIG)
  status_code = 0
  if bstack1lllll1l11_opy_.bstack1l1111111_opy_(CONFIG):
    status_code = mod_behave_main(arg, retries)
  else:
    from behave.__main__ import main as bstack111l1l11l_opy_
    status_code = bstack111l1l11l_opy_(arg)
  if status_code != 0:
    bstack1llll11ll1_opy_ = status_code
def bstack1l11ll1l_opy_():
  logger.info(bstack1ll11lll1_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack111lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨೀ"), help=bstack111lll_opy_ (u"ࠪࡋࡪࡴࡥࡳࡣࡷࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡨࡵ࡮ࡧ࡫ࡪࠫು"))
  parser.add_argument(bstack111lll_opy_ (u"ࠫ࠲ࡻࠧೂ"), bstack111lll_opy_ (u"ࠬ࠳࠭ࡶࡵࡨࡶࡳࡧ࡭ࡦࠩೃ"), help=bstack111lll_opy_ (u"࡙࠭ࡰࡷࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬೄ"))
  parser.add_argument(bstack111lll_opy_ (u"ࠧ࠮࡭ࠪ೅"), bstack111lll_opy_ (u"ࠨ࠯࠰࡯ࡪࡿࠧೆ"), help=bstack111lll_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡡࡤࡥࡨࡷࡸࠦ࡫ࡦࡻࠪೇ"))
  parser.add_argument(bstack111lll_opy_ (u"ࠪ࠱࡫࠭ೈ"), bstack111lll_opy_ (u"ࠫ࠲࠳ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ೉"), help=bstack111lll_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫೊ"))
  bstack1l11lll1ll_opy_ = parser.parse_args()
  try:
    bstack1ll11ll1ll_opy_ = bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥ࡯ࡧࡵ࡭ࡨ࠴ࡹ࡮࡮࠱ࡷࡦࡳࡰ࡭ࡧࠪೋ")
    if bstack1l11lll1ll_opy_.framework and bstack1l11lll1ll_opy_.framework not in (bstack111lll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧೌ"), bstack111lll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴್ࠩ")):
      bstack1ll11ll1ll_opy_ = bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠲ࡾࡳ࡬࠯ࡵࡤࡱࡵࡲࡥࠨ೎")
    bstack1l11l1l1l1_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll11ll1ll_opy_)
    bstack1l1l1111ll_opy_ = open(bstack1l11l1l1l1_opy_, bstack111lll_opy_ (u"ࠪࡶࠬ೏"))
    bstack1l1ll1l11l_opy_ = bstack1l1l1111ll_opy_.read()
    bstack1l1l1111ll_opy_.close()
    if bstack1l11lll1ll_opy_.username:
      bstack1l1ll1l11l_opy_ = bstack1l1ll1l11l_opy_.replace(bstack111lll_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫ೐"), bstack1l11lll1ll_opy_.username)
    if bstack1l11lll1ll_opy_.key:
      bstack1l1ll1l11l_opy_ = bstack1l1ll1l11l_opy_.replace(bstack111lll_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧ೑"), bstack1l11lll1ll_opy_.key)
    if bstack1l11lll1ll_opy_.framework:
      bstack1l1ll1l11l_opy_ = bstack1l1ll1l11l_opy_.replace(bstack111lll_opy_ (u"࡙࠭ࡐࡗࡕࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ೒"), bstack1l11lll1ll_opy_.framework)
    file_name = bstack111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪ೓")
    file_path = os.path.abspath(file_name)
    bstack1lllll11ll_opy_ = open(file_path, bstack111lll_opy_ (u"ࠨࡹࠪ೔"))
    bstack1lllll11ll_opy_.write(bstack1l1ll1l11l_opy_)
    bstack1lllll11ll_opy_.close()
    logger.info(bstack1l11l1ll1l_opy_)
    try:
      os.environ[bstack111lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫೕ")] = bstack1l11lll1ll_opy_.framework if bstack1l11lll1ll_opy_.framework != None else bstack111lll_opy_ (u"ࠥࠦೖ")
      config = yaml.safe_load(bstack1l1ll1l11l_opy_)
      config[bstack111lll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ೗")] = bstack111lll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲ࡹࡥࡵࡷࡳࠫ೘")
      bstack1llll11111_opy_(bstack1111l1111_opy_, config)
    except Exception as e:
      logger.debug(bstack1ll1llll11_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1111l11ll_opy_.format(str(e)))
def bstack1llll11111_opy_(bstack1ll1111l1l_opy_, config, bstack1llll1ll1_opy_={}):
  global bstack111lll111_opy_
  global bstack11ll11ll1_opy_
  global bstack1ll1l11ll_opy_
  if not config:
    return
  bstack1111lll1l_opy_ = bstack11111l1ll_opy_ if not bstack111lll111_opy_ else (
    bstack1l1l11ll_opy_ if bstack111lll_opy_ (u"࠭ࡡࡱࡲࠪ೙") in config else (
        bstack11l1lll11_opy_ if config.get(bstack111lll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ೚")) else bstack111l11l1_opy_
    )
)
  bstack1ll1lllll1_opy_ = False
  bstack11l1llllll_opy_ = False
  if bstack111lll111_opy_ is True:
      if bstack111lll_opy_ (u"ࠨࡣࡳࡴࠬ೛") in config:
          bstack1ll1lllll1_opy_ = True
      else:
          bstack11l1llllll_opy_ = True
  bstack11ll1ll1ll_opy_ = bstack1lll1l1l_opy_.bstack1l1ll1lll1_opy_(config, bstack11ll11ll1_opy_)
  bstack11l1l11l1_opy_ = bstack1l11ll1lll_opy_()
  data = {
    bstack111lll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ೜"): config[bstack111lll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬೝ")],
    bstack111lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧೞ"): config[bstack111lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ೟")],
    bstack111lll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪೠ"): bstack1ll1111l1l_opy_,
    bstack111lll_opy_ (u"ࠧࡥࡧࡷࡩࡨࡺࡥࡥࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫೡ"): os.environ.get(bstack111lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪೢ"), bstack11ll11ll1_opy_),
    bstack111lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫೣ"): bstack1l1l1l1l_opy_,
    bstack111lll_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰࠬ೤"): bstack1lllll111l_opy_(),
    bstack111lll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧ೥"): {
      bstack111lll_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ೦"): str(config[bstack111lll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭೧")]) if bstack111lll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ೨") in config else bstack111lll_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤ೩"),
      bstack111lll_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨ࡚ࡪࡸࡳࡪࡱࡱࠫ೪"): sys.version,
      bstack111lll_opy_ (u"ࠪࡶࡪ࡬ࡥࡳࡴࡨࡶࠬ೫"): bstack111lll1l_opy_(os.environ.get(bstack111lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭೬"), bstack11ll11ll1_opy_)),
      bstack111lll_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠧ೭"): bstack111lll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭೮"),
      bstack111lll_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨ೯"): bstack1111lll1l_opy_,
      bstack111lll_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭೰"): bstack11ll1ll1ll_opy_,
      bstack111lll_opy_ (u"ࠩࡷࡩࡸࡺࡨࡶࡤࡢࡹࡺ࡯ࡤࠨೱ"): os.environ[bstack111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨೲ")],
      bstack111lll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧೳ"): os.environ.get(bstack111lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ೴"), bstack11ll11ll1_opy_),
      bstack111lll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩ೵"): bstack11l111ll1l_opy_(os.environ.get(bstack111lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩ೶"), bstack11ll11ll1_opy_)),
      bstack111lll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ೷"): bstack11l1l11l1_opy_.get(bstack111lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ೸")),
      bstack111lll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩ೹"): bstack11l1l11l1_opy_.get(bstack111lll_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬ೺")),
      bstack111lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ೻"): config[bstack111lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ೼")] if config[bstack111lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ೽")] else bstack111lll_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤ೾"),
      bstack111lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ೿"): str(config[bstack111lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬഀ")]) if bstack111lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ഁ") in config else bstack111lll_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨം"),
      bstack111lll_opy_ (u"࠭࡯ࡴࠩഃ"): sys.platform,
      bstack111lll_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩഄ"): socket.gethostname(),
      bstack111lll_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪഅ"): bstack1ll1l11ll_opy_.get_property(bstack111lll_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫആ"))
    }
  }
  if not bstack1ll1l11ll_opy_.get_property(bstack111lll_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪഇ")) is None:
    data[bstack111lll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧഈ")][bstack111lll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࡍࡦࡶࡤࡨࡦࡺࡡࠨഉ")] = {
      bstack111lll_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ഊ"): bstack111lll_opy_ (u"ࠧࡶࡵࡨࡶࡤࡱࡩ࡭࡮ࡨࡨࠬഋ"),
      bstack111lll_opy_ (u"ࠨࡵ࡬࡫ࡳࡧ࡬ࠨഌ"): bstack1ll1l11ll_opy_.get_property(bstack111lll_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩ഍")),
      bstack111lll_opy_ (u"ࠪࡷ࡮࡭࡮ࡢ࡮ࡑࡹࡲࡨࡥࡳࠩഎ"): bstack1ll1l11ll_opy_.get_property(bstack111lll_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡓࡵࠧഏ"))
    }
  if bstack1ll1111l1l_opy_ == bstack1l1ll1l1ll_opy_:
    data[bstack111lll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨഐ")][bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡈࡵ࡮ࡧ࡫ࡪࠫ഑")] = bstack1lll1ll111_opy_(config)
    data[bstack111lll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪഒ")][bstack111lll_opy_ (u"ࠨ࡫ࡶࡔࡪࡸࡣࡺࡃࡸࡸࡴࡋ࡮ࡢࡤ࡯ࡩࡩ࠭ഓ")] = percy.bstack11lll1lll1_opy_
    data[bstack111lll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬഔ")][bstack111lll_opy_ (u"ࠪࡴࡪࡸࡣࡺࡄࡸ࡭ࡱࡪࡉࡥࠩക")] = percy.percy_build_id
  if not bstack1lllll1l11_opy_.bstack1l111ll1_opy_(CONFIG):
    data[bstack111lll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧഖ")][bstack111lll_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠩഗ")] = bstack1lllll1l11_opy_.bstack1l111ll1_opy_(CONFIG)
  update(data[bstack111lll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩഘ")], bstack1llll1ll1_opy_)
  try:
    response = bstack1l1ll1l111_opy_(bstack111lll_opy_ (u"ࠧࡑࡑࡖࡘࠬങ"), bstack11l1l111_opy_(bstack11lll11ll1_opy_), data, {
      bstack111lll_opy_ (u"ࠨࡣࡸࡸ࡭࠭ച"): (config[bstack111lll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫഛ")], config[bstack111lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ജ")])
    })
    if response:
      logger.debug(bstack11l11ll1l1_opy_.format(bstack1ll1111l1l_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1l1lllll1l_opy_.format(str(e)))
def bstack111lll1l_opy_(framework):
  return bstack111lll_opy_ (u"ࠦࢀࢃ࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴ࢁࡽࠣഝ").format(str(framework), __version__) if framework else bstack111lll_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࡿࢂࠨഞ").format(
    __version__)
def bstack1ll1ll1l1_opy_():
  global CONFIG
  global bstack11llll1lll_opy_
  if bool(CONFIG):
    return
  try:
    bstack11l11lllll_opy_()
    logger.debug(bstack11l1l1ll_opy_.format(str(CONFIG)))
    bstack11llll1lll_opy_ = bstack1111ll111_opy_.bstack1llll1111l_opy_(CONFIG, bstack11llll1lll_opy_)
    bstack1l11l1l111_opy_()
  except Exception as e:
    logger.error(bstack111lll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࠥട") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1l11llllll_opy_
  atexit.register(bstack1ll1lll111_opy_)
  signal.signal(signal.SIGINT, bstack1lll1l11l1_opy_)
  signal.signal(signal.SIGTERM, bstack1lll1l11l1_opy_)
def bstack1l11llllll_opy_(exctype, value, traceback):
  global bstack1ll11111l_opy_
  try:
    for driver in bstack1ll11111l_opy_:
      bstack1lll11l1ll_opy_(driver, bstack111lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧഠ"), bstack111lll_opy_ (u"ࠣࡕࡨࡷࡸ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦഡ") + str(value))
  except Exception:
    pass
  logger.info(bstack11l11llll_opy_)
  bstack1ll1llllll_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1ll1llllll_opy_(message=bstack111lll_opy_ (u"ࠩࠪഢ"), bstack1l1111111l_opy_ = False):
  global CONFIG
  bstack1lll111ll_opy_ = bstack111lll_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠬണ") if bstack1l1111111l_opy_ else bstack111lll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪത")
  try:
    if message:
      bstack1llll1ll1_opy_ = {
        bstack1lll111ll_opy_ : str(message)
      }
      bstack1llll11111_opy_(bstack1l1ll1l1ll_opy_, CONFIG, bstack1llll1ll1_opy_)
    else:
      bstack1llll11111_opy_(bstack1l1ll1l1ll_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack11l1111l_opy_.format(str(e)))
def bstack1l1llll11l_opy_(bstack11l11ll1ll_opy_, size):
  bstack1l1111llll_opy_ = []
  while len(bstack11l11ll1ll_opy_) > size:
    bstack1ll11lllll_opy_ = bstack11l11ll1ll_opy_[:size]
    bstack1l1111llll_opy_.append(bstack1ll11lllll_opy_)
    bstack11l11ll1ll_opy_ = bstack11l11ll1ll_opy_[size:]
  bstack1l1111llll_opy_.append(bstack11l11ll1ll_opy_)
  return bstack1l1111llll_opy_
def bstack1lll1111l1_opy_(args):
  if bstack111lll_opy_ (u"ࠬ࠳࡭ࠨഥ") in args and bstack111lll_opy_ (u"࠭ࡰࡥࡤࠪദ") in args:
    return True
  return False
@measure(event_name=EVENTS.bstack1l1ll1llll_opy_, stage=STAGE.bstack1ll11l111l_opy_)
def run_on_browserstack(bstack11ll1ll1l_opy_=None, bstack1l111llll1_opy_=None, bstack1lll1ll11l_opy_=False):
  global CONFIG
  global bstack11ll1111ll_opy_
  global bstack11lll111l_opy_
  global bstack11ll11ll1_opy_
  global bstack1ll1l11ll_opy_
  bstack1l11lll11l_opy_ = bstack111lll_opy_ (u"ࠧࠨധ")
  bstack1ll11l11l1_opy_(bstack1l1llll1l_opy_, logger)
  if bstack11ll1ll1l_opy_ and isinstance(bstack11ll1ll1l_opy_, str):
    bstack11ll1ll1l_opy_ = eval(bstack11ll1ll1l_opy_)
  if bstack11ll1ll1l_opy_:
    CONFIG = bstack11ll1ll1l_opy_[bstack111lll_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨന")]
    bstack11ll1111ll_opy_ = bstack11ll1ll1l_opy_[bstack111lll_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪഩ")]
    bstack11lll111l_opy_ = bstack11ll1ll1l_opy_[bstack111lll_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬപ")]
    bstack1ll1l11ll_opy_.bstack1lll1llll1_opy_(bstack111lll_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ഫ"), bstack11lll111l_opy_)
    bstack1l11lll11l_opy_ = bstack111lll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬബ")
  bstack1ll1l11ll_opy_.bstack1lll1llll1_opy_(bstack111lll_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨഭ"), uuid4().__str__())
  logger.info(bstack111lll_opy_ (u"ࠧࡔࡆࡎࠤࡷࡻ࡮ࠡࡵࡷࡥࡷࡺࡥࡥࠢࡺ࡭ࡹ࡮ࠠࡪࡦ࠽ࠤࠬമ") + bstack1ll1l11ll_opy_.get_property(bstack111lll_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪയ")));
  logger.debug(bstack111lll_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࡁࠬര") + bstack1ll1l11ll_opy_.get_property(bstack111lll_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࠬറ")))
  if not bstack1lll1ll11l_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack11ll111ll_opy_)
      return
    if sys.argv[1] == bstack111lll_opy_ (u"ࠫ࠲࠳ࡶࡦࡴࡶ࡭ࡴࡴࠧല") or sys.argv[1] == bstack111lll_opy_ (u"ࠬ࠳ࡶࠨള"):
      logger.info(bstack111lll_opy_ (u"࠭ࡂࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡖࡹࡵࡪࡲࡲ࡙ࠥࡄࡌࠢࡹࡿࢂ࠭ഴ").format(__version__))
      return
    if sys.argv[1] == bstack111lll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭വ"):
      bstack1l11ll1l_opy_()
      return
  args = sys.argv
  bstack1ll1ll1l1_opy_()
  global bstack11l1ll1l1l_opy_
  global bstack111ll1ll1_opy_
  global bstack1lllll111_opy_
  global bstack1ll11ll11_opy_
  global bstack11l1l11ll1_opy_
  global bstack1l1lll11l1_opy_
  global bstack1111l11l_opy_
  global bstack1l111llll_opy_
  global bstack11ll11l1_opy_
  global bstack11l11ll11_opy_
  global bstack1ll1ll1ll1_opy_
  bstack111ll1ll1_opy_ = len(CONFIG.get(bstack111lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫശ"), []))
  if not bstack1l11lll11l_opy_:
    if args[1] == bstack111lll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩഷ") or args[1] == bstack111lll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫസ"):
      bstack1l11lll11l_opy_ = bstack111lll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫഹ")
      args = args[2:]
    elif args[1] == bstack111lll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫഺ"):
      bstack1l11lll11l_opy_ = bstack111lll_opy_ (u"࠭ࡲࡰࡤࡲࡸ഻ࠬ")
      args = args[2:]
    elif args[1] == bstack111lll_opy_ (u"ࠧࡱࡣࡥࡳࡹ഼࠭"):
      bstack1l11lll11l_opy_ = bstack111lll_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧഽ")
      args = args[2:]
    elif args[1] == bstack111lll_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪാ"):
      bstack1l11lll11l_opy_ = bstack111lll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫി")
      args = args[2:]
    elif args[1] == bstack111lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫീ"):
      bstack1l11lll11l_opy_ = bstack111lll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬു")
      args = args[2:]
    elif args[1] == bstack111lll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ൂ"):
      bstack1l11lll11l_opy_ = bstack111lll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧൃ")
      args = args[2:]
    else:
      if not bstack111lll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫൄ") in CONFIG or str(CONFIG[bstack111lll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ൅")]).lower() in [bstack111lll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪെ"), bstack111lll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬേ")]:
        bstack1l11lll11l_opy_ = bstack111lll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬൈ")
        args = args[1:]
      elif str(CONFIG[bstack111lll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ൉")]).lower() == bstack111lll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ൊ"):
        bstack1l11lll11l_opy_ = bstack111lll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧോ")
        args = args[1:]
      elif str(CONFIG[bstack111lll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬൌ")]).lower() == bstack111lll_opy_ (u"ࠪࡴࡦࡨ࡯ࡵ്ࠩ"):
        bstack1l11lll11l_opy_ = bstack111lll_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪൎ")
        args = args[1:]
      elif str(CONFIG[bstack111lll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ൏")]).lower() == bstack111lll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭൐"):
        bstack1l11lll11l_opy_ = bstack111lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ൑")
        args = args[1:]
      elif str(CONFIG[bstack111lll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ൒")]).lower() == bstack111lll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ൓"):
        bstack1l11lll11l_opy_ = bstack111lll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪൔ")
        args = args[1:]
      else:
        os.environ[bstack111lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ൕ")] = bstack1l11lll11l_opy_
        bstack11l11111_opy_(bstack11l1lll1l1_opy_)
  os.environ[bstack111lll_opy_ (u"ࠬࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉ࠭ൖ")] = bstack1l11lll11l_opy_
  bstack11ll11ll1_opy_ = bstack1l11lll11l_opy_
  if cli.is_enabled(CONFIG):
    try:
      bstack1l1lllll11_opy_ = bstack1ll1l1l111_opy_[bstack111lll_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙࠳ࡂࡅࡆࠪൗ")] if bstack1l11lll11l_opy_ == bstack111lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ൘") and bstack111ll111_opy_() else bstack1l11lll11l_opy_
      bstack1l1ll11ll_opy_.invoke(bstack11ll1l111_opy_.bstack111ll1lll_opy_, bstack1ll11l11_opy_(
        sdk_version=__version__,
        path_config=bstack1ll11ll1_opy_(),
        path_project=os.getcwd(),
        test_framework=bstack1l1lllll11_opy_,
        frameworks=[bstack1l1lllll11_opy_],
        framework_versions={
          bstack1l1lllll11_opy_: bstack11l111ll1l_opy_(bstack111lll_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧ൙") if bstack1l11lll11l_opy_ in [bstack111lll_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ൚"), bstack111lll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ൛"), bstack111lll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ൜")] else bstack1l11lll11l_opy_)
        },
        bs_config=CONFIG
      ))
      if cli.config.get(bstack111lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠢ൝"), None):
        CONFIG[bstack111lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣ൞")] = cli.config.get(bstack111lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤൟ"), None)
    except Exception as e:
      bstack1l1ll11ll_opy_.invoke(bstack11ll1l111_opy_.bstack1l111l1l11_opy_, e.__traceback__, 1)
    if bstack11lll111l_opy_:
      CONFIG[bstack111lll_opy_ (u"ࠣࡣࡳࡴࠧൠ")] = cli.config[bstack111lll_opy_ (u"ࠤࡤࡴࡵࠨൡ")]
      logger.info(bstack1ll1ll11_opy_.format(CONFIG[bstack111lll_opy_ (u"ࠪࡥࡵࡶࠧൢ")]))
  else:
    bstack1l1ll11ll_opy_.clear()
  global bstack1ll11ll1l_opy_
  global bstack1lll1lllll_opy_
  if bstack11ll1ll1l_opy_:
    try:
      bstack11ll1ll1_opy_ = datetime.datetime.now()
      os.environ[bstack111lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ൣ")] = bstack1l11lll11l_opy_
      bstack1llll11111_opy_(bstack1ll111l1ll_opy_, CONFIG)
      cli.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽ࡷࡩࡱ࡟ࡵࡧࡶࡸࡤࡧࡴࡵࡧࡰࡴࡹ࡫ࡤࠣ൤"), datetime.datetime.now() - bstack11ll1ll1_opy_)
    except Exception as e:
      logger.debug(bstack11ll11111l_opy_.format(str(e)))
  global bstack1l1l11111l_opy_
  global bstack1l1ll11111_opy_
  global bstack1l1l111ll_opy_
  global bstack1lll11lll1_opy_
  global bstack11lll111ll_opy_
  global bstack11ll1l111l_opy_
  global bstack1ll1l11lll_opy_
  global bstack11ll1llll_opy_
  global bstack11lll1l11l_opy_
  global bstack11l1ll11_opy_
  global bstack1l111l1l1_opy_
  global bstack11l11l1lll_opy_
  global bstack1llll1l1ll_opy_
  global bstack11l111ll_opy_
  global bstack1llll11ll_opy_
  global bstack1l1111l1ll_opy_
  global bstack1ll1l11ll1_opy_
  global bstack1l1111l1_opy_
  global bstack11ll111l1_opy_
  global bstack1ll11l1111_opy_
  global bstack1l111l111_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l1l11111l_opy_ = webdriver.Remote.__init__
    bstack1l1ll11111_opy_ = WebDriver.quit
    bstack11l11l1lll_opy_ = WebDriver.close
    bstack1llll11ll_opy_ = WebDriver.get
    bstack1l111l111_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1ll11ll1l_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack11l1llll1_opy_
    bstack1lll1lllll_opy_ = bstack11l1llll1_opy_()
  except Exception as e:
    pass
  try:
    global bstack11l1l11l1l_opy_
    from QWeb.keywords import browser
    bstack11l1l11l1l_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1l11lllll1_opy_(CONFIG) and bstack1l1l1l1l1l_opy_():
    if bstack11l1ll1ll_opy_() < version.parse(bstack11l1l1111_opy_):
      logger.error(bstack1l11ll1ll_opy_.format(bstack11l1ll1ll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack111lll_opy_ (u"࠭࡟ࡨࡧࡷࡣࡵࡸ࡯ࡹࡻࡢࡹࡷࡲࠧ൥")) and callable(getattr(RemoteConnection, bstack111lll_opy_ (u"ࠧࡠࡩࡨࡸࡤࡶࡲࡰࡺࡼࡣࡺࡸ࡬ࠨ൦"))):
          RemoteConnection._get_proxy_url = bstack1lll11ll_opy_
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          ClientConfig.get_proxy_url = bstack1lll11ll_opy_
      except Exception as e:
        logger.error(bstack1l1l111ll1_opy_.format(str(e)))
  if not CONFIG.get(bstack111lll_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪ൧"), False) and not bstack11ll1ll1l_opy_:
    logger.info(bstack11l1l1lll1_opy_)
  if not cli.is_enabled(CONFIG):
    if bstack111lll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭൨") in CONFIG and str(CONFIG[bstack111lll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ൩")]).lower() != bstack111lll_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪ൪"):
      bstack1l111ll1l1_opy_()
    elif bstack1l11lll11l_opy_ != bstack111lll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ൫") or (bstack1l11lll11l_opy_ == bstack111lll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭൬") and not bstack11ll1ll1l_opy_):
      bstack1ll111l1l1_opy_()
  if (bstack1l11lll11l_opy_ in [bstack111lll_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭൭"), bstack111lll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ൮"), bstack111lll_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ൯")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1l1l1ll1l_opy_
        bstack11ll1l111l_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack11lll1l1l_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack11lll111ll_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack11l1lll111_opy_ + str(e))
    except Exception as e:
      bstack1l1l1l1ll_opy_(e, bstack11lll1l1l_opy_)
    if bstack1l11lll11l_opy_ != bstack111lll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ൰"):
      bstack11ll1l11l_opy_()
    bstack1l1l111ll_opy_ = Output.start_test
    bstack1lll11lll1_opy_ = Output.end_test
    bstack1ll1l11lll_opy_ = TestStatus.__init__
    bstack11lll1l11l_opy_ = pabot._run
    bstack11l1ll11_opy_ = QueueItem.__init__
    bstack1l111l1l1_opy_ = pabot._create_command_for_execution
    bstack11ll111l1_opy_ = pabot._report_results
  if bstack1l11lll11l_opy_ == bstack111lll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ൱"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l1l1l1ll_opy_(e, bstack11lll11111_opy_)
    bstack1llll1l1ll_opy_ = Runner.run_hook
    bstack11l111ll_opy_ = Step.run
  if bstack1l11lll11l_opy_ == bstack111lll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ൲"):
    try:
      from _pytest.config import Config
      bstack1ll1l11ll1_opy_ = Config.getoption
      from _pytest import runner
      bstack1l1111l1_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack11l1l1ll1l_opy_)
    try:
      from pytest_bdd import reporting
      bstack1ll11l1111_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack111lll_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧ൳"))
  try:
    framework_name = bstack111lll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭൴") if bstack1l11lll11l_opy_ in [bstack111lll_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ൵"), bstack111lll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ൶"), bstack111lll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ൷")] else bstack1llll1l1_opy_(bstack1l11lll11l_opy_)
    bstack1ll1l11l1l_opy_ = {
      bstack111lll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࠬ൸"): bstack111lll_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧ൹") if bstack1l11lll11l_opy_ == bstack111lll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ൺ") and bstack111ll111_opy_() else framework_name,
      bstack111lll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫൻ"): bstack11l111ll1l_opy_(framework_name),
      bstack111lll_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ർ"): __version__,
      bstack111lll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦࠪൽ"): bstack1l11lll11l_opy_
    }
    if bstack1l11lll11l_opy_ in bstack111ll1l1l_opy_ + bstack1l1ll11l_opy_:
      if bstack1l11l11ll1_opy_.bstack1l111lll1l_opy_(CONFIG):
        if bstack111lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪൾ") in CONFIG:
          os.environ[bstack111lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬൿ")] = os.getenv(bstack111lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭඀"), json.dumps(CONFIG[bstack111lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ඁ")]))
          CONFIG[bstack111lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧං")].pop(bstack111lll_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ඃ"), None)
          CONFIG[bstack111lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ඄")].pop(bstack111lll_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨඅ"), None)
        bstack1ll1l11l1l_opy_[bstack111lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫආ")] = {
          bstack111lll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪඇ"): bstack111lll_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨඈ"),
          bstack111lll_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨඉ"): str(bstack11l1ll1ll_opy_())
        }
    if bstack1l11lll11l_opy_ not in [bstack111lll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩඊ")] and not cli.is_running():
      bstack11lll1ll_opy_, bstack1111l1ll1_opy_ = bstack11111ll1l_opy_.launch(CONFIG, bstack1ll1l11l1l_opy_)
      if bstack1111l1ll1_opy_.get(bstack111lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩඋ")) is not None and bstack1l11l11ll1_opy_.bstack11ll1ll11_opy_(CONFIG) is None:
        value = bstack1111l1ll1_opy_[bstack111lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪඌ")].get(bstack111lll_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬඍ"))
        if value is not None:
            CONFIG[bstack111lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬඎ")] = value
        else:
          logger.debug(bstack111lll_opy_ (u"ࠨࡎࡰࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡧࡥࡹࡧࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠦඏ"))
  except Exception as e:
    logger.debug(bstack11llll11_opy_.format(bstack111lll_opy_ (u"ࠧࡕࡧࡶࡸࡍࡻࡢࠨඐ"), str(e)))
  if bstack1l11lll11l_opy_ == bstack111lll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨඑ"):
    bstack1lllll111_opy_ = True
    if bstack11ll1ll1l_opy_ and bstack1lll1ll11l_opy_:
      bstack1l1lll11l1_opy_ = CONFIG.get(bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ඒ"), {}).get(bstack111lll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬඓ"))
      bstack1ll1ll1l1l_opy_(bstack111l11111_opy_)
    elif bstack11ll1ll1l_opy_:
      bstack1l1lll11l1_opy_ = CONFIG.get(bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨඔ"), {}).get(bstack111lll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧඕ"))
      global bstack1ll11111l_opy_
      try:
        if bstack1lll1111l1_opy_(bstack11ll1ll1l_opy_[bstack111lll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩඖ")]) and multiprocessing.current_process().name == bstack111lll_opy_ (u"ࠧ࠱ࠩ඗"):
          bstack11ll1ll1l_opy_[bstack111lll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ඘")].remove(bstack111lll_opy_ (u"ࠩ࠰ࡱࠬ඙"))
          bstack11ll1ll1l_opy_[bstack111lll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ක")].remove(bstack111lll_opy_ (u"ࠫࡵࡪࡢࠨඛ"))
          bstack11ll1ll1l_opy_[bstack111lll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨග")] = bstack11ll1ll1l_opy_[bstack111lll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩඝ")][0]
          with open(bstack11ll1ll1l_opy_[bstack111lll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪඞ")], bstack111lll_opy_ (u"ࠨࡴࠪඟ")) as f:
            bstack11l1l11111_opy_ = f.read()
          bstack1l11ll1l1l_opy_ = bstack111lll_opy_ (u"ࠤࠥࠦ࡫ࡸ࡯࡮ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡵࡧ࡯ࠥ࡯࡭ࡱࡱࡵࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥ࠼ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩ࠭ࢁࡽࠪ࠽ࠣࡪࡷࡵ࡭ࠡࡲࡧࡦࠥ࡯࡭ࡱࡱࡵࡸࠥࡖࡤࡣ࠽ࠣࡳ࡬ࡥࡤࡣࠢࡀࠤࡕࡪࡢ࠯ࡦࡲࡣࡧࡸࡥࡢ࡭࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡥࡧࡩࠤࡲࡵࡤࡠࡤࡵࡩࡦࡱࠨࡴࡧ࡯ࡪ࠱ࠦࡡࡳࡩ࠯ࠤࡹ࡫࡭ࡱࡱࡵࡥࡷࡿࠠ࠾ࠢ࠳࠭࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡹࡸࡹ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡤࡶ࡬ࠦ࠽ࠡࡵࡷࡶ࠭࡯࡮ࡵࠪࡤࡶ࡬࠯ࠫ࠲࠲ࠬࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡨࡼࡨ࡫ࡰࡵࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡧࡳࠡࡧ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡵࡧࡳࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡰࡩࡢࡨࡧ࠮ࡳࡦ࡮ࡩ࠰ࡦࡸࡧ࠭ࡶࡨࡱࡵࡵࡲࡢࡴࡼ࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡒࡧࡦ࠳ࡪ࡯ࡠࡤࠣࡁࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡕࡪࡢ࠯ࡦࡲࡣࡧࡸࡥࡢ࡭ࠣࡁࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡕࡪࡢࠩࠫ࠱ࡷࡪࡺ࡟ࡵࡴࡤࡧࡪ࠮ࠩ࡝ࡰࠥࠦࠧච").format(str(bstack11ll1ll1l_opy_))
          bstack11l11lll_opy_ = bstack1l11ll1l1l_opy_ + bstack11l1l11111_opy_
          bstack1l11l111l1_opy_ = bstack11ll1ll1l_opy_[bstack111lll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ඡ")] + bstack111lll_opy_ (u"ࠫࡤࡨࡳࡵࡣࡦ࡯ࡤࡺࡥ࡮ࡲ࠱ࡴࡾ࠭ජ")
          with open(bstack1l11l111l1_opy_, bstack111lll_opy_ (u"ࠬࡽࠧඣ")):
            pass
          with open(bstack1l11l111l1_opy_, bstack111lll_opy_ (u"ࠨࡷࠬࠤඤ")) as f:
            f.write(bstack11l11lll_opy_)
          import subprocess
          bstack111lll11_opy_ = subprocess.run([bstack111lll_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢඥ"), bstack1l11l111l1_opy_])
          if os.path.exists(bstack1l11l111l1_opy_):
            os.unlink(bstack1l11l111l1_opy_)
          os._exit(bstack111lll11_opy_.returncode)
        else:
          if bstack1lll1111l1_opy_(bstack11ll1ll1l_opy_[bstack111lll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫඦ")]):
            bstack11ll1ll1l_opy_[bstack111lll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬට")].remove(bstack111lll_opy_ (u"ࠪ࠱ࡲ࠭ඨ"))
            bstack11ll1ll1l_opy_[bstack111lll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧඩ")].remove(bstack111lll_opy_ (u"ࠬࡶࡤࡣࠩඪ"))
            bstack11ll1ll1l_opy_[bstack111lll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩණ")] = bstack11ll1ll1l_opy_[bstack111lll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪඬ")][0]
          bstack1ll1ll1l1l_opy_(bstack111l11111_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack11ll1ll1l_opy_[bstack111lll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫත")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack111lll_opy_ (u"ࠩࡢࡣࡳࡧ࡭ࡦࡡࡢࠫථ")] = bstack111lll_opy_ (u"ࠪࡣࡤࡳࡡࡪࡰࡢࡣࠬද")
          mod_globals[bstack111lll_opy_ (u"ࠫࡤࡥࡦࡪ࡮ࡨࡣࡤ࠭ධ")] = os.path.abspath(bstack11ll1ll1l_opy_[bstack111lll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨන")])
          exec(open(bstack11ll1ll1l_opy_[bstack111lll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ඲")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack111lll_opy_ (u"ࠧࡄࡣࡸ࡫࡭ࡺࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃࠧඳ").format(str(e)))
          for driver in bstack1ll11111l_opy_:
            bstack1l111llll1_opy_.append({
              bstack111lll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ප"): bstack11ll1ll1l_opy_[bstack111lll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬඵ")],
              bstack111lll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩබ"): str(e),
              bstack111lll_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪභ"): multiprocessing.current_process().name
            })
            bstack1lll11l1ll_opy_(driver, bstack111lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬම"), bstack111lll_opy_ (u"ࠨࡓࡦࡵࡶ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤඹ") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1ll11111l_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack11lll111l_opy_, CONFIG, logger)
      bstack1l1llll111_opy_()
      bstack11111ll11_opy_()
      percy.bstack11l1111l1_opy_()
      bstack1lll1l11_opy_ = {
        bstack111lll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪය"): args[0],
        bstack111lll_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨර"): CONFIG,
        bstack111lll_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪ඼"): bstack11ll1111ll_opy_,
        bstack111lll_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬල"): bstack11lll111l_opy_
      }
      if bstack111lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ඾") in CONFIG:
        bstack11lllll1l1_opy_ = bstack11111l11_opy_(args, logger, CONFIG, bstack111lll111_opy_, bstack111ll1ll1_opy_)
        bstack1l111llll_opy_ = bstack11lllll1l1_opy_.bstack1ll11ll111_opy_(run_on_browserstack, bstack1lll1l11_opy_, bstack1lll1111l1_opy_(args))
      else:
        if bstack1lll1111l1_opy_(args):
          bstack1lll1l11_opy_[bstack111lll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ඿")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1lll1l11_opy_,))
          test.start()
          test.join()
        else:
          bstack1ll1ll1l1l_opy_(bstack111l11111_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack111lll_opy_ (u"࠭࡟ࡠࡰࡤࡱࡪࡥ࡟ࠨව")] = bstack111lll_opy_ (u"ࠧࡠࡡࡰࡥ࡮ࡴ࡟ࡠࠩශ")
          mod_globals[bstack111lll_opy_ (u"ࠨࡡࡢࡪ࡮ࡲࡥࡠࡡࠪෂ")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1l11lll11l_opy_ == bstack111lll_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨස") or bstack1l11lll11l_opy_ == bstack111lll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩහ"):
    percy.init(bstack11lll111l_opy_, CONFIG, logger)
    percy.bstack11l1111l1_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1l1l1l1ll_opy_(e, bstack11lll1l1l_opy_)
    bstack1l1llll111_opy_()
    bstack1ll1ll1l1l_opy_(bstack1l111l1l_opy_)
    if bstack111lll111_opy_:
      bstack1l1l1lll11_opy_(bstack1l111l1l_opy_, args)
      if bstack111lll_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩළ") in args:
        i = args.index(bstack111lll_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪෆ"))
        args.pop(i)
        args.pop(i)
      if bstack111lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ෇") not in CONFIG:
        CONFIG[bstack111lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ෈")] = [{}]
        bstack111ll1ll1_opy_ = 1
      if bstack11l1ll1l1l_opy_ == 0:
        bstack11l1ll1l1l_opy_ = 1
      args.insert(0, str(bstack11l1ll1l1l_opy_))
      args.insert(0, str(bstack111lll_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭෉")))
    if bstack11111ll1l_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1lll1l111l_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1lllllllll_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack111lll_opy_ (u"ࠤࡕࡓࡇࡕࡔࡠࡑࡓࡘࡎࡕࡎࡔࠤ්"),
        ).parse_args(bstack1lll1l111l_opy_)
        bstack1l1l1l11_opy_ = args.index(bstack1lll1l111l_opy_[0]) if len(bstack1lll1l111l_opy_) > 0 else len(args)
        args.insert(bstack1l1l1l11_opy_, str(bstack111lll_opy_ (u"ࠪ࠱࠲ࡲࡩࡴࡶࡨࡲࡪࡸࠧ෋")))
        args.insert(bstack1l1l1l11_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack111lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡷࡵࡢࡰࡶࡢࡰ࡮ࡹࡴࡦࡰࡨࡶ࠳ࡶࡹࠨ෌"))))
        if bstack1lllll1l11_opy_.bstack1l1111111_opy_(CONFIG):
          args.insert(bstack1l1l1l11_opy_, str(bstack111lll_opy_ (u"ࠬ࠳࠭࡭࡫ࡶࡸࡪࡴࡥࡳࠩ෍")))
          args.insert(bstack1l1l1l11_opy_ + 1, str(bstack111lll_opy_ (u"࠭ࡒࡦࡶࡵࡽࡋࡧࡩ࡭ࡧࡧ࠾ࢀࢃࠧ෎").format(bstack1lllll1l11_opy_.bstack1l1ll1l1l_opy_(CONFIG))))
        if bstack1ll111ll1_opy_(os.environ.get(bstack111lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠬා"))) and str(os.environ.get(bstack111lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࡥࡔࡆࡕࡗࡗࠬැ"), bstack111lll_opy_ (u"ࠩࡱࡹࡱࡲࠧෑ"))) != bstack111lll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨි"):
          for bstack1l11l11lll_opy_ in bstack1lllllllll_opy_:
            args.remove(bstack1l11l11lll_opy_)
          bstack1ll1l1lll1_opy_ = os.environ.get(bstack111lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠨී")).split(bstack111lll_opy_ (u"ࠬ࠲ࠧු"))
          for bstack1l1l11l11_opy_ in bstack1ll1l1lll1_opy_:
            args.append(bstack1l1l11l11_opy_)
      except Exception as e:
        logger.error(bstack111lll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡦࡺࡴࡢࡥ࡫࡭ࡳ࡭ࠠ࡭࡫ࡶࡸࡪࡴࡥࡳࠢࡩࡳࡷࠦࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࠠࡆࡴࡵࡳࡷࠦ࠭ࠡࠤ෕").format(e))
    pabot.main(args)
  elif bstack1l11lll11l_opy_ == bstack111lll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨූ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1l1l1l1ll_opy_(e, bstack11lll1l1l_opy_)
    for a in args:
      if bstack111lll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡑࡎࡄࡘࡋࡕࡒࡎࡋࡑࡈࡊ࡞ࠧ෗") in a:
        bstack11l1l11ll1_opy_ = int(a.split(bstack111lll_opy_ (u"ࠩ࠽ࠫෘ"))[1])
      if bstack111lll_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡇࡉࡋࡒࡏࡄࡃࡏࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧෙ") in a:
        bstack1l1lll11l1_opy_ = str(a.split(bstack111lll_opy_ (u"ࠫ࠿࠭ේ"))[1])
      if bstack111lll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡒࡉࡂࡔࡊࡗࠬෛ") in a:
        bstack1111l11l_opy_ = str(a.split(bstack111lll_opy_ (u"࠭࠺ࠨො"))[1])
    bstack11l1111lll_opy_ = None
    if bstack111lll_opy_ (u"ࠧ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽ࠭ෝ") in args:
      i = args.index(bstack111lll_opy_ (u"ࠨ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠧෞ"))
      args.pop(i)
      bstack11l1111lll_opy_ = args.pop(i)
    if bstack11l1111lll_opy_ is not None:
      global bstack1l1l11llll_opy_
      bstack1l1l11llll_opy_ = bstack11l1111lll_opy_
    bstack1ll1ll1l1l_opy_(bstack1l111l1l_opy_)
    run_cli(args)
    if bstack111lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠭ෟ") in multiprocessing.current_process().__dict__.keys():
      for bstack1lll1ll1l_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1l111llll1_opy_.append(bstack1lll1ll1l_opy_)
  elif bstack1l11lll11l_opy_ == bstack111lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ෠"):
    bstack1lll11lll_opy_ = bstack1llll1l111_opy_(args, logger, CONFIG, bstack111lll111_opy_)
    bstack1lll11lll_opy_.bstack11llll1l_opy_()
    bstack1l1llll111_opy_()
    bstack1ll11ll11_opy_ = True
    bstack11l11ll11_opy_ = bstack1lll11lll_opy_.bstack1llllll1l1_opy_()
    bstack1lll11lll_opy_.bstack1lll1l11_opy_(bstack1l11ll111l_opy_)
    bstack1111ll1l1_opy_(bstack1l11lll11l_opy_, CONFIG, bstack1lll11lll_opy_.bstack11111111_opy_(logger))
    bstack1ll111ll1l_opy_ = bstack1lll11lll_opy_.bstack1ll11ll111_opy_(bstack1ll1l111l_opy_, {
      bstack111lll_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬ෡"): bstack11ll1111ll_opy_,
      bstack111lll_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ෢"): bstack11lll111l_opy_,
      bstack111lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ෣"): bstack111lll111_opy_
    })
    try:
      bstack1ll1l1l1ll_opy_, bstack1lll1111l_opy_ = map(list, zip(*bstack1ll111ll1l_opy_))
      bstack11ll11l1_opy_ = bstack1ll1l1l1ll_opy_[0]
      for status_code in bstack1lll1111l_opy_:
        if status_code != 0:
          bstack1ll1ll1ll1_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack111lll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡦࡼࡥࠡࡧࡵࡶࡴࡸࡳࠡࡣࡱࡨࠥࡹࡴࡢࡶࡸࡷࠥࡩ࡯ࡥࡧ࠱ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠ࠻ࠢࡾࢁࠧ෤").format(str(e)))
  elif bstack1l11lll11l_opy_ == bstack111lll_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ෥"):
    try:
      from behave.__main__ import main as bstack111l1l11l_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1l1l1l1ll_opy_(e, bstack11lll11111_opy_)
    bstack1l1llll111_opy_()
    bstack1ll11ll11_opy_ = True
    bstack11ll1ll1l1_opy_ = 1
    if bstack111lll_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ෦") in CONFIG:
      bstack11ll1ll1l1_opy_ = CONFIG[bstack111lll_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ෧")]
    if bstack111lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ෨") in CONFIG:
      bstack1lllll1lll_opy_ = int(bstack11ll1ll1l1_opy_) * int(len(CONFIG[bstack111lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ෩")]))
    else:
      bstack1lllll1lll_opy_ = int(bstack11ll1ll1l1_opy_)
    config = Configuration(args)
    bstack1ll1l1l11_opy_ = config.paths
    if len(bstack1ll1l1l11_opy_) == 0:
      import glob
      pattern = bstack111lll_opy_ (u"࠭ࠪࠫ࠱࠭࠲࡫࡫ࡡࡵࡷࡵࡩࠬ෪")
      bstack1l1l11l1l_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1l1l11l1l_opy_)
      config = Configuration(args)
      bstack1ll1l1l11_opy_ = config.paths
    bstack11l11l1l_opy_ = [os.path.normpath(item) for item in bstack1ll1l1l11_opy_]
    bstack1lll1l1l1_opy_ = [os.path.normpath(item) for item in args]
    bstack1lll111ll1_opy_ = [item for item in bstack1lll1l1l1_opy_ if item not in bstack11l11l1l_opy_]
    import platform as pf
    if pf.system().lower() == bstack111lll_opy_ (u"ࠧࡸ࡫ࡱࡨࡴࡽࡳࠨ෫"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack11l11l1l_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l111l1111_opy_)))
                    for bstack1l111l1111_opy_ in bstack11l11l1l_opy_]
    bstack1l1lll1l1_opy_ = []
    for spec in bstack11l11l1l_opy_:
      bstack11l1ll1111_opy_ = []
      bstack11l1ll1111_opy_ += bstack1lll111ll1_opy_
      bstack11l1ll1111_opy_.append(spec)
      bstack1l1lll1l1_opy_.append(bstack11l1ll1111_opy_)
    execution_items = []
    for bstack11l1ll1111_opy_ in bstack1l1lll1l1_opy_:
      if bstack111lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ෬") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack111lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ෭")]):
          item = {}
          item[bstack111lll_opy_ (u"ࠪࡥࡷ࡭ࠧ෮")] = bstack111lll_opy_ (u"ࠫࠥ࠭෯").join(bstack11l1ll1111_opy_)
          item[bstack111lll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ෰")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack111lll_opy_ (u"࠭ࡡࡳࡩࠪ෱")] = bstack111lll_opy_ (u"ࠧࠡࠩෲ").join(bstack11l1ll1111_opy_)
        item[bstack111lll_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧෳ")] = 0
        execution_items.append(item)
    bstack1l11l1l1_opy_ = bstack1l1llll11l_opy_(execution_items, bstack1lllll1lll_opy_)
    for execution_item in bstack1l11l1l1_opy_:
      bstack1l111ll1l_opy_ = []
      for item in execution_item:
        bstack1l111ll1l_opy_.append(bstack1l11llll1l_opy_(name=str(item[bstack111lll_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ෴")]),
                                             target=bstack1l1l1ll11l_opy_,
                                             args=(item[bstack111lll_opy_ (u"ࠪࡥࡷ࡭ࠧ෵")],)))
      for t in bstack1l111ll1l_opy_:
        t.start()
      for t in bstack1l111ll1l_opy_:
        t.join()
  else:
    bstack11l11111_opy_(bstack11l1lll1l1_opy_)
  if not bstack11ll1ll1l_opy_:
    bstack1ll11lll11_opy_()
    if(bstack1l11lll11l_opy_ in [bstack111lll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ෶"), bstack111lll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ෷")]):
      bstack1llllll1ll_opy_()
  bstack1111ll111_opy_.bstack1l111l111l_opy_()
def browserstack_initialize(bstack11l11ll1l_opy_=None):
  logger.info(bstack111lll_opy_ (u"࠭ࡒࡶࡰࡱ࡭ࡳ࡭ࠠࡔࡆࡎࠤࡼ࡯ࡴࡩࠢࡤࡶ࡬ࡹ࠺ࠡࠩ෸") + str(bstack11l11ll1l_opy_))
  run_on_browserstack(bstack11l11ll1l_opy_, None, True)
@measure(event_name=EVENTS.bstack1lll11111_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l11l11l_opy_=bstack11l1l1llll_opy_)
def bstack1ll11lll11_opy_():
  global CONFIG
  global bstack11ll11ll1_opy_
  global bstack1ll1ll1ll1_opy_
  global bstack1llll11ll1_opy_
  global bstack1ll1l11ll_opy_
  bstack1lllllll1l_opy_.bstack1111l111_opy_()
  if cli.is_running():
    bstack1l1ll11ll_opy_.invoke(bstack11ll1l111_opy_.bstack11l1l1l11_opy_)
  if bstack11ll11ll1_opy_ == bstack111lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ෹"):
    if not cli.is_enabled(CONFIG):
      bstack11111ll1l_opy_.stop()
  else:
    bstack11111ll1l_opy_.stop()
  if not cli.is_enabled(CONFIG):
    bstack11l1ll111_opy_.bstack1111l1ll_opy_()
  if bstack111lll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ෺") in CONFIG and str(CONFIG[bstack111lll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭෻")]).lower() != bstack111lll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩ෼"):
    hashed_id, bstack1l111lll1_opy_ = bstack11lll1l1l1_opy_()
  else:
    hashed_id, bstack1l111lll1_opy_ = get_build_link()
  bstack1l11ll11l_opy_(hashed_id)
  logger.info(bstack111lll_opy_ (u"ࠫࡘࡊࡋࠡࡴࡸࡲࠥ࡫࡮ࡥࡧࡧࠤ࡫ࡵࡲࠡ࡫ࡧ࠾ࠬ෽") + bstack1ll1l11ll_opy_.get_property(bstack111lll_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪࠧ෾"), bstack111lll_opy_ (u"࠭ࠧ෿")) + bstack111lll_opy_ (u"ࠧ࠭ࠢࡷࡩࡸࡺࡨࡶࡤࠣ࡭ࡩࡀࠠࠨ฀") + os.getenv(bstack111lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ก"), bstack111lll_opy_ (u"ࠩࠪข")))
  if hashed_id is not None and bstack1l11llll11_opy_() != -1:
    sessions = bstack1l1l11111_opy_(hashed_id)
    bstack11llllll1_opy_(sessions, bstack1l111lll1_opy_)
  if bstack11ll11ll1_opy_ == bstack111lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪฃ") and bstack1ll1ll1ll1_opy_ != 0:
    sys.exit(bstack1ll1ll1ll1_opy_)
  if bstack11ll11ll1_opy_ == bstack111lll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫค") and bstack1llll11ll1_opy_ != 0:
    sys.exit(bstack1llll11ll1_opy_)
def bstack1l11ll11l_opy_(new_id):
    global bstack1l1l1l1l_opy_
    bstack1l1l1l1l_opy_ = new_id
def bstack1llll1l1_opy_(bstack1ll111l111_opy_):
  if bstack1ll111l111_opy_:
    return bstack1ll111l111_opy_.capitalize()
  else:
    return bstack111lll_opy_ (u"ࠬ࠭ฅ")
@measure(event_name=EVENTS.bstack1l111l11ll_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l11l11l_opy_=bstack11l1l1llll_opy_)
def bstack1ll111llll_opy_(bstack1l1111ll1l_opy_):
  if bstack111lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫฆ") in bstack1l1111ll1l_opy_ and bstack1l1111ll1l_opy_[bstack111lll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬง")] != bstack111lll_opy_ (u"ࠨࠩจ"):
    return bstack1l1111ll1l_opy_[bstack111lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧฉ")]
  else:
    bstack11l11l11l_opy_ = bstack111lll_opy_ (u"ࠥࠦช")
    if bstack111lll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫซ") in bstack1l1111ll1l_opy_ and bstack1l1111ll1l_opy_[bstack111lll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬฌ")] != None:
      bstack11l11l11l_opy_ += bstack1l1111ll1l_opy_[bstack111lll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ญ")] + bstack111lll_opy_ (u"ࠢ࠭ࠢࠥฎ")
      if bstack1l1111ll1l_opy_[bstack111lll_opy_ (u"ࠨࡱࡶࠫฏ")] == bstack111lll_opy_ (u"ࠤ࡬ࡳࡸࠨฐ"):
        bstack11l11l11l_opy_ += bstack111lll_opy_ (u"ࠥ࡭ࡔ࡙ࠠࠣฑ")
      bstack11l11l11l_opy_ += (bstack1l1111ll1l_opy_[bstack111lll_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨฒ")] or bstack111lll_opy_ (u"ࠬ࠭ณ"))
      return bstack11l11l11l_opy_
    else:
      bstack11l11l11l_opy_ += bstack1llll1l1_opy_(bstack1l1111ll1l_opy_[bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧด")]) + bstack111lll_opy_ (u"ࠢࠡࠤต") + (
              bstack1l1111ll1l_opy_[bstack111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪถ")] or bstack111lll_opy_ (u"ࠩࠪท")) + bstack111lll_opy_ (u"ࠥ࠰ࠥࠨธ")
      if bstack1l1111ll1l_opy_[bstack111lll_opy_ (u"ࠫࡴࡹࠧน")] == bstack111lll_opy_ (u"ࠧ࡝ࡩ࡯ࡦࡲࡻࡸࠨบ"):
        bstack11l11l11l_opy_ += bstack111lll_opy_ (u"ࠨࡗࡪࡰࠣࠦป")
      bstack11l11l11l_opy_ += bstack1l1111ll1l_opy_[bstack111lll_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫผ")] or bstack111lll_opy_ (u"ࠨࠩฝ")
      return bstack11l11l11l_opy_
@measure(event_name=EVENTS.bstack11lllll111_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l11l11l_opy_=bstack11l1l1llll_opy_)
def bstack11l1llll11_opy_(bstack1l11ll1l1_opy_):
  if bstack1l11ll1l1_opy_ == bstack111lll_opy_ (u"ࠤࡧࡳࡳ࡫ࠢพ"):
    return bstack111lll_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿࡭ࡲࡦࡧࡱ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧ࡭ࡲࡦࡧࡱࠦࡃࡉ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ฟ")
  elif bstack1l11ll1l1_opy_ == bstack111lll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦภ"):
    return bstack111lll_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡳࡧࡧ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡸࡥࡥࠤࡁࡊࡦ࡯࡬ࡦࡦ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨม")
  elif bstack1l11ll1l1_opy_ == bstack111lll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨย"):
    return bstack111lll_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡪࡶࡪ࡫࡮࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡪࡶࡪ࡫࡮ࠣࡀࡓࡥࡸࡹࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧร")
  elif bstack1l11ll1l1_opy_ == bstack111lll_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢฤ"):
    return bstack111lll_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡷ࡫ࡤ࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡵࡩࡩࠨ࠾ࡆࡴࡵࡳࡷࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫล")
  elif bstack1l11ll1l1_opy_ == bstack111lll_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࠦฦ"):
    return bstack111lll_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࠣࡦࡧࡤ࠷࠷࠼࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࠥࡨࡩࡦ࠹࠲࠷ࠤࡁࡘ࡮ࡳࡥࡰࡷࡷࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩว")
  elif bstack1l11ll1l1_opy_ == bstack111lll_opy_ (u"ࠧࡸࡵ࡯ࡰ࡬ࡲ࡬ࠨศ"):
    return bstack111lll_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡤ࡯ࡥࡨࡱ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡤ࡯ࡥࡨࡱࠢ࠿ࡔࡸࡲࡳ࡯࡮ࡨ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧษ")
  else:
    return bstack111lll_opy_ (u"ࠧ࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡦࡱࡧࡣ࡬࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡦࡱࡧࡣ࡬ࠤࡁࠫส") + bstack1llll1l1_opy_(
      bstack1l11ll1l1_opy_) + bstack111lll_opy_ (u"ࠨ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧห")
def bstack1l11111l_opy_(session):
  return bstack111lll_opy_ (u"ࠩ࠿ࡸࡷࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡲࡰࡹࠥࡂࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠦࡳࡦࡵࡶ࡭ࡴࡴ࠭࡯ࡣࡰࡩࠧࡄ࠼ࡢࠢ࡫ࡶࡪ࡬࠽ࠣࡽࢀࠦࠥࡺࡡࡳࡩࡨࡸࡂࠨ࡟ࡣ࡮ࡤࡲࡰࠨ࠾ࡼࡿ࠿࠳ࡦࡄ࠼࠰ࡶࡧࡂࢀࢃࡻࡾ࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀ࠴ࡺࡲ࠿ࠩฬ").format(
    session[bstack111lll_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥࡢࡹࡷࡲࠧอ")], bstack1ll111llll_opy_(session), bstack11l1llll11_opy_(session[bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡷࡹࡧࡴࡶࡵࠪฮ")]),
    bstack11l1llll11_opy_(session[bstack111lll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬฯ")]),
    bstack1llll1l1_opy_(session[bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧะ")] or session[bstack111lll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧั")] or bstack111lll_opy_ (u"ࠨࠩา")) + bstack111lll_opy_ (u"ࠤࠣࠦำ") + (session[bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬิ")] or bstack111lll_opy_ (u"ࠫࠬี")),
    session[bstack111lll_opy_ (u"ࠬࡵࡳࠨึ")] + bstack111lll_opy_ (u"ࠨࠠࠣื") + session[bstack111lll_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱุࠫ")], session[bstack111lll_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰูࠪ")] or bstack111lll_opy_ (u"ฺࠩࠪ"),
    session[bstack111lll_opy_ (u"ࠪࡧࡷ࡫ࡡࡵࡧࡧࡣࡦࡺࠧ฻")] if session[bstack111lll_opy_ (u"ࠫࡨࡸࡥࡢࡶࡨࡨࡤࡧࡴࠨ฼")] else bstack111lll_opy_ (u"ࠬ࠭฽"))
@measure(event_name=EVENTS.bstack11ll11lll1_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l11l11l_opy_=bstack11l1l1llll_opy_)
def bstack11llllll1_opy_(sessions, bstack1l111lll1_opy_):
  try:
    bstack11llll11ll_opy_ = bstack111lll_opy_ (u"ࠨࠢ฾")
    if not os.path.exists(bstack1llll11l11_opy_):
      os.mkdir(bstack1llll11l11_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack111lll_opy_ (u"ࠧࡢࡵࡶࡩࡹࡹ࠯ࡳࡧࡳࡳࡷࡺ࠮ࡩࡶࡰࡰࠬ฿")), bstack111lll_opy_ (u"ࠨࡴࠪเ")) as f:
      bstack11llll11ll_opy_ = f.read()
    bstack11llll11ll_opy_ = bstack11llll11ll_opy_.replace(bstack111lll_opy_ (u"ࠩࡾࠩࡗࡋࡓࡖࡎࡗࡗࡤࡉࡏࡖࡐࡗࠩࢂ࠭แ"), str(len(sessions)))
    bstack11llll11ll_opy_ = bstack11llll11ll_opy_.replace(bstack111lll_opy_ (u"ࠪࡿࠪࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠦࡿࠪโ"), bstack1l111lll1_opy_)
    bstack11llll11ll_opy_ = bstack11llll11ll_opy_.replace(bstack111lll_opy_ (u"ࠫࢀࠫࡂࡖࡋࡏࡈࡤࡔࡁࡎࡇࠨࢁࠬใ"),
                                              sessions[0].get(bstack111lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣࡳࡧ࡭ࡦࠩไ")) if sessions[0] else bstack111lll_opy_ (u"࠭ࠧๅ"))
    with open(os.path.join(bstack1llll11l11_opy_, bstack111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡲࡦࡲࡲࡶࡹ࠴ࡨࡵ࡯࡯ࠫๆ")), bstack111lll_opy_ (u"ࠨࡹࠪ็")) as stream:
      stream.write(bstack11llll11ll_opy_.split(bstack111lll_opy_ (u"ࠩࡾࠩࡘࡋࡓࡔࡋࡒࡒࡘࡥࡄࡂࡖࡄࠩࢂ่࠭"))[0])
      for session in sessions:
        stream.write(bstack1l11111l_opy_(session))
      stream.write(bstack11llll11ll_opy_.split(bstack111lll_opy_ (u"ࠪࡿ࡙ࠪࡅࡔࡕࡌࡓࡓ࡙࡟ࡅࡃࡗࡅࠪࢃ้ࠧ"))[1])
    logger.info(bstack111lll_opy_ (u"ࠫࡌ࡫࡮ࡦࡴࡤࡸࡪࡪࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡢࡶ࡫࡯ࡨࠥࡧࡲࡵ࡫ࡩࡥࡨࡺࡳࠡࡣࡷࠤࢀࢃ๊ࠧ").format(bstack1llll11l11_opy_));
  except Exception as e:
    logger.debug(bstack1ll11l1l_opy_.format(str(e)))
def bstack1l1l11111_opy_(hashed_id):
  global CONFIG
  try:
    bstack11ll1ll1_opy_ = datetime.datetime.now()
    host = bstack111lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡱ࡫࠰ࡧࡱࡵࡵࡥ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ๋ࠬ") if bstack111lll_opy_ (u"࠭ࡡࡱࡲࠪ์") in CONFIG else bstack111lll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨํ")
    user = CONFIG[bstack111lll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ๎")]
    key = CONFIG[bstack111lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ๏")]
    bstack1ll11ll1l1_opy_ = bstack111lll_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩ๐") if bstack111lll_opy_ (u"ࠫࡦࡶࡰࠨ๑") in CONFIG else (bstack111lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩ๒") if CONFIG.get(bstack111lll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪ๓")) else bstack111lll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩ๔"))
    if cli.is_running():
      host = bstack111llll1l_opy_(cli.config, [bstack111lll_opy_ (u"ࠣࡣࡳ࡭ࡸࠨ๕"), bstack111lll_opy_ (u"ࠤࡤࡴࡵࡇࡵࡵࡱࡰࡥࡹ࡫ࠢ๖"), bstack111lll_opy_ (u"ࠥࡥࡵ࡯ࠢ๗")], host) if bstack111lll_opy_ (u"ࠫࡦࡶࡰࠨ๘") in CONFIG else bstack111llll1l_opy_(cli.config, [bstack111lll_opy_ (u"ࠧࡧࡰࡪࡵࠥ๙"), bstack111lll_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥࠣ๚"), bstack111lll_opy_ (u"ࠢࡢࡲ࡬ࠦ๛")], host)
    url = bstack111lll_opy_ (u"ࠨࡽࢀ࠳ࢀࢃ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡷࡪࡹࡳࡪࡱࡱࡷ࠳ࡰࡳࡰࡰࠪ๜").format(host, bstack1ll11ll1l1_opy_, hashed_id)
    headers = {
      bstack111lll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨ๝"): bstack111lll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭๞"),
    }
    proxies = bstack1llll1ll11_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies, auth=(user, key))
    if response.json():
      cli.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼ࡪࡩࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࡠ࡮࡬ࡷࡹࠨ๟"), datetime.datetime.now() - bstack11ll1ll1_opy_)
      return list(map(lambda session: session[bstack111lll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡩࡸࡹࡩࡰࡰࠪ๠")], response.json()))
  except Exception as e:
    logger.debug(bstack1l1ll111_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack11l11l1111_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l11l11l_opy_=bstack11l1l1llll_opy_)
def get_build_link():
  global CONFIG
  global bstack1l1l1l1l_opy_
  try:
    if bstack111lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ๡") in CONFIG:
      bstack11ll1ll1_opy_ = datetime.datetime.now()
      host = bstack111lll_opy_ (u"ࠧࡢࡲ࡬࠱ࡨࡲ࡯ࡶࡦࠪ๢") if bstack111lll_opy_ (u"ࠨࡣࡳࡴࠬ๣") in CONFIG else bstack111lll_opy_ (u"ࠩࡤࡴ࡮࠭๤")
      user = CONFIG[bstack111lll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ๥")]
      key = CONFIG[bstack111lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ๦")]
      bstack1ll11ll1l1_opy_ = bstack111lll_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ๧") if bstack111lll_opy_ (u"࠭ࡡࡱࡲࠪ๨") in CONFIG else bstack111lll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩ๩")
      url = bstack111lll_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡾࢁ࠿ࢁࡽࡁࡽࢀ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡼࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠱࡮ࡸࡵ࡮ࠨ๪").format(user, key, host, bstack1ll11ll1l1_opy_)
      if cli.is_enabled(CONFIG):
        bstack1l111lll1_opy_, hashed_id = cli.bstack11111llll_opy_()
        logger.info(bstack1ll1111l_opy_.format(bstack1l111lll1_opy_))
        return [hashed_id, bstack1l111lll1_opy_]
      else:
        headers = {
          bstack111lll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨ๫"): bstack111lll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭๬"),
        }
        if bstack111lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭๭") in CONFIG:
          params = {bstack111lll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ๮"): CONFIG[bstack111lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ๯")], bstack111lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ๰"): CONFIG[bstack111lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ๱")]}
        else:
          params = {bstack111lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ๲"): CONFIG[bstack111lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭๳")]}
        proxies = bstack1llll1ll11_opy_(CONFIG, url)
        response = requests.get(url, params=params, headers=headers, proxies=proxies)
        if response.json():
          bstack1l1111lll_opy_ = response.json()[0][bstack111lll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡤࡸ࡭ࡱࡪࠧ๴")]
          if bstack1l1111lll_opy_:
            bstack1l111lll1_opy_ = bstack1l1111lll_opy_[bstack111lll_opy_ (u"ࠬࡶࡵࡣ࡮࡬ࡧࡤࡻࡲ࡭ࠩ๵")].split(bstack111lll_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨ࠳ࡢࡶ࡫࡯ࡨࠬ๶"))[0] + bstack111lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡹ࠯ࠨ๷") + bstack1l1111lll_opy_[
              bstack111lll_opy_ (u"ࠨࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ๸")]
            logger.info(bstack1ll1111l_opy_.format(bstack1l111lll1_opy_))
            bstack1l1l1l1l_opy_ = bstack1l1111lll_opy_[bstack111lll_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ๹")]
            bstack11l111l1l_opy_ = CONFIG[bstack111lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭๺")]
            if bstack111lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭๻") in CONFIG:
              bstack11l111l1l_opy_ += bstack111lll_opy_ (u"ࠬࠦࠧ๼") + CONFIG[bstack111lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ๽")]
            if bstack11l111l1l_opy_ != bstack1l1111lll_opy_[bstack111lll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ๾")]:
              logger.debug(bstack1lll1l1l1l_opy_.format(bstack1l1111lll_opy_[bstack111lll_opy_ (u"ࠨࡰࡤࡱࡪ࠭๿")], bstack11l111l1l_opy_))
            cli.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺ࡨࡧࡷࡣࡧࡻࡩ࡭ࡦࡢࡰ࡮ࡴ࡫ࠣ຀"), datetime.datetime.now() - bstack11ll1ll1_opy_)
            return [bstack1l1111lll_opy_[bstack111lll_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ກ")], bstack1l111lll1_opy_]
    else:
      logger.warn(bstack1ll1llll1_opy_)
  except Exception as e:
    logger.debug(bstack1l1l1l1l11_opy_.format(str(e)))
  return [None, None]
def bstack11ll111l1l_opy_(url, bstack1l1lll111_opy_=False):
  global CONFIG
  global bstack1l11ll111_opy_
  if not bstack1l11ll111_opy_:
    hostname = bstack1l1l1lll1_opy_(url)
    is_private = bstack11111l1l1_opy_(hostname)
    if (bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨຂ") in CONFIG and not bstack1ll111ll1_opy_(CONFIG[bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ຃")])) and (is_private or bstack1l1lll111_opy_):
      bstack1l11ll111_opy_ = hostname
def bstack1l1l1lll1_opy_(url):
  return urlparse(url).hostname
def bstack11111l1l1_opy_(hostname):
  for bstack11l11ll11l_opy_ in bstack1ll1l111l1_opy_:
    regex = re.compile(bstack11l11ll11l_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack11ll1llll1_opy_(bstack11l111111_opy_):
  return True if bstack11l111111_opy_ in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack1l1l111111_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l11l11l_opy_=bstack11l1l1llll_opy_)
def getAccessibilityResults(driver):
  global CONFIG
  global bstack11l1l11ll1_opy_
  bstack11llll1l1_opy_ = not (bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪຄ"), None) and bstack1ll11l1l1l_opy_(
          threading.current_thread(), bstack111lll_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭຅"), None))
  bstack11l1l11l_opy_ = getattr(driver, bstack111lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨຆ"), None) != True
  bstack1ll1l11l_opy_ = bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩງ"), None) and bstack1ll11l1l1l_opy_(
          threading.current_thread(), bstack111lll_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬຈ"), None)
  if bstack1ll1l11l_opy_:
    if not bstack1ll1l1ll11_opy_():
      logger.warning(bstack111lll_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡶࡰࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡄࡴࡵࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹ࠮ࠣຉ"))
      return {}
    logger.debug(bstack111lll_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡴࡨࡷࡺࡲࡴࡴࠩຊ"))
    logger.debug(perform_scan(driver, driver_command=bstack111lll_opy_ (u"࠭ࡥࡹࡧࡦࡹࡹ࡫ࡓࡤࡴ࡬ࡴࡹ࠭຋")))
    results = bstack1ll1lll1l1_opy_(bstack111lll_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡳࠣຌ"))
    if results is not None and results.get(bstack111lll_opy_ (u"ࠣ࡫ࡶࡷࡺ࡫ࡳࠣຍ")) is not None:
        return results[bstack111lll_opy_ (u"ࠤ࡬ࡷࡸࡻࡥࡴࠤຎ")]
    logger.error(bstack111lll_opy_ (u"ࠥࡒࡴࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡒࡦࡵࡸࡰࡹࡹࠠࡸࡧࡵࡩࠥ࡬࡯ࡶࡰࡧ࠲ࠧຏ"))
    return []
  if not bstack1l11l11ll1_opy_.bstack1111111l1_opy_(CONFIG, bstack11l1l11ll1_opy_) or (bstack11l1l11l_opy_ and bstack11llll1l1_opy_):
    logger.warning(bstack111lll_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡪࡺࡲࡪࡧࡹࡩࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸ࠴ࠢຐ"))
    return {}
  try:
    logger.debug(bstack111lll_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡴࡨࡷࡺࡲࡴࡴࠩຑ"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack11ll1l1ll_opy_.bstack11llll11l_opy_)
    return results
  except Exception:
    logger.error(bstack111lll_opy_ (u"ࠨࡎࡰࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡻࡪࡸࡥࠡࡨࡲࡹࡳࡪ࠮ࠣຒ"))
    return {}
@measure(event_name=EVENTS.bstack1ll1l1lll_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l11l11l_opy_=bstack11l1l1llll_opy_)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack11l1l11ll1_opy_
  bstack11llll1l1_opy_ = not (bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫຓ"), None) and bstack1ll11l1l1l_opy_(
          threading.current_thread(), bstack111lll_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧດ"), None))
  bstack11l1l11l_opy_ = getattr(driver, bstack111lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩຕ"), None) != True
  bstack1ll1l11l_opy_ = bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪຖ"), None) and bstack1ll11l1l1l_opy_(
          threading.current_thread(), bstack111lll_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ທ"), None)
  if bstack1ll1l11l_opy_:
    if not bstack1ll1l1ll11_opy_():
      logger.warning(bstack111lll_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡰࡱࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡅࡵࡶࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡵࡸࡱࡲࡧࡲࡺ࠰ࠥຘ"))
      return {}
    logger.debug(bstack111lll_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡷࡺࡳ࡭ࡢࡴࡼࠫນ"))
    logger.debug(perform_scan(driver, driver_command=bstack111lll_opy_ (u"ࠧࡦࡺࡨࡧࡺࡺࡥࡔࡥࡵ࡭ࡵࡺࠧບ")))
    results = bstack1ll1lll1l1_opy_(bstack111lll_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࡔࡷࡰࡱࡦࡸࡹࠣປ"))
    if results is not None and results.get(bstack111lll_opy_ (u"ࠤࡶࡹࡲࡳࡡࡳࡻࠥຜ")) is not None:
        return results[bstack111lll_opy_ (u"ࠥࡷࡺࡳ࡭ࡢࡴࡼࠦຝ")]
    logger.error(bstack111lll_opy_ (u"ࠦࡓࡵࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡓࡧࡶࡹࡱࡺࡳࠡࡕࡸࡱࡲࡧࡲࡺࠢࡺࡥࡸࠦࡦࡰࡷࡱࡨ࠳ࠨພ"))
    return {}
  if not bstack1l11l11ll1_opy_.bstack1111111l1_opy_(CONFIG, bstack11l1l11ll1_opy_) or (bstack11l1l11l_opy_ and bstack11llll1l1_opy_):
    logger.warning(bstack111lll_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡴࡷࡰࡱࡦࡸࡹ࠯ࠤຟ"))
    return {}
  try:
    logger.debug(bstack111lll_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡷࡺࡳ࡭ࡢࡴࡼࠫຠ"))
    logger.debug(perform_scan(driver))
    bstack1ll11l11l_opy_ = driver.execute_async_script(bstack11ll1l1ll_opy_.bstack11llllll1l_opy_)
    return bstack1ll11l11l_opy_
  except Exception:
    logger.error(bstack111lll_opy_ (u"ࠢࡏࡱࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡺࡳ࡭ࡢࡴࡼࠤࡼࡧࡳࠡࡨࡲࡹࡳࡪ࠮ࠣມ"))
    return {}
def bstack1ll1l1ll11_opy_():
  global CONFIG
  global bstack11l1l11ll1_opy_
  bstack111llll11_opy_ = bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨຢ"), None) and bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫຣ"), None)
  if not bstack1l11l11ll1_opy_.bstack1111111l1_opy_(CONFIG, bstack11l1l11ll1_opy_) or not bstack111llll11_opy_:
        logger.warning(bstack111lll_opy_ (u"ࠥࡒࡴࡺࠠࡢࡰࠣࡅࡵࡶࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࠡࡴࡨࡷࡺࡲࡴࡴ࠰ࠥ຤"))
        return False
  return True
def bstack1ll1lll1l1_opy_(bstack11l11lll1l_opy_):
    bstack1ll1ll1111_opy_ = bstack11111ll1l_opy_.current_test_uuid() if bstack11111ll1l_opy_.current_test_uuid() else bstack11l1ll111_opy_.current_hook_uuid()
    with ThreadPoolExecutor() as executor:
        future = executor.submit(bstack11ll111l_opy_(bstack1ll1ll1111_opy_, bstack11l11lll1l_opy_))
        try:
            return future.result(timeout=bstack11l1lll1_opy_)
        except TimeoutError:
            logger.error(bstack111lll_opy_ (u"࡙ࠦ࡯࡭ࡦࡱࡸࡸࠥࡧࡦࡵࡧࡵࠤࢀࢃࡳࠡࡹ࡫࡭ࡱ࡫ࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡕࡩࡸࡻ࡬ࡵࡵࠥລ").format(bstack11l1lll1_opy_))
        except Exception as ex:
            logger.debug(bstack111lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡷ࡫ࡴࡳ࡫ࡨࡺ࡮ࡴࡧࠡࡃࡳࡴࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡾࢁ࠳ࠦࡅࡳࡴࡲࡶࠥ࠳ࠠࡼࡿࠥ຦").format(bstack11l11lll1l_opy_, str(ex)))
    return {}
@measure(event_name=EVENTS.bstack1ll1l1l1_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l11l11l_opy_=bstack11l1l1llll_opy_)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack11l1l11ll1_opy_
  bstack11llll1l1_opy_ = not (bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪວ"), None) and bstack1ll11l1l1l_opy_(
          threading.current_thread(), bstack111lll_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ຨ"), None))
  bstack1ll1111ll1_opy_ = not (bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨຩ"), None) and bstack1ll11l1l1l_opy_(
          threading.current_thread(), bstack111lll_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫສ"), None))
  bstack11l1l11l_opy_ = getattr(driver, bstack111lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪຫ"), None) != True
  if not bstack1l11l11ll1_opy_.bstack1111111l1_opy_(CONFIG, bstack11l1l11ll1_opy_) or (bstack11l1l11l_opy_ and bstack11llll1l1_opy_ and bstack1ll1111ll1_opy_):
    logger.warning(bstack111lll_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡺࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡥࡤࡲ࠳ࠨຬ"))
    return {}
  try:
    bstack1lll11ll1_opy_ = bstack111lll_opy_ (u"ࠬࡧࡰࡱࠩອ") in CONFIG and CONFIG.get(bstack111lll_opy_ (u"࠭ࡡࡱࡲࠪຮ"), bstack111lll_opy_ (u"ࠧࠨຯ"))
    session_id = getattr(driver, bstack111lll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠬະ"), None)
    if not session_id:
      logger.warning(bstack111lll_opy_ (u"ࠤࡑࡳࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡉࡅࠢࡩࡳࡺࡴࡤࠡࡨࡲࡶࠥࡪࡲࡪࡸࡨࡶࠧັ"))
      return {bstack111lll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤາ"): bstack111lll_opy_ (u"ࠦࡓࡵࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡋࡇࠤ࡫ࡵࡵ࡯ࡦࠥຳ")}
    if bstack1lll11ll1_opy_:
      try:
        bstack11ll11ll11_opy_ = {
              bstack111lll_opy_ (u"ࠬࡺࡨࡋࡹࡷࡘࡴࡱࡥ࡯ࠩິ"): os.environ.get(bstack111lll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫີ"), os.environ.get(bstack111lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫຶ"), bstack111lll_opy_ (u"ࠨࠩື"))),
              bstack111lll_opy_ (u"ࠩࡷ࡬࡙࡫ࡳࡵࡔࡸࡲ࡚ࡻࡩࡥຸࠩ"): bstack11111ll1l_opy_.current_test_uuid() if bstack11111ll1l_opy_.current_test_uuid() else bstack11l1ll111_opy_.current_hook_uuid(),
              bstack111lll_opy_ (u"ࠪࡥࡺࡺࡨࡉࡧࡤࡨࡪࡸູࠧ"): os.environ.get(bstack111lll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕ຺ࠩ")),
              bstack111lll_opy_ (u"ࠬࡹࡣࡢࡰࡗ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬົ"): str(int(datetime.datetime.now().timestamp() * 1000)),
              bstack111lll_opy_ (u"࠭ࡴࡩࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫຼ"): os.environ.get(bstack111lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬຽ"), bstack111lll_opy_ (u"ࠨࠩ຾")),
              bstack111lll_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࠩ຿"): kwargs.get(bstack111lll_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࡢࡧࡴࡳ࡭ࡢࡰࡧࠫເ"), None) or bstack111lll_opy_ (u"ࠫࠬແ")
          }
        if not hasattr(thread_local, bstack111lll_opy_ (u"ࠬࡨࡡࡴࡧࡢࡥࡵࡶ࡟ࡢ࠳࠴ࡽࡤࡹࡣࡳ࡫ࡳࡸࠬໂ")):
            scripts = {bstack111lll_opy_ (u"࠭ࡳࡤࡣࡱࠫໃ"): bstack11ll1l1ll_opy_.perform_scan}
            thread_local.base_app_a11y_script = scripts
        bstack1ll1111l11_opy_ = copy.deepcopy(thread_local.base_app_a11y_script)
        bstack1ll1111l11_opy_[bstack111lll_opy_ (u"ࠧࡴࡥࡤࡲࠬໄ")] = bstack1ll1111l11_opy_[bstack111lll_opy_ (u"ࠨࡵࡦࡥࡳ࠭໅")] % json.dumps(bstack11ll11ll11_opy_)
        bstack11ll1l1ll_opy_.bstack1ll1l11l1_opy_(bstack1ll1111l11_opy_)
        bstack11ll1l1ll_opy_.store()
        bstack1llll1111_opy_ = driver.execute_script(bstack11ll1l1ll_opy_.perform_scan)
      except Exception as bstack1l1l11l1_opy_:
        logger.info(bstack111lll_opy_ (u"ࠤࡄࡴࡵ࡯ࡵ࡮ࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡧࡦࡴࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࠤໆ") + str(bstack1l1l11l1_opy_))
        bstack1llll1111_opy_ = {bstack111lll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤ໇"): str(bstack1l1l11l1_opy_)}
    else:
      bstack1llll1111_opy_ = driver.execute_async_script(bstack11ll1l1ll_opy_.perform_scan, {bstack111lll_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧ່ࠫ"): kwargs.get(bstack111lll_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࡤࡩ࡯࡮࡯ࡤࡲࡩ້࠭"), None) or bstack111lll_opy_ (u"໊࠭ࠧ")})
    return bstack1llll1111_opy_
  except Exception as err:
    logger.error(bstack111lll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡶࡺࡴࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡥࡤࡲ࠳ࠦࡻࡾࠤ໋").format(str(err)))
    return {}