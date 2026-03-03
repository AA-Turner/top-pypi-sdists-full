# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
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
from browserstack_sdk.bstack1ll111111l_opy_ import bstack1ll11llll1_opy_
from browserstack_sdk.bstack1l1lll111l_opy_ import *
import time
import requests
from bstack_utils.constants import EVENTS, STAGE, bstack1lll1ll1l1_opy_
from bstack_utils.messages import bstack111llllll_opy_, bstack111ll111_opy_, bstack1l1l111lll_opy_, bstack111l1l11_opy_, bstack1l1ll11l_opy_, bstack1lll1111l1_opy_
from bstack_utils.measure import measure
from bstack_utils.logger_utils import get_logger
from bstack_utils.helper import bstack1111llll1l_opy_
from browserstack_sdk.bstack1l1l11111_opy_ import bstack11l111l1l1_opy_
logger = get_logger(__name__)
def bstack1ll11l1lll_opy_():
  global CONFIG
  headers = {
        bstack11ll111_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack11ll111_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1111llll1l_opy_(CONFIG, bstack1lll1ll1l1_opy_)
  try:
    response = requests.get(bstack1lll1ll1l1_opy_, headers=headers, proxies=proxies, timeout=2)
    if response.json():
      bstack1l1l1l1ll_opy_ = response.json()[bstack11ll111_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack111llllll_opy_.format(response.json()))
      return bstack1l1l1l1ll_opy_
    else:
      logger.debug(bstack111ll111_opy_.format(bstack11ll111_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack111ll111_opy_.format(e))
def bstack1l1111l111_opy_(hub_url):
  global CONFIG
  url = bstack11ll111_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack11ll111_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack11ll111_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack11ll111_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1111llll1l_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=(0.5, 1.0))
    latency = time.perf_counter() - start_time
    logger.debug(bstack1l1l111lll_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack111l1l11_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack111ll1111l_opy_, stage=STAGE.bstack1111l1111_opy_)
def bstack1l1l1llll1_opy_():
  try:
    global bstack11lll111ll_opy_
    global CONFIG
    if bstack11ll111_opy_ (u"ࠫ࡭ࡻࡢࡓࡧࡪ࡭ࡴࡴࠧࡾ") in CONFIG and CONFIG[bstack11ll111_opy_ (u"ࠬ࡮ࡵࡣࡔࡨ࡫࡮ࡵ࡮ࠨࡿ")]:
      from bstack_utils.constants import bstack1ll1ll1l1l_opy_
      bstack11l1111l1_opy_ = CONFIG[bstack11ll111_opy_ (u"࠭ࡨࡶࡤࡕࡩ࡬࡯࡯࡯ࠩࢀ")]
      if bstack11l1111l1_opy_ in bstack1ll1ll1l1l_opy_:
        bstack11lll111ll_opy_ = bstack1ll1ll1l1l_opy_[bstack11l1111l1_opy_]
        logger.debug(bstack1l1ll11l_opy_.format(bstack11lll111ll_opy_))
        return
      else:
        logger.debug(bstack11ll111_opy_ (u"ࠢࡉࡷࡥࠤࡰ࡫ࡹࠡࠩࡾࢁࠬࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࡎࡕࡃࡡࡘࡖࡑࡥࡍࡂࡒ࠯ࠤ࡫ࡧ࡬࡭࡫ࡱ࡫ࠥࡨࡡࡤ࡭ࠣࡸࡴࠦ࡯ࡱࡶ࡬ࡱࡦࡲࠠࡩࡷࡥࠤࡩ࡫ࡴࡦࡥࡷ࡭ࡴࡴࠢࢁ").format(bstack11l1111l1_opy_))
    bstack1l1l1l1ll_opy_ = bstack1ll11l1lll_opy_()
    from concurrent.futures import ThreadPoolExecutor, as_completed
    if bstack1l1l1l1ll_opy_:
        with ThreadPoolExecutor(max_workers=len(bstack1l1l1l1ll_opy_)) as executor:
            bstack11ll1l1l11_opy_ = {executor.submit(bstack1l1111l111_opy_, bstack111ll11lll_opy_): bstack111ll11lll_opy_ for bstack111ll11lll_opy_ in bstack1l1l1l1ll_opy_}
            for future in as_completed(bstack11ll1l1l11_opy_):
                result = future.result()
                if result and result.get(bstack11ll111_opy_ (u"ࠨ࡮ࡤࡸࡪࡴࡣࡺࠩࢂ")) is not None:
                    bstack11lll111ll_opy_ = result[bstack11ll111_opy_ (u"ࠩ࡫ࡹࡧࡥࡵࡳ࡮ࠪࢃ")]
                    logger.debug(bstack1l1ll11l_opy_.format(bstack11lll111ll_opy_))
                    return
        bstack11lll111ll_opy_ = bstack1l1l1l1ll_opy_[0]
        logger.debug(bstack1l1ll11l_opy_.format(bstack11lll111ll_opy_))
        return
  except Exception as e:
    logger.debug(bstack1lll1111l1_opy_.format(e))
from browserstack_sdk.bstack1ll111lll1_opy_ import *
from browserstack_sdk.bstack1l1l11111_opy_ import *
from browserstack_sdk.bstack1111111ll_opy_ import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.logger_utils import get_logger
from bstack_utils.measure import measure
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack1lll11l1l1_opy_, stage=STAGE.bstack1111l1111_opy_)
def bstack11l1ll1lll_opy_():
    global bstack11lll111ll_opy_
    try:
        bstack1ll11l111_opy_ = bstack111lll1ll_opy_()
        bstack1llll1ll11_opy_(bstack1ll11l111_opy_)
        hub_url = bstack1ll11l111_opy_.get(bstack11ll111_opy_ (u"ࠥࡹࡷࡲࠢࢄ"), bstack11ll111_opy_ (u"ࠦࠧࢅ"))
        if hub_url.endswith(bstack11ll111_opy_ (u"ࠬ࠵ࡷࡥ࠱࡫ࡹࡧ࠭ࢆ")):
            hub_url = hub_url.rsplit(bstack11ll111_opy_ (u"࠭࠯ࡸࡦ࠲࡬ࡺࡨࠧࢇ"), 1)[0]
        if hub_url.startswith(bstack11ll111_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࠨ࢈")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack11ll111_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࠪࢉ")):
            hub_url = hub_url[8:]
        bstack11lll111ll_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack111lll1ll_opy_():
    global CONFIG
    bstack11lllllll1_opy_ = CONFIG.get(bstack11ll111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢊ"), {}).get(bstack11ll111_opy_ (u"ࠪ࡫ࡷ࡯ࡤࡏࡣࡰࡩࠬࢋ"), bstack11ll111_opy_ (u"ࠫࡓࡕ࡟ࡈࡔࡌࡈࡤࡔࡁࡎࡇࡢࡔࡆ࡙ࡓࡆࡆࠪࢌ"))
    if not isinstance(bstack11lllllll1_opy_, str):
        raise ValueError(bstack11ll111_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡌࡸࡩࡥࠢࡱࡥࡲ࡫ࠠ࡮ࡷࡶࡸࠥࡨࡥࠡࡣࠣࡺࡦࡲࡩࡥࠢࡶࡸࡷ࡯࡮ࡨࠤࢍ"))
    try:
        bstack1ll11l111_opy_ = bstack1l1l111111_opy_(bstack11lllllll1_opy_)
        return bstack1ll11l111_opy_
    except Exception as e:
        logger.error(bstack11ll111_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡩࡵ࡭ࡩࠦࡤࡦࡶࡤ࡭ࡱࡹࠠ࠻ࠢࡾࢁࠧࢎ").format(str(e)))
        return {}
def bstack1l1l111111_opy_(bstack11lllllll1_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack11ll111_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ࢏")] or not CONFIG[bstack11ll111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ࢐")]:
            raise ValueError(bstack11ll111_opy_ (u"ࠤࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠤࡴࡸࠠࡢࡥࡦࡩࡸࡹࠠ࡬ࡧࡼࠦ࢑"))
        url = bstack111ll111l1_opy_ + bstack11lllllll1_opy_
        auth = (CONFIG[bstack11ll111_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ࢒")], CONFIG[bstack11ll111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ࢓")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack11l11l1lll_opy_ = json.loads(response.text)
            return bstack11l11l1lll_opy_
    except ValueError as ve:
        logger.error(bstack11ll111_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡩࡵ࡭ࡩࠦࡤࡦࡶࡤ࡭ࡱࡹࠠ࠻ࠢࡾࢁࠧ࢔").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack11ll111_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡪࡶ࡮ࡪࠠࡥࡧࡷࡥ࡮ࡲࡳࠡ࠼ࠣࡿࢂࠨ࢕").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack1llll1ll11_opy_(bstack1lll1lll1_opy_):
    global CONFIG
    if bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ࢖") not in CONFIG or str(CONFIG[bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬࢗ")]).lower() == bstack11ll111_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ࢘"):
        CONFIG[bstack11ll111_opy_ (u"ࠪࡰࡴࡩࡡ࡭࢙ࠩ")] = False
    elif bstack11ll111_opy_ (u"ࠫ࡮ࡹࡔࡳ࡫ࡤࡰࡌࡸࡩࡥ࢚ࠩ") in bstack1lll1lll1_opy_:
        bstack1l11111ll1_opy_ = CONFIG.get(bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴ࢛ࠩ"), {})
        logger.debug(bstack11ll111_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡸࡪࡵࡷ࡭ࡳ࡭ࠠ࡭ࡱࡦࡥࡱࠦ࡯ࡱࡶ࡬ࡳࡳࡹ࠺ࠡࠧࡶࠦ࢜"), bstack1l11111ll1_opy_)
        bstack11ll11lll1_opy_ = bstack1lll1lll1_opy_.get(bstack11ll111_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡒࡦࡲࡨࡥࡹ࡫ࡲࡴࠤ࢝"), [])
        bstack11lll11ll1_opy_ = bstack11ll111_opy_ (u"ࠣ࠮ࠥ࢞").join(bstack11ll11lll1_opy_)
        logger.debug(bstack11ll111_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡅࡸࡷࡹࡵ࡭ࠡࡴࡨࡴࡪࡧࡴࡦࡴࠣࡷࡹࡸࡩ࡯ࡩ࠽ࠤࠪࡹࠢ࢟"), bstack11lll11ll1_opy_)
        bstack11l1l1l11l_opy_ = {
            bstack11ll111_opy_ (u"ࠥࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧࢠ"): bstack11ll111_opy_ (u"ࠦࡦࡺࡳ࠮ࡴࡨࡴࡪࡧࡴࡦࡴࠥࢡ"),
            bstack11ll111_opy_ (u"ࠧ࡬࡯ࡳࡥࡨࡐࡴࡩࡡ࡭ࠤࢢ"): bstack11ll111_opy_ (u"ࠨࡴࡳࡷࡨࠦࢣ"),
            bstack11ll111_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࠭ࡳࡧࡳࡩࡦࡺࡥࡳࠤࢤ"): bstack11lll11ll1_opy_
        }
        bstack1l11111ll1_opy_.update(bstack11l1l1l11l_opy_)
        logger.debug(bstack11ll111_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡖࡲࡧࡥࡹ࡫ࡤࠡ࡮ࡲࡧࡦࡲࠠࡰࡲࡷ࡭ࡴࡴࡳ࠻ࠢࠨࡷࠧࢥ"), bstack1l11111ll1_opy_)
        CONFIG[bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢦ")] = bstack1l11111ll1_opy_
        logger.debug(bstack11ll111_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡉ࡭ࡳࡧ࡬ࠡࡅࡒࡒࡋࡏࡇ࠻ࠢࠨࡷࠧࢧ"), CONFIG)
def bstack11llll11_opy_():
    bstack1ll11l111_opy_ = bstack111lll1ll_opy_()
    if not bstack1ll11l111_opy_[bstack11ll111_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡖࡴ࡯ࠫࢨ")]:
      raise ValueError(bstack11ll111_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡗࡵࡰࠥ࡯ࡳࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡩࡶࡴࡳࠠࡨࡴ࡬ࡨࠥࡪࡥࡵࡣ࡬ࡰࡸ࠴ࠢࢩ"))
    return bstack1ll11l111_opy_[bstack11ll111_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡘࡶࡱ࠭ࢪ")] + bstack11ll111_opy_ (u"ࠧࡀࡥࡤࡴࡸࡃࠧࢫ")
@measure(event_name=EVENTS.bstack1ll111l111_opy_, stage=STAGE.bstack1111l1111_opy_)
def bstack1l1l1111_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack11ll111_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪࢬ")], CONFIG[bstack11ll111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬࢭ")])
        url = bstack11ll1l1ll_opy_
        logger.debug(bstack11ll111_opy_ (u"ࠥࡅࡹࡺࡥ࡮ࡲࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴࠢࡩࡶࡴࡳࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡔࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠣࡅࡕࡏࠢࢮ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack11ll111_opy_ (u"ࠦࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠥࢯ"): bstack11ll111_opy_ (u"ࠧࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠣࢰ")})
            if response.status_code == 200:
                bstack111l1ll11l_opy_ = json.loads(response.text)
                bstack1l11111lll_opy_ = bstack111l1ll11l_opy_.get(bstack11ll111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡸ࠭ࢱ"), [])
                if bstack1l11111lll_opy_:
                    bstack111l1l11l_opy_ = bstack1l11111lll_opy_[0]
                    build_hashed_id = bstack111l1l11l_opy_.get(bstack11ll111_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪࢲ"))
                    bstack1lll1l111l_opy_ = bstack111l1lll11_opy_ + build_hashed_id
                    result.extend([build_hashed_id, bstack1lll1l111l_opy_])
                    logger.info(bstack111ll1l111_opy_.format(bstack1lll1l111l_opy_))
                    bstack11l1l1111l_opy_ = CONFIG[bstack11ll111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫࢳ")]
                    if bstack11ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࢴ") in CONFIG:
                      bstack11l1l1111l_opy_ += bstack11ll111_opy_ (u"ࠪࠤࠬࢵ") + CONFIG[bstack11ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࢶ")]
                    if bstack11l1l1111l_opy_ != bstack111l1l11l_opy_.get(bstack11ll111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪࢷ")):
                      logger.debug(bstack1l1ll11l11_opy_.format(bstack111l1l11l_opy_.get(bstack11ll111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫࢸ")), bstack11l1l1111l_opy_))
                    return result
                else:
                    logger.debug(bstack11ll111_opy_ (u"ࠢࡂࡖࡖࠤ࠿ࠦࡎࡰࠢࡥࡹ࡮ࡲࡤࡴࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠱ࠦࢹ"))
            else:
                logger.debug(bstack11ll111_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴ࠰ࠥࢺ"))
        except Exception as e:
            logger.error(bstack11ll111_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࡶࠤ࠿ࠦࡻࡾࠤࢻ").format(str(e)))
    else:
        logger.debug(bstack11ll111_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡆࡓࡓࡌࡉࡈࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡶࡩࡹ࠴ࠠࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴ࠰ࠥࢼ"))
    return [None, None]
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack111l1llll1_opy_ import bstack111l1llll1_opy_, bstack1l11lll1ll_opy_, bstack1l11l111l_opy_, bstack11ll1l11l1_opy_
from bstack_utils.measure import bstack11111111l_opy_
from bstack_utils.measure import measure
from bstack_utils.percy import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack111l111l1_opy_ import bstack11111l111_opy_
from bstack_utils.messages import *
from bstack_utils import logger_utils
from bstack_utils.constants import *
from bstack_utils.helper import bstack11ll1llll1_opy_, bstack1l1l11ll_opy_, bstack1llll1ll_opy_, bstack1lll11l111_opy_, \
  bstack11l1llllll_opy_, \
  Notset, is_robot_playwright_installed, bstack1ll1lll1l1_opy_, \
  bstack11lll1l111_opy_, bstack11ll1111_opy_, bstack11lllll111_opy_, bstack1llll111_opy_, bstack111l1lll_opy_, bstack1lllll11l_opy_, \
  bstack1l1111lll1_opy_, \
  bstack1ll1llll11_opy_, bstack11lllll1l1_opy_, bstack1l111111_opy_, bstack1l11l1lll_opy_, \
  bstack11ll1l11ll_opy_, bstack111lll111l_opy_, bstack11l1lll1_opy_, bstack1l111lllll_opy_, bstack11l1l11l11_opy_
from bstack_utils.bstack11ll1l11l_opy_ import bstack1l1l1111ll_opy_
from bstack_utils.bstack111l1ll111_opy_ import bstack11l1l11lll_opy_, bstack1ll1l1l1_opy_
from bstack_utils.bstack1llll1ll1_opy_ import bstack1l111l1l1l_opy_
from bstack_utils.session_utils import bstack1l11l1ll11_opy_, bstack111l1l1lll_opy_
from bstack_utils.bstack11ll11llll_opy_ import bstack11ll11llll_opy_
from bstack_utils.bstack11lll11lll_opy_ import bstack11l1ll111l_opy_
from bstack_utils.proxy import bstack111l11ll11_opy_, bstack1111llll1l_opy_, bstack1111lllll1_opy_, bstack1lllll1l11_opy_
from bstack_utils.bstack1l1l11lll_opy_ import bstack1l1ll1ll1l_opy_, bstack11l11l111_opy_
import bstack_utils.bstack111l111ll_opy_ as bstack111llll11l_opy_
import bstack_utils.bstack11l1l1ll1_opy_ as bstack1l11l11l1l_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.utils.bstack1lllll11_opy_ import bstack11l1ll11l1_opy_
from bstack_utils.bstack1lllll111l_opy_ import bstack1111lll11_opy_
from bstack_utils.bstack111l1l1l1_opy_ import bstack1ll11ll1_opy_
from bstack_utils.bstack11111111l_opy_ import bstack1111l1l1l_opy_
if os.getenv(bstack11ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡉࡑࡒࡏࡘ࠭ࢽ")):
  cli.bstack11l11lllll_opy_()
else:
  os.environ[bstack11ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡊࡒࡓࡐ࡙ࠧࢾ")] = bstack11ll111_opy_ (u"࠭ࡴࡳࡷࡨࠫࢿ")
bstack11l1lllll_opy_ = bstack11ll111_opy_ (u"ࠧࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠠࠡ࡫ࡩࠬࡵࡧࡧࡦࠢࡀࡁࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠠࡼ࡞ࡱࠤࠥࠦࡴࡳࡻࡾࡠࡳࠦࡣࡰࡰࡶࡸࠥ࡬ࡳࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࡡ࠭ࡦࡴ࡞ࠪ࠭ࡀࡢ࡮ࠡࠢࠣࠤࠥ࡬ࡳ࠯ࡣࡳࡴࡪࡴࡤࡇ࡫࡯ࡩࡘࡿ࡮ࡤࠪࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠬࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡳࡣ࡮ࡴࡤࡦࡺࠬࠤ࠰ࠦࠢ࠻ࠤࠣ࠯ࠥࡐࡓࡐࡐ࠱ࡷࡹࡸࡩ࡯ࡩ࡬ࡪࡾ࠮ࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࠬࡦࡽࡡࡪࡶࠣࡲࡪࡽࡐࡢࡩࡨ࠶࠳࡫ࡶࡢ࡮ࡸࡥࡹ࡫ࠨࠣࠪࠬࠤࡂࡄࠠࡼࡿࠥ࠰ࠥࡢࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡨࡧࡷࡗࡪࡹࡳࡪࡱࡱࡈࡪࡺࡡࡪ࡮ࡶࠦࢂࡢࠧࠪࠫࠬ࡟ࠧ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠣ࡟ࠬࠤ࠰ࠦࠢ࠭࡞࡟ࡲࠧ࠯࡜࡯ࠢࠣࠤࠥࢃࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡽ࡝ࡰࠣࠤ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠧࣀ")
LAUNCH_PATCH_ROBOT_PLAYWRIGHT = bstack11ll111_opy_ (u"ࠨ࡞ࡱ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࡢ࡮ࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡰࡢࡶ࡫ࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳࡞࡞ࡱࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠴ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡶ࡟ࡪࡰࡧࡩࡽࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠴ࡠࡠࡳࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡹ࡬ࡪࡥࡨࠬ࠵࠲ࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࠬࡠࡳࡩ࡯࡯ࡵࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬ࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ࠭ࡀࡢ࡮ࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮࡭ࡣࡸࡲࡨ࡮ࠠ࠾ࠢࡤࡷࡾࡴࡣࠡࠪ࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴࠫࠣࡁࡃࠦࡻ࡝ࡰ࡯ࡩࡹࠦࡣࡢࡲࡶ࠿ࡡࡴࡴࡳࡻࠣࡿࡡࡴࡣࡢࡲࡶࠤࡂࠦࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠪ࡞ࡱࠤࠥࢃࠠࡤࡣࡷࡧ࡭࠮ࡥࡹࠫࠣࡿࡡࡴࠠࠡࠢࠣࢁࡡࡴࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡣࡺࡥ࡮ࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮ࡤࡱࡱࡲࡪࡩࡴࠩࡽ࡟ࡲࠥࠦࠠࠡࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸ࠿ࠦࡠࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠦࡾࡩࡳࡩ࡯ࡥࡧࡘࡖࡎࡉ࡯࡮ࡲࡲࡲࡪࡴࡴࠩࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡦࡥࡵࡹࠩࠪࡿࡣ࠰ࡡࡴࠠࠡࠢࠣ࠲࠳࠴࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸࡢ࡮ࠡࠢࢀ࠭ࡡࡴࡽ࡝ࡰࡦࡳࡳࡹࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡧࡴࡴ࡮ࡦࡥࡷࠤࡂࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺ࠮ࡣ࡫ࡱࡨ࠭࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠮ࡁ࡜࡯࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭࠯ࡥࡲࡲࡳ࡫ࡣࡵࠢࡀࠤࡦࡹࡹ࡯ࡥࠣࠬࡨࡵ࡮࡯ࡧࡦࡸࡔࡶࡴࡪࡱࡱࡷ࠮ࠦ࠽࠿ࠢࡾࡠࡳࠦࠠ࡭ࡧࡷࠤࡨࡧࡰࡴ࠽࡟ࡲࠥࠦࡴࡳࡻࠣࡿࡡࡴࠠࠡࠢࠣࡧࡦࡶࡳࠡ࠿ࠣࡎࡘࡕࡎ࠯ࡲࡤࡶࡸ࡫ࠨࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷ࠮ࡢ࡮ࠡࠢࢀࠤࡨࡧࡴࡤࡪࠫࡩࡽ࠯ࠠࡼ࡞ࡱࠤࠥࢃ࡜࡯ࠢࠣࡧࡴࡴࡳࡵࠢࡰࡳࡩ࡯ࡦࡪࡧࡧࡉࡳࡪࡰࡰ࡫ࡱࡸࠥࡃࠠࡡࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࡣࠤ࠰ࠦࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭ࡀࡢ࡮ࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤ࠳࠴࠮ࡤࡱࡱࡲࡪࡩࡴࡐࡲࡷ࡭ࡴࡴࡳ࠭࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࡝ࡰࠣࠤࢂ࠯࡜࡯ࡿ࡟ࡲ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵࡜࡯ࠩࣁ")
from ._version import __version__
bstack11l1lllll1_opy_ = None
CONFIG = {}
bstack11l111ll11_opy_ = {}
bstack1lll1l11ll_opy_ = {}
bstack1lll1l1l_opy_ = None
bstack1l111111l_opy_ = None
bstack1lll11lll_opy_ = None
bstack1lll1l11_opy_ = -1
bstack1111l11ll_opy_ = 0
bstack1l11l1l1_opy_ = bstack111ll1l11_opy_
bstack1ll111ll1l_opy_ = 1
bstack11lll11ll_opy_ = False
bstack111ll1l11l_opy_ = False
bstack111l11111l_opy_ = bstack11ll111_opy_ (u"ࠩࠪࣂ")
bstack11111ll1l_opy_ = bstack11ll111_opy_ (u"ࠪࠫࣃ")
bstack1llll11l1_opy_ = False
bstack11ll11l11l_opy_ = True
bstack1ll1lllll1_opy_ = False
bstack1lll1ll1ll_opy_ = bstack11ll111_opy_ (u"ࠫࠬࣄ")
bstack1llllllll1_opy_ = []
bstack1lll11ll_opy_ = threading.Lock()
bstack1llll1ll1l_opy_ = threading.Lock()
bstack1l1ll11l1_opy_ = None
bstack11lll111ll_opy_ = bstack11ll111_opy_ (u"ࠬ࠭ࣅ")
bstack1l111l11l1_opy_ = False
bstack11111ll11_opy_ = None
bstack1ll11l11l1_opy_ = None
bstack1l11ll11ll_opy_ = None
bstack11ll1ll1_opy_ = -1
bstack1l111l111l_opy_ = os.path.join(os.path.expanduser(bstack11ll111_opy_ (u"࠭ࡾࠨࣆ")), bstack11ll111_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧࣇ"), bstack11ll111_opy_ (u"ࠨ࠰ࡵࡳࡧࡵࡴ࠮ࡴࡨࡴࡴࡸࡴ࠮ࡪࡨࡰࡵ࡫ࡲ࠯࡬ࡶࡳࡳ࠭ࣈ"))
bstack11l1111lll_opy_ = 0
bstack11ll1ll1ll_opy_ = 0
bstack1l111l1ll1_opy_ = []
bstack1lll1l1l11_opy_ = []
ROBOT_PYTHON_ERRORS = []
bstack11l1ll111_opy_ = []
bstack11l11l1l1_opy_ = bstack11ll111_opy_ (u"ࠩࠪࣉ")
bstack1l11lll1_opy_ = bstack11ll111_opy_ (u"ࠪࠫ࣊")
bstack1l11ll1ll1_opy_ = False
bstack1llllll1ll_opy_ = False
bstack1ll11111l1_opy_ = {}
bstack11l11llll_opy_ = {}
bstack11lll1ll_opy_ = None
bstack1llll1llll_opy_ = None
bstack11ll1lll1_opy_ = None
bstack11llll11l_opy_ = None
bstack1ll1l1l11l_opy_ = None
bstack11lll1lll_opy_ = None
bstack11lll1l11l_opy_ = None
bstack11l11ll1_opy_ = None
bstack111ll11ll1_opy_ = None
bstack1ll1l1l1ll_opy_ = None
bstack1l1111ll1l_opy_ = None
bstack1l11l1l11_opy_ = None
bstack11ll11lll_opy_ = None
bstack11lll1ll1l_opy_ = None
bstack11ll1l1111_opy_ = None
bstack111ll1llll_opy_ = None
bstack1l111ll1l_opy_ = None
bstack1l11ll1l_opy_ = None
bstack1lll11llll_opy_ = None
bstack11l1l1l11_opy_ = None
bstack111ll11l_opy_ = None
bstack1ll1l11lll_opy_ = None
bstack1ll1ll111_opy_ = None
thread_local = threading.local()
bstack1111l11l1_opy_ = False
bstack111l11111_opy_ = bstack11ll111_opy_ (u"ࠦࠧ࣋")
logger = logger_utils.get_logger(__name__, bstack1l11l1l1_opy_)
bstack1l1ll1ll11_opy_ = logger_utils.bstack11l1l11ll_opy_(__name__)
global_config = Config.get_instance()
percy = bstack1ll1111l_opy_()
bstack1lll1lllll_opy_ = bstack11111l111_opy_()
bstack1ll1111l1_opy_ = bstack1111111ll_opy_()
def bstack111l1111l_opy_():
  global CONFIG
  global bstack1l11ll1ll1_opy_
  global global_config
  testContextOptions = bstack11l111ll_opy_(CONFIG)
  if bstack11l1llllll_opy_(CONFIG):
    if (bstack11ll111_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ࣌") in testContextOptions and str(testContextOptions[bstack11ll111_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ࣍")]).lower() == bstack11ll111_opy_ (u"ࠧࡵࡴࡸࡩࠬ࣎")):
      bstack1l11ll1ll1_opy_ = True
      global_config.bstack11l1l1lll_opy_(True)
    global_config.bstack1ll1llll_opy_(testContextOptions.get(bstack11ll111_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷ࣏ࠬ"), False))
  else:
    bstack1l11ll1ll1_opy_ = True
    global_config.bstack11l1l1lll_opy_(True)
    global_config.bstack1ll1llll_opy_(True)
def bstack1llll111ll_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1ll1lll11_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l1l1lll11_opy_():
  global bstack11l11llll_opy_
  args = sys.argv
  for i in range(len(args)):
    if bstack11ll111_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡦࡳࡳ࡬ࡩࡨࡨ࡬ࡰࡪࠨ࣐") == args[i].lower() or bstack11ll111_opy_ (u"ࠥ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡮ࡧ࡫ࡪ࣑ࠦ") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      bstack11l11llll_opy_[bstack11ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ࣒")] = path
      return path
  return None
bstack1lll1111l_opy_ = re.compile(bstack11ll111_opy_ (u"ࡷࠨ࠮ࠫࡁ࡟ࠨࢀ࠮࠮ࠫࡁࠬࢁ࠳࠰࠿࣓ࠣ"))
def bstack1l11l111_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1lll1111l_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack11ll111_opy_ (u"ࠨࠤࡼࠤࣔ") + group + bstack11ll111_opy_ (u"ࠢࡾࠤࣕ"), os.environ.get(group))
  return value
def bstack1l1ll1l1_opy_():
  global bstack1ll1ll111_opy_
  if bstack1ll1ll111_opy_ is None:
        bstack1ll1ll111_opy_ = bstack1l1l1lll11_opy_()
  bstack1lll1ll1l_opy_ = bstack1ll1ll111_opy_
  if bstack1lll1ll1l_opy_ and os.path.exists(os.path.abspath(bstack1lll1ll1l_opy_)):
    fileName = bstack1lll1ll1l_opy_
  if bstack11ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬࣖ") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack11ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࡠࡈࡌࡐࡊ࠭ࣗ")])) and not bstack11ll111_opy_ (u"ࠪࡪ࡮ࡲࡥࡏࡣࡰࡩࠬࣘ") in locals():
    fileName = os.environ[bstack11ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨࣙ")]
  if bstack11ll111_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡑࡥࡲ࡫ࠧࣚ") in locals():
    bstack1_opy_ = os.path.abspath(fileName)
  else:
    bstack1_opy_ = bstack11ll111_opy_ (u"࠭ࠧࣛ")
  bstack1l1llll1l1_opy_ = os.getcwd()
  bstack11ll111l1_opy_ = bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪࣜ")
  bstack1l111l1l1_opy_ = bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺࡣࡰࡰࠬࣝ")
  while (not os.path.exists(bstack1_opy_)) and bstack1l1llll1l1_opy_ != bstack11ll111_opy_ (u"ࠤࠥࣞ"):
    bstack1_opy_ = os.path.join(bstack1l1llll1l1_opy_, bstack11ll111l1_opy_)
    if not os.path.exists(bstack1_opy_):
      bstack1_opy_ = os.path.join(bstack1l1llll1l1_opy_, bstack1l111l1l1_opy_)
    if bstack1l1llll1l1_opy_ != os.path.dirname(bstack1l1llll1l1_opy_):
      bstack1l1llll1l1_opy_ = os.path.dirname(bstack1l1llll1l1_opy_)
    else:
      bstack1l1llll1l1_opy_ = bstack11ll111_opy_ (u"ࠥࠦࣟ")
  bstack1ll1ll111_opy_ = bstack1_opy_ if os.path.exists(bstack1_opy_) else None
  return bstack1ll1ll111_opy_
def bstack11l1llll11_opy_(config):
    if bstack11ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࠫ࣠") in config:
      config[bstack11ll111_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ࣡")] = config[bstack11ll111_opy_ (u"࠭ࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬࠭࣢")]
    if bstack11ll111_opy_ (u"ࠧࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭ࡏࡱࡶ࡬ࡳࡳࡹࣣࠧ") in config:
      config[bstack11ll111_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬࣤ")] = config[bstack11ll111_opy_ (u"ࠩࡷࡩࡸࡺࡒࡦࡲࡲࡶࡹ࡯࡮ࡨࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣥ")]
def bstack1ll1l11ll1_opy_():
  bstack1_opy_ = bstack1l1ll1l1_opy_()
  if not os.path.exists(bstack1_opy_):
    bstack1l1ll11111_opy_(
      bstack1l11l11ll1_opy_.format(os.getcwd()))
  try:
    with open(bstack1_opy_, bstack11ll111_opy_ (u"ࠪࡶࣦࠬ")) as stream:
      yaml.add_implicit_resolver(bstack11ll111_opy_ (u"ࠦࠦࡶࡡࡵࡪࡨࡼࠧࣧ"), bstack1lll1111l_opy_)
      yaml.add_constructor(bstack11ll111_opy_ (u"ࠧࠧࡰࡢࡶ࡫ࡩࡽࠨࣨ"), bstack1l11l111_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      bstack11l1llll11_opy_(config)
      return config
  except:
    with open(bstack1_opy_, bstack11ll111_opy_ (u"࠭ࡲࠨࣩ")) as stream:
      try:
        config = yaml.safe_load(stream)
        bstack11l1llll11_opy_(config)
        return config
      except yaml.YAMLError as exc:
        bstack1l1ll11111_opy_(bstack11lll11l1l_opy_.format(str(exc)))
def bstack11ll1l11_opy_(config):
  bstack1ll11l111l_opy_ = bstack1lllll1ll_opy_(config)
  for option in list(bstack1ll11l111l_opy_):
    if option.lower() in bstack1ll1lll11l_opy_ and option != bstack1ll1lll11l_opy_[option.lower()]:
      bstack1ll11l111l_opy_[bstack1ll1lll11l_opy_[option.lower()]] = bstack1ll11l111l_opy_[option]
      del bstack1ll11l111l_opy_[option]
  return config
def bstack111l111l1l_opy_():
  global bstack1lll1l11ll_opy_
  for key, bstack111llll1l_opy_ in bstack1l11llll11_opy_.items():
    if isinstance(bstack111llll1l_opy_, list):
      for var in bstack111llll1l_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1lll1l11ll_opy_[key] = os.environ[var]
          break
    elif bstack111llll1l_opy_ in os.environ and os.environ[bstack111llll1l_opy_] and str(os.environ[bstack111llll1l_opy_]).strip():
      bstack1lll1l11ll_opy_[key] = os.environ[bstack111llll1l_opy_]
  if bstack11ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩ࣪") in os.environ:
    bstack1lll1l11ll_opy_[bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ࣫")] = {}
    bstack1lll1l11ll_opy_[bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭࣬")][bstack11ll111_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ࣭ࠬ")] = os.environ[bstack11ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࣮࠭")]
def bstack1l1llllll1_opy_():
  global bstack11l111ll11_opy_
  global bstack1lll1ll1ll_opy_
  global bstack11l11llll_opy_
  bstack1l1ll1l1l_opy_ = []
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) - 1 and bstack11ll111_opy_ (u"ࠬ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ࣯").lower() == val.lower():
      bstack11l111ll11_opy_[bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࣰࠪ")] = {}
      bstack11l111ll11_opy_[bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࣱࠫ")][bstack11ll111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࣲࠪ")] = sys.argv[idx + 1]
      bstack1l1ll1l1l_opy_.extend([idx, idx + 1])
      break
  for key, bstack11llll1lll_opy_ in bstack11l1l1ll_opy_.items():
    if isinstance(bstack11llll1lll_opy_, list):
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        for var in bstack11llll1lll_opy_:
          if bstack11ll111_opy_ (u"ࠩ࠰࠱ࠬࣳ") + var.lower() == val.lower() and key not in bstack11l111ll11_opy_:
            bstack11l111ll11_opy_[key] = sys.argv[idx + 1]
            bstack1lll1ll1ll_opy_ += bstack11ll111_opy_ (u"ࠪࠤ࠲࠳ࠧࣴ") + var + bstack11ll111_opy_ (u"ࠫࠥ࠭ࣵ") + shlex.quote(sys.argv[idx + 1])
            bstack11l1l11l11_opy_(bstack11l11llll_opy_, key, sys.argv[idx + 1])
            bstack1l1ll1l1l_opy_.extend([idx, idx + 1])
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        if bstack11ll111_opy_ (u"ࠬ࠳࠭ࠨࣶ") + bstack11llll1lll_opy_.lower() == val.lower() and key not in bstack11l111ll11_opy_:
          bstack11l111ll11_opy_[key] = sys.argv[idx + 1]
          bstack1lll1ll1ll_opy_ += bstack11ll111_opy_ (u"࠭ࠠ࠮࠯ࠪࣷ") + bstack11llll1lll_opy_ + bstack11ll111_opy_ (u"ࠧࠡࠩࣸ") + shlex.quote(sys.argv[idx + 1])
          bstack11l1l11l11_opy_(bstack11l11llll_opy_, key, sys.argv[idx + 1])
          bstack1l1ll1l1l_opy_.extend([idx, idx + 1])
  for idx in sorted(set(bstack1l1ll1l1l_opy_), reverse=True):
    if idx < len(sys.argv):
      del sys.argv[idx]
def bstack1l1l11ll1_opy_(config):
  bstack1l1ll1111l_opy_ = config.keys()
  for bstack1lllll1ll1_opy_, bstack111ll1ll1_opy_ in bstack11l111lll1_opy_.items():
    if bstack111ll1ll1_opy_ in bstack1l1ll1111l_opy_:
      config[bstack1lllll1ll1_opy_] = config[bstack111ll1ll1_opy_]
      del config[bstack111ll1ll1_opy_]
  for bstack1lllll1ll1_opy_, bstack111ll1ll1_opy_ in bstack1l1lll11l1_opy_.items():
    if isinstance(bstack111ll1ll1_opy_, list):
      for bstack11ll1ll1l1_opy_ in bstack111ll1ll1_opy_:
        if bstack11ll1ll1l1_opy_ in bstack1l1ll1111l_opy_:
          config[bstack1lllll1ll1_opy_] = config[bstack11ll1ll1l1_opy_]
          del config[bstack11ll1ll1l1_opy_]
          break
    elif bstack111ll1ll1_opy_ in bstack1l1ll1111l_opy_:
      config[bstack1lllll1ll1_opy_] = config[bstack111ll1ll1_opy_]
      del config[bstack111ll1ll1_opy_]
  for bstack11ll1ll1l1_opy_ in list(config):
    for bstack1ll1lllll_opy_ in bstack11l1ll11ll_opy_:
      if bstack11ll1ll1l1_opy_.lower() == bstack1ll1lllll_opy_.lower() and bstack11ll1ll1l1_opy_ != bstack1ll1lllll_opy_:
        config[bstack1ll1lllll_opy_] = config[bstack11ll1ll1l1_opy_]
        del config[bstack11ll1ll1l1_opy_]
  bstack1l1ll1l1ll_opy_ = [{}]
  if not config.get(bstack11ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࣹࠫ")):
    config[bstack11ll111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࣺࠬ")] = [{}]
  bstack1l1ll1l1ll_opy_ = config[bstack11ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣻ")]
  for platform in bstack1l1ll1l1ll_opy_:
    for bstack11ll1ll1l1_opy_ in list(platform):
      for bstack1ll1lllll_opy_ in bstack11l1ll11ll_opy_:
        if bstack11ll1ll1l1_opy_.lower() == bstack1ll1lllll_opy_.lower() and bstack11ll1ll1l1_opy_ != bstack1ll1lllll_opy_:
          platform[bstack1ll1lllll_opy_] = platform[bstack11ll1ll1l1_opy_]
          del platform[bstack11ll1ll1l1_opy_]
  for bstack1lllll1ll1_opy_, bstack111ll1ll1_opy_ in bstack1l1lll11l1_opy_.items():
    for platform in bstack1l1ll1l1ll_opy_:
      if isinstance(bstack111ll1ll1_opy_, list):
        for bstack11ll1ll1l1_opy_ in bstack111ll1ll1_opy_:
          if bstack11ll1ll1l1_opy_ in platform:
            platform[bstack1lllll1ll1_opy_] = platform[bstack11ll1ll1l1_opy_]
            del platform[bstack11ll1ll1l1_opy_]
            break
      elif bstack111ll1ll1_opy_ in platform:
        platform[bstack1lllll1ll1_opy_] = platform[bstack111ll1ll1_opy_]
        del platform[bstack111ll1ll1_opy_]
  for bstack11ll11l111_opy_ in bstack1l1llll1l_opy_:
    if bstack11ll11l111_opy_ in config:
      if not bstack1l1llll1l_opy_[bstack11ll11l111_opy_] in config:
        config[bstack1l1llll1l_opy_[bstack11ll11l111_opy_]] = {}
      config[bstack1l1llll1l_opy_[bstack11ll11l111_opy_]].update(config[bstack11ll11l111_opy_])
      del config[bstack11ll11l111_opy_]
  for platform in bstack1l1ll1l1ll_opy_:
    for bstack11ll11l111_opy_ in bstack1l1llll1l_opy_:
      if bstack11ll11l111_opy_ in list(platform):
        if not bstack1l1llll1l_opy_[bstack11ll11l111_opy_] in platform:
          platform[bstack1l1llll1l_opy_[bstack11ll11l111_opy_]] = {}
        platform[bstack1l1llll1l_opy_[bstack11ll11l111_opy_]].update(platform[bstack11ll11l111_opy_])
        del platform[bstack11ll11l111_opy_]
  config = bstack11ll1l11_opy_(config)
  return config
def bstack11l1l1111_opy_(config):
  global bstack11111ll1l_opy_
  bstack111lll1l1_opy_ = False
  if bstack11ll111_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨࣼ") in config and str(config[bstack11ll111_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩࣽ")]).lower() != bstack11ll111_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬࣾ"):
    if bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫࣿ") not in config or str(config[bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬऀ")]).lower() == bstack11ll111_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨँ"):
      config[bstack11ll111_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩं")] = False
    else:
      bstack1ll11l111_opy_ = bstack111lll1ll_opy_()
      if bstack11ll111_opy_ (u"ࠫ࡮ࡹࡔࡳ࡫ࡤࡰࡌࡸࡩࡥࠩः") in bstack1ll11l111_opy_:
        if not bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩऄ") in config:
          config[bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪअ")] = {}
        config[bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫआ")][bstack11ll111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪइ")] = bstack11ll111_opy_ (u"ࠩࡤࡸࡸ࠳ࡲࡦࡲࡨࡥࡹ࡫ࡲࠨई")
        bstack111lll1l1_opy_ = True
        bstack11111ll1l_opy_ = config[bstack11ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧउ")].get(bstack11ll111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ऊ"))
  if bstack11l1llllll_opy_(config) and bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩऋ") in config and str(config[bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪऌ")]).lower() != bstack11ll111_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ऍ") and not bstack111lll1l1_opy_:
    if not bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬऎ") in config:
      config[bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ए")] = {}
    if not config[bstack11ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧऐ")].get(bstack11ll111_opy_ (u"ࠫࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠨऑ")) and not bstack11ll111_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऒ") in config[bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪओ")]:
      current_time = datetime.datetime.now()
      bstack111l11lll_opy_ = current_time.strftime(bstack11ll111_opy_ (u"ࠧࠦࡦࡢࠩࡧࡥࠥࡉࠧࡐࠫऔ"))
      hostname = socket.gethostname()
      bstack11l1l1l111_opy_ = bstack11ll111_opy_ (u"ࠨࠩक").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack11ll111_opy_ (u"ࠩࡾࢁࡤࢁࡽࡠࡽࢀࠫख").format(bstack111l11lll_opy_, hostname, bstack11l1l1l111_opy_)
      config[bstack11ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧग")][bstack11ll111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭घ")] = identifier
    bstack11111ll1l_opy_ = config[bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩङ")].get(bstack11ll111_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨच"))
  return config
def bstack1ll1111111_opy_():
  bstack1ll1lll1ll_opy_ =  bstack1llll111_opy_()[bstack11ll111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷ࠭छ")]
  return bstack1ll1lll1ll_opy_ if bstack1ll1lll1ll_opy_ else -1
def bstack1ll1l111ll_opy_(bstack1ll1lll1ll_opy_):
  global CONFIG
  if not bstack11ll111_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪज") in CONFIG[bstack11ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫझ")]:
    return
  CONFIG[bstack11ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬञ")] = CONFIG[bstack11ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ट")].replace(
    bstack11ll111_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧठ"),
    str(bstack1ll1lll1ll_opy_)
  )
def bstack1l1l1l1ll1_opy_():
  global CONFIG
  if not bstack11ll111_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬड") in CONFIG[bstack11ll111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩढ")]:
    return
  current_time = datetime.datetime.now()
  bstack111l11lll_opy_ = current_time.strftime(bstack11ll111_opy_ (u"ࠨࠧࡧ࠱ࠪࡨ࠭ࠦࡊ࠽ࠩࡒ࠭ण"))
  CONFIG[bstack11ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫत")] = CONFIG[bstack11ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬथ")].replace(
    bstack11ll111_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪद"),
    bstack111l11lll_opy_
  )
def bstack111ll11l1_opy_():
  global CONFIG
  if bstack11ll111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧध") in CONFIG and not bool(CONFIG[bstack11ll111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨन")]):
    del CONFIG[bstack11ll111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऩ")]
    return
  if not bstack11ll111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪप") in CONFIG:
    CONFIG[bstack11ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫफ")] = bstack11ll111_opy_ (u"ࠪࠧࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ब")
  if bstack11ll111_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪभ") in CONFIG[bstack11ll111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧम")]:
    bstack1l1l1l1ll1_opy_()
    os.environ[bstack11ll111_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪय")] = CONFIG[bstack11ll111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩर")]
  if not bstack11ll111_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪऱ") in CONFIG[bstack11ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫल")]:
    return
  bstack1ll1lll1ll_opy_ = bstack11ll111_opy_ (u"ࠪࠫळ")
  bstack1l1lll1111_opy_ = bstack1ll1111111_opy_()
  if bstack1l1lll1111_opy_ != -1:
    bstack1ll1lll1ll_opy_ = bstack11ll111_opy_ (u"ࠫࡈࡏࠠࠨऴ") + str(bstack1l1lll1111_opy_)
  if bstack1ll1lll1ll_opy_ == bstack11ll111_opy_ (u"ࠬ࠭व"):
    bstack1l1111l1_opy_ = bstack1l1ll1llll_opy_(CONFIG[bstack11ll111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩश")])
    if bstack1l1111l1_opy_ != -1:
      bstack1ll1lll1ll_opy_ = str(bstack1l1111l1_opy_)
  if bstack1ll1lll1ll_opy_:
    bstack1ll1l111ll_opy_(bstack1ll1lll1ll_opy_)
    os.environ[bstack11ll111_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫष")] = CONFIG[bstack11ll111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪस")]
def bstack11l1l1l1_opy_(bstack11l11ll1l1_opy_, bstack1111l111l_opy_, path):
  bstack1ll11111_opy_ = {
    bstack11ll111_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ह"): bstack1111l111l_opy_
  }
  if os.path.exists(path):
    bstack111llll1ll_opy_ = json.load(open(path, bstack11ll111_opy_ (u"ࠪࡶࡧ࠭ऺ")))
  else:
    bstack111llll1ll_opy_ = {}
  bstack111llll1ll_opy_[bstack11l11ll1l1_opy_] = bstack1ll11111_opy_
  with open(path, bstack11ll111_opy_ (u"ࠦࡼ࠱ࠢऻ")) as outfile:
    json.dump(bstack111llll1ll_opy_, outfile)
def bstack1l1ll1llll_opy_(bstack11l11ll1l1_opy_):
  bstack11l11ll1l1_opy_ = str(bstack11l11ll1l1_opy_)
  bstack11l111l11l_opy_ = os.path.join(os.path.expanduser(bstack11ll111_opy_ (u"ࠬࢄ़ࠧ")), bstack11ll111_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ऽ"))
  try:
    if not os.path.exists(bstack11l111l11l_opy_):
      os.makedirs(bstack11l111l11l_opy_)
    file_path = os.path.join(os.path.expanduser(bstack11ll111_opy_ (u"ࠧࡿࠩा")), bstack11ll111_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨि"), bstack11ll111_opy_ (u"ࠩ࠱ࡦࡺ࡯࡬ࡥ࠯ࡱࡥࡲ࡫࠭ࡤࡣࡦ࡬ࡪ࠴ࡪࡴࡱࡱࠫी"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack11ll111_opy_ (u"ࠪࡻࠬु")):
        pass
      with open(file_path, bstack11ll111_opy_ (u"ࠦࡼ࠱ࠢू")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack11ll111_opy_ (u"ࠬࡸࠧृ")) as bstack11l111l11_opy_:
      bstack1lll11l1l_opy_ = json.load(bstack11l111l11_opy_)
    if bstack11l11ll1l1_opy_ in bstack1lll11l1l_opy_:
      bstack1l11lll111_opy_ = bstack1lll11l1l_opy_[bstack11l11ll1l1_opy_][bstack11ll111_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪॄ")]
      bstack11ll1lll11_opy_ = int(bstack1l11lll111_opy_) + 1
      bstack11l1l1l1_opy_(bstack11l11ll1l1_opy_, bstack11ll1lll11_opy_, file_path)
      return bstack11ll1lll11_opy_
    else:
      bstack11l1l1l1_opy_(bstack11l11ll1l1_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warning(bstack11l11lll11_opy_.format(str(e)))
    return -1
def bstack11l11111_opy_(config):
  if not config[bstack11ll111_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩॅ")] or not config[bstack11ll111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫॆ")]:
    return True
  else:
    return False
def bstack1111l1ll1_opy_(config, index=0):
  global bstack1llll11l1_opy_
  bstack1l1l1l11_opy_ = {}
  caps = bstack1l1l1lll1_opy_ + bstack1l1l11ll11_opy_
  if config.get(bstack11ll111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭े"), False):
    bstack1l1l1l11_opy_[bstack11ll111_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧै")] = True
    bstack1l1l1l11_opy_[bstack11ll111_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࡐࡲࡷ࡭ࡴࡴࡳࠨॉ")] = config.get(bstack11ll111_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩॊ"), {})
  if bstack1llll11l1_opy_:
    caps += bstack1ll1111l1l_opy_
  for key in config:
    if key in caps + [bstack11ll111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩो")]:
      continue
    bstack1l1l1l11_opy_[key] = config[key]
  if bstack11ll111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪौ") in config:
    for bstack1l1l1l1l11_opy_ in config[bstack11ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶ्ࠫ")][index]:
      if bstack1l1l1l1l11_opy_ in caps:
        continue
      bstack1l1l1l11_opy_[bstack1l1l1l1l11_opy_] = config[bstack11ll111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॎ")][index][bstack1l1l1l1l11_opy_]
  bstack1l1l1l11_opy_[bstack11ll111_opy_ (u"ࠪ࡬ࡴࡹࡴࡏࡣࡰࡩࠬॏ")] = socket.gethostname()
  if bstack11ll111_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬॐ") in bstack1l1l1l11_opy_:
    del (bstack1l1l1l11_opy_[bstack11ll111_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭॑")])
  return bstack1l1l1l11_opy_
def bstack11llll1ll1_opy_(config):
  global bstack1llll11l1_opy_
  bstack1l11ll1l1l_opy_ = {}
  caps = bstack1l1l11ll11_opy_
  if bstack1llll11l1_opy_:
    caps += bstack1ll1111l1l_opy_
  for key in caps:
    if key in config:
      bstack1l11ll1l1l_opy_[key] = config[key]
  return bstack1l11ll1l1l_opy_
def bstack1l1l111l1_opy_(bstack1l1l1l11_opy_, bstack1l11ll1l1l_opy_):
  bstack111l11ll_opy_ = {}
  for key in bstack1l1l1l11_opy_.keys():
    if key in bstack11l111lll1_opy_:
      bstack111l11ll_opy_[bstack11l111lll1_opy_[key]] = bstack1l1l1l11_opy_[key]
    else:
      bstack111l11ll_opy_[key] = bstack1l1l1l11_opy_[key]
  for key in bstack1l11ll1l1l_opy_:
    if key in bstack11l111lll1_opy_:
      bstack111l11ll_opy_[bstack11l111lll1_opy_[key]] = bstack1l11ll1l1l_opy_[key]
    else:
      bstack111l11ll_opy_[key] = bstack1l11ll1l1l_opy_[key]
  return bstack111l11ll_opy_
def bstack11l1111l1l_opy_(config, index=0):
  global bstack1llll11l1_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack111l1ll1_opy_ = bstack11ll1llll1_opy_(bstack1ll11111l_opy_, config, logger)
  bstack1l11ll1l1l_opy_ = bstack11llll1ll1_opy_(config)
  bstack1111ll111_opy_ = bstack1l1l11ll11_opy_
  bstack1111ll111_opy_ += bstack11llll1ll_opy_
  bstack1l11ll1l1l_opy_ = update(bstack1l11ll1l1l_opy_, bstack111l1ll1_opy_)
  if bstack1llll11l1_opy_:
    bstack1111ll111_opy_ += bstack1ll1111l1l_opy_
  if bstack11ll111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴ॒ࠩ") in config:
    if bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ॓") in config[bstack11ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ॔")][index]:
      caps[bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧॕ")] = config[bstack11ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॖ")][index][bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩॗ")]
    if bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭क़") in config[bstack11ll111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩख़")][index]:
      caps[bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨग़")] = str(config[bstack11ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫज़")][index][bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪड़")])
    bstack11ll1l111_opy_ = bstack11ll1llll1_opy_(bstack1ll11111l_opy_, config[bstack11ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ढ़")][index], logger)
    bstack1111ll111_opy_ += list(bstack11ll1l111_opy_.keys())
    for bstack1ll1l11l_opy_ in bstack1111ll111_opy_:
      if bstack1ll1l11l_opy_ in config[bstack11ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧफ़")][index]:
        if bstack1ll1l11l_opy_ == bstack11ll111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧय़"):
          try:
            bstack11ll1l111_opy_[bstack1ll1l11l_opy_] = str(config[bstack11ll111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩॠ")][index][bstack1ll1l11l_opy_] * 1.0)
          except:
            bstack11ll1l111_opy_[bstack1ll1l11l_opy_] = str(config[bstack11ll111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪॡ")][index][bstack1ll1l11l_opy_])
        else:
          bstack11ll1l111_opy_[bstack1ll1l11l_opy_] = config[bstack11ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫॢ")][index][bstack1ll1l11l_opy_]
        del (config[bstack11ll111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॣ")][index][bstack1ll1l11l_opy_])
    bstack1l11ll1l1l_opy_ = update(bstack1l11ll1l1l_opy_, bstack11ll1l111_opy_)
  bstack1l1l1l11_opy_ = bstack1111l1ll1_opy_(config, index)
  for bstack11ll1ll1l1_opy_ in bstack1l1l11ll11_opy_ + list(bstack111l1ll1_opy_.keys()):
    if bstack11ll1ll1l1_opy_ in bstack1l1l1l11_opy_:
      bstack1l11ll1l1l_opy_[bstack11ll1ll1l1_opy_] = bstack1l1l1l11_opy_[bstack11ll1ll1l1_opy_]
      del (bstack1l1l1l11_opy_[bstack11ll1ll1l1_opy_])
  if bstack1ll1lll1l1_opy_(config):
    bstack1l1l1l11_opy_[bstack11ll111_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ।")] = True
    caps.update(bstack1l11ll1l1l_opy_)
    caps[bstack11ll111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ॥")] = bstack1l1l1l11_opy_
  else:
    bstack1l1l1l11_opy_[bstack11ll111_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ०")] = False
    caps.update(bstack1l1l111l1_opy_(bstack1l1l1l11_opy_, bstack1l11ll1l1l_opy_))
    if bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ१") in caps:
      caps[bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ२")] = caps[bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭३")]
      del (caps[bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ४")])
    if bstack11ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ५") in caps:
      caps[bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭६")] = caps[bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭७")]
      del (caps[bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ८")])
  return caps
def bstack1l111lll11_opy_():
  global bstack11lll111ll_opy_
  global CONFIG
  if bstack11lll111ll_opy_ != bstack11ll111_opy_ (u"ࠧࠨ९") and (bstack11lll111ll_opy_.startswith(bstack11ll111_opy_ (u"ࠨࡪࡷࡸࡵࡀ࠯࠰ࠩ॰")) or bstack11lll111ll_opy_.startswith(bstack11ll111_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠫॱ"))):
    return bstack11lll111ll_opy_
  if bstack1ll1lll11_opy_() <= version.parse(bstack11ll111_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪॲ")):
    if bstack11lll111ll_opy_ != bstack11ll111_opy_ (u"ࠫࠬॳ"):
      return bstack11ll111_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨॴ") + bstack11lll111ll_opy_ + bstack11ll111_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥॵ")
    return bstack1l11l11l11_opy_
  if bstack11lll111ll_opy_ != bstack11ll111_opy_ (u"ࠧࠨॶ"):
    return bstack11ll111_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥॷ") + bstack11lll111ll_opy_ + bstack11ll111_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥॸ")
  return HTTPS_HUB
def bstack1lll1l1l1l_opy_(options):
  return hasattr(options, bstack11ll111_opy_ (u"ࠪࡷࡪࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠫॹ"))
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
def bstack1l1l11111l_opy_(options, bstack1llll11l1l_opy_):
  for bstack1l1ll1l111_opy_ in bstack1llll11l1l_opy_:
    if bstack1l1ll1l111_opy_ in [bstack11ll111_opy_ (u"ࠫࡦࡸࡧࡴࠩॺ"), bstack11ll111_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩॻ")]:
      continue
    if bstack1l1ll1l111_opy_ in options._experimental_options:
      options._experimental_options[bstack1l1ll1l111_opy_] = update(options._experimental_options[bstack1l1ll1l111_opy_],
                                                         bstack1llll11l1l_opy_[bstack1l1ll1l111_opy_])
    else:
      options.add_experimental_option(bstack1l1ll1l111_opy_, bstack1llll11l1l_opy_[bstack1l1ll1l111_opy_])
  if bstack11ll111_opy_ (u"࠭ࡡࡳࡩࡶࠫॼ") in bstack1llll11l1l_opy_:
    for arg in bstack1llll11l1l_opy_[bstack11ll111_opy_ (u"ࠧࡢࡴࡪࡷࠬॽ")]:
      options.add_argument(arg)
    del (bstack1llll11l1l_opy_[bstack11ll111_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ॾ")])
  if bstack11ll111_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ॿ") in bstack1llll11l1l_opy_:
    for ext in bstack1llll11l1l_opy_[bstack11ll111_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧঀ")]:
      try:
        options.add_extension(ext)
      except OSError:
        options.add_encoded_extension(ext)
    del (bstack1llll11l1l_opy_[bstack11ll111_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨঁ")])
def bstack11l11l11l1_opy_(options):
  bstack11ll111_opy_ (u"ࠧࠨࠢࠋࠢࠣࡍࡳࡰࡥࡤࡶࠣࡨࡪ࡬ࡡࡶ࡮ࡷࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡴࡶࡴࡪࡱࡱࡷࠥ࡬࡯ࡳࠢ࡯ࡳࡦࡪࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡹ࡫ࡩࡳࠦ࡯ࡷࡧࡵࡶ࡮ࡪࡥࡍࡱࡤࡨ࡙࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡧࡱࡥࡧࡲࡥࡥ࠰ࠍࠤࠥࡊࡥࡧࡧࡱࡷ࡮ࡼࡥ࠻ࠢࡱࡩࡻ࡫ࡲࠡࡱࡹࡩࡷࡽࡲࡪࡶࡨࡷࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠࡢࡴࡪࡷ࠱ࠦ࡯࡯࡮ࡼࠤࡦࡪࡤࡴࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡳࡳ࡫ࡳ࠯ࠌࠣࠤࡘ࡯࡭ࡪ࡮ࡤࡶࠥࡺ࡯ࠡࡌࡤࡺࡦࠦࡓࡅࡍࠪࡷࠥࡕࡶࡦࡴࡵ࡭ࡩ࡫ࡌࡰࡣࡧࡘࡪࡹࡴࡪࡰࡪࡇ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࡋࡩࡱࡶࡥࡳ࠰ࠍࠤ࡚ࠥࡨࡪࡵࠣ࡭ࡸࠦࡡࠡࡹࡵࡥࡵࡶࡥࡳࠢࡤࡶࡴࡻ࡮ࡥࠢࡷ࡬ࡪࠦࡣࡦࡰࡷࡶࡦࡲࡩࡻࡧࡧࠤ࡭࡫࡬ࡱࡧࡵࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠥࠦࠧং")
  global CONFIG
  global bstack1ll1lllll1_opy_
  try:
    if not bstack1ll1lllll1_opy_ or not options:
      return options
    from bstack_utils.bstack1ll1ll11ll_opy_ import bstack111l1ll1l_opy_
    bstack1l1ll1l1l1_opy_ = bstack111l1ll1l_opy_(options, bstack11l1ll1l1_opy_=bstack11ll111_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࠨঃ"))
    if bstack1l1ll1l1l1_opy_ > 0:
      logger.debug(bstack11ll111_opy_ (u"ࠢࡍࡱࡤࡨࠥࡺࡥࡴࡶ࡬ࡲ࡬ࡀࠠࡂࡦࡧࡩࡩࠦࡻࡾࠢࡧࡩ࡫ࡧࡵ࡭ࡶࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠦࡦࡰࡴࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧࠥ঄").format(bstack1l1ll1l1l1_opy_))
  except Exception as e:
    logger.debug(bstack11ll111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡮ࡴࡪࡦࡥࡷࠤࡱࡵࡡࡥࠢࡷࡩࡸࡺࡩ࡯ࡩࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࢁࡽࠣঅ").format(e))
  return options
def bstack111l1l11ll_opy_(options, bstack111ll11l1l_opy_):
  if bstack11ll111_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨআ") in bstack111ll11l1l_opy_:
    for bstack1111lllll_opy_ in bstack111ll11l1l_opy_[bstack11ll111_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩই")]:
      if bstack1111lllll_opy_ in options._preferences:
        options._preferences[bstack1111lllll_opy_] = update(options._preferences[bstack1111lllll_opy_], bstack111ll11l1l_opy_[bstack11ll111_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪঈ")][bstack1111lllll_opy_])
      else:
        options.set_preference(bstack1111lllll_opy_, bstack111ll11l1l_opy_[bstack11ll111_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫউ")][bstack1111lllll_opy_])
  if bstack11ll111_opy_ (u"࠭ࡡࡳࡩࡶࠫঊ") in bstack111ll11l1l_opy_:
    for arg in bstack111ll11l1l_opy_[bstack11ll111_opy_ (u"ࠧࡢࡴࡪࡷࠬঋ")]:
      options.add_argument(arg)
def bstack1111ll11l_opy_(options, bstack1llll1l111_opy_):
  if bstack11ll111_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࠩঌ") in bstack1llll1l111_opy_:
    options.use_webview(bool(bstack1llll1l111_opy_[bstack11ll111_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࠪ঍")]))
  bstack1l1l11111l_opy_(options, bstack1llll1l111_opy_)
def bstack11l111l1ll_opy_(options, bstack1ll1l1ll1l_opy_):
  for bstack11lll11l1_opy_ in bstack1ll1l1ll1l_opy_:
    if bstack11lll11l1_opy_ in [bstack11ll111_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧ঎"), bstack11ll111_opy_ (u"ࠫࡦࡸࡧࡴࠩএ")]:
      continue
    options.set_capability(bstack11lll11l1_opy_, bstack1ll1l1ll1l_opy_[bstack11lll11l1_opy_])
  if bstack11ll111_opy_ (u"ࠬࡧࡲࡨࡵࠪঐ") in bstack1ll1l1ll1l_opy_:
    for arg in bstack1ll1l1ll1l_opy_[bstack11ll111_opy_ (u"࠭ࡡࡳࡩࡶࠫ঑")]:
      options.add_argument(arg)
  if bstack11ll111_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫ঒") in bstack1ll1l1ll1l_opy_:
    options.bstack1ll11lll1_opy_(bool(bstack1ll1l1ll1l_opy_[bstack11ll111_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬও")]))
def bstack1l1111ll1_opy_(options, bstack1ll1l1l111_opy_):
  for bstack1l11lllll_opy_ in bstack1ll1l1l111_opy_:
    if bstack1l11lllll_opy_ in [bstack11ll111_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ঔ"), bstack11ll111_opy_ (u"ࠪࡥࡷ࡭ࡳࠨক")]:
      continue
    options._options[bstack1l11lllll_opy_] = bstack1ll1l1l111_opy_[bstack1l11lllll_opy_]
  if bstack11ll111_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨখ") in bstack1ll1l1l111_opy_:
    for bstack1ll1111ll_opy_ in bstack1ll1l1l111_opy_[bstack11ll111_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩগ")]:
      options.bstack11l1ll11_opy_(
        bstack1ll1111ll_opy_, bstack1ll1l1l111_opy_[bstack11ll111_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪঘ")][bstack1ll1111ll_opy_])
  if bstack11ll111_opy_ (u"ࠧࡢࡴࡪࡷࠬঙ") in bstack1ll1l1l111_opy_:
    for arg in bstack1ll1l1l111_opy_[bstack11ll111_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭চ")]:
      options.add_argument(arg)
def bstack111111ll1_opy_(options, caps):
  if not hasattr(options, bstack11ll111_opy_ (u"ࠩࡎࡉ࡞࠭ছ")):
    return
  if options.KEY == bstack11ll111_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨজ"):
    options = bstack11l11l11ll_opy_.bstack1l111ll11_opy_(bstack11111lll1_opy_=options, config=CONFIG)
  if options.KEY == bstack11ll111_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩঝ") and options.KEY in caps:
    bstack1l1l11111l_opy_(options, caps[bstack11ll111_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪঞ")])
  elif options.KEY == bstack11ll111_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫট") and options.KEY in caps:
    bstack111l1l11ll_opy_(options, caps[bstack11ll111_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬঠ")])
  elif options.KEY == bstack11ll111_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩড") and options.KEY in caps:
    bstack11l111l1ll_opy_(options, caps[bstack11ll111_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪঢ")])
  elif options.KEY == bstack11ll111_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫণ") and options.KEY in caps:
    bstack1111ll11l_opy_(options, caps[bstack11ll111_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬত")])
  elif options.KEY == bstack11ll111_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫথ") and options.KEY in caps:
    bstack1l1111ll1_opy_(options, caps[bstack11ll111_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬদ")])
def bstack1ll1ll1ll1_opy_(caps):
  global bstack1llll11l1_opy_
  if isinstance(os.environ.get(bstack11ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨধ")), str):
    bstack1llll11l1_opy_ = eval(os.getenv(bstack11ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩন")))
  if bstack1llll11l1_opy_:
    if bstack1llll111ll_opy_() < version.parse(bstack11ll111_opy_ (u"ࠩ࠵࠲࠸࠴࠰ࠨ঩")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack11ll111_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪপ")
    if bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩফ") in caps:
      browser = caps[bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪব")]
    elif bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧভ") in caps:
      browser = caps[bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨম")]
    browser = str(browser).lower()
    if browser == bstack11ll111_opy_ (u"ࠨ࡫ࡳ࡬ࡴࡴࡥࠨয") or browser == bstack11ll111_opy_ (u"ࠩ࡬ࡴࡦࡪࠧর"):
      browser = bstack11ll111_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪ঱")
    if browser == bstack11ll111_opy_ (u"ࠫࡸࡧ࡭ࡴࡷࡱ࡫ࠬল"):
      browser = bstack11ll111_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬ঳")
    if browser not in [bstack11ll111_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭঴"), bstack11ll111_opy_ (u"ࠧࡦࡦࡪࡩࠬ঵"), bstack11ll111_opy_ (u"ࠨ࡫ࡨࠫশ"), bstack11ll111_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩষ"), bstack11ll111_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫস")]:
      return None
    try:
      package = bstack11ll111_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳ࠰ࡾࢁ࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭হ").format(browser)
      name = bstack11ll111_opy_ (u"ࠬࡕࡰࡵ࡫ࡲࡲࡸ࠭঺")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1lll1l1l1l_opy_(options):
        return None
      for bstack11ll1ll1l1_opy_ in caps.keys():
        options.set_capability(bstack11ll1ll1l1_opy_, caps[bstack11ll1ll1l1_opy_])
      bstack111111ll1_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack11l1l11l1l_opy_(options, bstack1l11l11111_opy_):
  if not bstack1lll1l1l1l_opy_(options):
    return
  for bstack11ll1ll1l1_opy_ in bstack1l11l11111_opy_.keys():
    if bstack11ll1ll1l1_opy_ in bstack11llll1ll_opy_:
      continue
    if bstack11ll1ll1l1_opy_ in options._caps and type(options._caps[bstack11ll1ll1l1_opy_]) in [dict, list]:
      options._caps[bstack11ll1ll1l1_opy_] = update(options._caps[bstack11ll1ll1l1_opy_], bstack1l11l11111_opy_[bstack11ll1ll1l1_opy_])
    else:
      options.set_capability(bstack11ll1ll1l1_opy_, bstack1l11l11111_opy_[bstack11ll1ll1l1_opy_])
  bstack111111ll1_opy_(options, bstack1l11l11111_opy_)
  if bstack11ll111_opy_ (u"࠭࡭ࡰࡼ࠽ࡨࡪࡨࡵࡨࡩࡨࡶࡆࡪࡤࡳࡧࡶࡷࠬ঻") in options._caps:
    if options._caps[bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩ়ࠬ")] and options._caps[bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ঽ")].lower() != bstack11ll111_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪা"):
      del options._caps[bstack11ll111_opy_ (u"ࠪࡱࡴࢀ࠺ࡥࡧࡥࡹ࡬࡭ࡥࡳࡃࡧࡨࡷ࡫ࡳࡴࠩি")]
def bstack111111l11_opy_(proxy_config):
  if bstack11ll111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨী") in proxy_config:
    proxy_config[bstack11ll111_opy_ (u"ࠬࡹࡳ࡭ࡒࡵࡳࡽࡿࠧু")] = proxy_config[bstack11ll111_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪূ")]
    del (proxy_config[bstack11ll111_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫৃ")])
  if bstack11ll111_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫৄ") in proxy_config and proxy_config[bstack11ll111_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬ৅")].lower() != bstack11ll111_opy_ (u"ࠪࡨ࡮ࡸࡥࡤࡶࠪ৆"):
    proxy_config[bstack11ll111_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧে")] = bstack11ll111_opy_ (u"ࠬࡳࡡ࡯ࡷࡤࡰࠬৈ")
  if bstack11ll111_opy_ (u"࠭ࡰࡳࡱࡻࡽࡆࡻࡴࡰࡥࡲࡲ࡫࡯ࡧࡖࡴ࡯ࠫ৉") in proxy_config:
    proxy_config[bstack11ll111_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪ৊")] = bstack11ll111_opy_ (u"ࠨࡲࡤࡧࠬো")
  return proxy_config
def bstack1llll1111_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack11ll111_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨৌ") in config:
    return proxy
  config[bstack11ll111_opy_ (u"ࠪࡴࡷࡵࡸࡺ্ࠩ")] = bstack111111l11_opy_(config[bstack11ll111_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪৎ")])
  if proxy == None:
    proxy = Proxy(config[bstack11ll111_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ৏")])
  return proxy
def bstack11lll1l1_opy_(self):
  global CONFIG
  global bstack1l11l1l11_opy_
  try:
    proxy = bstack1111lllll1_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack11ll111_opy_ (u"࠭࠮ࡱࡣࡦࠫ৐")):
        proxies = bstack111l11ll11_opy_(proxy, bstack1l111lll11_opy_())
        if len(proxies) > 0:
          protocol, bstack111lllll11_opy_ = proxies.popitem()
          if bstack11ll111_opy_ (u"ࠢ࠻࠱࠲ࠦ৑") in bstack111lllll11_opy_:
            return bstack111lllll11_opy_
          else:
            return bstack11ll111_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ৒") + bstack111lllll11_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack11ll111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡶࡲࡰࡺࡼࠤࡺࡸ࡬ࠡ࠼ࠣࡿࢂࠨ৓").format(str(e)))
  return bstack1l11l1l11_opy_(self)
def bstack1ll11ll1l1_opy_():
  global CONFIG
  return bstack1lllll1l11_opy_(CONFIG) and bstack1lllll11l_opy_() and bstack1ll1lll11_opy_() >= version.parse(bstack11lll1l1l_opy_)
def bstack11lll1ll11_opy_():
  global CONFIG
  return (bstack11ll111_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭৔") in CONFIG or bstack11ll111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ৕") in CONFIG) and bstack1l1111lll1_opy_()
def bstack1lllll1ll_opy_(config):
  bstack1ll11l111l_opy_ = {}
  if bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ৖") in config:
    bstack1ll11l111l_opy_ = config[bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪৗ")]
  if bstack11ll111_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭৘") in config:
    bstack1ll11l111l_opy_ = config[bstack11ll111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ৙")]
  proxy = bstack1111lllll1_opy_(config)
  if proxy:
    if proxy.endswith(bstack11ll111_opy_ (u"ࠩ࠱ࡴࡦࡩࠧ৚")) and os.path.isfile(proxy):
      bstack1ll11l111l_opy_[bstack11ll111_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭৛")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack11ll111_opy_ (u"ࠫ࠳ࡶࡡࡤࠩড়")):
        proxies = bstack1111llll1l_opy_(config, bstack1l111lll11_opy_())
        if len(proxies) > 0:
          protocol, bstack111lllll11_opy_ = proxies.popitem()
          if bstack11ll111_opy_ (u"ࠧࡀ࠯࠰ࠤঢ়") in bstack111lllll11_opy_:
            parsed_url = urlparse(bstack111lllll11_opy_)
          else:
            parsed_url = urlparse(protocol + bstack11ll111_opy_ (u"ࠨ࠺࠰࠱ࠥ৞") + bstack111lllll11_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1ll11l111l_opy_[bstack11ll111_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪয়")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1ll11l111l_opy_[bstack11ll111_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡰࡴࡷࠫৠ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1ll11l111l_opy_[bstack11ll111_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬৡ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1ll11l111l_opy_[bstack11ll111_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭ৢ")] = str(parsed_url.password)
  return bstack1ll11l111l_opy_
def bstack11l111ll_opy_(config):
  if bstack11ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩৣ") in config:
    return config[bstack11ll111_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪ৤")]
  return {}
def bstack1l1111l1l_opy_(caps):
  global bstack11111ll1l_opy_
  if bstack11ll111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ৥") in caps:
    caps[bstack11ll111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ০")][bstack11ll111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧ১")] = True
    if bstack11111ll1l_opy_:
      caps[bstack11ll111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ২")][bstack11ll111_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ৩")] = bstack11111ll1l_opy_
  else:
    caps[bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩ৪")] = True
    if bstack11111ll1l_opy_:
      caps[bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭৫")] = bstack11111ll1l_opy_
@measure(event_name=EVENTS.bstack11111l1ll_opy_, stage=STAGE.bstack1111l1111_opy_, bstack11ll11ll11_opy_=bstack1lll11lll_opy_)
def bstack11ll1lll1l_opy_():
  global CONFIG
  if not bstack11l1llllll_opy_(CONFIG) or cli.is_enabled(CONFIG):
    return
  if bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ৬") in CONFIG and bstack11l1lll1_opy_(CONFIG[bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ৭")]):
    if (
      bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ৮") in CONFIG
      and bstack11l1lll1_opy_(CONFIG[bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭৯")].get(bstack11ll111_opy_ (u"ࠪࡷࡰ࡯ࡰࡃ࡫ࡱࡥࡷࡿࡉ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡣࡷ࡭ࡴࡴࠧৰ")))
    ):
      logger.debug(bstack11ll111_opy_ (u"ࠦࡑࡵࡣࡢ࡮ࠣࡦ࡮ࡴࡡࡳࡻࠣࡲࡴࡺࠠࡴࡶࡤࡶࡹ࡫ࡤࠡࡣࡶࠤࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤࡪࡴࡡࡣ࡮ࡨࡨࠧৱ"))
      return
    bstack1ll11l111l_opy_ = bstack1lllll1ll_opy_(CONFIG)
    bstack1ll11lll1l_opy_(CONFIG[bstack11ll111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ৲")], bstack1ll11l111l_opy_)
def bstack1ll11lll1l_opy_(key, bstack1ll11l111l_opy_):
  global bstack11l1lllll1_opy_
  logger.info(bstack1l11llll1l_opy_)
  try:
    bstack11l1lllll1_opy_ = Local()
    bstack1l11ll11l_opy_ = {bstack11ll111_opy_ (u"࠭࡫ࡦࡻࠪ৳"): key}
    bstack1l11ll11l_opy_.update(bstack1ll11l111l_opy_)
    logger.debug(bstack1ll11l1l11_opy_.format(str(bstack1l11ll11l_opy_)).replace(key, bstack11ll111_opy_ (u"ࠧ࡜ࡔࡈࡈࡆࡉࡔࡆࡆࡠࠫ৴")))
    bstack11l1lllll1_opy_.start(**bstack1l11ll11l_opy_)
    if bstack11l1lllll1_opy_.isRunning():
      logger.info(bstack1ll1lll1_opy_)
  except Exception as e:
    bstack1l1ll11111_opy_(bstack1llllll1l_opy_.format(str(e)))
def bstack11l1lll11_opy_():
  global bstack11l1lllll1_opy_
  if bstack11l1lllll1_opy_.isRunning():
    logger.info(bstack1ll11l11_opy_)
    bstack11l1lllll1_opy_.stop()
  bstack11l1lllll1_opy_ = None
def bstack1lllll1lll_opy_(bstack11l11lll1l_opy_=[]):
  global CONFIG
  bstack11l11ll1l_opy_ = []
  bstack11ll11ll1_opy_ = [bstack11ll111_opy_ (u"ࠨࡱࡶࠫ৵"), bstack11ll111_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬ৶"), bstack11ll111_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧ৷"), bstack11ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭৸"), bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ৹"), bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ৺")]
  try:
    for err in bstack11l11lll1l_opy_:
      bstack1llll11lll_opy_ = {}
      for k in bstack11ll11ll1_opy_:
        val = CONFIG[bstack11ll111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ৻")][int(err[bstack11ll111_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧৼ")])].get(k)
        if val:
          bstack1llll11lll_opy_[k] = val
      if(err[bstack11ll111_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ৽")] != bstack11ll111_opy_ (u"ࠪࠫ৾")):
        bstack1llll11lll_opy_[bstack11ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡵࠪ৿")] = {
          err[bstack11ll111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ਀")]: err[bstack11ll111_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬਁ")]
        }
        bstack11l11ll1l_opy_.append(bstack1llll11lll_opy_)
  except Exception as e:
    logger.debug(bstack11ll111_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡳࡷࡳࡡࡵࡶ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺ࠺ࠡࠩਂ") + str(e))
  finally:
    return bstack11l11ll1l_opy_
def bstack1l1lll111_opy_(file_name):
  bstack1l1l11ll1l_opy_ = []
  try:
    bstack1l1lll11ll_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1l1lll11ll_opy_):
      with open(bstack1l1lll11ll_opy_) as f:
        bstack111l111l11_opy_ = json.load(f)
        bstack1l1l11ll1l_opy_ = bstack111l111l11_opy_
      os.remove(bstack1l1lll11ll_opy_)
    return bstack1l1l11ll1l_opy_
  except Exception as e:
    logger.debug(bstack11ll111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪ࡮ࡴࡤࡪࡰࡪࠤࡪࡸࡲࡰࡴࠣࡰ࡮ࡹࡴ࠻ࠢࠪਃ") + str(e))
    return bstack1l1l11ll1l_opy_
def bstack111l1l1ll1_opy_():
  try:
      import time
      from bstack_utils.constants import bstack1lllll11l1_opy_, EVENTS
      from bstack_utils.helper import bstack1l1l11ll_opy_, get_host_info, global_config
      from datetime import datetime
      from filelock import FileLock
      from bstack_utils.bstack11111111l_opy_ import bstack1111l1l1l_opy_
      bstack1111l1l1l_opy_.bstack111ll1ll1l_opy_()
      bstack1lll111ll1_opy_ = os.path.join(os.getcwd(), bstack11ll111_opy_ (u"ࠩ࡯ࡳ࡬࠭਄"), bstack11ll111_opy_ (u"ࠪ࡯ࡪࡿ࠭࡮ࡧࡷࡶ࡮ࡩࡳ࠯࡬ࡶࡳࡳ࠭ਅ"))
      data = None
      lock = FileLock(bstack1lll111ll1_opy_+bstack11ll111_opy_ (u"ࠦ࠳ࡲ࡯ࡤ࡭ࠥਆ"), timeout=2)
      try:
          with lock:
              with open(bstack1lll111ll1_opy_, bstack11ll111_opy_ (u"ࠧࡸࠢਇ"), encoding=bstack11ll111_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧਈ")) as file:
                  data = json.load(file)
      except Exception as e:
          logger.debug(bstack11ll111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡶࡪࡧࡤࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࠦࡦࡪ࡮ࡨ࠾ࠥࢁࡽࠣਉ").format(e))
          return
      if not data:
          return
      def bstack11ll11111_opy_():
          try:
              config = {
                  bstack11ll111_opy_ (u"ࠣࡪࡨࡥࡩ࡫ࡲࡴࠤਊ"): {
                      bstack11ll111_opy_ (u"ࠤࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠣ਋"): bstack11ll111_opy_ (u"ࠥࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳࠨ਌"),
                  }
              }
              bstack11ll11l1l_opy_ = datetime.utcnow()
              current_time = bstack11ll11l1l_opy_.strftime(bstack11ll111_opy_ (u"ࠦࠪ࡟࠭ࠦ࡯࠰ࠩࡩ࡚ࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࠯ࠧࡩࠤ࡚࡚ࡃࠣ਍"))
              bstack111lll1111_opy_ = os.environ.get(bstack11ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ਎")) if os.environ.get(bstack11ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫਏ")) else global_config.get_property(bstack11ll111_opy_ (u"ࠢࡴࡦ࡮ࡖࡺࡴࡉࡥࠤਐ"))
              payload = {
                  bstack11ll111_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠧ਑"): bstack11ll111_opy_ (u"ࠤࡶࡨࡰࡥࡥࡷࡧࡱࡸࡸࠨ਒"),
                  bstack11ll111_opy_ (u"ࠥࡨࡦࡺࡡࠣਓ"): {
                      bstack11ll111_opy_ (u"ࠦࡹ࡫ࡳࡵࡪࡸࡦࡤࡻࡵࡪࡦࠥਔ"): bstack111lll1111_opy_,
                      bstack11ll111_opy_ (u"ࠧࡩࡲࡦࡣࡷࡩࡩࡥࡤࡢࡻࠥਕ"): current_time,
                      bstack11ll111_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡴࡡ࡮ࡧࠥਖ"): bstack11ll111_opy_ (u"ࠢࡔࡆࡎࡊࡪࡧࡴࡶࡴࡨࡔࡪࡸࡦࡰࡴࡰࡥࡳࡩࡥࠣਗ"),
                      bstack11ll111_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟࡫ࡵࡲࡲࠧਘ"): {
                          bstack11ll111_opy_ (u"ࠤࡰࡩࡦࡹࡵࡳࡧࡶࠦਙ"): data,
                          bstack11ll111_opy_ (u"ࠥࡷࡩࡱࡒࡶࡰࡌࡨࠧਚ"): global_config.get_property(bstack11ll111_opy_ (u"ࠦࡸࡪ࡫ࡓࡷࡱࡍࡩࠨਛ"))
                      },
                      bstack11ll111_opy_ (u"ࠧࡻࡳࡦࡴࡢࡨࡦࡺࡡࠣਜ"): global_config.get_property(bstack11ll111_opy_ (u"ࠨࡵࡴࡧࡵࡒࡦࡳࡥࠣਝ")),
                      bstack11ll111_opy_ (u"ࠢࡩࡱࡶࡸࡤ࡯࡮ࡧࡱࠥਞ"): get_host_info()
                  }
              }
              bstack11l1111ll1_opy_ = bstack1llll1ll_opy_(cli.config, [bstack11ll111_opy_ (u"ࠣࡣࡳ࡭ࡸࠨਟ"), bstack11ll111_opy_ (u"ࠤࡨࡨࡸࡏ࡮ࡴࡶࡵࡹࡲ࡫࡮ࡵࡣࡷ࡭ࡴࡴࠢਠ"), bstack11ll111_opy_ (u"ࠥࡥࡵ࡯ࠢਡ")], bstack1lllll11l1_opy_)
              response = bstack1l1l11ll_opy_(bstack11ll111_opy_ (u"ࠦࡕࡕࡓࡕࠤਢ"), bstack11l1111ll1_opy_, payload, config)
              if response.status_code >= 200 and response.status_code < 300:
                  logger.info(bstack11ll111_opy_ (u"ࠧࡑࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵࠣࡷࡪࡴࡴࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡵࡱࠣࡿࢂࠨਣ").format(bstack1lllll11l1_opy_))
              else:
                  logger.debug(bstack11ll111_opy_ (u"ࠨࡋࡦࡻࠣࡱࡪࡺࡲࡪࡥࡶࠤࡷ࡫ࡱࡶࡧࡶࡸࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪࠣࡷࡹࡧࡴࡶࡵࠣࡿࢂࠨਤ").format(response.status_code))
          except Exception as e:
              logger.debug(bstack11ll111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡴࡤࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࡀࠠࡼࡿࠥਥ").format(e))
      bstack11ll11111_opy_()
  except Exception as e:
      logger.debug(bstack11ll111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡴࡤࡠ࡭ࡨࡽࡤࡳࡥࡵࡴ࡬ࡧࡸࡀࠠࡼࡿࠥਦ").format(e))
def bstack1l11l11lll_opy_():
  bstack1lll1l111_opy_ = bstack11ll111_opy_ (u"ࠤࠥਧ")
  global bstack111l11111_opy_
  global bstack1llllllll1_opy_
  global bstack1l111l1ll1_opy_
  global bstack1lll1l1l11_opy_
  global ROBOT_PYTHON_ERRORS
  global bstack1l11lll1_opy_
  global CONFIG
  bstack1llll1l11_opy_ = os.environ.get(bstack11ll111_opy_ (u"ࠪࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡕࡔࡇࡇࠫਨ"))
  if bstack1llll1l11_opy_ not in [bstack11ll111_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ਩")]:
    bstack1lll1l111_opy_ = bstack1111l1l1l_opy_.bstack1ll111l11_opy_(EVENTS.bstack11llllll11_opy_)
  percy.shutdown()
  if bstack111l11111_opy_:
    logger.warning(bstack11l1l1ll1l_opy_.format(str(bstack111l11111_opy_)))
  else:
    try:
      bstack111llll1ll_opy_ = bstack11lll1l111_opy_(bstack11ll111_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫਪ"), logger)
      if bstack111llll1ll_opy_.get(bstack11ll111_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫਫ")) and bstack111llll1ll_opy_.get(bstack11ll111_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬਬ")).get(bstack11ll111_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪਭ")):
        logger.warning(bstack11l1l1ll1l_opy_.format(str(bstack111llll1ll_opy_[bstack11ll111_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧਮ")][bstack11ll111_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬਯ")])))
    except Exception as e:
      logger.error(e)
  if cli.is_running() and bstack1llll1l11_opy_ not in [bstack11ll111_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬਰ")]:
    bstack111l1llll1_opy_.invoke(bstack1l11lll1ll_opy_.bstack1lllllll1_opy_)
  logger.info(bstack11llllll1l_opy_)
  global bstack11l1lllll1_opy_
  if bstack11l1lllll1_opy_:
    bstack11l1lll11_opy_()
  try:
    with bstack1lll11ll_opy_:
      bstack1ll1l11l1_opy_ = bstack1llllllll1_opy_.copy()
    for driver in bstack1ll1l11l1_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1l111ll111_opy_)
  ROBOT_PYTHON_ERRORS = []
  if bstack1l11lll1_opy_ == bstack11ll111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ਱"):
    ROBOT_PYTHON_ERRORS = bstack1l1lll111_opy_(bstack11ll111_opy_ (u"࠭ࡲࡰࡤࡲࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧਲ"))
  if bstack1l11lll1_opy_ == bstack11ll111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧਲ਼") and len(bstack1lll1l1l11_opy_) == 0:
    bstack1lll1l1l11_opy_ = bstack1l1lll111_opy_(bstack11ll111_opy_ (u"ࠨࡲࡺࡣࡵࡿࡴࡦࡵࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭਴"))
    if len(bstack1lll1l1l11_opy_) == 0:
      bstack1lll1l1l11_opy_ = bstack1l1lll111_opy_(bstack11ll111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡳࡴࡵࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨਵ"))
  bstack11l1l111_opy_ = bstack11ll111_opy_ (u"ࠪࠫਸ਼")
  if len(bstack1l111l1ll1_opy_) > 0:
    bstack11l1l111_opy_ = bstack1lllll1lll_opy_(bstack1l111l1ll1_opy_)
  elif len(bstack1lll1l1l11_opy_) > 0:
    bstack11l1l111_opy_ = bstack1lllll1lll_opy_(bstack1lll1l1l11_opy_)
  elif len(ROBOT_PYTHON_ERRORS) > 0:
    bstack11l1l111_opy_ = bstack1lllll1lll_opy_(ROBOT_PYTHON_ERRORS)
  elif len(bstack11l1ll111_opy_) > 0:
    bstack11l1l111_opy_ = bstack1lllll1lll_opy_(bstack11l1ll111_opy_)
  if bstack1llll1l11_opy_ not in [bstack11ll111_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ਷")]:
    def bstack1l1lll11l_opy_():
      try:
        if bstack1llll1l11_opy_ in [bstack11ll111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫਸ"), bstack11ll111_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬਹ")]:
          bstack111l1l1111_opy_()
      except Exception as e:
        logger.debug(bstack11ll111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩ࡭ࡳࡧ࡬ࡠࡧࡻࡩࡨࡻࡴࡪࡱࡱ࠾ࠥࢁࡽࠣ਺").format(e))
    def bstack1ll1l1llll_opy_():
      try:
        if bool(bstack11l1l111_opy_):
          bstack1l1l111l1l_opy_(bstack11l1l111_opy_)
        else:
          bstack1l1l111l1l_opy_()
      except Exception as e:
        logger.debug(bstack11ll111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡴࡧࡱࡨ࡮ࡴࡧࠡࡧࡹࡩࡳࡺ࠺ࠡࡽࢀࠦ਻").format(e))
    def bstack1l1lll1l1_opy_():
      try:
        logger_utils.bstack1ll11l1ll_opy_(CONFIG)
      except Exception as e:
        logger.debug(bstack11ll111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡵࡨࡲࡩ࡯࡮ࡨࠢ࡯ࡳ࡬ࡹ࠺ࠡࡽࢀ਼ࠦ").format(e))
    bstack1111l11l_opy_ = threading.Thread(target=bstack1l1lll11l_opy_)
    bstack11l11lll1_opy_ = threading.Thread(target=bstack1ll1l1llll_opy_)
    bstack1l1l1l1lll_opy_ = threading.Thread(target=bstack1l1lll1l1_opy_)
    threads = [bstack1111l11l_opy_, bstack11l11lll1_opy_, bstack1l1l1l1lll_opy_]
    for thread in threads:
      try:
        thread.start()
      except Exception as e:
        logger.debug(bstack11ll111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡶࡸࡦࡸࡴࡪࡰࡪࠤࡹ࡮ࡲࡦࡣࡧࠤࢀࢃ࠺ࠡࡽࢀࠦ਽").format(thread.name, e))
    for thread in threads:
      try:
        thread.join()
      except Exception as e:
        logger.debug(bstack11ll111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡮ࡴ࡯࡮ࡪࡰࡪࠤࡹ࡮ࡲࡦࡣࡧࠤࢀࢃ࠺ࠡࡽࢀࠦਾ").format(thread.name, e))
    bstack11ll1111_opy_(bstack11ll1l1l1l_opy_, logger)
    bstack11ll1111_opy_(os.path.join(os.getcwd(), bstack11ll111_opy_ (u"ࠬࡲ࡯ࡨࠩਿ"), bstack11ll111_opy_ (u"࠭࡫ࡦࡻ࠰ࡱࡪࡺࡲࡪࡥࡶ࠲࡯ࡹ࡯࡯ࠩੀ")), logger)
  if bstack1llll1l11_opy_ not in [bstack11ll111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨੁ")]:
    bstack1111l1l1l_opy_.end(EVENTS.bstack11llllll11_opy_.value, bstack1lll1l111_opy_ + bstack11ll111_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣੂ"), bstack1lll1l111_opy_ + bstack11ll111_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ੃"), status=True, failure=None, test_name=None)
    bstack111l1l1ll1_opy_()
    logger_utils.bstack11l1l111l_opy_()
    logging.shutdown()
  if len(ROBOT_PYTHON_ERRORS) > 0:
    sys.exit(len(ROBOT_PYTHON_ERRORS))
def bstack11l1l11111_opy_(bstack1ll1l1lll_opy_, frame):
  global global_config
  logger.error(bstack1l11l111ll_opy_)
  global_config.bstack111lll11ll_opy_(bstack11ll111_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡒࡴ࠭੄"), bstack1ll1l1lll_opy_)
  if hasattr(signal, bstack11ll111_opy_ (u"ࠫࡘ࡯ࡧ࡯ࡣ࡯ࡷࠬ੅")):
    global_config.bstack111lll11ll_opy_(bstack11ll111_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬ੆"), signal.Signals(bstack1ll1l1lll_opy_).name)
  else:
    global_config.bstack111lll11ll_opy_(bstack11ll111_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭ੇ"), bstack11ll111_opy_ (u"ࠧࡔࡋࡊ࡙ࡓࡑࡎࡐ࡙ࡑࠫੈ"))
  if cli.is_running():
    bstack111l1llll1_opy_.invoke(bstack1l11lll1ll_opy_.bstack1lllllll1_opy_)
  bstack1llll1l11_opy_ = os.environ.get(bstack11ll111_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩ੉"))
  if bstack1llll1l11_opy_ == bstack11ll111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ੊") and not cli.is_enabled(CONFIG):
    TestHubHandler.stop(global_config.get_property(bstack11ll111_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪੋ")))
  bstack1l11l11lll_opy_()
  sys.exit(1)
def bstack1l1ll11111_opy_(err):
  logger.critical(bstack1ll11ll11l_opy_.format(str(err)))
  bstack1l1l111l1l_opy_(bstack1ll11ll11l_opy_.format(str(err)), True)
  atexit.unregister(bstack1l11l11lll_opy_)
  bstack111l1l1111_opy_()
  sys.exit(1)
def bstack11l11ll11l_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1l1l111l1l_opy_(message, True)
  atexit.unregister(bstack1l11l11lll_opy_)
  bstack111l1l1111_opy_()
  sys.exit(1)
def bstack1l1111l1l1_opy_():
  global CONFIG
  global bstack11l111ll11_opy_
  global bstack1lll1l11ll_opy_
  global bstack11ll11l11l_opy_
  CONFIG = bstack1ll1l11ll1_opy_()
  load_dotenv(CONFIG.get(bstack11ll111_opy_ (u"ࠫࡪࡴࡶࡇ࡫࡯ࡩࠬੌ")))
  bstack111l111l1l_opy_()
  bstack1l1llllll1_opy_()
  CONFIG = bstack1l1l11ll1_opy_(CONFIG)
  update(CONFIG, bstack1lll1l11ll_opy_)
  update(CONFIG, bstack11l111ll11_opy_)
  if not cli.is_enabled(CONFIG):
    CONFIG = bstack11l1l1111_opy_(CONFIG)
  bstack11ll11l11l_opy_ = bstack11l1llllll_opy_(CONFIG)
  os.environ[bstack11ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ੍")] = bstack11ll11l11l_opy_.__str__().lower()
  global_config.bstack111lll11ll_opy_(bstack11ll111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ੎"), bstack11ll11l11l_opy_)
  if (bstack11ll111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ੏") in CONFIG and bstack11ll111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ੐") in bstack11l111ll11_opy_) or (
          bstack11ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬੑ") in CONFIG and bstack11ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭੒") not in bstack1lll1l11ll_opy_):
    if os.getenv(bstack11ll111_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨ੓")):
      CONFIG[bstack11ll111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ੔")] = os.getenv(bstack11ll111_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪ੕"))
    else:
      if not CONFIG.get(bstack11ll111_opy_ (u"ࠢࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠥ੖"), bstack11ll111_opy_ (u"ࠣࠤ੗")) in bstack11ll11l11_opy_:
        bstack111ll11l1_opy_()
  elif (bstack11ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ੘") not in CONFIG and bstack11ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬਖ਼") in CONFIG) or (
          bstack11ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧਗ਼") in bstack1lll1l11ll_opy_ and bstack11ll111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨਜ਼") not in bstack11l111ll11_opy_):
    del (CONFIG[bstack11ll111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨੜ")])
  if bstack11l11111_opy_(CONFIG):
    bstack1l1ll11111_opy_(bstack111l11l1_opy_)
  Config.get_instance().bstack111lll11ll_opy_(bstack11ll111_opy_ (u"ࠢࡶࡵࡨࡶࡓࡧ࡭ࡦࠤ੝"), CONFIG[bstack11ll111_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪਫ਼")])
  bstack111l111ll1_opy_()
  bstack111lll1l1l_opy_()
  if bstack1llll11l1_opy_ and not CONFIG.get(bstack11ll111_opy_ (u"ࠤࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠧ੟"), bstack11ll111_opy_ (u"ࠥࠦ੠")) in bstack11ll11l11_opy_:
    CONFIG[bstack11ll111_opy_ (u"ࠫࡦࡶࡰࠨ੡")] = bstack1l11l11l1_opy_(CONFIG)
    logger.info(bstack11l1l111ll_opy_.format(CONFIG[bstack11ll111_opy_ (u"ࠬࡧࡰࡱࠩ੢")]))
  if not bstack11ll11l11l_opy_:
    CONFIG[bstack11ll111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ੣")] = [{}]
def bstack11lll1llll_opy_(config, bstack1l1111l11_opy_):
  global CONFIG
  global bstack1llll11l1_opy_
  CONFIG = config
  bstack1llll11l1_opy_ = bstack1l1111l11_opy_
def bstack111lll1l1l_opy_():
  global CONFIG
  global bstack1llll11l1_opy_
  if bstack11ll111_opy_ (u"ࠧࡢࡲࡳࠫ੤") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack11l11ll11l_opy_(e, bstack111ll1l1_opy_)
    bstack1llll11l1_opy_ = True
    global_config.bstack111lll11ll_opy_(bstack11ll111_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ੥"), True)
def bstack1l11l11l1_opy_(config):
  bstack1llll1l1ll_opy_ = bstack11ll111_opy_ (u"ࠩࠪ੦")
  app = config[bstack11ll111_opy_ (u"ࠪࡥࡵࡶࠧ੧")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1l111ll1ll_opy_:
      if os.path.exists(app):
        bstack1llll1l1ll_opy_ = bstack11l111111_opy_(config, app)
      elif bstack111ll1lll1_opy_(app):
        bstack1llll1l1ll_opy_ = app
      else:
        bstack1l1ll11111_opy_(bstack1111l1l1_opy_.format(app))
    else:
      if bstack111ll1lll1_opy_(app):
        bstack1llll1l1ll_opy_ = app
      elif os.path.exists(app):
        bstack1llll1l1ll_opy_ = bstack11l111111_opy_(app)
      else:
        bstack1l1ll11111_opy_(bstack1lll1l1l1_opy_)
  else:
    if len(app) > 2:
      bstack1l1ll11111_opy_(bstack1ll1l11ll_opy_)
    elif len(app) == 2:
      if bstack11ll111_opy_ (u"ࠫࡵࡧࡴࡩࠩ੨") in app and bstack11ll111_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨ੩") in app:
        if os.path.exists(app[bstack11ll111_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ੪")]):
          bstack1llll1l1ll_opy_ = bstack11l111111_opy_(config, app[bstack11ll111_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ੫")], app[bstack11ll111_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫ੬")])
        else:
          bstack1l1ll11111_opy_(bstack1111l1l1_opy_.format(app))
      else:
        bstack1l1ll11111_opy_(bstack1ll1l11ll_opy_)
    else:
      for key in app:
        if key in bstack1l11l1l11l_opy_:
          if key == bstack11ll111_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ੭"):
            if os.path.exists(app[key]):
              bstack1llll1l1ll_opy_ = bstack11l111111_opy_(config, app[key])
            else:
              bstack1l1ll11111_opy_(bstack1111l1l1_opy_.format(app))
          else:
            bstack1llll1l1ll_opy_ = app[key]
        else:
          bstack1l1ll11111_opy_(bstack11l111111l_opy_)
  return bstack1llll1l1ll_opy_
def bstack111ll1lll1_opy_(bstack1llll1l1ll_opy_):
  import re
  bstack1ll1111lll_opy_ = re.compile(bstack11ll111_opy_ (u"ࡵࠦࡣࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫࠦࠥ੮"))
  bstack11l111ll1l_opy_ = re.compile(bstack11ll111_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬ࠲࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰ࠤࠣ੯"))
  if bstack11ll111_opy_ (u"ࠬࡨࡳ࠻࠱࠲ࠫੰ") in bstack1llll1l1ll_opy_ or re.fullmatch(bstack1ll1111lll_opy_, bstack1llll1l1ll_opy_) or re.fullmatch(bstack11l111ll1l_opy_, bstack1llll1l1ll_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack1ll1l111_opy_, stage=STAGE.bstack1111l1111_opy_, bstack11ll11ll11_opy_=bstack1lll11lll_opy_)
def bstack11l111111_opy_(config, path, bstack1l1l1111l1_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack11ll111_opy_ (u"࠭ࡲࡣࠩੱ")).read()).hexdigest()
  bstack1l111l1l_opy_ = bstack11l1l1ll11_opy_(md5_hash)
  bstack1llll1l1ll_opy_ = None
  if bstack1l111l1l_opy_:
    logger.info(bstack1lllll111_opy_.format(bstack1l111l1l_opy_, md5_hash))
    return bstack1l111l1l_opy_
  bstack11lll11111_opy_ = datetime.datetime.now()
  bstack11l1111l11_opy_ = MultipartEncoder(
    fields={
      bstack11ll111_opy_ (u"ࠧࡧ࡫࡯ࡩࠬੲ"): (os.path.basename(path), open(os.path.abspath(path), bstack11ll111_opy_ (u"ࠨࡴࡥࠫੳ")), bstack11ll111_opy_ (u"ࠩࡷࡩࡽࡺ࠯ࡱ࡮ࡤ࡭ࡳ࠭ੴ")),
      bstack11ll111_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ੵ"): bstack1l1l1111l1_opy_
    }
  )
  response = requests.post(bstack1ll1ll1l1_opy_, data=bstack11l1111l11_opy_,
                           headers={bstack11ll111_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪ੶"): bstack11l1111l11_opy_.content_type},
                           auth=(config[bstack11ll111_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ੷")], config[bstack11ll111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ੸")]))
  try:
    res = json.loads(response.text)
    bstack1llll1l1ll_opy_ = res[bstack11ll111_opy_ (u"ࠧࡢࡲࡳࡣࡺࡸ࡬ࠨ੹")]
    logger.info(bstack1l1l1ll1l1_opy_.format(bstack1llll1l1ll_opy_))
    bstack111l1ll11_opy_(md5_hash, bstack1llll1l1ll_opy_)
    cli.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠣࡪࡷࡸࡵࡀࡵࡱ࡮ࡲࡥࡩࡥࡡࡱࡲࠥ੺"), datetime.datetime.now() - bstack11lll11111_opy_)
  except ValueError as err:
    bstack1l1ll11111_opy_(bstack1l111l1l11_opy_.format(str(err)))
  return bstack1llll1l1ll_opy_
def bstack111l111ll1_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack1ll111ll1l_opy_
  bstack111l1ll1ll_opy_ = 1
  bstack1l11l1l1l_opy_ = 1
  if bstack11ll111_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ੻") in CONFIG:
    bstack1l11l1l1l_opy_ = CONFIG[bstack11ll111_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ੼")]
  else:
    bstack1l11l1l1l_opy_ = bstack1l1lll1ll1_opy_(framework_name, args) or 1
  if bstack11ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ੽") in CONFIG:
    bstack111l1ll1ll_opy_ = len(CONFIG[bstack11ll111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ੾")])
  bstack1ll111ll1l_opy_ = int(bstack1l11l1l1l_opy_) * int(bstack111l1ll1ll_opy_)
def bstack1l1lll1ll1_opy_(framework_name, args):
  if framework_name == bstack1ll1ll11l_opy_ and args and bstack11ll111_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ੿") in args:
      bstack1l1l1111l_opy_ = args.index(bstack11ll111_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ઀"))
      return int(args[bstack1l1l1111l_opy_ + 1]) or 1
  return 1
def bstack11l1l1ll11_opy_(md5_hash):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack11ll111_opy_ (u"ࠨࡨ࡬ࡰࡪࡲ࡯ࡤ࡭ࠣࡲࡴࡺࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧ࠯ࠤࡺࡹࡩ࡯ࡩࠣࡦࡦࡹࡩࡤࠢࡩ࡭ࡱ࡫ࠠࡰࡲࡨࡶࡦࡺࡩࡰࡰࡶࠫઁ"))
    bstack1lll1lll11_opy_ = os.path.join(os.path.expanduser(bstack11ll111_opy_ (u"ࠩࢁࠫં")), bstack11ll111_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪઃ"), bstack11ll111_opy_ (u"ࠫࡦࡶࡰࡖࡲ࡯ࡳࡦࡪࡍࡅ࠷ࡋࡥࡸ࡮࠮࡫ࡵࡲࡲࠬ઄"))
    if os.path.exists(bstack1lll1lll11_opy_):
      try:
        bstack1ll111l11l_opy_ = json.load(open(bstack1lll1lll11_opy_, bstack11ll111_opy_ (u"ࠬࡸࡢࠨઅ")))
        if md5_hash in bstack1ll111l11l_opy_:
          bstack11111l1l1_opy_ = bstack1ll111l11l_opy_[md5_hash]
          bstack11lll111_opy_ = datetime.datetime.now()
          bstack1l1l1l111l_opy_ = datetime.datetime.strptime(bstack11111l1l1_opy_[bstack11ll111_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩઆ")], bstack11ll111_opy_ (u"ࠧࠦࡦ࠲ࠩࡲ࠵࡚ࠥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫઇ"))
          if (bstack11lll111_opy_ - bstack1l1l1l111l_opy_).days > 30:
            return None
          elif version.parse(str(__version__)) > version.parse(bstack11111l1l1_opy_[bstack11ll111_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ઈ")]):
            return None
          return bstack11111l1l1_opy_[bstack11ll111_opy_ (u"ࠩ࡬ࡨࠬઉ")]
      except Exception as e:
        logger.debug(bstack11ll111_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡵࡩࡦࡪࡩ࡯ࡩࠣࡑࡉ࠻ࠠࡩࡣࡶ࡬ࠥ࡬ࡩ࡭ࡧ࠽ࠤࢀࢃࠧઊ").format(str(e)))
    return None
  bstack1lll1lll11_opy_ = os.path.join(os.path.expanduser(bstack11ll111_opy_ (u"ࠫࢃ࠭ઋ")), bstack11ll111_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬઌ"), bstack11ll111_opy_ (u"࠭ࡡࡱࡲࡘࡴࡱࡵࡡࡥࡏࡇ࠹ࡍࡧࡳࡩ࠰࡭ࡷࡴࡴࠧઍ"))
  lock_file = bstack1lll1lll11_opy_ + bstack11ll111_opy_ (u"ࠧ࠯࡮ࡲࡧࡰ࠭઎")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack1lll1lll11_opy_):
        with open(bstack1lll1lll11_opy_, bstack11ll111_opy_ (u"ࠨࡴࠪએ")) as f:
          content = f.read().strip()
          if content:
            bstack1ll111l11l_opy_ = json.loads(content)
            if md5_hash in bstack1ll111l11l_opy_:
              bstack11111l1l1_opy_ = bstack1ll111l11l_opy_[md5_hash]
              bstack11lll111_opy_ = datetime.datetime.now()
              bstack1l1l1l111l_opy_ = datetime.datetime.strptime(bstack11111l1l1_opy_[bstack11ll111_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬઐ")], bstack11ll111_opy_ (u"ࠪࠩࡩ࠵ࠥ࡮࠱ࠨ࡝ࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧઑ"))
              if (bstack11lll111_opy_ - bstack1l1l1l111l_opy_).days > 30:
                return None
              elif version.parse(str(__version__)) > version.parse(bstack11111l1l1_opy_[bstack11ll111_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ઒")]):
                return None
              return bstack11111l1l1_opy_[bstack11ll111_opy_ (u"ࠬ࡯ࡤࠨઓ")]
      return None
  except Exception as e:
    logger.debug(bstack11ll111_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡽࡩࡵࡪࠣࡪ࡮ࡲࡥࠡ࡮ࡲࡧࡰ࡯࡮ࡨࠢࡩࡳࡷࠦࡍࡅ࠷ࠣ࡬ࡦࡹࡨ࠻ࠢࡾࢁࠬઔ").format(str(e)))
    return None
def bstack111l1ll11_opy_(md5_hash, bstack1llll1l1ll_opy_):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack11ll111_opy_ (u"ࠧࡧ࡫࡯ࡩࡱࡵࡣ࡬ࠢࡱࡳࡹࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦ࠮ࠣࡹࡸ࡯࡮ࡨࠢࡥࡥࡸ࡯ࡣࠡࡨ࡬ࡰࡪࠦ࡯ࡱࡧࡵࡥࡹ࡯࡯࡯ࡵࠪક"))
    bstack11l111l11l_opy_ = os.path.join(os.path.expanduser(bstack11ll111_opy_ (u"ࠨࢀࠪખ")), bstack11ll111_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩગ"))
    if not os.path.exists(bstack11l111l11l_opy_):
      os.makedirs(bstack11l111l11l_opy_)
    bstack1lll1lll11_opy_ = os.path.join(os.path.expanduser(bstack11ll111_opy_ (u"ࠪࢂࠬઘ")), bstack11ll111_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫઙ"), bstack11ll111_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭ચ"))
    bstack11ll1l1lll_opy_ = {
      bstack11ll111_opy_ (u"࠭ࡩࡥࠩછ"): bstack1llll1l1ll_opy_,
      bstack11ll111_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪજ"): datetime.datetime.strftime(datetime.datetime.now(), bstack11ll111_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬઝ")),
      bstack11ll111_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧઞ"): str(__version__)
    }
    try:
      bstack1ll111l11l_opy_ = {}
      if os.path.exists(bstack1lll1lll11_opy_):
        bstack1ll111l11l_opy_ = json.load(open(bstack1lll1lll11_opy_, bstack11ll111_opy_ (u"ࠪࡶࡧ࠭ટ")))
      bstack1ll111l11l_opy_[md5_hash] = bstack11ll1l1lll_opy_
      with open(bstack1lll1lll11_opy_, bstack11ll111_opy_ (u"ࠦࡼ࠱ࠢઠ")) as outfile:
        json.dump(bstack1ll111l11l_opy_, outfile)
    except Exception as e:
      logger.debug(bstack11ll111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡺࡶࡤࡢࡶ࡬ࡲ࡬ࠦࡍࡅ࠷ࠣ࡬ࡦࡹࡨࠡࡨ࡬ࡰࡪࡀࠠࡼࡿࠪડ").format(str(e)))
    return
  bstack11l111l11l_opy_ = os.path.join(os.path.expanduser(bstack11ll111_opy_ (u"࠭ࡾࠨઢ")), bstack11ll111_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧણ"))
  if not os.path.exists(bstack11l111l11l_opy_):
    os.makedirs(bstack11l111l11l_opy_)
  bstack1lll1lll11_opy_ = os.path.join(os.path.expanduser(bstack11ll111_opy_ (u"ࠨࢀࠪત")), bstack11ll111_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩથ"), bstack11ll111_opy_ (u"ࠪࡥࡵࡶࡕࡱ࡮ࡲࡥࡩࡓࡄ࠶ࡊࡤࡷ࡭࠴ࡪࡴࡱࡱࠫદ"))
  lock_file = bstack1lll1lll11_opy_ + bstack11ll111_opy_ (u"ࠫ࠳ࡲ࡯ࡤ࡭ࠪધ")
  bstack11ll1l1lll_opy_ = {
    bstack11ll111_opy_ (u"ࠬ࡯ࡤࠨન"): bstack1llll1l1ll_opy_,
    bstack11ll111_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ઩"): datetime.datetime.strftime(datetime.datetime.now(), bstack11ll111_opy_ (u"ࠧࠦࡦ࠲ࠩࡲ࠵࡚ࠥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫપ")),
    bstack11ll111_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ફ"): str(__version__)
  }
  try:
    with FileLock(lock_file, timeout=10):
      bstack1ll111l11l_opy_ = {}
      if os.path.exists(bstack1lll1lll11_opy_):
        with open(bstack1lll1lll11_opy_, bstack11ll111_opy_ (u"ࠩࡵࠫબ")) as f:
          content = f.read().strip()
          if content:
            bstack1ll111l11l_opy_ = json.loads(content)
      bstack1ll111l11l_opy_[md5_hash] = bstack11ll1l1lll_opy_
      with open(bstack1lll1lll11_opy_, bstack11ll111_opy_ (u"ࠥࡻࠧભ")) as outfile:
        json.dump(bstack1ll111l11l_opy_, outfile)
  except Exception as e:
    logger.debug(bstack11ll111_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡻ࡮ࡺࡨࠡࡨ࡬ࡰࡪࠦ࡬ࡰࡥ࡮࡭ࡳ࡭ࠠࡧࡱࡵࠤࡒࡊ࠵ࠡࡪࡤࡷ࡭ࠦࡵࡱࡦࡤࡸࡪࡀࠠࡼࡿࠪમ").format(str(e)))
def bstack1l1l1l11l1_opy_(self):
  return
def bstack1llllllll_opy_(self):
  return
def bstack1ll1l1111l_opy_():
  global bstack1l11ll11ll_opy_
  bstack1l11ll11ll_opy_ = True
def bstack11llll1l_opy_(self):
  global bstack111l11111l_opy_
  global bstack1lll1l1l_opy_
  global bstack1llll1llll_opy_
  bstack11llllllll_opy_ = bstack1111l1l1l_opy_.bstack1ll111l11_opy_(EVENTS.bstack1l11lll11l_opy_)
  try:
    if bstack11ll111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬય") in bstack111l11111l_opy_ and self.session_id != None and bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪર"), bstack11ll111_opy_ (u"ࠧࠨ઱")) != bstack11ll111_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩલ"):
      bstack1lll1ll11_opy_ = bstack11ll111_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩળ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11ll111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ઴")
      if bstack1lll1ll11_opy_ == bstack11ll111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫવ"):
        bstack11ll1l11ll_opy_(logger)
      if self != None:
        bstack1l11l1ll11_opy_(self, bstack1lll1ll11_opy_, bstack11ll111_opy_ (u"ࠬ࠲ࠠࠨશ").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack11ll111_opy_ (u"࠭ࠧષ")
    if bstack11ll111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧસ") in bstack111l11111l_opy_ and getattr(threading.current_thread(), bstack11ll111_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧહ"), None):
      bstack1l1l111l11_opy_.bstack1ll11llll_opy_(self, bstack1ll11111l1_opy_, logger, wait=True)
    if bstack11ll111_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ઺") in bstack111l11111l_opy_:
      bstack1l11l11l1l_opy_.bstack1l1llll1_opy_(self)
    bstack1111l1l1l_opy_.end(EVENTS.bstack1l11lll11l_opy_.value, bstack11llllllll_opy_ + bstack11ll111_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ઻"), bstack11llllllll_opy_ + bstack11ll111_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ઼"), status=True, failure=None, test_name=None)
  except Exception as e:
    logger.debug(bstack11ll111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࠨઽ") + str(e))
    bstack1111l1l1l_opy_.end(EVENTS.bstack1l11lll11l_opy_.value, bstack11llllllll_opy_ + bstack11ll111_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨા"), bstack11llllllll_opy_ + bstack11ll111_opy_ (u"ࠢ࠻ࡧࡱࡨࠧિ"), status=False, failure=str(e), test_name=None)
  bstack1llll1llll_opy_(self)
  self.session_id = None
def bstack11ll111ll_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack111ll11l11_opy_
    global bstack111l11111l_opy_
    command_executor = kwargs.get(bstack11ll111_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠫી"), bstack11ll111_opy_ (u"ࠩࠪુ"))
    bstack1ll1llll1_opy_ = False
    if type(command_executor) == str and bstack11ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ૂ") in command_executor:
      bstack1ll1llll1_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧૃ") in str(getattr(command_executor, bstack11ll111_opy_ (u"ࠬࡥࡵࡳ࡮ࠪૄ"), bstack11ll111_opy_ (u"࠭ࠧૅ"))):
      bstack1ll1llll1_opy_ = True
    else:
      kwargs = bstack11l11l11ll_opy_.bstack1l111ll11_opy_(bstack11111lll1_opy_=kwargs, config=CONFIG)
      return bstack11lll1ll_opy_(self, *args, **kwargs)
    if bstack1ll1llll1_opy_:
      bstack1l11l1l1ll_opy_ = bstack111llll11l_opy_.bstack1l1ll1lll_opy_(CONFIG, bstack111l11111l_opy_)
      if kwargs.get(bstack11ll111_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ૆")):
        kwargs[bstack11ll111_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩે")] = bstack111ll11l11_opy_(kwargs[bstack11ll111_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪૈ")], bstack111l11111l_opy_, CONFIG, bstack1l11l1l1ll_opy_)
      elif kwargs.get(bstack11ll111_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪૉ")):
        kwargs[bstack11ll111_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ૊")] = bstack111ll11l11_opy_(kwargs[bstack11ll111_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬો")], bstack111l11111l_opy_, CONFIG, bstack1l11l1l1ll_opy_)
  except Exception as e:
    logger.error(bstack11ll111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡦࡰࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡔࡆࡎࠤࡨࡧࡰࡴ࠼ࠣࡿࢂࠨૌ").format(str(e)))
  return bstack11lll1ll_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack1llll11l11_opy_, stage=STAGE.bstack1111l1111_opy_, bstack11ll11ll11_opy_=bstack1lll11lll_opy_)
def bstack1ll1lll111_opy_(self, command_executor=bstack11ll111_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯࠲࠴࠺࠲࠵࠴࠰࠯࠳࠽࠸࠹࠺࠴્ࠣ"), *args, **kwargs):
  global bstack1lll1l1l_opy_
  global bstack1llllllll1_opy_
  bstack1l111lll1_opy_ = bstack11ll111ll_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack11lll1ll1_opy_.on():
    return bstack1l111lll1_opy_
  try:
    logger.debug(bstack11ll111_opy_ (u"ࠨࡅࡲࡱࡲࡧ࡮ࡥࠢࡈࡼࡪࡩࡵࡵࡱࡵࠤࡼ࡮ࡥ࡯ࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥ࡯ࡳࠡࡨࡤࡰࡸ࡫ࠠ࠮ࠢࡾࢁࠬ૎").format(str(command_executor)))
    logger.debug(bstack11ll111_opy_ (u"ࠩࡋࡹࡧࠦࡕࡓࡎࠣ࡭ࡸࠦ࠭ࠡࡽࢀࠫ૏").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack11ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ૐ") in command_executor._url:
      global_config.bstack111lll11ll_opy_(bstack11ll111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬ૑"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨ૒") in command_executor):
    global_config.bstack111lll11ll_opy_(bstack11ll111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ૓"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1llll11l_opy_ = getattr(threading.current_thread(), bstack11ll111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡔࡦࡵࡷࡑࡪࡺࡡࠨ૔"), None)
  bstack1l11l11ll_opy_ = {}
  if self.capabilities is not None:
    bstack1l11l11ll_opy_[bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧ૕")] = self.capabilities.get(bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ૖"))
    bstack1l11l11ll_opy_[bstack11ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ૗")] = self.capabilities.get(bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ૘"))
    bstack1l11l11ll_opy_[bstack11ll111_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡤࡵࡰࡵ࡫ࡲࡲࡸ࠭૙")] = self.capabilities.get(bstack11ll111_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ૚"))
  if CONFIG.get(bstack11ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ૛"), False) and bstack11l11l11ll_opy_.bstack11ll1llll_opy_(bstack1l11l11ll_opy_):
    threading.current_thread().a11yPlatform = True
  if bstack11ll111_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ૜") in bstack111l11111l_opy_ or bstack11ll111_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ૝") in bstack111l11111l_opy_:
    TestHubHandler.bstack1l1ll1l11_opy_(self)
  if bstack11ll111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ૞") in bstack111l11111l_opy_ and bstack1llll11l_opy_ and bstack1llll11l_opy_.get(bstack11ll111_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ૟"), bstack11ll111_opy_ (u"ࠬ࠭ૠ")) == bstack11ll111_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧૡ"):
    TestHubHandler.bstack1l1ll1l11_opy_(self)
  bstack1lll1l1l_opy_ = self.session_id
  with bstack1lll11ll_opy_:
    bstack1llllllll1_opy_.append(self)
  return bstack1l111lll1_opy_
def bstack1l1l1ll1ll_opy_(args):
  return bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲࠨૢ") in str(args)
def bstack111l1llll_opy_(self, driver_command, *args, **kwargs):
  global bstack11l1l1l11_opy_
  global bstack1111l11l1_opy_
  bstack1l1111l1ll_opy_ = bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬૣ"), None) and bstack1lll11l111_opy_(
          threading.current_thread(), bstack11ll111_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ૤"), None)
  bstack11lllll1_opy_ = bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ૥"), None) and bstack1lll11l111_opy_(
          threading.current_thread(), bstack11ll111_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭૦"), None)
  bstack11ll11l1l1_opy_ = getattr(self, bstack11ll111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬ૧"), None) != None and getattr(self, bstack11ll111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭૨"), None) == True
  if not bstack1111l11l1_opy_ and bstack11ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ૩") in CONFIG and CONFIG[bstack11ll111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ૪")] == True and bstack11ll11llll_opy_.bstack111l1111l1_opy_(driver_command) and (bstack11ll11l1l1_opy_ or bstack1l1111l1ll_opy_ or bstack11lllll1_opy_) and not bstack1l1l1ll1ll_opy_(args):
    try:
      bstack1111l11l1_opy_ = True
      logger.debug(bstack11ll111_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡽࢀࠫ૫").format(driver_command))
      bstack1ll111lll_opy_ = perform_scan(self, driver_command=driver_command)
      logger.debug(bstack1ll111lll_opy_)
      try:
        bstack1l11l111l1_opy_ = {
          bstack11ll111_opy_ (u"ࠥࡶࡪࡷࡵࡦࡵࡷࠦ૬"): {
            bstack11ll111_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࠧ૭"): bstack11ll111_opy_ (u"ࠧࡇ࠱࠲࡛ࡢࡗࡈࡇࡎࠣ૮"),
            bstack11ll111_opy_ (u"ࠨࡰࡢࡴࡤࡱࡪࡺࡥࡳࡵࠥ૯"): [
              {
                bstack11ll111_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢ૰"): driver_command
              }
            ]
          },
          bstack11ll111_opy_ (u"ࠣࡴࡨࡷࡵࡵ࡮ࡴࡧࠥ૱"): {
            bstack11ll111_opy_ (u"ࠤࡥࡳࡩࡿࠢ૲"): {
              bstack11ll111_opy_ (u"ࠥࡱࡸ࡭ࠢ૳"): bstack1ll111lll_opy_.get(bstack11ll111_opy_ (u"ࠦࡲࡹࡧࠣ૴"), bstack11ll111_opy_ (u"ࠧࠨ૵")) if isinstance(bstack1ll111lll_opy_, dict) else bstack11ll111_opy_ (u"ࠨࠢ૶"),
              bstack11ll111_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳࠣ૷"): bstack1ll111lll_opy_.get(bstack11ll111_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴࠤ૸"), True) if isinstance(bstack1ll111lll_opy_, dict) else True
            }
          }
        }
        logger.debug(bstack11ll111_opy_ (u"ࠩࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡧࡦࡴࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡱࡵࡧࠡࡦࡤࡸࡦࡀࠠࡼࡿࠪૹ").format(bstack1l11l111l1_opy_))
        bstack1l1ll1ll11_opy_.info(json.dumps(bstack1l11l111l1_opy_, separators=(bstack11ll111_opy_ (u"ࠪ࠰ࠬૺ"), bstack11ll111_opy_ (u"ࠫ࠿࠭ૻ"))))
      except Exception as bstack111lll11l1_opy_:
        logger.debug(bstack11ll111_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡮ࡲ࡫ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡣࡢࡰࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠬૼ").format(str(bstack111lll11l1_opy_)))
    except Exception as err:
      logger.debug(bstack11ll111_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡩࡷ࡬࡯ࡳ࡯ࠣࡷࡨࡧ࡮ࠡࡽࢀࠫ૽").format(str(err)))
    bstack1111l11l1_opy_ = False
  response = bstack11l1l1l11_opy_(self, driver_command, *args, **kwargs)
  if (bstack11ll111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭૾") in str(bstack111l11111l_opy_).lower() or bstack11ll111_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ૿") in str(bstack111l11111l_opy_).lower()) and bstack11lll1ll1_opy_.on():
    try:
      if driver_command == bstack11ll111_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭଀"):
        TestHubHandler.bstack1lll11ll1_opy_({
            bstack11ll111_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩଁ"): response[bstack11ll111_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪଂ")],
            bstack11ll111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬଃ"): TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack11lll1ll1_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
def bstack1ll111ll11_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack1lll1l1l_opy_
  global bstack1lll1l11_opy_
  global bstack1lll11lll_opy_
  global bstack11lll11ll_opy_
  global bstack111ll1l11l_opy_
  global bstack111l11111l_opy_
  global bstack11lll1ll_opy_
  global bstack1llllllll1_opy_
  global bstack11ll1ll1_opy_
  global bstack1ll11111l1_opy_
  bstack11llllllll_opy_ = bstack1111l1l1l_opy_.bstack1ll111l11_opy_(EVENTS.bstack11ll111lll_opy_.value)
  if os.getenv(bstack11ll111_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ଄")) is not None and bstack11l11l11ll_opy_.bstack1l1lll11_opy_(CONFIG) is None:
    CONFIG[bstack11ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧଅ")] = True
  CONFIG[bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪଆ")] = str(bstack111l11111l_opy_) + str(__version__)
  bstack111lllllll_opy_ = os.environ[bstack11ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧଇ")]
  bstack1l11l1l1ll_opy_ = bstack111llll11l_opy_.bstack1l1ll1lll_opy_(CONFIG, bstack111l11111l_opy_)
  CONFIG[bstack11ll111_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ଈ")] = bstack111lllllll_opy_
  CONFIG[bstack11ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ଉ")] = bstack1l11l1l1ll_opy_
  if CONFIG.get(bstack11ll111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬଊ"),bstack11ll111_opy_ (u"࠭ࠧଋ")) and bstack11ll111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ଌ") in bstack111l11111l_opy_:
    CONFIG[bstack11ll111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ଍")].pop(bstack11ll111_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ଎"), None)
    CONFIG[bstack11ll111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪଏ")].pop(bstack11ll111_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩଐ"), None)
  command_executor = bstack1l111lll11_opy_()
  logger.debug(bstack11ll1l1l1_opy_.format(command_executor))
  proxy = bstack1llll1111_opy_(CONFIG, proxy)
  bstack1l111l111_opy_ = 0 if bstack1lll1l11_opy_ < 0 else bstack1lll1l11_opy_
  try:
    if bstack11lll11ll_opy_ is True:
      bstack1l111l111_opy_ = int(multiprocessing.current_process().name)
    elif bstack111ll1l11l_opy_ is True:
      bstack1l111l111_opy_ = int(threading.current_thread().name)
  except:
    bstack1l111l111_opy_ = 0
  bstack1l11l11111_opy_ = bstack11l1111l1l_opy_(CONFIG, bstack1l111l111_opy_)
  logger.debug(bstack1ll1l11l1l_opy_.format(str(bstack1l11l11111_opy_)))
  if bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ଑") in CONFIG and bstack11l1lll1_opy_(CONFIG[bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ଒")]):
    bstack1l1111l1l_opy_(bstack1l11l11111_opy_)
  if bstack11l11l11ll_opy_.bstack11l1111ll_opy_(CONFIG, bstack1l111l111_opy_) and bstack11l11l11ll_opy_.bstack1l1lllll1l_opy_(bstack1l11l11111_opy_, options, desired_capabilities, CONFIG):
    threading.current_thread().a11yPlatform = True
    if (cli.accessibility is None or not cli.accessibility.is_enabled()):
      bstack11l11l11ll_opy_.set_capabilities(bstack1l11l11111_opy_, CONFIG)
  if desired_capabilities:
    bstack111lll1lll_opy_ = bstack1l1l11ll1_opy_(desired_capabilities)
    bstack111lll1lll_opy_[bstack11ll111_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧଓ")] = bstack1ll1lll1l1_opy_(CONFIG)
    bstack1lllllll11_opy_ = bstack11l1111l1l_opy_(bstack111lll1lll_opy_)
    if bstack1lllllll11_opy_:
      bstack1l11l11111_opy_ = update(bstack1lllllll11_opy_, bstack1l11l11111_opy_)
    desired_capabilities = None
  if options:
    bstack11l1l11l1l_opy_(options, bstack1l11l11111_opy_)
  if not options:
    options = bstack1ll1ll1ll1_opy_(bstack1l11l11111_opy_)
  try:
    if bstack1ll1lllll1_opy_:
      def _1lll1111_opy_(bstack1ll11ll111_opy_):
        if not isinstance(bstack1ll11ll111_opy_, dict):
          return
        for _1ll1ll11l1_opy_ in list(bstack1ll11ll111_opy_.keys()):
          _1ll11ll11_opy_ = bstack1ll11ll111_opy_[_1ll1ll11l1_opy_]
          if _1ll11ll11_opy_ is None:
            bstack1ll11ll111_opy_.pop(_1ll1ll11l1_opy_, None)
          elif isinstance(_1ll11ll11_opy_, dict):
            _1lll1111_opy_(_1ll11ll11_opy_)
      _1lll1111_opy_(bstack1l11l11111_opy_)
      _1lll1111_opy_(desired_capabilities)
      if options is not None and hasattr(options, bstack11ll111_opy_ (u"ࠨࡡࡦࡥࡵࡹࠧଔ")):
        _1lll1111_opy_(options._caps)
  except Exception as e:
    logger.debug(bstack11ll111_opy_ (u"ࠤࡰࡳࡩࡥࡩ࡯࡫ࡷࠬ࠮ࠦࡰࡰࡵࡷ࠱ࡴࡶࡴࡪࡱࡱࡷࠥࡶࡲࡶࡰࡨࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽࠣକ").format(e))
  if bstack1ll1lllll1_opy_:
    options = bstack11l11l11l1_opy_(options)
  bstack1ll11111l1_opy_ = CONFIG.get(bstack11ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ଖ"))[bstack1l111l111_opy_]
  if proxy and bstack1ll1lll11_opy_() >= version.parse(bstack11ll111_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫଗ")):
    options.proxy(proxy)
  if options and bstack1ll1lll11_opy_() >= version.parse(bstack11ll111_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫଘ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1ll1lll11_opy_() < version.parse(bstack11ll111_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬଙ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1l11l11111_opy_)
  logger.info(bstack11llll11ll_opy_)
  bstack11111111l_opy_.end(EVENTS.bstack1l1lll1l_opy_.value, EVENTS.bstack1l1lll1l_opy_.value + bstack11ll111_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢଚ"), EVENTS.bstack1l1lll1l_opy_.value + bstack11ll111_opy_ (u"ࠣ࠼ࡨࡲࡩࠨଛ"), status=True, failure=None, test_name=bstack1lll11lll_opy_)
  if bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡴࡷࡵࡦࡪ࡮ࡨࠫଜ") in kwargs:
    del kwargs[bstack11ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡵࡸ࡯ࡧ࡫࡯ࡩࠬଝ")]
  bstack1111l1l1l_opy_.end(EVENTS.bstack11ll111lll_opy_.value, bstack11llllllll_opy_ + bstack11ll111_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦଞ"), bstack11llllllll_opy_ + bstack11ll111_opy_ (u"ࠧࡀࡥ࡯ࡦࠥଟ"), status=True, failure=None, test_name=bstack1lll11lll_opy_)
  try:
    if bstack1ll1lll11_opy_() >= version.parse(bstack11ll111_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ଠ")):
      bstack11lll1ll_opy_(self, command_executor=command_executor,
                options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
    elif bstack1ll1lll11_opy_() >= version.parse(bstack11ll111_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ଡ")):
      bstack11lll1ll_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities, options=options,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1ll1lll11_opy_() >= version.parse(bstack11ll111_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨଢ")):
      bstack11lll1ll_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    else:
      bstack11lll1ll_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive)
  except Exception as bstack11ll111111_opy_:
    logger.error(bstack1lllllll1l_opy_.format(bstack11ll111_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠨଣ"), str(bstack11ll111111_opy_)))
    raise bstack11ll111111_opy_
  bstack11llllllll_opy_ = bstack1111l1l1l_opy_.bstack1ll111l11_opy_(EVENTS.bstack1llll11l11_opy_.value)
  if bstack11l11l11ll_opy_.bstack11l1111ll_opy_(CONFIG, bstack1l111l111_opy_) and bstack11l11l11ll_opy_.bstack1l1lllll1l_opy_(self.caps, options, desired_capabilities):
    if CONFIG[bstack11ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬତ")][bstack11ll111_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪଥ")] == True:
      threading.current_thread().appA11yPlatform = True
      if cli.accessibility is None or not cli.accessibility.is_enabled():
        bstack11l11l11ll_opy_.set_capabilities(bstack1l11l11111_opy_, CONFIG)
  try:
    bstack1ll1111l11_opy_ = bstack11ll111_opy_ (u"ࠬ࠭ଦ")
    if bstack1ll1lll11_opy_() >= version.parse(bstack11ll111_opy_ (u"࠭࠴࠯࠲࠱࠴ࡧ࠷ࠧଧ")):
      if self.caps is not None:
        bstack1ll1111l11_opy_ = self.caps.get(bstack11ll111_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢନ"))
    else:
      if self.capabilities is not None:
        bstack1ll1111l11_opy_ = self.capabilities.get(bstack11ll111_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣ଩"))
    if bstack1ll1111l11_opy_:
      bstack1l111111_opy_(bstack1ll1111l11_opy_)
      if bstack1ll1lll11_opy_() <= version.parse(bstack11ll111_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩପ")):
        if bstack11lll111ll_opy_.startswith(bstack11ll111_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫଫ")) or bstack11lll111ll_opy_.startswith(bstack11ll111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࠭ବ")):
          self.command_executor._url = bstack11lll111ll_opy_
        else:
          self.command_executor._url = bstack11ll111_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨଭ") + bstack11lll111ll_opy_ + bstack11ll111_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥମ")
      else:
        self.command_executor._url = bstack11ll111_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤଯ") + bstack1ll1111l11_opy_ + bstack11ll111_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤର")
      logger.debug(bstack111l111lll_opy_.format(bstack1ll1111l11_opy_))
    else:
      logger.debug(bstack1l111lll1l_opy_.format(bstack11ll111_opy_ (u"ࠤࡒࡴࡹ࡯࡭ࡢ࡮ࠣࡌࡺࡨࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦࠥ଱")))
  except Exception as e:
    logger.debug(bstack1l111lll1l_opy_.format(e))
  if bstack11ll111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩଲ") in bstack111l11111l_opy_:
    bstack11ll11l1_opy_(bstack1lll1l11_opy_, bstack11ll1ll1_opy_)
  bstack1lll1l1l_opy_ = self.session_id
  if bstack11ll111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫଳ") in bstack111l11111l_opy_ or bstack11ll111_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ଴") in bstack111l11111l_opy_ or bstack11ll111_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬଵ") in bstack111l11111l_opy_ or bstack11ll111_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡨࡧࡱࡩࡷ࡯ࡣࠨଶ") in bstack111l11111l_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack1llll11l_opy_ = getattr(threading.current_thread(), bstack11ll111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡕࡧࡶࡸࡒ࡫ࡴࡢࠩଷ"), None)
  if bstack11ll111_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩସ") in bstack111l11111l_opy_ or bstack11ll111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩହ") in bstack111l11111l_opy_:
    TestHubHandler.bstack1l1ll1l11_opy_(self)
  if bstack11ll111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ଺") in bstack111l11111l_opy_ and bstack1llll11l_opy_ and bstack1llll11l_opy_.get(bstack11ll111_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ଻"), bstack11ll111_opy_ (u"଼࠭ࠧ")) == bstack11ll111_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨଽ"):
    TestHubHandler.bstack1l1ll1l11_opy_(self)
  with bstack1lll11ll_opy_:
    bstack1llllllll1_opy_.append(self)
  if bstack11ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫା") in CONFIG and bstack11ll111_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧି") in CONFIG[bstack11ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ୀ")][bstack1l111l111_opy_]:
    bstack1lll11lll_opy_ = CONFIG[bstack11ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧୁ")][bstack1l111l111_opy_][bstack11ll111_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪୂ")]
  logger.debug(bstack11ll1l111l_opy_.format(bstack1lll1l1l_opy_))
  bstack1111l1l1l_opy_.end(EVENTS.bstack1llll11l11_opy_.value, bstack11llllllll_opy_ + bstack11ll111_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨୃ"), bstack11llllllll_opy_ + bstack11ll111_opy_ (u"ࠢ࠻ࡧࡱࡨࠧୄ"), status=True, failure=None, test_name=bstack1lll11lll_opy_)
try:
  try:
    import Browser
    import os
    from subprocess import Popen
    from browserstack_sdk.__init__ import bstack11llll11_opy_
    def bstack11l111ll1_opy_(self, args, **kwargs):
      global CONFIG
      global bstack1l111l11l1_opy_
      from browserstack_sdk.__init__ import LAUNCH_PATCH_ROBOT_PLAYWRIGHT
      if(bstack11ll111_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࠮࡫ࡵࠥ୅") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack11ll111_opy_ (u"ࠩࢁࠫ୆")), bstack11ll111_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪେ"), bstack11ll111_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭ୈ")), bstack11ll111_opy_ (u"ࠬࡽࠧ୉")) as fp:
          fp.write(bstack11ll111_opy_ (u"ࠨࠢ୊"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack11ll111_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤୋ")))):
          with open(args[1], bstack11ll111_opy_ (u"ࠨࡴࠪୌ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack11ll111_opy_ (u"ࠩࡤࡷࡾࡴࡣࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡣࡳ࡫ࡷࡑࡣࡪࡩ࠭ࡩ࡯࡯ࡶࡨࡼࡹ࠲ࠠࡱࡣࡪࡩࠥࡃࠠࡷࡱ࡬ࡨࠥ࠶ࠩࠨ୍") in line), None)
            if index is not None:
                lines.insert(index+2, bstack11l1lllll_opy_)
            if bstack11ll111_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ୎") in CONFIG and str(CONFIG[bstack11ll111_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ୏")]).lower() != bstack11ll111_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ୐"):
                cdpUrl = bstack11llll11_opy_()
                LAUNCH_PATCH_ROBOT_PLAYWRIGHT = bstack11ll111_opy_ (u"࠭ࠧࠨࠌ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࠏࡩ࡯࡯ࡵࡷࠤࡧࡹࡴࡢࡥ࡮ࡣࡵࡧࡴࡩࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸ࡣ࠻ࠋࡥࡲࡲࡸࡺࠠࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠲࡟࠾ࠎࡨࡵ࡮ࡴࡶࠣࡴࡤ࡯࡮ࡥࡧࡻࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠲࡞࠽ࠍࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡷࡱ࡯ࡣࡦࠪ࠳࠰ࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳ࠪ࠽ࠍࡧࡴࡴࡳࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣࠫ࠾ࠎ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡱࡧࡵ࡯ࡥ࡫ࠤࡂࠦࡡࡴࡻࡱࡧࠥ࠮࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸ࠯ࠠ࠾ࡀࠣࡿࢀࠐࠠࠡ࡮ࡨࡸࠥࡩࡡࡱࡵ࠾ࠎࠥࠦࡴࡳࡻࠣࡿࢀࠐࠠࠡࠢࠣࡧࡦࡶࡳࠡ࠿ࠣࡎࡘࡕࡎ࠯ࡲࡤࡶࡸ࡫ࠨࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷ࠮ࡁࠊࠡࠢࢀࢁࠥࡩࡡࡵࡥ࡫ࠤ࠭࡫ࡸࠪࠢࡾࡿࠏࠦࠠࠡࠢࡦࡳࡳࡹ࡯࡭ࡧ࠱ࡩࡷࡸ࡯ࡳࠪࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ࠾ࠧ࠲ࠠࡦࡺࠬ࠿ࠏࠦࠠࡾࡿࠍࠤࠥࡸࡥࡵࡷࡵࡲࠥࡧࡷࡢ࡫ࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡨࡵ࡮࡯ࡧࡦࡸ࠭ࢁࡻࠋࠢࠣࠤࠥࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵ࠼ࠣࠫࢀࡩࡤࡱࡗࡵࡰࢂ࠭ࠠࠬࠢࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩ࠭ࠌࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴࠌࠣࠤࢂࢃࠩ࠼ࠌࢀࢁࡀࠐࡣࡰࡰࡶࡸࠥࡵࡲࡪࡩ࡬ࡲࡦࡲ࡟ࡤࡱࡱࡲࡪࡩࡴࠡ࠿ࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷ࠲ࡧ࡯࡮ࡥࠪ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱ࠮ࡤࡪࡵࡳࡲ࡯ࡵ࡮ࠫ࠾ࠎ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡨࡵ࡮࡯ࡧࡦࡸࠥࡃࠠࡢࡵࡼࡲࡨࠦࠨࡤࡱࡱࡲࡪࡩࡴࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁࡻࠋࠢࠣࡰࡪࡺࠠࡤࡣࡳࡷࡀࠐࠠࠡࡶࡵࡽࠥࢁࡻࠋࠢࠣࠤࠥࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࠼ࠌࠣࠤࢂࢃࠠࡤࡣࡷࡧ࡭ࠦࠨࡦࡺࠬࠤࢀࢁࠊࠡࠢࢀࢁࠏࠦࠠࡤࡱࡱࡷࡹࠦ࡭ࡰࡦ࡬ࡪ࡮࡫ࡤࡆࡰࡧࡴࡴ࡯࡮ࡵࠢࡀࠤࠬࢁࡣࡥࡲࡘࡶࡱࢃࠧࠡ࠭ࠣࡩࡳࡩ࡯ࡥࡧࡘࡖࡎࡉ࡯࡮ࡲࡲࡲࡪࡴࡴࠩࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡦࡥࡵࡹࠩࠪ࠽ࠍࠤࠥࡸࡥࡵࡷࡵࡲࠥࡧࡷࡢ࡫ࡷࠤࡴࡸࡩࡨ࡫ࡱࡥࡱࡥࡣࡰࡰࡱࡩࡨࡺࠨࡼࡽࠍࠤࠥࠦࠠ࠯࠰࠱ࡧࡴࡴ࡮ࡦࡥࡷࡓࡵࡺࡩࡰࡰࡶ࠰ࠏࠦࠠࠡࠢࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹࡀࠠ࡮ࡱࡧ࡭࡫࡯ࡥࡥࡇࡱࡨࡵࡵࡩ࡯ࡶࠍࠤࠥࢃࡽࠪ࠽ࠍࢁࢂࡁࠊ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱ࠍࠫࠬ࠭୑").format(cdpUrl=cdpUrl)
            lines.insert(1, LAUNCH_PATCH_ROBOT_PLAYWRIGHT)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack11ll111_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤ୒")), bstack11ll111_opy_ (u"ࠨࡹࠪ୓")) as bstack1l111l11_opy_:
              bstack1l111l11_opy_.writelines(lines)
        CONFIG[bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ୔")] = str(bstack111l11111l_opy_) + str(__version__)
        bstack111lllllll_opy_ = os.environ[bstack11ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ୕")]
        bstack1l11l1l1ll_opy_ = bstack111llll11l_opy_.bstack1l1ll1lll_opy_(CONFIG, bstack111l11111l_opy_)
        CONFIG[bstack11ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧୖ")] = bstack111lllllll_opy_
        CONFIG[bstack11ll111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧୗ")] = bstack1l11l1l1ll_opy_
        bstack1l111l111_opy_ = 0 if bstack1lll1l11_opy_ < 0 else bstack1lll1l11_opy_
        try:
          if bstack11lll11ll_opy_ is True:
            bstack1l111l111_opy_ = int(multiprocessing.current_process().name)
          elif bstack111ll1l11l_opy_ is True:
            bstack1l111l111_opy_ = int(threading.current_thread().name)
        except:
          bstack1l111l111_opy_ = 0
        CONFIG[bstack11ll111_opy_ (u"ࠨࡵࡴࡧ࡚࠷ࡈࠨ୘")] = False
        CONFIG[bstack11ll111_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ୙")] = True
        bstack1l11l11111_opy_ = bstack11l1111l1l_opy_(CONFIG, bstack1l111l111_opy_)
        logger.debug(bstack1ll1l11l1l_opy_.format(str(bstack1l11l11111_opy_)))
        if CONFIG.get(bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ୚")):
          bstack1l1111l1l_opy_(bstack1l11l11111_opy_)
          bstack1l11l11111_opy_[bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ୛")] = os.environ[bstack11ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬଡ଼")]
        if bstack11ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଢ଼") in CONFIG and bstack11ll111_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ୞") in CONFIG[bstack11ll111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩୟ")][bstack1l111l111_opy_]:
          bstack1lll11lll_opy_ = CONFIG[bstack11ll111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪୠ")][bstack1l111l111_opy_][bstack11ll111_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ୡ")]
        args.append(os.path.join(os.path.expanduser(bstack11ll111_opy_ (u"ࠩࢁࠫୢ")), bstack11ll111_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪୣ"), bstack11ll111_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭୤")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1l11l11111_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack11ll111_opy_ (u"ࠧ࡯࡮ࡥࡧࡻࡣࡧࡹࡴࡢࡥ࡮࠲࡯ࡹࠢ୥"))
      bstack1l111l11l1_opy_ = True
      return bstack11ll1l1111_opy_(self, args, **kwargs)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1lll1l11l_opy_(self,
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
    global bstack1lll1l11_opy_
    global bstack1lll11lll_opy_
    global bstack11lll11ll_opy_
    global bstack111ll1l11l_opy_
    global bstack111l11111l_opy_
    CONFIG[bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ୦")] = str(bstack111l11111l_opy_) + str(__version__)
    bstack111lllllll_opy_ = os.environ[bstack11ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ୧")]
    bstack1l11l1l1ll_opy_ = bstack111llll11l_opy_.bstack1l1ll1lll_opy_(CONFIG, bstack111l11111l_opy_)
    CONFIG[bstack11ll111_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ୨")] = bstack111lllllll_opy_
    CONFIG[bstack11ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ୩")] = bstack1l11l1l1ll_opy_
    bstack1l111l111_opy_ = 0 if bstack1lll1l11_opy_ < 0 else bstack1lll1l11_opy_
    try:
      if bstack11lll11ll_opy_ is True:
        bstack1l111l111_opy_ = int(multiprocessing.current_process().name)
      elif bstack111ll1l11l_opy_ is True:
        bstack1l111l111_opy_ = int(threading.current_thread().name)
    except:
      bstack1l111l111_opy_ = 0
    CONFIG[bstack11ll111_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤ୪")] = True
    bstack1l11l11111_opy_ = bstack11l1111l1l_opy_(CONFIG, bstack1l111l111_opy_)
    logger.debug(bstack1ll1l11l1l_opy_.format(str(bstack1l11l11111_opy_)))
    if CONFIG.get(bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ୫")):
      bstack1l1111l1l_opy_(bstack1l11l11111_opy_)
    if bstack11ll111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ୬") in CONFIG and bstack11ll111_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ୭") in CONFIG[bstack11ll111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ୮")][bstack1l111l111_opy_]:
      bstack1lll11lll_opy_ = CONFIG[bstack11ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ୯")][bstack1l111l111_opy_][bstack11ll111_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ୰")]
    import urllib
    import json
    if bstack11ll111_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧୱ") in CONFIG and str(CONFIG[bstack11ll111_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ୲")]).lower() != bstack11ll111_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ୳"):
        bstack1l1111ll_opy_ = bstack11llll11_opy_()
        cdpUrl = bstack1l1111ll_opy_ + urllib.parse.quote(json.dumps(bstack1l11l11111_opy_))
    else:
        cdpUrl = bstack11ll111_opy_ (u"࠭ࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠨ୴") + urllib.parse.quote(json.dumps(bstack1l11l11111_opy_))
    browser = self.connect(cdpUrl)
    return browser
except Exception as e:
    pass
def bstack11l1l111l1_opy_():
    global bstack1l111l11l1_opy_
    global bstack111l11111l_opy_
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l1ll1lll1_opy_
        global global_config
        if not bstack11ll11l11l_opy_:
          global bstack1ll1l11lll_opy_
          if not bstack1ll1l11lll_opy_:
            from bstack_utils.helper import bstack1l1l111l_opy_, bstack11l11l11_opy_, bstack1lll1ll11l_opy_
            bstack1ll1l11lll_opy_ = bstack1l1l111l_opy_()
            bstack11l11l11_opy_(bstack111l11111l_opy_)
            bstack1l11l1l1ll_opy_ = bstack111llll11l_opy_.bstack1l1ll1lll_opy_(CONFIG, bstack111l11111l_opy_)
            global_config.bstack111lll11ll_opy_(bstack11ll111_opy_ (u"ࠢࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡕࡘࡏࡅࡗࡆࡘࡤࡓࡁࡑࠤ୵"), bstack1l11l1l1ll_opy_)
          BrowserType.connect = bstack1l1ll1lll1_opy_
          return
        BrowserType.launch = bstack1lll1l11l_opy_
        bstack1l111l11l1_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack11l111ll1_opy_
      bstack1l111l11l1_opy_ = True
    except Exception as e:
      pass
def bstack11l11l111l_opy_(context, bstack1ll1ll1lll_opy_):
  try:
    if getattr(context, bstack11ll111_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭୶"), None):
      context.page.evaluate(bstack11ll111_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥ୷"), bstack11ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠧ୸")+ json.dumps(bstack1ll1ll1lll_opy_) + bstack11ll111_opy_ (u"ࠦࢂࢃࠢ୹"))
  except Exception as e:
    logger.debug(bstack11ll111_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡼࡿ࠽ࠤࢀࢃࠢ୺").format(str(e), traceback.format_exc()))
def bstack11l1ll1ll_opy_(context, message, level):
  try:
    if getattr(context, bstack11ll111_opy_ (u"࠭ࡰࡢࡩࡨࠫ୻"), None):
      context.page.evaluate(bstack11ll111_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣ୼"), bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭୽") + json.dumps(message) + bstack11ll111_opy_ (u"ࠩ࠯ࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠬ୾") + json.dumps(level) + bstack11ll111_opy_ (u"ࠪࢁࢂ࠭୿"))
  except Exception as e:
    logger.debug(bstack11ll111_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡢࡰࡱࡳࡹࡧࡴࡪࡱࡱࠤࢀࢃ࠺ࠡࡽࢀࠦ஀").format(str(e), traceback.format_exc()))
@measure(event_name=EVENTS.bstack1l1l1l1l1l_opy_, stage=STAGE.bstack1111l1111_opy_, bstack11ll11ll11_opy_=bstack1lll11lll_opy_)
def bstack1lll11l1_opy_(self, url):
  global bstack11lll1ll1l_opy_
  try:
    bstack111l11l111_opy_(url)
  except Exception as err:
    logger.debug(bstack1111ll1l_opy_.format(str(err)))
  try:
    bstack11lll1ll1l_opy_(self, url)
  except Exception as e:
    try:
      bstack111lllll1l_opy_ = str(e)
      if any(err_msg in bstack111lllll1l_opy_ for err_msg in bstack111l1lll1l_opy_):
        bstack111l11l111_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1111ll1l_opy_.format(str(err)))
    raise e
def bstack11l1l1l1l1_opy_(self):
  global bstack1ll11l11l1_opy_
  bstack1ll11l11l1_opy_ = self
  return
def bstack111l1l1l1l_opy_(self):
  global bstack11111ll11_opy_
  bstack11111ll11_opy_ = self
  return
def bstack1l11111l1_opy_(test_name, bstack1lllll1l1_opy_):
  global CONFIG
  if percy.bstack1lll11ll1l_opy_() == bstack11ll111_opy_ (u"ࠧࡺࡲࡶࡧࠥ஁"):
    bstack1l1111ll11_opy_ = os.path.relpath(bstack1lllll1l1_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack1l1111ll11_opy_)
    bstack11ll11ll11_opy_ = suite_name + bstack11ll111_opy_ (u"ࠨ࠭ࠣஂ") + test_name
    threading.current_thread().percySessionName = bstack11ll11ll11_opy_
def bstack111lll1l11_opy_(self, test, *args, **kwargs):
  global bstack11ll1lll1_opy_
  test_name = None
  bstack1lllll1l1_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1lllll1l1_opy_ = str(test.source)
  bstack1l11111l1_opy_(test_name, bstack1lllll1l1_opy_)
  bstack11ll1lll1_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.bstack1l11ll1ll_opy_, stage=STAGE.bstack1111l1111_opy_, bstack11ll11ll11_opy_=bstack1lll11lll_opy_)
def bstack1l111111l1_opy_(driver, bstack11ll11ll11_opy_):
  if not bstack1l11ll1ll1_opy_ and bstack11ll11ll11_opy_:
      bstack1ll11lll11_opy_ = {
          bstack11ll111_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧஃ"): bstack11ll111_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ஄"),
          bstack11ll111_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬஅ"): {
              bstack11ll111_opy_ (u"ࠪࡲࡦࡳࡥࠨஆ"): bstack11ll11ll11_opy_
          }
      }
      bstack11ll1l1l_opy_ = bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩஇ").format(json.dumps(bstack1ll11lll11_opy_))
      driver.execute_script(bstack11ll1l1l_opy_)
  if bstack1l111111l_opy_:
      bstack1lll1l1111_opy_ = {
          bstack11ll111_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬஈ"): bstack11ll111_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨஉ"),
          bstack11ll111_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪஊ"): {
              bstack11ll111_opy_ (u"ࠨࡦࡤࡸࡦ࠭஋"): bstack11ll11ll11_opy_ + bstack11ll111_opy_ (u"ࠩࠣࡴࡦࡹࡳࡦࡦࠤࠫ஌"),
              bstack11ll111_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ஍"): bstack11ll111_opy_ (u"ࠫ࡮ࡴࡦࡰࠩஎ")
          }
      }
      if bstack1l111111l_opy_.status == bstack11ll111_opy_ (u"ࠬࡖࡁࡔࡕࠪஏ"):
          bstack11lll1l11_opy_ = bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫஐ").format(json.dumps(bstack1lll1l1111_opy_))
          driver.execute_script(bstack11lll1l11_opy_)
          bstack1l11l1ll11_opy_(driver, bstack11ll111_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ஑"))
      elif bstack1l111111l_opy_.status == bstack11ll111_opy_ (u"ࠨࡈࡄࡍࡑ࠭ஒ"):
          reason = bstack11ll111_opy_ (u"ࠤࠥஓ")
          bstack1l1111111l_opy_ = bstack11ll11ll11_opy_ + bstack11ll111_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠫஔ")
          if bstack1l111111l_opy_.message:
              reason = str(bstack1l111111l_opy_.message)
              bstack1l1111111l_opy_ = bstack1l1111111l_opy_ + bstack11ll111_opy_ (u"ࠫࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠫக") + reason
          bstack1lll1l1111_opy_[bstack11ll111_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ஖")] = {
              bstack11ll111_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ஗"): bstack11ll111_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭஘"),
              bstack11ll111_opy_ (u"ࠨࡦࡤࡸࡦ࠭ங"): bstack1l1111111l_opy_
          }
          bstack11lll1l11_opy_ = bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧச").format(json.dumps(bstack1lll1l1111_opy_))
          driver.execute_script(bstack11lll1l11_opy_)
          bstack1l11l1ll11_opy_(driver, bstack11ll111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ஛"), reason)
          bstack111lll111l_opy_(reason, str(bstack1l111111l_opy_), str(bstack1lll1l11_opy_), logger)
@measure(event_name=EVENTS.bstack1ll11l1l1_opy_, stage=STAGE.bstack1111l1111_opy_, bstack11ll11ll11_opy_=bstack1lll11lll_opy_)
def bstack1l111l11l_opy_(driver, test):
  if percy.bstack1lll11ll1l_opy_() == bstack11ll111_opy_ (u"ࠦࡹࡸࡵࡦࠤஜ") and percy.bstack11lllllll_opy_() == bstack11ll111_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢ஝"):
      bstack1ll1l111l1_opy_ = bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"࠭ࡰࡦࡴࡦࡽࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩஞ"), None)
      bstack1lll1l1ll1_opy_(driver, bstack1ll1l111l1_opy_, test)
  if (bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫட"), None) and
      bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ஠"), None)) or (
      bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ஡"), None) and
      bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ஢"), None)):
      logger.info(bstack11ll111_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠢࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡮ࡹࠠࡶࡰࡧࡩࡷࡽࡡࡺ࠰ࠣࠦண"))
      bstack11l11l11ll_opy_.bstack111l1l11l1_opy_(driver, name=test.name, path=test.source)
def bstack1llll1l1l1_opy_(test, bstack11ll11ll11_opy_):
    try:
      bstack11lll11111_opy_ = datetime.datetime.now()
      data = {}
      if test:
        data[bstack11ll111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪத")] = bstack11ll11ll11_opy_
      if bstack1l111111l_opy_:
        if bstack1l111111l_opy_.status == bstack11ll111_opy_ (u"࠭ࡐࡂࡕࡖࠫ஥"):
          data[bstack11ll111_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ஦")] = bstack11ll111_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ஧")
        elif bstack1l111111l_opy_.status == bstack11ll111_opy_ (u"ࠩࡉࡅࡎࡒࠧந"):
          data[bstack11ll111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪன")] = bstack11ll111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫப")
          if bstack1l111111l_opy_.message:
            data[bstack11ll111_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ஫")] = str(bstack1l111111l_opy_.message)
      user = CONFIG[bstack11ll111_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ஬")]
      key = CONFIG[bstack11ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ஭")]
      host = bstack1llll1ll_opy_(cli.config, [bstack11ll111_opy_ (u"ࠣࡣࡳ࡭ࡸࠨம"), bstack11ll111_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨࠦய"), bstack11ll111_opy_ (u"ࠥࡥࡵ࡯ࠢர")], bstack11ll111_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠧற"))
      url = bstack11ll111_opy_ (u"ࠬࢁࡽ࠰ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡷࡪࡹࡳࡪࡱࡱࡷ࠴ࢁࡽ࠯࡬ࡶࡳࡳ࠭ல").format(host, bstack1lll1l1l_opy_)
      headers = {
        bstack11ll111_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡵࡻࡳࡩࠬள"): bstack11ll111_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪழ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers, auth=(user, key))
        cli.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠣࡪࡷࡸࡵࡀࡵࡱࡦࡤࡸࡪࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡹࡴࡢࡶࡸࡷࠧவ"), datetime.datetime.now() - bstack11lll11111_opy_)
    except Exception as e:
      logger.error(bstack111111111_opy_.format(str(e)))
def bstack1l1ll11l1l_opy_(test, bstack11ll11ll11_opy_):
  global CONFIG
  global bstack11111ll11_opy_
  global bstack1ll11l11l1_opy_
  global bstack1lll1l1l_opy_
  global bstack1l111111l_opy_
  global bstack1lll11lll_opy_
  global bstack11llll11l_opy_
  global bstack1ll1l1l11l_opy_
  global bstack11lll1lll_opy_
  global bstack111ll11l_opy_
  global bstack1llllllll1_opy_
  global bstack1ll11111l1_opy_
  global bstack1llll1ll1l_opy_
  try:
    if not bstack1lll1l1l_opy_:
      with bstack1llll1ll1l_opy_:
        bstack11l1llll1l_opy_ = os.path.join(os.path.expanduser(bstack11ll111_opy_ (u"ࠩࢁࠫஶ")), bstack11ll111_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪஷ"), bstack11ll111_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭ஸ"))
        if os.path.exists(bstack11l1llll1l_opy_):
          with open(bstack11l1llll1l_opy_, bstack11ll111_opy_ (u"ࠬࡸࠧஹ")) as f:
            content = f.read().strip()
            if content:
              bstack11lll111l_opy_ = json.loads(bstack11ll111_opy_ (u"ࠨࡻࠣ஺") + content + bstack11ll111_opy_ (u"ࠧࠣࡺࠥ࠾ࠥࠨࡹࠣࠩ஻") + bstack11ll111_opy_ (u"ࠣࡿࠥ஼"))
              bstack1lll1l1l_opy_ = bstack11lll111l_opy_.get(str(threading.get_ident()))
  except Exception as e:
    logger.debug(bstack11ll111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡴࡨࡥࡩ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡍࡉࡹࠠࡧ࡫࡯ࡩ࠿ࠦࠧ஽") + str(e))
  if not is_robot_playwright_installed():
    if bstack1llllllll1_opy_:
      with bstack1lll11ll_opy_:
        bstack11lll11l11_opy_ = bstack1llllllll1_opy_.copy()
      for driver in bstack11lll11l11_opy_:
        if bstack1lll1l1l_opy_ == driver.session_id:
          if test:
            bstack1l111l11l_opy_(driver, test)
          bstack1l111111l1_opy_(driver, bstack11ll11ll11_opy_)
    elif bstack1lll1l1l_opy_:
      bstack1llll1l1l1_opy_(test, bstack11ll11ll11_opy_)
    if bstack11111ll11_opy_:
      bstack1ll1l1l11l_opy_(bstack11111ll11_opy_)
    if bstack1ll11l11l1_opy_:
      bstack11lll1lll_opy_(bstack1ll11l11l1_opy_)
    if bstack1l11ll11ll_opy_:
      bstack111ll11l_opy_()
def bstack1l11ll111_opy_(self, test, *args, **kwargs):
  bstack11ll11ll11_opy_ = None
  if test:
    bstack11ll11ll11_opy_ = str(test.name)
  bstack1l1ll11l1l_opy_(test, bstack11ll11ll11_opy_)
  bstack11llll11l_opy_(self, test, *args, **kwargs)
def bstack1lll111l11_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack11lll1l11l_opy_
  global CONFIG
  global bstack1llllllll1_opy_
  global bstack1lll1l1l_opy_
  global bstack1llll1ll1l_opy_
  bstack111111l1_opy_ = None
  try:
    if bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩா"), None) or bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ி"), None):
      try:
        if not bstack1lll1l1l_opy_:
          bstack11l1llll1l_opy_ = os.path.join(os.path.expanduser(bstack11ll111_opy_ (u"ࠬࢄࠧீ")), bstack11ll111_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ு"), bstack11ll111_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩூ"))
          with bstack1llll1ll1l_opy_:
            if os.path.exists(bstack11l1llll1l_opy_):
              with open(bstack11l1llll1l_opy_, bstack11ll111_opy_ (u"ࠨࡴࠪ௃")) as f:
                content = f.read().strip()
                if content:
                  bstack11lll111l_opy_ = json.loads(bstack11ll111_opy_ (u"ࠤࡾࠦ௄") + content + bstack11ll111_opy_ (u"ࠪࠦࡽࠨ࠺ࠡࠤࡼࠦࠬ௅") + bstack11ll111_opy_ (u"ࠦࢂࠨெ"))
                  bstack1lll1l1l_opy_ = bstack11lll111l_opy_.get(str(threading.get_ident()))
      except Exception as e:
        logger.debug(bstack11ll111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡷ࡫ࡡࡥ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡉࡅࡵࠣࡪ࡮ࡲࡥࠡ࡫ࡱࠤࡹ࡫ࡳࡵࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࠫே") + str(e))
      if bstack1llllllll1_opy_:
        with bstack1lll11ll_opy_:
          bstack11lll11l11_opy_ = bstack1llllllll1_opy_.copy()
        for driver in bstack11lll11l11_opy_:
          if bstack1lll1l1l_opy_ == driver.session_id:
            bstack111111l1_opy_ = driver
    bstack11l1llll1_opy_ = bstack11l11l11ll_opy_.bstack1l11ll1111_opy_(test.tags)
    if bstack111111l1_opy_:
      threading.current_thread().isA11yTest = bstack11l11l11ll_opy_.bstack11lll111l1_opy_(bstack111111l1_opy_, bstack11l1llll1_opy_)
      threading.current_thread().isAppA11yTest = bstack11l11l11ll_opy_.bstack11lll111l1_opy_(bstack111111l1_opy_, bstack11l1llll1_opy_)
    else:
      threading.current_thread().isA11yTest = bstack11l1llll1_opy_
      threading.current_thread().isAppA11yTest = bstack11l1llll1_opy_
  except:
    pass
  bstack11lll1l11l_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1l111111l_opy_
  try:
    bstack1l111111l_opy_ = self._test
  except:
    bstack1l111111l_opy_ = self.test
def bstack1ll1ll1l_opy_():
  global bstack1l111l111l_opy_
  try:
    if os.path.exists(bstack1l111l111l_opy_):
      os.remove(bstack1l111l111l_opy_)
  except Exception as e:
    logger.debug(bstack11ll111_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡦࡨࡰࡪࡺࡩ࡯ࡩࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺ࠡࠩை") + str(e))
def bstack1l11ll1lll_opy_():
  global bstack1l111l111l_opy_
  bstack111llll1ll_opy_ = {}
  lock_file = bstack1l111l111l_opy_ + bstack11ll111_opy_ (u"ࠧ࠯࡮ࡲࡧࡰ࠭௉")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack11ll111_opy_ (u"ࠨࡨ࡬ࡰࡪࡲ࡯ࡤ࡭ࠣࡲࡴࡺࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧ࠯ࠤࡺࡹࡩ࡯ࡩࠣࡦࡦࡹࡩࡤࠢࡩ࡭ࡱ࡫ࠠࡰࡲࡨࡶࡦࡺࡩࡰࡰࡶࠫொ"))
    try:
      if not os.path.isfile(bstack1l111l111l_opy_):
        with open(bstack1l111l111l_opy_, bstack11ll111_opy_ (u"ࠩࡺࠫோ")) as f:
          json.dump({}, f)
      if os.path.exists(bstack1l111l111l_opy_):
        with open(bstack1l111l111l_opy_, bstack11ll111_opy_ (u"ࠪࡶࠬௌ")) as f:
          content = f.read().strip()
          if content:
            bstack111llll1ll_opy_ = json.loads(content)
    except Exception as e:
      logger.debug(bstack11ll111_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡲࡦࡣࡧ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾்ࠥ࠭") + str(e))
    return bstack111llll1ll_opy_
  try:
    os.makedirs(os.path.dirname(bstack1l111l111l_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      if not os.path.isfile(bstack1l111l111l_opy_):
        with open(bstack1l111l111l_opy_, bstack11ll111_opy_ (u"ࠬࡽࠧ௎")) as f:
          json.dump({}, f)
      if os.path.exists(bstack1l111l111l_opy_):
        with open(bstack1l111l111l_opy_, bstack11ll111_opy_ (u"࠭ࡲࠨ௏")) as f:
          content = f.read().strip()
          if content:
            bstack111llll1ll_opy_ = json.loads(content)
  except Exception as e:
    logger.debug(bstack11ll111_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡵࡩࡦࡪࡩ࡯ࡩࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺ࠡࠩௐ") + str(e))
  finally:
    return bstack111llll1ll_opy_
def bstack11ll11l1_opy_(platform_index, item_index):
  global bstack1l111l111l_opy_
  lock_file = bstack1l111l111l_opy_ + bstack11ll111_opy_ (u"ࠨ࠰࡯ࡳࡨࡱࠧ௑")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack11ll111_opy_ (u"ࠩࡩ࡭ࡱ࡫࡬ࡰࡥ࡮ࠤࡳࡵࡴࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨ࠰ࠥࡻࡳࡪࡰࡪࠤࡧࡧࡳࡪࡥࠣࡪ࡮ࡲࡥࠡࡱࡳࡩࡷࡧࡴࡪࡱࡱࡷࠬ௒"))
    try:
      bstack111llll1ll_opy_ = {}
      if os.path.exists(bstack1l111l111l_opy_):
        with open(bstack1l111l111l_opy_, bstack11ll111_opy_ (u"ࠪࡶࠬ௓")) as f:
          content = f.read().strip()
          if content:
            bstack111llll1ll_opy_ = json.loads(content)
      bstack111llll1ll_opy_[item_index] = platform_index
      with open(bstack1l111l111l_opy_, bstack11ll111_opy_ (u"ࠦࡼࠨ௔")) as outfile:
        json.dump(bstack111llll1ll_opy_, outfile)
    except Exception as e:
      logger.debug(bstack11ll111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡸࡴ࡬ࡸ࡮ࡴࡧࠡࡶࡲࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪ௕") + str(e))
    return
  try:
    os.makedirs(os.path.dirname(bstack1l111l111l_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      bstack111llll1ll_opy_ = {}
      if os.path.exists(bstack1l111l111l_opy_):
        with open(bstack1l111l111l_opy_, bstack11ll111_opy_ (u"࠭ࡲࠨ௖")) as f:
          content = f.read().strip()
          if content:
            bstack111llll1ll_opy_ = json.loads(content)
      bstack111llll1ll_opy_[item_index] = platform_index
      with open(bstack1l111l111l_opy_, bstack11ll111_opy_ (u"ࠢࡸࠤௗ")) as outfile:
        json.dump(bstack111llll1ll_opy_, outfile)
  except Exception as e:
    logger.debug(bstack11ll111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡻࡷ࡯ࡴࡪࡰࡪࠤࡹࡵࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭௘") + str(e))
def bstack11llll1l11_opy_(bstack1l1111llll_opy_):
  global CONFIG
  bstack1l1l111ll1_opy_ = bstack11ll111_opy_ (u"ࠩࠪ௙")
  if not bstack11ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭௚") in CONFIG:
    logger.info(bstack11ll111_opy_ (u"ࠫࡓࡵࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠣࡴࡦࡹࡳࡦࡦࠣࡹࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡴࡨࡴࡴࡸࡴࠡࡨࡲࡶࠥࡘ࡯ࡣࡱࡷࠤࡷࡻ࡮ࠨ௛"))
  try:
    platform = CONFIG[bstack11ll111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ௜")][bstack1l1111llll_opy_]
    if bstack11ll111_opy_ (u"࠭࡯ࡴࠩ௝") in platform:
      bstack1l1l111ll1_opy_ += str(platform[bstack11ll111_opy_ (u"ࠧࡰࡵࠪ௞")]) + bstack11ll111_opy_ (u"ࠨ࠮ࠣࠫ௟")
    if bstack11ll111_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬ௠") in platform:
      bstack1l1l111ll1_opy_ += str(platform[bstack11ll111_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭௡")]) + bstack11ll111_opy_ (u"ࠫ࠱ࠦࠧ௢")
    if bstack11ll111_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩ௣") in platform:
      bstack1l1l111ll1_opy_ += str(platform[bstack11ll111_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪ௤")]) + bstack11ll111_opy_ (u"ࠧ࠭ࠢࠪ௥")
    if bstack11ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪ௦") in platform:
      bstack1l1l111ll1_opy_ += str(platform[bstack11ll111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ௧")]) + bstack11ll111_opy_ (u"ࠪ࠰ࠥ࠭௨")
    if bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ௩") in platform:
      bstack1l1l111ll1_opy_ += str(platform[bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ௪")]) + bstack11ll111_opy_ (u"࠭ࠬࠡࠩ௫")
    if bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ௬") in platform:
      bstack1l1l111ll1_opy_ += str(platform[bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ௭")]) + bstack11ll111_opy_ (u"ࠩ࠯ࠤࠬ௮")
  except Exception as e:
    logger.debug(bstack11ll111_opy_ (u"ࠪࡗࡴࡳࡥࠡࡧࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡳ࡭ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡶࡸࡷ࡯࡮ࡨࠢࡩࡳࡷࠦࡲࡦࡲࡲࡶࡹࠦࡧࡦࡰࡨࡶࡦࡺࡩࡰࡰࠪ௯") + str(e))
  finally:
    if bstack1l1l111ll1_opy_[len(bstack1l1l111ll1_opy_) - 2:] == bstack11ll111_opy_ (u"ࠫ࠱ࠦࠧ௰"):
      bstack1l1l111ll1_opy_ = bstack1l1l111ll1_opy_[:-2]
    return bstack1l1l111ll1_opy_
def bstack111lll1ll1_opy_(path, bstack1l1l111ll1_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack11lllll1ll_opy_ = ET.parse(path)
    bstack1llll1lll_opy_ = bstack11lllll1ll_opy_.getroot()
    bstack11l111l111_opy_ = None
    for suite in bstack1llll1lll_opy_.iter(bstack11ll111_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫ௱")):
      if bstack11ll111_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭௲") in suite.attrib:
        suite.attrib[bstack11ll111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ௳")] += bstack11ll111_opy_ (u"ࠨࠢࠪ௴") + bstack1l1l111ll1_opy_
        bstack11l111l111_opy_ = suite
    bstack1lll111lll_opy_ = None
    for robot in bstack1llll1lll_opy_.iter(bstack11ll111_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ௵")):
      bstack1lll111lll_opy_ = robot
    bstack1l111llll1_opy_ = len(bstack1lll111lll_opy_.findall(bstack11ll111_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩ௶")))
    if bstack1l111llll1_opy_ == 1:
      bstack1lll111lll_opy_.remove(bstack1lll111lll_opy_.findall(bstack11ll111_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪ௷"))[0])
      bstack111l1l1l11_opy_ = ET.Element(bstack11ll111_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫ௸"), attrib={bstack11ll111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ௹"): bstack11ll111_opy_ (u"ࠧࡔࡷ࡬ࡸࡪࡹࠧ௺"), bstack11ll111_opy_ (u"ࠨ࡫ࡧࠫ௻"): bstack11ll111_opy_ (u"ࠩࡶ࠴ࠬ௼")})
      bstack1lll111lll_opy_.insert(1, bstack111l1l1l11_opy_)
      bstack1lllll1l1l_opy_ = None
      for suite in bstack1lll111lll_opy_.iter(bstack11ll111_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩ௽")):
        bstack1lllll1l1l_opy_ = suite
      bstack1lllll1l1l_opy_.append(bstack11l111l111_opy_)
      bstack1l1lll1lll_opy_ = None
      for status in bstack11l111l111_opy_.iter(bstack11ll111_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ௾")):
        bstack1l1lll1lll_opy_ = status
      bstack1lllll1l1l_opy_.append(bstack1l1lll1lll_opy_)
    bstack11lllll1ll_opy_.write(path)
  except Exception as e:
    logger.debug(bstack11ll111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡵࡷ࡮ࡴࡧࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡱࡩࡷࡧࡴࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠪ௿") + str(e))
def bstack1l1ll111ll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1l11ll1l_opy_
  global CONFIG
  if bstack11ll111_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡶࡡࡵࡪࠥఀ") in options:
    del options[bstack11ll111_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡰࡢࡶ࡫ࠦఁ")]
  bstack1ll11111_opy_ = bstack1l11ll1lll_opy_()
  for item_id in bstack1ll11111_opy_.keys():
    path = os.path.join(outs_dir, str(item_id), bstack11ll111_opy_ (u"ࠨࡱࡸࡸࡵࡻࡴ࠯ࡺࡰࡰࠬం"))
    bstack111lll1ll1_opy_(path, bstack11llll1l11_opy_(bstack1ll11111_opy_[item_id]))
  bstack1ll1ll1l_opy_()
  return bstack1l11ll1l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1l1l1ll11_opy_(self, ff_profile_dir):
  global bstack11l11ll1_opy_
  if not ff_profile_dir:
    return None
  return bstack11l11ll1_opy_(self, ff_profile_dir)
def bstack1l1l111ll_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack11111ll1l_opy_
  bstack111llll1l1_opy_ = []
  if bstack11ll111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬః") in CONFIG:
    bstack111llll1l1_opy_ = CONFIG[bstack11ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ఄ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack11ll111_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࠧఅ")],
      pabot_args[bstack11ll111_opy_ (u"ࠧࡼࡥࡳࡤࡲࡷࡪࠨఆ")],
      argfile,
      pabot_args.get(bstack11ll111_opy_ (u"ࠨࡨࡪࡸࡨࠦఇ")),
      pabot_args[bstack11ll111_opy_ (u"ࠢࡱࡴࡲࡧࡪࡹࡳࡦࡵࠥఈ")],
      platform[0],
      bstack11111ll1l_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack11ll111_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡩ࡭ࡱ࡫ࡳࠣఉ")] or [(bstack11ll111_opy_ (u"ࠤࠥఊ"), None)]
    for platform in enumerate(bstack111llll1l1_opy_)
  ]
def bstack111l11ll1_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1l11111l_opy_=bstack11ll111_opy_ (u"ࠪࠫఋ")):
  global bstack1ll1l1l1ll_opy_
  self.platform_index = platform_index
  self.bstack1l11lll11_opy_ = bstack1l11111l_opy_
  bstack1ll1l1l1ll_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack11l1lll1l_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1l1111ll1l_opy_
  global bstack1lll1ll1ll_opy_
  bstack111l1l111l_opy_ = copy.deepcopy(item)
  if not bstack11ll111_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ఌ") in item.options:
    bstack111l1l111l_opy_.options[bstack11ll111_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ఍")] = []
  bstack1111l1ll_opy_ = bstack111l1l111l_opy_.options[bstack11ll111_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨఎ")].copy()
  for v in bstack111l1l111l_opy_.options[bstack11ll111_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩఏ")]:
    if bstack11ll111_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡑࡎࡄࡘࡋࡕࡒࡎࡋࡑࡈࡊ࡞ࠧఐ") in v:
      bstack1111l1ll_opy_.remove(v)
    if bstack11ll111_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡅࡏࡍࡆࡘࡇࡔࠩ఑") in v:
      bstack1111l1ll_opy_.remove(v)
    if bstack11ll111_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡇࡉࡋࡒࡏࡄࡃࡏࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧఒ") in v:
      bstack1111l1ll_opy_.remove(v)
  bstack1111l1ll_opy_.insert(0, bstack11ll111_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚࠽ࡿࢂ࠭ఓ").format(bstack111l1l111l_opy_.platform_index))
  bstack1111l1ll_opy_.insert(0, bstack11ll111_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡉࡋࡆࡍࡑࡆࡅࡑࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓ࠼ࡾࢁࠬఔ").format(bstack111l1l111l_opy_.bstack1l11lll11_opy_))
  bstack111l1l111l_opy_.options[bstack11ll111_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨక")] = bstack1111l1ll_opy_
  if bstack1lll1ll1ll_opy_:
    bstack111l1l111l_opy_.options[bstack11ll111_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩఖ")].insert(0, bstack11ll111_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓ࠻ࡽࢀࠫగ").format(bstack1lll1ll1ll_opy_))
  return bstack1l1111ll1l_opy_(caller_id, datasources, is_last, bstack111l1l111l_opy_, outs_dir)
def bstack1ll1l1l1l_opy_(command, item_index):
  try:
    if global_config.get_property(bstack11ll111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪఘ")):
      os.environ[bstack11ll111_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫఙ")] = json.dumps(CONFIG[bstack11ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧచ")][item_index % bstack1111l11ll_opy_])
    global bstack1lll1ll1ll_opy_
    os.environ[bstack11ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬఛ")] = str(item_index % bstack1111l11ll_opy_)
    listener_arg = bstack11ll111_opy_ (u"࠭ࠧజ")
    if is_robot_playwright_installed() and cli.is_enabled(CONFIG):
      listener_arg = bstack11ll111_opy_ (u"ࠧࠡ࠯࠰ࡰ࡮ࡹࡴࡦࡰࡨࡶࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡸࡪ࡫࠯ࡴࡲࡦࡴࡺ࡟࡭࡫ࡶࡸࡪࡴࡥࡳࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠴ࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡓࡥࡹࡩࡨࡦࡴࠪఝ")
      logger.debug(bstack11ll111_opy_ (u"ࠣࡃࡧࡨ࡮ࡴࡧࠡࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡕࡧࡴࡤࡪࡨࡶࠥࡲࡩࡴࡶࡨࡲࡪࡸࠠࡧࡱࡵࠤ࡮ࡺࡥ࡮ࠢࡾࢁࠧఞ").format(item_index))
    bstack1l1l11l1l1_opy_ = bstack11ll111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠮ࡵࡧ࡯ࠥࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱࠦ࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࠢࠥట") + \
              str(item_index % bstack1111l11ll_opy_) + \
              bstack11ll111_opy_ (u"ࠥࠤ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠣࠦఠ") + \
              str(item_index) + \
              listener_arg
    if bstack1lll1ll1ll_opy_:
        bstack1l1l11l1l1_opy_ += bstack11ll111_opy_ (u"ࠦࠥࠨడ") + bstack1lll1ll1ll_opy_
    command[0:1] = bstack1l1l11l1l1_opy_.split()
  except Exception as e:
    logger.error(bstack11ll111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡲࡵࡤࡪࡨࡼ࡭ࡳ࡭ࠠࡤࡱࡰࡱࡦࡴࡤࠡࡨࡲࡶࠥࡶࡡࡣࡱࡷࠤࡷࡻ࡮࠻ࠢࡾࢁࠬఢ").format(str(e)))
def bstack111l11lll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack111ll11ll1_opy_
  try:
    bstack1ll1l1l1l_opy_(command, item_index)
    return bstack111ll11ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
  except Exception as e:
    logger.error(bstack11ll111_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠࡳࡷࡱ࠾ࠥࢁࡽࠨణ").format(str(e)))
    raise e
def bstack11ll1111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack111ll11ll1_opy_
  try:
    bstack1ll1l1l1l_opy_(command, item_index)
    return bstack111ll11ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
  except Exception as e:
    logger.error(bstack11ll111_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡧࡵࡴࠡࡴࡸࡲࠥ࠸࠮࠲࠵࠽ࠤࢀࢃࠧత").format(str(e)))
    try:
      return bstack111ll11ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
    except Exception as e2:
      logger.error(bstack11ll111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡦࡨ࡯ࡵࠢ࠵࠲࠶࠹ࠠࡧࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣࡿࢂ࠭థ").format(str(e2)))
      raise e
def bstack1lll1l1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack111ll11ll1_opy_
  try:
    bstack1ll1l1l1l_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    return bstack111ll11ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
  except Exception as e:
    logger.error(bstack11ll111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡢࡰࡶࠣࡶࡺࡴࠠ࠳࠰࠴࠹࠿ࠦࡻࡾࠩద").format(str(e)))
    try:
      return bstack111ll11ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
    except Exception as e2:
      logger.error(bstack11ll111_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡣࡱࡷࠤ࠷࠴࠱࠶ࠢࡩࡥࡱࡲࡢࡢࡥ࡮࠾ࠥࢁࡽࠨధ").format(str(e2)))
      raise e
def _1111llllll_opy_(bstack1l1l1ll111_opy_, item_index, process_timeout, sleep_before_start, bstack11l111l1_opy_):
  bstack1ll1l1l1l_opy_(bstack1l1l1ll111_opy_, item_index)
  if process_timeout is None:
    process_timeout = 3600
  if sleep_before_start and sleep_before_start > 0:
    time.sleep(min(sleep_before_start, 5))
  return process_timeout
def bstack1l11111ll_opy_(command, bstack11l11lll_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack111ll11ll1_opy_
  global bstack11l11llll_opy_
  global bstack1lll1ll1ll_opy_
  try:
    for env_name, bstack1111111l1_opy_ in bstack11l11llll_opy_.items():
      os.environ[env_name] = bstack1111111l1_opy_
    bstack1lll1ll1ll_opy_ = bstack11ll111_opy_ (u"ࠦࠧన")
    bstack1ll1l1l1l_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    if sleep_before_start and sleep_before_start > 0:
      time.sleep(min(sleep_before_start, 5))
    return bstack111ll11ll1_opy_(command, bstack11l11lll_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack11ll111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡥࡳࡹࠦࡲࡶࡰࠣ࠹࠳࠶࠺ࠡࡽࢀࠫ఩").format(str(e)))
    try:
      return bstack111ll11ll1_opy_(command, bstack11l11lll_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack11ll111_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠࡧࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣࡿࢂ࠭ప").format(str(e2)))
      raise e
def bstack1llll11111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack111ll11ll1_opy_
  try:
    process_timeout = _1111llllll_opy_(command, item_index, process_timeout, sleep_before_start, bstack11ll111_opy_ (u"ࠧ࠵࠰࠵ࠫఫ"))
    return bstack111ll11ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack11ll111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡦࡨ࡯ࡵࠢࡵࡹࡳࠦ࠴࠯࠴࠽ࠤࢀࢃࠧబ").format(str(e)))
    try:
      return bstack111ll11ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack11ll111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡢࡰࡶࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࡻࡾࠩభ").format(str(e2)))
      raise e
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack1ll1llll1l_opy_(self, runner, quiet=False, capture=True):
  global bstack11l11ll111_opy_
  bstack1l1llll1ll_opy_ = bstack11l11ll111_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack11ll111_opy_ (u"ࠪࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࡥࡡࡳࡴࠪమ")):
      runner.exception_arr = []
    if not hasattr(runner, bstack11ll111_opy_ (u"ࠫࡪࡾࡣࡠࡶࡵࡥࡨ࡫ࡢࡢࡥ࡮ࡣࡦࡸࡲࠨయ")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1l1llll1ll_opy_
def bstack1llll111l1_opy_(runner, hook_name, context, element, bstack111l11l1ll_opy_, *args):
  global bstack1l1ll11l1_opy_
  try:
    if runner.hooks.get(hook_name):
      bstack1ll1111l1_opy_.bstack11l1lll11l_opy_(hook_name, element)
    if bstack1l1ll11l1_opy_ is None or bstack1l1ll11l1_opy_:
      bstack111l11l1ll_opy_(runner, hook_name, context, *args)
    else:
      bstack11ll111ll1_opy_ = (context,) + args
      bstack111l11l1ll_opy_(runner, hook_name, *bstack11ll111ll1_opy_)
    if runner.hooks.get(hook_name):
      bstack1ll1111l1_opy_.bstack111ll1l1l_opy_(element)
      if hook_name not in [bstack11ll111_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠩర"), bstack11ll111_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠩఱ")] and args and hasattr(args[0], bstack11ll111_opy_ (u"ࠧࡦࡴࡵࡳࡷࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠧల")):
        args[0].error_message = bstack11ll111_opy_ (u"ࠨࠩళ")
  except Exception as e:
    logger.debug(bstack11ll111_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡮ࡡ࡯ࡦ࡯ࡩࠥ࡮࡯ࡰ࡭ࡶࠤ࡮ࡴࠠࡣࡧ࡫ࡥࡻ࡫࠺ࠡࡽࢀࠫఴ").format(str(e)))
@measure(event_name=EVENTS.bstack1ll1ll1l11_opy_, stage=STAGE.bstack1111l1111_opy_, hook_type=bstack11ll111_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡄࡰࡱࠨవ"), bstack11ll11ll11_opy_=bstack1lll11lll_opy_)
def bstack1ll1111ll1_opy_(runner, name, context, bstack111l11l1ll_opy_, *args):
    if runner.hooks.get(bstack11ll111_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣశ")).__name__ != bstack11ll111_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࡡࡧࡩ࡫ࡧࡵ࡭ࡶࡢ࡬ࡴࡵ࡫ࠣష"):
      bstack1llll111l1_opy_(runner, name, context, runner, bstack111l11l1ll_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack1l1lllll_opy_(bstack11ll111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬస")) else context.browser
      runner.driver_initialised = bstack11ll111_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦహ")
    except Exception as e:
      logger.debug(bstack11ll111_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡦࡵ࡭ࡻ࡫ࡲࠡ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡶࡩࠥࡧࡴࡵࡴ࡬ࡦࡺࡺࡥ࠻ࠢࡾࢁࠬ఺").format(str(e)))
def bstack1l1l1l11l_opy_(runner, name, context, bstack111l11l1ll_opy_, *args):
    bstack1llll111l1_opy_(runner, name, context, context.feature, bstack111l11l1ll_opy_, *args)
    try:
      if not bstack1l11ll1ll1_opy_:
        bstack111111l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1lllll_opy_(bstack11ll111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ఻")) else context.browser
        if is_driver_active(bstack111111l1_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack11ll111_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨ఼ࠦ")
          bstack1ll1ll1lll_opy_ = str(runner.feature.name)
          bstack11l11l111l_opy_(context, bstack1ll1ll1lll_opy_)
          bstack111111l1_opy_.execute_script(bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩఽ") + json.dumps(bstack1ll1ll1lll_opy_) + bstack11ll111_opy_ (u"ࠬࢃࡽࠨా"))
    except Exception as e:
      logger.debug(bstack11ll111_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭ి").format(str(e)))
def bstack1l11111111_opy_(runner, name, context, bstack111l11l1ll_opy_, *args):
    target = context.scenario if hasattr(context, bstack11ll111_opy_ (u"ࠧࡴࡥࡨࡲࡦࡸࡩࡰࠩీ")) else context.feature
    bstack1llll111l1_opy_(runner, name, context, target, bstack111l11l1ll_opy_, *args)
@measure(event_name=EVENTS.bstack11llll1l1l_opy_, stage=STAGE.bstack1111l1111_opy_, bstack11ll11ll11_opy_=bstack1lll11lll_opy_)
def bstack1l1l1llll_opy_(runner, name, context, bstack111l11l1ll_opy_, *args):
    bstack1ll1111l1_opy_.start_test(context)
    bstack1llll111l1_opy_(runner, name, context, context.scenario, bstack111l11l1ll_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack1l11l11l1l_opy_.bstack1llll1l11l_opy_(context, *args)
    try:
      bstack111111l1_opy_ = bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧు"), context.browser)
      if is_driver_active(bstack111111l1_opy_):
        TestHubHandler.bstack1l1ll1l11_opy_(bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨూ"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack11ll111_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧృ")
        if (not bstack1l11ll1ll1_opy_):
          scenario_name = args[0].name
          feature_name = bstack1ll1ll1lll_opy_ = str(runner.feature.name)
          bstack1ll1ll1lll_opy_ = feature_name + bstack11ll111_opy_ (u"ࠫࠥ࠳ࠠࠨౄ") + scenario_name
          if runner.driver_initialised == bstack11ll111_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢ౅"):
            bstack11l11l111l_opy_(context, bstack1ll1ll1lll_opy_)
            bstack111111l1_opy_.execute_script(bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫె") + json.dumps(bstack1ll1ll1lll_opy_) + bstack11ll111_opy_ (u"ࠧࡾࡿࠪే"))
    except Exception as e:
      logger.debug(bstack11ll111_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡨ࡫࡮ࡢࡴ࡬ࡳ࠿ࠦࡻࡾࠩై").format(str(e)))
@measure(event_name=EVENTS.bstack1ll1ll1l11_opy_, stage=STAGE.bstack1111l1111_opy_, hook_type=bstack11ll111_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡕࡷࡩࡵࠨ౉"), bstack11ll11ll11_opy_=bstack1lll11lll_opy_)
def bstack1l1l1ll11l_opy_(runner, name, context, bstack111l11l1ll_opy_, *args):
    bstack1llll111l1_opy_(runner, name, context, args[0], bstack111l11l1ll_opy_, *args)
    try:
      bstack111111l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1lllll_opy_(bstack11ll111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩొ")) else context.browser
      if is_driver_active(bstack111111l1_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack11ll111_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤో")
        bstack1ll1111l1_opy_.bstack11l11111l_opy_(args[0])
        if runner.driver_initialised == bstack11ll111_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥౌ"):
          feature_name = bstack1ll1ll1lll_opy_ = str(runner.feature.name)
          bstack1ll1ll1lll_opy_ = feature_name + bstack11ll111_opy_ (u"࠭ࠠ࠮్ࠢࠪ") + context.scenario.name
          bstack111111l1_opy_.execute_script(bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬ౎") + json.dumps(bstack1ll1ll1lll_opy_) + bstack11ll111_opy_ (u"ࠨࡿࢀࠫ౏"))
    except Exception as e:
      logger.debug(bstack11ll111_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡ࡫ࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡺࡥࡱ࠼ࠣࡿࢂ࠭౐").format(str(e)))
@measure(event_name=EVENTS.bstack1ll1ll1l11_opy_, stage=STAGE.bstack1111l1111_opy_, hook_type=bstack11ll111_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࡕࡷࡩࡵࠨ౑"), bstack11ll11ll11_opy_=bstack1lll11lll_opy_)
def bstack1llll111l_opy_(runner, name, context, bstack111l11l1ll_opy_, *args):
  bstack1ll1111l1_opy_.bstack11l11l1l_opy_(args[0])
  try:
    step_status = args[0].status.name
    bstack111111l1_opy_ = threading.current_thread().bstackSessionDriver if bstack11ll111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ౒") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack111111l1_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack11ll111_opy_ (u"ࠬ࡯࡮ࡴࡶࡨࡴࠬ౓")
        feature_name = bstack1ll1ll1lll_opy_ = str(runner.feature.name)
        bstack1ll1ll1lll_opy_ = feature_name + bstack11ll111_opy_ (u"࠭ࠠ࠮ࠢࠪ౔") + context.scenario.name
        bstack111111l1_opy_.execute_script(bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤౕࠬ") + json.dumps(bstack1ll1ll1lll_opy_) + bstack11ll111_opy_ (u"ࠨࡿࢀౖࠫ"))
    if str(step_status).lower() in [bstack11ll111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ౗"), bstack11ll111_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩౘ")]:
      bstack11l1lll111_opy_ = bstack11ll111_opy_ (u"ࠫࠬౙ")
      bstack1111l1l11_opy_ = bstack11ll111_opy_ (u"ࠬ࠭ౚ")
      bstack1l1ll11lll_opy_ = bstack11ll111_opy_ (u"࠭ࠧ౛")
      try:
        import traceback
        bstack11l1lll111_opy_ = runner.exception.__class__.__name__
        bstack1l11ll1l1_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1111l1l11_opy_ = bstack11ll111_opy_ (u"ࠧࠡࠩ౜").join(bstack1l11ll1l1_opy_)
        bstack1l1ll11lll_opy_ = bstack1l11ll1l1_opy_[-1]
      except Exception as e:
        logger.debug(bstack1l11llll_opy_.format(str(e)))
      bstack11l1lll111_opy_ += bstack1l1ll11lll_opy_
      bstack11l1ll1ll_opy_(context, json.dumps(str(args[0].name) + bstack11ll111_opy_ (u"ࠣࠢ࠰ࠤࡋࡧࡩ࡭ࡧࡧࠥࡡࡴࠢౝ") + str(bstack1111l1l11_opy_)),
                          bstack11ll111_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣ౞"))
      if runner.driver_initialised == bstack11ll111_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣ౟"):
        bstack111l1l1lll_opy_(getattr(context, bstack11ll111_opy_ (u"ࠫࡵࡧࡧࡦࠩౠ"), None), bstack11ll111_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧౡ"), bstack11l1lll111_opy_)
        bstack111111l1_opy_.execute_script(bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫౢ") + json.dumps(str(args[0].name) + bstack11ll111_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨౣ") + str(bstack1111l1l11_opy_)) + bstack11ll111_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨ౤"))
      if runner.driver_initialised == bstack11ll111_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢ౥"):
        bstack1l11l1ll11_opy_(bstack111111l1_opy_, bstack11ll111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ౦"), bstack11ll111_opy_ (u"ࠦࡘࡩࡥ࡯ࡣࡵ࡭ࡴࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࡢ࡮ࠣ౧") + str(bstack11l1lll111_opy_))
    else:
      bstack11l1ll1ll_opy_(context, bstack11ll111_opy_ (u"ࠧࡖࡡࡴࡵࡨࡨࠦࠨ౨"), bstack11ll111_opy_ (u"ࠨࡩ࡯ࡨࡲࠦ౩"))
      if runner.driver_initialised == bstack11ll111_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧ౪"):
        bstack111l1l1lll_opy_(getattr(context, bstack11ll111_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭౫"), None), bstack11ll111_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ౬"))
      bstack111111l1_opy_.execute_script(bstack11ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨ౭") + json.dumps(str(args[0].name) + bstack11ll111_opy_ (u"ࠦࠥ࠳ࠠࡑࡣࡶࡷࡪࡪࠡࠣ౮")) + bstack11ll111_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫ౯"))
      if runner.driver_initialised == bstack11ll111_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦ౰"):
        bstack1l11l1ll11_opy_(bstack111111l1_opy_, bstack11ll111_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ౱"))
  except Exception as e:
    logger.debug(bstack11ll111_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࠥࡹࡴࡦࡲ࠽ࠤࢀࢃࠧ౲").format(str(e)))
  bstack1llll111l1_opy_(runner, name, context, args[0], bstack111l11l1ll_opy_, *args)
@measure(event_name=EVENTS.bstack111llll11_opy_, stage=STAGE.bstack1111l1111_opy_, bstack11ll11ll11_opy_=bstack1lll11lll_opy_)
def bstack1l111l11ll_opy_(runner, name, context, bstack111l11l1ll_opy_, *args):
  bstack1ll1111l1_opy_.end_test(args[0])
  try:
    bstack1l1llll11_opy_ = args[0].status.name
    bstack111111l1_opy_ = bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ౳"), context.browser)
    bstack1l11l11l1l_opy_.bstack1l1llll1_opy_(bstack111111l1_opy_)
    if str(bstack1l1llll11_opy_).lower() in [bstack11ll111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ౴"), bstack11ll111_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ౵")]:
      bstack11l1lll111_opy_ = bstack11ll111_opy_ (u"ࠬ࠭౶")
      bstack1111l1l11_opy_ = bstack11ll111_opy_ (u"࠭ࠧ౷")
      bstack1l1ll11lll_opy_ = bstack11ll111_opy_ (u"ࠧࠨ౸")
      try:
        import traceback
        bstack11l1lll111_opy_ = runner.exception.__class__.__name__
        bstack1l11ll1l1_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1111l1l11_opy_ = bstack11ll111_opy_ (u"ࠨࠢࠪ౹").join(bstack1l11ll1l1_opy_)
        bstack1l1ll11lll_opy_ = bstack1l11ll1l1_opy_[-1]
      except Exception as e:
        logger.debug(bstack1l11llll_opy_.format(str(e)))
      bstack11l1lll111_opy_ += bstack1l1ll11lll_opy_
      bstack11l1ll1ll_opy_(context, json.dumps(str(args[0].name) + bstack11ll111_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣ౺") + str(bstack1111l1l11_opy_)),
                          bstack11ll111_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤ౻"))
      if runner.driver_initialised == bstack11ll111_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨ౼") or runner.driver_initialised == bstack11ll111_opy_ (u"ࠬ࡯࡮ࡴࡶࡨࡴࠬ౽"):
        bstack111l1l1lll_opy_(getattr(context, bstack11ll111_opy_ (u"࠭ࡰࡢࡩࡨࠫ౾"), None), bstack11ll111_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ౿"), bstack11l1lll111_opy_)
        bstack111111l1_opy_.execute_script(bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ಀ") + json.dumps(str(args[0].name) + bstack11ll111_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣಁ") + str(bstack1111l1l11_opy_)) + bstack11ll111_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪಂ"))
      if runner.driver_initialised == bstack11ll111_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨಃ") or runner.driver_initialised == bstack11ll111_opy_ (u"ࠬ࡯࡮ࡴࡶࡨࡴࠬ಄"):
        bstack1l11l1ll11_opy_(bstack111111l1_opy_, bstack11ll111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ಅ"), bstack11ll111_opy_ (u"ࠢࡔࡥࡨࡲࡦࡸࡩࡰࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦಆ") + str(bstack11l1lll111_opy_))
    else:
      bstack11l1ll1ll_opy_(context, bstack11ll111_opy_ (u"ࠣࡒࡤࡷࡸ࡫ࡤࠢࠤಇ"), bstack11ll111_opy_ (u"ࠤ࡬ࡲ࡫ࡵࠢಈ"))
      if runner.driver_initialised == bstack11ll111_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧಉ") or runner.driver_initialised == bstack11ll111_opy_ (u"ࠫ࡮ࡴࡳࡵࡧࡳࠫಊ"):
        bstack111l1l1lll_opy_(getattr(context, bstack11ll111_opy_ (u"ࠬࡶࡡࡨࡧࠪಋ"), None), bstack11ll111_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨಌ"))
      bstack111111l1_opy_.execute_script(bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ಍") + json.dumps(str(args[0].name) + bstack11ll111_opy_ (u"ࠣࠢ࠰ࠤࡕࡧࡳࡴࡧࡧࠥࠧಎ")) + bstack11ll111_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧࢃࡽࠨಏ"))
      if runner.driver_initialised == bstack11ll111_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧಐ") or runner.driver_initialised == bstack11ll111_opy_ (u"ࠫ࡮ࡴࡳࡵࡧࡳࠫ಑"):
        bstack1l11l1ll11_opy_(bstack111111l1_opy_, bstack11ll111_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧಒ"))
  except Exception as e:
    logger.debug(bstack11ll111_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨಓ").format(str(e)))
  bstack1llll111l1_opy_(runner, name, context, context.scenario, bstack111l11l1ll_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack1l1l11l1ll_opy_(runner, name, context, bstack111l11l1ll_opy_, *args):
    target = context.scenario if hasattr(context, bstack11ll111_opy_ (u"ࠧࡴࡥࡨࡲࡦࡸࡩࡰࠩಔ")) else context.feature
    bstack1llll111l1_opy_(runner, name, context, target, bstack111l11l1ll_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack1llllll111_opy_(runner, name, context, bstack111l11l1ll_opy_, *args):
    try:
      bstack111111l1_opy_ = bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧಕ"), context.browser)
      bstack11111l11l_opy_ = bstack11ll111_opy_ (u"ࠩࠪಖ")
      if context.failed is True:
        bstack1l11llll1_opy_ = []
        bstack1ll111l1l_opy_ = []
        bstack1l1l1l11ll_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack1l11llll1_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1l11ll1l1_opy_ = traceback.format_tb(exc_tb)
            bstack1ll11l1l1l_opy_ = bstack11ll111_opy_ (u"ࠪࠤࠬಗ").join(bstack1l11ll1l1_opy_)
            bstack1ll111l1l_opy_.append(bstack1ll11l1l1l_opy_)
            bstack1l1l1l11ll_opy_.append(bstack1l11ll1l1_opy_[-1])
        except Exception as e:
          logger.debug(bstack1l11llll_opy_.format(str(e)))
        bstack11l1lll111_opy_ = bstack11ll111_opy_ (u"ࠫࠬಘ")
        for i in range(len(bstack1l11llll1_opy_)):
          bstack11l1lll111_opy_ += bstack1l11llll1_opy_[i] + bstack1l1l1l11ll_opy_[i] + bstack11ll111_opy_ (u"ࠬࡢ࡮ࠨಙ")
        bstack11111l11l_opy_ = bstack11ll111_opy_ (u"࠭ࠠࠨಚ").join(bstack1ll111l1l_opy_)
        if runner.driver_initialised in [bstack11ll111_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣಛ"), bstack11ll111_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧಜ")]:
          bstack11l1ll1ll_opy_(context, bstack11111l11l_opy_, bstack11ll111_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣಝ"))
          bstack111l1l1lll_opy_(getattr(context, bstack11ll111_opy_ (u"ࠪࡴࡦ࡭ࡥࠨಞ"), None), bstack11ll111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦಟ"), bstack11l1lll111_opy_)
          bstack111111l1_opy_.execute_script(bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪಠ") + json.dumps(bstack11111l11l_opy_) + bstack11ll111_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥࢁࢂ࠭ಡ"))
          bstack1l11l1ll11_opy_(bstack111111l1_opy_, bstack11ll111_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢಢ"), bstack11ll111_opy_ (u"ࠣࡕࡲࡱࡪࠦࡳࡤࡧࡱࡥࡷ࡯࡯ࡴࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡠࡳࠨಣ") + str(bstack11l1lll111_opy_))
          bstack111l11llll_opy_ = bstack1l11l1lll_opy_(bstack11111l11l_opy_, runner.feature.name, logger)
          if (bstack111l11llll_opy_ != None):
            bstack11l1ll111_opy_.append(bstack111l11llll_opy_)
      else:
        if runner.driver_initialised in [bstack11ll111_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠥತ"), bstack11ll111_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢಥ")]:
          bstack11l1ll1ll_opy_(context, bstack11ll111_opy_ (u"ࠦࡋ࡫ࡡࡵࡷࡵࡩ࠿ࠦࠢದ") + str(runner.feature.name) + bstack11ll111_opy_ (u"ࠧࠦࡰࡢࡵࡶࡩࡩࠧࠢಧ"), bstack11ll111_opy_ (u"ࠨࡩ࡯ࡨࡲࠦನ"))
          bstack111l1l1lll_opy_(getattr(context, bstack11ll111_opy_ (u"ࠧࡱࡣࡪࡩࠬ಩"), None), bstack11ll111_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣಪ"))
          bstack111111l1_opy_.execute_script(bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧಫ") + json.dumps(bstack11ll111_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨ࠾ࠥࠨಬ") + str(runner.feature.name) + bstack11ll111_opy_ (u"ࠦࠥࡶࡡࡴࡵࡨࡨࠦࠨಭ")) + bstack11ll111_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫಮ"))
          bstack1l11l1ll11_opy_(bstack111111l1_opy_, bstack11ll111_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ಯ"))
          bstack111l11llll_opy_ = bstack1l11l1lll_opy_(bstack11111l11l_opy_, runner.feature.name, logger)
          if (bstack111l11llll_opy_ != None):
            bstack11l1ll111_opy_.append(bstack111l11llll_opy_)
    except Exception as e:
      logger.debug(bstack11ll111_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩರ").format(str(e)))
    bstack1llll111l1_opy_(runner, name, context, context.feature, bstack111l11l1ll_opy_, *args)
@measure(event_name=EVENTS.bstack1ll1ll1l11_opy_, stage=STAGE.bstack1111l1111_opy_, hook_type=bstack11ll111_opy_ (u"ࠣࡣࡩࡸࡪࡸࡁ࡭࡮ࠥಱ"), bstack11ll11ll11_opy_=bstack1lll11lll_opy_)
def bstack11ll11111l_opy_(runner, name, context, bstack111l11l1ll_opy_, *args):
    bstack1llll111l1_opy_(runner, name, context, runner, bstack111l11l1ll_opy_, *args)
def bstack11ll1111l1_opy_(self, filename=None):
  bstack11ll111_opy_ (u"ࠤࠥࠦࠏࠦࠠࡍࡱࡤࡨࠥ࡮࡯ࡰ࡭ࡶࠤࡦࡴࡤࠡࡧࡱࡷࡺࡸࡥࠡࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱ࠲ࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠤࡦࡸࡥࠡࡴࡨ࡫࡮ࡹࡴࡦࡴࡨࡨ࠳ࠐࠠࠡࡄࡨ࡬ࡦࡼࡥࠡࡸ࠴࠲࠸࠱ࠠࡥࡱࡨࡷࡳ࠭ࡴࠡࡥࡤࡰࡱࠦࡲࡶࡰࠣ࡬ࡴࡵ࡫ࡴࠢࡷ࡬ࡦࡺࠠࡢࡴࡨࡲࠬࡺࠠࡥࡧࡩ࡭ࡳ࡫ࡤ࠭ࠢࡶࡳࠥࡽࡥࠡ࡯ࡸࡷࡹࠐࠠࠡࡦࡲࠤࡹ࡮ࡩࡴࠢࡨࡼࡵࡲࡩࡤ࡫ࡷࡰࡾࠦࡴࡰࠢࡰࡥࡰ࡫ࠠࡴࡷࡵࡩࠥࡽࡥࠨࡴࡨࠤࡨࡧ࡬࡭ࡧࡧࠤ࡮ࡴࠠࡢࡰࡼࠤࡨࡧࡳࡦ࠰ࠍࠤࠥࠨࠢࠣಲ")
  global bstack111l1111_opy_
  bstack111l1111_opy_(self, filename)
  bstack1l1lll1l11_opy_ = []
  bstack11l11l1l1l_opy_ = [bstack11ll111_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠫಳ"), bstack11ll111_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡹࡧࡧࠨ಴"), bstack11ll111_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧವ"), bstack11ll111_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧಶ"), bstack11ll111_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡴࡢࡩࠪಷ"), bstack11ll111_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨಸ")]
  bstack1lll111l1l_opy_ = lambda *_: None
  for hook_name in bstack11l11l1l1l_opy_:
    if hook_name not in self.hooks:
      self.hooks[hook_name] = bstack1lll111l1l_opy_
      bstack1l1lll1l11_opy_.append(hook_name)
  if bstack1l1lll1l11_opy_:
    os.environ[bstack11ll111_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡖࡈࡐࡥࡄࡆࡈࡄ࡙ࡑ࡚࡟ࡉࡑࡒࡏࡘ࠭ಹ")] = bstack11ll111_opy_ (u"ࠪ࠰ࠬ಺").join(bstack1l1lll1l11_opy_)
def bstack1ll1lll1l_opy_(self, name, *args):
  global bstack111l11l1ll_opy_
  global bstack1l1ll11l1_opy_
  try:
    if bstack11ll11l11l_opy_:
      platform_index = int(threading.current_thread()._name) % bstack1111l11ll_opy_
      bstack1l1ll1ll_opy_ = CONFIG[bstack11ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ಻")][platform_index]
      os.environ[bstack11ll111_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ಼࠭")] = json.dumps(bstack1l1ll1ll_opy_)
    if not hasattr(self, bstack11ll111_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡧࡧࠫಽ")):
      self.driver_initialised = None
    bstack1ll111111_opy_ = {
        bstack11ll111_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠫಾ"): bstack1ll1111ll1_opy_,
        bstack11ll111_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠩಿ"): bstack1l1l1l11l_opy_,
        bstack11ll111_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡷࡥ࡬࠭ೀ"): bstack1l11111111_opy_,
        bstack11ll111_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬು"): bstack1l1l1llll_opy_,
        bstack11ll111_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠩೂ"): bstack1l1l1ll11l_opy_,
        bstack11ll111_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡺࡥࡱࠩೃ"): bstack1llll111l_opy_,
        bstack11ll111_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧೄ"): bstack1l111l11ll_opy_,
        bstack11ll111_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡴࡢࡩࠪ೅"): bstack1l1l11l1ll_opy_,
        bstack11ll111_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨೆ"): bstack1llllll111_opy_,
        bstack11ll111_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠬೇ"): bstack11ll11111l_opy_
    }
    handler = bstack1ll111111_opy_.get(name, bstack111l11l1ll_opy_)
    try:
      if args:
        context = args[0]
        remaining_args = args[1:]
        if bstack1l1ll11l1_opy_ is None or not bstack1l1ll11l1_opy_:
          context = self.context
          remaining_args = args
      else:
        context = self.context
        remaining_args = ()
      handler(self, name, context, bstack111l11l1ll_opy_, *remaining_args)
    except Exception as e:
      logger.debug(bstack11ll111_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡨࡥࡩࡣࡹࡩࠥ࡮࡯ࡰ࡭ࠣ࡬ࡦࡴࡤ࡭ࡧࡵࠤࢀࢃ࠺ࠡࡽࢀࠫೈ").format(name, str(e)))
    if name in [bstack11ll111_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫ೉"), bstack11ll111_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ೊ"), bstack11ll111_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠩೋ")]:
      try:
        bstack111111l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1lllll_opy_(bstack11ll111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ೌ")) else context.browser
        bstack111l1111ll_opy_ = (
          (name == bstack11ll111_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯್ࠫ") and self.driver_initialised == bstack11ll111_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨ೎")) or
          (name == bstack11ll111_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪ೏") and self.driver_initialised == bstack11ll111_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠧ೐")) or
          (name == bstack11ll111_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭೑") and self.driver_initialised in [bstack11ll111_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣ೒"), bstack11ll111_opy_ (u"ࠢࡪࡰࡶࡸࡪࡶࠢ೓")]) or
          (name == bstack11ll111_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡴࡶࡨࡴࠬ೔") and self.driver_initialised == bstack11ll111_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢೕ"))
        )
        if bstack111l1111ll_opy_:
          self.driver_initialised = None
          if bstack111111l1_opy_ and hasattr(bstack111111l1_opy_, bstack11ll111_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠧೖ")):
            try:
              bstack111111l1_opy_.quit()
            except Exception as e:
              logger.debug(bstack11ll111_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡵࡺ࡯ࡴࡵ࡫ࡱ࡫ࠥࡪࡲࡪࡸࡨࡶࠥ࡯࡮ࠡࡤࡨ࡬ࡦࡼࡥࠡࡪࡲࡳࡰࡀࠠࡼࡿࠪ೗").format(str(e)))
      except Exception as e:
        logger.debug(bstack11ll111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡨࡰࡱ࡮ࠤࡨࡲࡥࡢࡰࡸࡴࠥ࡬࡯ࡳࠢࡾࢁ࠿ࠦࡻࡾࠩ೘").format(name, str(e)))
  except Exception as e:
    logger.debug(bstack11ll111_opy_ (u"࠭ࡃࡳ࡫ࡷ࡭ࡨࡧ࡬ࠡࡧࡵࡶࡴࡸࠠࡪࡰࠣࡦࡪ࡮ࡡࡷࡧࠣࡶࡺࡴࠠࡩࡱࡲ࡯ࠥࢁࡽ࠻ࠢࡾࢁࠬ೙").format(name, str(e)))
    try:
      if bstack1l1ll11l1_opy_ is None or bstack1l1ll11l1_opy_:
        try:
          bstack111l11l1ll_opy_(self, name, self.context, *args)
        except TypeError:
          bstack111l11l1ll_opy_(self, name, *args)
      else:
        bstack111l11l1ll_opy_(self, name, *args)
    except Exception as e2:
      logger.debug(bstack11ll111_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡥࡱࡲࡢࡢࡥ࡮ࠤࡴࡸࡩࡨ࡫ࡱࡥࡱࠦࡢࡦࡪࡤࡺࡪࠦࡨࡰࡱ࡮ࠤࢀࢃ࠺ࠡࡽࢀࠫ೚").format(name, str(e2)))
def bstack111lll11_opy_(config, startdir):
  return bstack11ll111_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾ࠴ࢂࠨ೛").format(bstack11ll111_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣ೜"))
notset = Notset()
def bstack11l11l1l11_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack111ll1llll_opy_
  if str(name).lower() == bstack11ll111_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪೝ"):
    return bstack11ll111_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥೞ")
  else:
    return bstack111ll1llll_opy_(self, name, default, skip)
def bstack111ll111l_opy_(item, when):
  global bstack1l111ll1l_opy_
  try:
    bstack1l111ll1l_opy_(item, when)
  except Exception as e:
    pass
def bstack11llllll1_opy_():
  return
def browserstack_executor_helper(type, name, status, reason, bstack1l11l1llll_opy_, bstack11111l11_opy_):
  bstack1ll11lll11_opy_ = {
    bstack11ll111_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬ೟"): type,
    bstack11ll111_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩೠ"): {}
  }
  if type == bstack11ll111_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩೡ"):
    bstack1ll11lll11_opy_[bstack11ll111_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫೢ")][bstack11ll111_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨೣ")] = bstack1l11l1llll_opy_
    bstack1ll11lll11_opy_[bstack11ll111_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭೤")][bstack11ll111_opy_ (u"ࠫࡩࡧࡴࡢࠩ೥")] = json.dumps(str(bstack11111l11_opy_))
  if type == bstack11ll111_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭೦"):
    bstack1ll11lll11_opy_[bstack11ll111_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ೧")][bstack11ll111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ೨")] = name
  if type == bstack11ll111_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ೩"):
    bstack1ll11lll11_opy_[bstack11ll111_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ೪")][bstack11ll111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ೫")] = status
    if status == bstack11ll111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ೬"):
      bstack1ll11lll11_opy_[bstack11ll111_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ೭")][bstack11ll111_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭೮")] = json.dumps(str(reason))
  bstack11ll1l1l_opy_ = bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬ೯").format(json.dumps(bstack1ll11lll11_opy_))
  return bstack11ll1l1l_opy_
def bstack111l1l1l_opy_(driver_command, response):
    if driver_command == bstack11ll111_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬ೰"):
        TestHubHandler.bstack1lll11ll1_opy_({
            bstack11ll111_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨೱ"): response[bstack11ll111_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩೲ")],
            bstack11ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫೳ"): TestHubHandler.current_test_uuid()
        })
def bstack111lllll1_opy_(item, call, rep):
  global bstack1lll11llll_opy_
  global bstack1llllllll1_opy_
  global bstack1l11ll1ll1_opy_
  name = bstack11ll111_opy_ (u"ࠬ࠭೴")
  try:
    if rep.when == bstack11ll111_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ೵"):
      bstack1lll1l1l_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1l11ll1ll1_opy_:
          name = str(rep.nodeid)
          executor_string = browserstack_executor_helper(bstack11ll111_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ೶"), name, bstack11ll111_opy_ (u"ࠨࠩ೷"), bstack11ll111_opy_ (u"ࠩࠪ೸"), bstack11ll111_opy_ (u"ࠪࠫ೹"), bstack11ll111_opy_ (u"ࠫࠬ೺"))
          threading.current_thread().bstack11ll1111ll_opy_ = name
          for driver in bstack1llllllll1_opy_:
            if bstack1lll1l1l_opy_ == driver.session_id:
              driver.execute_script(executor_string)
      except Exception as e:
        logger.debug(bstack11ll111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬ೻").format(str(e)))
      try:
        bstack1l1ll1ll1l_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack11ll111_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ೼"):
          status = bstack11ll111_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ೽") if rep.outcome.lower() == bstack11ll111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ೾") else bstack11ll111_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ೿")
          reason = bstack11ll111_opy_ (u"ࠪࠫഀ")
          if status == bstack11ll111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫഁ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack11ll111_opy_ (u"ࠬ࡯࡮ࡧࡱࠪം") if status == bstack11ll111_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ഃ") else bstack11ll111_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ഄ")
          data = name + bstack11ll111_opy_ (u"ࠨࠢࡳࡥࡸࡹࡥࡥࠣࠪഅ") if status == bstack11ll111_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩആ") else name + bstack11ll111_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠥࠥ࠭ഇ") + reason
          bstack1l1ll1111_opy_ = browserstack_executor_helper(bstack11ll111_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭ഈ"), bstack11ll111_opy_ (u"ࠬ࠭ഉ"), bstack11ll111_opy_ (u"࠭ࠧഊ"), bstack11ll111_opy_ (u"ࠧࠨഋ"), level, data)
          for driver in bstack1llllllll1_opy_:
            if bstack1lll1l1l_opy_ == driver.session_id:
              driver.execute_script(bstack1l1ll1111_opy_)
      except Exception as e:
        logger.debug(bstack11ll111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡩ࡯࡯ࡶࡨࡼࡹࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬഌ").format(str(e)))
  except Exception as e:
    logger.debug(bstack11ll111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡴࡢࡶࡨࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿࢂ࠭഍").format(str(e)))
  bstack1lll11llll_opy_(item, call, rep)
def bstack1lll1l1ll1_opy_(driver, bstack1l111ll1_opy_, test=None):
  global bstack1lll1l11_opy_
  if test != None:
    bstack11l1ll11l_opy_ = getattr(test, bstack11ll111_opy_ (u"ࠪࡲࡦࡳࡥࠨഎ"), None)
    bstack1ll11ll1l_opy_ = getattr(test, bstack11ll111_opy_ (u"ࠫࡺࡻࡩࡥࠩഏ"), None)
    PercySDK.screenshot(driver, bstack1l111ll1_opy_, bstack11l1ll11l_opy_=bstack11l1ll11l_opy_, bstack1ll11ll1l_opy_=bstack1ll11ll1l_opy_, bstack11l111l1l_opy_=bstack1lll1l11_opy_)
  else:
    PercySDK.screenshot(driver, bstack1l111ll1_opy_)
@measure(event_name=EVENTS.bstack1lll11l1ll_opy_, stage=STAGE.bstack1111l1111_opy_, bstack11ll11ll11_opy_=bstack1lll11lll_opy_)
def bstack1l1lllllll_opy_(driver):
  if bstack1lll1lllll_opy_.bstack1l11111l1l_opy_() is True or bstack1lll1lllll_opy_.capturing() is True:
    return
  bstack1lll1lllll_opy_.bstack1l11l1l1l1_opy_()
  while not bstack1lll1lllll_opy_.bstack1l11111l1l_opy_():
    bstack111lll111_opy_ = bstack1lll1lllll_opy_.bstack1l1ll11ll1_opy_()
    bstack1lll1l1ll1_opy_(driver, bstack111lll111_opy_)
  bstack1lll1lllll_opy_.bstack1ll11lllll_opy_()
def bstack1lll1lll_opy_(sequence, driver_command, response = None, bstack1l11ll11l1_opy_ = None, args = None):
    try:
      if sequence != bstack11ll111_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬഐ"):
        return
      if percy.bstack1lll11ll1l_opy_() == bstack11ll111_opy_ (u"ࠨࡦࡢ࡮ࡶࡩࠧ഑"):
        return
      bstack111lll111_opy_ = bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠧࡱࡧࡵࡧࡾ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪഒ"), None)
      for command in bstack111111l1l_opy_:
        if command == driver_command:
          with bstack1lll11ll_opy_:
            bstack11lll11l11_opy_ = bstack1llllllll1_opy_.copy()
          for driver in bstack11lll11l11_opy_:
            bstack1l1lllllll_opy_(driver)
      bstack1l11l1lll1_opy_ = percy.bstack11lllllll_opy_()
      if driver_command in bstack111ll11ll_opy_[bstack1l11l1lll1_opy_]:
        bstack1lll1lllll_opy_.bstack111l1ll1l1_opy_(bstack111lll111_opy_, driver_command)
    except Exception as e:
      pass
def bstack1l1ll111l1_opy_(framework_name):
  if global_config.get_property(bstack11ll111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬഓ")):
      return
  global_config.bstack111lll11ll_opy_(bstack11ll111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡰࡳࡩࡥࡣࡢ࡮࡯ࡩࡩ࠭ഔ"), True)
  global bstack111l11111l_opy_
  global bstack1l111l11l1_opy_
  global bstack1llllll1ll_opy_
  bstack111l11111l_opy_ = framework_name
  logger.info(bstack111l111l_opy_.format(bstack111l11111l_opy_.split(bstack11ll111_opy_ (u"ࠪ࠱ࠬക"))[0]))
  bstack111l1111l_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    global bstack1ll1lllll1_opy_
    bstack11l1ll1111_opy_ = bstack11ll11l11l_opy_ or bstack1ll1lllll1_opy_
    if bstack11l1ll1111_opy_:
      Service.start = bstack1l1l1l11l1_opy_
      Service.stop = bstack1llllllll_opy_
      webdriver.Remote.get = bstack1lll11l1_opy_
      WebDriver.quit = bstack11llll1l_opy_
      webdriver.Remote.__init__ = bstack1ll111ll11_opy_
    if not bstack11ll11l11l_opy_ and not bstack1ll1lllll1_opy_:
        webdriver.Remote.__init__ = bstack1ll1lll111_opy_
    WebDriver.getAccessibilityResults = getAccessibilityResults
    WebDriver.get_accessibility_results = getAccessibilityResults
    WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
    WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
    WebDriver.performScan = perform_scan
    WebDriver.perform_scan = perform_scan
    WebDriver.execute = bstack111l1llll_opy_
    bstack1l111l11l1_opy_ = True
  except Exception as e:
    pass
  try:
    bstack11l1ll1111_opy_ = bstack11ll11l11l_opy_ or bstack1ll1lllll1_opy_
    if bstack11l1ll1111_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1ll1l1111l_opy_
  except Exception as e:
    pass
  bstack11l1l111l1_opy_()
  if not bstack1l111l11l1_opy_:
    bstack11l11ll11l_opy_(bstack11ll111_opy_ (u"ࠦࡕࡧࡣ࡬ࡣࡪࡩࡸࠦ࡮ࡰࡶࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠨഖ"), bstack1111ll11_opy_)
  if bstack1ll11ll1l1_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      if hasattr(RemoteConnection, bstack11ll111_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭ഗ")) and callable(getattr(RemoteConnection, bstack11ll111_opy_ (u"࠭࡟ࡨࡧࡷࡣࡵࡸ࡯ࡹࡻࡢࡹࡷࡲࠧഘ"))):
        RemoteConnection._get_proxy_url = bstack11lll1l1_opy_
      else:
        from selenium.webdriver.remote.client_config import ClientConfig
        ClientConfig.get_proxy_url = bstack11lll1l1_opy_
    except Exception as e:
      logger.error(bstack1lll111111_opy_.format(str(e)))
  if bstack11lll1ll11_opy_():
    bstack1ll1llll11_opy_(CONFIG, logger)
  if (bstack11ll111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ങ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      try:
        from pabot.pabot import QueueItem
        from pabot import pabot
      except Exception as e:
        logger.warning(bstack1l1ll111_opy_ + str(e))
      if not is_robot_playwright_installed():
        try:
          if percy.bstack1lll11ll1l_opy_() == bstack11ll111_opy_ (u"ࠣࡶࡵࡹࡪࠨച"):
            bstack1l111l1l1l_opy_(bstack1lll1lll_opy_)
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
          WebDriverCreator._get_ff_profile = bstack1l1l1ll11_opy_
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
          WebDriverCache.close = bstack111l1l1l1l_opy_
        except Exception as e:
          logger.warning(bstack1ll11l11l_opy_ + str(e))
        try:
          from AppiumLibrary.utils.applicationcache import ApplicationCache
          ApplicationCache.close = bstack11l1l1l1l1_opy_
        except Exception as e:
          logger.debug(bstack1lll11111l_opy_ + str(e))
    except Exception as e:
      bstack11l11ll11l_opy_(e, bstack1ll11l11l_opy_)
    Output.start_test = bstack111lll1l11_opy_
    Output.end_test = bstack1l11ll111_opy_
    TestStatus.__init__ = bstack1lll111l11_opy_
    QueueItem.__init__ = bstack111l11ll1_opy_
    pabot._create_items = bstack1l1l111ll_opy_
    try:
      from pabot import __version__ as bstack1llll1111l_opy_
      if version.parse(bstack1llll1111l_opy_) >= version.parse(bstack11ll111_opy_ (u"ࠩ࠸࠲࠵࠴࠰ࠨഛ")):
        pabot._run = bstack1l11111ll_opy_
      elif version.parse(bstack1llll1111l_opy_) >= version.parse(bstack11ll111_opy_ (u"ࠪ࠸࠳࠸࠮࠱ࠩജ")):
        pabot._run = bstack1llll11111_opy_
      elif version.parse(bstack1llll1111l_opy_) >= version.parse(bstack11ll111_opy_ (u"ࠫ࠷࠴࠱࠶࠰࠳ࠫഝ")):
        pabot._run = bstack1lll1l1ll_opy_
      elif version.parse(bstack1llll1111l_opy_) >= version.parse(bstack11ll111_opy_ (u"ࠬ࠸࠮࠲࠵࠱࠴ࠬഞ")):
        pabot._run = bstack11ll1111l_opy_
      else:
        pabot._run = bstack111l11lll1_opy_
    except Exception as e:
      pabot._run = bstack111l11lll1_opy_
    pabot._create_command_for_execution = bstack11l1lll1l_opy_
    pabot._report_results = bstack1l1ll111ll_opy_
  if bstack11ll111_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ട") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11l11ll11l_opy_(e, bstack1ll111l1_opy_)
    Runner.run_hook = bstack1ll1lll1l_opy_
    try:
      from behave import __version__ as bstack11l1l11l1_opy_
      if version.parse(bstack11l1l11l1_opy_) >= version.parse(bstack11ll111_opy_ (u"ࠧ࠲࠰࠶࠲࠵࠭ഠ")):
        Runner.load_hooks = bstack11ll1111l1_opy_
    except Exception as e:
      logger.debug(bstack11ll111_opy_ (u"ࠨࡅࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡷࡧࡵࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬഡ").format(str(e)))
    Step.run = bstack1ll1llll1l_opy_
  if bstack11ll111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩഢ") in str(framework_name).lower():
    if not bstack11ll11l11l_opy_:
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack111lll11_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack11llllll1_opy_
      Config.getoption = bstack11l11l1l11_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack111lllll1_opy_
    except Exception as e:
      pass
def bstack1llll1l1l_opy_():
  global CONFIG
  if bstack11ll111_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪണ") in CONFIG and int(CONFIG[bstack11ll111_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫത")]) > 1:
    logger.warning(bstack1l11ll11_opy_)
def bstack111llll1_opy_(arg, bstack1ll111l1l1_opy_, bstack1l1l11ll1l_opy_=None):
  global CONFIG
  global bstack11lll111ll_opy_
  global bstack1llll11l1_opy_
  global bstack11ll11l11l_opy_
  global bstack1ll1lllll1_opy_
  global global_config
  bstack1llll1l11_opy_ = bstack11ll111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬഥ")
  if bstack1ll111l1l1_opy_ and isinstance(bstack1ll111l1l1_opy_, str):
    bstack1ll111l1l1_opy_ = eval(bstack1ll111l1l1_opy_)
  CONFIG = bstack1ll111l1l1_opy_[bstack11ll111_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭ദ")]
  bstack11lll111ll_opy_ = bstack1ll111l1l1_opy_[bstack11ll111_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨധ")]
  bstack1llll11l1_opy_ = bstack1ll111l1l1_opy_[bstack11ll111_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪന")]
  bstack11ll11l11l_opy_ = bstack1ll111l1l1_opy_[bstack11ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬഩ")]
  try:
    bstack1llllll11l_opy_ = bstack1ll111l1l1_opy_.get(bstack11ll111_opy_ (u"ࠪࡓ࡛ࡋࡒࡓࡋࡇࡉࡤࡒࡏࡂࡆࡢࡘࡊ࡙ࡔࡊࡐࡊࠫപ"), False)
    bstack1ll1lllll1_opy_ = bool(bstack1llllll11l_opy_)
    os.environ[bstack11ll111_opy_ (u"ࠫࡔ࡜ࡅࡓࡔࡌࡈࡊࡥࡌࡐࡃࡇࡣ࡙ࡋࡓࡕࡋࡑࡋࠬഫ")] = str(bstack1ll1lllll1_opy_).lower()
  except Exception as e:
    logger.error(bstack11ll111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡒ࡚ࡊࡘࡒࡊࡆࡈࡣࡑࡕࡁࡅࡡࡗࡉࡘ࡚ࡉࡏࡉ࠽ࠤࢀࢃࠢബ").format(e))
    bstack1ll1lllll1_opy_ = False
    os.environ[bstack11ll111_opy_ (u"࠭ࡏࡗࡇࡕࡖࡎࡊࡅࡠࡎࡒࡅࡉࡥࡔࡆࡕࡗࡍࡓࡍࠧഭ")] = bstack11ll111_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭മ")
  global_config.bstack111lll11ll_opy_(bstack11ll111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩയ"), bstack11ll11l11l_opy_)
  os.environ[bstack11ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫര")] = bstack1llll1l11_opy_
  os.environ[bstack11ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠩറ")] = json.dumps(CONFIG)
  os.environ[bstack11ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡌ࡚ࡈ࡟ࡖࡔࡏࠫല")] = bstack11lll111ll_opy_
  os.environ[bstack11ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ള")] = str(bstack1llll11l1_opy_)
  os.environ[bstack11ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡌࡖࡉࡌࡒࠬഴ")] = str(True)
  if bstack11lllll111_opy_(arg, [bstack11ll111_opy_ (u"ࠧ࠮ࡰࠪവ"), bstack11ll111_opy_ (u"ࠨ࠯࠰ࡲࡺࡳࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩശ")]) != -1:
    os.environ[bstack11ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡄࡖࡆࡒࡌࡆࡎࠪഷ")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1l1111l11l_opy_)
    return
  bstack111l111111_opy_()
  global bstack1ll111ll1l_opy_
  global bstack1lll1l11_opy_
  global bstack11111ll1l_opy_
  global bstack1lll1ll1ll_opy_
  global bstack1lll1l1l11_opy_
  global bstack1llllll1ll_opy_
  global bstack11lll11ll_opy_
  arg.append(bstack11ll111_opy_ (u"ࠥ࠱࡜ࠨസ"))
  arg.append(bstack11ll111_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨ࠾ࡒࡵࡤࡶ࡮ࡨࠤࡦࡲࡲࡦࡣࡧࡽࠥ࡯࡭ࡱࡱࡵࡸࡪࡪ࠺ࡱࡻࡷࡩࡸࡺ࠮ࡑࡻࡷࡩࡸࡺࡗࡢࡴࡱ࡭ࡳ࡭ࠢഹ"))
  arg.append(bstack11ll111_opy_ (u"ࠧ࠳ࡗࠣഺ"))
  arg.append(bstack11ll111_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡀࡔࡩࡧࠣ࡬ࡴࡵ࡫ࡪ࡯ࡳࡰ഻ࠧ"))
  global bstack11lll1ll_opy_
  global bstack1llll1llll_opy_
  global bstack11l1l1l11_opy_
  global bstack11lll1l11l_opy_
  global bstack11l11ll1_opy_
  global bstack1ll1l1l1ll_opy_
  global bstack1l1111ll1l_opy_
  global bstack11ll11lll_opy_
  global bstack11lll1ll1l_opy_
  global bstack1l11l1l11_opy_
  global bstack111ll1llll_opy_
  global bstack1l111ll1l_opy_
  global bstack1lll11llll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11lll1ll_opy_ = webdriver.Remote.__init__
    bstack1llll1llll_opy_ = WebDriver.quit
    bstack11ll11lll_opy_ = WebDriver.close
    bstack11lll1ll1l_opy_ = WebDriver.get
    bstack11l1l1l11_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1lllll1l11_opy_(CONFIG) and bstack1lllll11l_opy_():
    if bstack1ll1lll11_opy_() < version.parse(bstack11lll1l1l_opy_):
      logger.error(bstack1ll111llll_opy_.format(bstack1ll1lll11_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack11ll111_opy_ (u"ࠧࡠࡩࡨࡸࡤࡶࡲࡰࡺࡼࡣࡺࡸ࡬ࠨ഼")) and callable(getattr(RemoteConnection, bstack11ll111_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩഽ"))):
          bstack1l11l1l11_opy_ = RemoteConnection._get_proxy_url
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          bstack1l11l1l11_opy_ = ClientConfig.get_proxy_url
      except Exception as e:
        logger.error(bstack1lll111111_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack111ll1llll_opy_ = Config.getoption
    from _pytest import runner
    bstack1l111ll1l_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warning(bstack11ll111_opy_ (u"ࠤࠨࡷ࠿ࠦࠥࡴࠤാ"), bstack11l1ll1ll1_opy_, str(e))
  try:
    from pytest_bdd import reporting
    bstack1lll11llll_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack11ll111_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡲࠤࡷࡻ࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࡶࠫി"))
  if cli.is_enabled(CONFIG) and cli.config:
    bstack11111ll1l_opy_ = cli.config.get(bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨീ"), {}).get(bstack11ll111_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧു"))
  else:
    bstack11111ll1l_opy_ = CONFIG.get(bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪൂ"), {}).get(bstack11ll111_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩൃ"))
  bstack11lll11ll_opy_ = True
  if cli.is_enabled(CONFIG):
    if cli.bstack1l11l1111_opy_():
      bstack111l1llll1_opy_.invoke(bstack1l11lll1ll_opy_.CONNECT, bstack11ll1l11l1_opy_())
    platform_index = int(os.environ.get(bstack11ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨൄ"), bstack11ll111_opy_ (u"ࠩ࠳ࠫ൅")))
  else:
    bstack1l1ll111l1_opy_(bstack1ll1l1ll11_opy_)
  os.environ[bstack11ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫെ")] = CONFIG[bstack11ll111_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭േ")]
  os.environ[bstack11ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨൈ")] = CONFIG[bstack11ll111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ൉")]
  os.environ[bstack11ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪൊ")] = bstack11ll11l11l_opy_.__str__()
  from _pytest.config import main as bstack11ll1l1ll1_opy_
  bstack1ll11l11ll_opy_ = []
  try:
    exit_code = bstack11ll1l1ll1_opy_(arg)
    if cli.is_enabled(CONFIG):
      cli.bstack1l1lll1ll_opy_()
    if bstack11ll111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬോ") in multiprocessing.current_process().__dict__.keys():
      for bstack11l1ll1l1l_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1ll11l11ll_opy_.append(bstack11l1ll1l1l_opy_)
    try:
      bstack11l1llll_opy_ = (bstack1ll11l11ll_opy_, int(exit_code))
      bstack1l1l11ll1l_opy_.append(bstack11l1llll_opy_)
    except:
      bstack1l1l11ll1l_opy_.append((bstack1ll11l11ll_opy_, exit_code))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack1ll11l11ll_opy_.append({bstack11ll111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧൌ"): bstack11ll111_opy_ (u"ࠪࡔࡷࡵࡣࡦࡵࡶࠤ്ࠬ") + os.environ.get(bstack11ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫൎ")), bstack11ll111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ൏"): traceback.format_exc(), bstack11ll111_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ൐"): int(os.environ.get(bstack11ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ൑")))})
    bstack1l1l11ll1l_opy_.append((bstack1ll11l11ll_opy_, 1))
def mod_behave_main(args, retries):
  try:
    from behave.configuration import Configuration
    from behave.__main__ import run_behave
    from browserstack_sdk.bstack_behave_runner import BehaveRunner
    config = Configuration(args)
    config.update_userdata({bstack11ll111_opy_ (u"ࠣࡴࡨࡸࡷ࡯ࡥࡴࠤ൒"): str(retries)})
    return run_behave(config, runner_class=BehaveRunner)
  except Exception as e:
    bstack1ll1l1111_opy_ = e.__class__.__name__
    print(bstack11ll111_opy_ (u"ࠤࠨࡷ࠿ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡢࡦࡪࡤࡺࡪࠦࡴࡦࡵࡷࠤࠪࡹࠢ൓") % (bstack1ll1l1111_opy_, e))
    return 1
def bstack1lll11lll1_opy_(arg):
  global bstack11ll1ll1ll_opy_
  bstack1l1ll111l1_opy_(bstack1l1l1lll_opy_)
  os.environ[bstack11ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫൔ")] = str(bstack1llll11l1_opy_)
  retries = bstack1111lll11_opy_.bstack11llllll_opy_(CONFIG)
  status_code = 0
  if bstack1111lll11_opy_.bstack111ll11111_opy_(CONFIG):
    status_code = mod_behave_main(arg, retries)
  else:
    from behave.__main__ import main as bstack1l11l1ll1l_opy_
    status_code = bstack1l11l1ll1l_opy_(arg)
  if status_code != 0:
    bstack11ll1ll1ll_opy_ = status_code
def bstack1l111ll1l1_opy_():
  logger.info(bstack1l111l1111_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack11ll111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪൕ"), help=bstack11ll111_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡣࡰࡰࡩ࡭࡬࠭ൖ"))
  parser.add_argument(bstack11ll111_opy_ (u"࠭࠭ࡶࠩൗ"), bstack11ll111_opy_ (u"ࠧ࠮࠯ࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫ൘"), help=bstack11ll111_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠧ൙"))
  parser.add_argument(bstack11ll111_opy_ (u"ࠩ࠰࡯ࠬ൚"), bstack11ll111_opy_ (u"ࠪ࠱࠲ࡱࡥࡺࠩ൛"), help=bstack11ll111_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡣࡦࡧࡪࡹࡳࠡ࡭ࡨࡽࠬ൜"))
  parser.add_argument(bstack11ll111_opy_ (u"ࠬ࠳ࡦࠨ൝"), bstack11ll111_opy_ (u"࠭࠭࠮ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ൞"), help=bstack11ll111_opy_ (u"࡚ࠧࡱࡸࡶࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ൟ"))
  bstack1l1l11lll1_opy_ = parser.parse_args()
  try:
    bstack11l1ll1l11_opy_ = bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡨࡧࡱࡩࡷ࡯ࡣ࠯ࡻࡰࡰ࠳ࡹࡡ࡮ࡲ࡯ࡩࠬൠ")
    if bstack1l1l11lll1_opy_.framework and bstack1l1l11lll1_opy_.framework not in (bstack11ll111_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩൡ"), bstack11ll111_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫൢ")):
      bstack11l1ll1l11_opy_ = bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠴ࡹ࡮࡮࠱ࡷࡦࡳࡰ࡭ࡧࠪൣ")
    bstack1l1ll11ll_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11l1ll1l11_opy_)
    bstack1lll111l_opy_ = open(bstack1l1ll11ll_opy_, bstack11ll111_opy_ (u"ࠬࡸࠧ൤"))
    bstack1l1l1l1111_opy_ = bstack1lll111l_opy_.read()
    bstack1lll111l_opy_.close()
    if bstack1l1l11lll1_opy_.username:
      bstack1l1l1l1111_opy_ = bstack1l1l1l1111_opy_.replace(bstack11ll111_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭൥"), bstack1l1l11lll1_opy_.username)
    if bstack1l1l11lll1_opy_.key:
      bstack1l1l1l1111_opy_ = bstack1l1l1l1111_opy_.replace(bstack11ll111_opy_ (u"࡚ࠧࡑࡘࡖࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩ൦"), bstack1l1l11lll1_opy_.key)
    if bstack1l1l11lll1_opy_.framework:
      bstack1l1l1l1111_opy_ = bstack1l1l1l1111_opy_.replace(bstack11ll111_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩ൧"), bstack1l1l11lll1_opy_.framework)
    file_name = bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬ൨")
    file_path = os.path.abspath(file_name)
    bstack1llll1l1_opy_ = open(file_path, bstack11ll111_opy_ (u"ࠪࡻࠬ൩"))
    bstack1llll1l1_opy_.write(bstack1l1l1l1111_opy_)
    bstack1llll1l1_opy_.close()
    logger.info(bstack1l11l1ll_opy_)
    try:
      os.environ[bstack11ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭൪")] = bstack1l1l11lll1_opy_.framework if bstack1l1l11lll1_opy_.framework != None else bstack11ll111_opy_ (u"ࠧࠨ൫")
      config = yaml.safe_load(bstack1l1l1l1111_opy_)
      config[bstack11ll111_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭൬")] = bstack11ll111_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡴࡧࡷࡹࡵ࠭൭")
      bstack1l1l11llll_opy_(bstack1ll1l1ll1_opy_, config)
    except Exception as e:
      logger.debug(bstack11lllll11_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack11l11l1ll_opy_.format(str(e)))
def bstack1l1l11llll_opy_(bstack11l1l1llll_opy_, config, bstack1lllllllll_opy_={}):
  global bstack11ll11l11l_opy_
  global bstack1l11lll1_opy_
  global global_config
  if not config:
    return
  bstack1l1ll1ll1_opy_ = bstack111ll1ll11_opy_ if not bstack11ll11l11l_opy_ else (
    bstack11llll11l1_opy_ if bstack11ll111_opy_ (u"ࠨࡣࡳࡴࠬ൮") in config else (
        bstack111ll1l1ll_opy_ if config.get(bstack11ll111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭൯")) else bstack1l1l11l11l_opy_
    )
)
  bstack11lllll11l_opy_ = False
  bstack1l1l1lllll_opy_ = False
  if bstack11ll11l11l_opy_ is True:
      if bstack11ll111_opy_ (u"ࠪࡥࡵࡶࠧ൰") in config:
          bstack11lllll11l_opy_ = True
      else:
          bstack1l1l1lllll_opy_ = True
  bstack1l11l1l1ll_opy_ = bstack111llll11l_opy_.bstack1l1ll1lll_opy_(config, bstack1l11lll1_opy_)
  bstack1ll1l11111_opy_ = bstack1ll1l1l1_opy_()
  data = {
    bstack11ll111_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭൱"): config[bstack11ll111_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ൲")],
    bstack11ll111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ൳"): config[bstack11ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ൴")],
    bstack11ll111_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ൵"): bstack11l1l1llll_opy_,
    bstack11ll111_opy_ (u"ࠩࡧࡩࡹ࡫ࡣࡵࡧࡧࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭൶"): os.environ.get(bstack11ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬ൷"), bstack1l11lll1_opy_),
    bstack11ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭൸"): bstack11l11l1l1_opy_,
    bstack11ll111_opy_ (u"ࠬࡵࡰࡵ࡫ࡰࡥࡱࡥࡨࡶࡤࡢࡹࡷࡲࠧ൹"): bstack11lllll1l1_opy_(),
    bstack11ll111_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩൺ"): {
      bstack11ll111_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬൻ"): str(config[bstack11ll111_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨർ")]) if bstack11ll111_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩൽ") in config else bstack11ll111_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦൾ"),
      bstack11ll111_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ൿ"): sys.version,
      bstack11ll111_opy_ (u"ࠬࡸࡥࡧࡧࡵࡶࡪࡸࠧ඀"): bstack1lll111ll_opy_(os.environ.get(bstack11ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨඁ"), bstack1l11lll1_opy_)),
      bstack11ll111_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩං"): bstack11ll111_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨඃ"),
      bstack11ll111_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪ඄"): bstack1l1ll1ll1_opy_,
      bstack11ll111_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨඅ"): bstack1l11l1l1ll_opy_,
      bstack11ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡪࡸࡦࡤࡻࡵࡪࡦࠪආ"): os.environ[bstack11ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪඇ")],
      bstack11ll111_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩඈ"): os.environ.get(bstack11ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩඉ"), bstack1l11lll1_opy_),
      bstack11ll111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫඊ"): bstack11l1l11lll_opy_(os.environ.get(bstack11ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫඋ"), bstack1l11lll1_opy_)),
      bstack11ll111_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩඌ"): bstack1ll1l11111_opy_.get(bstack11ll111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩඍ")),
      bstack11ll111_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫඎ"): bstack1ll1l11111_opy_.get(bstack11ll111_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧඏ")),
      bstack11ll111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪඐ"): config[bstack11ll111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫඑ")] if config[bstack11ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬඒ")] else bstack11ll111_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦඓ"),
      bstack11ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ඔ"): str(config[bstack11ll111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧඕ")]) if bstack11ll111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨඖ") in config else bstack11ll111_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣ඗"),
      bstack11ll111_opy_ (u"ࠨࡱࡶࠫ඘"): sys.platform,
      bstack11ll111_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫ඙"): socket.gethostname(),
      bstack11ll111_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࠬක"): global_config.get_property(bstack11ll111_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭ඛ"))
    }
  }
  if not global_config.get_property(bstack11ll111_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬග")) is None:
    data[bstack11ll111_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩඝ")][bstack11ll111_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡏࡨࡸࡦࡪࡡࡵࡣࠪඞ")] = {
      bstack11ll111_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨඟ"): bstack11ll111_opy_ (u"ࠩࡸࡷࡪࡸ࡟࡬࡫࡯ࡰࡪࡪࠧච"),
      bstack11ll111_opy_ (u"ࠪࡷ࡮࡭࡮ࡢ࡮ࠪඡ"): global_config.get_property(bstack11ll111_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡘ࡯ࡧ࡯ࡣ࡯ࠫජ")),
      bstack11ll111_opy_ (u"ࠬࡹࡩࡨࡰࡤࡰࡓࡻ࡭ࡣࡧࡵࠫඣ"): global_config.get_property(bstack11ll111_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡎࡰࠩඤ"))
    }
  if bstack11l1l1llll_opy_ == bstack11lll1l1l1_opy_:
    data[bstack11ll111_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪඥ")][bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡃࡰࡰࡩ࡭࡬࠭ඦ")] = bstack1l111lllll_opy_(config)
    data[bstack11ll111_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬට")][bstack11ll111_opy_ (u"ࠪ࡭ࡸࡖࡥࡳࡥࡼࡅࡺࡺ࡯ࡆࡰࡤࡦࡱ࡫ࡤࠨඨ")] = percy.bstack111ll1lll_opy_
    data[bstack11ll111_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧඩ")][bstack11ll111_opy_ (u"ࠬࡶࡥࡳࡥࡼࡆࡺ࡯࡬ࡥࡋࡧࠫඪ")] = percy.percy_build_id
  if not bstack1111lll11_opy_.bstack11l1l1lll1_opy_(CONFIG):
    data[bstack11ll111_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩණ")][bstack11ll111_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠫඬ")] = bstack1111lll11_opy_.bstack11l1l1lll1_opy_(CONFIG)
  bstack1l111llll_opy_ = bstack1llll1lll1_opy_.get_instance(CONFIG, logger)
  bstack1lllll111l_opy_ = bstack1111lll11_opy_.get_instance(config=CONFIG)
  if bstack1l111llll_opy_ is not None and bstack1lllll111l_opy_ is not None and bstack1lllll111l_opy_.bstack11l1ll1l_opy_():
    data[bstack11ll111_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫත")][bstack1lllll111l_opy_.bstack1l11111l11_opy_()] = bstack1l111llll_opy_.bstack111l11ll1l_opy_()
  update(data[bstack11ll111_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬථ")], bstack1lllllllll_opy_)
  try:
    response = bstack1l1l11ll_opy_(bstack11ll111_opy_ (u"ࠪࡔࡔ࡙ࡔࠨද"), bstack1l1l1111ll_opy_(bstack1l1l11l111_opy_), data, {
      bstack11ll111_opy_ (u"ࠫࡦࡻࡴࡩࠩධ"): (config[bstack11ll111_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧන")], config[bstack11ll111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ඲")])
    })
    if response:
      logger.debug(bstack11l11111ll_opy_.format(bstack11l1l1llll_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1lll11111_opy_.format(str(e)))
def bstack1lll111ll_opy_(framework):
  return bstack11ll111_opy_ (u"ࠢࡼࡿ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࡽࢀࠦඳ").format(str(framework), __version__) if framework else bstack11ll111_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࡻࡾࠤප").format(
    __version__)
def bstack111l111111_opy_():
  global CONFIG
  global bstack1l11l1l1_opy_
  if bool(CONFIG):
    return
  try:
    bstack1l1111l1l1_opy_()
    logger.debug(bstack11l11l1111_opy_.format(str(CONFIG)))
    bstack1l11l1l1_opy_ = logger_utils.configure_logger(CONFIG, bstack1l11l1l1_opy_)
    bstack111l1111l_opy_()
  except Exception as e:
    logger.error(bstack11ll111_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࡷࡳ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࠨඵ") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1l1l1l1l1_opy_
  atexit.register(bstack1l11l11lll_opy_)
  signal.signal(signal.SIGINT, bstack11l1l11111_opy_)
  signal.signal(signal.SIGTERM, bstack11l1l11111_opy_)
def bstack1l1l1l1l1_opy_(exctype, value, traceback):
  global bstack1llllllll1_opy_
  try:
    for driver in bstack1llllllll1_opy_:
      bstack1l11l1ll11_opy_(driver, bstack11ll111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪබ"), bstack11ll111_opy_ (u"ࠦࡘ࡫ࡳࡴ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢභ") + str(value))
  except Exception:
    pass
  logger.info(bstack1lll1111ll_opy_)
  bstack1l1l111l1l_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1l1l111l1l_opy_(message=bstack11ll111_opy_ (u"ࠬ࠭ම"), bstack1l1l1l111_opy_ = False):
  global CONFIG
  bstack11111l1l_opy_ = bstack11ll111_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠨඹ") if bstack1l1l1l111_opy_ else bstack11ll111_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ය")
  bstack1lll1ll1_opy_ = bstack1111l1l1l_opy_.bstack1ll111l11_opy_(EVENTS.bstack1ll1llllll_opy_)
  try:
    if message:
      bstack1lllllllll_opy_ = {
        bstack11111l1l_opy_ : str(message)
      }
      try:
        bstack1l1l11llll_opy_(bstack11lll1l1l1_opy_, CONFIG, bstack1lllllllll_opy_)
      finally:
        bstack1111l1l1l_opy_.end(EVENTS.bstack1ll1llllll_opy_.value, bstack1lll1ll1_opy_ + bstack11ll111_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣර"), bstack1lll1ll1_opy_ + bstack11ll111_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ඼"), status=True, failure=None, test_name=None)
    else:
      try:
        bstack1l1l11llll_opy_(bstack11lll1l1l1_opy_, CONFIG)
      finally:
        bstack1111l1l1l_opy_.end(EVENTS.bstack1ll1llllll_opy_.value, bstack1lll1ll1_opy_ + bstack11ll111_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥල"), bstack1lll1ll1_opy_ + bstack11ll111_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ඾"), status=True, failure=None, test_name=None)
  except Exception as e:
    logger.debug(bstack111l1l1ll_opy_.format(str(e)))
def bstack111llllll1_opy_(bstack1l1llll111_opy_, size):
  bstack1111llll1_opy_ = []
  while len(bstack1l1llll111_opy_) > size:
    bstack1ll1ll11_opy_ = bstack1l1llll111_opy_[:size]
    bstack1111llll1_opy_.append(bstack1ll1ll11_opy_)
    bstack1l1llll111_opy_ = bstack1l1llll111_opy_[size:]
  bstack1111llll1_opy_.append(bstack1l1llll111_opy_)
  return bstack1111llll1_opy_
def bstack1lll1ll111_opy_(args):
  if bstack11ll111_opy_ (u"ࠬ࠳࡭ࠨ඿") in args and bstack11ll111_opy_ (u"࠭ࡰࡥࡤࠪව") in args:
    return True
  return False
@measure(event_name=EVENTS.bstack1l1lll1l_opy_, stage=STAGE.bstack11ll1ll11l_opy_)
def run_on_browserstack(bstack11111111_opy_=None, bstack1l1l11ll1l_opy_=None, bstack1111l111_opy_=False):
  global CONFIG
  global bstack11lll111ll_opy_
  global bstack1llll11l1_opy_
  global bstack1l11lll1_opy_
  global global_config
  bstack1llll1l11_opy_ = bstack11ll111_opy_ (u"ࠧࠨශ")
  bstack1111ll1ll_opy_ = bstack11ll111_opy_ (u"ࠣࠤෂ")
  bstack11ll1111_opy_(bstack11ll1l1l1l_opy_, logger)
  if bstack11111111_opy_ and isinstance(bstack11111111_opy_, str):
    bstack11111111_opy_ = eval(bstack11111111_opy_)
  if bstack11111111_opy_:
    CONFIG = bstack11111111_opy_[bstack11ll111_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩස")]
    bstack11lll111ll_opy_ = bstack11111111_opy_[bstack11ll111_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫහ")]
    bstack1llll11l1_opy_ = bstack11111111_opy_[bstack11ll111_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ළ")]
    global_config.bstack111lll11ll_opy_(bstack11ll111_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧෆ"), bstack1llll11l1_opy_)
    bstack1llll1l11_opy_ = bstack11ll111_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡧࡦࡰࡨࡶ࡮ࡩࠧ෇")
  global_config.bstack111lll11ll_opy_(bstack11ll111_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥࠩ෈"), uuid4().__str__())
  logger.info(bstack11ll111_opy_ (u"ࠨࡕࡇࡏࠥࡸࡵ࡯ࠢࡶࡸࡦࡸࡴࡦࡦࠣࡻ࡮ࡺࡨࠡ࡫ࡧ࠾ࠥ࠭෉") + global_config.get_property(bstack11ll111_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧ්ࠫ")));
  logger.debug(bstack11ll111_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࡂ࠭෋") + global_config.get_property(bstack11ll111_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭෌")))
  if not bstack1111l111_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1l1111l11l_opy_)
      return
    if sys.argv[1] == bstack11ll111_opy_ (u"ࠬ࠳࠭ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ෍") or sys.argv[1] == bstack11ll111_opy_ (u"࠭࠭ࡷࠩ෎"):
      logger.info(bstack11ll111_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡐࡺࡶ࡫ࡳࡳࠦࡓࡅࡍࠣࡺࢀࢃࠧා").format(__version__))
      return
    if sys.argv[1] == bstack11ll111_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧැ"):
      bstack1l111ll1l1_opy_()
      return
    if sys.argv[1] == bstack11ll111_opy_ (u"ࠩ࡯ࡳࡦࡪࠧෑ"):
      from browserstack_sdk.bstack1111l1lll_opy_ import bstack1ll11111ll_opy_
      bstack111l111111_opy_()
      bstack1ll11111ll_opy_(CONFIG)
      return
  args = sys.argv
  bstack111l111111_opy_()
  global bstack1ll1lllll1_opy_
  try:
    from bstack_utils import constants as bstack11111llll_opy_
    override_value = CONFIG.get(bstack11ll111_opy_ (u"ࠪࡳࡻ࡫ࡲࡳ࡫ࡧࡩࡑࡵࡡࡥࡖࡨࡷࡹ࡯࡮ࡨࠩි"), False)
    bstack1ll1lllll1_opy_ = bool(override_value)
  except Exception as e:
    logger.error(bstack11ll111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡑ࡙ࡉࡗࡘࡉࡅࡇࡢࡐࡔࡇࡄࡠࡖࡈࡗ࡙ࡏࡎࡈ࠼ࠣࡿࢂࠨී").format(e))
    bstack1ll1lllll1_opy_ = False
  if bstack1ll1lllll1_opy_:
    bstack111l1lll1_opy_ = CONFIG.get(bstack11ll111_opy_ (u"ࠬࡲ࡯ࡢࡦࡗࡩࡸࡺࡩ࡯ࡩࡋࡹࡧ࡛ࡒࡍࠩු")) or bstack11111llll_opy_.bstack1llllll1l1_opy_
    logger.info(bstack11ll111_opy_ (u"ࠨࡇ࡭ࡱࡥࡥࡱࠦ࡯ࡷࡧࡵࡶ࡮ࡪࡥ࡭ࡱࡤࡨࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡫࡮ࡢࡤ࡯ࡩࡩ࠲ࠠࡶࡵ࡬ࡲ࡬ࠦࡨࡶࡤ࠽ࠤࢀࢃࠢ෕").format(bstack111l1lll1_opy_))
    bstack11lll111ll_opy_ = bstack111l1lll1_opy_
    try:
      bstack11111llll_opy_.HTTPS_HUB = bstack111l1lll1_opy_
      bstack11111llll_opy_.bstack1l11l11l11_opy_ = bstack111l1lll1_opy_
    except Exception:
      pass
  global bstack1ll111ll1l_opy_
  global bstack1111l11ll_opy_
  global bstack11lll11ll_opy_
  global bstack111ll1l11l_opy_
  global bstack1lll1l11_opy_
  global bstack11111ll1l_opy_
  global bstack1lll1ll1ll_opy_
  global bstack1l111l1ll1_opy_
  global bstack1lll1l1l11_opy_
  global bstack1llllll1ll_opy_
  global bstack11l1111lll_opy_
  bstack1111l11ll_opy_ = len(CONFIG.get(bstack11ll111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪූ"), []))
  if not bstack1llll1l11_opy_:
    if args[1] == bstack11ll111_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ෗") or args[1] == bstack11ll111_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪෘ") or args[1] == bstack11ll111_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠫෙ"):
      bstack1llll1l11_opy_ = bstack11ll111_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠬේ")
      args = args[2:]
    elif args[1] == bstack11ll111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫෛ"):
      bstack1llll1l11_opy_ = bstack11ll111_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬො")
      args = args[2:]
    elif args[1] == bstack11ll111_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ෝ"):
      bstack1llll1l11_opy_ = bstack11ll111_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧෞ")
      args = args[2:]
    elif args[1] == bstack11ll111_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪෟ"):
      bstack1llll1l11_opy_ = bstack11ll111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ෠")
      args = args[2:]
    elif args[1] == bstack11ll111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ෡"):
      bstack1llll1l11_opy_ = bstack11ll111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ෢")
      args = args[2:]
    elif args[1] == bstack11ll111_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭෣"):
      bstack1llll1l11_opy_ = bstack11ll111_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ෤")
      args = args[2:]
    else:
      if not bstack11ll111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ෥") in CONFIG or str(CONFIG[bstack11ll111_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ෦")]).lower() in [bstack11ll111_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ෧"), bstack11ll111_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬ෨"), bstack11ll111_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨ࠭෩")]:
        bstack1llll1l11_opy_ = bstack11ll111_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡧࡦࡰࡨࡶ࡮ࡩࠧ෪")
        args = args[1:]
      elif str(CONFIG[bstack11ll111_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ෫")]).lower() == bstack11ll111_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ෬"):
        bstack1llll1l11_opy_ = bstack11ll111_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ෭")
        args = args[1:]
      elif str(CONFIG[bstack11ll111_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭෮")]).lower() == bstack11ll111_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ෯"):
        bstack1llll1l11_opy_ = bstack11ll111_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ෰")
        args = args[1:]
      elif str(CONFIG[bstack11ll111_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ෱")]).lower() == bstack11ll111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧෲ"):
        bstack1llll1l11_opy_ = bstack11ll111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨෳ")
        args = args[1:]
      elif str(CONFIG[bstack11ll111_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ෴")]).lower() == bstack11ll111_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ෵"):
        bstack1llll1l11_opy_ = bstack11ll111_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ෶")
        args = args[1:]
      else:
        os.environ[bstack11ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ෷")] = bstack1llll1l11_opy_
        bstack1l1ll11111_opy_(bstack1ll111ll_opy_)
  os.environ[bstack11ll111_opy_ (u"࠭ࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࡡࡘࡗࡊࡊࠧ෸")] = bstack1llll1l11_opy_
  bstack1l11lll1_opy_ = bstack1llll1l11_opy_
  if cli.is_enabled(CONFIG):
    try:
      bstack1l11l1111l_opy_ = bstack1lll1l1lll_opy_[bstack11ll111_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࠭ࡃࡆࡇࠫ෹")] if bstack1llll1l11_opy_ == bstack11ll111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ෺") and bstack111l1lll_opy_() else bstack1llll1l11_opy_
      bstack111l1llll1_opy_.invoke(bstack1l11lll1ll_opy_.bstack11ll111l11_opy_, bstack1l11l111l_opy_(
        sdk_version=__version__,
        path_config=bstack1l1ll1l1_opy_(),
        path_project=os.getcwd(),
        test_framework=bstack1l11l1111l_opy_,
        frameworks=[bstack1l11l1111l_opy_],
        framework_versions={
          bstack1l11l1111l_opy_: bstack11l1l11lll_opy_(bstack11ll111_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨ෻") if bstack1llll1l11_opy_ in [bstack11ll111_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ෼"), bstack11ll111_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ෽"), bstack11ll111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭෾")] else bstack1llll1l11_opy_)
        },
        bs_config=CONFIG
      ))
      if cli.config and cli.config.get(bstack11ll111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣ෿"), None):
        CONFIG[bstack11ll111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤ฀")] = cli.config.get(bstack11ll111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠥก"), None)
    except Exception as e:
      bstack111l1llll1_opy_.invoke(bstack1l11lll1ll_opy_.bstack1ll1ll1ll_opy_, e.__traceback__, 1)
    if bstack1llll11l1_opy_:
      CONFIG[bstack11ll111_opy_ (u"ࠤࡤࡴࡵࠨข")] = cli.config[bstack11ll111_opy_ (u"ࠥࡥࡵࡶࠢฃ")]
      logger.info(bstack11l1l111ll_opy_.format(CONFIG[bstack11ll111_opy_ (u"ࠫࡦࡶࡰࠨค")]))
  else:
    bstack111l1llll1_opy_.clear()
  global bstack11ll1l1111_opy_
  global bstack1ll1l11lll_opy_
  if bstack11111111_opy_:
    try:
      bstack11lll11111_opy_ = datetime.datetime.now()
      os.environ[bstack11ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧฅ")] = bstack1llll1l11_opy_
      bstack111l11l1l_opy_ = bstack1111l1l1l_opy_.bstack1ll111l11_opy_(EVENTS.bstack1lll1lll1l_opy_)
      try:
        logger.info(bstack11ll111_opy_ (u"ࠨࡓࡦࡰࡧ࡭ࡳ࡭ࠠࡔࡆࡎࠤ࡙࡫ࡳࡵࠢࡄࡸࡹ࡫࡭ࡱࡶࡨࡨࠥ࡫ࡶࡦࡰࡷࠦฆ"))
        bstack1l1l11llll_opy_(bstack111111lll_opy_, CONFIG)
      finally:
        bstack1111l1l1l_opy_.end(EVENTS.bstack1lll1lll1l_opy_.value, bstack111l11l1l_opy_ + bstack11ll111_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢง"), bstack111l11l1l_opy_ + bstack11ll111_opy_ (u"ࠣ࠼ࡨࡲࡩࠨจ"), status=True, failure=None, test_name=None)
      cli.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺ࡴࡦ࡮ࡣࡹ࡫ࡳࡵࡡࡤࡸࡹ࡫࡭ࡱࡶࡨࡨࠧฉ"), datetime.datetime.now() - bstack11lll11111_opy_)
    except Exception as e:
      logger.debug(bstack1lll11l11l_opy_.format(str(e)))
  global bstack11lll1ll_opy_
  global bstack1llll1llll_opy_
  global bstack11ll1lll1_opy_
  global bstack11llll11l_opy_
  global bstack11lll1lll_opy_
  global bstack1ll1l1l11l_opy_
  global bstack11lll1l11l_opy_
  global bstack11l11ll1_opy_
  global bstack111ll11ll1_opy_
  global bstack1ll1l1l1ll_opy_
  global bstack1l1111ll1l_opy_
  global bstack11ll11lll_opy_
  global bstack111l11l1ll_opy_
  global bstack111l1111_opy_
  global bstack11l11ll111_opy_
  global bstack11lll1ll1l_opy_
  global bstack1l11l1l11_opy_
  global bstack111ll1llll_opy_
  global bstack1l111ll1l_opy_
  global bstack1l11ll1l_opy_
  global bstack1lll11llll_opy_
  global bstack11l1l1l11_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11lll1ll_opy_ = webdriver.Remote.__init__
    bstack1llll1llll_opy_ = WebDriver.quit
    bstack11ll11lll_opy_ = WebDriver.close
    bstack11lll1ll1l_opy_ = WebDriver.get
    bstack11l1l1l11_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack11ll1l1111_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack1l1l111l_opy_
    bstack1ll1l11lll_opy_ = bstack1l1l111l_opy_()
  except Exception as e:
    pass
  try:
    global bstack111ll11l_opy_
    from QWeb.keywords import browser
    bstack111ll11l_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1lllll1l11_opy_(CONFIG) and bstack1lllll11l_opy_():
    if bstack1ll1lll11_opy_() < version.parse(bstack11lll1l1l_opy_):
      logger.error(bstack1ll111llll_opy_.format(bstack1ll1lll11_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack11ll111_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫช")) and callable(getattr(RemoteConnection, bstack11ll111_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬซ"))):
          RemoteConnection._get_proxy_url = bstack11lll1l1_opy_
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          ClientConfig.get_proxy_url = bstack11lll1l1_opy_
      except Exception as e:
        logger.error(bstack1lll111111_opy_.format(str(e)))
  if not CONFIG.get(bstack11ll111_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧฌ"), False) and not bstack11111111_opy_:
    logger.info(bstack11l1111l_opy_)
  bstack1ll1l111l_opy_ = not cli.is_enabled(CONFIG) and bstack1llll1l11_opy_ not in [bstack11ll111_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧญ")]
  bstack11llll111l_opy_ = bstack1ll1l111l_opy_ and bstack11ll111_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫฎ") in CONFIG and str(CONFIG[bstack11ll111_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬฏ")]).lower() != bstack11ll111_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨฐ")
  bstack111l1lllll_opy_ = bstack1ll1l111l_opy_ and not bstack11llll111l_opy_ and (bstack1llll1l11_opy_ != bstack11ll111_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠫฑ") or (bstack1llll1l11_opy_ == bstack11ll111_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠬฒ") and not bstack11111111_opy_))
  if bstack1llll1l11_opy_ not in [bstack11ll111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ณ")]:
    bstack11ll1111_opy_(os.path.join(os.getcwd(), bstack11ll111_opy_ (u"࠭࡬ࡰࡩࠪด"), bstack11ll111_opy_ (u"ࠧ࡬ࡧࡼ࠱ࡲ࡫ࡴࡳ࡫ࡦࡷ࠳ࡰࡳࡰࡰࠪต")), logger)
  if (bstack1llll1l11_opy_ in [bstack11ll111_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧถ"), bstack11ll111_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨท"), bstack11ll111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫธ")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      try:
        from pabot.pabot import QueueItem
        from pabot import pabot
      except Exception as e:
        logger.warning(bstack1l1ll111_opy_ + str(e))
      if not is_robot_playwright_installed():
        try:
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
          WebDriverCreator._get_ff_profile = bstack1l1l1ll11_opy_
          bstack1ll1l1l11l_opy_ = WebDriverCache.close
        except Exception as e:
          logger.warning(bstack1ll11l11l_opy_ + str(e))
        try:
          from AppiumLibrary.utils.applicationcache import ApplicationCache
          bstack11lll1lll_opy_ = ApplicationCache.close
        except Exception as e:
          logger.debug(bstack1lll11111l_opy_ + str(e))
    except Exception as e:
      bstack11l11ll11l_opy_(e, bstack1ll11l11l_opy_)
    if bstack1llll1l11_opy_ != bstack11ll111_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬน"):
      bstack1ll1ll1l_opy_()
    bstack11ll1lll1_opy_ = Output.start_test
    bstack11llll11l_opy_ = Output.end_test
    bstack11lll1l11l_opy_ = TestStatus.__init__
    bstack111ll11ll1_opy_ = pabot._run
    bstack1ll1l1l1ll_opy_ = QueueItem.__init__
    bstack1l1111ll1l_opy_ = pabot._create_command_for_execution
    bstack1l11ll1l_opy_ = pabot._report_results
  if bstack1llll1l11_opy_ == bstack11ll111_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬบ"):
    global bstack1l1ll11l1_opy_
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11l11ll11l_opy_(e, bstack1ll111l1_opy_)
    bstack111l11l1ll_opy_ = Runner.run_hook
    bstack111l1111_opy_ = Runner.load_hooks
    bstack11l11ll111_opy_ = Step.run
    try:
      sig = inspect.signature(bstack111l11l1ll_opy_)
      params = list(sig.parameters.keys())
      bstack1l1ll11l1_opy_ = bstack11ll111_opy_ (u"࠭ࡣࡰࡰࡷࡩࡽࡺࠧป") in params
      logger.info(bstack11ll111_opy_ (u"ࠧࡅࡧࡷࡩࡨࡺࡥࡥࠢࡥࡩ࡭ࡧࡶࡦࠢࡵࡹࡳࡥࡨࡰࡱ࡮ࠤࡸ࡯ࡧ࡯ࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫผ").format(bstack11ll111_opy_ (u"ࠨ࠳࠱࠶࠳࠼ࠠࠩࡹ࡬ࡸ࡭ࠦࡣࡰࡰࡷࡩࡽࡺࠩࠨฝ") if bstack1l1ll11l1_opy_ else bstack11ll111_opy_ (u"ࠩ࠴࠲࠸࠱ࠠࠩࡹ࡬ࡸ࡭ࡵࡵࡵࠢࡦࡳࡳࡺࡥࡹࡶࠬࠫพ")))
    except Exception as e:
      logger.debug(bstack11ll111_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡧࡹࠦࡢࡦࡪࡤࡺࡪࠦࡲࡶࡰࡢ࡬ࡴࡵ࡫ࠡࡵ࡬࡫ࡳࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨฟ").format(str(e)))
      bstack1l1ll11l1_opy_ = None
  if bstack1llll1l11_opy_ == bstack11ll111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫภ"):
    try:
      from _pytest.config import Config
      bstack111ll1llll_opy_ = Config.getoption
      from _pytest import runner
      bstack1l111ll1l_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warning(bstack11ll111_opy_ (u"ࠧࠫࡳ࠻ࠢࠨࡷࠧม"), bstack11l1ll1ll1_opy_, str(e))
    try:
      from pytest_bdd import reporting
      bstack1lll11llll_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack11ll111_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧย"))
    if bstack11l11l111_opy_():
      logger.warning(bstack111ll1ll_opy_[bstack11ll111_opy_ (u"ࠧࡔࡆࡎ࠱ࡌࡋࡎ࠮࠲࠳࠹ࠬร")])
  try:
    framework_name = bstack11ll111_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧฤ") if bstack1llll1l11_opy_ in [bstack11ll111_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨล"), bstack11ll111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩฦ"), bstack11ll111_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬว")] else bstack1l111ll11l_opy_(bstack1llll1l11_opy_)
    bstack1lllll11ll_opy_ = {
      bstack11ll111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪ࠭ศ"): bstack11ll111_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨษ") if bstack1llll1l11_opy_ == bstack11ll111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧส") and bstack111l1lll_opy_() else framework_name,
      bstack11ll111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬห"): bstack11l1l11lll_opy_(framework_name),
      bstack11ll111_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧฬ"): __version__,
      bstack11ll111_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡵࡴࡧࡧࠫอ"): bstack1llll1l11_opy_
    }
    if bstack1llll1l11_opy_ in bstack1lll1llll1_opy_ + bstack1l1l11l1l_opy_:
      if bstack11l11l11ll_opy_.bstack1ll1ll1111_opy_(CONFIG):
        if bstack11ll111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫฮ") in CONFIG:
          os.environ[bstack11ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ฯ")] = os.getenv(bstack11ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧะ"), json.dumps(CONFIG[bstack11ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧั")]))
          CONFIG[bstack11ll111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨา")].pop(bstack11ll111_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧำ"), None)
          CONFIG[bstack11ll111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪิ")].pop(bstack11ll111_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩี"), None)
        bstack1lllll11ll_opy_[bstack11ll111_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬึ")] = {
          bstack11ll111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫื"): bstack11ll111_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ุࠩ"),
          bstack11ll111_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ูࠩ"): str(bstack1ll1lll11_opy_())
        }
    bstack11lll1lll1_opy_, bstack11l11l1ll1_opy_ = None, {}
    bstack111llll111_opy_ = None
    bstack11l1l11l_opy_ = None
    def bstack1l11l1ll1_opy_():
      if bstack11llll111l_opy_:
        bstack11l1ll1lll_opy_()
      elif bstack111l1lllll_opy_:
        bstack1l1l1llll1_opy_()
    def bstack11ll1ll11_opy_():
      nonlocal bstack11lll1lll1_opy_, bstack11l11l1ll1_opy_
      if bstack1llll1l11_opy_ not in [bstack11ll111_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ฺࠪ")] and not cli.is_running():
        bstack11lll1lll1_opy_, bstack11l11l1ll1_opy_ = TestHubHandler.launch(CONFIG, bstack1lllll11ll_opy_)
    if bstack11llll111l_opy_ or bstack111l1lllll_opy_:
      bstack111llll111_opy_ = threading.Thread(target=bstack1l11l1ll1_opy_)
      bstack111llll111_opy_.start()
    if bstack1llll1l11_opy_ not in [bstack11ll111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ฻")] and not cli.is_running():
      bstack11l1l11l_opy_ = threading.Thread(target=bstack11ll1ll11_opy_)
      bstack11l1l11l_opy_.start()
    if bstack111llll111_opy_:
      bstack111llll111_opy_.join()
    if bstack11l1l11l_opy_:
      bstack11l1l11l_opy_.join()
    if bstack11l11l1ll1_opy_.get(bstack11ll111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ฼")) is not None and bstack11l11l11ll_opy_.bstack1l1lll11_opy_(CONFIG) is None:
      value = bstack11l11l1ll1_opy_[bstack11ll111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ฽")].get(bstack11ll111_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧ฾"))
      if value is not None:
          CONFIG[bstack11ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ฿")] = value
      else:
        logger.debug(bstack11ll111_opy_ (u"ࠣࡐࡲࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡩࡧࡴࡢࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠨเ"))
  except Exception as e:
    logger.debug(bstack1lllllll1l_opy_.format(bstack11ll111_opy_ (u"ࠩࡗࡩࡸࡺࡈࡶࡤࠪแ"), str(e)))
  if bstack1llll1l11_opy_ == bstack11ll111_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠫโ"):
    bstack11lll11ll_opy_ = True
    if bstack11111111_opy_ and bstack1111l111_opy_:
      if cli.is_enabled(CONFIG):
        bstack11111ll1l_opy_ = cli.config.get(bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨใ"), {}).get(bstack11ll111_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧไ")) if cli.config else None
      else:
        bstack11111ll1l_opy_ = CONFIG.get(bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪๅ"), {}).get(bstack11ll111_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩๆ"))
      bstack1l1ll111l1_opy_(bstack1llll11ll_opy_)
    elif bstack11111111_opy_:
      if cli.is_enabled(CONFIG):
        bstack11111ll1l_opy_ = cli.config.get(bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ็"), {}).get(bstack11ll111_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ่ࠫ")) if cli.config else None
      else:
        bstack11111ll1l_opy_ = CONFIG.get(bstack11ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹ้ࠧ"), {}).get(bstack11ll111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ๊࠭"))
      global bstack1llllllll1_opy_
      try:
        if bstack1lll1ll111_opy_(bstack11111111_opy_[bstack11ll111_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ๋")]) and multiprocessing.current_process().name == bstack11ll111_opy_ (u"࠭࠰ࠨ์"):
          bstack11111111_opy_[bstack11ll111_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪํ")].remove(bstack11ll111_opy_ (u"ࠨ࠯ࡰࠫ๎"))
          bstack11111111_opy_[bstack11ll111_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ๏")].remove(bstack11ll111_opy_ (u"ࠪࡴࡩࡨࠧ๐"))
          bstack11111111_opy_[bstack11ll111_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ๑")] = bstack11111111_opy_[bstack11ll111_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ๒")][0]
          with open(bstack11111111_opy_[bstack11ll111_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ๓")], bstack11ll111_opy_ (u"ࠧࡳࠩ๔")) as f:
            bstack1l1111111_opy_ = f.read()
          bstack1l111111ll_opy_ = bstack11ll111_opy_ (u"ࠣࠤࠥࡪࡷࡵ࡭ࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡴࡦ࡮ࠤ࡮ࡳࡰࡰࡴࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿ࡫࠻ࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡨࠬࢀࢃࠩ࠼ࠢࡩࡶࡴࡳࠠࡱࡦࡥࠤ࡮ࡳࡰࡰࡴࡷࠤࡕࡪࡢ࠼ࠢࡲ࡫ࡤࡪࡢࠡ࠿ࠣࡔࡩࡨ࠮ࡥࡱࡢࡦࡷ࡫ࡡ࡬࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡤࡦࡨࠣࡱࡴࡪ࡟ࡣࡴࡨࡥࡰ࠮ࡳࡦ࡮ࡩ࠰ࠥࡧࡲࡨ࠮ࠣࡸࡪࡳࡰࡰࡴࡤࡶࡾࠦ࠽ࠡ࠲ࠬ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡸࡷࡿ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡣࡵ࡫ࠥࡃࠠࡴࡶࡵࠬ࡮ࡴࡴࠩࡣࡵ࡫࠮࠱࠱࠱ࠫࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡧࡻࡧࡪࡶࡴࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡦࡹࠠࡦ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡴࡦࡹࡳࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࡯ࡨࡡࡧࡦ࠭ࡹࡥ࡭ࡨ࠯ࡥࡷ࡭ࠬࡵࡧࡰࡴࡴࡸࡡࡳࡻࠬࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡑࡦࡥ࠲ࡩࡵ࡟ࡣࠢࡀࠤࡲࡵࡤࡠࡤࡵࡩࡦࡱࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡔࡩࡨ࠮ࡥࡱࡢࡦࡷ࡫ࡡ࡬ࠢࡀࠤࡲࡵࡤࡠࡤࡵࡩࡦࡱࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡔࡩࡨࠨࠪ࠰ࡶࡩࡹࡥࡴࡳࡣࡦࡩ࠭࠯࡜࡯ࠤࠥࠦ๕").format(str(bstack11111111_opy_))
          bstack11llll111_opy_ = bstack1l111111ll_opy_ + bstack1l1111111_opy_
          bstack1111ll1l1_opy_ = bstack11111111_opy_[bstack11ll111_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ๖")] + bstack11ll111_opy_ (u"ࠪࡣࡧࡹࡴࡢࡥ࡮ࡣࡹ࡫࡭ࡱ࠰ࡳࡽࠬ๗")
          with open(bstack1111ll1l1_opy_, bstack11ll111_opy_ (u"ࠫࡼ࠭๘")):
            pass
          with open(bstack1111ll1l1_opy_, bstack11ll111_opy_ (u"ࠧࡽࠫࠣ๙")) as f:
            f.write(bstack11llll111_opy_)
          import subprocess
          bstack1l1ll1l11l_opy_ = subprocess.run([bstack11ll111_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࠨ๚"), bstack1111ll1l1_opy_])
          if os.path.exists(bstack1111ll1l1_opy_):
            os.unlink(bstack1111ll1l1_opy_)
          os._exit(bstack1l1ll1l11l_opy_.returncode)
        else:
          if bstack1lll1ll111_opy_(bstack11111111_opy_[bstack11ll111_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ๛")]):
            bstack11111111_opy_[bstack11ll111_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ๜")].remove(bstack11ll111_opy_ (u"ࠩ࠰ࡱࠬ๝"))
            bstack11111111_opy_[bstack11ll111_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭๞")].remove(bstack11ll111_opy_ (u"ࠫࡵࡪࡢࠨ๟"))
            bstack11111111_opy_[bstack11ll111_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ๠")] = bstack11111111_opy_[bstack11ll111_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ๡")][0]
          bstack1l1ll111l1_opy_(bstack1llll11ll_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack11111111_opy_[bstack11ll111_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ๢")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack11ll111_opy_ (u"ࠨࡡࡢࡲࡦࡳࡥࡠࡡࠪ๣")] = bstack11ll111_opy_ (u"ࠩࡢࡣࡲࡧࡩ࡯ࡡࡢࠫ๤")
          mod_globals[bstack11ll111_opy_ (u"ࠪࡣࡤ࡬ࡩ࡭ࡧࡢࡣࠬ๥")] = os.path.abspath(bstack11111111_opy_[bstack11ll111_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ๦")])
          exec(open(bstack11111111_opy_[bstack11ll111_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ๧")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack11ll111_opy_ (u"࠭ࡃࡢࡷࡪ࡬ࡹࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡿࢂ࠭๨").format(str(e)))
          for driver in bstack1llllllll1_opy_:
            bstack1l1l11ll1l_opy_.append({
              bstack11ll111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ๩"): bstack11111111_opy_[bstack11ll111_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ๪")],
              bstack11ll111_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ๫"): str(e),
              bstack11ll111_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ๬"): multiprocessing.current_process().name
            })
            bstack1l11l1ll11_opy_(driver, bstack11ll111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ๭"), bstack11ll111_opy_ (u"࡙ࠧࡥࡴࡵ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࡢ࡮ࠣ๮") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1llllllll1_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1llll11l1_opy_, CONFIG, logger)
      bstack11ll1lll1l_opy_()
      bstack1llll1l1l_opy_()
      percy.bstack11111ll1_opy_()
      bstack1ll111l1l1_opy_ = {
        bstack11ll111_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ๯"): args[0],
        bstack11ll111_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧ๰"): CONFIG,
        bstack11ll111_opy_ (u"ࠨࡊࡘࡆࡤ࡛ࡒࡍࠩ๱"): bstack11lll111ll_opy_,
        bstack11ll111_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ๲"): bstack1llll11l1_opy_
      }
      if bstack11ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭๳") in CONFIG:
        bstack1ll11l1l_opy_ = bstack1ll11llll1_opy_(args, logger, CONFIG, bstack11ll11l11l_opy_, bstack1111l11ll_opy_)
        bstack1l111l1ll1_opy_ = bstack1ll11l1l_opy_.bstack1111llll_opy_(run_on_browserstack, bstack1ll111l1l1_opy_, bstack1lll1ll111_opy_(args))
      else:
        if bstack1lll1ll111_opy_(args):
          bstack1ll111l1l1_opy_[bstack11ll111_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ๴")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1ll111l1l1_opy_,))
          test.start()
          test.join()
        else:
          bstack1l1ll111l1_opy_(bstack1llll11ll_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack11ll111_opy_ (u"ࠬࡥ࡟࡯ࡣࡰࡩࡤࡥࠧ๵")] = bstack11ll111_opy_ (u"࠭࡟ࡠ࡯ࡤ࡭ࡳࡥ࡟ࠨ๶")
          mod_globals[bstack11ll111_opy_ (u"ࠧࡠࡡࡩ࡭ࡱ࡫࡟ࡠࠩ๷")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1llll1l11_opy_ == bstack11ll111_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ๸") or bstack1llll1l11_opy_ == bstack11ll111_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ๹"):
    percy.init(bstack1llll11l1_opy_, CONFIG, logger)
    percy.bstack11111ll1_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack11l11ll11l_opy_(e, bstack1ll11l11l_opy_)
    bstack11ll1lll1l_opy_()
    bstack1l1ll111l1_opy_(bstack1ll1ll11l_opy_)
    if bstack11ll11l11l_opy_:
      bstack111l111ll1_opy_(bstack1ll1ll11l_opy_, args)
      if bstack11ll111_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨ๺") in args:
        i = args.index(bstack11ll111_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩ๻"))
        args.pop(i)
        args.pop(i)
      if bstack11ll111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ๼") not in CONFIG:
        CONFIG[bstack11ll111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ๽")] = [{}]
        bstack1111l11ll_opy_ = 1
      if bstack1ll111ll1l_opy_ == 0:
        bstack1ll111ll1l_opy_ = 1
      args.insert(0, str(bstack1ll111ll1l_opy_))
      args.insert(0, str(bstack11ll111_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ๾")))
    if TestHubHandler.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1l1lllll1_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack11ll1lllll_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack11ll111_opy_ (u"ࠣࡔࡒࡆࡔ࡚࡟ࡐࡒࡗࡍࡔࡔࡓࠣ๿"),
        ).parse_args(bstack1l1lllll1_opy_)
        bstack1l1ll111l_opy_ = args.index(bstack1l1lllll1_opy_[0]) if len(bstack1l1lllll1_opy_) > 0 else len(args)
        args.insert(bstack1l1ll111l_opy_, str(bstack11ll111_opy_ (u"ࠩ࠰࠱ࡱ࡯ࡳࡵࡧࡱࡩࡷ࠭຀")))
        args.insert(bstack1l1ll111l_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11ll111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡶࡴࡨ࡯ࡵࡡ࡯࡭ࡸࡺࡥ࡯ࡧࡵ࠲ࡵࡿࠧກ"))))
        if bstack1111lll11_opy_.bstack111ll11111_opy_(CONFIG):
          args.insert(bstack1l1ll111l_opy_, str(bstack11ll111_opy_ (u"ࠫ࠲࠳࡬ࡪࡵࡷࡩࡳ࡫ࡲࠨຂ")))
          args.insert(bstack1l1ll111l_opy_ + 1, str(bstack11ll111_opy_ (u"ࠬࡘࡥࡵࡴࡼࡊࡦ࡯࡬ࡦࡦ࠽ࡿࢂ࠭຃").format(bstack1111lll11_opy_.bstack11llllll_opy_(CONFIG))))
        if bstack11l1lll1_opy_(os.environ.get(bstack11ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠫຄ"))) and str(os.environ.get(bstack11ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠫ຅"), bstack11ll111_opy_ (u"ࠨࡰࡸࡰࡱ࠭ຆ"))) != bstack11ll111_opy_ (u"ࠩࡱࡹࡱࡲࠧງ"):
          for bstack11ll1ll1l_opy_ in bstack11ll1lllll_opy_:
            args.remove(bstack11ll1ll1l_opy_)
          test_files = os.environ.get(bstack11ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠧຈ")).split(bstack11ll111_opy_ (u"ࠫ࠱࠭ຉ"))
          for bstack1ll11lll_opy_ in test_files:
            args.append(bstack1ll11lll_opy_)
      except Exception as e:
        logger.error(bstack11ll111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡥࡹࡺࡡࡤࡪ࡬ࡲ࡬ࠦ࡬ࡪࡵࡷࡩࡳ࡫ࡲࠡࡨࡲࡶࠥࢁࡽ࠯ࠢࡈࡶࡷࡵࡲࠡ࠯ࠣࡿࢂࠨຊ").format(bstack11l11ll11_opy_, e))
    pabot.main(args)
  elif bstack1llll1l11_opy_ == bstack11ll111_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧ຋"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack11l11ll11l_opy_(e, bstack1ll11l11l_opy_)
    for a in args:
      if bstack11ll111_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝࠭ຌ") in a:
        bstack1lll1l11_opy_ = int(a.split(bstack11ll111_opy_ (u"ࠨ࠼ࠪຍ"))[1])
      if bstack11ll111_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡆࡈࡊࡑࡕࡃࡂࡎࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ຎ") in a:
        bstack11111ll1l_opy_ = str(a.split(bstack11ll111_opy_ (u"ࠪ࠾ࠬຏ"))[1])
      if bstack11ll111_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡇࡑࡏࡁࡓࡉࡖࠫຐ") in a:
        bstack1lll1ll1ll_opy_ = str(a.split(bstack11ll111_opy_ (u"ࠬࡀࠧຑ"))[1])
    bstack11lll1111_opy_ = None
    bstack1lll1l11l1_opy_ = None
    if bstack11ll111_opy_ (u"࠭࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠬຒ") in args:
      i = args.index(bstack11ll111_opy_ (u"ࠧ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽ࠭ຓ"))
      args.pop(i)
      bstack11lll1111_opy_ = args.pop(i)
    if bstack11ll111_opy_ (u"ࠨ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࠫດ") in args:
      i = args.index(bstack11ll111_opy_ (u"ࠩ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࠬຕ"))
      args.pop(i)
      bstack1lll1l11l1_opy_ = args.pop(i)
    if bstack11lll1111_opy_ is not None:
      global bstack11ll1ll1_opy_
      bstack11ll1ll1_opy_ = bstack11lll1111_opy_
    if bstack1lll1l11l1_opy_ is not None and int(bstack1lll1l11_opy_) < 0:
      bstack1lll1l11_opy_ = int(bstack1lll1l11l1_opy_)
    if cli.is_enabled(CONFIG):
      if cli.bstack1l11l1111_opy_():
        bstack111l1llll1_opy_.invoke(bstack1l11lll1ll_opy_.CONNECT, bstack11ll1l11l1_opy_())
    bstack1l1ll111l1_opy_(bstack1ll1ll11l_opy_)
    run_cli(args)
    if bstack11ll111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺࠧຖ") in multiprocessing.current_process().__dict__.keys():
      for bstack11l1ll1l1l_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1l1l11ll1l_opy_.append(bstack11l1ll1l1l_opy_)
  elif bstack1llll1l11_opy_ == bstack11ll111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫທ"):
    bstack11ll1ll111_opy_ = bstack1l1l111l11_opy_(args, logger, CONFIG, bstack11ll11l11l_opy_)
    bstack11ll1ll111_opy_.bstack11111lll_opy_()
    bstack11ll1lll1l_opy_()
    bstack111ll1l11l_opy_ = True
    bstack1llllll1ll_opy_ = bstack11ll1ll111_opy_.bstack1ll1l11l11_opy_()
    bstack11ll1ll111_opy_.bstack1ll111l1l1_opy_(bstack1l11ll1ll1_opy_)
    bstack11ll1ll111_opy_.bstack1l11lll1l1_opy_()
    bstack1ll11ll1_opy_(bstack1llll1l11_opy_, CONFIG, bstack11ll1ll111_opy_.bstack1l11lll1l_opy_())
    bstack11111111l_opy_.end(EVENTS.bstack1l1lll1l_opy_.value, EVENTS.bstack1l1lll1l_opy_.value + bstack11ll111_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧຘ"), EVENTS.bstack1l1lll1l_opy_.value + bstack11ll111_opy_ (u"ࠨ࠺ࡦࡰࡧࠦນ"), status=True, failure=None, test_name=bstack1lll11lll_opy_)
    bstack111lllll_opy_ = bstack11ll1ll111_opy_.bstack1111llll_opy_(bstack111llll1_opy_, {
      bstack11ll111_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧບ"): CONFIG,
      bstack11ll111_opy_ (u"ࠨࡊࡘࡆࡤ࡛ࡒࡍࠩປ"): bstack11lll111ll_opy_,
      bstack11ll111_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫຜ"): bstack1llll11l1_opy_,
      bstack11ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭ຝ"): bstack11ll11l11l_opy_,
      bstack11ll111_opy_ (u"ࠫࡔ࡜ࡅࡓࡔࡌࡈࡊࡥࡌࡐࡃࡇࡣ࡙ࡋࡓࡕࡋࡑࡋࠬພ"): bstack1ll1lllll1_opy_
    })
    if not bstack11111111_opy_:
      bstack1111ll1ll_opy_ = bstack1111l1l1l_opy_.bstack1ll111l11_opy_(EVENTS.bstack1l1l11l11_opy_.value)
    try:
      bstack1ll11l11ll_opy_, bstack111lll1l_opy_ = map(list, zip(*bstack111lllll_opy_))
      bstack1lll1l1l11_opy_ = bstack1ll11l11ll_opy_[0]
      for status_code in bstack111lll1l_opy_:
        if status_code != 0:
          bstack11l1111lll_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack11ll111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡤࡺࡪࠦࡥࡳࡴࡲࡶࡸࠦࡡ࡯ࡦࠣࡷࡹࡧࡴࡶࡵࠣࡧࡴࡪࡥ࠯ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡀࠠࡼࡿࠥຟ").format(str(e)))
  elif bstack1llll1l11_opy_ == bstack11ll111_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ຠ"):
    try:
      from behave.__main__ import main as bstack1l11l1ll1l_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack11l11ll11l_opy_(e, bstack1ll111l1_opy_)
    bstack11ll1lll1l_opy_()
    bstack111ll1l11l_opy_ = True
    bstack1lll11l11_opy_ = 1
    if bstack11ll111_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧມ") in CONFIG:
      bstack1lll11l11_opy_ = CONFIG[bstack11ll111_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨຢ")]
    if bstack11ll111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬຣ") in CONFIG:
      bstack1l11lllll1_opy_ = int(bstack1lll11l11_opy_) * int(len(CONFIG[bstack11ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭຤")]))
    else:
      bstack1l11lllll1_opy_ = int(bstack1lll11l11_opy_)
    config = Configuration(args)
    bstack11l11ll1ll_opy_ = config.paths
    if len(bstack11l11ll1ll_opy_) == 0:
      import glob
      pattern = bstack11ll111_opy_ (u"ࠫ࠯࠰࠯ࠫ࠰ࡩࡩࡦࡺࡵࡳࡧࠪລ")
      bstack1ll11l1ll1_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1ll11l1ll1_opy_)
      config = Configuration(args)
      bstack11l11ll1ll_opy_ = config.paths
    bstack1l111l1lll_opy_ = [os.path.normpath(item) for item in bstack11l11ll1ll_opy_]
    bstack11l1lll1l1_opy_ = [os.path.normpath(item) for item in args]
    bstack1l11ll111l_opy_ = [item for item in bstack11l1lll1l1_opy_ if item not in bstack1l111l1lll_opy_]
    import platform as pf
    if pf.system().lower() == bstack11ll111_opy_ (u"ࠬࡽࡩ࡯ࡦࡲࡻࡸ࠭຦"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1l111l1lll_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l1l1ll1l_opy_)))
                    for bstack1l1l1ll1l_opy_ in bstack1l111l1lll_opy_]
    bstack1l111lll_opy_ = []
    for spec in bstack1l111l1lll_opy_:
      bstack11lll1l1ll_opy_ = []
      bstack11lll1l1ll_opy_ += bstack1l11ll111l_opy_
      bstack11lll1l1ll_opy_.append(spec)
      bstack1l111lll_opy_.append(bstack11lll1l1ll_opy_)
    execution_items = []
    for bstack11lll1l1ll_opy_ in bstack1l111lll_opy_:
      if bstack11ll111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩວ") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack11ll111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪຨ")]):
          item = {}
          item[bstack11ll111_opy_ (u"ࠨࡣࡵ࡫ࠬຩ")] = bstack11ll111_opy_ (u"ࠩࠣࠫສ").join(bstack11lll1l1ll_opy_)
          item[bstack11ll111_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩຫ")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack11ll111_opy_ (u"ࠫࡦࡸࡧࠨຬ")] = bstack11ll111_opy_ (u"ࠬࠦࠧອ").join(bstack11lll1l1ll_opy_)
        item[bstack11ll111_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬຮ")] = 0
        execution_items.append(item)
    bstack11l11111l1_opy_ = bstack111llllll1_opy_(execution_items, bstack1l11lllll1_opy_)
    for execution_item in bstack11l11111l1_opy_:
      bstack11ll111l_opy_ = []
      for item in execution_item:
        bstack11ll111l_opy_.append(bstack11l111l1l1_opy_(name=str(item[bstack11ll111_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ຯ")]),
                                             target=bstack1lll11lll1_opy_,
                                             args=(item[bstack11ll111_opy_ (u"ࠨࡣࡵ࡫ࠬະ")],)))
      for t in bstack11ll111l_opy_:
        t.start()
      for t in bstack11ll111l_opy_:
        t.join()
  else:
    bstack1l1ll11111_opy_(bstack1ll111ll_opy_)
  if not bstack11111111_opy_:
    bstack111l1l1111_opy_()
    if bstack1111ll1ll_opy_:
      bstack1111l1l1l_opy_.end(EVENTS.bstack1l1l11l11_opy_.value, bstack1111ll1ll_opy_ + bstack11ll111_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤັ"), bstack1111ll1ll_opy_ + bstack11ll111_opy_ (u"ࠥ࠾ࡪࡴࡤࠣາ"), status=True, failure=None, test_name=None)
  logger_utils.bstack11l1l111l_opy_()
def browserstack_initialize(bstack111ll1l1l1_opy_=None):
  logger.info(bstack11ll111_opy_ (u"ࠫࡗࡻ࡮࡯࡫ࡱ࡫࡙ࠥࡄࡌࠢࡺ࡭ࡹ࡮ࠠࡢࡴࡪࡷ࠿ࠦࠧຳ") + str(bstack111ll1l1l1_opy_))
  run_on_browserstack(bstack111ll1l1l1_opy_, None, True)
@measure(event_name=EVENTS.bstack1l11l1l111_opy_, stage=STAGE.bstack1111l1111_opy_, bstack11ll11ll11_opy_=bstack1lll11lll_opy_)
def bstack111l1l1111_opy_():
  global CONFIG
  global bstack1l11lll1_opy_
  global bstack11l1111lll_opy_
  global bstack11ll1ll1ll_opy_
  global global_config
  bstack11l1ll11l1_opy_.bstack1ll11ll1ll_opy_()
  if cli.is_running():
    bstack111l1llll1_opy_.invoke(bstack1l11lll1ll_opy_.bstack1lllllll1_opy_)
  else:
    bstack1lllll111l_opy_ = bstack1111lll11_opy_.get_instance(config=CONFIG)
    bstack1lllll111l_opy_.bstack111l11l11l_opy_(CONFIG)
  hashed_id = None
  bstack1lll1l111l_opy_ = None
  def bstack1l11ll1l11_opy_():
    try:
      if bstack1l11lll1_opy_ == bstack11ll111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬິ"):
        if not cli.is_enabled(CONFIG):
          TestHubHandler.stop()
      else:
        TestHubHandler.stop()
    except Exception as e:
      logger.debug(bstack11ll111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡹࡴࡰࡲࡳ࡭ࡳ࡭ࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࡾࢁࠧີ").format(e))
  def bstack111l1l111_opy_():
    try:
      if not cli.is_enabled(CONFIG):
        bstack11lll1ll1_opy_.bstack11ll1lll_opy_()
    except Exception as e:
      logger.debug(bstack11ll111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡰࡳ࡫ࡱࡸ࡮ࡴࡧࠡࡤࡸ࡭ࡱࡪࠠ࡭࡫ࡱ࡯࠿ࠦࡻࡾࠤຶ").format(e))
  def bstack11l111lll_opy_():
    nonlocal hashed_id, bstack1lll1l111l_opy_
    try:
      if bstack11ll111_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬື") in CONFIG and str(CONFIG[bstack11ll111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪຸ࠭")]).lower() != bstack11ll111_opy_ (u"ࠪࡪࡦࡲࡳࡦູࠩ"):
        hashed_id, bstack1lll1l111l_opy_ = bstack1l1l1111_opy_()
      else:
        hashed_id, bstack1lll1l111l_opy_ = get_build_link()
    except Exception as e:
      logger.debug(bstack11ll111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࠣࡰ࡮ࡴ࡫࠻ࠢࡾࢁ຺ࠧ").format(e))
  bstack111lll11l_opy_ = threading.Thread(target=bstack1l11ll1l11_opy_)
  bstack1ll111l1ll_opy_ = threading.Thread(target=bstack111l1l111_opy_)
  bstack1lll1llll_opy_ = threading.Thread(target=bstack11l111lll_opy_)
  threads = [bstack111lll11l_opy_, bstack1ll111l1ll_opy_, bstack1lll1llll_opy_]
  for thread in threads:
    try:
      thread.start()
    except Exception as e:
      logger.debug(bstack11ll111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡸࡺࡡࡳࡶ࡬ࡲ࡬ࠦࡴࡩࡴࡨࡥࡩࠦࡻࡾ࠼ࠣࡿࢂࠨົ").format(thread.name, e))
  for thread in threads:
    try:
      thread.join()
    except Exception as e:
      logger.debug(bstack11ll111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡰ࡯ࡪࡰ࡬ࡲ࡬ࠦࡴࡩࡴࡨࡥࡩࠦࡻࡾ࠼ࠣࡿࢂࠨຼ").format(thread.name, e))
  bstack1111111l_opy_(hashed_id)
  logger.info(bstack11ll111_opy_ (u"ࠧࡔࡆࡎࠤࡷࡻ࡮ࠡࡧࡱࡨࡪࡪࠠࡧࡱࡵࠤ࡮ࡪ࠺ࠨຽ") + global_config.get_property(bstack11ll111_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪ຾"), bstack11ll111_opy_ (u"ࠩࠪ຿")) + bstack11ll111_opy_ (u"ࠪ࠰ࠥࡺࡥࡴࡶ࡫ࡹࡧࠦࡩࡥ࠼ࠣࠫເ") + os.getenv(bstack11ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩແ"), bstack11ll111_opy_ (u"ࠬ࠭ໂ")))
  if hashed_id is not None and bstack1ll1111111_opy_() != -1:
    sessions = bstack1l11l11l_opy_(hashed_id)
    bstack1l1111lll_opy_(sessions, bstack1lll1l111l_opy_)
  if bstack1l11lll1_opy_ == bstack11ll111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ໃ") and bstack11l1111lll_opy_ != 0:
    sys.exit(bstack11l1111lll_opy_)
  if bstack1l11lll1_opy_ == bstack11ll111_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧໄ") and bstack11ll1ll1ll_opy_ != 0:
    sys.exit(bstack11ll1ll1ll_opy_)
def bstack1111111l_opy_(new_id):
    global bstack11l11l1l1_opy_
    bstack11l11l1l1_opy_ = new_id
def bstack1l111ll11l_opy_(bstack11l1l1l1l_opy_):
  if bstack11l1l1l1l_opy_:
    return bstack11l1l1l1l_opy_.capitalize()
  else:
    return bstack11ll111_opy_ (u"ࠨࠩ໅")
@measure(event_name=EVENTS.bstack1l1l11l1_opy_, stage=STAGE.bstack1111l1111_opy_, bstack11ll11ll11_opy_=bstack1lll11lll_opy_)
def bstack1ll11l1111_opy_(bstack1111lll1_opy_):
  if bstack11ll111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧໆ") in bstack1111lll1_opy_ and bstack1111lll1_opy_[bstack11ll111_opy_ (u"ࠪࡲࡦࡳࡥࠨ໇")] != bstack11ll111_opy_ (u"່ࠫࠬ"):
    return bstack1111lll1_opy_[bstack11ll111_opy_ (u"ࠬࡴࡡ࡮ࡧ້ࠪ")]
  else:
    bstack11ll11ll11_opy_ = bstack11ll111_opy_ (u"ࠨ໊ࠢ")
    if bstack11ll111_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫໋ࠧ") in bstack1111lll1_opy_ and bstack1111lll1_opy_[bstack11ll111_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨ໌")] != None:
      bstack11ll11ll11_opy_ += bstack1111lll1_opy_[bstack11ll111_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩໍ")] + bstack11ll111_opy_ (u"ࠥ࠰ࠥࠨ໎")
      if bstack1111lll1_opy_[bstack11ll111_opy_ (u"ࠫࡴࡹࠧ໏")] == bstack11ll111_opy_ (u"ࠧ࡯࡯ࡴࠤ໐"):
        bstack11ll11ll11_opy_ += bstack11ll111_opy_ (u"ࠨࡩࡐࡕࠣࠦ໑")
      bstack11ll11ll11_opy_ += (bstack1111lll1_opy_[bstack11ll111_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫ໒")] or bstack11ll111_opy_ (u"ࠨࠩ໓"))
      return bstack11ll11ll11_opy_
    else:
      bstack11ll11ll11_opy_ += bstack1l111ll11l_opy_(bstack1111lll1_opy_[bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪ໔")]) + bstack11ll111_opy_ (u"ࠥࠤࠧ໕") + (
              bstack1111lll1_opy_[bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭໖")] or bstack11ll111_opy_ (u"ࠬ࠭໗")) + bstack11ll111_opy_ (u"ࠨࠬࠡࠤ໘")
      if bstack1111lll1_opy_[bstack11ll111_opy_ (u"ࠧࡰࡵࠪ໙")] == bstack11ll111_opy_ (u"࡙ࠣ࡬ࡲࡩࡵࡷࡴࠤ໚"):
        bstack11ll11ll11_opy_ += bstack11ll111_opy_ (u"ࠤ࡚࡭ࡳࠦࠢ໛")
      bstack11ll11ll11_opy_ += bstack1111lll1_opy_[bstack11ll111_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧໜ")] or bstack11ll111_opy_ (u"ࠫࠬໝ")
      return bstack11ll11ll11_opy_
@measure(event_name=EVENTS.bstack1l1lll1l1l_opy_, stage=STAGE.bstack1111l1111_opy_, bstack11ll11ll11_opy_=bstack1lll11lll_opy_)
def bstack11l11l11l_opy_(bstack1llll11ll1_opy_):
  if bstack1llll11ll1_opy_ == bstack11ll111_opy_ (u"ࠧࡪ࡯࡯ࡧࠥໞ"):
    return bstack11ll111_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡩࡵࡩࡪࡴ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡩࡵࡩࡪࡴࠢ࠿ࡅࡲࡱࡵࡲࡥࡵࡧࡧࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩໟ")
  elif bstack1llll11ll1_opy_ == bstack11ll111_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ໠"):
    return bstack11ll111_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡶࡪࡪ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡴࡨࡨࠧࡄࡆࡢ࡫࡯ࡩࡩࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫ໡")
  elif bstack1llll11ll1_opy_ == bstack11ll111_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ໢"):
    return bstack11ll111_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿࡭ࡲࡦࡧࡱ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧ࡭ࡲࡦࡧࡱࠦࡃࡖࡡࡴࡵࡨࡨࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪ໣")
  elif bstack1llll11ll1_opy_ == bstack11ll111_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥ໤"):
    return bstack11ll111_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡳࡧࡧ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡸࡥࡥࠤࡁࡉࡷࡸ࡯ࡳ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ໥")
  elif bstack1llll11ll1_opy_ == bstack11ll111_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࠢ໦"):
    return bstack11ll111_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࠦࡩࡪࡧ࠳࠳࠸࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࠨ࡫ࡥࡢ࠵࠵࠺ࠧࡄࡔࡪ࡯ࡨࡳࡺࡺ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ໧")
  elif bstack1llll11ll1_opy_ == bstack11ll111_opy_ (u"ࠣࡴࡸࡲࡳ࡯࡮ࡨࠤ໨"):
    return bstack11ll111_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡧࡲࡡࡤ࡭࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡧࡲࡡࡤ࡭ࠥࡂࡗࡻ࡮࡯࡫ࡱ࡫ࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪ໩")
  else:
    return bstack11ll111_opy_ (u"ࠪࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡢ࡭ࡣࡦ࡯ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡢ࡭ࡣࡦ࡯ࠧࡄࠧ໪") + bstack1l111ll11l_opy_(
      bstack1llll11ll1_opy_) + bstack11ll111_opy_ (u"ࠫࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪ໫")
def bstack11ll11ll_opy_(session):
  return bstack11ll111_opy_ (u"ࠬࡂࡴࡳࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡵࡳࡼࠨ࠾࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠢࡶࡩࡸࡹࡩࡰࡰ࠰ࡲࡦࡳࡥࠣࡀ࠿ࡥࠥ࡮ࡲࡦࡨࡀࠦࢀࢃࠢࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤࡢࡦࡱࡧ࡮࡬ࠤࡁࡿࢂࡂ࠯ࡢࡀ࠿࠳ࡹࡪ࠾ࡼࡿࡾࢁࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼࠰ࡶࡵࡂࠬ໬").format(
    session[bstack11ll111_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨࡥࡵࡳ࡮ࠪ໭")], bstack1ll11l1111_opy_(session), bstack11l11l11l_opy_(session[bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡳࡵࡣࡷࡹࡸ࠭໮")]),
    bstack11l11l11l_opy_(session[bstack11ll111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ໯")]),
    bstack1l111ll11l_opy_(session[bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪ໰")] or session[bstack11ll111_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪ໱")] or bstack11ll111_opy_ (u"ࠫࠬ໲")) + bstack11ll111_opy_ (u"ࠧࠦࠢ໳") + (session[bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ໴")] or bstack11ll111_opy_ (u"ࠧࠨ໵")),
    session[bstack11ll111_opy_ (u"ࠨࡱࡶࠫ໶")] + bstack11ll111_opy_ (u"ࠤࠣࠦ໷") + session[bstack11ll111_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ໸")], session[bstack11ll111_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭໹")] or bstack11ll111_opy_ (u"ࠬ࠭໺"),
    session[bstack11ll111_opy_ (u"࠭ࡣࡳࡧࡤࡸࡪࡪ࡟ࡢࡶࠪ໻")] if session[bstack11ll111_opy_ (u"ࠧࡤࡴࡨࡥࡹ࡫ࡤࡠࡣࡷࠫ໼")] else bstack11ll111_opy_ (u"ࠨࠩ໽"))
@measure(event_name=EVENTS.bstack111l11l11_opy_, stage=STAGE.bstack1111l1111_opy_, bstack11ll11ll11_opy_=bstack1lll11lll_opy_)
def bstack1l1111lll_opy_(sessions, bstack1lll1l111l_opy_):
  try:
    bstack1ll1ll111l_opy_ = bstack11ll111_opy_ (u"ࠤࠥ໾")
    if not os.path.exists(bstack11ll11ll1l_opy_):
      os.mkdir(bstack11ll11ll1l_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11ll111_opy_ (u"ࠪࡥࡸࡹࡥࡵࡵ࠲ࡶࡪࡶ࡯ࡳࡶ࠱࡬ࡹࡳ࡬ࠨ໿")), bstack11ll111_opy_ (u"ࠫࡷ࠭ༀ")) as f:
      bstack1ll1ll111l_opy_ = f.read()
    bstack1ll1ll111l_opy_ = bstack1ll1ll111l_opy_.replace(bstack11ll111_opy_ (u"ࠬࢁࠥࡓࡇࡖ࡙ࡑ࡚ࡓࡠࡅࡒ࡙ࡓ࡚ࠥࡾࠩ༁"), str(len(sessions)))
    bstack1ll1ll111l_opy_ = bstack1ll1ll111l_opy_.replace(bstack11ll111_opy_ (u"࠭ࡻࠦࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠩࢂ࠭༂"), bstack1lll1l111l_opy_)
    bstack1ll1ll111l_opy_ = bstack1ll1ll111l_opy_.replace(bstack11ll111_opy_ (u"ࠧࡼࠧࡅ࡙ࡎࡒࡄࡠࡐࡄࡑࡊࠫࡽࠨ༃"),
                                              sessions[0].get(bstack11ll111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟࡯ࡣࡰࡩࠬ༄")) if sessions[0] else bstack11ll111_opy_ (u"ࠩࠪ༅"))
    with open(os.path.join(bstack11ll11ll1l_opy_, bstack11ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡵࡩࡵࡵࡲࡵ࠰࡫ࡸࡲࡲࠧ༆")), bstack11ll111_opy_ (u"ࠫࡼ࠭༇")) as stream:
      stream.write(bstack1ll1ll111l_opy_.split(bstack11ll111_opy_ (u"ࠬࢁࠥࡔࡇࡖࡗࡎࡕࡎࡔࡡࡇࡅ࡙ࡇࠥࡾࠩ༈"))[0])
      for session in sessions:
        stream.write(bstack11ll11ll_opy_(session))
      stream.write(bstack1ll1ll111l_opy_.split(bstack11ll111_opy_ (u"࠭ࡻࠦࡕࡈࡗࡘࡏࡏࡏࡕࡢࡈࡆ࡚ࡁࠦࡿࠪ༉"))[1])
    logger.info(bstack11ll111_opy_ (u"ࠧࡈࡧࡱࡩࡷࡧࡴࡦࡦࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡥࡹ࡮ࡲࡤࠡࡣࡵࡸ࡮࡬ࡡࡤࡶࡶࠤࡦࡺࠠࡼࡿࠪ༊").format(bstack11ll11ll1l_opy_));
  except Exception as e:
    logger.debug(bstack1l1llllll_opy_.format(str(e)))
def bstack1l11l11l_opy_(hashed_id):
  global CONFIG
  try:
    bstack11lll11111_opy_ = datetime.datetime.now()
    host = bstack11ll111_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡴ࡮࠳ࡣ࡭ࡱࡸࡨ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨ་") if bstack11ll111_opy_ (u"ࠩࡤࡴࡵ࠭༌") in CONFIG else bstack11ll111_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫ།")
    user = CONFIG[bstack11ll111_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭༎")]
    key = CONFIG[bstack11ll111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ༏")]
    bstack111111ll_opy_ = bstack11ll111_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ༐") if bstack11ll111_opy_ (u"ࠧࡢࡲࡳࠫ༑") in CONFIG else (bstack11ll111_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬ༒") if CONFIG.get(bstack11ll111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭༓")) else bstack11ll111_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ༔"))
    host = bstack1llll1ll_opy_(cli.config, [bstack11ll111_opy_ (u"ࠦࡦࡶࡩࡴࠤ༕"), bstack11ll111_opy_ (u"ࠧࡧࡰࡱࡃࡸࡸࡴࡳࡡࡵࡧࠥ༖"), bstack11ll111_opy_ (u"ࠨࡡࡱ࡫ࠥ༗")], host) if bstack11ll111_opy_ (u"ࠧࡢࡲࡳ༘ࠫ") in CONFIG else bstack1llll1ll_opy_(cli.config, [bstack11ll111_opy_ (u"ࠣࡣࡳ࡭ࡸࠨ༙"), bstack11ll111_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨࠦ༚"), bstack11ll111_opy_ (u"ࠥࡥࡵ࡯ࠢ༛")], host)
    url = bstack11ll111_opy_ (u"ࠫࢀࢃ࠯ࡼࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂ࠵ࡳࡦࡵࡶ࡭ࡴࡴࡳ࠯࡬ࡶࡳࡳ࠭༜").format(host, bstack111111ll_opy_, hashed_id)
    headers = {
      bstack11ll111_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫ༝"): bstack11ll111_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ༞"),
    }
    proxies = bstack1111llll1l_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies, auth=(user, key))
    if response.json():
      cli.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠢࡩࡶࡷࡴ࠿࡭ࡥࡵࡡࡶࡩࡸࡹࡩࡰࡰࡶࡣࡱ࡯ࡳࡵࠤ༟"), datetime.datetime.now() - bstack11lll11111_opy_)
      return list(map(lambda session: session[bstack11ll111_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭༠")], response.json()))
  except Exception as e:
    logger.debug(bstack11l11llll1_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack1111lll1l_opy_, stage=STAGE.bstack1111l1111_opy_, bstack11ll11ll11_opy_=bstack1lll11lll_opy_)
def get_build_link():
  global CONFIG
  global bstack11l11l1l1_opy_
  try:
    if bstack11ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ༡") in CONFIG:
      bstack11lll11111_opy_ = datetime.datetime.now()
      host = bstack11ll111_opy_ (u"ࠪࡥࡵ࡯࠭ࡤ࡮ࡲࡹࡩ࠭༢") if bstack11ll111_opy_ (u"ࠫࡦࡶࡰࠨ༣") in CONFIG else bstack11ll111_opy_ (u"ࠬࡧࡰࡪࠩ༤")
      user = CONFIG[bstack11ll111_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ༥")]
      key = CONFIG[bstack11ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ༦")]
      bstack111111ll_opy_ = bstack11ll111_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ༧") if bstack11ll111_opy_ (u"ࠩࡤࡴࡵ࠭༨") in CONFIG else bstack11ll111_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ༩")
      url = bstack11ll111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࢀࢃ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠴ࡪࡴࡱࡱࠫ༪").format(user, key, host, bstack111111ll_opy_)
      if cli.is_enabled(CONFIG):
        bstack1lll1l111l_opy_, hashed_id = cli.bstack11llll1111_opy_()
        logger.info(bstack111ll1l111_opy_.format(bstack1lll1l111l_opy_))
        return [hashed_id, bstack1lll1l111l_opy_]
      else:
        headers = {
          bstack11ll111_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫ༫"): bstack11ll111_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ༬"),
        }
        if bstack11ll111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ༭") in CONFIG:
          params = {bstack11ll111_opy_ (u"ࠨࡰࡤࡱࡪ࠭༮"): CONFIG[bstack11ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ༯")], bstack11ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭༰"): CONFIG[bstack11ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭༱")]}
        else:
          params = {bstack11ll111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ༲"): CONFIG[bstack11ll111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ༳")]}
        proxies = bstack1111llll1l_opy_(CONFIG, url)
        response = requests.get(url, params=params, headers=headers, proxies=proxies)
        if response.json():
          bstack1l1llll11l_opy_ = response.json()[0][bstack11ll111_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡧࡻࡩ࡭ࡦࠪ༴")]
          if bstack1l1llll11l_opy_:
            bstack1lll1l111l_opy_ = bstack1l1llll11l_opy_[bstack11ll111_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣࡠࡷࡵࡰ༵ࠬ")].split(bstack11ll111_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤ࠯ࡥࡹ࡮ࡲࡤࠨ༶"))[0] + bstack11ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡵ࠲༷ࠫ") + bstack1l1llll11l_opy_[
              bstack11ll111_opy_ (u"ࠫ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ༸")]
            logger.info(bstack111ll1l111_opy_.format(bstack1lll1l111l_opy_))
            bstack11l11l1l1_opy_ = bstack1l1llll11l_opy_[bstack11ll111_opy_ (u"ࠬ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ༹")]
            bstack11l1l1111l_opy_ = CONFIG[bstack11ll111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ༺")]
            if bstack11ll111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ༻") in CONFIG:
              bstack11l1l1111l_opy_ += bstack11ll111_opy_ (u"ࠨࠢࠪ༼") + CONFIG[bstack11ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ༽")]
            if bstack11l1l1111l_opy_ != bstack1l1llll11l_opy_[bstack11ll111_opy_ (u"ࠪࡲࡦࡳࡥࠨ༾")]:
              logger.debug(bstack1l1ll11l11_opy_.format(bstack1l1llll11l_opy_[bstack11ll111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ༿")], bstack11l1l1111l_opy_))
            cli.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࡫ࡪࡺ࡟ࡣࡷ࡬ࡰࡩࡥ࡬ࡪࡰ࡮ࠦཀ"), datetime.datetime.now() - bstack11lll11111_opy_)
            return [bstack1l1llll11l_opy_[bstack11ll111_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩཁ")], bstack1lll1l111l_opy_]
    else:
      logger.warning(bstack111l11l1l1_opy_)
  except Exception as e:
    logger.debug(bstack11l111llll_opy_.format(str(e)))
  return [None, None]
def bstack111l11l111_opy_(url, bstack11ll111l1l_opy_=False):
  global CONFIG
  global bstack111l11111_opy_
  if not bstack111l11111_opy_:
    hostname = bstack1lllll1111_opy_(url)
    is_private = bstack11lll1111l_opy_(hostname)
    if (bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫག") in CONFIG and not bstack11l1lll1_opy_(CONFIG[bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬགྷ")])) and (is_private or bstack11ll111l1l_opy_):
      bstack111l11111_opy_ = hostname
def bstack1lllll1111_opy_(url):
  return urlparse(url).hostname
def bstack11lll1111l_opy_(hostname):
  for bstack11lll11l_opy_ in bstack1l1lllll11_opy_:
    regex = re.compile(bstack11lll11l_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1l1lllll_opy_(bstack1ll1l1lll1_opy_):
  return True if bstack1ll1l1lll1_opy_ in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack111ll1111_opy_, stage=STAGE.bstack1111l1111_opy_, bstack11ll11ll11_opy_=bstack1lll11lll_opy_)
def getAccessibilityResults(driver):
  global CONFIG
  global bstack1lll1l11_opy_
  bstack1ll1l1l1l1_opy_ = not (bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ང"), None) and bstack1lll11l111_opy_(
          threading.current_thread(), bstack11ll111_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩཅ"), None))
  bstack1l111l1ll_opy_ = getattr(driver, bstack11ll111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫཆ"), None) != True
  bstack11lllll1_opy_ = bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠬ࡯ࡳࡂࡲࡳࡅ࠶࠷ࡹࡕࡧࡶࡸࠬཇ"), None) and bstack1lll11l111_opy_(
          threading.current_thread(), bstack11ll111_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ཈"), None)
  if bstack11lllll1_opy_:
    if not bstack1lll111l1_opy_():
      logger.warning(bstack11ll111_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡲࡳࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡪࡺࡲࡪࡧࡹࡩࠥࡇࡰࡱࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵ࠱ࠦཉ"))
      return {}
    logger.debug(bstack11ll111_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠬཊ"))
    logger.debug(perform_scan(driver, driver_command=bstack11ll111_opy_ (u"ࠩࡨࡼࡪࡩࡵࡵࡧࡖࡧࡷ࡯ࡰࡵࠩཋ")))
    results = bstack1l1l1ll1_opy_(bstack11ll111_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡶࠦཌ"))
    if results is not None and results.get(bstack11ll111_opy_ (u"ࠦ࡮ࡹࡳࡶࡧࡶࠦཌྷ")) is not None:
        return results[bstack11ll111_opy_ (u"ࠧ࡯ࡳࡴࡷࡨࡷࠧཎ")]
    logger.error(bstack11ll111_opy_ (u"ࠨࡎࡰࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡕࡩࡸࡻ࡬ࡵࡵࠣࡻࡪࡸࡥࠡࡨࡲࡹࡳࡪ࠮ࠣཏ"))
    return []
  if not bstack11l11l11ll_opy_.bstack11l1111ll_opy_(CONFIG, bstack1lll1l11_opy_) or (bstack1l111l1ll_opy_ and bstack1ll1l1l1l1_opy_):
    logger.warning(bstack11ll111_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴ࠰ࠥཐ"))
    return {}
  try:
    logger.debug(bstack11ll111_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠬད"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack11ll11llll_opy_.bstack1lll11ll11_opy_)
    return results
  except Exception:
    logger.error(bstack11ll111_opy_ (u"ࠤࡑࡳࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡷࡦࡴࡨࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦདྷ"))
    return {}
@measure(event_name=EVENTS.bstack11l1111111_opy_, stage=STAGE.bstack1111l1111_opy_, bstack11ll11ll11_opy_=bstack1lll11lll_opy_)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack1lll1l11_opy_
  bstack1ll1l1l1l1_opy_ = not (bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧན"), None) and bstack1lll11l111_opy_(
          threading.current_thread(), bstack11ll111_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪཔ"), None))
  bstack1l111l1ll_opy_ = getattr(driver, bstack11ll111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬཕ"), None) != True
  bstack11lllll1_opy_ = bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭བ"), None) and bstack1lll11l111_opy_(
          threading.current_thread(), bstack11ll111_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩབྷ"), None)
  if bstack11lllll1_opy_:
    if not bstack1lll111l1_opy_():
      logger.warning(bstack11ll111_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡳࡴࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡸࡻ࡭࡮ࡣࡵࡽ࠳ࠨམ"))
      return {}
    logger.debug(bstack11ll111_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡳࡶ࡯ࡰࡥࡷࡿࠧཙ"))
    logger.debug(perform_scan(driver, driver_command=bstack11ll111_opy_ (u"ࠪࡩࡽ࡫ࡣࡶࡶࡨࡗࡨࡸࡩࡱࡶࠪཚ")))
    results = bstack1l1l1ll1_opy_(bstack11ll111_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷࡗࡺࡳ࡭ࡢࡴࡼࠦཛ"))
    if results is not None and results.get(bstack11ll111_opy_ (u"ࠧࡹࡵ࡮࡯ࡤࡶࡾࠨཛྷ")) is not None:
        return results[bstack11ll111_opy_ (u"ࠨࡳࡶ࡯ࡰࡥࡷࡿࠢཝ")]
    logger.error(bstack11ll111_opy_ (u"ࠢࡏࡱࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡖࡪࡹࡵ࡭ࡶࡶࠤࡘࡻ࡭࡮ࡣࡵࡽࠥࡽࡡࡴࠢࡩࡳࡺࡴࡤ࠯ࠤཞ"))
    return {}
  if not bstack11l11l11ll_opy_.bstack11l1111ll_opy_(CONFIG, bstack1lll1l11_opy_) or (bstack1l111l1ll_opy_ and bstack1ll1l1l1l1_opy_):
    logger.warning(bstack11ll111_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡷࡺࡳ࡭ࡢࡴࡼ࠲ࠧཟ"))
    return {}
  try:
    logger.debug(bstack11ll111_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡳࡶ࡯ࡰࡥࡷࡿࠧའ"))
    logger.debug(perform_scan(driver))
    bstack11l1l1l1ll_opy_ = driver.execute_async_script(bstack11ll11llll_opy_.bstack1ll1l1ll_opy_)
    return bstack11l1l1l1ll_opy_
  except Exception:
    logger.error(bstack11ll111_opy_ (u"ࠥࡒࡴࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡶ࡯ࡰࡥࡷࡿࠠࡸࡣࡶࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦཡ"))
    return {}
def bstack1lll111l1_opy_():
  global CONFIG
  global bstack1lll1l11_opy_
  bstack1llllll11_opy_ = bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫར"), None) and bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧལ"), None)
  if not bstack11l11l11ll_opy_.bstack11l1111ll_opy_(CONFIG, bstack1lll1l11_opy_) or not bstack1llllll11_opy_:
        logger.warning(bstack11ll111_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡷ࡫ࡳࡶ࡮ࡷࡷ࠳ࠨཤ"))
        return False
  return True
def bstack1l1l1ll1_opy_(result_type):
    bstack11ll11l1ll_opy_ = TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack11lll1ll1_opy_.current_hook_uuid()
    with ThreadPoolExecutor() as executor:
        future = executor.submit(bstack11l1ll111l_opy_(bstack11ll11l1ll_opy_, result_type))
        try:
            return future.result(timeout=bstack11l1l11ll1_opy_)
        except TimeoutError:
            logger.error(bstack11ll111_opy_ (u"ࠢࡕ࡫ࡰࡩࡴࡻࡴࠡࡣࡩࡸࡪࡸࠠࡼࡿࡶࠤࡼ࡮ࡩ࡭ࡧࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡘࡥࡴࡷ࡯ࡸࡸࠨཥ").format(bstack11l1l11ll1_opy_))
        except Exception as ex:
            logger.debug(bstack11ll111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡳࡧࡷࡶ࡮࡫ࡶࡪࡰࡪࠤࡆࡶࡰࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࢁࡽ࠯ࠢࡈࡶࡷࡵࡲࠡ࠯ࠣࡿࢂࠨས").format(result_type, str(ex)))
    return {}
@measure(event_name=EVENTS.bstack111ll111ll_opy_, stage=STAGE.bstack1111l1111_opy_, bstack11ll11ll11_opy_=bstack1lll11lll_opy_)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack1lll1l11_opy_
  bstack1ll1l1l1l1_opy_ = not (bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ཧ"), None) and bstack1lll11l111_opy_(
          threading.current_thread(), bstack11ll111_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩཨ"), None))
  bstack1l1l1lll1l_opy_ = not (bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫཀྵ"), None) and bstack1lll11l111_opy_(
          threading.current_thread(), bstack11ll111_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧཪ"), None))
  bstack1l111l1ll_opy_ = getattr(driver, bstack11ll111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭ཫ"), None) != True
  if not bstack11l11l11ll_opy_.bstack11l1111ll_opy_(CONFIG, bstack1lll1l11_opy_) or (bstack1l111l1ll_opy_ and bstack1ll1l1l1l1_opy_ and bstack1l1l1lll1l_opy_):
    logger.warning(bstack11ll111_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡶࡰࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮࠯ࠤཬ"))
    return {}
  try:
    bstack1l1l1l1l_opy_ = bstack11ll111_opy_ (u"ࠨࡣࡳࡴࠬ཭") in CONFIG and CONFIG.get(bstack11ll111_opy_ (u"ࠩࡤࡴࡵ࠭཮"), bstack11ll111_opy_ (u"ࠪࠫ཯"))
    session_id = getattr(driver, bstack11ll111_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨ཰"), None)
    if not session_id:
      logger.warning(bstack11ll111_opy_ (u"ࠧࡔ࡯ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡌࡈࠥ࡬࡯ࡶࡰࡧࠤ࡫ࡵࡲࠡࡦࡵ࡭ࡻ࡫ࡲཱࠣ"))
      return {bstack11ll111_opy_ (u"ࠨࡥࡳࡴࡲࡶིࠧ"): bstack11ll111_opy_ (u"ࠢࡏࡱࠣࡷࡪࡹࡳࡪࡱࡱࠤࡎࡊࠠࡧࡱࡸࡲࡩࠨཱི")}
    if bstack1l1l1l1l_opy_:
      try:
        bstack1ll111ll1_opy_ = {
              bstack11ll111_opy_ (u"ࠨࡶ࡫ࡎࡼࡺࡔࡰ࡭ࡨࡲུࠬ"): os.environ.get(bstack11ll111_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜ཱུ࡚ࠧ"), os.environ.get(bstack11ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧྲྀ"), bstack11ll111_opy_ (u"ࠫࠬཷ"))),
              bstack11ll111_opy_ (u"ࠬࡺࡨࡕࡧࡶࡸࡗࡻ࡮ࡖࡷ࡬ࡨࠬླྀ"): TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack11lll1ll1_opy_.current_hook_uuid(),
              bstack11ll111_opy_ (u"࠭ࡡࡶࡶ࡫ࡌࡪࡧࡤࡦࡴࠪཹ"): os.environ.get(bstack11ll111_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘེࠬ")),
              bstack11ll111_opy_ (u"ࠨࡵࡦࡥࡳ࡚ࡩ࡮ࡧࡶࡸࡦࡳࡰࠨཻ"): str(int(datetime.datetime.now().timestamp() * 1000)),
              bstack11ll111_opy_ (u"ࠩࡷ࡬ࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪོࠧ"): os.environ.get(bstack11ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨཽ"), bstack11ll111_opy_ (u"ࠫࠬཾ")),
              bstack11ll111_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬཿ"): kwargs.get(bstack11ll111_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡣࡰ࡯ࡰࡥࡳࡪྀࠧ"), None) or bstack11ll111_opy_ (u"ࠧࠨཱྀ")
          }
        if not hasattr(thread_local, bstack11ll111_opy_ (u"ࠨࡤࡤࡷࡪࡥࡡࡱࡲࡢࡥ࠶࠷ࡹࡠࡵࡦࡶ࡮ࡶࡴࠨྂ")):
            scripts = {bstack11ll111_opy_ (u"ࠩࡶࡧࡦࡴࠧྃ"): bstack11ll11llll_opy_.perform_scan}
            thread_local.base_app_a11y_script = scripts
        bstack11l1lll1ll_opy_ = copy.deepcopy(thread_local.base_app_a11y_script)
        bstack11l1lll1ll_opy_[bstack11ll111_opy_ (u"ࠪࡷࡨࡧ࡮ࠨ྄")] = bstack11l1lll1ll_opy_[bstack11ll111_opy_ (u"ࠫࡸࡩࡡ࡯ࠩ྅")] % json.dumps(bstack1ll111ll1_opy_)
        bstack11ll11llll_opy_.bstack11llll1l1_opy_(bstack11l1lll1ll_opy_)
        bstack11ll11llll_opy_.store()
        bstack1l11llllll_opy_ = driver.execute_script(bstack11ll11llll_opy_.perform_scan)
      except Exception as bstack11lllll1l_opy_:
        logger.info(bstack11ll111_opy_ (u"ࠧࡇࡰࡱ࡫ࡸࡱࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡣࡢࡰࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࠧ྆") + str(bstack11lllll1l_opy_))
        bstack1l11llllll_opy_ = {bstack11ll111_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ྇"): str(bstack11lllll1l_opy_)}
    else:
      bstack1l11llllll_opy_ = driver.execute_async_script(bstack11ll11llll_opy_.perform_scan, {bstack11ll111_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪࠧྈ"): kwargs.get(bstack11ll111_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࡠࡥࡲࡱࡲࡧ࡮ࡥࠩྉ"), None) or bstack11ll111_opy_ (u"ࠩࠪྊ")})
    return bstack1l11llllll_opy_
  except Exception as err:
    logger.error(bstack11ll111_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡲࡶࡰࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮࠯ࠢࡾࢁࠧྋ").format(str(err)))
    return {}