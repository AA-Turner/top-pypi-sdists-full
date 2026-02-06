# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
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
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from browserstack_sdk.bstack11lll111_opy_ import bstack1ll1l1l1l_opy_
from browserstack_sdk.bstack1l11111l11_opy_ import *
import time
import requests
from bstack_utils.constants import EVENTS, STAGE, bstack1lll1llll_opy_
from bstack_utils.messages import bstack1lllll11l1_opy_, bstack1l111ll1ll_opy_, bstack111l11lll1_opy_, bstack1llll111l1_opy_, bstack111l1l111l_opy_, bstack111ll1ll_opy_
from bstack_utils.measure import measure
from bstack_utils.logger_utils import get_logger
from bstack_utils.helper import bstack11l1l1111_opy_
from browserstack_sdk.bstack11ll111ll_opy_ import bstack11ll11ll_opy_
logger = get_logger(__name__)
def bstack1ll11ll11l_opy_():
  global CONFIG
  headers = {
        bstack11lllll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack11lllll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack11l1l1111_opy_(CONFIG, bstack1lll1llll_opy_)
  try:
    response = requests.get(bstack1lll1llll_opy_, headers=headers, proxies=proxies, timeout=2)
    if response.json():
      bstack111l11ll11_opy_ = response.json()[bstack11lllll_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1lllll11l1_opy_.format(response.json()))
      return bstack111l11ll11_opy_
    else:
      logger.debug(bstack1l111ll1ll_opy_.format(bstack11lllll_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack1l111ll1ll_opy_.format(e))
def bstack1l1l11ll_opy_(hub_url):
  global CONFIG
  url = bstack11lllll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack11lllll_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack11lllll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack11lllll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack11l1l1111_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=(0.5, 1.0))
    latency = time.perf_counter() - start_time
    logger.debug(bstack111l11lll1_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1llll111l1_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack111lllll1_opy_, stage=STAGE.bstack1llll11111_opy_)
def bstack1lllll1l1l_opy_():
  try:
    global bstack11l1ll111_opy_
    global CONFIG
    if bstack11lllll_opy_ (u"ࠫ࡭ࡻࡢࡓࡧࡪ࡭ࡴࡴࠧࡾ") in CONFIG and CONFIG[bstack11lllll_opy_ (u"ࠬ࡮ࡵࡣࡔࡨ࡫࡮ࡵ࡮ࠨࡿ")]:
      from bstack_utils.constants import bstack111l11l1_opy_
      bstack11ll1ll11l_opy_ = CONFIG[bstack11lllll_opy_ (u"࠭ࡨࡶࡤࡕࡩ࡬࡯࡯࡯ࠩࢀ")]
      if bstack11ll1ll11l_opy_ in bstack111l11l1_opy_:
        bstack11l1ll111_opy_ = bstack111l11l1_opy_[bstack11ll1ll11l_opy_]
        logger.debug(bstack111l1l111l_opy_.format(bstack11l1ll111_opy_))
        return
      else:
        logger.debug(bstack11lllll_opy_ (u"ࠢࡉࡷࡥࠤࡰ࡫ࡹࠡࠩࡾࢁࠬࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࡎࡕࡃࡡࡘࡖࡑࡥࡍࡂࡒ࠯ࠤ࡫ࡧ࡬࡭࡫ࡱ࡫ࠥࡨࡡࡤ࡭ࠣࡸࡴࠦ࡯ࡱࡶ࡬ࡱࡦࡲࠠࡩࡷࡥࠤࡩ࡫ࡴࡦࡥࡷ࡭ࡴࡴࠢࢁ").format(bstack11ll1ll11l_opy_))
    bstack111l11ll11_opy_ = bstack1ll11ll11l_opy_()
    from concurrent.futures import ThreadPoolExecutor, as_completed
    if bstack111l11ll11_opy_:
        with ThreadPoolExecutor(max_workers=len(bstack111l11ll11_opy_)) as executor:
            bstack1l11l1ll1_opy_ = {executor.submit(bstack1l1l11ll_opy_, bstack1l1111111l_opy_): bstack1l1111111l_opy_ for bstack1l1111111l_opy_ in bstack111l11ll11_opy_}
            for future in as_completed(bstack1l11l1ll1_opy_):
                result = future.result()
                if result and result.get(bstack11lllll_opy_ (u"ࠨ࡮ࡤࡸࡪࡴࡣࡺࠩࢂ")) is not None:
                    bstack11l1ll111_opy_ = result[bstack11lllll_opy_ (u"ࠩ࡫ࡹࡧࡥࡵࡳ࡮ࠪࢃ")]
                    logger.debug(bstack111l1l111l_opy_.format(bstack11l1ll111_opy_))
                    return
        bstack11l1ll111_opy_ = bstack111l11ll11_opy_[0]
        logger.debug(bstack111l1l111l_opy_.format(bstack11l1ll111_opy_))
        return
  except Exception as e:
    logger.debug(bstack111ll1ll_opy_.format(e))
from browserstack_sdk.bstack1l1lll11l_opy_ import *
from browserstack_sdk.bstack11ll111ll_opy_ import *
from browserstack_sdk.bstack1ll1111l1_opy_ import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.logger_utils import get_logger
from bstack_utils.measure import measure
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack1l1l11ll11_opy_, stage=STAGE.bstack1llll11111_opy_)
def bstack1lll1l111l_opy_():
    global bstack11l1ll111_opy_
    try:
        bstack11lll1ll_opy_ = bstack11111l11_opy_()
        bstack1l1l111lll_opy_(bstack11lll1ll_opy_)
        hub_url = bstack11lll1ll_opy_.get(bstack11lllll_opy_ (u"ࠥࡹࡷࡲࠢࢄ"), bstack11lllll_opy_ (u"ࠦࠧࢅ"))
        if hub_url.endswith(bstack11lllll_opy_ (u"ࠬ࠵ࡷࡥ࠱࡫ࡹࡧ࠭ࢆ")):
            hub_url = hub_url.rsplit(bstack11lllll_opy_ (u"࠭࠯ࡸࡦ࠲࡬ࡺࡨࠧࢇ"), 1)[0]
        if hub_url.startswith(bstack11lllll_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࠨ࢈")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack11lllll_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࠪࢉ")):
            hub_url = hub_url[8:]
        bstack11l1ll111_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack11111l11_opy_():
    global CONFIG
    bstack1l11lll1_opy_ = CONFIG.get(bstack11lllll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢊ"), {}).get(bstack11lllll_opy_ (u"ࠪ࡫ࡷ࡯ࡤࡏࡣࡰࡩࠬࢋ"), bstack11lllll_opy_ (u"ࠫࡓࡕ࡟ࡈࡔࡌࡈࡤࡔࡁࡎࡇࡢࡔࡆ࡙ࡓࡆࡆࠪࢌ"))
    if not isinstance(bstack1l11lll1_opy_, str):
        raise ValueError(bstack11lllll_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡌࡸࡩࡥࠢࡱࡥࡲ࡫ࠠ࡮ࡷࡶࡸࠥࡨࡥࠡࡣࠣࡺࡦࡲࡩࡥࠢࡶࡸࡷ࡯࡮ࡨࠤࢍ"))
    try:
        bstack11lll1ll_opy_ = bstack1ll111ll1_opy_(bstack1l11lll1_opy_)
        return bstack11lll1ll_opy_
    except Exception as e:
        logger.error(bstack11lllll_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡩࡵ࡭ࡩࠦࡤࡦࡶࡤ࡭ࡱࡹࠠ࠻ࠢࡾࢁࠧࢎ").format(str(e)))
        return {}
def bstack1ll111ll1_opy_(bstack1l11lll1_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack11lllll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ࢏")] or not CONFIG[bstack11lllll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ࢐")]:
            raise ValueError(bstack11lllll_opy_ (u"ࠤࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠤࡴࡸࠠࡢࡥࡦࡩࡸࡹࠠ࡬ࡧࡼࠦ࢑"))
        url = bstack1l111l111_opy_ + bstack1l11lll1_opy_
        auth = (CONFIG[bstack11lllll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ࢒")], CONFIG[bstack11lllll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ࢓")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack11lll1l1l1_opy_ = json.loads(response.text)
            return bstack11lll1l1l1_opy_
    except ValueError as ve:
        logger.error(bstack11lllll_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡩࡵ࡭ࡩࠦࡤࡦࡶࡤ࡭ࡱࡹࠠ࠻ࠢࡾࢁࠧ࢔").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack11lllll_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡪࡶ࡮ࡪࠠࡥࡧࡷࡥ࡮ࡲࡳࠡ࠼ࠣࡿࢂࠨ࢕").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack1l1l111lll_opy_(bstack11ll111l_opy_):
    global CONFIG
    if bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ࢖") not in CONFIG or str(CONFIG[bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬࢗ")]).lower() == bstack11lllll_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ࢘"):
        CONFIG[bstack11lllll_opy_ (u"ࠪࡰࡴࡩࡡ࡭࢙ࠩ")] = False
    elif bstack11lllll_opy_ (u"ࠫ࡮ࡹࡔࡳ࡫ࡤࡰࡌࡸࡩࡥ࢚ࠩ") in bstack11ll111l_opy_:
        bstack11l1111l1_opy_ = CONFIG.get(bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴ࢛ࠩ"), {})
        logger.debug(bstack11lllll_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡸࡪࡵࡷ࡭ࡳ࡭ࠠ࡭ࡱࡦࡥࡱࠦ࡯ࡱࡶ࡬ࡳࡳࡹ࠺ࠡࠧࡶࠦ࢜"), bstack11l1111l1_opy_)
        bstack1lllllll11_opy_ = bstack11ll111l_opy_.get(bstack11lllll_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡒࡦࡲࡨࡥࡹ࡫ࡲࡴࠤ࢝"), [])
        bstack1lll11l1_opy_ = bstack11lllll_opy_ (u"ࠣ࠮ࠥ࢞").join(bstack1lllllll11_opy_)
        logger.debug(bstack11lllll_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡅࡸࡷࡹࡵ࡭ࠡࡴࡨࡴࡪࡧࡴࡦࡴࠣࡷࡹࡸࡩ࡯ࡩ࠽ࠤࠪࡹࠢ࢟"), bstack1lll11l1_opy_)
        bstack1ll1l1ll1_opy_ = {
            bstack11lllll_opy_ (u"ࠥࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧࢠ"): bstack11lllll_opy_ (u"ࠦࡦࡺࡳ࠮ࡴࡨࡴࡪࡧࡴࡦࡴࠥࢡ"),
            bstack11lllll_opy_ (u"ࠧ࡬࡯ࡳࡥࡨࡐࡴࡩࡡ࡭ࠤࢢ"): bstack11lllll_opy_ (u"ࠨࡴࡳࡷࡨࠦࢣ"),
            bstack11lllll_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࠭ࡳࡧࡳࡩࡦࡺࡥࡳࠤࢤ"): bstack1lll11l1_opy_
        }
        bstack11l1111l1_opy_.update(bstack1ll1l1ll1_opy_)
        logger.debug(bstack11lllll_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡖࡲࡧࡥࡹ࡫ࡤࠡ࡮ࡲࡧࡦࡲࠠࡰࡲࡷ࡭ࡴࡴࡳ࠻ࠢࠨࡷࠧࢥ"), bstack11l1111l1_opy_)
        CONFIG[bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢦ")] = bstack11l1111l1_opy_
        logger.debug(bstack11lllll_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡉ࡭ࡳࡧ࡬ࠡࡅࡒࡒࡋࡏࡇ࠻ࠢࠨࡷࠧࢧ"), CONFIG)
def bstack1l11l111_opy_():
    bstack11lll1ll_opy_ = bstack11111l11_opy_()
    if not bstack11lll1ll_opy_[bstack11lllll_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡖࡴ࡯ࠫࢨ")]:
      raise ValueError(bstack11lllll_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡗࡵࡰࠥ࡯ࡳࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡩࡶࡴࡳࠠࡨࡴ࡬ࡨࠥࡪࡥࡵࡣ࡬ࡰࡸ࠴ࠢࢩ"))
    return bstack11lll1ll_opy_[bstack11lllll_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡘࡶࡱ࠭ࢪ")] + bstack11lllll_opy_ (u"ࠧࡀࡥࡤࡴࡸࡃࠧࢫ")
@measure(event_name=EVENTS.bstack11l1l11ll1_opy_, stage=STAGE.bstack1llll11111_opy_)
def bstack111l11l11_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack11lllll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪࢬ")], CONFIG[bstack11lllll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬࢭ")])
        url = bstack111lll111l_opy_
        logger.debug(bstack11lllll_opy_ (u"ࠥࡅࡹࡺࡥ࡮ࡲࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴࠢࡩࡶࡴࡳࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡔࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠣࡅࡕࡏࠢࢮ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack11lllll_opy_ (u"ࠦࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠥࢯ"): bstack11lllll_opy_ (u"ࠧࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠣࢰ")})
            if response.status_code == 200:
                bstack1lll111111_opy_ = json.loads(response.text)
                bstack11l11111ll_opy_ = bstack1lll111111_opy_.get(bstack11lllll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡸ࠭ࢱ"), [])
                if bstack11l11111ll_opy_:
                    bstack111lllll1l_opy_ = bstack11l11111ll_opy_[0]
                    build_hashed_id = bstack111lllll1l_opy_.get(bstack11lllll_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪࢲ"))
                    bstack1l1l1lll1_opy_ = bstack11lllll1l1_opy_ + build_hashed_id
                    result.extend([build_hashed_id, bstack1l1l1lll1_opy_])
                    logger.info(bstack1l11111ll1_opy_.format(bstack1l1l1lll1_opy_))
                    bstack11l1llllll_opy_ = CONFIG[bstack11lllll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫࢳ")]
                    if bstack11lllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࢴ") in CONFIG:
                      bstack11l1llllll_opy_ += bstack11lllll_opy_ (u"ࠪࠤࠬࢵ") + CONFIG[bstack11lllll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࢶ")]
                    if bstack11l1llllll_opy_ != bstack111lllll1l_opy_.get(bstack11lllll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪࢷ")):
                      logger.debug(bstack1lll111l1_opy_.format(bstack111lllll1l_opy_.get(bstack11lllll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫࢸ")), bstack11l1llllll_opy_))
                    return result
                else:
                    logger.debug(bstack11lllll_opy_ (u"ࠢࡂࡖࡖࠤ࠿ࠦࡎࡰࠢࡥࡹ࡮ࡲࡤࡴࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠱ࠦࢹ"))
            else:
                logger.debug(bstack11lllll_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴ࠰ࠥࢺ"))
        except Exception as e:
            logger.error(bstack11lllll_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࡶࠤ࠿ࠦࡻࡾࠤࢻ").format(str(e)))
    else:
        logger.debug(bstack11lllll_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡆࡓࡓࡌࡉࡈࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡶࡩࡹ࠴ࠠࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴ࠰ࠥࢼ"))
    return [None, None]
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack11l1ll1l_opy_ import bstack11l1ll1l_opy_, bstack1lll11l1l_opy_, bstack11l11l1111_opy_, bstack1llllll111_opy_
from bstack_utils.measure import bstack11lll1l11l_opy_
from bstack_utils.measure import measure
from bstack_utils.percy import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack111l1ll1ll_opy_ import bstack11l11l11_opy_
from bstack_utils.messages import *
from bstack_utils import logger_utils
from bstack_utils.constants import *
from bstack_utils.helper import bstack1l1ll1ll_opy_, bstack111ll111_opy_, bstack1lll1l111_opy_, bstack1l1ll1ll1_opy_, \
  bstack1l111lll1l_opy_, \
  Notset, bstack1l1ll11ll_opy_, \
  bstack1l1l1111l_opy_, bstack1111lll11_opy_, bstack111l111l1_opy_, bstack11ll1lll1l_opy_, bstack11l111l111_opy_, bstack1ll1l111ll_opy_, \
  bstack111llll111_opy_, \
  bstack11lll111l_opy_, bstack11l1ll1l11_opy_, bstack1llll11lll_opy_, bstack1lll1l1l1_opy_, \
  bstack11l1lll1l_opy_, bstack1lll11ll1_opy_, bstack1ll1ll111_opy_, bstack1l1lll1111_opy_, bstack1l1l1111_opy_
from bstack_utils.bstack11ll1l11_opy_ import bstack1l11l11ll_opy_
from bstack_utils.bstack11lll1ll1_opy_ import bstack1llllll11l_opy_, bstack1l1l1lll11_opy_
from bstack_utils.bstack11l1lll1l1_opy_ import bstack1ll111111_opy_
from bstack_utils.bstack1l1l111l11_opy_ import bstack11l1l111l_opy_, bstack1ll11lll1_opy_
from bstack_utils.bstack1ll1111l1l_opy_ import bstack1ll1111l1l_opy_
from bstack_utils.bstack1l1lll1l11_opy_ import bstack11l11l1lll_opy_
from bstack_utils.proxy import bstack1l11lll11_opy_, bstack11l1l1111_opy_, bstack1l1l1l1ll1_opy_, bstack1ll11l111l_opy_
from bstack_utils.bstack11ll1ll11_opy_ import bstack1ll1lll11l_opy_, bstack1l1l1l1111_opy_
import bstack_utils.bstack111ll1ll1l_opy_ as bstack1llll1111_opy_
import bstack_utils.bstack1l111l1lll_opy_ as bstack11l11l1l1_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.utils.bstack1l1ll1lll_opy_ import bstack11l1111l11_opy_
from bstack_utils.bstack1lll1111l1_opy_ import bstack11l1lll11_opy_
from bstack_utils.bstack1llll1ll11_opy_ import bstack1111l1ll1_opy_
from bstack_utils.bstack11lll1l11l_opy_ import bstack1lll11l1ll_opy_
if os.getenv(bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡉࡑࡒࡏࡘ࠭ࢽ")):
  cli.bstack1l1111ll_opy_()
else:
  os.environ[bstack11lllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡊࡒࡓࡐ࡙ࠧࢾ")] = bstack11lllll_opy_ (u"࠭ࡴࡳࡷࡨࠫࢿ")
bstack11111l1l1_opy_ = bstack11lllll_opy_ (u"ࠧࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠠࠡ࡫ࡩࠬࡵࡧࡧࡦࠢࡀࡁࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠠࡼ࡞ࡱࠤࠥࠦࡴࡳࡻࡾࡠࡳࠦࡣࡰࡰࡶࡸࠥ࡬ࡳࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࡡ࠭ࡦࡴ࡞ࠪ࠭ࡀࡢ࡮ࠡࠢࠣࠤࠥ࡬ࡳ࠯ࡣࡳࡴࡪࡴࡤࡇ࡫࡯ࡩࡘࡿ࡮ࡤࠪࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠬࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡳࡣ࡮ࡴࡤࡦࡺࠬࠤ࠰ࠦࠢ࠻ࠤࠣ࠯ࠥࡐࡓࡐࡐ࠱ࡷࡹࡸࡩ࡯ࡩ࡬ࡪࡾ࠮ࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࠬࡦࡽࡡࡪࡶࠣࡲࡪࡽࡐࡢࡩࡨ࠶࠳࡫ࡶࡢ࡮ࡸࡥࡹ࡫ࠨࠣࠪࠬࠤࡂࡄࠠࡼࡿࠥ࠰ࠥࡢࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡨࡧࡷࡗࡪࡹࡳࡪࡱࡱࡈࡪࡺࡡࡪ࡮ࡶࠦࢂࡢࠧࠪࠫࠬ࡟ࠧ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠣ࡟ࠬࠤ࠰ࠦࠢ࠭࡞࡟ࡲࠧ࠯࡜࡯ࠢࠣࠤࠥࢃࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡽ࡝ࡰࠣࠤ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠧࣀ")
bstack11l11l11l_opy_ = bstack11lllll_opy_ (u"ࠨ࡞ࡱ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࡢ࡮ࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡰࡢࡶ࡫ࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳࡞࡞ࡱࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠴ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡶ࡟ࡪࡰࡧࡩࡽࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠴ࡠࡠࡳࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡹ࡬ࡪࡥࡨࠬ࠵࠲ࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࠬࡠࡳࡩ࡯࡯ࡵࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬ࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ࠭ࡀࡢ࡮ࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮࡭ࡣࡸࡲࡨ࡮ࠠ࠾ࠢࡤࡷࡾࡴࡣࠡࠪ࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴࠫࠣࡁࡃࠦࡻ࡝ࡰ࡯ࡩࡹࠦࡣࡢࡲࡶ࠿ࡡࡴࡴࡳࡻࠣࡿࡡࡴࡣࡢࡲࡶࠤࡂࠦࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠪ࡞ࡱࠤࠥࢃࠠࡤࡣࡷࡧ࡭࠮ࡥࡹࠫࠣࡿࡡࡴࠠࠡࠢࠣࢁࡡࡴࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡣࡺࡥ࡮ࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮ࡤࡱࡱࡲࡪࡩࡴࠩࡽ࡟ࡲࠥࠦࠠࠡࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸ࠿ࠦࡠࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠦࡾࡩࡳࡩ࡯ࡥࡧࡘࡖࡎࡉ࡯࡮ࡲࡲࡲࡪࡴࡴࠩࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡦࡥࡵࡹࠩࠪࡿࡣ࠰ࡡࡴࠠࠡࠢࠣ࠲࠳࠴࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸࡢ࡮ࠡࠢࢀ࠭ࡡࡴࡽ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠧࣁ")
from ._version import __version__
bstack11l11ll1_opy_ = None
CONFIG = {}
bstack1l111l11l_opy_ = {}
bstack111lllll11_opy_ = {}
bstack1ll11lll1l_opy_ = None
bstack11ll111l1_opy_ = None
bstack11l1l1ll1l_opy_ = None
bstack1l11111ll_opy_ = -1
bstack111lllllll_opy_ = 0
bstack1ll1ll1l11_opy_ = bstack111l1l11ll_opy_
bstack11l1l1lll_opy_ = 1
bstack1lll1l1ll_opy_ = False
bstack1llllllll_opy_ = False
bstack111ll1111_opy_ = bstack11lllll_opy_ (u"ࠩࠪࣂ")
bstack1lll1ll11l_opy_ = bstack11lllll_opy_ (u"ࠪࠫࣃ")
bstack1l1lll1l1_opy_ = False
bstack11ll1l1l11_opy_ = True
bstack1ll1l11ll1_opy_ = bstack11lllll_opy_ (u"ࠫࠬࣄ")
bstack1l11ll11ll_opy_ = []
bstack1l111ll111_opy_ = threading.Lock()
bstack1l1l1ll1ll_opy_ = threading.Lock()
bstack1ll1l1l111_opy_ = None
bstack11l1ll111_opy_ = bstack11lllll_opy_ (u"ࠬ࠭ࣅ")
bstack11llll1ll1_opy_ = False
bstack111l1l1l1l_opy_ = None
bstack111l1lll_opy_ = None
bstack1ll1ll1ll_opy_ = None
bstack1l1llll1l_opy_ = -1
bstack11ll1l11ll_opy_ = os.path.join(os.path.expanduser(bstack11lllll_opy_ (u"࠭ࡾࠨࣆ")), bstack11lllll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧࣇ"), bstack11lllll_opy_ (u"ࠨ࠰ࡵࡳࡧࡵࡴ࠮ࡴࡨࡴࡴࡸࡴ࠮ࡪࡨࡰࡵ࡫ࡲ࠯࡬ࡶࡳࡳ࠭ࣈ"))
bstack1l11111l1_opy_ = 0
bstack11ll111ll1_opy_ = 0
bstack1l11l111l1_opy_ = []
bstack1l1lllll1l_opy_ = []
ROBOT_PYTHON_ERRORS = []
bstack1l11llll1l_opy_ = []
bstack11l1ll1l1_opy_ = bstack11lllll_opy_ (u"ࠩࠪࣉ")
bstack11llllll11_opy_ = bstack11lllll_opy_ (u"ࠪࠫ࣊")
bstack1ll111l1l_opy_ = False
bstack111l1lll1_opy_ = False
bstack1111l11l1_opy_ = {}
bstack1l11l11l1_opy_ = {}
bstack1l1lll11l1_opy_ = None
bstack1ll111l11_opy_ = None
bstack1l1ll111ll_opy_ = None
bstack1l1l111l_opy_ = None
bstack111l11ll_opy_ = None
bstack11ll1l1ll_opy_ = None
bstack1111ll111_opy_ = None
bstack1111ll11_opy_ = None
bstack11ll1ll1ll_opy_ = None
bstack111111ll_opy_ = None
bstack1ll11ll111_opy_ = None
bstack111l1l1111_opy_ = None
bstack111llllll_opy_ = None
bstack11l1l111l1_opy_ = None
bstack11l11lll_opy_ = None
bstack1ll1lll111_opy_ = None
bstack11l1ll1ll1_opy_ = None
bstack111llll1ll_opy_ = None
bstack11l1lll1ll_opy_ = None
bstack1111l1lll_opy_ = None
bstack11lllll1_opy_ = None
bstack1l111111ll_opy_ = None
bstack1llll1l1l_opy_ = None
thread_local = threading.local()
bstack1l1lllllll_opy_ = False
bstack1l111ll11_opy_ = bstack11lllll_opy_ (u"ࠦࠧ࣋")
logger = logger_utils.get_logger(__name__, bstack1ll1ll1l11_opy_)
bstack1l111l111l_opy_ = logger_utils.bstack1l1l11111l_opy_(__name__)
bstack1l111111_opy_ = Config.bstack1llll1l111_opy_()
percy = bstack111llll1l1_opy_()
bstack1lll1llll1_opy_ = bstack11l11l11_opy_()
bstack1lllllll1_opy_ = bstack1ll1111l1_opy_()
def bstack1l1111ll11_opy_():
  global CONFIG
  global bstack1ll111l1l_opy_
  global bstack1l111111_opy_
  testContextOptions = bstack111l1111_opy_(CONFIG)
  if bstack1l111lll1l_opy_(CONFIG):
    if (bstack11lllll_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ࣌") in testContextOptions and str(testContextOptions[bstack11lllll_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ࣍")]).lower() == bstack11lllll_opy_ (u"ࠧࡵࡴࡸࡩࠬ࣎")):
      bstack1ll111l1l_opy_ = True
    bstack1l111111_opy_.bstack11l1l11lll_opy_(testContextOptions.get(bstack11lllll_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷ࣏ࠬ"), False))
  else:
    bstack1ll111l1l_opy_ = True
    bstack1l111111_opy_.bstack11l1l11lll_opy_(True)
def bstack1ll111l111_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack111l1ll1l_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack111llll1l_opy_():
  global bstack1l11l11l1_opy_
  args = sys.argv
  for i in range(len(args)):
    if bstack11lllll_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡦࡳࡳ࡬ࡩࡨࡨ࡬ࡰࡪࠨ࣐") == args[i].lower() or bstack11lllll_opy_ (u"ࠥ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡮ࡧ࡫ࡪ࣑ࠦ") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      bstack1l11l11l1_opy_[bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ࣒")] = path
      return path
  return None
bstack1l111111l_opy_ = re.compile(bstack11lllll_opy_ (u"ࡷࠨ࠮ࠫࡁ࡟ࠨࢀ࠮࠮ࠫࡁࠬࢁ࠳࠰࠿࣓ࠣ"))
def bstack1lllll11l_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1l111111l_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack11lllll_opy_ (u"ࠨࠤࡼࠤࣔ") + group + bstack11lllll_opy_ (u"ࠢࡾࠤࣕ"), os.environ.get(group))
  return value
def bstack11lllllll_opy_():
  global bstack1llll1l1l_opy_
  if bstack1llll1l1l_opy_ is None:
        bstack1llll1l1l_opy_ = bstack111llll1l_opy_()
  bstack1ll11lll11_opy_ = bstack1llll1l1l_opy_
  if bstack1ll11lll11_opy_ and os.path.exists(os.path.abspath(bstack1ll11lll11_opy_)):
    fileName = bstack1ll11lll11_opy_
  if bstack11lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬࣖ") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack11lllll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࡠࡈࡌࡐࡊ࠭ࣗ")])) and not bstack11lllll_opy_ (u"ࠪࡪ࡮ࡲࡥࡏࡣࡰࡩࠬࣘ") in locals():
    fileName = os.environ[bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨࣙ")]
  if bstack11lllll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡑࡥࡲ࡫ࠧࣚ") in locals():
    bstack1111ll1_opy_ = os.path.abspath(fileName)
  else:
    bstack1111ll1_opy_ = bstack11lllll_opy_ (u"࠭ࠧࣛ")
  bstack1l1l11ll1_opy_ = os.getcwd()
  bstack11l1l11ll_opy_ = bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪࣜ")
  bstack111111l11_opy_ = bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺࡣࡰࡰࠬࣝ")
  while (not os.path.exists(bstack1111ll1_opy_)) and bstack1l1l11ll1_opy_ != bstack11lllll_opy_ (u"ࠤࠥࣞ"):
    bstack1111ll1_opy_ = os.path.join(bstack1l1l11ll1_opy_, bstack11l1l11ll_opy_)
    if not os.path.exists(bstack1111ll1_opy_):
      bstack1111ll1_opy_ = os.path.join(bstack1l1l11ll1_opy_, bstack111111l11_opy_)
    if bstack1l1l11ll1_opy_ != os.path.dirname(bstack1l1l11ll1_opy_):
      bstack1l1l11ll1_opy_ = os.path.dirname(bstack1l1l11ll1_opy_)
    else:
      bstack1l1l11ll1_opy_ = bstack11lllll_opy_ (u"ࠥࠦࣟ")
  bstack1llll1l1l_opy_ = bstack1111ll1_opy_ if os.path.exists(bstack1111ll1_opy_) else None
  return bstack1llll1l1l_opy_
def bstack11l111111_opy_(config):
    if bstack11lllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࠫ࣠") in config:
      config[bstack11lllll_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ࣡")] = config[bstack11lllll_opy_ (u"࠭ࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬࠭࣢")]
    if bstack11lllll_opy_ (u"ࠧࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭ࡏࡱࡶ࡬ࡳࡳࡹࣣࠧ") in config:
      config[bstack11lllll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬࣤ")] = config[bstack11lllll_opy_ (u"ࠩࡷࡩࡸࡺࡒࡦࡲࡲࡶࡹ࡯࡮ࡨࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣥ")]
def bstack1l11l11l1l_opy_():
  bstack1111ll1_opy_ = bstack11lllllll_opy_()
  if not os.path.exists(bstack1111ll1_opy_):
    bstack11l1ll11l1_opy_(
      bstack1l1ll1l1_opy_.format(os.getcwd()))
  try:
    with open(bstack1111ll1_opy_, bstack11lllll_opy_ (u"ࠪࡶࣦࠬ")) as stream:
      yaml.add_implicit_resolver(bstack11lllll_opy_ (u"ࠦࠦࡶࡡࡵࡪࡨࡼࠧࣧ"), bstack1l111111l_opy_)
      yaml.add_constructor(bstack11lllll_opy_ (u"ࠧࠧࡰࡢࡶ࡫ࡩࡽࠨࣨ"), bstack1lllll11l_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      bstack11l111111_opy_(config)
      return config
  except:
    with open(bstack1111ll1_opy_, bstack11lllll_opy_ (u"࠭ࡲࠨࣩ")) as stream:
      try:
        config = yaml.safe_load(stream)
        bstack11l111111_opy_(config)
        return config
      except yaml.YAMLError as exc:
        bstack11l1ll11l1_opy_(bstack1lll1lll11_opy_.format(str(exc)))
def bstack1ll111l11l_opy_(config):
  bstack1llll11l11_opy_ = bstack111ll11ll_opy_(config)
  for option in list(bstack1llll11l11_opy_):
    if option.lower() in bstack111l1l111_opy_ and option != bstack111l1l111_opy_[option.lower()]:
      bstack1llll11l11_opy_[bstack111l1l111_opy_[option.lower()]] = bstack1llll11l11_opy_[option]
      del bstack1llll11l11_opy_[option]
  return config
def bstack1l1l1ll1_opy_():
  global bstack111lllll11_opy_
  for key, bstack1l1ll111l_opy_ in bstack1ll1ll1ll1_opy_.items():
    if isinstance(bstack1l1ll111l_opy_, list):
      for var in bstack1l1ll111l_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack111lllll11_opy_[key] = os.environ[var]
          break
    elif bstack1l1ll111l_opy_ in os.environ and os.environ[bstack1l1ll111l_opy_] and str(os.environ[bstack1l1ll111l_opy_]).strip():
      bstack111lllll11_opy_[key] = os.environ[bstack1l1ll111l_opy_]
  if bstack11lllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩ࣪") in os.environ:
    bstack111lllll11_opy_[bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ࣫")] = {}
    bstack111lllll11_opy_[bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭࣬")][bstack11lllll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ࣭ࠬ")] = os.environ[bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࣮࠭")]
def bstack1llll1ll_opy_():
  global bstack1l111l11l_opy_
  global bstack1ll1l11ll1_opy_
  global bstack1l11l11l1_opy_
  bstack1ll1ll11ll_opy_ = []
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) - 1 and bstack11lllll_opy_ (u"ࠬ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ࣯").lower() == val.lower():
      bstack1l111l11l_opy_[bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࣰࠪ")] = {}
      bstack1l111l11l_opy_[bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࣱࠫ")][bstack11lllll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࣲࠪ")] = sys.argv[idx + 1]
      bstack1ll1ll11ll_opy_.extend([idx, idx + 1])
      break
  for key, bstack1ll1lll11_opy_ in bstack11l11l1l1l_opy_.items():
    if isinstance(bstack1ll1lll11_opy_, list):
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        for var in bstack1ll1lll11_opy_:
          if bstack11lllll_opy_ (u"ࠩ࠰࠱ࠬࣳ") + var.lower() == val.lower() and key not in bstack1l111l11l_opy_:
            bstack1l111l11l_opy_[key] = sys.argv[idx + 1]
            bstack1ll1l11ll1_opy_ += bstack11lllll_opy_ (u"ࠪࠤ࠲࠳ࠧࣴ") + var + bstack11lllll_opy_ (u"ࠫࠥ࠭ࣵ") + shlex.quote(sys.argv[idx + 1])
            bstack1l1l1111_opy_(bstack1l11l11l1_opy_, key, sys.argv[idx + 1])
            bstack1ll1ll11ll_opy_.extend([idx, idx + 1])
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        if bstack11lllll_opy_ (u"ࠬ࠳࠭ࠨࣶ") + bstack1ll1lll11_opy_.lower() == val.lower() and key not in bstack1l111l11l_opy_:
          bstack1l111l11l_opy_[key] = sys.argv[idx + 1]
          bstack1ll1l11ll1_opy_ += bstack11lllll_opy_ (u"࠭ࠠ࠮࠯ࠪࣷ") + bstack1ll1lll11_opy_ + bstack11lllll_opy_ (u"ࠧࠡࠩࣸ") + shlex.quote(sys.argv[idx + 1])
          bstack1l1l1111_opy_(bstack1l11l11l1_opy_, key, sys.argv[idx + 1])
          bstack1ll1ll11ll_opy_.extend([idx, idx + 1])
  for idx in sorted(set(bstack1ll1ll11ll_opy_), reverse=True):
    if idx < len(sys.argv):
      del sys.argv[idx]
def bstack1ll11ll1l1_opy_(config):
  bstack111l1l1lll_opy_ = config.keys()
  for bstack11l1ll11l_opy_, bstack11111ll11_opy_ in bstack111ll111l1_opy_.items():
    if bstack11111ll11_opy_ in bstack111l1l1lll_opy_:
      config[bstack11l1ll11l_opy_] = config[bstack11111ll11_opy_]
      del config[bstack11111ll11_opy_]
  for bstack11l1ll11l_opy_, bstack11111ll11_opy_ in bstack11l11l1ll1_opy_.items():
    if isinstance(bstack11111ll11_opy_, list):
      for bstack11ll1l1l1l_opy_ in bstack11111ll11_opy_:
        if bstack11ll1l1l1l_opy_ in bstack111l1l1lll_opy_:
          config[bstack11l1ll11l_opy_] = config[bstack11ll1l1l1l_opy_]
          del config[bstack11ll1l1l1l_opy_]
          break
    elif bstack11111ll11_opy_ in bstack111l1l1lll_opy_:
      config[bstack11l1ll11l_opy_] = config[bstack11111ll11_opy_]
      del config[bstack11111ll11_opy_]
  for bstack11ll1l1l1l_opy_ in list(config):
    for bstack1lll11l11_opy_ in bstack11l11lllll_opy_:
      if bstack11ll1l1l1l_opy_.lower() == bstack1lll11l11_opy_.lower() and bstack11ll1l1l1l_opy_ != bstack1lll11l11_opy_:
        config[bstack1lll11l11_opy_] = config[bstack11ll1l1l1l_opy_]
        del config[bstack11ll1l1l1l_opy_]
  bstack1l1l1ll111_opy_ = [{}]
  if not config.get(bstack11lllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࣹࠫ")):
    config[bstack11lllll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࣺࠬ")] = [{}]
  bstack1l1l1ll111_opy_ = config[bstack11lllll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣻ")]
  for platform in bstack1l1l1ll111_opy_:
    for bstack11ll1l1l1l_opy_ in list(platform):
      for bstack1lll11l11_opy_ in bstack11l11lllll_opy_:
        if bstack11ll1l1l1l_opy_.lower() == bstack1lll11l11_opy_.lower() and bstack11ll1l1l1l_opy_ != bstack1lll11l11_opy_:
          platform[bstack1lll11l11_opy_] = platform[bstack11ll1l1l1l_opy_]
          del platform[bstack11ll1l1l1l_opy_]
  for bstack11l1ll11l_opy_, bstack11111ll11_opy_ in bstack11l11l1ll1_opy_.items():
    for platform in bstack1l1l1ll111_opy_:
      if isinstance(bstack11111ll11_opy_, list):
        for bstack11ll1l1l1l_opy_ in bstack11111ll11_opy_:
          if bstack11ll1l1l1l_opy_ in platform:
            platform[bstack11l1ll11l_opy_] = platform[bstack11ll1l1l1l_opy_]
            del platform[bstack11ll1l1l1l_opy_]
            break
      elif bstack11111ll11_opy_ in platform:
        platform[bstack11l1ll11l_opy_] = platform[bstack11111ll11_opy_]
        del platform[bstack11111ll11_opy_]
  for bstack111ll111l_opy_ in bstack1l11l1l11l_opy_:
    if bstack111ll111l_opy_ in config:
      if not bstack1l11l1l11l_opy_[bstack111ll111l_opy_] in config:
        config[bstack1l11l1l11l_opy_[bstack111ll111l_opy_]] = {}
      config[bstack1l11l1l11l_opy_[bstack111ll111l_opy_]].update(config[bstack111ll111l_opy_])
      del config[bstack111ll111l_opy_]
  for platform in bstack1l1l1ll111_opy_:
    for bstack111ll111l_opy_ in bstack1l11l1l11l_opy_:
      if bstack111ll111l_opy_ in list(platform):
        if not bstack1l11l1l11l_opy_[bstack111ll111l_opy_] in platform:
          platform[bstack1l11l1l11l_opy_[bstack111ll111l_opy_]] = {}
        platform[bstack1l11l1l11l_opy_[bstack111ll111l_opy_]].update(platform[bstack111ll111l_opy_])
        del platform[bstack111ll111l_opy_]
  config = bstack1ll111l11l_opy_(config)
  return config
def bstack11lll11ll1_opy_(config):
  global bstack1lll1ll11l_opy_
  bstack11ll11111_opy_ = False
  if bstack11lllll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨࣼ") in config and str(config[bstack11lllll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩࣽ")]).lower() != bstack11lllll_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬࣾ"):
    if bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫࣿ") not in config or str(config[bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬऀ")]).lower() == bstack11lllll_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨँ"):
      config[bstack11lllll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩं")] = False
    else:
      bstack11lll1ll_opy_ = bstack11111l11_opy_()
      if bstack11lllll_opy_ (u"ࠫ࡮ࡹࡔࡳ࡫ࡤࡰࡌࡸࡩࡥࠩः") in bstack11lll1ll_opy_:
        if not bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩऄ") in config:
          config[bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪअ")] = {}
        config[bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫआ")][bstack11lllll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪइ")] = bstack11lllll_opy_ (u"ࠩࡤࡸࡸ࠳ࡲࡦࡲࡨࡥࡹ࡫ࡲࠨई")
        bstack11ll11111_opy_ = True
        bstack1lll1ll11l_opy_ = config[bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧउ")].get(bstack11lllll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ऊ"))
  if bstack1l111lll1l_opy_(config) and bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩऋ") in config and str(config[bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪऌ")]).lower() != bstack11lllll_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ऍ") and not bstack11ll11111_opy_:
    if not bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬऎ") in config:
      config[bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ए")] = {}
    if not config[bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧऐ")].get(bstack11lllll_opy_ (u"ࠫࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠨऑ")) and not bstack11lllll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऒ") in config[bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪओ")]:
      bstack1lll11lll1_opy_ = datetime.datetime.now()
      bstack11ll11l111_opy_ = bstack1lll11lll1_opy_.strftime(bstack11lllll_opy_ (u"ࠧࠦࡦࡢࠩࡧࡥࠥࡉࠧࡐࠫऔ"))
      hostname = socket.gethostname()
      bstack1ll11l1l1_opy_ = bstack11lllll_opy_ (u"ࠨࠩक").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack11lllll_opy_ (u"ࠩࡾࢁࡤࢁࡽࡠࡽࢀࠫख").format(bstack11ll11l111_opy_, hostname, bstack1ll11l1l1_opy_)
      config[bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧग")][bstack11lllll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭घ")] = identifier
    bstack1lll1ll11l_opy_ = config[bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩङ")].get(bstack11lllll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨच"))
  return config
def bstack11l1ll111l_opy_():
  bstack11lll11l11_opy_ =  bstack11ll1lll1l_opy_()[bstack11lllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷ࠭छ")]
  return bstack11lll11l11_opy_ if bstack11lll11l11_opy_ else -1
def bstack1l1lll111l_opy_(bstack11lll11l11_opy_):
  global CONFIG
  if not bstack11lllll_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪज") in CONFIG[bstack11lllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫझ")]:
    return
  CONFIG[bstack11lllll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬञ")] = CONFIG[bstack11lllll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ट")].replace(
    bstack11lllll_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧठ"),
    str(bstack11lll11l11_opy_)
  )
def bstack1l11lllll1_opy_():
  global CONFIG
  if not bstack11lllll_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬड") in CONFIG[bstack11lllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩढ")]:
    return
  bstack1lll11lll1_opy_ = datetime.datetime.now()
  bstack11ll11l111_opy_ = bstack1lll11lll1_opy_.strftime(bstack11lllll_opy_ (u"ࠨࠧࡧ࠱ࠪࡨ࠭ࠦࡊ࠽ࠩࡒ࠭ण"))
  CONFIG[bstack11lllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫत")] = CONFIG[bstack11lllll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬथ")].replace(
    bstack11lllll_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪद"),
    bstack11ll11l111_opy_
  )
def bstack11l111l11_opy_():
  global CONFIG
  if bstack11lllll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧध") in CONFIG and not bool(CONFIG[bstack11lllll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨन")]):
    del CONFIG[bstack11lllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऩ")]
    return
  if not bstack11lllll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪप") in CONFIG:
    CONFIG[bstack11lllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫफ")] = bstack11lllll_opy_ (u"ࠪࠧࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ब")
  if bstack11lllll_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪभ") in CONFIG[bstack11lllll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧम")]:
    bstack1l11lllll1_opy_()
    os.environ[bstack11lllll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪय")] = CONFIG[bstack11lllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩर")]
  if not bstack11lllll_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪऱ") in CONFIG[bstack11lllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫल")]:
    return
  bstack11lll11l11_opy_ = bstack11lllll_opy_ (u"ࠪࠫळ")
  bstack1ll11111l1_opy_ = bstack11l1ll111l_opy_()
  if bstack1ll11111l1_opy_ != -1:
    bstack11lll11l11_opy_ = bstack11lllll_opy_ (u"ࠫࡈࡏࠠࠨऴ") + str(bstack1ll11111l1_opy_)
  if bstack11lll11l11_opy_ == bstack11lllll_opy_ (u"ࠬ࠭व"):
    bstack1l11l111l_opy_ = bstack1ll1l111_opy_(CONFIG[bstack11lllll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩश")])
    if bstack1l11l111l_opy_ != -1:
      bstack11lll11l11_opy_ = str(bstack1l11l111l_opy_)
  if bstack11lll11l11_opy_:
    bstack1l1lll111l_opy_(bstack11lll11l11_opy_)
    os.environ[bstack11lllll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫष")] = CONFIG[bstack11lllll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪस")]
def bstack1lllll111l_opy_(bstack11l1111111_opy_, bstack111lll11l1_opy_, path):
  bstack111l1l1l11_opy_ = {
    bstack11lllll_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ह"): bstack111lll11l1_opy_
  }
  if os.path.exists(path):
    bstack1ll1ll1l1_opy_ = json.load(open(path, bstack11lllll_opy_ (u"ࠪࡶࡧ࠭ऺ")))
  else:
    bstack1ll1ll1l1_opy_ = {}
  bstack1ll1ll1l1_opy_[bstack11l1111111_opy_] = bstack111l1l1l11_opy_
  with open(path, bstack11lllll_opy_ (u"ࠦࡼ࠱ࠢऻ")) as outfile:
    json.dump(bstack1ll1ll1l1_opy_, outfile)
def bstack1ll1l111_opy_(bstack11l1111111_opy_):
  bstack11l1111111_opy_ = str(bstack11l1111111_opy_)
  bstack1111l11ll_opy_ = os.path.join(os.path.expanduser(bstack11lllll_opy_ (u"ࠬࢄ़ࠧ")), bstack11lllll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ऽ"))
  try:
    if not os.path.exists(bstack1111l11ll_opy_):
      os.makedirs(bstack1111l11ll_opy_)
    file_path = os.path.join(os.path.expanduser(bstack11lllll_opy_ (u"ࠧࡿࠩा")), bstack11lllll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨि"), bstack11lllll_opy_ (u"ࠩ࠱ࡦࡺ࡯࡬ࡥ࠯ࡱࡥࡲ࡫࠭ࡤࡣࡦ࡬ࡪ࠴ࡪࡴࡱࡱࠫी"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack11lllll_opy_ (u"ࠪࡻࠬु")):
        pass
      with open(file_path, bstack11lllll_opy_ (u"ࠦࡼ࠱ࠢू")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack11lllll_opy_ (u"ࠬࡸࠧृ")) as bstack1111ll1l1_opy_:
      bstack11l111l1l_opy_ = json.load(bstack1111ll1l1_opy_)
    if bstack11l1111111_opy_ in bstack11l111l1l_opy_:
      bstack1l11l1ll11_opy_ = bstack11l111l1l_opy_[bstack11l1111111_opy_][bstack11lllll_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪॄ")]
      bstack1ll111llll_opy_ = int(bstack1l11l1ll11_opy_) + 1
      bstack1lllll111l_opy_(bstack11l1111111_opy_, bstack1ll111llll_opy_, file_path)
      return bstack1ll111llll_opy_
    else:
      bstack1lllll111l_opy_(bstack11l1111111_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warning(bstack11l1llll_opy_.format(str(e)))
    return -1
def bstack1l1lll1ll1_opy_(config):
  if not config[bstack11lllll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩॅ")] or not config[bstack11lllll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫॆ")]:
    return True
  else:
    return False
def bstack1llll1lll1_opy_(config, index=0):
  global bstack1l1lll1l1_opy_
  bstack1ll1ll1l1l_opy_ = {}
  caps = bstack1l111l1ll1_opy_ + bstack1l1l11ll1l_opy_
  if config.get(bstack11lllll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭े"), False):
    bstack1ll1ll1l1l_opy_[bstack11lllll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧै")] = True
    bstack1ll1ll1l1l_opy_[bstack11lllll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࡐࡲࡷ࡭ࡴࡴࡳࠨॉ")] = config.get(bstack11lllll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩॊ"), {})
  if bstack1l1lll1l1_opy_:
    caps += bstack11111ll1l_opy_
  for key in config:
    if key in caps + [bstack11lllll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩो")]:
      continue
    bstack1ll1ll1l1l_opy_[key] = config[key]
  if bstack11lllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪौ") in config:
    for bstack111ll11111_opy_ in config[bstack11lllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶ्ࠫ")][index]:
      if bstack111ll11111_opy_ in caps:
        continue
      bstack1ll1ll1l1l_opy_[bstack111ll11111_opy_] = config[bstack11lllll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॎ")][index][bstack111ll11111_opy_]
  bstack1ll1ll1l1l_opy_[bstack11lllll_opy_ (u"ࠪ࡬ࡴࡹࡴࡏࡣࡰࡩࠬॏ")] = socket.gethostname()
  if bstack11lllll_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬॐ") in bstack1ll1ll1l1l_opy_:
    del (bstack1ll1ll1l1l_opy_[bstack11lllll_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭॑")])
  return bstack1ll1ll1l1l_opy_
def bstack1l1l1l11_opy_(config):
  global bstack1l1lll1l1_opy_
  bstack11ll11ll1_opy_ = {}
  caps = bstack1l1l11ll1l_opy_
  if bstack1l1lll1l1_opy_:
    caps += bstack11111ll1l_opy_
  for key in caps:
    if key in config:
      bstack11ll11ll1_opy_[key] = config[key]
  return bstack11ll11ll1_opy_
def bstack1ll1ll11_opy_(bstack1ll1ll1l1l_opy_, bstack11ll11ll1_opy_):
  bstack1lllllllll_opy_ = {}
  for key in bstack1ll1ll1l1l_opy_.keys():
    if key in bstack111ll111l1_opy_:
      bstack1lllllllll_opy_[bstack111ll111l1_opy_[key]] = bstack1ll1ll1l1l_opy_[key]
    else:
      bstack1lllllllll_opy_[key] = bstack1ll1ll1l1l_opy_[key]
  for key in bstack11ll11ll1_opy_:
    if key in bstack111ll111l1_opy_:
      bstack1lllllllll_opy_[bstack111ll111l1_opy_[key]] = bstack11ll11ll1_opy_[key]
    else:
      bstack1lllllllll_opy_[key] = bstack11ll11ll1_opy_[key]
  return bstack1lllllllll_opy_
def bstack1lll11llll_opy_(config, index=0):
  global bstack1l1lll1l1_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack11l11ll111_opy_ = bstack1l1ll1ll_opy_(bstack111ll1l111_opy_, config, logger)
  bstack11ll11ll1_opy_ = bstack1l1l1l11_opy_(config)
  bstack11111l11l_opy_ = bstack1l1l11ll1l_opy_
  bstack11111l11l_opy_ += bstack1ll11l11ll_opy_
  bstack11ll11ll1_opy_ = update(bstack11ll11ll1_opy_, bstack11l11ll111_opy_)
  if bstack1l1lll1l1_opy_:
    bstack11111l11l_opy_ += bstack11111ll1l_opy_
  if bstack11lllll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴ॒ࠩ") in config:
    if bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ॓") in config[bstack11lllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ॔")][index]:
      caps[bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧॕ")] = config[bstack11lllll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॖ")][index][bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩॗ")]
    if bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭क़") in config[bstack11lllll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩख़")][index]:
      caps[bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨग़")] = str(config[bstack11lllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫज़")][index][bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪड़")])
    bstack1llll111l_opy_ = bstack1l1ll1ll_opy_(bstack111ll1l111_opy_, config[bstack11lllll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ढ़")][index], logger)
    bstack11111l11l_opy_ += list(bstack1llll111l_opy_.keys())
    for bstack11lll1l11_opy_ in bstack11111l11l_opy_:
      if bstack11lll1l11_opy_ in config[bstack11lllll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧफ़")][index]:
        if bstack11lll1l11_opy_ == bstack11lllll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧय़"):
          try:
            bstack1llll111l_opy_[bstack11lll1l11_opy_] = str(config[bstack11lllll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩॠ")][index][bstack11lll1l11_opy_] * 1.0)
          except:
            bstack1llll111l_opy_[bstack11lll1l11_opy_] = str(config[bstack11lllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪॡ")][index][bstack11lll1l11_opy_])
        else:
          bstack1llll111l_opy_[bstack11lll1l11_opy_] = config[bstack11lllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫॢ")][index][bstack11lll1l11_opy_]
        del (config[bstack11lllll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॣ")][index][bstack11lll1l11_opy_])
    bstack11ll11ll1_opy_ = update(bstack11ll11ll1_opy_, bstack1llll111l_opy_)
  bstack1ll1ll1l1l_opy_ = bstack1llll1lll1_opy_(config, index)
  for bstack11ll1l1l1l_opy_ in bstack1l1l11ll1l_opy_ + list(bstack11l11ll111_opy_.keys()):
    if bstack11ll1l1l1l_opy_ in bstack1ll1ll1l1l_opy_:
      bstack11ll11ll1_opy_[bstack11ll1l1l1l_opy_] = bstack1ll1ll1l1l_opy_[bstack11ll1l1l1l_opy_]
      del (bstack1ll1ll1l1l_opy_[bstack11ll1l1l1l_opy_])
  if bstack1l1ll11ll_opy_(config):
    bstack1ll1ll1l1l_opy_[bstack11lllll_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ।")] = True
    caps.update(bstack11ll11ll1_opy_)
    caps[bstack11lllll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ॥")] = bstack1ll1ll1l1l_opy_
  else:
    bstack1ll1ll1l1l_opy_[bstack11lllll_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ०")] = False
    caps.update(bstack1ll1ll11_opy_(bstack1ll1ll1l1l_opy_, bstack11ll11ll1_opy_))
    if bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ१") in caps:
      caps[bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ२")] = caps[bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭३")]
      del (caps[bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ४")])
    if bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ५") in caps:
      caps[bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭६")] = caps[bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭७")]
      del (caps[bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ८")])
  return caps
def bstack1l1llll111_opy_():
  global bstack11l1ll111_opy_
  global CONFIG
  if bstack111l1ll1l_opy_() <= version.parse(bstack11lllll_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧ९")):
    if bstack11l1ll111_opy_ != bstack11lllll_opy_ (u"ࠨࠩ॰"):
      return bstack11lllll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥॱ") + bstack11l1ll111_opy_ + bstack11lllll_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢॲ")
    return bstack11l11ll11l_opy_
  if bstack11l1ll111_opy_ != bstack11lllll_opy_ (u"ࠫࠬॳ"):
    return bstack11lllll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢॴ") + bstack11l1ll111_opy_ + bstack11lllll_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢॵ")
  return bstack1ll1111l_opy_
def bstack111ll11lll_opy_(options):
  return hasattr(options, bstack11lllll_opy_ (u"ࠧࡴࡧࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠨॶ"))
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
def bstack1l111lll11_opy_(options, bstack1ll11l11l_opy_):
  for bstack1l111111l1_opy_ in bstack1ll11l11l_opy_:
    if bstack1l111111l1_opy_ in [bstack11lllll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ॷ"), bstack11lllll_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ॸ")]:
      continue
    if bstack1l111111l1_opy_ in options._experimental_options:
      options._experimental_options[bstack1l111111l1_opy_] = update(options._experimental_options[bstack1l111111l1_opy_],
                                                         bstack1ll11l11l_opy_[bstack1l111111l1_opy_])
    else:
      options.add_experimental_option(bstack1l111111l1_opy_, bstack1ll11l11l_opy_[bstack1l111111l1_opy_])
  if bstack11lllll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨॹ") in bstack1ll11l11l_opy_:
    for arg in bstack1ll11l11l_opy_[bstack11lllll_opy_ (u"ࠫࡦࡸࡧࡴࠩॺ")]:
      options.add_argument(arg)
    del (bstack1ll11l11l_opy_[bstack11lllll_opy_ (u"ࠬࡧࡲࡨࡵࠪॻ")])
  if bstack11lllll_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪॼ") in bstack1ll11l11l_opy_:
    for ext in bstack1ll11l11l_opy_[bstack11lllll_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫॽ")]:
      try:
        options.add_extension(ext)
      except OSError:
        options.add_encoded_extension(ext)
    del (bstack1ll11l11l_opy_[bstack11lllll_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬॾ")])
def bstack1l111ll1l1_opy_(options, bstack1l1l1l1lll_opy_):
  if bstack11lllll_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨॿ") in bstack1l1l1l1lll_opy_:
    for bstack1l1ll1l1l_opy_ in bstack1l1l1l1lll_opy_[bstack11lllll_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩঀ")]:
      if bstack1l1ll1l1l_opy_ in options._preferences:
        options._preferences[bstack1l1ll1l1l_opy_] = update(options._preferences[bstack1l1ll1l1l_opy_], bstack1l1l1l1lll_opy_[bstack11lllll_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪঁ")][bstack1l1ll1l1l_opy_])
      else:
        options.set_preference(bstack1l1ll1l1l_opy_, bstack1l1l1l1lll_opy_[bstack11lllll_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫং")][bstack1l1ll1l1l_opy_])
  if bstack11lllll_opy_ (u"࠭ࡡࡳࡩࡶࠫঃ") in bstack1l1l1l1lll_opy_:
    for arg in bstack1l1l1l1lll_opy_[bstack11lllll_opy_ (u"ࠧࡢࡴࡪࡷࠬ঄")]:
      options.add_argument(arg)
def bstack11l1llll1l_opy_(options, bstack111l1ll11l_opy_):
  if bstack11lllll_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࠩঅ") in bstack111l1ll11l_opy_:
    options.use_webview(bool(bstack111l1ll11l_opy_[bstack11lllll_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࠪআ")]))
  bstack1l111lll11_opy_(options, bstack111l1ll11l_opy_)
def bstack11l1l1l1l_opy_(options, bstack1lll1ll1l1_opy_):
  for bstack111l111lll_opy_ in bstack1lll1ll1l1_opy_:
    if bstack111l111lll_opy_ in [bstack11lllll_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧই"), bstack11lllll_opy_ (u"ࠫࡦࡸࡧࡴࠩঈ")]:
      continue
    options.set_capability(bstack111l111lll_opy_, bstack1lll1ll1l1_opy_[bstack111l111lll_opy_])
  if bstack11lllll_opy_ (u"ࠬࡧࡲࡨࡵࠪউ") in bstack1lll1ll1l1_opy_:
    for arg in bstack1lll1ll1l1_opy_[bstack11lllll_opy_ (u"࠭ࡡࡳࡩࡶࠫঊ")]:
      options.add_argument(arg)
  if bstack11lllll_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫঋ") in bstack1lll1ll1l1_opy_:
    options.bstack1l1l1ll11l_opy_(bool(bstack1lll1ll1l1_opy_[bstack11lllll_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬঌ")]))
def bstack1ll1l1llll_opy_(options, bstack11ll1111l1_opy_):
  for bstack11l1111ll_opy_ in bstack11ll1111l1_opy_:
    if bstack11l1111ll_opy_ in [bstack11lllll_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭঍"), bstack11lllll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ঎")]:
      continue
    options._options[bstack11l1111ll_opy_] = bstack11ll1111l1_opy_[bstack11l1111ll_opy_]
  if bstack11lllll_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨএ") in bstack11ll1111l1_opy_:
    for bstack1111lll1l_opy_ in bstack11ll1111l1_opy_[bstack11lllll_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩঐ")]:
      options.bstack1ll1lllll_opy_(
        bstack1111lll1l_opy_, bstack11ll1111l1_opy_[bstack11lllll_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ঑")][bstack1111lll1l_opy_])
  if bstack11lllll_opy_ (u"ࠧࡢࡴࡪࡷࠬ঒") in bstack11ll1111l1_opy_:
    for arg in bstack11ll1111l1_opy_[bstack11lllll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ও")]:
      options.add_argument(arg)
def bstack1l11l1111_opy_(options, caps):
  if not hasattr(options, bstack11lllll_opy_ (u"ࠩࡎࡉ࡞࠭ঔ")):
    return
  if options.KEY == bstack11lllll_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨক"):
    options = bstack11l1llll11_opy_.bstack11111l1l_opy_(bstack111ll1ll1_opy_=options, config=CONFIG)
  if options.KEY == bstack11lllll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩখ") and options.KEY in caps:
    bstack1l111lll11_opy_(options, caps[bstack11lllll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪগ")])
  elif options.KEY == bstack11lllll_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫঘ") and options.KEY in caps:
    bstack1l111ll1l1_opy_(options, caps[bstack11lllll_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬঙ")])
  elif options.KEY == bstack11lllll_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩচ") and options.KEY in caps:
    bstack11l1l1l1l_opy_(options, caps[bstack11lllll_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪছ")])
  elif options.KEY == bstack11lllll_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫজ") and options.KEY in caps:
    bstack11l1llll1l_opy_(options, caps[bstack11lllll_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬঝ")])
  elif options.KEY == bstack11lllll_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫঞ") and options.KEY in caps:
    bstack1ll1l1llll_opy_(options, caps[bstack11lllll_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬট")])
def bstack1l111llll1_opy_(caps):
  global bstack1l1lll1l1_opy_
  if isinstance(os.environ.get(bstack11lllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨঠ")), str):
    bstack1l1lll1l1_opy_ = eval(os.getenv(bstack11lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩড")))
  if bstack1l1lll1l1_opy_:
    if bstack1ll111l111_opy_() < version.parse(bstack11lllll_opy_ (u"ࠩ࠵࠲࠸࠴࠰ࠨঢ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack11lllll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪণ")
    if bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩত") in caps:
      browser = caps[bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪথ")]
    elif bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧদ") in caps:
      browser = caps[bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨধ")]
    browser = str(browser).lower()
    if browser == bstack11lllll_opy_ (u"ࠨ࡫ࡳ࡬ࡴࡴࡥࠨন") or browser == bstack11lllll_opy_ (u"ࠩ࡬ࡴࡦࡪࠧ঩"):
      browser = bstack11lllll_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪপ")
    if browser == bstack11lllll_opy_ (u"ࠫࡸࡧ࡭ࡴࡷࡱ࡫ࠬফ"):
      browser = bstack11lllll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬব")
    if browser not in [bstack11lllll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ভ"), bstack11lllll_opy_ (u"ࠧࡦࡦࡪࡩࠬম"), bstack11lllll_opy_ (u"ࠨ࡫ࡨࠫয"), bstack11lllll_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩর"), bstack11lllll_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫ঱")]:
      return None
    try:
      package = bstack11lllll_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳ࠰ࡾࢁ࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ল").format(browser)
      name = bstack11lllll_opy_ (u"ࠬࡕࡰࡵ࡫ࡲࡲࡸ࠭঳")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack111ll11lll_opy_(options):
        return None
      for bstack11ll1l1l1l_opy_ in caps.keys():
        options.set_capability(bstack11ll1l1l1l_opy_, caps[bstack11ll1l1l1l_opy_])
      bstack1l11l1111_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack11l111l11l_opy_(options, bstack1llllll11_opy_):
  if not bstack111ll11lll_opy_(options):
    return
  for bstack11ll1l1l1l_opy_ in bstack1llllll11_opy_.keys():
    if bstack11ll1l1l1l_opy_ in bstack1ll11l11ll_opy_:
      continue
    if bstack11ll1l1l1l_opy_ in options._caps and type(options._caps[bstack11ll1l1l1l_opy_]) in [dict, list]:
      options._caps[bstack11ll1l1l1l_opy_] = update(options._caps[bstack11ll1l1l1l_opy_], bstack1llllll11_opy_[bstack11ll1l1l1l_opy_])
    else:
      options.set_capability(bstack11ll1l1l1l_opy_, bstack1llllll11_opy_[bstack11ll1l1l1l_opy_])
  bstack1l11l1111_opy_(options, bstack1llllll11_opy_)
  if bstack11lllll_opy_ (u"࠭࡭ࡰࡼ࠽ࡨࡪࡨࡵࡨࡩࡨࡶࡆࡪࡤࡳࡧࡶࡷࠬ঴") in options._caps:
    if options._caps[bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ঵")] and options._caps[bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭শ")].lower() != bstack11lllll_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪষ"):
      del options._caps[bstack11lllll_opy_ (u"ࠪࡱࡴࢀ࠺ࡥࡧࡥࡹ࡬࡭ࡥࡳࡃࡧࡨࡷ࡫ࡳࡴࠩস")]
def bstack111llll11l_opy_(proxy_config):
  if bstack11lllll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨহ") in proxy_config:
    proxy_config[bstack11lllll_opy_ (u"ࠬࡹࡳ࡭ࡒࡵࡳࡽࡿࠧ঺")] = proxy_config[bstack11lllll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ঻")]
    del (proxy_config[bstack11lllll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼ়ࠫ")])
  if bstack11lllll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫঽ") in proxy_config and proxy_config[bstack11lllll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬা")].lower() != bstack11lllll_opy_ (u"ࠪࡨ࡮ࡸࡥࡤࡶࠪি"):
    proxy_config[bstack11lllll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧী")] = bstack11lllll_opy_ (u"ࠬࡳࡡ࡯ࡷࡤࡰࠬু")
  if bstack11lllll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡆࡻࡴࡰࡥࡲࡲ࡫࡯ࡧࡖࡴ࡯ࠫূ") in proxy_config:
    proxy_config[bstack11lllll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪৃ")] = bstack11lllll_opy_ (u"ࠨࡲࡤࡧࠬৄ")
  return proxy_config
def bstack1lll1ll11_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack11lllll_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨ৅") in config:
    return proxy
  config[bstack11lllll_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩ৆")] = bstack111llll11l_opy_(config[bstack11lllll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪে")])
  if proxy == None:
    proxy = Proxy(config[bstack11lllll_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫৈ")])
  return proxy
def bstack1lllll111_opy_(self):
  global CONFIG
  global bstack111l1l1111_opy_
  try:
    proxy = bstack1l1l1l1ll1_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack11lllll_opy_ (u"࠭࠮ࡱࡣࡦࠫ৉")):
        proxies = bstack1l11lll11_opy_(proxy, bstack1l1llll111_opy_())
        if len(proxies) > 0:
          protocol, bstack111111111_opy_ = proxies.popitem()
          if bstack11lllll_opy_ (u"ࠢ࠻࠱࠲ࠦ৊") in bstack111111111_opy_:
            return bstack111111111_opy_
          else:
            return bstack11lllll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤো") + bstack111111111_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack11lllll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡶࡲࡰࡺࡼࠤࡺࡸ࡬ࠡ࠼ࠣࡿࢂࠨৌ").format(str(e)))
  return bstack111l1l1111_opy_(self)
def bstack11lllllll1_opy_():
  global CONFIG
  return bstack1ll11l111l_opy_(CONFIG) and bstack1ll1l111ll_opy_() and bstack111l1ll1l_opy_() >= version.parse(bstack1ll11l1lll_opy_)
def bstack1ll1llll11_opy_():
  global CONFIG
  return (bstack11lllll_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ্࠭") in CONFIG or bstack11lllll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨৎ") in CONFIG) and bstack111llll111_opy_()
def bstack111ll11ll_opy_(config):
  bstack1llll11l11_opy_ = {}
  if bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ৏") in config:
    bstack1llll11l11_opy_ = config[bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ৐")]
  if bstack11lllll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭৑") in config:
    bstack1llll11l11_opy_ = config[bstack11lllll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ৒")]
  proxy = bstack1l1l1l1ll1_opy_(config)
  if proxy:
    if proxy.endswith(bstack11lllll_opy_ (u"ࠩ࠱ࡴࡦࡩࠧ৓")) and os.path.isfile(proxy):
      bstack1llll11l11_opy_[bstack11lllll_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭৔")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack11lllll_opy_ (u"ࠫ࠳ࡶࡡࡤࠩ৕")):
        proxies = bstack11l1l1111_opy_(config, bstack1l1llll111_opy_())
        if len(proxies) > 0:
          protocol, bstack111111111_opy_ = proxies.popitem()
          if bstack11lllll_opy_ (u"ࠧࡀ࠯࠰ࠤ৖") in bstack111111111_opy_:
            parsed_url = urlparse(bstack111111111_opy_)
          else:
            parsed_url = urlparse(protocol + bstack11lllll_opy_ (u"ࠨ࠺࠰࠱ࠥৗ") + bstack111111111_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1llll11l11_opy_[bstack11lllll_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪ৘")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1llll11l11_opy_[bstack11lllll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡰࡴࡷࠫ৙")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1llll11l11_opy_[bstack11lllll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬ৚")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1llll11l11_opy_[bstack11lllll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭৛")] = str(parsed_url.password)
  return bstack1llll11l11_opy_
def bstack111l1111_opy_(config):
  if bstack11lllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩড়") in config:
    return config[bstack11lllll_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪঢ়")]
  return {}
def bstack1lll11lll_opy_(caps):
  global bstack1lll1ll11l_opy_
  if bstack11lllll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ৞") in caps:
    caps[bstack11lllll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨয়")][bstack11lllll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧৠ")] = True
    if bstack1lll1ll11l_opy_:
      caps[bstack11lllll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪৡ")][bstack11lllll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬৢ")] = bstack1lll1ll11l_opy_
  else:
    caps[bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩৣ")] = True
    if bstack1lll1ll11l_opy_:
      caps[bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭৤")] = bstack1lll1ll11l_opy_
@measure(event_name=EVENTS.bstack1l1ll111l1_opy_, stage=STAGE.bstack1llll11111_opy_, bstack11lll11111_opy_=bstack11l1l1ll1l_opy_)
def bstack11l1ll1l1l_opy_():
  global CONFIG
  if not bstack1l111lll1l_opy_(CONFIG) or cli.is_enabled(CONFIG):
    return
  if bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ৥") in CONFIG and bstack1ll1ll111_opy_(CONFIG[bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ০")]):
    if (
      bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ১") in CONFIG
      and bstack1ll1ll111_opy_(CONFIG[bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭২")].get(bstack11lllll_opy_ (u"ࠪࡷࡰ࡯ࡰࡃ࡫ࡱࡥࡷࡿࡉ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡣࡷ࡭ࡴࡴࠧ৩")))
    ):
      logger.debug(bstack11lllll_opy_ (u"ࠦࡑࡵࡣࡢ࡮ࠣࡦ࡮ࡴࡡࡳࡻࠣࡲࡴࡺࠠࡴࡶࡤࡶࡹ࡫ࡤࠡࡣࡶࠤࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤࡪࡴࡡࡣ࡮ࡨࡨࠧ৪"))
      return
    bstack1llll11l11_opy_ = bstack111ll11ll_opy_(CONFIG)
    bstack111lll1lll_opy_(CONFIG[bstack11lllll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ৫")], bstack1llll11l11_opy_)
def bstack111lll1lll_opy_(key, bstack1llll11l11_opy_):
  global bstack11l11ll1_opy_
  logger.info(bstack1l1l111l1_opy_)
  try:
    bstack11l11ll1_opy_ = Local()
    bstack1l1lll1ll_opy_ = {bstack11lllll_opy_ (u"࠭࡫ࡦࡻࠪ৬"): key}
    bstack1l1lll1ll_opy_.update(bstack1llll11l11_opy_)
    logger.debug(bstack1l111lll1_opy_.format(str(bstack1l1lll1ll_opy_)).replace(key, bstack11lllll_opy_ (u"ࠧ࡜ࡔࡈࡈࡆࡉࡔࡆࡆࡠࠫ৭")))
    bstack11l11ll1_opy_.start(**bstack1l1lll1ll_opy_)
    if bstack11l11ll1_opy_.isRunning():
      logger.info(bstack1ll1llllll_opy_)
  except Exception as e:
    bstack11l1ll11l1_opy_(bstack11lllll11l_opy_.format(str(e)))
def bstack1l11ll11_opy_():
  global bstack11l11ll1_opy_
  if bstack11l11ll1_opy_.isRunning():
    logger.info(bstack11ll1111l_opy_)
    bstack11l11ll1_opy_.stop()
  bstack11l11ll1_opy_ = None
def bstack1llll11l1_opy_(bstack1l1ll1l1ll_opy_=[]):
  global CONFIG
  bstack1ll111l1_opy_ = []
  bstack1l1l1l111l_opy_ = [bstack11lllll_opy_ (u"ࠨࡱࡶࠫ৮"), bstack11lllll_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬ৯"), bstack11lllll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧৰ"), bstack11lllll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ৱ"), bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ৲"), bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ৳")]
  try:
    for err in bstack1l1ll1l1ll_opy_:
      bstack1ll1l1lll1_opy_ = {}
      for k in bstack1l1l1l111l_opy_:
        val = CONFIG[bstack11lllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ৴")][int(err[bstack11lllll_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ৵")])].get(k)
        if val:
          bstack1ll1l1lll1_opy_[k] = val
      if(err[bstack11lllll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ৶")] != bstack11lllll_opy_ (u"ࠪࠫ৷")):
        bstack1ll1l1lll1_opy_[bstack11lllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡵࠪ৸")] = {
          err[bstack11lllll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ৹")]: err[bstack11lllll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ৺")]
        }
        bstack1ll111l1_opy_.append(bstack1ll1l1lll1_opy_)
  except Exception as e:
    logger.debug(bstack11lllll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡳࡷࡳࡡࡵࡶ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺ࠺ࠡࠩ৻") + str(e))
  finally:
    return bstack1ll111l1_opy_
def bstack11l1111ll1_opy_(file_name):
  bstack1ll11l11_opy_ = []
  try:
    bstack1l111lll_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1l111lll_opy_):
      with open(bstack1l111lll_opy_) as f:
        bstack11111ll1_opy_ = json.load(f)
        bstack1ll11l11_opy_ = bstack11111ll1_opy_
      os.remove(bstack1l111lll_opy_)
    return bstack1ll11l11_opy_
  except Exception as e:
    logger.debug(bstack11lllll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪ࡮ࡴࡤࡪࡰࡪࠤࡪࡸࡲࡰࡴࠣࡰ࡮ࡹࡴ࠻ࠢࠪৼ") + str(e))
    return bstack1ll11l11_opy_
def bstack111ll1ll11_opy_():
  try:
      import time
      from bstack_utils.constants import bstack111l111ll_opy_, EVENTS
      from bstack_utils.helper import bstack111ll111_opy_, get_host_info, bstack1l111111_opy_
      from datetime import datetime
      from filelock import FileLock
      from bstack_utils.bstack11lll1l11l_opy_ import bstack1lll11l1ll_opy_
      bstack1lll11l1ll_opy_.bstack11llllllll_opy_()
      bstack1l1111lll_opy_ = os.path.join(os.getcwd(), bstack11lllll_opy_ (u"ࠩ࡯ࡳ࡬࠭৽"), bstack11lllll_opy_ (u"ࠪ࡯ࡪࡿ࠭࡮ࡧࡷࡶ࡮ࡩࡳ࠯࡬ࡶࡳࡳ࠭৾"))
      data = None
      lock = FileLock(bstack1l1111lll_opy_+bstack11lllll_opy_ (u"ࠦ࠳ࡲ࡯ࡤ࡭ࠥ৿"), timeout=2)
      try:
          with lock:
              with open(bstack1l1111lll_opy_, bstack11lllll_opy_ (u"ࠧࡸࠢ਀"), encoding=bstack11lllll_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧਁ")) as file:
                  data = json.load(file)
      except Exception as e:
          logger.debug(bstack11lllll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡶࡪࡧࡤࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࠦࡦࡪ࡮ࡨ࠾ࠥࢁࡽࠣਂ").format(e))
          return
      if not data:
          return
      def bstack11ll1llll1_opy_():
          try:
              config = {
                  bstack11lllll_opy_ (u"ࠣࡪࡨࡥࡩ࡫ࡲࡴࠤਃ"): {
                      bstack11lllll_opy_ (u"ࠤࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠣ਄"): bstack11lllll_opy_ (u"ࠥࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳࠨਅ"),
                  }
              }
              bstack1ll1l11l1_opy_ = datetime.utcnow()
              bstack1lll11lll1_opy_ = bstack1ll1l11l1_opy_.strftime(bstack11lllll_opy_ (u"ࠦࠪ࡟࠭ࠦ࡯࠰ࠩࡩ࡚ࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࠯ࠧࡩࠤ࡚࡚ࡃࠣਆ"))
              bstack1ll11llll1_opy_ = os.environ.get(bstack11lllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪਇ")) if os.environ.get(bstack11lllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫਈ")) else bstack1l111111_opy_.get_property(bstack11lllll_opy_ (u"ࠢࡴࡦ࡮ࡖࡺࡴࡉࡥࠤਉ"))
              payload = {
                  bstack11lllll_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠧਊ"): bstack11lllll_opy_ (u"ࠤࡶࡨࡰࡥࡥࡷࡧࡱࡸࡸࠨ਋"),
                  bstack11lllll_opy_ (u"ࠥࡨࡦࡺࡡࠣ਌"): {
                      bstack11lllll_opy_ (u"ࠦࡹ࡫ࡳࡵࡪࡸࡦࡤࡻࡵࡪࡦࠥ਍"): bstack1ll11llll1_opy_,
                      bstack11lllll_opy_ (u"ࠧࡩࡲࡦࡣࡷࡩࡩࡥࡤࡢࡻࠥ਎"): bstack1lll11lll1_opy_,
                      bstack11lllll_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡴࡡ࡮ࡧࠥਏ"): bstack11lllll_opy_ (u"ࠢࡔࡆࡎࡊࡪࡧࡴࡶࡴࡨࡔࡪࡸࡦࡰࡴࡰࡥࡳࡩࡥࠣਐ"),
                      bstack11lllll_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟࡫ࡵࡲࡲࠧ਑"): {
                          bstack11lllll_opy_ (u"ࠤࡰࡩࡦࡹࡵࡳࡧࡶࠦ਒"): data,
                          bstack11lllll_opy_ (u"ࠥࡷࡩࡱࡒࡶࡰࡌࡨࠧਓ"): bstack1l111111_opy_.get_property(bstack11lllll_opy_ (u"ࠦࡸࡪ࡫ࡓࡷࡱࡍࡩࠨਔ"))
                      },
                      bstack11lllll_opy_ (u"ࠧࡻࡳࡦࡴࡢࡨࡦࡺࡡࠣਕ"): bstack1l111111_opy_.get_property(bstack11lllll_opy_ (u"ࠨࡵࡴࡧࡵࡒࡦࡳࡥࠣਖ")),
                      bstack11lllll_opy_ (u"ࠢࡩࡱࡶࡸࡤ࡯࡮ࡧࡱࠥਗ"): get_host_info()
                  }
              }
              bstack1lll1ll111_opy_ = bstack1lll1l111_opy_(cli.config, [bstack11lllll_opy_ (u"ࠣࡣࡳ࡭ࡸࠨਘ"), bstack11lllll_opy_ (u"ࠤࡨࡨࡸࡏ࡮ࡴࡶࡵࡹࡲ࡫࡮ࡵࡣࡷ࡭ࡴࡴࠢਙ"), bstack11lllll_opy_ (u"ࠥࡥࡵ࡯ࠢਚ")], bstack111l111ll_opy_)
              response = bstack111ll111_opy_(bstack11lllll_opy_ (u"ࠦࡕࡕࡓࡕࠤਛ"), bstack1lll1ll111_opy_, payload, config)
              if response.status_code >= 200 and response.status_code < 300:
                  logger.info(bstack11lllll_opy_ (u"ࠧࡑࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵࠣࡷࡪࡴࡴࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡵࡱࠣࡿࢂࠨਜ").format(bstack111l111ll_opy_))
              else:
                  logger.debug(bstack11lllll_opy_ (u"ࠨࡋࡦࡻࠣࡱࡪࡺࡲࡪࡥࡶࠤࡷ࡫ࡱࡶࡧࡶࡸࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪࠣࡷࡹࡧࡴࡶࡵࠣࡿࢂࠨਝ").format(response.status_code))
          except Exception as e:
              logger.debug(bstack11lllll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡴࡤࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࡀࠠࡼࡿࠥਞ").format(e))
      bstack11ll1llll1_opy_()
  except Exception as e:
      logger.debug(bstack11lllll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡴࡤࡠ࡭ࡨࡽࡤࡳࡥࡵࡴ࡬ࡧࡸࡀࠠࡼࡿࠥਟ").format(e))
def bstack1l1llll1_opy_():
  bstack1lllll1ll1_opy_ = bstack11lllll_opy_ (u"ࠤࠥਠ")
  global bstack1l111ll11_opy_
  global bstack1l11ll11ll_opy_
  global bstack1l11l111l1_opy_
  global bstack1l1lllll1l_opy_
  global ROBOT_PYTHON_ERRORS
  global bstack11llllll11_opy_
  global CONFIG
  bstack1l1111ll1l_opy_ = os.environ.get(bstack11lllll_opy_ (u"ࠪࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡕࡔࡇࡇࠫਡ"))
  if bstack1l1111ll1l_opy_ not in [bstack11lllll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬਢ")]:
    bstack1lllll1ll1_opy_ = bstack1lll11l1ll_opy_.bstack1llll1l1ll_opy_(EVENTS.bstack1ll111lll1_opy_)
  percy.shutdown()
  if bstack1l111ll11_opy_:
    logger.warning(bstack1l11l1l111_opy_.format(str(bstack1l111ll11_opy_)))
  else:
    try:
      bstack1ll1ll1l1_opy_ = bstack1l1l1111l_opy_(bstack11lllll_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫਣ"), logger)
      if bstack1ll1ll1l1_opy_.get(bstack11lllll_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫਤ")) and bstack1ll1ll1l1_opy_.get(bstack11lllll_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬਥ")).get(bstack11lllll_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪਦ")):
        logger.warning(bstack1l11l1l111_opy_.format(str(bstack1ll1ll1l1_opy_[bstack11lllll_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧਧ")][bstack11lllll_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬਨ")])))
    except Exception as e:
      logger.error(e)
  if cli.is_running():
    bstack11l1ll1l_opy_.invoke(bstack1lll11l1l_opy_.bstack11l1l11l1_opy_)
  logger.info(bstack1lll1l1l1l_opy_)
  global bstack11l11ll1_opy_
  if bstack11l11ll1_opy_:
    bstack1l11ll11_opy_()
  try:
    with bstack1l111ll111_opy_:
      bstack111llll1_opy_ = bstack1l11ll11ll_opy_.copy()
    for driver in bstack111llll1_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack11lll111ll_opy_)
  ROBOT_PYTHON_ERRORS = []
  if bstack11llllll11_opy_ == bstack11lllll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ਩"):
    ROBOT_PYTHON_ERRORS = bstack11l1111ll1_opy_(bstack11lllll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ਪ"))
  if bstack11llllll11_opy_ == bstack11lllll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ਫ") and len(bstack1l1lllll1l_opy_) == 0:
    bstack1l1lllll1l_opy_ = bstack11l1111ll1_opy_(bstack11lllll_opy_ (u"ࠧࡱࡹࡢࡴࡾࡺࡥࡴࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬਬ"))
    if len(bstack1l1lllll1l_opy_) == 0:
      bstack1l1lllll1l_opy_ = bstack11l1111ll1_opy_(bstack11lllll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡲࡳࡴࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧਭ"))
  bstack1l1111111_opy_ = bstack11lllll_opy_ (u"ࠩࠪਮ")
  if len(bstack1l11l111l1_opy_) > 0:
    bstack1l1111111_opy_ = bstack1llll11l1_opy_(bstack1l11l111l1_opy_)
  elif len(bstack1l1lllll1l_opy_) > 0:
    bstack1l1111111_opy_ = bstack1llll11l1_opy_(bstack1l1lllll1l_opy_)
  elif len(ROBOT_PYTHON_ERRORS) > 0:
    bstack1l1111111_opy_ = bstack1llll11l1_opy_(ROBOT_PYTHON_ERRORS)
  elif len(bstack1l11llll1l_opy_) > 0:
    bstack1l1111111_opy_ = bstack1llll11l1_opy_(bstack1l11llll1l_opy_)
  if bstack1l1111ll1l_opy_ not in [bstack11lllll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫਯ")]:
    def bstack11l11llll1_opy_():
      try:
        if bstack1l1111ll1l_opy_ in [bstack11lllll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪਰ"), bstack11lllll_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ਱")]:
          bstack1llll11ll_opy_()
      except Exception as e:
        logger.debug(bstack11lllll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡨ࡬ࡲࡦࡲ࡟ࡦࡺࡨࡧࡺࡺࡩࡰࡰ࠽ࠤࢀࢃࠢਲ").format(e))
    def bstack11l1l11l11_opy_():
      try:
        if bool(bstack1l1111111_opy_):
          bstack1lllll1l1_opy_(bstack1l1111111_opy_)
        else:
          bstack1lllll1l1_opy_()
      except Exception as e:
        logger.debug(bstack11lllll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡳࡦࡰࡧ࡭ࡳ࡭ࠠࡦࡸࡨࡲࡹࡀࠠࡼࡿࠥਲ਼").format(e))
    def bstack1111llll_opy_():
      try:
        logger_utils.bstack1ll111l1ll_opy_(CONFIG)
      except Exception as e:
        logger.debug(bstack11lllll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡴࡧࡱࡨ࡮ࡴࡧࠡ࡮ࡲ࡫ࡸࡀࠠࡼࡿࠥ਴").format(e))
    bstack1lll1l1l11_opy_ = threading.Thread(target=bstack11l11llll1_opy_)
    bstack11l1l1111l_opy_ = threading.Thread(target=bstack11l1l11l11_opy_)
    bstack111lll111_opy_ = threading.Thread(target=bstack1111llll_opy_)
    threads = [bstack1lll1l1l11_opy_, bstack11l1l1111l_opy_, bstack111lll111_opy_]
    for thread in threads:
      try:
        thread.start()
      except Exception as e:
        logger.debug(bstack11lllll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡵࡷࡥࡷࡺࡩ࡯ࡩࠣࡸ࡭ࡸࡥࡢࡦࠣࡿࢂࡀࠠࡼࡿࠥਵ").format(thread.name, e))
    for thread in threads:
      try:
        thread.join()
      except Exception as e:
        logger.debug(bstack11lllll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡭ࡳ࡮ࡴࡩ࡯ࡩࠣࡸ࡭ࡸࡥࡢࡦࠣࡿࢂࡀࠠࡼࡿࠥਸ਼").format(thread.name, e))
    bstack1111lll11_opy_(bstack1ll1111111_opy_, logger)
    bstack1111lll11_opy_(os.path.join(os.getcwd(), bstack11lllll_opy_ (u"ࠫࡱࡵࡧࠨ਷"), bstack11lllll_opy_ (u"ࠬࡱࡥࡺ࠯ࡰࡩࡹࡸࡩࡤࡵ࠱࡮ࡸࡵ࡮ࠨਸ")), logger)
  if bstack1l1111ll1l_opy_ not in [bstack11lllll_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧਹ")]:
    bstack1lll11l1ll_opy_.end(EVENTS.bstack1ll111lll1_opy_.value, bstack1lllll1ll1_opy_ + bstack11lllll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ਺"), bstack1lllll1ll1_opy_ + bstack11lllll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ਻"), status=True, failure=None, test_name=None)
    bstack111ll1ll11_opy_()
    logger_utils.bstack1l1llllll_opy_()
    logging.shutdown()
  if len(ROBOT_PYTHON_ERRORS) > 0:
    sys.exit(len(ROBOT_PYTHON_ERRORS))
def bstack11lll1ll11_opy_(bstack11l11l11ll_opy_, frame):
  global bstack1l111111_opy_
  logger.error(bstack1111l1111_opy_)
  bstack1l111111_opy_.bstack1llll1ll1l_opy_(bstack11lllll_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡑࡳ਼ࠬ"), bstack11l11l11ll_opy_)
  if hasattr(signal, bstack11lllll_opy_ (u"ࠪࡗ࡮࡭࡮ࡢ࡮ࡶࠫ਽")):
    bstack1l111111_opy_.bstack1llll1ll1l_opy_(bstack11lllll_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡘ࡯ࡧ࡯ࡣ࡯ࠫਾ"), signal.Signals(bstack11l11l11ll_opy_).name)
  else:
    bstack1l111111_opy_.bstack1llll1ll1l_opy_(bstack11lllll_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬਿ"), bstack11lllll_opy_ (u"࠭ࡓࡊࡉࡘࡒࡐࡔࡏࡘࡐࠪੀ"))
  if cli.is_running():
    bstack11l1ll1l_opy_.invoke(bstack1lll11l1l_opy_.bstack11l1l11l1_opy_)
  bstack1l1111ll1l_opy_ = os.environ.get(bstack11lllll_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨੁ"))
  if bstack1l1111ll1l_opy_ == bstack11lllll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨੂ") and not cli.is_enabled(CONFIG):
    bstack11lll1111l_opy_.stop(bstack1l111111_opy_.get_property(bstack11lllll_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩ੃")))
  bstack1l1llll1_opy_()
  sys.exit(1)
def bstack11l1ll11l1_opy_(err):
  logger.critical(bstack11ll11ll11_opy_.format(str(err)))
  bstack1lllll1l1_opy_(bstack11ll11ll11_opy_.format(str(err)), True)
  atexit.unregister(bstack1l1llll1_opy_)
  bstack1llll11ll_opy_()
  sys.exit(1)
def bstack11l111ll11_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1lllll1l1_opy_(message, True)
  atexit.unregister(bstack1l1llll1_opy_)
  bstack1llll11ll_opy_()
  sys.exit(1)
def bstack1l1llll1ll_opy_():
  global CONFIG
  global bstack1l111l11l_opy_
  global bstack111lllll11_opy_
  global bstack11ll1l1l11_opy_
  CONFIG = bstack1l11l11l1l_opy_()
  load_dotenv(CONFIG.get(bstack11lllll_opy_ (u"ࠪࡩࡳࡼࡆࡪ࡮ࡨࠫ੄")))
  bstack1l1l1ll1_opy_()
  bstack1llll1ll_opy_()
  CONFIG = bstack1ll11ll1l1_opy_(CONFIG)
  update(CONFIG, bstack111lllll11_opy_)
  update(CONFIG, bstack1l111l11l_opy_)
  if not cli.is_enabled(CONFIG):
    CONFIG = bstack11lll11ll1_opy_(CONFIG)
  bstack11ll1l1l11_opy_ = bstack1l111lll1l_opy_(CONFIG)
  os.environ[bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ੅")] = bstack11ll1l1l11_opy_.__str__().lower()
  bstack1l111111_opy_.bstack1llll1ll1l_opy_(bstack11lllll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭੆"), bstack11ll1l1l11_opy_)
  if (bstack11lllll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩੇ") in CONFIG and bstack11lllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪੈ") in bstack1l111l11l_opy_) or (
          bstack11lllll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ੉") in CONFIG and bstack11lllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ੊") not in bstack111lllll11_opy_):
    if os.getenv(bstack11lllll_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧੋ")):
      CONFIG[bstack11lllll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ੌ")] = os.getenv(bstack11lllll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅ੍ࠩ"))
    else:
      if not CONFIG.get(bstack11lllll_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠤ੎"), bstack11lllll_opy_ (u"ࠢࠣ੏")) in bstack1ll1l11l11_opy_:
        bstack11l111l11_opy_()
  elif (bstack11lllll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ੐") not in CONFIG and bstack11lllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫੑ") in CONFIG) or (
          bstack11lllll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭੒") in bstack111lllll11_opy_ and bstack11lllll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ੓") not in bstack1l111l11l_opy_):
    del (CONFIG[bstack11lllll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ੔")])
  if bstack1l1lll1ll1_opy_(CONFIG):
    bstack11l1ll11l1_opy_(bstack1111l1l11_opy_)
  Config.bstack1llll1l111_opy_().bstack1llll1ll1l_opy_(bstack11lllll_opy_ (u"ࠨࡵࡴࡧࡵࡒࡦࡳࡥࠣ੕"), CONFIG[bstack11lllll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ੖")])
  bstack1lll111ll1_opy_()
  bstack111lll11l_opy_()
  if bstack1l1lll1l1_opy_ and not CONFIG.get(bstack11lllll_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠦ੗"), bstack11lllll_opy_ (u"ࠤࠥ੘")) in bstack1ll1l11l11_opy_:
    CONFIG[bstack11lllll_opy_ (u"ࠪࡥࡵࡶࠧਖ਼")] = bstack11111111l_opy_(CONFIG)
    logger.info(bstack1l1lllll1_opy_.format(CONFIG[bstack11lllll_opy_ (u"ࠫࡦࡶࡰࠨਗ਼")]))
  if not bstack11ll1l1l11_opy_:
    CONFIG[bstack11lllll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨਜ਼")] = [{}]
def bstack111l1llll1_opy_(config, bstack1l1ll11l_opy_):
  global CONFIG
  global bstack1l1lll1l1_opy_
  CONFIG = config
  bstack1l1lll1l1_opy_ = bstack1l1ll11l_opy_
def bstack111lll11l_opy_():
  global CONFIG
  global bstack1l1lll1l1_opy_
  if bstack11lllll_opy_ (u"࠭ࡡࡱࡲࠪੜ") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack11l111ll11_opy_(e, bstack1l1l1ll1l1_opy_)
    bstack1l1lll1l1_opy_ = True
    bstack1l111111_opy_.bstack1llll1ll1l_opy_(bstack11lllll_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭੝"), True)
def bstack11111111l_opy_(config):
  bstack11lll1lll1_opy_ = bstack11lllll_opy_ (u"ࠨࠩਫ਼")
  app = config[bstack11lllll_opy_ (u"ࠩࡤࡴࡵ࠭੟")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1l1lll1l_opy_:
      if os.path.exists(app):
        bstack11lll1lll1_opy_ = bstack1l1llll11l_opy_(config, app)
      elif bstack1llll111_opy_(app):
        bstack11lll1lll1_opy_ = app
      else:
        bstack11l1ll11l1_opy_(bstack1l1ll1111l_opy_.format(app))
    else:
      if bstack1llll111_opy_(app):
        bstack11lll1lll1_opy_ = app
      elif os.path.exists(app):
        bstack11lll1lll1_opy_ = bstack1l1llll11l_opy_(app)
      else:
        bstack11l1ll11l1_opy_(bstack1ll1lll1l1_opy_)
  else:
    if len(app) > 2:
      bstack11l1ll11l1_opy_(bstack11llll111_opy_)
    elif len(app) == 2:
      if bstack11lllll_opy_ (u"ࠪࡴࡦࡺࡨࠨ੠") in app and bstack11lllll_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧ੡") in app:
        if os.path.exists(app[bstack11lllll_opy_ (u"ࠬࡶࡡࡵࡪࠪ੢")]):
          bstack11lll1lll1_opy_ = bstack1l1llll11l_opy_(config, app[bstack11lllll_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ੣")], app[bstack11lllll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪ੤")])
        else:
          bstack11l1ll11l1_opy_(bstack1l1ll1111l_opy_.format(app))
      else:
        bstack11l1ll11l1_opy_(bstack11llll111_opy_)
    else:
      for key in app:
        if key in bstack11llll1l11_opy_:
          if key == bstack11lllll_opy_ (u"ࠨࡲࡤࡸ࡭࠭੥"):
            if os.path.exists(app[key]):
              bstack11lll1lll1_opy_ = bstack1l1llll11l_opy_(config, app[key])
            else:
              bstack11l1ll11l1_opy_(bstack1l1ll1111l_opy_.format(app))
          else:
            bstack11lll1lll1_opy_ = app[key]
        else:
          bstack11l1ll11l1_opy_(bstack1ll1ll111l_opy_)
  return bstack11lll1lll1_opy_
def bstack1llll111_opy_(bstack11lll1lll1_opy_):
  import re
  bstack1ll11l1l1l_opy_ = re.compile(bstack11lllll_opy_ (u"ࡴࠥࡢࡠࡧ࠭ࡻࡃ࠰࡞࠵࠳࠹࡝ࡡ࠱ࡠ࠲ࡣࠪࠥࠤ੦"))
  bstack111l1l1ll_opy_ = re.compile(bstack11lllll_opy_ (u"ࡵࠦࡣࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫ࠱࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯ࠪࠢ੧"))
  if bstack11lllll_opy_ (u"ࠫࡧࡹ࠺࠰࠱ࠪ੨") in bstack11lll1lll1_opy_ or re.fullmatch(bstack1ll11l1l1l_opy_, bstack11lll1lll1_opy_) or re.fullmatch(bstack111l1l1ll_opy_, bstack11lll1lll1_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack11llll111l_opy_, stage=STAGE.bstack1llll11111_opy_, bstack11lll11111_opy_=bstack11l1l1ll1l_opy_)
def bstack1l1llll11l_opy_(config, path, bstack1l11llll1_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack11lllll_opy_ (u"ࠬࡸࡢࠨ੩")).read()).hexdigest()
  bstack11l1111lll_opy_ = bstack1l11ll1ll1_opy_(md5_hash)
  bstack11lll1lll1_opy_ = None
  if bstack11l1111lll_opy_:
    logger.info(bstack111l1l1l1_opy_.format(bstack11l1111lll_opy_, md5_hash))
    return bstack11l1111lll_opy_
  bstack1l1111l111_opy_ = datetime.datetime.now()
  bstack1lll1111ll_opy_ = MultipartEncoder(
    fields={
      bstack11lllll_opy_ (u"࠭ࡦࡪ࡮ࡨࠫ੪"): (os.path.basename(path), open(os.path.abspath(path), bstack11lllll_opy_ (u"ࠧࡳࡤࠪ੫")), bstack11lllll_opy_ (u"ࠨࡶࡨࡼࡹ࠵ࡰ࡭ࡣ࡬ࡲࠬ੬")),
      bstack11lllll_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ੭"): bstack1l11llll1_opy_
    }
  )
  response = requests.post(bstack1ll1l11111_opy_, data=bstack1lll1111ll_opy_,
                           headers={bstack11lllll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩ੮"): bstack1lll1111ll_opy_.content_type},
                           auth=(config[bstack11lllll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭੯")], config[bstack11lllll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨੰ")]))
  try:
    res = json.loads(response.text)
    bstack11lll1lll1_opy_ = res[bstack11lllll_opy_ (u"࠭ࡡࡱࡲࡢࡹࡷࡲࠧੱ")]
    logger.info(bstack1lll1l1lll_opy_.format(bstack11lll1lll1_opy_))
    bstack11lllll1l_opy_(md5_hash, bstack11lll1lll1_opy_)
    cli.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠢࡩࡶࡷࡴ࠿ࡻࡰ࡭ࡱࡤࡨࡤࡧࡰࡱࠤੲ"), datetime.datetime.now() - bstack1l1111l111_opy_)
  except ValueError as err:
    bstack11l1ll11l1_opy_(bstack1llllll1l1_opy_.format(str(err)))
  return bstack11lll1lll1_opy_
def bstack1lll111ll1_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack11l1l1lll_opy_
  bstack1l1ll11l11_opy_ = 1
  bstack1lll11ll1l_opy_ = 1
  if bstack11lllll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨੳ") in CONFIG:
    bstack1lll11ll1l_opy_ = CONFIG[bstack11lllll_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩੴ")]
  else:
    bstack1lll11ll1l_opy_ = bstack1ll1l111l_opy_(framework_name, args) or 1
  if bstack11lllll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ੵ") in CONFIG:
    bstack1l1ll11l11_opy_ = len(CONFIG[bstack11lllll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ੶")])
  bstack11l1l1lll_opy_ = int(bstack1lll11ll1l_opy_) * int(bstack1l1ll11l11_opy_)
def bstack1ll1l111l_opy_(framework_name, args):
  if framework_name == bstack1l1lllll_opy_ and args and bstack11lllll_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ੷") in args:
      bstack11l111l1l1_opy_ = args.index(bstack11lllll_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ੸"))
      return int(args[bstack11l111l1l1_opy_ + 1]) or 1
  return 1
def bstack1l11ll1ll1_opy_(md5_hash):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack11lllll_opy_ (u"ࠧࡧ࡫࡯ࡩࡱࡵࡣ࡬ࠢࡱࡳࡹࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦ࠮ࠣࡹࡸ࡯࡮ࡨࠢࡥࡥࡸ࡯ࡣࠡࡨ࡬ࡰࡪࠦ࡯ࡱࡧࡵࡥࡹ࡯࡯࡯ࡵࠪ੹"))
    bstack11l11111l_opy_ = os.path.join(os.path.expanduser(bstack11lllll_opy_ (u"ࠨࢀࠪ੺")), bstack11lllll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ੻"), bstack11lllll_opy_ (u"ࠪࡥࡵࡶࡕࡱ࡮ࡲࡥࡩࡓࡄ࠶ࡊࡤࡷ࡭࠴ࡪࡴࡱࡱࠫ੼"))
    if os.path.exists(bstack11l11111l_opy_):
      try:
        bstack1ll1l1l1ll_opy_ = json.load(open(bstack11l11111l_opy_, bstack11lllll_opy_ (u"ࠫࡷࡨࠧ੽")))
        if md5_hash in bstack1ll1l1l1ll_opy_:
          bstack11l1l1l1_opy_ = bstack1ll1l1l1ll_opy_[md5_hash]
          bstack1l11lll11l_opy_ = datetime.datetime.now()
          bstack1llll11l_opy_ = datetime.datetime.strptime(bstack11l1l1l1_opy_[bstack11lllll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ੾")], bstack11lllll_opy_ (u"࠭ࠥࡥ࠱ࠨࡱ࠴࡙ࠫࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪ੿"))
          if (bstack1l11lll11l_opy_ - bstack1llll11l_opy_).days > 30:
            return None
          elif version.parse(str(__version__)) > version.parse(bstack11l1l1l1_opy_[bstack11lllll_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ઀")]):
            return None
          return bstack11l1l1l1_opy_[bstack11lllll_opy_ (u"ࠨ࡫ࡧࠫઁ")]
      except Exception as e:
        logger.debug(bstack11lllll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡴࡨࡥࡩ࡯࡮ࡨࠢࡐࡈ࠺ࠦࡨࡢࡵ࡫ࠤ࡫࡯࡬ࡦ࠼ࠣࡿࢂ࠭ં").format(str(e)))
    return None
  bstack11l11111l_opy_ = os.path.join(os.path.expanduser(bstack11lllll_opy_ (u"ࠪࢂࠬઃ")), bstack11lllll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ઄"), bstack11lllll_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭અ"))
  lock_file = bstack11l11111l_opy_ + bstack11lllll_opy_ (u"࠭࠮࡭ࡱࡦ࡯ࠬઆ")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack11l11111l_opy_):
        with open(bstack11l11111l_opy_, bstack11lllll_opy_ (u"ࠧࡳࠩઇ")) as f:
          content = f.read().strip()
          if content:
            bstack1ll1l1l1ll_opy_ = json.loads(content)
            if md5_hash in bstack1ll1l1l1ll_opy_:
              bstack11l1l1l1_opy_ = bstack1ll1l1l1ll_opy_[md5_hash]
              bstack1l11lll11l_opy_ = datetime.datetime.now()
              bstack1llll11l_opy_ = datetime.datetime.strptime(bstack11l1l1l1_opy_[bstack11lllll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫઈ")], bstack11lllll_opy_ (u"ࠩࠨࡨ࠴ࠫ࡭࠰ࠧ࡜ࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭ઉ"))
              if (bstack1l11lll11l_opy_ - bstack1llll11l_opy_).days > 30:
                return None
              elif version.parse(str(__version__)) > version.parse(bstack11l1l1l1_opy_[bstack11lllll_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨઊ")]):
                return None
              return bstack11l1l1l1_opy_[bstack11lllll_opy_ (u"ࠫ࡮ࡪࠧઋ")]
      return None
  except Exception as e:
    logger.debug(bstack11lllll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡼ࡯ࡴࡩࠢࡩ࡭ࡱ࡫ࠠ࡭ࡱࡦ࡯࡮ࡴࡧࠡࡨࡲࡶࠥࡓࡄ࠶ࠢ࡫ࡥࡸ࡮࠺ࠡࡽࢀࠫઌ").format(str(e)))
    return None
def bstack11lllll1l_opy_(md5_hash, bstack11lll1lll1_opy_):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack11lllll_opy_ (u"࠭ࡦࡪ࡮ࡨࡰࡴࡩ࡫ࠡࡰࡲࡸࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥ࠭ࠢࡸࡷ࡮ࡴࡧࠡࡤࡤࡷ࡮ࡩࠠࡧ࡫࡯ࡩࠥࡵࡰࡦࡴࡤࡸ࡮ࡵ࡮ࡴࠩઍ"))
    bstack1111l11ll_opy_ = os.path.join(os.path.expanduser(bstack11lllll_opy_ (u"ࠧࡿࠩ઎")), bstack11lllll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨએ"))
    if not os.path.exists(bstack1111l11ll_opy_):
      os.makedirs(bstack1111l11ll_opy_)
    bstack11l11111l_opy_ = os.path.join(os.path.expanduser(bstack11lllll_opy_ (u"ࠩࢁࠫઐ")), bstack11lllll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪઑ"), bstack11lllll_opy_ (u"ࠫࡦࡶࡰࡖࡲ࡯ࡳࡦࡪࡍࡅ࠷ࡋࡥࡸ࡮࠮࡫ࡵࡲࡲࠬ઒"))
    bstack1l1l1ll11_opy_ = {
      bstack11lllll_opy_ (u"ࠬ࡯ࡤࠨઓ"): bstack11lll1lll1_opy_,
      bstack11lllll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩઔ"): datetime.datetime.strftime(datetime.datetime.now(), bstack11lllll_opy_ (u"ࠧࠦࡦ࠲ࠩࡲ࠵࡚ࠥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫક")),
      bstack11lllll_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ખ"): str(__version__)
    }
    try:
      bstack1ll1l1l1ll_opy_ = {}
      if os.path.exists(bstack11l11111l_opy_):
        bstack1ll1l1l1ll_opy_ = json.load(open(bstack11l11111l_opy_, bstack11lllll_opy_ (u"ࠩࡵࡦࠬગ")))
      bstack1ll1l1l1ll_opy_[md5_hash] = bstack1l1l1ll11_opy_
      with open(bstack11l11111l_opy_, bstack11lllll_opy_ (u"ࠥࡻ࠰ࠨઘ")) as outfile:
        json.dump(bstack1ll1l1l1ll_opy_, outfile)
    except Exception as e:
      logger.debug(bstack11lllll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡹࡵࡪࡡࡵ࡫ࡱ࡫ࠥࡓࡄ࠶ࠢ࡫ࡥࡸ࡮ࠠࡧ࡫࡯ࡩ࠿ࠦࡻࡾࠩઙ").format(str(e)))
    return
  bstack1111l11ll_opy_ = os.path.join(os.path.expanduser(bstack11lllll_opy_ (u"ࠬࢄࠧચ")), bstack11lllll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭છ"))
  if not os.path.exists(bstack1111l11ll_opy_):
    os.makedirs(bstack1111l11ll_opy_)
  bstack11l11111l_opy_ = os.path.join(os.path.expanduser(bstack11lllll_opy_ (u"ࠧࡿࠩજ")), bstack11lllll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨઝ"), bstack11lllll_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪઞ"))
  lock_file = bstack11l11111l_opy_ + bstack11lllll_opy_ (u"ࠪ࠲ࡱࡵࡣ࡬ࠩટ")
  bstack1l1l1ll11_opy_ = {
    bstack11lllll_opy_ (u"ࠫ࡮ࡪࠧઠ"): bstack11lll1lll1_opy_,
    bstack11lllll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨડ"): datetime.datetime.strftime(datetime.datetime.now(), bstack11lllll_opy_ (u"࠭ࠥࡥ࠱ࠨࡱ࠴࡙ࠫࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪઢ")),
    bstack11lllll_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬણ"): str(__version__)
  }
  try:
    with FileLock(lock_file, timeout=10):
      bstack1ll1l1l1ll_opy_ = {}
      if os.path.exists(bstack11l11111l_opy_):
        with open(bstack11l11111l_opy_, bstack11lllll_opy_ (u"ࠨࡴࠪત")) as f:
          content = f.read().strip()
          if content:
            bstack1ll1l1l1ll_opy_ = json.loads(content)
      bstack1ll1l1l1ll_opy_[md5_hash] = bstack1l1l1ll11_opy_
      with open(bstack11l11111l_opy_, bstack11lllll_opy_ (u"ࠤࡺࠦથ")) as outfile:
        json.dump(bstack1ll1l1l1ll_opy_, outfile)
  except Exception as e:
    logger.debug(bstack11lllll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡺ࡭ࡹ࡮ࠠࡧ࡫࡯ࡩࠥࡲ࡯ࡤ࡭࡬ࡲ࡬ࠦࡦࡰࡴࠣࡑࡉ࠻ࠠࡩࡣࡶ࡬ࠥࡻࡰࡥࡣࡷࡩ࠿ࠦࡻࡾࠩદ").format(str(e)))
def bstack11l1111l1l_opy_(self):
  return
def bstack111ll11l1l_opy_(self):
  return
def bstack11ll1llll_opy_():
  global bstack1ll1ll1ll_opy_
  bstack1ll1ll1ll_opy_ = True
def bstack1l11lll1l_opy_(self):
  global bstack111ll1111_opy_
  global bstack1ll11lll1l_opy_
  global bstack1ll111l11_opy_
  bstack1ll11111l_opy_ = bstack1lll11l1ll_opy_.bstack1llll1l1ll_opy_(EVENTS.bstack11l1l1l11l_opy_)
  try:
    if bstack11lllll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫધ") in bstack111ll1111_opy_ and self.session_id != None and bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠬࡺࡥࡴࡶࡖࡸࡦࡺࡵࡴࠩન"), bstack11lllll_opy_ (u"࠭ࠧ઩")) != bstack11lllll_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨપ"):
      bstack1ll1111lll_opy_ = bstack11lllll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨફ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11lllll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩબ")
      if bstack1ll1111lll_opy_ == bstack11lllll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪભ"):
        bstack11l1lll1l_opy_(logger)
      if self != None:
        bstack11l1l111l_opy_(self, bstack1ll1111lll_opy_, bstack11lllll_opy_ (u"ࠫ࠱ࠦࠧમ").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack11lllll_opy_ (u"ࠬ࠭ય")
    if bstack11lllll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ર") in bstack111ll1111_opy_ and getattr(threading.current_thread(), bstack11lllll_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭઱"), None):
      bstack1l1ll111_opy_.bstack11l1l1lll1_opy_(self, bstack1111l11l1_opy_, logger, wait=True)
    if bstack11lllll_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨલ") in bstack111ll1111_opy_:
      bstack11l11l1l1_opy_.bstack1l1l11l1l_opy_(self)
    bstack1lll11l1ll_opy_.end(EVENTS.bstack11l1l1l11l_opy_.value, bstack1ll11111l_opy_ + bstack11lllll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤળ"), bstack1ll11111l_opy_ + bstack11lllll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ઴"), status=True, failure=None, test_name=None)
  except Exception as e:
    logger.debug(bstack11lllll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࠧવ") + str(e))
    bstack1lll11l1ll_opy_.end(EVENTS.bstack11l1l1l11l_opy_.value, bstack1ll11111l_opy_ + bstack11lllll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧશ"), bstack1ll11111l_opy_ + bstack11lllll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦષ"), status=False, failure=str(e), test_name=None)
  bstack1ll111l11_opy_(self)
  self.session_id = None
def bstack11ll1lll11_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack1l1ll1ll11_opy_
    global bstack111ll1111_opy_
    command_executor = kwargs.get(bstack11lllll_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠪસ"), bstack11lllll_opy_ (u"ࠨࠩહ"))
    bstack11ll1ll1l1_opy_ = False
    if type(command_executor) == str and bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬ઺") in command_executor:
      bstack11ll1ll1l1_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭઻") in str(getattr(command_executor, bstack11lllll_opy_ (u"ࠫࡤࡻࡲ࡭઼ࠩ"), bstack11lllll_opy_ (u"ࠬ࠭ઽ"))):
      bstack11ll1ll1l1_opy_ = True
    else:
      kwargs = bstack11l1llll11_opy_.bstack11111l1l_opy_(bstack111ll1ll1_opy_=kwargs, config=CONFIG)
      return bstack1l1lll11l1_opy_(self, *args, **kwargs)
    if bstack11ll1ll1l1_opy_:
      bstack1l1l111ll1_opy_ = bstack1llll1111_opy_.bstack1111l111_opy_(CONFIG, bstack111ll1111_opy_)
      if kwargs.get(bstack11lllll_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧા")):
        kwargs[bstack11lllll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨિ")] = bstack1l1ll1ll11_opy_(kwargs[bstack11lllll_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩી")], bstack111ll1111_opy_, CONFIG, bstack1l1l111ll1_opy_)
      elif kwargs.get(bstack11lllll_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩુ")):
        kwargs[bstack11lllll_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪૂ")] = bstack1l1ll1ll11_opy_(kwargs[bstack11lllll_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫૃ")], bstack111ll1111_opy_, CONFIG, bstack1l1l111ll1_opy_)
  except Exception as e:
    logger.error(bstack11lllll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡥ࡯ࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡓࡅࡍࠣࡧࡦࡶࡳ࠻ࠢࡾࢁࠧૄ").format(str(e)))
  return bstack1l1lll11l1_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack111lll1111_opy_, stage=STAGE.bstack1llll11111_opy_, bstack11lll11111_opy_=bstack11l1l1ll1l_opy_)
def bstack11llllll_opy_(self, command_executor=bstack11lllll_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵࠱࠳࠹࠱࠴࠳࠶࠮࠲࠼࠷࠸࠹࠺ࠢૅ"), *args, **kwargs):
  global bstack1ll11lll1l_opy_
  global bstack1l11ll11ll_opy_
  bstack11lll1l1_opy_ = bstack11ll1lll11_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack1l1l11llll_opy_.on():
    return bstack11lll1l1_opy_
  try:
    logger.debug(bstack11lllll_opy_ (u"ࠧࡄࡱࡰࡱࡦࡴࡤࠡࡇࡻࡩࡨࡻࡴࡰࡴࠣࡻ࡭࡫࡮ࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤ࡮ࡹࠠࡧࡣ࡯ࡷࡪࠦ࠭ࠡࡽࢀࠫ૆").format(str(command_executor)))
    logger.debug(bstack11lllll_opy_ (u"ࠨࡊࡸࡦ࡛ࠥࡒࡍࠢ࡬ࡷࠥ࠳ࠠࡼࡿࠪે").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬૈ") in command_executor._url:
      bstack1l111111_opy_.bstack1llll1ll1l_opy_(bstack11lllll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫૉ"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧ૊") in command_executor):
    bstack1l111111_opy_.bstack1llll1ll1l_opy_(bstack11lllll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ો"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1l11l1l1_opy_ = getattr(threading.current_thread(), bstack11lllll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡚ࡥࡴࡶࡐࡩࡹࡧࠧૌ"), None)
  bstack1ll11ll1ll_opy_ = {}
  if self.capabilities is not None:
    bstack1ll11ll1ll_opy_[bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡰࡤࡱࡪ્࠭")] = self.capabilities.get(bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭૎"))
    bstack1ll11ll1ll_opy_[bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫ૏")] = self.capabilities.get(bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫૐ"))
    bstack1ll11ll1ll_opy_[bstack11lllll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡣࡴࡶࡴࡪࡱࡱࡷࠬ૑")] = self.capabilities.get(bstack11lllll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ૒"))
  if CONFIG.get(bstack11lllll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭૓"), False) and bstack11l1llll11_opy_.bstack1l111l11ll_opy_(bstack1ll11ll1ll_opy_):
    threading.current_thread().a11yPlatform = True
  if bstack11lllll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ૔") in bstack111ll1111_opy_ or bstack11lllll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ૕") in bstack111ll1111_opy_:
    bstack11lll1111l_opy_.bstack1lll111lll_opy_(self)
  if bstack11lllll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ૖") in bstack111ll1111_opy_ and bstack1l11l1l1_opy_ and bstack1l11l1l1_opy_.get(bstack11lllll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ૗"), bstack11lllll_opy_ (u"ࠫࠬ૘")) == bstack11lllll_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭૙"):
    bstack11lll1111l_opy_.bstack1lll111lll_opy_(self)
  bstack1ll11lll1l_opy_ = self.session_id
  with bstack1l111ll111_opy_:
    bstack1l11ll11ll_opy_.append(self)
  return bstack11lll1l1_opy_
def bstack11111l1ll_opy_(args):
  return bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠧ૚") in str(args)
def bstack11ll1lll_opy_(self, driver_command, *args, **kwargs):
  global bstack1111l1lll_opy_
  global bstack1l1lllllll_opy_
  bstack11l1lll111_opy_ = bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ૛"), None) and bstack1l1ll1ll1_opy_(
          threading.current_thread(), bstack11lllll_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ૜"), None)
  bstack1l11ll1l1l_opy_ = bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ૝"), None) and bstack1l1ll1ll1_opy_(
          threading.current_thread(), bstack11lllll_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ૞"), None)
  bstack1l1l1l1l1_opy_ = getattr(self, bstack11lllll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫ૟"), None) != None and getattr(self, bstack11lllll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬૠ"), None) == True
  if not bstack1l1lllllll_opy_ and bstack11lllll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ૡ") in CONFIG and CONFIG[bstack11lllll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧૢ")] == True and bstack1ll1111l1l_opy_.bstack1ll111ll_opy_(driver_command) and (bstack1l1l1l1l1_opy_ or bstack11l1lll111_opy_ or bstack1l11ll1l1l_opy_) and not bstack11111l1ll_opy_(args):
    try:
      bstack1l1lllllll_opy_ = True
      logger.debug(bstack11lllll_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡪࡴࡸࠠࡼࡿࠪૣ").format(driver_command))
      bstack1l111ll11l_opy_ = perform_scan(self, driver_command=driver_command)
      logger.debug(bstack1l111ll11l_opy_)
      try:
        bstack1llll11ll1_opy_ = {
          bstack11lllll_opy_ (u"ࠤࡵࡩࡶࡻࡥࡴࡶࠥ૤"): {
            bstack11lllll_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࠦ૥"): bstack11lllll_opy_ (u"ࠦࡆ࠷࠱࡚ࡡࡖࡇࡆࡔࠢ૦"),
            bstack11lllll_opy_ (u"ࠧࡶࡡࡳࡣࡰࡩࡹ࡫ࡲࡴࠤ૧"): [
              {
                bstack11lllll_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࠨ૨"): driver_command
              }
            ]
          },
          bstack11lllll_opy_ (u"ࠢࡳࡧࡶࡴࡴࡴࡳࡦࠤ૩"): {
            bstack11lllll_opy_ (u"ࠣࡤࡲࡨࡾࠨ૪"): {
              bstack11lllll_opy_ (u"ࠤࡰࡷ࡬ࠨ૫"): bstack1l111ll11l_opy_.get(bstack11lllll_opy_ (u"ࠥࡱࡸ࡭ࠢ૬"), bstack11lllll_opy_ (u"ࠦࠧ૭")) if isinstance(bstack1l111ll11l_opy_, dict) else bstack11lllll_opy_ (u"ࠧࠨ૮"),
              bstack11lllll_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢ૯"): bstack1l111ll11l_opy_.get(bstack11lllll_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳࠣ૰"), True) if isinstance(bstack1l111ll11l_opy_, dict) else True
            }
          }
        }
        logger.debug(bstack11lllll_opy_ (u"ࠨࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳࠦࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡰࡴ࡭ࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠩ૱").format(bstack1llll11ll1_opy_))
        bstack1l111l111l_opy_.info(json.dumps(bstack1llll11ll1_opy_, separators=(bstack11lllll_opy_ (u"ࠩ࠯ࠫ૲"), bstack11lllll_opy_ (u"ࠪ࠾ࠬ૳"))))
      except Exception as bstack111l1l1l_opy_:
        logger.debug(bstack11lllll_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡭ࡱࡪࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸࡩࡡ࡯ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠫ૴").format(str(bstack111l1l1l_opy_)))
    except Exception as err:
      logger.debug(bstack11lllll_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡨࡶ࡫ࡵࡲ࡮ࠢࡶࡧࡦࡴࠠࡼࡿࠪ૵").format(str(err)))
    bstack1l1lllllll_opy_ = False
  response = bstack1111l1lll_opy_(self, driver_command, *args, **kwargs)
  if (bstack11lllll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ૶") in str(bstack111ll1111_opy_).lower() or bstack11lllll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ૷") in str(bstack111ll1111_opy_).lower()) and bstack1l1l11llll_opy_.on():
    try:
      if driver_command == bstack11lllll_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬ૸"):
        bstack11lll1111l_opy_.bstack1l11l111ll_opy_({
            bstack11lllll_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨૹ"): response[bstack11lllll_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩૺ")],
            bstack11lllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫૻ"): bstack11lll1111l_opy_.current_test_uuid() if bstack11lll1111l_opy_.current_test_uuid() else bstack1l1l11llll_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
def bstack1l1111l11l_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack1ll11lll1l_opy_
  global bstack1l11111ll_opy_
  global bstack11l1l1ll1l_opy_
  global bstack1lll1l1ll_opy_
  global bstack1llllllll_opy_
  global bstack111ll1111_opy_
  global bstack1l1lll11l1_opy_
  global bstack1l11ll11ll_opy_
  global bstack1l1llll1l_opy_
  global bstack1111l11l1_opy_
  bstack1ll11111l_opy_ = bstack1lll11l1ll_opy_.bstack1llll1l1ll_opy_(EVENTS.bstack1ll11ll1_opy_.value)
  if os.getenv(bstack11lllll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪૼ")) is not None and bstack11l1llll11_opy_.bstack1lll1l11ll_opy_(CONFIG) is None:
    CONFIG[bstack11lllll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭૽")] = True
  CONFIG[bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ૾")] = str(bstack111ll1111_opy_) + str(__version__)
  bstack111llllll1_opy_ = os.environ[bstack11lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭૿")]
  bstack1l1l111ll1_opy_ = bstack1llll1111_opy_.bstack1111l111_opy_(CONFIG, bstack111ll1111_opy_)
  CONFIG[bstack11lllll_opy_ (u"ࠩࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬ଀")] = bstack111llllll1_opy_
  CONFIG[bstack11lllll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬଁ")] = bstack1l1l111ll1_opy_
  if CONFIG.get(bstack11lllll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫଂ"),bstack11lllll_opy_ (u"ࠬ࠭ଃ")) and bstack11lllll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ଄") in bstack111ll1111_opy_:
    CONFIG[bstack11lllll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧଅ")].pop(bstack11lllll_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ଆ"), None)
    CONFIG[bstack11lllll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩଇ")].pop(bstack11lllll_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨଈ"), None)
  command_executor = bstack1l1llll111_opy_()
  logger.debug(bstack11l1l1llll_opy_.format(command_executor))
  proxy = bstack1lll1ll11_opy_(CONFIG, proxy)
  bstack11111l111_opy_ = 0 if bstack1l11111ll_opy_ < 0 else bstack1l11111ll_opy_
  try:
    if bstack1lll1l1ll_opy_ is True:
      bstack11111l111_opy_ = int(multiprocessing.current_process().name)
    elif bstack1llllllll_opy_ is True:
      bstack11111l111_opy_ = int(threading.current_thread().name)
  except:
    bstack11111l111_opy_ = 0
  bstack1llllll11_opy_ = bstack1lll11llll_opy_(CONFIG, bstack11111l111_opy_)
  logger.debug(bstack1ll1l1l1_opy_.format(str(bstack1llllll11_opy_)))
  if bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨଉ") in CONFIG and bstack1ll1ll111_opy_(CONFIG[bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩଊ")]):
    bstack1lll11lll_opy_(bstack1llllll11_opy_)
  if bstack11l1llll11_opy_.bstack1ll1ll11l1_opy_(CONFIG, bstack11111l111_opy_) and bstack11l1llll11_opy_.bstack1l1l1l1l1l_opy_(bstack1llllll11_opy_, options, desired_capabilities, CONFIG):
    threading.current_thread().a11yPlatform = True
    if (cli.accessibility is None or not cli.accessibility.is_enabled()):
      bstack11l1llll11_opy_.set_capabilities(bstack1llllll11_opy_, CONFIG)
  if desired_capabilities:
    bstack1ll11l1111_opy_ = bstack1ll11ll1l1_opy_(desired_capabilities)
    bstack1ll11l1111_opy_[bstack11lllll_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ଋ")] = bstack1l1ll11ll_opy_(CONFIG)
    bstack1ll1lllll1_opy_ = bstack1lll11llll_opy_(bstack1ll11l1111_opy_)
    if bstack1ll1lllll1_opy_:
      bstack1llllll11_opy_ = update(bstack1ll1lllll1_opy_, bstack1llllll11_opy_)
    desired_capabilities = None
  if options:
    bstack11l111l11l_opy_(options, bstack1llllll11_opy_)
  if not options:
    options = bstack1l111llll1_opy_(bstack1llllll11_opy_)
  bstack1111l11l1_opy_ = CONFIG.get(bstack11lllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଌ"))[bstack11111l111_opy_]
  if proxy and bstack111l1ll1l_opy_() >= version.parse(bstack11lllll_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨ଍")):
    options.proxy(proxy)
  if options and bstack111l1ll1l_opy_() >= version.parse(bstack11lllll_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ଎")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack111l1ll1l_opy_() < version.parse(bstack11lllll_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩଏ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1llllll11_opy_)
  logger.info(bstack1l1l1111ll_opy_)
  bstack11lll1l11l_opy_.end(EVENTS.bstack11111111_opy_.value, EVENTS.bstack11111111_opy_.value + bstack11lllll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦଐ"), EVENTS.bstack11111111_opy_.value + bstack11lllll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ଑"), status=True, failure=None, test_name=bstack11l1l1ll1l_opy_)
  if bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡱࡴࡲࡪ࡮ࡲࡥࠨ଒") in kwargs:
    del kwargs[bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡲࡵࡳ࡫࡯࡬ࡦࠩଓ")]
  bstack1lll11l1ll_opy_.end(EVENTS.bstack1ll11ll1_opy_.value, bstack1ll11111l_opy_ + bstack11lllll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣଔ"), bstack1ll11111l_opy_ + bstack11lllll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢକ"), status=True, failure=None, test_name=bstack11l1l1ll1l_opy_)
  try:
    if bstack111l1ll1l_opy_() >= version.parse(bstack11lllll_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪଖ")):
      bstack1l1lll11l1_opy_(self, command_executor=command_executor,
                options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
    elif bstack111l1ll1l_opy_() >= version.parse(bstack11lllll_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪଗ")):
      bstack1l1lll11l1_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities, options=options,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    elif bstack111l1ll1l_opy_() >= version.parse(bstack11lllll_opy_ (u"ࠬ࠸࠮࠶࠵࠱࠴ࠬଘ")):
      bstack1l1lll11l1_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    else:
      bstack1l1lll11l1_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive)
  except Exception as bstack1l111ll1l_opy_:
    logger.error(bstack11ll11llll_opy_.format(bstack11lllll_opy_ (u"࠭ࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠬଙ"), str(bstack1l111ll1l_opy_)))
    raise bstack1l111ll1l_opy_
  bstack1ll11111l_opy_ = bstack1lll11l1ll_opy_.bstack1llll1l1ll_opy_(EVENTS.bstack111lll1111_opy_.value)
  if bstack11l1llll11_opy_.bstack1ll1ll11l1_opy_(CONFIG, bstack11111l111_opy_) and bstack11l1llll11_opy_.bstack1l1l1l1l1l_opy_(self.caps, options, desired_capabilities):
    if CONFIG[bstack11lllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩଚ")][bstack11lllll_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧଛ")] == True:
      threading.current_thread().appA11yPlatform = True
      if cli.accessibility is None or not cli.accessibility.is_enabled():
        bstack11l1llll11_opy_.set_capabilities(bstack1llllll11_opy_, CONFIG)
  try:
    bstack1l1l1l1l11_opy_ = bstack11lllll_opy_ (u"ࠩࠪଜ")
    if bstack111l1ll1l_opy_() >= version.parse(bstack11lllll_opy_ (u"ࠪ࠸࠳࠶࠮࠱ࡤ࠴ࠫଝ")):
      if self.caps is not None:
        bstack1l1l1l1l11_opy_ = self.caps.get(bstack11lllll_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦଞ"))
    else:
      if self.capabilities is not None:
        bstack1l1l1l1l11_opy_ = self.capabilities.get(bstack11lllll_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧଟ"))
    if bstack1l1l1l1l11_opy_:
      bstack1llll11lll_opy_(bstack1l1l1l1l11_opy_)
      if bstack111l1ll1l_opy_() <= version.parse(bstack11lllll_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭ଠ")):
        self.command_executor._url = bstack11lllll_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣଡ") + bstack11l1ll111_opy_ + bstack11lllll_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧଢ")
      else:
        self.command_executor._url = bstack11lllll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦଣ") + bstack1l1l1l1l11_opy_ + bstack11lllll_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦତ")
      logger.debug(bstack1ll1l11l_opy_.format(bstack1l1l1l1l11_opy_))
    else:
      logger.debug(bstack11111llll_opy_.format(bstack11lllll_opy_ (u"ࠦࡔࡶࡴࡪ࡯ࡤࡰࠥࡎࡵࡣࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠧଥ")))
  except Exception as e:
    logger.debug(bstack11111llll_opy_.format(e))
  if bstack11lllll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫଦ") in bstack111ll1111_opy_:
    bstack11llll11_opy_(bstack1l11111ll_opy_, bstack1l1llll1l_opy_)
  bstack1ll11lll1l_opy_ = self.session_id
  if bstack11lllll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ଧ") in bstack111ll1111_opy_ or bstack11lllll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧନ") in bstack111ll1111_opy_ or bstack11lllll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ଩") in bstack111ll1111_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack1l11l1l1_opy_ = getattr(threading.current_thread(), bstack11lllll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡖࡨࡷࡹࡓࡥࡵࡣࠪପ"), None)
  if bstack11lllll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪଫ") in bstack111ll1111_opy_ or bstack11lllll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪବ") in bstack111ll1111_opy_:
    bstack11lll1111l_opy_.bstack1lll111lll_opy_(self)
  if bstack11lllll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬଭ") in bstack111ll1111_opy_ and bstack1l11l1l1_opy_ and bstack1l11l1l1_opy_.get(bstack11lllll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ମ"), bstack11lllll_opy_ (u"ࠧࠨଯ")) == bstack11lllll_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩର"):
    bstack11lll1111l_opy_.bstack1lll111lll_opy_(self)
  with bstack1l111ll111_opy_:
    bstack1l11ll11ll_opy_.append(self)
  if bstack11lllll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ଱") in CONFIG and bstack11lllll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨଲ") in CONFIG[bstack11lllll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଳ")][bstack11111l111_opy_]:
    bstack11l1l1ll1l_opy_ = CONFIG[bstack11lllll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ଴")][bstack11111l111_opy_][bstack11lllll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫଵ")]
  logger.debug(bstack11l11111_opy_.format(bstack1ll11lll1l_opy_))
  bstack1lll11l1ll_opy_.end(EVENTS.bstack111lll1111_opy_.value, bstack1ll11111l_opy_ + bstack11lllll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢଶ"), bstack1ll11111l_opy_ + bstack11lllll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨଷ"), status=True, failure=None, test_name=bstack11l1l1ll1l_opy_)
try:
  try:
    import Browser
    from subprocess import Popen
    from browserstack_sdk.__init__ import bstack1l11l111_opy_
    def bstack1l1llllll1_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack11llll1ll1_opy_
      if(bstack11lllll_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸ࠯࡬ࡶࠦସ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack11lllll_opy_ (u"ࠪࢂࠬହ")), bstack11lllll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ଺"), bstack11lllll_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧ଻")), bstack11lllll_opy_ (u"࠭ࡷࠨ଼")) as fp:
          fp.write(bstack11lllll_opy_ (u"ࠢࠣଽ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack11lllll_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥା")))):
          with open(args[1], bstack11lllll_opy_ (u"ࠩࡵࠫି")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack11lllll_opy_ (u"ࠪࡥࡸࡿ࡮ࡤࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࡤࡴࡥࡸࡒࡤ࡫ࡪ࠮ࡣࡰࡰࡷࡩࡽࡺࠬࠡࡲࡤ࡫ࡪࠦ࠽ࠡࡸࡲ࡭ࡩࠦ࠰ࠪࠩୀ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack11111l1l1_opy_)
            if bstack11lllll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨୁ") in CONFIG and str(CONFIG[bstack11lllll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩୂ")]).lower() != bstack11lllll_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬୃ"):
                bstack1l1l1111l1_opy_ = bstack1l11l111_opy_()
                bstack11l11l11l_opy_ = bstack11lllll_opy_ (u"ࠧࠨࠩࠍ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࠐࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹࡝࠼ࠌࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠ࠿ࠏࡩ࡯࡯ࡵࡷࠤࡵࡥࡩ࡯ࡦࡨࡼࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠳࡟࠾ࠎࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡸࡲࡩࡤࡧࠫ࠴࠱ࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴ࠫ࠾ࠎࡨࡵ࡮ࡴࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫ࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤࠬ࠿ࠏ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡲࡡࡶࡰࡦ࡬ࠥࡃࠠࡢࡵࡼࡲࡨࠦࠨ࡭ࡣࡸࡲࡨ࡮ࡏࡱࡶ࡬ࡳࡳࡹࠩࠡ࠿ࡁࠤࢀࢁࠊࠡࠢ࡯ࡩࡹࠦࡣࡢࡲࡶ࠿ࠏࠦࠠࡵࡴࡼࠤࢀࢁࠊࠡࠢࠣࠤࡨࡧࡰࡴࠢࡀࠤࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸ࠯࠻ࠋࠢࠣࢁࢂࠦࡣࡢࡶࡦ࡬ࠥ࠮ࡥࡹࠫࠣࡿࢀࠐࠠࠡࠢࠣࡧࡴࡴࡳࡰ࡮ࡨ࠲ࡪࡸࡲࡰࡴࠫࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷ࠿ࠨࠬࠡࡧࡻ࠭ࡀࠐࠠࠡࡿࢀࠎࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡩ࡯࡯ࡰࡨࡧࡹ࠮ࡻࡼࠌࠣࠤࠥࠦࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶ࠽ࠤࠬࢁࡣࡥࡲࡘࡶࡱࢃࠧࠡ࠭ࠣࡩࡳࡩ࡯ࡥࡧࡘࡖࡎࡉ࡯࡮ࡲࡲࡲࡪࡴࡴࠩࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡦࡥࡵࡹࠩࠪ࠮ࠍࠤࠥࠦࠠ࠯࠰࠱ࡰࡦࡻ࡮ࡤࡪࡒࡴࡹ࡯࡯࡯ࡵࠍࠤࠥࢃࡽࠪ࠽ࠍࢁࢂࡁࠊ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱ࠍࠫࠬ࠭ୄ").format(bstack1l1l1111l1_opy_=bstack1l1l1111l1_opy_)
            lines.insert(1, bstack11l11l11l_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack11lllll_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥ୅")), bstack11lllll_opy_ (u"ࠩࡺࠫ୆")) as bstack1lll111l11_opy_:
              bstack1lll111l11_opy_.writelines(lines)
        CONFIG[bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬେ")] = str(bstack111ll1111_opy_) + str(__version__)
        bstack111llllll1_opy_ = os.environ[bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩୈ")]
        bstack1l1l111ll1_opy_ = bstack1llll1111_opy_.bstack1111l111_opy_(CONFIG, bstack111ll1111_opy_)
        CONFIG[bstack11lllll_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ୉")] = bstack111llllll1_opy_
        CONFIG[bstack11lllll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨ୊")] = bstack1l1l111ll1_opy_
        bstack11111l111_opy_ = 0 if bstack1l11111ll_opy_ < 0 else bstack1l11111ll_opy_
        try:
          if bstack1lll1l1ll_opy_ is True:
            bstack11111l111_opy_ = int(multiprocessing.current_process().name)
          elif bstack1llllllll_opy_ is True:
            bstack11111l111_opy_ = int(threading.current_thread().name)
        except:
          bstack11111l111_opy_ = 0
        CONFIG[bstack11lllll_opy_ (u"ࠢࡶࡵࡨ࡛࠸ࡉࠢୋ")] = False
        CONFIG[bstack11lllll_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢୌ")] = True
        bstack1llllll11_opy_ = bstack1lll11llll_opy_(CONFIG, bstack11111l111_opy_)
        logger.debug(bstack1ll1l1l1_opy_.format(str(bstack1llllll11_opy_)))
        if CONFIG.get(bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ୍࠭")):
          bstack1lll11lll_opy_(bstack1llllll11_opy_)
        if bstack11lllll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭୎") in CONFIG and bstack11lllll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ୏") in CONFIG[bstack11lllll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ୐")][bstack11111l111_opy_]:
          bstack11l1l1ll1l_opy_ = CONFIG[bstack11lllll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ୑")][bstack11111l111_opy_][bstack11lllll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ୒")]
        args.append(os.path.join(os.path.expanduser(bstack11lllll_opy_ (u"ࠨࢀࠪ୓")), bstack11lllll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ୔"), bstack11lllll_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬ୕")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1llllll11_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack11lllll_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨୖ"))
      bstack11llll1ll1_opy_ = True
      return bstack11l11lll_opy_(self, args, bufsize=bufsize, executable=executable,
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
  def bstack111ll11l_opy_(self,
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
    global bstack1l11111ll_opy_
    global bstack11l1l1ll1l_opy_
    global bstack1lll1l1ll_opy_
    global bstack1llllllll_opy_
    global bstack111ll1111_opy_
    CONFIG[bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧୗ")] = str(bstack111ll1111_opy_) + str(__version__)
    bstack111llllll1_opy_ = os.environ[bstack11lllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ୘")]
    bstack1l1l111ll1_opy_ = bstack1llll1111_opy_.bstack1111l111_opy_(CONFIG, bstack111ll1111_opy_)
    CONFIG[bstack11lllll_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ୙")] = bstack111llllll1_opy_
    CONFIG[bstack11lllll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ୚")] = bstack1l1l111ll1_opy_
    bstack11111l111_opy_ = 0 if bstack1l11111ll_opy_ < 0 else bstack1l11111ll_opy_
    try:
      if bstack1lll1l1ll_opy_ is True:
        bstack11111l111_opy_ = int(multiprocessing.current_process().name)
      elif bstack1llllllll_opy_ is True:
        bstack11111l111_opy_ = int(threading.current_thread().name)
    except:
      bstack11111l111_opy_ = 0
    CONFIG[bstack11lllll_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ୛")] = True
    bstack1llllll11_opy_ = bstack1lll11llll_opy_(CONFIG, bstack11111l111_opy_)
    logger.debug(bstack1ll1l1l1_opy_.format(str(bstack1llllll11_opy_)))
    if CONFIG.get(bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧଡ଼")):
      bstack1lll11lll_opy_(bstack1llllll11_opy_)
    if bstack11lllll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଢ଼") in CONFIG and bstack11lllll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ୞") in CONFIG[bstack11lllll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩୟ")][bstack11111l111_opy_]:
      bstack11l1l1ll1l_opy_ = CONFIG[bstack11lllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪୠ")][bstack11111l111_opy_][bstack11lllll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ୡ")]
    import urllib
    import json
    if bstack11lllll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ୢ") in CONFIG and str(CONFIG[bstack11lllll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧୣ")]).lower() != bstack11lllll_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪ୤"):
        bstack111l11l1l1_opy_ = bstack1l11l111_opy_()
        bstack1l1l1111l1_opy_ = bstack111l11l1l1_opy_ + urllib.parse.quote(json.dumps(bstack1llllll11_opy_))
    else:
        bstack1l1l1111l1_opy_ = bstack11lllll_opy_ (u"ࠬࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠧ୥") + urllib.parse.quote(json.dumps(bstack1llllll11_opy_))
    browser = self.connect(bstack1l1l1111l1_opy_)
    return browser
except Exception as e:
    pass
def bstack1lll1l1ll1_opy_():
    global bstack11llll1ll1_opy_
    global bstack111ll1111_opy_
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1ll1l11l1l_opy_
        global bstack1l111111_opy_
        if not bstack11ll1l1l11_opy_:
          global bstack1l111111ll_opy_
          if not bstack1l111111ll_opy_:
            from bstack_utils.helper import bstack1ll11ll11_opy_, bstack1l1ll1llll_opy_, bstack11lll1llll_opy_
            bstack1l111111ll_opy_ = bstack1ll11ll11_opy_()
            bstack1l1ll1llll_opy_(bstack111ll1111_opy_)
            bstack1l1l111ll1_opy_ = bstack1llll1111_opy_.bstack1111l111_opy_(CONFIG, bstack111ll1111_opy_)
            bstack1l111111_opy_.bstack1llll1ll1l_opy_(bstack11lllll_opy_ (u"ࠨࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡔࡗࡕࡄࡖࡅࡗࡣࡒࡇࡐࠣ୦"), bstack1l1l111ll1_opy_)
          BrowserType.connect = bstack1ll1l11l1l_opy_
          return
        BrowserType.launch = bstack111ll11l_opy_
        bstack11llll1ll1_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1l1llllll1_opy_
      bstack11llll1ll1_opy_ = True
    except Exception as e:
      pass
def bstack11l1l1ll11_opy_(context, bstack1ll1111ll1_opy_):
  try:
    if getattr(context, bstack11lllll_opy_ (u"ࠧࡱࡣࡪࡩࠬ୧"), None):
      context.page.evaluate(bstack11lllll_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ୨"), bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿࠭୩")+ json.dumps(bstack1ll1111ll1_opy_) + bstack11lllll_opy_ (u"ࠥࢁࢂࠨ୪"))
  except Exception as e:
    logger.debug(bstack11lllll_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡻࡾ࠼ࠣࡿࢂࠨ୫").format(str(e), traceback.format_exc()))
def bstack1l1111l1l1_opy_(context, message, level):
  try:
    if getattr(context, bstack11lllll_opy_ (u"ࠬࡶࡡࡨࡧࠪ୬"), None):
      context.page.evaluate(bstack11lllll_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢ୭"), bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ୮") + json.dumps(message) + bstack11lllll_opy_ (u"ࠨ࠮ࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠫ୯") + json.dumps(level) + bstack11lllll_opy_ (u"ࠩࢀࢁࠬ୰"))
  except Exception as e:
    logger.debug(bstack11lllll_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡡ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠣࡿࢂࡀࠠࡼࡿࠥୱ").format(str(e), traceback.format_exc()))
@measure(event_name=EVENTS.bstack111l11llll_opy_, stage=STAGE.bstack1llll11111_opy_, bstack11lll11111_opy_=bstack11l1l1ll1l_opy_)
def bstack11l1llll1_opy_(self, url):
  global bstack11l1l111l1_opy_
  try:
    bstack1ll11l1l_opy_(url)
  except Exception as err:
    logger.debug(bstack1111111ll_opy_.format(str(err)))
  try:
    bstack11l1l111l1_opy_(self, url)
  except Exception as e:
    try:
      bstack1l11l1ll_opy_ = str(e)
      if any(err_msg in bstack1l11l1ll_opy_ for err_msg in bstack1l11l1111l_opy_):
        bstack1ll11l1l_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1111111ll_opy_.format(str(err)))
    raise e
def bstack1ll1lll1l_opy_(self):
  global bstack111l1lll_opy_
  bstack111l1lll_opy_ = self
  return
def bstack1l111l1ll_opy_(self):
  global bstack111l1l1l1l_opy_
  bstack111l1l1l1l_opy_ = self
  return
def bstack1ll111l1l1_opy_(test_name, bstack1l11ll1111_opy_):
  global CONFIG
  if percy.bstack11l1l1ll_opy_() == bstack11lllll_opy_ (u"ࠦࡹࡸࡵࡦࠤ୲"):
    bstack111l1llll_opy_ = os.path.relpath(bstack1l11ll1111_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack111l1llll_opy_)
    bstack11lll11111_opy_ = suite_name + bstack11lllll_opy_ (u"ࠧ࠳ࠢ୳") + test_name
    threading.current_thread().percySessionName = bstack11lll11111_opy_
def bstack1l11l11lll_opy_(self, test, *args, **kwargs):
  global bstack1l1ll111ll_opy_
  test_name = None
  bstack1l11ll1111_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1l11ll1111_opy_ = str(test.source)
  bstack1ll111l1l1_opy_(test_name, bstack1l11ll1111_opy_)
  bstack1l1ll111ll_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.bstack1111l111l_opy_, stage=STAGE.bstack1llll11111_opy_, bstack11lll11111_opy_=bstack11l1l1ll1l_opy_)
def bstack11ll11ll1l_opy_(driver, bstack11lll11111_opy_):
  if not bstack1ll111l1l_opy_ and bstack11lll11111_opy_:
      bstack11l1l11l_opy_ = {
          bstack11lllll_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭୴"): bstack11lllll_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ୵"),
          bstack11lllll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ୶"): {
              bstack11lllll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ୷"): bstack11lll11111_opy_
          }
      }
      bstack11lll11l1l_opy_ = bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨ୸").format(json.dumps(bstack11l1l11l_opy_))
      driver.execute_script(bstack11lll11l1l_opy_)
  if bstack11ll111l1_opy_:
      bstack111ll11l11_opy_ = {
          bstack11lllll_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫ୹"): bstack11lllll_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧ୺"),
          bstack11lllll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ୻"): {
              bstack11lllll_opy_ (u"ࠧࡥࡣࡷࡥࠬ୼"): bstack11lll11111_opy_ + bstack11lllll_opy_ (u"ࠨࠢࡳࡥࡸࡹࡥࡥࠣࠪ୽"),
              bstack11lllll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ୾"): bstack11lllll_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨ୿")
          }
      }
      if bstack11ll111l1_opy_.status == bstack11lllll_opy_ (u"ࠫࡕࡇࡓࡔࠩ஀"):
          bstack1l1111llll_opy_ = bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪ஁").format(json.dumps(bstack111ll11l11_opy_))
          driver.execute_script(bstack1l1111llll_opy_)
          bstack11l1l111l_opy_(driver, bstack11lllll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ஂ"))
      elif bstack11ll111l1_opy_.status == bstack11lllll_opy_ (u"ࠧࡇࡃࡌࡐࠬஃ"):
          reason = bstack11lllll_opy_ (u"ࠣࠤ஄")
          bstack1lll1lll1_opy_ = bstack11lll11111_opy_ + bstack11lllll_opy_ (u"ࠩࠣࡪࡦ࡯࡬ࡦࡦࠪஅ")
          if bstack11ll111l1_opy_.message:
              reason = str(bstack11ll111l1_opy_.message)
              bstack1lll1lll1_opy_ = bstack1lll1lll1_opy_ + bstack11lllll_opy_ (u"ࠪࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲ࠻ࠢࠪஆ") + reason
          bstack111ll11l11_opy_[bstack11lllll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧஇ")] = {
              bstack11lllll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫஈ"): bstack11lllll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬஉ"),
              bstack11lllll_opy_ (u"ࠧࡥࡣࡷࡥࠬஊ"): bstack1lll1lll1_opy_
          }
          bstack1l1111llll_opy_ = bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭஋").format(json.dumps(bstack111ll11l11_opy_))
          driver.execute_script(bstack1l1111llll_opy_)
          bstack11l1l111l_opy_(driver, bstack11lllll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ஌"), reason)
          bstack1lll11ll1_opy_(reason, str(bstack11ll111l1_opy_), str(bstack1l11111ll_opy_), logger)
@measure(event_name=EVENTS.bstack11l1ll11ll_opy_, stage=STAGE.bstack1llll11111_opy_, bstack11lll11111_opy_=bstack11l1l1ll1l_opy_)
def bstack1l1ll11l1l_opy_(driver, test):
  if percy.bstack11l1l1ll_opy_() == bstack11lllll_opy_ (u"ࠥࡸࡷࡻࡥࠣ஍") and percy.bstack1l1111lll1_opy_() == bstack11lllll_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨஎ"):
      bstack1lll1111_opy_ = bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠬࡶࡥࡳࡥࡼࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨஏ"), None)
      bstack11l111ll1_opy_(driver, bstack1lll1111_opy_, test)
  if (bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪஐ"), None) and
      bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭஑"), None)) or (
      bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨஒ"), None) and
      bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫஓ"), None)):
      logger.info(bstack11lllll_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠡࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡭ࡸࠦࡵ࡯ࡦࡨࡶࡼࡧࡹ࠯ࠢࠥஔ"))
      bstack11l1llll11_opy_.bstack1111ll1ll_opy_(driver, name=test.name, path=test.source)
def bstack1l1l1llll1_opy_(test, bstack11lll11111_opy_):
    try:
      bstack1l1111l111_opy_ = datetime.datetime.now()
      data = {}
      if test:
        data[bstack11lllll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩக")] = bstack11lll11111_opy_
      if bstack11ll111l1_opy_:
        if bstack11ll111l1_opy_.status == bstack11lllll_opy_ (u"ࠬࡖࡁࡔࡕࠪ஖"):
          data[bstack11lllll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭஗")] = bstack11lllll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ஘")
        elif bstack11ll111l1_opy_.status == bstack11lllll_opy_ (u"ࠨࡈࡄࡍࡑ࠭ங"):
          data[bstack11lllll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩச")] = bstack11lllll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ஛")
          if bstack11ll111l1_opy_.message:
            data[bstack11lllll_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫஜ")] = str(bstack11ll111l1_opy_.message)
      user = CONFIG[bstack11lllll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ஝")]
      key = CONFIG[bstack11lllll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩஞ")]
      host = bstack1lll1l111_opy_(cli.config, [bstack11lllll_opy_ (u"ࠢࡢࡲ࡬ࡷࠧட"), bstack11lllll_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧࠥ஠"), bstack11lllll_opy_ (u"ࠤࡤࡴ࡮ࠨ஡")], bstack11lllll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠦ஢"))
      url = bstack11lllll_opy_ (u"ࠫࢀࢃ࠯ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡶࡩࡸࡹࡩࡰࡰࡶ࠳ࢀࢃ࠮࡫ࡵࡲࡲࠬண").format(host, bstack1ll11lll1l_opy_)
      headers = {
        bstack11lllll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫத"): bstack11lllll_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ஥"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers, auth=(user, key))
        cli.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠢࡩࡶࡷࡴ࠿ࡻࡰࡥࡣࡷࡩࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡸࡺࡡࡵࡷࡶࠦ஦"), datetime.datetime.now() - bstack1l1111l111_opy_)
    except Exception as e:
      logger.error(bstack1ll1l1111_opy_.format(str(e)))
def bstack111llll11_opy_(test, bstack11lll11111_opy_):
  global CONFIG
  global bstack111l1l1l1l_opy_
  global bstack111l1lll_opy_
  global bstack1ll11lll1l_opy_
  global bstack11ll111l1_opy_
  global bstack11l1l1ll1l_opy_
  global bstack1l1l111l_opy_
  global bstack111l11ll_opy_
  global bstack11ll1l1ll_opy_
  global bstack11lllll1_opy_
  global bstack1l11ll11ll_opy_
  global bstack1111l11l1_opy_
  global bstack1l1l1ll1ll_opy_
  try:
    if not bstack1ll11lll1l_opy_:
      with bstack1l1l1ll1ll_opy_:
        bstack11ll11l1l1_opy_ = os.path.join(os.path.expanduser(bstack11lllll_opy_ (u"ࠨࢀࠪ஧")), bstack11lllll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩந"), bstack11lllll_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬன"))
        if os.path.exists(bstack11ll11l1l1_opy_):
          with open(bstack11ll11l1l1_opy_, bstack11lllll_opy_ (u"ࠫࡷ࠭ப")) as f:
            content = f.read().strip()
            if content:
              bstack1l1111l1ll_opy_ = json.loads(bstack11lllll_opy_ (u"ࠧࢁࠢ஫") + content + bstack11lllll_opy_ (u"࠭ࠢࡹࠤ࠽ࠤࠧࡿࠢࠨ஬") + bstack11lllll_opy_ (u"ࠢࡾࠤ஭"))
              bstack1ll11lll1l_opy_ = bstack1l1111l1ll_opy_.get(str(threading.get_ident()))
  except Exception as e:
    logger.debug(bstack11lllll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡳࡧࡤࡨ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡌࡈࡸࠦࡦࡪ࡮ࡨ࠾ࠥ࠭ம") + str(e))
  if bstack1l11ll11ll_opy_:
    with bstack1l111ll111_opy_:
      bstack1llll1llll_opy_ = bstack1l11ll11ll_opy_.copy()
    for driver in bstack1llll1llll_opy_:
      if bstack1ll11lll1l_opy_ == driver.session_id:
        if test:
          bstack1l1ll11l1l_opy_(driver, test)
        bstack11ll11ll1l_opy_(driver, bstack11lll11111_opy_)
  elif bstack1ll11lll1l_opy_:
    bstack1l1l1llll1_opy_(test, bstack11lll11111_opy_)
  if bstack111l1l1l1l_opy_:
    bstack111l11ll_opy_(bstack111l1l1l1l_opy_)
  if bstack111l1lll_opy_:
    bstack11ll1l1ll_opy_(bstack111l1lll_opy_)
  if bstack1ll1ll1ll_opy_:
    bstack11lllll1_opy_()
def bstack1ll1l11lll_opy_(self, test, *args, **kwargs):
  bstack11lll11111_opy_ = None
  if test:
    bstack11lll11111_opy_ = str(test.name)
  bstack111llll11_opy_(test, bstack11lll11111_opy_)
  bstack1l1l111l_opy_(self, test, *args, **kwargs)
def bstack11ll111l11_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1111ll111_opy_
  global CONFIG
  global bstack1l11ll11ll_opy_
  global bstack1ll11lll1l_opy_
  global bstack1l1l1ll1ll_opy_
  bstack111lll11ll_opy_ = None
  try:
    if bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨய"), None) or bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬர"), None):
      try:
        if not bstack1ll11lll1l_opy_:
          bstack11ll11l1l1_opy_ = os.path.join(os.path.expanduser(bstack11lllll_opy_ (u"ࠫࢃ࠭ற")), bstack11lllll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬல"), bstack11lllll_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨள"))
          with bstack1l1l1ll1ll_opy_:
            if os.path.exists(bstack11ll11l1l1_opy_):
              with open(bstack11ll11l1l1_opy_, bstack11lllll_opy_ (u"ࠧࡳࠩழ")) as f:
                content = f.read().strip()
                if content:
                  bstack1l1111l1ll_opy_ = json.loads(bstack11lllll_opy_ (u"ࠣࡽࠥவ") + content + bstack11lllll_opy_ (u"ࠩࠥࡼࠧࡀࠠࠣࡻࠥࠫஶ") + bstack11lllll_opy_ (u"ࠥࢁࠧஷ"))
                  bstack1ll11lll1l_opy_ = bstack1l1111l1ll_opy_.get(str(threading.get_ident()))
      except Exception as e:
        logger.debug(bstack11lllll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡶࡪࡧࡤࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡏࡄࡴࠢࡩ࡭ࡱ࡫ࠠࡪࡰࠣࡸࡪࡹࡴࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࠪஸ") + str(e))
      if bstack1l11ll11ll_opy_:
        with bstack1l111ll111_opy_:
          bstack1llll1llll_opy_ = bstack1l11ll11ll_opy_.copy()
        for driver in bstack1llll1llll_opy_:
          if bstack1ll11lll1l_opy_ == driver.session_id:
            bstack111lll11ll_opy_ = driver
    bstack11ll1l1l_opy_ = bstack11l1llll11_opy_.bstack1l11lll111_opy_(test.tags)
    if bstack111lll11ll_opy_:
      threading.current_thread().isA11yTest = bstack11l1llll11_opy_.bstack1ll11l1l11_opy_(bstack111lll11ll_opy_, bstack11ll1l1l_opy_)
      threading.current_thread().isAppA11yTest = bstack11l1llll11_opy_.bstack1ll11l1l11_opy_(bstack111lll11ll_opy_, bstack11ll1l1l_opy_)
    else:
      threading.current_thread().isA11yTest = bstack11ll1l1l_opy_
      threading.current_thread().isAppA11yTest = bstack11ll1l1l_opy_
  except:
    pass
  bstack1111ll111_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack11ll111l1_opy_
  try:
    bstack11ll111l1_opy_ = self._test
  except:
    bstack11ll111l1_opy_ = self.test
def bstack1ll1llll_opy_():
  global bstack11ll1l11ll_opy_
  try:
    if os.path.exists(bstack11ll1l11ll_opy_):
      os.remove(bstack11ll1l11ll_opy_)
  except Exception as e:
    logger.debug(bstack11lllll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨஹ") + str(e))
def bstack11ll11l1l_opy_():
  global bstack11ll1l11ll_opy_
  bstack1ll1ll1l1_opy_ = {}
  lock_file = bstack11ll1l11ll_opy_ + bstack11lllll_opy_ (u"࠭࠮࡭ࡱࡦ࡯ࠬ஺")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack11lllll_opy_ (u"ࠧࡧ࡫࡯ࡩࡱࡵࡣ࡬ࠢࡱࡳࡹࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦ࠮ࠣࡹࡸ࡯࡮ࡨࠢࡥࡥࡸ࡯ࡣࠡࡨ࡬ࡰࡪࠦ࡯ࡱࡧࡵࡥࡹ࡯࡯࡯ࡵࠪ஻"))
    try:
      if not os.path.isfile(bstack11ll1l11ll_opy_):
        with open(bstack11ll1l11ll_opy_, bstack11lllll_opy_ (u"ࠨࡹࠪ஼")) as f:
          json.dump({}, f)
      if os.path.exists(bstack11ll1l11ll_opy_):
        with open(bstack11ll1l11ll_opy_, bstack11lllll_opy_ (u"ࠩࡵࠫ஽")) as f:
          content = f.read().strip()
          if content:
            bstack1ll1ll1l1_opy_ = json.loads(content)
    except Exception as e:
      logger.debug(bstack11lllll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡸࡥࡢࡦ࡬ࡲ࡬ࠦࡲࡰࡤࡲࡸࠥࡸࡥࡱࡱࡵࡸࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬா") + str(e))
    return bstack1ll1ll1l1_opy_
  try:
    os.makedirs(os.path.dirname(bstack11ll1l11ll_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      if not os.path.isfile(bstack11ll1l11ll_opy_):
        with open(bstack11ll1l11ll_opy_, bstack11lllll_opy_ (u"ࠫࡼ࠭ி")) as f:
          json.dump({}, f)
      if os.path.exists(bstack11ll1l11ll_opy_):
        with open(bstack11ll1l11ll_opy_, bstack11lllll_opy_ (u"ࠬࡸࠧீ")) as f:
          content = f.read().strip()
          if content:
            bstack1ll1ll1l1_opy_ = json.loads(content)
  except Exception as e:
    logger.debug(bstack11lllll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡴࡨࡥࡩ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨு") + str(e))
  finally:
    return bstack1ll1ll1l1_opy_
def bstack11llll11_opy_(platform_index, item_index):
  global bstack11ll1l11ll_opy_
  lock_file = bstack11ll1l11ll_opy_ + bstack11lllll_opy_ (u"ࠧ࠯࡮ࡲࡧࡰ࠭ூ")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack11lllll_opy_ (u"ࠨࡨ࡬ࡰࡪࡲ࡯ࡤ࡭ࠣࡲࡴࡺࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧ࠯ࠤࡺࡹࡩ࡯ࡩࠣࡦࡦࡹࡩࡤࠢࡩ࡭ࡱ࡫ࠠࡰࡲࡨࡶࡦࡺࡩࡰࡰࡶࠫ௃"))
    try:
      bstack1ll1ll1l1_opy_ = {}
      if os.path.exists(bstack11ll1l11ll_opy_):
        with open(bstack11ll1l11ll_opy_, bstack11lllll_opy_ (u"ࠩࡵࠫ௄")) as f:
          content = f.read().strip()
          if content:
            bstack1ll1ll1l1_opy_ = json.loads(content)
      bstack1ll1ll1l1_opy_[item_index] = platform_index
      with open(bstack11ll1l11ll_opy_, bstack11lllll_opy_ (u"ࠥࡻࠧ௅")) as outfile:
        json.dump(bstack1ll1ll1l1_opy_, outfile)
    except Exception as e:
      logger.debug(bstack11lllll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡷࡳ࡫ࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺ࠡࠩெ") + str(e))
    return
  try:
    os.makedirs(os.path.dirname(bstack11ll1l11ll_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      bstack1ll1ll1l1_opy_ = {}
      if os.path.exists(bstack11ll1l11ll_opy_):
        with open(bstack11ll1l11ll_opy_, bstack11lllll_opy_ (u"ࠬࡸࠧே")) as f:
          content = f.read().strip()
          if content:
            bstack1ll1ll1l1_opy_ = json.loads(content)
      bstack1ll1ll1l1_opy_[item_index] = platform_index
      with open(bstack11ll1l11ll_opy_, bstack11lllll_opy_ (u"ࠨࡷࠣை")) as outfile:
        json.dump(bstack1ll1ll1l1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack11lllll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡺࡶ࡮ࡺࡩ࡯ࡩࠣࡸࡴࠦࡲࡰࡤࡲࡸࠥࡸࡥࡱࡱࡵࡸࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬ௉") + str(e))
def bstack1ll1lll1ll_opy_(bstack11l1lllll1_opy_):
  global CONFIG
  bstack1l111llll_opy_ = bstack11lllll_opy_ (u"ࠨࠩொ")
  if not bstack11lllll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬோ") in CONFIG:
    logger.info(bstack11lllll_opy_ (u"ࠪࡒࡴࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠢࡳࡥࡸࡹࡥࡥࠢࡸࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡳࡧࡳࡳࡷࡺࠠࡧࡱࡵࠤࡗࡵࡢࡰࡶࠣࡶࡺࡴࠧௌ"))
  try:
    platform = CONFIG[bstack11lllll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹ்ࠧ")][bstack11l1lllll1_opy_]
    if bstack11lllll_opy_ (u"ࠬࡵࡳࠨ௎") in platform:
      bstack1l111llll_opy_ += str(platform[bstack11lllll_opy_ (u"࠭࡯ࡴࠩ௏")]) + bstack11lllll_opy_ (u"ࠧ࠭ࠢࠪௐ")
    if bstack11lllll_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫ௑") in platform:
      bstack1l111llll_opy_ += str(platform[bstack11lllll_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬ௒")]) + bstack11lllll_opy_ (u"ࠪ࠰ࠥ࠭௓")
    if bstack11lllll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨ௔") in platform:
      bstack1l111llll_opy_ += str(platform[bstack11lllll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩ௕")]) + bstack11lllll_opy_ (u"࠭ࠬࠡࠩ௖")
    if bstack11lllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩௗ") in platform:
      bstack1l111llll_opy_ += str(platform[bstack11lllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪ௘")]) + bstack11lllll_opy_ (u"ࠩ࠯ࠤࠬ௙")
    if bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ௚") in platform:
      bstack1l111llll_opy_ += str(platform[bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ௛")]) + bstack11lllll_opy_ (u"ࠬ࠲ࠠࠨ௜")
    if bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ௝") in platform:
      bstack1l111llll_opy_ += str(platform[bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ௞")]) + bstack11lllll_opy_ (u"ࠨ࠮ࠣࠫ௟")
  except Exception as e:
    logger.debug(bstack11lllll_opy_ (u"ࠩࡖࡳࡲ࡫ࠠࡦࡴࡵࡳࡷࠦࡩ࡯ࠢࡪࡩࡳ࡫ࡲࡢࡶ࡬ࡲ࡬ࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡵࡷࡶ࡮ࡴࡧࠡࡨࡲࡶࠥࡸࡥࡱࡱࡵࡸࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡯࡯࡯ࠩ௠") + str(e))
  finally:
    if bstack1l111llll_opy_[len(bstack1l111llll_opy_) - 2:] == bstack11lllll_opy_ (u"ࠪ࠰ࠥ࠭௡"):
      bstack1l111llll_opy_ = bstack1l111llll_opy_[:-2]
    return bstack1l111llll_opy_
def bstack1l111l1l1_opy_(path, bstack1l111llll_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1lll1ll1l_opy_ = ET.parse(path)
    bstack1lll1l11l1_opy_ = bstack1lll1ll1l_opy_.getroot()
    bstack1l11111l_opy_ = None
    for suite in bstack1lll1l11l1_opy_.iter(bstack11lllll_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪ௢")):
      if bstack11lllll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ௣") in suite.attrib:
        suite.attrib[bstack11lllll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ௤")] += bstack11lllll_opy_ (u"ࠧࠡࠩ௥") + bstack1l111llll_opy_
        bstack1l11111l_opy_ = suite
    bstack1lll11111_opy_ = None
    for robot in bstack1lll1l11l1_opy_.iter(bstack11lllll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ௦")):
      bstack1lll11111_opy_ = robot
    bstack1l1lllll11_opy_ = len(bstack1lll11111_opy_.findall(bstack11lllll_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨ௧")))
    if bstack1l1lllll11_opy_ == 1:
      bstack1lll11111_opy_.remove(bstack1lll11111_opy_.findall(bstack11lllll_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩ௨"))[0])
      bstack11l111llll_opy_ = ET.Element(bstack11lllll_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪ௩"), attrib={bstack11lllll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ௪"): bstack11lllll_opy_ (u"࠭ࡓࡶ࡫ࡷࡩࡸ࠭௫"), bstack11lllll_opy_ (u"ࠧࡪࡦࠪ௬"): bstack11lllll_opy_ (u"ࠨࡵ࠳ࠫ௭")})
      bstack1lll11111_opy_.insert(1, bstack11l111llll_opy_)
      bstack1ll11l1ll_opy_ = None
      for suite in bstack1lll11111_opy_.iter(bstack11lllll_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨ௮")):
        bstack1ll11l1ll_opy_ = suite
      bstack1ll11l1ll_opy_.append(bstack1l11111l_opy_)
      bstack11llll11ll_opy_ = None
      for status in bstack1l11111l_opy_.iter(bstack11lllll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ௯")):
        bstack11llll11ll_opy_ = status
      bstack1ll11l1ll_opy_.append(bstack11llll11ll_opy_)
    bstack1lll1ll1l_opy_.write(path)
  except Exception as e:
    logger.debug(bstack11lllll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡢࡴࡶ࡭ࡳ࡭ࠠࡸࡪ࡬ࡰࡪࠦࡧࡦࡰࡨࡶࡦࡺࡩ࡯ࡩࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠩ௰") + str(e))
def bstack1l111l1l1l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack111llll1ll_opy_
  global CONFIG
  if bstack11lllll_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡵࡧࡴࡩࠤ௱") in options:
    del options[bstack11lllll_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡶࡡࡵࡪࠥ௲")]
  bstack111l1l1l11_opy_ = bstack11ll11l1l_opy_()
  for item_id in bstack111l1l1l11_opy_.keys():
    path = os.path.join(outs_dir, str(item_id), bstack11lllll_opy_ (u"ࠧࡰࡷࡷࡴࡺࡺ࠮ࡹ࡯࡯ࠫ௳"))
    bstack1l111l1l1_opy_(path, bstack1ll1lll1ll_opy_(bstack111l1l1l11_opy_[item_id]))
  bstack1ll1llll_opy_()
  return bstack111llll1ll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack11ll11l1ll_opy_(self, ff_profile_dir):
  global bstack1111ll11_opy_
  if not ff_profile_dir:
    return None
  return bstack1111ll11_opy_(self, ff_profile_dir)
def bstack1ll11l11l1_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1lll1ll11l_opy_
  bstack111ll1l1l_opy_ = []
  if bstack11lllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ௴") in CONFIG:
    bstack111ll1l1l_opy_ = CONFIG[bstack11lllll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ௵")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack11lllll_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࠦ௶")],
      pabot_args[bstack11lllll_opy_ (u"ࠦࡻ࡫ࡲࡣࡱࡶࡩࠧ௷")],
      argfile,
      pabot_args.get(bstack11lllll_opy_ (u"ࠧ࡮ࡩࡷࡧࠥ௸")),
      pabot_args[bstack11lllll_opy_ (u"ࠨࡰࡳࡱࡦࡩࡸࡹࡥࡴࠤ௹")],
      platform[0],
      bstack1lll1ll11l_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack11lllll_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡨ࡬ࡰࡪࡹࠢ௺")] or [(bstack11lllll_opy_ (u"ࠣࠤ௻"), None)]
    for platform in enumerate(bstack111ll1l1l_opy_)
  ]
def bstack1l11ll1ll_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1l1l11l11l_opy_=bstack11lllll_opy_ (u"ࠩࠪ௼")):
  global bstack111111ll_opy_
  self.platform_index = platform_index
  self.bstack11l1l1l111_opy_ = bstack1l1l11l11l_opy_
  bstack111111ll_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1lll1l1111_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1ll11ll111_opy_
  global bstack1ll1l11ll1_opy_
  bstack1l1l11l1l1_opy_ = copy.deepcopy(item)
  if not bstack11lllll_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ௽") in item.options:
    bstack1l1l11l1l1_opy_.options[bstack11lllll_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭௾")] = []
  bstack1ll1llll1_opy_ = bstack1l1l11l1l1_opy_.options[bstack11lllll_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ௿")].copy()
  for v in bstack1l1l11l1l1_opy_.options[bstack11lllll_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨఀ")]:
    if bstack11lllll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝࠭ఁ") in v:
      bstack1ll1llll1_opy_.remove(v)
    if bstack11lllll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓࠨం") in v:
      bstack1ll1llll1_opy_.remove(v)
    if bstack11lllll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡆࡈࡊࡑࡕࡃࡂࡎࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ః") in v:
      bstack1ll1llll1_opy_.remove(v)
  bstack1ll1llll1_opy_.insert(0, bstack11lllll_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡓࡐࡆ࡚ࡆࡐࡔࡐࡍࡓࡊࡅ࡙࠼ࡾࢁࠬఄ").format(bstack1l1l11l1l1_opy_.platform_index))
  bstack1ll1llll1_opy_.insert(0, bstack11lllll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒ࠻ࡽࢀࠫఅ").format(bstack1l1l11l1l1_opy_.bstack11l1l1l111_opy_))
  bstack1l1l11l1l1_opy_.options[bstack11lllll_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧఆ")] = bstack1ll1llll1_opy_
  if bstack1ll1l11ll1_opy_:
    bstack1l1l11l1l1_opy_.options[bstack11lllll_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨఇ")].insert(0, bstack11lllll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙࠺ࡼࡿࠪఈ").format(bstack1ll1l11ll1_opy_))
  return bstack1ll11ll111_opy_(caller_id, datasources, is_last, bstack1l1l11l1l1_opy_, outs_dir)
def bstack1l1111l1l_opy_(command, item_index):
  try:
    if bstack1l111111_opy_.get_property(bstack11lllll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩఉ")):
      os.environ[bstack11lllll_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪఊ")] = json.dumps(CONFIG[bstack11lllll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ఋ")][item_index % bstack111lllllll_opy_])
    global bstack1ll1l11ll1_opy_
    if bstack1ll1l11ll1_opy_:
      command[0] = command[0].replace(bstack11lllll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪఌ"), bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡸࡪ࡫ࠡࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠢ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࠥ࠭఍") + str(item_index % bstack111lllllll_opy_) + bstack11lllll_opy_ (u"࠭ࠠ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽࠦࠧఎ") + str(
        item_index) + bstack11lllll_opy_ (u"ࠧࠡࠩఏ") + bstack1ll1l11ll1_opy_, 1)
    else:
      command[0] = command[0].replace(bstack11lllll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧఐ"),
                                      bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠮ࡵࡧ࡯ࠥࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱࠦ࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࠢࠪ఑") +  str(item_index % bstack111lllllll_opy_) + bstack11lllll_opy_ (u"ࠪࠤ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠣࠫఒ") + str(item_index), 1)
  except Exception as e:
    logger.error(bstack11lllll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡱࡴࡪࡩࡧࡻ࡬ࡲ࡬ࠦࡣࡰ࡯ࡰࡥࡳࡪࠠࡧࡱࡵࠤࡵࡧࡢࡰࡶࠣࡶࡺࡴ࠺ࠡࡽࢀࠫఓ").format(str(e)))
def bstack111ll1l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack11ll1ll1ll_opy_
  try:
    bstack1l1111l1l_opy_(command, item_index)
    return bstack11ll1ll1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
  except Exception as e:
    logger.error(bstack11lllll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡥࡳࡹࠦࡲࡶࡰ࠽ࠤࢀࢃࠧఔ").format(str(e)))
    raise e
def bstack111l11lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack11ll1ll1ll_opy_
  try:
    bstack1l1111l1l_opy_(command, item_index)
    return bstack11ll1ll1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
  except Exception as e:
    logger.error(bstack11lllll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠࡳࡷࡱࠤ࠷࠴࠱࠴࠼ࠣࡿࢂ࠭క").format(str(e)))
    try:
      return bstack11ll1ll1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
    except Exception as e2:
      logger.error(bstack11lllll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡧࡵࡴࠡ࠴࠱࠵࠸ࠦࡦࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢࡾࢁࠬఖ").format(str(e2)))
      raise e
def bstack1ll111ll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack11ll1ll1ll_opy_
  try:
    bstack1l1111l1l_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    return bstack11ll1ll1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
  except Exception as e:
    logger.error(bstack11lllll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡦࡨ࡯ࡵࠢࡵࡹࡳࠦ࠲࠯࠳࠸࠾ࠥࢁࡽࠨగ").format(str(e)))
    try:
      return bstack11ll1ll1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
    except Exception as e2:
      logger.error(bstack11lllll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡢࡰࡶࠣ࠶࠳࠷࠵ࠡࡨࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࢀࢃࠧఘ").format(str(e2)))
      raise e
def _111ll1l1l1_opy_(bstack111ll1111l_opy_, item_index, process_timeout, sleep_before_start, bstack1ll111111l_opy_):
  bstack1l1111l1l_opy_(bstack111ll1111l_opy_, item_index)
  if process_timeout is None:
    process_timeout = 3600
  if sleep_before_start and sleep_before_start > 0:
    time.sleep(min(sleep_before_start, 5))
  return process_timeout
def bstack1llllll1ll_opy_(command, bstack11l11lll11_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack11ll1ll1ll_opy_
  global bstack1l11l11l1_opy_
  global bstack1ll1l11ll1_opy_
  try:
    for env_name, bstack1l11lll1ll_opy_ in bstack1l11l11l1_opy_.items():
      os.environ[env_name] = bstack1l11lll1ll_opy_
    bstack1ll1l11ll1_opy_ = bstack11lllll_opy_ (u"ࠥࠦఙ")
    bstack1l1111l1l_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    if sleep_before_start and sleep_before_start > 0:
      time.sleep(min(sleep_before_start, 5))
    return bstack11ll1ll1ll_opy_(command, bstack11l11lll11_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack11lllll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡢࡤࡲࡸࠥࡸࡵ࡯ࠢ࠸࠲࠵ࡀࠠࡼࡿࠪచ").format(str(e)))
    try:
      return bstack11ll1ll1ll_opy_(command, bstack11l11lll11_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack11lllll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡥࡳࡹࠦࡦࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢࡾࢁࠬఛ").format(str(e2)))
      raise e
def bstack1l1ll1ll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack11ll1ll1ll_opy_
  try:
    process_timeout = _111ll1l1l1_opy_(command, item_index, process_timeout, sleep_before_start, bstack11lllll_opy_ (u"࠭࠴࠯࠴ࠪజ"))
    return bstack11ll1ll1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack11lllll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡧࡵࡴࠡࡴࡸࡲࠥ࠺࠮࠳࠼ࠣࡿࢂ࠭ఝ").format(str(e)))
    try:
      return bstack11ll1ll1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack11lllll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡦࡨ࡯ࡵࠢࡩࡥࡱࡲࡢࡢࡥ࡮࠾ࠥࢁࡽࠨఞ").format(str(e2)))
      raise e
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack111ll11l1_opy_(self, runner, quiet=False, capture=True):
  global bstack11l111lll1_opy_
  bstack111ll111ll_opy_ = bstack11l111lll1_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack11lllll_opy_ (u"ࠩࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࡤࡧࡲࡳࠩట")):
      runner.exception_arr = []
    if not hasattr(runner, bstack11lllll_opy_ (u"ࠪࡩࡽࡩ࡟ࡵࡴࡤࡧࡪࡨࡡࡤ࡭ࡢࡥࡷࡸࠧఠ")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack111ll111ll_opy_
def bstack11ll1111ll_opy_(runner, hook_name, context, element, bstack1ll1l1ll1l_opy_, *args):
  global bstack1ll1l1l111_opy_
  try:
    if runner.hooks.get(hook_name):
      bstack1lllllll1_opy_.bstack1l11ll111_opy_(hook_name, element)
    if bstack1ll1l1l111_opy_ is None or bstack1ll1l1l111_opy_:
      bstack1ll1l1ll1l_opy_(runner, hook_name, context, *args)
    else:
      bstack11ll111l1l_opy_ = (context,) + args
      bstack1ll1l1ll1l_opy_(runner, hook_name, *bstack11ll111l1l_opy_)
    if runner.hooks.get(hook_name):
      bstack1lllllll1_opy_.bstack111l11l11l_opy_(element)
      if hook_name not in [bstack11lllll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠨడ"), bstack11lllll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠨఢ")] and args and hasattr(args[0], bstack11lllll_opy_ (u"࠭ࡥࡳࡴࡲࡶࡤࡳࡥࡴࡵࡤ࡫ࡪ࠭ణ")):
        args[0].error_message = bstack11lllll_opy_ (u"ࠧࠨత")
  except Exception as e:
    logger.debug(bstack11lllll_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡭ࡧ࡮ࡥ࡮ࡨࠤ࡭ࡵ࡯࡬ࡵࠣ࡭ࡳࠦࡢࡦࡪࡤࡺࡪࡀࠠࡼࡿࠪథ").format(str(e)))
@measure(event_name=EVENTS.bstack1ll1l1l11l_opy_, stage=STAGE.bstack1llll11111_opy_, hook_type=bstack11lllll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡃ࡯ࡰࠧద"), bstack11lll11111_opy_=bstack11l1l1ll1l_opy_)
def bstack111l1l11l1_opy_(runner, name, context, bstack1ll1l1ll1l_opy_, *args):
    if runner.hooks.get(bstack11lllll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢధ")).__name__ != bstack11lllll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࡠࡦࡨࡪࡦࡻ࡬ࡵࡡ࡫ࡳࡴࡱࠢన"):
      bstack11ll1111ll_opy_(runner, name, context, runner, bstack1ll1l1ll1l_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack1lllll11_opy_(bstack11lllll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ఩")) else context.browser
      runner.driver_initialised = bstack11lllll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥప")
    except Exception as e:
      logger.debug(bstack11lllll_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡥࡴ࡬ࡺࡪࡸࠠࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡨࠤࡦࡺࡴࡳ࡫ࡥࡹࡹ࡫࠺ࠡࡽࢀࠫఫ").format(str(e)))
def bstack1l1ll1l11_opy_(runner, name, context, bstack1ll1l1ll1l_opy_, *args):
    bstack11ll1111ll_opy_(runner, name, context, context.feature, bstack1ll1l1ll1l_opy_, *args)
    try:
      if not bstack1ll111l1l_opy_:
        bstack111lll11ll_opy_ = threading.current_thread().bstackSessionDriver if bstack1lllll11_opy_(bstack11lllll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧబ")) else context.browser
        if is_driver_active(bstack111lll11ll_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack11lllll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠥభ")
          bstack1ll1111ll1_opy_ = str(runner.feature.name)
          bstack11l1l1ll11_opy_(context, bstack1ll1111ll1_opy_)
          bstack111lll11ll_opy_.execute_script(bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨమ") + json.dumps(bstack1ll1111ll1_opy_) + bstack11lllll_opy_ (u"ࠫࢂࢃࠧయ"))
    except Exception as e:
      logger.debug(bstack11lllll_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤ࡮ࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡧࡧࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬర").format(str(e)))
def bstack1l111l1l11_opy_(runner, name, context, bstack1ll1l1ll1l_opy_, *args):
    target = context.scenario if hasattr(context, bstack11lllll_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨఱ")) else context.feature
    bstack11ll1111ll_opy_(runner, name, context, target, bstack1ll1l1ll1l_opy_, *args)
@measure(event_name=EVENTS.bstack1ll1l11ll_opy_, stage=STAGE.bstack1llll11111_opy_, bstack11lll11111_opy_=bstack11l1l1ll1l_opy_)
def bstack11llll1lll_opy_(runner, name, context, bstack1ll1l1ll1l_opy_, *args):
    bstack1lllllll1_opy_.start_test(context)
    bstack11ll1111ll_opy_(runner, name, context, context.scenario, bstack1ll1l1ll1l_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack11l11l1l1_opy_.bstack11l1l111_opy_(context, *args)
    try:
      bstack111lll11ll_opy_ = bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ల"), context.browser)
      if is_driver_active(bstack111lll11ll_opy_):
        bstack11lll1111l_opy_.bstack1lll111lll_opy_(bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧళ"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack11lllll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦఴ")
        if (not bstack1ll111l1l_opy_):
          scenario_name = args[0].name
          feature_name = bstack1ll1111ll1_opy_ = str(runner.feature.name)
          bstack1ll1111ll1_opy_ = feature_name + bstack11lllll_opy_ (u"ࠪࠤ࠲ࠦࠧవ") + scenario_name
          if runner.driver_initialised == bstack11lllll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨశ"):
            bstack11l1l1ll11_opy_(context, bstack1ll1111ll1_opy_)
            bstack111lll11ll_opy_.execute_script(bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪష") + json.dumps(bstack1ll1111ll1_opy_) + bstack11lllll_opy_ (u"࠭ࡽࡾࠩస"))
    except Exception as e:
      logger.debug(bstack11lllll_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡧࡪࡴࡡࡳ࡫ࡲ࠾ࠥࢁࡽࠨహ").format(str(e)))
@measure(event_name=EVENTS.bstack1ll1l1l11l_opy_, stage=STAGE.bstack1llll11111_opy_, hook_type=bstack11lllll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡔࡶࡨࡴࠧ఺"), bstack11lll11111_opy_=bstack11l1l1ll1l_opy_)
def bstack1lll11ll_opy_(runner, name, context, bstack1ll1l1ll1l_opy_, *args):
    bstack11ll1111ll_opy_(runner, name, context, args[0], bstack1ll1l1ll1l_opy_, *args)
    try:
      bstack111lll11ll_opy_ = threading.current_thread().bstackSessionDriver if bstack1lllll11_opy_(bstack11lllll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ఻")) else context.browser
      if is_driver_active(bstack111lll11ll_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack11lllll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰ఼ࠣ")
        bstack1lllllll1_opy_.bstack111ll1llll_opy_(args[0])
        if runner.driver_initialised == bstack11lllll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤఽ"):
          feature_name = bstack1ll1111ll1_opy_ = str(runner.feature.name)
          bstack1ll1111ll1_opy_ = feature_name + bstack11lllll_opy_ (u"ࠬࠦ࠭ࠡࠩా") + context.scenario.name
          bstack111lll11ll_opy_.execute_script(bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫి") + json.dumps(bstack1ll1111ll1_opy_) + bstack11lllll_opy_ (u"ࠧࡾࡿࠪీ"))
    except Exception as e:
      logger.debug(bstack11lllll_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡹ࡫ࡰ࠻ࠢࡾࢁࠬు").format(str(e)))
@measure(event_name=EVENTS.bstack1ll1l1l11l_opy_, stage=STAGE.bstack1llll11111_opy_, hook_type=bstack11lllll_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࡔࡶࡨࡴࠧూ"), bstack11lll11111_opy_=bstack11l1l1ll1l_opy_)
def bstack11ll1l111l_opy_(runner, name, context, bstack1ll1l1ll1l_opy_, *args):
  bstack1lllllll1_opy_.bstack1111111l1_opy_(args[0])
  try:
    step_status = args[0].status.name
    bstack111lll11ll_opy_ = threading.current_thread().bstackSessionDriver if bstack11lllll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩృ") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack111lll11ll_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack11lllll_opy_ (u"ࠫ࡮ࡴࡳࡵࡧࡳࠫౄ")
        feature_name = bstack1ll1111ll1_opy_ = str(runner.feature.name)
        bstack1ll1111ll1_opy_ = feature_name + bstack11lllll_opy_ (u"ࠬࠦ࠭ࠡࠩ౅") + context.scenario.name
        bstack111lll11ll_opy_.execute_script(bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫె") + json.dumps(bstack1ll1111ll1_opy_) + bstack11lllll_opy_ (u"ࠧࡾࡿࠪే"))
    if str(step_status).lower() in [bstack11lllll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨై"), bstack11lllll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ౉")]:
      bstack11l11lll1l_opy_ = bstack11lllll_opy_ (u"ࠪࠫొ")
      bstack1ll1ll1lll_opy_ = bstack11lllll_opy_ (u"ࠫࠬో")
      bstack1l11l1l1l1_opy_ = bstack11lllll_opy_ (u"ࠬ࠭ౌ")
      try:
        import traceback
        bstack11l11lll1l_opy_ = runner.exception.__class__.__name__
        bstack111l11ll1l_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1ll1ll1lll_opy_ = bstack11lllll_opy_ (u"࠭ࠠࠨ్").join(bstack111l11ll1l_opy_)
        bstack1l11l1l1l1_opy_ = bstack111l11ll1l_opy_[-1]
      except Exception as e:
        logger.debug(bstack11ll1lllll_opy_.format(str(e)))
      bstack11l11lll1l_opy_ += bstack1l11l1l1l1_opy_
      bstack1l1111l1l1_opy_(context, json.dumps(str(args[0].name) + bstack11lllll_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨ౎") + str(bstack1ll1ll1lll_opy_)),
                          bstack11lllll_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢ౏"))
      if runner.driver_initialised == bstack11lllll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢ౐"):
        bstack1ll11lll1_opy_(getattr(context, bstack11lllll_opy_ (u"ࠪࡴࡦ࡭ࡥࠨ౑"), None), bstack11lllll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ౒"), bstack11l11lll1l_opy_)
        bstack111lll11ll_opy_.execute_script(bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ౓") + json.dumps(str(args[0].name) + bstack11lllll_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧ౔") + str(bstack1ll1ll1lll_opy_)) + bstack11lllll_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦࢂࢃౕࠧ"))
      if runner.driver_initialised == bstack11lllll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨౖ"):
        bstack11l1l111l_opy_(bstack111lll11ll_opy_, bstack11lllll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ౗"), bstack11lllll_opy_ (u"ࠥࡗࡨ࡫࡮ࡢࡴ࡬ࡳࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢౘ") + str(bstack11l11lll1l_opy_))
    else:
      bstack1l1111l1l1_opy_(context, bstack11lllll_opy_ (u"ࠦࡕࡧࡳࡴࡧࡧࠥࠧౙ"), bstack11lllll_opy_ (u"ࠧ࡯࡮ࡧࡱࠥౚ"))
      if runner.driver_initialised == bstack11lllll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦ౛"):
        bstack1ll11lll1_opy_(getattr(context, bstack11lllll_opy_ (u"ࠧࡱࡣࡪࡩࠬ౜"), None), bstack11lllll_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣౝ"))
      bstack111lll11ll_opy_.execute_script(bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ౞") + json.dumps(str(args[0].name) + bstack11lllll_opy_ (u"ࠥࠤ࠲ࠦࡐࡢࡵࡶࡩࡩࠧࠢ౟")) + bstack11lllll_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢࡾࡿࠪౠ"))
      if runner.driver_initialised == bstack11lllll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥౡ"):
        bstack11l1l111l_opy_(bstack111lll11ll_opy_, bstack11lllll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨౢ"))
  except Exception as e:
    logger.debug(bstack11lllll_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤࡸࡺࡥࡱ࠼ࠣࡿࢂ࠭ౣ").format(str(e)))
  bstack11ll1111ll_opy_(runner, name, context, args[0], bstack1ll1l1ll1l_opy_, *args)
@measure(event_name=EVENTS.bstack1l11l11l_opy_, stage=STAGE.bstack1llll11111_opy_, bstack11lll11111_opy_=bstack11l1l1ll1l_opy_)
def bstack1lll11ll11_opy_(runner, name, context, bstack1ll1l1ll1l_opy_, *args):
  bstack1lllllll1_opy_.end_test(args[0])
  try:
    bstack1l1l11l1_opy_ = args[0].status.name
    bstack111lll11ll_opy_ = bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ౤"), context.browser)
    bstack11l11l1l1_opy_.bstack1l1l11l1l_opy_(bstack111lll11ll_opy_)
    if str(bstack1l1l11l1_opy_).lower() in [bstack11lllll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ౥"), bstack11lllll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ౦")]:
      bstack11l11lll1l_opy_ = bstack11lllll_opy_ (u"ࠫࠬ౧")
      bstack1ll1ll1lll_opy_ = bstack11lllll_opy_ (u"ࠬ࠭౨")
      bstack1l11l1l1l1_opy_ = bstack11lllll_opy_ (u"࠭ࠧ౩")
      try:
        import traceback
        bstack11l11lll1l_opy_ = runner.exception.__class__.__name__
        bstack111l11ll1l_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1ll1ll1lll_opy_ = bstack11lllll_opy_ (u"ࠧࠡࠩ౪").join(bstack111l11ll1l_opy_)
        bstack1l11l1l1l1_opy_ = bstack111l11ll1l_opy_[-1]
      except Exception as e:
        logger.debug(bstack11ll1lllll_opy_.format(str(e)))
      bstack11l11lll1l_opy_ += bstack1l11l1l1l1_opy_
      bstack1l1111l1l1_opy_(context, json.dumps(str(args[0].name) + bstack11lllll_opy_ (u"ࠣࠢ࠰ࠤࡋࡧࡩ࡭ࡧࡧࠥࡡࡴࠢ౫") + str(bstack1ll1ll1lll_opy_)),
                          bstack11lllll_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣ౬"))
      if runner.driver_initialised == bstack11lllll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧ౭") or runner.driver_initialised == bstack11lllll_opy_ (u"ࠫ࡮ࡴࡳࡵࡧࡳࠫ౮"):
        bstack1ll11lll1_opy_(getattr(context, bstack11lllll_opy_ (u"ࠬࡶࡡࡨࡧࠪ౯"), None), bstack11lllll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ౰"), bstack11l11lll1l_opy_)
        bstack111lll11ll_opy_.execute_script(bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ౱") + json.dumps(str(args[0].name) + bstack11lllll_opy_ (u"ࠣࠢ࠰ࠤࡋࡧࡩ࡭ࡧࡧࠥࡡࡴࠢ౲") + str(bstack1ll1ll1lll_opy_)) + bstack11lllll_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࡽࡾࠩ౳"))
      if runner.driver_initialised == bstack11lllll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧ౴") or runner.driver_initialised == bstack11lllll_opy_ (u"ࠫ࡮ࡴࡳࡵࡧࡳࠫ౵"):
        bstack11l1l111l_opy_(bstack111lll11ll_opy_, bstack11lllll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ౶"), bstack11lllll_opy_ (u"ࠨࡓࡤࡧࡱࡥࡷ࡯࡯ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥ౷") + str(bstack11l11lll1l_opy_))
    else:
      bstack1l1111l1l1_opy_(context, bstack11lllll_opy_ (u"ࠢࡑࡣࡶࡷࡪࡪࠡࠣ౸"), bstack11lllll_opy_ (u"ࠣ࡫ࡱࡪࡴࠨ౹"))
      if runner.driver_initialised == bstack11lllll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦ౺") or runner.driver_initialised == bstack11lllll_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪ౻"):
        bstack1ll11lll1_opy_(getattr(context, bstack11lllll_opy_ (u"ࠫࡵࡧࡧࡦࠩ౼"), None), bstack11lllll_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ౽"))
      bstack111lll11ll_opy_.execute_script(bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ౾") + json.dumps(str(args[0].name) + bstack11lllll_opy_ (u"ࠢࠡ࠯ࠣࡔࡦࡹࡳࡦࡦࠤࠦ౿")) + bstack11lllll_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦࢂࢃࠧಀ"))
      if runner.driver_initialised == bstack11lllll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦಁ") or runner.driver_initialised == bstack11lllll_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪಂ"):
        bstack11l1l111l_opy_(bstack111lll11ll_opy_, bstack11lllll_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦಃ"))
  except Exception as e:
    logger.debug(bstack11lllll_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧ಄").format(str(e)))
  bstack11ll1111ll_opy_(runner, name, context, context.scenario, bstack1ll1l1ll1l_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack1l11ll1l_opy_(runner, name, context, bstack1ll1l1ll1l_opy_, *args):
    target = context.scenario if hasattr(context, bstack11lllll_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨಅ")) else context.feature
    bstack11ll1111ll_opy_(runner, name, context, target, bstack1ll1l1ll1l_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack1l1ll1l111_opy_(runner, name, context, bstack1ll1l1ll1l_opy_, *args):
    try:
      bstack111lll11ll_opy_ = bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ಆ"), context.browser)
      bstack11l1lll1_opy_ = bstack11lllll_opy_ (u"ࠨࠩಇ")
      if context.failed is True:
        bstack11lll1l1l_opy_ = []
        bstack111lll1l_opy_ = []
        bstack111l1lll1l_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack11lll1l1l_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack111l11ll1l_opy_ = traceback.format_tb(exc_tb)
            bstack1111l1l1_opy_ = bstack11lllll_opy_ (u"ࠩࠣࠫಈ").join(bstack111l11ll1l_opy_)
            bstack111lll1l_opy_.append(bstack1111l1l1_opy_)
            bstack111l1lll1l_opy_.append(bstack111l11ll1l_opy_[-1])
        except Exception as e:
          logger.debug(bstack11ll1lllll_opy_.format(str(e)))
        bstack11l11lll1l_opy_ = bstack11lllll_opy_ (u"ࠪࠫಉ")
        for i in range(len(bstack11lll1l1l_opy_)):
          bstack11l11lll1l_opy_ += bstack11lll1l1l_opy_[i] + bstack111l1lll1l_opy_[i] + bstack11lllll_opy_ (u"ࠫࡡࡴࠧಊ")
        bstack11l1lll1_opy_ = bstack11lllll_opy_ (u"ࠬࠦࠧಋ").join(bstack111lll1l_opy_)
        if runner.driver_initialised in [bstack11lllll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠢಌ"), bstack11lllll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦ಍")]:
          bstack1l1111l1l1_opy_(context, bstack11l1lll1_opy_, bstack11lllll_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢಎ"))
          bstack1ll11lll1_opy_(getattr(context, bstack11lllll_opy_ (u"ࠩࡳࡥ࡬࡫ࠧಏ"), None), bstack11lllll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥಐ"), bstack11l11lll1l_opy_)
          bstack111lll11ll_opy_.execute_script(bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ಑") + json.dumps(bstack11l1lll1_opy_) + bstack11lllll_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥࡩࡷࡸ࡯ࡳࠤࢀࢁࠬಒ"))
          bstack11l1l111l_opy_(bstack111lll11ll_opy_, bstack11lllll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨಓ"), bstack11lllll_opy_ (u"ࠢࡔࡱࡰࡩࠥࡹࡣࡦࡰࡤࡶ࡮ࡵࡳࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢ࡟ࡲࠧಔ") + str(bstack11l11lll1l_opy_))
          bstack11l111ll1l_opy_ = bstack1lll1l1l1_opy_(bstack11l1lll1_opy_, runner.feature.name, logger)
          if (bstack11l111ll1l_opy_ != None):
            bstack1l11llll1l_opy_.append(bstack11l111ll1l_opy_)
      else:
        if runner.driver_initialised in [bstack11lllll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠤಕ"), bstack11lllll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨಖ")]:
          bstack1l1111l1l1_opy_(context, bstack11lllll_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨ࠾ࠥࠨಗ") + str(runner.feature.name) + bstack11lllll_opy_ (u"ࠦࠥࡶࡡࡴࡵࡨࡨࠦࠨಘ"), bstack11lllll_opy_ (u"ࠧ࡯࡮ࡧࡱࠥಙ"))
          bstack1ll11lll1_opy_(getattr(context, bstack11lllll_opy_ (u"࠭ࡰࡢࡩࡨࠫಚ"), None), bstack11lllll_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢಛ"))
          bstack111lll11ll_opy_.execute_script(bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ಜ") + json.dumps(bstack11lllll_opy_ (u"ࠤࡉࡩࡦࡺࡵࡳࡧ࠽ࠤࠧಝ") + str(runner.feature.name) + bstack11lllll_opy_ (u"ࠥࠤࡵࡧࡳࡴࡧࡧࠥࠧಞ")) + bstack11lllll_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢࡾࡿࠪಟ"))
          bstack11l1l111l_opy_(bstack111lll11ll_opy_, bstack11lllll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬಠ"))
          bstack11l111ll1l_opy_ = bstack1lll1l1l1_opy_(bstack11l1lll1_opy_, runner.feature.name, logger)
          if (bstack11l111ll1l_opy_ != None):
            bstack1l11llll1l_opy_.append(bstack11l111ll1l_opy_)
    except Exception as e:
      logger.debug(bstack11lllll_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨಡ").format(str(e)))
    bstack11ll1111ll_opy_(runner, name, context, context.feature, bstack1ll1l1ll1l_opy_, *args)
@measure(event_name=EVENTS.bstack1ll1l1l11l_opy_, stage=STAGE.bstack1llll11111_opy_, hook_type=bstack11lllll_opy_ (u"ࠢࡢࡨࡷࡩࡷࡇ࡬࡭ࠤಢ"), bstack11lll11111_opy_=bstack11l1l1ll1l_opy_)
def bstack11ll11111l_opy_(runner, name, context, bstack1ll1l1ll1l_opy_, *args):
    bstack11ll1111ll_opy_(runner, name, context, runner, bstack1ll1l1ll1l_opy_, *args)
def bstack1l1l11111_opy_(self, filename=None):
  bstack11lllll_opy_ (u"ࠣࠤࠥࠎࠥࠦࡌࡰࡣࡧࠤ࡭ࡵ࡯࡬ࡵࠣࡥࡳࡪࠠࡦࡰࡶࡹࡷ࡫ࠠࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰ࠱ࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠣࡥࡷ࡫ࠠࡳࡧࡪ࡭ࡸࡺࡥࡳࡧࡧ࠲ࠏࠦࠠࡃࡧ࡫ࡥࡻ࡫ࠠࡷ࠳࠱࠷࠰ࠦࡤࡰࡧࡶࡲࠬࡺࠠࡤࡣ࡯ࡰࠥࡸࡵ࡯ࠢ࡫ࡳࡴࡱࡳࠡࡶ࡫ࡥࡹࠦࡡࡳࡧࡱࠫࡹࠦࡤࡦࡨ࡬ࡲࡪࡪࠬࠡࡵࡲࠤࡼ࡫ࠠ࡮ࡷࡶࡸࠏࠦࠠࡥࡱࠣࡸ࡭࡯ࡳࠡࡧࡻࡴࡱ࡯ࡣࡪࡶ࡯ࡽࠥࡺ࡯ࠡ࡯ࡤ࡯ࡪࠦࡳࡶࡴࡨࠤࡼ࡫ࠧࡳࡧࠣࡧࡦࡲ࡬ࡦࡦࠣ࡭ࡳࠦࡡ࡯ࡻࠣࡧࡦࡹࡥ࠯ࠌࠣࠤࠧࠨࠢಣ")
  global bstack1ll1111ll_opy_
  bstack1ll1111ll_opy_(self, filename)
  bstack11lll11ll_opy_ = []
  bstack1111ll11l_opy_ = [bstack11lllll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠪತ"), bstack11lllll_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡸࡦ࡭ࠧಥ"), bstack11lllll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ದ"), bstack11lllll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ಧ"), bstack11lllll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡺࡡࡨࠩನ"), bstack11lllll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡦࡦࡣࡷࡹࡷ࡫ࠧ಩")]
  bstack11lll1l1ll_opy_ = lambda *_: None
  for hook_name in bstack1111ll11l_opy_:
    if hook_name not in self.hooks:
      self.hooks[hook_name] = bstack11lll1l1ll_opy_
      bstack11lll11ll_opy_.append(hook_name)
  if bstack11lll11ll_opy_:
    os.environ[bstack11lllll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡕࡇࡏࡤࡊࡅࡇࡃࡘࡐ࡙ࡥࡈࡐࡑࡎࡗࠬಪ")] = bstack11lllll_opy_ (u"ࠩ࠯ࠫಫ").join(bstack11lll11ll_opy_)
def bstack111l1l1ll1_opy_(self, name, *args):
  global bstack1ll1l1ll1l_opy_
  global bstack1ll1l1l111_opy_
  try:
    if bstack11ll1l1l11_opy_:
      platform_index = int(threading.current_thread()._name) % bstack111lllllll_opy_
      bstack1lllll1ll_opy_ = CONFIG[bstack11lllll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ಬ")][platform_index]
      os.environ[bstack11lllll_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬಭ")] = json.dumps(bstack1lllll1ll_opy_)
    if not hasattr(self, bstack11lllll_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡳࡦࡦࠪಮ")):
      self.driver_initialised = None
    bstack11llll1l1l_opy_ = {
        bstack11lllll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠪಯ"): bstack111l1l11l1_opy_,
        bstack11lllll_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠨರ"): bstack1l1ll1l11_opy_,
        bstack11lllll_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡶࡤ࡫ࠬಱ"): bstack1l111l1l11_opy_,
        bstack11lllll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫಲ"): bstack11llll1lll_opy_,
        bstack11lllll_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠨಳ"): bstack1lll11ll_opy_,
        bstack11lllll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡹ࡫ࡰࠨ಴"): bstack11ll1l111l_opy_,
        bstack11lllll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ವ"): bstack1lll11ll11_opy_,
        bstack11lllll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡺࡡࡨࠩಶ"): bstack1l11ll1l_opy_,
        bstack11lllll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡦࡦࡣࡷࡹࡷ࡫ࠧಷ"): bstack1l1ll1l111_opy_,
        bstack11lllll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠫಸ"): bstack11ll11111l_opy_
    }
    handler = bstack11llll1l1l_opy_.get(name, bstack1ll1l1ll1l_opy_)
    try:
      if args:
        context = args[0]
        remaining_args = args[1:]
        if bstack1ll1l1l111_opy_ is None or not bstack1ll1l1l111_opy_:
          context = self.context
          remaining_args = args
      else:
        context = self.context
        remaining_args = ()
      handler(self, name, context, bstack1ll1l1ll1l_opy_, *remaining_args)
    except Exception as e:
      logger.debug(bstack11lllll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡧ࡫ࡨࡢࡸࡨࠤ࡭ࡵ࡯࡬ࠢ࡫ࡥࡳࡪ࡬ࡦࡴࠣࡿࢂࡀࠠࡼࡿࠪಹ").format(name, str(e)))
    if name in [bstack11lllll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪ಺"), bstack11lllll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ಻"), bstack11lllll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠨ಼")]:
      try:
        bstack111lll11ll_opy_ = threading.current_thread().bstackSessionDriver if bstack1lllll11_opy_(bstack11lllll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬಽ")) else context.browser
        bstack1111l1l1l_opy_ = (
          (name == bstack11lllll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪಾ") and self.driver_initialised == bstack11lllll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧಿ")) or
          (name == bstack11lllll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠩೀ") and self.driver_initialised == bstack11lllll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦು")) or
          (name == bstack11lllll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬೂ") and self.driver_initialised in [bstack11lllll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢೃ"), bstack11lllll_opy_ (u"ࠨࡩ࡯ࡵࡷࡩࡵࠨೄ")]) or
          (name == bstack11lllll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡵࡧࡳࠫ೅") and self.driver_initialised == bstack11lllll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨೆ"))
        )
        if bstack1111l1l1l_opy_:
          self.driver_initialised = None
          if bstack111lll11ll_opy_ and hasattr(bstack111lll11ll_opy_, bstack11lllll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩ࠭ೇ")):
            try:
              bstack111lll11ll_opy_.quit()
            except Exception as e:
              logger.debug(bstack11lllll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡴࡹ࡮ࡺࡴࡪࡰࡪࠤࡩࡸࡩࡷࡧࡵࠤ࡮ࡴࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡩࡱࡲ࡯࠿ࠦࡻࡾࠩೈ").format(str(e)))
      except Exception as e:
        logger.debug(bstack11lllll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࠥ࡮࡯ࡰ࡭ࠣࡧࡱ࡫ࡡ࡯ࡷࡳࠤ࡫ࡵࡲࠡࡽࢀ࠾ࠥࢁࡽࠨ೉").format(name, str(e)))
  except Exception as e:
    logger.debug(bstack11lllll_opy_ (u"ࠬࡉࡲࡪࡶ࡬ࡧࡦࡲࠠࡦࡴࡵࡳࡷࠦࡩ࡯ࠢࡥࡩ࡭ࡧࡶࡦࠢࡵࡹࡳࠦࡨࡰࡱ࡮ࠤࢀࢃ࠺ࠡࡽࢀࠫೊ").format(name, str(e)))
    try:
      if bstack1ll1l1l111_opy_ is None or bstack1ll1l1l111_opy_:
        try:
          bstack1ll1l1ll1l_opy_(self, name, self.context, *args)
        except TypeError:
          bstack1ll1l1ll1l_opy_(self, name, *args)
      else:
        bstack1ll1l1ll1l_opy_(self, name, *args)
    except Exception as e2:
      logger.debug(bstack11lllll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡨࡤࡰࡱࡨࡡࡤ࡭ࠣࡳࡷ࡯ࡧࡪࡰࡤࡰࠥࡨࡥࡩࡣࡹࡩࠥ࡮࡯ࡰ࡭ࠣࡿࢂࡀࠠࡼࡿࠪೋ").format(name, str(e2)))
def bstack11ll1l11l_opy_(config, startdir):
  return bstack11lllll_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࠳ࢁࠧೌ").format(bstack11lllll_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱ್ࠢ"))
notset = Notset()
def bstack11ll11l1_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1ll1lll111_opy_
  if str(name).lower() == bstack11lllll_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࠩ೎"):
    return bstack11lllll_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤ೏")
  else:
    return bstack1ll1lll111_opy_(self, name, default, skip)
def bstack1lllll1l11_opy_(item, when):
  global bstack11l1ll1ll1_opy_
  try:
    bstack11l1ll1ll1_opy_(item, when)
  except Exception as e:
    pass
def bstack111l1111l_opy_():
  return
def bstack111l1ll111_opy_(type, name, status, reason, bstack1l1l111ll_opy_, bstack11l111ll_opy_):
  bstack11l1l11l_opy_ = {
    bstack11lllll_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫ೐"): type,
    bstack11lllll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ೑"): {}
  }
  if type == bstack11lllll_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨ೒"):
    bstack11l1l11l_opy_[bstack11lllll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ೓")][bstack11lllll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ೔")] = bstack1l1l111ll_opy_
    bstack11l1l11l_opy_[bstack11lllll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬೕ")][bstack11lllll_opy_ (u"ࠪࡨࡦࡺࡡࠨೖ")] = json.dumps(str(bstack11l111ll_opy_))
  if type == bstack11lllll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ೗"):
    bstack11l1l11l_opy_[bstack11lllll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ೘")][bstack11lllll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ೙")] = name
  if type == bstack11lllll_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪ೚"):
    bstack11l1l11l_opy_[bstack11lllll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ೛")][bstack11lllll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ೜")] = status
    if status == bstack11lllll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪೝ"):
      bstack11l1l11l_opy_[bstack11lllll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧೞ")][bstack11lllll_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ೟")] = json.dumps(str(reason))
  bstack11lll11l1l_opy_ = bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫೠ").format(json.dumps(bstack11l1l11l_opy_))
  return bstack11lll11l1l_opy_
def bstack11llll1l_opy_(driver_command, response):
    if driver_command == bstack11lllll_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫೡ"):
        bstack11lll1111l_opy_.bstack1l11l111ll_opy_({
            bstack11lllll_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧೢ"): response[bstack11lllll_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨೣ")],
            bstack11lllll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ೤"): bstack11lll1111l_opy_.current_test_uuid()
        })
def bstack1l1l11lll1_opy_(item, call, rep):
  global bstack11l1lll1ll_opy_
  global bstack1l11ll11ll_opy_
  global bstack1ll111l1l_opy_
  name = bstack11lllll_opy_ (u"ࠫࠬ೥")
  try:
    if rep.when == bstack11lllll_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ೦"):
      bstack1ll11lll1l_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1ll111l1l_opy_:
          name = str(rep.nodeid)
          bstack1lll1l11_opy_ = bstack111l1ll111_opy_(bstack11lllll_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ೧"), name, bstack11lllll_opy_ (u"ࠧࠨ೨"), bstack11lllll_opy_ (u"ࠨࠩ೩"), bstack11lllll_opy_ (u"ࠩࠪ೪"), bstack11lllll_opy_ (u"ࠪࠫ೫"))
          threading.current_thread().bstack11lll1lll_opy_ = name
          for driver in bstack1l11ll11ll_opy_:
            if bstack1ll11lll1l_opy_ == driver.session_id:
              driver.execute_script(bstack1lll1l11_opy_)
      except Exception as e:
        logger.debug(bstack11lllll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫ೬").format(str(e)))
      try:
        bstack1ll1lll11l_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack11lllll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭೭"):
          status = bstack11lllll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭೮") if rep.outcome.lower() == bstack11lllll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ೯") else bstack11lllll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ೰")
          reason = bstack11lllll_opy_ (u"ࠩࠪೱ")
          if status == bstack11lllll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪೲ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack11lllll_opy_ (u"ࠫ࡮ࡴࡦࡰࠩೳ") if status == bstack11lllll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ೴") else bstack11lllll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ೵")
          data = name + bstack11lllll_opy_ (u"ࠧࠡࡲࡤࡷࡸ࡫ࡤࠢࠩ೶") if status == bstack11lllll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ೷") else name + bstack11lllll_opy_ (u"ࠩࠣࡪࡦ࡯࡬ࡦࡦࠤࠤࠬ೸") + reason
          bstack11ll111111_opy_ = bstack111l1ll111_opy_(bstack11lllll_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬ೹"), bstack11lllll_opy_ (u"ࠫࠬ೺"), bstack11lllll_opy_ (u"ࠬ࠭೻"), bstack11lllll_opy_ (u"࠭ࠧ೼"), level, data)
          for driver in bstack1l11ll11ll_opy_:
            if bstack1ll11lll1l_opy_ == driver.session_id:
              driver.execute_script(bstack11ll111111_opy_)
      except Exception as e:
        logger.debug(bstack11lllll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡨࡵ࡮ࡵࡧࡻࡸࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫ೽").format(str(e)))
  except Exception as e:
    logger.debug(bstack11lllll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡸࡺࡡࡵࡧࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾࢁࠬ೾").format(str(e)))
  bstack11l1lll1ll_opy_(item, call, rep)
def bstack11l111ll1_opy_(driver, bstack1llll1lll_opy_, test=None):
  global bstack1l11111ll_opy_
  if test != None:
    bstack1l1lll11_opy_ = getattr(test, bstack11lllll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ೿"), None)
    bstack1l1llll11_opy_ = getattr(test, bstack11lllll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨഀ"), None)
    PercySDK.screenshot(driver, bstack1llll1lll_opy_, bstack1l1lll11_opy_=bstack1l1lll11_opy_, bstack1l1llll11_opy_=bstack1l1llll11_opy_, bstack11l111lll_opy_=bstack1l11111ll_opy_)
  else:
    PercySDK.screenshot(driver, bstack1llll1lll_opy_)
@measure(event_name=EVENTS.bstack111l1l11l_opy_, stage=STAGE.bstack1llll11111_opy_, bstack11lll11111_opy_=bstack11l1l1ll1l_opy_)
def bstack111lll1l1l_opy_(driver):
  if bstack1lll1llll1_opy_.bstack11l1l1l11_opy_() is True or bstack1lll1llll1_opy_.capturing() is True:
    return
  bstack1lll1llll1_opy_.bstack11l111l1_opy_()
  while not bstack1lll1llll1_opy_.bstack11l1l1l11_opy_():
    bstack11l11l11l1_opy_ = bstack1lll1llll1_opy_.bstack1l11llll11_opy_()
    bstack11l111ll1_opy_(driver, bstack11l11l11l1_opy_)
  bstack1lll1llll1_opy_.bstack1l1l1l11l_opy_()
def bstack11ll1ll1_opy_(sequence, driver_command, response = None, bstack111ll11ll1_opy_ = None, args = None):
    try:
      if sequence != bstack11lllll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫഁ"):
        return
      if percy.bstack11l1l1ll_opy_() == bstack11lllll_opy_ (u"ࠧ࡬ࡡ࡭ࡵࡨࠦം"):
        return
      bstack11l11l11l1_opy_ = bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"࠭ࡰࡦࡴࡦࡽࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩഃ"), None)
      for command in bstack11ll1ll1l_opy_:
        if command == driver_command:
          with bstack1l111ll111_opy_:
            bstack1llll1llll_opy_ = bstack1l11ll11ll_opy_.copy()
          for driver in bstack1llll1llll_opy_:
            bstack111lll1l1l_opy_(driver)
      bstack111l1ll1l1_opy_ = percy.bstack1l1111lll1_opy_()
      if driver_command in bstack111lll1ll1_opy_[bstack111l1ll1l1_opy_]:
        bstack1lll1llll1_opy_.bstack11l11lll1_opy_(bstack11l11l11l1_opy_, driver_command)
    except Exception as e:
      pass
def bstack1l11l1lll_opy_(framework_name):
  if bstack1l111111_opy_.get_property(bstack11lllll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟࡮ࡱࡧࡣࡨࡧ࡬࡭ࡧࡧࠫഄ")):
      return
  bstack1l111111_opy_.bstack1llll1ll1l_opy_(bstack11lllll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬഅ"), True)
  global bstack111ll1111_opy_
  global bstack11llll1ll1_opy_
  global bstack111l1lll1_opy_
  bstack111ll1111_opy_ = framework_name
  logger.info(bstack11l11ll1ll_opy_.format(bstack111ll1111_opy_.split(bstack11lllll_opy_ (u"ࠩ࠰ࠫആ"))[0]))
  bstack1l1111ll11_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack11ll1l1l11_opy_:
      Service.start = bstack11l1111l1l_opy_
      Service.stop = bstack111ll11l1l_opy_
      webdriver.Remote.get = bstack11l1llll1_opy_
      WebDriver.quit = bstack1l11lll1l_opy_
      webdriver.Remote.__init__ = bstack1l1111l11l_opy_
    if not bstack11ll1l1l11_opy_:
        webdriver.Remote.__init__ = bstack11llllll_opy_
    WebDriver.getAccessibilityResults = getAccessibilityResults
    WebDriver.get_accessibility_results = getAccessibilityResults
    WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
    WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
    WebDriver.performScan = perform_scan
    WebDriver.perform_scan = perform_scan
    WebDriver.execute = bstack11ll1lll_opy_
    bstack11llll1ll1_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack11ll1l1l11_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack11ll1llll_opy_
  except Exception as e:
    pass
  bstack1lll1l1ll1_opy_()
  if not bstack11llll1ll1_opy_:
    bstack11l111ll11_opy_(bstack11lllll_opy_ (u"ࠥࡔࡦࡩ࡫ࡢࡩࡨࡷࠥࡴ࡯ࡵࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠧഇ"), bstack1l1ll1111_opy_)
  if bstack11lllllll1_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      if hasattr(RemoteConnection, bstack11lllll_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬഈ")) and callable(getattr(RemoteConnection, bstack11lllll_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭ഉ"))):
        RemoteConnection._get_proxy_url = bstack1lllll111_opy_
      else:
        from selenium.webdriver.remote.client_config import ClientConfig
        ClientConfig.get_proxy_url = bstack1lllll111_opy_
    except Exception as e:
      logger.error(bstack1lllll11ll_opy_.format(str(e)))
  if bstack1ll1llll11_opy_():
    bstack11lll111l_opy_(CONFIG, logger)
  if (bstack11lllll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬഊ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if percy.bstack11l1l1ll_opy_() == bstack11lllll_opy_ (u"ࠢࡵࡴࡸࡩࠧഋ"):
          bstack1ll111111_opy_(bstack11ll1ll1_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack11ll11l1ll_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1l111l1ll_opy_
      except Exception as e:
        logger.warning(bstack11l11ll11_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1ll1lll1l_opy_
      except Exception as e:
        logger.debug(bstack1l11lll1l1_opy_ + str(e))
    except Exception as e:
      bstack11l111ll11_opy_(e, bstack11l11ll11_opy_)
    Output.start_test = bstack1l11l11lll_opy_
    Output.end_test = bstack1ll1l11lll_opy_
    TestStatus.__init__ = bstack11ll111l11_opy_
    QueueItem.__init__ = bstack1l11ll1ll_opy_
    pabot._create_items = bstack1ll11l11l1_opy_
    try:
      from pabot import __version__ as bstack1l11ll1l11_opy_
      if version.parse(bstack1l11ll1l11_opy_) >= version.parse(bstack11lllll_opy_ (u"ࠨ࠷࠱࠴࠳࠶ࠧഌ")):
        pabot._run = bstack1llllll1ll_opy_
      elif version.parse(bstack1l11ll1l11_opy_) >= version.parse(bstack11lllll_opy_ (u"ࠩ࠷࠲࠷࠴࠰ࠨ഍")):
        pabot._run = bstack1l1ll1ll1l_opy_
      elif version.parse(bstack1l11ll1l11_opy_) >= version.parse(bstack11lllll_opy_ (u"ࠪ࠶࠳࠷࠵࠯࠲ࠪഎ")):
        pabot._run = bstack1ll111ll1l_opy_
      elif version.parse(bstack1l11ll1l11_opy_) >= version.parse(bstack11lllll_opy_ (u"ࠫ࠷࠴࠱࠴࠰࠳ࠫഏ")):
        pabot._run = bstack111l11lll_opy_
      else:
        pabot._run = bstack111ll1l11_opy_
    except Exception as e:
      pabot._run = bstack111ll1l11_opy_
    pabot._create_command_for_execution = bstack1lll1l1111_opy_
    pabot._report_results = bstack1l111l1l1l_opy_
  if bstack11lllll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬഐ") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11l111ll11_opy_(e, bstack1l1111l1_opy_)
    Runner.run_hook = bstack111l1l1ll1_opy_
    try:
      from behave import __version__ as bstack1ll111lll_opy_
      if version.parse(bstack1ll111lll_opy_) >= version.parse(bstack11lllll_opy_ (u"࠭࠱࠯࠵࠱࠴ࠬ഑")):
        Runner.load_hooks = bstack1l1l11111_opy_
    except Exception as e:
      logger.debug(bstack11lllll_opy_ (u"ࠧࡄࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡢࡦࡪࡤࡺࡪࠦࡶࡦࡴࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫഒ").format(str(e)))
    Step.run = bstack111ll11l1_opy_
  if bstack11lllll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨഓ") in str(framework_name).lower():
    if not bstack11ll1l1l11_opy_:
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack11ll1l11l_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack111l1111l_opy_
      Config.getoption = bstack11ll11l1_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1l1l11lll1_opy_
    except Exception as e:
      pass
def bstack1ll11lllll_opy_():
  global CONFIG
  if bstack11lllll_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩഔ") in CONFIG and int(CONFIG[bstack11lllll_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪക")]) > 1:
    logger.warning(bstack111l11ll1_opy_)
def bstack1111lll1_opy_(arg, bstack1l1l1lllll_opy_, bstack1ll11l11_opy_=None):
  global CONFIG
  global bstack11l1ll111_opy_
  global bstack1l1lll1l1_opy_
  global bstack11ll1l1l11_opy_
  global bstack1l111111_opy_
  bstack1l1111ll1l_opy_ = bstack11lllll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫഖ")
  if bstack1l1l1lllll_opy_ and isinstance(bstack1l1l1lllll_opy_, str):
    bstack1l1l1lllll_opy_ = eval(bstack1l1l1lllll_opy_)
  CONFIG = bstack1l1l1lllll_opy_[bstack11lllll_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬഗ")]
  bstack11l1ll111_opy_ = bstack1l1l1lllll_opy_[bstack11lllll_opy_ (u"࠭ࡈࡖࡄࡢ࡙ࡗࡒࠧഘ")]
  bstack1l1lll1l1_opy_ = bstack1l1l1lllll_opy_[bstack11lllll_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩങ")]
  bstack11ll1l1l11_opy_ = bstack1l1l1lllll_opy_[bstack11lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫച")]
  bstack1l111111_opy_.bstack1llll1ll1l_opy_(bstack11lllll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪഛ"), bstack11ll1l1l11_opy_)
  os.environ[bstack11lllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬജ")] = bstack1l1111ll1l_opy_
  os.environ[bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠪഝ")] = json.dumps(CONFIG)
  os.environ[bstack11lllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡍ࡛ࡂࡠࡗࡕࡐࠬഞ")] = bstack11l1ll111_opy_
  os.environ[bstack11lllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧട")] = str(bstack1l1lll1l1_opy_)
  os.environ[bstack11lllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡍࡗࡊࡍࡓ࠭ഠ")] = str(True)
  if bstack111l111l1_opy_(arg, [bstack11lllll_opy_ (u"ࠨ࠯ࡱࠫഡ"), bstack11lllll_opy_ (u"ࠩ࠰࠱ࡳࡻ࡭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪഢ")]) != -1:
    os.environ[bstack11lllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡅࡗࡇࡌࡍࡇࡏࠫണ")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1lll1lll_opy_)
    return
  bstack111111lll_opy_()
  global bstack11l1l1lll_opy_
  global bstack1l11111ll_opy_
  global bstack1lll1ll11l_opy_
  global bstack1ll1l11ll1_opy_
  global bstack1l1lllll1l_opy_
  global bstack111l1lll1_opy_
  global bstack1lll1l1ll_opy_
  arg.append(bstack11lllll_opy_ (u"ࠦ࠲࡝ࠢത"))
  arg.append(bstack11lllll_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩ࠿ࡓ࡯ࡥࡷ࡯ࡩࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡩ࡮ࡲࡲࡶࡹ࡫ࡤ࠻ࡲࡼࡸࡪࡹࡴ࠯ࡒࡼࡸࡪࡹࡴࡘࡣࡵࡲ࡮ࡴࡧࠣഥ"))
  arg.append(bstack11lllll_opy_ (u"ࠨ࠭ࡘࠤദ"))
  arg.append(bstack11lllll_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫࠺ࡕࡪࡨࠤ࡭ࡵ࡯࡬࡫ࡰࡴࡱࠨധ"))
  global bstack1l1lll11l1_opy_
  global bstack1ll111l11_opy_
  global bstack1111l1lll_opy_
  global bstack1111ll111_opy_
  global bstack1111ll11_opy_
  global bstack111111ll_opy_
  global bstack1ll11ll111_opy_
  global bstack111llllll_opy_
  global bstack11l1l111l1_opy_
  global bstack111l1l1111_opy_
  global bstack1ll1lll111_opy_
  global bstack11l1ll1ll1_opy_
  global bstack11l1lll1ll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l1lll11l1_opy_ = webdriver.Remote.__init__
    bstack1ll111l11_opy_ = WebDriver.quit
    bstack111llllll_opy_ = WebDriver.close
    bstack11l1l111l1_opy_ = WebDriver.get
    bstack1111l1lll_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1ll11l111l_opy_(CONFIG) and bstack1ll1l111ll_opy_():
    if bstack111l1ll1l_opy_() < version.parse(bstack1ll11l1lll_opy_):
      logger.error(bstack1111ll1l_opy_.format(bstack111l1ll1l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack11lllll_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩന")) and callable(getattr(RemoteConnection, bstack11lllll_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪഩ"))):
          bstack111l1l1111_opy_ = RemoteConnection._get_proxy_url
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          bstack111l1l1111_opy_ = ClientConfig.get_proxy_url
      except Exception as e:
        logger.error(bstack1lllll11ll_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1ll1lll111_opy_ = Config.getoption
    from _pytest import runner
    bstack11l1ll1ll1_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warning(bstack11lllll_opy_ (u"ࠥࠩࡸࡀࠠࠦࡵࠥപ"), bstack1l111ll1_opy_, str(e))
  try:
    from pytest_bdd import reporting
    bstack11l1lll1ll_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack11lllll_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡳࠥࡸࡵ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࡷࠬഫ"))
  bstack1lll1ll11l_opy_ = CONFIG.get(bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩബ"), {}).get(bstack11lllll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨഭ"))
  bstack1lll1l1ll_opy_ = True
  if cli.is_enabled(CONFIG):
    if cli.bstack11llll11l_opy_():
      bstack11l1ll1l_opy_.invoke(bstack1lll11l1l_opy_.CONNECT, bstack1llllll111_opy_())
    platform_index = int(os.environ.get(bstack11lllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧമ"), bstack11lllll_opy_ (u"ࠨ࠲ࠪയ")))
  else:
    bstack1l11l1lll_opy_(bstack11llllll1_opy_)
  os.environ[bstack11lllll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪര")] = CONFIG[bstack11lllll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬറ")]
  os.environ[bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧല")] = CONFIG[bstack11lllll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨള")]
  os.environ[bstack11lllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩഴ")] = bstack11ll1l1l11_opy_.__str__()
  from _pytest.config import main as bstack1l111lllll_opy_
  bstack11l1l1l1l1_opy_ = []
  try:
    exit_code = bstack1l111lllll_opy_(arg)
    if cli.is_enabled(CONFIG):
      cli.bstack11l1l11111_opy_()
    if bstack11lllll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷࠫവ") in multiprocessing.current_process().__dict__.keys():
      for bstack1l1l1llll_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack11l1l1l1l1_opy_.append(bstack1l1l1llll_opy_)
    try:
      bstack11lllll1ll_opy_ = (bstack11l1l1l1l1_opy_, int(exit_code))
      bstack1ll11l11_opy_.append(bstack11lllll1ll_opy_)
    except:
      bstack1ll11l11_opy_.append((bstack11l1l1l1l1_opy_, exit_code))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack11l1l1l1l1_opy_.append({bstack11lllll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ശ"): bstack11lllll_opy_ (u"ࠩࡓࡶࡴࡩࡥࡴࡵࠣࠫഷ") + os.environ.get(bstack11lllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪസ")), bstack11lllll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪഹ"): traceback.format_exc(), bstack11lllll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫഺ"): int(os.environ.get(bstack11lllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝഻࠭")))})
    bstack1ll11l11_opy_.append((bstack11l1l1l1l1_opy_, 1))
def mod_behave_main(args, retries):
  try:
    from behave.configuration import Configuration
    from behave.__main__ import run_behave
    from browserstack_sdk.bstack_behave_runner import BehaveRunner
    config = Configuration(args)
    config.update_userdata({bstack11lllll_opy_ (u"ࠢࡳࡧࡷࡶ࡮࡫ࡳ഼ࠣ"): str(retries)})
    return run_behave(config, runner_class=BehaveRunner)
  except Exception as e:
    bstack11ll1l1l1_opy_ = e.__class__.__name__
    print(bstack11lllll_opy_ (u"ࠣࠧࡶ࠾ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡨࡥࡩࡣࡹࡩࠥࡺࡥࡴࡶࠣࠩࡸࠨഽ") % (bstack11ll1l1l1_opy_, e))
    return 1
def bstack1l11111111_opy_(arg):
  global bstack11ll111ll1_opy_
  bstack1l11l1lll_opy_(bstack1lll11111l_opy_)
  os.environ[bstack11lllll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪാ")] = str(bstack1l1lll1l1_opy_)
  retries = bstack11l1lll11_opy_.bstack1l1l1lll_opy_(CONFIG)
  status_code = 0
  if bstack11l1lll11_opy_.bstack111l111l_opy_(CONFIG):
    status_code = mod_behave_main(arg, retries)
  else:
    from behave.__main__ import main as bstack11l1ll1ll_opy_
    status_code = bstack11l1ll1ll_opy_(arg)
  if status_code != 0:
    bstack11ll111ll1_opy_ = status_code
def bstack1ll11l1ll1_opy_():
  logger.info(bstack1ll1l1l11_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack11lllll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩി"), help=bstack11lllll_opy_ (u"ࠫࡌ࡫࡮ࡦࡴࡤࡸࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡩ࡯࡯ࡨ࡬࡫ࠬീ"))
  parser.add_argument(bstack11lllll_opy_ (u"ࠬ࠳ࡵࠨു"), bstack11lllll_opy_ (u"࠭࠭࠮ࡷࡶࡩࡷࡴࡡ࡮ࡧࠪൂ"), help=bstack11lllll_opy_ (u"࡚ࠧࡱࡸࡶࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡺࡹࡥࡳࡰࡤࡱࡪ࠭ൃ"))
  parser.add_argument(bstack11lllll_opy_ (u"ࠨ࠯࡮ࠫൄ"), bstack11lllll_opy_ (u"ࠩ࠰࠱ࡰ࡫ࡹࠨ൅"), help=bstack11lllll_opy_ (u"ࠪ࡝ࡴࡻࡲࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡢࡥࡦࡩࡸࡹࠠ࡬ࡧࡼࠫെ"))
  parser.add_argument(bstack11lllll_opy_ (u"ࠫ࠲࡬ࠧേ"), bstack11lllll_opy_ (u"ࠬ࠳࠭ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪൈ"), help=bstack11lllll_opy_ (u"࡙࠭ࡰࡷࡵࠤࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ൉"))
  bstack11l11ll1l_opy_ = parser.parse_args()
  try:
    bstack111l11l1ll_opy_ = bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡧࡦࡰࡨࡶ࡮ࡩ࠮ࡺ࡯࡯࠲ࡸࡧ࡭ࡱ࡮ࡨࠫൊ")
    if bstack11l11ll1l_opy_.framework and bstack11l11ll1l_opy_.framework not in (bstack11lllll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨോ"), bstack11lllll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪൌ")):
      bstack111l11l1ll_opy_ = bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯࠳ࡿ࡭࡭࠰ࡶࡥࡲࡶ࡬ࡦ്ࠩ")
    bstack111ll1l1ll_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack111l11l1ll_opy_)
    bstack11l111l1ll_opy_ = open(bstack111ll1l1ll_opy_, bstack11lllll_opy_ (u"ࠫࡷ࠭ൎ"))
    bstack1l111l11_opy_ = bstack11l111l1ll_opy_.read()
    bstack11l111l1ll_opy_.close()
    if bstack11l11ll1l_opy_.username:
      bstack1l111l11_opy_ = bstack1l111l11_opy_.replace(bstack11lllll_opy_ (u"ࠬ࡟ࡏࡖࡔࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬ൏"), bstack11l11ll1l_opy_.username)
    if bstack11l11ll1l_opy_.key:
      bstack1l111l11_opy_ = bstack1l111l11_opy_.replace(bstack11lllll_opy_ (u"࡙࠭ࡐࡗࡕࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨ൐"), bstack11l11ll1l_opy_.key)
    if bstack11l11ll1l_opy_.framework:
      bstack1l111l11_opy_ = bstack1l111l11_opy_.replace(bstack11lllll_opy_ (u"࡚ࠧࡑࡘࡖࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ൑"), bstack11l11ll1l_opy_.framework)
    file_name = bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫ൒")
    file_path = os.path.abspath(file_name)
    bstack1lll11l111_opy_ = open(file_path, bstack11lllll_opy_ (u"ࠩࡺࠫ൓"))
    bstack1lll11l111_opy_.write(bstack1l111l11_opy_)
    bstack1lll11l111_opy_.close()
    logger.info(bstack11ll1l1ll1_opy_)
    try:
      os.environ[bstack11lllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬൔ")] = bstack11l11ll1l_opy_.framework if bstack11l11ll1l_opy_.framework != None else bstack11lllll_opy_ (u"ࠦࠧൕ")
      config = yaml.safe_load(bstack1l111l11_opy_)
      config[bstack11lllll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬൖ")] = bstack11lllll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡳࡦࡶࡸࡴࠬൗ")
      bstack1llll111ll_opy_(bstack1llll1l11l_opy_, config)
    except Exception as e:
      logger.debug(bstack111l1l11_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1ll1111l11_opy_.format(str(e)))
def bstack1llll111ll_opy_(bstack11l11l111l_opy_, config, bstack1l111l1l_opy_={}):
  global bstack11ll1l1l11_opy_
  global bstack11llllll11_opy_
  global bstack1l111111_opy_
  if not config:
    return
  bstack1l11l11111_opy_ = bstack11l11l1l11_opy_ if not bstack11ll1l1l11_opy_ else (
    bstack1lllll1lll_opy_ if bstack11lllll_opy_ (u"ࠧࡢࡲࡳࠫ൘") in config else (
        bstack111l11l1l_opy_ if config.get(bstack11lllll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ൙")) else bstack11ll111lll_opy_
    )
)
  bstack1llll1l1l1_opy_ = False
  bstack1l1l1l1ll_opy_ = False
  if bstack11ll1l1l11_opy_ is True:
      if bstack11lllll_opy_ (u"ࠩࡤࡴࡵ࠭൚") in config:
          bstack1llll1l1l1_opy_ = True
      else:
          bstack1l1l1l1ll_opy_ = True
  bstack1l1l111ll1_opy_ = bstack1llll1111_opy_.bstack1111l111_opy_(config, bstack11llllll11_opy_)
  bstack1lll11l1l1_opy_ = bstack1l1l1lll11_opy_()
  data = {
    bstack11lllll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ൛"): config[bstack11lllll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭൜")],
    bstack11lllll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ൝"): config[bstack11lllll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ൞")],
    bstack11lllll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫൟ"): bstack11l11l111l_opy_,
    bstack11lllll_opy_ (u"ࠨࡦࡨࡸࡪࡩࡴࡦࡦࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬൠ"): os.environ.get(bstack11lllll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫൡ"), bstack11llllll11_opy_),
    bstack11lllll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬൢ"): bstack11l1ll1l1_opy_,
    bstack11lllll_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠭ൣ"): bstack11l1ll1l11_opy_(),
    bstack11lllll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨ൤"): {
      bstack11lllll_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ൥"): str(config[bstack11lllll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ൦")]) if bstack11lllll_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ൧") in config else bstack11lllll_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࠥ൨"),
      bstack11lllll_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩ࡛࡫ࡲࡴ࡫ࡲࡲࠬ൩"): sys.version,
      bstack11lllll_opy_ (u"ࠫࡷ࡫ࡦࡦࡴࡵࡩࡷ࠭൪"): bstack1lll1ll1_opy_(os.environ.get(bstack11lllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ൫"), bstack11llllll11_opy_)),
      bstack11lllll_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨ൬"): bstack11lllll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ൭"),
      bstack11lllll_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩ൮"): bstack1l11l11111_opy_,
      bstack11lllll_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧ൯"): bstack1l1l111ll1_opy_,
      bstack11lllll_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡣࡺࡻࡩࡥࠩ൰"): os.environ[bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ൱")],
      bstack11lllll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ൲"): os.environ.get(bstack11lllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ൳"), bstack11llllll11_opy_),
      bstack11lllll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪ൴"): bstack1llllll11l_opy_(os.environ.get(bstack11lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪ൵"), bstack11llllll11_opy_)),
      bstack11lllll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ൶"): bstack1lll11l1l1_opy_.get(bstack11lllll_opy_ (u"ࠪࡲࡦࡳࡥࠨ൷")),
      bstack11lllll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪ൸"): bstack1lll11l1l1_opy_.get(bstack11lllll_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭൹")),
      bstack11lllll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩൺ"): config[bstack11lllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪൻ")] if config[bstack11lllll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫർ")] else bstack11lllll_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࠥൽ"),
      bstack11lllll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬൾ"): str(config[bstack11lllll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ൿ")]) if bstack11lllll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ඀") in config else bstack11lllll_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢඁ"),
      bstack11lllll_opy_ (u"ࠧࡰࡵࠪං"): sys.platform,
      bstack11lllll_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪඃ"): socket.gethostname(),
      bstack11lllll_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫ඄"): bstack1l111111_opy_.get_property(bstack11lllll_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࠬඅ"))
    }
  }
  if not bstack1l111111_opy_.get_property(bstack11lllll_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡘ࡯ࡧ࡯ࡣ࡯ࠫආ")) is None:
    data[bstack11lllll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨඇ")][bstack11lllll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡎࡧࡷࡥࡩࡧࡴࡢࠩඈ")] = {
      bstack11lllll_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧඉ"): bstack11lllll_opy_ (u"ࠨࡷࡶࡩࡷࡥ࡫ࡪ࡮࡯ࡩࡩ࠭ඊ"),
      bstack11lllll_opy_ (u"ࠩࡶ࡭࡬ࡴࡡ࡭ࠩඋ"): bstack1l111111_opy_.get_property(bstack11lllll_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪඌ")),
      bstack11lllll_opy_ (u"ࠫࡸ࡯ࡧ࡯ࡣ࡯ࡒࡺࡳࡢࡦࡴࠪඍ"): bstack1l111111_opy_.get_property(bstack11lllll_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱࡔ࡯ࠨඎ"))
    }
  if bstack11l11l111l_opy_ == bstack111lllll_opy_:
    data[bstack11lllll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩඏ")][bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡉ࡯࡯ࡨ࡬࡫ࠬඐ")] = bstack1l1lll1111_opy_(config)
    data[bstack11lllll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫඑ")][bstack11lllll_opy_ (u"ࠩ࡬ࡷࡕ࡫ࡲࡤࡻࡄࡹࡹࡵࡅ࡯ࡣࡥࡰࡪࡪࠧඒ")] = percy.bstack11llll1ll_opy_
    data[bstack11lllll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭ඓ")][bstack11lllll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡅࡹ࡮ࡲࡤࡊࡦࠪඔ")] = percy.percy_build_id
  if not bstack11l1lll11_opy_.bstack111ll1l11l_opy_(CONFIG):
    data[bstack11lllll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨඕ")][bstack11lllll_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠪඖ")] = bstack11l1lll11_opy_.bstack111ll1l11l_opy_(CONFIG)
  bstack1l1ll1l1l1_opy_ = bstack11ll1l11l1_opy_.bstack1llll1l111_opy_(CONFIG, logger)
  bstack1lll1111l1_opy_ = bstack11l1lll11_opy_.bstack1llll1l111_opy_(config=CONFIG)
  if bstack1l1ll1l1l1_opy_ is not None and bstack1lll1111l1_opy_ is not None and bstack1lll1111l1_opy_.bstack1l1ll11ll1_opy_():
    data[bstack11lllll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪ඗")][bstack1lll1111l1_opy_.bstack1l111l11l1_opy_()] = bstack1l1ll1l1l1_opy_.bstack11l1l1ll1_opy_()
  update(data[bstack11lllll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫ඘")], bstack1l111l1l_opy_)
  try:
    response = bstack111ll111_opy_(bstack11lllll_opy_ (u"ࠩࡓࡓࡘ࡚ࠧ඙"), bstack1l11l11ll_opy_(bstack1lll1111l_opy_), data, {
      bstack11lllll_opy_ (u"ࠪࡥࡺࡺࡨࠨක"): (config[bstack11lllll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ඛ")], config[bstack11lllll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨග")])
    })
    if response:
      logger.debug(bstack1l1l1l11ll_opy_.format(bstack11l11l111l_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack11llll1111_opy_.format(str(e)))
def bstack1lll1ll1_opy_(framework):
  return bstack11lllll_opy_ (u"ࠨࡻࡾ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࡼࡿࠥඝ").format(str(framework), __version__) if framework else bstack11lllll_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴ࢁࡽࠣඞ").format(
    __version__)
def bstack111111lll_opy_():
  global CONFIG
  global bstack1ll1ll1l11_opy_
  if bool(CONFIG):
    return
  try:
    bstack1l1llll1ll_opy_()
    logger.debug(bstack1l11llllll_opy_.format(str(CONFIG)))
    bstack1ll1ll1l11_opy_ = logger_utils.configure_logger(CONFIG, bstack1ll1ll1l11_opy_)
    bstack1l1111ll11_opy_()
  except Exception as e:
    logger.error(bstack11lllll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࡶࡲ࠯ࠤࡪࡸࡲࡰࡴ࠽ࠤࠧඟ") + str(e))
    sys.exit(1)
  sys.excepthook = bstack111l1ll11_opy_
  atexit.register(bstack1l1llll1_opy_)
  signal.signal(signal.SIGINT, bstack11lll1ll11_opy_)
  signal.signal(signal.SIGTERM, bstack11lll1ll11_opy_)
def bstack111l1ll11_opy_(exctype, value, traceback):
  global bstack1l11ll11ll_opy_
  try:
    for driver in bstack1l11ll11ll_opy_:
      bstack11l1l111l_opy_(driver, bstack11lllll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩච"), bstack11lllll_opy_ (u"ࠥࡗࡪࡹࡳࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨඡ") + str(value))
  except Exception:
    pass
  logger.info(bstack111l1lllll_opy_)
  bstack1lllll1l1_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1lllll1l1_opy_(message=bstack11lllll_opy_ (u"ࠫࠬජ"), bstack1ll1llll1l_opy_ = False):
  global CONFIG
  bstack111lll1l11_opy_ = bstack11lllll_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠧඣ") if bstack1ll1llll1l_opy_ else bstack11lllll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬඤ")
  bstack1ll11ll1l_opy_ = bstack1lll11l1ll_opy_.bstack1llll1l1ll_opy_(EVENTS.bstack1ll1l1lll_opy_)
  try:
    if message:
      bstack1l111l1l_opy_ = {
        bstack111lll1l11_opy_ : str(message)
      }
      try:
        bstack1llll111ll_opy_(bstack111lllll_opy_, CONFIG, bstack1l111l1l_opy_)
      finally:
        bstack1lll11l1ll_opy_.end(EVENTS.bstack1ll1l1lll_opy_.value, bstack1ll11ll1l_opy_ + bstack11lllll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢඥ"), bstack1ll11ll1l_opy_ + bstack11lllll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨඦ"), status=True, failure=None, test_name=None)
    else:
      try:
        bstack1llll111ll_opy_(bstack111lllll_opy_, CONFIG)
      finally:
        bstack1lll11l1ll_opy_.end(EVENTS.bstack1ll1l1lll_opy_.value, bstack1ll11ll1l_opy_ + bstack11lllll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤට"), bstack1ll11ll1l_opy_ + bstack11lllll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣඨ"), status=True, failure=None, test_name=None)
  except Exception as e:
    logger.debug(bstack11ll1l1lll_opy_.format(str(e)))
def bstack11l11l111_opy_(bstack111l11l111_opy_, size):
  bstack11l11llll_opy_ = []
  while len(bstack111l11l111_opy_) > size:
    bstack1ll11l111_opy_ = bstack111l11l111_opy_[:size]
    bstack11l11llll_opy_.append(bstack1ll11l111_opy_)
    bstack111l11l111_opy_ = bstack111l11l111_opy_[size:]
  bstack11l11llll_opy_.append(bstack111l11l111_opy_)
  return bstack11l11llll_opy_
def bstack111111ll1_opy_(args):
  if bstack11lllll_opy_ (u"ࠫ࠲ࡳࠧඩ") in args and bstack11lllll_opy_ (u"ࠬࡶࡤࡣࠩඪ") in args:
    return True
  return False
@measure(event_name=EVENTS.bstack11111111_opy_, stage=STAGE.bstack111111l1l_opy_)
def run_on_browserstack(bstack1ll11llll_opy_=None, bstack1ll11l11_opy_=None, bstack1l1ll11111_opy_=False):
  global CONFIG
  global bstack11l1ll111_opy_
  global bstack1l1lll1l1_opy_
  global bstack11llllll11_opy_
  global bstack1l111111_opy_
  bstack1l1111ll1l_opy_ = bstack11lllll_opy_ (u"࠭ࠧණ")
  bstack11l11l1l_opy_ = bstack11lllll_opy_ (u"ࠢࠣඬ")
  bstack1111lll11_opy_(bstack1ll1111111_opy_, logger)
  if bstack1ll11llll_opy_ and isinstance(bstack1ll11llll_opy_, str):
    bstack1ll11llll_opy_ = eval(bstack1ll11llll_opy_)
  if bstack1ll11llll_opy_:
    CONFIG = bstack1ll11llll_opy_[bstack11lllll_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨත")]
    bstack11l1ll111_opy_ = bstack1ll11llll_opy_[bstack11lllll_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪථ")]
    bstack1l1lll1l1_opy_ = bstack1ll11llll_opy_[bstack11lllll_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬද")]
    bstack1l111111_opy_.bstack1llll1ll1l_opy_(bstack11lllll_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ධ"), bstack1l1lll1l1_opy_)
    bstack1l1111ll1l_opy_ = bstack11lllll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬන")
  bstack1l111111_opy_.bstack1llll1ll1l_opy_(bstack11lllll_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨ඲"), uuid4().__str__())
  logger.info(bstack11lllll_opy_ (u"ࠧࡔࡆࡎࠤࡷࡻ࡮ࠡࡵࡷࡥࡷࡺࡥࡥࠢࡺ࡭ࡹ࡮ࠠࡪࡦ࠽ࠤࠬඳ") + bstack1l111111_opy_.get_property(bstack11lllll_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪප")));
  logger.debug(bstack11lllll_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࡁࠬඵ") + bstack1l111111_opy_.get_property(bstack11lllll_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࠬබ")))
  if not bstack1l1ll11111_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1lll1lll_opy_)
      return
    if sys.argv[1] == bstack11lllll_opy_ (u"ࠫ࠲࠳ࡶࡦࡴࡶ࡭ࡴࡴࠧභ") or sys.argv[1] == bstack11lllll_opy_ (u"ࠬ࠳ࡶࠨම"):
      logger.info(bstack11lllll_opy_ (u"࠭ࡂࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡖࡹࡵࡪࡲࡲ࡙ࠥࡄࡌࠢࡹࡿࢂ࠭ඹ").format(__version__))
      return
    if sys.argv[1] == bstack11lllll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ය"):
      bstack1ll11l1ll1_opy_()
      return
  args = sys.argv
  bstack111111lll_opy_()
  global bstack11l1l1lll_opy_
  global bstack111lllllll_opy_
  global bstack1lll1l1ll_opy_
  global bstack1llllllll_opy_
  global bstack1l11111ll_opy_
  global bstack1lll1ll11l_opy_
  global bstack1ll1l11ll1_opy_
  global bstack1l11l111l1_opy_
  global bstack1l1lllll1l_opy_
  global bstack111l1lll1_opy_
  global bstack1l11111l1_opy_
  bstack111lllllll_opy_ = len(CONFIG.get(bstack11lllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫර"), []))
  if not bstack1l1111ll1l_opy_:
    if args[1] == bstack11lllll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ඼") or args[1] == bstack11lllll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫල"):
      bstack1l1111ll1l_opy_ = bstack11lllll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ඾")
      args = args[2:]
    elif args[1] == bstack11lllll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ඿"):
      bstack1l1111ll1l_opy_ = bstack11lllll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬව")
      args = args[2:]
    elif args[1] == bstack11lllll_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ශ"):
      bstack1l1111ll1l_opy_ = bstack11lllll_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧෂ")
      args = args[2:]
    elif args[1] == bstack11lllll_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪස"):
      bstack1l1111ll1l_opy_ = bstack11lllll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫහ")
      args = args[2:]
    elif args[1] == bstack11lllll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫළ"):
      bstack1l1111ll1l_opy_ = bstack11lllll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬෆ")
      args = args[2:]
    elif args[1] == bstack11lllll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭෇"):
      bstack1l1111ll1l_opy_ = bstack11lllll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ෈")
      args = args[2:]
    else:
      if not bstack11lllll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ෉") in CONFIG or str(CONFIG[bstack11lllll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯්ࠬ")]).lower() in [bstack11lllll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ෋"), bstack11lllll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬ෌")]:
        bstack1l1111ll1l_opy_ = bstack11lllll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ෍")
        args = args[1:]
      elif str(CONFIG[bstack11lllll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ෎")]).lower() == bstack11lllll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ා"):
        bstack1l1111ll1l_opy_ = bstack11lllll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧැ")
        args = args[1:]
      elif str(CONFIG[bstack11lllll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬෑ")]).lower() == bstack11lllll_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩි"):
        bstack1l1111ll1l_opy_ = bstack11lllll_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪී")
        args = args[1:]
      elif str(CONFIG[bstack11lllll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨු")]).lower() == bstack11lllll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭෕"):
        bstack1l1111ll1l_opy_ = bstack11lllll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧූ")
        args = args[1:]
      elif str(CONFIG[bstack11lllll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ෗")]).lower() == bstack11lllll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩෘ"):
        bstack1l1111ll1l_opy_ = bstack11lllll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪෙ")
        args = args[1:]
      else:
        os.environ[bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ේ")] = bstack1l1111ll1l_opy_
        bstack11l1ll11l1_opy_(bstack1l11l1lll1_opy_)
  os.environ[bstack11lllll_opy_ (u"ࠬࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉ࠭ෛ")] = bstack1l1111ll1l_opy_
  bstack11llllll11_opy_ = bstack1l1111ll1l_opy_
  if cli.is_enabled(CONFIG):
    try:
      bstack11l11111l1_opy_ = bstack1l1l1l1l_opy_[bstack11lllll_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙࠳ࡂࡅࡆࠪො")] if bstack1l1111ll1l_opy_ == bstack11lllll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧෝ") and bstack11l111l111_opy_() else bstack1l1111ll1l_opy_
      bstack11l1ll1l_opy_.invoke(bstack1lll11l1l_opy_.bstack1l11ll11l1_opy_, bstack11l11l1111_opy_(
        sdk_version=__version__,
        path_config=bstack11lllllll_opy_(),
        path_project=os.getcwd(),
        test_framework=bstack11l11111l1_opy_,
        frameworks=[bstack11l11111l1_opy_],
        framework_versions={
          bstack11l11111l1_opy_: bstack1llllll11l_opy_(bstack11lllll_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧෞ") if bstack1l1111ll1l_opy_ in [bstack11lllll_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨෟ"), bstack11lllll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ෠"), bstack11lllll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ෡")] else bstack1l1111ll1l_opy_)
        },
        bs_config=CONFIG
      ))
      if cli.config.get(bstack11lllll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠢ෢"), None):
        CONFIG[bstack11lllll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣ෣")] = cli.config.get(bstack11lllll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤ෤"), None)
    except Exception as e:
      bstack11l1ll1l_opy_.invoke(bstack1lll11l1l_opy_.bstack11ll1111_opy_, e.__traceback__, 1)
    if bstack1l1lll1l1_opy_:
      CONFIG[bstack11lllll_opy_ (u"ࠣࡣࡳࡴࠧ෥")] = cli.config[bstack11lllll_opy_ (u"ࠤࡤࡴࡵࠨ෦")]
      logger.info(bstack1l1lllll1_opy_.format(CONFIG[bstack11lllll_opy_ (u"ࠪࡥࡵࡶࠧ෧")]))
  else:
    bstack11l1ll1l_opy_.clear()
  global bstack11l11lll_opy_
  global bstack1l111111ll_opy_
  if bstack1ll11llll_opy_:
    try:
      bstack1l1111l111_opy_ = datetime.datetime.now()
      os.environ[bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭෨")] = bstack1l1111ll1l_opy_
      bstack1ll1ll1l_opy_ = bstack1lll11l1ll_opy_.bstack1llll1l1ll_opy_(EVENTS.bstack1llll1ll1_opy_)
      try:
        logger.info(bstack11lllll_opy_ (u"࡙ࠧࡥ࡯ࡦ࡬ࡲ࡬ࠦࡓࡅࡍࠣࡘࡪࡹࡴࠡࡃࡷࡸࡪࡳࡰࡵࡧࡧࠤࡪࡼࡥ࡯ࡶࠥ෩"))
        bstack1llll111ll_opy_(bstack111lll1ll_opy_, CONFIG)
      finally:
        bstack1lll11l1ll_opy_.end(EVENTS.bstack1llll1ll1_opy_.value, bstack1ll1ll1l_opy_ + bstack11lllll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ෪"), bstack1ll1ll1l_opy_ + bstack11lllll_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ෫"), status=True, failure=None, test_name=None)
      cli.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠣࡪࡷࡸࡵࡀࡳࡥ࡭ࡢࡸࡪࡹࡴࡠࡣࡷࡸࡪࡳࡰࡵࡧࡧࠦ෬"), datetime.datetime.now() - bstack1l1111l111_opy_)
    except Exception as e:
      logger.debug(bstack1l111l1111_opy_.format(str(e)))
  global bstack1l1lll11l1_opy_
  global bstack1ll111l11_opy_
  global bstack1l1ll111ll_opy_
  global bstack1l1l111l_opy_
  global bstack11ll1l1ll_opy_
  global bstack111l11ll_opy_
  global bstack1111ll111_opy_
  global bstack1111ll11_opy_
  global bstack11ll1ll1ll_opy_
  global bstack111111ll_opy_
  global bstack1ll11ll111_opy_
  global bstack111llllll_opy_
  global bstack1ll1l1ll1l_opy_
  global bstack1ll1111ll_opy_
  global bstack11l111lll1_opy_
  global bstack11l1l111l1_opy_
  global bstack111l1l1111_opy_
  global bstack1ll1lll111_opy_
  global bstack11l1ll1ll1_opy_
  global bstack111llll1ll_opy_
  global bstack11l1lll1ll_opy_
  global bstack1111l1lll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l1lll11l1_opy_ = webdriver.Remote.__init__
    bstack1ll111l11_opy_ = WebDriver.quit
    bstack111llllll_opy_ = WebDriver.close
    bstack11l1l111l1_opy_ = WebDriver.get
    bstack1111l1lll_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack11l11lll_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack1ll11ll11_opy_
    bstack1l111111ll_opy_ = bstack1ll11ll11_opy_()
  except Exception as e:
    pass
  try:
    global bstack11lllll1_opy_
    from QWeb.keywords import browser
    bstack11lllll1_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1ll11l111l_opy_(CONFIG) and bstack1ll1l111ll_opy_():
    if bstack111l1ll1l_opy_() < version.parse(bstack1ll11l1lll_opy_):
      logger.error(bstack1111ll1l_opy_.format(bstack111l1ll1l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack11lllll_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪ෭")) and callable(getattr(RemoteConnection, bstack11lllll_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫ෮"))):
          RemoteConnection._get_proxy_url = bstack1lllll111_opy_
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          ClientConfig.get_proxy_url = bstack1lllll111_opy_
      except Exception as e:
        logger.error(bstack1lllll11ll_opy_.format(str(e)))
  if not CONFIG.get(bstack11lllll_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭෯"), False) and not bstack1ll11llll_opy_:
    logger.info(bstack11lll11l_opy_)
  bstack111ll1lll_opy_ = not cli.is_enabled(CONFIG) and bstack1l1111ll1l_opy_ not in [bstack11lllll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭෰")]
  bstack1ll1ll1111_opy_ = bstack111ll1lll_opy_ and bstack11lllll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ෱") in CONFIG and str(CONFIG[bstack11lllll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫෲ")]).lower() != bstack11lllll_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧෳ")
  bstack1l1lll1lll_opy_ = bstack111ll1lll_opy_ and not bstack1ll1ll1111_opy_ and (bstack1l1111ll1l_opy_ != bstack11lllll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ෴") or (bstack1l1111ll1l_opy_ == bstack11lllll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ෵") and not bstack1ll11llll_opy_))
  if bstack1l1111ll1l_opy_ not in [bstack11lllll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ෶")]:
    bstack1111lll11_opy_(os.path.join(os.getcwd(), bstack11lllll_opy_ (u"ࠬࡲ࡯ࡨࠩ෷"), bstack11lllll_opy_ (u"࠭࡫ࡦࡻ࠰ࡱࡪࡺࡲࡪࡥࡶ࠲࡯ࡹ࡯࡯ࠩ෸")), logger)
  if (bstack1l1111ll1l_opy_ in [bstack11lllll_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭෹"), bstack11lllll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ෺"), bstack11lllll_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ෻")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack11ll11l1ll_opy_
        bstack111l11ll_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warning(bstack11l11ll11_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack11ll1l1ll_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1l11lll1l1_opy_ + str(e))
    except Exception as e:
      bstack11l111ll11_opy_(e, bstack11l11ll11_opy_)
    if bstack1l1111ll1l_opy_ != bstack11lllll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ෼"):
      bstack1ll1llll_opy_()
    bstack1l1ll111ll_opy_ = Output.start_test
    bstack1l1l111l_opy_ = Output.end_test
    bstack1111ll111_opy_ = TestStatus.__init__
    bstack11ll1ll1ll_opy_ = pabot._run
    bstack111111ll_opy_ = QueueItem.__init__
    bstack1ll11ll111_opy_ = pabot._create_command_for_execution
    bstack111llll1ll_opy_ = pabot._report_results
  if bstack1l1111ll1l_opy_ == bstack11lllll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ෽"):
    global bstack1ll1l1l111_opy_
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11l111ll11_opy_(e, bstack1l1111l1_opy_)
    bstack1ll1l1ll1l_opy_ = Runner.run_hook
    bstack1ll1111ll_opy_ = Runner.load_hooks
    bstack11l111lll1_opy_ = Step.run
    try:
      sig = inspect.signature(bstack1ll1l1ll1l_opy_)
      params = list(sig.parameters.keys())
      bstack1ll1l1l111_opy_ = bstack11lllll_opy_ (u"ࠬࡩ࡯࡯ࡶࡨࡼࡹ࠭෾") in params
      logger.info(bstack11lllll_opy_ (u"࠭ࡄࡦࡶࡨࡧࡹ࡫ࡤࠡࡤࡨ࡬ࡦࡼࡥࠡࡴࡸࡲࡤ࡮࡯ࡰ࡭ࠣࡷ࡮࡭࡮ࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪ෿").format(bstack11lllll_opy_ (u"ࠧ࠲࠰࠵࠲࠻ࠦࠨࡸ࡫ࡷ࡬ࠥࡩ࡯࡯ࡶࡨࡼࡹ࠯ࠧ฀") if bstack1ll1l1l111_opy_ else bstack11lllll_opy_ (u"ࠨ࠳࠱࠷࠰ࠦࠨࡸ࡫ࡷ࡬ࡴࡻࡴࠡࡥࡲࡲࡹ࡫ࡸࡵࠫࠪก")))
    except Exception as e:
      logger.debug(bstack11lllll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡦࡸࠥࡨࡥࡩࡣࡹࡩࠥࡸࡵ࡯ࡡ࡫ࡳࡴࡱࠠࡴ࡫ࡪࡲࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧข").format(str(e)))
      bstack1ll1l1l111_opy_ = None
  if bstack1l1111ll1l_opy_ == bstack11lllll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪฃ"):
    try:
      from _pytest.config import Config
      bstack1ll1lll111_opy_ = Config.getoption
      from _pytest import runner
      bstack11l1ll1ll1_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warning(bstack11lllll_opy_ (u"ࠦࠪࡹ࠺ࠡࠧࡶࠦค"), bstack1l111ll1_opy_, str(e))
    try:
      from pytest_bdd import reporting
      bstack11l1lll1ll_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack11lllll_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡴࠦࡲࡶࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࡸ࠭ฅ"))
    if bstack1l1l1l1111_opy_():
      logger.warning(bstack1llllll1l_opy_[bstack11lllll_opy_ (u"࠭ࡓࡅࡍ࠰ࡋࡊࡔ࠭࠱࠲࠸ࠫฆ")])
  try:
    framework_name = bstack11lllll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ง") if bstack1l1111ll1l_opy_ in [bstack11lllll_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧจ"), bstack11lllll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨฉ"), bstack11lllll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫช")] else bstack1lll1ll1ll_opy_(bstack1l1111ll1l_opy_)
    bstack1l1l111111_opy_ = {
      bstack11lllll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࠬซ"): bstack11lllll_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧฌ") if bstack1l1111ll1l_opy_ == bstack11lllll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ญ") and bstack11l111l111_opy_() else framework_name,
      bstack11lllll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫฎ"): bstack1llllll11l_opy_(framework_name),
      bstack11lllll_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ฏ"): __version__,
      bstack11lllll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦࠪฐ"): bstack1l1111ll1l_opy_
    }
    if bstack1l1111ll1l_opy_ in bstack11lll11l1_opy_ + bstack1ll1l1l1l1_opy_:
      if bstack11l1llll11_opy_.bstack1lll1lll1l_opy_(CONFIG):
        if bstack11lllll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪฑ") in CONFIG:
          os.environ[bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬฒ")] = os.getenv(bstack11lllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ณ"), json.dumps(CONFIG[bstack11lllll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ด")]))
          CONFIG[bstack11lllll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧต")].pop(bstack11lllll_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ถ"), None)
          CONFIG[bstack11lllll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩท")].pop(bstack11lllll_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨธ"), None)
        bstack1l1l111111_opy_[bstack11lllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫน")] = {
          bstack11lllll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪบ"): bstack11lllll_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨป"),
          bstack11lllll_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨผ"): str(bstack111l1ll1l_opy_())
        }
    bstack11ll1ll111_opy_, bstack1l1ll11l1_opy_ = None, {}
    bstack11llllll1l_opy_ = None
    bstack11ll1l111_opy_ = None
    def bstack1l11llll_opy_():
      if bstack1ll1ll1111_opy_:
        bstack1lll1l111l_opy_()
      elif bstack1l1lll1lll_opy_:
        bstack1lllll1l1l_opy_()
    def bstack1lll111l1l_opy_():
      nonlocal bstack11ll1ll111_opy_, bstack1l1ll11l1_opy_
      if bstack1l1111ll1l_opy_ not in [bstack11lllll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩฝ")] and not cli.is_running():
        bstack11ll1ll111_opy_, bstack1l1ll11l1_opy_ = bstack11lll1111l_opy_.launch(CONFIG, bstack1l1l111111_opy_)
    if bstack1ll1ll1111_opy_ or bstack1l1lll1lll_opy_:
      bstack11llllll1l_opy_ = threading.Thread(target=bstack1l11llll_opy_)
      bstack11llllll1l_opy_.start()
    if bstack1l1111ll1l_opy_ not in [bstack11lllll_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪพ")] and not cli.is_running():
      bstack11ll1l111_opy_ = threading.Thread(target=bstack1lll111l1l_opy_)
      bstack11ll1l111_opy_.start()
    if bstack11llllll1l_opy_:
      bstack11llllll1l_opy_.join()
    if bstack11ll1l111_opy_:
      bstack11ll1l111_opy_.join()
    if bstack1l1ll11l1_opy_.get(bstack11lllll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪฟ")) is not None and bstack11l1llll11_opy_.bstack1lll1l11ll_opy_(CONFIG) is None:
      value = bstack1l1ll11l1_opy_[bstack11lllll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫภ")].get(bstack11lllll_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ม"))
      if value is not None:
          CONFIG[bstack11lllll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ย")] = value
      else:
        logger.debug(bstack11lllll_opy_ (u"ࠢࡏࡱࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡨࡦࡺࡡࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡶࡪࡹࡰࡰࡰࡶࡩࠧร"))
  except Exception as e:
    logger.debug(bstack11ll11llll_opy_.format(bstack11lllll_opy_ (u"ࠨࡖࡨࡷࡹࡎࡵࡣࠩฤ"), str(e)))
  if bstack1l1111ll1l_opy_ == bstack11lllll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩล"):
    bstack1lll1l1ll_opy_ = True
    if bstack1ll11llll_opy_ and bstack1l1ll11111_opy_:
      bstack1lll1ll11l_opy_ = CONFIG.get(bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧฦ"), {}).get(bstack11lllll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ว"))
      bstack1l11l1lll_opy_(bstack1lll11l11l_opy_)
    elif bstack1ll11llll_opy_:
      bstack1lll1ll11l_opy_ = CONFIG.get(bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩศ"), {}).get(bstack11lllll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨษ"))
      global bstack1l11ll11ll_opy_
      try:
        if bstack111111ll1_opy_(bstack1ll11llll_opy_[bstack11lllll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪส")]) and multiprocessing.current_process().name == bstack11lllll_opy_ (u"ࠨ࠲ࠪห"):
          bstack1ll11llll_opy_[bstack11lllll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬฬ")].remove(bstack11lllll_opy_ (u"ࠪ࠱ࡲ࠭อ"))
          bstack1ll11llll_opy_[bstack11lllll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧฮ")].remove(bstack11lllll_opy_ (u"ࠬࡶࡤࡣࠩฯ"))
          bstack1ll11llll_opy_[bstack11lllll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩะ")] = bstack1ll11llll_opy_[bstack11lllll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪั")][0]
          with open(bstack1ll11llll_opy_[bstack11lllll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫา")], bstack11lllll_opy_ (u"ࠩࡵࠫำ")) as f:
            bstack1111lllll_opy_ = f.read()
          bstack1l1lll1l1l_opy_ = bstack11lllll_opy_ (u"ࠥࠦࠧ࡬ࡲࡰ࡯ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡨࡰࠦࡩ࡮ࡲࡲࡶࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦ࠽ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪ࠮ࡻࡾࠫ࠾ࠤ࡫ࡸ࡯࡮ࠢࡳࡨࡧࠦࡩ࡮ࡲࡲࡶࡹࠦࡐࡥࡤ࠾ࠤࡴ࡭࡟ࡥࡤࠣࡁࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡦࡨࡪࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠩࡵࡨࡰ࡫࠲ࠠࡢࡴࡪ࠰ࠥࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠡ࠿ࠣ࠴࠮ࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺࡲࡺ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡥࡷ࡭ࠠ࠾ࠢࡶࡸࡷ࠮ࡩ࡯ࡶࠫࡥࡷ࡭ࠩࠬ࠳࠳࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡩࡽࡩࡥࡱࡶࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡡࡴࠢࡨ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡶࡡࡴࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡱࡪࡣࡩࡨࠨࡴࡧ࡯ࡪ࠱ࡧࡲࡨ࠮ࡷࡩࡲࡶ࡯ࡳࡣࡵࡽ࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡓࡨࡧ࠴ࡤࡰࡡࡥࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮ࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣࠪࠬ࠲ࡸ࡫ࡴࡠࡶࡵࡥࡨ࡫ࠨࠪ࡞ࡱࠦࠧࠨิ").format(str(bstack1ll11llll_opy_))
          bstack1l1l1l11l1_opy_ = bstack1l1lll1l1l_opy_ + bstack1111lllll_opy_
          bstack11l1l111ll_opy_ = bstack1ll11llll_opy_[bstack11lllll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧี")] + bstack11lllll_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥࡴࡦ࡯ࡳ࠲ࡵࡿࠧึ")
          with open(bstack11l1l111ll_opy_, bstack11lllll_opy_ (u"࠭ࡷࠨื")):
            pass
          with open(bstack11l1l111ll_opy_, bstack11lllll_opy_ (u"ࠢࡸุ࠭ࠥ")) as f:
            f.write(bstack1l1l1l11l1_opy_)
          import subprocess
          bstack111ll1lll1_opy_ = subprocess.run([bstack11lllll_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ูࠣ"), bstack11l1l111ll_opy_])
          if os.path.exists(bstack11l1l111ll_opy_):
            os.unlink(bstack11l1l111ll_opy_)
          os._exit(bstack111ll1lll1_opy_.returncode)
        else:
          if bstack111111ll1_opy_(bstack1ll11llll_opy_[bstack11lllll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩฺࠬ")]):
            bstack1ll11llll_opy_[bstack11lllll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭฻")].remove(bstack11lllll_opy_ (u"ࠫ࠲ࡳࠧ฼"))
            bstack1ll11llll_opy_[bstack11lllll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ฽")].remove(bstack11lllll_opy_ (u"࠭ࡰࡥࡤࠪ฾"))
            bstack1ll11llll_opy_[bstack11lllll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ฿")] = bstack1ll11llll_opy_[bstack11lllll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫเ")][0]
          bstack1l11l1lll_opy_(bstack1lll11l11l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1ll11llll_opy_[bstack11lllll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬแ")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack11lllll_opy_ (u"ࠪࡣࡤࡴࡡ࡮ࡧࡢࡣࠬโ")] = bstack11lllll_opy_ (u"ࠫࡤࡥ࡭ࡢ࡫ࡱࡣࡤ࠭ใ")
          mod_globals[bstack11lllll_opy_ (u"ࠬࡥ࡟ࡧ࡫࡯ࡩࡤࡥࠧไ")] = os.path.abspath(bstack1ll11llll_opy_[bstack11lllll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩๅ")])
          exec(open(bstack1ll11llll_opy_[bstack11lllll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪๆ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack11lllll_opy_ (u"ࠨࡅࡤࡹ࡬࡮ࡴࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠨ็").format(str(e)))
          for driver in bstack1l11ll11ll_opy_:
            bstack1ll11l11_opy_.append({
              bstack11lllll_opy_ (u"ࠩࡱࡥࡲ࡫่ࠧ"): bstack1ll11llll_opy_[bstack11lllll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ้࠭")],
              bstack11lllll_opy_ (u"ࠫࡪࡸࡲࡰࡴ๊ࠪ"): str(e),
              bstack11lllll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻ๋ࠫ"): multiprocessing.current_process().name
            })
            bstack11l1l111l_opy_(driver, bstack11lllll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭์"), bstack11lllll_opy_ (u"ࠢࡔࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥํ") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1l11ll11ll_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1l1lll1l1_opy_, CONFIG, logger)
      bstack11l1ll1l1l_opy_()
      bstack1ll11lllll_opy_()
      percy.bstack1ll1l1ll11_opy_()
      bstack1l1l1lllll_opy_ = {
        bstack11lllll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ๎"): args[0],
        bstack11lllll_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩ๏"): CONFIG,
        bstack11lllll_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫ๐"): bstack11l1ll111_opy_,
        bstack11lllll_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭๑"): bstack1l1lll1l1_opy_
      }
      if bstack11lllll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ๒") in CONFIG:
        bstack11ll11lll_opy_ = bstack1ll1l1l1l_opy_(args, logger, CONFIG, bstack11ll1l1l11_opy_, bstack111lllllll_opy_)
        bstack1l11l111l1_opy_ = bstack11ll11lll_opy_.bstack11lllll11_opy_(run_on_browserstack, bstack1l1l1lllll_opy_, bstack111111ll1_opy_(args))
      else:
        if bstack111111ll1_opy_(args):
          bstack1l1l1lllll_opy_[bstack11lllll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ๓")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1l1l1lllll_opy_,))
          test.start()
          test.join()
        else:
          bstack1l11l1lll_opy_(bstack1lll11l11l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack11lllll_opy_ (u"ࠧࡠࡡࡱࡥࡲ࡫࡟ࡠࠩ๔")] = bstack11lllll_opy_ (u"ࠨࡡࡢࡱࡦ࡯࡮ࡠࡡࠪ๕")
          mod_globals[bstack11lllll_opy_ (u"ࠩࡢࡣ࡫࡯࡬ࡦࡡࡢࠫ๖")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1l1111ll1l_opy_ == bstack11lllll_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ๗") or bstack1l1111ll1l_opy_ == bstack11lllll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ๘"):
    percy.init(bstack1l1lll1l1_opy_, CONFIG, logger)
    percy.bstack1ll1l1ll11_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack11l111ll11_opy_(e, bstack11l11ll11_opy_)
    bstack11l1ll1l1l_opy_()
    bstack1l11l1lll_opy_(bstack1l1lllll_opy_)
    if bstack11ll1l1l11_opy_:
      bstack1lll111ll1_opy_(bstack1l1lllll_opy_, args)
      if bstack11lllll_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ๙") in args:
        i = args.index(bstack11lllll_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ๚"))
        args.pop(i)
        args.pop(i)
      if bstack11lllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ๛") not in CONFIG:
        CONFIG[bstack11lllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ๜")] = [{}]
        bstack111lllllll_opy_ = 1
      if bstack11l1l1lll_opy_ == 0:
        bstack11l1l1lll_opy_ = 1
      args.insert(0, str(bstack11l1l1lll_opy_))
      args.insert(0, str(bstack11lllll_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ๝")))
    if bstack11lll1111l_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1l1ll1l11l_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1lll1l11l_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack11lllll_opy_ (u"ࠥࡖࡔࡈࡏࡕࡡࡒࡔ࡙ࡏࡏࡏࡕࠥ๞"),
        ).parse_args(bstack1l1ll1l11l_opy_)
        bstack11l1lllll_opy_ = args.index(bstack1l1ll1l11l_opy_[0]) if len(bstack1l1ll1l11l_opy_) > 0 else len(args)
        args.insert(bstack11l1lllll_opy_, str(bstack11lllll_opy_ (u"ࠫ࠲࠳࡬ࡪࡵࡷࡩࡳ࡫ࡲࠨ๟")))
        args.insert(bstack11l1lllll_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11lllll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡸ࡯ࡣࡱࡷࡣࡱ࡯ࡳࡵࡧࡱࡩࡷ࠴ࡰࡺࠩ๠"))))
        if bstack11l1lll11_opy_.bstack111l111l_opy_(CONFIG):
          args.insert(bstack11l1lllll_opy_, str(bstack11lllll_opy_ (u"࠭࠭࠮࡮࡬ࡷࡹ࡫࡮ࡦࡴࠪ๡")))
          args.insert(bstack11l1lllll_opy_ + 1, str(bstack11lllll_opy_ (u"ࠧࡓࡧࡷࡶࡾࡌࡡࡪ࡮ࡨࡨ࠿ࢁࡽࠨ๢").format(bstack11l1lll11_opy_.bstack1l1l1lll_opy_(CONFIG))))
        if bstack1ll1ll111_opy_(os.environ.get(bstack11lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓ࠭๣"))) and str(os.environ.get(bstack11lllll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭๤"), bstack11lllll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ๥"))) != bstack11lllll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ๦"):
          for bstack11lll1111_opy_ in bstack1lll1l11l_opy_:
            args.remove(bstack11lll1111_opy_)
          test_files = os.environ.get(bstack11lllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠩ๧")).split(bstack11lllll_opy_ (u"࠭ࠬࠨ๨"))
          for bstack1lll111l_opy_ in test_files:
            args.append(bstack1lll111l_opy_)
      except Exception as e:
        logger.error(bstack11lllll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡧࡴࡵࡣࡦ࡬࡮ࡴࡧࠡ࡮࡬ࡷࡹ࡫࡮ࡦࡴࠣࡪࡴࡸࠠࡼࡿ࠱ࠤࡊࡸࡲࡰࡴࠣ࠱ࠥࢁࡽࠣ๩").format(bstack11ll11lll1_opy_, e))
    pabot.main(args)
  elif bstack1l1111ll1l_opy_ == bstack11lllll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ๪"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack11l111ll11_opy_(e, bstack11l11ll11_opy_)
    for a in args:
      if bstack11lllll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘࠨ๫") in a:
        bstack1l11111ll_opy_ = int(a.split(bstack11lllll_opy_ (u"ࠪ࠾ࠬ๬"))[1])
      if bstack11lllll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨ๭") in a:
        bstack1lll1ll11l_opy_ = str(a.split(bstack11lllll_opy_ (u"ࠬࡀࠧ๮"))[1])
      if bstack11lllll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘ࠭๯") in a:
        bstack1ll1l11ll1_opy_ = str(a.split(bstack11lllll_opy_ (u"ࠧ࠻ࠩ๰"))[1])
    bstack11l1lll11l_opy_ = None
    bstack1llll1l1_opy_ = None
    if bstack11lllll_opy_ (u"ࠨ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠧ๱") in args:
      i = args.index(bstack11lllll_opy_ (u"ࠩ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠨ๲"))
      args.pop(i)
      bstack11l1lll11l_opy_ = args.pop(i)
    if bstack11lllll_opy_ (u"ࠪ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽ࠭๳") in args:
      i = args.index(bstack11lllll_opy_ (u"ࠫ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࠧ๴"))
      args.pop(i)
      bstack1llll1l1_opy_ = args.pop(i)
    if bstack11l1lll11l_opy_ is not None:
      global bstack1l1llll1l_opy_
      bstack1l1llll1l_opy_ = bstack11l1lll11l_opy_
    if bstack1llll1l1_opy_ is not None and int(bstack1l11111ll_opy_) < 0:
      bstack1l11111ll_opy_ = int(bstack1llll1l1_opy_)
    bstack1l11l1lll_opy_(bstack1l1lllll_opy_)
    run_cli(args)
    if bstack11lllll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩ๵") in multiprocessing.current_process().__dict__.keys():
      for bstack1l1l1llll_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1ll11l11_opy_.append(bstack1l1l1llll_opy_)
  elif bstack1l1111ll1l_opy_ == bstack11lllll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭๶"):
    bstack11l11ll1l1_opy_ = bstack1l1ll111_opy_(args, logger, CONFIG, bstack11ll1l1l11_opy_)
    bstack11l11ll1l1_opy_.bstack1ll1lll1_opy_()
    bstack11l1ll1l1l_opy_()
    bstack1llllllll_opy_ = True
    bstack111l1lll1_opy_ = bstack11l11ll1l1_opy_.bstack11l1ll11_opy_()
    bstack11l11ll1l1_opy_.bstack1l1l1lllll_opy_(bstack1ll111l1l_opy_)
    bstack11l11ll1l1_opy_.bstack11ll1l1111_opy_()
    bstack1111l1ll1_opy_(bstack1l1111ll1l_opy_, CONFIG, bstack11l11ll1l1_opy_.bstack1lllll1111_opy_())
    bstack11lll1l11l_opy_.end(EVENTS.bstack11111111_opy_.value, EVENTS.bstack11111111_opy_.value + bstack11lllll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ๷"), EVENTS.bstack11111111_opy_.value + bstack11lllll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ๸"), status=True, failure=None, test_name=bstack11l1l1ll1l_opy_)
    bstack1lll111ll_opy_ = bstack11l11ll1l1_opy_.bstack11lllll11_opy_(bstack1111lll1_opy_, {
      bstack11lllll_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪ๹"): bstack11l1ll111_opy_,
      bstack11lllll_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ๺"): bstack1l1lll1l1_opy_,
      bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ๻"): bstack11ll1l1l11_opy_
    })
    if not bstack1ll11llll_opy_:
      bstack11l11l1l_opy_ = bstack1lll11l1ll_opy_.bstack1llll1l1ll_opy_(EVENTS.bstack1l11l1l1ll_opy_.value)
    try:
      bstack11l1l1l1l1_opy_, bstack1l1lll111_opy_ = map(list, zip(*bstack1lll111ll_opy_))
      bstack1l1lllll1l_opy_ = bstack11l1l1l1l1_opy_[0]
      for status_code in bstack1l1lll111_opy_:
        if status_code != 0:
          bstack1l11111l1_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack11lllll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡤࡺࡪࠦࡥࡳࡴࡲࡶࡸࠦࡡ࡯ࡦࠣࡷࡹࡧࡴࡶࡵࠣࡧࡴࡪࡥ࠯ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡀࠠࡼࡿࠥ๼").format(str(e)))
  elif bstack1l1111ll1l_opy_ == bstack11lllll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭๽"):
    try:
      from behave.__main__ import main as bstack11l1ll1ll_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack11l111ll11_opy_(e, bstack1l1111l1_opy_)
    bstack11l1ll1l1l_opy_()
    bstack1llllllll_opy_ = True
    bstack11l11l1ll_opy_ = 1
    if bstack11lllll_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ๾") in CONFIG:
      bstack11l11l1ll_opy_ = CONFIG[bstack11lllll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ๿")]
    if bstack11lllll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ຀") in CONFIG:
      bstack1l1llll1l1_opy_ = int(bstack11l11l1ll_opy_) * int(len(CONFIG[bstack11lllll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ກ")]))
    else:
      bstack1l1llll1l1_opy_ = int(bstack11l11l1ll_opy_)
    config = Configuration(args)
    bstack1l1111ll1_opy_ = config.paths
    if len(bstack1l1111ll1_opy_) == 0:
      import glob
      pattern = bstack11lllll_opy_ (u"ࠫ࠯࠰࠯ࠫ࠰ࡩࡩࡦࡺࡵࡳࡧࠪຂ")
      bstack11lll1l111_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack11lll1l111_opy_)
      config = Configuration(args)
      bstack1l1111ll1_opy_ = config.paths
    bstack111l11111_opy_ = [os.path.normpath(item) for item in bstack1l1111ll1_opy_]
    bstack1llll11l1l_opy_ = [os.path.normpath(item) for item in args]
    bstack1111llll1_opy_ = [item for item in bstack1llll11l1l_opy_ if item not in bstack111l11111_opy_]
    import platform as pf
    if pf.system().lower() == bstack11lllll_opy_ (u"ࠬࡽࡩ࡯ࡦࡲࡻࡸ࠭຃"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack111l11111_opy_ = [str(PurePosixPath(PureWindowsPath(bstack11l1ll1111_opy_)))
                    for bstack11l1ll1111_opy_ in bstack111l11111_opy_]
    bstack1l11l1l11_opy_ = []
    for spec in bstack111l11111_opy_:
      bstack111ll1l1_opy_ = []
      bstack111ll1l1_opy_ += bstack1111llll1_opy_
      bstack111ll1l1_opy_.append(spec)
      bstack1l11l1l11_opy_.append(bstack111ll1l1_opy_)
    execution_items = []
    for bstack111ll1l1_opy_ in bstack1l11l1l11_opy_:
      if bstack11lllll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩຄ") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack11lllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ຅")]):
          item = {}
          item[bstack11lllll_opy_ (u"ࠨࡣࡵ࡫ࠬຆ")] = bstack11lllll_opy_ (u"ࠩࠣࠫງ").join(bstack111ll1l1_opy_)
          item[bstack11lllll_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩຈ")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack11lllll_opy_ (u"ࠫࡦࡸࡧࠨຉ")] = bstack11lllll_opy_ (u"ࠬࠦࠧຊ").join(bstack111ll1l1_opy_)
        item[bstack11lllll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ຋")] = 0
        execution_items.append(item)
    bstack1l11l1llll_opy_ = bstack11l11l111_opy_(execution_items, bstack1l1llll1l1_opy_)
    for execution_item in bstack1l11l1llll_opy_:
      bstack1l11ll1l1_opy_ = []
      for item in execution_item:
        bstack1l11ll1l1_opy_.append(bstack11ll11ll_opy_(name=str(item[bstack11lllll_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ຌ")]),
                                             target=bstack1l11111111_opy_,
                                             args=(item[bstack11lllll_opy_ (u"ࠨࡣࡵ࡫ࠬຍ")],)))
      for t in bstack1l11ll1l1_opy_:
        t.start()
      for t in bstack1l11ll1l1_opy_:
        t.join()
  else:
    bstack11l1ll11l1_opy_(bstack1l11l1lll1_opy_)
  if not bstack1ll11llll_opy_:
    bstack1llll11ll_opy_()
    if bstack11l11l1l_opy_:
      bstack1lll11l1ll_opy_.end(EVENTS.bstack1l11l1l1ll_opy_.value, bstack11l11l1l_opy_ + bstack11lllll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤຎ"), bstack11l11l1l_opy_ + bstack11lllll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣຏ"), status=True, failure=None, test_name=None)
  logger_utils.bstack1l1llllll_opy_()
def browserstack_initialize(bstack1l1l11l11_opy_=None):
  logger.info(bstack11lllll_opy_ (u"ࠫࡗࡻ࡮࡯࡫ࡱ࡫࡙ࠥࡄࡌࠢࡺ࡭ࡹ࡮ࠠࡢࡴࡪࡷ࠿ࠦࠧຐ") + str(bstack1l1l11l11_opy_))
  run_on_browserstack(bstack1l1l11l11_opy_, None, True)
@measure(event_name=EVENTS.bstack1l1l11l1ll_opy_, stage=STAGE.bstack1llll11111_opy_, bstack11lll11111_opy_=bstack11l1l1ll1l_opy_)
def bstack1llll11ll_opy_():
  global CONFIG
  global bstack11llllll11_opy_
  global bstack1l11111l1_opy_
  global bstack11ll111ll1_opy_
  global bstack1l111111_opy_
  bstack11l1111l11_opy_.bstack11lll111l1_opy_()
  if cli.is_running():
    bstack11l1ll1l_opy_.invoke(bstack1lll11l1l_opy_.bstack11l1l11l1_opy_)
  else:
    bstack1lll1111l1_opy_ = bstack11l1lll11_opy_.bstack1llll1l111_opy_(config=CONFIG)
    bstack1lll1111l1_opy_.bstack11ll1lll1_opy_(CONFIG)
  hashed_id = None
  bstack1l1l1lll1_opy_ = None
  def bstack1111l11l_opy_():
    try:
      if bstack11llllll11_opy_ == bstack11lllll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬຑ"):
        if not cli.is_enabled(CONFIG):
          bstack11lll1111l_opy_.stop()
      else:
        bstack11lll1111l_opy_.stop()
    except Exception as e:
      logger.debug(bstack11lllll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡹࡴࡰࡲࡳ࡭ࡳ࡭ࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࡾࢁࠧຒ").format(e))
  def bstack1l1l1ll1l_opy_():
    try:
      if not cli.is_enabled(CONFIG):
        bstack1l1l11llll_opy_.bstack1l1lll11ll_opy_()
    except Exception as e:
      logger.debug(bstack11lllll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡰࡳ࡫ࡱࡸ࡮ࡴࡧࠡࡤࡸ࡭ࡱࡪࠠ࡭࡫ࡱ࡯࠿ࠦࡻࡾࠤຓ").format(e))
  def bstack11llll11l1_opy_():
    nonlocal hashed_id, bstack1l1l1lll1_opy_
    try:
      if bstack11lllll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬດ") in CONFIG and str(CONFIG[bstack11lllll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ຕ")]).lower() != bstack11lllll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩຖ"):
        hashed_id, bstack1l1l1lll1_opy_ = bstack111l11l11_opy_()
      else:
        hashed_id, bstack1l1l1lll1_opy_ = get_build_link()
    except Exception as e:
      logger.debug(bstack11lllll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࠣࡰ࡮ࡴ࡫࠻ࠢࡾࢁࠧທ").format(e))
  bstack1l1l111l1l_opy_ = threading.Thread(target=bstack1111l11l_opy_)
  bstack111111l1_opy_ = threading.Thread(target=bstack1l1l1ll1l_opy_)
  bstack11111lll1_opy_ = threading.Thread(target=bstack11llll11l1_opy_)
  threads = [bstack1l1l111l1l_opy_, bstack111111l1_opy_, bstack11111lll1_opy_]
  for thread in threads:
    try:
      thread.start()
    except Exception as e:
      logger.debug(bstack11lllll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡸࡺࡡࡳࡶ࡬ࡲ࡬ࠦࡴࡩࡴࡨࡥࡩࠦࡻࡾ࠼ࠣࡿࢂࠨຘ").format(thread.name, e))
  for thread in threads:
    try:
      thread.join()
    except Exception as e:
      logger.debug(bstack11lllll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡰ࡯ࡪࡰ࡬ࡲ࡬ࠦࡴࡩࡴࡨࡥࡩࠦࡻࡾ࠼ࠣࡿࢂࠨນ").format(thread.name, e))
  bstack1ll1ll11l_opy_(hashed_id)
  logger.info(bstack11lllll_opy_ (u"ࠧࡔࡆࡎࠤࡷࡻ࡮ࠡࡧࡱࡨࡪࡪࠠࡧࡱࡵࠤ࡮ࡪ࠺ࠨບ") + bstack1l111111_opy_.get_property(bstack11lllll_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪປ"), bstack11lllll_opy_ (u"ࠩࠪຜ")) + bstack11lllll_opy_ (u"ࠪ࠰ࠥࡺࡥࡴࡶ࡫ࡹࡧࠦࡩࡥ࠼ࠣࠫຝ") + os.getenv(bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩພ"), bstack11lllll_opy_ (u"ࠬ࠭ຟ")))
  if hashed_id is not None and bstack11l1ll111l_opy_() != -1:
    sessions = bstack11lll1ll1l_opy_(hashed_id)
    bstack111l1ll1_opy_(sessions, bstack1l1l1lll1_opy_)
  if bstack11llllll11_opy_ == bstack11lllll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ຠ") and bstack1l11111l1_opy_ != 0:
    sys.exit(bstack1l11111l1_opy_)
  if bstack11llllll11_opy_ == bstack11lllll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧມ") and bstack11ll111ll1_opy_ != 0:
    sys.exit(bstack11ll111ll1_opy_)
def bstack1ll1ll11l_opy_(new_id):
    global bstack11l1ll1l1_opy_
    bstack11l1ll1l1_opy_ = new_id
def bstack1lll1ll1ll_opy_(bstack1llllllll1_opy_):
  if bstack1llllllll1_opy_:
    return bstack1llllllll1_opy_.capitalize()
  else:
    return bstack11lllll_opy_ (u"ࠨࠩຢ")
@measure(event_name=EVENTS.bstack11ll11l11_opy_, stage=STAGE.bstack1llll11111_opy_, bstack11lll11111_opy_=bstack11l1l1ll1l_opy_)
def bstack1ll11111ll_opy_(bstack11l111111l_opy_):
  if bstack11lllll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧຣ") in bstack11l111111l_opy_ and bstack11l111111l_opy_[bstack11lllll_opy_ (u"ࠪࡲࡦࡳࡥࠨ຤")] != bstack11lllll_opy_ (u"ࠫࠬລ"):
    return bstack11l111111l_opy_[bstack11lllll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ຦")]
  else:
    bstack11lll11111_opy_ = bstack11lllll_opy_ (u"ࠨࠢວ")
    if bstack11lllll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧຨ") in bstack11l111111l_opy_ and bstack11l111111l_opy_[bstack11lllll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨຩ")] != None:
      bstack11lll11111_opy_ += bstack11l111111l_opy_[bstack11lllll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩສ")] + bstack11lllll_opy_ (u"ࠥ࠰ࠥࠨຫ")
      if bstack11l111111l_opy_[bstack11lllll_opy_ (u"ࠫࡴࡹࠧຬ")] == bstack11lllll_opy_ (u"ࠧ࡯࡯ࡴࠤອ"):
        bstack11lll11111_opy_ += bstack11lllll_opy_ (u"ࠨࡩࡐࡕࠣࠦຮ")
      bstack11lll11111_opy_ += (bstack11l111111l_opy_[bstack11lllll_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫຯ")] or bstack11lllll_opy_ (u"ࠨࠩະ"))
      return bstack11lll11111_opy_
    else:
      bstack11lll11111_opy_ += bstack1lll1ll1ll_opy_(bstack11l111111l_opy_[bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪັ")]) + bstack11lllll_opy_ (u"ࠥࠤࠧາ") + (
              bstack11l111111l_opy_[bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ຳ")] or bstack11lllll_opy_ (u"ࠬ࠭ິ")) + bstack11lllll_opy_ (u"ࠨࠬࠡࠤີ")
      if bstack11l111111l_opy_[bstack11lllll_opy_ (u"ࠧࡰࡵࠪຶ")] == bstack11lllll_opy_ (u"࡙ࠣ࡬ࡲࡩࡵࡷࡴࠤື"):
        bstack11lll11111_opy_ += bstack11lllll_opy_ (u"ࠤ࡚࡭ࡳຸࠦࠢ")
      bstack11lll11111_opy_ += bstack11l111111l_opy_[bstack11lllll_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴູࠧ")] or bstack11lllll_opy_ (u"຺ࠫࠬ")
      return bstack11lll11111_opy_
@measure(event_name=EVENTS.bstack1l11ll1lll_opy_, stage=STAGE.bstack1llll11111_opy_, bstack11lll11111_opy_=bstack11l1l1ll1l_opy_)
def bstack1l1l1lll1l_opy_(bstack1l11l11l11_opy_):
  if bstack1l11l11l11_opy_ == bstack11lllll_opy_ (u"ࠧࡪ࡯࡯ࡧࠥົ"):
    return bstack11lllll_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡩࡵࡩࡪࡴ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡩࡵࡩࡪࡴࠢ࠿ࡅࡲࡱࡵࡲࡥࡵࡧࡧࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩຼ")
  elif bstack1l11l11l11_opy_ == bstack11lllll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢຽ"):
    return bstack11lllll_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡶࡪࡪ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡴࡨࡨࠧࡄࡆࡢ࡫࡯ࡩࡩࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫ຾")
  elif bstack1l11l11l11_opy_ == bstack11lllll_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ຿"):
    return bstack11lllll_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿࡭ࡲࡦࡧࡱ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧ࡭ࡲࡦࡧࡱࠦࡃࡖࡡࡴࡵࡨࡨࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪເ")
  elif bstack1l11l11l11_opy_ == bstack11lllll_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥແ"):
    return bstack11lllll_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡳࡧࡧ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡸࡥࡥࠤࡁࡉࡷࡸ࡯ࡳ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧໂ")
  elif bstack1l11l11l11_opy_ == bstack11lllll_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࠢໃ"):
    return bstack11lllll_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࠦࡩࡪࡧ࠳࠳࠸࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࠨ࡫ࡥࡢ࠵࠵࠺ࠧࡄࡔࡪ࡯ࡨࡳࡺࡺ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬໄ")
  elif bstack1l11l11l11_opy_ == bstack11lllll_opy_ (u"ࠣࡴࡸࡲࡳ࡯࡮ࡨࠤ໅"):
    return bstack11lllll_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡧࡲࡡࡤ࡭࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡧࡲࡡࡤ࡭ࠥࡂࡗࡻ࡮࡯࡫ࡱ࡫ࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪໆ")
  else:
    return bstack11lllll_opy_ (u"ࠪࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡢ࡭ࡣࡦ࡯ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡢ࡭ࡣࡦ࡯ࠧࡄࠧ໇") + bstack1lll1ll1ll_opy_(
      bstack1l11l11l11_opy_) + bstack11lllll_opy_ (u"ࠫࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀ່ࠪ")
def bstack1l1l1l111_opy_(session):
  return bstack11lllll_opy_ (u"ࠬࡂࡴࡳࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡵࡳࡼࠨ࠾࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠢࡶࡩࡸࡹࡩࡰࡰ࠰ࡲࡦࡳࡥࠣࡀ࠿ࡥࠥ࡮ࡲࡦࡨࡀࠦࢀࢃࠢࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤࡢࡦࡱࡧ࡮࡬ࠤࡁࡿࢂࡂ࠯ࡢࡀ࠿࠳ࡹࡪ࠾ࡼࡿࡾࢁࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼࠰ࡶࡵࡂ້ࠬ").format(
    session[bstack11lllll_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨࡥࡵࡳ࡮໊ࠪ")], bstack1ll11111ll_opy_(session), bstack1l1l1lll1l_opy_(session[bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡳࡵࡣࡷࡹࡸ໋࠭")]),
    bstack1l1l1lll1l_opy_(session[bstack11lllll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ໌")]),
    bstack1lll1ll1ll_opy_(session[bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪໍ")] or session[bstack11lllll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪ໎")] or bstack11lllll_opy_ (u"ࠫࠬ໏")) + bstack11lllll_opy_ (u"ࠧࠦࠢ໐") + (session[bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ໑")] or bstack11lllll_opy_ (u"ࠧࠨ໒")),
    session[bstack11lllll_opy_ (u"ࠨࡱࡶࠫ໓")] + bstack11lllll_opy_ (u"ࠤࠣࠦ໔") + session[bstack11lllll_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ໕")], session[bstack11lllll_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭໖")] or bstack11lllll_opy_ (u"ࠬ࠭໗"),
    session[bstack11lllll_opy_ (u"࠭ࡣࡳࡧࡤࡸࡪࡪ࡟ࡢࡶࠪ໘")] if session[bstack11lllll_opy_ (u"ࠧࡤࡴࡨࡥࡹ࡫ࡤࡠࡣࡷࠫ໙")] else bstack11lllll_opy_ (u"ࠨࠩ໚"))
@measure(event_name=EVENTS.bstack1l1ll1lll1_opy_, stage=STAGE.bstack1llll11111_opy_, bstack11lll11111_opy_=bstack11l1l1ll1l_opy_)
def bstack111l1ll1_opy_(sessions, bstack1l1l1lll1_opy_):
  try:
    bstack11l1ll1lll_opy_ = bstack11lllll_opy_ (u"ࠤࠥ໛")
    if not os.path.exists(bstack1lll1l1l_opy_):
      os.mkdir(bstack1lll1l1l_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11lllll_opy_ (u"ࠪࡥࡸࡹࡥࡵࡵ࠲ࡶࡪࡶ࡯ࡳࡶ࠱࡬ࡹࡳ࡬ࠨໜ")), bstack11lllll_opy_ (u"ࠫࡷ࠭ໝ")) as f:
      bstack11l1ll1lll_opy_ = f.read()
    bstack11l1ll1lll_opy_ = bstack11l1ll1lll_opy_.replace(bstack11lllll_opy_ (u"ࠬࢁࠥࡓࡇࡖ࡙ࡑ࡚ࡓࡠࡅࡒ࡙ࡓ࡚ࠥࡾࠩໞ"), str(len(sessions)))
    bstack11l1ll1lll_opy_ = bstack11l1ll1lll_opy_.replace(bstack11lllll_opy_ (u"࠭ࡻࠦࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠩࢂ࠭ໟ"), bstack1l1l1lll1_opy_)
    bstack11l1ll1lll_opy_ = bstack11l1ll1lll_opy_.replace(bstack11lllll_opy_ (u"ࠧࡼࠧࡅ࡙ࡎࡒࡄࡠࡐࡄࡑࡊࠫࡽࠨ໠"),
                                              sessions[0].get(bstack11lllll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟࡯ࡣࡰࡩࠬ໡")) if sessions[0] else bstack11lllll_opy_ (u"ࠩࠪ໢"))
    with open(os.path.join(bstack1lll1l1l_opy_, bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡵࡩࡵࡵࡲࡵ࠰࡫ࡸࡲࡲࠧ໣")), bstack11lllll_opy_ (u"ࠫࡼ࠭໤")) as stream:
      stream.write(bstack11l1ll1lll_opy_.split(bstack11lllll_opy_ (u"ࠬࢁࠥࡔࡇࡖࡗࡎࡕࡎࡔࡡࡇࡅ࡙ࡇࠥࡾࠩ໥"))[0])
      for session in sessions:
        stream.write(bstack1l1l1l111_opy_(session))
      stream.write(bstack11l1ll1lll_opy_.split(bstack11lllll_opy_ (u"࠭ࡻࠦࡕࡈࡗࡘࡏࡏࡏࡕࡢࡈࡆ࡚ࡁࠦࡿࠪ໦"))[1])
    logger.info(bstack11lllll_opy_ (u"ࠧࡈࡧࡱࡩࡷࡧࡴࡦࡦࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡥࡹ࡮ࡲࡤࠡࡣࡵࡸ࡮࡬ࡡࡤࡶࡶࠤࡦࡺࠠࡼࡿࠪ໧").format(bstack1lll1l1l_opy_));
  except Exception as e:
    logger.debug(bstack1l11ll11l_opy_.format(str(e)))
def bstack11lll1ll1l_opy_(hashed_id):
  global CONFIG
  try:
    bstack1l1111l111_opy_ = datetime.datetime.now()
    host = bstack11lllll_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡴ࡮࠳ࡣ࡭ࡱࡸࡨ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨ໨") if bstack11lllll_opy_ (u"ࠩࡤࡴࡵ࠭໩") in CONFIG else bstack11lllll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫ໪")
    user = CONFIG[bstack11lllll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭໫")]
    key = CONFIG[bstack11lllll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ໬")]
    bstack1llll1l11_opy_ = bstack11lllll_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ໭") if bstack11lllll_opy_ (u"ࠧࡢࡲࡳࠫ໮") in CONFIG else (bstack11lllll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬ໯") if CONFIG.get(bstack11lllll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭໰")) else bstack11lllll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ໱"))
    host = bstack1lll1l111_opy_(cli.config, [bstack11lllll_opy_ (u"ࠦࡦࡶࡩࡴࠤ໲"), bstack11lllll_opy_ (u"ࠧࡧࡰࡱࡃࡸࡸࡴࡳࡡࡵࡧࠥ໳"), bstack11lllll_opy_ (u"ࠨࡡࡱ࡫ࠥ໴")], host) if bstack11lllll_opy_ (u"ࠧࡢࡲࡳࠫ໵") in CONFIG else bstack1lll1l111_opy_(cli.config, [bstack11lllll_opy_ (u"ࠣࡣࡳ࡭ࡸࠨ໶"), bstack11lllll_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨࠦ໷"), bstack11lllll_opy_ (u"ࠥࡥࡵ࡯ࠢ໸")], host)
    url = bstack11lllll_opy_ (u"ࠫࢀࢃ࠯ࡼࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂ࠵ࡳࡦࡵࡶ࡭ࡴࡴࡳ࠯࡬ࡶࡳࡳ࠭໹").format(host, bstack1llll1l11_opy_, hashed_id)
    headers = {
      bstack11lllll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫ໺"): bstack11lllll_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ໻"),
    }
    proxies = bstack11l1l1111_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies, auth=(user, key))
    if response.json():
      cli.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠢࡩࡶࡷࡴ࠿࡭ࡥࡵࡡࡶࡩࡸࡹࡩࡰࡰࡶࡣࡱ࡯ࡳࡵࠤ໼"), datetime.datetime.now() - bstack1l1111l111_opy_)
      return list(map(lambda session: session[bstack11lllll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭໽")], response.json()))
  except Exception as e:
    logger.debug(bstack111l1lll11_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack11l1l11l1l_opy_, stage=STAGE.bstack1llll11111_opy_, bstack11lll11111_opy_=bstack11l1l1ll1l_opy_)
def get_build_link():
  global CONFIG
  global bstack11l1ll1l1_opy_
  try:
    if bstack11lllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ໾") in CONFIG:
      bstack1l1111l111_opy_ = datetime.datetime.now()
      host = bstack11lllll_opy_ (u"ࠪࡥࡵ࡯࠭ࡤ࡮ࡲࡹࡩ࠭໿") if bstack11lllll_opy_ (u"ࠫࡦࡶࡰࠨༀ") in CONFIG else bstack11lllll_opy_ (u"ࠬࡧࡰࡪࠩ༁")
      user = CONFIG[bstack11lllll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ༂")]
      key = CONFIG[bstack11lllll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ༃")]
      bstack1llll1l11_opy_ = bstack11lllll_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ༄") if bstack11lllll_opy_ (u"ࠩࡤࡴࡵ࠭༅") in CONFIG else bstack11lllll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ༆")
      url = bstack11lllll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࢀࢃ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠴ࡪࡴࡱࡱࠫ༇").format(user, key, host, bstack1llll1l11_opy_)
      if cli.is_enabled(CONFIG):
        bstack1l1l1lll1_opy_, hashed_id = cli.bstack111lll11_opy_()
        logger.info(bstack1l11111ll1_opy_.format(bstack1l1l1lll1_opy_))
        return [hashed_id, bstack1l1l1lll1_opy_]
      else:
        headers = {
          bstack11lllll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫ༈"): bstack11lllll_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ༉"),
        }
        if bstack11lllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ༊") in CONFIG:
          params = {bstack11lllll_opy_ (u"ࠨࡰࡤࡱࡪ࠭་"): CONFIG[bstack11lllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ༌")], bstack11lllll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭།"): CONFIG[bstack11lllll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭༎")]}
        else:
          params = {bstack11lllll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ༏"): CONFIG[bstack11lllll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ༐")]}
        proxies = bstack11l1l1111_opy_(CONFIG, url)
        response = requests.get(url, params=params, headers=headers, proxies=proxies)
        if response.json():
          bstack11l1111l_opy_ = response.json()[0][bstack11lllll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡧࡻࡩ࡭ࡦࠪ༑")]
          if bstack11l1111l_opy_:
            bstack1l1l1lll1_opy_ = bstack11l1111l_opy_[bstack11lllll_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣࡠࡷࡵࡰࠬ༒")].split(bstack11lllll_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤ࠯ࡥࡹ࡮ࡲࡤࠨ༓"))[0] + bstack11lllll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡵ࠲ࠫ༔") + bstack11l1111l_opy_[
              bstack11lllll_opy_ (u"ࠫ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ༕")]
            logger.info(bstack1l11111ll1_opy_.format(bstack1l1l1lll1_opy_))
            bstack11l1ll1l1_opy_ = bstack11l1111l_opy_[bstack11lllll_opy_ (u"ࠬ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ༖")]
            bstack11l1llllll_opy_ = CONFIG[bstack11lllll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ༗")]
            if bstack11lllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳ༘ࠩ") in CONFIG:
              bstack11l1llllll_opy_ += bstack11lllll_opy_ (u"ࠨ༙ࠢࠪ") + CONFIG[bstack11lllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ༚")]
            if bstack11l1llllll_opy_ != bstack11l1111l_opy_[bstack11lllll_opy_ (u"ࠪࡲࡦࡳࡥࠨ༛")]:
              logger.debug(bstack1lll111l1_opy_.format(bstack11l1111l_opy_[bstack11lllll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ༜")], bstack11l1llllll_opy_))
            cli.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࡫ࡪࡺ࡟ࡣࡷ࡬ࡰࡩࡥ࡬ࡪࡰ࡮ࠦ༝"), datetime.datetime.now() - bstack1l1111l111_opy_)
            return [bstack11l1111l_opy_[bstack11lllll_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ༞")], bstack1l1l1lll1_opy_]
    else:
      logger.warning(bstack1111l1ll_opy_)
  except Exception as e:
    logger.debug(bstack1l11l1l1l_opy_.format(str(e)))
  return [None, None]
def bstack1ll11l1l_opy_(url, bstack1ll11111_opy_=False):
  global CONFIG
  global bstack1l111ll11_opy_
  if not bstack1l111ll11_opy_:
    hostname = bstack11ll11l11l_opy_(url)
    is_private = bstack1l11111lll_opy_(hostname)
    if (bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ༟") in CONFIG and not bstack1ll1ll111_opy_(CONFIG[bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ༠")])) and (is_private or bstack1ll11111_opy_):
      bstack1l111ll11_opy_ = hostname
def bstack11ll11l11l_opy_(url):
  return urlparse(url).hostname
def bstack1l11111lll_opy_(hostname):
  for bstack1l1ll11lll_opy_ in bstack1l1111l11_opy_:
    regex = re.compile(bstack1l1ll11lll_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1lllll11_opy_(bstack1l11ll111l_opy_):
  return True if bstack1l11ll111l_opy_ in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack1ll111ll11_opy_, stage=STAGE.bstack1llll11111_opy_, bstack11lll11111_opy_=bstack11l1l1ll1l_opy_)
def getAccessibilityResults(driver):
  global CONFIG
  global bstack1l11111ll_opy_
  bstack11lllll111_opy_ = not (bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭༡"), None) and bstack1l1ll1ll1_opy_(
          threading.current_thread(), bstack11lllll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ༢"), None))
  bstack1ll1l1ll_opy_ = getattr(driver, bstack11lllll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫ༣"), None) != True
  bstack1l11ll1l1l_opy_ = bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠬ࡯ࡳࡂࡲࡳࡅ࠶࠷ࡹࡕࡧࡶࡸࠬ༤"), None) and bstack1l1ll1ll1_opy_(
          threading.current_thread(), bstack11lllll_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ༥"), None)
  if bstack1l11ll1l1l_opy_:
    if not bstack1lllllll1l_opy_():
      logger.warning(bstack11lllll_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡲࡳࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡪࡺࡲࡪࡧࡹࡩࠥࡇࡰࡱࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵ࠱ࠦ༦"))
      return {}
    logger.debug(bstack11lllll_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠬ༧"))
    logger.debug(perform_scan(driver, driver_command=bstack11lllll_opy_ (u"ࠩࡨࡼࡪࡩࡵࡵࡧࡖࡧࡷ࡯ࡰࡵࠩ༨")))
    results = bstack11llll1l1_opy_(bstack11lllll_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡶࠦ༩"))
    if results is not None and results.get(bstack11lllll_opy_ (u"ࠦ࡮ࡹࡳࡶࡧࡶࠦ༪")) is not None:
        return results[bstack11lllll_opy_ (u"ࠧ࡯ࡳࡴࡷࡨࡷࠧ༫")]
    logger.error(bstack11lllll_opy_ (u"ࠨࡎࡰࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡕࡩࡸࡻ࡬ࡵࡵࠣࡻࡪࡸࡥࠡࡨࡲࡹࡳࡪ࠮ࠣ༬"))
    return []
  if not bstack11l1llll11_opy_.bstack1ll1ll11l1_opy_(CONFIG, bstack1l11111ll_opy_) or (bstack1ll1l1ll_opy_ and bstack11lllll111_opy_):
    logger.warning(bstack11lllll_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴ࠰ࠥ༭"))
    return {}
  try:
    logger.debug(bstack11lllll_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠬ༮"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack1ll1111l1l_opy_.bstack11l1l1l1ll_opy_)
    return results
  except Exception:
    logger.error(bstack11lllll_opy_ (u"ࠤࡑࡳࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡷࡦࡴࡨࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦ༯"))
    return {}
@measure(event_name=EVENTS.bstack1l1l11lll_opy_, stage=STAGE.bstack1llll11111_opy_, bstack11lll11111_opy_=bstack11l1l1ll1l_opy_)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack1l11111ll_opy_
  bstack11lllll111_opy_ = not (bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ༰"), None) and bstack1l1ll1ll1_opy_(
          threading.current_thread(), bstack11lllll_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ༱"), None))
  bstack1ll1l1ll_opy_ = getattr(driver, bstack11lllll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬ༲"), None) != True
  bstack1l11ll1l1l_opy_ = bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭༳"), None) and bstack1l1ll1ll1_opy_(
          threading.current_thread(), bstack11lllll_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ༴"), None)
  if bstack1l11ll1l1l_opy_:
    if not bstack1lllllll1l_opy_():
      logger.warning(bstack11lllll_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡳࡴࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡸࡻ࡭࡮ࡣࡵࡽ࠳ࠨ༵"))
      return {}
    logger.debug(bstack11lllll_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡳࡶ࡯ࡰࡥࡷࡿࠧ༶"))
    logger.debug(perform_scan(driver, driver_command=bstack11lllll_opy_ (u"ࠪࡩࡽ࡫ࡣࡶࡶࡨࡗࡨࡸࡩࡱࡶ༷ࠪ")))
    results = bstack11llll1l1_opy_(bstack11lllll_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷࡗࡺࡳ࡭ࡢࡴࡼࠦ༸"))
    if results is not None and results.get(bstack11lllll_opy_ (u"ࠧࡹࡵ࡮࡯ࡤࡶࡾࠨ༹")) is not None:
        return results[bstack11lllll_opy_ (u"ࠨࡳࡶ࡯ࡰࡥࡷࡿࠢ༺")]
    logger.error(bstack11lllll_opy_ (u"ࠢࡏࡱࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡖࡪࡹࡵ࡭ࡶࡶࠤࡘࡻ࡭࡮ࡣࡵࡽࠥࡽࡡࡴࠢࡩࡳࡺࡴࡤ࠯ࠤ༻"))
    return {}
  if not bstack11l1llll11_opy_.bstack1ll1ll11l1_opy_(CONFIG, bstack1l11111ll_opy_) or (bstack1ll1l1ll_opy_ and bstack11lllll111_opy_):
    logger.warning(bstack11lllll_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡷࡺࡳ࡭ࡢࡴࡼ࠲ࠧ༼"))
    return {}
  try:
    logger.debug(bstack11lllll_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡳࡶ࡯ࡰࡥࡷࡿࠧ༽"))
    logger.debug(perform_scan(driver))
    bstack1111111l_opy_ = driver.execute_async_script(bstack1ll1111l1l_opy_.bstack111lll1l1_opy_)
    return bstack1111111l_opy_
  except Exception:
    logger.error(bstack11lllll_opy_ (u"ࠥࡒࡴࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡶ࡯ࡰࡥࡷࡿࠠࡸࡣࡶࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦ༾"))
    return {}
def bstack1lllllll1l_opy_():
  global CONFIG
  global bstack1l11111ll_opy_
  bstack11111lll_opy_ = bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ༿"), None) and bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧཀ"), None)
  if not bstack11l1llll11_opy_.bstack1ll1ll11l1_opy_(CONFIG, bstack1l11111ll_opy_) or not bstack11111lll_opy_:
        logger.warning(bstack11lllll_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡷ࡫ࡳࡶ࡮ࡷࡷ࠳ࠨཁ"))
        return False
  return True
def bstack11llll1l1_opy_(result_type):
    bstack1l1l11l111_opy_ = bstack11lll1111l_opy_.current_test_uuid() if bstack11lll1111l_opy_.current_test_uuid() else bstack1l1l11llll_opy_.current_hook_uuid()
    with ThreadPoolExecutor() as executor:
        future = executor.submit(bstack11l11l1lll_opy_(bstack1l1l11l111_opy_, result_type))
        try:
            return future.result(timeout=bstack1l11111l1l_opy_)
        except TimeoutError:
            logger.error(bstack11lllll_opy_ (u"ࠢࡕ࡫ࡰࡩࡴࡻࡴࠡࡣࡩࡸࡪࡸࠠࡼࡿࡶࠤࡼ࡮ࡩ࡭ࡧࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡘࡥࡴࡷ࡯ࡸࡸࠨག").format(bstack1l11111l1l_opy_))
        except Exception as ex:
            logger.debug(bstack11lllll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡳࡧࡷࡶ࡮࡫ࡶࡪࡰࡪࠤࡆࡶࡰࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࢁࡽ࠯ࠢࡈࡶࡷࡵࡲࠡ࠯ࠣࡿࢂࠨགྷ").format(result_type, str(ex)))
    return {}
@measure(event_name=EVENTS.bstack1ll1l111l1_opy_, stage=STAGE.bstack1llll11111_opy_, bstack11lll11111_opy_=bstack11l1l1ll1l_opy_)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack1l11111ll_opy_
  bstack11lllll111_opy_ = not (bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ང"), None) and bstack1l1ll1ll1_opy_(
          threading.current_thread(), bstack11lllll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩཅ"), None))
  bstack1l11lllll_opy_ = not (bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫཆ"), None) and bstack1l1ll1ll1_opy_(
          threading.current_thread(), bstack11lllll_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧཇ"), None))
  bstack1ll1l1ll_opy_ = getattr(driver, bstack11lllll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭཈"), None) != True
  if not bstack11l1llll11_opy_.bstack1ll1ll11l1_opy_(CONFIG, bstack1l11111ll_opy_) or (bstack1ll1l1ll_opy_ and bstack11lllll111_opy_ and bstack1l11lllll_opy_):
    logger.warning(bstack11lllll_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡶࡰࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮࠯ࠤཉ"))
    return {}
  try:
    bstack1l11l1ll1l_opy_ = bstack11lllll_opy_ (u"ࠨࡣࡳࡴࠬཊ") in CONFIG and CONFIG.get(bstack11lllll_opy_ (u"ࠩࡤࡴࡵ࠭ཋ"), bstack11lllll_opy_ (u"ࠪࠫཌ"))
    session_id = getattr(driver, bstack11lllll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨཌྷ"), None)
    if not session_id:
      logger.warning(bstack11lllll_opy_ (u"ࠧࡔ࡯ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡌࡈࠥ࡬࡯ࡶࡰࡧࠤ࡫ࡵࡲࠡࡦࡵ࡭ࡻ࡫ࡲࠣཎ"))
      return {bstack11lllll_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧཏ"): bstack11lllll_opy_ (u"ࠢࡏࡱࠣࡷࡪࡹࡳࡪࡱࡱࠤࡎࡊࠠࡧࡱࡸࡲࡩࠨཐ")}
    if bstack1l11l1ll1l_opy_:
      try:
        bstack1llll1111l_opy_ = {
              bstack11lllll_opy_ (u"ࠨࡶ࡫ࡎࡼࡺࡔࡰ࡭ࡨࡲࠬད"): os.environ.get(bstack11lllll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧདྷ"), os.environ.get(bstack11lllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧན"), bstack11lllll_opy_ (u"ࠫࠬཔ"))),
              bstack11lllll_opy_ (u"ࠬࡺࡨࡕࡧࡶࡸࡗࡻ࡮ࡖࡷ࡬ࡨࠬཕ"): bstack11lll1111l_opy_.current_test_uuid() if bstack11lll1111l_opy_.current_test_uuid() else bstack1l1l11llll_opy_.current_hook_uuid(),
              bstack11lllll_opy_ (u"࠭ࡡࡶࡶ࡫ࡌࡪࡧࡤࡦࡴࠪབ"): os.environ.get(bstack11lllll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬབྷ")),
              bstack11lllll_opy_ (u"ࠨࡵࡦࡥࡳ࡚ࡩ࡮ࡧࡶࡸࡦࡳࡰࠨམ"): str(int(datetime.datetime.now().timestamp() * 1000)),
              bstack11lllll_opy_ (u"ࠩࡷ࡬ࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧཙ"): os.environ.get(bstack11lllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨཚ"), bstack11lllll_opy_ (u"ࠫࠬཛ")),
              bstack11lllll_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬཛྷ"): kwargs.get(bstack11lllll_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡣࡰ࡯ࡰࡥࡳࡪࠧཝ"), None) or bstack11lllll_opy_ (u"ࠧࠨཞ")
          }
        if not hasattr(thread_local, bstack11lllll_opy_ (u"ࠨࡤࡤࡷࡪࡥࡡࡱࡲࡢࡥ࠶࠷ࡹࡠࡵࡦࡶ࡮ࡶࡴࠨཟ")):
            scripts = {bstack11lllll_opy_ (u"ࠩࡶࡧࡦࡴࠧའ"): bstack1ll1111l1l_opy_.perform_scan}
            thread_local.base_app_a11y_script = scripts
        bstack11lll11lll_opy_ = copy.deepcopy(thread_local.base_app_a11y_script)
        bstack11lll11lll_opy_[bstack11lllll_opy_ (u"ࠪࡷࡨࡧ࡮ࠨཡ")] = bstack11lll11lll_opy_[bstack11lllll_opy_ (u"ࠫࡸࡩࡡ࡯ࠩར")] % json.dumps(bstack1llll1111l_opy_)
        bstack1ll1111l1l_opy_.bstack1l11l11ll1_opy_(bstack11lll11lll_opy_)
        bstack1ll1111l1l_opy_.store()
        bstack1lll1lllll_opy_ = driver.execute_script(bstack1ll1111l1l_opy_.perform_scan)
      except Exception as bstack1ll11lll_opy_:
        logger.info(bstack11lllll_opy_ (u"ࠧࡇࡰࡱ࡫ࡸࡱࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡣࡢࡰࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࠧལ") + str(bstack1ll11lll_opy_))
        bstack1lll1lllll_opy_ = {bstack11lllll_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧཤ"): str(bstack1ll11lll_opy_)}
    else:
      bstack1lll1lllll_opy_ = driver.execute_async_script(bstack1ll1111l1l_opy_.perform_scan, {bstack11lllll_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪࠧཥ"): kwargs.get(bstack11lllll_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࡠࡥࡲࡱࡲࡧ࡮ࡥࠩས"), None) or bstack11lllll_opy_ (u"ࠩࠪཧ")})
    return bstack1lll1lllll_opy_
  except Exception as err:
    logger.error(bstack11lllll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡲࡶࡰࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮࠯ࠢࡾࢁࠧཨ").format(str(err)))
    return {}