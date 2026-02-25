# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
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
from browserstack_sdk.bstack11ll11l1l1_opy_ import bstack11ll1llll1_opy_
from browserstack_sdk.bstack1llll1111l_opy_ import *
import time
import requests
from bstack_utils.constants import EVENTS, STAGE, bstack11l1llll1l_opy_
from bstack_utils.messages import bstack111l111ll1_opy_, bstack111l11ll1l_opy_, bstack1l1111l1_opy_, bstack11llll1ll_opy_, bstack1ll1lll11l_opy_, bstack1l1llll1l_opy_
from bstack_utils.measure import measure
from bstack_utils.logger_utils import get_logger
from bstack_utils.helper import bstack1lll1l11l1_opy_
from browserstack_sdk.bstack11l1lll1ll_opy_ import bstack11lllllll_opy_
logger = get_logger(__name__)
def bstack1l1l11l1l1_opy_():
  global CONFIG
  headers = {
        bstack11l1l11_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack11l1l11_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1lll1l11l1_opy_(CONFIG, bstack11l1llll1l_opy_)
  try:
    response = requests.get(bstack11l1llll1l_opy_, headers=headers, proxies=proxies, timeout=2)
    if response.json():
      bstack1ll111llll_opy_ = response.json()[bstack11l1l11_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack111l111ll1_opy_.format(response.json()))
      return bstack1ll111llll_opy_
    else:
      logger.debug(bstack111l11ll1l_opy_.format(bstack11l1l11_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack111l11ll1l_opy_.format(e))
def bstack1ll1lll1l_opy_(hub_url):
  global CONFIG
  url = bstack11l1l11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack11l1l11_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack11l1l11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack11l1l11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1lll1l11l1_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=(0.5, 1.0))
    latency = time.perf_counter() - start_time
    logger.debug(bstack1l1111l1_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack11llll1ll_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack1ll1lllll1_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
def bstack1ll1ll1l_opy_():
  try:
    global bstack1l1l11ll11_opy_
    global CONFIG
    if bstack11l1l11_opy_ (u"ࠫ࡭ࡻࡢࡓࡧࡪ࡭ࡴࡴࠧࡾ") in CONFIG and CONFIG[bstack11l1l11_opy_ (u"ࠬ࡮ࡵࡣࡔࡨ࡫࡮ࡵ࡮ࠨࡿ")]:
      from bstack_utils.constants import bstack111ll111_opy_
      bstack11l11l11_opy_ = CONFIG[bstack11l1l11_opy_ (u"࠭ࡨࡶࡤࡕࡩ࡬࡯࡯࡯ࠩࢀ")]
      if bstack11l11l11_opy_ in bstack111ll111_opy_:
        bstack1l1l11ll11_opy_ = bstack111ll111_opy_[bstack11l11l11_opy_]
        logger.debug(bstack1ll1lll11l_opy_.format(bstack1l1l11ll11_opy_))
        return
      else:
        logger.debug(bstack11l1l11_opy_ (u"ࠢࡉࡷࡥࠤࡰ࡫ࡹࠡࠩࡾࢁࠬࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࡎࡕࡃࡡࡘࡖࡑࡥࡍࡂࡒ࠯ࠤ࡫ࡧ࡬࡭࡫ࡱ࡫ࠥࡨࡡࡤ࡭ࠣࡸࡴࠦ࡯ࡱࡶ࡬ࡱࡦࡲࠠࡩࡷࡥࠤࡩ࡫ࡴࡦࡥࡷ࡭ࡴࡴࠢࢁ").format(bstack11l11l11_opy_))
    bstack1ll111llll_opy_ = bstack1l1l11l1l1_opy_()
    from concurrent.futures import ThreadPoolExecutor, as_completed
    if bstack1ll111llll_opy_:
        with ThreadPoolExecutor(max_workers=len(bstack1ll111llll_opy_)) as executor:
            bstack1l1ll1ll_opy_ = {executor.submit(bstack1ll1lll1l_opy_, bstack11l1lll1l1_opy_): bstack11l1lll1l1_opy_ for bstack11l1lll1l1_opy_ in bstack1ll111llll_opy_}
            for future in as_completed(bstack1l1ll1ll_opy_):
                result = future.result()
                if result and result.get(bstack11l1l11_opy_ (u"ࠨ࡮ࡤࡸࡪࡴࡣࡺࠩࢂ")) is not None:
                    bstack1l1l11ll11_opy_ = result[bstack11l1l11_opy_ (u"ࠩ࡫ࡹࡧࡥࡵࡳ࡮ࠪࢃ")]
                    logger.debug(bstack1ll1lll11l_opy_.format(bstack1l1l11ll11_opy_))
                    return
        bstack1l1l11ll11_opy_ = bstack1ll111llll_opy_[0]
        logger.debug(bstack1ll1lll11l_opy_.format(bstack1l1l11ll11_opy_))
        return
  except Exception as e:
    logger.debug(bstack1l1llll1l_opy_.format(e))
from browserstack_sdk.bstack1ll1lll11_opy_ import *
from browserstack_sdk.bstack11l1lll1ll_opy_ import *
from browserstack_sdk.bstack1l111l1ll_opy_ import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.logger_utils import get_logger
from bstack_utils.measure import measure
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack111ll1l1ll_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
def bstack1ll1l1l1ll_opy_():
    global bstack1l1l11ll11_opy_
    try:
        bstack1l11lllll_opy_ = bstack1l1l1ll11l_opy_()
        bstack1ll11l111l_opy_(bstack1l11lllll_opy_)
        hub_url = bstack1l11lllll_opy_.get(bstack11l1l11_opy_ (u"ࠥࡹࡷࡲࠢࢄ"), bstack11l1l11_opy_ (u"ࠦࠧࢅ"))
        if hub_url.endswith(bstack11l1l11_opy_ (u"ࠬ࠵ࡷࡥ࠱࡫ࡹࡧ࠭ࢆ")):
            hub_url = hub_url.rsplit(bstack11l1l11_opy_ (u"࠭࠯ࡸࡦ࠲࡬ࡺࡨࠧࢇ"), 1)[0]
        if hub_url.startswith(bstack11l1l11_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࠨ࢈")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack11l1l11_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࠪࢉ")):
            hub_url = hub_url[8:]
        bstack1l1l11ll11_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack1l1l1ll11l_opy_():
    global CONFIG
    bstack1ll111ll_opy_ = CONFIG.get(bstack11l1l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢊ"), {}).get(bstack11l1l11_opy_ (u"ࠪ࡫ࡷ࡯ࡤࡏࡣࡰࡩࠬࢋ"), bstack11l1l11_opy_ (u"ࠫࡓࡕ࡟ࡈࡔࡌࡈࡤࡔࡁࡎࡇࡢࡔࡆ࡙ࡓࡆࡆࠪࢌ"))
    if not isinstance(bstack1ll111ll_opy_, str):
        raise ValueError(bstack11l1l11_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡌࡸࡩࡥࠢࡱࡥࡲ࡫ࠠ࡮ࡷࡶࡸࠥࡨࡥࠡࡣࠣࡺࡦࡲࡩࡥࠢࡶࡸࡷ࡯࡮ࡨࠤࢍ"))
    try:
        bstack1l11lllll_opy_ = bstack11l1llll_opy_(bstack1ll111ll_opy_)
        return bstack1l11lllll_opy_
    except Exception as e:
        logger.error(bstack11l1l11_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡩࡵ࡭ࡩࠦࡤࡦࡶࡤ࡭ࡱࡹࠠ࠻ࠢࡾࢁࠧࢎ").format(str(e)))
        return {}
def bstack11l1llll_opy_(bstack1ll111ll_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack11l1l11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ࢏")] or not CONFIG[bstack11l1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ࢐")]:
            raise ValueError(bstack11l1l11_opy_ (u"ࠤࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠤࡴࡸࠠࡢࡥࡦࡩࡸࡹࠠ࡬ࡧࡼࠦ࢑"))
        url = bstack1ll11lllll_opy_ + bstack1ll111ll_opy_
        auth = (CONFIG[bstack11l1l11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ࢒")], CONFIG[bstack11l1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ࢓")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack11lll11ll1_opy_ = json.loads(response.text)
            return bstack11lll11ll1_opy_
    except ValueError as ve:
        logger.error(bstack11l1l11_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡩࡵ࡭ࡩࠦࡤࡦࡶࡤ࡭ࡱࡹࠠ࠻ࠢࡾࢁࠧ࢔").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack11l1l11_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡪࡶ࡮ࡪࠠࡥࡧࡷࡥ࡮ࡲࡳࠡ࠼ࠣࡿࢂࠨ࢕").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack1ll11l111l_opy_(bstack1l11ll1111_opy_):
    global CONFIG
    if bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ࢖") not in CONFIG or str(CONFIG[bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬࢗ")]).lower() == bstack11l1l11_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ࢘"):
        CONFIG[bstack11l1l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭࢙ࠩ")] = False
    elif bstack11l1l11_opy_ (u"ࠫ࡮ࡹࡔࡳ࡫ࡤࡰࡌࡸࡩࡥ࢚ࠩ") in bstack1l11ll1111_opy_:
        bstack11l1llll11_opy_ = CONFIG.get(bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴ࢛ࠩ"), {})
        logger.debug(bstack11l1l11_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡸࡪࡵࡷ࡭ࡳ࡭ࠠ࡭ࡱࡦࡥࡱࠦ࡯ࡱࡶ࡬ࡳࡳࡹ࠺ࠡࠧࡶࠦ࢜"), bstack11l1llll11_opy_)
        bstack11l111l1ll_opy_ = bstack1l11ll1111_opy_.get(bstack11l1l11_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡒࡦࡲࡨࡥࡹ࡫ࡲࡴࠤ࢝"), [])
        bstack11ll1ll11_opy_ = bstack11l1l11_opy_ (u"ࠣ࠮ࠥ࢞").join(bstack11l111l1ll_opy_)
        logger.debug(bstack11l1l11_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡅࡸࡷࡹࡵ࡭ࠡࡴࡨࡴࡪࡧࡴࡦࡴࠣࡷࡹࡸࡩ࡯ࡩ࠽ࠤࠪࡹࠢ࢟"), bstack11ll1ll11_opy_)
        bstack111lll1lll_opy_ = {
            bstack11l1l11_opy_ (u"ࠥࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧࢠ"): bstack11l1l11_opy_ (u"ࠦࡦࡺࡳ࠮ࡴࡨࡴࡪࡧࡴࡦࡴࠥࢡ"),
            bstack11l1l11_opy_ (u"ࠧ࡬࡯ࡳࡥࡨࡐࡴࡩࡡ࡭ࠤࢢ"): bstack11l1l11_opy_ (u"ࠨࡴࡳࡷࡨࠦࢣ"),
            bstack11l1l11_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࠭ࡳࡧࡳࡩࡦࡺࡥࡳࠤࢤ"): bstack11ll1ll11_opy_
        }
        bstack11l1llll11_opy_.update(bstack111lll1lll_opy_)
        logger.debug(bstack11l1l11_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡖࡲࡧࡥࡹ࡫ࡤࠡ࡮ࡲࡧࡦࡲࠠࡰࡲࡷ࡭ࡴࡴࡳ࠻ࠢࠨࡷࠧࢥ"), bstack11l1llll11_opy_)
        CONFIG[bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢦ")] = bstack11l1llll11_opy_
        logger.debug(bstack11l1l11_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡉ࡭ࡳࡧ࡬ࠡࡅࡒࡒࡋࡏࡇ࠻ࠢࠨࡷࠧࢧ"), CONFIG)
def bstack11l11l11l_opy_():
    bstack1l11lllll_opy_ = bstack1l1l1ll11l_opy_()
    if not bstack1l11lllll_opy_[bstack11l1l11_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡖࡴ࡯ࠫࢨ")]:
      raise ValueError(bstack11l1l11_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡗࡵࡰࠥ࡯ࡳࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡩࡶࡴࡳࠠࡨࡴ࡬ࡨࠥࡪࡥࡵࡣ࡬ࡰࡸ࠴ࠢࢩ"))
    return bstack1l11lllll_opy_[bstack11l1l11_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡘࡶࡱ࠭ࢪ")] + bstack11l1l11_opy_ (u"ࠧࡀࡥࡤࡴࡸࡃࠧࢫ")
@measure(event_name=EVENTS.bstack11lll1l11_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
def bstack1l1ll1lll1_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack11l1l11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪࢬ")], CONFIG[bstack11l1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬࢭ")])
        url = bstack1ll1111l11_opy_
        logger.debug(bstack11l1l11_opy_ (u"ࠥࡅࡹࡺࡥ࡮ࡲࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴࠢࡩࡶࡴࡳࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡔࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠣࡅࡕࡏࠢࢮ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack11l1l11_opy_ (u"ࠦࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠥࢯ"): bstack11l1l11_opy_ (u"ࠧࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠣࢰ")})
            if response.status_code == 200:
                bstack1111ll1l1_opy_ = json.loads(response.text)
                bstack1l11ll1lll_opy_ = bstack1111ll1l1_opy_.get(bstack11l1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡸ࠭ࢱ"), [])
                if bstack1l11ll1lll_opy_:
                    bstack1111lllll1_opy_ = bstack1l11ll1lll_opy_[0]
                    build_hashed_id = bstack1111lllll1_opy_.get(bstack11l1l11_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪࢲ"))
                    bstack1l1l1lll1_opy_ = bstack1l11l11l1l_opy_ + build_hashed_id
                    result.extend([build_hashed_id, bstack1l1l1lll1_opy_])
                    logger.info(bstack11l1ll11ll_opy_.format(bstack1l1l1lll1_opy_))
                    bstack1ll1l1lll_opy_ = CONFIG[bstack11l1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫࢳ")]
                    if bstack11l1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࢴ") in CONFIG:
                      bstack1ll1l1lll_opy_ += bstack11l1l11_opy_ (u"ࠪࠤࠬࢵ") + CONFIG[bstack11l1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࢶ")]
                    if bstack1ll1l1lll_opy_ != bstack1111lllll1_opy_.get(bstack11l1l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪࢷ")):
                      logger.debug(bstack11ll111ll1_opy_.format(bstack1111lllll1_opy_.get(bstack11l1l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫࢸ")), bstack1ll1l1lll_opy_))
                    return result
                else:
                    logger.debug(bstack11l1l11_opy_ (u"ࠢࡂࡖࡖࠤ࠿ࠦࡎࡰࠢࡥࡹ࡮ࡲࡤࡴࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠱ࠦࢹ"))
            else:
                logger.debug(bstack11l1l11_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴ࠰ࠥࢺ"))
        except Exception as e:
            logger.error(bstack11l1l11_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࡶࠤ࠿ࠦࡻࡾࠤࢻ").format(str(e)))
    else:
        logger.debug(bstack11l1l11_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡆࡓࡓࡌࡉࡈࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡶࡩࡹ࠴ࠠࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴ࠰ࠥࢼ"))
    return [None, None]
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack11l1l1l11_opy_ import bstack11l1l1l11_opy_, bstack1lllllll1_opy_, bstack11l1l1ll1_opy_, bstack1l1111l1l_opy_
from bstack_utils.measure import bstack111lll111l_opy_
from bstack_utils.measure import measure
from bstack_utils.percy import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack111111l1_opy_ import bstack11llllll11_opy_
from bstack_utils.messages import *
from bstack_utils import logger_utils
from bstack_utils.constants import *
from bstack_utils.helper import bstack1l1ll1111_opy_, bstack11l11llll_opy_, bstack1ll11l1l11_opy_, bstack11llll11l1_opy_, \
  bstack1lll1l1l_opy_, \
  Notset, is_robot_playwright_installed, bstack11ll1l1l1l_opy_, \
  bstack11l11l1ll1_opy_, bstack111ll1lll_opy_, bstack1l1l1llll1_opy_, bstack1l111l1lll_opy_, bstack1llll1ll1_opy_, bstack1ll111l1l_opy_, \
  bstack11ll1111ll_opy_, \
  bstack11lll1l111_opy_, bstack1l1l1l1l1_opy_, bstack11l1ll1l1_opy_, bstack111l11111_opy_, \
  bstack1llll1l11_opy_, bstack111l1l1l11_opy_, bstack1lll1l111_opy_, bstack1l1ll1l111_opy_, bstack11l11l111l_opy_
from bstack_utils.bstack1ll1l11ll_opy_ import bstack11l11lll_opy_
from bstack_utils.bstack1111l111_opy_ import bstack1l11ll1l1_opy_, bstack1l11l111l1_opy_
from bstack_utils.bstack111l1lll1_opy_ import bstack1l111111l_opy_
from bstack_utils.session_utils import bstack11lll1l11l_opy_, bstack1l111l11l1_opy_
from bstack_utils.bstack111llllll1_opy_ import bstack111llllll1_opy_
from bstack_utils.bstack1l1ll11ll_opy_ import bstack11l111lll_opy_
from bstack_utils.proxy import bstack11ll11lll_opy_, bstack1lll1l11l1_opy_, bstack11lll1ll11_opy_, bstack1l1llll1_opy_
from bstack_utils.bstack1ll1111ll_opy_ import bstack1ll1l1l1l_opy_, bstack1l1l1l1l11_opy_
import bstack_utils.bstack111l111l11_opy_ as bstack1l11l1l111_opy_
import bstack_utils.bstack1l1l11l1ll_opy_ as bstack1l11l1ll1l_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.utils.bstack1l1l1l111_opy_ import bstack1ll11l1ll_opy_
from bstack_utils.bstack11ll11l1l_opy_ import bstack1l1l11l11l_opy_
from bstack_utils.bstack1lll111ll1_opy_ import bstack111ll1111_opy_
from bstack_utils.bstack111lll111l_opy_ import bstack11ll1l1l1_opy_
if os.getenv(bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡉࡑࡒࡏࡘ࠭ࢽ")):
  cli.bstack11ll1ll1_opy_()
else:
  os.environ[bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡊࡒࡓࡐ࡙ࠧࢾ")] = bstack11l1l11_opy_ (u"࠭ࡴࡳࡷࡨࠫࢿ")
bstack1llll11ll1_opy_ = bstack11l1l11_opy_ (u"ࠧࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠠࠡ࡫ࡩࠬࡵࡧࡧࡦࠢࡀࡁࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠠࡼ࡞ࡱࠤࠥࠦࡴࡳࡻࡾࡠࡳࠦࡣࡰࡰࡶࡸࠥ࡬ࡳࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࡡ࠭ࡦࡴ࡞ࠪ࠭ࡀࡢ࡮ࠡࠢࠣࠤࠥ࡬ࡳ࠯ࡣࡳࡴࡪࡴࡤࡇ࡫࡯ࡩࡘࡿ࡮ࡤࠪࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠬࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡳࡣ࡮ࡴࡤࡦࡺࠬࠤ࠰ࠦࠢ࠻ࠤࠣ࠯ࠥࡐࡓࡐࡐ࠱ࡷࡹࡸࡩ࡯ࡩ࡬ࡪࡾ࠮ࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࠬࡦࡽࡡࡪࡶࠣࡲࡪࡽࡐࡢࡩࡨ࠶࠳࡫ࡶࡢ࡮ࡸࡥࡹ࡫ࠨࠣࠪࠬࠤࡂࡄࠠࡼࡿࠥ࠰ࠥࡢࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡨࡧࡷࡗࡪࡹࡳࡪࡱࡱࡈࡪࡺࡡࡪ࡮ࡶࠦࢂࡢࠧࠪࠫࠬ࡟ࠧ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠣ࡟ࠬࠤ࠰ࠦࠢ࠭࡞࡟ࡲࠧ࠯࡜࡯ࠢࠣࠤࠥࢃࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡽ࡝ࡰࠣࠤ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠧࣀ")
LAUNCH_PATCH_ROBOT_PLAYWRIGHT = bstack11l1l11_opy_ (u"ࠨ࡞ࡱ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࡢ࡮ࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡰࡢࡶ࡫ࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳࡞࡞ࡱࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠴ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡶ࡟ࡪࡰࡧࡩࡽࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠴ࡠࡠࡳࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡹ࡬ࡪࡥࡨࠬ࠵࠲ࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࠬࡠࡳࡩ࡯࡯ࡵࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬ࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ࠭ࡀࡢ࡮ࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮࡭ࡣࡸࡲࡨ࡮ࠠ࠾ࠢࡤࡷࡾࡴࡣࠡࠪ࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴࠫࠣࡁࡃࠦࡻ࡝ࡰ࡯ࡩࡹࠦࡣࡢࡲࡶ࠿ࡡࡴࡴࡳࡻࠣࡿࡡࡴࡣࡢࡲࡶࠤࡂࠦࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠪ࡞ࡱࠤࠥࢃࠠࡤࡣࡷࡧ࡭࠮ࡥࡹࠫࠣࡿࡡࡴࠠࠡࠢࠣࢁࡡࡴࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡣࡺࡥ࡮ࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮ࡤࡱࡱࡲࡪࡩࡴࠩࡽ࡟ࡲࠥࠦࠠࠡࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸ࠿ࠦࡠࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠦࡾࡩࡳࡩ࡯ࡥࡧࡘࡖࡎࡉ࡯࡮ࡲࡲࡲࡪࡴࡴࠩࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡦࡥࡵࡹࠩࠪࡿࡣ࠰ࡡࡴࠠࠡࠢࠣ࠲࠳࠴࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸࡢ࡮ࠡࠢࢀ࠭ࡡࡴࡽ࡝ࡰࡦࡳࡳࡹࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡧࡴࡴ࡮ࡦࡥࡷࠤࡂࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺ࠮ࡣ࡫ࡱࡨ࠭࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠮ࡁ࡜࡯࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭࠯ࡥࡲࡲࡳ࡫ࡣࡵࠢࡀࠤࡦࡹࡹ࡯ࡥࠣࠬࡨࡵ࡮࡯ࡧࡦࡸࡔࡶࡴࡪࡱࡱࡷ࠮ࠦ࠽࠿ࠢࡾࡠࡳࠦࠠ࡭ࡧࡷࠤࡨࡧࡰࡴ࠽࡟ࡲࠥࠦࡴࡳࡻࠣࡿࡡࡴࠠࠡࠢࠣࡧࡦࡶࡳࠡ࠿ࠣࡎࡘࡕࡎ࠯ࡲࡤࡶࡸ࡫ࠨࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷ࠮ࡢ࡮ࠡࠢࢀࠤࡨࡧࡴࡤࡪࠫࡩࡽ࠯ࠠࡼ࡞ࡱࠤࠥࢃ࡜࡯ࠢࠣࡧࡴࡴࡳࡵࠢࡰࡳࡩ࡯ࡦࡪࡧࡧࡉࡳࡪࡰࡰ࡫ࡱࡸࠥࡃࠠࡡࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࡣࠤ࠰ࠦࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭ࡀࡢ࡮ࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤ࠳࠴࠮ࡤࡱࡱࡲࡪࡩࡴࡐࡲࡷ࡭ࡴࡴࡳ࠭࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࡝ࡰࠣࠤࢂ࠯࡜࡯ࡿ࡟ࡲ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵࡜࡯ࠩࣁ")
from ._version import __version__
bstack1l11l11lll_opy_ = None
CONFIG = {}
bstack11l1lll11_opy_ = {}
bstack11ll111111_opy_ = {}
bstack1ll1l1111l_opy_ = None
bstack11l11l11ll_opy_ = None
bstack1ll1ll11l1_opy_ = None
bstack11ll1l111_opy_ = -1
bstack11ll111l1_opy_ = 0
bstack1l11l11l1_opy_ = bstack1llllll1l_opy_
bstack1lll1l1l11_opy_ = 1
bstack1l11ll11ll_opy_ = False
bstack11l1l11111_opy_ = False
bstack11ll1ll111_opy_ = bstack11l1l11_opy_ (u"ࠩࠪࣂ")
bstack1l1l1l1ll1_opy_ = bstack11l1l11_opy_ (u"ࠪࠫࣃ")
bstack1l11ll1ll1_opy_ = False
bstack1l1111111_opy_ = True
bstack111ll1llll_opy_ = False
bstack1ll111l11l_opy_ = bstack11l1l11_opy_ (u"ࠫࠬࣄ")
bstack1ll1111ll1_opy_ = []
bstack1lllllll11_opy_ = threading.Lock()
bstack11ll1l1ll1_opy_ = threading.Lock()
bstack1ll1lll1ll_opy_ = None
bstack1l1l11ll11_opy_ = bstack11l1l11_opy_ (u"ࠬ࠭ࣅ")
bstack1lll1ll1ll_opy_ = False
bstack1l11l1llll_opy_ = None
bstack111111lll_opy_ = None
bstack11l11ll11_opy_ = None
bstack1lll1llll1_opy_ = -1
bstack11l1l111l1_opy_ = os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"࠭ࡾࠨࣆ")), bstack11l1l11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧࣇ"), bstack11l1l11_opy_ (u"ࠨ࠰ࡵࡳࡧࡵࡴ࠮ࡴࡨࡴࡴࡸࡴ࠮ࡪࡨࡰࡵ࡫ࡲ࠯࡬ࡶࡳࡳ࠭ࣈ"))
bstack11l111l1_opy_ = 0
bstack1lll111l1_opy_ = 0
bstack1111lllll_opy_ = []
bstack111ll11l11_opy_ = []
ROBOT_PYTHON_ERRORS = []
bstack1l1l1l1ll_opy_ = []
bstack11lll1l1l_opy_ = bstack11l1l11_opy_ (u"ࠩࠪࣉ")
bstack1lll1ll1l1_opy_ = bstack11l1l11_opy_ (u"ࠪࠫ࣊")
bstack11lll11111_opy_ = False
bstack1lll11lll_opy_ = False
bstack1ll11ll11l_opy_ = {}
bstack1l11lllll1_opy_ = {}
bstack11l1ll11l1_opy_ = None
bstack1l1ll111l1_opy_ = None
bstack1ll111l111_opy_ = None
bstack1l11llll11_opy_ = None
bstack1l1lllllll_opy_ = None
bstack1l111l111l_opy_ = None
bstack1lll111lll_opy_ = None
bstack1lll111111_opy_ = None
bstack111l1l111_opy_ = None
bstack11l111lll1_opy_ = None
bstack1l1l111ll1_opy_ = None
bstack111l1ll11l_opy_ = None
bstack11l11l1l_opy_ = None
bstack1lll111ll_opy_ = None
bstack11ll11ll11_opy_ = None
bstack1l11l1ll1_opy_ = None
bstack11l11llll1_opy_ = None
bstack11l111l11l_opy_ = None
bstack1lll1lll1l_opy_ = None
bstack1l1l1111l_opy_ = None
bstack1l11llll1_opy_ = None
bstack1l1l1l1lll_opy_ = None
bstack1l1lll1111_opy_ = None
thread_local = threading.local()
bstack11l11ll111_opy_ = False
bstack11ll1l11l1_opy_ = bstack11l1l11_opy_ (u"ࠦࠧ࣋")
logger = logger_utils.get_logger(__name__, bstack1l11l11l1_opy_)
bstack11ll111ll_opy_ = logger_utils.bstack1lll1lll_opy_(__name__)
global_config = Config.get_instance()
percy = bstack11l1llll1_opy_()
bstack1l11l1l1l_opy_ = bstack11llllll11_opy_()
bstack1llllll1l1_opy_ = bstack1l111l1ll_opy_()
def bstack111l111lll_opy_():
  global CONFIG
  global bstack11lll11111_opy_
  global global_config
  testContextOptions = bstack1ll1lll1_opy_(CONFIG)
  if bstack1lll1l1l_opy_(CONFIG):
    if (bstack11l1l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ࣌") in testContextOptions and str(testContextOptions[bstack11l1l11_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ࣍")]).lower() == bstack11l1l11_opy_ (u"ࠧࡵࡴࡸࡩࠬ࣎")):
      bstack11lll11111_opy_ = True
      global_config.bstack1l1l1111l1_opy_(True)
    global_config.bstack1lllll11l1_opy_(testContextOptions.get(bstack11l1l11_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷ࣏ࠬ"), False))
  else:
    bstack11lll11111_opy_ = True
    global_config.bstack1l1l1111l1_opy_(True)
    global_config.bstack1lllll11l1_opy_(True)
def bstack1l11lll1l1_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1l1ll1111l_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack111ll11ll1_opy_():
  global bstack1l11lllll1_opy_
  args = sys.argv
  for i in range(len(args)):
    if bstack11l1l11_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡦࡳࡳ࡬ࡩࡨࡨ࡬ࡰࡪࠨ࣐") == args[i].lower() or bstack11l1l11_opy_ (u"ࠥ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡮ࡧ࡫ࡪ࣑ࠦ") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      bstack1l11lllll1_opy_[bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ࣒")] = path
      return path
  return None
bstack1ll111l1ll_opy_ = re.compile(bstack11l1l11_opy_ (u"ࡷࠨ࠮ࠫࡁ࡟ࠨࢀ࠮࠮ࠫࡁࠬࢁ࠳࠰࠿࣓ࠣ"))
def bstack1ll11l1ll1_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1ll111l1ll_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack11l1l11_opy_ (u"ࠨࠤࡼࠤࣔ") + group + bstack11l1l11_opy_ (u"ࠢࡾࠤࣕ"), os.environ.get(group))
  return value
def bstack11l1lll111_opy_():
  global bstack1l1lll1111_opy_
  if bstack1l1lll1111_opy_ is None:
        bstack1l1lll1111_opy_ = bstack111ll11ll1_opy_()
  bstack11ll1lllll_opy_ = bstack1l1lll1111_opy_
  if bstack11ll1lllll_opy_ and os.path.exists(os.path.abspath(bstack11ll1lllll_opy_)):
    fileName = bstack11ll1lllll_opy_
  if bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬࣖ") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࡠࡈࡌࡐࡊ࠭ࣗ")])) and not bstack11l1l11_opy_ (u"ࠪࡪ࡮ࡲࡥࡏࡣࡰࡩࠬࣘ") in locals():
    fileName = os.environ[bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨࣙ")]
  if bstack11l1l11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡑࡥࡲ࡫ࠧࣚ") in locals():
    bstack1lll1ll_opy_ = os.path.abspath(fileName)
  else:
    bstack1lll1ll_opy_ = bstack11l1l11_opy_ (u"࠭ࠧࣛ")
  bstack111l1l1111_opy_ = os.getcwd()
  bstack1lll1ll1_opy_ = bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪࣜ")
  bstack1ll1ll1lll_opy_ = bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺࡣࡰࡰࠬࣝ")
  while (not os.path.exists(bstack1lll1ll_opy_)) and bstack111l1l1111_opy_ != bstack11l1l11_opy_ (u"ࠤࠥࣞ"):
    bstack1lll1ll_opy_ = os.path.join(bstack111l1l1111_opy_, bstack1lll1ll1_opy_)
    if not os.path.exists(bstack1lll1ll_opy_):
      bstack1lll1ll_opy_ = os.path.join(bstack111l1l1111_opy_, bstack1ll1ll1lll_opy_)
    if bstack111l1l1111_opy_ != os.path.dirname(bstack111l1l1111_opy_):
      bstack111l1l1111_opy_ = os.path.dirname(bstack111l1l1111_opy_)
    else:
      bstack111l1l1111_opy_ = bstack11l1l11_opy_ (u"ࠥࠦࣟ")
  bstack1l1lll1111_opy_ = bstack1lll1ll_opy_ if os.path.exists(bstack1lll1ll_opy_) else None
  return bstack1l1lll1111_opy_
def bstack11lll111_opy_(config):
    if bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࠫ࣠") in config:
      config[bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ࣡")] = config[bstack11l1l11_opy_ (u"࠭ࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬࠭࣢")]
    if bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭ࡏࡱࡶ࡬ࡳࡳࡹࣣࠧ") in config:
      config[bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬࣤ")] = config[bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺࡒࡦࡲࡲࡶࡹ࡯࡮ࡨࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣥ")]
def bstack11l11l1l1l_opy_():
  bstack1lll1ll_opy_ = bstack11l1lll111_opy_()
  if not os.path.exists(bstack1lll1ll_opy_):
    bstack11l1lll11l_opy_(
      bstack1ll1111l1l_opy_.format(os.getcwd()))
  try:
    with open(bstack1lll1ll_opy_, bstack11l1l11_opy_ (u"ࠪࡶࣦࠬ")) as stream:
      yaml.add_implicit_resolver(bstack11l1l11_opy_ (u"ࠦࠦࡶࡡࡵࡪࡨࡼࠧࣧ"), bstack1ll111l1ll_opy_)
      yaml.add_constructor(bstack11l1l11_opy_ (u"ࠧࠧࡰࡢࡶ࡫ࡩࡽࠨࣨ"), bstack1ll11l1ll1_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      bstack11lll111_opy_(config)
      return config
  except:
    with open(bstack1lll1ll_opy_, bstack11l1l11_opy_ (u"࠭ࡲࠨࣩ")) as stream:
      try:
        config = yaml.safe_load(stream)
        bstack11lll111_opy_(config)
        return config
      except yaml.YAMLError as exc:
        bstack11l1lll11l_opy_(bstack1llllll11l_opy_.format(str(exc)))
def bstack11111llll_opy_(config):
  bstack111lllll1_opy_ = bstack1lllll1ll_opy_(config)
  for option in list(bstack111lllll1_opy_):
    if option.lower() in bstack11l1111l11_opy_ and option != bstack11l1111l11_opy_[option.lower()]:
      bstack111lllll1_opy_[bstack11l1111l11_opy_[option.lower()]] = bstack111lllll1_opy_[option]
      del bstack111lllll1_opy_[option]
  return config
def bstack11l11111ll_opy_():
  global bstack11ll111111_opy_
  for key, bstack1lll1lllll_opy_ in bstack11ll1l11l_opy_.items():
    if isinstance(bstack1lll1lllll_opy_, list):
      for var in bstack1lll1lllll_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack11ll111111_opy_[key] = os.environ[var]
          break
    elif bstack1lll1lllll_opy_ in os.environ and os.environ[bstack1lll1lllll_opy_] and str(os.environ[bstack1lll1lllll_opy_]).strip():
      bstack11ll111111_opy_[key] = os.environ[bstack1lll1lllll_opy_]
  if bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩ࣪") in os.environ:
    bstack11ll111111_opy_[bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ࣫")] = {}
    bstack11ll111111_opy_[bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭࣬")][bstack11l1l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ࣭ࠬ")] = os.environ[bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࣮࠭")]
def bstack1ll11l1l1l_opy_():
  global bstack11l1lll11_opy_
  global bstack1ll111l11l_opy_
  global bstack1l11lllll1_opy_
  bstack1l1lll1l11_opy_ = []
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) - 1 and bstack11l1l11_opy_ (u"ࠬ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ࣯").lower() == val.lower():
      bstack11l1lll11_opy_[bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࣰࠪ")] = {}
      bstack11l1lll11_opy_[bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࣱࠫ")][bstack11l1l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࣲࠪ")] = sys.argv[idx + 1]
      bstack1l1lll1l11_opy_.extend([idx, idx + 1])
      break
  for key, bstack1l11111l1l_opy_ in bstack11l111ll_opy_.items():
    if isinstance(bstack1l11111l1l_opy_, list):
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        for var in bstack1l11111l1l_opy_:
          if bstack11l1l11_opy_ (u"ࠩ࠰࠱ࠬࣳ") + var.lower() == val.lower() and key not in bstack11l1lll11_opy_:
            bstack11l1lll11_opy_[key] = sys.argv[idx + 1]
            bstack1ll111l11l_opy_ += bstack11l1l11_opy_ (u"ࠪࠤ࠲࠳ࠧࣴ") + var + bstack11l1l11_opy_ (u"ࠫࠥ࠭ࣵ") + shlex.quote(sys.argv[idx + 1])
            bstack11l11l111l_opy_(bstack1l11lllll1_opy_, key, sys.argv[idx + 1])
            bstack1l1lll1l11_opy_.extend([idx, idx + 1])
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        if bstack11l1l11_opy_ (u"ࠬ࠳࠭ࠨࣶ") + bstack1l11111l1l_opy_.lower() == val.lower() and key not in bstack11l1lll11_opy_:
          bstack11l1lll11_opy_[key] = sys.argv[idx + 1]
          bstack1ll111l11l_opy_ += bstack11l1l11_opy_ (u"࠭ࠠ࠮࠯ࠪࣷ") + bstack1l11111l1l_opy_ + bstack11l1l11_opy_ (u"ࠧࠡࠩࣸ") + shlex.quote(sys.argv[idx + 1])
          bstack11l11l111l_opy_(bstack1l11lllll1_opy_, key, sys.argv[idx + 1])
          bstack1l1lll1l11_opy_.extend([idx, idx + 1])
  for idx in sorted(set(bstack1l1lll1l11_opy_), reverse=True):
    if idx < len(sys.argv):
      del sys.argv[idx]
def bstack111111111_opy_(config):
  bstack1llll111_opy_ = config.keys()
  for bstack1ll1lll1l1_opy_, bstack11ll1l1l_opy_ in bstack11ll111l_opy_.items():
    if bstack11ll1l1l_opy_ in bstack1llll111_opy_:
      config[bstack1ll1lll1l1_opy_] = config[bstack11ll1l1l_opy_]
      del config[bstack11ll1l1l_opy_]
  for bstack1ll1lll1l1_opy_, bstack11ll1l1l_opy_ in bstack1l1l11l1l_opy_.items():
    if isinstance(bstack11ll1l1l_opy_, list):
      for bstack1l1l11ll_opy_ in bstack11ll1l1l_opy_:
        if bstack1l1l11ll_opy_ in bstack1llll111_opy_:
          config[bstack1ll1lll1l1_opy_] = config[bstack1l1l11ll_opy_]
          del config[bstack1l1l11ll_opy_]
          break
    elif bstack11ll1l1l_opy_ in bstack1llll111_opy_:
      config[bstack1ll1lll1l1_opy_] = config[bstack11ll1l1l_opy_]
      del config[bstack11ll1l1l_opy_]
  for bstack1l1l11ll_opy_ in list(config):
    for bstack1111l1ll_opy_ in bstack1l1l111l_opy_:
      if bstack1l1l11ll_opy_.lower() == bstack1111l1ll_opy_.lower() and bstack1l1l11ll_opy_ != bstack1111l1ll_opy_:
        config[bstack1111l1ll_opy_] = config[bstack1l1l11ll_opy_]
        del config[bstack1l1l11ll_opy_]
  bstack11l1111l1l_opy_ = [{}]
  if not config.get(bstack11l1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࣹࠫ")):
    config[bstack11l1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࣺࠬ")] = [{}]
  bstack11l1111l1l_opy_ = config[bstack11l1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣻ")]
  for platform in bstack11l1111l1l_opy_:
    for bstack1l1l11ll_opy_ in list(platform):
      for bstack1111l1ll_opy_ in bstack1l1l111l_opy_:
        if bstack1l1l11ll_opy_.lower() == bstack1111l1ll_opy_.lower() and bstack1l1l11ll_opy_ != bstack1111l1ll_opy_:
          platform[bstack1111l1ll_opy_] = platform[bstack1l1l11ll_opy_]
          del platform[bstack1l1l11ll_opy_]
  for bstack1ll1lll1l1_opy_, bstack11ll1l1l_opy_ in bstack1l1l11l1l_opy_.items():
    for platform in bstack11l1111l1l_opy_:
      if isinstance(bstack11ll1l1l_opy_, list):
        for bstack1l1l11ll_opy_ in bstack11ll1l1l_opy_:
          if bstack1l1l11ll_opy_ in platform:
            platform[bstack1ll1lll1l1_opy_] = platform[bstack1l1l11ll_opy_]
            del platform[bstack1l1l11ll_opy_]
            break
      elif bstack11ll1l1l_opy_ in platform:
        platform[bstack1ll1lll1l1_opy_] = platform[bstack11ll1l1l_opy_]
        del platform[bstack11ll1l1l_opy_]
  for bstack1l11l1ll_opy_ in bstack1lll1l11ll_opy_:
    if bstack1l11l1ll_opy_ in config:
      if not bstack1lll1l11ll_opy_[bstack1l11l1ll_opy_] in config:
        config[bstack1lll1l11ll_opy_[bstack1l11l1ll_opy_]] = {}
      config[bstack1lll1l11ll_opy_[bstack1l11l1ll_opy_]].update(config[bstack1l11l1ll_opy_])
      del config[bstack1l11l1ll_opy_]
  for platform in bstack11l1111l1l_opy_:
    for bstack1l11l1ll_opy_ in bstack1lll1l11ll_opy_:
      if bstack1l11l1ll_opy_ in list(platform):
        if not bstack1lll1l11ll_opy_[bstack1l11l1ll_opy_] in platform:
          platform[bstack1lll1l11ll_opy_[bstack1l11l1ll_opy_]] = {}
        platform[bstack1lll1l11ll_opy_[bstack1l11l1ll_opy_]].update(platform[bstack1l11l1ll_opy_])
        del platform[bstack1l11l1ll_opy_]
  config = bstack11111llll_opy_(config)
  return config
def bstack1111111l1_opy_(config):
  global bstack1l1l1l1ll1_opy_
  bstack1111l111l_opy_ = False
  if bstack11l1l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨࣼ") in config and str(config[bstack11l1l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩࣽ")]).lower() != bstack11l1l11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬࣾ"):
    if bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫࣿ") not in config or str(config[bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬऀ")]).lower() == bstack11l1l11_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨँ"):
      config[bstack11l1l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩं")] = False
    else:
      bstack1l11lllll_opy_ = bstack1l1l1ll11l_opy_()
      if bstack11l1l11_opy_ (u"ࠫ࡮ࡹࡔࡳ࡫ࡤࡰࡌࡸࡩࡥࠩः") in bstack1l11lllll_opy_:
        if not bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩऄ") in config:
          config[bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪअ")] = {}
        config[bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫआ")][bstack11l1l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪइ")] = bstack11l1l11_opy_ (u"ࠩࡤࡸࡸ࠳ࡲࡦࡲࡨࡥࡹ࡫ࡲࠨई")
        bstack1111l111l_opy_ = True
        bstack1l1l1l1ll1_opy_ = config[bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧउ")].get(bstack11l1l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ऊ"))
  if bstack1lll1l1l_opy_(config) and bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩऋ") in config and str(config[bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪऌ")]).lower() != bstack11l1l11_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ऍ") and not bstack1111l111l_opy_:
    if not bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬऎ") in config:
      config[bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ए")] = {}
    if not config[bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧऐ")].get(bstack11l1l11_opy_ (u"ࠫࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠨऑ")) and not bstack11l1l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऒ") in config[bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪओ")]:
      current_time = datetime.datetime.now()
      bstack111l1llll1_opy_ = current_time.strftime(bstack11l1l11_opy_ (u"ࠧࠦࡦࡢࠩࡧࡥࠥࡉࠧࡐࠫऔ"))
      hostname = socket.gethostname()
      bstack11l1111ll_opy_ = bstack11l1l11_opy_ (u"ࠨࠩक").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack11l1l11_opy_ (u"ࠩࡾࢁࡤࢁࡽࡠࡽࢀࠫख").format(bstack111l1llll1_opy_, hostname, bstack11l1111ll_opy_)
      config[bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧग")][bstack11l1l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭घ")] = identifier
    bstack1l1l1l1ll1_opy_ = config[bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩङ")].get(bstack11l1l11_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨच"))
  return config
def bstack1ll111l11_opy_():
  bstack1llll1ll1l_opy_ =  bstack1l111l1lll_opy_()[bstack11l1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷ࠭छ")]
  return bstack1llll1ll1l_opy_ if bstack1llll1ll1l_opy_ else -1
def bstack1l11l11ll1_opy_(bstack1llll1ll1l_opy_):
  global CONFIG
  if not bstack11l1l11_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪज") in CONFIG[bstack11l1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫझ")]:
    return
  CONFIG[bstack11l1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬञ")] = CONFIG[bstack11l1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ट")].replace(
    bstack11l1l11_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧठ"),
    str(bstack1llll1ll1l_opy_)
  )
def bstack11ll1111l_opy_():
  global CONFIG
  if not bstack11l1l11_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬड") in CONFIG[bstack11l1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩढ")]:
    return
  current_time = datetime.datetime.now()
  bstack111l1llll1_opy_ = current_time.strftime(bstack11l1l11_opy_ (u"ࠨࠧࡧ࠱ࠪࡨ࠭ࠦࡊ࠽ࠩࡒ࠭ण"))
  CONFIG[bstack11l1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫत")] = CONFIG[bstack11l1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬथ")].replace(
    bstack11l1l11_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪद"),
    bstack111l1llll1_opy_
  )
def bstack1l11l1ll11_opy_():
  global CONFIG
  if bstack11l1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧध") in CONFIG and not bool(CONFIG[bstack11l1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨन")]):
    del CONFIG[bstack11l1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऩ")]
    return
  if not bstack11l1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪप") in CONFIG:
    CONFIG[bstack11l1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫफ")] = bstack11l1l11_opy_ (u"ࠪࠧࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ब")
  if bstack11l1l11_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪभ") in CONFIG[bstack11l1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧम")]:
    bstack11ll1111l_opy_()
    os.environ[bstack11l1l11_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪय")] = CONFIG[bstack11l1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩर")]
  if not bstack11l1l11_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪऱ") in CONFIG[bstack11l1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫल")]:
    return
  bstack1llll1ll1l_opy_ = bstack11l1l11_opy_ (u"ࠪࠫळ")
  bstack1l11llll1l_opy_ = bstack1ll111l11_opy_()
  if bstack1l11llll1l_opy_ != -1:
    bstack1llll1ll1l_opy_ = bstack11l1l11_opy_ (u"ࠫࡈࡏࠠࠨऴ") + str(bstack1l11llll1l_opy_)
  if bstack1llll1ll1l_opy_ == bstack11l1l11_opy_ (u"ࠬ࠭व"):
    bstack111lllll_opy_ = bstack1ll11ll111_opy_(CONFIG[bstack11l1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩश")])
    if bstack111lllll_opy_ != -1:
      bstack1llll1ll1l_opy_ = str(bstack111lllll_opy_)
  if bstack1llll1ll1l_opy_:
    bstack1l11l11ll1_opy_(bstack1llll1ll1l_opy_)
    os.environ[bstack11l1l11_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫष")] = CONFIG[bstack11l1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪस")]
def bstack111l11lll_opy_(bstack1l1lllll1_opy_, bstack1l111lll_opy_, path):
  bstack1l1lll1ll_opy_ = {
    bstack11l1l11_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ह"): bstack1l111lll_opy_
  }
  if os.path.exists(path):
    bstack11lll1l1l1_opy_ = json.load(open(path, bstack11l1l11_opy_ (u"ࠪࡶࡧ࠭ऺ")))
  else:
    bstack11lll1l1l1_opy_ = {}
  bstack11lll1l1l1_opy_[bstack1l1lllll1_opy_] = bstack1l1lll1ll_opy_
  with open(path, bstack11l1l11_opy_ (u"ࠦࡼ࠱ࠢऻ")) as outfile:
    json.dump(bstack11lll1l1l1_opy_, outfile)
def bstack1ll11ll111_opy_(bstack1l1lllll1_opy_):
  bstack1l1lllll1_opy_ = str(bstack1l1lllll1_opy_)
  bstack111l1ll1l1_opy_ = os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"ࠬࢄ़ࠧ")), bstack11l1l11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ऽ"))
  try:
    if not os.path.exists(bstack111l1ll1l1_opy_):
      os.makedirs(bstack111l1ll1l1_opy_)
    file_path = os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"ࠧࡿࠩा")), bstack11l1l11_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨि"), bstack11l1l11_opy_ (u"ࠩ࠱ࡦࡺ࡯࡬ࡥ࠯ࡱࡥࡲ࡫࠭ࡤࡣࡦ࡬ࡪ࠴ࡪࡴࡱࡱࠫी"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack11l1l11_opy_ (u"ࠪࡻࠬु")):
        pass
      with open(file_path, bstack11l1l11_opy_ (u"ࠦࡼ࠱ࠢू")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack11l1l11_opy_ (u"ࠬࡸࠧृ")) as bstack1l1l111ll_opy_:
      bstack1lllll11ll_opy_ = json.load(bstack1l1l111ll_opy_)
    if bstack1l1lllll1_opy_ in bstack1lllll11ll_opy_:
      bstack11l111l111_opy_ = bstack1lllll11ll_opy_[bstack1l1lllll1_opy_][bstack11l1l11_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪॄ")]
      bstack1l1ll11111_opy_ = int(bstack11l111l111_opy_) + 1
      bstack111l11lll_opy_(bstack1l1lllll1_opy_, bstack1l1ll11111_opy_, file_path)
      return bstack1l1ll11111_opy_
    else:
      bstack111l11lll_opy_(bstack1l1lllll1_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warning(bstack1111l1lll_opy_.format(str(e)))
    return -1
def bstack11llll1l11_opy_(config):
  if not config[bstack11l1l11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩॅ")] or not config[bstack11l1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫॆ")]:
    return True
  else:
    return False
def bstack1lll1l11l_opy_(config, index=0):
  global bstack1l11ll1ll1_opy_
  bstack1l1l11l1_opy_ = {}
  caps = bstack11ll11l1ll_opy_ + bstack1llll1ll_opy_
  if config.get(bstack11l1l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭े"), False):
    bstack1l1l11l1_opy_[bstack11l1l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧै")] = True
    bstack1l1l11l1_opy_[bstack11l1l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࡐࡲࡷ࡭ࡴࡴࡳࠨॉ")] = config.get(bstack11l1l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩॊ"), {})
  if bstack1l11ll1ll1_opy_:
    caps += bstack1lllllllll_opy_
  for key in config:
    if key in caps + [bstack11l1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩो")]:
      continue
    bstack1l1l11l1_opy_[key] = config[key]
  if bstack11l1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪौ") in config:
    for bstack1l1l11ll1l_opy_ in config[bstack11l1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶ्ࠫ")][index]:
      if bstack1l1l11ll1l_opy_ in caps:
        continue
      bstack1l1l11l1_opy_[bstack1l1l11ll1l_opy_] = config[bstack11l1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॎ")][index][bstack1l1l11ll1l_opy_]
  bstack1l1l11l1_opy_[bstack11l1l11_opy_ (u"ࠪ࡬ࡴࡹࡴࡏࡣࡰࡩࠬॏ")] = socket.gethostname()
  if bstack11l1l11_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬॐ") in bstack1l1l11l1_opy_:
    del (bstack1l1l11l1_opy_[bstack11l1l11_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭॑")])
  return bstack1l1l11l1_opy_
def bstack11l11l1l1_opy_(config):
  global bstack1l11ll1ll1_opy_
  bstack11l1ll1l11_opy_ = {}
  caps = bstack1llll1ll_opy_
  if bstack1l11ll1ll1_opy_:
    caps += bstack1lllllllll_opy_
  for key in caps:
    if key in config:
      bstack11l1ll1l11_opy_[key] = config[key]
  return bstack11l1ll1l11_opy_
def bstack11l1111ll1_opy_(bstack1l1l11l1_opy_, bstack11l1ll1l11_opy_):
  bstack111ll1l1l_opy_ = {}
  for key in bstack1l1l11l1_opy_.keys():
    if key in bstack11ll111l_opy_:
      bstack111ll1l1l_opy_[bstack11ll111l_opy_[key]] = bstack1l1l11l1_opy_[key]
    else:
      bstack111ll1l1l_opy_[key] = bstack1l1l11l1_opy_[key]
  for key in bstack11l1ll1l11_opy_:
    if key in bstack11ll111l_opy_:
      bstack111ll1l1l_opy_[bstack11ll111l_opy_[key]] = bstack11l1ll1l11_opy_[key]
    else:
      bstack111ll1l1l_opy_[key] = bstack11l1ll1l11_opy_[key]
  return bstack111ll1l1l_opy_
def bstack11l11ll11l_opy_(config, index=0):
  global bstack1l11ll1ll1_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack11lll1ll_opy_ = bstack1l1ll1111_opy_(bstack11l111ll1l_opy_, config, logger)
  bstack11l1ll1l11_opy_ = bstack11l11l1l1_opy_(config)
  bstack11ll11111l_opy_ = bstack1llll1ll_opy_
  bstack11ll11111l_opy_ += bstack1l1ll11l11_opy_
  bstack11l1ll1l11_opy_ = update(bstack11l1ll1l11_opy_, bstack11lll1ll_opy_)
  if bstack1l11ll1ll1_opy_:
    bstack11ll11111l_opy_ += bstack1lllllllll_opy_
  if bstack11l1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴ॒ࠩ") in config:
    if bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ॓") in config[bstack11l1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ॔")][index]:
      caps[bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧॕ")] = config[bstack11l1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॖ")][index][bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩॗ")]
    if bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭क़") in config[bstack11l1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩख़")][index]:
      caps[bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨग़")] = str(config[bstack11l1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫज़")][index][bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪड़")])
    bstack1l1lllll_opy_ = bstack1l1ll1111_opy_(bstack11l111ll1l_opy_, config[bstack11l1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ढ़")][index], logger)
    bstack11ll11111l_opy_ += list(bstack1l1lllll_opy_.keys())
    for bstack1lll1111l1_opy_ in bstack11ll11111l_opy_:
      if bstack1lll1111l1_opy_ in config[bstack11l1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧफ़")][index]:
        if bstack1lll1111l1_opy_ == bstack11l1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧय़"):
          try:
            bstack1l1lllll_opy_[bstack1lll1111l1_opy_] = str(config[bstack11l1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩॠ")][index][bstack1lll1111l1_opy_] * 1.0)
          except:
            bstack1l1lllll_opy_[bstack1lll1111l1_opy_] = str(config[bstack11l1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪॡ")][index][bstack1lll1111l1_opy_])
        else:
          bstack1l1lllll_opy_[bstack1lll1111l1_opy_] = config[bstack11l1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫॢ")][index][bstack1lll1111l1_opy_]
        del (config[bstack11l1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॣ")][index][bstack1lll1111l1_opy_])
    bstack11l1ll1l11_opy_ = update(bstack11l1ll1l11_opy_, bstack1l1lllll_opy_)
  bstack1l1l11l1_opy_ = bstack1lll1l11l_opy_(config, index)
  for bstack1l1l11ll_opy_ in bstack1llll1ll_opy_ + list(bstack11lll1ll_opy_.keys()):
    if bstack1l1l11ll_opy_ in bstack1l1l11l1_opy_:
      bstack11l1ll1l11_opy_[bstack1l1l11ll_opy_] = bstack1l1l11l1_opy_[bstack1l1l11ll_opy_]
      del (bstack1l1l11l1_opy_[bstack1l1l11ll_opy_])
  if bstack11ll1l1l1l_opy_(config):
    bstack1l1l11l1_opy_[bstack11l1l11_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ।")] = True
    caps.update(bstack11l1ll1l11_opy_)
    caps[bstack11l1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ॥")] = bstack1l1l11l1_opy_
  else:
    bstack1l1l11l1_opy_[bstack11l1l11_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ०")] = False
    caps.update(bstack11l1111ll1_opy_(bstack1l1l11l1_opy_, bstack11l1ll1l11_opy_))
    if bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ१") in caps:
      caps[bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ२")] = caps[bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭३")]
      del (caps[bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ४")])
    if bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ५") in caps:
      caps[bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭६")] = caps[bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭७")]
      del (caps[bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ८")])
  return caps
def bstack1l11111111_opy_():
  global bstack1l1l11ll11_opy_
  global CONFIG
  if bstack1l1l11ll11_opy_ != bstack11l1l11_opy_ (u"ࠧࠨ९") and (bstack1l1l11ll11_opy_.startswith(bstack11l1l11_opy_ (u"ࠨࡪࡷࡸࡵࡀ࠯࠰ࠩ॰")) or bstack1l1l11ll11_opy_.startswith(bstack11l1l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠫॱ"))):
    return bstack1l1l11ll11_opy_
  if bstack1l1ll1111l_opy_() <= version.parse(bstack11l1l11_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪॲ")):
    if bstack1l1l11ll11_opy_ != bstack11l1l11_opy_ (u"ࠫࠬॳ"):
      return bstack11l1l11_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨॴ") + bstack1l1l11ll11_opy_ + bstack11l1l11_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥॵ")
    return bstack11ll1l1l11_opy_
  if bstack1l1l11ll11_opy_ != bstack11l1l11_opy_ (u"ࠧࠨॶ"):
    return bstack11l1l11_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥॷ") + bstack1l1l11ll11_opy_ + bstack11l1l11_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥॸ")
  return HTTPS_HUB
def bstack1l11l111l_opy_(options):
  return hasattr(options, bstack11l1l11_opy_ (u"ࠪࡷࡪࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠫॹ"))
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
def bstack111lll1l_opy_(options, bstack1ll1111lll_opy_):
  for bstack1l1111llll_opy_ in bstack1ll1111lll_opy_:
    if bstack1l1111llll_opy_ in [bstack11l1l11_opy_ (u"ࠫࡦࡸࡧࡴࠩॺ"), bstack11l1l11_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩॻ")]:
      continue
    if bstack1l1111llll_opy_ in options._experimental_options:
      options._experimental_options[bstack1l1111llll_opy_] = update(options._experimental_options[bstack1l1111llll_opy_],
                                                         bstack1ll1111lll_opy_[bstack1l1111llll_opy_])
    else:
      options.add_experimental_option(bstack1l1111llll_opy_, bstack1ll1111lll_opy_[bstack1l1111llll_opy_])
  if bstack11l1l11_opy_ (u"࠭ࡡࡳࡩࡶࠫॼ") in bstack1ll1111lll_opy_:
    for arg in bstack1ll1111lll_opy_[bstack11l1l11_opy_ (u"ࠧࡢࡴࡪࡷࠬॽ")]:
      options.add_argument(arg)
    del (bstack1ll1111lll_opy_[bstack11l1l11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ॾ")])
  if bstack11l1l11_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ॿ") in bstack1ll1111lll_opy_:
    for ext in bstack1ll1111lll_opy_[bstack11l1l11_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧঀ")]:
      try:
        options.add_extension(ext)
      except OSError:
        options.add_encoded_extension(ext)
    del (bstack1ll1111lll_opy_[bstack11l1l11_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨঁ")])
def bstack111ll1l11_opy_(options):
  bstack11l1l11_opy_ (u"ࠧࠨࠢࠋࠢࠣࡍࡳࡰࡥࡤࡶࠣࡨࡪ࡬ࡡࡶ࡮ࡷࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡴࡶࡴࡪࡱࡱࡷࠥ࡬࡯ࡳࠢ࡯ࡳࡦࡪࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡹ࡫ࡩࡳࠦ࡯ࡷࡧࡵࡶ࡮ࡪࡥࡍࡱࡤࡨ࡙࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡧࡱࡥࡧࡲࡥࡥ࠰ࠍࠤࠥࡊࡥࡧࡧࡱࡷ࡮ࡼࡥ࠻ࠢࡱࡩࡻ࡫ࡲࠡࡱࡹࡩࡷࡽࡲࡪࡶࡨࡷࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠࡢࡴࡪࡷ࠱ࠦ࡯࡯࡮ࡼࠤࡦࡪࡤࡴࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡳࡳ࡫ࡳ࠯ࠌࠣࠤࡘ࡯࡭ࡪ࡮ࡤࡶࠥࡺ࡯ࠡࡌࡤࡺࡦࠦࡓࡅࡍࠪࡷࠥࡕࡶࡦࡴࡵ࡭ࡩ࡫ࡌࡰࡣࡧࡘࡪࡹࡴࡪࡰࡪࡇ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࡋࡩࡱࡶࡥࡳ࠰ࠍࠤ࡚ࠥࡨࡪࡵࠣ࡭ࡸࠦࡡࠡࡹࡵࡥࡵࡶࡥࡳࠢࡤࡶࡴࡻ࡮ࡥࠢࡷ࡬ࡪࠦࡣࡦࡰࡷࡶࡦࡲࡩࡻࡧࡧࠤ࡭࡫࡬ࡱࡧࡵࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠥࠦࠧং")
  global CONFIG
  global bstack111ll1llll_opy_
  try:
    if not bstack111ll1llll_opy_ or not options:
      return options
    from bstack_utils.bstack111l1lll11_opy_ import bstack1ll11111_opy_
    bstack11l1l1lll_opy_ = bstack1ll11111_opy_(options, bstack1lll1ll11_opy_=bstack11l1l11_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࠨঃ"))
    if bstack11l1l1lll_opy_ > 0:
      logger.debug(bstack11l1l11_opy_ (u"ࠢࡍࡱࡤࡨࠥࡺࡥࡴࡶ࡬ࡲ࡬ࡀࠠࡂࡦࡧࡩࡩࠦࡻࡾࠢࡧࡩ࡫ࡧࡵ࡭ࡶࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠦࡦࡰࡴࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧࠥ঄").format(bstack11l1l1lll_opy_))
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡮ࡴࡪࡦࡥࡷࠤࡱࡵࡡࡥࠢࡷࡩࡸࡺࡩ࡯ࡩࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࢁࡽࠣঅ").format(e))
  return options
def bstack1lll11111_opy_(options, bstack111l1l11l_opy_):
  if bstack11l1l11_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨআ") in bstack111l1l11l_opy_:
    for bstack1111llll_opy_ in bstack111l1l11l_opy_[bstack11l1l11_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩই")]:
      if bstack1111llll_opy_ in options._preferences:
        options._preferences[bstack1111llll_opy_] = update(options._preferences[bstack1111llll_opy_], bstack111l1l11l_opy_[bstack11l1l11_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪঈ")][bstack1111llll_opy_])
      else:
        options.set_preference(bstack1111llll_opy_, bstack111l1l11l_opy_[bstack11l1l11_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫউ")][bstack1111llll_opy_])
  if bstack11l1l11_opy_ (u"࠭ࡡࡳࡩࡶࠫঊ") in bstack111l1l11l_opy_:
    for arg in bstack111l1l11l_opy_[bstack11l1l11_opy_ (u"ࠧࡢࡴࡪࡷࠬঋ")]:
      options.add_argument(arg)
def bstack11ll11ll1l_opy_(options, bstack1l111l1l_opy_):
  if bstack11l1l11_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࠩঌ") in bstack1l111l1l_opy_:
    options.use_webview(bool(bstack1l111l1l_opy_[bstack11l1l11_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࠪ঍")]))
  bstack111lll1l_opy_(options, bstack1l111l1l_opy_)
def bstack1llllll11_opy_(options, bstack1l111111l1_opy_):
  for bstack11l1l1l1ll_opy_ in bstack1l111111l1_opy_:
    if bstack11l1l1l1ll_opy_ in [bstack11l1l11_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧ঎"), bstack11l1l11_opy_ (u"ࠫࡦࡸࡧࡴࠩএ")]:
      continue
    options.set_capability(bstack11l1l1l1ll_opy_, bstack1l111111l1_opy_[bstack11l1l1l1ll_opy_])
  if bstack11l1l11_opy_ (u"ࠬࡧࡲࡨࡵࠪঐ") in bstack1l111111l1_opy_:
    for arg in bstack1l111111l1_opy_[bstack11l1l11_opy_ (u"࠭ࡡࡳࡩࡶࠫ঑")]:
      options.add_argument(arg)
  if bstack11l1l11_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫ঒") in bstack1l111111l1_opy_:
    options.bstack11ll1l11_opy_(bool(bstack1l111111l1_opy_[bstack11l1l11_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬও")]))
def bstack1lll11l11_opy_(options, bstack1111l11l_opy_):
  for bstack111l1ll111_opy_ in bstack1111l11l_opy_:
    if bstack111l1ll111_opy_ in [bstack11l1l11_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ঔ"), bstack11l1l11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨক")]:
      continue
    options._options[bstack111l1ll111_opy_] = bstack1111l11l_opy_[bstack111l1ll111_opy_]
  if bstack11l1l11_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨখ") in bstack1111l11l_opy_:
    for bstack1llll1ll11_opy_ in bstack1111l11l_opy_[bstack11l1l11_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩগ")]:
      options.bstack111lllllll_opy_(
        bstack1llll1ll11_opy_, bstack1111l11l_opy_[bstack11l1l11_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪঘ")][bstack1llll1ll11_opy_])
  if bstack11l1l11_opy_ (u"ࠧࡢࡴࡪࡷࠬঙ") in bstack1111l11l_opy_:
    for arg in bstack1111l11l_opy_[bstack11l1l11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭চ")]:
      options.add_argument(arg)
def bstack1l1l111lll_opy_(options, caps):
  if not hasattr(options, bstack11l1l11_opy_ (u"ࠩࡎࡉ࡞࠭ছ")):
    return
  if options.KEY == bstack11l1l11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨজ"):
    options = bstack1l111ll111_opy_.bstack1ll1ll1l11_opy_(bstack11llllll_opy_=options, config=CONFIG)
  if options.KEY == bstack11l1l11_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩঝ") and options.KEY in caps:
    bstack111lll1l_opy_(options, caps[bstack11l1l11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪঞ")])
  elif options.KEY == bstack11l1l11_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫট") and options.KEY in caps:
    bstack1lll11111_opy_(options, caps[bstack11l1l11_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬঠ")])
  elif options.KEY == bstack11l1l11_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩড") and options.KEY in caps:
    bstack1llllll11_opy_(options, caps[bstack11l1l11_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪঢ")])
  elif options.KEY == bstack11l1l11_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫণ") and options.KEY in caps:
    bstack11ll11ll1l_opy_(options, caps[bstack11l1l11_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬত")])
  elif options.KEY == bstack11l1l11_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫথ") and options.KEY in caps:
    bstack1lll11l11_opy_(options, caps[bstack11l1l11_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬদ")])
def bstack11ll1l11ll_opy_(caps):
  global bstack1l11ll1ll1_opy_
  if isinstance(os.environ.get(bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨধ")), str):
    bstack1l11ll1ll1_opy_ = eval(os.getenv(bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩন")))
  if bstack1l11ll1ll1_opy_:
    if bstack1l11lll1l1_opy_() < version.parse(bstack11l1l11_opy_ (u"ࠩ࠵࠲࠸࠴࠰ࠨ঩")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack11l1l11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪপ")
    if bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩফ") in caps:
      browser = caps[bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪব")]
    elif bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧভ") in caps:
      browser = caps[bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨম")]
    browser = str(browser).lower()
    if browser == bstack11l1l11_opy_ (u"ࠨ࡫ࡳ࡬ࡴࡴࡥࠨয") or browser == bstack11l1l11_opy_ (u"ࠩ࡬ࡴࡦࡪࠧর"):
      browser = bstack11l1l11_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪ঱")
    if browser == bstack11l1l11_opy_ (u"ࠫࡸࡧ࡭ࡴࡷࡱ࡫ࠬল"):
      browser = bstack11l1l11_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬ঳")
    if browser not in [bstack11l1l11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭঴"), bstack11l1l11_opy_ (u"ࠧࡦࡦࡪࡩࠬ঵"), bstack11l1l11_opy_ (u"ࠨ࡫ࡨࠫশ"), bstack11l1l11_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩষ"), bstack11l1l11_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫস")]:
      return None
    try:
      package = bstack11l1l11_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳ࠰ࡾࢁ࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭হ").format(browser)
      name = bstack11l1l11_opy_ (u"ࠬࡕࡰࡵ࡫ࡲࡲࡸ࠭঺")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1l11l111l_opy_(options):
        return None
      for bstack1l1l11ll_opy_ in caps.keys():
        options.set_capability(bstack1l1l11ll_opy_, caps[bstack1l1l11ll_opy_])
      bstack1l1l111lll_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1ll11111ll_opy_(options, bstack11ll11llll_opy_):
  if not bstack1l11l111l_opy_(options):
    return
  for bstack1l1l11ll_opy_ in bstack11ll11llll_opy_.keys():
    if bstack1l1l11ll_opy_ in bstack1l1ll11l11_opy_:
      continue
    if bstack1l1l11ll_opy_ in options._caps and type(options._caps[bstack1l1l11ll_opy_]) in [dict, list]:
      options._caps[bstack1l1l11ll_opy_] = update(options._caps[bstack1l1l11ll_opy_], bstack11ll11llll_opy_[bstack1l1l11ll_opy_])
    else:
      options.set_capability(bstack1l1l11ll_opy_, bstack11ll11llll_opy_[bstack1l1l11ll_opy_])
  bstack1l1l111lll_opy_(options, bstack11ll11llll_opy_)
  if bstack11l1l11_opy_ (u"࠭࡭ࡰࡼ࠽ࡨࡪࡨࡵࡨࡩࡨࡶࡆࡪࡤࡳࡧࡶࡷࠬ঻") in options._caps:
    if options._caps[bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩ়ࠬ")] and options._caps[bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ঽ")].lower() != bstack11l1l11_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪা"):
      del options._caps[bstack11l1l11_opy_ (u"ࠪࡱࡴࢀ࠺ࡥࡧࡥࡹ࡬࡭ࡥࡳࡃࡧࡨࡷ࡫ࡳࡴࠩি")]
def bstack1l11lll1_opy_(proxy_config):
  if bstack11l1l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨী") in proxy_config:
    proxy_config[bstack11l1l11_opy_ (u"ࠬࡹࡳ࡭ࡒࡵࡳࡽࡿࠧু")] = proxy_config[bstack11l1l11_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪূ")]
    del (proxy_config[bstack11l1l11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫৃ")])
  if bstack11l1l11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫৄ") in proxy_config and proxy_config[bstack11l1l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬ৅")].lower() != bstack11l1l11_opy_ (u"ࠪࡨ࡮ࡸࡥࡤࡶࠪ৆"):
    proxy_config[bstack11l1l11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧে")] = bstack11l1l11_opy_ (u"ࠬࡳࡡ࡯ࡷࡤࡰࠬৈ")
  if bstack11l1l11_opy_ (u"࠭ࡰࡳࡱࡻࡽࡆࡻࡴࡰࡥࡲࡲ࡫࡯ࡧࡖࡴ࡯ࠫ৉") in proxy_config:
    proxy_config[bstack11l1l11_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪ৊")] = bstack11l1l11_opy_ (u"ࠨࡲࡤࡧࠬো")
  return proxy_config
def bstack1l111lll1l_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack11l1l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨৌ") in config:
    return proxy
  config[bstack11l1l11_opy_ (u"ࠪࡴࡷࡵࡸࡺ্ࠩ")] = bstack1l11lll1_opy_(config[bstack11l1l11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪৎ")])
  if proxy == None:
    proxy = Proxy(config[bstack11l1l11_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ৏")])
  return proxy
def bstack1l1111l111_opy_(self):
  global CONFIG
  global bstack111l1ll11l_opy_
  try:
    proxy = bstack11lll1ll11_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack11l1l11_opy_ (u"࠭࠮ࡱࡣࡦࠫ৐")):
        proxies = bstack11ll11lll_opy_(proxy, bstack1l11111111_opy_())
        if len(proxies) > 0:
          protocol, bstack1llll11ll_opy_ = proxies.popitem()
          if bstack11l1l11_opy_ (u"ࠢ࠻࠱࠲ࠦ৑") in bstack1llll11ll_opy_:
            return bstack1llll11ll_opy_
          else:
            return bstack11l1l11_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ৒") + bstack1llll11ll_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack11l1l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡶࡲࡰࡺࡼࠤࡺࡸ࡬ࠡ࠼ࠣࡿࢂࠨ৓").format(str(e)))
  return bstack111l1ll11l_opy_(self)
def bstack111111l11_opy_():
  global CONFIG
  return bstack1l1llll1_opy_(CONFIG) and bstack1ll111l1l_opy_() and bstack1l1ll1111l_opy_() >= version.parse(bstack1lll11ll1l_opy_)
def bstack1ll1l1l1l1_opy_():
  global CONFIG
  return (bstack11l1l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭৔") in CONFIG or bstack11l1l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ৕") in CONFIG) and bstack11ll1111ll_opy_()
def bstack1lllll1ll_opy_(config):
  bstack111lllll1_opy_ = {}
  if bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ৖") in config:
    bstack111lllll1_opy_ = config[bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪৗ")]
  if bstack11l1l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭৘") in config:
    bstack111lllll1_opy_ = config[bstack11l1l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ৙")]
  proxy = bstack11lll1ll11_opy_(config)
  if proxy:
    if proxy.endswith(bstack11l1l11_opy_ (u"ࠩ࠱ࡴࡦࡩࠧ৚")) and os.path.isfile(proxy):
      bstack111lllll1_opy_[bstack11l1l11_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭৛")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack11l1l11_opy_ (u"ࠫ࠳ࡶࡡࡤࠩড়")):
        proxies = bstack1lll1l11l1_opy_(config, bstack1l11111111_opy_())
        if len(proxies) > 0:
          protocol, bstack1llll11ll_opy_ = proxies.popitem()
          if bstack11l1l11_opy_ (u"ࠧࡀ࠯࠰ࠤঢ়") in bstack1llll11ll_opy_:
            parsed_url = urlparse(bstack1llll11ll_opy_)
          else:
            parsed_url = urlparse(protocol + bstack11l1l11_opy_ (u"ࠨ࠺࠰࠱ࠥ৞") + bstack1llll11ll_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack111lllll1_opy_[bstack11l1l11_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪয়")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack111lllll1_opy_[bstack11l1l11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡰࡴࡷࠫৠ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack111lllll1_opy_[bstack11l1l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬৡ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack111lllll1_opy_[bstack11l1l11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭ৢ")] = str(parsed_url.password)
  return bstack111lllll1_opy_
def bstack1ll1lll1_opy_(config):
  if bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩৣ") in config:
    return config[bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪ৤")]
  return {}
def bstack1l1l11111l_opy_(caps):
  global bstack1l1l1l1ll1_opy_
  if bstack11l1l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ৥") in caps:
    caps[bstack11l1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ০")][bstack11l1l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧ১")] = True
    if bstack1l1l1l1ll1_opy_:
      caps[bstack11l1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ২")][bstack11l1l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ৩")] = bstack1l1l1l1ll1_opy_
  else:
    caps[bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩ৪")] = True
    if bstack1l1l1l1ll1_opy_:
      caps[bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭৫")] = bstack1l1l1l1ll1_opy_
@measure(event_name=EVENTS.bstack1l1llll1l1_opy_, stage=STAGE.bstack1l11l1l11l_opy_, bstack1l111l11l_opy_=bstack1ll1ll11l1_opy_)
def bstack11lll1lll1_opy_():
  global CONFIG
  if not bstack1lll1l1l_opy_(CONFIG) or cli.is_enabled(CONFIG):
    return
  if bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ৬") in CONFIG and bstack1lll1l111_opy_(CONFIG[bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ৭")]):
    if (
      bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ৮") in CONFIG
      and bstack1lll1l111_opy_(CONFIG[bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭৯")].get(bstack11l1l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡃ࡫ࡱࡥࡷࡿࡉ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡣࡷ࡭ࡴࡴࠧৰ")))
    ):
      logger.debug(bstack11l1l11_opy_ (u"ࠦࡑࡵࡣࡢ࡮ࠣࡦ࡮ࡴࡡࡳࡻࠣࡲࡴࡺࠠࡴࡶࡤࡶࡹ࡫ࡤࠡࡣࡶࠤࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤࡪࡴࡡࡣ࡮ࡨࡨࠧৱ"))
      return
    bstack111lllll1_opy_ = bstack1lllll1ll_opy_(CONFIG)
    bstack1111ll11_opy_(CONFIG[bstack11l1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ৲")], bstack111lllll1_opy_)
def bstack1111ll11_opy_(key, bstack111lllll1_opy_):
  global bstack1l11l11lll_opy_
  logger.info(bstack111l1lll_opy_)
  try:
    bstack1l11l11lll_opy_ = Local()
    bstack1ll1ll11ll_opy_ = {bstack11l1l11_opy_ (u"࠭࡫ࡦࡻࠪ৳"): key}
    bstack1ll1ll11ll_opy_.update(bstack111lllll1_opy_)
    logger.debug(bstack111ll1l111_opy_.format(str(bstack1ll1ll11ll_opy_)).replace(key, bstack11l1l11_opy_ (u"ࠧ࡜ࡔࡈࡈࡆࡉࡔࡆࡆࡠࠫ৴")))
    bstack1l11l11lll_opy_.start(**bstack1ll1ll11ll_opy_)
    if bstack1l11l11lll_opy_.isRunning():
      logger.info(bstack111l1111l_opy_)
  except Exception as e:
    bstack11l1lll11l_opy_(bstack1l1l11ll1_opy_.format(str(e)))
def bstack1lll11l1l1_opy_():
  global bstack1l11l11lll_opy_
  if bstack1l11l11lll_opy_.isRunning():
    logger.info(bstack11ll1111_opy_)
    bstack1l11l11lll_opy_.stop()
  bstack1l11l11lll_opy_ = None
def bstack111l11ll11_opy_(bstack1lll1llll_opy_=[]):
  global CONFIG
  bstack1l1lll111l_opy_ = []
  bstack1l11111l11_opy_ = [bstack11l1l11_opy_ (u"ࠨࡱࡶࠫ৵"), bstack11l1l11_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬ৶"), bstack11l1l11_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧ৷"), bstack11l1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭৸"), bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ৹"), bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ৺")]
  try:
    for err in bstack1lll1llll_opy_:
      bstack1llll111ll_opy_ = {}
      for k in bstack1l11111l11_opy_:
        val = CONFIG[bstack11l1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ৻")][int(err[bstack11l1l11_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧৼ")])].get(k)
        if val:
          bstack1llll111ll_opy_[k] = val
      if(err[bstack11l1l11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ৽")] != bstack11l1l11_opy_ (u"ࠪࠫ৾")):
        bstack1llll111ll_opy_[bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡵࠪ৿")] = {
          err[bstack11l1l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ਀")]: err[bstack11l1l11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬਁ")]
        }
        bstack1l1lll111l_opy_.append(bstack1llll111ll_opy_)
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡳࡷࡳࡡࡵࡶ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺ࠺ࠡࠩਂ") + str(e))
  finally:
    return bstack1l1lll111l_opy_
def bstack1l1l1llll_opy_(file_name):
  bstack1ll1ll1l1_opy_ = []
  try:
    bstack11ll1l111l_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack11ll1l111l_opy_):
      with open(bstack11ll1l111l_opy_) as f:
        bstack11ll11ll_opy_ = json.load(f)
        bstack1ll1ll1l1_opy_ = bstack11ll11ll_opy_
      os.remove(bstack11ll1l111l_opy_)
    return bstack1ll1ll1l1_opy_
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪ࡮ࡴࡤࡪࡰࡪࠤࡪࡸࡲࡰࡴࠣࡰ࡮ࡹࡴ࠻ࠢࠪਃ") + str(e))
    return bstack1ll1ll1l1_opy_
def bstack1ll1l11111_opy_():
  try:
      import time
      from bstack_utils.constants import bstack111l11lll1_opy_, EVENTS
      from bstack_utils.helper import bstack11l11llll_opy_, get_host_info, global_config
      from datetime import datetime
      from filelock import FileLock
      from bstack_utils.bstack111lll111l_opy_ import bstack11ll1l1l1_opy_
      bstack11ll1l1l1_opy_.bstack1111l11ll_opy_()
      bstack11l11l1111_opy_ = os.path.join(os.getcwd(), bstack11l1l11_opy_ (u"ࠩ࡯ࡳ࡬࠭਄"), bstack11l1l11_opy_ (u"ࠪ࡯ࡪࡿ࠭࡮ࡧࡷࡶ࡮ࡩࡳ࠯࡬ࡶࡳࡳ࠭ਅ"))
      data = None
      lock = FileLock(bstack11l11l1111_opy_+bstack11l1l11_opy_ (u"ࠦ࠳ࡲ࡯ࡤ࡭ࠥਆ"), timeout=2)
      try:
          with lock:
              with open(bstack11l11l1111_opy_, bstack11l1l11_opy_ (u"ࠧࡸࠢਇ"), encoding=bstack11l1l11_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧਈ")) as file:
                  data = json.load(file)
      except Exception as e:
          logger.debug(bstack11l1l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡶࡪࡧࡤࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࠦࡦࡪ࡮ࡨ࠾ࠥࢁࡽࠣਉ").format(e))
          return
      if not data:
          return
      def bstack1l1ll11lll_opy_():
          try:
              config = {
                  bstack11l1l11_opy_ (u"ࠣࡪࡨࡥࡩ࡫ࡲࡴࠤਊ"): {
                      bstack11l1l11_opy_ (u"ࠤࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠣ਋"): bstack11l1l11_opy_ (u"ࠥࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳࠨ਌"),
                  }
              }
              bstack1lll111l1l_opy_ = datetime.utcnow()
              current_time = bstack1lll111l1l_opy_.strftime(bstack11l1l11_opy_ (u"ࠦࠪ࡟࠭ࠦ࡯࠰ࠩࡩ࡚ࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࠯ࠧࡩࠤ࡚࡚ࡃࠣ਍"))
              bstack1l11l1lll_opy_ = os.environ.get(bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ਎")) if os.environ.get(bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫਏ")) else global_config.get_property(bstack11l1l11_opy_ (u"ࠢࡴࡦ࡮ࡖࡺࡴࡉࡥࠤਐ"))
              payload = {
                  bstack11l1l11_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠧ਑"): bstack11l1l11_opy_ (u"ࠤࡶࡨࡰࡥࡥࡷࡧࡱࡸࡸࠨ਒"),
                  bstack11l1l11_opy_ (u"ࠥࡨࡦࡺࡡࠣਓ"): {
                      bstack11l1l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡪࡸࡦࡤࡻࡵࡪࡦࠥਔ"): bstack1l11l1lll_opy_,
                      bstack11l1l11_opy_ (u"ࠧࡩࡲࡦࡣࡷࡩࡩࡥࡤࡢࡻࠥਕ"): current_time,
                      bstack11l1l11_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡴࡡ࡮ࡧࠥਖ"): bstack11l1l11_opy_ (u"ࠢࡔࡆࡎࡊࡪࡧࡴࡶࡴࡨࡔࡪࡸࡦࡰࡴࡰࡥࡳࡩࡥࠣਗ"),
                      bstack11l1l11_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟࡫ࡵࡲࡲࠧਘ"): {
                          bstack11l1l11_opy_ (u"ࠤࡰࡩࡦࡹࡵࡳࡧࡶࠦਙ"): data,
                          bstack11l1l11_opy_ (u"ࠥࡷࡩࡱࡒࡶࡰࡌࡨࠧਚ"): global_config.get_property(bstack11l1l11_opy_ (u"ࠦࡸࡪ࡫ࡓࡷࡱࡍࡩࠨਛ"))
                      },
                      bstack11l1l11_opy_ (u"ࠧࡻࡳࡦࡴࡢࡨࡦࡺࡡࠣਜ"): global_config.get_property(bstack11l1l11_opy_ (u"ࠨࡵࡴࡧࡵࡒࡦࡳࡥࠣਝ")),
                      bstack11l1l11_opy_ (u"ࠢࡩࡱࡶࡸࡤ࡯࡮ࡧࡱࠥਞ"): get_host_info()
                  }
              }
              bstack1ll11l111_opy_ = bstack1ll11l1l11_opy_(cli.config, [bstack11l1l11_opy_ (u"ࠣࡣࡳ࡭ࡸࠨਟ"), bstack11l1l11_opy_ (u"ࠤࡨࡨࡸࡏ࡮ࡴࡶࡵࡹࡲ࡫࡮ࡵࡣࡷ࡭ࡴࡴࠢਠ"), bstack11l1l11_opy_ (u"ࠥࡥࡵ࡯ࠢਡ")], bstack111l11lll1_opy_)
              response = bstack11l11llll_opy_(bstack11l1l11_opy_ (u"ࠦࡕࡕࡓࡕࠤਢ"), bstack1ll11l111_opy_, payload, config)
              if response.status_code >= 200 and response.status_code < 300:
                  logger.info(bstack11l1l11_opy_ (u"ࠧࡑࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵࠣࡷࡪࡴࡴࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡵࡱࠣࡿࢂࠨਣ").format(bstack111l11lll1_opy_))
              else:
                  logger.debug(bstack11l1l11_opy_ (u"ࠨࡋࡦࡻࠣࡱࡪࡺࡲࡪࡥࡶࠤࡷ࡫ࡱࡶࡧࡶࡸࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪࠣࡷࡹࡧࡴࡶࡵࠣࡿࢂࠨਤ").format(response.status_code))
          except Exception as e:
              logger.debug(bstack11l1l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡴࡤࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࡀࠠࡼࡿࠥਥ").format(e))
      bstack1l1ll11lll_opy_()
  except Exception as e:
      logger.debug(bstack11l1l11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡴࡤࡠ࡭ࡨࡽࡤࡳࡥࡵࡴ࡬ࡧࡸࡀࠠࡼࡿࠥਦ").format(e))
def bstack1llll1l1_opy_():
  bstack11lll111l1_opy_ = bstack11l1l11_opy_ (u"ࠤࠥਧ")
  global bstack11ll1l11l1_opy_
  global bstack1ll1111ll1_opy_
  global bstack1111lllll_opy_
  global bstack111ll11l11_opy_
  global ROBOT_PYTHON_ERRORS
  global bstack1lll1ll1l1_opy_
  global CONFIG
  bstack1l111ll11l_opy_ = os.environ.get(bstack11l1l11_opy_ (u"ࠪࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡕࡔࡇࡇࠫਨ"))
  if bstack1l111ll11l_opy_ not in [bstack11l1l11_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ਩")]:
    bstack11lll111l1_opy_ = bstack11ll1l1l1_opy_.bstack1l11l111ll_opy_(EVENTS.bstack111l1lll1l_opy_)
  percy.shutdown()
  if bstack11ll1l11l1_opy_:
    logger.warning(bstack11l1l1ll11_opy_.format(str(bstack11ll1l11l1_opy_)))
  else:
    try:
      bstack11lll1l1l1_opy_ = bstack11l11l1ll1_opy_(bstack11l1l11_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫਪ"), logger)
      if bstack11lll1l1l1_opy_.get(bstack11l1l11_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫਫ")) and bstack11lll1l1l1_opy_.get(bstack11l1l11_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬਬ")).get(bstack11l1l11_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪਭ")):
        logger.warning(bstack11l1l1ll11_opy_.format(str(bstack11lll1l1l1_opy_[bstack11l1l11_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧਮ")][bstack11l1l11_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬਯ")])))
    except Exception as e:
      logger.error(e)
  if cli.is_running() and bstack1l111ll11l_opy_ not in [bstack11l1l11_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬਰ")]:
    bstack11l1l1l11_opy_.invoke(bstack1lllllll1_opy_.bstack1l111l1ll1_opy_)
  logger.info(bstack1ll1ll111_opy_)
  global bstack1l11l11lll_opy_
  if bstack1l11l11lll_opy_:
    bstack1lll11l1l1_opy_()
  try:
    with bstack1lllllll11_opy_:
      bstack11l11ll1l_opy_ = bstack1ll1111ll1_opy_.copy()
    for driver in bstack11l11ll1l_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1l1111l1l1_opy_)
  ROBOT_PYTHON_ERRORS = []
  if bstack1lll1ll1l1_opy_ == bstack11l1l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ਱"):
    ROBOT_PYTHON_ERRORS = bstack1l1l1llll_opy_(bstack11l1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧਲ"))
  if bstack1lll1ll1l1_opy_ == bstack11l1l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧਲ਼") and len(bstack111ll11l11_opy_) == 0:
    bstack111ll11l11_opy_ = bstack1l1l1llll_opy_(bstack11l1l11_opy_ (u"ࠨࡲࡺࡣࡵࡿࡴࡦࡵࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭਴"))
    if len(bstack111ll11l11_opy_) == 0:
      bstack111ll11l11_opy_ = bstack1l1l1llll_opy_(bstack11l1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡳࡴࡵࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨਵ"))
  bstack1ll1l1111_opy_ = bstack11l1l11_opy_ (u"ࠪࠫਸ਼")
  if len(bstack1111lllll_opy_) > 0:
    bstack1ll1l1111_opy_ = bstack111l11ll11_opy_(bstack1111lllll_opy_)
  elif len(bstack111ll11l11_opy_) > 0:
    bstack1ll1l1111_opy_ = bstack111l11ll11_opy_(bstack111ll11l11_opy_)
  elif len(ROBOT_PYTHON_ERRORS) > 0:
    bstack1ll1l1111_opy_ = bstack111l11ll11_opy_(ROBOT_PYTHON_ERRORS)
  elif len(bstack1l1l1l1ll_opy_) > 0:
    bstack1ll1l1111_opy_ = bstack111l11ll11_opy_(bstack1l1l1l1ll_opy_)
  if bstack1l111ll11l_opy_ not in [bstack11l1l11_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ਷")]:
    def bstack111l1l11_opy_():
      try:
        if bstack1l111ll11l_opy_ in [bstack11l1l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫਸ"), bstack11l1l11_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬਹ")]:
          bstack1l111ll1l_opy_()
      except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩ࡭ࡳࡧ࡬ࡠࡧࡻࡩࡨࡻࡴࡪࡱࡱ࠾ࠥࢁࡽࠣ਺").format(e))
    def bstack1llll11l11_opy_():
      try:
        if bool(bstack1ll1l1111_opy_):
          bstack1l111l1111_opy_(bstack1ll1l1111_opy_)
        else:
          bstack1l111l1111_opy_()
      except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡴࡧࡱࡨ࡮ࡴࡧࠡࡧࡹࡩࡳࡺ࠺ࠡࡽࢀࠦ਻").format(e))
    def bstack11lll1111_opy_():
      try:
        logger_utils.bstack1l111ll1_opy_(CONFIG)
      except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡵࡨࡲࡩ࡯࡮ࡨࠢ࡯ࡳ࡬ࡹ࠺ࠡࡽࢀ਼ࠦ").format(e))
    bstack1l111l11_opy_ = threading.Thread(target=bstack111l1l11_opy_)
    bstack1l1111l1ll_opy_ = threading.Thread(target=bstack1llll11l11_opy_)
    bstack1lll1l111l_opy_ = threading.Thread(target=bstack11lll1111_opy_)
    threads = [bstack1l111l11_opy_, bstack1l1111l1ll_opy_, bstack1lll1l111l_opy_]
    for thread in threads:
      try:
        thread.start()
      except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡶࡸࡦࡸࡴࡪࡰࡪࠤࡹ࡮ࡲࡦࡣࡧࠤࢀࢃ࠺ࠡࡽࢀࠦ਽").format(thread.name, e))
    for thread in threads:
      try:
        thread.join()
      except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡮ࡴ࡯࡮ࡪࡰࡪࠤࡹ࡮ࡲࡦࡣࡧࠤࢀࢃ࠺ࠡࡽࢀࠦਾ").format(thread.name, e))
    bstack111ll1lll_opy_(bstack1l11ll1ll_opy_, logger)
    bstack111ll1lll_opy_(os.path.join(os.getcwd(), bstack11l1l11_opy_ (u"ࠬࡲ࡯ࡨࠩਿ"), bstack11l1l11_opy_ (u"࠭࡫ࡦࡻ࠰ࡱࡪࡺࡲࡪࡥࡶ࠲࡯ࡹ࡯࡯ࠩੀ")), logger)
  if bstack1l111ll11l_opy_ not in [bstack11l1l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨੁ")]:
    bstack11ll1l1l1_opy_.end(EVENTS.bstack111l1lll1l_opy_.value, bstack11lll111l1_opy_ + bstack11l1l11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣੂ"), bstack11lll111l1_opy_ + bstack11l1l11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ੃"), status=True, failure=None, test_name=None)
    bstack1ll1l11111_opy_()
    logger_utils.bstack1l1ll11l1_opy_()
    logging.shutdown()
  if len(ROBOT_PYTHON_ERRORS) > 0:
    sys.exit(len(ROBOT_PYTHON_ERRORS))
def bstack11lllll11_opy_(bstack11111l111_opy_, frame):
  global global_config
  logger.error(bstack1lll1l1111_opy_)
  global_config.bstack1l111111ll_opy_(bstack11l1l11_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡒࡴ࠭੄"), bstack11111l111_opy_)
  if hasattr(signal, bstack11l1l11_opy_ (u"ࠫࡘ࡯ࡧ࡯ࡣ࡯ࡷࠬ੅")):
    global_config.bstack1l111111ll_opy_(bstack11l1l11_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬ੆"), signal.Signals(bstack11111l111_opy_).name)
  else:
    global_config.bstack1l111111ll_opy_(bstack11l1l11_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭ੇ"), bstack11l1l11_opy_ (u"ࠧࡔࡋࡊ࡙ࡓࡑࡎࡐ࡙ࡑࠫੈ"))
  if cli.is_running():
    bstack11l1l1l11_opy_.invoke(bstack1lllllll1_opy_.bstack1l111l1ll1_opy_)
  bstack1l111ll11l_opy_ = os.environ.get(bstack11l1l11_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩ੉"))
  if bstack1l111ll11l_opy_ == bstack11l1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ੊") and not cli.is_enabled(CONFIG):
    TestHubHandler.stop(global_config.get_property(bstack11l1l11_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪੋ")))
  bstack1llll1l1_opy_()
  sys.exit(1)
def bstack11l1lll11l_opy_(err):
  logger.critical(bstack1111ll111_opy_.format(str(err)))
  bstack1l111l1111_opy_(bstack1111ll111_opy_.format(str(err)), True)
  atexit.unregister(bstack1llll1l1_opy_)
  bstack1l111ll1l_opy_()
  sys.exit(1)
def bstack1ll1llll1l_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1l111l1111_opy_(message, True)
  atexit.unregister(bstack1llll1l1_opy_)
  bstack1l111ll1l_opy_()
  sys.exit(1)
def bstack11lll1l1ll_opy_():
  global CONFIG
  global bstack11l1lll11_opy_
  global bstack11ll111111_opy_
  global bstack1l1111111_opy_
  CONFIG = bstack11l11l1l1l_opy_()
  load_dotenv(CONFIG.get(bstack11l1l11_opy_ (u"ࠫࡪࡴࡶࡇ࡫࡯ࡩࠬੌ")))
  bstack11l11111ll_opy_()
  bstack1ll11l1l1l_opy_()
  CONFIG = bstack111111111_opy_(CONFIG)
  update(CONFIG, bstack11ll111111_opy_)
  update(CONFIG, bstack11l1lll11_opy_)
  if not cli.is_enabled(CONFIG):
    CONFIG = bstack1111111l1_opy_(CONFIG)
  bstack1l1111111_opy_ = bstack1lll1l1l_opy_(CONFIG)
  os.environ[bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ੍")] = bstack1l1111111_opy_.__str__().lower()
  global_config.bstack1l111111ll_opy_(bstack11l1l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ੎"), bstack1l1111111_opy_)
  if (bstack11l1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ੏") in CONFIG and bstack11l1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ੐") in bstack11l1lll11_opy_) or (
          bstack11l1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬੑ") in CONFIG and bstack11l1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭੒") not in bstack11ll111111_opy_):
    if os.getenv(bstack11l1l11_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨ੓")):
      CONFIG[bstack11l1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ੔")] = os.getenv(bstack11l1l11_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪ੕"))
    else:
      if not CONFIG.get(bstack11l1l11_opy_ (u"ࠢࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠥ੖"), bstack11l1l11_opy_ (u"ࠣࠤ੗")) in bstack111l1111_opy_:
        bstack1l11l1ll11_opy_()
  elif (bstack11l1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ੘") not in CONFIG and bstack11l1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬਖ਼") in CONFIG) or (
          bstack11l1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧਗ਼") in bstack11ll111111_opy_ and bstack11l1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨਜ਼") not in bstack11l1lll11_opy_):
    del (CONFIG[bstack11l1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨੜ")])
  if bstack11llll1l11_opy_(CONFIG):
    bstack11l1lll11l_opy_(bstack1111lll1l_opy_)
  Config.get_instance().bstack1l111111ll_opy_(bstack11l1l11_opy_ (u"ࠢࡶࡵࡨࡶࡓࡧ࡭ࡦࠤ੝"), CONFIG[bstack11l1l11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪਫ਼")])
  bstack111l1ll1ll_opy_()
  bstack1llll1l1l1_opy_()
  if bstack1l11ll1ll1_opy_ and not CONFIG.get(bstack11l1l11_opy_ (u"ࠤࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠧ੟"), bstack11l1l11_opy_ (u"ࠥࠦ੠")) in bstack111l1111_opy_:
    CONFIG[bstack11l1l11_opy_ (u"ࠫࡦࡶࡰࠨ੡")] = bstack1l11111ll_opy_(CONFIG)
    logger.info(bstack1l111l1l1_opy_.format(CONFIG[bstack11l1l11_opy_ (u"ࠬࡧࡰࡱࠩ੢")]))
  if not bstack1l1111111_opy_:
    CONFIG[bstack11l1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ੣")] = [{}]
def bstack11llll1l_opy_(config, bstack11l1lll1l_opy_):
  global CONFIG
  global bstack1l11ll1ll1_opy_
  CONFIG = config
  bstack1l11ll1ll1_opy_ = bstack11l1lll1l_opy_
def bstack1llll1l1l1_opy_():
  global CONFIG
  global bstack1l11ll1ll1_opy_
  if bstack11l1l11_opy_ (u"ࠧࡢࡲࡳࠫ੤") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1ll1llll1l_opy_(e, bstack111l1l1l1l_opy_)
    bstack1l11ll1ll1_opy_ = True
    global_config.bstack1l111111ll_opy_(bstack11l1l11_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ੥"), True)
def bstack1l11111ll_opy_(config):
  bstack1llll111l1_opy_ = bstack11l1l11_opy_ (u"ࠩࠪ੦")
  app = config[bstack11l1l11_opy_ (u"ࠪࡥࡵࡶࠧ੧")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack111llll1l_opy_:
      if os.path.exists(app):
        bstack1llll111l1_opy_ = bstack11111ll11_opy_(config, app)
      elif bstack11l1lll1_opy_(app):
        bstack1llll111l1_opy_ = app
      else:
        bstack11l1lll11l_opy_(bstack11l11ll1_opy_.format(app))
    else:
      if bstack11l1lll1_opy_(app):
        bstack1llll111l1_opy_ = app
      elif os.path.exists(app):
        bstack1llll111l1_opy_ = bstack11111ll11_opy_(app)
      else:
        bstack11l1lll11l_opy_(bstack1l1ll11l1l_opy_)
  else:
    if len(app) > 2:
      bstack11l1lll11l_opy_(bstack1llllllll1_opy_)
    elif len(app) == 2:
      if bstack11l1l11_opy_ (u"ࠫࡵࡧࡴࡩࠩ੨") in app and bstack11l1l11_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨ੩") in app:
        if os.path.exists(app[bstack11l1l11_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ੪")]):
          bstack1llll111l1_opy_ = bstack11111ll11_opy_(config, app[bstack11l1l11_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ੫")], app[bstack11l1l11_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫ੬")])
        else:
          bstack11l1lll11l_opy_(bstack11l11ll1_opy_.format(app))
      else:
        bstack11l1lll11l_opy_(bstack1llllllll1_opy_)
    else:
      for key in app:
        if key in bstack111l11l1_opy_:
          if key == bstack11l1l11_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ੭"):
            if os.path.exists(app[key]):
              bstack1llll111l1_opy_ = bstack11111ll11_opy_(config, app[key])
            else:
              bstack11l1lll11l_opy_(bstack11l11ll1_opy_.format(app))
          else:
            bstack1llll111l1_opy_ = app[key]
        else:
          bstack11l1lll11l_opy_(bstack1lll1l1ll1_opy_)
  return bstack1llll111l1_opy_
def bstack11l1lll1_opy_(bstack1llll111l1_opy_):
  import re
  bstack11l1ll1111_opy_ = re.compile(bstack11l1l11_opy_ (u"ࡵࠦࡣࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫࠦࠥ੮"))
  bstack1l1ll1l11l_opy_ = re.compile(bstack11l1l11_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬ࠲࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰ࠤࠣ੯"))
  if bstack11l1l11_opy_ (u"ࠬࡨࡳ࠻࠱࠲ࠫੰ") in bstack1llll111l1_opy_ or re.fullmatch(bstack11l1ll1111_opy_, bstack1llll111l1_opy_) or re.fullmatch(bstack1l1ll1l11l_opy_, bstack1llll111l1_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack1ll11111l_opy_, stage=STAGE.bstack1l11l1l11l_opy_, bstack1l111l11l_opy_=bstack1ll1ll11l1_opy_)
def bstack11111ll11_opy_(config, path, bstack1ll1l1ll1_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack11l1l11_opy_ (u"࠭ࡲࡣࠩੱ")).read()).hexdigest()
  bstack1ll11ll1_opy_ = bstack1llllll111_opy_(md5_hash)
  bstack1llll111l1_opy_ = None
  if bstack1ll11ll1_opy_:
    logger.info(bstack11l1l1111_opy_.format(bstack1ll11ll1_opy_, md5_hash))
    return bstack1ll11ll1_opy_
  bstack111l11l1l1_opy_ = datetime.datetime.now()
  bstack11lllll1l1_opy_ = MultipartEncoder(
    fields={
      bstack11l1l11_opy_ (u"ࠧࡧ࡫࡯ࡩࠬੲ"): (os.path.basename(path), open(os.path.abspath(path), bstack11l1l11_opy_ (u"ࠨࡴࡥࠫੳ")), bstack11l1l11_opy_ (u"ࠩࡷࡩࡽࡺ࠯ࡱ࡮ࡤ࡭ࡳ࠭ੴ")),
      bstack11l1l11_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ੵ"): bstack1ll1l1ll1_opy_
    }
  )
  response = requests.post(bstack1ll11l1l1_opy_, data=bstack11lllll1l1_opy_,
                           headers={bstack11l1l11_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪ੶"): bstack11lllll1l1_opy_.content_type},
                           auth=(config[bstack11l1l11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ੷")], config[bstack11l1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ੸")]))
  try:
    res = json.loads(response.text)
    bstack1llll111l1_opy_ = res[bstack11l1l11_opy_ (u"ࠧࡢࡲࡳࡣࡺࡸ࡬ࠨ੹")]
    logger.info(bstack1lll1111_opy_.format(bstack1llll111l1_opy_))
    bstack1l1lllll1l_opy_(md5_hash, bstack1llll111l1_opy_)
    cli.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠣࡪࡷࡸࡵࡀࡵࡱ࡮ࡲࡥࡩࡥࡡࡱࡲࠥ੺"), datetime.datetime.now() - bstack111l11l1l1_opy_)
  except ValueError as err:
    bstack11l1lll11l_opy_(bstack1l1l1l111l_opy_.format(str(err)))
  return bstack1llll111l1_opy_
def bstack111l1ll1ll_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack1lll1l1l11_opy_
  bstack1ll111111_opy_ = 1
  bstack11l1ll1ll_opy_ = 1
  if bstack11l1l11_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ੻") in CONFIG:
    bstack11l1ll1ll_opy_ = CONFIG[bstack11l1l11_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ੼")]
  else:
    bstack11l1ll1ll_opy_ = bstack111lllll1l_opy_(framework_name, args) or 1
  if bstack11l1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ੽") in CONFIG:
    bstack1ll111111_opy_ = len(CONFIG[bstack11l1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ੾")])
  bstack1lll1l1l11_opy_ = int(bstack11l1ll1ll_opy_) * int(bstack1ll111111_opy_)
def bstack111lllll1l_opy_(framework_name, args):
  if framework_name == bstack1ll1l11l11_opy_ and args and bstack11l1l11_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ੿") in args:
      bstack11l1111l1_opy_ = args.index(bstack11l1l11_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ઀"))
      return int(args[bstack11l1111l1_opy_ + 1]) or 1
  return 1
def bstack1llllll111_opy_(md5_hash):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack11l1l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡲ࡯ࡤ࡭ࠣࡲࡴࡺࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧ࠯ࠤࡺࡹࡩ࡯ࡩࠣࡦࡦࡹࡩࡤࠢࡩ࡭ࡱ࡫ࠠࡰࡲࡨࡶࡦࡺࡩࡰࡰࡶࠫઁ"))
    bstack11l1l1ll_opy_ = os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"ࠩࢁࠫં")), bstack11l1l11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪઃ"), bstack11l1l11_opy_ (u"ࠫࡦࡶࡰࡖࡲ࡯ࡳࡦࡪࡍࡅ࠷ࡋࡥࡸ࡮࠮࡫ࡵࡲࡲࠬ઄"))
    if os.path.exists(bstack11l1l1ll_opy_):
      try:
        bstack1lll1ll1l_opy_ = json.load(open(bstack11l1l1ll_opy_, bstack11l1l11_opy_ (u"ࠬࡸࡢࠨઅ")))
        if md5_hash in bstack1lll1ll1l_opy_:
          bstack11l1l1llll_opy_ = bstack1lll1ll1l_opy_[md5_hash]
          bstack111l11l1l_opy_ = datetime.datetime.now()
          bstack11ll1ll1l_opy_ = datetime.datetime.strptime(bstack11l1l1llll_opy_[bstack11l1l11_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩઆ")], bstack11l1l11_opy_ (u"ࠧࠦࡦ࠲ࠩࡲ࠵࡚ࠥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫઇ"))
          if (bstack111l11l1l_opy_ - bstack11ll1ll1l_opy_).days > 30:
            return None
          elif version.parse(str(__version__)) > version.parse(bstack11l1l1llll_opy_[bstack11l1l11_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ઈ")]):
            return None
          return bstack11l1l1llll_opy_[bstack11l1l11_opy_ (u"ࠩ࡬ࡨࠬઉ")]
      except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡵࡩࡦࡪࡩ࡯ࡩࠣࡑࡉ࠻ࠠࡩࡣࡶ࡬ࠥ࡬ࡩ࡭ࡧ࠽ࠤࢀࢃࠧઊ").format(str(e)))
    return None
  bstack11l1l1ll_opy_ = os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"ࠫࢃ࠭ઋ")), bstack11l1l11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬઌ"), bstack11l1l11_opy_ (u"࠭ࡡࡱࡲࡘࡴࡱࡵࡡࡥࡏࡇ࠹ࡍࡧࡳࡩ࠰࡭ࡷࡴࡴࠧઍ"))
  lock_file = bstack11l1l1ll_opy_ + bstack11l1l11_opy_ (u"ࠧ࠯࡮ࡲࡧࡰ࠭઎")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack11l1l1ll_opy_):
        with open(bstack11l1l1ll_opy_, bstack11l1l11_opy_ (u"ࠨࡴࠪએ")) as f:
          content = f.read().strip()
          if content:
            bstack1lll1ll1l_opy_ = json.loads(content)
            if md5_hash in bstack1lll1ll1l_opy_:
              bstack11l1l1llll_opy_ = bstack1lll1ll1l_opy_[md5_hash]
              bstack111l11l1l_opy_ = datetime.datetime.now()
              bstack11ll1ll1l_opy_ = datetime.datetime.strptime(bstack11l1l1llll_opy_[bstack11l1l11_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬઐ")], bstack11l1l11_opy_ (u"ࠪࠩࡩ࠵ࠥ࡮࠱ࠨ࡝ࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧઑ"))
              if (bstack111l11l1l_opy_ - bstack11ll1ll1l_opy_).days > 30:
                return None
              elif version.parse(str(__version__)) > version.parse(bstack11l1l1llll_opy_[bstack11l1l11_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ઒")]):
                return None
              return bstack11l1l1llll_opy_[bstack11l1l11_opy_ (u"ࠬ࡯ࡤࠨઓ")]
      return None
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡽࡩࡵࡪࠣࡪ࡮ࡲࡥࠡ࡮ࡲࡧࡰ࡯࡮ࡨࠢࡩࡳࡷࠦࡍࡅ࠷ࠣ࡬ࡦࡹࡨ࠻ࠢࡾࢁࠬઔ").format(str(e)))
    return None
def bstack1l1lllll1l_opy_(md5_hash, bstack1llll111l1_opy_):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack11l1l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡱࡵࡣ࡬ࠢࡱࡳࡹࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦ࠮ࠣࡹࡸ࡯࡮ࡨࠢࡥࡥࡸ࡯ࡣࠡࡨ࡬ࡰࡪࠦ࡯ࡱࡧࡵࡥࡹ࡯࡯࡯ࡵࠪક"))
    bstack111l1ll1l1_opy_ = os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"ࠨࢀࠪખ")), bstack11l1l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩગ"))
    if not os.path.exists(bstack111l1ll1l1_opy_):
      os.makedirs(bstack111l1ll1l1_opy_)
    bstack11l1l1ll_opy_ = os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"ࠪࢂࠬઘ")), bstack11l1l11_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫઙ"), bstack11l1l11_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭ચ"))
    bstack11l1ll1l_opy_ = {
      bstack11l1l11_opy_ (u"࠭ࡩࡥࠩછ"): bstack1llll111l1_opy_,
      bstack11l1l11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪજ"): datetime.datetime.strftime(datetime.datetime.now(), bstack11l1l11_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬઝ")),
      bstack11l1l11_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧઞ"): str(__version__)
    }
    try:
      bstack1lll1ll1l_opy_ = {}
      if os.path.exists(bstack11l1l1ll_opy_):
        bstack1lll1ll1l_opy_ = json.load(open(bstack11l1l1ll_opy_, bstack11l1l11_opy_ (u"ࠪࡶࡧ࠭ટ")))
      bstack1lll1ll1l_opy_[md5_hash] = bstack11l1ll1l_opy_
      with open(bstack11l1l1ll_opy_, bstack11l1l11_opy_ (u"ࠦࡼ࠱ࠢઠ")) as outfile:
        json.dump(bstack1lll1ll1l_opy_, outfile)
    except Exception as e:
      logger.debug(bstack11l1l11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡺࡶࡤࡢࡶ࡬ࡲ࡬ࠦࡍࡅ࠷ࠣ࡬ࡦࡹࡨࠡࡨ࡬ࡰࡪࡀࠠࡼࡿࠪડ").format(str(e)))
    return
  bstack111l1ll1l1_opy_ = os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"࠭ࡾࠨઢ")), bstack11l1l11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧણ"))
  if not os.path.exists(bstack111l1ll1l1_opy_):
    os.makedirs(bstack111l1ll1l1_opy_)
  bstack11l1l1ll_opy_ = os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"ࠨࢀࠪત")), bstack11l1l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩથ"), bstack11l1l11_opy_ (u"ࠪࡥࡵࡶࡕࡱ࡮ࡲࡥࡩࡓࡄ࠶ࡊࡤࡷ࡭࠴ࡪࡴࡱࡱࠫદ"))
  lock_file = bstack11l1l1ll_opy_ + bstack11l1l11_opy_ (u"ࠫ࠳ࡲ࡯ࡤ࡭ࠪધ")
  bstack11l1ll1l_opy_ = {
    bstack11l1l11_opy_ (u"ࠬ࡯ࡤࠨન"): bstack1llll111l1_opy_,
    bstack11l1l11_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ઩"): datetime.datetime.strftime(datetime.datetime.now(), bstack11l1l11_opy_ (u"ࠧࠦࡦ࠲ࠩࡲ࠵࡚ࠥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫપ")),
    bstack11l1l11_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ફ"): str(__version__)
  }
  try:
    with FileLock(lock_file, timeout=10):
      bstack1lll1ll1l_opy_ = {}
      if os.path.exists(bstack11l1l1ll_opy_):
        with open(bstack11l1l1ll_opy_, bstack11l1l11_opy_ (u"ࠩࡵࠫબ")) as f:
          content = f.read().strip()
          if content:
            bstack1lll1ll1l_opy_ = json.loads(content)
      bstack1lll1ll1l_opy_[md5_hash] = bstack11l1ll1l_opy_
      with open(bstack11l1l1ll_opy_, bstack11l1l11_opy_ (u"ࠥࡻࠧભ")) as outfile:
        json.dump(bstack1lll1ll1l_opy_, outfile)
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡻ࡮ࡺࡨࠡࡨ࡬ࡰࡪࠦ࡬ࡰࡥ࡮࡭ࡳ࡭ࠠࡧࡱࡵࠤࡒࡊ࠵ࠡࡪࡤࡷ࡭ࠦࡵࡱࡦࡤࡸࡪࡀࠠࡼࡿࠪમ").format(str(e)))
def bstack1ll111l1_opy_(self):
  return
def bstack11lll1ll1_opy_(self):
  return
def bstack1ll11ll1l_opy_():
  global bstack11l11ll11_opy_
  bstack11l11ll11_opy_ = True
def bstack11l11111l1_opy_(self):
  global bstack11ll1ll111_opy_
  global bstack1ll1l1111l_opy_
  global bstack1l1ll111l1_opy_
  bstack1l1l1l1111_opy_ = bstack11ll1l1l1_opy_.bstack1l11l111ll_opy_(EVENTS.bstack1l1llllll_opy_)
  try:
    if bstack11l1l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬય") in bstack11ll1ll111_opy_ and self.session_id != None and bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪર"), bstack11l1l11_opy_ (u"ࠧࠨ઱")) != bstack11l1l11_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩલ"):
      bstack11l1ll11_opy_ = bstack11l1l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩળ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11l1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ઴")
      if bstack11l1ll11_opy_ == bstack11l1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫવ"):
        bstack1llll1l11_opy_(logger)
      if self != None:
        bstack11lll1l11l_opy_(self, bstack11l1ll11_opy_, bstack11l1l11_opy_ (u"ࠬ࠲ࠠࠨશ").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack11l1l11_opy_ (u"࠭ࠧષ")
    if bstack11l1l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧસ") in bstack11ll1ll111_opy_ and getattr(threading.current_thread(), bstack11l1l11_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧહ"), None):
      bstack11111111_opy_.bstack1ll1l1l1_opy_(self, bstack1ll11ll11l_opy_, logger, wait=True)
    if bstack11l1l11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ઺") in bstack11ll1ll111_opy_:
      bstack1l11l1ll1l_opy_.bstack1l111l11ll_opy_(self)
    bstack11ll1l1l1_opy_.end(EVENTS.bstack1l1llllll_opy_.value, bstack1l1l1l1111_opy_ + bstack11l1l11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ઻"), bstack1l1l1l1111_opy_ + bstack11l1l11_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ઼"), status=True, failure=None, test_name=None)
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࠨઽ") + str(e))
    bstack11ll1l1l1_opy_.end(EVENTS.bstack1l1llllll_opy_.value, bstack1l1l1l1111_opy_ + bstack11l1l11_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨા"), bstack1l1l1l1111_opy_ + bstack11l1l11_opy_ (u"ࠢ࠻ࡧࡱࡨࠧિ"), status=False, failure=str(e), test_name=None)
  bstack1l1ll111l1_opy_(self)
  self.session_id = None
def bstack1l1ll1l1_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack111l1llll_opy_
    global bstack11ll1ll111_opy_
    command_executor = kwargs.get(bstack11l1l11_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠫી"), bstack11l1l11_opy_ (u"ࠩࠪુ"))
    bstack1l11lll111_opy_ = False
    if type(command_executor) == str and bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ૂ") in command_executor:
      bstack1l11lll111_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧૃ") in str(getattr(command_executor, bstack11l1l11_opy_ (u"ࠬࡥࡵࡳ࡮ࠪૄ"), bstack11l1l11_opy_ (u"࠭ࠧૅ"))):
      bstack1l11lll111_opy_ = True
    else:
      kwargs = bstack1l111ll111_opy_.bstack1ll1ll1l11_opy_(bstack11llllll_opy_=kwargs, config=CONFIG)
      return bstack11l1ll11l1_opy_(self, *args, **kwargs)
    if bstack1l11lll111_opy_:
      bstack1llll111l_opy_ = bstack1l11l1l111_opy_.bstack1l111l111_opy_(CONFIG, bstack11ll1ll111_opy_)
      if kwargs.get(bstack11l1l11_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ૆")):
        kwargs[bstack11l1l11_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩે")] = bstack111l1llll_opy_(kwargs[bstack11l1l11_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪૈ")], bstack11ll1ll111_opy_, CONFIG, bstack1llll111l_opy_)
      elif kwargs.get(bstack11l1l11_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪૉ")):
        kwargs[bstack11l1l11_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ૊")] = bstack111l1llll_opy_(kwargs[bstack11l1l11_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬો")], bstack11ll1ll111_opy_, CONFIG, bstack1llll111l_opy_)
  except Exception as e:
    logger.error(bstack11l1l11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡦࡰࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡔࡆࡎࠤࡨࡧࡰࡴ࠼ࠣࡿࢂࠨૌ").format(str(e)))
  return bstack11l1ll11l1_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack11llll1l1_opy_, stage=STAGE.bstack1l11l1l11l_opy_, bstack1l111l11l_opy_=bstack1ll1ll11l1_opy_)
def bstack11lllllll1_opy_(self, command_executor=bstack11l1l11_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯࠲࠴࠺࠲࠵࠴࠰࠯࠳࠽࠸࠹࠺࠴્ࠣ"), *args, **kwargs):
  global bstack1ll1l1111l_opy_
  global bstack1ll1111ll1_opy_
  bstack1l11ll111l_opy_ = bstack1l1ll1l1_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack1l111111_opy_.on():
    return bstack1l11ll111l_opy_
  try:
    logger.debug(bstack11l1l11_opy_ (u"ࠨࡅࡲࡱࡲࡧ࡮ࡥࠢࡈࡼࡪࡩࡵࡵࡱࡵࠤࡼ࡮ࡥ࡯ࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥ࡯ࡳࠡࡨࡤࡰࡸ࡫ࠠ࠮ࠢࡾࢁࠬ૎").format(str(command_executor)))
    logger.debug(bstack11l1l11_opy_ (u"ࠩࡋࡹࡧࠦࡕࡓࡎࠣ࡭ࡸࠦ࠭ࠡࡽࢀࠫ૏").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ૐ") in command_executor._url:
      global_config.bstack1l111111ll_opy_(bstack11l1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬ૑"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨ૒") in command_executor):
    global_config.bstack1l111111ll_opy_(bstack11l1l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ૓"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1l1llllll1_opy_ = getattr(threading.current_thread(), bstack11l1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡔࡦࡵࡷࡑࡪࡺࡡࠨ૔"), None)
  bstack111l11l111_opy_ = {}
  if self.capabilities is not None:
    bstack111l11l111_opy_[bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧ૕")] = self.capabilities.get(bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ૖"))
    bstack111l11l111_opy_[bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ૗")] = self.capabilities.get(bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ૘"))
    bstack111l11l111_opy_[bstack11l1l11_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡤࡵࡰࡵ࡫ࡲࡲࡸ࠭૙")] = self.capabilities.get(bstack11l1l11_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ૚"))
  if CONFIG.get(bstack11l1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ૛"), False) and bstack1l111ll111_opy_.bstack1l1l11lll1_opy_(bstack111l11l111_opy_):
    threading.current_thread().a11yPlatform = True
  if bstack11l1l11_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ૜") in bstack11ll1ll111_opy_ or bstack11l1l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ૝") in bstack11ll1ll111_opy_:
    TestHubHandler.bstack1lllll1ll1_opy_(self)
  if bstack11l1l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ૞") in bstack11ll1ll111_opy_ and bstack1l1llllll1_opy_ and bstack1l1llllll1_opy_.get(bstack11l1l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ૟"), bstack11l1l11_opy_ (u"ࠬ࠭ૠ")) == bstack11l1l11_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧૡ"):
    TestHubHandler.bstack1lllll1ll1_opy_(self)
  bstack1ll1l1111l_opy_ = self.session_id
  with bstack1lllllll11_opy_:
    bstack1ll1111ll1_opy_.append(self)
  return bstack1l11ll111l_opy_
def bstack11l11111l_opy_(args):
  return bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲࠨૢ") in str(args)
def bstack1l1l1lll11_opy_(self, driver_command, *args, **kwargs):
  global bstack1l1l1111l_opy_
  global bstack11l11ll111_opy_
  bstack111l11111l_opy_ = bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬૣ"), None) and bstack11llll11l1_opy_(
          threading.current_thread(), bstack11l1l11_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ૤"), None)
  bstack1l11l11111_opy_ = bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ૥"), None) and bstack11llll11l1_opy_(
          threading.current_thread(), bstack11l1l11_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭૦"), None)
  bstack11l1l1l11l_opy_ = getattr(self, bstack11l1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬ૧"), None) != None and getattr(self, bstack11l1l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭૨"), None) == True
  if not bstack11l11ll111_opy_ and bstack11l1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ૩") in CONFIG and CONFIG[bstack11l1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ૪")] == True and bstack111llllll1_opy_.bstack1l111l1l1l_opy_(driver_command) and (bstack11l1l1l11l_opy_ or bstack111l11111l_opy_ or bstack1l11l11111_opy_) and not bstack11l11111l_opy_(args):
    try:
      bstack11l11ll111_opy_ = True
      logger.debug(bstack11l1l11_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡽࢀࠫ૫").format(driver_command))
      bstack1lll11ll11_opy_ = perform_scan(self, driver_command=driver_command)
      logger.debug(bstack1lll11ll11_opy_)
      try:
        bstack11ll1llll_opy_ = {
          bstack11l1l11_opy_ (u"ࠥࡶࡪࡷࡵࡦࡵࡷࠦ૬"): {
            bstack11l1l11_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࠧ૭"): bstack11l1l11_opy_ (u"ࠧࡇ࠱࠲࡛ࡢࡗࡈࡇࡎࠣ૮"),
            bstack11l1l11_opy_ (u"ࠨࡰࡢࡴࡤࡱࡪࡺࡥࡳࡵࠥ૯"): [
              {
                bstack11l1l11_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢ૰"): driver_command
              }
            ]
          },
          bstack11l1l11_opy_ (u"ࠣࡴࡨࡷࡵࡵ࡮ࡴࡧࠥ૱"): {
            bstack11l1l11_opy_ (u"ࠤࡥࡳࡩࡿࠢ૲"): {
              bstack11l1l11_opy_ (u"ࠥࡱࡸ࡭ࠢ૳"): bstack1lll11ll11_opy_.get(bstack11l1l11_opy_ (u"ࠦࡲࡹࡧࠣ૴"), bstack11l1l11_opy_ (u"ࠧࠨ૵")) if isinstance(bstack1lll11ll11_opy_, dict) else bstack11l1l11_opy_ (u"ࠨࠢ૶"),
              bstack11l1l11_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳࠣ૷"): bstack1lll11ll11_opy_.get(bstack11l1l11_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴࠤ૸"), True) if isinstance(bstack1lll11ll11_opy_, dict) else True
            }
          }
        }
        logger.debug(bstack11l1l11_opy_ (u"ࠩࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡧࡦࡴࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡱࡵࡧࠡࡦࡤࡸࡦࡀࠠࡼࡿࠪૹ").format(bstack11ll1llll_opy_))
        bstack11ll111ll_opy_.info(json.dumps(bstack11ll1llll_opy_, separators=(bstack11l1l11_opy_ (u"ࠪ࠰ࠬૺ"), bstack11l1l11_opy_ (u"ࠫ࠿࠭ૻ"))))
      except Exception as bstack111l1l11ll_opy_:
        logger.debug(bstack11l1l11_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡮ࡲ࡫ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡣࡢࡰࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠬૼ").format(str(bstack111l1l11ll_opy_)))
    except Exception as err:
      logger.debug(bstack11l1l11_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡩࡷ࡬࡯ࡳ࡯ࠣࡷࡨࡧ࡮ࠡࡽࢀࠫ૽").format(str(err)))
    bstack11l11ll111_opy_ = False
  response = bstack1l1l1111l_opy_(self, driver_command, *args, **kwargs)
  if (bstack11l1l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭૾") in str(bstack11ll1ll111_opy_).lower() or bstack11l1l11_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ૿") in str(bstack11ll1ll111_opy_).lower()) and bstack1l111111_opy_.on():
    try:
      if driver_command == bstack11l1l11_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭଀"):
        TestHubHandler.bstack11l1lllll_opy_({
            bstack11l1l11_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩଁ"): response[bstack11l1l11_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪଂ")],
            bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬଃ"): TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack1l111111_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
def bstack11l11l1lll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack1ll1l1111l_opy_
  global bstack11ll1l111_opy_
  global bstack1ll1ll11l1_opy_
  global bstack1l11ll11ll_opy_
  global bstack11l1l11111_opy_
  global bstack11ll1ll111_opy_
  global bstack11l1ll11l1_opy_
  global bstack1ll1111ll1_opy_
  global bstack1lll1llll1_opy_
  global bstack1ll11ll11l_opy_
  bstack1l1l1l1111_opy_ = bstack11ll1l1l1_opy_.bstack1l11l111ll_opy_(EVENTS.bstack11llllllll_opy_.value)
  if os.getenv(bstack11l1l11_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ଄")) is not None and bstack1l111ll111_opy_.bstack11l1ll1ll1_opy_(CONFIG) is None:
    CONFIG[bstack11l1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧଅ")] = True
  CONFIG[bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪଆ")] = str(bstack11ll1ll111_opy_) + str(__version__)
  bstack111ll11lll_opy_ = os.environ[bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧଇ")]
  bstack1llll111l_opy_ = bstack1l11l1l111_opy_.bstack1l111l111_opy_(CONFIG, bstack11ll1ll111_opy_)
  CONFIG[bstack11l1l11_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ଈ")] = bstack111ll11lll_opy_
  CONFIG[bstack11l1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ଉ")] = bstack1llll111l_opy_
  if CONFIG.get(bstack11l1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬଊ"),bstack11l1l11_opy_ (u"࠭ࠧଋ")) and bstack11l1l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ଌ") in bstack11ll1ll111_opy_:
    CONFIG[bstack11l1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ଍")].pop(bstack11l1l11_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ଎"), None)
    CONFIG[bstack11l1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪଏ")].pop(bstack11l1l11_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩଐ"), None)
  command_executor = bstack1l11111111_opy_()
  logger.debug(bstack111l111111_opy_.format(command_executor))
  proxy = bstack1l111lll1l_opy_(CONFIG, proxy)
  bstack1ll11ll1l1_opy_ = 0 if bstack11ll1l111_opy_ < 0 else bstack11ll1l111_opy_
  try:
    if bstack1l11ll11ll_opy_ is True:
      bstack1ll11ll1l1_opy_ = int(multiprocessing.current_process().name)
    elif bstack11l1l11111_opy_ is True:
      bstack1ll11ll1l1_opy_ = int(threading.current_thread().name)
  except:
    bstack1ll11ll1l1_opy_ = 0
  bstack11ll11llll_opy_ = bstack11l11ll11l_opy_(CONFIG, bstack1ll11ll1l1_opy_)
  logger.debug(bstack1l1l111111_opy_.format(str(bstack11ll11llll_opy_)))
  if bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ଑") in CONFIG and bstack1lll1l111_opy_(CONFIG[bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ଒")]):
    bstack1l1l11111l_opy_(bstack11ll11llll_opy_)
  if bstack1l111ll111_opy_.bstack111ll1111l_opy_(CONFIG, bstack1ll11ll1l1_opy_) and bstack1l111ll111_opy_.bstack11l1llllll_opy_(bstack11ll11llll_opy_, options, desired_capabilities, CONFIG):
    threading.current_thread().a11yPlatform = True
    if (cli.accessibility is None or not cli.accessibility.is_enabled()):
      bstack1l111ll111_opy_.set_capabilities(bstack11ll11llll_opy_, CONFIG)
  if desired_capabilities:
    bstack11ll1ll1ll_opy_ = bstack111111111_opy_(desired_capabilities)
    bstack11ll1ll1ll_opy_[bstack11l1l11_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧଓ")] = bstack11ll1l1l1l_opy_(CONFIG)
    bstack111ll111l_opy_ = bstack11l11ll11l_opy_(bstack11ll1ll1ll_opy_)
    if bstack111ll111l_opy_:
      bstack11ll11llll_opy_ = update(bstack111ll111l_opy_, bstack11ll11llll_opy_)
    desired_capabilities = None
  if options:
    bstack1ll11111ll_opy_(options, bstack11ll11llll_opy_)
  if not options:
    options = bstack11ll1l11ll_opy_(bstack11ll11llll_opy_)
  try:
    if bstack111ll1llll_opy_:
      def _11l1l1lll1_opy_(bstack1l11l1l1_opy_):
        if not isinstance(bstack1l11l1l1_opy_, dict):
          return
        for _1ll1l1llll_opy_ in list(bstack1l11l1l1_opy_.keys()):
          _111111ll1_opy_ = bstack1l11l1l1_opy_[_1ll1l1llll_opy_]
          if _111111ll1_opy_ is None:
            bstack1l11l1l1_opy_.pop(_1ll1l1llll_opy_, None)
          elif isinstance(_111111ll1_opy_, dict):
            _11l1l1lll1_opy_(_111111ll1_opy_)
      _11l1l1lll1_opy_(bstack11ll11llll_opy_)
      _11l1l1lll1_opy_(desired_capabilities)
      if options is not None and hasattr(options, bstack11l1l11_opy_ (u"ࠨࡡࡦࡥࡵࡹࠧଔ")):
        _11l1l1lll1_opy_(options._caps)
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"ࠤࡰࡳࡩࡥࡩ࡯࡫ࡷࠬ࠮ࠦࡰࡰࡵࡷ࠱ࡴࡶࡴࡪࡱࡱࡷࠥࡶࡲࡶࡰࡨࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽࠣକ").format(e))
  if bstack111ll1llll_opy_:
    options = bstack111ll1l11_opy_(options)
  bstack1ll11ll11l_opy_ = CONFIG.get(bstack11l1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ଖ"))[bstack1ll11ll1l1_opy_]
  if proxy and bstack1l1ll1111l_opy_() >= version.parse(bstack11l1l11_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫଗ")):
    options.proxy(proxy)
  if options and bstack1l1ll1111l_opy_() >= version.parse(bstack11l1l11_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫଘ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1l1ll1111l_opy_() < version.parse(bstack11l1l11_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬଙ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack11ll11llll_opy_)
  logger.info(bstack1l11lll1ll_opy_)
  bstack111lll111l_opy_.end(EVENTS.bstack1ll111l1l1_opy_.value, EVENTS.bstack1ll111l1l1_opy_.value + bstack11l1l11_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢଚ"), EVENTS.bstack1ll111l1l1_opy_.value + bstack11l1l11_opy_ (u"ࠣ࠼ࡨࡲࡩࠨଛ"), status=True, failure=None, test_name=bstack1ll1ll11l1_opy_)
  if bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡴࡷࡵࡦࡪ࡮ࡨࠫଜ") in kwargs:
    del kwargs[bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡵࡸ࡯ࡧ࡫࡯ࡩࠬଝ")]
  bstack11ll1l1l1_opy_.end(EVENTS.bstack11llllllll_opy_.value, bstack1l1l1l1111_opy_ + bstack11l1l11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦଞ"), bstack1l1l1l1111_opy_ + bstack11l1l11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥଟ"), status=True, failure=None, test_name=bstack1ll1ll11l1_opy_)
  try:
    if bstack1l1ll1111l_opy_() >= version.parse(bstack11l1l11_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ଠ")):
      bstack11l1ll11l1_opy_(self, command_executor=command_executor,
                options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
    elif bstack1l1ll1111l_opy_() >= version.parse(bstack11l1l11_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ଡ")):
      bstack11l1ll11l1_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities, options=options,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l1ll1111l_opy_() >= version.parse(bstack11l1l11_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨଢ")):
      bstack11l1ll11l1_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    else:
      bstack11l1ll11l1_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive)
  except Exception as bstack1lll11ll_opy_:
    logger.error(bstack1llll1lll_opy_.format(bstack11l1l11_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠨଣ"), str(bstack1lll11ll_opy_)))
    raise bstack1lll11ll_opy_
  bstack1l1l1l1111_opy_ = bstack11ll1l1l1_opy_.bstack1l11l111ll_opy_(EVENTS.bstack11llll1l1_opy_.value)
  if bstack1l111ll111_opy_.bstack111ll1111l_opy_(CONFIG, bstack1ll11ll1l1_opy_) and bstack1l111ll111_opy_.bstack11l1llllll_opy_(self.caps, options, desired_capabilities):
    if CONFIG[bstack11l1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬତ")][bstack11l1l11_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪଥ")] == True:
      threading.current_thread().appA11yPlatform = True
      if cli.accessibility is None or not cli.accessibility.is_enabled():
        bstack1l111ll111_opy_.set_capabilities(bstack11ll11llll_opy_, CONFIG)
  try:
    bstack11lll11l1_opy_ = bstack11l1l11_opy_ (u"ࠬ࠭ଦ")
    if bstack1l1ll1111l_opy_() >= version.parse(bstack11l1l11_opy_ (u"࠭࠴࠯࠲࠱࠴ࡧ࠷ࠧଧ")):
      if self.caps is not None:
        bstack11lll11l1_opy_ = self.caps.get(bstack11l1l11_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢନ"))
    else:
      if self.capabilities is not None:
        bstack11lll11l1_opy_ = self.capabilities.get(bstack11l1l11_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣ଩"))
    if bstack11lll11l1_opy_:
      bstack11l1ll1l1_opy_(bstack11lll11l1_opy_)
      if bstack1l1ll1111l_opy_() <= version.parse(bstack11l1l11_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩପ")):
        if bstack1l1l11ll11_opy_.startswith(bstack11l1l11_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫଫ")) or bstack1l1l11ll11_opy_.startswith(bstack11l1l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࠭ବ")):
          self.command_executor._url = bstack1l1l11ll11_opy_
        else:
          self.command_executor._url = bstack11l1l11_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨଭ") + bstack1l1l11ll11_opy_ + bstack11l1l11_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥମ")
      else:
        self.command_executor._url = bstack11l1l11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤଯ") + bstack11lll11l1_opy_ + bstack11l1l11_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤର")
      logger.debug(bstack1l111ll11_opy_.format(bstack11lll11l1_opy_))
    else:
      logger.debug(bstack1111111l_opy_.format(bstack11l1l11_opy_ (u"ࠤࡒࡴࡹ࡯࡭ࡢ࡮ࠣࡌࡺࡨࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦࠥ଱")))
  except Exception as e:
    logger.debug(bstack1111111l_opy_.format(e))
  if bstack11l1l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩଲ") in bstack11ll1ll111_opy_:
    bstack111ll11l_opy_(bstack11ll1l111_opy_, bstack1lll1llll1_opy_)
  bstack1ll1l1111l_opy_ = self.session_id
  if bstack11l1l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫଳ") in bstack11ll1ll111_opy_ or bstack11l1l11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ଴") in bstack11ll1ll111_opy_ or bstack11l1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬଵ") in bstack11ll1ll111_opy_ or bstack11l1l11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡨࡧࡱࡩࡷ࡯ࡣࠨଶ") in bstack11ll1ll111_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack1l1llllll1_opy_ = getattr(threading.current_thread(), bstack11l1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡕࡧࡶࡸࡒ࡫ࡴࡢࠩଷ"), None)
  if bstack11l1l11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩସ") in bstack11ll1ll111_opy_ or bstack11l1l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩହ") in bstack11ll1ll111_opy_:
    TestHubHandler.bstack1lllll1ll1_opy_(self)
  if bstack11l1l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ଺") in bstack11ll1ll111_opy_ and bstack1l1llllll1_opy_ and bstack1l1llllll1_opy_.get(bstack11l1l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ଻"), bstack11l1l11_opy_ (u"଼࠭ࠧ")) == bstack11l1l11_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨଽ"):
    TestHubHandler.bstack1lllll1ll1_opy_(self)
  with bstack1lllllll11_opy_:
    bstack1ll1111ll1_opy_.append(self)
  if bstack11l1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫା") in CONFIG and bstack11l1l11_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧି") in CONFIG[bstack11l1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ୀ")][bstack1ll11ll1l1_opy_]:
    bstack1ll1ll11l1_opy_ = CONFIG[bstack11l1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧୁ")][bstack1ll11ll1l1_opy_][bstack11l1l11_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪୂ")]
  logger.debug(bstack11l1l1l1_opy_.format(bstack1ll1l1111l_opy_))
  bstack11ll1l1l1_opy_.end(EVENTS.bstack11llll1l1_opy_.value, bstack1l1l1l1111_opy_ + bstack11l1l11_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨୃ"), bstack1l1l1l1111_opy_ + bstack11l1l11_opy_ (u"ࠢ࠻ࡧࡱࡨࠧୄ"), status=True, failure=None, test_name=bstack1ll1ll11l1_opy_)
try:
  try:
    import Browser
    import os
    from subprocess import Popen
    from browserstack_sdk.__init__ import bstack11l11l11l_opy_
    def bstack11l1ll1lll_opy_(self, args, **kwargs):
      global CONFIG
      global bstack1lll1ll1ll_opy_
      from browserstack_sdk.__init__ import LAUNCH_PATCH_ROBOT_PLAYWRIGHT
      if(bstack11l1l11_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࠮࡫ࡵࠥ୅") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"ࠩࢁࠫ୆")), bstack11l1l11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪେ"), bstack11l1l11_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭ୈ")), bstack11l1l11_opy_ (u"ࠬࡽࠧ୉")) as fp:
          fp.write(bstack11l1l11_opy_ (u"ࠨࠢ୊"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack11l1l11_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤୋ")))):
          with open(args[1], bstack11l1l11_opy_ (u"ࠨࡴࠪୌ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack11l1l11_opy_ (u"ࠩࡤࡷࡾࡴࡣࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡣࡳ࡫ࡷࡑࡣࡪࡩ࠭ࡩ࡯࡯ࡶࡨࡼࡹ࠲ࠠࡱࡣࡪࡩࠥࡃࠠࡷࡱ࡬ࡨࠥ࠶ࠩࠨ୍") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1llll11ll1_opy_)
            if bstack11l1l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ୎") in CONFIG and str(CONFIG[bstack11l1l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ୏")]).lower() != bstack11l1l11_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ୐"):
                cdpUrl = bstack11l11l11l_opy_()
                LAUNCH_PATCH_ROBOT_PLAYWRIGHT = bstack11l1l11_opy_ (u"࠭ࠧࠨࠌ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࠏࡩ࡯࡯ࡵࡷࠤࡧࡹࡴࡢࡥ࡮ࡣࡵࡧࡴࡩࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸ࡣ࠻ࠋࡥࡲࡲࡸࡺࠠࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠲࡟࠾ࠎࡨࡵ࡮ࡴࡶࠣࡴࡤ࡯࡮ࡥࡧࡻࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠲࡞࠽ࠍࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡷࡱ࡯ࡣࡦࠪ࠳࠰ࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳ࠪ࠽ࠍࡧࡴࡴࡳࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣࠫ࠾ࠎ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡱࡧࡵ࡯ࡥ࡫ࠤࡂࠦࡡࡴࡻࡱࡧࠥ࠮࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸ࠯ࠠ࠾ࡀࠣࡿࢀࠐࠠࠡ࡮ࡨࡸࠥࡩࡡࡱࡵ࠾ࠎࠥࠦࡴࡳࡻࠣࡿࢀࠐࠠࠡࠢࠣࡧࡦࡶࡳࠡ࠿ࠣࡎࡘࡕࡎ࠯ࡲࡤࡶࡸ࡫ࠨࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷ࠮ࡁࠊࠡࠢࢀࢁࠥࡩࡡࡵࡥ࡫ࠤ࠭࡫ࡸࠪࠢࡾࡿࠏࠦࠠࠡࠢࡦࡳࡳࡹ࡯࡭ࡧ࠱ࡩࡷࡸ࡯ࡳࠪࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ࠾ࠧ࠲ࠠࡦࡺࠬ࠿ࠏࠦࠠࡾࡿࠍࠤࠥࡸࡥࡵࡷࡵࡲࠥࡧࡷࡢ࡫ࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡨࡵ࡮࡯ࡧࡦࡸ࠭ࢁࡻࠋࠢࠣࠤࠥࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵ࠼ࠣࠫࢀࡩࡤࡱࡗࡵࡰࢂ࠭ࠠࠬࠢࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩ࠭ࠌࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴࠌࠣࠤࢂࢃࠩ࠼ࠌࢀࢁࡀࠐࡣࡰࡰࡶࡸࠥࡵࡲࡪࡩ࡬ࡲࡦࡲ࡟ࡤࡱࡱࡲࡪࡩࡴࠡ࠿ࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷ࠲ࡧ࡯࡮ࡥࠪ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱ࠮ࡤࡪࡵࡳࡲ࡯ࡵ࡮ࠫ࠾ࠎ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡨࡵ࡮࡯ࡧࡦࡸࠥࡃࠠࡢࡵࡼࡲࡨࠦࠨࡤࡱࡱࡲࡪࡩࡴࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁࡻࠋࠢࠣࡰࡪࡺࠠࡤࡣࡳࡷࡀࠐࠠࠡࡶࡵࡽࠥࢁࡻࠋࠢࠣࠤࠥࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࠼ࠌࠣࠤࢂࢃࠠࡤࡣࡷࡧ࡭ࠦࠨࡦࡺࠬࠤࢀࢁࠊࠡࠢࢀࢁࠏࠦࠠࡤࡱࡱࡷࡹࠦ࡭ࡰࡦ࡬ࡪ࡮࡫ࡤࡆࡰࡧࡴࡴ࡯࡮ࡵࠢࡀࠤࠬࢁࡣࡥࡲࡘࡶࡱࢃࠧࠡ࠭ࠣࡩࡳࡩ࡯ࡥࡧࡘࡖࡎࡉ࡯࡮ࡲࡲࡲࡪࡴࡴࠩࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡦࡥࡵࡹࠩࠪ࠽ࠍࠤࠥࡸࡥࡵࡷࡵࡲࠥࡧࡷࡢ࡫ࡷࠤࡴࡸࡩࡨ࡫ࡱࡥࡱࡥࡣࡰࡰࡱࡩࡨࡺࠨࡼࡽࠍࠤࠥࠦࠠ࠯࠰࠱ࡧࡴࡴ࡮ࡦࡥࡷࡓࡵࡺࡩࡰࡰࡶ࠰ࠏࠦࠠࠡࠢࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹࡀࠠ࡮ࡱࡧ࡭࡫࡯ࡥࡥࡇࡱࡨࡵࡵࡩ࡯ࡶࠍࠤࠥࢃࡽࠪ࠽ࠍࢁࢂࡁࠊ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱ࠍࠫࠬ࠭୑").format(cdpUrl=cdpUrl)
            lines.insert(1, LAUNCH_PATCH_ROBOT_PLAYWRIGHT)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack11l1l11_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤ୒")), bstack11l1l11_opy_ (u"ࠨࡹࠪ୓")) as bstack11l1l1l1l1_opy_:
              bstack11l1l1l1l1_opy_.writelines(lines)
        CONFIG[bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ୔")] = str(bstack11ll1ll111_opy_) + str(__version__)
        bstack111ll11lll_opy_ = os.environ[bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ୕")]
        bstack1llll111l_opy_ = bstack1l11l1l111_opy_.bstack1l111l111_opy_(CONFIG, bstack11ll1ll111_opy_)
        CONFIG[bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧୖ")] = bstack111ll11lll_opy_
        CONFIG[bstack11l1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧୗ")] = bstack1llll111l_opy_
        bstack1ll11ll1l1_opy_ = 0 if bstack11ll1l111_opy_ < 0 else bstack11ll1l111_opy_
        try:
          if bstack1l11ll11ll_opy_ is True:
            bstack1ll11ll1l1_opy_ = int(multiprocessing.current_process().name)
          elif bstack11l1l11111_opy_ is True:
            bstack1ll11ll1l1_opy_ = int(threading.current_thread().name)
        except:
          bstack1ll11ll1l1_opy_ = 0
        CONFIG[bstack11l1l11_opy_ (u"ࠨࡵࡴࡧ࡚࠷ࡈࠨ୘")] = False
        CONFIG[bstack11l1l11_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ୙")] = True
        bstack11ll11llll_opy_ = bstack11l11ll11l_opy_(CONFIG, bstack1ll11ll1l1_opy_)
        logger.debug(bstack1l1l111111_opy_.format(str(bstack11ll11llll_opy_)))
        if CONFIG.get(bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ୚")):
          bstack1l1l11111l_opy_(bstack11ll11llll_opy_)
          bstack11ll11llll_opy_[bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ୛")] = os.environ[bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬଡ଼")]
        if bstack11l1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଢ଼") in CONFIG and bstack11l1l11_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ୞") in CONFIG[bstack11l1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩୟ")][bstack1ll11ll1l1_opy_]:
          bstack1ll1ll11l1_opy_ = CONFIG[bstack11l1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪୠ")][bstack1ll11ll1l1_opy_][bstack11l1l11_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ୡ")]
        args.append(os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"ࠩࢁࠫୢ")), bstack11l1l11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪୣ"), bstack11l1l11_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭୤")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack11ll11llll_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack11l1l11_opy_ (u"ࠧ࡯࡮ࡥࡧࡻࡣࡧࡹࡴࡢࡥ࡮࠲࡯ࡹࠢ୥"))
      bstack1lll1ll1ll_opy_ = True
      return bstack11ll11ll11_opy_(self, args, **kwargs)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack11111ll1_opy_(self,
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
    global bstack11ll1l111_opy_
    global bstack1ll1ll11l1_opy_
    global bstack1l11ll11ll_opy_
    global bstack11l1l11111_opy_
    global bstack11ll1ll111_opy_
    CONFIG[bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ୦")] = str(bstack11ll1ll111_opy_) + str(__version__)
    bstack111ll11lll_opy_ = os.environ[bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ୧")]
    bstack1llll111l_opy_ = bstack1l11l1l111_opy_.bstack1l111l111_opy_(CONFIG, bstack11ll1ll111_opy_)
    CONFIG[bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ୨")] = bstack111ll11lll_opy_
    CONFIG[bstack11l1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ୩")] = bstack1llll111l_opy_
    bstack1ll11ll1l1_opy_ = 0 if bstack11ll1l111_opy_ < 0 else bstack11ll1l111_opy_
    try:
      if bstack1l11ll11ll_opy_ is True:
        bstack1ll11ll1l1_opy_ = int(multiprocessing.current_process().name)
      elif bstack11l1l11111_opy_ is True:
        bstack1ll11ll1l1_opy_ = int(threading.current_thread().name)
    except:
      bstack1ll11ll1l1_opy_ = 0
    CONFIG[bstack11l1l11_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤ୪")] = True
    bstack11ll11llll_opy_ = bstack11l11ll11l_opy_(CONFIG, bstack1ll11ll1l1_opy_)
    logger.debug(bstack1l1l111111_opy_.format(str(bstack11ll11llll_opy_)))
    if CONFIG.get(bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ୫")):
      bstack1l1l11111l_opy_(bstack11ll11llll_opy_)
    if bstack11l1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ୬") in CONFIG and bstack11l1l11_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ୭") in CONFIG[bstack11l1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ୮")][bstack1ll11ll1l1_opy_]:
      bstack1ll1ll11l1_opy_ = CONFIG[bstack11l1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ୯")][bstack1ll11ll1l1_opy_][bstack11l1l11_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ୰")]
    import urllib
    import json
    if bstack11l1l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧୱ") in CONFIG and str(CONFIG[bstack11l1l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ୲")]).lower() != bstack11l1l11_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ୳"):
        bstack111l1l1ll_opy_ = bstack11l11l11l_opy_()
        cdpUrl = bstack111l1l1ll_opy_ + urllib.parse.quote(json.dumps(bstack11ll11llll_opy_))
    else:
        cdpUrl = bstack11l1l11_opy_ (u"࠭ࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠨ୴") + urllib.parse.quote(json.dumps(bstack11ll11llll_opy_))
    browser = self.connect(cdpUrl)
    return browser
except Exception as e:
    pass
def bstack11llllll1l_opy_():
    global bstack1lll1ll1ll_opy_
    global bstack11ll1ll111_opy_
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1ll1l111l_opy_
        global global_config
        if not bstack1l1111111_opy_:
          global bstack1l1l1l1lll_opy_
          if not bstack1l1l1l1lll_opy_:
            from bstack_utils.helper import bstack11llllll1_opy_, bstack111ll1lll1_opy_, bstack1l1lll11l_opy_
            bstack1l1l1l1lll_opy_ = bstack11llllll1_opy_()
            bstack111ll1lll1_opy_(bstack11ll1ll111_opy_)
            bstack1llll111l_opy_ = bstack1l11l1l111_opy_.bstack1l111l111_opy_(CONFIG, bstack11ll1ll111_opy_)
            global_config.bstack1l111111ll_opy_(bstack11l1l11_opy_ (u"ࠢࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡕࡘࡏࡅࡗࡆࡘࡤࡓࡁࡑࠤ୵"), bstack1llll111l_opy_)
          BrowserType.connect = bstack1ll1l111l_opy_
          return
        BrowserType.launch = bstack11111ll1_opy_
        bstack1lll1ll1ll_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack11l1ll1lll_opy_
      bstack1lll1ll1ll_opy_ = True
    except Exception as e:
      pass
def bstack11lll1ll1l_opy_(context, bstack1llll1l11l_opy_):
  try:
    if getattr(context, bstack11l1l11_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭୶"), None):
      context.page.evaluate(bstack11l1l11_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥ୷"), bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠧ୸")+ json.dumps(bstack1llll1l11l_opy_) + bstack11l1l11_opy_ (u"ࠦࢂࢃࠢ୹"))
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡼࡿ࠽ࠤࢀࢃࠢ୺").format(str(e), traceback.format_exc()))
def bstack1lll1l1l1l_opy_(context, message, level):
  try:
    if getattr(context, bstack11l1l11_opy_ (u"࠭ࡰࡢࡩࡨࠫ୻"), None):
      context.page.evaluate(bstack11l1l11_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣ୼"), bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭୽") + json.dumps(message) + bstack11l1l11_opy_ (u"ࠩ࠯ࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠬ୾") + json.dumps(level) + bstack11l1l11_opy_ (u"ࠪࢁࢂ࠭୿"))
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡢࡰࡱࡳࡹࡧࡴࡪࡱࡱࠤࢀࢃ࠺ࠡࡽࢀࠦ஀").format(str(e), traceback.format_exc()))
@measure(event_name=EVENTS.bstack1l1ll1ll1l_opy_, stage=STAGE.bstack1l11l1l11l_opy_, bstack1l111l11l_opy_=bstack1ll1ll11l1_opy_)
def bstack1l11ll111_opy_(self, url):
  global bstack1lll111ll_opy_
  try:
    bstack11llll1ll1_opy_(url)
  except Exception as err:
    logger.debug(bstack1lllll111l_opy_.format(str(err)))
  try:
    bstack1lll111ll_opy_(self, url)
  except Exception as e:
    try:
      bstack111llllll_opy_ = str(e)
      if any(err_msg in bstack111llllll_opy_ for err_msg in bstack11l11lll11_opy_):
        bstack11llll1ll1_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1lllll111l_opy_.format(str(err)))
    raise e
def bstack1l1ll1llll_opy_(self):
  global bstack111111lll_opy_
  bstack111111lll_opy_ = self
  return
def bstack1l1l11l11_opy_(self):
  global bstack1l11l1llll_opy_
  bstack1l11l1llll_opy_ = self
  return
def bstack1ll11ll11_opy_(test_name, bstack11111l11_opy_):
  global CONFIG
  if percy.bstack1l1111ll11_opy_() == bstack11l1l11_opy_ (u"ࠧࡺࡲࡶࡧࠥ஁"):
    bstack1ll1l1ll_opy_ = os.path.relpath(bstack11111l11_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack1ll1l1ll_opy_)
    bstack1l111l11l_opy_ = suite_name + bstack11l1l11_opy_ (u"ࠨ࠭ࠣஂ") + test_name
    threading.current_thread().percySessionName = bstack1l111l11l_opy_
def bstack1ll11llll1_opy_(self, test, *args, **kwargs):
  global bstack1ll111l111_opy_
  test_name = None
  bstack11111l11_opy_ = None
  if test:
    test_name = str(test.name)
    bstack11111l11_opy_ = str(test.source)
  bstack1ll11ll11_opy_(test_name, bstack11111l11_opy_)
  bstack1ll111l111_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.bstack1l1ll1l1ll_opy_, stage=STAGE.bstack1l11l1l11l_opy_, bstack1l111l11l_opy_=bstack1ll1ll11l1_opy_)
def bstack1l11l111_opy_(driver, bstack1l111l11l_opy_):
  if not bstack11lll11111_opy_ and bstack1l111l11l_opy_:
      bstack1l1lll1l1_opy_ = {
          bstack11l1l11_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧஃ"): bstack11l1l11_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ஄"),
          bstack11l1l11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬஅ"): {
              bstack11l1l11_opy_ (u"ࠪࡲࡦࡳࡥࠨஆ"): bstack1l111l11l_opy_
          }
      }
      bstack11l11lll1_opy_ = bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩஇ").format(json.dumps(bstack1l1lll1l1_opy_))
      driver.execute_script(bstack11l11lll1_opy_)
  if bstack11l11l11ll_opy_:
      bstack111ll11l1_opy_ = {
          bstack11l1l11_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬஈ"): bstack11l1l11_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨஉ"),
          bstack11l1l11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪஊ"): {
              bstack11l1l11_opy_ (u"ࠨࡦࡤࡸࡦ࠭஋"): bstack1l111l11l_opy_ + bstack11l1l11_opy_ (u"ࠩࠣࡴࡦࡹࡳࡦࡦࠤࠫ஌"),
              bstack11l1l11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ஍"): bstack11l1l11_opy_ (u"ࠫ࡮ࡴࡦࡰࠩஎ")
          }
      }
      if bstack11l11l11ll_opy_.status == bstack11l1l11_opy_ (u"ࠬࡖࡁࡔࡕࠪஏ"):
          bstack1ll1l11l1l_opy_ = bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫஐ").format(json.dumps(bstack111ll11l1_opy_))
          driver.execute_script(bstack1ll1l11l1l_opy_)
          bstack11lll1l11l_opy_(driver, bstack11l1l11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ஑"))
      elif bstack11l11l11ll_opy_.status == bstack11l1l11_opy_ (u"ࠨࡈࡄࡍࡑ࠭ஒ"):
          reason = bstack11l1l11_opy_ (u"ࠤࠥஓ")
          bstack11ll1111l1_opy_ = bstack1l111l11l_opy_ + bstack11l1l11_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠫஔ")
          if bstack11l11l11ll_opy_.message:
              reason = str(bstack11l11l11ll_opy_.message)
              bstack11ll1111l1_opy_ = bstack11ll1111l1_opy_ + bstack11l1l11_opy_ (u"ࠫࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠫக") + reason
          bstack111ll11l1_opy_[bstack11l1l11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ஖")] = {
              bstack11l1l11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ஗"): bstack11l1l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭஘"),
              bstack11l1l11_opy_ (u"ࠨࡦࡤࡸࡦ࠭ங"): bstack11ll1111l1_opy_
          }
          bstack1ll1l11l1l_opy_ = bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧச").format(json.dumps(bstack111ll11l1_opy_))
          driver.execute_script(bstack1ll1l11l1l_opy_)
          bstack11lll1l11l_opy_(driver, bstack11l1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ஛"), reason)
          bstack111l1l1l11_opy_(reason, str(bstack11l11l11ll_opy_), str(bstack11ll1l111_opy_), logger)
@measure(event_name=EVENTS.bstack1lll11llll_opy_, stage=STAGE.bstack1l11l1l11l_opy_, bstack1l111l11l_opy_=bstack1ll1ll11l1_opy_)
def bstack1ll111lll1_opy_(driver, test):
  if percy.bstack1l1111ll11_opy_() == bstack11l1l11_opy_ (u"ࠦࡹࡸࡵࡦࠤஜ") and percy.bstack11l1ll111l_opy_() == bstack11l1l11_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢ஝"):
      bstack1l1111l11l_opy_ = bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"࠭ࡰࡦࡴࡦࡽࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩஞ"), None)
      bstack111ll1l1l1_opy_(driver, bstack1l1111l11l_opy_, test)
  if (bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫட"), None) and
      bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ஠"), None)) or (
      bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ஡"), None) and
      bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ஢"), None)):
      logger.info(bstack11l1l11_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠢࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡮ࡹࠠࡶࡰࡧࡩࡷࡽࡡࡺ࠰ࠣࠦண"))
      bstack1l111ll111_opy_.bstack1l111ll1l1_opy_(driver, name=test.name, path=test.source)
def bstack1ll1l11ll1_opy_(test, bstack1l111l11l_opy_):
    try:
      bstack111l11l1l1_opy_ = datetime.datetime.now()
      data = {}
      if test:
        data[bstack11l1l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪத")] = bstack1l111l11l_opy_
      if bstack11l11l11ll_opy_:
        if bstack11l11l11ll_opy_.status == bstack11l1l11_opy_ (u"࠭ࡐࡂࡕࡖࠫ஥"):
          data[bstack11l1l11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ஦")] = bstack11l1l11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ஧")
        elif bstack11l11l11ll_opy_.status == bstack11l1l11_opy_ (u"ࠩࡉࡅࡎࡒࠧந"):
          data[bstack11l1l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪன")] = bstack11l1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫப")
          if bstack11l11l11ll_opy_.message:
            data[bstack11l1l11_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ஫")] = str(bstack11l11l11ll_opy_.message)
      user = CONFIG[bstack11l1l11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ஬")]
      key = CONFIG[bstack11l1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ஭")]
      host = bstack1ll11l1l11_opy_(cli.config, [bstack11l1l11_opy_ (u"ࠣࡣࡳ࡭ࡸࠨம"), bstack11l1l11_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨࠦய"), bstack11l1l11_opy_ (u"ࠥࡥࡵ࡯ࠢர")], bstack11l1l11_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠧற"))
      url = bstack11l1l11_opy_ (u"ࠬࢁࡽ࠰ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡷࡪࡹࡳࡪࡱࡱࡷ࠴ࢁࡽ࠯࡬ࡶࡳࡳ࠭ல").format(host, bstack1ll1l1111l_opy_)
      headers = {
        bstack11l1l11_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡵࡻࡳࡩࠬள"): bstack11l1l11_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪழ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers, auth=(user, key))
        cli.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠣࡪࡷࡸࡵࡀࡵࡱࡦࡤࡸࡪࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡹࡴࡢࡶࡸࡷࠧவ"), datetime.datetime.now() - bstack111l11l1l1_opy_)
    except Exception as e:
      logger.error(bstack11ll1lll_opy_.format(str(e)))
def bstack1lll111l11_opy_(test, bstack1l111l11l_opy_):
  global CONFIG
  global bstack1l11l1llll_opy_
  global bstack111111lll_opy_
  global bstack1ll1l1111l_opy_
  global bstack11l11l11ll_opy_
  global bstack1ll1ll11l1_opy_
  global bstack1l11llll11_opy_
  global bstack1l1lllllll_opy_
  global bstack1l111l111l_opy_
  global bstack1l11llll1_opy_
  global bstack1ll1111ll1_opy_
  global bstack1ll11ll11l_opy_
  global bstack11ll1l1ll1_opy_
  try:
    if not bstack1ll1l1111l_opy_:
      with bstack11ll1l1ll1_opy_:
        bstack1ll1111l_opy_ = os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"ࠩࢁࠫஶ")), bstack11l1l11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪஷ"), bstack11l1l11_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭ஸ"))
        if os.path.exists(bstack1ll1111l_opy_):
          with open(bstack1ll1111l_opy_, bstack11l1l11_opy_ (u"ࠬࡸࠧஹ")) as f:
            content = f.read().strip()
            if content:
              bstack1lllll11l_opy_ = json.loads(bstack11l1l11_opy_ (u"ࠨࡻࠣ஺") + content + bstack11l1l11_opy_ (u"ࠧࠣࡺࠥ࠾ࠥࠨࡹࠣࠩ஻") + bstack11l1l11_opy_ (u"ࠣࡿࠥ஼"))
              bstack1ll1l1111l_opy_ = bstack1lllll11l_opy_.get(str(threading.get_ident()))
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡴࡨࡥࡩ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡍࡉࡹࠠࡧ࡫࡯ࡩ࠿ࠦࠧ஽") + str(e))
  if not is_robot_playwright_installed():
    if bstack1ll1111ll1_opy_:
      with bstack1lllllll11_opy_:
        bstack1lll1l11_opy_ = bstack1ll1111ll1_opy_.copy()
      for driver in bstack1lll1l11_opy_:
        if bstack1ll1l1111l_opy_ == driver.session_id:
          if test:
            bstack1ll111lll1_opy_(driver, test)
          bstack1l11l111_opy_(driver, bstack1l111l11l_opy_)
    elif bstack1ll1l1111l_opy_:
      bstack1ll1l11ll1_opy_(test, bstack1l111l11l_opy_)
    if bstack1l11l1llll_opy_:
      bstack1l1lllllll_opy_(bstack1l11l1llll_opy_)
    if bstack111111lll_opy_:
      bstack1l111l111l_opy_(bstack111111lll_opy_)
    if bstack11l11ll11_opy_:
      bstack1l11llll1_opy_()
def bstack1l1lll11l1_opy_(self, test, *args, **kwargs):
  bstack1l111l11l_opy_ = None
  if test:
    bstack1l111l11l_opy_ = str(test.name)
  bstack1lll111l11_opy_(test, bstack1l111l11l_opy_)
  bstack1l11llll11_opy_(self, test, *args, **kwargs)
def bstack11lll1111l_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1lll111lll_opy_
  global CONFIG
  global bstack1ll1111ll1_opy_
  global bstack1ll1l1111l_opy_
  global bstack11ll1l1ll1_opy_
  bstack1l1ll1ll1_opy_ = None
  try:
    if bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩா"), None) or bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ி"), None):
      try:
        if not bstack1ll1l1111l_opy_:
          bstack1ll1111l_opy_ = os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"ࠬࢄࠧீ")), bstack11l1l11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ு"), bstack11l1l11_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩூ"))
          with bstack11ll1l1ll1_opy_:
            if os.path.exists(bstack1ll1111l_opy_):
              with open(bstack1ll1111l_opy_, bstack11l1l11_opy_ (u"ࠨࡴࠪ௃")) as f:
                content = f.read().strip()
                if content:
                  bstack1lllll11l_opy_ = json.loads(bstack11l1l11_opy_ (u"ࠤࡾࠦ௄") + content + bstack11l1l11_opy_ (u"ࠪࠦࡽࠨ࠺ࠡࠤࡼࠦࠬ௅") + bstack11l1l11_opy_ (u"ࠦࢂࠨெ"))
                  bstack1ll1l1111l_opy_ = bstack1lllll11l_opy_.get(str(threading.get_ident()))
      except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡷ࡫ࡡࡥ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡉࡅࡵࠣࡪ࡮ࡲࡥࠡ࡫ࡱࠤࡹ࡫ࡳࡵࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࠫே") + str(e))
      if bstack1ll1111ll1_opy_:
        with bstack1lllllll11_opy_:
          bstack1lll1l11_opy_ = bstack1ll1111ll1_opy_.copy()
        for driver in bstack1lll1l11_opy_:
          if bstack1ll1l1111l_opy_ == driver.session_id:
            bstack1l1ll1ll1_opy_ = driver
    bstack1l1lll11ll_opy_ = bstack1l111ll111_opy_.bstack11ll1lll1l_opy_(test.tags)
    if bstack1l1ll1ll1_opy_:
      threading.current_thread().isA11yTest = bstack1l111ll111_opy_.bstack111ll1ll11_opy_(bstack1l1ll1ll1_opy_, bstack1l1lll11ll_opy_)
      threading.current_thread().isAppA11yTest = bstack1l111ll111_opy_.bstack111ll1ll11_opy_(bstack1l1ll1ll1_opy_, bstack1l1lll11ll_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1l1lll11ll_opy_
      threading.current_thread().isAppA11yTest = bstack1l1lll11ll_opy_
  except:
    pass
  bstack1lll111lll_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack11l11l11ll_opy_
  try:
    bstack11l11l11ll_opy_ = self._test
  except:
    bstack11l11l11ll_opy_ = self.test
def bstack1l1l11l111_opy_():
  global bstack11l1l111l1_opy_
  try:
    if os.path.exists(bstack11l1l111l1_opy_):
      os.remove(bstack11l1l111l1_opy_)
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡦࡨࡰࡪࡺࡩ࡯ࡩࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺ࠡࠩை") + str(e))
def bstack1ll1l1ll11_opy_():
  global bstack11l1l111l1_opy_
  bstack11lll1l1l1_opy_ = {}
  lock_file = bstack11l1l111l1_opy_ + bstack11l1l11_opy_ (u"ࠧ࠯࡮ࡲࡧࡰ࠭௉")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack11l1l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡲ࡯ࡤ࡭ࠣࡲࡴࡺࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧ࠯ࠤࡺࡹࡩ࡯ࡩࠣࡦࡦࡹࡩࡤࠢࡩ࡭ࡱ࡫ࠠࡰࡲࡨࡶࡦࡺࡩࡰࡰࡶࠫொ"))
    try:
      if not os.path.isfile(bstack11l1l111l1_opy_):
        with open(bstack11l1l111l1_opy_, bstack11l1l11_opy_ (u"ࠩࡺࠫோ")) as f:
          json.dump({}, f)
      if os.path.exists(bstack11l1l111l1_opy_):
        with open(bstack11l1l111l1_opy_, bstack11l1l11_opy_ (u"ࠪࡶࠬௌ")) as f:
          content = f.read().strip()
          if content:
            bstack11lll1l1l1_opy_ = json.loads(content)
    except Exception as e:
      logger.debug(bstack11l1l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡲࡦࡣࡧ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾்ࠥ࠭") + str(e))
    return bstack11lll1l1l1_opy_
  try:
    os.makedirs(os.path.dirname(bstack11l1l111l1_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      if not os.path.isfile(bstack11l1l111l1_opy_):
        with open(bstack11l1l111l1_opy_, bstack11l1l11_opy_ (u"ࠬࡽࠧ௎")) as f:
          json.dump({}, f)
      if os.path.exists(bstack11l1l111l1_opy_):
        with open(bstack11l1l111l1_opy_, bstack11l1l11_opy_ (u"࠭ࡲࠨ௏")) as f:
          content = f.read().strip()
          if content:
            bstack11lll1l1l1_opy_ = json.loads(content)
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡵࡩࡦࡪࡩ࡯ࡩࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺ࠡࠩௐ") + str(e))
  finally:
    return bstack11lll1l1l1_opy_
def bstack111ll11l_opy_(platform_index, item_index):
  global bstack11l1l111l1_opy_
  lock_file = bstack11l1l111l1_opy_ + bstack11l1l11_opy_ (u"ࠨ࠰࡯ࡳࡨࡱࠧ௑")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack11l1l11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡬ࡰࡥ࡮ࠤࡳࡵࡴࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨ࠰ࠥࡻࡳࡪࡰࡪࠤࡧࡧࡳࡪࡥࠣࡪ࡮ࡲࡥࠡࡱࡳࡩࡷࡧࡴࡪࡱࡱࡷࠬ௒"))
    try:
      bstack11lll1l1l1_opy_ = {}
      if os.path.exists(bstack11l1l111l1_opy_):
        with open(bstack11l1l111l1_opy_, bstack11l1l11_opy_ (u"ࠪࡶࠬ௓")) as f:
          content = f.read().strip()
          if content:
            bstack11lll1l1l1_opy_ = json.loads(content)
      bstack11lll1l1l1_opy_[item_index] = platform_index
      with open(bstack11l1l111l1_opy_, bstack11l1l11_opy_ (u"ࠦࡼࠨ௔")) as outfile:
        json.dump(bstack11lll1l1l1_opy_, outfile)
    except Exception as e:
      logger.debug(bstack11l1l11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡸࡴ࡬ࡸ࡮ࡴࡧࠡࡶࡲࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪ௕") + str(e))
    return
  try:
    os.makedirs(os.path.dirname(bstack11l1l111l1_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      bstack11lll1l1l1_opy_ = {}
      if os.path.exists(bstack11l1l111l1_opy_):
        with open(bstack11l1l111l1_opy_, bstack11l1l11_opy_ (u"࠭ࡲࠨ௖")) as f:
          content = f.read().strip()
          if content:
            bstack11lll1l1l1_opy_ = json.loads(content)
      bstack11lll1l1l1_opy_[item_index] = platform_index
      with open(bstack11l1l111l1_opy_, bstack11l1l11_opy_ (u"ࠢࡸࠤௗ")) as outfile:
        json.dump(bstack11lll1l1l1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡻࡷ࡯ࡴࡪࡰࡪࠤࡹࡵࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭௘") + str(e))
def bstack1ll1l1l11l_opy_(bstack1l11l1l1ll_opy_):
  global CONFIG
  bstack1111l1l1l_opy_ = bstack11l1l11_opy_ (u"ࠩࠪ௙")
  if not bstack11l1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭௚") in CONFIG:
    logger.info(bstack11l1l11_opy_ (u"ࠫࡓࡵࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠣࡴࡦࡹࡳࡦࡦࠣࡹࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡴࡨࡴࡴࡸࡴࠡࡨࡲࡶࠥࡘ࡯ࡣࡱࡷࠤࡷࡻ࡮ࠨ௛"))
  try:
    platform = CONFIG[bstack11l1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ௜")][bstack1l11l1l1ll_opy_]
    if bstack11l1l11_opy_ (u"࠭࡯ࡴࠩ௝") in platform:
      bstack1111l1l1l_opy_ += str(platform[bstack11l1l11_opy_ (u"ࠧࡰࡵࠪ௞")]) + bstack11l1l11_opy_ (u"ࠨ࠮ࠣࠫ௟")
    if bstack11l1l11_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬ௠") in platform:
      bstack1111l1l1l_opy_ += str(platform[bstack11l1l11_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭௡")]) + bstack11l1l11_opy_ (u"ࠫ࠱ࠦࠧ௢")
    if bstack11l1l11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩ௣") in platform:
      bstack1111l1l1l_opy_ += str(platform[bstack11l1l11_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪ௤")]) + bstack11l1l11_opy_ (u"ࠧ࠭ࠢࠪ௥")
    if bstack11l1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪ௦") in platform:
      bstack1111l1l1l_opy_ += str(platform[bstack11l1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ௧")]) + bstack11l1l11_opy_ (u"ࠪ࠰ࠥ࠭௨")
    if bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ௩") in platform:
      bstack1111l1l1l_opy_ += str(platform[bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ௪")]) + bstack11l1l11_opy_ (u"࠭ࠬࠡࠩ௫")
    if bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ௬") in platform:
      bstack1111l1l1l_opy_ += str(platform[bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ௭")]) + bstack11l1l11_opy_ (u"ࠩ࠯ࠤࠬ௮")
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"ࠪࡗࡴࡳࡥࠡࡧࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡳ࡭ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡶࡸࡷ࡯࡮ࡨࠢࡩࡳࡷࠦࡲࡦࡲࡲࡶࡹࠦࡧࡦࡰࡨࡶࡦࡺࡩࡰࡰࠪ௯") + str(e))
  finally:
    if bstack1111l1l1l_opy_[len(bstack1111l1l1l_opy_) - 2:] == bstack11l1l11_opy_ (u"ࠫ࠱ࠦࠧ௰"):
      bstack1111l1l1l_opy_ = bstack1111l1l1l_opy_[:-2]
    return bstack1111l1l1l_opy_
def bstack1l11l1111_opy_(path, bstack1111l1l1l_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack11l11ll1l1_opy_ = ET.parse(path)
    bstack11lllll11l_opy_ = bstack11l11ll1l1_opy_.getroot()
    bstack11111111l_opy_ = None
    for suite in bstack11lllll11l_opy_.iter(bstack11l1l11_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫ௱")):
      if bstack11l1l11_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭௲") in suite.attrib:
        suite.attrib[bstack11l1l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ௳")] += bstack11l1l11_opy_ (u"ࠨࠢࠪ௴") + bstack1111l1l1l_opy_
        bstack11111111l_opy_ = suite
    bstack11llll1111_opy_ = None
    for robot in bstack11lllll11l_opy_.iter(bstack11l1l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ௵")):
      bstack11llll1111_opy_ = robot
    bstack11lll1llll_opy_ = len(bstack11llll1111_opy_.findall(bstack11l1l11_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩ௶")))
    if bstack11lll1llll_opy_ == 1:
      bstack11llll1111_opy_.remove(bstack11llll1111_opy_.findall(bstack11l1l11_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪ௷"))[0])
      bstack11l111llll_opy_ = ET.Element(bstack11l1l11_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫ௸"), attrib={bstack11l1l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ௹"): bstack11l1l11_opy_ (u"ࠧࡔࡷ࡬ࡸࡪࡹࠧ௺"), bstack11l1l11_opy_ (u"ࠨ࡫ࡧࠫ௻"): bstack11l1l11_opy_ (u"ࠩࡶ࠴ࠬ௼")})
      bstack11llll1111_opy_.insert(1, bstack11l111llll_opy_)
      bstack111111l1l_opy_ = None
      for suite in bstack11llll1111_opy_.iter(bstack11l1l11_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩ௽")):
        bstack111111l1l_opy_ = suite
      bstack111111l1l_opy_.append(bstack11111111l_opy_)
      bstack1111ll11l_opy_ = None
      for status in bstack11111111l_opy_.iter(bstack11l1l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ௾")):
        bstack1111ll11l_opy_ = status
      bstack111111l1l_opy_.append(bstack1111ll11l_opy_)
    bstack11l11ll1l1_opy_.write(path)
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡵࡷ࡮ࡴࡧࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡱࡩࡷࡧࡴࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠪ௿") + str(e))
def bstack11lllll111_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack11l111l11l_opy_
  global CONFIG
  if bstack11l1l11_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡶࡡࡵࡪࠥఀ") in options:
    del options[bstack11l1l11_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡰࡢࡶ࡫ࠦఁ")]
  bstack1l1lll1ll_opy_ = bstack1ll1l1ll11_opy_()
  for item_id in bstack1l1lll1ll_opy_.keys():
    path = os.path.join(outs_dir, str(item_id), bstack11l1l11_opy_ (u"ࠨࡱࡸࡸࡵࡻࡴ࠯ࡺࡰࡰࠬం"))
    bstack1l11l1111_opy_(path, bstack1ll1l1l11l_opy_(bstack1l1lll1ll_opy_[item_id]))
  bstack1l1l11l111_opy_()
  return bstack11l111l11l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack111lll1l1_opy_(self, ff_profile_dir):
  global bstack1lll111111_opy_
  if not ff_profile_dir:
    return None
  return bstack1lll111111_opy_(self, ff_profile_dir)
def bstack11lll111l_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1l1l1l1ll1_opy_
  bstack1l11lll11_opy_ = []
  if bstack11l1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬః") in CONFIG:
    bstack1l11lll11_opy_ = CONFIG[bstack11l1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ఄ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack11l1l11_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࠧఅ")],
      pabot_args[bstack11l1l11_opy_ (u"ࠧࡼࡥࡳࡤࡲࡷࡪࠨఆ")],
      argfile,
      pabot_args.get(bstack11l1l11_opy_ (u"ࠨࡨࡪࡸࡨࠦఇ")),
      pabot_args[bstack11l1l11_opy_ (u"ࠢࡱࡴࡲࡧࡪࡹࡳࡦࡵࠥఈ")],
      platform[0],
      bstack1l1l1l1ll1_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack11l1l11_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡩ࡭ࡱ࡫ࡳࠣఉ")] or [(bstack11l1l11_opy_ (u"ࠤࠥఊ"), None)]
    for platform in enumerate(bstack1l11lll11_opy_)
  ]
def bstack1l11l1l1l1_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1lll1l1lll_opy_=bstack11l1l11_opy_ (u"ࠪࠫఋ")):
  global bstack11l111lll1_opy_
  self.platform_index = platform_index
  self.bstack1ll1l1l11_opy_ = bstack1lll1l1lll_opy_
  bstack11l111lll1_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1l11ll1l1l_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1l1l111ll1_opy_
  global bstack1ll111l11l_opy_
  bstack11111ll1l_opy_ = copy.deepcopy(item)
  if not bstack11l1l11_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ఌ") in item.options:
    bstack11111ll1l_opy_.options[bstack11l1l11_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ఍")] = []
  bstack1l11111lll_opy_ = bstack11111ll1l_opy_.options[bstack11l1l11_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨఎ")].copy()
  for v in bstack11111ll1l_opy_.options[bstack11l1l11_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩఏ")]:
    if bstack11l1l11_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡑࡎࡄࡘࡋࡕࡒࡎࡋࡑࡈࡊ࡞ࠧఐ") in v:
      bstack1l11111lll_opy_.remove(v)
    if bstack11l1l11_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡅࡏࡍࡆࡘࡇࡔࠩ఑") in v:
      bstack1l11111lll_opy_.remove(v)
    if bstack11l1l11_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡇࡉࡋࡒࡏࡄࡃࡏࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧఒ") in v:
      bstack1l11111lll_opy_.remove(v)
  bstack1l11111lll_opy_.insert(0, bstack11l1l11_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚࠽ࡿࢂ࠭ఓ").format(bstack11111ll1l_opy_.platform_index))
  bstack1l11111lll_opy_.insert(0, bstack11l1l11_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡉࡋࡆࡍࡑࡆࡅࡑࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓ࠼ࡾࢁࠬఔ").format(bstack11111ll1l_opy_.bstack1ll1l1l11_opy_))
  bstack11111ll1l_opy_.options[bstack11l1l11_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨక")] = bstack1l11111lll_opy_
  if bstack1ll111l11l_opy_:
    bstack11111ll1l_opy_.options[bstack11l1l11_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩఖ")].insert(0, bstack11l1l11_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓ࠻ࡽࢀࠫగ").format(bstack1ll111l11l_opy_))
  return bstack1l1l111ll1_opy_(caller_id, datasources, is_last, bstack11111ll1l_opy_, outs_dir)
def bstack1l11l1111l_opy_(command, item_index):
  try:
    if global_config.get_property(bstack11l1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪఘ")):
      os.environ[bstack11l1l11_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫఙ")] = json.dumps(CONFIG[bstack11l1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧచ")][item_index % bstack11ll111l1_opy_])
    global bstack1ll111l11l_opy_
    os.environ[bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬఛ")] = str(item_index % bstack11ll111l1_opy_)
    listener_arg = bstack11l1l11_opy_ (u"࠭ࠧజ")
    if is_robot_playwright_installed() and cli.is_enabled(CONFIG):
      listener_arg = bstack11l1l11_opy_ (u"ࠧࠡ࠯࠰ࡰ࡮ࡹࡴࡦࡰࡨࡶࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡸࡪ࡫࠯ࡴࡲࡦࡴࡺ࡟࡭࡫ࡶࡸࡪࡴࡥࡳࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠴ࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡓࡥࡹࡩࡨࡦࡴࠪఝ")
      logger.debug(bstack11l1l11_opy_ (u"ࠣࡃࡧࡨ࡮ࡴࡧࠡࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡕࡧࡴࡤࡪࡨࡶࠥࡲࡩࡴࡶࡨࡲࡪࡸࠠࡧࡱࡵࠤ࡮ࡺࡥ࡮ࠢࡾࢁࠧఞ").format(item_index))
    if bstack1ll111l11l_opy_:
      command[0] = command[0].replace(bstack11l1l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨట"), bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡶࡨࡰࠦࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠠ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࠣࠫఠ") + str(item_index % bstack11ll111l1_opy_) + bstack11l1l11_opy_ (u"ࠫࠥ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠤࠬడ") + str(
        item_index)  + listener_arg + bstack11l1l11_opy_ (u"ࠬࠦࠧఢ") + bstack1ll111l11l_opy_, 1)
    else:
      command[0] = command[0].replace(bstack11l1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬణ"),
                                      bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡳࡥ࡭ࠣࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠤ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࠠࠨత") +  str(item_index % bstack11ll111l1_opy_) + bstack11l1l11_opy_ (u"ࠨࠢ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠡࠩథ") + str(item_index)  + listener_arg, 1)
  except Exception as e:
    logger.error(bstack11l1l11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡯ࡲࡨ࡮࡬ࡹࡪࡰࡪࠤࡨࡵ࡭࡮ࡣࡱࡨࠥ࡬࡯ࡳࠢࡳࡥࡧࡵࡴࠡࡴࡸࡲ࠿ࠦࡻࡾࠩద").format(str(e)))
def bstack1ll111ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack111l1l111_opy_
  try:
    bstack1l11l1111l_opy_(command, item_index)
    return bstack111l1l111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
  except Exception as e:
    logger.error(bstack11l1l11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡣࡱࡷࠤࡷࡻ࡮࠻ࠢࡾࢁࠬధ").format(str(e)))
    raise e
def bstack1l1lll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack111l1l111_opy_
  try:
    bstack1l11l1111l_opy_(command, item_index)
    return bstack111l1l111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
  except Exception as e:
    logger.error(bstack11l1l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡢࡤࡲࡸࠥࡸࡵ࡯ࠢ࠵࠲࠶࠹࠺ࠡࡽࢀࠫన").format(str(e)))
    try:
      return bstack111l1l111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
    except Exception as e2:
      logger.error(bstack11l1l11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡥࡳࡹࠦ࠲࠯࠳࠶ࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࡼࡿࠪ఩").format(str(e2)))
      raise e
def bstack11ll1l1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack111l1l111_opy_
  try:
    bstack1l11l1111l_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    return bstack111l1l111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
  except Exception as e:
    logger.error(bstack11l1l11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠࡳࡷࡱࠤ࠷࠴࠱࠶࠼ࠣࡿࢂ࠭ప").format(str(e)))
    try:
      return bstack111l1l111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
    except Exception as e2:
      logger.error(bstack11l1l11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡧࡵࡴࠡ࠴࠱࠵࠺ࠦࡦࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢࡾࢁࠬఫ").format(str(e2)))
      raise e
def _111lllll11_opy_(bstack111lll11_opy_, item_index, process_timeout, sleep_before_start, bstack1l1lll111_opy_):
  bstack1l11l1111l_opy_(bstack111lll11_opy_, item_index)
  if process_timeout is None:
    process_timeout = 3600
  if sleep_before_start and sleep_before_start > 0:
    time.sleep(min(sleep_before_start, 5))
  return process_timeout
def bstack1lll1l1ll_opy_(command, bstack1l1l11111_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack111l1l111_opy_
  global bstack1l11lllll1_opy_
  global bstack1ll111l11l_opy_
  try:
    for env_name, bstack11l1111l_opy_ in bstack1l11lllll1_opy_.items():
      os.environ[env_name] = bstack11l1111l_opy_
    bstack1ll111l11l_opy_ = bstack11l1l11_opy_ (u"ࠣࠤబ")
    bstack1l11l1111l_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    if sleep_before_start and sleep_before_start > 0:
      time.sleep(min(sleep_before_start, 5))
    return bstack111l1l111_opy_(command, bstack1l1l11111_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack11l1l11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡢࡰࡶࠣࡶࡺࡴࠠ࠶࠰࠳࠾ࠥࢁࡽࠨభ").format(str(e)))
    try:
      return bstack111l1l111_opy_(command, bstack1l1l11111_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack11l1l11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡣࡱࡷࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࡼࡿࠪమ").format(str(e2)))
      raise e
def bstack1l1l11llll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack111l1l111_opy_
  try:
    process_timeout = _111lllll11_opy_(command, item_index, process_timeout, sleep_before_start, bstack11l1l11_opy_ (u"ࠫ࠹࠴࠲ࠨయ"))
    return bstack111l1l111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack11l1l11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡥࡳࡹࠦࡲࡶࡰࠣ࠸࠳࠸࠺ࠡࡽࢀࠫర").format(str(e)))
    try:
      return bstack111l1l111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack11l1l11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠࡧࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣࡿࢂ࠭ఱ").format(str(e2)))
      raise e
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack11l111l11_opy_(self, runner, quiet=False, capture=True):
  global bstack111l1111ll_opy_
  bstack11ll11l11_opy_ = bstack111l1111ll_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack11l1l11_opy_ (u"ࠧࡦࡺࡦࡩࡵࡺࡩࡰࡰࡢࡥࡷࡸࠧల")):
      runner.exception_arr = []
    if not hasattr(runner, bstack11l1l11_opy_ (u"ࠨࡧࡻࡧࡤࡺࡲࡢࡥࡨࡦࡦࡩ࡫ࡠࡣࡵࡶࠬళ")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack11ll11l11_opy_
def bstack11llll11_opy_(runner, hook_name, context, element, bstack11111lll_opy_, *args):
  global bstack1ll1lll1ll_opy_
  try:
    if runner.hooks.get(hook_name):
      bstack1llllll1l1_opy_.bstack1l1ll11l_opy_(hook_name, element)
    if bstack1ll1lll1ll_opy_ is None or bstack1ll1lll1ll_opy_:
      bstack11111lll_opy_(runner, hook_name, context, *args)
    else:
      bstack111l111l1l_opy_ = (context,) + args
      bstack11111lll_opy_(runner, hook_name, *bstack111l111l1l_opy_)
    if runner.hooks.get(hook_name):
      bstack1llllll1l1_opy_.bstack1l1l1ll1_opy_(element)
      if hook_name not in [bstack11l1l11_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱ࠭ఴ"), bstack11l1l11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ࠭వ")] and args and hasattr(args[0], bstack11l1l11_opy_ (u"ࠫࡪࡸࡲࡰࡴࡢࡱࡪࡹࡳࡢࡩࡨࠫశ")):
        args[0].error_message = bstack11l1l11_opy_ (u"ࠬ࠭ష")
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢ࡫ࡥࡳࡪ࡬ࡦࠢ࡫ࡳࡴࡱࡳࠡ࡫ࡱࠤࡧ࡫ࡨࡢࡸࡨ࠾ࠥࢁࡽࠨస").format(str(e)))
@measure(event_name=EVENTS.bstack11l1l11l1l_opy_, stage=STAGE.bstack1l11l1l11l_opy_, hook_type=bstack11l1l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࡁ࡭࡮ࠥహ"), bstack1l111l11l_opy_=bstack1ll1ll11l1_opy_)
def bstack1l1llll11_opy_(runner, name, context, bstack11111lll_opy_, *args):
    if runner.hooks.get(bstack11l1l11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧ఺")).__name__ != bstack11l1l11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࡥࡤࡦࡨࡤࡹࡱࡺ࡟ࡩࡱࡲ࡯ࠧ఻"):
      bstack11llll11_opy_(runner, name, context, runner, bstack11111lll_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack11l1l111l_opy_(bstack11l1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳ఼ࠩ")) else context.browser
      runner.driver_initialised = bstack11l1l11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣఽ")
    except Exception as e:
      logger.debug(bstack11l1l11_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡪࡲࡪࡸࡨࡶࠥ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡳࡦࠢࡤࡸࡹࡸࡩࡣࡷࡷࡩ࠿ࠦࡻࡾࠩా").format(str(e)))
def bstack11l111l1l1_opy_(runner, name, context, bstack11111lll_opy_, *args):
    bstack11llll11_opy_(runner, name, context, context.feature, bstack11111lll_opy_, *args)
    try:
      if not bstack11lll11111_opy_:
        bstack1l1ll1ll1_opy_ = threading.current_thread().bstackSessionDriver if bstack11l1l111l_opy_(bstack11l1l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬి")) else context.browser
        if is_driver_active(bstack1l1ll1ll1_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack11l1l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣీ")
          bstack1llll1l11l_opy_ = str(runner.feature.name)
          bstack11lll1ll1l_opy_(context, bstack1llll1l11l_opy_)
          bstack1l1ll1ll1_opy_.execute_script(bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭ు") + json.dumps(bstack1llll1l11l_opy_) + bstack11l1l11_opy_ (u"ࠩࢀࢁࠬూ"))
    except Exception as e:
      logger.debug(bstack11l1l11_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡬ࡥࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪృ").format(str(e)))
def bstack1l1l1111_opy_(runner, name, context, bstack11111lll_opy_, *args):
    target = context.scenario if hasattr(context, bstack11l1l11_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ౄ")) else context.feature
    bstack11llll11_opy_(runner, name, context, target, bstack11111lll_opy_, *args)
@measure(event_name=EVENTS.bstack11111lll1_opy_, stage=STAGE.bstack1l11l1l11l_opy_, bstack1l111l11l_opy_=bstack1ll1ll11l1_opy_)
def bstack11lll11l1l_opy_(runner, name, context, bstack11111lll_opy_, *args):
    bstack1llllll1l1_opy_.start_test(context)
    bstack11llll11_opy_(runner, name, context, context.scenario, bstack11111lll_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack1l11l1ll1l_opy_.bstack1ll1ll1ll_opy_(context, *args)
    try:
      bstack1l1ll1ll1_opy_ = bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ౅"), context.browser)
      if is_driver_active(bstack1l1ll1ll1_opy_):
        TestHubHandler.bstack1lllll1ll1_opy_(bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬె"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack11l1l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤే")
        if (not bstack11lll11111_opy_):
          scenario_name = args[0].name
          feature_name = bstack1llll1l11l_opy_ = str(runner.feature.name)
          bstack1llll1l11l_opy_ = feature_name + bstack11l1l11_opy_ (u"ࠨࠢ࠰ࠤࠬై") + scenario_name
          if runner.driver_initialised == bstack11l1l11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦ౉"):
            bstack11lll1ll1l_opy_(context, bstack1llll1l11l_opy_)
            bstack1l1ll1ll1_opy_.execute_script(bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨొ") + json.dumps(bstack1llll1l11l_opy_) + bstack11l1l11_opy_ (u"ࠫࢂࢃࠧో"))
    except Exception as e:
      logger.debug(bstack11l1l11_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤ࡮ࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡥࡨࡲࡦࡸࡩࡰ࠼ࠣࡿࢂ࠭ౌ").format(str(e)))
@measure(event_name=EVENTS.bstack11l1l11l1l_opy_, stage=STAGE.bstack1l11l1l11l_opy_, hook_type=bstack11l1l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪ࡙ࡴࡦࡲ్ࠥ"), bstack1l111l11l_opy_=bstack1ll1ll11l1_opy_)
def bstack1ll1llllll_opy_(runner, name, context, bstack11111lll_opy_, *args):
    bstack11llll11_opy_(runner, name, context, args[0], bstack11111lll_opy_, *args)
    try:
      bstack1l1ll1ll1_opy_ = threading.current_thread().bstackSessionDriver if bstack11l1l111l_opy_(bstack11l1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭౎")) else context.browser
      if is_driver_active(bstack1l1ll1ll1_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack11l1l11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨ౏")
        bstack1llllll1l1_opy_.bstack1lll11111l_opy_(args[0])
        if runner.driver_initialised == bstack11l1l11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢ౐"):
          feature_name = bstack1llll1l11l_opy_ = str(runner.feature.name)
          bstack1llll1l11l_opy_ = feature_name + bstack11l1l11_opy_ (u"ࠪࠤ࠲ࠦࠧ౑") + context.scenario.name
          bstack1l1ll1ll1_opy_.execute_script(bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩ౒") + json.dumps(bstack1llll1l11l_opy_) + bstack11l1l11_opy_ (u"ࠬࢃࡽࠨ౓"))
    except Exception as e:
      logger.debug(bstack11l1l11_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡷࡩࡵࡀࠠࡼࡿࠪ౔").format(str(e)))
@measure(event_name=EVENTS.bstack11l1l11l1l_opy_, stage=STAGE.bstack1l11l1l11l_opy_, hook_type=bstack11l1l11_opy_ (u"ࠢࡢࡨࡷࡩࡷ࡙ࡴࡦࡲౕࠥ"), bstack1l111l11l_opy_=bstack1ll1ll11l1_opy_)
def bstack111lll1ll_opy_(runner, name, context, bstack11111lll_opy_, *args):
  bstack1llllll1l1_opy_.bstack11l1ll1l1l_opy_(args[0])
  try:
    step_status = args[0].status.name
    bstack1l1ll1ll1_opy_ = threading.current_thread().bstackSessionDriver if bstack11l1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸౖࠧ") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack1l1ll1ll1_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack11l1l11_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩ౗")
        feature_name = bstack1llll1l11l_opy_ = str(runner.feature.name)
        bstack1llll1l11l_opy_ = feature_name + bstack11l1l11_opy_ (u"ࠪࠤ࠲ࠦࠧౘ") + context.scenario.name
        bstack1l1ll1ll1_opy_.execute_script(bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩౙ") + json.dumps(bstack1llll1l11l_opy_) + bstack11l1l11_opy_ (u"ࠬࢃࡽࠨౚ"))
    if str(step_status).lower() in [bstack11l1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭౛"), bstack11l1l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭౜")]:
      bstack1lll1111l_opy_ = bstack11l1l11_opy_ (u"ࠨࠩౝ")
      bstack1l11111l_opy_ = bstack11l1l11_opy_ (u"ࠩࠪ౞")
      bstack11l1l1l1l_opy_ = bstack11l1l11_opy_ (u"ࠪࠫ౟")
      try:
        import traceback
        bstack1lll1111l_opy_ = runner.exception.__class__.__name__
        bstack1lll1ll11l_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1l11111l_opy_ = bstack11l1l11_opy_ (u"ࠫࠥ࠭ౠ").join(bstack1lll1ll11l_opy_)
        bstack11l1l1l1l_opy_ = bstack1lll1ll11l_opy_[-1]
      except Exception as e:
        logger.debug(bstack1ll1l11lll_opy_.format(str(e)))
      bstack1lll1111l_opy_ += bstack11l1l1l1l_opy_
      bstack1lll1l1l1l_opy_(context, json.dumps(str(args[0].name) + bstack11l1l11_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦౡ") + str(bstack1l11111l_opy_)),
                          bstack11l1l11_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧౢ"))
      if runner.driver_initialised == bstack11l1l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧౣ"):
        bstack1l111l11l1_opy_(getattr(context, bstack11l1l11_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭౤"), None), bstack11l1l11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ౥"), bstack1lll1111l_opy_)
        bstack1l1ll1ll1_opy_.execute_script(bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨ౦") + json.dumps(str(args[0].name) + bstack11l1l11_opy_ (u"ࠦࠥ࠳ࠠࡇࡣ࡬ࡰࡪࡪࠡ࡝ࡰࠥ౧") + str(bstack1l11111l_opy_)) + bstack11l1l11_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥࡩࡷࡸ࡯ࡳࠤࢀࢁࠬ౨"))
      if runner.driver_initialised == bstack11l1l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦ౩"):
        bstack11lll1l11l_opy_(bstack1l1ll1ll1_opy_, bstack11l1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ౪"), bstack11l1l11_opy_ (u"ࠣࡕࡦࡩࡳࡧࡲࡪࡱࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧ౫") + str(bstack1lll1111l_opy_))
    else:
      bstack1lll1l1l1l_opy_(context, bstack11l1l11_opy_ (u"ࠤࡓࡥࡸࡹࡥࡥࠣࠥ౬"), bstack11l1l11_opy_ (u"ࠥ࡭ࡳ࡬࡯ࠣ౭"))
      if runner.driver_initialised == bstack11l1l11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤ౮"):
        bstack1l111l11l1_opy_(getattr(context, bstack11l1l11_opy_ (u"ࠬࡶࡡࡨࡧࠪ౯"), None), bstack11l1l11_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ౰"))
      bstack1l1ll1ll1_opy_.execute_script(bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ౱") + json.dumps(str(args[0].name) + bstack11l1l11_opy_ (u"ࠣࠢ࠰ࠤࡕࡧࡳࡴࡧࡧࠥࠧ౲")) + bstack11l1l11_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧࢃࡽࠨ౳"))
      if runner.driver_initialised == bstack11l1l11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣ౴"):
        bstack11lll1l11l_opy_(bstack1l1ll1ll1_opy_, bstack11l1l11_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ౵"))
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡶࡸࡪࡶ࠺ࠡࡽࢀࠫ౶").format(str(e)))
  bstack11llll11_opy_(runner, name, context, args[0], bstack11111lll_opy_, *args)
@measure(event_name=EVENTS.bstack111lll11l_opy_, stage=STAGE.bstack1l11l1l11l_opy_, bstack1l111l11l_opy_=bstack1ll1ll11l1_opy_)
def bstack1111lll11_opy_(runner, name, context, bstack11111lll_opy_, *args):
  bstack1llllll1l1_opy_.end_test(args[0])
  try:
    bstack11ll111lll_opy_ = args[0].status.name
    bstack1l1ll1ll1_opy_ = bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ౷"), context.browser)
    bstack1l11l1ll1l_opy_.bstack1l111l11ll_opy_(bstack1l1ll1ll1_opy_)
    if str(bstack11ll111lll_opy_).lower() in [bstack11l1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ౸"), bstack11l1l11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ౹")]:
      bstack1lll1111l_opy_ = bstack11l1l11_opy_ (u"ࠩࠪ౺")
      bstack1l11111l_opy_ = bstack11l1l11_opy_ (u"ࠪࠫ౻")
      bstack11l1l1l1l_opy_ = bstack11l1l11_opy_ (u"ࠫࠬ౼")
      try:
        import traceback
        bstack1lll1111l_opy_ = runner.exception.__class__.__name__
        bstack1lll1ll11l_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1l11111l_opy_ = bstack11l1l11_opy_ (u"ࠬࠦࠧ౽").join(bstack1lll1ll11l_opy_)
        bstack11l1l1l1l_opy_ = bstack1lll1ll11l_opy_[-1]
      except Exception as e:
        logger.debug(bstack1ll1l11lll_opy_.format(str(e)))
      bstack1lll1111l_opy_ += bstack11l1l1l1l_opy_
      bstack1lll1l1l1l_opy_(context, json.dumps(str(args[0].name) + bstack11l1l11_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧ౾") + str(bstack1l11111l_opy_)),
                          bstack11l1l11_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨ౿"))
      if runner.driver_initialised == bstack11l1l11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥಀ") or runner.driver_initialised == bstack11l1l11_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩಁ"):
        bstack1l111l11l1_opy_(getattr(context, bstack11l1l11_opy_ (u"ࠪࡴࡦ࡭ࡥࠨಂ"), None), bstack11l1l11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦಃ"), bstack1lll1111l_opy_)
        bstack1l1ll1ll1_opy_.execute_script(bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ಄") + json.dumps(str(args[0].name) + bstack11l1l11_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧಅ") + str(bstack1l11111l_opy_)) + bstack11l1l11_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦࢂࢃࠧಆ"))
      if runner.driver_initialised == bstack11l1l11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥಇ") or runner.driver_initialised == bstack11l1l11_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩಈ"):
        bstack11lll1l11l_opy_(bstack1l1ll1ll1_opy_, bstack11l1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪಉ"), bstack11l1l11_opy_ (u"ࠦࡘࡩࡥ࡯ࡣࡵ࡭ࡴࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࡢ࡮ࠣಊ") + str(bstack1lll1111l_opy_))
    else:
      bstack1lll1l1l1l_opy_(context, bstack11l1l11_opy_ (u"ࠧࡖࡡࡴࡵࡨࡨࠦࠨಋ"), bstack11l1l11_opy_ (u"ࠨࡩ࡯ࡨࡲࠦಌ"))
      if runner.driver_initialised == bstack11l1l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤ಍") or runner.driver_initialised == bstack11l1l11_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨಎ"):
        bstack1l111l11l1_opy_(getattr(context, bstack11l1l11_opy_ (u"ࠩࡳࡥ࡬࡫ࠧಏ"), None), bstack11l1l11_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥಐ"))
      bstack1l1ll1ll1_opy_.execute_script(bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ಑") + json.dumps(str(args[0].name) + bstack11l1l11_opy_ (u"ࠧࠦ࠭ࠡࡒࡤࡷࡸ࡫ࡤࠢࠤಒ")) + bstack11l1l11_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤࢀࢁࠬಓ"))
      if runner.driver_initialised == bstack11l1l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤಔ") or runner.driver_initialised == bstack11l1l11_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨಕ"):
        bstack11lll1l11l_opy_(bstack1l1ll1ll1_opy_, bstack11l1l11_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤಖ"))
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡯࡮ࠡࡣࡩࡸࡪࡸࠠࡧࡧࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬಗ").format(str(e)))
  bstack11llll11_opy_(runner, name, context, context.scenario, bstack11111lll_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack1l11ll1l_opy_(runner, name, context, bstack11111lll_opy_, *args):
    target = context.scenario if hasattr(context, bstack11l1l11_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ಘ")) else context.feature
    bstack11llll11_opy_(runner, name, context, target, bstack11111lll_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack1llllllll_opy_(runner, name, context, bstack11111lll_opy_, *args):
    try:
      bstack1l1ll1ll1_opy_ = bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫಙ"), context.browser)
      bstack1l11l1l11_opy_ = bstack11l1l11_opy_ (u"࠭ࠧಚ")
      if context.failed is True:
        bstack1ll1llll1_opy_ = []
        bstack11llll11l_opy_ = []
        bstack111ll1ll_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack1ll1llll1_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1lll1ll11l_opy_ = traceback.format_tb(exc_tb)
            bstack1l1ll1l1l_opy_ = bstack11l1l11_opy_ (u"ࠧࠡࠩಛ").join(bstack1lll1ll11l_opy_)
            bstack11llll11l_opy_.append(bstack1l1ll1l1l_opy_)
            bstack111ll1ll_opy_.append(bstack1lll1ll11l_opy_[-1])
        except Exception as e:
          logger.debug(bstack1ll1l11lll_opy_.format(str(e)))
        bstack1lll1111l_opy_ = bstack11l1l11_opy_ (u"ࠨࠩಜ")
        for i in range(len(bstack1ll1llll1_opy_)):
          bstack1lll1111l_opy_ += bstack1ll1llll1_opy_[i] + bstack111ll1ll_opy_[i] + bstack11l1l11_opy_ (u"ࠩ࡟ࡲࠬಝ")
        bstack1l11l1l11_opy_ = bstack11l1l11_opy_ (u"ࠪࠤࠬಞ").join(bstack11llll11l_opy_)
        if runner.driver_initialised in [bstack11l1l11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠧಟ"), bstack11l1l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤಠ")]:
          bstack1lll1l1l1l_opy_(context, bstack1l11l1l11_opy_, bstack11l1l11_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧಡ"))
          bstack1l111l11l1_opy_(getattr(context, bstack11l1l11_opy_ (u"ࠧࡱࡣࡪࡩࠬಢ"), None), bstack11l1l11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣಣ"), bstack1lll1111l_opy_)
          bstack1l1ll1ll1_opy_.execute_script(bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧತ") + json.dumps(bstack1l11l1l11_opy_) + bstack11l1l11_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪಥ"))
          bstack11lll1l11l_opy_(bstack1l1ll1ll1_opy_, bstack11l1l11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦದ"), bstack11l1l11_opy_ (u"࡙ࠧ࡯࡮ࡧࠣࡷࡨ࡫࡮ࡢࡴ࡬ࡳࡸࠦࡦࡢ࡫࡯ࡩࡩࡀࠠ࡝ࡰࠥಧ") + str(bstack1lll1111l_opy_))
          bstack1l1l1l1l1l_opy_ = bstack111l11111_opy_(bstack1l11l1l11_opy_, runner.feature.name, logger)
          if (bstack1l1l1l1l1l_opy_ != None):
            bstack1l1l1l1ll_opy_.append(bstack1l1l1l1l1l_opy_)
      else:
        if runner.driver_initialised in [bstack11l1l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠢನ"), bstack11l1l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦ಩")]:
          bstack1lll1l1l1l_opy_(context, bstack11l1l11_opy_ (u"ࠣࡈࡨࡥࡹࡻࡲࡦ࠼ࠣࠦಪ") + str(runner.feature.name) + bstack11l1l11_opy_ (u"ࠤࠣࡴࡦࡹࡳࡦࡦࠤࠦಫ"), bstack11l1l11_opy_ (u"ࠥ࡭ࡳ࡬࡯ࠣಬ"))
          bstack1l111l11l1_opy_(getattr(context, bstack11l1l11_opy_ (u"ࠫࡵࡧࡧࡦࠩಭ"), None), bstack11l1l11_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧಮ"))
          bstack1l1ll1ll1_opy_.execute_script(bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫಯ") + json.dumps(bstack11l1l11_opy_ (u"ࠢࡇࡧࡤࡸࡺࡸࡥ࠻ࠢࠥರ") + str(runner.feature.name) + bstack11l1l11_opy_ (u"ࠣࠢࡳࡥࡸࡹࡥࡥࠣࠥಱ")) + bstack11l1l11_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧࢃࡽࠨಲ"))
          bstack11lll1l11l_opy_(bstack1l1ll1ll1_opy_, bstack11l1l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪಳ"))
          bstack1l1l1l1l1l_opy_ = bstack111l11111_opy_(bstack1l11l1l11_opy_, runner.feature.name, logger)
          if (bstack1l1l1l1l1l_opy_ != None):
            bstack1l1l1l1ll_opy_.append(bstack1l1l1l1l1l_opy_)
    except Exception as e:
      logger.debug(bstack11l1l11_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭಴").format(str(e)))
    bstack11llll11_opy_(runner, name, context, context.feature, bstack11111lll_opy_, *args)
@measure(event_name=EVENTS.bstack11l1l11l1l_opy_, stage=STAGE.bstack1l11l1l11l_opy_, hook_type=bstack11l1l11_opy_ (u"ࠧࡧࡦࡵࡧࡵࡅࡱࡲࠢವ"), bstack1l111l11l_opy_=bstack1ll1ll11l1_opy_)
def bstack1111ll1ll_opy_(runner, name, context, bstack11111lll_opy_, *args):
    bstack11llll11_opy_(runner, name, context, runner, bstack11111lll_opy_, *args)
def bstack1ll1lllll_opy_(self, filename=None):
  bstack11l1l11_opy_ (u"ࠨࠢࠣࠌࠣࠤࡑࡵࡡࡥࠢ࡫ࡳࡴࡱࡳࠡࡣࡱࡨࠥ࡫࡮ࡴࡷࡵࡩࠥࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵ࠯ࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠡࡣࡵࡩࠥࡸࡥࡨ࡫ࡶࡸࡪࡸࡥࡥ࠰ࠍࠤࠥࡈࡥࡩࡣࡹࡩࠥࡼ࠱࠯࠵࠮ࠤࡩࡵࡥࡴࡰࠪࡸࠥࡩࡡ࡭࡮ࠣࡶࡺࡴࠠࡩࡱࡲ࡯ࡸࠦࡴࡩࡣࡷࠤࡦࡸࡥ࡯ࠩࡷࠤࡩ࡫ࡦࡪࡰࡨࡨ࠱ࠦࡳࡰࠢࡺࡩࠥࡳࡵࡴࡶࠍࠤࠥࡪ࡯ࠡࡶ࡫࡭ࡸࠦࡥࡹࡲ࡯࡭ࡨ࡯ࡴ࡭ࡻࠣࡸࡴࠦ࡭ࡢ࡭ࡨࠤࡸࡻࡲࡦࠢࡺࡩࠬࡸࡥࠡࡥࡤࡰࡱ࡫ࡤࠡ࡫ࡱࠤࡦࡴࡹࠡࡥࡤࡷࡪ࠴ࠊࠡࠢࠥࠦࠧಶ")
  global bstack11lll11ll_opy_
  bstack11lll11ll_opy_(self, filename)
  bstack1lllll1lll_opy_ = []
  bstack1l11l1lll1_opy_ = [bstack11l1l11_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠨಷ"), bstack11l1l11_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡶࡤ࡫ࠬಸ"), bstack11l1l11_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫಹ"), bstack11l1l11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ಺"), bstack11l1l11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡸࡦ࡭ࠧ಻"), bstack11l1l11_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩ಼ࠬ")]
  bstack11llll1lll_opy_ = lambda *_: None
  for hook_name in bstack1l11l1lll1_opy_:
    if hook_name not in self.hooks:
      self.hooks[hook_name] = bstack11llll1lll_opy_
      bstack1lllll1lll_opy_.append(hook_name)
  if bstack1lllll1lll_opy_:
    os.environ[bstack11l1l11_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡓࡅࡍࡢࡈࡊࡌࡁࡖࡎࡗࡣࡍࡕࡏࡌࡕࠪಽ")] = bstack11l1l11_opy_ (u"ࠧ࠭ࠩಾ").join(bstack1lllll1lll_opy_)
def bstack11111l1ll_opy_(self, name, *args):
  global bstack11111lll_opy_
  global bstack1ll1lll1ll_opy_
  try:
    if bstack1l1111111_opy_:
      platform_index = int(threading.current_thread()._name) % bstack11ll111l1_opy_
      bstack1l111lllll_opy_ = CONFIG[bstack11l1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫಿ")][platform_index]
      os.environ[bstack11l1l11_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪೀ")] = json.dumps(bstack1l111lllll_opy_)
    if not hasattr(self, bstack11l1l11_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡸ࡫ࡤࠨು")):
      self.driver_initialised = None
    bstack11l1l11ll_opy_ = {
        bstack11l1l11_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠨೂ"): bstack1l1llll11_opy_,
        bstack11l1l11_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ೃ"): bstack11l111l1l1_opy_,
        bstack11l1l11_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡴࡢࡩࠪೄ"): bstack1l1l1111_opy_,
        bstack11l1l11_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩ೅"): bstack11lll11l1l_opy_,
        bstack11l1l11_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵ࠭ೆ"): bstack1ll1llllll_opy_,
        bstack11l1l11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡷࡩࡵ࠭ೇ"): bstack111lll1ll_opy_,
        bstack11l1l11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫೈ"): bstack1111lll11_opy_,
        bstack11l1l11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡸࡦ࡭ࠧ೉"): bstack1l11ll1l_opy_,
        bstack11l1l11_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬೊ"): bstack1llllllll_opy_,
        bstack11l1l11_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠩೋ"): bstack1111ll1ll_opy_
    }
    handler = bstack11l1l11ll_opy_.get(name, bstack11111lll_opy_)
    try:
      if args:
        context = args[0]
        remaining_args = args[1:]
        if bstack1ll1lll1ll_opy_ is None or not bstack1ll1lll1ll_opy_:
          context = self.context
          remaining_args = args
      else:
        context = self.context
        remaining_args = ()
      handler(self, name, context, bstack11111lll_opy_, *remaining_args)
    except Exception as e:
      logger.debug(bstack11l1l11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡥࡩ࡭ࡧࡶࡦࠢ࡫ࡳࡴࡱࠠࡩࡣࡱࡨࡱ࡫ࡲࠡࡽࢀ࠾ࠥࢁࡽࠨೌ").format(name, str(e)))
    if name in [bstack11l1l11_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨ್"), bstack11l1l11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ೎"), bstack11l1l11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ࠭೏")]:
      try:
        bstack1l1ll1ll1_opy_ = threading.current_thread().bstackSessionDriver if bstack11l1l111l_opy_(bstack11l1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ೐")) else context.browser
        bstack1l1lll1l1l_opy_ = (
          (name == bstack11l1l11_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠨ೑") and self.driver_initialised == bstack11l1l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥ೒")) or
          (name == bstack11l1l11_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡦࡦࡣࡷࡹࡷ࡫ࠧ೓") and self.driver_initialised == bstack11l1l11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠤ೔")) or
          (name == bstack11l1l11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪೕ") and self.driver_initialised in [bstack11l1l11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧೖ"), bstack11l1l11_opy_ (u"ࠦ࡮ࡴࡳࡵࡧࡳࠦ೗")]) or
          (name == bstack11l1l11_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡺࡥࡱࠩ೘") and self.driver_initialised == bstack11l1l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦ೙"))
        )
        if bstack1l1lll1l1l_opy_:
          self.driver_initialised = None
          if bstack1l1ll1ll1_opy_ and hasattr(bstack1l1ll1ll1_opy_, bstack11l1l11_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠫ೚")):
            try:
              bstack1l1ll1ll1_opy_.quit()
            except Exception as e:
              logger.debug(bstack11l1l11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡲࡷ࡬ࡸࡹ࡯࡮ࡨࠢࡧࡶ࡮ࡼࡥࡳࠢ࡬ࡲࠥࡨࡥࡩࡣࡹࡩࠥ࡮࡯ࡰ࡭࠽ࠤࢀࢃࠧ೛").format(str(e)))
      except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࠣ࡬ࡴࡵ࡫ࠡࡥ࡯ࡩࡦࡴࡵࡱࠢࡩࡳࡷࠦࡻࡾ࠼ࠣࡿࢂ࠭೜").format(name, str(e)))
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"ࠪࡇࡷ࡯ࡴࡪࡥࡤࡰࠥ࡫ࡲࡳࡱࡵࠤ࡮ࡴࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡳࡷࡱࠤ࡭ࡵ࡯࡬ࠢࡾࢁ࠿ࠦࡻࡾࠩೝ").format(name, str(e)))
    try:
      if bstack1ll1lll1ll_opy_ is None or bstack1ll1lll1ll_opy_:
        try:
          bstack11111lll_opy_(self, name, self.context, *args)
        except TypeError:
          bstack11111lll_opy_(self, name, *args)
      else:
        bstack11111lll_opy_(self, name, *args)
    except Exception as e2:
      logger.debug(bstack11l1l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࠣࡦࡪ࡮ࡡࡷࡧࠣ࡬ࡴࡵ࡫ࠡࡽࢀ࠾ࠥࢁࡽࠨೞ").format(name, str(e2)))
def bstack11llll11ll_opy_(config, startdir):
  return bstack11l1l11_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶ࠿ࠦࡻ࠱ࡿࠥ೟").format(bstack11l1l11_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧೠ"))
notset = Notset()
def bstack1l1l111l1_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1l11l1ll1_opy_
  if str(name).lower() == bstack11l1l11_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸࠧೡ"):
    return bstack11l1l11_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢೢ")
  else:
    return bstack1l11l1ll1_opy_(self, name, default, skip)
def bstack111llll1l1_opy_(item, when):
  global bstack11l11llll1_opy_
  try:
    bstack11l11llll1_opy_(item, when)
  except Exception as e:
    pass
def bstack1l11111ll1_opy_():
  return
def browserstack_executor_helper(type, name, status, reason, bstack1ll1llll_opy_, bstack1lll11l1_opy_):
  bstack1l1lll1l1_opy_ = {
    bstack11l1l11_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩೣ"): type,
    bstack11l1l11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭೤"): {}
  }
  if type == bstack11l1l11_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭೥"):
    bstack1l1lll1l1_opy_[bstack11l1l11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ೦")][bstack11l1l11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ೧")] = bstack1ll1llll_opy_
    bstack1l1lll1l1_opy_[bstack11l1l11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ೨")][bstack11l1l11_opy_ (u"ࠨࡦࡤࡸࡦ࠭೩")] = json.dumps(str(bstack1lll11l1_opy_))
  if type == bstack11l1l11_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ೪"):
    bstack1l1lll1l1_opy_[bstack11l1l11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭೫")][bstack11l1l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ೬")] = name
  if type == bstack11l1l11_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ೭"):
    bstack1l1lll1l1_opy_[bstack11l1l11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ೮")][bstack11l1l11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ೯")] = status
    if status == bstack11l1l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ೰"):
      bstack1l1lll1l1_opy_[bstack11l1l11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬೱ")][bstack11l1l11_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪೲ")] = json.dumps(str(reason))
  bstack11l11lll1_opy_ = bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩೳ").format(json.dumps(bstack1l1lll1l1_opy_))
  return bstack11l11lll1_opy_
def bstack111l1l1l1_opy_(driver_command, response):
    if driver_command == bstack11l1l11_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠩ೴"):
        TestHubHandler.bstack11l1lllll_opy_({
            bstack11l1l11_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬ೵"): response[bstack11l1l11_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭೶")],
            bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ೷"): TestHubHandler.current_test_uuid()
        })
def bstack111ll1ll1l_opy_(item, call, rep):
  global bstack1lll1lll1l_opy_
  global bstack1ll1111ll1_opy_
  global bstack11lll11111_opy_
  name = bstack11l1l11_opy_ (u"ࠩࠪ೸")
  try:
    if rep.when == bstack11l1l11_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ೹"):
      bstack1ll1l1111l_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack11lll11111_opy_:
          name = str(rep.nodeid)
          executor_string = browserstack_executor_helper(bstack11l1l11_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ೺"), name, bstack11l1l11_opy_ (u"ࠬ࠭೻"), bstack11l1l11_opy_ (u"࠭ࠧ೼"), bstack11l1l11_opy_ (u"ࠧࠨ೽"), bstack11l1l11_opy_ (u"ࠨࠩ೾"))
          threading.current_thread().bstack11ll1ll11l_opy_ = name
          for driver in bstack1ll1111ll1_opy_:
            if bstack1ll1l1111l_opy_ == driver.session_id:
              driver.execute_script(executor_string)
      except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩ೿").format(str(e)))
      try:
        bstack1ll1l1l1l_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack11l1l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫഀ"):
          status = bstack11l1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫഁ") if rep.outcome.lower() == bstack11l1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬം") else bstack11l1l11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ഃ")
          reason = bstack11l1l11_opy_ (u"ࠧࠨഄ")
          if status == bstack11l1l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨഅ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack11l1l11_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧആ") if status == bstack11l1l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪഇ") else bstack11l1l11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪഈ")
          data = name + bstack11l1l11_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧഉ") if status == bstack11l1l11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ഊ") else name + bstack11l1l11_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠢࠢࠪഋ") + reason
          bstack11l11lllll_opy_ = browserstack_executor_helper(bstack11l1l11_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪഌ"), bstack11l1l11_opy_ (u"ࠩࠪ഍"), bstack11l1l11_opy_ (u"ࠪࠫഎ"), bstack11l1l11_opy_ (u"ࠫࠬഏ"), level, data)
          for driver in bstack1ll1111ll1_opy_:
            if bstack1ll1l1111l_opy_ == driver.session_id:
              driver.execute_script(bstack11l11lllll_opy_)
      except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡦࡳࡳࡺࡥࡹࡶࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩഐ").format(str(e)))
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡶࡸࡦࡺࡥࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼࡿࠪ഑").format(str(e)))
  bstack1lll1lll1l_opy_(item, call, rep)
def bstack111ll1l1l1_opy_(driver, bstack1ll11lll1_opy_, test=None):
  global bstack11ll1l111_opy_
  if test != None:
    bstack1ll1l1ll1l_opy_ = getattr(test, bstack11l1l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬഒ"), None)
    bstack111l1l1ll1_opy_ = getattr(test, bstack11l1l11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ഓ"), None)
    PercySDK.screenshot(driver, bstack1ll11lll1_opy_, bstack1ll1l1ll1l_opy_=bstack1ll1l1ll1l_opy_, bstack111l1l1ll1_opy_=bstack111l1l1ll1_opy_, bstack111l1111l1_opy_=bstack11ll1l111_opy_)
  else:
    PercySDK.screenshot(driver, bstack1ll11lll1_opy_)
@measure(event_name=EVENTS.bstack111lll1111_opy_, stage=STAGE.bstack1l11l1l11l_opy_, bstack1l111l11l_opy_=bstack1ll1ll11l1_opy_)
def bstack11lll11l_opy_(driver):
  if bstack1l11l1l1l_opy_.bstack11ll1ll1l1_opy_() is True or bstack1l11l1l1l_opy_.capturing() is True:
    return
  bstack1l11l1l1l_opy_.bstack111ll111l1_opy_()
  while not bstack1l11l1l1l_opy_.bstack11ll1ll1l1_opy_():
    bstack1ll1ll11_opy_ = bstack1l11l1l1l_opy_.bstack1l1l1lll1l_opy_()
    bstack111ll1l1l1_opy_(driver, bstack1ll1ll11_opy_)
  bstack1l11l1l1l_opy_.bstack1111l1111_opy_()
def bstack1ll11l11_opy_(sequence, driver_command, response = None, bstack111ll1l1_opy_ = None, args = None):
    try:
      if sequence != bstack11l1l11_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩഔ"):
        return
      if percy.bstack1l1111ll11_opy_() == bstack11l1l11_opy_ (u"ࠥࡪࡦࡲࡳࡦࠤക"):
        return
      bstack1ll1ll11_opy_ = bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧഖ"), None)
      for command in bstack1ll1111111_opy_:
        if command == driver_command:
          with bstack1lllllll11_opy_:
            bstack1lll1l11_opy_ = bstack1ll1111ll1_opy_.copy()
          for driver in bstack1lll1l11_opy_:
            bstack11lll11l_opy_(driver)
      bstack1111111ll_opy_ = percy.bstack11l1ll111l_opy_()
      if driver_command in bstack1l1l1l11ll_opy_[bstack1111111ll_opy_]:
        bstack1l11l1l1l_opy_.bstack1l111lll11_opy_(bstack1ll1ll11_opy_, driver_command)
    except Exception as e:
      pass
def bstack11ll11l111_opy_(framework_name):
  if global_config.get_property(bstack11l1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩഗ")):
      return
  global_config.bstack1l111111ll_opy_(bstack11l1l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪഘ"), True)
  global bstack11ll1ll111_opy_
  global bstack1lll1ll1ll_opy_
  global bstack1lll11lll_opy_
  bstack11ll1ll111_opy_ = framework_name
  logger.info(bstack11111l1l_opy_.format(bstack11ll1ll111_opy_.split(bstack11l1l11_opy_ (u"ࠧ࠮ࠩങ"))[0]))
  bstack111l111lll_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    global bstack111ll1llll_opy_
    bstack1lll1l1l1_opy_ = bstack1l1111111_opy_ or bstack111ll1llll_opy_
    if bstack1lll1l1l1_opy_:
      Service.start = bstack1ll111l1_opy_
      Service.stop = bstack11lll1ll1_opy_
      webdriver.Remote.get = bstack1l11ll111_opy_
      WebDriver.quit = bstack11l11111l1_opy_
      webdriver.Remote.__init__ = bstack11l11l1lll_opy_
    if not bstack1l1111111_opy_ and not bstack111ll1llll_opy_:
        webdriver.Remote.__init__ = bstack11lllllll1_opy_
    WebDriver.getAccessibilityResults = getAccessibilityResults
    WebDriver.get_accessibility_results = getAccessibilityResults
    WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
    WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
    WebDriver.performScan = perform_scan
    WebDriver.perform_scan = perform_scan
    WebDriver.execute = bstack1l1l1lll11_opy_
    bstack1lll1ll1ll_opy_ = True
  except Exception as e:
    pass
  try:
    bstack1lll1l1l1_opy_ = bstack1l1111111_opy_ or bstack111ll1llll_opy_
    if bstack1lll1l1l1_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1ll11ll1l_opy_
  except Exception as e:
    pass
  bstack11llllll1l_opy_()
  if not bstack1lll1ll1ll_opy_:
    bstack1ll1llll1l_opy_(bstack11l1l11_opy_ (u"ࠣࡒࡤࡧࡰࡧࡧࡦࡵࠣࡲࡴࡺࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠥച"), bstack1111l1ll1_opy_)
  if bstack111111l11_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      if hasattr(RemoteConnection, bstack11l1l11_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪഛ")) and callable(getattr(RemoteConnection, bstack11l1l11_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫജ"))):
        RemoteConnection._get_proxy_url = bstack1l1111l111_opy_
      else:
        from selenium.webdriver.remote.client_config import ClientConfig
        ClientConfig.get_proxy_url = bstack1l1111l111_opy_
    except Exception as e:
      logger.error(bstack1l1ll1l1l1_opy_.format(str(e)))
  if bstack1ll1l1l1l1_opy_():
    bstack11lll1l111_opy_(CONFIG, logger)
  if (bstack11l1l11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪഝ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      try:
        from pabot.pabot import QueueItem
        from pabot import pabot
      except Exception as e:
        logger.warning(bstack1llllll1ll_opy_ + str(e))
      if not is_robot_playwright_installed():
        try:
          if percy.bstack1l1111ll11_opy_() == bstack11l1l11_opy_ (u"ࠧࡺࡲࡶࡧࠥഞ"):
            bstack1l111111l_opy_(bstack1ll11l11_opy_)
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
          WebDriverCreator._get_ff_profile = bstack111lll1l1_opy_
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
          WebDriverCache.close = bstack1l1l11l11_opy_
        except Exception as e:
          logger.warning(bstack1ll1l11l_opy_ + str(e))
        try:
          from AppiumLibrary.utils.applicationcache import ApplicationCache
          ApplicationCache.close = bstack1l1ll1llll_opy_
        except Exception as e:
          logger.debug(bstack1l111lll1_opy_ + str(e))
    except Exception as e:
      bstack1ll1llll1l_opy_(e, bstack1ll1l11l_opy_)
    Output.start_test = bstack1ll11llll1_opy_
    Output.end_test = bstack1l1lll11l1_opy_
    TestStatus.__init__ = bstack11lll1111l_opy_
    QueueItem.__init__ = bstack1l11l1l1l1_opy_
    pabot._create_items = bstack11lll111l_opy_
    try:
      from pabot import __version__ as bstack1l1ll1ll11_opy_
      if version.parse(bstack1l1ll1ll11_opy_) >= version.parse(bstack11l1l11_opy_ (u"࠭࠵࠯࠲࠱࠴ࠬട")):
        pabot._run = bstack1lll1l1ll_opy_
      elif version.parse(bstack1l1ll1ll11_opy_) >= version.parse(bstack11l1l11_opy_ (u"ࠧ࠵࠰࠵࠲࠵࠭ഠ")):
        pabot._run = bstack1l1l11llll_opy_
      elif version.parse(bstack1l1ll1ll11_opy_) >= version.parse(bstack11l1l11_opy_ (u"ࠨ࠴࠱࠵࠺࠴࠰ࠨഡ")):
        pabot._run = bstack11ll1l1ll_opy_
      elif version.parse(bstack1l1ll1ll11_opy_) >= version.parse(bstack11l1l11_opy_ (u"ࠩ࠵࠲࠶࠹࠮࠱ࠩഢ")):
        pabot._run = bstack1l1lll1l_opy_
      else:
        pabot._run = bstack1ll111ll1_opy_
    except Exception as e:
      pabot._run = bstack1ll111ll1_opy_
    pabot._create_command_for_execution = bstack1l11ll1l1l_opy_
    pabot._report_results = bstack11lllll111_opy_
  if bstack11l1l11_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪണ") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll1llll1l_opy_(e, bstack11l1l1l111_opy_)
    Runner.run_hook = bstack11111l1ll_opy_
    try:
      from behave import __version__ as bstack1111ll1l_opy_
      if version.parse(bstack1111ll1l_opy_) >= version.parse(bstack11l1l11_opy_ (u"ࠫ࠶࠴࠳࠯࠲ࠪത")):
        Runner.load_hooks = bstack1ll1lllll_opy_
    except Exception as e:
      logger.debug(bstack11l1l11_opy_ (u"ࠬࡉ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤࡧ࡫ࡨࡢࡸࡨࠤࡻ࡫ࡲࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩഥ").format(str(e)))
    Step.run = bstack11l111l11_opy_
  if bstack11l1l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ദ") in str(framework_name).lower():
    if not bstack1l1111111_opy_:
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack11llll11ll_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1l11111ll1_opy_
      Config.getoption = bstack1l1l111l1_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack111ll1ll1l_opy_
    except Exception as e:
      pass
def bstack11ll1lll1_opy_():
  global CONFIG
  if bstack11l1l11_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧധ") in CONFIG and int(CONFIG[bstack11l1l11_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨന")]) > 1:
    logger.warning(bstack1l11111l1_opy_)
def bstack1l1lllll11_opy_(arg, bstack1lllll1l11_opy_, bstack1ll1ll1l1_opy_=None):
  global CONFIG
  global bstack1l1l11ll11_opy_
  global bstack1l11ll1ll1_opy_
  global bstack1l1111111_opy_
  global bstack111ll1llll_opy_
  global global_config
  bstack1l111ll11l_opy_ = bstack11l1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩഩ")
  if bstack1lllll1l11_opy_ and isinstance(bstack1lllll1l11_opy_, str):
    bstack1lllll1l11_opy_ = eval(bstack1lllll1l11_opy_)
  CONFIG = bstack1lllll1l11_opy_[bstack11l1l11_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪപ")]
  bstack1l1l11ll11_opy_ = bstack1lllll1l11_opy_[bstack11l1l11_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬഫ")]
  bstack1l11ll1ll1_opy_ = bstack1lllll1l11_opy_[bstack11l1l11_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧബ")]
  bstack1l1111111_opy_ = bstack1lllll1l11_opy_[bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩഭ")]
  try:
    bstack1l1lll1ll1_opy_ = bstack1lllll1l11_opy_.get(bstack11l1l11_opy_ (u"ࠧࡐࡘࡈࡖࡗࡏࡄࡆࡡࡏࡓࡆࡊ࡟ࡕࡇࡖࡘࡎࡔࡇࠨമ"), False)
    bstack111ll1llll_opy_ = bool(bstack1l1lll1ll1_opy_)
    os.environ[bstack11l1l11_opy_ (u"ࠨࡑ࡙ࡉࡗࡘࡉࡅࡇࡢࡐࡔࡇࡄࡠࡖࡈࡗ࡙ࡏࡎࡈࠩയ")] = str(bstack111ll1llll_opy_).lower()
  except Exception as e:
    logger.error(bstack11l1l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡏࡗࡇࡕࡖࡎࡊࡅࡠࡎࡒࡅࡉࡥࡔࡆࡕࡗࡍࡓࡍ࠺ࠡࡽࢀࠦര").format(e))
    bstack111ll1llll_opy_ = False
    os.environ[bstack11l1l11_opy_ (u"ࠪࡓ࡛ࡋࡒࡓࡋࡇࡉࡤࡒࡏࡂࡆࡢࡘࡊ࡙ࡔࡊࡐࡊࠫറ")] = bstack11l1l11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪല")
  global_config.bstack1l111111ll_opy_(bstack11l1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ള"), bstack1l1111111_opy_)
  os.environ[bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨഴ")] = bstack1l111ll11l_opy_
  os.environ[bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌ࠭വ")] = json.dumps(CONFIG)
  os.environ[bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡉࡗࡅࡣ࡚ࡘࡌࠨശ")] = bstack1l1l11ll11_opy_
  os.environ[bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪഷ")] = str(bstack1l11ll1ll1_opy_)
  os.environ[bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡐ࡚ࡍࡉࡏࠩസ")] = str(True)
  if bstack1l1l1llll1_opy_(arg, [bstack11l1l11_opy_ (u"ࠫ࠲ࡴࠧഹ"), bstack11l1l11_opy_ (u"ࠬ࠳࠭࡯ࡷࡰࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ഺ")]) != -1:
    os.environ[bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡁࡓࡃࡏࡐࡊࡒ഻ࠧ")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack111lll1l1l_opy_)
    return
  bstack111l1l11l1_opy_()
  global bstack1lll1l1l11_opy_
  global bstack11ll1l111_opy_
  global bstack1l1l1l1ll1_opy_
  global bstack1ll111l11l_opy_
  global bstack111ll11l11_opy_
  global bstack1lll11lll_opy_
  global bstack1l11ll11ll_opy_
  arg.append(bstack11l1l11_opy_ (u"ࠢ࠮഼࡙ࠥ"))
  arg.append(bstack11l1l11_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡥ࠻ࡏࡲࡨࡺࡲࡥࠡࡣ࡯ࡶࡪࡧࡤࡺࠢ࡬ࡱࡵࡵࡲࡵࡧࡧ࠾ࡵࡿࡴࡦࡵࡷ࠲ࡕࡿࡴࡦࡵࡷ࡛ࡦࡸ࡮ࡪࡰࡪࠦഽ"))
  arg.append(bstack11l1l11_opy_ (u"ࠤ࠰࡛ࠧാ"))
  arg.append(bstack11l1l11_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧ࠽ࡘ࡭࡫ࠠࡩࡱࡲ࡯࡮ࡳࡰ࡭ࠤി"))
  global bstack11l1ll11l1_opy_
  global bstack1l1ll111l1_opy_
  global bstack1l1l1111l_opy_
  global bstack1lll111lll_opy_
  global bstack1lll111111_opy_
  global bstack11l111lll1_opy_
  global bstack1l1l111ll1_opy_
  global bstack11l11l1l_opy_
  global bstack1lll111ll_opy_
  global bstack111l1ll11l_opy_
  global bstack1l11l1ll1_opy_
  global bstack11l11llll1_opy_
  global bstack1lll1lll1l_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11l1ll11l1_opy_ = webdriver.Remote.__init__
    bstack1l1ll111l1_opy_ = WebDriver.quit
    bstack11l11l1l_opy_ = WebDriver.close
    bstack1lll111ll_opy_ = WebDriver.get
    bstack1l1l1111l_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1l1llll1_opy_(CONFIG) and bstack1ll111l1l_opy_():
    if bstack1l1ll1111l_opy_() < version.parse(bstack1lll11ll1l_opy_):
      logger.error(bstack11lllll1_opy_.format(bstack1l1ll1111l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack11l1l11_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬീ")) and callable(getattr(RemoteConnection, bstack11l1l11_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭ു"))):
          bstack111l1ll11l_opy_ = RemoteConnection._get_proxy_url
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          bstack111l1ll11l_opy_ = ClientConfig.get_proxy_url
      except Exception as e:
        logger.error(bstack1l1ll1l1l1_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1l11l1ll1_opy_ = Config.getoption
    from _pytest import runner
    bstack11l11llll1_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warning(bstack11l1l11_opy_ (u"ࠨࠥࡴ࠼ࠣࠩࡸࠨൂ"), bstack11l11ll1ll_opy_, str(e))
  try:
    from pytest_bdd import reporting
    bstack1lll1lll1l_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨൃ"))
  if cli.is_enabled(CONFIG) and cli.config:
    bstack1l1l1l1ll1_opy_ = cli.config.get(bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬൄ"), {}).get(bstack11l1l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ൅"))
  else:
    bstack1l1l1l1ll1_opy_ = CONFIG.get(bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧെ"), {}).get(bstack11l1l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭േ"))
  bstack1l11ll11ll_opy_ = True
  if cli.is_enabled(CONFIG):
    if cli.bstack1lll11l1l_opy_():
      bstack11l1l1l11_opy_.invoke(bstack1lllllll1_opy_.CONNECT, bstack1l1111l1l_opy_())
    platform_index = int(os.environ.get(bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬൈ"), bstack11l1l11_opy_ (u"࠭࠰ࠨ൉")))
  else:
    bstack11ll11l111_opy_(bstack1ll1l111l1_opy_)
  os.environ[bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨൊ")] = CONFIG[bstack11l1l11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪോ")]
  os.environ[bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬൌ")] = CONFIG[bstack11l1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ്࠭")]
  os.environ[bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧൎ")] = bstack1l1111111_opy_.__str__()
  from _pytest.config import main as bstack1l1ll1l11_opy_
  bstack11l111ll11_opy_ = []
  try:
    exit_code = bstack1l1ll1l11_opy_(arg)
    if cli.is_enabled(CONFIG):
      cli.bstack11l1l11ll1_opy_()
    if bstack11l1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩ൏") in multiprocessing.current_process().__dict__.keys():
      for bstack1l1111ll1_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack11l111ll11_opy_.append(bstack1l1111ll1_opy_)
    try:
      bstack1111l11l1_opy_ = (bstack11l111ll11_opy_, int(exit_code))
      bstack1ll1ll1l1_opy_.append(bstack1111l11l1_opy_)
    except:
      bstack1ll1ll1l1_opy_.append((bstack11l111ll11_opy_, exit_code))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack11l111ll11_opy_.append({bstack11l1l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ൐"): bstack11l1l11_opy_ (u"ࠧࡑࡴࡲࡧࡪࡹࡳࠡࠩ൑") + os.environ.get(bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ൒")), bstack11l1l11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ൓"): traceback.format_exc(), bstack11l1l11_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩൔ"): int(os.environ.get(bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫൕ")))})
    bstack1ll1ll1l1_opy_.append((bstack11l111ll11_opy_, 1))
def mod_behave_main(args, retries):
  try:
    from behave.configuration import Configuration
    from behave.__main__ import run_behave
    from browserstack_sdk.bstack_behave_runner import BehaveRunner
    config = Configuration(args)
    config.update_userdata({bstack11l1l11_opy_ (u"ࠧࡸࡥࡵࡴ࡬ࡩࡸࠨൖ"): str(retries)})
    return run_behave(config, runner_class=BehaveRunner)
  except Exception as e:
    bstack111ll11l1l_opy_ = e.__class__.__name__
    print(bstack11l1l11_opy_ (u"ࠨࠥࡴ࠼ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡦࡪ࡮ࡡࡷࡧࠣࡸࡪࡹࡴࠡࠧࡶࠦൗ") % (bstack111ll11l1l_opy_, e))
    return 1
def bstack1l1111111l_opy_(arg):
  global bstack1lll111l1_opy_
  bstack11ll11l111_opy_(bstack11lll1l1_opy_)
  os.environ[bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ൘")] = str(bstack1l11ll1ll1_opy_)
  retries = bstack1l1l11l11l_opy_.bstack111lll1ll1_opy_(CONFIG)
  status_code = 0
  if bstack1l1l11l11l_opy_.bstack111lll1l11_opy_(CONFIG):
    status_code = mod_behave_main(arg, retries)
  else:
    from behave.__main__ import main as bstack1lll1lll1_opy_
    status_code = bstack1lll1lll1_opy_(arg)
  if status_code != 0:
    bstack1lll111l1_opy_ = status_code
def bstack11l11l111_opy_():
  logger.info(bstack1ll111ll11_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack11l1l11_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ൙"), help=bstack11l1l11_opy_ (u"ࠩࡊࡩࡳ࡫ࡲࡢࡶࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡧࡴࡴࡦࡪࡩࠪ൚"))
  parser.add_argument(bstack11l1l11_opy_ (u"ࠪ࠱ࡺ࠭൛"), bstack11l1l11_opy_ (u"ࠫ࠲࠳ࡵࡴࡧࡵࡲࡦࡳࡥࠨ൜"), help=bstack11l1l11_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫ൝"))
  parser.add_argument(bstack11l1l11_opy_ (u"࠭࠭࡬ࠩ൞"), bstack11l1l11_opy_ (u"ࠧ࠮࠯࡮ࡩࡾ࠭ൟ"), help=bstack11l1l11_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡧࡣࡤࡧࡶࡷࠥࡱࡥࡺࠩൠ"))
  parser.add_argument(bstack11l1l11_opy_ (u"ࠩ࠰ࡪࠬൡ"), bstack11l1l11_opy_ (u"ࠪ࠱࠲࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨൢ"), help=bstack11l1l11_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪൣ"))
  bstack1lll1ll111_opy_ = parser.parse_args()
  try:
    bstack111l1ll11_opy_ = bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡬࡫࡮ࡦࡴ࡬ࡧ࠳ࡿ࡭࡭࠰ࡶࡥࡲࡶ࡬ࡦࠩ൤")
    if bstack1lll1ll111_opy_.framework and bstack1lll1ll111_opy_.framework not in (bstack11l1l11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭൥"), bstack11l1l11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨ൦")):
      bstack111l1ll11_opy_ = bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࠱ࡽࡲࡲ࠮ࡴࡣࡰࡴࡱ࡫ࠧ൧")
    bstack11l111ll1_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack111l1ll11_opy_)
    bstack11llll111_opy_ = open(bstack11l111ll1_opy_, bstack11l1l11_opy_ (u"ࠩࡵࠫ൨"))
    bstack1ll11l1l_opy_ = bstack11llll111_opy_.read()
    bstack11llll111_opy_.close()
    if bstack1lll1ll111_opy_.username:
      bstack1ll11l1l_opy_ = bstack1ll11l1l_opy_.replace(bstack11l1l11_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪ൩"), bstack1lll1ll111_opy_.username)
    if bstack1lll1ll111_opy_.key:
      bstack1ll11l1l_opy_ = bstack1ll11l1l_opy_.replace(bstack11l1l11_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭൪"), bstack1lll1ll111_opy_.key)
    if bstack1lll1ll111_opy_.framework:
      bstack1ll11l1l_opy_ = bstack1ll11l1l_opy_.replace(bstack11l1l11_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭൫"), bstack1lll1ll111_opy_.framework)
    file_name = bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩ൬")
    file_path = os.path.abspath(file_name)
    bstack111l1ll1_opy_ = open(file_path, bstack11l1l11_opy_ (u"ࠧࡸࠩ൭"))
    bstack111l1ll1_opy_.write(bstack1ll11l1l_opy_)
    bstack111l1ll1_opy_.close()
    logger.info(bstack1ll11ll1ll_opy_)
    try:
      os.environ[bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪ൮")] = bstack1lll1ll111_opy_.framework if bstack1lll1ll111_opy_.framework != None else bstack11l1l11_opy_ (u"ࠤࠥ൯")
      config = yaml.safe_load(bstack1ll11l1l_opy_)
      config[bstack11l1l11_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ൰")] = bstack11l1l11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱ࡸ࡫ࡴࡶࡲࠪ൱")
      bstack11l1l11lll_opy_(bstack1l1l111l1l_opy_, config)
    except Exception as e:
      logger.debug(bstack1l11lll1l_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack111l111l_opy_.format(str(e)))
def bstack11l1l11lll_opy_(bstack1l11l11l_opy_, config, bstack11l1111111_opy_={}):
  global bstack1l1111111_opy_
  global bstack1lll1ll1l1_opy_
  global global_config
  if not config:
    return
  bstack11l111111l_opy_ = bstack111l1l1l_opy_ if not bstack1l1111111_opy_ else (
    bstack1l11llllll_opy_ if bstack11l1l11_opy_ (u"ࠬࡧࡰࡱࠩ൲") in config else (
        bstack1ll111111l_opy_ if config.get(bstack11l1l11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ൳")) else bstack1l11ll11l_opy_
    )
)
  bstack111lll11l1_opy_ = False
  bstack111111ll_opy_ = False
  if bstack1l1111111_opy_ is True:
      if bstack11l1l11_opy_ (u"ࠧࡢࡲࡳࠫ൴") in config:
          bstack111lll11l1_opy_ = True
      else:
          bstack111111ll_opy_ = True
  bstack1llll111l_opy_ = bstack1l11l1l111_opy_.bstack1l111l111_opy_(config, bstack1lll1ll1l1_opy_)
  bstack1l1l1ll11_opy_ = bstack1l11l111l1_opy_()
  data = {
    bstack11l1l11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ൵"): config[bstack11l1l11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ൶")],
    bstack11l1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭൷"): config[bstack11l1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ൸")],
    bstack11l1l11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ൹"): bstack1l11l11l_opy_,
    bstack11l1l11_opy_ (u"࠭ࡤࡦࡶࡨࡧࡹ࡫ࡤࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪൺ"): os.environ.get(bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩൻ"), bstack1lll1ll1l1_opy_),
    bstack11l1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪർ"): bstack11lll1l1l_opy_,
    bstack11l1l11_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯ࠫൽ"): bstack1l1l1l1l1_opy_(),
    bstack11l1l11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭ൾ"): {
      bstack11l1l11_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩൿ"): str(config[bstack11l1l11_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ඀")]) if bstack11l1l11_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ඁ") in config else bstack11l1l11_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣං"),
      bstack11l1l11_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧ࡙ࡩࡷࡹࡩࡰࡰࠪඃ"): sys.version,
      bstack11l1l11_opy_ (u"ࠩࡵࡩ࡫࡫ࡲࡳࡧࡵࠫ඄"): bstack11lll11l11_opy_(os.environ.get(bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬඅ"), bstack1lll1ll1l1_opy_)),
      bstack11l1l11_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭ආ"): bstack11l1l11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬඇ"),
      bstack11l1l11_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧඈ"): bstack11l111111l_opy_,
      bstack11l1l11_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬඉ"): bstack1llll111l_opy_,
      bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡡࡸࡹ࡮ࡪࠧඊ"): os.environ[bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧඋ")],
      bstack11l1l11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ඌ"): os.environ.get(bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ඍ"), bstack1lll1ll1l1_opy_),
      bstack11l1l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨඎ"): bstack1l11ll1l1_opy_(os.environ.get(bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨඏ"), bstack1lll1ll1l1_opy_)),
      bstack11l1l11_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ඐ"): bstack1l1l1ll11_opy_.get(bstack11l1l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭එ")),
      bstack11l1l11_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨඒ"): bstack1l1l1ll11_opy_.get(bstack11l1l11_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫඓ")),
      bstack11l1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧඔ"): config[bstack11l1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨඕ")] if config[bstack11l1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩඖ")] else bstack11l1l11_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣ඗"),
      bstack11l1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ඘"): str(config[bstack11l1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ඙")]) if bstack11l1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬක") in config else bstack11l1l11_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧඛ"),
      bstack11l1l11_opy_ (u"ࠬࡵࡳࠨග"): sys.platform,
      bstack11l1l11_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨඝ"): socket.gethostname(),
      bstack11l1l11_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥࠩඞ"): global_config.get_property(bstack11l1l11_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪඟ"))
    }
  }
  if not global_config.get_property(bstack11l1l11_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩච")) is None:
    data[bstack11l1l11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭ඡ")][bstack11l1l11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡓࡥࡵࡣࡧࡥࡹࡧࠧජ")] = {
      bstack11l1l11_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬඣ"): bstack11l1l11_opy_ (u"࠭ࡵࡴࡧࡵࡣࡰ࡯࡬࡭ࡧࡧࠫඤ"),
      bstack11l1l11_opy_ (u"ࠧࡴ࡫ࡪࡲࡦࡲࠧඥ"): global_config.get_property(bstack11l1l11_opy_ (u"ࠨࡵࡧ࡯ࡐ࡯࡬࡭ࡕ࡬࡫ࡳࡧ࡬ࠨඦ")),
      bstack11l1l11_opy_ (u"ࠩࡶ࡭࡬ࡴࡡ࡭ࡐࡸࡱࡧ࡫ࡲࠨට"): global_config.get_property(bstack11l1l11_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡒࡴ࠭ඨ"))
    }
  if bstack1l11l11l_opy_ == bstack1l1lll1lll_opy_:
    data[bstack11l1l11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧඩ")][bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡇࡴࡴࡦࡪࡩࠪඪ")] = bstack1l1ll1l111_opy_(config)
    data[bstack11l1l11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩණ")][bstack11l1l11_opy_ (u"ࠧࡪࡵࡓࡩࡷࡩࡹࡂࡷࡷࡳࡊࡴࡡࡣ࡮ࡨࡨࠬඬ")] = percy.bstack11l11lll1l_opy_
    data[bstack11l1l11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫත")][bstack11l1l11_opy_ (u"ࠩࡳࡩࡷࡩࡹࡃࡷ࡬ࡰࡩࡏࡤࠨථ")] = percy.percy_build_id
  if not bstack1l1l11l11l_opy_.bstack1111lll1_opy_(CONFIG):
    data[bstack11l1l11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭ද")][bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠨධ")] = bstack1l1l11l11l_opy_.bstack1111lll1_opy_(CONFIG)
  bstack1llll1l1ll_opy_ = bstack1lllll1l1l_opy_.get_instance(CONFIG, logger)
  bstack11ll11l1l_opy_ = bstack1l1l11l11l_opy_.get_instance(config=CONFIG)
  if bstack1llll1l1ll_opy_ is not None and bstack11ll11l1l_opy_ is not None and bstack11ll11l1l_opy_.bstack1l1ll111ll_opy_():
    data[bstack11l1l11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨන")][bstack11ll11l1l_opy_.bstack1ll11llll_opy_()] = bstack1llll1l1ll_opy_.bstack111llll111_opy_()
  update(data[bstack11l1l11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩ඲")], bstack11l1111111_opy_)
  try:
    response = bstack11l11llll_opy_(bstack11l1l11_opy_ (u"ࠧࡑࡑࡖࡘࠬඳ"), bstack11l11lll_opy_(bstack1l1111lll_opy_), data, {
      bstack11l1l11_opy_ (u"ࠨࡣࡸࡸ࡭࠭ප"): (config[bstack11l1l11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫඵ")], config[bstack11l1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭බ")])
    })
    if response:
      logger.debug(bstack1ll1111l1_opy_.format(bstack1l11l11l_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1l1111lll1_opy_.format(str(e)))
def bstack11lll11l11_opy_(framework):
  return bstack11l1l11_opy_ (u"ࠦࢀࢃ࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴ࢁࡽࠣභ").format(str(framework), __version__) if framework else bstack11l1l11_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࡿࢂࠨම").format(
    __version__)
def bstack111l1l11l1_opy_():
  global CONFIG
  global bstack1l11l11l1_opy_
  if bool(CONFIG):
    return
  try:
    bstack11lll1l1ll_opy_()
    logger.debug(bstack1ll11l11l_opy_.format(str(CONFIG)))
    bstack1l11l11l1_opy_ = logger_utils.configure_logger(CONFIG, bstack1l11l11l1_opy_)
    bstack111l111lll_opy_()
  except Exception as e:
    logger.error(bstack11l1l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࠥඹ") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1111llll1_opy_
  atexit.register(bstack1llll1l1_opy_)
  signal.signal(signal.SIGINT, bstack11lllll11_opy_)
  signal.signal(signal.SIGTERM, bstack11lllll11_opy_)
def bstack1111llll1_opy_(exctype, value, traceback):
  global bstack1ll1111ll1_opy_
  try:
    for driver in bstack1ll1111ll1_opy_:
      bstack11lll1l11l_opy_(driver, bstack11l1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧය"), bstack11l1l11_opy_ (u"ࠣࡕࡨࡷࡸ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦර") + str(value))
  except Exception:
    pass
  logger.info(bstack1lll11lll1_opy_)
  bstack1l111l1111_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1l111l1111_opy_(message=bstack11l1l11_opy_ (u"ࠩࠪ඼"), bstack1ll11lll_opy_ = False):
  global CONFIG
  bstack1l1ll11ll1_opy_ = bstack11l1l11_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠬල") if bstack1ll11lll_opy_ else bstack11l1l11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ඾")
  bstack111l1l111l_opy_ = bstack11ll1l1l1_opy_.bstack1l11l111ll_opy_(EVENTS.bstack111ll1ll1_opy_)
  try:
    if message:
      bstack11l1111111_opy_ = {
        bstack1l1ll11ll1_opy_ : str(message)
      }
      try:
        bstack11l1l11lll_opy_(bstack1l1lll1lll_opy_, CONFIG, bstack11l1111111_opy_)
      finally:
        bstack11ll1l1l1_opy_.end(EVENTS.bstack111ll1ll1_opy_.value, bstack111l1l111l_opy_ + bstack11l1l11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ඿"), bstack111l1l111l_opy_ + bstack11l1l11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦව"), status=True, failure=None, test_name=None)
    else:
      try:
        bstack11l1l11lll_opy_(bstack1l1lll1lll_opy_, CONFIG)
      finally:
        bstack11ll1l1l1_opy_.end(EVENTS.bstack111ll1ll1_opy_.value, bstack111l1l111l_opy_ + bstack11l1l11_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢශ"), bstack111l1l111l_opy_ + bstack11l1l11_opy_ (u"ࠣ࠼ࡨࡲࡩࠨෂ"), status=True, failure=None, test_name=None)
  except Exception as e:
    logger.debug(bstack1ll1lll111_opy_.format(str(e)))
def bstack111lll11ll_opy_(bstack1l11ll11l1_opy_, size):
  bstack1l11l11l11_opy_ = []
  while len(bstack1l11ll11l1_opy_) > size:
    bstack1l1llll111_opy_ = bstack1l11ll11l1_opy_[:size]
    bstack1l11l11l11_opy_.append(bstack1l1llll111_opy_)
    bstack1l11ll11l1_opy_ = bstack1l11ll11l1_opy_[size:]
  bstack1l11l11l11_opy_.append(bstack1l11ll11l1_opy_)
  return bstack1l11l11l11_opy_
def bstack1lllll11_opy_(args):
  if bstack11l1l11_opy_ (u"ࠩ࠰ࡱࠬස") in args and bstack11l1l11_opy_ (u"ࠪࡴࡩࡨࠧහ") in args:
    return True
  return False
@measure(event_name=EVENTS.bstack1ll111l1l1_opy_, stage=STAGE.bstack11111l11l_opy_)
def run_on_browserstack(bstack1llll1lll1_opy_=None, bstack1ll1ll1l1_opy_=None, bstack11lll1lll_opy_=False):
  global CONFIG
  global bstack1l1l11ll11_opy_
  global bstack1l11ll1ll1_opy_
  global bstack1lll1ll1l1_opy_
  global global_config
  bstack1l111ll11l_opy_ = bstack11l1l11_opy_ (u"ࠫࠬළ")
  bstack1l1l1111ll_opy_ = bstack11l1l11_opy_ (u"ࠧࠨෆ")
  bstack111ll1lll_opy_(bstack1l11ll1ll_opy_, logger)
  if bstack1llll1lll1_opy_ and isinstance(bstack1llll1lll1_opy_, str):
    bstack1llll1lll1_opy_ = eval(bstack1llll1lll1_opy_)
  if bstack1llll1lll1_opy_:
    CONFIG = bstack1llll1lll1_opy_[bstack11l1l11_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭෇")]
    bstack1l1l11ll11_opy_ = bstack1llll1lll1_opy_[bstack11l1l11_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨ෈")]
    bstack1l11ll1ll1_opy_ = bstack1llll1lll1_opy_[bstack11l1l11_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ෉")]
    global_config.bstack1l111111ll_opy_(bstack11l1l11_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈ්ࠫ"), bstack1l11ll1ll1_opy_)
    bstack1l111ll11l_opy_ = bstack11l1l11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠫ෋")
  global_config.bstack1l111111ll_opy_(bstack11l1l11_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭෌"), uuid4().__str__())
  logger.info(bstack11l1l11_opy_ (u"࡙ࠬࡄࡌࠢࡵࡹࡳࠦࡳࡵࡣࡵࡸࡪࡪࠠࡸ࡫ࡷ࡬ࠥ࡯ࡤ࠻ࠢࠪ෍") + global_config.get_property(bstack11l1l11_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨ෎")));
  logger.debug(bstack11l1l11_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥ࠿ࠪා") + global_config.get_property(bstack11l1l11_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪැ")))
  if not bstack11lll1lll_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack111lll1l1l_opy_)
      return
    if sys.argv[1] == bstack11l1l11_opy_ (u"ࠩ࠰࠱ࡻ࡫ࡲࡴ࡫ࡲࡲࠬෑ") or sys.argv[1] == bstack11l1l11_opy_ (u"ࠪ࠱ࡻ࠭ි"):
      logger.info(bstack11l1l11_opy_ (u"ࠫࡇࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡔࡾࡺࡨࡰࡰࠣࡗࡉࡑࠠࡷࡽࢀࠫී").format(__version__))
      return
    if sys.argv[1] == bstack11l1l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫු"):
      bstack11l11l111_opy_()
      return
    if sys.argv[1] == bstack11l1l11_opy_ (u"࠭࡬ࡰࡣࡧࠫ෕"):
      from browserstack_sdk.bstack1lll11l11l_opy_ import bstack1ll11l11l1_opy_
      bstack111l1l11l1_opy_()
      bstack1ll11l11l1_opy_(CONFIG)
      return
  args = sys.argv
  bstack111l1l11l1_opy_()
  global bstack111ll1llll_opy_
  try:
    from bstack_utils import constants as bstack11lllll1ll_opy_
    override_value = CONFIG.get(bstack11l1l11_opy_ (u"ࠧࡰࡸࡨࡶࡷ࡯ࡤࡦࡎࡲࡥࡩ࡚ࡥࡴࡶ࡬ࡲ࡬࠭ූ"), False)
    bstack111ll1llll_opy_ = bool(override_value)
  except Exception as e:
    logger.error(bstack11l1l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡕࡖࡆࡔࡕࡍࡉࡋ࡟ࡍࡑࡄࡈࡤ࡚ࡅࡔࡖࡌࡒࡌࡀࠠࡼࡿࠥ෗").format(e))
    bstack111ll1llll_opy_ = False
  if bstack111ll1llll_opy_:
    bstack111l11l11_opy_ = CONFIG.get(bstack11l1l11_opy_ (u"ࠩ࡯ࡳࡦࡪࡔࡦࡵࡷ࡭ࡳ࡭ࡈࡶࡤࡘࡖࡑ࠭ෘ")) or bstack11lllll1ll_opy_.bstack1ll1ll1ll1_opy_
    logger.info(bstack11l1l11_opy_ (u"ࠥࡋࡱࡵࡢࡢ࡮ࠣࡳࡻ࡫ࡲࡳ࡫ࡧࡩࡱࡵࡡࡥࡶࡨࡷࡹ࡯࡮ࡨࠢࡨࡲࡦࡨ࡬ࡦࡦ࠯ࠤࡺࡹࡩ࡯ࡩࠣ࡬ࡺࡨ࠺ࠡࡽࢀࠦෙ").format(bstack111l11l11_opy_))
    bstack1l1l11ll11_opy_ = bstack111l11l11_opy_
    try:
      bstack11lllll1ll_opy_.HTTPS_HUB = bstack111l11l11_opy_
      bstack11lllll1ll_opy_.bstack11ll1l1l11_opy_ = bstack111l11l11_opy_
    except Exception:
      pass
  global bstack1lll1l1l11_opy_
  global bstack11ll111l1_opy_
  global bstack1l11ll11ll_opy_
  global bstack11l1l11111_opy_
  global bstack11ll1l111_opy_
  global bstack1l1l1l1ll1_opy_
  global bstack1ll111l11l_opy_
  global bstack1111lllll_opy_
  global bstack111ll11l11_opy_
  global bstack1lll11lll_opy_
  global bstack11l111l1_opy_
  bstack11ll111l1_opy_ = len(CONFIG.get(bstack11l1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧේ"), []))
  if not bstack1l111ll11l_opy_:
    if args[1] == bstack11l1l11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬෛ") or args[1] == bstack11l1l11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧො") or args[1] == bstack11l1l11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡨࡧࡱࡩࡷ࡯ࡣࠨෝ"):
      bstack1l111ll11l_opy_ = bstack11l1l11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩෞ")
      args = args[2:]
    elif args[1] == bstack11l1l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨෟ"):
      bstack1l111ll11l_opy_ = bstack11l1l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ෠")
      args = args[2:]
    elif args[1] == bstack11l1l11_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ෡"):
      bstack1l111ll11l_opy_ = bstack11l1l11_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ෢")
      args = args[2:]
    elif args[1] == bstack11l1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧ෣"):
      bstack1l111ll11l_opy_ = bstack11l1l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ෤")
      args = args[2:]
    elif args[1] == bstack11l1l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ෥"):
      bstack1l111ll11l_opy_ = bstack11l1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ෦")
      args = args[2:]
    elif args[1] == bstack11l1l11_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ෧"):
      bstack1l111ll11l_opy_ = bstack11l1l11_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ෨")
      args = args[2:]
    else:
      if not bstack11l1l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ෩") in CONFIG or str(CONFIG[bstack11l1l11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ෪")]).lower() in [bstack11l1l11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ෫"), bstack11l1l11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩ෬"), bstack11l1l11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠪ෭")]:
        bstack1l111ll11l_opy_ = bstack11l1l11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠫ෮")
        args = args[1:]
      elif str(CONFIG[bstack11l1l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ෯")]).lower() == bstack11l1l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ෰"):
        bstack1l111ll11l_opy_ = bstack11l1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ෱")
        args = args[1:]
      elif str(CONFIG[bstack11l1l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪෲ")]).lower() == bstack11l1l11_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧෳ"):
        bstack1l111ll11l_opy_ = bstack11l1l11_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ෴")
        args = args[1:]
      elif str(CONFIG[bstack11l1l11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭෵")]).lower() == bstack11l1l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ෶"):
        bstack1l111ll11l_opy_ = bstack11l1l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ෷")
        args = args[1:]
      elif str(CONFIG[bstack11l1l11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ෸")]).lower() == bstack11l1l11_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ෹"):
        bstack1l111ll11l_opy_ = bstack11l1l11_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ෺")
        args = args[1:]
      else:
        os.environ[bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫ෻")] = bstack1l111ll11l_opy_
        bstack11l1lll11l_opy_(bstack1lll11l1ll_opy_)
  os.environ[bstack11l1l11_opy_ (u"ࠪࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡕࡔࡇࡇࠫ෼")] = bstack1l111ll11l_opy_
  bstack1lll1ll1l1_opy_ = bstack1l111ll11l_opy_
  if cli.is_enabled(CONFIG):
    try:
      bstack11ll11lll1_opy_ = bstack1l1l1l1l_opy_[bstack11l1l11_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗ࠱ࡇࡊࡄࠨ෽")] if bstack1l111ll11l_opy_ == bstack11l1l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ෾") and bstack1llll1ll1_opy_() else bstack1l111ll11l_opy_
      bstack11l1l1l11_opy_.invoke(bstack1lllllll1_opy_.bstack111l11ll_opy_, bstack11l1l1ll1_opy_(
        sdk_version=__version__,
        path_config=bstack11l1lll111_opy_(),
        path_project=os.getcwd(),
        test_framework=bstack11ll11lll1_opy_,
        frameworks=[bstack11ll11lll1_opy_],
        framework_versions={
          bstack11ll11lll1_opy_: bstack1l11ll1l1_opy_(bstack11l1l11_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬ෿") if bstack1l111ll11l_opy_ in [bstack11l1l11_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭฀"), bstack11l1l11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧก"), bstack11l1l11_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪข")] else bstack1l111ll11l_opy_)
        },
        bs_config=CONFIG
      ))
      if cli.config and cli.config.get(bstack11l1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧฃ"), None):
        CONFIG[bstack11l1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࠨค")] = cli.config.get(bstack11l1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠢฅ"), None)
    except Exception as e:
      bstack11l1l1l11_opy_.invoke(bstack1lllllll1_opy_.bstack1l1111ll1l_opy_, e.__traceback__, 1)
    if bstack1l11ll1ll1_opy_:
      CONFIG[bstack11l1l11_opy_ (u"ࠨࡡࡱࡲࠥฆ")] = cli.config[bstack11l1l11_opy_ (u"ࠢࡢࡲࡳࠦง")]
      logger.info(bstack1l111l1l1_opy_.format(CONFIG[bstack11l1l11_opy_ (u"ࠨࡣࡳࡴࠬจ")]))
  else:
    bstack11l1l1l11_opy_.clear()
  global bstack11ll11ll11_opy_
  global bstack1l1l1l1lll_opy_
  if bstack1llll1lll1_opy_:
    try:
      bstack111l11l1l1_opy_ = datetime.datetime.now()
      os.environ[bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫฉ")] = bstack1l111ll11l_opy_
      bstack1l1l1lll_opy_ = bstack11ll1l1l1_opy_.bstack1l11l111ll_opy_(EVENTS.bstack1llll11l1_opy_)
      try:
        logger.info(bstack11l1l11_opy_ (u"ࠥࡗࡪࡴࡤࡪࡰࡪࠤࡘࡊࡋࠡࡖࡨࡷࡹࠦࡁࡵࡶࡨࡱࡵࡺࡥࡥࠢࡨࡺࡪࡴࡴࠣช"))
        bstack11l1l11lll_opy_(bstack11l1l1ll1l_opy_, CONFIG)
      finally:
        bstack11ll1l1l1_opy_.end(EVENTS.bstack1llll11l1_opy_.value, bstack1l1l1lll_opy_ + bstack11l1l11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦซ"), bstack1l1l1lll_opy_ + bstack11l1l11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥฌ"), status=True, failure=None, test_name=None)
      cli.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠨࡨࡵࡶࡳ࠾ࡸࡪ࡫ࡠࡶࡨࡷࡹࡥࡡࡵࡶࡨࡱࡵࡺࡥࡥࠤญ"), datetime.datetime.now() - bstack111l11l1l1_opy_)
    except Exception as e:
      logger.debug(bstack11lll111ll_opy_.format(str(e)))
  global bstack11l1ll11l1_opy_
  global bstack1l1ll111l1_opy_
  global bstack1ll111l111_opy_
  global bstack1l11llll11_opy_
  global bstack1l111l111l_opy_
  global bstack1l1lllllll_opy_
  global bstack1lll111lll_opy_
  global bstack1lll111111_opy_
  global bstack111l1l111_opy_
  global bstack11l111lll1_opy_
  global bstack1l1l111ll1_opy_
  global bstack11l11l1l_opy_
  global bstack11111lll_opy_
  global bstack11lll11ll_opy_
  global bstack111l1111ll_opy_
  global bstack1lll111ll_opy_
  global bstack111l1ll11l_opy_
  global bstack1l11l1ll1_opy_
  global bstack11l11llll1_opy_
  global bstack11l111l11l_opy_
  global bstack1lll1lll1l_opy_
  global bstack1l1l1111l_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11l1ll11l1_opy_ = webdriver.Remote.__init__
    bstack1l1ll111l1_opy_ = WebDriver.quit
    bstack11l11l1l_opy_ = WebDriver.close
    bstack1lll111ll_opy_ = WebDriver.get
    bstack1l1l1111l_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack11ll11ll11_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack11llllll1_opy_
    bstack1l1l1l1lll_opy_ = bstack11llllll1_opy_()
  except Exception as e:
    pass
  try:
    global bstack1l11llll1_opy_
    from QWeb.keywords import browser
    bstack1l11llll1_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1l1llll1_opy_(CONFIG) and bstack1ll111l1l_opy_():
    if bstack1l1ll1111l_opy_() < version.parse(bstack1lll11ll1l_opy_):
      logger.error(bstack11lllll1_opy_.format(bstack1l1ll1111l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack11l1l11_opy_ (u"ࠧࡠࡩࡨࡸࡤࡶࡲࡰࡺࡼࡣࡺࡸ࡬ࠨฎ")) and callable(getattr(RemoteConnection, bstack11l1l11_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩฏ"))):
          RemoteConnection._get_proxy_url = bstack1l1111l111_opy_
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          ClientConfig.get_proxy_url = bstack1l1111l111_opy_
      except Exception as e:
        logger.error(bstack1l1ll1l1l1_opy_.format(str(e)))
  if not CONFIG.get(bstack11l1l11_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫฐ"), False) and not bstack1llll1lll1_opy_:
    logger.info(bstack1ll1l111_opy_)
  bstack11ll111l1l_opy_ = not cli.is_enabled(CONFIG) and bstack1l111ll11l_opy_ not in [bstack11l1l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫฑ")]
  bstack1l1l1l11_opy_ = bstack11ll111l1l_opy_ and bstack11l1l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨฒ") in CONFIG and str(CONFIG[bstack11l1l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩณ")]).lower() != bstack11l1l11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬด")
  bstack11l1l11l11_opy_ = bstack11ll111l1l_opy_ and not bstack1l1l1l11_opy_ and (bstack1l111ll11l_opy_ != bstack11l1l11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡨࡧࡱࡩࡷ࡯ࡣࠨต") or (bstack1l111ll11l_opy_ == bstack11l1l11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩถ") and not bstack1llll1lll1_opy_))
  if bstack1l111ll11l_opy_ not in [bstack11l1l11_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪท")]:
    bstack111ll1lll_opy_(os.path.join(os.getcwd(), bstack11l1l11_opy_ (u"ࠪࡰࡴ࡭ࠧธ"), bstack11l1l11_opy_ (u"ࠫࡰ࡫ࡹ࠮࡯ࡨࡸࡷ࡯ࡣࡴ࠰࡭ࡷࡴࡴࠧน")), logger)
  if (bstack1l111ll11l_opy_ in [bstack11l1l11_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫบ"), bstack11l1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬป"), bstack11l1l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨผ")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      try:
        from pabot.pabot import QueueItem
        from pabot import pabot
      except Exception as e:
        logger.warning(bstack1llllll1ll_opy_ + str(e))
      if not is_robot_playwright_installed():
        try:
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
          WebDriverCreator._get_ff_profile = bstack111lll1l1_opy_
          bstack1l1lllllll_opy_ = WebDriverCache.close
        except Exception as e:
          logger.warning(bstack1ll1l11l_opy_ + str(e))
        try:
          from AppiumLibrary.utils.applicationcache import ApplicationCache
          bstack1l111l111l_opy_ = ApplicationCache.close
        except Exception as e:
          logger.debug(bstack1l111lll1_opy_ + str(e))
    except Exception as e:
      bstack1ll1llll1l_opy_(e, bstack1ll1l11l_opy_)
    if bstack1l111ll11l_opy_ != bstack11l1l11_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩฝ"):
      bstack1l1l11l111_opy_()
    bstack1ll111l111_opy_ = Output.start_test
    bstack1l11llll11_opy_ = Output.end_test
    bstack1lll111lll_opy_ = TestStatus.__init__
    bstack111l1l111_opy_ = pabot._run
    bstack11l111lll1_opy_ = QueueItem.__init__
    bstack1l1l111ll1_opy_ = pabot._create_command_for_execution
    bstack11l111l11l_opy_ = pabot._report_results
  if bstack1l111ll11l_opy_ == bstack11l1l11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩพ"):
    global bstack1ll1lll1ll_opy_
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll1llll1l_opy_(e, bstack11l1l1l111_opy_)
    bstack11111lll_opy_ = Runner.run_hook
    bstack11lll11ll_opy_ = Runner.load_hooks
    bstack111l1111ll_opy_ = Step.run
    try:
      sig = inspect.signature(bstack11111lll_opy_)
      params = list(sig.parameters.keys())
      bstack1ll1lll1ll_opy_ = bstack11l1l11_opy_ (u"ࠪࡧࡴࡴࡴࡦࡺࡷࠫฟ") in params
      logger.info(bstack11l1l11_opy_ (u"ࠫࡉ࡫ࡴࡦࡥࡷࡩࡩࠦࡢࡦࡪࡤࡺࡪࠦࡲࡶࡰࡢ࡬ࡴࡵ࡫ࠡࡵ࡬࡫ࡳࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨภ").format(bstack11l1l11_opy_ (u"ࠬ࠷࠮࠳࠰࠹ࠤ࠭ࡽࡩࡵࡪࠣࡧࡴࡴࡴࡦࡺࡷ࠭ࠬม") if bstack1ll1lll1ll_opy_ else bstack11l1l11_opy_ (u"࠭࠱࠯࠵࠮ࠤ࠭ࡽࡩࡵࡪࡲࡹࡹࠦࡣࡰࡰࡷࡩࡽࡺࠩࠨย")))
    except Exception as e:
      logger.debug(bstack11l1l11_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡤࡶࠣࡦࡪ࡮ࡡࡷࡧࠣࡶࡺࡴ࡟ࡩࡱࡲ࡯ࠥࡹࡩࡨࡰࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬร").format(str(e)))
      bstack1ll1lll1ll_opy_ = None
  if bstack1l111ll11l_opy_ == bstack11l1l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨฤ"):
    try:
      from _pytest.config import Config
      bstack1l11l1ll1_opy_ = Config.getoption
      from _pytest import runner
      bstack11l11llll1_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warning(bstack11l1l11_opy_ (u"ࠤࠨࡷ࠿ࠦࠥࡴࠤล"), bstack11l11ll1ll_opy_, str(e))
    try:
      from pytest_bdd import reporting
      bstack1lll1lll1l_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack11l1l11_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡲࠤࡷࡻ࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࡶࠫฦ"))
    if bstack1l1l1l1l11_opy_():
      logger.warning(bstack11l111l1l_opy_[bstack11l1l11_opy_ (u"ࠫࡘࡊࡋ࠮ࡉࡈࡒ࠲࠶࠰࠶ࠩว")])
  try:
    framework_name = bstack11l1l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫศ") if bstack1l111ll11l_opy_ in [bstack11l1l11_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬษ"), bstack11l1l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ส"), bstack11l1l11_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩห")] else bstack1ll11l1111_opy_(bstack1l111ll11l_opy_)
    bstack11l1l11l1_opy_ = {
      bstack11l1l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࠪฬ"): bstack11l1l11_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶ࠰ࡧࡺࡩࡵ࡮ࡤࡨࡶࠬอ") if bstack1l111ll11l_opy_ == bstack11l1l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫฮ") and bstack1llll1ll1_opy_() else framework_name,
      bstack11l1l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩฯ"): bstack1l11ll1l1_opy_(framework_name),
      bstack11l1l11_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫะ"): __version__,
      bstack11l1l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨั"): bstack1l111ll11l_opy_
    }
    if bstack1l111ll11l_opy_ in bstack11ll1l1lll_opy_ + bstack11l111111_opy_:
      if bstack1l111ll111_opy_.bstack111l1ll1l_opy_(CONFIG):
        if bstack11l1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨา") in CONFIG:
          os.environ[bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪำ")] = os.getenv(bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫิ"), json.dumps(CONFIG[bstack11l1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫี")]))
          CONFIG[bstack11l1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬึ")].pop(bstack11l1l11_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫื"), None)
          CONFIG[bstack11l1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹุࠧ")].pop(bstack11l1l11_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪู࠭"), None)
        bstack11l1l11l1_opy_[bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ฺࠩ")] = {
          bstack11l1l11_opy_ (u"ࠪࡲࡦࡳࡥࠨ฻"): bstack11l1l11_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭฼"),
          bstack11l1l11_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭฽"): str(bstack1l1ll1111l_opy_())
        }
    bstack1ll1ll11l_opy_, bstack1lllllll1l_opy_ = None, {}
    bstack11ll1l1111_opy_ = None
    bstack111ll1l11l_opy_ = None
    def bstack1ll1l11l1_opy_():
      if bstack1l1l1l11_opy_:
        bstack1ll1l1l1ll_opy_()
      elif bstack11l1l11l11_opy_:
        bstack1ll1ll1l_opy_()
    def bstack1ll1llll11_opy_():
      nonlocal bstack1ll1ll11l_opy_, bstack1lllllll1l_opy_
      if bstack1l111ll11l_opy_ not in [bstack11l1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧ฾")] and not cli.is_running():
        bstack1ll1ll11l_opy_, bstack1lllllll1l_opy_ = TestHubHandler.launch(CONFIG, bstack11l1l11l1_opy_)
    if bstack1l1l1l11_opy_ or bstack11l1l11l11_opy_:
      bstack11ll1l1111_opy_ = threading.Thread(target=bstack1ll1l11l1_opy_)
      bstack11ll1l1111_opy_.start()
    if bstack1l111ll11l_opy_ not in [bstack11l1l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ฿")] and not cli.is_running():
      bstack111ll1l11l_opy_ = threading.Thread(target=bstack1ll1llll11_opy_)
      bstack111ll1l11l_opy_.start()
    if bstack11ll1l1111_opy_:
      bstack11ll1l1111_opy_.join()
    if bstack111ll1l11l_opy_:
      bstack111ll1l11l_opy_.join()
    if bstack1lllllll1l_opy_.get(bstack11l1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨเ")) is not None and bstack1l111ll111_opy_.bstack11l1ll1ll1_opy_(CONFIG) is None:
      value = bstack1lllllll1l_opy_[bstack11l1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩแ")].get(bstack11l1l11_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫโ"))
      if value is not None:
          CONFIG[bstack11l1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫใ")] = value
      else:
        logger.debug(bstack11l1l11_opy_ (u"ࠧࡔ࡯ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡦࡤࡸࡦࠦࡦࡰࡷࡱࡨࠥ࡯࡮ࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠥไ"))
  except Exception as e:
    logger.debug(bstack1llll1lll_opy_.format(bstack11l1l11_opy_ (u"࠭ࡔࡦࡵࡷࡌࡺࡨࠧๅ"), str(e)))
  if bstack1l111ll11l_opy_ == bstack11l1l11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡨࡧࡱࡩࡷ࡯ࡣࠨๆ"):
    bstack1l11ll11ll_opy_ = True
    if bstack1llll1lll1_opy_ and bstack11lll1lll_opy_:
      if cli.is_enabled(CONFIG):
        bstack1l1l1l1ll1_opy_ = cli.config.get(bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ็"), {}).get(bstack11l1l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ่ࠫ")) if cli.config else None
      else:
        bstack1l1l1l1ll1_opy_ = CONFIG.get(bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹ้ࠧ"), {}).get(bstack11l1l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ๊࠭"))
      bstack11ll11l111_opy_(bstack1lll1111ll_opy_)
    elif bstack1llll1lll1_opy_:
      if cli.is_enabled(CONFIG):
        bstack1l1l1l1ll1_opy_ = cli.config.get(bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴ๋ࠩ"), {}).get(bstack11l1l11_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ์")) if cli.config else None
      else:
        bstack1l1l1l1ll1_opy_ = CONFIG.get(bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫํ"), {}).get(bstack11l1l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ๎"))
      global bstack1ll1111ll1_opy_
      try:
        if bstack1lllll11_opy_(bstack1llll1lll1_opy_[bstack11l1l11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ๏")]) and multiprocessing.current_process().name == bstack11l1l11_opy_ (u"ࠪ࠴ࠬ๐"):
          bstack1llll1lll1_opy_[bstack11l1l11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ๑")].remove(bstack11l1l11_opy_ (u"ࠬ࠳࡭ࠨ๒"))
          bstack1llll1lll1_opy_[bstack11l1l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ๓")].remove(bstack11l1l11_opy_ (u"ࠧࡱࡦࡥࠫ๔"))
          bstack1llll1lll1_opy_[bstack11l1l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ๕")] = bstack1llll1lll1_opy_[bstack11l1l11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ๖")][0]
          with open(bstack1llll1lll1_opy_[bstack11l1l11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭๗")], bstack11l1l11_opy_ (u"ࠫࡷ࠭๘")) as f:
            bstack111l1lllll_opy_ = f.read()
          bstack11111l1l1_opy_ = bstack11l1l11_opy_ (u"ࠧࠨࠢࡧࡴࡲࡱࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡸࡪ࡫ࠡ࡫ࡰࡴࡴࡸࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡨ࠿ࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥࠩࡽࢀ࠭ࡀࠦࡦࡳࡱࡰࠤࡵࡪࡢࠡ࡫ࡰࡴࡴࡸࡴࠡࡒࡧࡦࡀࠦ࡯ࡨࡡࡧࡦࠥࡃࠠࡑࡦࡥ࠲ࡩࡵ࡟ࡣࡴࡨࡥࡰࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡨࡪ࡬ࠠ࡮ࡱࡧࡣࡧࡸࡥࡢ࡭ࠫࡷࡪࡲࡦ࠭ࠢࡤࡶ࡬࠲ࠠࡵࡧࡰࡴࡴࡸࡡࡳࡻࠣࡁࠥ࠶ࠩ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡵࡴࡼ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡧࡲࡨࠢࡀࠤࡸࡺࡲࠩ࡫ࡱࡸ࠭ࡧࡲࡨࠫ࠮࠵࠵࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡫ࡸࡤࡧࡳࡸࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡣࡶࠤࡪࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡱࡣࡶࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡳ࡬ࡥࡤࡣࠪࡶࡩࡱ࡬ࠬࡢࡴࡪ࠰ࡹ࡫࡭ࡱࡱࡵࡥࡷࡿࠩࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡕࡪࡢ࠯ࡦࡲࡣࡧࠦ࠽ࠡ࡯ࡲࡨࡤࡨࡲࡦࡣ࡮ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡑࡦࡥ࠲ࡩࡵ࡟ࡣࡴࡨࡥࡰࠦ࠽ࠡ࡯ࡲࡨࡤࡨࡲࡦࡣ࡮ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡑࡦࡥࠬ࠮࠴ࡳࡦࡶࡢࡸࡷࡧࡣࡦࠪࠬࡠࡳࠨࠢࠣ๙").format(str(bstack1llll1lll1_opy_))
          bstack1lllll1111_opy_ = bstack11111l1l1_opy_ + bstack111l1lllll_opy_
          bstack1l1111ll_opy_ = bstack1llll1lll1_opy_[bstack11l1l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ๚")] + bstack11l1l11_opy_ (u"ࠧࡠࡤࡶࡸࡦࡩ࡫ࡠࡶࡨࡱࡵ࠴ࡰࡺࠩ๛")
          with open(bstack1l1111ll_opy_, bstack11l1l11_opy_ (u"ࠨࡹࠪ๜")):
            pass
          with open(bstack1l1111ll_opy_, bstack11l1l11_opy_ (u"ࠤࡺ࠯ࠧ๝")) as f:
            f.write(bstack1lllll1111_opy_)
          import subprocess
          bstack1l1l11lll_opy_ = subprocess.run([bstack11l1l11_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࠥ๞"), bstack1l1111ll_opy_])
          if os.path.exists(bstack1l1111ll_opy_):
            os.unlink(bstack1l1111ll_opy_)
          os._exit(bstack1l1l11lll_opy_.returncode)
        else:
          if bstack1lllll11_opy_(bstack1llll1lll1_opy_[bstack11l1l11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ๟")]):
            bstack1llll1lll1_opy_[bstack11l1l11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ๠")].remove(bstack11l1l11_opy_ (u"࠭࠭࡮ࠩ๡"))
            bstack1llll1lll1_opy_[bstack11l1l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ๢")].remove(bstack11l1l11_opy_ (u"ࠨࡲࡧࡦࠬ๣"))
            bstack1llll1lll1_opy_[bstack11l1l11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ๤")] = bstack1llll1lll1_opy_[bstack11l1l11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭๥")][0]
          bstack11ll11l111_opy_(bstack1lll1111ll_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1llll1lll1_opy_[bstack11l1l11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ๦")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack11l1l11_opy_ (u"ࠬࡥ࡟࡯ࡣࡰࡩࡤࡥࠧ๧")] = bstack11l1l11_opy_ (u"࠭࡟ࡠ࡯ࡤ࡭ࡳࡥ࡟ࠨ๨")
          mod_globals[bstack11l1l11_opy_ (u"ࠧࡠࡡࡩ࡭ࡱ࡫࡟ࡠࠩ๩")] = os.path.abspath(bstack1llll1lll1_opy_[bstack11l1l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ๪")])
          exec(open(bstack1llll1lll1_opy_[bstack11l1l11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ๫")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack11l1l11_opy_ (u"ࠪࡇࡦࡻࡧࡩࡶࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࡼࡿࠪ๬").format(str(e)))
          for driver in bstack1ll1111ll1_opy_:
            bstack1ll1ll1l1_opy_.append({
              bstack11l1l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ๭"): bstack1llll1lll1_opy_[bstack11l1l11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ๮")],
              bstack11l1l11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ๯"): str(e),
              bstack11l1l11_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭๰"): multiprocessing.current_process().name
            })
            bstack11lll1l11l_opy_(driver, bstack11l1l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ๱"), bstack11l1l11_opy_ (u"ࠤࡖࡩࡸࡹࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧ๲") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1ll1111ll1_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1l11ll1ll1_opy_, CONFIG, logger)
      bstack11lll1lll1_opy_()
      bstack11ll1lll1_opy_()
      percy.bstack1lll111l_opy_()
      bstack1lllll1l11_opy_ = {
        bstack11l1l11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭๳"): args[0],
        bstack11l1l11_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫ๴"): CONFIG,
        bstack11l1l11_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭๵"): bstack1l1l11ll11_opy_,
        bstack11l1l11_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ๶"): bstack1l11ll1ll1_opy_
      }
      if bstack11l1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ๷") in CONFIG:
        bstack1l111llll1_opy_ = bstack11ll1llll1_opy_(args, logger, CONFIG, bstack1l1111111_opy_, bstack11ll111l1_opy_)
        bstack1111lllll_opy_ = bstack1l111llll1_opy_.bstack1lllll111_opy_(run_on_browserstack, bstack1lllll1l11_opy_, bstack1lllll11_opy_(args))
      else:
        if bstack1lllll11_opy_(args):
          bstack1lllll1l11_opy_[bstack11l1l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ๸")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1lllll1l11_opy_,))
          test.start()
          test.join()
        else:
          bstack11ll11l111_opy_(bstack1lll1111ll_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack11l1l11_opy_ (u"ࠩࡢࡣࡳࡧ࡭ࡦࡡࡢࠫ๹")] = bstack11l1l11_opy_ (u"ࠪࡣࡤࡳࡡࡪࡰࡢࡣࠬ๺")
          mod_globals[bstack11l1l11_opy_ (u"ࠫࡤࡥࡦࡪ࡮ࡨࡣࡤ࠭๻")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1l111ll11l_opy_ == bstack11l1l11_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ๼") or bstack1l111ll11l_opy_ == bstack11l1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ๽"):
    percy.init(bstack1l11ll1ll1_opy_, CONFIG, logger)
    percy.bstack1lll111l_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1ll1llll1l_opy_(e, bstack1ll1l11l_opy_)
    bstack11lll1lll1_opy_()
    bstack11ll11l111_opy_(bstack1ll1l11l11_opy_)
    if bstack1l1111111_opy_:
      bstack111l1ll1ll_opy_(bstack1ll1l11l11_opy_, args)
      if bstack11l1l11_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ๾") in args:
        i = args.index(bstack11l1l11_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭๿"))
        args.pop(i)
        args.pop(i)
      if bstack11l1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ຀") not in CONFIG:
        CONFIG[bstack11l1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ກ")] = [{}]
        bstack11ll111l1_opy_ = 1
      if bstack1lll1l1l11_opy_ == 0:
        bstack1lll1l1l11_opy_ = 1
      args.insert(0, str(bstack1lll1l1l11_opy_))
      args.insert(0, str(bstack11l1l11_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩຂ")))
    if TestHubHandler.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1ll11l11ll_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack11ll11ll1_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack11l1l11_opy_ (u"ࠧࡘࡏࡃࡑࡗࡣࡔࡖࡔࡊࡑࡑࡗࠧ຃"),
        ).parse_args(bstack1ll11l11ll_opy_)
        bstack11ll11l1_opy_ = args.index(bstack1ll11l11ll_opy_[0]) if len(bstack1ll11l11ll_opy_) > 0 else len(args)
        args.insert(bstack11ll11l1_opy_, str(bstack11l1l11_opy_ (u"࠭࠭࠮࡮࡬ࡷࡹ࡫࡮ࡦࡴࠪຄ")))
        args.insert(bstack11ll11l1_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11l1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡳࡱࡥࡳࡹࡥ࡬ࡪࡵࡷࡩࡳ࡫ࡲ࠯ࡲࡼࠫ຅"))))
        if bstack1l1l11l11l_opy_.bstack111lll1l11_opy_(CONFIG):
          args.insert(bstack11ll11l1_opy_, str(bstack11l1l11_opy_ (u"ࠨ࠯࠰ࡰ࡮ࡹࡴࡦࡰࡨࡶࠬຆ")))
          args.insert(bstack11ll11l1_opy_ + 1, str(bstack11l1l11_opy_ (u"ࠩࡕࡩࡹࡸࡹࡇࡣ࡬ࡰࡪࡪ࠺ࡼࡿࠪງ").format(bstack1l1l11l11l_opy_.bstack111lll1ll1_opy_(CONFIG))))
        if bstack1lll1l111_opy_(os.environ.get(bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠨຈ"))) and str(os.environ.get(bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠨຉ"), bstack11l1l11_opy_ (u"ࠬࡴࡵ࡭࡮ࠪຊ"))) != bstack11l1l11_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ຋"):
          for bstack11lllll1l_opy_ in bstack11ll11ll1_opy_:
            args.remove(bstack11lllll1l_opy_)
          test_files = os.environ.get(bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠫຌ")).split(bstack11l1l11_opy_ (u"ࠨ࠮ࠪຍ"))
          for bstack111l11llll_opy_ in test_files:
            args.append(bstack111l11llll_opy_)
      except Exception as e:
        logger.error(bstack11l1l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡢࡶࡷࡥࡨ࡮ࡩ࡯ࡩࠣࡰ࡮ࡹࡴࡦࡰࡨࡶࠥ࡬࡯ࡳࠢࡾࢁ࠳ࠦࡅࡳࡴࡲࡶࠥ࠳ࠠࡼࡿࠥຎ").format(bstack1l1l1l11l1_opy_, e))
    pabot.main(args)
  elif bstack1l111ll11l_opy_ == bstack11l1l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫຏ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1ll1llll1l_opy_(e, bstack1ll1l11l_opy_)
    for a in args:
      if bstack11l1l11_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚ࠪຐ") in a:
        bstack11ll1l111_opy_ = int(a.split(bstack11l1l11_opy_ (u"ࠬࡀࠧຑ"))[1])
      if bstack11l1l11_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪຒ") in a:
        bstack1l1l1l1ll1_opy_ = str(a.split(bstack11l1l11_opy_ (u"ࠧ࠻ࠩຓ"))[1])
      if bstack11l1l11_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓࠨດ") in a:
        bstack1ll111l11l_opy_ = str(a.split(bstack11l1l11_opy_ (u"ࠩ࠽ࠫຕ"))[1])
    bstack11l1l11l_opy_ = None
    bstack111llll1_opy_ = None
    if bstack11l1l11_opy_ (u"ࠪ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠩຖ") in args:
      i = args.index(bstack11l1l11_opy_ (u"ࠫ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠪທ"))
      args.pop(i)
      bstack11l1l11l_opy_ = args.pop(i)
    if bstack11l1l11_opy_ (u"ࠬ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸࠨຘ") in args:
      i = args.index(bstack11l1l11_opy_ (u"࠭࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࠩນ"))
      args.pop(i)
      bstack111llll1_opy_ = args.pop(i)
    if bstack11l1l11l_opy_ is not None:
      global bstack1lll1llll1_opy_
      bstack1lll1llll1_opy_ = bstack11l1l11l_opy_
    if bstack111llll1_opy_ is not None and int(bstack11ll1l111_opy_) < 0:
      bstack11ll1l111_opy_ = int(bstack111llll1_opy_)
    if cli.is_enabled(CONFIG):
      if cli.bstack1lll11l1l_opy_():
        bstack11l1l1l11_opy_.invoke(bstack1lllllll1_opy_.CONNECT, bstack1l1111l1l_opy_())
    bstack11ll11l111_opy_(bstack1ll1l11l11_opy_)
    run_cli(args)
    if bstack11l1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷࠫບ") in multiprocessing.current_process().__dict__.keys():
      for bstack1l1111ll1_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1ll1ll1l1_opy_.append(bstack1l1111ll1_opy_)
  elif bstack1l111ll11l_opy_ == bstack11l1l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨປ"):
    bstack1lll11l111_opy_ = bstack11111111_opy_(args, logger, CONFIG, bstack1l1111111_opy_)
    bstack1lll11l111_opy_.bstack111l111l1_opy_()
    bstack11lll1lll1_opy_()
    bstack11l1l11111_opy_ = True
    bstack1lll11lll_opy_ = bstack1lll11l111_opy_.bstack1l11lll11l_opy_()
    bstack1lll11l111_opy_.bstack1lllll1l11_opy_(bstack11lll11111_opy_)
    bstack1lll11l111_opy_.bstack1ll111ll1l_opy_()
    bstack111ll1111_opy_(bstack1l111ll11l_opy_, CONFIG, bstack1lll11l111_opy_.bstack1ll111lll_opy_())
    bstack111lll111l_opy_.end(EVENTS.bstack1ll111l1l1_opy_.value, EVENTS.bstack1ll111l1l1_opy_.value + bstack11l1l11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤຜ"), EVENTS.bstack1ll111l1l1_opy_.value + bstack11l1l11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣຝ"), status=True, failure=None, test_name=bstack1ll1ll11l1_opy_)
    bstack1l1l1ll1l1_opy_ = bstack1lll11l111_opy_.bstack1lllll111_opy_(bstack1l1lllll11_opy_, {
      bstack11l1l11_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫພ"): CONFIG,
      bstack11l1l11_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭ຟ"): bstack1l1l11ll11_opy_,
      bstack11l1l11_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨຠ"): bstack1l11ll1ll1_opy_,
      bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪມ"): bstack1l1111111_opy_,
      bstack11l1l11_opy_ (u"ࠨࡑ࡙ࡉࡗࡘࡉࡅࡇࡢࡐࡔࡇࡄࡠࡖࡈࡗ࡙ࡏࡎࡈࠩຢ"): bstack111ll1llll_opy_
    })
    if not bstack1llll1lll1_opy_:
      bstack1l1l1111ll_opy_ = bstack11ll1l1l1_opy_.bstack1l11l111ll_opy_(EVENTS.bstack1ll1l1l111_opy_.value)
    try:
      bstack11l111ll11_opy_, bstack1ll1ll1l1l_opy_ = map(list, zip(*bstack1l1l1ll1l1_opy_))
      bstack111ll11l11_opy_ = bstack11l111ll11_opy_[0]
      for status_code in bstack1ll1ll1l1l_opy_:
        if status_code != 0:
          bstack11l111l1_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack11l1l11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡡࡷࡧࠣࡩࡷࡸ࡯ࡳࡵࠣࡥࡳࡪࠠࡴࡶࡤࡸࡺࡹࠠࡤࡱࡧࡩ࠳ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࠽ࠤࢀࢃࠢຣ").format(str(e)))
  elif bstack1l111ll11l_opy_ == bstack11l1l11_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ຤"):
    try:
      from behave.__main__ import main as bstack1lll1lll1_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1ll1llll1l_opy_(e, bstack11l1l1l111_opy_)
    bstack11lll1lll1_opy_()
    bstack11l1l11111_opy_ = True
    bstack1ll1ll1111_opy_ = 1
    if bstack11l1l11_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫລ") in CONFIG:
      bstack1ll1ll1111_opy_ = CONFIG[bstack11l1l11_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ຦")]
    if bstack11l1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩວ") in CONFIG:
      bstack1llll1111_opy_ = int(bstack1ll1ll1111_opy_) * int(len(CONFIG[bstack11l1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪຨ")]))
    else:
      bstack1llll1111_opy_ = int(bstack1ll1ll1111_opy_)
    config = Configuration(args)
    bstack1l1lll11_opy_ = config.paths
    if len(bstack1l1lll11_opy_) == 0:
      import glob
      pattern = bstack11l1l11_opy_ (u"ࠨࠬ࠭࠳࠯࠴ࡦࡦࡣࡷࡹࡷ࡫ࠧຩ")
      bstack11l1ll11l_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack11l1ll11l_opy_)
      config = Configuration(args)
      bstack1l1lll11_opy_ = config.paths
    bstack111ll11111_opy_ = [os.path.normpath(item) for item in bstack1l1lll11_opy_]
    bstack1l11l11ll_opy_ = [os.path.normpath(item) for item in args]
    bstack111ll11ll_opy_ = [item for item in bstack1l11l11ll_opy_ if item not in bstack111ll11111_opy_]
    import platform as pf
    if pf.system().lower() == bstack11l1l11_opy_ (u"ࠩࡺ࡭ࡳࡪ࡯ࡸࡵࠪສ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack111ll11111_opy_ = [str(PurePosixPath(PureWindowsPath(bstack11ll1lll11_opy_)))
                    for bstack11ll1lll11_opy_ in bstack111ll11111_opy_]
    bstack1l111l1l11_opy_ = []
    for spec in bstack111ll11111_opy_:
      bstack11l1l1111l_opy_ = []
      bstack11l1l1111l_opy_ += bstack111ll11ll_opy_
      bstack11l1l1111l_opy_.append(spec)
      bstack1l111l1l11_opy_.append(bstack11l1l1111l_opy_)
    execution_items = []
    for bstack11l1l1111l_opy_ in bstack1l111l1l11_opy_:
      if bstack11l1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ຫ") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack11l1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧຬ")]):
          item = {}
          item[bstack11l1l11_opy_ (u"ࠬࡧࡲࡨࠩອ")] = bstack11l1l11_opy_ (u"࠭ࠠࠨຮ").join(bstack11l1l1111l_opy_)
          item[bstack11l1l11_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ຯ")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack11l1l11_opy_ (u"ࠨࡣࡵ࡫ࠬະ")] = bstack11l1l11_opy_ (u"ࠩࠣࠫັ").join(bstack11l1l1111l_opy_)
        item[bstack11l1l11_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩາ")] = 0
        execution_items.append(item)
    bstack1l1l111l11_opy_ = bstack111lll11ll_opy_(execution_items, bstack1llll1111_opy_)
    for execution_item in bstack1l1l111l11_opy_:
      bstack11ll11111_opy_ = []
      for item in execution_item:
        bstack11ll11111_opy_.append(bstack11lllllll_opy_(name=str(item[bstack11l1l11_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪຳ")]),
                                             target=bstack1l1111111l_opy_,
                                             args=(item[bstack11l1l11_opy_ (u"ࠬࡧࡲࡨࠩິ")],)))
      for t in bstack11ll11111_opy_:
        t.start()
      for t in bstack11ll11111_opy_:
        t.join()
  else:
    bstack11l1lll11l_opy_(bstack1lll11l1ll_opy_)
  if not bstack1llll1lll1_opy_:
    bstack1l111ll1l_opy_()
    if bstack1l1l1111ll_opy_:
      bstack11ll1l1l1_opy_.end(EVENTS.bstack1ll1l1l111_opy_.value, bstack1l1l1111ll_opy_ + bstack11l1l11_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨີ"), bstack1l1l1111ll_opy_ + bstack11l1l11_opy_ (u"ࠢ࠻ࡧࡱࡨࠧຶ"), status=True, failure=None, test_name=None)
  logger_utils.bstack1l1ll11l1_opy_()
def browserstack_initialize(bstack111llll11l_opy_=None):
  logger.info(bstack11l1l11_opy_ (u"ࠨࡔࡸࡲࡳ࡯࡮ࡨࠢࡖࡈࡐࠦࡷࡪࡶ࡫ࠤࡦࡸࡧࡴ࠼ࠣࠫື") + str(bstack111llll11l_opy_))
  run_on_browserstack(bstack111llll11l_opy_, None, True)
@measure(event_name=EVENTS.bstack1111llllll_opy_, stage=STAGE.bstack1l11l1l11l_opy_, bstack1l111l11l_opy_=bstack1ll1ll11l1_opy_)
def bstack1l111ll1l_opy_():
  global CONFIG
  global bstack1lll1ll1l1_opy_
  global bstack11l111l1_opy_
  global bstack1lll111l1_opy_
  global global_config
  bstack1ll11l1ll_opy_.bstack1llll1llll_opy_()
  if cli.is_running():
    bstack11l1l1l11_opy_.invoke(bstack1lllllll1_opy_.bstack1l111l1ll1_opy_)
  else:
    bstack11ll11l1l_opy_ = bstack1l1l11l11l_opy_.get_instance(config=CONFIG)
    bstack11ll11l1l_opy_.bstack11llll111l_opy_(CONFIG)
  hashed_id = None
  bstack1l1l1lll1_opy_ = None
  def bstack111l11ll1_opy_():
    try:
      if bstack1lll1ll1l1_opy_ == bstack11l1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵຸࠩ"):
        if not cli.is_enabled(CONFIG):
          TestHubHandler.stop()
      else:
        TestHubHandler.stop()
    except Exception as e:
      logger.debug(bstack11l1l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡶࡸࡴࡶࡰࡪࡰࡪࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࡻࡾࠤູ").format(e))
  def bstack1llll11l1l_opy_():
    try:
      if not cli.is_enabled(CONFIG):
        bstack1l111111_opy_.bstack1l1l1ll1ll_opy_()
    except Exception as e:
      logger.debug(bstack11l1l11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡴࡷ࡯࡮ࡵ࡫ࡱ࡫ࠥࡨࡵࡪ࡮ࡧࠤࡱ࡯࡮࡬࠼ࠣࡿࢂࠨ຺").format(e))
  def bstack1lll11ll1_opy_():
    nonlocal hashed_id, bstack1l1l1lll1_opy_
    try:
      if bstack11l1l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩົ") in CONFIG and str(CONFIG[bstack11l1l11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪຼ")]).lower() != bstack11l1l11_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ຽ"):
        hashed_id, bstack1l1l1lll1_opy_ = bstack1l1ll1lll1_opy_()
      else:
        hashed_id, bstack1l1l1lll1_opy_ = get_build_link()
    except Exception as e:
      logger.debug(bstack11l1l11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡤࡸ࡭ࡱࡪࠠ࡭࡫ࡱ࡯࠿ࠦࡻࡾࠤ຾").format(e))
  bstack1l1llll1ll_opy_ = threading.Thread(target=bstack111l11ll1_opy_)
  bstack1lll1lll11_opy_ = threading.Thread(target=bstack1llll11l1l_opy_)
  bstack1l1ll111_opy_ = threading.Thread(target=bstack1lll11ll1_opy_)
  threads = [bstack1l1llll1ll_opy_, bstack1lll1lll11_opy_, bstack1l1ll111_opy_]
  for thread in threads:
    try:
      thread.start()
    except Exception as e:
      logger.debug(bstack11l1l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡵࡷࡥࡷࡺࡩ࡯ࡩࠣࡸ࡭ࡸࡥࡢࡦࠣࡿࢂࡀࠠࡼࡿࠥ຿").format(thread.name, e))
  for thread in threads:
    try:
      thread.join()
    except Exception as e:
      logger.debug(bstack11l1l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡭ࡳ࡮ࡴࡩ࡯ࡩࠣࡸ࡭ࡸࡥࡢࡦࠣࡿࢂࡀࠠࡼࡿࠥເ").format(thread.name, e))
  bstack1l1l1l11l_opy_(hashed_id)
  logger.info(bstack11l1l11_opy_ (u"ࠫࡘࡊࡋࠡࡴࡸࡲࠥ࡫࡮ࡥࡧࡧࠤ࡫ࡵࡲࠡ࡫ࡧ࠾ࠬແ") + global_config.get_property(bstack11l1l11_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪࠧໂ"), bstack11l1l11_opy_ (u"࠭ࠧໃ")) + bstack11l1l11_opy_ (u"ࠧ࠭ࠢࡷࡩࡸࡺࡨࡶࡤࠣ࡭ࡩࡀࠠࠨໄ") + os.getenv(bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭໅"), bstack11l1l11_opy_ (u"ࠩࠪໆ")))
  if hashed_id is not None and bstack1ll111l11_opy_() != -1:
    sessions = bstack11l1l111_opy_(hashed_id)
    bstack11llll1l1l_opy_(sessions, bstack1l1l1lll1_opy_)
  if bstack1lll1ll1l1_opy_ == bstack11l1l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ໇") and bstack11l111l1_opy_ != 0:
    sys.exit(bstack11l111l1_opy_)
  if bstack1lll1ll1l1_opy_ == bstack11l1l11_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨ່ࠫ") and bstack1lll111l1_opy_ != 0:
    sys.exit(bstack1lll111l1_opy_)
def bstack1l1l1l11l_opy_(new_id):
    global bstack11lll1l1l_opy_
    bstack11lll1l1l_opy_ = new_id
def bstack1ll11l1111_opy_(bstack1llll11lll_opy_):
  if bstack1llll11lll_opy_:
    return bstack1llll11lll_opy_.capitalize()
  else:
    return bstack11l1l11_opy_ (u"້ࠬ࠭")
@measure(event_name=EVENTS.bstack1ll11l1lll_opy_, stage=STAGE.bstack1l11l1l11l_opy_, bstack1l111l11l_opy_=bstack1ll1ll11l1_opy_)
def bstack1ll11111l1_opy_(bstack11l11111_opy_):
  if bstack11l1l11_opy_ (u"࠭࡮ࡢ࡯ࡨ໊ࠫ") in bstack11l11111_opy_ and bstack11l11111_opy_[bstack11l1l11_opy_ (u"ࠧ࡯ࡣࡰࡩ໋ࠬ")] != bstack11l1l11_opy_ (u"ࠨࠩ໌"):
    return bstack11l11111_opy_[bstack11l1l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧໍ")]
  else:
    bstack1l111l11l_opy_ = bstack11l1l11_opy_ (u"ࠥࠦ໎")
    if bstack11l1l11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫ໏") in bstack11l11111_opy_ and bstack11l11111_opy_[bstack11l1l11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬ໐")] != None:
      bstack1l111l11l_opy_ += bstack11l11111_opy_[bstack11l1l11_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭໑")] + bstack11l1l11_opy_ (u"ࠢ࠭ࠢࠥ໒")
      if bstack11l11111_opy_[bstack11l1l11_opy_ (u"ࠨࡱࡶࠫ໓")] == bstack11l1l11_opy_ (u"ࠤ࡬ࡳࡸࠨ໔"):
        bstack1l111l11l_opy_ += bstack11l1l11_opy_ (u"ࠥ࡭ࡔ࡙ࠠࠣ໕")
      bstack1l111l11l_opy_ += (bstack11l11111_opy_[bstack11l1l11_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ໖")] or bstack11l1l11_opy_ (u"ࠬ࠭໗"))
      return bstack1l111l11l_opy_
    else:
      bstack1l111l11l_opy_ += bstack1ll11l1111_opy_(bstack11l11111_opy_[bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ໘")]) + bstack11l1l11_opy_ (u"ࠢࠡࠤ໙") + (
              bstack11l11111_opy_[bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪ໚")] or bstack11l1l11_opy_ (u"ࠩࠪ໛")) + bstack11l1l11_opy_ (u"ࠥ࠰ࠥࠨໜ")
      if bstack11l11111_opy_[bstack11l1l11_opy_ (u"ࠫࡴࡹࠧໝ")] == bstack11l1l11_opy_ (u"ࠧ࡝ࡩ࡯ࡦࡲࡻࡸࠨໞ"):
        bstack1l111l11l_opy_ += bstack11l1l11_opy_ (u"ࠨࡗࡪࡰࠣࠦໟ")
      bstack1l111l11l_opy_ += bstack11l11111_opy_[bstack11l1l11_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫ໠")] or bstack11l1l11_opy_ (u"ࠨࠩ໡")
      return bstack1l111l11l_opy_
@measure(event_name=EVENTS.bstack1111l1l11_opy_, stage=STAGE.bstack1l11l1l11l_opy_, bstack1l111l11l_opy_=bstack1ll1ll11l1_opy_)
def bstack1lllll1l1_opy_(bstack11ll111l11_opy_):
  if bstack11ll111l11_opy_ == bstack11l1l11_opy_ (u"ࠤࡧࡳࡳ࡫ࠢ໢"):
    return bstack11l1l11_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿࡭ࡲࡦࡧࡱ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧ࡭ࡲࡦࡧࡱࠦࡃࡉ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭໣")
  elif bstack11ll111l11_opy_ == bstack11l1l11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ໤"):
    return bstack11l1l11_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡳࡧࡧ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡸࡥࡥࠤࡁࡊࡦ࡯࡬ࡦࡦ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨ໥")
  elif bstack11ll111l11_opy_ == bstack11l1l11_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ໦"):
    return bstack11l1l11_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡪࡶࡪ࡫࡮࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡪࡶࡪ࡫࡮ࠣࡀࡓࡥࡸࡹࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ໧")
  elif bstack11ll111l11_opy_ == bstack11l1l11_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢ໨"):
    return bstack11l1l11_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡷ࡫ࡤ࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡵࡩࡩࠨ࠾ࡆࡴࡵࡳࡷࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫ໩")
  elif bstack11ll111l11_opy_ == bstack11l1l11_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࠦ໪"):
    return bstack11l1l11_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࠣࡦࡧࡤ࠷࠷࠼࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࠥࡨࡩࡦ࠹࠲࠷ࠤࡁࡘ࡮ࡳࡥࡰࡷࡷࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩ໫")
  elif bstack11ll111l11_opy_ == bstack11l1l11_opy_ (u"ࠧࡸࡵ࡯ࡰ࡬ࡲ࡬ࠨ໬"):
    return bstack11l1l11_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡤ࡯ࡥࡨࡱ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡤ࡯ࡥࡨࡱࠢ࠿ࡔࡸࡲࡳ࡯࡮ࡨ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ໭")
  else:
    return bstack11l1l11_opy_ (u"ࠧ࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡦࡱࡧࡣ࡬࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡦࡱࡧࡣ࡬ࠤࡁࠫ໮") + bstack1ll11l1111_opy_(
      bstack11ll111l11_opy_) + bstack11l1l11_opy_ (u"ࠨ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ໯")
def bstack1ll11lll11_opy_(session):
  return bstack11l1l11_opy_ (u"ࠩ࠿ࡸࡷࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡲࡰࡹࠥࡂࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠦࡳࡦࡵࡶ࡭ࡴࡴ࠭࡯ࡣࡰࡩࠧࡄ࠼ࡢࠢ࡫ࡶࡪ࡬࠽ࠣࡽࢀࠦࠥࡺࡡࡳࡩࡨࡸࡂࠨ࡟ࡣ࡮ࡤࡲࡰࠨ࠾ࡼࡿ࠿࠳ࡦࡄ࠼࠰ࡶࡧࡂࢀࢃࡻࡾ࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀ࠴ࡺࡲ࠿ࠩ໰").format(
    session[bstack11l1l11_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥࡢࡹࡷࡲࠧ໱")], bstack1ll11111l1_opy_(session), bstack1lllll1l1_opy_(session[bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡷࡹࡧࡴࡶࡵࠪ໲")]),
    bstack1lllll1l1_opy_(session[bstack11l1l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ໳")]),
    bstack1ll11l1111_opy_(session[bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ໴")] or session[bstack11l1l11_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ໵")] or bstack11l1l11_opy_ (u"ࠨࠩ໶")) + bstack11l1l11_opy_ (u"ࠤࠣࠦ໷") + (session[bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ໸")] or bstack11l1l11_opy_ (u"ࠫࠬ໹")),
    session[bstack11l1l11_opy_ (u"ࠬࡵࡳࠨ໺")] + bstack11l1l11_opy_ (u"ࠨࠠࠣ໻") + session[bstack11l1l11_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫ໼")], session[bstack11l1l11_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪ໽")] or bstack11l1l11_opy_ (u"ࠩࠪ໾"),
    session[bstack11l1l11_opy_ (u"ࠪࡧࡷ࡫ࡡࡵࡧࡧࡣࡦࡺࠧ໿")] if session[bstack11l1l11_opy_ (u"ࠫࡨࡸࡥࡢࡶࡨࡨࡤࡧࡴࠨༀ")] else bstack11l1l11_opy_ (u"ࠬ࠭༁"))
@measure(event_name=EVENTS.bstack1llll1l1l_opy_, stage=STAGE.bstack1l11l1l11l_opy_, bstack1l111l11l_opy_=bstack1ll1ll11l1_opy_)
def bstack11llll1l1l_opy_(sessions, bstack1l1l1lll1_opy_):
  try:
    bstack1l1ll111l_opy_ = bstack11l1l11_opy_ (u"ࠨࠢ༂")
    if not os.path.exists(bstack1ll1ll111l_opy_):
      os.mkdir(bstack1ll1ll111l_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11l1l11_opy_ (u"ࠧࡢࡵࡶࡩࡹࡹ࠯ࡳࡧࡳࡳࡷࡺ࠮ࡩࡶࡰࡰࠬ༃")), bstack11l1l11_opy_ (u"ࠨࡴࠪ༄")) as f:
      bstack1l1ll111l_opy_ = f.read()
    bstack1l1ll111l_opy_ = bstack1l1ll111l_opy_.replace(bstack11l1l11_opy_ (u"ࠩࡾࠩࡗࡋࡓࡖࡎࡗࡗࡤࡉࡏࡖࡐࡗࠩࢂ࠭༅"), str(len(sessions)))
    bstack1l1ll111l_opy_ = bstack1l1ll111l_opy_.replace(bstack11l1l11_opy_ (u"ࠪࡿࠪࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠦࡿࠪ༆"), bstack1l1l1lll1_opy_)
    bstack1l1ll111l_opy_ = bstack1l1ll111l_opy_.replace(bstack11l1l11_opy_ (u"ࠫࢀࠫࡂࡖࡋࡏࡈࡤࡔࡁࡎࡇࠨࢁࠬ༇"),
                                              sessions[0].get(bstack11l1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣࡳࡧ࡭ࡦࠩ༈")) if sessions[0] else bstack11l1l11_opy_ (u"࠭ࠧ༉"))
    with open(os.path.join(bstack1ll1ll111l_opy_, bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡲࡦࡲࡲࡶࡹ࠴ࡨࡵ࡯࡯ࠫ༊")), bstack11l1l11_opy_ (u"ࠨࡹࠪ་")) as stream:
      stream.write(bstack1l1ll111l_opy_.split(bstack11l1l11_opy_ (u"ࠩࡾࠩࡘࡋࡓࡔࡋࡒࡒࡘࡥࡄࡂࡖࡄࠩࢂ࠭༌"))[0])
      for session in sessions:
        stream.write(bstack1ll11lll11_opy_(session))
      stream.write(bstack1l1ll111l_opy_.split(bstack11l1l11_opy_ (u"ࠪࡿ࡙ࠪࡅࡔࡕࡌࡓࡓ࡙࡟ࡅࡃࡗࡅࠪࢃࠧ།"))[1])
    logger.info(bstack11l1l11_opy_ (u"ࠫࡌ࡫࡮ࡦࡴࡤࡸࡪࡪࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡢࡶ࡫࡯ࡨࠥࡧࡲࡵ࡫ࡩࡥࡨࡺࡳࠡࡣࡷࠤࢀࢃࠧ༎").format(bstack1ll1ll111l_opy_));
  except Exception as e:
    logger.debug(bstack111l111ll_opy_.format(str(e)))
def bstack11l1l111_opy_(hashed_id):
  global CONFIG
  try:
    bstack111l11l1l1_opy_ = datetime.datetime.now()
    host = bstack11l1l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡱ࡫࠰ࡧࡱࡵࡵࡥ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬ༏") if bstack11l1l11_opy_ (u"࠭ࡡࡱࡲࠪ༐") in CONFIG else bstack11l1l11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨ༑")
    user = CONFIG[bstack11l1l11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ༒")]
    key = CONFIG[bstack11l1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ༓")]
    bstack1ll1l111ll_opy_ = bstack11l1l11_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩ༔") if bstack11l1l11_opy_ (u"ࠫࡦࡶࡰࠨ༕") in CONFIG else (bstack11l1l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩ༖") if CONFIG.get(bstack11l1l11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪ༗")) else bstack11l1l11_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦ༘ࠩ"))
    host = bstack1ll11l1l11_opy_(cli.config, [bstack11l1l11_opy_ (u"ࠣࡣࡳ࡭ࡸࠨ༙"), bstack11l1l11_opy_ (u"ࠤࡤࡴࡵࡇࡵࡵࡱࡰࡥࡹ࡫ࠢ༚"), bstack11l1l11_opy_ (u"ࠥࡥࡵ࡯ࠢ༛")], host) if bstack11l1l11_opy_ (u"ࠫࡦࡶࡰࠨ༜") in CONFIG else bstack1ll11l1l11_opy_(cli.config, [bstack11l1l11_opy_ (u"ࠧࡧࡰࡪࡵࠥ༝"), bstack11l1l11_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥࠣ༞"), bstack11l1l11_opy_ (u"ࠢࡢࡲ࡬ࠦ༟")], host)
    url = bstack11l1l11_opy_ (u"ࠨࡽࢀ࠳ࢀࢃ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡷࡪࡹࡳࡪࡱࡱࡷ࠳ࡰࡳࡰࡰࠪ༠").format(host, bstack1ll1l111ll_opy_, hashed_id)
    headers = {
      bstack11l1l11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨ༡"): bstack11l1l11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭༢"),
    }
    proxies = bstack1lll1l11l1_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies, auth=(user, key))
    if response.json():
      cli.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼ࡪࡩࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࡠ࡮࡬ࡷࡹࠨ༣"), datetime.datetime.now() - bstack111l11l1l1_opy_)
      return list(map(lambda session: session[bstack11l1l11_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡩࡸࡹࡩࡰࡰࠪ༤")], response.json()))
  except Exception as e:
    logger.debug(bstack111l11l1ll_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack111llll11_opy_, stage=STAGE.bstack1l11l1l11l_opy_, bstack1l111l11l_opy_=bstack1ll1ll11l1_opy_)
def get_build_link():
  global CONFIG
  global bstack11lll1l1l_opy_
  try:
    if bstack11l1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ༥") in CONFIG:
      bstack111l11l1l1_opy_ = datetime.datetime.now()
      host = bstack11l1l11_opy_ (u"ࠧࡢࡲ࡬࠱ࡨࡲ࡯ࡶࡦࠪ༦") if bstack11l1l11_opy_ (u"ࠨࡣࡳࡴࠬ༧") in CONFIG else bstack11l1l11_opy_ (u"ࠩࡤࡴ࡮࠭༨")
      user = CONFIG[bstack11l1l11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ༩")]
      key = CONFIG[bstack11l1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ༪")]
      bstack1ll1l111ll_opy_ = bstack11l1l11_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ༫") if bstack11l1l11_opy_ (u"࠭ࡡࡱࡲࠪ༬") in CONFIG else bstack11l1l11_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩ༭")
      url = bstack11l1l11_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡾࢁ࠿ࢁࡽࡁࡽࢀ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡼࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠱࡮ࡸࡵ࡮ࠨ༮").format(user, key, host, bstack1ll1l111ll_opy_)
      if cli.is_enabled(CONFIG):
        bstack1l1l1lll1_opy_, hashed_id = cli.bstack11lll11lll_opy_()
        logger.info(bstack11l1ll11ll_opy_.format(bstack1l1l1lll1_opy_))
        return [hashed_id, bstack1l1l1lll1_opy_]
      else:
        headers = {
          bstack11l1l11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨ༯"): bstack11l1l11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭༰"),
        }
        if bstack11l1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭༱") in CONFIG:
          params = {bstack11l1l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ༲"): CONFIG[bstack11l1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ༳")], bstack11l1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ༴"): CONFIG[bstack11l1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴ༵ࠪ")]}
        else:
          params = {bstack11l1l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ༶"): CONFIG[bstack11l1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ༷࠭")]}
        proxies = bstack1lll1l11l1_opy_(CONFIG, url)
        response = requests.get(url, params=params, headers=headers, proxies=proxies)
        if response.json():
          bstack1l11ll1l11_opy_ = response.json()[0][bstack11l1l11_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡤࡸ࡭ࡱࡪࠧ༸")]
          if bstack1l11ll1l11_opy_:
            bstack1l1l1lll1_opy_ = bstack1l11ll1l11_opy_[bstack11l1l11_opy_ (u"ࠬࡶࡵࡣ࡮࡬ࡧࡤࡻࡲ࡭༹ࠩ")].split(bstack11l1l11_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨ࠳ࡢࡶ࡫࡯ࡨࠬ༺"))[0] + bstack11l1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡹ࠯ࠨ༻") + bstack1l11ll1l11_opy_[
              bstack11l1l11_opy_ (u"ࠨࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ༼")]
            logger.info(bstack11l1ll11ll_opy_.format(bstack1l1l1lll1_opy_))
            bstack11lll1l1l_opy_ = bstack1l11ll1l11_opy_[bstack11l1l11_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ༽")]
            bstack1ll1l1lll_opy_ = CONFIG[bstack11l1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭༾")]
            if bstack11l1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭༿") in CONFIG:
              bstack1ll1l1lll_opy_ += bstack11l1l11_opy_ (u"ࠬࠦࠧཀ") + CONFIG[bstack11l1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨཁ")]
            if bstack1ll1l1lll_opy_ != bstack1l11ll1l11_opy_[bstack11l1l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬག")]:
              logger.debug(bstack11ll111ll1_opy_.format(bstack1l11ll1l11_opy_[bstack11l1l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭གྷ")], bstack1ll1l1lll_opy_))
            cli.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺ࡨࡧࡷࡣࡧࡻࡩ࡭ࡦࡢࡰ࡮ࡴ࡫ࠣང"), datetime.datetime.now() - bstack111l11l1l1_opy_)
            return [bstack1l11ll1l11_opy_[bstack11l1l11_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ཅ")], bstack1l1l1lll1_opy_]
    else:
      logger.warning(bstack1l1l1ll111_opy_)
  except Exception as e:
    logger.debug(bstack1l111llll_opy_.format(str(e)))
  return [None, None]
def bstack11llll1ll1_opy_(url, bstack1ll1l1lll1_opy_=False):
  global CONFIG
  global bstack11ll1l11l1_opy_
  if not bstack11ll1l11l1_opy_:
    hostname = bstack11l1l111ll_opy_(url)
    is_private = bstack1111l1l1_opy_(hostname)
    if (bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨཆ") in CONFIG and not bstack1lll1l111_opy_(CONFIG[bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩཇ")])) and (is_private or bstack1ll1l1lll1_opy_):
      bstack11ll1l11l1_opy_ = hostname
def bstack11l1l111ll_opy_(url):
  return urlparse(url).hostname
def bstack1111l1l1_opy_(hostname):
  for bstack111llll1ll_opy_ in bstack1ll11lll1l_opy_:
    regex = re.compile(bstack111llll1ll_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack11l1l111l_opy_(bstack1l1ll1lll_opy_):
  return True if bstack1l1ll1lll_opy_ in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack1l11ll11_opy_, stage=STAGE.bstack1l11l1l11l_opy_, bstack1l111l11l_opy_=bstack1ll1ll11l1_opy_)
def getAccessibilityResults(driver):
  global CONFIG
  global bstack11ll1l111_opy_
  bstack1llll11l_opy_ = not (bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ཈"), None) and bstack11llll11l1_opy_(
          threading.current_thread(), bstack11l1l11_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ཉ"), None))
  bstack1llll1l111_opy_ = getattr(driver, bstack11l1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨཊ"), None) != True
  bstack1l11l11111_opy_ = bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩཋ"), None) and bstack11llll11l1_opy_(
          threading.current_thread(), bstack11l1l11_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬཌ"), None)
  if bstack1l11l11111_opy_:
    if not bstack11l1ll111_opy_():
      logger.warning(bstack11l1l11_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡶࡰࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡄࡴࡵࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹ࠮ࠣཌྷ"))
      return {}
    logger.debug(bstack11l1l11_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡴࡨࡷࡺࡲࡴࡴࠩཎ"))
    logger.debug(perform_scan(driver, driver_command=bstack11l1l11_opy_ (u"࠭ࡥࡹࡧࡦࡹࡹ࡫ࡓࡤࡴ࡬ࡴࡹ࠭ཏ")))
    results = bstack11ll11l11l_opy_(bstack11l1l11_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡳࠣཐ"))
    if results is not None and results.get(bstack11l1l11_opy_ (u"ࠣ࡫ࡶࡷࡺ࡫ࡳࠣད")) is not None:
        return results[bstack11l1l11_opy_ (u"ࠤ࡬ࡷࡸࡻࡥࡴࠤདྷ")]
    logger.error(bstack11l1l11_opy_ (u"ࠥࡒࡴࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡒࡦࡵࡸࡰࡹࡹࠠࡸࡧࡵࡩࠥ࡬࡯ࡶࡰࡧ࠲ࠧན"))
    return []
  if not bstack1l111ll111_opy_.bstack111ll1111l_opy_(CONFIG, bstack11ll1l111_opy_) or (bstack1llll1l111_opy_ and bstack1llll11l_opy_):
    logger.warning(bstack11l1l11_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡪࡺࡲࡪࡧࡹࡩࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸ࠴ࠢཔ"))
    return {}
  try:
    logger.debug(bstack11l1l11_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡴࡨࡷࡺࡲࡴࡴࠩཕ"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack111llllll1_opy_.bstack1llll11111_opy_)
    return results
  except Exception:
    logger.error(bstack11l1l11_opy_ (u"ࠨࡎࡰࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡻࡪࡸࡥࠡࡨࡲࡹࡳࡪ࠮ࠣབ"))
    return {}
@measure(event_name=EVENTS.bstack11l11l11l1_opy_, stage=STAGE.bstack1l11l1l11l_opy_, bstack1l111l11l_opy_=bstack1ll1ll11l1_opy_)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack11ll1l111_opy_
  bstack1llll11l_opy_ = not (bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫབྷ"), None) and bstack11llll11l1_opy_(
          threading.current_thread(), bstack11l1l11_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧམ"), None))
  bstack1llll1l111_opy_ = getattr(driver, bstack11l1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩཙ"), None) != True
  bstack1l11l11111_opy_ = bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪཚ"), None) and bstack11llll11l1_opy_(
          threading.current_thread(), bstack11l1l11_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ཛ"), None)
  if bstack1l11l11111_opy_:
    if not bstack11l1ll111_opy_():
      logger.warning(bstack11l1l11_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡰࡱࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡅࡵࡶࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡵࡸࡱࡲࡧࡲࡺ࠰ࠥཛྷ"))
      return {}
    logger.debug(bstack11l1l11_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡷࡺࡳ࡭ࡢࡴࡼࠫཝ"))
    logger.debug(perform_scan(driver, driver_command=bstack11l1l11_opy_ (u"ࠧࡦࡺࡨࡧࡺࡺࡥࡔࡥࡵ࡭ࡵࡺࠧཞ")))
    results = bstack11ll11l11l_opy_(bstack11l1l11_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࡔࡷࡰࡱࡦࡸࡹࠣཟ"))
    if results is not None and results.get(bstack11l1l11_opy_ (u"ࠤࡶࡹࡲࡳࡡࡳࡻࠥའ")) is not None:
        return results[bstack11l1l11_opy_ (u"ࠥࡷࡺࡳ࡭ࡢࡴࡼࠦཡ")]
    logger.error(bstack11l1l11_opy_ (u"ࠦࡓࡵࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡓࡧࡶࡹࡱࡺࡳࠡࡕࡸࡱࡲࡧࡲࡺࠢࡺࡥࡸࠦࡦࡰࡷࡱࡨ࠳ࠨར"))
    return {}
  if not bstack1l111ll111_opy_.bstack111ll1111l_opy_(CONFIG, bstack11ll1l111_opy_) or (bstack1llll1l111_opy_ and bstack1llll11l_opy_):
    logger.warning(bstack11l1l11_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡴࡷࡰࡱࡦࡸࡹ࠯ࠤལ"))
    return {}
  try:
    logger.debug(bstack11l1l11_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡷࡺࡳ࡭ࡢࡴࡼࠫཤ"))
    logger.debug(perform_scan(driver))
    bstack1l1l1lllll_opy_ = driver.execute_async_script(bstack111llllll1_opy_.bstack11l1111lll_opy_)
    return bstack1l1l1lllll_opy_
  except Exception:
    logger.error(bstack11l1l11_opy_ (u"ࠢࡏࡱࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡺࡳ࡭ࡢࡴࡼࠤࡼࡧࡳࠡࡨࡲࡹࡳࡪ࠮ࠣཥ"))
    return {}
def bstack11l1ll111_opy_():
  global CONFIG
  global bstack11ll1l111_opy_
  bstack111l1l1lll_opy_ = bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨས"), None) and bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫཧ"), None)
  if not bstack1l111ll111_opy_.bstack111ll1111l_opy_(CONFIG, bstack11ll1l111_opy_) or not bstack111l1l1lll_opy_:
        logger.warning(bstack11l1l11_opy_ (u"ࠥࡒࡴࡺࠠࡢࡰࠣࡅࡵࡶࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࠡࡴࡨࡷࡺࡲࡴࡴ࠰ࠥཨ"))
        return False
  return True
def bstack11ll11l11l_opy_(result_type):
    bstack111ll111ll_opy_ = TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack1l111111_opy_.current_hook_uuid()
    with ThreadPoolExecutor() as executor:
        future = executor.submit(bstack11l111lll_opy_(bstack111ll111ll_opy_, result_type))
        try:
            return future.result(timeout=bstack11l11l1l11_opy_)
        except TimeoutError:
            logger.error(bstack11l1l11_opy_ (u"࡙ࠦ࡯࡭ࡦࡱࡸࡸࠥࡧࡦࡵࡧࡵࠤࢀࢃࡳࠡࡹ࡫࡭ࡱ࡫ࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡕࡩࡸࡻ࡬ࡵࡵࠥཀྵ").format(bstack11l11l1l11_opy_))
        except Exception as ex:
            logger.debug(bstack11l1l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡷ࡫ࡴࡳ࡫ࡨࡺ࡮ࡴࡧࠡࡃࡳࡴࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡾࢁ࠳ࠦࡅࡳࡴࡲࡶࠥ࠳ࠠࡼࡿࠥཪ").format(result_type, str(ex)))
    return {}
@measure(event_name=EVENTS.bstack1l11llll_opy_, stage=STAGE.bstack1l11l1l11l_opy_, bstack1l111l11l_opy_=bstack1ll1ll11l1_opy_)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack11ll1l111_opy_
  bstack1llll11l_opy_ = not (bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪཫ"), None) and bstack11llll11l1_opy_(
          threading.current_thread(), bstack11l1l11_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ཬ"), None))
  bstack1l1l1ll1l_opy_ = not (bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ཭"), None) and bstack11llll11l1_opy_(
          threading.current_thread(), bstack11l1l11_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ཮"), None))
  bstack1llll1l111_opy_ = getattr(driver, bstack11l1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪ཯"), None) != True
  if not bstack1l111ll111_opy_.bstack111ll1111l_opy_(CONFIG, bstack11ll1l111_opy_) or (bstack1llll1l111_opy_ and bstack1llll11l_opy_ and bstack1l1l1ll1l_opy_):
    logger.warning(bstack11l1l11_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡺࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡥࡤࡲ࠳ࠨ཰"))
    return {}
  try:
    bstack1l111ll1ll_opy_ = bstack11l1l11_opy_ (u"ࠬࡧࡰࡱཱࠩ") in CONFIG and CONFIG.get(bstack11l1l11_opy_ (u"࠭ࡡࡱࡲིࠪ"), bstack11l1l11_opy_ (u"ࠧࠨཱི"))
    session_id = getattr(driver, bstack11l1l11_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨུࠬ"), None)
    if not session_id:
      logger.warning(bstack11l1l11_opy_ (u"ࠤࡑࡳࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡉࡅࠢࡩࡳࡺࡴࡤࠡࡨࡲࡶࠥࡪࡲࡪࡸࡨࡶཱུࠧ"))
      return {bstack11l1l11_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤྲྀ"): bstack11l1l11_opy_ (u"ࠦࡓࡵࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡋࡇࠤ࡫ࡵࡵ࡯ࡦࠥཷ")}
    if bstack1l111ll1ll_opy_:
      try:
        bstack111lll111_opy_ = {
              bstack11l1l11_opy_ (u"ࠬࡺࡨࡋࡹࡷࡘࡴࡱࡥ࡯ࠩླྀ"): os.environ.get(bstack11l1l11_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫཹ"), os.environ.get(bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗེࠫ"), bstack11l1l11_opy_ (u"ࠨཻࠩ"))),
              bstack11l1l11_opy_ (u"ࠩࡷ࡬࡙࡫ࡳࡵࡔࡸࡲ࡚ࡻࡩࡥོࠩ"): TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack1l111111_opy_.current_hook_uuid(),
              bstack11l1l11_opy_ (u"ࠪࡥࡺࡺࡨࡉࡧࡤࡨࡪࡸཽࠧ"): os.environ.get(bstack11l1l11_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩཾ")),
              bstack11l1l11_opy_ (u"ࠬࡹࡣࡢࡰࡗ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬཿ"): str(int(datetime.datetime.now().timestamp() * 1000)),
              bstack11l1l11_opy_ (u"࠭ࡴࡩࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧྀࠫ"): os.environ.get(bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈཱྀࠬ"), bstack11l1l11_opy_ (u"ࠨࠩྂ")),
              bstack11l1l11_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࠩྃ"): kwargs.get(bstack11l1l11_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࡢࡧࡴࡳ࡭ࡢࡰࡧ྄ࠫ"), None) or bstack11l1l11_opy_ (u"ࠫࠬ྅")
          }
        if not hasattr(thread_local, bstack11l1l11_opy_ (u"ࠬࡨࡡࡴࡧࡢࡥࡵࡶ࡟ࡢ࠳࠴ࡽࡤࡹࡣࡳ࡫ࡳࡸࠬ྆")):
            scripts = {bstack11l1l11_opy_ (u"࠭ࡳࡤࡣࡱࠫ྇"): bstack111llllll1_opy_.perform_scan}
            thread_local.base_app_a11y_script = scripts
        bstack111l11l11l_opy_ = copy.deepcopy(thread_local.base_app_a11y_script)
        bstack111l11l11l_opy_[bstack11l1l11_opy_ (u"ࠧࡴࡥࡤࡲࠬྈ")] = bstack111l11l11l_opy_[bstack11l1l11_opy_ (u"ࠨࡵࡦࡥࡳ࠭ྉ")] % json.dumps(bstack111lll111_opy_)
        bstack111llllll1_opy_.bstack11l11l1ll_opy_(bstack111l11l11l_opy_)
        bstack111llllll1_opy_.store()
        bstack1l1llll11l_opy_ = driver.execute_script(bstack111llllll1_opy_.perform_scan)
      except Exception as bstack1l1111l11_opy_:
        logger.info(bstack11l1l11_opy_ (u"ࠤࡄࡴࡵ࡯ࡵ࡮ࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡧࡦࡴࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࠤྊ") + str(bstack1l1111l11_opy_))
        bstack1l1llll11l_opy_ = {bstack11l1l11_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤྋ"): str(bstack1l1111l11_opy_)}
    else:
      bstack1l1llll11l_opy_ = driver.execute_async_script(bstack111llllll1_opy_.perform_scan, {bstack11l1l11_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࠫྌ"): kwargs.get(bstack11l1l11_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࡤࡩ࡯࡮࡯ࡤࡲࡩ࠭ྍ"), None) or bstack11l1l11_opy_ (u"࠭ࠧྎ")})
    return bstack1l1llll11l_opy_
  except Exception as err:
    logger.error(bstack11l1l11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡶࡺࡴࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡥࡤࡲ࠳ࠦࡻࡾࠤྏ").format(str(err)))
    return {}