# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
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
from browserstack_sdk.sdk_cli.bstack1l1111ll1_opy_ import bstack1llll1111l_opy_
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from browserstack_sdk.bstack11ll11111l_opy_ import bstack11ll1l1l1l_opy_
from browserstack_sdk.bstack1l1l1lll11_opy_ import *
import time
import requests
from bstack_utils.constants import EVENTS, STAGE, bstack11l1111l_opy_
from bstack_utils.messages import bstack1l11lll11l_opy_, bstack11l11111l_opy_, bstack1l1l111ll1_opy_, bstack111ll1ll_opy_, bstack1ll1ll11ll_opy_, bstack1l1ll11lll_opy_
from bstack_utils.measure import measure
from bstack_utils.logger_utils import get_logger
from bstack_utils.helper import bstack11l11ll11_opy_
from browserstack_sdk.bstack11l11lllll_opy_ import bstack1ll1111l11_opy_
logger = get_logger(__name__)
def bstack1l11l1l1ll_opy_():
  global CONFIG
  headers = {
        bstack1ll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack1ll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack11l11ll11_opy_(CONFIG, bstack11l1111l_opy_)
  try:
    response = requests.get(bstack11l1111l_opy_, headers=headers, proxies=proxies, timeout=2)
    if response.json():
      bstack111lllll_opy_ = response.json()[bstack1ll_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1l11lll11l_opy_.format(response.json()))
      return bstack111lllll_opy_
    else:
      logger.debug(bstack11l11111l_opy_.format(bstack1ll_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack11l11111l_opy_.format(e))
def bstack1111llll11_opy_(hub_url):
  global CONFIG
  url = bstack1ll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack1ll_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack1ll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack1ll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack11l11ll11_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=(0.5, 1.0))
    latency = time.perf_counter() - start_time
    logger.debug(bstack1l1l111ll1_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack111ll1ll_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack1l11lll111_opy_, stage=STAGE.bstack11llll111l_opy_)
def bstack11l11l1111_opy_():
  try:
    global bstack1ll1111l1_opy_
    global CONFIG
    if bstack1ll_opy_ (u"ࠫ࡭ࡻࡢࡓࡧࡪ࡭ࡴࡴࠧࡾ") in CONFIG and CONFIG[bstack1ll_opy_ (u"ࠬ࡮ࡵࡣࡔࡨ࡫࡮ࡵ࡮ࠨࡿ")]:
      from bstack_utils.constants import bstack1l111lll1l_opy_
      bstack111lllllll_opy_ = CONFIG[bstack1ll_opy_ (u"࠭ࡨࡶࡤࡕࡩ࡬࡯࡯࡯ࠩࢀ")]
      if bstack111lllllll_opy_ in bstack1l111lll1l_opy_:
        bstack1ll1111l1_opy_ = bstack1l111lll1l_opy_[bstack111lllllll_opy_]
        logger.debug(bstack1ll1ll11ll_opy_.format(bstack1ll1111l1_opy_))
        return
      else:
        logger.debug(bstack1ll_opy_ (u"ࠢࡉࡷࡥࠤࡰ࡫ࡹࠡࠩࡾࢁࠬࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࡎࡕࡃࡡࡘࡖࡑࡥࡍࡂࡒ࠯ࠤ࡫ࡧ࡬࡭࡫ࡱ࡫ࠥࡨࡡࡤ࡭ࠣࡸࡴࠦ࡯ࡱࡶ࡬ࡱࡦࡲࠠࡩࡷࡥࠤࡩ࡫ࡴࡦࡥࡷ࡭ࡴࡴࠢࢁ").format(bstack111lllllll_opy_))
    bstack111lllll_opy_ = bstack1l11l1l1ll_opy_()
    from concurrent.futures import ThreadPoolExecutor, as_completed
    if bstack111lllll_opy_:
        with ThreadPoolExecutor(max_workers=len(bstack111lllll_opy_)) as executor:
            bstack1ll1l1111_opy_ = {executor.submit(bstack1111llll11_opy_, bstack1lll1l1l_opy_): bstack1lll1l1l_opy_ for bstack1lll1l1l_opy_ in bstack111lllll_opy_}
            for future in as_completed(bstack1ll1l1111_opy_):
                result = future.result()
                if result and result.get(bstack1ll_opy_ (u"ࠨ࡮ࡤࡸࡪࡴࡣࡺࠩࢂ")) is not None:
                    bstack1ll1111l1_opy_ = result[bstack1ll_opy_ (u"ࠩ࡫ࡹࡧࡥࡵࡳ࡮ࠪࢃ")]
                    logger.debug(bstack1ll1ll11ll_opy_.format(bstack1ll1111l1_opy_))
                    return
        bstack1ll1111l1_opy_ = bstack111lllll_opy_[0]
        logger.debug(bstack1ll1ll11ll_opy_.format(bstack1ll1111l1_opy_))
        return
  except Exception as e:
    logger.debug(bstack1l1ll11lll_opy_.format(e))
from browserstack_sdk.bstack1lll11l1_opy_ import *
from browserstack_sdk.bstack111l11lll_opy_ import bstack1lll1lll1l_opy_
from browserstack_sdk.bstack11l11lllll_opy_ import *
from browserstack_sdk.bstack1ll1ll111l_opy_ import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.logger_utils import get_logger
from bstack_utils.measure import measure
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack1111l11l1_opy_, stage=STAGE.bstack11llll111l_opy_)
def bstack1l1l111l11_opy_():
    global bstack1ll1111l1_opy_
    try:
        bstack1l1l1ll1l1_opy_ = bstack1111ll11_opy_()
        bstack1l11l11111_opy_(bstack1l1l1ll1l1_opy_)
        hub_url = bstack1l1l1ll1l1_opy_.get(bstack1ll_opy_ (u"ࠥࡹࡷࡲࠢࢄ"), bstack1ll_opy_ (u"ࠦࠧࢅ"))
        if hub_url.endswith(bstack1ll_opy_ (u"ࠬ࠵ࡷࡥ࠱࡫ࡹࡧ࠭ࢆ")):
            hub_url = hub_url.rsplit(bstack1ll_opy_ (u"࠭࠯ࡸࡦ࠲࡬ࡺࡨࠧࢇ"), 1)[0]
        if hub_url.startswith(bstack1ll_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࠨ࢈")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack1ll_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࠪࢉ")):
            hub_url = hub_url[8:]
        bstack1ll1111l1_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack1111ll11_opy_():
    global CONFIG
    bstack11111ll1_opy_ = CONFIG.get(bstack1ll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢊ"), {}).get(bstack1ll_opy_ (u"ࠪ࡫ࡷ࡯ࡤࡏࡣࡰࡩࠬࢋ"), bstack1ll_opy_ (u"ࠫࡓࡕ࡟ࡈࡔࡌࡈࡤࡔࡁࡎࡇࡢࡔࡆ࡙ࡓࡆࡆࠪࢌ"))
    if not isinstance(bstack11111ll1_opy_, str):
        raise ValueError(bstack1ll_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡌࡸࡩࡥࠢࡱࡥࡲ࡫ࠠ࡮ࡷࡶࡸࠥࡨࡥࠡࡣࠣࡺࡦࡲࡩࡥࠢࡶࡸࡷ࡯࡮ࡨࠤࢍ"))
    try:
        bstack1l1l1ll1l1_opy_ = bstack1lll1l1l1l_opy_(bstack11111ll1_opy_)
        return bstack1l1l1ll1l1_opy_
    except Exception as e:
        logger.error(bstack1ll_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡩࡵ࡭ࡩࠦࡤࡦࡶࡤ࡭ࡱࡹࠠ࠻ࠢࡾࢁࠧࢎ").format(str(e)))
        return {}
def bstack1lll1l1l1l_opy_(bstack11111ll1_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack1ll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ࢏")] or not CONFIG[bstack1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ࢐")]:
            raise ValueError(bstack1ll_opy_ (u"ࠤࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠤࡴࡸࠠࡢࡥࡦࡩࡸࡹࠠ࡬ࡧࡼࠦ࢑"))
        url = bstack111111l1ll_opy_ + bstack11111ll1_opy_
        auth = (CONFIG[bstack1ll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ࢒")], CONFIG[bstack1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ࢓")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack11l1l11l_opy_ = json.loads(response.text)
            return bstack11l1l11l_opy_
    except ValueError as ve:
        logger.error(bstack1ll_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡩࡵ࡭ࡩࠦࡤࡦࡶࡤ࡭ࡱࡹࠠ࠻ࠢࡾࢁࠧ࢔").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack1ll_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡪࡶ࡮ࡪࠠࡥࡧࡷࡥ࡮ࡲࡳࠡ࠼ࠣࡿࢂࠨ࢕").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack1l11l11111_opy_(bstack1ll1l1l1ll_opy_):
    global CONFIG
    if bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ࢖") not in CONFIG or str(CONFIG[bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬࢗ")]).lower() == bstack1ll_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ࢘"):
        CONFIG[bstack1ll_opy_ (u"ࠪࡰࡴࡩࡡ࡭࢙ࠩ")] = False
    elif bstack1ll_opy_ (u"ࠫ࡮ࡹࡔࡳ࡫ࡤࡰࡌࡸࡩࡥ࢚ࠩ") in bstack1ll1l1l1ll_opy_:
        bstack1111ll11l1_opy_ = CONFIG.get(bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴ࢛ࠩ"), {})
        logger.debug(bstack1ll_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡸࡪࡵࡷ࡭ࡳ࡭ࠠ࡭ࡱࡦࡥࡱࠦ࡯ࡱࡶ࡬ࡳࡳࡹ࠺ࠡࠧࡶࠦ࢜"), bstack1111ll11l1_opy_)
        bstack1ll11111_opy_ = bstack1ll1l1l1ll_opy_.get(bstack1ll_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡒࡦࡲࡨࡥࡹ࡫ࡲࡴࠤ࢝"), [])
        bstack1l11l1ll1_opy_ = bstack1ll_opy_ (u"ࠣ࠮ࠥ࢞").join(bstack1ll11111_opy_)
        logger.debug(bstack1ll_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡅࡸࡷࡹࡵ࡭ࠡࡴࡨࡴࡪࡧࡴࡦࡴࠣࡷࡹࡸࡩ࡯ࡩ࠽ࠤࠪࡹࠢ࢟"), bstack1l11l1ll1_opy_)
        bstack1l1l111lll_opy_ = {
            bstack1ll_opy_ (u"ࠥࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧࢠ"): bstack1ll_opy_ (u"ࠦࡦࡺࡳ࠮ࡴࡨࡴࡪࡧࡴࡦࡴࠥࢡ"),
            bstack1ll_opy_ (u"ࠧ࡬࡯ࡳࡥࡨࡐࡴࡩࡡ࡭ࠤࢢ"): bstack1ll_opy_ (u"ࠨࡴࡳࡷࡨࠦࢣ"),
            bstack1ll_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࠭ࡳࡧࡳࡩࡦࡺࡥࡳࠤࢤ"): bstack1l11l1ll1_opy_
        }
        bstack1111ll11l1_opy_.update(bstack1l1l111lll_opy_)
        logger.debug(bstack1ll_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡖࡲࡧࡥࡹ࡫ࡤࠡ࡮ࡲࡧࡦࡲࠠࡰࡲࡷ࡭ࡴࡴࡳ࠻ࠢࠨࡷࠧࢥ"), bstack1111ll11l1_opy_)
        CONFIG[bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢦ")] = bstack1111ll11l1_opy_
        logger.debug(bstack1ll_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡉ࡭ࡳࡧ࡬ࠡࡅࡒࡒࡋࡏࡇ࠻ࠢࠨࡷࠧࢧ"), CONFIG)
def get_turboscale_playwright_url():
    bstack1l1l1ll1l1_opy_ = bstack1111ll11_opy_()
    if not bstack1l1l1ll1l1_opy_[bstack1ll_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡖࡴ࡯ࠫࢨ")]:
      raise ValueError(bstack1ll_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡗࡵࡰࠥ࡯ࡳࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡩࡶࡴࡳࠠࡨࡴ࡬ࡨࠥࡪࡥࡵࡣ࡬ࡰࡸ࠴ࠢࢩ"))
    return bstack1l1l1ll1l1_opy_[bstack1ll_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡘࡶࡱ࠭ࢪ")] + bstack1ll_opy_ (u"ࠧࡀࡥࡤࡴࡸࡃࠧࢫ")
@measure(event_name=EVENTS.bstack11l1l11111_opy_, stage=STAGE.bstack11llll111l_opy_)
def bstack1l1lll1ll1_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack1ll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪࢬ")], CONFIG[bstack1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬࢭ")])
        url = bstack1l11llll_opy_
        logger.debug(bstack1ll_opy_ (u"ࠥࡅࡹࡺࡥ࡮ࡲࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴࠢࡩࡶࡴࡳࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡔࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠣࡅࡕࡏࠢࢮ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack1ll_opy_ (u"ࠦࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠥࢯ"): bstack1ll_opy_ (u"ࠧࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠣࢰ")})
            if response.status_code == 200:
                bstack11lll1l1ll_opy_ = json.loads(response.text)
                bstack111l11ll1_opy_ = bstack11lll1l1ll_opy_.get(bstack1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡸ࠭ࢱ"), [])
                if bstack111l11ll1_opy_:
                    bstack1l111l1l_opy_ = bstack111l11ll1_opy_[0]
                    build_hashed_id = bstack1l111l1l_opy_.get(bstack1ll_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪࢲ"))
                    bstack1l11l111l1_opy_ = bstack111lll111_opy_ + build_hashed_id
                    result.extend([build_hashed_id, bstack1l11l111l1_opy_])
                    logger.info(bstack11l111111_opy_.format(bstack1l11l111l1_opy_))
                    bstack11l1lll1l1_opy_ = CONFIG[bstack1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫࢳ")]
                    if bstack1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࢴ") in CONFIG:
                      bstack11l1lll1l1_opy_ += bstack1ll_opy_ (u"ࠪࠤࠬࢵ") + CONFIG[bstack1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࢶ")]
                    if bstack11l1lll1l1_opy_ != bstack1l111l1l_opy_.get(bstack1ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪࢷ")):
                      logger.debug(bstack11llll1l1_opy_.format(bstack1l111l1l_opy_.get(bstack1ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫࢸ")), bstack11l1lll1l1_opy_))
                    return result
                else:
                    logger.debug(bstack1ll_opy_ (u"ࠢࡂࡖࡖࠤ࠿ࠦࡎࡰࠢࡥࡹ࡮ࡲࡤࡴࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠱ࠦࢹ"))
            else:
                logger.debug(bstack1ll_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴ࠰ࠥࢺ"))
        except Exception as e:
            logger.error(bstack1ll_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࡶࠤ࠿ࠦࡻࡾࠤࢻ").format(str(e)))
    else:
        logger.debug(bstack1ll_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡆࡓࡓࡌࡉࡈࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡶࡩࡹ࠴ࠠࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴ࠰ࠥࢼ"))
    return [None, None]
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack111l1lll11_opy_ import bstack111l1lll11_opy_, Events, bstack1l11l111_opy_, bstack11111l11_opy_
from bstack_utils.measure import bstack1l11ll1lll_opy_
from bstack_utils.measure import measure
from bstack_utils.percy import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack11ll111lll_opy_ import bstack1111lllll1_opy_
from bstack_utils.messages import *
from bstack_utils import logger_utils
from bstack_utils.constants import *
from bstack_utils.helper import bstack111ll1111_opy_, bstack1l1111l111_opy_, bstack11lll111ll_opy_, bstack1llll1lll_opy_, \
  bstack1lll1111ll_opy_, \
  Notset, is_robot_playwright_installed, bstack111lll1ll_opy_, \
  bstack1lll111l1l_opy_, bstack1l1l11l1ll_opy_, bstack111l11111l_opy_, bstack1lll11l1ll_opy_, bstack11lll11ll_opy_, bstack1ll1l1ll1l_opy_, \
  bstack1l1111l1l1_opy_, \
  bstack1ll11l11_opy_, bstack1lll1l1lll_opy_, bstack111l1l1ll1_opy_, bstack11l11llll1_opy_, \
  bstack1ll11l1l1l_opy_, bstack11111ll1ll_opy_, bstack11l1l1l11l_opy_, bstack111111l111_opy_, bstack1ll11l1111_opy_
from bstack_utils.bstack1l1lll1l_opy_ import bstack1l11llll1_opy_
from bstack_utils.bstack111l1111l1_opy_ import bstack1ll1lll11l_opy_, bstack11l1l1llll_opy_
from bstack_utils.bstack1111ll1l1l_opy_ import bstack11111lll_opy_
from bstack_utils.bstack111l1l1l1l_opy_ import bstack1l111l1l1l_opy_, bstack11lllll11l_opy_
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.bstack1lll1l11l1_opy_ import bstack11lll1l111_opy_
from bstack_utils.proxy import bstack1llll11111_opy_, bstack11l11ll11_opy_, bstack11lllll1_opy_, bstack1l1ll11l11_opy_
from bstack_utils.bstack111111111_opy_ import bstack11ll1lll_opy_, bstack1111l11ll1_opy_
import bstack_utils.bstack1l11llll11_opy_ as TestHubUtils
import bstack_utils.bstack1ll1lll111_opy_ as bstack1l11lll1l_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.utils.bstack111ll11l1_opy_ import bstack1l11l1lll1_opy_
from bstack_utils.bstack1ll1ll1ll_opy_ import bstack1l111111ll_opy_
from bstack_utils.bstack11lll1l1l_opy_ import bstack1ll1ll1l1_opy_
from bstack_utils.bstack1l11ll1lll_opy_ import bstack1l11l1ll11_opy_
if os.getenv(bstack1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡉࡑࡒࡏࡘ࠭ࢽ")):
  cli.bstack1llllll1l1l_opy_()
else:
  os.environ[bstack1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡊࡒࡓࡐ࡙ࠧࢾ")] = bstack1ll_opy_ (u"࠭ࡴࡳࡷࡨࠫࢿ")
bstack111l1l111_opy_ = bstack1ll_opy_ (u"ࠧࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠠࠡ࡫ࡩࠬࡵࡧࡧࡦࠢࡀࡁࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠠࡼ࡞ࡱࠤࠥࠦࡴࡳࡻࡾࡠࡳࠦࡣࡰࡰࡶࡸࠥ࡬ࡳࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࡡ࠭ࡦࡴ࡞ࠪ࠭ࡀࡢ࡮ࠡࠢࠣࠤࠥ࡬ࡳ࠯ࡣࡳࡴࡪࡴࡤࡇ࡫࡯ࡩࡘࡿ࡮ࡤࠪࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠬࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡳࡣ࡮ࡴࡤࡦࡺࠬࠤ࠰ࠦࠢ࠻ࠤࠣ࠯ࠥࡐࡓࡐࡐ࠱ࡷࡹࡸࡩ࡯ࡩ࡬ࡪࡾ࠮ࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࠬࡦࡽࡡࡪࡶࠣࡲࡪࡽࡐࡢࡩࡨ࠶࠳࡫ࡶࡢ࡮ࡸࡥࡹ࡫ࠨࠣࠪࠬࠤࡂࡄࠠࡼࡿࠥ࠰ࠥࡢࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡨࡧࡷࡗࡪࡹࡳࡪࡱࡱࡈࡪࡺࡡࡪ࡮ࡶࠦࢂࡢࠧࠪࠫࠬ࡟ࠧ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠣ࡟ࠬࠤ࠰ࠦࠢ࠭࡞࡟ࡲࠧ࠯࡜࡯ࠢࠣࠤࠥࢃࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡽ࡝ࡰࠣࠤ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠧࣀ")
LAUNCH_PATCH_ROBOT_PLAYWRIGHT = bstack1ll_opy_ (u"ࠨ࡞ࡱ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࡢ࡮ࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠻࡝ࠡ࠿ࡀࡁࠥࡢࠧࡵࡴࡸࡩࡡ࠭࡜࡯ࡥࡲࡲࡸࡺࠠࡣࡵࡷࡥࡨࡱ࡟ࡱࡣࡷ࡬ࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴࡟࡟ࡲࡨࡵ࡮ࡴࡶࠣࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࡝ࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠵ࡢࡢ࡮ࡤࡱࡱࡷࡹࠦࡰࡠ࡫ࡱࡨࡪࡾࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠵ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠵࡟ࠣࡁࡂࡃࠠ࡝ࠩࡷࡶࡺ࡫࡜ࠨ࡞ࡱࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡷࡱ࡯ࡣࡦࠪ࠳࠰ࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠵ࠪ࡞ࡱࡧࡴࡴࡳࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣࠫ࠾ࡠࡳࡩ࡯࡯ࡵࡷࠤࡴࡸࡩࡨ࡫ࡱࡥࡱࡥࡣࡩࡴࡲࡱ࡮ࡻ࡭ࡠ࡮ࡤࡹࡳࡩࡨࠡ࠿ࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡰࡦࡻ࡮ࡤࡪ࠱ࡦ࡮ࡴࡤࠩ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭ࠪ࠽࡟ࡲ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡱࡧࡵ࡯ࡥ࡫ࠤࡂࠦࡡࡴࡻࡱࡧࠥ࠮࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸ࠯ࠠ࠾ࡀࠣࡿࡡࡴࡩࡧࠢࠫࠥࡧࡹࡴࡢࡥ࡮ࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠪࠢࡾࡠࡳࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦ࡯ࡳ࡫ࡪ࡭ࡳࡧ࡬ࡠࡥ࡫ࡶࡴࡳࡩࡶ࡯ࡢࡰࡦࡻ࡮ࡤࡪࠫࡰࡦࡻ࡮ࡤࡪࡒࡴࡹ࡯࡯࡯ࡵࠬ࠿ࡡࡴࡽ࡝ࡰ࡯ࡩࡹࠦࡣࡢࡲࡶ࠿ࡡࡴࡴࡳࡻࠣࡿࡡࡴࡣࡢࡲࡶࠤࡂࠦࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠪ࡞ࡱࠤࠥࢃࠠࡤࡣࡷࡧ࡭࠮ࡥࡹࠫࠣࡿࡡࡴࠠࠡࠢࠣࢁࡡࡴࠠࠡ࡫ࡩࠤ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࠮ࠦࡻ࡝ࡰࠣࠤࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡩ࡯࡯ࡰࡨࡧࡹࡕࡶࡦࡴࡆࡈࡕ࠮ࡻ࡝ࡰࠣࠤࠥࠦࠠࠡࡧࡱࡨࡵࡵࡩ࡯ࡶࡘࡖࡑࡀࠠࡡࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠧࡿࡪࡴࡣࡰࡦࡨ࡙ࡗࡏࡃࡰ࡯ࡳࡳࡳ࡫࡮ࡵࠪࡍࡗࡔࡔ࠮ࡴࡶࡵ࡭ࡳ࡭ࡩࡧࡻࠫࡧࡦࡶࡳࠪࠫࢀࡤ࠱ࡢ࡮ࠡࠢࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴ࡞ࡱࠤࠥࠦࠠࡾࠫ࡟ࡲࠥࠦࡽ࡝ࡰࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࠻ࠢࡣࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠩࢁࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭ࢂࡦࠬ࡝ࡰࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴ࡞ࡱࠤࠥࢃࠩ࡝ࡰࢀࡠࡳࡩ࡯࡯ࡵࡷࠤࡴࡸࡩࡨ࡫ࡱࡥࡱࡥࡣࡰࡰࡱࡩࡨࡺࠠ࠾ࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱ࠮ࡤࡪࡵࡳࡲ࡯ࡵ࡮࠰ࡦࡳࡳࡴࡥࡤࡶ࠱ࡦ࡮ࡴࡤࠩ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭ࠪ࠽࡟ࡲ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡨࡵ࡮࡯ࡧࡦࡸࠥࡃࠠࡢࡵࡼࡲࡨࠦࠨࡤࡱࡱࡲࡪࡩࡴࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁ࡜࡯ࠢࠣ࡭࡫ࠦࠨࠢࡤࡶࡸࡦࡩ࡫ࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠮ࠦࡻ࡝ࡰࠣࠤࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥࡵࡲࡪࡩ࡬ࡲࡦࡲ࡟ࡤࡱࡱࡲࡪࡩࡴࠩࡥࡲࡲࡳ࡫ࡣࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠫ࠾ࡠࡳࠦࠠࡾ࡞ࡱࠤࠥࡲࡥࡵࠢࡦࡥࡵࡹ࠻࡝ࡰࠣࠤࡹࡸࡹࠡࡽ࡟ࡲࠥࠦࠠࠡࡥࡤࡴࡸࠦ࠽ࠡࡌࡖࡓࡓ࠴ࡰࡢࡴࡶࡩ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡩࡡࡱࡵࠬࡠࡳࠦࠠࡾࠢࡦࡥࡹࡩࡨࠩࡧࡻ࠭ࠥࢁ࡜࡯ࠢࠣࢁࡡࡴࠠࠡࡥࡲࡲࡸࡺࠠ࡮ࡱࡧ࡭࡫࡯ࡥࡥࡇࡱࡨࡵࡵࡩ࡯ࡶࠣࡁࠥࡦࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࡡࠢ࠮ࠤࡪࡴࡣࡰࡦࡨ࡙ࡗࡏࡃࡰ࡯ࡳࡳࡳ࡫࡮ࡵࠪࡍࡗࡔࡔ࠮ࡴࡶࡵ࡭ࡳ࡭ࡩࡧࡻࠫࡧࡦࡶࡳࠪࠫ࠾ࡠࡳࠦࠠࡪࡨࠣࠬࡧࡹࡴࡢࡥ࡮ࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ࠭ࠥࢁ࡜࡯ࠢࠣࠤࠥࡸࡥࡵࡷࡵࡲࠥࡧࡷࡢ࡫ࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡨࡵ࡮࡯ࡧࡦࡸࡔࡼࡥࡳࡅࡇࡔ࠭ࢁ࡜࡯ࠢࠣࠤࠥࠦࠠࡦࡰࡧࡴࡴ࡯࡮ࡵࡗࡕࡐ࠿ࠦ࡭ࡰࡦ࡬ࡪ࡮࡫ࡤࡆࡰࡧࡴࡴ࡯࡮ࡵ࠮࡟ࡲࠥࠦࠠࠡࠢࠣ࠲࠳࠴ࡣࡰࡰࡱࡩࡨࡺࡏࡱࡶ࡬ࡳࡳࡹ࡜࡯ࠢࠣࠤࠥࢃࠩ࡝ࡰࠣࠤࢂࡢ࡮ࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤ࠳࠴࠮ࡤࡱࡱࡲࡪࡩࡴࡐࡲࡷ࡭ࡴࡴࡳ࠭࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࡝ࡰࠣࠤࢂ࠯࡜࡯ࡿ࡟ࡲࡱ࡫ࡴࠡࡄࡵࡳࡼࡹࡥࡳࡅࡲࡲࡹ࡫ࡸࡵ࠽࡟ࡲࡹࡸࡹࠡࡽ࡟ࡲࠥࠦࡣࡰࡰࡶࡸࠥࡶࡡࡵࡪࡐࡳࡩࡻ࡬ࡦࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭ࠨࡰࡢࡶ࡫ࠦ࠮ࡁ࡜࡯ࠢࠣࡧࡴࡴࡳࡵࠢࡳࡻࡈࡵࡲࡦࡒࡤࡸ࡭ࠦ࠽ࠡࡲࡤࡸ࡭ࡓ࡯ࡥࡷ࡯ࡩ࠳ࡪࡩࡳࡰࡤࡱࡪ࠮ࡲࡦࡳࡸ࡭ࡷ࡫࠮ࡳࡧࡶࡳࡱࡼࡥࠩࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠳ࡣࡰࡴࡨ࠳ࡵࡧࡣ࡬ࡣࡪࡩ࠳ࡰࡳࡰࡰࠥ࠭࠮ࡁ࡜࡯ࠢࠣࡆࡷࡵࡷࡴࡧࡵࡇࡴࡴࡴࡦࡺࡷࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨࡱࡣࡷ࡬ࡒࡵࡤࡶ࡮ࡨ࠲࡯ࡵࡩ࡯ࠪࡳࡻࡈࡵࡲࡦࡒࡤࡸ࡭࠲ࠠࠣ࡮࡬ࡦ࠴ࡩ࡬ࡪࡧࡱࡸ࠴ࡨࡲࡰࡹࡶࡩࡷࡉ࡯࡯ࡶࡨࡼࡹࠨࠩࠪ࠰ࡅࡶࡴࡽࡳࡦࡴࡆࡳࡳࡺࡥࡹࡶ࠾ࡠࡳࢃࠠࡤࡣࡷࡧ࡭ࠦࠨࡦࠫࠣࡿࡡࡴࠠࠡࡥࡲࡲࡸࡵ࡬ࡦ࠰ࡺࡥࡷࡴࠨࠣࡅࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡱࡵࡡࡥࠢࡅࡶࡴࡽࡳࡦࡴࡆࡳࡳࡺࡥࡹࡶࠣࡪࡷࡵ࡭ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠲ࡩ࡯ࡳࡧ࠽ࠦ࠱ࠦࡥ࠯࡯ࡨࡷࡸࡧࡧࡦࠫ࠾ࡠࡳࢃ࡜࡯ࡥࡲࡲࡸࡺࠠࡰࡴ࡬࡫࡮ࡴࡡ࡭ࡡࡱࡩࡼࡖࡡࡨࡧࠣࡁࠥࡈࡲࡰࡹࡶࡩࡷࡉ࡯࡯ࡶࡨࡼࡹ࠴ࡰࡳࡱࡷࡳࡹࡿࡰࡦ࠰ࡱࡩࡼࡖࡡࡨࡧ࠾ࡠࡳࡈࡲࡰࡹࡶࡩࡷࡉ࡯࡯ࡶࡨࡼࡹ࠴ࡰࡳࡱࡷࡳࡹࡿࡰࡦ࠰ࡱࡩࡼࡖࡡࡨࡧࠣࡁࠥࡧࡳࡺࡰࡦࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠮ࠩࠡࡽ࡟ࡲࠥࠦࡩࡧࠢࠫࡦࡸࡺࡡࡤ࡭ࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠬࠤࢀࡢ࡮ࠡࠢࠣࠤࡹࡸࡹࠡࡽ࡟ࡲࠥࠦࠠࠡࠢࠣࡧࡴࡴࡳࡵࠢࡥࡶࡴࡽࡳࡦࡴࠣࡁࠥࡺࡨࡪࡵ࠱ࡦࡷࡵࡷࡴࡧࡵࠤࠫࠬࠠࡵࡪ࡬ࡷ࠳ࡨࡲࡰࡹࡶࡩࡷ࠮ࠩ࠼࡞ࡱࠤࠥࠦࠠࠡࠢ࡯ࡩࡹࠦࡰࡳ࡫ࡰࡥࡷࡿࡃࡰࡰࡷࡩࡽࡺࠠ࠾ࠢࡥࡶࡴࡽࡳࡦࡴࠣࠪࠫࠦࡴࡺࡲࡨࡳ࡫ࠦࡢࡳࡱࡺࡷࡪࡸ࠮ࡤࡱࡱࡸࡪࡾࡴࡴࠢࡀࡁࡂࠦ࡜ࠨࡨࡸࡲࡨࡺࡩࡰࡰ࡟ࠫࠥࡅࠠࡣࡴࡲࡻࡸ࡫ࡲ࠯ࡥࡲࡲࡹ࡫ࡸࡵࡵࠫ࠭ࡠ࠶࡝ࠡ࠼ࠣࡲࡺࡲ࡬࠼࡞ࡱࠤࠥࠦࠠࠡࠢ࡬ࡪࠥ࠮ࠡࡱࡴ࡬ࡱࡦࡸࡹࡄࡱࡱࡸࡪࡾࡴࠡࠨࠩࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࠬࠦࠡࡶࡼࡴࡪࡵࡦࠡࡤࡵࡳࡼࡹࡥࡳ࠰ࡱࡩࡼࡉ࡯࡯ࡶࡨࡼࡹࠦ࠽࠾࠿ࠣࡠࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡜ࠨࠫࠣࡿࡡࡴࠠࠡࠢࠣࠤࠥࠦࠠࡱࡴ࡬ࡱࡦࡸࡹࡄࡱࡱࡸࡪࡾࡴࠡ࠿ࠣࡥࡼࡧࡩࡵࠢࡥࡶࡴࡽࡳࡦࡴ࠱ࡲࡪࡽࡃࡰࡰࡷࡩࡽࡺࠨࠪ࠽࡟ࡲࠥࠦࠠࠡࠢࠣࢁࡡࡴࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡵࡷࠤࡹࡧࡲࡨࡧࡷࡇࡴࡴࡴࡦࡺࡷࠤࡂࠦࡰࡳ࡫ࡰࡥࡷࡿࡃࡰࡰࡷࡩࡽࡺࠠࡽࡾࠣࡸ࡭࡯ࡳ࠼࡞ࡱࠤࠥࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡲࡪࡽࡐࡢࡩࡨ࠲ࡨࡧ࡬࡭ࠪࡷࡥࡷ࡭ࡥࡵࡅࡲࡲࡹ࡫ࡸࡵࠫ࠾ࡠࡳࠦࠠࠡࠢࢀࠤࡨࡧࡴࡤࡪࠣࠬࡪ࠯ࠠࡼ࡞ࡱࠤࠥࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡲࡪࡽࡐࡢࡩࡨ࠲ࡨࡧ࡬࡭ࠪࡷ࡬࡮ࡹࠩ࠼࡞ࡱࠤࠥࠦࠠࡾ࡞ࡱࠤࠥࢃࠠ࡝ࡰࠣࠤࡪࡲࡳࡦࠢࡾࡠࡳࠦࠠࠡࠢࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣࡳࡷ࡯ࡧࡪࡰࡤࡰࡤࡴࡥࡸࡒࡤ࡫ࡪ࠴ࡣࡢ࡮࡯ࠬࡹ࡮ࡩࡴࠫ࠾ࡠࡳࠦࠠࡾ࡞ࡱࢁࡀࡢ࡮࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱࡟ࡲࠬࣁ")
from ._version import __version__
bstack1ll1ll1ll1_opy_ = None
CONFIG = {}
bstack1ll1lllll_opy_ = {}
bstack11ll11lll_opy_ = {}
bstack11ll11l1_opy_ = None
bstack11ll1l11l1_opy_ = None
SESSION_NAME = None
PLATFORM_INDEX = -1
bstack1l11ll11l1_opy_ = 0
bstack11l1l1lll_opy_ = bstack11lll1l1l1_opy_
bstack1111l1l1ll_opy_ = 1
PARALLELISE_VANILLA_PYTHON = False
PARALLELISE_THREADING_PYTHON = False
FRAMEWORK_NAME = bstack1ll_opy_ (u"ࠩࠪࣂ")
bstack1lll1111l1_opy_ = bstack1ll_opy_ (u"ࠪࠫࣃ")
bstack11l1llllll_opy_ = False
BROWSERSTACK_AUTOMATION = True
bstack1lll111111_opy_ = False
bstack1l111ll1_opy_ = bstack1ll_opy_ (u"ࠫࠬࣄ")
bstack1ll111ll1l_opy_ = []
bstack111l1111_opy_ = threading.Lock()
bstack1l111l11ll_opy_ = threading.Lock()
bstack111l1l11_opy_ = None
bstack1ll1111l1_opy_ = bstack1ll_opy_ (u"ࠬ࠭ࣅ")
SELENIUM_OR_PLAYWRIGHT_INSTALLED = False
bstack1l1l1llll_opy_ = None
bstack1l111111l_opy_ = None
bstack1ll1111ll_opy_ = None
bstack1lll1ll1l1_opy_ = -1
bstack1l1ll1l1l1_opy_ = os.path.join(os.path.expanduser(bstack1ll_opy_ (u"࠭ࡾࠨࣆ")), bstack1ll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧࣇ"), bstack1ll_opy_ (u"ࠨ࠰ࡵࡳࡧࡵࡴ࠮ࡴࡨࡴࡴࡸࡴ࠮ࡪࡨࡰࡵ࡫ࡲ࠯࡬ࡶࡳࡳ࠭ࣈ"))
bstack11111ll11l_opy_ = 0
bstack1l1lllll11_opy_ = 0
bstack1l11l11ll1_opy_ = []
bstack1l1l1ll11_opy_ = []
ROBOT_PYTHON_ERRORS = []
bstack1l1ll1ll1_opy_ = []
bstack1l1ll111_opy_ = bstack1ll_opy_ (u"ࠩࠪࣉ")
bstack1ll11ll1l1_opy_ = bstack1ll_opy_ (u"ࠪࠫ࣊")
bstack11llll1l1l_opy_ = False
bstack111ll111ll_opy_ = False
bstack1l1l1l111l_opy_ = {}
bstack1l11111l1_opy_ = {}
bstack11ll1111l_opy_ = None
bstack1111ll111l_opy_ = None
bstack11ll1l1l11_opy_ = None
bstack111ll11ll1_opy_ = None
bstack11lll11ll1_opy_ = None
bstack11l1l1l1_opy_ = None
bstack1ll1l1ll_opy_ = None
bstack11ll1l1lll_opy_ = None
bstack11l111lll_opy_ = None
bstack1ll1llll1l_opy_ = None
bstack1l1ll1lll_opy_ = None
bstack1111l1111_opy_ = None
bstack1ll1ll1lll_opy_ = None
bstack111l1ll1_opy_ = None
bstack111111l1_opy_ = None
bstack1ll1l111ll_opy_ = None
bstack11l111l1ll_opy_ = None
bstack11l1l11l1_opy_ = None
bstack1ll111l1l_opy_ = None
bstack1l11l1l11_opy_ = None
bstack111l111l1l_opy_ = None
bstack11111l11l_opy_ = None
bstack11ll1l1l1_opy_ = None
thread_local = threading.local()
bstack1l111ll11l_opy_ = False
bstack11l1111l1_opy_ = bstack1ll_opy_ (u"ࠦࠧ࣋")
_11llll1ll1_opy_ = None
logger = logger_utils.get_logger(__name__, bstack11l1l1lll_opy_)
automation_logger = logger_utils.get_automation_logger(__name__)
global_config = Config.bstack1l111l1111_opy_()
percy = bstack1ll1l11l11_opy_()
bstack111ll11l11_opy_ = bstack1111lllll1_opy_()
bstack1ll111l11l_opy_ = bstack1ll1ll111l_opy_()
def bstack1l11ll111_opy_():
  global CONFIG
  global bstack11llll1l1l_opy_
  global global_config
  testContextOptions = bstack1l1lll1111_opy_(CONFIG)
  if bstack1lll1111ll_opy_(CONFIG):
    if (bstack1ll_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ࣌") in testContextOptions and str(testContextOptions[bstack1ll_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ࣍")]).lower() == bstack1ll_opy_ (u"ࠧࡵࡴࡸࡩࠬ࣎")):
      bstack11llll1l1l_opy_ = True
      global_config.bstack11l1ll111_opy_(True)
    if (bstack1ll_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷ࣏ࠬ") in testContextOptions and str(testContextOptions[bstack1ll_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࣐࠭")]).lower() == bstack1ll_opy_ (u"ࠪࡸࡷࡻࡥࠨ࣑")):
      global_config.bstack11l1l11ll_opy_(True)
  else:
    bstack11llll1l1l_opy_ = True
    global_config.bstack11l1ll111_opy_(True)
    global_config.bstack11l1l11ll_opy_(True)
def bstack1lll111ll_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1ll11l11l1_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1lll1lllll_opy_():
  global bstack1l11111l1_opy_
  args = sys.argv
  for i in range(len(args)):
    if bstack1ll_opy_ (u"ࠦ࠲࠳ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡨࡵ࡮ࡧ࡫ࡪࡪ࡮ࡲࡥ࣒ࠣ") == args[i].lower() or bstack1ll_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰࡰࡩ࡭࡬ࠨ࣓") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      bstack1l11111l1_opy_[bstack1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࡤࡌࡉࡍࡇࠪࣔ")] = path
      return path
  return None
bstack1111l11ll_opy_ = re.compile(bstack1ll_opy_ (u"ࡲࠣ࠰࠭ࡃࡡࠪࡻࠩ࠰࠭ࡃ࠮ࢃ࠮ࠫࡁࠥࣕ"))
def bstack111ll1l111_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1111l11ll_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack1ll_opy_ (u"ࠣࠦࡾࠦࣖ") + group + bstack1ll_opy_ (u"ࠤࢀࠦࣗ"), os.environ.get(group))
  return value
def bstack11111111ll_opy_():
  global bstack11ll1l1l1_opy_
  if bstack11ll1l1l1_opy_ is None:
        bstack11ll1l1l1_opy_ = bstack1lll1lllll_opy_()
  bstack111ll11111_opy_ = bstack11ll1l1l1_opy_
  if bstack111ll11111_opy_ and os.path.exists(os.path.abspath(bstack111ll11111_opy_)):
    fileName = bstack111ll11111_opy_
  if bstack1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋࠧࣘ") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨࣙ")])) and not bstack1ll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡑࡥࡲ࡫ࠧࣚ") in locals():
    fileName = os.environ[bstack1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࡤࡌࡉࡍࡇࠪࣛ")]
  if bstack1ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡓࡧ࡭ࡦࠩࣜ") in locals():
    bstack1ll11l1_opy_ = os.path.abspath(fileName)
  else:
    bstack1ll11l1_opy_ = bstack1ll_opy_ (u"ࠨࠩࣝ")
  bstack1l1l1111ll_opy_ = os.getcwd()
  bstack11lll11l11_opy_ = bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬࣞ")
  bstack11ll1111l1_opy_ = bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡥࡲࡲࠧࣟ")
  while (not os.path.exists(bstack1ll11l1_opy_)) and bstack1l1l1111ll_opy_ != bstack1ll_opy_ (u"ࠦࠧ࣠"):
    bstack1ll11l1_opy_ = os.path.join(bstack1l1l1111ll_opy_, bstack11lll11l11_opy_)
    if not os.path.exists(bstack1ll11l1_opy_):
      bstack1ll11l1_opy_ = os.path.join(bstack1l1l1111ll_opy_, bstack11ll1111l1_opy_)
    if bstack1l1l1111ll_opy_ != os.path.dirname(bstack1l1l1111ll_opy_):
      bstack1l1l1111ll_opy_ = os.path.dirname(bstack1l1l1111ll_opy_)
    else:
      bstack1l1l1111ll_opy_ = bstack1ll_opy_ (u"ࠧࠨ࣡")
  bstack11ll1l1l1_opy_ = bstack1ll11l1_opy_ if os.path.exists(bstack1ll11l1_opy_) else None
  return bstack11ll1l1l1_opy_
def bstack11lll1ll11_opy_(config):
    if bstack1ll_opy_ (u"࠭ࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬࠭࣢") in config:
      config[bstack1ll_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࣣࠫ")] = config[bstack1ll_opy_ (u"ࠨࡶࡨࡷࡹࡘࡥࡱࡱࡵࡸ࡮ࡴࡧࠨࣤ")]
    if bstack1ll_opy_ (u"ࠩࡷࡩࡸࡺࡒࡦࡲࡲࡶࡹ࡯࡮ࡨࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣥ") in config:
      config[bstack1ll_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࣦࠧ")] = config[bstack1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࡓࡵࡺࡩࡰࡰࡶࠫࣧ")]
def bstack11l111111l_opy_():
  bstack1ll11l1_opy_ = bstack11111111ll_opy_()
  if not os.path.exists(bstack1ll11l1_opy_):
    bstack1ll11l11ll_opy_(
      bstack1l1l11ll11_opy_.format(os.getcwd()))
  try:
    with open(bstack1ll11l1_opy_, bstack1ll_opy_ (u"ࠬࡸࠧࣨ")) as stream:
      yaml.add_implicit_resolver(bstack1ll_opy_ (u"ࠨࠡࡱࡣࡷ࡬ࡪࡾࣩࠢ"), bstack1111l11ll_opy_)
      yaml.add_constructor(bstack1ll_opy_ (u"ࠢࠢࡲࡤࡸ࡭࡫ࡸࠣ࣪"), bstack111ll1l111_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      bstack11lll1ll11_opy_(config)
      return config
  except:
    with open(bstack1ll11l1_opy_, bstack1ll_opy_ (u"ࠨࡴࠪ࣫")) as stream:
      try:
        config = yaml.safe_load(stream)
        bstack11lll1ll11_opy_(config)
        return config
      except yaml.YAMLError as exc:
        bstack1ll11l11ll_opy_(bstack1l111l1l11_opy_.format(str(exc)))
def bstack1ll1l1l11l_opy_(config):
  bstack1l11l1111_opy_ = bstack111l1l111l_opy_(config)
  for option in list(bstack1l11l1111_opy_):
    if option.lower() in bstack1l111lllll_opy_ and option != bstack1l111lllll_opy_[option.lower()]:
      bstack1l11l1111_opy_[bstack1l111lllll_opy_[option.lower()]] = bstack1l11l1111_opy_[option]
      del bstack1l11l1111_opy_[option]
  return config
def bstack111l1l1l11_opy_():
  global bstack11ll11lll_opy_
  for key, bstack11l1l11ll1_opy_ in bstack1ll111llll_opy_.items():
    if isinstance(bstack11l1l11ll1_opy_, list):
      for var in bstack11l1l11ll1_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack11ll11lll_opy_[key] = os.environ[var]
          break
    elif bstack11l1l11ll1_opy_ in os.environ and os.environ[bstack11l1l11ll1_opy_] and str(os.environ[bstack11l1l11ll1_opy_]).strip():
      bstack11ll11lll_opy_[key] = os.environ[bstack11l1l11ll1_opy_]
  if bstack1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ࣬") in os.environ:
    bstack11ll11lll_opy_[bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹ࣭ࠧ")] = {}
    bstack11ll11lll_opy_[bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ࣮")][bstack1ll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣯ࠧ")] = os.environ[bstack1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨࣰ")]
def bstack1l1l11ll_opy_():
  global bstack1ll1lllll_opy_
  global bstack1l111ll1_opy_
  global bstack1l11111l1_opy_
  bstack1llll1ll1l_opy_ = []
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) - 1 and bstack1ll_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࣱࠪ").lower() == val.lower():
      bstack1ll1lllll_opy_[bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࣲࠬ")] = {}
      bstack1ll1lllll_opy_[bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࣳ")][bstack1ll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣴ")] = sys.argv[idx + 1]
      bstack1llll1ll1l_opy_.extend([idx, idx + 1])
      break
  for key, bstack1l11l1l11l_opy_ in bstack1lll11l1l1_opy_.items():
    if isinstance(bstack1l11l1l11l_opy_, list):
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        for var in bstack1l11l1l11l_opy_:
          if bstack1ll_opy_ (u"ࠫ࠲࠳ࠧࣵ") + var.lower() == val.lower() and key not in bstack1ll1lllll_opy_:
            bstack1ll1lllll_opy_[key] = sys.argv[idx + 1]
            bstack1l111ll1_opy_ += bstack1ll_opy_ (u"ࠬࠦ࠭࠮ࣶࠩ") + var + bstack1ll_opy_ (u"࠭ࠠࠨࣷ") + shlex.quote(sys.argv[idx + 1])
            bstack1ll11l1111_opy_(bstack1l11111l1_opy_, key, sys.argv[idx + 1])
            bstack1llll1ll1l_opy_.extend([idx, idx + 1])
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        if bstack1ll_opy_ (u"ࠧ࠮࠯ࠪࣸ") + bstack1l11l1l11l_opy_.lower() == val.lower() and key not in bstack1ll1lllll_opy_:
          bstack1ll1lllll_opy_[key] = sys.argv[idx + 1]
          bstack1l111ll1_opy_ += bstack1ll_opy_ (u"ࠨࠢ࠰࠱ࣹࠬ") + bstack1l11l1l11l_opy_ + bstack1ll_opy_ (u"ࣺࠩࠣࠫ") + shlex.quote(sys.argv[idx + 1])
          bstack1ll11l1111_opy_(bstack1l11111l1_opy_, key, sys.argv[idx + 1])
          bstack1llll1ll1l_opy_.extend([idx, idx + 1])
  for idx in sorted(set(bstack1llll1ll1l_opy_), reverse=True):
    if idx < len(sys.argv):
      del sys.argv[idx]
def bstack1l11111ll1_opy_(config):
  bstack1ll11l111l_opy_ = config.keys()
  for bstack111ll111l_opy_, bstack1l1ll111l_opy_ in bstack11l111l11_opy_.items():
    if bstack1l1ll111l_opy_ in bstack1ll11l111l_opy_:
      config[bstack111ll111l_opy_] = config[bstack1l1ll111l_opy_]
      del config[bstack1l1ll111l_opy_]
  for bstack111ll111l_opy_, bstack1l1ll111l_opy_ in bstack1111l1l1l1_opy_.items():
    if isinstance(bstack1l1ll111l_opy_, list):
      for bstack1l1l11lll_opy_ in bstack1l1ll111l_opy_:
        if bstack1l1l11lll_opy_ in bstack1ll11l111l_opy_:
          config[bstack111ll111l_opy_] = config[bstack1l1l11lll_opy_]
          del config[bstack1l1l11lll_opy_]
          break
    elif bstack1l1ll111l_opy_ in bstack1ll11l111l_opy_:
      config[bstack111ll111l_opy_] = config[bstack1l1ll111l_opy_]
      del config[bstack1l1ll111l_opy_]
  for bstack1l1l11lll_opy_ in list(config):
    for bstack1111llll_opy_ in bstack11ll11l11_opy_:
      if bstack1l1l11lll_opy_.lower() == bstack1111llll_opy_.lower() and bstack1l1l11lll_opy_ != bstack1111llll_opy_:
        config[bstack1111llll_opy_] = config[bstack1l1l11lll_opy_]
        del config[bstack1l1l11lll_opy_]
  bstack111l1ll1l_opy_ = [{}]
  if not config.get(bstack1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣻ")):
    config[bstack1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣼ")] = [{}]
  bstack111l1ll1l_opy_ = config[bstack1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨࣽ")]
  for platform in bstack111l1ll1l_opy_:
    for bstack1l1l11lll_opy_ in list(platform):
      for bstack1111llll_opy_ in bstack11ll11l11_opy_:
        if bstack1l1l11lll_opy_.lower() == bstack1111llll_opy_.lower() and bstack1l1l11lll_opy_ != bstack1111llll_opy_:
          platform[bstack1111llll_opy_] = platform[bstack1l1l11lll_opy_]
          del platform[bstack1l1l11lll_opy_]
  for bstack111ll111l_opy_, bstack1l1ll111l_opy_ in bstack1111l1l1l1_opy_.items():
    for platform in bstack111l1ll1l_opy_:
      if isinstance(bstack1l1ll111l_opy_, list):
        for bstack1l1l11lll_opy_ in bstack1l1ll111l_opy_:
          if bstack1l1l11lll_opy_ in platform:
            platform[bstack111ll111l_opy_] = platform[bstack1l1l11lll_opy_]
            del platform[bstack1l1l11lll_opy_]
            break
      elif bstack1l1ll111l_opy_ in platform:
        platform[bstack111ll111l_opy_] = platform[bstack1l1ll111l_opy_]
        del platform[bstack1l1ll111l_opy_]
  for bstack1111l111l1_opy_ in bstack11llll11l1_opy_:
    if bstack1111l111l1_opy_ in config:
      if not bstack11llll11l1_opy_[bstack1111l111l1_opy_] in config:
        config[bstack11llll11l1_opy_[bstack1111l111l1_opy_]] = {}
      config[bstack11llll11l1_opy_[bstack1111l111l1_opy_]].update(config[bstack1111l111l1_opy_])
      del config[bstack1111l111l1_opy_]
  for platform in bstack111l1ll1l_opy_:
    for bstack1111l111l1_opy_ in bstack11llll11l1_opy_:
      if bstack1111l111l1_opy_ in list(platform):
        if not bstack11llll11l1_opy_[bstack1111l111l1_opy_] in platform:
          platform[bstack11llll11l1_opy_[bstack1111l111l1_opy_]] = {}
        platform[bstack11llll11l1_opy_[bstack1111l111l1_opy_]].update(platform[bstack1111l111l1_opy_])
        del platform[bstack1111l111l1_opy_]
  config = bstack1ll1l1l11l_opy_(config)
  return config
def bstack1ll1ll1l_opy_(config):
  global bstack1lll1111l1_opy_
  bstack1l1l1111l1_opy_ = False
  bstack111l1llll1_opy_ = os.environ.get(bstack1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡊࡅࡇࡃࡘࡐ࡙ࡥࡌࡐࡅࡄࡐࡤࡏࡄࠨࣾ"))
  if bstack1ll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫࣿ") in config and str(config[bstack1ll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬऀ")]).lower() != bstack1ll_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨँ"):
    if bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧं") not in config or str(config[bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨः")]).lower() == bstack1ll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫऄ"):
      config[bstack1ll_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬअ")] = False
    else:
      bstack1l1l1ll1l1_opy_ = bstack1111ll11_opy_()
      if bstack1ll_opy_ (u"ࠧࡪࡵࡗࡶ࡮ࡧ࡬ࡈࡴ࡬ࡨࠬआ") in bstack1l1l1ll1l1_opy_:
        if not bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬइ") in config:
          config[bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ई")] = {}
        config[bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧउ")][bstack1ll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ऊ")] = bstack1ll_opy_ (u"ࠬࡧࡴࡴ࠯ࡵࡩࡵ࡫ࡡࡵࡧࡵࠫऋ")
        bstack1l1l1111l1_opy_ = True
        bstack1lll1111l1_opy_ = config[bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪऌ")].get(bstack1ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऍ"))
  if bstack1lll1111ll_opy_(config) and bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬऎ") in config and str(config[bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ए")]).lower() != bstack1ll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩऐ") and not bstack1l1l1111l1_opy_:
    if not bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऑ") in config:
      config[bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩऒ")] = {}
    bstack1111lll111_opy_ = config[bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪओ")].get(bstack1ll_opy_ (u"ࠧࡴ࡭࡬ࡴࡇ࡯࡮ࡢࡴࡼࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡸࡧࡴࡪࡱࡱࠫऔ"))
    if bstack111l1llll1_opy_:
      if bstack1111lll111_opy_:
        config[bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬक")][bstack1ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫख")] = bstack111l1llll1_opy_
      elif bstack1ll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬग") not in config[bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨघ")]:
        config[bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩङ")][bstack1ll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨच")] = bstack111l1llll1_opy_
    if not bstack1111lll111_opy_ and bstack1ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩछ") not in config[bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬज")]:
      bstack11l1ll1ll_opy_ = datetime.datetime.now()
      bstack1lll1l1l1_opy_ = bstack11l1ll1ll_opy_.strftime(bstack1ll_opy_ (u"ࠩࠨࡨࡤࠫࡢࡠࠧࡋࠩࡒ࠭झ"))
      hostname = socket.gethostname()
      bstack11l1111l11_opy_ = bstack1ll_opy_ (u"ࠪࠫञ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1ll_opy_ (u"ࠫࢀࢃ࡟ࡼࡿࡢࡿࢂ࠭ट").format(bstack1lll1l1l1_opy_, hostname, bstack11l1111l11_opy_)
      config[bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩठ")][bstack1ll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨड")] = identifier
    bstack1lll1111l1_opy_ = config[bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫढ")].get(bstack1ll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪण"))
  return config
def bstack111l1l11l1_opy_():
  bstack111l11llll_opy_ =  bstack1lll11l1ll_opy_()[bstack1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠨत")]
  return bstack111l11llll_opy_ if bstack111l11llll_opy_ else -1
def bstack111l1ll1l1_opy_(bstack111l11llll_opy_):
  global CONFIG
  if not bstack1ll_opy_ (u"ࠪࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬथ") in CONFIG[bstack1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭द")]:
    return
  CONFIG[bstack1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧध")] = CONFIG[bstack1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨन")].replace(
    bstack1ll_opy_ (u"ࠧࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩऩ"),
    str(bstack111l11llll_opy_)
  )
def bstack1ll11l111_opy_():
  global CONFIG
  if not bstack1ll_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧप") in CONFIG[bstack1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫफ")]:
    return
  bstack11l1ll1ll_opy_ = datetime.datetime.now()
  bstack1lll1l1l1_opy_ = bstack11l1ll1ll_opy_.strftime(bstack1ll_opy_ (u"ࠪࠩࡩ࠳ࠥࡣ࠯ࠨࡌ࠿ࠫࡍࠨब"))
  CONFIG[bstack1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭भ")] = CONFIG[bstack1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧम")].replace(
    bstack1ll_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬय"),
    bstack1lll1l1l1_opy_
  )
def bstack11ll11l11l_opy_():
  global CONFIG
  if bstack1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩर") in CONFIG and not bool(CONFIG[bstack1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪऱ")]):
    del CONFIG[bstack1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫल")]
    return
  if not bstack1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬळ") in CONFIG:
    CONFIG[bstack1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ऴ")] = bstack1ll_opy_ (u"ࠬࠩࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨव")
  if bstack1ll_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬश") in CONFIG[bstack1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩष")]:
    bstack1ll11l111_opy_()
    os.environ[bstack1ll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬस")] = CONFIG[bstack1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫह")]
  if not bstack1ll_opy_ (u"ࠪࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬऺ") in CONFIG[bstack1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ऻ")]:
    return
  bstack111l11llll_opy_ = bstack1ll_opy_ (u"़ࠬ࠭")
  bstack1l11l1lll_opy_ = bstack111l1l11l1_opy_()
  if bstack1l11l1lll_opy_ != -1:
    bstack111l11llll_opy_ = bstack1ll_opy_ (u"࠭ࡃࡊࠢࠪऽ") + str(bstack1l11l1lll_opy_)
  if bstack111l11llll_opy_ == bstack1ll_opy_ (u"ࠧࠨा"):
    bstack1111l11l11_opy_ = bstack1111ll11l_opy_(CONFIG[bstack1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫि")])
    if bstack1111l11l11_opy_ != -1:
      bstack111l11llll_opy_ = str(bstack1111l11l11_opy_)
  if bstack111l11llll_opy_:
    bstack111l1ll1l1_opy_(bstack111l11llll_opy_)
    os.environ[bstack1ll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ी")] = CONFIG[bstack1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬु")]
def bstack11l1lll11_opy_(bstack11ll1111ll_opy_, bstack1l11111111_opy_, path):
  json_data = {
    bstack1ll_opy_ (u"ࠫ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨू"): bstack1l11111111_opy_
  }
  if os.path.exists(path):
    bstack1111l1l1_opy_ = json.load(open(path, bstack1ll_opy_ (u"ࠬࡸࡢࠨृ")))
  else:
    bstack1111l1l1_opy_ = {}
  bstack1111l1l1_opy_[bstack11ll1111ll_opy_] = json_data
  with open(path, bstack1ll_opy_ (u"ࠨࡷࠬࠤॄ")) as outfile:
    json.dump(bstack1111l1l1_opy_, outfile)
def bstack1111ll11l_opy_(bstack11ll1111ll_opy_):
  bstack11ll1111ll_opy_ = str(bstack11ll1111ll_opy_)
  bstack1lllll11ll_opy_ = os.path.join(os.path.expanduser(bstack1ll_opy_ (u"ࠧࡿࠩॅ")), bstack1ll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨॆ"))
  try:
    if not os.path.exists(bstack1lllll11ll_opy_):
      os.makedirs(bstack1lllll11ll_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1ll_opy_ (u"ࠩࢁࠫे")), bstack1ll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪै"), bstack1ll_opy_ (u"ࠫ࠳ࡨࡵࡪ࡮ࡧ࠱ࡳࡧ࡭ࡦ࠯ࡦࡥࡨ࡮ࡥ࠯࡬ࡶࡳࡳ࠭ॉ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1ll_opy_ (u"ࠬࡽࠧॊ")):
        pass
      with open(file_path, bstack1ll_opy_ (u"ࠨࡷࠬࠤो")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1ll_opy_ (u"ࠧࡳࠩौ")) as bstack11lll11l_opy_:
      bstack11llll11l_opy_ = json.load(bstack11lll11l_opy_)
    if bstack11ll1111ll_opy_ in bstack11llll11l_opy_:
      bstack1ll1111lll_opy_ = bstack11llll11l_opy_[bstack11ll1111ll_opy_][bstack1ll_opy_ (u"ࠨ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ्ࠬ")]
      bstack11111llll_opy_ = int(bstack1ll1111lll_opy_) + 1
      bstack11l1lll11_opy_(bstack11ll1111ll_opy_, bstack11111llll_opy_, file_path)
      return bstack11111llll_opy_
    else:
      bstack11l1lll11_opy_(bstack11ll1111ll_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warning(bstack1l1l1111_opy_.format(str(e)))
    return -1
def bstack1l1ll11l1_opy_(config):
  if not config[bstack1ll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫॎ")] or not config[bstack1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ॏ")]:
    return True
  else:
    return False
def bstack1ll111lll_opy_(config, index=0):
  global bstack11l1llllll_opy_
  bstack111l11l111_opy_ = {}
  caps = bstack111111l1l_opy_ + bstack1lllllll11l_opy_
  if config.get(bstack1ll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨॐ"), False):
    bstack111l11l111_opy_[bstack1ll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩ॑")] = True
    bstack111l11l111_opy_[bstack1ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࡒࡴࡹ࡯࡯࡯ࡵ॒ࠪ")] = config.get(bstack1ll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࡓࡵࡺࡩࡰࡰࡶࠫ॓"), {})
  if bstack11l1llllll_opy_:
    caps += bstack11111ll11_opy_
  for key in config:
    if key in caps + [bstack1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ॔")]:
      continue
    bstack111l11l111_opy_[key] = config[key]
  if bstack1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॕ") in config:
    for bstack1l1l1l111_opy_ in config[bstack1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॖ")][index]:
      if bstack1l1l1l111_opy_ in caps:
        continue
      bstack111l11l111_opy_[bstack1l1l1l111_opy_] = config[bstack1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॗ")][index][bstack1l1l1l111_opy_]
  bstack111l11l111_opy_[bstack1ll_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧक़")] = socket.gethostname()
  if bstack1ll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧख़") in bstack111l11l111_opy_:
    del (bstack111l11l111_opy_[bstack1ll_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨग़")])
  return bstack111l11l111_opy_
def bstack1111ll11ll_opy_(config):
  global bstack11l1llllll_opy_
  bstack1l1l111l1l_opy_ = {}
  caps = bstack1lllllll11l_opy_
  if bstack11l1llllll_opy_:
    caps += bstack11111ll11_opy_
  for key in caps:
    if key in config:
      bstack1l1l111l1l_opy_[key] = config[key]
  return bstack1l1l111l1l_opy_
def bstack11l1ll11l1_opy_(bstack111l11l111_opy_, bstack1l1l111l1l_opy_):
  bstack1l11l1l1_opy_ = {}
  for key in bstack111l11l111_opy_.keys():
    if key in bstack11l111l11_opy_:
      bstack1l11l1l1_opy_[bstack11l111l11_opy_[key]] = bstack111l11l111_opy_[key]
    else:
      bstack1l11l1l1_opy_[key] = bstack111l11l111_opy_[key]
  for key in bstack1l1l111l1l_opy_:
    if key in bstack11l111l11_opy_:
      bstack1l11l1l1_opy_[bstack11l111l11_opy_[key]] = bstack1l1l111l1l_opy_[key]
    else:
      bstack1l11l1l1_opy_[key] = bstack1l1l111l1l_opy_[key]
  return bstack1l11l1l1_opy_
def get_caps(config, index=0):
  global bstack11l1llllll_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack1ll1lll1_opy_ = bstack111ll1111_opy_(bstack1l1lllll_opy_, config, logger)
  bstack1l1l111l1l_opy_ = bstack1111ll11ll_opy_(config)
  bstack1111l1ll_opy_ = bstack1lllllll11l_opy_
  bstack1111l1ll_opy_ += bstack1l1l1lllll_opy_
  bstack1l1l111l1l_opy_ = update(bstack1l1l111l1l_opy_, bstack1ll1lll1_opy_)
  if bstack11l1llllll_opy_:
    bstack1111l1ll_opy_ += bstack11111ll11_opy_
  if bstack1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫज़") in config:
    if bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧड़") in config[bstack1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ढ़")][index]:
      caps[bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩफ़")] = config[bstack1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨय़")][index][bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫॠ")]
    if bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨॡ") in config[bstack1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫॢ")][index]:
      caps[bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪॣ")] = str(config[bstack1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭।")][index][bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ॥")])
    bstack1lll1llll_opy_ = bstack111ll1111_opy_(bstack1l1lllll_opy_, config[bstack1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ०")][index], logger)
    bstack1111l1ll_opy_ += list(bstack1lll1llll_opy_.keys())
    for bstack1111l1lll_opy_ in bstack1111l1ll_opy_:
      if bstack1111l1lll_opy_ in config[bstack1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ१")][index]:
        if bstack1111l1lll_opy_ == bstack1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ२"):
          try:
            bstack1lll1llll_opy_[bstack1111l1lll_opy_] = str(config[bstack1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ३")][index][bstack1111l1lll_opy_] * 1.0)
          except:
            bstack1lll1llll_opy_[bstack1111l1lll_opy_] = str(config[bstack1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ४")][index][bstack1111l1lll_opy_])
        else:
          bstack1lll1llll_opy_[bstack1111l1lll_opy_] = config[bstack1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭५")][index][bstack1111l1lll_opy_]
        del (config[bstack1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ६")][index][bstack1111l1lll_opy_])
    bstack1l1l111l1l_opy_ = update(bstack1l1l111l1l_opy_, bstack1lll1llll_opy_)
  bstack111l11l111_opy_ = bstack1ll111lll_opy_(config, index)
  for bstack1l1l11lll_opy_ in bstack1lllllll11l_opy_ + list(bstack1ll1lll1_opy_.keys()):
    if bstack1l1l11lll_opy_ in bstack111l11l111_opy_:
      bstack1l1l111l1l_opy_[bstack1l1l11lll_opy_] = bstack111l11l111_opy_[bstack1l1l11lll_opy_]
      del (bstack111l11l111_opy_[bstack1l1l11lll_opy_])
  if bstack111lll1ll_opy_(config):
    bstack111l11l111_opy_[bstack1ll_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ७")] = True
    caps.update(bstack1l1l111l1l_opy_)
    caps[bstack1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ८")] = bstack111l11l111_opy_
  else:
    bstack111l11l111_opy_[bstack1ll_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧ९")] = False
    caps.update(bstack11l1ll11l1_opy_(bstack111l11l111_opy_, bstack1l1l111l1l_opy_))
    if bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭॰") in caps:
      caps[bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪॱ")] = caps[bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨॲ")]
      del (caps[bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩॳ")])
    if bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ॴ") in caps:
      caps[bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨॵ")] = caps[bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨॶ")]
      del (caps[bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩॷ")])
  return caps
def bstack1lll11l111_opy_():
  global bstack1ll1111l1_opy_
  global CONFIG
  if bstack1ll1111l1_opy_ != bstack1ll_opy_ (u"ࠩࠪॸ") and (bstack1ll1111l1_opy_.startswith(bstack1ll_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫॹ")) or bstack1ll1111l1_opy_.startswith(bstack1ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࠭ॺ"))):
    return bstack1ll1111l1_opy_
  if bstack1ll11l11l1_opy_() <= version.parse(bstack1ll_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬॻ")):
    if bstack1ll1111l1_opy_ != bstack1ll_opy_ (u"࠭ࠧॼ"):
      return bstack1ll_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣॽ") + bstack1ll1111l1_opy_ + bstack1ll_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧॾ")
    return bstack1lllll1l1l_opy_
  if bstack1ll1111l1_opy_ != bstack1ll_opy_ (u"ࠩࠪॿ"):
    return bstack1ll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧঀ") + bstack1ll1111l1_opy_ + bstack1ll_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧঁ")
  return bstack111l11lll1_opy_
def bstack11111llll1_opy_(options):
  return hasattr(options, bstack1ll_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭ং"))
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
def bstack11l1ll1l11_opy_(options, bstack1l1111111l_opy_):
  for bstack1l11l1llll_opy_ in bstack1l1111111l_opy_:
    if bstack1l11l1llll_opy_ in [bstack1ll_opy_ (u"࠭ࡡࡳࡩࡶࠫঃ"), bstack1ll_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫ঄")]:
      continue
    if bstack1l11l1llll_opy_ in options._experimental_options:
      options._experimental_options[bstack1l11l1llll_opy_] = update(options._experimental_options[bstack1l11l1llll_opy_],
                                                         bstack1l1111111l_opy_[bstack1l11l1llll_opy_])
    else:
      options.add_experimental_option(bstack1l11l1llll_opy_, bstack1l1111111l_opy_[bstack1l11l1llll_opy_])
  if bstack1ll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭অ") in bstack1l1111111l_opy_:
    for arg in bstack1l1111111l_opy_[bstack1ll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧআ")]:
      options.add_argument(arg)
    del (bstack1l1111111l_opy_[bstack1ll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨই")])
  if bstack1ll_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨঈ") in bstack1l1111111l_opy_:
    for ext in bstack1l1111111l_opy_[bstack1ll_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩউ")]:
      try:
        options.add_extension(ext)
      except OSError:
        options.add_encoded_extension(ext)
    del (bstack1l1111111l_opy_[bstack1ll_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪঊ")])
def bstack1l11l11ll_opy_(options):
  global CONFIG
  global bstack1lll111111_opy_
  try:
    if not bstack1lll111111_opy_ or not options:
      return options
    from bstack_utils.bstack1l11ll1111_opy_ import bstack1l11l1l1l1_opy_
    bstack1llll11ll1_opy_ = bstack1l11l1l1l1_opy_(options, bstack1ll1l1l1_opy_=bstack1ll_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢঋ"))
    if bstack1llll11ll1_opy_ > 0:
      logger.debug(bstack1ll_opy_ (u"ࠣࡎࡲࡥࡩࠦࡴࡦࡵࡷ࡭ࡳ࡭࠺ࠡࡃࡧࡨࡪࡪࠠࡼࡿࠣࡨࡪ࡬ࡡࡶ࡮ࡷࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠠࡧࡱࡵࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠦঌ").format(bstack1llll11ll1_opy_))
  except Exception as e:
    logger.debug(bstack1ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡯࡮࡫ࡧࡦࡸࠥࡲ࡯ࡢࡦࠣࡸࡪࡹࡴࡪࡰࡪࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡴࡶࡴࡪࡱࡱࡷ࠿ࠦࡻࡾࠤ঍").format(e))
  return options
def bstack11llll1111_opy_(options, bstack1llll1l1ll_opy_):
  if bstack1ll_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩ঎") in bstack1llll1l1ll_opy_:
    for bstack1l1111lll_opy_ in bstack1llll1l1ll_opy_[bstack1ll_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪএ")]:
      if bstack1l1111lll_opy_ in options._preferences:
        options._preferences[bstack1l1111lll_opy_] = update(options._preferences[bstack1l1111lll_opy_], bstack1llll1l1ll_opy_[bstack1ll_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫঐ")][bstack1l1111lll_opy_])
      else:
        options.set_preference(bstack1l1111lll_opy_, bstack1llll1l1ll_opy_[bstack1ll_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬ঑")][bstack1l1111lll_opy_])
  if bstack1ll_opy_ (u"ࠧࡢࡴࡪࡷࠬ঒") in bstack1llll1l1ll_opy_:
    for arg in bstack1llll1l1ll_opy_[bstack1ll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ও")]:
      options.add_argument(arg)
def bstack11ll1ll1l_opy_(options, bstack1l1llll1_opy_):
  if bstack1ll_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࠪঔ") in bstack1l1llll1_opy_:
    options.use_webview(bool(bstack1l1llll1_opy_[bstack1ll_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࠫক")]))
  bstack11l1ll1l11_opy_(options, bstack1l1llll1_opy_)
def bstack111lllll1l_opy_(options, bstack111lllll1_opy_):
  for bstack11l11lll11_opy_ in bstack111lllll1_opy_:
    if bstack11l11lll11_opy_ in [bstack1ll_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨখ"), bstack1ll_opy_ (u"ࠬࡧࡲࡨࡵࠪগ")]:
      continue
    options.set_capability(bstack11l11lll11_opy_, bstack111lllll1_opy_[bstack11l11lll11_opy_])
  if bstack1ll_opy_ (u"࠭ࡡࡳࡩࡶࠫঘ") in bstack111lllll1_opy_:
    for arg in bstack111lllll1_opy_[bstack1ll_opy_ (u"ࠧࡢࡴࡪࡷࠬঙ")]:
      options.add_argument(arg)
  if bstack1ll_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬচ") in bstack111lllll1_opy_:
    options.bstack111l111lll_opy_(bool(bstack111lllll1_opy_[bstack1ll_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭ছ")]))
def bstack1111l1l11l_opy_(options, bstack111111ll11_opy_):
  for bstack11l111llll_opy_ in bstack111111ll11_opy_:
    if bstack11l111llll_opy_ in [bstack1ll_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧজ"), bstack1ll_opy_ (u"ࠫࡦࡸࡧࡴࠩঝ")]:
      continue
    options._options[bstack11l111llll_opy_] = bstack111111ll11_opy_[bstack11l111llll_opy_]
  if bstack1ll_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩঞ") in bstack111111ll11_opy_:
    for bstack1111111l_opy_ in bstack111111ll11_opy_[bstack1ll_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪট")]:
      options.bstack11lll1111_opy_(
        bstack1111111l_opy_, bstack111111ll11_opy_[bstack1ll_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫঠ")][bstack1111111l_opy_])
  if bstack1ll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ড") in bstack111111ll11_opy_:
    for arg in bstack111111ll11_opy_[bstack1ll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧঢ")]:
      options.add_argument(arg)
def bstack1l111llll_opy_(options, caps):
  if not hasattr(options, bstack1ll_opy_ (u"ࠪࡏࡊ࡟ࠧণ")):
    return
  if options.KEY == bstack1ll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩত"):
    options = a11y.bstack1l1ll11ll1_opy_(bstack11l1lll1ll_opy_=options, config=CONFIG)
  if options.KEY == bstack1ll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪথ") and options.KEY in caps:
    bstack11l1ll1l11_opy_(options, caps[bstack1ll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫদ")])
  elif options.KEY == bstack1ll_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬধ") and options.KEY in caps:
    bstack11llll1111_opy_(options, caps[bstack1ll_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ন")])
  elif options.KEY == bstack1ll_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪ঩") and options.KEY in caps:
    bstack111lllll1l_opy_(options, caps[bstack1ll_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫপ")])
  elif options.KEY == bstack1ll_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬফ") and options.KEY in caps:
    bstack11ll1ll1l_opy_(options, caps[bstack1ll_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ব")])
  elif options.KEY == bstack1ll_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬভ") and options.KEY in caps:
    bstack1111l1l11l_opy_(options, caps[bstack1ll_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ম")])
def bstack111lll1l11_opy_(caps):
  global bstack11l1llllll_opy_
  if isinstance(os.environ.get(bstack1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩয")), str):
    bstack11l1llllll_opy_ = eval(os.getenv(bstack1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪর")))
  if bstack11l1llllll_opy_:
    if bstack1lll111ll_opy_() < version.parse(bstack1ll_opy_ (u"ࠪ࠶࠳࠹࠮࠱ࠩ঱")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1ll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫল")
    if bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ঳") in caps:
      browser = caps[bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ঴")]
    elif bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ঵") in caps:
      browser = caps[bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩশ")]
    browser = str(browser).lower()
    if browser == bstack1ll_opy_ (u"ࠩ࡬ࡴ࡭ࡵ࡮ࡦࠩষ") or browser == bstack1ll_opy_ (u"ࠪ࡭ࡵࡧࡤࠨস"):
      browser = bstack1ll_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫহ")
    if browser == bstack1ll_opy_ (u"ࠬࡹࡡ࡮ࡵࡸࡲ࡬࠭঺"):
      browser = bstack1ll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭঻")
    if browser not in [bstack1ll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫়ࠧ"), bstack1ll_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭ঽ"), bstack1ll_opy_ (u"ࠩ࡬ࡩࠬা"), bstack1ll_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪি"), bstack1ll_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬী")]:
      return None
    try:
      package = bstack1ll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡿࢂ࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧু").format(browser)
      name = bstack1ll_opy_ (u"࠭ࡏࡱࡶ࡬ࡳࡳࡹࠧূ")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack11111llll1_opy_(options):
        return None
      for bstack1l1l11lll_opy_ in caps.keys():
        options.set_capability(bstack1l1l11lll_opy_, caps[bstack1l1l11lll_opy_])
      bstack1l111llll_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1111lll11l_opy_(options, bstack11ll1ll1ll_opy_):
  if not bstack11111llll1_opy_(options):
    return
  for bstack1l1l11lll_opy_ in bstack11ll1ll1ll_opy_.keys():
    if bstack1l1l11lll_opy_ in bstack1l1l1lllll_opy_:
      continue
    if bstack1l1l11lll_opy_ in options._caps and type(options._caps[bstack1l1l11lll_opy_]) in [dict, list]:
      options._caps[bstack1l1l11lll_opy_] = update(options._caps[bstack1l1l11lll_opy_], bstack11ll1ll1ll_opy_[bstack1l1l11lll_opy_])
    else:
      options.set_capability(bstack1l1l11lll_opy_, bstack11ll1ll1ll_opy_[bstack1l1l11lll_opy_])
  bstack1l111llll_opy_(options, bstack11ll1ll1ll_opy_)
  if bstack1ll_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ࠭ৃ") in options._caps:
    if options._caps[bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ৄ")] and options._caps[bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ৅")].lower() != bstack1ll_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫ৆"):
      del options._caps[bstack1ll_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪে")]
def bstack11l1lll111_opy_(proxy_config):
  if bstack1ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩৈ") in proxy_config:
    proxy_config[bstack1ll_opy_ (u"࠭ࡳࡴ࡮ࡓࡶࡴࡾࡹࠨ৉")] = proxy_config[bstack1ll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ৊")]
    del (proxy_config[bstack1ll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬো")])
  if bstack1ll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬৌ") in proxy_config and proxy_config[bstack1ll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ্࠭")].lower() != bstack1ll_opy_ (u"ࠫࡩ࡯ࡲࡦࡥࡷࠫৎ"):
    proxy_config[bstack1ll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ৏")] = bstack1ll_opy_ (u"࠭࡭ࡢࡰࡸࡥࡱ࠭৐")
  if bstack1ll_opy_ (u"ࠧࡱࡴࡲࡼࡾࡇࡵࡵࡱࡦࡳࡳ࡬ࡩࡨࡗࡵࡰࠬ৑") in proxy_config:
    proxy_config[bstack1ll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫ৒")] = bstack1ll_opy_ (u"ࠩࡳࡥࡨ࠭৓")
  return proxy_config
def bstack1ll1l1l1l1_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1ll_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩ৔") in config:
    return proxy
  config[bstack1ll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪ৕")] = bstack11l1lll111_opy_(config[bstack1ll_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ৖")])
  if proxy == None:
    proxy = Proxy(config[bstack1ll_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬৗ")])
  return proxy
def bstack1111ll1l_opy_(self):
  global CONFIG
  global bstack1111l1111_opy_
  try:
    proxy = bstack11lllll1_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1ll_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ৘")):
        proxies = bstack1llll11111_opy_(proxy, bstack1lll11l111_opy_())
        if len(proxies) > 0:
          protocol, bstack11l1ll11l_opy_ = proxies.popitem()
          if bstack1ll_opy_ (u"ࠣ࠼࠲࠳ࠧ৙") in bstack11l1ll11l_opy_:
            return bstack11l1ll11l_opy_
          else:
            return bstack1ll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ৚") + bstack11l1ll11l_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1ll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡰࡳࡱࡻࡽࠥࡻࡲ࡭ࠢ࠽ࠤࢀࢃࠢ৛").format(str(e)))
  return bstack1111l1111_opy_(self)
def bstack1111l11lll_opy_():
  global CONFIG
  return bstack1l1ll11l11_opy_(CONFIG) and bstack1ll1l1ll1l_opy_() and bstack1ll11l11l1_opy_() >= version.parse(bstack1llll1ll_opy_)
def bstack1ll11ll11_opy_():
  global CONFIG
  return (bstack1ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧড়") in CONFIG or bstack1ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩঢ়") in CONFIG) and bstack1l1111l1l1_opy_()
def bstack111l1l111l_opy_(config):
  bstack1l11l1111_opy_ = {}
  if bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ৞") in config:
    bstack1l11l1111_opy_ = config[bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫয়")]
  if bstack1ll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧৠ") in config:
    bstack1l11l1111_opy_ = config[bstack1ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨৡ")]
  proxy = bstack11lllll1_opy_(config)
  if proxy:
    if proxy.endswith(bstack1ll_opy_ (u"ࠪ࠲ࡵࡧࡣࠨৢ")) and os.path.isfile(proxy):
      bstack1l11l1111_opy_[bstack1ll_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧৣ")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1ll_opy_ (u"ࠬ࠴ࡰࡢࡥࠪ৤")):
        proxies = bstack11l11ll11_opy_(config, bstack1lll11l111_opy_())
        if len(proxies) > 0:
          protocol, bstack11l1ll11l_opy_ = proxies.popitem()
          if bstack1ll_opy_ (u"ࠨ࠺࠰࠱ࠥ৥") in bstack11l1ll11l_opy_:
            parsed_url = urlparse(bstack11l1ll11l_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1ll_opy_ (u"ࠢ࠻࠱࠲ࠦ০") + bstack11l1ll11l_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1l11l1111_opy_[bstack1ll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡈࡰࡵࡷࠫ১")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1l11l1111_opy_[bstack1ll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬ২")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1l11l1111_opy_[bstack1ll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭৩")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1l11l1111_opy_[bstack1ll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧ৪")] = str(parsed_url.password)
  return bstack1l11l1111_opy_
def bstack1l1lll1111_opy_(config):
  if bstack1ll_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪ৫") in config:
    return config[bstack1ll_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫ৬")]
  return {}
def update_caps_for_local(caps):
  global bstack1lll1111l1_opy_
  if bstack1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ৭") in caps:
    caps[bstack1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ৮")][bstack1ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨ৯")] = True
    if bstack1lll1111l1_opy_:
      caps[bstack1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫৰ")][bstack1ll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ৱ")] = bstack1lll1111l1_opy_
  else:
    caps[bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪ৲")] = True
    if bstack1lll1111l1_opy_:
      caps[bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ৳")] = bstack1lll1111l1_opy_
@measure(event_name=EVENTS.bstack1l1l1llll1_opy_, stage=STAGE.bstack11llll111l_opy_, bstack111l11111_opy_=SESSION_NAME)
def bstack1l1llll1l1_opy_():
  global CONFIG, bstack1lll1111l1_opy_
  if not bstack1lll1111ll_opy_(CONFIG) or cli.is_enabled(CONFIG):
    return
  if bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ৴") in CONFIG and bstack11l1l1l11l_opy_(CONFIG[bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ৵")]):
    if (
      bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭৶") in CONFIG
      and bstack11l1l1l11l_opy_(CONFIG[bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ৷")].get(bstack1ll_opy_ (u"ࠫࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠨ৸")))
    ):
      logger.debug(bstack1ll_opy_ (u"ࠧࡒ࡯ࡤࡣ࡯ࠤࡧ࡯࡮ࡢࡴࡼࠤࡳࡵࡴࠡࡵࡷࡥࡷࡺࡥࡥࠢࡤࡷࠥࡹ࡫ࡪࡲࡅ࡭ࡳࡧࡲࡺࡋࡱ࡭ࡹ࡯ࡡ࡭࡫ࡶࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠨ৹"))
      return
    bstack1l11l1111_opy_ = bstack111l1l111l_opy_(CONFIG)
    bstack1lll1111l1_opy_ = bstack1l11l1111_opy_.get(bstack1ll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ৺")) or bstack1lll1111l1_opy_
    bstack1111l1lll1_opy_(CONFIG[bstack1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ৻")], bstack1l11l1111_opy_)
def bstack1111l1lll1_opy_(key, bstack1l11l1111_opy_):
  global bstack1ll1ll1ll1_opy_
  logger.info(bstack1l11l11l1l_opy_)
  try:
    bstack1ll1ll1ll1_opy_ = Local()
    bstack1ll111lll1_opy_ = {bstack1ll_opy_ (u"ࠨ࡭ࡨࡽࠬৼ"): key}
    bstack1ll111lll1_opy_.update(bstack1l11l1111_opy_)
    logger.debug(bstack111l1ll11_opy_.format(str(bstack1ll111lll1_opy_)).replace(key, bstack1ll_opy_ (u"ࠩ࡞ࡖࡊࡊࡁࡄࡖࡈࡈࡢ࠭৽")))
    bstack1ll1ll1ll1_opy_.start(**bstack1ll111lll1_opy_)
    if bstack1ll1ll1ll1_opy_.isRunning():
      logger.info(bstack11l1l1lll1_opy_)
  except Exception as e:
    bstack1ll11l11ll_opy_(bstack111lll111l_opy_.format(str(e)))
def bstack1ll1111l_opy_():
  global bstack1ll1ll1ll1_opy_
  if bstack1ll1ll1ll1_opy_.isRunning():
    logger.info(bstack11l111l111_opy_)
    bstack1ll1ll1ll1_opy_.stop()
  if bstack1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡇࡉࡋࡇࡕࡍࡖࡢࡐࡔࡉࡁࡍࡡࡌࡈࠬ৾") in os.environ:
    del os.environ[bstack1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡈࡊࡌࡁࡖࡎࡗࡣࡑࡕࡃࡂࡎࡢࡍࡉ࠭৿")]
  bstack1ll1ll1ll1_opy_ = None
def bstack111l1l1lll_opy_(bstack1lllllll111_opy_=[]):
  global CONFIG
  bstack1l1ll1ll1l_opy_ = []
  bstack1llll11ll_opy_ = [bstack1ll_opy_ (u"ࠬࡵࡳࠨ਀"), bstack1ll_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩਁ"), bstack1ll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫਂ"), bstack1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪਃ"), bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ਄"), bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫਅ")]
  try:
    for err in bstack1lllllll111_opy_:
      bstack11l111lll1_opy_ = {}
      for k in bstack1llll11ll_opy_:
        val = CONFIG[bstack1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਆ")][int(err[bstack1ll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫਇ")])].get(k)
        if val:
          bstack11l111lll1_opy_[k] = val
      if(err[bstack1ll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬਈ")] != bstack1ll_opy_ (u"ࠧࠨਉ")):
        bstack11l111lll1_opy_[bstack1ll_opy_ (u"ࠨࡶࡨࡷࡹࡹࠧਊ")] = {
          err[bstack1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ਋")]: err[bstack1ll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ਌")]
        }
        bstack1l1ll1ll1l_opy_.append(bstack11l111lll1_opy_)
  except Exception as e:
    logger.debug(bstack1ll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡰࡴࡰࡥࡹࡺࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷ࠾ࠥ࠭਍") + str(e))
  finally:
    return bstack1l1ll1ll1l_opy_
def bstack1l111l1ll_opy_(file_name):
  bstack11ll1l1ll_opy_ = []
  try:
    bstack11l11ll1l1_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack11l11ll1l1_opy_):
      with open(bstack11l11ll1l1_opy_) as f:
        bstack1l1l1lll_opy_ = json.load(f)
        bstack11ll1l1ll_opy_ = bstack1l1l1lll_opy_
      os.remove(bstack11l11ll1l1_opy_)
    return bstack11ll1l1ll_opy_
  except Exception as e:
    logger.debug(bstack1ll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧ࡫ࡱࡨ࡮ࡴࡧࠡࡧࡵࡶࡴࡸࠠ࡭࡫ࡶࡸ࠿ࠦࠧ਎") + str(e))
    return bstack11ll1l1ll_opy_
def bstack11lll111l_opy_():
  try:
      import time
      from bstack_utils.constants import bstack11llll11ll_opy_, EVENTS
      from bstack_utils.helper import bstack1l1111l111_opy_, get_host_info, global_config
      from datetime import datetime
      from filelock import FileLock
      from bstack_utils.bstack1l11ll1lll_opy_ import bstack1l11l1ll11_opy_
      bstack1l11l1ll11_opy_.bstack11lllll11_opy_()
      bstack1ll11ll1l_opy_ = os.path.join(os.getcwd(), bstack1ll_opy_ (u"࠭࡬ࡰࡩࠪਏ"), bstack1ll_opy_ (u"ࠧ࡬ࡧࡼ࠱ࡲ࡫ࡴࡳ࡫ࡦࡷ࠳ࡰࡳࡰࡰࠪਐ"))
      data = None
      lock = FileLock(bstack1ll11ll1l_opy_+bstack1ll_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢ਑"), timeout=2)
      try:
          with lock:
              with open(bstack1ll11ll1l_opy_, bstack1ll_opy_ (u"ࠤࡵࠦ਒"), encoding=bstack1ll_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤਓ")) as file:
                  data = json.load(file)
      except Exception as e:
          logger.debug(bstack1ll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡳࡧࡤࡨࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵࠣࡪ࡮ࡲࡥ࠻ࠢࡾࢁࠧਔ").format(e))
          return
      if not data:
          return
      def bstack111llll1ll_opy_():
          try:
              config = {
                  bstack1ll_opy_ (u"ࠧ࡮ࡥࡢࡦࡨࡶࡸࠨਕ"): {
                      bstack1ll_opy_ (u"ࠨࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠧਖ"): bstack1ll_opy_ (u"ࠢࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠥਗ"),
                  }
              }
              bstack1lll1ll1_opy_ = datetime.utcnow()
              bstack11l1ll1ll_opy_ = bstack1lll1ll1_opy_.strftime(bstack1ll_opy_ (u"ࠣࠧ࡜࠱ࠪࡳ࠭ࠦࡦࡗࠩࡍࡀࠥࡎ࠼ࠨࡗ࠳ࠫࡦࠡࡗࡗࡇࠧਘ"))
              test_id = os.environ.get(bstack1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧਙ")) if os.environ.get(bstack1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨਚ")) else global_config.get_property(bstack1ll_opy_ (u"ࠦࡸࡪ࡫ࡓࡷࡱࡍࡩࠨਛ"))
              payload = {
                  bstack1ll_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠤਜ"): bstack1ll_opy_ (u"ࠨࡳࡥ࡭ࡢࡩࡻ࡫࡮ࡵࡵࠥਝ"),
                  bstack1ll_opy_ (u"ࠢࡥࡣࡷࡥࠧਞ"): {
                      bstack1ll_opy_ (u"ࠣࡶࡨࡷࡹ࡮ࡵࡣࡡࡸࡹ࡮ࡪࠢਟ"): test_id,
                      bstack1ll_opy_ (u"ࠤࡦࡶࡪࡧࡴࡦࡦࡢࡨࡦࡿࠢਠ"): bstack11l1ll1ll_opy_,
                      bstack1ll_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡱࡥࡲ࡫ࠢਡ"): bstack1ll_opy_ (u"ࠦࡘࡊࡋࡇࡧࡤࡸࡺࡸࡥࡑࡧࡵࡪࡴࡸ࡭ࡢࡰࡦࡩࠧਢ"),
                      bstack1ll_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣ࡯ࡹ࡯࡯ࠤਣ"): {
                          bstack1ll_opy_ (u"ࠨ࡭ࡦࡣࡶࡹࡷ࡫ࡳࠣਤ"): data,
                          bstack1ll_opy_ (u"ࠢࡴࡦ࡮ࡖࡺࡴࡉࡥࠤਥ"): global_config.get_property(bstack1ll_opy_ (u"ࠣࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠥਦ"))
                      },
                      bstack1ll_opy_ (u"ࠤࡸࡷࡪࡸ࡟ࡥࡣࡷࡥࠧਧ"): global_config.get_property(bstack1ll_opy_ (u"ࠥࡹࡸ࡫ࡲࡏࡣࡰࡩࠧਨ")),
                      bstack1ll_opy_ (u"ࠦ࡭ࡵࡳࡵࡡ࡬ࡲ࡫ࡵࠢ਩"): get_host_info()
                  }
              }
              bstack1l111lll1_opy_ = bstack11lll111ll_opy_(cli.config, [bstack1ll_opy_ (u"ࠧࡧࡰࡪࡵࠥਪ"), bstack1ll_opy_ (u"ࠨࡥࡥࡵࡌࡲࡸࡺࡲࡶ࡯ࡨࡲࡹࡧࡴࡪࡱࡱࠦਫ"), bstack1ll_opy_ (u"ࠢࡢࡲ࡬ࠦਬ")], bstack11llll11ll_opy_)
              response = bstack1l1111l111_opy_(bstack1ll_opy_ (u"ࠣࡒࡒࡗ࡙ࠨਭ"), bstack1l111lll1_opy_, payload, config)
              if response.status_code >= 200 and response.status_code < 300:
                  logger.info(bstack1ll_opy_ (u"ࠤࡎࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹࠠࡴࡧࡱࡸࠥࡹࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡹࡵࠠࡼࡿࠥਮ").format(bstack11llll11ll_opy_))
              else:
                  logger.debug(bstack1ll_opy_ (u"ࠥࡏࡪࡿࠠ࡮ࡧࡷࡶ࡮ࡩࡳࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮ࠠࡴࡶࡤࡸࡺࡹࠠࡼࡿࠥਯ").format(response.status_code))
          except Exception as e:
              logger.debug(bstack1ll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡱࡨࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵ࠽ࠤࢀࢃࠢਰ").format(e))
      bstack111llll1ll_opy_()
  except Exception as e:
      logger.debug(bstack1ll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡱࡨࡤࡱࡥࡺࡡࡰࡩࡹࡸࡩࡤࡵ࠽ࠤࢀࢃࠢ਱").format(e))
def bstack111l1lll1_opy_(bstack11ll1lll1l_opy_=False):
  bstack11l1lll11l_opy_ = bstack1ll_opy_ (u"ࠨࠢਲ")
  global bstack11l1111l1_opy_
  global bstack1ll111ll1l_opy_
  global bstack1l11l11ll1_opy_
  global bstack1l1l1ll11_opy_
  global ROBOT_PYTHON_ERRORS
  global bstack1ll11ll1l1_opy_
  global CONFIG
  bstack1l1ll11l_opy_ = os.environ.get(bstack1ll_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨਲ਼"))
  if bstack1l1ll11l_opy_ not in [bstack1ll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ਴")]:
    bstack11l1lll11l_opy_ = bstack1l11l1ll11_opy_.bstack1111ll1111_opy_(EVENTS.bstack1l1l1l1ll_opy_)
  percy.shutdown()
  if bstack11l1111l1_opy_:
    logger.warning(bstack111l1l11ll_opy_.format(str(bstack11l1111l1_opy_)))
  else:
    try:
      bstack1111l1l1_opy_ = bstack1lll111l1l_opy_(bstack1ll_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨਵ"), logger)
      if bstack1111l1l1_opy_.get(bstack1ll_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨਸ਼")) and bstack1111l1l1_opy_.get(bstack1ll_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩ਷")).get(bstack1ll_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧਸ")):
        logger.warning(bstack111l1l11ll_opy_.format(str(bstack1111l1l1_opy_[bstack1ll_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫਹ")][bstack1ll_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩ਺")])))
    except Exception as e:
      logger.error(e)
  if cli.is_running() and bstack1l1ll11l_opy_ not in [bstack1ll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ਻")]:
    if _11llll1ll1_opy_ is not None:
      bstack11ll1lll1l_opy_ = _11llll1ll1_opy_
    else:
      bstack11ll1lll1l_opy_ = cli.is_running()
    bstack111l1lll11_opy_.invoke(Events.bstack1l1ll11ll_opy_)
  elif _11llll1ll1_opy_ is not None:
    bstack11ll1lll1l_opy_ = _11llll1ll1_opy_
  logger.info(bstack1l1111l1l_opy_)
  global bstack1ll1ll1ll1_opy_
  if bstack1ll1ll1ll1_opy_:
    bstack1ll1111l_opy_()
  try:
    with bstack111l1111_opy_:
      bstack1lll1l1111_opy_ = bstack1ll111ll1l_opy_.copy()
    for driver in bstack1lll1l1111_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1ll1l1111l_opy_)
  ROBOT_PYTHON_ERRORS = []
  if bstack1ll11ll1l1_opy_ == bstack1ll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ਼"):
    ROBOT_PYTHON_ERRORS = bstack1l111l1ll_opy_(bstack1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫ਽"))
  if bstack1ll11ll1l1_opy_ == bstack1ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫਾ") and len(bstack1l1l1ll11_opy_) == 0:
    bstack1l1l1ll11_opy_ = bstack1l111l1ll_opy_(bstack1ll_opy_ (u"ࠬࡶࡷࡠࡲࡼࡸࡪࡹࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪਿ"))
    if len(bstack1l1l1ll11_opy_) == 0:
      bstack1l1l1ll11_opy_ = bstack1l111l1ll_opy_(bstack1ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡰࡱࡲࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬੀ"))
  bstack11l11llll_opy_ = bstack1ll_opy_ (u"ࠧࠨੁ")
  if len(bstack1l11l11ll1_opy_) > 0:
    bstack11l11llll_opy_ = bstack111l1l1lll_opy_(bstack1l11l11ll1_opy_)
  elif len(bstack1l1l1ll11_opy_) > 0:
    bstack11l11llll_opy_ = bstack111l1l1lll_opy_(bstack1l1l1ll11_opy_)
  elif len(ROBOT_PYTHON_ERRORS) > 0:
    bstack11l11llll_opy_ = bstack111l1l1lll_opy_(ROBOT_PYTHON_ERRORS)
  elif len(bstack1l1ll1ll1_opy_) > 0:
    bstack11l11llll_opy_ = bstack111l1l1lll_opy_(bstack1l1ll1ll1_opy_)
  if bstack1l1ll11l_opy_ not in [bstack1ll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩੂ")]:
    def bstack1llllll1lll_opy_():
      try:
        if bstack1l1ll11l_opy_ in [bstack1ll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ੃"), bstack1ll_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ੄")]:
          bstack11lll1l11l_opy_()
      except Exception as e:
        logger.debug(bstack1ll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡪࡰࡤࡰࡤ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧ੅").format(e))
    def bstack1lll1l11l_opy_():
      try:
        if bool(bstack11l11llll_opy_):
          bstack1l1l11111l_opy_(bstack11l11llll_opy_, bstack11ll1lll1l_opy_=bstack11ll1lll1l_opy_)
        else:
          bstack1l1l11111l_opy_(bstack11ll1lll1l_opy_=bstack11ll1lll1l_opy_)
      except Exception as e:
        logger.debug(bstack1ll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥ࡫ࡶࡦࡰࡷ࠾ࠥࢁࡽࠣ੆").format(e))
    def bstack111l1ll111_opy_():
      try:
        logger_utils.bstack111l11l1_opy_(CONFIG)
      except Exception as e:
        logger.debug(bstack1ll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡹࡥ࡯ࡦ࡬ࡲ࡬ࠦ࡬ࡰࡩࡶ࠾ࠥࢁࡽࠣੇ").format(e))
    bstack1l1ll1l1_opy_ = threading.Thread(target=bstack1llllll1lll_opy_)
    bstack11l1ll1l1_opy_ = threading.Thread(target=bstack1lll1l11l_opy_)
    bstack1lllll1ll1l_opy_ = threading.Thread(target=bstack111l1ll111_opy_)
    threads = [bstack1l1ll1l1_opy_, bstack11l1ll1l1_opy_, bstack1lllll1ll1l_opy_]
    for thread in threads:
      try:
        thread.start()
      except Exception as e:
        logger.debug(bstack1ll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡳࡵࡣࡵࡸ࡮ࡴࡧࠡࡶ࡫ࡶࡪࡧࡤࠡࡽࢀ࠾ࠥࢁࡽࠣੈ").format(thread.name, e))
    for thread in threads:
      try:
        thread.join()
      except Exception as e:
        logger.debug(bstack1ll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠ࡫ࡱ࡬ࡲ࡮ࡴࡧࠡࡶ࡫ࡶࡪࡧࡤࠡࡽࢀ࠾ࠥࢁࡽࠣ੉").format(thread.name, e))
    bstack1l1l11l1ll_opy_(bstack11l111ll1l_opy_, logger)
    bstack1l1l11l1ll_opy_(os.path.join(os.getcwd(), bstack1ll_opy_ (u"ࠩ࡯ࡳ࡬࠭੊"), bstack1ll_opy_ (u"ࠪ࡯ࡪࡿ࠭࡮ࡧࡷࡶ࡮ࡩࡳ࠯࡬ࡶࡳࡳ࠭ੋ")), logger)
  if bstack1l1ll11l_opy_ not in [bstack1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬੌ")]:
    bstack1l11l1ll11_opy_.end(EVENTS.bstack1l1l1l1ll_opy_.value, bstack11l1lll11l_opy_ + bstack1ll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸ੍ࠧ"), bstack11l1lll11l_opy_ + bstack1ll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ੎"), status=True, failure=None, test_name=None)
    bstack11lll111l_opy_()
    logger_utils.bstack11ll1lll1_opy_()
    logging.shutdown()
  if len(ROBOT_PYTHON_ERRORS) > 0:
    sys.exit(len(ROBOT_PYTHON_ERRORS))
def bstack1l11lll1_opy_(bstack111ll111l1_opy_, frame):
  global global_config
  logger.error(bstack11111l11ll_opy_)
  global_config.bstack11l11l11ll_opy_(bstack1ll_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡏࡱࠪ੏"), bstack111ll111l1_opy_)
  if hasattr(signal, bstack1ll_opy_ (u"ࠨࡕ࡬࡫ࡳࡧ࡬ࡴࠩ੐")):
    global_config.bstack11l11l11ll_opy_(bstack1ll_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩੑ"), signal.Signals(bstack111ll111l1_opy_).name)
  else:
    global_config.bstack11l11l11ll_opy_(bstack1ll_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪ੒"), bstack1ll_opy_ (u"ࠫࡘࡏࡇࡖࡐࡎࡒࡔ࡝ࡎࠨ੓"))
  bstack11ll1lll1l_opy_ = cli.is_running()
  if bstack11ll1lll1l_opy_:
    bstack111l1lll11_opy_.invoke(Events.bstack1l1ll11ll_opy_)
  bstack1l1ll11l_opy_ = os.environ.get(bstack1ll_opy_ (u"ࠬࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉ࠭੔"))
  if bstack1l1ll11l_opy_ == bstack1ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭੕") and not cli.is_enabled(CONFIG):
    TestHubHandler.stop(global_config.get_property(bstack1ll_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡔ࡫ࡪࡲࡦࡲࠧ੖")))
  bstack111l1lll1_opy_(bstack11ll1lll1l_opy_)
  sys.exit(1)
def bstack1ll11l11ll_opy_(err):
  logger.critical(bstack1llll1l11l_opy_.format(str(err)))
  bstack1l1l11111l_opy_(bstack1llll1l11l_opy_.format(str(err)), True)
  atexit.unregister(bstack111l1lll1_opy_)
  bstack11lll1l11l_opy_()
  sys.exit(1)
def bstack11111lll1l_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1l1l11111l_opy_(message, True)
  atexit.unregister(bstack111l1lll1_opy_)
  bstack11lll1l11l_opy_()
  sys.exit(1)
def bstack1111l11l_opy_():
  global CONFIG
  global bstack1ll1lllll_opy_
  global bstack11ll11lll_opy_
  global BROWSERSTACK_AUTOMATION
  CONFIG = bstack11l111111l_opy_()
  load_dotenv(CONFIG.get(bstack1ll_opy_ (u"ࠨࡧࡱࡺࡋ࡯࡬ࡦࠩ੗")))
  bstack111l1l1l11_opy_()
  bstack1l1l11ll_opy_()
  CONFIG = bstack1l11111ll1_opy_(CONFIG)
  update(CONFIG, bstack11ll11lll_opy_)
  update(CONFIG, bstack1ll1lllll_opy_)
  if not cli.is_enabled(CONFIG):
    CONFIG = bstack1ll1ll1l_opy_(CONFIG)
  BROWSERSTACK_AUTOMATION = bstack1lll1111ll_opy_(CONFIG)
  os.environ[bstack1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬ੘")] = BROWSERSTACK_AUTOMATION.__str__().lower()
  global_config.bstack11l11l11ll_opy_(bstack1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫਖ਼"), BROWSERSTACK_AUTOMATION)
  if (bstack1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧਗ਼") in CONFIG and bstack1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨਜ਼") in bstack1ll1lllll_opy_) or (
          bstack1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩੜ") in CONFIG and bstack1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ੝") not in bstack11ll11lll_opy_):
    if os.getenv(bstack1ll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬਫ਼")):
      CONFIG[bstack1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ੟")] = os.getenv(bstack1ll_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧ੠"))
    else:
      if not CONFIG.get(bstack1ll_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠢ੡"), bstack1ll_opy_ (u"ࠧࠨ੢")) in bstack1l1ll11l1l_opy_:
        bstack11ll11l11l_opy_()
  elif (bstack1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ੣") not in CONFIG and bstack1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ੤") in CONFIG) or (
          bstack1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ੥") in bstack11ll11lll_opy_ and bstack1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ੦") not in bstack1ll1lllll_opy_):
    del (CONFIG[bstack1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ੧")])
  if bstack1l1ll11l1_opy_(CONFIG):
    bstack1ll11l11ll_opy_(bstack11lllllll_opy_)
  Config.bstack1l111l1111_opy_().bstack11l11l11ll_opy_(bstack1ll_opy_ (u"ࠦࡺࡹࡥࡳࡐࡤࡱࡪࠨ੨"), CONFIG[bstack1ll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ੩")])
  bstack11l1l11l1l_opy_()
  bstack1llllllll_opy_()
  if bstack11l1llllll_opy_ and not CONFIG.get(bstack1ll_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠤ੪"), bstack1ll_opy_ (u"ࠢࠣ੫")) in bstack1l1ll11l1l_opy_:
    CONFIG[bstack1ll_opy_ (u"ࠨࡣࡳࡴࠬ੬")] = bstack11l111l1_opy_(CONFIG)
    logger.info(bstack1lll11111_opy_.format(CONFIG[bstack1ll_opy_ (u"ࠩࡤࡴࡵ࠭੭")]))
  if not BROWSERSTACK_AUTOMATION:
    CONFIG[bstack1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭੮")] = [{}]
def bstack11l1l1l1ll_opy_(config, bstack1llll1111_opy_):
  global CONFIG
  global bstack11l1llllll_opy_
  CONFIG = config
  bstack11l1llllll_opy_ = bstack1llll1111_opy_
def bstack1llllllll_opy_():
  global CONFIG
  global bstack11l1llllll_opy_
  if bstack1ll_opy_ (u"ࠫࡦࡶࡰࠨ੯") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack11111lll1l_opy_(e, bstack11lllll1l1_opy_)
    bstack11l1llllll_opy_ = True
    global_config.bstack11l11l11ll_opy_(bstack1ll_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫੰ"), True)
def bstack11l111l1_opy_(config):
  bstack11l1l1l1l1_opy_ = bstack1ll_opy_ (u"࠭ࠧੱ")
  app = config[bstack1ll_opy_ (u"ࠧࡢࡲࡳࠫੲ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack11lll1lll_opy_:
      if os.path.exists(app):
        bstack11l1l1l1l1_opy_ = bstack1lll1ll111_opy_(config, app)
      elif bstack1l1lll1ll_opy_(app):
        bstack11l1l1l1l1_opy_ = app
      else:
        bstack1ll11l11ll_opy_(bstack1l1lll11_opy_.format(app))
    else:
      if bstack1l1lll1ll_opy_(app):
        bstack11l1l1l1l1_opy_ = app
      elif os.path.exists(app):
        bstack11l1l1l1l1_opy_ = bstack1lll1ll111_opy_(app)
      else:
        bstack1ll11l11ll_opy_(bstack1ll1l111_opy_)
  else:
    if len(app) > 2:
      bstack1ll11l11ll_opy_(bstack11lll11l1l_opy_)
    elif len(app) == 2:
      if bstack1ll_opy_ (u"ࠨࡲࡤࡸ࡭࠭ੳ") in app and bstack1ll_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬੴ") in app:
        if os.path.exists(app[bstack1ll_opy_ (u"ࠪࡴࡦࡺࡨࠨੵ")]):
          bstack11l1l1l1l1_opy_ = bstack1lll1ll111_opy_(config, app[bstack1ll_opy_ (u"ࠫࡵࡧࡴࡩࠩ੶")], app[bstack1ll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨ੷")])
        else:
          bstack1ll11l11ll_opy_(bstack1l1lll11_opy_.format(app))
      else:
        bstack1ll11l11ll_opy_(bstack11lll11l1l_opy_)
    else:
      for key in app:
        if key in bstack1111llll1_opy_:
          if key == bstack1ll_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ੸"):
            if os.path.exists(app[key]):
              bstack11l1l1l1l1_opy_ = bstack1lll1ll111_opy_(config, app[key])
            else:
              bstack1ll11l11ll_opy_(bstack1l1lll11_opy_.format(app))
          else:
            bstack11l1l1l1l1_opy_ = app[key]
        else:
          bstack1ll11l11ll_opy_(bstack1l1111lll1_opy_)
  return bstack11l1l1l1l1_opy_
def bstack1l1lll1ll_opy_(bstack11l1l1l1l1_opy_):
  import re
  bstack1ll1l11111_opy_ = re.compile(bstack1ll_opy_ (u"ࡲࠣࡠ࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯ࠪࠢ੹"))
  bstack111llll11l_opy_ = re.compile(bstack1ll_opy_ (u"ࡳࠤࡡ࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰࠯࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭ࠨࠧ੺"))
  if bstack1ll_opy_ (u"ࠩࡥࡷ࠿࠵࠯ࠨ੻") in bstack11l1l1l1l1_opy_ or re.fullmatch(bstack1ll1l11111_opy_, bstack11l1l1l1l1_opy_) or re.fullmatch(bstack111llll11l_opy_, bstack11l1l1l1l1_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack11ll111l11_opy_, stage=STAGE.bstack11llll111l_opy_, bstack111l11111_opy_=SESSION_NAME)
def bstack1lll1ll111_opy_(config, path, bstack11l1lllll1_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1ll_opy_ (u"ࠪࡶࡧ࠭੼")).read()).hexdigest()
  bstack11ll11lll1_opy_ = bstack11l11l111_opy_(md5_hash)
  bstack11l1l1l1l1_opy_ = None
  if bstack11ll11lll1_opy_:
    logger.info(bstack11l1l11l11_opy_.format(bstack11ll11lll1_opy_, md5_hash))
    return bstack11ll11lll1_opy_
  bstack1l1111ll_opy_ = datetime.datetime.now()
  multipart_data = MultipartEncoder(
    fields={
      bstack1ll_opy_ (u"ࠫ࡫࡯࡬ࡦࠩ੽"): (os.path.basename(path), open(os.path.abspath(path), bstack1ll_opy_ (u"ࠬࡸࡢࠨ੾")), bstack1ll_opy_ (u"࠭ࡴࡦࡺࡷ࠳ࡵࡲࡡࡪࡰࠪ੿")),
      bstack1ll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪ઀"): bstack11l1lllll1_opy_
    }
  )
  response = requests.post(bstack1l1l1ll1_opy_, data=multipart_data,
                           headers={bstack1ll_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧઁ"): multipart_data.content_type},
                           auth=(config[bstack1ll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫં")], config[bstack1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ઃ")]))
  try:
    res = json.loads(response.text)
    bstack11l1l1l1l1_opy_ = res[bstack1ll_opy_ (u"ࠫࡦࡶࡰࡠࡷࡵࡰࠬ઄")]
    logger.info(bstack1l111ll1l_opy_.format(bstack11l1l1l1l1_opy_))
    bstack11l111l1l1_opy_(md5_hash, bstack11l1l1l1l1_opy_)
    cli.bstack1lll11ll11_opy_(bstack1ll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽ࡹࡵࡲ࡯ࡢࡦࡢࡥࡵࡶࠢઅ"), datetime.datetime.now() - bstack1l1111ll_opy_)
  except ValueError as err:
    bstack1ll11l11ll_opy_(bstack1lllll11l_opy_.format(str(err)))
  return bstack11l1l1l1l1_opy_
def bstack11l1l11l1l_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack1111l1l1ll_opy_
  bstack1lll1lll1_opy_ = 1
  bstack11l1l11lll_opy_ = 1
  if bstack1ll_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭આ") in CONFIG:
    bstack11l1l11lll_opy_ = CONFIG[bstack1ll_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧઇ")]
  else:
    bstack11l1l11lll_opy_ = bstack1lllll1ll1_opy_(framework_name, args) or 1
  if bstack1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫઈ") in CONFIG:
    bstack1lll1lll1_opy_ = len(CONFIG[bstack1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬઉ")])
  bstack1111l1l1ll_opy_ = int(bstack11l1l11lll_opy_) * int(bstack1lll1lll1_opy_)
def bstack1lllll1ll1_opy_(framework_name, args):
  if framework_name == bstack11l1ll11_opy_ and args and bstack1ll_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨઊ") in args:
      bstack1llll11l_opy_ = args.index(bstack1ll_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩઋ"))
      return int(args[bstack1llll11l_opy_ + 1]) or 1
  return 1
def bstack11l11l111_opy_(md5_hash):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1ll_opy_ (u"ࠬ࡬ࡩ࡭ࡧ࡯ࡳࡨࡱࠠ࡯ࡱࡷࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠬࠡࡷࡶ࡭ࡳ࡭ࠠࡣࡣࡶ࡭ࡨࠦࡦࡪ࡮ࡨࠤࡴࡶࡥࡳࡣࡷ࡭ࡴࡴࡳࠨઌ"))
    bstack1lll1llll1_opy_ = os.path.join(os.path.expanduser(bstack1ll_opy_ (u"࠭ࡾࠨઍ")), bstack1ll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ઎"), bstack1ll_opy_ (u"ࠨࡣࡳࡴ࡚ࡶ࡬ࡰࡣࡧࡑࡉ࠻ࡈࡢࡵ࡫࠲࡯ࡹ࡯࡯ࠩએ"))
    if os.path.exists(bstack1lll1llll1_opy_):
      try:
        bstack11l1ll11ll_opy_ = json.load(open(bstack1lll1llll1_opy_, bstack1ll_opy_ (u"ࠩࡵࡦࠬઐ")))
        if md5_hash in bstack11l1ll11ll_opy_:
          bstack11111l111l_opy_ = bstack11l1ll11ll_opy_[md5_hash]
          bstack1l11ll111l_opy_ = datetime.datetime.now()
          bstack1llllll1ll1_opy_ = datetime.datetime.strptime(bstack11111l111l_opy_[bstack1ll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ઑ")], bstack1ll_opy_ (u"ࠫࠪࡪ࠯ࠦ࡯࠲ࠩ࡞ࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨ઒"))
          if (bstack1l11ll111l_opy_ - bstack1llllll1ll1_opy_).days > 30:
            return None
          elif version.parse(str(__version__)) > version.parse(bstack11111l111l_opy_[bstack1ll_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪઓ")]):
            return None
          return bstack11111l111l_opy_[bstack1ll_opy_ (u"࠭ࡩࡥࠩઔ")]
      except Exception as e:
        logger.debug(bstack1ll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡲࡦࡣࡧ࡭ࡳ࡭ࠠࡎࡆ࠸ࠤ࡭ࡧࡳࡩࠢࡩ࡭ࡱ࡫࠺ࠡࡽࢀࠫક").format(str(e)))
    return None
  bstack1lll1llll1_opy_ = os.path.join(os.path.expanduser(bstack1ll_opy_ (u"ࠨࢀࠪખ")), bstack1ll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩગ"), bstack1ll_opy_ (u"ࠪࡥࡵࡶࡕࡱ࡮ࡲࡥࡩࡓࡄ࠶ࡊࡤࡷ࡭࠴ࡪࡴࡱࡱࠫઘ"))
  lock_file = bstack1lll1llll1_opy_ + bstack1ll_opy_ (u"ࠫ࠳ࡲ࡯ࡤ࡭ࠪઙ")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack1lll1llll1_opy_):
        with open(bstack1lll1llll1_opy_, bstack1ll_opy_ (u"ࠬࡸࠧચ")) as f:
          content = f.read().strip()
          if content:
            bstack11l1ll11ll_opy_ = json.loads(content)
            if md5_hash in bstack11l1ll11ll_opy_:
              bstack11111l111l_opy_ = bstack11l1ll11ll_opy_[md5_hash]
              bstack1l11ll111l_opy_ = datetime.datetime.now()
              bstack1llllll1ll1_opy_ = datetime.datetime.strptime(bstack11111l111l_opy_[bstack1ll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩછ")], bstack1ll_opy_ (u"ࠧࠦࡦ࠲ࠩࡲ࠵࡚ࠥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫજ"))
              if (bstack1l11ll111l_opy_ - bstack1llllll1ll1_opy_).days > 30:
                return None
              elif version.parse(str(__version__)) > version.parse(bstack11111l111l_opy_[bstack1ll_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ઝ")]):
                return None
              return bstack11111l111l_opy_[bstack1ll_opy_ (u"ࠩ࡬ࡨࠬઞ")]
      return None
  except Exception as e:
    logger.debug(bstack1ll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡺ࡭ࡹ࡮ࠠࡧ࡫࡯ࡩࠥࡲ࡯ࡤ࡭࡬ࡲ࡬ࠦࡦࡰࡴࠣࡑࡉ࠻ࠠࡩࡣࡶ࡬࠿ࠦࡻࡾࠩટ").format(str(e)))
    return None
def bstack11l111l1l1_opy_(md5_hash, bstack11l1l1l1l1_opy_):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1ll_opy_ (u"ࠫ࡫࡯࡬ࡦ࡮ࡲࡧࡰࠦ࡮ࡰࡶࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪ࠲ࠠࡶࡵ࡬ࡲ࡬ࠦࡢࡢࡵ࡬ࡧࠥ࡬ࡩ࡭ࡧࠣࡳࡵ࡫ࡲࡢࡶ࡬ࡳࡳࡹࠧઠ"))
    bstack1lllll11ll_opy_ = os.path.join(os.path.expanduser(bstack1ll_opy_ (u"ࠬࢄࠧડ")), bstack1ll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ઢ"))
    if not os.path.exists(bstack1lllll11ll_opy_):
      os.makedirs(bstack1lllll11ll_opy_)
    bstack1lll1llll1_opy_ = os.path.join(os.path.expanduser(bstack1ll_opy_ (u"ࠧࡿࠩણ")), bstack1ll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨત"), bstack1ll_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪથ"))
    bstack1l1ll1l1l_opy_ = {
      bstack1ll_opy_ (u"ࠪ࡭ࡩ࠭દ"): bstack11l1l1l1l1_opy_,
      bstack1ll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧધ"): datetime.datetime.strftime(datetime.datetime.now(), bstack1ll_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩન")),
      bstack1ll_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ઩"): str(__version__)
    }
    try:
      bstack11l1ll11ll_opy_ = {}
      if os.path.exists(bstack1lll1llll1_opy_):
        bstack11l1ll11ll_opy_ = json.load(open(bstack1lll1llll1_opy_, bstack1ll_opy_ (u"ࠧࡳࡤࠪપ")))
      bstack11l1ll11ll_opy_[md5_hash] = bstack1l1ll1l1l_opy_
      with open(bstack1lll1llll1_opy_, bstack1ll_opy_ (u"ࠣࡹ࠮ࠦફ")) as outfile:
        json.dump(bstack11l1ll11ll_opy_, outfile)
    except Exception as e:
      logger.debug(bstack1ll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡷࡳࡨࡦࡺࡩ࡯ࡩࠣࡑࡉ࠻ࠠࡩࡣࡶ࡬ࠥ࡬ࡩ࡭ࡧ࠽ࠤࢀࢃࠧબ").format(str(e)))
    return
  bstack1lllll11ll_opy_ = os.path.join(os.path.expanduser(bstack1ll_opy_ (u"ࠪࢂࠬભ")), bstack1ll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫમ"))
  if not os.path.exists(bstack1lllll11ll_opy_):
    os.makedirs(bstack1lllll11ll_opy_)
  bstack1lll1llll1_opy_ = os.path.join(os.path.expanduser(bstack1ll_opy_ (u"ࠬࢄࠧય")), bstack1ll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ર"), bstack1ll_opy_ (u"ࠧࡢࡲࡳ࡙ࡵࡲ࡯ࡢࡦࡐࡈ࠺ࡎࡡࡴࡪ࠱࡮ࡸࡵ࡮ࠨ઱"))
  lock_file = bstack1lll1llll1_opy_ + bstack1ll_opy_ (u"ࠨ࠰࡯ࡳࡨࡱࠧલ")
  bstack1l1ll1l1l_opy_ = {
    bstack1ll_opy_ (u"ࠩ࡬ࡨࠬળ"): bstack11l1l1l1l1_opy_,
    bstack1ll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭઴"): datetime.datetime.strftime(datetime.datetime.now(), bstack1ll_opy_ (u"ࠫࠪࡪ࠯ࠦ࡯࠲ࠩ࡞ࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨવ")),
    bstack1ll_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪશ"): str(__version__)
  }
  try:
    with FileLock(lock_file, timeout=10):
      bstack11l1ll11ll_opy_ = {}
      if os.path.exists(bstack1lll1llll1_opy_):
        with open(bstack1lll1llll1_opy_, bstack1ll_opy_ (u"࠭ࡲࠨષ")) as f:
          content = f.read().strip()
          if content:
            bstack11l1ll11ll_opy_ = json.loads(content)
      bstack11l1ll11ll_opy_[md5_hash] = bstack1l1ll1l1l_opy_
      with open(bstack1lll1llll1_opy_, bstack1ll_opy_ (u"ࠢࡸࠤસ")) as outfile:
        json.dump(bstack11l1ll11ll_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1ll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡸ࡫ࡷ࡬ࠥ࡬ࡩ࡭ࡧࠣࡰࡴࡩ࡫ࡪࡰࡪࠤ࡫ࡵࡲࠡࡏࡇ࠹ࠥ࡮ࡡࡴࡪࠣࡹࡵࡪࡡࡵࡧ࠽ࠤࢀࢃࠧહ").format(str(e)))
def bstack111lll11l_opy_(self):
  return
def bstack1111l1ll1l_opy_(self):
  return
def bstack1llll1l1l1_opy_():
  global bstack1ll1111ll_opy_
  bstack1ll1111ll_opy_ = True
def bstack1l111lll_opy_(self):
  global FRAMEWORK_NAME
  global bstack11ll11l1_opy_
  global bstack1111ll111l_opy_
  bstack1lll1lll11_opy_ = bstack1l11l1ll11_opy_.bstack1111ll1111_opy_(EVENTS.bstack1111111lll_opy_)
  try:
    if bstack1ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ઺") in FRAMEWORK_NAME and self.session_id != None and bstack1llll1lll_opy_(threading.current_thread(), bstack1ll_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧ઻"), bstack1ll_opy_ (u"઼ࠫࠬ")) != bstack1ll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ઽ"):
      bstack1l11lll1ll_opy_ = bstack1ll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ા") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧિ")
      if bstack1l11lll1ll_opy_ == bstack1ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨી"):
        bstack1ll11l1l1l_opy_(logger)
      if self != None:
        bstack1l111l1l1l_opy_(self, bstack1l11lll1ll_opy_, bstack1ll_opy_ (u"ࠩ࠯ࠤࠬુ").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack1ll_opy_ (u"ࠪࠫૂ")
    if bstack1ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫૃ") in FRAMEWORK_NAME and getattr(threading.current_thread(), bstack1ll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫૄ"), None):
      bstack1l11ll1l11_opy_.bstack1l11111l1l_opy_(self, bstack1l1l1l111l_opy_, logger, wait=True)
    if bstack1ll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ૅ") in FRAMEWORK_NAME:
      bstack1l11lll1l_opy_.bstack11111lllll_opy_(self)
    bstack1l11l1ll11_opy_.end(EVENTS.bstack1111111lll_opy_.value, bstack1lll1lll11_opy_ + bstack1ll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ૆"), bstack1lll1lll11_opy_ + bstack1ll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨે"), status=True, failure=None, test_name=None)
  except Exception as e:
    logger.debug(bstack1ll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࠥૈ") + str(e))
    bstack1l11l1ll11_opy_.end(EVENTS.bstack1111111lll_opy_.value, bstack1lll1lll11_opy_ + bstack1ll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥૉ"), bstack1lll1lll11_opy_ + bstack1ll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ૊"), status=False, failure=str(e), test_name=None)
  bstack1111ll111l_opy_(self)
  self.session_id = None
def bstack1ll111l1_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack111l11ll1l_opy_
    global FRAMEWORK_NAME
    command_executor = kwargs.get(bstack1ll_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠨો"), bstack1ll_opy_ (u"࠭ࠧૌ"))
    bstack1ll11ll111_opy_ = False
    if type(command_executor) == str and bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯્ࠪ") in command_executor:
      bstack1ll11ll111_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫ૎") in str(getattr(command_executor, bstack1ll_opy_ (u"ࠩࡢࡹࡷࡲࠧ૏"), bstack1ll_opy_ (u"ࠪࠫૐ"))):
      bstack1ll11ll111_opy_ = True
    else:
      kwargs = a11y.bstack1l1ll11ll1_opy_(bstack11l1lll1ll_opy_=kwargs, config=CONFIG)
      return bstack11ll1111l_opy_(self, *args, **kwargs)
    if bstack1ll11ll111_opy_:
      bstack111ll1l1ll_opy_ = TestHubUtils.bstack11l11l11l_opy_(CONFIG, FRAMEWORK_NAME)
      if kwargs.get(bstack1ll_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ૑")):
        kwargs[bstack1ll_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭૒")] = bstack111l11ll1l_opy_(kwargs[bstack1ll_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧ૓")], FRAMEWORK_NAME, CONFIG, bstack111ll1l1ll_opy_)
      elif kwargs.get(bstack1ll_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ૔")):
        kwargs[bstack1ll_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ૕")] = bstack111l11ll1l_opy_(kwargs[bstack1ll_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ૖")], FRAMEWORK_NAME, CONFIG, bstack111ll1l1ll_opy_)
  except Exception as e:
    logger.error(bstack1ll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡘࡊࡋࠡࡥࡤࡴࡸࡀࠠࡼࡿࠥ૗").format(str(e)))
  return bstack11ll1111l_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack111111ll_opy_, stage=STAGE.bstack11llll111l_opy_, bstack111l11111_opy_=SESSION_NAME)
def bstack1llll11l1l_opy_(self, command_executor=bstack1ll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳࠶࠸࠷࠯࠲࠱࠴࠳࠷࠺࠵࠶࠷࠸ࠧ૘"), *args, **kwargs):
  global bstack11ll11l1_opy_
  global bstack1ll111ll1l_opy_
  bstack1lllllll1_opy_ = bstack1ll111l1_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack111l111ll1_opy_.on():
    return bstack1lllllll1_opy_
  try:
    if isinstance(command_executor, (str, bytes)):
      bstack1111ll111_opy_ = str(command_executor)
    else:
      bstack1111ll111_opy_ = str(
        getattr(command_executor, bstack1ll_opy_ (u"ࠬࡥࡵࡳ࡮ࠪ૙"), None)
        or getattr(getattr(command_executor, bstack1ll_opy_ (u"࠭࡟ࡤ࡮࡬ࡩࡳࡺ࡟ࡤࡱࡱࡪ࡮࡭ࠧ૚"), None), bstack1ll_opy_ (u"ࠧࡳࡧࡰࡳࡹ࡫࡟ࡴࡧࡵࡺࡪࡸ࡟ࡢࡦࡧࡶࠬ૛"), None)
        or bstack1ll_opy_ (u"ࠨࠩ૜")
      )
    logger.debug(bstack1ll_opy_ (u"ࠩࡋࡹࡧࠦࡕࡓࡎࠣ࡭ࡸࠦ࠭ࠡࡽࢀࠫ૝").format(bstack1111ll111_opy_.split(bstack1ll_opy_ (u"ࠪࡄࠬ૞"))[-1] if bstack1ll_opy_ (u"ࠫࡅ࠭૟") in bstack1111ll111_opy_ else bstack1111ll111_opy_))
    if bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨૠ") in bstack1111ll111_opy_:
      global_config.bstack11l11l11ll_opy_(bstack1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧૡ"), True)
  except Exception as e:
    logger.error(bstack1ll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡩࡨࡦࡥ࡮࡭ࡳ࡭ࠠࡤࡱࡰࡱࡦࡴࡤࠡࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧૢ").format(str(e)))
    pass
  if (isinstance(command_executor, str) and bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫૣ") in command_executor):
    global_config.bstack11l11l11ll_opy_(bstack1ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪ૤"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1111l1ll11_opy_ = getattr(threading.current_thread(), bstack1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡗࡩࡸࡺࡍࡦࡶࡤࠫ૥"), None)
  bstack11ll1l11l_opy_ = {}
  if self.capabilities is not None:
    bstack11ll1l11l_opy_[bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧࠪ૦")] = self.capabilities.get(bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ૧"))
    bstack11ll1l11l_opy_[bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ૨")] = self.capabilities.get(bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ૩"))
    bstack11ll1l11l_opy_[bstack1ll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡠࡱࡳࡸ࡮ࡵ࡮ࡴࠩ૪")] = self.capabilities.get(bstack1ll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ૫"))
  if CONFIG.get(bstack1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ૬"), False) and a11y.bstack11ll11ll1_opy_(bstack11ll1l11l_opy_):
    threading.current_thread().a11yPlatform = True
  if bstack1ll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ૭") in FRAMEWORK_NAME or bstack1ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ૮") in FRAMEWORK_NAME:
    TestHubHandler.send_cbt_info(self)
  if bstack1ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭૯") in FRAMEWORK_NAME and bstack1111l1ll11_opy_ and bstack1111l1ll11_opy_.get(bstack1ll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ૰"), bstack1ll_opy_ (u"ࠨࠩ૱")) == bstack1ll_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ૲"):
    TestHubHandler.send_cbt_info(self)
  bstack11ll11l1_opy_ = self.session_id
  with bstack111l1111_opy_:
    bstack1ll111ll1l_opy_.append(self)
  return bstack1lllllll1_opy_
def bstack1ll1111ll1_opy_(args):
  return bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵࠫ૳") in str(args)
def bstack11l11l1l11_opy_(self, driver_command, *args, **kwargs):
  global bstack1l11l1l11_opy_
  global bstack1l111ll11l_opy_
  bstack1ll1l11l_opy_ = bstack1llll1lll_opy_(threading.current_thread(), bstack1ll_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ૴"), None) and bstack1llll1lll_opy_(
          threading.current_thread(), bstack1ll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ૵"), None)
  bstack11ll11ll1l_opy_ = bstack1llll1lll_opy_(threading.current_thread(), bstack1ll_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭૶"), None) and bstack1llll1lll_opy_(
          threading.current_thread(), bstack1ll_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ૷"), None)
  bstack11ll1ll1_opy_ = getattr(self, bstack1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ૸"), None) != None and getattr(self, bstack1ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩૹ"), None) == True
  bstack111111llll_opy_ = str(FRAMEWORK_NAME).lower()
  bstack1lll11lll1_opy_ = not bstack1l111ll11l_opy_ and bstack1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪૺ") in CONFIG and CONFIG[bstack1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫૻ")] == True and accessibility_scripts.bstack1l1llllll_opy_(driver_command) and (bstack11ll1ll1_opy_ or bstack1ll1l11l_opy_ or bstack11ll11ll1l_opy_) and not bstack1ll1111ll1_opy_(args)
  if bstack1ll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨ࠭ૼ") in bstack111111llll_opy_:
    bstack11111111l_opy_ = a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX)
    bstack1lll11lll1_opy_ =  not bstack1l111ll11l_opy_ and bstack11111111l_opy_ and accessibility_scripts.bstack1l1llllll_opy_(driver_command) and (bstack11ll1ll1_opy_ or bstack1ll1l11l_opy_ or bstack11ll11ll1l_opy_) and not bstack1ll1111ll1_opy_(args)
  if bstack1lll11lll1_opy_:
    try:
      bstack1l111ll11l_opy_ = True
      logger.debug(bstack1ll_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡨࡲࡶࠥࢁࡽࠨ૽").format(driver_command))
      bstack1ll1111111_opy_ = perform_scan(self, driver_command=driver_command)
      logger.debug(bstack1ll1111111_opy_)
      try:
        log_data = {
          bstack1ll_opy_ (u"ࠢࡳࡧࡴࡹࡪࡹࡴࠣ૾"): {
            bstack1ll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤ૿"): bstack1ll_opy_ (u"ࠤࡄ࠵࠶࡟࡟ࡔࡅࡄࡒࠧ଀"),
            bstack1ll_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡧࡷࡩࡷࡹࠢଁ"): [
              {
                bstack1ll_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦଂ"): driver_command
              }
            ]
          },
          bstack1ll_opy_ (u"ࠧࡸࡥࡴࡲࡲࡲࡸ࡫ࠢଃ"): {
            bstack1ll_opy_ (u"ࠨࡢࡰࡦࡼࠦ଄"): {
              bstack1ll_opy_ (u"ࠢ࡮ࡵࡪࠦଅ"): bstack1ll1111111_opy_.get(bstack1ll_opy_ (u"ࠣ࡯ࡶ࡫ࠧଆ"), bstack1ll_opy_ (u"ࠤࠥଇ")) if isinstance(bstack1ll1111111_opy_, dict) else bstack1ll_opy_ (u"ࠥࠦଈ"),
              bstack1ll_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧଉ"): bstack1ll1111111_opy_.get(bstack1ll_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨଊ"), True) if isinstance(bstack1ll1111111_opy_, dict) else True
            }
          }
        }
        logger.debug(bstack1ll_opy_ (u"࠭ࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡤࡣࡱࠤࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡ࡮ࡲ࡫ࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠧଋ").format(log_data))
        automation_logger.info(json.dumps(log_data, separators=(bstack1ll_opy_ (u"ࠧ࠭ࠩଌ"), bstack1ll_opy_ (u"ࠨ࠼ࠪ଍"))))
      except Exception as bstack11111111_opy_:
        logger.debug(bstack1ll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡲ࡯ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡧࡦࡴࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠩ଎").format(str(bstack11111111_opy_)))
    except Exception as err:
      logger.debug(bstack1ll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡦࡴࡩࡳࡷࡳࠠࡴࡥࡤࡲࠥࢁࡽࠨଏ").format(str(err)))
    bstack1l111ll11l_opy_ = False
  response = bstack1l11l1l11_opy_(self, driver_command, *args, **kwargs)
  bstack1lllll1111_opy_ = (
    (bstack1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪଐ") in bstack111111llll_opy_ or bstack1ll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ଑") in bstack111111llll_opy_) and bstack111l111ll1_opy_.on()
  ) or (bstack1ll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡧࡦࡰࡨࡶ࡮ࡩࠧ଒") in bstack111111llll_opy_)
  if bstack1lllll1111_opy_:
    try:
      if driver_command == bstack1ll_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫଓ"):
        bstack11ll11l1ll_opy_ = TestHubHandler.current_test_uuid()
        if not bstack11ll11l1ll_opy_:
          bstack11ll11l1ll_opy_ = bstack111l111ll1_opy_.current_hook_uuid()
        if not bstack11ll11l1ll_opy_ and bstack1ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩଔ") in bstack111111llll_opy_:
          bstack11ll11l1ll_opy_ = getattr(threading.current_thread(), bstack1ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭କ"), None)
        if bstack11ll11l1ll_opy_:
          bstack1l11l1111l_opy_ = response.get(bstack1ll_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩଖ"), None) if isinstance(response, dict) else None
          if bstack1l11l1111l_opy_ and isinstance(bstack1l11l1111l_opy_, str) and len(bstack1l11l1111l_opy_) > 0:
            if bstack1ll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠬଗ") in bstack111111llll_opy_:
              try:
                from browserstack_sdk.sdk_cli.cli import cli
                if cli and cli.is_running() and cli.bstack1ll11ll11l_opy_:
                  _111l111111_opy_(cli, bstack1l11l1111l_opy_, bstack11ll11l1ll_opy_)
                else:
                  logger.debug(bstack1ll_opy_ (u"࡙ࠬࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠢࡱࡳࡹࠦࡳࡦࡰࡷ࠾ࠥࡉࡌࡊࠢࡱࡳࡹࠦࡲࡦࡣࡧࡽࠬଘ"))
              except Exception as bstack1l1l1l1ll1_opy_:
                logger.debug(bstack1ll_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡳࡪࠠࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠤࡻ࡯ࡡࠡࡩࡕࡔࡈࡀࠠࡼࡿࠪଙ").format(str(bstack1l1l1l1ll1_opy_)))
            else:
              TestHubHandler.bstack11l1l1l111_opy_({
                  bstack1ll_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭ଚ"): bstack1l11l1111l_opy_,
                  bstack1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨଛ"): bstack11ll11l1ll_opy_
              })
        else:
          logger.debug(bstack1ll_opy_ (u"ࠩࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠦࡣࡢࡲࡷࡹࡷ࡫ࡤࠡࡤࡸࡸࠥࡴ࡯ࠡࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨࠤ࡫ࡵࡲࠡࡽࢀࠫଜ").format(bstack111111llll_opy_))
    except Exception as e:
      logger.debug(bstack1ll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡰࡧࠤࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴ࠻ࠢࡾࢁࠬଝ").format(str(e)))
  return response
def _111l111111_opy_(cli, bstack1l11l1111l_opy_, bstack11ll11l1ll_opy_):
  from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack111l1111ll_opy_
  bstack111111l1l1_opy_ = None
  try:
    if cli and cli.test_framework and hasattr(cli.test_framework, bstack1ll_opy_ (u"ࠫ࡬࡫ࡴࡠࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࠩଞ")):
      bstack111111l1l1_opy_ = cli.test_framework.get_current_test_instance()
  except Exception as e:
    logger.debug(bstack1ll_opy_ (u"࡙ࠬࡣࡳࡧࡨࡲࡸ࡮࡯ࡵ࠼ࠣࡇࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡧࡦࡶࠣࡸࡪࡹࡴࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠽ࠤࢀࢃࠧଟ").format(e))
  if bstack111111l1l1_opy_ and cli.bstack111111ll1_opy_:
    entry = bstack111l1111ll_opy_(TestFramework.KIND_SCREENSHOT, bstack1l11l1111l_opy_)
    cli.bstack111111ll1_opy_.bstack11lll1lll1_opy_(bstack111111l1l1_opy_, [entry])
    logger.debug(bstack1ll_opy_ (u"࠭ࡓࡤࡴࡨࡩࡳࡹࡨࡰࡶࠣࡷࡪࡴࡴࠡࡸ࡬ࡥࠥ࡭ࡒࡑࡅࠣࡪࡴࡸࠠࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪ࠽ࡼࡿࠪଠ").format(bstack11ll11l1ll_opy_))
  else:
    logger.debug(bstack1ll_opy_ (u"ࠧࡔࡥࡵࡩࡪࡴࡳࡩࡱࡷࠤࡳࡵࡴࠡࡵࡨࡲࡹࡀࠠࡵࡧࡶࡸࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣࡩࡻ࡫࡮ࡵࡡࡧ࡭ࡸࡶࡡࡵࡥ࡫ࡩࡷࡃࡻࡾࠩଡ").format(
      bstack111111l1l1_opy_ is not None, cli.bstack111111ll1_opy_ is not None))
def bstack1111llll1l_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack11ll11l1_opy_
  global PLATFORM_INDEX
  global SESSION_NAME
  global PARALLELISE_VANILLA_PYTHON
  global PARALLELISE_THREADING_PYTHON
  global FRAMEWORK_NAME
  global bstack11ll1111l_opy_
  global bstack1ll111ll1l_opy_
  global bstack1lll1ll1l1_opy_
  global bstack1l1l1l111l_opy_
  bstack1lll1lll11_opy_ = bstack1l11l1ll11_opy_.bstack1111ll1111_opy_(EVENTS.bstack1l1llll11_opy_.value)
  if os.getenv(bstack1ll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ଢ")) is not None and a11y.bstack1l111l111l_opy_(CONFIG) is None:
    CONFIG[bstack1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩଣ")] = True
  CONFIG[bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬତ")] = str(FRAMEWORK_NAME) + str(__version__)
  bstack1l1111l11l_opy_ = os.environ[bstack1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩଥ")]
  bstack111ll1l1ll_opy_ = TestHubUtils.bstack11l11l11l_opy_(CONFIG, FRAMEWORK_NAME)
  CONFIG[bstack1ll_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨଦ")] = bstack1l1111l11l_opy_
  CONFIG[bstack1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨଧ")] = bstack111ll1l1ll_opy_
  if CONFIG.get(bstack1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧନ"),bstack1ll_opy_ (u"ࠨࠩ଩")) and bstack1ll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨପ") in FRAMEWORK_NAME:
    CONFIG[bstack1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪଫ")].pop(bstack1ll_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩବ"), None)
    CONFIG[bstack1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬଭ")].pop(bstack1ll_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫମ"), None)
  command_executor = bstack1lll11l111_opy_()
  logger.debug(bstack1lll11llll_opy_.format(command_executor))
  proxy = bstack1ll1l1l1l1_opy_(CONFIG, proxy)
  bstack11l11ll1_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
  try:
    if PARALLELISE_VANILLA_PYTHON is True:
      bstack11l11ll1_opy_ = int(multiprocessing.current_process().name)
    elif PARALLELISE_THREADING_PYTHON is True:
      bstack11l11ll1_opy_ = int(threading.current_thread().name)
  except:
    bstack11l11ll1_opy_ = 0
  bstack11ll1ll1ll_opy_ = get_caps(CONFIG, bstack11l11ll1_opy_)
  logger.debug(CONFIG_FILE_CONTENT.format(str(bstack11ll1ll1ll_opy_)))
  if bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫଯ") in CONFIG and bstack11l1l1l11l_opy_(CONFIG[bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬର")]):
    update_caps_for_local(bstack11ll1ll1ll_opy_)
  if a11y.is_enabled_platform(CONFIG, bstack11l11ll1_opy_) and a11y.is_platform_supported(bstack11ll1ll1ll_opy_, options, desired_capabilities, CONFIG):
    threading.current_thread().a11yPlatform = True
    if (cli.accessibility is None or not cli.accessibility.is_enabled() or bstack1ll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠪ଱") in FRAMEWORK_NAME):
      a11y.set_capabilities(bstack11ll1ll1ll_opy_, CONFIG)
  if desired_capabilities:
    bstack11ll1llll1_opy_ = bstack1l11111ll1_opy_(desired_capabilities)
    bstack11ll1llll1_opy_[bstack1ll_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪଲ")] = bstack111lll1ll_opy_(CONFIG)
    bstack11l111ll_opy_ = get_caps(bstack11ll1llll1_opy_)
    if bstack11l111ll_opy_:
      bstack11ll1ll1ll_opy_ = update(bstack11l111ll_opy_, bstack11ll1ll1ll_opy_)
    desired_capabilities = None
  if options:
    bstack1111lll11l_opy_(options, bstack11ll1ll1ll_opy_)
  if not options:
    options = bstack111lll1l11_opy_(bstack11ll1ll1ll_opy_)
  try:
    if bstack1lll111111_opy_:
      def _1111111ll1_opy_(bstack1l1l111111_opy_):
        if not isinstance(bstack1l1l111111_opy_, dict):
          return
        for _11111l1111_opy_ in list(bstack1l1l111111_opy_.keys()):
          _1111lll1ll_opy_ = bstack1l1l111111_opy_[_11111l1111_opy_]
          if _1111lll1ll_opy_ is None:
            bstack1l1l111111_opy_.pop(_11111l1111_opy_, None)
          elif isinstance(_1111lll1ll_opy_, dict):
            _1111111ll1_opy_(_1111lll1ll_opy_)
      _1111111ll1_opy_(bstack11ll1ll1ll_opy_)
      _1111111ll1_opy_(desired_capabilities)
      if options is not None and hasattr(options, bstack1ll_opy_ (u"ࠫࡤࡩࡡࡱࡵࠪଳ")):
        _1111111ll1_opy_(options._caps)
  except Exception as e:
    logger.debug(bstack1ll_opy_ (u"ࠧࡳ࡯ࡥࡡ࡬ࡲ࡮ࡺࠨࠪࠢࡳࡳࡸࡺ࠭ࡰࡲࡷ࡭ࡴࡴࡳࠡࡲࡵࡹࡳ࡫ࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡽࢀࠦ଴").format(e))
  if bstack1lll111111_opy_:
    options = bstack1l11l11ll_opy_(options)
  bstack1l1l1l111l_opy_ = CONFIG.get(bstack1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଵ"))[bstack11l11ll1_opy_]
  if proxy and bstack1ll11l11l1_opy_() >= version.parse(bstack1ll_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧଶ")):
    options.proxy(proxy)
  if options and bstack1ll11l11l1_opy_() >= version.parse(bstack1ll_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧଷ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1ll11l11l1_opy_() < version.parse(bstack1ll_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨସ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack11ll1ll1ll_opy_)
  logger.info(bstack11ll11l111_opy_)
  bstack1l11ll1lll_opy_.end(EVENTS.bstack1l1ll1111l_opy_.value, EVENTS.bstack1l1ll1111l_opy_.value + bstack1ll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥହ"), EVENTS.bstack1l1ll1111l_opy_.value + bstack1ll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ଺"), status=True, failure=None, test_name=SESSION_NAME)
  if bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡰࡳࡱࡩ࡭ࡱ࡫ࠧ଻") in kwargs:
    del kwargs[bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡱࡴࡲࡪ࡮ࡲࡥࠨ଼")]
  bstack1l11l1ll11_opy_.end(EVENTS.bstack1l1llll11_opy_.value, bstack1lll1lll11_opy_ + bstack1ll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢଽ"), bstack1lll1lll11_opy_ + bstack1ll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨା"), status=True, failure=None, test_name=SESSION_NAME)
  try:
    if bstack1ll11l11l1_opy_() >= version.parse(bstack1ll_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩି")):
      bstack11ll1111l_opy_(self, command_executor=command_executor,
                options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
    elif bstack1ll11l11l1_opy_() >= version.parse(bstack1ll_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩୀ")):
      bstack11ll1111l_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities, options=options,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1ll11l11l1_opy_() >= version.parse(bstack1ll_opy_ (u"ࠫ࠷࠴࠵࠴࠰࠳ࠫୁ")):
      bstack11ll1111l_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    else:
      bstack11ll1111l_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive)
  except Exception as bstack11111ll1l_opy_:
    logger.error(bstack1lll1l11_opy_.format(bstack1ll_opy_ (u"ࠬࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠫୂ"), str(bstack11111ll1l_opy_)))
    raise bstack11111ll1l_opy_
  bstack1lll1lll11_opy_ = bstack1l11l1ll11_opy_.bstack1111ll1111_opy_(EVENTS.bstack111111ll_opy_.value)
  if a11y.is_enabled_platform(CONFIG, bstack11l11ll1_opy_) and a11y.is_platform_supported(self.capabilities, options, desired_capabilities):
    if CONFIG[bstack1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨୃ")][bstack1ll_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ୄ")] == True:
      threading.current_thread().appA11yPlatform = True
      if cli.accessibility is None or not cli.accessibility.is_enabled() or bstack1ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩ୅") in FRAMEWORK_NAME:
        a11y.set_capabilities(bstack11ll1ll1ll_opy_, CONFIG)
  try:
    bstack1llll111l_opy_ = bstack1ll_opy_ (u"ࠩࠪ୆")
    if bstack1ll11l11l1_opy_() >= version.parse(bstack1ll_opy_ (u"ࠪ࠸࠳࠶࠮࠱ࡤ࠴ࠫେ")):
      if self.caps is not None:
        bstack1llll111l_opy_ = self.caps.get(bstack1ll_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦୈ"))
    else:
      if self.capabilities is not None:
        bstack1llll111l_opy_ = self.capabilities.get(bstack1ll_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧ୉"))
    if bstack1llll111l_opy_:
      bstack111l1l1ll1_opy_(bstack1llll111l_opy_)
      if bstack1ll11l11l1_opy_() <= version.parse(bstack1ll_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭୊")):
        if bstack1ll1111l1_opy_.startswith(bstack1ll_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࠨୋ")) or bstack1ll1111l1_opy_.startswith(bstack1ll_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࠪୌ")):
          self.command_executor._url = bstack1ll1111l1_opy_
        else:
          self.command_executor._url = bstack1ll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱୍ࠥ") + bstack1ll1111l1_opy_ + bstack1ll_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢ୎")
      else:
        self.command_executor._url = bstack1ll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨ୏") + bstack1llll111l_opy_ + bstack1ll_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨ୐")
      logger.debug(bstack11l11111ll_opy_.format(bstack1llll111l_opy_))
    else:
      logger.debug(bstack111l1l1l1_opy_.format(bstack1ll_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢ୑")))
  except Exception as e:
    logger.debug(bstack111l1l1l1_opy_.format(e))
  if bstack1ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭୒") in FRAMEWORK_NAME:
    bstack1l1ll1l111_opy_(PLATFORM_INDEX, bstack1lll1ll1l1_opy_)
  bstack11ll11l1_opy_ = self.session_id
  if bstack1ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ୓") in FRAMEWORK_NAME or bstack1ll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ୔") in FRAMEWORK_NAME or bstack1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ୕") in FRAMEWORK_NAME or bstack1ll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠬୖ") in FRAMEWORK_NAME:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack1111l1ll11_opy_ = getattr(threading.current_thread(), bstack1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࡙࡫ࡳࡵࡏࡨࡸࡦ࠭ୗ"), None)
  if bstack1ll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭୘") in FRAMEWORK_NAME or bstack1ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭୙") in FRAMEWORK_NAME:
    TestHubHandler.send_cbt_info(self)
  if bstack1ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ୚") in FRAMEWORK_NAME and bstack1111l1ll11_opy_ and bstack1111l1ll11_opy_.get(bstack1ll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ୛"), bstack1ll_opy_ (u"ࠪࠫଡ଼")) == bstack1ll_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬଢ଼"):
    TestHubHandler.send_cbt_info(self)
  with bstack111l1111_opy_:
    bstack1ll111ll1l_opy_.append(self)
  if bstack1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ୞") in CONFIG and bstack1ll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫୟ") in CONFIG[bstack1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪୠ")][bstack11l11ll1_opy_]:
    SESSION_NAME = CONFIG[bstack1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫୡ")][bstack11l11ll1_opy_][bstack1ll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧୢ")]
  logger.debug(bstack1111lll1l_opy_.format(bstack11ll11l1_opy_))
  bstack1l11l1ll11_opy_.end(EVENTS.bstack111111ll_opy_.value, bstack1lll1lll11_opy_ + bstack1ll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥୣ"), bstack1lll1lll11_opy_ + bstack1ll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ୤"), status=True, failure=None, test_name=SESSION_NAME)
ROBOT_PLAYWRIGHT_CDP_URL = None
bstack1l1ll1ll_opy_ = False
bstack11111l11l_opy_ = None
def set_playwright_globals(**kwargs):
    bstack1ll_opy_ (u"ࠧࠨࠢࡊࡰ࡭ࡩࡨࡺࠠࡨ࡮ࡲࡦࡦࡲࡳࠡࡨࡵࡳࡲࠦ࡟ࡠ࡫ࡱ࡭ࡹࡥ࡟࠯ࡲࡼࠤ࡮ࡴࡴࡰࠢࡷ࡬࡮ࡹࠠ࡮ࡱࡧࡹࡱ࡫ࠧࡴࠢࡱࡥࡲ࡫ࡳࡱࡣࡦࡩ࠳ࠐࠠࠡࠢࠣࡇࡦࡲ࡬ࡦࡦࠣࡦࡾࠦ࡟ࡠ࡫ࡱ࡭ࡹࡥ࡟࠯ࡲࡼࠤࡧ࡫ࡦࡰࡴࡨࠤࡵࡧࡴࡤࡪࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠨࠪࠢࡶࡳࠥࡺࡨࡢࡶࠣࡱࡴࡪ࡟࡭ࡣࡸࡲࡨ࡮ࠊࠡࠢࠣࠤࡦࡴࡤࠡࡲࡤࡸࡨ࡮࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡨࡧ࡮ࠡࡣࡦࡧࡪࡹࡳࠡࡅࡒࡒࡋࡏࡇ࠭ࠢࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤࡔࡁࡎࡇ࠯ࠤࡪࡺࡣ࠯ࠤࠥࠦ୥")
    g = globals()
    for key, value in kwargs.items():
        g[key] = value
try:
  try:
    import Browser
    import os
    from subprocess import Popen
    from browserstack_sdk.__init__ import get_turboscale_playwright_url
    from browserstack_sdk.sdk_cli.utils.bstack11111111l1_opy_ import bstack1ll1l11l1l_opy_
    def bstack11l11111l1_opy_(self, args, **kwargs):
      global CONFIG
      global SELENIUM_OR_PLAYWRIGHT_INSTALLED
      global ROBOT_PLAYWRIGHT_CDP_URL
      global bstack1l1ll1ll_opy_
      from browserstack_sdk.__init__ import LAUNCH_PATCH_ROBOT_PLAYWRIGHT
      if(bstack1ll_opy_ (u"ࠨࡩ࡯ࡦࡨࡼ࠳ࡰࡳࠣ୦") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1ll_opy_ (u"ࠧࡿࠩ୧")), bstack1ll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ୨"), bstack1ll_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫ୩")), bstack1ll_opy_ (u"ࠪࡻࠬ୪")) as fp:
          fp.write(bstack1ll_opy_ (u"ࠦࠧ୫"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1ll_opy_ (u"ࠧ࡯࡮ࡥࡧࡻࡣࡧࡹࡴࡢࡥ࡮࠲࡯ࡹࠢ୬")))):
          with open(args[1], bstack1ll_opy_ (u"࠭ࡲࠨ୭")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1ll_opy_ (u"ࠧࡢࡵࡼࡲࡨࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡡࡱࡩࡼࡖࡡࡨࡧࠫࡧࡴࡴࡴࡦࡺࡷ࠰ࠥࡶࡡࡨࡧࠣࡁࠥࡼ࡯ࡪࡦࠣ࠴࠮࠭୮") in line), None)
            if index is not None:
                lines.insert(index+2, bstack111l1l111_opy_)
            if bstack1ll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ୯") in CONFIG and str(CONFIG[bstack1ll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭୰")]).lower() != bstack1ll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩୱ"):
                cdpUrl = get_turboscale_playwright_url()
                LAUNCH_PATCH_ROBOT_PLAYWRIGHT = bstack1ll_opy_ (u"ࠫࠬ࠭ࠊ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱ࠍࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠷ࡠࠤࡂࡃ࠽ࠡࠩࡷࡶࡺ࡫ࠧ࠼ࠌࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭ࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࡠ࠿ࠏࡩ࡯࡯ࡵࡷࠤࡧࡹࡴࡢࡥ࡮ࡣࡨࡧࡰࡴࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠶ࡣ࠻ࠋࡥࡲࡲࡸࡺࠠࡱࡡ࡬ࡲࡩ࡫ࡸࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࡝ࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠶ࡢࡁࠊࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠶ࡠࠤࡂࡃ࠽ࠡࠩࡷࡶࡺ࡫ࠧ࠼ࠌࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰ࡶࡰ࡮ࡩࡥࠩ࠲࠯ࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠻ࠩ࠼ࠌࡦࡳࡳࡹࡴࠡ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢࠪ࠽ࠍࡧࡴࡴࡳࡵࠢࡲࡶ࡮࡭ࡩ࡯ࡣ࡯ࡣࡨ࡮ࡲࡰ࡯࡬ࡹࡲࡥ࡬ࡢࡷࡱࡧ࡭ࠦ࠽ࠡ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭࠯࡮ࡤࡹࡳࡩࡨ࠯ࡤ࡬ࡲࡩ࠮ࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠯࠻ࠋ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭࠯࡮ࡤࡹࡳࡩࡨࠡ࠿ࠣࡥࡸࡿ࡮ࡤࠢࠫࡰࡦࡻ࡮ࡤࡪࡒࡴࡹ࡯࡯࡯ࡵࠬࠤࡂࡄࠠࡼࡽࠍࠤࠥ࡯ࡦࠡࠪࠤࡦࡸࡺࡡࡤ࡭ࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠩࠡࡽࡾࠎࠥࠦࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡣࡺࡥ࡮ࡺࠠࡰࡴ࡬࡫࡮ࡴࡡ࡭ࡡࡦ࡬ࡷࡵ࡭ࡪࡷࡰࡣࡱࡧࡵ࡯ࡥ࡫ࠬࡱࡧࡵ࡯ࡥ࡫ࡓࡵࡺࡩࡰࡰࡶ࠭ࡀࠐࠠࠡࡿࢀࠎࠥࠦ࡬ࡦࡶࠣࡧࡦࡶࡳ࠼ࠌࠣࠤࡹࡸࡹࠡࡽࡾࠎࠥࠦࠠࠡࡥࡤࡴࡸࠦ࠽ࠡࡌࡖࡓࡓ࠴ࡰࡢࡴࡶࡩ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡩࡡࡱࡵࠬ࠿ࠏࠦࠠࡾࡿࠣࡧࡦࡺࡣࡩࠢࠫࡩࡽ࠯ࠠࡼࡽࠍࠤࠥࠦࠠࡤࡱࡱࡷࡴࡲࡥ࠯ࡧࡵࡶࡴࡸࠨࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴ࠼ࠥ࠰ࠥ࡫ࡸࠪ࠽ࠍࠤࠥࢃࡽࠋࠢࠣ࡭࡫ࠦࠨࡣࡵࡷࡥࡨࡱ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠩࠡࡽࡾࠎࠥࠦࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡣࡺࡥ࡮ࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮ࡤࡱࡱࡲࡪࡩࡴࡐࡸࡨࡶࡈࡊࡐࠩࡽࡾࠎࠥࠦࠠࠡࠢࠣࡩࡳࡪࡰࡰ࡫ࡱࡸ࡚ࡘࡌ࠻ࠢࠪࡿࡨࡪࡰࡖࡴ࡯ࢁࠬࠦࠫࠡࡧࡱࡧࡴࡪࡥࡖࡔࡌࡇࡴࡳࡰࡰࡰࡨࡲࡹ࠮ࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡤࡣࡳࡷ࠮࠯ࠬࠋࠢࠣࠤࠥࠦࠠ࠯࠰࠱ࡰࡦࡻ࡮ࡤࡪࡒࡴࡹ࡯࡯࡯ࡵࠍࠤࠥࠦࠠࡾࡿࠬ࠿ࠏࠦࠠࡾࡿࠍࠤࠥࡸࡥࡵࡷࡵࡲࠥࡧࡷࡢ࡫ࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡨࡵ࡮࡯ࡧࡦࡸ࠭ࢁࡻࠋࠢࠣࠤࠥࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵ࠼ࠣࠫࢀࡩࡤࡱࡗࡵࡰࢂ࠭ࠠࠬࠢࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩ࠭ࠌࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴࠌࠣࠤࢂࢃࠩ࠼ࠌࢀࢁࡀࠐࡣࡰࡰࡶࡸࠥࡵࡲࡪࡩ࡬ࡲࡦࡲ࡟ࡤࡱࡱࡲࡪࡩࡴࠡ࠿ࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷ࠲ࡧ࡯࡮ࡥࠪ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱ࠮ࡤࡪࡵࡳࡲ࡯ࡵ࡮ࠫ࠾ࠎ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡨࡵ࡮࡯ࡧࡦࡸࠥࡃࠠࡢࡵࡼࡲࡨࠦࠨࡤࡱࡱࡲࡪࡩࡴࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁࡻࠋࠢࠣ࡭࡫ࠦࠨࠢࡤࡶࡸࡦࡩ࡫ࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠮ࠦࡻࡼࠌࠣࠤࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥࡵࡲࡪࡩ࡬ࡲࡦࡲ࡟ࡤࡱࡱࡲࡪࡩࡴࠩࡥࡲࡲࡳ࡫ࡣࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠫ࠾ࠎࠥࠦࡽࡾࠌࠣࠤࡱ࡫ࡴࠡࡥࡤࡴࡸࡁࠊࠡࠢࡷࡶࡾࠦࡻࡼࠌࠣࠤࠥࠦࡣࡢࡲࡶࠤࡂࠦࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠪ࠽ࠍࠤࠥࢃࡽࠡࡥࡤࡸࡨ࡮ࠠࠩࡧࡻ࠭ࠥࢁࡻࠋࠢࠣࢁࢂࠐࠠࠡࡥࡲࡲࡸࡺࠠ࡮ࡱࡧ࡭࡫࡯ࡥࡥࡇࡱࡨࡵࡵࡩ࡯ࡶࠣࡁࠥ࠭ࡻࡤࡦࡳ࡙ࡷࡲࡽࠨࠢ࠮ࠤࡪࡴࡣࡰࡦࡨ࡙ࡗࡏࡃࡰ࡯ࡳࡳࡳ࡫࡮ࡵࠪࡍࡗࡔࡔ࠮ࡴࡶࡵ࡭ࡳ࡭ࡩࡧࡻࠫࡧࡦࡶࡳࠪࠫ࠾ࠎࠥࠦࡩࡧࠢࠫࡦࡸࡺࡡࡤ࡭ࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠬࠤࢀࢁࠊࠡࠢࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷࡓࡻ࡫ࡲࡄࡆࡓࠬࢀࢁࠊࠡࠢࠣࠤࠥࠦࡥ࡯ࡦࡳࡳ࡮ࡴࡴࡖࡔࡏ࠾ࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࠭ࠌࠣࠤࠥࠦࠠࠡ࠰࠱࠲ࡨࡵ࡮࡯ࡧࡦࡸࡔࡶࡴࡪࡱࡱࡷࠏࠦࠠࠡࠢࢀࢁ࠮ࡁࠊࠡࠢࢀࢁࠏࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦ࡯ࡳ࡫ࡪ࡭ࡳࡧ࡬ࡠࡥࡲࡲࡳ࡫ࡣࡵࠪࡾࡿࠏࠦࠠࠡࠢ࠱࠲࠳ࡩ࡯࡯ࡰࡨࡧࡹࡕࡰࡵ࡫ࡲࡲࡸ࠲ࠊࠡࠢࠣࠤࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࠻ࠢࡰࡳࡩ࡯ࡦࡪࡧࡧࡉࡳࡪࡰࡰ࡫ࡱࡸࠏࠦࠠࡾࡿࠬ࠿ࠏࢃࡽ࠼ࠌ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࠏ࠭ࠧࠨ୲").format(cdpUrl=cdpUrl)
            lines.insert(1, LAUNCH_PATCH_ROBOT_PLAYWRIGHT)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1ll_opy_ (u"ࠧ࡯࡮ࡥࡧࡻࡣࡧࡹࡴࡢࡥ࡮࠲࡯ࡹࠢ୳")), bstack1ll_opy_ (u"࠭ࡷࠨ୴")) as bstack111lll11_opy_:
              bstack111lll11_opy_.writelines(lines)
        CONFIG[bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ୵")] = str(FRAMEWORK_NAME) + str(__version__)
        bstack1l1111l11l_opy_ = os.environ[bstack1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭୶")]
        bstack111ll1l1ll_opy_ = TestHubUtils.bstack11l11l11l_opy_(CONFIG, FRAMEWORK_NAME)
        CONFIG[bstack1ll_opy_ (u"ࠩࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬ୷")] = bstack1l1111l11l_opy_
        CONFIG[bstack1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬ୸")] = bstack111ll1l1ll_opy_
        bstack11l11ll1_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
        try:
          if PARALLELISE_VANILLA_PYTHON is True:
            bstack11l11ll1_opy_ = int(multiprocessing.current_process().name)
          elif PARALLELISE_THREADING_PYTHON is True:
            bstack11l11ll1_opy_ = int(threading.current_thread().name)
        except Exception:
          bstack11l11ll1_opy_ = 0
        CONFIG[bstack1ll_opy_ (u"ࠦࡺࡹࡥࡘ࠵ࡆࠦ୹")] = False
        CONFIG[bstack1ll_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦ୺")] = True
        bstack1111l111ll_opy_ = bstack1ll1l11l1l_opy_(bstack11l11ll1_opy_)
        if bstack1111l111ll_opy_ is not None:
          import bstack_utils.constants as _1lll1l1ll1_opy_
          _1l11111ll_opy_ = bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ୻") if bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ୼") in bstack1111l111ll_opy_ else bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭୽")
          _111l1lll1l_opy_ = bstack1111l111ll_opy_.get(_1l11111ll_opy_, bstack1ll_opy_ (u"ࠩࠪ୾")).strip().lower()
          _1111lll1l1_opy_ = _111l1lll1l_opy_ in _1lll1l1ll1_opy_.bstack1l1lll11l1_opy_
          if bstack1111l111ll_opy_.get(bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ୿")) and not _1111lll1l1_opy_:
            bstack1111l111ll_opy_[bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ஀")] = False
            _1lllll11_opy_ = [k for k in bstack1111l111ll_opy_ if k.startswith(bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ஁"))]
            for k in _1lllll11_opy_:
              del bstack1111l111ll_opy_[k]
          bstack11l1ll1l_opy_ = bstack1111l111ll_opy_
          import urllib.parse
          if bstack1ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪஂ") in CONFIG and str(CONFIG[bstack1ll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫஃ")]).lower() != bstack1ll_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧ஄"):
            ROBOT_PLAYWRIGHT_CDP_URL = get_turboscale_playwright_url() + urllib.parse.quote(json.dumps(bstack11l1ll1l_opy_))
          else:
            ROBOT_PLAYWRIGHT_CDP_URL = bstack1ll_opy_ (u"ࠩࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠫஅ") + urllib.parse.quote(json.dumps(bstack11l1ll1l_opy_))
          os.environ[bstack1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡓࡇࡕࡔࡠࡒ࡚ࡣࡈࡊࡐࡠࡗࡕࡐࠬஆ")] = ROBOT_PLAYWRIGHT_CDP_URL
          bstack1l1ll1ll_opy_ = True
          from browserstack_sdk.sdk_cli.bstack11111ll111_opy_ import bstack11l1111ll_opy_
          from browserstack_sdk.sdk_cli.bstack111lll11ll_opy_ import bstack11ll1l111l_opy_
          instance = next(iter(bstack11l1111ll_opy_.bstack1l111l11l_opy_.values()), None)
          if instance:
            bstack11ll1l111l_opy_.bstack1l1l1l1l_opy_(instance, bstack11ll1l111l_opy_.bstack11l1111l1l_opy_, bstack1111l111ll_opy_)
            bstack11ll1l111l_opy_.bstack1l1l1l1l_opy_(instance, bstack11ll1l111l_opy_.bstack11llll1l11_opy_, ROBOT_PLAYWRIGHT_CDP_URL)
          try:
            from browserstack_sdk.sdk_cli.cli import cli as _11l11ll111_opy_
            from browserstack_sdk.sdk_cli.bstack11111ll111_opy_ import bstack1111ll1l11_opy_, bstack1llll11lll_opy_
            _11l11ll111_opy_.bstack11111ll111_opy_.bstack1l1l1ll1ll_opy_(
              None,
              (instance, bstack1ll_opy_ (u"ࠫࡲࡵࡤࡠࡲࡲࡴࡪࡴࠧஇ")),
              (bstack1111ll1l11_opy_.bstack1l1l1l11l_opy_, bstack1llll11lll_opy_.PRE),
              None,
            )
          except Exception as e:
            logger.debug(bstack1ll_opy_ (u"ࠧࡳ࡯ࡥࡡࡳࡳࡵ࡫࡮࠻ࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡬ࡩࡳࡧࠣࡇࡗࡋࡁࡕࡇ࠱ࡔࡗࡋ࠺ࠡࡽࢀࠦஈ").format(e))
          logger.debug(bstack1ll_opy_ (u"ࠨ࡭ࡰࡦࡢࡴࡴࡶࡥ࡯࠼ࠣࡹࡸ࡯࡮ࡨࠢࡩ࡭ࡳࡧ࡬ࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡧࡴࡲࡱࠥࡊࡲࡪࡸࡨࡶࡎࡴࡩࡵࠤஉ"))
        else:
          bstack11l1ll1l_opy_ = get_caps(CONFIG, bstack11l11ll1_opy_)
          if CONFIG.get(bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫஊ")):
            update_caps_for_local(bstack11l1ll1l_opy_)
            bstack11l1ll1l_opy_[bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ஋")] = os.environ[bstack1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ஌")]
          logger.debug(bstack1ll_opy_ (u"ࠥࡱࡴࡪ࡟ࡱࡱࡳࡩࡳࡀࠠࡅࡴ࡬ࡺࡪࡸࡉ࡯࡫ࡷࠤࡺࡴࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦ࠮ࠣࡪࡦࡲ࡬ࡪࡰࡪࠤࡧࡧࡣ࡬ࠢࡷࡳࠥ࡭ࡥࡵࡡࡦࡥࡵࡹࠢ஍"))
        logger.debug(CONFIG_FILE_CONTENT.format(str(bstack11l1ll1l_opy_)))
        if bstack1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧஎ") in CONFIG and bstack1ll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪஏ") in CONFIG[bstack1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩஐ")][bstack11l11ll1_opy_]:
          SESSION_NAME = CONFIG[bstack1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ஑")][bstack11l11ll1_opy_][bstack1ll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ஒ")]
        from bstack_utils.helper import bstack1lll1111ll_opy_
        args.append(bstack1ll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧஓ") if bstack1lll1111ll_opy_(CONFIG) else bstack1ll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩஔ"))
        args.append(str(bstack11l1ll1l_opy_.get(bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪக"), False)).lower())
        args.append(os.path.join(os.path.expanduser(bstack1ll_opy_ (u"ࠬࢄࠧ஖")), bstack1ll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭஗"), bstack1ll_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩ஘")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack11l1ll1l_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1ll_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥங"))
      SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
      return bstack111111l1_opy_(self, args, **kwargs)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1l111l1l1_opy_(self,
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
    CONFIG[bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫச")] = str(FRAMEWORK_NAME) + str(__version__)
    bstack1l1111l11l_opy_ = os.environ[bstack1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ஛")]
    bstack111ll1l1ll_opy_ = TestHubUtils.bstack11l11l11l_opy_(CONFIG, FRAMEWORK_NAME)
    CONFIG[bstack1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧஜ")] = bstack1l1111l11l_opy_
    CONFIG[bstack1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧ஝")] = bstack111ll1l1ll_opy_
    bstack11l11ll1_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
    try:
      if PARALLELISE_VANILLA_PYTHON is True:
        bstack11l11ll1_opy_ = int(multiprocessing.current_process().name)
      elif PARALLELISE_THREADING_PYTHON is True:
        bstack11l11ll1_opy_ = int(threading.current_thread().name)
    except Exception:
      bstack11l11ll1_opy_ = 0
    CONFIG[bstack1ll_opy_ (u"ࠨࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧஞ")] = True
    bstack11ll1ll1ll_opy_ = get_caps(CONFIG, bstack11l11ll1_opy_)
    bstack1lllllll1l_opy_ = bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨட") if bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩ஠") in bstack11ll1ll1ll_opy_ else bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ஡")
    bstack1lll111ll1_opy_ = False
    try:
        from bstack_utils import accessibility as a11y
        import bstack_utils.constants as bstack11lll1111l_opy_
        bstack11ll111l_opy_ = bstack11ll1ll1ll_opy_.get(bstack1lllllll1l_opy_, bstack1ll_opy_ (u"ࠪࠫ஢")).strip().lower()
        browser_version = str(bstack11ll1ll1ll_opy_.get(bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ண"), bstack11ll1ll1ll_opy_.get(bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭த"), bstack1ll_opy_ (u"࠭ࠧ஥")))).strip()
        bstack1lll1l111_opy_ = bstack11ll111l_opy_ in bstack11lll1111l_opy_.bstack1l1lll11l1_opy_
        min_version = bstack11lll1111l_opy_.MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION
        if not browser_version or browser_version.lower().startswith(bstack1ll_opy_ (u"ࠧ࡭ࡣࡷࡩࡸࡺࠧ஦")):
            bstack1ll1l111l_opy_ = True
        else:
            major = browser_version.split(bstack1ll_opy_ (u"ࠨ࠰ࠪ஧"))[0]
            bstack1ll1l111l_opy_ = major.isdigit() and int(major) > min_version
        if not bstack1ll1l111l_opy_:
            logger.warning(bstack1ll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࠣࡺࡪࡸࡳࡪࡱࡱࠤ࡬ࡸࡥࡢࡶࡨࡶࠥࡺࡨࡢࡰࠣࡿࢂ࠴ࠠࡄࡷࡵࡶࡪࡴࡴࠡࡸࡨࡶࡸ࡯࡯࡯࠼ࠣࡿࢂࠨந").format(min_version, browser_version))
        if a11y.is_enabled_platform(CONFIG, bstack11l11ll1_opy_) and bstack1lll1l111_opy_ and bstack1ll1l111l_opy_ and a11y.is_platform_supported(bstack11ll1ll1ll_opy_, options=None, config=CONFIG):
            bstack1lll111ll1_opy_ = True
            import browserstack_sdk
            browserstack_sdk.CONFIG[bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩன")] = True
            bstack11ll1ll1ll_opy_[bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪப")] = True
            if CONFIG.get(bstack1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧ஫")):
                bstack11ll1ll1ll_opy_[bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧ஬")] = CONFIG[bstack1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩ஭")]
            import json as _json
            bstack111llll1_opy_ = os.getenv(bstack1ll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ம"))
            bstack1l11ll11l_opy_ = bstack11ll1ll1ll_opy_.get(bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳ࠯ࡣࡸࡸ࡭࡚࡯࡬ࡧࡱࠫய"))
            if not bstack111llll1_opy_ and bstack1l11ll11l_opy_:
                os.environ[bstack1ll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨர")] = bstack1l11ll11l_opy_
                bstack111llll1_opy_ = bstack1l11ll11l_opy_
            if bstack111llll1_opy_:
                bstack11ll1ll1ll_opy_[bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵ࠱ࡥࡺࡺࡨࡕࡱ࡮ࡩࡳ࠭ற")] = bstack111llll1_opy_
            bstack111ll1ll1l_opy_ = _json.loads(os.getenv(bstack1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ல"), bstack1ll_opy_ (u"࠭ࡻࡾࠩள"))).get(bstack1ll_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨழ"))
            if bstack111ll1ll1l_opy_:
                bstack11ll1ll1ll_opy_[bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹ࠮ࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨவ")] = bstack111ll1ll1l_opy_
            bstack11ll1ll1ll_opy_.pop(bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨஶ"), None)
            bstack11ll1ll1ll_opy_.pop(bstack1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪஷ"), None)
            bstack11ll1ll1ll_opy_.pop(bstack1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫஸ"), None)
            logger.debug(bstack1ll_opy_ (u"ࠧࡇ࠱࠲ࡻࠣࡩࡳࡧࡢ࡭ࡧࡧࠤ࡫ࡵࡲࠡࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࠨࡼࡿࠣࡿࢂ࠯ࠢஹ").format(
                bstack11ll111l_opy_, browser_version))
    except Exception as e:
        bstack1lll111ll1_opy_ = False
        logger.debug(bstack1ll_opy_ (u"ࠨࡁ࠲࠳ࡼࠤࡩ࡫ࡴࡦࡥࡷ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡽࢀࠦ஺").format(str(e)))
    logger.debug(CONFIG_FILE_CONTENT.format(str(bstack11ll1ll1ll_opy_)))
    if CONFIG.get(bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ஻")):
      update_caps_for_local(bstack11ll1ll1ll_opy_)
    if bstack1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ஼") in CONFIG and bstack1ll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ஽") in CONFIG[bstack1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ா")][bstack11l11ll1_opy_]:
      SESSION_NAME = CONFIG[bstack1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧி")][bstack11l11ll1_opy_][bstack1ll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪீ")]
    import urllib
    import json
    if bstack1ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪு") in CONFIG and str(CONFIG[bstack1ll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫூ")]).lower() != bstack1ll_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧ௃"):
        bstack1ll1ll11l1_opy_ = get_turboscale_playwright_url()
        cdpUrl = bstack1ll1ll11l1_opy_ + urllib.parse.quote(json.dumps(bstack11ll1ll1ll_opy_))
    else:
        cdpUrl = bstack1ll_opy_ (u"ࠩࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠫ௄") + urllib.parse.quote(json.dumps(bstack11ll1ll1ll_opy_))
    try:
        from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
        PlaywrightDriverWrapperDirect.setup_dispatch_capture()
    except Exception as exc:
        logger.debug(bstack1ll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࡸࡴࠥࡪࡩࡴࡲࡤࡸࡨ࡮ࠠࡤࡣࡳࡸࡺࡸࡥࠡࡨࡲࡶࠥࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥ࠼ࠣࠩࡸࠨ௅"), exc)
    if bstack1lll111ll1_opy_:
        browser = self.connect_over_cdp(cdpUrl)
    else:
        browser = bstack11111l11l_opy_(self, cdpUrl)
    try:
        from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
        wrapper = PlaywrightDriverWrapperDirect(browser, page=None, capabilities=bstack11ll1ll1ll_opy_, config=CONFIG)
        threading.current_thread().bstackSessionDriver = wrapper
        logger.debug(bstack1ll_opy_ (u"ࠦࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡅࡴ࡬ࡺࡪࡸࡗࡳࡣࡳࡴࡪࡸࡄࡪࡴࡨࡧࡹࠦࡳࡦࡶࡸࡴࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫ࠠࡧࡱࡵࠤࡹ࡮ࡲࡦࡣࡧࠤࠪࡹࠢெ"), threading.get_ident())
        threading.current_thread().bstackTestErrorMessages = []
        if bstack1lll111ll1_opy_:
            threading.current_thread().a11yPlatform = True
            wrapper.bstackA11yShouldScan = True
        if wrapper.session_id and not wrapper._cbt_info_sent:
            PlaywrightDriverWrapperDirect._send_cbt_info_on_session()
        try:
            from playwright.sync_api import Browser as bstack1llll1l1_opy_
            if not hasattr(bstack1llll1l1_opy_, bstack1ll_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥ࡮ࡦࡹࡢࡴࡦ࡭ࡥࡠࡲࡤࡸࡨ࡮ࡥࡥࠩே")):
                _1ll11ll1_opy_ = bstack1llll1l1_opy_.new_page
                def _1ll111l11_opy_(bstack11l111l11l_opy_, *bstack11l1l1ll1l_opy_, **bstack1ll11lll1_opy_):
                    if getattr(threading.current_thread(), bstack1ll_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬை"), None):
                        try:
                            bstack1llll1ll1_opy_ = bstack11l111l11l_opy_.contexts[0] if bstack11l111l11l_opy_.contexts else None
                            if bstack1llll1ll1_opy_ and bstack1llll1ll1_opy_.pages:
                                page = None
                                for _1lllll1llll_opy_ in bstack1llll1ll1_opy_.pages:
                                    if bstack1ll_opy_ (u"ࠢࡢࡤࡲࡹࡹࡀࡢ࡭ࡣࡱ࡯ࠧ௉") in _1lllll1llll_opy_.url:
                                        page = _1lllll1llll_opy_
                                        logger.debug(bstack1ll_opy_ (u"ࠣࡃ࠴࠵ࡾࡀࠠࡳࡧࡸࡷ࡮ࡴࡧࠡࡣࡥࡳࡺࡺ࠺ࡣ࡮ࡤࡲࡰࠦࡰࡢࡩࡨࠤ࡫ࡸ࡯࡮ࠢࡧࡩ࡫ࡧࡵ࡭ࡶࠣࡧࡴࡴࡴࡦࡺࡷࠦொ"))
                                        break
                                if page is None:
                                    page = bstack1llll1ll1_opy_.new_page(*bstack11l1l1ll1l_opy_, **bstack1ll11lll1_opy_)
                                    logger.debug(bstack1ll_opy_ (u"ࠤࡄ࠵࠶ࡿ࠺ࠡࡰࡲࠤࡧࡲࡡ࡯࡭ࠣࡴࡦ࡭ࡥࠡࡨࡲࡹࡳࡪࠬࠡࡥࡵࡩࡦࡺࡥࡥࠢࡱࡩࡼࠦࡰࡢࡩࡨࠤ࡮ࡴࠠࡥࡧࡩࡥࡺࡲࡴࠡࡥࡲࡲࡹ࡫ࡸࡵࠤோ"))
                            elif bstack1llll1ll1_opy_:
                                page = bstack1llll1ll1_opy_.new_page(*bstack11l1l1ll1l_opy_, **bstack1ll11lll1_opy_)
                                logger.debug(bstack1ll_opy_ (u"ࠥࡅ࠶࠷ࡹ࠻ࠢࡦࡶࡪࡧࡴࡦࡦࠣࡲࡪࡽࠠࡱࡣࡪࡩࠥ࡯࡮ࠡࡦࡨࡪࡦࡻ࡬ࡵࠢࡦࡳࡳࡺࡥࡹࡶࠥௌ"))
                            else:
                                page = _1ll11ll1_opy_(bstack11l111l11l_opy_, *bstack11l1l1ll1l_opy_, **bstack1ll11lll1_opy_)
                                logger.debug(bstack1ll_opy_ (u"ࠦࡆ࠷࠱ࡺ࠼ࠣࡲࡴࠦࡤࡦࡨࡤࡹࡱࡺࠠࡤࡱࡱࡸࡪࡾࡴ࠭ࠢࡩࡥࡱࡲࡩ࡯ࡩࠣࡦࡦࡩ࡫ࠡࡶࡲࠤࡳ࡫ࡷࡠࡲࡤ࡫ࡪ࠮்ࠩࠣ"))
                        except Exception as bstack1l1l1l1lll_opy_:
                            logger.debug(bstack1ll_opy_ (u"ࠧࡇ࠱࠲ࡻ࠽ࠤࡩ࡫ࡦࡢࡷ࡯ࡸࠥࡩ࡯࡯ࡶࡨࡼࡹࠦࡰࡢࡩࡨࠤࡷ࡫ࡵࡴࡧࠣࡪࡦ࡯࡬ࡦࡦࠣࠬࠪࡹࠩ࠭ࠢࡩࡥࡱࡲࡩ࡯ࡩࠣࡦࡦࡩ࡫ࠣ௎"), bstack1l1l1l1lll_opy_)
                            page = _1ll11ll1_opy_(bstack11l111l11l_opy_, *bstack11l1l1ll1l_opy_, **bstack1ll11lll1_opy_)
                    else:
                        page = _1ll11ll1_opy_(bstack11l111l11l_opy_, *bstack11l1l1ll1l_opy_, **bstack1ll11lll1_opy_)
                    try:
                        _w = getattr(threading.current_thread(), bstack1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ௏"), None)
                        if _w and hasattr(_w, bstack1ll_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫࡟ࡱࡣࡪࡩࠬௐ")):
                            _w.update_page(page)
                        if _w and not _w.session_id:
                            try:
                                import json as _json
                                result = page.evaluate(
                                    bstack1ll_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ௑"), bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡪࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡥࡵࡣ࡬ࡰࡸࠨࡽࠨ௒"))
                                if isinstance(result, str):
                                    result = _json.loads(result)
                                if isinstance(result, dict):
                                    sid = result.get(bstack1ll_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭௓")) or result.get(bstack1ll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨ௔")) or result.get(bstack1ll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡏࡤࠨ௕"))
                                    if sid:
                                        import threading as _11111lll11_opy_
                                        from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
                                        with PlaywrightDriverWrapperDirect._session_ids_lock:
                                            PlaywrightDriverWrapperDirect._session_ids[_11111lll11_opy_.get_ident()] = sid
                                        logger.debug(bstack1ll_opy_ (u"ࠨࡃࡢࡲࡷࡹࡷ࡫ࡤࠡࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠥࡼࡩࡢࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠪࡹࠢ௖"), sid)
                                        PlaywrightDriverWrapperDirect._send_cbt_info_on_session()
                                    else:
                                        logger.debug(bstack1ll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲࠡࡩࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡉ࡫ࡴࡢ࡫࡯ࡷࠥࡸࡥࡵࡷࡵࡲࡪࡪࠠ࡯ࡱࠣࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪ࠺ࠡࠧࡶࠦௗ"), result)
                                else:
                                    logger.debug(bstack1ll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠢࡪࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡥࡵࡣ࡬ࡰࡸࠦࡲࡦࡵࡸࡰࡹࡀࠠࠦࡵࠥ௘"), result)
                            except Exception as _1111l1111l_opy_:
                                logger.debug(bstack1ll_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠦࡦࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡸ࡬ࡥࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࠦࡵࠥ௙"), _1111l1111l_opy_)
                        if (getattr(threading.current_thread(), bstack1ll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ௚"), None)
                                and not getattr(threading.current_thread(), bstack1ll_opy_ (u"ࠫࡦ࠷࠱ࡺࡡࡶࡸࡦࡸࡴࡦࡦࠪ௛"), False)):
                            threading.current_thread().a11y_started = True
                            try:
                                from bstack_utils import accessibility as _1l1l111l_opy_
                                bstack11l1111ll1_opy_ = getattr(threading.current_thread(), bstack1ll_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ௜"), True)
                                _1l1l111l_opy_.start_test_capture(_w, bstack11l1111ll1_opy_)
                            except Exception:
                                logger.debug(bstack1ll_opy_ (u"ࠨࡄࡦࡨࡨࡶࡷ࡫ࡤࠡࡃ࠴࠵ࡾࠦࡳࡵࡣࡵࡸࡤࡺࡥࡴࡶࡢࡧࡦࡶࡴࡶࡴࡨࠤ࡫ࡧࡩ࡭ࡧࡧࠦ௝"))
                    except Exception as exc:
                        logger.debug(bstack1ll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡹࡵࡪࡡࡵࡧࠣࡴࡦ࡭ࡥࠡ࡫ࡱࠤࡼࡸࡡࡱࡲࡨࡶ࠿ࠦࠥࡴࠤ௞"), exc)
                    return page
                bstack1llll1l1_opy_.new_page = _1ll111l11_opy_
                bstack1llll1l1_opy_._bstack_new_page_patched = True
        except Exception as exc:
            logger.debug(bstack1ll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡴࡤࡪࠣࡗࡾࡴࡣࡃࡴࡲࡻࡸ࡫ࡲ࠯ࡰࡨࡻࡤࡶࡡࡨࡧࠣࡪࡴࡸࠠࡱࡣࡪࡩࠥࡩࡡࡱࡶࡸࡶࡪࡀࠠࠦࡵࠥ௟"), exc)
        try:
            from playwright.sync_api import Page as bstack1lllll1l1l1_opy_, Browser as _1ll1l1lll1_opy_
            if not hasattr(bstack1lllll1l1l1_opy_, bstack1ll_opy_ (u"ࠩࡢࡦࡸࡺࡡࡤ࡭ࡢࡴࡦ࡭ࡥࡠࡥ࡯ࡳࡸ࡫࡟ࡱࡣࡷࡧ࡭࡫ࡤࠨ௠")):
                _1l1l1l1111_opy_ = bstack1lllll1l1l1_opy_.close
                def _1l11111lll_opy_(bstack1l1lllllll_opy_, *bstack1l1l1ll11l_opy_, _bstack_sdk_close=False, **bstack11l1l1111l_opy_):
                    if not _bstack_sdk_close:
                        logger.debug(bstack1ll_opy_ (u"ࠥࡈࡪ࡬ࡥࡳࡴࡨࡨࠥࡶࡡࡨࡧ࠱ࡧࡱࡵࡳࡦࠪࠬࠤ⠙ࠦࡷࡪ࡮࡯ࠤࡨࡲ࡯ࡴࡧࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢ௡"))
                        threading.current_thread().bstack_deferred_page_close = True
                        threading.current_thread().bstack_deferred_page_ref = bstack1l1lllllll_opy_
                        return
                    return _1l1l1l1111_opy_(bstack1l1lllllll_opy_, *bstack1l1l1ll11l_opy_, **bstack11l1l1111l_opy_)
                bstack1lllll1l1l1_opy_.close = _1l11111lll_opy_
                bstack1lllll1l1l1_opy_._bstack_page_close_patched = True
            if not hasattr(_1ll1l1lll1_opy_, bstack1ll_opy_ (u"ࠫࡤࡨࡳࡵࡣࡦ࡯ࡤࡨࡲࡰࡹࡶࡩࡷࡥࡣ࡭ࡱࡶࡩࡤࡶࡡࡵࡥ࡫ࡩࡩ࠭௢")):
                _11llllllll_opy_ = _1ll1l1lll1_opy_.close
                def _1ll1l111l1_opy_(bstack11l111l11l_opy_, *bstack111111ll1l_opy_, _bstack_sdk_close=False, **bstack1l11l1ll1l_opy_):
                    if not _bstack_sdk_close:
                        logger.debug(bstack1ll_opy_ (u"ࠧࡊࡥࡧࡧࡵࡶࡪࡪࠠࡣࡴࡲࡻࡸ࡫ࡲ࠯ࡥ࡯ࡳࡸ࡫ࠨࠪࠢ⠗ࠤࡼ࡯࡬࡭ࠢࡦࡰࡴࡹࡥࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧ௣"))
                        threading.current_thread().bstack_deferred_browser_close = True
                        threading.current_thread().bstack_deferred_browser_ref = bstack11l111l11l_opy_
                        return
                    return _11llllllll_opy_(bstack11l111l11l_opy_, *bstack111111ll1l_opy_, **bstack1l11l1ll1l_opy_)
                _1ll1l1lll1_opy_.close = _1ll1l111l1_opy_
                _1ll1l1lll1_opy_._bstack_browser_close_patched = True
            if not hasattr(bstack1lllll1l1l1_opy_, bstack1ll_opy_ (u"࠭࡟ࡣࡵࡷࡥࡨࡱ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡣࡵࡧࡴࡤࡪࡨࡨࠬ௤")):
                _1llll1l111_opy_ = bstack1lllll1l1l1_opy_.screenshot
                def _1l1l1l1l11_opy_(bstack1l1lllllll_opy_, *bstack1l111111l1_opy_, **bstack1ll1l1ll1_opy_):
                    result = _1llll1l111_opy_(bstack1l1lllllll_opy_, *bstack1l111111l1_opy_, **bstack1ll1l1ll1_opy_)
                    try:
                        from bstack_utils.testhub_handler import TestHubHandler
                        from bstack_utils.bstack1l1l11l1_opy_ import bstack111l111ll1_opy_
                        if bstack111l111ll1_opy_.on():
                            import base64
                            if isinstance(result, bytes):
                                bstack1llllllll11_opy_ = base64.b64encode(result).decode(bstack1ll_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭௥"))
                            else:
                                bstack1llllllll11_opy_ = str(result)
                            test_uuid = TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack111l111ll1_opy_.current_hook_uuid()
                            if test_uuid and bstack1llllllll11_opy_:
                                TestHubHandler.bstack11l1l1l111_opy_({
                                    bstack1ll_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧ௦"): bstack1llllllll11_opy_,
                                    bstack1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ௧"): test_uuid
                                })
                                logger.debug(bstack1ll_opy_ (u"ࠥࡗࡪࡴࡴࠡࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠢࡷࡳࠥࡕ࠱࠲ࡻࠣࡪࡴࡸࠠࡵࡧࡶࡸࠥࢁࡽࠣ௨").format(test_uuid))
                    except Exception as bstack1lll11ll1l_opy_:
                        logger.debug(bstack1ll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡱࡨࠥࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠦࡴࡰࠢࡒ࠵࠶ࡿ࠺ࠡࡽࢀࠦ௩").format(str(bstack1lll11ll1l_opy_)))
                    return result
                bstack1lllll1l1l1_opy_.screenshot = _1l1l1l1l11_opy_
                bstack1lllll1l1l1_opy_._bstack_screenshot_patched = True
        except Exception as exc:
            logger.debug(bstack1ll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡨࠤࡩ࡫ࡦࡦࡴࡵࡩࡩࠦࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡧࡱࡵࡳࡦࠢ࡫ࡳࡴࡱࡳ࠻ࠢࠨࡷࠧ௪"), exc)
        logger.debug(bstack1ll_opy_ (u"ࠨࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡇࡶ࡮ࡼࡥࡳ࡙ࡵࡥࡵࡶࡥࡳࡆ࡬ࡶࡪࡩࡴࠡࡵࡨࡸࡺࡶࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࠢࡩࡳࡷࠦࡴࡩࡴࡨࡥࡩࠦࡻࡾࠤ௫").format(threading.get_ident()))
    except Exception as e:
        logger.debug(bstack1ll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡷࡳࡣࡳࡴࡪࡸ࠺ࠡࡽࢀࠦ௬").format(str(e)))
    return browser
  async def bstack111ll1lll_opy_(self, *args, **kwargs):
    global bstack11111l11l_opy_, CONFIG, FRAMEWORK_NAME, __version__, BROWSERSTACK_AUTOMATION
    global PLATFORM_INDEX, PARALLELISE_VANILLA_PYTHON, PARALLELISE_THREADING_PYTHON, SESSION_NAME
    import urllib.parse as _1l1ll1l1ll_opy_
    import json
    ws_endpoint = args[0] if args else kwargs.get(bstack1ll_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬ௭"), kwargs.get(bstack1ll_opy_ (u"ࠩࡺࡷࡤ࡫࡮ࡥࡲࡲ࡭ࡳࡺࠧ௮"), bstack1ll_opy_ (u"ࠪࠫ௯")))
    bstack11lllll1l_opy_ = (ws_endpoint
                 and bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧ௰") in str(ws_endpoint)
                 and bstack1ll_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫ௱") in str(ws_endpoint))
    bstack1llll1l11_opy_ = {}
    if bstack11lllll1l_opy_:
        from bstack_utils.helper import bstack1lll1ll1ll_opy_
        bstack1ll111ll11_opy_ = bstack1lll1ll1ll_opy_()
        try:
            if bstack1ll111ll11_opy_:
                CONFIG[bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ௲")] = str(FRAMEWORK_NAME) + str(__version__)
                bstack1l1111l11l_opy_ = os.environ.get(bstack1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ௳"), bstack1ll_opy_ (u"ࠨࠩ௴"))
                if bstack1l1111l11l_opy_:
                    CONFIG[bstack1ll_opy_ (u"ࠩࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬ௵")] = bstack1l1111l11l_opy_
                CONFIG[bstack1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬ௶")] = TestHubUtils.bstack11l11l11l_opy_(CONFIG, FRAMEWORK_NAME)
                bstack11l11ll1_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
                try:
                    if PARALLELISE_VANILLA_PYTHON is True:
                        bstack11l11ll1_opy_ = int(multiprocessing.current_process().name)
                    elif PARALLELISE_THREADING_PYTHON is True:
                        bstack11l11ll1_opy_ = int(threading.current_thread().name)
                except Exception:
                    bstack11l11ll1_opy_ = 0
                CONFIG[bstack1ll_opy_ (u"ࠦ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ௷")] = True
                bstack1llll1l11_opy_ = get_caps(CONFIG, bstack11l11ll1_opy_)
                if CONFIG.get(bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ௸")):
                    update_caps_for_local(bstack1llll1l11_opy_)
                if bstack1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ௹") in CONFIG and bstack1ll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ௺") in CONFIG[bstack1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ௻")][bstack11l11ll1_opy_]:
                    SESSION_NAME = CONFIG[bstack1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ௼")][bstack11l11ll1_opy_][bstack1ll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ௽")]
                logger.debug(bstack1ll_opy_ (u"ࠦࡈࡧࡳࡦࠢࡄ࠾ࠥࡘࡥࡱ࡮ࡤࡧࡪࡪࠠࡶࡵࡨࡶࠥࡩࡡࡱࡵࠣࡻ࡮ࡺࡨࠡࡻࡰࡰࠥࡩࡡࡱࡵ࠽ࠤࢀࢃࠢ௾").format(str(bstack1llll1l11_opy_)))
            else:
                bstack1l1111ll1l_opy_ = str(ws_endpoint).split(bstack1ll_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫ௿"))[1]
                bstack1llll1l11_opy_ = json.loads(_1l1ll1l1ll_opy_.unquote(bstack1l1111ll1l_opy_))
                bstack1llll1l11_opy_ = bstack1llll1l11_opy_ or {}
                bstack1l1111l11l_opy_ = os.environ.get(bstack1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫఀ"), bstack1ll_opy_ (u"ࠧࠨఁ"))
                bstack111ll1l1ll_opy_ = TestHubUtils.bstack11l11l11l_opy_(CONFIG, FRAMEWORK_NAME)
                bstack1llll1l11_opy_[bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩం")] = str(FRAMEWORK_NAME) + str(__version__)
                bstack1llll1l11_opy_[bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪః")] = BROWSERSTACK_AUTOMATION
                if bstack1l1111l11l_opy_:
                    bstack1llll1l11_opy_[bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬఄ")] = bstack1l1111l11l_opy_
                bstack1llll1l11_opy_[bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬఅ")] = bstack111ll1l1ll_opy_
                logger.debug(bstack1ll_opy_ (u"ࠧࡉࡡࡴࡧࠣࡈ࠿ࠦࡍࡦࡴࡪࡩࡩࠦࡓࡅࡍࠣࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࠦࡩ࡯ࡶࡲࠤࡺࡹࡥࡳࠢࡦࡥࡵࡹࠢఆ"))
            ws_url = str(ws_endpoint).split(bstack1ll_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬఇ"))[0]
            ws_endpoint = ws_url + bstack1ll_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭ఈ") + _1l1ll1l1ll_opy_.quote(json.dumps(bstack1llll1l11_opy_))
            if args:
                args = (ws_endpoint,) + args[1:]
            else:
                if bstack1ll_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬఉ") in kwargs:
                    kwargs[bstack1ll_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭ఊ")] = ws_endpoint
                else:
                    kwargs[bstack1ll_opy_ (u"ࠪࡻࡸࡥࡥ࡯ࡦࡳࡳ࡮ࡴࡴࠨఋ")] = ws_endpoint
            logger.debug(bstack1ll_opy_ (u"ࠦࡑ࡫ࡧࡢࡥࡼࠤࡨࡵ࡮࡯ࡧࡦࡸ࡛ࠥࡒࡍࠢࡸࡴࡩࡧࡴࡦࡦࠣࡻ࡮ࡺࡨࠡࡽࢀࠤࡨࡧࡰࡴࠤఌ").format(bstack1ll_opy_ (u"ࠧࡿ࡭࡭ࠤ఍") if bstack1ll111ll11_opy_ else bstack1ll_opy_ (u"ࠨࡴࡦ࡮ࡨࡱࡪࡺࡲࡺࠤఎ")))
        except Exception as e:
            logger.debug(bstack1ll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡪࡸࡧࡦࠢࡦࡥࡵࡹࠠࡪࡰࡷࡳࠥࡩ࡯࡯ࡰࡨࡧࡹࠦࡕࡓࡎ࠽ࠤࢀࢃࠢఏ").format(str(e)))
        try:
            from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
            PlaywrightDriverWrapperDirect.setup_dispatch_capture()
        except Exception as exc:
            logger.debug(bstack1ll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࡶࡲࠣࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠥࡩࡡࡱࡶࡸࡶࡪࠦࡩ࡯ࠢࡰࡳࡩࡥࡣࡰࡰࡱࡩࡨࡺ࠺ࠡࠧࡶࠦఐ"), exc)
    browser = await bstack11111l11l_opy_(self, *args, **kwargs)
    if bstack11lllll1l_opy_:
        try:
            from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
            wrapper = PlaywrightDriverWrapperDirect(browser, page=None, capabilities=bstack1llll1l11_opy_, config=CONFIG)
            threading.current_thread().bstackSessionDriver = wrapper
            logger.debug(bstack1ll_opy_ (u"ࠤࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡊࡲࡪࡸࡨࡶ࡜ࡸࡡࡱࡲࡨࡶࡉ࡯ࡲࡦࡥࡷࠤࡸ࡫ࡴࡶࡲࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࠥ࡬࡯ࡳࠢࡷ࡬ࡷ࡫ࡡࡥࠢࠨࡷࠧ఑"), threading.get_ident())
            threading.current_thread().bstackTestErrorMessages = []
            if wrapper.session_id and not wrapper._cbt_info_sent:
                PlaywrightDriverWrapperDirect._send_cbt_info_on_session()
            try:
                from playwright.sync_api import Browser as bstack1llll1l1_opy_
                if not hasattr(bstack1llll1l1_opy_, bstack1ll_opy_ (u"ࠪࡣࡧࡹࡴࡢࡥ࡮ࡣࡳ࡫ࡷࡠࡲࡤ࡫ࡪࡥࡰࡢࡶࡦ࡬ࡪࡪࠧఒ")):
                    _1ll11ll1_opy_ = bstack1llll1l1_opy_.new_page
                    def _1ll111l11_opy_(bstack11l111l11l_opy_, *bstack11l1l1ll1l_opy_, **bstack1ll11lll1_opy_):
                        page = _1ll11ll1_opy_(bstack11l111l11l_opy_, *bstack11l1l1ll1l_opy_, **bstack1ll11lll1_opy_)
                        try:
                            _w = getattr(threading.current_thread(), bstack1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪఓ"), None)
                            if _w and hasattr(_w, bstack1ll_opy_ (u"ࠬࡻࡰࡥࡣࡷࡩࡤࡶࡡࡨࡧࠪఔ")):
                                _w.update_page(page)
                        except Exception as exc:
                            logger.debug(bstack1ll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡸࡴࡩࡧࡴࡦࠢࡳࡥ࡬࡫ࠠࡪࡰࠣࡻࡷࡧࡰࡱࡧࡵࠤ࠭ࡳ࡯ࡥࡡࡦࡳࡳࡴࡥࡤࡶࠬ࠾ࠥࠫࡳࠣక"), exc)
                        return page
                    bstack1llll1l1_opy_.new_page = _1ll111l11_opy_
                    bstack1llll1l1_opy_._bstack_new_page_patched = True
            except Exception as exc:
                logger.debug(bstack1ll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡺࡣࡩࠢࡖࡽࡳࡩࡂࡳࡱࡺࡷࡪࡸ࠮࡯ࡧࡺࡣࡵࡧࡧࡦࠢ࡬ࡲࠥࡳ࡯ࡥࡡࡦࡳࡳࡴࡥࡤࡶ࠽ࠤࠪࡹࠢఖ"), exc)
            try:
                from playwright.sync_api import Page as bstack1lllll1l1l1_opy_, Browser as _1ll1l1lll1_opy_
                if not hasattr(bstack1lllll1l1l1_opy_, bstack1ll_opy_ (u"ࠨࡡࡥࡷࡹࡧࡣ࡬ࡡࡳࡥ࡬࡫࡟ࡤ࡮ࡲࡷࡪࡥࡰࡢࡶࡦ࡬ࡪࡪࠧగ")):
                    _1l1l1l1111_opy_ = bstack1lllll1l1l1_opy_.close
                    def _1l11111lll_opy_(bstack1l1lllllll_opy_, *bstack1l1l1ll11l_opy_, _bstack_sdk_close=False, **bstack11l1l1111l_opy_):
                        if not _bstack_sdk_close:
                            logger.debug(bstack1ll_opy_ (u"ࠤࡇࡩ࡫࡫ࡲࡳࡧࡧࠤࡵࡧࡧࡦ࠰ࡦࡰࡴࡹࡥࠩࠫࠣ⠘ࠥࡽࡩ࡭࡮ࠣࡧࡱࡵࡳࡦࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨఘ"))
                            threading.current_thread().bstack_deferred_page_close = True
                            threading.current_thread().bstack_deferred_page_ref = bstack1l1lllllll_opy_
                            return
                        return _1l1l1l1111_opy_(bstack1l1lllllll_opy_, *bstack1l1l1ll11l_opy_, **bstack11l1l1111l_opy_)
                    bstack1lllll1l1l1_opy_.close = _1l11111lll_opy_
                    bstack1lllll1l1l1_opy_._bstack_page_close_patched = True
                if not hasattr(_1ll1l1lll1_opy_, bstack1ll_opy_ (u"ࠪࡣࡧࡹࡴࡢࡥ࡮ࡣࡧࡸ࡯ࡸࡵࡨࡶࡤࡩ࡬ࡰࡵࡨࡣࡵࡧࡴࡤࡪࡨࡨࠬఙ")):
                    _11llllllll_opy_ = _1ll1l1lll1_opy_.close
                    def _1ll1l111l1_opy_(bstack11l111l11l_opy_, *bstack111111ll1l_opy_, _bstack_sdk_close=False, **bstack1l11l1ll1l_opy_):
                        if not _bstack_sdk_close:
                            logger.debug(bstack1ll_opy_ (u"ࠦࡉ࡫ࡦࡦࡴࡵࡩࡩࠦࡢࡳࡱࡺࡷࡪࡸ࠮ࡤ࡮ࡲࡷࡪ࠮ࠩࠡ⠖ࠣࡻ࡮ࡲ࡬ࠡࡥ࡯ࡳࡸ࡫ࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦచ"))
                            threading.current_thread().bstack_deferred_browser_close = True
                            threading.current_thread().bstack_deferred_browser_ref = bstack11l111l11l_opy_
                            return
                        return _11llllllll_opy_(bstack11l111l11l_opy_, *bstack111111ll1l_opy_, **bstack1l11l1ll1l_opy_)
                    _1ll1l1lll1_opy_.close = _1ll1l111l1_opy_
                    _1ll1l1lll1_opy_._bstack_browser_close_patched = True
                if not hasattr(bstack1lllll1l1l1_opy_, bstack1ll_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡢࡴࡦࡺࡣࡩࡧࡧࠫఛ")):
                    _1llll1l111_opy_ = bstack1lllll1l1l1_opy_.screenshot
                    def _1l1l1l1l11_opy_(bstack1l1lllllll_opy_, *bstack1l111111l1_opy_, **bstack1ll1l1ll1_opy_):
                        result = _1llll1l111_opy_(bstack1l1lllllll_opy_, *bstack1l111111l1_opy_, **bstack1ll1l1ll1_opy_)
                        try:
                            from bstack_utils.testhub_handler import TestHubHandler
                            from bstack_utils.bstack1l1l11l1_opy_ import bstack111l111ll1_opy_
                            if bstack111l111ll1_opy_.on():
                                import base64
                                if isinstance(result, bytes):
                                    bstack1llllllll11_opy_ = base64.b64encode(result).decode(bstack1ll_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬజ"))
                                else:
                                    bstack1llllllll11_opy_ = str(result)
                                test_uuid = TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack111l111ll1_opy_.current_hook_uuid()
                                if test_uuid and bstack1llllllll11_opy_:
                                    TestHubHandler.bstack11l1l1l111_opy_({
                                        bstack1ll_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭ఝ"): bstack1llllllll11_opy_,
                                        bstack1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨఞ"): test_uuid
                                    })
                        except Exception as bstack1lll11ll1l_opy_:
                            logger.debug(bstack1ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥ࡯ࡦࠣࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠤࡹࡵࠠࡐ࠳࠴ࡽࠥ࠮࡭ࡰࡦࡢࡧࡴࡴ࡮ࡦࡥࡷ࠭࠿ࠦࠥࡴࠤట"), bstack1lll11ll1l_opy_)
                        return result
                    bstack1lllll1l1l1_opy_.screenshot = _1l1l1l1l11_opy_
                    bstack1lllll1l1l1_opy_._bstack_screenshot_patched = True
            except Exception as exc:
                logger.debug(bstack1ll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡦࠢࡧࡩ࡫࡫ࡲࡳࡧࡧࠤࡨࡲ࡯ࡴࡧࠣ࡬ࡴࡵ࡫ࡴࠢ࡬ࡲࠥࡳ࡯ࡥࡡࡦࡳࡳࡴࡥࡤࡶ࠽ࠤࠪࡹࠢఠ"), exc)
            logger.debug(bstack1ll_opy_ (u"ࠦࡑ࡫ࡧࡢࡥࡼࠤࡨࡵ࡮࡯ࡧࡦࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡴࡳࡣࡦ࡯࡮ࡴࡧࠡࡵࡨࡸࡺࡶࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࠢࡩࡳࡷࠦࡴࡩࡴࡨࡥࡩࠦࡻࡾࠤడ").format(threading.get_ident()))
        except Exception as e:
            logger.debug(bstack1ll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠ࡭ࡧࡪࡥࡨࡿࠠࡤࡱࡱࡲࡪࡩࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡷࡶࡦࡩ࡫ࡪࡰࡪ࠾ࠥࢁࡽࠣఢ").format(str(e)))
    return browser
except Exception as e:
    pass
def patch_playwright():
    global SELENIUM_OR_PLAYWRIGHT_INSTALLED
    global FRAMEWORK_NAME
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1lll1ll1ll_opy_
        global bstack11111l11l_opy_
        if not bstack11111l11l_opy_:
            bstack11111l11l_opy_ = BrowserType.connect
        BrowserType.connect = bstack111ll1lll_opy_
        if bstack1lll1ll1ll_opy_():
            BrowserType.launch = bstack1l111l1l1_opy_
            SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
        try:
            from playwright.sync_api._context_manager import PlaywrightContextManager
            if not hasattr(PlaywrightContextManager, bstack1ll_opy_ (u"࠭࡟ࡣࡵࡷࡥࡨࡱ࡟ࡦࡰࡷࡩࡷࡥࡰࡢࡶࡦ࡬ࡪࡪࠧణ")):
                _111l1lllll_opy_ = PlaywrightContextManager.__enter__
                def _1lllll1l1ll_opy_(bstack1llll11l11_opy_):
                    pw = _111l1lllll_opy_(bstack1llll11l11_opy_)
                    _11l1l1ll1_opy_ = pw.stop
                    _1lll111l_opy_ = threading.current_thread()
                    _1lll111l_opy_.bstack_deferred_pw_ref = pw
                    _1lll111l_opy_.bstack_deferred_pw_stop_fn = _11l1l1ll1_opy_
                    def _1lllll1ll11_opy_(*args, _bstack_sdk_close=False, **kwargs):
                        if not _bstack_sdk_close:
                            logger.debug(bstack1ll_opy_ (u"ࠢࡅࡧࡩࡩࡷࡸࡥࡥࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠴ࡳࡵࡱࡳࠬ࠮ࠦ⠔ࠡࡹ࡬ࡰࡱࠦࡳࡵࡱࡳࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣత"))
                            threading.current_thread().bstack_deferred_pw_stop = True
                            return
                        return _11l1l1ll1_opy_()
                    pw.stop = _1lllll1ll11_opy_
                    return pw
                PlaywrightContextManager.__enter__ = _1lllll1l1ll_opy_
                PlaywrightContextManager._bstack_enter_patched = True
        except Exception as e:
            logger.debug(bstack1ll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡴࡤࡪࠣࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࡃࡰࡰࡷࡩࡽࡺࡍࡢࡰࡤ࡫ࡪࡸ࠮ࡠࡡࡨࡲࡹ࡫ࡲࡠࡡ࠽ࠤࠪࡹࠢథ"), e)
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack11l11111l1_opy_
      SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
    except Exception as e:
      pass
def playwright_set_session_name(context, bstack1l11llll1l_opy_):
  try:
    if getattr(context, bstack1ll_opy_ (u"ࠩࡳࡥ࡬࡫ࠧద"), None):
      context.page.evaluate(bstack1ll_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦధ"), bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠨన")+ json.dumps(bstack1l11llll1l_opy_) + bstack1ll_opy_ (u"ࠧࢃࡽࠣ఩"))
  except Exception as e:
    logger.debug(bstack1ll_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡽࢀ࠾ࠥࢁࡽࠣప").format(str(e), traceback.format_exc()))
def playwright_annotate(context, message, level):
  try:
    if getattr(context, bstack1ll_opy_ (u"ࠧࡱࡣࡪࡩࠬఫ"), None):
      context.page.evaluate(bstack1ll_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤబ"), bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧభ") + json.dumps(message) + bstack1ll_opy_ (u"ࠪ࠰ࠧࡲࡥࡷࡧ࡯ࠦ࠿࠭మ") + json.dumps(level) + bstack1ll_opy_ (u"ࠫࢂࢃࠧయ"))
  except Exception as e:
    logger.debug(bstack1ll_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡣࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠥࢁࡽ࠻ࠢࡾࢁࠧర").format(str(e), traceback.format_exc()))
@measure(event_name=EVENTS.bstack11l1ll111l_opy_, stage=STAGE.bstack11llll111l_opy_, bstack111l11111_opy_=SESSION_NAME)
def bstack1l1l11l1l1_opy_(self, url):
  global bstack111l1ll1_opy_
  try:
    bstack1ll1l1llll_opy_(url)
  except Exception as err:
    logger.debug(bstack1ll1ll11_opy_.format(str(err)))
  try:
    bstack111l1ll1_opy_(self, url)
  except Exception as e:
    try:
      parsed_error = str(e)
      if any(err_msg in parsed_error for err_msg in bstack111l111l11_opy_):
        bstack1ll1l1llll_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1ll1ll11_opy_.format(str(err)))
    raise e
def bstack1ll11111l_opy_(self):
  global bstack1l111111l_opy_
  bstack1l111111l_opy_ = self
  return
def bstack1l1lll1l1_opy_(self):
  global bstack1l1l1llll_opy_
  bstack1l1l1llll_opy_ = self
  return
def bstack1l1l1l1l1l_opy_(test_name, bstack111lll1l_opy_):
  global CONFIG
  if percy.bstack11l11ll11l_opy_() == bstack1ll_opy_ (u"ࠨࡴࡳࡷࡨࠦఱ"):
    bstack11l1llll11_opy_ = os.path.relpath(bstack111lll1l_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack11l1llll11_opy_)
    bstack111l11111_opy_ = suite_name + bstack1ll_opy_ (u"ࠢ࠮ࠤల") + test_name
    threading.current_thread().percySessionName = bstack111l11111_opy_
def bstack1lllll111_opy_(self, test, *args, **kwargs):
  global bstack11ll1l1l11_opy_
  test_name = None
  bstack111lll1l_opy_ = None
  if test:
    test_name = str(test.name)
    bstack111lll1l_opy_ = str(test.source)
  bstack1l1l1l1l1l_opy_(test_name, bstack111lll1l_opy_)
  bstack11ll1l1l11_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.bstack11l11l1ll1_opy_, stage=STAGE.bstack11llll111l_opy_, bstack111l11111_opy_=SESSION_NAME)
def bstack1l11lll11_opy_(driver, bstack111l11111_opy_):
  if not bstack11llll1l1l_opy_ and bstack111l11111_opy_:
      bstack1l1lll11ll_opy_ = {
          bstack1ll_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨళ"): bstack1ll_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪఴ"),
          bstack1ll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭వ"): {
              bstack1ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩశ"): bstack111l11111_opy_
          }
      }
      bstack1llll1l1l_opy_ = bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪష").format(json.dumps(bstack1l1lll11ll_opy_))
      driver.execute_script(bstack1llll1l1l_opy_)
  if bstack11ll1l11l1_opy_:
      bstack11111l1l11_opy_ = {
          bstack1ll_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭స"): bstack1ll_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩహ"),
          bstack1ll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ఺"): {
              bstack1ll_opy_ (u"ࠩࡧࡥࡹࡧࠧ఻"): bstack111l11111_opy_ + bstack1ll_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧ఼ࠥࠬ"),
              bstack1ll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪఽ"): bstack1ll_opy_ (u"ࠬ࡯࡮ࡧࡱࠪా")
          }
      }
      if bstack11ll1l11l1_opy_.status == bstack1ll_opy_ (u"࠭ࡐࡂࡕࡖࠫి"):
          bstack11ll11llll_opy_ = bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬీ").format(json.dumps(bstack11111l1l11_opy_))
          driver.execute_script(bstack11ll11llll_opy_)
          bstack1l111l1l1l_opy_(driver, bstack1ll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨు"))
      elif bstack11ll1l11l1_opy_.status == bstack1ll_opy_ (u"ࠩࡉࡅࡎࡒࠧూ"):
          reason = bstack1ll_opy_ (u"ࠥࠦృ")
          bstack111l1ll11l_opy_ = bstack111l11111_opy_ + bstack1ll_opy_ (u"ࠫࠥ࡬ࡡࡪ࡮ࡨࡨࠬౄ")
          if bstack11ll1l11l1_opy_.message:
              reason = str(bstack11ll1l11l1_opy_.message)
              bstack111l1ll11l_opy_ = bstack111l1ll11l_opy_ + bstack1ll_opy_ (u"ࠬࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴ࠽ࠤࠬ౅") + reason
          bstack11111l1l11_opy_[bstack1ll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩె")] = {
              bstack1ll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ే"): bstack1ll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧై"),
              bstack1ll_opy_ (u"ࠩࡧࡥࡹࡧࠧ౉"): bstack111l1ll11l_opy_
          }
          bstack11ll11llll_opy_ = bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨొ").format(json.dumps(bstack11111l1l11_opy_))
          driver.execute_script(bstack11ll11llll_opy_)
          bstack1l111l1l1l_opy_(driver, bstack1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫో"), reason)
          bstack11111ll1ll_opy_(reason, str(bstack11ll1l11l1_opy_), str(PLATFORM_INDEX), logger)
@measure(event_name=EVENTS.bstack1llllll11ll_opy_, stage=STAGE.bstack11llll111l_opy_, bstack111l11111_opy_=SESSION_NAME)
def bstack11l11l11l1_opy_(driver, test):
  if percy.bstack11l11ll11l_opy_() == bstack1ll_opy_ (u"ࠧࡺࡲࡶࡧࠥౌ") and percy.bstack11111l1ll1_opy_() == bstack1ll_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥ్ࠣ"):
      bstack1111l11l1l_opy_ = bstack1llll1lll_opy_(threading.current_thread(), bstack1ll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ౎"), None)
      bstack111l111l1_opy_(driver, bstack1111l11l1l_opy_, test)
  if (bstack1llll1lll_opy_(threading.current_thread(), bstack1ll_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬ౏"), None) and
      bstack1llll1lll_opy_(threading.current_thread(), bstack1ll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ౐"), None)) or (
      bstack1llll1lll_opy_(threading.current_thread(), bstack1ll_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ౑"), None) and
      bstack1llll1lll_opy_(threading.current_thread(), bstack1ll_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭౒"), None)):
      logger.info(bstack1ll_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠣࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡷࡱࡨࡪࡸࡷࡢࡻ࠱ࠤࠧ౓"))
      a11y.bstack1111l111_opy_(driver, name=test.name, path=test.source)
def bstack11ll1l111_opy_(test, bstack111l11111_opy_):
    try:
      bstack1l1111ll_opy_ = datetime.datetime.now()
      data = {}
      if test:
        data[bstack1ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ౔")] = bstack111l11111_opy_
      if bstack11ll1l11l1_opy_:
        if bstack11ll1l11l1_opy_.status == bstack1ll_opy_ (u"ࠧࡑࡃࡖࡗౕࠬ"):
          data[bstack1ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨౖ")] = bstack1ll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ౗")
        elif bstack11ll1l11l1_opy_.status == bstack1ll_opy_ (u"ࠪࡊࡆࡏࡌࠨౘ"):
          data[bstack1ll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫౙ")] = bstack1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬౚ")
          if bstack11ll1l11l1_opy_.message:
            data[bstack1ll_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭౛")] = str(bstack11ll1l11l1_opy_.message)
      user = CONFIG[bstack1ll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ౜")]
      key = CONFIG[bstack1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫౝ")]
      host = bstack11lll111ll_opy_(cli.config, [bstack1ll_opy_ (u"ࠤࡤࡴ࡮ࡹࠢ౞"), bstack1ll_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷࡩࠧ౟"), bstack1ll_opy_ (u"ࠦࡦࡶࡩࠣౠ")], bstack1ll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡱ࡫࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࠨౡ"))
      url = bstack1ll_opy_ (u"࠭ࡻࡾ࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡸ࡫ࡳࡴ࡫ࡲࡲࡸ࠵ࡻࡾ࠰࡭ࡷࡴࡴࠧౢ").format(host, bstack11ll11l1_opy_)
      headers = {
        bstack1ll_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭ౣ"): bstack1ll_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ౤"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers, auth=(user, key))
        cli.bstack1lll11ll11_opy_(bstack1ll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺ࡶࡲࡧࡥࡹ࡫࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡳࡵࡣࡷࡹࡸࠨ౥"), datetime.datetime.now() - bstack1l1111ll_opy_)
    except Exception as e:
      logger.error(bstack11ll111l1_opy_.format(str(e)))
def bstack1l1l11llll_opy_(test, bstack111l11111_opy_):
  global CONFIG
  global bstack1l1l1llll_opy_
  global bstack1l111111l_opy_
  global bstack11ll11l1_opy_
  global bstack11ll1l11l1_opy_
  global SESSION_NAME
  global bstack111ll11ll1_opy_
  global bstack11lll11ll1_opy_
  global bstack11l1l1l1_opy_
  global bstack111l111l1l_opy_
  global bstack1ll111ll1l_opy_
  global bstack1l1l1l111l_opy_
  global bstack1l111l11ll_opy_
  try:
    if not bstack11ll11l1_opy_:
      with bstack1l111l11ll_opy_:
        bstack111l1lll_opy_ = os.path.join(os.path.expanduser(bstack1ll_opy_ (u"ࠪࢂࠬ౦")), bstack1ll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ౧"), bstack1ll_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧ౨"))
        if os.path.exists(bstack111l1lll_opy_):
          with open(bstack111l1lll_opy_, bstack1ll_opy_ (u"࠭ࡲࠨ౩")) as f:
            content = f.read().strip()
            if content:
              bstack1ll11111l1_opy_ = json.loads(bstack1ll_opy_ (u"ࠢࡼࠤ౪") + content + bstack1ll_opy_ (u"ࠨࠤࡻࠦ࠿ࠦࠢࡺࠤࠪ౫") + bstack1ll_opy_ (u"ࠤࢀࠦ౬"))
              bstack11ll11l1_opy_ = bstack1ll11111l1_opy_.get(str(threading.get_ident()))
  except Exception as e:
    logger.debug(bstack1ll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡵࡩࡦࡪࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡎࡊࡳࠡࡨ࡬ࡰࡪࡀࠠࠨ౭") + str(e))
  if not is_robot_playwright_installed():
    if bstack1ll111ll1l_opy_:
      with bstack111l1111_opy_:
        bstack111ll1l1_opy_ = bstack1ll111ll1l_opy_.copy()
      for driver in bstack111ll1l1_opy_:
        if bstack11ll11l1_opy_ == driver.session_id:
          if test:
            bstack11l11l11l1_opy_(driver, test)
          bstack1l11lll11_opy_(driver, bstack111l11111_opy_)
    elif bstack11ll11l1_opy_:
      bstack11ll1l111_opy_(test, bstack111l11111_opy_)
    if bstack1l1l1llll_opy_:
      bstack11lll11ll1_opy_(bstack1l1l1llll_opy_)
    if bstack1l111111l_opy_:
      bstack11l1l1l1_opy_(bstack1l111111l_opy_)
    if bstack1ll1111ll_opy_:
      bstack111l111l1l_opy_()
def bstack1ll1llll_opy_(self, test, *args, **kwargs):
  bstack111l11111_opy_ = None
  if test:
    bstack111l11111_opy_ = str(test.name)
  bstack1l1l11llll_opy_(test, bstack111l11111_opy_)
  bstack111ll11ll1_opy_(self, test, *args, **kwargs)
def bstack1l1lll111l_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1ll1l1ll_opy_
  global CONFIG
  global bstack1ll111ll1l_opy_
  global bstack11ll11l1_opy_
  global bstack1l111l11ll_opy_
  bstack11lll111_opy_ = None
  try:
    if bstack1llll1lll_opy_(threading.current_thread(), bstack1ll_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ౮"), None) or bstack1llll1lll_opy_(threading.current_thread(), bstack1ll_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ౯"), None):
      try:
        if not bstack11ll11l1_opy_:
          bstack111l1lll_opy_ = os.path.join(os.path.expanduser(bstack1ll_opy_ (u"࠭ࡾࠨ౰")), bstack1ll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ౱"), bstack1ll_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪ౲"))
          with bstack1l111l11ll_opy_:
            if os.path.exists(bstack111l1lll_opy_):
              with open(bstack111l1lll_opy_, bstack1ll_opy_ (u"ࠩࡵࠫ౳")) as f:
                content = f.read().strip()
                if content:
                  bstack1ll11111l1_opy_ = json.loads(bstack1ll_opy_ (u"ࠥࡿࠧ౴") + content + bstack1ll_opy_ (u"ࠫࠧࡾࠢ࠻ࠢࠥࡽࠧ࠭౵") + bstack1ll_opy_ (u"ࠧࢃࠢ౶"))
                  bstack11ll11l1_opy_ = bstack1ll11111l1_opy_.get(str(threading.get_ident()))
      except Exception as e:
        logger.debug(bstack1ll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡸࡥࡢࡦ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡊࡆࡶࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥࡺࡥࡴࡶࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࠬ౷") + str(e))
      if bstack1ll111ll1l_opy_:
        with bstack111l1111_opy_:
          bstack111ll1l1_opy_ = bstack1ll111ll1l_opy_.copy()
        for driver in bstack111ll1l1_opy_:
          if bstack11ll11l1_opy_ == driver.session_id:
            bstack11lll111_opy_ = driver
    bstack11l1111ll1_opy_ = a11y.is_enabled_testcase(test.tags)
    if bstack11lll111_opy_:
      threading.current_thread().isA11yTest = a11y.start_test_capture(bstack11lll111_opy_, bstack11l1111ll1_opy_)
      threading.current_thread().isAppA11yTest = a11y.start_test_capture(bstack11lll111_opy_, bstack11l1111ll1_opy_)
    else:
      threading.current_thread().isA11yTest = bstack11l1111ll1_opy_
      threading.current_thread().isAppA11yTest = bstack11l1111ll1_opy_
  except:
    pass
  bstack1ll1l1ll_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack11ll1l11l1_opy_
  try:
    bstack11ll1l11l1_opy_ = self._test
  except:
    bstack11ll1l11l1_opy_ = self.test
def bstack111ll1lll1_opy_():
  global bstack1l1ll1l1l1_opy_
  try:
    if os.path.exists(bstack1l1ll1l1l1_opy_):
      os.remove(bstack1l1ll1l1l1_opy_)
  except Exception as e:
    logger.debug(bstack1ll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪ౸") + str(e))
def bstack1l1l11ll1l_opy_():
  global bstack1l1ll1l1l1_opy_
  bstack1111l1l1_opy_ = {}
  lock_file = bstack1l1ll1l1l1_opy_ + bstack1ll_opy_ (u"ࠨ࠰࡯ࡳࡨࡱࠧ౹")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1ll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡬ࡰࡥ࡮ࠤࡳࡵࡴࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨ࠰ࠥࡻࡳࡪࡰࡪࠤࡧࡧࡳࡪࡥࠣࡪ࡮ࡲࡥࠡࡱࡳࡩࡷࡧࡴࡪࡱࡱࡷࠬ౺"))
    try:
      if not os.path.isfile(bstack1l1ll1l1l1_opy_):
        with open(bstack1l1ll1l1l1_opy_, bstack1ll_opy_ (u"ࠪࡻࠬ౻")) as f:
          json.dump({}, f)
      if os.path.exists(bstack1l1ll1l1l1_opy_):
        with open(bstack1l1ll1l1l1_opy_, bstack1ll_opy_ (u"ࠫࡷ࠭౼")) as f:
          content = f.read().strip()
          if content:
            bstack1111l1l1_opy_ = json.loads(content)
    except Exception as e:
      logger.debug(bstack1ll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡳࡧࡤࡨ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧ౽") + str(e))
    return bstack1111l1l1_opy_
  try:
    os.makedirs(os.path.dirname(bstack1l1ll1l1l1_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      if not os.path.isfile(bstack1l1ll1l1l1_opy_):
        with open(bstack1l1ll1l1l1_opy_, bstack1ll_opy_ (u"࠭ࡷࠨ౾")) as f:
          json.dump({}, f)
      if os.path.exists(bstack1l1ll1l1l1_opy_):
        with open(bstack1l1ll1l1l1_opy_, bstack1ll_opy_ (u"ࠧࡳࠩ౿")) as f:
          content = f.read().strip()
          if content:
            bstack1111l1l1_opy_ = json.loads(content)
  except Exception as e:
    logger.debug(bstack1ll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡶࡪࡧࡤࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪಀ") + str(e))
  finally:
    return bstack1111l1l1_opy_
def bstack1l1ll1l111_opy_(platform_index, item_index):
  global bstack1l1ll1l1l1_opy_
  lock_file = bstack1l1ll1l1l1_opy_ + bstack1ll_opy_ (u"ࠩ࠱ࡰࡴࡩ࡫ࠨಁ")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1ll_opy_ (u"ࠪࡪ࡮ࡲࡥ࡭ࡱࡦ࡯ࠥࡴ࡯ࡵࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩ࠱ࠦࡵࡴ࡫ࡱ࡫ࠥࡨࡡࡴ࡫ࡦࠤ࡫࡯࡬ࡦࠢࡲࡴࡪࡸࡡࡵ࡫ࡲࡲࡸ࠭ಂ"))
    try:
      bstack1111l1l1_opy_ = {}
      if os.path.exists(bstack1l1ll1l1l1_opy_):
        with open(bstack1l1ll1l1l1_opy_, bstack1ll_opy_ (u"ࠫࡷ࠭ಃ")) as f:
          content = f.read().strip()
          if content:
            bstack1111l1l1_opy_ = json.loads(content)
      bstack1111l1l1_opy_[item_index] = platform_index
      with open(bstack1l1ll1l1l1_opy_, bstack1ll_opy_ (u"ࠧࡽࠢ಄")) as outfile:
        json.dump(bstack1111l1l1_opy_, outfile)
    except Exception as e:
      logger.debug(bstack1ll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡹࡵ࡭ࡹ࡯࡮ࡨࠢࡷࡳࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫಅ") + str(e))
    return
  try:
    os.makedirs(os.path.dirname(bstack1l1ll1l1l1_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      bstack1111l1l1_opy_ = {}
      if os.path.exists(bstack1l1ll1l1l1_opy_):
        with open(bstack1l1ll1l1l1_opy_, bstack1ll_opy_ (u"ࠧࡳࠩಆ")) as f:
          content = f.read().strip()
          if content:
            bstack1111l1l1_opy_ = json.loads(content)
      bstack1111l1l1_opy_[item_index] = platform_index
      with open(bstack1l1ll1l1l1_opy_, bstack1ll_opy_ (u"ࠣࡹࠥಇ")) as outfile:
        json.dump(bstack1111l1l1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1ll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡼࡸࡩࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧಈ") + str(e))
def bstack1l1l111ll_opy_(bstack1ll1l1lll_opy_):
  global CONFIG
  bstack1llllll11l_opy_ = bstack1ll_opy_ (u"ࠪࠫಉ")
  if not bstack1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧಊ") in CONFIG:
    logger.info(bstack1ll_opy_ (u"ࠬࡔ࡯ࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠤࡵࡧࡳࡴࡧࡧࠤࡺࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡨࡧࡱࡩࡷࡧࡴࡦࠢࡵࡩࡵࡵࡲࡵࠢࡩࡳࡷࠦࡒࡰࡤࡲࡸࠥࡸࡵ࡯ࠩಋ"))
  try:
    platform = CONFIG[bstack1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩಌ")][bstack1ll1l1lll_opy_]
    if bstack1ll_opy_ (u"ࠧࡰࡵࠪ಍") in platform:
      bstack1llllll11l_opy_ += str(platform[bstack1ll_opy_ (u"ࠨࡱࡶࠫಎ")]) + bstack1ll_opy_ (u"ࠩ࠯ࠤࠬಏ")
    if bstack1ll_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ಐ") in platform:
      bstack1llllll11l_opy_ += str(platform[bstack1ll_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧ಑")]) + bstack1ll_opy_ (u"ࠬ࠲ࠠࠨಒ")
    if bstack1ll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪಓ") in platform:
      bstack1llllll11l_opy_ += str(platform[bstack1ll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫಔ")]) + bstack1ll_opy_ (u"ࠨ࠮ࠣࠫಕ")
    if bstack1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫಖ") in platform:
      bstack1llllll11l_opy_ += str(platform[bstack1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬಗ")]) + bstack1ll_opy_ (u"ࠫ࠱ࠦࠧಘ")
    if bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪಙ") in platform:
      bstack1llllll11l_opy_ += str(platform[bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫಚ")]) + bstack1ll_opy_ (u"ࠧ࠭ࠢࠪಛ")
    if bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩಜ") in platform:
      bstack1llllll11l_opy_ += str(platform[bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪಝ")]) + bstack1ll_opy_ (u"ࠪ࠰ࠥ࠭ಞ")
  except Exception as e:
    logger.debug(bstack1ll_opy_ (u"ࠫࡘࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡴࡧࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡷࡹࡸࡩ࡯ࡩࠣࡪࡴࡸࠠࡳࡧࡳࡳࡷࡺࠠࡨࡧࡱࡩࡷࡧࡴࡪࡱࡱࠫಟ") + str(e))
  finally:
    if bstack1llllll11l_opy_[len(bstack1llllll11l_opy_) - 2:] == bstack1ll_opy_ (u"ࠬ࠲ࠠࠨಠ"):
      bstack1llllll11l_opy_ = bstack1llllll11l_opy_[:-2]
    return bstack1llllll11l_opy_
def bstack1l11ll1ll1_opy_(path, bstack1llllll11l_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1l1l1lll1l_opy_ = ET.parse(path)
    bstack111ll1l11_opy_ = bstack1l1l1lll1l_opy_.getroot()
    bstack1111111l1_opy_ = None
    for suite in bstack111ll1l11_opy_.iter(bstack1ll_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬಡ")):
      if bstack1ll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧಢ") in suite.attrib:
        suite.attrib[bstack1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ಣ")] += bstack1ll_opy_ (u"ࠩࠣࠫತ") + bstack1llllll11l_opy_
        bstack1111111l1_opy_ = suite
    bstack1ll1l11lll_opy_ = None
    for robot in bstack111ll1l11_opy_.iter(bstack1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩಥ")):
      bstack1ll1l11lll_opy_ = robot
    bstack11l11l11_opy_ = len(bstack1ll1l11lll_opy_.findall(bstack1ll_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪದ")))
    if bstack11l11l11_opy_ == 1:
      bstack1ll1l11lll_opy_.remove(bstack1ll1l11lll_opy_.findall(bstack1ll_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫಧ"))[0])
      bstack1ll11l1ll1_opy_ = ET.Element(bstack1ll_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬನ"), attrib={bstack1ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ಩"): bstack1ll_opy_ (u"ࠨࡕࡸ࡭ࡹ࡫ࡳࠨಪ"), bstack1ll_opy_ (u"ࠩ࡬ࡨࠬಫ"): bstack1ll_opy_ (u"ࠪࡷ࠵࠭ಬ")})
      bstack1ll1l11lll_opy_.insert(1, bstack1ll11l1ll1_opy_)
      bstack111ll11ll_opy_ = None
      for suite in bstack1ll1l11lll_opy_.iter(bstack1ll_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪಭ")):
        bstack111ll11ll_opy_ = suite
      bstack111ll11ll_opy_.append(bstack1111111l1_opy_)
      bstack1l1111l11_opy_ = None
      for status in bstack1111111l1_opy_.iter(bstack1ll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬಮ")):
        bstack1l1111l11_opy_ = status
      bstack111ll11ll_opy_.append(bstack1l1111l11_opy_)
    bstack1l1l1lll1l_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1ll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡶࡸ࡯࡮ࡨࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡱ࡫ࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠫಯ") + str(e))
def bstack11ll1l1l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack11l1l11l1_opy_
  global CONFIG
  if bstack1ll_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡰࡢࡶ࡫ࠦರ") in options:
    del options[bstack1ll_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡱࡣࡷ࡬ࠧಱ")]
  json_data = bstack1l1l11ll1l_opy_()
  for item_id in json_data.keys():
    path = os.path.join(outs_dir, str(item_id), bstack1ll_opy_ (u"ࠩࡲࡹࡹࡶࡵࡵ࠰ࡻࡱࡱ࠭ಲ"))
    bstack1l11ll1ll1_opy_(path, bstack1l1l111ll_opy_(json_data[item_id]))
  bstack111ll1lll1_opy_()
  return bstack11l1l11l1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack11l11111_opy_(self, ff_profile_dir):
  global bstack11ll1l1lll_opy_
  if not ff_profile_dir:
    return None
  return bstack11ll1l1lll_opy_(self, ff_profile_dir)
def bstack11l11l111l_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1lll1111l1_opy_
  bstack111l11l11l_opy_ = []
  if bstack1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ಳ") in CONFIG:
    bstack111l11l11l_opy_ = CONFIG[bstack1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ಴")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1ll_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࠨವ")],
      pabot_args[bstack1ll_opy_ (u"ࠨࡶࡦࡴࡥࡳࡸ࡫ࠢಶ")],
      argfile,
      pabot_args.get(bstack1ll_opy_ (u"ࠢࡩ࡫ࡹࡩࠧಷ")),
      pabot_args[bstack1ll_opy_ (u"ࠣࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠦಸ")],
      platform[0],
      bstack1lll1111l1_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1ll_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡪ࡮ࡲࡥࡴࠤಹ")] or [(bstack1ll_opy_ (u"ࠥࠦ಺"), None)]
    for platform in enumerate(bstack111l11l11l_opy_)
  ]
def bstack1lll111lll_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1l11l111l_opy_=bstack1ll_opy_ (u"ࠫࠬ಻")):
  global bstack1ll1llll1l_opy_
  self.platform_index = platform_index
  self.bstack111l11l1l_opy_ = bstack1l11l111l_opy_
  bstack1ll1llll1l_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1ll1l11l1_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1l1ll1lll_opy_
  global bstack1l111ll1_opy_
  bstack1l11111l_opy_ = copy.deepcopy(item)
  if not bstack1ll_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫಼ࠧ") in item.options:
    bstack1l11111l_opy_.options[bstack1ll_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨಽ")] = []
  bstack1l11l11l11_opy_ = bstack1l11111l_opy_.options[bstack1ll_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩಾ")].copy()
  for v in bstack1l11111l_opy_.options[bstack1ll_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪಿ")]:
    if bstack1ll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘࠨೀ") in v:
      bstack1l11l11l11_opy_.remove(v)
    if bstack1ll_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡆࡐࡎࡇࡒࡈࡕࠪು") in v:
      bstack1l11l11l11_opy_.remove(v)
    if bstack1ll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨೂ") in v:
      bstack1l11l11l11_opy_.remove(v)
  bstack1l11l11l11_opy_.insert(0, bstack1ll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡕࡒࡁࡕࡈࡒࡖࡒࡏࡎࡅࡇ࡛࠾ࢀࢃࠧೃ").format(bstack1l11111l_opy_.platform_index))
  bstack1l11l11l11_opy_.insert(0, bstack1ll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔ࠽ࡿࢂ࠭ೄ").format(bstack1l11111l_opy_.bstack111l11l1l_opy_))
  bstack1l11111l_opy_.options[bstack1ll_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ೅")] = bstack1l11l11l11_opy_
  if bstack1l111ll1_opy_:
    bstack1l11111l_opy_.options[bstack1ll_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪೆ")].insert(0, bstack1ll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡅࡏࡍࡆࡘࡇࡔ࠼ࡾࢁࠬೇ").format(bstack1l111ll1_opy_))
  return bstack1l1ll1lll_opy_(caller_id, datasources, is_last, bstack1l11111l_opy_, outs_dir)
def bstack1l1lllll1_opy_(command, item_index):
  try:
    if global_config.get_property(bstack1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫೈ")):
      os.environ[bstack1ll_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬ೉")] = json.dumps(CONFIG[bstack1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨೊ")][item_index % bstack1l11ll11l1_opy_])
    global bstack1l111ll1_opy_
    os.environ[bstack1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ೋ")] = str(item_index % bstack1l11ll11l1_opy_)
    listener_arg = bstack1ll_opy_ (u"ࠧࠨೌ")
    if is_robot_playwright_installed() and cli.is_enabled(CONFIG):
      listener_arg = bstack1ll_opy_ (u"ࠨࠢ࠰࠱ࡱ࡯ࡳࡵࡧࡱࡩࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡹࡤ࡬࠰ࡵࡳࡧࡵࡴࡠ࡮࡬ࡷࡹ࡫࡮ࡦࡴࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠮ࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡔࡦࡺࡣࡩࡧࡵ್ࠫ")
      logger.debug(bstack1ll_opy_ (u"ࠤࡄࡨࡩ࡯࡮ࡨࠢࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡖࡡࡵࡥ࡫ࡩࡷࠦ࡬ࡪࡵࡷࡩࡳ࡫ࡲࠡࡨࡲࡶࠥ࡯ࡴࡦ࡯ࠣࡿࢂࠨ೎").format(item_index))
    bstack111lll1lll_opy_ = bstack1ll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡶࡨࡰࠦࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠠ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࠣࠦ೏") + \
              str(item_index % bstack1l11ll11l1_opy_) + \
              bstack1ll_opy_ (u"ࠦࠥ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠤࠧ೐") + \
              str(item_index) + \
              listener_arg
    if bstack1l111ll1_opy_:
        bstack111lll1lll_opy_ += bstack1ll_opy_ (u"ࠧࠦࠢ೑") + bstack1l111ll1_opy_
    command[0:1] = bstack111lll1lll_opy_.split()
  except Exception as e:
    logger.error(bstack1ll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡳ࡯ࡥ࡫ࡩࡽ࡮ࡴࡧࠡࡥࡲࡱࡲࡧ࡮ࡥࠢࡩࡳࡷࠦࡰࡢࡤࡲࡸࠥࡸࡵ࡯࠼ࠣࡿࢂ࠭೒").format(str(e)))
def bstack1l11l1l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack11l111lll_opy_
  try:
    bstack1l1lllll1_opy_(command, item_index)
    return bstack11l111lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
  except Exception as e:
    logger.error(bstack1ll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡧࡵࡴࠡࡴࡸࡲ࠿ࠦࡻࡾࠩ೓").format(str(e)))
    raise e
def bstack1111ll1lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack11l111lll_opy_
  try:
    bstack1l1lllll1_opy_(command, item_index)
    return bstack11l111lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
  except Exception as e:
    logger.error(bstack1ll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡦࡨ࡯ࡵࠢࡵࡹࡳࠦ࠲࠯࠳࠶࠾ࠥࢁࡽࠨ೔").format(str(e)))
    try:
      return bstack11l111lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
    except Exception as e2:
      logger.error(bstack1ll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡢࡰࡶࠣ࠶࠳࠷࠳ࠡࡨࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࢀࢃࠧೕ").format(str(e2)))
      raise e
def bstack11lll1llll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack11l111lll_opy_
  try:
    bstack1l1lllll1_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    return bstack11l111lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
  except Exception as e:
    logger.error(bstack1ll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡣࡱࡷࠤࡷࡻ࡮ࠡ࠴࠱࠵࠺ࡀࠠࡼࡿࠪೖ").format(str(e)))
    try:
      return bstack11l111lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
    except Exception as e2:
      logger.error(bstack1ll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡢࡤࡲࡸࠥ࠸࠮࠲࠷ࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࡻࡾࠩ೗").format(str(e2)))
      raise e
def _1ll11l1lll_opy_(bstack1ll11l1l_opy_, item_index, process_timeout, sleep_before_start, bstack1l111l11l1_opy_):
  bstack1l1lllll1_opy_(bstack1ll11l1l_opy_, item_index)
  if process_timeout is None:
    process_timeout = 3600
  if sleep_before_start and sleep_before_start > 0:
    time.sleep(min(sleep_before_start, 5))
  return process_timeout
def bstack1llll1ll11_opy_(command, bstack1111111l11_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack11l111lll_opy_
  global bstack1l11111l1_opy_
  global bstack1l111ll1_opy_
  try:
    for env_name, bstack11l1ll1l1l_opy_ in bstack1l11111l1_opy_.items():
      os.environ[env_name] = bstack11l1ll1l1l_opy_
    bstack1l111ll1_opy_ = bstack1ll_opy_ (u"ࠧࠨ೘")
    bstack1l1lllll1_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    if sleep_before_start and sleep_before_start > 0:
      time.sleep(min(sleep_before_start, 5))
    return bstack11l111lll_opy_(command, bstack1111111l11_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack1ll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠࡳࡷࡱࠤ࠺࠴࠰࠻ࠢࡾࢁࠬ೙").format(str(e)))
    try:
      return bstack11l111lll_opy_(command, bstack1111111l11_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack1ll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡧࡵࡴࠡࡨࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࢀࢃࠧ೚").format(str(e2)))
      raise e
def bstack111lllll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack11l111lll_opy_
  try:
    process_timeout = _1ll11l1lll_opy_(command, item_index, process_timeout, sleep_before_start, bstack1ll_opy_ (u"ࠨ࠶࠱࠶ࠬ೛"))
    return bstack11l111lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack1ll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡢࡰࡶࠣࡶࡺࡴࠠ࠵࠰࠵࠾ࠥࢁࡽࠨ೜").format(str(e)))
    try:
      return bstack11l111lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack1ll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡣࡱࡷࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࡼࡿࠪೝ").format(str(e2)))
      raise e
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack11111l111_opy_(self, runner, quiet=False, capture=True):
  global bstack1lllll1ll_opy_
  bstack1l1ll1111_opy_ = bstack1lllll1ll_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack1ll_opy_ (u"ࠫࡪࡾࡣࡦࡲࡷ࡭ࡴࡴ࡟ࡢࡴࡵࠫೞ")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1ll_opy_ (u"ࠬ࡫ࡸࡤࡡࡷࡶࡦࡩࡥࡣࡣࡦ࡯ࡤࡧࡲࡳࠩ೟")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1l1ll1111_opy_
def bstack111111lll_opy_(runner, hook_name, context, element, bstack111ll111_opy_, *args):
  global bstack111l1l11_opy_
  try:
    if runner.hooks.get(hook_name):
      bstack1ll111l11l_opy_.bstack1111111l1l_opy_(hook_name, element)
    if bstack111l1l11_opy_ is None or bstack111l1l11_opy_:
      bstack111ll111_opy_(runner, hook_name, context, *args)
    else:
      bstack1l1111111_opy_ = (context,) + args
      bstack111ll111_opy_(runner, hook_name, *bstack1l1111111_opy_)
    if runner.hooks.get(hook_name):
      bstack1ll111l11l_opy_.bstack1lllllllll1_opy_(element)
      if hook_name not in [bstack1ll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠪೠ"), bstack1ll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪೡ")] and args and hasattr(args[0], bstack1ll_opy_ (u"ࠨࡧࡵࡶࡴࡸ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠨೢ")):
        args[0].error_message = bstack1ll_opy_ (u"ࠩࠪೣ")
  except Exception as e:
    logger.debug(bstack1ll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡨࡢࡰࡧࡰࡪࠦࡨࡰࡱ࡮ࡷࠥ࡯࡮ࠡࡤࡨ࡬ࡦࡼࡥ࠻ࠢࡾࢁࠬ೤").format(str(e)))
@measure(event_name=EVENTS.bstack1l1ll1ll11_opy_, stage=STAGE.bstack11llll111l_opy_, hook_type=bstack1ll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡅࡱࡲࠢ೥"), bstack111l11111_opy_=SESSION_NAME)
def bstack111llllll1_opy_(runner, name, context, bstack111ll111_opy_, *args):
    if runner.hooks.get(bstack1ll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤ೦")).__name__ != bstack1ll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࡢࡨࡪ࡬ࡡࡶ࡮ࡷࡣ࡭ࡵ࡯࡬ࠤ೧"):
      bstack111111lll_opy_(runner, name, context, runner, bstack111ll111_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack11ll11111_opy_(bstack1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭೨")) else context.browser
      runner.driver_initialised = bstack1ll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧ೩")
    except Exception as e:
      logger.debug(bstack1ll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡧࡶ࡮ࡼࡥࡳࠢ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡷࡪࠦࡡࡵࡶࡵ࡭ࡧࡻࡴࡦ࠼ࠣࡿࢂ࠭೪").format(str(e)))
def bstack1lll1ll1l_opy_(runner, name, context, bstack111ll111_opy_, *args):
    bstack111111lll_opy_(runner, name, context, context.feature, bstack111ll111_opy_, *args)
    try:
      if not bstack11llll1l1l_opy_:
        bstack11lll111_opy_ = threading.current_thread().bstackSessionDriver if bstack11ll11111_opy_(bstack1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ೫")) else context.browser
        if is_driver_active(bstack11lll111_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack1ll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠧ೬")
          bstack1l11llll1l_opy_ = str(runner.feature.name)
          playwright_set_session_name(context, bstack1l11llll1l_opy_)
          bstack11lll111_opy_.execute_script(bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ೭") + json.dumps(bstack1l11llll1l_opy_) + bstack1ll_opy_ (u"࠭ࡽࡾࠩ೮"))
    except Exception as e:
      logger.debug(bstack1ll_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧ೯").format(str(e)))
def bstack11l1l111_opy_(runner, name, context, bstack111ll111_opy_, *args):
    target = context.scenario if hasattr(context, bstack1ll_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪ೰")) else context.feature
    bstack111111lll_opy_(runner, name, context, target, bstack111ll111_opy_, *args)
@measure(event_name=EVENTS.bstack1l111111_opy_, stage=STAGE.bstack11llll111l_opy_, bstack111l11111_opy_=SESSION_NAME)
def bstack11lll1ll1l_opy_(runner, name, context, bstack111ll111_opy_, *args):
    bstack1ll111l11l_opy_.start_test(context)
    bstack111111lll_opy_(runner, name, context, context.scenario, bstack111ll111_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack1l11lll1l_opy_.bstack1ll1llll11_opy_(context, *args)
    try:
      bstack11lll111_opy_ = bstack1llll1lll_opy_(threading.current_thread(), bstack1ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨೱ"), context.browser)
      if is_driver_active(bstack11lll111_opy_):
        TestHubHandler.send_cbt_info(bstack1llll1lll_opy_(threading.current_thread(), bstack1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩೲ"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack1ll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨೳ")
        if (not bstack11llll1l1l_opy_):
          scenario_name = args[0].name
          feature_name = bstack1l11llll1l_opy_ = str(runner.feature.name)
          bstack1l11llll1l_opy_ = feature_name + bstack1ll_opy_ (u"ࠬࠦ࠭ࠡࠩ೴") + scenario_name
          if runner.driver_initialised == bstack1ll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣ೵"):
            playwright_set_session_name(context, bstack1l11llll1l_opy_)
            bstack11lll111_opy_.execute_script(bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬ೶") + json.dumps(bstack1l11llll1l_opy_) + bstack1ll_opy_ (u"ࠨࡿࢀࠫ೷"))
    except Exception as e:
      logger.debug(bstack1ll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡ࡫ࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡀࠠࡼࡿࠪ೸").format(str(e)))
@measure(event_name=EVENTS.bstack1l1ll1ll11_opy_, stage=STAGE.bstack11llll111l_opy_, hook_type=bstack1ll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡖࡸࡪࡶࠢ೹"), bstack111l11111_opy_=SESSION_NAME)
def bstack1l111l11_opy_(runner, name, context, bstack111ll111_opy_, *args):
    bstack111111lll_opy_(runner, name, context, args[0], bstack111ll111_opy_, *args)
    try:
      bstack11lll111_opy_ = threading.current_thread().bstackSessionDriver if bstack11ll11111_opy_(bstack1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ೺")) else context.browser
      if is_driver_active(bstack11lll111_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack1ll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥ೻")
        bstack1ll111l11l_opy_.bstack1l111ll1l1_opy_(args[0])
        if runner.driver_initialised == bstack1ll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦ೼") and not bstack11llll1l1l_opy_:
          feature_name = bstack1l11llll1l_opy_ = str(runner.feature.name)
          bstack1l11llll1l_opy_ = feature_name + bstack1ll_opy_ (u"ࠧࠡ࠯ࠣࠫ೽") + context.scenario.name
          playwright_set_session_name(context, bstack1l11llll1l_opy_)
          bstack11lll111_opy_.execute_script(bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭೾") + json.dumps(bstack1l11llll1l_opy_) + bstack1ll_opy_ (u"ࠩࢀࢁࠬ೿"))
    except Exception as e:
      logger.debug(bstack1ll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡴࡦࡲ࠽ࠤࢀࢃࠧഀ").format(str(e)))
@measure(event_name=EVENTS.bstack1l1ll1ll11_opy_, stage=STAGE.bstack11llll111l_opy_, hook_type=bstack1ll_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࡖࡸࡪࡶࠢഁ"), bstack111l11111_opy_=SESSION_NAME)
def bstack1ll1l11ll1_opy_(runner, name, context, bstack111ll111_opy_, *args):
  bstack1ll111l11l_opy_.bstack1llllll11l1_opy_(args[0])
  try:
    step_status = args[0].status.name
    bstack11lll111_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫം") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack11lll111_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack1ll_opy_ (u"࠭ࡩ࡯ࡵࡷࡩࡵ࠭ഃ")
        if not bstack11llll1l1l_opy_:
          feature_name = bstack1l11llll1l_opy_ = str(runner.feature.name)
          bstack1l11llll1l_opy_ = feature_name + bstack1ll_opy_ (u"ࠧࠡ࠯ࠣࠫഄ") + context.scenario.name
          playwright_set_session_name(context, bstack1l11llll1l_opy_)
          bstack11lll111_opy_.execute_script(bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭അ") + json.dumps(bstack1l11llll1l_opy_) + bstack1ll_opy_ (u"ࠩࢀࢁࠬആ"))
    if str(step_status).lower() in [bstack1ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪഇ"), bstack1ll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪഈ")]:
      bstack111l11ll_opy_ = bstack1ll_opy_ (u"ࠬ࠭ഉ")
      bstack11ll1ll11l_opy_ = bstack1ll_opy_ (u"࠭ࠧഊ")
      bstack1llllll111_opy_ = bstack1ll_opy_ (u"ࠧࠨഋ")
      try:
        import traceback
        bstack111l11ll_opy_ = runner.exception.__class__.__name__
        bstack111ll1ll11_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack11ll1ll11l_opy_ = bstack1ll_opy_ (u"ࠨࠢࠪഌ").join(bstack111ll1ll11_opy_)
        bstack1llllll111_opy_ = bstack111ll1ll11_opy_[-1]
      except Exception as e:
        logger.debug(bstack111111lll1_opy_.format(str(e)))
      bstack111l11ll_opy_ += bstack1llllll111_opy_
      playwright_annotate(context, json.dumps(str(args[0].name) + bstack1ll_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣ഍") + str(bstack11ll1ll11l_opy_)),
                          bstack1ll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤഎ"))
      if runner.driver_initialised == bstack1ll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤഏ"):
        bstack11lllll11l_opy_(getattr(context, bstack1ll_opy_ (u"ࠬࡶࡡࡨࡧࠪഐ"), None), bstack1ll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ഑"), bstack111l11ll_opy_)
        bstack11lll111_opy_.execute_script(bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬഒ") + json.dumps(str(args[0].name) + bstack1ll_opy_ (u"ࠣࠢ࠰ࠤࡋࡧࡩ࡭ࡧࡧࠥࡡࡴࠢഓ") + str(bstack11ll1ll11l_opy_)) + bstack1ll_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࡽࡾࠩഔ"))
      if runner.driver_initialised == bstack1ll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣക"):
        bstack1l111l1l1l_opy_(bstack11lll111_opy_, bstack1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫഖ"), bstack1ll_opy_ (u"࡙ࠧࡣࡦࡰࡤࡶ࡮ࡵࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤഗ") + str(bstack111l11ll_opy_))
    else:
      playwright_annotate(context, bstack1ll_opy_ (u"ࠨࡐࡢࡵࡶࡩࡩࠧࠢഘ"), bstack1ll_opy_ (u"ࠢࡪࡰࡩࡳࠧങ"))
      if runner.driver_initialised == bstack1ll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨച"):
        bstack11lllll11l_opy_(getattr(context, bstack1ll_opy_ (u"ࠩࡳࡥ࡬࡫ࠧഛ"), None), bstack1ll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥജ"))
      bstack11lll111_opy_.execute_script(bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩഝ") + json.dumps(str(args[0].name) + bstack1ll_opy_ (u"ࠧࠦ࠭ࠡࡒࡤࡷࡸ࡫ࡤࠢࠤഞ")) + bstack1ll_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤࢀࢁࠬട"))
      if runner.driver_initialised == bstack1ll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧഠ"):
        bstack1l111l1l1l_opy_(bstack11lll111_opy_, bstack1ll_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣഡ"))
  except Exception as e:
    logger.debug(bstack1ll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡳࡵࡧࡳ࠾ࠥࢁࡽࠨഢ").format(str(e)))
  bstack111111lll_opy_(runner, name, context, args[0], bstack111ll111_opy_, *args)
@measure(event_name=EVENTS.bstack11ll11l1l_opy_, stage=STAGE.bstack11llll111l_opy_, bstack111l11111_opy_=SESSION_NAME)
def bstack1ll11lll11_opy_(runner, name, context, bstack111ll111_opy_, *args):
  bstack1ll111l11l_opy_.end_test(args[0])
  try:
    bstack1111l1llll_opy_ = args[0].status.name
    bstack11lll111_opy_ = bstack1llll1lll_opy_(threading.current_thread(), bstack1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩണ"), context.browser)
    bstack1l11lll1l_opy_.bstack11111lllll_opy_(bstack11lll111_opy_)
    if str(bstack1111l1llll_opy_).lower() in [bstack1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫത"), bstack1ll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫഥ")]:
      bstack111l11ll_opy_ = bstack1ll_opy_ (u"࠭ࠧദ")
      bstack11ll1ll11l_opy_ = bstack1ll_opy_ (u"ࠧࠨധ")
      bstack1llllll111_opy_ = bstack1ll_opy_ (u"ࠨࠩന")
      try:
        import traceback
        bstack111l11ll_opy_ = runner.exception.__class__.__name__
        bstack111ll1ll11_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack11ll1ll11l_opy_ = bstack1ll_opy_ (u"ࠩࠣࠫഩ").join(bstack111ll1ll11_opy_)
        bstack1llllll111_opy_ = bstack111ll1ll11_opy_[-1]
      except Exception as e:
        logger.debug(bstack111111lll1_opy_.format(str(e)))
      bstack111l11ll_opy_ += bstack1llllll111_opy_
      playwright_annotate(context, json.dumps(str(args[0].name) + bstack1ll_opy_ (u"ࠥࠤ࠲ࠦࡆࡢ࡫࡯ࡩࡩࠧ࡜࡯ࠤപ") + str(bstack11ll1ll11l_opy_)),
                          bstack1ll_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥഫ"))
      if runner.driver_initialised == bstack1ll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢബ") or runner.driver_initialised == bstack1ll_opy_ (u"࠭ࡩ࡯ࡵࡷࡩࡵ࠭ഭ"):
        bstack11lllll11l_opy_(getattr(context, bstack1ll_opy_ (u"ࠧࡱࡣࡪࡩࠬമ"), None), bstack1ll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣയ"), bstack111l11ll_opy_)
        bstack11lll111_opy_.execute_script(bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧര") + json.dumps(str(args[0].name) + bstack1ll_opy_ (u"ࠥࠤ࠲ࠦࡆࡢ࡫࡯ࡩࡩࠧ࡜࡯ࠤറ") + str(bstack11ll1ll11l_opy_)) + bstack1ll_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣࡿࢀࠫല"))
      if runner.driver_initialised == bstack1ll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢള") or runner.driver_initialised == bstack1ll_opy_ (u"࠭ࡩ࡯ࡵࡷࡩࡵ࠭ഴ"):
        bstack1l111l1l1l_opy_(bstack11lll111_opy_, bstack1ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧവ"), bstack1ll_opy_ (u"ࠣࡕࡦࡩࡳࡧࡲࡪࡱࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧശ") + str(bstack111l11ll_opy_))
    else:
      playwright_annotate(context, bstack1ll_opy_ (u"ࠤࡓࡥࡸࡹࡥࡥࠣࠥഷ"), bstack1ll_opy_ (u"ࠥ࡭ࡳ࡬࡯ࠣസ"))
      if runner.driver_initialised == bstack1ll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨഹ") or runner.driver_initialised == bstack1ll_opy_ (u"ࠬ࡯࡮ࡴࡶࡨࡴࠬഺ"):
        bstack11lllll11l_opy_(getattr(context, bstack1ll_opy_ (u"࠭ࡰࡢࡩࡨ഻ࠫ"), None), bstack1ll_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪ഼ࠢ"))
      bstack11lll111_opy_.execute_script(bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ഽ") + json.dumps(str(args[0].name) + bstack1ll_opy_ (u"ࠤࠣ࠱ࠥࡖࡡࡴࡵࡨࡨࠦࠨാ")) + bstack1ll_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩി"))
      if runner.driver_initialised == bstack1ll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨീ") or runner.driver_initialised == bstack1ll_opy_ (u"ࠬ࡯࡮ࡴࡶࡨࡴࠬു"):
        bstack1l111l1l1l_opy_(bstack11lll111_opy_, bstack1ll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨൂ"))
  except Exception as e:
    logger.debug(bstack1ll_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩൃ").format(str(e)))
  bstack111111lll_opy_(runner, name, context, context.scenario, bstack111ll111_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack1l1l11l1l_opy_(runner, name, context, bstack111ll111_opy_, *args):
    target = context.scenario if hasattr(context, bstack1ll_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪൄ")) else context.feature
    bstack111111lll_opy_(runner, name, context, target, bstack111ll111_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack1l11l11l1_opy_(runner, name, context, bstack111ll111_opy_, *args):
    try:
      bstack11lll111_opy_ = bstack1llll1lll_opy_(threading.current_thread(), bstack1ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ൅"), context.browser)
      bstack1ll111111l_opy_ = bstack1ll_opy_ (u"ࠪࠫെ")
      if context.failed is True:
        bstack111lll1ll1_opy_ = []
        bstack11111l1l1_opy_ = []
        bstack1llllll111l_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack111lll1ll1_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack111ll1ll11_opy_ = traceback.format_tb(exc_tb)
            bstack1l1llll1ll_opy_ = bstack1ll_opy_ (u"ࠫࠥ࠭േ").join(bstack111ll1ll11_opy_)
            bstack11111l1l1_opy_.append(bstack1l1llll1ll_opy_)
            bstack1llllll111l_opy_.append(bstack111ll1ll11_opy_[-1])
        except Exception as e:
          logger.debug(bstack111111lll1_opy_.format(str(e)))
        bstack111l11ll_opy_ = bstack1ll_opy_ (u"ࠬ࠭ൈ")
        for i in range(len(bstack111lll1ll1_opy_)):
          bstack111l11ll_opy_ += bstack111lll1ll1_opy_[i] + bstack1llllll111l_opy_[i] + bstack1ll_opy_ (u"࠭࡜࡯ࠩ൉")
        bstack1ll111111l_opy_ = bstack1ll_opy_ (u"ࠧࠡࠩൊ").join(bstack11111l1l1_opy_)
        if runner.driver_initialised in [bstack1ll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠤോ"), bstack1ll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨൌ")]:
          playwright_annotate(context, bstack1ll111111l_opy_, bstack1ll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤ്"))
          bstack11lllll11l_opy_(getattr(context, bstack1ll_opy_ (u"ࠫࡵࡧࡧࡦࠩൎ"), None), bstack1ll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ൏"), bstack111l11ll_opy_)
          bstack11lll111_opy_.execute_script(bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ൐") + json.dumps(bstack1ll111111l_opy_) + bstack1ll_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦࢂࢃࠧ൑"))
          bstack1l111l1l1l_opy_(bstack11lll111_opy_, bstack1ll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ൒"), bstack1ll_opy_ (u"ࠤࡖࡳࡲ࡫ࠠࡴࡥࡨࡲࡦࡸࡩࡰࡵࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࡡࡴࠢ൓") + str(bstack111l11ll_opy_))
          bstack1111ll1l1_opy_ = bstack11l11llll1_opy_(bstack1ll111111l_opy_, runner.feature.name, logger)
          if (bstack1111ll1l1_opy_ != None):
            bstack1l1ll1ll1_opy_.append(bstack1111ll1l1_opy_)
      else:
        if runner.driver_initialised in [bstack1ll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦൔ"), bstack1ll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣൕ")]:
          playwright_annotate(context, bstack1ll_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࡀࠠࠣൖ") + str(runner.feature.name) + bstack1ll_opy_ (u"ࠨࠠࡱࡣࡶࡷࡪࡪࠡࠣൗ"), bstack1ll_opy_ (u"ࠢࡪࡰࡩࡳࠧ൘"))
          bstack11lllll11l_opy_(getattr(context, bstack1ll_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭൙"), None), bstack1ll_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ൚"))
          bstack11lll111_opy_.execute_script(bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨ൛") + json.dumps(bstack1ll_opy_ (u"ࠦࡋ࡫ࡡࡵࡷࡵࡩ࠿ࠦࠢ൜") + str(runner.feature.name) + bstack1ll_opy_ (u"ࠧࠦࡰࡢࡵࡶࡩࡩࠧࠢ൝")) + bstack1ll_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤࢀࢁࠬ൞"))
          bstack1l111l1l1l_opy_(bstack11lll111_opy_, bstack1ll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧൟ"))
          bstack1111ll1l1_opy_ = bstack11l11llll1_opy_(bstack1ll111111l_opy_, runner.feature.name, logger)
          if (bstack1111ll1l1_opy_ != None):
            bstack1l1ll1ll1_opy_.append(bstack1111ll1l1_opy_)
    except Exception as e:
      logger.debug(bstack1ll_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࠥ࡬ࡥࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪൠ").format(str(e)))
    bstack111111lll_opy_(runner, name, context, context.feature, bstack111ll111_opy_, *args)
@measure(event_name=EVENTS.bstack1l1ll1ll11_opy_, stage=STAGE.bstack11llll111l_opy_, hook_type=bstack1ll_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࡂ࡮࡯ࠦൡ"), bstack111l11111_opy_=SESSION_NAME)
def bstack111ll1l11l_opy_(runner, name, context, bstack111ll111_opy_, *args):
    bstack111111lll_opy_(runner, name, context, runner, bstack111ll111_opy_, *args)
def bstack1lll11ll1_opy_(self, filename=None):
  global bstack11l11ll1l_opy_
  bstack11l11ll1l_opy_(self, filename)
  bstack111l1l11l_opy_ = []
  bstack11l1l1ll11_opy_ = [bstack1ll_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠫൢ"), bstack1ll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡹࡧࡧࠨൣ"), bstack1ll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧ൤"), bstack1ll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧ൥"), bstack1ll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡴࡢࡩࠪ൦"), bstack1ll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨ൧")]
  bstack111ll11lll_opy_ = lambda *_: None
  for hook_name in bstack11l1l1ll11_opy_:
    if hook_name not in self.hooks:
      self.hooks[hook_name] = bstack111ll11lll_opy_
      bstack111l1l11l_opy_.append(hook_name)
  if bstack111l1l11l_opy_:
    os.environ[bstack1ll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡖࡈࡐࡥࡄࡆࡈࡄ࡙ࡑ࡚࡟ࡉࡑࡒࡏࡘ࠭൨")] = bstack1ll_opy_ (u"ࠪ࠰ࠬ൩").join(bstack111l1l11l_opy_)
def _execute_deferred_playwright_close():
  try:
    _1lll111l_opy_ = threading.current_thread()
    _1l1l1l11ll_opy_ = getattr(_1lll111l_opy_, bstack1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡩ࡫ࡦࡦࡴࡵࡩࡩࡥࡰࡢࡩࡨࡣࡷ࡫ࡦࠨ൪"), None)
    _11111l1l1l_opy_ = getattr(_1lll111l_opy_, bstack1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡪࡥࡧࡧࡵࡶࡪࡪ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡠࡴࡨࡪࠬ൫"), None)
    _111l1l1l_opy_ = getattr(_1lll111l_opy_, bstack1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡤࡦࡨࡨࡶࡷ࡫ࡤࡠࡲࡺࡣࡸࡺ࡯ࡱࡡࡩࡲࠬ൬"), None)
    _wrapper = getattr(_1lll111l_opy_, bstack1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭൭"), None)
    if not _11111l1l1l_opy_ and _wrapper and hasattr(_wrapper, bstack1ll_opy_ (u"ࠨࡡࡥࡶࡴࡽࡳࡦࡴࠪ൮")):
      _11111l1l1l_opy_ = _wrapper._browser
    if not _1l1l1l11ll_opy_ and _wrapper and hasattr(_wrapper, bstack1ll_opy_ (u"ࠩࡢࡴࡦ࡭ࡥࠨ൯")):
      _1l1l1l11ll_opy_ = _wrapper._page
    if not _111l1l1l_opy_:
      _11llllll1l_opy_ = getattr(_1lll111l_opy_, bstack1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡨࡪ࡬ࡥࡳࡴࡨࡨࡤࡶࡷࡠࡴࡨࡪࠬ൰"), None)
      if _11llllll1l_opy_ and hasattr(_11llllll1l_opy_, bstack1ll_opy_ (u"ࠫࡸࡺ࡯ࡱࠩ൱")):
        _111l1l1l_opy_ = _11llllll1l_opy_.stop
    _1l1111l1ll_opy_ = _1l1l1l11ll_opy_ or _11111l1l1l_opy_ or _111l1l1l_opy_
    if not _1l1111l1ll_opy_:
      return
    if _1l1l1l11ll_opy_ and hasattr(_1l1l1l11ll_opy_, bstack1ll_opy_ (u"ࠬࡩ࡬ࡰࡵࡨࠫ൲")):
      try:
        _1l1l1l11ll_opy_.close(_bstack_sdk_close=True)
      except TypeError:
        try:
          _1l1l1l11ll_opy_.close()
        except Exception:
          pass
      except Exception as e:
        logger.debug(bstack1ll_opy_ (u"࠭ࡄࡦࡨࡨࡶࡷ࡫ࡤࠡࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡶࡡࡨࡧ࠱ࡧࡱࡵࡳࡦࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡿࢂ࠭൳").format(str(e)))
    if _11111l1l1l_opy_ and hasattr(_11111l1l1l_opy_, bstack1ll_opy_ (u"ࠧࡤ࡮ࡲࡷࡪ࠭൴")):
      try:
        _11111l1l1l_opy_.close(_bstack_sdk_close=True)
      except TypeError:
        try:
          _11111l1l1l_opy_.close()
        except Exception:
          pass
      except Exception as e:
        logger.debug(bstack1ll_opy_ (u"ࠨࡆࡨࡪࡪࡸࡲࡦࡦࠣࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡣࡴࡲࡻࡸ࡫ࡲ࠯ࡥ࡯ࡳࡸ࡫ࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡽࢀࠫ൵").format(str(e)))
    if _111l1l1l_opy_:
      try:
        _111l1l1l_opy_(_bstack_sdk_close=True)
      except TypeError:
        try:
          _111l1l1l_opy_()
        except Exception:
          pass
      except Exception as e:
        logger.debug(bstack1ll_opy_ (u"ࠩࡇࡩ࡫࡫ࡲࡳࡧࡧࠤࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡷࡳࡵࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࡼࡿࠪ൶").format(str(e)))
    for attr in (bstack1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡨࡪ࡬ࡥࡳࡴࡨࡨࡤࡶࡡࡨࡧࡢࡧࡱࡵࡳࡦࠩ൷"), bstack1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡩ࡫ࡦࡦࡴࡵࡩࡩࡥࡰࡢࡩࡨࡣࡷ࡫ࡦࠨ൸"),
                 bstack1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡪࡥࡧࡧࡵࡶࡪࡪ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡠࡥ࡯ࡳࡸ࡫ࠧ൹"), bstack1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡤࡦࡨࡨࡶࡷ࡫ࡤࡠࡤࡵࡳࡼࡹࡥࡳࡡࡵࡩ࡫࠭ൺ"),
                 bstack1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡥࡧࡩࡩࡷࡸࡥࡥࡡࡳࡻࡤࡹࡴࡰࡲࠪൻ"), bstack1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡦࡨࡪࡪࡸࡲࡦࡦࡢࡴࡼࡥࡳࡵࡱࡳࡣ࡫ࡴࠧർ"),
                 bstack1ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡧࡩ࡫࡫ࡲࡳࡧࡧࡣࡵࡽ࡟ࡳࡧࡩࠫൽ")):
      try:
        delattr(_1lll111l_opy_, attr)
      except AttributeError:
        pass
    if _wrapper:
      try:
        _wrapper._page = None
        _wrapper._browser = None
      except Exception:
        pass
    logger.debug(bstack1ll_opy_ (u"ࠪࡈࡪ࡬ࡥࡳࡴࡨࡨࠥࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡦࡰࡴࡹࡥࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠤ࡫ࡵࡲࠡࡶ࡫ࡶࡪࡧࡤࠡࡽࢀࠫൾ").format(_1lll111l_opy_.ident))
  except Exception as e:
    logger.debug(bstack1ll_opy_ (u"ࠫࡉ࡫ࡦࡦࡴࡵࡩࡩࠦࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡧࡱࡵࡳࡦࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡿࢂ࠭ൿ").format(str(e)))
def bstack1lll11l1l_opy_(self, name, *args):
  global bstack111ll111_opy_
  global bstack111l1l11_opy_
  try:
    if BROWSERSTACK_AUTOMATION:
      platform_index = int(threading.current_thread()._name) % bstack1l11ll11l1_opy_
      bstack11llll1ll_opy_ = CONFIG[bstack1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ඀")][platform_index]
      os.environ[bstack1ll_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧඁ")] = json.dumps(bstack11llll1ll_opy_)
    if not hasattr(self, bstack1ll_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡨࡨࠬං")):
      self.driver_initialised = None
    bstack1ll1lllll1_opy_ = {
        bstack1ll_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠬඃ"): bstack111llllll1_opy_,
        bstack1ll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠪ඄"): bstack1lll1ll1l_opy_,
        bstack1ll_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡸࡦ࡭ࠧඅ"): bstack11l1l111_opy_,
        bstack1ll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ආ"): bstack11lll1ll1l_opy_,
        bstack1ll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠪඇ"): bstack1l111l11_opy_,
        bstack1ll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡴࡦࡲࠪඈ"): bstack1ll1l11ll1_opy_,
        bstack1ll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨඉ"): bstack1ll11lll11_opy_,
        bstack1ll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡵࡣࡪࠫඊ"): bstack1l1l11l1l_opy_,
        bstack1ll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠩඋ"): bstack1l11l11l1_opy_,
        bstack1ll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ࠭ඌ"): bstack111ll1l11l_opy_
    }
    handler = bstack1ll1lllll1_opy_.get(name, bstack111ll111_opy_)
    try:
      if args:
        context = args[0]
        remaining_args = args[1:]
        if bstack111l1l11_opy_ is None or not bstack111l1l11_opy_:
          context = self.context
          remaining_args = args
      else:
        context = self.context
        remaining_args = ()
      handler(self, name, context, bstack111ll111_opy_, *remaining_args)
    except Exception as e:
      logger.debug(bstack1ll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡢࡦࡪࡤࡺࡪࠦࡨࡰࡱ࡮ࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶࠥࢁࡽ࠻ࠢࡾࢁࠬඍ").format(name, str(e)))
    if name == bstack1ll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ඎ"):
      _execute_deferred_playwright_close()
    if name in [bstack1ll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ඏ"), bstack1ll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨඐ"), bstack1ll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠫඑ")]:
      try:
        bstack11lll111_opy_ = threading.current_thread().bstackSessionDriver if bstack11ll11111_opy_(bstack1ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨඒ")) else context.browser
        bstack1111l1l1l_opy_ = (
          (name == bstack1ll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ࠭ඓ") and self.driver_initialised == bstack1ll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣඔ")) or
          (name == bstack1ll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬඕ") and self.driver_initialised == bstack1ll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠢඖ")) or
          (name == bstack1ll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨ඗") and self.driver_initialised in [bstack1ll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥ඘"), bstack1ll_opy_ (u"ࠤ࡬ࡲࡸࡺࡥࡱࠤ඙")]) or
          (name == bstack1ll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡸࡪࡶࠧක") and self.driver_initialised == bstack1ll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤඛ"))
        )
        if bstack1111l1l1l_opy_:
          self.driver_initialised = None
          if bstack11lll111_opy_ and hasattr(bstack11lll111_opy_, bstack1ll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠩග")):
            try:
              bstack11lll111_opy_.quit()
            except Exception as e:
              logger.debug(bstack1ll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡷࡵࡪࡶࡷ࡭ࡳ࡭ࠠࡥࡴ࡬ࡺࡪࡸࠠࡪࡰࠣࡦࡪ࡮ࡡࡷࡧࠣ࡬ࡴࡵ࡫࠻ࠢࡾࢁࠬඝ").format(str(e)))
      except Exception as e:
        logger.debug(bstack1ll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࠡࡪࡲࡳࡰࠦࡣ࡭ࡧࡤࡲࡺࡶࠠࡧࡱࡵࠤࢀࢃ࠺ࠡࡽࢀࠫඞ").format(name, str(e)))
  except Exception as e:
    logger.debug(bstack1ll_opy_ (u"ࠨࡅࡵ࡭ࡹ࡯ࡣࡢ࡮ࠣࡩࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡨࡥࡩࡣࡹࡩࠥࡸࡵ࡯ࠢ࡫ࡳࡴࡱࠠࡼࡿ࠽ࠤࢀࢃࠧඟ").format(name, str(e)))
    try:
      if bstack111l1l11_opy_ is None or bstack111l1l11_opy_:
        try:
          bstack111ll111_opy_(self, name, self.context, *args)
        except TypeError:
          bstack111ll111_opy_(self, name, *args)
      else:
        bstack111ll111_opy_(self, name, *args)
    except Exception as e2:
      logger.debug(bstack1ll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࠦ࡯ࡳ࡫ࡪ࡭ࡳࡧ࡬ࠡࡤࡨ࡬ࡦࡼࡥࠡࡪࡲࡳࡰࠦࡻࡾ࠼ࠣࡿࢂ࠭ච").format(name, str(e2)))
  finally:
    if name == bstack1ll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫඡ"):
      _execute_deferred_playwright_close()
def bstack1llllllll1l_opy_(config, startdir):
  return bstack1ll_opy_ (u"ࠦࡩࡸࡩࡷࡧࡵ࠾ࠥࢁ࠰ࡾࠤජ").format(bstack1ll_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦඣ"))
notset = Notset()
def bstack11ll1l11_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1ll1l111ll_opy_
  if str(name).lower() == bstack1ll_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷ࠭ඤ"):
    return bstack1ll_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨඥ")
  else:
    return bstack1ll1l111ll_opy_(self, name, default, skip)
def bstack1lll111l11_opy_(item, when):
  global bstack11l111l1ll_opy_
  try:
    bstack11l111l1ll_opy_(item, when)
  except Exception as e:
    pass
def bstack1l1l1l1l1_opy_():
  return
def bstack1l1lll1lll_opy_(type, name, status, reason, bstack1llllll1l_opy_, bstack1l1l11l111_opy_):
  bstack1l1lll11ll_opy_ = {
    bstack1ll_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨඦ"): type,
    bstack1ll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬට"): {}
  }
  if type == bstack1ll_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬඨ"):
    bstack1l1lll11ll_opy_[bstack1ll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧඩ")][bstack1ll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫඪ")] = bstack1llllll1l_opy_
    bstack1l1lll11ll_opy_[bstack1ll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩණ")][bstack1ll_opy_ (u"ࠧࡥࡣࡷࡥࠬඬ")] = json.dumps(str(bstack1l1l11l111_opy_))
  if type == bstack1ll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩත"):
    bstack1l1lll11ll_opy_[bstack1ll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬථ")][bstack1ll_opy_ (u"ࠪࡲࡦࡳࡥࠨද")] = name
  if type == bstack1ll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧධ"):
    bstack1l1lll11ll_opy_[bstack1ll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨන")][bstack1ll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭඲")] = status
    if status == bstack1ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧඳ"):
      bstack1l1lll11ll_opy_[bstack1ll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫප")][bstack1ll_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩඵ")] = json.dumps(str(reason))
  bstack1llll1l1l_opy_ = bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨබ").format(json.dumps(bstack1l1lll11ll_opy_))
  return bstack1llll1l1l_opy_
def bstack1ll1lll1l1_opy_(driver_command, response):
    if driver_command == bstack1ll_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨභ"):
        TestHubHandler.bstack11l1l1l111_opy_({
            bstack1ll_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫම"): response[bstack1ll_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬඹ")],
            bstack1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧය"): TestHubHandler.current_test_uuid()
        })
def bstack111ll1111l_opy_(item, call, rep):
  global bstack1ll111l1l_opy_
  global bstack1ll111ll1l_opy_
  global bstack11llll1l1l_opy_
  name = bstack1ll_opy_ (u"ࠨࠩර")
  try:
    if rep.when == bstack1ll_opy_ (u"ࠩࡦࡥࡱࡲࠧ඼"):
      bstack11ll11l1_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack11llll1l1l_opy_:
          name = str(rep.nodeid)
          bstack1lll11ll_opy_ = bstack1l1lll1lll_opy_(bstack1ll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫල"), name, bstack1ll_opy_ (u"ࠫࠬ඾"), bstack1ll_opy_ (u"ࠬ࠭඿"), bstack1ll_opy_ (u"࠭ࠧව"), bstack1ll_opy_ (u"ࠧࠨශ"))
          threading.current_thread().bstack1l11ll11ll_opy_ = name
          for driver in bstack1ll111ll1l_opy_:
            if bstack11ll11l1_opy_ == driver.session_id:
              driver.execute_script(bstack1lll11ll_opy_)
      except Exception as e:
        logger.debug(bstack1ll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨෂ").format(str(e)))
      try:
        bstack11ll1lll_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack1ll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪස"):
          status = bstack1ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪහ") if rep.outcome.lower() == bstack1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫළ") else bstack1ll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬෆ")
          reason = bstack1ll_opy_ (u"࠭ࠧ෇")
          if status == bstack1ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ෈"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack1ll_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭෉") if status == bstack1ll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥ්ࠩ") else bstack1ll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ෋")
          data = name + bstack1ll_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭෌") if status == bstack1ll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ෍") else name + bstack1ll_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠡࠡࠩ෎") + reason
          bstack1ll11lll_opy_ = bstack1l1lll1lll_opy_(bstack1ll_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩා"), bstack1ll_opy_ (u"ࠨࠩැ"), bstack1ll_opy_ (u"ࠩࠪෑ"), bstack1ll_opy_ (u"ࠪࠫි"), level, data)
          for driver in bstack1ll111ll1l_opy_:
            if bstack11ll11l1_opy_ == driver.session_id:
              driver.execute_script(bstack1ll11lll_opy_)
      except Exception as e:
        logger.debug(bstack1ll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡥࡲࡲࡹ࡫ࡸࡵࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨී").format(str(e)))
  except Exception as e:
    logger.debug(bstack1ll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡵࡷࡥࡹ࡫ࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻࡾࠩු").format(str(e)))
  bstack1ll111l1l_opy_(item, call, rep)
def bstack111l111l1_opy_(driver, bstack1111111111_opy_, test=None):
  global PLATFORM_INDEX
  if test != None:
    bstack11ll1lllll_opy_ = getattr(test, bstack1ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ෕"), None)
    bstack1l111l1ll1_opy_ = getattr(test, bstack1ll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬූ"), None)
    PercySDK.screenshot(driver, bstack1111111111_opy_, bstack11ll1lllll_opy_=bstack11ll1lllll_opy_, bstack1l111l1ll1_opy_=bstack1l111l1ll1_opy_, bstack1ll1ll1l1l_opy_=PLATFORM_INDEX)
  else:
    PercySDK.screenshot(driver, bstack1111111111_opy_)
@measure(event_name=EVENTS.bstack1l11lllll_opy_, stage=STAGE.bstack11llll111l_opy_, bstack111l11111_opy_=SESSION_NAME)
def bstack1111l1l111_opy_(driver):
  if bstack111ll11l11_opy_.bstack111111111l_opy_() is True or bstack111ll11l11_opy_.capturing() is True:
    return
  bstack111ll11l11_opy_.bstack11111l1lll_opy_()
  while not bstack111ll11l11_opy_.bstack111111111l_opy_():
    bstack1111l1l11_opy_ = bstack111ll11l11_opy_.bstack111l111ll_opy_()
    bstack111l111l1_opy_(driver, bstack1111l1l11_opy_)
  bstack111ll11l11_opy_.bstack11l11ll1ll_opy_()
def bstack1l1111llll_opy_(sequence, driver_command, response = None, bstack11l111ll11_opy_ = None, args = None):
    try:
      if sequence != bstack1ll_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨ෗"):
        return
      if percy.bstack11l11ll11l_opy_() == bstack1ll_opy_ (u"ࠤࡩࡥࡱࡹࡥࠣෘ"):
        return
      bstack1111l1l11_opy_ = bstack1llll1lll_opy_(threading.current_thread(), bstack1ll_opy_ (u"ࠪࡴࡪࡸࡣࡺࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ෙ"), None)
      for command in bstack11l1lll1l_opy_:
        if command == driver_command:
          with bstack111l1111_opy_:
            bstack111ll1l1_opy_ = bstack1ll111ll1l_opy_.copy()
          for driver in bstack111ll1l1_opy_:
            bstack1111l1l111_opy_(driver)
      bstack1lll1111l_opy_ = percy.bstack11111l1ll1_opy_()
      if driver_command in bstack1l111llll1_opy_[bstack1lll1111l_opy_]:
        bstack111ll11l11_opy_.bstack1lll1ll11_opy_(bstack1111l1l11_opy_, driver_command)
    except Exception as e:
      pass
_1l11ll1l_opy_ = threading.Event()
def bstack11llllll_opy_(framework_name):
  if global_config.get_property(bstack1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨේ")):
      _1l11ll1l_opy_.wait(timeout=30)
      return
  global_config.bstack11l11l11ll_opy_(bstack1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩෛ"), True)
  global FRAMEWORK_NAME
  global SELENIUM_OR_PLAYWRIGHT_INSTALLED
  global bstack111ll111ll_opy_
  FRAMEWORK_NAME = framework_name
  logger.info(bstack1l1l1111l_opy_.format(FRAMEWORK_NAME.split(bstack1ll_opy_ (u"࠭࠭ࠨො"))[0]))
  bstack1l11ll111_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    global bstack1lll111111_opy_
    bstack1lllllll1l1_opy_ = BROWSERSTACK_AUTOMATION or bstack1lll111111_opy_
    if bstack1lllllll1l1_opy_:
      Service.start = bstack111lll11l_opy_
      Service.stop = bstack1111l1ll1l_opy_
      webdriver.Remote.get = bstack1l1l11l1l1_opy_
      WebDriver.quit = bstack1l111lll_opy_
      webdriver.Remote.__init__ = bstack1111llll1l_opy_
    if not BROWSERSTACK_AUTOMATION and not bstack1lll111111_opy_:
        webdriver.Remote.__init__ = bstack1llll11l1l_opy_
    WebDriver.getAccessibilityResults = getAccessibilityResults
    WebDriver.get_accessibility_results = getAccessibilityResults
    WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
    WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
    WebDriver.performScan = perform_scan
    WebDriver.perform_scan = perform_scan
    WebDriver.execute = bstack11l11l1l11_opy_
    SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
  except Exception as e:
    pass
  try:
    bstack1lllllll1l1_opy_ = BROWSERSTACK_AUTOMATION or bstack1lll111111_opy_
    if bstack1lllllll1l1_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1llll1l1l1_opy_
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
    logger.debug(bstack1ll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤ࡬ࡲ࡯ࡣࡣ࡯ࡷ࠿ࠦࡻࡾࠤෝ").format(str(e)))
  patch_playwright()
  if not SELENIUM_OR_PLAYWRIGHT_INSTALLED:
    bstack11111lll1l_opy_(bstack1ll_opy_ (u"ࠣࡒࡤࡧࡰࡧࡧࡦࡵࠣࡲࡴࡺࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠥෞ"), bstack11111l1ll_opy_)
  if bstack1111l11lll_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      if hasattr(RemoteConnection, bstack1ll_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪෟ")) and callable(getattr(RemoteConnection, bstack1ll_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫ෠"))):
        RemoteConnection._get_proxy_url = bstack1111ll1l_opy_
      else:
        from selenium.webdriver.remote.client_config import ClientConfig
        ClientConfig.get_proxy_url = bstack1111ll1l_opy_
    except Exception as e:
      logger.error(bstack111l11ll11_opy_.format(str(e)))
  if bstack1ll11ll11_opy_():
    bstack1ll11l11_opy_(CONFIG, logger)
  if (bstack1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ෡") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      try:
        from pabot.pabot import QueueItem
        from pabot import pabot
      except Exception as e:
        logger.warning(bstack1lllll1l11_opy_ + str(e))
      if not is_robot_playwright_installed():
        try:
          if percy.bstack11l11ll11l_opy_() == bstack1ll_opy_ (u"ࠧࡺࡲࡶࡧࠥ෢"):
            bstack11111lll_opy_(bstack1l1111llll_opy_)
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
          WebDriverCreator._get_ff_profile = bstack11l11111_opy_
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
          WebDriverCache.close = bstack1l1lll1l1_opy_
        except Exception as e:
          logger.warning(bstack1ll1lll1ll_opy_ + str(e))
        try:
          from AppiumLibrary.utils.applicationcache import ApplicationCache
          ApplicationCache.close = bstack1ll11111l_opy_
        except Exception as e:
          logger.debug(bstack1l1l11lll1_opy_ + str(e))
    except Exception as e:
      bstack11111lll1l_opy_(e, bstack1ll1lll1ll_opy_)
    Output.start_test = bstack1lllll111_opy_
    Output.end_test = bstack1ll1llll_opy_
    TestStatus.__init__ = bstack1l1lll111l_opy_
    QueueItem.__init__ = bstack1lll111lll_opy_
    pabot._create_items = bstack11l11l111l_opy_
    try:
      from pabot import __version__ as bstack11l11l1ll_opy_
      if version.parse(bstack11l11l1ll_opy_) >= version.parse(bstack1ll_opy_ (u"࠭࠵࠯࠲࠱࠴ࠬ෣")):
        pabot._run = bstack1llll1ll11_opy_
      elif version.parse(bstack11l11l1ll_opy_) >= version.parse(bstack1ll_opy_ (u"ࠧ࠵࠰࠵࠲࠵࠭෤")):
        pabot._run = bstack111lllll11_opy_
      elif version.parse(bstack11l11l1ll_opy_) >= version.parse(bstack1ll_opy_ (u"ࠨ࠴࠱࠵࠺࠴࠰ࠨ෥")):
        pabot._run = bstack11lll1llll_opy_
      elif version.parse(bstack11l11l1ll_opy_) >= version.parse(bstack1ll_opy_ (u"ࠩ࠵࠲࠶࠹࠮࠱ࠩ෦")):
        pabot._run = bstack1111ll1lll_opy_
      else:
        pabot._run = bstack1l11l1l1l_opy_
    except Exception as e:
      pabot._run = bstack1l11l1l1l_opy_
    pabot._create_command_for_execution = bstack1ll1l11l1_opy_
    pabot._report_results = bstack11ll1l1l_opy_
  if bstack1ll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ෧") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11111lll1l_opy_(e, bstack1llll1lll1_opy_)
    Runner.run_hook = bstack1lll11l1l_opy_
    try:
      from behave import __version__ as bstack1ll1111l1l_opy_
      if version.parse(bstack1ll1111l1l_opy_) >= version.parse(bstack1ll_opy_ (u"ࠫ࠶࠴࠳࠯࠲ࠪ෨")):
        Runner.load_hooks = bstack1lll11ll1_opy_
    except Exception as e:
      logger.debug(bstack1ll_opy_ (u"ࠬࡉ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤࡧ࡫ࡨࡢࡸࡨࠤࡻ࡫ࡲࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩ෩").format(str(e)))
    Step.run = bstack11111l111_opy_
  if bstack1ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭෪") in str(framework_name).lower():
    if not BROWSERSTACK_AUTOMATION:
      _1l11ll1l_opy_.set()
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack1llllllll1l_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1l1l1l1l1_opy_
      Config.getoption = bstack11ll1l11_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack111ll1111l_opy_
    except Exception as e:
      pass
  _1l11ll1l_opy_.set()
def bstack11l1lllll_opy_():
  global CONFIG
  if bstack1ll_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ෫") in CONFIG and int(CONFIG[bstack1ll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ෬")]) > 1:
    logger.warning(bstack1l1l1l11l1_opy_)
def bstack1llllll1l1_opy_(arg, bstack11l11lll_opy_, bstack11ll1l1ll_opy_=None):
  global CONFIG
  global bstack1ll1111l1_opy_
  global bstack11l1llllll_opy_
  global BROWSERSTACK_AUTOMATION
  global bstack1lll111111_opy_
  global global_config
  bstack1l1ll11l_opy_ = bstack1ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ෭")
  if bstack11l11lll_opy_ and isinstance(bstack11l11lll_opy_, str):
    bstack11l11lll_opy_ = eval(bstack11l11lll_opy_)
  CONFIG = bstack11l11lll_opy_[bstack1ll_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪ෮")]
  bstack1ll1111l1_opy_ = bstack11l11lll_opy_[bstack1ll_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬ෯")]
  bstack11l1llllll_opy_ = bstack11l11lll_opy_[bstack1ll_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ෰")]
  BROWSERSTACK_AUTOMATION = bstack11l11lll_opy_[bstack1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ෱")]
  try:
    bstack11l11l1lll_opy_ = bstack11l11lll_opy_.get(bstack1ll_opy_ (u"ࠧࡐࡘࡈࡖࡗࡏࡄࡆࡡࡏࡓࡆࡊ࡟ࡕࡇࡖࡘࡎࡔࡇࠨෲ"), False)
    bstack1lll111111_opy_ = bool(bstack11l11l1lll_opy_)
    os.environ[bstack1ll_opy_ (u"ࠨࡑ࡙ࡉࡗࡘࡉࡅࡇࡢࡐࡔࡇࡄࡠࡖࡈࡗ࡙ࡏࡎࡈࠩෳ")] = str(bstack1lll111111_opy_).lower()
  except Exception as e:
    logger.error(bstack1ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡏࡗࡇࡕࡖࡎࡊࡅࡠࡎࡒࡅࡉࡥࡔࡆࡕࡗࡍࡓࡍ࠺ࠡࡽࢀࠦ෴").format(e))
    bstack1lll111111_opy_ = False
    os.environ[bstack1ll_opy_ (u"ࠪࡓ࡛ࡋࡒࡓࡋࡇࡉࡤࡒࡏࡂࡆࡢࡘࡊ࡙ࡔࡊࡐࡊࠫ෵")] = bstack1ll_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪ෶")
  global_config.bstack11l11l11ll_opy_(bstack1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭෷"), BROWSERSTACK_AUTOMATION)
  os.environ[bstack1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ෸")] = bstack1l1ll11l_opy_
  os.environ[bstack1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌ࠭෹")] = json.dumps(CONFIG)
  os.environ[bstack1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡉࡗࡅࡣ࡚ࡘࡌࠨ෺")] = bstack1ll1111l1_opy_
  os.environ[bstack1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ෻")] = str(bstack11l1llllll_opy_)
  os.environ[bstack1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡐ࡚ࡍࡉࡏࠩ෼")] = str(True)
  if bstack111l11111l_opy_(arg, [bstack1ll_opy_ (u"ࠫ࠲ࡴࠧ෽"), bstack1ll_opy_ (u"ࠬ࠳࠭࡯ࡷࡰࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭෾")]) != -1:
    os.environ[bstack1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡁࡓࡃࡏࡐࡊࡒࠧ෿")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1l11111l11_opy_)
    return
  bstack1l1l1ll1l_opy_()
  global bstack1111l1l1ll_opy_
  global PLATFORM_INDEX
  global bstack1lll1111l1_opy_
  global bstack1l111ll1_opy_
  global bstack1l1l1ll11_opy_
  global bstack111ll111ll_opy_
  global PARALLELISE_VANILLA_PYTHON
  arg.append(bstack1ll_opy_ (u"ࠢ࠮࡙ࠥ฀"))
  arg.append(bstack1ll_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡥ࠻ࡏࡲࡨࡺࡲࡥࠡࡣ࡯ࡶࡪࡧࡤࡺࠢ࡬ࡱࡵࡵࡲࡵࡧࡧ࠾ࡵࡿࡴࡦࡵࡷ࠲ࡕࡿࡴࡦࡵࡷ࡛ࡦࡸ࡮ࡪࡰࡪࠦก"))
  arg.append(bstack1ll_opy_ (u"ࠤ࠰࡛ࠧข"))
  arg.append(bstack1ll_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧ࠽ࡘ࡭࡫ࠠࡩࡱࡲ࡯࡮ࡳࡰ࡭ࠤฃ"))
  global bstack11ll1111l_opy_
  global bstack1111ll111l_opy_
  global bstack1l11l1l11_opy_
  global bstack1ll1l1ll_opy_
  global bstack11ll1l1lll_opy_
  global bstack1ll1llll1l_opy_
  global bstack1l1ll1lll_opy_
  global bstack1ll1ll1lll_opy_
  global bstack111l1ll1_opy_
  global bstack1111l1111_opy_
  global bstack1ll1l111ll_opy_
  global bstack11l111l1ll_opy_
  global bstack1ll111l1l_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11ll1111l_opy_ = webdriver.Remote.__init__
    bstack1111ll111l_opy_ = WebDriver.quit
    bstack1ll1ll1lll_opy_ = WebDriver.close
    bstack111l1ll1_opy_ = WebDriver.get
    bstack1l11l1l11_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1l1ll11l11_opy_(CONFIG) and bstack1ll1l1ll1l_opy_():
    if bstack1ll11l11l1_opy_() < version.parse(bstack1llll1ll_opy_):
      logger.error(bstack1l11ll11_opy_.format(bstack1ll11l11l1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack1ll_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬค")) and callable(getattr(RemoteConnection, bstack1ll_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭ฅ"))):
          bstack1111l1111_opy_ = RemoteConnection._get_proxy_url
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          bstack1111l1111_opy_ = ClientConfig.get_proxy_url
      except Exception as e:
        logger.error(bstack111l11ll11_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1ll1l111ll_opy_ = Config.getoption
    from _pytest import runner
    bstack11l111l1ll_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warning(bstack1ll_opy_ (u"ࠨࠥࡴ࠼ࠣࠩࡸࠨฆ"), bstack1l1llll1l_opy_, str(e))
  try:
    from pytest_bdd import reporting
    bstack1ll111l1l_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack1ll_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨง"))
  if cli.is_enabled(CONFIG) and cli.config:
    bstack1lll1111l1_opy_ = cli.config.get(bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬจ"), {}).get(bstack1ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫฉ"))
  else:
    bstack1lll1111l1_opy_ = CONFIG.get(bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧช"), {}).get(bstack1ll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ซ"))
  PARALLELISE_VANILLA_PYTHON = True
  if cli.is_enabled(CONFIG):
    if cli.bstack1l1ll1l11_opy_():
      bstack111l1lll11_opy_.invoke(Events.CONNECT, bstack11111l11_opy_())
    platform_index = int(os.environ.get(bstack1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬฌ"), bstack1ll_opy_ (u"࠭࠰ࠨญ")))
  else:
    bstack11llllll_opy_(bstack1l1ll1llll_opy_)
  os.environ[bstack1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨฎ")] = CONFIG[bstack1ll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪฏ")]
  os.environ[bstack1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬฐ")] = CONFIG[bstack1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ฑ")]
  os.environ[bstack1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧฒ")] = BROWSERSTACK_AUTOMATION.__str__()
  from _pytest.config import main as bstack11111l1l_opy_
  bstack1ll1l1l1l_opy_ = []
  try:
    exit_code = bstack11111l1l_opy_(arg)
    if cli.is_enabled(CONFIG):
      cli.bstack11llll111_opy_()
    if bstack1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩณ") in multiprocessing.current_process().__dict__.keys():
      for bstack1l1111l1_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1ll1l1l1l_opy_.append(bstack1l1111l1_opy_)
    try:
      bstack111ll1ll1_opy_ = (bstack1ll1l1l1l_opy_, int(exit_code))
      bstack11ll1l1ll_opy_.append(bstack111ll1ll1_opy_)
    except:
      bstack11ll1l1ll_opy_.append((bstack1ll1l1l1l_opy_, exit_code))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack1ll1l1l1l_opy_.append({bstack1ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫด"): bstack1ll_opy_ (u"ࠧࡑࡴࡲࡧࡪࡹࡳࠡࠩต") + os.environ.get(bstack1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨถ")), bstack1ll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨท"): traceback.format_exc(), bstack1ll_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩธ"): int(os.environ.get(bstack1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫน")))})
    bstack11ll1l1ll_opy_.append((bstack1ll1l1l1l_opy_, 1))
def mod_behave_main(args, retries):
  try:
    from behave.configuration import Configuration
    from behave.__main__ import run_behave
    from browserstack_sdk.bstack_behave_runner import BehaveRunner
    config = Configuration(args)
    config.update_userdata({bstack1ll_opy_ (u"ࠧࡸࡥࡵࡴ࡬ࡩࡸࠨบ"): str(retries)})
    return run_behave(config, runner_class=BehaveRunner)
  except Exception as e:
    bstack11l111l1l_opy_ = e.__class__.__name__
    print(bstack1ll_opy_ (u"ࠨࠥࡴ࠼ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡦࡪ࡮ࡡࡷࡧࠣࡸࡪࡹࡴࠡࠧࡶࠦป") % (bstack11l111l1l_opy_, e))
    return 1
def bstack1llllll1111_opy_(arg):
  global bstack1l1lllll11_opy_
  bstack11llllll_opy_(bstack11llll1l_opy_)
  os.environ[bstack1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨผ")] = str(bstack11l1llllll_opy_)
  retries = bstack1l111111ll_opy_.bstack1111l11111_opy_(CONFIG)
  status_code = 0
  if bstack1l111111ll_opy_.bstack1ll11llll_opy_(CONFIG):
    status_code = mod_behave_main(arg, retries)
  else:
    from behave.__main__ import main as bstack11lll1l11_opy_
    status_code = bstack11lll1l11_opy_(arg)
  if status_code != 0:
    bstack1l1lllll11_opy_ = status_code
def bstack1llll11l1_opy_():
  logger.info(bstack111lll1111_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1ll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧฝ"), help=bstack1ll_opy_ (u"ࠩࡊࡩࡳ࡫ࡲࡢࡶࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡧࡴࡴࡦࡪࡩࠪพ"))
  parser.add_argument(bstack1ll_opy_ (u"ࠪ࠱ࡺ࠭ฟ"), bstack1ll_opy_ (u"ࠫ࠲࠳ࡵࡴࡧࡵࡲࡦࡳࡥࠨภ"), help=bstack1ll_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫม"))
  parser.add_argument(bstack1ll_opy_ (u"࠭࠭࡬ࠩย"), bstack1ll_opy_ (u"ࠧ࠮࠯࡮ࡩࡾ࠭ร"), help=bstack1ll_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡧࡣࡤࡧࡶࡷࠥࡱࡥࡺࠩฤ"))
  parser.add_argument(bstack1ll_opy_ (u"ࠩ࠰ࡪࠬล"), bstack1ll_opy_ (u"ࠪ࠱࠲࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨฦ"), help=bstack1ll_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪว"))
  bstack1lllll11l1_opy_ = parser.parse_args()
  try:
    bstack1lll11lll_opy_ = bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡬࡫࡮ࡦࡴ࡬ࡧ࠳ࡿ࡭࡭࠰ࡶࡥࡲࡶ࡬ࡦࠩศ")
    if bstack1lllll11l1_opy_.framework and bstack1lllll11l1_opy_.framework not in (bstack1ll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ษ"), bstack1ll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨส")):
      bstack1lll11lll_opy_ = bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࠱ࡽࡲࡲ࠮ࡴࡣࡰࡴࡱ࡫ࠧห")
    bstack1ll1ll1l11_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1lll11lll_opy_)
    bstack11l1ll1ll1_opy_ = open(bstack1ll1ll1l11_opy_, bstack1ll_opy_ (u"ࠩࡵࠫฬ"))
    bstack11ll11l1l1_opy_ = bstack11l1ll1ll1_opy_.read()
    bstack11l1ll1ll1_opy_.close()
    if bstack1lllll11l1_opy_.username:
      bstack11ll11l1l1_opy_ = bstack11ll11l1l1_opy_.replace(bstack1ll_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪอ"), bstack1lllll11l1_opy_.username)
    if bstack1lllll11l1_opy_.key:
      bstack11ll11l1l1_opy_ = bstack11ll11l1l1_opy_.replace(bstack1ll_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭ฮ"), bstack1lllll11l1_opy_.key)
    if bstack1lllll11l1_opy_.framework:
      bstack11ll11l1l1_opy_ = bstack11ll11l1l1_opy_.replace(bstack1ll_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ฯ"), bstack1lllll11l1_opy_.framework)
    file_name = bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩะ")
    file_path = os.path.abspath(file_name)
    bstack1l11llllll_opy_ = open(file_path, bstack1ll_opy_ (u"ࠧࡸࠩั"))
    bstack1l11llllll_opy_.write(bstack11ll11l1l1_opy_)
    bstack1l11llllll_opy_.close()
    logger.info(bstack1lll11l11_opy_)
    try:
      os.environ[bstack1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪา")] = bstack1lllll11l1_opy_.framework if bstack1lllll11l1_opy_.framework != None else bstack1ll_opy_ (u"ࠤࠥำ")
      config = yaml.safe_load(bstack11ll11l1l1_opy_)
      config[bstack1ll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪิ")] = bstack1ll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱ࡸ࡫ࡴࡶࡲࠪี")
      bstack1ll11ll1ll_opy_(bstack111lll1l1l_opy_, config)
    except Exception as e:
      logger.debug(bstack1lllllll11_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1l111ll11_opy_.format(str(e)))
def bstack1ll11ll1ll_opy_(bstack1l1l111l1_opy_, config, bstack1l111l111_opy_=None, bstack11ll1lll1l_opy_=False):
  global BROWSERSTACK_AUTOMATION
  global bstack1ll11ll1l1_opy_
  global global_config
  if not config:
    return
  if bstack1l111l111_opy_ is None:
    bstack1l111l111_opy_ = {}
  bstack1ll11lll1l_opy_ = bstack1llllll11_opy_ if not BROWSERSTACK_AUTOMATION else (
    bstack11l1l1ll_opy_ if bstack1ll_opy_ (u"ࠬࡧࡰࡱࠩึ") in config else (
        bstack111l1l1ll_opy_ if config.get(bstack1ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪื")) else bstack11lll111l1_opy_
    )
)
  bstack11ll11ll11_opy_ = False
  bstack11lll11111_opy_ = False
  if BROWSERSTACK_AUTOMATION is True:
      if bstack1ll_opy_ (u"ࠧࡢࡲࡳุࠫ") in config:
          bstack11ll11ll11_opy_ = True
      else:
          bstack11lll11111_opy_ = True
  bstack111ll1l1ll_opy_ = TestHubUtils.bstack11l11l11l_opy_(config, bstack1ll11ll1l1_opy_)
  bstack1l1ll111l1_opy_ = bstack11l1l1llll_opy_()
  data = {
    bstack1ll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧูࠪ"): config[bstack1ll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨฺࠫ")],
    bstack1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭฻"): config[bstack1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ฼")],
    bstack1ll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ฽"): bstack1l1l111l1_opy_,
    bstack1ll_opy_ (u"࠭ࡤࡦࡶࡨࡧࡹ࡫ࡤࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ฾"): os.environ.get(bstack1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩ฿"), bstack1ll11ll1l1_opy_),
    bstack1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪเ"): bstack1l1ll111_opy_,
    bstack1ll_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯ࠫแ"): bstack1lll1l1lll_opy_(),
    bstack1ll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭โ"): {
      bstack1ll_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩใ"): str(config[bstack1ll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬไ")]) if bstack1ll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ๅ") in config else bstack1ll_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣๆ"),
      bstack1ll_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧ࡙ࡩࡷࡹࡩࡰࡰࠪ็"): sys.version,
      bstack1ll_opy_ (u"ࠩࡵࡩ࡫࡫ࡲࡳࡧࡵ่ࠫ"): bstack1ll11lllll_opy_(os.environ.get(bstack1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏ้ࠬ"), bstack1ll11ll1l1_opy_)),
      bstack1ll_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ๊࠭"): bstack1ll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ๋ࠬ"),
      bstack1ll_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧ์"): bstack1ll11lll1l_opy_,
      bstack1ll_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬํ"): bstack111ll1l1ll_opy_,
      bstack1ll_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡡࡸࡹ࡮ࡪࠧ๎"): os.environ[bstack1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ๏")],
      bstack1ll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭๐"): os.environ.get(bstack1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭๑"), bstack1ll11ll1l1_opy_),
      bstack1ll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ๒"): bstack1ll1lll11l_opy_(os.environ.get(bstack1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ๓"), bstack1ll11ll1l1_opy_)),
      bstack1ll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭๔"): bstack1l1ll111l1_opy_.get(bstack1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭๕")),
      bstack1ll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ๖"): bstack1l1ll111l1_opy_.get(bstack1ll_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫ๗")),
      bstack1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ๘"): config[bstack1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ๙")] if config[bstack1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ๚")] else bstack1ll_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣ๛"),
      bstack1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ๜"): str(config[bstack1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ๝")]) if bstack1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ๞") in config else bstack1ll_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧ๟"),
      bstack1ll_opy_ (u"ࠬࡵࡳࠨ๠"): sys.platform,
      bstack1ll_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨ๡"): socket.gethostname(),
      bstack1ll_opy_ (u"ࠧࡪࡵࡆࡐࡎࡋ࡮ࡢࡤ࡯ࡩࡩ࠭๢"): bstack11ll1lll1l_opy_,
      bstack1ll_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪ๣"): global_config.get_property(bstack1ll_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫ๤"))
    }
  }
  if not global_config.get_property(bstack1ll_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪ๥")) is None:
    data[bstack1ll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧ๦")][bstack1ll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࡍࡦࡶࡤࡨࡦࡺࡡࠨ๧")] = {
      bstack1ll_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭๨"): bstack1ll_opy_ (u"ࠧࡶࡵࡨࡶࡤࡱࡩ࡭࡮ࡨࡨࠬ๩"),
      bstack1ll_opy_ (u"ࠨࡵ࡬࡫ࡳࡧ࡬ࠨ๪"): global_config.get_property(bstack1ll_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩ๫")),
      bstack1ll_opy_ (u"ࠪࡷ࡮࡭࡮ࡢ࡮ࡑࡹࡲࡨࡥࡳࠩ๬"): global_config.get_property(bstack1ll_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡓࡵࠧ๭"))
    }
  if bstack1l1l111l1_opy_ == bstack1l1l11l11l_opy_:
    data[bstack1ll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨ๮")][bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡈࡵ࡮ࡧ࡫ࡪࠫ๯")] = bstack111111l111_opy_(config)
    data[bstack1ll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪ๰")][bstack1ll_opy_ (u"ࠨ࡫ࡶࡔࡪࡸࡣࡺࡃࡸࡸࡴࡋ࡮ࡢࡤ࡯ࡩࡩ࠭๱")] = percy.bstack11l1llll1_opy_
    data[bstack1ll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬ๲")][bstack1ll_opy_ (u"ࠪࡴࡪࡸࡣࡺࡄࡸ࡭ࡱࡪࡉࡥࠩ๳")] = percy.percy_build_id
  if not bstack1l111111ll_opy_.bstack1lll11l11l_opy_(CONFIG):
    data[bstack1ll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧ๴")][bstack1ll_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠩ๵")] = bstack1l111111ll_opy_.bstack1lll11l11l_opy_(CONFIG)
  bstack11llll1lll_opy_ = bstack1l11ll1ll_opy_.bstack1l111l1111_opy_(CONFIG, logger)
  bstack1ll1ll1ll_opy_ = bstack1l111111ll_opy_.bstack1l111l1111_opy_(config=CONFIG)
  if bstack11llll1lll_opy_ is not None and bstack1ll1ll1ll_opy_ is not None and bstack1ll1ll1ll_opy_.bstack1llll111ll_opy_():
    data[bstack1ll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩ๶")][bstack1ll1ll1ll_opy_.bstack1l1l11ll1_opy_()] = bstack11llll1lll_opy_.bstack1llllllll1_opy_()
  update(data[bstack1ll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪ๷")], bstack1l111l111_opy_)
  try:
    response = bstack1l1111l111_opy_(bstack1ll_opy_ (u"ࠨࡒࡒࡗ࡙࠭๸"), bstack1l11llll1_opy_(bstack1ll111l111_opy_), data, {
      bstack1ll_opy_ (u"ࠩࡤࡹࡹ࡮ࠧ๹"): (config[bstack1ll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ๺")], config[bstack1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ๻")])
    })
    if response:
      logger.debug(bstack1lllll1lll_opy_.format(bstack1l1l111l1_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1llllll1l11_opy_.format(str(e)))
def bstack1ll11lllll_opy_(framework):
  return bstack1ll_opy_ (u"ࠧࢁࡽ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࡻࡾࠤ๼").format(str(framework), __version__) if framework else bstack1ll_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࢀࢃࠢ๽").format(
    __version__)
def bstack1l1l1ll1l_opy_():
  global CONFIG
  global bstack11l1l1lll_opy_
  if bool(CONFIG):
    return
  try:
    bstack1111l11l_opy_()
    logger.debug(bstack1ll111ll_opy_.format(str(CONFIG)))
    bstack11l1l1lll_opy_ = logger_utils.configure_logger(CONFIG, bstack11l1l1lll_opy_)
    bstack1l11ll111_opy_()
  except Exception as e:
    logger.error(bstack1ll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱ࠮ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠦ๾") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1ll111l1l1_opy_
  atexit.register(bstack111l1lll1_opy_)
  signal.signal(signal.SIGINT, bstack1l11lll1_opy_)
  signal.signal(signal.SIGTERM, bstack1l11lll1_opy_)
def bstack1ll111l1l1_opy_(exctype, value, traceback):
  global bstack1ll111ll1l_opy_
  try:
    for driver in bstack1ll111ll1l_opy_:
      bstack1l111l1l1l_opy_(driver, bstack1ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ๿"), bstack1ll_opy_ (u"ࠤࡖࡩࡸࡹࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧ຀") + str(value))
  except Exception:
    pass
  logger.info(bstack1ll1ll1111_opy_)
  bstack1l1l11111l_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1l1l11111l_opy_(message=bstack1ll_opy_ (u"ࠪࠫກ"), bstack11l1111111_opy_ = False, bstack11ll1lll1l_opy_ = False):
  global CONFIG
  bstack11ll1l1111_opy_ = bstack1ll_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡉࡽࡩࡥࡱࡶ࡬ࡳࡳ࠭ຂ") if bstack11l1111111_opy_ else bstack1ll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ຃")
  bstack11l11lll1l_opy_ = bstack1l11l1ll11_opy_.bstack1111ll1111_opy_(EVENTS.bstack111ll1llll_opy_)
  try:
    if message:
      bstack1l111l111_opy_ = {
        bstack11ll1l1111_opy_ : str(message)
      }
      try:
        bstack1ll11ll1ll_opy_(bstack1l1l11l11l_opy_, CONFIG, bstack1l111l111_opy_, bstack11ll1lll1l_opy_)
      finally:
        bstack1l11l1ll11_opy_.end(EVENTS.bstack111ll1llll_opy_.value, bstack11l11lll1l_opy_ + bstack1ll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨຄ"), bstack11l11lll1l_opy_ + bstack1ll_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ຅"), status=True, failure=None, test_name=None)
    else:
      try:
        bstack1ll11ll1ll_opy_(bstack1l1l11l11l_opy_, CONFIG, bstack11ll1lll1l_opy_=bstack11ll1lll1l_opy_)
      finally:
        bstack1l11l1ll11_opy_.end(EVENTS.bstack111ll1llll_opy_.value, bstack11l11lll1l_opy_ + bstack1ll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣຆ"), bstack11l11lll1l_opy_ + bstack1ll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢງ"), status=True, failure=None, test_name=None)
  except Exception as e:
    logger.debug(bstack1l111lll11_opy_.format(str(e)))
def bstack11ll1l1ll1_opy_(bstack111ll11l1l_opy_, size):
  bstack1ll1llll1_opy_ = []
  while len(bstack111ll11l1l_opy_) > size:
    bstack1ll111l1ll_opy_ = bstack111ll11l1l_opy_[:size]
    bstack1ll1llll1_opy_.append(bstack1ll111l1ll_opy_)
    bstack111ll11l1l_opy_ = bstack111ll11l1l_opy_[size:]
  bstack1ll1llll1_opy_.append(bstack111ll11l1l_opy_)
  return bstack1ll1llll1_opy_
def bstack11l1llll_opy_(args):
  if bstack1ll_opy_ (u"ࠪ࠱ࡲ࠭ຈ") in args and bstack1ll_opy_ (u"ࠫࡵࡪࡢࠨຉ") in args:
    return True
  return False
@measure(event_name=EVENTS.bstack1l1ll1111l_opy_, stage=STAGE.bstack1ll1lll1l_opy_)
def run_on_browserstack(bstack11l11l1l_opy_=None, bstack11ll1l1ll_opy_=None, bstack1l1lll1l11_opy_=False):
  global CONFIG
  global bstack1ll1111l1_opy_
  global bstack11l1llllll_opy_
  global bstack1ll11ll1l1_opy_
  global global_config
  bstack1l1ll11l_opy_ = bstack1ll_opy_ (u"ࠬ࠭ຊ")
  bstack1l1llllll1_opy_ = bstack1ll_opy_ (u"ࠨࠢ຋")
  bstack1l1l11l1ll_opy_(bstack11l111ll1l_opy_, logger)
  if bstack11l11l1l_opy_ and isinstance(bstack11l11l1l_opy_, str):
    bstack11l11l1l_opy_ = eval(bstack11l11l1l_opy_)
  if bstack11l11l1l_opy_:
    CONFIG = bstack11l11l1l_opy_[bstack1ll_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧຌ")]
    bstack1ll1111l1_opy_ = bstack11l11l1l_opy_[bstack1ll_opy_ (u"ࠨࡊࡘࡆࡤ࡛ࡒࡍࠩຍ")]
    bstack11l1llllll_opy_ = bstack11l11l1l_opy_[bstack1ll_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫຎ")]
    global_config.bstack11l11l11ll_opy_(bstack1ll_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬຏ"), bstack11l1llllll_opy_)
    bstack1l1ll11l_opy_ = bstack1ll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠬຐ")
  global_config.bstack11l11l11ll_opy_(bstack1ll_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪࠧຑ"), uuid4().__str__())
  logger.info(bstack1ll_opy_ (u"࠭ࡓࡅࡍࠣࡶࡺࡴࠠࡴࡶࡤࡶࡹ࡫ࡤࠡࡹ࡬ࡸ࡭ࠦࡩࡥ࠼ࠣࠫຒ") + global_config.get_property(bstack1ll_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥࠩຓ")));
  logger.debug(bstack1ll_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࡀࠫດ") + global_config.get_property(bstack1ll_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫຕ")))
  if not bstack1l1lll1l11_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1l11111l11_opy_)
      return
    if sys.argv[1] == bstack1ll_opy_ (u"ࠪ࠱࠲ࡼࡥࡳࡵ࡬ࡳࡳ࠭ຖ") or sys.argv[1] == bstack1ll_opy_ (u"ࠫ࠲ࡼࠧທ"):
      logger.info(bstack1ll_opy_ (u"ࠬࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡕࡿࡴࡩࡱࡱࠤࡘࡊࡋࠡࡸࡾࢁࠬຘ").format(__version__))
      return
    if sys.argv[1] == bstack1ll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬນ"):
      bstack1llll11l1_opy_()
      return
    if sys.argv[1] == bstack1ll_opy_ (u"ࠧ࡭ࡱࡤࡨࠬບ"):
      from browserstack_sdk.bstack11l1l1l1l_opy_ import bstack111l1llll_opy_
      bstack1l1l1ll1l_opy_()
      bstack111l1llll_opy_(CONFIG)
      return
  args = sys.argv
  bstack1l1l1ll1l_opy_()
  global bstack1lll111111_opy_
  try:
    from bstack_utils import constants as bstack11l1lll1_opy_
    override_value = CONFIG.get(bstack1ll_opy_ (u"ࠨࡱࡹࡩࡷࡸࡩࡥࡧࡏࡳࡦࡪࡔࡦࡵࡷ࡭ࡳ࡭ࠧປ"), False)
    bstack1lll111111_opy_ = bool(override_value)
  except Exception as e:
    logger.error(bstack1ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡏࡗࡇࡕࡖࡎࡊࡅࡠࡎࡒࡅࡉࡥࡔࡆࡕࡗࡍࡓࡍ࠺ࠡࡽࢀࠦຜ").format(e))
    bstack1lll111111_opy_ = False
  if bstack1lll111111_opy_:
    bstack1ll11l11l_opy_ = CONFIG.get(bstack1ll_opy_ (u"ࠪࡰࡴࡧࡤࡕࡧࡶࡸ࡮ࡴࡧࡉࡷࡥ࡙ࡗࡒࠧຝ")) or bstack11l1lll1_opy_.bstack1l1lll1l1l_opy_
    logger.info(bstack1ll_opy_ (u"ࠦࡌࡲ࡯ࡣࡣ࡯ࠤࡴࡼࡥࡳࡴ࡬ࡨࡪࡲ࡯ࡢࡦࡷࡩࡸࡺࡩ࡯ࡩࠣࡩࡳࡧࡢ࡭ࡧࡧ࠰ࠥࡻࡳࡪࡰࡪࠤ࡭ࡻࡢ࠻ࠢࡾࢁࠧພ").format(bstack1ll11l11l_opy_))
    bstack1ll1111l1_opy_ = bstack1ll11l11l_opy_
    try:
      bstack11l1lll1_opy_.bstack111l11lll1_opy_ = bstack1ll11l11l_opy_
      bstack11l1lll1_opy_.bstack1lllll1l1l_opy_ = bstack1ll11l11l_opy_
    except Exception:
      pass
  global bstack1111l1l1ll_opy_
  global bstack1l11ll11l1_opy_
  global PARALLELISE_VANILLA_PYTHON
  global PARALLELISE_THREADING_PYTHON
  global PLATFORM_INDEX
  global bstack1lll1111l1_opy_
  global bstack1l111ll1_opy_
  global bstack1l11l11ll1_opy_
  global bstack1l1l1ll11_opy_
  global bstack111ll111ll_opy_
  global bstack11111ll11l_opy_
  bstack1l11ll11l1_opy_ = len(CONFIG.get(bstack1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨຟ"), []))
  if not bstack1l1ll11l_opy_:
    if args[1] == bstack1ll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ຠ") or args[1] == bstack1ll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨມ") or args[1] == bstack1ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩຢ"):
      bstack1l1ll11l_opy_ = bstack1ll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠪຣ")
      args = args[2:]
    elif args[1] == bstack1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ຤"):
      bstack1l1ll11l_opy_ = bstack1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪລ")
      args = args[2:]
    elif args[1] == bstack1ll_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ຦"):
      bstack1l1ll11l_opy_ = bstack1ll_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬວ")
      args = args[2:]
    elif args[1] == bstack1ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨຨ"):
      bstack1l1ll11l_opy_ = bstack1ll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩຩ")
      args = args[2:]
    elif args[1] == bstack1ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩສ"):
      bstack1l1ll11l_opy_ = bstack1ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪຫ")
      args = args[2:]
    elif args[1] == bstack1ll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫຬ"):
      bstack1l1ll11l_opy_ = bstack1ll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬອ")
      args = args[2:]
    else:
      if not bstack1ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩຮ") in CONFIG or str(CONFIG[bstack1ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪຯ")]).lower() in [bstack1ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨະ"), bstack1ll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪັ"), bstack1ll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠫາ")]:
        bstack1l1ll11l_opy_ = bstack1ll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠬຳ")
        args = args[1:]
      elif str(CONFIG[bstack1ll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨິ")]).lower() == bstack1ll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬີ"):
        bstack1l1ll11l_opy_ = bstack1ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ຶ")
        args = args[1:]
      elif str(CONFIG[bstack1ll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫື")]).lower() == bstack1ll_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨຸ"):
        bstack1l1ll11l_opy_ = bstack1ll_opy_ (u"ࠪࡴࡦࡨ࡯ࡵູࠩ")
        args = args[1:]
      elif str(CONFIG[bstack1ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ຺ࠧ")]).lower() == bstack1ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬົ"):
        bstack1l1ll11l_opy_ = bstack1ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ຼ")
        args = args[1:]
      elif str(CONFIG[bstack1ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪຽ")]).lower() == bstack1ll_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ຾"):
        bstack1l1ll11l_opy_ = bstack1ll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ຿")
        args = args[1:]
      else:
        os.environ[bstack1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬເ")] = bstack1l1ll11l_opy_
        bstack1ll11l11ll_opy_(bstack1l1llll111_opy_)
  os.environ[bstack1ll_opy_ (u"ࠫࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ࡟ࡖࡕࡈࡈࠬແ")] = bstack1l1ll11l_opy_
  bstack1ll11ll1l1_opy_ = bstack1l1ll11l_opy_
  if cli.is_enabled(CONFIG):
    bstack1l11lll1l1_opy_ = os.environ.get(bstack1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤ࡙ࡅࡔࡕࡌࡓࡓࡥࡉࡅࠩໂ"), bstack1ll_opy_ (u"࠭ࠧໃ")) != bstack1ll_opy_ (u"ࠧࠨໄ")
    if bstack1l11lll1l1_opy_:
        try:
          bstack111l1lll11_opy_.invoke(Events.CONNECT, bstack11111l11_opy_())
        except Exception as e:
          bstack111l1lll11_opy_.invoke(Events.bstack11ll1lll11_opy_, e.__traceback__, 1)
    else:
        try:
          if bstack1l1ll11l_opy_ == bstack1ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ໅") and bstack11lll11ll_opy_():
            bstack1111l1ll1_opy_ = bstack11lllll111_opy_[bstack1ll_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕ࠯ࡅࡈࡉ࠭ໆ")]
          elif bstack1l1ll11l_opy_ in [bstack1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ໇"), bstack1ll_opy_ (u"ࠫࡵࡧࡢࡰࡶ່ࠪ")]:
            bstack1111l1ll1_opy_ = bstack1ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ້ࠫ")
          else:
            bstack1111l1ll1_opy_ = bstack1l1ll11l_opy_
          bstack111l1lll11_opy_.invoke(Events.bstack1ll11llll1_opy_, bstack1l11l111_opy_(
        sdk_version=__version__,
        path_config=bstack11111111ll_opy_(),
        path_project=os.getcwd(),
        test_framework=bstack1111l1ll1_opy_,
        frameworks=[bstack1111l1ll1_opy_],
        framework_versions={
          bstack1111l1ll1_opy_: bstack1ll1lll11l_opy_(bstack1ll_opy_ (u"࠭ࡒࡰࡤࡲࡸ໊ࠬ") if bstack1l1ll11l_opy_ in [bstack1ll_opy_ (u"ࠧࡱࡣࡥࡳࡹ໋࠭"), bstack1ll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ໌"), bstack1ll_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪໍ")] else bstack1l1ll11l_opy_)
        },
        bs_config=CONFIG
      ))
          if cli.config and cli.config.get(bstack1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧ໎"), None):
            CONFIG[bstack1ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࠨ໏")] = cli.config.get(bstack1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠢ໐"), None)
        except Exception as e:
          bstack111l1lll11_opy_.invoke(Events.bstack11ll1lll11_opy_, e.__traceback__, 1)
    if bstack11l1llllll_opy_:
      CONFIG[bstack1ll_opy_ (u"ࠨࡡࡱࡲࠥ໑")] = cli.config[bstack1ll_opy_ (u"ࠢࡢࡲࡳࠦ໒")]
      logger.info(bstack1lll11111_opy_.format(CONFIG[bstack1ll_opy_ (u"ࠨࡣࡳࡴࠬ໓")]))
  else:
    bstack111l1lll11_opy_.clear()
  global bstack111111l1_opy_
  global bstack11111l11l_opy_
  if bstack11l11l1l_opy_:
    try:
      bstack1l1111ll_opy_ = datetime.datetime.now()
      os.environ[bstack1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫ໔")] = bstack1l1ll11l_opy_
      bstack1lll1l11ll_opy_ = bstack1l11l1ll11_opy_.bstack1111ll1111_opy_(EVENTS.bstack1llllllllll_opy_)
      try:
        logger.info(bstack1ll_opy_ (u"ࠥࡗࡪࡴࡤࡪࡰࡪࠤࡘࡊࡋࠡࡖࡨࡷࡹࠦࡁࡵࡶࡨࡱࡵࡺࡥࡥࠢࡨࡺࡪࡴࡴࠣ໕"))
        bstack1ll11ll1ll_opy_(bstack1111lll1_opy_, CONFIG)
      finally:
        bstack1l11l1ll11_opy_.end(EVENTS.bstack1llllllllll_opy_.value, bstack1lll1l11ll_opy_ + bstack1ll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ໖"), bstack1lll1l11ll_opy_ + bstack1ll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ໗"), status=True, failure=None, test_name=None)
      cli.bstack1lll11ll11_opy_(bstack1ll_opy_ (u"ࠨࡨࡵࡶࡳ࠾ࡸࡪ࡫ࡠࡶࡨࡷࡹࡥࡡࡵࡶࡨࡱࡵࡺࡥࡥࠤ໘"), datetime.datetime.now() - bstack1l1111ll_opy_)
    except Exception as e:
      logger.debug(bstack1l1llll11l_opy_.format(str(e)))
  global bstack11ll1111l_opy_
  global bstack1111ll111l_opy_
  global bstack11ll1l1l11_opy_
  global bstack111ll11ll1_opy_
  global bstack11l1l1l1_opy_
  global bstack11lll11ll1_opy_
  global bstack1ll1l1ll_opy_
  global bstack11ll1l1lll_opy_
  global bstack11l111lll_opy_
  global bstack1ll1llll1l_opy_
  global bstack1l1ll1lll_opy_
  global bstack1ll1ll1lll_opy_
  global bstack111ll111_opy_
  global bstack11l11ll1l_opy_
  global bstack1lllll1ll_opy_
  global bstack111l1ll1_opy_
  global bstack1111l1111_opy_
  global bstack1ll1l111ll_opy_
  global bstack11l111l1ll_opy_
  global bstack11l1l11l1_opy_
  global bstack1ll111l1l_opy_
  global bstack1l11l1l11_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11ll1111l_opy_ = webdriver.Remote.__init__
    bstack1111ll111l_opy_ = WebDriver.quit
    bstack1ll1ll1lll_opy_ = WebDriver.close
    bstack111l1ll1_opy_ = WebDriver.get
    bstack1l11l1l11_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack111111l1_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack1l11lllll1_opy_
    bstack11111l11l_opy_ = bstack1l11lllll1_opy_()
  except Exception as e:
    pass
  try:
    global bstack111l111l1l_opy_
    from QWeb.keywords import browser
    bstack111l111l1l_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1l1ll11l11_opy_(CONFIG) and bstack1ll1l1ll1l_opy_():
    if bstack1ll11l11l1_opy_() < version.parse(bstack1llll1ll_opy_):
      logger.error(bstack1l11ll11_opy_.format(bstack1ll11l11l1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack1ll_opy_ (u"ࠧࡠࡩࡨࡸࡤࡶࡲࡰࡺࡼࡣࡺࡸ࡬ࠨ໙")) and callable(getattr(RemoteConnection, bstack1ll_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩ໚"))):
          RemoteConnection._get_proxy_url = bstack1111ll1l_opy_
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          ClientConfig.get_proxy_url = bstack1111ll1l_opy_
      except Exception as e:
        logger.error(bstack111l11ll11_opy_.format(str(e)))
  if not CONFIG.get(bstack1ll_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫ໛"), False) and not bstack11l11l1l_opy_:
    logger.info(bstack11111l11l1_opy_)
  bstack1ll1l1ll11_opy_ = not cli.is_enabled(CONFIG) and bstack1l1ll11l_opy_ not in [bstack1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫໜ")]
  bstack11ll1ll1l1_opy_ = bstack1ll1l1ll11_opy_ and bstack1ll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨໝ") in CONFIG and str(CONFIG[bstack1ll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩໞ")]).lower() != bstack1ll_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬໟ")
  bstack1ll1lll11_opy_ = bstack1ll1l1ll11_opy_ and not bstack11ll1ll1l1_opy_ and (bstack1l1ll11l_opy_ != bstack1ll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡨࡧࡱࡩࡷ࡯ࡣࠨ໠") or (bstack1l1ll11l_opy_ == bstack1ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩ໡") and not bstack11l11l1l_opy_))
  if bstack1l1ll11l_opy_ not in [bstack1ll_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ໢")]:
    bstack1l1l11l1ll_opy_(os.path.join(os.getcwd(), bstack1ll_opy_ (u"ࠪࡰࡴ࡭ࠧ໣"), bstack1ll_opy_ (u"ࠫࡰ࡫ࡹ࠮࡯ࡨࡸࡷ࡯ࡣࡴ࠰࡭ࡷࡴࡴࠧ໤")), logger)
  if (bstack1l1ll11l_opy_ in [bstack1ll_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ໥"), bstack1ll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ໦"), bstack1ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ໧")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      try:
        from pabot.pabot import QueueItem
        from pabot import pabot
      except Exception as e:
        logger.warning(bstack1lllll1l11_opy_ + str(e))
      if not is_robot_playwright_installed():
        try:
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
          WebDriverCreator._get_ff_profile = bstack11l11111_opy_
          bstack11lll11ll1_opy_ = WebDriverCache.close
        except Exception as e:
          logger.warning(bstack1ll1lll1ll_opy_ + str(e))
        try:
          from AppiumLibrary.utils.applicationcache import ApplicationCache
          bstack11l1l1l1_opy_ = ApplicationCache.close
        except Exception as e:
          logger.debug(bstack1l1l11lll1_opy_ + str(e))
    except Exception as e:
      bstack11111lll1l_opy_(e, bstack1ll1lll1ll_opy_)
    if bstack1l1ll11l_opy_ != bstack1ll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ໨"):
      bstack111ll1lll1_opy_()
    bstack11ll1l1l11_opy_ = Output.start_test
    bstack111ll11ll1_opy_ = Output.end_test
    bstack1ll1l1ll_opy_ = TestStatus.__init__
    bstack11l111lll_opy_ = pabot._run
    bstack1ll1llll1l_opy_ = QueueItem.__init__
    bstack1l1ll1lll_opy_ = pabot._create_command_for_execution
    bstack11l1l11l1_opy_ = pabot._report_results
  if bstack1l1ll11l_opy_ == bstack1ll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ໩"):
    global bstack111l1l11_opy_
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11111lll1l_opy_(e, bstack1llll1lll1_opy_)
    bstack111ll111_opy_ = Runner.run_hook
    bstack11l11ll1l_opy_ = Runner.load_hooks
    bstack1lllll1ll_opy_ = Step.run
    try:
      sig = inspect.signature(bstack111ll111_opy_)
      params = list(sig.parameters.keys())
      bstack111l1l11_opy_ = bstack1ll_opy_ (u"ࠪࡧࡴࡴࡴࡦࡺࡷࠫ໪") in params
      logger.info(bstack1ll_opy_ (u"ࠫࡉ࡫ࡴࡦࡥࡷࡩࡩࠦࡢࡦࡪࡤࡺࡪࠦࡲࡶࡰࡢ࡬ࡴࡵ࡫ࠡࡵ࡬࡫ࡳࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨ໫").format(bstack1ll_opy_ (u"ࠬ࠷࠮࠳࠰࠹ࠤ࠭ࡽࡩࡵࡪࠣࡧࡴࡴࡴࡦࡺࡷ࠭ࠬ໬") if bstack111l1l11_opy_ else bstack1ll_opy_ (u"࠭࠱࠯࠵࠮ࠤ࠭ࡽࡩࡵࡪࡲࡹࡹࠦࡣࡰࡰࡷࡩࡽࡺࠩࠨ໭")))
    except Exception as e:
      logger.debug(bstack1ll_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡤࡶࠣࡦࡪ࡮ࡡࡷࡧࠣࡶࡺࡴ࡟ࡩࡱࡲ࡯ࠥࡹࡩࡨࡰࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬ໮").format(str(e)))
      bstack111l1l11_opy_ = None
  if bstack1l1ll11l_opy_ == bstack1ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ໯"):
    try:
      from _pytest.config import Config
      bstack1ll1l111ll_opy_ = Config.getoption
      from _pytest import runner
      bstack11l111l1ll_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warning(bstack1ll_opy_ (u"ࠤࠨࡷ࠿ࠦࠥࡴࠤ໰"), bstack1l1llll1l_opy_, str(e))
    try:
      from pytest_bdd import reporting
      bstack1ll111l1l_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1ll_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡲࠤࡷࡻ࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࡶࠫ໱"))
    if bstack1111l11ll1_opy_():
      logger.warning(bstack111l1l1111_opy_[bstack1ll_opy_ (u"ࠫࡘࡊࡋ࠮ࡉࡈࡒ࠲࠶࠰࠶ࠩ໲")])
  try:
    framework_name = bstack1ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ໳") if bstack1l1ll11l_opy_ in [bstack1ll_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ໴"), bstack1ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭໵"), bstack1ll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ໶")] else bstack1111lllll_opy_(bstack1l1ll11l_opy_)
    bstack11ll1ll11_opy_ = {
      bstack1ll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࠪ໷"): bstack1ll_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶ࠰ࡧࡺࡩࡵ࡮ࡤࡨࡶࠬ໸") if bstack1l1ll11l_opy_ == bstack1ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ໹") and bstack11lll11ll_opy_() else framework_name,
      bstack1ll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ໺"): bstack1ll1lll11l_opy_(framework_name),
      bstack1ll_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ໻"): __version__,
      bstack1ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨ໼"): bstack1l1ll11l_opy_
    }
    if bstack1l1ll11l_opy_ in bstack1111111ll_opy_ + bstack11lll11lll_opy_:
      if a11y.is_enabled_root(CONFIG):
        if bstack1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ໽") in CONFIG:
          os.environ[bstack1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ໾")] = os.getenv(bstack1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ໿"), json.dumps(CONFIG[bstack1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫༀ")]))
          CONFIG[bstack1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ༁")].pop(bstack1ll_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫ༂"), None)
          CONFIG[bstack1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ༃")].pop(bstack1ll_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭༄"), None)
        bstack1ll11l1ll_opy_ = bstack1ll_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭༅") if CONFIG.get(bstack1ll_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩ༆")) or bstack1l1111l1l1_opy_() else bstack1ll_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭༇")
        if bstack1ll11l1ll_opy_ == bstack1ll_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩ༈"):
          try:
            import importlib.metadata as _11lllll1ll_opy_
            bstack1lll1l1l11_opy_ = _11lllll1ll_opy_.version(bstack1ll_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ༉"))
          except Exception:
            bstack1lll1l1l11_opy_ = bstack1ll_opy_ (u"ࠧࡶࡰ࡮ࡲࡴࡽ࡮ࠨ༊")
        else:
          bstack1lll1l1l11_opy_ = str(bstack1ll11l11l1_opy_())
        bstack11ll1ll11_opy_[bstack1ll_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ་")] = {
          bstack1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ༌"): bstack1ll11l1ll_opy_,
          bstack1ll_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫ།"): bstack1lll1l1l11_opy_
        }
    bstack11ll11ll_opy_, bstack11lllllll1_opy_ = None, {}
    bstack1lllllll1ll_opy_ = None
    bstack11lll11l1_opy_ = None
    def bstack11llllll11_opy_():
      if bstack11ll1ll1l1_opy_:
        bstack1l1l111l11_opy_()
      elif bstack1ll1lll11_opy_:
        bstack11l11l1111_opy_()
    def bstack1l11l11l_opy_():
      nonlocal bstack11ll11ll_opy_, bstack11lllllll1_opy_
      if bstack1l1ll11l_opy_ not in [bstack1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ༎")] and not cli.is_running():
        bstack11ll11ll_opy_, bstack11lllllll1_opy_ = TestHubHandler.launch(CONFIG, bstack11ll1ll11_opy_)
    if bstack11ll1ll1l1_opy_ or bstack1ll1lll11_opy_:
      bstack1lllllll1ll_opy_ = threading.Thread(target=bstack11llllll11_opy_)
      bstack1lllllll1ll_opy_.start()
    if bstack1l1ll11l_opy_ not in [bstack1ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭༏")] and not cli.is_running():
      bstack11lll11l1_opy_ = threading.Thread(target=bstack1l11l11l_opy_)
      bstack11lll11l1_opy_.start()
    if bstack1lllllll1ll_opy_:
      bstack1lllllll1ll_opy_.join()
    if bstack11lll11l1_opy_:
      bstack11lll11l1_opy_.join()
    if bstack11lllllll1_opy_.get(bstack1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭༐")) is not None and a11y.bstack1l111l111l_opy_(CONFIG) is None:
      value = bstack11lllllll1_opy_[bstack1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ༑")].get(bstack1ll_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩ༒"))
      if value is not None:
          CONFIG[bstack1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ༓")] = value
      else:
        logger.debug(bstack1ll_opy_ (u"ࠥࡒࡴࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡤࡢࡶࡤࠤ࡫ࡵࡵ࡯ࡦࠣ࡭ࡳࠦࡲࡦࡵࡳࡳࡳࡹࡥࠣ༔"))
  except Exception as e:
    logger.debug(bstack1lll1l11_opy_.format(bstack1ll_opy_ (u"࡙ࠫ࡫ࡳࡵࡊࡸࡦࠬ༕"), str(e)))
  if bstack1l1ll11l_opy_ == bstack1ll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨ࠭༖"):
    PARALLELISE_VANILLA_PYTHON = True
    if bstack11l11l1l_opy_ and bstack1l1lll1l11_opy_:
      if cli.is_enabled(CONFIG):
        bstack1lll1111l1_opy_ = cli.config.get(bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ༗"), {}).get(bstack1ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳ༘ࠩ")) if cli.config else None
      else:
        bstack1lll1111l1_opy_ = CONFIG.get(bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷ༙ࠬ"), {}).get(bstack1ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ༚"))
      bstack11llllll_opy_(bstack11l11l1l1_opy_)
    elif bstack11l11l1l_opy_:
      if cli.is_enabled(CONFIG):
        bstack1lll1111l1_opy_ = cli.config.get(bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ༛"), {}).get(bstack1ll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭༜")) if cli.config else None
      else:
        bstack1lll1111l1_opy_ = CONFIG.get(bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ༝"), {}).get(bstack1ll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ༞"))
      global bstack1ll111ll1l_opy_
      try:
        if bstack11l1llll_opy_(bstack11l11l1l_opy_[bstack1ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ༟")]) and multiprocessing.current_process().name == bstack1ll_opy_ (u"ࠨ࠲ࠪ༠"):
          bstack11l11l1l_opy_[bstack1ll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ༡")].remove(bstack1ll_opy_ (u"ࠪ࠱ࡲ࠭༢"))
          bstack11l11l1l_opy_[bstack1ll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ༣")].remove(bstack1ll_opy_ (u"ࠬࡶࡤࡣࠩ༤"))
          bstack11l11l1l_opy_[bstack1ll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ༥")] = bstack11l11l1l_opy_[bstack1ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ༦")][0]
          with open(bstack11l11l1l_opy_[bstack1ll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ༧")], bstack1ll_opy_ (u"ࠩࡵࠫ༨")) as f:
            file_content = f.read()
          bstack1llll1llll_opy_ = bstack1ll_opy_ (u"ࠥࠦࠧ࡬ࡲࡰ࡯ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡨࡰࠦࡩ࡮ࡲࡲࡶࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦ࠽ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪ࠮ࡻࡾࠫ࠾ࠤ࡫ࡸ࡯࡮ࠢࡳࡨࡧࠦࡩ࡮ࡲࡲࡶࡹࠦࡐࡥࡤ࠾ࠤࡴ࡭࡟ࡥࡤࠣࡁࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡦࡨࡪࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠩࡵࡨࡰ࡫࠲ࠠࡢࡴࡪ࠰ࠥࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠡ࠿ࠣ࠴࠮ࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺࡲࡺ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡥࡷ࡭ࠠ࠾ࠢࡶࡸࡷ࠮ࡩ࡯ࡶࠫࡥࡷ࡭ࠩࠬ࠳࠳࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡩࡽࡩࡥࡱࡶࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡡࡴࠢࡨ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡶࡡࡴࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡱࡪࡣࡩࡨࠨࡴࡧ࡯ࡪ࠱ࡧࡲࡨ࠮ࡷࡩࡲࡶ࡯ࡳࡣࡵࡽ࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡓࡨࡧ࠴ࡤࡰࡡࡥࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮ࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣࠪࠬ࠲ࡸ࡫ࡴࡠࡶࡵࡥࡨ࡫ࠨࠪ࡞ࡱࠦࠧࠨ༩").format(str(bstack11l11l1l_opy_))
          bstack11ll111ll_opy_ = bstack1llll1llll_opy_ + file_content
          bstack1lll11111l_opy_ = bstack11l11l1l_opy_[bstack1ll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ༪")] + bstack1ll_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥࡴࡦ࡯ࡳ࠲ࡵࡿࠧ༫")
          with open(bstack1lll11111l_opy_, bstack1ll_opy_ (u"࠭ࡷࠨ༬")):
            pass
          with open(bstack1lll11111l_opy_, bstack1ll_opy_ (u"ࠢࡸ࠭ࠥ༭")) as f:
            f.write(bstack11ll111ll_opy_)
          import subprocess
          bstack1lll1l111l_opy_ = subprocess.run([bstack1ll_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࠣ༮"), bstack1lll11111l_opy_])
          if os.path.exists(bstack1lll11111l_opy_):
            os.unlink(bstack1lll11111l_opy_)
          os._exit(bstack1lll1l111l_opy_.returncode)
        else:
          if bstack11l1llll_opy_(bstack11l11l1l_opy_[bstack1ll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ༯")]):
            bstack11l11l1l_opy_[bstack1ll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭༰")].remove(bstack1ll_opy_ (u"ࠫ࠲ࡳࠧ༱"))
            bstack11l11l1l_opy_[bstack1ll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ༲")].remove(bstack1ll_opy_ (u"࠭ࡰࡥࡤࠪ༳"))
            bstack11l11l1l_opy_[bstack1ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ༴")] = bstack11l11l1l_opy_[bstack1ll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨ༵ࠫ")][0]
          bstack11llllll_opy_(bstack11l11l1l1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack11l11l1l_opy_[bstack1ll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ༶")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1ll_opy_ (u"ࠪࡣࡤࡴࡡ࡮ࡧࡢࡣ༷ࠬ")] = bstack1ll_opy_ (u"ࠫࡤࡥ࡭ࡢ࡫ࡱࡣࡤ࠭༸")
          mod_globals[bstack1ll_opy_ (u"ࠬࡥ࡟ࡧ࡫࡯ࡩࡤࡥ༹ࠧ")] = os.path.abspath(bstack11l11l1l_opy_[bstack1ll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ༺")])
          exec(open(bstack11l11l1l_opy_[bstack1ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ༻")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1ll_opy_ (u"ࠨࡅࡤࡹ࡬࡮ࡴࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠨ༼").format(str(e)))
          for driver in bstack1ll111ll1l_opy_:
            bstack11ll1l1ll_opy_.append({
              bstack1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ༽"): bstack11l11l1l_opy_[bstack1ll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭༾")],
              bstack1ll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ༿"): str(e),
              bstack1ll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫཀ"): multiprocessing.current_process().name
            })
            bstack1l111l1l1l_opy_(driver, bstack1ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ཁ"), bstack1ll_opy_ (u"ࠢࡔࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥག") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1ll111ll1l_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack11l1llllll_opy_, CONFIG, logger)
      bstack1l1llll1l1_opy_()
      bstack11l1lllll_opy_()
      percy.bstack111111l11_opy_()
      bstack11l11lll_opy_ = {
        bstack1ll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫགྷ"): args[0],
        bstack1ll_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩང"): CONFIG,
        bstack1ll_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫཅ"): bstack1ll1111l1_opy_,
        bstack1ll_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ཆ"): bstack11l1llllll_opy_
      }
      if bstack1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨཇ") in CONFIG:
        bstack111llll1l_opy_ = bstack11ll1l1l1l_opy_(args, logger, CONFIG, BROWSERSTACK_AUTOMATION, bstack1l11ll11l1_opy_)
        bstack1l11l11ll1_opy_ = bstack111llll1l_opy_.bstack111l11l1ll_opy_(run_on_browserstack, bstack11l11lll_opy_, bstack11l1llll_opy_(args))
      else:
        if bstack11l1llll_opy_(args):
          bstack11l1l111l_opy_ = multiprocessing.get_context(bstack1ll_opy_ (u"࠭ࡳࡱࡣࡺࡲࠬ཈"))
          bstack11l11lll_opy_[bstack1ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪཉ")] = args
          test = bstack11l1l111l_opy_.Process(name=str(0),
                                target=run_on_browserstack, args=(bstack11l11lll_opy_,))
          test.start()
          test.join()
        else:
          bstack11llllll_opy_(bstack11l11l1l1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1ll_opy_ (u"ࠨࡡࡢࡲࡦࡳࡥࡠࡡࠪཊ")] = bstack1ll_opy_ (u"ࠩࡢࡣࡲࡧࡩ࡯ࡡࡢࠫཋ")
          mod_globals[bstack1ll_opy_ (u"ࠪࡣࡤ࡬ࡩ࡭ࡧࡢࡣࠬཌ")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1l1ll11l_opy_ == bstack1ll_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪཌྷ") or bstack1l1ll11l_opy_ == bstack1ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫཎ"):
    percy.init(bstack11l1llllll_opy_, CONFIG, logger)
    percy.bstack111111l11_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack11111lll1l_opy_(e, bstack1ll1lll1ll_opy_)
    bstack1l1llll1l1_opy_()
    if bstack1lll1111l1_opy_:
      os.environ[bstack1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡊࡅࡇࡃࡘࡐ࡙ࡥࡌࡐࡅࡄࡐࡤࡏࡄࠨཏ")] = bstack1lll1111l1_opy_
    bstack11llllll_opy_(bstack11l1ll11_opy_)
    if BROWSERSTACK_AUTOMATION:
      bstack11l1l11l1l_opy_(bstack11l1ll11_opy_, args)
      if bstack1ll_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬཐ") in args:
        i = args.index(bstack1ll_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ད"))
        args.pop(i)
        args.pop(i)
      if bstack1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬདྷ") not in CONFIG:
        CONFIG[bstack1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ན")] = [{}]
        bstack1l11ll11l1_opy_ = 1
      if bstack1111l1l1ll_opy_ == 0:
        bstack1111l1l1ll_opy_ = 1
      args.insert(0, str(bstack1111l1l1ll_opy_))
      args.insert(0, str(bstack1ll_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩཔ")))
    if TestHubHandler.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack111111l11l_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack11111ll1l1_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack1ll_opy_ (u"ࠧࡘࡏࡃࡑࡗࡣࡔࡖࡔࡊࡑࡑࡗࠧཕ"),
        ).parse_args(bstack111111l11l_opy_)
        bstack11l1111lll_opy_ = args.index(bstack111111l11l_opy_[0]) if len(bstack111111l11l_opy_) > 0 else len(args)
        args.insert(bstack11l1111lll_opy_, str(bstack1ll_opy_ (u"࠭࠭࠮࡮࡬ࡷࡹ࡫࡮ࡦࡴࠪབ")))
        args.insert(bstack11l1111lll_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡳࡱࡥࡳࡹࡥ࡬ࡪࡵࡷࡩࡳ࡫ࡲ࠯ࡲࡼࠫབྷ"))))
        if bstack1l111111ll_opy_.bstack1ll11llll_opy_(CONFIG):
          args.insert(bstack11l1111lll_opy_, str(bstack1ll_opy_ (u"ࠨ࠯࠰ࡰ࡮ࡹࡴࡦࡰࡨࡶࠬམ")))
          args.insert(bstack11l1111lll_opy_ + 1, str(bstack1ll_opy_ (u"ࠩࡕࡩࡹࡸࡹࡇࡣ࡬ࡰࡪࡪ࠺ࡼࡿࠪཙ").format(bstack1l111111ll_opy_.bstack1111l11111_opy_(CONFIG))))
        if bstack11l1l1l11l_opy_(os.environ.get(bstack1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠨཚ"))) and str(os.environ.get(bstack1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠨཛ"), bstack1ll_opy_ (u"ࠬࡴࡵ࡭࡮ࠪཛྷ"))) != bstack1ll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫཝ"):
          for bstack111l1ll1ll_opy_ in bstack11111ll1l1_opy_:
            args.remove(bstack111l1ll1ll_opy_)
          test_files = os.environ.get(bstack1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠫཞ")).split(bstack1ll_opy_ (u"ࠨ࠮ࠪཟ"))
          for bstack111llll1l1_opy_ in test_files:
            args.append(bstack111llll1l1_opy_)
      except Exception as e:
        logger.error(bstack1ll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡢࡶࡷࡥࡨ࡮ࡩ࡯ࡩࠣࡰ࡮ࡹࡴࡦࡰࡨࡶࠥ࡬࡯ࡳࠢࡾࢁ࠳ࠦࡅࡳࡴࡲࡶࠥ࠳ࠠࡼࡿࠥའ").format(bstack1lll1ll11l_opy_, e))
    pabot.main(args)
  elif bstack1l1ll11l_opy_ == bstack1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫཡ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack11111lll1l_opy_(e, bstack1ll1lll1ll_opy_)
    for a in args:
      if bstack1ll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚ࠪར") in a:
        PLATFORM_INDEX = int(a.split(bstack1ll_opy_ (u"ࠬࡀࠧལ"))[1])
      if bstack1ll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪཤ") in a:
        bstack1lll1111l1_opy_ = str(a.split(bstack1ll_opy_ (u"ࠧ࠻ࠩཥ"))[1])
      if bstack1ll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓࠨས") in a:
        bstack1l111ll1_opy_ = str(a.split(bstack1ll_opy_ (u"ࠩ࠽ࠫཧ"))[1])
    if os.environ.get(bstack1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡇࡉࡋࡇࡕࡍࡖࡢࡐࡔࡉࡁࡍࡡࡌࡈࠬཨ")):
      bstack1lll1111l1_opy_ = os.environ.get(bstack1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡈࡊࡌࡁࡖࡎࡗࡣࡑࡕࡃࡂࡎࡢࡍࡉ࠭ཀྵ"))
    if bstack1lll1111l1_opy_:
      if bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩཪ") not in CONFIG:
        CONFIG[bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪཫ")] = {}
      CONFIG[bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫཬ")][bstack1ll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ཭")] = bstack1lll1111l1_opy_
    bstack1l1l1lll1_opy_ = None
    bstack11l111ll1_opy_ = None
    if bstack1ll_opy_ (u"ࠩ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠨ཮") in args:
      i = args.index(bstack1ll_opy_ (u"ࠪ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠩ཯"))
      args.pop(i)
      bstack1l1l1lll1_opy_ = args.pop(i)
    if bstack1ll_opy_ (u"ࠫ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࠧ཰") in args:
      i = args.index(bstack1ll_opy_ (u"ࠬ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸࠨཱ"))
      args.pop(i)
      bstack11l111ll1_opy_ = args.pop(i)
    if bstack1l1l1lll1_opy_ is not None:
      global bstack1lll1ll1l1_opy_
      bstack1lll1ll1l1_opy_ = bstack1l1l1lll1_opy_
    if bstack11l111ll1_opy_ is not None and int(PLATFORM_INDEX) < 0:
      PLATFORM_INDEX = int(bstack11l111ll1_opy_)
    if cli.is_enabled(CONFIG):
      if cli.bstack1l1ll1l11_opy_():
        bstack111l1lll11_opy_.invoke(Events.CONNECT, bstack11111l11_opy_())
        cli.bstack11l1l111ll_opy_(PLATFORM_INDEX)
      if cli.bstack111l11l11_opy_(bstack1llll1111l_opy_):
        cli.bstack1lllll1lll1_opy_()
    bstack11llllll_opy_(bstack11l1ll11_opy_)
    run_cli(args)
    if bstack1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶིࠪ") in multiprocessing.current_process().__dict__.keys():
      for bstack1l1111l1_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack11ll1l1ll_opy_.append(bstack1l1111l1_opy_)
  elif bstack1l1ll11l_opy_ == bstack1ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺཱིࠧ"):
    bstack1l11l1ll_opy_ = bstack1l11ll1l11_opy_(args, logger, CONFIG, BROWSERSTACK_AUTOMATION)
    bstack1l11l1ll_opy_.bstack1lll1l1ll_opy_()
    bstack1l1llll1l1_opy_()
    PARALLELISE_THREADING_PYTHON = True
    bstack111ll111ll_opy_ = bstack1l11l1ll_opy_.bstack1llll111_opy_()
    bstack1l11l1ll_opy_.bstack11l11lll_opy_(bstack11llll1l1l_opy_)
    bstack1l11l1ll_opy_.bstack1ll1l1l11_opy_()
    bstack1ll1ll1l1_opy_(bstack1l1ll11l_opy_, CONFIG, bstack1l11l1ll_opy_.bstack1111lll11_opy_())
    bstack1l11ll1lll_opy_.end(EVENTS.bstack1l1ll1111l_opy_.value, EVENTS.bstack1l1ll1111l_opy_.value + bstack1ll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴུࠣ"), EVENTS.bstack1l1ll1111l_opy_.value + bstack1ll_opy_ (u"ࠤ࠽ࡩࡳࡪཱུࠢ"), status=True, failure=None, test_name=SESSION_NAME)
    bstack111lll11l1_opy_ = bstack1l11l1ll_opy_.bstack111l11l1ll_opy_(bstack1llllll1l1_opy_, {
      bstack1ll_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪྲྀ"): CONFIG,
      bstack1ll_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬཷ"): bstack1ll1111l1_opy_,
      bstack1ll_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧླྀ"): bstack11l1llllll_opy_,
      bstack1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩཹ"): BROWSERSTACK_AUTOMATION,
      bstack1ll_opy_ (u"ࠧࡐࡘࡈࡖࡗࡏࡄࡆࡡࡏࡓࡆࡊ࡟ࡕࡇࡖࡘࡎࡔࡇࠨེ"): bstack1lll111111_opy_
    })
    if not bstack11l11l1l_opy_:
      bstack1l1llllll1_opy_ = bstack1l11l1ll11_opy_.bstack1111ll1111_opy_(EVENTS.bstack11ll1111_opy_.value)
    try:
      bstack1ll1l1l1l_opy_, bstack1ll1ll11l_opy_ = map(list, zip(*bstack111lll11l1_opy_))
      bstack1l1l1ll11_opy_ = bstack1ll1l1l1l_opy_[0]
      for status_code in bstack1ll1ll11l_opy_:
        if status_code != 0:
          bstack11111ll11l_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack1ll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡧࡶࡦࠢࡨࡶࡷࡵࡲࡴࠢࡤࡲࡩࠦࡳࡵࡣࡷࡹࡸࠦࡣࡰࡦࡨ࠲ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࠼ࠣࡿࢂࠨཻ").format(str(e)))
  elif bstack1l1ll11l_opy_ == bstack1ll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦོࠩ"):
    try:
      from behave.__main__ import main as bstack11lll1l11_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack11111lll1l_opy_(e, bstack1llll1lll1_opy_)
    bstack1l1llll1l1_opy_()
    PARALLELISE_THREADING_PYTHON = True
    bstack1ll111111_opy_ = 1
    if bstack1ll_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ཽࠪ") in CONFIG:
      bstack1ll111111_opy_ = CONFIG[bstack1ll_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫཾ")]
    if bstack1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨཿ") in CONFIG:
      bstack11ll1l11ll_opy_ = int(bstack1ll111111_opy_) * int(len(CONFIG[bstack1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴྀࠩ")]))
    else:
      bstack11ll1l11ll_opy_ = int(bstack1ll111111_opy_)
    config = Configuration(args)
    bstack1ll1l11ll_opy_ = config.paths
    if len(bstack1ll1l11ll_opy_) == 0:
      import glob
      pattern = bstack1ll_opy_ (u"ࠧࠫࠬ࠲࠮࠳࡬ࡥࡢࡶࡸࡶࡪཱྀ࠭")
      bstack1l1lll11l_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1l1lll11l_opy_)
      config = Configuration(args)
      bstack1ll1l11ll_opy_ = config.paths
    bstack11ll111l1l_opy_ = [os.path.normpath(item) for item in bstack1ll1l11ll_opy_]
    bstack11l11lll1_opy_ = [os.path.normpath(item) for item in args]
    bstack11l1l1l11_opy_ = [item for item in bstack11l11lll1_opy_ if item not in bstack11ll111l1l_opy_]
    import platform as pf
    if pf.system().lower() == bstack1ll_opy_ (u"ࠨࡹ࡬ࡲࡩࡵࡷࡴࠩྂ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack11ll111l1l_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l11ll1l1l_opy_)))
                    for bstack1l11ll1l1l_opy_ in bstack11ll111l1l_opy_]
    try:
      bstack1l1l1l11_opy_ = bstack1lll1lll1l_opy_(args, logger, CONFIG, BROWSERSTACK_AUTOMATION)
      bstack1l1l1l11_opy_.bstack11l11l1l1l_opy_(bstack11ll111l1l_opy_)
      bstack1l1l1l11_opy_.bstack1ll1l1l11_opy_()
      bstack11ll111l1l_opy_ = bstack1l1l1l11_opy_.bstack1llllll1ll_opy_()
    except Exception as e:
      logger.error(bstack1ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡧࡰࡱ࡮ࡼࠤࡹ࡫ࡳࡵࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡩࡳࡷࠦࡢࡦࡪࡤࡺࡪࡀࠠࠦࡵࠥྃ"), e, exc_info=True)
      logger.info(bstack1ll_opy_ (u"ࠥࡇࡴࡴࡴࡪࡰࡸ࡭ࡳ࡭ࠠࡸ࡫ࡷ࡬ࠥࡵࡲࡪࡩ࡬ࡲࡦࡲࠠࡴࡲࡨࡧࠥ࡬ࡩ࡭ࡧࡶࠤࡼ࡯ࡴࡩࡱࡸࡸࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ྄ࠧ"))
    bstack111llll111_opy_ = []
    for spec in bstack11ll111l1l_opy_:
      bstack1111llllll_opy_ = []
      bstack1111llllll_opy_ += bstack11l1l1l11_opy_
      bstack1111llllll_opy_.append(spec)
      bstack111llll111_opy_.append(bstack1111llllll_opy_)
    execution_items = []
    for bstack1111llllll_opy_ in bstack111llll111_opy_:
      if bstack1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ྅") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ྆")]):
          item = {}
          item[bstack1ll_opy_ (u"࠭ࡡࡳࡩࠪ྇")] = bstack1ll_opy_ (u"ࠧࠡࠩྈ").join(bstack1111llllll_opy_)
          item[bstack1ll_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧྉ")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack1ll_opy_ (u"ࠩࡤࡶ࡬࠭ྊ")] = bstack1ll_opy_ (u"ࠪࠤࠬྋ").join(bstack1111llllll_opy_)
        item[bstack1ll_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪྌ")] = 0
        execution_items.append(item)
    bstack11ll111ll1_opy_ = bstack11ll1l1ll1_opy_(execution_items, bstack11ll1l11ll_opy_)
    for execution_item in bstack11ll111ll1_opy_:
      bstack11l1llll1l_opy_ = []
      for item in execution_item:
        bstack11l1llll1l_opy_.append(bstack1ll1111l11_opy_(name=str(item[bstack1ll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫྍ")]),
                                             target=bstack1llllll1111_opy_,
                                             args=(item[bstack1ll_opy_ (u"࠭ࡡࡳࡩࠪྎ")],)))
      for t in bstack11l1llll1l_opy_:
        t.start()
      for t in bstack11l1llll1l_opy_:
        t.join()
  else:
    bstack1ll11l11ll_opy_(bstack1l1llll111_opy_)
  if not bstack11l11l1l_opy_:
    bstack11lll1l11l_opy_()
    if bstack1l1llllll1_opy_:
      bstack1l11l1ll11_opy_.end(EVENTS.bstack11ll1111_opy_.value, bstack1l1llllll1_opy_ + bstack1ll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢྏ"), bstack1l1llllll1_opy_ + bstack1ll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨྐ"), status=True, failure=None, test_name=None)
  logger_utils.bstack11ll1lll1_opy_()
def browserstack_initialize(bstack1lllllllll_opy_=None):
  logger.info(bstack1ll_opy_ (u"ࠩࡕࡹࡳࡴࡩ࡯ࡩࠣࡗࡉࡑࠠࡸ࡫ࡷ࡬ࠥࡧࡲࡨࡵ࠽ࠤࠬྑ") + str(bstack1lllllllll_opy_))
  run_on_browserstack(bstack1lllllllll_opy_, None, True)
@measure(event_name=EVENTS.bstack1lll1111_opy_, stage=STAGE.bstack11llll111l_opy_, bstack111l11111_opy_=SESSION_NAME)
def bstack11lll1l11l_opy_():
  global CONFIG
  global bstack1ll11ll1l1_opy_
  global bstack11111ll11l_opy_
  global bstack1l1lllll11_opy_
  global global_config
  global _11llll1ll1_opy_
  bstack1l11l1lll1_opy_.bstack111ll1l1l1_opy_()
  _11llll1ll1_opy_ = cli.is_running()
  if _11llll1ll1_opy_:
    bstack111l1lll11_opy_.invoke(Events.bstack1l1ll11ll_opy_)
  else:
    bstack1ll1ll1ll_opy_ = bstack1l111111ll_opy_.bstack1l111l1111_opy_(config=CONFIG)
    bstack1ll1ll1ll_opy_.bstack1l1111ll11_opy_(CONFIG)
  hashed_id = None
  bstack1l11l111l1_opy_ = None
  def bstack111llllll_opy_():
    try:
      if bstack1ll11ll1l1_opy_ == bstack1ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪྒ"):
        if not cli.is_enabled(CONFIG):
          TestHubHandler.stop()
      else:
        TestHubHandler.stop()
    except Exception as e:
      logger.debug(bstack1ll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡷࡹࡵࡰࡱ࡫ࡱ࡫࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࡼࡿࠥྒྷ").format(e))
  def bstack1ll11l1l1_opy_():
    try:
      if not cli.is_enabled(CONFIG):
        bstack111l111ll1_opy_.bstack1l1lllll1l_opy_()
    except Exception as e:
      logger.debug(bstack1ll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡵࡸࡩ࡯ࡶ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࠥࡲࡩ࡯࡭࠽ࠤࢀࢃࠢྔ").format(e))
  def bstack1l1ll11111_opy_():
    nonlocal hashed_id, bstack1l11l111l1_opy_
    try:
      if bstack1ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪྕ") in CONFIG and str(CONFIG[bstack1ll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫྖ")]).lower() != bstack1ll_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧྗ"):
        hashed_id, bstack1l11l111l1_opy_ = bstack1l1lll1ll1_opy_()
      else:
        hashed_id, bstack1l11l111l1_opy_ = get_build_link()
    except Exception as e:
      logger.debug(bstack1ll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡥࡹ࡮ࡲࡤࠡ࡮࡬ࡲࡰࡀࠠࡼࡿࠥ྘").format(e))
  bstack1ll11l1l11_opy_ = threading.Thread(target=bstack111llllll_opy_)
  bstack1l111ll111_opy_ = threading.Thread(target=bstack1ll11l1l1_opy_)
  bstack1l11l1l111_opy_ = threading.Thread(target=bstack1l1ll11111_opy_)
  threads = [bstack1ll11l1l11_opy_, bstack1l111ll111_opy_, bstack1l11l1l111_opy_]
  for thread in threads:
    try:
      thread.start()
    except Exception as e:
      logger.debug(bstack1ll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡶࡸࡦࡸࡴࡪࡰࡪࠤࡹ࡮ࡲࡦࡣࡧࠤࢀࢃ࠺ࠡࡽࢀࠦྙ").format(thread.name, e))
  for thread in threads:
    try:
      thread.join()
    except Exception as e:
      logger.debug(bstack1ll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡮ࡴ࡯࡮ࡪࡰࡪࠤࡹ࡮ࡲࡦࡣࡧࠤࢀࢃ࠺ࠡࡽࢀࠦྚ").format(thread.name, e))
  bstack11lll1ll_opy_(hashed_id)
  logger.info(bstack1ll_opy_ (u"࡙ࠬࡄࡌࠢࡵࡹࡳࠦࡥ࡯ࡦࡨࡨࠥ࡬࡯ࡳࠢ࡬ࡨ࠿࠭ྛ") + global_config.get_property(bstack1ll_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨྜ"), bstack1ll_opy_ (u"ࠧࠨྜྷ")) + bstack1ll_opy_ (u"ࠨ࠮ࠣࡸࡪࡹࡴࡩࡷࡥࠤ࡮ࡪ࠺ࠡࠩྞ") + os.getenv(bstack1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧྟ"), bstack1ll_opy_ (u"ࠪࠫྠ")))
  if hashed_id is not None and bstack111l1l11l1_opy_() != -1:
    sessions = bstack111l11l1l1_opy_(hashed_id)
    bstack1ll1l1l111_opy_(sessions, bstack1l11l111l1_opy_)
  if bstack1ll11ll1l1_opy_ == bstack1ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫྡ") and bstack11111ll11l_opy_ != 0:
    sys.exit(bstack11111ll11l_opy_)
  if bstack1ll11ll1l1_opy_ == bstack1ll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬྡྷ") and bstack1l1lllll11_opy_ != 0:
    sys.exit(bstack1l1lllll11_opy_)
def bstack11lll1ll_opy_(new_id):
    global bstack1l1ll111_opy_
    bstack1l1ll111_opy_ = new_id
def bstack1111lllll_opy_(bstack1l1l11l11_opy_):
  if bstack1l1l11l11_opy_:
    return bstack1l1l11l11_opy_.capitalize()
  else:
    return bstack1ll_opy_ (u"࠭ࠧྣ")
@measure(event_name=EVENTS.bstack1ll111ll1_opy_, stage=STAGE.bstack11llll111l_opy_, bstack111l11111_opy_=SESSION_NAME)
def bstack111l111l_opy_(bstack1l11l11lll_opy_):
  if bstack1ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬྤ") in bstack1l11l11lll_opy_ and bstack1l11l11lll_opy_[bstack1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ྥ")] != bstack1ll_opy_ (u"ࠩࠪྦ"):
    return bstack1l11l11lll_opy_[bstack1ll_opy_ (u"ࠪࡲࡦࡳࡥࠨྦྷ")]
  else:
    bstack111l11111_opy_ = bstack1ll_opy_ (u"ࠦࠧྨ")
    if bstack1ll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬྩ") in bstack1l11l11lll_opy_ and bstack1l11l11lll_opy_[bstack1ll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ྪ")] != None:
      bstack111l11111_opy_ += bstack1l11l11lll_opy_[bstack1ll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧྫ")] + bstack1ll_opy_ (u"ࠣ࠮ࠣࠦྫྷ")
      if bstack1l11l11lll_opy_[bstack1ll_opy_ (u"ࠩࡲࡷࠬྭ")] == bstack1ll_opy_ (u"ࠥ࡭ࡴࡹࠢྮ"):
        bstack111l11111_opy_ += bstack1ll_opy_ (u"ࠦ࡮ࡕࡓࠡࠤྯ")
      bstack111l11111_opy_ += (bstack1l11l11lll_opy_[bstack1ll_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩྰ")] or bstack1ll_opy_ (u"࠭ࠧྱ"))
      return bstack111l11111_opy_
    else:
      bstack111l11111_opy_ += bstack1111lllll_opy_(bstack1l11l11lll_opy_[bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨྲ")]) + bstack1ll_opy_ (u"ࠣࠢࠥླ") + (
              bstack1l11l11lll_opy_[bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫྴ")] or bstack1ll_opy_ (u"ࠪࠫྵ")) + bstack1ll_opy_ (u"ࠦ࠱ࠦࠢྶ")
      if bstack1l11l11lll_opy_[bstack1ll_opy_ (u"ࠬࡵࡳࠨྷ")] == bstack1ll_opy_ (u"ࠨࡗࡪࡰࡧࡳࡼࡹࠢྸ"):
        bstack111l11111_opy_ += bstack1ll_opy_ (u"ࠢࡘ࡫ࡱࠤࠧྐྵ")
      bstack111l11111_opy_ += bstack1l11l11lll_opy_[bstack1ll_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬྺ")] or bstack1ll_opy_ (u"ࠩࠪྻ")
      return bstack111l11111_opy_
@measure(event_name=EVENTS.bstack1l111l1lll_opy_, stage=STAGE.bstack11llll111l_opy_, bstack111l11111_opy_=SESSION_NAME)
def bstack11llll11_opy_(bstack11l1ll1lll_opy_):
  if bstack11l1ll1lll_opy_ == bstack1ll_opy_ (u"ࠥࡨࡴࡴࡥࠣྼ"):
    return bstack1ll_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡧࡳࡧࡨࡲࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡧࡳࡧࡨࡲࠧࡄࡃࡰ࡯ࡳࡰࡪࡺࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ྽")
  elif bstack11l1ll1lll_opy_ == bstack1ll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ྾"):
    return bstack1ll_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡴࡨࡨࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡲࡦࡦࠥࡂࡋࡧࡩ࡭ࡧࡧࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩ྿")
  elif bstack11l1ll1lll_opy_ == bstack1ll_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ࿀"):
    return bstack1ll_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽࡫ࡷ࡫ࡥ࡯࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥ࡫ࡷ࡫ࡥ࡯ࠤࡁࡔࡦࡹࡳࡦࡦ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨ࿁")
  elif bstack11l1ll1lll_opy_ == bstack1ll_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣ࿂"):
    return bstack1ll_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡸࡥࡥ࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡶࡪࡪࠢ࠿ࡇࡵࡶࡴࡸ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ࿃")
  elif bstack11l1ll1lll_opy_ == bstack1ll_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࠧ࿄"):
    return bstack1ll_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࠤࡧࡨࡥ࠸࠸࠶࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࠦࡩࡪࡧ࠳࠳࠸ࠥࡂ࡙࡯࡭ࡦࡱࡸࡸࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪ࿅")
  elif bstack11l1ll1lll_opy_ == bstack1ll_opy_ (u"ࠨࡲࡶࡰࡱ࡭ࡳ࡭࿆ࠢ"):
    return bstack1ll_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡥࡰࡦࡩ࡫࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡥࡰࡦࡩ࡫ࠣࡀࡕࡹࡳࡴࡩ࡯ࡩ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨ࿇")
  else:
    return bstack1ll_opy_ (u"ࠨ࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡧࡲࡡࡤ࡭࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡧࡲࡡࡤ࡭ࠥࡂࠬ࿈") + bstack1111lllll_opy_(
      bstack11l1ll1lll_opy_) + bstack1ll_opy_ (u"ࠩ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨ࿉")
def bstack11ll1llll_opy_(session):
  return bstack1ll_opy_ (u"ࠪࡀࡹࡸࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡳࡱࡺࠦࡃࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠠࡴࡧࡶࡷ࡮ࡵ࡮࠮ࡰࡤࡱࡪࠨ࠾࠽ࡣࠣ࡬ࡷ࡫ࡦ࠾ࠤࡾࢁࠧࠦࡴࡢࡴࡪࡩࡹࡃࠢࡠࡤ࡯ࡥࡳࡱࠢ࠿ࡽࢀࡀ࠴ࡧ࠾࠽࠱ࡷࡨࡃࢁࡽࡼࡿ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁ࠵ࡴࡳࡀࠪ࿊").format(
    session[bstack1ll_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦࡣࡺࡸ࡬ࠨ࿋")], bstack111l111l_opy_(session), bstack11llll11_opy_(session[bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡸࡺࡡࡵࡷࡶࠫ࿌")]),
    bstack11llll11_opy_(session[bstack1ll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭࿍")]),
    bstack1111lllll_opy_(session[bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ࿎")] or session[bstack1ll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨ࿏")] or bstack1ll_opy_ (u"ࠩࠪ࿐")) + bstack1ll_opy_ (u"ࠥࠤࠧ࿑") + (session[bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭࿒")] or bstack1ll_opy_ (u"ࠬ࠭࿓")),
    session[bstack1ll_opy_ (u"࠭࡯ࡴࠩ࿔")] + bstack1ll_opy_ (u"ࠢࠡࠤ࿕") + session[bstack1ll_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ࿖")], session[bstack1ll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫ࿗")] or bstack1ll_opy_ (u"ࠪࠫ࿘"),
    session[bstack1ll_opy_ (u"ࠫࡨࡸࡥࡢࡶࡨࡨࡤࡧࡴࠨ࿙")] if session[bstack1ll_opy_ (u"ࠬࡩࡲࡦࡣࡷࡩࡩࡥࡡࡵࠩ࿚")] else bstack1ll_opy_ (u"࠭ࠧ࿛"))
@measure(event_name=EVENTS.bstack1lllll1l1_opy_, stage=STAGE.bstack11llll111l_opy_, bstack111l11111_opy_=SESSION_NAME)
def bstack1ll1l1l111_opy_(sessions, bstack1l11l111l1_opy_):
  try:
    bstack1l11l111ll_opy_ = bstack1ll_opy_ (u"ࠢࠣ࿜")
    if not os.path.exists(bstack1111l111l_opy_):
      os.mkdir(bstack1111l111l_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll_opy_ (u"ࠨࡣࡶࡷࡪࡺࡳ࠰ࡴࡨࡴࡴࡸࡴ࠯ࡪࡷࡱࡱ࠭࿝")), bstack1ll_opy_ (u"ࠩࡵࠫ࿞")) as f:
      bstack1l11l111ll_opy_ = f.read()
    bstack1l11l111ll_opy_ = bstack1l11l111ll_opy_.replace(bstack1ll_opy_ (u"ࠪࡿࠪࡘࡅࡔࡗࡏࡘࡘࡥࡃࡐࡗࡑࡘࠪࢃࠧ࿟"), str(len(sessions)))
    bstack1l11l111ll_opy_ = bstack1l11l111ll_opy_.replace(bstack1ll_opy_ (u"ࠫࢀࠫࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠧࢀࠫ࿠"), bstack1l11l111l1_opy_)
    bstack1l11l111ll_opy_ = bstack1l11l111ll_opy_.replace(bstack1ll_opy_ (u"ࠬࢁࠥࡃࡗࡌࡐࡉࡥࡎࡂࡏࡈࠩࢂ࠭࿡"),
                                              sessions[0].get(bstack1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡴࡡ࡮ࡧࠪ࿢")) if sessions[0] else bstack1ll_opy_ (u"ࠧࠨ࿣"))
    with open(os.path.join(bstack1111l111l_opy_, bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡳࡧࡳࡳࡷࡺ࠮ࡩࡶࡰࡰࠬ࿤")), bstack1ll_opy_ (u"ࠩࡺࠫ࿥")) as stream:
      stream.write(bstack1l11l111ll_opy_.split(bstack1ll_opy_ (u"ࠪࡿ࡙ࠪࡅࡔࡕࡌࡓࡓ࡙࡟ࡅࡃࡗࡅࠪࢃࠧ࿦"))[0])
      for session in sessions:
        stream.write(bstack11ll1llll_opy_(session))
      stream.write(bstack1l11l111ll_opy_.split(bstack1ll_opy_ (u"ࠫࢀࠫࡓࡆࡕࡖࡍࡔࡔࡓࡠࡆࡄࡘࡆࠫࡽࠨ࿧"))[1])
    logger.info(bstack1ll_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡫ࡤࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡣࡷ࡬ࡰࡩࠦࡡࡳࡶ࡬ࡪࡦࡩࡴࡴࠢࡤࡸࠥࢁࡽࠨ࿨").format(bstack1111l111l_opy_));
  except Exception as e:
    logger.debug(bstack11ll111111_opy_.format(str(e)))
def bstack111l11l1l1_opy_(hashed_id):
  global CONFIG
  try:
    bstack1l1111ll_opy_ = datetime.datetime.now()
    host = bstack1ll_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡲ࡬࠱ࡨࡲ࡯ࡶࡦ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭࿩") if bstack1ll_opy_ (u"ࠧࡢࡲࡳࠫ࿪") in CONFIG else bstack1ll_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩ࿫")
    user = CONFIG[bstack1ll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ࿬")]
    key = CONFIG[bstack1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭࿭")]
    bstack1l1ll1l11l_opy_ = bstack1ll_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪ࿮") if bstack1ll_opy_ (u"ࠬࡧࡰࡱࠩ࿯") in CONFIG else (bstack1ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪ࿰") if CONFIG.get(bstack1ll_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫ࿱")) else bstack1ll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ࿲"))
    host = bstack11lll111ll_opy_(cli.config, [bstack1ll_opy_ (u"ࠤࡤࡴ࡮ࡹࠢ࿳"), bstack1ll_opy_ (u"ࠥࡥࡵࡶࡁࡶࡶࡲࡱࡦࡺࡥࠣ࿴"), bstack1ll_opy_ (u"ࠦࡦࡶࡩࠣ࿵")], host) if bstack1ll_opy_ (u"ࠬࡧࡰࡱࠩ࿶") in CONFIG else bstack11lll111ll_opy_(cli.config, [bstack1ll_opy_ (u"ࠨࡡࡱ࡫ࡶࠦ࿷"), bstack1ll_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡦࠤ࿸"), bstack1ll_opy_ (u"ࠣࡣࡳ࡭ࠧ࿹")], host)
    url = bstack1ll_opy_ (u"ࠩࡾࢁ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀ࠳ࡸ࡫ࡳࡴ࡫ࡲࡲࡸ࠴ࡪࡴࡱࡱࠫ࿺").format(host, bstack1l1ll1l11l_opy_, hashed_id)
    headers = {
      bstack1ll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩ࿻"): bstack1ll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ࿼"),
    }
    proxies = bstack11l11ll11_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies, auth=(user, key))
    if response.json():
      cli.bstack1lll11ll11_opy_(bstack1ll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࡫ࡪࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࡡ࡯࡭ࡸࡺࠢ࿽"), datetime.datetime.now() - bstack1l1111ll_opy_)
      return list(map(lambda session: session[bstack1ll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࠫ࿾")], response.json()))
  except Exception as e:
    logger.debug(bstack1l111ll1ll_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack1l1l1ll111_opy_, stage=STAGE.bstack11llll111l_opy_, bstack111l11111_opy_=SESSION_NAME)
def get_build_link():
  global CONFIG
  global bstack1l1ll111_opy_
  try:
    if bstack1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ࿿") in CONFIG:
      bstack1l1111ll_opy_ = datetime.datetime.now()
      host = bstack1ll_opy_ (u"ࠨࡣࡳ࡭࠲ࡩ࡬ࡰࡷࡧࠫက") if bstack1ll_opy_ (u"ࠩࡤࡴࡵ࠭ခ") in CONFIG else bstack1ll_opy_ (u"ࠪࡥࡵ࡯ࠧဂ")
      user = CONFIG[bstack1ll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ဃ")]
      key = CONFIG[bstack1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨင")]
      bstack1l1ll1l11l_opy_ = bstack1ll_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬစ") if bstack1ll_opy_ (u"ࠧࡢࡲࡳࠫဆ") in CONFIG else bstack1ll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪဇ")
      url = bstack1ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡾࢁ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀ࠳ࡧࡻࡩ࡭ࡦࡶ࠲࡯ࡹ࡯࡯ࠩဈ").format(user, key, host, bstack1l1ll1l11l_opy_)
      if cli.is_enabled(CONFIG):
        bstack1l11l111l1_opy_, hashed_id = cli.bstack1ll11111ll_opy_()
        logger.info(bstack11l111111_opy_.format(bstack1l11l111l1_opy_))
        return [hashed_id, bstack1l11l111l1_opy_]
      else:
        headers = {
          bstack1ll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩဉ"): bstack1ll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧည"),
        }
        if bstack1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧဋ") in CONFIG:
          params = {bstack1ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫဌ"): CONFIG[bstack1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪဍ")], bstack1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫဎ"): CONFIG[bstack1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫဏ")]}
        else:
          params = {bstack1ll_opy_ (u"ࠪࡲࡦࡳࡥࠨတ"): CONFIG[bstack1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧထ")]}
        proxies = bstack11l11ll11_opy_(CONFIG, url)
        response = requests.get(url, params=params, headers=headers, proxies=proxies)
        if response.json():
          bstack1lll1lll_opy_ = response.json()[0][bstack1ll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡥࡹ࡮ࡲࡤࠨဒ")]
          if bstack1lll1lll_opy_:
            bstack1l11l111l1_opy_ = bstack1lll1lll_opy_[bstack1ll_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨࡥࡵࡳ࡮ࠪဓ")].split(bstack1ll_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࠭ࡣࡷ࡬ࡰࡩ࠭န"))[0] + bstack1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡳ࠰ࠩပ") + bstack1lll1lll_opy_[
              bstack1ll_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬဖ")]
            logger.info(bstack11l111111_opy_.format(bstack1l11l111l1_opy_))
            bstack1l1ll111_opy_ = bstack1lll1lll_opy_[bstack1ll_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ဗ")]
            bstack11l1lll1l1_opy_ = CONFIG[bstack1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧဘ")]
            if bstack1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧမ") in CONFIG:
              bstack11l1lll1l1_opy_ += bstack1ll_opy_ (u"࠭ࠠࠨယ") + CONFIG[bstack1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩရ")]
            if bstack11l1lll1l1_opy_ != bstack1lll1lll_opy_[bstack1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭လ")]:
              logger.debug(bstack11llll1l1_opy_.format(bstack1lll1lll_opy_[bstack1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧဝ")], bstack11l1lll1l1_opy_))
            cli.bstack1lll11ll11_opy_(bstack1ll_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻ࡩࡨࡸࡤࡨࡵࡪ࡮ࡧࡣࡱ࡯࡮࡬ࠤသ"), datetime.datetime.now() - bstack1l1111ll_opy_)
            return [bstack1lll1lll_opy_[bstack1ll_opy_ (u"ࠫ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧဟ")], bstack1l11l111l1_opy_]
    else:
      logger.warning(bstack1llll111l1_opy_)
  except Exception as e:
    logger.debug(bstack111ll1l1l_opy_.format(str(e)))
  return [None, None]
def bstack1ll1l1llll_opy_(url, bstack1l1ll1lll1_opy_=False):
  global CONFIG
  global bstack11l1111l1_opy_
  if not bstack11l1111l1_opy_:
    hostname = bstack11llllll1_opy_(url)
    is_private = bstack111lll1l1_opy_(hostname)
    if (bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩဠ") in CONFIG and not bstack11l1l1l11l_opy_(CONFIG[bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪအ")])) and (is_private or bstack1l1ll1lll1_opy_):
      bstack11l1111l1_opy_ = hostname
def bstack11llllll1_opy_(url):
  return urlparse(url).hostname
def bstack111lll1l1_opy_(hostname):
  for bstack1l1lll111_opy_ in bstack1111ll1ll1_opy_:
    regex = re.compile(bstack1l1lll111_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack11ll11111_opy_(bstack111l1111l_opy_):
  return True if bstack111l1111l_opy_ in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack1ll1llllll_opy_, stage=STAGE.bstack11llll111l_opy_, bstack111l11111_opy_=SESSION_NAME)
def getAccessibilityResults(driver):
  global CONFIG
  global PLATFORM_INDEX
  bstack1l1ll111ll_opy_ = not (bstack1llll1lll_opy_(threading.current_thread(), bstack1ll_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫဢ"), None) and bstack1llll1lll_opy_(
          threading.current_thread(), bstack1ll_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧဣ"), None))
  bstack11ll1ll111_opy_ = getattr(driver, bstack1ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩဤ"), None) != True
  bstack11ll11ll1l_opy_ = bstack1llll1lll_opy_(threading.current_thread(), bstack1ll_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪဥ"), None) and bstack1llll1lll_opy_(
          threading.current_thread(), bstack1ll_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ဦ"), None)
  if bstack11ll11ll1l_opy_:
    if not bstack1lllll111l_opy_():
      logger.warning(bstack1ll_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡰࡱࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡅࡵࡶࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳ࠯ࠤဧ"))
      return {}
    logger.debug(bstack1ll_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪဨ"))
    logger.debug(perform_scan(driver, driver_command=bstack1ll_opy_ (u"ࠧࡦࡺࡨࡧࡺࡺࡥࡔࡥࡵ࡭ࡵࡺࠧဩ")))
    results = bstack1111ll1ll_opy_(bstack1ll_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࡴࠤဪ"))
    if results is not None and results.get(bstack1ll_opy_ (u"ࠤ࡬ࡷࡸࡻࡥࡴࠤါ")) is not None:
        return results[bstack1ll_opy_ (u"ࠥ࡭ࡸࡹࡵࡦࡵࠥာ")]
    logger.error(bstack1ll_opy_ (u"ࠦࡓࡵࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡓࡧࡶࡹࡱࡺࡳࠡࡹࡨࡶࡪࠦࡦࡰࡷࡱࡨ࠳ࠨိ"))
    return []
  if not a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX) or (bstack11ll1ll111_opy_ and bstack1l1ll111ll_opy_):
    logger.warning(bstack1ll_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹ࠮ࠣီ"))
    return {}
  try:
    logger.debug(bstack1ll_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪု"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(accessibility_scripts.get_results)
    return results
  except Exception:
    logger.error(bstack1ll_opy_ (u"ࠢࡏࡱࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡼ࡫ࡲࡦࠢࡩࡳࡺࡴࡤ࠯ࠤူ"))
    return {}
@measure(event_name=EVENTS.bstack111ll11l_opy_, stage=STAGE.bstack11llll111l_opy_, bstack111l11111_opy_=SESSION_NAME)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global PLATFORM_INDEX
  bstack1l1ll111ll_opy_ = not (bstack1llll1lll_opy_(threading.current_thread(), bstack1ll_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬေ"), None) and bstack1llll1lll_opy_(
          threading.current_thread(), bstack1ll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨဲ"), None))
  bstack11ll1ll111_opy_ = getattr(driver, bstack1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪဳ"), None) != True
  bstack11ll11ll1l_opy_ = bstack1llll1lll_opy_(threading.current_thread(), bstack1ll_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫဴ"), None) and bstack1llll1lll_opy_(
          threading.current_thread(), bstack1ll_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧဵ"), None)
  if bstack11ll11ll1l_opy_:
    if not bstack1lllll111l_opy_():
      logger.warning(bstack1ll_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡆࡶࡰࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡶࡹࡲࡳࡡࡳࡻ࠱ࠦံ"))
      return {}
    logger.debug(bstack1ll_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡸࡻ࡭࡮ࡣࡵࡽ့ࠬ"))
    logger.debug(perform_scan(driver, driver_command=bstack1ll_opy_ (u"ࠨࡧࡻࡩࡨࡻࡴࡦࡕࡦࡶ࡮ࡶࡴࠨး")))
    results = bstack1111ll1ll_opy_(bstack1ll_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡕࡸࡱࡲࡧࡲࡺࠤ္"))
    if results is not None and results.get(bstack1ll_opy_ (u"ࠥࡷࡺࡳ࡭ࡢࡴࡼ်ࠦ")) is not None:
        return results[bstack1ll_opy_ (u"ࠦࡸࡻ࡭࡮ࡣࡵࡽࠧျ")]
    logger.error(bstack1ll_opy_ (u"ࠧࡔ࡯ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡔࡨࡷࡺࡲࡴࡴࠢࡖࡹࡲࡳࡡࡳࡻࠣࡻࡦࡹࠠࡧࡱࡸࡲࡩ࠴ࠢြ"))
    return {}
  if not a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX) or (bstack11ll1ll111_opy_ and bstack1l1ll111ll_opy_):
    logger.warning(bstack1ll_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡵࡸࡱࡲࡧࡲࡺ࠰ࠥွ"))
    return {}
  try:
    logger.debug(bstack1ll_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡸࡻ࡭࡮ࡣࡵࡽࠬှ"))
    logger.debug(perform_scan(driver))
    bstack11111lll1_opy_ = driver.execute_async_script(accessibility_scripts.get_results_summary)
    return bstack11111lll1_opy_
  except Exception:
    logger.error(bstack1ll_opy_ (u"ࠣࡐࡲࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸࡻ࡭࡮ࡣࡵࡽࠥࡽࡡࡴࠢࡩࡳࡺࡴࡤ࠯ࠤဿ"))
    return {}
def bstack1lllll111l_opy_():
  global CONFIG
  global PLATFORM_INDEX
  bstack111llll11_opy_ = bstack1llll1lll_opy_(threading.current_thread(), bstack1ll_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ၀"), None) and bstack1llll1lll_opy_(threading.current_thread(), bstack1ll_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ၁"), None)
  if not a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX) or not bstack111llll11_opy_:
        logger.warning(bstack1ll_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡶࡰࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡵࡩࡸࡻ࡬ࡵࡵ࠱ࠦ၂"))
        return False
  return True
def bstack1111ll1ll_opy_(result_type):
    bstack11ll11l1ll_opy_ = TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack111l111ll1_opy_.current_hook_uuid()
    with ThreadPoolExecutor() as executor:
        future = executor.submit(bstack11lll1l111_opy_(bstack11ll11l1ll_opy_, result_type))
        try:
            return future.result(timeout=bstack11l1l1111_opy_)
        except TimeoutError:
            logger.error(bstack1ll_opy_ (u"࡚ࠧࡩ࡮ࡧࡲࡹࡹࠦࡡࡧࡶࡨࡶࠥࢁࡽࡴࠢࡺ࡬࡮ࡲࡥࠡࡨࡨࡸࡨ࡮ࡩ࡯ࡩࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡖࡪࡹࡵ࡭ࡶࡶࠦ၃").format(bstack11l1l1111_opy_))
        except Exception as ex:
            logger.debug(bstack1ll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡸࡥࡵࡴ࡬ࡩࡻ࡯࡮ࡨࠢࡄࡴࡵࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡿࢂ࠴ࠠࡆࡴࡵࡳࡷࠦ࠭ࠡࡽࢀࠦ၄").format(result_type, str(ex)))
    return {}
@measure(event_name=EVENTS.bstack11l1ll1111_opy_, stage=STAGE.bstack11llll111l_opy_, bstack111l11111_opy_=SESSION_NAME)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global PLATFORM_INDEX
  bstack1l1ll111ll_opy_ = not (bstack1llll1lll_opy_(threading.current_thread(), bstack1ll_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ၅"), None) and bstack1llll1lll_opy_(
          threading.current_thread(), bstack1ll_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ၆"), None))
  bstack1l1l11111_opy_ = not (bstack1llll1lll_opy_(threading.current_thread(), bstack1ll_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ၇"), None) and bstack1llll1lll_opy_(
          threading.current_thread(), bstack1ll_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ၈"), None))
  bstack11ll1ll111_opy_ = getattr(driver, bstack1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫ၉"), None) != True
  if not a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX) or (bstack11ll1ll111_opy_ and bstack1l1ll111ll_opy_ and bstack1l1l11111_opy_):
    logger.warning(bstack1ll_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷࡻ࡮ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳ࠴ࠢ၊"))
    return {}
  try:
    bstack1lll111l1_opy_ = bstack1ll_opy_ (u"࠭ࡡࡱࡲࠪ။") in CONFIG and CONFIG.get(bstack1ll_opy_ (u"ࠧࡢࡲࡳࠫ၌"), bstack1ll_opy_ (u"ࠨࠩ၍"))
    session_id = getattr(driver, bstack1ll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩ࠭၎"), None)
    if not session_id:
      logger.warning(bstack1ll_opy_ (u"ࠥࡒࡴࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡊࡆࠣࡪࡴࡻ࡮ࡥࠢࡩࡳࡷࠦࡤࡳ࡫ࡹࡩࡷࠨ၏"))
      return {bstack1ll_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥၐ"): bstack1ll_opy_ (u"ࠧࡔ࡯ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡌࡈࠥ࡬࡯ࡶࡰࡧࠦၑ")}
    if bstack1lll111l1_opy_:
      try:
        bstack1ll1ll111_opy_ = {
              bstack1ll_opy_ (u"࠭ࡴࡩࡌࡺࡸ࡙ࡵ࡫ࡦࡰࠪၒ"): os.environ.get(bstack1ll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬၓ"), os.environ.get(bstack1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬၔ"), bstack1ll_opy_ (u"ࠩࠪၕ"))),
              bstack1ll_opy_ (u"ࠪࡸ࡭࡚ࡥࡴࡶࡕࡹࡳ࡛ࡵࡪࡦࠪၖ"): TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack111l111ll1_opy_.current_hook_uuid(),
              bstack1ll_opy_ (u"ࠫࡦࡻࡴࡩࡊࡨࡥࡩ࡫ࡲࠨၗ"): os.environ.get(bstack1ll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪၘ")),
              bstack1ll_opy_ (u"࠭ࡳࡤࡣࡱࡘ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ၙ"): str(int(datetime.datetime.now().timestamp() * 1000)),
              bstack1ll_opy_ (u"ࠧࡵࡪࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬၚ"): os.environ.get(bstack1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ၛ"), bstack1ll_opy_ (u"ࠩࠪၜ")),
              bstack1ll_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࠪၝ"): kwargs.get(bstack1ll_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࡣࡨࡵ࡭࡮ࡣࡱࡨࠬၞ"), None) or bstack1ll_opy_ (u"ࠬ࠭ၟ")
          }
        if not hasattr(thread_local, bstack1ll_opy_ (u"࠭ࡢࡢࡵࡨࡣࡦࡶࡰࡠࡣ࠴࠵ࡾࡥࡳࡤࡴ࡬ࡴࡹ࠭ၠ")):
            scripts = {bstack1ll_opy_ (u"ࠧࡴࡥࡤࡲࠬၡ"): accessibility_scripts.perform_scan}
            thread_local.base_app_a11y_script = scripts
        bstack11l1l111l1_opy_ = copy.deepcopy(thread_local.base_app_a11y_script)
        bstack11l1l111l1_opy_[bstack1ll_opy_ (u"ࠨࡵࡦࡥࡳ࠭ၢ")] = bstack11l1l111l1_opy_[bstack1ll_opy_ (u"ࠩࡶࡧࡦࡴࠧၣ")] % json.dumps(bstack1ll1ll111_opy_)
        accessibility_scripts.bstack11lll1l1_opy_(bstack11l1l111l1_opy_)
        accessibility_scripts.store()
        bstack11lll1ll1_opy_ = driver.execute_script(accessibility_scripts.perform_scan)
      except Exception as bstack1l11ll1l1_opy_:
        logger.info(bstack1ll_opy_ (u"ࠥࡅࡵࡶࡩࡶ࡯ࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࠥၤ") + str(bstack1l11ll1l1_opy_))
        bstack11lll1ll1_opy_ = {bstack1ll_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥၥ"): str(bstack1l11ll1l1_opy_)}
    else:
      bstack11lll1ll1_opy_ = driver.execute_async_script(accessibility_scripts.perform_scan, {bstack1ll_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬၦ"): kwargs.get(bstack1ll_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡣࡰ࡯ࡰࡥࡳࡪࠧၧ"), None) or bstack1ll_opy_ (u"ࠧࠨၨ")})
    return bstack11lll1ll1_opy_
  except Exception as err:
    logger.error(bstack1ll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡷࡻ࡮ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳ࠴ࠠࡼࡿࠥၩ").format(str(err)))
    return {}