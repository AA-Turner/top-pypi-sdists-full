# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
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
from browserstack_sdk.sdk_cli.bstack1l1111l11l_opy_ import bstack1l11l111l_opy_
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from browserstack_sdk.bstack1l1llll111_opy_ import bstack1111l111l_opy_
from browserstack_sdk.bstack111l1lll1_opy_ import *
import time
import requests
from bstack_utils.constants import EVENTS, STAGE, bstack1ll11ll1l_opy_
from bstack_utils.messages import bstack1l1lllllll_opy_, bstack1lll111ll1_opy_, bstack111llll1l_opy_, bstack1l1l111lll_opy_, bstack1l1l11ll11_opy_, bstack1111l111_opy_
from bstack_utils.measure import measure
from bstack_utils.logger_utils import get_logger
from bstack_utils.helper import bstack11lllll1l_opy_
from browserstack_sdk.bstack1111l11111_opy_ import bstack1111l11l1l_opy_
logger = get_logger(__name__)
def bstack11lllll1_opy_():
  global CONFIG
  headers = {
        bstack1ll11_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack1ll11_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack11lllll1l_opy_(CONFIG, bstack1ll11ll1l_opy_)
  try:
    response = requests.get(bstack1ll11ll1l_opy_, headers=headers, proxies=proxies, timeout=2)
    if response.json():
      bstack1l1lllll1l_opy_ = response.json()[bstack1ll11_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1l1lllllll_opy_.format(response.json()))
      return bstack1l1lllll1l_opy_
    else:
      logger.debug(bstack1lll111ll1_opy_.format(bstack1ll11_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack1lll111ll1_opy_.format(e))
def bstack1l1l111ll1_opy_(hub_url):
  global CONFIG
  url = bstack1ll11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack1ll11_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack1ll11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack1ll11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack11lllll1l_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=(0.5, 1.0))
    latency = time.perf_counter() - start_time
    logger.debug(bstack111llll1l_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1l1l111lll_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack1l11ll11l_opy_, stage=STAGE.bstack11111llll_opy_)
def bstack1l1lllll11_opy_():
  try:
    global bstack11llll1l1l_opy_
    global CONFIG
    if bstack1ll11_opy_ (u"ࠫ࡭ࡻࡢࡓࡧࡪ࡭ࡴࡴࠧࡾ") in CONFIG and CONFIG[bstack1ll11_opy_ (u"ࠬ࡮ࡵࡣࡔࡨ࡫࡮ࡵ࡮ࠨࡿ")]:
      from bstack_utils.constants import bstack11l1l111l_opy_
      bstack1ll1ll1l1_opy_ = CONFIG[bstack1ll11_opy_ (u"࠭ࡨࡶࡤࡕࡩ࡬࡯࡯࡯ࠩࢀ")]
      if bstack1ll1ll1l1_opy_ in bstack11l1l111l_opy_:
        bstack11llll1l1l_opy_ = bstack11l1l111l_opy_[bstack1ll1ll1l1_opy_]
        logger.debug(bstack1l1l11ll11_opy_.format(bstack11llll1l1l_opy_))
        return
      else:
        logger.debug(bstack1ll11_opy_ (u"ࠢࡉࡷࡥࠤࡰ࡫ࡹࠡࠩࡾࢁࠬࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࡎࡕࡃࡡࡘࡖࡑࡥࡍࡂࡒ࠯ࠤ࡫ࡧ࡬࡭࡫ࡱ࡫ࠥࡨࡡࡤ࡭ࠣࡸࡴࠦ࡯ࡱࡶ࡬ࡱࡦࡲࠠࡩࡷࡥࠤࡩ࡫ࡴࡦࡥࡷ࡭ࡴࡴࠢࢁ").format(bstack1ll1ll1l1_opy_))
    bstack1l1lllll1l_opy_ = bstack11lllll1_opy_()
    from concurrent.futures import ThreadPoolExecutor, as_completed
    if bstack1l1lllll1l_opy_:
        with ThreadPoolExecutor(max_workers=len(bstack1l1lllll1l_opy_)) as executor:
            bstack1ll11111l1_opy_ = {executor.submit(bstack1l1l111ll1_opy_, bstack111ll11l_opy_): bstack111ll11l_opy_ for bstack111ll11l_opy_ in bstack1l1lllll1l_opy_}
            for future in as_completed(bstack1ll11111l1_opy_):
                result = future.result()
                if result and result.get(bstack1ll11_opy_ (u"ࠨ࡮ࡤࡸࡪࡴࡣࡺࠩࢂ")) is not None:
                    bstack11llll1l1l_opy_ = result[bstack1ll11_opy_ (u"ࠩ࡫ࡹࡧࡥࡵࡳ࡮ࠪࢃ")]
                    logger.debug(bstack1l1l11ll11_opy_.format(bstack11llll1l1l_opy_))
                    return
        bstack11llll1l1l_opy_ = bstack1l1lllll1l_opy_[0]
        logger.debug(bstack1l1l11ll11_opy_.format(bstack11llll1l1l_opy_))
        return
  except Exception as e:
    logger.debug(bstack1111l111_opy_.format(e))
from browserstack_sdk.bstack11llll11ll_opy_ import *
from browserstack_sdk.bstack1lll11l1ll_opy_ import bstack111ll1l11_opy_
from browserstack_sdk.bstack1111l11111_opy_ import *
from browserstack_sdk.bstack1l1l111l1_opy_ import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.logger_utils import get_logger
from bstack_utils.measure import measure
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack1lllll1ll1_opy_, stage=STAGE.bstack11111llll_opy_)
def bstack11l1l1l111_opy_():
    global bstack11llll1l1l_opy_
    try:
        bstack1l11l11l_opy_ = bstack1l111111_opy_()
        bstack11ll11ll1l_opy_(bstack1l11l11l_opy_)
        hub_url = bstack1l11l11l_opy_.get(bstack1ll11_opy_ (u"ࠥࡹࡷࡲࠢࢄ"), bstack1ll11_opy_ (u"ࠦࠧࢅ"))
        if hub_url.endswith(bstack1ll11_opy_ (u"ࠬ࠵ࡷࡥ࠱࡫ࡹࡧ࠭ࢆ")):
            hub_url = hub_url.rsplit(bstack1ll11_opy_ (u"࠭࠯ࡸࡦ࠲࡬ࡺࡨࠧࢇ"), 1)[0]
        if hub_url.startswith(bstack1ll11_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࠨ࢈")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack1ll11_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࠪࢉ")):
            hub_url = hub_url[8:]
        bstack11llll1l1l_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack1l111111_opy_():
    global CONFIG
    bstack1111ll1l11_opy_ = CONFIG.get(bstack1ll11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢊ"), {}).get(bstack1ll11_opy_ (u"ࠪ࡫ࡷ࡯ࡤࡏࡣࡰࡩࠬࢋ"), bstack1ll11_opy_ (u"ࠫࡓࡕ࡟ࡈࡔࡌࡈࡤࡔࡁࡎࡇࡢࡔࡆ࡙ࡓࡆࡆࠪࢌ"))
    if not isinstance(bstack1111ll1l11_opy_, str):
        raise ValueError(bstack1ll11_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡌࡸࡩࡥࠢࡱࡥࡲ࡫ࠠ࡮ࡷࡶࡸࠥࡨࡥࠡࡣࠣࡺࡦࡲࡩࡥࠢࡶࡸࡷ࡯࡮ࡨࠤࢍ"))
    try:
        bstack1l11l11l_opy_ = bstack1l11lll1l1_opy_(bstack1111ll1l11_opy_)
        return bstack1l11l11l_opy_
    except Exception as e:
        logger.error(bstack1ll11_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡩࡵ࡭ࡩࠦࡤࡦࡶࡤ࡭ࡱࡹࠠ࠻ࠢࡾࢁࠧࢎ").format(str(e)))
        return {}
def bstack1l11lll1l1_opy_(bstack1111ll1l11_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack1ll11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ࢏")] or not CONFIG[bstack1ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ࢐")]:
            raise ValueError(bstack1ll11_opy_ (u"ࠤࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠤࡴࡸࠠࡢࡥࡦࡩࡸࡹࠠ࡬ࡧࡼࠦ࢑"))
        url = bstack11l111ll1l_opy_ + bstack1111ll1l11_opy_
        auth = (CONFIG[bstack1ll11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ࢒")], CONFIG[bstack1ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ࢓")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack1l111ll1_opy_ = json.loads(response.text)
            return bstack1l111ll1_opy_
    except ValueError as ve:
        logger.error(bstack1ll11_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡩࡵ࡭ࡩࠦࡤࡦࡶࡤ࡭ࡱࡹࠠ࠻ࠢࡾࢁࠧ࢔").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack1ll11_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡪࡶ࡮ࡪࠠࡥࡧࡷࡥ࡮ࡲࡳࠡ࠼ࠣࡿࢂࠨ࢕").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack11ll11ll1l_opy_(bstack1l1l11ll1l_opy_):
    global CONFIG
    if bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ࢖") not in CONFIG or str(CONFIG[bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬࢗ")]).lower() == bstack1ll11_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ࢘"):
        CONFIG[bstack1ll11_opy_ (u"ࠪࡰࡴࡩࡡ࡭࢙ࠩ")] = False
    elif bstack1ll11_opy_ (u"ࠫ࡮ࡹࡔࡳ࡫ࡤࡰࡌࡸࡩࡥ࢚ࠩ") in bstack1l1l11ll1l_opy_:
        bstack1l1l1l111l_opy_ = CONFIG.get(bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴ࢛ࠩ"), {})
        logger.debug(bstack1ll11_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡸࡪࡵࡷ࡭ࡳ࡭ࠠ࡭ࡱࡦࡥࡱࠦ࡯ࡱࡶ࡬ࡳࡳࡹ࠺ࠡࠧࡶࠦ࢜"), bstack1l1l1l111l_opy_)
        bstack11l1l111_opy_ = bstack1l1l11ll1l_opy_.get(bstack1ll11_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡒࡦࡲࡨࡥࡹ࡫ࡲࡴࠤ࢝"), [])
        bstack11ll111l1_opy_ = bstack1ll11_opy_ (u"ࠣ࠮ࠥ࢞").join(bstack11l1l111_opy_)
        logger.debug(bstack1ll11_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡅࡸࡷࡹࡵ࡭ࠡࡴࡨࡴࡪࡧࡴࡦࡴࠣࡷࡹࡸࡩ࡯ࡩ࠽ࠤࠪࡹࠢ࢟"), bstack11ll111l1_opy_)
        bstack1111ll11l_opy_ = {
            bstack1ll11_opy_ (u"ࠥࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧࢠ"): bstack1ll11_opy_ (u"ࠦࡦࡺࡳ࠮ࡴࡨࡴࡪࡧࡴࡦࡴࠥࢡ"),
            bstack1ll11_opy_ (u"ࠧ࡬࡯ࡳࡥࡨࡐࡴࡩࡡ࡭ࠤࢢ"): bstack1ll11_opy_ (u"ࠨࡴࡳࡷࡨࠦࢣ"),
            bstack1ll11_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࠭ࡳࡧࡳࡩࡦࡺࡥࡳࠤࢤ"): bstack11ll111l1_opy_
        }
        bstack1l1l1l111l_opy_.update(bstack1111ll11l_opy_)
        logger.debug(bstack1ll11_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡖࡲࡧࡥࡹ࡫ࡤࠡ࡮ࡲࡧࡦࡲࠠࡰࡲࡷ࡭ࡴࡴࡳ࠻ࠢࠨࡷࠧࢥ"), bstack1l1l1l111l_opy_)
        CONFIG[bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢦ")] = bstack1l1l1l111l_opy_
        logger.debug(bstack1ll11_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡉ࡭ࡳࡧ࡬ࠡࡅࡒࡒࡋࡏࡇ࠻ࠢࠨࡷࠧࢧ"), CONFIG)
def get_turboscale_playwright_url():
    bstack1l11l11l_opy_ = bstack1l111111_opy_()
    if not bstack1l11l11l_opy_[bstack1ll11_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡖࡴ࡯ࠫࢨ")]:
      raise ValueError(bstack1ll11_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡗࡵࡰࠥ࡯ࡳࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡩࡶࡴࡳࠠࡨࡴ࡬ࡨࠥࡪࡥࡵࡣ࡬ࡰࡸ࠴ࠢࢩ"))
    return bstack1l11l11l_opy_[bstack1ll11_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡘࡶࡱ࠭ࢪ")] + bstack1ll11_opy_ (u"ࠧࡀࡥࡤࡴࡸࡃࠧࢫ")
@measure(event_name=EVENTS.bstack11l11lll_opy_, stage=STAGE.bstack11111llll_opy_)
def bstack11l1ll1l1_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack1ll11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪࢬ")], CONFIG[bstack1ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬࢭ")])
        url = bstack11l1ll11ll_opy_
        logger.debug(bstack1ll11_opy_ (u"ࠥࡅࡹࡺࡥ࡮ࡲࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴࠢࡩࡶࡴࡳࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡔࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠣࡅࡕࡏࠢࢮ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack1ll11_opy_ (u"ࠦࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠥࢯ"): bstack1ll11_opy_ (u"ࠧࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠣࢰ")})
            if response.status_code == 200:
                bstack111l11l11_opy_ = json.loads(response.text)
                bstack11llllll11_opy_ = bstack111l11l11_opy_.get(bstack1ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡸ࠭ࢱ"), [])
                if bstack11llllll11_opy_:
                    bstack11ll111l11_opy_ = bstack11llllll11_opy_[0]
                    build_hashed_id = bstack11ll111l11_opy_.get(bstack1ll11_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪࢲ"))
                    bstack1l1111111l_opy_ = bstack1llll11l1_opy_ + build_hashed_id
                    result.extend([build_hashed_id, bstack1l1111111l_opy_])
                    logger.info(bstack11111lll11_opy_.format(bstack1l1111111l_opy_))
                    bstack1l1ll111l1_opy_ = CONFIG[bstack1ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫࢳ")]
                    if bstack1ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࢴ") in CONFIG:
                      bstack1l1ll111l1_opy_ += bstack1ll11_opy_ (u"ࠪࠤࠬࢵ") + CONFIG[bstack1ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࢶ")]
                    if bstack1l1ll111l1_opy_ != bstack11ll111l11_opy_.get(bstack1ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪࢷ")):
                      logger.debug(bstack1l1ll1llll_opy_.format(bstack11ll111l11_opy_.get(bstack1ll11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫࢸ")), bstack1l1ll111l1_opy_))
                    return result
                else:
                    logger.debug(bstack1ll11_opy_ (u"ࠢࡂࡖࡖࠤ࠿ࠦࡎࡰࠢࡥࡹ࡮ࡲࡤࡴࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠱ࠦࢹ"))
            else:
                logger.debug(bstack1ll11_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴ࠰ࠥࢺ"))
        except Exception as e:
            logger.error(bstack1ll11_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࡶࠤ࠿ࠦࡻࡾࠤࢻ").format(str(e)))
    else:
        logger.debug(bstack1ll11_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡆࡓࡓࡌࡉࡈࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡶࡩࡹ࠴ࠠࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴ࠰ࠥࢼ"))
    return [None, None]
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1lll111l_opy_ import bstack1lll111l_opy_, Events, bstack1l111ll11_opy_, bstack11lll11ll_opy_
from bstack_utils.measure import bstack1ll1lll11l_opy_
from bstack_utils.measure import measure
from bstack_utils.percy import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack111l11l111_opy_ import bstack1l11111l_opy_
from bstack_utils.messages import *
from bstack_utils import logger_utils
from bstack_utils.constants import *
from bstack_utils.helper import bstack11111l11ll_opy_, bstack1ll11l111l_opy_, bstack1l11llll11_opy_, bstack1l1111l111_opy_, \
  bstack1ll11l1l11_opy_, \
  Notset, is_robot_playwright_installed, bstack11l11l1l1l_opy_, \
  bstack11lll1llll_opy_, bstack11ll11llll_opy_, bstack1ll1l111l1_opy_, bstack11ll11l1l1_opy_, bstack1111l1111l_opy_, bstack1l1111111_opy_, \
  bstack111111111l_opy_, \
  bstack1lllllllll1_opy_, bstack1l11ll1ll_opy_, bstack11llll11_opy_, bstack111111l11_opy_, \
  bstack1ll111ll1_opy_, bstack1l1ll11l_opy_, bstack1lll1111ll_opy_, bstack1111l11l_opy_, bstack1111llll1_opy_
from bstack_utils.bstack1ll1ll11ll_opy_ import bstack1llll1ll1l_opy_
from bstack_utils.bstack1ll1llllll_opy_ import bstack11l1lllll1_opy_, bstack1l1lll11ll_opy_
from bstack_utils.bstack1lllll111l_opy_ import bstack1l1111l11_opy_
from bstack_utils.session_utils import bstack11l11l111l_opy_, bstack1ll1l11lll_opy_
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.bstack1lll11l111_opy_ import bstack11l1l1ll1_opy_
from bstack_utils.proxy import bstack111l1l1l_opy_, bstack11lllll1l_opy_, bstack11l11lll1_opy_, bstack1111lllll_opy_
from bstack_utils.bstack1l1111ll_opy_ import bstack1l1l11l1ll_opy_, bstack1l1lll11_opy_
import bstack_utils.bstack111l11ll1_opy_ as TestHubUtils
import bstack_utils.bstack111lll111l_opy_ as bstack1l1l1111l_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.utils.bstack1l1lll1ll_opy_ import bstack1lll1l1ll_opy_
from bstack_utils.bstack1l1l1llll1_opy_ import bstack1l1ll11ll1_opy_
from bstack_utils.bstack11l1111111_opy_ import bstack1ll1l1ll1l_opy_
from bstack_utils.bstack1ll1lll11l_opy_ import bstack11ll11l1ll_opy_
if os.getenv(bstack1ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡉࡑࡒࡏࡘ࠭ࢽ")):
  cli.bstack1lll1l1ll1_opy_()
else:
  os.environ[bstack1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡊࡒࡓࡐ࡙ࠧࢾ")] = bstack1ll11_opy_ (u"࠭ࡴࡳࡷࡨࠫࢿ")
bstack111l11ll_opy_ = bstack1ll11_opy_ (u"ࠧࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠠࠡ࡫ࡩࠬࡵࡧࡧࡦࠢࡀࡁࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠠࡼ࡞ࡱࠤࠥࠦࡴࡳࡻࡾࡠࡳࠦࡣࡰࡰࡶࡸࠥ࡬ࡳࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࡡ࠭ࡦࡴ࡞ࠪ࠭ࡀࡢ࡮ࠡࠢࠣࠤࠥ࡬ࡳ࠯ࡣࡳࡴࡪࡴࡤࡇ࡫࡯ࡩࡘࡿ࡮ࡤࠪࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠬࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡳࡣ࡮ࡴࡤࡦࡺࠬࠤ࠰ࠦࠢ࠻ࠤࠣ࠯ࠥࡐࡓࡐࡐ࠱ࡷࡹࡸࡩ࡯ࡩ࡬ࡪࡾ࠮ࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࠬࡦࡽࡡࡪࡶࠣࡲࡪࡽࡐࡢࡩࡨ࠶࠳࡫ࡶࡢ࡮ࡸࡥࡹ࡫ࠨࠣࠪࠬࠤࡂࡄࠠࡼࡿࠥ࠰ࠥࡢࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡨࡧࡷࡗࡪࡹࡳࡪࡱࡱࡈࡪࡺࡡࡪ࡮ࡶࠦࢂࡢࠧࠪࠫࠬ࡟ࠧ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠣ࡟ࠬࠤ࠰ࠦࠢ࠭࡞࡟ࡲࠧ࠯࡜࡯ࠢࠣࠤࠥࢃࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡽ࡝ࡰࠣࠤ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠧࣀ")
LAUNCH_PATCH_ROBOT_PLAYWRIGHT = bstack1ll11_opy_ (u"ࠨ࡞ࡱ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࡢ࡮ࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠻࡝ࠡ࠿ࡀࡁࠥࡢࠧࡵࡴࡸࡩࡡ࠭࡜࡯ࡥࡲࡲࡸࡺࠠࡣࡵࡷࡥࡨࡱ࡟ࡱࡣࡷ࡬ࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴࡟࡟ࡲࡨࡵ࡮ࡴࡶࠣࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࡝ࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠵ࡢࡢ࡮ࡤࡱࡱࡷࡹࠦࡰࡠ࡫ࡱࡨࡪࡾࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠵ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠵࡟ࠣࡁࡂࡃࠠ࡝ࠩࡷࡶࡺ࡫࡜ࠨ࡞ࡱࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡷࡱ࡯ࡣࡦࠪ࠳࠰ࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠵ࠪ࡞ࡱࡧࡴࡴࡳࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣࠫ࠾ࡠࡳࡩ࡯࡯ࡵࡷࠤࡴࡸࡩࡨ࡫ࡱࡥࡱࡥࡣࡩࡴࡲࡱ࡮ࡻ࡭ࡠ࡮ࡤࡹࡳࡩࡨࠡ࠿ࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡰࡦࡻ࡮ࡤࡪ࠱ࡦ࡮ࡴࡤࠩ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭ࠪ࠽࡟ࡲ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡱࡧࡵ࡯ࡥ࡫ࠤࡂࠦࡡࡴࡻࡱࡧࠥ࠮࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸ࠯ࠠ࠾ࡀࠣࡿࡡࡴࡩࡧࠢࠫࠥࡧࡹࡴࡢࡥ࡮ࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠪࠢࡾࡠࡳࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦ࡯ࡳ࡫ࡪ࡭ࡳࡧ࡬ࡠࡥ࡫ࡶࡴࡳࡩࡶ࡯ࡢࡰࡦࡻ࡮ࡤࡪࠫࡰࡦࡻ࡮ࡤࡪࡒࡴࡹ࡯࡯࡯ࡵࠬ࠿ࡡࡴࡽ࡝ࡰ࡯ࡩࡹࠦࡣࡢࡲࡶ࠿ࡡࡴࡴࡳࡻࠣࡿࡡࡴࡣࡢࡲࡶࠤࡂࠦࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠪ࡞ࡱࠤࠥࢃࠠࡤࡣࡷࡧ࡭࠮ࡥࡹࠫࠣࡿࡡࡴࠠࠡࠢࠣࢁࡡࡴࠠࠡ࡫ࡩࠤ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࠮ࠦࡻ࡝ࡰࠣࠤࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡩ࡯࡯ࡰࡨࡧࡹࡕࡶࡦࡴࡆࡈࡕ࠮ࡻ࡝ࡰࠣࠤࠥࠦࠠࠡࡧࡱࡨࡵࡵࡩ࡯ࡶࡘࡖࡑࡀࠠࡡࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠧࡿࡪࡴࡣࡰࡦࡨ࡙ࡗࡏࡃࡰ࡯ࡳࡳࡳ࡫࡮ࡵࠪࡍࡗࡔࡔ࠮ࡴࡶࡵ࡭ࡳ࡭ࡩࡧࡻࠫࡧࡦࡶࡳࠪࠫࢀࡤ࠱ࡢ࡮ࠡࠢࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴ࡞ࡱࠤࠥࠦࠠࡾࠫ࡟ࡲࠥࠦࡽ࡝ࡰࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࠻ࠢࡣࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠩࢁࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭ࢂࡦࠬ࡝ࡰࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴ࡞ࡱࠤࠥࢃࠩ࡝ࡰࢀࡠࡳࡩ࡯࡯ࡵࡷࠤࡴࡸࡩࡨ࡫ࡱࡥࡱࡥࡣࡰࡰࡱࡩࡨࡺࠠ࠾ࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱ࠮ࡤࡪࡵࡳࡲ࡯ࡵ࡮࠰ࡦࡳࡳࡴࡥࡤࡶ࠱ࡦ࡮ࡴࡤࠩ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭ࠪ࠽࡟ࡲ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡨࡵ࡮࡯ࡧࡦࡸࠥࡃࠠࡢࡵࡼࡲࡨࠦࠨࡤࡱࡱࡲࡪࡩࡴࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁ࡜࡯ࠢࠣ࡭࡫ࠦࠨࠢࡤࡶࡸࡦࡩ࡫ࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠮ࠦࡻ࡝ࡰࠣࠤࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥࡵࡲࡪࡩ࡬ࡲࡦࡲ࡟ࡤࡱࡱࡲࡪࡩࡴࠩࡥࡲࡲࡳ࡫ࡣࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠫ࠾ࡠࡳࠦࠠࡾ࡞ࡱࠤࠥࡲࡥࡵࠢࡦࡥࡵࡹ࠻࡝ࡰࠣࠤࡹࡸࡹࠡࡽ࡟ࡲࠥࠦࠠࠡࡥࡤࡴࡸࠦ࠽ࠡࡌࡖࡓࡓ࠴ࡰࡢࡴࡶࡩ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡩࡡࡱࡵࠬࡠࡳࠦࠠࡾࠢࡦࡥࡹࡩࡨࠩࡧࡻ࠭ࠥࢁ࡜࡯ࠢࠣࢁࡡࡴࠠࠡࡥࡲࡲࡸࡺࠠ࡮ࡱࡧ࡭࡫࡯ࡥࡥࡇࡱࡨࡵࡵࡩ࡯ࡶࠣࡁࠥࡦࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࡡࠢ࠮ࠤࡪࡴࡣࡰࡦࡨ࡙ࡗࡏࡃࡰ࡯ࡳࡳࡳ࡫࡮ࡵࠪࡍࡗࡔࡔ࠮ࡴࡶࡵ࡭ࡳ࡭ࡩࡧࡻࠫࡧࡦࡶࡳࠪࠫ࠾ࡠࡳࠦࠠࡪࡨࠣࠬࡧࡹࡴࡢࡥ࡮ࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ࠭ࠥࢁ࡜࡯ࠢࠣࠤࠥࡸࡥࡵࡷࡵࡲࠥࡧࡷࡢ࡫ࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡨࡵ࡮࡯ࡧࡦࡸࡔࡼࡥࡳࡅࡇࡔ࠭ࢁ࡜࡯ࠢࠣࠤࠥࠦࠠࡦࡰࡧࡴࡴ࡯࡮ࡵࡗࡕࡐ࠿ࠦ࡭ࡰࡦ࡬ࡪ࡮࡫ࡤࡆࡰࡧࡴࡴ࡯࡮ࡵ࠮࡟ࡲࠥࠦࠠࠡࠢࠣ࠲࠳࠴ࡣࡰࡰࡱࡩࡨࡺࡏࡱࡶ࡬ࡳࡳࡹ࡜࡯ࠢࠣࠤࠥࢃࠩ࡝ࡰࠣࠤࢂࡢ࡮ࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤ࠳࠴࠮ࡤࡱࡱࡲࡪࡩࡴࡐࡲࡷ࡭ࡴࡴࡳ࠭࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࡝ࡰࠣࠤࢂ࠯࡜࡯ࡿ࡟ࡲࡱ࡫ࡴࠡࡄࡵࡳࡼࡹࡥࡳࡅࡲࡲࡹ࡫ࡸࡵ࠽࡟ࡲࡹࡸࡹࠡࡽ࡟ࡲࠥࠦࡣࡰࡰࡶࡸࠥࡶࡡࡵࡪࡐࡳࡩࡻ࡬ࡦࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭ࠨࡰࡢࡶ࡫ࠦ࠮ࡁ࡜࡯ࠢࠣࡧࡴࡴࡳࡵࠢࡳࡻࡈࡵࡲࡦࡒࡤࡸ࡭ࠦ࠽ࠡࡲࡤࡸ࡭ࡓ࡯ࡥࡷ࡯ࡩ࠳ࡪࡩࡳࡰࡤࡱࡪ࠮ࡲࡦࡳࡸ࡭ࡷ࡫࠮ࡳࡧࡶࡳࡱࡼࡥࠩࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠳ࡣࡰࡴࡨ࠳ࡵࡧࡣ࡬ࡣࡪࡩ࠳ࡰࡳࡰࡰࠥ࠭࠮ࡁ࡜࡯ࠢࠣࡆࡷࡵࡷࡴࡧࡵࡇࡴࡴࡴࡦࡺࡷࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨࡱࡣࡷ࡬ࡒࡵࡤࡶ࡮ࡨ࠲࡯ࡵࡩ࡯ࠪࡳࡻࡈࡵࡲࡦࡒࡤࡸ࡭࠲ࠠࠣ࡮࡬ࡦ࠴ࡩ࡬ࡪࡧࡱࡸ࠴ࡨࡲࡰࡹࡶࡩࡷࡉ࡯࡯ࡶࡨࡼࡹࠨࠩࠪ࠰ࡅࡶࡴࡽࡳࡦࡴࡆࡳࡳࡺࡥࡹࡶ࠾ࡠࡳࢃࠠࡤࡣࡷࡧ࡭ࠦࠨࡦࠫࠣࡿࡡࡴࠠࠡࡥࡲࡲࡸࡵ࡬ࡦ࠰ࡺࡥࡷࡴࠨࠣࡅࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡱࡵࡡࡥࠢࡅࡶࡴࡽࡳࡦࡴࡆࡳࡳࡺࡥࡹࡶࠣࡪࡷࡵ࡭ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠲ࡩ࡯ࡳࡧ࠽ࠦ࠱ࠦࡥ࠯࡯ࡨࡷࡸࡧࡧࡦࠫ࠾ࡠࡳࢃ࡜࡯ࡥࡲࡲࡸࡺࠠࡰࡴ࡬࡫࡮ࡴࡡ࡭ࡡࡱࡩࡼࡖࡡࡨࡧࠣࡁࠥࡈࡲࡰࡹࡶࡩࡷࡉ࡯࡯ࡶࡨࡼࡹ࠴ࡰࡳࡱࡷࡳࡹࡿࡰࡦ࠰ࡱࡩࡼࡖࡡࡨࡧ࠾ࡠࡳࡈࡲࡰࡹࡶࡩࡷࡉ࡯࡯ࡶࡨࡼࡹ࠴ࡰࡳࡱࡷࡳࡹࡿࡰࡦ࠰ࡱࡩࡼࡖࡡࡨࡧࠣࡁࠥࡧࡳࡺࡰࡦࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠮ࠩࠡࡽ࡟ࡲࠥࠦࡩࡧࠢࠫࡦࡸࡺࡡࡤ࡭ࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠬࠤࢀࡢ࡮ࠡࠢࠣࠤࡹࡸࡹࠡࡽ࡟ࡲࠥࠦࠠࠡࠢࠣࡧࡴࡴࡳࡵࠢࡥࡶࡴࡽࡳࡦࡴࠣࡁࠥࡺࡨࡪࡵ࠱ࡦࡷࡵࡷࡴࡧࡵࠤࠫࠬࠠࡵࡪ࡬ࡷ࠳ࡨࡲࡰࡹࡶࡩࡷ࠮ࠩ࠼࡞ࡱࠤࠥࠦࠠࠡࠢ࡯ࡩࡹࠦࡰࡳ࡫ࡰࡥࡷࡿࡃࡰࡰࡷࡩࡽࡺࠠ࠾ࠢࡥࡶࡴࡽࡳࡦࡴࠣࠪࠫࠦࡴࡺࡲࡨࡳ࡫ࠦࡢࡳࡱࡺࡷࡪࡸ࠮ࡤࡱࡱࡸࡪࡾࡴࡴࠢࡀࡁࡂࠦ࡜ࠨࡨࡸࡲࡨࡺࡩࡰࡰ࡟ࠫࠥࡅࠠࡣࡴࡲࡻࡸ࡫ࡲ࠯ࡥࡲࡲࡹ࡫ࡸࡵࡵࠫ࠭ࡠ࠶࡝ࠡ࠼ࠣࡲࡺࡲ࡬࠼࡞ࡱࠤࠥࠦࠠࠡࠢ࡬ࡪࠥ࠮ࠡࡱࡴ࡬ࡱࡦࡸࡹࡄࡱࡱࡸࡪࡾࡴࠡࠨࠩࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࠬࠦࠡࡶࡼࡴࡪࡵࡦࠡࡤࡵࡳࡼࡹࡥࡳ࠰ࡱࡩࡼࡉ࡯࡯ࡶࡨࡼࡹࠦ࠽࠾࠿ࠣࡠࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡜ࠨࠫࠣࡿࡡࡴࠠࠡࠢࠣࠤࠥࠦࠠࡱࡴ࡬ࡱࡦࡸࡹࡄࡱࡱࡸࡪࡾࡴࠡ࠿ࠣࡥࡼࡧࡩࡵࠢࡥࡶࡴࡽࡳࡦࡴ࠱ࡲࡪࡽࡃࡰࡰࡷࡩࡽࡺࠨࠪ࠽࡟ࡲࠥࠦࠠࠡࠢࠣࢁࡡࡴࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡵࡷࠤࡹࡧࡲࡨࡧࡷࡇࡴࡴࡴࡦࡺࡷࠤࡂࠦࡰࡳ࡫ࡰࡥࡷࡿࡃࡰࡰࡷࡩࡽࡺࠠࡽࡾࠣࡸ࡭࡯ࡳ࠼࡞ࡱࠤࠥࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡲࡪࡽࡐࡢࡩࡨ࠲ࡨࡧ࡬࡭ࠪࡷࡥࡷ࡭ࡥࡵࡅࡲࡲࡹ࡫ࡸࡵࠫ࠾ࡠࡳࠦࠠࠡࠢࢀࠤࡨࡧࡴࡤࡪࠣࠬࡪ࠯ࠠࡼ࡞ࡱࠤࠥࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡲࡪࡽࡐࡢࡩࡨ࠲ࡨࡧ࡬࡭ࠪࡷ࡬࡮ࡹࠩ࠼࡞ࡱࠤࠥࠦࠠࡾ࡞ࡱࠤࠥࢃࠠ࡝ࡰࠣࠤࡪࡲࡳࡦࠢࡾࡠࡳࠦࠠࠡࠢࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣࡳࡷ࡯ࡧࡪࡰࡤࡰࡤࡴࡥࡸࡒࡤ࡫ࡪ࠴ࡣࡢ࡮࡯ࠬࡹ࡮ࡩࡴࠫ࠾ࡠࡳࠦࠠࡾ࡞ࡱࢁࡀࡢ࡮࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱࡟ࡲࠬࣁ")
from ._version import __version__
bstack1ll11ll11_opy_ = None
CONFIG = {}
bstack111l11111_opy_ = {}
bstack11llll1l_opy_ = {}
bstack1ll1l11l_opy_ = None
bstack1l1llll1l_opy_ = None
SESSION_NAME = None
PLATFORM_INDEX = -1
bstack11l1lll1l_opy_ = 0
bstack1111ll1l_opy_ = bstack11l11llll1_opy_
bstack11l1llll11_opy_ = 1
PARALLELISE_VANILLA_PYTHON = False
PARALLELISE_THREADING_PYTHON = False
FRAMEWORK_NAME = bstack1ll11_opy_ (u"ࠩࠪࣂ")
bstack111lll11_opy_ = bstack1ll11_opy_ (u"ࠪࠫࣃ")
bstack1l11lll111_opy_ = False
BROWSERSTACK_AUTOMATION = True
bstack11l1l1ll11_opy_ = False
bstack1l11l1l11_opy_ = bstack1ll11_opy_ (u"ࠫࠬࣄ")
bstack11l1ll1l11_opy_ = []
bstack1llll1l1l_opy_ = threading.Lock()
bstack1l1ll1lll1_opy_ = threading.Lock()
bstack11lll11lll_opy_ = None
bstack11llll1l1l_opy_ = bstack1ll11_opy_ (u"ࠬ࠭ࣅ")
SELENIUM_OR_PLAYWRIGHT_INSTALLED = False
bstack1l1l1l1l_opy_ = None
bstack1lll11ll11_opy_ = None
bstack11ll11l1l_opy_ = None
bstack111l1111l1_opy_ = -1
bstack11l11ll1l1_opy_ = os.path.join(os.path.expanduser(bstack1ll11_opy_ (u"࠭ࡾࠨࣆ")), bstack1ll11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧࣇ"), bstack1ll11_opy_ (u"ࠨ࠰ࡵࡳࡧࡵࡴ࠮ࡴࡨࡴࡴࡸࡴ࠮ࡪࡨࡰࡵ࡫ࡲ࠯࡬ࡶࡳࡳ࠭ࣈ"))
bstack11l1ll1111_opy_ = 0
bstack1ll1l11l1l_opy_ = 0
bstack1l1ll111ll_opy_ = []
bstack1l111l111l_opy_ = []
ROBOT_PYTHON_ERRORS = []
bstack1llllllllll_opy_ = []
bstack11l1ll11l1_opy_ = bstack1ll11_opy_ (u"ࠩࠪࣉ")
bstack11111l1ll1_opy_ = bstack1ll11_opy_ (u"ࠪࠫ࣊")
bstack11l1l1lll_opy_ = False
bstack11ll111ll_opy_ = False
bstack1l11l1llll_opy_ = {}
bstack1lll1l11ll_opy_ = {}
bstack1llllllll1_opy_ = None
bstack1ll1111l1_opy_ = None
bstack11111ll1l_opy_ = None
bstack1ll1l1l1l1_opy_ = None
bstack1l111l11l1_opy_ = None
bstack11ll1lll_opy_ = None
bstack11l1l1ll1l_opy_ = None
bstack1lll111ll_opy_ = None
bstack1l1l1l1l11_opy_ = None
bstack1lll1l1l1l_opy_ = None
bstack1lll11ll1l_opy_ = None
bstack1111l1l11_opy_ = None
bstack1l111111l1_opy_ = None
bstack111111l1l1_opy_ = None
bstack111l1l1ll_opy_ = None
bstack111l1ll1l1_opy_ = None
bstack11ll11lll1_opy_ = None
bstack1l1l1lll1_opy_ = None
bstack1l1l11ll1_opy_ = None
bstack11l1lll1ll_opy_ = None
bstack1ll1111ll1_opy_ = None
bstack111llll11_opy_ = None
bstack1lll111lll_opy_ = None
thread_local = threading.local()
bstack1l1l111l11_opy_ = False
bstack111ll111_opy_ = bstack1ll11_opy_ (u"ࠦࠧ࣋")
_11111ll11_opy_ = None
logger = logger_utils.get_logger(__name__, bstack1111ll1l_opy_)
automation_logger = logger_utils.get_automation_logger(__name__)
global_config = Config.get_instance()
percy = bstack1l1l1ll1l1_opy_()
bstack1l11lll11l_opy_ = bstack1l11111l_opy_()
bstack11ll1l1lll_opy_ = bstack1l1l111l1_opy_()
def bstack111l111l11_opy_():
  global CONFIG
  global bstack11l1l1lll_opy_
  global global_config
  testContextOptions = bstack1lll1llll1_opy_(CONFIG)
  if bstack1ll11l1l11_opy_(CONFIG):
    if (bstack1ll11_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ࣌") in testContextOptions and str(testContextOptions[bstack1ll11_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ࣍")]).lower() == bstack1ll11_opy_ (u"ࠧࡵࡴࡸࡩࠬ࣎")):
      bstack11l1l1lll_opy_ = True
      global_config.bstack1lll111l1_opy_(True)
    if (bstack1ll11_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷ࣏ࠬ") in testContextOptions and str(testContextOptions[bstack1ll11_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࣐࠭")]).lower() == bstack1ll11_opy_ (u"ࠪࡸࡷࡻࡥࠨ࣑")):
      global_config.bstack1llll111l_opy_(True)
  else:
    bstack11l1l1lll_opy_ = True
    global_config.bstack1lll111l1_opy_(True)
    global_config.bstack1llll111l_opy_(True)
def bstack1111ll11l1_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1lll11llll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1ll111l1l_opy_():
  global bstack1lll1l11ll_opy_
  args = sys.argv
  for i in range(len(args)):
    if bstack1ll11_opy_ (u"ࠦ࠲࠳ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡨࡵ࡮ࡧ࡫ࡪࡪ࡮ࡲࡥ࣒ࠣ") == args[i].lower() or bstack1ll11_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰࡰࡩ࡭࡬ࠨ࣓") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      bstack1lll1l11ll_opy_[bstack1ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࡤࡌࡉࡍࡇࠪࣔ")] = path
      return path
  return None
bstack111lllll11_opy_ = re.compile(bstack1ll11_opy_ (u"ࡲࠣ࠰࠭ࡃࡡࠪࡻࠩ࠰࠭ࡃ࠮ࢃ࠮ࠫࡁࠥࣕ"))
def bstack1lll1ll1l_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack111lllll11_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack1ll11_opy_ (u"ࠣࠦࡾࠦࣖ") + group + bstack1ll11_opy_ (u"ࠤࢀࠦࣗ"), os.environ.get(group))
  return value
def bstack11l111l111_opy_():
  global bstack1lll111lll_opy_
  if bstack1lll111lll_opy_ is None:
        bstack1lll111lll_opy_ = bstack1ll111l1l_opy_()
  bstack11l1l1l1l_opy_ = bstack1lll111lll_opy_
  if bstack11l1l1l1l_opy_ and os.path.exists(os.path.abspath(bstack11l1l1l1l_opy_)):
    fileName = bstack11l1l1l1l_opy_
  if bstack1ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋࠧࣘ") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack1ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨࣙ")])) and not bstack1ll11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡑࡥࡲ࡫ࠧࣚ") in locals():
    fileName = os.environ[bstack1ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࡤࡌࡉࡍࡇࠪࣛ")]
  if bstack1ll11_opy_ (u"ࠧࡧ࡫࡯ࡩࡓࡧ࡭ࡦࠩࣜ") in locals():
    bstack1l11ll_opy_ = os.path.abspath(fileName)
  else:
    bstack1l11ll_opy_ = bstack1ll11_opy_ (u"ࠨࠩࣝ")
  bstack11l11l11_opy_ = os.getcwd()
  bstack1lllll111_opy_ = bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬࣞ")
  bstack11ll111lll_opy_ = bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡥࡲࡲࠧࣟ")
  while (not os.path.exists(bstack1l11ll_opy_)) and bstack11l11l11_opy_ != bstack1ll11_opy_ (u"ࠦࠧ࣠"):
    bstack1l11ll_opy_ = os.path.join(bstack11l11l11_opy_, bstack1lllll111_opy_)
    if not os.path.exists(bstack1l11ll_opy_):
      bstack1l11ll_opy_ = os.path.join(bstack11l11l11_opy_, bstack11ll111lll_opy_)
    if bstack11l11l11_opy_ != os.path.dirname(bstack11l11l11_opy_):
      bstack11l11l11_opy_ = os.path.dirname(bstack11l11l11_opy_)
    else:
      bstack11l11l11_opy_ = bstack1ll11_opy_ (u"ࠧࠨ࣡")
  bstack1lll111lll_opy_ = bstack1l11ll_opy_ if os.path.exists(bstack1l11ll_opy_) else None
  return bstack1lll111lll_opy_
def bstack11l1111l1l_opy_(config):
    if bstack1ll11_opy_ (u"࠭ࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬࠭࣢") in config:
      config[bstack1ll11_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࣣࠫ")] = config[bstack1ll11_opy_ (u"ࠨࡶࡨࡷࡹࡘࡥࡱࡱࡵࡸ࡮ࡴࡧࠨࣤ")]
    if bstack1ll11_opy_ (u"ࠩࡷࡩࡸࡺࡒࡦࡲࡲࡶࡹ࡯࡮ࡨࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣥ") in config:
      config[bstack1ll11_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࣦࠧ")] = config[bstack1ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࡓࡵࡺࡩࡰࡰࡶࠫࣧ")]
def bstack1l1l111111_opy_():
  bstack1l11ll_opy_ = bstack11l111l111_opy_()
  if not os.path.exists(bstack1l11ll_opy_):
    bstack11l1l111l1_opy_(
      bstack11l1lllll_opy_.format(os.getcwd()))
  try:
    with open(bstack1l11ll_opy_, bstack1ll11_opy_ (u"ࠬࡸࠧࣨ")) as stream:
      yaml.add_implicit_resolver(bstack1ll11_opy_ (u"ࠨࠡࡱࡣࡷ࡬ࡪࡾࣩࠢ"), bstack111lllll11_opy_)
      yaml.add_constructor(bstack1ll11_opy_ (u"ࠢࠢࡲࡤࡸ࡭࡫ࡸࠣ࣪"), bstack1lll1ll1l_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      bstack11l1111l1l_opy_(config)
      return config
  except:
    with open(bstack1l11ll_opy_, bstack1ll11_opy_ (u"ࠨࡴࠪ࣫")) as stream:
      try:
        config = yaml.safe_load(stream)
        bstack11l1111l1l_opy_(config)
        return config
      except yaml.YAMLError as exc:
        bstack11l1l111l1_opy_(bstack11111ll1_opy_.format(str(exc)))
def bstack1l1ll1ll1l_opy_(config):
  bstack1ll1l11l1_opy_ = bstack11ll1ll1ll_opy_(config)
  for option in list(bstack1ll1l11l1_opy_):
    if option.lower() in bstack1lllll1111_opy_ and option != bstack1lllll1111_opy_[option.lower()]:
      bstack1ll1l11l1_opy_[bstack1lllll1111_opy_[option.lower()]] = bstack1ll1l11l1_opy_[option]
      del bstack1ll1l11l1_opy_[option]
  return config
def bstack111lll11ll_opy_():
  global bstack11llll1l_opy_
  for key, bstack1l111ll11l_opy_ in bstack11ll1ll1l_opy_.items():
    if isinstance(bstack1l111ll11l_opy_, list):
      for var in bstack1l111ll11l_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack11llll1l_opy_[key] = os.environ[var]
          break
    elif bstack1l111ll11l_opy_ in os.environ and os.environ[bstack1l111ll11l_opy_] and str(os.environ[bstack1l111ll11l_opy_]).strip():
      bstack11llll1l_opy_[key] = os.environ[bstack1l111ll11l_opy_]
  if bstack1ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ࣬") in os.environ:
    bstack11llll1l_opy_[bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹ࣭ࠧ")] = {}
    bstack11llll1l_opy_[bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ࣮")][bstack1ll11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣯ࠧ")] = os.environ[bstack1ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨࣰ")]
def bstack11l111l11l_opy_():
  global bstack111l11111_opy_
  global bstack1l11l1l11_opy_
  global bstack1lll1l11ll_opy_
  bstack1l11l1l1ll_opy_ = []
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) - 1 and bstack1ll11_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࣱࠪ").lower() == val.lower():
      bstack111l11111_opy_[bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࣲࠬ")] = {}
      bstack111l11111_opy_[bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࣳ")][bstack1ll11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣴ")] = sys.argv[idx + 1]
      bstack1l11l1l1ll_opy_.extend([idx, idx + 1])
      break
  for key, bstack1l1ll11lll_opy_ in bstack11l111l1l_opy_.items():
    if isinstance(bstack1l1ll11lll_opy_, list):
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        for var in bstack1l1ll11lll_opy_:
          if bstack1ll11_opy_ (u"ࠫ࠲࠳ࠧࣵ") + var.lower() == val.lower() and key not in bstack111l11111_opy_:
            bstack111l11111_opy_[key] = sys.argv[idx + 1]
            bstack1l11l1l11_opy_ += bstack1ll11_opy_ (u"ࠬࠦ࠭࠮ࣶࠩ") + var + bstack1ll11_opy_ (u"࠭ࠠࠨࣷ") + shlex.quote(sys.argv[idx + 1])
            bstack1111llll1_opy_(bstack1lll1l11ll_opy_, key, sys.argv[idx + 1])
            bstack1l11l1l1ll_opy_.extend([idx, idx + 1])
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        if bstack1ll11_opy_ (u"ࠧ࠮࠯ࠪࣸ") + bstack1l1ll11lll_opy_.lower() == val.lower() and key not in bstack111l11111_opy_:
          bstack111l11111_opy_[key] = sys.argv[idx + 1]
          bstack1l11l1l11_opy_ += bstack1ll11_opy_ (u"ࠨࠢ࠰࠱ࣹࠬ") + bstack1l1ll11lll_opy_ + bstack1ll11_opy_ (u"ࣺࠩࠣࠫ") + shlex.quote(sys.argv[idx + 1])
          bstack1111llll1_opy_(bstack1lll1l11ll_opy_, key, sys.argv[idx + 1])
          bstack1l11l1l1ll_opy_.extend([idx, idx + 1])
  for idx in sorted(set(bstack1l11l1l1ll_opy_), reverse=True):
    if idx < len(sys.argv):
      del sys.argv[idx]
def bstack111ll1lll_opy_(config):
  bstack11l11llll_opy_ = config.keys()
  for bstack11lll11111_opy_, bstack1l1l11l111_opy_ in bstack1llll11l1l_opy_.items():
    if bstack1l1l11l111_opy_ in bstack11l11llll_opy_:
      config[bstack11lll11111_opy_] = config[bstack1l1l11l111_opy_]
      del config[bstack1l1l11l111_opy_]
  for bstack11lll11111_opy_, bstack1l1l11l111_opy_ in bstack1ll1111ll_opy_.items():
    if isinstance(bstack1l1l11l111_opy_, list):
      for bstack1111llll1l_opy_ in bstack1l1l11l111_opy_:
        if bstack1111llll1l_opy_ in bstack11l11llll_opy_:
          config[bstack11lll11111_opy_] = config[bstack1111llll1l_opy_]
          del config[bstack1111llll1l_opy_]
          break
    elif bstack1l1l11l111_opy_ in bstack11l11llll_opy_:
      config[bstack11lll11111_opy_] = config[bstack1l1l11l111_opy_]
      del config[bstack1l1l11l111_opy_]
  for bstack1111llll1l_opy_ in list(config):
    for bstack1l11lll1ll_opy_ in bstack1l1l1ll11l_opy_:
      if bstack1111llll1l_opy_.lower() == bstack1l11lll1ll_opy_.lower() and bstack1111llll1l_opy_ != bstack1l11lll1ll_opy_:
        config[bstack1l11lll1ll_opy_] = config[bstack1111llll1l_opy_]
        del config[bstack1111llll1l_opy_]
  bstack1l111lll1l_opy_ = [{}]
  if not config.get(bstack1ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣻ")):
    config[bstack1ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣼ")] = [{}]
  bstack1l111lll1l_opy_ = config[bstack1ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨࣽ")]
  for platform in bstack1l111lll1l_opy_:
    for bstack1111llll1l_opy_ in list(platform):
      for bstack1l11lll1ll_opy_ in bstack1l1l1ll11l_opy_:
        if bstack1111llll1l_opy_.lower() == bstack1l11lll1ll_opy_.lower() and bstack1111llll1l_opy_ != bstack1l11lll1ll_opy_:
          platform[bstack1l11lll1ll_opy_] = platform[bstack1111llll1l_opy_]
          del platform[bstack1111llll1l_opy_]
  for bstack11lll11111_opy_, bstack1l1l11l111_opy_ in bstack1ll1111ll_opy_.items():
    for platform in bstack1l111lll1l_opy_:
      if isinstance(bstack1l1l11l111_opy_, list):
        for bstack1111llll1l_opy_ in bstack1l1l11l111_opy_:
          if bstack1111llll1l_opy_ in platform:
            platform[bstack11lll11111_opy_] = platform[bstack1111llll1l_opy_]
            del platform[bstack1111llll1l_opy_]
            break
      elif bstack1l1l11l111_opy_ in platform:
        platform[bstack11lll11111_opy_] = platform[bstack1l1l11l111_opy_]
        del platform[bstack1l1l11l111_opy_]
  for bstack1ll1l1l11_opy_ in bstack1llllll1l_opy_:
    if bstack1ll1l1l11_opy_ in config:
      if not bstack1llllll1l_opy_[bstack1ll1l1l11_opy_] in config:
        config[bstack1llllll1l_opy_[bstack1ll1l1l11_opy_]] = {}
      config[bstack1llllll1l_opy_[bstack1ll1l1l11_opy_]].update(config[bstack1ll1l1l11_opy_])
      del config[bstack1ll1l1l11_opy_]
  for platform in bstack1l111lll1l_opy_:
    for bstack1ll1l1l11_opy_ in bstack1llllll1l_opy_:
      if bstack1ll1l1l11_opy_ in list(platform):
        if not bstack1llllll1l_opy_[bstack1ll1l1l11_opy_] in platform:
          platform[bstack1llllll1l_opy_[bstack1ll1l1l11_opy_]] = {}
        platform[bstack1llllll1l_opy_[bstack1ll1l1l11_opy_]].update(platform[bstack1ll1l1l11_opy_])
        del platform[bstack1ll1l1l11_opy_]
  config = bstack1l1ll1ll1l_opy_(config)
  return config
def bstack1ll11lll1_opy_(config):
  global bstack111lll11_opy_
  bstack111l1lllll_opy_ = False
  bstack111ll11ll1_opy_ = os.environ.get(bstack1ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡊࡅࡇࡃࡘࡐ࡙ࡥࡌࡐࡅࡄࡐࡤࡏࡄࠨࣾ"))
  if bstack1ll11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫࣿ") in config and str(config[bstack1ll11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬऀ")]).lower() != bstack1ll11_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨँ"):
    if bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧं") not in config or str(config[bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨः")]).lower() == bstack1ll11_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫऄ"):
      config[bstack1ll11_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬअ")] = False
    else:
      bstack1l11l11l_opy_ = bstack1l111111_opy_()
      if bstack1ll11_opy_ (u"ࠧࡪࡵࡗࡶ࡮ࡧ࡬ࡈࡴ࡬ࡨࠬआ") in bstack1l11l11l_opy_:
        if not bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬइ") in config:
          config[bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ई")] = {}
        config[bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧउ")][bstack1ll11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ऊ")] = bstack1ll11_opy_ (u"ࠬࡧࡴࡴ࠯ࡵࡩࡵ࡫ࡡࡵࡧࡵࠫऋ")
        bstack111l1lllll_opy_ = True
        bstack111lll11_opy_ = config[bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪऌ")].get(bstack1ll11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऍ"))
  if bstack1ll11l1l11_opy_(config) and bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬऎ") in config and str(config[bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ए")]).lower() != bstack1ll11_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩऐ") and not bstack111l1lllll_opy_:
    if not bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऑ") in config:
      config[bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩऒ")] = {}
    bstack11lll1lll_opy_ = config[bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪओ")].get(bstack1ll11_opy_ (u"ࠧࡴ࡭࡬ࡴࡇ࡯࡮ࡢࡴࡼࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡸࡧࡴࡪࡱࡱࠫऔ"))
    if bstack111ll11ll1_opy_:
      if bstack11lll1lll_opy_:
        config[bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬक")][bstack1ll11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫख")] = bstack111ll11ll1_opy_
      elif bstack1ll11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬग") not in config[bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨघ")]:
        config[bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩङ")][bstack1ll11_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨच")] = bstack111ll11ll1_opy_
    if not bstack11lll1lll_opy_ and bstack1ll11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩछ") not in config[bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬज")]:
      current_time = datetime.datetime.now()
      bstack11ll1ll11l_opy_ = current_time.strftime(bstack1ll11_opy_ (u"ࠩࠨࡨࡤࠫࡢࡠࠧࡋࠩࡒ࠭झ"))
      hostname = socket.gethostname()
      bstack1l1l1lllll_opy_ = bstack1ll11_opy_ (u"ࠪࠫञ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1ll11_opy_ (u"ࠫࢀࢃ࡟ࡼࡿࡢࡿࢂ࠭ट").format(bstack11ll1ll11l_opy_, hostname, bstack1l1l1lllll_opy_)
      config[bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩठ")][bstack1ll11_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨड")] = identifier
    bstack111lll11_opy_ = config[bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫढ")].get(bstack1ll11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪण"))
  return config
def bstack11l11l1l1_opy_():
  bstack11l11l1ll_opy_ =  bstack11ll11l1l1_opy_()[bstack1ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠨत")]
  return bstack11l11l1ll_opy_ if bstack11l11l1ll_opy_ else -1
def bstack11ll1lll1l_opy_(bstack11l11l1ll_opy_):
  global CONFIG
  if not bstack1ll11_opy_ (u"ࠪࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬथ") in CONFIG[bstack1ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭द")]:
    return
  CONFIG[bstack1ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧध")] = CONFIG[bstack1ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨन")].replace(
    bstack1ll11_opy_ (u"ࠧࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩऩ"),
    str(bstack11l11l1ll_opy_)
  )
def bstack111l11l1ll_opy_():
  global CONFIG
  if not bstack1ll11_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧप") in CONFIG[bstack1ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫफ")]:
    return
  current_time = datetime.datetime.now()
  bstack11ll1ll11l_opy_ = current_time.strftime(bstack1ll11_opy_ (u"ࠪࠩࡩ࠳ࠥࡣ࠯ࠨࡌ࠿ࠫࡍࠨब"))
  CONFIG[bstack1ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭भ")] = CONFIG[bstack1ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧम")].replace(
    bstack1ll11_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬय"),
    bstack11ll1ll11l_opy_
  )
def bstack1l111ll1l_opy_():
  global CONFIG
  if bstack1ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩर") in CONFIG and not bool(CONFIG[bstack1ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪऱ")]):
    del CONFIG[bstack1ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫल")]
    return
  if not bstack1ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬळ") in CONFIG:
    CONFIG[bstack1ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ऴ")] = bstack1ll11_opy_ (u"ࠬࠩࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨव")
  if bstack1ll11_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬश") in CONFIG[bstack1ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩष")]:
    bstack111l11l1ll_opy_()
    os.environ[bstack1ll11_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬस")] = CONFIG[bstack1ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫह")]
  if not bstack1ll11_opy_ (u"ࠪࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬऺ") in CONFIG[bstack1ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ऻ")]:
    return
  bstack11l11l1ll_opy_ = bstack1ll11_opy_ (u"़ࠬ࠭")
  bstack1llll1lll1_opy_ = bstack11l11l1l1_opy_()
  if bstack1llll1lll1_opy_ != -1:
    bstack11l11l1ll_opy_ = bstack1ll11_opy_ (u"࠭ࡃࡊࠢࠪऽ") + str(bstack1llll1lll1_opy_)
  if bstack11l11l1ll_opy_ == bstack1ll11_opy_ (u"ࠧࠨा"):
    bstack11111l1l11_opy_ = bstack111l1l11_opy_(CONFIG[bstack1ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫि")])
    if bstack11111l1l11_opy_ != -1:
      bstack11l11l1ll_opy_ = str(bstack11111l1l11_opy_)
  if bstack11l11l1ll_opy_:
    bstack11ll1lll1l_opy_(bstack11l11l1ll_opy_)
    os.environ[bstack1ll11_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ी")] = CONFIG[bstack1ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬु")]
def bstack1l1llll11l_opy_(bstack1llll1ll_opy_, bstack1111l1ll11_opy_, path):
  json_data = {
    bstack1ll11_opy_ (u"ࠫ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨू"): bstack1111l1ll11_opy_
  }
  if os.path.exists(path):
    bstack1l1l1lll_opy_ = json.load(open(path, bstack1ll11_opy_ (u"ࠬࡸࡢࠨृ")))
  else:
    bstack1l1l1lll_opy_ = {}
  bstack1l1l1lll_opy_[bstack1llll1ll_opy_] = json_data
  with open(path, bstack1ll11_opy_ (u"ࠨࡷࠬࠤॄ")) as outfile:
    json.dump(bstack1l1l1lll_opy_, outfile)
def bstack111l1l11_opy_(bstack1llll1ll_opy_):
  bstack1llll1ll_opy_ = str(bstack1llll1ll_opy_)
  bstack1lll111l11_opy_ = os.path.join(os.path.expanduser(bstack1ll11_opy_ (u"ࠧࡿࠩॅ")), bstack1ll11_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨॆ"))
  try:
    if not os.path.exists(bstack1lll111l11_opy_):
      os.makedirs(bstack1lll111l11_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1ll11_opy_ (u"ࠩࢁࠫे")), bstack1ll11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪै"), bstack1ll11_opy_ (u"ࠫ࠳ࡨࡵࡪ࡮ࡧ࠱ࡳࡧ࡭ࡦ࠯ࡦࡥࡨ࡮ࡥ࠯࡬ࡶࡳࡳ࠭ॉ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1ll11_opy_ (u"ࠬࡽࠧॊ")):
        pass
      with open(file_path, bstack1ll11_opy_ (u"ࠨࡷࠬࠤो")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1ll11_opy_ (u"ࠧࡳࠩौ")) as bstack1l1ll11l1_opy_:
      bstack111l11ll1l_opy_ = json.load(bstack1l1ll11l1_opy_)
    if bstack1llll1ll_opy_ in bstack111l11ll1l_opy_:
      bstack111l1l111_opy_ = bstack111l11ll1l_opy_[bstack1llll1ll_opy_][bstack1ll11_opy_ (u"ࠨ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ्ࠬ")]
      bstack1111l1ll_opy_ = int(bstack111l1l111_opy_) + 1
      bstack1l1llll11l_opy_(bstack1llll1ll_opy_, bstack1111l1ll_opy_, file_path)
      return bstack1111l1ll_opy_
    else:
      bstack1l1llll11l_opy_(bstack1llll1ll_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warning(bstack1ll1ll111_opy_.format(str(e)))
    return -1
def bstack11ll1111_opy_(config):
  if not config[bstack1ll11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫॎ")] or not config[bstack1ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ॏ")]:
    return True
  else:
    return False
def bstack111llllll1_opy_(config, index=0):
  global bstack1l11lll111_opy_
  bstack1llll11ll1_opy_ = {}
  caps = bstack111ll111l1_opy_ + bstack1111l1l1l_opy_
  if config.get(bstack1ll11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨॐ"), False):
    bstack1llll11ll1_opy_[bstack1ll11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩ॑")] = True
    bstack1llll11ll1_opy_[bstack1ll11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࡒࡴࡹ࡯࡯࡯ࡵ॒ࠪ")] = config.get(bstack1ll11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࡓࡵࡺࡩࡰࡰࡶࠫ॓"), {})
  if bstack1l11lll111_opy_:
    caps += bstack111l111ll1_opy_
  for key in config:
    if key in caps + [bstack1ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ॔")]:
      continue
    bstack1llll11ll1_opy_[key] = config[key]
  if bstack1ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॕ") in config:
    for bstack1ll1l1l111_opy_ in config[bstack1ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॖ")][index]:
      if bstack1ll1l1l111_opy_ in caps:
        continue
      bstack1llll11ll1_opy_[bstack1ll1l1l111_opy_] = config[bstack1ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॗ")][index][bstack1ll1l1l111_opy_]
  bstack1llll11ll1_opy_[bstack1ll11_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧक़")] = socket.gethostname()
  if bstack1ll11_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧख़") in bstack1llll11ll1_opy_:
    del (bstack1llll11ll1_opy_[bstack1ll11_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨग़")])
  return bstack1llll11ll1_opy_
def bstack11l1l11111_opy_(config):
  global bstack1l11lll111_opy_
  bstack1l11llll1l_opy_ = {}
  caps = bstack1111l1l1l_opy_
  if bstack1l11lll111_opy_:
    caps += bstack111l111ll1_opy_
  for key in caps:
    if key in config:
      bstack1l11llll1l_opy_[key] = config[key]
  return bstack1l11llll1l_opy_
def bstack111l1lll_opy_(bstack1llll11ll1_opy_, bstack1l11llll1l_opy_):
  bstack11l111lll1_opy_ = {}
  for key in bstack1llll11ll1_opy_.keys():
    if key in bstack1llll11l1l_opy_:
      bstack11l111lll1_opy_[bstack1llll11l1l_opy_[key]] = bstack1llll11ll1_opy_[key]
    else:
      bstack11l111lll1_opy_[key] = bstack1llll11ll1_opy_[key]
  for key in bstack1l11llll1l_opy_:
    if key in bstack1llll11l1l_opy_:
      bstack11l111lll1_opy_[bstack1llll11l1l_opy_[key]] = bstack1l11llll1l_opy_[key]
    else:
      bstack11l111lll1_opy_[key] = bstack1l11llll1l_opy_[key]
  return bstack11l111lll1_opy_
def get_caps(config, index=0):
  global bstack1l11lll111_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack1l11ll1l1_opy_ = bstack11111l11ll_opy_(bstack1lll11l1_opy_, config, logger)
  bstack1l11llll1l_opy_ = bstack11l1l11111_opy_(config)
  bstack1l11ll1l_opy_ = bstack1111l1l1l_opy_
  bstack1l11ll1l_opy_ += bstack1l1ll11ll_opy_
  bstack1l11llll1l_opy_ = update(bstack1l11llll1l_opy_, bstack1l11ll1l1_opy_)
  if bstack1l11lll111_opy_:
    bstack1l11ll1l_opy_ += bstack111l111ll1_opy_
  if bstack1ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫज़") in config:
    if bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧड़") in config[bstack1ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ढ़")][index]:
      caps[bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩफ़")] = config[bstack1ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨय़")][index][bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫॠ")]
    if bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨॡ") in config[bstack1ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫॢ")][index]:
      caps[bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪॣ")] = str(config[bstack1ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭।")][index][bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ॥")])
    bstack11ll1lllll_opy_ = bstack11111l11ll_opy_(bstack1lll11l1_opy_, config[bstack1ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ०")][index], logger)
    bstack1l11ll1l_opy_ += list(bstack11ll1lllll_opy_.keys())
    for bstack11lll11l11_opy_ in bstack1l11ll1l_opy_:
      if bstack11lll11l11_opy_ in config[bstack1ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ१")][index]:
        if bstack11lll11l11_opy_ == bstack1ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ२"):
          try:
            bstack11ll1lllll_opy_[bstack11lll11l11_opy_] = str(config[bstack1ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ३")][index][bstack11lll11l11_opy_] * 1.0)
          except:
            bstack11ll1lllll_opy_[bstack11lll11l11_opy_] = str(config[bstack1ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ४")][index][bstack11lll11l11_opy_])
        else:
          bstack11ll1lllll_opy_[bstack11lll11l11_opy_] = config[bstack1ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭५")][index][bstack11lll11l11_opy_]
        del (config[bstack1ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ६")][index][bstack11lll11l11_opy_])
    bstack1l11llll1l_opy_ = update(bstack1l11llll1l_opy_, bstack11ll1lllll_opy_)
  bstack1llll11ll1_opy_ = bstack111llllll1_opy_(config, index)
  for bstack1111llll1l_opy_ in bstack1111l1l1l_opy_ + list(bstack1l11ll1l1_opy_.keys()):
    if bstack1111llll1l_opy_ in bstack1llll11ll1_opy_:
      bstack1l11llll1l_opy_[bstack1111llll1l_opy_] = bstack1llll11ll1_opy_[bstack1111llll1l_opy_]
      del (bstack1llll11ll1_opy_[bstack1111llll1l_opy_])
  if bstack11l11l1l1l_opy_(config):
    bstack1llll11ll1_opy_[bstack1ll11_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ७")] = True
    caps.update(bstack1l11llll1l_opy_)
    caps[bstack1ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ८")] = bstack1llll11ll1_opy_
  else:
    bstack1llll11ll1_opy_[bstack1ll11_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧ९")] = False
    caps.update(bstack111l1lll_opy_(bstack1llll11ll1_opy_, bstack1l11llll1l_opy_))
    if bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭॰") in caps:
      caps[bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪॱ")] = caps[bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨॲ")]
      del (caps[bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩॳ")])
    if bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ॴ") in caps:
      caps[bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨॵ")] = caps[bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨॶ")]
      del (caps[bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩॷ")])
  return caps
def bstack1l111llll1_opy_():
  global bstack11llll1l1l_opy_
  global CONFIG
  if bstack11llll1l1l_opy_ != bstack1ll11_opy_ (u"ࠩࠪॸ") and (bstack11llll1l1l_opy_.startswith(bstack1ll11_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫॹ")) or bstack11llll1l1l_opy_.startswith(bstack1ll11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࠭ॺ"))):
    return bstack11llll1l1l_opy_
  if bstack1lll11llll_opy_() <= version.parse(bstack1ll11_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬॻ")):
    if bstack11llll1l1l_opy_ != bstack1ll11_opy_ (u"࠭ࠧॼ"):
      return bstack1ll11_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣॽ") + bstack11llll1l1l_opy_ + bstack1ll11_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧॾ")
    return bstack111l111ll_opy_
  if bstack11llll1l1l_opy_ != bstack1ll11_opy_ (u"ࠩࠪॿ"):
    return bstack1ll11_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧঀ") + bstack11llll1l1l_opy_ + bstack1ll11_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧঁ")
  return HTTPS_HUB
def bstack11l11111l1_opy_(options):
  return hasattr(options, bstack1ll11_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭ং"))
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
def bstack111l1l1l11_opy_(options, bstack1l1111lll1_opy_):
  for bstack11l1l1l11_opy_ in bstack1l1111lll1_opy_:
    if bstack11l1l1l11_opy_ in [bstack1ll11_opy_ (u"࠭ࡡࡳࡩࡶࠫঃ"), bstack1ll11_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫ঄")]:
      continue
    if bstack11l1l1l11_opy_ in options._experimental_options:
      options._experimental_options[bstack11l1l1l11_opy_] = update(options._experimental_options[bstack11l1l1l11_opy_],
                                                         bstack1l1111lll1_opy_[bstack11l1l1l11_opy_])
    else:
      options.add_experimental_option(bstack11l1l1l11_opy_, bstack1l1111lll1_opy_[bstack11l1l1l11_opy_])
  if bstack1ll11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭অ") in bstack1l1111lll1_opy_:
    for arg in bstack1l1111lll1_opy_[bstack1ll11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧআ")]:
      options.add_argument(arg)
    del (bstack1l1111lll1_opy_[bstack1ll11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨই")])
  if bstack1ll11_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨঈ") in bstack1l1111lll1_opy_:
    for ext in bstack1l1111lll1_opy_[bstack1ll11_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩউ")]:
      try:
        options.add_extension(ext)
      except OSError:
        options.add_encoded_extension(ext)
    del (bstack1l1111lll1_opy_[bstack1ll11_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪঊ")])
def bstack1l111l111_opy_(options):
  global CONFIG
  global bstack11l1l1ll11_opy_
  try:
    if not bstack11l1l1ll11_opy_ or not options:
      return options
    from bstack_utils.bstack1ll1ll11_opy_ import bstack1lll11l11l_opy_
    bstack1llll11l_opy_ = bstack1lll11l11l_opy_(options, bstack1l1l11111l_opy_=bstack1ll11_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢঋ"))
    if bstack1llll11l_opy_ > 0:
      logger.debug(bstack1ll11_opy_ (u"ࠣࡎࡲࡥࡩࠦࡴࡦࡵࡷ࡭ࡳ࡭࠺ࠡࡃࡧࡨࡪࡪࠠࡼࡿࠣࡨࡪ࡬ࡡࡶ࡮ࡷࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠠࡧࡱࡵࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠦঌ").format(bstack1llll11l_opy_))
  except Exception as e:
    logger.debug(bstack1ll11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡯࡮࡫ࡧࡦࡸࠥࡲ࡯ࡢࡦࠣࡸࡪࡹࡴࡪࡰࡪࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡴࡶࡴࡪࡱࡱࡷ࠿ࠦࡻࡾࠤ঍").format(e))
  return options
def bstack1l1l1llll_opy_(options, bstack111lllllll_opy_):
  if bstack1ll11_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩ঎") in bstack111lllllll_opy_:
    for bstack1l1l11lll1_opy_ in bstack111lllllll_opy_[bstack1ll11_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪএ")]:
      if bstack1l1l11lll1_opy_ in options._preferences:
        options._preferences[bstack1l1l11lll1_opy_] = update(options._preferences[bstack1l1l11lll1_opy_], bstack111lllllll_opy_[bstack1ll11_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫঐ")][bstack1l1l11lll1_opy_])
      else:
        options.set_preference(bstack1l1l11lll1_opy_, bstack111lllllll_opy_[bstack1ll11_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬ঑")][bstack1l1l11lll1_opy_])
  if bstack1ll11_opy_ (u"ࠧࡢࡴࡪࡷࠬ঒") in bstack111lllllll_opy_:
    for arg in bstack111lllllll_opy_[bstack1ll11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ও")]:
      options.add_argument(arg)
def bstack1llll11lll_opy_(options, bstack1111l11lll_opy_):
  if bstack1ll11_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࠪঔ") in bstack1111l11lll_opy_:
    options.use_webview(bool(bstack1111l11lll_opy_[bstack1ll11_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࠫক")]))
  bstack111l1l1l11_opy_(options, bstack1111l11lll_opy_)
def bstack11l1l1111_opy_(options, bstack11111ll1ll_opy_):
  for bstack1l11l1lll1_opy_ in bstack11111ll1ll_opy_:
    if bstack1l11l1lll1_opy_ in [bstack1ll11_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨখ"), bstack1ll11_opy_ (u"ࠬࡧࡲࡨࡵࠪগ")]:
      continue
    options.set_capability(bstack1l11l1lll1_opy_, bstack11111ll1ll_opy_[bstack1l11l1lll1_opy_])
  if bstack1ll11_opy_ (u"࠭ࡡࡳࡩࡶࠫঘ") in bstack11111ll1ll_opy_:
    for arg in bstack11111ll1ll_opy_[bstack1ll11_opy_ (u"ࠧࡢࡴࡪࡷࠬঙ")]:
      options.add_argument(arg)
  if bstack1ll11_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬচ") in bstack11111ll1ll_opy_:
    options.bstack1111l1l11l_opy_(bool(bstack11111ll1ll_opy_[bstack1ll11_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭ছ")]))
def bstack1l1111llll_opy_(options, bstack111lll1l1l_opy_):
  for bstack1l1l1l11ll_opy_ in bstack111lll1l1l_opy_:
    if bstack1l1l1l11ll_opy_ in [bstack1ll11_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧজ"), bstack1ll11_opy_ (u"ࠫࡦࡸࡧࡴࠩঝ")]:
      continue
    options._options[bstack1l1l1l11ll_opy_] = bstack111lll1l1l_opy_[bstack1l1l1l11ll_opy_]
  if bstack1ll11_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩঞ") in bstack111lll1l1l_opy_:
    for bstack111l1111ll_opy_ in bstack111lll1l1l_opy_[bstack1ll11_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪট")]:
      options.bstack1l111l1l1l_opy_(
        bstack111l1111ll_opy_, bstack111lll1l1l_opy_[bstack1ll11_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫঠ")][bstack111l1111ll_opy_])
  if bstack1ll11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ড") in bstack111lll1l1l_opy_:
    for arg in bstack111lll1l1l_opy_[bstack1ll11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧঢ")]:
      options.add_argument(arg)
def bstack1l11ll11_opy_(options, caps):
  if not hasattr(options, bstack1ll11_opy_ (u"ࠪࡏࡊ࡟ࠧণ")):
    return
  if options.KEY == bstack1ll11_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩত"):
    options = a11y.bstack1l1ll1l111_opy_(bstack1l1lll1l1_opy_=options, config=CONFIG)
  if options.KEY == bstack1ll11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪথ") and options.KEY in caps:
    bstack111l1l1l11_opy_(options, caps[bstack1ll11_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫদ")])
  elif options.KEY == bstack1ll11_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬধ") and options.KEY in caps:
    bstack1l1l1llll_opy_(options, caps[bstack1ll11_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ন")])
  elif options.KEY == bstack1ll11_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪ঩") and options.KEY in caps:
    bstack11l1l1111_opy_(options, caps[bstack1ll11_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫপ")])
  elif options.KEY == bstack1ll11_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬফ") and options.KEY in caps:
    bstack1llll11lll_opy_(options, caps[bstack1ll11_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ব")])
  elif options.KEY == bstack1ll11_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬভ") and options.KEY in caps:
    bstack1l1111llll_opy_(options, caps[bstack1ll11_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ম")])
def bstack1l1l11ll_opy_(caps):
  global bstack1l11lll111_opy_
  if isinstance(os.environ.get(bstack1ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩয")), str):
    bstack1l11lll111_opy_ = eval(os.getenv(bstack1ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪর")))
  if bstack1l11lll111_opy_:
    if bstack1111ll11l1_opy_() < version.parse(bstack1ll11_opy_ (u"ࠪ࠶࠳࠹࠮࠱ࠩ঱")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1ll11_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫল")
    if bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ঳") in caps:
      browser = caps[bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ঴")]
    elif bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ঵") in caps:
      browser = caps[bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩশ")]
    browser = str(browser).lower()
    if browser == bstack1ll11_opy_ (u"ࠩ࡬ࡴ࡭ࡵ࡮ࡦࠩষ") or browser == bstack1ll11_opy_ (u"ࠪ࡭ࡵࡧࡤࠨস"):
      browser = bstack1ll11_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫহ")
    if browser == bstack1ll11_opy_ (u"ࠬࡹࡡ࡮ࡵࡸࡲ࡬࠭঺"):
      browser = bstack1ll11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭঻")
    if browser not in [bstack1ll11_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫়ࠧ"), bstack1ll11_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭ঽ"), bstack1ll11_opy_ (u"ࠩ࡬ࡩࠬা"), bstack1ll11_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪি"), bstack1ll11_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬী")]:
      return None
    try:
      package = bstack1ll11_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡿࢂ࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧু").format(browser)
      name = bstack1ll11_opy_ (u"࠭ࡏࡱࡶ࡬ࡳࡳࡹࠧূ")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack11l11111l1_opy_(options):
        return None
      for bstack1111llll1l_opy_ in caps.keys():
        options.set_capability(bstack1111llll1l_opy_, caps[bstack1111llll1l_opy_])
      bstack1l11ll11_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack111ll1ll1_opy_(options, bstack1lll1ll1_opy_):
  if not bstack11l11111l1_opy_(options):
    return
  for bstack1111llll1l_opy_ in bstack1lll1ll1_opy_.keys():
    if bstack1111llll1l_opy_ in bstack1l1ll11ll_opy_:
      continue
    if bstack1111llll1l_opy_ in options._caps and type(options._caps[bstack1111llll1l_opy_]) in [dict, list]:
      options._caps[bstack1111llll1l_opy_] = update(options._caps[bstack1111llll1l_opy_], bstack1lll1ll1_opy_[bstack1111llll1l_opy_])
    else:
      options.set_capability(bstack1111llll1l_opy_, bstack1lll1ll1_opy_[bstack1111llll1l_opy_])
  bstack1l11ll11_opy_(options, bstack1lll1ll1_opy_)
  if bstack1ll11_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ࠭ৃ") in options._caps:
    if options._caps[bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ৄ")] and options._caps[bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ৅")].lower() != bstack1ll11_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫ৆"):
      del options._caps[bstack1ll11_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪে")]
def bstack1111l11l1_opy_(proxy_config):
  if bstack1ll11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩৈ") in proxy_config:
    proxy_config[bstack1ll11_opy_ (u"࠭ࡳࡴ࡮ࡓࡶࡴࡾࡹࠨ৉")] = proxy_config[bstack1ll11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ৊")]
    del (proxy_config[bstack1ll11_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬো")])
  if bstack1ll11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬৌ") in proxy_config and proxy_config[bstack1ll11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ্࠭")].lower() != bstack1ll11_opy_ (u"ࠫࡩ࡯ࡲࡦࡥࡷࠫৎ"):
    proxy_config[bstack1ll11_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ৏")] = bstack1ll11_opy_ (u"࠭࡭ࡢࡰࡸࡥࡱ࠭৐")
  if bstack1ll11_opy_ (u"ࠧࡱࡴࡲࡼࡾࡇࡵࡵࡱࡦࡳࡳ࡬ࡩࡨࡗࡵࡰࠬ৑") in proxy_config:
    proxy_config[bstack1ll11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫ৒")] = bstack1ll11_opy_ (u"ࠩࡳࡥࡨ࠭৓")
  return proxy_config
def bstack1l11l11111_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1ll11_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩ৔") in config:
    return proxy
  config[bstack1ll11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪ৕")] = bstack1111l11l1_opy_(config[bstack1ll11_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ৖")])
  if proxy == None:
    proxy = Proxy(config[bstack1ll11_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬৗ")])
  return proxy
def bstack1ll1ll1111_opy_(self):
  global CONFIG
  global bstack1111l1l11_opy_
  try:
    proxy = bstack11l11lll1_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1ll11_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ৘")):
        proxies = bstack111l1l1l_opy_(proxy, bstack1l111llll1_opy_())
        if len(proxies) > 0:
          protocol, bstack111111l1ll_opy_ = proxies.popitem()
          if bstack1ll11_opy_ (u"ࠣ࠼࠲࠳ࠧ৙") in bstack111111l1ll_opy_:
            return bstack111111l1ll_opy_
          else:
            return bstack1ll11_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ৚") + bstack111111l1ll_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1ll11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡰࡳࡱࡻࡽࠥࡻࡲ࡭ࠢ࠽ࠤࢀࢃࠢ৛").format(str(e)))
  return bstack1111l1l11_opy_(self)
def bstack11lllll1l1_opy_():
  global CONFIG
  return bstack1111lllll_opy_(CONFIG) and bstack1l1111111_opy_() and bstack1lll11llll_opy_() >= version.parse(bstack1l11l1l11l_opy_)
def bstack1ll111l11_opy_():
  global CONFIG
  return (bstack1ll11_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧড়") in CONFIG or bstack1ll11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩঢ়") in CONFIG) and bstack111111111l_opy_()
def bstack11ll1ll1ll_opy_(config):
  bstack1ll1l11l1_opy_ = {}
  if bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ৞") in config:
    bstack1ll1l11l1_opy_ = config[bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫয়")]
  if bstack1ll11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧৠ") in config:
    bstack1ll1l11l1_opy_ = config[bstack1ll11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨৡ")]
  proxy = bstack11l11lll1_opy_(config)
  if proxy:
    if proxy.endswith(bstack1ll11_opy_ (u"ࠪ࠲ࡵࡧࡣࠨৢ")) and os.path.isfile(proxy):
      bstack1ll1l11l1_opy_[bstack1ll11_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧৣ")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1ll11_opy_ (u"ࠬ࠴ࡰࡢࡥࠪ৤")):
        proxies = bstack11lllll1l_opy_(config, bstack1l111llll1_opy_())
        if len(proxies) > 0:
          protocol, bstack111111l1ll_opy_ = proxies.popitem()
          if bstack1ll11_opy_ (u"ࠨ࠺࠰࠱ࠥ৥") in bstack111111l1ll_opy_:
            parsed_url = urlparse(bstack111111l1ll_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1ll11_opy_ (u"ࠢ࠻࠱࠲ࠦ০") + bstack111111l1ll_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1ll1l11l1_opy_[bstack1ll11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡈࡰࡵࡷࠫ১")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1ll1l11l1_opy_[bstack1ll11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬ২")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1ll1l11l1_opy_[bstack1ll11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭৩")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1ll1l11l1_opy_[bstack1ll11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧ৪")] = str(parsed_url.password)
  return bstack1ll1l11l1_opy_
def bstack1lll1llll1_opy_(config):
  if bstack1ll11_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪ৫") in config:
    return config[bstack1ll11_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫ৬")]
  return {}
def update_caps_for_local(caps):
  global bstack111lll11_opy_
  if bstack1ll11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ৭") in caps:
    caps[bstack1ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ৮")][bstack1ll11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨ৯")] = True
    if bstack111lll11_opy_:
      caps[bstack1ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫৰ")][bstack1ll11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ৱ")] = bstack111lll11_opy_
  else:
    caps[bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪ৲")] = True
    if bstack111lll11_opy_:
      caps[bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ৳")] = bstack111lll11_opy_
@measure(event_name=EVENTS.bstack1ll1lllll_opy_, stage=STAGE.bstack11111llll_opy_, bstack11lll1l111_opy_=SESSION_NAME)
def bstack1111l1l1ll_opy_():
  global CONFIG, bstack111lll11_opy_
  if not bstack1ll11l1l11_opy_(CONFIG) or cli.is_enabled(CONFIG):
    return
  if bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ৴") in CONFIG and bstack1lll1111ll_opy_(CONFIG[bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ৵")]):
    if (
      bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭৶") in CONFIG
      and bstack1lll1111ll_opy_(CONFIG[bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ৷")].get(bstack1ll11_opy_ (u"ࠫࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠨ৸")))
    ):
      logger.debug(bstack1ll11_opy_ (u"ࠧࡒ࡯ࡤࡣ࡯ࠤࡧ࡯࡮ࡢࡴࡼࠤࡳࡵࡴࠡࡵࡷࡥࡷࡺࡥࡥࠢࡤࡷࠥࡹ࡫ࡪࡲࡅ࡭ࡳࡧࡲࡺࡋࡱ࡭ࡹ࡯ࡡ࡭࡫ࡶࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠨ৹"))
      return
    bstack1ll1l11l1_opy_ = bstack11ll1ll1ll_opy_(CONFIG)
    bstack111lll11_opy_ = bstack1ll1l11l1_opy_.get(bstack1ll11_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ৺")) or bstack111lll11_opy_
    bstack1l11l11ll_opy_(CONFIG[bstack1ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ৻")], bstack1ll1l11l1_opy_)
def bstack1l11l11ll_opy_(key, bstack1ll1l11l1_opy_):
  global bstack1ll11ll11_opy_
  logger.info(bstack1ll1llll1l_opy_)
  try:
    bstack1ll11ll11_opy_ = Local()
    bstack111l1llll_opy_ = {bstack1ll11_opy_ (u"ࠨ࡭ࡨࡽࠬৼ"): key}
    bstack111l1llll_opy_.update(bstack1ll1l11l1_opy_)
    logger.debug(bstack11llllllll_opy_.format(str(bstack111l1llll_opy_)).replace(key, bstack1ll11_opy_ (u"ࠩ࡞ࡖࡊࡊࡁࡄࡖࡈࡈࡢ࠭৽")))
    bstack1ll11ll11_opy_.start(**bstack111l1llll_opy_)
    if bstack1ll11ll11_opy_.isRunning():
      logger.info(bstack11ll1llll_opy_)
  except Exception as e:
    bstack11l1l111l1_opy_(bstack1l1l1111l1_opy_.format(str(e)))
def bstack11ll1l1l1l_opy_():
  global bstack1ll11ll11_opy_
  if bstack1ll11ll11_opy_.isRunning():
    logger.info(bstack1lllllll1l_opy_)
    bstack1ll11ll11_opy_.stop()
  if bstack1ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡇࡉࡋࡇࡕࡍࡖࡢࡐࡔࡉࡁࡍࡡࡌࡈࠬ৾") in os.environ:
    del os.environ[bstack1ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡈࡊࡌࡁࡖࡎࡗࡣࡑࡕࡃࡂࡎࡢࡍࡉ࠭৿")]
  bstack1ll11ll11_opy_ = None
def bstack1l1l1111ll_opy_(bstack1111l1lll_opy_=[]):
  global CONFIG
  bstack1l1l11l11_opy_ = []
  bstack11ll1l1ll1_opy_ = [bstack1ll11_opy_ (u"ࠬࡵࡳࠨ਀"), bstack1ll11_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩਁ"), bstack1ll11_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫਂ"), bstack1ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪਃ"), bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ਄"), bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫਅ")]
  try:
    for err in bstack1111l1lll_opy_:
      bstack1l1ll1ll_opy_ = {}
      for k in bstack11ll1l1ll1_opy_:
        val = CONFIG[bstack1ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਆ")][int(err[bstack1ll11_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫਇ")])].get(k)
        if val:
          bstack1l1ll1ll_opy_[k] = val
      if(err[bstack1ll11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬਈ")] != bstack1ll11_opy_ (u"ࠧࠨਉ")):
        bstack1l1ll1ll_opy_[bstack1ll11_opy_ (u"ࠨࡶࡨࡷࡹࡹࠧਊ")] = {
          err[bstack1ll11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ਋")]: err[bstack1ll11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ਌")]
        }
        bstack1l1l11l11_opy_.append(bstack1l1ll1ll_opy_)
  except Exception as e:
    logger.debug(bstack1ll11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡰࡴࡰࡥࡹࡺࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷ࠾ࠥ࠭਍") + str(e))
  finally:
    return bstack1l1l11l11_opy_
def bstack111l111l1_opy_(file_name):
  bstack11lll1111l_opy_ = []
  try:
    bstack111ll1ll11_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack111ll1ll11_opy_):
      with open(bstack111ll1ll11_opy_) as f:
        bstack1111lll111_opy_ = json.load(f)
        bstack11lll1111l_opy_ = bstack1111lll111_opy_
      os.remove(bstack111ll1ll11_opy_)
    return bstack11lll1111l_opy_
  except Exception as e:
    logger.debug(bstack1ll11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧ࡫ࡱࡨ࡮ࡴࡧࠡࡧࡵࡶࡴࡸࠠ࡭࡫ࡶࡸ࠿ࠦࠧ਎") + str(e))
    return bstack11lll1111l_opy_
def bstack11llll1ll1_opy_():
  try:
      import time
      from bstack_utils.constants import bstack1lll1ll1ll_opy_, EVENTS
      from bstack_utils.helper import bstack1ll11l111l_opy_, get_host_info, global_config
      from datetime import datetime
      from filelock import FileLock
      from bstack_utils.bstack1ll1lll11l_opy_ import bstack11ll11l1ll_opy_
      bstack11ll11l1ll_opy_.bstack11lllllll1_opy_()
      bstack111l11l1_opy_ = os.path.join(os.getcwd(), bstack1ll11_opy_ (u"࠭࡬ࡰࡩࠪਏ"), bstack1ll11_opy_ (u"ࠧ࡬ࡧࡼ࠱ࡲ࡫ࡴࡳ࡫ࡦࡷ࠳ࡰࡳࡰࡰࠪਐ"))
      data = None
      lock = FileLock(bstack111l11l1_opy_+bstack1ll11_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢ਑"), timeout=2)
      try:
          with lock:
              with open(bstack111l11l1_opy_, bstack1ll11_opy_ (u"ࠤࡵࠦ਒"), encoding=bstack1ll11_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤਓ")) as file:
                  data = json.load(file)
      except Exception as e:
          logger.debug(bstack1ll11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡳࡧࡤࡨࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵࠣࡪ࡮ࡲࡥ࠻ࠢࡾࢁࠧਔ").format(e))
          return
      if not data:
          return
      def bstack11l1111lll_opy_():
          try:
              config = {
                  bstack1ll11_opy_ (u"ࠧ࡮ࡥࡢࡦࡨࡶࡸࠨਕ"): {
                      bstack1ll11_opy_ (u"ࠨࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠧਖ"): bstack1ll11_opy_ (u"ࠢࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠥਗ"),
                  }
              }
              bstack11l1l1ll_opy_ = datetime.utcnow()
              current_time = bstack11l1l1ll_opy_.strftime(bstack1ll11_opy_ (u"ࠣࠧ࡜࠱ࠪࡳ࠭ࠦࡦࡗࠩࡍࡀࠥࡎ࠼ࠨࡗ࠳ࠫࡦࠡࡗࡗࡇࠧਘ"))
              test_id = os.environ.get(bstack1ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧਙ")) if os.environ.get(bstack1ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨਚ")) else global_config.get_property(bstack1ll11_opy_ (u"ࠦࡸࡪ࡫ࡓࡷࡱࡍࡩࠨਛ"))
              payload = {
                  bstack1ll11_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠤਜ"): bstack1ll11_opy_ (u"ࠨࡳࡥ࡭ࡢࡩࡻ࡫࡮ࡵࡵࠥਝ"),
                  bstack1ll11_opy_ (u"ࠢࡥࡣࡷࡥࠧਞ"): {
                      bstack1ll11_opy_ (u"ࠣࡶࡨࡷࡹ࡮ࡵࡣࡡࡸࡹ࡮ࡪࠢਟ"): test_id,
                      bstack1ll11_opy_ (u"ࠤࡦࡶࡪࡧࡴࡦࡦࡢࡨࡦࡿࠢਠ"): current_time,
                      bstack1ll11_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡱࡥࡲ࡫ࠢਡ"): bstack1ll11_opy_ (u"ࠦࡘࡊࡋࡇࡧࡤࡸࡺࡸࡥࡑࡧࡵࡪࡴࡸ࡭ࡢࡰࡦࡩࠧਢ"),
                      bstack1ll11_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣ࡯ࡹ࡯࡯ࠤਣ"): {
                          bstack1ll11_opy_ (u"ࠨ࡭ࡦࡣࡶࡹࡷ࡫ࡳࠣਤ"): data,
                          bstack1ll11_opy_ (u"ࠢࡴࡦ࡮ࡖࡺࡴࡉࡥࠤਥ"): global_config.get_property(bstack1ll11_opy_ (u"ࠣࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠥਦ"))
                      },
                      bstack1ll11_opy_ (u"ࠤࡸࡷࡪࡸ࡟ࡥࡣࡷࡥࠧਧ"): global_config.get_property(bstack1ll11_opy_ (u"ࠥࡹࡸ࡫ࡲࡏࡣࡰࡩࠧਨ")),
                      bstack1ll11_opy_ (u"ࠦ࡭ࡵࡳࡵࡡ࡬ࡲ࡫ࡵࠢ਩"): get_host_info()
                  }
              }
              bstack1l1111ll1l_opy_ = bstack1l11llll11_opy_(cli.config, [bstack1ll11_opy_ (u"ࠧࡧࡰࡪࡵࠥਪ"), bstack1ll11_opy_ (u"ࠨࡥࡥࡵࡌࡲࡸࡺࡲࡶ࡯ࡨࡲࡹࡧࡴࡪࡱࡱࠦਫ"), bstack1ll11_opy_ (u"ࠢࡢࡲ࡬ࠦਬ")], bstack1lll1ll1ll_opy_)
              response = bstack1ll11l111l_opy_(bstack1ll11_opy_ (u"ࠣࡒࡒࡗ࡙ࠨਭ"), bstack1l1111ll1l_opy_, payload, config)
              if response.status_code >= 200 and response.status_code < 300:
                  logger.info(bstack1ll11_opy_ (u"ࠤࡎࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹࠠࡴࡧࡱࡸࠥࡹࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡹࡵࠠࡼࡿࠥਮ").format(bstack1lll1ll1ll_opy_))
              else:
                  logger.debug(bstack1ll11_opy_ (u"ࠥࡏࡪࡿࠠ࡮ࡧࡷࡶ࡮ࡩࡳࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮ࠠࡴࡶࡤࡸࡺࡹࠠࡼࡿࠥਯ").format(response.status_code))
          except Exception as e:
              logger.debug(bstack1ll11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡱࡨࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵ࠽ࠤࢀࢃࠢਰ").format(e))
      bstack11l1111lll_opy_()
  except Exception as e:
      logger.debug(bstack1ll11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡱࡨࡤࡱࡥࡺࡡࡰࡩࡹࡸࡩࡤࡵ࠽ࠤࢀࢃࠢ਱").format(e))
def bstack11llllll1_opy_(bstack111111ll1_opy_=False):
  bstack1l11111lll_opy_ = bstack1ll11_opy_ (u"ࠨࠢਲ")
  global bstack111ll111_opy_
  global bstack11l1ll1l11_opy_
  global bstack1l1ll111ll_opy_
  global bstack1l111l111l_opy_
  global ROBOT_PYTHON_ERRORS
  global bstack11111l1ll1_opy_
  global CONFIG
  bstack11lll11ll1_opy_ = os.environ.get(bstack1ll11_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨਲ਼"))
  if bstack11lll11ll1_opy_ not in [bstack1ll11_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ਴")]:
    bstack1l11111lll_opy_ = bstack11ll11l1ll_opy_.bstack11l11l111_opy_(EVENTS.bstack1l1lllll_opy_)
  percy.shutdown()
  if bstack111ll111_opy_:
    logger.warning(bstack11l11l1111_opy_.format(str(bstack111ll111_opy_)))
  else:
    try:
      bstack1l1l1lll_opy_ = bstack11lll1llll_opy_(bstack1ll11_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨਵ"), logger)
      if bstack1l1l1lll_opy_.get(bstack1ll11_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨਸ਼")) and bstack1l1l1lll_opy_.get(bstack1ll11_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩ਷")).get(bstack1ll11_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧਸ")):
        logger.warning(bstack11l11l1111_opy_.format(str(bstack1l1l1lll_opy_[bstack1ll11_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫਹ")][bstack1ll11_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩ਺")])))
    except Exception as e:
      logger.error(e)
  if cli.is_running() and bstack11lll11ll1_opy_ not in [bstack1ll11_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ਻")]:
    if _11111ll11_opy_ is not None:
      bstack111111ll1_opy_ = _11111ll11_opy_
    else:
      bstack111111ll1_opy_ = cli.is_running()
    bstack1lll111l_opy_.invoke(Events.bstack11lll1l11l_opy_)
  elif _11111ll11_opy_ is not None:
    bstack111111ll1_opy_ = _11111ll11_opy_
  logger.info(bstack1ll111lll_opy_)
  global bstack1ll11ll11_opy_
  if bstack1ll11ll11_opy_:
    bstack11ll1l1l1l_opy_()
  try:
    with bstack1llll1l1l_opy_:
      bstack1l1ll11111_opy_ = bstack11l1ll1l11_opy_.copy()
    for driver in bstack1l1ll11111_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1ll1l1l1ll_opy_)
  ROBOT_PYTHON_ERRORS = []
  if bstack11111l1ll1_opy_ == bstack1ll11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ਼"):
    ROBOT_PYTHON_ERRORS = bstack111l111l1_opy_(bstack1ll11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫ਽"))
  if bstack11111l1ll1_opy_ == bstack1ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫਾ") and len(bstack1l111l111l_opy_) == 0:
    bstack1l111l111l_opy_ = bstack111l111l1_opy_(bstack1ll11_opy_ (u"ࠬࡶࡷࡠࡲࡼࡸࡪࡹࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪਿ"))
    if len(bstack1l111l111l_opy_) == 0:
      bstack1l111l111l_opy_ = bstack111l111l1_opy_(bstack1ll11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡰࡱࡲࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬੀ"))
  bstack11llll1l11_opy_ = bstack1ll11_opy_ (u"ࠧࠨੁ")
  if len(bstack1l1ll111ll_opy_) > 0:
    bstack11llll1l11_opy_ = bstack1l1l1111ll_opy_(bstack1l1ll111ll_opy_)
  elif len(bstack1l111l111l_opy_) > 0:
    bstack11llll1l11_opy_ = bstack1l1l1111ll_opy_(bstack1l111l111l_opy_)
  elif len(ROBOT_PYTHON_ERRORS) > 0:
    bstack11llll1l11_opy_ = bstack1l1l1111ll_opy_(ROBOT_PYTHON_ERRORS)
  elif len(bstack1llllllllll_opy_) > 0:
    bstack11llll1l11_opy_ = bstack1l1l1111ll_opy_(bstack1llllllllll_opy_)
  if bstack11lll11ll1_opy_ not in [bstack1ll11_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩੂ")]:
    def bstack11l1llll_opy_():
      try:
        if bstack11lll11ll1_opy_ in [bstack1ll11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ੃"), bstack1ll11_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ੄")]:
          bstack1111ll111l_opy_()
      except Exception as e:
        logger.debug(bstack1ll11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡪࡰࡤࡰࡤ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧ੅").format(e))
    def bstack1l111111ll_opy_():
      try:
        if bool(bstack11llll1l11_opy_):
          bstack1l11ll1111_opy_(bstack11llll1l11_opy_, bstack111111ll1_opy_=bstack111111ll1_opy_)
        else:
          bstack1l11ll1111_opy_(bstack111111ll1_opy_=bstack111111ll1_opy_)
      except Exception as e:
        logger.debug(bstack1ll11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥ࡫ࡶࡦࡰࡷ࠾ࠥࢁࡽࠣ੆").format(e))
    def bstack1ll111l1ll_opy_():
      try:
        logger_utils.bstack11111lll1l_opy_(CONFIG)
      except Exception as e:
        logger.debug(bstack1ll11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡹࡥ࡯ࡦ࡬ࡲ࡬ࠦ࡬ࡰࡩࡶ࠾ࠥࢁࡽࠣੇ").format(e))
    bstack1l1l1l11l1_opy_ = threading.Thread(target=bstack11l1llll_opy_)
    bstack111l1l11l1_opy_ = threading.Thread(target=bstack1l111111ll_opy_)
    bstack1l1lllll1_opy_ = threading.Thread(target=bstack1ll111l1ll_opy_)
    threads = [bstack1l1l1l11l1_opy_, bstack111l1l11l1_opy_, bstack1l1lllll1_opy_]
    for thread in threads:
      try:
        thread.start()
      except Exception as e:
        logger.debug(bstack1ll11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡳࡵࡣࡵࡸ࡮ࡴࡧࠡࡶ࡫ࡶࡪࡧࡤࠡࡽࢀ࠾ࠥࢁࡽࠣੈ").format(thread.name, e))
    for thread in threads:
      try:
        thread.join()
      except Exception as e:
        logger.debug(bstack1ll11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠ࡫ࡱ࡬ࡲ࡮ࡴࡧࠡࡶ࡫ࡶࡪࡧࡤࠡࡽࢀ࠾ࠥࢁࡽࠣ੉").format(thread.name, e))
    bstack11ll11llll_opy_(bstack1l111l11_opy_, logger)
    bstack11ll11llll_opy_(os.path.join(os.getcwd(), bstack1ll11_opy_ (u"ࠩ࡯ࡳ࡬࠭੊"), bstack1ll11_opy_ (u"ࠪ࡯ࡪࡿ࠭࡮ࡧࡷࡶ࡮ࡩࡳ࠯࡬ࡶࡳࡳ࠭ੋ")), logger)
  if bstack11lll11ll1_opy_ not in [bstack1ll11_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬੌ")]:
    bstack11ll11l1ll_opy_.end(EVENTS.bstack1l1lllll_opy_.value, bstack1l11111lll_opy_ + bstack1ll11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸ੍ࠧ"), bstack1l11111lll_opy_ + bstack1ll11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ੎"), status=True, failure=None, test_name=None)
    bstack11llll1ll1_opy_()
    logger_utils.bstack1ll11ll1l1_opy_()
    logging.shutdown()
  if len(ROBOT_PYTHON_ERRORS) > 0:
    sys.exit(len(ROBOT_PYTHON_ERRORS))
def bstack1l111l11ll_opy_(bstack11ll1ll1_opy_, frame):
  global global_config
  logger.error(bstack1l11lllll1_opy_)
  global_config.bstack1ll11l111_opy_(bstack1ll11_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡏࡱࠪ੏"), bstack11ll1ll1_opy_)
  if hasattr(signal, bstack1ll11_opy_ (u"ࠨࡕ࡬࡫ࡳࡧ࡬ࡴࠩ੐")):
    global_config.bstack1ll11l111_opy_(bstack1ll11_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩੑ"), signal.Signals(bstack11ll1ll1_opy_).name)
  else:
    global_config.bstack1ll11l111_opy_(bstack1ll11_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪ੒"), bstack1ll11_opy_ (u"ࠫࡘࡏࡇࡖࡐࡎࡒࡔ࡝ࡎࠨ੓"))
  bstack111111ll1_opy_ = cli.is_running()
  if bstack111111ll1_opy_:
    bstack1lll111l_opy_.invoke(Events.bstack11lll1l11l_opy_)
  bstack11lll11ll1_opy_ = os.environ.get(bstack1ll11_opy_ (u"ࠬࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉ࠭੔"))
  if bstack11lll11ll1_opy_ == bstack1ll11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭੕") and not cli.is_enabled(CONFIG):
    TestHubHandler.stop(global_config.get_property(bstack1ll11_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡔ࡫ࡪࡲࡦࡲࠧ੖")))
  bstack11llllll1_opy_(bstack111111ll1_opy_)
  sys.exit(1)
def bstack11l1l111l1_opy_(err):
  logger.critical(bstack11l1lll11_opy_.format(str(err)))
  bstack1l11ll1111_opy_(bstack11l1lll11_opy_.format(str(err)), True)
  atexit.unregister(bstack11llllll1_opy_)
  bstack1111ll111l_opy_()
  sys.exit(1)
def bstack1ll1ll1l11_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1l11ll1111_opy_(message, True)
  atexit.unregister(bstack11llllll1_opy_)
  bstack1111ll111l_opy_()
  sys.exit(1)
def bstack11l11ll111_opy_():
  global CONFIG
  global bstack111l11111_opy_
  global bstack11llll1l_opy_
  global BROWSERSTACK_AUTOMATION
  CONFIG = bstack1l1l111111_opy_()
  load_dotenv(CONFIG.get(bstack1ll11_opy_ (u"ࠨࡧࡱࡺࡋ࡯࡬ࡦࠩ੗")))
  bstack111lll11ll_opy_()
  bstack11l111l11l_opy_()
  CONFIG = bstack111ll1lll_opy_(CONFIG)
  update(CONFIG, bstack11llll1l_opy_)
  update(CONFIG, bstack111l11111_opy_)
  if not cli.is_enabled(CONFIG):
    CONFIG = bstack1ll11lll1_opy_(CONFIG)
  BROWSERSTACK_AUTOMATION = bstack1ll11l1l11_opy_(CONFIG)
  os.environ[bstack1ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬ੘")] = BROWSERSTACK_AUTOMATION.__str__().lower()
  global_config.bstack1ll11l111_opy_(bstack1ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫਖ਼"), BROWSERSTACK_AUTOMATION)
  if (bstack1ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧਗ਼") in CONFIG and bstack1ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨਜ਼") in bstack111l11111_opy_) or (
          bstack1ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩੜ") in CONFIG and bstack1ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ੝") not in bstack11llll1l_opy_):
    if os.getenv(bstack1ll11_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬਫ਼")):
      CONFIG[bstack1ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ੟")] = os.getenv(bstack1ll11_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧ੠"))
    else:
      if not CONFIG.get(bstack1ll11_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠢ੡"), bstack1ll11_opy_ (u"ࠧࠨ੢")) in bstack11l111ll11_opy_:
        bstack1l111ll1l_opy_()
  elif (bstack1ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ੣") not in CONFIG and bstack1ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ੤") in CONFIG) or (
          bstack1ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ੥") in bstack11llll1l_opy_ and bstack1ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ੦") not in bstack111l11111_opy_):
    del (CONFIG[bstack1ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ੧")])
  if bstack11ll1111_opy_(CONFIG):
    bstack11l1l111l1_opy_(bstack1l1llll11_opy_)
  Config.get_instance().bstack1ll11l111_opy_(bstack1ll11_opy_ (u"ࠦࡺࡹࡥࡳࡐࡤࡱࡪࠨ੨"), CONFIG[bstack1ll11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ੩")])
  bstack1lll1l1lll_opy_()
  bstack1l11l1ll1l_opy_()
  if bstack1l11lll111_opy_ and not CONFIG.get(bstack1ll11_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠤ੪"), bstack1ll11_opy_ (u"ࠢࠣ੫")) in bstack11l111ll11_opy_:
    CONFIG[bstack1ll11_opy_ (u"ࠨࡣࡳࡴࠬ੬")] = bstack11l1llll1_opy_(CONFIG)
    logger.info(bstack111llllll_opy_.format(CONFIG[bstack1ll11_opy_ (u"ࠩࡤࡴࡵ࠭੭")]))
  if not BROWSERSTACK_AUTOMATION:
    CONFIG[bstack1ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭੮")] = [{}]
def bstack111111l1l_opy_(config, bstack1l11l11l11_opy_):
  global CONFIG
  global bstack1l11lll111_opy_
  CONFIG = config
  bstack1l11lll111_opy_ = bstack1l11l11l11_opy_
def bstack1l11l1ll1l_opy_():
  global CONFIG
  global bstack1l11lll111_opy_
  if bstack1ll11_opy_ (u"ࠫࡦࡶࡰࠨ੯") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1ll1ll1l11_opy_(e, bstack11111111l1_opy_)
    bstack1l11lll111_opy_ = True
    global_config.bstack1ll11l111_opy_(bstack1ll11_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫੰ"), True)
def bstack11l1llll1_opy_(config):
  bstack1l11l11l1l_opy_ = bstack1ll11_opy_ (u"࠭ࠧੱ")
  app = config[bstack1ll11_opy_ (u"ࠧࡢࡲࡳࠫੲ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack11111l111l_opy_:
      if os.path.exists(app):
        bstack1l11l11l1l_opy_ = bstack111ll11lll_opy_(config, app)
      elif bstack111l1l1111_opy_(app):
        bstack1l11l11l1l_opy_ = app
      else:
        bstack11l1l111l1_opy_(bstack1ll1llll1_opy_.format(app))
    else:
      if bstack111l1l1111_opy_(app):
        bstack1l11l11l1l_opy_ = app
      elif os.path.exists(app):
        bstack1l11l11l1l_opy_ = bstack111ll11lll_opy_(app)
      else:
        bstack11l1l111l1_opy_(bstack1lll1llll_opy_)
  else:
    if len(app) > 2:
      bstack11l1l111l1_opy_(bstack11lll1l1ll_opy_)
    elif len(app) == 2:
      if bstack1ll11_opy_ (u"ࠨࡲࡤࡸ࡭࠭ੳ") in app and bstack1ll11_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬੴ") in app:
        if os.path.exists(app[bstack1ll11_opy_ (u"ࠪࡴࡦࡺࡨࠨੵ")]):
          bstack1l11l11l1l_opy_ = bstack111ll11lll_opy_(config, app[bstack1ll11_opy_ (u"ࠫࡵࡧࡴࡩࠩ੶")], app[bstack1ll11_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨ੷")])
        else:
          bstack11l1l111l1_opy_(bstack1ll1llll1_opy_.format(app))
      else:
        bstack11l1l111l1_opy_(bstack11lll1l1ll_opy_)
    else:
      for key in app:
        if key in bstack11l111l1_opy_:
          if key == bstack1ll11_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ੸"):
            if os.path.exists(app[key]):
              bstack1l11l11l1l_opy_ = bstack111ll11lll_opy_(config, app[key])
            else:
              bstack11l1l111l1_opy_(bstack1ll1llll1_opy_.format(app))
          else:
            bstack1l11l11l1l_opy_ = app[key]
        else:
          bstack11l1l111l1_opy_(bstack1l1l1ll1ll_opy_)
  return bstack1l11l11l1l_opy_
def bstack111l1l1111_opy_(bstack1l11l11l1l_opy_):
  import re
  bstack11lll111ll_opy_ = re.compile(bstack1ll11_opy_ (u"ࡲࠣࡠ࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯ࠪࠢ੹"))
  bstack1l1ll1l1ll_opy_ = re.compile(bstack1ll11_opy_ (u"ࡳࠤࡡ࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰࠯࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭ࠨࠧ੺"))
  if bstack1ll11_opy_ (u"ࠩࡥࡷ࠿࠵࠯ࠨ੻") in bstack1l11l11l1l_opy_ or re.fullmatch(bstack11lll111ll_opy_, bstack1l11l11l1l_opy_) or re.fullmatch(bstack1l1ll1l1ll_opy_, bstack1l11l11l1l_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack1lllll11ll_opy_, stage=STAGE.bstack11111llll_opy_, bstack11lll1l111_opy_=SESSION_NAME)
def bstack111ll11lll_opy_(config, path, bstack1l1ll1ll11_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1ll11_opy_ (u"ࠪࡶࡧ࠭੼")).read()).hexdigest()
  bstack11l111l1l1_opy_ = bstack1l1lll11l1_opy_(md5_hash)
  bstack1l11l11l1l_opy_ = None
  if bstack11l111l1l1_opy_:
    logger.info(bstack11111111l_opy_.format(bstack11l111l1l1_opy_, md5_hash))
    return bstack11l111l1l1_opy_
  bstack11l111ll1_opy_ = datetime.datetime.now()
  multipart_data = MultipartEncoder(
    fields={
      bstack1ll11_opy_ (u"ࠫ࡫࡯࡬ࡦࠩ੽"): (os.path.basename(path), open(os.path.abspath(path), bstack1ll11_opy_ (u"ࠬࡸࡢࠨ੾")), bstack1ll11_opy_ (u"࠭ࡴࡦࡺࡷ࠳ࡵࡲࡡࡪࡰࠪ੿")),
      bstack1ll11_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪ઀"): bstack1l1ll1ll11_opy_
    }
  )
  response = requests.post(bstack1l11l1111l_opy_, data=multipart_data,
                           headers={bstack1ll11_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧઁ"): multipart_data.content_type},
                           auth=(config[bstack1ll11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫં")], config[bstack1ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ઃ")]))
  try:
    res = json.loads(response.text)
    bstack1l11l11l1l_opy_ = res[bstack1ll11_opy_ (u"ࠫࡦࡶࡰࡠࡷࡵࡰࠬ઄")]
    logger.info(bstack1111lll1l1_opy_.format(bstack1l11l11l1l_opy_))
    bstack1llll111_opy_(md5_hash, bstack1l11l11l1l_opy_)
    cli.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽ࡹࡵࡲ࡯ࡢࡦࡢࡥࡵࡶࠢઅ"), datetime.datetime.now() - bstack11l111ll1_opy_)
  except ValueError as err:
    bstack11l1l111l1_opy_(bstack11llll111l_opy_.format(str(err)))
  return bstack1l11l11l1l_opy_
def bstack1lll1l1lll_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack11l1llll11_opy_
  bstack111ll1l111_opy_ = 1
  bstack1lllll1l11_opy_ = 1
  if bstack1ll11_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭આ") in CONFIG:
    bstack1lllll1l11_opy_ = CONFIG[bstack1ll11_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧઇ")]
  else:
    bstack1lllll1l11_opy_ = bstack1l1111ll1_opy_(framework_name, args) or 1
  if bstack1ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫઈ") in CONFIG:
    bstack111ll1l111_opy_ = len(CONFIG[bstack1ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬઉ")])
  bstack11l1llll11_opy_ = int(bstack1lllll1l11_opy_) * int(bstack111ll1l111_opy_)
def bstack1l1111ll1_opy_(framework_name, args):
  if framework_name == bstack1l1l11l1l1_opy_ and args and bstack1ll11_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨઊ") in args:
      bstack1111ll1111_opy_ = args.index(bstack1ll11_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩઋ"))
      return int(args[bstack1111ll1111_opy_ + 1]) or 1
  return 1
def bstack1l1lll11l1_opy_(md5_hash):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1ll11_opy_ (u"ࠬ࡬ࡩ࡭ࡧ࡯ࡳࡨࡱࠠ࡯ࡱࡷࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠬࠡࡷࡶ࡭ࡳ࡭ࠠࡣࡣࡶ࡭ࡨࠦࡦࡪ࡮ࡨࠤࡴࡶࡥࡳࡣࡷ࡭ࡴࡴࡳࠨઌ"))
    bstack111l1l1l1_opy_ = os.path.join(os.path.expanduser(bstack1ll11_opy_ (u"࠭ࡾࠨઍ")), bstack1ll11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ઎"), bstack1ll11_opy_ (u"ࠨࡣࡳࡴ࡚ࡶ࡬ࡰࡣࡧࡑࡉ࠻ࡈࡢࡵ࡫࠲࡯ࡹ࡯࡯ࠩએ"))
    if os.path.exists(bstack111l1l1l1_opy_):
      try:
        bstack1l1l1l111_opy_ = json.load(open(bstack111l1l1l1_opy_, bstack1ll11_opy_ (u"ࠩࡵࡦࠬઐ")))
        if md5_hash in bstack1l1l1l111_opy_:
          bstack1l1ll1l11_opy_ = bstack1l1l1l111_opy_[md5_hash]
          bstack1ll11lll_opy_ = datetime.datetime.now()
          bstack11ll1111ll_opy_ = datetime.datetime.strptime(bstack1l1ll1l11_opy_[bstack1ll11_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ઑ")], bstack1ll11_opy_ (u"ࠫࠪࡪ࠯ࠦ࡯࠲ࠩ࡞ࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨ઒"))
          if (bstack1ll11lll_opy_ - bstack11ll1111ll_opy_).days > 30:
            return None
          elif version.parse(str(__version__)) > version.parse(bstack1l1ll1l11_opy_[bstack1ll11_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪઓ")]):
            return None
          return bstack1l1ll1l11_opy_[bstack1ll11_opy_ (u"࠭ࡩࡥࠩઔ")]
      except Exception as e:
        logger.debug(bstack1ll11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡲࡦࡣࡧ࡭ࡳ࡭ࠠࡎࡆ࠸ࠤ࡭ࡧࡳࡩࠢࡩ࡭ࡱ࡫࠺ࠡࡽࢀࠫક").format(str(e)))
    return None
  bstack111l1l1l1_opy_ = os.path.join(os.path.expanduser(bstack1ll11_opy_ (u"ࠨࢀࠪખ")), bstack1ll11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩગ"), bstack1ll11_opy_ (u"ࠪࡥࡵࡶࡕࡱ࡮ࡲࡥࡩࡓࡄ࠶ࡊࡤࡷ࡭࠴ࡪࡴࡱࡱࠫઘ"))
  lock_file = bstack111l1l1l1_opy_ + bstack1ll11_opy_ (u"ࠫ࠳ࡲ࡯ࡤ࡭ࠪઙ")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack111l1l1l1_opy_):
        with open(bstack111l1l1l1_opy_, bstack1ll11_opy_ (u"ࠬࡸࠧચ")) as f:
          content = f.read().strip()
          if content:
            bstack1l1l1l111_opy_ = json.loads(content)
            if md5_hash in bstack1l1l1l111_opy_:
              bstack1l1ll1l11_opy_ = bstack1l1l1l111_opy_[md5_hash]
              bstack1ll11lll_opy_ = datetime.datetime.now()
              bstack11ll1111ll_opy_ = datetime.datetime.strptime(bstack1l1ll1l11_opy_[bstack1ll11_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩછ")], bstack1ll11_opy_ (u"ࠧࠦࡦ࠲ࠩࡲ࠵࡚ࠥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫજ"))
              if (bstack1ll11lll_opy_ - bstack11ll1111ll_opy_).days > 30:
                return None
              elif version.parse(str(__version__)) > version.parse(bstack1l1ll1l11_opy_[bstack1ll11_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ઝ")]):
                return None
              return bstack1l1ll1l11_opy_[bstack1ll11_opy_ (u"ࠩ࡬ࡨࠬઞ")]
      return None
  except Exception as e:
    logger.debug(bstack1ll11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡺ࡭ࡹ࡮ࠠࡧ࡫࡯ࡩࠥࡲ࡯ࡤ࡭࡬ࡲ࡬ࠦࡦࡰࡴࠣࡑࡉ࠻ࠠࡩࡣࡶ࡬࠿ࠦࡻࡾࠩટ").format(str(e)))
    return None
def bstack1llll111_opy_(md5_hash, bstack1l11l11l1l_opy_):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1ll11_opy_ (u"ࠫ࡫࡯࡬ࡦ࡮ࡲࡧࡰࠦ࡮ࡰࡶࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪ࠲ࠠࡶࡵ࡬ࡲ࡬ࠦࡢࡢࡵ࡬ࡧࠥ࡬ࡩ࡭ࡧࠣࡳࡵ࡫ࡲࡢࡶ࡬ࡳࡳࡹࠧઠ"))
    bstack1lll111l11_opy_ = os.path.join(os.path.expanduser(bstack1ll11_opy_ (u"ࠬࢄࠧડ")), bstack1ll11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ઢ"))
    if not os.path.exists(bstack1lll111l11_opy_):
      os.makedirs(bstack1lll111l11_opy_)
    bstack111l1l1l1_opy_ = os.path.join(os.path.expanduser(bstack1ll11_opy_ (u"ࠧࡿࠩણ")), bstack1ll11_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨત"), bstack1ll11_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪથ"))
    bstack1l1l1l1111_opy_ = {
      bstack1ll11_opy_ (u"ࠪ࡭ࡩ࠭દ"): bstack1l11l11l1l_opy_,
      bstack1ll11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧધ"): datetime.datetime.strftime(datetime.datetime.now(), bstack1ll11_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩન")),
      bstack1ll11_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ઩"): str(__version__)
    }
    try:
      bstack1l1l1l111_opy_ = {}
      if os.path.exists(bstack111l1l1l1_opy_):
        bstack1l1l1l111_opy_ = json.load(open(bstack111l1l1l1_opy_, bstack1ll11_opy_ (u"ࠧࡳࡤࠪપ")))
      bstack1l1l1l111_opy_[md5_hash] = bstack1l1l1l1111_opy_
      with open(bstack111l1l1l1_opy_, bstack1ll11_opy_ (u"ࠣࡹ࠮ࠦફ")) as outfile:
        json.dump(bstack1l1l1l111_opy_, outfile)
    except Exception as e:
      logger.debug(bstack1ll11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡷࡳࡨࡦࡺࡩ࡯ࡩࠣࡑࡉ࠻ࠠࡩࡣࡶ࡬ࠥ࡬ࡩ࡭ࡧ࠽ࠤࢀࢃࠧબ").format(str(e)))
    return
  bstack1lll111l11_opy_ = os.path.join(os.path.expanduser(bstack1ll11_opy_ (u"ࠪࢂࠬભ")), bstack1ll11_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫમ"))
  if not os.path.exists(bstack1lll111l11_opy_):
    os.makedirs(bstack1lll111l11_opy_)
  bstack111l1l1l1_opy_ = os.path.join(os.path.expanduser(bstack1ll11_opy_ (u"ࠬࢄࠧય")), bstack1ll11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ર"), bstack1ll11_opy_ (u"ࠧࡢࡲࡳ࡙ࡵࡲ࡯ࡢࡦࡐࡈ࠺ࡎࡡࡴࡪ࠱࡮ࡸࡵ࡮ࠨ઱"))
  lock_file = bstack111l1l1l1_opy_ + bstack1ll11_opy_ (u"ࠨ࠰࡯ࡳࡨࡱࠧલ")
  bstack1l1l1l1111_opy_ = {
    bstack1ll11_opy_ (u"ࠩ࡬ࡨࠬળ"): bstack1l11l11l1l_opy_,
    bstack1ll11_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭઴"): datetime.datetime.strftime(datetime.datetime.now(), bstack1ll11_opy_ (u"ࠫࠪࡪ࠯ࠦ࡯࠲ࠩ࡞ࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨવ")),
    bstack1ll11_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪશ"): str(__version__)
  }
  try:
    with FileLock(lock_file, timeout=10):
      bstack1l1l1l111_opy_ = {}
      if os.path.exists(bstack111l1l1l1_opy_):
        with open(bstack111l1l1l1_opy_, bstack1ll11_opy_ (u"࠭ࡲࠨષ")) as f:
          content = f.read().strip()
          if content:
            bstack1l1l1l111_opy_ = json.loads(content)
      bstack1l1l1l111_opy_[md5_hash] = bstack1l1l1l1111_opy_
      with open(bstack111l1l1l1_opy_, bstack1ll11_opy_ (u"ࠢࡸࠤસ")) as outfile:
        json.dump(bstack1l1l1l111_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1ll11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡸ࡫ࡷ࡬ࠥ࡬ࡩ࡭ࡧࠣࡰࡴࡩ࡫ࡪࡰࡪࠤ࡫ࡵࡲࠡࡏࡇ࠹ࠥ࡮ࡡࡴࡪࠣࡹࡵࡪࡡࡵࡧ࠽ࠤࢀࢃࠧહ").format(str(e)))
def bstack11ll1l11ll_opy_(self):
  return
def bstack1111ll111_opy_(self):
  return
def bstack1111l1ll1_opy_():
  global bstack11ll11l1l_opy_
  bstack11ll11l1l_opy_ = True
def bstack1llllll11_opy_(self):
  global FRAMEWORK_NAME
  global bstack1ll1l11l_opy_
  global bstack1ll1111l1_opy_
  bstack1l11ll1ll1_opy_ = bstack11ll11l1ll_opy_.bstack11l11l111_opy_(EVENTS.bstack111ll1l1l_opy_)
  try:
    if bstack1ll11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ઺") in FRAMEWORK_NAME and self.session_id != None and bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧ઻"), bstack1ll11_opy_ (u"઼ࠫࠬ")) != bstack1ll11_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ઽ"):
      bstack1l1ll11l1l_opy_ = bstack1ll11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ા") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1ll11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧિ")
      if bstack1l1ll11l1l_opy_ == bstack1ll11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨી"):
        bstack1ll111ll1_opy_(logger)
      if self != None:
        bstack11l11l111l_opy_(self, bstack1l1ll11l1l_opy_, bstack1ll11_opy_ (u"ࠩ࠯ࠤࠬુ").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack1ll11_opy_ (u"ࠪࠫૂ")
    if bstack1ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫૃ") in FRAMEWORK_NAME and getattr(threading.current_thread(), bstack1ll11_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫૄ"), None):
      bstack1lll1l111l_opy_.bstack1ll111ll_opy_(self, bstack1l11l1llll_opy_, logger, wait=True)
    if bstack1ll11_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ૅ") in FRAMEWORK_NAME:
      bstack1l1l1111l_opy_.bstack11l1l1l1ll_opy_(self)
    bstack11ll11l1ll_opy_.end(EVENTS.bstack111ll1l1l_opy_.value, bstack1l11ll1ll1_opy_ + bstack1ll11_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ૆"), bstack1l11ll1ll1_opy_ + bstack1ll11_opy_ (u"ࠣ࠼ࡨࡲࡩࠨે"), status=True, failure=None, test_name=None)
  except Exception as e:
    logger.debug(bstack1ll11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࠥૈ") + str(e))
    bstack11ll11l1ll_opy_.end(EVENTS.bstack111ll1l1l_opy_.value, bstack1l11ll1ll1_opy_ + bstack1ll11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥૉ"), bstack1l11ll1ll1_opy_ + bstack1ll11_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ૊"), status=False, failure=str(e), test_name=None)
  bstack1ll1111l1_opy_(self)
  self.session_id = None
def bstack111l111lll_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack1lll1l11_opy_
    global FRAMEWORK_NAME
    command_executor = kwargs.get(bstack1ll11_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠨો"), bstack1ll11_opy_ (u"࠭ࠧૌ"))
    bstack1llll111ll_opy_ = False
    if type(command_executor) == str and bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯્ࠪ") in command_executor:
      bstack1llll111ll_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫ૎") in str(getattr(command_executor, bstack1ll11_opy_ (u"ࠩࡢࡹࡷࡲࠧ૏"), bstack1ll11_opy_ (u"ࠪࠫૐ"))):
      bstack1llll111ll_opy_ = True
    else:
      kwargs = a11y.bstack1l1ll1l111_opy_(bstack1l1lll1l1_opy_=kwargs, config=CONFIG)
      return bstack1llllllll1_opy_(self, *args, **kwargs)
    if bstack1llll111ll_opy_:
      bstack1ll1lll11_opy_ = TestHubUtils.bstack11ll1l111_opy_(CONFIG, FRAMEWORK_NAME)
      if kwargs.get(bstack1ll11_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ૑")):
        kwargs[bstack1ll11_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭૒")] = bstack1lll1l11_opy_(kwargs[bstack1ll11_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧ૓")], FRAMEWORK_NAME, CONFIG, bstack1ll1lll11_opy_)
      elif kwargs.get(bstack1ll11_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ૔")):
        kwargs[bstack1ll11_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ૕")] = bstack1lll1l11_opy_(kwargs[bstack1ll11_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ૖")], FRAMEWORK_NAME, CONFIG, bstack1ll1lll11_opy_)
  except Exception as e:
    logger.error(bstack1ll11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡘࡊࡋࠡࡥࡤࡴࡸࡀࠠࡼࡿࠥ૗").format(str(e)))
  return bstack1llllllll1_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack1ll11llll_opy_, stage=STAGE.bstack11111llll_opy_, bstack11lll1l111_opy_=SESSION_NAME)
def bstack1l1l1l1l1l_opy_(self, command_executor=bstack1ll11_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳࠶࠸࠷࠯࠲࠱࠴࠳࠷࠺࠵࠶࠷࠸ࠧ૘"), *args, **kwargs):
  global bstack1ll1l11l_opy_
  global bstack11l1ll1l11_opy_
  bstack11l1ll11l_opy_ = bstack111l111lll_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack11l11l1lll_opy_.on():
    return bstack11l1ll11l_opy_
  try:
    if isinstance(command_executor, (str, bytes)):
      bstack11lll1l1l_opy_ = str(command_executor)
    else:
      bstack11lll1l1l_opy_ = str(
        getattr(command_executor, bstack1ll11_opy_ (u"ࠬࡥࡵࡳ࡮ࠪ૙"), None)
        or getattr(getattr(command_executor, bstack1ll11_opy_ (u"࠭࡟ࡤ࡮࡬ࡩࡳࡺ࡟ࡤࡱࡱࡪ࡮࡭ࠧ૚"), None), bstack1ll11_opy_ (u"ࠧࡳࡧࡰࡳࡹ࡫࡟ࡴࡧࡵࡺࡪࡸ࡟ࡢࡦࡧࡶࠬ૛"), None)
        or bstack1ll11_opy_ (u"ࠨࠩ૜")
      )
    logger.debug(bstack1ll11_opy_ (u"ࠩࡋࡹࡧࠦࡕࡓࡎࠣ࡭ࡸࠦ࠭ࠡࡽࢀࠫ૝").format(bstack11lll1l1l_opy_.split(bstack1ll11_opy_ (u"ࠪࡄࠬ૞"))[-1] if bstack1ll11_opy_ (u"ࠫࡅ࠭૟") in bstack11lll1l1l_opy_ else bstack11lll1l1l_opy_))
    if bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨૠ") in bstack11lll1l1l_opy_:
      global_config.bstack1ll11l111_opy_(bstack1ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧૡ"), True)
  except Exception as e:
    logger.error(bstack1ll11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡩࡨࡦࡥ࡮࡭ࡳ࡭ࠠࡤࡱࡰࡱࡦࡴࡤࠡࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧૢ").format(str(e)))
    pass
  if (isinstance(command_executor, str) and bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫૣ") in command_executor):
    global_config.bstack1ll11l111_opy_(bstack1ll11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪ૤"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack11l1ll111_opy_ = getattr(threading.current_thread(), bstack1ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡗࡩࡸࡺࡍࡦࡶࡤࠫ૥"), None)
  bstack11l1111ll1_opy_ = {}
  if self.capabilities is not None:
    bstack11l1111ll1_opy_[bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧࠪ૦")] = self.capabilities.get(bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ૧"))
    bstack11l1111ll1_opy_[bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ૨")] = self.capabilities.get(bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ૩"))
    bstack11l1111ll1_opy_[bstack1ll11_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡠࡱࡳࡸ࡮ࡵ࡮ࡴࠩ૪")] = self.capabilities.get(bstack1ll11_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ૫"))
  if CONFIG.get(bstack1ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ૬"), False) and a11y.bstack11ll111ll1_opy_(bstack11l1111ll1_opy_):
    threading.current_thread().a11yPlatform = True
  if bstack1ll11_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ૭") in FRAMEWORK_NAME or bstack1ll11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ૮") in FRAMEWORK_NAME:
    TestHubHandler.send_cbt_info(self)
  if bstack1ll11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭૯") in FRAMEWORK_NAME and bstack11l1ll111_opy_ and bstack11l1ll111_opy_.get(bstack1ll11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ૰"), bstack1ll11_opy_ (u"ࠨࠩ૱")) == bstack1ll11_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ૲"):
    TestHubHandler.send_cbt_info(self)
  bstack1ll1l11l_opy_ = self.session_id
  with bstack1llll1l1l_opy_:
    bstack11l1ll1l11_opy_.append(self)
  return bstack11l1ll11l_opy_
def bstack111l1ll1ll_opy_(args):
  return bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵࠫ૳") in str(args)
def bstack1ll1111l11_opy_(self, driver_command, *args, **kwargs):
  global bstack11l1lll1ll_opy_
  global bstack1l1l111l11_opy_
  bstack1llll11111_opy_ = bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ૴"), None) and bstack1l1111l111_opy_(
          threading.current_thread(), bstack1ll11_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ૵"), None)
  bstack111l1lll11_opy_ = bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭૶"), None) and bstack1l1111l111_opy_(
          threading.current_thread(), bstack1ll11_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ૷"), None)
  bstack1l1l1ll11_opy_ = getattr(self, bstack1ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ૸"), None) != None and getattr(self, bstack1ll11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩૹ"), None) == True
  if not bstack1l1l111l11_opy_ and bstack1ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪૺ") in CONFIG and CONFIG[bstack1ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫૻ")] == True and accessibility_scripts.bstack1lll11ll1_opy_(driver_command) and (bstack1l1l1ll11_opy_ or bstack1llll11111_opy_ or bstack111l1lll11_opy_) and not bstack111l1ll1ll_opy_(args):
    try:
      bstack1l1l111l11_opy_ = True
      logger.debug(bstack1ll11_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࢀࢃࠧૼ").format(driver_command))
      bstack1l1ll1l1l_opy_ = perform_scan(self, driver_command=driver_command)
      logger.debug(bstack1l1ll1l1l_opy_)
      try:
        log_data = {
          bstack1ll11_opy_ (u"ࠨࡲࡦࡳࡸࡩࡸࡺࠢ૽"): {
            bstack1ll11_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࠣ૾"): bstack1ll11_opy_ (u"ࠣࡃ࠴࠵࡞ࡥࡓࡄࡃࡑࠦ૿"),
            bstack1ll11_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡦࡶࡨࡶࡸࠨ଀"): [
              {
                bstack1ll11_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࠥଁ"): driver_command
              }
            ]
          },
          bstack1ll11_opy_ (u"ࠦࡷ࡫ࡳࡱࡱࡱࡷࡪࠨଂ"): {
            bstack1ll11_opy_ (u"ࠧࡨ࡯ࡥࡻࠥଃ"): {
              bstack1ll11_opy_ (u"ࠨ࡭ࡴࡩࠥ଄"): bstack1l1ll1l1l_opy_.get(bstack1ll11_opy_ (u"ࠢ࡮ࡵࡪࠦଅ"), bstack1ll11_opy_ (u"ࠣࠤଆ")) if isinstance(bstack1l1ll1l1l_opy_, dict) else bstack1ll11_opy_ (u"ࠤࠥଇ"),
              bstack1ll11_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶࠦଈ"): bstack1l1ll1l1l_opy_.get(bstack1ll11_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧଉ"), True) if isinstance(bstack1l1ll1l1l_opy_, dict) else True
            }
          }
        }
        logger.debug(bstack1ll11_opy_ (u"ࠬࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡣࡢࡰࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠ࡭ࡱࡪࠤࡩࡧࡴࡢ࠼ࠣࡿࢂ࠭ଊ").format(log_data))
        automation_logger.info(json.dumps(log_data, separators=(bstack1ll11_opy_ (u"࠭ࠬࠨଋ"), bstack1ll11_opy_ (u"ࠧ࠻ࠩଌ"))))
      except Exception as bstack1ll1l1llll_opy_:
        logger.debug(bstack1ll11_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡱࡵࡧࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳࠦࡤࡢࡶࡤ࠾ࠥࢁࡽࠨ଍").format(str(bstack1ll1l1llll_opy_)))
    except Exception as err:
      logger.debug(bstack1ll11_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡥࡳࡨࡲࡶࡲࠦࡳࡤࡣࡱࠤࢀࢃࠧ଎").format(str(err)))
    bstack1l1l111l11_opy_ = False
  response = bstack11l1lll1ll_opy_(self, driver_command, *args, **kwargs)
  if (bstack1ll11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩଏ") in str(FRAMEWORK_NAME).lower() or bstack1ll11_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫଐ") in str(FRAMEWORK_NAME).lower()) and bstack11l11l1lll_opy_.on():
    try:
      if driver_command == bstack1ll11_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠩ଑"):
        TestHubHandler.bstack1ll1llll_opy_({
            bstack1ll11_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬ଒"): response[bstack1ll11_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭ଓ")],
            bstack1ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨଔ"): TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack11l11l1lll_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
def bstack1lllll11l1_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack1ll1l11l_opy_
  global PLATFORM_INDEX
  global SESSION_NAME
  global PARALLELISE_VANILLA_PYTHON
  global PARALLELISE_THREADING_PYTHON
  global FRAMEWORK_NAME
  global bstack1llllllll1_opy_
  global bstack11l1ll1l11_opy_
  global bstack111l1111l1_opy_
  global bstack1l11l1llll_opy_
  bstack1l11ll1ll1_opy_ = bstack11ll11l1ll_opy_.bstack11l11l111_opy_(EVENTS.bstack1lll1ll111_opy_.value)
  if os.getenv(bstack1ll11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧକ")) is not None and a11y.bstack1111l1llll_opy_(CONFIG) is None:
    CONFIG[bstack1ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪଖ")] = True
  CONFIG[bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ଗ")] = str(FRAMEWORK_NAME) + str(__version__)
  bstack1l11l1l1_opy_ = os.environ[bstack1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪଘ")]
  bstack1ll1lll11_opy_ = TestHubUtils.bstack11ll1l111_opy_(CONFIG, FRAMEWORK_NAME)
  CONFIG[bstack1ll11_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩଙ")] = bstack1l11l1l1_opy_
  CONFIG[bstack1ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩଚ")] = bstack1ll1lll11_opy_
  if CONFIG.get(bstack1ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨଛ"),bstack1ll11_opy_ (u"ࠩࠪଜ")) and bstack1ll11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩଝ") in FRAMEWORK_NAME:
    CONFIG[bstack1ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫଞ")].pop(bstack1ll11_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪଟ"), None)
    CONFIG[bstack1ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ଠ")].pop(bstack1ll11_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬଡ"), None)
  command_executor = bstack1l111llll1_opy_()
  logger.debug(bstack1l1lll1l_opy_.format(command_executor))
  proxy = bstack1l11l11111_opy_(CONFIG, proxy)
  bstack11111lll1_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
  try:
    if PARALLELISE_VANILLA_PYTHON is True:
      bstack11111lll1_opy_ = int(multiprocessing.current_process().name)
    elif PARALLELISE_THREADING_PYTHON is True:
      bstack11111lll1_opy_ = int(threading.current_thread().name)
  except:
    bstack11111lll1_opy_ = 0
  bstack1lll1ll1_opy_ = get_caps(CONFIG, bstack11111lll1_opy_)
  logger.debug(CONFIG_FILE_CONTENT.format(str(bstack1lll1ll1_opy_)))
  if bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬଢ") in CONFIG and bstack1lll1111ll_opy_(CONFIG[bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ଣ")]):
    update_caps_for_local(bstack1lll1ll1_opy_)
  if a11y.is_enabled_platform(CONFIG, bstack11111lll1_opy_) and a11y.is_platform_supported(bstack1lll1ll1_opy_, options, desired_capabilities, CONFIG):
    threading.current_thread().a11yPlatform = True
    if (cli.accessibility is None or not cli.accessibility.is_enabled()):
      a11y.set_capabilities(bstack1lll1ll1_opy_, CONFIG)
  if desired_capabilities:
    bstack111lll1ll1_opy_ = bstack111ll1lll_opy_(desired_capabilities)
    bstack111lll1ll1_opy_[bstack1ll11_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪତ")] = bstack11l11l1l1l_opy_(CONFIG)
    bstack1ll1111l1l_opy_ = get_caps(bstack111lll1ll1_opy_)
    if bstack1ll1111l1l_opy_:
      bstack1lll1ll1_opy_ = update(bstack1ll1111l1l_opy_, bstack1lll1ll1_opy_)
    desired_capabilities = None
  if options:
    bstack111ll1ll1_opy_(options, bstack1lll1ll1_opy_)
  if not options:
    options = bstack1l1l11ll_opy_(bstack1lll1ll1_opy_)
  try:
    if bstack11l1l1ll11_opy_:
      def _1l11llll_opy_(bstack11lll1l1_opy_):
        if not isinstance(bstack11lll1l1_opy_, dict):
          return
        for _1l1llllll1_opy_ in list(bstack11lll1l1_opy_.keys()):
          _111lll1l1_opy_ = bstack11lll1l1_opy_[_1l1llllll1_opy_]
          if _111lll1l1_opy_ is None:
            bstack11lll1l1_opy_.pop(_1l1llllll1_opy_, None)
          elif isinstance(_111lll1l1_opy_, dict):
            _1l11llll_opy_(_111lll1l1_opy_)
      _1l11llll_opy_(bstack1lll1ll1_opy_)
      _1l11llll_opy_(desired_capabilities)
      if options is not None and hasattr(options, bstack1ll11_opy_ (u"ࠫࡤࡩࡡࡱࡵࠪଥ")):
        _1l11llll_opy_(options._caps)
  except Exception as e:
    logger.debug(bstack1ll11_opy_ (u"ࠧࡳ࡯ࡥࡡ࡬ࡲ࡮ࡺࠨࠪࠢࡳࡳࡸࡺ࠭ࡰࡲࡷ࡭ࡴࡴࡳࠡࡲࡵࡹࡳ࡫ࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡽࢀࠦଦ").format(e))
  if bstack11l1l1ll11_opy_:
    options = bstack1l111l111_opy_(options)
  bstack1l11l1llll_opy_ = CONFIG.get(bstack1ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଧ"))[bstack11111lll1_opy_]
  if proxy and bstack1lll11llll_opy_() >= version.parse(bstack1ll11_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧନ")):
    options.proxy(proxy)
  if options and bstack1lll11llll_opy_() >= version.parse(bstack1ll11_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ଩")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1lll11llll_opy_() < version.parse(bstack1ll11_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨପ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1lll1ll1_opy_)
  logger.info(bstack1l1111l1_opy_)
  bstack1ll1lll11l_opy_.end(EVENTS.bstack11ll1l111l_opy_.value, EVENTS.bstack11ll1l111l_opy_.value + bstack1ll11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥଫ"), EVENTS.bstack11ll1l111l_opy_.value + bstack1ll11_opy_ (u"ࠦ࠿࡫࡮ࡥࠤବ"), status=True, failure=None, test_name=SESSION_NAME)
  if bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡰࡳࡱࡩ࡭ࡱ࡫ࠧଭ") in kwargs:
    del kwargs[bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡱࡴࡲࡪ࡮ࡲࡥࠨମ")]
  bstack11ll11l1ll_opy_.end(EVENTS.bstack1lll1ll111_opy_.value, bstack1l11ll1ll1_opy_ + bstack1ll11_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢଯ"), bstack1l11ll1ll1_opy_ + bstack1ll11_opy_ (u"ࠣ࠼ࡨࡲࡩࠨର"), status=True, failure=None, test_name=SESSION_NAME)
  try:
    if bstack1lll11llll_opy_() >= version.parse(bstack1ll11_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩ଱")):
      bstack1llllllll1_opy_(self, command_executor=command_executor,
                options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
    elif bstack1lll11llll_opy_() >= version.parse(bstack1ll11_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩଲ")):
      bstack1llllllll1_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities, options=options,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1lll11llll_opy_() >= version.parse(bstack1ll11_opy_ (u"ࠫ࠷࠴࠵࠴࠰࠳ࠫଳ")):
      bstack1llllllll1_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    else:
      bstack1llllllll1_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive)
  except Exception as bstack1l1l111l1l_opy_:
    logger.error(bstack1l111l1ll_opy_.format(bstack1ll11_opy_ (u"ࠬࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠫ଴"), str(bstack1l1l111l1l_opy_)))
    raise bstack1l1l111l1l_opy_
  bstack1l11ll1ll1_opy_ = bstack11ll11l1ll_opy_.bstack11l11l111_opy_(EVENTS.bstack1ll11llll_opy_.value)
  if a11y.is_enabled_platform(CONFIG, bstack11111lll1_opy_) and a11y.is_platform_supported(self.caps, options, desired_capabilities):
    if CONFIG[bstack1ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨଵ")][bstack1ll11_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ଶ")] == True:
      threading.current_thread().appA11yPlatform = True
      if cli.accessibility is None or not cli.accessibility.is_enabled():
        a11y.set_capabilities(bstack1lll1ll1_opy_, CONFIG)
  try:
    bstack11lll1ll11_opy_ = bstack1ll11_opy_ (u"ࠨࠩଷ")
    if bstack1lll11llll_opy_() >= version.parse(bstack1ll11_opy_ (u"ࠩ࠷࠲࠵࠴࠰ࡣ࠳ࠪସ")):
      if self.caps is not None:
        bstack11lll1ll11_opy_ = self.caps.get(bstack1ll11_opy_ (u"ࠥࡳࡵࡺࡩ࡮ࡣ࡯ࡌࡺࡨࡕࡳ࡮ࠥହ"))
    else:
      if self.capabilities is not None:
        bstack11lll1ll11_opy_ = self.capabilities.get(bstack1ll11_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦ଺"))
    if bstack11lll1ll11_opy_:
      bstack11llll11_opy_(bstack11lll1ll11_opy_)
      if bstack1lll11llll_opy_() <= version.parse(bstack1ll11_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬ଻")):
        if bstack11llll1l1l_opy_.startswith(bstack1ll11_opy_ (u"࠭ࡨࡵࡶࡳ࠾࠴࠵଼ࠧ")) or bstack11llll1l1l_opy_.startswith(bstack1ll11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࠩଽ")):
          self.command_executor._url = bstack11llll1l1l_opy_
        else:
          self.command_executor._url = bstack1ll11_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤା") + bstack11llll1l1l_opy_ + bstack1ll11_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨି")
      else:
        self.command_executor._url = bstack1ll11_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧୀ") + bstack11lll1ll11_opy_ + bstack1ll11_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧୁ")
      logger.debug(bstack11ll1ll11_opy_.format(bstack11lll1ll11_opy_))
    else:
      logger.debug(bstack1ll1ll11l_opy_.format(bstack1ll11_opy_ (u"ࠧࡕࡰࡵ࡫ࡰࡥࡱࠦࡈࡶࡤࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨୂ")))
  except Exception as e:
    logger.debug(bstack1ll1ll11l_opy_.format(e))
  if bstack1ll11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬୃ") in FRAMEWORK_NAME:
    bstack1l11111ll1_opy_(PLATFORM_INDEX, bstack111l1111l1_opy_)
  bstack1ll1l11l_opy_ = self.session_id
  if bstack1ll11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧୄ") in FRAMEWORK_NAME or bstack1ll11_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ୅") in FRAMEWORK_NAME or bstack1ll11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ୆") in FRAMEWORK_NAME or bstack1ll11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠫେ") in FRAMEWORK_NAME:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack11l1ll111_opy_ = getattr(threading.current_thread(), bstack1ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡘࡪࡹࡴࡎࡧࡷࡥࠬୈ"), None)
  if bstack1ll11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ୉") in FRAMEWORK_NAME or bstack1ll11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ୊") in FRAMEWORK_NAME:
    TestHubHandler.send_cbt_info(self)
  if bstack1ll11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧୋ") in FRAMEWORK_NAME and bstack11l1ll111_opy_ and bstack11l1ll111_opy_.get(bstack1ll11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨୌ"), bstack1ll11_opy_ (u"୍ࠩࠪ")) == bstack1ll11_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ୎"):
    TestHubHandler.send_cbt_info(self)
  with bstack1llll1l1l_opy_:
    bstack11l1ll1l11_opy_.append(self)
  if bstack1ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ୏") in CONFIG and bstack1ll11_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ୐") in CONFIG[bstack1ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ୑")][bstack11111lll1_opy_]:
    SESSION_NAME = CONFIG[bstack1ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ୒")][bstack11111lll1_opy_][bstack1ll11_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭୓")]
  logger.debug(bstack111l11111l_opy_.format(bstack1ll1l11l_opy_))
  bstack11ll11l1ll_opy_.end(EVENTS.bstack1ll11llll_opy_.value, bstack1l11ll1ll1_opy_ + bstack1ll11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ୔"), bstack1l11ll1ll1_opy_ + bstack1ll11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ୕"), status=True, failure=None, test_name=SESSION_NAME)
ROBOT_PLAYWRIGHT_CDP_URL = None
bstack1llll1l11l_opy_ = False
bstack111llll11_opy_ = None
def set_playwright_globals(**kwargs):
    bstack1ll11_opy_ (u"ࠦࠧࠨࡉ࡯࡬ࡨࡧࡹࠦࡧ࡭ࡱࡥࡥࡱࡹࠠࡧࡴࡲࡱࠥࡥ࡟ࡪࡰ࡬ࡸࡤࡥ࠮ࡱࡻࠣ࡭ࡳࡺ࡯ࠡࡶ࡫࡭ࡸࠦ࡭ࡰࡦࡸࡰࡪ࠭ࡳࠡࡰࡤࡱࡪࡹࡰࡢࡥࡨ࠲ࠏࠦࠠࠡࠢࡆࡥࡱࡲࡥࡥࠢࡥࡽࠥࡥ࡟ࡪࡰ࡬ࡸࡤࡥ࠮ࡱࡻࠣࡦࡪ࡬࡯ࡳࡧࠣࡴࡦࡺࡣࡩࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠮ࠩࠡࡵࡲࠤࡹ࡮ࡡࡵࠢࡰࡳࡩࡥ࡬ࡢࡷࡱࡧ࡭ࠐࠠࠡࠢࠣࡥࡳࡪࠠࡱࡣࡷࡧ࡭ࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡧࡦࡴࠠࡢࡥࡦࡩࡸࡹࠠࡄࡑࡑࡊࡎࡍࠬࠡࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣࡓࡇࡍࡆ࠮ࠣࡩࡹࡩ࠮ࠣࠤࠥୖ")
    g = globals()
    for key, value in kwargs.items():
        g[key] = value
try:
  try:
    import Browser
    import os
    from subprocess import Popen
    from browserstack_sdk.__init__ import get_turboscale_playwright_url
    from browserstack_sdk.sdk_cli.utils.bstack11ll1l1ll_opy_ import bstack1l1lll1l11_opy_
    def bstack1ll1lll1l1_opy_(self, args, **kwargs):
      global CONFIG
      global SELENIUM_OR_PLAYWRIGHT_INSTALLED
      global ROBOT_PLAYWRIGHT_CDP_URL
      global bstack1llll1l11l_opy_
      from browserstack_sdk.__init__ import LAUNCH_PATCH_ROBOT_PLAYWRIGHT
      if(bstack1ll11_opy_ (u"ࠧ࡯࡮ࡥࡧࡻ࠲࡯ࡹࠢୗ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1ll11_opy_ (u"࠭ࡾࠨ୘")), bstack1ll11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ୙"), bstack1ll11_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪ୚")), bstack1ll11_opy_ (u"ࠩࡺࠫ୛")) as fp:
          fp.write(bstack1ll11_opy_ (u"ࠥࠦଡ଼"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1ll11_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨଢ଼")))):
          with open(args[1], bstack1ll11_opy_ (u"ࠬࡸࠧ୞")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1ll11_opy_ (u"࠭ࡡࡴࡻࡱࡧࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡠࡰࡨࡻࡕࡧࡧࡦࠪࡦࡳࡳࡺࡥࡹࡶ࠯ࠤࡵࡧࡧࡦࠢࡀࠤࡻࡵࡩࡥࠢ࠳࠭ࠬୟ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack111l11ll_opy_)
            if bstack1ll11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫୠ") in CONFIG and str(CONFIG[bstack1ll11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬୡ")]).lower() != bstack1ll11_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨୢ"):
                cdpUrl = get_turboscale_playwright_url()
                LAUNCH_PATCH_ROBOT_PLAYWRIGHT = bstack1ll11_opy_ (u"ࠪࠫࠬࠐ࠯ࠫࠢࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࠦࠪ࠰ࠌࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠶࡟ࠣࡁࡂࡃࠠࠨࡶࡵࡹࡪ࠭࠻ࠋࡥࡲࡲࡸࡺࠠࡣࡵࡷࡥࡨࡱ࡟ࡱࡣࡷ࡬ࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴࡟࠾ࠎࡨࡵ࡮ࡴࡶࠣࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࡝ࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠵ࡢࡁࠊࡤࡱࡱࡷࡹࠦࡰࡠ࡫ࡱࡨࡪࡾࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠵ࡡࡀࠐࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠵࡟ࠣࡁࡂࡃࠠࠨࡶࡵࡹࡪ࠭࠻ࠋࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯ࡵ࡯࡭ࡨ࡫ࠨ࠱࠮ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠺࠯࠻ࠋࡥࡲࡲࡸࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯ࠥࡃࠠࡳࡧࡴࡹ࡮ࡸࡥࠩࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨࠩ࠼ࠌࡦࡳࡳࡹࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡧ࡭ࡸ࡯࡮࡫ࡸࡱࡤࡲࡡࡶࡰࡦ࡬ࠥࡃࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮࡭ࡣࡸࡲࡨ࡮࠮ࡣ࡫ࡱࡨ࠭࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠮ࡁࠊࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮࡭ࡣࡸࡲࡨ࡮ࠠ࠾ࠢࡤࡷࡾࡴࡣࠡࠪ࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴࠫࠣࡁࡃࠦࡻࡼࠌࠣࠤ࡮࡬ࠠࠩࠣࡥࡷࡹࡧࡣ࡬ࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠯ࠠࡼࡽࠍࠤࠥࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦ࡯ࡳ࡫ࡪ࡭ࡳࡧ࡬ࡠࡥ࡫ࡶࡴࡳࡩࡶ࡯ࡢࡰࡦࡻ࡮ࡤࡪࠫࡰࡦࡻ࡮ࡤࡪࡒࡴࡹ࡯࡯࡯ࡵࠬ࠿ࠏࠦࠠࡾࡿࠍࠤࠥࡲࡥࡵࠢࡦࡥࡵࡹ࠻ࠋࠢࠣࡸࡷࡿࠠࡼࡽࠍࠤࠥࠦࠠࡤࡣࡳࡷࠥࡃࠠࡋࡕࡒࡒ࠳ࡶࡡࡳࡵࡨࠬࡧࡹࡴࡢࡥ࡮ࡣࡨࡧࡰࡴࠫ࠾ࠎࠥࠦࡽࡾࠢࡦࡥࡹࡩࡨࠡࠪࡨࡼ࠮ࠦࡻࡼࠌࠣࠤࠥࠦࡣࡰࡰࡶࡳࡱ࡫࠮ࡦࡴࡵࡳࡷ࠮ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠻ࠤ࠯ࠤࡪࡾࠩ࠼ࠌࠣࠤࢂࢃࠊࠡࠢ࡬ࡪࠥ࠮ࡢࡴࡶࡤࡧࡰࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠯ࠠࡼࡽࠍࠤࠥࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࡏࡷࡧࡵࡇࡉࡖࠨࡼࡽࠍࠤࠥࠦࠠࠡࠢࡨࡲࡩࡶ࡯ࡪࡰࡷ࡙ࡗࡒ࠺ࠡࠩࡾࡧࡩࡶࡕࡳ࡮ࢀࠫࠥ࠱ࠠࡦࡰࡦࡳࡩ࡫ࡕࡓࡋࡆࡳࡲࡶ࡯࡯ࡧࡱࡸ࠭ࡐࡓࡐࡐ࠱ࡷࡹࡸࡩ࡯ࡩ࡬ࡪࡾ࠮ࡣࡢࡲࡶ࠭࠮࠲ࠊࠡࠢࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴࠌࠣࠤࠥࠦࡽࡾࠫ࠾ࠎࠥࠦࡽࡾࠌࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࢁࠊࠡࠢࠣࠤࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࠻ࠢࠪࡿࡨࡪࡰࡖࡴ࡯ࢁࠬࠦࠫࠡࡧࡱࡧࡴࡪࡥࡖࡔࡌࡇࡴࡳࡰࡰࡰࡨࡲࡹ࠮ࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡤࡣࡳࡷ࠮࠯ࠬࠋࠢࠣࠤࠥ࠴࠮࠯࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠋࠢࠣࢁࢂ࠯࠻ࠋࡿࢀ࠿ࠏࡩ࡯࡯ࡵࡷࠤࡴࡸࡩࡨ࡫ࡱࡥࡱࡥࡣࡰࡰࡱࡩࡨࡺࠠ࠾ࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱ࠮ࡤࡪࡵࡳࡲ࡯ࡵ࡮࠰ࡦࡳࡳࡴࡥࡤࡶ࠱ࡦ࡮ࡴࡤࠩ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭ࠪ࠽ࠍ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷࠤࡂࠦࡡࡴࡻࡱࡧࠥ࠮ࡣࡰࡰࡱࡩࡨࡺࡏࡱࡶ࡬ࡳࡳࡹࠩࠡ࠿ࡁࠤࢀࢁࠊࠡࠢ࡬ࡪࠥ࠮ࠡࡣࡵࡷࡥࡨࡱ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠭ࠥࢁࡻࠋࠢࠣࠤࠥࡸࡥࡵࡷࡵࡲࠥࡧࡷࡢ࡫ࡷࠤࡴࡸࡩࡨ࡫ࡱࡥࡱࡥࡣࡰࡰࡱࡩࡨࡺࠨࡤࡱࡱࡲࡪࡩࡴࡐࡲࡷ࡭ࡴࡴࡳࠪ࠽ࠍࠤࠥࢃࡽࠋࠢࠣࡰࡪࡺࠠࡤࡣࡳࡷࡀࠐࠠࠡࡶࡵࡽࠥࢁࡻࠋࠢࠣࠤࠥࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࠼ࠌࠣࠤࢂࢃࠠࡤࡣࡷࡧ࡭ࠦࠨࡦࡺࠬࠤࢀࢁࠊࠡࠢࢀࢁࠏࠦࠠࡤࡱࡱࡷࡹࠦ࡭ࡰࡦ࡬ࡪ࡮࡫ࡤࡆࡰࡧࡴࡴ࡯࡮ࡵࠢࡀࠤࠬࢁࡣࡥࡲࡘࡶࡱࢃࠧࠡ࠭ࠣࡩࡳࡩ࡯ࡥࡧࡘࡖࡎࡉ࡯࡮ࡲࡲࡲࡪࡴࡴࠩࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡦࡥࡵࡹࠩࠪ࠽ࠍࠤࠥ࡯ࡦࠡࠪࡥࡷࡹࡧࡣ࡬ࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠫࠣࡿࢀࠐࠠࠡࠢࠣࡶࡪࡺࡵࡳࡰࠣࡥࡼࡧࡩࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱ࠮ࡤࡪࡵࡳࡲ࡯ࡵ࡮࠰ࡦࡳࡳࡴࡥࡤࡶࡒࡺࡪࡸࡃࡅࡒࠫࡿࢀࠐࠠࠡࠢࠣࠤࠥ࡫࡮ࡥࡲࡲ࡭ࡳࡺࡕࡓࡎ࠽ࠤࡲࡵࡤࡪࡨ࡬ࡩࡩࡋ࡮ࡥࡲࡲ࡭ࡳࡺࠬࠋࠢࠣࠤࠥࠦࠠ࠯࠰࠱ࡧࡴࡴ࡮ࡦࡥࡷࡓࡵࡺࡩࡰࡰࡶࠎࠥࠦࠠࠡࡿࢀ࠭ࡀࠐࠠࠡࡿࢀࠎࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥࡵࡲࡪࡩ࡬ࡲࡦࡲ࡟ࡤࡱࡱࡲࡪࡩࡴࠩࡽࡾࠎࠥࠦࠠࠡ࠰࠱࠲ࡨࡵ࡮࡯ࡧࡦࡸࡔࡶࡴࡪࡱࡱࡷ࠱ࠐࠠࠡࠢࠣࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺ࠺ࠡ࡯ࡲࡨ࡮࡬ࡩࡦࡦࡈࡲࡩࡶ࡯ࡪࡰࡷࠎࠥࠦࡽࡾࠫ࠾ࠎࢂࢃ࠻ࠋ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࠎࠬ࠭ࠧୣ").format(cdpUrl=cdpUrl)
            lines.insert(1, LAUNCH_PATCH_ROBOT_PLAYWRIGHT)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1ll11_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨ୤")), bstack1ll11_opy_ (u"ࠬࡽࠧ୥")) as bstack1l1l1ll111_opy_:
              bstack1l1l1ll111_opy_.writelines(lines)
        CONFIG[bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ୦")] = str(FRAMEWORK_NAME) + str(__version__)
        bstack1l11l1l1_opy_ = os.environ[bstack1ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ୧")]
        bstack1ll1lll11_opy_ = TestHubUtils.bstack11ll1l111_opy_(CONFIG, FRAMEWORK_NAME)
        CONFIG[bstack1ll11_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ୨")] = bstack1l11l1l1_opy_
        CONFIG[bstack1ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ୩")] = bstack1ll1lll11_opy_
        bstack11111lll1_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
        try:
          if PARALLELISE_VANILLA_PYTHON is True:
            bstack11111lll1_opy_ = int(multiprocessing.current_process().name)
          elif PARALLELISE_THREADING_PYTHON is True:
            bstack11111lll1_opy_ = int(threading.current_thread().name)
        except Exception:
          bstack11111lll1_opy_ = 0
        CONFIG[bstack1ll11_opy_ (u"ࠥࡹࡸ࡫ࡗ࠴ࡅࠥ୪")] = False
        CONFIG[bstack1ll11_opy_ (u"ࠦ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ୫")] = True
        bstack1111l1lll1_opy_ = bstack1l1lll1l11_opy_(bstack11111lll1_opy_)
        if bstack1111l1lll1_opy_ is not None:
          import bstack_utils.constants as _1llll1llll_opy_
          _1lll1l1l_opy_ = bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭୬") if bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ୭") in bstack1111l1lll1_opy_ else bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ୮")
          _1l11ll1lll_opy_ = bstack1111l1lll1_opy_.get(_1lll1l1l_opy_, bstack1ll11_opy_ (u"ࠨࠩ୯")).strip().lower()
          _1ll1lll1_opy_ = _1l11ll1lll_opy_ in _1llll1llll_opy_.bstack1111l111l1_opy_
          if bstack1111l1lll1_opy_.get(bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ୰")) and not _1ll1lll1_opy_:
            bstack1111l1lll1_opy_[bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩୱ")] = False
            _1l11ll111_opy_ = [k for k in bstack1111l1lll1_opy_ if k.startswith(bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ୲"))]
            for k in _1l11ll111_opy_:
              del bstack1111l1lll1_opy_[k]
          bstack1ll11l11_opy_ = bstack1111l1lll1_opy_
          import urllib.parse
          if bstack1ll11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ୳") in CONFIG and str(CONFIG[bstack1ll11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ୴")]).lower() != bstack1ll11_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭୵"):
            ROBOT_PLAYWRIGHT_CDP_URL = get_turboscale_playwright_url() + urllib.parse.quote(json.dumps(bstack1ll11l11_opy_))
          else:
            ROBOT_PLAYWRIGHT_CDP_URL = bstack1ll11_opy_ (u"ࠨࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠪ୶") + urllib.parse.quote(json.dumps(bstack1ll11l11_opy_))
          os.environ[bstack1ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡒࡆࡔ࡚࡟ࡑ࡙ࡢࡇࡉࡖ࡟ࡖࡔࡏࠫ୷")] = ROBOT_PLAYWRIGHT_CDP_URL
          bstack1llll1l11l_opy_ = True
          from browserstack_sdk.sdk_cli.bstack1l11111ll_opy_ import bstack111l1ll111_opy_
          from browserstack_sdk.sdk_cli.bstack1l1ll1l11l_opy_ import bstack1l111lllll_opy_
          instance = next(iter(bstack111l1ll111_opy_.bstack1l1l111l_opy_.values()), None)
          if instance:
            bstack1l111lllll_opy_.bstack1l11lllll_opy_(instance, bstack1l111lllll_opy_.bstack1lll1l1111_opy_, bstack1111l1lll1_opy_)
            bstack1l111lllll_opy_.bstack1l11lllll_opy_(instance, bstack1l111lllll_opy_.bstack1ll11l1lll_opy_, ROBOT_PLAYWRIGHT_CDP_URL)
          try:
            from browserstack_sdk.sdk_cli.cli import cli as _1l11l1111_opy_
            from browserstack_sdk.sdk_cli.bstack1l11111ll_opy_ import bstack1ll1l1ll11_opy_, bstack1ll11ll1ll_opy_
            _1l11l1111_opy_.bstack1l11111ll_opy_.bstack1ll1ll111l_opy_(
              None,
              (instance, bstack1ll11_opy_ (u"ࠪࡱࡴࡪ࡟ࡱࡱࡳࡩࡳ࠭୸")),
              (bstack1ll1l1ll11_opy_.bstack1ll11lllll_opy_, bstack1ll11ll1ll_opy_.PRE),
              None,
            )
          except Exception as e:
            logger.debug(bstack1ll11_opy_ (u"ࠦࡲࡵࡤࡠࡲࡲࡴࡪࡴ࠺ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡫࡯ࡲࡦࠢࡆࡖࡊࡇࡔࡆ࠰ࡓࡖࡊࡀࠠࡼࡿࠥ୹").format(e))
          logger.debug(bstack1ll11_opy_ (u"ࠧࡳ࡯ࡥࡡࡳࡳࡵ࡫࡮࠻ࠢࡸࡷ࡮ࡴࡧࠡࡨ࡬ࡲࡦࡲ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡦࡳࡱࡰࠤࡉࡸࡩࡷࡧࡵࡍࡳ࡯ࡴࠣ୺"))
        else:
          bstack1ll11l11_opy_ = get_caps(CONFIG, bstack11111lll1_opy_)
          if CONFIG.get(bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ୻")):
            update_caps_for_local(bstack1ll11l11_opy_)
            bstack1ll11l11_opy_[bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ୼")] = os.environ[bstack1ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪ୽")]
          logger.debug(bstack1ll11_opy_ (u"ࠤࡰࡳࡩࡥࡰࡰࡲࡨࡲ࠿ࠦࡄࡳ࡫ࡹࡩࡷࡏ࡮ࡪࡶࠣࡹࡳࡧࡶࡢ࡫࡯ࡥࡧࡲࡥ࠭ࠢࡩࡥࡱࡲࡩ࡯ࡩࠣࡦࡦࡩ࡫ࠡࡶࡲࠤ࡬࡫ࡴࡠࡥࡤࡴࡸࠨ୾"))
        logger.debug(CONFIG_FILE_CONTENT.format(str(bstack1ll11l11_opy_)))
        if bstack1ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭୿") in CONFIG and bstack1ll11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ஀") in CONFIG[bstack1ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ஁")][bstack11111lll1_opy_]:
          SESSION_NAME = CONFIG[bstack1ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩஂ")][bstack11111lll1_opy_][bstack1ll11_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬஃ")]
        from bstack_utils.helper import bstack1ll11l1l11_opy_
        args.append(bstack1ll11_opy_ (u"ࠨࡶࡵࡹࡪ࠭஄") if bstack1ll11l1l11_opy_(CONFIG) else bstack1ll11_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨஅ"))
        args.append(str(bstack1ll11l11_opy_.get(bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩஆ"), False)).lower())
        args.append(os.path.join(os.path.expanduser(bstack1ll11_opy_ (u"ࠫࢃ࠭இ")), bstack1ll11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬஈ"), bstack1ll11_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨஉ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1ll11l11_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1ll11_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤஊ"))
      SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
      return bstack111l1l1ll_opy_(self, args, **kwargs)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1l11111l1_opy_(self,
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
    global PLATFORM_INDEX
    global SESSION_NAME
    global PARALLELISE_VANILLA_PYTHON
    global PARALLELISE_THREADING_PYTHON
    global FRAMEWORK_NAME
    CONFIG[bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ஋")] = str(FRAMEWORK_NAME) + str(__version__)
    bstack1l11l1l1_opy_ = os.environ[bstack1ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ஌")]
    bstack1ll1lll11_opy_ = TestHubUtils.bstack11ll1l111_opy_(CONFIG, FRAMEWORK_NAME)
    CONFIG[bstack1ll11_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭஍")] = bstack1l11l1l1_opy_
    CONFIG[bstack1ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭எ")] = bstack1ll1lll11_opy_
    bstack11111lll1_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
    try:
      if PARALLELISE_VANILLA_PYTHON is True:
        bstack11111lll1_opy_ = int(multiprocessing.current_process().name)
      elif PARALLELISE_THREADING_PYTHON is True:
        bstack11111lll1_opy_ = int(threading.current_thread().name)
    except Exception:
      bstack11111lll1_opy_ = 0
    CONFIG[bstack1ll11_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦஏ")] = True
    bstack1lll1ll1_opy_ = get_caps(CONFIG, bstack11111lll1_opy_)
    bstack111l11l1l_opy_ = bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧஐ") if bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ஑") in bstack1lll1ll1_opy_ else bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ஒ")
    bstack1l11llll1_opy_ = False
    try:
        from bstack_utils import accessibility as a11y
        import bstack_utils.constants as bstack11ll1111l1_opy_
        bstack1l1111l1ll_opy_ = bstack1lll1ll1_opy_.get(bstack111l11l1l_opy_, bstack1ll11_opy_ (u"ࠩࠪஓ")).strip().lower()
        browser_version = str(bstack1lll1ll1_opy_.get(bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬஔ"), bstack1lll1ll1_opy_.get(bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬக"), bstack1ll11_opy_ (u"ࠬ࠭஖")))).strip()
        bstack11l1ll1lll_opy_ = bstack1l1111l1ll_opy_ in bstack11ll1111l1_opy_.bstack1111l111l1_opy_
        min_version = bstack11ll1111l1_opy_.MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION
        if not browser_version or browser_version.lower().startswith(bstack1ll11_opy_ (u"࠭࡬ࡢࡶࡨࡷࡹ࠭஗")):
            bstack11lll11l1_opy_ = True
        else:
            major = browser_version.split(bstack1ll11_opy_ (u"ࠧ࠯ࠩ஘"))[0]
            bstack11lll11l1_opy_ = major.isdigit() and int(major) > min_version
        if not bstack11lll11l1_opy_:
            logger.warning(bstack1ll11_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠣ࡫ࡷ࡫ࡡࡵࡧࡵࠤࡹ࡮ࡡ࡯ࠢࡾࢁ࠳ࠦࡃࡶࡴࡵࡩࡳࡺࠠࡷࡧࡵࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠧங").format(min_version, browser_version))
        if a11y.is_enabled_platform(CONFIG, bstack11111lll1_opy_) and bstack11l1ll1lll_opy_ and bstack11lll11l1_opy_ and a11y.is_platform_supported(bstack1lll1ll1_opy_, options=None, config=CONFIG):
            bstack1l11llll1_opy_ = True
            import browserstack_sdk
            browserstack_sdk.CONFIG[bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨச")] = True
            bstack1lll1ll1_opy_[bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ஛")] = True
            if CONFIG.get(bstack1ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ஜ")):
                bstack1lll1ll1_opy_[bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭஝")] = CONFIG[bstack1ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨஞ")]
            import json as _json
            bstack1ll11l1ll1_opy_ = os.getenv(bstack1ll11_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬட"))
            bstack1lllll11_opy_ = bstack1lll1ll1_opy_.get(bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹ࠮ࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪ஠"))
            if not bstack1ll11l1ll1_opy_ and bstack1lllll11_opy_:
                os.environ[bstack1ll11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ஡")] = bstack1lllll11_opy_
                bstack1ll11l1ll1_opy_ = bstack1lllll11_opy_
            if bstack1ll11l1ll1_opy_:
                bstack1lll1ll1_opy_[bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴ࠰ࡤࡹࡹ࡮ࡔࡰ࡭ࡨࡲࠬ஢")] = bstack1ll11l1ll1_opy_
            bstack111lllll_opy_ = _json.loads(os.getenv(bstack1ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬண"), bstack1ll11_opy_ (u"ࠬࢁࡽࠨத"))).get(bstack1ll11_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ஥"))
            if bstack111lllll_opy_:
                bstack1lll1ll1_opy_[bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠴ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ஦")] = bstack111lllll_opy_
            bstack1lll1ll1_opy_.pop(bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ஧"), None)
            bstack1lll1ll1_opy_.pop(bstack1ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩந"), None)
            bstack1lll1ll1_opy_.pop(bstack1ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪன"), None)
            logger.debug(bstack1ll11_opy_ (u"ࠦࡆ࠷࠱ࡺࠢࡨࡲࡦࡨ࡬ࡦࡦࠣࡪࡴࡸࠠࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥ࠮ࡻࡾࠢࡾࢁ࠮ࠨப").format(
                bstack1l1111l1ll_opy_, browser_version))
    except Exception as e:
        bstack1l11llll1_opy_ = False
        logger.debug(bstack1ll11_opy_ (u"ࠧࡇ࠱࠲ࡻࠣࡨࡪࡺࡥࡤࡶ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࡼࡿࠥ஫").format(str(e)))
    logger.debug(CONFIG_FILE_CONTENT.format(str(bstack1lll1ll1_opy_)))
    if CONFIG.get(bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ஬")):
      update_caps_for_local(bstack1lll1ll1_opy_)
    if bstack1ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ஭") in CONFIG and bstack1ll11_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ம") in CONFIG[bstack1ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬய")][bstack11111lll1_opy_]:
      SESSION_NAME = CONFIG[bstack1ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ர")][bstack11111lll1_opy_][bstack1ll11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩற")]
    import urllib
    import json
    if bstack1ll11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩல") in CONFIG and str(CONFIG[bstack1ll11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪள")]).lower() != bstack1ll11_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ழ"):
        bstack11l11l11ll_opy_ = get_turboscale_playwright_url()
        cdpUrl = bstack11l11l11ll_opy_ + urllib.parse.quote(json.dumps(bstack1lll1ll1_opy_))
    else:
        cdpUrl = bstack1ll11_opy_ (u"ࠨࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠪவ") + urllib.parse.quote(json.dumps(bstack1lll1ll1_opy_))
    try:
        from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
        PlaywrightDriverWrapperDirect.setup_dispatch_capture()
    except Exception as exc:
        logger.debug(bstack1ll11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࡷࡳࠤࡩ࡯ࡳࡱࡣࡷࡧ࡭ࠦࡣࡢࡲࡷࡹࡷ࡫ࠠࡧࡱࡵࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤ࠻ࠢࠨࡷࠧஶ"), exc)
    if bstack1l11llll1_opy_:
        browser = self.connect_over_cdp(cdpUrl)
    else:
        browser = bstack111llll11_opy_(self, cdpUrl)
    try:
        from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
        wrapper = PlaywrightDriverWrapperDirect(browser, page=None, capabilities=bstack1lll1ll1_opy_, config=CONFIG)
        threading.current_thread().bstackSessionDriver = wrapper
        logger.debug(bstack1ll11_opy_ (u"ࠥࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࡄࡳ࡫ࡹࡩࡷ࡝ࡲࡢࡲࡳࡩࡷࡊࡩࡳࡧࡦࡸࠥࡹࡥࡵࡷࡳࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࠦࡦࡰࡴࠣࡸ࡭ࡸࡥࡢࡦࠣࠩࡸࠨஷ"), threading.get_ident())
        threading.current_thread().bstackTestErrorMessages = []
        if bstack1l11llll1_opy_:
            threading.current_thread().a11yPlatform = True
            wrapper.bstackA11yShouldScan = True
        if wrapper.session_id and not wrapper._cbt_info_sent:
            PlaywrightDriverWrapperDirect._send_cbt_info_on_session()
        try:
            from playwright.sync_api import Browser as bstack1l11111111_opy_
            if not hasattr(bstack1l11111111_opy_, bstack1ll11_opy_ (u"ࠫࡤࡨࡳࡵࡣࡦ࡯ࡤࡴࡥࡸࡡࡳࡥ࡬࡫࡟ࡱࡣࡷࡧ࡭࡫ࡤࠨஸ")):
                _11l111l11_opy_ = bstack1l11111111_opy_.new_page
                def _11l11ll1l_opy_(bstack111lll11l1_opy_, *bstack11l1l1l11l_opy_, **bstack1l11ll1l1l_opy_):
                    if getattr(threading.current_thread(), bstack1ll11_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫஹ"), None):
                        try:
                            bstack111ll11ll_opy_ = bstack111lll11l1_opy_.contexts[0] if bstack111lll11l1_opy_.contexts else None
                            if bstack111ll11ll_opy_ and bstack111ll11ll_opy_.pages:
                                page = None
                                for _11111l1l1l_opy_ in bstack111ll11ll_opy_.pages:
                                    if bstack1ll11_opy_ (u"ࠨࡡࡣࡱࡸࡸ࠿ࡨ࡬ࡢࡰ࡮ࠦ஺") in _11111l1l1l_opy_.url:
                                        page = _11111l1l1l_opy_
                                        logger.debug(bstack1ll11_opy_ (u"ࠢࡂ࠳࠴ࡽ࠿ࠦࡲࡦࡷࡶ࡭ࡳ࡭ࠠࡢࡤࡲࡹࡹࡀࡢ࡭ࡣࡱ࡯ࠥࡶࡡࡨࡧࠣࡪࡷࡵ࡭ࠡࡦࡨࡪࡦࡻ࡬ࡵࠢࡦࡳࡳࡺࡥࡹࡶࠥ஻"))
                                        break
                                if page is None:
                                    page = bstack111ll11ll_opy_.new_page(*bstack11l1l1l11l_opy_, **bstack1l11ll1l1l_opy_)
                                    logger.debug(bstack1ll11_opy_ (u"ࠣࡃ࠴࠵ࡾࡀࠠ࡯ࡱࠣࡦࡱࡧ࡮࡬ࠢࡳࡥ࡬࡫ࠠࡧࡱࡸࡲࡩ࠲ࠠࡤࡴࡨࡥࡹ࡫ࡤࠡࡰࡨࡻࠥࡶࡡࡨࡧࠣ࡭ࡳࠦࡤࡦࡨࡤࡹࡱࡺࠠࡤࡱࡱࡸࡪࡾࡴࠣ஼"))
                            elif bstack111ll11ll_opy_:
                                page = bstack111ll11ll_opy_.new_page(*bstack11l1l1l11l_opy_, **bstack1l11ll1l1l_opy_)
                                logger.debug(bstack1ll11_opy_ (u"ࠤࡄ࠵࠶ࡿ࠺ࠡࡥࡵࡩࡦࡺࡥࡥࠢࡱࡩࡼࠦࡰࡢࡩࡨࠤ࡮ࡴࠠࡥࡧࡩࡥࡺࡲࡴࠡࡥࡲࡲࡹ࡫ࡸࡵࠤ஽"))
                            else:
                                page = _11l111l11_opy_(bstack111lll11l1_opy_, *bstack11l1l1l11l_opy_, **bstack1l11ll1l1l_opy_)
                                logger.debug(bstack1ll11_opy_ (u"ࠥࡅ࠶࠷ࡹ࠻ࠢࡱࡳࠥࡪࡥࡧࡣࡸࡰࡹࠦࡣࡰࡰࡷࡩࡽࡺࠬࠡࡨࡤࡰࡱ࡯࡮ࡨࠢࡥࡥࡨࡱࠠࡵࡱࠣࡲࡪࡽ࡟ࡱࡣࡪࡩ࠭࠯ࠢா"))
                        except Exception as bstack11lllllll_opy_:
                            logger.debug(bstack1ll11_opy_ (u"ࠦࡆ࠷࠱ࡺ࠼ࠣࡨࡪ࡬ࡡࡶ࡮ࡷࠤࡨࡵ࡮ࡵࡧࡻࡸࠥࡶࡡࡨࡧࠣࡶࡪࡻࡳࡦࠢࡩࡥ࡮ࡲࡥࡥࠢࠫࠩࡸ࠯ࠬࠡࡨࡤࡰࡱ࡯࡮ࡨࠢࡥࡥࡨࡱࠢி"), bstack11lllllll_opy_)
                            page = _11l111l11_opy_(bstack111lll11l1_opy_, *bstack11l1l1l11l_opy_, **bstack1l11ll1l1l_opy_)
                    else:
                        page = _11l111l11_opy_(bstack111lll11l1_opy_, *bstack11l1l1l11l_opy_, **bstack1l11ll1l1l_opy_)
                    try:
                        _w = getattr(threading.current_thread(), bstack1ll11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫீ"), None)
                        if _w and hasattr(_w, bstack1ll11_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡥࡰࡢࡩࡨࠫு")):
                            _w.update_page(page)
                        if _w and not _w.session_id:
                            try:
                                import json as _json
                                result = page.evaluate(
                                    bstack1ll11_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣூ"), bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡩࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡉ࡫ࡴࡢ࡫࡯ࡷࠧࢃࠧ௃"))
                                if isinstance(result, str):
                                    result = _json.loads(result)
                                if isinstance(result, dict):
                                    sid = result.get(bstack1ll11_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ௄")) or result.get(bstack1ll11_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠧ௅")) or result.get(bstack1ll11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡎࡪࠧெ"))
                                    if sid:
                                        import threading as _1111l1l1l1_opy_
                                        from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
                                        with PlaywrightDriverWrapperDirect._session_ids_lock:
                                            PlaywrightDriverWrapperDirect._session_ids[_1111l1l1l1_opy_.get_ident()] = sid
                                        logger.debug(bstack1ll11_opy_ (u"ࠧࡉࡡࡱࡶࡸࡶࡪࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠤࡻ࡯ࡡࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࠩࡸࠨே"), sid)
                                        PlaywrightDriverWrapperDirect._send_cbt_info_on_session()
                                    else:
                                        logger.debug(bstack1ll11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠠࡨࡧࡷࡗࡪࡹࡳࡪࡱࡱࡈࡪࡺࡡࡪ࡮ࡶࠤࡷ࡫ࡴࡶࡴࡱࡩࡩࠦ࡮ࡰࠢࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࡀࠠࠦࡵࠥை"), result)
                                else:
                                    logger.debug(bstack1ll11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲࠡࡩࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡉ࡫ࡴࡢ࡫࡯ࡷࠥࡸࡥࡴࡷ࡯ࡸ࠿ࠦࠥࡴࠤ௉"), result)
                            except Exception as _1l1ll1ll1_opy_:
                                logger.debug(bstack1ll11_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠥ࡬ࡡ࡭࡮ࡥࡥࡨࡱࠠࡷ࡫ࡤࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࠥࡴࠤொ"), _1l1ll1ll1_opy_)
                        if (getattr(threading.current_thread(), bstack1ll11_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨோ"), None)
                                and not getattr(threading.current_thread(), bstack1ll11_opy_ (u"ࠪࡥ࠶࠷ࡹࡠࡵࡷࡥࡷࡺࡥࡥࠩௌ"), False)):
                            threading.current_thread().a11y_started = True
                            try:
                                from bstack_utils import accessibility as _111111ll_opy_
                                bstack1ll11l1ll_opy_ = getattr(threading.current_thread(), bstack1ll11_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ்"), True)
                                _111111ll_opy_.start_test_capture(_w, bstack1ll11l1ll_opy_)
                            except Exception:
                                logger.debug(bstack1ll11_opy_ (u"ࠧࡊࡥࡧࡧࡵࡶࡪࡪࠠࡂ࠳࠴ࡽࠥࡹࡴࡢࡴࡷࡣࡹ࡫ࡳࡵࡡࡦࡥࡵࡺࡵࡳࡧࠣࡪࡦ࡯࡬ࡦࡦࠥ௎"))
                    except Exception as exc:
                        logger.debug(bstack1ll11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡸࡴࡩࡧࡴࡦࠢࡳࡥ࡬࡫ࠠࡪࡰࠣࡻࡷࡧࡰࡱࡧࡵ࠾ࠥࠫࡳࠣ௏"), exc)
                    return page
                bstack1l11111111_opy_.new_page = _11l11ll1l_opy_
                bstack1l11111111_opy_._bstack_new_page_patched = True
        except Exception as exc:
            logger.debug(bstack1ll11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡺࡣࡩࠢࡖࡽࡳࡩࡂࡳࡱࡺࡷࡪࡸ࠮࡯ࡧࡺࡣࡵࡧࡧࡦࠢࡩࡳࡷࠦࡰࡢࡩࡨࠤࡨࡧࡰࡵࡷࡵࡩ࠿ࠦࠥࡴࠤௐ"), exc)
        try:
            from playwright.sync_api import Page as bstack111llll1_opy_, Browser as _11ll1l11l_opy_
            if not hasattr(bstack111llll1_opy_, bstack1ll11_opy_ (u"ࠨࡡࡥࡷࡹࡧࡣ࡬ࡡࡳࡥ࡬࡫࡟ࡤ࡮ࡲࡷࡪࡥࡰࡢࡶࡦ࡬ࡪࡪࠧ௑")):
                _111lll11l_opy_ = bstack111llll1_opy_.close
                def _1111l1ll1l_opy_(bstack1lll1ll1l1_opy_, *bstack1ll11111ll_opy_, _bstack_sdk_close=False, **bstack1ll111111l_opy_):
                    if not _bstack_sdk_close:
                        logger.debug(bstack1ll11_opy_ (u"ࠤࡇࡩ࡫࡫ࡲࡳࡧࡧࠤࡵࡧࡧࡦ࠰ࡦࡰࡴࡹࡥࠩࠫࠣ⠘ࠥࡽࡩ࡭࡮ࠣࡧࡱࡵࡳࡦࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨ௒"))
                        threading.current_thread().bstack_deferred_page_close = True
                        threading.current_thread().bstack_deferred_page_ref = bstack1lll1ll1l1_opy_
                        return
                    return _111lll11l_opy_(bstack1lll1ll1l1_opy_, *bstack1ll11111ll_opy_, **bstack1ll111111l_opy_)
                bstack111llll1_opy_.close = _1111l1ll1l_opy_
                bstack111llll1_opy_._bstack_page_close_patched = True
            if not hasattr(_11ll1l11l_opy_, bstack1ll11_opy_ (u"ࠪࡣࡧࡹࡴࡢࡥ࡮ࡣࡧࡸ࡯ࡸࡵࡨࡶࡤࡩ࡬ࡰࡵࡨࡣࡵࡧࡴࡤࡪࡨࡨࠬ௓")):
                _1llll1111_opy_ = _11ll1l11l_opy_.close
                def _1ll11l1l1_opy_(bstack111lll11l1_opy_, *bstack11l1111l_opy_, _bstack_sdk_close=False, **bstack1llll1lll_opy_):
                    if not _bstack_sdk_close:
                        logger.debug(bstack1ll11_opy_ (u"ࠦࡉ࡫ࡦࡦࡴࡵࡩࡩࠦࡢࡳࡱࡺࡷࡪࡸ࠮ࡤ࡮ࡲࡷࡪ࠮ࠩࠡ⠖ࠣࡻ࡮ࡲ࡬ࠡࡥ࡯ࡳࡸ࡫ࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦ௔"))
                        threading.current_thread().bstack_deferred_browser_close = True
                        threading.current_thread().bstack_deferred_browser_ref = bstack111lll11l1_opy_
                        return
                    return _1llll1111_opy_(bstack111lll11l1_opy_, *bstack11l1111l_opy_, **bstack1llll1lll_opy_)
                _11ll1l11l_opy_.close = _1ll11l1l1_opy_
                _11ll1l11l_opy_._bstack_browser_close_patched = True
            if not hasattr(bstack111llll1_opy_, bstack1ll11_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡢࡴࡦࡺࡣࡩࡧࡧࠫ௕")):
                _1ll11ll1_opy_ = bstack111llll1_opy_.screenshot
                def _11l111lll_opy_(bstack1lll1ll1l1_opy_, *bstack1ll11l11l_opy_, **bstack1lll1l1l11_opy_):
                    result = _1ll11ll1_opy_(bstack1lll1ll1l1_opy_, *bstack1ll11l11l_opy_, **bstack1lll1l1l11_opy_)
                    try:
                        from bstack_utils.testhub_handler import TestHubHandler
                        from bstack_utils.bstack111l111l_opy_ import bstack11l11l1lll_opy_
                        if bstack11l11l1lll_opy_.on():
                            import base64
                            if isinstance(result, bytes):
                                bstack11l111l1ll_opy_ = base64.b64encode(result).decode(bstack1ll11_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬ௖"))
                            else:
                                bstack11l111l1ll_opy_ = str(result)
                            test_uuid = TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack11l11l1lll_opy_.current_hook_uuid()
                            if test_uuid and bstack11l111l1ll_opy_:
                                TestHubHandler.bstack1ll1llll_opy_({
                                    bstack1ll11_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭ௗ"): bstack11l111l1ll_opy_,
                                    bstack1ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ௘"): test_uuid
                                })
                                logger.debug(bstack1ll11_opy_ (u"ࠤࡖࡩࡳࡺࠠࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠡࡶࡲࠤࡔ࠷࠱ࡺࠢࡩࡳࡷࠦࡴࡦࡵࡷࠤࢀࢃࠢ௙").format(test_uuid))
                    except Exception as bstack111l11ll11_opy_:
                        logger.debug(bstack1ll11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡰࡧࠤࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠥࡺ࡯ࠡࡑ࠴࠵ࡾࡀࠠࡼࡿࠥ௚").format(str(bstack111l11ll11_opy_)))
                    return result
                bstack111llll1_opy_.screenshot = _11l111lll_opy_
                bstack111llll1_opy_._bstack_screenshot_patched = True
        except Exception as exc:
            logger.debug(bstack1ll11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡧࠣࡨࡪ࡬ࡥࡳࡴࡨࡨࠥࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡦࡰࡴࡹࡥࠡࡪࡲࡳࡰࡹ࠺ࠡࠧࡶࠦ௛"), exc)
        logger.debug(bstack1ll11_opy_ (u"ࠧࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡆࡵ࡭ࡻ࡫ࡲࡘࡴࡤࡴࡵ࡫ࡲࡅ࡫ࡵࡩࡨࡺࠠࡴࡧࡷࡹࡵࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࠡࡨࡲࡶࠥࡺࡨࡳࡧࡤࡨࠥࢁࡽࠣ௜").format(threading.get_ident()))
    except Exception as e:
        logger.debug(bstack1ll11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡽࡲࡢࡲࡳࡩࡷࡀࠠࡼࡿࠥ௝").format(str(e)))
    return browser
  async def bstack1ll111l11l_opy_(self, *args, **kwargs):
    global bstack111llll11_opy_, CONFIG, FRAMEWORK_NAME, __version__, BROWSERSTACK_AUTOMATION
    global PLATFORM_INDEX, PARALLELISE_VANILLA_PYTHON, PARALLELISE_THREADING_PYTHON, SESSION_NAME
    import urllib.parse as _1111ll1ll1_opy_
    import json
    ws_endpoint = args[0] if args else kwargs.get(bstack1ll11_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫ௞"), kwargs.get(bstack1ll11_opy_ (u"ࠨࡹࡶࡣࡪࡴࡤࡱࡱ࡬ࡲࡹ࠭௟"), bstack1ll11_opy_ (u"ࠩࠪ௠")))
    bstack1l11l1l1l1_opy_ = (ws_endpoint
                 and bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭௡") in str(ws_endpoint)
                 and bstack1ll11_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ௢") in str(ws_endpoint))
    bstack11l1111l1_opy_ = {}
    if bstack1l11l1l1l1_opy_:
        from bstack_utils.helper import bstack1l111l1111_opy_
        bstack11l1llllll_opy_ = bstack1l111l1111_opy_()
        try:
            if bstack11l1llllll_opy_:
                CONFIG[bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ௣")] = str(FRAMEWORK_NAME) + str(__version__)
                bstack1l11l1l1_opy_ = os.environ.get(bstack1ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ௤"), bstack1ll11_opy_ (u"ࠧࠨ௥"))
                if bstack1l11l1l1_opy_:
                    CONFIG[bstack1ll11_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ௦")] = bstack1l11l1l1_opy_
                CONFIG[bstack1ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ௧")] = TestHubUtils.bstack11ll1l111_opy_(CONFIG, FRAMEWORK_NAME)
                bstack11111lll1_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
                try:
                    if PARALLELISE_VANILLA_PYTHON is True:
                        bstack11111lll1_opy_ = int(multiprocessing.current_process().name)
                    elif PARALLELISE_THREADING_PYTHON is True:
                        bstack11111lll1_opy_ = int(threading.current_thread().name)
                except Exception:
                    bstack11111lll1_opy_ = 0
                CONFIG[bstack1ll11_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤ௨")] = True
                bstack11l1111l1_opy_ = get_caps(CONFIG, bstack11111lll1_opy_)
                if CONFIG.get(bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ௩")):
                    update_caps_for_local(bstack11l1111l1_opy_)
                if bstack1ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ௪") in CONFIG and bstack1ll11_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ௫") in CONFIG[bstack1ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ௬")][bstack11111lll1_opy_]:
                    SESSION_NAME = CONFIG[bstack1ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ௭")][bstack11111lll1_opy_][bstack1ll11_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ௮")]
                logger.debug(bstack1ll11_opy_ (u"ࠥࡇࡦࡹࡥࠡࡃ࠽ࠤࡗ࡫ࡰ࡭ࡣࡦࡩࡩࠦࡵࡴࡧࡵࠤࡨࡧࡰࡴࠢࡺ࡭ࡹ࡮ࠠࡺ࡯࡯ࠤࡨࡧࡰࡴ࠼ࠣࡿࢂࠨ௯").format(str(bstack11l1111l1_opy_)))
            else:
                bstack1llll1l1_opy_ = str(ws_endpoint).split(bstack1ll11_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ௰"))[1]
                bstack11l1111l1_opy_ = json.loads(_1111ll1ll1_opy_.unquote(bstack1llll1l1_opy_))
                bstack11l1111l1_opy_ = bstack11l1111l1_opy_ or {}
                bstack1l11l1l1_opy_ = os.environ.get(bstack1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ௱"), bstack1ll11_opy_ (u"࠭ࠧ௲"))
                bstack1ll1lll11_opy_ = TestHubUtils.bstack11ll1l111_opy_(CONFIG, FRAMEWORK_NAME)
                bstack11l1111l1_opy_[bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ௳")] = str(FRAMEWORK_NAME) + str(__version__)
                bstack11l1111l1_opy_[bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ௴")] = BROWSERSTACK_AUTOMATION
                if bstack1l11l1l1_opy_:
                    bstack11l1111l1_opy_[bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ௵")] = bstack1l11l1l1_opy_
                bstack11l1111l1_opy_[bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ௶")] = bstack1ll1lll11_opy_
                logger.debug(bstack1ll11_opy_ (u"ࠦࡈࡧࡳࡦࠢࡇ࠾ࠥࡓࡥࡳࡩࡨࡨ࡙ࠥࡄࡌࠢࡷࡩࡱ࡫࡭ࡦࡶࡵࡽࠥ࡯࡮ࡵࡱࠣࡹࡸ࡫ࡲࠡࡥࡤࡴࡸࠨ௷"))
            ws_url = str(ws_endpoint).split(bstack1ll11_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫ௸"))[0]
            ws_endpoint = ws_url + bstack1ll11_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬ௹") + _1111ll1ll1_opy_.quote(json.dumps(bstack11l1111l1_opy_))
            if args:
                args = (ws_endpoint,) + args[1:]
            else:
                if bstack1ll11_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫ௺") in kwargs:
                    kwargs[bstack1ll11_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬ௻")] = ws_endpoint
                else:
                    kwargs[bstack1ll11_opy_ (u"ࠩࡺࡷࡤ࡫࡮ࡥࡲࡲ࡭ࡳࡺࠧ௼")] = ws_endpoint
            logger.debug(bstack1ll11_opy_ (u"ࠥࡐࡪ࡭ࡡࡤࡻࠣࡧࡴࡴ࡮ࡦࡥࡷࠤ࡚ࡘࡌࠡࡷࡳࡨࡦࡺࡥࡥࠢࡺ࡭ࡹ࡮ࠠࡼࡿࠣࡧࡦࡶࡳࠣ௽").format(bstack1ll11_opy_ (u"ࠦࡾࡳ࡬ࠣ௾") if bstack11l1llllll_opy_ else bstack1ll11_opy_ (u"ࠧࡺࡥ࡭ࡧࡰࡩࡹࡸࡹࠣ௿")))
        except Exception as e:
            logger.debug(bstack1ll11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡩࡷ࡭ࡥࠡࡥࡤࡴࡸࠦࡩ࡯ࡶࡲࠤࡨࡵ࡮࡯ࡧࡦࡸ࡛ࠥࡒࡍ࠼ࠣࡿࢂࠨఀ").format(str(e)))
        try:
            from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
            PlaywrightDriverWrapperDirect.setup_dispatch_capture()
        except Exception as exc:
            logger.debug(bstack1ll11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠤࡨࡧࡰࡵࡷࡵࡩࠥ࡯࡮ࠡ࡯ࡲࡨࡤࡩ࡯࡯ࡰࡨࡧࡹࡀࠠࠦࡵࠥఁ"), exc)
    browser = await bstack111llll11_opy_(self, *args, **kwargs)
    if bstack1l11l1l1l1_opy_:
        try:
            from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
            wrapper = PlaywrightDriverWrapperDirect(browser, page=None, capabilities=bstack11l1111l1_opy_, config=CONFIG)
            threading.current_thread().bstackSessionDriver = wrapper
            logger.debug(bstack1ll11_opy_ (u"ࠣࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡉࡸࡩࡷࡧࡵ࡛ࡷࡧࡰࡱࡧࡵࡈ࡮ࡸࡥࡤࡶࠣࡷࡪࡺࡵࡱࠢࡦࡳࡲࡶ࡬ࡦࡶࡨࠤ࡫ࡵࡲࠡࡶ࡫ࡶࡪࡧࡤࠡࠧࡶࠦం"), threading.get_ident())
            threading.current_thread().bstackTestErrorMessages = []
            if wrapper.session_id and not wrapper._cbt_info_sent:
                PlaywrightDriverWrapperDirect._send_cbt_info_on_session()
            try:
                from playwright.sync_api import Browser as bstack1l11111111_opy_
                if not hasattr(bstack1l11111111_opy_, bstack1ll11_opy_ (u"ࠩࡢࡦࡸࡺࡡࡤ࡭ࡢࡲࡪࡽ࡟ࡱࡣࡪࡩࡤࡶࡡࡵࡥ࡫ࡩࡩ࠭ః")):
                    _11l111l11_opy_ = bstack1l11111111_opy_.new_page
                    def _11l11ll1l_opy_(bstack111lll11l1_opy_, *bstack11l1l1l11l_opy_, **bstack1l11ll1l1l_opy_):
                        page = _11l111l11_opy_(bstack111lll11l1_opy_, *bstack11l1l1l11l_opy_, **bstack1l11ll1l1l_opy_)
                        try:
                            _w = getattr(threading.current_thread(), bstack1ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩఄ"), None)
                            if _w and hasattr(_w, bstack1ll11_opy_ (u"ࠫࡺࡶࡤࡢࡶࡨࡣࡵࡧࡧࡦࠩఅ")):
                                _w.update_page(page)
                        except Exception as exc:
                            logger.debug(bstack1ll11_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡷࡳࡨࡦࡺࡥࠡࡲࡤ࡫ࡪࠦࡩ࡯ࠢࡺࡶࡦࡶࡰࡦࡴࠣࠬࡲࡵࡤࡠࡥࡲࡲࡳ࡫ࡣࡵࠫ࠽ࠤࠪࡹࠢఆ"), exc)
                        return page
                    bstack1l11111111_opy_.new_page = _11l11ll1l_opy_
                    bstack1l11111111_opy_._bstack_new_page_patched = True
            except Exception as exc:
                logger.debug(bstack1ll11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡹࡩࡨࠡࡕࡼࡲࡨࡈࡲࡰࡹࡶࡩࡷ࠴࡮ࡦࡹࡢࡴࡦ࡭ࡥࠡ࡫ࡱࠤࡲࡵࡤࡠࡥࡲࡲࡳ࡫ࡣࡵ࠼ࠣࠩࡸࠨఇ"), exc)
            try:
                from playwright.sync_api import Page as bstack111llll1_opy_, Browser as _11ll1l11l_opy_
                if not hasattr(bstack111llll1_opy_, bstack1ll11_opy_ (u"ࠧࡠࡤࡶࡸࡦࡩ࡫ࡠࡲࡤ࡫ࡪࡥࡣ࡭ࡱࡶࡩࡤࡶࡡࡵࡥ࡫ࡩࡩ࠭ఈ")):
                    _111lll11l_opy_ = bstack111llll1_opy_.close
                    def _1111l1ll1l_opy_(bstack1lll1ll1l1_opy_, *bstack1ll11111ll_opy_, _bstack_sdk_close=False, **bstack1ll111111l_opy_):
                        if not _bstack_sdk_close:
                            logger.debug(bstack1ll11_opy_ (u"ࠣࡆࡨࡪࡪࡸࡲࡦࡦࠣࡴࡦ࡭ࡥ࠯ࡥ࡯ࡳࡸ࡫ࠨࠪࠢ⠗ࠤࡼ࡯࡬࡭ࠢࡦࡰࡴࡹࡥࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧఉ"))
                            threading.current_thread().bstack_deferred_page_close = True
                            threading.current_thread().bstack_deferred_page_ref = bstack1lll1ll1l1_opy_
                            return
                        return _111lll11l_opy_(bstack1lll1ll1l1_opy_, *bstack1ll11111ll_opy_, **bstack1ll111111l_opy_)
                    bstack111llll1_opy_.close = _1111l1ll1l_opy_
                    bstack111llll1_opy_._bstack_page_close_patched = True
                if not hasattr(_11ll1l11l_opy_, bstack1ll11_opy_ (u"ࠩࡢࡦࡸࡺࡡࡤ࡭ࡢࡦࡷࡵࡷࡴࡧࡵࡣࡨࡲ࡯ࡴࡧࡢࡴࡦࡺࡣࡩࡧࡧࠫఊ")):
                    _1llll1111_opy_ = _11ll1l11l_opy_.close
                    def _1ll11l1l1_opy_(bstack111lll11l1_opy_, *bstack11l1111l_opy_, _bstack_sdk_close=False, **bstack1llll1lll_opy_):
                        if not _bstack_sdk_close:
                            logger.debug(bstack1ll11_opy_ (u"ࠥࡈࡪ࡬ࡥࡳࡴࡨࡨࠥࡨࡲࡰࡹࡶࡩࡷ࠴ࡣ࡭ࡱࡶࡩ࠭࠯ࠠ⠕ࠢࡺ࡭ࡱࡲࠠࡤ࡮ࡲࡷࡪࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥఋ"))
                            threading.current_thread().bstack_deferred_browser_close = True
                            threading.current_thread().bstack_deferred_browser_ref = bstack111lll11l1_opy_
                            return
                        return _1llll1111_opy_(bstack111lll11l1_opy_, *bstack11l1111l_opy_, **bstack1llll1lll_opy_)
                    _11ll1l11l_opy_.close = _1ll11l1l1_opy_
                    _11ll1l11l_opy_._bstack_browser_close_patched = True
                if not hasattr(bstack111llll1_opy_, bstack1ll11_opy_ (u"ࠫࡤࡨࡳࡵࡣࡦ࡯ࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡡࡳࡥࡹࡩࡨࡦࡦࠪఌ")):
                    _1ll11ll1_opy_ = bstack111llll1_opy_.screenshot
                    def _11l111lll_opy_(bstack1lll1ll1l1_opy_, *bstack1ll11l11l_opy_, **bstack1lll1l1l11_opy_):
                        result = _1ll11ll1_opy_(bstack1lll1ll1l1_opy_, *bstack1ll11l11l_opy_, **bstack1lll1l1l11_opy_)
                        try:
                            from bstack_utils.testhub_handler import TestHubHandler
                            from bstack_utils.bstack111l111l_opy_ import bstack11l11l1lll_opy_
                            if bstack11l11l1lll_opy_.on():
                                import base64
                                if isinstance(result, bytes):
                                    bstack11l111l1ll_opy_ = base64.b64encode(result).decode(bstack1ll11_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫ఍"))
                                else:
                                    bstack11l111l1ll_opy_ = str(result)
                                test_uuid = TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack11l11l1lll_opy_.current_hook_uuid()
                                if test_uuid and bstack11l111l1ll_opy_:
                                    TestHubHandler.bstack1ll1llll_opy_({
                                        bstack1ll11_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬఎ"): bstack11l111l1ll_opy_,
                                        bstack1ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧఏ"): test_uuid
                                    })
                        except Exception as bstack111l11ll11_opy_:
                            logger.debug(bstack1ll11_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫࡮ࡥࠢࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠣࡸࡴࠦࡏ࠲࠳ࡼࠤ࠭ࡳ࡯ࡥࡡࡦࡳࡳࡴࡥࡤࡶࠬ࠾ࠥࠫࡳࠣఐ"), bstack111l11ll11_opy_)
                        return result
                    bstack111llll1_opy_.screenshot = _11l111lll_opy_
                    bstack111llll1_opy_._bstack_screenshot_patched = True
            except Exception as exc:
                logger.debug(bstack1ll11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡥࠡࡦࡨࡪࡪࡸࡲࡦࡦࠣࡧࡱࡵࡳࡦࠢ࡫ࡳࡴࡱࡳࠡ࡫ࡱࠤࡲࡵࡤࡠࡥࡲࡲࡳ࡫ࡣࡵ࠼ࠣࠩࡸࠨ఑"), exc)
            logger.debug(bstack1ll11_opy_ (u"ࠥࡐࡪ࡭ࡡࡤࡻࠣࡧࡴࡴ࡮ࡦࡥࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡺࡲࡢࡥ࡮࡭ࡳ࡭ࠠࡴࡧࡷࡹࡵࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࠡࡨࡲࡶࠥࡺࡨࡳࡧࡤࡨࠥࢁࡽࠣఒ").format(threading.get_ident()))
        except Exception as e:
            logger.debug(bstack1ll11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦ࡬ࡦࡩࡤࡧࡾࠦࡣࡰࡰࡱࡩࡨࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡶࡵࡥࡨࡱࡩ࡯ࡩ࠽ࠤࢀࢃࠢఓ").format(str(e)))
    return browser
except Exception as e:
    pass
def patch_playwright():
    global SELENIUM_OR_PLAYWRIGHT_INSTALLED
    global FRAMEWORK_NAME
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l111l1111_opy_
        global bstack111llll11_opy_
        if not bstack111llll11_opy_:
            bstack111llll11_opy_ = BrowserType.connect
        BrowserType.connect = bstack1ll111l11l_opy_
        if bstack1l111l1111_opy_():
            BrowserType.launch = bstack1l11111l1_opy_
            SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
        try:
            from playwright.sync_api._context_manager import PlaywrightContextManager
            if not hasattr(PlaywrightContextManager, bstack1ll11_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥࡥ࡯ࡶࡨࡶࡤࡶࡡࡵࡥ࡫ࡩࡩ࠭ఔ")):
                _11111lllll_opy_ = PlaywrightContextManager.__enter__
                def _1l111ll111_opy_(bstack1l11ll11l1_opy_):
                    pw = _11111lllll_opy_(bstack1l11ll11l1_opy_)
                    _1l1l11lll_opy_ = pw.stop
                    _111ll1llll_opy_ = threading.current_thread()
                    _111ll1llll_opy_.bstack_deferred_pw_ref = pw
                    _111ll1llll_opy_.bstack_deferred_pw_stop_fn = _1l1l11lll_opy_
                    def _1111111lll_opy_(*args, _bstack_sdk_close=False, **kwargs):
                        if not _bstack_sdk_close:
                            logger.debug(bstack1ll11_opy_ (u"ࠨࡄࡦࡨࡨࡶࡷ࡫ࡤࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠳ࡹࡴࡰࡲࠫ࠭ࠥ⠚ࠠࡸ࡫࡯ࡰࠥࡹࡴࡰࡲࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢక"))
                            threading.current_thread().bstack_deferred_pw_stop = True
                            return
                        return _1l1l11lll_opy_()
                    pw.stop = _1111111lll_opy_
                    return pw
                PlaywrightContextManager.__enter__ = _1l111ll111_opy_
                PlaywrightContextManager._bstack_enter_patched = True
        except Exception as e:
            logger.debug(bstack1ll11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡺࡣࡩࠢࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡉ࡯࡯ࡶࡨࡼࡹࡓࡡ࡯ࡣࡪࡩࡷ࠴࡟ࡠࡧࡱࡸࡪࡸ࡟ࡠ࠼ࠣࠩࡸࠨఖ"), e)
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1ll1lll1l1_opy_
      SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
    except Exception as e:
      pass
def playwright_set_session_name(context, bstack111ll11111_opy_):
  try:
    if getattr(context, bstack1ll11_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭గ"), None):
      context.page.evaluate(bstack1ll11_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥఘ"), bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠧఙ")+ json.dumps(bstack111ll11111_opy_) + bstack1ll11_opy_ (u"ࠦࢂࢃࠢచ"))
  except Exception as e:
    logger.debug(bstack1ll11_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡼࡿ࠽ࠤࢀࢃࠢఛ").format(str(e), traceback.format_exc()))
def playwright_annotate(context, message, level):
  try:
    if getattr(context, bstack1ll11_opy_ (u"࠭ࡰࡢࡩࡨࠫజ"), None):
      context.page.evaluate(bstack1ll11_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣఝ"), bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ఞ") + json.dumps(message) + bstack1ll11_opy_ (u"ࠩ࠯ࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠬట") + json.dumps(level) + bstack1ll11_opy_ (u"ࠪࢁࢂ࠭ఠ"))
  except Exception as e:
    logger.debug(bstack1ll11_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡢࡰࡱࡳࡹࡧࡴࡪࡱࡱࠤࢀࢃ࠺ࠡࡽࢀࠦడ").format(str(e), traceback.format_exc()))
@measure(event_name=EVENTS.bstack1ll111111_opy_, stage=STAGE.bstack11111llll_opy_, bstack11lll1l111_opy_=SESSION_NAME)
def bstack111111ll1l_opy_(self, url):
  global bstack111111l1l1_opy_
  try:
    bstack1111ll1l1_opy_(url)
  except Exception as err:
    logger.debug(bstack11l111111l_opy_.format(str(err)))
  try:
    bstack111111l1l1_opy_(self, url)
  except Exception as e:
    try:
      parsed_error = str(e)
      if any(err_msg in parsed_error for err_msg in bstack1lll1ll11l_opy_):
        bstack1111ll1l1_opy_(url, True)
    except Exception as err:
      logger.debug(bstack11l111111l_opy_.format(str(err)))
    raise e
def bstack1l11lll1_opy_(self):
  global bstack1lll11ll11_opy_
  bstack1lll11ll11_opy_ = self
  return
def bstack11l1111l11_opy_(self):
  global bstack1l1l1l1l_opy_
  bstack1l1l1l1l_opy_ = self
  return
def bstack1llllll1ll_opy_(test_name, bstack111lll1l11_opy_):
  global CONFIG
  if percy.bstack1lllll1l1_opy_() == bstack1ll11_opy_ (u"ࠧࡺࡲࡶࡧࠥఢ"):
    bstack111l1ll1l_opy_ = os.path.relpath(bstack111lll1l11_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack111l1ll1l_opy_)
    bstack11lll1l111_opy_ = suite_name + bstack1ll11_opy_ (u"ࠨ࠭ࠣణ") + test_name
    threading.current_thread().percySessionName = bstack11lll1l111_opy_
def bstack1lllllll11_opy_(self, test, *args, **kwargs):
  global bstack11111ll1l_opy_
  test_name = None
  bstack111lll1l11_opy_ = None
  if test:
    test_name = str(test.name)
    bstack111lll1l11_opy_ = str(test.source)
  bstack1llllll1ll_opy_(test_name, bstack111lll1l11_opy_)
  bstack11111ll1l_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.bstack11ll1111l_opy_, stage=STAGE.bstack11111llll_opy_, bstack11lll1l111_opy_=SESSION_NAME)
def bstack11l1lll111_opy_(driver, bstack11lll1l111_opy_):
  if not bstack11l1l1lll_opy_ and bstack11lll1l111_opy_:
      bstack1lll111111_opy_ = {
          bstack1ll11_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧత"): bstack1ll11_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩథ"),
          bstack1ll11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬద"): {
              bstack1ll11_opy_ (u"ࠪࡲࡦࡳࡥࠨధ"): bstack11lll1l111_opy_
          }
      }
      bstack1llll11l11_opy_ = bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩన").format(json.dumps(bstack1lll111111_opy_))
      driver.execute_script(bstack1llll11l11_opy_)
  if bstack1l1llll1l_opy_:
      bstack11ll11lll_opy_ = {
          bstack1ll11_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬ఩"): bstack1ll11_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨప"),
          bstack1ll11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪఫ"): {
              bstack1ll11_opy_ (u"ࠨࡦࡤࡸࡦ࠭బ"): bstack11lll1l111_opy_ + bstack1ll11_opy_ (u"ࠩࠣࡴࡦࡹࡳࡦࡦࠤࠫభ"),
              bstack1ll11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩమ"): bstack1ll11_opy_ (u"ࠫ࡮ࡴࡦࡰࠩయ")
          }
      }
      if bstack1l1llll1l_opy_.status == bstack1ll11_opy_ (u"ࠬࡖࡁࡔࡕࠪర"):
          bstack111l1lll1l_opy_ = bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫఱ").format(json.dumps(bstack11ll11lll_opy_))
          driver.execute_script(bstack111l1lll1l_opy_)
          bstack11l11l111l_opy_(driver, bstack1ll11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧల"))
      elif bstack1l1llll1l_opy_.status == bstack1ll11_opy_ (u"ࠨࡈࡄࡍࡑ࠭ళ"):
          reason = bstack1ll11_opy_ (u"ࠤࠥఴ")
          bstack11l11lllll_opy_ = bstack11lll1l111_opy_ + bstack1ll11_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠫవ")
          if bstack1l1llll1l_opy_.message:
              reason = str(bstack1l1llll1l_opy_.message)
              bstack11l11lllll_opy_ = bstack11l11lllll_opy_ + bstack1ll11_opy_ (u"ࠫࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠫశ") + reason
          bstack11ll11lll_opy_[bstack1ll11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨష")] = {
              bstack1ll11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬస"): bstack1ll11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭హ"),
              bstack1ll11_opy_ (u"ࠨࡦࡤࡸࡦ࠭఺"): bstack11l11lllll_opy_
          }
          bstack111l1lll1l_opy_ = bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧ఻").format(json.dumps(bstack11ll11lll_opy_))
          driver.execute_script(bstack111l1lll1l_opy_)
          bstack11l11l111l_opy_(driver, bstack1ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦ఼ࠪ"), reason)
          bstack1l1ll11l_opy_(reason, str(bstack1l1llll1l_opy_), str(PLATFORM_INDEX), logger)
@measure(event_name=EVENTS.bstack1l11l1ll11_opy_, stage=STAGE.bstack11111llll_opy_, bstack11lll1l111_opy_=SESSION_NAME)
def bstack1ll1l11ll1_opy_(driver, test):
  if percy.bstack1lllll1l1_opy_() == bstack1ll11_opy_ (u"ࠦࡹࡸࡵࡦࠤఽ") and percy.bstack11l11l11l1_opy_() == bstack1ll11_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢా"):
      bstack1111lll11_opy_ = bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"࠭ࡰࡦࡴࡦࡽࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩి"), None)
      bstack11lll111l1_opy_(driver, bstack1111lll11_opy_, test)
  if (bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫీ"), None) and
      bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧు"), None)) or (
      bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩూ"), None) and
      bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬృ"), None)):
      logger.info(bstack1ll11_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠢࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡮ࡹࠠࡶࡰࡧࡩࡷࡽࡡࡺ࠰ࠣࠦౄ"))
      a11y.bstack1l1l1ll1l_opy_(driver, name=test.name, path=test.source)
def bstack1ll1lll111_opy_(test, bstack11lll1l111_opy_):
    try:
      bstack11l111ll1_opy_ = datetime.datetime.now()
      data = {}
      if test:
        data[bstack1ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ౅")] = bstack11lll1l111_opy_
      if bstack1l1llll1l_opy_:
        if bstack1l1llll1l_opy_.status == bstack1ll11_opy_ (u"࠭ࡐࡂࡕࡖࠫె"):
          data[bstack1ll11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧే")] = bstack1ll11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨై")
        elif bstack1l1llll1l_opy_.status == bstack1ll11_opy_ (u"ࠩࡉࡅࡎࡒࠧ౉"):
          data[bstack1ll11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪొ")] = bstack1ll11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫో")
          if bstack1l1llll1l_opy_.message:
            data[bstack1ll11_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬౌ")] = str(bstack1l1llll1l_opy_.message)
      user = CONFIG[bstack1ll11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ్")]
      key = CONFIG[bstack1ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ౎")]
      host = bstack1l11llll11_opy_(cli.config, [bstack1ll11_opy_ (u"ࠣࡣࡳ࡭ࡸࠨ౏"), bstack1ll11_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨࠦ౐"), bstack1ll11_opy_ (u"ࠥࡥࡵ࡯ࠢ౑")], bstack1ll11_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠧ౒"))
      url = bstack1ll11_opy_ (u"ࠬࢁࡽ࠰ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡷࡪࡹࡳࡪࡱࡱࡷ࠴ࢁࡽ࠯࡬ࡶࡳࡳ࠭౓").format(host, bstack1ll1l11l_opy_)
      headers = {
        bstack1ll11_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡵࡻࡳࡩࠬ౔"): bstack1ll11_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰౕࠪ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers, auth=(user, key))
        cli.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠣࡪࡷࡸࡵࡀࡵࡱࡦࡤࡸࡪࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡹࡴࡢࡶࡸࡷౖࠧ"), datetime.datetime.now() - bstack11l111ll1_opy_)
    except Exception as e:
      logger.error(bstack11lll11l_opy_.format(str(e)))
def bstack11l1l1111l_opy_(test, bstack11lll1l111_opy_):
  global CONFIG
  global bstack1l1l1l1l_opy_
  global bstack1lll11ll11_opy_
  global bstack1ll1l11l_opy_
  global bstack1l1llll1l_opy_
  global SESSION_NAME
  global bstack1ll1l1l1l1_opy_
  global bstack1l111l11l1_opy_
  global bstack11ll1lll_opy_
  global bstack1ll1111ll1_opy_
  global bstack11l1ll1l11_opy_
  global bstack1l11l1llll_opy_
  global bstack1l1ll1lll1_opy_
  try:
    if not bstack1ll1l11l_opy_:
      with bstack1l1ll1lll1_opy_:
        bstack11l11lll11_opy_ = os.path.join(os.path.expanduser(bstack1ll11_opy_ (u"ࠩࢁࠫ౗")), bstack1ll11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪౘ"), bstack1ll11_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭ౙ"))
        if os.path.exists(bstack11l11lll11_opy_):
          with open(bstack11l11lll11_opy_, bstack1ll11_opy_ (u"ࠬࡸࠧౚ")) as f:
            content = f.read().strip()
            if content:
              bstack1l11l111ll_opy_ = json.loads(bstack1ll11_opy_ (u"ࠨࡻࠣ౛") + content + bstack1ll11_opy_ (u"ࠧࠣࡺࠥ࠾ࠥࠨࡹࠣࠩ౜") + bstack1ll11_opy_ (u"ࠣࡿࠥౝ"))
              bstack1ll1l11l_opy_ = bstack1l11l111ll_opy_.get(str(threading.get_ident()))
  except Exception as e:
    logger.debug(bstack1ll11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡴࡨࡥࡩ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡍࡉࡹࠠࡧ࡫࡯ࡩ࠿ࠦࠧ౞") + str(e))
  if not is_robot_playwright_installed():
    if bstack11l1ll1l11_opy_:
      with bstack1llll1l1l_opy_:
        bstack1l1111l1l1_opy_ = bstack11l1ll1l11_opy_.copy()
      for driver in bstack1l1111l1l1_opy_:
        if bstack1ll1l11l_opy_ == driver.session_id:
          if test:
            bstack1ll1l11ll1_opy_(driver, test)
          bstack11l1lll111_opy_(driver, bstack11lll1l111_opy_)
    elif bstack1ll1l11l_opy_:
      bstack1ll1lll111_opy_(test, bstack11lll1l111_opy_)
    if bstack1l1l1l1l_opy_:
      bstack1l111l11l1_opy_(bstack1l1l1l1l_opy_)
    if bstack1lll11ll11_opy_:
      bstack11ll1lll_opy_(bstack1lll11ll11_opy_)
    if bstack11ll11l1l_opy_:
      bstack1ll1111ll1_opy_()
def bstack1llllllll_opy_(self, test, *args, **kwargs):
  bstack11lll1l111_opy_ = None
  if test:
    bstack11lll1l111_opy_ = str(test.name)
  bstack11l1l1111l_opy_(test, bstack11lll1l111_opy_)
  bstack1ll1l1l1l1_opy_(self, test, *args, **kwargs)
def bstack1ll1l1111l_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack11l1l1ll1l_opy_
  global CONFIG
  global bstack11l1ll1l11_opy_
  global bstack1ll1l11l_opy_
  global bstack1l1ll1lll1_opy_
  bstack1l1l11111_opy_ = None
  try:
    if bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ౟"), None) or bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ౠ"), None):
      try:
        if not bstack1ll1l11l_opy_:
          bstack11l11lll11_opy_ = os.path.join(os.path.expanduser(bstack1ll11_opy_ (u"ࠬࢄࠧౡ")), bstack1ll11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ౢ"), bstack1ll11_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩౣ"))
          with bstack1l1ll1lll1_opy_:
            if os.path.exists(bstack11l11lll11_opy_):
              with open(bstack11l11lll11_opy_, bstack1ll11_opy_ (u"ࠨࡴࠪ౤")) as f:
                content = f.read().strip()
                if content:
                  bstack1l11l111ll_opy_ = json.loads(bstack1ll11_opy_ (u"ࠤࡾࠦ౥") + content + bstack1ll11_opy_ (u"ࠪࠦࡽࠨ࠺ࠡࠤࡼࠦࠬ౦") + bstack1ll11_opy_ (u"ࠦࢂࠨ౧"))
                  bstack1ll1l11l_opy_ = bstack1l11l111ll_opy_.get(str(threading.get_ident()))
      except Exception as e:
        logger.debug(bstack1ll11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡷ࡫ࡡࡥ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡉࡅࡵࠣࡪ࡮ࡲࡥࠡ࡫ࡱࠤࡹ࡫ࡳࡵࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࠫ౨") + str(e))
      if bstack11l1ll1l11_opy_:
        with bstack1llll1l1l_opy_:
          bstack1l1111l1l1_opy_ = bstack11l1ll1l11_opy_.copy()
        for driver in bstack1l1111l1l1_opy_:
          if bstack1ll1l11l_opy_ == driver.session_id:
            bstack1l1l11111_opy_ = driver
    bstack1ll11l1ll_opy_ = a11y.is_enabled_testcase(test.tags)
    if bstack1l1l11111_opy_:
      threading.current_thread().isA11yTest = a11y.start_test_capture(bstack1l1l11111_opy_, bstack1ll11l1ll_opy_)
      threading.current_thread().isAppA11yTest = a11y.start_test_capture(bstack1l1l11111_opy_, bstack1ll11l1ll_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1ll11l1ll_opy_
      threading.current_thread().isAppA11yTest = bstack1ll11l1ll_opy_
  except:
    pass
  bstack11l1l1ll1l_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1l1llll1l_opy_
  try:
    bstack1l1llll1l_opy_ = self._test
  except:
    bstack1l1llll1l_opy_ = self.test
def bstack11111ll111_opy_():
  global bstack11l11ll1l1_opy_
  try:
    if os.path.exists(bstack11l11ll1l1_opy_):
      os.remove(bstack11l11ll1l1_opy_)
  except Exception as e:
    logger.debug(bstack1ll11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡦࡨࡰࡪࡺࡩ࡯ࡩࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺ࠡࠩ౩") + str(e))
def bstack11111l1111_opy_():
  global bstack11l11ll1l1_opy_
  bstack1l1l1lll_opy_ = {}
  lock_file = bstack11l11ll1l1_opy_ + bstack1ll11_opy_ (u"ࠧ࠯࡮ࡲࡧࡰ࠭౪")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1ll11_opy_ (u"ࠨࡨ࡬ࡰࡪࡲ࡯ࡤ࡭ࠣࡲࡴࡺࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧ࠯ࠤࡺࡹࡩ࡯ࡩࠣࡦࡦࡹࡩࡤࠢࡩ࡭ࡱ࡫ࠠࡰࡲࡨࡶࡦࡺࡩࡰࡰࡶࠫ౫"))
    try:
      if not os.path.isfile(bstack11l11ll1l1_opy_):
        with open(bstack11l11ll1l1_opy_, bstack1ll11_opy_ (u"ࠩࡺࠫ౬")) as f:
          json.dump({}, f)
      if os.path.exists(bstack11l11ll1l1_opy_):
        with open(bstack11l11ll1l1_opy_, bstack1ll11_opy_ (u"ࠪࡶࠬ౭")) as f:
          content = f.read().strip()
          if content:
            bstack1l1l1lll_opy_ = json.loads(content)
    except Exception as e:
      logger.debug(bstack1ll11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡲࡦࡣࡧ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭౮") + str(e))
    return bstack1l1l1lll_opy_
  try:
    os.makedirs(os.path.dirname(bstack11l11ll1l1_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      if not os.path.isfile(bstack11l11ll1l1_opy_):
        with open(bstack11l11ll1l1_opy_, bstack1ll11_opy_ (u"ࠬࡽࠧ౯")) as f:
          json.dump({}, f)
      if os.path.exists(bstack11l11ll1l1_opy_):
        with open(bstack11l11ll1l1_opy_, bstack1ll11_opy_ (u"࠭ࡲࠨ౰")) as f:
          content = f.read().strip()
          if content:
            bstack1l1l1lll_opy_ = json.loads(content)
  except Exception as e:
    logger.debug(bstack1ll11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡵࡩࡦࡪࡩ࡯ࡩࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺ࠡࠩ౱") + str(e))
  finally:
    return bstack1l1l1lll_opy_
def bstack1l11111ll1_opy_(platform_index, item_index):
  global bstack11l11ll1l1_opy_
  lock_file = bstack11l11ll1l1_opy_ + bstack1ll11_opy_ (u"ࠨ࠰࡯ࡳࡨࡱࠧ౲")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1ll11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡬ࡰࡥ࡮ࠤࡳࡵࡴࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨ࠰ࠥࡻࡳࡪࡰࡪࠤࡧࡧࡳࡪࡥࠣࡪ࡮ࡲࡥࠡࡱࡳࡩࡷࡧࡴࡪࡱࡱࡷࠬ౳"))
    try:
      bstack1l1l1lll_opy_ = {}
      if os.path.exists(bstack11l11ll1l1_opy_):
        with open(bstack11l11ll1l1_opy_, bstack1ll11_opy_ (u"ࠪࡶࠬ౴")) as f:
          content = f.read().strip()
          if content:
            bstack1l1l1lll_opy_ = json.loads(content)
      bstack1l1l1lll_opy_[item_index] = platform_index
      with open(bstack11l11ll1l1_opy_, bstack1ll11_opy_ (u"ࠦࡼࠨ౵")) as outfile:
        json.dump(bstack1l1l1lll_opy_, outfile)
    except Exception as e:
      logger.debug(bstack1ll11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡸࡴ࡬ࡸ࡮ࡴࡧࠡࡶࡲࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪ౶") + str(e))
    return
  try:
    os.makedirs(os.path.dirname(bstack11l11ll1l1_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      bstack1l1l1lll_opy_ = {}
      if os.path.exists(bstack11l11ll1l1_opy_):
        with open(bstack11l11ll1l1_opy_, bstack1ll11_opy_ (u"࠭ࡲࠨ౷")) as f:
          content = f.read().strip()
          if content:
            bstack1l1l1lll_opy_ = json.loads(content)
      bstack1l1l1lll_opy_[item_index] = platform_index
      with open(bstack11l11ll1l1_opy_, bstack1ll11_opy_ (u"ࠢࡸࠤ౸")) as outfile:
        json.dump(bstack1l1l1lll_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1ll11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡻࡷ࡯ࡴࡪࡰࡪࠤࡹࡵࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭౹") + str(e))
def bstack1l1l1l1ll_opy_(bstack1l1lll111l_opy_):
  global CONFIG
  bstack1ll1l11l11_opy_ = bstack1ll11_opy_ (u"ࠩࠪ౺")
  if not bstack1ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭౻") in CONFIG:
    logger.info(bstack1ll11_opy_ (u"ࠫࡓࡵࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠣࡴࡦࡹࡳࡦࡦࠣࡹࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡴࡨࡴࡴࡸࡴࠡࡨࡲࡶࠥࡘ࡯ࡣࡱࡷࠤࡷࡻ࡮ࠨ౼"))
  try:
    platform = CONFIG[bstack1ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ౽")][bstack1l1lll111l_opy_]
    if bstack1ll11_opy_ (u"࠭࡯ࡴࠩ౾") in platform:
      bstack1ll1l11l11_opy_ += str(platform[bstack1ll11_opy_ (u"ࠧࡰࡵࠪ౿")]) + bstack1ll11_opy_ (u"ࠨ࠮ࠣࠫಀ")
    if bstack1ll11_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬಁ") in platform:
      bstack1ll1l11l11_opy_ += str(platform[bstack1ll11_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ಂ")]) + bstack1ll11_opy_ (u"ࠫ࠱ࠦࠧಃ")
    if bstack1ll11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩ಄") in platform:
      bstack1ll1l11l11_opy_ += str(platform[bstack1ll11_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪಅ")]) + bstack1ll11_opy_ (u"ࠧ࠭ࠢࠪಆ")
    if bstack1ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪಇ") in platform:
      bstack1ll1l11l11_opy_ += str(platform[bstack1ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫಈ")]) + bstack1ll11_opy_ (u"ࠪ࠰ࠥ࠭ಉ")
    if bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩಊ") in platform:
      bstack1ll1l11l11_opy_ += str(platform[bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪಋ")]) + bstack1ll11_opy_ (u"࠭ࠬࠡࠩಌ")
    if bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ಍") in platform:
      bstack1ll1l11l11_opy_ += str(platform[bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩಎ")]) + bstack1ll11_opy_ (u"ࠩ࠯ࠤࠬಏ")
  except Exception as e:
    logger.debug(bstack1ll11_opy_ (u"ࠪࡗࡴࡳࡥࠡࡧࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡳ࡭ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡶࡸࡷ࡯࡮ࡨࠢࡩࡳࡷࠦࡲࡦࡲࡲࡶࡹࠦࡧࡦࡰࡨࡶࡦࡺࡩࡰࡰࠪಐ") + str(e))
  finally:
    if bstack1ll1l11l11_opy_[len(bstack1ll1l11l11_opy_) - 2:] == bstack1ll11_opy_ (u"ࠫ࠱ࠦࠧ಑"):
      bstack1ll1l11l11_opy_ = bstack1ll1l11l11_opy_[:-2]
    return bstack1ll1l11l11_opy_
def bstack1ll1111111_opy_(path, bstack1ll1l11l11_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1llllll11l_opy_ = ET.parse(path)
    bstack111ll111ll_opy_ = bstack1llllll11l_opy_.getroot()
    bstack111ll1ll1l_opy_ = None
    for suite in bstack111ll111ll_opy_.iter(bstack1ll11_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫಒ")):
      if bstack1ll11_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ಓ") in suite.attrib:
        suite.attrib[bstack1ll11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬಔ")] += bstack1ll11_opy_ (u"ࠨࠢࠪಕ") + bstack1ll1l11l11_opy_
        bstack111ll1ll1l_opy_ = suite
    bstack1ll1l1ll1_opy_ = None
    for robot in bstack111ll111ll_opy_.iter(bstack1ll11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨಖ")):
      bstack1ll1l1ll1_opy_ = robot
    bstack1l11llllll_opy_ = len(bstack1ll1l1ll1_opy_.findall(bstack1ll11_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩಗ")))
    if bstack1l11llllll_opy_ == 1:
      bstack1ll1l1ll1_opy_.remove(bstack1ll1l1ll1_opy_.findall(bstack1ll11_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪಘ"))[0])
      bstack1lll11l1l_opy_ = ET.Element(bstack1ll11_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫಙ"), attrib={bstack1ll11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫಚ"): bstack1ll11_opy_ (u"ࠧࡔࡷ࡬ࡸࡪࡹࠧಛ"), bstack1ll11_opy_ (u"ࠨ࡫ࡧࠫಜ"): bstack1ll11_opy_ (u"ࠩࡶ࠴ࠬಝ")})
      bstack1ll1l1ll1_opy_.insert(1, bstack1lll11l1l_opy_)
      bstack1l111l1l1_opy_ = None
      for suite in bstack1ll1l1ll1_opy_.iter(bstack1ll11_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩಞ")):
        bstack1l111l1l1_opy_ = suite
      bstack1l111l1l1_opy_.append(bstack111ll1ll1l_opy_)
      bstack1l11ll1l11_opy_ = None
      for status in bstack111ll1ll1l_opy_.iter(bstack1ll11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫಟ")):
        bstack1l11ll1l11_opy_ = status
      bstack1l111l1l1_opy_.append(bstack1l11ll1l11_opy_)
    bstack1llllll11l_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1ll11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡵࡷ࡮ࡴࡧࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡱࡩࡷࡧࡴࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠪಠ") + str(e))
def bstack1ll11l1111_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1l1l1lll1_opy_
  global CONFIG
  if bstack1ll11_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡶࡡࡵࡪࠥಡ") in options:
    del options[bstack1ll11_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡰࡢࡶ࡫ࠦಢ")]
  json_data = bstack11111l1111_opy_()
  for item_id in json_data.keys():
    path = os.path.join(outs_dir, str(item_id), bstack1ll11_opy_ (u"ࠨࡱࡸࡸࡵࡻࡴ࠯ࡺࡰࡰࠬಣ"))
    bstack1ll1111111_opy_(path, bstack1l1l1l1ll_opy_(json_data[item_id]))
  bstack11111ll111_opy_()
  return bstack1l1l1lll1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack111111l111_opy_(self, ff_profile_dir):
  global bstack1lll111ll_opy_
  if not ff_profile_dir:
    return None
  return bstack1lll111ll_opy_(self, ff_profile_dir)
def bstack11l11lll1l_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack111lll11_opy_
  bstack111111lll_opy_ = []
  if bstack1ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬತ") in CONFIG:
    bstack111111lll_opy_ = CONFIG[bstack1ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ಥ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1ll11_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࠧದ")],
      pabot_args[bstack1ll11_opy_ (u"ࠧࡼࡥࡳࡤࡲࡷࡪࠨಧ")],
      argfile,
      pabot_args.get(bstack1ll11_opy_ (u"ࠨࡨࡪࡸࡨࠦನ")),
      pabot_args[bstack1ll11_opy_ (u"ࠢࡱࡴࡲࡧࡪࡹࡳࡦࡵࠥ಩")],
      platform[0],
      bstack111lll11_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1ll11_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡩ࡭ࡱ࡫ࡳࠣಪ")] or [(bstack1ll11_opy_ (u"ࠤࠥಫ"), None)]
    for platform in enumerate(bstack111111lll_opy_)
  ]
def bstack11lll1lll1_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1111ll11ll_opy_=bstack1ll11_opy_ (u"ࠪࠫಬ")):
  global bstack1lll1l1l1l_opy_
  self.platform_index = platform_index
  self.bstack11l1l11l1_opy_ = bstack1111ll11ll_opy_
  bstack1lll1l1l1l_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1111lll1l_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1lll11ll1l_opy_
  global bstack1l11l1l11_opy_
  bstack111ll1l11l_opy_ = copy.deepcopy(item)
  if not bstack1ll11_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ಭ") in item.options:
    bstack111ll1l11l_opy_.options[bstack1ll11_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧಮ")] = []
  bstack11lll111l_opy_ = bstack111ll1l11l_opy_.options[bstack1ll11_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨಯ")].copy()
  for v in bstack111ll1l11l_opy_.options[bstack1ll11_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩರ")]:
    if bstack1ll11_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡑࡎࡄࡘࡋࡕࡒࡎࡋࡑࡈࡊ࡞ࠧಱ") in v:
      bstack11lll111l_opy_.remove(v)
    if bstack1ll11_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡅࡏࡍࡆࡘࡇࡔࠩಲ") in v:
      bstack11lll111l_opy_.remove(v)
    if bstack1ll11_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡇࡉࡋࡒࡏࡄࡃࡏࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧಳ") in v:
      bstack11lll111l_opy_.remove(v)
  bstack11lll111l_opy_.insert(0, bstack1ll11_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚࠽ࡿࢂ࠭಴").format(bstack111ll1l11l_opy_.platform_index))
  bstack11lll111l_opy_.insert(0, bstack1ll11_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡉࡋࡆࡍࡑࡆࡅࡑࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓ࠼ࡾࢁࠬವ").format(bstack111ll1l11l_opy_.bstack11l1l11l1_opy_))
  bstack111ll1l11l_opy_.options[bstack1ll11_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨಶ")] = bstack11lll111l_opy_
  if bstack1l11l1l11_opy_:
    bstack111ll1l11l_opy_.options[bstack1ll11_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩಷ")].insert(0, bstack1ll11_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓ࠻ࡽࢀࠫಸ").format(bstack1l11l1l11_opy_))
  return bstack1lll11ll1l_opy_(caller_id, datasources, is_last, bstack111ll1l11l_opy_, outs_dir)
def bstack11l11111l_opy_(command, item_index):
  try:
    if global_config.get_property(bstack1ll11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪಹ")):
      os.environ[bstack1ll11_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫ಺")] = json.dumps(CONFIG[bstack1ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ಻")][item_index % bstack11l1lll1l_opy_])
    global bstack1l11l1l11_opy_
    os.environ[bstack1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜಼ࠬ")] = str(item_index % bstack11l1lll1l_opy_)
    listener_arg = bstack1ll11_opy_ (u"࠭ࠧಽ")
    if is_robot_playwright_installed() and cli.is_enabled(CONFIG):
      listener_arg = bstack1ll11_opy_ (u"ࠧࠡ࠯࠰ࡰ࡮ࡹࡴࡦࡰࡨࡶࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡸࡪ࡫࠯ࡴࡲࡦࡴࡺ࡟࡭࡫ࡶࡸࡪࡴࡥࡳࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠴ࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡓࡥࡹࡩࡨࡦࡴࠪಾ")
      logger.debug(bstack1ll11_opy_ (u"ࠣࡃࡧࡨ࡮ࡴࡧࠡࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡕࡧࡴࡤࡪࡨࡶࠥࡲࡩࡴࡶࡨࡲࡪࡸࠠࡧࡱࡵࠤ࡮ࡺࡥ࡮ࠢࡾࢁࠧಿ").format(item_index))
    bstack1ll111l1_opy_ = bstack1ll11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠮ࡵࡧ࡯ࠥࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱࠦ࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࠢࠥೀ") + \
              str(item_index % bstack11l1lll1l_opy_) + \
              bstack1ll11_opy_ (u"ࠥࠤ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠣࠦು") + \
              str(item_index) + \
              listener_arg
    if bstack1l11l1l11_opy_:
        bstack1ll111l1_opy_ += bstack1ll11_opy_ (u"ࠦࠥࠨೂ") + bstack1l11l1l11_opy_
    command[0:1] = bstack1ll111l1_opy_.split()
  except Exception as e:
    logger.error(bstack1ll11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡲࡵࡤࡪࡨࡼ࡭ࡳ࡭ࠠࡤࡱࡰࡱࡦࡴࡤࠡࡨࡲࡶࠥࡶࡡࡣࡱࡷࠤࡷࡻ࡮࠻ࠢࡾࢁࠬೃ").format(str(e)))
def bstack1llll111l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1l1l1l1l11_opy_
  try:
    bstack11l11111l_opy_(command, item_index)
    return bstack1l1l1l1l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
  except Exception as e:
    logger.error(bstack1ll11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠࡳࡷࡱ࠾ࠥࢁࡽࠨೄ").format(str(e)))
    raise e
def bstack1111lll11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1l1l1l1l11_opy_
  try:
    bstack11l11111l_opy_(command, item_index)
    return bstack1l1l1l1l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
  except Exception as e:
    logger.error(bstack1ll11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡧࡵࡴࠡࡴࡸࡲࠥ࠸࠮࠲࠵࠽ࠤࢀࢃࠧ೅").format(str(e)))
    try:
      return bstack1l1l1l1l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
    except Exception as e2:
      logger.error(bstack1ll11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡦࡨ࡯ࡵࠢ࠵࠲࠶࠹ࠠࡧࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣࡿࢂ࠭ೆ").format(str(e2)))
      raise e
def bstack111l1l111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1l1l1l1l11_opy_
  try:
    bstack11l11111l_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    return bstack1l1l1l1l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
  except Exception as e:
    logger.error(bstack1ll11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡢࡰࡶࠣࡶࡺࡴࠠ࠳࠰࠴࠹࠿ࠦࡻࡾࠩೇ").format(str(e)))
    try:
      return bstack1l1l1l1l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
    except Exception as e2:
      logger.error(bstack1ll11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡣࡱࡷࠤ࠷࠴࠱࠶ࠢࡩࡥࡱࡲࡢࡢࡥ࡮࠾ࠥࢁࡽࠨೈ").format(str(e2)))
      raise e
def _1lll1lll1_opy_(bstack1lll11111_opy_, item_index, process_timeout, sleep_before_start, bstack11lll11l1l_opy_):
  bstack11l11111l_opy_(bstack1lll11111_opy_, item_index)
  if process_timeout is None:
    process_timeout = 3600
  if sleep_before_start and sleep_before_start > 0:
    time.sleep(min(sleep_before_start, 5))
  return process_timeout
def bstack11l11ll11l_opy_(command, bstack11l1l11l1l_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack1l1l1l1l11_opy_
  global bstack1lll1l11ll_opy_
  global bstack1l11l1l11_opy_
  try:
    for env_name, bstack1ll111ll1l_opy_ in bstack1lll1l11ll_opy_.items():
      os.environ[env_name] = bstack1ll111ll1l_opy_
    bstack1l11l1l11_opy_ = bstack1ll11_opy_ (u"ࠦࠧ೉")
    bstack11l11111l_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    if sleep_before_start and sleep_before_start > 0:
      time.sleep(min(sleep_before_start, 5))
    return bstack1l1l1l1l11_opy_(command, bstack11l1l11l1l_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack1ll11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡥࡳࡹࠦࡲࡶࡰࠣ࠹࠳࠶࠺ࠡࡽࢀࠫೊ").format(str(e)))
    try:
      return bstack1l1l1l1l11_opy_(command, bstack11l1l11l1l_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack1ll11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠࡧࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣࡿࢂ࠭ೋ").format(str(e2)))
      raise e
def bstack1ll111ll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack1l1l1l1l11_opy_
  try:
    process_timeout = _1lll1lll1_opy_(command, item_index, process_timeout, sleep_before_start, bstack1ll11_opy_ (u"ࠧ࠵࠰࠵ࠫೌ"))
    return bstack1l1l1l1l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack1ll11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡦࡨ࡯ࡵࠢࡵࡹࡳࠦ࠴࠯࠴࠽ࠤࢀࢃ್ࠧ").format(str(e)))
    try:
      return bstack1l1l1l1l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack1ll11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡢࡰࡶࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࡻࡾࠩ೎").format(str(e2)))
      raise e
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack1ll1l1l1l_opy_(self, runner, quiet=False, capture=True):
  global bstack1l1llll1l1_opy_
  bstack111111111_opy_ = bstack1l1llll1l1_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack1ll11_opy_ (u"ࠪࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࡥࡡࡳࡴࠪ೏")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1ll11_opy_ (u"ࠫࡪࡾࡣࡠࡶࡵࡥࡨ࡫ࡢࡢࡥ࡮ࡣࡦࡸࡲࠨ೐")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack111111111_opy_
def bstack11ll1lll1_opy_(runner, hook_name, context, element, bstack11l1l1lll1_opy_, *args):
  global bstack11lll11lll_opy_
  try:
    if runner.hooks.get(hook_name):
      bstack11ll1l1lll_opy_.bstack1l1lll1lll_opy_(hook_name, element)
    if bstack11lll11lll_opy_ is None or bstack11lll11lll_opy_:
      bstack11l1l1lll1_opy_(runner, hook_name, context, *args)
    else:
      bstack1lll1l11l_opy_ = (context,) + args
      bstack11l1l1lll1_opy_(runner, hook_name, *bstack1lll1l11l_opy_)
    if runner.hooks.get(hook_name):
      bstack11ll1l1lll_opy_.bstack11l1l1l1l1_opy_(element)
      if hook_name not in [bstack1ll11_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠩ೑"), bstack1ll11_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠩ೒")] and args and hasattr(args[0], bstack1ll11_opy_ (u"ࠧࡦࡴࡵࡳࡷࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠧ೓")):
        args[0].error_message = bstack1ll11_opy_ (u"ࠨࠩ೔")
  except Exception as e:
    logger.debug(bstack1ll11_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡮ࡡ࡯ࡦ࡯ࡩࠥ࡮࡯ࡰ࡭ࡶࠤ࡮ࡴࠠࡣࡧ࡫ࡥࡻ࡫࠺ࠡࡽࢀࠫೕ").format(str(e)))
@measure(event_name=EVENTS.bstack11l1l1l1_opy_, stage=STAGE.bstack11111llll_opy_, hook_type=bstack1ll11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡄࡰࡱࠨೖ"), bstack11lll1l111_opy_=SESSION_NAME)
def bstack11lll1l1l1_opy_(runner, name, context, bstack11l1l1lll1_opy_, *args):
    if runner.hooks.get(bstack1ll11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣ೗")).__name__ != bstack1ll11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࡡࡧࡩ࡫ࡧࡵ࡭ࡶࡢ࡬ࡴࡵ࡫ࠣ೘"):
      bstack11ll1lll1_opy_(runner, name, context, runner, bstack11l1l1lll1_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack111l1l1l1l_opy_(bstack1ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ೙")) else context.browser
      runner.driver_initialised = bstack1ll11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦ೚")
    except Exception as e:
      logger.debug(bstack1ll11_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡦࡵ࡭ࡻ࡫ࡲࠡ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡶࡩࠥࡧࡴࡵࡴ࡬ࡦࡺࡺࡥ࠻ࠢࡾࢁࠬ೛").format(str(e)))
def bstack11ll1ll111_opy_(runner, name, context, bstack11l1l1lll1_opy_, *args):
    bstack11ll1lll1_opy_(runner, name, context, context.feature, bstack11l1l1lll1_opy_, *args)
    try:
      if not bstack11l1l1lll_opy_:
        bstack1l1l11111_opy_ = threading.current_thread().bstackSessionDriver if bstack111l1l1l1l_opy_(bstack1ll11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ೜")) else context.browser
        if is_driver_active(bstack1l1l11111_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack1ll11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦೝ")
          bstack111ll11111_opy_ = str(runner.feature.name)
          playwright_set_session_name(context, bstack111ll11111_opy_)
          bstack1l1l11111_opy_.execute_script(bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩೞ") + json.dumps(bstack111ll11111_opy_) + bstack1ll11_opy_ (u"ࠬࢃࡽࠨ೟"))
    except Exception as e:
      logger.debug(bstack1ll11_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭ೠ").format(str(e)))
def bstack1ll11ll11l_opy_(runner, name, context, bstack11l1l1lll1_opy_, *args):
    target = context.scenario if hasattr(context, bstack1ll11_opy_ (u"ࠧࡴࡥࡨࡲࡦࡸࡩࡰࠩೡ")) else context.feature
    bstack11ll1lll1_opy_(runner, name, context, target, bstack11l1l1lll1_opy_, *args)
@measure(event_name=EVENTS.bstack1l1llll1_opy_, stage=STAGE.bstack11111llll_opy_, bstack11lll1l111_opy_=SESSION_NAME)
def bstack111lllll1l_opy_(runner, name, context, bstack11l1l1lll1_opy_, *args):
    bstack11ll1l1lll_opy_.start_test(context)
    bstack11ll1lll1_opy_(runner, name, context, context.scenario, bstack11l1l1lll1_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack1l1l1111l_opy_.bstack1l111lll_opy_(context, *args)
    try:
      bstack1l1l11111_opy_ = bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧೢ"), context.browser)
      if is_driver_active(bstack1l1l11111_opy_):
        TestHubHandler.send_cbt_info(bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨೣ"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack1ll11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧ೤")
        if (not bstack11l1l1lll_opy_):
          scenario_name = args[0].name
          feature_name = bstack111ll11111_opy_ = str(runner.feature.name)
          bstack111ll11111_opy_ = feature_name + bstack1ll11_opy_ (u"ࠫࠥ࠳ࠠࠨ೥") + scenario_name
          if runner.driver_initialised == bstack1ll11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢ೦"):
            playwright_set_session_name(context, bstack111ll11111_opy_)
            bstack1l1l11111_opy_.execute_script(bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫ೧") + json.dumps(bstack111ll11111_opy_) + bstack1ll11_opy_ (u"ࠧࡾࡿࠪ೨"))
    except Exception as e:
      logger.debug(bstack1ll11_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡨ࡫࡮ࡢࡴ࡬ࡳ࠿ࠦࡻࡾࠩ೩").format(str(e)))
@measure(event_name=EVENTS.bstack11l1l1l1_opy_, stage=STAGE.bstack11111llll_opy_, hook_type=bstack1ll11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡕࡷࡩࡵࠨ೪"), bstack11lll1l111_opy_=SESSION_NAME)
def bstack11ll1l11_opy_(runner, name, context, bstack11l1l1lll1_opy_, *args):
    bstack11ll1lll1_opy_(runner, name, context, args[0], bstack11l1l1lll1_opy_, *args)
    try:
      bstack1l1l11111_opy_ = threading.current_thread().bstackSessionDriver if bstack111l1l1l1l_opy_(bstack1ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ೫")) else context.browser
      if is_driver_active(bstack1l1l11111_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack1ll11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤ೬")
        bstack11ll1l1lll_opy_.bstack1ll11lll11_opy_(args[0])
        if runner.driver_initialised == bstack1ll11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥ೭") and not bstack11l1l1lll_opy_:
          feature_name = bstack111ll11111_opy_ = str(runner.feature.name)
          bstack111ll11111_opy_ = feature_name + bstack1ll11_opy_ (u"࠭ࠠ࠮ࠢࠪ೮") + context.scenario.name
          playwright_set_session_name(context, bstack111ll11111_opy_)
          bstack1l1l11111_opy_.execute_script(bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬ೯") + json.dumps(bstack111ll11111_opy_) + bstack1ll11_opy_ (u"ࠨࡿࢀࠫ೰"))
    except Exception as e:
      logger.debug(bstack1ll11_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡ࡫ࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡺࡥࡱ࠼ࠣࡿࢂ࠭ೱ").format(str(e)))
@measure(event_name=EVENTS.bstack11l1l1l1_opy_, stage=STAGE.bstack11111llll_opy_, hook_type=bstack1ll11_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࡕࡷࡩࡵࠨೲ"), bstack11lll1l111_opy_=SESSION_NAME)
def bstack1ll11l11ll_opy_(runner, name, context, bstack11l1l1lll1_opy_, *args):
  bstack11ll1l1lll_opy_.bstack11111l11l_opy_(args[0])
  try:
    step_status = args[0].status.name
    bstack1l1l11111_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪೳ") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack1l1l11111_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack1ll11_opy_ (u"ࠬ࡯࡮ࡴࡶࡨࡴࠬ೴")
        if not bstack11l1l1lll_opy_:
          feature_name = bstack111ll11111_opy_ = str(runner.feature.name)
          bstack111ll11111_opy_ = feature_name + bstack1ll11_opy_ (u"࠭ࠠ࠮ࠢࠪ೵") + context.scenario.name
          playwright_set_session_name(context, bstack111ll11111_opy_)
          bstack1l1l11111_opy_.execute_script(bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬ೶") + json.dumps(bstack111ll11111_opy_) + bstack1ll11_opy_ (u"ࠨࡿࢀࠫ೷"))
    if str(step_status).lower() in [bstack1ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ೸"), bstack1ll11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ೹")]:
      bstack11lll1ll1_opy_ = bstack1ll11_opy_ (u"ࠫࠬ೺")
      bstack1111lllll1_opy_ = bstack1ll11_opy_ (u"ࠬ࠭೻")
      bstack11lllll1ll_opy_ = bstack1ll11_opy_ (u"࠭ࠧ೼")
      try:
        import traceback
        bstack11lll1ll1_opy_ = runner.exception.__class__.__name__
        bstack1lll11ll_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1111lllll1_opy_ = bstack1ll11_opy_ (u"ࠧࠡࠩ೽").join(bstack1lll11ll_opy_)
        bstack11lllll1ll_opy_ = bstack1lll11ll_opy_[-1]
      except Exception as e:
        logger.debug(bstack1ll111llll_opy_.format(str(e)))
      bstack11lll1ll1_opy_ += bstack11lllll1ll_opy_
      playwright_annotate(context, json.dumps(str(args[0].name) + bstack1ll11_opy_ (u"ࠣࠢ࠰ࠤࡋࡧࡩ࡭ࡧࡧࠥࡡࡴࠢ೾") + str(bstack1111lllll1_opy_)),
                          bstack1ll11_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣ೿"))
      if runner.driver_initialised == bstack1ll11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣഀ"):
        bstack1ll1l11lll_opy_(getattr(context, bstack1ll11_opy_ (u"ࠫࡵࡧࡧࡦࠩഁ"), None), bstack1ll11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧം"), bstack11lll1ll1_opy_)
        bstack1l1l11111_opy_.execute_script(bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫഃ") + json.dumps(str(args[0].name) + bstack1ll11_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨഄ") + str(bstack1111lllll1_opy_)) + bstack1ll11_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨഅ"))
      if runner.driver_initialised == bstack1ll11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢആ"):
        bstack11l11l111l_opy_(bstack1l1l11111_opy_, bstack1ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪഇ"), bstack1ll11_opy_ (u"ࠦࡘࡩࡥ࡯ࡣࡵ࡭ࡴࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࡢ࡮ࠣഈ") + str(bstack11lll1ll1_opy_))
    else:
      playwright_annotate(context, bstack1ll11_opy_ (u"ࠧࡖࡡࡴࡵࡨࡨࠦࠨഉ"), bstack1ll11_opy_ (u"ࠨࡩ࡯ࡨࡲࠦഊ"))
      if runner.driver_initialised == bstack1ll11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧഋ"):
        bstack1ll1l11lll_opy_(getattr(context, bstack1ll11_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭ഌ"), None), bstack1ll11_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ഍"))
      bstack1l1l11111_opy_.execute_script(bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨഎ") + json.dumps(str(args[0].name) + bstack1ll11_opy_ (u"ࠦࠥ࠳ࠠࡑࡣࡶࡷࡪࡪࠡࠣഏ")) + bstack1ll11_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫഐ"))
      if runner.driver_initialised == bstack1ll11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦ഑"):
        bstack11l11l111l_opy_(bstack1l1l11111_opy_, bstack1ll11_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢഒ"))
  except Exception as e:
    logger.debug(bstack1ll11_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࠥࡹࡴࡦࡲ࠽ࠤࢀࢃࠧഓ").format(str(e)))
  bstack11ll1lll1_opy_(runner, name, context, args[0], bstack11l1l1lll1_opy_, *args)
@measure(event_name=EVENTS.bstack11lll111_opy_, stage=STAGE.bstack11111llll_opy_, bstack11lll1l111_opy_=SESSION_NAME)
def bstack11ll111l_opy_(runner, name, context, bstack11l1l1lll1_opy_, *args):
  bstack11ll1l1lll_opy_.end_test(args[0])
  try:
    bstack111l1l11ll_opy_ = args[0].status.name
    bstack1l1l11111_opy_ = bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨഔ"), context.browser)
    bstack1l1l1111l_opy_.bstack11l1l1l1ll_opy_(bstack1l1l11111_opy_)
    if str(bstack111l1l11ll_opy_).lower() in [bstack1ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪക"), bstack1ll11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪഖ")]:
      bstack11lll1ll1_opy_ = bstack1ll11_opy_ (u"ࠬ࠭ഗ")
      bstack1111lllll1_opy_ = bstack1ll11_opy_ (u"࠭ࠧഘ")
      bstack11lllll1ll_opy_ = bstack1ll11_opy_ (u"ࠧࠨങ")
      try:
        import traceback
        bstack11lll1ll1_opy_ = runner.exception.__class__.__name__
        bstack1lll11ll_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1111lllll1_opy_ = bstack1ll11_opy_ (u"ࠨࠢࠪച").join(bstack1lll11ll_opy_)
        bstack11lllll1ll_opy_ = bstack1lll11ll_opy_[-1]
      except Exception as e:
        logger.debug(bstack1ll111llll_opy_.format(str(e)))
      bstack11lll1ll1_opy_ += bstack11lllll1ll_opy_
      playwright_annotate(context, json.dumps(str(args[0].name) + bstack1ll11_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣഛ") + str(bstack1111lllll1_opy_)),
                          bstack1ll11_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤജ"))
      if runner.driver_initialised == bstack1ll11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨഝ") or runner.driver_initialised == bstack1ll11_opy_ (u"ࠬ࡯࡮ࡴࡶࡨࡴࠬഞ"):
        bstack1ll1l11lll_opy_(getattr(context, bstack1ll11_opy_ (u"࠭ࡰࡢࡩࡨࠫട"), None), bstack1ll11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢഠ"), bstack11lll1ll1_opy_)
        bstack1l1l11111_opy_.execute_script(bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ഡ") + json.dumps(str(args[0].name) + bstack1ll11_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣഢ") + str(bstack1111lllll1_opy_)) + bstack1ll11_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪണ"))
      if runner.driver_initialised == bstack1ll11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨത") or runner.driver_initialised == bstack1ll11_opy_ (u"ࠬ࡯࡮ࡴࡶࡨࡴࠬഥ"):
        bstack11l11l111l_opy_(bstack1l1l11111_opy_, bstack1ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ദ"), bstack1ll11_opy_ (u"ࠢࡔࡥࡨࡲࡦࡸࡩࡰࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦധ") + str(bstack11lll1ll1_opy_))
    else:
      playwright_annotate(context, bstack1ll11_opy_ (u"ࠣࡒࡤࡷࡸ࡫ࡤࠢࠤന"), bstack1ll11_opy_ (u"ࠤ࡬ࡲ࡫ࡵࠢഩ"))
      if runner.driver_initialised == bstack1ll11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧപ") or runner.driver_initialised == bstack1ll11_opy_ (u"ࠫ࡮ࡴࡳࡵࡧࡳࠫഫ"):
        bstack1ll1l11lll_opy_(getattr(context, bstack1ll11_opy_ (u"ࠬࡶࡡࡨࡧࠪബ"), None), bstack1ll11_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨഭ"))
      bstack1l1l11111_opy_.execute_script(bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬമ") + json.dumps(str(args[0].name) + bstack1ll11_opy_ (u"ࠣࠢ࠰ࠤࡕࡧࡳࡴࡧࡧࠥࠧയ")) + bstack1ll11_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧࢃࡽࠨര"))
      if runner.driver_initialised == bstack1ll11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧറ") or runner.driver_initialised == bstack1ll11_opy_ (u"ࠫ࡮ࡴࡳࡵࡧࡳࠫല"):
        bstack11l11l111l_opy_(bstack1l1l11111_opy_, bstack1ll11_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧള"))
  except Exception as e:
    logger.debug(bstack1ll11_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨഴ").format(str(e)))
  bstack11ll1lll1_opy_(runner, name, context, context.scenario, bstack11l1l1lll1_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack111llll11l_opy_(runner, name, context, bstack11l1l1lll1_opy_, *args):
    target = context.scenario if hasattr(context, bstack1ll11_opy_ (u"ࠧࡴࡥࡨࡲࡦࡸࡩࡰࠩവ")) else context.feature
    bstack11ll1lll1_opy_(runner, name, context, target, bstack11l1l1lll1_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack1lll1ll11_opy_(runner, name, context, bstack11l1l1lll1_opy_, *args):
    try:
      bstack1l1l11111_opy_ = bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧശ"), context.browser)
      bstack1111111l1l_opy_ = bstack1ll11_opy_ (u"ࠩࠪഷ")
      if context.failed is True:
        bstack1lll1111_opy_ = []
        bstack11llllll_opy_ = []
        bstack11111l1l1_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack1lll1111_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1lll11ll_opy_ = traceback.format_tb(exc_tb)
            bstack1ll11lll1l_opy_ = bstack1ll11_opy_ (u"ࠪࠤࠬസ").join(bstack1lll11ll_opy_)
            bstack11llllll_opy_.append(bstack1ll11lll1l_opy_)
            bstack11111l1l1_opy_.append(bstack1lll11ll_opy_[-1])
        except Exception as e:
          logger.debug(bstack1ll111llll_opy_.format(str(e)))
        bstack11lll1ll1_opy_ = bstack1ll11_opy_ (u"ࠫࠬഹ")
        for i in range(len(bstack1lll1111_opy_)):
          bstack11lll1ll1_opy_ += bstack1lll1111_opy_[i] + bstack11111l1l1_opy_[i] + bstack1ll11_opy_ (u"ࠬࡢ࡮ࠨഺ")
        bstack1111111l1l_opy_ = bstack1ll11_opy_ (u"࠭ࠠࠨ഻").join(bstack11llllll_opy_)
        if runner.driver_initialised in [bstack1ll11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥ഼ࠣ"), bstack1ll11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧഽ")]:
          playwright_annotate(context, bstack1111111l1l_opy_, bstack1ll11_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣാ"))
          bstack1ll1l11lll_opy_(getattr(context, bstack1ll11_opy_ (u"ࠪࡴࡦ࡭ࡥࠨി"), None), bstack1ll11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦീ"), bstack11lll1ll1_opy_)
          bstack1l1l11111_opy_.execute_script(bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪു") + json.dumps(bstack1111111l1l_opy_) + bstack1ll11_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥࢁࢂ࠭ൂ"))
          bstack11l11l111l_opy_(bstack1l1l11111_opy_, bstack1ll11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢൃ"), bstack1ll11_opy_ (u"ࠣࡕࡲࡱࡪࠦࡳࡤࡧࡱࡥࡷ࡯࡯ࡴࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡠࡳࠨൄ") + str(bstack11lll1ll1_opy_))
          bstack1l1l1lll11_opy_ = bstack111111l11_opy_(bstack1111111l1l_opy_, runner.feature.name, logger)
          if (bstack1l1l1lll11_opy_ != None):
            bstack1llllllllll_opy_.append(bstack1l1l1lll11_opy_)
      else:
        if runner.driver_initialised in [bstack1ll11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠥ൅"), bstack1ll11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢെ")]:
          playwright_annotate(context, bstack1ll11_opy_ (u"ࠦࡋ࡫ࡡࡵࡷࡵࡩ࠿ࠦࠢേ") + str(runner.feature.name) + bstack1ll11_opy_ (u"ࠧࠦࡰࡢࡵࡶࡩࡩࠧࠢൈ"), bstack1ll11_opy_ (u"ࠨࡩ࡯ࡨࡲࠦ൉"))
          bstack1ll1l11lll_opy_(getattr(context, bstack1ll11_opy_ (u"ࠧࡱࡣࡪࡩࠬൊ"), None), bstack1ll11_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣോ"))
          bstack1l1l11111_opy_.execute_script(bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧൌ") + json.dumps(bstack1ll11_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨ࠾ࠥࠨ്") + str(runner.feature.name) + bstack1ll11_opy_ (u"ࠦࠥࡶࡡࡴࡵࡨࡨࠦࠨൎ")) + bstack1ll11_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫ൏"))
          bstack11l11l111l_opy_(bstack1l1l11111_opy_, bstack1ll11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭൐"))
          bstack1l1l1lll11_opy_ = bstack111111l11_opy_(bstack1111111l1l_opy_, runner.feature.name, logger)
          if (bstack1l1l1lll11_opy_ != None):
            bstack1llllllllll_opy_.append(bstack1l1l1lll11_opy_)
    except Exception as e:
      logger.debug(bstack1ll11_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩ൑").format(str(e)))
    bstack11ll1lll1_opy_(runner, name, context, context.feature, bstack11l1l1lll1_opy_, *args)
@measure(event_name=EVENTS.bstack11l1l1l1_opy_, stage=STAGE.bstack11111llll_opy_, hook_type=bstack1ll11_opy_ (u"ࠣࡣࡩࡸࡪࡸࡁ࡭࡮ࠥ൒"), bstack11lll1l111_opy_=SESSION_NAME)
def bstack1ll1llll11_opy_(runner, name, context, bstack11l1l1lll1_opy_, *args):
    bstack11ll1lll1_opy_(runner, name, context, runner, bstack11l1l1lll1_opy_, *args)
def bstack1l111l1l11_opy_(self, filename=None):
  global bstack1lll11lll_opy_
  bstack1lll11lll_opy_(self, filename)
  bstack11ll111111_opy_ = []
  bstack1l1ll1l1l1_opy_ = [bstack1ll11_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠪ൓"), bstack1ll11_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡸࡦ࡭ࠧൔ"), bstack1ll11_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ൕ"), bstack1ll11_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ൖ"), bstack1ll11_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡺࡡࡨࠩൗ"), bstack1ll11_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡦࡦࡣࡷࡹࡷ࡫ࠧ൘")]
  bstack1l1l11l1l_opy_ = lambda *_: None
  for hook_name in bstack1l1ll1l1l1_opy_:
    if hook_name not in self.hooks:
      self.hooks[hook_name] = bstack1l1l11l1l_opy_
      bstack11ll111111_opy_.append(hook_name)
  if bstack11ll111111_opy_:
    os.environ[bstack1ll11_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡕࡇࡏࡤࡊࡅࡇࡃࡘࡐ࡙ࡥࡈࡐࡑࡎࡗࠬ൙")] = bstack1ll11_opy_ (u"ࠩ࠯ࠫ൚").join(bstack11ll111111_opy_)
def _execute_deferred_playwright_close():
  try:
    _111ll1llll_opy_ = threading.current_thread()
    _1lllll11l_opy_ = getattr(_111ll1llll_opy_, bstack1ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡨࡪ࡬ࡥࡳࡴࡨࡨࡤࡶࡡࡨࡧࡢࡶࡪ࡬ࠧ൛"), None)
    _111lll1lll_opy_ = getattr(_111ll1llll_opy_, bstack1ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡩ࡫ࡦࡦࡴࡵࡩࡩࡥࡢࡳࡱࡺࡷࡪࡸ࡟ࡳࡧࡩࠫ൜"), None)
    _1l1l111ll_opy_ = getattr(_111ll1llll_opy_, bstack1ll11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡪࡥࡧࡧࡵࡶࡪࡪ࡟ࡱࡹࡢࡷࡹࡵࡰࡠࡨࡱࠫ൝"), None)
    _wrapper = getattr(_111ll1llll_opy_, bstack1ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ൞"), None)
    if not _111lll1lll_opy_ and _wrapper and hasattr(_wrapper, bstack1ll11_opy_ (u"ࠧࡠࡤࡵࡳࡼࡹࡥࡳࠩൟ")):
      _111lll1lll_opy_ = _wrapper._browser
    if not _1lllll11l_opy_ and _wrapper and hasattr(_wrapper, bstack1ll11_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧൠ")):
      _1lllll11l_opy_ = _wrapper._page
    if not _1l1l111ll_opy_:
      _11l1ll111l_opy_ = getattr(_111ll1llll_opy_, bstack1ll11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡧࡩ࡫࡫ࡲࡳࡧࡧࡣࡵࡽ࡟ࡳࡧࡩࠫൡ"), None)
      if _11l1ll111l_opy_ and hasattr(_11l1ll111l_opy_, bstack1ll11_opy_ (u"ࠪࡷࡹࡵࡰࠨൢ")):
        _1l1l111ll_opy_ = _11l1ll111l_opy_.stop
    _1ll1l1l1_opy_ = _1lllll11l_opy_ or _111lll1lll_opy_ or _1l1l111ll_opy_
    if not _1ll1l1l1_opy_:
      return
    if _1lllll11l_opy_ and hasattr(_1lllll11l_opy_, bstack1ll11_opy_ (u"ࠫࡨࡲ࡯ࡴࡧࠪൣ")):
      try:
        _1lllll11l_opy_.close(_bstack_sdk_close=True)
      except TypeError:
        try:
          _1lllll11l_opy_.close()
        except Exception:
          pass
      except Exception as e:
        logger.debug(bstack1ll11_opy_ (u"ࠬࡊࡥࡧࡧࡵࡶࡪࡪࠠࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡵࡧࡧࡦ࠰ࡦࡰࡴࡹࡥࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࡾࢁࠬ൤").format(str(e)))
    if _111lll1lll_opy_ and hasattr(_111lll1lll_opy_, bstack1ll11_opy_ (u"࠭ࡣ࡭ࡱࡶࡩࠬ൥")):
      try:
        _111lll1lll_opy_.close(_bstack_sdk_close=True)
      except TypeError:
        try:
          _111lll1lll_opy_.close()
        except Exception:
          pass
      except Exception as e:
        logger.debug(bstack1ll11_opy_ (u"ࠧࡅࡧࡩࡩࡷࡸࡥࡥࠢࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡢࡳࡱࡺࡷࡪࡸ࠮ࡤ࡮ࡲࡷࡪࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࡼࡿࠪ൦").format(str(e)))
    if _1l1l111ll_opy_:
      try:
        _1l1l111ll_opy_(_bstack_sdk_close=True)
      except TypeError:
        try:
          _1l1l111ll_opy_()
        except Exception:
          pass
      except Exception as e:
        logger.debug(bstack1ll11_opy_ (u"ࠨࡆࡨࡪࡪࡸࡲࡦࡦࠣࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡶࡲࡴࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡾࠩ൧").format(str(e)))
    for attr in (bstack1ll11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡧࡩ࡫࡫ࡲࡳࡧࡧࡣࡵࡧࡧࡦࡡࡦࡰࡴࡹࡥࠨ൨"), bstack1ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡨࡪ࡬ࡥࡳࡴࡨࡨࡤࡶࡡࡨࡧࡢࡶࡪ࡬ࠧ൩"),
                 bstack1ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡩ࡫ࡦࡦࡴࡵࡩࡩࡥࡢࡳࡱࡺࡷࡪࡸ࡟ࡤ࡮ࡲࡷࡪ࠭൪"), bstack1ll11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡪࡥࡧࡧࡵࡶࡪࡪ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡠࡴࡨࡪࠬ൫"),
                 bstack1ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡤࡦࡨࡨࡶࡷ࡫ࡤࡠࡲࡺࡣࡸࡺ࡯ࡱࠩ൬"), bstack1ll11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡥࡧࡩࡩࡷࡸࡥࡥࡡࡳࡻࡤࡹࡴࡰࡲࡢࡪࡳ࠭൭"),
                 bstack1ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡦࡨࡪࡪࡸࡲࡦࡦࡢࡴࡼࡥࡲࡦࡨࠪ൮")):
      try:
        delattr(_111ll1llll_opy_, attr)
      except AttributeError:
        pass
    if _wrapper:
      try:
        _wrapper._page = None
        _wrapper._browser = None
      except Exception:
        pass
    logger.debug(bstack1ll11_opy_ (u"ࠩࡇࡩ࡫࡫ࡲࡳࡧࡧࠤࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡥ࡯ࡳࡸ࡫ࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࡦࠣࡪࡴࡸࠠࡵࡪࡵࡩࡦࡪࠠࡼࡿࠪ൯").format(_111ll1llll_opy_.ident))
  except Exception as e:
    logger.debug(bstack1ll11_opy_ (u"ࠪࡈࡪ࡬ࡥࡳࡴࡨࡨࠥࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡦࡰࡴࡹࡥࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࡾࢁࠬ൰").format(str(e)))
def bstack1l1l1l11_opy_(self, name, *args):
  global bstack11l1l1lll1_opy_
  global bstack11lll11lll_opy_
  try:
    if BROWSERSTACK_AUTOMATION:
      platform_index = int(threading.current_thread()._name) % bstack11l1lll1l_opy_
      bstack11l1l11lll_opy_ = CONFIG[bstack1ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ൱")][platform_index]
      os.environ[bstack1ll11_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭൲")] = json.dumps(bstack11l1l11lll_opy_)
    if not hasattr(self, bstack1ll11_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡧࡧࠫ൳")):
      self.driver_initialised = None
    bstack11l1ll11_opy_ = {
        bstack1ll11_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠫ൴"): bstack11lll1l1l1_opy_,
        bstack1ll11_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠩ൵"): bstack11ll1ll111_opy_,
        bstack1ll11_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡷࡥ࡬࠭൶"): bstack1ll11ll11l_opy_,
        bstack1ll11_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ൷"): bstack111lllll1l_opy_,
        bstack1ll11_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠩ൸"): bstack11ll1l11_opy_,
        bstack1ll11_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡺࡥࡱࠩ൹"): bstack1ll11l11ll_opy_,
        bstack1ll11_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧൺ"): bstack11ll111l_opy_,
        bstack1ll11_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡴࡢࡩࠪൻ"): bstack111llll11l_opy_,
        bstack1ll11_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨർ"): bstack1lll1ll11_opy_,
        bstack1ll11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠬൽ"): bstack1ll1llll11_opy_
    }
    handler = bstack11l1ll11_opy_.get(name, bstack11l1l1lll1_opy_)
    try:
      if args:
        context = args[0]
        remaining_args = args[1:]
        if bstack11lll11lll_opy_ is None or not bstack11lll11lll_opy_:
          context = self.context
          remaining_args = args
      else:
        context = self.context
        remaining_args = ()
      handler(self, name, context, bstack11l1l1lll1_opy_, *remaining_args)
    except Exception as e:
      logger.debug(bstack1ll11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡨࡥࡩࡣࡹࡩࠥ࡮࡯ࡰ࡭ࠣ࡬ࡦࡴࡤ࡭ࡧࡵࠤࢀࢃ࠺ࠡࡽࢀࠫൾ").format(name, str(e)))
    if name == bstack1ll11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬൿ"):
      _execute_deferred_playwright_close()
    if name in [bstack1ll11_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬ඀"), bstack1ll11_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧඁ"), bstack1ll11_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪං")]:
      try:
        bstack1l1l11111_opy_ = threading.current_thread().bstackSessionDriver if bstack111l1l1l1l_opy_(bstack1ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧඃ")) else context.browser
        bstack11l111llll_opy_ = (
          (name == bstack1ll11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠬ඄") and self.driver_initialised == bstack1ll11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢඅ")) or
          (name == bstack1ll11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫආ") and self.driver_initialised == bstack1ll11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨඇ")) or
          (name == bstack1ll11_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧඈ") and self.driver_initialised in [bstack1ll11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤඉ"), bstack1ll11_opy_ (u"ࠣ࡫ࡱࡷࡹ࡫ࡰࠣඊ")]) or
          (name == bstack1ll11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡷࡩࡵ࠭උ") and self.driver_initialised == bstack1ll11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣඌ"))
        )
        if bstack11l111llll_opy_:
          self.driver_initialised = None
          if bstack1l1l11111_opy_ and hasattr(bstack1l1l11111_opy_, bstack1ll11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨඍ")):
            try:
              bstack1l1l11111_opy_.quit()
            except Exception as e:
              logger.debug(bstack1ll11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡶࡻࡩࡵࡶ࡬ࡲ࡬ࠦࡤࡳ࡫ࡹࡩࡷࠦࡩ࡯ࠢࡥࡩ࡭ࡧࡶࡦࠢ࡫ࡳࡴࡱ࠺ࠡࡽࢀࠫඎ").format(str(e)))
      except Exception as e:
        logger.debug(bstack1ll11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡣࡩࡸࡪࡸࠠࡩࡱࡲ࡯ࠥࡩ࡬ࡦࡣࡱࡹࡵࠦࡦࡰࡴࠣࡿࢂࡀࠠࡼࡿࠪඏ").format(name, str(e)))
  except Exception as e:
    logger.debug(bstack1ll11_opy_ (u"ࠧࡄࡴ࡬ࡸ࡮ࡩࡡ࡭ࠢࡨࡶࡷࡵࡲࠡ࡫ࡱࠤࡧ࡫ࡨࡢࡸࡨࠤࡷࡻ࡮ࠡࡪࡲࡳࡰࠦࡻࡾ࠼ࠣࡿࢂ࠭ඐ").format(name, str(e)))
    try:
      if bstack11lll11lll_opy_ is None or bstack11lll11lll_opy_:
        try:
          bstack11l1l1lll1_opy_(self, name, self.context, *args)
        except TypeError:
          bstack11l1l1lll1_opy_(self, name, *args)
      else:
        bstack11l1l1lll1_opy_(self, name, *args)
    except Exception as e2:
      logger.debug(bstack1ll11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡵࡲࡪࡩ࡬ࡲࡦࡲࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡩࡱࡲ࡯ࠥࢁࡽ࠻ࠢࡾࢁࠬඑ").format(name, str(e2)))
  finally:
    if name == bstack1ll11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪඒ"):
      _execute_deferred_playwright_close()
def bstack11l1l11ll_opy_(config, startdir):
  return bstack1ll11_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀ࠶ࡽࠣඓ").format(bstack1ll11_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥඔ"))
notset = Notset()
def bstack11l1l11l11_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack111l1ll1l1_opy_
  if str(name).lower() == bstack1ll11_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࠬඕ"):
    return bstack1ll11_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧඖ")
  else:
    return bstack111l1ll1l1_opy_(self, name, default, skip)
def bstack11ll11l11_opy_(item, when):
  global bstack11ll11lll1_opy_
  try:
    bstack11ll11lll1_opy_(item, when)
  except Exception as e:
    pass
def bstack1l1ll1111_opy_():
  return
def browserstack_executor_helper(type, name, status, reason, bstack11l11ll11_opy_, bstack11ll1l1l11_opy_):
  bstack1lll111111_opy_ = {
    bstack1ll11_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧ඗"): type,
    bstack1ll11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ඘"): {}
  }
  if type == bstack1ll11_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫ඙"):
    bstack1lll111111_opy_[bstack1ll11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ක")][bstack1ll11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪඛ")] = bstack11l11ll11_opy_
    bstack1lll111111_opy_[bstack1ll11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨග")][bstack1ll11_opy_ (u"࠭ࡤࡢࡶࡤࠫඝ")] = json.dumps(str(bstack11ll1l1l11_opy_))
  if type == bstack1ll11_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨඞ"):
    bstack1lll111111_opy_[bstack1ll11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫඟ")][bstack1ll11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧච")] = name
  if type == bstack1ll11_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ඡ"):
    bstack1lll111111_opy_[bstack1ll11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧජ")][bstack1ll11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬඣ")] = status
    if status == bstack1ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ඤ"):
      bstack1lll111111_opy_[bstack1ll11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪඥ")][bstack1ll11_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨඦ")] = json.dumps(str(reason))
  bstack1llll11l11_opy_ = bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧට").format(json.dumps(bstack1lll111111_opy_))
  return bstack1llll11l11_opy_
def bstack1ll11111_opy_(driver_command, response):
    if driver_command == bstack1ll11_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧඨ"):
        TestHubHandler.bstack1ll1llll_opy_({
            bstack1ll11_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪඩ"): response[bstack1ll11_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫඪ")],
            bstack1ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ණ"): TestHubHandler.current_test_uuid()
        })
def bstack11l11l1ll1_opy_(item, call, rep):
  global bstack1l1l11ll1_opy_
  global bstack11l1ll1l11_opy_
  global bstack11l1l1lll_opy_
  name = bstack1ll11_opy_ (u"ࠧࠨඬ")
  try:
    if rep.when == bstack1ll11_opy_ (u"ࠨࡥࡤࡰࡱ࠭ත"):
      bstack1ll1l11l_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack11l1l1lll_opy_:
          name = str(rep.nodeid)
          executor_string = browserstack_executor_helper(bstack1ll11_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪථ"), name, bstack1ll11_opy_ (u"ࠪࠫද"), bstack1ll11_opy_ (u"ࠫࠬධ"), bstack1ll11_opy_ (u"ࠬ࠭න"), bstack1ll11_opy_ (u"࠭ࠧ඲"))
          threading.current_thread().bstack1l11l1l111_opy_ = name
          for driver in bstack11l1ll1l11_opy_:
            if bstack1ll1l11l_opy_ == driver.session_id:
              driver.execute_script(executor_string)
      except Exception as e:
        logger.debug(bstack1ll11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧඳ").format(str(e)))
      try:
        bstack1l1l11l1ll_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack1ll11_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩප"):
          status = bstack1ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩඵ") if rep.outcome.lower() == bstack1ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪබ") else bstack1ll11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫභ")
          reason = bstack1ll11_opy_ (u"ࠬ࠭ම")
          if status == bstack1ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ඹ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack1ll11_opy_ (u"ࠧࡪࡰࡩࡳࠬය") if status == bstack1ll11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨර") else bstack1ll11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ඼")
          data = name + bstack1ll11_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬල") if status == bstack1ll11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ඾") else name + bstack1ll11_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩࠧࠠࠨ඿") + reason
          bstack11l11ll1ll_opy_ = browserstack_executor_helper(bstack1ll11_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨව"), bstack1ll11_opy_ (u"ࠧࠨශ"), bstack1ll11_opy_ (u"ࠨࠩෂ"), bstack1ll11_opy_ (u"ࠩࠪස"), level, data)
          for driver in bstack11l1ll1l11_opy_:
            if bstack1ll1l11l_opy_ == driver.session_id:
              driver.execute_script(bstack11l11ll1ll_opy_)
      except Exception as e:
        logger.debug(bstack1ll11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡤࡱࡱࡸࡪࡾࡴࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧහ").format(str(e)))
  except Exception as e:
    logger.debug(bstack1ll11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡶࡤࡸࡪࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁࡽࠨළ").format(str(e)))
  bstack1l1l11ll1_opy_(item, call, rep)
def bstack11lll111l1_opy_(driver, bstack1lll1lll11_opy_, test=None):
  global PLATFORM_INDEX
  if test != None:
    bstack1llll1l111_opy_ = getattr(test, bstack1ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪෆ"), None)
    bstack111111ll11_opy_ = getattr(test, bstack1ll11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ෇"), None)
    PercySDK.screenshot(driver, bstack1lll1lll11_opy_, bstack1llll1l111_opy_=bstack1llll1l111_opy_, bstack111111ll11_opy_=bstack111111ll11_opy_, bstack1lll1111l_opy_=PLATFORM_INDEX)
  else:
    PercySDK.screenshot(driver, bstack1lll1lll11_opy_)
@measure(event_name=EVENTS.bstack11ll11l111_opy_, stage=STAGE.bstack11111llll_opy_, bstack11lll1l111_opy_=SESSION_NAME)
def bstack11l11111_opy_(driver):
  if bstack1l11lll11l_opy_.bstack1llll1ll11_opy_() is True or bstack1l11lll11l_opy_.capturing() is True:
    return
  bstack1l11lll11l_opy_.bstack1l11ll11ll_opy_()
  while not bstack1l11lll11l_opy_.bstack1llll1ll11_opy_():
    bstack1l11l11ll1_opy_ = bstack1l11lll11l_opy_.bstack11lllll11l_opy_()
    bstack11lll111l1_opy_(driver, bstack1l11l11ll1_opy_)
  bstack1l11lll11l_opy_.bstack11l1l1llll_opy_()
def bstack111111l1_opy_(sequence, driver_command, response = None, bstack1111l1l1_opy_ = None, args = None):
    try:
      if sequence != bstack1ll11_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧ෈"):
        return
      if percy.bstack1lllll1l1_opy_() == bstack1ll11_opy_ (u"ࠣࡨࡤࡰࡸ࡫ࠢ෉"):
        return
      bstack1l11l11ll1_opy_ = bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠩࡳࡩࡷࡩࡹࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩ්ࠬ"), None)
      for command in bstack111llll111_opy_:
        if command == driver_command:
          with bstack1llll1l1l_opy_:
            bstack1l1111l1l1_opy_ = bstack11l1ll1l11_opy_.copy()
          for driver in bstack1l1111l1l1_opy_:
            bstack11l11111_opy_(driver)
      bstack11l11ll1_opy_ = percy.bstack11l11l11l1_opy_()
      if driver_command in bstack1l1l11llll_opy_[bstack11l11ll1_opy_]:
        bstack1l11lll11l_opy_.bstack1llll11ll_opy_(bstack1l11l11ll1_opy_, driver_command)
    except Exception as e:
      pass
_11llll1lll_opy_ = threading.Event()
def bstack1l1llll1ll_opy_(framework_name):
  if global_config.get_property(bstack1ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡱࡴࡪ࡟ࡤࡣ࡯ࡰࡪࡪࠧ෋")):
      _11llll1lll_opy_.wait(timeout=30)
      return
  global_config.bstack1ll11l111_opy_(bstack1ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨ෌"), True)
  global FRAMEWORK_NAME
  global SELENIUM_OR_PLAYWRIGHT_INSTALLED
  global bstack11ll111ll_opy_
  FRAMEWORK_NAME = framework_name
  logger.info(bstack1l11l1ll1_opy_.format(FRAMEWORK_NAME.split(bstack1ll11_opy_ (u"ࠬ࠳ࠧ෍"))[0]))
  bstack111l111l11_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    global bstack11l1l1ll11_opy_
    bstack1l1111lll_opy_ = BROWSERSTACK_AUTOMATION or bstack11l1l1ll11_opy_
    if bstack1l1111lll_opy_:
      Service.start = bstack11ll1l11ll_opy_
      Service.stop = bstack1111ll111_opy_
      webdriver.Remote.get = bstack111111ll1l_opy_
      WebDriver.quit = bstack1llllll11_opy_
      webdriver.Remote.__init__ = bstack1lllll11l1_opy_
    if not BROWSERSTACK_AUTOMATION and not bstack11l1l1ll11_opy_:
        webdriver.Remote.__init__ = bstack1l1l1l1l1l_opy_
    WebDriver.getAccessibilityResults = getAccessibilityResults
    WebDriver.get_accessibility_results = getAccessibilityResults
    WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
    WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
    WebDriver.performScan = perform_scan
    WebDriver.perform_scan = perform_scan
    WebDriver.execute = bstack1ll1111l11_opy_
    SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
  except Exception as e:
    pass
  try:
    bstack1l1111lll_opy_ = BROWSERSTACK_AUTOMATION or bstack11l1l1ll11_opy_
    if bstack1l1111lll_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1111l1ll1_opy_
  except Exception as e:
    pass
  try:
    set_playwright_globals(
        CONFIG=CONFIG,
        FRAMEWORK_NAME=FRAMEWORK_NAME,
        PLATFORM_INDEX=PLATFORM_INDEX,
        SESSION_NAME=SESSION_NAME,
        PARALLELISE_VANILLA_PYTHON=PARALLELISE_VANILLA_PYTHON,
        PARALLELISE_THREADING_PYTHON=PARALLELISE_THREADING_PYTHON,
        __version__=__version__,
        TestHubUtils=TestHubUtils,
        get_caps=get_caps,
        update_caps_for_local=update_caps_for_local,
        logger=logger,
        CONFIG_FILE_CONTENT=CONFIG_FILE_CONTENT,
        BROWSERSTACK_AUTOMATION=BROWSERSTACK_AUTOMATION,
        SELENIUM_OR_PLAYWRIGHT_INSTALLED=SELENIUM_OR_PLAYWRIGHT_INSTALLED,
        global_config=global_config,
        get_turboscale_playwright_url=get_turboscale_playwright_url,
        os=os,
        threading=threading,
        multiprocessing=multiprocessing,
        json=json,
        traceback=traceback,
    )
  except Exception as e:
    logger.debug(bstack1ll11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣ࡫ࡱࡵࡢࡢ࡮ࡶ࠾ࠥࢁࡽࠣ෎").format(str(e)))
  patch_playwright()
  if not SELENIUM_OR_PLAYWRIGHT_INSTALLED:
    bstack1ll1ll1l11_opy_(bstack1ll11_opy_ (u"ࠢࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠢࡱࡳࡹࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠤා"), bstack111l1l11l_opy_)
  if bstack11lllll1l1_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      if hasattr(RemoteConnection, bstack1ll11_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩැ")) and callable(getattr(RemoteConnection, bstack1ll11_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪෑ"))):
        RemoteConnection._get_proxy_url = bstack1ll1ll1111_opy_
      else:
        from selenium.webdriver.remote.client_config import ClientConfig
        ClientConfig.get_proxy_url = bstack1ll1ll1111_opy_
    except Exception as e:
      logger.error(bstack1lll11l1l1_opy_.format(str(e)))
  if bstack1ll111l11_opy_():
    bstack1lllllllll1_opy_(CONFIG, logger)
  if (bstack1ll11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩි") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      try:
        from pabot.pabot import QueueItem
        from pabot import pabot
      except Exception as e:
        logger.warning(bstack1l1111l1l_opy_ + str(e))
      if not is_robot_playwright_installed():
        try:
          if percy.bstack1lllll1l1_opy_() == bstack1ll11_opy_ (u"ࠦࡹࡸࡵࡦࠤී"):
            bstack1l1111l11_opy_(bstack111111l1_opy_)
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
          WebDriverCreator._get_ff_profile = bstack111111l111_opy_
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
          WebDriverCache.close = bstack11l1111l11_opy_
        except Exception as e:
          logger.warning(bstack11ll11111l_opy_ + str(e))
        try:
          from AppiumLibrary.utils.applicationcache import ApplicationCache
          ApplicationCache.close = bstack1l11lll1_opy_
        except Exception as e:
          logger.debug(bstack11111l1ll_opy_ + str(e))
    except Exception as e:
      bstack1ll1ll1l11_opy_(e, bstack11ll11111l_opy_)
    Output.start_test = bstack1lllllll11_opy_
    Output.end_test = bstack1llllllll_opy_
    TestStatus.__init__ = bstack1ll1l1111l_opy_
    QueueItem.__init__ = bstack11lll1lll1_opy_
    pabot._create_items = bstack11l11lll1l_opy_
    try:
      from pabot import __version__ as bstack1ll1l1ll_opy_
      if version.parse(bstack1ll1l1ll_opy_) >= version.parse(bstack1ll11_opy_ (u"ࠬ࠻࠮࠱࠰࠳ࠫු")):
        pabot._run = bstack11l11ll11l_opy_
      elif version.parse(bstack1ll1l1ll_opy_) >= version.parse(bstack1ll11_opy_ (u"࠭࠴࠯࠴࠱࠴ࠬ෕")):
        pabot._run = bstack1ll111ll11_opy_
      elif version.parse(bstack1ll1l1ll_opy_) >= version.parse(bstack1ll11_opy_ (u"ࠧ࠳࠰࠴࠹࠳࠶ࠧූ")):
        pabot._run = bstack111l1l111l_opy_
      elif version.parse(bstack1ll1l1ll_opy_) >= version.parse(bstack1ll11_opy_ (u"ࠨ࠴࠱࠵࠸࠴࠰ࠨ෗")):
        pabot._run = bstack1111lll11l_opy_
      else:
        pabot._run = bstack1llll111l1_opy_
    except Exception as e:
      pabot._run = bstack1llll111l1_opy_
    pabot._create_command_for_execution = bstack1111lll1l_opy_
    pabot._report_results = bstack1ll11l1111_opy_
  if bstack1ll11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩෘ") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll1ll1l11_opy_(e, bstack1l111111l_opy_)
    Runner.run_hook = bstack1l1l1l11_opy_
    try:
      from behave import __version__ as bstack1l1lll11l_opy_
      if version.parse(bstack1l1lll11l_opy_) >= version.parse(bstack1ll11_opy_ (u"ࠪ࠵࠳࠹࠮࠱ࠩෙ")):
        Runner.load_hooks = bstack1l111l1l11_opy_
    except Exception as e:
      logger.debug(bstack1ll11_opy_ (u"ࠫࡈࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡦࡪ࡮ࡡࡷࡧࠣࡺࡪࡸࡳࡪࡱࡱ࠾ࠥࢁࡽࠨේ").format(str(e)))
    Step.run = bstack1ll1l1l1l_opy_
  if bstack1ll11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬෛ") in str(framework_name).lower():
    if not BROWSERSTACK_AUTOMATION:
      _11llll1lll_opy_.set()
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack11l1l11ll_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1l1ll1111_opy_
      Config.getoption = bstack11l1l11l11_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack11l11l1ll1_opy_
    except Exception as e:
      pass
  _11llll1lll_opy_.set()
def bstack1111111l_opy_():
  global CONFIG
  if bstack1ll11_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ො") in CONFIG and int(CONFIG[bstack1ll11_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧෝ")]) > 1:
    logger.warning(bstack111l1ll1_opy_)
def bstack1llll1l1l1_opy_(arg, bstack1l11l111_opy_, bstack11lll1111l_opy_=None):
  global CONFIG
  global bstack11llll1l1l_opy_
  global bstack1l11lll111_opy_
  global BROWSERSTACK_AUTOMATION
  global bstack11l1l1ll11_opy_
  global global_config
  bstack11lll11ll1_opy_ = bstack1ll11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨෞ")
  if bstack1l11l111_opy_ and isinstance(bstack1l11l111_opy_, str):
    bstack1l11l111_opy_ = eval(bstack1l11l111_opy_)
  CONFIG = bstack1l11l111_opy_[bstack1ll11_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩෟ")]
  bstack11llll1l1l_opy_ = bstack1l11l111_opy_[bstack1ll11_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫ෠")]
  bstack1l11lll111_opy_ = bstack1l11l111_opy_[bstack1ll11_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭෡")]
  BROWSERSTACK_AUTOMATION = bstack1l11l111_opy_[bstack1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ෢")]
  try:
    bstack1l111l1lll_opy_ = bstack1l11l111_opy_.get(bstack1ll11_opy_ (u"࠭ࡏࡗࡇࡕࡖࡎࡊࡅࡠࡎࡒࡅࡉࡥࡔࡆࡕࡗࡍࡓࡍࠧ෣"), False)
    bstack11l1l1ll11_opy_ = bool(bstack1l111l1lll_opy_)
    os.environ[bstack1ll11_opy_ (u"ࠧࡐࡘࡈࡖࡗࡏࡄࡆࡡࡏࡓࡆࡊ࡟ࡕࡇࡖࡘࡎࡔࡇࠨ෤")] = str(bstack11l1l1ll11_opy_).lower()
  except Exception as e:
    logger.error(bstack1ll11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡕࡖࡆࡔࡕࡍࡉࡋ࡟ࡍࡑࡄࡈࡤ࡚ࡅࡔࡖࡌࡒࡌࡀࠠࡼࡿࠥ෥").format(e))
    bstack11l1l1ll11_opy_ = False
    os.environ[bstack1ll11_opy_ (u"ࠩࡒ࡚ࡊࡘࡒࡊࡆࡈࡣࡑࡕࡁࡅࡡࡗࡉࡘ࡚ࡉࡏࡉࠪ෦")] = bstack1ll11_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩ෧")
  global_config.bstack1ll11l111_opy_(bstack1ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬ෨"), BROWSERSTACK_AUTOMATION)
  os.environ[bstack1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ෩")] = bstack11lll11ll1_opy_
  os.environ[bstack1ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࠬ෪")] = json.dumps(CONFIG)
  os.environ[bstack1ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡈࡖࡄࡢ࡙ࡗࡒࠧ෫")] = bstack11llll1l1l_opy_
  os.environ[bstack1ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ෬")] = str(bstack1l11lll111_opy_)
  os.environ[bstack1ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡏ࡙ࡌࡏࡎࠨ෭")] = str(True)
  if bstack1ll1l111l1_opy_(arg, [bstack1ll11_opy_ (u"ࠪ࠱ࡳ࠭෮"), bstack1ll11_opy_ (u"ࠫ࠲࠳࡮ࡶ࡯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ෯")]) != -1:
    os.environ[bstack1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡇࡒࡂࡎࡏࡉࡑ࠭෰")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack11l1ll1l_opy_)
    return
  bstack1l1llllll_opy_()
  global bstack11l1llll11_opy_
  global PLATFORM_INDEX
  global bstack111lll11_opy_
  global bstack1l11l1l11_opy_
  global bstack1l111l111l_opy_
  global bstack11ll111ll_opy_
  global PARALLELISE_VANILLA_PYTHON
  arg.append(bstack1ll11_opy_ (u"ࠨ࠭ࡘࠤ෱"))
  arg.append(bstack1ll11_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫࠺ࡎࡱࡧࡹࡱ࡫ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡ࡫ࡰࡴࡴࡸࡴࡦࡦ࠽ࡴࡾࡺࡥࡴࡶ࠱ࡔࡾࡺࡥࡴࡶ࡚ࡥࡷࡴࡩ࡯ࡩࠥෲ"))
  arg.append(bstack1ll11_opy_ (u"ࠣ࠯࡚ࠦෳ"))
  arg.append(bstack1ll11_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡦ࠼ࡗ࡬ࡪࠦࡨࡰࡱ࡮࡭ࡲࡶ࡬ࠣ෴"))
  global bstack1llllllll1_opy_
  global bstack1ll1111l1_opy_
  global bstack11l1lll1ll_opy_
  global bstack11l1l1ll1l_opy_
  global bstack1lll111ll_opy_
  global bstack1lll1l1l1l_opy_
  global bstack1lll11ll1l_opy_
  global bstack1l111111l1_opy_
  global bstack111111l1l1_opy_
  global bstack1111l1l11_opy_
  global bstack111l1ll1l1_opy_
  global bstack11ll11lll1_opy_
  global bstack1l1l11ll1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1llllllll1_opy_ = webdriver.Remote.__init__
    bstack1ll1111l1_opy_ = WebDriver.quit
    bstack1l111111l1_opy_ = WebDriver.close
    bstack111111l1l1_opy_ = WebDriver.get
    bstack11l1lll1ll_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1111lllll_opy_(CONFIG) and bstack1l1111111_opy_():
    if bstack1lll11llll_opy_() < version.parse(bstack1l11l1l11l_opy_):
      logger.error(bstack1l1111ll11_opy_.format(bstack1lll11llll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack1ll11_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫ෵")) and callable(getattr(RemoteConnection, bstack1ll11_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬ෶"))):
          bstack1111l1l11_opy_ = RemoteConnection._get_proxy_url
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          bstack1111l1l11_opy_ = ClientConfig.get_proxy_url
      except Exception as e:
        logger.error(bstack1lll11l1l1_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack111l1ll1l1_opy_ = Config.getoption
    from _pytest import runner
    bstack11ll11lll1_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warning(bstack1ll11_opy_ (u"ࠧࠫࡳ࠻ࠢࠨࡷࠧ෷"), bstack1l1ll1111l_opy_, str(e))
  try:
    from pytest_bdd import reporting
    bstack1l1l11ll1_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack1ll11_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧ෸"))
  if cli.is_enabled(CONFIG) and cli.config:
    bstack111lll11_opy_ = cli.config.get(bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ෹"), {}).get(bstack1ll11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ෺"))
  else:
    bstack111lll11_opy_ = CONFIG.get(bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭෻"), {}).get(bstack1ll11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ෼"))
  PARALLELISE_VANILLA_PYTHON = True
  if cli.is_enabled(CONFIG):
    if cli.bstack1ll1111lll_opy_():
      bstack1lll111l_opy_.invoke(Events.CONNECT, bstack11lll11ll_opy_())
    platform_index = int(os.environ.get(bstack1ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ෽"), bstack1ll11_opy_ (u"ࠬ࠶ࠧ෾")))
  else:
    bstack1l1llll1ll_opy_(bstack11111l1l_opy_)
  os.environ[bstack1ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧ෿")] = CONFIG[bstack1ll11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ฀")]
  os.environ[bstack1ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫก")] = CONFIG[bstack1ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬข")]
  os.environ[bstack1ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭ฃ")] = BROWSERSTACK_AUTOMATION.__str__()
  from _pytest.config import main as bstack1l1l1l1l1_opy_
  bstack11l1l11l_opy_ = []
  try:
    exit_code = bstack1l1l1l1l1_opy_(arg)
    if cli.is_enabled(CONFIG):
      cli.bstack1lllll1ll_opy_()
    if bstack1ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴࠨค") in multiprocessing.current_process().__dict__.keys():
      for bstack1lll11lll1_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack11l1l11l_opy_.append(bstack1lll11lll1_opy_)
    try:
      bstack111ll1l1l1_opy_ = (bstack11l1l11l_opy_, int(exit_code))
      bstack11lll1111l_opy_.append(bstack111ll1l1l1_opy_)
    except:
      bstack11lll1111l_opy_.append((bstack11l1l11l_opy_, exit_code))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack11l1l11l_opy_.append({bstack1ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪฅ"): bstack1ll11_opy_ (u"࠭ࡐࡳࡱࡦࡩࡸࡹࠠࠨฆ") + os.environ.get(bstack1ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧง")), bstack1ll11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧจ"): traceback.format_exc(), bstack1ll11_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨฉ"): int(os.environ.get(bstack1ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪช")))})
    bstack11lll1111l_opy_.append((bstack11l1l11l_opy_, 1))
def mod_behave_main(args, retries):
  try:
    from behave.configuration import Configuration
    from behave.__main__ import run_behave
    from browserstack_sdk.bstack_behave_runner import BehaveRunner
    config = Configuration(args)
    config.update_userdata({bstack1ll11_opy_ (u"ࠦࡷ࡫ࡴࡳ࡫ࡨࡷࠧซ"): str(retries)})
    return run_behave(config, runner_class=BehaveRunner)
  except Exception as e:
    bstack1l1ll1lll_opy_ = e.__class__.__name__
    print(bstack1ll11_opy_ (u"ࠧࠫࡳ࠻ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡴࡸࡲࡳ࡯࡮ࡨࠢࡥࡩ࡭ࡧࡶࡦࠢࡷࡩࡸࡺࠠࠦࡵࠥฌ") % (bstack1l1ll1lll_opy_, e))
    return 1
def bstack1ll1111l_opy_(arg):
  global bstack1ll1l11l1l_opy_
  bstack1l1llll1ll_opy_(bstack111ll1111_opy_)
  os.environ[bstack1ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧญ")] = str(bstack1l11lll111_opy_)
  retries = bstack1l1ll11ll1_opy_.bstack1111llll11_opy_(CONFIG)
  status_code = 0
  if bstack1l1ll11ll1_opy_.bstack1lll1lllll_opy_(CONFIG):
    status_code = mod_behave_main(arg, retries)
  else:
    from behave.__main__ import main as bstack111ll11l1_opy_
    status_code = bstack111ll11l1_opy_(arg)
  if status_code != 0:
    bstack1ll1l11l1l_opy_ = status_code
def bstack1llll1l1ll_opy_():
  logger.info(bstack1lllll1lll_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1ll11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ฎ"), help=bstack1ll11_opy_ (u"ࠨࡉࡨࡲࡪࡸࡡࡵࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡦࡳࡳ࡬ࡩࡨࠩฏ"))
  parser.add_argument(bstack1ll11_opy_ (u"ࠩ࠰ࡹࠬฐ"), bstack1ll11_opy_ (u"ࠪ࠱࠲ࡻࡳࡦࡴࡱࡥࡲ࡫ࠧฑ"), help=bstack1ll11_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡷࡶࡩࡷࡴࡡ࡮ࡧࠪฒ"))
  parser.add_argument(bstack1ll11_opy_ (u"ࠬ࠳࡫ࠨณ"), bstack1ll11_opy_ (u"࠭࠭࠮࡭ࡨࡽࠬด"), help=bstack1ll11_opy_ (u"࡚ࠧࡱࡸࡶࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡦࡩࡣࡦࡵࡶࠤࡰ࡫ࡹࠨต"))
  parser.add_argument(bstack1ll11_opy_ (u"ࠨ࠯ࡩࠫถ"), bstack1ll11_opy_ (u"ࠩ࠰࠱࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧท"), help=bstack1ll11_opy_ (u"ࠪ࡝ࡴࡻࡲࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩธ"))
  bstack1ll1ll1l1l_opy_ = parser.parse_args()
  try:
    bstack111ll1111l_opy_ = bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡫ࡪࡴࡥࡳ࡫ࡦ࠲ࡾࡳ࡬࠯ࡵࡤࡱࡵࡲࡥࠨน")
    if bstack1ll1ll1l1l_opy_.framework and bstack1ll1ll1l1l_opy_.framework not in (bstack1ll11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬบ"), bstack1ll11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧป")):
      bstack111ll1111l_opy_ = bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠰ࡼࡱࡱ࠴ࡳࡢ࡯ࡳࡰࡪ࠭ผ")
    bstack1l11l1ll_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack111ll1111l_opy_)
    bstack11lll1ll_opy_ = open(bstack1l11l1ll_opy_, bstack1ll11_opy_ (u"ࠨࡴࠪฝ"))
    bstack1l11l11l1_opy_ = bstack11lll1ll_opy_.read()
    bstack11lll1ll_opy_.close()
    if bstack1ll1ll1l1l_opy_.username:
      bstack1l11l11l1_opy_ = bstack1l11l11l1_opy_.replace(bstack1ll11_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩพ"), bstack1ll1ll1l1l_opy_.username)
    if bstack1ll1ll1l1l_opy_.key:
      bstack1l11l11l1_opy_ = bstack1l11l11l1_opy_.replace(bstack1ll11_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬฟ"), bstack1ll1ll1l1l_opy_.key)
    if bstack1ll1ll1l1l_opy_.framework:
      bstack1l11l11l1_opy_ = bstack1l11l11l1_opy_.replace(bstack1ll11_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬภ"), bstack1ll1ll1l1l_opy_.framework)
    file_name = bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨม")
    file_path = os.path.abspath(file_name)
    bstack1ll11l1l_opy_ = open(file_path, bstack1ll11_opy_ (u"࠭ࡷࠨย"))
    bstack1ll11l1l_opy_.write(bstack1l11l11l1_opy_)
    bstack1ll11l1l_opy_.close()
    logger.info(bstack11ll11111_opy_)
    try:
      os.environ[bstack1ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩร")] = bstack1ll1ll1l1l_opy_.framework if bstack1ll1ll1l1l_opy_.framework != None else bstack1ll11_opy_ (u"ࠣࠤฤ")
      config = yaml.safe_load(bstack1l11l11l1_opy_)
      config[bstack1ll11_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩล")] = bstack1ll11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰ࡷࡪࡺࡵࡱࠩฦ")
      bstack11l1lll11l_opy_(bstack1111l1111_opy_, config)
    except Exception as e:
      logger.debug(bstack11111l11_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1ll111lll1_opy_.format(str(e)))
def bstack11l1lll11l_opy_(bstack1l1ll111l_opy_, config, bstack11111ll1l1_opy_=None, bstack111111ll1_opy_=False):
  global BROWSERSTACK_AUTOMATION
  global bstack11111l1ll1_opy_
  global global_config
  if not config:
    return
  if bstack11111ll1l1_opy_ is None:
    bstack11111ll1l1_opy_ = {}
  bstack1lll111l1l_opy_ = bstack1llllll111_opy_ if not BROWSERSTACK_AUTOMATION else (
    bstack11llll1ll_opy_ if bstack1ll11_opy_ (u"ࠫࡦࡶࡰࠨว") in config else (
        bstack1111lll1_opy_ if config.get(bstack1ll11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩศ")) else bstack1ll1l111_opy_
    )
)
  bstack11l1llll1l_opy_ = False
  bstack11111lll_opy_ = False
  if BROWSERSTACK_AUTOMATION is True:
      if bstack1ll11_opy_ (u"࠭ࡡࡱࡲࠪษ") in config:
          bstack11l1llll1l_opy_ = True
      else:
          bstack11111lll_opy_ = True
  bstack1ll1lll11_opy_ = TestHubUtils.bstack11ll1l111_opy_(config, bstack11111l1ll1_opy_)
  bstack1l11lll1l_opy_ = bstack1l1lll11ll_opy_()
  data = {
    bstack1ll11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩส"): config[bstack1ll11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪห")],
    bstack1ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬฬ"): config[bstack1ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭อ")],
    bstack1ll11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨฮ"): bstack1l1ll111l_opy_,
    bstack1ll11_opy_ (u"ࠬࡪࡥࡵࡧࡦࡸࡪࡪࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩฯ"): os.environ.get(bstack1ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨะ"), bstack11111l1ll1_opy_),
    bstack1ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩั"): bstack11l1ll11l1_opy_,
    bstack1ll11_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮ࠪา"): bstack1l11ll1ll_opy_(),
    bstack1ll11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬำ"): {
      bstack1ll11_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨิ"): str(config[bstack1ll11_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫี")]) if bstack1ll11_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬึ") in config else bstack1ll11_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢื"),
      bstack1ll11_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࡘࡨࡶࡸ࡯࡯࡯ุࠩ"): sys.version,
      bstack1ll11_opy_ (u"ࠨࡴࡨࡪࡪࡸࡲࡦࡴูࠪ"): bstack1lllll1l1l_opy_(os.environ.get(bstack1ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎฺࠫ"), bstack11111l1ll1_opy_)),
      bstack1ll11_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬ฻"): bstack1ll11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ฼"),
      bstack1ll11_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭฽"): bstack1lll111l1l_opy_,
      bstack1ll11_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ࡟࡮ࡣࡳࠫ฾"): bstack1ll1lll11_opy_,
      bstack1ll11_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡠࡷࡸ࡭ࡩ࠭฿"): os.environ[bstack1ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭เ")],
      bstack1ll11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬแ"): os.environ.get(bstack1ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬโ"), bstack11111l1ll1_opy_),
      bstack1ll11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧใ"): bstack11l1lllll1_opy_(os.environ.get(bstack1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧไ"), bstack11111l1ll1_opy_)),
      bstack1ll11_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬๅ"): bstack1l11lll1l_opy_.get(bstack1ll11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬๆ")),
      bstack1ll11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧ็"): bstack1l11lll1l_opy_.get(bstack1ll11_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰ่ࠪ")),
      bstack1ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ้࠭"): config[bstack1ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫๊ࠧ")] if config[bstack1ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ๋")] else bstack1ll11_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢ์"),
      bstack1ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩํ"): str(config[bstack1ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ๎")]) if bstack1ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ๏") in config else bstack1ll11_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦ๐"),
      bstack1ll11_opy_ (u"ࠫࡴࡹࠧ๑"): sys.platform,
      bstack1ll11_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧ๒"): socket.gethostname(),
      bstack1ll11_opy_ (u"࠭ࡩࡴࡅࡏࡍࡊࡴࡡࡣ࡮ࡨࡨࠬ๓"): bstack111111ll1_opy_,
      bstack1ll11_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥࠩ๔"): global_config.get_property(bstack1ll11_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪ๕"))
    }
  }
  if not global_config.get_property(bstack1ll11_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩ๖")) is None:
    data[bstack1ll11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭๗")][bstack1ll11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡓࡥࡵࡣࡧࡥࡹࡧࠧ๘")] = {
      bstack1ll11_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ๙"): bstack1ll11_opy_ (u"࠭ࡵࡴࡧࡵࡣࡰ࡯࡬࡭ࡧࡧࠫ๚"),
      bstack1ll11_opy_ (u"ࠧࡴ࡫ࡪࡲࡦࡲࠧ๛"): global_config.get_property(bstack1ll11_opy_ (u"ࠨࡵࡧ࡯ࡐ࡯࡬࡭ࡕ࡬࡫ࡳࡧ࡬ࠨ๜")),
      bstack1ll11_opy_ (u"ࠩࡶ࡭࡬ࡴࡡ࡭ࡐࡸࡱࡧ࡫ࡲࠨ๝"): global_config.get_property(bstack1ll11_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡒࡴ࠭๞"))
    }
  if bstack1l1ll111l_opy_ == bstack11ll11ll11_opy_:
    data[bstack1ll11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧ๟")][bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡇࡴࡴࡦࡪࡩࠪ๠")] = bstack1111l11l_opy_(config)
    data[bstack1ll11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩ๡")][bstack1ll11_opy_ (u"ࠧࡪࡵࡓࡩࡷࡩࡹࡂࡷࡷࡳࡊࡴࡡࡣ࡮ࡨࡨࠬ๢")] = percy.bstack11llll11l_opy_
    data[bstack1ll11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫ๣")][bstack1ll11_opy_ (u"ࠩࡳࡩࡷࡩࡹࡃࡷ࡬ࡰࡩࡏࡤࠨ๤")] = percy.percy_build_id
  if not bstack1l1ll11ll1_opy_.bstack1lll11l11_opy_(CONFIG):
    data[bstack1ll11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭๥")][bstack1ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠨ๦")] = bstack1l1ll11ll1_opy_.bstack1lll11l11_opy_(CONFIG)
  bstack11ll1l1l_opy_ = bstack1ll1ll11l1_opy_.get_instance(CONFIG, logger)
  bstack1l1l1llll1_opy_ = bstack1l1ll11ll1_opy_.get_instance(config=CONFIG)
  if bstack11ll1l1l_opy_ is not None and bstack1l1l1llll1_opy_ is not None and bstack1l1l1llll1_opy_.bstack1ll11ll111_opy_():
    data[bstack1ll11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨ๧")][bstack1l1l1llll1_opy_.bstack11ll11ll_opy_()] = bstack11ll1l1l_opy_.bstack111ll11l11_opy_()
  update(data[bstack1ll11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩ๨")], bstack11111ll1l1_opy_)
  try:
    response = bstack1ll11l111l_opy_(bstack1ll11_opy_ (u"ࠧࡑࡑࡖࡘࠬ๩"), bstack1llll1ll1l_opy_(bstack11l11l1l11_opy_), data, {
      bstack1ll11_opy_ (u"ࠨࡣࡸࡸ࡭࠭๪"): (config[bstack1ll11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ๫")], config[bstack1ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭๬")])
    })
    if response:
      logger.debug(bstack1l1l11l1_opy_.format(bstack1l1ll111l_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1111l11ll_opy_.format(str(e)))
def bstack1lllll1l1l_opy_(framework):
  return bstack1ll11_opy_ (u"ࠦࢀࢃ࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴ࢁࡽࠣ๭").format(str(framework), __version__) if framework else bstack1ll11_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࡿࢂࠨ๮").format(
    __version__)
def bstack1l1llllll_opy_():
  global CONFIG
  global bstack1111ll1l_opy_
  if bool(CONFIG):
    return
  try:
    bstack11l11ll111_opy_()
    logger.debug(bstack11ll11ll1_opy_.format(str(CONFIG)))
    bstack1111ll1l_opy_ = logger_utils.configure_logger(CONFIG, bstack1111ll1l_opy_)
    bstack111l111l11_opy_()
  except Exception as e:
    logger.error(bstack1ll11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࠥ๯") + str(e))
    sys.exit(1)
  sys.excepthook = bstack111lll1ll_opy_
  atexit.register(bstack11llllll1_opy_)
  signal.signal(signal.SIGINT, bstack1l111l11ll_opy_)
  signal.signal(signal.SIGTERM, bstack1l111l11ll_opy_)
def bstack111lll1ll_opy_(exctype, value, traceback):
  global bstack11l1ll1l11_opy_
  try:
    for driver in bstack11l1ll1l11_opy_:
      bstack11l11l111l_opy_(driver, bstack1ll11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ๰"), bstack1ll11_opy_ (u"ࠣࡕࡨࡷࡸ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦ๱") + str(value))
  except Exception:
    pass
  logger.info(bstack1lll1lll_opy_)
  bstack1l11ll1111_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1l11ll1111_opy_(message=bstack1ll11_opy_ (u"ࠩࠪ๲"), bstack11ll1l1111_opy_ = False, bstack111111ll1_opy_ = False):
  global CONFIG
  bstack111l11lll_opy_ = bstack1ll11_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠬ๳") if bstack11ll1l1111_opy_ else bstack1ll11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ๴")
  bstack1ll11llll1_opy_ = bstack11ll11l1ll_opy_.bstack11l11l111_opy_(EVENTS.bstack11l111ll_opy_)
  try:
    if message:
      bstack11111ll1l1_opy_ = {
        bstack111l11lll_opy_ : str(message)
      }
      try:
        bstack11l1lll11l_opy_(bstack11ll11ll11_opy_, CONFIG, bstack11111ll1l1_opy_, bstack111111ll1_opy_)
      finally:
        bstack11ll11l1ll_opy_.end(EVENTS.bstack11l111ll_opy_.value, bstack1ll11llll1_opy_ + bstack1ll11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ๵"), bstack1ll11llll1_opy_ + bstack1ll11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ๶"), status=True, failure=None, test_name=None)
    else:
      try:
        bstack11l1lll11l_opy_(bstack11ll11ll11_opy_, CONFIG, bstack111111ll1_opy_=bstack111111ll1_opy_)
      finally:
        bstack11ll11l1ll_opy_.end(EVENTS.bstack11l111ll_opy_.value, bstack1ll11llll1_opy_ + bstack1ll11_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ๷"), bstack1ll11llll1_opy_ + bstack1ll11_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ๸"), status=True, failure=None, test_name=None)
  except Exception as e:
    logger.debug(bstack1111ll11_opy_.format(str(e)))
def bstack1l1ll11l11_opy_(bstack1111111ll_opy_, size):
  bstack1l111lll1_opy_ = []
  while len(bstack1111111ll_opy_) > size:
    bstack111l111111_opy_ = bstack1111111ll_opy_[:size]
    bstack1l111lll1_opy_.append(bstack111l111111_opy_)
    bstack1111111ll_opy_ = bstack1111111ll_opy_[size:]
  bstack1l111lll1_opy_.append(bstack1111111ll_opy_)
  return bstack1l111lll1_opy_
def bstack11ll11l11l_opy_(args):
  if bstack1ll11_opy_ (u"ࠩ࠰ࡱࠬ๹") in args and bstack1ll11_opy_ (u"ࠪࡴࡩࡨࠧ๺") in args:
    return True
  return False
@measure(event_name=EVENTS.bstack11ll1l111l_opy_, stage=STAGE.bstack1l111l1l_opy_)
def run_on_browserstack(bstack111ll111l_opy_=None, bstack11lll1111l_opy_=None, bstack1111111111_opy_=False):
  global CONFIG
  global bstack11llll1l1l_opy_
  global bstack1l11lll111_opy_
  global bstack11111l1ll1_opy_
  global global_config
  bstack11lll11ll1_opy_ = bstack1ll11_opy_ (u"ࠫࠬ๻")
  bstack1ll1l11ll_opy_ = bstack1ll11_opy_ (u"ࠧࠨ๼")
  bstack11ll11llll_opy_(bstack1l111l11_opy_, logger)
  if bstack111ll111l_opy_ and isinstance(bstack111ll111l_opy_, str):
    bstack111ll111l_opy_ = eval(bstack111ll111l_opy_)
  if bstack111ll111l_opy_:
    CONFIG = bstack111ll111l_opy_[bstack1ll11_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭๽")]
    bstack11llll1l1l_opy_ = bstack111ll111l_opy_[bstack1ll11_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨ๾")]
    bstack1l11lll111_opy_ = bstack111ll111l_opy_[bstack1ll11_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ๿")]
    global_config.bstack1ll11l111_opy_(bstack1ll11_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ຀"), bstack1l11lll111_opy_)
    bstack11lll11ll1_opy_ = bstack1ll11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠫກ")
  global_config.bstack1ll11l111_opy_(bstack1ll11_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭ຂ"), uuid4().__str__())
  logger.info(bstack1ll11_opy_ (u"࡙ࠬࡄࡌࠢࡵࡹࡳࠦࡳࡵࡣࡵࡸࡪࡪࠠࡸ࡫ࡷ࡬ࠥ࡯ࡤ࠻ࠢࠪ຃") + global_config.get_property(bstack1ll11_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨຄ")));
  logger.debug(bstack1ll11_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥ࠿ࠪ຅") + global_config.get_property(bstack1ll11_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪຆ")))
  if not bstack1111111111_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack11l1ll1l_opy_)
      return
    if sys.argv[1] == bstack1ll11_opy_ (u"ࠩ࠰࠱ࡻ࡫ࡲࡴ࡫ࡲࡲࠬງ") or sys.argv[1] == bstack1ll11_opy_ (u"ࠪ࠱ࡻ࠭ຈ"):
      logger.info(bstack1ll11_opy_ (u"ࠫࡇࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡔࡾࡺࡨࡰࡰࠣࡗࡉࡑࠠࡷࡽࢀࠫຉ").format(__version__))
      return
    if sys.argv[1] == bstack1ll11_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫຊ"):
      bstack1llll1l1ll_opy_()
      return
    if sys.argv[1] == bstack1ll11_opy_ (u"࠭࡬ࡰࡣࡧࠫ຋"):
      from browserstack_sdk.bstack111l11l1l1_opy_ import bstack11l1l11ll1_opy_
      bstack1l1llllll_opy_()
      bstack11l1l11ll1_opy_(CONFIG)
      return
  args = sys.argv
  bstack1l1llllll_opy_()
  global bstack11l1l1ll11_opy_
  try:
    from bstack_utils import constants as bstack11ll11l1_opy_
    override_value = CONFIG.get(bstack1ll11_opy_ (u"ࠧࡰࡸࡨࡶࡷ࡯ࡤࡦࡎࡲࡥࡩ࡚ࡥࡴࡶ࡬ࡲ࡬࠭ຌ"), False)
    bstack11l1l1ll11_opy_ = bool(override_value)
  except Exception as e:
    logger.error(bstack1ll11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡕࡖࡆࡔࡕࡍࡉࡋ࡟ࡍࡑࡄࡈࡤ࡚ࡅࡔࡖࡌࡒࡌࡀࠠࡼࡿࠥຍ").format(e))
    bstack11l1l1ll11_opy_ = False
  if bstack11l1l1ll11_opy_:
    bstack111ll1lll1_opy_ = CONFIG.get(bstack1ll11_opy_ (u"ࠩ࡯ࡳࡦࡪࡔࡦࡵࡷ࡭ࡳ࡭ࡈࡶࡤࡘࡖࡑ࠭ຎ")) or bstack11ll11l1_opy_.bstack111l11lll1_opy_
    logger.info(bstack1ll11_opy_ (u"ࠥࡋࡱࡵࡢࡢ࡮ࠣࡳࡻ࡫ࡲࡳ࡫ࡧࡩࡱࡵࡡࡥࡶࡨࡷࡹ࡯࡮ࡨࠢࡨࡲࡦࡨ࡬ࡦࡦ࠯ࠤࡺࡹࡩ࡯ࡩࠣ࡬ࡺࡨ࠺ࠡࡽࢀࠦຏ").format(bstack111ll1lll1_opy_))
    bstack11llll1l1l_opy_ = bstack111ll1lll1_opy_
    try:
      bstack11ll11l1_opy_.HTTPS_HUB = bstack111ll1lll1_opy_
      bstack11ll11l1_opy_.bstack111l111ll_opy_ = bstack111ll1lll1_opy_
    except Exception:
      pass
  global bstack11l1llll11_opy_
  global bstack11l1lll1l_opy_
  global PARALLELISE_VANILLA_PYTHON
  global PARALLELISE_THREADING_PYTHON
  global PLATFORM_INDEX
  global bstack111lll11_opy_
  global bstack1l11l1l11_opy_
  global bstack1l1ll111ll_opy_
  global bstack1l111l111l_opy_
  global bstack11ll111ll_opy_
  global bstack11l1ll1111_opy_
  bstack11l1lll1l_opy_ = len(CONFIG.get(bstack1ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧຐ"), []))
  if not bstack11lll11ll1_opy_:
    if args[1] == bstack1ll11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬຑ") or args[1] == bstack1ll11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧຒ") or args[1] == bstack1ll11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡨࡧࡱࡩࡷ࡯ࡣࠨຓ"):
      bstack11lll11ll1_opy_ = bstack1ll11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩດ")
      args = args[2:]
    elif args[1] == bstack1ll11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨຕ"):
      bstack11lll11ll1_opy_ = bstack1ll11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩຖ")
      args = args[2:]
    elif args[1] == bstack1ll11_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪທ"):
      bstack11lll11ll1_opy_ = bstack1ll11_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫຘ")
      args = args[2:]
    elif args[1] == bstack1ll11_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧນ"):
      bstack11lll11ll1_opy_ = bstack1ll11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨບ")
      args = args[2:]
    elif args[1] == bstack1ll11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨປ"):
      bstack11lll11ll1_opy_ = bstack1ll11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩຜ")
      args = args[2:]
    elif args[1] == bstack1ll11_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪຝ"):
      bstack11lll11ll1_opy_ = bstack1ll11_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫພ")
      args = args[2:]
    else:
      if not bstack1ll11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨຟ") in CONFIG or str(CONFIG[bstack1ll11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩຠ")]).lower() in [bstack1ll11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧມ"), bstack1ll11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩຢ"), bstack1ll11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠪຣ")]:
        bstack11lll11ll1_opy_ = bstack1ll11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠫ຤")
        args = args[1:]
      elif str(CONFIG[bstack1ll11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧລ")]).lower() == bstack1ll11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ຦"):
        bstack11lll11ll1_opy_ = bstack1ll11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬວ")
        args = args[1:]
      elif str(CONFIG[bstack1ll11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪຨ")]).lower() == bstack1ll11_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧຩ"):
        bstack11lll11ll1_opy_ = bstack1ll11_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨສ")
        args = args[1:]
      elif str(CONFIG[bstack1ll11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ຫ")]).lower() == bstack1ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫຬ"):
        bstack11lll11ll1_opy_ = bstack1ll11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬອ")
        args = args[1:]
      elif str(CONFIG[bstack1ll11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩຮ")]).lower() == bstack1ll11_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧຯ"):
        bstack11lll11ll1_opy_ = bstack1ll11_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨະ")
        args = args[1:]
      else:
        os.environ[bstack1ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫັ")] = bstack11lll11ll1_opy_
        bstack11l1l111l1_opy_(bstack11l1ll1ll1_opy_)
  os.environ[bstack1ll11_opy_ (u"ࠪࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡕࡔࡇࡇࠫາ")] = bstack11lll11ll1_opy_
  bstack11111l1ll1_opy_ = bstack11lll11ll1_opy_
  if cli.is_enabled(CONFIG):
    try:
      if bstack11lll11ll1_opy_ == bstack1ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫຳ") and bstack1111l1111l_opy_():
        bstack11l1111ll_opy_ = bstack11111l1lll_opy_[bstack1ll11_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘ࠲ࡈࡄࡅࠩິ")]
      elif bstack11lll11ll1_opy_ in [bstack1ll11_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧີ"), bstack1ll11_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ຶ")]:
        bstack11l1111ll_opy_ = bstack1ll11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧື")
      else:
        bstack11l1111ll_opy_ = bstack11lll11ll1_opy_
      bstack1lll111l_opy_.invoke(Events.bstack1111l111ll_opy_, bstack1l111ll11_opy_(
        sdk_version=__version__,
        path_config=bstack11l111l111_opy_(),
        path_project=os.getcwd(),
        test_framework=bstack11l1111ll_opy_,
        frameworks=[bstack11l1111ll_opy_],
        framework_versions={
          bstack11l1111ll_opy_: bstack11l1lllll1_opy_(bstack1ll11_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨຸ") if bstack11lll11ll1_opy_ in [bstack1ll11_opy_ (u"ࠪࡴࡦࡨ࡯ࡵູࠩ"), bstack1ll11_opy_ (u"ࠫࡷࡵࡢࡰࡶ຺ࠪ"), bstack1ll11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ົ")] else bstack11lll11ll1_opy_)
        },
        bs_config=CONFIG
      ))
      if cli.config and cli.config.get(bstack1ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣຼ"), None):
        CONFIG[bstack1ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤຽ")] = cli.config.get(bstack1ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠥ຾"), None)
    except Exception as e:
      bstack1lll111l_opy_.invoke(Events.bstack11111ll11l_opy_, e.__traceback__, 1)
    if bstack1l11lll111_opy_:
      CONFIG[bstack1ll11_opy_ (u"ࠤࡤࡴࡵࠨ຿")] = cli.config[bstack1ll11_opy_ (u"ࠥࡥࡵࡶࠢເ")]
      logger.info(bstack111llllll_opy_.format(CONFIG[bstack1ll11_opy_ (u"ࠫࡦࡶࡰࠨແ")]))
  else:
    bstack1lll111l_opy_.clear()
  global bstack111l1l1ll_opy_
  global bstack111llll11_opy_
  if bstack111ll111l_opy_:
    try:
      bstack11l111ll1_opy_ = datetime.datetime.now()
      os.environ[bstack1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧໂ")] = bstack11lll11ll1_opy_
      bstack1l1l1111_opy_ = bstack11ll11l1ll_opy_.bstack11l11l111_opy_(EVENTS.bstack1l111lll11_opy_)
      try:
        logger.info(bstack1ll11_opy_ (u"ࠨࡓࡦࡰࡧ࡭ࡳ࡭ࠠࡔࡆࡎࠤ࡙࡫ࡳࡵࠢࡄࡸࡹ࡫࡭ࡱࡶࡨࡨࠥ࡫ࡶࡦࡰࡷࠦໃ"))
        bstack11l1lll11l_opy_(bstack111l111l1l_opy_, CONFIG)
      finally:
        bstack11ll11l1ll_opy_.end(EVENTS.bstack1l111lll11_opy_.value, bstack1l1l1111_opy_ + bstack1ll11_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢໄ"), bstack1l1l1111_opy_ + bstack1ll11_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ໅"), status=True, failure=None, test_name=None)
      cli.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺ࡴࡦ࡮ࡣࡹ࡫ࡳࡵࡡࡤࡸࡹ࡫࡭ࡱࡶࡨࡨࠧໆ"), datetime.datetime.now() - bstack11l111ll1_opy_)
    except Exception as e:
      logger.debug(bstack1llll1ll1_opy_.format(str(e)))
  global bstack1llllllll1_opy_
  global bstack1ll1111l1_opy_
  global bstack11111ll1l_opy_
  global bstack1ll1l1l1l1_opy_
  global bstack11ll1lll_opy_
  global bstack1l111l11l1_opy_
  global bstack11l1l1ll1l_opy_
  global bstack1lll111ll_opy_
  global bstack1l1l1l1l11_opy_
  global bstack1lll1l1l1l_opy_
  global bstack1lll11ll1l_opy_
  global bstack1l111111l1_opy_
  global bstack11l1l1lll1_opy_
  global bstack1lll11lll_opy_
  global bstack1l1llll1l1_opy_
  global bstack111111l1l1_opy_
  global bstack1111l1l11_opy_
  global bstack111l1ll1l1_opy_
  global bstack11ll11lll1_opy_
  global bstack1l1l1lll1_opy_
  global bstack1l1l11ll1_opy_
  global bstack11l1lll1ll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1llllllll1_opy_ = webdriver.Remote.__init__
    bstack1ll1111l1_opy_ = WebDriver.quit
    bstack1l111111l1_opy_ = WebDriver.close
    bstack111111l1l1_opy_ = WebDriver.get
    bstack11l1lll1ll_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack111l1l1ll_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack1l11l1l1l_opy_
    bstack111llll11_opy_ = bstack1l11l1l1l_opy_()
  except Exception as e:
    pass
  try:
    global bstack1ll1111ll1_opy_
    from QWeb.keywords import browser
    bstack1ll1111ll1_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1111lllll_opy_(CONFIG) and bstack1l1111111_opy_():
    if bstack1lll11llll_opy_() < version.parse(bstack1l11l1l11l_opy_):
      logger.error(bstack1l1111ll11_opy_.format(bstack1lll11llll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack1ll11_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫ໇")) and callable(getattr(RemoteConnection, bstack1ll11_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰ່ࠬ"))):
          RemoteConnection._get_proxy_url = bstack1ll1ll1111_opy_
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          ClientConfig.get_proxy_url = bstack1ll1ll1111_opy_
      except Exception as e:
        logger.error(bstack1lll11l1l1_opy_.format(str(e)))
  if not CONFIG.get(bstack1ll11_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹ້ࠧ"), False) and not bstack111ll111l_opy_:
    logger.info(bstack11l11l1l_opy_)
  bstack11ll1l1l1_opy_ = not cli.is_enabled(CONFIG) and bstack11lll11ll1_opy_ not in [bstack1ll11_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲ໊ࠧ")]
  bstack111lll1l_opy_ = bstack11ll1l1l1_opy_ and bstack1ll11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨ໋ࠫ") in CONFIG and str(CONFIG[bstack1ll11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ໌")]).lower() != bstack1ll11_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨໍ")
  bstack1lll1l1l1_opy_ = bstack11ll1l1l1_opy_ and not bstack111lll1l_opy_ and (bstack11lll11ll1_opy_ != bstack1ll11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠫ໎") or (bstack11lll11ll1_opy_ == bstack1ll11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠬ໏") and not bstack111ll111l_opy_))
  if bstack11lll11ll1_opy_ not in [bstack1ll11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭໐")]:
    bstack11ll11llll_opy_(os.path.join(os.getcwd(), bstack1ll11_opy_ (u"࠭࡬ࡰࡩࠪ໑"), bstack1ll11_opy_ (u"ࠧ࡬ࡧࡼ࠱ࡲ࡫ࡴࡳ࡫ࡦࡷ࠳ࡰࡳࡰࡰࠪ໒")), logger)
  if (bstack11lll11ll1_opy_ in [bstack1ll11_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ໓"), bstack1ll11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ໔"), bstack1ll11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ໕")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      try:
        from pabot.pabot import QueueItem
        from pabot import pabot
      except Exception as e:
        logger.warning(bstack1l1111l1l_opy_ + str(e))
      if not is_robot_playwright_installed():
        try:
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
          WebDriverCreator._get_ff_profile = bstack111111l111_opy_
          bstack1l111l11l1_opy_ = WebDriverCache.close
        except Exception as e:
          logger.warning(bstack11ll11111l_opy_ + str(e))
        try:
          from AppiumLibrary.utils.applicationcache import ApplicationCache
          bstack11ll1lll_opy_ = ApplicationCache.close
        except Exception as e:
          logger.debug(bstack11111l1ll_opy_ + str(e))
    except Exception as e:
      bstack1ll1ll1l11_opy_(e, bstack11ll11111l_opy_)
    if bstack11lll11ll1_opy_ != bstack1ll11_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ໖"):
      bstack11111ll111_opy_()
    bstack11111ll1l_opy_ = Output.start_test
    bstack1ll1l1l1l1_opy_ = Output.end_test
    bstack11l1l1ll1l_opy_ = TestStatus.__init__
    bstack1l1l1l1l11_opy_ = pabot._run
    bstack1lll1l1l1l_opy_ = QueueItem.__init__
    bstack1lll11ll1l_opy_ = pabot._create_command_for_execution
    bstack1l1l1lll1_opy_ = pabot._report_results
  if bstack11lll11ll1_opy_ == bstack1ll11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ໗"):
    global bstack11lll11lll_opy_
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll1ll1l11_opy_(e, bstack1l111111l_opy_)
    bstack11l1l1lll1_opy_ = Runner.run_hook
    bstack1lll11lll_opy_ = Runner.load_hooks
    bstack1l1llll1l1_opy_ = Step.run
    try:
      sig = inspect.signature(bstack11l1l1lll1_opy_)
      params = list(sig.parameters.keys())
      bstack11lll11lll_opy_ = bstack1ll11_opy_ (u"࠭ࡣࡰࡰࡷࡩࡽࡺࠧ໘") in params
      logger.info(bstack1ll11_opy_ (u"ࠧࡅࡧࡷࡩࡨࡺࡥࡥࠢࡥࡩ࡭ࡧࡶࡦࠢࡵࡹࡳࡥࡨࡰࡱ࡮ࠤࡸ࡯ࡧ࡯ࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫ໙").format(bstack1ll11_opy_ (u"ࠨ࠳࠱࠶࠳࠼ࠠࠩࡹ࡬ࡸ࡭ࠦࡣࡰࡰࡷࡩࡽࡺࠩࠨ໚") if bstack11lll11lll_opy_ else bstack1ll11_opy_ (u"ࠩ࠴࠲࠸࠱ࠠࠩࡹ࡬ࡸ࡭ࡵࡵࡵࠢࡦࡳࡳࡺࡥࡹࡶࠬࠫ໛")))
    except Exception as e:
      logger.debug(bstack1ll11_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡧࡹࠦࡢࡦࡪࡤࡺࡪࠦࡲࡶࡰࡢ࡬ࡴࡵ࡫ࠡࡵ࡬࡫ࡳࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨໜ").format(str(e)))
      bstack11lll11lll_opy_ = None
  if bstack11lll11ll1_opy_ == bstack1ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫໝ"):
    try:
      from _pytest.config import Config
      bstack111l1ll1l1_opy_ = Config.getoption
      from _pytest import runner
      bstack11ll11lll1_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warning(bstack1ll11_opy_ (u"ࠧࠫࡳ࠻ࠢࠨࡷࠧໞ"), bstack1l1ll1111l_opy_, str(e))
    try:
      from pytest_bdd import reporting
      bstack1l1l11ll1_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1ll11_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧໟ"))
    if bstack1l1lll11_opy_():
      logger.warning(bstack11llllll1l_opy_[bstack1ll11_opy_ (u"ࠧࡔࡆࡎ࠱ࡌࡋࡎ࠮࠲࠳࠹ࠬ໠")])
  try:
    framework_name = bstack1ll11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ໡") if bstack11lll11ll1_opy_ in [bstack1ll11_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ໢"), bstack1ll11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ໣"), bstack1ll11_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ໤")] else bstack1ll1l11111_opy_(bstack11lll11ll1_opy_)
    bstack1l111ll1l1_opy_ = {
      bstack1ll11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪ࠭໥"): bstack1ll11_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨ໦") if bstack11lll11ll1_opy_ == bstack1ll11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ໧") and bstack1111l1111l_opy_() else framework_name,
      bstack1ll11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ໨"): bstack11l1lllll1_opy_(framework_name),
      bstack1ll11_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ໩"): __version__,
      bstack1ll11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡵࡴࡧࡧࠫ໪"): bstack11lll11ll1_opy_
    }
    if bstack11lll11ll1_opy_ in bstack1l1ll111_opy_ + bstack111ll1ll_opy_:
      if a11y.is_enabled_root(CONFIG):
        if bstack1ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ໫") in CONFIG:
          os.environ[bstack1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭໬")] = os.getenv(bstack1ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ໭"), json.dumps(CONFIG[bstack1ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ໮")]))
          CONFIG[bstack1ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ໯")].pop(bstack1ll11_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ໰"), None)
          CONFIG[bstack1ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ໱")].pop(bstack1ll11_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ໲"), None)
        bstack111111llll_opy_ = bstack1ll11_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩ໳") if CONFIG.get(bstack1ll11_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬ໴")) or bstack111111111l_opy_() else bstack1ll11_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩ໵")
        if bstack111111llll_opy_ == bstack1ll11_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬ໶"):
          try:
            import importlib.metadata as _111l1llll1_opy_
            bstack1l111ll1ll_opy_ = _111l1llll1_opy_.version(bstack1ll11_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ໷"))
          except Exception:
            bstack1l111ll1ll_opy_ = bstack1ll11_opy_ (u"ࠪࡹࡳࡱ࡮ࡰࡹࡱࠫ໸")
        else:
          bstack1l111ll1ll_opy_ = str(bstack1lll11llll_opy_())
        bstack1l111ll1l1_opy_[bstack1ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ໹")] = {
          bstack1ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ໺"): bstack111111llll_opy_,
          bstack1ll11_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧ໻"): bstack1l111ll1ll_opy_
        }
    bstack1l11l1lll_opy_, bstack1ll1lllll1_opy_ = None, {}
    bstack1111111l11_opy_ = None
    bstack11ll111l1l_opy_ = None
    def bstack1ll11111l_opy_():
      if bstack111lll1l_opy_:
        bstack11l1l1l111_opy_()
      elif bstack1lll1l1l1_opy_:
        bstack1l1lllll11_opy_()
    def bstack1ll1l1l11l_opy_():
      nonlocal bstack1l11l1lll_opy_, bstack1ll1lllll1_opy_
      if bstack11lll11ll1_opy_ not in [bstack1ll11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ໼")] and not cli.is_running():
        bstack1l11l1lll_opy_, bstack1ll1lllll1_opy_ = TestHubHandler.launch(CONFIG, bstack1l111ll1l1_opy_)
    if bstack111lll1l_opy_ or bstack1lll1l1l1_opy_:
      bstack1111111l11_opy_ = threading.Thread(target=bstack1ll11111l_opy_)
      bstack1111111l11_opy_.start()
    if bstack11lll11ll1_opy_ not in [bstack1ll11_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ໽")] and not cli.is_running():
      bstack11ll111l1l_opy_ = threading.Thread(target=bstack1ll1l1l11l_opy_)
      bstack11ll111l1l_opy_.start()
    if bstack1111111l11_opy_:
      bstack1111111l11_opy_.join()
    if bstack11ll111l1l_opy_:
      bstack11ll111l1l_opy_.join()
    if bstack1ll1lllll1_opy_.get(bstack1ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ໾")) is not None and a11y.bstack1111l1llll_opy_(CONFIG) is None:
      value = bstack1ll1lllll1_opy_[bstack1ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ໿")].get(bstack1ll11_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬༀ"))
      if value is not None:
          CONFIG[bstack1ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ༁")] = value
      else:
        logger.debug(bstack1ll11_opy_ (u"ࠨࡎࡰࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡧࡥࡹࡧࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠦ༂"))
  except Exception as e:
    logger.debug(bstack1l111l1ll_opy_.format(bstack1ll11_opy_ (u"ࠧࡕࡧࡶࡸࡍࡻࡢࠨ༃"), str(e)))
  if bstack11lll11ll1_opy_ == bstack1ll11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩ༄"):
    PARALLELISE_VANILLA_PYTHON = True
    if bstack111ll111l_opy_ and bstack1111111111_opy_:
      if cli.is_enabled(CONFIG):
        bstack111lll11_opy_ = cli.config.get(bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭༅"), {}).get(bstack1ll11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ༆")) if cli.config else None
      else:
        bstack111lll11_opy_ = CONFIG.get(bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ༇"), {}).get(bstack1ll11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ༈"))
      bstack1l1llll1ll_opy_(bstack1l111llll_opy_)
    elif bstack111ll111l_opy_:
      if cli.is_enabled(CONFIG):
        bstack111lll11_opy_ = cli.config.get(bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ༉"), {}).get(bstack1ll11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ༊")) if cli.config else None
      else:
        bstack111lll11_opy_ = CONFIG.get(bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ་"), {}).get(bstack1ll11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ༌"))
      global bstack11l1ll1l11_opy_
      try:
        if bstack11ll11l11l_opy_(bstack111ll111l_opy_[bstack1ll11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭།")]) and multiprocessing.current_process().name == bstack1ll11_opy_ (u"ࠫ࠵࠭༎"):
          bstack111ll111l_opy_[bstack1ll11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ༏")].remove(bstack1ll11_opy_ (u"࠭࠭࡮ࠩ༐"))
          bstack111ll111l_opy_[bstack1ll11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ༑")].remove(bstack1ll11_opy_ (u"ࠨࡲࡧࡦࠬ༒"))
          bstack111ll111l_opy_[bstack1ll11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ༓")] = bstack111ll111l_opy_[bstack1ll11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭༔")][0]
          with open(bstack111ll111l_opy_[bstack1ll11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ༕")], bstack1ll11_opy_ (u"ࠬࡸࠧ༖")) as f:
            file_content = f.read()
          bstack1llllll1l1_opy_ = bstack1ll11_opy_ (u"ࠨࠢࠣࡨࡵࡳࡲࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡹࡤ࡬ࠢ࡬ࡱࡵࡵࡲࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩࡀࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦࠪࡾࢁ࠮ࡁࠠࡧࡴࡲࡱࠥࡶࡤࡣࠢ࡬ࡱࡵࡵࡲࡵࠢࡓࡨࡧࡁࠠࡰࡩࡢࡨࡧࠦ࠽ࠡࡒࡧࡦ࠳ࡪ࡯ࡠࡤࡵࡩࡦࡱ࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡩ࡫ࡦࠡ࡯ࡲࡨࡤࡨࡲࡦࡣ࡮ࠬࡸ࡫࡬ࡧ࠮ࠣࡥࡷ࡭ࠬࠡࡶࡨࡱࡵࡵࡲࡢࡴࡼࠤࡂࠦ࠰ࠪ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡶࡵࡽ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡡࡳࡩࠣࡁࠥࡹࡴࡳࠪ࡬ࡲࡹ࠮ࡡࡳࡩࠬ࠯࠶࠶ࠩࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡥࡹࡥࡨࡴࡹࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡤࡷࠥ࡫࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡲࡤࡷࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡴ࡭࡟ࡥࡤࠫࡷࡪࡲࡦ࠭ࡣࡵ࡫࠱ࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠪࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࠠ࠾ࠢࡰࡳࡩࡥࡢࡳࡧࡤ࡯ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡒࡧࡦ࠳ࡪ࡯ࡠࡤࡵࡩࡦࡱࠠ࠾ࠢࡰࡳࡩࡥࡢࡳࡧࡤ࡯ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡒࡧࡦ࠭࠯࠮ࡴࡧࡷࡣࡹࡸࡡࡤࡧࠫ࠭ࡡࡴࠢࠣࠤ༗").format(str(bstack111ll111l_opy_))
          bstack11lll1l11_opy_ = bstack1llllll1l1_opy_ + file_content
          bstack111llll1ll_opy_ = bstack111ll111l_opy_[bstack1ll11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧ༘ࠪ")] + bstack1ll11_opy_ (u"ࠨࡡࡥࡷࡹࡧࡣ࡬ࡡࡷࡩࡲࡶ࠮ࡱࡻ༙ࠪ")
          with open(bstack111llll1ll_opy_, bstack1ll11_opy_ (u"ࠩࡺࠫ༚")):
            pass
          with open(bstack111llll1ll_opy_, bstack1ll11_opy_ (u"ࠥࡻ࠰ࠨ༛")) as f:
            f.write(bstack11lll1l11_opy_)
          import subprocess
          bstack1l1lll1111_opy_ = subprocess.run([bstack1ll11_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࠦ༜"), bstack111llll1ll_opy_])
          if os.path.exists(bstack111llll1ll_opy_):
            os.unlink(bstack111llll1ll_opy_)
          os._exit(bstack1l1lll1111_opy_.returncode)
        else:
          if bstack11ll11l11l_opy_(bstack111ll111l_opy_[bstack1ll11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ༝")]):
            bstack111ll111l_opy_[bstack1ll11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ༞")].remove(bstack1ll11_opy_ (u"ࠧ࠮࡯ࠪ༟"))
            bstack111ll111l_opy_[bstack1ll11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ༠")].remove(bstack1ll11_opy_ (u"ࠩࡳࡨࡧ࠭༡"))
            bstack111ll111l_opy_[bstack1ll11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭༢")] = bstack111ll111l_opy_[bstack1ll11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ༣")][0]
          bstack1l1llll1ll_opy_(bstack1l111llll_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack111ll111l_opy_[bstack1ll11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ༤")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1ll11_opy_ (u"࠭࡟ࡠࡰࡤࡱࡪࡥ࡟ࠨ༥")] = bstack1ll11_opy_ (u"ࠧࡠࡡࡰࡥ࡮ࡴ࡟ࡠࠩ༦")
          mod_globals[bstack1ll11_opy_ (u"ࠨࡡࡢࡪ࡮ࡲࡥࡠࡡࠪ༧")] = os.path.abspath(bstack111ll111l_opy_[bstack1ll11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ༨")])
          exec(open(bstack111ll111l_opy_[bstack1ll11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭༩")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1ll11_opy_ (u"ࠫࡈࡧࡵࡨࡪࡷࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠫ༪").format(str(e)))
          for driver in bstack11l1ll1l11_opy_:
            bstack11lll1111l_opy_.append({
              bstack1ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ༫"): bstack111ll111l_opy_[bstack1ll11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ༬")],
              bstack1ll11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭༭"): str(e),
              bstack1ll11_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ༮"): multiprocessing.current_process().name
            })
            bstack11l11l111l_opy_(driver, bstack1ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ༯"), bstack1ll11_opy_ (u"ࠥࡗࡪࡹࡳࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨ༰") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack11l1ll1l11_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1l11lll111_opy_, CONFIG, logger)
      bstack1111l1l1ll_opy_()
      bstack1111111l_opy_()
      percy.bstack111lllll1_opy_()
      bstack1l11l111_opy_ = {
        bstack1ll11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ༱"): args[0],
        bstack1ll11_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬ༲"): CONFIG,
        bstack1ll11_opy_ (u"࠭ࡈࡖࡄࡢ࡙ࡗࡒࠧ༳"): bstack11llll1l1l_opy_,
        bstack1ll11_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ༴"): bstack1l11lll111_opy_
      }
      if bstack1ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶ༵ࠫ") in CONFIG:
        bstack1l1l1lll1l_opy_ = bstack1111l111l_opy_(args, logger, CONFIG, BROWSERSTACK_AUTOMATION, bstack11l1lll1l_opy_)
        bstack1l1ll111ll_opy_ = bstack1l1l1lll1l_opy_.bstack11l1ll1ll_opy_(run_on_browserstack, bstack1l11l111_opy_, bstack11ll11l11l_opy_(args))
      else:
        if bstack11ll11l11l_opy_(args):
          bstack1l11l111_opy_[bstack1ll11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ༶")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1l11l111_opy_,))
          test.start()
          test.join()
        else:
          bstack1l1llll1ll_opy_(bstack1l111llll_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1ll11_opy_ (u"ࠪࡣࡤࡴࡡ࡮ࡧࡢࡣ༷ࠬ")] = bstack1ll11_opy_ (u"ࠫࡤࡥ࡭ࡢ࡫ࡱࡣࡤ࠭༸")
          mod_globals[bstack1ll11_opy_ (u"ࠬࡥ࡟ࡧ࡫࡯ࡩࡤࡥ༹ࠧ")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack11lll11ll1_opy_ == bstack1ll11_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ༺") or bstack11lll11ll1_opy_ == bstack1ll11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭༻"):
    percy.init(bstack1l11lll111_opy_, CONFIG, logger)
    percy.bstack111lllll1_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1ll1ll1l11_opy_(e, bstack11ll11111l_opy_)
    bstack1111l1l1ll_opy_()
    if bstack111lll11_opy_:
      os.environ[bstack1ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡅࡇࡉࡅ࡚ࡒࡔࡠࡎࡒࡇࡆࡒ࡟ࡊࡆࠪ༼")] = bstack111lll11_opy_
    bstack1l1llll1ll_opy_(bstack1l1l11l1l1_opy_)
    if BROWSERSTACK_AUTOMATION:
      bstack1lll1l1lll_opy_(bstack1l1l11l1l1_opy_, args)
      if bstack1ll11_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ༽") in args:
        i = args.index(bstack1ll11_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨ༾"))
        args.pop(i)
        args.pop(i)
      if bstack1ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ༿") not in CONFIG:
        CONFIG[bstack1ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨཀ")] = [{}]
        bstack11l1lll1l_opy_ = 1
      if bstack11l1llll11_opy_ == 0:
        bstack11l1llll11_opy_ = 1
      args.insert(0, str(bstack11l1llll11_opy_))
      args.insert(0, str(bstack1ll11_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫཁ")))
    if TestHubHandler.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack11l111111_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1l1l1l1ll1_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack1ll11_opy_ (u"ࠢࡓࡑࡅࡓ࡙ࡥࡏࡑࡖࡌࡓࡓ࡙ࠢག"),
        ).parse_args(bstack11l111111_opy_)
        bstack1111111l1_opy_ = args.index(bstack11l111111_opy_[0]) if len(bstack11l111111_opy_) > 0 else len(args)
        args.insert(bstack1111111l1_opy_, str(bstack1ll11_opy_ (u"ࠨ࠯࠰ࡰ࡮ࡹࡴࡦࡰࡨࡶࠬགྷ")))
        args.insert(bstack1111111l1_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡵࡳࡧࡵࡴࡠ࡮࡬ࡷࡹ࡫࡮ࡦࡴ࠱ࡴࡾ࠭ང"))))
        if bstack1l1ll11ll1_opy_.bstack1lll1lllll_opy_(CONFIG):
          args.insert(bstack1111111l1_opy_, str(bstack1ll11_opy_ (u"ࠪ࠱࠲ࡲࡩࡴࡶࡨࡲࡪࡸࠧཅ")))
          args.insert(bstack1111111l1_opy_ + 1, str(bstack1ll11_opy_ (u"ࠫࡗ࡫ࡴࡳࡻࡉࡥ࡮ࡲࡥࡥ࠼ࡾࢁࠬཆ").format(bstack1l1ll11ll1_opy_.bstack1111llll11_opy_(CONFIG))))
        if bstack1lll1111ll_opy_(os.environ.get(bstack1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࠪཇ"))) and str(os.environ.get(bstack1ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࡣ࡙ࡋࡓࡕࡕࠪ཈"), bstack1ll11_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬཉ"))) != bstack1ll11_opy_ (u"ࠨࡰࡸࡰࡱ࠭ཊ"):
          for bstack1l111l1ll1_opy_ in bstack1l1l1l1ll1_opy_:
            args.remove(bstack1l111l1ll1_opy_)
          test_files = os.environ.get(bstack1ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭ཋ")).split(bstack1ll11_opy_ (u"ࠪ࠰ࠬཌ"))
          for bstack1llll1l11_opy_ in test_files:
            args.append(bstack1llll1l11_opy_)
      except Exception as e:
        logger.error(bstack1ll11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡤࡸࡹࡧࡣࡩ࡫ࡱ࡫ࠥࡲࡩࡴࡶࡨࡲࡪࡸࠠࡧࡱࡵࠤࢀࢃ࠮ࠡࡇࡵࡶࡴࡸࠠ࠮ࠢࡾࢁࠧཌྷ").format(bstack1ll1l1lll_opy_, e))
    pabot.main(args)
  elif bstack11lll11ll1_opy_ == bstack1ll11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ཎ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1ll1ll1l11_opy_(e, bstack11ll11111l_opy_)
    for a in args:
      if bstack1ll11_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬཏ") in a:
        PLATFORM_INDEX = int(a.split(bstack1ll11_opy_ (u"ࠧ࠻ࠩཐ"))[1])
      if bstack1ll11_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡅࡇࡉࡐࡔࡉࡁࡍࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬད") in a:
        bstack111lll11_opy_ = str(a.split(bstack1ll11_opy_ (u"ࠩ࠽ࠫདྷ"))[1])
      if bstack1ll11_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡆࡐࡎࡇࡒࡈࡕࠪན") in a:
        bstack1l11l1l11_opy_ = str(a.split(bstack1ll11_opy_ (u"ࠫ࠿࠭པ"))[1])
    if os.environ.get(bstack1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡉࡋࡆࡂࡗࡏࡘࡤࡒࡏࡄࡃࡏࡣࡎࡊࠧཕ")):
      bstack111lll11_opy_ = os.environ.get(bstack1ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡊࡅࡇࡃࡘࡐ࡙ࡥࡌࡐࡅࡄࡐࡤࡏࡄࠨབ"))
    if bstack111lll11_opy_:
      if bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫབྷ") not in CONFIG:
        CONFIG[bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬམ")] = {}
      CONFIG[bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ཙ")][bstack1ll11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬཚ")] = bstack111lll11_opy_
    bstack11111111_opy_ = None
    bstack111lll111_opy_ = None
    if bstack1ll11_opy_ (u"ࠫ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠪཛ") in args:
      i = args.index(bstack1ll11_opy_ (u"ࠬ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠫཛྷ"))
      args.pop(i)
      bstack11111111_opy_ = args.pop(i)
    if bstack1ll11_opy_ (u"࠭࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࠩཝ") in args:
      i = args.index(bstack1ll11_opy_ (u"ࠧ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࠪཞ"))
      args.pop(i)
      bstack111lll111_opy_ = args.pop(i)
    if bstack11111111_opy_ is not None:
      global bstack111l1111l1_opy_
      bstack111l1111l1_opy_ = bstack11111111_opy_
    if bstack111lll111_opy_ is not None and int(PLATFORM_INDEX) < 0:
      PLATFORM_INDEX = int(bstack111lll111_opy_)
    if cli.is_enabled(CONFIG):
      if cli.bstack1ll1111lll_opy_():
        bstack1lll111l_opy_.invoke(Events.CONNECT, bstack11lll11ll_opy_())
        cli.bstack11lll1111_opy_(PLATFORM_INDEX)
      if cli.bstack11ll1lll11_opy_(bstack1l11l111l_opy_):
        cli.bstack111111lll1_opy_()
    bstack1l1llll1ll_opy_(bstack1l1l11l1l1_opy_)
    run_cli(args)
    if bstack1ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬཟ") in multiprocessing.current_process().__dict__.keys():
      for bstack1lll11lll1_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack11lll1111l_opy_.append(bstack1lll11lll1_opy_)
  elif bstack11lll11ll1_opy_ == bstack1ll11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩའ"):
    bstack1ll11l11l1_opy_ = bstack1lll1l111l_opy_(args, logger, CONFIG, BROWSERSTACK_AUTOMATION)
    bstack1ll11l11l1_opy_.bstack11lll1ll1l_opy_()
    bstack1111l1l1ll_opy_()
    PARALLELISE_THREADING_PYTHON = True
    bstack11ll111ll_opy_ = bstack1ll11l11l1_opy_.bstack1ll1ll1l_opy_()
    bstack1ll11l11l1_opy_.bstack1l11l111_opy_(bstack11l1l1lll_opy_)
    bstack1ll11l11l1_opy_.bstack1l11111l1l_opy_()
    bstack1ll1l1ll1l_opy_(bstack11lll11ll1_opy_, CONFIG, bstack1ll11l11l1_opy_.bstack1ll1l1lll1_opy_())
    bstack1ll1lll11l_opy_.end(EVENTS.bstack11ll1l111l_opy_.value, EVENTS.bstack11ll1l111l_opy_.value + bstack1ll11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥཡ"), EVENTS.bstack11ll1l111l_opy_.value + bstack1ll11_opy_ (u"ࠦ࠿࡫࡮ࡥࠤར"), status=True, failure=None, test_name=SESSION_NAME)
    bstack1l1l11l11l_opy_ = bstack1ll11l11l1_opy_.bstack11l1ll1ll_opy_(bstack1llll1l1l1_opy_, {
      bstack1ll11_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬལ"): CONFIG,
      bstack1ll11_opy_ (u"࠭ࡈࡖࡄࡢ࡙ࡗࡒࠧཤ"): bstack11llll1l1l_opy_,
      bstack1ll11_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩཥ"): bstack1l11lll111_opy_,
      bstack1ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫས"): BROWSERSTACK_AUTOMATION,
      bstack1ll11_opy_ (u"ࠩࡒ࡚ࡊࡘࡒࡊࡆࡈࡣࡑࡕࡁࡅࡡࡗࡉࡘ࡚ࡉࡏࡉࠪཧ"): bstack11l1l1ll11_opy_
    })
    if not bstack111ll111l_opy_:
      bstack1ll1l11ll_opy_ = bstack11ll11l1ll_opy_.bstack11l11l111_opy_(EVENTS.bstack1111ll1ll_opy_.value)
    try:
      bstack11l1l11l_opy_, bstack11llll111_opy_ = map(list, zip(*bstack1l1l11l11l_opy_))
      bstack1l111l111l_opy_ = bstack11l1l11l_opy_[0]
      for status_code in bstack11llll111_opy_:
        if status_code != 0:
          bstack11l1ll1111_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack1ll11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡢࡸࡨࠤࡪࡸࡲࡰࡴࡶࠤࡦࡴࡤࠡࡵࡷࡥࡹࡻࡳࠡࡥࡲࡨࡪ࠴ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࠾ࠥࢁࡽࠣཨ").format(str(e)))
  elif bstack11lll11ll1_opy_ == bstack1ll11_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫཀྵ"):
    try:
      from behave.__main__ import main as bstack111ll11l1_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1ll1ll1l11_opy_(e, bstack1l111111l_opy_)
    bstack1111l1l1ll_opy_()
    PARALLELISE_THREADING_PYTHON = True
    bstack1ll1ll1lll_opy_ = 1
    if bstack1ll11_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬཪ") in CONFIG:
      bstack1ll1ll1lll_opy_ = CONFIG[bstack1ll11_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ཫ")]
    if bstack1ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪཬ") in CONFIG:
      bstack1lllllll1_opy_ = int(bstack1ll1ll1lll_opy_) * int(len(CONFIG[bstack1ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ཭")]))
    else:
      bstack1lllllll1_opy_ = int(bstack1ll1ll1lll_opy_)
    config = Configuration(args)
    bstack111ll1l1_opy_ = config.paths
    if len(bstack111ll1l1_opy_) == 0:
      import glob
      pattern = bstack1ll11_opy_ (u"ࠩ࠭࠮࠴࠰࠮ࡧࡧࡤࡸࡺࡸࡥࠨ཮")
      bstack11ll1l11l1_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack11ll1l11l1_opy_)
      config = Configuration(args)
      bstack111ll1l1_opy_ = config.paths
    bstack1l1ll1l1_opy_ = [os.path.normpath(item) for item in bstack111ll1l1_opy_]
    bstack11l1lll1l1_opy_ = [os.path.normpath(item) for item in args]
    bstack1111l1l111_opy_ = [item for item in bstack11l1lll1l1_opy_ if item not in bstack1l1ll1l1_opy_]
    import platform as pf
    if pf.system().lower() == bstack1ll11_opy_ (u"ࠪࡻ࡮ࡴࡤࡰࡹࡶࠫ཯"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1l1ll1l1_opy_ = [str(PurePosixPath(PureWindowsPath(bstack111l1111_opy_)))
                    for bstack111l1111_opy_ in bstack1l1ll1l1_opy_]
    try:
      bstack1l1lll1l1l_opy_ = bstack111ll1l11_opy_(args, logger, CONFIG, BROWSERSTACK_AUTOMATION)
      bstack1l1lll1l1l_opy_.bstack111111l11l_opy_(bstack1l1ll1l1_opy_)
      bstack1l1lll1l1l_opy_.bstack1l11111l1l_opy_()
      bstack1l1ll1l1_opy_ = bstack1l1lll1l1l_opy_.bstack1l1l1ll1_opy_()
    except Exception as e:
      logger.error(bstack1ll11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡢࡲࡳࡰࡾࠦࡴࡦࡵࡷࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤ࡫ࡵࡲࠡࡤࡨ࡬ࡦࡼࡥ࠻ࠢࠨࡷࠧ཰"), e, exc_info=True)
      logger.info(bstack1ll11_opy_ (u"ࠧࡉ࡯࡯ࡶ࡬ࡲࡺ࡯࡮ࡨࠢࡺ࡭ࡹ࡮ࠠࡰࡴ࡬࡫࡮ࡴࡡ࡭ࠢࡶࡴࡪࡩࠠࡧ࡫࡯ࡩࡸࠦࡷࡪࡶ࡫ࡳࡺࡺࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴཱࠢ"))
    bstack1lllllllll_opy_ = []
    for spec in bstack1l1ll1l1_opy_:
      bstack111ll1l1ll_opy_ = []
      bstack111ll1l1ll_opy_ += bstack1111l1l111_opy_
      bstack111ll1l1ll_opy_.append(spec)
      bstack1lllllllll_opy_.append(bstack111ll1l1ll_opy_)
    execution_items = []
    for bstack111ll1l1ll_opy_ in bstack1lllllllll_opy_:
      if bstack1ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴིࠩ") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack1ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵཱིࠪ")]):
          item = {}
          item[bstack1ll11_opy_ (u"ࠨࡣࡵ࡫ུࠬ")] = bstack1ll11_opy_ (u"ཱུࠩࠣࠫ").join(bstack111ll1l1ll_opy_)
          item[bstack1ll11_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩྲྀ")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack1ll11_opy_ (u"ࠫࡦࡸࡧࠨཷ")] = bstack1ll11_opy_ (u"ࠬࠦࠧླྀ").join(bstack111ll1l1ll_opy_)
        item[bstack1ll11_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬཹ")] = 0
        execution_items.append(item)
    bstack111ll11l1l_opy_ = bstack1l1ll11l11_opy_(execution_items, bstack1lllllll1_opy_)
    for execution_item in bstack111ll11l1l_opy_:
      bstack1lll1l11l1_opy_ = []
      for item in execution_item:
        bstack1lll1l11l1_opy_.append(bstack1111l11l1l_opy_(name=str(item[bstack1ll11_opy_ (u"ࠧࡪࡰࡧࡩࡽེ࠭")]),
                                             target=bstack1ll1111l_opy_,
                                             args=(item[bstack1ll11_opy_ (u"ࠨࡣࡵ࡫ཻࠬ")],)))
      for t in bstack1lll1l11l1_opy_:
        t.start()
      for t in bstack1lll1l11l1_opy_:
        t.join()
  else:
    bstack11l1l111l1_opy_(bstack11l1ll1ll1_opy_)
  if not bstack111ll111l_opy_:
    bstack1111ll111l_opy_()
    if bstack1ll1l11ll_opy_:
      bstack11ll11l1ll_opy_.end(EVENTS.bstack1111ll1ll_opy_.value, bstack1ll1l11ll_opy_ + bstack1ll11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤོ"), bstack1ll1l11ll_opy_ + bstack1ll11_opy_ (u"ࠥ࠾ࡪࡴࡤཽࠣ"), status=True, failure=None, test_name=None)
  logger_utils.bstack1ll11ll1l1_opy_()
def browserstack_initialize(bstack1l1l1l11l_opy_=None):
  logger.info(bstack1ll11_opy_ (u"ࠫࡗࡻ࡮࡯࡫ࡱ࡫࡙ࠥࡄࡌࠢࡺ࡭ࡹ࡮ࠠࡢࡴࡪࡷ࠿ࠦࠧཾ") + str(bstack1l1l1l11l_opy_))
  run_on_browserstack(bstack1l1l1l11l_opy_, None, True)
@measure(event_name=EVENTS.bstack111l1ll11_opy_, stage=STAGE.bstack11111llll_opy_, bstack11lll1l111_opy_=SESSION_NAME)
def bstack1111ll111l_opy_():
  global CONFIG
  global bstack11111l1ll1_opy_
  global bstack11l1ll1111_opy_
  global bstack1ll1l11l1l_opy_
  global global_config
  global _11111ll11_opy_
  bstack1lll1l1ll_opy_.bstack11111llll1_opy_()
  _11111ll11_opy_ = cli.is_running()
  if _11111ll11_opy_:
    bstack1lll111l_opy_.invoke(Events.bstack11lll1l11l_opy_)
  else:
    bstack1l1l1llll1_opy_ = bstack1l1ll11ll1_opy_.get_instance(config=CONFIG)
    bstack1l1l1llll1_opy_.bstack1ll1lll1ll_opy_(CONFIG)
  hashed_id = None
  bstack1l1111111l_opy_ = None
  def bstack111llll1l1_opy_():
    try:
      if bstack11111l1ll1_opy_ == bstack1ll11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬཿ"):
        if not cli.is_enabled(CONFIG):
          TestHubHandler.stop()
      else:
        TestHubHandler.stop()
    except Exception as e:
      logger.debug(bstack1ll11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡹࡴࡰࡲࡳ࡭ࡳ࡭ࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࡾࢁྀࠧ").format(e))
  def bstack11l11111ll_opy_():
    try:
      if not cli.is_enabled(CONFIG):
        bstack11l11l1lll_opy_.bstack11llll1111_opy_()
    except Exception as e:
      logger.debug(bstack1ll11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡰࡳ࡫ࡱࡸ࡮ࡴࡧࠡࡤࡸ࡭ࡱࡪࠠ࡭࡫ࡱ࡯࠿ࠦࡻࡾࠤཱྀ").format(e))
  def bstack111l1l1lll_opy_():
    nonlocal hashed_id, bstack1l1111111l_opy_
    try:
      if bstack1ll11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬྂ") in CONFIG and str(CONFIG[bstack1ll11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ྃ")]).lower() != bstack1ll11_opy_ (u"ࠪࡪࡦࡲࡳࡦ྄ࠩ"):
        hashed_id, bstack1l1111111l_opy_ = bstack11l1ll1l1_opy_()
      else:
        hashed_id, bstack1l1111111l_opy_ = get_build_link()
    except Exception as e:
      logger.debug(bstack1ll11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࠣࡰ࡮ࡴ࡫࠻ࠢࡾࢁࠧ྅").format(e))
  bstack1lll1l111_opy_ = threading.Thread(target=bstack111llll1l1_opy_)
  bstack111l11l11l_opy_ = threading.Thread(target=bstack11l11111ll_opy_)
  bstack111l1111l_opy_ = threading.Thread(target=bstack111l1l1lll_opy_)
  threads = [bstack1lll1l111_opy_, bstack111l11l11l_opy_, bstack111l1111l_opy_]
  for thread in threads:
    try:
      thread.start()
    except Exception as e:
      logger.debug(bstack1ll11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡸࡺࡡࡳࡶ࡬ࡲ࡬ࠦࡴࡩࡴࡨࡥࡩࠦࡻࡾ࠼ࠣࡿࢂࠨ྆").format(thread.name, e))
  for thread in threads:
    try:
      thread.join()
    except Exception as e:
      logger.debug(bstack1ll11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡰ࡯ࡪࡰ࡬ࡲ࡬ࠦࡴࡩࡴࡨࡥࡩࠦࡻࡾ࠼ࠣࡿࢂࠨ྇").format(thread.name, e))
  bstack1ll1lll1l_opy_(hashed_id)
  logger.info(bstack1ll11_opy_ (u"ࠧࡔࡆࡎࠤࡷࡻ࡮ࠡࡧࡱࡨࡪࡪࠠࡧࡱࡵࠤ࡮ࡪ࠺ࠨྈ") + global_config.get_property(bstack1ll11_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪྉ"), bstack1ll11_opy_ (u"ࠩࠪྊ")) + bstack1ll11_opy_ (u"ࠪ࠰ࠥࡺࡥࡴࡶ࡫ࡹࡧࠦࡩࡥ࠼ࠣࠫྋ") + os.getenv(bstack1ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩྌ"), bstack1ll11_opy_ (u"ࠬ࠭ྍ")))
  if hashed_id is not None and bstack11l11l1l1_opy_() != -1:
    sessions = bstack1ll1l111l_opy_(hashed_id)
    bstack11ll1llll1_opy_(sessions, bstack1l1111111l_opy_)
  if bstack11111l1ll1_opy_ == bstack1ll11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ྎ") and bstack11l1ll1111_opy_ != 0:
    sys.exit(bstack11l1ll1111_opy_)
  if bstack11111l1ll1_opy_ == bstack1ll11_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧྏ") and bstack1ll1l11l1l_opy_ != 0:
    sys.exit(bstack1ll1l11l1l_opy_)
def bstack1ll1lll1l_opy_(new_id):
    global bstack11l1ll11l1_opy_
    bstack11l1ll11l1_opy_ = new_id
def bstack1ll1l11111_opy_(bstack1111llllll_opy_):
  if bstack1111llllll_opy_:
    return bstack1111llllll_opy_.capitalize()
  else:
    return bstack1ll11_opy_ (u"ࠨࠩྐ")
@measure(event_name=EVENTS.bstack1111ll1l1l_opy_, stage=STAGE.bstack11111llll_opy_, bstack11lll1l111_opy_=SESSION_NAME)
def bstack11llll11l1_opy_(bstack11l1ll1l1l_opy_):
  if bstack1ll11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧྑ") in bstack11l1ll1l1l_opy_ and bstack11l1ll1l1l_opy_[bstack1ll11_opy_ (u"ࠪࡲࡦࡳࡥࠨྒ")] != bstack1ll11_opy_ (u"ࠫࠬྒྷ"):
    return bstack11l1ll1l1l_opy_[bstack1ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪྔ")]
  else:
    bstack11lll1l111_opy_ = bstack1ll11_opy_ (u"ࠨࠢྕ")
    if bstack1ll11_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧྖ") in bstack11l1ll1l1l_opy_ and bstack11l1ll1l1l_opy_[bstack1ll11_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨྗ")] != None:
      bstack11lll1l111_opy_ += bstack11l1ll1l1l_opy_[bstack1ll11_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩ྘")] + bstack1ll11_opy_ (u"ࠥ࠰ࠥࠨྙ")
      if bstack11l1ll1l1l_opy_[bstack1ll11_opy_ (u"ࠫࡴࡹࠧྚ")] == bstack1ll11_opy_ (u"ࠧ࡯࡯ࡴࠤྛ"):
        bstack11lll1l111_opy_ += bstack1ll11_opy_ (u"ࠨࡩࡐࡕࠣࠦྜ")
      bstack11lll1l111_opy_ += (bstack11l1ll1l1l_opy_[bstack1ll11_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫྜྷ")] or bstack1ll11_opy_ (u"ࠨࠩྞ"))
      return bstack11lll1l111_opy_
    else:
      bstack11lll1l111_opy_ += bstack1ll1l11111_opy_(bstack11l1ll1l1l_opy_[bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪྟ")]) + bstack1ll11_opy_ (u"ࠥࠤࠧྠ") + (
              bstack11l1ll1l1l_opy_[bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ྡ")] or bstack1ll11_opy_ (u"ࠬ࠭ྡྷ")) + bstack1ll11_opy_ (u"ࠨࠬࠡࠤྣ")
      if bstack11l1ll1l1l_opy_[bstack1ll11_opy_ (u"ࠧࡰࡵࠪྤ")] == bstack1ll11_opy_ (u"࡙ࠣ࡬ࡲࡩࡵࡷࡴࠤྥ"):
        bstack11lll1l111_opy_ += bstack1ll11_opy_ (u"ࠤ࡚࡭ࡳࠦࠢྦ")
      bstack11lll1l111_opy_ += bstack11l1ll1l1l_opy_[bstack1ll11_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧྦྷ")] or bstack1ll11_opy_ (u"ࠫࠬྨ")
      return bstack11lll1l111_opy_
@measure(event_name=EVENTS.bstack111l11llll_opy_, stage=STAGE.bstack11111llll_opy_, bstack11lll1l111_opy_=SESSION_NAME)
def bstack11111111ll_opy_(bstack1ll1l1111_opy_):
  if bstack1ll1l1111_opy_ == bstack1ll11_opy_ (u"ࠧࡪ࡯࡯ࡧࠥྩ"):
    return bstack1ll11_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡩࡵࡩࡪࡴ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡩࡵࡩࡪࡴࠢ࠿ࡅࡲࡱࡵࡲࡥࡵࡧࡧࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩྪ")
  elif bstack1ll1l1111_opy_ == bstack1ll11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢྫ"):
    return bstack1ll11_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡶࡪࡪ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡴࡨࡨࠧࡄࡆࡢ࡫࡯ࡩࡩࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫྫྷ")
  elif bstack1ll1l1111_opy_ == bstack1ll11_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤྭ"):
    return bstack1ll11_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿࡭ࡲࡦࡧࡱ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧ࡭ࡲࡦࡧࡱࠦࡃࡖࡡࡴࡵࡨࡨࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪྮ")
  elif bstack1ll1l1111_opy_ == bstack1ll11_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥྯ"):
    return bstack1ll11_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡳࡧࡧ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡸࡥࡥࠤࡁࡉࡷࡸ࡯ࡳ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧྰ")
  elif bstack1ll1l1111_opy_ == bstack1ll11_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࠢྱ"):
    return bstack1ll11_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࠦࡩࡪࡧ࠳࠳࠸࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࠨ࡫ࡥࡢ࠵࠵࠺ࠧࡄࡔࡪ࡯ࡨࡳࡺࡺ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬྲ")
  elif bstack1ll1l1111_opy_ == bstack1ll11_opy_ (u"ࠣࡴࡸࡲࡳ࡯࡮ࡨࠤླ"):
    return bstack1ll11_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡧࡲࡡࡤ࡭࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡧࡲࡡࡤ࡭ࠥࡂࡗࡻ࡮࡯࡫ࡱ࡫ࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪྴ")
  else:
    return bstack1ll11_opy_ (u"ࠪࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡢ࡭ࡣࡦ࡯ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡢ࡭ࡣࡦ࡯ࠧࡄࠧྵ") + bstack1ll1l11111_opy_(
      bstack1ll1l1111_opy_) + bstack1ll11_opy_ (u"ࠫࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪྶ")
def bstack111lll1111_opy_(session):
  return bstack1ll11_opy_ (u"ࠬࡂࡴࡳࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡵࡳࡼࠨ࠾࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠢࡶࡩࡸࡹࡩࡰࡰ࠰ࡲࡦࡳࡥࠣࡀ࠿ࡥࠥ࡮ࡲࡦࡨࡀࠦࢀࢃࠢࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤࡢࡦࡱࡧ࡮࡬ࠤࡁࡿࢂࡂ࠯ࡢࡀ࠿࠳ࡹࡪ࠾ࡼࡿࡾࢁࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼࠰ࡶࡵࡂࠬྷ").format(
    session[bstack1ll11_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨࡥࡵࡳ࡮ࠪྸ")], bstack11llll11l1_opy_(session), bstack11111111ll_opy_(session[bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡳࡵࡣࡷࡹࡸ࠭ྐྵ")]),
    bstack11111111ll_opy_(session[bstack1ll11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨྺ")]),
    bstack1ll1l11111_opy_(session[bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪྻ")] or session[bstack1ll11_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪྼ")] or bstack1ll11_opy_ (u"ࠫࠬ྽")) + bstack1ll11_opy_ (u"ࠧࠦࠢ྾") + (session[bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ྿")] or bstack1ll11_opy_ (u"ࠧࠨ࿀")),
    session[bstack1ll11_opy_ (u"ࠨࡱࡶࠫ࿁")] + bstack1ll11_opy_ (u"ࠤࠣࠦ࿂") + session[bstack1ll11_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ࿃")], session[bstack1ll11_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭࿄")] or bstack1ll11_opy_ (u"ࠬ࠭࿅"),
    session[bstack1ll11_opy_ (u"࠭ࡣࡳࡧࡤࡸࡪࡪ࡟ࡢࡶ࿆ࠪ")] if session[bstack1ll11_opy_ (u"ࠧࡤࡴࡨࡥࡹ࡫ࡤࡠࡣࡷࠫ࿇")] else bstack1ll11_opy_ (u"ࠨࠩ࿈"))
@measure(event_name=EVENTS.bstack1lll11111l_opy_, stage=STAGE.bstack11111llll_opy_, bstack11lll1l111_opy_=SESSION_NAME)
def bstack11ll1llll1_opy_(sessions, bstack1l1111111l_opy_):
  try:
    bstack1ll1ll1ll1_opy_ = bstack1ll11_opy_ (u"ࠤࠥ࿉")
    if not os.path.exists(bstack1l11l111l1_opy_):
      os.mkdir(bstack1l11l111l1_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll11_opy_ (u"ࠪࡥࡸࡹࡥࡵࡵ࠲ࡶࡪࡶ࡯ࡳࡶ࠱࡬ࡹࡳ࡬ࠨ࿊")), bstack1ll11_opy_ (u"ࠫࡷ࠭࿋")) as f:
      bstack1ll1ll1ll1_opy_ = f.read()
    bstack1ll1ll1ll1_opy_ = bstack1ll1ll1ll1_opy_.replace(bstack1ll11_opy_ (u"ࠬࢁࠥࡓࡇࡖ࡙ࡑ࡚ࡓࡠࡅࡒ࡙ࡓ࡚ࠥࡾࠩ࿌"), str(len(sessions)))
    bstack1ll1ll1ll1_opy_ = bstack1ll1ll1ll1_opy_.replace(bstack1ll11_opy_ (u"࠭ࡻࠦࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠩࢂ࠭࿍"), bstack1l1111111l_opy_)
    bstack1ll1ll1ll1_opy_ = bstack1ll1ll1ll1_opy_.replace(bstack1ll11_opy_ (u"ࠧࡼࠧࡅ࡙ࡎࡒࡄࡠࡐࡄࡑࡊࠫࡽࠨ࿎"),
                                              sessions[0].get(bstack1ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟࡯ࡣࡰࡩࠬ࿏")) if sessions[0] else bstack1ll11_opy_ (u"ࠩࠪ࿐"))
    with open(os.path.join(bstack1l11l111l1_opy_, bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡵࡩࡵࡵࡲࡵ࠰࡫ࡸࡲࡲࠧ࿑")), bstack1ll11_opy_ (u"ࠫࡼ࠭࿒")) as stream:
      stream.write(bstack1ll1ll1ll1_opy_.split(bstack1ll11_opy_ (u"ࠬࢁࠥࡔࡇࡖࡗࡎࡕࡎࡔࡡࡇࡅ࡙ࡇࠥࡾࠩ࿓"))[0])
      for session in sessions:
        stream.write(bstack111lll1111_opy_(session))
      stream.write(bstack1ll1ll1ll1_opy_.split(bstack1ll11_opy_ (u"࠭ࡻࠦࡕࡈࡗࡘࡏࡏࡏࡕࡢࡈࡆ࡚ࡁࠦࡿࠪ࿔"))[1])
    logger.info(bstack1ll11_opy_ (u"ࠧࡈࡧࡱࡩࡷࡧࡴࡦࡦࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡥࡹ࡮ࡲࡤࠡࡣࡵࡸ࡮࡬ࡡࡤࡶࡶࠤࡦࡺࠠࡼࡿࠪ࿕").format(bstack1l11l111l1_opy_));
  except Exception as e:
    logger.debug(bstack1ll1ll1ll_opy_.format(str(e)))
def bstack1ll1l111l_opy_(hashed_id):
  global CONFIG
  try:
    bstack11l111ll1_opy_ = datetime.datetime.now()
    host = bstack1ll11_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡴ࡮࠳ࡣ࡭ࡱࡸࡨ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨ࿖") if bstack1ll11_opy_ (u"ࠩࡤࡴࡵ࠭࿗") in CONFIG else bstack1ll11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫ࿘")
    user = CONFIG[bstack1ll11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭࿙")]
    key = CONFIG[bstack1ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ࿚")]
    bstack1ll111l1l1_opy_ = bstack1ll11_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ࿛") if bstack1ll11_opy_ (u"ࠧࡢࡲࡳࠫ࿜") in CONFIG else (bstack1ll11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬ࿝") if CONFIG.get(bstack1ll11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭࿞")) else bstack1ll11_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ࿟"))
    host = bstack1l11llll11_opy_(cli.config, [bstack1ll11_opy_ (u"ࠦࡦࡶࡩࡴࠤ࿠"), bstack1ll11_opy_ (u"ࠧࡧࡰࡱࡃࡸࡸࡴࡳࡡࡵࡧࠥ࿡"), bstack1ll11_opy_ (u"ࠨࡡࡱ࡫ࠥ࿢")], host) if bstack1ll11_opy_ (u"ࠧࡢࡲࡳࠫ࿣") in CONFIG else bstack1l11llll11_opy_(cli.config, [bstack1ll11_opy_ (u"ࠣࡣࡳ࡭ࡸࠨ࿤"), bstack1ll11_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨࠦ࿥"), bstack1ll11_opy_ (u"ࠥࡥࡵ࡯ࠢ࿦")], host)
    url = bstack1ll11_opy_ (u"ࠫࢀࢃ࠯ࡼࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂ࠵ࡳࡦࡵࡶ࡭ࡴࡴࡳ࠯࡬ࡶࡳࡳ࠭࿧").format(host, bstack1ll111l1l1_opy_, hashed_id)
    headers = {
      bstack1ll11_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫ࿨"): bstack1ll11_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ࿩"),
    }
    proxies = bstack11lllll1l_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies, auth=(user, key))
    if response.json():
      cli.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠢࡩࡶࡷࡴ࠿࡭ࡥࡵࡡࡶࡩࡸࡹࡩࡰࡰࡶࡣࡱ࡯ࡳࡵࠤ࿪"), datetime.datetime.now() - bstack11l111ll1_opy_)
      return list(map(lambda session: session[bstack1ll11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭࿫")], response.json()))
  except Exception as e:
    logger.debug(bstack1l1lll111_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack1111l11l11_opy_, stage=STAGE.bstack11111llll_opy_, bstack11lll1l111_opy_=SESSION_NAME)
def get_build_link():
  global CONFIG
  global bstack11l1ll11l1_opy_
  try:
    if bstack1ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ࿬") in CONFIG:
      bstack11l111ll1_opy_ = datetime.datetime.now()
      host = bstack1ll11_opy_ (u"ࠪࡥࡵ࡯࠭ࡤ࡮ࡲࡹࡩ࠭࿭") if bstack1ll11_opy_ (u"ࠫࡦࡶࡰࠨ࿮") in CONFIG else bstack1ll11_opy_ (u"ࠬࡧࡰࡪࠩ࿯")
      user = CONFIG[bstack1ll11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ࿰")]
      key = CONFIG[bstack1ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ࿱")]
      bstack1ll111l1l1_opy_ = bstack1ll11_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ࿲") if bstack1ll11_opy_ (u"ࠩࡤࡴࡵ࠭࿳") in CONFIG else bstack1ll11_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ࿴")
      url = bstack1ll11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࢀࢃ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠴ࡪࡴࡱࡱࠫ࿵").format(user, key, host, bstack1ll111l1l1_opy_)
      if cli.is_enabled(CONFIG):
        bstack1l1111111l_opy_, hashed_id = cli.bstack1ll111l111_opy_()
        logger.info(bstack11111lll11_opy_.format(bstack1l1111111l_opy_))
        return [hashed_id, bstack1l1111111l_opy_]
      else:
        headers = {
          bstack1ll11_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫ࿶"): bstack1ll11_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ࿷"),
        }
        if bstack1ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ࿸") in CONFIG:
          params = {bstack1ll11_opy_ (u"ࠨࡰࡤࡱࡪ࠭࿹"): CONFIG[bstack1ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ࿺")], bstack1ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࿻"): CONFIG[bstack1ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࿼")]}
        else:
          params = {bstack1ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ࿽"): CONFIG[bstack1ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ࿾")]}
        proxies = bstack11lllll1l_opy_(CONFIG, url)
        response = requests.get(url, params=params, headers=headers, proxies=proxies)
        if response.json():
          bstack11l1lll1_opy_ = response.json()[0][bstack1ll11_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡧࡻࡩ࡭ࡦࠪ࿿")]
          if bstack11l1lll1_opy_:
            bstack1l1111111l_opy_ = bstack11l1lll1_opy_[bstack1ll11_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣࡠࡷࡵࡰࠬက")].split(bstack1ll11_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤ࠯ࡥࡹ࡮ࡲࡤࠨခ"))[0] + bstack1ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡵ࠲ࠫဂ") + bstack11l1lll1_opy_[
              bstack1ll11_opy_ (u"ࠫ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧဃ")]
            logger.info(bstack11111lll11_opy_.format(bstack1l1111111l_opy_))
            bstack11l1ll11l1_opy_ = bstack11l1lll1_opy_[bstack1ll11_opy_ (u"ࠬ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨင")]
            bstack1l1ll111l1_opy_ = CONFIG[bstack1ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩစ")]
            if bstack1ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩဆ") in CONFIG:
              bstack1l1ll111l1_opy_ += bstack1ll11_opy_ (u"ࠨࠢࠪဇ") + CONFIG[bstack1ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫဈ")]
            if bstack1l1ll111l1_opy_ != bstack11l1lll1_opy_[bstack1ll11_opy_ (u"ࠪࡲࡦࡳࡥࠨဉ")]:
              logger.debug(bstack1l1ll1llll_opy_.format(bstack11l1lll1_opy_[bstack1ll11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩည")], bstack1l1ll111l1_opy_))
            cli.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࡫ࡪࡺ࡟ࡣࡷ࡬ࡰࡩࡥ࡬ࡪࡰ࡮ࠦဋ"), datetime.datetime.now() - bstack11l111ll1_opy_)
            return [bstack11l1lll1_opy_[bstack1ll11_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩဌ")], bstack1l1111111l_opy_]
    else:
      logger.warning(bstack1llll1111l_opy_)
  except Exception as e:
    logger.debug(bstack1111l11ll1_opy_.format(str(e)))
  return [None, None]
def bstack1111ll1l1_opy_(url, bstack1ll11l1l1l_opy_=False):
  global CONFIG
  global bstack111ll111_opy_
  if not bstack111ll111_opy_:
    hostname = bstack11lllll11_opy_(url)
    is_private = bstack1ll1l111ll_opy_(hostname)
    if (bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫဍ") in CONFIG and not bstack1lll1111ll_opy_(CONFIG[bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬဎ")])) and (is_private or bstack1ll11l1l1l_opy_):
      bstack111ll111_opy_ = hostname
def bstack11lllll11_opy_(url):
  return urlparse(url).hostname
def bstack1ll1l111ll_opy_(hostname):
  for bstack11llll1l1_opy_ in bstack1111ll1lll_opy_:
    regex = re.compile(bstack11llll1l1_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack111l1l1l1l_opy_(bstack1l1l1l1lll_opy_):
  return True if bstack1l1l1l1lll_opy_ in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack11lllll111_opy_, stage=STAGE.bstack11111llll_opy_, bstack11lll1l111_opy_=SESSION_NAME)
def getAccessibilityResults(driver):
  global CONFIG
  global PLATFORM_INDEX
  bstack1l11lll11_opy_ = not (bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ဏ"), None) and bstack1l1111l111_opy_(
          threading.current_thread(), bstack1ll11_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩတ"), None))
  bstack1l11111l11_opy_ = getattr(driver, bstack1ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫထ"), None) != True
  bstack111l1lll11_opy_ = bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠬ࡯ࡳࡂࡲࡳࡅ࠶࠷ࡹࡕࡧࡶࡸࠬဒ"), None) and bstack1l1111l111_opy_(
          threading.current_thread(), bstack1ll11_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨဓ"), None)
  if bstack111l1lll11_opy_:
    if not bstack1111llll_opy_():
      logger.warning(bstack1ll11_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡲࡳࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡪࡺࡲࡪࡧࡹࡩࠥࡇࡰࡱࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵ࠱ࠦန"))
      return {}
    logger.debug(bstack1ll11_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠬပ"))
    logger.debug(perform_scan(driver, driver_command=bstack1ll11_opy_ (u"ࠩࡨࡼࡪࡩࡵࡵࡧࡖࡧࡷ࡯ࡰࡵࠩဖ")))
    results = bstack1l111l11l_opy_(bstack1ll11_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡶࠦဗ"))
    if results is not None and results.get(bstack1ll11_opy_ (u"ࠦ࡮ࡹࡳࡶࡧࡶࠦဘ")) is not None:
        return results[bstack1ll11_opy_ (u"ࠧ࡯ࡳࡴࡷࡨࡷࠧမ")]
    logger.error(bstack1ll11_opy_ (u"ࠨࡎࡰࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡕࡩࡸࡻ࡬ࡵࡵࠣࡻࡪࡸࡥࠡࡨࡲࡹࡳࡪ࠮ࠣယ"))
    return []
  if not a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX) or (bstack1l11111l11_opy_ and bstack1l11lll11_opy_):
    logger.warning(bstack1ll11_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴ࠰ࠥရ"))
    return {}
  try:
    logger.debug(bstack1ll11_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠬလ"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(accessibility_scripts.get_results)
    return results
  except Exception:
    logger.error(bstack1ll11_opy_ (u"ࠤࡑࡳࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡷࡦࡴࡨࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦဝ"))
    return {}
@measure(event_name=EVENTS.bstack11l1l111ll_opy_, stage=STAGE.bstack11111llll_opy_, bstack11lll1l111_opy_=SESSION_NAME)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global PLATFORM_INDEX
  bstack1l11lll11_opy_ = not (bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧသ"), None) and bstack1l1111l111_opy_(
          threading.current_thread(), bstack1ll11_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪဟ"), None))
  bstack1l11111l11_opy_ = getattr(driver, bstack1ll11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬဠ"), None) != True
  bstack111l1lll11_opy_ = bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭အ"), None) and bstack1l1111l111_opy_(
          threading.current_thread(), bstack1ll11_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩဢ"), None)
  if bstack111l1lll11_opy_:
    if not bstack1111llll_opy_():
      logger.warning(bstack1ll11_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡳࡴࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡸࡻ࡭࡮ࡣࡵࡽ࠳ࠨဣ"))
      return {}
    logger.debug(bstack1ll11_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡳࡶ࡯ࡰࡥࡷࡿࠧဤ"))
    logger.debug(perform_scan(driver, driver_command=bstack1ll11_opy_ (u"ࠪࡩࡽ࡫ࡣࡶࡶࡨࡗࡨࡸࡩࡱࡶࠪဥ")))
    results = bstack1l111l11l_opy_(bstack1ll11_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷࡗࡺࡳ࡭ࡢࡴࡼࠦဦ"))
    if results is not None and results.get(bstack1ll11_opy_ (u"ࠧࡹࡵ࡮࡯ࡤࡶࡾࠨဧ")) is not None:
        return results[bstack1ll11_opy_ (u"ࠨࡳࡶ࡯ࡰࡥࡷࡿࠢဨ")]
    logger.error(bstack1ll11_opy_ (u"ࠢࡏࡱࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡖࡪࡹࡵ࡭ࡶࡶࠤࡘࡻ࡭࡮ࡣࡵࡽࠥࡽࡡࡴࠢࡩࡳࡺࡴࡤ࠯ࠤဩ"))
    return {}
  if not a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX) or (bstack1l11111l11_opy_ and bstack1l11lll11_opy_):
    logger.warning(bstack1ll11_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡷࡺࡳ࡭ࡢࡴࡼ࠲ࠧဪ"))
    return {}
  try:
    logger.debug(bstack1ll11_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡳࡶ࡯ࡰࡥࡷࡿࠧါ"))
    logger.debug(perform_scan(driver))
    bstack111l1ll11l_opy_ = driver.execute_async_script(accessibility_scripts.get_results_summary)
    return bstack111l1ll11l_opy_
  except Exception:
    logger.error(bstack1ll11_opy_ (u"ࠥࡒࡴࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡶ࡯ࡰࡥࡷࡿࠠࡸࡣࡶࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦာ"))
    return {}
def bstack1111llll_opy_():
  global CONFIG
  global PLATFORM_INDEX
  bstack1l11l11lll_opy_ = bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫိ"), None) and bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧီ"), None)
  if not a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX) or not bstack1l11l11lll_opy_:
        logger.warning(bstack1ll11_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡷ࡫ࡳࡶ࡮ࡷࡷ࠳ࠨု"))
        return False
  return True
def bstack1l111l11l_opy_(result_type):
    bstack1l11ll111l_opy_ = TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack11l11l1lll_opy_.current_hook_uuid()
    with ThreadPoolExecutor() as executor:
        future = executor.submit(bstack11l1l1ll1_opy_(bstack1l11ll111l_opy_, result_type))
        try:
            return future.result(timeout=bstack1l1lll1ll1_opy_)
        except TimeoutError:
            logger.error(bstack1ll11_opy_ (u"ࠢࡕ࡫ࡰࡩࡴࡻࡴࠡࡣࡩࡸࡪࡸࠠࡼࡿࡶࠤࡼ࡮ࡩ࡭ࡧࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡘࡥࡴࡷ࡯ࡸࡸࠨူ").format(bstack1l1lll1ll1_opy_))
        except Exception as ex:
            logger.debug(bstack1ll11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡳࡧࡷࡶ࡮࡫ࡶࡪࡰࡪࠤࡆࡶࡰࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࢁࡽ࠯ࠢࡈࡶࡷࡵࡲࠡ࠯ࠣࡿࢂࠨေ").format(result_type, str(ex)))
    return {}
@measure(event_name=EVENTS.bstack11ll1ll1l1_opy_, stage=STAGE.bstack11111llll_opy_, bstack11lll1l111_opy_=SESSION_NAME)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global PLATFORM_INDEX
  bstack1l11lll11_opy_ = not (bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ဲ"), None) and bstack1l1111l111_opy_(
          threading.current_thread(), bstack1ll11_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩဳ"), None))
  bstack1lll1lll1l_opy_ = not (bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫဴ"), None) and bstack1l1111l111_opy_(
          threading.current_thread(), bstack1ll11_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧဵ"), None))
  bstack1l11111l11_opy_ = getattr(driver, bstack1ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭ံ"), None) != True
  if not a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX) or (bstack1l11111l11_opy_ and bstack1l11lll11_opy_ and bstack1lll1lll1l_opy_):
    logger.warning(bstack1ll11_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡶࡰࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮࠯ࠤ့"))
    return {}
  try:
    bstack1lll1111l1_opy_ = bstack1ll11_opy_ (u"ࠨࡣࡳࡴࠬး") in CONFIG and CONFIG.get(bstack1ll11_opy_ (u"ࠩࡤࡴࡵ္࠭"), bstack1ll11_opy_ (u"်ࠪࠫ"))
    session_id = getattr(driver, bstack1ll11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨျ"), None)
    if not session_id:
      logger.warning(bstack1ll11_opy_ (u"ࠧࡔ࡯ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡌࡈࠥ࡬࡯ࡶࡰࡧࠤ࡫ࡵࡲࠡࡦࡵ࡭ࡻ࡫ࡲࠣြ"))
      return {bstack1ll11_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧွ"): bstack1ll11_opy_ (u"ࠢࡏࡱࠣࡷࡪࡹࡳࡪࡱࡱࠤࡎࡊࠠࡧࡱࡸࡲࡩࠨှ")}
    if bstack1lll1111l1_opy_:
      try:
        bstack111l1l1ll1_opy_ = {
              bstack1ll11_opy_ (u"ࠨࡶ࡫ࡎࡼࡺࡔࡰ࡭ࡨࡲࠬဿ"): os.environ.get(bstack1ll11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ၀"), os.environ.get(bstack1ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ၁"), bstack1ll11_opy_ (u"ࠫࠬ၂"))),
              bstack1ll11_opy_ (u"ࠬࡺࡨࡕࡧࡶࡸࡗࡻ࡮ࡖࡷ࡬ࡨࠬ၃"): TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack11l11l1lll_opy_.current_hook_uuid(),
              bstack1ll11_opy_ (u"࠭ࡡࡶࡶ࡫ࡌࡪࡧࡤࡦࡴࠪ၄"): os.environ.get(bstack1ll11_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ၅")),
              bstack1ll11_opy_ (u"ࠨࡵࡦࡥࡳ࡚ࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ၆"): str(int(datetime.datetime.now().timestamp() * 1000)),
              bstack1ll11_opy_ (u"ࠩࡷ࡬ࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧ၇"): os.environ.get(bstack1ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ၈"), bstack1ll11_opy_ (u"ࠫࠬ၉")),
              bstack1ll11_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬ၊"): kwargs.get(bstack1ll11_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡣࡰ࡯ࡰࡥࡳࡪࠧ။"), None) or bstack1ll11_opy_ (u"ࠧࠨ၌")
          }
        if not hasattr(thread_local, bstack1ll11_opy_ (u"ࠨࡤࡤࡷࡪࡥࡡࡱࡲࡢࡥ࠶࠷ࡹࡠࡵࡦࡶ࡮ࡶࡴࠨ၍")):
            scripts = {bstack1ll11_opy_ (u"ࠩࡶࡧࡦࡴࠧ၎"): accessibility_scripts.perform_scan}
            thread_local.base_app_a11y_script = scripts
        bstack11l11l11l_opy_ = copy.deepcopy(thread_local.base_app_a11y_script)
        bstack11l11l11l_opy_[bstack1ll11_opy_ (u"ࠪࡷࡨࡧ࡮ࠨ၏")] = bstack11l11l11l_opy_[bstack1ll11_opy_ (u"ࠫࡸࡩࡡ࡯ࠩၐ")] % json.dumps(bstack111l1l1ll1_opy_)
        accessibility_scripts.bstack11111l111_opy_(bstack11l11l11l_opy_)
        accessibility_scripts.store()
        bstack1111lll1ll_opy_ = driver.execute_script(accessibility_scripts.perform_scan)
      except Exception as bstack11111l11l1_opy_:
        logger.info(bstack1ll11_opy_ (u"ࠧࡇࡰࡱ࡫ࡸࡱࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡣࡢࡰࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࠧၑ") + str(bstack11111l11l1_opy_))
        bstack1111lll1ll_opy_ = {bstack1ll11_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧၒ"): str(bstack11111l11l1_opy_)}
    else:
      bstack1111lll1ll_opy_ = driver.execute_async_script(accessibility_scripts.perform_scan, {bstack1ll11_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪࠧၓ"): kwargs.get(bstack1ll11_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࡠࡥࡲࡱࡲࡧ࡮ࡥࠩၔ"), None) or bstack1ll11_opy_ (u"ࠩࠪၕ")})
    return bstack1111lll1ll_opy_
  except Exception as err:
    logger.error(bstack1ll11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡲࡶࡰࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮࠯ࠢࡾࢁࠧၖ").format(str(err)))
    return {}