# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
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
from browserstack_sdk.bstack11lll1l1l1_opy_ import bstack111l1ll111_opy_
from browserstack_sdk.bstack11ll11l1l1_opy_ import *
import time
import requests
from bstack_utils.constants import EVENTS, STAGE, bstack1l1ll11lll_opy_
from bstack_utils.messages import bstack1lll111ll_opy_, bstack1l11lll1ll_opy_, bstack111l1ll11l_opy_, bstack11111111l_opy_, bstack1ll1l11l1l_opy_, bstack11llll1l_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack111llll1ll_opy_ import get_logger
from bstack_utils.helper import bstack1l11ll11l1_opy_
from browserstack_sdk.bstack1ll11l111l_opy_ import bstack11111111_opy_
logger = get_logger(__name__)
def bstack111lll11ll_opy_():
  global CONFIG
  headers = {
        bstack1l1111_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack1l1111_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1l11ll11l1_opy_(CONFIG, bstack1l1ll11lll_opy_)
  try:
    response = requests.get(bstack1l1ll11lll_opy_, headers=headers, proxies=proxies, timeout=2)
    if response.json():
      bstack11lll1111_opy_ = response.json()[bstack1l1111_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1lll111ll_opy_.format(response.json()))
      return bstack11lll1111_opy_
    else:
      logger.debug(bstack1l11lll1ll_opy_.format(bstack1l1111_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack1l11lll1ll_opy_.format(e))
def bstack1l11lll1l_opy_(hub_url):
  global CONFIG
  url = bstack1l1111_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack1l1111_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack1l1111_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack1l1111_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1l11ll11l1_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=(0.5, 1.0))
    latency = time.perf_counter() - start_time
    logger.debug(bstack111l1ll11l_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack11111111l_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack11lllll111_opy_, stage=STAGE.bstack1111lll11_opy_)
def bstack1111l1l1_opy_():
  try:
    global bstack1l1lll1l11_opy_
    global CONFIG
    if bstack1l1111_opy_ (u"ࠫ࡭ࡻࡢࡓࡧࡪ࡭ࡴࡴࠧࡾ") in CONFIG and CONFIG[bstack1l1111_opy_ (u"ࠬ࡮ࡵࡣࡔࡨ࡫࡮ࡵ࡮ࠨࡿ")]:
      from bstack_utils.constants import bstack111l111l1_opy_
      bstack11l1ll1111_opy_ = CONFIG[bstack1l1111_opy_ (u"࠭ࡨࡶࡤࡕࡩ࡬࡯࡯࡯ࠩࢀ")]
      if bstack11l1ll1111_opy_ in bstack111l111l1_opy_:
        bstack1l1lll1l11_opy_ = bstack111l111l1_opy_[bstack11l1ll1111_opy_]
        logger.debug(bstack1ll1l11l1l_opy_.format(bstack1l1lll1l11_opy_))
        return
      else:
        logger.debug(bstack1l1111_opy_ (u"ࠢࡉࡷࡥࠤࡰ࡫ࡹࠡࠩࡾࢁࠬࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࡎࡕࡃࡡࡘࡖࡑࡥࡍࡂࡒ࠯ࠤ࡫ࡧ࡬࡭࡫ࡱ࡫ࠥࡨࡡࡤ࡭ࠣࡸࡴࠦ࡯ࡱࡶ࡬ࡱࡦࡲࠠࡩࡷࡥࠤࡩ࡫ࡴࡦࡥࡷ࡭ࡴࡴࠢࢁ").format(bstack11l1ll1111_opy_))
    bstack11lll1111_opy_ = bstack111lll11ll_opy_()
    from concurrent.futures import ThreadPoolExecutor, as_completed
    if bstack11lll1111_opy_:
        with ThreadPoolExecutor(max_workers=len(bstack11lll1111_opy_)) as executor:
            bstack1l1ll1lll_opy_ = {executor.submit(bstack1l11lll1l_opy_, bstack1l1ll1111_opy_): bstack1l1ll1111_opy_ for bstack1l1ll1111_opy_ in bstack11lll1111_opy_}
            for future in as_completed(bstack1l1ll1lll_opy_):
                result = future.result()
                if result and result.get(bstack1l1111_opy_ (u"ࠨ࡮ࡤࡸࡪࡴࡣࡺࠩࢂ")) is not None:
                    bstack1l1lll1l11_opy_ = result[bstack1l1111_opy_ (u"ࠩ࡫ࡹࡧࡥࡵࡳ࡮ࠪࢃ")]
                    logger.debug(bstack1ll1l11l1l_opy_.format(bstack1l1lll1l11_opy_))
                    return
        bstack1l1lll1l11_opy_ = bstack11lll1111_opy_[0]
        logger.debug(bstack1ll1l11l1l_opy_.format(bstack1l1lll1l11_opy_))
        return
  except Exception as e:
    logger.debug(bstack11llll1l_opy_.format(e))
from browserstack_sdk.bstack111l1l1ll1_opy_ import *
from browserstack_sdk.bstack1ll11l111l_opy_ import *
from browserstack_sdk.bstack11ll11ll1_opy_ import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.bstack111llll1ll_opy_ import get_logger
from bstack_utils.measure import measure
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack1ll111ll11_opy_, stage=STAGE.bstack1111lll11_opy_)
def bstack1lll111l1l_opy_():
    global bstack1l1lll1l11_opy_
    try:
        bstack1ll11111l1_opy_ = bstack1lllll1ll1_opy_()
        bstack1lllll11l_opy_(bstack1ll11111l1_opy_)
        hub_url = bstack1ll11111l1_opy_.get(bstack1l1111_opy_ (u"ࠥࡹࡷࡲࠢࢄ"), bstack1l1111_opy_ (u"ࠦࠧࢅ"))
        if hub_url.endswith(bstack1l1111_opy_ (u"ࠬ࠵ࡷࡥ࠱࡫ࡹࡧ࠭ࢆ")):
            hub_url = hub_url.rsplit(bstack1l1111_opy_ (u"࠭࠯ࡸࡦ࠲࡬ࡺࡨࠧࢇ"), 1)[0]
        if hub_url.startswith(bstack1l1111_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࠨ࢈")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack1l1111_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࠪࢉ")):
            hub_url = hub_url[8:]
        bstack1l1lll1l11_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack1lllll1ll1_opy_():
    global CONFIG
    bstack11ll1l111l_opy_ = CONFIG.get(bstack1l1111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢊ"), {}).get(bstack1l1111_opy_ (u"ࠪ࡫ࡷ࡯ࡤࡏࡣࡰࡩࠬࢋ"), bstack1l1111_opy_ (u"ࠫࡓࡕ࡟ࡈࡔࡌࡈࡤࡔࡁࡎࡇࡢࡔࡆ࡙ࡓࡆࡆࠪࢌ"))
    if not isinstance(bstack11ll1l111l_opy_, str):
        raise ValueError(bstack1l1111_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡌࡸࡩࡥࠢࡱࡥࡲ࡫ࠠ࡮ࡷࡶࡸࠥࡨࡥࠡࡣࠣࡺࡦࡲࡩࡥࠢࡶࡸࡷ࡯࡮ࡨࠤࢍ"))
    try:
        bstack1ll11111l1_opy_ = bstack1ll1ll11_opy_(bstack11ll1l111l_opy_)
        return bstack1ll11111l1_opy_
    except Exception as e:
        logger.error(bstack1l1111_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡩࡵ࡭ࡩࠦࡤࡦࡶࡤ࡭ࡱࡹࠠ࠻ࠢࡾࢁࠧࢎ").format(str(e)))
        return {}
def bstack1ll1ll11_opy_(bstack11ll1l111l_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack1l1111_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ࢏")] or not CONFIG[bstack1l1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ࢐")]:
            raise ValueError(bstack1l1111_opy_ (u"ࠤࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠤࡴࡸࠠࡢࡥࡦࡩࡸࡹࠠ࡬ࡧࡼࠦ࢑"))
        url = bstack1l11l1lll_opy_ + bstack11ll1l111l_opy_
        auth = (CONFIG[bstack1l1111_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ࢒")], CONFIG[bstack1l1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ࢓")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack1l1lll1lll_opy_ = json.loads(response.text)
            return bstack1l1lll1lll_opy_
    except ValueError as ve:
        logger.error(bstack1l1111_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡩࡵ࡭ࡩࠦࡤࡦࡶࡤ࡭ࡱࡹࠠ࠻ࠢࡾࢁࠧ࢔").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack1l1111_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡪࡶ࡮ࡪࠠࡥࡧࡷࡥ࡮ࡲࡳࠡ࠼ࠣࡿࢂࠨ࢕").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack1lllll11l_opy_(bstack1lllll1111_opy_):
    global CONFIG
    if bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ࢖") not in CONFIG or str(CONFIG[bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬࢗ")]).lower() == bstack1l1111_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ࢘"):
        CONFIG[bstack1l1111_opy_ (u"ࠪࡰࡴࡩࡡ࡭࢙ࠩ")] = False
    elif bstack1l1111_opy_ (u"ࠫ࡮ࡹࡔࡳ࡫ࡤࡰࡌࡸࡩࡥ࢚ࠩ") in bstack1lllll1111_opy_:
        bstack11ll11l1ll_opy_ = CONFIG.get(bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴ࢛ࠩ"), {})
        logger.debug(bstack1l1111_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡸࡪࡵࡷ࡭ࡳ࡭ࠠ࡭ࡱࡦࡥࡱࠦ࡯ࡱࡶ࡬ࡳࡳࡹ࠺ࠡࠧࡶࠦ࢜"), bstack11ll11l1ll_opy_)
        bstack111lllll11_opy_ = bstack1lllll1111_opy_.get(bstack1l1111_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡒࡦࡲࡨࡥࡹ࡫ࡲࡴࠤ࢝"), [])
        bstack11l1l11ll1_opy_ = bstack1l1111_opy_ (u"ࠣ࠮ࠥ࢞").join(bstack111lllll11_opy_)
        logger.debug(bstack1l1111_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡅࡸࡷࡹࡵ࡭ࠡࡴࡨࡴࡪࡧࡴࡦࡴࠣࡷࡹࡸࡩ࡯ࡩ࠽ࠤࠪࡹࠢ࢟"), bstack11l1l11ll1_opy_)
        bstack1ll1l1l11_opy_ = {
            bstack1l1111_opy_ (u"ࠥࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧࢠ"): bstack1l1111_opy_ (u"ࠦࡦࡺࡳ࠮ࡴࡨࡴࡪࡧࡴࡦࡴࠥࢡ"),
            bstack1l1111_opy_ (u"ࠧ࡬࡯ࡳࡥࡨࡐࡴࡩࡡ࡭ࠤࢢ"): bstack1l1111_opy_ (u"ࠨࡴࡳࡷࡨࠦࢣ"),
            bstack1l1111_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࠭ࡳࡧࡳࡩࡦࡺࡥࡳࠤࢤ"): bstack11l1l11ll1_opy_
        }
        bstack11ll11l1ll_opy_.update(bstack1ll1l1l11_opy_)
        logger.debug(bstack1l1111_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡖࡲࡧࡥࡹ࡫ࡤࠡ࡮ࡲࡧࡦࡲࠠࡰࡲࡷ࡭ࡴࡴࡳ࠻ࠢࠨࡷࠧࢥ"), bstack11ll11l1ll_opy_)
        CONFIG[bstack1l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢦ")] = bstack11ll11l1ll_opy_
        logger.debug(bstack1l1111_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡉ࡭ࡳࡧ࡬ࠡࡅࡒࡒࡋࡏࡇ࠻ࠢࠨࡷࠧࢧ"), CONFIG)
def bstack1l111ll111_opy_():
    bstack1ll11111l1_opy_ = bstack1lllll1ll1_opy_()
    if not bstack1ll11111l1_opy_[bstack1l1111_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡖࡴ࡯ࠫࢨ")]:
      raise ValueError(bstack1l1111_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡗࡵࡰࠥ࡯ࡳࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡩࡶࡴࡳࠠࡨࡴ࡬ࡨࠥࡪࡥࡵࡣ࡬ࡰࡸ࠴ࠢࢩ"))
    return bstack1ll11111l1_opy_[bstack1l1111_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡘࡶࡱ࠭ࢪ")] + bstack1l1111_opy_ (u"ࠧࡀࡥࡤࡴࡸࡃࠧࢫ")
@measure(event_name=EVENTS.bstack1ll1lllll1_opy_, stage=STAGE.bstack1111lll11_opy_)
def bstack1ll111ll_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack1l1111_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪࢬ")], CONFIG[bstack1l1111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬࢭ")])
        url = bstack11ll11ll_opy_
        logger.debug(bstack1l1111_opy_ (u"ࠥࡅࡹࡺࡥ࡮ࡲࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴࠢࡩࡶࡴࡳࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡔࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠣࡅࡕࡏࠢࢮ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack1l1111_opy_ (u"ࠦࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠥࢯ"): bstack1l1111_opy_ (u"ࠧࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠣࢰ")})
            if response.status_code == 200:
                bstack1l11ll1ll1_opy_ = json.loads(response.text)
                bstack11llllll1l_opy_ = bstack1l11ll1ll1_opy_.get(bstack1l1111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡸ࠭ࢱ"), [])
                if bstack11llllll1l_opy_:
                    bstack11ll1llll1_opy_ = bstack11llllll1l_opy_[0]
                    build_hashed_id = bstack11ll1llll1_opy_.get(bstack1l1111_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪࢲ"))
                    bstack1lll1ll1l1_opy_ = bstack1l111ll1l1_opy_ + build_hashed_id
                    result.extend([build_hashed_id, bstack1lll1ll1l1_opy_])
                    logger.info(bstack1l1111111_opy_.format(bstack1lll1ll1l1_opy_))
                    bstack11l1lll11l_opy_ = CONFIG[bstack1l1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫࢳ")]
                    if bstack1l1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࢴ") in CONFIG:
                      bstack11l1lll11l_opy_ += bstack1l1111_opy_ (u"ࠪࠤࠬࢵ") + CONFIG[bstack1l1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࢶ")]
                    if bstack11l1lll11l_opy_ != bstack11ll1llll1_opy_.get(bstack1l1111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪࢷ")):
                      logger.debug(bstack1l1l111l1l_opy_.format(bstack11ll1llll1_opy_.get(bstack1l1111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫࢸ")), bstack11l1lll11l_opy_))
                    return result
                else:
                    logger.debug(bstack1l1111_opy_ (u"ࠢࡂࡖࡖࠤ࠿ࠦࡎࡰࠢࡥࡹ࡮ࡲࡤࡴࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠱ࠦࢹ"))
            else:
                logger.debug(bstack1l1111_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴ࠰ࠥࢺ"))
        except Exception as e:
            logger.error(bstack1l1111_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࡶࠤ࠿ࠦࡻࡾࠤࢻ").format(str(e)))
    else:
        logger.debug(bstack1l1111_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡆࡓࡓࡌࡉࡈࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡶࡩࡹ࠴ࠠࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴ࠰ࠥࢼ"))
    return [None, None]
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1ll1111ll_opy_ import bstack1ll1111ll_opy_, bstack1ll1l11l_opy_, bstack1l1l11l1l_opy_, bstack1ll111llll_opy_
from bstack_utils.measure import bstack11l111111l_opy_
from bstack_utils.measure import measure
from bstack_utils.percy import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1lll1l111l_opy_ import bstack11lll1ll11_opy_
from bstack_utils.messages import *
from bstack_utils import bstack111llll1ll_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack11l111111_opy_, bstack1l1ll11111_opy_, bstack11ll1l11_opy_, bstack111111lll_opy_, \
  bstack1l111111l1_opy_, \
  Notset, bstack111l1lll11_opy_, \
  bstack11lllll1_opy_, bstack1l111llll_opy_, bstack111ll1l1_opy_, bstack1l11ll1l1_opy_, bstack1llllll1l_opy_, bstack1111l111_opy_, \
  bstack111l11ll1_opy_, \
  bstack11111ll1_opy_, bstack1111lll1l_opy_, bstack1l1lllll1_opy_, bstack1llllll111_opy_, \
  bstack11lll11l11_opy_, bstack1l1111l111_opy_, bstack1l1111lll1_opy_, bstack11l1l1ll1_opy_, bstack111l11ll_opy_
from bstack_utils.bstack11l1lll1ll_opy_ import bstack111lll1l1_opy_
from bstack_utils.bstack11111l1l_opy_ import bstack111lll1111_opy_, bstack1l1ll1ll_opy_
from bstack_utils.bstack111llll1l1_opy_ import bstack1lll1l1l11_opy_
from bstack_utils.bstack11l1l11l1_opy_ import bstack1l111l1ll_opy_, bstack1llll1lll1_opy_
from bstack_utils.bstack1l1111l1ll_opy_ import bstack1l1111l1ll_opy_
from bstack_utils.bstack1l1lll111l_opy_ import bstack1l11l1ll11_opy_
from bstack_utils.proxy import bstack11l1l111l1_opy_, bstack1l11ll11l1_opy_, bstack1ll1l1l1_opy_, bstack11l1ll111l_opy_
from bstack_utils.bstack11l11l11ll_opy_ import bstack1l1lll111_opy_, bstack111ll111ll_opy_
import bstack_utils.bstack111ll1llll_opy_ as bstack11l11ll111_opy_
import bstack_utils.bstack111lll111_opy_ as bstack1l111llll1_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.utils.bstack1llll1ll11_opy_ import bstack11ll1lll1_opy_
from bstack_utils.bstack111l1111_opy_ import bstack1l1llll1l_opy_
from bstack_utils.bstack1l11l11l1_opy_ import bstack111lll1l1l_opy_
from bstack_utils.bstack11l111111l_opy_ import bstack11ll111lll_opy_
if os.getenv(bstack1l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡉࡑࡒࡏࡘ࠭ࢽ")):
  cli.bstack1llll1l11_opy_()
else:
  os.environ[bstack1l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡊࡒࡓࡐ࡙ࠧࢾ")] = bstack1l1111_opy_ (u"࠭ࡴࡳࡷࡨࠫࢿ")
bstack111ll111l1_opy_ = bstack1l1111_opy_ (u"ࠧࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠠࠡ࡫ࡩࠬࡵࡧࡧࡦࠢࡀࡁࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠠࡼ࡞ࡱࠤࠥࠦࡴࡳࡻࡾࡠࡳࠦࡣࡰࡰࡶࡸࠥ࡬ࡳࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࡡ࠭ࡦࡴ࡞ࠪ࠭ࡀࡢ࡮ࠡࠢࠣࠤࠥ࡬ࡳ࠯ࡣࡳࡴࡪࡴࡤࡇ࡫࡯ࡩࡘࡿ࡮ࡤࠪࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠬࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡳࡣ࡮ࡴࡤࡦࡺࠬࠤ࠰ࠦࠢ࠻ࠤࠣ࠯ࠥࡐࡓࡐࡐ࠱ࡷࡹࡸࡩ࡯ࡩ࡬ࡪࡾ࠮ࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࠬࡦࡽࡡࡪࡶࠣࡲࡪࡽࡐࡢࡩࡨ࠶࠳࡫ࡶࡢ࡮ࡸࡥࡹ࡫ࠨࠣࠪࠬࠤࡂࡄࠠࡼࡿࠥ࠰ࠥࡢࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡨࡧࡷࡗࡪࡹࡳࡪࡱࡱࡈࡪࡺࡡࡪ࡮ࡶࠦࢂࡢࠧࠪࠫࠬ࡟ࠧ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠣ࡟ࠬࠤ࠰ࠦࠢ࠭࡞࡟ࡲࠧ࠯࡜࡯ࠢࠣࠤࠥࢃࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡽ࡝ࡰࠣࠤ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠧࣀ")
bstack11l11ll1l1_opy_ = bstack1l1111_opy_ (u"ࠨ࡞ࡱ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࡢ࡮ࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡰࡢࡶ࡫ࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳࡞࡞ࡱࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠴ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡶ࡟ࡪࡰࡧࡩࡽࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠴ࡠࡠࡳࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡹ࡬ࡪࡥࡨࠬ࠵࠲ࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࠬࡠࡳࡩ࡯࡯ࡵࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬ࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ࠭ࡀࡢ࡮ࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮࡭ࡣࡸࡲࡨ࡮ࠠ࠾ࠢࡤࡷࡾࡴࡣࠡࠪ࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴࠫࠣࡁࡃࠦࡻ࡝ࡰ࡯ࡩࡹࠦࡣࡢࡲࡶ࠿ࡡࡴࡴࡳࡻࠣࡿࡡࡴࡣࡢࡲࡶࠤࡂࠦࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠪ࡞ࡱࠤࠥࢃࠠࡤࡣࡷࡧ࡭࠮ࡥࡹࠫࠣࡿࡡࡴࠠࠡࠢࠣࢁࡡࡴࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡣࡺࡥ࡮ࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮ࡤࡱࡱࡲࡪࡩࡴࠩࡽ࡟ࡲࠥࠦࠠࠡࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸ࠿ࠦࡠࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠦࡾࡩࡳࡩ࡯ࡥࡧࡘࡖࡎࡉ࡯࡮ࡲࡲࡲࡪࡴࡴࠩࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡦࡥࡵࡹࠩࠪࡿࡣ࠰ࡡࡴࠠࠡࠢࠣ࠲࠳࠴࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸࡢ࡮ࠡࠢࢀ࠭ࡡࡴࡽ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠧࣁ")
from ._version import __version__
bstack1l1l1ll1ll_opy_ = None
CONFIG = {}
bstack11l1111l1_opy_ = {}
bstack1111ll1l1_opy_ = {}
bstack11lll1llll_opy_ = None
bstack11ll1ll11_opy_ = None
bstack11l1111lll_opy_ = None
bstack1l1llll11_opy_ = -1
bstack11l1ll1l11_opy_ = 0
bstack11l1ll11l1_opy_ = bstack1lllll11_opy_
bstack11ll1l1ll1_opy_ = 1
bstack1l11llll_opy_ = False
bstack1lll111ll1_opy_ = False
bstack111l111l_opy_ = bstack1l1111_opy_ (u"ࠩࠪࣂ")
bstack11l11111_opy_ = bstack1l1111_opy_ (u"ࠪࠫࣃ")
bstack1lll11l11l_opy_ = False
bstack1l1llll1l1_opy_ = True
bstack1ll1l11l11_opy_ = bstack1l1111_opy_ (u"ࠫࠬࣄ")
bstack1l1lll11ll_opy_ = []
bstack11l1l11111_opy_ = threading.Lock()
bstack1lll1111l1_opy_ = threading.Lock()
bstack1111l1l11_opy_ = None
bstack1l1lll1l11_opy_ = bstack1l1111_opy_ (u"ࠬ࠭ࣅ")
bstack1ll11l1l_opy_ = False
bstack11l1ll11l_opy_ = None
bstack1llll1llll_opy_ = None
bstack1lllll1lll_opy_ = None
bstack1l111l11l_opy_ = -1
bstack1ll1ll1lll_opy_ = os.path.join(os.path.expanduser(bstack1l1111_opy_ (u"࠭ࡾࠨࣆ")), bstack1l1111_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧࣇ"), bstack1l1111_opy_ (u"ࠨ࠰ࡵࡳࡧࡵࡴ࠮ࡴࡨࡴࡴࡸࡴ࠮ࡪࡨࡰࡵ࡫ࡲ࠯࡬ࡶࡳࡳ࠭ࣈ"))
bstack1l1l111lll_opy_ = 0
bstack1l111l1111_opy_ = 0
bstack1l11l1ll1_opy_ = []
bstack111l1lll1_opy_ = []
ROBOT_PYTHON_ERRORS = []
bstack111l1ll1ll_opy_ = []
bstack11ll1l111_opy_ = bstack1l1111_opy_ (u"ࠩࠪࣉ")
bstack1ll11111l_opy_ = bstack1l1111_opy_ (u"ࠪࠫ࣊")
bstack1l1lll11l_opy_ = False
bstack1l1ll11ll1_opy_ = False
bstack11lll111_opy_ = {}
bstack1ll1lllll_opy_ = {}
bstack1llll11l1l_opy_ = None
bstack1l111111l_opy_ = None
bstack11111ll11_opy_ = None
bstack1l1ll1l11l_opy_ = None
bstack111lllll1_opy_ = None
bstack1l11l1l1_opy_ = None
bstack1llll1l1l1_opy_ = None
bstack1lll1llll1_opy_ = None
bstack1l1111ll11_opy_ = None
bstack11llllllll_opy_ = None
bstack1lll1ll1ll_opy_ = None
bstack11l11ll11l_opy_ = None
bstack11l1ll1l_opy_ = None
bstack11ll11lll_opy_ = None
bstack1l11l111l1_opy_ = None
bstack1ll1l1l1l_opy_ = None
bstack1l1l1llll_opy_ = None
bstack11ll1l1l_opy_ = None
bstack11lll1lll1_opy_ = None
bstack111llllll1_opy_ = None
bstack11lll1lll_opy_ = None
bstack1ll1ll111_opy_ = None
bstack1ll1lll1_opy_ = None
thread_local = threading.local()
bstack11llll1111_opy_ = False
bstack1111lllll_opy_ = bstack1l1111_opy_ (u"ࠦࠧ࣋")
logger = bstack111llll1ll_opy_.get_logger(__name__, bstack11l1ll11l1_opy_)
bstack11l1lll11_opy_ = bstack111llll1ll_opy_.bstack1l11ll11l_opy_(__name__)
bstack1llllll11l_opy_ = Config.bstack111ll1lll1_opy_()
percy = bstack1l1l11l1ll_opy_()
bstack1ll1l11l1_opy_ = bstack11lll1ll11_opy_()
bstack1llll1ll_opy_ = bstack11ll11ll1_opy_()
def bstack1l1l1l1l1l_opy_():
  global CONFIG
  global bstack1l1lll11l_opy_
  global bstack1llllll11l_opy_
  testContextOptions = bstack11l11l1ll_opy_(CONFIG)
  if bstack1l111111l1_opy_(CONFIG):
    if (bstack1l1111_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ࣌") in testContextOptions and str(testContextOptions[bstack1l1111_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ࣍")]).lower() == bstack1l1111_opy_ (u"ࠧࡵࡴࡸࡩࠬ࣎")):
      bstack1l1lll11l_opy_ = True
    bstack1llllll11l_opy_.bstack1l11ll1111_opy_(testContextOptions.get(bstack1l1111_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷ࣏ࠬ"), False))
  else:
    bstack1l1lll11l_opy_ = True
    bstack1llllll11l_opy_.bstack1l11ll1111_opy_(True)
def bstack1l1l111ll_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack11ll111l_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack11l11lll1l_opy_():
  global bstack1ll1lllll_opy_
  args = sys.argv
  for i in range(len(args)):
    if bstack1l1111_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡦࡳࡳ࡬ࡩࡨࡨ࡬ࡰࡪࠨ࣐") == args[i].lower() or bstack1l1111_opy_ (u"ࠥ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡮ࡧ࡫ࡪ࣑ࠦ") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      bstack1ll1lllll_opy_[bstack1l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ࣒")] = path
      return path
  return None
bstack1l1ll1llll_opy_ = re.compile(bstack1l1111_opy_ (u"ࡷࠨ࠮ࠫࡁ࡟ࠨࢀ࠮࠮ࠫࡁࠬࢁ࠳࠰࠿࣓ࠣ"))
def bstack11l1111l1l_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1l1ll1llll_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack1l1111_opy_ (u"ࠨࠤࡼࠤࣔ") + group + bstack1l1111_opy_ (u"ࠢࡾࠤࣕ"), os.environ.get(group))
  return value
def bstack1ll11lllll_opy_():
  global bstack1ll1lll1_opy_
  if bstack1ll1lll1_opy_ is None:
        bstack1ll1lll1_opy_ = bstack11l11lll1l_opy_()
  bstack1l1lll1ll1_opy_ = bstack1ll1lll1_opy_
  if bstack1l1lll1ll1_opy_ and os.path.exists(os.path.abspath(bstack1l1lll1ll1_opy_)):
    fileName = bstack1l1lll1ll1_opy_
  if bstack1l1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬࣖ") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack1l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࡠࡈࡌࡐࡊ࠭ࣗ")])) and not bstack1l1111_opy_ (u"ࠪࡪ࡮ࡲࡥࡏࡣࡰࡩࠬࣘ") in locals():
    fileName = os.environ[bstack1l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨࣙ")]
  if bstack1l1111_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡑࡥࡲ࡫ࠧࣚ") in locals():
    bstack1llllll1_opy_ = os.path.abspath(fileName)
  else:
    bstack1llllll1_opy_ = bstack1l1111_opy_ (u"࠭ࠧࣛ")
  bstack111l1l111_opy_ = os.getcwd()
  bstack1lll1lll1_opy_ = bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪࣜ")
  bstack1lll11l1l1_opy_ = bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺࡣࡰࡰࠬࣝ")
  while (not os.path.exists(bstack1llllll1_opy_)) and bstack111l1l111_opy_ != bstack1l1111_opy_ (u"ࠤࠥࣞ"):
    bstack1llllll1_opy_ = os.path.join(bstack111l1l111_opy_, bstack1lll1lll1_opy_)
    if not os.path.exists(bstack1llllll1_opy_):
      bstack1llllll1_opy_ = os.path.join(bstack111l1l111_opy_, bstack1lll11l1l1_opy_)
    if bstack111l1l111_opy_ != os.path.dirname(bstack111l1l111_opy_):
      bstack111l1l111_opy_ = os.path.dirname(bstack111l1l111_opy_)
    else:
      bstack111l1l111_opy_ = bstack1l1111_opy_ (u"ࠥࠦࣟ")
  bstack1ll1lll1_opy_ = bstack1llllll1_opy_ if os.path.exists(bstack1llllll1_opy_) else None
  return bstack1ll1lll1_opy_
def bstack1l11llllll_opy_(config):
    if bstack1l1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࠫ࣠") in config:
      config[bstack1l1111_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ࣡")] = config[bstack1l1111_opy_ (u"࠭ࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬࠭࣢")]
    if bstack1l1111_opy_ (u"ࠧࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭ࡏࡱࡶ࡬ࡳࡳࡹࣣࠧ") in config:
      config[bstack1l1111_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬࣤ")] = config[bstack1l1111_opy_ (u"ࠩࡷࡩࡸࡺࡒࡦࡲࡲࡶࡹ࡯࡮ࡨࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣥ")]
def bstack11l1l1ll1l_opy_():
  bstack1llllll1_opy_ = bstack1ll11lllll_opy_()
  if not os.path.exists(bstack1llllll1_opy_):
    bstack11ll11l1l_opy_(
      bstack11l1lll111_opy_.format(os.getcwd()))
  try:
    with open(bstack1llllll1_opy_, bstack1l1111_opy_ (u"ࠪࡶࣦࠬ")) as stream:
      yaml.add_implicit_resolver(bstack1l1111_opy_ (u"ࠦࠦࡶࡡࡵࡪࡨࡼࠧࣧ"), bstack1l1ll1llll_opy_)
      yaml.add_constructor(bstack1l1111_opy_ (u"ࠧࠧࡰࡢࡶ࡫ࡩࡽࠨࣨ"), bstack11l1111l1l_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      bstack1l11llllll_opy_(config)
      return config
  except:
    with open(bstack1llllll1_opy_, bstack1l1111_opy_ (u"࠭ࡲࠨࣩ")) as stream:
      try:
        config = yaml.safe_load(stream)
        bstack1l11llllll_opy_(config)
        return config
      except yaml.YAMLError as exc:
        bstack11ll11l1l_opy_(bstack1ll1llll1l_opy_.format(str(exc)))
def bstack1l11ll1lll_opy_(config):
  bstack1l111l1ll1_opy_ = bstack11l111ll1l_opy_(config)
  for option in list(bstack1l111l1ll1_opy_):
    if option.lower() in bstack1ll11l11_opy_ and option != bstack1ll11l11_opy_[option.lower()]:
      bstack1l111l1ll1_opy_[bstack1ll11l11_opy_[option.lower()]] = bstack1l111l1ll1_opy_[option]
      del bstack1l111l1ll1_opy_[option]
  return config
def bstack11llll11l_opy_():
  global bstack1111ll1l1_opy_
  for key, bstack1l11lllll1_opy_ in bstack1l1lll1l1_opy_.items():
    if isinstance(bstack1l11lllll1_opy_, list):
      for var in bstack1l11lllll1_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1111ll1l1_opy_[key] = os.environ[var]
          break
    elif bstack1l11lllll1_opy_ in os.environ and os.environ[bstack1l11lllll1_opy_] and str(os.environ[bstack1l11lllll1_opy_]).strip():
      bstack1111ll1l1_opy_[key] = os.environ[bstack1l11lllll1_opy_]
  if bstack1l1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩ࣪") in os.environ:
    bstack1111ll1l1_opy_[bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ࣫")] = {}
    bstack1111ll1l1_opy_[bstack1l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭࣬")][bstack1l1111_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ࣭ࠬ")] = os.environ[bstack1l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࣮࠭")]
def bstack1llll11l1_opy_():
  global bstack11l1111l1_opy_
  global bstack1ll1l11l11_opy_
  global bstack1ll1lllll_opy_
  bstack1l1l1ll1_opy_ = []
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) - 1 and bstack1l1111_opy_ (u"ࠬ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ࣯").lower() == val.lower():
      bstack11l1111l1_opy_[bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࣰࠪ")] = {}
      bstack11l1111l1_opy_[bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࣱࠫ")][bstack1l1111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࣲࠪ")] = sys.argv[idx + 1]
      bstack1l1l1ll1_opy_.extend([idx, idx + 1])
      break
  for key, bstack1l11ll1l1l_opy_ in bstack1l11l11ll1_opy_.items():
    if isinstance(bstack1l11ll1l1l_opy_, list):
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        for var in bstack1l11ll1l1l_opy_:
          if bstack1l1111_opy_ (u"ࠩ࠰࠱ࠬࣳ") + var.lower() == val.lower() and key not in bstack11l1111l1_opy_:
            bstack11l1111l1_opy_[key] = sys.argv[idx + 1]
            bstack1ll1l11l11_opy_ += bstack1l1111_opy_ (u"ࠪࠤ࠲࠳ࠧࣴ") + var + bstack1l1111_opy_ (u"ࠫࠥ࠭ࣵ") + shlex.quote(sys.argv[idx + 1])
            bstack111l11ll_opy_(bstack1ll1lllll_opy_, key, sys.argv[idx + 1])
            bstack1l1l1ll1_opy_.extend([idx, idx + 1])
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        if bstack1l1111_opy_ (u"ࠬ࠳࠭ࠨࣶ") + bstack1l11ll1l1l_opy_.lower() == val.lower() and key not in bstack11l1111l1_opy_:
          bstack11l1111l1_opy_[key] = sys.argv[idx + 1]
          bstack1ll1l11l11_opy_ += bstack1l1111_opy_ (u"࠭ࠠ࠮࠯ࠪࣷ") + bstack1l11ll1l1l_opy_ + bstack1l1111_opy_ (u"ࠧࠡࠩࣸ") + shlex.quote(sys.argv[idx + 1])
          bstack111l11ll_opy_(bstack1ll1lllll_opy_, key, sys.argv[idx + 1])
          bstack1l1l1ll1_opy_.extend([idx, idx + 1])
  for idx in sorted(set(bstack1l1l1ll1_opy_), reverse=True):
    if idx < len(sys.argv):
      del sys.argv[idx]
def bstack1111l1l1l_opy_(config):
  bstack111ll111_opy_ = config.keys()
  for bstack1l1l111ll1_opy_, bstack1ll1l111l_opy_ in bstack11lll11l_opy_.items():
    if bstack1ll1l111l_opy_ in bstack111ll111_opy_:
      config[bstack1l1l111ll1_opy_] = config[bstack1ll1l111l_opy_]
      del config[bstack1ll1l111l_opy_]
  for bstack1l1l111ll1_opy_, bstack1ll1l111l_opy_ in bstack111lll1ll_opy_.items():
    if isinstance(bstack1ll1l111l_opy_, list):
      for bstack11l1l1l1l1_opy_ in bstack1ll1l111l_opy_:
        if bstack11l1l1l1l1_opy_ in bstack111ll111_opy_:
          config[bstack1l1l111ll1_opy_] = config[bstack11l1l1l1l1_opy_]
          del config[bstack11l1l1l1l1_opy_]
          break
    elif bstack1ll1l111l_opy_ in bstack111ll111_opy_:
      config[bstack1l1l111ll1_opy_] = config[bstack1ll1l111l_opy_]
      del config[bstack1ll1l111l_opy_]
  for bstack11l1l1l1l1_opy_ in list(config):
    for bstack1l1ll1ll1_opy_ in bstack1ll11ll1l_opy_:
      if bstack11l1l1l1l1_opy_.lower() == bstack1l1ll1ll1_opy_.lower() and bstack11l1l1l1l1_opy_ != bstack1l1ll1ll1_opy_:
        config[bstack1l1ll1ll1_opy_] = config[bstack11l1l1l1l1_opy_]
        del config[bstack11l1l1l1l1_opy_]
  bstack111111l11_opy_ = [{}]
  if not config.get(bstack1l1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࣹࠫ")):
    config[bstack1l1111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࣺࠬ")] = [{}]
  bstack111111l11_opy_ = config[bstack1l1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣻ")]
  for platform in bstack111111l11_opy_:
    for bstack11l1l1l1l1_opy_ in list(platform):
      for bstack1l1ll1ll1_opy_ in bstack1ll11ll1l_opy_:
        if bstack11l1l1l1l1_opy_.lower() == bstack1l1ll1ll1_opy_.lower() and bstack11l1l1l1l1_opy_ != bstack1l1ll1ll1_opy_:
          platform[bstack1l1ll1ll1_opy_] = platform[bstack11l1l1l1l1_opy_]
          del platform[bstack11l1l1l1l1_opy_]
  for bstack1l1l111ll1_opy_, bstack1ll1l111l_opy_ in bstack111lll1ll_opy_.items():
    for platform in bstack111111l11_opy_:
      if isinstance(bstack1ll1l111l_opy_, list):
        for bstack11l1l1l1l1_opy_ in bstack1ll1l111l_opy_:
          if bstack11l1l1l1l1_opy_ in platform:
            platform[bstack1l1l111ll1_opy_] = platform[bstack11l1l1l1l1_opy_]
            del platform[bstack11l1l1l1l1_opy_]
            break
      elif bstack1ll1l111l_opy_ in platform:
        platform[bstack1l1l111ll1_opy_] = platform[bstack1ll1l111l_opy_]
        del platform[bstack1ll1l111l_opy_]
  for bstack1lll11111_opy_ in bstack11l11ll1l_opy_:
    if bstack1lll11111_opy_ in config:
      if not bstack11l11ll1l_opy_[bstack1lll11111_opy_] in config:
        config[bstack11l11ll1l_opy_[bstack1lll11111_opy_]] = {}
      config[bstack11l11ll1l_opy_[bstack1lll11111_opy_]].update(config[bstack1lll11111_opy_])
      del config[bstack1lll11111_opy_]
  for platform in bstack111111l11_opy_:
    for bstack1lll11111_opy_ in bstack11l11ll1l_opy_:
      if bstack1lll11111_opy_ in list(platform):
        if not bstack11l11ll1l_opy_[bstack1lll11111_opy_] in platform:
          platform[bstack11l11ll1l_opy_[bstack1lll11111_opy_]] = {}
        platform[bstack11l11ll1l_opy_[bstack1lll11111_opy_]].update(platform[bstack1lll11111_opy_])
        del platform[bstack1lll11111_opy_]
  config = bstack1l11ll1lll_opy_(config)
  return config
def bstack11lllllll_opy_(config):
  global bstack11l11111_opy_
  bstack11l1l1lll1_opy_ = False
  if bstack1l1111_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨࣼ") in config and str(config[bstack1l1111_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩࣽ")]).lower() != bstack1l1111_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬࣾ"):
    if bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫࣿ") not in config or str(config[bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬऀ")]).lower() == bstack1l1111_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨँ"):
      config[bstack1l1111_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩं")] = False
    else:
      bstack1ll11111l1_opy_ = bstack1lllll1ll1_opy_()
      if bstack1l1111_opy_ (u"ࠫ࡮ࡹࡔࡳ࡫ࡤࡰࡌࡸࡩࡥࠩः") in bstack1ll11111l1_opy_:
        if not bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩऄ") in config:
          config[bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪअ")] = {}
        config[bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫआ")][bstack1l1111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪइ")] = bstack1l1111_opy_ (u"ࠩࡤࡸࡸ࠳ࡲࡦࡲࡨࡥࡹ࡫ࡲࠨई")
        bstack11l1l1lll1_opy_ = True
        bstack11l11111_opy_ = config[bstack1l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧउ")].get(bstack1l1111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ऊ"))
  if bstack1l111111l1_opy_(config) and bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩऋ") in config and str(config[bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪऌ")]).lower() != bstack1l1111_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ऍ") and not bstack11l1l1lll1_opy_:
    if not bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬऎ") in config:
      config[bstack1l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ए")] = {}
    if not config[bstack1l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧऐ")].get(bstack1l1111_opy_ (u"ࠫࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠨऑ")) and not bstack1l1111_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऒ") in config[bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪओ")]:
      bstack1111l11l1_opy_ = datetime.datetime.now()
      bstack1l1l11l11_opy_ = bstack1111l11l1_opy_.strftime(bstack1l1111_opy_ (u"ࠧࠦࡦࡢࠩࡧࡥࠥࡉࠧࡐࠫऔ"))
      hostname = socket.gethostname()
      bstack1llll11l11_opy_ = bstack1l1111_opy_ (u"ࠨࠩक").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1l1111_opy_ (u"ࠩࡾࢁࡤࢁࡽࡠࡽࢀࠫख").format(bstack1l1l11l11_opy_, hostname, bstack1llll11l11_opy_)
      config[bstack1l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧग")][bstack1l1111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭घ")] = identifier
    bstack11l11111_opy_ = config[bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩङ")].get(bstack1l1111_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨच"))
  return config
def bstack11l1lllll1_opy_():
  bstack111l1lllll_opy_ =  bstack1l11ll1l1_opy_()[bstack1l1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷ࠭छ")]
  return bstack111l1lllll_opy_ if bstack111l1lllll_opy_ else -1
def bstack11lll1l11l_opy_(bstack111l1lllll_opy_):
  global CONFIG
  if not bstack1l1111_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪज") in CONFIG[bstack1l1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫझ")]:
    return
  CONFIG[bstack1l1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬञ")] = CONFIG[bstack1l1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ट")].replace(
    bstack1l1111_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧठ"),
    str(bstack111l1lllll_opy_)
  )
def bstack11lll1l1ll_opy_():
  global CONFIG
  if not bstack1l1111_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬड") in CONFIG[bstack1l1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩढ")]:
    return
  bstack1111l11l1_opy_ = datetime.datetime.now()
  bstack1l1l11l11_opy_ = bstack1111l11l1_opy_.strftime(bstack1l1111_opy_ (u"ࠨࠧࡧ࠱ࠪࡨ࠭ࠦࡊ࠽ࠩࡒ࠭ण"))
  CONFIG[bstack1l1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫत")] = CONFIG[bstack1l1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬथ")].replace(
    bstack1l1111_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪद"),
    bstack1l1l11l11_opy_
  )
def bstack1lll11lll_opy_():
  global CONFIG
  if bstack1l1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧध") in CONFIG and not bool(CONFIG[bstack1l1111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨन")]):
    del CONFIG[bstack1l1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऩ")]
    return
  if not bstack1l1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪप") in CONFIG:
    CONFIG[bstack1l1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫफ")] = bstack1l1111_opy_ (u"ࠪࠧࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ब")
  if bstack1l1111_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪभ") in CONFIG[bstack1l1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧम")]:
    bstack11lll1l1ll_opy_()
    os.environ[bstack1l1111_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪय")] = CONFIG[bstack1l1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩर")]
  if not bstack1l1111_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪऱ") in CONFIG[bstack1l1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫल")]:
    return
  bstack111l1lllll_opy_ = bstack1l1111_opy_ (u"ࠪࠫळ")
  bstack1l1l1ll1l1_opy_ = bstack11l1lllll1_opy_()
  if bstack1l1l1ll1l1_opy_ != -1:
    bstack111l1lllll_opy_ = bstack1l1111_opy_ (u"ࠫࡈࡏࠠࠨऴ") + str(bstack1l1l1ll1l1_opy_)
  if bstack111l1lllll_opy_ == bstack1l1111_opy_ (u"ࠬ࠭व"):
    bstack11l1l111l_opy_ = bstack11l1llll_opy_(CONFIG[bstack1l1111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩश")])
    if bstack11l1l111l_opy_ != -1:
      bstack111l1lllll_opy_ = str(bstack11l1l111l_opy_)
  if bstack111l1lllll_opy_:
    bstack11lll1l11l_opy_(bstack111l1lllll_opy_)
    os.environ[bstack1l1111_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫष")] = CONFIG[bstack1l1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪस")]
def bstack1llll1l1_opy_(bstack11l11lll_opy_, bstack1l1ll11ll_opy_, path):
  bstack11l11l11l1_opy_ = {
    bstack1l1111_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ह"): bstack1l1ll11ll_opy_
  }
  if os.path.exists(path):
    bstack11l1l11lll_opy_ = json.load(open(path, bstack1l1111_opy_ (u"ࠪࡶࡧ࠭ऺ")))
  else:
    bstack11l1l11lll_opy_ = {}
  bstack11l1l11lll_opy_[bstack11l11lll_opy_] = bstack11l11l11l1_opy_
  with open(path, bstack1l1111_opy_ (u"ࠦࡼ࠱ࠢऻ")) as outfile:
    json.dump(bstack11l1l11lll_opy_, outfile)
def bstack11l1llll_opy_(bstack11l11lll_opy_):
  bstack11l11lll_opy_ = str(bstack11l11lll_opy_)
  bstack1l1llllll1_opy_ = os.path.join(os.path.expanduser(bstack1l1111_opy_ (u"ࠬࢄ़ࠧ")), bstack1l1111_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ऽ"))
  try:
    if not os.path.exists(bstack1l1llllll1_opy_):
      os.makedirs(bstack1l1llllll1_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1l1111_opy_ (u"ࠧࡿࠩा")), bstack1l1111_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨि"), bstack1l1111_opy_ (u"ࠩ࠱ࡦࡺ࡯࡬ࡥ࠯ࡱࡥࡲ࡫࠭ࡤࡣࡦ࡬ࡪ࠴ࡪࡴࡱࡱࠫी"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1l1111_opy_ (u"ࠪࡻࠬु")):
        pass
      with open(file_path, bstack1l1111_opy_ (u"ࠦࡼ࠱ࠢू")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1l1111_opy_ (u"ࠬࡸࠧृ")) as bstack111ll1ll_opy_:
      bstack11ll1111l1_opy_ = json.load(bstack111ll1ll_opy_)
    if bstack11l11lll_opy_ in bstack11ll1111l1_opy_:
      bstack1l1ll111_opy_ = bstack11ll1111l1_opy_[bstack11l11lll_opy_][bstack1l1111_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪॄ")]
      bstack11llll11_opy_ = int(bstack1l1ll111_opy_) + 1
      bstack1llll1l1_opy_(bstack11l11lll_opy_, bstack11llll11_opy_, file_path)
      return bstack11llll11_opy_
    else:
      bstack1llll1l1_opy_(bstack11l11lll_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warning(bstack1l1l1111_opy_.format(str(e)))
    return -1
def bstack111111ll1_opy_(config):
  if not config[bstack1l1111_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩॅ")] or not config[bstack1l1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫॆ")]:
    return True
  else:
    return False
def bstack1l11111lll_opy_(config, index=0):
  global bstack1lll11l11l_opy_
  bstack11lll111ll_opy_ = {}
  caps = bstack1ll1l11ll_opy_ + bstack11l11l1l11_opy_
  if config.get(bstack1l1111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭े"), False):
    bstack11lll111ll_opy_[bstack1l1111_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧै")] = True
    bstack11lll111ll_opy_[bstack1l1111_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࡐࡲࡷ࡭ࡴࡴࡳࠨॉ")] = config.get(bstack1l1111_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩॊ"), {})
  if bstack1lll11l11l_opy_:
    caps += bstack1l111ll11_opy_
  for key in config:
    if key in caps + [bstack1l1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩो")]:
      continue
    bstack11lll111ll_opy_[key] = config[key]
  if bstack1l1111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪौ") in config:
    for bstack1l11111111_opy_ in config[bstack1l1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶ्ࠫ")][index]:
      if bstack1l11111111_opy_ in caps:
        continue
      bstack11lll111ll_opy_[bstack1l11111111_opy_] = config[bstack1l1111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॎ")][index][bstack1l11111111_opy_]
  bstack11lll111ll_opy_[bstack1l1111_opy_ (u"ࠪ࡬ࡴࡹࡴࡏࡣࡰࡩࠬॏ")] = socket.gethostname()
  if bstack1l1111_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬॐ") in bstack11lll111ll_opy_:
    del (bstack11lll111ll_opy_[bstack1l1111_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭॑")])
  return bstack11lll111ll_opy_
def bstack11lll11ll_opy_(config):
  global bstack1lll11l11l_opy_
  bstack11lll11111_opy_ = {}
  caps = bstack11l11l1l11_opy_
  if bstack1lll11l11l_opy_:
    caps += bstack1l111ll11_opy_
  for key in caps:
    if key in config:
      bstack11lll11111_opy_[key] = config[key]
  return bstack11lll11111_opy_
def bstack111l1l1l_opy_(bstack11lll111ll_opy_, bstack11lll11111_opy_):
  bstack1llll11l_opy_ = {}
  for key in bstack11lll111ll_opy_.keys():
    if key in bstack11lll11l_opy_:
      bstack1llll11l_opy_[bstack11lll11l_opy_[key]] = bstack11lll111ll_opy_[key]
    else:
      bstack1llll11l_opy_[key] = bstack11lll111ll_opy_[key]
  for key in bstack11lll11111_opy_:
    if key in bstack11lll11l_opy_:
      bstack1llll11l_opy_[bstack11lll11l_opy_[key]] = bstack11lll11111_opy_[key]
    else:
      bstack1llll11l_opy_[key] = bstack11lll11111_opy_[key]
  return bstack1llll11l_opy_
def bstack11l1l1l11l_opy_(config, index=0):
  global bstack1lll11l11l_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack1lllll11l1_opy_ = bstack11l111111_opy_(bstack1l11ll111_opy_, config, logger)
  bstack11lll11111_opy_ = bstack11lll11ll_opy_(config)
  bstack11ll1l1l1l_opy_ = bstack11l11l1l11_opy_
  bstack11ll1l1l1l_opy_ += bstack111lll11l_opy_
  bstack11lll11111_opy_ = update(bstack11lll11111_opy_, bstack1lllll11l1_opy_)
  if bstack1lll11l11l_opy_:
    bstack11ll1l1l1l_opy_ += bstack1l111ll11_opy_
  if bstack1l1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴ॒ࠩ") in config:
    if bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ॓") in config[bstack1l1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ॔")][index]:
      caps[bstack1l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧॕ")] = config[bstack1l1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॖ")][index][bstack1l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩॗ")]
    if bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭क़") in config[bstack1l1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩख़")][index]:
      caps[bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨग़")] = str(config[bstack1l1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫज़")][index][bstack1l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪड़")])
    bstack1llll1l11l_opy_ = bstack11l111111_opy_(bstack1l11ll111_opy_, config[bstack1l1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ढ़")][index], logger)
    bstack11ll1l1l1l_opy_ += list(bstack1llll1l11l_opy_.keys())
    for bstack11l111ll11_opy_ in bstack11ll1l1l1l_opy_:
      if bstack11l111ll11_opy_ in config[bstack1l1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧफ़")][index]:
        if bstack11l111ll11_opy_ == bstack1l1111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧय़"):
          try:
            bstack1llll1l11l_opy_[bstack11l111ll11_opy_] = str(config[bstack1l1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩॠ")][index][bstack11l111ll11_opy_] * 1.0)
          except:
            bstack1llll1l11l_opy_[bstack11l111ll11_opy_] = str(config[bstack1l1111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪॡ")][index][bstack11l111ll11_opy_])
        else:
          bstack1llll1l11l_opy_[bstack11l111ll11_opy_] = config[bstack1l1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫॢ")][index][bstack11l111ll11_opy_]
        del (config[bstack1l1111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॣ")][index][bstack11l111ll11_opy_])
    bstack11lll11111_opy_ = update(bstack11lll11111_opy_, bstack1llll1l11l_opy_)
  bstack11lll111ll_opy_ = bstack1l11111lll_opy_(config, index)
  for bstack11l1l1l1l1_opy_ in bstack11l11l1l11_opy_ + list(bstack1lllll11l1_opy_.keys()):
    if bstack11l1l1l1l1_opy_ in bstack11lll111ll_opy_:
      bstack11lll11111_opy_[bstack11l1l1l1l1_opy_] = bstack11lll111ll_opy_[bstack11l1l1l1l1_opy_]
      del (bstack11lll111ll_opy_[bstack11l1l1l1l1_opy_])
  if bstack111l1lll11_opy_(config):
    bstack11lll111ll_opy_[bstack1l1111_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ।")] = True
    caps.update(bstack11lll11111_opy_)
    caps[bstack1l1111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ॥")] = bstack11lll111ll_opy_
  else:
    bstack11lll111ll_opy_[bstack1l1111_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ०")] = False
    caps.update(bstack111l1l1l_opy_(bstack11lll111ll_opy_, bstack11lll11111_opy_))
    if bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ१") in caps:
      caps[bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ२")] = caps[bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭३")]
      del (caps[bstack1l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ४")])
    if bstack1l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ५") in caps:
      caps[bstack1l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭६")] = caps[bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭७")]
      del (caps[bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ८")])
  return caps
def bstack1l1l11l1_opy_():
  global bstack1l1lll1l11_opy_
  global CONFIG
  if bstack11ll111l_opy_() <= version.parse(bstack1l1111_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧ९")):
    if bstack1l1lll1l11_opy_ != bstack1l1111_opy_ (u"ࠨࠩ॰"):
      return bstack1l1111_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥॱ") + bstack1l1lll1l11_opy_ + bstack1l1111_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢॲ")
    return bstack111ll11l_opy_
  if bstack1l1lll1l11_opy_ != bstack1l1111_opy_ (u"ࠫࠬॳ"):
    return bstack1l1111_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢॴ") + bstack1l1lll1l11_opy_ + bstack1l1111_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢॵ")
  return bstack1l1l1l1ll1_opy_
def bstack111l1ll11_opy_(options):
  return hasattr(options, bstack1l1111_opy_ (u"ࠧࡴࡧࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠨॶ"))
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
def bstack11ll11111l_opy_(options, bstack1ll1111111_opy_):
  for bstack1l11l11l1l_opy_ in bstack1ll1111111_opy_:
    if bstack1l11l11l1l_opy_ in [bstack1l1111_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ॷ"), bstack1l1111_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ॸ")]:
      continue
    if bstack1l11l11l1l_opy_ in options._experimental_options:
      options._experimental_options[bstack1l11l11l1l_opy_] = update(options._experimental_options[bstack1l11l11l1l_opy_],
                                                         bstack1ll1111111_opy_[bstack1l11l11l1l_opy_])
    else:
      options.add_experimental_option(bstack1l11l11l1l_opy_, bstack1ll1111111_opy_[bstack1l11l11l1l_opy_])
  if bstack1l1111_opy_ (u"ࠪࡥࡷ࡭ࡳࠨॹ") in bstack1ll1111111_opy_:
    for arg in bstack1ll1111111_opy_[bstack1l1111_opy_ (u"ࠫࡦࡸࡧࡴࠩॺ")]:
      options.add_argument(arg)
    del (bstack1ll1111111_opy_[bstack1l1111_opy_ (u"ࠬࡧࡲࡨࡵࠪॻ")])
  if bstack1l1111_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪॼ") in bstack1ll1111111_opy_:
    for ext in bstack1ll1111111_opy_[bstack1l1111_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫॽ")]:
      try:
        options.add_extension(ext)
      except OSError:
        options.add_encoded_extension(ext)
    del (bstack1ll1111111_opy_[bstack1l1111_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬॾ")])
def bstack111llll1_opy_(options, bstack11l1lll1l1_opy_):
  if bstack1l1111_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨॿ") in bstack11l1lll1l1_opy_:
    for bstack1l1111l1_opy_ in bstack11l1lll1l1_opy_[bstack1l1111_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩঀ")]:
      if bstack1l1111l1_opy_ in options._preferences:
        options._preferences[bstack1l1111l1_opy_] = update(options._preferences[bstack1l1111l1_opy_], bstack11l1lll1l1_opy_[bstack1l1111_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪঁ")][bstack1l1111l1_opy_])
      else:
        options.set_preference(bstack1l1111l1_opy_, bstack11l1lll1l1_opy_[bstack1l1111_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫং")][bstack1l1111l1_opy_])
  if bstack1l1111_opy_ (u"࠭ࡡࡳࡩࡶࠫঃ") in bstack11l1lll1l1_opy_:
    for arg in bstack11l1lll1l1_opy_[bstack1l1111_opy_ (u"ࠧࡢࡴࡪࡷࠬ঄")]:
      options.add_argument(arg)
def bstack11l1l1111_opy_(options, bstack1l1l1ll1l_opy_):
  if bstack1l1111_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࠩঅ") in bstack1l1l1ll1l_opy_:
    options.use_webview(bool(bstack1l1l1ll1l_opy_[bstack1l1111_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࠪআ")]))
  bstack11ll11111l_opy_(options, bstack1l1l1ll1l_opy_)
def bstack1llll111_opy_(options, bstack1l1l1l11l_opy_):
  for bstack1lll1ll11l_opy_ in bstack1l1l1l11l_opy_:
    if bstack1lll1ll11l_opy_ in [bstack1l1111_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧই"), bstack1l1111_opy_ (u"ࠫࡦࡸࡧࡴࠩঈ")]:
      continue
    options.set_capability(bstack1lll1ll11l_opy_, bstack1l1l1l11l_opy_[bstack1lll1ll11l_opy_])
  if bstack1l1111_opy_ (u"ࠬࡧࡲࡨࡵࠪউ") in bstack1l1l1l11l_opy_:
    for arg in bstack1l1l1l11l_opy_[bstack1l1111_opy_ (u"࠭ࡡࡳࡩࡶࠫঊ")]:
      options.add_argument(arg)
  if bstack1l1111_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫঋ") in bstack1l1l1l11l_opy_:
    options.bstack11llllll_opy_(bool(bstack1l1l1l11l_opy_[bstack1l1111_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬঌ")]))
def bstack1ll11ll11_opy_(options, bstack1l11l111_opy_):
  for bstack11ll11l1_opy_ in bstack1l11l111_opy_:
    if bstack11ll11l1_opy_ in [bstack1l1111_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭঍"), bstack1l1111_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ঎")]:
      continue
    options._options[bstack11ll11l1_opy_] = bstack1l11l111_opy_[bstack11ll11l1_opy_]
  if bstack1l1111_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨএ") in bstack1l11l111_opy_:
    for bstack11l11l1l1l_opy_ in bstack1l11l111_opy_[bstack1l1111_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩঐ")]:
      options.bstack111ll11l11_opy_(
        bstack11l11l1l1l_opy_, bstack1l11l111_opy_[bstack1l1111_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ঑")][bstack11l11l1l1l_opy_])
  if bstack1l1111_opy_ (u"ࠧࡢࡴࡪࡷࠬ঒") in bstack1l11l111_opy_:
    for arg in bstack1l11l111_opy_[bstack1l1111_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ও")]:
      options.add_argument(arg)
def bstack1111llll1_opy_(options, caps):
  if not hasattr(options, bstack1l1111_opy_ (u"ࠩࡎࡉ࡞࠭ঔ")):
    return
  if options.KEY == bstack1l1111_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨক"):
    options = bstack1l11l1l111_opy_.bstack1l1l1l11l1_opy_(bstack1111l111l_opy_=options, config=CONFIG)
  if options.KEY == bstack1l1111_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩখ") and options.KEY in caps:
    bstack11ll11111l_opy_(options, caps[bstack1l1111_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪগ")])
  elif options.KEY == bstack1l1111_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫঘ") and options.KEY in caps:
    bstack111llll1_opy_(options, caps[bstack1l1111_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬঙ")])
  elif options.KEY == bstack1l1111_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩচ") and options.KEY in caps:
    bstack1llll111_opy_(options, caps[bstack1l1111_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪছ")])
  elif options.KEY == bstack1l1111_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫজ") and options.KEY in caps:
    bstack11l1l1111_opy_(options, caps[bstack1l1111_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬঝ")])
  elif options.KEY == bstack1l1111_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫঞ") and options.KEY in caps:
    bstack1ll11ll11_opy_(options, caps[bstack1l1111_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬট")])
def bstack1l1l1lllll_opy_(caps):
  global bstack1lll11l11l_opy_
  if isinstance(os.environ.get(bstack1l1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨঠ")), str):
    bstack1lll11l11l_opy_ = eval(os.getenv(bstack1l1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩড")))
  if bstack1lll11l11l_opy_:
    if bstack1l1l111ll_opy_() < version.parse(bstack1l1111_opy_ (u"ࠩ࠵࠲࠸࠴࠰ࠨঢ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1l1111_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪণ")
    if bstack1l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩত") in caps:
      browser = caps[bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪথ")]
    elif bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧদ") in caps:
      browser = caps[bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨধ")]
    browser = str(browser).lower()
    if browser == bstack1l1111_opy_ (u"ࠨ࡫ࡳ࡬ࡴࡴࡥࠨন") or browser == bstack1l1111_opy_ (u"ࠩ࡬ࡴࡦࡪࠧ঩"):
      browser = bstack1l1111_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪপ")
    if browser == bstack1l1111_opy_ (u"ࠫࡸࡧ࡭ࡴࡷࡱ࡫ࠬফ"):
      browser = bstack1l1111_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬব")
    if browser not in [bstack1l1111_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ভ"), bstack1l1111_opy_ (u"ࠧࡦࡦࡪࡩࠬম"), bstack1l1111_opy_ (u"ࠨ࡫ࡨࠫয"), bstack1l1111_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩর"), bstack1l1111_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫ঱")]:
      return None
    try:
      package = bstack1l1111_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳ࠰ࡾࢁ࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ল").format(browser)
      name = bstack1l1111_opy_ (u"ࠬࡕࡰࡵ࡫ࡲࡲࡸ࠭঳")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack111l1ll11_opy_(options):
        return None
      for bstack11l1l1l1l1_opy_ in caps.keys():
        options.set_capability(bstack11l1l1l1l1_opy_, caps[bstack11l1l1l1l1_opy_])
      bstack1111llll1_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack11l1l1l1_opy_(options, bstack11ll11ll1l_opy_):
  if not bstack111l1ll11_opy_(options):
    return
  for bstack11l1l1l1l1_opy_ in bstack11ll11ll1l_opy_.keys():
    if bstack11l1l1l1l1_opy_ in bstack111lll11l_opy_:
      continue
    if bstack11l1l1l1l1_opy_ in options._caps and type(options._caps[bstack11l1l1l1l1_opy_]) in [dict, list]:
      options._caps[bstack11l1l1l1l1_opy_] = update(options._caps[bstack11l1l1l1l1_opy_], bstack11ll11ll1l_opy_[bstack11l1l1l1l1_opy_])
    else:
      options.set_capability(bstack11l1l1l1l1_opy_, bstack11ll11ll1l_opy_[bstack11l1l1l1l1_opy_])
  bstack1111llll1_opy_(options, bstack11ll11ll1l_opy_)
  if bstack1l1111_opy_ (u"࠭࡭ࡰࡼ࠽ࡨࡪࡨࡵࡨࡩࡨࡶࡆࡪࡤࡳࡧࡶࡷࠬ঴") in options._caps:
    if options._caps[bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ঵")] and options._caps[bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭শ")].lower() != bstack1l1111_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪষ"):
      del options._caps[bstack1l1111_opy_ (u"ࠪࡱࡴࢀ࠺ࡥࡧࡥࡹ࡬࡭ࡥࡳࡃࡧࡨࡷ࡫ࡳࡴࠩস")]
def bstack11l111lll_opy_(proxy_config):
  if bstack1l1111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨহ") in proxy_config:
    proxy_config[bstack1l1111_opy_ (u"ࠬࡹࡳ࡭ࡒࡵࡳࡽࡿࠧ঺")] = proxy_config[bstack1l1111_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ঻")]
    del (proxy_config[bstack1l1111_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼ়ࠫ")])
  if bstack1l1111_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫঽ") in proxy_config and proxy_config[bstack1l1111_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬা")].lower() != bstack1l1111_opy_ (u"ࠪࡨ࡮ࡸࡥࡤࡶࠪি"):
    proxy_config[bstack1l1111_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧী")] = bstack1l1111_opy_ (u"ࠬࡳࡡ࡯ࡷࡤࡰࠬু")
  if bstack1l1111_opy_ (u"࠭ࡰࡳࡱࡻࡽࡆࡻࡴࡰࡥࡲࡲ࡫࡯ࡧࡖࡴ࡯ࠫূ") in proxy_config:
    proxy_config[bstack1l1111_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪৃ")] = bstack1l1111_opy_ (u"ࠨࡲࡤࡧࠬৄ")
  return proxy_config
def bstack1l1l1111ll_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1l1111_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨ৅") in config:
    return proxy
  config[bstack1l1111_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩ৆")] = bstack11l111lll_opy_(config[bstack1l1111_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪে")])
  if proxy == None:
    proxy = Proxy(config[bstack1l1111_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫৈ")])
  return proxy
def bstack111llll11l_opy_(self):
  global CONFIG
  global bstack11l11ll11l_opy_
  try:
    proxy = bstack1ll1l1l1_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1l1111_opy_ (u"࠭࠮ࡱࡣࡦࠫ৉")):
        proxies = bstack11l1l111l1_opy_(proxy, bstack1l1l11l1_opy_())
        if len(proxies) > 0:
          protocol, bstack11ll111l1l_opy_ = proxies.popitem()
          if bstack1l1111_opy_ (u"ࠢ࠻࠱࠲ࠦ৊") in bstack11ll111l1l_opy_:
            return bstack11ll111l1l_opy_
          else:
            return bstack1l1111_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤো") + bstack11ll111l1l_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1l1111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡶࡲࡰࡺࡼࠤࡺࡸ࡬ࠡ࠼ࠣࡿࢂࠨৌ").format(str(e)))
  return bstack11l11ll11l_opy_(self)
def bstack1lll1l1111_opy_():
  global CONFIG
  return bstack11l1ll111l_opy_(CONFIG) and bstack1111l111_opy_() and bstack11ll111l_opy_() >= version.parse(bstack11ll111l11_opy_)
def bstack11l111l11l_opy_():
  global CONFIG
  return (bstack1l1111_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ্࠭") in CONFIG or bstack1l1111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨৎ") in CONFIG) and bstack111l11ll1_opy_()
def bstack11l111ll1l_opy_(config):
  bstack1l111l1ll1_opy_ = {}
  if bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ৏") in config:
    bstack1l111l1ll1_opy_ = config[bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ৐")]
  if bstack1l1111_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭৑") in config:
    bstack1l111l1ll1_opy_ = config[bstack1l1111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ৒")]
  proxy = bstack1ll1l1l1_opy_(config)
  if proxy:
    if proxy.endswith(bstack1l1111_opy_ (u"ࠩ࠱ࡴࡦࡩࠧ৓")) and os.path.isfile(proxy):
      bstack1l111l1ll1_opy_[bstack1l1111_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭৔")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1l1111_opy_ (u"ࠫ࠳ࡶࡡࡤࠩ৕")):
        proxies = bstack1l11ll11l1_opy_(config, bstack1l1l11l1_opy_())
        if len(proxies) > 0:
          protocol, bstack11ll111l1l_opy_ = proxies.popitem()
          if bstack1l1111_opy_ (u"ࠧࡀ࠯࠰ࠤ৖") in bstack11ll111l1l_opy_:
            parsed_url = urlparse(bstack11ll111l1l_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1l1111_opy_ (u"ࠨ࠺࠰࠱ࠥৗ") + bstack11ll111l1l_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1l111l1ll1_opy_[bstack1l1111_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪ৘")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1l111l1ll1_opy_[bstack1l1111_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡰࡴࡷࠫ৙")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1l111l1ll1_opy_[bstack1l1111_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬ৚")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1l111l1ll1_opy_[bstack1l1111_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭৛")] = str(parsed_url.password)
  return bstack1l111l1ll1_opy_
def bstack11l11l1ll_opy_(config):
  if bstack1l1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩড়") in config:
    return config[bstack1l1111_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪঢ়")]
  return {}
def bstack1111l11l_opy_(caps):
  global bstack11l11111_opy_
  if bstack1l1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ৞") in caps:
    caps[bstack1l1111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨয়")][bstack1l1111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧৠ")] = True
    if bstack11l11111_opy_:
      caps[bstack1l1111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪৡ")][bstack1l1111_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬৢ")] = bstack11l11111_opy_
  else:
    caps[bstack1l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩৣ")] = True
    if bstack11l11111_opy_:
      caps[bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭৤")] = bstack11l11111_opy_
@measure(event_name=EVENTS.bstack11111ll1l_opy_, stage=STAGE.bstack1111lll11_opy_, bstack1l1l111l_opy_=bstack11l1111lll_opy_)
def bstack1l1ll1l1l_opy_():
  global CONFIG
  if not bstack1l111111l1_opy_(CONFIG) or cli.is_enabled(CONFIG):
    return
  if bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ৥") in CONFIG and bstack1l1111lll1_opy_(CONFIG[bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ০")]):
    if (
      bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ১") in CONFIG
      and bstack1l1111lll1_opy_(CONFIG[bstack1l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭২")].get(bstack1l1111_opy_ (u"ࠪࡷࡰ࡯ࡰࡃ࡫ࡱࡥࡷࡿࡉ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡣࡷ࡭ࡴࡴࠧ৩")))
    ):
      logger.debug(bstack1l1111_opy_ (u"ࠦࡑࡵࡣࡢ࡮ࠣࡦ࡮ࡴࡡࡳࡻࠣࡲࡴࡺࠠࡴࡶࡤࡶࡹ࡫ࡤࠡࡣࡶࠤࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤࡪࡴࡡࡣ࡮ࡨࡨࠧ৪"))
      return
    bstack1l111l1ll1_opy_ = bstack11l111ll1l_opy_(CONFIG)
    bstack1lllll1l11_opy_(CONFIG[bstack1l1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ৫")], bstack1l111l1ll1_opy_)
def bstack1lllll1l11_opy_(key, bstack1l111l1ll1_opy_):
  global bstack1l1l1ll1ll_opy_
  logger.info(bstack11ll11l11l_opy_)
  try:
    bstack1l1l1ll1ll_opy_ = Local()
    bstack111ll11ll1_opy_ = {bstack1l1111_opy_ (u"࠭࡫ࡦࡻࠪ৬"): key}
    bstack111ll11ll1_opy_.update(bstack1l111l1ll1_opy_)
    logger.debug(bstack1l1l11ll1l_opy_.format(str(bstack111ll11ll1_opy_)).replace(key, bstack1l1111_opy_ (u"ࠧ࡜ࡔࡈࡈࡆࡉࡔࡆࡆࡠࠫ৭")))
    bstack1l1l1ll1ll_opy_.start(**bstack111ll11ll1_opy_)
    if bstack1l1l1ll1ll_opy_.isRunning():
      logger.info(bstack1ll11l1l1l_opy_)
  except Exception as e:
    bstack11ll11l1l_opy_(bstack1ll11lll1_opy_.format(str(e)))
def bstack111ll1l1l_opy_():
  global bstack1l1l1ll1ll_opy_
  if bstack1l1l1ll1ll_opy_.isRunning():
    logger.info(bstack1lll1lll1l_opy_)
    bstack1l1l1ll1ll_opy_.stop()
  bstack1l1l1ll1ll_opy_ = None
def bstack111ll11lll_opy_(bstack1l11l1l11l_opy_=[]):
  global CONFIG
  bstack111lllllll_opy_ = []
  bstack11lllll1l_opy_ = [bstack1l1111_opy_ (u"ࠨࡱࡶࠫ৮"), bstack1l1111_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬ৯"), bstack1l1111_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧৰ"), bstack1l1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ৱ"), bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ৲"), bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ৳")]
  try:
    for err in bstack1l11l1l11l_opy_:
      bstack11ll1ll11l_opy_ = {}
      for k in bstack11lllll1l_opy_:
        val = CONFIG[bstack1l1111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ৴")][int(err[bstack1l1111_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ৵")])].get(k)
        if val:
          bstack11ll1ll11l_opy_[k] = val
      if(err[bstack1l1111_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ৶")] != bstack1l1111_opy_ (u"ࠪࠫ৷")):
        bstack11ll1ll11l_opy_[bstack1l1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡵࠪ৸")] = {
          err[bstack1l1111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ৹")]: err[bstack1l1111_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ৺")]
        }
        bstack111lllllll_opy_.append(bstack11ll1ll11l_opy_)
  except Exception as e:
    logger.debug(bstack1l1111_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡳࡷࡳࡡࡵࡶ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺ࠺ࠡࠩ৻") + str(e))
  finally:
    return bstack111lllllll_opy_
def bstack1l1l1ll11l_opy_(file_name):
  bstack111l11llll_opy_ = []
  try:
    bstack1ll11llll1_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1ll11llll1_opy_):
      with open(bstack1ll11llll1_opy_) as f:
        bstack11l1111111_opy_ = json.load(f)
        bstack111l11llll_opy_ = bstack11l1111111_opy_
      os.remove(bstack1ll11llll1_opy_)
    return bstack111l11llll_opy_
  except Exception as e:
    logger.debug(bstack1l1111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪ࡮ࡴࡤࡪࡰࡪࠤࡪࡸࡲࡰࡴࠣࡰ࡮ࡹࡴ࠻ࠢࠪৼ") + str(e))
    return bstack111l11llll_opy_
def bstack1l11l111ll_opy_():
  try:
      import time
      from bstack_utils.constants import bstack1111ll11l_opy_, EVENTS
      from bstack_utils.helper import bstack1l1ll11111_opy_, get_host_info, bstack1llllll11l_opy_
      from datetime import datetime
      from filelock import FileLock
      bstack11ll1ll1l1_opy_ = os.path.join(os.getcwd(), bstack1l1111_opy_ (u"ࠩ࡯ࡳ࡬࠭৽"), bstack1l1111_opy_ (u"ࠪ࡯ࡪࡿ࠭࡮ࡧࡷࡶ࡮ࡩࡳ࠯࡬ࡶࡳࡳ࠭৾"))
      data = None
      lock = FileLock(bstack11ll1ll1l1_opy_+bstack1l1111_opy_ (u"ࠦ࠳ࡲ࡯ࡤ࡭ࠥ৿"), timeout=2)
      try:
          with lock:
              with open(bstack11ll1ll1l1_opy_, bstack1l1111_opy_ (u"ࠧࡸࠢ਀"), encoding=bstack1l1111_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧਁ")) as file:
                  data = json.load(file)
      except Exception as e:
          logger.debug(bstack1l1111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡶࡪࡧࡤࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࠦࡦࡪ࡮ࡨ࠾ࠥࢁࡽࠣਂ").format(e))
          return
      if not data:
          return
      def bstack1l11llll1_opy_():
          try:
              config = {
                  bstack1l1111_opy_ (u"ࠣࡪࡨࡥࡩ࡫ࡲࡴࠤਃ"): {
                      bstack1l1111_opy_ (u"ࠤࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠣ਄"): bstack1l1111_opy_ (u"ࠥࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳࠨਅ"),
                  }
              }
              bstack1llll1111_opy_ = datetime.utcnow()
              bstack1111l11l1_opy_ = bstack1llll1111_opy_.strftime(bstack1l1111_opy_ (u"ࠦࠪ࡟࠭ࠦ࡯࠰ࠩࡩ࡚ࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࠯ࠧࡩࠤ࡚࡚ࡃࠣਆ"))
              bstack1l1llll1ll_opy_ = os.environ.get(bstack1l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪਇ")) if os.environ.get(bstack1l1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫਈ")) else bstack1llllll11l_opy_.get_property(bstack1l1111_opy_ (u"ࠢࡴࡦ࡮ࡖࡺࡴࡉࡥࠤਉ"))
              payload = {
                  bstack1l1111_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠧਊ"): bstack1l1111_opy_ (u"ࠤࡶࡨࡰࡥࡥࡷࡧࡱࡸࡸࠨ਋"),
                  bstack1l1111_opy_ (u"ࠥࡨࡦࡺࡡࠣ਌"): {
                      bstack1l1111_opy_ (u"ࠦࡹ࡫ࡳࡵࡪࡸࡦࡤࡻࡵࡪࡦࠥ਍"): bstack1l1llll1ll_opy_,
                      bstack1l1111_opy_ (u"ࠧࡩࡲࡦࡣࡷࡩࡩࡥࡤࡢࡻࠥ਎"): bstack1111l11l1_opy_,
                      bstack1l1111_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡴࡡ࡮ࡧࠥਏ"): bstack1l1111_opy_ (u"ࠢࡔࡆࡎࡊࡪࡧࡴࡶࡴࡨࡔࡪࡸࡦࡰࡴࡰࡥࡳࡩࡥࠣਐ"),
                      bstack1l1111_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟࡫ࡵࡲࡲࠧ਑"): {
                          bstack1l1111_opy_ (u"ࠤࡰࡩࡦࡹࡵࡳࡧࡶࠦ਒"): data,
                          bstack1l1111_opy_ (u"ࠥࡷࡩࡱࡒࡶࡰࡌࡨࠧਓ"): bstack1llllll11l_opy_.get_property(bstack1l1111_opy_ (u"ࠦࡸࡪ࡫ࡓࡷࡱࡍࡩࠨਔ"))
                      },
                      bstack1l1111_opy_ (u"ࠧࡻࡳࡦࡴࡢࡨࡦࡺࡡࠣਕ"): bstack1llllll11l_opy_.get_property(bstack1l1111_opy_ (u"ࠨࡵࡴࡧࡵࡒࡦࡳࡥࠣਖ")),
                      bstack1l1111_opy_ (u"ࠢࡩࡱࡶࡸࡤ࡯࡮ࡧࡱࠥਗ"): get_host_info()
                  }
              }
              bstack111111l1l_opy_ = bstack11ll1l11_opy_(cli.config, [bstack1l1111_opy_ (u"ࠣࡣࡳ࡭ࡸࠨਘ"), bstack1l1111_opy_ (u"ࠤࡨࡨࡸࡏ࡮ࡴࡶࡵࡹࡲ࡫࡮ࡵࡣࡷ࡭ࡴࡴࠢਙ"), bstack1l1111_opy_ (u"ࠥࡥࡵ࡯ࠢਚ")], bstack1111ll11l_opy_)
              response = bstack1l1ll11111_opy_(bstack1l1111_opy_ (u"ࠦࡕࡕࡓࡕࠤਛ"), bstack111111l1l_opy_, payload, config)
              if response.status_code >= 200 and response.status_code < 300:
                  logger.info(bstack1l1111_opy_ (u"ࠧࡑࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵࠣࡷࡪࡴࡴࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡵࡱࠣࡿࢂࠨਜ").format(bstack1111ll11l_opy_))
              else:
                  logger.debug(bstack1l1111_opy_ (u"ࠨࡋࡦࡻࠣࡱࡪࡺࡲࡪࡥࡶࠤࡷ࡫ࡱࡶࡧࡶࡸࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪࠣࡷࡹࡧࡴࡶࡵࠣࡿࢂࠨਝ").format(response.status_code))
          except Exception as e:
              logger.debug(bstack1l1111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡴࡤࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࡀࠠࡼࡿࠥਞ").format(e))
      bstack1l11llll1_opy_()
      bstack1l111llll_opy_(bstack11ll1ll1l1_opy_, logger)
  except Exception as e:
      logger.debug(bstack1l1111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡴࡤࡠ࡭ࡨࡽࡤࡳࡥࡵࡴ࡬ࡧࡸࡀࠠࡼࡿࠥਟ").format(e))
def bstack1l111l11_opy_():
  bstack1111ll1l_opy_ = bstack1l1111_opy_ (u"ࠤࠥਠ")
  global bstack1111lllll_opy_
  global bstack1l1lll11ll_opy_
  global bstack1l11l1ll1_opy_
  global bstack111l1lll1_opy_
  global ROBOT_PYTHON_ERRORS
  global bstack1ll11111l_opy_
  global CONFIG
  bstack11l11l11l_opy_ = os.environ.get(bstack1l1111_opy_ (u"ࠪࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡕࡔࡇࡇࠫਡ"))
  if bstack11l11l11l_opy_ not in [bstack1l1111_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬਢ")]:
    bstack1111ll1l_opy_ = bstack11ll111lll_opy_.bstack111llllll_opy_(EVENTS.bstack1ll1l1111l_opy_)
  percy.shutdown()
  if bstack1111lllll_opy_:
    logger.warning(bstack11ll1l11l_opy_.format(str(bstack1111lllll_opy_)))
  else:
    try:
      bstack11l1l11lll_opy_ = bstack11lllll1_opy_(bstack1l1111_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫਣ"), logger)
      if bstack11l1l11lll_opy_.get(bstack1l1111_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫਤ")) and bstack11l1l11lll_opy_.get(bstack1l1111_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬਥ")).get(bstack1l1111_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪਦ")):
        logger.warning(bstack11ll1l11l_opy_.format(str(bstack11l1l11lll_opy_[bstack1l1111_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧਧ")][bstack1l1111_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬਨ")])))
    except Exception as e:
      logger.error(e)
  if cli.is_running():
    bstack1ll1111ll_opy_.invoke(bstack1ll1l11l_opy_.bstack1l1l11ll11_opy_)
  logger.info(bstack1l11ll1l_opy_)
  global bstack1l1l1ll1ll_opy_
  if bstack1l1l1ll1ll_opy_:
    bstack111ll1l1l_opy_()
  try:
    with bstack11l1l11111_opy_:
      bstack11l1l1ll_opy_ = bstack1l1lll11ll_opy_.copy()
    for driver in bstack11l1l1ll_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack11l111l111_opy_)
  ROBOT_PYTHON_ERRORS = []
  if bstack1ll11111l_opy_ == bstack1l1111_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ਩"):
    ROBOT_PYTHON_ERRORS = bstack1l1l1ll11l_opy_(bstack1l1111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ਪ"))
  if bstack1ll11111l_opy_ == bstack1l1111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ਫ") and len(bstack111l1lll1_opy_) == 0:
    bstack111l1lll1_opy_ = bstack1l1l1ll11l_opy_(bstack1l1111_opy_ (u"ࠧࡱࡹࡢࡴࡾࡺࡥࡴࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬਬ"))
    if len(bstack111l1lll1_opy_) == 0:
      bstack111l1lll1_opy_ = bstack1l1l1ll11l_opy_(bstack1l1111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡲࡳࡴࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧਭ"))
  bstack111l11l11l_opy_ = bstack1l1111_opy_ (u"ࠩࠪਮ")
  if len(bstack1l11l1ll1_opy_) > 0:
    bstack111l11l11l_opy_ = bstack111ll11lll_opy_(bstack1l11l1ll1_opy_)
  elif len(bstack111l1lll1_opy_) > 0:
    bstack111l11l11l_opy_ = bstack111ll11lll_opy_(bstack111l1lll1_opy_)
  elif len(ROBOT_PYTHON_ERRORS) > 0:
    bstack111l11l11l_opy_ = bstack111ll11lll_opy_(ROBOT_PYTHON_ERRORS)
  elif len(bstack111l1ll1ll_opy_) > 0:
    bstack111l11l11l_opy_ = bstack111ll11lll_opy_(bstack111l1ll1ll_opy_)
  if bstack11l11l11l_opy_ not in [bstack1l1111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫਯ")]:
    def bstack1ll1llllll_opy_():
      try:
        if bstack11l11l11l_opy_ in [bstack1l1111_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪਰ"), bstack1l1111_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ਱")]:
          bstack1ll111l1l1_opy_()
      except Exception as e:
        logger.debug(bstack1l1111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡨ࡬ࡲࡦࡲ࡟ࡦࡺࡨࡧࡺࡺࡩࡰࡰ࠽ࠤࢀࢃࠢਲ").format(e))
    def bstack1ll11ll11l_opy_():
      try:
        if bool(bstack111l11l11l_opy_):
          bstack1ll1ll1ll1_opy_(bstack111l11l11l_opy_)
        else:
          bstack1ll1ll1ll1_opy_()
      except Exception as e:
        logger.debug(bstack1l1111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡳࡦࡰࡧ࡭ࡳ࡭ࠠࡦࡸࡨࡲࡹࡀࠠࡼࡿࠥਲ਼").format(e))
    def bstack1ll1l1lll1_opy_():
      try:
        bstack111llll1ll_opy_.bstack1l1111ll_opy_(CONFIG)
      except Exception as e:
        logger.debug(bstack1l1111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡴࡧࡱࡨ࡮ࡴࡧࠡ࡮ࡲ࡫ࡸࡀࠠࡼࡿࠥ਴").format(e))
    bstack11l11ll1_opy_ = threading.Thread(target=bstack1ll1llllll_opy_)
    bstack1l1l1111l_opy_ = threading.Thread(target=bstack1ll11ll11l_opy_)
    bstack1llllllll1_opy_ = threading.Thread(target=bstack1ll1l1lll1_opy_)
    threads = [bstack11l11ll1_opy_, bstack1l1l1111l_opy_, bstack1llllllll1_opy_]
    for thread in threads:
      try:
        thread.start()
      except Exception as e:
        logger.debug(bstack1l1111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡵࡷࡥࡷࡺࡩ࡯ࡩࠣࡸ࡭ࡸࡥࡢࡦࠣࡿࢂࡀࠠࡼࡿࠥਵ").format(thread.name, e))
    for thread in threads:
      try:
        thread.join()
      except Exception as e:
        logger.debug(bstack1l1111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡭ࡳ࡮ࡴࡩ࡯ࡩࠣࡸ࡭ࡸࡥࡢࡦࠣࡿࢂࡀࠠࡼࡿࠥਸ਼").format(thread.name, e))
    bstack1l111llll_opy_(bstack11l111lll1_opy_, logger)
  if bstack11l11l11l_opy_ not in [bstack1l1111_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ਷")]:
    bstack11ll111lll_opy_.end(EVENTS.bstack1ll1l1111l_opy_.value, bstack1111ll1l_opy_ + bstack1l1111_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧਸ"), bstack1111ll1l_opy_ + bstack1l1111_opy_ (u"ࠨ࠺ࡦࡰࡧࠦਹ"), status=True, failure=None, test_name=None)
    bstack1l11l111ll_opy_()
    bstack111llll1ll_opy_.bstack1111ll1ll_opy_()
    logging.shutdown()
  if len(ROBOT_PYTHON_ERRORS) > 0:
    sys.exit(len(ROBOT_PYTHON_ERRORS))
def bstack11llll1ll1_opy_(bstack11l1l1ll11_opy_, frame):
  global bstack1llllll11l_opy_
  logger.error(bstack11llll1ll_opy_)
  bstack1llllll11l_opy_.bstack11l1l111ll_opy_(bstack1l1111_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡏࡱࠪ਺"), bstack11l1l1ll11_opy_)
  if hasattr(signal, bstack1l1111_opy_ (u"ࠨࡕ࡬࡫ࡳࡧ࡬ࡴࠩ਻")):
    bstack1llllll11l_opy_.bstack11l1l111ll_opy_(bstack1l1111_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭਼ࠩ"), signal.Signals(bstack11l1l1ll11_opy_).name)
  else:
    bstack1llllll11l_opy_.bstack11l1l111ll_opy_(bstack1l1111_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪ਽"), bstack1l1111_opy_ (u"ࠫࡘࡏࡇࡖࡐࡎࡒࡔ࡝ࡎࠨਾ"))
  if cli.is_running():
    bstack1ll1111ll_opy_.invoke(bstack1ll1l11l_opy_.bstack1l1l11ll11_opy_)
  bstack11l11l11l_opy_ = os.environ.get(bstack1l1111_opy_ (u"ࠬࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉ࠭ਿ"))
  if bstack11l11l11l_opy_ == bstack1l1111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ੀ") and not cli.is_enabled(CONFIG):
    bstack11l11111l_opy_.stop(bstack1llllll11l_opy_.get_property(bstack1l1111_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡔ࡫ࡪࡲࡦࡲࠧੁ")))
  bstack1l111l11_opy_()
  sys.exit(1)
def bstack11ll11l1l_opy_(err):
  logger.critical(bstack11ll1llll_opy_.format(str(err)))
  bstack1ll1ll1ll1_opy_(bstack11ll1llll_opy_.format(str(err)), True)
  atexit.unregister(bstack1l111l11_opy_)
  bstack1ll111l1l1_opy_()
  sys.exit(1)
def bstack111l1l11_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1ll1ll1ll1_opy_(message, True)
  atexit.unregister(bstack1l111l11_opy_)
  bstack1ll111l1l1_opy_()
  sys.exit(1)
def bstack1l1lll1l1l_opy_():
  global CONFIG
  global bstack11l1111l1_opy_
  global bstack1111ll1l1_opy_
  global bstack1l1llll1l1_opy_
  CONFIG = bstack11l1l1ll1l_opy_()
  load_dotenv(CONFIG.get(bstack1l1111_opy_ (u"ࠨࡧࡱࡺࡋ࡯࡬ࡦࠩੂ")))
  bstack11llll11l_opy_()
  bstack1llll11l1_opy_()
  CONFIG = bstack1111l1l1l_opy_(CONFIG)
  update(CONFIG, bstack1111ll1l1_opy_)
  update(CONFIG, bstack11l1111l1_opy_)
  if not cli.is_enabled(CONFIG):
    CONFIG = bstack11lllllll_opy_(CONFIG)
  bstack1l1llll1l1_opy_ = bstack1l111111l1_opy_(CONFIG)
  os.environ[bstack1l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬ੃")] = bstack1l1llll1l1_opy_.__str__().lower()
  bstack1llllll11l_opy_.bstack11l1l111ll_opy_(bstack1l1111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫ੄"), bstack1l1llll1l1_opy_)
  if (bstack1l1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ੅") in CONFIG and bstack1l1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ੆") in bstack11l1111l1_opy_) or (
          bstack1l1111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩੇ") in CONFIG and bstack1l1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪੈ") not in bstack1111ll1l1_opy_):
    if os.getenv(bstack1l1111_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬ੉")):
      CONFIG[bstack1l1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ੊")] = os.getenv(bstack1l1111_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧੋ"))
    else:
      if not CONFIG.get(bstack1l1111_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠢੌ"), bstack1l1111_opy_ (u"ࠧࠨ੍")) in bstack111ll1111_opy_:
        bstack1lll11lll_opy_()
  elif (bstack1l1111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ੎") not in CONFIG and bstack1l1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ੏") in CONFIG) or (
          bstack1l1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ੐") in bstack1111ll1l1_opy_ and bstack1l1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬੑ") not in bstack11l1111l1_opy_):
    del (CONFIG[bstack1l1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ੒")])
  if bstack111111ll1_opy_(CONFIG):
    bstack11ll11l1l_opy_(bstack1ll11lll_opy_)
  Config.bstack111ll1lll1_opy_().bstack11l1l111ll_opy_(bstack1l1111_opy_ (u"ࠦࡺࡹࡥࡳࡐࡤࡱࡪࠨ੓"), CONFIG[bstack1l1111_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ੔")])
  bstack1l1lllll_opy_()
  bstack1lll1lllll_opy_()
  if bstack1lll11l11l_opy_ and not CONFIG.get(bstack1l1111_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠤ੕"), bstack1l1111_opy_ (u"ࠢࠣ੖")) in bstack111ll1111_opy_:
    CONFIG[bstack1l1111_opy_ (u"ࠨࡣࡳࡴࠬ੗")] = bstack11ll1l1l11_opy_(CONFIG)
    logger.info(bstack1l11l1l1l_opy_.format(CONFIG[bstack1l1111_opy_ (u"ࠩࡤࡴࡵ࠭੘")]))
  if not bstack1l1llll1l1_opy_:
    CONFIG[bstack1l1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ਖ਼")] = [{}]
def bstack1lll1l1ll_opy_(config, bstack1111ll111_opy_):
  global CONFIG
  global bstack1lll11l11l_opy_
  CONFIG = config
  bstack1lll11l11l_opy_ = bstack1111ll111_opy_
def bstack1lll1lllll_opy_():
  global CONFIG
  global bstack1lll11l11l_opy_
  if bstack1l1111_opy_ (u"ࠫࡦࡶࡰࠨਗ਼") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack111l1l11_opy_(e, bstack11lll11lll_opy_)
    bstack1lll11l11l_opy_ = True
    bstack1llllll11l_opy_.bstack11l1l111ll_opy_(bstack1l1111_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫਜ਼"), True)
def bstack11ll1l1l11_opy_(config):
  bstack1lll1ll1_opy_ = bstack1l1111_opy_ (u"࠭ࠧੜ")
  app = config[bstack1l1111_opy_ (u"ࠧࡢࡲࡳࠫ੝")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1l1ll1l1l1_opy_:
      if os.path.exists(app):
        bstack1lll1ll1_opy_ = bstack1ll111l111_opy_(config, app)
      elif bstack1l111l1l_opy_(app):
        bstack1lll1ll1_opy_ = app
      else:
        bstack11ll11l1l_opy_(bstack1l1l1ll11_opy_.format(app))
    else:
      if bstack1l111l1l_opy_(app):
        bstack1lll1ll1_opy_ = app
      elif os.path.exists(app):
        bstack1lll1ll1_opy_ = bstack1ll111l111_opy_(app)
      else:
        bstack11ll11l1l_opy_(bstack111l111ll_opy_)
  else:
    if len(app) > 2:
      bstack11ll11l1l_opy_(bstack1l1lllll11_opy_)
    elif len(app) == 2:
      if bstack1l1111_opy_ (u"ࠨࡲࡤࡸ࡭࠭ਫ਼") in app and bstack1l1111_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ੟") in app:
        if os.path.exists(app[bstack1l1111_opy_ (u"ࠪࡴࡦࡺࡨࠨ੠")]):
          bstack1lll1ll1_opy_ = bstack1ll111l111_opy_(config, app[bstack1l1111_opy_ (u"ࠫࡵࡧࡴࡩࠩ੡")], app[bstack1l1111_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨ੢")])
        else:
          bstack11ll11l1l_opy_(bstack1l1l1ll11_opy_.format(app))
      else:
        bstack11ll11l1l_opy_(bstack1l1lllll11_opy_)
    else:
      for key in app:
        if key in bstack1l11lll11_opy_:
          if key == bstack1l1111_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ੣"):
            if os.path.exists(app[key]):
              bstack1lll1ll1_opy_ = bstack1ll111l111_opy_(config, app[key])
            else:
              bstack11ll11l1l_opy_(bstack1l1l1ll11_opy_.format(app))
          else:
            bstack1lll1ll1_opy_ = app[key]
        else:
          bstack11ll11l1l_opy_(bstack11l1ll11ll_opy_)
  return bstack1lll1ll1_opy_
def bstack1l111l1l_opy_(bstack1lll1ll1_opy_):
  import re
  bstack1l11l1lll1_opy_ = re.compile(bstack1l1111_opy_ (u"ࡲࠣࡠ࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯ࠪࠢ੤"))
  bstack111lllll1l_opy_ = re.compile(bstack1l1111_opy_ (u"ࡳࠤࡡ࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰࠯࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭ࠨࠧ੥"))
  if bstack1l1111_opy_ (u"ࠩࡥࡷ࠿࠵࠯ࠨ੦") in bstack1lll1ll1_opy_ or re.fullmatch(bstack1l11l1lll1_opy_, bstack1lll1ll1_opy_) or re.fullmatch(bstack111lllll1l_opy_, bstack1lll1ll1_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack1lll1l11l_opy_, stage=STAGE.bstack1111lll11_opy_, bstack1l1l111l_opy_=bstack11l1111lll_opy_)
def bstack1ll111l111_opy_(config, path, bstack1lllll1ll_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1l1111_opy_ (u"ࠪࡶࡧ࠭੧")).read()).hexdigest()
  bstack1ll1l11lll_opy_ = bstack111l11l1l1_opy_(md5_hash)
  bstack1lll1ll1_opy_ = None
  if bstack1ll1l11lll_opy_:
    logger.info(bstack1l1111ll1_opy_.format(bstack1ll1l11lll_opy_, md5_hash))
    return bstack1ll1l11lll_opy_
  bstack1ll1lll11l_opy_ = datetime.datetime.now()
  bstack1ll11l1111_opy_ = MultipartEncoder(
    fields={
      bstack1l1111_opy_ (u"ࠫ࡫࡯࡬ࡦࠩ੨"): (os.path.basename(path), open(os.path.abspath(path), bstack1l1111_opy_ (u"ࠬࡸࡢࠨ੩")), bstack1l1111_opy_ (u"࠭ࡴࡦࡺࡷ࠳ࡵࡲࡡࡪࡰࠪ੪")),
      bstack1l1111_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪ੫"): bstack1lllll1ll_opy_
    }
  )
  response = requests.post(bstack11l1ll1l1_opy_, data=bstack1ll11l1111_opy_,
                           headers={bstack1l1111_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ੬"): bstack1ll11l1111_opy_.content_type},
                           auth=(config[bstack1l1111_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ੭")], config[bstack1l1111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭੮")]))
  try:
    res = json.loads(response.text)
    bstack1lll1ll1_opy_ = res[bstack1l1111_opy_ (u"ࠫࡦࡶࡰࡠࡷࡵࡰࠬ੯")]
    logger.info(bstack11l11ll11_opy_.format(bstack1lll1ll1_opy_))
    bstack11ll1l1lll_opy_(md5_hash, bstack1lll1ll1_opy_)
    cli.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽ࡹࡵࡲ࡯ࡢࡦࡢࡥࡵࡶࠢੰ"), datetime.datetime.now() - bstack1ll1lll11l_opy_)
  except ValueError as err:
    bstack11ll11l1l_opy_(bstack11lllll1ll_opy_.format(str(err)))
  return bstack1lll1ll1_opy_
def bstack1l1lllll_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack11ll1l1ll1_opy_
  bstack1l11l1ll_opy_ = 1
  bstack1l111l1l11_opy_ = 1
  if bstack1l1111_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ੱ") in CONFIG:
    bstack1l111l1l11_opy_ = CONFIG[bstack1l1111_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧੲ")]
  else:
    bstack1l111l1l11_opy_ = bstack1llllll1ll_opy_(framework_name, args) or 1
  if bstack1l1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫੳ") in CONFIG:
    bstack1l11l1ll_opy_ = len(CONFIG[bstack1l1111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬੴ")])
  bstack11ll1l1ll1_opy_ = int(bstack1l111l1l11_opy_) * int(bstack1l11l1ll_opy_)
def bstack1llllll1ll_opy_(framework_name, args):
  if framework_name == bstack11llll11ll_opy_ and args and bstack1l1111_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨੵ") in args:
      bstack1l1l1l111_opy_ = args.index(bstack1l1111_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩ੶"))
      return int(args[bstack1l1l1l111_opy_ + 1]) or 1
  return 1
def bstack111l11l1l1_opy_(md5_hash):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l1111_opy_ (u"ࠬ࡬ࡩ࡭ࡧ࡯ࡳࡨࡱࠠ࡯ࡱࡷࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠬࠡࡷࡶ࡭ࡳ࡭ࠠࡣࡣࡶ࡭ࡨࠦࡦࡪ࡮ࡨࠤࡴࡶࡥࡳࡣࡷ࡭ࡴࡴࡳࠨ੷"))
    bstack1ll11l1ll1_opy_ = os.path.join(os.path.expanduser(bstack1l1111_opy_ (u"࠭ࡾࠨ੸")), bstack1l1111_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ੹"), bstack1l1111_opy_ (u"ࠨࡣࡳࡴ࡚ࡶ࡬ࡰࡣࡧࡑࡉ࠻ࡈࡢࡵ࡫࠲࡯ࡹ࡯࡯ࠩ੺"))
    if os.path.exists(bstack1ll11l1ll1_opy_):
      try:
        bstack1llll1111l_opy_ = json.load(open(bstack1ll11l1ll1_opy_, bstack1l1111_opy_ (u"ࠩࡵࡦࠬ੻")))
        if md5_hash in bstack1llll1111l_opy_:
          bstack1l1ll1ll1l_opy_ = bstack1llll1111l_opy_[md5_hash]
          bstack11l111l1ll_opy_ = datetime.datetime.now()
          bstack11ll1l1ll_opy_ = datetime.datetime.strptime(bstack1l1ll1ll1l_opy_[bstack1l1111_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭੼")], bstack1l1111_opy_ (u"ࠫࠪࡪ࠯ࠦ࡯࠲ࠩ࡞ࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨ੽"))
          if (bstack11l111l1ll_opy_ - bstack11ll1l1ll_opy_).days > 30:
            return None
          elif version.parse(str(__version__)) > version.parse(bstack1l1ll1ll1l_opy_[bstack1l1111_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ੾")]):
            return None
          return bstack1l1ll1ll1l_opy_[bstack1l1111_opy_ (u"࠭ࡩࡥࠩ੿")]
      except Exception as e:
        logger.debug(bstack1l1111_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡲࡦࡣࡧ࡭ࡳ࡭ࠠࡎࡆ࠸ࠤ࡭ࡧࡳࡩࠢࡩ࡭ࡱ࡫࠺ࠡࡽࢀࠫ઀").format(str(e)))
    return None
  bstack1ll11l1ll1_opy_ = os.path.join(os.path.expanduser(bstack1l1111_opy_ (u"ࠨࢀࠪઁ")), bstack1l1111_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩં"), bstack1l1111_opy_ (u"ࠪࡥࡵࡶࡕࡱ࡮ࡲࡥࡩࡓࡄ࠶ࡊࡤࡷ࡭࠴ࡪࡴࡱࡱࠫઃ"))
  lock_file = bstack1ll11l1ll1_opy_ + bstack1l1111_opy_ (u"ࠫ࠳ࡲ࡯ࡤ࡭ࠪ઄")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack1ll11l1ll1_opy_):
        with open(bstack1ll11l1ll1_opy_, bstack1l1111_opy_ (u"ࠬࡸࠧઅ")) as f:
          content = f.read().strip()
          if content:
            bstack1llll1111l_opy_ = json.loads(content)
            if md5_hash in bstack1llll1111l_opy_:
              bstack1l1ll1ll1l_opy_ = bstack1llll1111l_opy_[md5_hash]
              bstack11l111l1ll_opy_ = datetime.datetime.now()
              bstack11ll1l1ll_opy_ = datetime.datetime.strptime(bstack1l1ll1ll1l_opy_[bstack1l1111_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩઆ")], bstack1l1111_opy_ (u"ࠧࠦࡦ࠲ࠩࡲ࠵࡚ࠥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫઇ"))
              if (bstack11l111l1ll_opy_ - bstack11ll1l1ll_opy_).days > 30:
                return None
              elif version.parse(str(__version__)) > version.parse(bstack1l1ll1ll1l_opy_[bstack1l1111_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ઈ")]):
                return None
              return bstack1l1ll1ll1l_opy_[bstack1l1111_opy_ (u"ࠩ࡬ࡨࠬઉ")]
      return None
  except Exception as e:
    logger.debug(bstack1l1111_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡺ࡭ࡹ࡮ࠠࡧ࡫࡯ࡩࠥࡲ࡯ࡤ࡭࡬ࡲ࡬ࠦࡦࡰࡴࠣࡑࡉ࠻ࠠࡩࡣࡶ࡬࠿ࠦࡻࡾࠩઊ").format(str(e)))
    return None
def bstack11ll1l1lll_opy_(md5_hash, bstack1lll1ll1_opy_):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l1111_opy_ (u"ࠫ࡫࡯࡬ࡦ࡮ࡲࡧࡰࠦ࡮ࡰࡶࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪ࠲ࠠࡶࡵ࡬ࡲ࡬ࠦࡢࡢࡵ࡬ࡧࠥ࡬ࡩ࡭ࡧࠣࡳࡵ࡫ࡲࡢࡶ࡬ࡳࡳࡹࠧઋ"))
    bstack1l1llllll1_opy_ = os.path.join(os.path.expanduser(bstack1l1111_opy_ (u"ࠬࢄࠧઌ")), bstack1l1111_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ઍ"))
    if not os.path.exists(bstack1l1llllll1_opy_):
      os.makedirs(bstack1l1llllll1_opy_)
    bstack1ll11l1ll1_opy_ = os.path.join(os.path.expanduser(bstack1l1111_opy_ (u"ࠧࡿࠩ઎")), bstack1l1111_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨએ"), bstack1l1111_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪઐ"))
    bstack1llll11111_opy_ = {
      bstack1l1111_opy_ (u"ࠪ࡭ࡩ࠭ઑ"): bstack1lll1ll1_opy_,
      bstack1l1111_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ઒"): datetime.datetime.strftime(datetime.datetime.now(), bstack1l1111_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩઓ")),
      bstack1l1111_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫઔ"): str(__version__)
    }
    try:
      bstack1llll1111l_opy_ = {}
      if os.path.exists(bstack1ll11l1ll1_opy_):
        bstack1llll1111l_opy_ = json.load(open(bstack1ll11l1ll1_opy_, bstack1l1111_opy_ (u"ࠧࡳࡤࠪક")))
      bstack1llll1111l_opy_[md5_hash] = bstack1llll11111_opy_
      with open(bstack1ll11l1ll1_opy_, bstack1l1111_opy_ (u"ࠣࡹ࠮ࠦખ")) as outfile:
        json.dump(bstack1llll1111l_opy_, outfile)
    except Exception as e:
      logger.debug(bstack1l1111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡷࡳࡨࡦࡺࡩ࡯ࡩࠣࡑࡉ࠻ࠠࡩࡣࡶ࡬ࠥ࡬ࡩ࡭ࡧ࠽ࠤࢀࢃࠧગ").format(str(e)))
    return
  bstack1l1llllll1_opy_ = os.path.join(os.path.expanduser(bstack1l1111_opy_ (u"ࠪࢂࠬઘ")), bstack1l1111_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫઙ"))
  if not os.path.exists(bstack1l1llllll1_opy_):
    os.makedirs(bstack1l1llllll1_opy_)
  bstack1ll11l1ll1_opy_ = os.path.join(os.path.expanduser(bstack1l1111_opy_ (u"ࠬࢄࠧચ")), bstack1l1111_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭છ"), bstack1l1111_opy_ (u"ࠧࡢࡲࡳ࡙ࡵࡲ࡯ࡢࡦࡐࡈ࠺ࡎࡡࡴࡪ࠱࡮ࡸࡵ࡮ࠨજ"))
  lock_file = bstack1ll11l1ll1_opy_ + bstack1l1111_opy_ (u"ࠨ࠰࡯ࡳࡨࡱࠧઝ")
  bstack1llll11111_opy_ = {
    bstack1l1111_opy_ (u"ࠩ࡬ࡨࠬઞ"): bstack1lll1ll1_opy_,
    bstack1l1111_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ટ"): datetime.datetime.strftime(datetime.datetime.now(), bstack1l1111_opy_ (u"ࠫࠪࡪ࠯ࠦ࡯࠲ࠩ࡞ࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨઠ")),
    bstack1l1111_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪડ"): str(__version__)
  }
  try:
    with FileLock(lock_file, timeout=10):
      bstack1llll1111l_opy_ = {}
      if os.path.exists(bstack1ll11l1ll1_opy_):
        with open(bstack1ll11l1ll1_opy_, bstack1l1111_opy_ (u"࠭ࡲࠨઢ")) as f:
          content = f.read().strip()
          if content:
            bstack1llll1111l_opy_ = json.loads(content)
      bstack1llll1111l_opy_[md5_hash] = bstack1llll11111_opy_
      with open(bstack1ll11l1ll1_opy_, bstack1l1111_opy_ (u"ࠢࡸࠤણ")) as outfile:
        json.dump(bstack1llll1111l_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1l1111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡸ࡫ࡷ࡬ࠥ࡬ࡩ࡭ࡧࠣࡰࡴࡩ࡫ࡪࡰࡪࠤ࡫ࡵࡲࠡࡏࡇ࠹ࠥ࡮ࡡࡴࡪࠣࡹࡵࡪࡡࡵࡧ࠽ࠤࢀࢃࠧત").format(str(e)))
def bstack1l111l111_opy_(self):
  return
def bstack111ll1ll1l_opy_(self):
  return
def bstack11llll111_opy_():
  global bstack1lllll1lll_opy_
  bstack1lllll1lll_opy_ = True
def bstack111ll11111_opy_(self):
  global bstack111l111l_opy_
  global bstack11lll1llll_opy_
  global bstack1l111111l_opy_
  bstack1ll1111lll_opy_ = bstack11ll111lll_opy_.bstack111llllll_opy_(EVENTS.bstack11lll1ll1l_opy_)
  try:
    if bstack1l1111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩથ") in bstack111l111l_opy_ and self.session_id != None and bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧદ"), bstack1l1111_opy_ (u"ࠫࠬધ")) != bstack1l1111_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ન"):
      bstack1ll11l11l1_opy_ = bstack1l1111_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭઩") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1l1111_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧપ")
      if bstack1ll11l11l1_opy_ == bstack1l1111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨફ"):
        bstack11lll11l11_opy_(logger)
      if self != None:
        bstack1l111l1ll_opy_(self, bstack1ll11l11l1_opy_, bstack1l1111_opy_ (u"ࠩ࠯ࠤࠬબ").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack1l1111_opy_ (u"ࠪࠫભ")
    if bstack1l1111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫમ") in bstack111l111l_opy_ and getattr(threading.current_thread(), bstack1l1111_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫય"), None):
      bstack111ll1l1ll_opy_.bstack1l1l1l1ll_opy_(self, bstack11lll111_opy_, logger, wait=True)
    if bstack1l1111_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ર") in bstack111l111l_opy_:
      bstack1l111llll1_opy_.bstack1l1l1l1lll_opy_(self)
    bstack11ll111lll_opy_.end(EVENTS.bstack11lll1ll1l_opy_.value, bstack1ll1111lll_opy_ + bstack1l1111_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ઱"), bstack1ll1111lll_opy_ + bstack1l1111_opy_ (u"ࠣ࠼ࡨࡲࡩࠨલ"), status=True, failure=None, test_name=None)
  except Exception as e:
    logger.debug(bstack1l1111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࠥળ") + str(e))
    bstack11ll111lll_opy_.end(EVENTS.bstack11lll1ll1l_opy_.value, bstack1ll1111lll_opy_ + bstack1l1111_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ઴"), bstack1ll1111lll_opy_ + bstack1l1111_opy_ (u"ࠦ࠿࡫࡮ࡥࠤવ"), status=False, failure=str(e), test_name=None)
  bstack1l111111l_opy_(self)
  self.session_id = None
def bstack1lll1l1ll1_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack1l1lll11_opy_
    global bstack111l111l_opy_
    command_executor = kwargs.get(bstack1l1111_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠨશ"), bstack1l1111_opy_ (u"࠭ࠧષ"))
    bstack111ll1l111_opy_ = False
    if type(command_executor) == str and bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪસ") in command_executor:
      bstack111ll1l111_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫહ") in str(getattr(command_executor, bstack1l1111_opy_ (u"ࠩࡢࡹࡷࡲࠧ઺"), bstack1l1111_opy_ (u"ࠪࠫ઻"))):
      bstack111ll1l111_opy_ = True
    else:
      kwargs = bstack1l11l1l111_opy_.bstack1l1l1l11l1_opy_(bstack1111l111l_opy_=kwargs, config=CONFIG)
      return bstack1llll11l1l_opy_(self, *args, **kwargs)
    if bstack111ll1l111_opy_:
      bstack1l1111lll_opy_ = bstack11l11ll111_opy_.bstack1l11l11lll_opy_(CONFIG, bstack111l111l_opy_)
      if kwargs.get(bstack1l1111_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷ઼ࠬ")):
        kwargs[bstack1l1111_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ઽ")] = bstack1l1lll11_opy_(kwargs[bstack1l1111_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧા")], bstack111l111l_opy_, CONFIG, bstack1l1111lll_opy_)
      elif kwargs.get(bstack1l1111_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧિ")):
        kwargs[bstack1l1111_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨી")] = bstack1l1lll11_opy_(kwargs[bstack1l1111_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩુ")], bstack111l111l_opy_, CONFIG, bstack1l1111lll_opy_)
  except Exception as e:
    logger.error(bstack1l1111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡘࡊࡋࠡࡥࡤࡴࡸࡀࠠࡼࡿࠥૂ").format(str(e)))
  return bstack1llll11l1l_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack11ll111l1_opy_, stage=STAGE.bstack1111lll11_opy_, bstack1l1l111l_opy_=bstack11l1111lll_opy_)
def bstack11llll1lll_opy_(self, command_executor=bstack1l1111_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳࠶࠸࠷࠯࠲࠱࠴࠳࠷࠺࠵࠶࠷࠸ࠧૃ"), *args, **kwargs):
  global bstack11lll1llll_opy_
  global bstack1l1lll11ll_opy_
  bstack1l11ll1ll_opy_ = bstack1lll1l1ll1_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack1lll11ll11_opy_.on():
    return bstack1l11ll1ll_opy_
  try:
    logger.debug(bstack1l1111_opy_ (u"ࠬࡉ࡯࡮࡯ࡤࡲࡩࠦࡅࡹࡧࡦࡹࡹࡵࡲࠡࡹ࡫ࡩࡳࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥ࡬ࡡ࡭ࡵࡨࠤ࠲ࠦࡻࡾࠩૄ").format(str(command_executor)))
    logger.debug(bstack1l1111_opy_ (u"࠭ࡈࡶࡤ࡙ࠣࡗࡒࠠࡪࡵࠣ࠱ࠥࢁࡽࠨૅ").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ૆") in command_executor._url:
      bstack1llllll11l_opy_.bstack11l1l111ll_opy_(bstack1l1111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩે"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack1l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬૈ") in command_executor):
    bstack1llllll11l_opy_.bstack11l1l111ll_opy_(bstack1l1111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫૉ"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack111l11l11_opy_ = getattr(threading.current_thread(), bstack1l1111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡘࡪࡹࡴࡎࡧࡷࡥࠬ૊"), None)
  bstack1ll1111l11_opy_ = {}
  if self.capabilities is not None:
    bstack1ll1111l11_opy_[bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫો")] = self.capabilities.get(bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫૌ"))
    bstack1ll1111l11_opy_[bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯્ࠩ")] = self.capabilities.get(bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ૎"))
    bstack1ll1111l11_opy_[bstack1l1111_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡡࡲࡴࡹ࡯࡯࡯ࡵࠪ૏")] = self.capabilities.get(bstack1l1111_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨૐ"))
  if CONFIG.get(bstack1l1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ૑"), False) and bstack1l11l1l111_opy_.bstack11lll1l1l_opy_(bstack1ll1111l11_opy_):
    threading.current_thread().a11yPlatform = True
  if bstack1l1111_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ૒") in bstack111l111l_opy_ or bstack1l1111_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ૓") in bstack111l111l_opy_:
    bstack11l11111l_opy_.bstack111lll1ll1_opy_(self)
  if bstack1l1111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ૔") in bstack111l111l_opy_ and bstack111l11l11_opy_ and bstack111l11l11_opy_.get(bstack1l1111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ૕"), bstack1l1111_opy_ (u"ࠩࠪ૖")) == bstack1l1111_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ૗"):
    bstack11l11111l_opy_.bstack111lll1ll1_opy_(self)
  bstack11lll1llll_opy_ = self.session_id
  with bstack11l1l11111_opy_:
    bstack1l1lll11ll_opy_.append(self)
  return bstack1l11ll1ll_opy_
def bstack111l11lll1_opy_(args):
  return bstack1l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠬ૘") in str(args)
def bstack11l111ll1_opy_(self, driver_command, *args, **kwargs):
  global bstack111llllll1_opy_
  global bstack11llll1111_opy_
  bstack1l11111l1_opy_ = bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ૙"), None) and bstack111111lll_opy_(
          threading.current_thread(), bstack1l1111_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ૚"), None)
  bstack1ll1l111ll_opy_ = bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ૛"), None) and bstack111111lll_opy_(
          threading.current_thread(), bstack1l1111_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ૜"), None)
  bstack1ll1111l_opy_ = getattr(self, bstack1l1111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩ૝"), None) != None and getattr(self, bstack1l1111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪ૞"), None) == True
  if not bstack11llll1111_opy_ and bstack1l1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ૟") in CONFIG and CONFIG[bstack1l1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬૠ")] == True and bstack1l1111l1ll_opy_.bstack11111lll_opy_(driver_command) and (bstack1ll1111l_opy_ or bstack1l11111l1_opy_ or bstack1ll1l111ll_opy_) and not bstack111l11lll1_opy_(args):
    try:
      bstack11llll1111_opy_ = True
      logger.debug(bstack1l1111_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡨࡲࡶࠥࢁࡽࠨૡ").format(driver_command))
      bstack1ll1l1l111_opy_ = perform_scan(self, driver_command=driver_command)
      logger.debug(bstack1ll1l1l111_opy_)
      try:
        bstack111l111lll_opy_ = {
          bstack1l1111_opy_ (u"ࠢࡳࡧࡴࡹࡪࡹࡴࠣૢ"): {
            bstack1l1111_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤૣ"): bstack1l1111_opy_ (u"ࠤࡄ࠵࠶࡟࡟ࡔࡅࡄࡒࠧ૤"),
            bstack1l1111_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡧࡷࡩࡷࡹࠢ૥"): [
              {
                bstack1l1111_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦ૦"): driver_command
              }
            ]
          },
          bstack1l1111_opy_ (u"ࠧࡸࡥࡴࡲࡲࡲࡸ࡫ࠢ૧"): {
            bstack1l1111_opy_ (u"ࠨࡢࡰࡦࡼࠦ૨"): {
              bstack1l1111_opy_ (u"ࠢ࡮ࡵࡪࠦ૩"): bstack1ll1l1l111_opy_.get(bstack1l1111_opy_ (u"ࠣ࡯ࡶ࡫ࠧ૪"), bstack1l1111_opy_ (u"ࠤࠥ૫")) if isinstance(bstack1ll1l1l111_opy_, dict) else bstack1l1111_opy_ (u"ࠥࠦ૬"),
              bstack1l1111_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧ૭"): bstack1ll1l1l111_opy_.get(bstack1l1111_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨ૮"), True) if isinstance(bstack1ll1l1l111_opy_, dict) else True
            }
          }
        }
        logger.debug(bstack1l1111_opy_ (u"࠭ࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡤࡣࡱࠤࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡ࡮ࡲ࡫ࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠧ૯").format(bstack111l111lll_opy_))
        bstack11l1lll11_opy_.info(json.dumps(bstack111l111lll_opy_, separators=(bstack1l1111_opy_ (u"ࠧ࠭ࠩ૰"), bstack1l1111_opy_ (u"ࠨ࠼ࠪ૱"))))
      except Exception as bstack1l1l111111_opy_:
        logger.debug(bstack1l1111_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡲ࡯ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡧࡦࡴࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠩ૲").format(str(bstack1l1l111111_opy_)))
    except Exception as err:
      logger.debug(bstack1l1111_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡦࡴࡩࡳࡷࡳࠠࡴࡥࡤࡲࠥࢁࡽࠨ૳").format(str(err)))
    bstack11llll1111_opy_ = False
  response = bstack111llllll1_opy_(self, driver_command, *args, **kwargs)
  if (bstack1l1111_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ૴") in str(bstack111l111l_opy_).lower() or bstack1l1111_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ૵") in str(bstack111l111l_opy_).lower()) and bstack1lll11ll11_opy_.on():
    try:
      if driver_command == bstack1l1111_opy_ (u"࠭ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪ૶"):
        bstack11l11111l_opy_.bstack11l1l1l1l_opy_({
            bstack1l1111_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭૷"): response[bstack1l1111_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧ૸")],
            bstack1l1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩૹ"): bstack11l11111l_opy_.current_test_uuid() if bstack11l11111l_opy_.current_test_uuid() else bstack1lll11ll11_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
def bstack1l1ll11l_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack11lll1llll_opy_
  global bstack1l1llll11_opy_
  global bstack11l1111lll_opy_
  global bstack1l11llll_opy_
  global bstack1lll111ll1_opy_
  global bstack111l111l_opy_
  global bstack1llll11l1l_opy_
  global bstack1l1lll11ll_opy_
  global bstack1l111l11l_opy_
  global bstack11lll111_opy_
  bstack1ll1111lll_opy_ = bstack11ll111lll_opy_.bstack111llllll_opy_(EVENTS.bstack1lllllll1l_opy_.value)
  if os.getenv(bstack1l1111_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨૺ")) is not None and bstack1l11l1l111_opy_.bstack1lll1111ll_opy_(CONFIG) is None:
    CONFIG[bstack1l1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫૻ")] = True
  CONFIG[bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧૼ")] = str(bstack111l111l_opy_) + str(__version__)
  bstack1llllll1l1_opy_ = os.environ[bstack1l1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ૽")]
  bstack1l1111lll_opy_ = bstack11l11ll111_opy_.bstack1l11l11lll_opy_(CONFIG, bstack111l111l_opy_)
  CONFIG[bstack1l1111_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ૾")] = bstack1llllll1l1_opy_
  CONFIG[bstack1l1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ૿")] = bstack1l1111lll_opy_
  if CONFIG.get(bstack1l1111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ଀"),bstack1l1111_opy_ (u"ࠪࠫଁ")) and bstack1l1111_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪଂ") in bstack111l111l_opy_:
    CONFIG[bstack1l1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬଃ")].pop(bstack1l1111_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫ଄"), None)
    CONFIG[bstack1l1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧଅ")].pop(bstack1l1111_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ଆ"), None)
  command_executor = bstack1l1l11l1_opy_()
  logger.debug(bstack1111lll1_opy_.format(command_executor))
  proxy = bstack1l1l1111ll_opy_(CONFIG, proxy)
  bstack11llll11l1_opy_ = 0 if bstack1l1llll11_opy_ < 0 else bstack1l1llll11_opy_
  try:
    if bstack1l11llll_opy_ is True:
      bstack11llll11l1_opy_ = int(multiprocessing.current_process().name)
    elif bstack1lll111ll1_opy_ is True:
      bstack11llll11l1_opy_ = int(threading.current_thread().name)
  except:
    bstack11llll11l1_opy_ = 0
  bstack11ll11ll1l_opy_ = bstack11l1l1l11l_opy_(CONFIG, bstack11llll11l1_opy_)
  logger.debug(bstack1lll1111l_opy_.format(str(bstack11ll11ll1l_opy_)))
  if bstack1l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ଇ") in CONFIG and bstack1l1111lll1_opy_(CONFIG[bstack1l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧଈ")]):
    bstack1111l11l_opy_(bstack11ll11ll1l_opy_)
  if bstack1l11l1l111_opy_.bstack11l111l1l_opy_(CONFIG, bstack11llll11l1_opy_) and bstack1l11l1l111_opy_.bstack111l11111_opy_(bstack11ll11ll1l_opy_, options, desired_capabilities, CONFIG):
    threading.current_thread().a11yPlatform = True
    if (cli.accessibility is None or not cli.accessibility.is_enabled()):
      bstack1l11l1l111_opy_.set_capabilities(bstack11ll11ll1l_opy_, CONFIG)
  if desired_capabilities:
    bstack1111l1111_opy_ = bstack1111l1l1l_opy_(desired_capabilities)
    bstack1111l1111_opy_[bstack1l1111_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫଉ")] = bstack111l1lll11_opy_(CONFIG)
    bstack1ll1lll1l1_opy_ = bstack11l1l1l11l_opy_(bstack1111l1111_opy_)
    if bstack1ll1lll1l1_opy_:
      bstack11ll11ll1l_opy_ = update(bstack1ll1lll1l1_opy_, bstack11ll11ll1l_opy_)
    desired_capabilities = None
  if options:
    bstack11l1l1l1_opy_(options, bstack11ll11ll1l_opy_)
  if not options:
    options = bstack1l1l1lllll_opy_(bstack11ll11ll1l_opy_)
  bstack11lll111_opy_ = CONFIG.get(bstack1l1111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨଊ"))[bstack11llll11l1_opy_]
  if proxy and bstack11ll111l_opy_() >= version.parse(bstack1l1111_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ଋ")):
    options.proxy(proxy)
  if options and bstack11ll111l_opy_() >= version.parse(bstack1l1111_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ଌ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack11ll111l_opy_() < version.parse(bstack1l1111_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ଍")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack11ll11ll1l_opy_)
  logger.info(bstack1l111lll11_opy_)
  bstack11l111111l_opy_.end(EVENTS.bstack11lllll1l1_opy_.value, EVENTS.bstack11lllll1l1_opy_.value + bstack1l1111_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ଎"), EVENTS.bstack11lllll1l1_opy_.value + bstack1l1111_opy_ (u"ࠥ࠾ࡪࡴࡤࠣଏ"), status=True, failure=None, test_name=bstack11l1111lll_opy_)
  if bstack1l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡶࡲࡰࡨ࡬ࡰࡪ࠭ଐ") in kwargs:
    del kwargs[bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡰࡳࡱࡩ࡭ࡱ࡫ࠧ଑")]
  bstack11ll111lll_opy_.end(EVENTS.bstack1lllllll1l_opy_.value, bstack1ll1111lll_opy_ + bstack1l1111_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ଒"), bstack1ll1111lll_opy_ + bstack1l1111_opy_ (u"ࠢ࠻ࡧࡱࡨࠧଓ"), status=True, failure=None, test_name=bstack11l1111lll_opy_)
  try:
    if bstack11ll111l_opy_() >= version.parse(bstack1l1111_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨଔ")):
      bstack1llll11l1l_opy_(self, command_executor=command_executor,
                options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
    elif bstack11ll111l_opy_() >= version.parse(bstack1l1111_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨକ")):
      bstack1llll11l1l_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities, options=options,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11ll111l_opy_() >= version.parse(bstack1l1111_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪଖ")):
      bstack1llll11l1l_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    else:
      bstack1llll11l1l_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive)
  except Exception as bstack11l1ll11_opy_:
    logger.error(bstack11ll11ll11_opy_.format(bstack1l1111_opy_ (u"ࠫࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠪଗ"), str(bstack11l1ll11_opy_)))
    raise bstack11l1ll11_opy_
  bstack1ll1111lll_opy_ = bstack11ll111lll_opy_.bstack111llllll_opy_(EVENTS.bstack11ll111l1_opy_.value)
  if bstack1l11l1l111_opy_.bstack11l111l1l_opy_(CONFIG, bstack11llll11l1_opy_) and bstack1l11l1l111_opy_.bstack111l11111_opy_(self.caps, options, desired_capabilities):
    if CONFIG[bstack1l1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧଘ")][bstack1l1111_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬଙ")] == True:
      threading.current_thread().appA11yPlatform = True
      if cli.accessibility is None or not cli.accessibility.is_enabled():
        bstack1l11l1l111_opy_.set_capabilities(bstack11ll11ll1l_opy_, CONFIG)
  try:
    bstack1ll1ll1l11_opy_ = bstack1l1111_opy_ (u"ࠧࠨଚ")
    if bstack11ll111l_opy_() >= version.parse(bstack1l1111_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࡢ࠲ࠩଛ")):
      if self.caps is not None:
        bstack1ll1ll1l11_opy_ = self.caps.get(bstack1l1111_opy_ (u"ࠤࡲࡴࡹ࡯࡭ࡢ࡮ࡋࡹࡧ࡛ࡲ࡭ࠤଜ"))
    else:
      if self.capabilities is not None:
        bstack1ll1ll1l11_opy_ = self.capabilities.get(bstack1l1111_opy_ (u"ࠥࡳࡵࡺࡩ࡮ࡣ࡯ࡌࡺࡨࡕࡳ࡮ࠥଝ"))
    if bstack1ll1ll1l11_opy_:
      bstack1l1lllll1_opy_(bstack1ll1ll1l11_opy_)
      if bstack11ll111l_opy_() <= version.parse(bstack1l1111_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫଞ")):
        self.command_executor._url = bstack1l1111_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨଟ") + bstack1l1lll1l11_opy_ + bstack1l1111_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥଠ")
      else:
        self.command_executor._url = bstack1l1111_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤଡ") + bstack1ll1ll1l11_opy_ + bstack1l1111_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤଢ")
      logger.debug(bstack1l1ll11l1l_opy_.format(bstack1ll1ll1l11_opy_))
    else:
      logger.debug(bstack1l11l1l1ll_opy_.format(bstack1l1111_opy_ (u"ࠤࡒࡴࡹ࡯࡭ࡢ࡮ࠣࡌࡺࡨࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦࠥଣ")))
  except Exception as e:
    logger.debug(bstack1l11l1l1ll_opy_.format(e))
  if bstack1l1111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩତ") in bstack111l111l_opy_:
    bstack111llll1l_opy_(bstack1l1llll11_opy_, bstack1l111l11l_opy_)
  bstack11lll1llll_opy_ = self.session_id
  if bstack1l1111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫଥ") in bstack111l111l_opy_ or bstack1l1111_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬଦ") in bstack111l111l_opy_ or bstack1l1111_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬଧ") in bstack111l111l_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack111l11l11_opy_ = getattr(threading.current_thread(), bstack1l1111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡔࡦࡵࡷࡑࡪࡺࡡࠨନ"), None)
  if bstack1l1111_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ଩") in bstack111l111l_opy_ or bstack1l1111_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨପ") in bstack111l111l_opy_:
    bstack11l11111l_opy_.bstack111lll1ll1_opy_(self)
  if bstack1l1111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪଫ") in bstack111l111l_opy_ and bstack111l11l11_opy_ and bstack111l11l11_opy_.get(bstack1l1111_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫବ"), bstack1l1111_opy_ (u"ࠬ࠭ଭ")) == bstack1l1111_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧମ"):
    bstack11l11111l_opy_.bstack111lll1ll1_opy_(self)
  with bstack11l1l11111_opy_:
    bstack1l1lll11ll_opy_.append(self)
  if bstack1l1111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଯ") in CONFIG and bstack1l1111_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ର") in CONFIG[bstack1l1111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ଱")][bstack11llll11l1_opy_]:
    bstack11l1111lll_opy_ = CONFIG[bstack1l1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ଲ")][bstack11llll11l1_opy_][bstack1l1111_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩଳ")]
  logger.debug(bstack111lll1l_opy_.format(bstack11lll1llll_opy_))
  bstack11ll111lll_opy_.end(EVENTS.bstack11ll111l1_opy_.value, bstack1ll1111lll_opy_ + bstack1l1111_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ଴"), bstack1ll1111lll_opy_ + bstack1l1111_opy_ (u"ࠨ࠺ࡦࡰࡧࠦଵ"), status=True, failure=None, test_name=bstack11l1111lll_opy_)
try:
  try:
    import Browser
    from subprocess import Popen
    from browserstack_sdk.__init__ import bstack1l111ll111_opy_
    def bstack1ll11l1l11_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1ll11l1l_opy_
      if(bstack1l1111_opy_ (u"ࠢࡪࡰࡧࡩࡽ࠴ࡪࡴࠤଶ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1l1111_opy_ (u"ࠨࢀࠪଷ")), bstack1l1111_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩସ"), bstack1l1111_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬହ")), bstack1l1111_opy_ (u"ࠫࡼ࠭଺")) as fp:
          fp.write(bstack1l1111_opy_ (u"ࠧࠨ଻"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1l1111_opy_ (u"ࠨࡩ࡯ࡦࡨࡼࡤࡨࡳࡵࡣࡦ࡯࠳ࡰࡳ଼ࠣ")))):
          with open(args[1], bstack1l1111_opy_ (u"ࠧࡳࠩଽ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1l1111_opy_ (u"ࠨࡣࡶࡽࡳࡩࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡢࡲࡪࡽࡐࡢࡩࡨࠬࡨࡵ࡮ࡵࡧࡻࡸ࠱ࠦࡰࡢࡩࡨࠤࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠧା") in line), None)
            if index is not None:
                lines.insert(index+2, bstack111ll111l1_opy_)
            if bstack1l1111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ି") in CONFIG and str(CONFIG[bstack1l1111_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧୀ")]).lower() != bstack1l1111_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪୁ"):
                bstack1llllll11_opy_ = bstack1l111ll111_opy_()
                bstack11l11ll1l1_opy_ = bstack1l1111_opy_ (u"ࠬ࠭ࠧࠋ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࠎࡨࡵ࡮ࡴࡶࠣࡦࡸࡺࡡࡤ࡭ࡢࡴࡦࡺࡨࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࡝ࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠷ࡢࡁࠊࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡣࡢࡲࡶࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠱࡞࠽ࠍࡧࡴࡴࡳࡵࠢࡳࡣ࡮ࡴࡤࡦࡺࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠸࡝࠼ࠌࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰ࡶࡰ࡮ࡩࡥࠩ࠲࠯ࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹ࠩ࠼ࠌࡦࡳࡳࡹࡴࠡ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢࠪ࠽ࠍ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡰࡦࡻ࡮ࡤࡪࠣࡁࠥࡧࡳࡺࡰࡦࠤ࠭ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷ࠮ࠦ࠽࠿ࠢࡾࡿࠏࠦࠠ࡭ࡧࡷࠤࡨࡧࡰࡴ࠽ࠍࠤࠥࡺࡲࡺࠢࡾࡿࠏࠦࠠࠡࠢࡦࡥࡵࡹࠠ࠾ࠢࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࡢࡴࡶࡤࡧࡰࡥࡣࡢࡲࡶ࠭ࡀࠐࠠࠡࡿࢀࠤࡨࡧࡴࡤࡪࠣࠬࡪࡾࠩࠡࡽࡾࠎࠥࠦࠠࠡࡥࡲࡲࡸࡵ࡬ࡦ࠰ࡨࡶࡷࡵࡲࠩࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵ࠽ࠦ࠱ࠦࡥࡹࠫ࠾ࠎࠥࠦࡽࡾࠌࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࢁࠊࠡࠢࠣࠤࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࠻ࠢࠪࡿࡨࡪࡰࡖࡴ࡯ࢁࠬࠦࠫࠡࡧࡱࡧࡴࡪࡥࡖࡔࡌࡇࡴࡳࡰࡰࡰࡨࡲࡹ࠮ࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡤࡣࡳࡷ࠮࠯ࠬࠋࠢࠣࠤࠥ࠴࠮࠯࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠋࠢࠣࢁࢂ࠯࠻ࠋࡿࢀ࠿ࠏ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯ࠋࠩࠪࠫୂ").format(bstack1llllll11_opy_=bstack1llllll11_opy_)
            lines.insert(1, bstack11l11ll1l1_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1l1111_opy_ (u"ࠨࡩ࡯ࡦࡨࡼࡤࡨࡳࡵࡣࡦ࡯࠳ࡰࡳࠣୃ")), bstack1l1111_opy_ (u"ࠧࡸࠩୄ")) as bstack1l1l1llll1_opy_:
              bstack1l1l1llll1_opy_.writelines(lines)
        CONFIG[bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ୅")] = str(bstack111l111l_opy_) + str(__version__)
        bstack1llllll1l1_opy_ = os.environ[bstack1l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ୆")]
        bstack1l1111lll_opy_ = bstack11l11ll111_opy_.bstack1l11l11lll_opy_(CONFIG, bstack111l111l_opy_)
        CONFIG[bstack1l1111_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭େ")] = bstack1llllll1l1_opy_
        CONFIG[bstack1l1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ୈ")] = bstack1l1111lll_opy_
        bstack11llll11l1_opy_ = 0 if bstack1l1llll11_opy_ < 0 else bstack1l1llll11_opy_
        try:
          if bstack1l11llll_opy_ is True:
            bstack11llll11l1_opy_ = int(multiprocessing.current_process().name)
          elif bstack1lll111ll1_opy_ is True:
            bstack11llll11l1_opy_ = int(threading.current_thread().name)
        except:
          bstack11llll11l1_opy_ = 0
        CONFIG[bstack1l1111_opy_ (u"ࠧࡻࡳࡦ࡙࠶ࡇࠧ୉")] = False
        CONFIG[bstack1l1111_opy_ (u"ࠨࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧ୊")] = True
        bstack11ll11ll1l_opy_ = bstack11l1l1l11l_opy_(CONFIG, bstack11llll11l1_opy_)
        logger.debug(bstack1lll1111l_opy_.format(str(bstack11ll11ll1l_opy_)))
        if CONFIG.get(bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫୋ")):
          bstack1111l11l_opy_(bstack11ll11ll1l_opy_)
        if bstack1l1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫୌ") in CONFIG and bstack1l1111_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫୍ࠧ") in CONFIG[bstack1l1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭୎")][bstack11llll11l1_opy_]:
          bstack11l1111lll_opy_ = CONFIG[bstack1l1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ୏")][bstack11llll11l1_opy_][bstack1l1111_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ୐")]
        args.append(os.path.join(os.path.expanduser(bstack1l1111_opy_ (u"࠭ࡾࠨ୑")), bstack1l1111_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ୒"), bstack1l1111_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪ୓")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack11ll11ll1l_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1l1111_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸࡠࡤࡶࡸࡦࡩ࡫࠯࡬ࡶࠦ୔"))
      bstack1ll11l1l_opy_ = True
      return bstack1l11l111l1_opy_(self, args, bufsize=bufsize, executable=executable,
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
  def bstack11ll11111_opy_(self,
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
    global bstack1l1llll11_opy_
    global bstack11l1111lll_opy_
    global bstack1l11llll_opy_
    global bstack1lll111ll1_opy_
    global bstack111l111l_opy_
    CONFIG[bstack1l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ୕")] = str(bstack111l111l_opy_) + str(__version__)
    bstack1llllll1l1_opy_ = os.environ[bstack1l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩୖ")]
    bstack1l1111lll_opy_ = bstack11l11ll111_opy_.bstack1l11l11lll_opy_(CONFIG, bstack111l111l_opy_)
    CONFIG[bstack1l1111_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨୗ")] = bstack1llllll1l1_opy_
    CONFIG[bstack1l1111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨ୘")] = bstack1l1111lll_opy_
    bstack11llll11l1_opy_ = 0 if bstack1l1llll11_opy_ < 0 else bstack1l1llll11_opy_
    try:
      if bstack1l11llll_opy_ is True:
        bstack11llll11l1_opy_ = int(multiprocessing.current_process().name)
      elif bstack1lll111ll1_opy_ is True:
        bstack11llll11l1_opy_ = int(threading.current_thread().name)
    except:
      bstack11llll11l1_opy_ = 0
    CONFIG[bstack1l1111_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ୙")] = True
    bstack11ll11ll1l_opy_ = bstack11l1l1l11l_opy_(CONFIG, bstack11llll11l1_opy_)
    logger.debug(bstack1lll1111l_opy_.format(str(bstack11ll11ll1l_opy_)))
    if CONFIG.get(bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ୚")):
      bstack1111l11l_opy_(bstack11ll11ll1l_opy_)
    if bstack1l1111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ୛") in CONFIG and bstack1l1111_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨଡ଼") in CONFIG[bstack1l1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଢ଼")][bstack11llll11l1_opy_]:
      bstack11l1111lll_opy_ = CONFIG[bstack1l1111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ୞")][bstack11llll11l1_opy_][bstack1l1111_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫୟ")]
    import urllib
    import json
    if bstack1l1111_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫୠ") in CONFIG and str(CONFIG[bstack1l1111_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬୡ")]).lower() != bstack1l1111_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨୢ"):
        bstack11ll1l1l1_opy_ = bstack1l111ll111_opy_()
        bstack1llllll11_opy_ = bstack11ll1l1l1_opy_ + urllib.parse.quote(json.dumps(bstack11ll11ll1l_opy_))
    else:
        bstack1llllll11_opy_ = bstack1l1111_opy_ (u"ࠪࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠬୣ") + urllib.parse.quote(json.dumps(bstack11ll11ll1l_opy_))
    browser = self.connect(bstack1llllll11_opy_)
    return browser
except Exception as e:
    pass
def bstack111l1l11ll_opy_():
    global bstack1ll11l1l_opy_
    global bstack111l111l_opy_
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1ll11111ll_opy_
        global bstack1llllll11l_opy_
        if not bstack1l1llll1l1_opy_:
          global bstack1ll1ll111_opy_
          if not bstack1ll1ll111_opy_:
            from bstack_utils.helper import bstack1l111lll1_opy_, bstack11lll1l111_opy_, bstack1111111l_opy_
            bstack1ll1ll111_opy_ = bstack1l111lll1_opy_()
            bstack11lll1l111_opy_(bstack111l111l_opy_)
            bstack1l1111lll_opy_ = bstack11l11ll111_opy_.bstack1l11l11lll_opy_(CONFIG, bstack111l111l_opy_)
            bstack1llllll11l_opy_.bstack11l1l111ll_opy_(bstack1l1111_opy_ (u"ࠦࡕࡒࡁ࡚࡙ࡕࡍࡌࡎࡔࡠࡒࡕࡓࡉ࡛ࡃࡕࡡࡐࡅࡕࠨ୤"), bstack1l1111lll_opy_)
          BrowserType.connect = bstack1ll11111ll_opy_
          return
        BrowserType.launch = bstack11ll11111_opy_
        bstack1ll11l1l_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1ll11l1l11_opy_
      bstack1ll11l1l_opy_ = True
    except Exception as e:
      pass
def bstack1llll1ll1_opy_(context, bstack11l1lll1_opy_):
  try:
    if getattr(context, bstack1l1111_opy_ (u"ࠬࡶࡡࡨࡧࠪ୥"), None):
      context.page.evaluate(bstack1l1111_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢ୦"), bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫ୧")+ json.dumps(bstack11l1lll1_opy_) + bstack1l1111_opy_ (u"ࠣࡿࢀࠦ୨"))
  except Exception as e:
    logger.debug(bstack1l1111_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃ࠺ࠡࡽࢀࠦ୩").format(str(e), traceback.format_exc()))
def bstack11l1ll111_opy_(context, message, level):
  try:
    if getattr(context, bstack1l1111_opy_ (u"ࠪࡴࡦ࡭ࡥࠨ୪"), None):
      context.page.evaluate(bstack1l1111_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧ୫"), bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ୬") + json.dumps(message) + bstack1l1111_opy_ (u"࠭ࠬࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠩ୭") + json.dumps(level) + bstack1l1111_opy_ (u"ࠧࡾࡿࠪ୮"))
  except Exception as e:
    logger.debug(bstack1l1111_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡࡽࢀ࠾ࠥࢁࡽࠣ୯").format(str(e), traceback.format_exc()))
@measure(event_name=EVENTS.bstack1llll1l1l_opy_, stage=STAGE.bstack1111lll11_opy_, bstack1l1l111l_opy_=bstack11l1111lll_opy_)
def bstack1l111ll1ll_opy_(self, url):
  global bstack11ll11lll_opy_
  try:
    bstack1lll1l11_opy_(url)
  except Exception as err:
    logger.debug(bstack1l1l11lll_opy_.format(str(err)))
  try:
    bstack11ll11lll_opy_(self, url)
  except Exception as e:
    try:
      bstack1l111l111l_opy_ = str(e)
      if any(err_msg in bstack1l111l111l_opy_ for err_msg in bstack11l11ll1ll_opy_):
        bstack1lll1l11_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1l1l11lll_opy_.format(str(err)))
    raise e
def bstack1111llll_opy_(self):
  global bstack1llll1llll_opy_
  bstack1llll1llll_opy_ = self
  return
def bstack11lll1ll1_opy_(self):
  global bstack11l1ll11l_opy_
  bstack11l1ll11l_opy_ = self
  return
def bstack1l1lll1ll_opy_(test_name, bstack1l1ll1lll1_opy_):
  global CONFIG
  if percy.bstack11l1llllll_opy_() == bstack1l1111_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ୰"):
    bstack1lll11ll_opy_ = os.path.relpath(bstack1l1ll1lll1_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack1lll11ll_opy_)
    bstack1l1l111l_opy_ = suite_name + bstack1l1111_opy_ (u"ࠥ࠱ࠧୱ") + test_name
    threading.current_thread().percySessionName = bstack1l1l111l_opy_
def bstack1ll1ll1l1_opy_(self, test, *args, **kwargs):
  global bstack11111ll11_opy_
  test_name = None
  bstack1l1ll1lll1_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1l1ll1lll1_opy_ = str(test.source)
  bstack1l1lll1ll_opy_(test_name, bstack1l1ll1lll1_opy_)
  bstack11111ll11_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.bstack111lll1l11_opy_, stage=STAGE.bstack1111lll11_opy_, bstack1l1l111l_opy_=bstack11l1111lll_opy_)
def bstack1l1l1lll1l_opy_(driver, bstack1l1l111l_opy_):
  if not bstack1l1lll11l_opy_ and bstack1l1l111l_opy_:
      bstack11ll1l11l1_opy_ = {
          bstack1l1111_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫ୲"): bstack1l1111_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭୳"),
          bstack1l1111_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ୴"): {
              bstack1l1111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ୵"): bstack1l1l111l_opy_
          }
      }
      bstack11l1l11l1l_opy_ = bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭୶").format(json.dumps(bstack11ll1l11l1_opy_))
      driver.execute_script(bstack11l1l11l1l_opy_)
  if bstack11ll1ll11_opy_:
      bstack1lll1lll_opy_ = {
          bstack1l1111_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩ୷"): bstack1l1111_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬ୸"),
          bstack1l1111_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ୹"): {
              bstack1l1111_opy_ (u"ࠬࡪࡡࡵࡣࠪ୺"): bstack1l1l111l_opy_ + bstack1l1111_opy_ (u"࠭ࠠࡱࡣࡶࡷࡪࡪࠡࠨ୻"),
              bstack1l1111_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭୼"): bstack1l1111_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭୽")
          }
      }
      if bstack11ll1ll11_opy_.status == bstack1l1111_opy_ (u"ࠩࡓࡅࡘ࡙ࠧ୾"):
          bstack1l1111l1l_opy_ = bstack1l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨ୿").format(json.dumps(bstack1lll1lll_opy_))
          driver.execute_script(bstack1l1111l1l_opy_)
          bstack1l111l1ll_opy_(driver, bstack1l1111_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ஀"))
      elif bstack11ll1ll11_opy_.status == bstack1l1111_opy_ (u"ࠬࡌࡁࡊࡎࠪ஁"):
          reason = bstack1l1111_opy_ (u"ࠨࠢஂ")
          bstack11lll11l1_opy_ = bstack1l1l111l_opy_ + bstack1l1111_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠨஃ")
          if bstack11ll1ll11_opy_.message:
              reason = str(bstack11ll1ll11_opy_.message)
              bstack11lll11l1_opy_ = bstack11lll11l1_opy_ + bstack1l1111_opy_ (u"ࠨࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࡀࠠࠨ஄") + reason
          bstack1lll1lll_opy_[bstack1l1111_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬஅ")] = {
              bstack1l1111_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩஆ"): bstack1l1111_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪஇ"),
              bstack1l1111_opy_ (u"ࠬࡪࡡࡵࡣࠪஈ"): bstack11lll11l1_opy_
          }
          bstack1l1111l1l_opy_ = bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫஉ").format(json.dumps(bstack1lll1lll_opy_))
          driver.execute_script(bstack1l1111l1l_opy_)
          bstack1l111l1ll_opy_(driver, bstack1l1111_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧஊ"), reason)
          bstack1l1111l111_opy_(reason, str(bstack11ll1ll11_opy_), str(bstack1l1llll11_opy_), logger)
@measure(event_name=EVENTS.bstack111l11ll1l_opy_, stage=STAGE.bstack1111lll11_opy_, bstack1l1l111l_opy_=bstack11l1111lll_opy_)
def bstack1l1ll1l11_opy_(driver, test):
  if percy.bstack11l1llllll_opy_() == bstack1l1111_opy_ (u"ࠣࡶࡵࡹࡪࠨ஋") and percy.bstack11llllll11_opy_() == bstack1l1111_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦ஌"):
      bstack1ll1l1lll_opy_ = bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠪࡴࡪࡸࡣࡺࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭஍"), None)
      bstack1l1lllllll_opy_(driver, bstack1ll1l1lll_opy_, test)
  if (bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨஎ"), None) and
      bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫஏ"), None)) or (
      bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ஐ"), None) and
      bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ஑"), None)):
      logger.info(bstack1l1111_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠦࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡ࡫ࡶࠤࡺࡴࡤࡦࡴࡺࡥࡾ࠴ࠠࠣஒ"))
      bstack1l11l1l111_opy_.bstack111ll1ll1_opy_(driver, name=test.name, path=test.source)
def bstack111l1l1111_opy_(test, bstack1l1l111l_opy_):
    try:
      bstack1ll1lll11l_opy_ = datetime.datetime.now()
      data = {}
      if test:
        data[bstack1l1111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧஓ")] = bstack1l1l111l_opy_
      if bstack11ll1ll11_opy_:
        if bstack11ll1ll11_opy_.status == bstack1l1111_opy_ (u"ࠪࡔࡆ࡙ࡓࠨஔ"):
          data[bstack1l1111_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫக")] = bstack1l1111_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ஖")
        elif bstack11ll1ll11_opy_.status == bstack1l1111_opy_ (u"࠭ࡆࡂࡋࡏࠫ஗"):
          data[bstack1l1111_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ஘")] = bstack1l1111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨங")
          if bstack11ll1ll11_opy_.message:
            data[bstack1l1111_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩச")] = str(bstack11ll1ll11_opy_.message)
      user = CONFIG[bstack1l1111_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ஛")]
      key = CONFIG[bstack1l1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧஜ")]
      host = bstack11ll1l11_opy_(cli.config, [bstack1l1111_opy_ (u"ࠧࡧࡰࡪࡵࠥ஝"), bstack1l1111_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥࠣஞ"), bstack1l1111_opy_ (u"ࠢࡢࡲ࡬ࠦட")], bstack1l1111_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠤ஠"))
      url = bstack1l1111_opy_ (u"ࠩࡾࢁ࠴ࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡴࡧࡶࡷ࡮ࡵ࡮ࡴ࠱ࡾࢁ࠳ࡰࡳࡰࡰࠪ஡").format(host, bstack11lll1llll_opy_)
      headers = {
        bstack1l1111_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩ஢"): bstack1l1111_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧண"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers, auth=(user, key))
        cli.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽ࡹࡵࡪࡡࡵࡧࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡸࡦࡺࡵࡴࠤத"), datetime.datetime.now() - bstack1ll1lll11l_opy_)
    except Exception as e:
      logger.error(bstack1l11llll11_opy_.format(str(e)))
def bstack1ll1ll11l_opy_(test, bstack1l1l111l_opy_):
  global CONFIG
  global bstack11l1ll11l_opy_
  global bstack1llll1llll_opy_
  global bstack11lll1llll_opy_
  global bstack11ll1ll11_opy_
  global bstack11l1111lll_opy_
  global bstack1l1ll1l11l_opy_
  global bstack111lllll1_opy_
  global bstack1l11l1l1_opy_
  global bstack11lll1lll_opy_
  global bstack1l1lll11ll_opy_
  global bstack11lll111_opy_
  global bstack1lll1111l1_opy_
  try:
    if not bstack11lll1llll_opy_:
      with bstack1lll1111l1_opy_:
        bstack1l1l1lll11_opy_ = os.path.join(os.path.expanduser(bstack1l1111_opy_ (u"࠭ࡾࠨ஥")), bstack1l1111_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ஦"), bstack1l1111_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪ஧"))
        if os.path.exists(bstack1l1l1lll11_opy_):
          with open(bstack1l1l1lll11_opy_, bstack1l1111_opy_ (u"ࠩࡵࠫந")) as f:
            content = f.read().strip()
            if content:
              bstack11l1l11l11_opy_ = json.loads(bstack1l1111_opy_ (u"ࠥࡿࠧன") + content + bstack1l1111_opy_ (u"ࠫࠧࡾࠢ࠻ࠢࠥࡽࠧ࠭ப") + bstack1l1111_opy_ (u"ࠧࢃࠢ஫"))
              bstack11lll1llll_opy_ = bstack11l1l11l11_opy_.get(str(threading.get_ident()))
  except Exception as e:
    logger.debug(bstack1l1111_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡸࡥࡢࡦ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡊࡆࡶࠤ࡫࡯࡬ࡦ࠼ࠣࠫ஬") + str(e))
  if bstack1l1lll11ll_opy_:
    with bstack11l1l11111_opy_:
      bstack1l1l11111_opy_ = bstack1l1lll11ll_opy_.copy()
    for driver in bstack1l1l11111_opy_:
      if bstack11lll1llll_opy_ == driver.session_id:
        if test:
          bstack1l1ll1l11_opy_(driver, test)
        bstack1l1l1lll1l_opy_(driver, bstack1l1l111l_opy_)
  elif bstack11lll1llll_opy_:
    bstack111l1l1111_opy_(test, bstack1l1l111l_opy_)
  if bstack11l1ll11l_opy_:
    bstack111lllll1_opy_(bstack11l1ll11l_opy_)
  if bstack1llll1llll_opy_:
    bstack1l11l1l1_opy_(bstack1llll1llll_opy_)
  if bstack1lllll1lll_opy_:
    bstack11lll1lll_opy_()
def bstack1l11ll1l11_opy_(self, test, *args, **kwargs):
  bstack1l1l111l_opy_ = None
  if test:
    bstack1l1l111l_opy_ = str(test.name)
  bstack1ll1ll11l_opy_(test, bstack1l1l111l_opy_)
  bstack1l1ll1l11l_opy_(self, test, *args, **kwargs)
def bstack1lll11ll1_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1llll1l1l1_opy_
  global CONFIG
  global bstack1l1lll11ll_opy_
  global bstack11lll1llll_opy_
  global bstack1lll1111l1_opy_
  bstack1l1llll111_opy_ = None
  try:
    if bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭஭"), None) or bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪம"), None):
      try:
        if not bstack11lll1llll_opy_:
          bstack1l1l1lll11_opy_ = os.path.join(os.path.expanduser(bstack1l1111_opy_ (u"ࠩࢁࠫய")), bstack1l1111_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪர"), bstack1l1111_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭ற"))
          with bstack1lll1111l1_opy_:
            if os.path.exists(bstack1l1l1lll11_opy_):
              with open(bstack1l1l1lll11_opy_, bstack1l1111_opy_ (u"ࠬࡸࠧல")) as f:
                content = f.read().strip()
                if content:
                  bstack11l1l11l11_opy_ = json.loads(bstack1l1111_opy_ (u"ࠨࡻࠣள") + content + bstack1l1111_opy_ (u"ࠧࠣࡺࠥ࠾ࠥࠨࡹࠣࠩழ") + bstack1l1111_opy_ (u"ࠣࡿࠥவ"))
                  bstack11lll1llll_opy_ = bstack11l1l11l11_opy_.get(str(threading.get_ident()))
      except Exception as e:
        logger.debug(bstack1l1111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡴࡨࡥࡩ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡍࡉࡹࠠࡧ࡫࡯ࡩࠥ࡯࡮ࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࡀࠠࠨஶ") + str(e))
      if bstack1l1lll11ll_opy_:
        with bstack11l1l11111_opy_:
          bstack1l1l11111_opy_ = bstack1l1lll11ll_opy_.copy()
        for driver in bstack1l1l11111_opy_:
          if bstack11lll1llll_opy_ == driver.session_id:
            bstack1l1llll111_opy_ = driver
    bstack11l111l1l1_opy_ = bstack1l11l1l111_opy_.bstack1lllll11ll_opy_(test.tags)
    if bstack1l1llll111_opy_:
      threading.current_thread().isA11yTest = bstack1l11l1l111_opy_.bstack111l11l1ll_opy_(bstack1l1llll111_opy_, bstack11l111l1l1_opy_)
      threading.current_thread().isAppA11yTest = bstack1l11l1l111_opy_.bstack111l11l1ll_opy_(bstack1l1llll111_opy_, bstack11l111l1l1_opy_)
    else:
      threading.current_thread().isA11yTest = bstack11l111l1l1_opy_
      threading.current_thread().isAppA11yTest = bstack11l111l1l1_opy_
  except:
    pass
  bstack1llll1l1l1_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack11ll1ll11_opy_
  try:
    bstack11ll1ll11_opy_ = self._test
  except:
    bstack11ll1ll11_opy_ = self.test
def bstack1l1111llll_opy_():
  global bstack1ll1ll1lll_opy_
  try:
    if os.path.exists(bstack1ll1ll1lll_opy_):
      os.remove(bstack1ll1ll1lll_opy_)
  except Exception as e:
    logger.debug(bstack1l1111_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭ஷ") + str(e))
def bstack111l1l1l11_opy_():
  global bstack1ll1ll1lll_opy_
  bstack11l1l11lll_opy_ = {}
  lock_file = bstack1ll1ll1lll_opy_ + bstack1l1111_opy_ (u"ࠫ࠳ࡲ࡯ࡤ࡭ࠪஸ")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l1111_opy_ (u"ࠬ࡬ࡩ࡭ࡧ࡯ࡳࡨࡱࠠ࡯ࡱࡷࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠬࠡࡷࡶ࡭ࡳ࡭ࠠࡣࡣࡶ࡭ࡨࠦࡦࡪ࡮ࡨࠤࡴࡶࡥࡳࡣࡷ࡭ࡴࡴࡳࠨஹ"))
    try:
      if not os.path.isfile(bstack1ll1ll1lll_opy_):
        with open(bstack1ll1ll1lll_opy_, bstack1l1111_opy_ (u"࠭ࡷࠨ஺")) as f:
          json.dump({}, f)
      if os.path.exists(bstack1ll1ll1lll_opy_):
        with open(bstack1ll1ll1lll_opy_, bstack1l1111_opy_ (u"ࠧࡳࠩ஻")) as f:
          content = f.read().strip()
          if content:
            bstack11l1l11lll_opy_ = json.loads(content)
    except Exception as e:
      logger.debug(bstack1l1111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡶࡪࡧࡤࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪ஼") + str(e))
    return bstack11l1l11lll_opy_
  try:
    os.makedirs(os.path.dirname(bstack1ll1ll1lll_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      if not os.path.isfile(bstack1ll1ll1lll_opy_):
        with open(bstack1ll1ll1lll_opy_, bstack1l1111_opy_ (u"ࠩࡺࠫ஽")) as f:
          json.dump({}, f)
      if os.path.exists(bstack1ll1ll1lll_opy_):
        with open(bstack1ll1ll1lll_opy_, bstack1l1111_opy_ (u"ࠪࡶࠬா")) as f:
          content = f.read().strip()
          if content:
            bstack11l1l11lll_opy_ = json.loads(content)
  except Exception as e:
    logger.debug(bstack1l1111_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡲࡦࡣࡧ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭ி") + str(e))
  finally:
    return bstack11l1l11lll_opy_
def bstack111llll1l_opy_(platform_index, item_index):
  global bstack1ll1ll1lll_opy_
  lock_file = bstack1ll1ll1lll_opy_ + bstack1l1111_opy_ (u"ࠬ࠴࡬ࡰࡥ࡮ࠫீ")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l1111_opy_ (u"࠭ࡦࡪ࡮ࡨࡰࡴࡩ࡫ࠡࡰࡲࡸࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥ࠭ࠢࡸࡷ࡮ࡴࡧࠡࡤࡤࡷ࡮ࡩࠠࡧ࡫࡯ࡩࠥࡵࡰࡦࡴࡤࡸ࡮ࡵ࡮ࡴࠩு"))
    try:
      bstack11l1l11lll_opy_ = {}
      if os.path.exists(bstack1ll1ll1lll_opy_):
        with open(bstack1ll1ll1lll_opy_, bstack1l1111_opy_ (u"ࠧࡳࠩூ")) as f:
          content = f.read().strip()
          if content:
            bstack11l1l11lll_opy_ = json.loads(content)
      bstack11l1l11lll_opy_[item_index] = platform_index
      with open(bstack1ll1ll1lll_opy_, bstack1l1111_opy_ (u"ࠣࡹࠥ௃")) as outfile:
        json.dump(bstack11l1l11lll_opy_, outfile)
    except Exception as e:
      logger.debug(bstack1l1111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡼࡸࡩࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧ௄") + str(e))
    return
  try:
    os.makedirs(os.path.dirname(bstack1ll1ll1lll_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      bstack11l1l11lll_opy_ = {}
      if os.path.exists(bstack1ll1ll1lll_opy_):
        with open(bstack1ll1ll1lll_opy_, bstack1l1111_opy_ (u"ࠪࡶࠬ௅")) as f:
          content = f.read().strip()
          if content:
            bstack11l1l11lll_opy_ = json.loads(content)
      bstack11l1l11lll_opy_[item_index] = platform_index
      with open(bstack1ll1ll1lll_opy_, bstack1l1111_opy_ (u"ࠦࡼࠨெ")) as outfile:
        json.dump(bstack11l1l11lll_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1l1111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡸࡴ࡬ࡸ࡮ࡴࡧࠡࡶࡲࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪே") + str(e))
def bstack1l1lll1l_opy_(bstack1l1l11ll_opy_):
  global CONFIG
  bstack1l11ll111l_opy_ = bstack1l1111_opy_ (u"࠭ࠧை")
  if not bstack1l1111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ௉") in CONFIG:
    logger.info(bstack1l1111_opy_ (u"ࠨࡐࡲࠤࡵࡲࡡࡵࡨࡲࡶࡲࡹࠠࡱࡣࡶࡷࡪࡪࠠࡶࡰࡤࡦࡱ࡫ࠠࡵࡱࠣ࡫ࡪࡴࡥࡳࡣࡷࡩࠥࡸࡥࡱࡱࡵࡸࠥ࡬࡯ࡳࠢࡕࡳࡧࡵࡴࠡࡴࡸࡲࠬொ"))
  try:
    platform = CONFIG[bstack1l1111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬோ")][bstack1l1l11ll_opy_]
    if bstack1l1111_opy_ (u"ࠪࡳࡸ࠭ௌ") in platform:
      bstack1l11ll111l_opy_ += str(platform[bstack1l1111_opy_ (u"ࠫࡴࡹ்ࠧ")]) + bstack1l1111_opy_ (u"ࠬ࠲ࠠࠨ௎")
    if bstack1l1111_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ௏") in platform:
      bstack1l11ll111l_opy_ += str(platform[bstack1l1111_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪௐ")]) + bstack1l1111_opy_ (u"ࠨ࠮ࠣࠫ௑")
    if bstack1l1111_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭௒") in platform:
      bstack1l11ll111l_opy_ += str(platform[bstack1l1111_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧ௓")]) + bstack1l1111_opy_ (u"ࠫ࠱ࠦࠧ௔")
    if bstack1l1111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ௕") in platform:
      bstack1l11ll111l_opy_ += str(platform[bstack1l1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ௖")]) + bstack1l1111_opy_ (u"ࠧ࠭ࠢࠪௗ")
    if bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭௘") in platform:
      bstack1l11ll111l_opy_ += str(platform[bstack1l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ௙")]) + bstack1l1111_opy_ (u"ࠪ࠰ࠥ࠭௚")
    if bstack1l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ௛") in platform:
      bstack1l11ll111l_opy_ += str(platform[bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭௜")]) + bstack1l1111_opy_ (u"࠭ࠬࠡࠩ௝")
  except Exception as e:
    logger.debug(bstack1l1111_opy_ (u"ࠧࡔࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡱࡩࡷࡧࡴࡪࡰࡪࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡳࡵࡴ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡶࡪࡶ࡯ࡳࡶࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡴࡴࠧ௞") + str(e))
  finally:
    if bstack1l11ll111l_opy_[len(bstack1l11ll111l_opy_) - 2:] == bstack1l1111_opy_ (u"ࠨ࠮ࠣࠫ௟"):
      bstack1l11ll111l_opy_ = bstack1l11ll111l_opy_[:-2]
    return bstack1l11ll111l_opy_
def bstack1111l1lll_opy_(path, bstack1l11ll111l_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack111l1l1ll_opy_ = ET.parse(path)
    bstack1l1l1ll111_opy_ = bstack111l1l1ll_opy_.getroot()
    bstack1lll1ll11_opy_ = None
    for suite in bstack1l1l1ll111_opy_.iter(bstack1l1111_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨ௠")):
      if bstack1l1111_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ௡") in suite.attrib:
        suite.attrib[bstack1l1111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ௢")] += bstack1l1111_opy_ (u"ࠬࠦࠧ௣") + bstack1l11ll111l_opy_
        bstack1lll1ll11_opy_ = suite
    bstack11l11lllll_opy_ = None
    for robot in bstack1l1l1ll111_opy_.iter(bstack1l1111_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ௤")):
      bstack11l11lllll_opy_ = robot
    bstack11l1llll1l_opy_ = len(bstack11l11lllll_opy_.findall(bstack1l1111_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭௥")))
    if bstack11l1llll1l_opy_ == 1:
      bstack11l11lllll_opy_.remove(bstack11l11lllll_opy_.findall(bstack1l1111_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧ௦"))[0])
      bstack1lllll1l1_opy_ = ET.Element(bstack1l1111_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨ௧"), attrib={bstack1l1111_opy_ (u"ࠪࡲࡦࡳࡥࠨ௨"): bstack1l1111_opy_ (u"ࠫࡘࡻࡩࡵࡧࡶࠫ௩"), bstack1l1111_opy_ (u"ࠬ࡯ࡤࠨ௪"): bstack1l1111_opy_ (u"࠭ࡳ࠱ࠩ௫")})
      bstack11l11lllll_opy_.insert(1, bstack1lllll1l1_opy_)
      bstack1l1ll1l1_opy_ = None
      for suite in bstack11l11lllll_opy_.iter(bstack1l1111_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭௬")):
        bstack1l1ll1l1_opy_ = suite
      bstack1l1ll1l1_opy_.append(bstack1lll1ll11_opy_)
      bstack111l1ll1l_opy_ = None
      for status in bstack1lll1ll11_opy_.iter(bstack1l1111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ௭")):
        bstack111l1ll1l_opy_ = status
      bstack1l1ll1l1_opy_.append(bstack111l1ll1l_opy_)
    bstack111l1l1ll_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1l1111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡲࡴ࡫ࡱ࡫ࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠧ௮") + str(e))
def bstack1ll111l1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack11ll1l1l_opy_
  global CONFIG
  if bstack1l1111_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࡳࡥࡹ࡮ࠢ௯") in options:
    del options[bstack1l1111_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡴࡦࡺࡨࠣ௰")]
  bstack11l11l11l1_opy_ = bstack111l1l1l11_opy_()
  for item_id in bstack11l11l11l1_opy_.keys():
    path = os.path.join(outs_dir, str(item_id), bstack1l1111_opy_ (u"ࠬࡵࡵࡵࡲࡸࡸ࠳ࡾ࡭࡭ࠩ௱"))
    bstack1111l1lll_opy_(path, bstack1l1lll1l_opy_(bstack11l11l11l1_opy_[item_id]))
  bstack1l1111llll_opy_()
  return bstack11ll1l1l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack11l11l111l_opy_(self, ff_profile_dir):
  global bstack1lll1llll1_opy_
  if not ff_profile_dir:
    return None
  return bstack1lll1llll1_opy_(self, ff_profile_dir)
def bstack1l111l11l1_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack11l11111_opy_
  bstack111111l1_opy_ = []
  if bstack1l1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ௲") in CONFIG:
    bstack111111l1_opy_ = CONFIG[bstack1l1111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ௳")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1l1111_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤ௴")],
      pabot_args[bstack1l1111_opy_ (u"ࠤࡹࡩࡷࡨ࡯ࡴࡧࠥ௵")],
      argfile,
      pabot_args.get(bstack1l1111_opy_ (u"ࠥ࡬࡮ࡼࡥࠣ௶")),
      pabot_args[bstack1l1111_opy_ (u"ࠦࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠢ௷")],
      platform[0],
      bstack11l11111_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1l1111_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡦࡪ࡮ࡨࡷࠧ௸")] or [(bstack1l1111_opy_ (u"ࠨࠢ௹"), None)]
    for platform in enumerate(bstack111111l1_opy_)
  ]
def bstack11ll1ll1ll_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1l1ll1111l_opy_=bstack1l1111_opy_ (u"ࠧࠨ௺")):
  global bstack11llllllll_opy_
  self.platform_index = platform_index
  self.bstack1lllllll1_opy_ = bstack1l1ll1111l_opy_
  bstack11llllllll_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1lll11l1_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1lll1ll1ll_opy_
  global bstack1ll1l11l11_opy_
  bstack1ll11ll1_opy_ = copy.deepcopy(item)
  if not bstack1l1111_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ௻") in item.options:
    bstack1ll11ll1_opy_.options[bstack1l1111_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ௼")] = []
  bstack1l1llllll_opy_ = bstack1ll11ll1_opy_.options[bstack1l1111_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ௽")].copy()
  for v in bstack1ll11ll1_opy_.options[bstack1l1111_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭௾")]:
    if bstack1l1111_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡕࡒࡁࡕࡈࡒࡖࡒࡏࡎࡅࡇ࡛ࠫ௿") in v:
      bstack1l1llllll_opy_.remove(v)
    if bstack1l1111_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘ࠭ఀ") in v:
      bstack1l1llllll_opy_.remove(v)
    if bstack1l1111_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡄࡆࡈࡏࡓࡈࡇࡌࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫఁ") in v:
      bstack1l1llllll_opy_.remove(v)
  bstack1l1llllll_opy_.insert(0, bstack1l1111_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡑࡎࡄࡘࡋࡕࡒࡎࡋࡑࡈࡊ࡞࠺ࡼࡿࠪం").format(bstack1ll11ll1_opy_.platform_index))
  bstack1l1llllll_opy_.insert(0, bstack1l1111_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡆࡈࡊࡑࡕࡃࡂࡎࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗࡀࡻࡾࠩః").format(bstack1ll11ll1_opy_.bstack1lllllll1_opy_))
  bstack1ll11ll1_opy_.options[bstack1l1111_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬఄ")] = bstack1l1llllll_opy_
  if bstack1ll1l11l11_opy_:
    bstack1ll11ll1_opy_.options[bstack1l1111_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭అ")].insert(0, bstack1l1111_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡒࡉࡂࡔࡊࡗ࠿ࢁࡽࠨఆ").format(bstack1ll1l11l11_opy_))
  return bstack1lll1ll1ll_opy_(caller_id, datasources, is_last, bstack1ll11ll1_opy_, outs_dir)
def bstack1l1lll1111_opy_(command, item_index):
  try:
    if bstack1llllll11l_opy_.get_property(bstack1l1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧఇ")):
      os.environ[bstack1l1111_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨఈ")] = json.dumps(CONFIG[bstack1l1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫఉ")][item_index % bstack11l1ll1l11_opy_])
    global bstack1ll1l11l11_opy_
    if bstack1ll1l11l11_opy_:
      command[0] = command[0].replace(bstack1l1111_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨఊ"), bstack1l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡶࡨࡰࠦࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠠ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࠣࠫఋ") + str(item_index % bstack11l1ll1l11_opy_) + bstack1l1111_opy_ (u"ࠫࠥ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠤࠬఌ") + str(
        item_index) + bstack1l1111_opy_ (u"ࠬࠦࠧ఍") + bstack1ll1l11l11_opy_, 1)
    else:
      command[0] = command[0].replace(bstack1l1111_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬఎ"),
                                      bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡳࡥ࡭ࠣࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠤ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࠠࠨఏ") +  str(item_index % bstack11l1ll1l11_opy_) + bstack1l1111_opy_ (u"ࠨࠢ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠡࠩఐ") + str(item_index), 1)
  except Exception as e:
    logger.error(bstack1l1111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡯ࡲࡨ࡮࡬ࡹࡪࡰࡪࠤࡨࡵ࡭࡮ࡣࡱࡨࠥ࡬࡯ࡳࠢࡳࡥࡧࡵࡴࠡࡴࡸࡲ࠿ࠦࡻࡾࠩ఑").format(str(e)))
def bstack111lll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1l1111ll11_opy_
  try:
    bstack1l1lll1111_opy_(command, item_index)
    return bstack1l1111ll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
  except Exception as e:
    logger.error(bstack1l1111_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡣࡱࡷࠤࡷࡻ࡮࠻ࠢࡾࢁࠬఒ").format(str(e)))
    raise e
def bstack1l11lll1l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1l1111ll11_opy_
  try:
    bstack1l1lll1111_opy_(command, item_index)
    return bstack1l1111ll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
  except Exception as e:
    logger.error(bstack1l1111_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡢࡤࡲࡸࠥࡸࡵ࡯ࠢ࠵࠲࠶࠹࠺ࠡࡽࢀࠫఓ").format(str(e)))
    try:
      return bstack1l1111ll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
    except Exception as e2:
      logger.error(bstack1l1111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡥࡳࡹࠦ࠲࠯࠳࠶ࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࡼࡿࠪఔ").format(str(e2)))
      raise e
def bstack1ll1ll1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1l1111ll11_opy_
  try:
    bstack1l1lll1111_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    return bstack1l1111ll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
  except Exception as e:
    logger.error(bstack1l1111_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠࡳࡷࡱࠤ࠷࠴࠱࠶࠼ࠣࡿࢂ࠭క").format(str(e)))
    try:
      return bstack1l1111ll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
    except Exception as e2:
      logger.error(bstack1l1111_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡧࡵࡴࠡ࠴࠱࠵࠺ࠦࡦࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢࡾࢁࠬఖ").format(str(e2)))
      raise e
def _11lll1l1_opy_(bstack111l1lll1l_opy_, item_index, process_timeout, sleep_before_start, bstack11l11lll11_opy_):
  bstack1l1lll1111_opy_(bstack111l1lll1l_opy_, item_index)
  if process_timeout is None:
    process_timeout = 3600
  if sleep_before_start and sleep_before_start > 0:
    time.sleep(min(sleep_before_start, 5))
  return process_timeout
def bstack11l1ll1ll1_opy_(command, bstack1l1111l11l_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack1l1111ll11_opy_
  global bstack1ll1lllll_opy_
  global bstack1ll1l11l11_opy_
  try:
    for env_name, bstack1lll11llll_opy_ in bstack1ll1lllll_opy_.items():
      os.environ[env_name] = bstack1lll11llll_opy_
    bstack1ll1l11l11_opy_ = bstack1l1111_opy_ (u"ࠣࠤగ")
    bstack1l1lll1111_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    if sleep_before_start and sleep_before_start > 0:
      time.sleep(min(sleep_before_start, 5))
    return bstack1l1111ll11_opy_(command, bstack1l1111l11l_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack1l1111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡢࡰࡶࠣࡶࡺࡴࠠ࠶࠰࠳࠾ࠥࢁࡽࠨఘ").format(str(e)))
    try:
      return bstack1l1111ll11_opy_(command, bstack1l1111l11l_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack1l1111_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡣࡱࡷࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࡼࡿࠪఙ").format(str(e2)))
      raise e
def bstack1l1ll11l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack1l1111ll11_opy_
  try:
    process_timeout = _11lll1l1_opy_(command, item_index, process_timeout, sleep_before_start, bstack1l1111_opy_ (u"ࠫ࠹࠴࠲ࠨచ"))
    return bstack1l1111ll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack1l1111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡥࡳࡹࠦࡲࡶࡰࠣ࠸࠳࠸࠺ࠡࡽࢀࠫఛ").format(str(e)))
    try:
      return bstack1l1111ll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack1l1111_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠࡧࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣࡿࢂ࠭జ").format(str(e2)))
      raise e
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack1l1l11ll1_opy_(self, runner, quiet=False, capture=True):
  global bstack1l1l11111l_opy_
  bstack11ll1lll_opy_ = bstack1l1l11111l_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack1l1111_opy_ (u"ࠧࡦࡺࡦࡩࡵࡺࡩࡰࡰࡢࡥࡷࡸࠧఝ")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1l1111_opy_ (u"ࠨࡧࡻࡧࡤࡺࡲࡢࡥࡨࡦࡦࡩ࡫ࡠࡣࡵࡶࠬఞ")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack11ll1lll_opy_
def bstack1l111111_opy_(runner, hook_name, context, element, bstack111l1l11l_opy_, *args):
  global bstack1111l1l11_opy_
  try:
    if runner.hooks.get(hook_name):
      bstack1llll1ll_opy_.bstack11ll111111_opy_(hook_name, element)
    if bstack1111l1l11_opy_ is None or bstack1111l1l11_opy_:
      bstack111l1l11l_opy_(runner, hook_name, context, *args)
    else:
      bstack1ll1ll1111_opy_ = (context,) + args
      bstack111l1l11l_opy_(runner, hook_name, *bstack1ll1ll1111_opy_)
    if runner.hooks.get(hook_name):
      bstack1llll1ll_opy_.bstack1l1l1lll_opy_(element)
      if hook_name not in [bstack1l1111_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱ࠭ట"), bstack1l1111_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ࠭ఠ")] and args and hasattr(args[0], bstack1l1111_opy_ (u"ࠫࡪࡸࡲࡰࡴࡢࡱࡪࡹࡳࡢࡩࡨࠫడ")):
        args[0].error_message = bstack1l1111_opy_ (u"ࠬ࠭ఢ")
  except Exception as e:
    logger.debug(bstack1l1111_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢ࡫ࡥࡳࡪ࡬ࡦࠢ࡫ࡳࡴࡱࡳࠡ࡫ࡱࠤࡧ࡫ࡨࡢࡸࡨ࠾ࠥࢁࡽࠨణ").format(str(e)))
@measure(event_name=EVENTS.bstack11ll11l111_opy_, stage=STAGE.bstack1111lll11_opy_, hook_type=bstack1l1111_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࡁ࡭࡮ࠥత"), bstack1l1l111l_opy_=bstack11l1111lll_opy_)
def bstack1l1ll111l_opy_(runner, name, context, bstack111l1l11l_opy_, *args):
    if runner.hooks.get(bstack1l1111_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧథ")).__name__ != bstack1l1111_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࡥࡤࡦࡨࡤࡹࡱࡺ࡟ࡩࡱࡲ࡯ࠧద"):
      bstack1l111111_opy_(runner, name, context, runner, bstack111l1l11l_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack11l1l11l_opy_(bstack1l1111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩధ")) else context.browser
      runner.driver_initialised = bstack1l1111_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣన")
    except Exception as e:
      logger.debug(bstack1l1111_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡪࡲࡪࡸࡨࡶࠥ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡳࡦࠢࡤࡸࡹࡸࡩࡣࡷࡷࡩ࠿ࠦࡻࡾࠩ఩").format(str(e)))
def bstack1l111l1lll_opy_(runner, name, context, bstack111l1l11l_opy_, *args):
    bstack1l111111_opy_(runner, name, context, context.feature, bstack111l1l11l_opy_, *args)
    try:
      if not bstack1l1lll11l_opy_:
        bstack1l1llll111_opy_ = threading.current_thread().bstackSessionDriver if bstack11l1l11l_opy_(bstack1l1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬప")) else context.browser
        if is_driver_active(bstack1l1llll111_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack1l1111_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣఫ")
          bstack11l1lll1_opy_ = str(runner.feature.name)
          bstack1llll1ll1_opy_(context, bstack11l1lll1_opy_)
          bstack1l1llll111_opy_.execute_script(bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭బ") + json.dumps(bstack11l1lll1_opy_) + bstack1l1111_opy_ (u"ࠩࢀࢁࠬభ"))
    except Exception as e:
      logger.debug(bstack1l1111_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡬ࡥࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪమ").format(str(e)))
def bstack1ll11l1ll_opy_(runner, name, context, bstack111l1l11l_opy_, *args):
    target = context.scenario if hasattr(context, bstack1l1111_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭య")) else context.feature
    bstack1l111111_opy_(runner, name, context, target, bstack111l1l11l_opy_, *args)
@measure(event_name=EVENTS.bstack111lll111l_opy_, stage=STAGE.bstack1111lll11_opy_, bstack1l1l111l_opy_=bstack11l1111lll_opy_)
def bstack11ll1111l_opy_(runner, name, context, bstack111l1l11l_opy_, *args):
    bstack1llll1ll_opy_.start_test(context)
    bstack1l111111_opy_(runner, name, context, context.scenario, bstack111l1l11l_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack1l111llll1_opy_.bstack11ll1ll1l_opy_(context, *args)
    try:
      bstack1l1llll111_opy_ = bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫర"), context.browser)
      if is_driver_active(bstack1l1llll111_opy_):
        bstack11l11111l_opy_.bstack111lll1ll1_opy_(bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬఱ"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack1l1111_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤల")
        if (not bstack1l1lll11l_opy_):
          scenario_name = args[0].name
          feature_name = bstack11l1lll1_opy_ = str(runner.feature.name)
          bstack11l1lll1_opy_ = feature_name + bstack1l1111_opy_ (u"ࠨࠢ࠰ࠤࠬళ") + scenario_name
          if runner.driver_initialised == bstack1l1111_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦఴ"):
            bstack1llll1ll1_opy_(context, bstack11l1lll1_opy_)
            bstack1l1llll111_opy_.execute_script(bstack1l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨవ") + json.dumps(bstack11l1lll1_opy_) + bstack1l1111_opy_ (u"ࠫࢂࢃࠧశ"))
    except Exception as e:
      logger.debug(bstack1l1111_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤ࡮ࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡥࡨࡲࡦࡸࡩࡰ࠼ࠣࡿࢂ࠭ష").format(str(e)))
@measure(event_name=EVENTS.bstack11ll11l111_opy_, stage=STAGE.bstack1111lll11_opy_, hook_type=bstack1l1111_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪ࡙ࡴࡦࡲࠥస"), bstack1l1l111l_opy_=bstack11l1111lll_opy_)
def bstack111lll11l1_opy_(runner, name, context, bstack111l1l11l_opy_, *args):
    bstack1l111111_opy_(runner, name, context, args[0], bstack111l1l11l_opy_, *args)
    try:
      bstack1l1llll111_opy_ = threading.current_thread().bstackSessionDriver if bstack11l1l11l_opy_(bstack1l1111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭హ")) else context.browser
      if is_driver_active(bstack1l1llll111_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack1l1111_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨ఺")
        bstack1llll1ll_opy_.bstack1ll1ll11ll_opy_(args[0])
        if runner.driver_initialised == bstack1l1111_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢ఻"):
          feature_name = bstack11l1lll1_opy_ = str(runner.feature.name)
          bstack11l1lll1_opy_ = feature_name + bstack1l1111_opy_ (u"ࠪࠤ࠲఼ࠦࠧ") + context.scenario.name
          bstack1l1llll111_opy_.execute_script(bstack1l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩఽ") + json.dumps(bstack11l1lll1_opy_) + bstack1l1111_opy_ (u"ࠬࢃࡽࠨా"))
    except Exception as e:
      logger.debug(bstack1l1111_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡷࡩࡵࡀࠠࡼࡿࠪి").format(str(e)))
@measure(event_name=EVENTS.bstack11ll11l111_opy_, stage=STAGE.bstack1111lll11_opy_, hook_type=bstack1l1111_opy_ (u"ࠢࡢࡨࡷࡩࡷ࡙ࡴࡦࡲࠥీ"), bstack1l1l111l_opy_=bstack11l1111lll_opy_)
def bstack1l1111l1l1_opy_(runner, name, context, bstack111l1l11l_opy_, *args):
  bstack1llll1ll_opy_.bstack1l11l1l11_opy_(args[0])
  try:
    step_status = args[0].status.name
    bstack1l1llll111_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧు") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack1l1llll111_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack1l1111_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩూ")
        feature_name = bstack11l1lll1_opy_ = str(runner.feature.name)
        bstack11l1lll1_opy_ = feature_name + bstack1l1111_opy_ (u"ࠪࠤ࠲ࠦࠧృ") + context.scenario.name
        bstack1l1llll111_opy_.execute_script(bstack1l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩౄ") + json.dumps(bstack11l1lll1_opy_) + bstack1l1111_opy_ (u"ࠬࢃࡽࠨ౅"))
    if str(step_status).lower() in [bstack1l1111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ె"), bstack1l1111_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ే")]:
      bstack11l1l1l11_opy_ = bstack1l1111_opy_ (u"ࠨࠩై")
      bstack1ll11111_opy_ = bstack1l1111_opy_ (u"ࠩࠪ౉")
      bstack1l11l11l11_opy_ = bstack1l1111_opy_ (u"ࠪࠫొ")
      try:
        import traceback
        bstack11l1l1l11_opy_ = runner.exception.__class__.__name__
        bstack111llll11_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1ll11111_opy_ = bstack1l1111_opy_ (u"ࠫࠥ࠭ో").join(bstack111llll11_opy_)
        bstack1l11l11l11_opy_ = bstack111llll11_opy_[-1]
      except Exception as e:
        logger.debug(bstack11111l11_opy_.format(str(e)))
      bstack11l1l1l11_opy_ += bstack1l11l11l11_opy_
      bstack11l1ll111_opy_(context, json.dumps(str(args[0].name) + bstack1l1111_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦౌ") + str(bstack1ll11111_opy_)),
                          bstack1l1111_opy_ (u"ࠨࡥࡳࡴࡲࡶ్ࠧ"))
      if runner.driver_initialised == bstack1l1111_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧ౎"):
        bstack1llll1lll1_opy_(getattr(context, bstack1l1111_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭౏"), None), bstack1l1111_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ౐"), bstack11l1l1l11_opy_)
        bstack1l1llll111_opy_.execute_script(bstack1l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨ౑") + json.dumps(str(args[0].name) + bstack1l1111_opy_ (u"ࠦࠥ࠳ࠠࡇࡣ࡬ࡰࡪࡪࠡ࡝ࡰࠥ౒") + str(bstack1ll11111_opy_)) + bstack1l1111_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥࡩࡷࡸ࡯ࡳࠤࢀࢁࠬ౓"))
      if runner.driver_initialised == bstack1l1111_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦ౔"):
        bstack1l111l1ll_opy_(bstack1l1llll111_opy_, bstack1l1111_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪౕࠧ"), bstack1l1111_opy_ (u"ࠣࡕࡦࡩࡳࡧࡲࡪࡱࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲౖࠧ") + str(bstack11l1l1l11_opy_))
    else:
      bstack11l1ll111_opy_(context, bstack1l1111_opy_ (u"ࠤࡓࡥࡸࡹࡥࡥࠣࠥ౗"), bstack1l1111_opy_ (u"ࠥ࡭ࡳ࡬࡯ࠣౘ"))
      if runner.driver_initialised == bstack1l1111_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤౙ"):
        bstack1llll1lll1_opy_(getattr(context, bstack1l1111_opy_ (u"ࠬࡶࡡࡨࡧࠪౚ"), None), bstack1l1111_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ౛"))
      bstack1l1llll111_opy_.execute_script(bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ౜") + json.dumps(str(args[0].name) + bstack1l1111_opy_ (u"ࠣࠢ࠰ࠤࡕࡧࡳࡴࡧࡧࠥࠧౝ")) + bstack1l1111_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧࢃࡽࠨ౞"))
      if runner.driver_initialised == bstack1l1111_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣ౟"):
        bstack1l111l1ll_opy_(bstack1l1llll111_opy_, bstack1l1111_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦౠ"))
  except Exception as e:
    logger.debug(bstack1l1111_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡶࡸࡪࡶ࠺ࠡࡽࢀࠫౡ").format(str(e)))
  bstack1l111111_opy_(runner, name, context, args[0], bstack111l1l11l_opy_, *args)
@measure(event_name=EVENTS.bstack11llllll1_opy_, stage=STAGE.bstack1111lll11_opy_, bstack1l1l111l_opy_=bstack11l1111lll_opy_)
def bstack111l11l1_opy_(runner, name, context, bstack111l1l11l_opy_, *args):
  bstack1llll1ll_opy_.end_test(args[0])
  try:
    bstack1lllll111l_opy_ = args[0].status.name
    bstack1l1llll111_opy_ = bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬౢ"), context.browser)
    bstack1l111llll1_opy_.bstack1l1l1l1lll_opy_(bstack1l1llll111_opy_)
    if str(bstack1lllll111l_opy_).lower() in [bstack1l1111_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧౣ"), bstack1l1111_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ౤")]:
      bstack11l1l1l11_opy_ = bstack1l1111_opy_ (u"ࠩࠪ౥")
      bstack1ll11111_opy_ = bstack1l1111_opy_ (u"ࠪࠫ౦")
      bstack1l11l11l11_opy_ = bstack1l1111_opy_ (u"ࠫࠬ౧")
      try:
        import traceback
        bstack11l1l1l11_opy_ = runner.exception.__class__.__name__
        bstack111llll11_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1ll11111_opy_ = bstack1l1111_opy_ (u"ࠬࠦࠧ౨").join(bstack111llll11_opy_)
        bstack1l11l11l11_opy_ = bstack111llll11_opy_[-1]
      except Exception as e:
        logger.debug(bstack11111l11_opy_.format(str(e)))
      bstack11l1l1l11_opy_ += bstack1l11l11l11_opy_
      bstack11l1ll111_opy_(context, json.dumps(str(args[0].name) + bstack1l1111_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧ౩") + str(bstack1ll11111_opy_)),
                          bstack1l1111_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨ౪"))
      if runner.driver_initialised == bstack1l1111_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥ౫") or runner.driver_initialised == bstack1l1111_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩ౬"):
        bstack1llll1lll1_opy_(getattr(context, bstack1l1111_opy_ (u"ࠪࡴࡦ࡭ࡥࠨ౭"), None), bstack1l1111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ౮"), bstack11l1l1l11_opy_)
        bstack1l1llll111_opy_.execute_script(bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ౯") + json.dumps(str(args[0].name) + bstack1l1111_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧ౰") + str(bstack1ll11111_opy_)) + bstack1l1111_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦࢂࢃࠧ౱"))
      if runner.driver_initialised == bstack1l1111_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥ౲") or runner.driver_initialised == bstack1l1111_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩ౳"):
        bstack1l111l1ll_opy_(bstack1l1llll111_opy_, bstack1l1111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ౴"), bstack1l1111_opy_ (u"ࠦࡘࡩࡥ࡯ࡣࡵ࡭ࡴࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࡢ࡮ࠣ౵") + str(bstack11l1l1l11_opy_))
    else:
      bstack11l1ll111_opy_(context, bstack1l1111_opy_ (u"ࠧࡖࡡࡴࡵࡨࡨࠦࠨ౶"), bstack1l1111_opy_ (u"ࠨࡩ࡯ࡨࡲࠦ౷"))
      if runner.driver_initialised == bstack1l1111_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤ౸") or runner.driver_initialised == bstack1l1111_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨ౹"):
        bstack1llll1lll1_opy_(getattr(context, bstack1l1111_opy_ (u"ࠩࡳࡥ࡬࡫ࠧ౺"), None), bstack1l1111_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ౻"))
      bstack1l1llll111_opy_.execute_script(bstack1l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ౼") + json.dumps(str(args[0].name) + bstack1l1111_opy_ (u"ࠧࠦ࠭ࠡࡒࡤࡷࡸ࡫ࡤࠢࠤ౽")) + bstack1l1111_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤࢀࢁࠬ౾"))
      if runner.driver_initialised == bstack1l1111_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤ౿") or runner.driver_initialised == bstack1l1111_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨಀ"):
        bstack1l111l1ll_opy_(bstack1l1llll111_opy_, bstack1l1111_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤಁ"))
  except Exception as e:
    logger.debug(bstack1l1111_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡯࡮ࠡࡣࡩࡸࡪࡸࠠࡧࡧࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬಂ").format(str(e)))
  bstack1l111111_opy_(runner, name, context, context.scenario, bstack111l1l11l_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack1l11l111l_opy_(runner, name, context, bstack111l1l11l_opy_, *args):
    target = context.scenario if hasattr(context, bstack1l1111_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ಃ")) else context.feature
    bstack1l111111_opy_(runner, name, context, target, bstack111l1l11l_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack11l111l11_opy_(runner, name, context, bstack111l1l11l_opy_, *args):
    try:
      bstack1l1llll111_opy_ = bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ಄"), context.browser)
      bstack1l11111l1l_opy_ = bstack1l1111_opy_ (u"࠭ࠧಅ")
      if context.failed is True:
        bstack11l11l11_opy_ = []
        bstack11l1l1lll_opy_ = []
        bstack111l11l111_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack11l11l11_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack111llll11_opy_ = traceback.format_tb(exc_tb)
            bstack1l11ll11ll_opy_ = bstack1l1111_opy_ (u"ࠧࠡࠩಆ").join(bstack111llll11_opy_)
            bstack11l1l1lll_opy_.append(bstack1l11ll11ll_opy_)
            bstack111l11l111_opy_.append(bstack111llll11_opy_[-1])
        except Exception as e:
          logger.debug(bstack11111l11_opy_.format(str(e)))
        bstack11l1l1l11_opy_ = bstack1l1111_opy_ (u"ࠨࠩಇ")
        for i in range(len(bstack11l11l11_opy_)):
          bstack11l1l1l11_opy_ += bstack11l11l11_opy_[i] + bstack111l11l111_opy_[i] + bstack1l1111_opy_ (u"ࠩ࡟ࡲࠬಈ")
        bstack1l11111l1l_opy_ = bstack1l1111_opy_ (u"ࠪࠤࠬಉ").join(bstack11l1l1lll_opy_)
        if runner.driver_initialised in [bstack1l1111_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠧಊ"), bstack1l1111_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤಋ")]:
          bstack11l1ll111_opy_(context, bstack1l11111l1l_opy_, bstack1l1111_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧಌ"))
          bstack1llll1lll1_opy_(getattr(context, bstack1l1111_opy_ (u"ࠧࡱࡣࡪࡩࠬ಍"), None), bstack1l1111_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣಎ"), bstack11l1l1l11_opy_)
          bstack1l1llll111_opy_.execute_script(bstack1l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧಏ") + json.dumps(bstack1l11111l1l_opy_) + bstack1l1111_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪಐ"))
          bstack1l111l1ll_opy_(bstack1l1llll111_opy_, bstack1l1111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ಑"), bstack1l1111_opy_ (u"࡙ࠧ࡯࡮ࡧࠣࡷࡨ࡫࡮ࡢࡴ࡬ࡳࡸࠦࡦࡢ࡫࡯ࡩࡩࡀࠠ࡝ࡰࠥಒ") + str(bstack11l1l1l11_opy_))
          bstack1ll1l1ll_opy_ = bstack1llllll111_opy_(bstack1l11111l1l_opy_, runner.feature.name, logger)
          if (bstack1ll1l1ll_opy_ != None):
            bstack111l1ll1ll_opy_.append(bstack1ll1l1ll_opy_)
      else:
        if runner.driver_initialised in [bstack1l1111_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠢಓ"), bstack1l1111_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦಔ")]:
          bstack11l1ll111_opy_(context, bstack1l1111_opy_ (u"ࠣࡈࡨࡥࡹࡻࡲࡦ࠼ࠣࠦಕ") + str(runner.feature.name) + bstack1l1111_opy_ (u"ࠤࠣࡴࡦࡹࡳࡦࡦࠤࠦಖ"), bstack1l1111_opy_ (u"ࠥ࡭ࡳ࡬࡯ࠣಗ"))
          bstack1llll1lll1_opy_(getattr(context, bstack1l1111_opy_ (u"ࠫࡵࡧࡧࡦࠩಘ"), None), bstack1l1111_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧಙ"))
          bstack1l1llll111_opy_.execute_script(bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫಚ") + json.dumps(bstack1l1111_opy_ (u"ࠢࡇࡧࡤࡸࡺࡸࡥ࠻ࠢࠥಛ") + str(runner.feature.name) + bstack1l1111_opy_ (u"ࠣࠢࡳࡥࡸࡹࡥࡥࠣࠥಜ")) + bstack1l1111_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧࢃࡽࠨಝ"))
          bstack1l111l1ll_opy_(bstack1l1llll111_opy_, bstack1l1111_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪಞ"))
          bstack1ll1l1ll_opy_ = bstack1llllll111_opy_(bstack1l11111l1l_opy_, runner.feature.name, logger)
          if (bstack1ll1l1ll_opy_ != None):
            bstack111l1ll1ll_opy_.append(bstack1ll1l1ll_opy_)
    except Exception as e:
      logger.debug(bstack1l1111_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭ಟ").format(str(e)))
    bstack1l111111_opy_(runner, name, context, context.feature, bstack111l1l11l_opy_, *args)
@measure(event_name=EVENTS.bstack11ll11l111_opy_, stage=STAGE.bstack1111lll11_opy_, hook_type=bstack1l1111_opy_ (u"ࠧࡧࡦࡵࡧࡵࡅࡱࡲࠢಠ"), bstack1l1l111l_opy_=bstack11l1111lll_opy_)
def bstack11l11l1ll1_opy_(runner, name, context, bstack111l1l11l_opy_, *args):
    bstack1l111111_opy_(runner, name, context, runner, bstack111l1l11l_opy_, *args)
def bstack1l11lll1_opy_(self, filename=None):
  bstack1l1111_opy_ (u"ࠨࠢࠣࠌࠣࠤࡑࡵࡡࡥࠢ࡫ࡳࡴࡱࡳࠡࡣࡱࡨࠥ࡫࡮ࡴࡷࡵࡩࠥࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵ࠯ࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠡࡣࡵࡩࠥࡸࡥࡨ࡫ࡶࡸࡪࡸࡥࡥ࠰ࠍࠤࠥࡈࡥࡩࡣࡹࡩࠥࡼ࠱࠯࠵࠮ࠤࡩࡵࡥࡴࡰࠪࡸࠥࡩࡡ࡭࡮ࠣࡶࡺࡴࠠࡩࡱࡲ࡯ࡸࠦࡴࡩࡣࡷࠤࡦࡸࡥ࡯ࠩࡷࠤࡩ࡫ࡦࡪࡰࡨࡨ࠱ࠦࡳࡰࠢࡺࡩࠥࡳࡵࡴࡶࠍࠤࠥࡪ࡯ࠡࡶ࡫࡭ࡸࠦࡥࡹࡲ࡯࡭ࡨ࡯ࡴ࡭ࡻࠣࡸࡴࠦ࡭ࡢ࡭ࡨࠤࡸࡻࡲࡦࠢࡺࡩࠬࡸࡥࠡࡥࡤࡰࡱ࡫ࡤࠡ࡫ࡱࠤࡦࡴࡹࠡࡥࡤࡷࡪ࠴ࠊࠡࠢࠥࠦࠧಡ")
  global bstack1lll111l_opy_
  bstack1lll111l_opy_(self, filename)
  bstack1ll1ll111l_opy_ = []
  bstack1llll11ll1_opy_ = [bstack1l1111_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠨಢ"), bstack1l1111_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡶࡤ࡫ࠬಣ"), bstack1l1111_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫತ"), bstack1l1111_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫಥ"), bstack1l1111_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡸࡦ࡭ࠧದ"), bstack1l1111_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬಧ")]
  bstack11llll1l1_opy_ = lambda *_: None
  for hook_name in bstack1llll11ll1_opy_:
    if hook_name not in self.hooks:
      self.hooks[hook_name] = bstack11llll1l1_opy_
      bstack1ll1ll111l_opy_.append(hook_name)
  if bstack1ll1ll111l_opy_:
    os.environ[bstack1l1111_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡓࡅࡍࡢࡈࡊࡌࡁࡖࡎࡗࡣࡍࡕࡏࡌࡕࠪನ")] = bstack1l1111_opy_ (u"ࠧ࠭ࠩ಩").join(bstack1ll1ll111l_opy_)
def bstack1lll1lll11_opy_(self, name, *args):
  global bstack111l1l11l_opy_
  global bstack1111l1l11_opy_
  try:
    if bstack1l1llll1l1_opy_:
      platform_index = int(threading.current_thread()._name) % bstack11l1ll1l11_opy_
      bstack11111l111_opy_ = CONFIG[bstack1l1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫಪ")][platform_index]
      os.environ[bstack1l1111_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪಫ")] = json.dumps(bstack11111l111_opy_)
    if not hasattr(self, bstack1l1111_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡸ࡫ࡤࠨಬ")):
      self.driver_initialised = None
    bstack11lllll11_opy_ = {
        bstack1l1111_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠨಭ"): bstack1l1ll111l_opy_,
        bstack1l1111_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ಮ"): bstack1l111l1lll_opy_,
        bstack1l1111_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡴࡢࡩࠪಯ"): bstack1ll11l1ll_opy_,
        bstack1l1111_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩರ"): bstack11ll1111l_opy_,
        bstack1l1111_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵ࠭ಱ"): bstack111lll11l1_opy_,
        bstack1l1111_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡷࡩࡵ࠭ಲ"): bstack1l1111l1l1_opy_,
        bstack1l1111_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫಳ"): bstack111l11l1_opy_,
        bstack1l1111_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡸࡦ࡭ࠧ಴"): bstack1l11l111l_opy_,
        bstack1l1111_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬವ"): bstack11l111l11_opy_,
        bstack1l1111_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠩಶ"): bstack11l11l1ll1_opy_
    }
    handler = bstack11lllll11_opy_.get(name, bstack111l1l11l_opy_)
    try:
      if args:
        context = args[0]
        remaining_args = args[1:]
        if bstack1111l1l11_opy_ is None or not bstack1111l1l11_opy_:
          context = self.context
          remaining_args = args
      else:
        context = self.context
        remaining_args = ()
      handler(self, name, context, bstack111l1l11l_opy_, *remaining_args)
    except Exception as e:
      logger.debug(bstack1l1111_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡥࡩ࡭ࡧࡶࡦࠢ࡫ࡳࡴࡱࠠࡩࡣࡱࡨࡱ࡫ࡲࠡࡽࢀ࠾ࠥࢁࡽࠨಷ").format(name, str(e)))
    if name in [bstack1l1111_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨಸ"), bstack1l1111_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪಹ"), bstack1l1111_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ࠭಺")]:
      try:
        bstack1l1llll111_opy_ = threading.current_thread().bstackSessionDriver if bstack11l1l11l_opy_(bstack1l1111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ಻")) else context.browser
        bstack11l1111l11_opy_ = (
          (name == bstack1l1111_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠨ಼") and self.driver_initialised == bstack1l1111_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥಽ")) or
          (name == bstack1l1111_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡦࡦࡣࡷࡹࡷ࡫ࠧಾ") and self.driver_initialised == bstack1l1111_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠤಿ")) or
          (name == bstack1l1111_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪೀ") and self.driver_initialised in [bstack1l1111_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧು"), bstack1l1111_opy_ (u"ࠦ࡮ࡴࡳࡵࡧࡳࠦೂ")]) or
          (name == bstack1l1111_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡺࡥࡱࠩೃ") and self.driver_initialised == bstack1l1111_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦೄ"))
        )
        if bstack11l1111l11_opy_:
          self.driver_initialised = None
          if bstack1l1llll111_opy_ and hasattr(bstack1l1llll111_opy_, bstack1l1111_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠫ೅")):
            try:
              bstack1l1llll111_opy_.quit()
            except Exception as e:
              logger.debug(bstack1l1111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡲࡷ࡬ࡸࡹ࡯࡮ࡨࠢࡧࡶ࡮ࡼࡥࡳࠢ࡬ࡲࠥࡨࡥࡩࡣࡹࡩࠥ࡮࡯ࡰ࡭࠽ࠤࢀࢃࠧೆ").format(str(e)))
      except Exception as e:
        logger.debug(bstack1l1111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࠣ࡬ࡴࡵ࡫ࠡࡥ࡯ࡩࡦࡴࡵࡱࠢࡩࡳࡷࠦࡻࡾ࠼ࠣࡿࢂ࠭ೇ").format(name, str(e)))
  except Exception as e:
    logger.debug(bstack1l1111_opy_ (u"ࠪࡇࡷ࡯ࡴࡪࡥࡤࡰࠥ࡫ࡲࡳࡱࡵࠤ࡮ࡴࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡳࡷࡱࠤ࡭ࡵ࡯࡬ࠢࡾࢁ࠿ࠦࡻࡾࠩೈ").format(name, str(e)))
    try:
      if bstack1111l1l11_opy_ is None or bstack1111l1l11_opy_:
        try:
          bstack111l1l11l_opy_(self, name, self.context, *args)
        except TypeError:
          bstack111l1l11l_opy_(self, name, *args)
      else:
        bstack111l1l11l_opy_(self, name, *args)
    except Exception as e2:
      logger.debug(bstack1l1111_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࠣࡦࡪ࡮ࡡࡷࡧࠣ࡬ࡴࡵ࡫ࠡࡽࢀ࠾ࠥࢁࡽࠨ೉").format(name, str(e2)))
def bstack1l1111111l_opy_(config, startdir):
  return bstack1l1111_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶ࠿ࠦࡻ࠱ࡿࠥೊ").format(bstack1l1111_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧೋ"))
notset = Notset()
def bstack11l111llll_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1ll1l1l1l_opy_
  if str(name).lower() == bstack1l1111_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸࠧೌ"):
    return bstack1l1111_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱ್ࠢ")
  else:
    return bstack1ll1l1l1l_opy_(self, name, default, skip)
def bstack1l11ll11_opy_(item, when):
  global bstack1l1l1llll_opy_
  try:
    bstack1l1l1llll_opy_(item, when)
  except Exception as e:
    pass
def bstack11lllll11l_opy_():
  return
def bstack1lll1l1l_opy_(type, name, status, reason, bstack11ll11llll_opy_, bstack1ll1l11ll1_opy_):
  bstack11ll1l11l1_opy_ = {
    bstack1l1111_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩ೎"): type,
    bstack1l1111_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭೏"): {}
  }
  if type == bstack1l1111_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭೐"):
    bstack11ll1l11l1_opy_[bstack1l1111_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ೑")][bstack1l1111_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ೒")] = bstack11ll11llll_opy_
    bstack11ll1l11l1_opy_[bstack1l1111_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ೓")][bstack1l1111_opy_ (u"ࠨࡦࡤࡸࡦ࠭೔")] = json.dumps(str(bstack1ll1l11ll1_opy_))
  if type == bstack1l1111_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪೕ"):
    bstack11ll1l11l1_opy_[bstack1l1111_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ೖ")][bstack1l1111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ೗")] = name
  if type == bstack1l1111_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ೘"):
    bstack11ll1l11l1_opy_[bstack1l1111_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ೙")][bstack1l1111_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ೚")] = status
    if status == bstack1l1111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ೛"):
      bstack11ll1l11l1_opy_[bstack1l1111_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ೜")][bstack1l1111_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪೝ")] = json.dumps(str(reason))
  bstack11l1l11l1l_opy_ = bstack1l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩೞ").format(json.dumps(bstack11ll1l11l1_opy_))
  return bstack11l1l11l1l_opy_
def bstack111l1l11l1_opy_(driver_command, response):
    if driver_command == bstack1l1111_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠩ೟"):
        bstack11l11111l_opy_.bstack11l1l1l1l_opy_({
            bstack1l1111_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬೠ"): response[bstack1l1111_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭ೡ")],
            bstack1l1111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨೢ"): bstack11l11111l_opy_.current_test_uuid()
        })
def bstack11111llll_opy_(item, call, rep):
  global bstack11lll1lll1_opy_
  global bstack1l1lll11ll_opy_
  global bstack1l1lll11l_opy_
  name = bstack1l1111_opy_ (u"ࠩࠪೣ")
  try:
    if rep.when == bstack1l1111_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ೤"):
      bstack11lll1llll_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1l1lll11l_opy_:
          name = str(rep.nodeid)
          bstack1l1l1l1l_opy_ = bstack1lll1l1l_opy_(bstack1l1111_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ೥"), name, bstack1l1111_opy_ (u"ࠬ࠭೦"), bstack1l1111_opy_ (u"࠭ࠧ೧"), bstack1l1111_opy_ (u"ࠧࠨ೨"), bstack1l1111_opy_ (u"ࠨࠩ೩"))
          threading.current_thread().bstack1ll1l1llll_opy_ = name
          for driver in bstack1l1lll11ll_opy_:
            if bstack11lll1llll_opy_ == driver.session_id:
              driver.execute_script(bstack1l1l1l1l_opy_)
      except Exception as e:
        logger.debug(bstack1l1111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩ೪").format(str(e)))
      try:
        bstack1l1lll111_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack1l1111_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ೫"):
          status = bstack1l1111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ೬") if rep.outcome.lower() == bstack1l1111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ೭") else bstack1l1111_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭೮")
          reason = bstack1l1111_opy_ (u"ࠧࠨ೯")
          if status == bstack1l1111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ೰"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack1l1111_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧೱ") if status == bstack1l1111_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪೲ") else bstack1l1111_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪೳ")
          data = name + bstack1l1111_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧ೴") if status == bstack1l1111_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭೵") else name + bstack1l1111_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠢࠢࠪ೶") + reason
          bstack1lll11111l_opy_ = bstack1lll1l1l_opy_(bstack1l1111_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪ೷"), bstack1l1111_opy_ (u"ࠩࠪ೸"), bstack1l1111_opy_ (u"ࠪࠫ೹"), bstack1l1111_opy_ (u"ࠫࠬ೺"), level, data)
          for driver in bstack1l1lll11ll_opy_:
            if bstack11lll1llll_opy_ == driver.session_id:
              driver.execute_script(bstack1lll11111l_opy_)
      except Exception as e:
        logger.debug(bstack1l1111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡦࡳࡳࡺࡥࡹࡶࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩ೻").format(str(e)))
  except Exception as e:
    logger.debug(bstack1l1111_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡶࡸࡦࡺࡥࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼࡿࠪ೼").format(str(e)))
  bstack11lll1lll1_opy_(item, call, rep)
def bstack1l1lllllll_opy_(driver, bstack111l11lll_opy_, test=None):
  global bstack1l1llll11_opy_
  if test != None:
    bstack1ll11l11l_opy_ = getattr(test, bstack1l1111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ೽"), None)
    bstack1111l1ll1_opy_ = getattr(test, bstack1l1111_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭೾"), None)
    PercySDK.screenshot(driver, bstack111l11lll_opy_, bstack1ll11l11l_opy_=bstack1ll11l11l_opy_, bstack1111l1ll1_opy_=bstack1111l1ll1_opy_, bstack1lll111111_opy_=bstack1l1llll11_opy_)
  else:
    PercySDK.screenshot(driver, bstack111l11lll_opy_)
@measure(event_name=EVENTS.bstack1l11111ll_opy_, stage=STAGE.bstack1111lll11_opy_, bstack1l1l111l_opy_=bstack11l1111lll_opy_)
def bstack111l1l1l1l_opy_(driver):
  if bstack1ll1l11l1_opy_.bstack11l111ll_opy_() is True or bstack1ll1l11l1_opy_.capturing() is True:
    return
  bstack1ll1l11l1_opy_.bstack1l1ll111ll_opy_()
  while not bstack1ll1l11l1_opy_.bstack11l111ll_opy_():
    bstack1l1l1l1l11_opy_ = bstack1ll1l11l1_opy_.bstack1l111lllll_opy_()
    bstack1l1lllllll_opy_(driver, bstack1l1l1l1l11_opy_)
  bstack1ll1l11l1_opy_.bstack1ll111lll_opy_()
def bstack1l1l1lll1_opy_(sequence, driver_command, response = None, bstack11l11llll_opy_ = None, args = None):
    try:
      if sequence != bstack1l1111_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩ೿"):
        return
      if percy.bstack11l1llllll_opy_() == bstack1l1111_opy_ (u"ࠥࡪࡦࡲࡳࡦࠤഀ"):
        return
      bstack1l1l1l1l11_opy_ = bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧഁ"), None)
      for command in bstack111ll1l1l1_opy_:
        if command == driver_command:
          with bstack11l1l11111_opy_:
            bstack1l1l11111_opy_ = bstack1l1lll11ll_opy_.copy()
          for driver in bstack1l1l11111_opy_:
            bstack111l1l1l1l_opy_(driver)
      bstack1l11llll1l_opy_ = percy.bstack11llllll11_opy_()
      if driver_command in bstack1l11lllll_opy_[bstack1l11llll1l_opy_]:
        bstack1ll1l11l1_opy_.bstack111l1llll_opy_(bstack1l1l1l1l11_opy_, driver_command)
    except Exception as e:
      pass
def bstack1lll1l1lll_opy_(framework_name):
  if bstack1llllll11l_opy_.get_property(bstack1l1111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩം")):
      return
  bstack1llllll11l_opy_.bstack11l1l111ll_opy_(bstack1l1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪഃ"), True)
  global bstack111l111l_opy_
  global bstack1ll11l1l_opy_
  global bstack1l1ll11ll1_opy_
  bstack111l111l_opy_ = framework_name
  logger.info(bstack11l1111ll_opy_.format(bstack111l111l_opy_.split(bstack1l1111_opy_ (u"ࠧ࠮ࠩഄ"))[0]))
  bstack1l1l1l1l1l_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1l1llll1l1_opy_:
      Service.start = bstack1l111l111_opy_
      Service.stop = bstack111ll1ll1l_opy_
      webdriver.Remote.get = bstack1l111ll1ll_opy_
      WebDriver.quit = bstack111ll11111_opy_
      webdriver.Remote.__init__ = bstack1l1ll11l_opy_
    if not bstack1l1llll1l1_opy_:
        webdriver.Remote.__init__ = bstack11llll1lll_opy_
    WebDriver.getAccessibilityResults = getAccessibilityResults
    WebDriver.get_accessibility_results = getAccessibilityResults
    WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
    WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
    WebDriver.performScan = perform_scan
    WebDriver.perform_scan = perform_scan
    WebDriver.execute = bstack11l111ll1_opy_
    bstack1ll11l1l_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack1l1llll1l1_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack11llll111_opy_
  except Exception as e:
    pass
  bstack111l1l11ll_opy_()
  if not bstack1ll11l1l_opy_:
    bstack111l1l11_opy_(bstack1l1111_opy_ (u"ࠣࡒࡤࡧࡰࡧࡧࡦࡵࠣࡲࡴࡺࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠥഅ"), bstack111ll11l1_opy_)
  if bstack1lll1l1111_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      if hasattr(RemoteConnection, bstack1l1111_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪആ")) and callable(getattr(RemoteConnection, bstack1l1111_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫഇ"))):
        RemoteConnection._get_proxy_url = bstack111llll11l_opy_
      else:
        from selenium.webdriver.remote.client_config import ClientConfig
        ClientConfig.get_proxy_url = bstack111llll11l_opy_
    except Exception as e:
      logger.error(bstack111111111_opy_.format(str(e)))
  if bstack11l111l11l_opy_():
    bstack11111ll1_opy_(CONFIG, logger)
  if (bstack1l1111_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪഈ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if percy.bstack11l1llllll_opy_() == bstack1l1111_opy_ (u"ࠧࡺࡲࡶࡧࠥഉ"):
          bstack1lll1l1l11_opy_(bstack1l1l1lll1_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack11l11l111l_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack11lll1ll1_opy_
      except Exception as e:
        logger.warning(bstack1lll11l11_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1111llll_opy_
      except Exception as e:
        logger.debug(bstack1ll111111l_opy_ + str(e))
    except Exception as e:
      bstack111l1l11_opy_(e, bstack1lll11l11_opy_)
    Output.start_test = bstack1ll1ll1l1_opy_
    Output.end_test = bstack1l11ll1l11_opy_
    TestStatus.__init__ = bstack1lll11ll1_opy_
    QueueItem.__init__ = bstack11ll1ll1ll_opy_
    pabot._create_items = bstack1l111l11l1_opy_
    try:
      from pabot import __version__ as bstack1ll1l1ll1l_opy_
      if version.parse(bstack1ll1l1ll1l_opy_) >= version.parse(bstack1l1111_opy_ (u"࠭࠵࠯࠲࠱࠴ࠬഊ")):
        pabot._run = bstack11l1ll1ll1_opy_
      elif version.parse(bstack1ll1l1ll1l_opy_) >= version.parse(bstack1l1111_opy_ (u"ࠧ࠵࠰࠵࠲࠵࠭ഋ")):
        pabot._run = bstack1l1ll11l11_opy_
      elif version.parse(bstack1ll1l1ll1l_opy_) >= version.parse(bstack1l1111_opy_ (u"ࠨ࠴࠱࠵࠺࠴࠰ࠨഌ")):
        pabot._run = bstack1ll1ll1ll_opy_
      elif version.parse(bstack1ll1l1ll1l_opy_) >= version.parse(bstack1l1111_opy_ (u"ࠩ࠵࠲࠶࠹࠮࠱ࠩ഍")):
        pabot._run = bstack1l11lll1l1_opy_
      else:
        pabot._run = bstack111lll11_opy_
    except Exception as e:
      pabot._run = bstack111lll11_opy_
    pabot._create_command_for_execution = bstack1lll11l1_opy_
    pabot._report_results = bstack1ll111l1_opy_
  if bstack1l1111_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪഎ") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack111l1l11_opy_(e, bstack11111l11l_opy_)
    Runner.run_hook = bstack1lll1lll11_opy_
    try:
      from behave import __version__ as bstack1111ll11_opy_
      if version.parse(bstack1111ll11_opy_) >= version.parse(bstack1l1111_opy_ (u"ࠫ࠶࠴࠳࠯࠲ࠪഏ")):
        Runner.load_hooks = bstack1l11lll1_opy_
    except Exception as e:
      logger.debug(bstack1l1111_opy_ (u"ࠬࡉ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤࡧ࡫ࡨࡢࡸࡨࠤࡻ࡫ࡲࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩഐ").format(str(e)))
    Step.run = bstack1l1l11ll1_opy_
  if bstack1l1111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭഑") in str(framework_name).lower():
    if not bstack1l1llll1l1_opy_:
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack1l1111111l_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack11lllll11l_opy_
      Config.getoption = bstack11l111llll_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack11111llll_opy_
    except Exception as e:
      pass
def bstack111l1ll1l1_opy_():
  global CONFIG
  if bstack1l1111_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧഒ") in CONFIG and int(CONFIG[bstack1l1111_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨഓ")]) > 1:
    logger.warning(bstack11lll11l1l_opy_)
def bstack111ll111l_opy_(arg, bstack1111111l1_opy_, bstack111l11llll_opy_=None):
  global CONFIG
  global bstack1l1lll1l11_opy_
  global bstack1lll11l11l_opy_
  global bstack1l1llll1l1_opy_
  global bstack1llllll11l_opy_
  bstack11l11l11l_opy_ = bstack1l1111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩഔ")
  if bstack1111111l1_opy_ and isinstance(bstack1111111l1_opy_, str):
    bstack1111111l1_opy_ = eval(bstack1111111l1_opy_)
  CONFIG = bstack1111111l1_opy_[bstack1l1111_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪക")]
  bstack1l1lll1l11_opy_ = bstack1111111l1_opy_[bstack1l1111_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬഖ")]
  bstack1lll11l11l_opy_ = bstack1111111l1_opy_[bstack1l1111_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧഗ")]
  bstack1l1llll1l1_opy_ = bstack1111111l1_opy_[bstack1l1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩഘ")]
  bstack1llllll11l_opy_.bstack11l1l111ll_opy_(bstack1l1111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨങ"), bstack1l1llll1l1_opy_)
  os.environ[bstack1l1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪച")] = bstack11l11l11l_opy_
  os.environ[bstack1l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࠨഛ")] = json.dumps(CONFIG)
  os.environ[bstack1l1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡋ࡙ࡇࡥࡕࡓࡎࠪജ")] = bstack1l1lll1l11_opy_
  os.environ[bstack1l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬഝ")] = str(bstack1lll11l11l_opy_)
  os.environ[bstack1l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡒࡕࡈࡋࡑࠫഞ")] = str(True)
  if bstack111ll1l1_opy_(arg, [bstack1l1111_opy_ (u"࠭࠭࡯ࠩട"), bstack1l1111_opy_ (u"ࠧ࠮࠯ࡱࡹࡲࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨഠ")]) != -1:
    os.environ[bstack1l1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡃࡕࡅࡑࡒࡅࡍࠩഡ")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1l11lll111_opy_)
    return
  bstack1llll1lll_opy_()
  global bstack11ll1l1ll1_opy_
  global bstack1l1llll11_opy_
  global bstack11l11111_opy_
  global bstack1ll1l11l11_opy_
  global bstack111l1lll1_opy_
  global bstack1l1ll11ll1_opy_
  global bstack1l11llll_opy_
  arg.append(bstack1l1111_opy_ (u"ࠤ࠰࡛ࠧഢ"))
  arg.append(bstack1l1111_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧ࠽ࡑࡴࡪࡵ࡭ࡧࠣࡥࡱࡸࡥࡢࡦࡼࠤ࡮ࡳࡰࡰࡴࡷࡩࡩࡀࡰࡺࡶࡨࡷࡹ࠴ࡐࡺࡶࡨࡷࡹ࡝ࡡࡳࡰ࡬ࡲ࡬ࠨണ"))
  arg.append(bstack1l1111_opy_ (u"ࠦ࠲࡝ࠢത"))
  arg.append(bstack1l1111_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩ࠿࡚ࡨࡦࠢ࡫ࡳࡴࡱࡩ࡮ࡲ࡯ࠦഥ"))
  global bstack1llll11l1l_opy_
  global bstack1l111111l_opy_
  global bstack111llllll1_opy_
  global bstack1llll1l1l1_opy_
  global bstack1lll1llll1_opy_
  global bstack11llllllll_opy_
  global bstack1lll1ll1ll_opy_
  global bstack11l1ll1l_opy_
  global bstack11ll11lll_opy_
  global bstack11l11ll11l_opy_
  global bstack1ll1l1l1l_opy_
  global bstack1l1l1llll_opy_
  global bstack11lll1lll1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1llll11l1l_opy_ = webdriver.Remote.__init__
    bstack1l111111l_opy_ = WebDriver.quit
    bstack11l1ll1l_opy_ = WebDriver.close
    bstack11ll11lll_opy_ = WebDriver.get
    bstack111llllll1_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack11l1ll111l_opy_(CONFIG) and bstack1111l111_opy_():
    if bstack11ll111l_opy_() < version.parse(bstack11ll111l11_opy_):
      logger.error(bstack111l1llll1_opy_.format(bstack11ll111l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack1l1111_opy_ (u"࠭࡟ࡨࡧࡷࡣࡵࡸ࡯ࡹࡻࡢࡹࡷࡲࠧദ")) and callable(getattr(RemoteConnection, bstack1l1111_opy_ (u"ࠧࡠࡩࡨࡸࡤࡶࡲࡰࡺࡼࡣࡺࡸ࡬ࠨധ"))):
          bstack11l11ll11l_opy_ = RemoteConnection._get_proxy_url
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          bstack11l11ll11l_opy_ = ClientConfig.get_proxy_url
      except Exception as e:
        logger.error(bstack111111111_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1ll1l1l1l_opy_ = Config.getoption
    from _pytest import runner
    bstack1l1l1llll_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warning(bstack1l1111_opy_ (u"ࠣࠧࡶ࠾ࠥࠫࡳࠣന"), bstack11l1l1111l_opy_, str(e))
  try:
    from pytest_bdd import reporting
    bstack11lll1lll1_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack1l1111_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡱࠣࡶࡺࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࡵࠪഩ"))
  bstack11l11111_opy_ = CONFIG.get(bstack1l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧപ"), {}).get(bstack1l1111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ഫ"))
  bstack1l11llll_opy_ = True
  if cli.is_enabled(CONFIG):
    if cli.bstack1l1l11llll_opy_():
      bstack1ll1111ll_opy_.invoke(bstack1ll1l11l_opy_.CONNECT, bstack1ll111llll_opy_())
    platform_index = int(os.environ.get(bstack1l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬബ"), bstack1l1111_opy_ (u"࠭࠰ࠨഭ")))
  else:
    bstack1lll1l1lll_opy_(bstack11ll1111ll_opy_)
  os.environ[bstack1l1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨമ")] = CONFIG[bstack1l1111_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪയ")]
  os.environ[bstack1l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬര")] = CONFIG[bstack1l1111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭റ")]
  os.environ[bstack1l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧല")] = bstack1l1llll1l1_opy_.__str__()
  from _pytest.config import main as bstack11llll111l_opy_
  bstack1ll1l1111_opy_ = []
  try:
    exit_code = bstack11llll111l_opy_(arg)
    if cli.is_enabled(CONFIG):
      cli.bstack1ll11ll1ll_opy_()
    if bstack1l1111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩള") in multiprocessing.current_process().__dict__.keys():
      for bstack1lll1l11l1_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1ll1l1111_opy_.append(bstack1lll1l11l1_opy_)
    try:
      bstack1lll1l1l1l_opy_ = (bstack1ll1l1111_opy_, int(exit_code))
      bstack111l11llll_opy_.append(bstack1lll1l1l1l_opy_)
    except:
      bstack111l11llll_opy_.append((bstack1ll1l1111_opy_, exit_code))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack1ll1l1111_opy_.append({bstack1l1111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫഴ"): bstack1l1111_opy_ (u"ࠧࡑࡴࡲࡧࡪࡹࡳࠡࠩവ") + os.environ.get(bstack1l1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨശ")), bstack1l1111_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨഷ"): traceback.format_exc(), bstack1l1111_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩസ"): int(os.environ.get(bstack1l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫഹ")))})
    bstack111l11llll_opy_.append((bstack1ll1l1111_opy_, 1))
def mod_behave_main(args, retries):
  try:
    from behave.configuration import Configuration
    from behave.__main__ import run_behave
    from browserstack_sdk.bstack_behave_runner import BehaveRunner
    config = Configuration(args)
    config.update_userdata({bstack1l1111_opy_ (u"ࠧࡸࡥࡵࡴ࡬ࡩࡸࠨഺ"): str(retries)})
    return run_behave(config, runner_class=BehaveRunner)
  except Exception as e:
    bstack11lllllll1_opy_ = e.__class__.__name__
    print(bstack1l1111_opy_ (u"ࠨࠥࡴ࠼ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡦࡪ࡮ࡡࡷࡧࠣࡸࡪࡹࡴࠡࠧࡶ഻ࠦ") % (bstack11lllllll1_opy_, e))
    return 1
def bstack11l1l1l1ll_opy_(arg):
  global bstack1l111l1111_opy_
  bstack1lll1l1lll_opy_(bstack1ll11llll_opy_)
  os.environ[bstack1l1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ഼")] = str(bstack1lll11l11l_opy_)
  retries = bstack1l1llll1l_opy_.bstack1llll111l_opy_(CONFIG)
  status_code = 0
  if bstack1l1llll1l_opy_.bstack1lllll1l1l_opy_(CONFIG):
    status_code = mod_behave_main(arg, retries)
  else:
    from behave.__main__ import main as bstack1ll1l111_opy_
    status_code = bstack1ll1l111_opy_(arg)
  if status_code != 0:
    bstack1l111l1111_opy_ = status_code
def bstack1l1l1l11_opy_():
  logger.info(bstack1l11l1llll_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1l1111_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧഽ"), help=bstack1l1111_opy_ (u"ࠩࡊࡩࡳ࡫ࡲࡢࡶࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡧࡴࡴࡦࡪࡩࠪാ"))
  parser.add_argument(bstack1l1111_opy_ (u"ࠪ࠱ࡺ࠭ി"), bstack1l1111_opy_ (u"ࠫ࠲࠳ࡵࡴࡧࡵࡲࡦࡳࡥࠨീ"), help=bstack1l1111_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫു"))
  parser.add_argument(bstack1l1111_opy_ (u"࠭࠭࡬ࠩൂ"), bstack1l1111_opy_ (u"ࠧ࠮࠯࡮ࡩࡾ࠭ൃ"), help=bstack1l1111_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡧࡣࡤࡧࡶࡷࠥࡱࡥࡺࠩൄ"))
  parser.add_argument(bstack1l1111_opy_ (u"ࠩ࠰ࡪࠬ൅"), bstack1l1111_opy_ (u"ࠪ࠱࠲࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨെ"), help=bstack1l1111_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪേ"))
  bstack1l111l1l1l_opy_ = parser.parse_args()
  try:
    bstack1lll111lll_opy_ = bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡬࡫࡮ࡦࡴ࡬ࡧ࠳ࡿ࡭࡭࠰ࡶࡥࡲࡶ࡬ࡦࠩൈ")
    if bstack1l111l1l1l_opy_.framework and bstack1l111l1l1l_opy_.framework not in (bstack1l1111_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭൉"), bstack1l1111_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨൊ")):
      bstack1lll111lll_opy_ = bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࠱ࡽࡲࡲ࠮ࡴࡣࡰࡴࡱ࡫ࠧോ")
    bstack1ll11lll11_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1lll111lll_opy_)
    bstack1111111ll_opy_ = open(bstack1ll11lll11_opy_, bstack1l1111_opy_ (u"ࠩࡵࠫൌ"))
    bstack111l1l1l1_opy_ = bstack1111111ll_opy_.read()
    bstack1111111ll_opy_.close()
    if bstack1l111l1l1l_opy_.username:
      bstack111l1l1l1_opy_ = bstack111l1l1l1_opy_.replace(bstack1l1111_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡗࡖࡉࡗࡔࡁࡎࡇ്ࠪ"), bstack1l111l1l1l_opy_.username)
    if bstack1l111l1l1l_opy_.key:
      bstack111l1l1l1_opy_ = bstack111l1l1l1_opy_.replace(bstack1l1111_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭ൎ"), bstack1l111l1l1l_opy_.key)
    if bstack1l111l1l1l_opy_.framework:
      bstack111l1l1l1_opy_ = bstack111l1l1l1_opy_.replace(bstack1l1111_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭൏"), bstack1l111l1l1l_opy_.framework)
    file_name = bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩ൐")
    file_path = os.path.abspath(file_name)
    bstack111l1l1lll_opy_ = open(file_path, bstack1l1111_opy_ (u"ࠧࡸࠩ൑"))
    bstack111l1l1lll_opy_.write(bstack111l1l1l1_opy_)
    bstack111l1l1lll_opy_.close()
    logger.info(bstack1lllllllll_opy_)
    try:
      os.environ[bstack1l1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪ൒")] = bstack1l111l1l1l_opy_.framework if bstack1l111l1l1l_opy_.framework != None else bstack1l1111_opy_ (u"ࠤࠥ൓")
      config = yaml.safe_load(bstack111l1l1l1_opy_)
      config[bstack1l1111_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪൔ")] = bstack1l1111_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱ࡸ࡫ࡴࡶࡲࠪൕ")
      bstack1lll111l1_opy_(bstack1l1ll1ll11_opy_, config)
    except Exception as e:
      logger.debug(bstack11l1ll1ll_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1l11l1ll1l_opy_.format(str(e)))
def bstack1lll111l1_opy_(bstack1ll11l11ll_opy_, config, bstack111ll11ll_opy_={}):
  global bstack1l1llll1l1_opy_
  global bstack1ll11111l_opy_
  global bstack1llllll11l_opy_
  if not config:
    return
  bstack11l1ll1l1l_opy_ = bstack11l11l1l1_opy_ if not bstack1l1llll1l1_opy_ else (
    bstack1lll111l11_opy_ if bstack1l1111_opy_ (u"ࠬࡧࡰࡱࠩൖ") in config else (
        bstack1llllllll_opy_ if config.get(bstack1l1111_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪൗ")) else bstack1l11111ll1_opy_
    )
)
  bstack11ll1l1111_opy_ = False
  bstack1lll1ll1l_opy_ = False
  if bstack1l1llll1l1_opy_ is True:
      if bstack1l1111_opy_ (u"ࠧࡢࡲࡳࠫ൘") in config:
          bstack11ll1l1111_opy_ = True
      else:
          bstack1lll1ll1l_opy_ = True
  bstack1l1111lll_opy_ = bstack11l11ll111_opy_.bstack1l11l11lll_opy_(config, bstack1ll11111l_opy_)
  bstack1ll11l1lll_opy_ = bstack1l1ll1ll_opy_()
  data = {
    bstack1l1111_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ൙"): config[bstack1l1111_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ൚")],
    bstack1l1111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭൛"): config[bstack1l1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ൜")],
    bstack1l1111_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ൝"): bstack1ll11l11ll_opy_,
    bstack1l1111_opy_ (u"࠭ࡤࡦࡶࡨࡧࡹ࡫ࡤࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ൞"): os.environ.get(bstack1l1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩൟ"), bstack1ll11111l_opy_),
    bstack1l1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪൠ"): bstack11ll1l111_opy_,
    bstack1l1111_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯ࠫൡ"): bstack1111lll1l_opy_(),
    bstack1l1111_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭ൢ"): {
      bstack1l1111_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩൣ"): str(config[bstack1l1111_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ൤")]) if bstack1l1111_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭൥") in config else bstack1l1111_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣ൦"),
      bstack1l1111_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧ࡙ࡩࡷࡹࡩࡰࡰࠪ൧"): sys.version,
      bstack1l1111_opy_ (u"ࠩࡵࡩ࡫࡫ࡲࡳࡧࡵࠫ൨"): bstack11l11111l1_opy_(os.environ.get(bstack1l1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬ൩"), bstack1ll11111l_opy_)),
      bstack1l1111_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭൪"): bstack1l1111_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ൫"),
      bstack1l1111_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧ൬"): bstack11l1ll1l1l_opy_,
      bstack1l1111_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬ൭"): bstack1l1111lll_opy_,
      bstack1l1111_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡡࡸࡹ࡮ࡪࠧ൮"): os.environ[bstack1l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ൯")],
      bstack1l1111_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭൰"): os.environ.get(bstack1l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭൱"), bstack1ll11111l_opy_),
      bstack1l1111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ൲"): bstack111lll1111_opy_(os.environ.get(bstack1l1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ൳"), bstack1ll11111l_opy_)),
      bstack1l1111_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭൴"): bstack1ll11l1lll_opy_.get(bstack1l1111_opy_ (u"ࠨࡰࡤࡱࡪ࠭൵")),
      bstack1l1111_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ൶"): bstack1ll11l1lll_opy_.get(bstack1l1111_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫ൷")),
      bstack1l1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ൸"): config[bstack1l1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ൹")] if config[bstack1l1111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩൺ")] else bstack1l1111_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣൻ"),
      bstack1l1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪർ"): str(config[bstack1l1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫൽ")]) if bstack1l1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬൾ") in config else bstack1l1111_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧൿ"),
      bstack1l1111_opy_ (u"ࠬࡵࡳࠨ඀"): sys.platform,
      bstack1l1111_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨඁ"): socket.gethostname(),
      bstack1l1111_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥࠩං"): bstack1llllll11l_opy_.get_property(bstack1l1111_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪඃ"))
    }
  }
  if not bstack1llllll11l_opy_.get_property(bstack1l1111_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩ඄")) is None:
    data[bstack1l1111_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭අ")][bstack1l1111_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡓࡥࡵࡣࡧࡥࡹࡧࠧආ")] = {
      bstack1l1111_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬඇ"): bstack1l1111_opy_ (u"࠭ࡵࡴࡧࡵࡣࡰ࡯࡬࡭ࡧࡧࠫඈ"),
      bstack1l1111_opy_ (u"ࠧࡴ࡫ࡪࡲࡦࡲࠧඉ"): bstack1llllll11l_opy_.get_property(bstack1l1111_opy_ (u"ࠨࡵࡧ࡯ࡐ࡯࡬࡭ࡕ࡬࡫ࡳࡧ࡬ࠨඊ")),
      bstack1l1111_opy_ (u"ࠩࡶ࡭࡬ࡴࡡ࡭ࡐࡸࡱࡧ࡫ࡲࠨඋ"): bstack1llllll11l_opy_.get_property(bstack1l1111_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡒࡴ࠭ඌ"))
    }
  if bstack1ll11l11ll_opy_ == bstack11l11l1111_opy_:
    data[bstack1l1111_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧඍ")][bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡇࡴࡴࡦࡪࡩࠪඎ")] = bstack11l1l1ll1_opy_(config)
    data[bstack1l1111_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩඏ")][bstack1l1111_opy_ (u"ࠧࡪࡵࡓࡩࡷࡩࡹࡂࡷࡷࡳࡊࡴࡡࡣ࡮ࡨࡨࠬඐ")] = percy.bstack1ll1l1l1ll_opy_
    data[bstack1l1111_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫඑ")][bstack1l1111_opy_ (u"ࠩࡳࡩࡷࡩࡹࡃࡷ࡬ࡰࡩࡏࡤࠨඒ")] = percy.percy_build_id
  if not bstack1l1llll1l_opy_.bstack1ll1ll1l1l_opy_(CONFIG):
    data[bstack1l1111_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭ඓ")][bstack1l1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠨඔ")] = bstack1l1llll1l_opy_.bstack1ll1ll1l1l_opy_(CONFIG)
  bstack1ll1ll1l_opy_ = bstack11111l1l1_opy_.bstack111ll1lll1_opy_(CONFIG, logger)
  bstack111l1111_opy_ = bstack1l1llll1l_opy_.bstack111ll1lll1_opy_(config=CONFIG)
  if bstack1ll1ll1l_opy_ is not None and bstack111l1111_opy_ is not None and bstack111l1111_opy_.bstack1l11111l_opy_():
    data[bstack1l1111_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨඕ")][bstack111l1111_opy_.bstack1ll1l11111_opy_()] = bstack1ll1ll1l_opy_.bstack111l1111l_opy_()
  update(data[bstack1l1111_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩඖ")], bstack111ll11ll_opy_)
  try:
    response = bstack1l1ll11111_opy_(bstack1l1111_opy_ (u"ࠧࡑࡑࡖࡘࠬ඗"), bstack111lll1l1_opy_(bstack1lll1l111_opy_), data, {
      bstack1l1111_opy_ (u"ࠨࡣࡸࡸ࡭࠭඘"): (config[bstack1l1111_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ඙")], config[bstack1l1111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ක")])
    })
    if response:
      logger.debug(bstack1l1ll1l111_opy_.format(bstack1ll11l11ll_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1ll1l1ll1_opy_.format(str(e)))
def bstack11l11111l1_opy_(framework):
  return bstack1l1111_opy_ (u"ࠦࢀࢃ࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴ࢁࡽࠣඛ").format(str(framework), __version__) if framework else bstack1l1111_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࡿࢂࠨග").format(
    __version__)
def bstack1llll1lll_opy_():
  global CONFIG
  global bstack11l1ll11l1_opy_
  if bool(CONFIG):
    return
  try:
    bstack1l1lll1l1l_opy_()
    logger.debug(bstack1l11l11ll_opy_.format(str(CONFIG)))
    bstack11l1ll11l1_opy_ = bstack111llll1ll_opy_.configure_logger(CONFIG, bstack11l1ll11l1_opy_)
    bstack1l1l1l1l1l_opy_()
  except Exception as e:
    logger.error(bstack1l1111_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࠥඝ") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1ll111lll1_opy_
  atexit.register(bstack1l111l11_opy_)
  signal.signal(signal.SIGINT, bstack11llll1ll1_opy_)
  signal.signal(signal.SIGTERM, bstack11llll1ll1_opy_)
def bstack1ll111lll1_opy_(exctype, value, traceback):
  global bstack1l1lll11ll_opy_
  try:
    for driver in bstack1l1lll11ll_opy_:
      bstack1l111l1ll_opy_(driver, bstack1l1111_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧඞ"), bstack1l1111_opy_ (u"ࠣࡕࡨࡷࡸ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦඟ") + str(value))
  except Exception:
    pass
  logger.info(bstack1l111lll_opy_)
  bstack1ll1ll1ll1_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1ll1ll1ll1_opy_(message=bstack1l1111_opy_ (u"ࠩࠪච"), bstack1llll111ll_opy_ = False):
  global CONFIG
  bstack111ll1111l_opy_ = bstack1l1111_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠬඡ") if bstack1llll111ll_opy_ else bstack1l1111_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪජ")
  bstack1ll1ll11l1_opy_ = bstack11ll111lll_opy_.bstack111llllll_opy_(EVENTS.bstack1ll1111l1_opy_)
  try:
    if message:
      bstack111ll11ll_opy_ = {
        bstack111ll1111l_opy_ : str(message)
      }
      try:
        bstack1lll111l1_opy_(bstack11l11l1111_opy_, CONFIG, bstack111ll11ll_opy_)
      finally:
        bstack11ll111lll_opy_.end(EVENTS.bstack1ll1111l1_opy_.value, bstack1ll1ll11l1_opy_ + bstack1l1111_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧඣ"), bstack1ll1ll11l1_opy_ + bstack1l1111_opy_ (u"ࠨ࠺ࡦࡰࡧࠦඤ"), status=True, failure=None, test_name=None)
    else:
      try:
        bstack1lll111l1_opy_(bstack11l11l1111_opy_, CONFIG)
      finally:
        bstack11ll111lll_opy_.end(EVENTS.bstack1ll1111l1_opy_.value, bstack1ll1ll11l1_opy_ + bstack1l1111_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢඥ"), bstack1ll1ll11l1_opy_ + bstack1l1111_opy_ (u"ࠣ࠼ࡨࡲࡩࠨඦ"), status=True, failure=None, test_name=None)
  except Exception as e:
    logger.debug(bstack1ll1l1l11l_opy_.format(str(e)))
def bstack1lll11l1ll_opy_(bstack1ll11ll1l1_opy_, size):
  bstack1llll111l1_opy_ = []
  while len(bstack1ll11ll1l1_opy_) > size:
    bstack1l1l111l11_opy_ = bstack1ll11ll1l1_opy_[:size]
    bstack1llll111l1_opy_.append(bstack1l1l111l11_opy_)
    bstack1ll11ll1l1_opy_ = bstack1ll11ll1l1_opy_[size:]
  bstack1llll111l1_opy_.append(bstack1ll11ll1l1_opy_)
  return bstack1llll111l1_opy_
def bstack1l1l11l111_opy_(args):
  if bstack1l1111_opy_ (u"ࠩ࠰ࡱࠬට") in args and bstack1l1111_opy_ (u"ࠪࡴࡩࡨࠧඨ") in args:
    return True
  return False
@measure(event_name=EVENTS.bstack11lllll1l1_opy_, stage=STAGE.bstack1l111ll1_opy_)
def run_on_browserstack(bstack11ll1lllll_opy_=None, bstack111l11llll_opy_=None, bstack11l11l1l_opy_=False):
  global CONFIG
  global bstack1l1lll1l11_opy_
  global bstack1lll11l11l_opy_
  global bstack1ll11111l_opy_
  global bstack1llllll11l_opy_
  bstack11l11l11l_opy_ = bstack1l1111_opy_ (u"ࠫࠬඩ")
  bstack1ll111111_opy_ = bstack1l1111_opy_ (u"ࠧࠨඪ")
  bstack1l111llll_opy_(bstack11l111lll1_opy_, logger)
  if bstack11ll1lllll_opy_ and isinstance(bstack11ll1lllll_opy_, str):
    bstack11ll1lllll_opy_ = eval(bstack11ll1lllll_opy_)
  if bstack11ll1lllll_opy_:
    CONFIG = bstack11ll1lllll_opy_[bstack1l1111_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭ණ")]
    bstack1l1lll1l11_opy_ = bstack11ll1lllll_opy_[bstack1l1111_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨඬ")]
    bstack1lll11l11l_opy_ = bstack11ll1lllll_opy_[bstack1l1111_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪත")]
    bstack1llllll11l_opy_.bstack11l1l111ll_opy_(bstack1l1111_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫථ"), bstack1lll11l11l_opy_)
    bstack11l11l11l_opy_ = bstack1l1111_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪද")
  bstack1llllll11l_opy_.bstack11l1l111ll_opy_(bstack1l1111_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭ධ"), uuid4().__str__())
  logger.info(bstack1l1111_opy_ (u"࡙ࠬࡄࡌࠢࡵࡹࡳࠦࡳࡵࡣࡵࡸࡪࡪࠠࡸ࡫ࡷ࡬ࠥ࡯ࡤ࠻ࠢࠪන") + bstack1llllll11l_opy_.get_property(bstack1l1111_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨ඲")));
  logger.debug(bstack1l1111_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥ࠿ࠪඳ") + bstack1llllll11l_opy_.get_property(bstack1l1111_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪප")))
  if not bstack11l11l1l_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1l11lll111_opy_)
      return
    if sys.argv[1] == bstack1l1111_opy_ (u"ࠩ࠰࠱ࡻ࡫ࡲࡴ࡫ࡲࡲࠬඵ") or sys.argv[1] == bstack1l1111_opy_ (u"ࠪ࠱ࡻ࠭බ"):
      logger.info(bstack1l1111_opy_ (u"ࠫࡇࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡔࡾࡺࡨࡰࡰࠣࡗࡉࡑࠠࡷࡽࢀࠫභ").format(__version__))
      return
    if sys.argv[1] == bstack1l1111_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫම"):
      bstack1l1l1l11_opy_()
      return
  args = sys.argv
  bstack1llll1lll_opy_()
  global bstack11ll1l1ll1_opy_
  global bstack11l1ll1l11_opy_
  global bstack1l11llll_opy_
  global bstack1lll111ll1_opy_
  global bstack1l1llll11_opy_
  global bstack11l11111_opy_
  global bstack1ll1l11l11_opy_
  global bstack1l11l1ll1_opy_
  global bstack111l1lll1_opy_
  global bstack1l1ll11ll1_opy_
  global bstack1l1l111lll_opy_
  bstack11l1ll1l11_opy_ = len(CONFIG.get(bstack1l1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩඹ"), []))
  if not bstack11l11l11l_opy_:
    if args[1] == bstack1l1111_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧය") or args[1] == bstack1l1111_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩර"):
      bstack11l11l11l_opy_ = bstack1l1111_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ඼")
      args = args[2:]
    elif args[1] == bstack1l1111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩල"):
      bstack11l11l11l_opy_ = bstack1l1111_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ඾")
      args = args[2:]
    elif args[1] == bstack1l1111_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ඿"):
      bstack11l11l11l_opy_ = bstack1l1111_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬව")
      args = args[2:]
    elif args[1] == bstack1l1111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨශ"):
      bstack11l11l11l_opy_ = bstack1l1111_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩෂ")
      args = args[2:]
    elif args[1] == bstack1l1111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩස"):
      bstack11l11l11l_opy_ = bstack1l1111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪහ")
      args = args[2:]
    elif args[1] == bstack1l1111_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫළ"):
      bstack11l11l11l_opy_ = bstack1l1111_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬෆ")
      args = args[2:]
    else:
      if not bstack1l1111_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ෇") in CONFIG or str(CONFIG[bstack1l1111_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ෈")]).lower() in [bstack1l1111_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ෉"), bstack1l1111_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵්ࠪ")]:
        bstack11l11l11l_opy_ = bstack1l1111_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ෋")
        args = args[1:]
      elif str(CONFIG[bstack1l1111_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ෌")]).lower() == bstack1l1111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ෍"):
        bstack11l11l11l_opy_ = bstack1l1111_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ෎")
        args = args[1:]
      elif str(CONFIG[bstack1l1111_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪා")]).lower() == bstack1l1111_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧැ"):
        bstack11l11l11l_opy_ = bstack1l1111_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨෑ")
        args = args[1:]
      elif str(CONFIG[bstack1l1111_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ි")]).lower() == bstack1l1111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫී"):
        bstack11l11l11l_opy_ = bstack1l1111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬු")
        args = args[1:]
      elif str(CONFIG[bstack1l1111_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ෕")]).lower() == bstack1l1111_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧූ"):
        bstack11l11l11l_opy_ = bstack1l1111_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ෗")
        args = args[1:]
      else:
        os.environ[bstack1l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫෘ")] = bstack11l11l11l_opy_
        bstack11ll11l1l_opy_(bstack1ll111l11l_opy_)
  os.environ[bstack1l1111_opy_ (u"ࠪࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡕࡔࡇࡇࠫෙ")] = bstack11l11l11l_opy_
  bstack1ll11111l_opy_ = bstack11l11l11l_opy_
  if cli.is_enabled(CONFIG):
    try:
      bstack11l11111ll_opy_ = bstack11l1lllll_opy_[bstack1l1111_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗ࠱ࡇࡊࡄࠨේ")] if bstack11l11l11l_opy_ == bstack1l1111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬෛ") and bstack1llllll1l_opy_() else bstack11l11l11l_opy_
      bstack1ll1111ll_opy_.invoke(bstack1ll1l11l_opy_.bstack1ll1l1ll11_opy_, bstack1l1l11l1l_opy_(
        sdk_version=__version__,
        path_config=bstack1ll11lllll_opy_(),
        path_project=os.getcwd(),
        test_framework=bstack11l11111ll_opy_,
        frameworks=[bstack11l11111ll_opy_],
        framework_versions={
          bstack11l11111ll_opy_: bstack111lll1111_opy_(bstack1l1111_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬො") if bstack11l11l11l_opy_ in [bstack1l1111_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ෝ"), bstack1l1111_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧෞ"), bstack1l1111_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪෟ")] else bstack11l11l11l_opy_)
        },
        bs_config=CONFIG
      ))
      if cli.config.get(bstack1l1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧ෠"), None):
        CONFIG[bstack1l1111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࠨ෡")] = cli.config.get(bstack1l1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠢ෢"), None)
    except Exception as e:
      bstack1ll1111ll_opy_.invoke(bstack1ll1l11l_opy_.bstack1l1l1l111l_opy_, e.__traceback__, 1)
    if bstack1lll11l11l_opy_:
      CONFIG[bstack1l1111_opy_ (u"ࠨࡡࡱࡲࠥ෣")] = cli.config[bstack1l1111_opy_ (u"ࠢࡢࡲࡳࠦ෤")]
      logger.info(bstack1l11l1l1l_opy_.format(CONFIG[bstack1l1111_opy_ (u"ࠨࡣࡳࡴࠬ෥")]))
  else:
    bstack1ll1111ll_opy_.clear()
  global bstack1l11l111l1_opy_
  global bstack1ll1ll111_opy_
  if bstack11ll1lllll_opy_:
    try:
      bstack1ll1lll11l_opy_ = datetime.datetime.now()
      os.environ[bstack1l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫ෦")] = bstack11l11l11l_opy_
      bstack1l11l1111l_opy_ = bstack11ll111lll_opy_.bstack111llllll_opy_(EVENTS.bstack1ll1lll1l_opy_)
      try:
        logger.info(bstack1l1111_opy_ (u"ࠥࡗࡪࡴࡤࡪࡰࡪࠤࡘࡊࡋࠡࡖࡨࡷࡹࠦࡁࡵࡶࡨࡱࡵࡺࡥࡥࠢࡨࡺࡪࡴࡴࠣ෧"))
        bstack1lll111l1_opy_(bstack1lll1ll111_opy_, CONFIG)
      finally:
        bstack11ll111lll_opy_.end(EVENTS.bstack1ll1lll1l_opy_.value, bstack1l11l1111l_opy_ + bstack1l1111_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ෨"), bstack1l11l1111l_opy_ + bstack1l1111_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ෩"), status=True, failure=None, test_name=None)
      cli.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠨࡨࡵࡶࡳ࠾ࡸࡪ࡫ࡠࡶࡨࡷࡹࡥࡡࡵࡶࡨࡱࡵࡺࡥࡥࠤ෪"), datetime.datetime.now() - bstack1ll1lll11l_opy_)
    except Exception as e:
      logger.debug(bstack111ll1l11l_opy_.format(str(e)))
  global bstack1llll11l1l_opy_
  global bstack1l111111l_opy_
  global bstack11111ll11_opy_
  global bstack1l1ll1l11l_opy_
  global bstack1l11l1l1_opy_
  global bstack111lllll1_opy_
  global bstack1llll1l1l1_opy_
  global bstack1lll1llll1_opy_
  global bstack1l1111ll11_opy_
  global bstack11llllllll_opy_
  global bstack1lll1ll1ll_opy_
  global bstack11l1ll1l_opy_
  global bstack111l1l11l_opy_
  global bstack1lll111l_opy_
  global bstack1l1l11111l_opy_
  global bstack11ll11lll_opy_
  global bstack11l11ll11l_opy_
  global bstack1ll1l1l1l_opy_
  global bstack1l1l1llll_opy_
  global bstack11ll1l1l_opy_
  global bstack11lll1lll1_opy_
  global bstack111llllll1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1llll11l1l_opy_ = webdriver.Remote.__init__
    bstack1l111111l_opy_ = WebDriver.quit
    bstack11l1ll1l_opy_ = WebDriver.close
    bstack11ll11lll_opy_ = WebDriver.get
    bstack111llllll1_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1l11l111l1_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack1l111lll1_opy_
    bstack1ll1ll111_opy_ = bstack1l111lll1_opy_()
  except Exception as e:
    pass
  try:
    global bstack11lll1lll_opy_
    from QWeb.keywords import browser
    bstack11lll1lll_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack11l1ll111l_opy_(CONFIG) and bstack1111l111_opy_():
    if bstack11ll111l_opy_() < version.parse(bstack11ll111l11_opy_):
      logger.error(bstack111l1llll1_opy_.format(bstack11ll111l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack1l1111_opy_ (u"ࠧࡠࡩࡨࡸࡤࡶࡲࡰࡺࡼࡣࡺࡸ࡬ࠨ෫")) and callable(getattr(RemoteConnection, bstack1l1111_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩ෬"))):
          RemoteConnection._get_proxy_url = bstack111llll11l_opy_
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          ClientConfig.get_proxy_url = bstack111llll11l_opy_
      except Exception as e:
        logger.error(bstack111111111_opy_.format(str(e)))
  if not CONFIG.get(bstack1l1111_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫ෭"), False) and not bstack11ll1lllll_opy_:
    logger.info(bstack11ll1lll1l_opy_)
  bstack11l1l1l111_opy_ = not cli.is_enabled(CONFIG) and bstack11l11l11l_opy_ not in [bstack1l1111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ෮")]
  bstack11l1llll11_opy_ = bstack11l1l1l111_opy_ and bstack1l1111_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ෯") in CONFIG and str(CONFIG[bstack1l1111_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ෰")]).lower() != bstack1l1111_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ෱")
  bstack1lll1111_opy_ = bstack11l1l1l111_opy_ and not bstack11l1llll11_opy_ and (bstack11l11l11l_opy_ != bstack1l1111_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧෲ") or (bstack11l11l11l_opy_ == bstack1l1111_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨෳ") and not bstack11ll1lllll_opy_))
  if (bstack11l11l11l_opy_ in [bstack1l1111_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ෴"), bstack1l1111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ෵"), bstack1l1111_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ෶")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack11l11l111l_opy_
        bstack111lllll1_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warning(bstack1lll11l11_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1l11l1l1_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1ll111111l_opy_ + str(e))
    except Exception as e:
      bstack111l1l11_opy_(e, bstack1lll11l11_opy_)
    if bstack11l11l11l_opy_ != bstack1l1111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭෷"):
      bstack1l1111llll_opy_()
    bstack11111ll11_opy_ = Output.start_test
    bstack1l1ll1l11l_opy_ = Output.end_test
    bstack1llll1l1l1_opy_ = TestStatus.__init__
    bstack1l1111ll11_opy_ = pabot._run
    bstack11llllllll_opy_ = QueueItem.__init__
    bstack1lll1ll1ll_opy_ = pabot._create_command_for_execution
    bstack11ll1l1l_opy_ = pabot._report_results
  if bstack11l11l11l_opy_ == bstack1l1111_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭෸"):
    global bstack1111l1l11_opy_
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack111l1l11_opy_(e, bstack11111l11l_opy_)
    bstack111l1l11l_opy_ = Runner.run_hook
    bstack1lll111l_opy_ = Runner.load_hooks
    bstack1l1l11111l_opy_ = Step.run
    try:
      sig = inspect.signature(bstack111l1l11l_opy_)
      params = list(sig.parameters.keys())
      bstack1111l1l11_opy_ = bstack1l1111_opy_ (u"ࠧࡤࡱࡱࡸࡪࡾࡴࠨ෹") in params
      logger.info(bstack1l1111_opy_ (u"ࠨࡆࡨࡸࡪࡩࡴࡦࡦࠣࡦࡪ࡮ࡡࡷࡧࠣࡶࡺࡴ࡟ࡩࡱࡲ࡯ࠥࡹࡩࡨࡰࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬ෺").format(bstack1l1111_opy_ (u"ࠩ࠴࠲࠷࠴࠶ࠡࠪࡺ࡭ࡹ࡮ࠠࡤࡱࡱࡸࡪࡾࡴࠪࠩ෻") if bstack1111l1l11_opy_ else bstack1l1111_opy_ (u"ࠪ࠵࠳࠹ࠫࠡࠪࡺ࡭ࡹ࡮࡯ࡶࡶࠣࡧࡴࡴࡴࡦࡺࡷ࠭ࠬ෼")))
    except Exception as e:
      logger.debug(bstack1l1111_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡨࡺࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡳࡷࡱࡣ࡭ࡵ࡯࡬ࠢࡶ࡭࡬ࡴࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩ෽").format(str(e)))
      bstack1111l1l11_opy_ = None
  if bstack11l11l11l_opy_ == bstack1l1111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ෾"):
    try:
      from _pytest.config import Config
      bstack1ll1l1l1l_opy_ = Config.getoption
      from _pytest import runner
      bstack1l1l1llll_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warning(bstack1l1111_opy_ (u"ࠨࠥࡴ࠼ࠣࠩࡸࠨ෿"), bstack11l1l1111l_opy_, str(e))
    try:
      from pytest_bdd import reporting
      bstack11lll1lll1_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1l1111_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨ฀"))
    if bstack111ll111ll_opy_():
      logger.warning(bstack11l11l111_opy_[bstack1l1111_opy_ (u"ࠨࡕࡇࡏ࠲ࡍࡅࡏ࠯࠳࠴࠺࠭ก")])
  try:
    framework_name = bstack1l1111_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨข") if bstack11l11l11l_opy_ in [bstack1l1111_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩฃ"), bstack1l1111_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪค"), bstack1l1111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ฅ")] else bstack11l11lll1_opy_(bstack11l11l11l_opy_)
    bstack11ll111ll_opy_ = {
      bstack1l1111_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࠧฆ"): bstack1l1111_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩง") if bstack11l11l11l_opy_ == bstack1l1111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨจ") and bstack1llllll1l_opy_() else framework_name,
      bstack1l1111_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ฉ"): bstack111lll1111_opy_(framework_name),
      bstack1l1111_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨช"): __version__,
      bstack1l1111_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬซ"): bstack11l11l11l_opy_
    }
    if bstack11l11l11l_opy_ in bstack1l1ll1l1ll_opy_ + bstack1l111lll1l_opy_:
      if bstack1l11l1l111_opy_.bstack111ll11l1l_opy_(CONFIG):
        if bstack1l1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬฌ") in CONFIG:
          os.environ[bstack1l1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧญ")] = os.getenv(bstack1l1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨฎ"), json.dumps(CONFIG[bstack1l1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨฏ")]))
          CONFIG[bstack1l1111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩฐ")].pop(bstack1l1111_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨฑ"), None)
          CONFIG[bstack1l1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫฒ")].pop(bstack1l1111_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪณ"), None)
        bstack11ll111ll_opy_[bstack1l1111_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ด")] = {
          bstack1l1111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬต"): bstack1l1111_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࠪถ"),
          bstack1l1111_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪท"): str(bstack11ll111l_opy_())
        }
    bstack1111l1ll_opy_, bstack1ll11l1l1_opy_ = None, {}
    bstack11ll1lll11_opy_ = None
    bstack1111l11ll_opy_ = None
    def bstack11l1lll1l_opy_():
      if bstack11l1llll11_opy_:
        bstack1lll111l1l_opy_()
      elif bstack1lll1111_opy_:
        bstack1111l1l1_opy_()
    def bstack11lll1ll_opy_():
      nonlocal bstack1111l1ll_opy_, bstack1ll11l1l1_opy_
      if bstack11l11l11l_opy_ not in [bstack1l1111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫธ")] and not cli.is_running():
        bstack1111l1ll_opy_, bstack1ll11l1l1_opy_ = bstack11l11111l_opy_.launch(CONFIG, bstack11ll111ll_opy_)
    if bstack11l1llll11_opy_ or bstack1lll1111_opy_:
      bstack11ll1lll11_opy_ = threading.Thread(target=bstack11l1lll1l_opy_)
      bstack11ll1lll11_opy_.start()
    if bstack11l11l11l_opy_ not in [bstack1l1111_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬน")] and not cli.is_running():
      bstack1111l11ll_opy_ = threading.Thread(target=bstack11lll1ll_opy_)
      bstack1111l11ll_opy_.start()
    if bstack11ll1lll11_opy_:
      bstack11ll1lll11_opy_.join()
    if bstack1111l11ll_opy_:
      bstack1111l11ll_opy_.join()
    if bstack1ll11l1l1_opy_.get(bstack1l1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬบ")) is not None and bstack1l11l1l111_opy_.bstack1lll1111ll_opy_(CONFIG) is None:
      value = bstack1ll11l1l1_opy_[bstack1l1111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ป")].get(bstack1l1111_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨผ"))
      if value is not None:
          CONFIG[bstack1l1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨฝ")] = value
      else:
        logger.debug(bstack1l1111_opy_ (u"ࠤࡑࡳࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡪࡡࡵࡣࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠢพ"))
  except Exception as e:
    logger.debug(bstack11ll11ll11_opy_.format(bstack1l1111_opy_ (u"ࠪࡘࡪࡹࡴࡉࡷࡥࠫฟ"), str(e)))
  if bstack11l11l11l_opy_ == bstack1l1111_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫภ"):
    bstack1l11llll_opy_ = True
    if bstack11ll1lllll_opy_ and bstack11l11l1l_opy_:
      bstack11l11111_opy_ = CONFIG.get(bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩม"), {}).get(bstack1l1111_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨย"))
      bstack1lll1l1lll_opy_(bstack111llll111_opy_)
    elif bstack11ll1lllll_opy_:
      bstack11l11111_opy_ = CONFIG.get(bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫร"), {}).get(bstack1l1111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪฤ"))
      global bstack1l1lll11ll_opy_
      try:
        if bstack1l1l11l111_opy_(bstack11ll1lllll_opy_[bstack1l1111_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬล")]) and multiprocessing.current_process().name == bstack1l1111_opy_ (u"ࠪ࠴ࠬฦ"):
          bstack11ll1lllll_opy_[bstack1l1111_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧว")].remove(bstack1l1111_opy_ (u"ࠬ࠳࡭ࠨศ"))
          bstack11ll1lllll_opy_[bstack1l1111_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩษ")].remove(bstack1l1111_opy_ (u"ࠧࡱࡦࡥࠫส"))
          bstack11ll1lllll_opy_[bstack1l1111_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫห")] = bstack11ll1lllll_opy_[bstack1l1111_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬฬ")][0]
          with open(bstack11ll1lllll_opy_[bstack1l1111_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭อ")], bstack1l1111_opy_ (u"ࠫࡷ࠭ฮ")) as f:
            bstack1l111l1l1_opy_ = f.read()
          bstack1l1l11l1l1_opy_ = bstack1l1111_opy_ (u"ࠧࠨࠢࡧࡴࡲࡱࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡸࡪ࡫ࠡ࡫ࡰࡴࡴࡸࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡨ࠿ࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥࠩࡽࢀ࠭ࡀࠦࡦࡳࡱࡰࠤࡵࡪࡢࠡ࡫ࡰࡴࡴࡸࡴࠡࡒࡧࡦࡀࠦ࡯ࡨࡡࡧࡦࠥࡃࠠࡑࡦࡥ࠲ࡩࡵ࡟ࡣࡴࡨࡥࡰࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡨࡪ࡬ࠠ࡮ࡱࡧࡣࡧࡸࡥࡢ࡭ࠫࡷࡪࡲࡦ࠭ࠢࡤࡶ࡬࠲ࠠࡵࡧࡰࡴࡴࡸࡡࡳࡻࠣࡁࠥ࠶ࠩ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡵࡴࡼ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡧࡲࡨࠢࡀࠤࡸࡺࡲࠩ࡫ࡱࡸ࠭ࡧࡲࡨࠫ࠮࠵࠵࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡫ࡸࡤࡧࡳࡸࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡣࡶࠤࡪࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡱࡣࡶࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡳ࡬ࡥࡤࡣࠪࡶࡩࡱ࡬ࠬࡢࡴࡪ࠰ࡹ࡫࡭ࡱࡱࡵࡥࡷࡿࠩࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡕࡪࡢ࠯ࡦࡲࡣࡧࠦ࠽ࠡ࡯ࡲࡨࡤࡨࡲࡦࡣ࡮ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡑࡦࡥ࠲ࡩࡵ࡟ࡣࡴࡨࡥࡰࠦ࠽ࠡ࡯ࡲࡨࡤࡨࡲࡦࡣ࡮ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡑࡦࡥࠬ࠮࠴ࡳࡦࡶࡢࡸࡷࡧࡣࡦࠪࠬࡠࡳࠨࠢࠣฯ").format(str(bstack11ll1lllll_opy_))
          bstack11l1ll1lll_opy_ = bstack1l1l11l1l1_opy_ + bstack1l111l1l1_opy_
          bstack1l111ll11l_opy_ = bstack11ll1lllll_opy_[bstack1l1111_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩะ")] + bstack1l1111_opy_ (u"ࠧࡠࡤࡶࡸࡦࡩ࡫ࡠࡶࡨࡱࡵ࠴ࡰࡺࠩั")
          with open(bstack1l111ll11l_opy_, bstack1l1111_opy_ (u"ࠨࡹࠪา")):
            pass
          with open(bstack1l111ll11l_opy_, bstack1l1111_opy_ (u"ࠤࡺ࠯ࠧำ")) as f:
            f.write(bstack11l1ll1lll_opy_)
          import subprocess
          bstack111l1l111l_opy_ = subprocess.run([bstack1l1111_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࠥิ"), bstack1l111ll11l_opy_])
          if os.path.exists(bstack1l111ll11l_opy_):
            os.unlink(bstack1l111ll11l_opy_)
          os._exit(bstack111l1l111l_opy_.returncode)
        else:
          if bstack1l1l11l111_opy_(bstack11ll1lllll_opy_[bstack1l1111_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧี")]):
            bstack11ll1lllll_opy_[bstack1l1111_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨึ")].remove(bstack1l1111_opy_ (u"࠭࠭࡮ࠩื"))
            bstack11ll1lllll_opy_[bstack1l1111_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧุࠪ")].remove(bstack1l1111_opy_ (u"ࠨࡲࡧࡦูࠬ"))
            bstack11ll1lllll_opy_[bstack1l1111_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩฺࠬ")] = bstack11ll1lllll_opy_[bstack1l1111_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭฻")][0]
          bstack1lll1l1lll_opy_(bstack111llll111_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack11ll1lllll_opy_[bstack1l1111_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ฼")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1l1111_opy_ (u"ࠬࡥ࡟࡯ࡣࡰࡩࡤࡥࠧ฽")] = bstack1l1111_opy_ (u"࠭࡟ࡠ࡯ࡤ࡭ࡳࡥ࡟ࠨ฾")
          mod_globals[bstack1l1111_opy_ (u"ࠧࡠࡡࡩ࡭ࡱ࡫࡟ࡠࠩ฿")] = os.path.abspath(bstack11ll1lllll_opy_[bstack1l1111_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫเ")])
          exec(open(bstack11ll1lllll_opy_[bstack1l1111_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬแ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1l1111_opy_ (u"ࠪࡇࡦࡻࡧࡩࡶࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࡼࡿࠪโ").format(str(e)))
          for driver in bstack1l1lll11ll_opy_:
            bstack111l11llll_opy_.append({
              bstack1l1111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩใ"): bstack11ll1lllll_opy_[bstack1l1111_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨไ")],
              bstack1l1111_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬๅ"): str(e),
              bstack1l1111_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ๆ"): multiprocessing.current_process().name
            })
            bstack1l111l1ll_opy_(driver, bstack1l1111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ็"), bstack1l1111_opy_ (u"ࠤࡖࡩࡸࡹࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲ่ࠧ") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1l1lll11ll_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1lll11l11l_opy_, CONFIG, logger)
      bstack1l1ll1l1l_opy_()
      bstack111l1ll1l1_opy_()
      percy.bstack11llll1l11_opy_()
      bstack1111111l1_opy_ = {
        bstack1l1111_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ้࠭"): args[0],
        bstack1l1111_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊ๊ࠫ"): CONFIG,
        bstack1l1111_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ๋࠭"): bstack1l1lll1l11_opy_,
        bstack1l1111_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ์"): bstack1lll11l11l_opy_
      }
      if bstack1l1111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪํ") in CONFIG:
        bstack11ll1111_opy_ = bstack111l1ll111_opy_(args, logger, CONFIG, bstack1l1llll1l1_opy_, bstack11l1ll1l11_opy_)
        bstack1l11l1ll1_opy_ = bstack11ll1111_opy_.bstack111ll1l11_opy_(run_on_browserstack, bstack1111111l1_opy_, bstack1l1l11l111_opy_(args))
      else:
        if bstack1l1l11l111_opy_(args):
          bstack1111111l1_opy_[bstack1l1111_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ๎")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1111111l1_opy_,))
          test.start()
          test.join()
        else:
          bstack1lll1l1lll_opy_(bstack111llll111_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1l1111_opy_ (u"ࠩࡢࡣࡳࡧ࡭ࡦࡡࡢࠫ๏")] = bstack1l1111_opy_ (u"ࠪࡣࡤࡳࡡࡪࡰࡢࡣࠬ๐")
          mod_globals[bstack1l1111_opy_ (u"ࠫࡤࡥࡦࡪ࡮ࡨࡣࡤ࠭๑")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack11l11l11l_opy_ == bstack1l1111_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ๒") or bstack11l11l11l_opy_ == bstack1l1111_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ๓"):
    percy.init(bstack1lll11l11l_opy_, CONFIG, logger)
    percy.bstack11llll1l11_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack111l1l11_opy_(e, bstack1lll11l11_opy_)
    bstack1l1ll1l1l_opy_()
    bstack1lll1l1lll_opy_(bstack11llll11ll_opy_)
    if bstack1l1llll1l1_opy_:
      bstack1l1lllll_opy_(bstack11llll11ll_opy_, args)
      if bstack1l1111_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ๔") in args:
        i = args.index(bstack1l1111_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭๕"))
        args.pop(i)
        args.pop(i)
      if bstack1l1111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ๖") not in CONFIG:
        CONFIG[bstack1l1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭๗")] = [{}]
        bstack11l1ll1l11_opy_ = 1
      if bstack11ll1l1ll1_opy_ == 0:
        bstack11ll1l1ll1_opy_ = 1
      args.insert(0, str(bstack11ll1l1ll1_opy_))
      args.insert(0, str(bstack1l1111_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩ๘")))
    if bstack11l11111l_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1ll1l1l1l1_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1l1l1l11ll_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack1l1111_opy_ (u"ࠧࡘࡏࡃࡑࡗࡣࡔࡖࡔࡊࡑࡑࡗࠧ๙"),
        ).parse_args(bstack1ll1l1l1l1_opy_)
        bstack1l111l11ll_opy_ = args.index(bstack1ll1l1l1l1_opy_[0]) if len(bstack1ll1l1l1l1_opy_) > 0 else len(args)
        args.insert(bstack1l111l11ll_opy_, str(bstack1l1111_opy_ (u"࠭࠭࠮࡮࡬ࡷࡹ࡫࡮ࡦࡴࠪ๚")))
        args.insert(bstack1l111l11ll_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l1111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡳࡱࡥࡳࡹࡥ࡬ࡪࡵࡷࡩࡳ࡫ࡲ࠯ࡲࡼࠫ๛"))))
        if bstack1l1llll1l_opy_.bstack1lllll1l1l_opy_(CONFIG):
          args.insert(bstack1l111l11ll_opy_, str(bstack1l1111_opy_ (u"ࠨ࠯࠰ࡰ࡮ࡹࡴࡦࡰࡨࡶࠬ๜")))
          args.insert(bstack1l111l11ll_opy_ + 1, str(bstack1l1111_opy_ (u"ࠩࡕࡩࡹࡸࡹࡇࡣ࡬ࡰࡪࡪ࠺ࡼࡿࠪ๝").format(bstack1l1llll1l_opy_.bstack1llll111l_opy_(CONFIG))))
        if bstack1l1111lll1_opy_(os.environ.get(bstack1l1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠨ๞"))) and str(os.environ.get(bstack1l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠨ๟"), bstack1l1111_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ๠"))) != bstack1l1111_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ๡"):
          for bstack1l111ll1l_opy_ in bstack1l1l1l11ll_opy_:
            args.remove(bstack1l111ll1l_opy_)
          test_files = os.environ.get(bstack1l1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠫ๢")).split(bstack1l1111_opy_ (u"ࠨ࠮ࠪ๣"))
          for bstack1ll111l11_opy_ in test_files:
            args.append(bstack1ll111l11_opy_)
      except Exception as e:
        logger.error(bstack1l1111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡢࡶࡷࡥࡨ࡮ࡩ࡯ࡩࠣࡰ࡮ࡹࡴࡦࡰࡨࡶࠥ࡬࡯ࡳࠢࡾࢁ࠳ࠦࡅࡳࡴࡲࡶࠥ࠳ࠠࡼࡿࠥ๤").format(bstack1ll1lll111_opy_, e))
    pabot.main(args)
  elif bstack11l11l11l_opy_ == bstack1l1111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ๥"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack111l1l11_opy_(e, bstack1lll11l11_opy_)
    for a in args:
      if bstack1l1111_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚ࠪ๦") in a:
        bstack1l1llll11_opy_ = int(a.split(bstack1l1111_opy_ (u"ࠬࡀࠧ๧"))[1])
      if bstack1l1111_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪ๨") in a:
        bstack11l11111_opy_ = str(a.split(bstack1l1111_opy_ (u"ࠧ࠻ࠩ๩"))[1])
      if bstack1l1111_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓࠨ๪") in a:
        bstack1ll1l11l11_opy_ = str(a.split(bstack1l1111_opy_ (u"ࠩ࠽ࠫ๫"))[1])
    bstack11ll111ll1_opy_ = None
    bstack1ll111l1ll_opy_ = None
    if bstack1l1111_opy_ (u"ࠪ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠩ๬") in args:
      i = args.index(bstack1l1111_opy_ (u"ࠫ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠪ๭"))
      args.pop(i)
      bstack11ll111ll1_opy_ = args.pop(i)
    if bstack1l1111_opy_ (u"ࠬ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸࠨ๮") in args:
      i = args.index(bstack1l1111_opy_ (u"࠭࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࠩ๯"))
      args.pop(i)
      bstack1ll111l1ll_opy_ = args.pop(i)
    if bstack11ll111ll1_opy_ is not None:
      global bstack1l111l11l_opy_
      bstack1l111l11l_opy_ = bstack11ll111ll1_opy_
    if bstack1ll111l1ll_opy_ is not None and int(bstack1l1llll11_opy_) < 0:
      bstack1l1llll11_opy_ = int(bstack1ll111l1ll_opy_)
    bstack1lll1l1lll_opy_(bstack11llll11ll_opy_)
    run_cli(args)
    if bstack1l1111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷࠫ๰") in multiprocessing.current_process().__dict__.keys():
      for bstack1lll1l11l1_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack111l11llll_opy_.append(bstack1lll1l11l1_opy_)
  elif bstack11l11l11l_opy_ == bstack1l1111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ๱"):
    bstack111l11l1l_opy_ = bstack111ll1l1ll_opy_(args, logger, CONFIG, bstack1l1llll1l1_opy_)
    bstack111l11l1l_opy_.bstack1ll1111ll1_opy_()
    bstack1l1ll1l1l_opy_()
    bstack1lll111ll1_opy_ = True
    bstack1l1ll11ll1_opy_ = bstack111l11l1l_opy_.bstack1lll11lll1_opy_()
    bstack111l11l1l_opy_.bstack1111111l1_opy_(bstack1l1lll11l_opy_)
    bstack111l11l1l_opy_.bstack111111ll_opy_()
    bstack111lll1l1l_opy_(bstack11l11l11l_opy_, CONFIG, bstack111l11l1l_opy_.bstack111l1ll1_opy_())
    bstack11l111111l_opy_.end(EVENTS.bstack11lllll1l1_opy_.value, EVENTS.bstack11lllll1l1_opy_.value + bstack1l1111_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ๲"), EVENTS.bstack11lllll1l1_opy_.value + bstack1l1111_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ๳"), status=True, failure=None, test_name=bstack11l1111lll_opy_)
    bstack1l1l111l1_opy_ = bstack111l11l1l_opy_.bstack111ll1l11_opy_(bstack111ll111l_opy_, {
      bstack1l1111_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬ๴"): bstack1l1lll1l11_opy_,
      bstack1l1111_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ๵"): bstack1lll11l11l_opy_,
      bstack1l1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ๶"): bstack1l1llll1l1_opy_
    })
    if not bstack11ll1lllll_opy_:
      bstack1ll111111_opy_ = bstack11ll111lll_opy_.bstack111llllll_opy_(EVENTS.bstack1l11l11l_opy_.value)
    try:
      bstack1ll1l1111_opy_, bstack11ll1l11ll_opy_ = map(list, zip(*bstack1l1l111l1_opy_))
      bstack111l1lll1_opy_ = bstack1ll1l1111_opy_[0]
      for status_code in bstack11ll1l11ll_opy_:
        if status_code != 0:
          bstack1l1l111lll_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack1l1111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡦࡼࡥࠡࡧࡵࡶࡴࡸࡳࠡࡣࡱࡨࠥࡹࡴࡢࡶࡸࡷࠥࡩ࡯ࡥࡧ࠱ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠ࠻ࠢࡾࢁࠧ๷").format(str(e)))
  elif bstack11l11l11l_opy_ == bstack1l1111_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ๸"):
    try:
      from behave.__main__ import main as bstack1ll1l111_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack111l1l11_opy_(e, bstack11111l11l_opy_)
    bstack1l1ll1l1l_opy_()
    bstack1lll111ll1_opy_ = True
    bstack11lll111l1_opy_ = 1
    if bstack1l1111_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ๹") in CONFIG:
      bstack11lll111l1_opy_ = CONFIG[bstack1l1111_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ๺")]
    if bstack1l1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ๻") in CONFIG:
      bstack1ll1llll_opy_ = int(bstack11lll111l1_opy_) * int(len(CONFIG[bstack1l1111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ๼")]))
    else:
      bstack1ll1llll_opy_ = int(bstack11lll111l1_opy_)
    config = Configuration(args)
    bstack1l1111ll1l_opy_ = config.paths
    if len(bstack1l1111ll1l_opy_) == 0:
      import glob
      pattern = bstack1l1111_opy_ (u"࠭ࠪࠫ࠱࠭࠲࡫࡫ࡡࡵࡷࡵࡩࠬ๽")
      bstack1lllllll11_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1lllllll11_opy_)
      config = Configuration(args)
      bstack1l1111ll1l_opy_ = config.paths
    bstack1l1lllll1l_opy_ = [os.path.normpath(item) for item in bstack1l1111ll1l_opy_]
    bstack11l1111ll1_opy_ = [os.path.normpath(item) for item in args]
    bstack11111l1ll_opy_ = [item for item in bstack11l1111ll1_opy_ if item not in bstack1l1lllll1l_opy_]
    import platform as pf
    if pf.system().lower() == bstack1l1111_opy_ (u"ࠧࡸ࡫ࡱࡨࡴࡽࡳࠨ๾"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1l1lllll1l_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1ll1lll11_opy_)))
                    for bstack1ll1lll11_opy_ in bstack1l1lllll1l_opy_]
    bstack1l1l1111l1_opy_ = []
    for spec in bstack1l1lllll1l_opy_:
      bstack1ll1111l1l_opy_ = []
      bstack1ll1111l1l_opy_ += bstack11111l1ll_opy_
      bstack1ll1111l1l_opy_.append(spec)
      bstack1l1l1111l1_opy_.append(bstack1ll1111l1l_opy_)
    execution_items = []
    for bstack1ll1111l1l_opy_ in bstack1l1l1111l1_opy_:
      if bstack1l1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ๿") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack1l1111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ຀")]):
          item = {}
          item[bstack1l1111_opy_ (u"ࠪࡥࡷ࡭ࠧກ")] = bstack1l1111_opy_ (u"ࠫࠥ࠭ຂ").join(bstack1ll1111l1l_opy_)
          item[bstack1l1111_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ຃")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack1l1111_opy_ (u"࠭ࡡࡳࡩࠪຄ")] = bstack1l1111_opy_ (u"ࠧࠡࠩ຅").join(bstack1ll1111l1l_opy_)
        item[bstack1l1111_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧຆ")] = 0
        execution_items.append(item)
    bstack1l1l1l1l1_opy_ = bstack1lll11l1ll_opy_(execution_items, bstack1ll1llll_opy_)
    for execution_item in bstack1l1l1l1l1_opy_:
      bstack111l11ll11_opy_ = []
      for item in execution_item:
        bstack111l11ll11_opy_.append(bstack11111111_opy_(name=str(item[bstack1l1111_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨງ")]),
                                             target=bstack11l1l1l1ll_opy_,
                                             args=(item[bstack1l1111_opy_ (u"ࠪࡥࡷ࡭ࠧຈ")],)))
      for t in bstack111l11ll11_opy_:
        t.start()
      for t in bstack111l11ll11_opy_:
        t.join()
  else:
    bstack11ll11l1l_opy_(bstack1ll111l11l_opy_)
  if not bstack11ll1lllll_opy_:
    bstack1ll111l1l1_opy_()
    if bstack1ll111111_opy_:
      bstack11ll111lll_opy_.end(EVENTS.bstack1l11l11l_opy_.value, bstack1ll111111_opy_ + bstack1l1111_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦຉ"), bstack1ll111111_opy_ + bstack1l1111_opy_ (u"ࠧࡀࡥ࡯ࡦࠥຊ"), status=True, failure=None, test_name=None)
  bstack111llll1ll_opy_.bstack1111ll1ll_opy_()
def browserstack_initialize(bstack1lll1l11ll_opy_=None):
  logger.info(bstack1l1111_opy_ (u"࠭ࡒࡶࡰࡱ࡭ࡳ࡭ࠠࡔࡆࡎࠤࡼ࡯ࡴࡩࠢࡤࡶ࡬ࡹ࠺ࠡࠩ຋") + str(bstack1lll1l11ll_opy_))
  run_on_browserstack(bstack1lll1l11ll_opy_, None, True)
@measure(event_name=EVENTS.bstack1ll111ll1l_opy_, stage=STAGE.bstack1111lll11_opy_, bstack1l1l111l_opy_=bstack11l1111lll_opy_)
def bstack1ll111l1l1_opy_():
  global CONFIG
  global bstack1ll11111l_opy_
  global bstack1l1l111lll_opy_
  global bstack1l111l1111_opy_
  global bstack1llllll11l_opy_
  bstack11ll1lll1_opy_.bstack1llll1l1ll_opy_()
  if cli.is_running():
    bstack1ll1111ll_opy_.invoke(bstack1ll1l11l_opy_.bstack1l1l11ll11_opy_)
  else:
    bstack111l1111_opy_ = bstack1l1llll1l_opy_.bstack111ll1lll1_opy_(config=CONFIG)
    bstack111l1111_opy_.bstack1l11l11111_opy_(CONFIG)
  hashed_id = None
  bstack1lll1ll1l1_opy_ = None
  def bstack11l11l1lll_opy_():
    try:
      if bstack1ll11111l_opy_ == bstack1l1111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧຌ"):
        if not cli.is_enabled(CONFIG):
          bstack11l11111l_opy_.stop()
      else:
        bstack11l11111l_opy_.stop()
    except Exception as e:
      logger.debug(bstack1l1111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡴࡶࡲࡴࡵ࡯࡮ࡨࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࢀࢃࠢຍ").format(e))
  def bstack11l1llll1_opy_():
    try:
      if not cli.is_enabled(CONFIG):
        bstack1lll11ll11_opy_.bstack1l1ll11l1_opy_()
    except Exception as e:
      logger.debug(bstack1l1111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡲࡵ࡭ࡳࡺࡩ࡯ࡩࠣࡦࡺ࡯࡬ࡥࠢ࡯࡭ࡳࡱ࠺ࠡࡽࢀࠦຎ").format(e))
  def bstack1ll1llll11_opy_():
    nonlocal hashed_id, bstack1lll1ll1l1_opy_
    try:
      if bstack1l1111_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧຏ") in CONFIG and str(CONFIG[bstack1l1111_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨຐ")]).lower() != bstack1l1111_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫຑ"):
        hashed_id, bstack1lll1ll1l1_opy_ = bstack1ll111ll_opy_()
      else:
        hashed_id, bstack1lll1ll1l1_opy_ = get_build_link()
    except Exception as e:
      logger.debug(bstack1l1111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࠥࡲࡩ࡯࡭࠽ࠤࢀࢃࠢຒ").format(e))
  bstack111lll1lll_opy_ = threading.Thread(target=bstack11l11l1lll_opy_)
  bstack1l1llll11l_opy_ = threading.Thread(target=bstack11l1llll1_opy_)
  bstack1l11l1111_opy_ = threading.Thread(target=bstack1ll1llll11_opy_)
  threads = [bstack111lll1lll_opy_, bstack1l1llll11l_opy_, bstack1l11l1111_opy_]
  for thread in threads:
    try:
      thread.start()
    except Exception as e:
      logger.debug(bstack1l1111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡳࡵࡣࡵࡸ࡮ࡴࡧࠡࡶ࡫ࡶࡪࡧࡤࠡࡽࢀ࠾ࠥࢁࡽࠣຓ").format(thread.name, e))
  for thread in threads:
    try:
      thread.join()
    except Exception as e:
      logger.debug(bstack1l1111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠ࡫ࡱ࡬ࡲ࡮ࡴࡧࠡࡶ࡫ࡶࡪࡧࡤࠡࡽࢀ࠾ࠥࢁࡽࠣດ").format(thread.name, e))
  bstack1lll11ll1l_opy_(hashed_id)
  logger.info(bstack1l1111_opy_ (u"ࠩࡖࡈࡐࠦࡲࡶࡰࠣࡩࡳࡪࡥࡥࠢࡩࡳࡷࠦࡩࡥ࠼ࠪຕ") + bstack1llllll11l_opy_.get_property(bstack1l1111_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࠬຖ"), bstack1l1111_opy_ (u"ࠫࠬທ")) + bstack1l1111_opy_ (u"ࠬ࠲ࠠࡵࡧࡶࡸ࡭ࡻࡢࠡ࡫ࡧ࠾ࠥ࠭ຘ") + os.getenv(bstack1l1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫນ"), bstack1l1111_opy_ (u"ࠧࠨບ")))
  if hashed_id is not None and bstack11l1lllll1_opy_() != -1:
    sessions = bstack1lll1llll_opy_(hashed_id)
    bstack111l1lll_opy_(sessions, bstack1lll1ll1l1_opy_)
  if bstack1ll11111l_opy_ == bstack1l1111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨປ") and bstack1l1l111lll_opy_ != 0:
    sys.exit(bstack1l1l111lll_opy_)
  if bstack1ll11111l_opy_ == bstack1l1111_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩຜ") and bstack1l111l1111_opy_ != 0:
    sys.exit(bstack1l111l1111_opy_)
def bstack1lll11ll1l_opy_(new_id):
    global bstack11ll1l111_opy_
    bstack11ll1l111_opy_ = new_id
def bstack11l11lll1_opy_(bstack11lll1l11_opy_):
  if bstack11lll1l11_opy_:
    return bstack11lll1l11_opy_.capitalize()
  else:
    return bstack1l1111_opy_ (u"ࠪࠫຝ")
@measure(event_name=EVENTS.bstack11l1l111_opy_, stage=STAGE.bstack1111lll11_opy_, bstack1l1l111l_opy_=bstack11l1111lll_opy_)
def bstack11ll1ll111_opy_(bstack1l1llll1_opy_):
  if bstack1l1111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩພ") in bstack1l1llll1_opy_ and bstack1l1llll1_opy_[bstack1l1111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪຟ")] != bstack1l1111_opy_ (u"࠭ࠧຠ"):
    return bstack1l1llll1_opy_[bstack1l1111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬມ")]
  else:
    bstack1l1l111l_opy_ = bstack1l1111_opy_ (u"ࠣࠤຢ")
    if bstack1l1111_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩຣ") in bstack1l1llll1_opy_ and bstack1l1llll1_opy_[bstack1l1111_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪ຤")] != None:
      bstack1l1l111l_opy_ += bstack1l1llll1_opy_[bstack1l1111_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫລ")] + bstack1l1111_opy_ (u"ࠧ࠲ࠠࠣ຦")
      if bstack1l1llll1_opy_[bstack1l1111_opy_ (u"࠭࡯ࡴࠩວ")] == bstack1l1111_opy_ (u"ࠢࡪࡱࡶࠦຨ"):
        bstack1l1l111l_opy_ += bstack1l1111_opy_ (u"ࠣ࡫ࡒࡗࠥࠨຩ")
      bstack1l1l111l_opy_ += (bstack1l1llll1_opy_[bstack1l1111_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ສ")] or bstack1l1111_opy_ (u"ࠪࠫຫ"))
      return bstack1l1l111l_opy_
    else:
      bstack1l1l111l_opy_ += bstack11l11lll1_opy_(bstack1l1llll1_opy_[bstack1l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬຬ")]) + bstack1l1111_opy_ (u"ࠧࠦࠢອ") + (
              bstack1l1llll1_opy_[bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨຮ")] or bstack1l1111_opy_ (u"ࠧࠨຯ")) + bstack1l1111_opy_ (u"ࠣ࠮ࠣࠦະ")
      if bstack1l1llll1_opy_[bstack1l1111_opy_ (u"ࠩࡲࡷࠬັ")] == bstack1l1111_opy_ (u"࡛ࠥ࡮ࡴࡤࡰࡹࡶࠦາ"):
        bstack1l1l111l_opy_ += bstack1l1111_opy_ (u"ࠦ࡜࡯࡮ࠡࠤຳ")
      bstack1l1l111l_opy_ += bstack1l1llll1_opy_[bstack1l1111_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩິ")] or bstack1l1111_opy_ (u"࠭ࠧີ")
      return bstack1l1l111l_opy_
@measure(event_name=EVENTS.bstack1llll11ll_opy_, stage=STAGE.bstack1111lll11_opy_, bstack1l1l111l_opy_=bstack11l1111lll_opy_)
def bstack111ll1lll_opy_(bstack11l111l1_opy_):
  if bstack11l111l1_opy_ == bstack1l1111_opy_ (u"ࠢࡥࡱࡱࡩࠧຶ"):
    return bstack1l1111_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽࡫ࡷ࡫ࡥ࡯࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥ࡫ࡷ࡫ࡥ࡯ࠤࡁࡇࡴࡳࡰ࡭ࡧࡷࡩࡩࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫື")
  elif bstack11l111l1_opy_ == bstack1l1111_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤຸ"):
    return bstack1l1111_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡸࡥࡥ࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡶࡪࡪࠢ࠿ࡈࡤ࡭ࡱ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃູ࠭")
  elif bstack11l111l1_opy_ == bstack1l1111_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧ຺ࠦ"):
    return bstack1l1111_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡨࡴࡨࡩࡳࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡨࡴࡨࡩࡳࠨ࠾ࡑࡣࡶࡷࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬົ")
  elif bstack11l111l1_opy_ == bstack1l1111_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧຼ"):
    return bstack1l1111_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡵࡩࡩࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡳࡧࡧࠦࡃࡋࡲࡳࡱࡵࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩຽ")
  elif bstack11l111l1_opy_ == bstack1l1111_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤ຾"):
    return bstack1l1111_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࠨ࡫ࡥࡢ࠵࠵࠺ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࠣࡦࡧࡤ࠷࠷࠼ࠢ࠿ࡖ࡬ࡱࡪࡵࡵࡵ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ຿")
  elif bstack11l111l1_opy_ == bstack1l1111_opy_ (u"ࠥࡶࡺࡴ࡮ࡪࡰࡪࠦເ"):
    return bstack1l1111_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡢ࡭ࡣࡦ࡯ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡢ࡭ࡣࡦ࡯ࠧࡄࡒࡶࡰࡱ࡭ࡳ࡭࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬແ")
  else:
    return bstack1l1111_opy_ (u"ࠬࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡤ࡯ࡥࡨࡱ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡤ࡯ࡥࡨࡱࠢ࠿ࠩໂ") + bstack11l11lll1_opy_(
      bstack11l111l1_opy_) + bstack1l1111_opy_ (u"࠭࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬໃ")
def bstack11lll11ll1_opy_(session):
  return bstack1l1111_opy_ (u"ࠧ࠽ࡶࡵࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡷࡵࡷࠣࡀ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠲ࡴࡡ࡮ࡧࠥࡂࡁࡧࠠࡩࡴࡨࡪࡂࠨࡻࡾࠤࠣࡸࡦࡸࡧࡦࡶࡀࠦࡤࡨ࡬ࡢࡰ࡮ࠦࡃࢁࡽ࠽࠱ࡤࡂࡁ࠵ࡴࡥࡀࡾࢁࢀࢃ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾࠲ࡸࡷࡄࠧໄ").format(
    session[bstack1l1111_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣࡠࡷࡵࡰࠬ໅")], bstack11ll1ll111_opy_(session), bstack111ll1lll_opy_(session[bstack1l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡵࡷࡥࡹࡻࡳࠨໆ")]),
    bstack111ll1lll_opy_(session[bstack1l1111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ໇")]),
    bstack11l11lll1_opy_(session[bstack1l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ່ࠬ")] or session[bstack1l1111_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩ້ࠬ")] or bstack1l1111_opy_ (u"໊࠭ࠧ")) + bstack1l1111_opy_ (u"ࠢࠡࠤ໋") + (session[bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪ໌")] or bstack1l1111_opy_ (u"ࠩࠪໍ")),
    session[bstack1l1111_opy_ (u"ࠪࡳࡸ࠭໎")] + bstack1l1111_opy_ (u"ࠦࠥࠨ໏") + session[bstack1l1111_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ໐")], session[bstack1l1111_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨ໑")] or bstack1l1111_opy_ (u"ࠧࠨ໒"),
    session[bstack1l1111_opy_ (u"ࠨࡥࡵࡩࡦࡺࡥࡥࡡࡤࡸࠬ໓")] if session[bstack1l1111_opy_ (u"ࠩࡦࡶࡪࡧࡴࡦࡦࡢࡥࡹ࠭໔")] else bstack1l1111_opy_ (u"ࠪࠫ໕"))
@measure(event_name=EVENTS.bstack1l1l1l1111_opy_, stage=STAGE.bstack1111lll11_opy_, bstack1l1l111l_opy_=bstack11l1111lll_opy_)
def bstack111l1lll_opy_(sessions, bstack1lll1ll1l1_opy_):
  try:
    bstack11l1111l_opy_ = bstack1l1111_opy_ (u"ࠦࠧ໖")
    if not os.path.exists(bstack1lll11l1l_opy_):
      os.mkdir(bstack1lll11l1l_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l1111_opy_ (u"ࠬࡧࡳࡴࡧࡷࡷ࠴ࡸࡥࡱࡱࡵࡸ࠳࡮ࡴ࡮࡮ࠪ໗")), bstack1l1111_opy_ (u"࠭ࡲࠨ໘")) as f:
      bstack11l1111l_opy_ = f.read()
    bstack11l1111l_opy_ = bstack11l1111l_opy_.replace(bstack1l1111_opy_ (u"ࠧࡼࠧࡕࡉࡘ࡛ࡌࡕࡕࡢࡇࡔ࡛ࡎࡕࠧࢀࠫ໙"), str(len(sessions)))
    bstack11l1111l_opy_ = bstack11l1111l_opy_.replace(bstack1l1111_opy_ (u"ࠨࡽࠨࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠫࡽࠨ໚"), bstack1lll1ll1l1_opy_)
    bstack11l1111l_opy_ = bstack11l1111l_opy_.replace(bstack1l1111_opy_ (u"ࠩࡾࠩࡇ࡛ࡉࡍࡆࡢࡒࡆࡓࡅࠦࡿࠪ໛"),
                                              sessions[0].get(bstack1l1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡱࡥࡲ࡫ࠧໜ")) if sessions[0] else bstack1l1111_opy_ (u"ࠫࠬໝ"))
    with open(os.path.join(bstack1lll11l1l_opy_, bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡷ࡫ࡰࡰࡴࡷ࠲࡭ࡺ࡭࡭ࠩໞ")), bstack1l1111_opy_ (u"࠭ࡷࠨໟ")) as stream:
      stream.write(bstack11l1111l_opy_.split(bstack1l1111_opy_ (u"ࠧࡼࠧࡖࡉࡘ࡙ࡉࡐࡐࡖࡣࡉࡇࡔࡂࠧࢀࠫ໠"))[0])
      for session in sessions:
        stream.write(bstack11lll11ll1_opy_(session))
      stream.write(bstack11l1111l_opy_.split(bstack1l1111_opy_ (u"ࠨࡽࠨࡗࡊ࡙ࡓࡊࡑࡑࡗࡤࡊࡁࡕࡃࠨࢁࠬ໡"))[1])
    logger.info(bstack1l1111_opy_ (u"ࠩࡊࡩࡳ࡫ࡲࡢࡶࡨࡨࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡧࡻࡩ࡭ࡦࠣࡥࡷࡺࡩࡧࡣࡦࡸࡸࠦࡡࡵࠢࡾࢁࠬ໢").format(bstack1lll11l1l_opy_));
  except Exception as e:
    logger.debug(bstack1llll11lll_opy_.format(str(e)))
def bstack1lll1llll_opy_(hashed_id):
  global CONFIG
  try:
    bstack1ll1lll11l_opy_ = datetime.datetime.now()
    host = bstack1l1111_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠮ࡥ࡯ࡳࡺࡪ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ໣") if bstack1l1111_opy_ (u"ࠫࡦࡶࡰࠨ໤") in CONFIG else bstack1l1111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡱ࡫࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭໥")
    user = CONFIG[bstack1l1111_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ໦")]
    key = CONFIG[bstack1l1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ໧")]
    bstack1l1lll11l1_opy_ = bstack1l1111_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ໨") if bstack1l1111_opy_ (u"ࠩࡤࡴࡵ࠭໩") in CONFIG else (bstack1l1111_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧ໪") if CONFIG.get(bstack1l1111_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨ໫")) else bstack1l1111_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ໬"))
    host = bstack11ll1l11_opy_(cli.config, [bstack1l1111_opy_ (u"ࠨࡡࡱ࡫ࡶࠦ໭"), bstack1l1111_opy_ (u"ࠢࡢࡲࡳࡅࡺࡺ࡯࡮ࡣࡷࡩࠧ໮"), bstack1l1111_opy_ (u"ࠣࡣࡳ࡭ࠧ໯")], host) if bstack1l1111_opy_ (u"ࠩࡤࡴࡵ࠭໰") in CONFIG else bstack11ll1l11_opy_(cli.config, [bstack1l1111_opy_ (u"ࠥࡥࡵ࡯ࡳࠣ໱"), bstack1l1111_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸࡪࠨ໲"), bstack1l1111_opy_ (u"ࠧࡧࡰࡪࠤ໳")], host)
    url = bstack1l1111_opy_ (u"࠭ࡻࡾ࠱ࡾࢁ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽ࠰ࡵࡨࡷࡸ࡯࡯࡯ࡵ࠱࡮ࡸࡵ࡮ࠨ໴").format(host, bstack1l1lll11l1_opy_, hashed_id)
    headers = {
      bstack1l1111_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭໵"): bstack1l1111_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ໶"),
    }
    proxies = bstack1l11ll11l1_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies, auth=(user, key))
    if response.json():
      cli.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺ࡨࡧࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࡥ࡬ࡪࡵࡷࠦ໷"), datetime.datetime.now() - bstack1ll1lll11l_opy_)
      return list(map(lambda session: session[bstack1l1111_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ໸")], response.json()))
  except Exception as e:
    logger.debug(bstack1ll11ll111_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack11111lll1_opy_, stage=STAGE.bstack1111lll11_opy_, bstack1l1l111l_opy_=bstack11l1111lll_opy_)
def get_build_link():
  global CONFIG
  global bstack11ll1l111_opy_
  try:
    if bstack1l1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ໹") in CONFIG:
      bstack1ll1lll11l_opy_ = datetime.datetime.now()
      host = bstack1l1111_opy_ (u"ࠬࡧࡰࡪ࠯ࡦࡰࡴࡻࡤࠨ໺") if bstack1l1111_opy_ (u"࠭ࡡࡱࡲࠪ໻") in CONFIG else bstack1l1111_opy_ (u"ࠧࡢࡲ࡬ࠫ໼")
      user = CONFIG[bstack1l1111_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ໽")]
      key = CONFIG[bstack1l1111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ໾")]
      bstack1l1lll11l1_opy_ = bstack1l1111_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩ໿") if bstack1l1111_opy_ (u"ࠫࡦࡶࡰࠨༀ") in CONFIG else bstack1l1111_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ༁")
      url = bstack1l1111_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡼࡿ࠽ࡿࢂࡆࡻࡾ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠯࡬ࡶࡳࡳ࠭༂").format(user, key, host, bstack1l1lll11l1_opy_)
      if cli.is_enabled(CONFIG):
        bstack1lll1ll1l1_opy_, hashed_id = cli.bstack11lll111l_opy_()
        logger.info(bstack1l1111111_opy_.format(bstack1lll1ll1l1_opy_))
        return [hashed_id, bstack1lll1ll1l1_opy_]
      else:
        headers = {
          bstack1l1111_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭༃"): bstack1l1111_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ༄"),
        }
        if bstack1l1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ༅") in CONFIG:
          params = {bstack1l1111_opy_ (u"ࠪࡲࡦࡳࡥࠨ༆"): CONFIG[bstack1l1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ༇")], bstack1l1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ༈"): CONFIG[bstack1l1111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ༉")]}
        else:
          params = {bstack1l1111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ༊"): CONFIG[bstack1l1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ་")]}
        proxies = bstack1l11ll11l1_opy_(CONFIG, url)
        response = requests.get(url, params=params, headers=headers, proxies=proxies)
        if response.json():
          bstack1ll1llll1_opy_ = response.json()[0][bstack1l1111_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡢࡶ࡫࡯ࡨࠬ༌")]
          if bstack1ll1llll1_opy_:
            bstack1lll1ll1l1_opy_ = bstack1ll1llll1_opy_[bstack1l1111_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥࡢࡹࡷࡲࠧ།")].split(bstack1l1111_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦ࠱ࡧࡻࡩ࡭ࡦࠪ༎"))[0] + bstack1l1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡷ࠴࠭༏") + bstack1ll1llll1_opy_[
              bstack1l1111_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ༐")]
            logger.info(bstack1l1111111_opy_.format(bstack1lll1ll1l1_opy_))
            bstack11ll1l111_opy_ = bstack1ll1llll1_opy_[bstack1l1111_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ༑")]
            bstack11l1lll11l_opy_ = CONFIG[bstack1l1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ༒")]
            if bstack1l1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ༓") in CONFIG:
              bstack11l1lll11l_opy_ += bstack1l1111_opy_ (u"ࠪࠤࠬ༔") + CONFIG[bstack1l1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭༕")]
            if bstack11l1lll11l_opy_ != bstack1ll1llll1_opy_[bstack1l1111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ༖")]:
              logger.debug(bstack1l1l111l1l_opy_.format(bstack1ll1llll1_opy_[bstack1l1111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ༗")], bstack11l1lll11l_opy_))
            cli.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠢࡩࡶࡷࡴ࠿࡭ࡥࡵࡡࡥࡹ࡮ࡲࡤࡠ࡮࡬ࡲࡰࠨ༘"), datetime.datetime.now() - bstack1ll1lll11l_opy_)
            return [bstack1ll1llll1_opy_[bstack1l1111_opy_ (u"ࠨࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧ༙ࠫ")], bstack1lll1ll1l1_opy_]
    else:
      logger.warning(bstack11llll1l1l_opy_)
  except Exception as e:
    logger.debug(bstack1l11111l11_opy_.format(str(e)))
  return [None, None]
def bstack1lll1l11_opy_(url, bstack1l1111l11_opy_=False):
  global CONFIG
  global bstack1111lllll_opy_
  if not bstack1111lllll_opy_:
    hostname = bstack1l11l1l1l1_opy_(url)
    is_private = bstack11ll1ll1_opy_(hostname)
    if (bstack1l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭༚") in CONFIG and not bstack1l1111lll1_opy_(CONFIG[bstack1l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ༛")])) and (is_private or bstack1l1111l11_opy_):
      bstack1111lllll_opy_ = hostname
def bstack1l11l1l1l1_opy_(url):
  return urlparse(url).hostname
def bstack11ll1ll1_opy_(hostname):
  for bstack111ll1ll11_opy_ in bstack1ll111l1l_opy_:
    regex = re.compile(bstack111ll1ll11_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack11l1l11l_opy_(bstack1l111111ll_opy_):
  return True if bstack1l111111ll_opy_ in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack1ll111ll1_opy_, stage=STAGE.bstack1111lll11_opy_, bstack1l1l111l_opy_=bstack11l1111lll_opy_)
def getAccessibilityResults(driver):
  global CONFIG
  global bstack1l1llll11_opy_
  bstack1ll1l111l1_opy_ = not (bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ༜"), None) and bstack111111lll_opy_(
          threading.current_thread(), bstack1l1111_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ༝"), None))
  bstack11ll11lll1_opy_ = getattr(driver, bstack1l1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭༞"), None) != True
  bstack1ll1l111ll_opy_ = bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ༟"), None) and bstack111111lll_opy_(
          threading.current_thread(), bstack1l1111_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ༠"), None)
  if bstack1ll1l111ll_opy_:
    if not bstack111lllll_opy_():
      logger.warning(bstack1l1111_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡴࡵࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡂࡲࡳࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷ࠳ࠨ༡"))
      return {}
    logger.debug(bstack1l1111_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡲࡦࡵࡸࡰࡹࡹࠧ༢"))
    logger.debug(perform_scan(driver, driver_command=bstack1l1111_opy_ (u"ࠫࡪࡾࡥࡤࡷࡷࡩࡘࡩࡲࡪࡲࡷࠫ༣")))
    results = bstack1ll11lll1l_opy_(bstack1l1111_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸࡸࠨ༤"))
    if results is not None and results.get(bstack1l1111_opy_ (u"ࠨࡩࡴࡵࡸࡩࡸࠨ༥")) is not None:
        return results[bstack1l1111_opy_ (u"ࠢࡪࡵࡶࡹࡪࡹࠢ༦")]
    logger.error(bstack1l1111_opy_ (u"ࠣࡐࡲࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡗ࡫ࡳࡶ࡮ࡷࡷࠥࡽࡥࡳࡧࠣࡪࡴࡻ࡮ࡥ࠰ࠥ༧"))
    return []
  if not bstack1l11l1l111_opy_.bstack11l111l1l_opy_(CONFIG, bstack1l1llll11_opy_) or (bstack11ll11lll1_opy_ and bstack1ll1l111l1_opy_):
    logger.warning(bstack1l1111_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶ࠲ࠧ༨"))
    return {}
  try:
    logger.debug(bstack1l1111_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡲࡦࡵࡸࡰࡹࡹࠧ༩"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack1l1111l1ll_opy_.bstack1l11lll11l_opy_)
    return results
  except Exception:
    logger.error(bstack1l1111_opy_ (u"ࠦࡓࡵࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡹࡨࡶࡪࠦࡦࡰࡷࡱࡨ࠳ࠨ༪"))
    return {}
@measure(event_name=EVENTS.bstack1llll1ll1l_opy_, stage=STAGE.bstack1111lll11_opy_, bstack1l1l111l_opy_=bstack11l1111lll_opy_)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack1l1llll11_opy_
  bstack1ll1l111l1_opy_ = not (bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ༫"), None) and bstack111111lll_opy_(
          threading.current_thread(), bstack1l1111_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ༬"), None))
  bstack11ll11lll1_opy_ = getattr(driver, bstack1l1111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧ༭"), None) != True
  bstack1ll1l111ll_opy_ = bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ༮"), None) and bstack111111lll_opy_(
          threading.current_thread(), bstack1l1111_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ༯"), None)
  if bstack1ll1l111ll_opy_:
    if not bstack111lllll_opy_():
      logger.warning(bstack1l1111_opy_ (u"ࠥࡒࡴࡺࠠࡢࡰࠣࡅࡵࡶࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࠡࡃࡳࡴࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡳࡶ࡯ࡰࡥࡷࡿ࠮ࠣ༰"))
      return {}
    logger.debug(bstack1l1111_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡢࡦࡨࡲࡶࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡳࡧࡶࡹࡱࡺࡳࠡࡵࡸࡱࡲࡧࡲࡺࠩ༱"))
    logger.debug(perform_scan(driver, driver_command=bstack1l1111_opy_ (u"ࠬ࡫ࡸࡦࡥࡸࡸࡪ࡙ࡣࡳ࡫ࡳࡸࠬ༲")))
    results = bstack1ll11lll1l_opy_(bstack1l1111_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹ࡙ࡵ࡮࡯ࡤࡶࡾࠨ༳"))
    if results is not None and results.get(bstack1l1111_opy_ (u"ࠢࡴࡷࡰࡱࡦࡸࡹࠣ༴")) is not None:
        return results[bstack1l1111_opy_ (u"ࠣࡵࡸࡱࡲࡧࡲࡺࠤ༵")]
    logger.error(bstack1l1111_opy_ (u"ࠤࡑࡳࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡘࡥࡴࡷ࡯ࡸࡸࠦࡓࡶ࡯ࡰࡥࡷࡿࠠࡸࡣࡶࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦ༶"))
    return {}
  if not bstack1l11l1l111_opy_.bstack11l111l1l_opy_(CONFIG, bstack1l1llll11_opy_) or (bstack11ll11lll1_opy_ and bstack1ll1l111l1_opy_):
    logger.warning(bstack1l1111_opy_ (u"ࠥࡒࡴࡺࠠࡢࡰࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡹࡵ࡮࡯ࡤࡶࡾ࠴༷ࠢ"))
    return {}
  try:
    logger.debug(bstack1l1111_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡢࡦࡨࡲࡶࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡳࡧࡶࡹࡱࡺࡳࠡࡵࡸࡱࡲࡧࡲࡺࠩ༸"))
    logger.debug(perform_scan(driver))
    bstack1ll1lll1ll_opy_ = driver.execute_async_script(bstack1l1111l1ll_opy_.bstack1lll1l1l1_opy_)
    return bstack1ll1lll1ll_opy_
  except Exception:
    logger.error(bstack1l1111_opy_ (u"ࠧࡔ࡯ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡸࡱࡲࡧࡲࡺࠢࡺࡥࡸࠦࡦࡰࡷࡱࡨ࠳ࠨ༹"))
    return {}
def bstack111lllll_opy_():
  global CONFIG
  global bstack1l1llll11_opy_
  bstack1lll11l111_opy_ = bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭༺"), None) and bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ༻"), None)
  if not bstack1l11l1l111_opy_.bstack11l111l1l_opy_(CONFIG, bstack1l1llll11_opy_) or not bstack1lll11l111_opy_:
        logger.warning(bstack1l1111_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡳࡴࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡲࡦࡵࡸࡰࡹࡹ࠮ࠣ༼"))
        return False
  return True
def bstack1ll11lll1l_opy_(result_type):
    bstack1l1l11l11l_opy_ = bstack11l11111l_opy_.current_test_uuid() if bstack11l11111l_opy_.current_test_uuid() else bstack1lll11ll11_opy_.current_hook_uuid()
    with ThreadPoolExecutor() as executor:
        future = executor.submit(bstack1l11l1ll11_opy_(bstack1l1l11l11l_opy_, result_type))
        try:
            return future.result(timeout=bstack11l11llll1_opy_)
        except TimeoutError:
            logger.error(bstack1l1111_opy_ (u"ࠤࡗ࡭ࡲ࡫࡯ࡶࡶࠣࡥ࡫ࡺࡥࡳࠢࡾࢁࡸࠦࡷࡩ࡫࡯ࡩࠥ࡬ࡥࡵࡥ࡫࡭ࡳ࡭ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡓࡧࡶࡹࡱࡺࡳࠣ༽").format(bstack11l11llll1_opy_))
        except Exception as ex:
            logger.debug(bstack1l1111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡵࡩࡹࡸࡩࡦࡸ࡬ࡲ࡬ࠦࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡼࡿ࠱ࠤࡊࡸࡲࡰࡴࠣ࠱ࠥࢁࡽࠣ༾").format(result_type, str(ex)))
    return {}
@measure(event_name=EVENTS.bstack11l1l1llll_opy_, stage=STAGE.bstack1111lll11_opy_, bstack1l1l111l_opy_=bstack11l1111lll_opy_)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack1l1llll11_opy_
  bstack1ll1l111l1_opy_ = not (bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ༿"), None) and bstack111111lll_opy_(
          threading.current_thread(), bstack1l1111_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫཀ"), None))
  bstack11lll1111l_opy_ = not (bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ཁ"), None) and bstack111111lll_opy_(
          threading.current_thread(), bstack1l1111_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩག"), None))
  bstack11ll11lll1_opy_ = getattr(driver, bstack1l1111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨགྷ"), None) != True
  if not bstack1l11l1l111_opy_.bstack11l111l1l_opy_(CONFIG, bstack1l1llll11_opy_) or (bstack11ll11lll1_opy_ and bstack1ll1l111l1_opy_ and bstack11lll1111l_opy_):
    logger.warning(bstack1l1111_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡸࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡣࡢࡰ࠱ࠦང"))
    return {}
  try:
    bstack1llll1l111_opy_ = bstack1l1111_opy_ (u"ࠪࡥࡵࡶࠧཅ") in CONFIG and CONFIG.get(bstack1l1111_opy_ (u"ࠫࡦࡶࡰࠨཆ"), bstack1l1111_opy_ (u"ࠬ࠭ཇ"))
    session_id = getattr(driver, bstack1l1111_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠪ཈"), None)
    if not session_id:
      logger.warning(bstack1l1111_opy_ (u"ࠢࡏࡱࠣࡷࡪࡹࡳࡪࡱࡱࠤࡎࡊࠠࡧࡱࡸࡲࡩࠦࡦࡰࡴࠣࡨࡷ࡯ࡶࡦࡴࠥཉ"))
      return {bstack1l1111_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢཊ"): bstack1l1111_opy_ (u"ࠤࡑࡳࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡉࡅࠢࡩࡳࡺࡴࡤࠣཋ")}
    if bstack1llll1l111_opy_:
      try:
        bstack1ll11l111_opy_ = {
              bstack1l1111_opy_ (u"ࠪࡸ࡭ࡐࡷࡵࡖࡲ࡯ࡪࡴࠧཌ"): os.environ.get(bstack1l1111_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩཌྷ"), os.environ.get(bstack1l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩཎ"), bstack1l1111_opy_ (u"࠭ࠧཏ"))),
              bstack1l1111_opy_ (u"ࠧࡵࡪࡗࡩࡸࡺࡒࡶࡰࡘࡹ࡮ࡪࠧཐ"): bstack11l11111l_opy_.current_test_uuid() if bstack11l11111l_opy_.current_test_uuid() else bstack1lll11ll11_opy_.current_hook_uuid(),
              bstack1l1111_opy_ (u"ࠨࡣࡸࡸ࡭ࡎࡥࡢࡦࡨࡶࠬད"): os.environ.get(bstack1l1111_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧདྷ")),
              bstack1l1111_opy_ (u"ࠪࡷࡨࡧ࡮ࡕ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪན"): str(int(datetime.datetime.now().timestamp() * 1000)),
              bstack1l1111_opy_ (u"ࠫࡹ࡮ࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩཔ"): os.environ.get(bstack1l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪཕ"), bstack1l1111_opy_ (u"࠭ࠧབ")),
              bstack1l1111_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪࠧབྷ"): kwargs.get(bstack1l1111_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࡠࡥࡲࡱࡲࡧ࡮ࡥࠩམ"), None) or bstack1l1111_opy_ (u"ࠩࠪཙ")
          }
        if not hasattr(thread_local, bstack1l1111_opy_ (u"ࠪࡦࡦࡹࡥࡠࡣࡳࡴࡤࡧ࠱࠲ࡻࡢࡷࡨࡸࡩࡱࡶࠪཚ")):
            scripts = {bstack1l1111_opy_ (u"ࠫࡸࡩࡡ࡯ࠩཛ"): bstack1l1111l1ll_opy_.perform_scan}
            thread_local.base_app_a11y_script = scripts
        bstack11ll11l11_opy_ = copy.deepcopy(thread_local.base_app_a11y_script)
        bstack11ll11l11_opy_[bstack1l1111_opy_ (u"ࠬࡹࡣࡢࡰࠪཛྷ")] = bstack11ll11l11_opy_[bstack1l1111_opy_ (u"࠭ࡳࡤࡣࡱࠫཝ")] % json.dumps(bstack1ll11l111_opy_)
        bstack1l1111l1ll_opy_.bstack1l1l11lll1_opy_(bstack11ll11l11_opy_)
        bstack1l1111l1ll_opy_.store()
        bstack1l1ll111l1_opy_ = driver.execute_script(bstack1l1111l1ll_opy_.perform_scan)
      except Exception as bstack1lllll111_opy_:
        logger.info(bstack1l1111_opy_ (u"ࠢࡂࡲࡳ࡭ࡺࡳࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡥࡤࡲࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࠢཞ") + str(bstack1lllll111_opy_))
        bstack1l1ll111l1_opy_ = {bstack1l1111_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢཟ"): str(bstack1lllll111_opy_)}
    else:
      bstack1l1ll111l1_opy_ = driver.execute_async_script(bstack1l1111l1ll_opy_.perform_scan, {bstack1l1111_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࠩའ"): kwargs.get(bstack1l1111_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࡢࡧࡴࡳ࡭ࡢࡰࡧࠫཡ"), None) or bstack1l1111_opy_ (u"ࠫࠬར")})
    return bstack1l1ll111l1_opy_
  except Exception as err:
    logger.error(bstack1l1111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡴࡸࡲࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡣࡢࡰ࠱ࠤࢀࢃࠢལ").format(str(err)))
    return {}