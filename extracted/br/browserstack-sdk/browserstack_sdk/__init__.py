# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
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
from browserstack_sdk.bstack1ll11l1lll_opy_ import bstack1ll1lll11_opy_
from browserstack_sdk.bstack11111l1l_opy_ import *
import time
import requests
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.measure import measure
def bstack1ll1ll1l1l_opy_():
  global CONFIG
  headers = {
        bstack11ll11_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack11ll11_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1l1ll111_opy_(CONFIG, bstack111lll1l_opy_)
  try:
    response = requests.get(bstack111lll1l_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1l11llll1_opy_ = response.json()[bstack11ll11_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack11lll11l_opy_.format(response.json()))
      return bstack1l11llll1_opy_
    else:
      logger.debug(bstack1llll1111_opy_.format(bstack11ll11_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack1llll1111_opy_.format(e))
def bstack1ll1111l1_opy_(hub_url):
  global CONFIG
  url = bstack11ll11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack11ll11_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack11ll11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack11ll11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1l1ll111_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1111ll111_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack11l1ll111_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack1ll11l1l1_opy_, stage=STAGE.bstack1lll11llll_opy_)
def bstack11ll111ll_opy_():
  try:
    global bstack11lll111ll_opy_
    bstack1l11llll1_opy_ = bstack1ll1ll1l1l_opy_()
    bstack1l111ll11_opy_ = []
    results = []
    for bstack11llll1ll_opy_ in bstack1l11llll1_opy_:
      bstack1l111ll11_opy_.append(bstack1l1l11l1l_opy_(target=bstack1ll1111l1_opy_,args=(bstack11llll1ll_opy_,)))
    for t in bstack1l111ll11_opy_:
      t.start()
    for t in bstack1l111ll11_opy_:
      results.append(t.join())
    bstack1llll111_opy_ = {}
    for item in results:
      hub_url = item[bstack11ll11_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack11ll11_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack1llll111_opy_[hub_url] = latency
    bstack1lllll111l_opy_ = min(bstack1llll111_opy_, key= lambda x: bstack1llll111_opy_[x])
    bstack11lll111ll_opy_ = bstack1lllll111l_opy_
    logger.debug(bstack11lll1ll1_opy_.format(bstack1lllll111l_opy_))
  except Exception as e:
    logger.debug(bstack1l1l11l1l1_opy_.format(e))
from browserstack_sdk.bstack1l1ll11ll1_opy_ import *
from browserstack_sdk.bstack1l1ll1l1l1_opy_ import *
from browserstack_sdk.bstack11l111ll11_opy_ import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.bstack1111l1ll1_opy_ import get_logger
from bstack_utils.measure import measure
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack1ll1l1l1l_opy_, stage=STAGE.bstack1lll11llll_opy_)
def bstack1l1l1lll1l_opy_():
    global bstack11lll111ll_opy_
    try:
        bstack11l11l1l1_opy_ = bstack1llll1l1l_opy_()
        bstack11ll1lll11_opy_(bstack11l11l1l1_opy_)
        hub_url = bstack11l11l1l1_opy_.get(bstack11ll11_opy_ (u"ࠨࡵࡳ࡮ࠥࢀ"), bstack11ll11_opy_ (u"ࠢࠣࢁ"))
        if hub_url.endswith(bstack11ll11_opy_ (u"ࠨ࠱ࡺࡨ࠴࡮ࡵࡣࠩࢂ")):
            hub_url = hub_url.rsplit(bstack11ll11_opy_ (u"ࠩ࠲ࡻࡩ࠵ࡨࡶࡤࠪࢃ"), 1)[0]
        if hub_url.startswith(bstack11ll11_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫࢄ")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack11ll11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࠭ࢅ")):
            hub_url = hub_url[8:]
        bstack11lll111ll_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack1llll1l1l_opy_():
    global CONFIG
    bstack1llllll111_opy_ = CONFIG.get(bstack11ll11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢆ"), {}).get(bstack11ll11_opy_ (u"࠭ࡧࡳ࡫ࡧࡒࡦࡳࡥࠨࢇ"), bstack11ll11_opy_ (u"ࠧࡏࡑࡢࡋࡗࡏࡄࡠࡐࡄࡑࡊࡥࡐࡂࡕࡖࡉࡉ࠭࢈"))
    if not isinstance(bstack1llllll111_opy_, str):
        raise ValueError(bstack11ll11_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡈࡴ࡬ࡨࠥࡴࡡ࡮ࡧࠣࡱࡺࡹࡴࠡࡤࡨࠤࡦࠦࡶࡢ࡮࡬ࡨࠥࡹࡴࡳ࡫ࡱ࡫ࠧࢉ"))
    try:
        bstack11l11l1l1_opy_ = bstack111lll11_opy_(bstack1llllll111_opy_)
        return bstack11l11l1l1_opy_
    except Exception as e:
        logger.error(bstack11ll11_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣࢊ").format(str(e)))
        return {}
def bstack111lll11_opy_(bstack1llllll111_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack11ll11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࢋ")] or not CONFIG[bstack11ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧࢌ")]:
            raise ValueError(bstack11ll11_opy_ (u"ࠧࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠠࡰࡴࠣࡥࡨࡩࡥࡴࡵࠣ࡯ࡪࡿࠢࢍ"))
        url = bstack1ll11l1ll1_opy_ + bstack1llllll111_opy_
        auth = (CONFIG[bstack11ll11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨࢎ")], CONFIG[bstack11ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ࢏")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack11l1111l1_opy_ = json.loads(response.text)
            return bstack11l1111l1_opy_
    except ValueError as ve:
        logger.error(bstack11ll11_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣ࢐").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack11ll11_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥ࡭ࡲࡪࡦࠣࡨࡪࡺࡡࡪ࡮ࡶࠤ࠿ࠦࡻࡾࠤ࢑").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack11ll1lll11_opy_(bstack1l111l1lll_opy_):
    global CONFIG
    if bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ࢒") not in CONFIG or str(CONFIG[bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ࢓")]).lower() == bstack11ll11_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ࢔"):
        CONFIG[bstack11ll11_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬ࢕")] = False
    elif bstack11ll11_opy_ (u"ࠧࡪࡵࡗࡶ࡮ࡧ࡬ࡈࡴ࡬ࡨࠬ࢖") in bstack1l111l1lll_opy_:
        bstack11l11l1ll_opy_ = CONFIG.get(bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢗ"), {})
        logger.debug(bstack11ll11_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡰࡴࡩࡡ࡭ࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࠪࡹࠢ࢘"), bstack11l11l1ll_opy_)
        bstack1lll1ll11l_opy_ = bstack1l111l1lll_opy_.get(bstack11ll11_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡕࡩࡵ࡫ࡡࡵࡧࡵࡷ࢙ࠧ"), [])
        bstack1111lll11_opy_ = bstack11ll11_opy_ (u"ࠦ࠱ࠨ࢚").join(bstack1lll1ll11l_opy_)
        logger.debug(bstack11ll11_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡈࡻࡳࡵࡱࡰࠤࡷ࡫ࡰࡦࡣࡷࡩࡷࠦࡳࡵࡴ࡬ࡲ࡬ࡀࠠࠦࡵ࢛ࠥ"), bstack1111lll11_opy_)
        bstack1l111llll1_opy_ = {
            bstack11ll11_opy_ (u"ࠨ࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣ࢜"): bstack11ll11_opy_ (u"ࠢࡢࡶࡶ࠱ࡷ࡫ࡰࡦࡣࡷࡩࡷࠨ࢝"),
            bstack11ll11_opy_ (u"ࠣࡨࡲࡶࡨ࡫ࡌࡰࡥࡤࡰࠧ࢞"): bstack11ll11_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ࢟"),
            bstack11ll11_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠧࢠ"): bstack1111lll11_opy_
        }
        bstack11l11l1ll_opy_.update(bstack1l111llll1_opy_)
        logger.debug(bstack11ll11_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼࡙ࠣࡵࡪࡡࡵࡧࡧࠤࡱࡵࡣࡢ࡮ࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࠫࡳࠣࢡ"), bstack11l11l1ll_opy_)
        CONFIG[bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢢ")] = bstack11l11l1ll_opy_
        logger.debug(bstack11ll11_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡌࡩ࡯ࡣ࡯ࠤࡈࡕࡎࡇࡋࡊ࠾ࠥࠫࡳࠣࢣ"), CONFIG)
def bstack11lll1l11_opy_():
    bstack11l11l1l1_opy_ = bstack1llll1l1l_opy_()
    if not bstack11l11l1l1_opy_[bstack11ll11_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࡙ࡷࡲࠧࢤ")]:
      raise ValueError(bstack11ll11_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࡚ࡸ࡬ࠡ࡫ࡶࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࡬ࡲࡰ࡯ࠣ࡫ࡷ࡯ࡤࠡࡦࡨࡸࡦ࡯࡬ࡴ࠰ࠥࢥ"))
    return bstack11l11l1l1_opy_[bstack11ll11_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࡛ࡲ࡭ࠩࢦ")] + bstack11ll11_opy_ (u"ࠪࡃࡨࡧࡰࡴ࠿ࠪࢧ")
@measure(event_name=EVENTS.bstack1l11l1111l_opy_, stage=STAGE.bstack1lll11llll_opy_)
def bstack11l11lllll_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack11ll11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ࢨ")], CONFIG[bstack11ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࢩ")])
        url = bstack1l11lll1ll_opy_
        logger.debug(bstack11ll11_opy_ (u"ࠨࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬ࡲࡰ࡯ࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡗࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࠦࡁࡑࡋࠥࢪ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack11ll11_opy_ (u"ࠢࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪࠨࢫ"): bstack11ll11_opy_ (u"ࠣࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠦࢬ")})
            if response.status_code == 200:
                bstack1l11lllll1_opy_ = json.loads(response.text)
                bstack1l11lll111_opy_ = bstack1l11lllll1_opy_.get(bstack11ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡴࠩࢭ"), [])
                if bstack1l11lll111_opy_:
                    bstack1l111l1ll1_opy_ = bstack1l11lll111_opy_[0]
                    build_hashed_id = bstack1l111l1ll1_opy_.get(bstack11ll11_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ࢮ"))
                    bstack1lll1l1l_opy_ = bstack1lll1lll11_opy_ + build_hashed_id
                    result.extend([build_hashed_id, bstack1lll1l1l_opy_])
                    logger.info(bstack1l11l1ll11_opy_.format(bstack1lll1l1l_opy_))
                    bstack1l111l1111_opy_ = CONFIG[bstack11ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧࢯ")]
                    if bstack11ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢰ") in CONFIG:
                      bstack1l111l1111_opy_ += bstack11ll11_opy_ (u"࠭ࠠࠨࢱ") + CONFIG[bstack11ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࢲ")]
                    if bstack1l111l1111_opy_ != bstack1l111l1ll1_opy_.get(bstack11ll11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ࢳ")):
                      logger.debug(bstack11l11l11l_opy_.format(bstack1l111l1ll1_opy_.get(bstack11ll11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧࢴ")), bstack1l111l1111_opy_))
                    return result
                else:
                    logger.debug(bstack11ll11_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡑࡳࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡵࡪࡨࠤࡷ࡫ࡳࡱࡱࡱࡷࡪ࠴ࠢࢵ"))
            else:
                logger.debug(bstack11ll11_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢶ"))
        except Exception as e:
            logger.error(bstack11ll11_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࡹࠠ࠻ࠢࡾࢁࠧࢷ").format(str(e)))
    else:
        logger.debug(bstack11ll11_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡉࡏࡏࡈࡌࡋࠥ࡯ࡳࠡࡰࡲࡸࠥࡹࡥࡵ࠰࡙ࠣࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢸ"))
    return [None, None]
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack11111l11l_opy_ import bstack11111l11l_opy_, bstack11l11l1l_opy_, bstack11l11ll1_opy_, bstack11ll1111ll_opy_
from bstack_utils.measure import bstack1ll11ll1_opy_
from bstack_utils.measure import measure
from bstack_utils.percy import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1111l111l_opy_ import bstack1l11lll1l1_opy_
from bstack_utils.messages import *
from bstack_utils import bstack1111l1ll1_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1111ll1ll_opy_, bstack1llll1ll_opy_, bstack1l1l11ll1_opy_, bstack111ll1lll_opy_, \
  bstack1l111lll1l_opy_, \
  Notset, bstack1llll11l1l_opy_, \
  bstack1l1l11111l_opy_, bstack1ll11111l1_opy_, bstack11llllll_opy_, bstack11l1l1l1l_opy_, bstack111ll11l_opy_, bstack1111llll1_opy_, \
  bstack11lll11111_opy_, \
  bstack1l11ll1l1_opy_, bstack11l111l11_opy_, bstack1lll111lll_opy_, bstack11llll11l1_opy_, \
  bstack1lll1l1l1_opy_, bstack1lll1l111_opy_, bstack1l111ll1l_opy_, bstack11l1l1l1_opy_
from bstack_utils.bstack11l1111ll1_opy_ import bstack11ll11l1ll_opy_
from bstack_utils.bstack11lll1lll1_opy_ import bstack1l1111l1ll_opy_, bstack1ll1ll1lll_opy_
from bstack_utils.bstack1ll111111_opy_ import bstack1l1l11l111_opy_
from bstack_utils.bstack1l1l11l11l_opy_ import bstack11l1l1l11l_opy_, bstack11lll1l11l_opy_
from bstack_utils.bstack11llll1l1l_opy_ import bstack11llll1l1l_opy_
from bstack_utils.bstack11ll1lll_opy_ import bstack1lll11111_opy_
from bstack_utils.proxy import bstack1ll1lll1_opy_, bstack1l1ll111_opy_, bstack1l111111l1_opy_, bstack1ll111l11l_opy_
from bstack_utils.bstack1l1lllllll_opy_ import bstack1ll11lll11_opy_
import bstack_utils.bstack11l1lll11l_opy_ as bstack1l1ll1lll1_opy_
import bstack_utils.bstack1ll11ll1ll_opy_ as bstack1lll1111l1_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.utils.bstack1l1ll1ll1_opy_ import bstack11111lll1_opy_
from bstack_utils.bstack1lll111l_opy_ import bstack111l11l1l_opy_
from bstack_utils.bstack1l1l1l1ll1_opy_ import bstack11l111lll_opy_
if os.getenv(bstack11ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡌࡔࡕࡋࡔࠩࢹ")):
  cli.bstack1ll1l111_opy_()
else:
  os.environ[bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡍࡕࡏࡌࡕࠪࢺ")] = bstack11ll11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧࢻ")
bstack1111l111_opy_ = bstack11ll11_opy_ (u"ࠪࠤࠥ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࠣࠤ࡮࡬ࠨࡱࡣࡪࡩࠥࡃ࠽࠾ࠢࡹࡳ࡮ࡪࠠ࠱ࠫࠣࡿࡡࡴࠠࠡࠢࡷࡶࡾࢁ࡜࡯ࠢࡦࡳࡳࡹࡴࠡࡨࡶࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨ࡝ࠩࡩࡷࡡ࠭ࠩ࠼࡞ࡱࠤࠥࠦࠠࠡࡨࡶ࠲ࡦࡶࡰࡦࡰࡧࡊ࡮ࡲࡥࡔࡻࡱࡧ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪ࠯ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡶ࡟ࡪࡰࡧࡩࡽ࠯ࠠࠬࠢࠥ࠾ࠧࠦࠫࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࠨࡢࡹࡤ࡭ࡹࠦ࡮ࡦࡹࡓࡥ࡬࡫࠲࠯ࡧࡹࡥࡱࡻࡡࡵࡧࠫࠦ࠭࠯ࠠ࠾ࡀࠣࡿࢂࠨࠬࠡ࡞ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥ࡫ࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡄࡦࡶࡤ࡭ࡱࡹࠢࡾ࡞ࠪ࠭࠮࠯࡛ࠣࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠦࡢ࠯ࠠࠬࠢࠥ࠰ࡡࡢ࡮ࠣࠫ࡟ࡲࠥࠦࠠࠡࡿࡦࡥࡹࡩࡨࠩࡧࡻ࠭ࢀࡢ࡮ࠡࠢࠣࠤࢂࡢ࡮ࠡࠢࢀࡠࡳࠦࠠ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱ࠪࢼ")
bstack11lll11lll_opy_ = bstack11ll11_opy_ (u"ࠫࡡࡴ࠯ࠫࠢࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࠦࠪ࠰࡞ࡱࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠶ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡩࡡࡱࡵࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠷࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡲࡢ࡭ࡳࡪࡥࡹࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠷ࡣ࡜࡯ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯ࡵ࡯࡭ࡨ࡫ࠨ࠱࠮ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸࠯࡜࡯ࡥࡲࡲࡸࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯ࠥࡃࠠࡳࡧࡴࡹ࡮ࡸࡥࠩࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨࠩ࠼࡞ࡱ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡰࡦࡻ࡮ࡤࡪࠣࡁࠥࡧࡳࡺࡰࡦࠤ࠭ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷ࠮ࠦ࠽࠿ࠢࡾࡠࡳࡲࡥࡵࠢࡦࡥࡵࡹ࠻࡝ࡰࡷࡶࡾࠦࡻ࡝ࡰࡦࡥࡵࡹࠠ࠾ࠢࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࡢࡴࡶࡤࡧࡰࡥࡣࡢࡲࡶ࠭ࡡࡴࠠࠡࡿࠣࡧࡦࡺࡣࡩࠪࡨࡼ࠮ࠦࡻ࡝ࡰࠣࠤࠥࠦࡽ࡝ࡰࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࠻ࠢࡣࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠩࢁࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭ࢂࡦࠬ࡝ࡰࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴ࡞ࡱࠤࠥࢃࠩ࡝ࡰࢀࡠࡳ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࠪࢽ")
from ._version import __version__
bstack1ll11l1l1l_opy_ = None
CONFIG = {}
bstack1l111111ll_opy_ = {}
bstack1ll1llllll_opy_ = {}
bstack11ll1111l1_opy_ = None
bstack111ll1l11_opy_ = None
bstack11ll11lll_opy_ = None
bstack11llllllll_opy_ = -1
bstack111l1l111_opy_ = 0
bstack11lllll11l_opy_ = bstack11ll11ll_opy_
bstack1l111llll_opy_ = 1
bstack111lll1ll_opy_ = False
bstack11l111ll1_opy_ = False
bstack1lll11l1ll_opy_ = bstack11ll11_opy_ (u"ࠬ࠭ࢾ")
bstack11llllll11_opy_ = bstack11ll11_opy_ (u"࠭ࠧࢿ")
bstack1ll1lllll1_opy_ = False
bstack11ll11l1_opy_ = True
bstack11l1111l11_opy_ = bstack11ll11_opy_ (u"ࠧࠨࣀ")
bstack1l11ll1ll1_opy_ = []
bstack11lll111ll_opy_ = bstack11ll11_opy_ (u"ࠨࠩࣁ")
bstack1ll111ll11_opy_ = False
bstack1lllll1lll_opy_ = None
bstack1lll111l1_opy_ = None
bstack11111111_opy_ = None
bstack1ll1l111l1_opy_ = -1
bstack11ll1l11l1_opy_ = os.path.join(os.path.expanduser(bstack11ll11_opy_ (u"ࠩࢁࠫࣂ")), bstack11ll11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪࣃ"), bstack11ll11_opy_ (u"ࠫ࠳ࡸ࡯ࡣࡱࡷ࠱ࡷ࡫ࡰࡰࡴࡷ࠱࡭࡫࡬ࡱࡧࡵ࠲࡯ࡹ࡯࡯ࠩࣄ"))
bstack11ll1l1l1_opy_ = 0
bstack111l1lll_opy_ = 0
bstack11l11l1111_opy_ = []
bstack1l1l1lll11_opy_ = []
bstack11l1llll1_opy_ = []
bstack1ll1l1111_opy_ = []
bstack1l11l1l11_opy_ = bstack11ll11_opy_ (u"ࠬ࠭ࣅ")
bstack11llll11l_opy_ = bstack11ll11_opy_ (u"࠭ࠧࣆ")
bstack1llllll1ll_opy_ = False
bstack11l111111l_opy_ = False
bstack1lll1ll1ll_opy_ = {}
bstack1l1llll1_opy_ = None
bstack11llll1l_opy_ = None
bstack11l1ll1111_opy_ = None
bstack1111lll1l_opy_ = None
bstack11l1ll1l1l_opy_ = None
bstack1ll11l11l1_opy_ = None
bstack1ll1l1lll1_opy_ = None
bstack111ll1l1_opy_ = None
bstack11ll1111_opy_ = None
bstack11l1l1ll1l_opy_ = None
bstack11l11l1l1l_opy_ = None
bstack11ll11111l_opy_ = None
bstack1ll1111ll1_opy_ = None
bstack11lllllll_opy_ = None
bstack1l1l1ll111_opy_ = None
bstack1lll11ll1_opy_ = None
bstack11l111l1_opy_ = None
bstack1l1111l11_opy_ = None
bstack1ll111ll1_opy_ = None
bstack1ll11ll11_opy_ = None
bstack1l11l1llll_opy_ = None
bstack1ll11ll1l1_opy_ = None
bstack11l1111ll_opy_ = None
thread_local = threading.local()
bstack11l1ll1l11_opy_ = False
bstack1l1111ll11_opy_ = bstack11ll11_opy_ (u"ࠢࠣࣇ")
logger = bstack1111l1ll1_opy_.get_logger(__name__, bstack11lllll11l_opy_)
bstack1l1ll1llll_opy_ = Config.bstack1lll11ll_opy_()
percy = bstack1l1111ll1_opy_()
bstack1lll1l1111_opy_ = bstack1l11lll1l1_opy_()
bstack1ll1ll1111_opy_ = bstack11l111ll11_opy_()
def bstack11l1lll1_opy_():
  global CONFIG
  global bstack1llllll1ll_opy_
  global bstack1l1ll1llll_opy_
  testContextOptions = bstack11lll111_opy_(CONFIG)
  if bstack1l111lll1l_opy_(CONFIG):
    if (bstack11ll11_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪࣈ") in testContextOptions and str(testContextOptions[bstack11ll11_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫࣉ")]).lower() == bstack11ll11_opy_ (u"ࠪࡸࡷࡻࡥࠨ࣊")):
      bstack1llllll1ll_opy_ = True
    bstack1l1ll1llll_opy_.bstack1111111l_opy_(testContextOptions.get(bstack11ll11_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ࣋"), False))
  else:
    bstack1llllll1ll_opy_ = True
    bstack1l1ll1llll_opy_.bstack1111111l_opy_(True)
def bstack11l11lll1_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1lll1ll1_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1ll1ll11_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack11ll11_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡩ࡯࡯ࡨ࡬࡫࡫࡯࡬ࡦࠤ࣌") == args[i].lower() or bstack11ll11_opy_ (u"ࠨ࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡪ࡮࡭ࠢ࣍") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack11l1111l11_opy_
      bstack11l1111l11_opy_ += bstack11ll11_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠤࠬ࣎") + path
      return path
  return None
bstack1l1ll1ll_opy_ = re.compile(bstack11ll11_opy_ (u"ࡳࠤ࠱࠮ࡄࡢࠤࡼࠪ࠱࠮ࡄ࠯ࡽ࠯ࠬࡂ࣏ࠦ"))
def bstack1l11ll1l11_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1l1ll1ll_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack11ll11_opy_ (u"ࠤࠧࡿ࣐ࠧ") + group + bstack11ll11_opy_ (u"ࠥࢁ࣑ࠧ"), os.environ.get(group))
  return value
def bstack1lll1l1ll1_opy_():
  global bstack11l1111ll_opy_
  if bstack11l1111ll_opy_ is None:
        bstack11l1111ll_opy_ = bstack1ll1ll11_opy_()
  bstack1l111111_opy_ = bstack11l1111ll_opy_
  if bstack1l111111_opy_ and os.path.exists(os.path.abspath(bstack1l111111_opy_)):
    fileName = bstack1l111111_opy_
  if bstack11ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ࣒") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack11ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆ࣓ࠩ")])) and not bstack11ll11_opy_ (u"࠭ࡦࡪ࡮ࡨࡒࡦࡳࡥࠨࣔ") in locals():
    fileName = os.environ[bstack11ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫࣕ")]
  if bstack11ll11_opy_ (u"ࠨࡨ࡬ࡰࡪࡔࡡ࡮ࡧࠪࣖ") in locals():
    bstack1llll11_opy_ = os.path.abspath(fileName)
  else:
    bstack1llll11_opy_ = bstack11ll11_opy_ (u"ࠩࠪࣗ")
  bstack1ll11lllll_opy_ = os.getcwd()
  bstack11l1ll1l_opy_ = bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ࣘ")
  bstack111111l1_opy_ = bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡦࡳ࡬ࠨࣙ")
  while (not os.path.exists(bstack1llll11_opy_)) and bstack1ll11lllll_opy_ != bstack11ll11_opy_ (u"ࠧࠨࣚ"):
    bstack1llll11_opy_ = os.path.join(bstack1ll11lllll_opy_, bstack11l1ll1l_opy_)
    if not os.path.exists(bstack1llll11_opy_):
      bstack1llll11_opy_ = os.path.join(bstack1ll11lllll_opy_, bstack111111l1_opy_)
    if bstack1ll11lllll_opy_ != os.path.dirname(bstack1ll11lllll_opy_):
      bstack1ll11lllll_opy_ = os.path.dirname(bstack1ll11lllll_opy_)
    else:
      bstack1ll11lllll_opy_ = bstack11ll11_opy_ (u"ࠨࠢࣛ")
  bstack11l1111ll_opy_ = bstack1llll11_opy_ if os.path.exists(bstack1llll11_opy_) else None
  return bstack11l1111ll_opy_
def bstack1l1ll11111_opy_():
  bstack1llll11_opy_ = bstack1lll1l1ll1_opy_()
  if not os.path.exists(bstack1llll11_opy_):
    bstack1ll11l111_opy_(
      bstack11lllll11_opy_.format(os.getcwd()))
  try:
    with open(bstack1llll11_opy_, bstack11ll11_opy_ (u"ࠧࡳࠩࣜ")) as stream:
      yaml.add_implicit_resolver(bstack11ll11_opy_ (u"ࠣࠣࡳࡥࡹ࡮ࡥࡹࠤࣝ"), bstack1l1ll1ll_opy_)
      yaml.add_constructor(bstack11ll11_opy_ (u"ࠤࠤࡴࡦࡺࡨࡦࡺࠥࣞ"), bstack1l11ll1l11_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack1llll11_opy_, bstack11ll11_opy_ (u"ࠪࡶࠬࣟ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack1ll11l111_opy_(bstack1l11ll11ll_opy_.format(str(exc)))
def bstack11lll1lll_opy_(config):
  bstack1ll111llll_opy_ = bstack1lllllll1l_opy_(config)
  for option in list(bstack1ll111llll_opy_):
    if option.lower() in bstack1lll111l11_opy_ and option != bstack1lll111l11_opy_[option.lower()]:
      bstack1ll111llll_opy_[bstack1lll111l11_opy_[option.lower()]] = bstack1ll111llll_opy_[option]
      del bstack1ll111llll_opy_[option]
  return config
def bstack1111l1l1_opy_():
  global bstack1ll1llllll_opy_
  for key, bstack1lllll11l1_opy_ in bstack1ll1l1ll11_opy_.items():
    if isinstance(bstack1lllll11l1_opy_, list):
      for var in bstack1lllll11l1_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1ll1llllll_opy_[key] = os.environ[var]
          break
    elif bstack1lllll11l1_opy_ in os.environ and os.environ[bstack1lllll11l1_opy_] and str(os.environ[bstack1lllll11l1_opy_]).strip():
      bstack1ll1llllll_opy_[key] = os.environ[bstack1lllll11l1_opy_]
  if bstack11ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭࣠") in os.environ:
    bstack1ll1llllll_opy_[bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ࣡")] = {}
    bstack1ll1llllll_opy_[bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ࣢")][bstack11ll11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࣣࠩ")] = os.environ[bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪࣤ")]
def bstack11llll1l1_opy_():
  global bstack1l111111ll_opy_
  global bstack11l1111l11_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack11ll11_opy_ (u"ࠩ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣥ").lower() == val.lower():
      bstack1l111111ll_opy_[bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࣦࠧ")] = {}
      bstack1l111111ll_opy_[bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣧ")][bstack11ll11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣨ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack1l1l111111_opy_ in bstack1ll1l1l1_opy_.items():
    if isinstance(bstack1l1l111111_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1l1l111111_opy_:
          if idx < len(sys.argv) and bstack11ll11_opy_ (u"࠭࠭࠮ࣩࠩ") + var.lower() == val.lower() and not key in bstack1l111111ll_opy_:
            bstack1l111111ll_opy_[key] = sys.argv[idx + 1]
            bstack11l1111l11_opy_ += bstack11ll11_opy_ (u"ࠧࠡ࠯࠰ࠫ࣪") + var + bstack11ll11_opy_ (u"ࠨࠢࠪ࣫") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack11ll11_opy_ (u"ࠩ࠰࠱ࠬ࣬") + bstack1l1l111111_opy_.lower() == val.lower() and not key in bstack1l111111ll_opy_:
          bstack1l111111ll_opy_[key] = sys.argv[idx + 1]
          bstack11l1111l11_opy_ += bstack11ll11_opy_ (u"ࠪࠤ࠲࠳࣭ࠧ") + bstack1l1l111111_opy_ + bstack11ll11_opy_ (u"࣮ࠫࠥ࠭") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1l1l1l1111_opy_(config):
  bstack11lllllll1_opy_ = config.keys()
  for bstack1ll1lll1l_opy_, bstack111llllll_opy_ in bstack1l1l1l11l_opy_.items():
    if bstack111llllll_opy_ in bstack11lllllll1_opy_:
      config[bstack1ll1lll1l_opy_] = config[bstack111llllll_opy_]
      del config[bstack111llllll_opy_]
  for bstack1ll1lll1l_opy_, bstack111llllll_opy_ in bstack11ll1l111_opy_.items():
    if isinstance(bstack111llllll_opy_, list):
      for bstack11l1l11l1l_opy_ in bstack111llllll_opy_:
        if bstack11l1l11l1l_opy_ in bstack11lllllll1_opy_:
          config[bstack1ll1lll1l_opy_] = config[bstack11l1l11l1l_opy_]
          del config[bstack11l1l11l1l_opy_]
          break
    elif bstack111llllll_opy_ in bstack11lllllll1_opy_:
      config[bstack1ll1lll1l_opy_] = config[bstack111llllll_opy_]
      del config[bstack111llllll_opy_]
  for bstack11l1l11l1l_opy_ in list(config):
    for bstack1ll1lll1l1_opy_ in bstack1lll111l1l_opy_:
      if bstack11l1l11l1l_opy_.lower() == bstack1ll1lll1l1_opy_.lower() and bstack11l1l11l1l_opy_ != bstack1ll1lll1l1_opy_:
        config[bstack1ll1lll1l1_opy_] = config[bstack11l1l11l1l_opy_]
        del config[bstack11l1l11l1l_opy_]
  bstack111ll111_opy_ = [{}]
  if not config.get(bstack11ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ࣯")):
    config[bstack11ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࣰࠩ")] = [{}]
  bstack111ll111_opy_ = config[bstack11ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࣱࠪ")]
  for platform in bstack111ll111_opy_:
    for bstack11l1l11l1l_opy_ in list(platform):
      for bstack1ll1lll1l1_opy_ in bstack1lll111l1l_opy_:
        if bstack11l1l11l1l_opy_.lower() == bstack1ll1lll1l1_opy_.lower() and bstack11l1l11l1l_opy_ != bstack1ll1lll1l1_opy_:
          platform[bstack1ll1lll1l1_opy_] = platform[bstack11l1l11l1l_opy_]
          del platform[bstack11l1l11l1l_opy_]
  for bstack1ll1lll1l_opy_, bstack111llllll_opy_ in bstack11ll1l111_opy_.items():
    for platform in bstack111ll111_opy_:
      if isinstance(bstack111llllll_opy_, list):
        for bstack11l1l11l1l_opy_ in bstack111llllll_opy_:
          if bstack11l1l11l1l_opy_ in platform:
            platform[bstack1ll1lll1l_opy_] = platform[bstack11l1l11l1l_opy_]
            del platform[bstack11l1l11l1l_opy_]
            break
      elif bstack111llllll_opy_ in platform:
        platform[bstack1ll1lll1l_opy_] = platform[bstack111llllll_opy_]
        del platform[bstack111llllll_opy_]
  for bstack1l1l11ll1l_opy_ in bstack1llll11ll_opy_:
    if bstack1l1l11ll1l_opy_ in config:
      if not bstack1llll11ll_opy_[bstack1l1l11ll1l_opy_] in config:
        config[bstack1llll11ll_opy_[bstack1l1l11ll1l_opy_]] = {}
      config[bstack1llll11ll_opy_[bstack1l1l11ll1l_opy_]].update(config[bstack1l1l11ll1l_opy_])
      del config[bstack1l1l11ll1l_opy_]
  for platform in bstack111ll111_opy_:
    for bstack1l1l11ll1l_opy_ in bstack1llll11ll_opy_:
      if bstack1l1l11ll1l_opy_ in list(platform):
        if not bstack1llll11ll_opy_[bstack1l1l11ll1l_opy_] in platform:
          platform[bstack1llll11ll_opy_[bstack1l1l11ll1l_opy_]] = {}
        platform[bstack1llll11ll_opy_[bstack1l1l11ll1l_opy_]].update(platform[bstack1l1l11ll1l_opy_])
        del platform[bstack1l1l11ll1l_opy_]
  config = bstack11lll1lll_opy_(config)
  return config
def bstack11l1ll11ll_opy_(config):
  global bstack11llllll11_opy_
  bstack1l1111l1_opy_ = False
  if bstack11ll11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࣲࠬ") in config and str(config[bstack11ll11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ࣳ")]).lower() != bstack11ll11_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩࣴ"):
    if bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨࣵ") not in config or str(config[bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࣶࠩ")]).lower() == bstack11ll11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬࣷ"):
      config[bstack11ll11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭ࣸ")] = False
    else:
      bstack11l11l1l1_opy_ = bstack1llll1l1l_opy_()
      if bstack11ll11_opy_ (u"ࠨ࡫ࡶࡘࡷ࡯ࡡ࡭ࡉࡵ࡭ࡩࣹ࠭") in bstack11l11l1l1_opy_:
        if not bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸࣺ࠭") in config:
          config[bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࣻ")] = {}
        config[bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣼ")][bstack11ll11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣽ")] = bstack11ll11_opy_ (u"࠭ࡡࡵࡵ࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠬࣾ")
        bstack1l1111l1_opy_ = True
        bstack11llllll11_opy_ = config[bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࣿ")].get(bstack11ll11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪऀ"))
  if bstack1l111lll1l_opy_(config) and bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ँ") in config and str(config[bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧं")]).lower() != bstack11ll11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪः") and not bstack1l1111l1_opy_:
    if not bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩऄ") in config:
      config[bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪअ")] = {}
    if not config[bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫआ")].get(bstack11ll11_opy_ (u"ࠨࡵ࡮࡭ࡵࡈࡩ࡯ࡣࡵࡽࡎࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡡࡵ࡫ࡲࡲࠬइ")) and not bstack11ll11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫई") in config[bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧउ")]:
      bstack1l11l11ll_opy_ = datetime.datetime.now()
      bstack1ll1111l1l_opy_ = bstack1l11l11ll_opy_.strftime(bstack11ll11_opy_ (u"ࠫࠪࡪ࡟ࠦࡤࡢࠩࡍࠫࡍࠨऊ"))
      hostname = socket.gethostname()
      bstack1ll1l1ll1l_opy_ = bstack11ll11_opy_ (u"ࠬ࠭ऋ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack11ll11_opy_ (u"࠭ࡻࡾࡡࡾࢁࡤࢁࡽࠨऌ").format(bstack1ll1111l1l_opy_, hostname, bstack1ll1l1ll1l_opy_)
      config[bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫऍ")][bstack11ll11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪऎ")] = identifier
    bstack11llllll11_opy_ = config[bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ए")].get(bstack11ll11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬऐ"))
  return config
def bstack1ll11ll111_opy_():
  bstack11lll11ll_opy_ =  bstack11l1l1l1l_opy_()[bstack11ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠪऑ")]
  return bstack11lll11ll_opy_ if bstack11lll11ll_opy_ else -1
def bstack11lll1l1ll_opy_(bstack11lll11ll_opy_):
  global CONFIG
  if not bstack11ll11_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧऒ") in CONFIG[bstack11ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨओ")]:
    return
  CONFIG[bstack11ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऔ")] = CONFIG[bstack11ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪक")].replace(
    bstack11ll11_opy_ (u"ࠩࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫख"),
    str(bstack11lll11ll_opy_)
  )
def bstack11l1lll1ll_opy_():
  global CONFIG
  if not bstack11ll11_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾࠩग") in CONFIG[bstack11ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭घ")]:
    return
  bstack1l11l11ll_opy_ = datetime.datetime.now()
  bstack1ll1111l1l_opy_ = bstack1l11l11ll_opy_.strftime(bstack11ll11_opy_ (u"ࠬࠫࡤ࠮ࠧࡥ࠱ࠪࡎ࠺ࠦࡏࠪङ"))
  CONFIG[bstack11ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨच")] = CONFIG[bstack11ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩछ")].replace(
    bstack11ll11_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧज"),
    bstack1ll1111l1l_opy_
  )
def bstack1l1111l11l_opy_():
  global CONFIG
  if bstack11ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫझ") in CONFIG and not bool(CONFIG[bstack11ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬञ")]):
    del CONFIG[bstack11ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ट")]
    return
  if not bstack11ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧठ") in CONFIG:
    CONFIG[bstack11ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨड")] = bstack11ll11_opy_ (u"ࠧࠤࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪढ")
  if bstack11ll11_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧण") in CONFIG[bstack11ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫत")]:
    bstack11l1lll1ll_opy_()
    os.environ[bstack11ll11_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧथ")] = CONFIG[bstack11ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭द")]
  if not bstack11ll11_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧध") in CONFIG[bstack11ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨन")]:
    return
  bstack11lll11ll_opy_ = bstack11ll11_opy_ (u"ࠧࠨऩ")
  bstack1ll111l1ll_opy_ = bstack1ll11ll111_opy_()
  if bstack1ll111l1ll_opy_ != -1:
    bstack11lll11ll_opy_ = bstack11ll11_opy_ (u"ࠨࡅࡌࠤࠬप") + str(bstack1ll111l1ll_opy_)
  if bstack11lll11ll_opy_ == bstack11ll11_opy_ (u"ࠩࠪफ"):
    bstack11l1l111_opy_ = bstack1ll1l1l1ll_opy_(CONFIG[bstack11ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ब")])
    if bstack11l1l111_opy_ != -1:
      bstack11lll11ll_opy_ = str(bstack11l1l111_opy_)
  if bstack11lll11ll_opy_:
    bstack11lll1l1ll_opy_(bstack11lll11ll_opy_)
    os.environ[bstack11ll11_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨभ")] = CONFIG[bstack11ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧम")]
def bstack1l1l1ll1l_opy_(bstack1l11lll11l_opy_, bstack1l1111lll_opy_, path):
  bstack1l1l11l1ll_opy_ = {
    bstack11ll11_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪय"): bstack1l1111lll_opy_
  }
  if os.path.exists(path):
    bstack11l1l1l1l1_opy_ = json.load(open(path, bstack11ll11_opy_ (u"ࠧࡳࡤࠪर")))
  else:
    bstack11l1l1l1l1_opy_ = {}
  bstack11l1l1l1l1_opy_[bstack1l11lll11l_opy_] = bstack1l1l11l1ll_opy_
  with open(path, bstack11ll11_opy_ (u"ࠣࡹ࠮ࠦऱ")) as outfile:
    json.dump(bstack11l1l1l1l1_opy_, outfile)
def bstack1ll1l1l1ll_opy_(bstack1l11lll11l_opy_):
  bstack1l11lll11l_opy_ = str(bstack1l11lll11l_opy_)
  bstack1l11l111l1_opy_ = os.path.join(os.path.expanduser(bstack11ll11_opy_ (u"ࠩࢁࠫल")), bstack11ll11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪळ"))
  try:
    if not os.path.exists(bstack1l11l111l1_opy_):
      os.makedirs(bstack1l11l111l1_opy_)
    file_path = os.path.join(os.path.expanduser(bstack11ll11_opy_ (u"ࠫࢃ࠭ऴ")), bstack11ll11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬव"), bstack11ll11_opy_ (u"࠭࠮ࡣࡷ࡬ࡰࡩ࠳࡮ࡢ࡯ࡨ࠱ࡨࡧࡣࡩࡧ࠱࡮ࡸࡵ࡮ࠨश"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack11ll11_opy_ (u"ࠧࡸࠩष")):
        pass
      with open(file_path, bstack11ll11_opy_ (u"ࠣࡹ࠮ࠦस")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack11ll11_opy_ (u"ࠩࡵࠫह")) as bstack111111l1l_opy_:
      bstack111l1l1l_opy_ = json.load(bstack111111l1l_opy_)
    if bstack1l11lll11l_opy_ in bstack111l1l1l_opy_:
      bstack111l11l1_opy_ = bstack111l1l1l_opy_[bstack1l11lll11l_opy_][bstack11ll11_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऺ")]
      bstack11llll111l_opy_ = int(bstack111l11l1_opy_) + 1
      bstack1l1l1ll1l_opy_(bstack1l11lll11l_opy_, bstack11llll111l_opy_, file_path)
      return bstack11llll111l_opy_
    else:
      bstack1l1l1ll1l_opy_(bstack1l11lll11l_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1l1llll1ll_opy_.format(str(e)))
    return -1
def bstack1111111ll_opy_(config):
  if not config[bstack11ll11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ऻ")] or not config[bstack11ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ़")]:
    return True
  else:
    return False
def bstack1l1l1ll1_opy_(config, index=0):
  global bstack1ll1lllll1_opy_
  bstack1lllllll11_opy_ = {}
  caps = bstack111l1ll1_opy_ + bstack1l1ll1l111_opy_
  if config.get(bstack11ll11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪऽ"), False):
    bstack1lllllll11_opy_[bstack11ll11_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫा")] = True
    bstack1lllllll11_opy_[bstack11ll11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࡔࡶࡴࡪࡱࡱࡷࠬि")] = config.get(bstack11ll11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ी"), {})
  if bstack1ll1lllll1_opy_:
    caps += bstack1ll1ll1l1_opy_
  for key in config:
    if key in caps + [bstack11ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ु")]:
      continue
    bstack1lllllll11_opy_[key] = config[key]
  if bstack11ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧू") in config:
    for bstack1lllll1l1l_opy_ in config[bstack11ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨृ")][index]:
      if bstack1lllll1l1l_opy_ in caps:
        continue
      bstack1lllllll11_opy_[bstack1lllll1l1l_opy_] = config[bstack11ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩॄ")][index][bstack1lllll1l1l_opy_]
  bstack1lllllll11_opy_[bstack11ll11_opy_ (u"ࠧࡩࡱࡶࡸࡓࡧ࡭ࡦࠩॅ")] = socket.gethostname()
  if bstack11ll11_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩॆ") in bstack1lllllll11_opy_:
    del (bstack1lllllll11_opy_[bstack11ll11_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪे")])
  return bstack1lllllll11_opy_
def bstack1llll11l_opy_(config):
  global bstack1ll1lllll1_opy_
  bstack11l11ll111_opy_ = {}
  caps = bstack1l1ll1l111_opy_
  if bstack1ll1lllll1_opy_:
    caps += bstack1ll1ll1l1_opy_
  for key in caps:
    if key in config:
      bstack11l11ll111_opy_[key] = config[key]
  return bstack11l11ll111_opy_
def bstack11ll1ll1_opy_(bstack1lllllll11_opy_, bstack11l11ll111_opy_):
  bstack1l1llll1l1_opy_ = {}
  for key in bstack1lllllll11_opy_.keys():
    if key in bstack1l1l1l11l_opy_:
      bstack1l1llll1l1_opy_[bstack1l1l1l11l_opy_[key]] = bstack1lllllll11_opy_[key]
    else:
      bstack1l1llll1l1_opy_[key] = bstack1lllllll11_opy_[key]
  for key in bstack11l11ll111_opy_:
    if key in bstack1l1l1l11l_opy_:
      bstack1l1llll1l1_opy_[bstack1l1l1l11l_opy_[key]] = bstack11l11ll111_opy_[key]
    else:
      bstack1l1llll1l1_opy_[key] = bstack11l11ll111_opy_[key]
  return bstack1l1llll1l1_opy_
def bstack1l11l11l1_opy_(config, index=0):
  global bstack1ll1lllll1_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack1l1lll11l_opy_ = bstack1111ll1ll_opy_(bstack1lll1l1l1l_opy_, config, logger)
  bstack11l11ll111_opy_ = bstack1llll11l_opy_(config)
  bstack1l1l1ll11_opy_ = bstack1l1ll1l111_opy_
  bstack1l1l1ll11_opy_ += bstack1l1l1ll1l1_opy_
  bstack11l11ll111_opy_ = update(bstack11l11ll111_opy_, bstack1l1lll11l_opy_)
  if bstack1ll1lllll1_opy_:
    bstack1l1l1ll11_opy_ += bstack1ll1ll1l1_opy_
  if bstack11ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ै") in config:
    if bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩॉ") in config[bstack11ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨॊ")][index]:
      caps[bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫो")] = config[bstack11ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪौ")][index][bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ्࠭")]
    if bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪॎ") in config[bstack11ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॏ")][index]:
      caps[bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬॐ")] = str(config[bstack11ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ॑")][index][bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴ॒ࠧ")])
    bstack1l1l1l111_opy_ = bstack1111ll1ll_opy_(bstack1lll1l1l1l_opy_, config[bstack11ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ॓")][index], logger)
    bstack1l1l1ll11_opy_ += list(bstack1l1l1l111_opy_.keys())
    for bstack1ll1llll1_opy_ in bstack1l1l1ll11_opy_:
      if bstack1ll1llll1_opy_ in config[bstack11ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ॔")][index]:
        if bstack1ll1llll1_opy_ == bstack11ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫॕ"):
          try:
            bstack1l1l1l111_opy_[bstack1ll1llll1_opy_] = str(config[bstack11ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॖ")][index][bstack1ll1llll1_opy_] * 1.0)
          except:
            bstack1l1l1l111_opy_[bstack1ll1llll1_opy_] = str(config[bstack11ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॗ")][index][bstack1ll1llll1_opy_])
        else:
          bstack1l1l1l111_opy_[bstack1ll1llll1_opy_] = config[bstack11ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨक़")][index][bstack1ll1llll1_opy_]
        del (config[bstack11ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩख़")][index][bstack1ll1llll1_opy_])
    bstack11l11ll111_opy_ = update(bstack11l11ll111_opy_, bstack1l1l1l111_opy_)
  bstack1lllllll11_opy_ = bstack1l1l1ll1_opy_(config, index)
  for bstack11l1l11l1l_opy_ in bstack1l1ll1l111_opy_ + list(bstack1l1lll11l_opy_.keys()):
    if bstack11l1l11l1l_opy_ in bstack1lllllll11_opy_:
      bstack11l11ll111_opy_[bstack11l1l11l1l_opy_] = bstack1lllllll11_opy_[bstack11l1l11l1l_opy_]
      del (bstack1lllllll11_opy_[bstack11l1l11l1l_opy_])
  if bstack1llll11l1l_opy_(config):
    bstack1lllllll11_opy_[bstack11ll11_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧग़")] = True
    caps.update(bstack11l11ll111_opy_)
    caps[bstack11ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩज़")] = bstack1lllllll11_opy_
  else:
    bstack1lllllll11_opy_[bstack11ll11_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩड़")] = False
    caps.update(bstack11ll1ll1_opy_(bstack1lllllll11_opy_, bstack11l11ll111_opy_))
    if bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨढ़") in caps:
      caps[bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬफ़")] = caps[bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪय़")]
      del (caps[bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫॠ")])
    if bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨॡ") in caps:
      caps[bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪॢ")] = caps[bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪॣ")]
      del (caps[bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ।")])
  return caps
def bstack11ll11l111_opy_():
  global bstack11lll111ll_opy_
  global CONFIG
  if bstack1lll1ll1_opy_() <= version.parse(bstack11ll11_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫ॥")):
    if bstack11lll111ll_opy_ != bstack11ll11_opy_ (u"ࠬ࠭०"):
      return bstack11ll11_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ१") + bstack11lll111ll_opy_ + bstack11ll11_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦ२")
    return bstack11l1l11l11_opy_
  if bstack11lll111ll_opy_ != bstack11ll11_opy_ (u"ࠨࠩ३"):
    return bstack11ll11_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦ४") + bstack11lll111ll_opy_ + bstack11ll11_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦ५")
  return bstack11llll1lll_opy_
def bstack1l11ll111l_opy_(options):
  return hasattr(options, bstack11ll11_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬ६"))
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
def bstack11l1lllll_opy_(options, bstack11l111llll_opy_):
  for bstack111l1llll_opy_ in bstack11l111llll_opy_:
    if bstack111l1llll_opy_ in [bstack11ll11_opy_ (u"ࠬࡧࡲࡨࡵࠪ७"), bstack11ll11_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪ८")]:
      continue
    if bstack111l1llll_opy_ in options._experimental_options:
      options._experimental_options[bstack111l1llll_opy_] = update(options._experimental_options[bstack111l1llll_opy_],
                                                         bstack11l111llll_opy_[bstack111l1llll_opy_])
    else:
      options.add_experimental_option(bstack111l1llll_opy_, bstack11l111llll_opy_[bstack111l1llll_opy_])
  if bstack11ll11_opy_ (u"ࠧࡢࡴࡪࡷࠬ९") in bstack11l111llll_opy_:
    for arg in bstack11l111llll_opy_[bstack11ll11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭॰")]:
      options.add_argument(arg)
    del (bstack11l111llll_opy_[bstack11ll11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॱ")])
  if bstack11ll11_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧॲ") in bstack11l111llll_opy_:
    for ext in bstack11l111llll_opy_[bstack11ll11_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨॳ")]:
      try:
        options.add_extension(ext)
      except OSError:
        options.add_encoded_extension(ext)
    del (bstack11l111llll_opy_[bstack11ll11_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩॴ")])
def bstack1l1111llll_opy_(options, bstack11ll1l1l_opy_):
  if bstack11ll11_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬॵ") in bstack11ll1l1l_opy_:
    for bstack1ll1ll1ll_opy_ in bstack11ll1l1l_opy_[bstack11ll11_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ॶ")]:
      if bstack1ll1ll1ll_opy_ in options._preferences:
        options._preferences[bstack1ll1ll1ll_opy_] = update(options._preferences[bstack1ll1ll1ll_opy_], bstack11ll1l1l_opy_[bstack11ll11_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧॷ")][bstack1ll1ll1ll_opy_])
      else:
        options.set_preference(bstack1ll1ll1ll_opy_, bstack11ll1l1l_opy_[bstack11ll11_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨॸ")][bstack1ll1ll1ll_opy_])
  if bstack11ll11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨॹ") in bstack11ll1l1l_opy_:
    for arg in bstack11ll1l1l_opy_[bstack11ll11_opy_ (u"ࠫࡦࡸࡧࡴࠩॺ")]:
      options.add_argument(arg)
def bstack1l1l111ll1_opy_(options, bstack1lll1llll_opy_):
  if bstack11ll11_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼ࠭ॻ") in bstack1lll1llll_opy_:
    options.use_webview(bool(bstack1lll1llll_opy_[bstack11ll11_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࠧॼ")]))
  bstack11l1lllll_opy_(options, bstack1lll1llll_opy_)
def bstack11llll111_opy_(options, bstack1l1ll111l1_opy_):
  for bstack1111ll11l_opy_ in bstack1l1ll111l1_opy_:
    if bstack1111ll11l_opy_ in [bstack11ll11_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫॽ"), bstack11ll11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ॾ")]:
      continue
    options.set_capability(bstack1111ll11l_opy_, bstack1l1ll111l1_opy_[bstack1111ll11l_opy_])
  if bstack11ll11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॿ") in bstack1l1ll111l1_opy_:
    for arg in bstack1l1ll111l1_opy_[bstack11ll11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨঀ")]:
      options.add_argument(arg)
  if bstack11ll11_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨঁ") in bstack1l1ll111l1_opy_:
    options.bstack1l111111l_opy_(bool(bstack1l1ll111l1_opy_[bstack11ll11_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩং")]))
def bstack111l1111l_opy_(options, bstack1ll1111lll_opy_):
  for bstack1lll11ll11_opy_ in bstack1ll1111lll_opy_:
    if bstack1lll11ll11_opy_ in [bstack11ll11_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪঃ"), bstack11ll11_opy_ (u"ࠧࡢࡴࡪࡷࠬ঄")]:
      continue
    options._options[bstack1lll11ll11_opy_] = bstack1ll1111lll_opy_[bstack1lll11ll11_opy_]
  if bstack11ll11_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬঅ") in bstack1ll1111lll_opy_:
    for bstack1l111l1ll_opy_ in bstack1ll1111lll_opy_[bstack11ll11_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭আ")]:
      options.bstack1l11llll_opy_(
        bstack1l111l1ll_opy_, bstack1ll1111lll_opy_[bstack11ll11_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧই")][bstack1l111l1ll_opy_])
  if bstack11ll11_opy_ (u"ࠫࡦࡸࡧࡴࠩঈ") in bstack1ll1111lll_opy_:
    for arg in bstack1ll1111lll_opy_[bstack11ll11_opy_ (u"ࠬࡧࡲࡨࡵࠪউ")]:
      options.add_argument(arg)
def bstack11ll1ll11_opy_(options, caps):
  if not hasattr(options, bstack11ll11_opy_ (u"࠭ࡋࡆ࡛ࠪঊ")):
    return
  if options.KEY == bstack11ll11_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬঋ"):
    options = bstack11l11lll11_opy_.bstack11l1l111l_opy_(bstack11l11111l1_opy_=options, config=CONFIG)
  if options.KEY == bstack11ll11_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ঌ") and options.KEY in caps:
    bstack11l1lllll_opy_(options, caps[bstack11ll11_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ঍")])
  elif options.KEY == bstack11ll11_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨ঎") and options.KEY in caps:
    bstack1l1111llll_opy_(options, caps[bstack11ll11_opy_ (u"ࠫࡲࡵࡺ࠻ࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩএ")])
  elif options.KEY == bstack11ll11_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ঐ") and options.KEY in caps:
    bstack11llll111_opy_(options, caps[bstack11ll11_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧ঑")])
  elif options.KEY == bstack11ll11_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ঒") and options.KEY in caps:
    bstack1l1l111ll1_opy_(options, caps[bstack11ll11_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩও")])
  elif options.KEY == bstack11ll11_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨঔ") and options.KEY in caps:
    bstack111l1111l_opy_(options, caps[bstack11ll11_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩক")])
def bstack1ll11111l_opy_(caps):
  global bstack1ll1lllll1_opy_
  if isinstance(os.environ.get(bstack11ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬখ")), str):
    bstack1ll1lllll1_opy_ = eval(os.getenv(bstack11ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭গ")))
  if bstack1ll1lllll1_opy_:
    if bstack11l11lll1_opy_() < version.parse(bstack11ll11_opy_ (u"࠭࠲࠯࠵࠱࠴ࠬঘ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack11ll11_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧঙ")
    if bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭চ") in caps:
      browser = caps[bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧছ")]
    elif bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫজ") in caps:
      browser = caps[bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬঝ")]
    browser = str(browser).lower()
    if browser == bstack11ll11_opy_ (u"ࠬ࡯ࡰࡩࡱࡱࡩࠬঞ") or browser == bstack11ll11_opy_ (u"࠭ࡩࡱࡣࡧࠫট"):
      browser = bstack11ll11_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧঠ")
    if browser == bstack11ll11_opy_ (u"ࠨࡵࡤࡱࡸࡻ࡮ࡨࠩড"):
      browser = bstack11ll11_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩঢ")
    if browser not in [bstack11ll11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪণ"), bstack11ll11_opy_ (u"ࠫࡪࡪࡧࡦࠩত"), bstack11ll11_opy_ (u"ࠬ࡯ࡥࠨথ"), bstack11ll11_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭দ"), bstack11ll11_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨধ")]:
      return None
    try:
      package = bstack11ll11_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷ࠴ࡻࡾ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪন").format(browser)
      name = bstack11ll11_opy_ (u"ࠩࡒࡴࡹ࡯࡯࡯ࡵࠪ঩")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1l11ll111l_opy_(options):
        return None
      for bstack11l1l11l1l_opy_ in caps.keys():
        options.set_capability(bstack11l1l11l1l_opy_, caps[bstack11l1l11l1l_opy_])
      bstack11ll1ll11_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1ll1l1l11_opy_(options, bstack1lll1ll11_opy_):
  if not bstack1l11ll111l_opy_(options):
    return
  for bstack11l1l11l1l_opy_ in bstack1lll1ll11_opy_.keys():
    if bstack11l1l11l1l_opy_ in bstack1l1l1ll1l1_opy_:
      continue
    if bstack11l1l11l1l_opy_ in options._caps and type(options._caps[bstack11l1l11l1l_opy_]) in [dict, list]:
      options._caps[bstack11l1l11l1l_opy_] = update(options._caps[bstack11l1l11l1l_opy_], bstack1lll1ll11_opy_[bstack11l1l11l1l_opy_])
    else:
      options.set_capability(bstack11l1l11l1l_opy_, bstack1lll1ll11_opy_[bstack11l1l11l1l_opy_])
  bstack11ll1ll11_opy_(options, bstack1lll1ll11_opy_)
  if bstack11ll11_opy_ (u"ࠪࡱࡴࢀ࠺ࡥࡧࡥࡹ࡬࡭ࡥࡳࡃࡧࡨࡷ࡫ࡳࡴࠩপ") in options._caps:
    if options._caps[bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩফ")] and options._caps[bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪব")].lower() != bstack11ll11_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧভ"):
      del options._caps[bstack11ll11_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ࠭ম")]
def bstack1l1ll1ll1l_opy_(proxy_config):
  if bstack11ll11_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬয") in proxy_config:
    proxy_config[bstack11ll11_opy_ (u"ࠩࡶࡷࡱࡖࡲࡰࡺࡼࠫর")] = proxy_config[bstack11ll11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ঱")]
    del (proxy_config[bstack11ll11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨল")])
  if bstack11ll11_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ঳") in proxy_config and proxy_config[bstack11ll11_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩ঴")].lower() != bstack11ll11_opy_ (u"ࠧࡥ࡫ࡵࡩࡨࡺࠧ঵"):
    proxy_config[bstack11ll11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫশ")] = bstack11ll11_opy_ (u"ࠩࡰࡥࡳࡻࡡ࡭ࠩষ")
  if bstack11ll11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡃࡸࡸࡴࡩ࡯࡯ࡨ࡬࡫࡚ࡸ࡬ࠨস") in proxy_config:
    proxy_config[bstack11ll11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧহ")] = bstack11ll11_opy_ (u"ࠬࡶࡡࡤࠩ঺")
  return proxy_config
def bstack11l1l1111_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack11ll11_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ঻") in config:
    return proxy
  config[bstack11ll11_opy_ (u"ࠧࡱࡴࡲࡼࡾ়࠭")] = bstack1l1ll1ll1l_opy_(config[bstack11ll11_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧঽ")])
  if proxy == None:
    proxy = Proxy(config[bstack11ll11_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨা")])
  return proxy
def bstack11l11l11_opy_(self):
  global CONFIG
  global bstack11ll11111l_opy_
  try:
    proxy = bstack1l111111l1_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack11ll11_opy_ (u"ࠪ࠲ࡵࡧࡣࠨি")):
        proxies = bstack1ll1lll1_opy_(proxy, bstack11ll11l111_opy_())
        if len(proxies) > 0:
          protocol, bstack1l11l1ll1l_opy_ = proxies.popitem()
          if bstack11ll11_opy_ (u"ࠦ࠿࠵࠯ࠣী") in bstack1l11l1ll1l_opy_:
            return bstack1l11l1ll1l_opy_
          else:
            return bstack11ll11_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨু") + bstack1l11l1ll1l_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack11ll11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡳࡶࡴࡾࡹࠡࡷࡵࡰࠥࡀࠠࡼࡿࠥূ").format(str(e)))
  return bstack11ll11111l_opy_(self)
def bstack11l1ll111l_opy_():
  global CONFIG
  return bstack1ll111l11l_opy_(CONFIG) and bstack1111llll1_opy_() and bstack1lll1ll1_opy_() >= version.parse(bstack1lll111ll_opy_)
def bstack1l1llll111_opy_():
  global CONFIG
  return (bstack11ll11_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪৃ") in CONFIG or bstack11ll11_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬৄ") in CONFIG) and bstack11lll11111_opy_()
def bstack1lllllll1l_opy_(config):
  bstack1ll111llll_opy_ = {}
  if bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭৅") in config:
    bstack1ll111llll_opy_ = config[bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ৆")]
  if bstack11ll11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪে") in config:
    bstack1ll111llll_opy_ = config[bstack11ll11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫৈ")]
  proxy = bstack1l111111l1_opy_(config)
  if proxy:
    if proxy.endswith(bstack11ll11_opy_ (u"࠭࠮ࡱࡣࡦࠫ৉")) and os.path.isfile(proxy):
      bstack1ll111llll_opy_[bstack11ll11_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪ৊")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack11ll11_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭ো")):
        proxies = bstack1l1ll111_opy_(config, bstack11ll11l111_opy_())
        if len(proxies) > 0:
          protocol, bstack1l11l1ll1l_opy_ = proxies.popitem()
          if bstack11ll11_opy_ (u"ࠤ࠽࠳࠴ࠨৌ") in bstack1l11l1ll1l_opy_:
            parsed_url = urlparse(bstack1l11l1ll1l_opy_)
          else:
            parsed_url = urlparse(protocol + bstack11ll11_opy_ (u"ࠥ࠾࠴࠵্ࠢ") + bstack1l11l1ll1l_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1ll111llll_opy_[bstack11ll11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡋࡳࡸࡺࠧৎ")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1ll111llll_opy_[bstack11ll11_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡴࡸࡴࠨ৏")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1ll111llll_opy_[bstack11ll11_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡚ࡹࡥࡳࠩ৐")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1ll111llll_opy_[bstack11ll11_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖࡡࡴࡵࠪ৑")] = str(parsed_url.password)
  return bstack1ll111llll_opy_
def bstack11lll111_opy_(config):
  if bstack11ll11_opy_ (u"ࠨࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸ࠭৒") in config:
    return config[bstack11ll11_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧ৓")]
  return {}
def bstack1lll1lllll_opy_(caps):
  global bstack11llllll11_opy_
  if bstack11ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ৔") in caps:
    caps[bstack11ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ৕")][bstack11ll11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫ৖")] = True
    if bstack11llllll11_opy_:
      caps[bstack11ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧৗ")][bstack11ll11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ৘")] = bstack11llllll11_opy_
  else:
    caps[bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭৙")] = True
    if bstack11llllll11_opy_:
      caps[bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ৚")] = bstack11llllll11_opy_
@measure(event_name=EVENTS.bstack111l111ll_opy_, stage=STAGE.bstack1lll11llll_opy_, bstack1111llll_opy_=bstack11ll11lll_opy_)
def bstack111llll11_opy_():
  global CONFIG
  if not bstack1l111lll1l_opy_(CONFIG) or cli.is_enabled(CONFIG):
    return
  if bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ৛") in CONFIG and bstack1l111ll1l_opy_(CONFIG[bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨড়")]):
    if (
      bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩঢ়") in CONFIG
      and bstack1l111ll1l_opy_(CONFIG[bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ৞")].get(bstack11ll11_opy_ (u"ࠧࡴ࡭࡬ࡴࡇ࡯࡮ࡢࡴࡼࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡸࡧࡴࡪࡱࡱࠫয়")))
    ):
      logger.debug(bstack11ll11_opy_ (u"ࠣࡎࡲࡧࡦࡲࠠࡣ࡫ࡱࡥࡷࡿࠠ࡯ࡱࡷࠤࡸࡺࡡࡳࡶࡨࡨࠥࡧࡳࠡࡵ࡮࡭ࡵࡈࡩ࡯ࡣࡵࡽࡎࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡡࡵ࡫ࡲࡲࠥ࡯ࡳࠡࡧࡱࡥࡧࡲࡥࡥࠤৠ"))
      return
    bstack1ll111llll_opy_ = bstack1lllllll1l_opy_(CONFIG)
    bstack1lll1l11l_opy_(CONFIG[bstack11ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬৡ")], bstack1ll111llll_opy_)
def bstack1lll1l11l_opy_(key, bstack1ll111llll_opy_):
  global bstack1ll11l1l1l_opy_
  logger.info(bstack11l1l1l11_opy_)
  try:
    bstack1ll11l1l1l_opy_ = Local()
    bstack1l11111l_opy_ = {bstack11ll11_opy_ (u"ࠪ࡯ࡪࡿࠧৢ"): key}
    bstack1l11111l_opy_.update(bstack1ll111llll_opy_)
    logger.debug(bstack11l1l11lll_opy_.format(str(bstack1l11111l_opy_)).replace(key, bstack11ll11_opy_ (u"ࠫࡠࡘࡅࡅࡃࡆࡘࡊࡊ࡝ࠨৣ")))
    bstack1ll11l1l1l_opy_.start(**bstack1l11111l_opy_)
    if bstack1ll11l1l1l_opy_.isRunning():
      logger.info(bstack1lll1111l_opy_)
  except Exception as e:
    bstack1ll11l111_opy_(bstack1l11lll1l_opy_.format(str(e)))
def bstack11lll11ll1_opy_():
  global bstack1ll11l1l1l_opy_
  if bstack1ll11l1l1l_opy_.isRunning():
    logger.info(bstack11ll11l11l_opy_)
    bstack1ll11l1l1l_opy_.stop()
  bstack1ll11l1l1l_opy_ = None
def bstack1l1l1llll1_opy_(bstack1l1ll1ll11_opy_=[]):
  global CONFIG
  bstack1ll1l1lll_opy_ = []
  bstack1l1l11l11_opy_ = [bstack11ll11_opy_ (u"ࠬࡵࡳࠨ৤"), bstack11ll11_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ৥"), bstack11ll11_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ০"), bstack11ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪ১"), bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ২"), bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ৩")]
  try:
    for err in bstack1l1ll1ll11_opy_:
      bstack1l11l11ll1_opy_ = {}
      for k in bstack1l1l11l11_opy_:
        val = CONFIG[bstack11ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ৪")][int(err[bstack11ll11_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ৫")])].get(k)
        if val:
          bstack1l11l11ll1_opy_[k] = val
      if(err[bstack11ll11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ৬")] != bstack11ll11_opy_ (u"ࠧࠨ৭")):
        bstack1l11l11ll1_opy_[bstack11ll11_opy_ (u"ࠨࡶࡨࡷࡹࡹࠧ৮")] = {
          err[bstack11ll11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ৯")]: err[bstack11ll11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩৰ")]
        }
        bstack1ll1l1lll_opy_.append(bstack1l11l11ll1_opy_)
  except Exception as e:
    logger.debug(bstack11ll11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡰࡴࡰࡥࡹࡺࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷ࠾ࠥ࠭ৱ") + str(e))
  finally:
    return bstack1ll1l1lll_opy_
def bstack1l1ll1111_opy_(file_name):
  bstack1ll11l11_opy_ = []
  try:
    bstack1l1l1lllll_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1l1l1lllll_opy_):
      with open(bstack1l1l1lllll_opy_) as f:
        bstack1lll1ll111_opy_ = json.load(f)
        bstack1ll11l11_opy_ = bstack1lll1ll111_opy_
      os.remove(bstack1l1l1lllll_opy_)
    return bstack1ll11l11_opy_
  except Exception as e:
    logger.debug(bstack11ll11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧ࡫ࡱࡨ࡮ࡴࡧࠡࡧࡵࡶࡴࡸࠠ࡭࡫ࡶࡸ࠿ࠦࠧ৲") + str(e))
    return bstack1ll11l11_opy_
def bstack1ll1l1111l_opy_():
  try:
      from bstack_utils.constants import bstack1l1lll1111_opy_, EVENTS
      from bstack_utils.helper import bstack1llll1ll_opy_, get_host_info, bstack1l1ll1llll_opy_
      from datetime import datetime
      from filelock import FileLock
      bstack1llll1ll1l_opy_ = os.path.join(os.getcwd(), bstack11ll11_opy_ (u"࠭࡬ࡰࡩࠪ৳"), bstack11ll11_opy_ (u"ࠧ࡬ࡧࡼ࠱ࡲ࡫ࡴࡳ࡫ࡦࡷ࠳ࡰࡳࡰࡰࠪ৴"))
      lock = FileLock(bstack1llll1ll1l_opy_+bstack11ll11_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢ৵"))
      def bstack1l1l11lll1_opy_():
          try:
              with lock:
                  with open(bstack1llll1ll1l_opy_, bstack11ll11_opy_ (u"ࠤࡵࠦ৶"), encoding=bstack11ll11_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤ৷")) as file:
                      data = json.load(file)
                      config = {
                          bstack11ll11_opy_ (u"ࠦ࡭࡫ࡡࡥࡧࡵࡷࠧ৸"): {
                              bstack11ll11_opy_ (u"ࠧࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠦ৹"): bstack11ll11_opy_ (u"ࠨࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠤ৺"),
                          }
                      }
                      bstack1l1lll11_opy_ = datetime.utcnow()
                      bstack1l11l11ll_opy_ = bstack1l1lll11_opy_.strftime(bstack11ll11_opy_ (u"࡛ࠢࠦ࠰ࠩࡲ࠳ࠥࡥࡖࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࠲ࠪ࡬ࠠࡖࡖࡆࠦ৻"))
                      bstack1lll111111_opy_ = os.environ.get(bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ৼ")) if os.environ.get(bstack11ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ৽")) else bstack1l1ll1llll_opy_.get_property(bstack11ll11_opy_ (u"ࠥࡷࡩࡱࡒࡶࡰࡌࡨࠧ৾"))
                      payload = {
                          bstack11ll11_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠣ৿"): bstack11ll11_opy_ (u"ࠧࡹࡤ࡬ࡡࡨࡺࡪࡴࡴࡴࠤ਀"),
                          bstack11ll11_opy_ (u"ࠨࡤࡢࡶࡤࠦਁ"): {
                              bstack11ll11_opy_ (u"ࠢࡵࡧࡶࡸ࡭ࡻࡢࡠࡷࡸ࡭ࡩࠨਂ"): bstack1lll111111_opy_,
                              bstack11ll11_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡥࡡࡧࡥࡾࠨਃ"): bstack1l11l11ll_opy_,
                              bstack11ll11_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡰࡤࡱࡪࠨ਄"): bstack11ll11_opy_ (u"ࠥࡗࡉࡑࡆࡦࡣࡷࡹࡷ࡫ࡐࡦࡴࡩࡳࡷࡳࡡ࡯ࡥࡨࠦਅ"),
                              bstack11ll11_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢ࡮ࡸࡵ࡮ࠣਆ"): {
                                  bstack11ll11_opy_ (u"ࠧࡳࡥࡢࡵࡸࡶࡪࡹࠢਇ"): data,
                                  bstack11ll11_opy_ (u"ࠨࡳࡥ࡭ࡕࡹࡳࡏࡤࠣਈ"): bstack1l1ll1llll_opy_.get_property(bstack11ll11_opy_ (u"ࠢࡴࡦ࡮ࡖࡺࡴࡉࡥࠤਉ"))
                              },
                              bstack11ll11_opy_ (u"ࠣࡷࡶࡩࡷࡥࡤࡢࡶࡤࠦਊ"): bstack1l1ll1llll_opy_.get_property(bstack11ll11_opy_ (u"ࠤࡸࡷࡪࡸࡎࡢ࡯ࡨࠦ਋")),
                              bstack11ll11_opy_ (u"ࠥ࡬ࡴࡹࡴࡠ࡫ࡱࡪࡴࠨ਌"): get_host_info()
                          }
                      }
                      bstack1l11ll1ll_opy_ = bstack1l1l11ll1_opy_(cli.config, [bstack11ll11_opy_ (u"ࠦࡦࡶࡩࡴࠤ਍"), bstack11ll11_opy_ (u"ࠧ࡫ࡤࡴࡋࡱࡷࡹࡸࡵ࡮ࡧࡱࡸࡦࡺࡩࡰࡰࠥ਎"), bstack11ll11_opy_ (u"ࠨࡡࡱ࡫ࠥਏ")], bstack1l1lll1111_opy_) if cli.is_running() else bstack1l1lll1111_opy_
                      response = bstack1llll1ll_opy_(bstack11ll11_opy_ (u"ࠢࡑࡑࡖࡘࠧਐ"), bstack1l11ll1ll_opy_, payload, config)
                      if(response.status_code >= 200 and response.status_code < 300):
                          logger.debug(bstack11ll11_opy_ (u"ࠣࡆࡤࡸࡦࠦࡳࡦࡰࡷࠤࡸࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻࠣࡸࡴࠦࡻࡾࠢࡺ࡭ࡹ࡮ࠠࡥࡣࡷࡥࠥࢁࡽࠣ਑").format(bstack1l1lll1111_opy_, payload))
                      else:
                          logger.debug(bstack11ll11_opy_ (u"ࠤࡕࡩࡶࡻࡥࡴࡶࠣࡪࡦ࡯࡬ࡦࡦࠣࡪࡴࡸࠠࡼࡿࠣࡻ࡮ࡺࡨࠡࡦࡤࡸࡦࠦࡻࡾࠤ਒").format(bstack1l1lll1111_opy_, payload))
          except Exception as e:
              logger.debug(bstack11ll11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡰࡧࠤࡰ࡫ࡹࠡ࡯ࡨࡸࡷ࡯ࡣࡴࠢࡧࡥࡹࡧࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵࠤࢀࢃࠢਓ").format(e))
      bstack1l1l11lll1_opy_()
      bstack1ll11111l1_opy_(bstack1llll1ll1l_opy_, logger)
  except:
    pass
def bstack1ll11l1ll_opy_():
  global bstack1l1111ll11_opy_
  global bstack1l11ll1ll1_opy_
  global bstack11l11l1111_opy_
  global bstack1l1l1lll11_opy_
  global bstack11l1llll1_opy_
  global bstack11llll11l_opy_
  global CONFIG
  bstack11ll1l11l_opy_ = os.environ.get(bstack11ll11_opy_ (u"ࠫࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ࡟ࡖࡕࡈࡈࠬਔ"))
  if bstack11ll1l11l_opy_ in [bstack11ll11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫਕ"), bstack11ll11_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬਖ")]:
    bstack1l1l1111l_opy_()
  percy.shutdown()
  if bstack1l1111ll11_opy_:
    logger.warning(bstack111lllll1_opy_.format(str(bstack1l1111ll11_opy_)))
  else:
    try:
      bstack11l1l1l1l1_opy_ = bstack1l1l11111l_opy_(bstack11ll11_opy_ (u"ࠧ࠯ࡤࡶࡸࡦࡩ࡫࠮ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭ਗ"), logger)
      if bstack11l1l1l1l1_opy_.get(bstack11ll11_opy_ (u"ࠨࡰࡸࡨ࡬࡫࡟࡭ࡱࡦࡥࡱ࠭ਘ")) and bstack11l1l1l1l1_opy_.get(bstack11ll11_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧਙ")).get(bstack11ll11_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬਚ")):
        logger.warning(bstack111lllll1_opy_.format(str(bstack11l1l1l1l1_opy_[bstack11ll11_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩਛ")][bstack11ll11_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧਜ")])))
    except Exception as e:
      logger.error(e)
  if cli.is_running():
    bstack11111l11l_opy_.invoke(bstack11l11l1l_opy_.bstack1l11ll1l_opy_)
  logger.info(bstack111ll11l1_opy_)
  global bstack1ll11l1l1l_opy_
  if bstack1ll11l1l1l_opy_:
    bstack11lll11ll1_opy_()
  try:
    for driver in bstack1l11ll1ll1_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack11l1l1llll_opy_)
  if bstack11llll11l_opy_ == bstack11ll11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬਝ"):
    bstack11l1llll1_opy_ = bstack1l1ll1111_opy_(bstack11ll11_opy_ (u"ࠧࡳࡱࡥࡳࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨਞ"))
  if bstack11llll11l_opy_ == bstack11ll11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨਟ") and len(bstack1l1l1lll11_opy_) == 0:
    bstack1l1l1lll11_opy_ = bstack1l1ll1111_opy_(bstack11ll11_opy_ (u"ࠩࡳࡻࡤࡶࡹࡵࡧࡶࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧਠ"))
    if len(bstack1l1l1lll11_opy_) == 0:
      bstack1l1l1lll11_opy_ = bstack1l1ll1111_opy_(bstack11ll11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡴࡵࡶ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩਡ"))
  bstack1ll11llll1_opy_ = bstack11ll11_opy_ (u"ࠫࠬਢ")
  if len(bstack11l11l1111_opy_) > 0:
    bstack1ll11llll1_opy_ = bstack1l1l1llll1_opy_(bstack11l11l1111_opy_)
  elif len(bstack1l1l1lll11_opy_) > 0:
    bstack1ll11llll1_opy_ = bstack1l1l1llll1_opy_(bstack1l1l1lll11_opy_)
  elif len(bstack11l1llll1_opy_) > 0:
    bstack1ll11llll1_opy_ = bstack1l1l1llll1_opy_(bstack11l1llll1_opy_)
  elif len(bstack1ll1l1111_opy_) > 0:
    bstack1ll11llll1_opy_ = bstack1l1l1llll1_opy_(bstack1ll1l1111_opy_)
  if bool(bstack1ll11llll1_opy_):
    bstack11l1ll11l1_opy_(bstack1ll11llll1_opy_)
  else:
    bstack11l1ll11l1_opy_()
  bstack1ll11111l1_opy_(bstack111l11l11_opy_, logger)
  if bstack11ll1l11l_opy_ not in [bstack11ll11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ਣ")]:
    bstack1ll1l1111l_opy_()
  bstack1111l1ll1_opy_.bstack11ll1lllll_opy_(CONFIG)
  if len(bstack11l1llll1_opy_) > 0:
    sys.exit(len(bstack11l1llll1_opy_))
def bstack11llll1ll1_opy_(bstack11ll111111_opy_, frame):
  global bstack1l1ll1llll_opy_
  logger.error(bstack11l1lll111_opy_)
  bstack1l1ll1llll_opy_.bstack1l111lll11_opy_(bstack11ll11_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡎࡰࠩਤ"), bstack11ll111111_opy_)
  if hasattr(signal, bstack11ll11_opy_ (u"ࠧࡔ࡫ࡪࡲࡦࡲࡳࠨਥ")):
    bstack1l1ll1llll_opy_.bstack1l111lll11_opy_(bstack11ll11_opy_ (u"ࠨࡵࡧ࡯ࡐ࡯࡬࡭ࡕ࡬࡫ࡳࡧ࡬ࠨਦ"), signal.Signals(bstack11ll111111_opy_).name)
  else:
    bstack1l1ll1llll_opy_.bstack1l111lll11_opy_(bstack11ll11_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩਧ"), bstack11ll11_opy_ (u"ࠪࡗࡎࡍࡕࡏࡍࡑࡓ࡜ࡔࠧਨ"))
  if cli.is_running():
    bstack11111l11l_opy_.invoke(bstack11l11l1l_opy_.bstack1l11ll1l_opy_)
  bstack11ll1l11l_opy_ = os.environ.get(bstack11ll11_opy_ (u"ࠫࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ࡟ࡖࡕࡈࡈࠬ਩"))
  if bstack11ll1l11l_opy_ == bstack11ll11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬਪ") and not cli.is_enabled(CONFIG):
    bstack1l1l1l1ll_opy_.stop(bstack1l1ll1llll_opy_.get_property(bstack11ll11_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭ਫ")))
  bstack1ll11l1ll_opy_()
  sys.exit(1)
def bstack1ll11l111_opy_(err):
  logger.critical(bstack1lll11111l_opy_.format(str(err)))
  bstack11l1ll11l1_opy_(bstack1lll11111l_opy_.format(str(err)), True)
  atexit.unregister(bstack1ll11l1ll_opy_)
  bstack1l1l1111l_opy_()
  sys.exit(1)
def bstack1lll11l1l1_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack11l1ll11l1_opy_(message, True)
  atexit.unregister(bstack1ll11l1ll_opy_)
  bstack1l1l1111l_opy_()
  sys.exit(1)
def bstack1llll11ll1_opy_():
  global CONFIG
  global bstack1l111111ll_opy_
  global bstack1ll1llllll_opy_
  global bstack11ll11l1_opy_
  CONFIG = bstack1l1ll11111_opy_()
  load_dotenv(CONFIG.get(bstack11ll11_opy_ (u"ࠧࡦࡰࡹࡊ࡮ࡲࡥࠨਬ")))
  bstack1111l1l1_opy_()
  bstack11llll1l1_opy_()
  CONFIG = bstack1l1l1l1111_opy_(CONFIG)
  update(CONFIG, bstack1ll1llllll_opy_)
  update(CONFIG, bstack1l111111ll_opy_)
  if not cli.is_enabled(CONFIG):
    CONFIG = bstack11l1ll11ll_opy_(CONFIG)
  bstack11ll11l1_opy_ = bstack1l111lll1l_opy_(CONFIG)
  os.environ[bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫਭ")] = bstack11ll11l1_opy_.__str__().lower()
  bstack1l1ll1llll_opy_.bstack1l111lll11_opy_(bstack11ll11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪਮ"), bstack11ll11l1_opy_)
  if (bstack11ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ਯ") in CONFIG and bstack11ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧਰ") in bstack1l111111ll_opy_) or (
          bstack11ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ਱") in CONFIG and bstack11ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩਲ") not in bstack1ll1llllll_opy_):
    if os.getenv(bstack11ll11_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫਲ਼")):
      CONFIG[bstack11ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ਴")] = os.getenv(bstack11ll11_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ਵ"))
    else:
      if not CONFIG.get(bstack11ll11_opy_ (u"ࠥࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠨਸ਼"), bstack11ll11_opy_ (u"ࠦࠧ਷")) in bstack1ll111lll1_opy_:
        bstack1l1111l11l_opy_()
  elif (bstack11ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨਸ") not in CONFIG and bstack11ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨਹ") in CONFIG) or (
          bstack11ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ਺") in bstack1ll1llllll_opy_ and bstack11ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ਻") not in bstack1l111111ll_opy_):
    del (CONFIG[bstack11ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ਼ࠫ")])
  if bstack1111111ll_opy_(CONFIG):
    bstack1ll11l111_opy_(bstack1l11l1l1l_opy_)
  Config.bstack1lll11ll_opy_().bstack1l111lll11_opy_(bstack11ll11_opy_ (u"ࠥࡹࡸ࡫ࡲࡏࡣࡰࡩࠧ਽"), CONFIG[bstack11ll11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ਾ")])
  bstack1l11l111_opy_()
  bstack111l1l1l1_opy_()
  if bstack1ll1lllll1_opy_ and not CONFIG.get(bstack11ll11_opy_ (u"ࠧ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠣਿ"), bstack11ll11_opy_ (u"ࠨࠢੀ")) in bstack1ll111lll1_opy_:
    CONFIG[bstack11ll11_opy_ (u"ࠧࡢࡲࡳࠫੁ")] = bstack1llllll1l_opy_(CONFIG)
    logger.info(bstack1l111ll1l1_opy_.format(CONFIG[bstack11ll11_opy_ (u"ࠨࡣࡳࡴࠬੂ")]))
  if not bstack11ll11l1_opy_:
    CONFIG[bstack11ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ੃")] = [{}]
def bstack11l11l111l_opy_(config, bstack1lll1l111l_opy_):
  global CONFIG
  global bstack1ll1lllll1_opy_
  CONFIG = config
  bstack1ll1lllll1_opy_ = bstack1lll1l111l_opy_
def bstack111l1l1l1_opy_():
  global CONFIG
  global bstack1ll1lllll1_opy_
  if bstack11ll11_opy_ (u"ࠪࡥࡵࡶࠧ੄") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1lll11l1l1_opy_(e, bstack1ll1llll1l_opy_)
    bstack1ll1lllll1_opy_ = True
    bstack1l1ll1llll_opy_.bstack1l111lll11_opy_(bstack11ll11_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪ੅"), True)
def bstack1llllll1l_opy_(config):
  bstack11lll1l1l1_opy_ = bstack11ll11_opy_ (u"ࠬ࠭੆")
  app = config[bstack11ll11_opy_ (u"࠭ࡡࡱࡲࠪੇ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack11l111l111_opy_:
      if os.path.exists(app):
        bstack11lll1l1l1_opy_ = bstack11l111ll1l_opy_(config, app)
      elif bstack1l1lll111_opy_(app):
        bstack11lll1l1l1_opy_ = app
      else:
        bstack1ll11l111_opy_(bstack1llll11l11_opy_.format(app))
    else:
      if bstack1l1lll111_opy_(app):
        bstack11lll1l1l1_opy_ = app
      elif os.path.exists(app):
        bstack11lll1l1l1_opy_ = bstack11l111ll1l_opy_(app)
      else:
        bstack1ll11l111_opy_(bstack11lllll1l1_opy_)
  else:
    if len(app) > 2:
      bstack1ll11l111_opy_(bstack1l111ll11l_opy_)
    elif len(app) == 2:
      if bstack11ll11_opy_ (u"ࠧࡱࡣࡷ࡬ࠬੈ") in app and bstack11ll11_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫ੉") in app:
        if os.path.exists(app[bstack11ll11_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ੊")]):
          bstack11lll1l1l1_opy_ = bstack11l111ll1l_opy_(config, app[bstack11ll11_opy_ (u"ࠪࡴࡦࡺࡨࠨੋ")], app[bstack11ll11_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧੌ")])
        else:
          bstack1ll11l111_opy_(bstack1llll11l11_opy_.format(app))
      else:
        bstack1ll11l111_opy_(bstack1l111ll11l_opy_)
    else:
      for key in app:
        if key in bstack11l11ll11l_opy_:
          if key == bstack11ll11_opy_ (u"ࠬࡶࡡࡵࡪ੍ࠪ"):
            if os.path.exists(app[key]):
              bstack11lll1l1l1_opy_ = bstack11l111ll1l_opy_(config, app[key])
            else:
              bstack1ll11l111_opy_(bstack1llll11l11_opy_.format(app))
          else:
            bstack11lll1l1l1_opy_ = app[key]
        else:
          bstack1ll11l111_opy_(bstack1lll11l11l_opy_)
  return bstack11lll1l1l1_opy_
def bstack1l1lll111_opy_(bstack11lll1l1l1_opy_):
  import re
  bstack11l1l11l1_opy_ = re.compile(bstack11ll11_opy_ (u"ࡸࠢ࡟࡝ࡤ࠱ࡿࡇ࡛࠭࠲࠰࠽ࡡࡥ࠮࡝࠯ࡠ࠮ࠩࠨ੎"))
  bstack1llllllll1_opy_ = re.compile(bstack11ll11_opy_ (u"ࡲࠣࡠ࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯࠵࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬࠧࠦ੏"))
  if bstack11ll11_opy_ (u"ࠨࡤࡶ࠾࠴࠵ࠧ੐") in bstack11lll1l1l1_opy_ or re.fullmatch(bstack11l1l11l1_opy_, bstack11lll1l1l1_opy_) or re.fullmatch(bstack1llllllll1_opy_, bstack11lll1l1l1_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack1111l1l11_opy_, stage=STAGE.bstack1lll11llll_opy_, bstack1111llll_opy_=bstack11ll11lll_opy_)
def bstack11l111ll1l_opy_(config, path, bstack111llll1l_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack11ll11_opy_ (u"ࠩࡵࡦࠬੑ")).read()).hexdigest()
  bstack1ll11llll_opy_ = bstack1l1l11lll_opy_(md5_hash)
  bstack11lll1l1l1_opy_ = None
  if bstack1ll11llll_opy_:
    logger.info(bstack1lll11l111_opy_.format(bstack1ll11llll_opy_, md5_hash))
    return bstack1ll11llll_opy_
  bstack1ll1lll1ll_opy_ = datetime.datetime.now()
  bstack1l1l1llll_opy_ = MultipartEncoder(
    fields={
      bstack11ll11_opy_ (u"ࠪࡪ࡮ࡲࡥࠨ੒"): (os.path.basename(path), open(os.path.abspath(path), bstack11ll11_opy_ (u"ࠫࡷࡨࠧ੓")), bstack11ll11_opy_ (u"ࠬࡺࡥࡹࡶ࠲ࡴࡱࡧࡩ࡯ࠩ੔")),
      bstack11ll11_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩ੕"): bstack111llll1l_opy_
    }
  )
  response = requests.post(bstack11l11lll1l_opy_, data=bstack1l1l1llll_opy_,
                           headers={bstack11ll11_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭੖"): bstack1l1l1llll_opy_.content_type},
                           auth=(config[bstack11ll11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ੗")], config[bstack11ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ੘")]))
  try:
    res = json.loads(response.text)
    bstack11lll1l1l1_opy_ = res[bstack11ll11_opy_ (u"ࠪࡥࡵࡶ࡟ࡶࡴ࡯ࠫਖ਼")]
    logger.info(bstack1l11111ll_opy_.format(bstack11lll1l1l1_opy_))
    bstack1l1ll1lll_opy_(md5_hash, bstack11lll1l1l1_opy_)
    cli.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼ࡸࡴࡱࡵࡡࡥࡡࡤࡴࡵࠨਗ਼"), datetime.datetime.now() - bstack1ll1lll1ll_opy_)
  except ValueError as err:
    bstack1ll11l111_opy_(bstack1lllll111_opy_.format(str(err)))
  return bstack11lll1l1l1_opy_
def bstack1l11l111_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack1l111llll_opy_
  bstack11lllll1_opy_ = 1
  bstack1llll11l1_opy_ = 1
  if bstack11ll11_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬਜ਼") in CONFIG:
    bstack1llll11l1_opy_ = CONFIG[bstack11ll11_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ੜ")]
  else:
    bstack1llll11l1_opy_ = bstack1l1l1111ll_opy_(framework_name, args) or 1
  if bstack11ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ੝") in CONFIG:
    bstack11lllll1_opy_ = len(CONFIG[bstack11ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫਫ਼")])
  bstack1l111llll_opy_ = int(bstack1llll11l1_opy_) * int(bstack11lllll1_opy_)
def bstack1l1l1111ll_opy_(framework_name, args):
  if framework_name == bstack1llllll11l_opy_ and args and bstack11ll11_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ੟") in args:
      bstack1ll1ll1l11_opy_ = args.index(bstack11ll11_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨ੠"))
      return int(args[bstack1ll1ll1l11_opy_ + 1]) or 1
  return 1
def bstack1l1l11lll_opy_(md5_hash):
  bstack1111l11l1_opy_ = os.path.join(os.path.expanduser(bstack11ll11_opy_ (u"ࠫࢃ࠭੡")), bstack11ll11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ੢"), bstack11ll11_opy_ (u"࠭ࡡࡱࡲࡘࡴࡱࡵࡡࡥࡏࡇ࠹ࡍࡧࡳࡩ࠰࡭ࡷࡴࡴࠧ੣"))
  if os.path.exists(bstack1111l11l1_opy_):
    bstack111lll1l1_opy_ = json.load(open(bstack1111l11l1_opy_, bstack11ll11_opy_ (u"ࠧࡳࡤࠪ੤")))
    if md5_hash in bstack111lll1l1_opy_:
      bstack1l11111l1l_opy_ = bstack111lll1l1_opy_[md5_hash]
      bstack1l1llllll1_opy_ = datetime.datetime.now()
      bstack1llll1l111_opy_ = datetime.datetime.strptime(bstack1l11111l1l_opy_[bstack11ll11_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ੥")], bstack11ll11_opy_ (u"ࠩࠨࡨ࠴ࠫ࡭࠰ࠧ࡜ࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭੦"))
      if (bstack1l1llllll1_opy_ - bstack1llll1l111_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1l11111l1l_opy_[bstack11ll11_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ੧")]):
        return None
      return bstack1l11111l1l_opy_[bstack11ll11_opy_ (u"ࠫ࡮ࡪࠧ੨")]
  else:
    return None
def bstack1l1ll1lll_opy_(md5_hash, bstack11lll1l1l1_opy_):
  bstack1l11l111l1_opy_ = os.path.join(os.path.expanduser(bstack11ll11_opy_ (u"ࠬࢄࠧ੩")), bstack11ll11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭੪"))
  if not os.path.exists(bstack1l11l111l1_opy_):
    os.makedirs(bstack1l11l111l1_opy_)
  bstack1111l11l1_opy_ = os.path.join(os.path.expanduser(bstack11ll11_opy_ (u"ࠧࡿࠩ੫")), bstack11ll11_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ੬"), bstack11ll11_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪ੭"))
  bstack1llllllll_opy_ = {
    bstack11ll11_opy_ (u"ࠪ࡭ࡩ࠭੮"): bstack11lll1l1l1_opy_,
    bstack11ll11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ੯"): datetime.datetime.strftime(datetime.datetime.now(), bstack11ll11_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩੰ")),
    bstack11ll11_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫੱ"): str(__version__)
  }
  if os.path.exists(bstack1111l11l1_opy_):
    bstack111lll1l1_opy_ = json.load(open(bstack1111l11l1_opy_, bstack11ll11_opy_ (u"ࠧࡳࡤࠪੲ")))
  else:
    bstack111lll1l1_opy_ = {}
  bstack111lll1l1_opy_[md5_hash] = bstack1llllllll_opy_
  with open(bstack1111l11l1_opy_, bstack11ll11_opy_ (u"ࠣࡹ࠮ࠦੳ")) as outfile:
    json.dump(bstack111lll1l1_opy_, outfile)
def bstack11111l111_opy_(self):
  return
def bstack11lllll1ll_opy_(self):
  return
def bstack111lllll_opy_():
  global bstack11111111_opy_
  bstack11111111_opy_ = True
@measure(event_name=EVENTS.bstack1l11lll1_opy_, stage=STAGE.bstack1lll11llll_opy_, bstack1111llll_opy_=bstack11ll11lll_opy_)
def bstack1l1l1111_opy_(self):
  global bstack1lll11l1ll_opy_
  global bstack11ll1111l1_opy_
  global bstack11llll1l_opy_
  try:
    if bstack11ll11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩੴ") in bstack1lll11l1ll_opy_ and self.session_id != None and bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧੵ"), bstack11ll11_opy_ (u"ࠫࠬ੶")) != bstack11ll11_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭੷"):
      bstack1l1l111l1l_opy_ = bstack11ll11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭੸") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11ll11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ੹")
      if bstack1l1l111l1l_opy_ == bstack11ll11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ੺"):
        bstack1lll1l1l1_opy_(logger)
      if self != None:
        bstack11l1l1l11l_opy_(self, bstack1l1l111l1l_opy_, bstack11ll11_opy_ (u"ࠩ࠯ࠤࠬ੻").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack11ll11_opy_ (u"ࠪࠫ੼")
    if bstack11ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ੽") in bstack1lll11l1ll_opy_ and getattr(threading.current_thread(), bstack11ll11_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ੾"), None):
      bstack1l111l1l_opy_.bstack1l1l1ll11l_opy_(self, bstack1lll1ll1ll_opy_, logger, wait=True)
    if bstack11ll11_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭੿") in bstack1lll11l1ll_opy_:
      if not threading.currentThread().behave_test_status:
        bstack11l1l1l11l_opy_(self, bstack11ll11_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ઀"))
      bstack1lll1111l1_opy_.bstack1111l1111_opy_(self)
  except Exception as e:
    logger.debug(bstack11ll11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࠤઁ") + str(e))
  bstack11llll1l_opy_(self)
  self.session_id = None
def bstack11l1ll1l1_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack111111lll_opy_
    global bstack1lll11l1ll_opy_
    command_executor = kwargs.get(bstack11ll11_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠬં"), bstack11ll11_opy_ (u"ࠪࠫઃ"))
    bstack1llll1l1ll_opy_ = False
    if type(command_executor) == str and bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧ઄") in command_executor:
      bstack1llll1l1ll_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨઅ") in str(getattr(command_executor, bstack11ll11_opy_ (u"࠭࡟ࡶࡴ࡯ࠫઆ"), bstack11ll11_opy_ (u"ࠧࠨઇ"))):
      bstack1llll1l1ll_opy_ = True
    else:
      kwargs = bstack11l11lll11_opy_.bstack11l1l111l_opy_(bstack11l11111l1_opy_=kwargs, config=CONFIG)
      return bstack1l1llll1_opy_(self, *args, **kwargs)
    if bstack1llll1l1ll_opy_:
      bstack1l11111111_opy_ = bstack1l1ll1lll1_opy_.bstack1ll1l1l11l_opy_(CONFIG, bstack1lll11l1ll_opy_)
      if kwargs.get(bstack11ll11_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩઈ")):
        kwargs[bstack11ll11_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪઉ")] = bstack111111lll_opy_(kwargs[bstack11ll11_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫઊ")], bstack1lll11l1ll_opy_, CONFIG, bstack1l11111111_opy_)
      elif kwargs.get(bstack11ll11_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫઋ")):
        kwargs[bstack11ll11_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬઌ")] = bstack111111lll_opy_(kwargs[bstack11ll11_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ઍ")], bstack1lll11l1ll_opy_, CONFIG, bstack1l11111111_opy_)
  except Exception as e:
    logger.error(bstack11ll11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩࡧࡱࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡕࡇࡏࠥࡩࡡࡱࡵ࠽ࠤࢀࢃࠢ઎").format(str(e)))
  return bstack1l1llll1_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack11lll111l1_opy_, stage=STAGE.bstack1lll11llll_opy_, bstack1111llll_opy_=bstack11ll11lll_opy_)
def bstack1ll111ll1l_opy_(self, command_executor=bstack11ll11_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰࠳࠵࠻࠳࠶࠮࠱࠰࠴࠾࠹࠺࠴࠵ࠤએ"), *args, **kwargs):
  global bstack11ll1111l1_opy_
  global bstack1l11ll1ll1_opy_
  bstack1l11l1ll_opy_ = bstack11l1ll1l1_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack11l1ll11_opy_.on():
    return bstack1l11l1ll_opy_
  try:
    logger.debug(bstack11ll11_opy_ (u"ࠩࡆࡳࡲࡳࡡ࡯ࡦࠣࡉࡽ࡫ࡣࡶࡶࡲࡶࠥࡽࡨࡦࡰࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡩࡴࠢࡩࡥࡱࡹࡥࠡ࠯ࠣࡿࢂ࠭ઐ").format(str(command_executor)))
    logger.debug(bstack11ll11_opy_ (u"ࠪࡌࡺࡨࠠࡖࡔࡏࠤ࡮ࡹࠠ࠮ࠢࡾࢁࠬઑ").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧ઒") in command_executor._url:
      bstack1l1ll1llll_opy_.bstack1l111lll11_opy_(bstack11ll11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ઓ"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩઔ") in command_executor):
    bstack1l1ll1llll_opy_.bstack1l111lll11_opy_(bstack11ll11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨક"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1lll1lll_opy_ = getattr(threading.current_thread(), bstack11ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡕࡧࡶࡸࡒ࡫ࡴࡢࠩખ"), None)
  bstack1l1lllll_opy_ = {}
  if self.capabilities is not None:
    bstack1l1lllll_opy_[bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡲࡦࡳࡥࠨગ")] = self.capabilities.get(bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨઘ"))
    bstack1l1lllll_opy_[bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ઙ")] = self.capabilities.get(bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ચ"))
    bstack1l1lllll_opy_[bstack11ll11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡥ࡯ࡱࡶ࡬ࡳࡳࡹࠧછ")] = self.capabilities.get(bstack11ll11_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬજ"))
  if CONFIG.get(bstack11ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨઝ"), False) and bstack11l11lll11_opy_.bstack1l1l111l1_opy_(bstack1l1lllll_opy_):
    threading.current_thread().a11yPlatform = True
  if bstack11ll11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩઞ") in bstack1lll11l1ll_opy_ or bstack11ll11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩટ") in bstack1lll11l1ll_opy_:
    bstack1l1l1l1ll_opy_.bstack1l1l111ll_opy_(self)
  if bstack11ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫઠ") in bstack1lll11l1ll_opy_ and bstack1lll1lll_opy_ and bstack1lll1lll_opy_.get(bstack11ll11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬડ"), bstack11ll11_opy_ (u"࠭ࠧઢ")) == bstack11ll11_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨણ"):
    bstack1l1l1l1ll_opy_.bstack1l1l111ll_opy_(self)
  bstack11ll1111l1_opy_ = self.session_id
  bstack1l11ll1ll1_opy_.append(self)
  return bstack1l11l1ll_opy_
def bstack1l111l11ll_opy_(args):
  return bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠩત") in str(args)
def bstack11ll111l11_opy_(self, driver_command, *args, **kwargs):
  global bstack1ll11ll11_opy_
  global bstack11l1ll1l11_opy_
  bstack11111111l_opy_ = bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭થ"), None) and bstack111ll1lll_opy_(
          threading.current_thread(), bstack11ll11_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩદ"), None)
  bstack1l1l1l1l11_opy_ = bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫધ"), None) and bstack111ll1lll_opy_(
          threading.current_thread(), bstack11ll11_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧન"), None)
  bstack1l11l1lll_opy_ = getattr(self, bstack11ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭઩"), None) != None and getattr(self, bstack11ll11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧપ"), None) == True
  if not bstack11l1ll1l11_opy_ and bstack11ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨફ") in CONFIG and CONFIG[bstack11ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩબ")] == True and bstack11llll1l1l_opy_.bstack1l1ll1l11l_opy_(driver_command) and (bstack1l11l1lll_opy_ or bstack11111111l_opy_) and not bstack1l111l11ll_opy_(args):
    try:
      bstack11l1ll1l11_opy_ = True
      logger.debug(bstack11ll11_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡾࢁࠬભ").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack11ll11_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡧࡵࡪࡴࡸ࡭ࠡࡵࡦࡥࡳࠦࡻࡾࠩમ").format(str(err)))
    bstack11l1ll1l11_opy_ = False
  response = bstack1ll11ll11_opy_(self, driver_command, *args, **kwargs)
  if (bstack11ll11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫય") in str(bstack1lll11l1ll_opy_).lower() or bstack11ll11_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ર") in str(bstack1lll11l1ll_opy_).lower()) and bstack11l1ll11_opy_.on():
    try:
      if driver_command == bstack11ll11_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫ઱"):
        bstack1l1l1l1ll_opy_.bstack111lll11l_opy_({
            bstack11ll11_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧલ"): response[bstack11ll11_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨળ")],
            bstack11ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ઴"): bstack1l1l1l1ll_opy_.current_test_uuid() if bstack1l1l1l1ll_opy_.current_test_uuid() else bstack11l1ll11_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
@measure(event_name=EVENTS.bstack1llll1l11l_opy_, stage=STAGE.bstack1lll11llll_opy_, bstack1111llll_opy_=bstack11ll11lll_opy_)
def bstack1ll11ll11l_opy_(self, command_executor,
             desired_capabilities=None, bstack1l1l11ll11_opy_=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack11ll1111l1_opy_
  global bstack11llllllll_opy_
  global bstack11ll11lll_opy_
  global bstack111lll1ll_opy_
  global bstack11l111ll1_opy_
  global bstack1lll11l1ll_opy_
  global bstack1l1llll1_opy_
  global bstack1l11ll1ll1_opy_
  global bstack1ll1l111l1_opy_
  global bstack1lll1ll1ll_opy_
  CONFIG[bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭વ")] = str(bstack1lll11l1ll_opy_) + str(__version__)
  bstack1ll11l11ll_opy_ = os.environ[bstack11ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪશ")]
  bstack1l11111111_opy_ = bstack1l1ll1lll1_opy_.bstack1ll1l1l11l_opy_(CONFIG, bstack1lll11l1ll_opy_)
  CONFIG[bstack11ll11_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩષ")] = bstack1ll11l11ll_opy_
  CONFIG[bstack11ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩસ")] = bstack1l11111111_opy_
  if CONFIG.get(bstack11ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨહ"),bstack11ll11_opy_ (u"ࠩࠪ઺")) and bstack11ll11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ઻") in bstack1lll11l1ll_opy_:
    CONFIG[bstack11ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶ઼ࠫ")].pop(bstack11ll11_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪઽ"), None)
    CONFIG[bstack11ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ા")].pop(bstack11ll11_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬિ"), None)
  command_executor = bstack11ll11l111_opy_()
  logger.debug(bstack11ll11ll11_opy_.format(command_executor))
  proxy = bstack11l1l1111_opy_(CONFIG, proxy)
  bstack1l111l111l_opy_ = 0 if bstack11llllllll_opy_ < 0 else bstack11llllllll_opy_
  try:
    if bstack111lll1ll_opy_ is True:
      bstack1l111l111l_opy_ = int(multiprocessing.current_process().name)
    elif bstack11l111ll1_opy_ is True:
      bstack1l111l111l_opy_ = int(threading.current_thread().name)
  except:
    bstack1l111l111l_opy_ = 0
  bstack1lll1ll11_opy_ = bstack1l11l11l1_opy_(CONFIG, bstack1l111l111l_opy_)
  logger.debug(bstack11llll1111_opy_.format(str(bstack1lll1ll11_opy_)))
  if bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬી") in CONFIG and bstack1l111ll1l_opy_(CONFIG[bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ુ")]):
    bstack1lll1lllll_opy_(bstack1lll1ll11_opy_)
  if bstack11l11lll11_opy_.bstack11lll11l1l_opy_(CONFIG, bstack1l111l111l_opy_) and bstack11l11lll11_opy_.bstack1ll1ll111_opy_(bstack1lll1ll11_opy_, options, desired_capabilities, CONFIG):
    threading.current_thread().a11yPlatform = True
    if (cli.accessibility is None or not cli.accessibility.is_enabled()):
      bstack11l11lll11_opy_.set_capabilities(bstack1lll1ll11_opy_, CONFIG)
  if desired_capabilities:
    bstack11lllll111_opy_ = bstack1l1l1l1111_opy_(desired_capabilities)
    bstack11lllll111_opy_[bstack11ll11_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪૂ")] = bstack1llll11l1l_opy_(CONFIG)
    bstack1l11llll1l_opy_ = bstack1l11l11l1_opy_(bstack11lllll111_opy_)
    if bstack1l11llll1l_opy_:
      bstack1lll1ll11_opy_ = update(bstack1l11llll1l_opy_, bstack1lll1ll11_opy_)
    desired_capabilities = None
  if options:
    bstack1ll1l1l11_opy_(options, bstack1lll1ll11_opy_)
  if not options:
    options = bstack1ll11111l_opy_(bstack1lll1ll11_opy_)
  bstack1lll1ll1ll_opy_ = CONFIG.get(bstack11ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧૃ"))[bstack1l111l111l_opy_]
  if proxy and bstack1lll1ll1_opy_() >= version.parse(bstack11ll11_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬૄ")):
    options.proxy(proxy)
  if options and bstack1lll1ll1_opy_() >= version.parse(bstack11ll11_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬૅ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1lll1ll1_opy_() < version.parse(bstack11ll11_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭૆")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1lll1ll11_opy_)
  logger.info(bstack1l11ll1l1l_opy_)
  bstack1ll11ll1_opy_.end(EVENTS.bstack1l11llllll_opy_.value, EVENTS.bstack1l11llllll_opy_.value + bstack11ll11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣે"), EVENTS.bstack1l11llllll_opy_.value + bstack11ll11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢૈ"), status=True, failure=None, test_name=bstack11ll11lll_opy_)
  if bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡵࡸ࡯ࡧ࡫࡯ࡩࠬૉ") in kwargs:
    del kwargs[bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡶࡲࡰࡨ࡬ࡰࡪ࠭૊")]
  if bstack1lll1ll1_opy_() >= version.parse(bstack11ll11_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬો")):
    bstack1l1llll1_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
  elif bstack1lll1ll1_opy_() >= version.parse(bstack11ll11_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬૌ")):
    bstack1l1llll1_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              bstack1l1l11ll11_opy_=bstack1l1l11ll11_opy_, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1lll1ll1_opy_() >= version.parse(bstack11ll11_opy_ (u"ࠧ࠳࠰࠸࠷࠳࠶્ࠧ")):
    bstack1l1llll1_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              bstack1l1l11ll11_opy_=bstack1l1l11ll11_opy_, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1l1llll1_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              bstack1l1l11ll11_opy_=bstack1l1l11ll11_opy_, proxy=proxy,
              keep_alive=keep_alive)
  if bstack11l11lll11_opy_.bstack11lll11l1l_opy_(CONFIG, bstack1l111l111l_opy_) and bstack11l11lll11_opy_.bstack1ll1ll111_opy_(self.caps, options, desired_capabilities):
    if CONFIG[bstack11ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ૎")][bstack11ll11_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨ૏")] == True:
      threading.current_thread().appA11yPlatform = True
      if cli.accessibility is None or not cli.accessibility.is_enabled():
        bstack11l11lll11_opy_.set_capabilities(bstack1lll1ll11_opy_, CONFIG)
  try:
    bstack111l1l11l_opy_ = bstack11ll11_opy_ (u"ࠪࠫૐ")
    if bstack1lll1ll1_opy_() >= version.parse(bstack11ll11_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࡥ࠵ࠬ૑")):
      if self.caps is not None:
        bstack111l1l11l_opy_ = self.caps.get(bstack11ll11_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧ૒"))
    else:
      if self.capabilities is not None:
        bstack111l1l11l_opy_ = self.capabilities.get(bstack11ll11_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨ૓"))
    if bstack111l1l11l_opy_:
      bstack1lll111lll_opy_(bstack111l1l11l_opy_)
      if bstack1lll1ll1_opy_() <= version.parse(bstack11ll11_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧ૔")):
        self.command_executor._url = bstack11ll11_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ૕") + bstack11lll111ll_opy_ + bstack11ll11_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨ૖")
      else:
        self.command_executor._url = bstack11ll11_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ૗") + bstack111l1l11l_opy_ + bstack11ll11_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧ૘")
      logger.debug(bstack11ll11lll1_opy_.format(bstack111l1l11l_opy_))
    else:
      logger.debug(bstack111l1ll11_opy_.format(bstack11ll11_opy_ (u"ࠧࡕࡰࡵ࡫ࡰࡥࡱࠦࡈࡶࡤࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨ૙")))
  except Exception as e:
    logger.debug(bstack111l1ll11_opy_.format(e))
  if bstack11ll11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ૚") in bstack1lll11l1ll_opy_:
    bstack11lll1llll_opy_(bstack11llllllll_opy_, bstack1ll1l111l1_opy_)
  bstack11ll1111l1_opy_ = self.session_id
  if bstack11ll11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ૛") in bstack1lll11l1ll_opy_ or bstack11ll11_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ૜") in bstack1lll11l1ll_opy_ or bstack11ll11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ૝") in bstack1lll11l1ll_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack1lll1lll_opy_ = getattr(threading.current_thread(), bstack11ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡗࡩࡸࡺࡍࡦࡶࡤࠫ૞"), None)
  if bstack11ll11_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ૟") in bstack1lll11l1ll_opy_ or bstack11ll11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫૠ") in bstack1lll11l1ll_opy_:
    bstack1l1l1l1ll_opy_.bstack1l1l111ll_opy_(self)
  if bstack11ll11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ૡ") in bstack1lll11l1ll_opy_ and bstack1lll1lll_opy_ and bstack1lll1lll_opy_.get(bstack11ll11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧૢ"), bstack11ll11_opy_ (u"ࠨࠩૣ")) == bstack11ll11_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ૤"):
    bstack1l1l1l1ll_opy_.bstack1l1l111ll_opy_(self)
  bstack1l11ll1ll1_opy_.append(self)
  if bstack11ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭૥") in CONFIG and bstack11ll11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ૦") in CONFIG[bstack11ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ૧")][bstack1l111l111l_opy_]:
    bstack11ll11lll_opy_ = CONFIG[bstack11ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ૨")][bstack1l111l111l_opy_][bstack11ll11_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ૩")]
  logger.debug(bstack11llll1l11_opy_.format(bstack11ll1111l1_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    from browserstack_sdk.__init__ import bstack11lll1l11_opy_
    def bstack1l11ll111_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1ll111ll11_opy_
      if(bstack11ll11_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࠮࡫ࡵࠥ૪") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack11ll11_opy_ (u"ࠩࢁࠫ૫")), bstack11ll11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ૬"), bstack11ll11_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭૭")), bstack11ll11_opy_ (u"ࠬࡽࠧ૮")) as fp:
          fp.write(bstack11ll11_opy_ (u"ࠨࠢ૯"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack11ll11_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤ૰")))):
          with open(args[1], bstack11ll11_opy_ (u"ࠨࡴࠪ૱")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack11ll11_opy_ (u"ࠩࡤࡷࡾࡴࡣࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡣࡳ࡫ࡷࡑࡣࡪࡩ࠭ࡩ࡯࡯ࡶࡨࡼࡹ࠲ࠠࡱࡣࡪࡩࠥࡃࠠࡷࡱ࡬ࡨࠥ࠶ࠩࠨ૲") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1111l111_opy_)
            if bstack11ll11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ૳") in CONFIG and str(CONFIG[bstack11ll11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ૴")]).lower() != bstack11ll11_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ૵"):
                bstack1lll1l11l1_opy_ = bstack11lll1l11_opy_()
                bstack11lll11lll_opy_ = bstack11ll11_opy_ (u"࠭ࠧࠨࠌ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࠏࡩ࡯࡯ࡵࡷࠤࡧࡹࡴࡢࡥ࡮ࡣࡵࡧࡴࡩࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸ࡣ࠻ࠋࡥࡲࡲࡸࡺࠠࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠲࡟࠾ࠎࡨࡵ࡮ࡴࡶࠣࡴࡤ࡯࡮ࡥࡧࡻࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠲࡞࠽ࠍࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡷࡱ࡯ࡣࡦࠪ࠳࠰ࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳ࠪ࠽ࠍࡧࡴࡴࡳࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣࠫ࠾ࠎ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡱࡧࡵ࡯ࡥ࡫ࠤࡂࠦࡡࡴࡻࡱࡧࠥ࠮࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸ࠯ࠠ࠾ࡀࠣࡿࢀࠐࠠࠡ࡮ࡨࡸࠥࡩࡡࡱࡵ࠾ࠎࠥࠦࡴࡳࡻࠣࡿࢀࠐࠠࠡࠢࠣࡧࡦࡶࡳࠡ࠿ࠣࡎࡘࡕࡎ࠯ࡲࡤࡶࡸ࡫ࠨࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷ࠮ࡁࠊࠡࠢࢀࢁࠥࡩࡡࡵࡥ࡫ࠤ࠭࡫ࡸࠪࠢࡾࡿࠏࠦࠠࠡࠢࡦࡳࡳࡹ࡯࡭ࡧ࠱ࡩࡷࡸ࡯ࡳࠪࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ࠾ࠧ࠲ࠠࡦࡺࠬ࠿ࠏࠦࠠࡾࡿࠍࠤࠥࡸࡥࡵࡷࡵࡲࠥࡧࡷࡢ࡫ࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡨࡵ࡮࡯ࡧࡦࡸ࠭ࢁࡻࠋࠢࠣࠤࠥࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵ࠼ࠣࠫࢀࡩࡤࡱࡗࡵࡰࢂ࠭ࠠࠬࠢࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩ࠭ࠌࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴࠌࠣࠤࢂࢃࠩ࠼ࠌࢀࢁࡀࠐ࠯ࠫࠢࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࠦࠪ࠰ࠌࠪࠫࠬ૶").format(bstack1lll1l11l1_opy_=bstack1lll1l11l1_opy_)
            lines.insert(1, bstack11lll11lll_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack11ll11_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤ૷")), bstack11ll11_opy_ (u"ࠨࡹࠪ૸")) as bstack1l11ll1111_opy_:
              bstack1l11ll1111_opy_.writelines(lines)
        CONFIG[bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫૹ")] = str(bstack1lll11l1ll_opy_) + str(__version__)
        bstack1ll11l11ll_opy_ = os.environ[bstack11ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨૺ")]
        bstack1l11111111_opy_ = bstack1l1ll1lll1_opy_.bstack1ll1l1l11l_opy_(CONFIG, bstack1lll11l1ll_opy_)
        CONFIG[bstack11ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧૻ")] = bstack1ll11l11ll_opy_
        CONFIG[bstack11ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧૼ")] = bstack1l11111111_opy_
        bstack1l111l111l_opy_ = 0 if bstack11llllllll_opy_ < 0 else bstack11llllllll_opy_
        try:
          if bstack111lll1ll_opy_ is True:
            bstack1l111l111l_opy_ = int(multiprocessing.current_process().name)
          elif bstack11l111ll1_opy_ is True:
            bstack1l111l111l_opy_ = int(threading.current_thread().name)
        except:
          bstack1l111l111l_opy_ = 0
        CONFIG[bstack11ll11_opy_ (u"ࠨࡵࡴࡧ࡚࠷ࡈࠨ૽")] = False
        CONFIG[bstack11ll11_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ૾")] = True
        bstack1lll1ll11_opy_ = bstack1l11l11l1_opy_(CONFIG, bstack1l111l111l_opy_)
        logger.debug(bstack11llll1111_opy_.format(str(bstack1lll1ll11_opy_)))
        if CONFIG.get(bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ૿")):
          bstack1lll1lllll_opy_(bstack1lll1ll11_opy_)
        if bstack11ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ଀") in CONFIG and bstack11ll11_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨଁ") in CONFIG[bstack11ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଂ")][bstack1l111l111l_opy_]:
          bstack11ll11lll_opy_ = CONFIG[bstack11ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨଃ")][bstack1l111l111l_opy_][bstack11ll11_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ଄")]
        args.append(os.path.join(os.path.expanduser(bstack11ll11_opy_ (u"ࠧࡿࠩଅ")), bstack11ll11_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨଆ"), bstack11ll11_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫଇ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1lll1ll11_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack11ll11_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧଈ"))
      bstack1ll111ll11_opy_ = True
      return bstack1l1l1ll111_opy_(self, args, bufsize=bufsize, executable=executable,
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
  def bstack1l1ll1l1ll_opy_(self,
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
    global bstack11llllllll_opy_
    global bstack11ll11lll_opy_
    global bstack111lll1ll_opy_
    global bstack11l111ll1_opy_
    global bstack1lll11l1ll_opy_
    CONFIG[bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ଉ")] = str(bstack1lll11l1ll_opy_) + str(__version__)
    bstack1ll11l11ll_opy_ = os.environ[bstack11ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪଊ")]
    bstack1l11111111_opy_ = bstack1l1ll1lll1_opy_.bstack1ll1l1l11l_opy_(CONFIG, bstack1lll11l1ll_opy_)
    CONFIG[bstack11ll11_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩଋ")] = bstack1ll11l11ll_opy_
    CONFIG[bstack11ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩଌ")] = bstack1l11111111_opy_
    bstack1l111l111l_opy_ = 0 if bstack11llllllll_opy_ < 0 else bstack11llllllll_opy_
    try:
      if bstack111lll1ll_opy_ is True:
        bstack1l111l111l_opy_ = int(multiprocessing.current_process().name)
      elif bstack11l111ll1_opy_ is True:
        bstack1l111l111l_opy_ = int(threading.current_thread().name)
    except:
      bstack1l111l111l_opy_ = 0
    CONFIG[bstack11ll11_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢ଍")] = True
    bstack1lll1ll11_opy_ = bstack1l11l11l1_opy_(CONFIG, bstack1l111l111l_opy_)
    logger.debug(bstack11llll1111_opy_.format(str(bstack1lll1ll11_opy_)))
    if CONFIG.get(bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭଎")):
      bstack1lll1lllll_opy_(bstack1lll1ll11_opy_)
    if bstack11ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ଏ") in CONFIG and bstack11ll11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩଐ") in CONFIG[bstack11ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ଑")][bstack1l111l111l_opy_]:
      bstack11ll11lll_opy_ = CONFIG[bstack11ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ଒")][bstack1l111l111l_opy_][bstack11ll11_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬଓ")]
    import urllib
    import json
    if bstack11ll11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬଔ") in CONFIG and str(CONFIG[bstack11ll11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭କ")]).lower() != bstack11ll11_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩଖ"):
        bstack1l1111l1l_opy_ = bstack11lll1l11_opy_()
        bstack1lll1l11l1_opy_ = bstack1l1111l1l_opy_ + urllib.parse.quote(json.dumps(bstack1lll1ll11_opy_))
    else:
        bstack1lll1l11l1_opy_ = bstack11ll11_opy_ (u"ࠫࡼࡹࡳ࠻࠱࠲ࡧࡩࡶ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠿ࡤࡣࡳࡷࡂ࠭ଗ") + urllib.parse.quote(json.dumps(bstack1lll1ll11_opy_))
    browser = self.connect(bstack1lll1l11l1_opy_)
    return browser
except Exception as e:
    pass
def bstack11ll111l_opy_():
    global bstack1ll111ll11_opy_
    global bstack1lll11l1ll_opy_
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l1lllll1_opy_
        global bstack1l1ll1llll_opy_
        if not bstack11ll11l1_opy_:
          global bstack1ll11ll1l1_opy_
          if not bstack1ll11ll1l1_opy_:
            from bstack_utils.helper import bstack1ll1111l_opy_, bstack1l111ll1ll_opy_, bstack111l1ll1l_opy_
            bstack1ll11ll1l1_opy_ = bstack1ll1111l_opy_()
            bstack1l111ll1ll_opy_(bstack1lll11l1ll_opy_)
            bstack1l11111111_opy_ = bstack1l1ll1lll1_opy_.bstack1ll1l1l11l_opy_(CONFIG, bstack1lll11l1ll_opy_)
            bstack1l1ll1llll_opy_.bstack1l111lll11_opy_(bstack11ll11_opy_ (u"ࠧࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡓࡖࡔࡊࡕࡄࡖࡢࡑࡆࡖࠢଘ"), bstack1l11111111_opy_)
          BrowserType.connect = bstack1l1lllll1_opy_
          return
        BrowserType.launch = bstack1l1ll1l1ll_opy_
        bstack1ll111ll11_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1l11ll111_opy_
      bstack1ll111ll11_opy_ = True
    except Exception as e:
      pass
def bstack1111ll1l_opy_(context, bstack11l1l1ll11_opy_):
  try:
    context.page.evaluate(bstack11ll11_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢଙ"), bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫଚ")+ json.dumps(bstack11l1l1ll11_opy_) + bstack11ll11_opy_ (u"ࠣࡿࢀࠦଛ"))
  except Exception as e:
    logger.debug(bstack11ll11_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃ࠺ࠡࡽࢀࠦଜ").format(str(e), traceback.format_exc()))
def bstack1l11l111l_opy_(context, message, level):
  try:
    context.page.evaluate(bstack11ll11_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦଝ"), bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩଞ") + json.dumps(message) + bstack11ll11_opy_ (u"ࠬ࠲ࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠨଟ") + json.dumps(level) + bstack11ll11_opy_ (u"࠭ࡽࡾࠩଠ"))
  except Exception as e:
    logger.debug(bstack11ll11_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠࡼࡿ࠽ࠤࢀࢃࠢଡ").format(str(e), traceback.format_exc()))
@measure(event_name=EVENTS.bstack111llll1_opy_, stage=STAGE.bstack1lll11llll_opy_, bstack1111llll_opy_=bstack11ll11lll_opy_)
def bstack111111l11_opy_(self, url):
  global bstack11lllllll_opy_
  try:
    bstack1l1lll11ll_opy_(url)
  except Exception as err:
    logger.debug(bstack1ll1l11l11_opy_.format(str(err)))
  try:
    bstack11lllllll_opy_(self, url)
  except Exception as e:
    try:
      bstack1ll1l1ll1_opy_ = str(e)
      if any(err_msg in bstack1ll1l1ll1_opy_ for err_msg in bstack1ll1ll11ll_opy_):
        bstack1l1lll11ll_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1ll1l11l11_opy_.format(str(err)))
    raise e
def bstack11l11ll1l_opy_(self):
  global bstack1lll111l1_opy_
  bstack1lll111l1_opy_ = self
  return
def bstack1lll111ll1_opy_(self):
  global bstack1lllll1lll_opy_
  bstack1lllll1lll_opy_ = self
  return
def bstack1l11111ll1_opy_(test_name, bstack1l1111111l_opy_):
  global CONFIG
  if percy.bstack11ll1ll1l_opy_() == bstack11ll11_opy_ (u"ࠣࡶࡵࡹࡪࠨଢ"):
    bstack11l11l111_opy_ = os.path.relpath(bstack1l1111111l_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack11l11l111_opy_)
    bstack1111llll_opy_ = suite_name + bstack11ll11_opy_ (u"ࠤ࠰ࠦଣ") + test_name
    threading.current_thread().percySessionName = bstack1111llll_opy_
def bstack1lllll11_opy_(self, test, *args, **kwargs):
  global bstack11l1ll1111_opy_
  test_name = None
  bstack1l1111111l_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1l1111111l_opy_ = str(test.source)
  bstack1l11111ll1_opy_(test_name, bstack1l1111111l_opy_)
  bstack11l1ll1111_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.bstack1l1lll1ll1_opy_, stage=STAGE.bstack1lll11llll_opy_, bstack1111llll_opy_=bstack11ll11lll_opy_)
def bstack1l11l1l1_opy_(driver, bstack1111llll_opy_):
  if not bstack1llllll1ll_opy_ and bstack1111llll_opy_:
      bstack1l11l1111_opy_ = {
          bstack11ll11_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪତ"): bstack11ll11_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬଥ"),
          bstack11ll11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨଦ"): {
              bstack11ll11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫଧ"): bstack1111llll_opy_
          }
      }
      bstack1l1ll11ll_opy_ = bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬନ").format(json.dumps(bstack1l11l1111_opy_))
      driver.execute_script(bstack1l1ll11ll_opy_)
  if bstack111ll1l11_opy_:
      bstack1ll111l1_opy_ = {
          bstack11ll11_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨ଩"): bstack11ll11_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫପ"),
          bstack11ll11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ଫ"): {
              bstack11ll11_opy_ (u"ࠫࡩࡧࡴࡢࠩବ"): bstack1111llll_opy_ + bstack11ll11_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧଭ"),
              bstack11ll11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬମ"): bstack11ll11_opy_ (u"ࠧࡪࡰࡩࡳࠬଯ")
          }
      }
      if bstack111ll1l11_opy_.status == bstack11ll11_opy_ (u"ࠨࡒࡄࡗࡘ࠭ର"):
          bstack1l111l11_opy_ = bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧ଱").format(json.dumps(bstack1ll111l1_opy_))
          driver.execute_script(bstack1l111l11_opy_)
          bstack11l1l1l11l_opy_(driver, bstack11ll11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪଲ"))
      elif bstack111ll1l11_opy_.status == bstack11ll11_opy_ (u"ࠫࡋࡇࡉࡍࠩଳ"):
          reason = bstack11ll11_opy_ (u"ࠧࠨ଴")
          bstack1ll111l1l1_opy_ = bstack1111llll_opy_ + bstack11ll11_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠧଵ")
          if bstack111ll1l11_opy_.message:
              reason = str(bstack111ll1l11_opy_.message)
              bstack1ll111l1l1_opy_ = bstack1ll111l1l1_opy_ + bstack11ll11_opy_ (u"ࠧࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶ࠿ࠦࠧଶ") + reason
          bstack1ll111l1_opy_[bstack11ll11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫଷ")] = {
              bstack11ll11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨସ"): bstack11ll11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩହ"),
              bstack11ll11_opy_ (u"ࠫࡩࡧࡴࡢࠩ଺"): bstack1ll111l1l1_opy_
          }
          bstack1l111l11_opy_ = bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪ଻").format(json.dumps(bstack1ll111l1_opy_))
          driver.execute_script(bstack1l111l11_opy_)
          bstack11l1l1l11l_opy_(driver, bstack11ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ଼࠭"), reason)
          bstack1lll1l111_opy_(reason, str(bstack111ll1l11_opy_), str(bstack11llllllll_opy_), logger)
@measure(event_name=EVENTS.bstack11l11llll_opy_, stage=STAGE.bstack1lll11llll_opy_, bstack1111llll_opy_=bstack11ll11lll_opy_)
def bstack11ll111ll1_opy_(driver, test):
  if percy.bstack11ll1ll1l_opy_() == bstack11ll11_opy_ (u"ࠢࡵࡴࡸࡩࠧଽ") and percy.bstack1l1l11l1_opy_() == bstack11ll11_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥା"):
      bstack1ll1ll1ll1_opy_ = bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠩࡳࡩࡷࡩࡹࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬି"), None)
      bstack11111llll_opy_(driver, bstack1ll1ll1ll1_opy_, test)
  if (bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧୀ"), None) and
      bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪୁ"), None)) or (
      bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠬ࡯ࡳࡂࡲࡳࡅ࠶࠷ࡹࡕࡧࡶࡸࠬୂ"), None) and
      bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨୃ"), None)):
      logger.info(bstack11ll11_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠥࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡪࡵࠣࡹࡳࡪࡥࡳࡹࡤࡽ࠳ࠦࠢୄ"))
      bstack11l11lll11_opy_.bstack1ll1l1l111_opy_(driver, name=test.name, path=test.source)
def bstack1ll111l1l_opy_(test, bstack1111llll_opy_):
    try:
      bstack1ll1lll1ll_opy_ = datetime.datetime.now()
      data = {}
      if test:
        data[bstack11ll11_opy_ (u"ࠨࡰࡤࡱࡪ࠭୅")] = bstack1111llll_opy_
      if bstack111ll1l11_opy_:
        if bstack111ll1l11_opy_.status == bstack11ll11_opy_ (u"ࠩࡓࡅࡘ࡙ࠧ୆"):
          data[bstack11ll11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪେ")] = bstack11ll11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫୈ")
        elif bstack111ll1l11_opy_.status == bstack11ll11_opy_ (u"ࠬࡌࡁࡊࡎࠪ୉"):
          data[bstack11ll11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭୊")] = bstack11ll11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧୋ")
          if bstack111ll1l11_opy_.message:
            data[bstack11ll11_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨୌ")] = str(bstack111ll1l11_opy_.message)
      user = CONFIG[bstack11ll11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨ୍ࠫ")]
      key = CONFIG[bstack11ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭୎")]
      host = bstack1l1l11ll1_opy_(cli.config, [bstack11ll11_opy_ (u"ࠦࡦࡶࡩࡴࠤ୏"), bstack11ll11_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫ࠢ୐"), bstack11ll11_opy_ (u"ࠨࡡࡱ࡫ࠥ୑")], bstack11ll11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠣ୒"))
      url = bstack11ll11_opy_ (u"ࠨࡽࢀ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡳࡦࡵࡶ࡭ࡴࡴࡳ࠰ࡽࢀ࠲࡯ࡹ࡯࡯ࠩ୓").format(host, bstack11ll1111l1_opy_)
      headers = {
        bstack11ll11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨ୔"): bstack11ll11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭୕"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers, auth=(user, key))
        cli.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼ࡸࡴࡩࡧࡴࡦࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡵࡷࡥࡹࡻࡳࠣୖ"), datetime.datetime.now() - bstack1ll1lll1ll_opy_)
    except Exception as e:
      logger.error(bstack1l11l111ll_opy_.format(str(e)))
def bstack1l1111lll1_opy_(test, bstack1111llll_opy_):
  global CONFIG
  global bstack1lllll1lll_opy_
  global bstack1lll111l1_opy_
  global bstack11ll1111l1_opy_
  global bstack111ll1l11_opy_
  global bstack11ll11lll_opy_
  global bstack1111lll1l_opy_
  global bstack11l1ll1l1l_opy_
  global bstack1ll11l11l1_opy_
  global bstack1l11l1llll_opy_
  global bstack1l11ll1ll1_opy_
  global bstack1lll1ll1ll_opy_
  try:
    if not bstack11ll1111l1_opy_:
      with open(os.path.join(os.path.expanduser(bstack11ll11_opy_ (u"ࠬࢄࠧୗ")), bstack11ll11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭୘"), bstack11ll11_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩ୙"))) as f:
        bstack1ll1l11ll_opy_ = json.loads(bstack11ll11_opy_ (u"ࠣࡽࠥ୚") + f.read().strip() + bstack11ll11_opy_ (u"ࠩࠥࡼࠧࡀࠠࠣࡻࠥࠫ୛") + bstack11ll11_opy_ (u"ࠥࢁࠧଡ଼"))
        bstack11ll1111l1_opy_ = bstack1ll1l11ll_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1l11ll1ll1_opy_:
    for driver in bstack1l11ll1ll1_opy_:
      if bstack11ll1111l1_opy_ == driver.session_id:
        if test:
          bstack11ll111ll1_opy_(driver, test)
        bstack1l11l1l1_opy_(driver, bstack1111llll_opy_)
  elif bstack11ll1111l1_opy_:
    bstack1ll111l1l_opy_(test, bstack1111llll_opy_)
  if bstack1lllll1lll_opy_:
    bstack11l1ll1l1l_opy_(bstack1lllll1lll_opy_)
  if bstack1lll111l1_opy_:
    bstack1ll11l11l1_opy_(bstack1lll111l1_opy_)
  if bstack11111111_opy_:
    bstack1l11l1llll_opy_()
def bstack1l11l1l1ll_opy_(self, test, *args, **kwargs):
  bstack1111llll_opy_ = None
  if test:
    bstack1111llll_opy_ = str(test.name)
  bstack1l1111lll1_opy_(test, bstack1111llll_opy_)
  bstack1111lll1l_opy_(self, test, *args, **kwargs)
def bstack1l1l1l1l_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1ll1l1lll1_opy_
  global CONFIG
  global bstack1l11ll1ll1_opy_
  global bstack11ll1111l1_opy_
  bstack1l1lll1lll_opy_ = None
  try:
    if bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪଢ଼"), None) or bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ୞"), None):
      try:
        if not bstack11ll1111l1_opy_:
          with open(os.path.join(os.path.expanduser(bstack11ll11_opy_ (u"࠭ࡾࠨୟ")), bstack11ll11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧୠ"), bstack11ll11_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪୡ"))) as f:
            bstack1ll1l11ll_opy_ = json.loads(bstack11ll11_opy_ (u"ࠤࡾࠦୢ") + f.read().strip() + bstack11ll11_opy_ (u"ࠪࠦࡽࠨ࠺ࠡࠤࡼࠦࠬୣ") + bstack11ll11_opy_ (u"ࠦࢂࠨ୤"))
            bstack11ll1111l1_opy_ = bstack1ll1l11ll_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack1l11ll1ll1_opy_:
        for driver in bstack1l11ll1ll1_opy_:
          if bstack11ll1111l1_opy_ == driver.session_id:
            bstack1l1lll1lll_opy_ = driver
    bstack1ll1l11l1l_opy_ = bstack11l11lll11_opy_.bstack1ll1lllll_opy_(test.tags)
    if bstack1l1lll1lll_opy_:
      threading.current_thread().isA11yTest = bstack11l11lll11_opy_.bstack1l1111l1l1_opy_(bstack1l1lll1lll_opy_, bstack1ll1l11l1l_opy_)
      threading.current_thread().isAppA11yTest = bstack11l11lll11_opy_.bstack1l1111l1l1_opy_(bstack1l1lll1lll_opy_, bstack1ll1l11l1l_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1ll1l11l1l_opy_
      threading.current_thread().isAppA11yTest = bstack1ll1l11l1l_opy_
  except:
    pass
  bstack1ll1l1lll1_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack111ll1l11_opy_
  try:
    bstack111ll1l11_opy_ = self._test
  except:
    bstack111ll1l11_opy_ = self.test
def bstack1llll1lll_opy_():
  global bstack11ll1l11l1_opy_
  try:
    if os.path.exists(bstack11ll1l11l1_opy_):
      os.remove(bstack11ll1l11l1_opy_)
  except Exception as e:
    logger.debug(bstack11ll11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨ୥") + str(e))
def bstack111ll1111_opy_():
  global bstack11ll1l11l1_opy_
  bstack11l1l1l1l1_opy_ = {}
  try:
    if not os.path.isfile(bstack11ll1l11l1_opy_):
      with open(bstack11ll1l11l1_opy_, bstack11ll11_opy_ (u"࠭ࡷࠨ୦")):
        pass
      with open(bstack11ll1l11l1_opy_, bstack11ll11_opy_ (u"ࠢࡸ࠭ࠥ୧")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack11ll1l11l1_opy_):
      bstack11l1l1l1l1_opy_ = json.load(open(bstack11ll1l11l1_opy_, bstack11ll11_opy_ (u"ࠨࡴࡥࠫ୨")))
  except Exception as e:
    logger.debug(bstack11ll11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡷ࡫ࡡࡥ࡫ࡱ࡫ࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫ୩") + str(e))
  finally:
    return bstack11l1l1l1l1_opy_
def bstack11lll1llll_opy_(platform_index, item_index):
  global bstack11ll1l11l1_opy_
  try:
    bstack11l1l1l1l1_opy_ = bstack111ll1111_opy_()
    bstack11l1l1l1l1_opy_[item_index] = platform_index
    with open(bstack11ll1l11l1_opy_, bstack11ll11_opy_ (u"ࠥࡻ࠰ࠨ୪")) as outfile:
      json.dump(bstack11l1l1l1l1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack11ll11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡷࡳ࡫ࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺ࠡࠩ୫") + str(e))
def bstack1lllll11l_opy_(bstack1l11lllll_opy_):
  global CONFIG
  bstack1l111l1l11_opy_ = bstack11ll11_opy_ (u"ࠬ࠭୬")
  if not bstack11ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ୭") in CONFIG:
    logger.info(bstack11ll11_opy_ (u"ࠧࡏࡱࠣࡴࡱࡧࡴࡧࡱࡵࡱࡸࠦࡰࡢࡵࡶࡩࡩࠦࡵ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡪࡩࡳ࡫ࡲࡢࡶࡨࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫ࡵࡲࠡࡔࡲࡦࡴࡺࠠࡳࡷࡱࠫ୮"))
  try:
    platform = CONFIG[bstack11ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ୯")][bstack1l11lllll_opy_]
    if bstack11ll11_opy_ (u"ࠩࡲࡷࠬ୰") in platform:
      bstack1l111l1l11_opy_ += str(platform[bstack11ll11_opy_ (u"ࠪࡳࡸ࠭ୱ")]) + bstack11ll11_opy_ (u"ࠫ࠱ࠦࠧ୲")
    if bstack11ll11_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨ୳") in platform:
      bstack1l111l1l11_opy_ += str(platform[bstack11ll11_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ୴")]) + bstack11ll11_opy_ (u"ࠧ࠭ࠢࠪ୵")
    if bstack11ll11_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬ୶") in platform:
      bstack1l111l1l11_opy_ += str(platform[bstack11ll11_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭୷")]) + bstack11ll11_opy_ (u"ࠪ࠰ࠥ࠭୸")
    if bstack11ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭୹") in platform:
      bstack1l111l1l11_opy_ += str(platform[bstack11ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ୺")]) + bstack11ll11_opy_ (u"࠭ࠬࠡࠩ୻")
    if bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ୼") in platform:
      bstack1l111l1l11_opy_ += str(platform[bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭୽")]) + bstack11ll11_opy_ (u"ࠩ࠯ࠤࠬ୾")
    if bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ୿") in platform:
      bstack1l111l1l11_opy_ += str(platform[bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ஀")]) + bstack11ll11_opy_ (u"ࠬ࠲ࠠࠨ஁")
  except Exception as e:
    logger.debug(bstack11ll11_opy_ (u"࠭ࡓࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡰࡨࡶࡦࡺࡩ࡯ࡩࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡹࡴࡳ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡵࡩࡵࡵࡲࡵࠢࡪࡩࡳ࡫ࡲࡢࡶ࡬ࡳࡳ࠭ஂ") + str(e))
  finally:
    if bstack1l111l1l11_opy_[len(bstack1l111l1l11_opy_) - 2:] == bstack11ll11_opy_ (u"ࠧ࠭ࠢࠪஃ"):
      bstack1l111l1l11_opy_ = bstack1l111l1l11_opy_[:-2]
    return bstack1l111l1l11_opy_
def bstack1ll1l11lll_opy_(path, bstack1l111l1l11_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack11llll11ll_opy_ = ET.parse(path)
    bstack11ll11llll_opy_ = bstack11llll11ll_opy_.getroot()
    bstack1llll11lll_opy_ = None
    for suite in bstack11ll11llll_opy_.iter(bstack11ll11_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧ஄")):
      if bstack11ll11_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩஅ") in suite.attrib:
        suite.attrib[bstack11ll11_opy_ (u"ࠪࡲࡦࡳࡥࠨஆ")] += bstack11ll11_opy_ (u"ࠫࠥ࠭இ") + bstack1l111l1l11_opy_
        bstack1llll11lll_opy_ = suite
    bstack1l1ll11l11_opy_ = None
    for robot in bstack11ll11llll_opy_.iter(bstack11ll11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫஈ")):
      bstack1l1ll11l11_opy_ = robot
    bstack1ll1l1ll_opy_ = len(bstack1l1ll11l11_opy_.findall(bstack11ll11_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬஉ")))
    if bstack1ll1l1ll_opy_ == 1:
      bstack1l1ll11l11_opy_.remove(bstack1l1ll11l11_opy_.findall(bstack11ll11_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭ஊ"))[0])
      bstack1111lll1_opy_ = ET.Element(bstack11ll11_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧ஋"), attrib={bstack11ll11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ஌"): bstack11ll11_opy_ (u"ࠪࡗࡺ࡯ࡴࡦࡵࠪ஍"), bstack11ll11_opy_ (u"ࠫ࡮ࡪࠧஎ"): bstack11ll11_opy_ (u"ࠬࡹ࠰ࠨஏ")})
      bstack1l1ll11l11_opy_.insert(1, bstack1111lll1_opy_)
      bstack1l11l11l1l_opy_ = None
      for suite in bstack1l1ll11l11_opy_.iter(bstack11ll11_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬஐ")):
        bstack1l11l11l1l_opy_ = suite
      bstack1l11l11l1l_opy_.append(bstack1llll11lll_opy_)
      bstack1lll11ll1l_opy_ = None
      for status in bstack1llll11lll_opy_.iter(bstack11ll11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ஑")):
        bstack1lll11ll1l_opy_ = status
      bstack1l11l11l1l_opy_.append(bstack1lll11ll1l_opy_)
    bstack11llll11ll_opy_.write(path)
  except Exception as e:
    logger.debug(bstack11ll11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡦࡸࡳࡪࡰࡪࠤࡼ࡮ࡩ࡭ࡧࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹ࠭ஒ") + str(e))
def bstack11lll1111_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1l1111l11_opy_
  global CONFIG
  if bstack11ll11_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡲࡤࡸ࡭ࠨஓ") in options:
    del options[bstack11ll11_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࡳࡥࡹ࡮ࠢஔ")]
  bstack1l1l11l1ll_opy_ = bstack111ll1111_opy_()
  for bstack1111l11l_opy_ in bstack1l1l11l1ll_opy_.keys():
    path = os.path.join(os.getcwd(), bstack11ll11_opy_ (u"ࠫࡵࡧࡢࡰࡶࡢࡶࡪࡹࡵ࡭ࡶࡶࠫக"), str(bstack1111l11l_opy_), bstack11ll11_opy_ (u"ࠬࡵࡵࡵࡲࡸࡸ࠳ࡾ࡭࡭ࠩ஖"))
    bstack1ll1l11lll_opy_(path, bstack1lllll11l_opy_(bstack1l1l11l1ll_opy_[bstack1111l11l_opy_]))
  bstack1llll1lll_opy_()
  return bstack1l1111l11_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack11l1l11111_opy_(self, ff_profile_dir):
  global bstack111ll1l1_opy_
  if not ff_profile_dir:
    return None
  return bstack111ll1l1_opy_(self, ff_profile_dir)
def bstack11ll1ll111_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack11llllll11_opy_
  bstack11ll11l1l_opy_ = []
  if bstack11ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ஗") in CONFIG:
    bstack11ll11l1l_opy_ = CONFIG[bstack11ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ஘")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack11ll11_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤங")],
      pabot_args[bstack11ll11_opy_ (u"ࠤࡹࡩࡷࡨ࡯ࡴࡧࠥச")],
      argfile,
      pabot_args.get(bstack11ll11_opy_ (u"ࠥ࡬࡮ࡼࡥࠣ஛")),
      pabot_args[bstack11ll11_opy_ (u"ࠦࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠢஜ")],
      platform[0],
      bstack11llllll11_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack11ll11_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡦࡪ࡮ࡨࡷࠧ஝")] or [(bstack11ll11_opy_ (u"ࠨࠢஞ"), None)]
    for platform in enumerate(bstack11ll11l1l_opy_)
  ]
def bstack1lll1ll1l1_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1llll11111_opy_=bstack11ll11_opy_ (u"ࠧࠨட")):
  global bstack11l1l1ll1l_opy_
  self.platform_index = platform_index
  self.bstack11ll11111_opy_ = bstack1llll11111_opy_
  bstack11l1l1ll1l_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack11l1ll1ll_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack11l11l1l1l_opy_
  global bstack11l1111l11_opy_
  bstack1l1llllll_opy_ = copy.deepcopy(item)
  if not bstack11ll11_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ஠") in item.options:
    bstack1l1llllll_opy_.options[bstack11ll11_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ஡")] = []
  bstack1llll111ll_opy_ = bstack1l1llllll_opy_.options[bstack11ll11_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ஢")].copy()
  for v in bstack1l1llllll_opy_.options[bstack11ll11_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ண")]:
    if bstack11ll11_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡕࡒࡁࡕࡈࡒࡖࡒࡏࡎࡅࡇ࡛ࠫத") in v:
      bstack1llll111ll_opy_.remove(v)
    if bstack11ll11_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘ࠭஥") in v:
      bstack1llll111ll_opy_.remove(v)
    if bstack11ll11_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡄࡆࡈࡏࡓࡈࡇࡌࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ஦") in v:
      bstack1llll111ll_opy_.remove(v)
  bstack1llll111ll_opy_.insert(0, bstack11ll11_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡑࡎࡄࡘࡋࡕࡒࡎࡋࡑࡈࡊ࡞࠺ࡼࡿࠪ஧").format(bstack1l1llllll_opy_.platform_index))
  bstack1llll111ll_opy_.insert(0, bstack11ll11_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡆࡈࡊࡑࡕࡃࡂࡎࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗࡀࡻࡾࠩந").format(bstack1l1llllll_opy_.bstack11ll11111_opy_))
  bstack1l1llllll_opy_.options[bstack11ll11_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬன")] = bstack1llll111ll_opy_
  if bstack11l1111l11_opy_:
    bstack1l1llllll_opy_.options[bstack11ll11_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ப")].insert(0, bstack11ll11_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡒࡉࡂࡔࡊࡗ࠿ࢁࡽࠨ஫").format(bstack11l1111l11_opy_))
  return bstack11l11l1l1l_opy_(caller_id, datasources, is_last, bstack1l1llllll_opy_, outs_dir)
def bstack1l1lllll1l_opy_(command, item_index):
  if bstack1l1ll1llll_opy_.get_property(bstack11ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ஬")):
    os.environ[bstack11ll11_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨ஭")] = json.dumps(CONFIG[bstack11ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫம")][item_index % bstack111l1l111_opy_])
  global bstack11l1111l11_opy_
  if bstack11l1111l11_opy_:
    command[0] = command[0].replace(bstack11ll11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨய"), bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡶࡨࡰࠦࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠠ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽࠦࠧர") + str(
      item_index) + bstack11ll11_opy_ (u"ࠫࠥ࠭ற") + bstack11l1111l11_opy_, 1)
  else:
    command[0] = command[0].replace(bstack11ll11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫல"),
                                    bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡹࡤ࡬ࠢࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠣ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠢࠪள") + str(item_index), 1)
def bstack11ll1l1l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack11ll1111_opy_
  bstack1l1lllll1l_opy_(command, item_index)
  return bstack11ll1111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1ll1l111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack11ll1111_opy_
  bstack1l1lllll1l_opy_(command, item_index)
  return bstack11ll1111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack11ll111l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack11ll1111_opy_
  bstack1l1lllll1l_opy_(command, item_index)
  return bstack11ll1111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack11l11ll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack11ll1111_opy_
  bstack1l1lllll1l_opy_(command, item_index)
  return bstack11ll1111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack1l1lllll11_opy_(self, runner, quiet=False, capture=True):
  global bstack11lll1l1l_opy_
  bstack11l11lll_opy_ = bstack11lll1l1l_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack11ll11_opy_ (u"ࠧࡦࡺࡦࡩࡵࡺࡩࡰࡰࡢࡥࡷࡸࠧழ")):
      runner.exception_arr = []
    if not hasattr(runner, bstack11ll11_opy_ (u"ࠨࡧࡻࡧࡤࡺࡲࡢࡥࡨࡦࡦࡩ࡫ࡠࡣࡵࡶࠬவ")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack11l11lll_opy_
def bstack11ll11ll1l_opy_(runner, hook_name, context, element, bstack11l11111l_opy_, *args):
  try:
    if runner.hooks.get(hook_name):
      bstack1ll1ll1111_opy_.bstack1ll11111_opy_(hook_name, element)
    bstack11l11111l_opy_(runner, hook_name, context, *args)
    if runner.hooks.get(hook_name):
      bstack1ll1ll1111_opy_.bstack1l1lll1l_opy_(element)
      if hook_name not in [bstack11ll11_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱ࠭ஶ"), bstack11ll11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ࠭ஷ")] and args and hasattr(args[0], bstack11ll11_opy_ (u"ࠫࡪࡸࡲࡰࡴࡢࡱࡪࡹࡳࡢࡩࡨࠫஸ")):
        args[0].error_message = bstack11ll11_opy_ (u"ࠬ࠭ஹ")
  except Exception as e:
    logger.debug(bstack11ll11_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢ࡫ࡥࡳࡪ࡬ࡦࠢ࡫ࡳࡴࡱࡳࠡ࡫ࡱࠤࡧ࡫ࡨࡢࡸࡨ࠾ࠥࢁࡽࠨ஺").format(str(e)))
@measure(event_name=EVENTS.bstack1l11l1lll1_opy_, stage=STAGE.bstack1lll11llll_opy_, hook_type=bstack11ll11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࡁ࡭࡮ࠥ஻"), bstack1111llll_opy_=bstack11ll11lll_opy_)
def bstack11lll1ll_opy_(runner, name, context, bstack11l11111l_opy_, *args):
    if runner.hooks.get(bstack11ll11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧ஼")).__name__ != bstack11ll11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࡥࡤࡦࡨࡤࡹࡱࡺ࡟ࡩࡱࡲ࡯ࠧ஽"):
      bstack11ll11ll1l_opy_(runner, name, context, runner, bstack11l11111l_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack1l11ll1lll_opy_(bstack11ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩா")) else context.browser
      runner.driver_initialised = bstack11ll11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣி")
    except Exception as e:
      logger.debug(bstack11ll11_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡪࡲࡪࡸࡨࡶࠥ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡳࡦࠢࡤࡸࡹࡸࡩࡣࡷࡷࡩ࠿ࠦࡻࡾࠩீ").format(str(e)))
def bstack1lllllllll_opy_(runner, name, context, bstack11l11111l_opy_, *args):
    bstack11ll11ll1l_opy_(runner, name, context, context.feature, bstack11l11111l_opy_, *args)
    try:
      if not bstack1llllll1ll_opy_:
        bstack1l1lll1lll_opy_ = threading.current_thread().bstackSessionDriver if bstack1l11ll1lll_opy_(bstack11ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬு")) else context.browser
        if is_driver_active(bstack1l1lll1lll_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack11ll11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣூ")
          bstack11l1l1ll11_opy_ = str(runner.feature.name)
          bstack1111ll1l_opy_(context, bstack11l1l1ll11_opy_)
          bstack1l1lll1lll_opy_.execute_script(bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭௃") + json.dumps(bstack11l1l1ll11_opy_) + bstack11ll11_opy_ (u"ࠩࢀࢁࠬ௄"))
    except Exception as e:
      logger.debug(bstack11ll11_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡬ࡥࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪ௅").format(str(e)))
def bstack111l111l_opy_(runner, name, context, bstack11l11111l_opy_, *args):
    if hasattr(context, bstack11ll11_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ெ")):
        bstack1ll1ll1111_opy_.start_test(context)
    target = context.scenario if hasattr(context, bstack11ll11_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧே")) else context.feature
    bstack11ll11ll1l_opy_(runner, name, context, target, bstack11l11111l_opy_, *args)
@measure(event_name=EVENTS.bstack11lll11l1_opy_, stage=STAGE.bstack1lll11llll_opy_, bstack1111llll_opy_=bstack11ll11lll_opy_)
def bstack1l1llll11_opy_(runner, name, context, bstack11l11111l_opy_, *args):
    if len(context.scenario.tags) == 0: bstack1ll1ll1111_opy_.start_test(context)
    bstack11ll11ll1l_opy_(runner, name, context, context.scenario, bstack11l11111l_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack1lll1111l1_opy_.bstack1l1l1l1lll_opy_(context, *args)
    try:
      bstack1l1lll1lll_opy_ = bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬை"), context.browser)
      if is_driver_active(bstack1l1lll1lll_opy_):
        bstack1l1l1l1ll_opy_.bstack1l1l111ll_opy_(bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭௉"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack11ll11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥொ")
        if (not bstack1llllll1ll_opy_):
          scenario_name = args[0].name
          feature_name = bstack11l1l1ll11_opy_ = str(runner.feature.name)
          bstack11l1l1ll11_opy_ = feature_name + bstack11ll11_opy_ (u"ࠩࠣ࠱ࠥ࠭ோ") + scenario_name
          if runner.driver_initialised == bstack11ll11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧௌ"):
            bstack1111ll1l_opy_(context, bstack11l1l1ll11_opy_)
            bstack1l1lll1lll_opy_.execute_script(bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺்ࠡࠩ") + json.dumps(bstack11l1l1ll11_opy_) + bstack11ll11_opy_ (u"ࠬࢃࡽࠨ௎"))
    except Exception as e:
      logger.debug(bstack11ll11_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱ࠽ࠤࢀࢃࠧ௏").format(str(e)))
@measure(event_name=EVENTS.bstack1l11l1lll1_opy_, stage=STAGE.bstack1lll11llll_opy_, hook_type=bstack11ll11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࡓࡵࡧࡳࠦௐ"), bstack1111llll_opy_=bstack11ll11lll_opy_)
def bstack11l1lll1l_opy_(runner, name, context, bstack11l11111l_opy_, *args):
    bstack11ll11ll1l_opy_(runner, name, context, args[0], bstack11l11111l_opy_, *args)
    try:
      bstack1l1lll1lll_opy_ = threading.current_thread().bstackSessionDriver if bstack1l11ll1lll_opy_(bstack11ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ௑")) else context.browser
      if is_driver_active(bstack1l1lll1lll_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack11ll11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢ௒")
        bstack1ll1ll1111_opy_.bstack11l1llll11_opy_(args[0])
        if runner.driver_initialised == bstack11ll11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣ௓"):
          feature_name = bstack11l1l1ll11_opy_ = str(runner.feature.name)
          bstack11l1l1ll11_opy_ = feature_name + bstack11ll11_opy_ (u"ࠫࠥ࠳ࠠࠨ௔") + context.scenario.name
          bstack1l1lll1lll_opy_.execute_script(bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ௕") + json.dumps(bstack11l1l1ll11_opy_) + bstack11ll11_opy_ (u"࠭ࡽࡾࠩ௖"))
    except Exception as e:
      logger.debug(bstack11ll11_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡸࡪࡶ࠺ࠡࡽࢀࠫௗ").format(str(e)))
@measure(event_name=EVENTS.bstack1l11l1lll1_opy_, stage=STAGE.bstack1lll11llll_opy_, hook_type=bstack11ll11_opy_ (u"ࠣࡣࡩࡸࡪࡸࡓࡵࡧࡳࠦ௘"), bstack1111llll_opy_=bstack11ll11lll_opy_)
def bstack1111ll11_opy_(runner, name, context, bstack11l11111l_opy_, *args):
  bstack1ll1ll1111_opy_.bstack1lll11lll_opy_(args[0])
  try:
    bstack1l11l1l1l1_opy_ = args[0].status.name
    bstack1l1lll1lll_opy_ = threading.current_thread().bstackSessionDriver if bstack11ll11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ௙") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack1l1lll1lll_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack11ll11_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪ௚")
        feature_name = bstack11l1l1ll11_opy_ = str(runner.feature.name)
        bstack11l1l1ll11_opy_ = feature_name + bstack11ll11_opy_ (u"ࠫࠥ࠳ࠠࠨ௛") + context.scenario.name
        bstack1l1lll1lll_opy_.execute_script(bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ௜") + json.dumps(bstack11l1l1ll11_opy_) + bstack11ll11_opy_ (u"࠭ࡽࡾࠩ௝"))
    if str(bstack1l11l1l1l1_opy_).lower() == bstack11ll11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ௞"):
      bstack1lll11l11_opy_ = bstack11ll11_opy_ (u"ࠨࠩ௟")
      bstack1l111lll_opy_ = bstack11ll11_opy_ (u"ࠩࠪ௠")
      bstack11l11l11ll_opy_ = bstack11ll11_opy_ (u"ࠪࠫ௡")
      try:
        import traceback
        bstack1lll11l11_opy_ = runner.exception.__class__.__name__
        bstack1ll1ll11l_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1l111lll_opy_ = bstack11ll11_opy_ (u"ࠫࠥ࠭௢").join(bstack1ll1ll11l_opy_)
        bstack11l11l11ll_opy_ = bstack1ll1ll11l_opy_[-1]
      except Exception as e:
        logger.debug(bstack1lllllll1_opy_.format(str(e)))
      bstack1lll11l11_opy_ += bstack11l11l11ll_opy_
      bstack1l11l111l_opy_(context, json.dumps(str(args[0].name) + bstack11ll11_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦ௣") + str(bstack1l111lll_opy_)),
                          bstack11ll11_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ௤"))
      if runner.driver_initialised == bstack11ll11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧ௥"):
        bstack11lll1l11l_opy_(getattr(context, bstack11ll11_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭௦"), None), bstack11ll11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ௧"), bstack1lll11l11_opy_)
        bstack1l1lll1lll_opy_.execute_script(bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨ௨") + json.dumps(str(args[0].name) + bstack11ll11_opy_ (u"ࠦࠥ࠳ࠠࡇࡣ࡬ࡰࡪࡪࠡ࡝ࡰࠥ௩") + str(bstack1l111lll_opy_)) + bstack11ll11_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥࡩࡷࡸ࡯ࡳࠤࢀࢁࠬ௪"))
      if runner.driver_initialised == bstack11ll11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦ௫"):
        bstack11l1l1l11l_opy_(bstack1l1lll1lll_opy_, bstack11ll11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ௬"), bstack11ll11_opy_ (u"ࠣࡕࡦࡩࡳࡧࡲࡪࡱࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧ௭") + str(bstack1lll11l11_opy_))
    else:
      bstack1l11l111l_opy_(context, bstack11ll11_opy_ (u"ࠤࡓࡥࡸࡹࡥࡥࠣࠥ௮"), bstack11ll11_opy_ (u"ࠥ࡭ࡳ࡬࡯ࠣ௯"))
      if runner.driver_initialised == bstack11ll11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤ௰"):
        bstack11lll1l11l_opy_(getattr(context, bstack11ll11_opy_ (u"ࠬࡶࡡࡨࡧࠪ௱"), None), bstack11ll11_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ௲"))
      bstack1l1lll1lll_opy_.execute_script(bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ௳") + json.dumps(str(args[0].name) + bstack11ll11_opy_ (u"ࠣࠢ࠰ࠤࡕࡧࡳࡴࡧࡧࠥࠧ௴")) + bstack11ll11_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧࢃࡽࠨ௵"))
      if runner.driver_initialised == bstack11ll11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣ௶"):
        bstack11l1l1l11l_opy_(bstack1l1lll1lll_opy_, bstack11ll11_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ௷"))
  except Exception as e:
    logger.debug(bstack11ll11_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡶࡸࡪࡶ࠺ࠡࡽࢀࠫ௸").format(str(e)))
  bstack11ll11ll1l_opy_(runner, name, context, args[0], bstack11l11111l_opy_, *args)
@measure(event_name=EVENTS.bstack11l1lllll1_opy_, stage=STAGE.bstack1lll11llll_opy_, bstack1111llll_opy_=bstack11ll11lll_opy_)
def bstack1l11l1l11l_opy_(runner, name, context, bstack11l11111l_opy_, *args):
  bstack1ll1ll1111_opy_.end_test(args[0])
  try:
    bstack111l11ll1_opy_ = args[0].status.name
    bstack1l1lll1lll_opy_ = bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ௹"), context.browser)
    bstack1lll1111l1_opy_.bstack1111l1111_opy_(bstack1l1lll1lll_opy_)
    if str(bstack111l11ll1_opy_).lower() == bstack11ll11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ௺"):
      bstack1lll11l11_opy_ = bstack11ll11_opy_ (u"ࠨࠩ௻")
      bstack1l111lll_opy_ = bstack11ll11_opy_ (u"ࠩࠪ௼")
      bstack11l11l11ll_opy_ = bstack11ll11_opy_ (u"ࠪࠫ௽")
      try:
        import traceback
        bstack1lll11l11_opy_ = runner.exception.__class__.__name__
        bstack1ll1ll11l_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1l111lll_opy_ = bstack11ll11_opy_ (u"ࠫࠥ࠭௾").join(bstack1ll1ll11l_opy_)
        bstack11l11l11ll_opy_ = bstack1ll1ll11l_opy_[-1]
      except Exception as e:
        logger.debug(bstack1lllllll1_opy_.format(str(e)))
      bstack1lll11l11_opy_ += bstack11l11l11ll_opy_
      bstack1l11l111l_opy_(context, json.dumps(str(args[0].name) + bstack11ll11_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦ௿") + str(bstack1l111lll_opy_)),
                          bstack11ll11_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧఀ"))
      if runner.driver_initialised == bstack11ll11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤఁ") or runner.driver_initialised == bstack11ll11_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨం"):
        bstack11lll1l11l_opy_(getattr(context, bstack11ll11_opy_ (u"ࠩࡳࡥ࡬࡫ࠧః"), None), bstack11ll11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥఄ"), bstack1lll11l11_opy_)
        bstack1l1lll1lll_opy_.execute_script(bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩఅ") + json.dumps(str(args[0].name) + bstack11ll11_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦఆ") + str(bstack1l111lll_opy_)) + bstack11ll11_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥࢁࢂ࠭ఇ"))
      if runner.driver_initialised == bstack11ll11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤఈ") or runner.driver_initialised == bstack11ll11_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨఉ"):
        bstack11l1l1l11l_opy_(bstack1l1lll1lll_opy_, bstack11ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩఊ"), bstack11ll11_opy_ (u"ࠥࡗࡨ࡫࡮ࡢࡴ࡬ࡳࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢఋ") + str(bstack1lll11l11_opy_))
    else:
      bstack1l11l111l_opy_(context, bstack11ll11_opy_ (u"ࠦࡕࡧࡳࡴࡧࡧࠥࠧఌ"), bstack11ll11_opy_ (u"ࠧ࡯࡮ࡧࡱࠥ఍"))
      if runner.driver_initialised == bstack11ll11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣఎ") or runner.driver_initialised == bstack11ll11_opy_ (u"ࠧࡪࡰࡶࡸࡪࡶࠧఏ"):
        bstack11lll1l11l_opy_(getattr(context, bstack11ll11_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭ఐ"), None), bstack11ll11_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ఑"))
      bstack1l1lll1lll_opy_.execute_script(bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨఒ") + json.dumps(str(args[0].name) + bstack11ll11_opy_ (u"ࠦࠥ࠳ࠠࡑࡣࡶࡷࡪࡪࠡࠣఓ")) + bstack11ll11_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫఔ"))
      if runner.driver_initialised == bstack11ll11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣక") or runner.driver_initialised == bstack11ll11_opy_ (u"ࠧࡪࡰࡶࡸࡪࡶࠧఖ"):
        bstack11l1l1l11l_opy_(bstack1l1lll1lll_opy_, bstack11ll11_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣగ"))
  except Exception as e:
    logger.debug(bstack11ll11_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫఘ").format(str(e)))
  bstack11ll11ll1l_opy_(runner, name, context, context.scenario, bstack11l11111l_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack1l11l1l111_opy_(runner, name, context, bstack11l11111l_opy_, *args):
    target = context.scenario if hasattr(context, bstack11ll11_opy_ (u"ࠪࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬఙ")) else context.feature
    bstack11ll11ll1l_opy_(runner, name, context, target, bstack11l11111l_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack11l11111ll_opy_(runner, name, context, bstack11l11111l_opy_, *args):
    try:
      bstack1l1lll1lll_opy_ = bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪచ"), context.browser)
      bstack11ll111l1l_opy_ = bstack11ll11_opy_ (u"ࠬ࠭ఛ")
      if context.failed is True:
        bstack11lll1ll1l_opy_ = []
        bstack1ll1ll11l1_opy_ = []
        bstack1l1l1l11l1_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack11lll1ll1l_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1ll1ll11l_opy_ = traceback.format_tb(exc_tb)
            bstack1lll11l1l_opy_ = bstack11ll11_opy_ (u"࠭ࠠࠨజ").join(bstack1ll1ll11l_opy_)
            bstack1ll1ll11l1_opy_.append(bstack1lll11l1l_opy_)
            bstack1l1l1l11l1_opy_.append(bstack1ll1ll11l_opy_[-1])
        except Exception as e:
          logger.debug(bstack1lllllll1_opy_.format(str(e)))
        bstack1lll11l11_opy_ = bstack11ll11_opy_ (u"ࠧࠨఝ")
        for i in range(len(bstack11lll1ll1l_opy_)):
          bstack1lll11l11_opy_ += bstack11lll1ll1l_opy_[i] + bstack1l1l1l11l1_opy_[i] + bstack11ll11_opy_ (u"ࠨ࡞ࡱࠫఞ")
        bstack11ll111l1l_opy_ = bstack11ll11_opy_ (u"ࠩࠣࠫట").join(bstack1ll1ll11l1_opy_)
        if runner.driver_initialised in [bstack11ll11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦఠ"), bstack11ll11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣడ")]:
          bstack1l11l111l_opy_(context, bstack11ll111l1l_opy_, bstack11ll11_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦఢ"))
          bstack11lll1l11l_opy_(getattr(context, bstack11ll11_opy_ (u"࠭ࡰࡢࡩࡨࠫణ"), None), bstack11ll11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢత"), bstack1lll11l11_opy_)
          bstack1l1lll1lll_opy_.execute_script(bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭థ") + json.dumps(bstack11ll111l1l_opy_) + bstack11ll11_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࡽࡾࠩద"))
          bstack11l1l1l11l_opy_(bstack1l1lll1lll_opy_, bstack11ll11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥధ"), bstack11ll11_opy_ (u"ࠦࡘࡵ࡭ࡦࠢࡶࡧࡪࡴࡡࡳ࡫ࡲࡷࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦ࡜࡯ࠤన") + str(bstack1lll11l11_opy_))
          bstack11l111111_opy_ = bstack11llll11l1_opy_(bstack11ll111l1l_opy_, runner.feature.name, logger)
          if (bstack11l111111_opy_ != None):
            bstack1ll1l1111_opy_.append(bstack11l111111_opy_)
      else:
        if runner.driver_initialised in [bstack11ll11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨ఩"), bstack11ll11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥప")]:
          bstack1l11l111l_opy_(context, bstack11ll11_opy_ (u"ࠢࡇࡧࡤࡸࡺࡸࡥ࠻ࠢࠥఫ") + str(runner.feature.name) + bstack11ll11_opy_ (u"ࠣࠢࡳࡥࡸࡹࡥࡥࠣࠥబ"), bstack11ll11_opy_ (u"ࠤ࡬ࡲ࡫ࡵࠢభ"))
          bstack11lll1l11l_opy_(getattr(context, bstack11ll11_opy_ (u"ࠪࡴࡦ࡭ࡥࠨమ"), None), bstack11ll11_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦయ"))
          bstack1l1lll1lll_opy_.execute_script(bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪర") + json.dumps(bstack11ll11_opy_ (u"ࠨࡆࡦࡣࡷࡹࡷ࡫࠺ࠡࠤఱ") + str(runner.feature.name) + bstack11ll11_opy_ (u"ࠢࠡࡲࡤࡷࡸ࡫ࡤࠢࠤల")) + bstack11ll11_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦࢂࢃࠧళ"))
          bstack11l1l1l11l_opy_(bstack1l1lll1lll_opy_, bstack11ll11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩఴ"))
          bstack11l111111_opy_ = bstack11llll11l1_opy_(bstack11ll111l1l_opy_, runner.feature.name, logger)
          if (bstack11l111111_opy_ != None):
            bstack1ll1l1111_opy_.append(bstack11l111111_opy_)
    except Exception as e:
      logger.debug(bstack11ll11_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡯࡮ࠡࡣࡩࡸࡪࡸࠠࡧࡧࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬవ").format(str(e)))
    bstack11ll11ll1l_opy_(runner, name, context, context.feature, bstack11l11111l_opy_, *args)
@measure(event_name=EVENTS.bstack1l11l1lll1_opy_, stage=STAGE.bstack1lll11llll_opy_, hook_type=bstack11ll11_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࡄࡰࡱࠨశ"), bstack1111llll_opy_=bstack11ll11lll_opy_)
def bstack1llll1l1_opy_(runner, name, context, bstack11l11111l_opy_, *args):
    bstack11ll11ll1l_opy_(runner, name, context, runner, bstack11l11111l_opy_, *args)
def bstack1l1l111l_opy_(self, name, context, *args):
  if bstack11ll11l1_opy_:
    platform_index = int(threading.current_thread()._name) % bstack111l1l111_opy_
    bstack11l1l111l1_opy_ = CONFIG[bstack11ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨష")][platform_index]
    os.environ[bstack11ll11_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧస")] = json.dumps(bstack11l1l111l1_opy_)
  global bstack11l11111l_opy_
  if not hasattr(self, bstack11ll11_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡨࡨࠬహ")):
    self.driver_initialised = None
  bstack1ll1l11l1_opy_ = {
      bstack11ll11_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠬ఺"): bstack11lll1ll_opy_,
      bstack11ll11_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠪ఻"): bstack1lllllllll_opy_,
      bstack11ll11_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡸࡦ࡭఼ࠧ"): bstack111l111l_opy_,
      bstack11ll11_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ఽ"): bstack1l1llll11_opy_,
      bstack11ll11_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠪా"): bstack11l1lll1l_opy_,
      bstack11ll11_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡴࡦࡲࠪి"): bstack1111ll11_opy_,
      bstack11ll11_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨీ"): bstack1l11l1l11l_opy_,
      bstack11ll11_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡵࡣࡪࠫు"): bstack1l11l1l111_opy_,
      bstack11ll11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠩూ"): bstack11l11111ll_opy_,
      bstack11ll11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ࠭ృ"): bstack1llll1l1_opy_
  }
  handler = bstack1ll1l11l1_opy_.get(name, bstack11l11111l_opy_)
  handler(self, name, context, bstack11l11111l_opy_, *args)
  if name in [bstack11ll11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫౄ"), bstack11ll11_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭౅"), bstack11ll11_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠩె")]:
    try:
      bstack1l1lll1lll_opy_ = threading.current_thread().bstackSessionDriver if bstack1l11ll1lll_opy_(bstack11ll11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ే")) else context.browser
      bstack1ll1llll11_opy_ = (
        (name == bstack11ll11_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠫై") and self.driver_initialised == bstack11ll11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨ౉")) or
        (name == bstack11ll11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪొ") and self.driver_initialised == bstack11ll11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠧో")) or
        (name == bstack11ll11_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ౌ") and self.driver_initialised in [bstack11ll11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯్ࠣ"), bstack11ll11_opy_ (u"ࠢࡪࡰࡶࡸࡪࡶࠢ౎")]) or
        (name == bstack11ll11_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡴࡶࡨࡴࠬ౏") and self.driver_initialised == bstack11ll11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢ౐"))
      )
      if bstack1ll1llll11_opy_:
        self.driver_initialised = None
        bstack1l1lll1lll_opy_.quit()
    except Exception:
      pass
def bstack1ll1l11l_opy_(config, startdir):
  return bstack11ll11_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀ࠶ࡽࠣ౑").format(bstack11ll11_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥ౒"))
notset = Notset()
def bstack111l1l11_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1lll11ll1_opy_
  if str(name).lower() == bstack11ll11_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࠬ౓"):
    return bstack11ll11_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧ౔")
  else:
    return bstack1lll11ll1_opy_(self, name, default, skip)
def bstack11111lll_opy_(item, when):
  global bstack11l111l1_opy_
  try:
    bstack11l111l1_opy_(item, when)
  except Exception as e:
    pass
def bstack11ll1ll1l1_opy_():
  return
def bstack11l1lll11_opy_(type, name, status, reason, bstack111lll111_opy_, bstack11ll111lll_opy_):
  bstack1l11l1111_opy_ = {
    bstack11ll11_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴౕࠧ"): type,
    bstack11ll11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶౖࠫ"): {}
  }
  if type == bstack11ll11_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫ౗"):
    bstack1l11l1111_opy_[bstack11ll11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ౘ")][bstack11ll11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪౙ")] = bstack111lll111_opy_
    bstack1l11l1111_opy_[bstack11ll11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨౚ")][bstack11ll11_opy_ (u"࠭ࡤࡢࡶࡤࠫ౛")] = json.dumps(str(bstack11ll111lll_opy_))
  if type == bstack11ll11_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ౜"):
    bstack1l11l1111_opy_[bstack11ll11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫౝ")][bstack11ll11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ౞")] = name
  if type == bstack11ll11_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭౟"):
    bstack1l11l1111_opy_[bstack11ll11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧౠ")][bstack11ll11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬౡ")] = status
    if status == bstack11ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ౢ"):
      bstack1l11l1111_opy_[bstack11ll11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪౣ")][bstack11ll11_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨ౤")] = json.dumps(str(reason))
  bstack1l1ll11ll_opy_ = bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧ౥").format(json.dumps(bstack1l11l1111_opy_))
  return bstack1l1ll11ll_opy_
def bstack1l1l1l1l1l_opy_(driver_command, response):
    if driver_command == bstack11ll11_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧ౦"):
        bstack1l1l1l1ll_opy_.bstack111lll11l_opy_({
            bstack11ll11_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪ౧"): response[bstack11ll11_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫ౨")],
            bstack11ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭౩"): bstack1l1l1l1ll_opy_.current_test_uuid()
        })
def bstack1l1l1lll1_opy_(item, call, rep):
  global bstack1ll111ll1_opy_
  global bstack1l11ll1ll1_opy_
  global bstack1llllll1ll_opy_
  name = bstack11ll11_opy_ (u"ࠧࠨ౪")
  try:
    if rep.when == bstack11ll11_opy_ (u"ࠨࡥࡤࡰࡱ࠭౫"):
      bstack11ll1111l1_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1llllll1ll_opy_:
          name = str(rep.nodeid)
          bstack11ll11l11_opy_ = bstack11l1lll11_opy_(bstack11ll11_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ౬"), name, bstack11ll11_opy_ (u"ࠪࠫ౭"), bstack11ll11_opy_ (u"ࠫࠬ౮"), bstack11ll11_opy_ (u"ࠬ࠭౯"), bstack11ll11_opy_ (u"࠭ࠧ౰"))
          threading.current_thread().bstack11l1lll1l1_opy_ = name
          for driver in bstack1l11ll1ll1_opy_:
            if bstack11ll1111l1_opy_ == driver.session_id:
              driver.execute_script(bstack11ll11l11_opy_)
      except Exception as e:
        logger.debug(bstack11ll11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧ౱").format(str(e)))
      try:
        bstack1ll11lll11_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack11ll11_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ౲"):
          status = bstack11ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ౳") if rep.outcome.lower() == bstack11ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ౴") else bstack11ll11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ౵")
          reason = bstack11ll11_opy_ (u"ࠬ࠭౶")
          if status == bstack11ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭౷"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack11ll11_opy_ (u"ࠧࡪࡰࡩࡳࠬ౸") if status == bstack11ll11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ౹") else bstack11ll11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ౺")
          data = name + bstack11ll11_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬ౻") if status == bstack11ll11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ౼") else name + bstack11ll11_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩࠧࠠࠨ౽") + reason
          bstack11111ll11_opy_ = bstack11l1lll11_opy_(bstack11ll11_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨ౾"), bstack11ll11_opy_ (u"ࠧࠨ౿"), bstack11ll11_opy_ (u"ࠨࠩಀ"), bstack11ll11_opy_ (u"ࠩࠪಁ"), level, data)
          for driver in bstack1l11ll1ll1_opy_:
            if bstack11ll1111l1_opy_ == driver.session_id:
              driver.execute_script(bstack11111ll11_opy_)
      except Exception as e:
        logger.debug(bstack11ll11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡤࡱࡱࡸࡪࡾࡴࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧಂ").format(str(e)))
  except Exception as e:
    logger.debug(bstack11ll11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡶࡤࡸࡪࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁࡽࠨಃ").format(str(e)))
  bstack1ll111ll1_opy_(item, call, rep)
def bstack11111llll_opy_(driver, bstack11l1111l_opy_, test=None):
  global bstack11llllllll_opy_
  if test != None:
    bstack1l1lll11l1_opy_ = getattr(test, bstack11ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ಄"), None)
    bstack1l1111111_opy_ = getattr(test, bstack11ll11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫಅ"), None)
    PercySDK.screenshot(driver, bstack11l1111l_opy_, bstack1l1lll11l1_opy_=bstack1l1lll11l1_opy_, bstack1l1111111_opy_=bstack1l1111111_opy_, bstack11ll1lll1_opy_=bstack11llllllll_opy_)
  else:
    PercySDK.screenshot(driver, bstack11l1111l_opy_)
@measure(event_name=EVENTS.bstack1lll1111_opy_, stage=STAGE.bstack1lll11llll_opy_, bstack1111llll_opy_=bstack11ll11lll_opy_)
def bstack111l1l1ll_opy_(driver):
  if bstack1lll1l1111_opy_.bstack11l11l1ll1_opy_() is True or bstack1lll1l1111_opy_.capturing() is True:
    return
  bstack1lll1l1111_opy_.bstack1ll11lll1l_opy_()
  while not bstack1lll1l1111_opy_.bstack11l11l1ll1_opy_():
    bstack1ll111l11_opy_ = bstack1lll1l1111_opy_.bstack1l1111ll_opy_()
    bstack11111llll_opy_(driver, bstack1ll111l11_opy_)
  bstack1lll1l1111_opy_.bstack11l11111_opy_()
def bstack1111l1l1l_opy_(sequence, driver_command, response = None, bstack111l11ll_opy_ = None, args = None):
    try:
      if sequence != bstack11ll11_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧಆ"):
        return
      if percy.bstack11ll1ll1l_opy_() == bstack11ll11_opy_ (u"ࠣࡨࡤࡰࡸ࡫ࠢಇ"):
        return
      bstack1ll111l11_opy_ = bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠩࡳࡩࡷࡩࡹࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬಈ"), None)
      for command in bstack1lll1l11ll_opy_:
        if command == driver_command:
          for driver in bstack1l11ll1ll1_opy_:
            bstack111l1l1ll_opy_(driver)
      bstack11l111lll1_opy_ = percy.bstack1l1l11l1_opy_()
      if driver_command in bstack1l1ll11l1_opy_[bstack11l111lll1_opy_]:
        bstack1lll1l1111_opy_.bstack1l1111l111_opy_(bstack1ll111l11_opy_, driver_command)
    except Exception as e:
      pass
def bstack1ll1ll111l_opy_(framework_name):
  if bstack1l1ll1llll_opy_.get_property(bstack11ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡱࡴࡪ࡟ࡤࡣ࡯ࡰࡪࡪࠧಉ")):
      return
  bstack1l1ll1llll_opy_.bstack1l111lll11_opy_(bstack11ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨಊ"), True)
  global bstack1lll11l1ll_opy_
  global bstack1ll111ll11_opy_
  global bstack11l111111l_opy_
  bstack1lll11l1ll_opy_ = framework_name
  logger.info(bstack11l1l11ll1_opy_.format(bstack1lll11l1ll_opy_.split(bstack11ll11_opy_ (u"ࠬ࠳ࠧಋ"))[0]))
  bstack11l1lll1_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack11ll11l1_opy_:
      Service.start = bstack11111l111_opy_
      Service.stop = bstack11lllll1ll_opy_
      webdriver.Remote.get = bstack111111l11_opy_
      WebDriver.quit = bstack1l1l1111_opy_
      webdriver.Remote.__init__ = bstack1ll11ll11l_opy_
    if not bstack11ll11l1_opy_:
        webdriver.Remote.__init__ = bstack1ll111ll1l_opy_
    WebDriver.getAccessibilityResults = getAccessibilityResults
    WebDriver.get_accessibility_results = getAccessibilityResults
    WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
    WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
    WebDriver.performScan = perform_scan
    WebDriver.perform_scan = perform_scan
    WebDriver.execute = bstack11ll111l11_opy_
    bstack1ll111ll11_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack11ll11l1_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack111lllll_opy_
  except Exception as e:
    pass
  bstack11ll111l_opy_()
  if not bstack1ll111ll11_opy_:
    bstack1lll11l1l1_opy_(bstack11ll11_opy_ (u"ࠨࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠡࡰࡲࡸࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠣಌ"), bstack1ll111ll_opy_)
  if bstack11l1ll111l_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      if hasattr(RemoteConnection, bstack11ll11_opy_ (u"ࠧࡠࡩࡨࡸࡤࡶࡲࡰࡺࡼࡣࡺࡸ࡬ࠨ಍")) and callable(getattr(RemoteConnection, bstack11ll11_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩಎ"))):
        RemoteConnection._get_proxy_url = bstack11l11l11_opy_
      else:
        from selenium.webdriver.remote.client_config import ClientConfig
        ClientConfig.get_proxy_url = bstack11l11l11_opy_
    except Exception as e:
      logger.error(bstack11ll1111l_opy_.format(str(e)))
  if bstack1l1llll111_opy_():
    bstack1l11ll1l1_opy_(CONFIG, logger)
  if (bstack11ll11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨಏ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if percy.bstack11ll1ll1l_opy_() == bstack11ll11_opy_ (u"ࠥࡸࡷࡻࡥࠣಐ"):
          bstack1l1l11l111_opy_(bstack1111l1l1l_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack11l1l11111_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1lll111ll1_opy_
      except Exception as e:
        logger.warn(bstack11l1111lll_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack11l11ll1l_opy_
      except Exception as e:
        logger.debug(bstack1l11111l11_opy_ + str(e))
    except Exception as e:
      bstack1lll11l1l1_opy_(e, bstack11l1111lll_opy_)
    Output.start_test = bstack1lllll11_opy_
    Output.end_test = bstack1l11l1l1ll_opy_
    TestStatus.__init__ = bstack1l1l1l1l_opy_
    QueueItem.__init__ = bstack1lll1ll1l1_opy_
    pabot._create_items = bstack11ll1ll111_opy_
    try:
      from pabot import __version__ as bstack1lllll1ll1_opy_
      if version.parse(bstack1lllll1ll1_opy_) >= version.parse(bstack11ll11_opy_ (u"ࠫ࠹࠴࠲࠯࠲ࠪ಑")):
        pabot._run = bstack11l11ll11_opy_
      elif version.parse(bstack1lllll1ll1_opy_) >= version.parse(bstack11ll11_opy_ (u"ࠬ࠸࠮࠲࠷࠱࠴ࠬಒ")):
        pabot._run = bstack11ll111l1_opy_
      elif version.parse(bstack1lllll1ll1_opy_) >= version.parse(bstack11ll11_opy_ (u"࠭࠲࠯࠳࠶࠲࠵࠭ಓ")):
        pabot._run = bstack1ll1l111l_opy_
      else:
        pabot._run = bstack11ll1l1l11_opy_
    except Exception as e:
      pabot._run = bstack11ll1l1l11_opy_
    pabot._create_command_for_execution = bstack11l1ll1ll_opy_
    pabot._report_results = bstack11lll1111_opy_
  if bstack11ll11_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧಔ") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1lll11l1l1_opy_(e, bstack11l1l1l111_opy_)
    Runner.run_hook = bstack1l1l111l_opy_
    Step.run = bstack1l1lllll11_opy_
  if bstack11ll11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨಕ") in str(framework_name).lower():
    if not bstack11ll11l1_opy_:
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack1ll1l11l_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack11ll1ll1l1_opy_
      Config.getoption = bstack111l1l11_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1l1l1lll1_opy_
    except Exception as e:
      pass
def bstack1l111l11l_opy_():
  global CONFIG
  if bstack11ll11_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩಖ") in CONFIG and int(CONFIG[bstack11ll11_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪಗ")]) > 1:
    logger.warn(bstack1ll1l11ll1_opy_)
def bstack1l1lll111l_opy_(arg, bstack1ll11ll1l_opy_, bstack1ll11l11_opy_=None):
  global CONFIG
  global bstack11lll111ll_opy_
  global bstack1ll1lllll1_opy_
  global bstack11ll11l1_opy_
  global bstack1l1ll1llll_opy_
  bstack11ll1l11l_opy_ = bstack11ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫಘ")
  if bstack1ll11ll1l_opy_ and isinstance(bstack1ll11ll1l_opy_, str):
    bstack1ll11ll1l_opy_ = eval(bstack1ll11ll1l_opy_)
  CONFIG = bstack1ll11ll1l_opy_[bstack11ll11_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬಙ")]
  bstack11lll111ll_opy_ = bstack1ll11ll1l_opy_[bstack11ll11_opy_ (u"࠭ࡈࡖࡄࡢ࡙ࡗࡒࠧಚ")]
  bstack1ll1lllll1_opy_ = bstack1ll11ll1l_opy_[bstack11ll11_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩಛ")]
  bstack11ll11l1_opy_ = bstack1ll11ll1l_opy_[bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫಜ")]
  bstack1l1ll1llll_opy_.bstack1l111lll11_opy_(bstack11ll11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪಝ"), bstack11ll11l1_opy_)
  os.environ[bstack11ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬಞ")] = bstack11ll1l11l_opy_
  os.environ[bstack11ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠪಟ")] = json.dumps(CONFIG)
  os.environ[bstack11ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡍ࡛ࡂࡠࡗࡕࡐࠬಠ")] = bstack11lll111ll_opy_
  os.environ[bstack11ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧಡ")] = str(bstack1ll1lllll1_opy_)
  os.environ[bstack11ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡍࡗࡊࡍࡓ࠭ಢ")] = str(True)
  if bstack11llllll_opy_(arg, [bstack11ll11_opy_ (u"ࠨ࠯ࡱࠫಣ"), bstack11ll11_opy_ (u"ࠩ࠰࠱ࡳࡻ࡭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪತ")]) != -1:
    os.environ[bstack11ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡅࡗࡇࡌࡍࡇࡏࠫಥ")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1lllll11ll_opy_)
    return
  bstack1l11ll11l1_opy_()
  global bstack1l111llll_opy_
  global bstack11llllllll_opy_
  global bstack11llllll11_opy_
  global bstack11l1111l11_opy_
  global bstack1l1l1lll11_opy_
  global bstack11l111111l_opy_
  global bstack111lll1ll_opy_
  arg.append(bstack11ll11_opy_ (u"ࠦ࠲࡝ࠢದ"))
  arg.append(bstack11ll11_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩ࠿ࡓ࡯ࡥࡷ࡯ࡩࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡩ࡮ࡲࡲࡶࡹ࡫ࡤ࠻ࡲࡼࡸࡪࡹࡴ࠯ࡒࡼࡸࡪࡹࡴࡘࡣࡵࡲ࡮ࡴࡧࠣಧ"))
  arg.append(bstack11ll11_opy_ (u"ࠨ࠭ࡘࠤನ"))
  arg.append(bstack11ll11_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫࠺ࡕࡪࡨࠤ࡭ࡵ࡯࡬࡫ࡰࡴࡱࠨ಩"))
  global bstack1l1llll1_opy_
  global bstack11llll1l_opy_
  global bstack1ll11ll11_opy_
  global bstack1ll1l1lll1_opy_
  global bstack111ll1l1_opy_
  global bstack11l1l1ll1l_opy_
  global bstack11l11l1l1l_opy_
  global bstack1ll1111ll1_opy_
  global bstack11lllllll_opy_
  global bstack11ll11111l_opy_
  global bstack1lll11ll1_opy_
  global bstack11l111l1_opy_
  global bstack1ll111ll1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l1llll1_opy_ = webdriver.Remote.__init__
    bstack11llll1l_opy_ = WebDriver.quit
    bstack1ll1111ll1_opy_ = WebDriver.close
    bstack11lllllll_opy_ = WebDriver.get
    bstack1ll11ll11_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1ll111l11l_opy_(CONFIG) and bstack1111llll1_opy_():
    if bstack1lll1ll1_opy_() < version.parse(bstack1lll111ll_opy_):
      logger.error(bstack11ll1l11ll_opy_.format(bstack1lll1ll1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack11ll11_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩಪ")) and callable(getattr(RemoteConnection, bstack11ll11_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪಫ"))):
          bstack11ll11111l_opy_ = RemoteConnection._get_proxy_url
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          bstack11ll11111l_opy_ = ClientConfig.get_proxy_url
      except Exception as e:
        logger.error(bstack11ll1111l_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1lll11ll1_opy_ = Config.getoption
    from _pytest import runner
    bstack11l111l1_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack11ll1l1l1l_opy_)
  try:
    from pytest_bdd import reporting
    bstack1ll111ll1_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack11ll11_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡲࠤࡷࡻ࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࡶࠫಬ"))
  bstack11llllll11_opy_ = CONFIG.get(bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨಭ"), {}).get(bstack11ll11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧಮ"))
  bstack111lll1ll_opy_ = True
  if cli.is_enabled(CONFIG):
    if cli.bstack1l11111lll_opy_():
      bstack11111l11l_opy_.invoke(bstack11l11l1l_opy_.CONNECT, bstack11ll1111ll_opy_())
    platform_index = int(os.environ.get(bstack11ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ಯ"), bstack11ll11_opy_ (u"ࠧ࠱ࠩರ")))
  else:
    bstack1ll1ll111l_opy_(bstack11l11l1lll_opy_)
  os.environ[bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩಱ")] = CONFIG[bstack11ll11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫಲ")]
  os.environ[bstack11ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭ಳ")] = CONFIG[bstack11ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ಴")]
  os.environ[bstack11ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨವ")] = bstack11ll11l1_opy_.__str__()
  from _pytest.config import main as bstack11l1l1lll1_opy_
  bstack11l111l1l_opy_ = []
  try:
    bstack11lll111l_opy_ = bstack11l1l1lll1_opy_(arg)
    if cli.is_enabled(CONFIG):
      cli.bstack1ll11l11l_opy_()
    if bstack11ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶࠪಶ") in multiprocessing.current_process().__dict__.keys():
      for bstack1l111ll111_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack11l111l1l_opy_.append(bstack1l111ll111_opy_)
    try:
      bstack11ll1l1lll_opy_ = (bstack11l111l1l_opy_, int(bstack11lll111l_opy_))
      bstack1ll11l11_opy_.append(bstack11ll1l1lll_opy_)
    except:
      bstack1ll11l11_opy_.append((bstack11l111l1l_opy_, bstack11lll111l_opy_))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack11l111l1l_opy_.append({bstack11ll11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬಷ"): bstack11ll11_opy_ (u"ࠨࡒࡵࡳࡨ࡫ࡳࡴࠢࠪಸ") + os.environ.get(bstack11ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩಹ")), bstack11ll11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ಺"): traceback.format_exc(), bstack11ll11_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ಻"): int(os.environ.get(bstack11ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜಼ࠬ")))})
    bstack1ll11l11_opy_.append((bstack11l111l1l_opy_, 1))
def mod_behave_main(args, retries):
  try:
    from behave.configuration import Configuration
    from behave.__main__ import run_behave
    from browserstack_sdk.bstack_behave_runner import BehaveRunner
    config = Configuration(args)
    config.update_userdata({bstack11ll11_opy_ (u"ࠨࡲࡦࡶࡵ࡭ࡪࡹࠢಽ"): str(retries)})
    return run_behave(config, runner_class=BehaveRunner)
  except Exception as e:
    bstack1l111lll1_opy_ = e.__class__.__name__
    print(bstack11ll11_opy_ (u"ࠢࠦࡵ࠽ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡶࡺࡴ࡮ࡪࡰࡪࠤࡧ࡫ࡨࡢࡸࡨࠤࡹ࡫ࡳࡵࠢࠨࡷࠧಾ") % (bstack1l111lll1_opy_, e))
    return 1
def bstack11111ll1l_opy_(arg):
  global bstack111l1lll_opy_
  bstack1ll1ll111l_opy_(bstack111111ll1_opy_)
  os.environ[bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩಿ")] = str(bstack1ll1lllll1_opy_)
  retries = bstack111l11l1l_opy_.bstack11ll1llll_opy_(CONFIG)
  status_code = 0
  if bstack111l11l1l_opy_.bstack1llll1ll11_opy_(CONFIG):
    status_code = mod_behave_main(arg, retries)
  else:
    from behave.__main__ import main as bstack111l11111_opy_
    status_code = bstack111l11111_opy_(arg)
  if status_code != 0:
    bstack111l1lll_opy_ = status_code
def bstack11l1ll1lll_opy_():
  logger.info(bstack1l1lll1l11_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack11ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨೀ"), help=bstack11ll11_opy_ (u"ࠪࡋࡪࡴࡥࡳࡣࡷࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡨࡵ࡮ࡧ࡫ࡪࠫು"))
  parser.add_argument(bstack11ll11_opy_ (u"ࠫ࠲ࡻࠧೂ"), bstack11ll11_opy_ (u"ࠬ࠳࠭ࡶࡵࡨࡶࡳࡧ࡭ࡦࠩೃ"), help=bstack11ll11_opy_ (u"࡙࠭ࡰࡷࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬೄ"))
  parser.add_argument(bstack11ll11_opy_ (u"ࠧ࠮࡭ࠪ೅"), bstack11ll11_opy_ (u"ࠨ࠯࠰࡯ࡪࡿࠧೆ"), help=bstack11ll11_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡡࡤࡥࡨࡷࡸࠦ࡫ࡦࡻࠪೇ"))
  parser.add_argument(bstack11ll11_opy_ (u"ࠪ࠱࡫࠭ೈ"), bstack11ll11_opy_ (u"ࠫ࠲࠳ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ೉"), help=bstack11ll11_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫೊ"))
  bstack11l1llll1l_opy_ = parser.parse_args()
  try:
    bstack111l1111_opy_ = bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥ࡯ࡧࡵ࡭ࡨ࠴ࡹ࡮࡮࠱ࡷࡦࡳࡰ࡭ࡧࠪೋ")
    if bstack11l1llll1l_opy_.framework and bstack11l1llll1l_opy_.framework not in (bstack11ll11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧೌ"), bstack11ll11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴್ࠩ")):
      bstack111l1111_opy_ = bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠲ࡾࡳ࡬࠯ࡵࡤࡱࡵࡲࡥࠨ೎")
    bstack111ll111l_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack111l1111_opy_)
    bstack11l11ll1l1_opy_ = open(bstack111ll111l_opy_, bstack11ll11_opy_ (u"ࠪࡶࠬ೏"))
    bstack111ll1ll1_opy_ = bstack11l11ll1l1_opy_.read()
    bstack11l11ll1l1_opy_.close()
    if bstack11l1llll1l_opy_.username:
      bstack111ll1ll1_opy_ = bstack111ll1ll1_opy_.replace(bstack11ll11_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫ೐"), bstack11l1llll1l_opy_.username)
    if bstack11l1llll1l_opy_.key:
      bstack111ll1ll1_opy_ = bstack111ll1ll1_opy_.replace(bstack11ll11_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧ೑"), bstack11l1llll1l_opy_.key)
    if bstack11l1llll1l_opy_.framework:
      bstack111ll1ll1_opy_ = bstack111ll1ll1_opy_.replace(bstack11ll11_opy_ (u"࡙࠭ࡐࡗࡕࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ೒"), bstack11l1llll1l_opy_.framework)
    file_name = bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪ೓")
    file_path = os.path.abspath(file_name)
    bstack1ll11111ll_opy_ = open(file_path, bstack11ll11_opy_ (u"ࠨࡹࠪ೔"))
    bstack1ll11111ll_opy_.write(bstack111ll1ll1_opy_)
    bstack1ll11111ll_opy_.close()
    logger.info(bstack1ll1ll1l_opy_)
    try:
      os.environ[bstack11ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫೕ")] = bstack11l1llll1l_opy_.framework if bstack11l1llll1l_opy_.framework != None else bstack11ll11_opy_ (u"ࠥࠦೖ")
      config = yaml.safe_load(bstack111ll1ll1_opy_)
      config[bstack11ll11_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ೗")] = bstack11ll11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲ࡹࡥࡵࡷࡳࠫ೘")
      bstack1ll111l111_opy_(bstack111l111l1_opy_, config)
    except Exception as e:
      logger.debug(bstack11lll1ll11_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1lll1l1lll_opy_.format(str(e)))
def bstack1ll111l111_opy_(bstack1l1ll11l1l_opy_, config, bstack1ll1111l11_opy_={}):
  global bstack11ll11l1_opy_
  global bstack11llll11l_opy_
  global bstack1l1ll1llll_opy_
  if not config:
    return
  bstack11llllll1_opy_ = bstack1lllll1ll_opy_ if not bstack11ll11l1_opy_ else (
    bstack1lll1ll1l_opy_ if bstack11ll11_opy_ (u"࠭ࡡࡱࡲࠪ೙") in config else (
        bstack1l111ll1_opy_ if config.get(bstack11ll11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ೚")) else bstack1l1ll111l_opy_
    )
)
  bstack1llllll11_opy_ = False
  bstack1llll1111l_opy_ = False
  if bstack11ll11l1_opy_ is True:
      if bstack11ll11_opy_ (u"ࠨࡣࡳࡴࠬ೛") in config:
          bstack1llllll11_opy_ = True
      else:
          bstack1llll1111l_opy_ = True
  bstack1l11111111_opy_ = bstack1l1ll1lll1_opy_.bstack1ll1l1l11l_opy_(config, bstack11llll11l_opy_)
  bstack1ll11l1111_opy_ = bstack1ll1ll1lll_opy_()
  data = {
    bstack11ll11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ೜"): config[bstack11ll11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬೝ")],
    bstack11ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧೞ"): config[bstack11ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ೟")],
    bstack11ll11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪೠ"): bstack1l1ll11l1l_opy_,
    bstack11ll11_opy_ (u"ࠧࡥࡧࡷࡩࡨࡺࡥࡥࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫೡ"): os.environ.get(bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪೢ"), bstack11llll11l_opy_),
    bstack11ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫೣ"): bstack1l11l1l11_opy_,
    bstack11ll11_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰࠬ೤"): bstack11l111l11_opy_(),
    bstack11ll11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧ೥"): {
      bstack11ll11_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ೦"): str(config[bstack11ll11_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭೧")]) if bstack11ll11_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ೨") in config else bstack11ll11_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤ೩"),
      bstack11ll11_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨ࡚ࡪࡸࡳࡪࡱࡱࠫ೪"): sys.version,
      bstack11ll11_opy_ (u"ࠪࡶࡪ࡬ࡥࡳࡴࡨࡶࠬ೫"): bstack1lll11lll1_opy_(os.environ.get(bstack11ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭೬"), bstack11llll11l_opy_)),
      bstack11ll11_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠧ೭"): bstack11ll11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭೮"),
      bstack11ll11_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨ೯"): bstack11llllll1_opy_,
      bstack11ll11_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭೰"): bstack1l11111111_opy_,
      bstack11ll11_opy_ (u"ࠩࡷࡩࡸࡺࡨࡶࡤࡢࡹࡺ࡯ࡤࠨೱ"): os.environ[bstack11ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨೲ")],
      bstack11ll11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧೳ"): os.environ.get(bstack11ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ೴"), bstack11llll11l_opy_),
      bstack11ll11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩ೵"): bstack1l1111l1ll_opy_(os.environ.get(bstack11ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩ೶"), bstack11llll11l_opy_)),
      bstack11ll11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ೷"): bstack1ll11l1111_opy_.get(bstack11ll11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ೸")),
      bstack11ll11_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩ೹"): bstack1ll11l1111_opy_.get(bstack11ll11_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬ೺")),
      bstack11ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ೻"): config[bstack11ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ೼")] if config[bstack11ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ೽")] else bstack11ll11_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤ೾"),
      bstack11ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ೿"): str(config[bstack11ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬഀ")]) if bstack11ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ഁ") in config else bstack11ll11_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨം"),
      bstack11ll11_opy_ (u"࠭࡯ࡴࠩഃ"): sys.platform,
      bstack11ll11_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩഄ"): socket.gethostname(),
      bstack11ll11_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪഅ"): bstack1l1ll1llll_opy_.get_property(bstack11ll11_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫആ"))
    }
  }
  if not bstack1l1ll1llll_opy_.get_property(bstack11ll11_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪഇ")) is None:
    data[bstack11ll11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧഈ")][bstack11ll11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࡍࡦࡶࡤࡨࡦࡺࡡࠨഉ")] = {
      bstack11ll11_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ഊ"): bstack11ll11_opy_ (u"ࠧࡶࡵࡨࡶࡤࡱࡩ࡭࡮ࡨࡨࠬഋ"),
      bstack11ll11_opy_ (u"ࠨࡵ࡬࡫ࡳࡧ࡬ࠨഌ"): bstack1l1ll1llll_opy_.get_property(bstack11ll11_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩ഍")),
      bstack11ll11_opy_ (u"ࠪࡷ࡮࡭࡮ࡢ࡮ࡑࡹࡲࡨࡥࡳࠩഎ"): bstack1l1ll1llll_opy_.get_property(bstack11ll11_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡓࡵࠧഏ"))
    }
  if bstack1l1ll11l1l_opy_ == bstack11ll1llll1_opy_:
    data[bstack11ll11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨഐ")][bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡈࡵ࡮ࡧ࡫ࡪࠫ഑")] = bstack11l1l1l1_opy_(config)
    data[bstack11ll11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪഒ")][bstack11ll11_opy_ (u"ࠨ࡫ࡶࡔࡪࡸࡣࡺࡃࡸࡸࡴࡋ࡮ࡢࡤ࡯ࡩࡩ࠭ഓ")] = percy.bstack11l1ll11l_opy_
    data[bstack11ll11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬഔ")][bstack11ll11_opy_ (u"ࠪࡴࡪࡸࡣࡺࡄࡸ࡭ࡱࡪࡉࡥࠩക")] = percy.percy_build_id
  if not bstack111l11l1l_opy_.bstack111ll1ll_opy_(CONFIG):
    data[bstack11ll11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧഖ")][bstack11ll11_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠩഗ")] = bstack111l11l1l_opy_.bstack111ll1ll_opy_(CONFIG)
  bstack1l111l1l1l_opy_ = bstack1lll1lll1_opy_.bstack1lll11ll_opy_(CONFIG, logger)
  bstack1lll111l_opy_ = bstack111l11l1l_opy_.bstack1lll11ll_opy_(config=CONFIG)
  if bstack1l111l1l1l_opy_ is not None and bstack1lll111l_opy_ is not None and bstack1lll111l_opy_.bstack1111111l1_opy_():
    data[bstack11ll11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩഘ")][bstack1lll111l_opy_.bstack1l1ll1l11_opy_()] = bstack1l111l1l1l_opy_.bstack1llllll1l1_opy_()
  update(data[bstack11ll11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪങ")], bstack1ll1111l11_opy_)
  try:
    response = bstack1llll1ll_opy_(bstack11ll11_opy_ (u"ࠨࡒࡒࡗ࡙࠭ച"), bstack11ll11l1ll_opy_(bstack1l1l1lll_opy_), data, {
      bstack11ll11_opy_ (u"ࠩࡤࡹࡹ࡮ࠧഛ"): (config[bstack11ll11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬജ")], config[bstack11ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧഝ")])
    })
    if response:
      logger.debug(bstack111ll1l1l_opy_.format(bstack1l1ll11l1l_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1l1111ll1l_opy_.format(str(e)))
def bstack1lll11lll1_opy_(framework):
  return bstack11ll11_opy_ (u"ࠧࢁࡽ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࡻࡾࠤഞ").format(str(framework), __version__) if framework else bstack11ll11_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࢀࢃࠢട").format(
    __version__)
def bstack1l11ll11l1_opy_():
  global CONFIG
  global bstack11lllll11l_opy_
  if bool(CONFIG):
    return
  try:
    bstack1llll11ll1_opy_()
    logger.debug(bstack1llll1lll1_opy_.format(str(CONFIG)))
    bstack11lllll11l_opy_ = bstack1111l1ll1_opy_.bstack1lll11l1_opy_(CONFIG, bstack11lllll11l_opy_)
    bstack11l1lll1_opy_()
  except Exception as e:
    logger.error(bstack11ll11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱ࠮ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠦഠ") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1lll1lll1l_opy_
  atexit.register(bstack1ll11l1ll_opy_)
  signal.signal(signal.SIGINT, bstack11llll1ll1_opy_)
  signal.signal(signal.SIGTERM, bstack11llll1ll1_opy_)
def bstack1lll1lll1l_opy_(exctype, value, traceback):
  global bstack1l11ll1ll1_opy_
  try:
    for driver in bstack1l11ll1ll1_opy_:
      bstack11l1l1l11l_opy_(driver, bstack11ll11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨഡ"), bstack11ll11_opy_ (u"ࠤࡖࡩࡸࡹࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧഢ") + str(value))
  except Exception:
    pass
  logger.info(bstack1l1l1ll1ll_opy_)
  bstack11l1ll11l1_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack11l1ll11l1_opy_(message=bstack11ll11_opy_ (u"ࠪࠫണ"), bstack11l1l1l1ll_opy_ = False):
  global CONFIG
  bstack1ll11l1l11_opy_ = bstack11ll11_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡉࡽࡩࡥࡱࡶ࡬ࡳࡳ࠭ത") if bstack11l1l1l1ll_opy_ else bstack11ll11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫഥ")
  try:
    if message:
      bstack1ll1111l11_opy_ = {
        bstack1ll11l1l11_opy_ : str(message)
      }
      bstack1ll111l111_opy_(bstack11ll1llll1_opy_, CONFIG, bstack1ll1111l11_opy_)
    else:
      bstack1ll111l111_opy_(bstack11ll1llll1_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1l111l11l1_opy_.format(str(e)))
def bstack1l1l1l11ll_opy_(bstack11l1111111_opy_, size):
  bstack1l1lll1l1l_opy_ = []
  while len(bstack11l1111111_opy_) > size:
    bstack1l111l111_opy_ = bstack11l1111111_opy_[:size]
    bstack1l1lll1l1l_opy_.append(bstack1l111l111_opy_)
    bstack11l1111111_opy_ = bstack11l1111111_opy_[size:]
  bstack1l1lll1l1l_opy_.append(bstack11l1111111_opy_)
  return bstack1l1lll1l1l_opy_
def bstack11l1l1111l_opy_(args):
  if bstack11ll11_opy_ (u"࠭࠭࡮ࠩദ") in args and bstack11ll11_opy_ (u"ࠧࡱࡦࡥࠫധ") in args:
    return True
  return False
@measure(event_name=EVENTS.bstack1l11llllll_opy_, stage=STAGE.bstack11l11l11l1_opy_)
def run_on_browserstack(bstack1llll1llll_opy_=None, bstack1ll11l11_opy_=None, bstack111l1lll1_opy_=False):
  global CONFIG
  global bstack11lll111ll_opy_
  global bstack1ll1lllll1_opy_
  global bstack11llll11l_opy_
  global bstack1l1ll1llll_opy_
  bstack11ll1l11l_opy_ = bstack11ll11_opy_ (u"ࠨࠩന")
  bstack1ll11111l1_opy_(bstack111l11l11_opy_, logger)
  if bstack1llll1llll_opy_ and isinstance(bstack1llll1llll_opy_, str):
    bstack1llll1llll_opy_ = eval(bstack1llll1llll_opy_)
  if bstack1llll1llll_opy_:
    CONFIG = bstack1llll1llll_opy_[bstack11ll11_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩഩ")]
    bstack11lll111ll_opy_ = bstack1llll1llll_opy_[bstack11ll11_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫപ")]
    bstack1ll1lllll1_opy_ = bstack1llll1llll_opy_[bstack11ll11_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ഫ")]
    bstack1l1ll1llll_opy_.bstack1l111lll11_opy_(bstack11ll11_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧബ"), bstack1ll1lllll1_opy_)
    bstack11ll1l11l_opy_ = bstack11ll11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ഭ")
  bstack1l1ll1llll_opy_.bstack1l111lll11_opy_(bstack11ll11_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥࠩമ"), uuid4().__str__())
  logger.info(bstack11ll11_opy_ (u"ࠨࡕࡇࡏࠥࡸࡵ࡯ࠢࡶࡸࡦࡸࡴࡦࡦࠣࡻ࡮ࡺࡨࠡ࡫ࡧ࠾ࠥ࠭യ") + bstack1l1ll1llll_opy_.get_property(bstack11ll11_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫര")));
  logger.debug(bstack11ll11_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࡂ࠭റ") + bstack1l1ll1llll_opy_.get_property(bstack11ll11_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭ല")))
  if not bstack111l1lll1_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1lllll11ll_opy_)
      return
    if sys.argv[1] == bstack11ll11_opy_ (u"ࠬ࠳࠭ࡷࡧࡵࡷ࡮ࡵ࡮ࠨള") or sys.argv[1] == bstack11ll11_opy_ (u"࠭࠭ࡷࠩഴ"):
      logger.info(bstack11ll11_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡐࡺࡶ࡫ࡳࡳࠦࡓࡅࡍࠣࡺࢀࢃࠧവ").format(__version__))
      return
    if sys.argv[1] == bstack11ll11_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧശ"):
      bstack11l1ll1lll_opy_()
      return
  args = sys.argv
  bstack1l11ll11l1_opy_()
  global bstack1l111llll_opy_
  global bstack111l1l111_opy_
  global bstack111lll1ll_opy_
  global bstack11l111ll1_opy_
  global bstack11llllllll_opy_
  global bstack11llllll11_opy_
  global bstack11l1111l11_opy_
  global bstack11l11l1111_opy_
  global bstack1l1l1lll11_opy_
  global bstack11l111111l_opy_
  global bstack11ll1l1l1_opy_
  bstack111l1l111_opy_ = len(CONFIG.get(bstack11ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬഷ"), []))
  if not bstack11ll1l11l_opy_:
    if args[1] == bstack11ll11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪസ") or args[1] == bstack11ll11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬഹ"):
      bstack11ll1l11l_opy_ = bstack11ll11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬഺ")
      args = args[2:]
    elif args[1] == bstack11ll11_opy_ (u"࠭ࡲࡰࡤࡲࡸ഻ࠬ"):
      bstack11ll1l11l_opy_ = bstack11ll11_opy_ (u"ࠧࡳࡱࡥࡳࡹ഼࠭")
      args = args[2:]
    elif args[1] == bstack11ll11_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧഽ"):
      bstack11ll1l11l_opy_ = bstack11ll11_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨാ")
      args = args[2:]
    elif args[1] == bstack11ll11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫി"):
      bstack11ll1l11l_opy_ = bstack11ll11_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬീ")
      args = args[2:]
    elif args[1] == bstack11ll11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬു"):
      bstack11ll1l11l_opy_ = bstack11ll11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ൂ")
      args = args[2:]
    elif args[1] == bstack11ll11_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧൃ"):
      bstack11ll1l11l_opy_ = bstack11ll11_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨൄ")
      args = args[2:]
    else:
      if not bstack11ll11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ൅") in CONFIG or str(CONFIG[bstack11ll11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭െ")]).lower() in [bstack11ll11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫേ"), bstack11ll11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠸࠭ൈ")]:
        bstack11ll1l11l_opy_ = bstack11ll11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭൉")
        args = args[1:]
      elif str(CONFIG[bstack11ll11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪൊ")]).lower() == bstack11ll11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧോ"):
        bstack11ll1l11l_opy_ = bstack11ll11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨൌ")
        args = args[1:]
      elif str(CONFIG[bstack11ll11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ്࠭")]).lower() == bstack11ll11_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪൎ"):
        bstack11ll1l11l_opy_ = bstack11ll11_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ൏")
        args = args[1:]
      elif str(CONFIG[bstack11ll11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ൐")]).lower() == bstack11ll11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ൑"):
        bstack11ll1l11l_opy_ = bstack11ll11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ൒")
        args = args[1:]
      elif str(CONFIG[bstack11ll11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ൓")]).lower() == bstack11ll11_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪൔ"):
        bstack11ll1l11l_opy_ = bstack11ll11_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫൕ")
        args = args[1:]
      else:
        os.environ[bstack11ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧൖ")] = bstack11ll1l11l_opy_
        bstack1ll11l111_opy_(bstack11ll1l1111_opy_)
  os.environ[bstack11ll11_opy_ (u"࠭ࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࡡࡘࡗࡊࡊࠧൗ")] = bstack11ll1l11l_opy_
  bstack11llll11l_opy_ = bstack11ll1l11l_opy_
  if cli.is_enabled(CONFIG):
    try:
      bstack1l1lll1l1_opy_ = bstack1lllll1l1_opy_[bstack11ll11_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࠭ࡃࡆࡇࠫ൘")] if bstack11ll1l11l_opy_ == bstack11ll11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ൙") and bstack111ll11l_opy_() else bstack11ll1l11l_opy_
      bstack11111l11l_opy_.invoke(bstack11l11l1l_opy_.bstack1l11l11lll_opy_, bstack11l11ll1_opy_(
        sdk_version=__version__,
        path_config=bstack1lll1l1ll1_opy_(),
        path_project=os.getcwd(),
        test_framework=bstack1l1lll1l1_opy_,
        frameworks=[bstack1l1lll1l1_opy_],
        framework_versions={
          bstack1l1lll1l1_opy_: bstack1l1111l1ll_opy_(bstack11ll11_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨ൚") if bstack11ll1l11l_opy_ in [bstack11ll11_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ൛"), bstack11ll11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ൜"), bstack11ll11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭൝")] else bstack11ll1l11l_opy_)
        },
        bs_config=CONFIG
      ))
      if cli.config.get(bstack11ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣ൞"), None):
        CONFIG[bstack11ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤൟ")] = cli.config.get(bstack11ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠥൠ"), None)
    except Exception as e:
      bstack11111l11l_opy_.invoke(bstack11l11l1l_opy_.bstack11llllll1l_opy_, e.__traceback__, 1)
    if bstack1ll1lllll1_opy_:
      CONFIG[bstack11ll11_opy_ (u"ࠤࡤࡴࡵࠨൡ")] = cli.config[bstack11ll11_opy_ (u"ࠥࡥࡵࡶࠢൢ")]
      logger.info(bstack1l111ll1l1_opy_.format(CONFIG[bstack11ll11_opy_ (u"ࠫࡦࡶࡰࠨൣ")]))
  else:
    bstack11111l11l_opy_.clear()
  global bstack1l1l1ll111_opy_
  global bstack1ll11ll1l1_opy_
  if bstack1llll1llll_opy_:
    try:
      bstack1ll1lll1ll_opy_ = datetime.datetime.now()
      os.environ[bstack11ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ൤")] = bstack11ll1l11l_opy_
      bstack1ll111l111_opy_(bstack1l1l11111_opy_, CONFIG)
      cli.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠨࡨࡵࡶࡳ࠾ࡸࡪ࡫ࡠࡶࡨࡷࡹࡥࡡࡵࡶࡨࡱࡵࡺࡥࡥࠤ൥"), datetime.datetime.now() - bstack1ll1lll1ll_opy_)
    except Exception as e:
      logger.debug(bstack11l111ll_opy_.format(str(e)))
  global bstack1l1llll1_opy_
  global bstack11llll1l_opy_
  global bstack11l1ll1111_opy_
  global bstack1111lll1l_opy_
  global bstack1ll11l11l1_opy_
  global bstack11l1ll1l1l_opy_
  global bstack1ll1l1lll1_opy_
  global bstack111ll1l1_opy_
  global bstack11ll1111_opy_
  global bstack11l1l1ll1l_opy_
  global bstack11l11l1l1l_opy_
  global bstack1ll1111ll1_opy_
  global bstack11l11111l_opy_
  global bstack11lll1l1l_opy_
  global bstack11lllllll_opy_
  global bstack11ll11111l_opy_
  global bstack1lll11ll1_opy_
  global bstack11l111l1_opy_
  global bstack1l1111l11_opy_
  global bstack1ll111ll1_opy_
  global bstack1ll11ll11_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l1llll1_opy_ = webdriver.Remote.__init__
    bstack11llll1l_opy_ = WebDriver.quit
    bstack1ll1111ll1_opy_ = WebDriver.close
    bstack11lllllll_opy_ = WebDriver.get
    bstack1ll11ll11_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1l1l1ll111_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack1ll1111l_opy_
    bstack1ll11ll1l1_opy_ = bstack1ll1111l_opy_()
  except Exception as e:
    pass
  try:
    global bstack1l11l1llll_opy_
    from QWeb.keywords import browser
    bstack1l11l1llll_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1ll111l11l_opy_(CONFIG) and bstack1111llll1_opy_():
    if bstack1lll1ll1_opy_() < version.parse(bstack1lll111ll_opy_):
      logger.error(bstack11ll1l11ll_opy_.format(bstack1lll1ll1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack11ll11_opy_ (u"ࠧࡠࡩࡨࡸࡤࡶࡲࡰࡺࡼࡣࡺࡸ࡬ࠨ൦")) and callable(getattr(RemoteConnection, bstack11ll11_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩ൧"))):
          RemoteConnection._get_proxy_url = bstack11l11l11_opy_
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          ClientConfig.get_proxy_url = bstack11l11l11_opy_
      except Exception as e:
        logger.error(bstack11ll1111l_opy_.format(str(e)))
  if not CONFIG.get(bstack11ll11_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫ൨"), False) and not bstack1llll1llll_opy_:
    logger.info(bstack1l111lllll_opy_)
  if not cli.is_enabled(CONFIG):
    if bstack11ll11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ൩") in CONFIG and str(CONFIG[bstack11ll11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ൪")]).lower() != bstack11ll11_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ൫"):
      bstack1l1l1lll1l_opy_()
    elif bstack11ll1l11l_opy_ != bstack11ll11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭൬") or (bstack11ll1l11l_opy_ == bstack11ll11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ൭") and not bstack1llll1llll_opy_):
      bstack11ll111ll_opy_()
  if (bstack11ll1l11l_opy_ in [bstack11ll11_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ൮"), bstack11ll11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ൯"), bstack11ll11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ൰")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack11l1l11111_opy_
        bstack11l1ll1l1l_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack11l1111lll_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1ll11l11l1_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1l11111l11_opy_ + str(e))
    except Exception as e:
      bstack1lll11l1l1_opy_(e, bstack11l1111lll_opy_)
    if bstack11ll1l11l_opy_ != bstack11ll11_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ൱"):
      bstack1llll1lll_opy_()
    bstack11l1ll1111_opy_ = Output.start_test
    bstack1111lll1l_opy_ = Output.end_test
    bstack1ll1l1lll1_opy_ = TestStatus.__init__
    bstack11ll1111_opy_ = pabot._run
    bstack11l1l1ll1l_opy_ = QueueItem.__init__
    bstack11l11l1l1l_opy_ = pabot._create_command_for_execution
    bstack1l1111l11_opy_ = pabot._report_results
  if bstack11ll1l11l_opy_ == bstack11ll11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ൲"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1lll11l1l1_opy_(e, bstack11l1l1l111_opy_)
    bstack11l11111l_opy_ = Runner.run_hook
    bstack11lll1l1l_opy_ = Step.run
  if bstack11ll1l11l_opy_ == bstack11ll11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭൳"):
    try:
      from _pytest.config import Config
      bstack1lll11ll1_opy_ = Config.getoption
      from _pytest import runner
      bstack11l111l1_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack11ll1l1l1l_opy_)
    try:
      from pytest_bdd import reporting
      bstack1ll111ll1_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack11ll11_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨ൴"))
  try:
    framework_name = bstack11ll11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ൵") if bstack11ll1l11l_opy_ in [bstack11ll11_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ൶"), bstack11ll11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ൷"), bstack11ll11_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ൸")] else bstack1l11llll11_opy_(bstack11ll1l11l_opy_)
    bstack1l1llll11l_opy_ = {
      bstack11ll11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪ࠭൹"): bstack11ll11_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨൺ") if bstack11ll1l11l_opy_ == bstack11ll11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧൻ") and bstack111ll11l_opy_() else framework_name,
      bstack11ll11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬർ"): bstack1l1111l1ll_opy_(framework_name),
      bstack11ll11_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧൽ"): __version__,
      bstack11ll11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡵࡴࡧࡧࠫൾ"): bstack11ll1l11l_opy_
    }
    if bstack11ll1l11l_opy_ in bstack1ll1l111ll_opy_ + bstack1111l11ll_opy_:
      if bstack11l11lll11_opy_.bstack1l11l11l11_opy_(CONFIG):
        if bstack11ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫൿ") in CONFIG:
          os.environ[bstack11ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭඀")] = os.getenv(bstack11ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧඁ"), json.dumps(CONFIG[bstack11ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧං")]))
          CONFIG[bstack11ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨඃ")].pop(bstack11ll11_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ඄"), None)
          CONFIG[bstack11ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪඅ")].pop(bstack11ll11_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩආ"), None)
        bstack1l1llll11l_opy_[bstack11ll11_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬඇ")] = {
          bstack11ll11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫඈ"): bstack11ll11_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩඉ"),
          bstack11ll11_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩඊ"): str(bstack1lll1ll1_opy_())
        }
    if bstack11ll1l11l_opy_ not in [bstack11ll11_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪඋ")] and not cli.is_running():
      bstack1ll1l11111_opy_, bstack1ll111lll_opy_ = bstack1l1l1l1ll_opy_.launch(CONFIG, bstack1l1llll11l_opy_)
      if bstack1ll111lll_opy_.get(bstack11ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪඌ")) is not None and bstack11l11lll11_opy_.bstack1l1ll111ll_opy_(CONFIG) is None:
        value = bstack1ll111lll_opy_[bstack11ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫඍ")].get(bstack11ll11_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ඎ"))
        if value is not None:
            CONFIG[bstack11ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ඏ")] = value
        else:
          logger.debug(bstack11ll11_opy_ (u"ࠢࡏࡱࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡨࡦࡺࡡࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡶࡪࡹࡰࡰࡰࡶࡩࠧඐ"))
  except Exception as e:
    logger.debug(bstack1l11lll11_opy_.format(bstack11ll11_opy_ (u"ࠨࡖࡨࡷࡹࡎࡵࡣࠩඑ"), str(e)))
  if bstack11ll1l11l_opy_ == bstack11ll11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩඒ"):
    bstack111lll1ll_opy_ = True
    if bstack1llll1llll_opy_ and bstack111l1lll1_opy_:
      bstack11llllll11_opy_ = CONFIG.get(bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧඓ"), {}).get(bstack11ll11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ඔ"))
      bstack1ll1ll111l_opy_(bstack1l11ll11l_opy_)
    elif bstack1llll1llll_opy_:
      bstack11llllll11_opy_ = CONFIG.get(bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩඕ"), {}).get(bstack11ll11_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨඖ"))
      global bstack1l11ll1ll1_opy_
      try:
        if bstack11l1l1111l_opy_(bstack1llll1llll_opy_[bstack11ll11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ඗")]) and multiprocessing.current_process().name == bstack11ll11_opy_ (u"ࠨ࠲ࠪ඘"):
          bstack1llll1llll_opy_[bstack11ll11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ඙")].remove(bstack11ll11_opy_ (u"ࠪ࠱ࡲ࠭ක"))
          bstack1llll1llll_opy_[bstack11ll11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧඛ")].remove(bstack11ll11_opy_ (u"ࠬࡶࡤࡣࠩග"))
          bstack1llll1llll_opy_[bstack11ll11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩඝ")] = bstack1llll1llll_opy_[bstack11ll11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪඞ")][0]
          with open(bstack1llll1llll_opy_[bstack11ll11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫඟ")], bstack11ll11_opy_ (u"ࠩࡵࠫච")) as f:
            bstack1lll1111ll_opy_ = f.read()
          bstack11l1111l1l_opy_ = bstack11ll11_opy_ (u"ࠥࠦࠧ࡬ࡲࡰ࡯ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡨࡰࠦࡩ࡮ࡲࡲࡶࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦ࠽ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪ࠮ࡻࡾࠫ࠾ࠤ࡫ࡸ࡯࡮ࠢࡳࡨࡧࠦࡩ࡮ࡲࡲࡶࡹࠦࡐࡥࡤ࠾ࠤࡴ࡭࡟ࡥࡤࠣࡁࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡦࡨࡪࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠩࡵࡨࡰ࡫࠲ࠠࡢࡴࡪ࠰ࠥࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠡ࠿ࠣ࠴࠮ࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺࡲࡺ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡥࡷ࡭ࠠ࠾ࠢࡶࡸࡷ࠮ࡩ࡯ࡶࠫࡥࡷ࡭ࠩࠬ࠳࠳࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡩࡽࡩࡥࡱࡶࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡡࡴࠢࡨ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡶࡡࡴࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡱࡪࡣࡩࡨࠨࡴࡧ࡯ࡪ࠱ࡧࡲࡨ࠮ࡷࡩࡲࡶ࡯ࡳࡣࡵࡽ࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡓࡨࡧ࠴ࡤࡰࡡࡥࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮ࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣࠪࠬ࠲ࡸ࡫ࡴࡠࡶࡵࡥࡨ࡫ࠨࠪ࡞ࡱࠦࠧࠨඡ").format(str(bstack1llll1llll_opy_))
          bstack1111l1lll_opy_ = bstack11l1111l1l_opy_ + bstack1lll1111ll_opy_
          bstack11lll1l111_opy_ = bstack1llll1llll_opy_[bstack11ll11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧජ")] + bstack11ll11_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥࡴࡦ࡯ࡳ࠲ࡵࡿࠧඣ")
          with open(bstack11lll1l111_opy_, bstack11ll11_opy_ (u"࠭ࡷࠨඤ")):
            pass
          with open(bstack11lll1l111_opy_, bstack11ll11_opy_ (u"ࠢࡸ࠭ࠥඥ")) as f:
            f.write(bstack1111l1lll_opy_)
          import subprocess
          bstack11l111l1l1_opy_ = subprocess.run([bstack11ll11_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࠣඦ"), bstack11lll1l111_opy_])
          if os.path.exists(bstack11lll1l111_opy_):
            os.unlink(bstack11lll1l111_opy_)
          os._exit(bstack11l111l1l1_opy_.returncode)
        else:
          if bstack11l1l1111l_opy_(bstack1llll1llll_opy_[bstack11ll11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬට")]):
            bstack1llll1llll_opy_[bstack11ll11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ඨ")].remove(bstack11ll11_opy_ (u"ࠫ࠲ࡳࠧඩ"))
            bstack1llll1llll_opy_[bstack11ll11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨඪ")].remove(bstack11ll11_opy_ (u"࠭ࡰࡥࡤࠪණ"))
            bstack1llll1llll_opy_[bstack11ll11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪඬ")] = bstack1llll1llll_opy_[bstack11ll11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫත")][0]
          bstack1ll1ll111l_opy_(bstack1l11ll11l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1llll1llll_opy_[bstack11ll11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬථ")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack11ll11_opy_ (u"ࠪࡣࡤࡴࡡ࡮ࡧࡢࡣࠬද")] = bstack11ll11_opy_ (u"ࠫࡤࡥ࡭ࡢ࡫ࡱࡣࡤ࠭ධ")
          mod_globals[bstack11ll11_opy_ (u"ࠬࡥ࡟ࡧ࡫࡯ࡩࡤࡥࠧන")] = os.path.abspath(bstack1llll1llll_opy_[bstack11ll11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ඲")])
          exec(open(bstack1llll1llll_opy_[bstack11ll11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪඳ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack11ll11_opy_ (u"ࠨࡅࡤࡹ࡬࡮ࡴࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠨප").format(str(e)))
          for driver in bstack1l11ll1ll1_opy_:
            bstack1ll11l11_opy_.append({
              bstack11ll11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧඵ"): bstack1llll1llll_opy_[bstack11ll11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭බ")],
              bstack11ll11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪභ"): str(e),
              bstack11ll11_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫම"): multiprocessing.current_process().name
            })
            bstack11l1l1l11l_opy_(driver, bstack11ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ඹ"), bstack11ll11_opy_ (u"ࠢࡔࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥය") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1l11ll1ll1_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1ll1lllll1_opy_, CONFIG, logger)
      bstack111llll11_opy_()
      bstack1l111l11l_opy_()
      percy.bstack1ll11lll_opy_()
      bstack1ll11ll1l_opy_ = {
        bstack11ll11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫර"): args[0],
        bstack11ll11_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩ඼"): CONFIG,
        bstack11ll11_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫල"): bstack11lll111ll_opy_,
        bstack11ll11_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭඾"): bstack1ll1lllll1_opy_
      }
      if bstack11ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ඿") in CONFIG:
        bstack11ll11ll1_opy_ = bstack1ll1lll11_opy_(args, logger, CONFIG, bstack11ll11l1_opy_, bstack111l1l111_opy_)
        bstack11l11l1111_opy_ = bstack11ll11ll1_opy_.bstack1ll1111ll_opy_(run_on_browserstack, bstack1ll11ll1l_opy_, bstack11l1l1111l_opy_(args))
      else:
        if bstack11l1l1111l_opy_(args):
          bstack1ll11ll1l_opy_[bstack11ll11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩව")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1ll11ll1l_opy_,))
          test.start()
          test.join()
        else:
          bstack1ll1ll111l_opy_(bstack1l11ll11l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack11ll11_opy_ (u"ࠧࡠࡡࡱࡥࡲ࡫࡟ࡠࠩශ")] = bstack11ll11_opy_ (u"ࠨࡡࡢࡱࡦ࡯࡮ࡠࡡࠪෂ")
          mod_globals[bstack11ll11_opy_ (u"ࠩࡢࡣ࡫࡯࡬ࡦࡡࡢࠫස")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack11ll1l11l_opy_ == bstack11ll11_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩහ") or bstack11ll1l11l_opy_ == bstack11ll11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪළ"):
    percy.init(bstack1ll1lllll1_opy_, CONFIG, logger)
    percy.bstack1ll11lll_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1lll11l1l1_opy_(e, bstack11l1111lll_opy_)
    bstack111llll11_opy_()
    bstack1ll1ll111l_opy_(bstack1llllll11l_opy_)
    if bstack11ll11l1_opy_:
      bstack1l11l111_opy_(bstack1llllll11l_opy_, args)
      if bstack11ll11_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪෆ") in args:
        i = args.index(bstack11ll11_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ෇"))
        args.pop(i)
        args.pop(i)
      if bstack11ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ෈") not in CONFIG:
        CONFIG[bstack11ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ෉")] = [{}]
        bstack111l1l111_opy_ = 1
      if bstack1l111llll_opy_ == 0:
        bstack1l111llll_opy_ = 1
      args.insert(0, str(bstack1l111llll_opy_))
      args.insert(0, str(bstack11ll11_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹ්ࠧ")))
    if bstack1l1l1l1ll_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1llll1l11_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack11111l11_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack11ll11_opy_ (u"ࠥࡖࡔࡈࡏࡕࡡࡒࡔ࡙ࡏࡏࡏࡕࠥ෋"),
        ).parse_args(bstack1llll1l11_opy_)
        bstack1ll1111111_opy_ = args.index(bstack1llll1l11_opy_[0]) if len(bstack1llll1l11_opy_) > 0 else len(args)
        args.insert(bstack1ll1111111_opy_, str(bstack11ll11_opy_ (u"ࠫ࠲࠳࡬ࡪࡵࡷࡩࡳ࡫ࡲࠨ෌")))
        args.insert(bstack1ll1111111_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11ll11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡸ࡯ࡣࡱࡷࡣࡱ࡯ࡳࡵࡧࡱࡩࡷ࠴ࡰࡺࠩ෍"))))
        if bstack111l11l1l_opy_.bstack1llll1ll11_opy_(CONFIG):
          args.insert(bstack1ll1111111_opy_, str(bstack11ll11_opy_ (u"࠭࠭࠮࡮࡬ࡷࡹ࡫࡮ࡦࡴࠪ෎")))
          args.insert(bstack1ll1111111_opy_ + 1, str(bstack11ll11_opy_ (u"ࠧࡓࡧࡷࡶࡾࡌࡡࡪ࡮ࡨࡨ࠿ࢁࡽࠨා").format(bstack111l11l1l_opy_.bstack11ll1llll_opy_(CONFIG))))
        if bstack1l111ll1l_opy_(os.environ.get(bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓ࠭ැ"))) and str(os.environ.get(bstack11ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭ෑ"), bstack11ll11_opy_ (u"ࠪࡲࡺࡲ࡬ࠨි"))) != bstack11ll11_opy_ (u"ࠫࡳࡻ࡬࡭ࠩී"):
          for bstack1l11l1ll1_opy_ in bstack11111l11_opy_:
            args.remove(bstack1l11l1ll1_opy_)
          test_files = os.environ.get(bstack11ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠩු")).split(bstack11ll11_opy_ (u"࠭ࠬࠨ෕"))
          for bstack11111ll1_opy_ in test_files:
            args.append(bstack11111ll1_opy_)
      except Exception as e:
        logger.error(bstack11ll11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡧࡴࡵࡣࡦ࡬࡮ࡴࡧࠡ࡮࡬ࡷࡹ࡫࡮ࡦࡴࠣࡪࡴࡸࠠࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࠡࡇࡵࡶࡴࡸࠠ࠮ࠢࠥූ").format(e))
    pabot.main(args)
  elif bstack11ll1l11l_opy_ == bstack11ll11_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ෗"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1lll11l1l1_opy_(e, bstack11l1111lll_opy_)
    for a in args:
      if bstack11ll11_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘࠨෘ") in a:
        bstack11llllllll_opy_ = int(a.split(bstack11ll11_opy_ (u"ࠪ࠾ࠬෙ"))[1])
      if bstack11ll11_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨේ") in a:
        bstack11llllll11_opy_ = str(a.split(bstack11ll11_opy_ (u"ࠬࡀࠧෛ"))[1])
      if bstack11ll11_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘ࠭ො") in a:
        bstack11l1111l11_opy_ = str(a.split(bstack11ll11_opy_ (u"ࠧ࠻ࠩෝ"))[1])
    bstack1llll1ll1_opy_ = None
    if bstack11ll11_opy_ (u"ࠨ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠧෞ") in args:
      i = args.index(bstack11ll11_opy_ (u"ࠩ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠨෟ"))
      args.pop(i)
      bstack1llll1ll1_opy_ = args.pop(i)
    if bstack1llll1ll1_opy_ is not None:
      global bstack1ll1l111l1_opy_
      bstack1ll1l111l1_opy_ = bstack1llll1ll1_opy_
    bstack1ll1ll111l_opy_(bstack1llllll11l_opy_)
    run_cli(args)
    if bstack11ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺࠧ෠") in multiprocessing.current_process().__dict__.keys():
      for bstack1l111ll111_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1ll11l11_opy_.append(bstack1l111ll111_opy_)
  elif bstack11ll1l11l_opy_ == bstack11ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ෡"):
    bstack1ll1lll11l_opy_ = bstack1l111l1l_opy_(args, logger, CONFIG, bstack11ll11l1_opy_)
    bstack1ll1lll11l_opy_.bstack11l11llll1_opy_()
    bstack111llll11_opy_()
    bstack11l111ll1_opy_ = True
    bstack11l111111l_opy_ = bstack1ll1lll11l_opy_.bstack11111l1l1_opy_()
    bstack1ll1lll11l_opy_.bstack1l111l1l1_opy_()
    bstack1ll1lll11l_opy_.bstack1ll11ll1l_opy_(bstack1llllll1ll_opy_)
    bstack11l111lll_opy_(bstack11ll1l11l_opy_, CONFIG, bstack1ll1lll11l_opy_.bstack11lll1l1_opy_())
    bstack1lll1l11_opy_ = bstack1ll1lll11l_opy_.bstack1ll1111ll_opy_(bstack1l1lll111l_opy_, {
      bstack11ll11_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭෢"): bstack11lll111ll_opy_,
      bstack11ll11_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ෣"): bstack1ll1lllll1_opy_,
      bstack11ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪ෤"): bstack11ll11l1_opy_
    })
    try:
      bstack11l111l1l_opy_, bstack111l11lll_opy_ = map(list, zip(*bstack1lll1l11_opy_))
      bstack1l1l1lll11_opy_ = bstack11l111l1l_opy_[0]
      for status_code in bstack111l11lll_opy_:
        if status_code != 0:
          bstack11ll1l1l1_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack11ll11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡧࡶࡦࠢࡨࡶࡷࡵࡲࡴࠢࡤࡲࡩࠦࡳࡵࡣࡷࡹࡸࠦࡣࡰࡦࡨ࠲ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࠼ࠣࡿࢂࠨ෥").format(str(e)))
  elif bstack11ll1l11l_opy_ == bstack11ll11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ෦"):
    try:
      from behave.__main__ import main as bstack111l11111_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1lll11l1l1_opy_(e, bstack11l1l1l111_opy_)
    bstack111llll11_opy_()
    bstack11l111ll1_opy_ = True
    bstack11lll1111l_opy_ = 1
    if bstack11ll11_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ෧") in CONFIG:
      bstack11lll1111l_opy_ = CONFIG[bstack11ll11_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ෨")]
    if bstack11ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ෩") in CONFIG:
      bstack1l1l1l11_opy_ = int(bstack11lll1111l_opy_) * int(len(CONFIG[bstack11ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ෪")]))
    else:
      bstack1l1l1l11_opy_ = int(bstack11lll1111l_opy_)
    config = Configuration(args)
    bstack11ll1ll11l_opy_ = config.paths
    if len(bstack11ll1ll11l_opy_) == 0:
      import glob
      pattern = bstack11ll11_opy_ (u"ࠧࠫࠬ࠲࠮࠳࡬ࡥࡢࡶࡸࡶࡪ࠭෫")
      bstack1llll1l1l1_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1llll1l1l1_opy_)
      config = Configuration(args)
      bstack11ll1ll11l_opy_ = config.paths
    bstack11ll1l11_opy_ = [os.path.normpath(item) for item in bstack11ll1ll11l_opy_]
    bstack1l1ll1l1_opy_ = [os.path.normpath(item) for item in args]
    bstack11ll1lll1l_opy_ = [item for item in bstack1l1ll1l1_opy_ if item not in bstack11ll1l11_opy_]
    import platform as pf
    if pf.system().lower() == bstack11ll11_opy_ (u"ࠨࡹ࡬ࡲࡩࡵࡷࡴࠩ෬"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack11ll1l11_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l1lll1ll_opy_)))
                    for bstack1l1lll1ll_opy_ in bstack11ll1l11_opy_]
    bstack11l111l1ll_opy_ = []
    for spec in bstack11ll1l11_opy_:
      bstack11l111l11l_opy_ = []
      bstack11l111l11l_opy_ += bstack11ll1lll1l_opy_
      bstack11l111l11l_opy_.append(spec)
      bstack11l111l1ll_opy_.append(bstack11l111l11l_opy_)
    execution_items = []
    for bstack11l111l11l_opy_ in bstack11l111l1ll_opy_:
      if bstack11ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ෭") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack11ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭෮")]):
          item = {}
          item[bstack11ll11_opy_ (u"ࠫࡦࡸࡧࠨ෯")] = bstack11ll11_opy_ (u"ࠬࠦࠧ෰").join(bstack11l111l11l_opy_)
          item[bstack11ll11_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ෱")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack11ll11_opy_ (u"ࠧࡢࡴࡪࠫෲ")] = bstack11ll11_opy_ (u"ࠨࠢࠪෳ").join(bstack11l111l11l_opy_)
        item[bstack11ll11_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ෴")] = 0
        execution_items.append(item)
    bstack1111l1ll_opy_ = bstack1l1l1l11ll_opy_(execution_items, bstack1l1l1l11_opy_)
    for execution_item in bstack1111l1ll_opy_:
      bstack11ll1l1ll_opy_ = []
      for item in execution_item:
        bstack11ll1l1ll_opy_.append(bstack1l1l11l1l_opy_(name=str(item[bstack11ll11_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ෵")]),
                                             target=bstack11111ll1l_opy_,
                                             args=(item[bstack11ll11_opy_ (u"ࠫࡦࡸࡧࠨ෶")],)))
      for t in bstack11ll1l1ll_opy_:
        t.start()
      for t in bstack11ll1l1ll_opy_:
        t.join()
  else:
    bstack1ll11l111_opy_(bstack11ll1l1111_opy_)
  if not bstack1llll1llll_opy_:
    bstack1l1l1111l_opy_()
    if(bstack11ll1l11l_opy_ in [bstack11ll11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ෷"), bstack11ll11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭෸")]):
      bstack1ll1l1111l_opy_()
  bstack1111l1ll1_opy_.bstack11ll1l1ll1_opy_()
def browserstack_initialize(bstack11l11l1l11_opy_=None):
  logger.info(bstack11ll11_opy_ (u"ࠧࡓࡷࡱࡲ࡮ࡴࡧࠡࡕࡇࡏࠥࡽࡩࡵࡪࠣࡥࡷ࡭ࡳ࠻ࠢࠪ෹") + str(bstack11l11l1l11_opy_))
  run_on_browserstack(bstack11l11l1l11_opy_, None, True)
@measure(event_name=EVENTS.bstack11l1l111ll_opy_, stage=STAGE.bstack1lll11llll_opy_, bstack1111llll_opy_=bstack11ll11lll_opy_)
def bstack1l1l1111l_opy_():
  global CONFIG
  global bstack11llll11l_opy_
  global bstack11ll1l1l1_opy_
  global bstack111l1lll_opy_
  global bstack1l1ll1llll_opy_
  bstack11111lll1_opy_.bstack1lllll1111_opy_()
  if cli.is_running():
    bstack11111l11l_opy_.invoke(bstack11l11l1l_opy_.bstack1l11ll1l_opy_)
  if bstack11llll11l_opy_ == bstack11ll11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ෺"):
    if not cli.is_enabled(CONFIG):
      bstack1l1l1l1ll_opy_.stop()
  else:
    bstack1l1l1l1ll_opy_.stop()
  if not cli.is_enabled(CONFIG):
    bstack11l1ll11_opy_.bstack1l1l11ll_opy_()
  if bstack11ll11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭෻") in CONFIG and str(CONFIG[bstack11ll11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ෼")]).lower() != bstack11ll11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪ෽"):
    hashed_id, bstack1lll1l1l_opy_ = bstack11l11lllll_opy_()
  else:
    hashed_id, bstack1lll1l1l_opy_ = get_build_link()
  bstack11ll11l1l1_opy_(hashed_id)
  logger.info(bstack11ll11_opy_ (u"࡙ࠬࡄࡌࠢࡵࡹࡳࠦࡥ࡯ࡦࡨࡨࠥ࡬࡯ࡳࠢ࡬ࡨ࠿࠭෾") + bstack1l1ll1llll_opy_.get_property(bstack11ll11_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨ෿"), bstack11ll11_opy_ (u"ࠧࠨ฀")) + bstack11ll11_opy_ (u"ࠨ࠮ࠣࡸࡪࡹࡴࡩࡷࡥࠤ࡮ࡪ࠺ࠡࠩก") + os.getenv(bstack11ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧข"), bstack11ll11_opy_ (u"ࠪࠫฃ")))
  if hashed_id is not None and bstack1ll11ll111_opy_() != -1:
    sessions = bstack1l1l11llll_opy_(hashed_id)
    bstack1l1l1111l1_opy_(sessions, bstack1lll1l1l_opy_)
  if bstack11llll11l_opy_ == bstack11ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫค") and bstack11ll1l1l1_opy_ != 0:
    sys.exit(bstack11ll1l1l1_opy_)
  if bstack11llll11l_opy_ == bstack11ll11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬฅ") and bstack111l1lll_opy_ != 0:
    sys.exit(bstack111l1lll_opy_)
def bstack11ll11l1l1_opy_(new_id):
    global bstack1l11l1l11_opy_
    bstack1l11l1l11_opy_ = new_id
def bstack1l11llll11_opy_(bstack1l1ll1l1l_opy_):
  if bstack1l1ll1l1l_opy_:
    return bstack1l1ll1l1l_opy_.capitalize()
  else:
    return bstack11ll11_opy_ (u"࠭ࠧฆ")
@measure(event_name=EVENTS.bstack1l11ll11_opy_, stage=STAGE.bstack1lll11llll_opy_, bstack1111llll_opy_=bstack11ll11lll_opy_)
def bstack11l1l1lll_opy_(bstack11l11ll1ll_opy_):
  if bstack11ll11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬง") in bstack11l11ll1ll_opy_ and bstack11l11ll1ll_opy_[bstack11ll11_opy_ (u"ࠨࡰࡤࡱࡪ࠭จ")] != bstack11ll11_opy_ (u"ࠩࠪฉ"):
    return bstack11l11ll1ll_opy_[bstack11ll11_opy_ (u"ࠪࡲࡦࡳࡥࠨช")]
  else:
    bstack1111llll_opy_ = bstack11ll11_opy_ (u"ࠦࠧซ")
    if bstack11ll11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬฌ") in bstack11l11ll1ll_opy_ and bstack11l11ll1ll_opy_[bstack11ll11_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ญ")] != None:
      bstack1111llll_opy_ += bstack11l11ll1ll_opy_[bstack11ll11_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧฎ")] + bstack11ll11_opy_ (u"ࠣ࠮ࠣࠦฏ")
      if bstack11l11ll1ll_opy_[bstack11ll11_opy_ (u"ࠩࡲࡷࠬฐ")] == bstack11ll11_opy_ (u"ࠥ࡭ࡴࡹࠢฑ"):
        bstack1111llll_opy_ += bstack11ll11_opy_ (u"ࠦ࡮ࡕࡓࠡࠤฒ")
      bstack1111llll_opy_ += (bstack11l11ll1ll_opy_[bstack11ll11_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩณ")] or bstack11ll11_opy_ (u"࠭ࠧด"))
      return bstack1111llll_opy_
    else:
      bstack1111llll_opy_ += bstack1l11llll11_opy_(bstack11l11ll1ll_opy_[bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨต")]) + bstack11ll11_opy_ (u"ࠣࠢࠥถ") + (
              bstack11l11ll1ll_opy_[bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫท")] or bstack11ll11_opy_ (u"ࠪࠫธ")) + bstack11ll11_opy_ (u"ࠦ࠱ࠦࠢน")
      if bstack11l11ll1ll_opy_[bstack11ll11_opy_ (u"ࠬࡵࡳࠨบ")] == bstack11ll11_opy_ (u"ࠨࡗࡪࡰࡧࡳࡼࡹࠢป"):
        bstack1111llll_opy_ += bstack11ll11_opy_ (u"ࠢࡘ࡫ࡱࠤࠧผ")
      bstack1111llll_opy_ += bstack11l11ll1ll_opy_[bstack11ll11_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬฝ")] or bstack11ll11_opy_ (u"ࠩࠪพ")
      return bstack1111llll_opy_
@measure(event_name=EVENTS.bstack1l1ll1111l_opy_, stage=STAGE.bstack1lll11llll_opy_, bstack1111llll_opy_=bstack11ll11lll_opy_)
def bstack1l11111l1_opy_(bstack1ll11lll1_opy_):
  if bstack1ll11lll1_opy_ == bstack11ll11_opy_ (u"ࠥࡨࡴࡴࡥࠣฟ"):
    return bstack11ll11_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡧࡳࡧࡨࡲࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡧࡳࡧࡨࡲࠧࡄࡃࡰ࡯ࡳࡰࡪࡺࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧภ")
  elif bstack1ll11lll1_opy_ == bstack11ll11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧม"):
    return bstack11ll11_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡴࡨࡨࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡲࡦࡦࠥࡂࡋࡧࡩ࡭ࡧࡧࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩย")
  elif bstack1ll11lll1_opy_ == bstack11ll11_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢร"):
    return bstack11ll11_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽࡫ࡷ࡫ࡥ࡯࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥ࡫ࡷ࡫ࡥ࡯ࠤࡁࡔࡦࡹࡳࡦࡦ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨฤ")
  elif bstack1ll11lll1_opy_ == bstack11ll11_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣล"):
    return bstack11ll11_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡸࡥࡥ࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡶࡪࡪࠢ࠿ࡇࡵࡶࡴࡸ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬฦ")
  elif bstack1ll11lll1_opy_ == bstack11ll11_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࠧว"):
    return bstack11ll11_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࠤࡧࡨࡥ࠸࠸࠶࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࠦࡩࡪࡧ࠳࠳࠸ࠥࡂ࡙࡯࡭ࡦࡱࡸࡸࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪศ")
  elif bstack1ll11lll1_opy_ == bstack11ll11_opy_ (u"ࠨࡲࡶࡰࡱ࡭ࡳ࡭ࠢษ"):
    return bstack11ll11_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡥࡰࡦࡩ࡫࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡥࡰࡦࡩ࡫ࠣࡀࡕࡹࡳࡴࡩ࡯ࡩ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨส")
  else:
    return bstack11ll11_opy_ (u"ࠨ࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡧࡲࡡࡤ࡭࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡧࡲࡡࡤ࡭ࠥࡂࠬห") + bstack1l11llll11_opy_(
      bstack1ll11lll1_opy_) + bstack11ll11_opy_ (u"ࠩ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨฬ")
def bstack11lll11l11_opy_(session):
  return bstack11ll11_opy_ (u"ࠪࡀࡹࡸࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡳࡱࡺࠦࡃࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠠࡴࡧࡶࡷ࡮ࡵ࡮࠮ࡰࡤࡱࡪࠨ࠾࠽ࡣࠣ࡬ࡷ࡫ࡦ࠾ࠤࡾࢁࠧࠦࡴࡢࡴࡪࡩࡹࡃࠢࡠࡤ࡯ࡥࡳࡱࠢ࠿ࡽࢀࡀ࠴ࡧ࠾࠽࠱ࡷࡨࡃࢁࡽࡼࡿ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁ࠵ࡴࡳࡀࠪอ").format(
    session[bstack11ll11_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦࡣࡺࡸ࡬ࠨฮ")], bstack11l1l1lll_opy_(session), bstack1l11111l1_opy_(session[bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡸࡺࡡࡵࡷࡶࠫฯ")]),
    bstack1l11111l1_opy_(session[bstack11ll11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ะ")]),
    bstack1l11llll11_opy_(session[bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨั")] or session[bstack11ll11_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨา")] or bstack11ll11_opy_ (u"ࠩࠪำ")) + bstack11ll11_opy_ (u"ࠥࠤࠧิ") + (session[bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ี")] or bstack11ll11_opy_ (u"ࠬ࠭ึ")),
    session[bstack11ll11_opy_ (u"࠭࡯ࡴࠩื")] + bstack11ll11_opy_ (u"ࠢࠡࠤุ") + session[bstack11ll11_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲูࠬ")], session[bstack11ll11_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱฺࠫ")] or bstack11ll11_opy_ (u"ࠪࠫ฻"),
    session[bstack11ll11_opy_ (u"ࠫࡨࡸࡥࡢࡶࡨࡨࡤࡧࡴࠨ฼")] if session[bstack11ll11_opy_ (u"ࠬࡩࡲࡦࡣࡷࡩࡩࡥࡡࡵࠩ฽")] else bstack11ll11_opy_ (u"࠭ࠧ฾"))
@measure(event_name=EVENTS.bstack11lllll1l_opy_, stage=STAGE.bstack1lll11llll_opy_, bstack1111llll_opy_=bstack11ll11lll_opy_)
def bstack1l1l1111l1_opy_(sessions, bstack1lll1l1l_opy_):
  try:
    bstack1l11l11l_opy_ = bstack11ll11_opy_ (u"ࠢࠣ฿")
    if not os.path.exists(bstack1l1l111lll_opy_):
      os.mkdir(bstack1l1l111lll_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11ll11_opy_ (u"ࠨࡣࡶࡷࡪࡺࡳ࠰ࡴࡨࡴࡴࡸࡴ࠯ࡪࡷࡱࡱ࠭เ")), bstack11ll11_opy_ (u"ࠩࡵࠫแ")) as f:
      bstack1l11l11l_opy_ = f.read()
    bstack1l11l11l_opy_ = bstack1l11l11l_opy_.replace(bstack11ll11_opy_ (u"ࠪࡿࠪࡘࡅࡔࡗࡏࡘࡘࡥࡃࡐࡗࡑࡘࠪࢃࠧโ"), str(len(sessions)))
    bstack1l11l11l_opy_ = bstack1l11l11l_opy_.replace(bstack11ll11_opy_ (u"ࠫࢀࠫࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠧࢀࠫใ"), bstack1lll1l1l_opy_)
    bstack1l11l11l_opy_ = bstack1l11l11l_opy_.replace(bstack11ll11_opy_ (u"ࠬࢁࠥࡃࡗࡌࡐࡉࡥࡎࡂࡏࡈࠩࢂ࠭ไ"),
                                              sessions[0].get(bstack11ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡴࡡ࡮ࡧࠪๅ")) if sessions[0] else bstack11ll11_opy_ (u"ࠧࠨๆ"))
    with open(os.path.join(bstack1l1l111lll_opy_, bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡳࡧࡳࡳࡷࡺ࠮ࡩࡶࡰࡰࠬ็")), bstack11ll11_opy_ (u"ࠩࡺ่ࠫ")) as stream:
      stream.write(bstack1l11l11l_opy_.split(bstack11ll11_opy_ (u"ࠪࡿ࡙ࠪࡅࡔࡕࡌࡓࡓ࡙࡟ࡅࡃࡗࡅࠪࢃ้ࠧ"))[0])
      for session in sessions:
        stream.write(bstack11lll11l11_opy_(session))
      stream.write(bstack1l11l11l_opy_.split(bstack11ll11_opy_ (u"ࠫࢀࠫࡓࡆࡕࡖࡍࡔࡔࡓࡠࡆࡄࡘࡆࠫࡽࠨ๊"))[1])
    logger.info(bstack11ll11_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡫ࡤࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡣࡷ࡬ࡰࡩࠦࡡࡳࡶ࡬ࡪࡦࡩࡴࡴࠢࡤࡸࠥࢁࡽࠨ๋").format(bstack1l1l111lll_opy_));
  except Exception as e:
    logger.debug(bstack11l1llll_opy_.format(str(e)))
def bstack1l1l11llll_opy_(hashed_id):
  global CONFIG
  try:
    bstack1ll1lll1ll_opy_ = datetime.datetime.now()
    host = bstack11ll11_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡲ࡬࠱ࡨࡲ࡯ࡶࡦ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭์") if bstack11ll11_opy_ (u"ࠧࡢࡲࡳࠫํ") in CONFIG else bstack11ll11_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩ๎")
    user = CONFIG[bstack11ll11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ๏")]
    key = CONFIG[bstack11ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭๐")]
    bstack1l1ll11l_opy_ = bstack11ll11_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪ๑") if bstack11ll11_opy_ (u"ࠬࡧࡰࡱࠩ๒") in CONFIG else (bstack11ll11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪ๓") if CONFIG.get(bstack11ll11_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫ๔")) else bstack11ll11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ๕"))
    if cli.is_running():
      host = bstack1l1l11ll1_opy_(cli.config, [bstack11ll11_opy_ (u"ࠤࡤࡴ࡮ࡹࠢ๖"), bstack11ll11_opy_ (u"ࠥࡥࡵࡶࡁࡶࡶࡲࡱࡦࡺࡥࠣ๗"), bstack11ll11_opy_ (u"ࠦࡦࡶࡩࠣ๘")], host) if bstack11ll11_opy_ (u"ࠬࡧࡰࡱࠩ๙") in CONFIG else bstack1l1l11ll1_opy_(cli.config, [bstack11ll11_opy_ (u"ࠨࡡࡱ࡫ࡶࠦ๚"), bstack11ll11_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡦࠤ๛"), bstack11ll11_opy_ (u"ࠣࡣࡳ࡭ࠧ๜")], host)
    url = bstack11ll11_opy_ (u"ࠩࡾࢁ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀ࠳ࡸ࡫ࡳࡴ࡫ࡲࡲࡸ࠴ࡪࡴࡱࡱࠫ๝").format(host, bstack1l1ll11l_opy_, hashed_id)
    headers = {
      bstack11ll11_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩ๞"): bstack11ll11_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ๟"),
    }
    proxies = bstack1l1ll111_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies, auth=(user, key))
    if response.json():
      cli.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࡫ࡪࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࡡ࡯࡭ࡸࡺࠢ๠"), datetime.datetime.now() - bstack1ll1lll1ll_opy_)
      return list(map(lambda session: session[bstack11ll11_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࠫ๡")], response.json()))
  except Exception as e:
    logger.debug(bstack1111ll1l1_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack1lll1l1l11_opy_, stage=STAGE.bstack1lll11llll_opy_, bstack1111llll_opy_=bstack11ll11lll_opy_)
def get_build_link():
  global CONFIG
  global bstack1l11l1l11_opy_
  try:
    if bstack11ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ๢") in CONFIG:
      bstack1ll1lll1ll_opy_ = datetime.datetime.now()
      host = bstack11ll11_opy_ (u"ࠨࡣࡳ࡭࠲ࡩ࡬ࡰࡷࡧࠫ๣") if bstack11ll11_opy_ (u"ࠩࡤࡴࡵ࠭๤") in CONFIG else bstack11ll11_opy_ (u"ࠪࡥࡵ࡯ࠧ๥")
      user = CONFIG[bstack11ll11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭๦")]
      key = CONFIG[bstack11ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ๧")]
      bstack1l1ll11l_opy_ = bstack11ll11_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ๨") if bstack11ll11_opy_ (u"ࠧࡢࡲࡳࠫ๩") in CONFIG else bstack11ll11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ๪")
      url = bstack11ll11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡾࢁ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀ࠳ࡧࡻࡩ࡭ࡦࡶ࠲࡯ࡹ࡯࡯ࠩ๫").format(user, key, host, bstack1l1ll11l_opy_)
      if cli.is_enabled(CONFIG):
        bstack1lll1l1l_opy_, hashed_id = cli.bstack11l1l1ll1_opy_()
        logger.info(bstack1l11l1ll11_opy_.format(bstack1lll1l1l_opy_))
        return [hashed_id, bstack1lll1l1l_opy_]
      else:
        headers = {
          bstack11ll11_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩ๬"): bstack11ll11_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ๭"),
        }
        if bstack11ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ๮") in CONFIG:
          params = {bstack11ll11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ๯"): CONFIG[bstack11ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ๰")], bstack11ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ๱"): CONFIG[bstack11ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ๲")]}
        else:
          params = {bstack11ll11_opy_ (u"ࠪࡲࡦࡳࡥࠨ๳"): CONFIG[bstack11ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ๴")]}
        proxies = bstack1l1ll111_opy_(CONFIG, url)
        response = requests.get(url, params=params, headers=headers, proxies=proxies)
        if response.json():
          bstack1111lllll_opy_ = response.json()[0][bstack11ll11_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡥࡹ࡮ࡲࡤࠨ๵")]
          if bstack1111lllll_opy_:
            bstack1lll1l1l_opy_ = bstack1111lllll_opy_[bstack11ll11_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨࡥࡵࡳ࡮ࠪ๶")].split(bstack11ll11_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࠭ࡣࡷ࡬ࡰࡩ࠭๷"))[0] + bstack11ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡳ࠰ࠩ๸") + bstack1111lllll_opy_[
              bstack11ll11_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ๹")]
            logger.info(bstack1l11l1ll11_opy_.format(bstack1lll1l1l_opy_))
            bstack1l11l1l11_opy_ = bstack1111lllll_opy_[bstack11ll11_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭๺")]
            bstack1l111l1111_opy_ = CONFIG[bstack11ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ๻")]
            if bstack11ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ๼") in CONFIG:
              bstack1l111l1111_opy_ += bstack11ll11_opy_ (u"࠭ࠠࠨ๽") + CONFIG[bstack11ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ๾")]
            if bstack1l111l1111_opy_ != bstack1111lllll_opy_[bstack11ll11_opy_ (u"ࠨࡰࡤࡱࡪ࠭๿")]:
              logger.debug(bstack11l11l11l_opy_.format(bstack1111lllll_opy_[bstack11ll11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ຀")], bstack1l111l1111_opy_))
            cli.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻ࡩࡨࡸࡤࡨࡵࡪ࡮ࡧࡣࡱ࡯࡮࡬ࠤກ"), datetime.datetime.now() - bstack1ll1lll1ll_opy_)
            return [bstack1111lllll_opy_[bstack11ll11_opy_ (u"ࠫ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧຂ")], bstack1lll1l1l_opy_]
    else:
      logger.warn(bstack1lll1llll1_opy_)
  except Exception as e:
    logger.debug(bstack1lll1l1ll_opy_.format(str(e)))
  return [None, None]
def bstack1l1lll11ll_opy_(url, bstack1ll1lll111_opy_=False):
  global CONFIG
  global bstack1l1111ll11_opy_
  if not bstack1l1111ll11_opy_:
    hostname = bstack11l1ll1ll1_opy_(url)
    is_private = bstack11l1l11l_opy_(hostname)
    if (bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ຃") in CONFIG and not bstack1l111ll1l_opy_(CONFIG[bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪຄ")])) and (is_private or bstack1ll1lll111_opy_):
      bstack1l1111ll11_opy_ = hostname
def bstack11l1ll1ll1_opy_(url):
  return urlparse(url).hostname
def bstack11l1l11l_opy_(hostname):
  for bstack1l11l11111_opy_ in bstack11ll1l111l_opy_:
    regex = re.compile(bstack1l11l11111_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1l11ll1lll_opy_(bstack111ll11ll_opy_):
  return True if bstack111ll11ll_opy_ in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack1ll1llll_opy_, stage=STAGE.bstack1lll11llll_opy_, bstack1111llll_opy_=bstack11ll11lll_opy_)
def getAccessibilityResults(driver):
  global CONFIG
  global bstack11llllllll_opy_
  bstack1llll111l_opy_ = not (bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ຅"), None) and bstack111ll1lll_opy_(
          threading.current_thread(), bstack11ll11_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧຆ"), None))
  bstack11l1llllll_opy_ = getattr(driver, bstack11ll11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩງ"), None) != True
  bstack1l1l1l1l11_opy_ = bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪຈ"), None) and bstack111ll1lll_opy_(
          threading.current_thread(), bstack11ll11_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ຉ"), None)
  if bstack1l1l1l1l11_opy_:
    if not bstack11llll11_opy_():
      logger.warning(bstack11ll11_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡰࡱࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡅࡵࡶࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳ࠯ࠤຊ"))
      return {}
    logger.debug(bstack11ll11_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪ຋"))
    logger.debug(perform_scan(driver, driver_command=bstack11ll11_opy_ (u"ࠧࡦࡺࡨࡧࡺࡺࡥࡔࡥࡵ࡭ࡵࡺࠧຌ")))
    results = bstack1l1ll11lll_opy_(bstack11ll11_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࡴࠤຍ"))
    if results is not None and results.get(bstack11ll11_opy_ (u"ࠤ࡬ࡷࡸࡻࡥࡴࠤຎ")) is not None:
        return results[bstack11ll11_opy_ (u"ࠥ࡭ࡸࡹࡵࡦࡵࠥຏ")]
    logger.error(bstack11ll11_opy_ (u"ࠦࡓࡵࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡓࡧࡶࡹࡱࡺࡳࠡࡹࡨࡶࡪࠦࡦࡰࡷࡱࡨ࠳ࠨຐ"))
    return []
  if not bstack11l11lll11_opy_.bstack11lll11l1l_opy_(CONFIG, bstack11llllllll_opy_) or (bstack11l1llllll_opy_ and bstack1llll111l_opy_):
    logger.warning(bstack11ll11_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹ࠮ࠣຑ"))
    return {}
  try:
    logger.debug(bstack11ll11_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪຒ"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack11llll1l1l_opy_.bstack1ll1l1llll_opy_)
    return results
  except Exception:
    logger.error(bstack11ll11_opy_ (u"ࠢࡏࡱࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡼ࡫ࡲࡦࠢࡩࡳࡺࡴࡤ࠯ࠤຓ"))
    return {}
@measure(event_name=EVENTS.bstack1ll11l1l_opy_, stage=STAGE.bstack1lll11llll_opy_, bstack1111llll_opy_=bstack11ll11lll_opy_)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack11llllllll_opy_
  bstack1llll111l_opy_ = not (bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬດ"), None) and bstack111ll1lll_opy_(
          threading.current_thread(), bstack11ll11_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨຕ"), None))
  bstack11l1llllll_opy_ = getattr(driver, bstack11ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪຖ"), None) != True
  bstack1l1l1l1l11_opy_ = bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫທ"), None) and bstack111ll1lll_opy_(
          threading.current_thread(), bstack11ll11_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧຘ"), None)
  if bstack1l1l1l1l11_opy_:
    if not bstack11llll11_opy_():
      logger.warning(bstack11ll11_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡆࡶࡰࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡶࡹࡲࡳࡡࡳࡻ࠱ࠦນ"))
      return {}
    logger.debug(bstack11ll11_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡸࡻ࡭࡮ࡣࡵࡽࠬບ"))
    logger.debug(perform_scan(driver, driver_command=bstack11ll11_opy_ (u"ࠨࡧࡻࡩࡨࡻࡴࡦࡕࡦࡶ࡮ࡶࡴࠨປ")))
    results = bstack1l1ll11lll_opy_(bstack11ll11_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡕࡸࡱࡲࡧࡲࡺࠤຜ"))
    if results is not None and results.get(bstack11ll11_opy_ (u"ࠥࡷࡺࡳ࡭ࡢࡴࡼࠦຝ")) is not None:
        return results[bstack11ll11_opy_ (u"ࠦࡸࡻ࡭࡮ࡣࡵࡽࠧພ")]
    logger.error(bstack11ll11_opy_ (u"ࠧࡔ࡯ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡔࡨࡷࡺࡲࡴࡴࠢࡖࡹࡲࡳࡡࡳࡻࠣࡻࡦࡹࠠࡧࡱࡸࡲࡩ࠴ࠢຟ"))
    return {}
  if not bstack11l11lll11_opy_.bstack11lll11l1l_opy_(CONFIG, bstack11llllllll_opy_) or (bstack11l1llllll_opy_ and bstack1llll111l_opy_):
    logger.warning(bstack11ll11_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡵࡸࡱࡲࡧࡲࡺ࠰ࠥຠ"))
    return {}
  try:
    logger.debug(bstack11ll11_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡸࡻ࡭࡮ࡣࡵࡽࠬມ"))
    logger.debug(perform_scan(driver))
    bstack1l1l111l11_opy_ = driver.execute_async_script(bstack11llll1l1l_opy_.bstack1l1l1l111l_opy_)
    return bstack1l1l111l11_opy_
  except Exception:
    logger.error(bstack11ll11_opy_ (u"ࠣࡐࡲࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸࡻ࡭࡮ࡣࡵࡽࠥࡽࡡࡴࠢࡩࡳࡺࡴࡤ࠯ࠤຢ"))
    return {}
def bstack11llll11_opy_():
  global CONFIG
  global bstack11llllllll_opy_
  bstack1l1l1l1l1_opy_ = bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩຣ"), None) and bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ຤"), None)
  if not bstack11l11lll11_opy_.bstack11lll11l1l_opy_(CONFIG, bstack11llllllll_opy_) or not bstack1l1l1l1l1_opy_:
        logger.warning(bstack11ll11_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡶࡰࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡵࡩࡸࡻ࡬ࡵࡵ࠱ࠦລ"))
        return False
  return True
def bstack1l1ll11lll_opy_(bstack11111l1ll_opy_):
    bstack1l1llll1l_opy_ = bstack1l1l1l1ll_opy_.current_test_uuid() if bstack1l1l1l1ll_opy_.current_test_uuid() else bstack11l1ll11_opy_.current_hook_uuid()
    with ThreadPoolExecutor() as executor:
        future = executor.submit(bstack1lll11111_opy_(bstack1l1llll1l_opy_, bstack11111l1ll_opy_))
        try:
            return future.result(timeout=bstack11l1l11ll_opy_)
        except TimeoutError:
            logger.error(bstack11ll11_opy_ (u"࡚ࠧࡩ࡮ࡧࡲࡹࡹࠦࡡࡧࡶࡨࡶࠥࢁࡽࡴࠢࡺ࡬࡮ࡲࡥࠡࡨࡨࡸࡨ࡮ࡩ࡯ࡩࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡖࡪࡹࡵ࡭ࡶࡶࠦ຦").format(bstack11l1l11ll_opy_))
        except Exception as ex:
            logger.debug(bstack11ll11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡸࡥࡵࡴ࡬ࡩࡻ࡯࡮ࡨࠢࡄࡴࡵࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡿࢂ࠴ࠠࡆࡴࡵࡳࡷࠦ࠭ࠡࡽࢀࠦວ").format(bstack11111l1ll_opy_, str(ex)))
    return {}
@measure(event_name=EVENTS.bstack1lllll1l11_opy_, stage=STAGE.bstack1lll11llll_opy_, bstack1111llll_opy_=bstack11ll11lll_opy_)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack11llllllll_opy_
  bstack1llll111l_opy_ = not (bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫຨ"), None) and bstack111ll1lll_opy_(
          threading.current_thread(), bstack11ll11_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧຩ"), None))
  bstack11l1l1ll_opy_ = not (bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩສ"), None) and bstack111ll1lll_opy_(
          threading.current_thread(), bstack11ll11_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬຫ"), None))
  bstack11l1llllll_opy_ = getattr(driver, bstack11ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫຬ"), None) != True
  if not bstack11l11lll11_opy_.bstack11lll11l1l_opy_(CONFIG, bstack11llllllll_opy_) or (bstack11l1llllll_opy_ and bstack1llll111l_opy_ and bstack11l1l1ll_opy_):
    logger.warning(bstack11ll11_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷࡻ࡮ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳ࠴ࠢອ"))
    return {}
  try:
    bstack111111ll_opy_ = bstack11ll11_opy_ (u"࠭ࡡࡱࡲࠪຮ") in CONFIG and CONFIG.get(bstack11ll11_opy_ (u"ࠧࡢࡲࡳࠫຯ"), bstack11ll11_opy_ (u"ࠨࠩະ"))
    session_id = getattr(driver, bstack11ll11_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩ࠭ັ"), None)
    if not session_id:
      logger.warning(bstack11ll11_opy_ (u"ࠥࡒࡴࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡊࡆࠣࡪࡴࡻ࡮ࡥࠢࡩࡳࡷࠦࡤࡳ࡫ࡹࡩࡷࠨາ"))
      return {bstack11ll11_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥຳ"): bstack11ll11_opy_ (u"ࠧࡔ࡯ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡌࡈࠥ࡬࡯ࡶࡰࡧࠦິ")}
    if bstack111111ll_opy_:
      try:
        bstack1ll111111l_opy_ = {
              bstack11ll11_opy_ (u"࠭ࡴࡩࡌࡺࡸ࡙ࡵ࡫ࡦࡰࠪີ"): os.environ.get(bstack11ll11_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬຶ"), os.environ.get(bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬື"), bstack11ll11_opy_ (u"ຸࠩࠪ"))),
              bstack11ll11_opy_ (u"ࠪࡸ࡭࡚ࡥࡴࡶࡕࡹࡳ࡛ࡵࡪࡦູࠪ"): bstack1l1l1l1ll_opy_.current_test_uuid() if bstack1l1l1l1ll_opy_.current_test_uuid() else bstack11l1ll11_opy_.current_hook_uuid(),
              bstack11ll11_opy_ (u"ࠫࡦࡻࡴࡩࡊࡨࡥࡩ࡫ࡲࠨ຺"): os.environ.get(bstack11ll11_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪົ")),
              bstack11ll11_opy_ (u"࠭ࡳࡤࡣࡱࡘ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ຼ"): str(int(datetime.datetime.now().timestamp() * 1000)),
              bstack11ll11_opy_ (u"ࠧࡵࡪࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬຽ"): os.environ.get(bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭຾"), bstack11ll11_opy_ (u"ࠩࠪ຿")),
              bstack11ll11_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࠪເ"): kwargs.get(bstack11ll11_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࡣࡨࡵ࡭࡮ࡣࡱࡨࠬແ"), None) or bstack11ll11_opy_ (u"ࠬ࠭ໂ")
          }
        if not hasattr(thread_local, bstack11ll11_opy_ (u"࠭ࡢࡢࡵࡨࡣࡦࡶࡰࡠࡣ࠴࠵ࡾࡥࡳࡤࡴ࡬ࡴࡹ࠭ໃ")):
            scripts = {bstack11ll11_opy_ (u"ࠧࡴࡥࡤࡲࠬໄ"): bstack11llll1l1l_opy_.perform_scan}
            thread_local.base_app_a11y_script = scripts
        bstack1llll111l1_opy_ = copy.deepcopy(thread_local.base_app_a11y_script)
        bstack1llll111l1_opy_[bstack11ll11_opy_ (u"ࠨࡵࡦࡥࡳ࠭໅")] = bstack1llll111l1_opy_[bstack11ll11_opy_ (u"ࠩࡶࡧࡦࡴࠧໆ")] % json.dumps(bstack1ll111111l_opy_)
        bstack11llll1l1l_opy_.bstack11ll1ll1ll_opy_(bstack1llll111l1_opy_)
        bstack11llll1l1l_opy_.store()
        bstack1ll11l111l_opy_ = driver.execute_script(bstack11llll1l1l_opy_.perform_scan)
      except Exception as bstack111111111_opy_:
        logger.info(bstack11ll11_opy_ (u"ࠥࡅࡵࡶࡩࡶ࡯ࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࠥ໇") + str(bstack111111111_opy_))
        bstack1ll11l111l_opy_ = {bstack11ll11_opy_ (u"ࠦࡪࡸࡲࡰࡴ່ࠥ"): str(bstack111111111_opy_)}
    else:
      bstack1ll11l111l_opy_ = driver.execute_async_script(bstack11llll1l1l_opy_.perform_scan, {bstack11ll11_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨ້ࠬ"): kwargs.get(bstack11ll11_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡣࡰ࡯ࡰࡥࡳࡪ໊ࠧ"), None) or bstack11ll11_opy_ (u"ࠧࠨ໋")})
    return bstack1ll11l111l_opy_
  except Exception as err:
    logger.error(bstack11ll11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡷࡻ࡮ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳ࠴ࠠࡼࡿࠥ໌").format(str(err)))
    return {}