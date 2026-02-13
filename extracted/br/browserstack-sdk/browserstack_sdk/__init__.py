# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
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
import inspect
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import json
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from browserstack_sdk.bstack1ll11ll1l1_opy_ import bstack11lll1ll_opy_
from browserstack_sdk.bstack1ll1l1l11_opy_ import *
import time
import requests
from bstack_utils.constants import EVENTS, STAGE, bstack11l11111l1_opy_
from bstack_utils.messages import bstack11lll11ll1_opy_, bstack111l11lll1_opy_, bstack11l1ll1ll1_opy_, bstack11ll1lll_opy_, bstack1lllll11_opy_, bstack1lll1ll1l_opy_
from bstack_utils.measure import measure
from bstack_utils.logger_utils import get_logger
from bstack_utils.helper import bstack1llll1l111_opy_
from browserstack_sdk.bstack1l11l11l1_opy_ import bstack111ll11l11_opy_
logger = get_logger(__name__)
def bstack11l1ll1lll_opy_():
  global CONFIG
  headers = {
        bstack11l11_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack11l11_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1llll1l111_opy_(CONFIG, bstack11l11111l1_opy_)
  try:
    response = requests.get(bstack11l11111l1_opy_, headers=headers, proxies=proxies, timeout=2)
    if response.json():
      bstack1l1l11ll_opy_ = response.json()[bstack11l11_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack11lll11ll1_opy_.format(response.json()))
      return bstack1l1l11ll_opy_
    else:
      logger.debug(bstack111l11lll1_opy_.format(bstack11l11_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack111l11lll1_opy_.format(e))
def bstack1l111l1l1l_opy_(hub_url):
  global CONFIG
  url = bstack11l11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack11l11_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack11l11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack11l11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1llll1l111_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=(0.5, 1.0))
    latency = time.perf_counter() - start_time
    logger.debug(bstack11l1ll1ll1_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack11ll1lll_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack1lll1111l1_opy_, stage=STAGE.bstack111ll11l1_opy_)
def bstack11l1l1l1l1_opy_():
  try:
    global bstack1ll1l1l1ll_opy_
    global CONFIG
    if bstack11l11_opy_ (u"ࠫ࡭ࡻࡢࡓࡧࡪ࡭ࡴࡴࠧࡾ") in CONFIG and CONFIG[bstack11l11_opy_ (u"ࠬ࡮ࡵࡣࡔࡨ࡫࡮ࡵ࡮ࠨࡿ")]:
      from bstack_utils.constants import bstack1ll1lllll1_opy_
      bstack111l1l1lll_opy_ = CONFIG[bstack11l11_opy_ (u"࠭ࡨࡶࡤࡕࡩ࡬࡯࡯࡯ࠩࢀ")]
      if bstack111l1l1lll_opy_ in bstack1ll1lllll1_opy_:
        bstack1ll1l1l1ll_opy_ = bstack1ll1lllll1_opy_[bstack111l1l1lll_opy_]
        logger.debug(bstack1lllll11_opy_.format(bstack1ll1l1l1ll_opy_))
        return
      else:
        logger.debug(bstack11l11_opy_ (u"ࠢࡉࡷࡥࠤࡰ࡫ࡹࠡࠩࡾࢁࠬࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࡎࡕࡃࡡࡘࡖࡑࡥࡍࡂࡒ࠯ࠤ࡫ࡧ࡬࡭࡫ࡱ࡫ࠥࡨࡡࡤ࡭ࠣࡸࡴࠦ࡯ࡱࡶ࡬ࡱࡦࡲࠠࡩࡷࡥࠤࡩ࡫ࡴࡦࡥࡷ࡭ࡴࡴࠢࢁ").format(bstack111l1l1lll_opy_))
    bstack1l1l11ll_opy_ = bstack11l1ll1lll_opy_()
    from concurrent.futures import ThreadPoolExecutor, as_completed
    if bstack1l1l11ll_opy_:
        with ThreadPoolExecutor(max_workers=len(bstack1l1l11ll_opy_)) as executor:
            bstack1l1l11l1l_opy_ = {executor.submit(bstack1l111l1l1l_opy_, bstack1lll111l11_opy_): bstack1lll111l11_opy_ for bstack1lll111l11_opy_ in bstack1l1l11ll_opy_}
            for future in as_completed(bstack1l1l11l1l_opy_):
                result = future.result()
                if result and result.get(bstack11l11_opy_ (u"ࠨ࡮ࡤࡸࡪࡴࡣࡺࠩࢂ")) is not None:
                    bstack1ll1l1l1ll_opy_ = result[bstack11l11_opy_ (u"ࠩ࡫ࡹࡧࡥࡵࡳ࡮ࠪࢃ")]
                    logger.debug(bstack1lllll11_opy_.format(bstack1ll1l1l1ll_opy_))
                    return
        bstack1ll1l1l1ll_opy_ = bstack1l1l11ll_opy_[0]
        logger.debug(bstack1lllll11_opy_.format(bstack1ll1l1l1ll_opy_))
        return
  except Exception as e:
    logger.debug(bstack1lll1ll1l_opy_.format(e))
from browserstack_sdk.bstack1ll1l111ll_opy_ import *
from browserstack_sdk.bstack1l11l11l1_opy_ import *
from browserstack_sdk.bstack11llll11_opy_ import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.logger_utils import get_logger
from bstack_utils.measure import measure
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack11l1l111_opy_, stage=STAGE.bstack111ll11l1_opy_)
def bstack1l11ll11l1_opy_():
    global bstack1ll1l1l1ll_opy_
    try:
        bstack1ll1ll1ll1_opy_ = bstack11l11l11l_opy_()
        bstack111ll1l1l_opy_(bstack1ll1ll1ll1_opy_)
        hub_url = bstack1ll1ll1ll1_opy_.get(bstack11l11_opy_ (u"ࠥࡹࡷࡲࠢࢄ"), bstack11l11_opy_ (u"ࠦࠧࢅ"))
        if hub_url.endswith(bstack11l11_opy_ (u"ࠬ࠵ࡷࡥ࠱࡫ࡹࡧ࠭ࢆ")):
            hub_url = hub_url.rsplit(bstack11l11_opy_ (u"࠭࠯ࡸࡦ࠲࡬ࡺࡨࠧࢇ"), 1)[0]
        if hub_url.startswith(bstack11l11_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࠨ࢈")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack11l11_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࠪࢉ")):
            hub_url = hub_url[8:]
        bstack1ll1l1l1ll_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack11l11l11l_opy_():
    global CONFIG
    bstack1l1111l1l1_opy_ = CONFIG.get(bstack11l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢊ"), {}).get(bstack11l11_opy_ (u"ࠪ࡫ࡷ࡯ࡤࡏࡣࡰࡩࠬࢋ"), bstack11l11_opy_ (u"ࠫࡓࡕ࡟ࡈࡔࡌࡈࡤࡔࡁࡎࡇࡢࡔࡆ࡙ࡓࡆࡆࠪࢌ"))
    if not isinstance(bstack1l1111l1l1_opy_, str):
        raise ValueError(bstack11l11_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡌࡸࡩࡥࠢࡱࡥࡲ࡫ࠠ࡮ࡷࡶࡸࠥࡨࡥࠡࡣࠣࡺࡦࡲࡩࡥࠢࡶࡸࡷ࡯࡮ࡨࠤࢍ"))
    try:
        bstack1ll1ll1ll1_opy_ = bstack1l111l1l11_opy_(bstack1l1111l1l1_opy_)
        return bstack1ll1ll1ll1_opy_
    except Exception as e:
        logger.error(bstack11l11_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡩࡵ࡭ࡩࠦࡤࡦࡶࡤ࡭ࡱࡹࠠ࠻ࠢࡾࢁࠧࢎ").format(str(e)))
        return {}
def bstack1l111l1l11_opy_(bstack1l1111l1l1_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack11l11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ࢏")] or not CONFIG[bstack11l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ࢐")]:
            raise ValueError(bstack11l11_opy_ (u"ࠤࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠤࡴࡸࠠࡢࡥࡦࡩࡸࡹࠠ࡬ࡧࡼࠦ࢑"))
        url = bstack1l11111l1_opy_ + bstack1l1111l1l1_opy_
        auth = (CONFIG[bstack11l11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ࢒")], CONFIG[bstack11l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ࢓")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack1l1l111ll1_opy_ = json.loads(response.text)
            return bstack1l1l111ll1_opy_
    except ValueError as ve:
        logger.error(bstack11l11_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡩࡵ࡭ࡩࠦࡤࡦࡶࡤ࡭ࡱࡹࠠ࠻ࠢࡾࢁࠧ࢔").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack11l11_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡪࡶ࡮ࡪࠠࡥࡧࡷࡥ࡮ࡲࡳࠡ࠼ࠣࡿࢂࠨ࢕").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack111ll1l1l_opy_(bstack1l1l11l111_opy_):
    global CONFIG
    if bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ࢖") not in CONFIG or str(CONFIG[bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬࢗ")]).lower() == bstack11l11_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ࢘"):
        CONFIG[bstack11l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭࢙ࠩ")] = False
    elif bstack11l11_opy_ (u"ࠫ࡮ࡹࡔࡳ࡫ࡤࡰࡌࡸࡩࡥ࢚ࠩ") in bstack1l1l11l111_opy_:
        bstack1ll1111l1_opy_ = CONFIG.get(bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴ࢛ࠩ"), {})
        logger.debug(bstack11l11_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡸࡪࡵࡷ࡭ࡳ࡭ࠠ࡭ࡱࡦࡥࡱࠦ࡯ࡱࡶ࡬ࡳࡳࡹ࠺ࠡࠧࡶࠦ࢜"), bstack1ll1111l1_opy_)
        bstack11l1l111l_opy_ = bstack1l1l11l111_opy_.get(bstack11l11_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡒࡦࡲࡨࡥࡹ࡫ࡲࡴࠤ࢝"), [])
        bstack1ll1ll11ll_opy_ = bstack11l11_opy_ (u"ࠣ࠮ࠥ࢞").join(bstack11l1l111l_opy_)
        logger.debug(bstack11l11_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡅࡸࡷࡹࡵ࡭ࠡࡴࡨࡴࡪࡧࡴࡦࡴࠣࡷࡹࡸࡩ࡯ࡩ࠽ࠤࠪࡹࠢ࢟"), bstack1ll1ll11ll_opy_)
        bstack1l111ll1_opy_ = {
            bstack11l11_opy_ (u"ࠥࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧࢠ"): bstack11l11_opy_ (u"ࠦࡦࡺࡳ࠮ࡴࡨࡴࡪࡧࡴࡦࡴࠥࢡ"),
            bstack11l11_opy_ (u"ࠧ࡬࡯ࡳࡥࡨࡐࡴࡩࡡ࡭ࠤࢢ"): bstack11l11_opy_ (u"ࠨࡴࡳࡷࡨࠦࢣ"),
            bstack11l11_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࠭ࡳࡧࡳࡩࡦࡺࡥࡳࠤࢤ"): bstack1ll1ll11ll_opy_
        }
        bstack1ll1111l1_opy_.update(bstack1l111ll1_opy_)
        logger.debug(bstack11l11_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡖࡲࡧࡥࡹ࡫ࡤࠡ࡮ࡲࡧࡦࡲࠠࡰࡲࡷ࡭ࡴࡴࡳ࠻ࠢࠨࡷࠧࢥ"), bstack1ll1111l1_opy_)
        CONFIG[bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢦ")] = bstack1ll1111l1_opy_
        logger.debug(bstack11l11_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡉ࡭ࡳࡧ࡬ࠡࡅࡒࡒࡋࡏࡇ࠻ࠢࠨࡷࠧࢧ"), CONFIG)
def bstack1l1ll1ll11_opy_():
    bstack1ll1ll1ll1_opy_ = bstack11l11l11l_opy_()
    if not bstack1ll1ll1ll1_opy_[bstack11l11_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡖࡴ࡯ࠫࢨ")]:
      raise ValueError(bstack11l11_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡗࡵࡰࠥ࡯ࡳࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡩࡶࡴࡳࠠࡨࡴ࡬ࡨࠥࡪࡥࡵࡣ࡬ࡰࡸ࠴ࠢࢩ"))
    return bstack1ll1ll1ll1_opy_[bstack11l11_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡘࡶࡱ࠭ࢪ")] + bstack11l11_opy_ (u"ࠧࡀࡥࡤࡴࡸࡃࠧࢫ")
@measure(event_name=EVENTS.bstack1l1111lll1_opy_, stage=STAGE.bstack111ll11l1_opy_)
def bstack11l1l11l1_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack11l11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪࢬ")], CONFIG[bstack11l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬࢭ")])
        url = bstack111l1l1111_opy_
        logger.debug(bstack11l11_opy_ (u"ࠥࡅࡹࡺࡥ࡮ࡲࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴࠢࡩࡶࡴࡳࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡔࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠣࡅࡕࡏࠢࢮ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack11l11_opy_ (u"ࠦࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠥࢯ"): bstack11l11_opy_ (u"ࠧࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠣࢰ")})
            if response.status_code == 200:
                bstack1l1lll11ll_opy_ = json.loads(response.text)
                bstack1111lll111_opy_ = bstack1l1lll11ll_opy_.get(bstack11l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡸ࠭ࢱ"), [])
                if bstack1111lll111_opy_:
                    bstack11lll1111_opy_ = bstack1111lll111_opy_[0]
                    build_hashed_id = bstack11lll1111_opy_.get(bstack11l11_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪࢲ"))
                    bstack1l11l1l111_opy_ = bstack1l1ll1111_opy_ + build_hashed_id
                    result.extend([build_hashed_id, bstack1l11l1l111_opy_])
                    logger.info(bstack111l11l1l1_opy_.format(bstack1l11l1l111_opy_))
                    bstack11lll1l1_opy_ = CONFIG[bstack11l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫࢳ")]
                    if bstack11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࢴ") in CONFIG:
                      bstack11lll1l1_opy_ += bstack11l11_opy_ (u"ࠪࠤࠬࢵ") + CONFIG[bstack11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࢶ")]
                    if bstack11lll1l1_opy_ != bstack11lll1111_opy_.get(bstack11l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪࢷ")):
                      logger.debug(bstack11l11ll1_opy_.format(bstack11lll1111_opy_.get(bstack11l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫࢸ")), bstack11lll1l1_opy_))
                    return result
                else:
                    logger.debug(bstack11l11_opy_ (u"ࠢࡂࡖࡖࠤ࠿ࠦࡎࡰࠢࡥࡹ࡮ࡲࡤࡴࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠱ࠦࢹ"))
            else:
                logger.debug(bstack11l11_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴ࠰ࠥࢺ"))
        except Exception as e:
            logger.error(bstack11l11_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࡶࠤ࠿ࠦࡻࡾࠤࢻ").format(str(e)))
    else:
        logger.debug(bstack11l11_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡆࡓࡓࡌࡉࡈࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡶࡩࡹ࠴ࠠࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴ࠰ࠥࢼ"))
    return [None, None]
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1l11l11111_opy_ import bstack1l11l11111_opy_, bstack11ll111111_opy_, bstack11ll1lllll_opy_, bstack111l1ll1l_opy_
from bstack_utils.measure import bstack11ll11ll1l_opy_
from bstack_utils.measure import measure
from bstack_utils.percy import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1ll1ll11l_opy_ import bstack111lll111_opy_
from bstack_utils.messages import *
from bstack_utils import logger_utils
from bstack_utils.constants import *
from bstack_utils.helper import bstack11l1l1llll_opy_, bstack1l11l11ll1_opy_, bstack1l11l1llll_opy_, bstack11ll11l11_opy_, \
  bstack1ll111l11_opy_, \
  Notset, is_robot_playwright_installed, bstack1l1l1llll_opy_, \
  bstack1l1111ll_opy_, bstack11l11llll1_opy_, bstack1llllllll_opy_, bstack11l1lllll1_opy_, bstack11lll1111l_opy_, bstack1l1l1l1lll_opy_, \
  bstack1l1lllll1_opy_, \
  bstack1l11llllll_opy_, bstack1l111l11l_opy_, bstack111llll1_opy_, bstack111ll11111_opy_, \
  bstack11111l111_opy_, bstack111111111_opy_, bstack1ll1l11lll_opy_, bstack111l111ll1_opy_, bstack1l1l1111l1_opy_
from bstack_utils.bstack111ll1111l_opy_ import bstack11l111ll1_opy_
from bstack_utils.bstack1lll1llll_opy_ import bstack1ll1llll_opy_, bstack11l1l1111l_opy_
from bstack_utils.bstack1l111l1ll_opy_ import bstack111l111l1_opy_
from bstack_utils.bstack1ll111l1l1_opy_ import bstack1ll1l1l1_opy_, bstack1l11lll11l_opy_
from bstack_utils.bstack1l1lll111l_opy_ import bstack1l1lll111l_opy_
from bstack_utils.bstack11ll11111_opy_ import bstack1lll1l1ll1_opy_
from bstack_utils.proxy import bstack11l11l1ll1_opy_, bstack1llll1l111_opy_, bstack111l11l11_opy_, bstack1l1l11l11l_opy_
from bstack_utils.bstack1ll1ll111_opy_ import bstack11ll1llll_opy_, bstack1l1111111l_opy_
import bstack_utils.bstack11l1l11lll_opy_ as bstack1l11l1l1l1_opy_
import bstack_utils.bstack11llll11l1_opy_ as bstack1ll11l11ll_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.utils.bstack1l11l111ll_opy_ import bstack1l1ll111l_opy_
from bstack_utils.bstack1l11ll1l_opy_ import bstack1l11l1l1ll_opy_
from bstack_utils.bstack1l11l1l11_opy_ import bstack1ll11l111_opy_
from bstack_utils.bstack11ll11ll1l_opy_ import bstack111l1lllll_opy_
if os.getenv(bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡉࡑࡒࡏࡘ࠭ࢽ")):
  cli.bstack1l1l11ll1l_opy_()
else:
  os.environ[bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡊࡒࡓࡐ࡙ࠧࢾ")] = bstack11l11_opy_ (u"࠭ࡴࡳࡷࡨࠫࢿ")
bstack1ll1ll1lll_opy_ = bstack11l11_opy_ (u"ࠧࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠠࠡ࡫ࡩࠬࡵࡧࡧࡦࠢࡀࡁࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠠࡼ࡞ࡱࠤࠥࠦࡴࡳࡻࡾࡠࡳࠦࡣࡰࡰࡶࡸࠥ࡬ࡳࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࡡ࠭ࡦࡴ࡞ࠪ࠭ࡀࡢ࡮ࠡࠢࠣࠤࠥ࡬ࡳ࠯ࡣࡳࡴࡪࡴࡤࡇ࡫࡯ࡩࡘࡿ࡮ࡤࠪࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠬࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡳࡣ࡮ࡴࡤࡦࡺࠬࠤ࠰ࠦࠢ࠻ࠤࠣ࠯ࠥࡐࡓࡐࡐ࠱ࡷࡹࡸࡩ࡯ࡩ࡬ࡪࡾ࠮ࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࠬࡦࡽࡡࡪࡶࠣࡲࡪࡽࡐࡢࡩࡨ࠶࠳࡫ࡶࡢ࡮ࡸࡥࡹ࡫ࠨࠣࠪࠬࠤࡂࡄࠠࡼࡿࠥ࠰ࠥࡢࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡨࡧࡷࡗࡪࡹࡳࡪࡱࡱࡈࡪࡺࡡࡪ࡮ࡶࠦࢂࡢࠧࠪࠫࠬ࡟ࠧ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠣ࡟ࠬࠤ࠰ࠦࠢ࠭࡞࡟ࡲࠧ࠯࡜࡯ࠢࠣࠤࠥࢃࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡽ࡝ࡰࠣࠤ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠧࣀ")
LAUNCH_PATCH_ROBOT_PLAYWRIGHT = bstack11l11_opy_ (u"ࠨ࡞ࡱ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࡢ࡮ࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡰࡢࡶ࡫ࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳࡞࡞ࡱࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠴ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡶ࡟ࡪࡰࡧࡩࡽࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠴ࡠࡠࡳࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡹ࡬ࡪࡥࡨࠬ࠵࠲ࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࠬࡠࡳࡩ࡯࡯ࡵࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬ࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ࠭ࡀࡢ࡮ࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮࡭ࡣࡸࡲࡨ࡮ࠠ࠾ࠢࡤࡷࡾࡴࡣࠡࠪ࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴࠫࠣࡁࡃࠦࡻ࡝ࡰ࡯ࡩࡹࠦࡣࡢࡲࡶ࠿ࡡࡴࡴࡳࡻࠣࡿࡡࡴࡣࡢࡲࡶࠤࡂࠦࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠪ࡞ࡱࠤࠥࢃࠠࡤࡣࡷࡧ࡭࠮ࡥࡹࠫࠣࡿࡡࡴࠠࠡࠢࠣࢁࡡࡴࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡣࡺࡥ࡮ࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮ࡤࡱࡱࡲࡪࡩࡴࠩࡽ࡟ࡲࠥࠦࠠࠡࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸ࠿ࠦࡠࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠦࡾࡩࡳࡩ࡯ࡥࡧࡘࡖࡎࡉ࡯࡮ࡲࡲࡲࡪࡴࡴࠩࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡦࡥࡵࡹࠩࠪࡿࡣ࠰ࡡࡴࠠࠡࠢࠣ࠲࠳࠴࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸࡢ࡮ࠡࠢࢀ࠭ࡡࡴࡽ࡝ࡰࡦࡳࡳࡹࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡧࡴࡴ࡮ࡦࡥࡷࠤࡂࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺ࠮ࡣ࡫ࡱࡨ࠭࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠮ࡁ࡜࡯࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭࠯ࡥࡲࡲࡳ࡫ࡣࡵࠢࡀࠤࡦࡹࡹ࡯ࡥࠣࠬࡨࡵ࡮࡯ࡧࡦࡸࡔࡶࡴࡪࡱࡱࡷ࠮ࠦ࠽࠿ࠢࡾࡠࡳࠦࠠ࡭ࡧࡷࠤࡨࡧࡰࡴ࠽࡟ࡲࠥࠦࡴࡳࡻࠣࡿࡡࡴࠠࠡࠢࠣࡧࡦࡶࡳࠡ࠿ࠣࡎࡘࡕࡎ࠯ࡲࡤࡶࡸ࡫ࠨࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷ࠮ࡢ࡮ࠡࠢࢀࠤࡨࡧࡴࡤࡪࠫࡩࡽ࠯ࠠࡼ࡞ࡱࠤࠥࢃ࡜࡯ࠢࠣࡧࡴࡴࡳࡵࠢࡰࡳࡩ࡯ࡦࡪࡧࡧࡉࡳࡪࡰࡰ࡫ࡱࡸࠥࡃࠠࡡࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࡣࠤ࠰ࠦࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭ࡀࡢ࡮ࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤ࠳࠴࠮ࡤࡱࡱࡲࡪࡩࡴࡐࡲࡷ࡭ࡴࡴࡳ࠭࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࡝ࡰࠣࠤࢂ࠯࡜࡯ࡿ࡟ࡲ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵࡜࡯ࠩࣁ")
from ._version import __version__
bstack1l1l111ll_opy_ = None
CONFIG = {}
bstack11ll11lll1_opy_ = {}
bstack1lllll1l11_opy_ = {}
bstack1111ll1l1_opy_ = None
bstack1l11ll11_opy_ = None
bstack11l1111lll_opy_ = None
bstack111llll1ll_opy_ = -1
bstack1ll1l111l_opy_ = 0
bstack1l1ll1llll_opy_ = bstack11ll111l_opy_
bstack1l111lll11_opy_ = 1
bstack11lllll1l_opy_ = False
bstack111l1111ll_opy_ = False
bstack11l1111ll1_opy_ = bstack11l11_opy_ (u"ࠩࠪࣂ")
bstack1l1lll1l11_opy_ = bstack11l11_opy_ (u"ࠪࠫࣃ")
bstack11lll1l11_opy_ = False
bstack111l1l11_opy_ = True
bstack1ll11l1111_opy_ = False
bstack111lll11_opy_ = bstack11l11_opy_ (u"ࠫࠬࣄ")
bstack111l1llll1_opy_ = []
bstack1ll1ll1l1_opy_ = threading.Lock()
bstack1l1ll1l11_opy_ = threading.Lock()
bstack1l11l11ll_opy_ = None
bstack1ll1l1l1ll_opy_ = bstack11l11_opy_ (u"ࠬ࠭ࣅ")
bstack1l1lllll_opy_ = False
bstack11l11l11l1_opy_ = None
bstack11llll1111_opy_ = None
bstack1l1ll1lll1_opy_ = None
bstack11l111l111_opy_ = -1
bstack111ll11l1l_opy_ = os.path.join(os.path.expanduser(bstack11l11_opy_ (u"࠭ࡾࠨࣆ")), bstack11l11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧࣇ"), bstack11l11_opy_ (u"ࠨ࠰ࡵࡳࡧࡵࡴ࠮ࡴࡨࡴࡴࡸࡴ࠮ࡪࡨࡰࡵ࡫ࡲ࠯࡬ࡶࡳࡳ࠭ࣈ"))
bstack11ll1ll1l1_opy_ = 0
bstack111ll1111_opy_ = 0
bstack11l1lll1_opy_ = []
bstack1l11l1l11l_opy_ = []
ROBOT_PYTHON_ERRORS = []
bstack1lll11ll1l_opy_ = []
bstack1l1111l11_opy_ = bstack11l11_opy_ (u"ࠩࠪࣉ")
bstack1llll11l1l_opy_ = bstack11l11_opy_ (u"ࠪࠫ࣊")
bstack1llllllll1_opy_ = False
bstack1lll111ll_opy_ = False
bstack11l11lll1l_opy_ = {}
bstack11ll1l11l_opy_ = {}
bstack11l111111_opy_ = None
bstack11l111l1ll_opy_ = None
bstack111ll1lll1_opy_ = None
bstack11ll1l1l1_opy_ = None
bstack1llll1ll_opy_ = None
bstack1ll1ll1l1l_opy_ = None
bstack11ll1l1111_opy_ = None
bstack111llll11l_opy_ = None
bstack11l1l1ll_opy_ = None
bstack111l1l111_opy_ = None
bstack1l1l1ll1ll_opy_ = None
bstack111lllllll_opy_ = None
bstack1l1111l1ll_opy_ = None
bstack11ll11ll_opy_ = None
bstack1ll1111l1l_opy_ = None
bstack1l111l1ll1_opy_ = None
bstack1ll111111l_opy_ = None
bstack11l1ll1l1_opy_ = None
bstack11l1ll11l1_opy_ = None
bstack1lll111l_opy_ = None
bstack11l111l1l1_opy_ = None
bstack11llllll11_opy_ = None
bstack1111l1l11_opy_ = None
thread_local = threading.local()
bstack1l1l1ll111_opy_ = False
bstack1llll1ll1l_opy_ = bstack11l11_opy_ (u"ࠦࠧ࣋")
logger = logger_utils.get_logger(__name__, bstack1l1ll1llll_opy_)
bstack111111l11_opy_ = logger_utils.bstack11llll1l11_opy_(__name__)
bstack11l1l1111_opy_ = Config.bstack111l1lll_opy_()
percy = bstack11l11ll11_opy_()
bstack1lll11ll_opy_ = bstack111lll111_opy_()
bstack1l111llll_opy_ = bstack11llll11_opy_()
def bstack1lll1lll1_opy_():
  global CONFIG
  global bstack1llllllll1_opy_
  global bstack11l1l1111_opy_
  testContextOptions = bstack1l1ll11lll_opy_(CONFIG)
  if bstack1ll111l11_opy_(CONFIG):
    if (bstack11l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ࣌") in testContextOptions and str(testContextOptions[bstack11l11_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ࣍")]).lower() == bstack11l11_opy_ (u"ࠧࡵࡴࡸࡩࠬ࣎")):
      bstack1llllllll1_opy_ = True
      bstack11l1l1111_opy_.bstack11l111lll_opy_(True)
    bstack11l1l1111_opy_.bstack1ll1l11ll1_opy_(testContextOptions.get(bstack11l11_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷ࣏ࠬ"), False))
  else:
    bstack1llllllll1_opy_ = True
    bstack11l1l1111_opy_.bstack11l111lll_opy_(True)
    bstack11l1l1111_opy_.bstack1ll1l11ll1_opy_(True)
def bstack1l1l11111_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack111l1lll1_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack111l11ll_opy_():
  global bstack11ll1l11l_opy_
  args = sys.argv
  for i in range(len(args)):
    if bstack11l11_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡦࡳࡳ࡬ࡩࡨࡨ࡬ࡰࡪࠨ࣐") == args[i].lower() or bstack11l11_opy_ (u"ࠥ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡮ࡧ࡫ࡪ࣑ࠦ") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      bstack11ll1l11l_opy_[bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ࣒")] = path
      return path
  return None
bstack1lll11l1ll_opy_ = re.compile(bstack11l11_opy_ (u"ࡷࠨ࠮ࠫࡁ࡟ࠨࢀ࠮࠮ࠫࡁࠬࢁ࠳࠰࠿࣓ࠣ"))
def bstack111ll1l11l_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1lll11l1ll_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack11l11_opy_ (u"ࠨࠤࡼࠤࣔ") + group + bstack11l11_opy_ (u"ࠢࡾࠤࣕ"), os.environ.get(group))
  return value
def bstack11ll11l1l_opy_():
  global bstack1111l1l11_opy_
  if bstack1111l1l11_opy_ is None:
        bstack1111l1l11_opy_ = bstack111l11ll_opy_()
  bstack1ll1l1lll_opy_ = bstack1111l1l11_opy_
  if bstack1ll1l1lll_opy_ and os.path.exists(os.path.abspath(bstack1ll1l1lll_opy_)):
    fileName = bstack1ll1l1lll_opy_
  if bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬࣖ") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࡠࡈࡌࡐࡊ࠭ࣗ")])) and not bstack11l11_opy_ (u"ࠪࡪ࡮ࡲࡥࡏࡣࡰࡩࠬࣘ") in locals():
    fileName = os.environ[bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨࣙ")]
  if bstack11l11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡑࡥࡲ࡫ࠧࣚ") in locals():
    bstack1111l1_opy_ = os.path.abspath(fileName)
  else:
    bstack1111l1_opy_ = bstack11l11_opy_ (u"࠭ࠧࣛ")
  bstack1ll1111lll_opy_ = os.getcwd()
  bstack1ll11ll1ll_opy_ = bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪࣜ")
  bstack111lllll1_opy_ = bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺࡣࡰࡰࠬࣝ")
  while (not os.path.exists(bstack1111l1_opy_)) and bstack1ll1111lll_opy_ != bstack11l11_opy_ (u"ࠤࠥࣞ"):
    bstack1111l1_opy_ = os.path.join(bstack1ll1111lll_opy_, bstack1ll11ll1ll_opy_)
    if not os.path.exists(bstack1111l1_opy_):
      bstack1111l1_opy_ = os.path.join(bstack1ll1111lll_opy_, bstack111lllll1_opy_)
    if bstack1ll1111lll_opy_ != os.path.dirname(bstack1ll1111lll_opy_):
      bstack1ll1111lll_opy_ = os.path.dirname(bstack1ll1111lll_opy_)
    else:
      bstack1ll1111lll_opy_ = bstack11l11_opy_ (u"ࠥࠦࣟ")
  bstack1111l1l11_opy_ = bstack1111l1_opy_ if os.path.exists(bstack1111l1_opy_) else None
  return bstack1111l1l11_opy_
def bstack111l11ll11_opy_(config):
    if bstack11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࠫ࣠") in config:
      config[bstack11l11_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ࣡")] = config[bstack11l11_opy_ (u"࠭ࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬࠭࣢")]
    if bstack11l11_opy_ (u"ࠧࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭ࡏࡱࡶ࡬ࡳࡳࡹࣣࠧ") in config:
      config[bstack11l11_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬࣤ")] = config[bstack11l11_opy_ (u"ࠩࡷࡩࡸࡺࡒࡦࡲࡲࡶࡹ࡯࡮ࡨࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣥ")]
def bstack11l1ll11ll_opy_():
  bstack1111l1_opy_ = bstack11ll11l1l_opy_()
  if not os.path.exists(bstack1111l1_opy_):
    bstack1l1lll1111_opy_(
      bstack1ll111l11l_opy_.format(os.getcwd()))
  try:
    with open(bstack1111l1_opy_, bstack11l11_opy_ (u"ࠪࡶࣦࠬ")) as stream:
      yaml.add_implicit_resolver(bstack11l11_opy_ (u"ࠦࠦࡶࡡࡵࡪࡨࡼࠧࣧ"), bstack1lll11l1ll_opy_)
      yaml.add_constructor(bstack11l11_opy_ (u"ࠧࠧࡰࡢࡶ࡫ࡩࡽࠨࣨ"), bstack111ll1l11l_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      bstack111l11ll11_opy_(config)
      return config
  except:
    with open(bstack1111l1_opy_, bstack11l11_opy_ (u"࠭ࡲࠨࣩ")) as stream:
      try:
        config = yaml.safe_load(stream)
        bstack111l11ll11_opy_(config)
        return config
      except yaml.YAMLError as exc:
        bstack1l1lll1111_opy_(bstack1111ll1lll_opy_.format(str(exc)))
def bstack1l1l11lll1_opy_(config):
  bstack111l1111_opy_ = bstack1111l1l1l_opy_(config)
  for option in list(bstack111l1111_opy_):
    if option.lower() in bstack1111lll1ll_opy_ and option != bstack1111lll1ll_opy_[option.lower()]:
      bstack111l1111_opy_[bstack1111lll1ll_opy_[option.lower()]] = bstack111l1111_opy_[option]
      del bstack111l1111_opy_[option]
  return config
def bstack1llllll1l_opy_():
  global bstack1lllll1l11_opy_
  for key, bstack1l1l1l1l11_opy_ in bstack1l11l11l1l_opy_.items():
    if isinstance(bstack1l1l1l1l11_opy_, list):
      for var in bstack1l1l1l1l11_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1lllll1l11_opy_[key] = os.environ[var]
          break
    elif bstack1l1l1l1l11_opy_ in os.environ and os.environ[bstack1l1l1l1l11_opy_] and str(os.environ[bstack1l1l1l1l11_opy_]).strip():
      bstack1lllll1l11_opy_[key] = os.environ[bstack1l1l1l1l11_opy_]
  if bstack11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩ࣪") in os.environ:
    bstack1lllll1l11_opy_[bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ࣫")] = {}
    bstack1lllll1l11_opy_[bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭࣬")][bstack11l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ࣭ࠬ")] = os.environ[bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࣮࠭")]
def bstack1l1l111lll_opy_():
  global bstack11ll11lll1_opy_
  global bstack111lll11_opy_
  global bstack11ll1l11l_opy_
  bstack111l1l1ll_opy_ = []
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) - 1 and bstack11l11_opy_ (u"ࠬ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ࣯").lower() == val.lower():
      bstack11ll11lll1_opy_[bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࣰࠪ")] = {}
      bstack11ll11lll1_opy_[bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࣱࠫ")][bstack11l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࣲࠪ")] = sys.argv[idx + 1]
      bstack111l1l1ll_opy_.extend([idx, idx + 1])
      break
  for key, bstack1lll1l11l1_opy_ in bstack1ll11llll1_opy_.items():
    if isinstance(bstack1lll1l11l1_opy_, list):
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        for var in bstack1lll1l11l1_opy_:
          if bstack11l11_opy_ (u"ࠩ࠰࠱ࠬࣳ") + var.lower() == val.lower() and key not in bstack11ll11lll1_opy_:
            bstack11ll11lll1_opy_[key] = sys.argv[idx + 1]
            bstack111lll11_opy_ += bstack11l11_opy_ (u"ࠪࠤ࠲࠳ࠧࣴ") + var + bstack11l11_opy_ (u"ࠫࠥ࠭ࣵ") + shlex.quote(sys.argv[idx + 1])
            bstack1l1l1111l1_opy_(bstack11ll1l11l_opy_, key, sys.argv[idx + 1])
            bstack111l1l1ll_opy_.extend([idx, idx + 1])
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        if bstack11l11_opy_ (u"ࠬ࠳࠭ࠨࣶ") + bstack1lll1l11l1_opy_.lower() == val.lower() and key not in bstack11ll11lll1_opy_:
          bstack11ll11lll1_opy_[key] = sys.argv[idx + 1]
          bstack111lll11_opy_ += bstack11l11_opy_ (u"࠭ࠠ࠮࠯ࠪࣷ") + bstack1lll1l11l1_opy_ + bstack11l11_opy_ (u"ࠧࠡࠩࣸ") + shlex.quote(sys.argv[idx + 1])
          bstack1l1l1111l1_opy_(bstack11ll1l11l_opy_, key, sys.argv[idx + 1])
          bstack111l1l1ll_opy_.extend([idx, idx + 1])
  for idx in sorted(set(bstack111l1l1ll_opy_), reverse=True):
    if idx < len(sys.argv):
      del sys.argv[idx]
def bstack11llll11ll_opy_(config):
  bstack1ll1lll1ll_opy_ = config.keys()
  for bstack11l11l1111_opy_, bstack11l11l1l1_opy_ in bstack1l11111ll_opy_.items():
    if bstack11l11l1l1_opy_ in bstack1ll1lll1ll_opy_:
      config[bstack11l11l1111_opy_] = config[bstack11l11l1l1_opy_]
      del config[bstack11l11l1l1_opy_]
  for bstack11l11l1111_opy_, bstack11l11l1l1_opy_ in bstack1lllll1ll1_opy_.items():
    if isinstance(bstack11l11l1l1_opy_, list):
      for bstack1ll11l11l_opy_ in bstack11l11l1l1_opy_:
        if bstack1ll11l11l_opy_ in bstack1ll1lll1ll_opy_:
          config[bstack11l11l1111_opy_] = config[bstack1ll11l11l_opy_]
          del config[bstack1ll11l11l_opy_]
          break
    elif bstack11l11l1l1_opy_ in bstack1ll1lll1ll_opy_:
      config[bstack11l11l1111_opy_] = config[bstack11l11l1l1_opy_]
      del config[bstack11l11l1l1_opy_]
  for bstack1ll11l11l_opy_ in list(config):
    for bstack1ll111l111_opy_ in bstack1l11lll1_opy_:
      if bstack1ll11l11l_opy_.lower() == bstack1ll111l111_opy_.lower() and bstack1ll11l11l_opy_ != bstack1ll111l111_opy_:
        config[bstack1ll111l111_opy_] = config[bstack1ll11l11l_opy_]
        del config[bstack1ll11l11l_opy_]
  bstack111111ll1_opy_ = [{}]
  if not config.get(bstack11l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࣹࠫ")):
    config[bstack11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࣺࠬ")] = [{}]
  bstack111111ll1_opy_ = config[bstack11l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣻ")]
  for platform in bstack111111ll1_opy_:
    for bstack1ll11l11l_opy_ in list(platform):
      for bstack1ll111l111_opy_ in bstack1l11lll1_opy_:
        if bstack1ll11l11l_opy_.lower() == bstack1ll111l111_opy_.lower() and bstack1ll11l11l_opy_ != bstack1ll111l111_opy_:
          platform[bstack1ll111l111_opy_] = platform[bstack1ll11l11l_opy_]
          del platform[bstack1ll11l11l_opy_]
  for bstack11l11l1111_opy_, bstack11l11l1l1_opy_ in bstack1lllll1ll1_opy_.items():
    for platform in bstack111111ll1_opy_:
      if isinstance(bstack11l11l1l1_opy_, list):
        for bstack1ll11l11l_opy_ in bstack11l11l1l1_opy_:
          if bstack1ll11l11l_opy_ in platform:
            platform[bstack11l11l1111_opy_] = platform[bstack1ll11l11l_opy_]
            del platform[bstack1ll11l11l_opy_]
            break
      elif bstack11l11l1l1_opy_ in platform:
        platform[bstack11l11l1111_opy_] = platform[bstack11l11l1l1_opy_]
        del platform[bstack11l11l1l1_opy_]
  for bstack111lll11l_opy_ in bstack11ll1l11l1_opy_:
    if bstack111lll11l_opy_ in config:
      if not bstack11ll1l11l1_opy_[bstack111lll11l_opy_] in config:
        config[bstack11ll1l11l1_opy_[bstack111lll11l_opy_]] = {}
      config[bstack11ll1l11l1_opy_[bstack111lll11l_opy_]].update(config[bstack111lll11l_opy_])
      del config[bstack111lll11l_opy_]
  for platform in bstack111111ll1_opy_:
    for bstack111lll11l_opy_ in bstack11ll1l11l1_opy_:
      if bstack111lll11l_opy_ in list(platform):
        if not bstack11ll1l11l1_opy_[bstack111lll11l_opy_] in platform:
          platform[bstack11ll1l11l1_opy_[bstack111lll11l_opy_]] = {}
        platform[bstack11ll1l11l1_opy_[bstack111lll11l_opy_]].update(platform[bstack111lll11l_opy_])
        del platform[bstack111lll11l_opy_]
  config = bstack1l1l11lll1_opy_(config)
  return config
def bstack11l1lllll_opy_(config):
  global bstack1l1lll1l11_opy_
  bstack1l111l11_opy_ = False
  if bstack11l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨࣼ") in config and str(config[bstack11l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩࣽ")]).lower() != bstack11l11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬࣾ"):
    if bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫࣿ") not in config or str(config[bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬऀ")]).lower() == bstack11l11_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨँ"):
      config[bstack11l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩं")] = False
    else:
      bstack1ll1ll1ll1_opy_ = bstack11l11l11l_opy_()
      if bstack11l11_opy_ (u"ࠫ࡮ࡹࡔࡳ࡫ࡤࡰࡌࡸࡩࡥࠩः") in bstack1ll1ll1ll1_opy_:
        if not bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩऄ") in config:
          config[bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪअ")] = {}
        config[bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫआ")][bstack11l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪइ")] = bstack11l11_opy_ (u"ࠩࡤࡸࡸ࠳ࡲࡦࡲࡨࡥࡹ࡫ࡲࠨई")
        bstack1l111l11_opy_ = True
        bstack1l1lll1l11_opy_ = config[bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧउ")].get(bstack11l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ऊ"))
  if bstack1ll111l11_opy_(config) and bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩऋ") in config and str(config[bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪऌ")]).lower() != bstack11l11_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ऍ") and not bstack1l111l11_opy_:
    if not bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬऎ") in config:
      config[bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ए")] = {}
    if not config[bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧऐ")].get(bstack11l11_opy_ (u"ࠫࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠨऑ")) and not bstack11l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऒ") in config[bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪओ")]:
      bstack11l1lll11_opy_ = datetime.datetime.now()
      bstack1ll11lll1_opy_ = bstack11l1lll11_opy_.strftime(bstack11l11_opy_ (u"ࠧࠦࡦࡢࠩࡧࡥࠥࡉࠧࡐࠫऔ"))
      hostname = socket.gethostname()
      bstack1lll1l1111_opy_ = bstack11l11_opy_ (u"ࠨࠩक").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack11l11_opy_ (u"ࠩࡾࢁࡤࢁࡽࡠࡽࢀࠫख").format(bstack1ll11lll1_opy_, hostname, bstack1lll1l1111_opy_)
      config[bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧग")][bstack11l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭घ")] = identifier
    bstack1l1lll1l11_opy_ = config[bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩङ")].get(bstack11l11_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨच"))
  return config
def bstack1l1lll11l1_opy_():
  bstack11llll111_opy_ =  bstack11l1lllll1_opy_()[bstack11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷ࠭छ")]
  return bstack11llll111_opy_ if bstack11llll111_opy_ else -1
def bstack11lll1ll1l_opy_(bstack11llll111_opy_):
  global CONFIG
  if not bstack11l11_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪज") in CONFIG[bstack11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫझ")]:
    return
  CONFIG[bstack11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬञ")] = CONFIG[bstack11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ट")].replace(
    bstack11l11_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧठ"),
    str(bstack11llll111_opy_)
  )
def bstack11ll11l11l_opy_():
  global CONFIG
  if not bstack11l11_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬड") in CONFIG[bstack11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩढ")]:
    return
  bstack11l1lll11_opy_ = datetime.datetime.now()
  bstack1ll11lll1_opy_ = bstack11l1lll11_opy_.strftime(bstack11l11_opy_ (u"ࠨࠧࡧ࠱ࠪࡨ࠭ࠦࡊ࠽ࠩࡒ࠭ण"))
  CONFIG[bstack11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫत")] = CONFIG[bstack11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬथ")].replace(
    bstack11l11_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪद"),
    bstack1ll11lll1_opy_
  )
def bstack111lll1ll1_opy_():
  global CONFIG
  if bstack11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧध") in CONFIG and not bool(CONFIG[bstack11l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨन")]):
    del CONFIG[bstack11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऩ")]
    return
  if not bstack11l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪप") in CONFIG:
    CONFIG[bstack11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫफ")] = bstack11l11_opy_ (u"ࠪࠧࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ब")
  if bstack11l11_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪभ") in CONFIG[bstack11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧम")]:
    bstack11ll11l11l_opy_()
    os.environ[bstack11l11_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪय")] = CONFIG[bstack11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩर")]
  if not bstack11l11_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪऱ") in CONFIG[bstack11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫल")]:
    return
  bstack11llll111_opy_ = bstack11l11_opy_ (u"ࠪࠫळ")
  bstack111lll11ll_opy_ = bstack1l1lll11l1_opy_()
  if bstack111lll11ll_opy_ != -1:
    bstack11llll111_opy_ = bstack11l11_opy_ (u"ࠫࡈࡏࠠࠨऴ") + str(bstack111lll11ll_opy_)
  if bstack11llll111_opy_ == bstack11l11_opy_ (u"ࠬ࠭व"):
    bstack1l1ll111ll_opy_ = bstack1lll1l11l_opy_(CONFIG[bstack11l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩश")])
    if bstack1l1ll111ll_opy_ != -1:
      bstack11llll111_opy_ = str(bstack1l1ll111ll_opy_)
  if bstack11llll111_opy_:
    bstack11lll1ll1l_opy_(bstack11llll111_opy_)
    os.environ[bstack11l11_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫष")] = CONFIG[bstack11l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪस")]
def bstack1lll1111_opy_(bstack111llllll1_opy_, bstack1lll11l111_opy_, path):
  bstack11l1l11l_opy_ = {
    bstack11l11_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ह"): bstack1lll11l111_opy_
  }
  if os.path.exists(path):
    bstack1l1ll1l1_opy_ = json.load(open(path, bstack11l11_opy_ (u"ࠪࡶࡧ࠭ऺ")))
  else:
    bstack1l1ll1l1_opy_ = {}
  bstack1l1ll1l1_opy_[bstack111llllll1_opy_] = bstack11l1l11l_opy_
  with open(path, bstack11l11_opy_ (u"ࠦࡼ࠱ࠢऻ")) as outfile:
    json.dump(bstack1l1ll1l1_opy_, outfile)
def bstack1lll1l11l_opy_(bstack111llllll1_opy_):
  bstack111llllll1_opy_ = str(bstack111llllll1_opy_)
  bstack1l1llll1l1_opy_ = os.path.join(os.path.expanduser(bstack11l11_opy_ (u"ࠬࢄ़ࠧ")), bstack11l11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ऽ"))
  try:
    if not os.path.exists(bstack1l1llll1l1_opy_):
      os.makedirs(bstack1l1llll1l1_opy_)
    file_path = os.path.join(os.path.expanduser(bstack11l11_opy_ (u"ࠧࡿࠩा")), bstack11l11_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨि"), bstack11l11_opy_ (u"ࠩ࠱ࡦࡺ࡯࡬ࡥ࠯ࡱࡥࡲ࡫࠭ࡤࡣࡦ࡬ࡪ࠴ࡪࡴࡱࡱࠫी"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack11l11_opy_ (u"ࠪࡻࠬु")):
        pass
      with open(file_path, bstack11l11_opy_ (u"ࠦࡼ࠱ࠢू")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack11l11_opy_ (u"ࠬࡸࠧृ")) as bstack1ll1l1ll1l_opy_:
      bstack1lll1l1lll_opy_ = json.load(bstack1ll1l1ll1l_opy_)
    if bstack111llllll1_opy_ in bstack1lll1l1lll_opy_:
      bstack1l1l1l1l_opy_ = bstack1lll1l1lll_opy_[bstack111llllll1_opy_][bstack11l11_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪॄ")]
      bstack1llll1l1l1_opy_ = int(bstack1l1l1l1l_opy_) + 1
      bstack1lll1111_opy_(bstack111llllll1_opy_, bstack1llll1l1l1_opy_, file_path)
      return bstack1llll1l1l1_opy_
    else:
      bstack1lll1111_opy_(bstack111llllll1_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warning(bstack1l111ll11l_opy_.format(str(e)))
    return -1
def bstack1l11l1ll11_opy_(config):
  if not config[bstack11l11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩॅ")] or not config[bstack11l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫॆ")]:
    return True
  else:
    return False
def bstack11llll1ll_opy_(config, index=0):
  global bstack11lll1l11_opy_
  bstack1ll1llllll_opy_ = {}
  caps = bstack1l1lllllll_opy_ + bstack1llll1l1_opy_
  if config.get(bstack11l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭े"), False):
    bstack1ll1llllll_opy_[bstack11l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧै")] = True
    bstack1ll1llllll_opy_[bstack11l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࡐࡲࡷ࡭ࡴࡴࡳࠨॉ")] = config.get(bstack11l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩॊ"), {})
  if bstack11lll1l11_opy_:
    caps += bstack1llll1l11_opy_
  for key in config:
    if key in caps + [bstack11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩो")]:
      continue
    bstack1ll1llllll_opy_[key] = config[key]
  if bstack11l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪौ") in config:
    for bstack11lll11l1_opy_ in config[bstack11l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶ्ࠫ")][index]:
      if bstack11lll11l1_opy_ in caps:
        continue
      bstack1ll1llllll_opy_[bstack11lll11l1_opy_] = config[bstack11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॎ")][index][bstack11lll11l1_opy_]
  bstack1ll1llllll_opy_[bstack11l11_opy_ (u"ࠪ࡬ࡴࡹࡴࡏࡣࡰࡩࠬॏ")] = socket.gethostname()
  if bstack11l11_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬॐ") in bstack1ll1llllll_opy_:
    del (bstack1ll1llllll_opy_[bstack11l11_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭॑")])
  return bstack1ll1llllll_opy_
def bstack1111l11ll_opy_(config):
  global bstack11lll1l11_opy_
  bstack1ll1l1111_opy_ = {}
  caps = bstack1llll1l1_opy_
  if bstack11lll1l11_opy_:
    caps += bstack1llll1l11_opy_
  for key in caps:
    if key in config:
      bstack1ll1l1111_opy_[key] = config[key]
  return bstack1ll1l1111_opy_
def bstack1l1ll1ll1_opy_(bstack1ll1llllll_opy_, bstack1ll1l1111_opy_):
  bstack1l11l1l1l_opy_ = {}
  for key in bstack1ll1llllll_opy_.keys():
    if key in bstack1l11111ll_opy_:
      bstack1l11l1l1l_opy_[bstack1l11111ll_opy_[key]] = bstack1ll1llllll_opy_[key]
    else:
      bstack1l11l1l1l_opy_[key] = bstack1ll1llllll_opy_[key]
  for key in bstack1ll1l1111_opy_:
    if key in bstack1l11111ll_opy_:
      bstack1l11l1l1l_opy_[bstack1l11111ll_opy_[key]] = bstack1ll1l1111_opy_[key]
    else:
      bstack1l11l1l1l_opy_[key] = bstack1ll1l1111_opy_[key]
  return bstack1l11l1l1l_opy_
def bstack1lll111l1_opy_(config, index=0):
  global bstack11lll1l11_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack11ll1111ll_opy_ = bstack11l1l1llll_opy_(bstack1llll11l_opy_, config, logger)
  bstack1ll1l1111_opy_ = bstack1111l11ll_opy_(config)
  bstack11l1l11111_opy_ = bstack1llll1l1_opy_
  bstack11l1l11111_opy_ += bstack1111llll11_opy_
  bstack1ll1l1111_opy_ = update(bstack1ll1l1111_opy_, bstack11ll1111ll_opy_)
  if bstack11lll1l11_opy_:
    bstack11l1l11111_opy_ += bstack1llll1l11_opy_
  if bstack11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴ॒ࠩ") in config:
    if bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ॓") in config[bstack11l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ॔")][index]:
      caps[bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧॕ")] = config[bstack11l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॖ")][index][bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩॗ")]
    if bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭क़") in config[bstack11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩख़")][index]:
      caps[bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨग़")] = str(config[bstack11l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫज़")][index][bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪड़")])
    bstack1l11l11lll_opy_ = bstack11l1l1llll_opy_(bstack1llll11l_opy_, config[bstack11l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ढ़")][index], logger)
    bstack11l1l11111_opy_ += list(bstack1l11l11lll_opy_.keys())
    for bstack1llll1lll_opy_ in bstack11l1l11111_opy_:
      if bstack1llll1lll_opy_ in config[bstack11l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧफ़")][index]:
        if bstack1llll1lll_opy_ == bstack11l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧय़"):
          try:
            bstack1l11l11lll_opy_[bstack1llll1lll_opy_] = str(config[bstack11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩॠ")][index][bstack1llll1lll_opy_] * 1.0)
          except:
            bstack1l11l11lll_opy_[bstack1llll1lll_opy_] = str(config[bstack11l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪॡ")][index][bstack1llll1lll_opy_])
        else:
          bstack1l11l11lll_opy_[bstack1llll1lll_opy_] = config[bstack11l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫॢ")][index][bstack1llll1lll_opy_]
        del (config[bstack11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॣ")][index][bstack1llll1lll_opy_])
    bstack1ll1l1111_opy_ = update(bstack1ll1l1111_opy_, bstack1l11l11lll_opy_)
  bstack1ll1llllll_opy_ = bstack11llll1ll_opy_(config, index)
  for bstack1ll11l11l_opy_ in bstack1llll1l1_opy_ + list(bstack11ll1111ll_opy_.keys()):
    if bstack1ll11l11l_opy_ in bstack1ll1llllll_opy_:
      bstack1ll1l1111_opy_[bstack1ll11l11l_opy_] = bstack1ll1llllll_opy_[bstack1ll11l11l_opy_]
      del (bstack1ll1llllll_opy_[bstack1ll11l11l_opy_])
  if bstack1l1l1llll_opy_(config):
    bstack1ll1llllll_opy_[bstack11l11_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ।")] = True
    caps.update(bstack1ll1l1111_opy_)
    caps[bstack11l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ॥")] = bstack1ll1llllll_opy_
  else:
    bstack1ll1llllll_opy_[bstack11l11_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ०")] = False
    caps.update(bstack1l1ll1ll1_opy_(bstack1ll1llllll_opy_, bstack1ll1l1111_opy_))
    if bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ१") in caps:
      caps[bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ२")] = caps[bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭३")]
      del (caps[bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ४")])
    if bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ५") in caps:
      caps[bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭६")] = caps[bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭७")]
      del (caps[bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ८")])
  return caps
def bstack1l1llll1ll_opy_():
  global bstack1ll1l1l1ll_opy_
  global CONFIG
  if bstack1ll1l1l1ll_opy_ != bstack11l11_opy_ (u"ࠧࠨ९") and (bstack1ll1l1l1ll_opy_.startswith(bstack11l11_opy_ (u"ࠨࡪࡷࡸࡵࡀ࠯࠰ࠩ॰")) or bstack1ll1l1l1ll_opy_.startswith(bstack11l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠫॱ"))):
    return bstack1ll1l1l1ll_opy_
  if bstack111l1lll1_opy_() <= version.parse(bstack11l11_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪॲ")):
    if bstack1ll1l1l1ll_opy_ != bstack11l11_opy_ (u"ࠫࠬॳ"):
      return bstack11l11_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨॴ") + bstack1ll1l1l1ll_opy_ + bstack11l11_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥॵ")
    return bstack1l1111ll1_opy_
  if bstack1ll1l1l1ll_opy_ != bstack11l11_opy_ (u"ࠧࠨॶ"):
    return bstack11l11_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥॷ") + bstack1ll1l1l1ll_opy_ + bstack11l11_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥॸ")
  return bstack11l111l1_opy_
def bstack111lllll1l_opy_(options):
  return hasattr(options, bstack11l11_opy_ (u"ࠪࡷࡪࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠫॹ"))
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
def bstack111l11l1ll_opy_(options, bstack1l1l1l111_opy_):
  for bstack11lll1lll_opy_ in bstack1l1l1l111_opy_:
    if bstack11lll1lll_opy_ in [bstack11l11_opy_ (u"ࠫࡦࡸࡧࡴࠩॺ"), bstack11l11_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩॻ")]:
      continue
    if bstack11lll1lll_opy_ in options._experimental_options:
      options._experimental_options[bstack11lll1lll_opy_] = update(options._experimental_options[bstack11lll1lll_opy_],
                                                         bstack1l1l1l111_opy_[bstack11lll1lll_opy_])
    else:
      options.add_experimental_option(bstack11lll1lll_opy_, bstack1l1l1l111_opy_[bstack11lll1lll_opy_])
  if bstack11l11_opy_ (u"࠭ࡡࡳࡩࡶࠫॼ") in bstack1l1l1l111_opy_:
    for arg in bstack1l1l1l111_opy_[bstack11l11_opy_ (u"ࠧࡢࡴࡪࡷࠬॽ")]:
      options.add_argument(arg)
    del (bstack1l1l1l111_opy_[bstack11l11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ॾ")])
  if bstack11l11_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ॿ") in bstack1l1l1l111_opy_:
    for ext in bstack1l1l1l111_opy_[bstack11l11_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧঀ")]:
      try:
        options.add_extension(ext)
      except OSError:
        options.add_encoded_extension(ext)
    del (bstack1l1l1l111_opy_[bstack11l11_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨঁ")])
def bstack1ll11llll_opy_(options):
  bstack11l11_opy_ (u"ࠧࠨࠢࠋࠢࠣࡍࡳࡰࡥࡤࡶࠣࡨࡪ࡬ࡡࡶ࡮ࡷࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡴࡶࡴࡪࡱࡱࡷࠥ࡬࡯ࡳࠢ࡯ࡳࡦࡪࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡹ࡫ࡩࡳࠦ࡯ࡷࡧࡵࡶ࡮ࡪࡥࡍࡱࡤࡨ࡙࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡧࡱࡥࡧࡲࡥࡥ࠰ࠍࠤࠥࡊࡥࡧࡧࡱࡷ࡮ࡼࡥ࠻ࠢࡱࡩࡻ࡫ࡲࠡࡱࡹࡩࡷࡽࡲࡪࡶࡨࡷࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠࡢࡴࡪࡷ࠱ࠦ࡯࡯࡮ࡼࠤࡦࡪࡤࡴࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡳࡳ࡫ࡳ࠯ࠌࠣࠤࡘ࡯࡭ࡪ࡮ࡤࡶࠥࡺ࡯ࠡࡌࡤࡺࡦࠦࡓࡅࡍࠪࡷࠥࡕࡶࡦࡴࡵ࡭ࡩ࡫ࡌࡰࡣࡧࡘࡪࡹࡴࡪࡰࡪࡇ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࡋࡩࡱࡶࡥࡳ࠰ࠍࠤ࡚ࠥࡨࡪࡵࠣ࡭ࡸࠦࡡࠡࡹࡵࡥࡵࡶࡥࡳࠢࡤࡶࡴࡻ࡮ࡥࠢࡷ࡬ࡪࠦࡣࡦࡰࡷࡶࡦࡲࡩࡻࡧࡧࠤ࡭࡫࡬ࡱࡧࡵࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠥࠦࠧং")
  global CONFIG
  global bstack1ll11l1111_opy_
  try:
    if not bstack1ll11l1111_opy_ or not options:
      return options
    from bstack_utils.bstack11l111l11_opy_ import bstack111ll11ll1_opy_
    bstack1ll1l1ll11_opy_ = bstack111ll11ll1_opy_(options, bstack111111lll_opy_=bstack11l11_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࠨঃ"))
    if bstack1ll1l1ll11_opy_ > 0:
      logger.debug(bstack11l11_opy_ (u"ࠢࡍࡱࡤࡨࠥࡺࡥࡴࡶ࡬ࡲ࡬ࡀࠠࡂࡦࡧࡩࡩࠦࡻࡾࠢࡧࡩ࡫ࡧࡵ࡭ࡶࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠦࡦࡰࡴࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧࠥ঄").format(bstack1ll1l1ll11_opy_))
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡮ࡴࡪࡦࡥࡷࠤࡱࡵࡡࡥࠢࡷࡩࡸࡺࡩ࡯ࡩࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࢁࡽࠣঅ").format(e))
  return options
def bstack1l11ll1l1l_opy_(options, bstack1l11ll111l_opy_):
  if bstack11l11_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨআ") in bstack1l11ll111l_opy_:
    for bstack1ll1111l_opy_ in bstack1l11ll111l_opy_[bstack11l11_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩই")]:
      if bstack1ll1111l_opy_ in options._preferences:
        options._preferences[bstack1ll1111l_opy_] = update(options._preferences[bstack1ll1111l_opy_], bstack1l11ll111l_opy_[bstack11l11_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪঈ")][bstack1ll1111l_opy_])
      else:
        options.set_preference(bstack1ll1111l_opy_, bstack1l11ll111l_opy_[bstack11l11_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫউ")][bstack1ll1111l_opy_])
  if bstack11l11_opy_ (u"࠭ࡡࡳࡩࡶࠫঊ") in bstack1l11ll111l_opy_:
    for arg in bstack1l11ll111l_opy_[bstack11l11_opy_ (u"ࠧࡢࡴࡪࡷࠬঋ")]:
      options.add_argument(arg)
def bstack1lll1ll11l_opy_(options, bstack11llll1l1_opy_):
  if bstack11l11_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࠩঌ") in bstack11llll1l1_opy_:
    options.use_webview(bool(bstack11llll1l1_opy_[bstack11l11_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࠪ঍")]))
  bstack111l11l1ll_opy_(options, bstack11llll1l1_opy_)
def bstack111lll111l_opy_(options, bstack111lll1l_opy_):
  for bstack1111111l_opy_ in bstack111lll1l_opy_:
    if bstack1111111l_opy_ in [bstack11l11_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧ঎"), bstack11l11_opy_ (u"ࠫࡦࡸࡧࡴࠩএ")]:
      continue
    options.set_capability(bstack1111111l_opy_, bstack111lll1l_opy_[bstack1111111l_opy_])
  if bstack11l11_opy_ (u"ࠬࡧࡲࡨࡵࠪঐ") in bstack111lll1l_opy_:
    for arg in bstack111lll1l_opy_[bstack11l11_opy_ (u"࠭ࡡࡳࡩࡶࠫ঑")]:
      options.add_argument(arg)
  if bstack11l11_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫ঒") in bstack111lll1l_opy_:
    options.bstack1lll1ll111_opy_(bool(bstack111lll1l_opy_[bstack11l11_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬও")]))
def bstack111llllll_opy_(options, bstack1ll111llll_opy_):
  for bstack1l11l1111_opy_ in bstack1ll111llll_opy_:
    if bstack1l11l1111_opy_ in [bstack11l11_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ঔ"), bstack11l11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨক")]:
      continue
    options._options[bstack1l11l1111_opy_] = bstack1ll111llll_opy_[bstack1l11l1111_opy_]
  if bstack11l11_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨখ") in bstack1ll111llll_opy_:
    for bstack1llll11111_opy_ in bstack1ll111llll_opy_[bstack11l11_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩগ")]:
      options.bstack11lllllll1_opy_(
        bstack1llll11111_opy_, bstack1ll111llll_opy_[bstack11l11_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪঘ")][bstack1llll11111_opy_])
  if bstack11l11_opy_ (u"ࠧࡢࡴࡪࡷࠬঙ") in bstack1ll111llll_opy_:
    for arg in bstack1ll111llll_opy_[bstack11l11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭চ")]:
      options.add_argument(arg)
def bstack1l1ll111_opy_(options, caps):
  if not hasattr(options, bstack11l11_opy_ (u"ࠩࡎࡉ࡞࠭ছ")):
    return
  if options.KEY == bstack11l11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨজ"):
    options = bstack1lllll111l_opy_.bstack1l111l1l_opy_(bstack111l1ll1ll_opy_=options, config=CONFIG)
  if options.KEY == bstack11l11_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩঝ") and options.KEY in caps:
    bstack111l11l1ll_opy_(options, caps[bstack11l11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪঞ")])
  elif options.KEY == bstack11l11_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫট") and options.KEY in caps:
    bstack1l11ll1l1l_opy_(options, caps[bstack11l11_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬঠ")])
  elif options.KEY == bstack11l11_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩড") and options.KEY in caps:
    bstack111lll111l_opy_(options, caps[bstack11l11_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪঢ")])
  elif options.KEY == bstack11l11_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫণ") and options.KEY in caps:
    bstack1lll1ll11l_opy_(options, caps[bstack11l11_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬত")])
  elif options.KEY == bstack11l11_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫথ") and options.KEY in caps:
    bstack111llllll_opy_(options, caps[bstack11l11_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬদ")])
def bstack1111ll1ll1_opy_(caps):
  global bstack11lll1l11_opy_
  if isinstance(os.environ.get(bstack11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨধ")), str):
    bstack11lll1l11_opy_ = eval(os.getenv(bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩন")))
  if bstack11lll1l11_opy_:
    if bstack1l1l11111_opy_() < version.parse(bstack11l11_opy_ (u"ࠩ࠵࠲࠸࠴࠰ࠨ঩")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack11l11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪপ")
    if bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩফ") in caps:
      browser = caps[bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪব")]
    elif bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧভ") in caps:
      browser = caps[bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨম")]
    browser = str(browser).lower()
    if browser == bstack11l11_opy_ (u"ࠨ࡫ࡳ࡬ࡴࡴࡥࠨয") or browser == bstack11l11_opy_ (u"ࠩ࡬ࡴࡦࡪࠧর"):
      browser = bstack11l11_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪ঱")
    if browser == bstack11l11_opy_ (u"ࠫࡸࡧ࡭ࡴࡷࡱ࡫ࠬল"):
      browser = bstack11l11_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬ঳")
    if browser not in [bstack11l11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭঴"), bstack11l11_opy_ (u"ࠧࡦࡦࡪࡩࠬ঵"), bstack11l11_opy_ (u"ࠨ࡫ࡨࠫশ"), bstack11l11_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩষ"), bstack11l11_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫস")]:
      return None
    try:
      package = bstack11l11_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳ࠰ࡾࢁ࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭হ").format(browser)
      name = bstack11l11_opy_ (u"ࠬࡕࡰࡵ࡫ࡲࡲࡸ࠭঺")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack111lllll1l_opy_(options):
        return None
      for bstack1ll11l11l_opy_ in caps.keys():
        options.set_capability(bstack1ll11l11l_opy_, caps[bstack1ll11l11l_opy_])
      bstack1l1ll111_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1ll1lllll_opy_(options, bstack11ll1ll1_opy_):
  if not bstack111lllll1l_opy_(options):
    return
  for bstack1ll11l11l_opy_ in bstack11ll1ll1_opy_.keys():
    if bstack1ll11l11l_opy_ in bstack1111llll11_opy_:
      continue
    if bstack1ll11l11l_opy_ in options._caps and type(options._caps[bstack1ll11l11l_opy_]) in [dict, list]:
      options._caps[bstack1ll11l11l_opy_] = update(options._caps[bstack1ll11l11l_opy_], bstack11ll1ll1_opy_[bstack1ll11l11l_opy_])
    else:
      options.set_capability(bstack1ll11l11l_opy_, bstack11ll1ll1_opy_[bstack1ll11l11l_opy_])
  bstack1l1ll111_opy_(options, bstack11ll1ll1_opy_)
  if bstack11l11_opy_ (u"࠭࡭ࡰࡼ࠽ࡨࡪࡨࡵࡨࡩࡨࡶࡆࡪࡤࡳࡧࡶࡷࠬ঻") in options._caps:
    if options._caps[bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩ়ࠬ")] and options._caps[bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ঽ")].lower() != bstack11l11_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪা"):
      del options._caps[bstack11l11_opy_ (u"ࠪࡱࡴࢀ࠺ࡥࡧࡥࡹ࡬࡭ࡥࡳࡃࡧࡨࡷ࡫ࡳࡴࠩি")]
def bstack1111lll1l_opy_(proxy_config):
  if bstack11l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨী") in proxy_config:
    proxy_config[bstack11l11_opy_ (u"ࠬࡹࡳ࡭ࡒࡵࡳࡽࡿࠧু")] = proxy_config[bstack11l11_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪূ")]
    del (proxy_config[bstack11l11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫৃ")])
  if bstack11l11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫৄ") in proxy_config and proxy_config[bstack11l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬ৅")].lower() != bstack11l11_opy_ (u"ࠪࡨ࡮ࡸࡥࡤࡶࠪ৆"):
    proxy_config[bstack11l11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧে")] = bstack11l11_opy_ (u"ࠬࡳࡡ࡯ࡷࡤࡰࠬৈ")
  if bstack11l11_opy_ (u"࠭ࡰࡳࡱࡻࡽࡆࡻࡴࡰࡥࡲࡲ࡫࡯ࡧࡖࡴ࡯ࠫ৉") in proxy_config:
    proxy_config[bstack11l11_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪ৊")] = bstack11l11_opy_ (u"ࠨࡲࡤࡧࠬো")
  return proxy_config
def bstack1l11l1lll_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack11l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨৌ") in config:
    return proxy
  config[bstack11l11_opy_ (u"ࠪࡴࡷࡵࡸࡺ্ࠩ")] = bstack1111lll1l_opy_(config[bstack11l11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪৎ")])
  if proxy == None:
    proxy = Proxy(config[bstack11l11_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ৏")])
  return proxy
def bstack1l11ll1l1_opy_(self):
  global CONFIG
  global bstack111lllllll_opy_
  try:
    proxy = bstack111l11l11_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack11l11_opy_ (u"࠭࠮ࡱࡣࡦࠫ৐")):
        proxies = bstack11l11l1ll1_opy_(proxy, bstack1l1llll1ll_opy_())
        if len(proxies) > 0:
          protocol, bstack1111ll11_opy_ = proxies.popitem()
          if bstack11l11_opy_ (u"ࠢ࠻࠱࠲ࠦ৑") in bstack1111ll11_opy_:
            return bstack1111ll11_opy_
          else:
            return bstack11l11_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ৒") + bstack1111ll11_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack11l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡶࡲࡰࡺࡼࠤࡺࡸ࡬ࠡ࠼ࠣࡿࢂࠨ৓").format(str(e)))
  return bstack111lllllll_opy_(self)
def bstack1lll1ll11_opy_():
  global CONFIG
  return bstack1l1l11l11l_opy_(CONFIG) and bstack1l1l1l1lll_opy_() and bstack111l1lll1_opy_() >= version.parse(bstack11ll111ll1_opy_)
def bstack111lllll_opy_():
  global CONFIG
  return (bstack11l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭৔") in CONFIG or bstack11l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ৕") in CONFIG) and bstack1l1lllll1_opy_()
def bstack1111l1l1l_opy_(config):
  bstack111l1111_opy_ = {}
  if bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ৖") in config:
    bstack111l1111_opy_ = config[bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪৗ")]
  if bstack11l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭৘") in config:
    bstack111l1111_opy_ = config[bstack11l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ৙")]
  proxy = bstack111l11l11_opy_(config)
  if proxy:
    if proxy.endswith(bstack11l11_opy_ (u"ࠩ࠱ࡴࡦࡩࠧ৚")) and os.path.isfile(proxy):
      bstack111l1111_opy_[bstack11l11_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭৛")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack11l11_opy_ (u"ࠫ࠳ࡶࡡࡤࠩড়")):
        proxies = bstack1llll1l111_opy_(config, bstack1l1llll1ll_opy_())
        if len(proxies) > 0:
          protocol, bstack1111ll11_opy_ = proxies.popitem()
          if bstack11l11_opy_ (u"ࠧࡀ࠯࠰ࠤঢ়") in bstack1111ll11_opy_:
            parsed_url = urlparse(bstack1111ll11_opy_)
          else:
            parsed_url = urlparse(protocol + bstack11l11_opy_ (u"ࠨ࠺࠰࠱ࠥ৞") + bstack1111ll11_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack111l1111_opy_[bstack11l11_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪয়")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack111l1111_opy_[bstack11l11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡰࡴࡷࠫৠ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack111l1111_opy_[bstack11l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬৡ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack111l1111_opy_[bstack11l11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭ৢ")] = str(parsed_url.password)
  return bstack111l1111_opy_
def bstack1l1ll11lll_opy_(config):
  if bstack11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩৣ") in config:
    return config[bstack11l11_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪ৤")]
  return {}
def bstack1l1111l111_opy_(caps):
  global bstack1l1lll1l11_opy_
  if bstack11l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ৥") in caps:
    caps[bstack11l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ০")][bstack11l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧ১")] = True
    if bstack1l1lll1l11_opy_:
      caps[bstack11l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ২")][bstack11l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ৩")] = bstack1l1lll1l11_opy_
  else:
    caps[bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩ৪")] = True
    if bstack1l1lll1l11_opy_:
      caps[bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭৫")] = bstack1l1lll1l11_opy_
@measure(event_name=EVENTS.bstack1l1111l11l_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l111l11l_opy_=bstack11l1111lll_opy_)
def bstack1l111lll1_opy_():
  global CONFIG
  if not bstack1ll111l11_opy_(CONFIG) or cli.is_enabled(CONFIG):
    return
  if bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ৬") in CONFIG and bstack1ll1l11lll_opy_(CONFIG[bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ৭")]):
    if (
      bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ৮") in CONFIG
      and bstack1ll1l11lll_opy_(CONFIG[bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭৯")].get(bstack11l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡃ࡫ࡱࡥࡷࡿࡉ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡣࡷ࡭ࡴࡴࠧৰ")))
    ):
      logger.debug(bstack11l11_opy_ (u"ࠦࡑࡵࡣࡢ࡮ࠣࡦ࡮ࡴࡡࡳࡻࠣࡲࡴࡺࠠࡴࡶࡤࡶࡹ࡫ࡤࠡࡣࡶࠤࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤࡪࡴࡡࡣ࡮ࡨࡨࠧৱ"))
      return
    bstack111l1111_opy_ = bstack1111l1l1l_opy_(CONFIG)
    bstack1111llllll_opy_(CONFIG[bstack11l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ৲")], bstack111l1111_opy_)
def bstack1111llllll_opy_(key, bstack111l1111_opy_):
  global bstack1l1l111ll_opy_
  logger.info(bstack1ll1l111_opy_)
  try:
    bstack1l1l111ll_opy_ = Local()
    bstack1lll11l1l_opy_ = {bstack11l11_opy_ (u"࠭࡫ࡦࡻࠪ৳"): key}
    bstack1lll11l1l_opy_.update(bstack111l1111_opy_)
    logger.debug(bstack1ll1111111_opy_.format(str(bstack1lll11l1l_opy_)).replace(key, bstack11l11_opy_ (u"ࠧ࡜ࡔࡈࡈࡆࡉࡔࡆࡆࡠࠫ৴")))
    bstack1l1l111ll_opy_.start(**bstack1lll11l1l_opy_)
    if bstack1l1l111ll_opy_.isRunning():
      logger.info(bstack111llll1l_opy_)
  except Exception as e:
    bstack1l1lll1111_opy_(bstack111l1111l_opy_.format(str(e)))
def bstack1l1ll1111l_opy_():
  global bstack1l1l111ll_opy_
  if bstack1l1l111ll_opy_.isRunning():
    logger.info(bstack11ll1lll1l_opy_)
    bstack1l1l111ll_opy_.stop()
  bstack1l1l111ll_opy_ = None
def bstack1l111l1lll_opy_(bstack11l111lll1_opy_=[]):
  global CONFIG
  bstack11lllll11l_opy_ = []
  bstack1l1l111l1l_opy_ = [bstack11l11_opy_ (u"ࠨࡱࡶࠫ৵"), bstack11l11_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬ৶"), bstack11l11_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧ৷"), bstack11l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭৸"), bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ৹"), bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ৺")]
  try:
    for err in bstack11l111lll1_opy_:
      bstack1llll11ll1_opy_ = {}
      for k in bstack1l1l111l1l_opy_:
        val = CONFIG[bstack11l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ৻")][int(err[bstack11l11_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧৼ")])].get(k)
        if val:
          bstack1llll11ll1_opy_[k] = val
      if(err[bstack11l11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ৽")] != bstack11l11_opy_ (u"ࠪࠫ৾")):
        bstack1llll11ll1_opy_[bstack11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡵࠪ৿")] = {
          err[bstack11l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ਀")]: err[bstack11l11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬਁ")]
        }
        bstack11lllll11l_opy_.append(bstack1llll11ll1_opy_)
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡳࡷࡳࡡࡵࡶ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺ࠺ࠡࠩਂ") + str(e))
  finally:
    return bstack11lllll11l_opy_
def bstack111ll11ll_opy_(file_name):
  bstack1l11l1lll1_opy_ = []
  try:
    bstack111ll1lll_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack111ll1lll_opy_):
      with open(bstack111ll1lll_opy_) as f:
        bstack111l11llll_opy_ = json.load(f)
        bstack1l11l1lll1_opy_ = bstack111l11llll_opy_
      os.remove(bstack111ll1lll_opy_)
    return bstack1l11l1lll1_opy_
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪ࡮ࡴࡤࡪࡰࡪࠤࡪࡸࡲࡰࡴࠣࡰ࡮ࡹࡴ࠻ࠢࠪਃ") + str(e))
    return bstack1l11l1lll1_opy_
def bstack111l111l_opy_():
  try:
      import time
      from bstack_utils.constants import bstack1l1l1l1l1_opy_, EVENTS
      from bstack_utils.helper import bstack1l11l11ll1_opy_, get_host_info, bstack11l1l1111_opy_
      from datetime import datetime
      from filelock import FileLock
      from bstack_utils.bstack11ll11ll1l_opy_ import bstack111l1lllll_opy_
      bstack111l1lllll_opy_.bstack1ll11ll111_opy_()
      bstack1lll1l1l_opy_ = os.path.join(os.getcwd(), bstack11l11_opy_ (u"ࠩ࡯ࡳ࡬࠭਄"), bstack11l11_opy_ (u"ࠪ࡯ࡪࡿ࠭࡮ࡧࡷࡶ࡮ࡩࡳ࠯࡬ࡶࡳࡳ࠭ਅ"))
      data = None
      lock = FileLock(bstack1lll1l1l_opy_+bstack11l11_opy_ (u"ࠦ࠳ࡲ࡯ࡤ࡭ࠥਆ"), timeout=2)
      try:
          with lock:
              with open(bstack1lll1l1l_opy_, bstack11l11_opy_ (u"ࠧࡸࠢਇ"), encoding=bstack11l11_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧਈ")) as file:
                  data = json.load(file)
      except Exception as e:
          logger.debug(bstack11l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡶࡪࡧࡤࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࠦࡦࡪ࡮ࡨ࠾ࠥࢁࡽࠣਉ").format(e))
          return
      if not data:
          return
      def bstack11l11lll_opy_():
          try:
              config = {
                  bstack11l11_opy_ (u"ࠣࡪࡨࡥࡩ࡫ࡲࡴࠤਊ"): {
                      bstack11l11_opy_ (u"ࠤࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠣ਋"): bstack11l11_opy_ (u"ࠥࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳࠨ਌"),
                  }
              }
              bstack11l11ll111_opy_ = datetime.utcnow()
              bstack11l1lll11_opy_ = bstack11l11ll111_opy_.strftime(bstack11l11_opy_ (u"ࠦࠪ࡟࠭ࠦ࡯࠰ࠩࡩ࡚ࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࠯ࠧࡩࠤ࡚࡚ࡃࠣ਍"))
              bstack1lllll11ll_opy_ = os.environ.get(bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ਎")) if os.environ.get(bstack11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫਏ")) else bstack11l1l1111_opy_.get_property(bstack11l11_opy_ (u"ࠢࡴࡦ࡮ࡖࡺࡴࡉࡥࠤਐ"))
              payload = {
                  bstack11l11_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠧ਑"): bstack11l11_opy_ (u"ࠤࡶࡨࡰࡥࡥࡷࡧࡱࡸࡸࠨ਒"),
                  bstack11l11_opy_ (u"ࠥࡨࡦࡺࡡࠣਓ"): {
                      bstack11l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡪࡸࡦࡤࡻࡵࡪࡦࠥਔ"): bstack1lllll11ll_opy_,
                      bstack11l11_opy_ (u"ࠧࡩࡲࡦࡣࡷࡩࡩࡥࡤࡢࡻࠥਕ"): bstack11l1lll11_opy_,
                      bstack11l11_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡴࡡ࡮ࡧࠥਖ"): bstack11l11_opy_ (u"ࠢࡔࡆࡎࡊࡪࡧࡴࡶࡴࡨࡔࡪࡸࡦࡰࡴࡰࡥࡳࡩࡥࠣਗ"),
                      bstack11l11_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟࡫ࡵࡲࡲࠧਘ"): {
                          bstack11l11_opy_ (u"ࠤࡰࡩࡦࡹࡵࡳࡧࡶࠦਙ"): data,
                          bstack11l11_opy_ (u"ࠥࡷࡩࡱࡒࡶࡰࡌࡨࠧਚ"): bstack11l1l1111_opy_.get_property(bstack11l11_opy_ (u"ࠦࡸࡪ࡫ࡓࡷࡱࡍࡩࠨਛ"))
                      },
                      bstack11l11_opy_ (u"ࠧࡻࡳࡦࡴࡢࡨࡦࡺࡡࠣਜ"): bstack11l1l1111_opy_.get_property(bstack11l11_opy_ (u"ࠨࡵࡴࡧࡵࡒࡦࡳࡥࠣਝ")),
                      bstack11l11_opy_ (u"ࠢࡩࡱࡶࡸࡤ࡯࡮ࡧࡱࠥਞ"): get_host_info()
                  }
              }
              bstack11111l11_opy_ = bstack1l11l1llll_opy_(cli.config, [bstack11l11_opy_ (u"ࠣࡣࡳ࡭ࡸࠨਟ"), bstack11l11_opy_ (u"ࠤࡨࡨࡸࡏ࡮ࡴࡶࡵࡹࡲ࡫࡮ࡵࡣࡷ࡭ࡴࡴࠢਠ"), bstack11l11_opy_ (u"ࠥࡥࡵ࡯ࠢਡ")], bstack1l1l1l1l1_opy_)
              response = bstack1l11l11ll1_opy_(bstack11l11_opy_ (u"ࠦࡕࡕࡓࡕࠤਢ"), bstack11111l11_opy_, payload, config)
              if response.status_code >= 200 and response.status_code < 300:
                  logger.info(bstack11l11_opy_ (u"ࠧࡑࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵࠣࡷࡪࡴࡴࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡵࡱࠣࡿࢂࠨਣ").format(bstack1l1l1l1l1_opy_))
              else:
                  logger.debug(bstack11l11_opy_ (u"ࠨࡋࡦࡻࠣࡱࡪࡺࡲࡪࡥࡶࠤࡷ࡫ࡱࡶࡧࡶࡸࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪࠣࡷࡹࡧࡴࡶࡵࠣࡿࢂࠨਤ").format(response.status_code))
          except Exception as e:
              logger.debug(bstack11l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡴࡤࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࡀࠠࡼࡿࠥਥ").format(e))
      bstack11l11lll_opy_()
  except Exception as e:
      logger.debug(bstack11l11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡴࡤࡠ࡭ࡨࡽࡤࡳࡥࡵࡴ࡬ࡧࡸࡀࠠࡼࡿࠥਦ").format(e))
def bstack11ll1l1l11_opy_():
  bstack1l11ll1111_opy_ = bstack11l11_opy_ (u"ࠤࠥਧ")
  global bstack1llll1ll1l_opy_
  global bstack111l1llll1_opy_
  global bstack11l1lll1_opy_
  global bstack1l11l1l11l_opy_
  global ROBOT_PYTHON_ERRORS
  global bstack1llll11l1l_opy_
  global CONFIG
  bstack1l1l1l111l_opy_ = os.environ.get(bstack11l11_opy_ (u"ࠪࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡕࡔࡇࡇࠫਨ"))
  if bstack1l1l1l111l_opy_ not in [bstack11l11_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ਩")]:
    bstack1l11ll1111_opy_ = bstack111l1lllll_opy_.bstack1l11111111_opy_(EVENTS.bstack1lll1lll1l_opy_)
  percy.shutdown()
  if bstack1llll1ll1l_opy_:
    logger.warning(bstack1l1l11lll_opy_.format(str(bstack1llll1ll1l_opy_)))
  else:
    try:
      bstack1l1ll1l1_opy_ = bstack1l1111ll_opy_(bstack11l11_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫਪ"), logger)
      if bstack1l1ll1l1_opy_.get(bstack11l11_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫਫ")) and bstack1l1ll1l1_opy_.get(bstack11l11_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬਬ")).get(bstack11l11_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪਭ")):
        logger.warning(bstack1l1l11lll_opy_.format(str(bstack1l1ll1l1_opy_[bstack11l11_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧਮ")][bstack11l11_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬਯ")])))
    except Exception as e:
      logger.error(e)
  if cli.is_running() and bstack1l1l1l111l_opy_ not in [bstack11l11_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬਰ")]:
    bstack1l11l11111_opy_.invoke(bstack11ll111111_opy_.bstack11l1l111l1_opy_)
  logger.info(bstack1ll1lll11_opy_)
  global bstack1l1l111ll_opy_
  if bstack1l1l111ll_opy_:
    bstack1l1ll1111l_opy_()
  try:
    with bstack1ll1ll1l1_opy_:
      bstack1ll1111ll1_opy_ = bstack111l1llll1_opy_.copy()
    for driver in bstack1ll1111ll1_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack11lll11111_opy_)
  ROBOT_PYTHON_ERRORS = []
  if bstack1llll11l1l_opy_ == bstack11l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ਱"):
    ROBOT_PYTHON_ERRORS = bstack111ll11ll_opy_(bstack11l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧਲ"))
  if bstack1llll11l1l_opy_ == bstack11l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧਲ਼") and len(bstack1l11l1l11l_opy_) == 0:
    bstack1l11l1l11l_opy_ = bstack111ll11ll_opy_(bstack11l11_opy_ (u"ࠨࡲࡺࡣࡵࡿࡴࡦࡵࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭਴"))
    if len(bstack1l11l1l11l_opy_) == 0:
      bstack1l11l1l11l_opy_ = bstack111ll11ll_opy_(bstack11l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡳࡴࡵࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨਵ"))
  bstack1llll11ll_opy_ = bstack11l11_opy_ (u"ࠪࠫਸ਼")
  if len(bstack11l1lll1_opy_) > 0:
    bstack1llll11ll_opy_ = bstack1l111l1lll_opy_(bstack11l1lll1_opy_)
  elif len(bstack1l11l1l11l_opy_) > 0:
    bstack1llll11ll_opy_ = bstack1l111l1lll_opy_(bstack1l11l1l11l_opy_)
  elif len(ROBOT_PYTHON_ERRORS) > 0:
    bstack1llll11ll_opy_ = bstack1l111l1lll_opy_(ROBOT_PYTHON_ERRORS)
  elif len(bstack1lll11ll1l_opy_) > 0:
    bstack1llll11ll_opy_ = bstack1l111l1lll_opy_(bstack1lll11ll1l_opy_)
  if bstack1l1l1l111l_opy_ not in [bstack11l11_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ਷")]:
    def bstack1lllllllll_opy_():
      try:
        if bstack1l1l1l111l_opy_ in [bstack11l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫਸ"), bstack11l11_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬਹ")]:
          bstack1lll11l1_opy_()
      except Exception as e:
        logger.debug(bstack11l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩ࡭ࡳࡧ࡬ࡠࡧࡻࡩࡨࡻࡴࡪࡱࡱ࠾ࠥࢁࡽࠣ਺").format(e))
    def bstack1ll1l11l1l_opy_():
      try:
        if bool(bstack1llll11ll_opy_):
          bstack111ll111l1_opy_(bstack1llll11ll_opy_)
        else:
          bstack111ll111l1_opy_()
      except Exception as e:
        logger.debug(bstack11l11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡴࡧࡱࡨ࡮ࡴࡧࠡࡧࡹࡩࡳࡺ࠺ࠡࡽࢀࠦ਻").format(e))
    def bstack1l1ll11l11_opy_():
      try:
        logger_utils.bstack1l1l1l11l_opy_(CONFIG)
      except Exception as e:
        logger.debug(bstack11l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡵࡨࡲࡩ࡯࡮ࡨࠢ࡯ࡳ࡬ࡹ࠺ࠡࡽࢀ਼ࠦ").format(e))
    bstack1l1l111l1_opy_ = threading.Thread(target=bstack1lllllllll_opy_)
    bstack111l11111l_opy_ = threading.Thread(target=bstack1ll1l11l1l_opy_)
    bstack11ll1l11ll_opy_ = threading.Thread(target=bstack1l1ll11l11_opy_)
    threads = [bstack1l1l111l1_opy_, bstack111l11111l_opy_, bstack11ll1l11ll_opy_]
    for thread in threads:
      try:
        thread.start()
      except Exception as e:
        logger.debug(bstack11l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡶࡸࡦࡸࡴࡪࡰࡪࠤࡹ࡮ࡲࡦࡣࡧࠤࢀࢃ࠺ࠡࡽࢀࠦ਽").format(thread.name, e))
    for thread in threads:
      try:
        thread.join()
      except Exception as e:
        logger.debug(bstack11l11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡮ࡴ࡯࡮ࡪࡰࡪࠤࡹ࡮ࡲࡦࡣࡧࠤࢀࢃ࠺ࠡࡽࢀࠦਾ").format(thread.name, e))
    bstack11l11llll1_opy_(bstack11l1111111_opy_, logger)
    bstack11l11llll1_opy_(os.path.join(os.getcwd(), bstack11l11_opy_ (u"ࠬࡲ࡯ࡨࠩਿ"), bstack11l11_opy_ (u"࠭࡫ࡦࡻ࠰ࡱࡪࡺࡲࡪࡥࡶ࠲࡯ࡹ࡯࡯ࠩੀ")), logger)
  if bstack1l1l1l111l_opy_ not in [bstack11l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨੁ")]:
    bstack111l1lllll_opy_.end(EVENTS.bstack1lll1lll1l_opy_.value, bstack1l11ll1111_opy_ + bstack11l11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣੂ"), bstack1l11ll1111_opy_ + bstack11l11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ੃"), status=True, failure=None, test_name=None)
    bstack111l111l_opy_()
    logger_utils.bstack111l1ll111_opy_()
    logging.shutdown()
  if len(ROBOT_PYTHON_ERRORS) > 0:
    sys.exit(len(ROBOT_PYTHON_ERRORS))
def bstack1l1ll1l1ll_opy_(bstack1ll1ll1111_opy_, frame):
  global bstack11l1l1111_opy_
  logger.error(bstack11l1ll1l_opy_)
  bstack11l1l1111_opy_.bstack1ll111ll11_opy_(bstack11l11_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡒࡴ࠭੄"), bstack1ll1ll1111_opy_)
  if hasattr(signal, bstack11l11_opy_ (u"ࠫࡘ࡯ࡧ࡯ࡣ࡯ࡷࠬ੅")):
    bstack11l1l1111_opy_.bstack1ll111ll11_opy_(bstack11l11_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬ੆"), signal.Signals(bstack1ll1ll1111_opy_).name)
  else:
    bstack11l1l1111_opy_.bstack1ll111ll11_opy_(bstack11l11_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭ੇ"), bstack11l11_opy_ (u"ࠧࡔࡋࡊ࡙ࡓࡑࡎࡐ࡙ࡑࠫੈ"))
  if cli.is_running():
    bstack1l11l11111_opy_.invoke(bstack11ll111111_opy_.bstack11l1l111l1_opy_)
  bstack1l1l1l111l_opy_ = os.environ.get(bstack11l11_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩ੉"))
  if bstack1l1l1l111l_opy_ == bstack11l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ੊") and not cli.is_enabled(CONFIG):
    bstack1ll111l1_opy_.stop(bstack11l1l1111_opy_.get_property(bstack11l11_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪੋ")))
  bstack11ll1l1l11_opy_()
  sys.exit(1)
def bstack1l1lll1111_opy_(err):
  logger.critical(bstack11ll1ll11l_opy_.format(str(err)))
  bstack111ll111l1_opy_(bstack11ll1ll11l_opy_.format(str(err)), True)
  atexit.unregister(bstack11ll1l1l11_opy_)
  bstack1lll11l1_opy_()
  sys.exit(1)
def bstack1l11l1ll1l_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack111ll111l1_opy_(message, True)
  atexit.unregister(bstack11ll1l1l11_opy_)
  bstack1lll11l1_opy_()
  sys.exit(1)
def bstack111ll1l1_opy_():
  global CONFIG
  global bstack11ll11lll1_opy_
  global bstack1lllll1l11_opy_
  global bstack111l1l11_opy_
  CONFIG = bstack11l1ll11ll_opy_()
  load_dotenv(CONFIG.get(bstack11l11_opy_ (u"ࠫࡪࡴࡶࡇ࡫࡯ࡩࠬੌ")))
  bstack1llllll1l_opy_()
  bstack1l1l111lll_opy_()
  CONFIG = bstack11llll11ll_opy_(CONFIG)
  update(CONFIG, bstack1lllll1l11_opy_)
  update(CONFIG, bstack11ll11lll1_opy_)
  if not cli.is_enabled(CONFIG):
    CONFIG = bstack11l1lllll_opy_(CONFIG)
  bstack111l1l11_opy_ = bstack1ll111l11_opy_(CONFIG)
  os.environ[bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ੍")] = bstack111l1l11_opy_.__str__().lower()
  bstack11l1l1111_opy_.bstack1ll111ll11_opy_(bstack11l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ੎"), bstack111l1l11_opy_)
  if (bstack11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ੏") in CONFIG and bstack11l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ੐") in bstack11ll11lll1_opy_) or (
          bstack11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬੑ") in CONFIG and bstack11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭੒") not in bstack1lllll1l11_opy_):
    if os.getenv(bstack11l11_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨ੓")):
      CONFIG[bstack11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ੔")] = os.getenv(bstack11l11_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪ੕"))
    else:
      if not CONFIG.get(bstack11l11_opy_ (u"ࠢࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠥ੖"), bstack11l11_opy_ (u"ࠣࠤ੗")) in bstack1l1lll1l1_opy_:
        bstack111lll1ll1_opy_()
  elif (bstack11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ੘") not in CONFIG and bstack11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬਖ਼") in CONFIG) or (
          bstack11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧਗ਼") in bstack1lllll1l11_opy_ and bstack11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨਜ਼") not in bstack11ll11lll1_opy_):
    del (CONFIG[bstack11l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨੜ")])
  if bstack1l11l1ll11_opy_(CONFIG):
    bstack1l1lll1111_opy_(bstack1ll1l11l_opy_)
  Config.bstack111l1lll_opy_().bstack1ll111ll11_opy_(bstack11l11_opy_ (u"ࠢࡶࡵࡨࡶࡓࡧ࡭ࡦࠤ੝"), CONFIG[bstack11l11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪਫ਼")])
  bstack111l11ll1l_opy_()
  bstack1l1llllll_opy_()
  if bstack11lll1l11_opy_ and not CONFIG.get(bstack11l11_opy_ (u"ࠤࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠧ੟"), bstack11l11_opy_ (u"ࠥࠦ੠")) in bstack1l1lll1l1_opy_:
    CONFIG[bstack11l11_opy_ (u"ࠫࡦࡶࡰࠨ੡")] = bstack1l11llll1_opy_(CONFIG)
    logger.info(bstack1ll11l1l_opy_.format(CONFIG[bstack11l11_opy_ (u"ࠬࡧࡰࡱࠩ੢")]))
  if not bstack111l1l11_opy_:
    CONFIG[bstack11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ੣")] = [{}]
def bstack11111llll_opy_(config, bstack11l1l1ll1_opy_):
  global CONFIG
  global bstack11lll1l11_opy_
  CONFIG = config
  bstack11lll1l11_opy_ = bstack11l1l1ll1_opy_
def bstack1l1llllll_opy_():
  global CONFIG
  global bstack11lll1l11_opy_
  if bstack11l11_opy_ (u"ࠧࡢࡲࡳࠫ੤") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1l11l1ll1l_opy_(e, bstack1ll1lll1l_opy_)
    bstack11lll1l11_opy_ = True
    bstack11l1l1111_opy_.bstack1ll111ll11_opy_(bstack11l11_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ੥"), True)
def bstack1l11llll1_opy_(config):
  bstack1l1111ll11_opy_ = bstack11l11_opy_ (u"ࠩࠪ੦")
  app = config[bstack11l11_opy_ (u"ࠪࡥࡵࡶࠧ੧")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1l1ll11ll1_opy_:
      if os.path.exists(app):
        bstack1l1111ll11_opy_ = bstack1l1l1lllll_opy_(config, app)
      elif bstack111ll111ll_opy_(app):
        bstack1l1111ll11_opy_ = app
      else:
        bstack1l1lll1111_opy_(bstack1ll11ll1_opy_.format(app))
    else:
      if bstack111ll111ll_opy_(app):
        bstack1l1111ll11_opy_ = app
      elif os.path.exists(app):
        bstack1l1111ll11_opy_ = bstack1l1l1lllll_opy_(app)
      else:
        bstack1l1lll1111_opy_(bstack1111111l1_opy_)
  else:
    if len(app) > 2:
      bstack1l1lll1111_opy_(bstack1lll1lll11_opy_)
    elif len(app) == 2:
      if bstack11l11_opy_ (u"ࠫࡵࡧࡴࡩࠩ੨") in app and bstack11l11_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨ੩") in app:
        if os.path.exists(app[bstack11l11_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ੪")]):
          bstack1l1111ll11_opy_ = bstack1l1l1lllll_opy_(config, app[bstack11l11_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ੫")], app[bstack11l11_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫ੬")])
        else:
          bstack1l1lll1111_opy_(bstack1ll11ll1_opy_.format(app))
      else:
        bstack1l1lll1111_opy_(bstack1lll1lll11_opy_)
    else:
      for key in app:
        if key in bstack11l1111ll_opy_:
          if key == bstack11l11_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ੭"):
            if os.path.exists(app[key]):
              bstack1l1111ll11_opy_ = bstack1l1l1lllll_opy_(config, app[key])
            else:
              bstack1l1lll1111_opy_(bstack1ll11ll1_opy_.format(app))
          else:
            bstack1l1111ll11_opy_ = app[key]
        else:
          bstack1l1lll1111_opy_(bstack1l1ll1ll_opy_)
  return bstack1l1111ll11_opy_
def bstack111ll111ll_opy_(bstack1l1111ll11_opy_):
  import re
  bstack11lll111ll_opy_ = re.compile(bstack11l11_opy_ (u"ࡵࠦࡣࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫࠦࠥ੮"))
  bstack1lll1lll_opy_ = re.compile(bstack11l11_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬ࠲࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰ࠤࠣ੯"))
  if bstack11l11_opy_ (u"ࠬࡨࡳ࠻࠱࠲ࠫੰ") in bstack1l1111ll11_opy_ or re.fullmatch(bstack11lll111ll_opy_, bstack1l1111ll11_opy_) or re.fullmatch(bstack1lll1lll_opy_, bstack1l1111ll11_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack111l1ll1_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l111l11l_opy_=bstack11l1111lll_opy_)
def bstack1l1l1lllll_opy_(config, path, bstack111l1111l1_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack11l11_opy_ (u"࠭ࡲࡣࠩੱ")).read()).hexdigest()
  bstack1llllll1l1_opy_ = bstack1ll1111ll_opy_(md5_hash)
  bstack1l1111ll11_opy_ = None
  if bstack1llllll1l1_opy_:
    logger.info(bstack1l11111lll_opy_.format(bstack1llllll1l1_opy_, md5_hash))
    return bstack1llllll1l1_opy_
  bstack1lllll111_opy_ = datetime.datetime.now()
  bstack11l1l1l1ll_opy_ = MultipartEncoder(
    fields={
      bstack11l11_opy_ (u"ࠧࡧ࡫࡯ࡩࠬੲ"): (os.path.basename(path), open(os.path.abspath(path), bstack11l11_opy_ (u"ࠨࡴࡥࠫੳ")), bstack11l11_opy_ (u"ࠩࡷࡩࡽࡺ࠯ࡱ࡮ࡤ࡭ࡳ࠭ੴ")),
      bstack11l11_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ੵ"): bstack111l1111l1_opy_
    }
  )
  response = requests.post(bstack111l111ll_opy_, data=bstack11l1l1l1ll_opy_,
                           headers={bstack11l11_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪ੶"): bstack11l1l1l1ll_opy_.content_type},
                           auth=(config[bstack11l11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ੷")], config[bstack11l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ੸")]))
  try:
    res = json.loads(response.text)
    bstack1l1111ll11_opy_ = res[bstack11l11_opy_ (u"ࠧࡢࡲࡳࡣࡺࡸ࡬ࠨ੹")]
    logger.info(bstack1lll1lllll_opy_.format(bstack1l1111ll11_opy_))
    bstack11ll11ll11_opy_(md5_hash, bstack1l1111ll11_opy_)
    cli.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠣࡪࡷࡸࡵࡀࡵࡱ࡮ࡲࡥࡩࡥࡡࡱࡲࠥ੺"), datetime.datetime.now() - bstack1lllll111_opy_)
  except ValueError as err:
    bstack1l1lll1111_opy_(bstack1ll1l11111_opy_.format(str(err)))
  return bstack1l1111ll11_opy_
def bstack111l11ll1l_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack1l111lll11_opy_
  bstack1111llll1l_opy_ = 1
  bstack11lll11l1l_opy_ = 1
  if bstack11l11_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ੻") in CONFIG:
    bstack11lll11l1l_opy_ = CONFIG[bstack11l11_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ੼")]
  else:
    bstack11lll11l1l_opy_ = bstack1l1l1111ll_opy_(framework_name, args) or 1
  if bstack11l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ੽") in CONFIG:
    bstack1111llll1l_opy_ = len(CONFIG[bstack11l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ੾")])
  bstack1l111lll11_opy_ = int(bstack11lll11l1l_opy_) * int(bstack1111llll1l_opy_)
def bstack1l1l1111ll_opy_(framework_name, args):
  if framework_name == bstack11ll1111l_opy_ and args and bstack11l11_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ੿") in args:
      bstack11l11111l_opy_ = args.index(bstack11l11_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ઀"))
      return int(args[bstack11l11111l_opy_ + 1]) or 1
  return 1
def bstack1ll1111ll_opy_(md5_hash):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack11l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡲ࡯ࡤ࡭ࠣࡲࡴࡺࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧ࠯ࠤࡺࡹࡩ࡯ࡩࠣࡦࡦࡹࡩࡤࠢࡩ࡭ࡱ࡫ࠠࡰࡲࡨࡶࡦࡺࡩࡰࡰࡶࠫઁ"))
    bstack11l111ll1l_opy_ = os.path.join(os.path.expanduser(bstack11l11_opy_ (u"ࠩࢁࠫં")), bstack11l11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪઃ"), bstack11l11_opy_ (u"ࠫࡦࡶࡰࡖࡲ࡯ࡳࡦࡪࡍࡅ࠷ࡋࡥࡸ࡮࠮࡫ࡵࡲࡲࠬ઄"))
    if os.path.exists(bstack11l111ll1l_opy_):
      try:
        bstack11ll11l1_opy_ = json.load(open(bstack11l111ll1l_opy_, bstack11l11_opy_ (u"ࠬࡸࡢࠨઅ")))
        if md5_hash in bstack11ll11l1_opy_:
          bstack1llllll1ll_opy_ = bstack11ll11l1_opy_[md5_hash]
          bstack11l11lllll_opy_ = datetime.datetime.now()
          bstack1l1llll111_opy_ = datetime.datetime.strptime(bstack1llllll1ll_opy_[bstack11l11_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩઆ")], bstack11l11_opy_ (u"ࠧࠦࡦ࠲ࠩࡲ࠵࡚ࠥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫઇ"))
          if (bstack11l11lllll_opy_ - bstack1l1llll111_opy_).days > 30:
            return None
          elif version.parse(str(__version__)) > version.parse(bstack1llllll1ll_opy_[bstack11l11_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ઈ")]):
            return None
          return bstack1llllll1ll_opy_[bstack11l11_opy_ (u"ࠩ࡬ࡨࠬઉ")]
      except Exception as e:
        logger.debug(bstack11l11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡵࡩࡦࡪࡩ࡯ࡩࠣࡑࡉ࠻ࠠࡩࡣࡶ࡬ࠥ࡬ࡩ࡭ࡧ࠽ࠤࢀࢃࠧઊ").format(str(e)))
    return None
  bstack11l111ll1l_opy_ = os.path.join(os.path.expanduser(bstack11l11_opy_ (u"ࠫࢃ࠭ઋ")), bstack11l11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬઌ"), bstack11l11_opy_ (u"࠭ࡡࡱࡲࡘࡴࡱࡵࡡࡥࡏࡇ࠹ࡍࡧࡳࡩ࠰࡭ࡷࡴࡴࠧઍ"))
  lock_file = bstack11l111ll1l_opy_ + bstack11l11_opy_ (u"ࠧ࠯࡮ࡲࡧࡰ࠭઎")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack11l111ll1l_opy_):
        with open(bstack11l111ll1l_opy_, bstack11l11_opy_ (u"ࠨࡴࠪએ")) as f:
          content = f.read().strip()
          if content:
            bstack11ll11l1_opy_ = json.loads(content)
            if md5_hash in bstack11ll11l1_opy_:
              bstack1llllll1ll_opy_ = bstack11ll11l1_opy_[md5_hash]
              bstack11l11lllll_opy_ = datetime.datetime.now()
              bstack1l1llll111_opy_ = datetime.datetime.strptime(bstack1llllll1ll_opy_[bstack11l11_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬઐ")], bstack11l11_opy_ (u"ࠪࠩࡩ࠵ࠥ࡮࠱ࠨ࡝ࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧઑ"))
              if (bstack11l11lllll_opy_ - bstack1l1llll111_opy_).days > 30:
                return None
              elif version.parse(str(__version__)) > version.parse(bstack1llllll1ll_opy_[bstack11l11_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ઒")]):
                return None
              return bstack1llllll1ll_opy_[bstack11l11_opy_ (u"ࠬ࡯ࡤࠨઓ")]
      return None
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡽࡩࡵࡪࠣࡪ࡮ࡲࡥࠡ࡮ࡲࡧࡰ࡯࡮ࡨࠢࡩࡳࡷࠦࡍࡅ࠷ࠣ࡬ࡦࡹࡨ࠻ࠢࡾࢁࠬઔ").format(str(e)))
    return None
def bstack11ll11ll11_opy_(md5_hash, bstack1l1111ll11_opy_):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack11l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡱࡵࡣ࡬ࠢࡱࡳࡹࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦ࠮ࠣࡹࡸ࡯࡮ࡨࠢࡥࡥࡸ࡯ࡣࠡࡨ࡬ࡰࡪࠦ࡯ࡱࡧࡵࡥࡹ࡯࡯࡯ࡵࠪક"))
    bstack1l1llll1l1_opy_ = os.path.join(os.path.expanduser(bstack11l11_opy_ (u"ࠨࢀࠪખ")), bstack11l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩગ"))
    if not os.path.exists(bstack1l1llll1l1_opy_):
      os.makedirs(bstack1l1llll1l1_opy_)
    bstack11l111ll1l_opy_ = os.path.join(os.path.expanduser(bstack11l11_opy_ (u"ࠪࢂࠬઘ")), bstack11l11_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫઙ"), bstack11l11_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭ચ"))
    bstack11l1lll11l_opy_ = {
      bstack11l11_opy_ (u"࠭ࡩࡥࠩછ"): bstack1l1111ll11_opy_,
      bstack11l11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪજ"): datetime.datetime.strftime(datetime.datetime.now(), bstack11l11_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬઝ")),
      bstack11l11_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧઞ"): str(__version__)
    }
    try:
      bstack11ll11l1_opy_ = {}
      if os.path.exists(bstack11l111ll1l_opy_):
        bstack11ll11l1_opy_ = json.load(open(bstack11l111ll1l_opy_, bstack11l11_opy_ (u"ࠪࡶࡧ࠭ટ")))
      bstack11ll11l1_opy_[md5_hash] = bstack11l1lll11l_opy_
      with open(bstack11l111ll1l_opy_, bstack11l11_opy_ (u"ࠦࡼ࠱ࠢઠ")) as outfile:
        json.dump(bstack11ll11l1_opy_, outfile)
    except Exception as e:
      logger.debug(bstack11l11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡺࡶࡤࡢࡶ࡬ࡲ࡬ࠦࡍࡅ࠷ࠣ࡬ࡦࡹࡨࠡࡨ࡬ࡰࡪࡀࠠࡼࡿࠪડ").format(str(e)))
    return
  bstack1l1llll1l1_opy_ = os.path.join(os.path.expanduser(bstack11l11_opy_ (u"࠭ࡾࠨઢ")), bstack11l11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧણ"))
  if not os.path.exists(bstack1l1llll1l1_opy_):
    os.makedirs(bstack1l1llll1l1_opy_)
  bstack11l111ll1l_opy_ = os.path.join(os.path.expanduser(bstack11l11_opy_ (u"ࠨࢀࠪત")), bstack11l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩથ"), bstack11l11_opy_ (u"ࠪࡥࡵࡶࡕࡱ࡮ࡲࡥࡩࡓࡄ࠶ࡊࡤࡷ࡭࠴ࡪࡴࡱࡱࠫદ"))
  lock_file = bstack11l111ll1l_opy_ + bstack11l11_opy_ (u"ࠫ࠳ࡲ࡯ࡤ࡭ࠪધ")
  bstack11l1lll11l_opy_ = {
    bstack11l11_opy_ (u"ࠬ࡯ࡤࠨન"): bstack1l1111ll11_opy_,
    bstack11l11_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ઩"): datetime.datetime.strftime(datetime.datetime.now(), bstack11l11_opy_ (u"ࠧࠦࡦ࠲ࠩࡲ࠵࡚ࠥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫપ")),
    bstack11l11_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ફ"): str(__version__)
  }
  try:
    with FileLock(lock_file, timeout=10):
      bstack11ll11l1_opy_ = {}
      if os.path.exists(bstack11l111ll1l_opy_):
        with open(bstack11l111ll1l_opy_, bstack11l11_opy_ (u"ࠩࡵࠫબ")) as f:
          content = f.read().strip()
          if content:
            bstack11ll11l1_opy_ = json.loads(content)
      bstack11ll11l1_opy_[md5_hash] = bstack11l1lll11l_opy_
      with open(bstack11l111ll1l_opy_, bstack11l11_opy_ (u"ࠥࡻࠧભ")) as outfile:
        json.dump(bstack11ll11l1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡻ࡮ࡺࡨࠡࡨ࡬ࡰࡪࠦ࡬ࡰࡥ࡮࡭ࡳ࡭ࠠࡧࡱࡵࠤࡒࡊ࠵ࠡࡪࡤࡷ࡭ࠦࡵࡱࡦࡤࡸࡪࡀࠠࡼࡿࠪમ").format(str(e)))
def bstack1l1l1ll1l_opy_(self):
  return
def bstack1ll1l1ll_opy_(self):
  return
def bstack1111l1ll_opy_():
  global bstack1l1ll1lll1_opy_
  bstack1l1ll1lll1_opy_ = True
def bstack1ll11ll11l_opy_(self):
  global bstack11l1111ll1_opy_
  global bstack1111ll1l1_opy_
  global bstack11l111l1ll_opy_
  bstack1l111l111l_opy_ = bstack111l1lllll_opy_.bstack1l11111111_opy_(EVENTS.bstack1lll11l1l1_opy_)
  try:
    if bstack11l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬય") in bstack11l1111ll1_opy_ and self.session_id != None and bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪર"), bstack11l11_opy_ (u"ࠧࠨ઱")) != bstack11l11_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩલ"):
      bstack111l111lll_opy_ = bstack11l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩળ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ઴")
      if bstack111l111lll_opy_ == bstack11l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫવ"):
        bstack11111l111_opy_(logger)
      if self != None:
        bstack1ll1l1l1_opy_(self, bstack111l111lll_opy_, bstack11l11_opy_ (u"ࠬ࠲ࠠࠨશ").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack11l11_opy_ (u"࠭ࠧષ")
    if bstack11l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧસ") in bstack11l1111ll1_opy_ and getattr(threading.current_thread(), bstack11l11_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧહ"), None):
      bstack1ll11l1l11_opy_.bstack1l1l111l_opy_(self, bstack11l11lll1l_opy_, logger, wait=True)
    if bstack11l11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ઺") in bstack11l1111ll1_opy_:
      bstack1ll11l11ll_opy_.bstack1111l1111_opy_(self)
    bstack111l1lllll_opy_.end(EVENTS.bstack1lll11l1l1_opy_.value, bstack1l111l111l_opy_ + bstack11l11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ઻"), bstack1l111l111l_opy_ + bstack11l11_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ઼"), status=True, failure=None, test_name=None)
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࠨઽ") + str(e))
    bstack111l1lllll_opy_.end(EVENTS.bstack1lll11l1l1_opy_.value, bstack1l111l111l_opy_ + bstack11l11_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨા"), bstack1l111l111l_opy_ + bstack11l11_opy_ (u"ࠢ࠻ࡧࡱࡨࠧિ"), status=False, failure=str(e), test_name=None)
  bstack11l111l1ll_opy_(self)
  self.session_id = None
def bstack1111l111_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack11ll1l1ll1_opy_
    global bstack11l1111ll1_opy_
    command_executor = kwargs.get(bstack11l11_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠫી"), bstack11l11_opy_ (u"ࠩࠪુ"))
    bstack1llll1l1ll_opy_ = False
    if type(command_executor) == str and bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ૂ") in command_executor:
      bstack1llll1l1ll_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧૃ") in str(getattr(command_executor, bstack11l11_opy_ (u"ࠬࡥࡵࡳ࡮ࠪૄ"), bstack11l11_opy_ (u"࠭ࠧૅ"))):
      bstack1llll1l1ll_opy_ = True
    else:
      kwargs = bstack1lllll111l_opy_.bstack1l111l1l_opy_(bstack111l1ll1ll_opy_=kwargs, config=CONFIG)
      return bstack11l111111_opy_(self, *args, **kwargs)
    if bstack1llll1l1ll_opy_:
      bstack111ll1ll1l_opy_ = bstack1l11l1l1l1_opy_.bstack11l1ll11l_opy_(CONFIG, bstack11l1111ll1_opy_)
      if kwargs.get(bstack11l11_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ૆")):
        kwargs[bstack11l11_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩે")] = bstack11ll1l1ll1_opy_(kwargs[bstack11l11_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪૈ")], bstack11l1111ll1_opy_, CONFIG, bstack111ll1ll1l_opy_)
      elif kwargs.get(bstack11l11_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪૉ")):
        kwargs[bstack11l11_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ૊")] = bstack11ll1l1ll1_opy_(kwargs[bstack11l11_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬો")], bstack11l1111ll1_opy_, CONFIG, bstack111ll1ll1l_opy_)
  except Exception as e:
    logger.error(bstack11l11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡦࡰࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡔࡆࡎࠤࡨࡧࡰࡴ࠼ࠣࡿࢂࠨૌ").format(str(e)))
  return bstack11l111111_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack1l1l1ll11_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l111l11l_opy_=bstack11l1111lll_opy_)
def bstack1ll1llll1_opy_(self, command_executor=bstack11l11_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯࠲࠴࠺࠲࠵࠴࠰࠯࠳࠽࠸࠹࠺࠴્ࠣ"), *args, **kwargs):
  global bstack1111ll1l1_opy_
  global bstack111l1llll1_opy_
  bstack1ll1ll1ll_opy_ = bstack1111l111_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack11l1ll111l_opy_.on():
    return bstack1ll1ll1ll_opy_
  try:
    logger.debug(bstack11l11_opy_ (u"ࠨࡅࡲࡱࡲࡧ࡮ࡥࠢࡈࡼࡪࡩࡵࡵࡱࡵࠤࡼ࡮ࡥ࡯ࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥ࡯ࡳࠡࡨࡤࡰࡸ࡫ࠠ࠮ࠢࡾࢁࠬ૎").format(str(command_executor)))
    logger.debug(bstack11l11_opy_ (u"ࠩࡋࡹࡧࠦࡕࡓࡎࠣ࡭ࡸࠦ࠭ࠡࡽࢀࠫ૏").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ૐ") in command_executor._url:
      bstack11l1l1111_opy_.bstack1ll111ll11_opy_(bstack11l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬ૑"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨ૒") in command_executor):
    bstack11l1l1111_opy_.bstack1ll111ll11_opy_(bstack11l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ૓"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack111l1l1l_opy_ = getattr(threading.current_thread(), bstack11l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡔࡦࡵࡷࡑࡪࡺࡡࠨ૔"), None)
  bstack1ll1ll1l_opy_ = {}
  if self.capabilities is not None:
    bstack1ll1ll1l_opy_[bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧ૕")] = self.capabilities.get(bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ૖"))
    bstack1ll1ll1l_opy_[bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ૗")] = self.capabilities.get(bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ૘"))
    bstack1ll1ll1l_opy_[bstack11l11_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡤࡵࡰࡵ࡫ࡲࡲࡸ࠭૙")] = self.capabilities.get(bstack11l11_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ૚"))
  if CONFIG.get(bstack11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ૛"), False) and bstack1lllll111l_opy_.bstack11l1l1l111_opy_(bstack1ll1ll1l_opy_):
    threading.current_thread().a11yPlatform = True
  if bstack11l11_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ૜") in bstack11l1111ll1_opy_ or bstack11l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ૝") in bstack11l1111ll1_opy_:
    bstack1ll111l1_opy_.bstack1ll1111l11_opy_(self)
  if bstack11l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ૞") in bstack11l1111ll1_opy_ and bstack111l1l1l_opy_ and bstack111l1l1l_opy_.get(bstack11l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ૟"), bstack11l11_opy_ (u"ࠬ࠭ૠ")) == bstack11l11_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧૡ"):
    bstack1ll111l1_opy_.bstack1ll1111l11_opy_(self)
  bstack1111ll1l1_opy_ = self.session_id
  with bstack1ll1ll1l1_opy_:
    bstack111l1llll1_opy_.append(self)
  return bstack1ll1ll1ll_opy_
def bstack11ll1111l1_opy_(args):
  return bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲࠨૢ") in str(args)
def bstack11111ll11_opy_(self, driver_command, *args, **kwargs):
  global bstack1lll111l_opy_
  global bstack1l1l1ll111_opy_
  bstack1l111lll1l_opy_ = bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬૣ"), None) and bstack11ll11l11_opy_(
          threading.current_thread(), bstack11l11_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ૤"), None)
  bstack1l1l11ll11_opy_ = bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ૥"), None) and bstack11ll11l11_opy_(
          threading.current_thread(), bstack11l11_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭૦"), None)
  bstack11llll11l_opy_ = getattr(self, bstack11l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬ૧"), None) != None and getattr(self, bstack11l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭૨"), None) == True
  if not bstack1l1l1ll111_opy_ and bstack11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ૩") in CONFIG and CONFIG[bstack11l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ૪")] == True and bstack1l1lll111l_opy_.bstack1lll1l1ll_opy_(driver_command) and (bstack11llll11l_opy_ or bstack1l111lll1l_opy_ or bstack1l1l11ll11_opy_) and not bstack11ll1111l1_opy_(args):
    try:
      bstack1l1l1ll111_opy_ = True
      logger.debug(bstack11l11_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡽࢀࠫ૫").format(driver_command))
      bstack1lllllll1_opy_ = perform_scan(self, driver_command=driver_command)
      logger.debug(bstack1lllllll1_opy_)
      try:
        bstack1llll11l1_opy_ = {
          bstack11l11_opy_ (u"ࠥࡶࡪࡷࡵࡦࡵࡷࠦ૬"): {
            bstack11l11_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࠧ૭"): bstack11l11_opy_ (u"ࠧࡇ࠱࠲࡛ࡢࡗࡈࡇࡎࠣ૮"),
            bstack11l11_opy_ (u"ࠨࡰࡢࡴࡤࡱࡪࡺࡥࡳࡵࠥ૯"): [
              {
                bstack11l11_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢ૰"): driver_command
              }
            ]
          },
          bstack11l11_opy_ (u"ࠣࡴࡨࡷࡵࡵ࡮ࡴࡧࠥ૱"): {
            bstack11l11_opy_ (u"ࠤࡥࡳࡩࡿࠢ૲"): {
              bstack11l11_opy_ (u"ࠥࡱࡸ࡭ࠢ૳"): bstack1lllllll1_opy_.get(bstack11l11_opy_ (u"ࠦࡲࡹࡧࠣ૴"), bstack11l11_opy_ (u"ࠧࠨ૵")) if isinstance(bstack1lllllll1_opy_, dict) else bstack11l11_opy_ (u"ࠨࠢ૶"),
              bstack11l11_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳࠣ૷"): bstack1lllllll1_opy_.get(bstack11l11_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴࠤ૸"), True) if isinstance(bstack1lllllll1_opy_, dict) else True
            }
          }
        }
        logger.debug(bstack11l11_opy_ (u"ࠩࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡧࡦࡴࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡱࡵࡧࠡࡦࡤࡸࡦࡀࠠࡼࡿࠪૹ").format(bstack1llll11l1_opy_))
        bstack111111l11_opy_.info(json.dumps(bstack1llll11l1_opy_, separators=(bstack11l11_opy_ (u"ࠪ࠰ࠬૺ"), bstack11l11_opy_ (u"ࠫ࠿࠭ૻ"))))
      except Exception as bstack11llll1l_opy_:
        logger.debug(bstack11l11_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡮ࡲ࡫ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡣࡢࡰࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠬૼ").format(str(bstack11llll1l_opy_)))
    except Exception as err:
      logger.debug(bstack11l11_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡩࡷ࡬࡯ࡳ࡯ࠣࡷࡨࡧ࡮ࠡࡽࢀࠫ૽").format(str(err)))
    bstack1l1l1ll111_opy_ = False
  response = bstack1lll111l_opy_(self, driver_command, *args, **kwargs)
  if (bstack11l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭૾") in str(bstack11l1111ll1_opy_).lower() or bstack11l11_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ૿") in str(bstack11l1111ll1_opy_).lower()) and bstack11l1ll111l_opy_.on():
    try:
      if driver_command == bstack11l11_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭଀"):
        bstack1ll111l1_opy_.bstack1l111111l_opy_({
            bstack11l11_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩଁ"): response[bstack11l11_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪଂ")],
            bstack11l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬଃ"): bstack1ll111l1_opy_.current_test_uuid() if bstack1ll111l1_opy_.current_test_uuid() else bstack11l1ll111l_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
def bstack1ll111111_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack1111ll1l1_opy_
  global bstack111llll1ll_opy_
  global bstack11l1111lll_opy_
  global bstack11lllll1l_opy_
  global bstack111l1111ll_opy_
  global bstack11l1111ll1_opy_
  global bstack11l111111_opy_
  global bstack111l1llll1_opy_
  global bstack11l111l111_opy_
  global bstack11l11lll1l_opy_
  bstack1l111l111l_opy_ = bstack111l1lllll_opy_.bstack1l11111111_opy_(EVENTS.bstack1l1l11ll1_opy_.value)
  if os.getenv(bstack11l11_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ଄")) is not None and bstack1lllll111l_opy_.bstack1ll11l1l1l_opy_(CONFIG) is None:
    CONFIG[bstack11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧଅ")] = True
  CONFIG[bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪଆ")] = str(bstack11l1111ll1_opy_) + str(__version__)
  bstack1ll11ll1l_opy_ = os.environ[bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧଇ")]
  bstack111ll1ll1l_opy_ = bstack1l11l1l1l1_opy_.bstack11l1ll11l_opy_(CONFIG, bstack11l1111ll1_opy_)
  CONFIG[bstack11l11_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ଈ")] = bstack1ll11ll1l_opy_
  CONFIG[bstack11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ଉ")] = bstack111ll1ll1l_opy_
  if CONFIG.get(bstack11l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬଊ"),bstack11l11_opy_ (u"࠭ࠧଋ")) and bstack11l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ଌ") in bstack11l1111ll1_opy_:
    CONFIG[bstack11l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ଍")].pop(bstack11l11_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ଎"), None)
    CONFIG[bstack11l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪଏ")].pop(bstack11l11_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩଐ"), None)
  command_executor = bstack1l1llll1ll_opy_()
  logger.debug(bstack1111ll11l_opy_.format(command_executor))
  proxy = bstack1l11l1lll_opy_(CONFIG, proxy)
  bstack11lllll1l1_opy_ = 0 if bstack111llll1ll_opy_ < 0 else bstack111llll1ll_opy_
  try:
    if bstack11lllll1l_opy_ is True:
      bstack11lllll1l1_opy_ = int(multiprocessing.current_process().name)
    elif bstack111l1111ll_opy_ is True:
      bstack11lllll1l1_opy_ = int(threading.current_thread().name)
  except:
    bstack11lllll1l1_opy_ = 0
  bstack11ll1ll1_opy_ = bstack1lll111l1_opy_(CONFIG, bstack11lllll1l1_opy_)
  logger.debug(bstack1l11ll1ll_opy_.format(str(bstack11ll1ll1_opy_)))
  if bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ଑") in CONFIG and bstack1ll1l11lll_opy_(CONFIG[bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ଒")]):
    bstack1l1111l111_opy_(bstack11ll1ll1_opy_)
  if bstack1lllll111l_opy_.bstack1llll1lll1_opy_(CONFIG, bstack11lllll1l1_opy_) and bstack1lllll111l_opy_.bstack11l111l1l_opy_(bstack11ll1ll1_opy_, options, desired_capabilities, CONFIG):
    threading.current_thread().a11yPlatform = True
    if (cli.accessibility is None or not cli.accessibility.is_enabled()):
      bstack1lllll111l_opy_.set_capabilities(bstack11ll1ll1_opy_, CONFIG)
  if desired_capabilities:
    bstack1lllll1ll_opy_ = bstack11llll11ll_opy_(desired_capabilities)
    bstack1lllll1ll_opy_[bstack11l11_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧଓ")] = bstack1l1l1llll_opy_(CONFIG)
    bstack1l11l1111l_opy_ = bstack1lll111l1_opy_(bstack1lllll1ll_opy_)
    if bstack1l11l1111l_opy_:
      bstack11ll1ll1_opy_ = update(bstack1l11l1111l_opy_, bstack11ll1ll1_opy_)
    desired_capabilities = None
  if options:
    bstack1ll1lllll_opy_(options, bstack11ll1ll1_opy_)
  if not options:
    options = bstack1111ll1ll1_opy_(bstack11ll1ll1_opy_)
  try:
    if bstack1ll11l1111_opy_:
      def _11llllll1l_opy_(bstack111ll1ll_opy_):
        if not isinstance(bstack111ll1ll_opy_, dict):
          return
        for _1lll1l111l_opy_ in list(bstack111ll1ll_opy_.keys()):
          _111ll1l1l1_opy_ = bstack111ll1ll_opy_[_1lll1l111l_opy_]
          if _111ll1l1l1_opy_ is None:
            bstack111ll1ll_opy_.pop(_1lll1l111l_opy_, None)
          elif isinstance(_111ll1l1l1_opy_, dict):
            _11llllll1l_opy_(_111ll1l1l1_opy_)
      _11llllll1l_opy_(bstack11ll1ll1_opy_)
      _11llllll1l_opy_(desired_capabilities)
      if options is not None and hasattr(options, bstack11l11_opy_ (u"ࠨࡡࡦࡥࡵࡹࠧଔ")):
        _11llllll1l_opy_(options._caps)
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"ࠤࡰࡳࡩࡥࡩ࡯࡫ࡷࠬ࠮ࠦࡰࡰࡵࡷ࠱ࡴࡶࡴࡪࡱࡱࡷࠥࡶࡲࡶࡰࡨࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽࠣକ").format(e))
  if bstack1ll11l1111_opy_:
    options = bstack1ll11llll_opy_(options)
  bstack11l11lll1l_opy_ = CONFIG.get(bstack11l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ଖ"))[bstack11lllll1l1_opy_]
  if proxy and bstack111l1lll1_opy_() >= version.parse(bstack11l11_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫଗ")):
    options.proxy(proxy)
  if options and bstack111l1lll1_opy_() >= version.parse(bstack11l11_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫଘ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack111l1lll1_opy_() < version.parse(bstack11l11_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬଙ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack11ll1ll1_opy_)
  logger.info(bstack111l1l1l1_opy_)
  bstack11ll11ll1l_opy_.end(EVENTS.bstack11lllll1ll_opy_.value, EVENTS.bstack11lllll1ll_opy_.value + bstack11l11_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢଚ"), EVENTS.bstack11lllll1ll_opy_.value + bstack11l11_opy_ (u"ࠣ࠼ࡨࡲࡩࠨଛ"), status=True, failure=None, test_name=bstack11l1111lll_opy_)
  if bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡴࡷࡵࡦࡪ࡮ࡨࠫଜ") in kwargs:
    del kwargs[bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡵࡸ࡯ࡧ࡫࡯ࡩࠬଝ")]
  bstack111l1lllll_opy_.end(EVENTS.bstack1l1l11ll1_opy_.value, bstack1l111l111l_opy_ + bstack11l11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦଞ"), bstack1l111l111l_opy_ + bstack11l11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥଟ"), status=True, failure=None, test_name=bstack11l1111lll_opy_)
  try:
    if bstack111l1lll1_opy_() >= version.parse(bstack11l11_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ଠ")):
      bstack11l111111_opy_(self, command_executor=command_executor,
                options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
    elif bstack111l1lll1_opy_() >= version.parse(bstack11l11_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ଡ")):
      bstack11l111111_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities, options=options,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    elif bstack111l1lll1_opy_() >= version.parse(bstack11l11_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨଢ")):
      bstack11l111111_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    else:
      bstack11l111111_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive)
  except Exception as bstack11llll111l_opy_:
    logger.error(bstack1l1lll1lll_opy_.format(bstack11l11_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠨଣ"), str(bstack11llll111l_opy_)))
    raise bstack11llll111l_opy_
  bstack1l111l111l_opy_ = bstack111l1lllll_opy_.bstack1l11111111_opy_(EVENTS.bstack1l1l1ll11_opy_.value)
  if bstack1lllll111l_opy_.bstack1llll1lll1_opy_(CONFIG, bstack11lllll1l1_opy_) and bstack1lllll111l_opy_.bstack11l111l1l_opy_(self.caps, options, desired_capabilities):
    if CONFIG[bstack11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬତ")][bstack11l11_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪଥ")] == True:
      threading.current_thread().appA11yPlatform = True
      if cli.accessibility is None or not cli.accessibility.is_enabled():
        bstack1lllll111l_opy_.set_capabilities(bstack11ll1ll1_opy_, CONFIG)
  try:
    bstack1111lll1_opy_ = bstack11l11_opy_ (u"ࠬ࠭ଦ")
    if bstack111l1lll1_opy_() >= version.parse(bstack11l11_opy_ (u"࠭࠴࠯࠲࠱࠴ࡧ࠷ࠧଧ")):
      if self.caps is not None:
        bstack1111lll1_opy_ = self.caps.get(bstack11l11_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢନ"))
    else:
      if self.capabilities is not None:
        bstack1111lll1_opy_ = self.capabilities.get(bstack11l11_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣ଩"))
    if bstack1111lll1_opy_:
      bstack111llll1_opy_(bstack1111lll1_opy_)
      if bstack111l1lll1_opy_() <= version.parse(bstack11l11_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩପ")):
        if bstack1ll1l1l1ll_opy_.startswith(bstack11l11_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫଫ")) or bstack1ll1l1l1ll_opy_.startswith(bstack11l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࠭ବ")):
          self.command_executor._url = bstack1ll1l1l1ll_opy_
        else:
          self.command_executor._url = bstack11l11_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨଭ") + bstack1ll1l1l1ll_opy_ + bstack11l11_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥମ")
      else:
        self.command_executor._url = bstack11l11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤଯ") + bstack1111lll1_opy_ + bstack11l11_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤର")
      logger.debug(bstack11l1l1l1_opy_.format(bstack1111lll1_opy_))
    else:
      logger.debug(bstack1lll111111_opy_.format(bstack11l11_opy_ (u"ࠤࡒࡴࡹ࡯࡭ࡢ࡮ࠣࡌࡺࡨࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦࠥ଱")))
  except Exception as e:
    logger.debug(bstack1lll111111_opy_.format(e))
  if bstack11l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩଲ") in bstack11l1111ll1_opy_:
    bstack11ll111ll_opy_(bstack111llll1ll_opy_, bstack11l111l111_opy_)
  bstack1111ll1l1_opy_ = self.session_id
  if bstack11l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫଳ") in bstack11l1111ll1_opy_ or bstack11l11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ଴") in bstack11l1111ll1_opy_ or bstack11l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬଵ") in bstack11l1111ll1_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack111l1l1l_opy_ = getattr(threading.current_thread(), bstack11l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡔࡦࡵࡷࡑࡪࡺࡡࠨଶ"), None)
  if bstack11l11_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨଷ") in bstack11l1111ll1_opy_ or bstack11l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨସ") in bstack11l1111ll1_opy_:
    bstack1ll111l1_opy_.bstack1ll1111l11_opy_(self)
  if bstack11l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪହ") in bstack11l1111ll1_opy_ and bstack111l1l1l_opy_ and bstack111l1l1l_opy_.get(bstack11l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ଺"), bstack11l11_opy_ (u"ࠬ࠭଻")) == bstack11l11_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭଼ࠧ"):
    bstack1ll111l1_opy_.bstack1ll1111l11_opy_(self)
  with bstack1ll1ll1l1_opy_:
    bstack111l1llll1_opy_.append(self)
  if bstack11l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଽ") in CONFIG and bstack11l11_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ା") in CONFIG[bstack11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬି")][bstack11lllll1l1_opy_]:
    bstack11l1111lll_opy_ = CONFIG[bstack11l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ୀ")][bstack11lllll1l1_opy_][bstack11l11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩୁ")]
  logger.debug(bstack1ll11111ll_opy_.format(bstack1111ll1l1_opy_))
  bstack111l1lllll_opy_.end(EVENTS.bstack1l1l1ll11_opy_.value, bstack1l111l111l_opy_ + bstack11l11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧୂ"), bstack1l111l111l_opy_ + bstack11l11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦୃ"), status=True, failure=None, test_name=bstack11l1111lll_opy_)
try:
  try:
    import Browser
    import os
    from subprocess import Popen
    from browserstack_sdk.__init__ import bstack1l1ll1ll11_opy_
    def bstack1lll11llll_opy_(self, args, **kwargs):
      global CONFIG
      global bstack1l1lllll_opy_
      from browserstack_sdk.__init__ import LAUNCH_PATCH_ROBOT_PLAYWRIGHT
      if(bstack11l11_opy_ (u"ࠢࡪࡰࡧࡩࡽ࠴ࡪࡴࠤୄ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack11l11_opy_ (u"ࠨࢀࠪ୅")), bstack11l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ୆"), bstack11l11_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬେ")), bstack11l11_opy_ (u"ࠫࡼ࠭ୈ")) as fp:
          fp.write(bstack11l11_opy_ (u"ࠧࠨ୉"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack11l11_opy_ (u"ࠨࡩ࡯ࡦࡨࡼࡤࡨࡳࡵࡣࡦ࡯࠳ࡰࡳࠣ୊")))):
          with open(args[1], bstack11l11_opy_ (u"ࠧࡳࠩୋ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack11l11_opy_ (u"ࠨࡣࡶࡽࡳࡩࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡢࡲࡪࡽࡐࡢࡩࡨࠬࡨࡵ࡮ࡵࡧࡻࡸ࠱ࠦࡰࡢࡩࡨࠤࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠧୌ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1ll1ll1lll_opy_)
            if bstack11l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ୍࠭") in CONFIG and str(CONFIG[bstack11l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ୎")]).lower() != bstack11l11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪ୏"):
                cdpUrl = bstack1l1ll1ll11_opy_()
                LAUNCH_PATCH_ROBOT_PLAYWRIGHT = bstack11l11_opy_ (u"ࠬ࠭ࠧࠋ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࠎࡨࡵ࡮ࡴࡶࠣࡦࡸࡺࡡࡤ࡭ࡢࡴࡦࡺࡨࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࡝ࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠷ࡢࡁࠊࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡣࡢࡲࡶࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠱࡞࠽ࠍࡧࡴࡴࡳࡵࠢࡳࡣ࡮ࡴࡤࡦࡺࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠸࡝࠼ࠌࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰ࡶࡰ࡮ࡩࡥࠩ࠲࠯ࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹ࠩ࠼ࠌࡦࡳࡳࡹࡴࠡ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢࠪ࠽ࠍ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡰࡦࡻ࡮ࡤࡪࠣࡁࠥࡧࡳࡺࡰࡦࠤ࠭ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷ࠮ࠦ࠽࠿ࠢࡾࡿࠏࠦࠠ࡭ࡧࡷࠤࡨࡧࡰࡴ࠽ࠍࠤࠥࡺࡲࡺࠢࡾࡿࠏࠦࠠࠡࠢࡦࡥࡵࡹࠠ࠾ࠢࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࡢࡴࡶࡤࡧࡰࡥࡣࡢࡲࡶ࠭ࡀࠐࠠࠡࡿࢀࠤࡨࡧࡴࡤࡪࠣࠬࡪࡾࠩࠡࡽࡾࠎࠥࠦࠠࠡࡥࡲࡲࡸࡵ࡬ࡦ࠰ࡨࡶࡷࡵࡲࠩࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵ࠽ࠦ࠱ࠦࡥࡹࠫ࠾ࠎࠥࠦࡽࡾࠌࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࢁࠊࠡࠢࠣࠤࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࠻ࠢࠪࡿࡨࡪࡰࡖࡴ࡯ࢁࠬࠦࠫࠡࡧࡱࡧࡴࡪࡥࡖࡔࡌࡇࡴࡳࡰࡰࡰࡨࡲࡹ࠮ࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡤࡣࡳࡷ࠮࠯ࠬࠋࠢࠣࠤࠥ࠴࠮࠯࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠋࠢࠣࢁࢂ࠯࠻ࠋࡿࢀ࠿ࠏࡩ࡯࡯ࡵࡷࠤࡴࡸࡩࡨ࡫ࡱࡥࡱࡥࡣࡰࡰࡱࡩࡨࡺࠠ࠾ࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱ࠮ࡤࡪࡵࡳࡲ࡯ࡵ࡮࠰ࡦࡳࡳࡴࡥࡤࡶ࠱ࡦ࡮ࡴࡤࠩ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭ࠪ࠽ࠍ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷࠤࡂࠦࡡࡴࡻࡱࡧࠥ࠮ࡣࡰࡰࡱࡩࡨࡺࡏࡱࡶ࡬ࡳࡳࡹࠩࠡ࠿ࡁࠤࢀࢁࠊࠡࠢ࡯ࡩࡹࠦࡣࡢࡲࡶ࠿ࠏࠦࠠࡵࡴࡼࠤࢀࢁࠊࠡࠢࠣࠤࡨࡧࡰࡴࠢࡀࠤࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸ࠯࠻ࠋࠢࠣࢁࢂࠦࡣࡢࡶࡦ࡬ࠥ࠮ࡥࡹࠫࠣࡿࢀࠐࠠࠡࡿࢀࠎࠥࠦࡣࡰࡰࡶࡸࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࡅ࡯ࡦࡳࡳ࡮ࡴࡴࠡ࠿ࠣࠫࢀࡩࡤࡱࡗࡵࡰࢂ࠭ࠠࠬࠢࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩ࠼ࠌࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣࡳࡷ࡯ࡧࡪࡰࡤࡰࡤࡩ࡯࡯ࡰࡨࡧࡹ࠮ࡻࡼࠌࠣࠤࠥࠦ࠮࠯࠰ࡦࡳࡳࡴࡥࡤࡶࡒࡴࡹ࡯࡯࡯ࡵ࠯ࠎࠥࠦࠠࠡࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸ࠿ࠦ࡭ࡰࡦ࡬ࡪ࡮࡫ࡤࡆࡰࡧࡴࡴ࡯࡮ࡵࠌࠣࠤࢂࢃࠩ࠼ࠌࢀࢁࡀࠐ࠯ࠫࠢࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࠦࠪ࠰ࠌࠪࠫࠬ୐").format(cdpUrl=cdpUrl)
            lines.insert(1, LAUNCH_PATCH_ROBOT_PLAYWRIGHT)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack11l11_opy_ (u"ࠨࡩ࡯ࡦࡨࡼࡤࡨࡳࡵࡣࡦ࡯࠳ࡰࡳࠣ୑")), bstack11l11_opy_ (u"ࠧࡸࠩ୒")) as bstack11llll1l1l_opy_:
              bstack11llll1l1l_opy_.writelines(lines)
        CONFIG[bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ୓")] = str(bstack11l1111ll1_opy_) + str(__version__)
        bstack1ll11ll1l_opy_ = os.environ[bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ୔")]
        bstack111ll1ll1l_opy_ = bstack1l11l1l1l1_opy_.bstack11l1ll11l_opy_(CONFIG, bstack11l1111ll1_opy_)
        CONFIG[bstack11l11_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭୕")] = bstack1ll11ll1l_opy_
        CONFIG[bstack11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ୖ")] = bstack111ll1ll1l_opy_
        bstack11lllll1l1_opy_ = 0 if bstack111llll1ll_opy_ < 0 else bstack111llll1ll_opy_
        try:
          if bstack11lllll1l_opy_ is True:
            bstack11lllll1l1_opy_ = int(multiprocessing.current_process().name)
          elif bstack111l1111ll_opy_ is True:
            bstack11lllll1l1_opy_ = int(threading.current_thread().name)
        except:
          bstack11lllll1l1_opy_ = 0
        CONFIG[bstack11l11_opy_ (u"ࠧࡻࡳࡦ࡙࠶ࡇࠧୗ")] = False
        CONFIG[bstack11l11_opy_ (u"ࠨࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧ୘")] = True
        bstack11ll1ll1_opy_ = bstack1lll111l1_opy_(CONFIG, bstack11lllll1l1_opy_)
        logger.debug(bstack1l11ll1ll_opy_.format(str(bstack11ll1ll1_opy_)))
        if CONFIG.get(bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ୙")):
          bstack1l1111l111_opy_(bstack11ll1ll1_opy_)
          bstack11ll1ll1_opy_[bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ୚")] = os.environ[bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ୛")]
        if bstack11l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ଡ଼") in CONFIG and bstack11l11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩଢ଼") in CONFIG[bstack11l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ୞")][bstack11lllll1l1_opy_]:
          bstack11l1111lll_opy_ = CONFIG[bstack11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩୟ")][bstack11lllll1l1_opy_][bstack11l11_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬୠ")]
        args.append(os.path.join(os.path.expanduser(bstack11l11_opy_ (u"ࠨࢀࠪୡ")), bstack11l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩୢ"), bstack11l11_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬୣ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack11ll1ll1_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack11l11_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨ୤"))
      bstack1l1lllll_opy_ = True
      return bstack1ll1111l1l_opy_(self, args, **kwargs)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack11ll11ll1_opy_(self,
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
    global bstack111llll1ll_opy_
    global bstack11l1111lll_opy_
    global bstack11lllll1l_opy_
    global bstack111l1111ll_opy_
    global bstack11l1111ll1_opy_
    CONFIG[bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ୥")] = str(bstack11l1111ll1_opy_) + str(__version__)
    bstack1ll11ll1l_opy_ = os.environ[bstack11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ୦")]
    bstack111ll1ll1l_opy_ = bstack1l11l1l1l1_opy_.bstack11l1ll11l_opy_(CONFIG, bstack11l1111ll1_opy_)
    CONFIG[bstack11l11_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ୧")] = bstack1ll11ll1l_opy_
    CONFIG[bstack11l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ୨")] = bstack111ll1ll1l_opy_
    bstack11lllll1l1_opy_ = 0 if bstack111llll1ll_opy_ < 0 else bstack111llll1ll_opy_
    try:
      if bstack11lllll1l_opy_ is True:
        bstack11lllll1l1_opy_ = int(multiprocessing.current_process().name)
      elif bstack111l1111ll_opy_ is True:
        bstack11lllll1l1_opy_ = int(threading.current_thread().name)
    except:
      bstack11lllll1l1_opy_ = 0
    CONFIG[bstack11l11_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ୩")] = True
    bstack11ll1ll1_opy_ = bstack1lll111l1_opy_(CONFIG, bstack11lllll1l1_opy_)
    logger.debug(bstack1l11ll1ll_opy_.format(str(bstack11ll1ll1_opy_)))
    if CONFIG.get(bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ୪")):
      bstack1l1111l111_opy_(bstack11ll1ll1_opy_)
    if bstack11l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ୫") in CONFIG and bstack11l11_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ୬") in CONFIG[bstack11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ୭")][bstack11lllll1l1_opy_]:
      bstack11l1111lll_opy_ = CONFIG[bstack11l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ୮")][bstack11lllll1l1_opy_][bstack11l11_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭୯")]
    import urllib
    import json
    if bstack11l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭୰") in CONFIG and str(CONFIG[bstack11l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧୱ")]).lower() != bstack11l11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪ୲"):
        bstack1lll1l1l11_opy_ = bstack1l1ll1ll11_opy_()
        cdpUrl = bstack1lll1l1l11_opy_ + urllib.parse.quote(json.dumps(bstack11ll1ll1_opy_))
    else:
        cdpUrl = bstack11l11_opy_ (u"ࠬࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠧ୳") + urllib.parse.quote(json.dumps(bstack11ll1ll1_opy_))
    browser = self.connect(cdpUrl)
    return browser
except Exception as e:
    pass
def bstack11l111llll_opy_():
    global bstack1l1lllll_opy_
    global bstack11l1111ll1_opy_
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l111lll_opy_
        global bstack11l1l1111_opy_
        if not bstack111l1l11_opy_:
          global bstack11llllll11_opy_
          if not bstack11llllll11_opy_:
            from bstack_utils.helper import bstack1ll1llll11_opy_, bstack1l1lll1l_opy_, bstack1l1l1llll1_opy_
            bstack11llllll11_opy_ = bstack1ll1llll11_opy_()
            bstack1l1lll1l_opy_(bstack11l1111ll1_opy_)
            bstack111ll1ll1l_opy_ = bstack1l11l1l1l1_opy_.bstack11l1ll11l_opy_(CONFIG, bstack11l1111ll1_opy_)
            bstack11l1l1111_opy_.bstack1ll111ll11_opy_(bstack11l11_opy_ (u"ࠨࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡔࡗࡕࡄࡖࡅࡗࡣࡒࡇࡐࠣ୴"), bstack111ll1ll1l_opy_)
          BrowserType.connect = bstack1l111lll_opy_
          return
        BrowserType.launch = bstack11ll11ll1_opy_
        bstack1l1lllll_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1lll11llll_opy_
      bstack1l1lllll_opy_ = True
    except Exception as e:
      pass
def bstack1111llll_opy_(context, bstack11l1llll1_opy_):
  try:
    if getattr(context, bstack11l11_opy_ (u"ࠧࡱࡣࡪࡩࠬ୵"), None):
      context.page.evaluate(bstack11l11_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ୶"), bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿࠭୷")+ json.dumps(bstack11l1llll1_opy_) + bstack11l11_opy_ (u"ࠥࢁࢂࠨ୸"))
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡻࡾ࠼ࠣࡿࢂࠨ୹").format(str(e), traceback.format_exc()))
def bstack11l1l11ll_opy_(context, message, level):
  try:
    if getattr(context, bstack11l11_opy_ (u"ࠬࡶࡡࡨࡧࠪ୺"), None):
      context.page.evaluate(bstack11l11_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢ୻"), bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ୼") + json.dumps(message) + bstack11l11_opy_ (u"ࠨ࠮ࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠫ୽") + json.dumps(level) + bstack11l11_opy_ (u"ࠩࢀࢁࠬ୾"))
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡡ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠣࡿࢂࡀࠠࡼࡿࠥ୿").format(str(e), traceback.format_exc()))
@measure(event_name=EVENTS.bstack1lll11111_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l111l11l_opy_=bstack11l1111lll_opy_)
def bstack1ll1l1l111_opy_(self, url):
  global bstack11ll11ll_opy_
  try:
    bstack1ll111ll1_opy_(url)
  except Exception as err:
    logger.debug(bstack1l1ll11l_opy_.format(str(err)))
  try:
    bstack11ll11ll_opy_(self, url)
  except Exception as e:
    try:
      bstack111lll11l1_opy_ = str(e)
      if any(err_msg in bstack111lll11l1_opy_ for err_msg in bstack11ll11l1l1_opy_):
        bstack1ll111ll1_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1l1ll11l_opy_.format(str(err)))
    raise e
def bstack1ll11l1l1_opy_(self):
  global bstack11llll1111_opy_
  bstack11llll1111_opy_ = self
  return
def bstack11lll1llll_opy_(self):
  global bstack11l11l11l1_opy_
  bstack11l11l11l1_opy_ = self
  return
def bstack11ll1l11_opy_(test_name, bstack1l11llll11_opy_):
  global CONFIG
  if percy.bstack1l1l1l1111_opy_() == bstack11l11_opy_ (u"ࠦࡹࡸࡵࡦࠤ஀"):
    bstack1l1lll11_opy_ = os.path.relpath(bstack1l11llll11_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack1l1lll11_opy_)
    bstack11l111l11l_opy_ = suite_name + bstack11l11_opy_ (u"ࠧ࠳ࠢ஁") + test_name
    threading.current_thread().percySessionName = bstack11l111l11l_opy_
def bstack1l1111ll1l_opy_(self, test, *args, **kwargs):
  global bstack111ll1lll1_opy_
  test_name = None
  bstack1l11llll11_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1l11llll11_opy_ = str(test.source)
  bstack11ll1l11_opy_(test_name, bstack1l11llll11_opy_)
  bstack111ll1lll1_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.bstack1111lll11l_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l111l11l_opy_=bstack11l1111lll_opy_)
def bstack11lll111l1_opy_(driver, bstack11l111l11l_opy_):
  if not bstack1llllllll1_opy_ and bstack11l111l11l_opy_:
      bstack1lll1l11_opy_ = {
          bstack11l11_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭ஂ"): bstack11l11_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨஃ"),
          bstack11l11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ஄"): {
              bstack11l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧஅ"): bstack11l111l11l_opy_
          }
      }
      bstack1l1l111111_opy_ = bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨஆ").format(json.dumps(bstack1lll1l11_opy_))
      driver.execute_script(bstack1l1l111111_opy_)
  if bstack1l11ll11_opy_:
      bstack1ll1l1l1l_opy_ = {
          bstack11l11_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫஇ"): bstack11l11_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧஈ"),
          bstack11l11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩஉ"): {
              bstack11l11_opy_ (u"ࠧࡥࡣࡷࡥࠬஊ"): bstack11l111l11l_opy_ + bstack11l11_opy_ (u"ࠨࠢࡳࡥࡸࡹࡥࡥࠣࠪ஋"),
              bstack11l11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ஌"): bstack11l11_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨ஍")
          }
      }
      if bstack1l11ll11_opy_.status == bstack11l11_opy_ (u"ࠫࡕࡇࡓࡔࠩஎ"):
          bstack1ll1lll1_opy_ = bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪஏ").format(json.dumps(bstack1ll1l1l1l_opy_))
          driver.execute_script(bstack1ll1lll1_opy_)
          bstack1ll1l1l1_opy_(driver, bstack11l11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ஐ"))
      elif bstack1l11ll11_opy_.status == bstack11l11_opy_ (u"ࠧࡇࡃࡌࡐࠬ஑"):
          reason = bstack11l11_opy_ (u"ࠣࠤஒ")
          bstack1l111111_opy_ = bstack11l111l11l_opy_ + bstack11l11_opy_ (u"ࠩࠣࡪࡦ࡯࡬ࡦࡦࠪஓ")
          if bstack1l11ll11_opy_.message:
              reason = str(bstack1l11ll11_opy_.message)
              bstack1l111111_opy_ = bstack1l111111_opy_ + bstack11l11_opy_ (u"ࠪࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲ࠻ࠢࠪஔ") + reason
          bstack1ll1l1l1l_opy_[bstack11l11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧக")] = {
              bstack11l11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ஖"): bstack11l11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ஗"),
              bstack11l11_opy_ (u"ࠧࡥࡣࡷࡥࠬ஘"): bstack1l111111_opy_
          }
          bstack1ll1lll1_opy_ = bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ங").format(json.dumps(bstack1ll1l1l1l_opy_))
          driver.execute_script(bstack1ll1lll1_opy_)
          bstack1ll1l1l1_opy_(driver, bstack11l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩச"), reason)
          bstack111111111_opy_(reason, str(bstack1l11ll11_opy_), str(bstack111llll1ll_opy_), logger)
@measure(event_name=EVENTS.bstack1ll111lll_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l111l11l_opy_=bstack11l1111lll_opy_)
def bstack1l11111l11_opy_(driver, test):
  if percy.bstack1l1l1l1111_opy_() == bstack11l11_opy_ (u"ࠥࡸࡷࡻࡥࠣ஛") and percy.bstack1lllll11l1_opy_() == bstack11l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨஜ"):
      bstack1l1l1l1ll_opy_ = bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ஝"), None)
      bstack111lllll11_opy_(driver, bstack1l1l1l1ll_opy_, test)
  if (bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪஞ"), None) and
      bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ட"), None)) or (
      bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ஠"), None) and
      bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ஡"), None)):
      logger.info(bstack11l11_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠡࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡭ࡸࠦࡵ࡯ࡦࡨࡶࡼࡧࡹ࠯ࠢࠥ஢"))
      bstack1lllll111l_opy_.bstack1ll1l111l1_opy_(driver, name=test.name, path=test.source)
def bstack1l111l11l1_opy_(test, bstack11l111l11l_opy_):
    try:
      bstack1lllll111_opy_ = datetime.datetime.now()
      data = {}
      if test:
        data[bstack11l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩண")] = bstack11l111l11l_opy_
      if bstack1l11ll11_opy_:
        if bstack1l11ll11_opy_.status == bstack11l11_opy_ (u"ࠬࡖࡁࡔࡕࠪத"):
          data[bstack11l11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭஥")] = bstack11l11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ஦")
        elif bstack1l11ll11_opy_.status == bstack11l11_opy_ (u"ࠨࡈࡄࡍࡑ࠭஧"):
          data[bstack11l11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩந")] = bstack11l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪன")
          if bstack1l11ll11_opy_.message:
            data[bstack11l11_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫப")] = str(bstack1l11ll11_opy_.message)
      user = CONFIG[bstack11l11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ஫")]
      key = CONFIG[bstack11l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ஬")]
      host = bstack1l11l1llll_opy_(cli.config, [bstack11l11_opy_ (u"ࠢࡢࡲ࡬ࡷࠧ஭"), bstack11l11_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧࠥம"), bstack11l11_opy_ (u"ࠤࡤࡴ࡮ࠨய")], bstack11l11_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠦர"))
      url = bstack11l11_opy_ (u"ࠫࢀࢃ࠯ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡶࡩࡸࡹࡩࡰࡰࡶ࠳ࢀࢃ࠮࡫ࡵࡲࡲࠬற").format(host, bstack1111ll1l1_opy_)
      headers = {
        bstack11l11_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫல"): bstack11l11_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩள"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers, auth=(user, key))
        cli.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠢࡩࡶࡷࡴ࠿ࡻࡰࡥࡣࡷࡩࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡸࡺࡡࡵࡷࡶࠦழ"), datetime.datetime.now() - bstack1lllll111_opy_)
    except Exception as e:
      logger.error(bstack1ll1ll11l1_opy_.format(str(e)))
def bstack11ll11llll_opy_(test, bstack11l111l11l_opy_):
  global CONFIG
  global bstack11l11l11l1_opy_
  global bstack11llll1111_opy_
  global bstack1111ll1l1_opy_
  global bstack1l11ll11_opy_
  global bstack11l1111lll_opy_
  global bstack11ll1l1l1_opy_
  global bstack1llll1ll_opy_
  global bstack1ll1ll1l1l_opy_
  global bstack11l111l1l1_opy_
  global bstack111l1llll1_opy_
  global bstack11l11lll1l_opy_
  global bstack1l1ll1l11_opy_
  try:
    if not bstack1111ll1l1_opy_:
      with bstack1l1ll1l11_opy_:
        bstack1l111lllll_opy_ = os.path.join(os.path.expanduser(bstack11l11_opy_ (u"ࠨࢀࠪவ")), bstack11l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩஶ"), bstack11l11_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬஷ"))
        if os.path.exists(bstack1l111lllll_opy_):
          with open(bstack1l111lllll_opy_, bstack11l11_opy_ (u"ࠫࡷ࠭ஸ")) as f:
            content = f.read().strip()
            if content:
              bstack1l111ll1l1_opy_ = json.loads(bstack11l11_opy_ (u"ࠧࢁࠢஹ") + content + bstack11l11_opy_ (u"࠭ࠢࡹࠤ࠽ࠤࠧࡿࠢࠨ஺") + bstack11l11_opy_ (u"ࠢࡾࠤ஻"))
              bstack1111ll1l1_opy_ = bstack1l111ll1l1_opy_.get(str(threading.get_ident()))
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡳࡧࡤࡨ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡌࡈࡸࠦࡦࡪ࡮ࡨ࠾ࠥ࠭஼") + str(e))
  if not is_robot_playwright_installed():
    if bstack111l1llll1_opy_:
      with bstack1ll1ll1l1_opy_:
        bstack11111ll1l_opy_ = bstack111l1llll1_opy_.copy()
      for driver in bstack11111ll1l_opy_:
        if bstack1111ll1l1_opy_ == driver.session_id:
          if test:
            bstack1l11111l11_opy_(driver, test)
          bstack11lll111l1_opy_(driver, bstack11l111l11l_opy_)
    elif bstack1111ll1l1_opy_:
      bstack1l111l11l1_opy_(test, bstack11l111l11l_opy_)
    if bstack11l11l11l1_opy_:
      bstack1llll1ll_opy_(bstack11l11l11l1_opy_)
    if bstack11llll1111_opy_:
      bstack1ll1ll1l1l_opy_(bstack11llll1111_opy_)
    if bstack1l1ll1lll1_opy_:
      bstack11l111l1l1_opy_()
def bstack1l1l11l1ll_opy_(self, test, *args, **kwargs):
  bstack11l111l11l_opy_ = None
  if test:
    bstack11l111l11l_opy_ = str(test.name)
  bstack11ll11llll_opy_(test, bstack11l111l11l_opy_)
  bstack11ll1l1l1_opy_(self, test, *args, **kwargs)
def bstack1ll11l11_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack11ll1l1111_opy_
  global CONFIG
  global bstack111l1llll1_opy_
  global bstack1111ll1l1_opy_
  global bstack1l1ll1l11_opy_
  bstack111l11111_opy_ = None
  try:
    if bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ஽"), None) or bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬா"), None):
      try:
        if not bstack1111ll1l1_opy_:
          bstack1l111lllll_opy_ = os.path.join(os.path.expanduser(bstack11l11_opy_ (u"ࠫࢃ࠭ி")), bstack11l11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬீ"), bstack11l11_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨு"))
          with bstack1l1ll1l11_opy_:
            if os.path.exists(bstack1l111lllll_opy_):
              with open(bstack1l111lllll_opy_, bstack11l11_opy_ (u"ࠧࡳࠩூ")) as f:
                content = f.read().strip()
                if content:
                  bstack1l111ll1l1_opy_ = json.loads(bstack11l11_opy_ (u"ࠣࡽࠥ௃") + content + bstack11l11_opy_ (u"ࠩࠥࡼࠧࡀࠠࠣࡻࠥࠫ௄") + bstack11l11_opy_ (u"ࠥࢁࠧ௅"))
                  bstack1111ll1l1_opy_ = bstack1l111ll1l1_opy_.get(str(threading.get_ident()))
      except Exception as e:
        logger.debug(bstack11l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡶࡪࡧࡤࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡏࡄࡴࠢࡩ࡭ࡱ࡫ࠠࡪࡰࠣࡸࡪࡹࡴࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࠪெ") + str(e))
      if bstack111l1llll1_opy_:
        with bstack1ll1ll1l1_opy_:
          bstack11111ll1l_opy_ = bstack111l1llll1_opy_.copy()
        for driver in bstack11111ll1l_opy_:
          if bstack1111ll1l1_opy_ == driver.session_id:
            bstack111l11111_opy_ = driver
    bstack1l11l111l_opy_ = bstack1lllll111l_opy_.bstack11l11l1lll_opy_(test.tags)
    if bstack111l11111_opy_:
      threading.current_thread().isA11yTest = bstack1lllll111l_opy_.bstack11l1l11ll1_opy_(bstack111l11111_opy_, bstack1l11l111l_opy_)
      threading.current_thread().isAppA11yTest = bstack1lllll111l_opy_.bstack11l1l11ll1_opy_(bstack111l11111_opy_, bstack1l11l111l_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1l11l111l_opy_
      threading.current_thread().isAppA11yTest = bstack1l11l111l_opy_
  except:
    pass
  bstack11ll1l1111_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1l11ll11_opy_
  try:
    bstack1l11ll11_opy_ = self._test
  except:
    bstack1l11ll11_opy_ = self.test
def bstack1llll1llll_opy_():
  global bstack111ll11l1l_opy_
  try:
    if os.path.exists(bstack111ll11l1l_opy_):
      os.remove(bstack111ll11l1l_opy_)
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨே") + str(e))
def bstack1l11ll11l_opy_():
  global bstack111ll11l1l_opy_
  bstack1l1ll1l1_opy_ = {}
  lock_file = bstack111ll11l1l_opy_ + bstack11l11_opy_ (u"࠭࠮࡭ࡱࡦ࡯ࠬை")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack11l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡱࡵࡣ࡬ࠢࡱࡳࡹࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦ࠮ࠣࡹࡸ࡯࡮ࡨࠢࡥࡥࡸ࡯ࡣࠡࡨ࡬ࡰࡪࠦ࡯ࡱࡧࡵࡥࡹ࡯࡯࡯ࡵࠪ௉"))
    try:
      if not os.path.isfile(bstack111ll11l1l_opy_):
        with open(bstack111ll11l1l_opy_, bstack11l11_opy_ (u"ࠨࡹࠪொ")) as f:
          json.dump({}, f)
      if os.path.exists(bstack111ll11l1l_opy_):
        with open(bstack111ll11l1l_opy_, bstack11l11_opy_ (u"ࠩࡵࠫோ")) as f:
          content = f.read().strip()
          if content:
            bstack1l1ll1l1_opy_ = json.loads(content)
    except Exception as e:
      logger.debug(bstack11l11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡸࡥࡢࡦ࡬ࡲ࡬ࠦࡲࡰࡤࡲࡸࠥࡸࡥࡱࡱࡵࡸࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬௌ") + str(e))
    return bstack1l1ll1l1_opy_
  try:
    os.makedirs(os.path.dirname(bstack111ll11l1l_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      if not os.path.isfile(bstack111ll11l1l_opy_):
        with open(bstack111ll11l1l_opy_, bstack11l11_opy_ (u"ࠫࡼ்࠭")) as f:
          json.dump({}, f)
      if os.path.exists(bstack111ll11l1l_opy_):
        with open(bstack111ll11l1l_opy_, bstack11l11_opy_ (u"ࠬࡸࠧ௎")) as f:
          content = f.read().strip()
          if content:
            bstack1l1ll1l1_opy_ = json.loads(content)
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡴࡨࡥࡩ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨ௏") + str(e))
  finally:
    return bstack1l1ll1l1_opy_
def bstack11ll111ll_opy_(platform_index, item_index):
  global bstack111ll11l1l_opy_
  lock_file = bstack111ll11l1l_opy_ + bstack11l11_opy_ (u"ࠧ࠯࡮ࡲࡧࡰ࠭ௐ")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack11l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡲ࡯ࡤ࡭ࠣࡲࡴࡺࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧ࠯ࠤࡺࡹࡩ࡯ࡩࠣࡦࡦࡹࡩࡤࠢࡩ࡭ࡱ࡫ࠠࡰࡲࡨࡶࡦࡺࡩࡰࡰࡶࠫ௑"))
    try:
      bstack1l1ll1l1_opy_ = {}
      if os.path.exists(bstack111ll11l1l_opy_):
        with open(bstack111ll11l1l_opy_, bstack11l11_opy_ (u"ࠩࡵࠫ௒")) as f:
          content = f.read().strip()
          if content:
            bstack1l1ll1l1_opy_ = json.loads(content)
      bstack1l1ll1l1_opy_[item_index] = platform_index
      with open(bstack111ll11l1l_opy_, bstack11l11_opy_ (u"ࠥࡻࠧ௓")) as outfile:
        json.dump(bstack1l1ll1l1_opy_, outfile)
    except Exception as e:
      logger.debug(bstack11l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡷࡳ࡫ࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺ࠡࠩ௔") + str(e))
    return
  try:
    os.makedirs(os.path.dirname(bstack111ll11l1l_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      bstack1l1ll1l1_opy_ = {}
      if os.path.exists(bstack111ll11l1l_opy_):
        with open(bstack111ll11l1l_opy_, bstack11l11_opy_ (u"ࠬࡸࠧ௕")) as f:
          content = f.read().strip()
          if content:
            bstack1l1ll1l1_opy_ = json.loads(content)
      bstack1l1ll1l1_opy_[item_index] = platform_index
      with open(bstack111ll11l1l_opy_, bstack11l11_opy_ (u"ࠨࡷࠣ௖")) as outfile:
        json.dump(bstack1l1ll1l1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡺࡶ࡮ࡺࡩ࡯ࡩࠣࡸࡴࠦࡲࡰࡤࡲࡸࠥࡸࡥࡱࡱࡵࡸࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬௗ") + str(e))
def bstack1ll11l1ll1_opy_(bstack11lll1ll11_opy_):
  global CONFIG
  bstack1ll111l1ll_opy_ = bstack11l11_opy_ (u"ࠨࠩ௘")
  if not bstack11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ௙") in CONFIG:
    logger.info(bstack11l11_opy_ (u"ࠪࡒࡴࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠢࡳࡥࡸࡹࡥࡥࠢࡸࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡳࡧࡳࡳࡷࡺࠠࡧࡱࡵࠤࡗࡵࡢࡰࡶࠣࡶࡺࡴࠧ௚"))
  try:
    platform = CONFIG[bstack11l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ௛")][bstack11lll1ll11_opy_]
    if bstack11l11_opy_ (u"ࠬࡵࡳࠨ௜") in platform:
      bstack1ll111l1ll_opy_ += str(platform[bstack11l11_opy_ (u"࠭࡯ࡴࠩ௝")]) + bstack11l11_opy_ (u"ࠧ࠭ࠢࠪ௞")
    if bstack11l11_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫ௟") in platform:
      bstack1ll111l1ll_opy_ += str(platform[bstack11l11_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬ௠")]) + bstack11l11_opy_ (u"ࠪ࠰ࠥ࠭௡")
    if bstack11l11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨ௢") in platform:
      bstack1ll111l1ll_opy_ += str(platform[bstack11l11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩ௣")]) + bstack11l11_opy_ (u"࠭ࠬࠡࠩ௤")
    if bstack11l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ௥") in platform:
      bstack1ll111l1ll_opy_ += str(platform[bstack11l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪ௦")]) + bstack11l11_opy_ (u"ࠩ࠯ࠤࠬ௧")
    if bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ௨") in platform:
      bstack1ll111l1ll_opy_ += str(platform[bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ௩")]) + bstack11l11_opy_ (u"ࠬ࠲ࠠࠨ௪")
    if bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ௫") in platform:
      bstack1ll111l1ll_opy_ += str(platform[bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ௬")]) + bstack11l11_opy_ (u"ࠨ࠮ࠣࠫ௭")
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"ࠩࡖࡳࡲ࡫ࠠࡦࡴࡵࡳࡷࠦࡩ࡯ࠢࡪࡩࡳ࡫ࡲࡢࡶ࡬ࡲ࡬ࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡵࡷࡶ࡮ࡴࡧࠡࡨࡲࡶࠥࡸࡥࡱࡱࡵࡸࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡯࡯࡯ࠩ௮") + str(e))
  finally:
    if bstack1ll111l1ll_opy_[len(bstack1ll111l1ll_opy_) - 2:] == bstack11l11_opy_ (u"ࠪ࠰ࠥ࠭௯"):
      bstack1ll111l1ll_opy_ = bstack1ll111l1ll_opy_[:-2]
    return bstack1ll111l1ll_opy_
def bstack1l1lll1ll_opy_(path, bstack1ll111l1ll_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1ll11lll1l_opy_ = ET.parse(path)
    bstack11lll1l1l_opy_ = bstack1ll11lll1l_opy_.getroot()
    bstack111111l1_opy_ = None
    for suite in bstack11lll1l1l_opy_.iter(bstack11l11_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪ௰")):
      if bstack11l11_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ௱") in suite.attrib:
        suite.attrib[bstack11l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ௲")] += bstack11l11_opy_ (u"ࠧࠡࠩ௳") + bstack1ll111l1ll_opy_
        bstack111111l1_opy_ = suite
    bstack1lll11111l_opy_ = None
    for robot in bstack11lll1l1l_opy_.iter(bstack11l11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ௴")):
      bstack1lll11111l_opy_ = robot
    bstack11l1ll1l11_opy_ = len(bstack1lll11111l_opy_.findall(bstack11l11_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨ௵")))
    if bstack11l1ll1l11_opy_ == 1:
      bstack1lll11111l_opy_.remove(bstack1lll11111l_opy_.findall(bstack11l11_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩ௶"))[0])
      bstack1ll1l11ll_opy_ = ET.Element(bstack11l11_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪ௷"), attrib={bstack11l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ௸"): bstack11l11_opy_ (u"࠭ࡓࡶ࡫ࡷࡩࡸ࠭௹"), bstack11l11_opy_ (u"ࠧࡪࡦࠪ௺"): bstack11l11_opy_ (u"ࠨࡵ࠳ࠫ௻")})
      bstack1lll11111l_opy_.insert(1, bstack1ll1l11ll_opy_)
      bstack1llll111ll_opy_ = None
      for suite in bstack1lll11111l_opy_.iter(bstack11l11_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨ௼")):
        bstack1llll111ll_opy_ = suite
      bstack1llll111ll_opy_.append(bstack111111l1_opy_)
      bstack11l111ll_opy_ = None
      for status in bstack111111l1_opy_.iter(bstack11l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ௽")):
        bstack11l111ll_opy_ = status
      bstack1llll111ll_opy_.append(bstack11l111ll_opy_)
    bstack1ll11lll1l_opy_.write(path)
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡢࡴࡶ࡭ࡳ࡭ࠠࡸࡪ࡬ࡰࡪࠦࡧࡦࡰࡨࡶࡦࡺࡩ࡯ࡩࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠩ௾") + str(e))
def bstack1l111l11ll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack11l1ll1l1_opy_
  global CONFIG
  if bstack11l11_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡵࡧࡴࡩࠤ௿") in options:
    del options[bstack11l11_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡶࡡࡵࡪࠥఀ")]
  bstack11l1l11l_opy_ = bstack1l11ll11l_opy_()
  for item_id in bstack11l1l11l_opy_.keys():
    path = os.path.join(outs_dir, str(item_id), bstack11l11_opy_ (u"ࠧࡰࡷࡷࡴࡺࡺ࠮ࡹ࡯࡯ࠫఁ"))
    bstack1l1lll1ll_opy_(path, bstack1ll11l1ll1_opy_(bstack11l1l11l_opy_[item_id]))
  bstack1llll1llll_opy_()
  return bstack11l1ll1l1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1ll111l1l_opy_(self, ff_profile_dir):
  global bstack111llll11l_opy_
  if not ff_profile_dir:
    return None
  return bstack111llll11l_opy_(self, ff_profile_dir)
def bstack111l111l1l_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1l1lll1l11_opy_
  bstack111l1l11l_opy_ = []
  if bstack11l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫం") in CONFIG:
    bstack111l1l11l_opy_ = CONFIG[bstack11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬః")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack11l11_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࠦఄ")],
      pabot_args[bstack11l11_opy_ (u"ࠦࡻ࡫ࡲࡣࡱࡶࡩࠧఅ")],
      argfile,
      pabot_args.get(bstack11l11_opy_ (u"ࠧ࡮ࡩࡷࡧࠥఆ")),
      pabot_args[bstack11l11_opy_ (u"ࠨࡰࡳࡱࡦࡩࡸࡹࡥࡴࠤఇ")],
      platform[0],
      bstack1l1lll1l11_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack11l11_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡨ࡬ࡰࡪࡹࠢఈ")] or [(bstack11l11_opy_ (u"ࠣࠤఉ"), None)]
    for platform in enumerate(bstack111l1l11l_opy_)
  ]
def bstack111ll1l1ll_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1lll11l11_opy_=bstack11l11_opy_ (u"ࠩࠪఊ")):
  global bstack111l1l111_opy_
  self.platform_index = platform_index
  self.bstack1ll11111_opy_ = bstack1lll11l11_opy_
  bstack111l1l111_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1l11ll11ll_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1l1l1ll1ll_opy_
  global bstack111lll11_opy_
  bstack1ll1lll11l_opy_ = copy.deepcopy(item)
  if not bstack11l11_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬఋ") in item.options:
    bstack1ll1lll11l_opy_.options[bstack11l11_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ఌ")] = []
  bstack1ll1l1lll1_opy_ = bstack1ll1lll11l_opy_.options[bstack11l11_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ఍")].copy()
  for v in bstack1ll1lll11l_opy_.options[bstack11l11_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨఎ")]:
    if bstack11l11_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝࠭ఏ") in v:
      bstack1ll1l1lll1_opy_.remove(v)
    if bstack11l11_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓࠨఐ") in v:
      bstack1ll1l1lll1_opy_.remove(v)
    if bstack11l11_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡆࡈࡊࡑࡕࡃࡂࡎࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭఑") in v:
      bstack1ll1l1lll1_opy_.remove(v)
  bstack1ll1l1lll1_opy_.insert(0, bstack11l11_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡓࡐࡆ࡚ࡆࡐࡔࡐࡍࡓࡊࡅ࡙࠼ࡾࢁࠬఒ").format(bstack1ll1lll11l_opy_.platform_index))
  bstack1ll1l1lll1_opy_.insert(0, bstack11l11_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒ࠻ࡽࢀࠫఓ").format(bstack1ll1lll11l_opy_.bstack1ll11111_opy_))
  bstack1ll1lll11l_opy_.options[bstack11l11_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧఔ")] = bstack1ll1l1lll1_opy_
  if bstack111lll11_opy_:
    bstack1ll1lll11l_opy_.options[bstack11l11_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨక")].insert(0, bstack11l11_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙࠺ࡼࡿࠪఖ").format(bstack111lll11_opy_))
  return bstack1l1l1ll1ll_opy_(caller_id, datasources, is_last, bstack1ll1lll11l_opy_, outs_dir)
def bstack11llllllll_opy_(command, item_index):
  try:
    if bstack11l1l1111_opy_.get_property(bstack11l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩగ")):
      os.environ[bstack11l11_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪఘ")] = json.dumps(CONFIG[bstack11l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ఙ")][item_index % bstack1ll1l111l_opy_])
    global bstack111lll11_opy_
    os.environ[bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫచ")] = str(item_index % bstack1ll1l111l_opy_)
    listener_arg = bstack11l11_opy_ (u"ࠬ࠭ఛ")
    if is_robot_playwright_installed() and cli.is_enabled(CONFIG):
      listener_arg = bstack11l11_opy_ (u"࠭ࠠ࠮࠯࡯࡭ࡸࡺࡥ࡯ࡧࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡷࡩࡱ࠮ࡳࡱࡥࡳࡹࡥ࡬ࡪࡵࡷࡩࡳ࡫ࡲࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠳ࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡒࡤࡸࡨ࡮ࡥࡳࠩజ")
      logger.debug(bstack11l11_opy_ (u"ࠢࡂࡦࡧ࡭ࡳ࡭ࠠࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡔࡦࡺࡣࡩࡧࡵࠤࡱ࡯ࡳࡵࡧࡱࡩࡷࠦࡦࡰࡴࠣ࡭ࡹ࡫࡭ࠡࡽࢀࠦఝ").format(item_index))
    if bstack111lll11_opy_:
      command[0] = command[0].replace(bstack11l11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧఞ"), bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠮ࡵࡧ࡯ࠥࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱࠦ࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࠢࠪట") + str(item_index % bstack1ll1l111l_opy_) + bstack11l11_opy_ (u"ࠪࠤ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠣࠫఠ") + str(
        item_index)  + listener_arg + bstack11l11_opy_ (u"ࠫࠥ࠭డ") + bstack111lll11_opy_, 1)
    else:
      command[0] = command[0].replace(bstack11l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫఢ"),
                                      bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡹࡤ࡬ࠢࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠣ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࠦࠧణ") +  str(item_index % bstack1ll1l111l_opy_) + bstack11l11_opy_ (u"ࠧࠡ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠠࠨత") + str(item_index)  + listener_arg, 1)
  except Exception as e:
    logger.error(bstack11l11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠ࡮ࡱࡧ࡭࡫ࡿࡩ࡯ࡩࠣࡧࡴࡳ࡭ࡢࡰࡧࠤ࡫ࡵࡲࠡࡲࡤࡦࡴࡺࠠࡳࡷࡱ࠾ࠥࢁࡽࠨథ").format(str(e)))
def bstack11l111111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack11l1l1ll_opy_
  try:
    bstack11llllllll_opy_(command, item_index)
    return bstack11l1l1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
  except Exception as e:
    logger.error(bstack11l11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡢࡰࡶࠣࡶࡺࡴ࠺ࠡࡽࢀࠫద").format(str(e)))
    raise e
def bstack1l11l1ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack11l1l1ll_opy_
  try:
    bstack11llllllll_opy_(command, item_index)
    return bstack11l1l1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
  except Exception as e:
    logger.error(bstack11l11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡣࡱࡷࠤࡷࡻ࡮ࠡ࠴࠱࠵࠸ࡀࠠࡼࡿࠪధ").format(str(e)))
    try:
      return bstack11l1l1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
    except Exception as e2:
      logger.error(bstack11l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡢࡤࡲࡸࠥ࠸࠮࠲࠵ࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࡻࡾࠩన").format(str(e2)))
      raise e
def bstack1ll11l11l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack11l1l1ll_opy_
  try:
    bstack11llllllll_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    return bstack11l1l1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
  except Exception as e:
    logger.error(bstack11l11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡥࡳࡹࠦࡲࡶࡰࠣ࠶࠳࠷࠵࠻ࠢࡾࢁࠬ఩").format(str(e)))
    try:
      return bstack11l1l1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
    except Exception as e2:
      logger.error(bstack11l11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠ࠳࠰࠴࠹ࠥ࡬ࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࡽࢀࠫప").format(str(e2)))
      raise e
def _1l11lll1l1_opy_(bstack11l11ll11l_opy_, item_index, process_timeout, sleep_before_start, bstack1l1l1l11ll_opy_):
  bstack11llllllll_opy_(bstack11l11ll11l_opy_, item_index)
  if process_timeout is None:
    process_timeout = 3600
  if sleep_before_start and sleep_before_start > 0:
    time.sleep(min(sleep_before_start, 5))
  return process_timeout
def bstack11lllll111_opy_(command, bstack111ll11l_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack11l1l1ll_opy_
  global bstack11ll1l11l_opy_
  global bstack111lll11_opy_
  try:
    for env_name, bstack11ll11l111_opy_ in bstack11ll1l11l_opy_.items():
      os.environ[env_name] = bstack11ll11l111_opy_
    bstack111lll11_opy_ = bstack11l11_opy_ (u"ࠢࠣఫ")
    bstack11llllllll_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    if sleep_before_start and sleep_before_start > 0:
      time.sleep(min(sleep_before_start, 5))
    return bstack11l1l1ll_opy_(command, bstack111ll11l_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack11l11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡦࡨ࡯ࡵࠢࡵࡹࡳࠦ࠵࠯࠲࠽ࠤࢀࢃࠧబ").format(str(e)))
    try:
      return bstack11l1l1ll_opy_(command, bstack111ll11l_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack11l11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡢࡰࡶࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࡻࡾࠩభ").format(str(e2)))
      raise e
def bstack1l1111lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack11l1l1ll_opy_
  try:
    process_timeout = _1l11lll1l1_opy_(command, item_index, process_timeout, sleep_before_start, bstack11l11_opy_ (u"ࠪ࠸࠳࠸ࠧమ"))
    return bstack11l1l1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack11l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡢࡤࡲࡸࠥࡸࡵ࡯ࠢ࠷࠲࠷ࡀࠠࡼࡿࠪయ").format(str(e)))
    try:
      return bstack11l1l1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack11l11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡥࡳࡹࠦࡦࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢࡾࢁࠬర").format(str(e2)))
      raise e
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack1llllll11l_opy_(self, runner, quiet=False, capture=True):
  global bstack11l1l1l1l_opy_
  bstack1l11ll111_opy_ = bstack11l1l1l1l_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack11l11_opy_ (u"࠭ࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࡡࡤࡶࡷ࠭ఱ")):
      runner.exception_arr = []
    if not hasattr(runner, bstack11l11_opy_ (u"ࠧࡦࡺࡦࡣࡹࡸࡡࡤࡧࡥࡥࡨࡱ࡟ࡢࡴࡵࠫల")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1l11ll111_opy_
def bstack11llll1ll1_opy_(runner, hook_name, context, element, bstack1l1l1ll11l_opy_, *args):
  global bstack1l11l11ll_opy_
  try:
    if runner.hooks.get(hook_name):
      bstack1l111llll_opy_.bstack111l1l11l1_opy_(hook_name, element)
    if bstack1l11l11ll_opy_ is None or bstack1l11l11ll_opy_:
      bstack1l1l1ll11l_opy_(runner, hook_name, context, *args)
    else:
      bstack111ll11lll_opy_ = (context,) + args
      bstack1l1l1ll11l_opy_(runner, hook_name, *bstack111ll11lll_opy_)
    if runner.hooks.get(hook_name):
      bstack1l111llll_opy_.bstack11lll1l111_opy_(element)
      if hook_name not in [bstack11l11_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠬళ"), bstack11l11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠬఴ")] and args and hasattr(args[0], bstack11l11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡡࡰࡩࡸࡹࡡࡨࡧࠪవ")):
        args[0].error_message = bstack11l11_opy_ (u"ࠫࠬశ")
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡪࡤࡲࡩࡲࡥࠡࡪࡲࡳࡰࡹࠠࡪࡰࠣࡦࡪ࡮ࡡࡷࡧ࠽ࠤࢀࢃࠧష").format(str(e)))
@measure(event_name=EVENTS.bstack11l1llllll_opy_, stage=STAGE.bstack111ll11l1_opy_, hook_type=bstack11l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡇ࡬࡭ࠤస"), bstack11l111l11l_opy_=bstack11l1111lll_opy_)
def bstack11l11l111l_opy_(runner, name, context, bstack1l1l1ll11l_opy_, *args):
    if runner.hooks.get(bstack11l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦహ")).__name__ != bstack11l11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࡤࡪࡥࡧࡣࡸࡰࡹࡥࡨࡰࡱ࡮ࠦ఺"):
      bstack11llll1ll1_opy_(runner, name, context, runner, bstack1l1l1ll11l_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack11l1l111ll_opy_(bstack11l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ఻")) else context.browser
      runner.driver_initialised = bstack11l11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲ఼ࠢ")
    except Exception as e:
      logger.debug(bstack11l11_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡩࡸࡩࡷࡧࡵࠤ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡥࠡࡣࡷࡸࡷ࡯ࡢࡶࡶࡨ࠾ࠥࢁࡽࠨఽ").format(str(e)))
def bstack1ll1ll11_opy_(runner, name, context, bstack1l1l1ll11l_opy_, *args):
    bstack11llll1ll1_opy_(runner, name, context, context.feature, bstack1l1l1ll11l_opy_, *args)
    try:
      if not bstack1llllllll1_opy_:
        bstack111l11111_opy_ = threading.current_thread().bstackSessionDriver if bstack11l1l111ll_opy_(bstack11l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫా")) else context.browser
        if is_driver_active(bstack111l11111_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack11l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠢి")
          bstack11l1llll1_opy_ = str(runner.feature.name)
          bstack1111llll_opy_(context, bstack11l1llll1_opy_)
          bstack111l11111_opy_.execute_script(bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬీ") + json.dumps(bstack11l1llll1_opy_) + bstack11l11_opy_ (u"ࠨࡿࢀࠫు"))
    except Exception as e:
      logger.debug(bstack11l11_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡ࡫ࡱࠤࡧ࡫ࡦࡰࡴࡨࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩూ").format(str(e)))
def bstack1lll1l11ll_opy_(runner, name, context, bstack1l1l1ll11l_opy_, *args):
    target = context.scenario if hasattr(context, bstack11l11_opy_ (u"ࠪࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬృ")) else context.feature
    bstack11llll1ll1_opy_(runner, name, context, target, bstack1l1l1ll11l_opy_, *args)
@measure(event_name=EVENTS.bstack11lll1l11l_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l111l11l_opy_=bstack11l1111lll_opy_)
def bstack1lll1llll1_opy_(runner, name, context, bstack1l1l1ll11l_opy_, *args):
    bstack1l111llll_opy_.start_test(context)
    bstack11llll1ll1_opy_(runner, name, context, context.scenario, bstack1l1l1ll11l_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack1ll11l11ll_opy_.bstack111l11ll1_opy_(context, *args)
    try:
      bstack111l11111_opy_ = bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪౄ"), context.browser)
      if is_driver_active(bstack111l11111_opy_):
        bstack1ll111l1_opy_.bstack1ll1111l11_opy_(bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ౅"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack11l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣె")
        if (not bstack1llllllll1_opy_):
          scenario_name = args[0].name
          feature_name = bstack11l1llll1_opy_ = str(runner.feature.name)
          bstack11l1llll1_opy_ = feature_name + bstack11l11_opy_ (u"ࠧࠡ࠯ࠣࠫే") + scenario_name
          if runner.driver_initialised == bstack11l11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥై"):
            bstack1111llll_opy_(context, bstack11l1llll1_opy_)
            bstack111l11111_opy_.execute_script(bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧ౉") + json.dumps(bstack11l1llll1_opy_) + bstack11l11_opy_ (u"ࠪࢁࢂ࠭ొ"))
    except Exception as e:
      logger.debug(bstack11l11_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣ࡭ࡳࠦࡢࡦࡨࡲࡶࡪࠦࡳࡤࡧࡱࡥࡷ࡯࡯࠻ࠢࡾࢁࠬో").format(str(e)))
@measure(event_name=EVENTS.bstack11l1llllll_opy_, stage=STAGE.bstack111ll11l1_opy_, hook_type=bstack11l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡘࡺࡥࡱࠤౌ"), bstack11l111l11l_opy_=bstack11l1111lll_opy_)
def bstack1ll1l1l11l_opy_(runner, name, context, bstack1l1l1ll11l_opy_, *args):
    bstack11llll1ll1_opy_(runner, name, context, args[0], bstack1l1l1ll11l_opy_, *args)
    try:
      bstack111l11111_opy_ = threading.current_thread().bstackSessionDriver if bstack11l1l111ll_opy_(bstack11l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶ్ࠬ")) else context.browser
      if is_driver_active(bstack111l11111_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack11l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧ౎")
        bstack1l111llll_opy_.bstack11lll11lll_opy_(args[0])
        if runner.driver_initialised == bstack11l11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨ౏"):
          feature_name = bstack11l1llll1_opy_ = str(runner.feature.name)
          bstack11l1llll1_opy_ = feature_name + bstack11l11_opy_ (u"ࠩࠣ࠱ࠥ࠭౐") + context.scenario.name
          bstack111l11111_opy_.execute_script(bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨ౑") + json.dumps(bstack11l1llll1_opy_) + bstack11l11_opy_ (u"ࠫࢂࢃࠧ౒"))
    except Exception as e:
      logger.debug(bstack11l11_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤ࡮ࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡶࡨࡴ࠿ࠦࡻࡾࠩ౓").format(str(e)))
@measure(event_name=EVENTS.bstack11l1llllll_opy_, stage=STAGE.bstack111ll11l1_opy_, hook_type=bstack11l11_opy_ (u"ࠨࡡࡧࡶࡨࡶࡘࡺࡥࡱࠤ౔"), bstack11l111l11l_opy_=bstack11l1111lll_opy_)
def bstack1l1l1l11_opy_(runner, name, context, bstack1l1l1ll11l_opy_, *args):
  bstack1l111llll_opy_.bstack1l1l11l1l1_opy_(args[0])
  try:
    step_status = args[0].status.name
    bstack111l11111_opy_ = threading.current_thread().bstackSessionDriver if bstack11l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷౕ࠭") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack111l11111_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack11l11_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨౖ")
        feature_name = bstack11l1llll1_opy_ = str(runner.feature.name)
        bstack11l1llll1_opy_ = feature_name + bstack11l11_opy_ (u"ࠩࠣ࠱ࠥ࠭౗") + context.scenario.name
        bstack111l11111_opy_.execute_script(bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨౘ") + json.dumps(bstack11l1llll1_opy_) + bstack11l11_opy_ (u"ࠫࢂࢃࠧౙ"))
    if str(step_status).lower() in [bstack11l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬౚ"), bstack11l11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ౛")]:
      bstack11ll111l1_opy_ = bstack11l11_opy_ (u"ࠧࠨ౜")
      bstack11lll1ll1_opy_ = bstack11l11_opy_ (u"ࠨࠩౝ")
      bstack11l11l1l11_opy_ = bstack11l11_opy_ (u"ࠩࠪ౞")
      try:
        import traceback
        bstack11ll111l1_opy_ = runner.exception.__class__.__name__
        bstack1lllll11l_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack11lll1ll1_opy_ = bstack11l11_opy_ (u"ࠪࠤࠬ౟").join(bstack1lllll11l_opy_)
        bstack11l11l1l11_opy_ = bstack1lllll11l_opy_[-1]
      except Exception as e:
        logger.debug(bstack1ll111lll1_opy_.format(str(e)))
      bstack11ll111l1_opy_ += bstack11l11l1l11_opy_
      bstack11l1l11ll_opy_(context, json.dumps(str(args[0].name) + bstack11l11_opy_ (u"ࠦࠥ࠳ࠠࡇࡣ࡬ࡰࡪࡪࠡ࡝ࡰࠥౠ") + str(bstack11lll1ll1_opy_)),
                          bstack11l11_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦౡ"))
      if runner.driver_initialised == bstack11l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦౢ"):
        bstack1l11lll11l_opy_(getattr(context, bstack11l11_opy_ (u"ࠧࡱࡣࡪࡩࠬౣ"), None), bstack11l11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ౤"), bstack11ll111l1_opy_)
        bstack111l11111_opy_.execute_script(bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ౥") + json.dumps(str(args[0].name) + bstack11l11_opy_ (u"ࠥࠤ࠲ࠦࡆࡢ࡫࡯ࡩࡩࠧ࡜࡯ࠤ౦") + str(bstack11lll1ll1_opy_)) + bstack11l11_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣࡿࢀࠫ౧"))
      if runner.driver_initialised == bstack11l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥ౨"):
        bstack1ll1l1l1_opy_(bstack111l11111_opy_, bstack11l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭౩"), bstack11l11_opy_ (u"ࠢࡔࡥࡨࡲࡦࡸࡩࡰࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦ౪") + str(bstack11ll111l1_opy_))
    else:
      bstack11l1l11ll_opy_(context, bstack11l11_opy_ (u"ࠣࡒࡤࡷࡸ࡫ࡤࠢࠤ౫"), bstack11l11_opy_ (u"ࠤ࡬ࡲ࡫ࡵࠢ౬"))
      if runner.driver_initialised == bstack11l11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣ౭"):
        bstack1l11lll11l_opy_(getattr(context, bstack11l11_opy_ (u"ࠫࡵࡧࡧࡦࠩ౮"), None), bstack11l11_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ౯"))
      bstack111l11111_opy_.execute_script(bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ౰") + json.dumps(str(args[0].name) + bstack11l11_opy_ (u"ࠢࠡ࠯ࠣࡔࡦࡹࡳࡦࡦࠤࠦ౱")) + bstack11l11_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦࢂࢃࠧ౲"))
      if runner.driver_initialised == bstack11l11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢ౳"):
        bstack1ll1l1l1_opy_(bstack111l11111_opy_, bstack11l11_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ౴"))
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࠡࡵࡷࡩࡵࡀࠠࡼࡿࠪ౵").format(str(e)))
  bstack11llll1ll1_opy_(runner, name, context, args[0], bstack1l1l1ll11l_opy_, *args)
@measure(event_name=EVENTS.bstack111ll111l_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l111l11l_opy_=bstack11l1111lll_opy_)
def bstack1l1111llll_opy_(runner, name, context, bstack1l1l1ll11l_opy_, *args):
  bstack1l111llll_opy_.end_test(args[0])
  try:
    bstack1lll1111ll_opy_ = args[0].status.name
    bstack111l11111_opy_ = bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ౶"), context.browser)
    bstack1ll11l11ll_opy_.bstack1111l1111_opy_(bstack111l11111_opy_)
    if str(bstack1lll1111ll_opy_).lower() in [bstack11l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭౷"), bstack11l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭౸")]:
      bstack11ll111l1_opy_ = bstack11l11_opy_ (u"ࠨࠩ౹")
      bstack11lll1ll1_opy_ = bstack11l11_opy_ (u"ࠩࠪ౺")
      bstack11l11l1l11_opy_ = bstack11l11_opy_ (u"ࠪࠫ౻")
      try:
        import traceback
        bstack11ll111l1_opy_ = runner.exception.__class__.__name__
        bstack1lllll11l_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack11lll1ll1_opy_ = bstack11l11_opy_ (u"ࠫࠥ࠭౼").join(bstack1lllll11l_opy_)
        bstack11l11l1l11_opy_ = bstack1lllll11l_opy_[-1]
      except Exception as e:
        logger.debug(bstack1ll111lll1_opy_.format(str(e)))
      bstack11ll111l1_opy_ += bstack11l11l1l11_opy_
      bstack11l1l11ll_opy_(context, json.dumps(str(args[0].name) + bstack11l11_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦ౽") + str(bstack11lll1ll1_opy_)),
                          bstack11l11_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ౾"))
      if runner.driver_initialised == bstack11l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤ౿") or runner.driver_initialised == bstack11l11_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨಀ"):
        bstack1l11lll11l_opy_(getattr(context, bstack11l11_opy_ (u"ࠩࡳࡥ࡬࡫ࠧಁ"), None), bstack11l11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥಂ"), bstack11ll111l1_opy_)
        bstack111l11111_opy_.execute_script(bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩಃ") + json.dumps(str(args[0].name) + bstack11l11_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦ಄") + str(bstack11lll1ll1_opy_)) + bstack11l11_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥࢁࢂ࠭ಅ"))
      if runner.driver_initialised == bstack11l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤಆ") or runner.driver_initialised == bstack11l11_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨಇ"):
        bstack1ll1l1l1_opy_(bstack111l11111_opy_, bstack11l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩಈ"), bstack11l11_opy_ (u"ࠥࡗࡨ࡫࡮ࡢࡴ࡬ࡳࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢಉ") + str(bstack11ll111l1_opy_))
    else:
      bstack11l1l11ll_opy_(context, bstack11l11_opy_ (u"ࠦࡕࡧࡳࡴࡧࡧࠥࠧಊ"), bstack11l11_opy_ (u"ࠧ࡯࡮ࡧࡱࠥಋ"))
      if runner.driver_initialised == bstack11l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣಌ") or runner.driver_initialised == bstack11l11_opy_ (u"ࠧࡪࡰࡶࡸࡪࡶࠧ಍"):
        bstack1l11lll11l_opy_(getattr(context, bstack11l11_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭ಎ"), None), bstack11l11_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤಏ"))
      bstack111l11111_opy_.execute_script(bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨಐ") + json.dumps(str(args[0].name) + bstack11l11_opy_ (u"ࠦࠥ࠳ࠠࡑࡣࡶࡷࡪࡪࠡࠣ಑")) + bstack11l11_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫಒ"))
      if runner.driver_initialised == bstack11l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣಓ") or runner.driver_initialised == bstack11l11_opy_ (u"ࠧࡪࡰࡶࡸࡪࡶࠧಔ"):
        bstack1ll1l1l1_opy_(bstack111l11111_opy_, bstack11l11_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣಕ"))
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫಖ").format(str(e)))
  bstack11llll1ll1_opy_(runner, name, context, context.scenario, bstack1l1l1ll11l_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack111lll1l1l_opy_(runner, name, context, bstack1l1l1ll11l_opy_, *args):
    target = context.scenario if hasattr(context, bstack11l11_opy_ (u"ࠪࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬಗ")) else context.feature
    bstack11llll1ll1_opy_(runner, name, context, target, bstack1l1l1ll11l_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack111lll1l11_opy_(runner, name, context, bstack1l1l1ll11l_opy_, *args):
    try:
      bstack111l11111_opy_ = bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪಘ"), context.browser)
      bstack111l111l11_opy_ = bstack11l11_opy_ (u"ࠬ࠭ಙ")
      if context.failed is True:
        bstack111llll1l1_opy_ = []
        bstack1111lll11_opy_ = []
        bstack11l1l1l11_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack111llll1l1_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1lllll11l_opy_ = traceback.format_tb(exc_tb)
            bstack1l1l1lll1l_opy_ = bstack11l11_opy_ (u"࠭ࠠࠨಚ").join(bstack1lllll11l_opy_)
            bstack1111lll11_opy_.append(bstack1l1l1lll1l_opy_)
            bstack11l1l1l11_opy_.append(bstack1lllll11l_opy_[-1])
        except Exception as e:
          logger.debug(bstack1ll111lll1_opy_.format(str(e)))
        bstack11ll111l1_opy_ = bstack11l11_opy_ (u"ࠧࠨಛ")
        for i in range(len(bstack111llll1l1_opy_)):
          bstack11ll111l1_opy_ += bstack111llll1l1_opy_[i] + bstack11l1l1l11_opy_[i] + bstack11l11_opy_ (u"ࠨ࡞ࡱࠫಜ")
        bstack111l111l11_opy_ = bstack11l11_opy_ (u"ࠩࠣࠫಝ").join(bstack1111lll11_opy_)
        if runner.driver_initialised in [bstack11l11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦಞ"), bstack11l11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣಟ")]:
          bstack11l1l11ll_opy_(context, bstack111l111l11_opy_, bstack11l11_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦಠ"))
          bstack1l11lll11l_opy_(getattr(context, bstack11l11_opy_ (u"࠭ࡰࡢࡩࡨࠫಡ"), None), bstack11l11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢಢ"), bstack11ll111l1_opy_)
          bstack111l11111_opy_.execute_script(bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ಣ") + json.dumps(bstack111l111l11_opy_) + bstack11l11_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࡽࡾࠩತ"))
          bstack1ll1l1l1_opy_(bstack111l11111_opy_, bstack11l11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥಥ"), bstack11l11_opy_ (u"ࠦࡘࡵ࡭ࡦࠢࡶࡧࡪࡴࡡࡳ࡫ࡲࡷࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦ࡜࡯ࠤದ") + str(bstack11ll111l1_opy_))
          bstack11lll11l_opy_ = bstack111ll11111_opy_(bstack111l111l11_opy_, runner.feature.name, logger)
          if (bstack11lll11l_opy_ != None):
            bstack1lll11ll1l_opy_.append(bstack11lll11l_opy_)
      else:
        if runner.driver_initialised in [bstack11l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨಧ"), bstack11l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥನ")]:
          bstack11l1l11ll_opy_(context, bstack11l11_opy_ (u"ࠢࡇࡧࡤࡸࡺࡸࡥ࠻ࠢࠥ಩") + str(runner.feature.name) + bstack11l11_opy_ (u"ࠣࠢࡳࡥࡸࡹࡥࡥࠣࠥಪ"), bstack11l11_opy_ (u"ࠤ࡬ࡲ࡫ࡵࠢಫ"))
          bstack1l11lll11l_opy_(getattr(context, bstack11l11_opy_ (u"ࠪࡴࡦ࡭ࡥࠨಬ"), None), bstack11l11_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦಭ"))
          bstack111l11111_opy_.execute_script(bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪಮ") + json.dumps(bstack11l11_opy_ (u"ࠨࡆࡦࡣࡷࡹࡷ࡫࠺ࠡࠤಯ") + str(runner.feature.name) + bstack11l11_opy_ (u"ࠢࠡࡲࡤࡷࡸ࡫ࡤࠢࠤರ")) + bstack11l11_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦࢂࢃࠧಱ"))
          bstack1ll1l1l1_opy_(bstack111l11111_opy_, bstack11l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩಲ"))
          bstack11lll11l_opy_ = bstack111ll11111_opy_(bstack111l111l11_opy_, runner.feature.name, logger)
          if (bstack11lll11l_opy_ != None):
            bstack1lll11ll1l_opy_.append(bstack11lll11l_opy_)
    except Exception as e:
      logger.debug(bstack11l11_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡯࡮ࠡࡣࡩࡸࡪࡸࠠࡧࡧࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬಳ").format(str(e)))
    bstack11llll1ll1_opy_(runner, name, context, context.feature, bstack1l1l1ll11l_opy_, *args)
@measure(event_name=EVENTS.bstack11l1llllll_opy_, stage=STAGE.bstack111ll11l1_opy_, hook_type=bstack11l11_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࡄࡰࡱࠨ಴"), bstack11l111l11l_opy_=bstack11l1111lll_opy_)
def bstack111ll1l111_opy_(runner, name, context, bstack1l1l1ll11l_opy_, *args):
    bstack11llll1ll1_opy_(runner, name, context, runner, bstack1l1l1ll11l_opy_, *args)
def bstack1l1l1111_opy_(self, filename=None):
  bstack11l11_opy_ (u"ࠧࠨࠢࠋࠢࠣࡐࡴࡧࡤࠡࡪࡲࡳࡰࡹࠠࡢࡰࡧࠤࡪࡴࡳࡶࡴࡨࠤࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠵ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠠࡢࡴࡨࠤࡷ࡫ࡧࡪࡵࡷࡩࡷ࡫ࡤ࠯ࠌࠣࠤࡇ࡫ࡨࡢࡸࡨࠤࡻ࠷࠮࠴࠭ࠣࡨࡴ࡫ࡳ࡯ࠩࡷࠤࡨࡧ࡬࡭ࠢࡵࡹࡳࠦࡨࡰࡱ࡮ࡷࠥࡺࡨࡢࡶࠣࡥࡷ࡫࡮ࠨࡶࠣࡨࡪ࡬ࡩ࡯ࡧࡧ࠰ࠥࡹ࡯ࠡࡹࡨࠤࡲࡻࡳࡵࠌࠣࠤࡩࡵࠠࡵࡪ࡬ࡷࠥ࡫ࡸࡱ࡮࡬ࡧ࡮ࡺ࡬ࡺࠢࡷࡳࠥࡳࡡ࡬ࡧࠣࡷࡺࡸࡥࠡࡹࡨࠫࡷ࡫ࠠࡤࡣ࡯ࡰࡪࡪࠠࡪࡰࠣࡥࡳࡿࠠࡤࡣࡶࡩ࠳ࠐࠠࠡࠤࠥࠦವ")
  global bstack1ll11111l1_opy_
  bstack1ll11111l1_opy_(self, filename)
  bstack1111l111l_opy_ = []
  bstack11lll11ll_opy_ = [bstack11l11_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠧಶ"), bstack11l11_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡵࡣࡪࠫಷ"), bstack11l11_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪಸ"), bstack11l11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪಹ"), bstack11l11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡷࡥ࡬࠭಺"), bstack11l11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫ಻")]
  bstack11ll1111_opy_ = lambda *_: None
  for hook_name in bstack11lll11ll_opy_:
    if hook_name not in self.hooks:
      self.hooks[hook_name] = bstack11ll1111_opy_
      bstack1111l111l_opy_.append(hook_name)
  if bstack1111l111l_opy_:
    os.environ[bstack11l11_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤ࡙ࡄࡌࡡࡇࡉࡋࡇࡕࡍࡖࡢࡌࡔࡕࡋࡔ಼ࠩ")] = bstack11l11_opy_ (u"࠭ࠬࠨಽ").join(bstack1111l111l_opy_)
def bstack11l1111l11_opy_(self, name, *args):
  global bstack1l1l1ll11l_opy_
  global bstack1l11l11ll_opy_
  try:
    if bstack111l1l11_opy_:
      platform_index = int(threading.current_thread()._name) % bstack1ll1l111l_opy_
      bstack111ll1llll_opy_ = CONFIG[bstack11l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪಾ")][platform_index]
      os.environ[bstack11l11_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩಿ")] = json.dumps(bstack111ll1llll_opy_)
    if not hasattr(self, bstack11l11_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡷࡪࡪࠧೀ")):
      self.driver_initialised = None
    bstack1l11ll1ll1_opy_ = {
        bstack11l11_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠧು"): bstack11l11l111l_opy_,
        bstack11l11_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠬೂ"): bstack1ll1ll11_opy_,
        bstack11l11_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡺࡡࡨࠩೃ"): bstack1lll1l11ll_opy_,
        bstack11l11_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨೄ"): bstack1lll1llll1_opy_,
        bstack11l11_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠬ೅"): bstack1ll1l1l11l_opy_,
        bstack11l11_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡴࡶࡨࡴࠬೆ"): bstack1l1l1l11_opy_,
        bstack11l11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪೇ"): bstack1l1111llll_opy_,
        bstack11l11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡷࡥ࡬࠭ೈ"): bstack111lll1l1l_opy_,
        bstack11l11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫ೉"): bstack111lll1l11_opy_,
        bstack11l11_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠨೊ"): bstack111ll1l111_opy_
    }
    handler = bstack1l11ll1ll1_opy_.get(name, bstack1l1l1ll11l_opy_)
    try:
      if args:
        context = args[0]
        remaining_args = args[1:]
        if bstack1l11l11ll_opy_ is None or not bstack1l11l11ll_opy_:
          context = self.context
          remaining_args = args
      else:
        context = self.context
        remaining_args = ()
      handler(self, name, context, bstack1l1l1ll11l_opy_, *remaining_args)
    except Exception as e:
      logger.debug(bstack11l11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡤࡨ࡬ࡦࡼࡥࠡࡪࡲࡳࡰࠦࡨࡢࡰࡧࡰࡪࡸࠠࡼࡿ࠽ࠤࢀࢃࠧೋ").format(name, str(e)))
    if name in [bstack11l11_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡦࡦࡣࡷࡹࡷ࡫ࠧೌ"), bstack11l11_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡴࡥࡨࡲࡦࡸࡩࡰ್ࠩ"), bstack11l11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠬ೎")]:
      try:
        bstack111l11111_opy_ = threading.current_thread().bstackSessionDriver if bstack11l1l111ll_opy_(bstack11l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ೏")) else context.browser
        bstack1111l1lll_opy_ = (
          (name == bstack11l11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡥࡱࡲࠧ೐") and self.driver_initialised == bstack11l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤ೑")) or
          (name == bstack11l11_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭೒") and self.driver_initialised == bstack11l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣ೓")) or
          (name == bstack11l11_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩ೔") and self.driver_initialised in [bstack11l11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦೕ"), bstack11l11_opy_ (u"ࠥ࡭ࡳࡹࡴࡦࡲࠥೖ")]) or
          (name == bstack11l11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡹ࡫ࡰࠨ೗") and self.driver_initialised == bstack11l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥ೘"))
        )
        if bstack1111l1lll_opy_:
          self.driver_initialised = None
          if bstack111l11111_opy_ and hasattr(bstack111l11111_opy_, bstack11l11_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠪ೙")):
            try:
              bstack111l11111_opy_.quit()
            except Exception as e:
              logger.debug(bstack11l11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡱࡶ࡫ࡷࡸ࡮ࡴࡧࠡࡦࡵ࡭ࡻ࡫ࡲࠡ࡫ࡱࠤࡧ࡫ࡨࡢࡸࡨࠤ࡭ࡵ࡯࡬࠼ࠣࡿࢂ࠭೚").format(str(e)))
      except Exception as e:
        logger.debug(bstack11l11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢ࡫ࡳࡴࡱࠠࡤ࡮ࡨࡥࡳࡻࡰࠡࡨࡲࡶࠥࢁࡽ࠻ࠢࡾࢁࠬ೛").format(name, str(e)))
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"ࠩࡆࡶ࡮ࡺࡩࡤࡣ࡯ࠤࡪࡸࡲࡰࡴࠣ࡭ࡳࠦࡢࡦࡪࡤࡺࡪࠦࡲࡶࡰࠣ࡬ࡴࡵ࡫ࠡࡽࢀ࠾ࠥࢁࡽࠨ೜").format(name, str(e)))
    try:
      if bstack1l11l11ll_opy_ is None or bstack1l11l11ll_opy_:
        try:
          bstack1l1l1ll11l_opy_(self, name, self.context, *args)
        except TypeError:
          bstack1l1l1ll11l_opy_(self, name, *args)
      else:
        bstack1l1l1ll11l_opy_(self, name, *args)
    except Exception as e2:
      logger.debug(bstack11l11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡬ࡡ࡭࡮ࡥࡥࡨࡱࠠࡰࡴ࡬࡫࡮ࡴࡡ࡭ࠢࡥࡩ࡭ࡧࡶࡦࠢ࡫ࡳࡴࡱࠠࡼࡿ࠽ࠤࢀࢃࠧೝ").format(name, str(e2)))
def bstack1l111llll1_opy_(config, startdir):
  return bstack11l11_opy_ (u"ࠦࡩࡸࡩࡷࡧࡵ࠾ࠥࢁ࠰ࡾࠤೞ").format(bstack11l11_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦ೟"))
notset = Notset()
def bstack11l1ll1l1l_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1l111l1ll1_opy_
  if str(name).lower() == bstack11l11_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷ࠭ೠ"):
    return bstack11l11_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨೡ")
  else:
    return bstack1l111l1ll1_opy_(self, name, default, skip)
def bstack1l1lllll1l_opy_(item, when):
  global bstack1ll111111l_opy_
  try:
    bstack1ll111111l_opy_(item, when)
  except Exception as e:
    pass
def bstack1l1l1ll1l1_opy_():
  return
def bstack1lll1l1l1l_opy_(type, name, status, reason, bstack111lll1ll_opy_, bstack1l11lll1l_opy_):
  bstack1lll1l11_opy_ = {
    bstack11l11_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨೢ"): type,
    bstack11l11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬೣ"): {}
  }
  if type == bstack11l11_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬ೤"):
    bstack1lll1l11_opy_[bstack11l11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ೥")][bstack11l11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ೦")] = bstack111lll1ll_opy_
    bstack1lll1l11_opy_[bstack11l11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ೧")][bstack11l11_opy_ (u"ࠧࡥࡣࡷࡥࠬ೨")] = json.dumps(str(bstack1l11lll1l_opy_))
  if type == bstack11l11_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ೩"):
    bstack1lll1l11_opy_[bstack11l11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ೪")][bstack11l11_opy_ (u"ࠪࡲࡦࡳࡥࠨ೫")] = name
  if type == bstack11l11_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧ೬"):
    bstack1lll1l11_opy_[bstack11l11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ೭")][bstack11l11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭೮")] = status
    if status == bstack11l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ೯"):
      bstack1lll1l11_opy_[bstack11l11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ೰")][bstack11l11_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩೱ")] = json.dumps(str(reason))
  bstack1l1l111111_opy_ = bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨೲ").format(json.dumps(bstack1lll1l11_opy_))
  return bstack1l1l111111_opy_
def bstack111lll1l1_opy_(driver_command, response):
    if driver_command == bstack11l11_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨೳ"):
        bstack1ll111l1_opy_.bstack1l111111l_opy_({
            bstack11l11_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫ೴"): response[bstack11l11_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬ೵")],
            bstack11l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ೶"): bstack1ll111l1_opy_.current_test_uuid()
        })
def bstack1l111ll1ll_opy_(item, call, rep):
  global bstack11l1ll11l1_opy_
  global bstack111l1llll1_opy_
  global bstack1llllllll1_opy_
  name = bstack11l11_opy_ (u"ࠨࠩ೷")
  try:
    if rep.when == bstack11l11_opy_ (u"ࠩࡦࡥࡱࡲࠧ೸"):
      bstack1111ll1l1_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1llllllll1_opy_:
          name = str(rep.nodeid)
          bstack11111lll1_opy_ = bstack1lll1l1l1l_opy_(bstack11l11_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ೹"), name, bstack11l11_opy_ (u"ࠫࠬ೺"), bstack11l11_opy_ (u"ࠬ࠭೻"), bstack11l11_opy_ (u"࠭ࠧ೼"), bstack11l11_opy_ (u"ࠧࠨ೽"))
          threading.current_thread().bstack1l1111l1l_opy_ = name
          for driver in bstack111l1llll1_opy_:
            if bstack1111ll1l1_opy_ == driver.session_id:
              driver.execute_script(bstack11111lll1_opy_)
      except Exception as e:
        logger.debug(bstack11l11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨ೾").format(str(e)))
      try:
        bstack11ll1llll_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack11l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ೿"):
          status = bstack11l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪഀ") if rep.outcome.lower() == bstack11l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫഁ") else bstack11l11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬം")
          reason = bstack11l11_opy_ (u"࠭ࠧഃ")
          if status == bstack11l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧഄ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack11l11_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭അ") if status == bstack11l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩആ") else bstack11l11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩഇ")
          data = name + bstack11l11_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭ഈ") if status == bstack11l11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬഉ") else name + bstack11l11_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠡࠡࠩഊ") + reason
          bstack1lll111lll_opy_ = bstack1lll1l1l1l_opy_(bstack11l11_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩഋ"), bstack11l11_opy_ (u"ࠨࠩഌ"), bstack11l11_opy_ (u"ࠩࠪ഍"), bstack11l11_opy_ (u"ࠪࠫഎ"), level, data)
          for driver in bstack111l1llll1_opy_:
            if bstack1111ll1l1_opy_ == driver.session_id:
              driver.execute_script(bstack1lll111lll_opy_)
      except Exception as e:
        logger.debug(bstack11l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡥࡲࡲࡹ࡫ࡸࡵࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨഏ").format(str(e)))
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡵࡷࡥࡹ࡫ࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻࡾࠩഐ").format(str(e)))
  bstack11l1ll11l1_opy_(item, call, rep)
def bstack111lllll11_opy_(driver, bstack111l1lll11_opy_, test=None):
  global bstack111llll1ll_opy_
  if test != None:
    bstack11lll1l1ll_opy_ = getattr(test, bstack11l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ഑"), None)
    bstack11l1ll11_opy_ = getattr(test, bstack11l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬഒ"), None)
    PercySDK.screenshot(driver, bstack111l1lll11_opy_, bstack11lll1l1ll_opy_=bstack11lll1l1ll_opy_, bstack11l1ll11_opy_=bstack11l1ll11_opy_, bstack1l11111l1l_opy_=bstack111llll1ll_opy_)
  else:
    PercySDK.screenshot(driver, bstack111l1lll11_opy_)
@measure(event_name=EVENTS.bstack11l11111_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l111l11l_opy_=bstack11l1111lll_opy_)
def bstack1l1l11l1_opy_(driver):
  if bstack1lll11ll_opy_.bstack1111l1l1_opy_() is True or bstack1lll11ll_opy_.capturing() is True:
    return
  bstack1lll11ll_opy_.bstack11l11l1l1l_opy_()
  while not bstack1lll11ll_opy_.bstack1111l1l1_opy_():
    bstack1ll1lll1l1_opy_ = bstack1lll11ll_opy_.bstack1111l11l_opy_()
    bstack111lllll11_opy_(driver, bstack1ll1lll1l1_opy_)
  bstack1lll11ll_opy_.bstack11111ll1_opy_()
def bstack1llll1l1l_opy_(sequence, driver_command, response = None, bstack11l1l11l11_opy_ = None, args = None):
    try:
      if sequence != bstack11l11_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨഓ"):
        return
      if percy.bstack1l1l1l1111_opy_() == bstack11l11_opy_ (u"ࠤࡩࡥࡱࡹࡥࠣഔ"):
        return
      bstack1ll1lll1l1_opy_ = bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠪࡴࡪࡸࡣࡺࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ക"), None)
      for command in bstack111lll1lll_opy_:
        if command == driver_command:
          with bstack1ll1ll1l1_opy_:
            bstack11111ll1l_opy_ = bstack111l1llll1_opy_.copy()
          for driver in bstack11111ll1l_opy_:
            bstack1l1l11l1_opy_(driver)
      bstack1llll1ll1_opy_ = percy.bstack1lllll11l1_opy_()
      if driver_command in bstack1lll11ll1_opy_[bstack1llll1ll1_opy_]:
        bstack1lll11ll_opy_.bstack11l1l1ll1l_opy_(bstack1ll1lll1l1_opy_, driver_command)
    except Exception as e:
      pass
def bstack1l1l1lll11_opy_(framework_name):
  if bstack11l1l1111_opy_.get_property(bstack11l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨഖ")):
      return
  bstack11l1l1111_opy_.bstack1ll111ll11_opy_(bstack11l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩഗ"), True)
  global bstack11l1111ll1_opy_
  global bstack1l1lllll_opy_
  global bstack1lll111ll_opy_
  bstack11l1111ll1_opy_ = framework_name
  logger.info(bstack11ll111lll_opy_.format(bstack11l1111ll1_opy_.split(bstack11l11_opy_ (u"࠭࠭ࠨഘ"))[0]))
  bstack1lll1lll1_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    global bstack1ll11l1111_opy_
    bstack1llll1111l_opy_ = bstack111l1l11_opy_ or bstack1ll11l1111_opy_
    if bstack1llll1111l_opy_:
      Service.start = bstack1l1l1ll1l_opy_
      Service.stop = bstack1ll1l1ll_opy_
      webdriver.Remote.get = bstack1ll1l1l111_opy_
      WebDriver.quit = bstack1ll11ll11l_opy_
      webdriver.Remote.__init__ = bstack1ll111111_opy_
    if not bstack111l1l11_opy_ and not bstack1ll11l1111_opy_:
        webdriver.Remote.__init__ = bstack1ll1llll1_opy_
    WebDriver.getAccessibilityResults = getAccessibilityResults
    WebDriver.get_accessibility_results = getAccessibilityResults
    WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
    WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
    WebDriver.performScan = perform_scan
    WebDriver.perform_scan = perform_scan
    WebDriver.execute = bstack11111ll11_opy_
    bstack1l1lllll_opy_ = True
  except Exception as e:
    pass
  try:
    bstack1llll1111l_opy_ = bstack111l1l11_opy_ or bstack1ll11l1111_opy_
    if bstack1llll1111l_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1111l1ll_opy_
  except Exception as e:
    pass
  bstack11l111llll_opy_()
  if not bstack1l1lllll_opy_:
    bstack1l11l1ll1l_opy_(bstack11l11_opy_ (u"ࠢࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠢࡱࡳࡹࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠤങ"), bstack11111lll_opy_)
  if bstack1lll1ll11_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      if hasattr(RemoteConnection, bstack11l11_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩച")) and callable(getattr(RemoteConnection, bstack11l11_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪഛ"))):
        RemoteConnection._get_proxy_url = bstack1l11ll1l1_opy_
      else:
        from selenium.webdriver.remote.client_config import ClientConfig
        ClientConfig.get_proxy_url = bstack1l11ll1l1_opy_
    except Exception as e:
      logger.error(bstack11l1111l1_opy_.format(str(e)))
  if bstack111lllll_opy_():
    bstack1l11llllll_opy_(CONFIG, logger)
  if (bstack11l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩജ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      try:
        from pabot.pabot import QueueItem
        from pabot import pabot
      except Exception as e:
        logger.warning(bstack1l1l11l11_opy_ + str(e))
      if not is_robot_playwright_installed():
        try:
          if percy.bstack1l1l1l1111_opy_() == bstack11l11_opy_ (u"ࠦࡹࡸࡵࡦࠤഝ"):
            bstack111l111l1_opy_(bstack1llll1l1l_opy_)
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
          WebDriverCreator._get_ff_profile = bstack1ll111l1l_opy_
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
          WebDriverCache.close = bstack11lll1llll_opy_
        except Exception as e:
          logger.warning(bstack11ll11lll_opy_ + str(e))
        try:
          from AppiumLibrary.utils.applicationcache import ApplicationCache
          ApplicationCache.close = bstack1ll11l1l1_opy_
        except Exception as e:
          logger.debug(bstack1lll1111l_opy_ + str(e))
    except Exception as e:
      bstack1l11l1ll1l_opy_(e, bstack11ll11lll_opy_)
    Output.start_test = bstack1l1111ll1l_opy_
    Output.end_test = bstack1l1l11l1ll_opy_
    TestStatus.__init__ = bstack1ll11l11_opy_
    QueueItem.__init__ = bstack111ll1l1ll_opy_
    pabot._create_items = bstack111l111l1l_opy_
    try:
      from pabot import __version__ as bstack1ll1l1llll_opy_
      if version.parse(bstack1ll1l1llll_opy_) >= version.parse(bstack11l11_opy_ (u"ࠬ࠻࠮࠱࠰࠳ࠫഞ")):
        pabot._run = bstack11lllll111_opy_
      elif version.parse(bstack1ll1l1llll_opy_) >= version.parse(bstack11l11_opy_ (u"࠭࠴࠯࠴࠱࠴ࠬട")):
        pabot._run = bstack1l1111lll_opy_
      elif version.parse(bstack1ll1l1llll_opy_) >= version.parse(bstack11l11_opy_ (u"ࠧ࠳࠰࠴࠹࠳࠶ࠧഠ")):
        pabot._run = bstack1ll11l11l1_opy_
      elif version.parse(bstack1ll1l1llll_opy_) >= version.parse(bstack11l11_opy_ (u"ࠨ࠴࠱࠵࠸࠴࠰ࠨഡ")):
        pabot._run = bstack1l11l1ll1_opy_
      else:
        pabot._run = bstack11l111111l_opy_
    except Exception as e:
      pabot._run = bstack11l111111l_opy_
    pabot._create_command_for_execution = bstack1l11ll11ll_opy_
    pabot._report_results = bstack1l111l11ll_opy_
  if bstack11l11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩഢ") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l11l1ll1l_opy_(e, bstack1111lll1l1_opy_)
    Runner.run_hook = bstack11l1111l11_opy_
    try:
      from behave import __version__ as bstack1111llll1_opy_
      if version.parse(bstack1111llll1_opy_) >= version.parse(bstack11l11_opy_ (u"ࠪ࠵࠳࠹࠮࠱ࠩണ")):
        Runner.load_hooks = bstack1l1l1111_opy_
    except Exception as e:
      logger.debug(bstack11l11_opy_ (u"ࠫࡈࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡦࡪ࡮ࡡࡷࡧࠣࡺࡪࡸࡳࡪࡱࡱ࠾ࠥࢁࡽࠨത").format(str(e)))
    Step.run = bstack1llllll11l_opy_
  if bstack11l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬഥ") in str(framework_name).lower():
    if not bstack111l1l11_opy_:
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack1l111llll1_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1l1l1ll1l1_opy_
      Config.getoption = bstack11l1ll1l1l_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1l111ll1ll_opy_
    except Exception as e:
      pass
def bstack1l1111l1_opy_():
  global CONFIG
  if bstack11l11_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ദ") in CONFIG and int(CONFIG[bstack11l11_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧധ")]) > 1:
    logger.warning(bstack1l1ll1l11l_opy_)
def bstack11l11ll1l1_opy_(arg, bstack11ll1lll1_opy_, bstack1l11l1lll1_opy_=None):
  global CONFIG
  global bstack1ll1l1l1ll_opy_
  global bstack11lll1l11_opy_
  global bstack111l1l11_opy_
  global bstack1ll11l1111_opy_
  global bstack11l1l1111_opy_
  bstack1l1l1l111l_opy_ = bstack11l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨന")
  if bstack11ll1lll1_opy_ and isinstance(bstack11ll1lll1_opy_, str):
    bstack11ll1lll1_opy_ = eval(bstack11ll1lll1_opy_)
  CONFIG = bstack11ll1lll1_opy_[bstack11l11_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩഩ")]
  bstack1ll1l1l1ll_opy_ = bstack11ll1lll1_opy_[bstack11l11_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫപ")]
  bstack11lll1l11_opy_ = bstack11ll1lll1_opy_[bstack11l11_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ഫ")]
  bstack111l1l11_opy_ = bstack11ll1lll1_opy_[bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨബ")]
  try:
    bstack111l1ll1l1_opy_ = bstack11ll1lll1_opy_.get(bstack11l11_opy_ (u"࠭ࡏࡗࡇࡕࡖࡎࡊࡅࡠࡎࡒࡅࡉࡥࡔࡆࡕࡗࡍࡓࡍࠧഭ"), False)
    bstack1ll11l1111_opy_ = bool(bstack111l1ll1l1_opy_)
    os.environ[bstack11l11_opy_ (u"ࠧࡐࡘࡈࡖࡗࡏࡄࡆࡡࡏࡓࡆࡊ࡟ࡕࡇࡖࡘࡎࡔࡇࠨമ")] = str(bstack1ll11l1111_opy_).lower()
  except Exception as e:
    logger.error(bstack11l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡕࡖࡆࡔࡕࡍࡉࡋ࡟ࡍࡑࡄࡈࡤ࡚ࡅࡔࡖࡌࡒࡌࡀࠠࡼࡿࠥയ").format(e))
    bstack1ll11l1111_opy_ = False
    os.environ[bstack11l11_opy_ (u"ࠩࡒ࡚ࡊࡘࡒࡊࡆࡈࡣࡑࡕࡁࡅࡡࡗࡉࡘ࡚ࡉࡏࡉࠪര")] = bstack11l11_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩറ")
  bstack11l1l1111_opy_.bstack1ll111ll11_opy_(bstack11l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬല"), bstack111l1l11_opy_)
  os.environ[bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧള")] = bstack1l1l1l111l_opy_
  os.environ[bstack11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࠬഴ")] = json.dumps(CONFIG)
  os.environ[bstack11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡈࡖࡄࡢ࡙ࡗࡒࠧവ")] = bstack1ll1l1l1ll_opy_
  os.environ[bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩശ")] = str(bstack11lll1l11_opy_)
  os.environ[bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡏ࡙ࡌࡏࡎࠨഷ")] = str(True)
  if bstack1llllllll_opy_(arg, [bstack11l11_opy_ (u"ࠪ࠱ࡳ࠭സ"), bstack11l11_opy_ (u"ࠫ࠲࠳࡮ࡶ࡯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬഹ")]) != -1:
    os.environ[bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡇࡒࡂࡎࡏࡉࡑ࠭ഺ")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack11lll111_opy_)
    return
  bstack11l11llll_opy_()
  global bstack1l111lll11_opy_
  global bstack111llll1ll_opy_
  global bstack1l1lll1l11_opy_
  global bstack111lll11_opy_
  global bstack1l11l1l11l_opy_
  global bstack1lll111ll_opy_
  global bstack11lllll1l_opy_
  arg.append(bstack11l11_opy_ (u"ࠨ࠭ࡘࠤ഻"))
  arg.append(bstack11l11_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫࠺ࡎࡱࡧࡹࡱ࡫ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡ࡫ࡰࡴࡴࡸࡴࡦࡦ࠽ࡴࡾࡺࡥࡴࡶ࠱ࡔࡾࡺࡥࡴࡶ࡚ࡥࡷࡴࡩ࡯ࡩ഼ࠥ"))
  arg.append(bstack11l11_opy_ (u"ࠣ࠯࡚ࠦഽ"))
  arg.append(bstack11l11_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡦ࠼ࡗ࡬ࡪࠦࡨࡰࡱ࡮࡭ࡲࡶ࡬ࠣാ"))
  global bstack11l111111_opy_
  global bstack11l111l1ll_opy_
  global bstack1lll111l_opy_
  global bstack11ll1l1111_opy_
  global bstack111llll11l_opy_
  global bstack111l1l111_opy_
  global bstack1l1l1ll1ll_opy_
  global bstack1l1111l1ll_opy_
  global bstack11ll11ll_opy_
  global bstack111lllllll_opy_
  global bstack1l111l1ll1_opy_
  global bstack1ll111111l_opy_
  global bstack11l1ll11l1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11l111111_opy_ = webdriver.Remote.__init__
    bstack11l111l1ll_opy_ = WebDriver.quit
    bstack1l1111l1ll_opy_ = WebDriver.close
    bstack11ll11ll_opy_ = WebDriver.get
    bstack1lll111l_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1l1l11l11l_opy_(CONFIG) and bstack1l1l1l1lll_opy_():
    if bstack111l1lll1_opy_() < version.parse(bstack11ll111ll1_opy_):
      logger.error(bstack1111lllll_opy_.format(bstack111l1lll1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack11l11_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫി")) and callable(getattr(RemoteConnection, bstack11l11_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬീ"))):
          bstack111lllllll_opy_ = RemoteConnection._get_proxy_url
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          bstack111lllllll_opy_ = ClientConfig.get_proxy_url
      except Exception as e:
        logger.error(bstack11l1111l1_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1l111l1ll1_opy_ = Config.getoption
    from _pytest import runner
    bstack1ll111111l_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warning(bstack11l11_opy_ (u"ࠧࠫࡳ࠻ࠢࠨࡷࠧു"), bstack11lllll11_opy_, str(e))
  try:
    from pytest_bdd import reporting
    bstack11l1ll11l1_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧൂ"))
  bstack1l1lll1l11_opy_ = CONFIG.get(bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫൃ"), {}).get(bstack11l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪൄ"))
  bstack11lllll1l_opy_ = True
  if cli.is_enabled(CONFIG):
    if cli.bstack11111l1l_opy_():
      bstack1l11l11111_opy_.invoke(bstack11ll111111_opy_.CONNECT, bstack111l1ll1l_opy_())
    platform_index = int(os.environ.get(bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ൅"), bstack11l11_opy_ (u"ࠪ࠴ࠬെ")))
  else:
    bstack1l1l1lll11_opy_(bstack1lllllll1l_opy_)
  os.environ[bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬേ")] = CONFIG[bstack11l11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧൈ")]
  os.environ[bstack11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩ൉")] = CONFIG[bstack11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪൊ")]
  os.environ[bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫോ")] = bstack111l1l11_opy_.__str__()
  from _pytest.config import main as bstack1l1l1lll_opy_
  bstack1l1lll111_opy_ = []
  try:
    exit_code = bstack1l1l1lll_opy_(arg)
    if cli.is_enabled(CONFIG):
      cli.bstack1lllll1l1l_opy_()
    if bstack11l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠭ൌ") in multiprocessing.current_process().__dict__.keys():
      for bstack1l1ll1l111_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1l1lll111_opy_.append(bstack1l1ll1l111_opy_)
    try:
      bstack1lllll1111_opy_ = (bstack1l1lll111_opy_, int(exit_code))
      bstack1l11l1lll1_opy_.append(bstack1lllll1111_opy_)
    except:
      bstack1l11l1lll1_opy_.append((bstack1l1lll111_opy_, exit_code))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack1l1lll111_opy_.append({bstack11l11_opy_ (u"ࠪࡲࡦࡳࡥࠨ്"): bstack11l11_opy_ (u"ࠫࡕࡸ࡯ࡤࡧࡶࡷࠥ࠭ൎ") + os.environ.get(bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ൏")), bstack11l11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ൐"): traceback.format_exc(), bstack11l11_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭൑"): int(os.environ.get(bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ൒")))})
    bstack1l11l1lll1_opy_.append((bstack1l1lll111_opy_, 1))
def mod_behave_main(args, retries):
  try:
    from behave.configuration import Configuration
    from behave.__main__ import run_behave
    from browserstack_sdk.bstack_behave_runner import BehaveRunner
    config = Configuration(args)
    config.update_userdata({bstack11l11_opy_ (u"ࠤࡵࡩࡹࡸࡩࡦࡵࠥ൓"): str(retries)})
    return run_behave(config, runner_class=BehaveRunner)
  except Exception as e:
    bstack1l11ll1l11_opy_ = e.__class__.__name__
    print(bstack11l11_opy_ (u"ࠥࠩࡸࡀࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡵࡧࡶࡸࠥࠫࡳࠣൔ") % (bstack1l11ll1l11_opy_, e))
    return 1
def bstack111l1l1l1l_opy_(arg):
  global bstack111ll1111_opy_
  bstack1l1l1lll11_opy_(bstack11l111ll11_opy_)
  os.environ[bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬൕ")] = str(bstack11lll1l11_opy_)
  retries = bstack1l11l1l1ll_opy_.bstack11l1l1lll1_opy_(CONFIG)
  status_code = 0
  if bstack1l11l1l1ll_opy_.bstack11l11lll11_opy_(CONFIG):
    status_code = mod_behave_main(arg, retries)
  else:
    from behave.__main__ import main as bstack1l11l111_opy_
    status_code = bstack1l11l111_opy_(arg)
  if status_code != 0:
    bstack111ll1111_opy_ = status_code
def bstack1111111ll_opy_():
  logger.info(bstack1111ll1ll_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack11l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫൖ"), help=bstack11l11_opy_ (u"࠭ࡇࡦࡰࡨࡶࡦࡺࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡤࡱࡱࡪ࡮࡭ࠧൗ"))
  parser.add_argument(bstack11l11_opy_ (u"ࠧ࠮ࡷࠪ൘"), bstack11l11_opy_ (u"ࠨ࠯࠰ࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬ൙"), help=bstack11l11_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡵࡴࡧࡵࡲࡦࡳࡥࠨ൚"))
  parser.add_argument(bstack11l11_opy_ (u"ࠪ࠱ࡰ࠭൛"), bstack11l11_opy_ (u"ࠫ࠲࠳࡫ࡦࡻࠪ൜"), help=bstack11l11_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡤࡧࡨ࡫ࡳࡴࠢ࡮ࡩࡾ࠭൝"))
  parser.add_argument(bstack11l11_opy_ (u"࠭࠭ࡧࠩ൞"), bstack11l11_opy_ (u"ࠧ࠮࠯ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬൟ"), help=bstack11l11_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧൠ"))
  bstack1l1ll11l1l_opy_ = parser.parse_args()
  try:
    bstack1l11111l_opy_ = bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡩࡨࡲࡪࡸࡩࡤ࠰ࡼࡱࡱ࠴ࡳࡢ࡯ࡳࡰࡪ࠭ൡ")
    if bstack1l1ll11l1l_opy_.framework and bstack1l1ll11l1l_opy_.framework not in (bstack11l11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪൢ"), bstack11l11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬൣ")):
      bstack1l11111l_opy_ = bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠮ࡺ࡯࡯࠲ࡸࡧ࡭ࡱ࡮ࡨࠫ൤")
    bstack11111111_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l11111l_opy_)
    bstack1lll1l111_opy_ = open(bstack11111111_opy_, bstack11l11_opy_ (u"࠭ࡲࠨ൥"))
    bstack1ll11l111l_opy_ = bstack1lll1l111_opy_.read()
    bstack1lll1l111_opy_.close()
    if bstack1l1ll11l1l_opy_.username:
      bstack1ll11l111l_opy_ = bstack1ll11l111l_opy_.replace(bstack11l11_opy_ (u"࡚ࠧࡑࡘࡖࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧ൦"), bstack1l1ll11l1l_opy_.username)
    if bstack1l1ll11l1l_opy_.key:
      bstack1ll11l111l_opy_ = bstack1ll11l111l_opy_.replace(bstack11l11_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ൧"), bstack1l1ll11l1l_opy_.key)
    if bstack1l1ll11l1l_opy_.framework:
      bstack1ll11l111l_opy_ = bstack1ll11l111l_opy_.replace(bstack11l11_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪ൨"), bstack1l1ll11l1l_opy_.framework)
    file_name = bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭൩")
    file_path = os.path.abspath(file_name)
    bstack1l1lllll11_opy_ = open(file_path, bstack11l11_opy_ (u"ࠫࡼ࠭൪"))
    bstack1l1lllll11_opy_.write(bstack1ll11l111l_opy_)
    bstack1l1lllll11_opy_.close()
    logger.info(bstack11ll1l111l_opy_)
    try:
      os.environ[bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ൫")] = bstack1l1ll11l1l_opy_.framework if bstack1l1ll11l1l_opy_.framework != None else bstack11l11_opy_ (u"ࠨࠢ൬")
      config = yaml.safe_load(bstack1ll11l111l_opy_)
      config[bstack11l11_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ൭")] = bstack11l11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡵࡨࡸࡺࡶࠧ൮")
      bstack1lll11l11l_opy_(bstack11lll1l1l1_opy_, config)
    except Exception as e:
      logger.debug(bstack1l1ll1lll_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1111ll1l_opy_.format(str(e)))
def bstack1lll11l11l_opy_(bstack1l1ll11111_opy_, config, bstack11l1l1ll11_opy_={}):
  global bstack111l1l11_opy_
  global bstack1llll11l1l_opy_
  global bstack11l1l1111_opy_
  if not config:
    return
  bstack1l1llll1_opy_ = bstack11l11l1l_opy_ if not bstack111l1l11_opy_ else (
    bstack111l1l1l11_opy_ if bstack11l11_opy_ (u"ࠩࡤࡴࡵ࠭൯") in config else (
        bstack1llll11l11_opy_ if config.get(bstack11l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ൰")) else bstack1l111l1111_opy_
    )
)
  bstack11lll11l11_opy_ = False
  bstack1l1ll1l1l1_opy_ = False
  if bstack111l1l11_opy_ is True:
      if bstack11l11_opy_ (u"ࠫࡦࡶࡰࠨ൱") in config:
          bstack11lll11l11_opy_ = True
      else:
          bstack1l1ll1l1l1_opy_ = True
  bstack111ll1ll1l_opy_ = bstack1l11l1l1l1_opy_.bstack11l1ll11l_opy_(config, bstack1llll11l1l_opy_)
  bstack1ll111ll1l_opy_ = bstack11l1l1111l_opy_()
  data = {
    bstack11l11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ൲"): config[bstack11l11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ൳")],
    bstack11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ൴"): config[bstack11l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ൵")],
    bstack11l11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭൶"): bstack1l1ll11111_opy_,
    bstack11l11_opy_ (u"ࠪࡨࡪࡺࡥࡤࡶࡨࡨࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ൷"): os.environ.get(bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭൸"), bstack1llll11l1l_opy_),
    bstack11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ൹"): bstack1l1111l11_opy_,
    bstack11l11_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬ࠨൺ"): bstack1l111l11l_opy_(),
    bstack11l11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪൻ"): {
      bstack11l11_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ർ"): str(config[bstack11l11_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩൽ")]) if bstack11l11_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪൾ") in config else bstack11l11_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧൿ"),
      bstack11l11_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࡖࡦࡴࡶ࡭ࡴࡴࠧ඀"): sys.version,
      bstack11l11_opy_ (u"࠭ࡲࡦࡨࡨࡶࡷ࡫ࡲࠨඁ"): bstack11ll1ll11_opy_(os.environ.get(bstack11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩං"), bstack1llll11l1l_opy_)),
      bstack11l11_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪඃ"): bstack11l11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ඄"),
      bstack11l11_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫඅ"): bstack1l1llll1_opy_,
      bstack11l11_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩආ"): bstack111ll1ll1l_opy_,
      bstack11l11_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡥࡵࡶ࡫ࡧࠫඇ"): os.environ[bstack11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫඈ")],
      bstack11l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪඉ"): os.environ.get(bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪඊ"), bstack1llll11l1l_opy_),
      bstack11l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬඋ"): bstack1ll1llll_opy_(os.environ.get(bstack11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬඌ"), bstack1llll11l1l_opy_)),
      bstack11l11_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪඍ"): bstack1ll111ll1l_opy_.get(bstack11l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪඎ")),
      bstack11l11_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬඏ"): bstack1ll111ll1l_opy_.get(bstack11l11_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨඐ")),
      bstack11l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫඑ"): config[bstack11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬඒ")] if config[bstack11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ඓ")] else bstack11l11_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧඔ"),
      bstack11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧඕ"): str(config[bstack11l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨඖ")]) if bstack11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ඗") in config else bstack11l11_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤ඘"),
      bstack11l11_opy_ (u"ࠩࡲࡷࠬ඙"): sys.platform,
      bstack11l11_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬක"): socket.gethostname(),
      bstack11l11_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭ඛ"): bstack11l1l1111_opy_.get_property(bstack11l11_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪࠧග"))
    }
  }
  if not bstack11l1l1111_opy_.get_property(bstack11l11_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭ඝ")) is None:
    data[bstack11l11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪඞ")][bstack11l11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡐࡩࡹࡧࡤࡢࡶࡤࠫඟ")] = {
      bstack11l11_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩච"): bstack11l11_opy_ (u"ࠪࡹࡸ࡫ࡲࡠ࡭࡬ࡰࡱ࡫ࡤࠨඡ"),
      bstack11l11_opy_ (u"ࠫࡸ࡯ࡧ࡯ࡣ࡯ࠫජ"): bstack11l1l1111_opy_.get_property(bstack11l11_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬඣ")),
      bstack11l11_opy_ (u"࠭ࡳࡪࡩࡱࡥࡱࡔࡵ࡮ࡤࡨࡶࠬඤ"): bstack11l1l1111_opy_.get_property(bstack11l11_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡏࡱࠪඥ"))
    }
  if bstack1l1ll11111_opy_ == bstack111l111111_opy_:
    data[bstack11l11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫඦ")][bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡄࡱࡱࡪ࡮࡭ࠧට")] = bstack111l111ll1_opy_(config)
    data[bstack11l11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭ඨ")][bstack11l11_opy_ (u"ࠫ࡮ࡹࡐࡦࡴࡦࡽࡆࡻࡴࡰࡇࡱࡥࡧࡲࡥࡥࠩඩ")] = percy.bstack111111ll_opy_
    data[bstack11l11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨඪ")][bstack11l11_opy_ (u"࠭ࡰࡦࡴࡦࡽࡇࡻࡩ࡭ࡦࡌࡨࠬණ")] = percy.percy_build_id
  if not bstack1l11l1l1ll_opy_.bstack1llll11lll_opy_(CONFIG):
    data[bstack11l11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪඬ")][bstack11l11_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠬත")] = bstack1l11l1l1ll_opy_.bstack1llll11lll_opy_(CONFIG)
  bstack1l1llll1l_opy_ = bstack1l1lll11l_opy_.bstack111l1lll_opy_(CONFIG, logger)
  bstack1l11ll1l_opy_ = bstack1l11l1l1ll_opy_.bstack111l1lll_opy_(config=CONFIG)
  if bstack1l1llll1l_opy_ is not None and bstack1l11ll1l_opy_ is not None and bstack1l11ll1l_opy_.bstack1l11lllll_opy_():
    data[bstack11l11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬථ")][bstack1l11ll1l_opy_.bstack11llllll1_opy_()] = bstack1l1llll1l_opy_.bstack1l1l1111l_opy_()
  update(data[bstack11l11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭ද")], bstack11l1l1ll11_opy_)
  try:
    response = bstack1l11l11ll1_opy_(bstack11l11_opy_ (u"ࠫࡕࡕࡓࡕࠩධ"), bstack11l111ll1_opy_(bstack1ll11l1ll_opy_), data, {
      bstack11l11_opy_ (u"ࠬࡧࡵࡵࡪࠪන"): (config[bstack11l11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ඲")], config[bstack11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪඳ")])
    })
    if response:
      logger.debug(bstack111l1l11ll_opy_.format(bstack1l1ll11111_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack111ll111_opy_.format(str(e)))
def bstack11ll1ll11_opy_(framework):
  return bstack11l11_opy_ (u"ࠣࡽࢀ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࡾࢁࠧප").format(str(framework), __version__) if framework else bstack11l11_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࡼࡿࠥඵ").format(
    __version__)
def bstack11l11llll_opy_():
  global CONFIG
  global bstack1l1ll1llll_opy_
  if bool(CONFIG):
    return
  try:
    bstack111ll1l1_opy_()
    logger.debug(bstack11ll1llll1_opy_.format(str(CONFIG)))
    bstack1l1ll1llll_opy_ = logger_utils.configure_logger(CONFIG, bstack1l1ll1llll_opy_)
    bstack1lll1lll1_opy_()
  except Exception as e:
    logger.error(bstack11l11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࡸࡴ࠱ࠦࡥࡳࡴࡲࡶ࠿ࠦࠢබ") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1l111ll111_opy_
  atexit.register(bstack11ll1l1l11_opy_)
  signal.signal(signal.SIGINT, bstack1l1ll1l1ll_opy_)
  signal.signal(signal.SIGTERM, bstack1l1ll1l1ll_opy_)
def bstack1l111ll111_opy_(exctype, value, traceback):
  global bstack111l1llll1_opy_
  try:
    for driver in bstack111l1llll1_opy_:
      bstack1ll1l1l1_opy_(driver, bstack11l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫභ"), bstack11l11_opy_ (u"࡙ࠧࡥࡴࡵ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࡢ࡮ࠣම") + str(value))
  except Exception:
    pass
  logger.info(bstack1l111l1l1_opy_)
  bstack111ll111l1_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack111ll111l1_opy_(message=bstack11l11_opy_ (u"࠭ࠧඹ"), bstack1llll1l11l_opy_ = False):
  global CONFIG
  bstack11ll111l11_opy_ = bstack11l11_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠩය") if bstack1llll1l11l_opy_ else bstack11l11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧර")
  bstack1l1l11llll_opy_ = bstack111l1lllll_opy_.bstack1l11111111_opy_(EVENTS.bstack11lllllll_opy_)
  try:
    if message:
      bstack11l1l1ll11_opy_ = {
        bstack11ll111l11_opy_ : str(message)
      }
      try:
        bstack1lll11l11l_opy_(bstack111l111111_opy_, CONFIG, bstack11l1l1ll11_opy_)
      finally:
        bstack111l1lllll_opy_.end(EVENTS.bstack11lllllll_opy_.value, bstack1l1l11llll_opy_ + bstack11l11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ඼"), bstack1l1l11llll_opy_ + bstack11l11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣල"), status=True, failure=None, test_name=None)
    else:
      try:
        bstack1lll11l11l_opy_(bstack111l111111_opy_, CONFIG)
      finally:
        bstack111l1lllll_opy_.end(EVENTS.bstack11lllllll_opy_.value, bstack1l1l11llll_opy_ + bstack11l11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ඾"), bstack1l1l11llll_opy_ + bstack11l11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ඿"), status=True, failure=None, test_name=None)
  except Exception as e:
    logger.debug(bstack1ll11111l_opy_.format(str(e)))
def bstack1l1l11111l_opy_(bstack1l11111ll1_opy_, size):
  bstack11l1l11l1l_opy_ = []
  while len(bstack1l11111ll1_opy_) > size:
    bstack1l11lllll1_opy_ = bstack1l11111ll1_opy_[:size]
    bstack11l1l11l1l_opy_.append(bstack1l11lllll1_opy_)
    bstack1l11111ll1_opy_ = bstack1l11111ll1_opy_[size:]
  bstack11l1l11l1l_opy_.append(bstack1l11111ll1_opy_)
  return bstack11l1l11l1l_opy_
def bstack1ll1l1ll1_opy_(args):
  if bstack11l11_opy_ (u"࠭࠭࡮ࠩව") in args and bstack11l11_opy_ (u"ࠧࡱࡦࡥࠫශ") in args:
    return True
  return False
@measure(event_name=EVENTS.bstack11lllll1ll_opy_, stage=STAGE.bstack111l1ll11l_opy_)
def run_on_browserstack(bstack1l1l1ll1_opy_=None, bstack1l11l1lll1_opy_=None, bstack1l1lll1l1l_opy_=False):
  global CONFIG
  global bstack1ll1l1l1ll_opy_
  global bstack11lll1l11_opy_
  global bstack1llll11l1l_opy_
  global bstack11l1l1111_opy_
  bstack1l1l1l111l_opy_ = bstack11l11_opy_ (u"ࠨࠩෂ")
  bstack1l1ll1l1l_opy_ = bstack11l11_opy_ (u"ࠤࠥස")
  bstack11l11llll1_opy_(bstack11l1111111_opy_, logger)
  if bstack1l1l1ll1_opy_ and isinstance(bstack1l1l1ll1_opy_, str):
    bstack1l1l1ll1_opy_ = eval(bstack1l1l1ll1_opy_)
  if bstack1l1l1ll1_opy_:
    CONFIG = bstack1l1l1ll1_opy_[bstack11l11_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪහ")]
    bstack1ll1l1l1ll_opy_ = bstack1l1l1ll1_opy_[bstack11l11_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬළ")]
    bstack11lll1l11_opy_ = bstack1l1l1ll1_opy_[bstack11l11_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧෆ")]
    bstack11l1l1111_opy_.bstack1ll111ll11_opy_(bstack11l11_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ෇"), bstack11lll1l11_opy_)
    bstack1l1l1l111l_opy_ = bstack11l11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ෈")
  bstack11l1l1111_opy_.bstack1ll111ll11_opy_(bstack11l11_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪ෉"), uuid4().__str__())
  logger.info(bstack11l11_opy_ (u"ࠩࡖࡈࡐࠦࡲࡶࡰࠣࡷࡹࡧࡲࡵࡧࡧࠤࡼ࡯ࡴࡩࠢ࡬ࡨ࠿්ࠦࠧ") + bstack11l1l1111_opy_.get_property(bstack11l11_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࠬ෋")));
  logger.debug(bstack11l11_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩࡃࠧ෌") + bstack11l1l1111_opy_.get_property(bstack11l11_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪࠧ෍")))
  if not bstack1l1lll1l1l_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack11lll111_opy_)
      return
    if sys.argv[1] == bstack11l11_opy_ (u"࠭࠭࠮ࡸࡨࡶࡸ࡯࡯࡯ࠩ෎") or sys.argv[1] == bstack11l11_opy_ (u"ࠧ࠮ࡸࠪා"):
      logger.info(bstack11l11_opy_ (u"ࠨࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡑࡻࡷ࡬ࡴࡴࠠࡔࡆࡎࠤࡻࢁࡽࠨැ").format(__version__))
      return
    if sys.argv[1] == bstack11l11_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨෑ"):
      bstack1111111ll_opy_()
      return
    if sys.argv[1] == bstack11l11_opy_ (u"ࠪࡰࡴࡧࡤࠨි"):
      from browserstack_sdk.bstack11ll1l111_opy_ import bstack1l111111ll_opy_
      bstack11l11llll_opy_()
      bstack1l111111ll_opy_(CONFIG)
      return
  args = sys.argv
  bstack11l11llll_opy_()
  global bstack1ll11l1111_opy_
  try:
    from bstack_utils import constants as bstack11111l11l_opy_
    override_value = CONFIG.get(bstack11l11_opy_ (u"ࠫࡴࡼࡥࡳࡴ࡬ࡨࡪࡒ࡯ࡢࡦࡗࡩࡸࡺࡩ࡯ࡩࠪී"), False)
    bstack1ll11l1111_opy_ = bool(override_value)
  except Exception as e:
    logger.error(bstack11l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡒ࡚ࡊࡘࡒࡊࡆࡈࡣࡑࡕࡁࡅࡡࡗࡉࡘ࡚ࡉࡏࡉ࠽ࠤࢀࢃࠢු").format(e))
    bstack1ll11l1111_opy_ = False
  if bstack1ll11l1111_opy_:
    bstack1llll1111_opy_ = CONFIG.get(bstack11l11_opy_ (u"࠭࡬ࡰࡣࡧࡘࡪࡹࡴࡪࡰࡪࡌࡺࡨࡕࡓࡎࠪ෕")) or bstack11111l11l_opy_.bstack1l11lll11_opy_
    logger.info(bstack11l11_opy_ (u"ࠢࡈ࡮ࡲࡦࡦࡲࠠࡰࡸࡨࡶࡷ࡯ࡤࡦ࡮ࡲࡥࡩࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡥ࡯ࡣࡥࡰࡪࡪࠬࠡࡷࡶ࡭ࡳ࡭ࠠࡩࡷࡥ࠾ࠥࢁࡽࠣූ").format(bstack1llll1111_opy_))
    bstack1ll1l1l1ll_opy_ = bstack1llll1111_opy_
    try:
      bstack11111l11l_opy_.bstack11l111l1_opy_ = bstack1llll1111_opy_
      bstack11111l11l_opy_.bstack1l1111ll1_opy_ = bstack1llll1111_opy_
    except Exception:
      pass
  global bstack1l111lll11_opy_
  global bstack1ll1l111l_opy_
  global bstack11lllll1l_opy_
  global bstack111l1111ll_opy_
  global bstack111llll1ll_opy_
  global bstack1l1lll1l11_opy_
  global bstack111lll11_opy_
  global bstack11l1lll1_opy_
  global bstack1l11l1l11l_opy_
  global bstack1lll111ll_opy_
  global bstack11ll1ll1l1_opy_
  bstack1ll1l111l_opy_ = len(CONFIG.get(bstack11l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ෗"), []))
  if not bstack1l1l1l111l_opy_:
    if args[1] == bstack11l11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩෘ") or args[1] == bstack11l11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫෙ"):
      bstack1l1l1l111l_opy_ = bstack11l11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫේ")
      args = args[2:]
    elif args[1] == bstack11l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫෛ"):
      bstack1l1l1l111l_opy_ = bstack11l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬො")
      args = args[2:]
    elif args[1] == bstack11l11_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ෝ"):
      bstack1l1l1l111l_opy_ = bstack11l11_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧෞ")
      args = args[2:]
    elif args[1] == bstack11l11_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪෟ"):
      bstack1l1l1l111l_opy_ = bstack11l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ෠")
      args = args[2:]
    elif args[1] == bstack11l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ෡"):
      bstack1l1l1l111l_opy_ = bstack11l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ෢")
      args = args[2:]
    elif args[1] == bstack11l11_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭෣"):
      bstack1l1l1l111l_opy_ = bstack11l11_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ෤")
      args = args[2:]
    else:
      if not bstack11l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ෥") in CONFIG or str(CONFIG[bstack11l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ෦")]).lower() in [bstack11l11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ෧"), bstack11l11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬ෨")]:
        bstack1l1l1l111l_opy_ = bstack11l11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ෩")
        args = args[1:]
      elif str(CONFIG[bstack11l11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ෪")]).lower() == bstack11l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭෫"):
        bstack1l1l1l111l_opy_ = bstack11l11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ෬")
        args = args[1:]
      elif str(CONFIG[bstack11l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ෭")]).lower() == bstack11l11_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ෮"):
        bstack1l1l1l111l_opy_ = bstack11l11_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ෯")
        args = args[1:]
      elif str(CONFIG[bstack11l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ෰")]).lower() == bstack11l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭෱"):
        bstack1l1l1l111l_opy_ = bstack11l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧෲ")
        args = args[1:]
      elif str(CONFIG[bstack11l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫෳ")]).lower() == bstack11l11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ෴"):
        bstack1l1l1l111l_opy_ = bstack11l11_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ෵")
        args = args[1:]
      else:
        os.environ[bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭෶")] = bstack1l1l1l111l_opy_
        bstack1l1lll1111_opy_(bstack111llll11_opy_)
  os.environ[bstack11l11_opy_ (u"ࠬࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉ࠭෷")] = bstack1l1l1l111l_opy_
  bstack1llll11l1l_opy_ = bstack1l1l1l111l_opy_
  if cli.is_enabled(CONFIG):
    try:
      bstack1lll1ll1l1_opy_ = bstack1l1ll11l1_opy_[bstack11l11_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙࠳ࡂࡅࡆࠪ෸")] if bstack1l1l1l111l_opy_ == bstack11l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ෹") and bstack11lll1111l_opy_() else bstack1l1l1l111l_opy_
      bstack1l11l11111_opy_.invoke(bstack11ll111111_opy_.bstack1l1llllll1_opy_, bstack11ll1lllll_opy_(
        sdk_version=__version__,
        path_config=bstack11ll11l1l_opy_(),
        path_project=os.getcwd(),
        test_framework=bstack1lll1ll1l1_opy_,
        frameworks=[bstack1lll1ll1l1_opy_],
        framework_versions={
          bstack1lll1ll1l1_opy_: bstack1ll1llll_opy_(bstack11l11_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧ෺") if bstack1l1l1l111l_opy_ in [bstack11l11_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ෻"), bstack11l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ෼"), bstack11l11_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ෽")] else bstack1l1l1l111l_opy_)
        },
        bs_config=CONFIG
      ))
      if cli.config and cli.config.get(bstack11l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠢ෾"), None):
        CONFIG[bstack11l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣ෿")] = cli.config.get(bstack11l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤ฀"), None)
    except Exception as e:
      bstack1l11l11111_opy_.invoke(bstack11ll111111_opy_.bstack111111l1l_opy_, e.__traceback__, 1)
    if bstack11lll1l11_opy_:
      CONFIG[bstack11l11_opy_ (u"ࠣࡣࡳࡴࠧก")] = cli.config[bstack11l11_opy_ (u"ࠤࡤࡴࡵࠨข")]
      logger.info(bstack1ll11l1l_opy_.format(CONFIG[bstack11l11_opy_ (u"ࠪࡥࡵࡶࠧฃ")]))
  else:
    bstack1l11l11111_opy_.clear()
  global bstack1ll1111l1l_opy_
  global bstack11llllll11_opy_
  if bstack1l1l1ll1_opy_:
    try:
      bstack1lllll111_opy_ = datetime.datetime.now()
      os.environ[bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ค")] = bstack1l1l1l111l_opy_
      bstack11l1l1l11l_opy_ = bstack111l1lllll_opy_.bstack1l11111111_opy_(EVENTS.bstack111l11l1l_opy_)
      try:
        logger.info(bstack11l11_opy_ (u"࡙ࠧࡥ࡯ࡦ࡬ࡲ࡬ࠦࡓࡅࡍࠣࡘࡪࡹࡴࠡࡃࡷࡸࡪࡳࡰࡵࡧࡧࠤࡪࡼࡥ࡯ࡶࠥฅ"))
        bstack1lll11l11l_opy_(bstack1lll11lll1_opy_, CONFIG)
      finally:
        bstack111l1lllll_opy_.end(EVENTS.bstack111l11l1l_opy_.value, bstack11l1l1l11l_opy_ + bstack11l11_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨฆ"), bstack11l1l1l11l_opy_ + bstack11l11_opy_ (u"ࠢ࠻ࡧࡱࡨࠧง"), status=True, failure=None, test_name=None)
      cli.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠣࡪࡷࡸࡵࡀࡳࡥ࡭ࡢࡸࡪࡹࡴࡠࡣࡷࡸࡪࡳࡰࡵࡧࡧࠦจ"), datetime.datetime.now() - bstack1lllll111_opy_)
    except Exception as e:
      logger.debug(bstack1l11l1ll_opy_.format(str(e)))
  global bstack11l111111_opy_
  global bstack11l111l1ll_opy_
  global bstack111ll1lll1_opy_
  global bstack11ll1l1l1_opy_
  global bstack1ll1ll1l1l_opy_
  global bstack1llll1ll_opy_
  global bstack11ll1l1111_opy_
  global bstack111llll11l_opy_
  global bstack11l1l1ll_opy_
  global bstack111l1l111_opy_
  global bstack1l1l1ll1ll_opy_
  global bstack1l1111l1ll_opy_
  global bstack1l1l1ll11l_opy_
  global bstack1ll11111l1_opy_
  global bstack11l1l1l1l_opy_
  global bstack11ll11ll_opy_
  global bstack111lllllll_opy_
  global bstack1l111l1ll1_opy_
  global bstack1ll111111l_opy_
  global bstack11l1ll1l1_opy_
  global bstack11l1ll11l1_opy_
  global bstack1lll111l_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11l111111_opy_ = webdriver.Remote.__init__
    bstack11l111l1ll_opy_ = WebDriver.quit
    bstack1l1111l1ll_opy_ = WebDriver.close
    bstack11ll11ll_opy_ = WebDriver.get
    bstack1lll111l_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1ll1111l1l_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack1ll1llll11_opy_
    bstack11llllll11_opy_ = bstack1ll1llll11_opy_()
  except Exception as e:
    pass
  try:
    global bstack11l111l1l1_opy_
    from QWeb.keywords import browser
    bstack11l111l1l1_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1l1l11l11l_opy_(CONFIG) and bstack1l1l1l1lll_opy_():
    if bstack111l1lll1_opy_() < version.parse(bstack11ll111ll1_opy_):
      logger.error(bstack1111lllll_opy_.format(bstack111l1lll1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack11l11_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪฉ")) and callable(getattr(RemoteConnection, bstack11l11_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫช"))):
          RemoteConnection._get_proxy_url = bstack1l11ll1l1_opy_
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          ClientConfig.get_proxy_url = bstack1l11ll1l1_opy_
      except Exception as e:
        logger.error(bstack11l1111l1_opy_.format(str(e)))
  if not CONFIG.get(bstack11l11_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭ซ"), False) and not bstack1l1l1ll1_opy_:
    logger.info(bstack11ll111l1l_opy_)
  bstack111l11l1_opy_ = not cli.is_enabled(CONFIG) and bstack1l1l1l111l_opy_ not in [bstack11l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ฌ")]
  bstack1111ll111_opy_ = bstack111l11l1_opy_ and bstack11l11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪญ") in CONFIG and str(CONFIG[bstack11l11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫฎ")]).lower() != bstack11l11_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧฏ")
  bstack1llll111l1_opy_ = bstack111l11l1_opy_ and not bstack1111ll111_opy_ and (bstack1l1l1l111l_opy_ != bstack11l11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩฐ") or (bstack1l1l1l111l_opy_ == bstack11l11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪฑ") and not bstack1l1l1ll1_opy_))
  if bstack1l1l1l111l_opy_ not in [bstack11l11_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬฒ")]:
    bstack11l11llll1_opy_(os.path.join(os.getcwd(), bstack11l11_opy_ (u"ࠬࡲ࡯ࡨࠩณ"), bstack11l11_opy_ (u"࠭࡫ࡦࡻ࠰ࡱࡪࡺࡲࡪࡥࡶ࠲࡯ࡹ࡯࡯ࠩด")), logger)
  if (bstack1l1l1l111l_opy_ in [bstack11l11_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ต"), bstack11l11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧถ"), bstack11l11_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪท")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      try:
        from pabot.pabot import QueueItem
        from pabot import pabot
      except Exception as e:
        logger.warning(bstack1l1l11l11_opy_ + str(e))
      if not is_robot_playwright_installed():
        try:
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
          WebDriverCreator._get_ff_profile = bstack1ll111l1l_opy_
          bstack1llll1ll_opy_ = WebDriverCache.close
        except Exception as e:
          logger.warning(bstack11ll11lll_opy_ + str(e))
        try:
          from AppiumLibrary.utils.applicationcache import ApplicationCache
          bstack1ll1ll1l1l_opy_ = ApplicationCache.close
        except Exception as e:
          logger.debug(bstack1lll1111l_opy_ + str(e))
    except Exception as e:
      bstack1l11l1ll1l_opy_(e, bstack11ll11lll_opy_)
    if bstack1l1l1l111l_opy_ != bstack11l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫธ"):
      bstack1llll1llll_opy_()
    bstack111ll1lll1_opy_ = Output.start_test
    bstack11ll1l1l1_opy_ = Output.end_test
    bstack11ll1l1111_opy_ = TestStatus.__init__
    bstack11l1l1ll_opy_ = pabot._run
    bstack111l1l111_opy_ = QueueItem.__init__
    bstack1l1l1ll1ll_opy_ = pabot._create_command_for_execution
    bstack11l1ll1l1_opy_ = pabot._report_results
  if bstack1l1l1l111l_opy_ == bstack11l11_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫน"):
    global bstack1l11l11ll_opy_
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l11l1ll1l_opy_(e, bstack1111lll1l1_opy_)
    bstack1l1l1ll11l_opy_ = Runner.run_hook
    bstack1ll11111l1_opy_ = Runner.load_hooks
    bstack11l1l1l1l_opy_ = Step.run
    try:
      sig = inspect.signature(bstack1l1l1ll11l_opy_)
      params = list(sig.parameters.keys())
      bstack1l11l11ll_opy_ = bstack11l11_opy_ (u"ࠬࡩ࡯࡯ࡶࡨࡼࡹ࠭บ") in params
      logger.info(bstack11l11_opy_ (u"࠭ࡄࡦࡶࡨࡧࡹ࡫ࡤࠡࡤࡨ࡬ࡦࡼࡥࠡࡴࡸࡲࡤ࡮࡯ࡰ࡭ࠣࡷ࡮࡭࡮ࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪป").format(bstack11l11_opy_ (u"ࠧ࠲࠰࠵࠲࠻ࠦࠨࡸ࡫ࡷ࡬ࠥࡩ࡯࡯ࡶࡨࡼࡹ࠯ࠧผ") if bstack1l11l11ll_opy_ else bstack11l11_opy_ (u"ࠨ࠳࠱࠷࠰ࠦࠨࡸ࡫ࡷ࡬ࡴࡻࡴࠡࡥࡲࡲࡹ࡫ࡸࡵࠫࠪฝ")))
    except Exception as e:
      logger.debug(bstack11l11_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡦࡸࠥࡨࡥࡩࡣࡹࡩࠥࡸࡵ࡯ࡡ࡫ࡳࡴࡱࠠࡴ࡫ࡪࡲࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧพ").format(str(e)))
      bstack1l11l11ll_opy_ = None
  if bstack1l1l1l111l_opy_ == bstack11l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪฟ"):
    try:
      from _pytest.config import Config
      bstack1l111l1ll1_opy_ = Config.getoption
      from _pytest import runner
      bstack1ll111111l_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warning(bstack11l11_opy_ (u"ࠦࠪࡹ࠺ࠡࠧࡶࠦภ"), bstack11lllll11_opy_, str(e))
    try:
      from pytest_bdd import reporting
      bstack11l1ll11l1_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack11l11_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡴࠦࡲࡶࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࡸ࠭ม"))
    if bstack1l1111111l_opy_():
      logger.warning(bstack11l1ll1ll_opy_[bstack11l11_opy_ (u"࠭ࡓࡅࡍ࠰ࡋࡊࡔ࠭࠱࠲࠸ࠫย")])
  try:
    framework_name = bstack11l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ร") if bstack1l1l1l111l_opy_ in [bstack11l11_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧฤ"), bstack11l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨล"), bstack11l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫฦ")] else bstack1l1l1l1ll1_opy_(bstack1l1l1l111l_opy_)
    bstack1l1l1l1l1l_opy_ = {
      bstack11l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࠬว"): bstack11l11_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧศ") if bstack1l1l1l111l_opy_ == bstack11l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ษ") and bstack11lll1111l_opy_() else framework_name,
      bstack11l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫส"): bstack1ll1llll_opy_(framework_name),
      bstack11l11_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ห"): __version__,
      bstack11l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦࠪฬ"): bstack1l1l1l111l_opy_
    }
    if bstack1l1l1l111l_opy_ in bstack11l1111l_opy_ + bstack1l1l111l11_opy_:
      if bstack1lllll111l_opy_.bstack1lll1l1l1_opy_(CONFIG):
        if bstack11l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪอ") in CONFIG:
          os.environ[bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬฮ")] = os.getenv(bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ฯ"), json.dumps(CONFIG[bstack11l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ะ")]))
          CONFIG[bstack11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧั")].pop(bstack11l11_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭า"), None)
          CONFIG[bstack11l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩำ")].pop(bstack11l11_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨิ"), None)
        bstack1l1l1l1l1l_opy_[bstack11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫี")] = {
          bstack11l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪึ"): bstack11l11_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨื"),
          bstack11l11_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨุ"): str(bstack111l1lll1_opy_())
        }
    bstack1l11llll1l_opy_, bstack11lllll1_opy_ = None, {}
    bstack1ll111ll_opy_ = None
    bstack1ll1ll111l_opy_ = None
    def bstack1l1ll111l1_opy_():
      if bstack1111ll111_opy_:
        bstack1l11ll11l1_opy_()
      elif bstack1llll111l1_opy_:
        bstack11l1l1l1l1_opy_()
    def bstack111ll1ll1_opy_():
      nonlocal bstack1l11llll1l_opy_, bstack11lllll1_opy_
      if bstack1l1l1l111l_opy_ not in [bstack11l11_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ูࠩ")] and not cli.is_running():
        bstack1l11llll1l_opy_, bstack11lllll1_opy_ = bstack1ll111l1_opy_.launch(CONFIG, bstack1l1l1l1l1l_opy_)
    if bstack1111ll111_opy_ or bstack1llll111l1_opy_:
      bstack1ll111ll_opy_ = threading.Thread(target=bstack1l1ll111l1_opy_)
      bstack1ll111ll_opy_.start()
    if bstack1l1l1l111l_opy_ not in [bstack11l11_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ฺࠪ")] and not cli.is_running():
      bstack1ll1ll111l_opy_ = threading.Thread(target=bstack111ll1ll1_opy_)
      bstack1ll1ll111l_opy_.start()
    if bstack1ll111ll_opy_:
      bstack1ll111ll_opy_.join()
    if bstack1ll1ll111l_opy_:
      bstack1ll1ll111l_opy_.join()
    if bstack11lllll1_opy_.get(bstack11l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ฻")) is not None and bstack1lllll111l_opy_.bstack1ll11l1l1l_opy_(CONFIG) is None:
      value = bstack11lllll1_opy_[bstack11l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ฼")].get(bstack11l11_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭฽"))
      if value is not None:
          CONFIG[bstack11l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭฾")] = value
      else:
        logger.debug(bstack11l11_opy_ (u"ࠢࡏࡱࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡨࡦࡺࡡࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡶࡪࡹࡰࡰࡰࡶࡩࠧ฿"))
  except Exception as e:
    logger.debug(bstack1l1lll1lll_opy_.format(bstack11l11_opy_ (u"ࠨࡖࡨࡷࡹࡎࡵࡣࠩเ"), str(e)))
  if bstack1l1l1l111l_opy_ == bstack11l11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩแ"):
    bstack11lllll1l_opy_ = True
    if bstack1l1l1ll1_opy_ and bstack1l1lll1l1l_opy_:
      bstack1l1lll1l11_opy_ = CONFIG.get(bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧโ"), {}).get(bstack11l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ใ"))
      bstack1l1l1lll11_opy_(bstack11l1l1lll_opy_)
    elif bstack1l1l1ll1_opy_:
      bstack1l1lll1l11_opy_ = CONFIG.get(bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩไ"), {}).get(bstack11l11_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨๅ"))
      global bstack111l1llll1_opy_
      try:
        if bstack1ll1l1ll1_opy_(bstack1l1l1ll1_opy_[bstack11l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪๆ")]) and multiprocessing.current_process().name == bstack11l11_opy_ (u"ࠨ࠲ࠪ็"):
          bstack1l1l1ll1_opy_[bstack11l11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩ่ࠬ")].remove(bstack11l11_opy_ (u"ࠪ࠱ࡲ้࠭"))
          bstack1l1l1ll1_opy_[bstack11l11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫๊ࠧ")].remove(bstack11l11_opy_ (u"ࠬࡶࡤࡣ๋ࠩ"))
          bstack1l1l1ll1_opy_[bstack11l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ์")] = bstack1l1l1ll1_opy_[bstack11l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪํ")][0]
          with open(bstack1l1l1ll1_opy_[bstack11l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ๎")], bstack11l11_opy_ (u"ࠩࡵࠫ๏")) as f:
            bstack111l11l111_opy_ = f.read()
          bstack1l11l111l1_opy_ = bstack11l11_opy_ (u"ࠥࠦࠧ࡬ࡲࡰ࡯ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡨࡰࠦࡩ࡮ࡲࡲࡶࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦ࠽ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪ࠮ࡻࡾࠫ࠾ࠤ࡫ࡸ࡯࡮ࠢࡳࡨࡧࠦࡩ࡮ࡲࡲࡶࡹࠦࡐࡥࡤ࠾ࠤࡴ࡭࡟ࡥࡤࠣࡁࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡦࡨࡪࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠩࡵࡨࡰ࡫࠲ࠠࡢࡴࡪ࠰ࠥࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠡ࠿ࠣ࠴࠮ࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺࡲࡺ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡥࡷ࡭ࠠ࠾ࠢࡶࡸࡷ࠮ࡩ࡯ࡶࠫࡥࡷ࡭ࠩࠬ࠳࠳࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡩࡽࡩࡥࡱࡶࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡡࡴࠢࡨ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡶࡡࡴࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡱࡪࡣࡩࡨࠨࡴࡧ࡯ࡪ࠱ࡧࡲࡨ࠮ࡷࡩࡲࡶ࡯ࡳࡣࡵࡽ࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡓࡨࡧ࠴ࡤࡰࡡࡥࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮ࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣࠪࠬ࠲ࡸ࡫ࡴࡠࡶࡵࡥࡨ࡫ࠨࠪ࡞ࡱࠦࠧࠨ๐").format(str(bstack1l1l1ll1_opy_))
          bstack11l1llll_opy_ = bstack1l11l111l1_opy_ + bstack111l11l111_opy_
          bstack1l111111l1_opy_ = bstack1l1l1ll1_opy_[bstack11l11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ๑")] + bstack11l11_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥࡴࡦ࡯ࡳ࠲ࡵࡿࠧ๒")
          with open(bstack1l111111l1_opy_, bstack11l11_opy_ (u"࠭ࡷࠨ๓")):
            pass
          with open(bstack1l111111l1_opy_, bstack11l11_opy_ (u"ࠢࡸ࠭ࠥ๔")) as f:
            f.write(bstack11l1llll_opy_)
          import subprocess
          bstack11l11lll1_opy_ = subprocess.run([bstack11l11_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࠣ๕"), bstack1l111111l1_opy_])
          if os.path.exists(bstack1l111111l1_opy_):
            os.unlink(bstack1l111111l1_opy_)
          os._exit(bstack11l11lll1_opy_.returncode)
        else:
          if bstack1ll1l1ll1_opy_(bstack1l1l1ll1_opy_[bstack11l11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ๖")]):
            bstack1l1l1ll1_opy_[bstack11l11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭๗")].remove(bstack11l11_opy_ (u"ࠫ࠲ࡳࠧ๘"))
            bstack1l1l1ll1_opy_[bstack11l11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ๙")].remove(bstack11l11_opy_ (u"࠭ࡰࡥࡤࠪ๚"))
            bstack1l1l1ll1_opy_[bstack11l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ๛")] = bstack1l1l1ll1_opy_[bstack11l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ๜")][0]
          bstack1l1l1lll11_opy_(bstack11l1l1lll_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1l1l1ll1_opy_[bstack11l11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ๝")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack11l11_opy_ (u"ࠪࡣࡤࡴࡡ࡮ࡧࡢࡣࠬ๞")] = bstack11l11_opy_ (u"ࠫࡤࡥ࡭ࡢ࡫ࡱࡣࡤ࠭๟")
          mod_globals[bstack11l11_opy_ (u"ࠬࡥ࡟ࡧ࡫࡯ࡩࡤࡥࠧ๠")] = os.path.abspath(bstack1l1l1ll1_opy_[bstack11l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ๡")])
          exec(open(bstack1l1l1ll1_opy_[bstack11l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ๢")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack11l11_opy_ (u"ࠨࡅࡤࡹ࡬࡮ࡴࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠨ๣").format(str(e)))
          for driver in bstack111l1llll1_opy_:
            bstack1l11l1lll1_opy_.append({
              bstack11l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ๤"): bstack1l1l1ll1_opy_[bstack11l11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭๥")],
              bstack11l11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ๦"): str(e),
              bstack11l11_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ๧"): multiprocessing.current_process().name
            })
            bstack1ll1l1l1_opy_(driver, bstack11l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭๨"), bstack11l11_opy_ (u"ࠢࡔࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥ๩") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack111l1llll1_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack11lll1l11_opy_, CONFIG, logger)
      bstack1l111lll1_opy_()
      bstack1l1111l1_opy_()
      percy.bstack1ll11ll11_opy_()
      bstack11ll1lll1_opy_ = {
        bstack11l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ๪"): args[0],
        bstack11l11_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩ๫"): CONFIG,
        bstack11l11_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫ๬"): bstack1ll1l1l1ll_opy_,
        bstack11l11_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭๭"): bstack11lll1l11_opy_
      }
      if bstack11l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ๮") in CONFIG:
        bstack1lll11ll11_opy_ = bstack11lll1ll_opy_(args, logger, CONFIG, bstack111l1l11_opy_, bstack1ll1l111l_opy_)
        bstack11l1lll1_opy_ = bstack1lll11ll11_opy_.bstack1l1111111_opy_(run_on_browserstack, bstack11ll1lll1_opy_, bstack1ll1l1ll1_opy_(args))
      else:
        if bstack1ll1l1ll1_opy_(args):
          bstack11ll1lll1_opy_[bstack11l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ๯")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack11ll1lll1_opy_,))
          test.start()
          test.join()
        else:
          bstack1l1l1lll11_opy_(bstack11l1l1lll_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack11l11_opy_ (u"ࠧࡠࡡࡱࡥࡲ࡫࡟ࡠࠩ๰")] = bstack11l11_opy_ (u"ࠨࡡࡢࡱࡦ࡯࡮ࡠࡡࠪ๱")
          mod_globals[bstack11l11_opy_ (u"ࠩࡢࡣ࡫࡯࡬ࡦࡡࡢࠫ๲")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1l1l1l111l_opy_ == bstack11l11_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ๳") or bstack1l1l1l111l_opy_ == bstack11l11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ๴"):
    percy.init(bstack11lll1l11_opy_, CONFIG, logger)
    percy.bstack1ll11ll11_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1l11l1ll1l_opy_(e, bstack11ll11lll_opy_)
    bstack1l111lll1_opy_()
    bstack1l1l1lll11_opy_(bstack11ll1111l_opy_)
    if bstack111l1l11_opy_:
      bstack111l11ll1l_opy_(bstack11ll1111l_opy_, args)
      if bstack11l11_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ๵") in args:
        i = args.index(bstack11l11_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ๶"))
        args.pop(i)
        args.pop(i)
      if bstack11l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ๷") not in CONFIG:
        CONFIG[bstack11l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ๸")] = [{}]
        bstack1ll1l111l_opy_ = 1
      if bstack1l111lll11_opy_ == 0:
        bstack1l111lll11_opy_ = 1
      args.insert(0, str(bstack1l111lll11_opy_))
      args.insert(0, str(bstack11l11_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ๹")))
    if bstack1ll111l1_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1llllll111_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack111ll1ll11_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack11l11_opy_ (u"ࠥࡖࡔࡈࡏࡕࡡࡒࡔ࡙ࡏࡏࡏࡕࠥ๺"),
        ).parse_args(bstack1llllll111_opy_)
        bstack11l1llll1l_opy_ = args.index(bstack1llllll111_opy_[0]) if len(bstack1llllll111_opy_) > 0 else len(args)
        args.insert(bstack11l1llll1l_opy_, str(bstack11l11_opy_ (u"ࠫ࠲࠳࡬ࡪࡵࡷࡩࡳ࡫ࡲࠨ๻")))
        args.insert(bstack11l1llll1l_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡸ࡯ࡣࡱࡷࡣࡱ࡯ࡳࡵࡧࡱࡩࡷ࠴ࡰࡺࠩ๼"))))
        if bstack1l11l1l1ll_opy_.bstack11l11lll11_opy_(CONFIG):
          args.insert(bstack11l1llll1l_opy_, str(bstack11l11_opy_ (u"࠭࠭࠮࡮࡬ࡷࡹ࡫࡮ࡦࡴࠪ๽")))
          args.insert(bstack11l1llll1l_opy_ + 1, str(bstack11l11_opy_ (u"ࠧࡓࡧࡷࡶࡾࡌࡡࡪ࡮ࡨࡨ࠿ࢁࡽࠨ๾").format(bstack1l11l1l1ll_opy_.bstack11l1l1lll1_opy_(CONFIG))))
        if bstack1ll1l11lll_opy_(os.environ.get(bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓ࠭๿"))) and str(os.environ.get(bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭຀"), bstack11l11_opy_ (u"ࠪࡲࡺࡲ࡬ࠨກ"))) != bstack11l11_opy_ (u"ࠫࡳࡻ࡬࡭ࠩຂ"):
          for bstack1ll1llll1l_opy_ in bstack111ll1ll11_opy_:
            args.remove(bstack1ll1llll1l_opy_)
          test_files = os.environ.get(bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠩ຃")).split(bstack11l11_opy_ (u"࠭ࠬࠨຄ"))
          for bstack111l11lll_opy_ in test_files:
            args.append(bstack111l11lll_opy_)
      except Exception as e:
        logger.error(bstack11l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡧࡴࡵࡣࡦ࡬࡮ࡴࡧࠡ࡮࡬ࡷࡹ࡫࡮ࡦࡴࠣࡪࡴࡸࠠࡼࡿ࠱ࠤࡊࡸࡲࡰࡴࠣ࠱ࠥࢁࡽࠣ຅").format(bstack1lllll1lll_opy_, e))
    pabot.main(args)
  elif bstack1l1l1l111l_opy_ == bstack11l11_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩຆ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1l11l1ll1l_opy_(e, bstack11ll11lll_opy_)
    for a in args:
      if bstack11l11_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘࠨງ") in a:
        bstack111llll1ll_opy_ = int(a.split(bstack11l11_opy_ (u"ࠪ࠾ࠬຈ"))[1])
      if bstack11l11_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨຉ") in a:
        bstack1l1lll1l11_opy_ = str(a.split(bstack11l11_opy_ (u"ࠬࡀࠧຊ"))[1])
      if bstack11l11_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘ࠭຋") in a:
        bstack111lll11_opy_ = str(a.split(bstack11l11_opy_ (u"ࠧ࠻ࠩຌ"))[1])
    bstack111l1llll_opy_ = None
    bstack11l11ll1ll_opy_ = None
    if bstack11l11_opy_ (u"ࠨ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠧຍ") in args:
      i = args.index(bstack11l11_opy_ (u"ࠩ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠨຎ"))
      args.pop(i)
      bstack111l1llll_opy_ = args.pop(i)
    if bstack11l11_opy_ (u"ࠪ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽ࠭ຏ") in args:
      i = args.index(bstack11l11_opy_ (u"ࠫ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࠧຐ"))
      args.pop(i)
      bstack11l11ll1ll_opy_ = args.pop(i)
    if bstack111l1llll_opy_ is not None:
      global bstack11l111l111_opy_
      bstack11l111l111_opy_ = bstack111l1llll_opy_
    if bstack11l11ll1ll_opy_ is not None and int(bstack111llll1ll_opy_) < 0:
      bstack111llll1ll_opy_ = int(bstack11l11ll1ll_opy_)
    if cli.is_enabled(CONFIG):
      if cli.bstack11111l1l_opy_():
        bstack1l11l11111_opy_.invoke(bstack11ll111111_opy_.CONNECT, bstack111l1ll1l_opy_())
    bstack1l1l1lll11_opy_(bstack11ll1111l_opy_)
    run_cli(args)
    if bstack11l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩຑ") in multiprocessing.current_process().__dict__.keys():
      for bstack1l1ll1l111_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1l11l1lll1_opy_.append(bstack1l1ll1l111_opy_)
  elif bstack1l1l1l111l_opy_ == bstack11l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ຒ"):
    bstack11llll1lll_opy_ = bstack1ll11l1l11_opy_(args, logger, CONFIG, bstack111l1l11_opy_)
    bstack11llll1lll_opy_.bstack11ll11l1ll_opy_()
    bstack1l111lll1_opy_()
    bstack111l1111ll_opy_ = True
    bstack1lll111ll_opy_ = bstack11llll1lll_opy_.bstack11l11l111_opy_()
    bstack11llll1lll_opy_.bstack11ll1lll1_opy_(bstack1llllllll1_opy_)
    bstack11llll1lll_opy_.bstack11111l1ll_opy_()
    bstack1ll11l111_opy_(bstack1l1l1l111l_opy_, CONFIG, bstack11llll1lll_opy_.bstack111l1lll1l_opy_())
    bstack11ll11ll1l_opy_.end(EVENTS.bstack11lllll1ll_opy_.value, EVENTS.bstack11lllll1ll_opy_.value + bstack11l11_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢຓ"), EVENTS.bstack11lllll1ll_opy_.value + bstack11l11_opy_ (u"ࠣ࠼ࡨࡲࡩࠨດ"), status=True, failure=None, test_name=bstack11l1111lll_opy_)
    bstack1l111ll11_opy_ = bstack11llll1lll_opy_.bstack1l1111111_opy_(bstack11l11ll1l1_opy_, {
      bstack11l11_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩຕ"): CONFIG,
      bstack11l11_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫຖ"): bstack1ll1l1l1ll_opy_,
      bstack11l11_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ທ"): bstack11lll1l11_opy_,
      bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨຘ"): bstack111l1l11_opy_,
      bstack11l11_opy_ (u"࠭ࡏࡗࡇࡕࡖࡎࡊࡅࡠࡎࡒࡅࡉࡥࡔࡆࡕࡗࡍࡓࡍࠧນ"): bstack1ll11l1111_opy_
    })
    if not bstack1l1l1ll1_opy_:
      bstack1l1ll1l1l_opy_ = bstack111l1lllll_opy_.bstack1l11111111_opy_(EVENTS.bstack111l11l11l_opy_.value)
    try:
      bstack1l1lll111_opy_, bstack1l11lll111_opy_ = map(list, zip(*bstack1l111ll11_opy_))
      bstack1l11l1l11l_opy_ = bstack1l1lll111_opy_[0]
      for status_code in bstack1l11lll111_opy_:
        if status_code != 0:
          bstack11ll1ll1l1_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack11l11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡦࡼࡥࠡࡧࡵࡶࡴࡸࡳࠡࡣࡱࡨࠥࡹࡴࡢࡶࡸࡷࠥࡩ࡯ࡥࡧ࠱ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠ࠻ࠢࡾࢁࠧບ").format(str(e)))
  elif bstack1l1l1l111l_opy_ == bstack11l11_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨປ"):
    try:
      from behave.__main__ import main as bstack1l11l111_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1l11l1ll1l_opy_(e, bstack1111lll1l1_opy_)
    bstack1l111lll1_opy_()
    bstack111l1111ll_opy_ = True
    bstack1lll111l1l_opy_ = 1
    if bstack11l11_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩຜ") in CONFIG:
      bstack1lll111l1l_opy_ = CONFIG[bstack11l11_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪຝ")]
    if bstack11l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧພ") in CONFIG:
      bstack11l1111l1l_opy_ = int(bstack1lll111l1l_opy_) * int(len(CONFIG[bstack11l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨຟ")]))
    else:
      bstack11l1111l1l_opy_ = int(bstack1lll111l1l_opy_)
    config = Configuration(args)
    bstack1l1l1lll1_opy_ = config.paths
    if len(bstack1l1l1lll1_opy_) == 0:
      import glob
      pattern = bstack11l11_opy_ (u"࠭ࠪࠫ࠱࠭࠲࡫࡫ࡡࡵࡷࡵࡩࠬຠ")
      bstack1l11l11l_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1l11l11l_opy_)
      config = Configuration(args)
      bstack1l1l1lll1_opy_ = config.paths
    bstack1111l1ll1_opy_ = [os.path.normpath(item) for item in bstack1l1l1lll1_opy_]
    bstack1ll1l11l1_opy_ = [os.path.normpath(item) for item in args]
    bstack11111l1l1_opy_ = [item for item in bstack1ll1l11l1_opy_ if item not in bstack1111l1ll1_opy_]
    import platform as pf
    if pf.system().lower() == bstack11l11_opy_ (u"ࠧࡸ࡫ࡱࡨࡴࡽࡳࠨມ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1111l1ll1_opy_ = [str(PurePosixPath(PureWindowsPath(bstack11llllll_opy_)))
                    for bstack11llllll_opy_ in bstack1111l1ll1_opy_]
    bstack1llll111_opy_ = []
    for spec in bstack1111l1ll1_opy_:
      bstack1l11l1l1_opy_ = []
      bstack1l11l1l1_opy_ += bstack11111l1l1_opy_
      bstack1l11l1l1_opy_.append(spec)
      bstack1llll111_opy_.append(bstack1l11l1l1_opy_)
    execution_items = []
    for bstack1l11l1l1_opy_ in bstack1llll111_opy_:
      if bstack11l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫຢ") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬຣ")]):
          item = {}
          item[bstack11l11_opy_ (u"ࠪࡥࡷ࡭ࠧ຤")] = bstack11l11_opy_ (u"ࠫࠥ࠭ລ").join(bstack1l11l1l1_opy_)
          item[bstack11l11_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ຦")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack11l11_opy_ (u"࠭ࡡࡳࡩࠪວ")] = bstack11l11_opy_ (u"ࠧࠡࠩຨ").join(bstack1l11l1l1_opy_)
        item[bstack11l11_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧຩ")] = 0
        execution_items.append(item)
    bstack11111111l_opy_ = bstack1l1l11111l_opy_(execution_items, bstack11l1111l1l_opy_)
    for execution_item in bstack11111111l_opy_:
      bstack11l1ll1111_opy_ = []
      for item in execution_item:
        bstack11l1ll1111_opy_.append(bstack111ll11l11_opy_(name=str(item[bstack11l11_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨສ")]),
                                             target=bstack111l1l1l1l_opy_,
                                             args=(item[bstack11l11_opy_ (u"ࠪࡥࡷ࡭ࠧຫ")],)))
      for t in bstack11l1ll1111_opy_:
        t.start()
      for t in bstack11l1ll1111_opy_:
        t.join()
  else:
    bstack1l1lll1111_opy_(bstack111llll11_opy_)
  if not bstack1l1l1ll1_opy_:
    bstack1lll11l1_opy_()
    if bstack1l1ll1l1l_opy_:
      bstack111l1lllll_opy_.end(EVENTS.bstack111l11l11l_opy_.value, bstack1l1ll1l1l_opy_ + bstack11l11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦຬ"), bstack1l1ll1l1l_opy_ + bstack11l11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥອ"), status=True, failure=None, test_name=None)
  logger_utils.bstack111l1ll111_opy_()
def browserstack_initialize(bstack11l11111ll_opy_=None):
  logger.info(bstack11l11_opy_ (u"࠭ࡒࡶࡰࡱ࡭ࡳ࡭ࠠࡔࡆࡎࠤࡼ࡯ࡴࡩࠢࡤࡶ࡬ࡹ࠺ࠡࠩຮ") + str(bstack11l11111ll_opy_))
  run_on_browserstack(bstack11l11111ll_opy_, None, True)
@measure(event_name=EVENTS.bstack1ll11l1lll_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l111l11l_opy_=bstack11l1111lll_opy_)
def bstack1lll11l1_opy_():
  global CONFIG
  global bstack1llll11l1l_opy_
  global bstack11ll1ll1l1_opy_
  global bstack111ll1111_opy_
  global bstack11l1l1111_opy_
  bstack1l1ll111l_opy_.bstack11l1lll1l_opy_()
  if cli.is_running():
    bstack1l11l11111_opy_.invoke(bstack11ll111111_opy_.bstack11l1l111l1_opy_)
  else:
    bstack1l11ll1l_opy_ = bstack1l11l1l1ll_opy_.bstack111l1lll_opy_(config=CONFIG)
    bstack1l11ll1l_opy_.bstack11l1ll111_opy_(CONFIG)
  hashed_id = None
  bstack1l11l1l111_opy_ = None
  def bstack1111l11l1_opy_():
    try:
      if bstack1llll11l1l_opy_ == bstack11l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧຯ"):
        if not cli.is_enabled(CONFIG):
          bstack1ll111l1_opy_.stop()
      else:
        bstack1ll111l1_opy_.stop()
    except Exception as e:
      logger.debug(bstack11l11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡴࡶࡲࡴࡵ࡯࡮ࡨࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࢀࢃࠢະ").format(e))
  def bstack11l11l1ll_opy_():
    try:
      if not cli.is_enabled(CONFIG):
        bstack11l1ll111l_opy_.bstack11l1lll111_opy_()
    except Exception as e:
      logger.debug(bstack11l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡲࡵ࡭ࡳࡺࡩ࡯ࡩࠣࡦࡺ࡯࡬ࡥࠢ࡯࡭ࡳࡱ࠺ࠡࡽࢀࠦັ").format(e))
  def bstack1ll1ll1l11_opy_():
    nonlocal hashed_id, bstack1l11l1l111_opy_
    try:
      if bstack11l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧາ") in CONFIG and str(CONFIG[bstack11l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨຳ")]).lower() != bstack11l11_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫິ"):
        hashed_id, bstack1l11l1l111_opy_ = bstack11l1l11l1_opy_()
      else:
        hashed_id, bstack1l11l1l111_opy_ = get_build_link()
    except Exception as e:
      logger.debug(bstack11l11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࠥࡲࡩ࡯࡭࠽ࠤࢀࢃࠢີ").format(e))
  bstack11lll111l_opy_ = threading.Thread(target=bstack1111l11l1_opy_)
  bstack11lll1lll1_opy_ = threading.Thread(target=bstack11l11l1ll_opy_)
  bstack11l1lll1l1_opy_ = threading.Thread(target=bstack1ll1ll1l11_opy_)
  threads = [bstack11lll111l_opy_, bstack11lll1lll1_opy_, bstack11l1lll1l1_opy_]
  for thread in threads:
    try:
      thread.start()
    except Exception as e:
      logger.debug(bstack11l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡳࡵࡣࡵࡸ࡮ࡴࡧࠡࡶ࡫ࡶࡪࡧࡤࠡࡽࢀ࠾ࠥࢁࡽࠣຶ").format(thread.name, e))
  for thread in threads:
    try:
      thread.join()
    except Exception as e:
      logger.debug(bstack11l11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠ࡫ࡱ࡬ࡲ࡮ࡴࡧࠡࡶ࡫ࡶࡪࡧࡤࠡࡽࢀ࠾ࠥࢁࡽࠣື").format(thread.name, e))
  bstack1l1lll1ll1_opy_(hashed_id)
  logger.info(bstack11l11_opy_ (u"ࠩࡖࡈࡐࠦࡲࡶࡰࠣࡩࡳࡪࡥࡥࠢࡩࡳࡷࠦࡩࡥ࠼ຸࠪ") + bstack11l1l1111_opy_.get_property(bstack11l11_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨູࠬ"), bstack11l11_opy_ (u"຺ࠫࠬ")) + bstack11l11_opy_ (u"ࠬ࠲ࠠࡵࡧࡶࡸ࡭ࡻࡢࠡ࡫ࡧ࠾ࠥ࠭ົ") + os.getenv(bstack11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫຼ"), bstack11l11_opy_ (u"ࠧࠨຽ")))
  if hashed_id is not None and bstack1l1lll11l1_opy_() != -1:
    sessions = bstack1lll111ll1_opy_(hashed_id)
    bstack1llll111l_opy_(sessions, bstack1l11l1l111_opy_)
  if bstack1llll11l1l_opy_ == bstack11l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ຾") and bstack11ll1ll1l1_opy_ != 0:
    sys.exit(bstack11ll1ll1l1_opy_)
  if bstack1llll11l1l_opy_ == bstack11l11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ຿") and bstack111ll1111_opy_ != 0:
    sys.exit(bstack111ll1111_opy_)
def bstack1l1lll1ll1_opy_(new_id):
    global bstack1l1111l11_opy_
    bstack1l1111l11_opy_ = new_id
def bstack1l1l1l1ll1_opy_(bstack1111lllll1_opy_):
  if bstack1111lllll1_opy_:
    return bstack1111lllll1_opy_.capitalize()
  else:
    return bstack11l11_opy_ (u"ࠪࠫເ")
@measure(event_name=EVENTS.bstack1lllllll11_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l111l11l_opy_=bstack11l1111lll_opy_)
def bstack1ll1lll111_opy_(bstack11l1llll11_opy_):
  if bstack11l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩແ") in bstack11l1llll11_opy_ and bstack11l1llll11_opy_[bstack11l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪໂ")] != bstack11l11_opy_ (u"࠭ࠧໃ"):
    return bstack11l1llll11_opy_[bstack11l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬໄ")]
  else:
    bstack11l111l11l_opy_ = bstack11l11_opy_ (u"ࠣࠤ໅")
    if bstack11l11_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩໆ") in bstack11l1llll11_opy_ and bstack11l1llll11_opy_[bstack11l11_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪ໇")] != None:
      bstack11l111l11l_opy_ += bstack11l1llll11_opy_[bstack11l11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨ່ࠫ")] + bstack11l11_opy_ (u"ࠧ࠲້ࠠࠣ")
      if bstack11l1llll11_opy_[bstack11l11_opy_ (u"࠭࡯ࡴ໊ࠩ")] == bstack11l11_opy_ (u"ࠢࡪࡱࡶ໋ࠦ"):
        bstack11l111l11l_opy_ += bstack11l11_opy_ (u"ࠣ࡫ࡒࡗࠥࠨ໌")
      bstack11l111l11l_opy_ += (bstack11l1llll11_opy_[bstack11l11_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ໍ")] or bstack11l11_opy_ (u"ࠪࠫ໎"))
      return bstack11l111l11l_opy_
    else:
      bstack11l111l11l_opy_ += bstack1l1l1l1ll1_opy_(bstack11l1llll11_opy_[bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬ໏")]) + bstack11l11_opy_ (u"ࠧࠦࠢ໐") + (
              bstack11l1llll11_opy_[bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ໑")] or bstack11l11_opy_ (u"ࠧࠨ໒")) + bstack11l11_opy_ (u"ࠣ࠮ࠣࠦ໓")
      if bstack11l1llll11_opy_[bstack11l11_opy_ (u"ࠩࡲࡷࠬ໔")] == bstack11l11_opy_ (u"࡛ࠥ࡮ࡴࡤࡰࡹࡶࠦ໕"):
        bstack11l111l11l_opy_ += bstack11l11_opy_ (u"ࠦ࡜࡯࡮ࠡࠤ໖")
      bstack11l111l11l_opy_ += bstack11l1llll11_opy_[bstack11l11_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ໗")] or bstack11l11_opy_ (u"࠭ࠧ໘")
      return bstack11l111l11l_opy_
@measure(event_name=EVENTS.bstack111lll1111_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l111l11l_opy_=bstack11l1111lll_opy_)
def bstack11ll1l1ll_opy_(bstack11ll1ll1ll_opy_):
  if bstack11ll1ll1ll_opy_ == bstack11l11_opy_ (u"ࠢࡥࡱࡱࡩࠧ໙"):
    return bstack11l11_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽࡫ࡷ࡫ࡥ࡯࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥ࡫ࡷ࡫ࡥ࡯ࠤࡁࡇࡴࡳࡰ࡭ࡧࡷࡩࡩࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫ໚")
  elif bstack11ll1ll1ll_opy_ == bstack11l11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ໛"):
    return bstack11l11_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡸࡥࡥ࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡶࡪࡪࠢ࠿ࡈࡤ࡭ࡱ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ໜ")
  elif bstack11ll1ll1ll_opy_ == bstack11l11_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦໝ"):
    return bstack11l11_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡨࡴࡨࡩࡳࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡨࡴࡨࡩࡳࠨ࠾ࡑࡣࡶࡷࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬໞ")
  elif bstack11ll1ll1ll_opy_ == bstack11l11_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧໟ"):
    return bstack11l11_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡵࡩࡩࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡳࡧࡧࠦࡃࡋࡲࡳࡱࡵࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩ໠")
  elif bstack11ll1ll1ll_opy_ == bstack11l11_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤ໡"):
    return bstack11l11_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࠨ࡫ࡥࡢ࠵࠵࠺ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࠣࡦࡧࡤ࠷࠷࠼ࠢ࠿ࡖ࡬ࡱࡪࡵࡵࡵ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ໢")
  elif bstack11ll1ll1ll_opy_ == bstack11l11_opy_ (u"ࠥࡶࡺࡴ࡮ࡪࡰࡪࠦ໣"):
    return bstack11l11_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡢ࡭ࡣࡦ࡯ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡢ࡭ࡣࡦ࡯ࠧࡄࡒࡶࡰࡱ࡭ࡳ࡭࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ໤")
  else:
    return bstack11l11_opy_ (u"ࠬࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡤ࡯ࡥࡨࡱ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡤ࡯ࡥࡨࡱࠢ࠿ࠩ໥") + bstack1l1l1l1ll1_opy_(
      bstack11ll1ll1ll_opy_) + bstack11l11_opy_ (u"࠭࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ໦")
def bstack1lllll1l1_opy_(session):
  return bstack11l11_opy_ (u"ࠧ࠽ࡶࡵࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡷࡵࡷࠣࡀ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠲ࡴࡡ࡮ࡧࠥࡂࡁࡧࠠࡩࡴࡨࡪࡂࠨࡻࡾࠤࠣࡸࡦࡸࡧࡦࡶࡀࠦࡤࡨ࡬ࡢࡰ࡮ࠦࡃࢁࡽ࠽࠱ࡤࡂࡁ࠵ࡴࡥࡀࡾࢁࢀࢃ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾࠲ࡸࡷࡄࠧ໧").format(
    session[bstack11l11_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣࡠࡷࡵࡰࠬ໨")], bstack1ll1lll111_opy_(session), bstack11ll1l1ll_opy_(session[bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡵࡷࡥࡹࡻࡳࠨ໩")]),
    bstack11ll1l1ll_opy_(session[bstack11l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ໪")]),
    bstack1l1l1l1ll1_opy_(session[bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬ໫")] or session[bstack11l11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬ໬")] or bstack11l11_opy_ (u"࠭ࠧ໭")) + bstack11l11_opy_ (u"ࠢࠡࠤ໮") + (session[bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪ໯")] or bstack11l11_opy_ (u"ࠩࠪ໰")),
    session[bstack11l11_opy_ (u"ࠪࡳࡸ࠭໱")] + bstack11l11_opy_ (u"ࠦࠥࠨ໲") + session[bstack11l11_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ໳")], session[bstack11l11_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨ໴")] or bstack11l11_opy_ (u"ࠧࠨ໵"),
    session[bstack11l11_opy_ (u"ࠨࡥࡵࡩࡦࡺࡥࡥࡡࡤࡸࠬ໶")] if session[bstack11l11_opy_ (u"ࠩࡦࡶࡪࡧࡴࡦࡦࡢࡥࡹ࠭໷")] else bstack11l11_opy_ (u"ࠪࠫ໸"))
@measure(event_name=EVENTS.bstack1l1llll11l_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l111l11l_opy_=bstack11l1111lll_opy_)
def bstack1llll111l_opy_(sessions, bstack1l11l1l111_opy_):
  try:
    bstack11ll1ll1l_opy_ = bstack11l11_opy_ (u"ࠦࠧ໹")
    if not os.path.exists(bstack1lll1ll1ll_opy_):
      os.mkdir(bstack1lll1ll1ll_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11l11_opy_ (u"ࠬࡧࡳࡴࡧࡷࡷ࠴ࡸࡥࡱࡱࡵࡸ࠳࡮ࡴ࡮࡮ࠪ໺")), bstack11l11_opy_ (u"࠭ࡲࠨ໻")) as f:
      bstack11ll1ll1l_opy_ = f.read()
    bstack11ll1ll1l_opy_ = bstack11ll1ll1l_opy_.replace(bstack11l11_opy_ (u"ࠧࡼࠧࡕࡉࡘ࡛ࡌࡕࡕࡢࡇࡔ࡛ࡎࡕࠧࢀࠫ໼"), str(len(sessions)))
    bstack11ll1ll1l_opy_ = bstack11ll1ll1l_opy_.replace(bstack11l11_opy_ (u"ࠨࡽࠨࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠫࡽࠨ໽"), bstack1l11l1l111_opy_)
    bstack11ll1ll1l_opy_ = bstack11ll1ll1l_opy_.replace(bstack11l11_opy_ (u"ࠩࡾࠩࡇ࡛ࡉࡍࡆࡢࡒࡆࡓࡅࠦࡿࠪ໾"),
                                              sessions[0].get(bstack11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡱࡥࡲ࡫ࠧ໿")) if sessions[0] else bstack11l11_opy_ (u"ࠫࠬༀ"))
    with open(os.path.join(bstack1lll1ll1ll_opy_, bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡷ࡫ࡰࡰࡴࡷ࠲࡭ࡺ࡭࡭ࠩ༁")), bstack11l11_opy_ (u"࠭ࡷࠨ༂")) as stream:
      stream.write(bstack11ll1ll1l_opy_.split(bstack11l11_opy_ (u"ࠧࡼࠧࡖࡉࡘ࡙ࡉࡐࡐࡖࡣࡉࡇࡔࡂࠧࢀࠫ༃"))[0])
      for session in sessions:
        stream.write(bstack1lllll1l1_opy_(session))
      stream.write(bstack11ll1ll1l_opy_.split(bstack11l11_opy_ (u"ࠨࡽࠨࡗࡊ࡙ࡓࡊࡑࡑࡗࡤࡊࡁࡕࡃࠨࢁࠬ༄"))[1])
    logger.info(bstack11l11_opy_ (u"ࠩࡊࡩࡳ࡫ࡲࡢࡶࡨࡨࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡧࡻࡩ࡭ࡦࠣࡥࡷࡺࡩࡧࡣࡦࡸࡸࠦࡡࡵࠢࡾࢁࠬ༅").format(bstack1lll1ll1ll_opy_));
  except Exception as e:
    logger.debug(bstack11ll1l1l_opy_.format(str(e)))
def bstack1lll111ll1_opy_(hashed_id):
  global CONFIG
  try:
    bstack1lllll111_opy_ = datetime.datetime.now()
    host = bstack11l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠮ࡥ࡯ࡳࡺࡪ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ༆") if bstack11l11_opy_ (u"ࠫࡦࡶࡰࠨ༇") in CONFIG else bstack11l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡱ࡫࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭༈")
    user = CONFIG[bstack11l11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ༉")]
    key = CONFIG[bstack11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ༊")]
    bstack1l1ll11ll_opy_ = bstack11l11_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ་") if bstack11l11_opy_ (u"ࠩࡤࡴࡵ࠭༌") in CONFIG else (bstack11l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧ།") if CONFIG.get(bstack11l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨ༎")) else bstack11l11_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ༏"))
    host = bstack1l11l1llll_opy_(cli.config, [bstack11l11_opy_ (u"ࠨࡡࡱ࡫ࡶࠦ༐"), bstack11l11_opy_ (u"ࠢࡢࡲࡳࡅࡺࡺ࡯࡮ࡣࡷࡩࠧ༑"), bstack11l11_opy_ (u"ࠣࡣࡳ࡭ࠧ༒")], host) if bstack11l11_opy_ (u"ࠩࡤࡴࡵ࠭༓") in CONFIG else bstack1l11l1llll_opy_(cli.config, [bstack11l11_opy_ (u"ࠥࡥࡵ࡯ࡳࠣ༔"), bstack11l11_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸࡪࠨ༕"), bstack11l11_opy_ (u"ࠧࡧࡰࡪࠤ༖")], host)
    url = bstack11l11_opy_ (u"࠭ࡻࡾ࠱ࡾࢁ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽ࠰ࡵࡨࡷࡸ࡯࡯࡯ࡵ࠱࡮ࡸࡵ࡮ࠨ༗").format(host, bstack1l1ll11ll_opy_, hashed_id)
    headers = {
      bstack11l11_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ༘࠭"): bstack11l11_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱ༙ࠫ"),
    }
    proxies = bstack1llll1l111_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies, auth=(user, key))
    if response.json():
      cli.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺ࡨࡧࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࡥ࡬ࡪࡵࡷࠦ༚"), datetime.datetime.now() - bstack1lllll111_opy_)
      return list(map(lambda session: session[bstack11l11_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ༛")], response.json()))
  except Exception as e:
    logger.debug(bstack1l1ll1ll1l_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack111l1ll11_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l111l11l_opy_=bstack11l1111lll_opy_)
def get_build_link():
  global CONFIG
  global bstack1l1111l11_opy_
  try:
    if bstack11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ༜") in CONFIG:
      bstack1lllll111_opy_ = datetime.datetime.now()
      host = bstack11l11_opy_ (u"ࠬࡧࡰࡪ࠯ࡦࡰࡴࡻࡤࠨ༝") if bstack11l11_opy_ (u"࠭ࡡࡱࡲࠪ༞") in CONFIG else bstack11l11_opy_ (u"ࠧࡢࡲ࡬ࠫ༟")
      user = CONFIG[bstack11l11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ༠")]
      key = CONFIG[bstack11l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ༡")]
      bstack1l1ll11ll_opy_ = bstack11l11_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩ༢") if bstack11l11_opy_ (u"ࠫࡦࡶࡰࠨ༣") in CONFIG else bstack11l11_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ༤")
      url = bstack11l11_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡼࡿ࠽ࡿࢂࡆࡻࡾ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠯࡬ࡶࡳࡳ࠭༥").format(user, key, host, bstack1l1ll11ll_opy_)
      if cli.is_enabled(CONFIG):
        bstack1l11l1l111_opy_, hashed_id = cli.bstack11l11ll1l_opy_()
        logger.info(bstack111l11l1l1_opy_.format(bstack1l11l1l111_opy_))
        return [hashed_id, bstack1l11l1l111_opy_]
      else:
        headers = {
          bstack11l11_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭༦"): bstack11l11_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ༧"),
        }
        if bstack11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ༨") in CONFIG:
          params = {bstack11l11_opy_ (u"ࠪࡲࡦࡳࡥࠨ༩"): CONFIG[bstack11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ༪")], bstack11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ༫"): CONFIG[bstack11l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ༬")]}
        else:
          params = {bstack11l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ༭"): CONFIG[bstack11l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ༮")]}
        proxies = bstack1llll1l111_opy_(CONFIG, url)
        response = requests.get(url, params=params, headers=headers, proxies=proxies)
        if response.json():
          bstack111l1l111l_opy_ = response.json()[0][bstack11l11_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡢࡶ࡫࡯ࡨࠬ༯")]
          if bstack111l1l111l_opy_:
            bstack1l11l1l111_opy_ = bstack111l1l111l_opy_[bstack11l11_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥࡢࡹࡷࡲࠧ༰")].split(bstack11l11_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦ࠱ࡧࡻࡩ࡭ࡦࠪ༱"))[0] + bstack11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡷ࠴࠭༲") + bstack111l1l111l_opy_[
              bstack11l11_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ༳")]
            logger.info(bstack111l11l1l1_opy_.format(bstack1l11l1l111_opy_))
            bstack1l1111l11_opy_ = bstack111l1l111l_opy_[bstack11l11_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ༴")]
            bstack11lll1l1_opy_ = CONFIG[bstack11l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨ༵ࠫ")]
            if bstack11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ༶") in CONFIG:
              bstack11lll1l1_opy_ += bstack11l11_opy_ (u"ࠪࠤ༷ࠬ") + CONFIG[bstack11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭༸")]
            if bstack11lll1l1_opy_ != bstack111l1l111l_opy_[bstack11l11_opy_ (u"ࠬࡴࡡ࡮ࡧ༹ࠪ")]:
              logger.debug(bstack11l11ll1_opy_.format(bstack111l1l111l_opy_[bstack11l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ༺")], bstack11lll1l1_opy_))
            cli.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠢࡩࡶࡷࡴ࠿࡭ࡥࡵࡡࡥࡹ࡮ࡲࡤࡠ࡮࡬ࡲࡰࠨ༻"), datetime.datetime.now() - bstack1lllll111_opy_)
            return [bstack111l1l111l_opy_[bstack11l11_opy_ (u"ࠨࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ༼")], bstack1l11l1l111_opy_]
    else:
      logger.warning(bstack1ll1l11l11_opy_)
  except Exception as e:
    logger.debug(bstack1lll11lll_opy_.format(str(e)))
  return [None, None]
def bstack1ll111ll1_opy_(url, bstack1llllll11_opy_=False):
  global CONFIG
  global bstack1llll1ll1l_opy_
  if not bstack1llll1ll1l_opy_:
    hostname = bstack11ll1lll11_opy_(url)
    is_private = bstack1ll11lll_opy_(hostname)
    if (bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭༽") in CONFIG and not bstack1ll1l11lll_opy_(CONFIG[bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ༾")])) and (is_private or bstack1llllll11_opy_):
      bstack1llll1ll1l_opy_ = hostname
def bstack11ll1lll11_opy_(url):
  return urlparse(url).hostname
def bstack1ll11lll_opy_(hostname):
  for bstack11ll11111l_opy_ in bstack1l11ll1lll_opy_:
    regex = re.compile(bstack11ll11111l_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack11l1l111ll_opy_(bstack1l111ll1l_opy_):
  return True if bstack1l111ll1l_opy_ in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack111ll1l11_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l111l11l_opy_=bstack11l1111lll_opy_)
def getAccessibilityResults(driver):
  global CONFIG
  global bstack111llll1ll_opy_
  bstack111llll111_opy_ = not (bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ༿"), None) and bstack11ll11l11_opy_(
          threading.current_thread(), bstack11l11_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫཀ"), None))
  bstack1l11l11l11_opy_ = getattr(driver, bstack11l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭ཁ"), None) != True
  bstack1l1l11ll11_opy_ = bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧག"), None) and bstack11ll11l11_opy_(
          threading.current_thread(), bstack11l11_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪགྷ"), None)
  if bstack1l1l11ll11_opy_:
    if not bstack11ll1l1l1l_opy_():
      logger.warning(bstack11l11_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡴࡵࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡂࡲࡳࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷ࠳ࠨང"))
      return {}
    logger.debug(bstack11l11_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡲࡦࡵࡸࡰࡹࡹࠧཅ"))
    logger.debug(perform_scan(driver, driver_command=bstack11l11_opy_ (u"ࠫࡪࡾࡥࡤࡷࡷࡩࡘࡩࡲࡪࡲࡷࠫཆ")))
    results = bstack11ll1ll111_opy_(bstack11l11_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸࡸࠨཇ"))
    if results is not None and results.get(bstack11l11_opy_ (u"ࠨࡩࡴࡵࡸࡩࡸࠨ཈")) is not None:
        return results[bstack11l11_opy_ (u"ࠢࡪࡵࡶࡹࡪࡹࠢཉ")]
    logger.error(bstack11l11_opy_ (u"ࠣࡐࡲࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡗ࡫ࡳࡶ࡮ࡷࡷࠥࡽࡥࡳࡧࠣࡪࡴࡻ࡮ࡥ࠰ࠥཊ"))
    return []
  if not bstack1lllll111l_opy_.bstack1llll1lll1_opy_(CONFIG, bstack111llll1ll_opy_) or (bstack1l11l11l11_opy_ and bstack111llll111_opy_):
    logger.warning(bstack11l11_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶ࠲ࠧཋ"))
    return {}
  try:
    logger.debug(bstack11l11_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡲࡦࡵࡸࡰࡹࡹࠧཌ"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack1l1lll111l_opy_.bstack1l11llll_opy_)
    return results
  except Exception:
    logger.error(bstack11l11_opy_ (u"ࠦࡓࡵࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡹࡨࡶࡪࠦࡦࡰࡷࡱࡨ࠳ࠨཌྷ"))
    return {}
@measure(event_name=EVENTS.bstack1llll1ll11_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l111l11l_opy_=bstack11l1111lll_opy_)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack111llll1ll_opy_
  bstack111llll111_opy_ = not (bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩཎ"), None) and bstack11ll11l11_opy_(
          threading.current_thread(), bstack11l11_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬཏ"), None))
  bstack1l11l11l11_opy_ = getattr(driver, bstack11l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧཐ"), None) != True
  bstack1l1l11ll11_opy_ = bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨད"), None) and bstack11ll11l11_opy_(
          threading.current_thread(), bstack11l11_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫདྷ"), None)
  if bstack1l1l11ll11_opy_:
    if not bstack11ll1l1l1l_opy_():
      logger.warning(bstack11l11_opy_ (u"ࠥࡒࡴࡺࠠࡢࡰࠣࡅࡵࡶࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࠡࡃࡳࡴࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡳࡶ࡯ࡰࡥࡷࡿ࠮ࠣན"))
      return {}
    logger.debug(bstack11l11_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡢࡦࡨࡲࡶࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡳࡧࡶࡹࡱࡺࡳࠡࡵࡸࡱࡲࡧࡲࡺࠩཔ"))
    logger.debug(perform_scan(driver, driver_command=bstack11l11_opy_ (u"ࠬ࡫ࡸࡦࡥࡸࡸࡪ࡙ࡣࡳ࡫ࡳࡸࠬཕ")))
    results = bstack11ll1ll111_opy_(bstack11l11_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹ࡙ࡵ࡮࡯ࡤࡶࡾࠨབ"))
    if results is not None and results.get(bstack11l11_opy_ (u"ࠢࡴࡷࡰࡱࡦࡸࡹࠣབྷ")) is not None:
        return results[bstack11l11_opy_ (u"ࠣࡵࡸࡱࡲࡧࡲࡺࠤམ")]
    logger.error(bstack11l11_opy_ (u"ࠤࡑࡳࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡘࡥࡴࡷ࡯ࡸࡸࠦࡓࡶ࡯ࡰࡥࡷࡿࠠࡸࡣࡶࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦཙ"))
    return {}
  if not bstack1lllll111l_opy_.bstack1llll1lll1_opy_(CONFIG, bstack111llll1ll_opy_) or (bstack1l11l11l11_opy_ and bstack111llll111_opy_):
    logger.warning(bstack11l11_opy_ (u"ࠥࡒࡴࡺࠠࡢࡰࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡹࡵ࡮࡯ࡤࡶࡾ࠴ࠢཚ"))
    return {}
  try:
    logger.debug(bstack11l11_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡢࡦࡨࡲࡶࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡳࡧࡶࡹࡱࡺࡳࠡࡵࡸࡱࡲࡧࡲࡺࠩཛ"))
    logger.debug(perform_scan(driver))
    bstack1l11lll1ll_opy_ = driver.execute_async_script(bstack1l1lll111l_opy_.bstack11l11l11ll_opy_)
    return bstack1l11lll1ll_opy_
  except Exception:
    logger.error(bstack11l11_opy_ (u"ࠧࡔ࡯ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡸࡱࡲࡧࡲࡺࠢࡺࡥࡸࠦࡦࡰࡷࡱࡨ࠳ࠨཛྷ"))
    return {}
def bstack11ll1l1l1l_opy_():
  global CONFIG
  global bstack111llll1ll_opy_
  bstack111l1l1ll1_opy_ = bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ཝ"), None) and bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩཞ"), None)
  if not bstack1lllll111l_opy_.bstack1llll1lll1_opy_(CONFIG, bstack111llll1ll_opy_) or not bstack111l1l1ll1_opy_:
        logger.warning(bstack11l11_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡳࡴࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡲࡦࡵࡸࡰࡹࡹ࠮ࠣཟ"))
        return False
  return True
def bstack11ll1ll111_opy_(result_type):
    bstack1ll1l1111l_opy_ = bstack1ll111l1_opy_.current_test_uuid() if bstack1ll111l1_opy_.current_test_uuid() else bstack11l1ll111l_opy_.current_hook_uuid()
    with ThreadPoolExecutor() as executor:
        future = executor.submit(bstack1lll1l1ll1_opy_(bstack1ll1l1111l_opy_, result_type))
        try:
            return future.result(timeout=bstack1l1l1l11l1_opy_)
        except TimeoutError:
            logger.error(bstack11l11_opy_ (u"ࠤࡗ࡭ࡲ࡫࡯ࡶࡶࠣࡥ࡫ࡺࡥࡳࠢࡾࢁࡸࠦࡷࡩ࡫࡯ࡩࠥ࡬ࡥࡵࡥ࡫࡭ࡳ࡭ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡓࡧࡶࡹࡱࡺࡳࠣའ").format(bstack1l1l1l11l1_opy_))
        except Exception as ex:
            logger.debug(bstack11l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡵࡩࡹࡸࡩࡦࡸ࡬ࡲ࡬ࠦࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡼࡿ࠱ࠤࡊࡸࡲࡰࡴࠣ࠱ࠥࢁࡽࠣཡ").format(result_type, str(ex)))
    return {}
@measure(event_name=EVENTS.bstack11ll1l1lll_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l111l11l_opy_=bstack11l1111lll_opy_)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack111llll1ll_opy_
  bstack111llll111_opy_ = not (bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨར"), None) and bstack11ll11l11_opy_(
          threading.current_thread(), bstack11l11_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫལ"), None))
  bstack1ll1l1l1l1_opy_ = not (bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ཤ"), None) and bstack11ll11l11_opy_(
          threading.current_thread(), bstack11l11_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩཥ"), None))
  bstack1l11l11l11_opy_ = getattr(driver, bstack11l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨས"), None) != True
  if not bstack1lllll111l_opy_.bstack1llll1lll1_opy_(CONFIG, bstack111llll1ll_opy_) or (bstack1l11l11l11_opy_ and bstack111llll111_opy_ and bstack1ll1l1l1l1_opy_):
    logger.warning(bstack11l11_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡸࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡣࡢࡰ࠱ࠦཧ"))
    return {}
  try:
    bstack1ll11lll11_opy_ = bstack11l11_opy_ (u"ࠪࡥࡵࡶࠧཨ") in CONFIG and CONFIG.get(bstack11l11_opy_ (u"ࠫࡦࡶࡰࠨཀྵ"), bstack11l11_opy_ (u"ࠬ࠭ཪ"))
    session_id = getattr(driver, bstack11l11_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠪཫ"), None)
    if not session_id:
      logger.warning(bstack11l11_opy_ (u"ࠢࡏࡱࠣࡷࡪࡹࡳࡪࡱࡱࠤࡎࡊࠠࡧࡱࡸࡲࡩࠦࡦࡰࡴࠣࡨࡷ࡯ࡶࡦࡴࠥཬ"))
      return {bstack11l11_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢ཭"): bstack11l11_opy_ (u"ࠤࡑࡳࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡉࡅࠢࡩࡳࡺࡴࡤࠣ཮")}
    if bstack1ll11lll11_opy_:
      try:
        bstack11l11l11_opy_ = {
              bstack11l11_opy_ (u"ࠪࡸ࡭ࡐࡷࡵࡖࡲ࡯ࡪࡴࠧ཯"): os.environ.get(bstack11l11_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ཰"), os.environ.get(bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕཱࠩ"), bstack11l11_opy_ (u"ི࠭ࠧ"))),
              bstack11l11_opy_ (u"ࠧࡵࡪࡗࡩࡸࡺࡒࡶࡰࡘࡹ࡮ࡪཱིࠧ"): bstack1ll111l1_opy_.current_test_uuid() if bstack1ll111l1_opy_.current_test_uuid() else bstack11l1ll111l_opy_.current_hook_uuid(),
              bstack11l11_opy_ (u"ࠨࡣࡸࡸ࡭ࡎࡥࡢࡦࡨࡶུࠬ"): os.environ.get(bstack11l11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜ཱུ࡚ࠧ")),
              bstack11l11_opy_ (u"ࠪࡷࡨࡧ࡮ࡕ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪྲྀ"): str(int(datetime.datetime.now().timestamp() * 1000)),
              bstack11l11_opy_ (u"ࠫࡹ࡮ࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩཷ"): os.environ.get(bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪླྀ"), bstack11l11_opy_ (u"࠭ࠧཹ")),
              bstack11l11_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪེࠧ"): kwargs.get(bstack11l11_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࡠࡥࡲࡱࡲࡧ࡮ࡥཻࠩ"), None) or bstack11l11_opy_ (u"ོࠩࠪ")
          }
        if not hasattr(thread_local, bstack11l11_opy_ (u"ࠪࡦࡦࡹࡥࡠࡣࡳࡴࡤࡧ࠱࠲ࡻࡢࡷࡨࡸࡩࡱࡶཽࠪ")):
            scripts = {bstack11l11_opy_ (u"ࠫࡸࡩࡡ࡯ࠩཾ"): bstack1l1lll111l_opy_.perform_scan}
            thread_local.base_app_a11y_script = scripts
        bstack1l1llll11_opy_ = copy.deepcopy(thread_local.base_app_a11y_script)
        bstack1l1llll11_opy_[bstack11l11_opy_ (u"ࠬࡹࡣࡢࡰࠪཿ")] = bstack1l1llll11_opy_[bstack11l11_opy_ (u"࠭ࡳࡤࡣࡱྀࠫ")] % json.dumps(bstack11l11l11_opy_)
        bstack1l1lll111l_opy_.bstack1l111l111_opy_(bstack1l1llll11_opy_)
        bstack1l1lll111l_opy_.store()
        bstack11l1lll1ll_opy_ = driver.execute_script(bstack1l1lll111l_opy_.perform_scan)
      except Exception as bstack1ll11lllll_opy_:
        logger.info(bstack11l11_opy_ (u"ࠢࡂࡲࡳ࡭ࡺࡳࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡥࡤࡲࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ཱྀࠦࠢ") + str(bstack1ll11lllll_opy_))
        bstack11l1lll1ll_opy_ = {bstack11l11_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢྂ"): str(bstack1ll11lllll_opy_)}
    else:
      bstack11l1lll1ll_opy_ = driver.execute_async_script(bstack1l1lll111l_opy_.perform_scan, {bstack11l11_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࠩྃ"): kwargs.get(bstack11l11_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࡢࡧࡴࡳ࡭ࡢࡰࡧ྄ࠫ"), None) or bstack11l11_opy_ (u"ࠫࠬ྅")})
    return bstack11l1lll1ll_opy_
  except Exception as err:
    logger.error(bstack11l11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡴࡸࡲࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡣࡢࡰ࠱ࠤࢀࢃࠢ྆").format(str(err)))
    return {}