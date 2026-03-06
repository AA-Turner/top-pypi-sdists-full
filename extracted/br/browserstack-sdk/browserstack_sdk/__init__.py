# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
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
from browserstack_sdk.sdk_cli.bstack1ll1l111_opy_ import bstack11111lll1_opy_
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from browserstack_sdk.bstack11lll1lll1_opy_ import bstack11l111l1ll_opy_
from browserstack_sdk.bstack1l1lll11_opy_ import *
import time
import requests
from bstack_utils.constants import EVENTS, STAGE, bstack11l1ll11_opy_
from bstack_utils.messages import bstack1l111ll1l_opy_, bstack11lll1l11_opy_, bstack1l111111ll_opy_, bstack111l11lll1_opy_, bstack11l11l111l_opy_, bstack11l1lll11l_opy_
from bstack_utils.measure import measure
from bstack_utils.logger_utils import get_logger
from bstack_utils.helper import bstack11111ll1_opy_
from browserstack_sdk.bstack1l11llll11_opy_ import bstack1l11l1l11_opy_
logger = get_logger(__name__)
def bstack1l1ll11ll_opy_():
  global CONFIG
  headers = {
        bstack1111_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack1111_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack11111ll1_opy_(CONFIG, bstack11l1ll11_opy_)
  try:
    response = requests.get(bstack11l1ll11_opy_, headers=headers, proxies=proxies, timeout=2)
    if response.json():
      bstack1l111l1l1l_opy_ = response.json()[bstack1111_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1l111ll1l_opy_.format(response.json()))
      return bstack1l111l1l1l_opy_
    else:
      logger.debug(bstack11lll1l11_opy_.format(bstack1111_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack11lll1l11_opy_.format(e))
def bstack111l111l_opy_(hub_url):
  global CONFIG
  url = bstack1111_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack1111_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack1111_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack1111_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack11111ll1_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=(0.5, 1.0))
    latency = time.perf_counter() - start_time
    logger.debug(bstack1l111111ll_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack111l11lll1_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack111l1l1ll1_opy_, stage=STAGE.bstack111l1lllll_opy_)
def bstack11ll11ll1_opy_():
  try:
    global bstack11l1l1lll_opy_
    global CONFIG
    if bstack1111_opy_ (u"ࠫ࡭ࡻࡢࡓࡧࡪ࡭ࡴࡴࠧࡾ") in CONFIG and CONFIG[bstack1111_opy_ (u"ࠬ࡮ࡵࡣࡔࡨ࡫࡮ࡵ࡮ࠨࡿ")]:
      from bstack_utils.constants import bstack1ll1l11l_opy_
      bstack1l1l1ll111_opy_ = CONFIG[bstack1111_opy_ (u"࠭ࡨࡶࡤࡕࡩ࡬࡯࡯࡯ࠩࢀ")]
      if bstack1l1l1ll111_opy_ in bstack1ll1l11l_opy_:
        bstack11l1l1lll_opy_ = bstack1ll1l11l_opy_[bstack1l1l1ll111_opy_]
        logger.debug(bstack11l11l111l_opy_.format(bstack11l1l1lll_opy_))
        return
      else:
        logger.debug(bstack1111_opy_ (u"ࠢࡉࡷࡥࠤࡰ࡫ࡹࠡࠩࡾࢁࠬࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࡎࡕࡃࡡࡘࡖࡑࡥࡍࡂࡒ࠯ࠤ࡫ࡧ࡬࡭࡫ࡱ࡫ࠥࡨࡡࡤ࡭ࠣࡸࡴࠦ࡯ࡱࡶ࡬ࡱࡦࡲࠠࡩࡷࡥࠤࡩ࡫ࡴࡦࡥࡷ࡭ࡴࡴࠢࢁ").format(bstack1l1l1ll111_opy_))
    bstack1l111l1l1l_opy_ = bstack1l1ll11ll_opy_()
    from concurrent.futures import ThreadPoolExecutor, as_completed
    if bstack1l111l1l1l_opy_:
        with ThreadPoolExecutor(max_workers=len(bstack1l111l1l1l_opy_)) as executor:
            bstack1l111ll11_opy_ = {executor.submit(bstack111l111l_opy_, bstack1ll1l1111l_opy_): bstack1ll1l1111l_opy_ for bstack1ll1l1111l_opy_ in bstack1l111l1l1l_opy_}
            for future in as_completed(bstack1l111ll11_opy_):
                result = future.result()
                if result and result.get(bstack1111_opy_ (u"ࠨ࡮ࡤࡸࡪࡴࡣࡺࠩࢂ")) is not None:
                    bstack11l1l1lll_opy_ = result[bstack1111_opy_ (u"ࠩ࡫ࡹࡧࡥࡵࡳ࡮ࠪࢃ")]
                    logger.debug(bstack11l11l111l_opy_.format(bstack11l1l1lll_opy_))
                    return
        bstack11l1l1lll_opy_ = bstack1l111l1l1l_opy_[0]
        logger.debug(bstack11l11l111l_opy_.format(bstack11l1l1lll_opy_))
        return
  except Exception as e:
    logger.debug(bstack11l1lll11l_opy_.format(e))
from browserstack_sdk.bstack1l1l111l_opy_ import *
from browserstack_sdk.bstack1l11llll11_opy_ import *
from browserstack_sdk.bstack11l11llll1_opy_ import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.logger_utils import get_logger
from bstack_utils.measure import measure
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack1l1l11l111_opy_, stage=STAGE.bstack111l1lllll_opy_)
def bstack11ll1l1111_opy_():
    global bstack11l1l1lll_opy_
    try:
        bstack1l1ll1l1l_opy_ = bstack111l1ll1l1_opy_()
        bstack11l11l11_opy_(bstack1l1ll1l1l_opy_)
        hub_url = bstack1l1ll1l1l_opy_.get(bstack1111_opy_ (u"ࠥࡹࡷࡲࠢࢄ"), bstack1111_opy_ (u"ࠦࠧࢅ"))
        if hub_url.endswith(bstack1111_opy_ (u"ࠬ࠵ࡷࡥ࠱࡫ࡹࡧ࠭ࢆ")):
            hub_url = hub_url.rsplit(bstack1111_opy_ (u"࠭࠯ࡸࡦ࠲࡬ࡺࡨࠧࢇ"), 1)[0]
        if hub_url.startswith(bstack1111_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࠨ࢈")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack1111_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࠪࢉ")):
            hub_url = hub_url[8:]
        bstack11l1l1lll_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack111l1ll1l1_opy_():
    global CONFIG
    bstack11llll1ll_opy_ = CONFIG.get(bstack1111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢊ"), {}).get(bstack1111_opy_ (u"ࠪ࡫ࡷ࡯ࡤࡏࡣࡰࡩࠬࢋ"), bstack1111_opy_ (u"ࠫࡓࡕ࡟ࡈࡔࡌࡈࡤࡔࡁࡎࡇࡢࡔࡆ࡙ࡓࡆࡆࠪࢌ"))
    if not isinstance(bstack11llll1ll_opy_, str):
        raise ValueError(bstack1111_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡌࡸࡩࡥࠢࡱࡥࡲ࡫ࠠ࡮ࡷࡶࡸࠥࡨࡥࠡࡣࠣࡺࡦࡲࡩࡥࠢࡶࡸࡷ࡯࡮ࡨࠤࢍ"))
    try:
        bstack1l1ll1l1l_opy_ = bstack11l1lll1_opy_(bstack11llll1ll_opy_)
        return bstack1l1ll1l1l_opy_
    except Exception as e:
        logger.error(bstack1111_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡩࡵ࡭ࡩࠦࡤࡦࡶࡤ࡭ࡱࡹࠠ࠻ࠢࡾࢁࠧࢎ").format(str(e)))
        return {}
def bstack11l1lll1_opy_(bstack11llll1ll_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack1111_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ࢏")] or not CONFIG[bstack1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ࢐")]:
            raise ValueError(bstack1111_opy_ (u"ࠤࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠤࡴࡸࠠࡢࡥࡦࡩࡸࡹࠠ࡬ࡧࡼࠦ࢑"))
        url = bstack1lll1l1ll1_opy_ + bstack11llll1ll_opy_
        auth = (CONFIG[bstack1111_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ࢒")], CONFIG[bstack1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ࢓")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack1l1l1111l1_opy_ = json.loads(response.text)
            return bstack1l1l1111l1_opy_
    except ValueError as ve:
        logger.error(bstack1111_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡩࡵ࡭ࡩࠦࡤࡦࡶࡤ࡭ࡱࡹࠠ࠻ࠢࡾࢁࠧ࢔").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack1111_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡪࡶ࡮ࡪࠠࡥࡧࡷࡥ࡮ࡲࡳࠡ࠼ࠣࡿࢂࠨ࢕").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack11l11l11_opy_(bstack1l1l1111l_opy_):
    global CONFIG
    if bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ࢖") not in CONFIG or str(CONFIG[bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬࢗ")]).lower() == bstack1111_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ࢘"):
        CONFIG[bstack1111_opy_ (u"ࠪࡰࡴࡩࡡ࡭࢙ࠩ")] = False
    elif bstack1111_opy_ (u"ࠫ࡮ࡹࡔࡳ࡫ࡤࡰࡌࡸࡩࡥ࢚ࠩ") in bstack1l1l1111l_opy_:
        bstack11ll111ll_opy_ = CONFIG.get(bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴ࢛ࠩ"), {})
        logger.debug(bstack1111_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡸࡪࡵࡷ࡭ࡳ࡭ࠠ࡭ࡱࡦࡥࡱࠦ࡯ࡱࡶ࡬ࡳࡳࡹ࠺ࠡࠧࡶࠦ࢜"), bstack11ll111ll_opy_)
        bstack1ll111l1l_opy_ = bstack1l1l1111l_opy_.get(bstack1111_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡒࡦࡲࡨࡥࡹ࡫ࡲࡴࠤ࢝"), [])
        bstack111111l11_opy_ = bstack1111_opy_ (u"ࠣ࠮ࠥ࢞").join(bstack1ll111l1l_opy_)
        logger.debug(bstack1111_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡅࡸࡷࡹࡵ࡭ࠡࡴࡨࡴࡪࡧࡴࡦࡴࠣࡷࡹࡸࡩ࡯ࡩ࠽ࠤࠪࡹࠢ࢟"), bstack111111l11_opy_)
        bstack11lll1ll1_opy_ = {
            bstack1111_opy_ (u"ࠥࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧࢠ"): bstack1111_opy_ (u"ࠦࡦࡺࡳ࠮ࡴࡨࡴࡪࡧࡴࡦࡴࠥࢡ"),
            bstack1111_opy_ (u"ࠧ࡬࡯ࡳࡥࡨࡐࡴࡩࡡ࡭ࠤࢢ"): bstack1111_opy_ (u"ࠨࡴࡳࡷࡨࠦࢣ"),
            bstack1111_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࠭ࡳࡧࡳࡩࡦࡺࡥࡳࠤࢤ"): bstack111111l11_opy_
        }
        bstack11ll111ll_opy_.update(bstack11lll1ll1_opy_)
        logger.debug(bstack1111_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡖࡲࡧࡥࡹ࡫ࡤࠡ࡮ࡲࡧࡦࡲࠠࡰࡲࡷ࡭ࡴࡴࡳ࠻ࠢࠨࡷࠧࢥ"), bstack11ll111ll_opy_)
        CONFIG[bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢦ")] = bstack11ll111ll_opy_
        logger.debug(bstack1111_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡉ࡭ࡳࡧ࡬ࠡࡅࡒࡒࡋࡏࡇ࠻ࠢࠨࡷࠧࢧ"), CONFIG)
def bstack1ll1l11l1l_opy_():
    bstack1l1ll1l1l_opy_ = bstack111l1ll1l1_opy_()
    if not bstack1l1ll1l1l_opy_[bstack1111_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡖࡴ࡯ࠫࢨ")]:
      raise ValueError(bstack1111_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡗࡵࡰࠥ࡯ࡳࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡩࡶࡴࡳࠠࡨࡴ࡬ࡨࠥࡪࡥࡵࡣ࡬ࡰࡸ࠴ࠢࢩ"))
    return bstack1l1ll1l1l_opy_[bstack1111_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡘࡶࡱ࠭ࢪ")] + bstack1111_opy_ (u"ࠧࡀࡥࡤࡴࡸࡃࠧࢫ")
@measure(event_name=EVENTS.bstack111llll1l_opy_, stage=STAGE.bstack111l1lllll_opy_)
def bstack11l1l11lll_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack1111_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪࢬ")], CONFIG[bstack1111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬࢭ")])
        url = bstack1lll111l11_opy_
        logger.debug(bstack1111_opy_ (u"ࠥࡅࡹࡺࡥ࡮ࡲࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴࠢࡩࡶࡴࡳࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡔࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠣࡅࡕࡏࠢࢮ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack1111_opy_ (u"ࠦࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠥࢯ"): bstack1111_opy_ (u"ࠧࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠣࢰ")})
            if response.status_code == 200:
                bstack1111lll1_opy_ = json.loads(response.text)
                bstack1l111111l1_opy_ = bstack1111lll1_opy_.get(bstack1111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡸ࠭ࢱ"), [])
                if bstack1l111111l1_opy_:
                    bstack11ll1ll1ll_opy_ = bstack1l111111l1_opy_[0]
                    build_hashed_id = bstack11ll1ll1ll_opy_.get(bstack1111_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪࢲ"))
                    bstack1111llllll_opy_ = bstack1l1l1l1l11_opy_ + build_hashed_id
                    result.extend([build_hashed_id, bstack1111llllll_opy_])
                    logger.info(bstack111llllll_opy_.format(bstack1111llllll_opy_))
                    bstack1l1ll1llll_opy_ = CONFIG[bstack1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫࢳ")]
                    if bstack1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࢴ") in CONFIG:
                      bstack1l1ll1llll_opy_ += bstack1111_opy_ (u"ࠪࠤࠬࢵ") + CONFIG[bstack1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࢶ")]
                    if bstack1l1ll1llll_opy_ != bstack11ll1ll1ll_opy_.get(bstack1111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪࢷ")):
                      logger.debug(bstack11lll1ll_opy_.format(bstack11ll1ll1ll_opy_.get(bstack1111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫࢸ")), bstack1l1ll1llll_opy_))
                    return result
                else:
                    logger.debug(bstack1111_opy_ (u"ࠢࡂࡖࡖࠤ࠿ࠦࡎࡰࠢࡥࡹ࡮ࡲࡤࡴࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠱ࠦࢹ"))
            else:
                logger.debug(bstack1111_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴ࠰ࠥࢺ"))
        except Exception as e:
            logger.error(bstack1111_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࡶࠤ࠿ࠦࡻࡾࠤࢻ").format(str(e)))
    else:
        logger.debug(bstack1111_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡆࡓࡓࡌࡉࡈࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡶࡩࡹ࠴ࠠࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴ࠰ࠥࢼ"))
    return [None, None]
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack11l1lllll1_opy_ import bstack11l1lllll1_opy_, bstack1llll11l1_opy_, bstack1ll11lll11_opy_, bstack11ll111l1_opy_
from bstack_utils.measure import bstack1ll1l11ll1_opy_
from bstack_utils.measure import measure
from bstack_utils.percy import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack11lll1llll_opy_ import bstack111l111ll1_opy_
from bstack_utils.messages import *
from bstack_utils import logger_utils
from bstack_utils.constants import *
from bstack_utils.helper import bstack1lllllll1_opy_, bstack1llll1l1ll_opy_, bstack11111l1ll_opy_, bstack1lll11lll1_opy_, \
  bstack1ll11ll11l_opy_, \
  Notset, is_robot_playwright_installed, bstack1ll1l1ll11_opy_, \
  bstack1llllll1l_opy_, bstack1l1lll1l1l_opy_, bstack1l1l1lll1l_opy_, bstack1ll11111_opy_, bstack1l1ll11l_opy_, bstack1lllll11l1_opy_, \
  bstack1l1l1ll1l1_opy_, \
  bstack1ll1ll1ll1_opy_, bstack1llll11l11_opy_, bstack1l1l1ll11_opy_, bstack1l11ll111_opy_, \
  bstack1l1lll111_opy_, bstack11lllll1ll_opy_, bstack11ll1l1l1l_opy_, bstack11l1l1l11_opy_, bstack1ll1l11lll_opy_
from bstack_utils.bstack11l11lll1l_opy_ import bstack1l1ll1l1ll_opy_
from bstack_utils.bstack111l1llll1_opy_ import bstack1ll11l1111_opy_, bstack1ll11l1l1_opy_
from bstack_utils.bstack1ll1lll111_opy_ import bstack111l1lll_opy_
from bstack_utils.session_utils import bstack1l1lllll1l_opy_, bstack11lllll111_opy_
from bstack_utils.bstack1l111l111_opy_ import bstack1l111l111_opy_
from bstack_utils.bstack11l1ll11l1_opy_ import bstack11lllll1l1_opy_
from bstack_utils.proxy import bstack1l111lllll_opy_, bstack11111ll1_opy_, bstack1ll111l111_opy_, bstack111l11l11_opy_
from bstack_utils.bstack1lllllll11_opy_ import bstack11ll1l11_opy_, bstack11l1l111ll_opy_
import bstack_utils.bstack1ll111111l_opy_ as bstack1l111l1l_opy_
import bstack_utils.bstack1l1ll1l11l_opy_ as bstack1ll1ll11l1_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.utils.bstack1llll11lll_opy_ import bstack111l1l1111_opy_
from bstack_utils.bstack1l11111ll1_opy_ import bstack11l111lll1_opy_
from bstack_utils.bstack111ll1ll1_opy_ import bstack1l1111l111_opy_
from bstack_utils.bstack1ll1l11ll1_opy_ import bstack1l11l1ll_opy_
if os.getenv(bstack1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡉࡑࡒࡏࡘ࠭ࢽ")):
  cli.bstack111l11l1l_opy_()
else:
  os.environ[bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡊࡒࡓࡐ࡙ࠧࢾ")] = bstack1111_opy_ (u"࠭ࡴࡳࡷࡨࠫࢿ")
bstack1lll11l1l1_opy_ = bstack1111_opy_ (u"ࠧࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠠࠡ࡫ࡩࠬࡵࡧࡧࡦࠢࡀࡁࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠠࡼ࡞ࡱࠤࠥࠦࡴࡳࡻࡾࡠࡳࠦࡣࡰࡰࡶࡸࠥ࡬ࡳࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࡡ࠭ࡦࡴ࡞ࠪ࠭ࡀࡢ࡮ࠡࠢࠣࠤࠥ࡬ࡳ࠯ࡣࡳࡴࡪࡴࡤࡇ࡫࡯ࡩࡘࡿ࡮ࡤࠪࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠬࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡳࡣ࡮ࡴࡤࡦࡺࠬࠤ࠰ࠦࠢ࠻ࠤࠣ࠯ࠥࡐࡓࡐࡐ࠱ࡷࡹࡸࡩ࡯ࡩ࡬ࡪࡾ࠮ࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࠬࡦࡽࡡࡪࡶࠣࡲࡪࡽࡐࡢࡩࡨ࠶࠳࡫ࡶࡢ࡮ࡸࡥࡹ࡫ࠨࠣࠪࠬࠤࡂࡄࠠࡼࡿࠥ࠰ࠥࡢࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡨࡧࡷࡗࡪࡹࡳࡪࡱࡱࡈࡪࡺࡡࡪ࡮ࡶࠦࢂࡢࠧࠪࠫࠬ࡟ࠧ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠣ࡟ࠬࠤ࠰ࠦࠢ࠭࡞࡟ࡲࠧ࠯࡜࡯ࠢࠣࠤࠥࢃࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡽ࡝ࡰࠣࠤ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠧࣀ")
LAUNCH_PATCH_ROBOT_PLAYWRIGHT = bstack1111_opy_ (u"ࠨ࡞ࡱ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࡢ࡮ࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡰࡢࡶ࡫ࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳࡞࡞ࡱࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠴ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡶ࡟ࡪࡰࡧࡩࡽࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠴ࡠࡠࡳࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡹ࡬ࡪࡥࡨࠬ࠵࠲ࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࠬࡠࡳࡩ࡯࡯ࡵࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬ࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ࠭ࡀࡢ࡮ࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮࡭ࡣࡸࡲࡨ࡮ࠠ࠾ࠢࡤࡷࡾࡴࡣࠡࠪ࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴࠫࠣࡁࡃࠦࡻ࡝ࡰ࡯ࡩࡹࠦࡣࡢࡲࡶ࠿ࡡࡴࡴࡳࡻࠣࡿࡡࡴࡣࡢࡲࡶࠤࡂࠦࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠪ࡞ࡱࠤࠥࢃࠠࡤࡣࡷࡧ࡭࠮ࡥࡹࠫࠣࡿࡡࡴࠠࠡࠢࠣࢁࡡࡴࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡣࡺࡥ࡮ࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮ࡤࡱࡱࡲࡪࡩࡴࠩࡽ࡟ࡲࠥࠦࠠࠡࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸ࠿ࠦࡠࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠦࡾࡩࡳࡩ࡯ࡥࡧࡘࡖࡎࡉ࡯࡮ࡲࡲࡲࡪࡴࡴࠩࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡦࡥࡵࡹࠩࠪࡿࡣ࠰ࡡࡴࠠࠡࠢࠣ࠲࠳࠴࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸࡢ࡮ࠡࠢࢀ࠭ࡡࡴࡽ࡝ࡰࡦࡳࡳࡹࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡧࡴࡴ࡮ࡦࡥࡷࠤࡂࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺ࠮ࡣ࡫ࡱࡨ࠭࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠮ࡁ࡜࡯࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭࠯ࡥࡲࡲࡳ࡫ࡣࡵࠢࡀࠤࡦࡹࡹ࡯ࡥࠣࠬࡨࡵ࡮࡯ࡧࡦࡸࡔࡶࡴࡪࡱࡱࡷ࠮ࠦ࠽࠿ࠢࡾࡠࡳࠦࠠ࡭ࡧࡷࠤࡨࡧࡰࡴ࠽࡟ࡲࠥࠦࡴࡳࡻࠣࡿࡡࡴࠠࠡࠢࠣࡧࡦࡶࡳࠡ࠿ࠣࡎࡘࡕࡎ࠯ࡲࡤࡶࡸ࡫ࠨࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷ࠮ࡢ࡮ࠡࠢࢀࠤࡨࡧࡴࡤࡪࠫࡩࡽ࠯ࠠࡼ࡞ࡱࠤࠥࢃ࡜࡯ࠢࠣࡧࡴࡴࡳࡵࠢࡰࡳࡩ࡯ࡦࡪࡧࡧࡉࡳࡪࡰࡰ࡫ࡱࡸࠥࡃࠠࡡࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࡣࠤ࠰ࠦࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭ࡀࡢ࡮ࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤ࠳࠴࠮ࡤࡱࡱࡲࡪࡩࡴࡐࡲࡷ࡭ࡴࡴࡳ࠭࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࡝ࡰࠣࠤࢂ࠯࡜࡯ࡿ࡟ࡲ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵࡜࡯ࠩࣁ")
from ._version import __version__
bstack1lll111ll_opy_ = None
CONFIG = {}
bstack11l11ll1l1_opy_ = {}
bstack1111llll1_opy_ = {}
bstack1l1l111l11_opy_ = None
bstack1ll1111ll_opy_ = None
bstack1lll11ll1_opy_ = None
bstack11l11ll1_opy_ = -1
bstack11llllll_opy_ = 0
bstack1lll11111_opy_ = bstack1l11ll11l1_opy_
bstack1l1l11l1l_opy_ = 1
bstack1lll11l1ll_opy_ = False
bstack111lllll11_opy_ = False
bstack111llll11l_opy_ = bstack1111_opy_ (u"ࠩࠪࣂ")
bstack111lllll1l_opy_ = bstack1111_opy_ (u"ࠪࠫࣃ")
bstack1l11l11ll1_opy_ = False
bstack1111ll1l_opy_ = True
bstack11l1l11l11_opy_ = False
bstack1ll1l11l1_opy_ = bstack1111_opy_ (u"ࠫࠬࣄ")
bstack1ll11111l1_opy_ = []
bstack111l1l11l_opy_ = threading.Lock()
bstack1l1l1lll1_opy_ = threading.Lock()
bstack1ll1l1l11_opy_ = None
bstack11l1l1lll_opy_ = bstack1111_opy_ (u"ࠬ࠭ࣅ")
bstack11l1111l1_opy_ = False
bstack11l11111l_opy_ = None
bstack1lll11l11l_opy_ = None
bstack1ll1ll111l_opy_ = None
bstack11ll1l1l1_opy_ = -1
bstack1111l1l11_opy_ = os.path.join(os.path.expanduser(bstack1111_opy_ (u"࠭ࡾࠨࣆ")), bstack1111_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧࣇ"), bstack1111_opy_ (u"ࠨ࠰ࡵࡳࡧࡵࡴ࠮ࡴࡨࡴࡴࡸࡴ࠮ࡪࡨࡰࡵ࡫ࡲ࠯࡬ࡶࡳࡳ࠭ࣈ"))
bstack1ll11l11_opy_ = 0
bstack111ll1l1ll_opy_ = 0
bstack1ll11lll1l_opy_ = []
bstack1l1ll11lll_opy_ = []
ROBOT_PYTHON_ERRORS = []
bstack1lll111lll_opy_ = []
bstack111ll1111l_opy_ = bstack1111_opy_ (u"ࠩࠪࣉ")
bstack1l1l11ll11_opy_ = bstack1111_opy_ (u"ࠪࠫ࣊")
bstack1ll1llll1_opy_ = False
bstack1l1l111111_opy_ = False
bstack1l1l1l1ll_opy_ = {}
bstack1llll11ll_opy_ = {}
bstack11l1111l11_opy_ = None
bstack1l111ll1_opy_ = None
bstack1l1l11l1_opy_ = None
bstack11l11111ll_opy_ = None
bstack11l1ll111_opy_ = None
bstack111l1111l_opy_ = None
bstack1lll1111ll_opy_ = None
bstack1lll11lll_opy_ = None
bstack1l11lll1ll_opy_ = None
bstack11ll1lll1l_opy_ = None
bstack1llllll111_opy_ = None
bstack111l111111_opy_ = None
bstack1llll1ll1l_opy_ = None
bstack1111ll1lll_opy_ = None
bstack1lll1ll11_opy_ = None
bstack1ll11lllll_opy_ = None
bstack1llll11111_opy_ = None
bstack1l1ll1ll_opy_ = None
bstack1ll1l1ll_opy_ = None
bstack111lll1l1l_opy_ = None
bstack1l11llllll_opy_ = None
bstack111llll1l1_opy_ = None
bstack1l111111_opy_ = None
thread_local = threading.local()
bstack1l1111ll1_opy_ = False
bstack111ll1l1_opy_ = bstack1111_opy_ (u"ࠦࠧ࣋")
_1l1ll1ll11_opy_ = None
logger = logger_utils.get_logger(__name__, bstack1lll11111_opy_)
bstack11llllll1l_opy_ = logger_utils.bstack1ll11llll1_opy_(__name__)
global_config = Config.get_instance()
percy = bstack1l111llll1_opy_()
bstack1l1l1ll1ll_opy_ = bstack111l111ll1_opy_()
bstack11111lll_opy_ = bstack11l11llll1_opy_()
def bstack1ll1l1lll1_opy_():
  global CONFIG
  global bstack1ll1llll1_opy_
  global global_config
  testContextOptions = bstack1ll1llll11_opy_(CONFIG)
  if bstack1ll11ll11l_opy_(CONFIG):
    if (bstack1111_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ࣌") in testContextOptions and str(testContextOptions[bstack1111_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ࣍")]).lower() == bstack1111_opy_ (u"ࠧࡵࡴࡸࡩࠬ࣎")):
      bstack1ll1llll1_opy_ = True
      global_config.bstack1l11l111_opy_(True)
    global_config.bstack1l11l11l_opy_(testContextOptions.get(bstack1111_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷ࣏ࠬ"), False))
  else:
    bstack1ll1llll1_opy_ = True
    global_config.bstack1l11l111_opy_(True)
    global_config.bstack1l11l11l_opy_(True)
def bstack1l111llll_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1l111ll11l_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack11l11ll1ll_opy_():
  global bstack1llll11ll_opy_
  args = sys.argv
  for i in range(len(args)):
    if bstack1111_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡦࡳࡳ࡬ࡩࡨࡨ࡬ࡰࡪࠨ࣐") == args[i].lower() or bstack1111_opy_ (u"ࠥ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡮ࡧ࡫ࡪ࣑ࠦ") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      bstack1llll11ll_opy_[bstack1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ࣒")] = path
      return path
  return None
bstack11lllll11_opy_ = re.compile(bstack1111_opy_ (u"ࡷࠨ࠮ࠫࡁ࡟ࠨࢀ࠮࠮ࠫࡁࠬࢁ࠳࠰࠿࣓ࠣ"))
def bstack111l1111ll_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack11lllll11_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack1111_opy_ (u"ࠨࠤࡼࠤࣔ") + group + bstack1111_opy_ (u"ࠢࡾࠤࣕ"), os.environ.get(group))
  return value
def bstack111llllll1_opy_():
  global bstack1l111111_opy_
  if bstack1l111111_opy_ is None:
        bstack1l111111_opy_ = bstack11l11ll1ll_opy_()
  bstack1111lll1l_opy_ = bstack1l111111_opy_
  if bstack1111lll1l_opy_ and os.path.exists(os.path.abspath(bstack1111lll1l_opy_)):
    fileName = bstack1111lll1l_opy_
  if bstack1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬࣖ") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࡠࡈࡌࡐࡊ࠭ࣗ")])) and not bstack1111_opy_ (u"ࠪࡪ࡮ࡲࡥࡏࡣࡰࡩࠬࣘ") in locals():
    fileName = os.environ[bstack1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨࣙ")]
  if bstack1111_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡑࡥࡲ࡫ࠧࣚ") in locals():
    bstack1llll_opy_ = os.path.abspath(fileName)
  else:
    bstack1llll_opy_ = bstack1111_opy_ (u"࠭ࠧࣛ")
  bstack1ll11l111l_opy_ = os.getcwd()
  bstack11l11ll11_opy_ = bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪࣜ")
  bstack1l1l1lllll_opy_ = bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺࡣࡰࡰࠬࣝ")
  while (not os.path.exists(bstack1llll_opy_)) and bstack1ll11l111l_opy_ != bstack1111_opy_ (u"ࠤࠥࣞ"):
    bstack1llll_opy_ = os.path.join(bstack1ll11l111l_opy_, bstack11l11ll11_opy_)
    if not os.path.exists(bstack1llll_opy_):
      bstack1llll_opy_ = os.path.join(bstack1ll11l111l_opy_, bstack1l1l1lllll_opy_)
    if bstack1ll11l111l_opy_ != os.path.dirname(bstack1ll11l111l_opy_):
      bstack1ll11l111l_opy_ = os.path.dirname(bstack1ll11l111l_opy_)
    else:
      bstack1ll11l111l_opy_ = bstack1111_opy_ (u"ࠥࠦࣟ")
  bstack1l111111_opy_ = bstack1llll_opy_ if os.path.exists(bstack1llll_opy_) else None
  return bstack1l111111_opy_
def bstack1ll1111ll1_opy_(config):
    if bstack1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࠫ࣠") in config:
      config[bstack1111_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ࣡")] = config[bstack1111_opy_ (u"࠭ࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬࠭࣢")]
    if bstack1111_opy_ (u"ࠧࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭ࡏࡱࡶ࡬ࡳࡳࡹࣣࠧ") in config:
      config[bstack1111_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬࣤ")] = config[bstack1111_opy_ (u"ࠩࡷࡩࡸࡺࡒࡦࡲࡲࡶࡹ࡯࡮ࡨࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣥ")]
def bstack11l1llll1l_opy_():
  bstack1llll_opy_ = bstack111llllll1_opy_()
  if not os.path.exists(bstack1llll_opy_):
    bstack1ll1ll11_opy_(
      bstack1ll1ll11l_opy_.format(os.getcwd()))
  try:
    with open(bstack1llll_opy_, bstack1111_opy_ (u"ࠪࡶࣦࠬ")) as stream:
      yaml.add_implicit_resolver(bstack1111_opy_ (u"ࠦࠦࡶࡡࡵࡪࡨࡼࠧࣧ"), bstack11lllll11_opy_)
      yaml.add_constructor(bstack1111_opy_ (u"ࠧࠧࡰࡢࡶ࡫ࡩࡽࠨࣨ"), bstack111l1111ll_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      bstack1ll1111ll1_opy_(config)
      return config
  except:
    with open(bstack1llll_opy_, bstack1111_opy_ (u"࠭ࡲࠨࣩ")) as stream:
      try:
        config = yaml.safe_load(stream)
        bstack1ll1111ll1_opy_(config)
        return config
      except yaml.YAMLError as exc:
        bstack1ll1ll11_opy_(bstack11l111ll1l_opy_.format(str(exc)))
def bstack1lll111l1l_opy_(config):
  bstack11llll11_opy_ = bstack11ll11111_opy_(config)
  for option in list(bstack11llll11_opy_):
    if option.lower() in bstack11l1111lll_opy_ and option != bstack11l1111lll_opy_[option.lower()]:
      bstack11llll11_opy_[bstack11l1111lll_opy_[option.lower()]] = bstack11llll11_opy_[option]
      del bstack11llll11_opy_[option]
  return config
def bstack1l1111ll11_opy_():
  global bstack1111llll1_opy_
  for key, bstack11lll111_opy_ in bstack1l1llll1l1_opy_.items():
    if isinstance(bstack11lll111_opy_, list):
      for var in bstack11lll111_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1111llll1_opy_[key] = os.environ[var]
          break
    elif bstack11lll111_opy_ in os.environ and os.environ[bstack11lll111_opy_] and str(os.environ[bstack11lll111_opy_]).strip():
      bstack1111llll1_opy_[key] = os.environ[bstack11lll111_opy_]
  if bstack1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩ࣪") in os.environ:
    bstack1111llll1_opy_[bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ࣫")] = {}
    bstack1111llll1_opy_[bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭࣬")][bstack1111_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ࣭ࠬ")] = os.environ[bstack1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࣮࠭")]
def bstack1lll1111l1_opy_():
  global bstack11l11ll1l1_opy_
  global bstack1ll1l11l1_opy_
  global bstack1llll11ll_opy_
  bstack1l1l1l11_opy_ = []
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) - 1 and bstack1111_opy_ (u"ࠬ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ࣯").lower() == val.lower():
      bstack11l11ll1l1_opy_[bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࣰࠪ")] = {}
      bstack11l11ll1l1_opy_[bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࣱࠫ")][bstack1111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࣲࠪ")] = sys.argv[idx + 1]
      bstack1l1l1l11_opy_.extend([idx, idx + 1])
      break
  for key, bstack1ll1l11ll_opy_ in bstack1l111l11l_opy_.items():
    if isinstance(bstack1ll1l11ll_opy_, list):
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        for var in bstack1ll1l11ll_opy_:
          if bstack1111_opy_ (u"ࠩ࠰࠱ࠬࣳ") + var.lower() == val.lower() and key not in bstack11l11ll1l1_opy_:
            bstack11l11ll1l1_opy_[key] = sys.argv[idx + 1]
            bstack1ll1l11l1_opy_ += bstack1111_opy_ (u"ࠪࠤ࠲࠳ࠧࣴ") + var + bstack1111_opy_ (u"ࠫࠥ࠭ࣵ") + shlex.quote(sys.argv[idx + 1])
            bstack1ll1l11lll_opy_(bstack1llll11ll_opy_, key, sys.argv[idx + 1])
            bstack1l1l1l11_opy_.extend([idx, idx + 1])
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        if bstack1111_opy_ (u"ࠬ࠳࠭ࠨࣶ") + bstack1ll1l11ll_opy_.lower() == val.lower() and key not in bstack11l11ll1l1_opy_:
          bstack11l11ll1l1_opy_[key] = sys.argv[idx + 1]
          bstack1ll1l11l1_opy_ += bstack1111_opy_ (u"࠭ࠠ࠮࠯ࠪࣷ") + bstack1ll1l11ll_opy_ + bstack1111_opy_ (u"ࠧࠡࠩࣸ") + shlex.quote(sys.argv[idx + 1])
          bstack1ll1l11lll_opy_(bstack1llll11ll_opy_, key, sys.argv[idx + 1])
          bstack1l1l1l11_opy_.extend([idx, idx + 1])
  for idx in sorted(set(bstack1l1l1l11_opy_), reverse=True):
    if idx < len(sys.argv):
      del sys.argv[idx]
def bstack11l1ll1ll1_opy_(config):
  bstack11lll1l11l_opy_ = config.keys()
  for bstack11l1l1l1l_opy_, bstack1l1111111l_opy_ in bstack1ll11l11l_opy_.items():
    if bstack1l1111111l_opy_ in bstack11lll1l11l_opy_:
      config[bstack11l1l1l1l_opy_] = config[bstack1l1111111l_opy_]
      del config[bstack1l1111111l_opy_]
  for bstack11l1l1l1l_opy_, bstack1l1111111l_opy_ in bstack1lll1l1l1l_opy_.items():
    if isinstance(bstack1l1111111l_opy_, list):
      for bstack1111lllll_opy_ in bstack1l1111111l_opy_:
        if bstack1111lllll_opy_ in bstack11lll1l11l_opy_:
          config[bstack11l1l1l1l_opy_] = config[bstack1111lllll_opy_]
          del config[bstack1111lllll_opy_]
          break
    elif bstack1l1111111l_opy_ in bstack11lll1l11l_opy_:
      config[bstack11l1l1l1l_opy_] = config[bstack1l1111111l_opy_]
      del config[bstack1l1111111l_opy_]
  for bstack1111lllll_opy_ in list(config):
    for bstack1l1llll1_opy_ in bstack1111lll1l1_opy_:
      if bstack1111lllll_opy_.lower() == bstack1l1llll1_opy_.lower() and bstack1111lllll_opy_ != bstack1l1llll1_opy_:
        config[bstack1l1llll1_opy_] = config[bstack1111lllll_opy_]
        del config[bstack1111lllll_opy_]
  bstack1l1l1l1l1l_opy_ = [{}]
  if not config.get(bstack1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࣹࠫ")):
    config[bstack1111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࣺࠬ")] = [{}]
  bstack1l1l1l1l1l_opy_ = config[bstack1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣻ")]
  for platform in bstack1l1l1l1l1l_opy_:
    for bstack1111lllll_opy_ in list(platform):
      for bstack1l1llll1_opy_ in bstack1111lll1l1_opy_:
        if bstack1111lllll_opy_.lower() == bstack1l1llll1_opy_.lower() and bstack1111lllll_opy_ != bstack1l1llll1_opy_:
          platform[bstack1l1llll1_opy_] = platform[bstack1111lllll_opy_]
          del platform[bstack1111lllll_opy_]
  for bstack11l1l1l1l_opy_, bstack1l1111111l_opy_ in bstack1lll1l1l1l_opy_.items():
    for platform in bstack1l1l1l1l1l_opy_:
      if isinstance(bstack1l1111111l_opy_, list):
        for bstack1111lllll_opy_ in bstack1l1111111l_opy_:
          if bstack1111lllll_opy_ in platform:
            platform[bstack11l1l1l1l_opy_] = platform[bstack1111lllll_opy_]
            del platform[bstack1111lllll_opy_]
            break
      elif bstack1l1111111l_opy_ in platform:
        platform[bstack11l1l1l1l_opy_] = platform[bstack1l1111111l_opy_]
        del platform[bstack1l1111111l_opy_]
  for bstack1l1ll1lll1_opy_ in bstack1l11l11l11_opy_:
    if bstack1l1ll1lll1_opy_ in config:
      if not bstack1l11l11l11_opy_[bstack1l1ll1lll1_opy_] in config:
        config[bstack1l11l11l11_opy_[bstack1l1ll1lll1_opy_]] = {}
      config[bstack1l11l11l11_opy_[bstack1l1ll1lll1_opy_]].update(config[bstack1l1ll1lll1_opy_])
      del config[bstack1l1ll1lll1_opy_]
  for platform in bstack1l1l1l1l1l_opy_:
    for bstack1l1ll1lll1_opy_ in bstack1l11l11l11_opy_:
      if bstack1l1ll1lll1_opy_ in list(platform):
        if not bstack1l11l11l11_opy_[bstack1l1ll1lll1_opy_] in platform:
          platform[bstack1l11l11l11_opy_[bstack1l1ll1lll1_opy_]] = {}
        platform[bstack1l11l11l11_opy_[bstack1l1ll1lll1_opy_]].update(platform[bstack1l1ll1lll1_opy_])
        del platform[bstack1l1ll1lll1_opy_]
  config = bstack1lll111l1l_opy_(config)
  return config
def bstack11ll111111_opy_(config):
  global bstack111lllll1l_opy_
  bstack1l1111llll_opy_ = False
  if bstack1111_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨࣼ") in config and str(config[bstack1111_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩࣽ")]).lower() != bstack1111_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬࣾ"):
    if bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫࣿ") not in config or str(config[bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬऀ")]).lower() == bstack1111_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨँ"):
      config[bstack1111_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩं")] = False
    else:
      bstack1l1ll1l1l_opy_ = bstack111l1ll1l1_opy_()
      if bstack1111_opy_ (u"ࠫ࡮ࡹࡔࡳ࡫ࡤࡰࡌࡸࡩࡥࠩः") in bstack1l1ll1l1l_opy_:
        if not bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩऄ") in config:
          config[bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪअ")] = {}
        config[bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫआ")][bstack1111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪइ")] = bstack1111_opy_ (u"ࠩࡤࡸࡸ࠳ࡲࡦࡲࡨࡥࡹ࡫ࡲࠨई")
        bstack1l1111llll_opy_ = True
        bstack111lllll1l_opy_ = config[bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧउ")].get(bstack1111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ऊ"))
  if bstack1ll11ll11l_opy_(config) and bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩऋ") in config and str(config[bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪऌ")]).lower() != bstack1111_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ऍ") and not bstack1l1111llll_opy_:
    if not bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬऎ") in config:
      config[bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ए")] = {}
    if not config[bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧऐ")].get(bstack1111_opy_ (u"ࠫࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠨऑ")) and not bstack1111_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऒ") in config[bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪओ")]:
      current_time = datetime.datetime.now()
      bstack1lllll11_opy_ = current_time.strftime(bstack1111_opy_ (u"ࠧࠦࡦࡢࠩࡧࡥࠥࡉࠧࡐࠫऔ"))
      hostname = socket.gethostname()
      bstack1lll111l_opy_ = bstack1111_opy_ (u"ࠨࠩक").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1111_opy_ (u"ࠩࡾࢁࡤࢁࡽࡠࡽࢀࠫख").format(bstack1lllll11_opy_, hostname, bstack1lll111l_opy_)
      config[bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧग")][bstack1111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭घ")] = identifier
    bstack111lllll1l_opy_ = config[bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩङ")].get(bstack1111_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨच"))
  return config
def bstack11l1l1ll1l_opy_():
  bstack111l1ll11l_opy_ =  bstack1ll11111_opy_()[bstack1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷ࠭छ")]
  return bstack111l1ll11l_opy_ if bstack111l1ll11l_opy_ else -1
def bstack11l1l1l11l_opy_(bstack111l1ll11l_opy_):
  global CONFIG
  if not bstack1111_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪज") in CONFIG[bstack1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫझ")]:
    return
  CONFIG[bstack1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬञ")] = CONFIG[bstack1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ट")].replace(
    bstack1111_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧठ"),
    str(bstack111l1ll11l_opy_)
  )
def bstack1l1l1l1l1_opy_():
  global CONFIG
  if not bstack1111_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬड") in CONFIG[bstack1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩढ")]:
    return
  current_time = datetime.datetime.now()
  bstack1lllll11_opy_ = current_time.strftime(bstack1111_opy_ (u"ࠨࠧࡧ࠱ࠪࡨ࠭ࠦࡊ࠽ࠩࡒ࠭ण"))
  CONFIG[bstack1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫत")] = CONFIG[bstack1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬथ")].replace(
    bstack1111_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪद"),
    bstack1lllll11_opy_
  )
def bstack111ll1111_opy_():
  global CONFIG
  if bstack1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧध") in CONFIG and not bool(CONFIG[bstack1111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨन")]):
    del CONFIG[bstack1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऩ")]
    return
  if not bstack1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪप") in CONFIG:
    CONFIG[bstack1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫफ")] = bstack1111_opy_ (u"ࠪࠧࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ब")
  if bstack1111_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪभ") in CONFIG[bstack1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧम")]:
    bstack1l1l1l1l1_opy_()
    os.environ[bstack1111_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪय")] = CONFIG[bstack1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩर")]
  if not bstack1111_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪऱ") in CONFIG[bstack1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫल")]:
    return
  bstack111l1ll11l_opy_ = bstack1111_opy_ (u"ࠪࠫळ")
  bstack1l1ll11111_opy_ = bstack11l1l1ll1l_opy_()
  if bstack1l1ll11111_opy_ != -1:
    bstack111l1ll11l_opy_ = bstack1111_opy_ (u"ࠫࡈࡏࠠࠨऴ") + str(bstack1l1ll11111_opy_)
  if bstack111l1ll11l_opy_ == bstack1111_opy_ (u"ࠬ࠭व"):
    bstack1l1lllllll_opy_ = bstack11l1lll1ll_opy_(CONFIG[bstack1111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩश")])
    if bstack1l1lllllll_opy_ != -1:
      bstack111l1ll11l_opy_ = str(bstack1l1lllllll_opy_)
  if bstack111l1ll11l_opy_:
    bstack11l1l1l11l_opy_(bstack111l1ll11l_opy_)
    os.environ[bstack1111_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫष")] = CONFIG[bstack1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪस")]
def bstack11l11l1ll1_opy_(bstack11l1l11ll_opy_, bstack1ll11ll1ll_opy_, path):
  bstack1ll1ll1lll_opy_ = {
    bstack1111_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ह"): bstack1ll11ll1ll_opy_
  }
  if os.path.exists(path):
    bstack1l1lll1l11_opy_ = json.load(open(path, bstack1111_opy_ (u"ࠪࡶࡧ࠭ऺ")))
  else:
    bstack1l1lll1l11_opy_ = {}
  bstack1l1lll1l11_opy_[bstack11l1l11ll_opy_] = bstack1ll1ll1lll_opy_
  with open(path, bstack1111_opy_ (u"ࠦࡼ࠱ࠢऻ")) as outfile:
    json.dump(bstack1l1lll1l11_opy_, outfile)
def bstack11l1lll1ll_opy_(bstack11l1l11ll_opy_):
  bstack11l1l11ll_opy_ = str(bstack11l1l11ll_opy_)
  bstack11llll111_opy_ = os.path.join(os.path.expanduser(bstack1111_opy_ (u"ࠬࢄ़ࠧ")), bstack1111_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ऽ"))
  try:
    if not os.path.exists(bstack11llll111_opy_):
      os.makedirs(bstack11llll111_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1111_opy_ (u"ࠧࡿࠩा")), bstack1111_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨि"), bstack1111_opy_ (u"ࠩ࠱ࡦࡺ࡯࡬ࡥ࠯ࡱࡥࡲ࡫࠭ࡤࡣࡦ࡬ࡪ࠴ࡪࡴࡱࡱࠫी"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1111_opy_ (u"ࠪࡻࠬु")):
        pass
      with open(file_path, bstack1111_opy_ (u"ࠦࡼ࠱ࠢू")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1111_opy_ (u"ࠬࡸࠧृ")) as bstack1llllllll_opy_:
      bstack111lll1111_opy_ = json.load(bstack1llllllll_opy_)
    if bstack11l1l11ll_opy_ in bstack111lll1111_opy_:
      bstack11l1111l_opy_ = bstack111lll1111_opy_[bstack11l1l11ll_opy_][bstack1111_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪॄ")]
      bstack11llll11l1_opy_ = int(bstack11l1111l_opy_) + 1
      bstack11l11l1ll1_opy_(bstack11l1l11ll_opy_, bstack11llll11l1_opy_, file_path)
      return bstack11llll11l1_opy_
    else:
      bstack11l11l1ll1_opy_(bstack11l1l11ll_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warning(bstack111ll111l1_opy_.format(str(e)))
    return -1
def bstack1l11lll1l_opy_(config):
  if not config[bstack1111_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩॅ")] or not config[bstack1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫॆ")]:
    return True
  else:
    return False
def bstack1lll1111l_opy_(config, index=0):
  global bstack1l11l11ll1_opy_
  bstack11l1l1ll_opy_ = {}
  caps = bstack11l11l1l1_opy_ + bstack11l11111_opy_
  if config.get(bstack1111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭े"), False):
    bstack11l1l1ll_opy_[bstack1111_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧै")] = True
    bstack11l1l1ll_opy_[bstack1111_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࡐࡲࡷ࡭ࡴࡴࡳࠨॉ")] = config.get(bstack1111_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩॊ"), {})
  if bstack1l11l11ll1_opy_:
    caps += bstack1l111l1lll_opy_
  for key in config:
    if key in caps + [bstack1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩो")]:
      continue
    bstack11l1l1ll_opy_[key] = config[key]
  if bstack1111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪौ") in config:
    for bstack1l1ll111l1_opy_ in config[bstack1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶ्ࠫ")][index]:
      if bstack1l1ll111l1_opy_ in caps:
        continue
      bstack11l1l1ll_opy_[bstack1l1ll111l1_opy_] = config[bstack1111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॎ")][index][bstack1l1ll111l1_opy_]
  bstack11l1l1ll_opy_[bstack1111_opy_ (u"ࠪ࡬ࡴࡹࡴࡏࡣࡰࡩࠬॏ")] = socket.gethostname()
  if bstack1111_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬॐ") in bstack11l1l1ll_opy_:
    del (bstack11l1l1ll_opy_[bstack1111_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭॑")])
  return bstack11l1l1ll_opy_
def bstack1l11l11ll_opy_(config):
  global bstack1l11l11ll1_opy_
  bstack1llllll1l1_opy_ = {}
  caps = bstack11l11111_opy_
  if bstack1l11l11ll1_opy_:
    caps += bstack1l111l1lll_opy_
  for key in caps:
    if key in config:
      bstack1llllll1l1_opy_[key] = config[key]
  return bstack1llllll1l1_opy_
def bstack111ll11l1l_opy_(bstack11l1l1ll_opy_, bstack1llllll1l1_opy_):
  bstack111l1ll1_opy_ = {}
  for key in bstack11l1l1ll_opy_.keys():
    if key in bstack1ll11l11l_opy_:
      bstack111l1ll1_opy_[bstack1ll11l11l_opy_[key]] = bstack11l1l1ll_opy_[key]
    else:
      bstack111l1ll1_opy_[key] = bstack11l1l1ll_opy_[key]
  for key in bstack1llllll1l1_opy_:
    if key in bstack1ll11l11l_opy_:
      bstack111l1ll1_opy_[bstack1ll11l11l_opy_[key]] = bstack1llllll1l1_opy_[key]
    else:
      bstack111l1ll1_opy_[key] = bstack1llllll1l1_opy_[key]
  return bstack111l1ll1_opy_
def bstack1ll11l1l11_opy_(config, index=0):
  global bstack1l11l11ll1_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack11ll1l1lll_opy_ = bstack1lllllll1_opy_(bstack1ll11l1ll1_opy_, config, logger)
  bstack1llllll1l1_opy_ = bstack1l11l11ll_opy_(config)
  bstack1lll11l11_opy_ = bstack11l11111_opy_
  bstack1lll11l11_opy_ += bstack111lll11_opy_
  bstack1llllll1l1_opy_ = update(bstack1llllll1l1_opy_, bstack11ll1l1lll_opy_)
  if bstack1l11l11ll1_opy_:
    bstack1lll11l11_opy_ += bstack1l111l1lll_opy_
  if bstack1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴ॒ࠩ") in config:
    if bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ॓") in config[bstack1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ॔")][index]:
      caps[bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧॕ")] = config[bstack1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॖ")][index][bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩॗ")]
    if bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭क़") in config[bstack1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩख़")][index]:
      caps[bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨग़")] = str(config[bstack1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫज़")][index][bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪड़")])
    bstack11ll1lll11_opy_ = bstack1lllllll1_opy_(bstack1ll11l1ll1_opy_, config[bstack1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ढ़")][index], logger)
    bstack1lll11l11_opy_ += list(bstack11ll1lll11_opy_.keys())
    for bstack11l11ll11l_opy_ in bstack1lll11l11_opy_:
      if bstack11l11ll11l_opy_ in config[bstack1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧफ़")][index]:
        if bstack11l11ll11l_opy_ == bstack1111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧय़"):
          try:
            bstack11ll1lll11_opy_[bstack11l11ll11l_opy_] = str(config[bstack1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩॠ")][index][bstack11l11ll11l_opy_] * 1.0)
          except:
            bstack11ll1lll11_opy_[bstack11l11ll11l_opy_] = str(config[bstack1111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪॡ")][index][bstack11l11ll11l_opy_])
        else:
          bstack11ll1lll11_opy_[bstack11l11ll11l_opy_] = config[bstack1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫॢ")][index][bstack11l11ll11l_opy_]
        del (config[bstack1111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॣ")][index][bstack11l11ll11l_opy_])
    bstack1llllll1l1_opy_ = update(bstack1llllll1l1_opy_, bstack11ll1lll11_opy_)
  bstack11l1l1ll_opy_ = bstack1lll1111l_opy_(config, index)
  for bstack1111lllll_opy_ in bstack11l11111_opy_ + list(bstack11ll1l1lll_opy_.keys()):
    if bstack1111lllll_opy_ in bstack11l1l1ll_opy_:
      bstack1llllll1l1_opy_[bstack1111lllll_opy_] = bstack11l1l1ll_opy_[bstack1111lllll_opy_]
      del (bstack11l1l1ll_opy_[bstack1111lllll_opy_])
  if bstack1ll1l1ll11_opy_(config):
    bstack11l1l1ll_opy_[bstack1111_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ।")] = True
    caps.update(bstack1llllll1l1_opy_)
    caps[bstack1111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ॥")] = bstack11l1l1ll_opy_
  else:
    bstack11l1l1ll_opy_[bstack1111_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ०")] = False
    caps.update(bstack111ll11l1l_opy_(bstack11l1l1ll_opy_, bstack1llllll1l1_opy_))
    if bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ१") in caps:
      caps[bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ२")] = caps[bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭३")]
      del (caps[bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ४")])
    if bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ५") in caps:
      caps[bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭६")] = caps[bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭७")]
      del (caps[bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ८")])
  return caps
def bstack1111l111l_opy_():
  global bstack11l1l1lll_opy_
  global CONFIG
  if bstack11l1l1lll_opy_ != bstack1111_opy_ (u"ࠧࠨ९") and (bstack11l1l1lll_opy_.startswith(bstack1111_opy_ (u"ࠨࡪࡷࡸࡵࡀ࠯࠰ࠩ॰")) or bstack11l1l1lll_opy_.startswith(bstack1111_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠫॱ"))):
    return bstack11l1l1lll_opy_
  if bstack1l111ll11l_opy_() <= version.parse(bstack1111_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪॲ")):
    if bstack11l1l1lll_opy_ != bstack1111_opy_ (u"ࠫࠬॳ"):
      return bstack1111_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨॴ") + bstack11l1l1lll_opy_ + bstack1111_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥॵ")
    return bstack11l11lll1_opy_
  if bstack11l1l1lll_opy_ != bstack1111_opy_ (u"ࠧࠨॶ"):
    return bstack1111_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥॷ") + bstack11l1l1lll_opy_ + bstack1111_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥॸ")
  return HTTPS_HUB
def bstack11l1l111_opy_(options):
  return hasattr(options, bstack1111_opy_ (u"ࠪࡷࡪࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠫॹ"))
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
def bstack1l111lll11_opy_(options, bstack1l1l11111l_opy_):
  for bstack1l1111lll_opy_ in bstack1l1l11111l_opy_:
    if bstack1l1111lll_opy_ in [bstack1111_opy_ (u"ࠫࡦࡸࡧࡴࠩॺ"), bstack1111_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩॻ")]:
      continue
    if bstack1l1111lll_opy_ in options._experimental_options:
      options._experimental_options[bstack1l1111lll_opy_] = update(options._experimental_options[bstack1l1111lll_opy_],
                                                         bstack1l1l11111l_opy_[bstack1l1111lll_opy_])
    else:
      options.add_experimental_option(bstack1l1111lll_opy_, bstack1l1l11111l_opy_[bstack1l1111lll_opy_])
  if bstack1111_opy_ (u"࠭ࡡࡳࡩࡶࠫॼ") in bstack1l1l11111l_opy_:
    for arg in bstack1l1l11111l_opy_[bstack1111_opy_ (u"ࠧࡢࡴࡪࡷࠬॽ")]:
      options.add_argument(arg)
    del (bstack1l1l11111l_opy_[bstack1111_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ॾ")])
  if bstack1111_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ॿ") in bstack1l1l11111l_opy_:
    for ext in bstack1l1l11111l_opy_[bstack1111_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧঀ")]:
      try:
        options.add_extension(ext)
      except OSError:
        options.add_encoded_extension(ext)
    del (bstack1l1l11111l_opy_[bstack1111_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨঁ")])
def bstack111l1l1ll_opy_(options):
  bstack1111_opy_ (u"ࠧࠨࠢࠋࠢࠣࡍࡳࡰࡥࡤࡶࠣࡨࡪ࡬ࡡࡶ࡮ࡷࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡴࡶࡴࡪࡱࡱࡷࠥ࡬࡯ࡳࠢ࡯ࡳࡦࡪࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡹ࡫ࡩࡳࠦ࡯ࡷࡧࡵࡶ࡮ࡪࡥࡍࡱࡤࡨ࡙࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡧࡱࡥࡧࡲࡥࡥ࠰ࠍࠤࠥࡊࡥࡧࡧࡱࡷ࡮ࡼࡥ࠻ࠢࡱࡩࡻ࡫ࡲࠡࡱࡹࡩࡷࡽࡲࡪࡶࡨࡷࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠࡢࡴࡪࡷ࠱ࠦ࡯࡯࡮ࡼࠤࡦࡪࡤࡴࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡳࡳ࡫ࡳ࠯ࠌࠣࠤࡘ࡯࡭ࡪ࡮ࡤࡶࠥࡺ࡯ࠡࡌࡤࡺࡦࠦࡓࡅࡍࠪࡷࠥࡕࡶࡦࡴࡵ࡭ࡩ࡫ࡌࡰࡣࡧࡘࡪࡹࡴࡪࡰࡪࡇ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࡋࡩࡱࡶࡥࡳ࠰ࠍࠤ࡚ࠥࡨࡪࡵࠣ࡭ࡸࠦࡡࠡࡹࡵࡥࡵࡶࡥࡳࠢࡤࡶࡴࡻ࡮ࡥࠢࡷ࡬ࡪࠦࡣࡦࡰࡷࡶࡦࡲࡩࡻࡧࡧࠤ࡭࡫࡬ࡱࡧࡵࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠥࠦࠧং")
  global CONFIG
  global bstack11l1l11l11_opy_
  try:
    if not bstack11l1l11l11_opy_ or not options:
      return options
    from bstack_utils.bstack1ll1111l_opy_ import bstack1llllll1ll_opy_
    bstack11l11lll11_opy_ = bstack1llllll1ll_opy_(options, bstack1l1l1111ll_opy_=bstack1111_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࠨঃ"))
    if bstack11l11lll11_opy_ > 0:
      logger.debug(bstack1111_opy_ (u"ࠢࡍࡱࡤࡨࠥࡺࡥࡴࡶ࡬ࡲ࡬ࡀࠠࡂࡦࡧࡩࡩࠦࡻࡾࠢࡧࡩ࡫ࡧࡵ࡭ࡶࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠦࡦࡰࡴࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧࠥ঄").format(bstack11l11lll11_opy_))
  except Exception as e:
    logger.debug(bstack1111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡮ࡴࡪࡦࡥࡷࠤࡱࡵࡡࡥࠢࡷࡩࡸࡺࡩ࡯ࡩࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࢁࡽࠣঅ").format(e))
  return options
def bstack11l1ll111l_opy_(options, bstack111ll11ll1_opy_):
  if bstack1111_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨআ") in bstack111ll11ll1_opy_:
    for bstack1lllll11ll_opy_ in bstack111ll11ll1_opy_[bstack1111_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩই")]:
      if bstack1lllll11ll_opy_ in options._preferences:
        options._preferences[bstack1lllll11ll_opy_] = update(options._preferences[bstack1lllll11ll_opy_], bstack111ll11ll1_opy_[bstack1111_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪঈ")][bstack1lllll11ll_opy_])
      else:
        options.set_preference(bstack1lllll11ll_opy_, bstack111ll11ll1_opy_[bstack1111_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫউ")][bstack1lllll11ll_opy_])
  if bstack1111_opy_ (u"࠭ࡡࡳࡩࡶࠫঊ") in bstack111ll11ll1_opy_:
    for arg in bstack111ll11ll1_opy_[bstack1111_opy_ (u"ࠧࡢࡴࡪࡷࠬঋ")]:
      options.add_argument(arg)
def bstack11lll11l_opy_(options, bstack1l1l1l1lll_opy_):
  if bstack1111_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࠩঌ") in bstack1l1l1l1lll_opy_:
    options.use_webview(bool(bstack1l1l1l1lll_opy_[bstack1111_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࠪ঍")]))
  bstack1l111lll11_opy_(options, bstack1l1l1l1lll_opy_)
def bstack1ll111l1l1_opy_(options, bstack11ll111l_opy_):
  for bstack11l1l1ll11_opy_ in bstack11ll111l_opy_:
    if bstack11l1l1ll11_opy_ in [bstack1111_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧ঎"), bstack1111_opy_ (u"ࠫࡦࡸࡧࡴࠩএ")]:
      continue
    options.set_capability(bstack11l1l1ll11_opy_, bstack11ll111l_opy_[bstack11l1l1ll11_opy_])
  if bstack1111_opy_ (u"ࠬࡧࡲࡨࡵࠪঐ") in bstack11ll111l_opy_:
    for arg in bstack11ll111l_opy_[bstack1111_opy_ (u"࠭ࡡࡳࡩࡶࠫ঑")]:
      options.add_argument(arg)
  if bstack1111_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫ঒") in bstack11ll111l_opy_:
    options.bstack1ll11lll_opy_(bool(bstack11ll111l_opy_[bstack1111_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬও")]))
def bstack1111lll11l_opy_(options, bstack1lllll11l_opy_):
  for bstack1l1ll1ll1l_opy_ in bstack1lllll11l_opy_:
    if bstack1l1ll1ll1l_opy_ in [bstack1111_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ঔ"), bstack1111_opy_ (u"ࠪࡥࡷ࡭ࡳࠨক")]:
      continue
    options._options[bstack1l1ll1ll1l_opy_] = bstack1lllll11l_opy_[bstack1l1ll1ll1l_opy_]
  if bstack1111_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨখ") in bstack1lllll11l_opy_:
    for bstack11l111ll_opy_ in bstack1lllll11l_opy_[bstack1111_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩগ")]:
      options.bstack111l111lll_opy_(
        bstack11l111ll_opy_, bstack1lllll11l_opy_[bstack1111_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪঘ")][bstack11l111ll_opy_])
  if bstack1111_opy_ (u"ࠧࡢࡴࡪࡷࠬঙ") in bstack1lllll11l_opy_:
    for arg in bstack1lllll11l_opy_[bstack1111_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭চ")]:
      options.add_argument(arg)
def bstack1l1lll11l_opy_(options, caps):
  if not hasattr(options, bstack1111_opy_ (u"ࠩࡎࡉ࡞࠭ছ")):
    return
  if options.KEY == bstack1111_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨজ"):
    options = bstack11l1111111_opy_.bstack11l1l11l1_opy_(bstack1llll1l1l1_opy_=options, config=CONFIG)
  if options.KEY == bstack1111_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩঝ") and options.KEY in caps:
    bstack1l111lll11_opy_(options, caps[bstack1111_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪঞ")])
  elif options.KEY == bstack1111_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫট") and options.KEY in caps:
    bstack11l1ll111l_opy_(options, caps[bstack1111_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬঠ")])
  elif options.KEY == bstack1111_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩড") and options.KEY in caps:
    bstack1ll111l1l1_opy_(options, caps[bstack1111_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪঢ")])
  elif options.KEY == bstack1111_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫণ") and options.KEY in caps:
    bstack11lll11l_opy_(options, caps[bstack1111_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬত")])
  elif options.KEY == bstack1111_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫথ") and options.KEY in caps:
    bstack1111lll11l_opy_(options, caps[bstack1111_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬদ")])
def bstack11l111l111_opy_(caps):
  global bstack1l11l11ll1_opy_
  if isinstance(os.environ.get(bstack1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨধ")), str):
    bstack1l11l11ll1_opy_ = eval(os.getenv(bstack1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩন")))
  if bstack1l11l11ll1_opy_:
    if bstack1l111llll_opy_() < version.parse(bstack1111_opy_ (u"ࠩ࠵࠲࠸࠴࠰ࠨ঩")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1111_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪপ")
    if bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩফ") in caps:
      browser = caps[bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪব")]
    elif bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧভ") in caps:
      browser = caps[bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨম")]
    browser = str(browser).lower()
    if browser == bstack1111_opy_ (u"ࠨ࡫ࡳ࡬ࡴࡴࡥࠨয") or browser == bstack1111_opy_ (u"ࠩ࡬ࡴࡦࡪࠧর"):
      browser = bstack1111_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪ঱")
    if browser == bstack1111_opy_ (u"ࠫࡸࡧ࡭ࡴࡷࡱ࡫ࠬল"):
      browser = bstack1111_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬ঳")
    if browser not in [bstack1111_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭঴"), bstack1111_opy_ (u"ࠧࡦࡦࡪࡩࠬ঵"), bstack1111_opy_ (u"ࠨ࡫ࡨࠫশ"), bstack1111_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩষ"), bstack1111_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫস")]:
      return None
    try:
      package = bstack1111_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳ࠰ࡾࢁ࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭হ").format(browser)
      name = bstack1111_opy_ (u"ࠬࡕࡰࡵ࡫ࡲࡲࡸ࠭঺")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack11l1l111_opy_(options):
        return None
      for bstack1111lllll_opy_ in caps.keys():
        options.set_capability(bstack1111lllll_opy_, caps[bstack1111lllll_opy_])
      bstack1l1lll11l_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack111ll1l111_opy_(options, bstack1l1l1l11l1_opy_):
  if not bstack11l1l111_opy_(options):
    return
  for bstack1111lllll_opy_ in bstack1l1l1l11l1_opy_.keys():
    if bstack1111lllll_opy_ in bstack111lll11_opy_:
      continue
    if bstack1111lllll_opy_ in options._caps and type(options._caps[bstack1111lllll_opy_]) in [dict, list]:
      options._caps[bstack1111lllll_opy_] = update(options._caps[bstack1111lllll_opy_], bstack1l1l1l11l1_opy_[bstack1111lllll_opy_])
    else:
      options.set_capability(bstack1111lllll_opy_, bstack1l1l1l11l1_opy_[bstack1111lllll_opy_])
  bstack1l1lll11l_opy_(options, bstack1l1l1l11l1_opy_)
  if bstack1111_opy_ (u"࠭࡭ࡰࡼ࠽ࡨࡪࡨࡵࡨࡩࡨࡶࡆࡪࡤࡳࡧࡶࡷࠬ঻") in options._caps:
    if options._caps[bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩ়ࠬ")] and options._caps[bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ঽ")].lower() != bstack1111_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪা"):
      del options._caps[bstack1111_opy_ (u"ࠪࡱࡴࢀ࠺ࡥࡧࡥࡹ࡬࡭ࡥࡳࡃࡧࡨࡷ࡫ࡳࡴࠩি")]
def bstack1l1l1lll11_opy_(proxy_config):
  if bstack1111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨী") in proxy_config:
    proxy_config[bstack1111_opy_ (u"ࠬࡹࡳ࡭ࡒࡵࡳࡽࡿࠧু")] = proxy_config[bstack1111_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪূ")]
    del (proxy_config[bstack1111_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫৃ")])
  if bstack1111_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫৄ") in proxy_config and proxy_config[bstack1111_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬ৅")].lower() != bstack1111_opy_ (u"ࠪࡨ࡮ࡸࡥࡤࡶࠪ৆"):
    proxy_config[bstack1111_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧে")] = bstack1111_opy_ (u"ࠬࡳࡡ࡯ࡷࡤࡰࠬৈ")
  if bstack1111_opy_ (u"࠭ࡰࡳࡱࡻࡽࡆࡻࡴࡰࡥࡲࡲ࡫࡯ࡧࡖࡴ࡯ࠫ৉") in proxy_config:
    proxy_config[bstack1111_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪ৊")] = bstack1111_opy_ (u"ࠨࡲࡤࡧࠬো")
  return proxy_config
def bstack1lllll111_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1111_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨৌ") in config:
    return proxy
  config[bstack1111_opy_ (u"ࠪࡴࡷࡵࡸࡺ্ࠩ")] = bstack1l1l1lll11_opy_(config[bstack1111_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪৎ")])
  if proxy == None:
    proxy = Proxy(config[bstack1111_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ৏")])
  return proxy
def bstack1111llll_opy_(self):
  global CONFIG
  global bstack111l111111_opy_
  try:
    proxy = bstack1ll111l111_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1111_opy_ (u"࠭࠮ࡱࡣࡦࠫ৐")):
        proxies = bstack1l111lllll_opy_(proxy, bstack1111l111l_opy_())
        if len(proxies) > 0:
          protocol, bstack1llllllll1_opy_ = proxies.popitem()
          if bstack1111_opy_ (u"ࠢ࠻࠱࠲ࠦ৑") in bstack1llllllll1_opy_:
            return bstack1llllllll1_opy_
          else:
            return bstack1111_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ৒") + bstack1llllllll1_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡶࡲࡰࡺࡼࠤࡺࡸ࡬ࠡ࠼ࠣࡿࢂࠨ৓").format(str(e)))
  return bstack111l111111_opy_(self)
def bstack1ll111l11l_opy_():
  global CONFIG
  return bstack111l11l11_opy_(CONFIG) and bstack1lllll11l1_opy_() and bstack1l111ll11l_opy_() >= version.parse(bstack11lll11ll_opy_)
def bstack1l111l1ll_opy_():
  global CONFIG
  return (bstack1111_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭৔") in CONFIG or bstack1111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ৕") in CONFIG) and bstack1l1l1ll1l1_opy_()
def bstack11ll11111_opy_(config):
  bstack11llll11_opy_ = {}
  if bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ৖") in config:
    bstack11llll11_opy_ = config[bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪৗ")]
  if bstack1111_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭৘") in config:
    bstack11llll11_opy_ = config[bstack1111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ৙")]
  proxy = bstack1ll111l111_opy_(config)
  if proxy:
    if proxy.endswith(bstack1111_opy_ (u"ࠩ࠱ࡴࡦࡩࠧ৚")) and os.path.isfile(proxy):
      bstack11llll11_opy_[bstack1111_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭৛")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1111_opy_ (u"ࠫ࠳ࡶࡡࡤࠩড়")):
        proxies = bstack11111ll1_opy_(config, bstack1111l111l_opy_())
        if len(proxies) > 0:
          protocol, bstack1llllllll1_opy_ = proxies.popitem()
          if bstack1111_opy_ (u"ࠧࡀ࠯࠰ࠤঢ়") in bstack1llllllll1_opy_:
            parsed_url = urlparse(bstack1llllllll1_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1111_opy_ (u"ࠨ࠺࠰࠱ࠥ৞") + bstack1llllllll1_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack11llll11_opy_[bstack1111_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪয়")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack11llll11_opy_[bstack1111_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡰࡴࡷࠫৠ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack11llll11_opy_[bstack1111_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬৡ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack11llll11_opy_[bstack1111_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭ৢ")] = str(parsed_url.password)
  return bstack11llll11_opy_
def bstack1ll1llll11_opy_(config):
  if bstack1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩৣ") in config:
    return config[bstack1111_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪ৤")]
  return {}
def bstack11ll11l11_opy_(caps):
  global bstack111lllll1l_opy_
  if bstack1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ৥") in caps:
    caps[bstack1111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ০")][bstack1111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧ১")] = True
    if bstack111lllll1l_opy_:
      caps[bstack1111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ২")][bstack1111_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ৩")] = bstack111lllll1l_opy_
  else:
    caps[bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩ৪")] = True
    if bstack111lllll1l_opy_:
      caps[bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭৫")] = bstack111lllll1l_opy_
@measure(event_name=EVENTS.bstack111ll11lll_opy_, stage=STAGE.bstack111l1lllll_opy_, bstack11ll1l11l1_opy_=bstack1lll11ll1_opy_)
def bstack1l1ll111_opy_():
  global CONFIG
  if not bstack1ll11ll11l_opy_(CONFIG) or cli.is_enabled(CONFIG):
    return
  if bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ৬") in CONFIG and bstack11ll1l1l1l_opy_(CONFIG[bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ৭")]):
    if (
      bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ৮") in CONFIG
      and bstack11ll1l1l1l_opy_(CONFIG[bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭৯")].get(bstack1111_opy_ (u"ࠪࡷࡰ࡯ࡰࡃ࡫ࡱࡥࡷࡿࡉ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡣࡷ࡭ࡴࡴࠧৰ")))
    ):
      logger.debug(bstack1111_opy_ (u"ࠦࡑࡵࡣࡢ࡮ࠣࡦ࡮ࡴࡡࡳࡻࠣࡲࡴࡺࠠࡴࡶࡤࡶࡹ࡫ࡤࠡࡣࡶࠤࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤࡪࡴࡡࡣ࡮ࡨࡨࠧৱ"))
      return
    bstack11llll11_opy_ = bstack11ll11111_opy_(CONFIG)
    bstack1l11l1lll_opy_(CONFIG[bstack1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ৲")], bstack11llll11_opy_)
def bstack1l11l1lll_opy_(key, bstack11llll11_opy_):
  global bstack1lll111ll_opy_
  logger.info(bstack111l1ll11_opy_)
  try:
    bstack1lll111ll_opy_ = Local()
    bstack1ll1ll1ll_opy_ = {bstack1111_opy_ (u"࠭࡫ࡦࡻࠪ৳"): key}
    bstack1ll1ll1ll_opy_.update(bstack11llll11_opy_)
    logger.debug(bstack11ll1ll1_opy_.format(str(bstack1ll1ll1ll_opy_)).replace(key, bstack1111_opy_ (u"ࠧ࡜ࡔࡈࡈࡆࡉࡔࡆࡆࡠࠫ৴")))
    bstack1lll111ll_opy_.start(**bstack1ll1ll1ll_opy_)
    if bstack1lll111ll_opy_.isRunning():
      logger.info(bstack111lll11l_opy_)
  except Exception as e:
    bstack1ll1ll11_opy_(bstack111l11l11l_opy_.format(str(e)))
def bstack11lll1l111_opy_():
  global bstack1lll111ll_opy_
  if bstack1lll111ll_opy_.isRunning():
    logger.info(bstack11l11ll111_opy_)
    bstack1lll111ll_opy_.stop()
  bstack1lll111ll_opy_ = None
def bstack11111l1l_opy_(bstack11l1ll1l11_opy_=[]):
  global CONFIG
  bstack11lll111ll_opy_ = []
  bstack1ll1ll11ll_opy_ = [bstack1111_opy_ (u"ࠨࡱࡶࠫ৵"), bstack1111_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬ৶"), bstack1111_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧ৷"), bstack1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭৸"), bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ৹"), bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ৺")]
  try:
    for err in bstack11l1ll1l11_opy_:
      bstack1ll1111lll_opy_ = {}
      for k in bstack1ll1ll11ll_opy_:
        val = CONFIG[bstack1111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ৻")][int(err[bstack1111_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧৼ")])].get(k)
        if val:
          bstack1ll1111lll_opy_[k] = val
      if(err[bstack1111_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ৽")] != bstack1111_opy_ (u"ࠪࠫ৾")):
        bstack1ll1111lll_opy_[bstack1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡵࠪ৿")] = {
          err[bstack1111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ਀")]: err[bstack1111_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬਁ")]
        }
        bstack11lll111ll_opy_.append(bstack1ll1111lll_opy_)
  except Exception as e:
    logger.debug(bstack1111_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡳࡷࡳࡡࡵࡶ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺ࠺ࠡࠩਂ") + str(e))
  finally:
    return bstack11lll111ll_opy_
def bstack1l1l111lll_opy_(file_name):
  bstack1l1llllll1_opy_ = []
  try:
    bstack11l1lll111_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack11l1lll111_opy_):
      with open(bstack11l1lll111_opy_) as f:
        bstack11ll11l1l1_opy_ = json.load(f)
        bstack1l1llllll1_opy_ = bstack11ll11l1l1_opy_
      os.remove(bstack11l1lll111_opy_)
    return bstack1l1llllll1_opy_
  except Exception as e:
    logger.debug(bstack1111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪ࡮ࡴࡤࡪࡰࡪࠤࡪࡸࡲࡰࡴࠣࡰ࡮ࡹࡴ࠻ࠢࠪਃ") + str(e))
    return bstack1l1llllll1_opy_
def bstack1l1l1l111_opy_():
  try:
      import time
      from bstack_utils.constants import bstack111l1l1lll_opy_, EVENTS
      from bstack_utils.helper import bstack1llll1l1ll_opy_, get_host_info, global_config
      from datetime import datetime
      from filelock import FileLock
      from bstack_utils.bstack1ll1l11ll1_opy_ import bstack1l11l1ll_opy_
      bstack1l11l1ll_opy_.bstack11ll11l1ll_opy_()
      bstack1l1l1l1ll1_opy_ = os.path.join(os.getcwd(), bstack1111_opy_ (u"ࠩ࡯ࡳ࡬࠭਄"), bstack1111_opy_ (u"ࠪ࡯ࡪࡿ࠭࡮ࡧࡷࡶ࡮ࡩࡳ࠯࡬ࡶࡳࡳ࠭ਅ"))
      data = None
      lock = FileLock(bstack1l1l1l1ll1_opy_+bstack1111_opy_ (u"ࠦ࠳ࡲ࡯ࡤ࡭ࠥਆ"), timeout=2)
      try:
          with lock:
              with open(bstack1l1l1l1ll1_opy_, bstack1111_opy_ (u"ࠧࡸࠢਇ"), encoding=bstack1111_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧਈ")) as file:
                  data = json.load(file)
      except Exception as e:
          logger.debug(bstack1111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡶࡪࡧࡤࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࠦࡦࡪ࡮ࡨ࠾ࠥࢁࡽࠣਉ").format(e))
          return
      if not data:
          return
      def bstack1111lll11_opy_():
          try:
              config = {
                  bstack1111_opy_ (u"ࠣࡪࡨࡥࡩ࡫ࡲࡴࠤਊ"): {
                      bstack1111_opy_ (u"ࠤࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠣ਋"): bstack1111_opy_ (u"ࠥࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳࠨ਌"),
                  }
              }
              bstack1l1ll111l_opy_ = datetime.utcnow()
              current_time = bstack1l1ll111l_opy_.strftime(bstack1111_opy_ (u"ࠦࠪ࡟࠭ࠦ࡯࠰ࠩࡩ࡚ࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࠯ࠧࡩࠤ࡚࡚ࡃࠣ਍"))
              test_id = os.environ.get(bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ਎")) if os.environ.get(bstack1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫਏ")) else global_config.get_property(bstack1111_opy_ (u"ࠢࡴࡦ࡮ࡖࡺࡴࡉࡥࠤਐ"))
              payload = {
                  bstack1111_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠧ਑"): bstack1111_opy_ (u"ࠤࡶࡨࡰࡥࡥࡷࡧࡱࡸࡸࠨ਒"),
                  bstack1111_opy_ (u"ࠥࡨࡦࡺࡡࠣਓ"): {
                      bstack1111_opy_ (u"ࠦࡹ࡫ࡳࡵࡪࡸࡦࡤࡻࡵࡪࡦࠥਔ"): test_id,
                      bstack1111_opy_ (u"ࠧࡩࡲࡦࡣࡷࡩࡩࡥࡤࡢࡻࠥਕ"): current_time,
                      bstack1111_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡴࡡ࡮ࡧࠥਖ"): bstack1111_opy_ (u"ࠢࡔࡆࡎࡊࡪࡧࡴࡶࡴࡨࡔࡪࡸࡦࡰࡴࡰࡥࡳࡩࡥࠣਗ"),
                      bstack1111_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟࡫ࡵࡲࡲࠧਘ"): {
                          bstack1111_opy_ (u"ࠤࡰࡩࡦࡹࡵࡳࡧࡶࠦਙ"): data,
                          bstack1111_opy_ (u"ࠥࡷࡩࡱࡒࡶࡰࡌࡨࠧਚ"): global_config.get_property(bstack1111_opy_ (u"ࠦࡸࡪ࡫ࡓࡷࡱࡍࡩࠨਛ"))
                      },
                      bstack1111_opy_ (u"ࠧࡻࡳࡦࡴࡢࡨࡦࡺࡡࠣਜ"): global_config.get_property(bstack1111_opy_ (u"ࠨࡵࡴࡧࡵࡒࡦࡳࡥࠣਝ")),
                      bstack1111_opy_ (u"ࠢࡩࡱࡶࡸࡤ࡯࡮ࡧࡱࠥਞ"): get_host_info()
                  }
              }
              bstack1llll1l11_opy_ = bstack11111l1ll_opy_(cli.config, [bstack1111_opy_ (u"ࠣࡣࡳ࡭ࡸࠨਟ"), bstack1111_opy_ (u"ࠤࡨࡨࡸࡏ࡮ࡴࡶࡵࡹࡲ࡫࡮ࡵࡣࡷ࡭ࡴࡴࠢਠ"), bstack1111_opy_ (u"ࠥࡥࡵ࡯ࠢਡ")], bstack111l1l1lll_opy_)
              response = bstack1llll1l1ll_opy_(bstack1111_opy_ (u"ࠦࡕࡕࡓࡕࠤਢ"), bstack1llll1l11_opy_, payload, config)
              if response.status_code >= 200 and response.status_code < 300:
                  logger.info(bstack1111_opy_ (u"ࠧࡑࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵࠣࡷࡪࡴࡴࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡵࡱࠣࡿࢂࠨਣ").format(bstack111l1l1lll_opy_))
              else:
                  logger.debug(bstack1111_opy_ (u"ࠨࡋࡦࡻࠣࡱࡪࡺࡲࡪࡥࡶࠤࡷ࡫ࡱࡶࡧࡶࡸࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪࠣࡷࡹࡧࡴࡶࡵࠣࡿࢂࠨਤ").format(response.status_code))
          except Exception as e:
              logger.debug(bstack1111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡴࡤࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࡀࠠࡼࡿࠥਥ").format(e))
      bstack1111lll11_opy_()
  except Exception as e:
      logger.debug(bstack1111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡴࡤࡠ࡭ࡨࡽࡤࡳࡥࡵࡴ࡬ࡧࡸࡀࠠࡼࡿࠥਦ").format(e))
def bstack111lll1l11_opy_(bstack11l1l1111l_opy_=False):
  bstack1l11ll11_opy_ = bstack1111_opy_ (u"ࠤࠥਧ")
  global bstack111ll1l1_opy_
  global bstack1ll11111l1_opy_
  global bstack1ll11lll1l_opy_
  global bstack1l1ll11lll_opy_
  global ROBOT_PYTHON_ERRORS
  global bstack1l1l11ll11_opy_
  global CONFIG
  bstack1ll1llllll_opy_ = os.environ.get(bstack1111_opy_ (u"ࠪࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡕࡔࡇࡇࠫਨ"))
  if bstack1ll1llllll_opy_ not in [bstack1111_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ਩")]:
    bstack1l11ll11_opy_ = bstack1l11l1ll_opy_.bstack11l111111_opy_(EVENTS.bstack1l1l11111_opy_)
  percy.shutdown()
  if bstack111ll1l1_opy_:
    logger.warning(bstack11lllllll_opy_.format(str(bstack111ll1l1_opy_)))
  else:
    try:
      bstack1l1lll1l11_opy_ = bstack1llllll1l_opy_(bstack1111_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫਪ"), logger)
      if bstack1l1lll1l11_opy_.get(bstack1111_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫਫ")) and bstack1l1lll1l11_opy_.get(bstack1111_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬਬ")).get(bstack1111_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪਭ")):
        logger.warning(bstack11lllllll_opy_.format(str(bstack1l1lll1l11_opy_[bstack1111_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧਮ")][bstack1111_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬਯ")])))
    except Exception as e:
      logger.error(e)
  if cli.is_running() and bstack1ll1llllll_opy_ not in [bstack1111_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬਰ")]:
    if _1l1ll1ll11_opy_ is not None:
      bstack11l1l1111l_opy_ = _1l1ll1ll11_opy_
    else:
      bstack11l1l1111l_opy_ = cli.is_running()
    bstack11l1lllll1_opy_.invoke(bstack1llll11l1_opy_.bstack1ll1lll1l1_opy_)
  elif _1l1ll1ll11_opy_ is not None:
    bstack11l1l1111l_opy_ = _1l1ll1ll11_opy_
  logger.info(bstack1111l1111_opy_)
  global bstack1lll111ll_opy_
  if bstack1lll111ll_opy_:
    bstack11lll1l111_opy_()
  try:
    with bstack111l1l11l_opy_:
      bstack1l111ll111_opy_ = bstack1ll11111l1_opy_.copy()
    for driver in bstack1l111ll111_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1111l1ll1_opy_)
  ROBOT_PYTHON_ERRORS = []
  if bstack1l1l11ll11_opy_ == bstack1111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ਱"):
    ROBOT_PYTHON_ERRORS = bstack1l1l111lll_opy_(bstack1111_opy_ (u"࠭ࡲࡰࡤࡲࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧਲ"))
  if bstack1l1l11ll11_opy_ == bstack1111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧਲ਼") and len(bstack1l1ll11lll_opy_) == 0:
    bstack1l1ll11lll_opy_ = bstack1l1l111lll_opy_(bstack1111_opy_ (u"ࠨࡲࡺࡣࡵࡿࡴࡦࡵࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭਴"))
    if len(bstack1l1ll11lll_opy_) == 0:
      bstack1l1ll11lll_opy_ = bstack1l1l111lll_opy_(bstack1111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡳࡴࡵࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨਵ"))
  bstack1llll11ll1_opy_ = bstack1111_opy_ (u"ࠪࠫਸ਼")
  if len(bstack1ll11lll1l_opy_) > 0:
    bstack1llll11ll1_opy_ = bstack11111l1l_opy_(bstack1ll11lll1l_opy_)
  elif len(bstack1l1ll11lll_opy_) > 0:
    bstack1llll11ll1_opy_ = bstack11111l1l_opy_(bstack1l1ll11lll_opy_)
  elif len(ROBOT_PYTHON_ERRORS) > 0:
    bstack1llll11ll1_opy_ = bstack11111l1l_opy_(ROBOT_PYTHON_ERRORS)
  elif len(bstack1lll111lll_opy_) > 0:
    bstack1llll11ll1_opy_ = bstack11111l1l_opy_(bstack1lll111lll_opy_)
  if bstack1ll1llllll_opy_ not in [bstack1111_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ਷")]:
    def bstack1l1l11ll1l_opy_():
      try:
        if bstack1ll1llllll_opy_ in [bstack1111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫਸ"), bstack1111_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬਹ")]:
          bstack1ll1lll1_opy_()
      except Exception as e:
        logger.debug(bstack1111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩ࡭ࡳࡧ࡬ࡠࡧࡻࡩࡨࡻࡴࡪࡱࡱ࠾ࠥࢁࡽࠣ਺").format(e))
    def bstack1l1l111l1_opy_():
      try:
        if bool(bstack1llll11ll1_opy_):
          bstack11l1ll11l_opy_(bstack1llll11ll1_opy_, bstack11l1l1111l_opy_=bstack11l1l1111l_opy_)
        else:
          bstack11l1ll11l_opy_(bstack11l1l1111l_opy_=bstack11l1l1111l_opy_)
      except Exception as e:
        logger.debug(bstack1111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡴࡧࡱࡨ࡮ࡴࡧࠡࡧࡹࡩࡳࡺ࠺ࠡࡽࢀࠦ਻").format(e))
    def bstack111lll111_opy_():
      try:
        logger_utils.bstack1l1111l11_opy_(CONFIG)
      except Exception as e:
        logger.debug(bstack1111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡵࡨࡲࡩ࡯࡮ࡨࠢ࡯ࡳ࡬ࡹ࠺ࠡࡽࢀ਼ࠦ").format(e))
    bstack1ll1l1l1_opy_ = threading.Thread(target=bstack1l1l11ll1l_opy_)
    bstack1l11ll111l_opy_ = threading.Thread(target=bstack1l1l111l1_opy_)
    bstack111l11ll1_opy_ = threading.Thread(target=bstack111lll111_opy_)
    threads = [bstack1ll1l1l1_opy_, bstack1l11ll111l_opy_, bstack111l11ll1_opy_]
    for thread in threads:
      try:
        thread.start()
      except Exception as e:
        logger.debug(bstack1111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡶࡸࡦࡸࡴࡪࡰࡪࠤࡹ࡮ࡲࡦࡣࡧࠤࢀࢃ࠺ࠡࡽࢀࠦ਽").format(thread.name, e))
    for thread in threads:
      try:
        thread.join()
      except Exception as e:
        logger.debug(bstack1111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡮ࡴ࡯࡮ࡪࡰࡪࠤࡹ࡮ࡲࡦࡣࡧࠤࢀࢃ࠺ࠡࡽࢀࠦਾ").format(thread.name, e))
    bstack1l1lll1l1l_opy_(bstack1l11ll1ll_opy_, logger)
    bstack1l1lll1l1l_opy_(os.path.join(os.getcwd(), bstack1111_opy_ (u"ࠬࡲ࡯ࡨࠩਿ"), bstack1111_opy_ (u"࠭࡫ࡦࡻ࠰ࡱࡪࡺࡲࡪࡥࡶ࠲࡯ࡹ࡯࡯ࠩੀ")), logger)
  if bstack1ll1llllll_opy_ not in [bstack1111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨੁ")]:
    bstack1l11l1ll_opy_.end(EVENTS.bstack1l1l11111_opy_.value, bstack1l11ll11_opy_ + bstack1111_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣੂ"), bstack1l11ll11_opy_ + bstack1111_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ੃"), status=True, failure=None, test_name=None)
    bstack1l1l1l111_opy_()
    logger_utils.bstack1llll1111_opy_()
    logging.shutdown()
  if len(ROBOT_PYTHON_ERRORS) > 0:
    sys.exit(len(ROBOT_PYTHON_ERRORS))
def bstack1l1ll1l111_opy_(bstack1l111l1ll1_opy_, frame):
  global global_config
  logger.error(bstack1111l1l1l_opy_)
  global_config.bstack11llll1l1_opy_(bstack1111_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡒࡴ࠭੄"), bstack1l111l1ll1_opy_)
  if hasattr(signal, bstack1111_opy_ (u"ࠫࡘ࡯ࡧ࡯ࡣ࡯ࡷࠬ੅")):
    global_config.bstack11llll1l1_opy_(bstack1111_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬ੆"), signal.Signals(bstack1l111l1ll1_opy_).name)
  else:
    global_config.bstack11llll1l1_opy_(bstack1111_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭ੇ"), bstack1111_opy_ (u"ࠧࡔࡋࡊ࡙ࡓࡑࡎࡐ࡙ࡑࠫੈ"))
  bstack11l1l1111l_opy_ = cli.is_running()
  if bstack11l1l1111l_opy_:
    bstack11l1lllll1_opy_.invoke(bstack1llll11l1_opy_.bstack1ll1lll1l1_opy_)
  bstack1ll1llllll_opy_ = os.environ.get(bstack1111_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩ੉"))
  if bstack1ll1llllll_opy_ == bstack1111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ੊") and not cli.is_enabled(CONFIG):
    TestHubHandler.stop(global_config.get_property(bstack1111_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪੋ")))
  bstack111lll1l11_opy_(bstack11l1l1111l_opy_)
  sys.exit(1)
def bstack1ll1ll11_opy_(err):
  logger.critical(bstack111ll1l11_opy_.format(str(err)))
  bstack11l1ll11l_opy_(bstack111ll1l11_opy_.format(str(err)), True)
  atexit.unregister(bstack111lll1l11_opy_)
  bstack1ll1lll1_opy_()
  sys.exit(1)
def bstack1lll11llll_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack11l1ll11l_opy_(message, True)
  atexit.unregister(bstack111lll1l11_opy_)
  bstack1ll1lll1_opy_()
  sys.exit(1)
def bstack1l1l1l111l_opy_():
  global CONFIG
  global bstack11l11ll1l1_opy_
  global bstack1111llll1_opy_
  global bstack1111ll1l_opy_
  CONFIG = bstack11l1llll1l_opy_()
  load_dotenv(CONFIG.get(bstack1111_opy_ (u"ࠫࡪࡴࡶࡇ࡫࡯ࡩࠬੌ")))
  bstack1l1111ll11_opy_()
  bstack1lll1111l1_opy_()
  CONFIG = bstack11l1ll1ll1_opy_(CONFIG)
  update(CONFIG, bstack1111llll1_opy_)
  update(CONFIG, bstack11l11ll1l1_opy_)
  if not cli.is_enabled(CONFIG):
    CONFIG = bstack11ll111111_opy_(CONFIG)
  bstack1111ll1l_opy_ = bstack1ll11ll11l_opy_(CONFIG)
  os.environ[bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ੍")] = bstack1111ll1l_opy_.__str__().lower()
  global_config.bstack11llll1l1_opy_(bstack1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ੎"), bstack1111ll1l_opy_)
  if (bstack1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ੏") in CONFIG and bstack1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ੐") in bstack11l11ll1l1_opy_) or (
          bstack1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬੑ") in CONFIG and bstack1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭੒") not in bstack1111llll1_opy_):
    if os.getenv(bstack1111_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨ੓")):
      CONFIG[bstack1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ੔")] = os.getenv(bstack1111_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪ੕"))
    else:
      if not CONFIG.get(bstack1111_opy_ (u"ࠢࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠥ੖"), bstack1111_opy_ (u"ࠣࠤ੗")) in bstack1ll11l1l1l_opy_:
        bstack111ll1111_opy_()
  elif (bstack1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ੘") not in CONFIG and bstack1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬਖ਼") in CONFIG) or (
          bstack1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧਗ਼") in bstack1111llll1_opy_ and bstack1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨਜ਼") not in bstack11l11ll1l1_opy_):
    del (CONFIG[bstack1111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨੜ")])
  if bstack1l11lll1l_opy_(CONFIG):
    bstack1ll1ll11_opy_(bstack1111111ll_opy_)
  Config.get_instance().bstack11llll1l1_opy_(bstack1111_opy_ (u"ࠢࡶࡵࡨࡶࡓࡧ࡭ࡦࠤ੝"), CONFIG[bstack1111_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪਫ਼")])
  bstack1lll11111l_opy_()
  bstack1l1lll1ll1_opy_()
  if bstack1l11l11ll1_opy_ and not CONFIG.get(bstack1111_opy_ (u"ࠤࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠧ੟"), bstack1111_opy_ (u"ࠥࠦ੠")) in bstack1ll11l1l1l_opy_:
    CONFIG[bstack1111_opy_ (u"ࠫࡦࡶࡰࠨ੡")] = bstack1llll1l1l_opy_(CONFIG)
    logger.info(bstack11lll1l1l1_opy_.format(CONFIG[bstack1111_opy_ (u"ࠬࡧࡰࡱࠩ੢")]))
  if not bstack1111ll1l_opy_:
    CONFIG[bstack1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ੣")] = [{}]
def bstack1l111lll_opy_(config, bstack11l1ll1lll_opy_):
  global CONFIG
  global bstack1l11l11ll1_opy_
  CONFIG = config
  bstack1l11l11ll1_opy_ = bstack11l1ll1lll_opy_
def bstack1l1lll1ll1_opy_():
  global CONFIG
  global bstack1l11l11ll1_opy_
  if bstack1111_opy_ (u"ࠧࡢࡲࡳࠫ੤") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1lll11llll_opy_(e, bstack1111lll111_opy_)
    bstack1l11l11ll1_opy_ = True
    global_config.bstack11llll1l1_opy_(bstack1111_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ੥"), True)
def bstack1llll1l1l_opy_(config):
  bstack111l1l1l1l_opy_ = bstack1111_opy_ (u"ࠩࠪ੦")
  app = config[bstack1111_opy_ (u"ࠪࡥࡵࡶࠧ੧")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1lllllll1l_opy_:
      if os.path.exists(app):
        bstack111l1l1l1l_opy_ = bstack1l111l1l1_opy_(config, app)
      elif bstack111l1l11ll_opy_(app):
        bstack111l1l1l1l_opy_ = app
      else:
        bstack1ll1ll11_opy_(bstack1ll1lll11_opy_.format(app))
    else:
      if bstack111l1l11ll_opy_(app):
        bstack111l1l1l1l_opy_ = app
      elif os.path.exists(app):
        bstack111l1l1l1l_opy_ = bstack1l111l1l1_opy_(app)
      else:
        bstack1ll1ll11_opy_(bstack1l1lll1ll_opy_)
  else:
    if len(app) > 2:
      bstack1ll1ll11_opy_(bstack1ll11l1lll_opy_)
    elif len(app) == 2:
      if bstack1111_opy_ (u"ࠫࡵࡧࡴࡩࠩ੨") in app and bstack1111_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨ੩") in app:
        if os.path.exists(app[bstack1111_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ੪")]):
          bstack111l1l1l1l_opy_ = bstack1l111l1l1_opy_(config, app[bstack1111_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ੫")], app[bstack1111_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫ੬")])
        else:
          bstack1ll1ll11_opy_(bstack1ll1lll11_opy_.format(app))
      else:
        bstack1ll1ll11_opy_(bstack1ll11l1lll_opy_)
    else:
      for key in app:
        if key in bstack11l1l1l1ll_opy_:
          if key == bstack1111_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ੭"):
            if os.path.exists(app[key]):
              bstack111l1l1l1l_opy_ = bstack1l111l1l1_opy_(config, app[key])
            else:
              bstack1ll1ll11_opy_(bstack1ll1lll11_opy_.format(app))
          else:
            bstack111l1l1l1l_opy_ = app[key]
        else:
          bstack1ll1ll11_opy_(bstack1l11ll1lll_opy_)
  return bstack111l1l1l1l_opy_
def bstack111l1l11ll_opy_(bstack111l1l1l1l_opy_):
  import re
  bstack111l1llll_opy_ = re.compile(bstack1111_opy_ (u"ࡵࠦࡣࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫࠦࠥ੮"))
  bstack111l11111_opy_ = re.compile(bstack1111_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬ࠲࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰ࠤࠣ੯"))
  if bstack1111_opy_ (u"ࠬࡨࡳ࠻࠱࠲ࠫੰ") in bstack111l1l1l1l_opy_ or re.fullmatch(bstack111l1llll_opy_, bstack111l1l1l1l_opy_) or re.fullmatch(bstack111l11111_opy_, bstack111l1l1l1l_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack1ll11ll1l1_opy_, stage=STAGE.bstack111l1lllll_opy_, bstack11ll1l11l1_opy_=bstack1lll11ll1_opy_)
def bstack1l111l1l1_opy_(config, path, bstack1l11lll11l_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1111_opy_ (u"࠭ࡲࡣࠩੱ")).read()).hexdigest()
  bstack1l1ll1lll_opy_ = bstack11ll11l111_opy_(md5_hash)
  bstack111l1l1l1l_opy_ = None
  if bstack1l1ll1lll_opy_:
    logger.info(bstack111l1ll1l_opy_.format(bstack1l1ll1lll_opy_, md5_hash))
    return bstack1l1ll1lll_opy_
  bstack1l1llll111_opy_ = datetime.datetime.now()
  bstack11111ll1l_opy_ = MultipartEncoder(
    fields={
      bstack1111_opy_ (u"ࠧࡧ࡫࡯ࡩࠬੲ"): (os.path.basename(path), open(os.path.abspath(path), bstack1111_opy_ (u"ࠨࡴࡥࠫੳ")), bstack1111_opy_ (u"ࠩࡷࡩࡽࡺ࠯ࡱ࡮ࡤ࡭ࡳ࠭ੴ")),
      bstack1111_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ੵ"): bstack1l11lll11l_opy_
    }
  )
  response = requests.post(bstack11l1l111l1_opy_, data=bstack11111ll1l_opy_,
                           headers={bstack1111_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪ੶"): bstack11111ll1l_opy_.content_type},
                           auth=(config[bstack1111_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ੷")], config[bstack1111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ੸")]))
  try:
    res = json.loads(response.text)
    bstack111l1l1l1l_opy_ = res[bstack1111_opy_ (u"ࠧࡢࡲࡳࡣࡺࡸ࡬ࠨ੹")]
    logger.info(bstack111l111l1_opy_.format(bstack111l1l1l1l_opy_))
    bstack11l11l1111_opy_(md5_hash, bstack111l1l1l1l_opy_)
    cli.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠣࡪࡷࡸࡵࡀࡵࡱ࡮ࡲࡥࡩࡥࡡࡱࡲࠥ੺"), datetime.datetime.now() - bstack1l1llll111_opy_)
  except ValueError as err:
    bstack1ll1ll11_opy_(bstack1l1lll11ll_opy_.format(str(err)))
  return bstack111l1l1l1l_opy_
def bstack1lll11111l_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack1l1l11l1l_opy_
  bstack1lllll1l1l_opy_ = 1
  bstack1llll1ll_opy_ = 1
  if bstack1111_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ੻") in CONFIG:
    bstack1llll1ll_opy_ = CONFIG[bstack1111_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ੼")]
  else:
    bstack1llll1ll_opy_ = bstack1l1llll11l_opy_(framework_name, args) or 1
  if bstack1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ੽") in CONFIG:
    bstack1lllll1l1l_opy_ = len(CONFIG[bstack1111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ੾")])
  bstack1l1l11l1l_opy_ = int(bstack1llll1ll_opy_) * int(bstack1lllll1l1l_opy_)
def bstack1l1llll11l_opy_(framework_name, args):
  if framework_name == bstack1l11l11lll_opy_ and args and bstack1111_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ੿") in args:
      bstack111l1ll1ll_opy_ = args.index(bstack1111_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ઀"))
      return int(args[bstack111l1ll1ll_opy_ + 1]) or 1
  return 1
def bstack11ll11l111_opy_(md5_hash):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1111_opy_ (u"ࠨࡨ࡬ࡰࡪࡲ࡯ࡤ࡭ࠣࡲࡴࡺࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧ࠯ࠤࡺࡹࡩ࡯ࡩࠣࡦࡦࡹࡩࡤࠢࡩ࡭ࡱ࡫ࠠࡰࡲࡨࡶࡦࡺࡩࡰࡰࡶࠫઁ"))
    bstack111111l1_opy_ = os.path.join(os.path.expanduser(bstack1111_opy_ (u"ࠩࢁࠫં")), bstack1111_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪઃ"), bstack1111_opy_ (u"ࠫࡦࡶࡰࡖࡲ࡯ࡳࡦࡪࡍࡅ࠷ࡋࡥࡸ࡮࠮࡫ࡵࡲࡲࠬ઄"))
    if os.path.exists(bstack111111l1_opy_):
      try:
        bstack11ll11llll_opy_ = json.load(open(bstack111111l1_opy_, bstack1111_opy_ (u"ࠬࡸࡢࠨઅ")))
        if md5_hash in bstack11ll11llll_opy_:
          bstack111lll1l1_opy_ = bstack11ll11llll_opy_[md5_hash]
          bstack1l11lllll_opy_ = datetime.datetime.now()
          bstack1lllll1111_opy_ = datetime.datetime.strptime(bstack111lll1l1_opy_[bstack1111_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩઆ")], bstack1111_opy_ (u"ࠧࠦࡦ࠲ࠩࡲ࠵࡚ࠥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫઇ"))
          if (bstack1l11lllll_opy_ - bstack1lllll1111_opy_).days > 30:
            return None
          elif version.parse(str(__version__)) > version.parse(bstack111lll1l1_opy_[bstack1111_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ઈ")]):
            return None
          return bstack111lll1l1_opy_[bstack1111_opy_ (u"ࠩ࡬ࡨࠬઉ")]
      except Exception as e:
        logger.debug(bstack1111_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡵࡩࡦࡪࡩ࡯ࡩࠣࡑࡉ࠻ࠠࡩࡣࡶ࡬ࠥ࡬ࡩ࡭ࡧ࠽ࠤࢀࢃࠧઊ").format(str(e)))
    return None
  bstack111111l1_opy_ = os.path.join(os.path.expanduser(bstack1111_opy_ (u"ࠫࢃ࠭ઋ")), bstack1111_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬઌ"), bstack1111_opy_ (u"࠭ࡡࡱࡲࡘࡴࡱࡵࡡࡥࡏࡇ࠹ࡍࡧࡳࡩ࠰࡭ࡷࡴࡴࠧઍ"))
  lock_file = bstack111111l1_opy_ + bstack1111_opy_ (u"ࠧ࠯࡮ࡲࡧࡰ࠭઎")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack111111l1_opy_):
        with open(bstack111111l1_opy_, bstack1111_opy_ (u"ࠨࡴࠪએ")) as f:
          content = f.read().strip()
          if content:
            bstack11ll11llll_opy_ = json.loads(content)
            if md5_hash in bstack11ll11llll_opy_:
              bstack111lll1l1_opy_ = bstack11ll11llll_opy_[md5_hash]
              bstack1l11lllll_opy_ = datetime.datetime.now()
              bstack1lllll1111_opy_ = datetime.datetime.strptime(bstack111lll1l1_opy_[bstack1111_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬઐ")], bstack1111_opy_ (u"ࠪࠩࡩ࠵ࠥ࡮࠱ࠨ࡝ࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧઑ"))
              if (bstack1l11lllll_opy_ - bstack1lllll1111_opy_).days > 30:
                return None
              elif version.parse(str(__version__)) > version.parse(bstack111lll1l1_opy_[bstack1111_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ઒")]):
                return None
              return bstack111lll1l1_opy_[bstack1111_opy_ (u"ࠬ࡯ࡤࠨઓ")]
      return None
  except Exception as e:
    logger.debug(bstack1111_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡽࡩࡵࡪࠣࡪ࡮ࡲࡥࠡ࡮ࡲࡧࡰ࡯࡮ࡨࠢࡩࡳࡷࠦࡍࡅ࠷ࠣ࡬ࡦࡹࡨ࠻ࠢࡾࢁࠬઔ").format(str(e)))
    return None
def bstack11l11l1111_opy_(md5_hash, bstack111l1l1l1l_opy_):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1111_opy_ (u"ࠧࡧ࡫࡯ࡩࡱࡵࡣ࡬ࠢࡱࡳࡹࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦ࠮ࠣࡹࡸ࡯࡮ࡨࠢࡥࡥࡸ࡯ࡣࠡࡨ࡬ࡰࡪࠦ࡯ࡱࡧࡵࡥࡹ࡯࡯࡯ࡵࠪક"))
    bstack11llll111_opy_ = os.path.join(os.path.expanduser(bstack1111_opy_ (u"ࠨࢀࠪખ")), bstack1111_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩગ"))
    if not os.path.exists(bstack11llll111_opy_):
      os.makedirs(bstack11llll111_opy_)
    bstack111111l1_opy_ = os.path.join(os.path.expanduser(bstack1111_opy_ (u"ࠪࢂࠬઘ")), bstack1111_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫઙ"), bstack1111_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭ચ"))
    bstack1l11ll1l1l_opy_ = {
      bstack1111_opy_ (u"࠭ࡩࡥࠩછ"): bstack111l1l1l1l_opy_,
      bstack1111_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪજ"): datetime.datetime.strftime(datetime.datetime.now(), bstack1111_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬઝ")),
      bstack1111_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧઞ"): str(__version__)
    }
    try:
      bstack11ll11llll_opy_ = {}
      if os.path.exists(bstack111111l1_opy_):
        bstack11ll11llll_opy_ = json.load(open(bstack111111l1_opy_, bstack1111_opy_ (u"ࠪࡶࡧ࠭ટ")))
      bstack11ll11llll_opy_[md5_hash] = bstack1l11ll1l1l_opy_
      with open(bstack111111l1_opy_, bstack1111_opy_ (u"ࠦࡼ࠱ࠢઠ")) as outfile:
        json.dump(bstack11ll11llll_opy_, outfile)
    except Exception as e:
      logger.debug(bstack1111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡺࡶࡤࡢࡶ࡬ࡲ࡬ࠦࡍࡅ࠷ࠣ࡬ࡦࡹࡨࠡࡨ࡬ࡰࡪࡀࠠࡼࡿࠪડ").format(str(e)))
    return
  bstack11llll111_opy_ = os.path.join(os.path.expanduser(bstack1111_opy_ (u"࠭ࡾࠨઢ")), bstack1111_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧણ"))
  if not os.path.exists(bstack11llll111_opy_):
    os.makedirs(bstack11llll111_opy_)
  bstack111111l1_opy_ = os.path.join(os.path.expanduser(bstack1111_opy_ (u"ࠨࢀࠪત")), bstack1111_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩથ"), bstack1111_opy_ (u"ࠪࡥࡵࡶࡕࡱ࡮ࡲࡥࡩࡓࡄ࠶ࡊࡤࡷ࡭࠴ࡪࡴࡱࡱࠫદ"))
  lock_file = bstack111111l1_opy_ + bstack1111_opy_ (u"ࠫ࠳ࡲ࡯ࡤ࡭ࠪધ")
  bstack1l11ll1l1l_opy_ = {
    bstack1111_opy_ (u"ࠬ࡯ࡤࠨન"): bstack111l1l1l1l_opy_,
    bstack1111_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ઩"): datetime.datetime.strftime(datetime.datetime.now(), bstack1111_opy_ (u"ࠧࠦࡦ࠲ࠩࡲ࠵࡚ࠥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫપ")),
    bstack1111_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ફ"): str(__version__)
  }
  try:
    with FileLock(lock_file, timeout=10):
      bstack11ll11llll_opy_ = {}
      if os.path.exists(bstack111111l1_opy_):
        with open(bstack111111l1_opy_, bstack1111_opy_ (u"ࠩࡵࠫબ")) as f:
          content = f.read().strip()
          if content:
            bstack11ll11llll_opy_ = json.loads(content)
      bstack11ll11llll_opy_[md5_hash] = bstack1l11ll1l1l_opy_
      with open(bstack111111l1_opy_, bstack1111_opy_ (u"ࠥࡻࠧભ")) as outfile:
        json.dump(bstack11ll11llll_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1111_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡻ࡮ࡺࡨࠡࡨ࡬ࡰࡪࠦ࡬ࡰࡥ࡮࡭ࡳ࡭ࠠࡧࡱࡵࠤࡒࡊ࠵ࠡࡪࡤࡷ࡭ࠦࡵࡱࡦࡤࡸࡪࡀࠠࡼࡿࠪમ").format(str(e)))
def bstack1111l11l1_opy_(self):
  return
def bstack11l1l111l_opy_(self):
  return
def bstack1lll111ll1_opy_():
  global bstack1ll1ll111l_opy_
  bstack1ll1ll111l_opy_ = True
def bstack11111l111_opy_(self):
  global bstack111llll11l_opy_
  global bstack1l1l111l11_opy_
  global bstack1l111ll1_opy_
  bstack1l1l1llll1_opy_ = bstack1l11l1ll_opy_.bstack11l111111_opy_(EVENTS.bstack111ll1l1l1_opy_)
  try:
    if bstack1111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬય") in bstack111llll11l_opy_ and self.session_id != None and bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪર"), bstack1111_opy_ (u"ࠧࠨ઱")) != bstack1111_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩલ"):
      bstack111l11l111_opy_ = bstack1111_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩળ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ઴")
      if bstack111l11l111_opy_ == bstack1111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫવ"):
        bstack1l1lll111_opy_(logger)
      if self != None:
        bstack1l1lllll1l_opy_(self, bstack111l11l111_opy_, bstack1111_opy_ (u"ࠬ࠲ࠠࠨશ").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack1111_opy_ (u"࠭ࠧષ")
    if bstack1111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧસ") in bstack111llll11l_opy_ and getattr(threading.current_thread(), bstack1111_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧહ"), None):
      bstack1l11l11111_opy_.bstack111lllll1_opy_(self, bstack1l1l1l1ll_opy_, logger, wait=True)
    if bstack1111_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ઺") in bstack111llll11l_opy_:
      bstack1ll1ll11l1_opy_.bstack1l1lll1l_opy_(self)
    bstack1l11l1ll_opy_.end(EVENTS.bstack111ll1l1l1_opy_.value, bstack1l1l1llll1_opy_ + bstack1111_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ઻"), bstack1l1l1llll1_opy_ + bstack1111_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ઼"), status=True, failure=None, test_name=None)
  except Exception as e:
    logger.debug(bstack1111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࠨઽ") + str(e))
    bstack1l11l1ll_opy_.end(EVENTS.bstack111ll1l1l1_opy_.value, bstack1l1l1llll1_opy_ + bstack1111_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨા"), bstack1l1l1llll1_opy_ + bstack1111_opy_ (u"ࠢ࠻ࡧࡱࡨࠧિ"), status=False, failure=str(e), test_name=None)
  bstack1l111ll1_opy_(self)
  self.session_id = None
def bstack11ll11ll11_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack11lll111l1_opy_
    global bstack111llll11l_opy_
    command_executor = kwargs.get(bstack1111_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠫી"), bstack1111_opy_ (u"ࠩࠪુ"))
    bstack1llll1ll11_opy_ = False
    if type(command_executor) == str and bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ૂ") in command_executor:
      bstack1llll1ll11_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧૃ") in str(getattr(command_executor, bstack1111_opy_ (u"ࠬࡥࡵࡳ࡮ࠪૄ"), bstack1111_opy_ (u"࠭ࠧૅ"))):
      bstack1llll1ll11_opy_ = True
    else:
      kwargs = bstack11l1111111_opy_.bstack11l1l11l1_opy_(bstack1llll1l1l1_opy_=kwargs, config=CONFIG)
      return bstack11l1111l11_opy_(self, *args, **kwargs)
    if bstack1llll1ll11_opy_:
      bstack1ll11ll1_opy_ = bstack1l111l1l_opy_.bstack111l11l1l1_opy_(CONFIG, bstack111llll11l_opy_)
      if kwargs.get(bstack1111_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ૆")):
        kwargs[bstack1111_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩે")] = bstack11lll111l1_opy_(kwargs[bstack1111_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪૈ")], bstack111llll11l_opy_, CONFIG, bstack1ll11ll1_opy_)
      elif kwargs.get(bstack1111_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪૉ")):
        kwargs[bstack1111_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ૊")] = bstack11lll111l1_opy_(kwargs[bstack1111_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬો")], bstack111llll11l_opy_, CONFIG, bstack1ll11ll1_opy_)
  except Exception as e:
    logger.error(bstack1111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡦࡰࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡔࡆࡎࠤࡨࡧࡰࡴ࠼ࠣࡿࢂࠨૌ").format(str(e)))
  return bstack11l1111l11_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack1l1lll11l1_opy_, stage=STAGE.bstack111l1lllll_opy_, bstack11ll1l11l1_opy_=bstack1lll11ll1_opy_)
def bstack1ll1lllll_opy_(self, command_executor=bstack1111_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯࠲࠴࠺࠲࠵࠴࠰࠯࠳࠽࠸࠹࠺࠴્ࠣ"), *args, **kwargs):
  global bstack1l1l111l11_opy_
  global bstack1ll11111l1_opy_
  bstack11lll11l1_opy_ = bstack11ll11ll11_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack11l111ll11_opy_.on():
    return bstack11lll11l1_opy_
  try:
    logger.debug(bstack1111_opy_ (u"ࠨࡅࡲࡱࡲࡧ࡮ࡥࠢࡈࡼࡪࡩࡵࡵࡱࡵࠤࡼ࡮ࡥ࡯ࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥ࡯ࡳࠡࡨࡤࡰࡸ࡫ࠠ࠮ࠢࡾࢁࠬ૎").format(str(command_executor)))
    logger.debug(bstack1111_opy_ (u"ࠩࡋࡹࡧࠦࡕࡓࡎࠣ࡭ࡸࠦ࠭ࠡࡽࢀࠫ૏").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ૐ") in command_executor._url:
      global_config.bstack11llll1l1_opy_(bstack1111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬ૑"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨ૒") in command_executor):
    global_config.bstack11llll1l1_opy_(bstack1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ૓"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1l1111ll_opy_ = getattr(threading.current_thread(), bstack1111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡔࡦࡵࡷࡑࡪࡺࡡࠨ૔"), None)
  bstack1ll1l11l11_opy_ = {}
  if self.capabilities is not None:
    bstack1ll1l11l11_opy_[bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧ૕")] = self.capabilities.get(bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ૖"))
    bstack1ll1l11l11_opy_[bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ૗")] = self.capabilities.get(bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ૘"))
    bstack1ll1l11l11_opy_[bstack1111_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡤࡵࡰࡵ࡫ࡲࡲࡸ࠭૙")] = self.capabilities.get(bstack1111_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ૚"))
  if CONFIG.get(bstack1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ૛"), False) and bstack11l1111111_opy_.bstack1l111l11l1_opy_(bstack1ll1l11l11_opy_):
    threading.current_thread().a11yPlatform = True
  if bstack1111_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ૜") in bstack111llll11l_opy_ or bstack1111_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ૝") in bstack111llll11l_opy_:
    TestHubHandler.bstack1l11l1l11l_opy_(self)
  if bstack1111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ૞") in bstack111llll11l_opy_ and bstack1l1111ll_opy_ and bstack1l1111ll_opy_.get(bstack1111_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ૟"), bstack1111_opy_ (u"ࠬ࠭ૠ")) == bstack1111_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧૡ"):
    TestHubHandler.bstack1l11l1l11l_opy_(self)
  bstack1l1l111l11_opy_ = self.session_id
  with bstack111l1l11l_opy_:
    bstack1ll11111l1_opy_.append(self)
  return bstack11lll11l1_opy_
def bstack1ll11111l_opy_(args):
  return bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲࠨૢ") in str(args)
def bstack1l111l11ll_opy_(self, driver_command, *args, **kwargs):
  global bstack111lll1l1l_opy_
  global bstack1l1111ll1_opy_
  bstack1ll11l11ll_opy_ = bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬૣ"), None) and bstack1lll11lll1_opy_(
          threading.current_thread(), bstack1111_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ૤"), None)
  bstack1l11111lll_opy_ = bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ૥"), None) and bstack1lll11lll1_opy_(
          threading.current_thread(), bstack1111_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭૦"), None)
  bstack1l11l1ll1l_opy_ = getattr(self, bstack1111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬ૧"), None) != None and getattr(self, bstack1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭૨"), None) == True
  if not bstack1l1111ll1_opy_ and bstack1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ૩") in CONFIG and CONFIG[bstack1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ૪")] == True and bstack1l111l111_opy_.bstack1ll1111111_opy_(driver_command) and (bstack1l11l1ll1l_opy_ or bstack1ll11l11ll_opy_ or bstack1l11111lll_opy_) and not bstack1ll11111l_opy_(args):
    try:
      bstack1l1111ll1_opy_ = True
      logger.debug(bstack1111_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡽࢀࠫ૫").format(driver_command))
      bstack1llll1l11l_opy_ = perform_scan(self, driver_command=driver_command)
      logger.debug(bstack1llll1l11l_opy_)
      try:
        bstack1llll11l_opy_ = {
          bstack1111_opy_ (u"ࠥࡶࡪࡷࡵࡦࡵࡷࠦ૬"): {
            bstack1111_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࠧ૭"): bstack1111_opy_ (u"ࠧࡇ࠱࠲࡛ࡢࡗࡈࡇࡎࠣ૮"),
            bstack1111_opy_ (u"ࠨࡰࡢࡴࡤࡱࡪࡺࡥࡳࡵࠥ૯"): [
              {
                bstack1111_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢ૰"): driver_command
              }
            ]
          },
          bstack1111_opy_ (u"ࠣࡴࡨࡷࡵࡵ࡮ࡴࡧࠥ૱"): {
            bstack1111_opy_ (u"ࠤࡥࡳࡩࡿࠢ૲"): {
              bstack1111_opy_ (u"ࠥࡱࡸ࡭ࠢ૳"): bstack1llll1l11l_opy_.get(bstack1111_opy_ (u"ࠦࡲࡹࡧࠣ૴"), bstack1111_opy_ (u"ࠧࠨ૵")) if isinstance(bstack1llll1l11l_opy_, dict) else bstack1111_opy_ (u"ࠨࠢ૶"),
              bstack1111_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳࠣ૷"): bstack1llll1l11l_opy_.get(bstack1111_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴࠤ૸"), True) if isinstance(bstack1llll1l11l_opy_, dict) else True
            }
          }
        }
        logger.debug(bstack1111_opy_ (u"ࠩࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡧࡦࡴࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡱࡵࡧࠡࡦࡤࡸࡦࡀࠠࡼࡿࠪૹ").format(bstack1llll11l_opy_))
        bstack11llllll1l_opy_.info(json.dumps(bstack1llll11l_opy_, separators=(bstack1111_opy_ (u"ࠪ࠰ࠬૺ"), bstack1111_opy_ (u"ࠫ࠿࠭ૻ"))))
      except Exception as bstack1l111l1l11_opy_:
        logger.debug(bstack1111_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡮ࡲ࡫ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡣࡢࡰࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠬૼ").format(str(bstack1l111l1l11_opy_)))
    except Exception as err:
      logger.debug(bstack1111_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡩࡷ࡬࡯ࡳ࡯ࠣࡷࡨࡧ࡮ࠡࡽࢀࠫ૽").format(str(err)))
    bstack1l1111ll1_opy_ = False
  response = bstack111lll1l1l_opy_(self, driver_command, *args, **kwargs)
  if (bstack1111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭૾") in str(bstack111llll11l_opy_).lower() or bstack1111_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ૿") in str(bstack111llll11l_opy_).lower()) and bstack11l111ll11_opy_.on():
    try:
      if driver_command == bstack1111_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭଀"):
        TestHubHandler.bstack1l11l1l1l_opy_({
            bstack1111_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩଁ"): response[bstack1111_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪଂ")],
            bstack1111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬଃ"): TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack11l111ll11_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
def bstack11lll11lll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack1l1l111l11_opy_
  global bstack11l11ll1_opy_
  global bstack1lll11ll1_opy_
  global bstack1lll11l1ll_opy_
  global bstack111lllll11_opy_
  global bstack111llll11l_opy_
  global bstack11l1111l11_opy_
  global bstack1ll11111l1_opy_
  global bstack11ll1l1l1_opy_
  global bstack1l1l1l1ll_opy_
  bstack1l1l1llll1_opy_ = bstack1l11l1ll_opy_.bstack11l111111_opy_(EVENTS.bstack1l1l1111_opy_.value)
  if os.getenv(bstack1111_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ଄")) is not None and bstack11l1111111_opy_.bstack1l1l1ll1l_opy_(CONFIG) is None:
    CONFIG[bstack1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧଅ")] = True
  CONFIG[bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪଆ")] = str(bstack111llll11l_opy_) + str(__version__)
  bstack11l1l11l1l_opy_ = os.environ[bstack1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧଇ")]
  bstack1ll11ll1_opy_ = bstack1l111l1l_opy_.bstack111l11l1l1_opy_(CONFIG, bstack111llll11l_opy_)
  CONFIG[bstack1111_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ଈ")] = bstack11l1l11l1l_opy_
  CONFIG[bstack1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ଉ")] = bstack1ll11ll1_opy_
  if CONFIG.get(bstack1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬଊ"),bstack1111_opy_ (u"࠭ࠧଋ")) and bstack1111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ଌ") in bstack111llll11l_opy_:
    CONFIG[bstack1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ଍")].pop(bstack1111_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ଎"), None)
    CONFIG[bstack1111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪଏ")].pop(bstack1111_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩଐ"), None)
  command_executor = bstack1111l111l_opy_()
  logger.debug(bstack1ll1l1l11l_opy_.format(command_executor))
  proxy = bstack1lllll111_opy_(CONFIG, proxy)
  bstack111ll11111_opy_ = 0 if bstack11l11ll1_opy_ < 0 else bstack11l11ll1_opy_
  try:
    if bstack1lll11l1ll_opy_ is True:
      bstack111ll11111_opy_ = int(multiprocessing.current_process().name)
    elif bstack111lllll11_opy_ is True:
      bstack111ll11111_opy_ = int(threading.current_thread().name)
  except:
    bstack111ll11111_opy_ = 0
  bstack1l1l1l11l1_opy_ = bstack1ll11l1l11_opy_(CONFIG, bstack111ll11111_opy_)
  logger.debug(bstack1l11111111_opy_.format(str(bstack1l1l1l11l1_opy_)))
  if bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ଑") in CONFIG and bstack11ll1l1l1l_opy_(CONFIG[bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ଒")]):
    bstack11ll11l11_opy_(bstack1l1l1l11l1_opy_)
  if bstack11l1111111_opy_.bstack111ll1lll1_opy_(CONFIG, bstack111ll11111_opy_) and bstack11l1111111_opy_.bstack1ll1111l1l_opy_(bstack1l1l1l11l1_opy_, options, desired_capabilities, CONFIG):
    threading.current_thread().a11yPlatform = True
    if (cli.accessibility is None or not cli.accessibility.is_enabled()):
      bstack11l1111111_opy_.set_capabilities(bstack1l1l1l11l1_opy_, CONFIG)
  if desired_capabilities:
    bstack1l11lll11_opy_ = bstack11l1ll1ll1_opy_(desired_capabilities)
    bstack1l11lll11_opy_[bstack1111_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧଓ")] = bstack1ll1l1ll11_opy_(CONFIG)
    bstack1l1l1ll11l_opy_ = bstack1ll11l1l11_opy_(bstack1l11lll11_opy_)
    if bstack1l1l1ll11l_opy_:
      bstack1l1l1l11l1_opy_ = update(bstack1l1l1ll11l_opy_, bstack1l1l1l11l1_opy_)
    desired_capabilities = None
  if options:
    bstack111ll1l111_opy_(options, bstack1l1l1l11l1_opy_)
  if not options:
    options = bstack11l111l111_opy_(bstack1l1l1l11l1_opy_)
  try:
    if bstack11l1l11l11_opy_:
      def _1l1llll1l_opy_(bstack11lll1l1l_opy_):
        if not isinstance(bstack11lll1l1l_opy_, dict):
          return
        for _1ll1ll1l_opy_ in list(bstack11lll1l1l_opy_.keys()):
          _111l111l1l_opy_ = bstack11lll1l1l_opy_[_1ll1ll1l_opy_]
          if _111l111l1l_opy_ is None:
            bstack11lll1l1l_opy_.pop(_1ll1ll1l_opy_, None)
          elif isinstance(_111l111l1l_opy_, dict):
            _1l1llll1l_opy_(_111l111l1l_opy_)
      _1l1llll1l_opy_(bstack1l1l1l11l1_opy_)
      _1l1llll1l_opy_(desired_capabilities)
      if options is not None and hasattr(options, bstack1111_opy_ (u"ࠨࡡࡦࡥࡵࡹࠧଔ")):
        _1l1llll1l_opy_(options._caps)
  except Exception as e:
    logger.debug(bstack1111_opy_ (u"ࠤࡰࡳࡩࡥࡩ࡯࡫ࡷࠬ࠮ࠦࡰࡰࡵࡷ࠱ࡴࡶࡴࡪࡱࡱࡷࠥࡶࡲࡶࡰࡨࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽࠣକ").format(e))
  if bstack11l1l11l11_opy_:
    options = bstack111l1l1ll_opy_(options)
  bstack1l1l1l1ll_opy_ = CONFIG.get(bstack1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ଖ"))[bstack111ll11111_opy_]
  if proxy and bstack1l111ll11l_opy_() >= version.parse(bstack1111_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫଗ")):
    options.proxy(proxy)
  if options and bstack1l111ll11l_opy_() >= version.parse(bstack1111_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫଘ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1l111ll11l_opy_() < version.parse(bstack1111_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬଙ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1l1l1l11l1_opy_)
  logger.info(bstack111111lll_opy_)
  bstack1ll1l11ll1_opy_.end(EVENTS.bstack11l11lllll_opy_.value, EVENTS.bstack11l11lllll_opy_.value + bstack1111_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢଚ"), EVENTS.bstack11l11lllll_opy_.value + bstack1111_opy_ (u"ࠣ࠼ࡨࡲࡩࠨଛ"), status=True, failure=None, test_name=bstack1lll11ll1_opy_)
  if bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡴࡷࡵࡦࡪ࡮ࡨࠫଜ") in kwargs:
    del kwargs[bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡵࡸ࡯ࡧ࡫࡯ࡩࠬଝ")]
  bstack1l11l1ll_opy_.end(EVENTS.bstack1l1l1111_opy_.value, bstack1l1l1llll1_opy_ + bstack1111_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦଞ"), bstack1l1l1llll1_opy_ + bstack1111_opy_ (u"ࠧࡀࡥ࡯ࡦࠥଟ"), status=True, failure=None, test_name=bstack1lll11ll1_opy_)
  try:
    if bstack1l111ll11l_opy_() >= version.parse(bstack1111_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ଠ")):
      bstack11l1111l11_opy_(self, command_executor=command_executor,
                options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
    elif bstack1l111ll11l_opy_() >= version.parse(bstack1111_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ଡ")):
      bstack11l1111l11_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities, options=options,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l111ll11l_opy_() >= version.parse(bstack1111_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨଢ")):
      bstack11l1111l11_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    else:
      bstack11l1111l11_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive)
  except Exception as bstack1lll11l1_opy_:
    logger.error(bstack1l11111l1_opy_.format(bstack1111_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠨଣ"), str(bstack1lll11l1_opy_)))
    raise bstack1lll11l1_opy_
  bstack1l1l1llll1_opy_ = bstack1l11l1ll_opy_.bstack11l111111_opy_(EVENTS.bstack1l1lll11l1_opy_.value)
  if bstack11l1111111_opy_.bstack111ll1lll1_opy_(CONFIG, bstack111ll11111_opy_) and bstack11l1111111_opy_.bstack1ll1111l1l_opy_(self.caps, options, desired_capabilities):
    if CONFIG[bstack1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬତ")][bstack1111_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪଥ")] == True:
      threading.current_thread().appA11yPlatform = True
      if cli.accessibility is None or not cli.accessibility.is_enabled():
        bstack11l1111111_opy_.set_capabilities(bstack1l1l1l11l1_opy_, CONFIG)
  try:
    bstack11llllllll_opy_ = bstack1111_opy_ (u"ࠬ࠭ଦ")
    if bstack1l111ll11l_opy_() >= version.parse(bstack1111_opy_ (u"࠭࠴࠯࠲࠱࠴ࡧ࠷ࠧଧ")):
      if self.caps is not None:
        bstack11llllllll_opy_ = self.caps.get(bstack1111_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢନ"))
    else:
      if self.capabilities is not None:
        bstack11llllllll_opy_ = self.capabilities.get(bstack1111_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣ଩"))
    if bstack11llllllll_opy_:
      bstack1l1l1ll11_opy_(bstack11llllllll_opy_)
      if bstack1l111ll11l_opy_() <= version.parse(bstack1111_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩପ")):
        if bstack11l1l1lll_opy_.startswith(bstack1111_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫଫ")) or bstack11l1l1lll_opy_.startswith(bstack1111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࠭ବ")):
          self.command_executor._url = bstack11l1l1lll_opy_
        else:
          self.command_executor._url = bstack1111_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨଭ") + bstack11l1l1lll_opy_ + bstack1111_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥମ")
      else:
        self.command_executor._url = bstack1111_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤଯ") + bstack11llllllll_opy_ + bstack1111_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤର")
      logger.debug(bstack1l1lllll11_opy_.format(bstack11llllllll_opy_))
    else:
      logger.debug(bstack111l1l1l11_opy_.format(bstack1111_opy_ (u"ࠤࡒࡴࡹ࡯࡭ࡢ࡮ࠣࡌࡺࡨࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦࠥ଱")))
  except Exception as e:
    logger.debug(bstack111l1l1l11_opy_.format(e))
  if bstack1111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩଲ") in bstack111llll11l_opy_:
    bstack1l1ll1l1l1_opy_(bstack11l11ll1_opy_, bstack11ll1l1l1_opy_)
  bstack1l1l111l11_opy_ = self.session_id
  if bstack1111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫଳ") in bstack111llll11l_opy_ or bstack1111_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ଴") in bstack111llll11l_opy_ or bstack1111_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬଵ") in bstack111llll11l_opy_ or bstack1111_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡨࡧࡱࡩࡷ࡯ࡣࠨଶ") in bstack111llll11l_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack1l1111ll_opy_ = getattr(threading.current_thread(), bstack1111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡕࡧࡶࡸࡒ࡫ࡴࡢࠩଷ"), None)
  if bstack1111_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩସ") in bstack111llll11l_opy_ or bstack1111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩହ") in bstack111llll11l_opy_:
    TestHubHandler.bstack1l11l1l11l_opy_(self)
  if bstack1111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ଺") in bstack111llll11l_opy_ and bstack1l1111ll_opy_ and bstack1l1111ll_opy_.get(bstack1111_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ଻"), bstack1111_opy_ (u"଼࠭ࠧ")) == bstack1111_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨଽ"):
    TestHubHandler.bstack1l11l1l11l_opy_(self)
  with bstack111l1l11l_opy_:
    bstack1ll11111l1_opy_.append(self)
  if bstack1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫା") in CONFIG and bstack1111_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧି") in CONFIG[bstack1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ୀ")][bstack111ll11111_opy_]:
    bstack1lll11ll1_opy_ = CONFIG[bstack1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧୁ")][bstack111ll11111_opy_][bstack1111_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪୂ")]
  logger.debug(bstack1lll1l1l1_opy_.format(bstack1l1l111l11_opy_))
  bstack1l11l1ll_opy_.end(EVENTS.bstack1l1lll11l1_opy_.value, bstack1l1l1llll1_opy_ + bstack1111_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨୃ"), bstack1l1l1llll1_opy_ + bstack1111_opy_ (u"ࠢ࠻ࡧࡱࡨࠧୄ"), status=True, failure=None, test_name=bstack1lll11ll1_opy_)
ROBOT_PLAYWRIGHT_CDP_URL = None
try:
  try:
    import Browser
    import os
    from subprocess import Popen
    from browserstack_sdk.__init__ import bstack1ll1l11l1l_opy_
    def bstack11l1l1ll1_opy_(self, args, **kwargs):
      global CONFIG
      global bstack11l1111l1_opy_
      global ROBOT_PLAYWRIGHT_CDP_URL
      from browserstack_sdk.__init__ import LAUNCH_PATCH_ROBOT_PLAYWRIGHT
      if(bstack1111_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࠮࡫ࡵࠥ୅") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1111_opy_ (u"ࠩࢁࠫ୆")), bstack1111_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪେ"), bstack1111_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭ୈ")), bstack1111_opy_ (u"ࠬࡽࠧ୉")) as fp:
          fp.write(bstack1111_opy_ (u"ࠨࠢ୊"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1111_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤୋ")))):
          with open(args[1], bstack1111_opy_ (u"ࠨࡴࠪୌ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1111_opy_ (u"ࠩࡤࡷࡾࡴࡣࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡣࡳ࡫ࡷࡑࡣࡪࡩ࠭ࡩ࡯࡯ࡶࡨࡼࡹ࠲ࠠࡱࡣࡪࡩࠥࡃࠠࡷࡱ࡬ࡨࠥ࠶ࠩࠨ୍") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1lll11l1l1_opy_)
            if bstack1111_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ୎") in CONFIG and str(CONFIG[bstack1111_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ୏")]).lower() != bstack1111_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ୐"):
                cdpUrl = bstack1ll1l11l1l_opy_()
                LAUNCH_PATCH_ROBOT_PLAYWRIGHT = bstack1111_opy_ (u"࠭ࠧࠨࠌ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࠏࡩ࡯࡯ࡵࡷࠤࡧࡹࡴࡢࡥ࡮ࡣࡵࡧࡴࡩࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸ࡣ࠻ࠋࡥࡲࡲࡸࡺࠠࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠲࡟࠾ࠎࡨࡵ࡮ࡴࡶࠣࡴࡤ࡯࡮ࡥࡧࡻࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠲࡞࠽ࠍࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡷࡱ࡯ࡣࡦࠪ࠳࠰ࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳ࠪ࠽ࠍࡧࡴࡴࡳࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣࠫ࠾ࠎ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡱࡧࡵ࡯ࡥ࡫ࠤࡂࠦࡡࡴࡻࡱࡧࠥ࠮࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸ࠯ࠠ࠾ࡀࠣࡿࢀࠐࠠࠡ࡮ࡨࡸࠥࡩࡡࡱࡵ࠾ࠎࠥࠦࡴࡳࡻࠣࡿࢀࠐࠠࠡࠢࠣࡧࡦࡶࡳࠡ࠿ࠣࡎࡘࡕࡎ࠯ࡲࡤࡶࡸ࡫ࠨࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷ࠮ࡁࠊࠡࠢࢀࢁࠥࡩࡡࡵࡥ࡫ࠤ࠭࡫ࡸࠪࠢࡾࡿࠏࠦࠠࠡࠢࡦࡳࡳࡹ࡯࡭ࡧ࠱ࡩࡷࡸ࡯ࡳࠪࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ࠾ࠧ࠲ࠠࡦࡺࠬ࠿ࠏࠦࠠࡾࡿࠍࠤࠥࡸࡥࡵࡷࡵࡲࠥࡧࡷࡢ࡫ࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡨࡵ࡮࡯ࡧࡦࡸ࠭ࢁࡻࠋࠢࠣࠤࠥࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵ࠼ࠣࠫࢀࡩࡤࡱࡗࡵࡰࢂ࠭ࠠࠬࠢࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩ࠭ࠌࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴࠌࠣࠤࢂࢃࠩ࠼ࠌࢀࢁࡀࠐࡣࡰࡰࡶࡸࠥࡵࡲࡪࡩ࡬ࡲࡦࡲ࡟ࡤࡱࡱࡲࡪࡩࡴࠡ࠿ࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷ࠲ࡧ࡯࡮ࡥࠪ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱ࠮ࡤࡪࡵࡳࡲ࡯ࡵ࡮ࠫ࠾ࠎ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡨࡵ࡮࡯ࡧࡦࡸࠥࡃࠠࡢࡵࡼࡲࡨࠦࠨࡤࡱࡱࡲࡪࡩࡴࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁࡻࠋࠢࠣࡰࡪࡺࠠࡤࡣࡳࡷࡀࠐࠠࠡࡶࡵࡽࠥࢁࡻࠋࠢࠣࠤࠥࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࠼ࠌࠣࠤࢂࢃࠠࡤࡣࡷࡧ࡭ࠦࠨࡦࡺࠬࠤࢀࢁࠊࠡࠢࢀࢁࠏࠦࠠࡤࡱࡱࡷࡹࠦ࡭ࡰࡦ࡬ࡪ࡮࡫ࡤࡆࡰࡧࡴࡴ࡯࡮ࡵࠢࡀࠤࠬࢁࡣࡥࡲࡘࡶࡱࢃࠧࠡ࠭ࠣࡩࡳࡩ࡯ࡥࡧࡘࡖࡎࡉ࡯࡮ࡲࡲࡲࡪࡴࡴࠩࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡦࡥࡵࡹࠩࠪ࠽ࠍࠤࠥࡸࡥࡵࡷࡵࡲࠥࡧࡷࡢ࡫ࡷࠤࡴࡸࡩࡨ࡫ࡱࡥࡱࡥࡣࡰࡰࡱࡩࡨࡺࠨࡼࡽࠍࠤࠥࠦࠠ࠯࠰࠱ࡧࡴࡴ࡮ࡦࡥࡷࡓࡵࡺࡩࡰࡰࡶ࠰ࠏࠦࠠࠡࠢࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹࡀࠠ࡮ࡱࡧ࡭࡫࡯ࡥࡥࡇࡱࡨࡵࡵࡩ࡯ࡶࠍࠤࠥࢃࡽࠪ࠽ࠍࢁࢂࡁࠊ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱ࠍࠫࠬ࠭୑").format(cdpUrl=cdpUrl)
            lines.insert(1, LAUNCH_PATCH_ROBOT_PLAYWRIGHT)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1111_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤ୒")), bstack1111_opy_ (u"ࠨࡹࠪ୓")) as bstack1l1111l1_opy_:
              bstack1l1111l1_opy_.writelines(lines)
        CONFIG[bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ୔")] = str(bstack111llll11l_opy_) + str(__version__)
        bstack11l1l11l1l_opy_ = os.environ[bstack1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ୕")]
        bstack1ll11ll1_opy_ = bstack1l111l1l_opy_.bstack111l11l1l1_opy_(CONFIG, bstack111llll11l_opy_)
        CONFIG[bstack1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧୖ")] = bstack11l1l11l1l_opy_
        CONFIG[bstack1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧୗ")] = bstack1ll11ll1_opy_
        bstack111ll11111_opy_ = 0 if bstack11l11ll1_opy_ < 0 else bstack11l11ll1_opy_
        try:
          if bstack1lll11l1ll_opy_ is True:
            bstack111ll11111_opy_ = int(multiprocessing.current_process().name)
          elif bstack111lllll11_opy_ is True:
            bstack111ll11111_opy_ = int(threading.current_thread().name)
        except:
          bstack111ll11111_opy_ = 0
        CONFIG[bstack1111_opy_ (u"ࠨࡵࡴࡧ࡚࠷ࡈࠨ୘")] = False
        CONFIG[bstack1111_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ୙")] = True
        bstack1l1l1l11l1_opy_ = bstack1ll11l1l11_opy_(CONFIG, bstack111ll11111_opy_)
        logger.debug(bstack1l11111111_opy_.format(str(bstack1l1l1l11l1_opy_)))
        if CONFIG.get(bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ୚")):
          bstack11ll11l11_opy_(bstack1l1l1l11l1_opy_)
          bstack1l1l1l11l1_opy_[bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ୛")] = os.environ[bstack1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬଡ଼")]
        import urllib.parse
        if bstack1111_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨଢ଼") in CONFIG and str(CONFIG[bstack1111_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ୞")]).lower() != bstack1111_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬୟ"):
          ROBOT_PLAYWRIGHT_CDP_URL = bstack1ll1l11l1l_opy_() + urllib.parse.quote(json.dumps(bstack1l1l1l11l1_opy_))
        else:
          ROBOT_PLAYWRIGHT_CDP_URL = bstack1111_opy_ (u"ࠧࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠩୠ") + urllib.parse.quote(json.dumps(bstack1l1l1l11l1_opy_))
        os.environ[bstack1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡑࡅࡓ࡙ࡥࡐࡘࡡࡆࡈࡕࡥࡕࡓࡎࠪୡ")] = ROBOT_PLAYWRIGHT_CDP_URL
        if bstack1111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬୢ") in CONFIG and bstack1111_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨୣ") in CONFIG[bstack1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ୤")][bstack111ll11111_opy_]:
          bstack1lll11ll1_opy_ = CONFIG[bstack1111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ୥")][bstack111ll11111_opy_][bstack1111_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ୦")]
        args.append(os.path.join(os.path.expanduser(bstack1111_opy_ (u"ࠧࡿࠩ୧")), bstack1111_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ୨"), bstack1111_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫ୩")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1l1l1l11l1_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1111_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧ୪"))
      bstack11l1111l1_opy_ = True
      return bstack1lll1ll11_opy_(self, args, **kwargs)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1l11111l1l_opy_(self,
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
    global bstack11l11ll1_opy_
    global bstack1lll11ll1_opy_
    global bstack1lll11l1ll_opy_
    global bstack111lllll11_opy_
    global bstack111llll11l_opy_
    CONFIG[bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭୫")] = str(bstack111llll11l_opy_) + str(__version__)
    bstack11l1l11l1l_opy_ = os.environ[bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ୬")]
    bstack1ll11ll1_opy_ = bstack1l111l1l_opy_.bstack111l11l1l1_opy_(CONFIG, bstack111llll11l_opy_)
    CONFIG[bstack1111_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ୭")] = bstack11l1l11l1l_opy_
    CONFIG[bstack1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩ୮")] = bstack1ll11ll1_opy_
    bstack111ll11111_opy_ = 0 if bstack11l11ll1_opy_ < 0 else bstack11l11ll1_opy_
    try:
      if bstack1lll11l1ll_opy_ is True:
        bstack111ll11111_opy_ = int(multiprocessing.current_process().name)
      elif bstack111lllll11_opy_ is True:
        bstack111ll11111_opy_ = int(threading.current_thread().name)
    except:
      bstack111ll11111_opy_ = 0
    CONFIG[bstack1111_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢ୯")] = True
    bstack1l1l1l11l1_opy_ = bstack1ll11l1l11_opy_(CONFIG, bstack111ll11111_opy_)
    logger.debug(bstack1l11111111_opy_.format(str(bstack1l1l1l11l1_opy_)))
    if CONFIG.get(bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭୰")):
      bstack11ll11l11_opy_(bstack1l1l1l11l1_opy_)
    if bstack1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ୱ") in CONFIG and bstack1111_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ୲") in CONFIG[bstack1111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ୳")][bstack111ll11111_opy_]:
      bstack1lll11ll1_opy_ = CONFIG[bstack1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ୴")][bstack111ll11111_opy_][bstack1111_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ୵")]
    import urllib
    import json
    if bstack1111_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ୶") in CONFIG and str(CONFIG[bstack1111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭୷")]).lower() != bstack1111_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩ୸"):
        bstack11lll1ll1l_opy_ = bstack1ll1l11l1l_opy_()
        cdpUrl = bstack11lll1ll1l_opy_ + urllib.parse.quote(json.dumps(bstack1l1l1l11l1_opy_))
    else:
        cdpUrl = bstack1111_opy_ (u"ࠫࡼࡹࡳ࠻࠱࠲ࡧࡩࡶ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠿ࡤࡣࡳࡷࡂ࠭୹") + urllib.parse.quote(json.dumps(bstack1l1l1l11l1_opy_))
    browser = self.connect(cdpUrl)
    return browser
except Exception as e:
    pass
def bstack11l11l1l1l_opy_():
    global bstack11l1111l1_opy_
    global bstack111llll11l_opy_
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack111lll111l_opy_
        global global_config
        if not bstack1111ll1l_opy_:
          global bstack111llll1l1_opy_
          if not bstack111llll1l1_opy_:
            from bstack_utils.helper import bstack111l1l1l1_opy_, bstack111ll1ll1l_opy_, bstack11l1111l1l_opy_
            bstack111llll1l1_opy_ = bstack111l1l1l1_opy_()
            bstack111ll1ll1l_opy_(bstack111llll11l_opy_)
            bstack1ll11ll1_opy_ = bstack1l111l1l_opy_.bstack111l11l1l1_opy_(CONFIG, bstack111llll11l_opy_)
            global_config.bstack11llll1l1_opy_(bstack1111_opy_ (u"ࠧࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡓࡖࡔࡊࡕࡄࡖࡢࡑࡆࡖࠢ୺"), bstack1ll11ll1_opy_)
          BrowserType.connect = bstack111lll111l_opy_
          return
        BrowserType.launch = bstack1l11111l1l_opy_
        bstack11l1111l1_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack11l1l1ll1_opy_
      bstack11l1111l1_opy_ = True
    except Exception as e:
      pass
def bstack1lllll1lll_opy_(context, bstack11ll1ll1l_opy_):
  try:
    if getattr(context, bstack1111_opy_ (u"࠭ࡰࡢࡩࡨࠫ୻"), None):
      context.page.evaluate(bstack1111_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣ୼"), bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬ୽")+ json.dumps(bstack11ll1ll1l_opy_) + bstack1111_opy_ (u"ࠤࢀࢁࠧ୾"))
  except Exception as e:
    logger.debug(bstack1111_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽ࠻ࠢࡾࢁࠧ୿").format(str(e), traceback.format_exc()))
def bstack1l1111ll1l_opy_(context, message, level):
  try:
    if getattr(context, bstack1111_opy_ (u"ࠫࡵࡧࡧࡦࠩ஀"), None):
      context.page.evaluate(bstack1111_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨ஁"), bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫஂ") + json.dumps(message) + bstack1111_opy_ (u"ࠧ࠭ࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠪஃ") + json.dumps(level) + bstack1111_opy_ (u"ࠨࡿࢀࠫ஄"))
  except Exception as e:
    logger.debug(bstack1111_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠢࡾࢁ࠿ࠦࡻࡾࠤஅ").format(str(e), traceback.format_exc()))
@measure(event_name=EVENTS.bstack11lll1l1_opy_, stage=STAGE.bstack111l1lllll_opy_, bstack11ll1l11l1_opy_=bstack1lll11ll1_opy_)
def bstack11ll11lll_opy_(self, url):
  global bstack1111ll1lll_opy_
  try:
    bstack1l11l1l1ll_opy_(url)
  except Exception as err:
    logger.debug(bstack1ll111ll_opy_.format(str(err)))
  try:
    bstack1111ll1lll_opy_(self, url)
  except Exception as e:
    try:
      bstack11l111llll_opy_ = str(e)
      if any(err_msg in bstack11l111llll_opy_ for err_msg in bstack1ll11ll11_opy_):
        bstack1l11l1l1ll_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1ll111ll_opy_.format(str(err)))
    raise e
def bstack11l1llll_opy_(self):
  global bstack1lll11l11l_opy_
  bstack1lll11l11l_opy_ = self
  return
def bstack1ll11l11l1_opy_(self):
  global bstack11l11111l_opy_
  bstack11l11111l_opy_ = self
  return
def bstack1lll1ll1_opy_(test_name, bstack1ll1l1l1l1_opy_):
  global CONFIG
  if percy.bstack1lll1l1l_opy_() == bstack1111_opy_ (u"ࠥࡸࡷࡻࡥࠣஆ"):
    bstack1llll1l111_opy_ = os.path.relpath(bstack1ll1l1l1l1_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack1llll1l111_opy_)
    bstack11ll1l11l1_opy_ = suite_name + bstack1111_opy_ (u"ࠦ࠲ࠨஇ") + test_name
    threading.current_thread().percySessionName = bstack11ll1l11l1_opy_
def bstack11111l1l1_opy_(self, test, *args, **kwargs):
  global bstack1l1l11l1_opy_
  test_name = None
  bstack1ll1l1l1l1_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1ll1l1l1l1_opy_ = str(test.source)
  bstack1lll1ll1_opy_(test_name, bstack1ll1l1l1l1_opy_)
  bstack1l1l11l1_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.bstack1llll111l1_opy_, stage=STAGE.bstack111l1lllll_opy_, bstack11ll1l11l1_opy_=bstack1lll11ll1_opy_)
def bstack1ll1l11111_opy_(driver, bstack11ll1l11l1_opy_):
  if not bstack1ll1llll1_opy_ and bstack11ll1l11l1_opy_:
      bstack1111ll1l1_opy_ = {
          bstack1111_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬஈ"): bstack1111_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧஉ"),
          bstack1111_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪஊ"): {
              bstack1111_opy_ (u"ࠨࡰࡤࡱࡪ࠭஋"): bstack11ll1l11l1_opy_
          }
      }
      bstack1l1ll1ll1_opy_ = bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧ஌").format(json.dumps(bstack1111ll1l1_opy_))
      driver.execute_script(bstack1l1ll1ll1_opy_)
  if bstack1ll1111ll_opy_:
      bstack111111ll1_opy_ = {
          bstack1111_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪ஍"): bstack1111_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭எ"),
          bstack1111_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨஏ"): {
              bstack1111_opy_ (u"࠭ࡤࡢࡶࡤࠫஐ"): bstack11ll1l11l1_opy_ + bstack1111_opy_ (u"ࠧࠡࡲࡤࡷࡸ࡫ࡤࠢࠩ஑"),
              bstack1111_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧஒ"): bstack1111_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧஓ")
          }
      }
      if bstack1ll1111ll_opy_.status == bstack1111_opy_ (u"ࠪࡔࡆ࡙ࡓࠨஔ"):
          bstack1l11ll1l_opy_ = bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩக").format(json.dumps(bstack111111ll1_opy_))
          driver.execute_script(bstack1l11ll1l_opy_)
          bstack1l1lllll1l_opy_(driver, bstack1111_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ஖"))
      elif bstack1ll1111ll_opy_.status == bstack1111_opy_ (u"࠭ࡆࡂࡋࡏࠫ஗"):
          reason = bstack1111_opy_ (u"ࠢࠣ஘")
          bstack111ll11l1_opy_ = bstack11ll1l11l1_opy_ + bstack1111_opy_ (u"ࠨࠢࡩࡥ࡮ࡲࡥࡥࠩங")
          if bstack1ll1111ll_opy_.message:
              reason = str(bstack1ll1111ll_opy_.message)
              bstack111ll11l1_opy_ = bstack111ll11l1_opy_ + bstack1111_opy_ (u"ࠩࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸ࠺ࠡࠩச") + reason
          bstack111111ll1_opy_[bstack1111_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭஛")] = {
              bstack1111_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪஜ"): bstack1111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ஝"),
              bstack1111_opy_ (u"࠭ࡤࡢࡶࡤࠫஞ"): bstack111ll11l1_opy_
          }
          bstack1l11ll1l_opy_ = bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬட").format(json.dumps(bstack111111ll1_opy_))
          driver.execute_script(bstack1l11ll1l_opy_)
          bstack1l1lllll1l_opy_(driver, bstack1111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ஠"), reason)
          bstack11lllll1ll_opy_(reason, str(bstack1ll1111ll_opy_), str(bstack11l11ll1_opy_), logger)
@measure(event_name=EVENTS.bstack111l1l11l1_opy_, stage=STAGE.bstack111l1lllll_opy_, bstack11ll1l11l1_opy_=bstack1lll11ll1_opy_)
def bstack111llll1_opy_(driver, test):
  if percy.bstack1lll1l1l_opy_() == bstack1111_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ஡") and percy.bstack11l1l1lll1_opy_() == bstack1111_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧ஢"):
      bstack1llll1l1_opy_ = bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧண"), None)
      bstack11lllllll1_opy_(driver, bstack1llll1l1_opy_, test)
  if (bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩத"), None) and
      bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ஥"), None)) or (
      bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ஦"), None) and
      bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ஧"), None)):
      logger.info(bstack1111_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠠࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡵࡻࡦࡿ࠮ࠡࠤந"))
      bstack11l1111111_opy_.bstack1ll1ll1l11_opy_(driver, name=test.name, path=test.source)
def bstack11l1l11l_opy_(test, bstack11ll1l11l1_opy_):
    try:
      bstack1l1llll111_opy_ = datetime.datetime.now()
      data = {}
      if test:
        data[bstack1111_opy_ (u"ࠪࡲࡦࡳࡥࠨன")] = bstack11ll1l11l1_opy_
      if bstack1ll1111ll_opy_:
        if bstack1ll1111ll_opy_.status == bstack1111_opy_ (u"ࠫࡕࡇࡓࡔࠩப"):
          data[bstack1111_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ஫")] = bstack1111_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭஬")
        elif bstack1ll1111ll_opy_.status == bstack1111_opy_ (u"ࠧࡇࡃࡌࡐࠬ஭"):
          data[bstack1111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨம")] = bstack1111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩய")
          if bstack1ll1111ll_opy_.message:
            data[bstack1111_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪர")] = str(bstack1ll1111ll_opy_.message)
      user = CONFIG[bstack1111_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ற")]
      key = CONFIG[bstack1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨல")]
      host = bstack11111l1ll_opy_(cli.config, [bstack1111_opy_ (u"ࠨࡡࡱ࡫ࡶࠦள"), bstack1111_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡦࠤழ"), bstack1111_opy_ (u"ࠣࡣࡳ࡭ࠧவ")], bstack1111_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡵ࡯࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠥஶ"))
      url = bstack1111_opy_ (u"ࠪࡿࢂ࠵ࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡵࡨࡷࡸ࡯࡯࡯ࡵ࠲ࡿࢂ࠴ࡪࡴࡱࡱࠫஷ").format(host, bstack1l1l111l11_opy_)
      headers = {
        bstack1111_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪஸ"): bstack1111_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨஹ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers, auth=(user, key))
        cli.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠨࡨࡵࡶࡳ࠾ࡺࡶࡤࡢࡶࡨࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡷࡹࡧࡴࡶࡵࠥ஺"), datetime.datetime.now() - bstack1l1llll111_opy_)
    except Exception as e:
      logger.error(bstack1ll111l11_opy_.format(str(e)))
def bstack1111llll1l_opy_(test, bstack11ll1l11l1_opy_):
  global CONFIG
  global bstack11l11111l_opy_
  global bstack1lll11l11l_opy_
  global bstack1l1l111l11_opy_
  global bstack1ll1111ll_opy_
  global bstack1lll11ll1_opy_
  global bstack11l11111ll_opy_
  global bstack11l1ll111_opy_
  global bstack111l1111l_opy_
  global bstack1l11llllll_opy_
  global bstack1ll11111l1_opy_
  global bstack1l1l1l1ll_opy_
  global bstack1l1l1lll1_opy_
  try:
    if not bstack1l1l111l11_opy_:
      with bstack1l1l1lll1_opy_:
        bstack1lll11ll11_opy_ = os.path.join(os.path.expanduser(bstack1111_opy_ (u"ࠧࡿࠩ஻")), bstack1111_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ஼"), bstack1111_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫ஽"))
        if os.path.exists(bstack1lll11ll11_opy_):
          with open(bstack1lll11ll11_opy_, bstack1111_opy_ (u"ࠪࡶࠬா")) as f:
            content = f.read().strip()
            if content:
              bstack1111l1l1_opy_ = json.loads(bstack1111_opy_ (u"ࠦࢀࠨி") + content + bstack1111_opy_ (u"ࠬࠨࡸࠣ࠼ࠣࠦࡾࠨࠧீ") + bstack1111_opy_ (u"ࠨࡽࠣு"))
              bstack1l1l111l11_opy_ = bstack1111l1l1_opy_.get(str(threading.get_ident()))
  except Exception as e:
    logger.debug(bstack1111_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡲࡦࡣࡧ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡋࡇࡷࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬூ") + str(e))
  if not is_robot_playwright_installed():
    if bstack1ll11111l1_opy_:
      with bstack111l1l11l_opy_:
        bstack1l1ll11l1_opy_ = bstack1ll11111l1_opy_.copy()
      for driver in bstack1l1ll11l1_opy_:
        if bstack1l1l111l11_opy_ == driver.session_id:
          if test:
            bstack111llll1_opy_(driver, test)
          bstack1ll1l11111_opy_(driver, bstack11ll1l11l1_opy_)
    elif bstack1l1l111l11_opy_:
      bstack11l1l11l_opy_(test, bstack11ll1l11l1_opy_)
    if bstack11l11111l_opy_:
      bstack11l1ll111_opy_(bstack11l11111l_opy_)
    if bstack1lll11l11l_opy_:
      bstack111l1111l_opy_(bstack1lll11l11l_opy_)
    if bstack1ll1ll111l_opy_:
      bstack1l11llllll_opy_()
def bstack1l1ll11l11_opy_(self, test, *args, **kwargs):
  bstack11ll1l11l1_opy_ = None
  if test:
    bstack11ll1l11l1_opy_ = str(test.name)
  bstack1111llll1l_opy_(test, bstack11ll1l11l1_opy_)
  bstack11l11111ll_opy_(self, test, *args, **kwargs)
def bstack111l11l1_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1lll1111ll_opy_
  global CONFIG
  global bstack1ll11111l1_opy_
  global bstack1l1l111l11_opy_
  global bstack1l1l1lll1_opy_
  bstack1lll1ll11l_opy_ = None
  try:
    if bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ௃"), None) or bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ௄"), None):
      try:
        if not bstack1l1l111l11_opy_:
          bstack1lll11ll11_opy_ = os.path.join(os.path.expanduser(bstack1111_opy_ (u"ࠪࢂࠬ௅")), bstack1111_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫெ"), bstack1111_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧே"))
          with bstack1l1l1lll1_opy_:
            if os.path.exists(bstack1lll11ll11_opy_):
              with open(bstack1lll11ll11_opy_, bstack1111_opy_ (u"࠭ࡲࠨை")) as f:
                content = f.read().strip()
                if content:
                  bstack1111l1l1_opy_ = json.loads(bstack1111_opy_ (u"ࠢࡼࠤ௉") + content + bstack1111_opy_ (u"ࠨࠤࡻࠦ࠿ࠦࠢࡺࠤࠪொ") + bstack1111_opy_ (u"ࠤࢀࠦோ"))
                  bstack1l1l111l11_opy_ = bstack1111l1l1_opy_.get(str(threading.get_ident()))
      except Exception as e:
        logger.debug(bstack1111_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡵࡩࡦࡪࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡎࡊࡳࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢࡷࡩࡸࡺࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࠩௌ") + str(e))
      if bstack1ll11111l1_opy_:
        with bstack111l1l11l_opy_:
          bstack1l1ll11l1_opy_ = bstack1ll11111l1_opy_.copy()
        for driver in bstack1l1ll11l1_opy_:
          if bstack1l1l111l11_opy_ == driver.session_id:
            bstack1lll1ll11l_opy_ = driver
    bstack11l1ll1l_opy_ = bstack11l1111111_opy_.bstack111l1lll1_opy_(test.tags)
    if bstack1lll1ll11l_opy_:
      threading.current_thread().isA11yTest = bstack11l1111111_opy_.bstack11ll1llll1_opy_(bstack1lll1ll11l_opy_, bstack11l1ll1l_opy_)
      threading.current_thread().isAppA11yTest = bstack11l1111111_opy_.bstack11ll1llll1_opy_(bstack1lll1ll11l_opy_, bstack11l1ll1l_opy_)
    else:
      threading.current_thread().isA11yTest = bstack11l1ll1l_opy_
      threading.current_thread().isAppA11yTest = bstack11l1ll1l_opy_
  except:
    pass
  bstack1lll1111ll_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1ll1111ll_opy_
  try:
    bstack1ll1111ll_opy_ = self._test
  except:
    bstack1ll1111ll_opy_ = self.test
def bstack1l11l111l_opy_():
  global bstack1111l1l11_opy_
  try:
    if os.path.exists(bstack1111l1l11_opy_):
      os.remove(bstack1111l1l11_opy_)
  except Exception as e:
    logger.debug(bstack1111_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿்ࠦࠧ") + str(e))
def bstack1l11l1ll1_opy_():
  global bstack1111l1l11_opy_
  bstack1l1lll1l11_opy_ = {}
  lock_file = bstack1111l1l11_opy_ + bstack1111_opy_ (u"ࠬ࠴࡬ࡰࡥ࡮ࠫ௎")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1111_opy_ (u"࠭ࡦࡪ࡮ࡨࡰࡴࡩ࡫ࠡࡰࡲࡸࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥ࠭ࠢࡸࡷ࡮ࡴࡧࠡࡤࡤࡷ࡮ࡩࠠࡧ࡫࡯ࡩࠥࡵࡰࡦࡴࡤࡸ࡮ࡵ࡮ࡴࠩ௏"))
    try:
      if not os.path.isfile(bstack1111l1l11_opy_):
        with open(bstack1111l1l11_opy_, bstack1111_opy_ (u"ࠧࡸࠩௐ")) as f:
          json.dump({}, f)
      if os.path.exists(bstack1111l1l11_opy_):
        with open(bstack1111l1l11_opy_, bstack1111_opy_ (u"ࠨࡴࠪ௑")) as f:
          content = f.read().strip()
          if content:
            bstack1l1lll1l11_opy_ = json.loads(content)
    except Exception as e:
      logger.debug(bstack1111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡷ࡫ࡡࡥ࡫ࡱ࡫ࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫ௒") + str(e))
    return bstack1l1lll1l11_opy_
  try:
    os.makedirs(os.path.dirname(bstack1111l1l11_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      if not os.path.isfile(bstack1111l1l11_opy_):
        with open(bstack1111l1l11_opy_, bstack1111_opy_ (u"ࠪࡻࠬ௓")) as f:
          json.dump({}, f)
      if os.path.exists(bstack1111l1l11_opy_):
        with open(bstack1111l1l11_opy_, bstack1111_opy_ (u"ࠫࡷ࠭௔")) as f:
          content = f.read().strip()
          if content:
            bstack1l1lll1l11_opy_ = json.loads(content)
  except Exception as e:
    logger.debug(bstack1111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡳࡧࡤࡨ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧ௕") + str(e))
  finally:
    return bstack1l1lll1l11_opy_
def bstack1l1ll1l1l1_opy_(platform_index, item_index):
  global bstack1111l1l11_opy_
  lock_file = bstack1111l1l11_opy_ + bstack1111_opy_ (u"࠭࠮࡭ࡱࡦ࡯ࠬ௖")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1111_opy_ (u"ࠧࡧ࡫࡯ࡩࡱࡵࡣ࡬ࠢࡱࡳࡹࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦ࠮ࠣࡹࡸ࡯࡮ࡨࠢࡥࡥࡸ࡯ࡣࠡࡨ࡬ࡰࡪࠦ࡯ࡱࡧࡵࡥࡹ࡯࡯࡯ࡵࠪௗ"))
    try:
      bstack1l1lll1l11_opy_ = {}
      if os.path.exists(bstack1111l1l11_opy_):
        with open(bstack1111l1l11_opy_, bstack1111_opy_ (u"ࠨࡴࠪ௘")) as f:
          content = f.read().strip()
          if content:
            bstack1l1lll1l11_opy_ = json.loads(content)
      bstack1l1lll1l11_opy_[item_index] = platform_index
      with open(bstack1111l1l11_opy_, bstack1111_opy_ (u"ࠤࡺࠦ௙")) as outfile:
        json.dump(bstack1l1lll1l11_opy_, outfile)
    except Exception as e:
      logger.debug(bstack1111_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡽࡲࡪࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨ௚") + str(e))
    return
  try:
    os.makedirs(os.path.dirname(bstack1111l1l11_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      bstack1l1lll1l11_opy_ = {}
      if os.path.exists(bstack1111l1l11_opy_):
        with open(bstack1111l1l11_opy_, bstack1111_opy_ (u"ࠫࡷ࠭௛")) as f:
          content = f.read().strip()
          if content:
            bstack1l1lll1l11_opy_ = json.loads(content)
      bstack1l1lll1l11_opy_[item_index] = platform_index
      with open(bstack1111l1l11_opy_, bstack1111_opy_ (u"ࠧࡽࠢ௜")) as outfile:
        json.dump(bstack1l1lll1l11_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1111_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡹࡵ࡭ࡹ࡯࡮ࡨࠢࡷࡳࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫ௝") + str(e))
def bstack1l11ll1111_opy_(bstack1l11ll1l11_opy_):
  global CONFIG
  bstack1ll1111l1_opy_ = bstack1111_opy_ (u"ࠧࠨ௞")
  if not bstack1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ௟") in CONFIG:
    logger.info(bstack1111_opy_ (u"ࠩࡑࡳࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠡࡲࡤࡷࡸ࡫ࡤࠡࡷࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࠦࡲࡦࡲࡲࡶࡹࠦࡦࡰࡴࠣࡖࡴࡨ࡯ࡵࠢࡵࡹࡳ࠭௠"))
  try:
    platform = CONFIG[bstack1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭௡")][bstack1l11ll1l11_opy_]
    if bstack1111_opy_ (u"ࠫࡴࡹࠧ௢") in platform:
      bstack1ll1111l1_opy_ += str(platform[bstack1111_opy_ (u"ࠬࡵࡳࠨ௣")]) + bstack1111_opy_ (u"࠭ࠬࠡࠩ௤")
    if bstack1111_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪ௥") in platform:
      bstack1ll1111l1_opy_ += str(platform[bstack1111_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫ௦")]) + bstack1111_opy_ (u"ࠩ࠯ࠤࠬ௧")
    if bstack1111_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧ௨") in platform:
      bstack1ll1111l1_opy_ += str(platform[bstack1111_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨ௩")]) + bstack1111_opy_ (u"ࠬ࠲ࠠࠨ௪")
    if bstack1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ௫") in platform:
      bstack1ll1111l1_opy_ += str(platform[bstack1111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ௬")]) + bstack1111_opy_ (u"ࠨ࠮ࠣࠫ௭")
    if bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ௮") in platform:
      bstack1ll1111l1_opy_ += str(platform[bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ௯")]) + bstack1111_opy_ (u"ࠫ࠱ࠦࠧ௰")
    if bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭௱") in platform:
      bstack1ll1111l1_opy_ += str(platform[bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ௲")]) + bstack1111_opy_ (u"ࠧ࠭ࠢࠪ௳")
  except Exception as e:
    logger.debug(bstack1111_opy_ (u"ࠨࡕࡲࡱࡪࠦࡥࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡱ࡫ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡴࡶࡵ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡷ࡫ࡰࡰࡴࡷࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡵ࡮ࠨ௴") + str(e))
  finally:
    if bstack1ll1111l1_opy_[len(bstack1ll1111l1_opy_) - 2:] == bstack1111_opy_ (u"ࠩ࠯ࠤࠬ௵"):
      bstack1ll1111l1_opy_ = bstack1ll1111l1_opy_[:-2]
    return bstack1ll1111l1_opy_
def bstack1111llll11_opy_(path, bstack1ll1111l1_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1l1l1l11l_opy_ = ET.parse(path)
    bstack1l11111ll_opy_ = bstack1l1l1l11l_opy_.getroot()
    bstack1111lllll1_opy_ = None
    for suite in bstack1l11111ll_opy_.iter(bstack1111_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩ௶")):
      if bstack1111_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ௷") in suite.attrib:
        suite.attrib[bstack1111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ௸")] += bstack1111_opy_ (u"࠭ࠠࠨ௹") + bstack1ll1111l1_opy_
        bstack1111lllll1_opy_ = suite
    bstack11lll11111_opy_ = None
    for robot in bstack1l11111ll_opy_.iter(bstack1111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭௺")):
      bstack11lll11111_opy_ = robot
    bstack1l1ll1111l_opy_ = len(bstack11lll11111_opy_.findall(bstack1111_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧ௻")))
    if bstack1l1ll1111l_opy_ == 1:
      bstack11lll11111_opy_.remove(bstack11lll11111_opy_.findall(bstack1111_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨ௼"))[0])
      bstack1111111l_opy_ = ET.Element(bstack1111_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩ௽"), attrib={bstack1111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ௾"): bstack1111_opy_ (u"࡙ࠬࡵࡪࡶࡨࡷࠬ௿"), bstack1111_opy_ (u"࠭ࡩࡥࠩఀ"): bstack1111_opy_ (u"ࠧࡴ࠲ࠪఁ")})
      bstack11lll11111_opy_.insert(1, bstack1111111l_opy_)
      bstack11l1l1111_opy_ = None
      for suite in bstack11lll11111_opy_.iter(bstack1111_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧం")):
        bstack11l1l1111_opy_ = suite
      bstack11l1l1111_opy_.append(bstack1111lllll1_opy_)
      bstack1ll11l1l_opy_ = None
      for status in bstack1111lllll1_opy_.iter(bstack1111_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩః")):
        bstack1ll11l1l_opy_ = status
      bstack11l1l1111_opy_.append(bstack1ll11l1l_opy_)
    bstack1l1l1l11l_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1111_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡳࡵ࡬ࡲ࡬ࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠨఄ") + str(e))
def bstack11llll1l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1l1ll1ll_opy_
  global CONFIG
  if bstack1111_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡴࡦࡺࡨࠣఅ") in options:
    del options[bstack1111_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡵࡧࡴࡩࠤఆ")]
  bstack1ll1ll1lll_opy_ = bstack1l11l1ll1_opy_()
  for item_id in bstack1ll1ll1lll_opy_.keys():
    path = os.path.join(outs_dir, str(item_id), bstack1111_opy_ (u"࠭࡯ࡶࡶࡳࡹࡹ࠴ࡸ࡮࡮ࠪఇ"))
    bstack1111llll11_opy_(path, bstack1l11ll1111_opy_(bstack1ll1ll1lll_opy_[item_id]))
  bstack1l11l111l_opy_()
  return bstack1l1ll1ll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack11l11l1l11_opy_(self, ff_profile_dir):
  global bstack1lll11lll_opy_
  if not ff_profile_dir:
    return None
  return bstack1lll11lll_opy_(self, ff_profile_dir)
def bstack11ll111l11_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack111lllll1l_opy_
  bstack11ll1lll1_opy_ = []
  if bstack1111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪఈ") in CONFIG:
    bstack11ll1lll1_opy_ = CONFIG[bstack1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫఉ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1111_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࠥఊ")],
      pabot_args[bstack1111_opy_ (u"ࠥࡺࡪࡸࡢࡰࡵࡨࠦఋ")],
      argfile,
      pabot_args.get(bstack1111_opy_ (u"ࠦ࡭࡯ࡶࡦࠤఌ")),
      pabot_args[bstack1111_opy_ (u"ࠧࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠣ఍")],
      platform[0],
      bstack111lllll1l_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1111_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡧ࡫࡯ࡩࡸࠨఎ")] or [(bstack1111_opy_ (u"ࠢࠣఏ"), None)]
    for platform in enumerate(bstack11ll1lll1_opy_)
  ]
def bstack1l11l1l111_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack11l1l1l1l1_opy_=bstack1111_opy_ (u"ࠨࠩఐ")):
  global bstack11ll1lll1l_opy_
  self.platform_index = platform_index
  self.bstack1l1llllll_opy_ = bstack11l1l1l1l1_opy_
  bstack11ll1lll1l_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack11111l11l_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1llllll111_opy_
  global bstack1ll1l11l1_opy_
  bstack1l11l11l1l_opy_ = copy.deepcopy(item)
  if not bstack1111_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ఑") in item.options:
    bstack1l11l11l1l_opy_.options[bstack1111_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬఒ")] = []
  bstack1ll1l1ll1_opy_ = bstack1l11l11l1l_opy_.options[bstack1111_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ఓ")].copy()
  for v in bstack1l11l11l1l_opy_.options[bstack1111_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧఔ")]:
    if bstack1111_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬక") in v:
      bstack1ll1l1ll1_opy_.remove(v)
    if bstack1111_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙ࠧఖ") in v:
      bstack1ll1l1ll1_opy_.remove(v)
    if bstack1111_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡅࡇࡉࡐࡔࡉࡁࡍࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬగ") in v:
      bstack1ll1l1ll1_opy_.remove(v)
  bstack1ll1l1ll1_opy_.insert(0, bstack1111_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘ࠻ࡽࢀࠫఘ").format(bstack1l11l11l1l_opy_.platform_index))
  bstack1ll1l1ll1_opy_.insert(0, bstack1111_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡇࡉࡋࡒࡏࡄࡃࡏࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘ࠺ࡼࡿࠪఙ").format(bstack1l11l11l1l_opy_.bstack1l1llllll_opy_))
  bstack1l11l11l1l_opy_.options[bstack1111_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭చ")] = bstack1ll1l1ll1_opy_
  if bstack1ll1l11l1_opy_:
    bstack1l11l11l1l_opy_.options[bstack1111_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧఛ")].insert(0, bstack1111_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘࡀࡻࡾࠩజ").format(bstack1ll1l11l1_opy_))
  return bstack1llllll111_opy_(caller_id, datasources, is_last, bstack1l11l11l1l_opy_, outs_dir)
def bstack1llll1111l_opy_(command, item_index):
  try:
    if global_config.get_property(bstack1111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨఝ")):
      os.environ[bstack1111_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩఞ")] = json.dumps(CONFIG[bstack1111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬట")][item_index % bstack11llllll_opy_])
    global bstack1ll1l11l1_opy_
    os.environ[bstack1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪఠ")] = str(item_index % bstack11llllll_opy_)
    listener_arg = bstack1111_opy_ (u"ࠫࠬడ")
    if is_robot_playwright_installed() and cli.is_enabled(CONFIG):
      listener_arg = bstack1111_opy_ (u"ࠬࠦ࠭࠮࡮࡬ࡷࡹ࡫࡮ࡦࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡨࡰ࠴ࡲࡰࡤࡲࡸࡤࡲࡩࡴࡶࡨࡲࡪࡸ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠲ࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡑࡣࡷࡧ࡭࡫ࡲࠨఢ")
      logger.debug(bstack1111_opy_ (u"ࠨࡁࡥࡦ࡬ࡲ࡬ࠦࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡓࡥࡹࡩࡨࡦࡴࠣࡰ࡮ࡹࡴࡦࡰࡨࡶࠥ࡬࡯ࡳࠢ࡬ࡸࡪࡳࠠࡼࡿࠥణ").format(item_index))
    bstack1l1l111ll_opy_ = bstack1111_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡳࡥ࡭ࠣࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠤ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࠠࠣత") + \
              str(item_index % bstack11llllll_opy_) + \
              bstack1111_opy_ (u"ࠣࠢ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠡࠤథ") + \
              str(item_index) + \
              listener_arg
    if bstack1ll1l11l1_opy_:
        bstack1l1l111ll_opy_ += bstack1111_opy_ (u"ࠤࠣࠦద") + bstack1ll1l11l1_opy_
    command[0:1] = bstack1l1l111ll_opy_.split()
  except Exception as e:
    logger.error(bstack1111_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡰࡳࡩ࡯ࡦࡺ࡫ࡱ࡫ࠥࡩ࡯࡮࡯ࡤࡲࡩࠦࡦࡰࡴࠣࡴࡦࡨ࡯ࡵࠢࡵࡹࡳࡀࠠࡼࡿࠪధ").format(str(e)))
def bstack1l1lllll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1l11lll1ll_opy_
  try:
    bstack1llll1111l_opy_(command, item_index)
    return bstack1l11lll1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
  except Exception as e:
    logger.error(bstack1111_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡢࡤࡲࡸࠥࡸࡵ࡯࠼ࠣࡿࢂ࠭న").format(str(e)))
    raise e
def bstack1l1ll11l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1l11lll1ll_opy_
  try:
    bstack1llll1111l_opy_(command, item_index)
    return bstack1l11lll1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
  except Exception as e:
    logger.error(bstack1111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡥࡳࡹࠦࡲࡶࡰࠣ࠶࠳࠷࠳࠻ࠢࡾࢁࠬ఩").format(str(e)))
    try:
      return bstack1l11lll1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
    except Exception as e2:
      logger.error(bstack1111_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠ࠳࠰࠴࠷ࠥ࡬ࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࡽࢀࠫప").format(str(e2)))
      raise e
def bstack1111ll111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1l11lll1ll_opy_
  try:
    bstack1llll1111l_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    return bstack1l11lll1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
  except Exception as e:
    logger.error(bstack1111_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡧࡵࡴࠡࡴࡸࡲࠥ࠸࠮࠲࠷࠽ࠤࢀࢃࠧఫ").format(str(e)))
    try:
      return bstack1l11lll1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
    except Exception as e2:
      logger.error(bstack1111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡦࡨ࡯ࡵࠢ࠵࠲࠶࠻ࠠࡧࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣࡿࢂ࠭బ").format(str(e2)))
      raise e
def _11l111l1l1_opy_(bstack1llll111l_opy_, item_index, process_timeout, sleep_before_start, bstack1ll1lll11l_opy_):
  bstack1llll1111l_opy_(bstack1llll111l_opy_, item_index)
  if process_timeout is None:
    process_timeout = 3600
  if sleep_before_start and sleep_before_start > 0:
    time.sleep(min(sleep_before_start, 5))
  return process_timeout
def bstack11ll111l1l_opy_(command, bstack1111l1ll_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack1l11lll1ll_opy_
  global bstack1llll11ll_opy_
  global bstack1ll1l11l1_opy_
  try:
    for env_name, bstack1llll1lll_opy_ in bstack1llll11ll_opy_.items():
      os.environ[env_name] = bstack1llll1lll_opy_
    bstack1ll1l11l1_opy_ = bstack1111_opy_ (u"ࠤࠥభ")
    bstack1llll1111l_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    if sleep_before_start and sleep_before_start > 0:
      time.sleep(min(sleep_before_start, 5))
    return bstack1l11lll1ll_opy_(command, bstack1111l1ll_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack1111_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡣࡱࡷࠤࡷࡻ࡮ࠡ࠷࠱࠴࠿ࠦࡻࡾࠩమ").format(str(e)))
    try:
      return bstack1l11lll1ll_opy_(command, bstack1111l1ll_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack1111_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡢࡤࡲࡸࠥ࡬ࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࡽࢀࠫయ").format(str(e2)))
      raise e
def bstack1llll1llll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack1l11lll1ll_opy_
  try:
    process_timeout = _11l111l1l1_opy_(command, item_index, process_timeout, sleep_before_start, bstack1111_opy_ (u"ࠬ࠺࠮࠳ࠩర"))
    return bstack1l11lll1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack1111_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠࡳࡷࡱࠤ࠹࠴࠲࠻ࠢࡾࢁࠬఱ").format(str(e)))
    try:
      return bstack1l11lll1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack1111_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡧࡵࡴࠡࡨࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࢀࢃࠧల").format(str(e2)))
      raise e
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack11l1l1llll_opy_(self, runner, quiet=False, capture=True):
  global bstack1l11l1ll11_opy_
  bstack1lll1llll1_opy_ = bstack1l11l1ll11_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack1111_opy_ (u"ࠨࡧࡻࡧࡪࡶࡴࡪࡱࡱࡣࡦࡸࡲࠨళ")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1111_opy_ (u"ࠩࡨࡼࡨࡥࡴࡳࡣࡦࡩࡧࡧࡣ࡬ࡡࡤࡶࡷ࠭ఴ")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1lll1llll1_opy_
def bstack1l11l111l1_opy_(runner, hook_name, context, element, bstack11l11ll1l_opy_, *args):
  global bstack1ll1l1l11_opy_
  try:
    if runner.hooks.get(hook_name):
      bstack11111lll_opy_.bstack11l1ll1l1_opy_(hook_name, element)
    if bstack1ll1l1l11_opy_ is None or bstack1ll1l1l11_opy_:
      bstack11l11ll1l_opy_(runner, hook_name, context, *args)
    else:
      bstack1ll11l111_opy_ = (context,) + args
      bstack11l11ll1l_opy_(runner, hook_name, *bstack1ll11l111_opy_)
    if runner.hooks.get(hook_name):
      bstack11111lll_opy_.bstack1l1l11llll_opy_(element)
      if hook_name not in [bstack1111_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠧవ"), bstack1111_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡥࡱࡲࠧశ")] and args and hasattr(args[0], bstack1111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡣࡲ࡫ࡳࡴࡣࡪࡩࠬష")):
        args[0].error_message = bstack1111_opy_ (u"࠭ࠧస")
  except Exception as e:
    logger.debug(bstack1111_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣ࡬ࡦࡴࡤ࡭ࡧࠣ࡬ࡴࡵ࡫ࡴࠢ࡬ࡲࠥࡨࡥࡩࡣࡹࡩ࠿ࠦࡻࡾࠩహ").format(str(e)))
@measure(event_name=EVENTS.bstack1ll1l1lll_opy_, stage=STAGE.bstack111l1lllll_opy_, hook_type=bstack1111_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡂ࡮࡯ࠦ఺"), bstack11ll1l11l1_opy_=bstack1lll11ll1_opy_)
def bstack11lllll11l_opy_(runner, name, context, bstack11l11ll1l_opy_, *args):
    if runner.hooks.get(bstack1111_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨ఻")).__name__ != bstack1111_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲ࡟ࡥࡧࡩࡥࡺࡲࡴࡠࡪࡲࡳࡰࠨ఼"):
      bstack1l11l111l1_opy_(runner, name, context, runner, bstack11l11ll1l_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack1l111l111l_opy_(bstack1111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪఽ")) else context.browser
      runner.driver_initialised = bstack1111_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤా")
    except Exception as e:
      logger.debug(bstack1111_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡤࡳ࡫ࡹࡩࡷࠦࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡧࠣࡥࡹࡺࡲࡪࡤࡸࡸࡪࡀࠠࡼࡿࠪి").format(str(e)))
def bstack1lll1l1l11_opy_(runner, name, context, bstack11l11ll1l_opy_, *args):
    bstack1l11l111l1_opy_(runner, name, context, context.feature, bstack11l11ll1l_opy_, *args)
    try:
      if not bstack1ll1llll1_opy_:
        bstack1lll1ll11l_opy_ = threading.current_thread().bstackSessionDriver if bstack1l111l111l_opy_(bstack1111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ీ")) else context.browser
        if is_driver_active(bstack1lll1ll11l_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack1111_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠤు")
          bstack11ll1ll1l_opy_ = str(runner.feature.name)
          bstack1lllll1lll_opy_(context, bstack11ll1ll1l_opy_)
          bstack1lll1ll11l_opy_.execute_script(bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧూ") + json.dumps(bstack11ll1ll1l_opy_) + bstack1111_opy_ (u"ࠪࢁࢂ࠭ృ"))
    except Exception as e:
      logger.debug(bstack1111_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣ࡭ࡳࠦࡢࡦࡨࡲࡶࡪࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫౄ").format(str(e)))
def bstack1lll1l11_opy_(runner, name, context, bstack11l11ll1l_opy_, *args):
    target = context.scenario if hasattr(context, bstack1111_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧ౅")) else context.feature
    bstack1l11l111l1_opy_(runner, name, context, target, bstack11l11ll1l_opy_, *args)
@measure(event_name=EVENTS.bstack1l1111l1ll_opy_, stage=STAGE.bstack111l1lllll_opy_, bstack11ll1l11l1_opy_=bstack1lll11ll1_opy_)
def bstack1llll111ll_opy_(runner, name, context, bstack11l11ll1l_opy_, *args):
    bstack11111lll_opy_.start_test(context)
    bstack1l11l111l1_opy_(runner, name, context, context.scenario, bstack11l11ll1l_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack1ll1ll11l1_opy_.bstack11ll1lll_opy_(context, *args)
    try:
      bstack1lll1ll11l_opy_ = bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬె"), context.browser)
      if is_driver_active(bstack1lll1ll11l_opy_):
        TestHubHandler.bstack1l11l1l11l_opy_(bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ే"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack1111_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥై")
        if (not bstack1ll1llll1_opy_):
          scenario_name = args[0].name
          feature_name = bstack11ll1ll1l_opy_ = str(runner.feature.name)
          bstack11ll1ll1l_opy_ = feature_name + bstack1111_opy_ (u"ࠩࠣ࠱ࠥ࠭౉") + scenario_name
          if runner.driver_initialised == bstack1111_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧొ"):
            bstack1lllll1lll_opy_(context, bstack11ll1ll1l_opy_)
            bstack1lll1ll11l_opy_.execute_script(bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩో") + json.dumps(bstack11ll1ll1l_opy_) + bstack1111_opy_ (u"ࠬࢃࡽࠨౌ"))
    except Exception as e:
      logger.debug(bstack1111_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱ࠽ࠤࢀࢃ్ࠧ").format(str(e)))
@measure(event_name=EVENTS.bstack1ll1l1lll_opy_, stage=STAGE.bstack111l1lllll_opy_, hook_type=bstack1111_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࡓࡵࡧࡳࠦ౎"), bstack11ll1l11l1_opy_=bstack1lll11ll1_opy_)
def bstack111llll111_opy_(runner, name, context, bstack11l11ll1l_opy_, *args):
    bstack1l11l111l1_opy_(runner, name, context, args[0], bstack11l11ll1l_opy_, *args)
    try:
      bstack1lll1ll11l_opy_ = threading.current_thread().bstackSessionDriver if bstack1l111l111l_opy_(bstack1111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ౏")) else context.browser
      if is_driver_active(bstack1lll1ll11l_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack1111_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢ౐")
        bstack11111lll_opy_.bstack11ll1l1l11_opy_(args[0])
        if runner.driver_initialised == bstack1111_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣ౑"):
          feature_name = bstack11ll1ll1l_opy_ = str(runner.feature.name)
          bstack11ll1ll1l_opy_ = feature_name + bstack1111_opy_ (u"ࠫࠥ࠳ࠠࠨ౒") + context.scenario.name
          bstack1lll1ll11l_opy_.execute_script(bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ౓") + json.dumps(bstack11ll1ll1l_opy_) + bstack1111_opy_ (u"࠭ࡽࡾࠩ౔"))
    except Exception as e:
      logger.debug(bstack1111_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡸࡪࡶ࠺ࠡࡽࢀౕࠫ").format(str(e)))
@measure(event_name=EVENTS.bstack1ll1l1lll_opy_, stage=STAGE.bstack111l1lllll_opy_, hook_type=bstack1111_opy_ (u"ࠣࡣࡩࡸࡪࡸࡓࡵࡧࡳౖࠦ"), bstack11ll1l11l1_opy_=bstack1lll11ll1_opy_)
def bstack1lllll1ll1_opy_(runner, name, context, bstack11l11ll1l_opy_, *args):
  bstack11111lll_opy_.bstack1l1l1lll_opy_(args[0])
  try:
    step_status = args[0].status.name
    bstack1lll1ll11l_opy_ = threading.current_thread().bstackSessionDriver if bstack1111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ౗") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack1lll1ll11l_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack1111_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪౘ")
        feature_name = bstack11ll1ll1l_opy_ = str(runner.feature.name)
        bstack11ll1ll1l_opy_ = feature_name + bstack1111_opy_ (u"ࠫࠥ࠳ࠠࠨౙ") + context.scenario.name
        bstack1lll1ll11l_opy_.execute_script(bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪౚ") + json.dumps(bstack11ll1ll1l_opy_) + bstack1111_opy_ (u"࠭ࡽࡾࠩ౛"))
    if str(step_status).lower() in [bstack1111_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ౜"), bstack1111_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧౝ")]:
      bstack1lll1lll_opy_ = bstack1111_opy_ (u"ࠩࠪ౞")
      bstack111l11ll1l_opy_ = bstack1111_opy_ (u"ࠪࠫ౟")
      bstack1111111l1_opy_ = bstack1111_opy_ (u"ࠫࠬౠ")
      try:
        import traceback
        bstack1lll1lll_opy_ = runner.exception.__class__.__name__
        bstack1l111ll1ll_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack111l11ll1l_opy_ = bstack1111_opy_ (u"ࠬࠦࠧౡ").join(bstack1l111ll1ll_opy_)
        bstack1111111l1_opy_ = bstack1l111ll1ll_opy_[-1]
      except Exception as e:
        logger.debug(bstack111lllll_opy_.format(str(e)))
      bstack1lll1lll_opy_ += bstack1111111l1_opy_
      bstack1l1111ll1l_opy_(context, json.dumps(str(args[0].name) + bstack1111_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧౢ") + str(bstack111l11ll1l_opy_)),
                          bstack1111_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨౣ"))
      if runner.driver_initialised == bstack1111_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨ౤"):
        bstack11lllll111_opy_(getattr(context, bstack1111_opy_ (u"ࠩࡳࡥ࡬࡫ࠧ౥"), None), bstack1111_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ౦"), bstack1lll1lll_opy_)
        bstack1lll1ll11l_opy_.execute_script(bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ౧") + json.dumps(str(args[0].name) + bstack1111_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦ౨") + str(bstack111l11ll1l_opy_)) + bstack1111_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥࢁࢂ࠭౩"))
      if runner.driver_initialised == bstack1111_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧ౪"):
        bstack1l1lllll1l_opy_(bstack1lll1ll11l_opy_, bstack1111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ౫"), bstack1111_opy_ (u"ࠤࡖࡧࡪࡴࡡࡳ࡫ࡲࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨ౬") + str(bstack1lll1lll_opy_))
    else:
      bstack1l1111ll1l_opy_(context, bstack1111_opy_ (u"ࠥࡔࡦࡹࡳࡦࡦࠤࠦ౭"), bstack1111_opy_ (u"ࠦ࡮ࡴࡦࡰࠤ౮"))
      if runner.driver_initialised == bstack1111_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥ౯"):
        bstack11lllll111_opy_(getattr(context, bstack1111_opy_ (u"࠭ࡰࡢࡩࡨࠫ౰"), None), bstack1111_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ౱"))
      bstack1lll1ll11l_opy_.execute_script(bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭౲") + json.dumps(str(args[0].name) + bstack1111_opy_ (u"ࠤࠣ࠱ࠥࡖࡡࡴࡵࡨࡨࠦࠨ౳")) + bstack1111_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩ౴"))
      if runner.driver_initialised == bstack1111_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤ౵"):
        bstack1l1lllll1l_opy_(bstack1lll1ll11l_opy_, bstack1111_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ౶"))
  except Exception as e:
    logger.debug(bstack1111_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࠣࡷࡹ࡫ࡰ࠻ࠢࡾࢁࠬ౷").format(str(e)))
  bstack1l11l111l1_opy_(runner, name, context, args[0], bstack11l11ll1l_opy_, *args)
@measure(event_name=EVENTS.bstack1l1lll1111_opy_, stage=STAGE.bstack111l1lllll_opy_, bstack11ll1l11l1_opy_=bstack1lll11ll1_opy_)
def bstack11llll111l_opy_(runner, name, context, bstack11l11ll1l_opy_, *args):
  bstack11111lll_opy_.end_test(args[0])
  try:
    bstack1ll1ll1l1l_opy_ = args[0].status.name
    bstack1lll1ll11l_opy_ = bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭౸"), context.browser)
    bstack1ll1ll11l1_opy_.bstack1l1lll1l_opy_(bstack1lll1ll11l_opy_)
    if str(bstack1ll1ll1l1l_opy_).lower() in [bstack1111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ౹"), bstack1111_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ౺")]:
      bstack1lll1lll_opy_ = bstack1111_opy_ (u"ࠪࠫ౻")
      bstack111l11ll1l_opy_ = bstack1111_opy_ (u"ࠫࠬ౼")
      bstack1111111l1_opy_ = bstack1111_opy_ (u"ࠬ࠭౽")
      try:
        import traceback
        bstack1lll1lll_opy_ = runner.exception.__class__.__name__
        bstack1l111ll1ll_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack111l11ll1l_opy_ = bstack1111_opy_ (u"࠭ࠠࠨ౾").join(bstack1l111ll1ll_opy_)
        bstack1111111l1_opy_ = bstack1l111ll1ll_opy_[-1]
      except Exception as e:
        logger.debug(bstack111lllll_opy_.format(str(e)))
      bstack1lll1lll_opy_ += bstack1111111l1_opy_
      bstack1l1111ll1l_opy_(context, json.dumps(str(args[0].name) + bstack1111_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨ౿") + str(bstack111l11ll1l_opy_)),
                          bstack1111_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢಀ"))
      if runner.driver_initialised == bstack1111_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦಁ") or runner.driver_initialised == bstack1111_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪಂ"):
        bstack11lllll111_opy_(getattr(context, bstack1111_opy_ (u"ࠫࡵࡧࡧࡦࠩಃ"), None), bstack1111_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ಄"), bstack1lll1lll_opy_)
        bstack1lll1ll11l_opy_.execute_script(bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫಅ") + json.dumps(str(args[0].name) + bstack1111_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨಆ") + str(bstack111l11ll1l_opy_)) + bstack1111_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨಇ"))
      if runner.driver_initialised == bstack1111_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦಈ") or runner.driver_initialised == bstack1111_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪಉ"):
        bstack1l1lllll1l_opy_(bstack1lll1ll11l_opy_, bstack1111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫಊ"), bstack1111_opy_ (u"࡙ࠧࡣࡦࡰࡤࡶ࡮ࡵࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤಋ") + str(bstack1lll1lll_opy_))
    else:
      bstack1l1111ll1l_opy_(context, bstack1111_opy_ (u"ࠨࡐࡢࡵࡶࡩࡩࠧࠢಌ"), bstack1111_opy_ (u"ࠢࡪࡰࡩࡳࠧ಍"))
      if runner.driver_initialised == bstack1111_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥಎ") or runner.driver_initialised == bstack1111_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩಏ"):
        bstack11lllll111_opy_(getattr(context, bstack1111_opy_ (u"ࠪࡴࡦ࡭ࡥࠨಐ"), None), bstack1111_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ಑"))
      bstack1lll1ll11l_opy_.execute_script(bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪಒ") + json.dumps(str(args[0].name) + bstack1111_opy_ (u"ࠨࠠ࠮ࠢࡓࡥࡸࡹࡥࡥࠣࠥಓ")) + bstack1111_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥࢁࢂ࠭ಔ"))
      if runner.driver_initialised == bstack1111_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥಕ") or runner.driver_initialised == bstack1111_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩಖ"):
        bstack1l1lllll1l_opy_(bstack1lll1ll11l_opy_, bstack1111_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥಗ"))
  except Exception as e:
    logger.debug(bstack1111_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭ಘ").format(str(e)))
  bstack1l11l111l1_opy_(runner, name, context, context.scenario, bstack11l11ll1l_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack111l1111l1_opy_(runner, name, context, bstack11l11ll1l_opy_, *args):
    target = context.scenario if hasattr(context, bstack1111_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧಙ")) else context.feature
    bstack1l11l111l1_opy_(runner, name, context, target, bstack11l11ll1l_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack111llll1ll_opy_(runner, name, context, bstack11l11ll1l_opy_, *args):
    try:
      bstack1lll1ll11l_opy_ = bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬಚ"), context.browser)
      bstack111ll11l_opy_ = bstack1111_opy_ (u"ࠧࠨಛ")
      if context.failed is True:
        bstack1ll1l1111_opy_ = []
        bstack11l1llll1_opy_ = []
        bstack1l1l111ll1_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack1ll1l1111_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1l111ll1ll_opy_ = traceback.format_tb(exc_tb)
            bstack1ll111ll11_opy_ = bstack1111_opy_ (u"ࠨࠢࠪಜ").join(bstack1l111ll1ll_opy_)
            bstack11l1llll1_opy_.append(bstack1ll111ll11_opy_)
            bstack1l1l111ll1_opy_.append(bstack1l111ll1ll_opy_[-1])
        except Exception as e:
          logger.debug(bstack111lllll_opy_.format(str(e)))
        bstack1lll1lll_opy_ = bstack1111_opy_ (u"ࠩࠪಝ")
        for i in range(len(bstack1ll1l1111_opy_)):
          bstack1lll1lll_opy_ += bstack1ll1l1111_opy_[i] + bstack1l1l111ll1_opy_[i] + bstack1111_opy_ (u"ࠪࡠࡳ࠭ಞ")
        bstack111ll11l_opy_ = bstack1111_opy_ (u"ࠫࠥ࠭ಟ").join(bstack11l1llll1_opy_)
        if runner.driver_initialised in [bstack1111_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨಠ"), bstack1111_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥಡ")]:
          bstack1l1111ll1l_opy_(context, bstack111ll11l_opy_, bstack1111_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨಢ"))
          bstack11lllll111_opy_(getattr(context, bstack1111_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭ಣ"), None), bstack1111_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤತ"), bstack1lll1lll_opy_)
          bstack1lll1ll11l_opy_.execute_script(bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨಥ") + json.dumps(bstack111ll11l_opy_) + bstack1111_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣࡿࢀࠫದ"))
          bstack1l1lllll1l_opy_(bstack1lll1ll11l_opy_, bstack1111_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧಧ"), bstack1111_opy_ (u"ࠨࡓࡰ࡯ࡨࠤࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡹࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡ࡞ࡱࠦನ") + str(bstack1lll1lll_opy_))
          bstack11llllll1_opy_ = bstack1l11ll111_opy_(bstack111ll11l_opy_, runner.feature.name, logger)
          if (bstack11llllll1_opy_ != None):
            bstack1lll111lll_opy_.append(bstack11llllll1_opy_)
      else:
        if runner.driver_initialised in [bstack1111_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣ಩"), bstack1111_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧಪ")]:
          bstack1l1111ll1l_opy_(context, bstack1111_opy_ (u"ࠤࡉࡩࡦࡺࡵࡳࡧ࠽ࠤࠧಫ") + str(runner.feature.name) + bstack1111_opy_ (u"ࠥࠤࡵࡧࡳࡴࡧࡧࠥࠧಬ"), bstack1111_opy_ (u"ࠦ࡮ࡴࡦࡰࠤಭ"))
          bstack11lllll111_opy_(getattr(context, bstack1111_opy_ (u"ࠬࡶࡡࡨࡧࠪಮ"), None), bstack1111_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨಯ"))
          bstack1lll1ll11l_opy_.execute_script(bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬರ") + json.dumps(bstack1111_opy_ (u"ࠣࡈࡨࡥࡹࡻࡲࡦ࠼ࠣࠦಱ") + str(runner.feature.name) + bstack1111_opy_ (u"ࠤࠣࡴࡦࡹࡳࡦࡦࠤࠦಲ")) + bstack1111_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩಳ"))
          bstack1l1lllll1l_opy_(bstack1lll1ll11l_opy_, bstack1111_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ಴"))
          bstack11llllll1_opy_ = bstack1l11ll111_opy_(bstack111ll11l_opy_, runner.feature.name, logger)
          if (bstack11llllll1_opy_ != None):
            bstack1lll111lll_opy_.append(bstack11llllll1_opy_)
    except Exception as e:
      logger.debug(bstack1111_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧವ").format(str(e)))
    bstack1l11l111l1_opy_(runner, name, context, context.feature, bstack11l11ll1l_opy_, *args)
@measure(event_name=EVENTS.bstack1ll1l1lll_opy_, stage=STAGE.bstack111l1lllll_opy_, hook_type=bstack1111_opy_ (u"ࠨࡡࡧࡶࡨࡶࡆࡲ࡬ࠣಶ"), bstack11ll1l11l1_opy_=bstack1lll11ll1_opy_)
def bstack1lll1ll1l1_opy_(runner, name, context, bstack11l11ll1l_opy_, *args):
    bstack1l11l111l1_opy_(runner, name, context, runner, bstack11l11ll1l_opy_, *args)
def bstack111l1111_opy_(self, filename=None):
  bstack1111_opy_ (u"ࠢࠣࠤࠍࠤࠥࡒ࡯ࡢࡦࠣ࡬ࡴࡵ࡫ࡴࠢࡤࡲࡩࠦࡥ࡯ࡵࡸࡶࡪࠦࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯࠰ࡣࡩࡸࡪࡸ࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠢࡤࡶࡪࠦࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡦࡦ࠱ࠎࠥࠦࡂࡦࡪࡤࡺࡪࠦࡶ࠲࠰࠶࠯ࠥࡪ࡯ࡦࡵࡱࠫࡹࠦࡣࡢ࡮࡯ࠤࡷࡻ࡮ࠡࡪࡲࡳࡰࡹࠠࡵࡪࡤࡸࠥࡧࡲࡦࡰࠪࡸࠥࡪࡥࡧ࡫ࡱࡩࡩ࠲ࠠࡴࡱࠣࡻࡪࠦ࡭ࡶࡵࡷࠎࠥࠦࡤࡰࠢࡷ࡬࡮ࡹࠠࡦࡺࡳࡰ࡮ࡩࡩࡵ࡮ࡼࠤࡹࡵࠠ࡮ࡣ࡮ࡩࠥࡹࡵࡳࡧࠣࡻࡪ࠭ࡲࡦࠢࡦࡥࡱࡲࡥࡥࠢ࡬ࡲࠥࡧ࡮ࡺࠢࡦࡥࡸ࡫࠮ࠋࠢࠣࠦࠧࠨಷ")
  global bstack1ll1l111ll_opy_
  bstack1ll1l111ll_opy_(self, filename)
  bstack1lllll111l_opy_ = []
  bstack1l111lll1l_opy_ = [bstack1111_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠩಸ"), bstack1111_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡷࡥ࡬࠭ಹ"), bstack1111_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ಺"), bstack1111_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ಻"), bstack1111_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡹࡧࡧࠨ಼"), bstack1111_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ಽ")]
  bstack1l1l11ll1_opy_ = lambda *_: None
  for hook_name in bstack1l111lll1l_opy_:
    if hook_name not in self.hooks:
      self.hooks[hook_name] = bstack1l1l11ll1_opy_
      bstack1lllll111l_opy_.append(hook_name)
  if bstack1lllll111l_opy_:
    os.environ[bstack1111_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡔࡆࡎࡣࡉࡋࡆࡂࡗࡏࡘࡤࡎࡏࡐࡍࡖࠫಾ")] = bstack1111_opy_ (u"ࠨ࠮ࠪಿ").join(bstack1lllll111l_opy_)
def bstack1l1llll1ll_opy_(self, name, *args):
  global bstack11l11ll1l_opy_
  global bstack1ll1l1l11_opy_
  try:
    if bstack1111ll1l_opy_:
      platform_index = int(threading.current_thread()._name) % bstack11llllll_opy_
      bstack11llll1111_opy_ = CONFIG[bstack1111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬೀ")][platform_index]
      os.environ[bstack1111_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫು")] = json.dumps(bstack11llll1111_opy_)
    if not hasattr(self, bstack1111_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡥࡥࠩೂ")):
      self.driver_initialised = None
    bstack1lll1l1111_opy_ = {
        bstack1111_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠩೃ"): bstack11lllll11l_opy_,
        bstack1111_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠧೄ"): bstack1lll1l1l11_opy_,
        bstack1111_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡵࡣࡪࠫ೅"): bstack1lll1l11_opy_,
        bstack1111_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪೆ"): bstack1llll111ll_opy_,
        bstack1111_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠧೇ"): bstack111llll111_opy_,
        bstack1111_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡸࡪࡶࠧೈ"): bstack1lllll1ll1_opy_,
        bstack1111_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ೉"): bstack11llll111l_opy_,
        bstack1111_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡹࡧࡧࠨೊ"): bstack111l1111l1_opy_,
        bstack1111_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ೋ"): bstack111llll1ll_opy_,
        bstack1111_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪೌ"): bstack1lll1ll1l1_opy_
    }
    handler = bstack1lll1l1111_opy_.get(name, bstack11l11ll1l_opy_)
    try:
      if args:
        context = args[0]
        remaining_args = args[1:]
        if bstack1ll1l1l11_opy_ is None or not bstack1ll1l1l11_opy_:
          context = self.context
          remaining_args = args
      else:
        context = self.context
        remaining_args = ()
      handler(self, name, context, bstack11l11ll1l_opy_, *remaining_args)
    except Exception as e:
      logger.debug(bstack1111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡦࡪ࡮ࡡࡷࡧࠣ࡬ࡴࡵ࡫ࠡࡪࡤࡲࡩࡲࡥࡳࠢࡾࢁ࠿ࠦࡻࡾ್ࠩ").format(name, str(e)))
    if name in [bstack1111_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠩ೎"), bstack1111_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ೏"), bstack1111_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡥࡱࡲࠧ೐")]:
      try:
        bstack1lll1ll11l_opy_ = threading.current_thread().bstackSessionDriver if bstack1l111l111l_opy_(bstack1111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ೑")) else context.browser
        bstack1l111111l_opy_ = (
          (name == bstack1111_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠩ೒") and self.driver_initialised == bstack1111_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦ೓")) or
          (name == bstack1111_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨ೔") and self.driver_initialised == bstack1111_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠥೕ")) or
          (name == bstack1111_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫೖ") and self.driver_initialised in [bstack1111_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨ೗"), bstack1111_opy_ (u"ࠧ࡯࡮ࡴࡶࡨࡴࠧ೘")]) or
          (name == bstack1111_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡴࡦࡲࠪ೙") and self.driver_initialised == bstack1111_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧ೚"))
        )
        if bstack1l111111l_opy_:
          self.driver_initialised = None
          if bstack1lll1ll11l_opy_ and hasattr(bstack1lll1ll11l_opy_, bstack1111_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠬ೛")):
            try:
              bstack1lll1ll11l_opy_.quit()
            except Exception as e:
              logger.debug(bstack1111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡳࡸ࡭ࡹࡺࡩ࡯ࡩࠣࡨࡷ࡯ࡶࡦࡴࠣ࡭ࡳࠦࡢࡦࡪࡤࡺࡪࠦࡨࡰࡱ࡮࠾ࠥࢁࡽࠨ೜").format(str(e)))
      except Exception as e:
        logger.debug(bstack1111_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡭ࡵ࡯࡬ࠢࡦࡰࡪࡧ࡮ࡶࡲࠣࡪࡴࡸࠠࡼࡿ࠽ࠤࢀࢃࠧೝ").format(name, str(e)))
  except Exception as e:
    logger.debug(bstack1111_opy_ (u"ࠫࡈࡸࡩࡵ࡫ࡦࡥࡱࠦࡥࡳࡴࡲࡶࠥ࡯࡮ࠡࡤࡨ࡬ࡦࡼࡥࠡࡴࡸࡲࠥ࡮࡯ࡰ࡭ࠣࡿࢂࡀࠠࡼࡿࠪೞ").format(name, str(e)))
    try:
      if bstack1ll1l1l11_opy_ is None or bstack1ll1l1l11_opy_:
        try:
          bstack11l11ll1l_opy_(self, name, self.context, *args)
        except TypeError:
          bstack11l11ll1l_opy_(self, name, *args)
      else:
        bstack11l11ll1l_opy_(self, name, *args)
    except Exception as e2:
      logger.debug(bstack1111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡲࡶ࡮࡭ࡩ࡯ࡣ࡯ࠤࡧ࡫ࡨࡢࡸࡨࠤ࡭ࡵ࡯࡬ࠢࡾࢁ࠿ࠦࡻࡾࠩ೟").format(name, str(e2)))
def bstack11l1l1l111_opy_(config, startdir):
  return bstack1111_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡀࠠࡼ࠲ࢀࠦೠ").format(bstack1111_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨೡ"))
notset = Notset()
def bstack111lll1lll_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1ll11lllll_opy_
  if str(name).lower() == bstack1111_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࠨೢ"):
    return bstack1111_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣೣ")
  else:
    return bstack1ll11lllll_opy_(self, name, default, skip)
def bstack11l11l11ll_opy_(item, when):
  global bstack1llll11111_opy_
  try:
    bstack1llll11111_opy_(item, when)
  except Exception as e:
    pass
def bstack1l11ll11ll_opy_():
  return
def browserstack_executor_helper(type, name, status, reason, bstack1l1l11l11_opy_, bstack1l11l1111l_opy_):
  bstack1111ll1l1_opy_ = {
    bstack1111_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪ೤"): type,
    bstack1111_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ೥"): {}
  }
  if type == bstack1111_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧ೦"):
    bstack1111ll1l1_opy_[bstack1111_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ೧")][bstack1111_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭೨")] = bstack1l1l11l11_opy_
    bstack1111ll1l1_opy_[bstack1111_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ೩")][bstack1111_opy_ (u"ࠩࡧࡥࡹࡧࠧ೪")] = json.dumps(str(bstack1l11l1111l_opy_))
  if type == bstack1111_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ೫"):
    bstack1111ll1l1_opy_[bstack1111_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ೬")][bstack1111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ೭")] = name
  if type == bstack1111_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩ೮"):
    bstack1111ll1l1_opy_[bstack1111_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ೯")][bstack1111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ೰")] = status
    if status == bstack1111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩೱ"):
      bstack1111ll1l1_opy_[bstack1111_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ೲ")][bstack1111_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫೳ")] = json.dumps(str(reason))
  bstack1l1ll1ll1_opy_ = bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪ೴").format(json.dumps(bstack1111ll1l1_opy_))
  return bstack1l1ll1ll1_opy_
def bstack1l11lllll1_opy_(driver_command, response):
    if driver_command == bstack1111_opy_ (u"࠭ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪ೵"):
        TestHubHandler.bstack1l11l1l1l_opy_({
            bstack1111_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭೶"): response[bstack1111_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧ೷")],
            bstack1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ೸"): TestHubHandler.current_test_uuid()
        })
def bstack11l1llllll_opy_(item, call, rep):
  global bstack1ll1l1ll_opy_
  global bstack1ll11111l1_opy_
  global bstack1ll1llll1_opy_
  name = bstack1111_opy_ (u"ࠪࠫ೹")
  try:
    if rep.when == bstack1111_opy_ (u"ࠫࡨࡧ࡬࡭ࠩ೺"):
      bstack1l1l111l11_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1ll1llll1_opy_:
          name = str(rep.nodeid)
          executor_string = browserstack_executor_helper(bstack1111_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭೻"), name, bstack1111_opy_ (u"࠭ࠧ೼"), bstack1111_opy_ (u"ࠧࠨ೽"), bstack1111_opy_ (u"ࠨࠩ೾"), bstack1111_opy_ (u"ࠩࠪ೿"))
          threading.current_thread().bstack11l111111l_opy_ = name
          for driver in bstack1ll11111l1_opy_:
            if bstack1l1l111l11_opy_ == driver.session_id:
              driver.execute_script(executor_string)
      except Exception as e:
        logger.debug(bstack1111_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪഀ").format(str(e)))
      try:
        bstack11ll1l11_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack1111_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬഁ"):
          status = bstack1111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬം") if rep.outcome.lower() == bstack1111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ഃ") else bstack1111_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧഄ")
          reason = bstack1111_opy_ (u"ࠨࠩഅ")
          if status == bstack1111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩആ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack1111_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨഇ") if status == bstack1111_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫഈ") else bstack1111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫഉ")
          data = name + bstack1111_opy_ (u"࠭ࠠࡱࡣࡶࡷࡪࡪࠡࠨഊ") if status == bstack1111_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧഋ") else name + bstack1111_opy_ (u"ࠨࠢࡩࡥ࡮ࡲࡥࡥࠣࠣࠫഌ") + reason
          bstack1l111l11_opy_ = browserstack_executor_helper(bstack1111_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫ഍"), bstack1111_opy_ (u"ࠪࠫഎ"), bstack1111_opy_ (u"ࠫࠬഏ"), bstack1111_opy_ (u"ࠬ࠭ഐ"), level, data)
          for driver in bstack1ll11111l1_opy_:
            if bstack1l1l111l11_opy_ == driver.session_id:
              driver.execute_script(bstack1l111l11_opy_)
      except Exception as e:
        logger.debug(bstack1111_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡧࡴࡴࡴࡦࡺࡷࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪ഑").format(str(e)))
  except Exception as e:
    logger.debug(bstack1111_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡷࡹࡧࡴࡦࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࡽࢀࠫഒ").format(str(e)))
  bstack1ll1l1ll_opy_(item, call, rep)
def bstack11lllllll1_opy_(driver, bstack11ll1111l1_opy_, test=None):
  global bstack11l11ll1_opy_
  if test != None:
    bstack1l1l11lll_opy_ = getattr(test, bstack1111_opy_ (u"ࠨࡰࡤࡱࡪ࠭ഓ"), None)
    bstack1lll111l1_opy_ = getattr(test, bstack1111_opy_ (u"ࠩࡸࡹ࡮ࡪࠧഔ"), None)
    PercySDK.screenshot(driver, bstack11ll1111l1_opy_, bstack1l1l11lll_opy_=bstack1l1l11lll_opy_, bstack1lll111l1_opy_=bstack1lll111l1_opy_, bstack11l1ll1ll_opy_=bstack11l11ll1_opy_)
  else:
    PercySDK.screenshot(driver, bstack11ll1111l1_opy_)
@measure(event_name=EVENTS.bstack1lll1llll_opy_, stage=STAGE.bstack111l1lllll_opy_, bstack11ll1l11l1_opy_=bstack1lll11ll1_opy_)
def bstack1l1l1l1l_opy_(driver):
  if bstack1l1l1ll1ll_opy_.bstack1lll1l11l1_opy_() is True or bstack1l1l1ll1ll_opy_.capturing() is True:
    return
  bstack1l1l1ll1ll_opy_.bstack1ll1l111l_opy_()
  while not bstack1l1l1ll1ll_opy_.bstack1lll1l11l1_opy_():
    bstack11lll1111l_opy_ = bstack1l1l1ll1ll_opy_.bstack111llll11_opy_()
    bstack11lllllll1_opy_(driver, bstack11lll1111l_opy_)
  bstack1l1l1ll1ll_opy_.bstack1lll1ll1l_opy_()
def bstack1l111l1111_opy_(sequence, driver_command, response = None, bstack1l1ll111ll_opy_ = None, args = None):
    try:
      if sequence != bstack1111_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪക"):
        return
      if percy.bstack1lll1l1l_opy_() == bstack1111_opy_ (u"ࠦ࡫ࡧ࡬ࡴࡧࠥഖ"):
        return
      bstack11lll1111l_opy_ = bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠬࡶࡥࡳࡥࡼࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨഗ"), None)
      for command in bstack111111l1l_opy_:
        if command == driver_command:
          with bstack111l1l11l_opy_:
            bstack1l1ll11l1_opy_ = bstack1ll11111l1_opy_.copy()
          for driver in bstack1l1ll11l1_opy_:
            bstack1l1l1l1l_opy_(driver)
      bstack111lll11l1_opy_ = percy.bstack11l1l1lll1_opy_()
      if driver_command in bstack11ll11lll1_opy_[bstack111lll11l1_opy_]:
        bstack1l1l1ll1ll_opy_.bstack111l11ll_opy_(bstack11lll1111l_opy_, driver_command)
    except Exception as e:
      pass
def bstack1l111ll1l1_opy_(framework_name):
  if global_config.get_property(bstack1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪഘ")):
      return
  global_config.bstack11llll1l1_opy_(bstack1111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟࡮ࡱࡧࡣࡨࡧ࡬࡭ࡧࡧࠫങ"), True)
  global bstack111llll11l_opy_
  global bstack11l1111l1_opy_
  global bstack1l1l111111_opy_
  bstack111llll11l_opy_ = framework_name
  logger.info(bstack1lll1ll111_opy_.format(bstack111llll11l_opy_.split(bstack1111_opy_ (u"ࠨ࠯ࠪച"))[0]))
  bstack1ll1l1lll1_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    global bstack11l1l11l11_opy_
    bstack1lll1lll1_opy_ = bstack1111ll1l_opy_ or bstack11l1l11l11_opy_
    if bstack1lll1lll1_opy_:
      Service.start = bstack1111l11l1_opy_
      Service.stop = bstack11l1l111l_opy_
      webdriver.Remote.get = bstack11ll11lll_opy_
      WebDriver.quit = bstack11111l111_opy_
      webdriver.Remote.__init__ = bstack11lll11lll_opy_
    if not bstack1111ll1l_opy_ and not bstack11l1l11l11_opy_:
        webdriver.Remote.__init__ = bstack1ll1lllll_opy_
    WebDriver.getAccessibilityResults = getAccessibilityResults
    WebDriver.get_accessibility_results = getAccessibilityResults
    WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
    WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
    WebDriver.performScan = perform_scan
    WebDriver.perform_scan = perform_scan
    WebDriver.execute = bstack1l111l11ll_opy_
    bstack11l1111l1_opy_ = True
  except Exception as e:
    pass
  try:
    bstack1lll1lll1_opy_ = bstack1111ll1l_opy_ or bstack11l1l11l11_opy_
    if bstack1lll1lll1_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1lll111ll1_opy_
  except Exception as e:
    pass
  bstack11l11l1l1l_opy_()
  if not bstack11l1111l1_opy_:
    bstack1lll11llll_opy_(bstack1111_opy_ (u"ࠤࡓࡥࡨࡱࡡࡨࡧࡶࠤࡳࡵࡴࠡ࡫ࡱࡷࡹࡧ࡬࡭ࡧࡧࠦഛ"), bstack1ll111lll1_opy_)
  if bstack1ll111l11l_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      if hasattr(RemoteConnection, bstack1111_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫജ")) and callable(getattr(RemoteConnection, bstack1111_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬഝ"))):
        RemoteConnection._get_proxy_url = bstack1111llll_opy_
      else:
        from selenium.webdriver.remote.client_config import ClientConfig
        ClientConfig.get_proxy_url = bstack1111llll_opy_
    except Exception as e:
      logger.error(bstack1l1ll1111_opy_.format(str(e)))
  if bstack1l111l1ll_opy_():
    bstack1ll1ll1ll1_opy_(CONFIG, logger)
  if (bstack1111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫഞ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      try:
        from pabot.pabot import QueueItem
        from pabot import pabot
      except Exception as e:
        logger.warning(bstack11llll1ll1_opy_ + str(e))
      if not is_robot_playwright_installed():
        try:
          if percy.bstack1lll1l1l_opy_() == bstack1111_opy_ (u"ࠨࡴࡳࡷࡨࠦട"):
            bstack111l1lll_opy_(bstack1l111l1111_opy_)
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
          WebDriverCreator._get_ff_profile = bstack11l11l1l11_opy_
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
          WebDriverCache.close = bstack1ll11l11l1_opy_
        except Exception as e:
          logger.warning(bstack111l1l111_opy_ + str(e))
        try:
          from AppiumLibrary.utils.applicationcache import ApplicationCache
          ApplicationCache.close = bstack11l1llll_opy_
        except Exception as e:
          logger.debug(bstack1ll1lll1ll_opy_ + str(e))
    except Exception as e:
      bstack1lll11llll_opy_(e, bstack111l1l111_opy_)
    Output.start_test = bstack11111l1l1_opy_
    Output.end_test = bstack1l1ll11l11_opy_
    TestStatus.__init__ = bstack111l11l1_opy_
    QueueItem.__init__ = bstack1l11l1l111_opy_
    pabot._create_items = bstack11ll111l11_opy_
    try:
      from pabot import __version__ as bstack11ll1l111_opy_
      if version.parse(bstack11ll1l111_opy_) >= version.parse(bstack1111_opy_ (u"ࠧ࠶࠰࠳࠲࠵࠭ഠ")):
        pabot._run = bstack11ll111l1l_opy_
      elif version.parse(bstack11ll1l111_opy_) >= version.parse(bstack1111_opy_ (u"ࠨ࠶࠱࠶࠳࠶ࠧഡ")):
        pabot._run = bstack1llll1llll_opy_
      elif version.parse(bstack11ll1l111_opy_) >= version.parse(bstack1111_opy_ (u"ࠩ࠵࠲࠶࠻࠮࠱ࠩഢ")):
        pabot._run = bstack1111ll111_opy_
      elif version.parse(bstack11ll1l111_opy_) >= version.parse(bstack1111_opy_ (u"ࠪ࠶࠳࠷࠳࠯࠲ࠪണ")):
        pabot._run = bstack1l1ll11l1l_opy_
      else:
        pabot._run = bstack1l1lllll_opy_
    except Exception as e:
      pabot._run = bstack1l1lllll_opy_
    pabot._create_command_for_execution = bstack11111l11l_opy_
    pabot._report_results = bstack11llll1l_opy_
  if bstack1111_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫത") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1lll11llll_opy_(e, bstack11ll1111ll_opy_)
    Runner.run_hook = bstack1l1llll1ll_opy_
    try:
      from behave import __version__ as bstack11l11l11l_opy_
      if version.parse(bstack11l11l11l_opy_) >= version.parse(bstack1111_opy_ (u"ࠬ࠷࠮࠴࠰࠳ࠫഥ")):
        Runner.load_hooks = bstack111l1111_opy_
    except Exception as e:
      logger.debug(bstack1111_opy_ (u"࠭ࡃࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥࡨࡥࡩࡣࡹࡩࠥࡼࡥࡳࡵ࡬ࡳࡳࡀࠠࡼࡿࠪദ").format(str(e)))
    Step.run = bstack11l1l1llll_opy_
  if bstack1111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧധ") in str(framework_name).lower():
    if not bstack1111ll1l_opy_:
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack11l1l1l111_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1l11ll11ll_opy_
      Config.getoption = bstack111lll1lll_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack11l1llllll_opy_
    except Exception as e:
      pass
def bstack111l1lll1l_opy_():
  global CONFIG
  if bstack1111_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨന") in CONFIG and int(CONFIG[bstack1111_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩഩ")]) > 1:
    logger.warning(bstack11ll1l11ll_opy_)
def bstack1lll1111_opy_(arg, bstack1l1lll111l_opy_, bstack1l1llllll1_opy_=None):
  global CONFIG
  global bstack11l1l1lll_opy_
  global bstack1l11l11ll1_opy_
  global bstack1111ll1l_opy_
  global bstack11l1l11l11_opy_
  global global_config
  bstack1ll1llllll_opy_ = bstack1111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪപ")
  if bstack1l1lll111l_opy_ and isinstance(bstack1l1lll111l_opy_, str):
    bstack1l1lll111l_opy_ = eval(bstack1l1lll111l_opy_)
  CONFIG = bstack1l1lll111l_opy_[bstack1111_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫഫ")]
  bstack11l1l1lll_opy_ = bstack1l1lll111l_opy_[bstack1111_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭ബ")]
  bstack1l11l11ll1_opy_ = bstack1l1lll111l_opy_[bstack1111_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨഭ")]
  bstack1111ll1l_opy_ = bstack1l1lll111l_opy_[bstack1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪമ")]
  try:
    bstack1lllll1ll_opy_ = bstack1l1lll111l_opy_.get(bstack1111_opy_ (u"ࠨࡑ࡙ࡉࡗࡘࡉࡅࡇࡢࡐࡔࡇࡄࡠࡖࡈࡗ࡙ࡏࡎࡈࠩയ"), False)
    bstack11l1l11l11_opy_ = bool(bstack1lllll1ll_opy_)
    os.environ[bstack1111_opy_ (u"ࠩࡒ࡚ࡊࡘࡒࡊࡆࡈࡣࡑࡕࡁࡅࡡࡗࡉࡘ࡚ࡉࡏࡉࠪര")] = str(bstack11l1l11l11_opy_).lower()
  except Exception as e:
    logger.error(bstack1111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡐࡘࡈࡖࡗࡏࡄࡆࡡࡏࡓࡆࡊ࡟ࡕࡇࡖࡘࡎࡔࡇ࠻ࠢࡾࢁࠧറ").format(e))
    bstack11l1l11l11_opy_ = False
    os.environ[bstack1111_opy_ (u"ࠫࡔ࡜ࡅࡓࡔࡌࡈࡊࡥࡌࡐࡃࡇࡣ࡙ࡋࡓࡕࡋࡑࡋࠬല")] = bstack1111_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫള")
  global_config.bstack11llll1l1_opy_(bstack1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧഴ"), bstack1111ll1l_opy_)
  os.environ[bstack1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩവ")] = bstack1ll1llllll_opy_
  os.environ[bstack1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍࠧശ")] = json.dumps(CONFIG)
  os.environ[bstack1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡊࡘࡆࡤ࡛ࡒࡍࠩഷ")] = bstack11l1l1lll_opy_
  os.environ[bstack1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫസ")] = str(bstack1l11l11ll1_opy_)
  os.environ[bstack1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡑ࡛ࡇࡊࡐࠪഹ")] = str(True)
  if bstack1l1l1lll1l_opy_(arg, [bstack1111_opy_ (u"ࠬ࠳࡮ࠨഺ"), bstack1111_opy_ (u"࠭࠭࠮ࡰࡸࡱࡵࡸ࡯ࡤࡧࡶࡷࡪࡹ഻ࠧ")]) != -1:
    os.environ[bstack1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡂࡔࡄࡐࡑࡋࡌࠨ഼")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack11l111l1_opy_)
    return
  bstack111l1lll11_opy_()
  global bstack1l1l11l1l_opy_
  global bstack11l11ll1_opy_
  global bstack111lllll1l_opy_
  global bstack1ll1l11l1_opy_
  global bstack1l1ll11lll_opy_
  global bstack1l1l111111_opy_
  global bstack1lll11l1ll_opy_
  arg.append(bstack1111_opy_ (u"ࠣ࠯࡚ࠦഽ"))
  arg.append(bstack1111_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡦ࠼ࡐࡳࡩࡻ࡬ࡦࠢࡤࡰࡷ࡫ࡡࡥࡻࠣ࡭ࡲࡶ࡯ࡳࡶࡨࡨ࠿ࡶࡹࡵࡧࡶࡸ࠳ࡖࡹࡵࡧࡶࡸ࡜ࡧࡲ࡯࡫ࡱ࡫ࠧാ"))
  arg.append(bstack1111_opy_ (u"ࠥ࠱࡜ࠨി"))
  arg.append(bstack1111_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨ࠾࡙࡮ࡥࠡࡪࡲࡳࡰ࡯࡭ࡱ࡮ࠥീ"))
  global bstack11l1111l11_opy_
  global bstack1l111ll1_opy_
  global bstack111lll1l1l_opy_
  global bstack1lll1111ll_opy_
  global bstack1lll11lll_opy_
  global bstack11ll1lll1l_opy_
  global bstack1llllll111_opy_
  global bstack1llll1ll1l_opy_
  global bstack1111ll1lll_opy_
  global bstack111l111111_opy_
  global bstack1ll11lllll_opy_
  global bstack1llll11111_opy_
  global bstack1ll1l1ll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11l1111l11_opy_ = webdriver.Remote.__init__
    bstack1l111ll1_opy_ = WebDriver.quit
    bstack1llll1ll1l_opy_ = WebDriver.close
    bstack1111ll1lll_opy_ = WebDriver.get
    bstack111lll1l1l_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack111l11l11_opy_(CONFIG) and bstack1lllll11l1_opy_():
    if bstack1l111ll11l_opy_() < version.parse(bstack11lll11ll_opy_):
      logger.error(bstack1111l11l_opy_.format(bstack1l111ll11l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack1111_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭ു")) and callable(getattr(RemoteConnection, bstack1111_opy_ (u"࠭࡟ࡨࡧࡷࡣࡵࡸ࡯ࡹࡻࡢࡹࡷࡲࠧൂ"))):
          bstack111l111111_opy_ = RemoteConnection._get_proxy_url
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          bstack111l111111_opy_ = ClientConfig.get_proxy_url
      except Exception as e:
        logger.error(bstack1l1ll1111_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1ll11lllll_opy_ = Config.getoption
    from _pytest import runner
    bstack1llll11111_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warning(bstack1111_opy_ (u"ࠢࠦࡵ࠽ࠤࠪࡹࠢൃ"), bstack1l11llll_opy_, str(e))
  try:
    from pytest_bdd import reporting
    bstack1ll1l1ll_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack1111_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡰࠢࡵࡹࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࡴࠩൄ"))
  if cli.is_enabled(CONFIG) and cli.config:
    bstack111lllll1l_opy_ = cli.config.get(bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭൅"), {}).get(bstack1111_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬെ"))
  else:
    bstack111lllll1l_opy_ = CONFIG.get(bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨേ"), {}).get(bstack1111_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧൈ"))
  bstack1lll11l1ll_opy_ = True
  if cli.is_enabled(CONFIG):
    if cli.bstack1lll1l1lll_opy_():
      bstack11l1lllll1_opy_.invoke(bstack1llll11l1_opy_.CONNECT, bstack11ll111l1_opy_())
    platform_index = int(os.environ.get(bstack1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭൉"), bstack1111_opy_ (u"ࠧ࠱ࠩൊ")))
  else:
    bstack1l111ll1l1_opy_(bstack111l111l11_opy_)
  os.environ[bstack1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩോ")] = CONFIG[bstack1111_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫൌ")]
  os.environ[bstack1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞്࠭")] = CONFIG[bstack1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧൎ")]
  os.environ[bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ൏")] = bstack1111ll1l_opy_.__str__()
  from _pytest.config import main as bstack1l11llll1l_opy_
  bstack1l11llll1_opy_ = []
  try:
    exit_code = bstack1l11llll1l_opy_(arg)
    if cli.is_enabled(CONFIG):
      cli.bstack111lll11ll_opy_()
    if bstack1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶࠪ൐") in multiprocessing.current_process().__dict__.keys():
      for bstack1ll111lll_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1l11llll1_opy_.append(bstack1ll111lll_opy_)
    try:
      bstack111l1l111l_opy_ = (bstack1l11llll1_opy_, int(exit_code))
      bstack1l1llllll1_opy_.append(bstack111l1l111l_opy_)
    except:
      bstack1l1llllll1_opy_.append((bstack1l11llll1_opy_, exit_code))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack1l11llll1_opy_.append({bstack1111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ൑"): bstack1111_opy_ (u"ࠨࡒࡵࡳࡨ࡫ࡳࡴࠢࠪ൒") + os.environ.get(bstack1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ൓")), bstack1111_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩൔ"): traceback.format_exc(), bstack1111_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪൕ"): int(os.environ.get(bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬൖ")))})
    bstack1l1llllll1_opy_.append((bstack1l11llll1_opy_, 1))
def mod_behave_main(args, retries):
  try:
    from behave.configuration import Configuration
    from behave.__main__ import run_behave
    from browserstack_sdk.bstack_behave_runner import BehaveRunner
    config = Configuration(args)
    config.update_userdata({bstack1111_opy_ (u"ࠨࡲࡦࡶࡵ࡭ࡪࡹࠢൗ"): str(retries)})
    return run_behave(config, runner_class=BehaveRunner)
  except Exception as e:
    bstack1lll1l11ll_opy_ = e.__class__.__name__
    print(bstack1111_opy_ (u"ࠢࠦࡵ࠽ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡶࡺࡴ࡮ࡪࡰࡪࠤࡧ࡫ࡨࡢࡸࡨࠤࡹ࡫ࡳࡵࠢࠨࡷࠧ൘") % (bstack1lll1l11ll_opy_, e))
    return 1
def bstack1111ll11_opy_(arg):
  global bstack111ll1l1ll_opy_
  bstack1l111ll1l1_opy_(bstack11l1l1l1_opy_)
  os.environ[bstack1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ൙")] = str(bstack1l11l11ll1_opy_)
  retries = bstack11l111lll1_opy_.bstack1ll11111ll_opy_(CONFIG)
  status_code = 0
  if bstack11l111lll1_opy_.bstack11111l11_opy_(CONFIG):
    status_code = mod_behave_main(arg, retries)
  else:
    from behave.__main__ import main as bstack1l111lll1_opy_
    status_code = bstack1l111lll1_opy_(arg)
  if status_code != 0:
    bstack111ll1l1ll_opy_ = status_code
def bstack1ll1l1llll_opy_():
  logger.info(bstack111lll1ll_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1111_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ൚"), help=bstack1111_opy_ (u"ࠪࡋࡪࡴࡥࡳࡣࡷࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡨࡵ࡮ࡧ࡫ࡪࠫ൛"))
  parser.add_argument(bstack1111_opy_ (u"ࠫ࠲ࡻࠧ൜"), bstack1111_opy_ (u"ࠬ࠳࠭ࡶࡵࡨࡶࡳࡧ࡭ࡦࠩ൝"), help=bstack1111_opy_ (u"࡙࠭ࡰࡷࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬ൞"))
  parser.add_argument(bstack1111_opy_ (u"ࠧ࠮࡭ࠪൟ"), bstack1111_opy_ (u"ࠨ࠯࠰࡯ࡪࡿࠧൠ"), help=bstack1111_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡡࡤࡥࡨࡷࡸࠦ࡫ࡦࡻࠪൡ"))
  parser.add_argument(bstack1111_opy_ (u"ࠪ࠱࡫࠭ൢ"), bstack1111_opy_ (u"ࠫ࠲࠳ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩൣ"), help=bstack1111_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ൤"))
  bstack1lllllllll_opy_ = parser.parse_args()
  try:
    bstack111ll111_opy_ = bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥ࡯ࡧࡵ࡭ࡨ࠴ࡹ࡮࡮࠱ࡷࡦࡳࡰ࡭ࡧࠪ൥")
    if bstack1lllllllll_opy_.framework and bstack1lllllllll_opy_.framework not in (bstack1111_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ൦"), bstack1111_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩ൧")):
      bstack111ll111_opy_ = bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠲ࡾࡳ࡬࠯ࡵࡤࡱࡵࡲࡥࠨ൨")
    bstack1ll1ll1l1_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack111ll111_opy_)
    bstack111ll11l11_opy_ = open(bstack1ll1ll1l1_opy_, bstack1111_opy_ (u"ࠪࡶࠬ൩"))
    bstack1l1l11l1ll_opy_ = bstack111ll11l11_opy_.read()
    bstack111ll11l11_opy_.close()
    if bstack1lllllllll_opy_.username:
      bstack1l1l11l1ll_opy_ = bstack1l1l11l1ll_opy_.replace(bstack1111_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫ൪"), bstack1lllllllll_opy_.username)
    if bstack1lllllllll_opy_.key:
      bstack1l1l11l1ll_opy_ = bstack1l1l11l1ll_opy_.replace(bstack1111_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧ൫"), bstack1lllllllll_opy_.key)
    if bstack1lllllllll_opy_.framework:
      bstack1l1l11l1ll_opy_ = bstack1l1l11l1ll_opy_.replace(bstack1111_opy_ (u"࡙࠭ࡐࡗࡕࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ൬"), bstack1lllllllll_opy_.framework)
    file_name = bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪ൭")
    file_path = os.path.abspath(file_name)
    bstack111ll1l1l_opy_ = open(file_path, bstack1111_opy_ (u"ࠨࡹࠪ൮"))
    bstack111ll1l1l_opy_.write(bstack1l1l11l1ll_opy_)
    bstack111ll1l1l_opy_.close()
    logger.info(bstack111lll1ll1_opy_)
    try:
      os.environ[bstack1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫ൯")] = bstack1lllllllll_opy_.framework if bstack1lllllllll_opy_.framework != None else bstack1111_opy_ (u"ࠥࠦ൰")
      config = yaml.safe_load(bstack1l1l11l1ll_opy_)
      config[bstack1111_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ൱")] = bstack1111_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲ࡹࡥࡵࡷࡳࠫ൲")
      bstack11l11l1ll_opy_(bstack11l1l11111_opy_, config)
    except Exception as e:
      logger.debug(bstack11l11l111_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack11llll1l1l_opy_.format(str(e)))
def bstack11l11l1ll_opy_(bstack111ll11ll_opy_, config, bstack11ll1l1ll1_opy_=None, bstack11l1l1111l_opy_=False):
  global bstack1111ll1l_opy_
  global bstack1l1l11ll11_opy_
  global global_config
  if not config:
    return
  if bstack11ll1l1ll1_opy_ is None:
    bstack11ll1l1ll1_opy_ = {}
  bstack1l11l1l1l1_opy_ = bstack111l11ll11_opy_ if not bstack1111ll1l_opy_ else (
    bstack1l1l1l1111_opy_ if bstack1111_opy_ (u"࠭ࡡࡱࡲࠪ൳") in config else (
        bstack1ll1111l11_opy_ if config.get(bstack1111_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ൴")) else bstack111ll1llll_opy_
    )
)
  bstack11111ll11_opy_ = False
  bstack1111lll1ll_opy_ = False
  if bstack1111ll1l_opy_ is True:
      if bstack1111_opy_ (u"ࠨࡣࡳࡴࠬ൵") in config:
          bstack11111ll11_opy_ = True
      else:
          bstack1111lll1ll_opy_ = True
  bstack1ll11ll1_opy_ = bstack1l111l1l_opy_.bstack111l11l1l1_opy_(config, bstack1l1l11ll11_opy_)
  bstack1llll111_opy_ = bstack1ll11l1l1_opy_()
  data = {
    bstack1111_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ൶"): config[bstack1111_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ൷")],
    bstack1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ൸"): config[bstack1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ൹")],
    bstack1111_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪൺ"): bstack111ll11ll_opy_,
    bstack1111_opy_ (u"ࠧࡥࡧࡷࡩࡨࡺࡥࡥࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫൻ"): os.environ.get(bstack1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪർ"), bstack1l1l11ll11_opy_),
    bstack1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫൽ"): bstack111ll1111l_opy_,
    bstack1111_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰࠬൾ"): bstack1llll11l11_opy_(),
    bstack1111_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧൿ"): {
      bstack1111_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ඀"): str(config[bstack1111_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ඁ")]) if bstack1111_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧං") in config else bstack1111_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤඃ"),
      bstack1111_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨ࡚ࡪࡸࡳࡪࡱࡱࠫ඄"): sys.version,
      bstack1111_opy_ (u"ࠪࡶࡪ࡬ࡥࡳࡴࡨࡶࠬඅ"): bstack1111l1lll_opy_(os.environ.get(bstack1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ආ"), bstack1l1l11ll11_opy_)),
      bstack1111_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠧඇ"): bstack1111_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ඈ"),
      bstack1111_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨඉ"): bstack1l11l1l1l1_opy_,
      bstack1111_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭ඊ"): bstack1ll11ll1_opy_,
      bstack1111_opy_ (u"ࠩࡷࡩࡸࡺࡨࡶࡤࡢࡹࡺ࡯ࡤࠨඋ"): os.environ[bstack1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨඌ")],
      bstack1111_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧඍ"): os.environ.get(bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧඎ"), bstack1l1l11ll11_opy_),
      bstack1111_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩඏ"): bstack1ll11l1111_opy_(os.environ.get(bstack1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩඐ"), bstack1l1l11ll11_opy_)),
      bstack1111_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧඑ"): bstack1llll111_opy_.get(bstack1111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧඒ")),
      bstack1111_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩඓ"): bstack1llll111_opy_.get(bstack1111_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬඔ")),
      bstack1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨඕ"): config[bstack1111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩඖ")] if config[bstack1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ඗")] else bstack1111_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤ඘"),
      bstack1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ඙"): str(config[bstack1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬක")]) if bstack1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ඛ") in config else bstack1111_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨග"),
      bstack1111_opy_ (u"࠭࡯ࡴࠩඝ"): sys.platform,
      bstack1111_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩඞ"): socket.gethostname(),
      bstack1111_opy_ (u"ࠨ࡫ࡶࡇࡑࡏࡅ࡯ࡣࡥࡰࡪࡪࠧඟ"): bstack11l1l1111l_opy_,
      bstack1111_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫච"): global_config.get_property(bstack1111_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࠬඡ"))
    }
  }
  if not global_config.get_property(bstack1111_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡘ࡯ࡧ࡯ࡣ࡯ࠫජ")) is None:
    data[bstack1111_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨඣ")][bstack1111_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡎࡧࡷࡥࡩࡧࡴࡢࠩඤ")] = {
      bstack1111_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧඥ"): bstack1111_opy_ (u"ࠨࡷࡶࡩࡷࡥ࡫ࡪ࡮࡯ࡩࡩ࠭ඦ"),
      bstack1111_opy_ (u"ࠩࡶ࡭࡬ࡴࡡ࡭ࠩට"): global_config.get_property(bstack1111_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪඨ")),
      bstack1111_opy_ (u"ࠫࡸ࡯ࡧ࡯ࡣ࡯ࡒࡺࡳࡢࡦࡴࠪඩ"): global_config.get_property(bstack1111_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱࡔ࡯ࠨඪ"))
    }
  if bstack111ll11ll_opy_ == bstack11llll1lll_opy_:
    data[bstack1111_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩණ")][bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡉ࡯࡯ࡨ࡬࡫ࠬඬ")] = bstack11l1l1l11_opy_(config)
    data[bstack1111_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫත")][bstack1111_opy_ (u"ࠩ࡬ࡷࡕ࡫ࡲࡤࡻࡄࡹࡹࡵࡅ࡯ࡣࡥࡰࡪࡪࠧථ")] = percy.bstack11111111_opy_
    data[bstack1111_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭ද")][bstack1111_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡅࡹ࡮ࡲࡤࡊࡦࠪධ")] = percy.percy_build_id
  if not bstack11l111lll1_opy_.bstack111l11llll_opy_(CONFIG):
    data[bstack1111_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨන")][bstack1111_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠪ඲")] = bstack11l111lll1_opy_.bstack111l11llll_opy_(CONFIG)
  bstack111l1l1l_opy_ = bstack1l1l111l1l_opy_.get_instance(CONFIG, logger)
  bstack1l11111ll1_opy_ = bstack11l111lll1_opy_.get_instance(config=CONFIG)
  if bstack111l1l1l_opy_ is not None and bstack1l11111ll1_opy_ is not None and bstack1l11111ll1_opy_.bstack1lll111111_opy_():
    data[bstack1111_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪඳ")][bstack1l11111ll1_opy_.bstack1ll11ll111_opy_()] = bstack111l1l1l_opy_.bstack111l1ll111_opy_()
  update(data[bstack1111_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫප")], bstack11ll1l1ll1_opy_)
  try:
    response = bstack1llll1l1ll_opy_(bstack1111_opy_ (u"ࠩࡓࡓࡘ࡚ࠧඵ"), bstack1l1ll1l1ll_opy_(bstack11l1111ll_opy_), data, {
      bstack1111_opy_ (u"ࠪࡥࡺࡺࡨࠨබ"): (config[bstack1111_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭භ")], config[bstack1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨම")])
    })
    if response:
      logger.debug(bstack11ll1ll11_opy_.format(bstack111ll11ll_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1l1lll1lll_opy_.format(str(e)))
def bstack1111l1lll_opy_(framework):
  return bstack1111_opy_ (u"ࠨࡻࡾ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࡼࡿࠥඹ").format(str(framework), __version__) if framework else bstack1111_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴ࢁࡽࠣය").format(
    __version__)
def bstack111l1lll11_opy_():
  global CONFIG
  global bstack1lll11111_opy_
  if bool(CONFIG):
    return
  try:
    bstack1l1l1l111l_opy_()
    logger.debug(bstack11ll1l1l_opy_.format(str(CONFIG)))
    bstack1lll11111_opy_ = logger_utils.configure_logger(CONFIG, bstack1lll11111_opy_)
    bstack1ll1l1lll1_opy_()
  except Exception as e:
    logger.error(bstack1111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࡶࡲ࠯ࠤࡪࡸࡲࡰࡴ࠽ࠤࠧර") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1ll1l1ll1l_opy_
  atexit.register(bstack111lll1l11_opy_)
  signal.signal(signal.SIGINT, bstack1l1ll1l111_opy_)
  signal.signal(signal.SIGTERM, bstack1l1ll1l111_opy_)
def bstack1ll1l1ll1l_opy_(exctype, value, traceback):
  global bstack1ll11111l1_opy_
  try:
    for driver in bstack1ll11111l1_opy_:
      bstack1l1lllll1l_opy_(driver, bstack1111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ඼"), bstack1111_opy_ (u"ࠥࡗࡪࡹࡳࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨල") + str(value))
  except Exception:
    pass
  logger.info(bstack1l1l11lll1_opy_)
  bstack11l1ll11l_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack11l1ll11l_opy_(message=bstack1111_opy_ (u"ࠫࠬ඾"), bstack11l111l1l_opy_ = False, bstack11l1l1111l_opy_ = False):
  global CONFIG
  bstack1lll1l111_opy_ = bstack1111_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠧ඿") if bstack11l111l1l_opy_ else bstack1111_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬව")
  bstack11lll1ll11_opy_ = bstack1l11l1ll_opy_.bstack11l111111_opy_(EVENTS.bstack11ll11l1_opy_)
  try:
    if message:
      bstack11ll1l1ll1_opy_ = {
        bstack1lll1l111_opy_ : str(message)
      }
      try:
        bstack11l11l1ll_opy_(bstack11llll1lll_opy_, CONFIG, bstack11ll1l1ll1_opy_, bstack11l1l1111l_opy_)
      finally:
        bstack1l11l1ll_opy_.end(EVENTS.bstack11ll11l1_opy_.value, bstack11lll1ll11_opy_ + bstack1111_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢශ"), bstack11lll1ll11_opy_ + bstack1111_opy_ (u"ࠣ࠼ࡨࡲࡩࠨෂ"), status=True, failure=None, test_name=None)
    else:
      try:
        bstack11l11l1ll_opy_(bstack11llll1lll_opy_, CONFIG, bstack11l1l1111l_opy_=bstack11l1l1111l_opy_)
      finally:
        bstack1l11l1ll_opy_.end(EVENTS.bstack11ll11l1_opy_.value, bstack11lll1ll11_opy_ + bstack1111_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤස"), bstack11lll1ll11_opy_ + bstack1111_opy_ (u"ࠥ࠾ࡪࡴࡤࠣහ"), status=True, failure=None, test_name=None)
  except Exception as e:
    logger.debug(bstack1l1l1llll_opy_.format(str(e)))
def bstack11l1l11ll1_opy_(bstack11ll1l1ll_opy_, size):
  bstack1lll1lllll_opy_ = []
  while len(bstack11ll1l1ll_opy_) > size:
    bstack1lll1ll1ll_opy_ = bstack11ll1l1ll_opy_[:size]
    bstack1lll1lllll_opy_.append(bstack1lll1ll1ll_opy_)
    bstack11ll1l1ll_opy_ = bstack11ll1l1ll_opy_[size:]
  bstack1lll1lllll_opy_.append(bstack11ll1l1ll_opy_)
  return bstack1lll1lllll_opy_
def bstack1ll11llll_opy_(args):
  if bstack1111_opy_ (u"ࠫ࠲ࡳࠧළ") in args and bstack1111_opy_ (u"ࠬࡶࡤࡣࠩෆ") in args:
    return True
  return False
@measure(event_name=EVENTS.bstack11l11lllll_opy_, stage=STAGE.bstack1llllll11l_opy_)
def run_on_browserstack(bstack1l1111l1l_opy_=None, bstack1l1llllll1_opy_=None, bstack11ll11111l_opy_=False):
  global CONFIG
  global bstack11l1l1lll_opy_
  global bstack1l11l11ll1_opy_
  global bstack1l1l11ll11_opy_
  global global_config
  bstack1ll1llllll_opy_ = bstack1111_opy_ (u"࠭ࠧ෇")
  bstack1ll111l1ll_opy_ = bstack1111_opy_ (u"ࠢࠣ෈")
  bstack1l1lll1l1l_opy_(bstack1l11ll1ll_opy_, logger)
  if bstack1l1111l1l_opy_ and isinstance(bstack1l1111l1l_opy_, str):
    bstack1l1111l1l_opy_ = eval(bstack1l1111l1l_opy_)
  if bstack1l1111l1l_opy_:
    CONFIG = bstack1l1111l1l_opy_[bstack1111_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨ෉")]
    bstack11l1l1lll_opy_ = bstack1l1111l1l_opy_[bstack1111_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎ්ࠪ")]
    bstack1l11l11ll1_opy_ = bstack1l1111l1l_opy_[bstack1111_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ෋")]
    global_config.bstack11llll1l1_opy_(bstack1111_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭෌"), bstack1l11l11ll1_opy_)
    bstack1ll1llllll_opy_ = bstack1111_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨ࠭෍")
  global_config.bstack11llll1l1_opy_(bstack1111_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨ෎"), uuid4().__str__())
  logger.info(bstack1111_opy_ (u"ࠧࡔࡆࡎࠤࡷࡻ࡮ࠡࡵࡷࡥࡷࡺࡥࡥࠢࡺ࡭ࡹ࡮ࠠࡪࡦ࠽ࠤࠬා") + global_config.get_property(bstack1111_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪැ")));
  logger.debug(bstack1111_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࡁࠬෑ") + global_config.get_property(bstack1111_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࠬි")))
  if not bstack11ll11111l_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack11l111l1_opy_)
      return
    if sys.argv[1] == bstack1111_opy_ (u"ࠫ࠲࠳ࡶࡦࡴࡶ࡭ࡴࡴࠧී") or sys.argv[1] == bstack1111_opy_ (u"ࠬ࠳ࡶࠨු"):
      logger.info(bstack1111_opy_ (u"࠭ࡂࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡖࡹࡵࡪࡲࡲ࡙ࠥࡄࡌࠢࡹࡿࢂ࠭෕").format(__version__))
      return
    if sys.argv[1] == bstack1111_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ූ"):
      bstack1ll1l1llll_opy_()
      return
    if sys.argv[1] == bstack1111_opy_ (u"ࠨ࡮ࡲࡥࡩ࠭෗"):
      from browserstack_sdk.bstack1l1111l11l_opy_ import bstack111ll1lll_opy_
      bstack111l1lll11_opy_()
      bstack111ll1lll_opy_(CONFIG)
      return
  args = sys.argv
  bstack111l1lll11_opy_()
  global bstack11l1l11l11_opy_
  try:
    from bstack_utils import constants as bstack1l11l1llll_opy_
    override_value = CONFIG.get(bstack1111_opy_ (u"ࠩࡲࡺࡪࡸࡲࡪࡦࡨࡐࡴࡧࡤࡕࡧࡶࡸ࡮ࡴࡧࠨෘ"), False)
    bstack11l1l11l11_opy_ = bool(override_value)
  except Exception as e:
    logger.error(bstack1111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡐࡘࡈࡖࡗࡏࡄࡆࡡࡏࡓࡆࡊ࡟ࡕࡇࡖࡘࡎࡔࡇ࠻ࠢࡾࢁࠧෙ").format(e))
    bstack11l1l11l11_opy_ = False
  if bstack11l1l11l11_opy_:
    bstack1l11ll1l1_opy_ = CONFIG.get(bstack1111_opy_ (u"ࠫࡱࡵࡡࡥࡖࡨࡷࡹ࡯࡮ࡨࡊࡸࡦ࡚ࡘࡌࠨේ")) or bstack1l11l1llll_opy_.bstack1l11l1l1_opy_
    logger.info(bstack1111_opy_ (u"ࠧࡍ࡬ࡰࡤࡤࡰࠥࡵࡶࡦࡴࡵ࡭ࡩ࡫࡬ࡰࡣࡧࡸࡪࡹࡴࡪࡰࡪࠤࡪࡴࡡࡣ࡮ࡨࡨ࠱ࠦࡵࡴ࡫ࡱ࡫ࠥ࡮ࡵࡣ࠼ࠣࡿࢂࠨෛ").format(bstack1l11ll1l1_opy_))
    bstack11l1l1lll_opy_ = bstack1l11ll1l1_opy_
    try:
      bstack1l11l1llll_opy_.HTTPS_HUB = bstack1l11ll1l1_opy_
      bstack1l11l1llll_opy_.bstack11l11lll1_opy_ = bstack1l11ll1l1_opy_
    except Exception:
      pass
  global bstack1l1l11l1l_opy_
  global bstack11llllll_opy_
  global bstack1lll11l1ll_opy_
  global bstack111lllll11_opy_
  global bstack11l11ll1_opy_
  global bstack111lllll1l_opy_
  global bstack1ll1l11l1_opy_
  global bstack1ll11lll1l_opy_
  global bstack1l1ll11lll_opy_
  global bstack1l1l111111_opy_
  global bstack1ll11l11_opy_
  bstack11llllll_opy_ = len(CONFIG.get(bstack1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩො"), []))
  if not bstack1ll1llllll_opy_:
    if args[1] == bstack1111_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧෝ") or args[1] == bstack1111_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩෞ") or args[1] == bstack1111_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠪෟ"):
      bstack1ll1llllll_opy_ = bstack1111_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠫ෠")
      args = args[2:]
    elif args[1] == bstack1111_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ෡"):
      bstack1ll1llllll_opy_ = bstack1111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ෢")
      args = args[2:]
    elif args[1] == bstack1111_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ෣"):
      bstack1ll1llllll_opy_ = bstack1111_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭෤")
      args = args[2:]
    elif args[1] == bstack1111_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ෥"):
      bstack1ll1llllll_opy_ = bstack1111_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ෦")
      args = args[2:]
    elif args[1] == bstack1111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ෧"):
      bstack1ll1llllll_opy_ = bstack1111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ෨")
      args = args[2:]
    elif args[1] == bstack1111_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ෩"):
      bstack1ll1llllll_opy_ = bstack1111_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭෪")
      args = args[2:]
    else:
      if not bstack1111_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ෫") in CONFIG or str(CONFIG[bstack1111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ෬")]).lower() in [bstack1111_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ෭"), bstack1111_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫ෮"), bstack1111_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠬ෯")]:
        bstack1ll1llllll_opy_ = bstack1111_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨ࠭෰")
        args = args[1:]
      elif str(CONFIG[bstack1111_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ෱")]).lower() == bstack1111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ෲ"):
        bstack1ll1llllll_opy_ = bstack1111_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧෳ")
        args = args[1:]
      elif str(CONFIG[bstack1111_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ෴")]).lower() == bstack1111_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ෵"):
        bstack1ll1llllll_opy_ = bstack1111_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ෶")
        args = args[1:]
      elif str(CONFIG[bstack1111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ෷")]).lower() == bstack1111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭෸"):
        bstack1ll1llllll_opy_ = bstack1111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ෹")
        args = args[1:]
      elif str(CONFIG[bstack1111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ෺")]).lower() == bstack1111_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ෻"):
        bstack1ll1llllll_opy_ = bstack1111_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ෼")
        args = args[1:]
      else:
        os.environ[bstack1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭෽")] = bstack1ll1llllll_opy_
        bstack1ll1ll11_opy_(bstack11lll11l1l_opy_)
  os.environ[bstack1111_opy_ (u"ࠬࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉ࠭෾")] = bstack1ll1llllll_opy_
  bstack1l1l11ll11_opy_ = bstack1ll1llllll_opy_
  if cli.is_enabled(CONFIG):
    try:
      if bstack1ll1llllll_opy_ == bstack1111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭෿") and bstack1l1ll11l_opy_():
        bstack11llll11ll_opy_ = bstack111lll1l_opy_[bstack1111_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࠭ࡃࡆࡇࠫ฀")]
      elif bstack1ll1llllll_opy_ in [bstack1111_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩก"), bstack1111_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨข")]:
        bstack11llll11ll_opy_ = bstack1111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩฃ")
      else:
        bstack11llll11ll_opy_ = bstack1ll1llllll_opy_
      bstack11l1lllll1_opy_.invoke(bstack1llll11l1_opy_.bstack1ll1l111l1_opy_, bstack1ll11lll11_opy_(
        sdk_version=__version__,
        path_config=bstack111llllll1_opy_(),
        path_project=os.getcwd(),
        test_framework=bstack11llll11ll_opy_,
        frameworks=[bstack11llll11ll_opy_],
        framework_versions={
          bstack11llll11ll_opy_: bstack1ll11l1111_opy_(bstack1111_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪค") if bstack1ll1llllll_opy_ in [bstack1111_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫฅ"), bstack1111_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬฆ"), bstack1111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨง")] else bstack1ll1llllll_opy_)
        },
        bs_config=CONFIG
      ))
      if cli.config and cli.config.get(bstack1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠥจ"), None):
        CONFIG[bstack1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠦฉ")] = cli.config.get(bstack1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧช"), None)
    except Exception as e:
      bstack11l1lllll1_opy_.invoke(bstack1llll11l1_opy_.bstack11ll11l1l_opy_, e.__traceback__, 1)
    if bstack1l11l11ll1_opy_:
      CONFIG[bstack1111_opy_ (u"ࠦࡦࡶࡰࠣซ")] = cli.config[bstack1111_opy_ (u"ࠧࡧࡰࡱࠤฌ")]
      logger.info(bstack11lll1l1l1_opy_.format(CONFIG[bstack1111_opy_ (u"࠭ࡡࡱࡲࠪญ")]))
  else:
    bstack11l1lllll1_opy_.clear()
  global bstack1lll1ll11_opy_
  global bstack111llll1l1_opy_
  if bstack1l1111l1l_opy_:
    try:
      bstack1l1llll111_opy_ = datetime.datetime.now()
      os.environ[bstack1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩฎ")] = bstack1ll1llllll_opy_
      bstack11lll1111_opy_ = bstack1l11l1ll_opy_.bstack11l111111_opy_(EVENTS.bstack11lllll1_opy_)
      try:
        logger.info(bstack1111_opy_ (u"ࠣࡕࡨࡲࡩ࡯࡮ࡨࠢࡖࡈࡐࠦࡔࡦࡵࡷࠤࡆࡺࡴࡦ࡯ࡳࡸࡪࡪࠠࡦࡸࡨࡲࡹࠨฏ"))
        bstack11l11l1ll_opy_(bstack1ll11lll1_opy_, CONFIG)
      finally:
        bstack1l11l1ll_opy_.end(EVENTS.bstack11lllll1_opy_.value, bstack11lll1111_opy_ + bstack1111_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤฐ"), bstack11lll1111_opy_ + bstack1111_opy_ (u"ࠥ࠾ࡪࡴࡤࠣฑ"), status=True, failure=None, test_name=None)
      cli.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼ࡶࡨࡰࡥࡴࡦࡵࡷࡣࡦࡺࡴࡦ࡯ࡳࡸࡪࡪࠢฒ"), datetime.datetime.now() - bstack1l1llll111_opy_)
    except Exception as e:
      logger.debug(bstack1ll11ll1l_opy_.format(str(e)))
  global bstack11l1111l11_opy_
  global bstack1l111ll1_opy_
  global bstack1l1l11l1_opy_
  global bstack11l11111ll_opy_
  global bstack111l1111l_opy_
  global bstack11l1ll111_opy_
  global bstack1lll1111ll_opy_
  global bstack1lll11lll_opy_
  global bstack1l11lll1ll_opy_
  global bstack11ll1lll1l_opy_
  global bstack1llllll111_opy_
  global bstack1llll1ll1l_opy_
  global bstack11l11ll1l_opy_
  global bstack1ll1l111ll_opy_
  global bstack1l11l1ll11_opy_
  global bstack1111ll1lll_opy_
  global bstack111l111111_opy_
  global bstack1ll11lllll_opy_
  global bstack1llll11111_opy_
  global bstack1l1ll1ll_opy_
  global bstack1ll1l1ll_opy_
  global bstack111lll1l1l_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11l1111l11_opy_ = webdriver.Remote.__init__
    bstack1l111ll1_opy_ = WebDriver.quit
    bstack1llll1ll1l_opy_ = WebDriver.close
    bstack1111ll1lll_opy_ = WebDriver.get
    bstack111lll1l1l_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1lll1ll11_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack111l1l1l1_opy_
    bstack111llll1l1_opy_ = bstack111l1l1l1_opy_()
  except Exception as e:
    pass
  try:
    global bstack1l11llllll_opy_
    from QWeb.keywords import browser
    bstack1l11llllll_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack111l11l11_opy_(CONFIG) and bstack1lllll11l1_opy_():
    if bstack1l111ll11l_opy_() < version.parse(bstack11lll11ll_opy_):
      logger.error(bstack1111l11l_opy_.format(bstack1l111ll11l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack1111_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭ณ")) and callable(getattr(RemoteConnection, bstack1111_opy_ (u"࠭࡟ࡨࡧࡷࡣࡵࡸ࡯ࡹࡻࡢࡹࡷࡲࠧด"))):
          RemoteConnection._get_proxy_url = bstack1111llll_opy_
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          ClientConfig.get_proxy_url = bstack1111llll_opy_
      except Exception as e:
        logger.error(bstack1l1ll1111_opy_.format(str(e)))
  if not CONFIG.get(bstack1111_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡷࡷࡳࡈࡧࡰࡵࡷࡵࡩࡑࡵࡧࡴࠩต"), False) and not bstack1l1111l1l_opy_:
    logger.info(bstack1lll1l11l_opy_)
  bstack11ll1111_opy_ = not cli.is_enabled(CONFIG) and bstack1ll1llllll_opy_ not in [bstack1111_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩถ")]
  bstack1l1lll1l1_opy_ = bstack11ll1111_opy_ and bstack1111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ท") in CONFIG and str(CONFIG[bstack1111_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧธ")]).lower() != bstack1111_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪน")
  bstack1ll1ll111_opy_ = bstack11ll1111_opy_ and not bstack1l1lll1l1_opy_ and (bstack1ll1llllll_opy_ != bstack1111_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨ࠭บ") or (bstack1ll1llllll_opy_ == bstack1111_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡧࡦࡰࡨࡶ࡮ࡩࠧป") and not bstack1l1111l1l_opy_))
  if bstack1ll1llllll_opy_ not in [bstack1111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨผ")]:
    bstack1l1lll1l1l_opy_(os.path.join(os.getcwd(), bstack1111_opy_ (u"ࠨ࡮ࡲ࡫ࠬฝ"), bstack1111_opy_ (u"ࠩ࡮ࡩࡾ࠳࡭ࡦࡶࡵ࡭ࡨࡹ࠮࡫ࡵࡲࡲࠬพ")), logger)
  if (bstack1ll1llllll_opy_ in [bstack1111_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩฟ"), bstack1111_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪภ"), bstack1111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ม")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      try:
        from pabot.pabot import QueueItem
        from pabot import pabot
      except Exception as e:
        logger.warning(bstack11llll1ll1_opy_ + str(e))
      if not is_robot_playwright_installed():
        try:
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
          WebDriverCreator._get_ff_profile = bstack11l11l1l11_opy_
          bstack11l1ll111_opy_ = WebDriverCache.close
        except Exception as e:
          logger.warning(bstack111l1l111_opy_ + str(e))
        try:
          from AppiumLibrary.utils.applicationcache import ApplicationCache
          bstack111l1111l_opy_ = ApplicationCache.close
        except Exception as e:
          logger.debug(bstack1ll1lll1ll_opy_ + str(e))
    except Exception as e:
      bstack1lll11llll_opy_(e, bstack111l1l111_opy_)
    if bstack1ll1llllll_opy_ != bstack1111_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧย"):
      bstack1l11l111l_opy_()
    bstack1l1l11l1_opy_ = Output.start_test
    bstack11l11111ll_opy_ = Output.end_test
    bstack1lll1111ll_opy_ = TestStatus.__init__
    bstack1l11lll1ll_opy_ = pabot._run
    bstack11ll1lll1l_opy_ = QueueItem.__init__
    bstack1llllll111_opy_ = pabot._create_command_for_execution
    bstack1l1ll1ll_opy_ = pabot._report_results
  if bstack1ll1llllll_opy_ == bstack1111_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧร"):
    global bstack1ll1l1l11_opy_
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1lll11llll_opy_(e, bstack11ll1111ll_opy_)
    bstack11l11ll1l_opy_ = Runner.run_hook
    bstack1ll1l111ll_opy_ = Runner.load_hooks
    bstack1l11l1ll11_opy_ = Step.run
    try:
      sig = inspect.signature(bstack11l11ll1l_opy_)
      params = list(sig.parameters.keys())
      bstack1ll1l1l11_opy_ = bstack1111_opy_ (u"ࠨࡥࡲࡲࡹ࡫ࡸࡵࠩฤ") in params
      logger.info(bstack1111_opy_ (u"ࠩࡇࡩࡹ࡫ࡣࡵࡧࡧࠤࡧ࡫ࡨࡢࡸࡨࠤࡷࡻ࡮ࡠࡪࡲࡳࡰࠦࡳࡪࡩࡱࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭ล").format(bstack1111_opy_ (u"ࠪ࠵࠳࠸࠮࠷ࠢࠫࡻ࡮ࡺࡨࠡࡥࡲࡲࡹ࡫ࡸࡵࠫࠪฦ") if bstack1ll1l1l11_opy_ else bstack1111_opy_ (u"ࠫ࠶࠴࠳ࠬࠢࠫࡻ࡮ࡺࡨࡰࡷࡷࠤࡨࡵ࡮ࡵࡧࡻࡸ࠮࠭ว")))
    except Exception as e:
      logger.debug(bstack1111_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡩࡴࠡࡤࡨ࡬ࡦࡼࡥࠡࡴࡸࡲࡤ࡮࡯ࡰ࡭ࠣࡷ࡮࡭࡮ࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪศ").format(str(e)))
      bstack1ll1l1l11_opy_ = None
  if bstack1ll1llllll_opy_ == bstack1111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ษ"):
    try:
      from _pytest.config import Config
      bstack1ll11lllll_opy_ = Config.getoption
      from _pytest import runner
      bstack1llll11111_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warning(bstack1111_opy_ (u"ࠢࠦࡵ࠽ࠤࠪࡹࠢส"), bstack1l11llll_opy_, str(e))
    try:
      from pytest_bdd import reporting
      bstack1ll1l1ll_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1111_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡰࠢࡵࡹࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࡴࠩห"))
    if bstack11l1l111ll_opy_():
      logger.warning(bstack11l11l11l1_opy_[bstack1111_opy_ (u"ࠩࡖࡈࡐ࠳ࡇࡆࡐ࠰࠴࠵࠻ࠧฬ")])
  try:
    framework_name = bstack1111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩอ") if bstack1ll1llllll_opy_ in [bstack1111_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪฮ"), bstack1111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫฯ"), bstack1111_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧะ")] else bstack1l11l1111_opy_(bstack1ll1llllll_opy_)
    bstack11l1llll11_opy_ = {
      bstack1111_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠨั"): bstack1111_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪา") if bstack1ll1llllll_opy_ == bstack1111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩำ") and bstack1l1ll11l_opy_() else framework_name,
      bstack1111_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧิ"): bstack1ll11l1111_opy_(framework_name),
      bstack1111_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩี"): __version__,
      bstack1111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡷࡶࡩࡩ࠭ึ"): bstack1ll1llllll_opy_
    }
    if bstack1ll1llllll_opy_ in bstack1l11lll1l1_opy_ + bstack1lll11l1l_opy_:
      if bstack11l1111111_opy_.bstack1llllll11_opy_(CONFIG):
        if bstack1111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ื") in CONFIG:
          os.environ[bstack1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨุ")] = os.getenv(bstack1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍูࠩ"), json.dumps(CONFIG[bstack1111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴฺࠩ")]))
          CONFIG[bstack1111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ฻")].pop(bstack1111_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ฼"), None)
          CONFIG[bstack1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ฽")].pop(bstack1111_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫ฾"), None)
        bstack11l1llll11_opy_[bstack1111_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ฿")] = {
          bstack1111_opy_ (u"ࠨࡰࡤࡱࡪ࠭เ"): bstack1111_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫแ"),
          bstack1111_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫโ"): str(bstack1l111ll11l_opy_())
        }
    bstack11111111l_opy_, bstack1llll1lll1_opy_ = None, {}
    bstack1ll1l1l1l_opy_ = None
    bstack1l1l11ll_opy_ = None
    def bstack1l1111lll1_opy_():
      if bstack1l1lll1l1_opy_:
        bstack11ll1l1111_opy_()
      elif bstack1ll1ll111_opy_:
        bstack11ll11ll1_opy_()
    def bstack1lll1l111l_opy_():
      nonlocal bstack11111111l_opy_, bstack1llll1lll1_opy_
      if bstack1ll1llllll_opy_ not in [bstack1111_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬใ")] and not cli.is_running():
        bstack11111111l_opy_, bstack1llll1lll1_opy_ = TestHubHandler.launch(CONFIG, bstack11l1llll11_opy_)
    if bstack1l1lll1l1_opy_ or bstack1ll1ll111_opy_:
      bstack1ll1l1l1l_opy_ = threading.Thread(target=bstack1l1111lll1_opy_)
      bstack1ll1l1l1l_opy_.start()
    if bstack1ll1llllll_opy_ not in [bstack1111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ไ")] and not cli.is_running():
      bstack1l1l11ll_opy_ = threading.Thread(target=bstack1lll1l111l_opy_)
      bstack1l1l11ll_opy_.start()
    if bstack1ll1l1l1l_opy_:
      bstack1ll1l1l1l_opy_.join()
    if bstack1l1l11ll_opy_:
      bstack1l1l11ll_opy_.join()
    if bstack1llll1lll1_opy_.get(bstack1111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ๅ")) is not None and bstack11l1111111_opy_.bstack1l1l1ll1l_opy_(CONFIG) is None:
      value = bstack1llll1lll1_opy_[bstack1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧๆ")].get(bstack1111_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩ็"))
      if value is not None:
          CONFIG[bstack1111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺ่ࠩ")] = value
      else:
        logger.debug(bstack1111_opy_ (u"ࠥࡒࡴࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡤࡢࡶࡤࠤ࡫ࡵࡵ࡯ࡦࠣ࡭ࡳࠦࡲࡦࡵࡳࡳࡳࡹࡥ้ࠣ"))
  except Exception as e:
    logger.debug(bstack1l11111l1_opy_.format(bstack1111_opy_ (u"࡙ࠫ࡫ࡳࡵࡊࡸࡦ๊ࠬ"), str(e)))
  if bstack1ll1llllll_opy_ == bstack1111_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨ๋࠭"):
    bstack1lll11l1ll_opy_ = True
    if bstack1l1111l1l_opy_ and bstack11ll11111l_opy_:
      if cli.is_enabled(CONFIG):
        bstack111lllll1l_opy_ = cli.config.get(bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ์"), {}).get(bstack1111_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩํ")) if cli.config else None
      else:
        bstack111lllll1l_opy_ = CONFIG.get(bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ๎"), {}).get(bstack1111_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ๏"))
      bstack1l111ll1l1_opy_(bstack1l1lllll1_opy_)
    elif bstack1l1111l1l_opy_:
      if cli.is_enabled(CONFIG):
        bstack111lllll1l_opy_ = cli.config.get(bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ๐"), {}).get(bstack1111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭๑")) if cli.config else None
      else:
        bstack111lllll1l_opy_ = CONFIG.get(bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ๒"), {}).get(bstack1111_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ๓"))
      global bstack1ll11111l1_opy_
      try:
        if bstack1ll11llll_opy_(bstack1l1111l1l_opy_[bstack1111_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ๔")]) and multiprocessing.current_process().name == bstack1111_opy_ (u"ࠨ࠲ࠪ๕"):
          bstack1l1111l1l_opy_[bstack1111_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ๖")].remove(bstack1111_opy_ (u"ࠪ࠱ࡲ࠭๗"))
          bstack1l1111l1l_opy_[bstack1111_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ๘")].remove(bstack1111_opy_ (u"ࠬࡶࡤࡣࠩ๙"))
          bstack1l1111l1l_opy_[bstack1111_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ๚")] = bstack1l1111l1l_opy_[bstack1111_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ๛")][0]
          with open(bstack1l1111l1l_opy_[bstack1111_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ๜")], bstack1111_opy_ (u"ࠩࡵࠫ๝")) as f:
            bstack1ll1llll1l_opy_ = f.read()
          bstack11l11111l1_opy_ = bstack1111_opy_ (u"ࠥࠦࠧ࡬ࡲࡰ࡯ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡨࡰࠦࡩ࡮ࡲࡲࡶࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦ࠽ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪ࠮ࡻࡾࠫ࠾ࠤ࡫ࡸ࡯࡮ࠢࡳࡨࡧࠦࡩ࡮ࡲࡲࡶࡹࠦࡐࡥࡤ࠾ࠤࡴ࡭࡟ࡥࡤࠣࡁࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡦࡨࡪࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠩࡵࡨࡰ࡫࠲ࠠࡢࡴࡪ࠰ࠥࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠡ࠿ࠣ࠴࠮ࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺࡲࡺ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡥࡷ࡭ࠠ࠾ࠢࡶࡸࡷ࠮ࡩ࡯ࡶࠫࡥࡷ࡭ࠩࠬ࠳࠳࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡩࡽࡩࡥࡱࡶࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡡࡴࠢࡨ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡶࡡࡴࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡱࡪࡣࡩࡨࠨࡴࡧ࡯ࡪ࠱ࡧࡲࡨ࠮ࡷࡩࡲࡶ࡯ࡳࡣࡵࡽ࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡓࡨࡧ࠴ࡤࡰࡡࡥࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮ࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣࠪࠬ࠲ࡸ࡫ࡴࡠࡶࡵࡥࡨ࡫ࠨࠪ࡞ࡱࠦࠧࠨ๞").format(str(bstack1l1111l1l_opy_))
          bstack1l11lll1_opy_ = bstack11l11111l1_opy_ + bstack1ll1llll1l_opy_
          bstack11lll11l11_opy_ = bstack1l1111l1l_opy_[bstack1111_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ๟")] + bstack1111_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥࡴࡦ࡯ࡳ࠲ࡵࡿࠧ๠")
          with open(bstack11lll11l11_opy_, bstack1111_opy_ (u"࠭ࡷࠨ๡")):
            pass
          with open(bstack11lll11l11_opy_, bstack1111_opy_ (u"ࠢࡸ࠭ࠥ๢")) as f:
            f.write(bstack1l11lll1_opy_)
          import subprocess
          bstack1ll1l1l111_opy_ = subprocess.run([bstack1111_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࠣ๣"), bstack11lll11l11_opy_])
          if os.path.exists(bstack11lll11l11_opy_):
            os.unlink(bstack11lll11l11_opy_)
          os._exit(bstack1ll1l1l111_opy_.returncode)
        else:
          if bstack1ll11llll_opy_(bstack1l1111l1l_opy_[bstack1111_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ๤")]):
            bstack1l1111l1l_opy_[bstack1111_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭๥")].remove(bstack1111_opy_ (u"ࠫ࠲ࡳࠧ๦"))
            bstack1l1111l1l_opy_[bstack1111_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ๧")].remove(bstack1111_opy_ (u"࠭ࡰࡥࡤࠪ๨"))
            bstack1l1111l1l_opy_[bstack1111_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ๩")] = bstack1l1111l1l_opy_[bstack1111_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ๪")][0]
          bstack1l111ll1l1_opy_(bstack1l1lllll1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1l1111l1l_opy_[bstack1111_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ๫")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1111_opy_ (u"ࠪࡣࡤࡴࡡ࡮ࡧࡢࡣࠬ๬")] = bstack1111_opy_ (u"ࠫࡤࡥ࡭ࡢ࡫ࡱࡣࡤ࠭๭")
          mod_globals[bstack1111_opy_ (u"ࠬࡥ࡟ࡧ࡫࡯ࡩࡤࡥࠧ๮")] = os.path.abspath(bstack1l1111l1l_opy_[bstack1111_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ๯")])
          exec(open(bstack1l1111l1l_opy_[bstack1111_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ๰")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1111_opy_ (u"ࠨࡅࡤࡹ࡬࡮ࡴࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠨ๱").format(str(e)))
          for driver in bstack1ll11111l1_opy_:
            bstack1l1llllll1_opy_.append({
              bstack1111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ๲"): bstack1l1111l1l_opy_[bstack1111_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭๳")],
              bstack1111_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ๴"): str(e),
              bstack1111_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ๵"): multiprocessing.current_process().name
            })
            bstack1l1lllll1l_opy_(driver, bstack1111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭๶"), bstack1111_opy_ (u"ࠢࡔࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥ๷") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1ll11111l1_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1l11l11ll1_opy_, CONFIG, logger)
      bstack1l1ll111_opy_()
      bstack111l1lll1l_opy_()
      percy.bstack111l1l11_opy_()
      bstack1l1lll111l_opy_ = {
        bstack1111_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ๸"): args[0],
        bstack1111_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩ๹"): CONFIG,
        bstack1111_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫ๺"): bstack11l1l1lll_opy_,
        bstack1111_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭๻"): bstack1l11l11ll1_opy_
      }
      if bstack1111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ๼") in CONFIG:
        bstack111l111ll_opy_ = bstack11l111l1ll_opy_(args, logger, CONFIG, bstack1111ll1l_opy_, bstack11llllll_opy_)
        bstack1ll11lll1l_opy_ = bstack111l111ll_opy_.bstack11lll1l1ll_opy_(run_on_browserstack, bstack1l1lll111l_opy_, bstack1ll11llll_opy_(args))
      else:
        if bstack1ll11llll_opy_(args):
          bstack1l1lll111l_opy_[bstack1111_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ๽")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1l1lll111l_opy_,))
          test.start()
          test.join()
        else:
          bstack1l111ll1l1_opy_(bstack1l1lllll1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1111_opy_ (u"ࠧࡠࡡࡱࡥࡲ࡫࡟ࡠࠩ๾")] = bstack1111_opy_ (u"ࠨࡡࡢࡱࡦ࡯࡮ࡠࡡࠪ๿")
          mod_globals[bstack1111_opy_ (u"ࠩࡢࡣ࡫࡯࡬ࡦࡡࡢࠫ຀")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1ll1llllll_opy_ == bstack1111_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩກ") or bstack1ll1llllll_opy_ == bstack1111_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪຂ"):
    percy.init(bstack1l11l11ll1_opy_, CONFIG, logger)
    percy.bstack111l1l11_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1lll11llll_opy_(e, bstack111l1l111_opy_)
    bstack1l1ll111_opy_()
    bstack1l111ll1l1_opy_(bstack1l11l11lll_opy_)
    if bstack1111ll1l_opy_:
      bstack1lll11111l_opy_(bstack1l11l11lll_opy_, args)
      if bstack1111_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ຃") in args:
        i = args.index(bstack1111_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫຄ"))
        args.pop(i)
        args.pop(i)
      if bstack1111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ຅") not in CONFIG:
        CONFIG[bstack1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫຆ")] = [{}]
        bstack11llllll_opy_ = 1
      if bstack1l1l11l1l_opy_ == 0:
        bstack1l1l11l1l_opy_ = 1
      args.insert(0, str(bstack1l1l11l1l_opy_))
      args.insert(0, str(bstack1111_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧງ")))
    if TestHubHandler.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack11ll1ll1l1_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack11ll1l111l_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack1111_opy_ (u"ࠥࡖࡔࡈࡏࡕࡡࡒࡔ࡙ࡏࡏࡏࡕࠥຈ"),
        ).parse_args(bstack11ll1ll1l1_opy_)
        bstack11l1lll1l_opy_ = args.index(bstack11ll1ll1l1_opy_[0]) if len(bstack11ll1ll1l1_opy_) > 0 else len(args)
        args.insert(bstack11l1lll1l_opy_, str(bstack1111_opy_ (u"ࠫ࠲࠳࡬ࡪࡵࡷࡩࡳ࡫ࡲࠨຉ")))
        args.insert(bstack11l1lll1l_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡸ࡯ࡣࡱࡷࡣࡱ࡯ࡳࡵࡧࡱࡩࡷ࠴ࡰࡺࠩຊ"))))
        if bstack11l111lll1_opy_.bstack11111l11_opy_(CONFIG):
          args.insert(bstack11l1lll1l_opy_, str(bstack1111_opy_ (u"࠭࠭࠮࡮࡬ࡷࡹ࡫࡮ࡦࡴࠪ຋")))
          args.insert(bstack11l1lll1l_opy_ + 1, str(bstack1111_opy_ (u"ࠧࡓࡧࡷࡶࡾࡌࡡࡪ࡮ࡨࡨ࠿ࢁࡽࠨຌ").format(bstack11l111lll1_opy_.bstack1ll11111ll_opy_(CONFIG))))
        if bstack11ll1l1l1l_opy_(os.environ.get(bstack1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓ࠭ຍ"))) and str(os.environ.get(bstack1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭ຎ"), bstack1111_opy_ (u"ࠪࡲࡺࡲ࡬ࠨຏ"))) != bstack1111_opy_ (u"ࠫࡳࡻ࡬࡭ࠩຐ"):
          for bstack111ll1l11l_opy_ in bstack11ll1l111l_opy_:
            args.remove(bstack111ll1l11l_opy_)
          test_files = os.environ.get(bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠩຑ")).split(bstack1111_opy_ (u"࠭ࠬࠨຒ"))
          for bstack111111ll_opy_ in test_files:
            args.append(bstack111111ll_opy_)
      except Exception as e:
        logger.error(bstack1111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡧࡴࡵࡣࡦ࡬࡮ࡴࡧࠡ࡮࡬ࡷࡹ࡫࡮ࡦࡴࠣࡪࡴࡸࠠࡼࡿ࠱ࠤࡊࡸࡲࡰࡴࠣ࠱ࠥࢁࡽࠣຓ").format(bstack1lll11l111_opy_, e))
    pabot.main(args)
  elif bstack1ll1llllll_opy_ == bstack1111_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩດ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1lll11llll_opy_(e, bstack111l1l111_opy_)
    for a in args:
      if bstack1111_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘࠨຕ") in a:
        bstack11l11ll1_opy_ = int(a.split(bstack1111_opy_ (u"ࠪ࠾ࠬຖ"))[1])
      if bstack1111_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨທ") in a:
        bstack111lllll1l_opy_ = str(a.split(bstack1111_opy_ (u"ࠬࡀࠧຘ"))[1])
      if bstack1111_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘ࠭ນ") in a:
        bstack1ll1l11l1_opy_ = str(a.split(bstack1111_opy_ (u"ࠧ࠻ࠩບ"))[1])
    bstack11ll1l11l_opy_ = None
    bstack11l1lllll_opy_ = None
    if bstack1111_opy_ (u"ࠨ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠧປ") in args:
      i = args.index(bstack1111_opy_ (u"ࠩ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠨຜ"))
      args.pop(i)
      bstack11ll1l11l_opy_ = args.pop(i)
    if bstack1111_opy_ (u"ࠪ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽ࠭ຝ") in args:
      i = args.index(bstack1111_opy_ (u"ࠫ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࠧພ"))
      args.pop(i)
      bstack11l1lllll_opy_ = args.pop(i)
    if bstack11ll1l11l_opy_ is not None:
      global bstack11ll1l1l1_opy_
      bstack11ll1l1l1_opy_ = bstack11ll1l11l_opy_
    if bstack11l1lllll_opy_ is not None and int(bstack11l11ll1_opy_) < 0:
      bstack11l11ll1_opy_ = int(bstack11l1lllll_opy_)
    if cli.is_enabled(CONFIG):
      if cli.bstack1lll1l1lll_opy_():
        bstack11l1lllll1_opy_.invoke(bstack1llll11l1_opy_.CONNECT, bstack11ll111l1_opy_())
        cli.bstack1llll1ll1_opy_(bstack11l11ll1_opy_)
      if cli.bstack1l11ll11l_opy_(bstack11111lll1_opy_):
        cli.bstack11l1lll11_opy_()
    bstack1l111ll1l1_opy_(bstack1l11l11lll_opy_)
    run_cli(args)
    if bstack1111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩຟ") in multiprocessing.current_process().__dict__.keys():
      for bstack1ll111lll_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1l1llllll1_opy_.append(bstack1ll111lll_opy_)
  elif bstack1ll1llllll_opy_ == bstack1111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ຠ"):
    bstack1lll1lll11_opy_ = bstack1l11l11111_opy_(args, logger, CONFIG, bstack1111ll1l_opy_)
    bstack1lll1lll11_opy_.bstack1ll11l1ll_opy_()
    bstack1l1ll111_opy_()
    bstack111lllll11_opy_ = True
    bstack1l1l111111_opy_ = bstack1lll1lll11_opy_.bstack1ll1lllll1_opy_()
    bstack1lll1lll11_opy_.bstack1l1lll111l_opy_(bstack1ll1llll1_opy_)
    bstack1lll1lll11_opy_.bstack1l11111l_opy_()
    bstack1l1111l111_opy_(bstack1ll1llllll_opy_, CONFIG, bstack1lll1lll11_opy_.bstack1l1ll1l11_opy_())
    bstack1ll1l11ll1_opy_.end(EVENTS.bstack11l11lllll_opy_.value, EVENTS.bstack11l11lllll_opy_.value + bstack1111_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢມ"), EVENTS.bstack11l11lllll_opy_.value + bstack1111_opy_ (u"ࠣ࠼ࡨࡲࡩࠨຢ"), status=True, failure=None, test_name=bstack1lll11ll1_opy_)
    bstack1l1l11l11l_opy_ = bstack1lll1lll11_opy_.bstack11lll1l1ll_opy_(bstack1lll1111_opy_, {
      bstack1111_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩຣ"): CONFIG,
      bstack1111_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫ຤"): bstack11l1l1lll_opy_,
      bstack1111_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ລ"): bstack1l11l11ll1_opy_,
      bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ຦"): bstack1111ll1l_opy_,
      bstack1111_opy_ (u"࠭ࡏࡗࡇࡕࡖࡎࡊࡅࡠࡎࡒࡅࡉࡥࡔࡆࡕࡗࡍࡓࡍࠧວ"): bstack11l1l11l11_opy_
    })
    if not bstack1l1111l1l_opy_:
      bstack1ll111l1ll_opy_ = bstack1l11l1ll_opy_.bstack11l111111_opy_(EVENTS.bstack1l11l111ll_opy_.value)
    try:
      bstack1l11llll1_opy_, bstack11lll1lll_opy_ = map(list, zip(*bstack1l1l11l11l_opy_))
      bstack1l1ll11lll_opy_ = bstack1l11llll1_opy_[0]
      for status_code in bstack11lll1lll_opy_:
        if status_code != 0:
          bstack1ll11l11_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack1111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡦࡼࡥࠡࡧࡵࡶࡴࡸࡳࠡࡣࡱࡨࠥࡹࡴࡢࡶࡸࡷࠥࡩ࡯ࡥࡧ࠱ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠ࠻ࠢࡾࢁࠧຨ").format(str(e)))
  elif bstack1ll1llllll_opy_ == bstack1111_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨຩ"):
    try:
      from behave.__main__ import main as bstack1l111lll1_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1lll11llll_opy_(e, bstack11ll1111ll_opy_)
    bstack1l1ll111_opy_()
    bstack111lllll11_opy_ = True
    bstack1111ll1ll_opy_ = 1
    if bstack1111_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩສ") in CONFIG:
      bstack1111ll1ll_opy_ = CONFIG[bstack1111_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪຫ")]
    if bstack1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧຬ") in CONFIG:
      bstack1111l11ll_opy_ = int(bstack1111ll1ll_opy_) * int(len(CONFIG[bstack1111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨອ")]))
    else:
      bstack1111l11ll_opy_ = int(bstack1111ll1ll_opy_)
    config = Configuration(args)
    bstack111ll111l_opy_ = config.paths
    if len(bstack111ll111l_opy_) == 0:
      import glob
      pattern = bstack1111_opy_ (u"࠭ࠪࠫ࠱࠭࠲࡫࡫ࡡࡵࡷࡵࡩࠬຮ")
      bstack1l1l11l1l1_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1l1l11l1l1_opy_)
      config = Configuration(args)
      bstack111ll111l_opy_ = config.paths
    bstack11llllll11_opy_ = [os.path.normpath(item) for item in bstack111ll111l_opy_]
    bstack11llll1l11_opy_ = [os.path.normpath(item) for item in args]
    bstack11lll111l_opy_ = [item for item in bstack11llll1l11_opy_ if item not in bstack11llllll11_opy_]
    import platform as pf
    if pf.system().lower() == bstack1111_opy_ (u"ࠧࡸ࡫ࡱࡨࡴࡽࡳࠨຯ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack11llllll11_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l1l1ll1_opy_)))
                    for bstack1l1l1ll1_opy_ in bstack11llllll11_opy_]
    bstack1l1ll11ll1_opy_ = []
    for spec in bstack11llllll11_opy_:
      bstack111ll1ll11_opy_ = []
      bstack111ll1ll11_opy_ += bstack11lll111l_opy_
      bstack111ll1ll11_opy_.append(spec)
      bstack1l1ll11ll1_opy_.append(bstack111ll1ll11_opy_)
    execution_items = []
    for bstack111ll1ll11_opy_ in bstack1l1ll11ll1_opy_:
      if bstack1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫະ") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack1111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬັ")]):
          item = {}
          item[bstack1111_opy_ (u"ࠪࡥࡷ࡭ࠧາ")] = bstack1111_opy_ (u"ࠫࠥ࠭ຳ").join(bstack111ll1ll11_opy_)
          item[bstack1111_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫິ")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack1111_opy_ (u"࠭ࡡࡳࡩࠪີ")] = bstack1111_opy_ (u"ࠧࠡࠩຶ").join(bstack111ll1ll11_opy_)
        item[bstack1111_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧື")] = 0
        execution_items.append(item)
    bstack1l11l11l1_opy_ = bstack11l1l11ll1_opy_(execution_items, bstack1111l11ll_opy_)
    for execution_item in bstack1l11l11l1_opy_:
      bstack11ll111lll_opy_ = []
      for item in execution_item:
        bstack11ll111lll_opy_.append(bstack1l11l1l11_opy_(name=str(item[bstack1111_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨຸ")]),
                                             target=bstack1111ll11_opy_,
                                             args=(item[bstack1111_opy_ (u"ࠪࡥࡷ࡭ູࠧ")],)))
      for t in bstack11ll111lll_opy_:
        t.start()
      for t in bstack11ll111lll_opy_:
        t.join()
  else:
    bstack1ll1ll11_opy_(bstack11lll11l1l_opy_)
  if not bstack1l1111l1l_opy_:
    bstack1ll1lll1_opy_()
    if bstack1ll111l1ll_opy_:
      bstack1l11l1ll_opy_.end(EVENTS.bstack1l11l111ll_opy_.value, bstack1ll111l1ll_opy_ + bstack1111_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷ຺ࠦ"), bstack1ll111l1ll_opy_ + bstack1111_opy_ (u"ࠧࡀࡥ࡯ࡦࠥົ"), status=True, failure=None, test_name=None)
  logger_utils.bstack1llll1111_opy_()
def browserstack_initialize(bstack1l1111111_opy_=None):
  logger.info(bstack1111_opy_ (u"࠭ࡒࡶࡰࡱ࡭ࡳ࡭ࠠࡔࡆࡎࠤࡼ࡯ࡴࡩࠢࡤࡶ࡬ࡹ࠺ࠡࠩຼ") + str(bstack1l1111111_opy_))
  run_on_browserstack(bstack1l1111111_opy_, None, True)
@measure(event_name=EVENTS.bstack1ll111ll1_opy_, stage=STAGE.bstack111l1lllll_opy_, bstack11ll1l11l1_opy_=bstack1lll11ll1_opy_)
def bstack1ll1lll1_opy_():
  global CONFIG
  global bstack1l1l11ll11_opy_
  global bstack1ll11l11_opy_
  global bstack111ll1l1ll_opy_
  global global_config
  global _1l1ll1ll11_opy_
  bstack111l1l1111_opy_.bstack11ll11ll1l_opy_()
  _1l1ll1ll11_opy_ = cli.is_running()
  if _1l1ll1ll11_opy_:
    bstack11l1lllll1_opy_.invoke(bstack1llll11l1_opy_.bstack1ll1lll1l1_opy_)
  else:
    bstack1l11111ll1_opy_ = bstack11l111lll1_opy_.get_instance(config=CONFIG)
    bstack1l11111ll1_opy_.bstack1lll11ll_opy_(CONFIG)
  hashed_id = None
  bstack1111llllll_opy_ = None
  def bstack11ll1lllll_opy_():
    try:
      if bstack1l1l11ll11_opy_ == bstack1111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧຽ"):
        if not cli.is_enabled(CONFIG):
          TestHubHandler.stop()
      else:
        TestHubHandler.stop()
    except Exception as e:
      logger.debug(bstack1111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡴࡶࡲࡴࡵ࡯࡮ࡨࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࢀࢃࠢ຾").format(e))
  def bstack11l1ll11ll_opy_():
    try:
      if not cli.is_enabled(CONFIG):
        bstack11l111ll11_opy_.bstack11l1111ll1_opy_()
    except Exception as e:
      logger.debug(bstack1111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡲࡵ࡭ࡳࡺࡩ࡯ࡩࠣࡦࡺ࡯࡬ࡥࠢ࡯࡭ࡳࡱ࠺ࠡࡽࢀࠦ຿").format(e))
  def bstack1llll11l1l_opy_():
    nonlocal hashed_id, bstack1111llllll_opy_
    try:
      if bstack1111_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧເ") in CONFIG and str(CONFIG[bstack1111_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨແ")]).lower() != bstack1111_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫໂ"):
        hashed_id, bstack1111llllll_opy_ = bstack11l1l11lll_opy_()
      else:
        hashed_id, bstack1111llllll_opy_ = get_build_link()
    except Exception as e:
      logger.debug(bstack1111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࠥࡲࡩ࡯࡭࠽ࠤࢀࢃࠢໃ").format(e))
  bstack111ll1ll_opy_ = threading.Thread(target=bstack11ll1lllll_opy_)
  bstack111l11l1ll_opy_ = threading.Thread(target=bstack11l1ll11ll_opy_)
  bstack11l1ll1l1l_opy_ = threading.Thread(target=bstack1llll11l1l_opy_)
  threads = [bstack111ll1ll_opy_, bstack111l11l1ll_opy_, bstack11l1ll1l1l_opy_]
  for thread in threads:
    try:
      thread.start()
    except Exception as e:
      logger.debug(bstack1111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡳࡵࡣࡵࡸ࡮ࡴࡧࠡࡶ࡫ࡶࡪࡧࡤࠡࡽࢀ࠾ࠥࢁࡽࠣໄ").format(thread.name, e))
  for thread in threads:
    try:
      thread.join()
    except Exception as e:
      logger.debug(bstack1111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠ࡫ࡱ࡬ࡲ࡮ࡴࡧࠡࡶ࡫ࡶࡪࡧࡤࠡࡽࢀ࠾ࠥࢁࡽࠣ໅").format(thread.name, e))
  bstack1l1l1l11ll_opy_(hashed_id)
  logger.info(bstack1111_opy_ (u"ࠩࡖࡈࡐࠦࡲࡶࡰࠣࡩࡳࡪࡥࡥࠢࡩࡳࡷࠦࡩࡥ࠼ࠪໆ") + global_config.get_property(bstack1111_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࠬ໇"), bstack1111_opy_ (u"່ࠫࠬ")) + bstack1111_opy_ (u"ࠬ࠲ࠠࡵࡧࡶࡸ࡭ࡻࡢࠡ࡫ࡧ࠾້ࠥ࠭") + os.getenv(bstack1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇ໊ࠫ"), bstack1111_opy_ (u"ࠧࠨ໋")))
  if hashed_id is not None and bstack11l1l1ll1l_opy_() != -1:
    sessions = bstack11l11l1l_opy_(hashed_id)
    bstack11l111l11l_opy_(sessions, bstack1111llllll_opy_)
  if bstack1l1l11ll11_opy_ == bstack1111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ໌") and bstack1ll11l11_opy_ != 0:
    sys.exit(bstack1ll11l11_opy_)
  if bstack1l1l11ll11_opy_ == bstack1111_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩໍ") and bstack111ll1l1ll_opy_ != 0:
    sys.exit(bstack111ll1l1ll_opy_)
def bstack1l1l1l11ll_opy_(new_id):
    global bstack111ll1111l_opy_
    bstack111ll1111l_opy_ = new_id
def bstack1l11l1111_opy_(bstack1111ll11l_opy_):
  if bstack1111ll11l_opy_:
    return bstack1111ll11l_opy_.capitalize()
  else:
    return bstack1111_opy_ (u"ࠪࠫ໎")
@measure(event_name=EVENTS.bstack11ll11l11l_opy_, stage=STAGE.bstack111l1lllll_opy_, bstack11ll1l11l1_opy_=bstack1lll11ll1_opy_)
def bstack11llll11l_opy_(bstack1l11l1lll1_opy_):
  if bstack1111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ໏") in bstack1l11l1lll1_opy_ and bstack1l11l1lll1_opy_[bstack1111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ໐")] != bstack1111_opy_ (u"࠭ࠧ໑"):
    return bstack1l11l1lll1_opy_[bstack1111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ໒")]
  else:
    bstack11ll1l11l1_opy_ = bstack1111_opy_ (u"ࠣࠤ໓")
    if bstack1111_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩ໔") in bstack1l11l1lll1_opy_ and bstack1l11l1lll1_opy_[bstack1111_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪ໕")] != None:
      bstack11ll1l11l1_opy_ += bstack1l11l1lll1_opy_[bstack1111_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫ໖")] + bstack1111_opy_ (u"ࠧ࠲ࠠࠣ໗")
      if bstack1l11l1lll1_opy_[bstack1111_opy_ (u"࠭࡯ࡴࠩ໘")] == bstack1111_opy_ (u"ࠢࡪࡱࡶࠦ໙"):
        bstack11ll1l11l1_opy_ += bstack1111_opy_ (u"ࠣ࡫ࡒࡗࠥࠨ໚")
      bstack11ll1l11l1_opy_ += (bstack1l11l1lll1_opy_[bstack1111_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭໛")] or bstack1111_opy_ (u"ࠪࠫໜ"))
      return bstack11ll1l11l1_opy_
    else:
      bstack11ll1l11l1_opy_ += bstack1l11l1111_opy_(bstack1l11l1lll1_opy_[bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬໝ")]) + bstack1111_opy_ (u"ࠧࠦࠢໞ") + (
              bstack1l11l1lll1_opy_[bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨໟ")] or bstack1111_opy_ (u"ࠧࠨ໠")) + bstack1111_opy_ (u"ࠣ࠮ࠣࠦ໡")
      if bstack1l11l1lll1_opy_[bstack1111_opy_ (u"ࠩࡲࡷࠬ໢")] == bstack1111_opy_ (u"࡛ࠥ࡮ࡴࡤࡰࡹࡶࠦ໣"):
        bstack11ll1l11l1_opy_ += bstack1111_opy_ (u"ࠦ࡜࡯࡮ࠡࠤ໤")
      bstack11ll1l11l1_opy_ += bstack1l11l1lll1_opy_[bstack1111_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ໥")] or bstack1111_opy_ (u"࠭ࠧ໦")
      return bstack11ll1l11l1_opy_
@measure(event_name=EVENTS.bstack11ll1ll11l_opy_, stage=STAGE.bstack111l1lllll_opy_, bstack11ll1l11l1_opy_=bstack1lll11ll1_opy_)
def bstack11l1ll1111_opy_(bstack1ll111llll_opy_):
  if bstack1ll111llll_opy_ == bstack1111_opy_ (u"ࠢࡥࡱࡱࡩࠧ໧"):
    return bstack1111_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽࡫ࡷ࡫ࡥ࡯࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥ࡫ࡷ࡫ࡥ࡯ࠤࡁࡇࡴࡳࡰ࡭ࡧࡷࡩࡩࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫ໨")
  elif bstack1ll111llll_opy_ == bstack1111_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ໩"):
    return bstack1111_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡸࡥࡥ࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡶࡪࡪࠢ࠿ࡈࡤ࡭ࡱ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭໪")
  elif bstack1ll111llll_opy_ == bstack1111_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ໫"):
    return bstack1111_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡨࡴࡨࡩࡳࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡨࡴࡨࡩࡳࠨ࠾ࡑࡣࡶࡷࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ໬")
  elif bstack1ll111llll_opy_ == bstack1111_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ໭"):
    return bstack1111_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡵࡩࡩࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡳࡧࡧࠦࡃࡋࡲࡳࡱࡵࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩ໮")
  elif bstack1ll111llll_opy_ == bstack1111_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤ໯"):
    return bstack1111_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࠨ࡫ࡥࡢ࠵࠵࠺ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࠣࡦࡧࡤ࠷࠷࠼ࠢ࠿ࡖ࡬ࡱࡪࡵࡵࡵ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ໰")
  elif bstack1ll111llll_opy_ == bstack1111_opy_ (u"ࠥࡶࡺࡴ࡮ࡪࡰࡪࠦ໱"):
    return bstack1111_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡢ࡭ࡣࡦ࡯ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡢ࡭ࡣࡦ࡯ࠧࡄࡒࡶࡰࡱ࡭ࡳ࡭࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ໲")
  else:
    return bstack1111_opy_ (u"ࠬࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡤ࡯ࡥࡨࡱ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡤ࡯ࡥࡨࡱࠢ࠿ࠩ໳") + bstack1l11l1111_opy_(
      bstack1ll111llll_opy_) + bstack1111_opy_ (u"࠭࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ໴")
def bstack111111111_opy_(session):
  return bstack1111_opy_ (u"ࠧ࠽ࡶࡵࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡷࡵࡷࠣࡀ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠲ࡴࡡ࡮ࡧࠥࡂࡁࡧࠠࡩࡴࡨࡪࡂࠨࡻࡾࠤࠣࡸࡦࡸࡧࡦࡶࡀࠦࡤࡨ࡬ࡢࡰ࡮ࠦࡃࢁࡽ࠽࠱ࡤࡂࡁ࠵ࡴࡥࡀࡾࢁࢀࢃ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾࠲ࡸࡷࡄࠧ໵").format(
    session[bstack1111_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣࡠࡷࡵࡰࠬ໶")], bstack11llll11l_opy_(session), bstack11l1ll1111_opy_(session[bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡵࡷࡥࡹࡻࡳࠨ໷")]),
    bstack11l1ll1111_opy_(session[bstack1111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ໸")]),
    bstack1l11l1111_opy_(session[bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬ໹")] or session[bstack1111_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬ໺")] or bstack1111_opy_ (u"࠭ࠧ໻")) + bstack1111_opy_ (u"ࠢࠡࠤ໼") + (session[bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪ໽")] or bstack1111_opy_ (u"ࠩࠪ໾")),
    session[bstack1111_opy_ (u"ࠪࡳࡸ࠭໿")] + bstack1111_opy_ (u"ࠦࠥࠨༀ") + session[bstack1111_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ༁")], session[bstack1111_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨ༂")] or bstack1111_opy_ (u"ࠧࠨ༃"),
    session[bstack1111_opy_ (u"ࠨࡥࡵࡩࡦࡺࡥࡥࡡࡤࡸࠬ༄")] if session[bstack1111_opy_ (u"ࠩࡦࡶࡪࡧࡴࡦࡦࡢࡥࡹ࠭༅")] else bstack1111_opy_ (u"ࠪࠫ༆"))
@measure(event_name=EVENTS.bstack1ll1l1l1ll_opy_, stage=STAGE.bstack111l1lllll_opy_, bstack11ll1l11l1_opy_=bstack1lll11ll1_opy_)
def bstack11l111l11l_opy_(sessions, bstack1111llllll_opy_):
  try:
    bstack11ll11ll_opy_ = bstack1111_opy_ (u"ࠦࠧ༇")
    if not os.path.exists(bstack1ll111l1_opy_):
      os.mkdir(bstack1ll111l1_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1111_opy_ (u"ࠬࡧࡳࡴࡧࡷࡷ࠴ࡸࡥࡱࡱࡵࡸ࠳࡮ࡴ࡮࡮ࠪ༈")), bstack1111_opy_ (u"࠭ࡲࠨ༉")) as f:
      bstack11ll11ll_opy_ = f.read()
    bstack11ll11ll_opy_ = bstack11ll11ll_opy_.replace(bstack1111_opy_ (u"ࠧࡼࠧࡕࡉࡘ࡛ࡌࡕࡕࡢࡇࡔ࡛ࡎࡕࠧࢀࠫ༊"), str(len(sessions)))
    bstack11ll11ll_opy_ = bstack11ll11ll_opy_.replace(bstack1111_opy_ (u"ࠨࡽࠨࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠫࡽࠨ་"), bstack1111llllll_opy_)
    bstack11ll11ll_opy_ = bstack11ll11ll_opy_.replace(bstack1111_opy_ (u"ࠩࡾࠩࡇ࡛ࡉࡍࡆࡢࡒࡆࡓࡅࠦࡿࠪ༌"),
                                              sessions[0].get(bstack1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡱࡥࡲ࡫ࠧ།")) if sessions[0] else bstack1111_opy_ (u"ࠫࠬ༎"))
    with open(os.path.join(bstack1ll111l1_opy_, bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡷ࡫ࡰࡰࡴࡷ࠲࡭ࡺ࡭࡭ࠩ༏")), bstack1111_opy_ (u"࠭ࡷࠨ༐")) as stream:
      stream.write(bstack11ll11ll_opy_.split(bstack1111_opy_ (u"ࠧࡼࠧࡖࡉࡘ࡙ࡉࡐࡐࡖࡣࡉࡇࡔࡂࠧࢀࠫ༑"))[0])
      for session in sessions:
        stream.write(bstack111111111_opy_(session))
      stream.write(bstack11ll11ll_opy_.split(bstack1111_opy_ (u"ࠨࡽࠨࡗࡊ࡙ࡓࡊࡑࡑࡗࡤࡊࡁࡕࡃࠨࢁࠬ༒"))[1])
    logger.info(bstack1111_opy_ (u"ࠩࡊࡩࡳ࡫ࡲࡢࡶࡨࡨࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡧࡻࡩ࡭ࡦࠣࡥࡷࡺࡩࡧࡣࡦࡸࡸࠦࡡࡵࠢࡾࢁࠬ༓").format(bstack1ll111l1_opy_));
  except Exception as e:
    logger.debug(bstack11l111ll1_opy_.format(str(e)))
def bstack11l11l1l_opy_(hashed_id):
  global CONFIG
  try:
    bstack1l1llll111_opy_ = datetime.datetime.now()
    host = bstack1111_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠮ࡥ࡯ࡳࡺࡪ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ༔") if bstack1111_opy_ (u"ࠫࡦࡶࡰࠨ༕") in CONFIG else bstack1111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡱ࡫࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭༖")
    user = CONFIG[bstack1111_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ༗")]
    key = CONFIG[bstack1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻ༘ࠪ")]
    bstack1l11lll111_opy_ = bstack1111_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫༙ࠧ") if bstack1111_opy_ (u"ࠩࡤࡴࡵ࠭༚") in CONFIG else (bstack1111_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧ༛") if CONFIG.get(bstack1111_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨ༜")) else bstack1111_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ༝"))
    host = bstack11111l1ll_opy_(cli.config, [bstack1111_opy_ (u"ࠨࡡࡱ࡫ࡶࠦ༞"), bstack1111_opy_ (u"ࠢࡢࡲࡳࡅࡺࡺ࡯࡮ࡣࡷࡩࠧ༟"), bstack1111_opy_ (u"ࠣࡣࡳ࡭ࠧ༠")], host) if bstack1111_opy_ (u"ࠩࡤࡴࡵ࠭༡") in CONFIG else bstack11111l1ll_opy_(cli.config, [bstack1111_opy_ (u"ࠥࡥࡵ࡯ࡳࠣ༢"), bstack1111_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸࡪࠨ༣"), bstack1111_opy_ (u"ࠧࡧࡰࡪࠤ༤")], host)
    url = bstack1111_opy_ (u"࠭ࡻࡾ࠱ࡾࢁ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽ࠰ࡵࡨࡷࡸ࡯࡯࡯ࡵ࠱࡮ࡸࡵ࡮ࠨ༥").format(host, bstack1l11lll111_opy_, hashed_id)
    headers = {
      bstack1111_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭༦"): bstack1111_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ༧"),
    }
    proxies = bstack11111ll1_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies, auth=(user, key))
    if response.json():
      cli.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺ࡨࡧࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࡥ࡬ࡪࡵࡷࠦ༨"), datetime.datetime.now() - bstack1l1llll111_opy_)
      return list(map(lambda session: session[bstack1111_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ༩")], response.json()))
  except Exception as e:
    logger.debug(bstack1111l111_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack11ll111ll1_opy_, stage=STAGE.bstack111l1lllll_opy_, bstack11ll1l11l1_opy_=bstack1lll11ll1_opy_)
def get_build_link():
  global CONFIG
  global bstack111ll1111l_opy_
  try:
    if bstack1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ༪") in CONFIG:
      bstack1l1llll111_opy_ = datetime.datetime.now()
      host = bstack1111_opy_ (u"ࠬࡧࡰࡪ࠯ࡦࡰࡴࡻࡤࠨ༫") if bstack1111_opy_ (u"࠭ࡡࡱࡲࠪ༬") in CONFIG else bstack1111_opy_ (u"ࠧࡢࡲ࡬ࠫ༭")
      user = CONFIG[bstack1111_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ༮")]
      key = CONFIG[bstack1111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ༯")]
      bstack1l11lll111_opy_ = bstack1111_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩ༰") if bstack1111_opy_ (u"ࠫࡦࡶࡰࠨ༱") in CONFIG else bstack1111_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ༲")
      url = bstack1111_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡼࡿ࠽ࡿࢂࡆࡻࡾ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠯࡬ࡶࡳࡳ࠭༳").format(user, key, host, bstack1l11lll111_opy_)
      if cli.is_enabled(CONFIG):
        bstack1111llllll_opy_, hashed_id = cli.bstack1ll1lll1l_opy_()
        logger.info(bstack111llllll_opy_.format(bstack1111llllll_opy_))
        return [hashed_id, bstack1111llllll_opy_]
      else:
        headers = {
          bstack1111_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭༴"): bstack1111_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱ༵ࠫ"),
        }
        if bstack1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ༶") in CONFIG:
          params = {bstack1111_opy_ (u"ࠪࡲࡦࡳࡥࠨ༷"): CONFIG[bstack1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ༸")], bstack1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ༹"): CONFIG[bstack1111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ༺")]}
        else:
          params = {bstack1111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ༻"): CONFIG[bstack1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ༼")]}
        proxies = bstack11111ll1_opy_(CONFIG, url)
        response = requests.get(url, params=params, headers=headers, proxies=proxies)
        if response.json():
          bstack1lllll1l11_opy_ = response.json()[0][bstack1111_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡢࡶ࡫࡯ࡨࠬ༽")]
          if bstack1lllll1l11_opy_:
            bstack1111llllll_opy_ = bstack1lllll1l11_opy_[bstack1111_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥࡢࡹࡷࡲࠧ༾")].split(bstack1111_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦ࠱ࡧࡻࡩ࡭ࡦࠪ༿"))[0] + bstack1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡷ࠴࠭ཀ") + bstack1lllll1l11_opy_[
              bstack1111_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩཁ")]
            logger.info(bstack111llllll_opy_.format(bstack1111llllll_opy_))
            bstack111ll1111l_opy_ = bstack1lllll1l11_opy_[bstack1111_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪག")]
            bstack1l1ll1llll_opy_ = CONFIG[bstack1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫགྷ")]
            if bstack1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫང") in CONFIG:
              bstack1l1ll1llll_opy_ += bstack1111_opy_ (u"ࠪࠤࠬཅ") + CONFIG[bstack1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ཆ")]
            if bstack1l1ll1llll_opy_ != bstack1lllll1l11_opy_[bstack1111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪཇ")]:
              logger.debug(bstack11lll1ll_opy_.format(bstack1lllll1l11_opy_[bstack1111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ཈")], bstack1l1ll1llll_opy_))
            cli.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠢࡩࡶࡷࡴ࠿࡭ࡥࡵࡡࡥࡹ࡮ࡲࡤࡠ࡮࡬ࡲࡰࠨཉ"), datetime.datetime.now() - bstack1l1llll111_opy_)
            return [bstack1lllll1l11_opy_[bstack1111_opy_ (u"ࠨࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫཊ")], bstack1111llllll_opy_]
    else:
      logger.warning(bstack111ll111ll_opy_)
  except Exception as e:
    logger.debug(bstack1l11ll1ll1_opy_.format(str(e)))
  return [None, None]
def bstack1l11l1l1ll_opy_(url, bstack11lllll1l_opy_=False):
  global CONFIG
  global bstack111ll1l1_opy_
  if not bstack111ll1l1_opy_:
    hostname = bstack11l111l11_opy_(url)
    is_private = bstack11l11llll_opy_(hostname)
    if (bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ཋ") in CONFIG and not bstack11ll1l1l1l_opy_(CONFIG[bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧཌ")])) and (is_private or bstack11lllll1l_opy_):
      bstack111ll1l1_opy_ = hostname
def bstack11l111l11_opy_(url):
  return urlparse(url).hostname
def bstack11l11llll_opy_(hostname):
  for bstack111l11lll_opy_ in bstack1ll1ll1111_opy_:
    regex = re.compile(bstack111l11lll_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1l111l111l_opy_(bstack111lllllll_opy_):
  return True if bstack111lllllll_opy_ in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack11l11l1lll_opy_, stage=STAGE.bstack111l1lllll_opy_, bstack11ll1l11l1_opy_=bstack1lll11ll1_opy_)
def getAccessibilityResults(driver):
  global CONFIG
  global bstack11l11ll1_opy_
  bstack11lll11ll1_opy_ = not (bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨཌྷ"), None) and bstack1lll11lll1_opy_(
          threading.current_thread(), bstack1111_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫཎ"), None))
  bstack1lllll1l1_opy_ = getattr(driver, bstack1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭ཏ"), None) != True
  bstack1l11111lll_opy_ = bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧཐ"), None) and bstack1lll11lll1_opy_(
          threading.current_thread(), bstack1111_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪད"), None)
  if bstack1l11111lll_opy_:
    if not bstack1ll111111_opy_():
      logger.warning(bstack1111_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡴࡵࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡂࡲࡳࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷ࠳ࠨདྷ"))
      return {}
    logger.debug(bstack1111_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡲࡦࡵࡸࡰࡹࡹࠧན"))
    logger.debug(perform_scan(driver, driver_command=bstack1111_opy_ (u"ࠫࡪࡾࡥࡤࡷࡷࡩࡘࡩࡲࡪࡲࡷࠫཔ")))
    results = bstack1l1ll1l1_opy_(bstack1111_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸࡸࠨཕ"))
    if results is not None and results.get(bstack1111_opy_ (u"ࠨࡩࡴࡵࡸࡩࡸࠨབ")) is not None:
        return results[bstack1111_opy_ (u"ࠢࡪࡵࡶࡹࡪࡹࠢབྷ")]
    logger.error(bstack1111_opy_ (u"ࠣࡐࡲࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡗ࡫ࡳࡶ࡮ࡷࡷࠥࡽࡥࡳࡧࠣࡪࡴࡻ࡮ࡥ࠰ࠥམ"))
    return []
  if not bstack11l1111111_opy_.bstack111ll1lll1_opy_(CONFIG, bstack11l11ll1_opy_) or (bstack1lllll1l1_opy_ and bstack11lll11ll1_opy_):
    logger.warning(bstack1111_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶ࠲ࠧཙ"))
    return {}
  try:
    logger.debug(bstack1111_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡲࡦࡵࡸࡰࡹࡹࠧཚ"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack1l111l111_opy_.bstack1l1llll11_opy_)
    return results
  except Exception:
    logger.error(bstack1111_opy_ (u"ࠦࡓࡵࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡹࡨࡶࡪࠦࡦࡰࡷࡱࡨ࠳ࠨཛ"))
    return {}
@measure(event_name=EVENTS.bstack11l1lll1l1_opy_, stage=STAGE.bstack111l1lllll_opy_, bstack11ll1l11l1_opy_=bstack1lll11ll1_opy_)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack11l11ll1_opy_
  bstack11lll11ll1_opy_ = not (bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩཛྷ"), None) and bstack1lll11lll1_opy_(
          threading.current_thread(), bstack1111_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬཝ"), None))
  bstack1lllll1l1_opy_ = getattr(driver, bstack1111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧཞ"), None) != True
  bstack1l11111lll_opy_ = bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨཟ"), None) and bstack1lll11lll1_opy_(
          threading.current_thread(), bstack1111_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫའ"), None)
  if bstack1l11111lll_opy_:
    if not bstack1ll111111_opy_():
      logger.warning(bstack1111_opy_ (u"ࠥࡒࡴࡺࠠࡢࡰࠣࡅࡵࡶࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࠡࡃࡳࡴࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡳࡶ࡯ࡰࡥࡷࡿ࠮ࠣཡ"))
      return {}
    logger.debug(bstack1111_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡢࡦࡨࡲࡶࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡳࡧࡶࡹࡱࡺࡳࠡࡵࡸࡱࡲࡧࡲࡺࠩར"))
    logger.debug(perform_scan(driver, driver_command=bstack1111_opy_ (u"ࠬ࡫ࡸࡦࡥࡸࡸࡪ࡙ࡣࡳ࡫ࡳࡸࠬལ")))
    results = bstack1l1ll1l1_opy_(bstack1111_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹ࡙ࡵ࡮࡯ࡤࡶࡾࠨཤ"))
    if results is not None and results.get(bstack1111_opy_ (u"ࠢࡴࡷࡰࡱࡦࡸࡹࠣཥ")) is not None:
        return results[bstack1111_opy_ (u"ࠣࡵࡸࡱࡲࡧࡲࡺࠤས")]
    logger.error(bstack1111_opy_ (u"ࠤࡑࡳࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡘࡥࡴࡷ࡯ࡸࡸࠦࡓࡶ࡯ࡰࡥࡷࡿࠠࡸࡣࡶࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦཧ"))
    return {}
  if not bstack11l1111111_opy_.bstack111ll1lll1_opy_(CONFIG, bstack11l11ll1_opy_) or (bstack1lllll1l1_opy_ and bstack11lll11ll1_opy_):
    logger.warning(bstack1111_opy_ (u"ࠥࡒࡴࡺࠠࡢࡰࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡹࡵ࡮࡯ࡤࡶࡾ࠴ࠢཨ"))
    return {}
  try:
    logger.debug(bstack1111_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡢࡦࡨࡲࡶࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡳࡧࡶࡹࡱࡺࡳࠡࡵࡸࡱࡲࡧࡲࡺࠩཀྵ"))
    logger.debug(perform_scan(driver))
    bstack1l1111l1l1_opy_ = driver.execute_async_script(bstack1l111l111_opy_.bstack1ll1llll_opy_)
    return bstack1l1111l1l1_opy_
  except Exception:
    logger.error(bstack1111_opy_ (u"ࠧࡔ࡯ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡸࡱࡲࡧࡲࡺࠢࡺࡥࡸࠦࡦࡰࡷࡱࡨ࠳ࠨཪ"))
    return {}
def bstack1ll111111_opy_():
  global CONFIG
  global bstack11l11ll1_opy_
  bstack1lll11ll1l_opy_ = bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ཫ"), None) and bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩཬ"), None)
  if not bstack11l1111111_opy_.bstack111ll1lll1_opy_(CONFIG, bstack11l11ll1_opy_) or not bstack1lll11ll1l_opy_:
        logger.warning(bstack1111_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡳࡴࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡲࡦࡵࡸࡰࡹࡹ࠮ࠣ཭"))
        return False
  return True
def bstack1l1ll1l1_opy_(result_type):
    bstack1ll111ll1l_opy_ = TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack11l111ll11_opy_.current_hook_uuid()
    with ThreadPoolExecutor() as executor:
        future = executor.submit(bstack11lllll1l1_opy_(bstack1ll111ll1l_opy_, result_type))
        try:
            return future.result(timeout=bstack111l11111l_opy_)
        except TimeoutError:
            logger.error(bstack1111_opy_ (u"ࠤࡗ࡭ࡲ࡫࡯ࡶࡶࠣࡥ࡫ࡺࡥࡳࠢࡾࢁࡸࠦࡷࡩ࡫࡯ࡩࠥ࡬ࡥࡵࡥ࡫࡭ࡳ࡭ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡓࡧࡶࡹࡱࡺࡳࠣ཮").format(bstack111l11111l_opy_))
        except Exception as ex:
            logger.debug(bstack1111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡵࡩࡹࡸࡩࡦࡸ࡬ࡲ࡬ࠦࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡼࡿ࠱ࠤࡊࡸࡲࡰࡴࠣ࠱ࠥࢁࡽࠣ཯").format(result_type, str(ex)))
    return {}
@measure(event_name=EVENTS.bstack11l11lll_opy_, stage=STAGE.bstack111l1lllll_opy_, bstack11ll1l11l1_opy_=bstack1lll11ll1_opy_)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack11l11ll1_opy_
  bstack11lll11ll1_opy_ = not (bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ཰"), None) and bstack1lll11lll1_opy_(
          threading.current_thread(), bstack1111_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰཱࠫ"), None))
  bstack1lll1l1ll_opy_ = not (bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹི࠭"), None) and bstack1lll11lll1_opy_(
          threading.current_thread(), bstack1111_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ཱིࠩ"), None))
  bstack1lllll1l1_opy_ = getattr(driver, bstack1111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨུ"), None) != True
  if not bstack11l1111111_opy_.bstack111ll1lll1_opy_(CONFIG, bstack11l11ll1_opy_) or (bstack1lllll1l1_opy_ and bstack11lll11ll1_opy_ and bstack1lll1l1ll_opy_):
    logger.warning(bstack1111_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡸࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡣࡢࡰ࠱ཱུࠦ"))
    return {}
  try:
    bstack11ll1ll111_opy_ = bstack1111_opy_ (u"ࠪࡥࡵࡶࠧྲྀ") in CONFIG and CONFIG.get(bstack1111_opy_ (u"ࠫࡦࡶࡰࠨཷ"), bstack1111_opy_ (u"ࠬ࠭ླྀ"))
    session_id = getattr(driver, bstack1111_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠪཹ"), None)
    if not session_id:
      logger.warning(bstack1111_opy_ (u"ࠢࡏࡱࠣࡷࡪࡹࡳࡪࡱࡱࠤࡎࡊࠠࡧࡱࡸࡲࡩࠦࡦࡰࡴࠣࡨࡷ࡯ࡶࡦࡴེࠥ"))
      return {bstack1111_opy_ (u"ࠣࡧࡵࡶࡴࡸཻࠢ"): bstack1111_opy_ (u"ࠤࡑࡳࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡉࡅࠢࡩࡳࡺࡴࡤོࠣ")}
    if bstack11ll1ll111_opy_:
      try:
        bstack1lll1lll1l_opy_ = {
              bstack1111_opy_ (u"ࠪࡸ࡭ࡐࡷࡵࡖࡲ࡯ࡪࡴཽࠧ"): os.environ.get(bstack1111_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩཾ"), os.environ.get(bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩཿ"), bstack1111_opy_ (u"ྀ࠭ࠧ"))),
              bstack1111_opy_ (u"ࠧࡵࡪࡗࡩࡸࡺࡒࡶࡰࡘࡹ࡮ࡪཱྀࠧ"): TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack11l111ll11_opy_.current_hook_uuid(),
              bstack1111_opy_ (u"ࠨࡣࡸࡸ࡭ࡎࡥࡢࡦࡨࡶࠬྂ"): os.environ.get(bstack1111_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧྃ")),
              bstack1111_opy_ (u"ࠪࡷࡨࡧ࡮ࡕ࡫ࡰࡩࡸࡺࡡ࡮ࡲ྄ࠪ"): str(int(datetime.datetime.now().timestamp() * 1000)),
              bstack1111_opy_ (u"ࠫࡹ࡮ࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ྅"): os.environ.get(bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ྆"), bstack1111_opy_ (u"࠭ࠧ྇")),
              bstack1111_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪࠧྈ"): kwargs.get(bstack1111_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࡠࡥࡲࡱࡲࡧ࡮ࡥࠩྉ"), None) or bstack1111_opy_ (u"ࠩࠪྊ")
          }
        if not hasattr(thread_local, bstack1111_opy_ (u"ࠪࡦࡦࡹࡥࡠࡣࡳࡴࡤࡧ࠱࠲ࡻࡢࡷࡨࡸࡩࡱࡶࠪྋ")):
            scripts = {bstack1111_opy_ (u"ࠫࡸࡩࡡ࡯ࠩྌ"): bstack1l111l111_opy_.perform_scan}
            thread_local.base_app_a11y_script = scripts
        bstack11111llll_opy_ = copy.deepcopy(thread_local.base_app_a11y_script)
        bstack11111llll_opy_[bstack1111_opy_ (u"ࠬࡹࡣࡢࡰࠪྍ")] = bstack11111llll_opy_[bstack1111_opy_ (u"࠭ࡳࡤࡣࡱࠫྎ")] % json.dumps(bstack1lll1lll1l_opy_)
        bstack1l111l111_opy_.bstack11ll1111l_opy_(bstack11111llll_opy_)
        bstack1l111l111_opy_.store()
        bstack1l11111l11_opy_ = driver.execute_script(bstack1l111l111_opy_.perform_scan)
      except Exception as bstack11l111lll_opy_:
        logger.info(bstack1111_opy_ (u"ࠢࡂࡲࡳ࡭ࡺࡳࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡥࡤࡲࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࠢྏ") + str(bstack11l111lll_opy_))
        bstack1l11111l11_opy_ = {bstack1111_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢྐ"): str(bstack11l111lll_opy_)}
    else:
      bstack1l11111l11_opy_ = driver.execute_async_script(bstack1l111l111_opy_.perform_scan, {bstack1111_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࠩྑ"): kwargs.get(bstack1111_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࡢࡧࡴࡳ࡭ࡢࡰࡧࠫྒ"), None) or bstack1111_opy_ (u"ࠫࠬྒྷ")})
    return bstack1l11111l11_opy_
  except Exception as err:
    logger.error(bstack1111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡴࡸࡲࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡣࡢࡰ࠱ࠤࢀࢃࠢྔ").format(str(err)))
    return {}