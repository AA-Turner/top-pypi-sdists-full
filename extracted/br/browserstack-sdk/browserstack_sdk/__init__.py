# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
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
from browserstack_sdk.sdk_cli.bstack1111ll1l11_opy_ import bstack1l111l11_opy_
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from browserstack_sdk.bstack1llll1111l_opy_ import bstack11lll1lll1_opy_
from browserstack_sdk.bstack11ll11ll1_opy_ import *
import time
import requests
from bstack_utils.constants import EVENTS, STAGE, bstack11lll1lll_opy_
from bstack_utils.messages import bstack1l1ll111l_opy_, bstack11111ll1l_opy_, bstack111l1l1l1l_opy_, bstack1ll1ll11ll_opy_, bstack1l11l1lll_opy_, bstack1ll111lll1_opy_
from bstack_utils.measure import measure
from bstack_utils.logger_utils import get_logger
from bstack_utils.helper import bstack1l1111111l_opy_
from browserstack_sdk.bstack1l11ll1l11_opy_ import bstack1ll1111lll_opy_
logger = get_logger(__name__)
def bstack1lll111l1_opy_():
  global CONFIG
  headers = {
        bstack111ll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack111ll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1l1111111l_opy_(CONFIG, bstack11lll1lll_opy_)
  try:
    response = requests.get(bstack11lll1lll_opy_, headers=headers, proxies=proxies, timeout=2)
    if response.json():
      bstack11ll111ll_opy_ = response.json()[bstack111ll_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1l1ll111l_opy_.format(response.json()))
      return bstack11ll111ll_opy_
    else:
      logger.debug(bstack11111ll1l_opy_.format(bstack111ll_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack11111ll1l_opy_.format(e))
def bstack111ll11l_opy_(hub_url):
  global CONFIG
  url = bstack111ll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack111ll_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack111ll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack111ll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1l1111111l_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=(0.5, 1.0))
    latency = time.perf_counter() - start_time
    logger.debug(bstack111l1l1l1l_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1ll1ll11ll_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack1111ll1l_opy_, stage=STAGE.bstack1l1l11l1l_opy_)
def bstack11l111llll_opy_():
  try:
    global bstack11111l1111_opy_
    global CONFIG
    if bstack111ll_opy_ (u"ࠫ࡭ࡻࡢࡓࡧࡪ࡭ࡴࡴࠧࡾ") in CONFIG and CONFIG[bstack111ll_opy_ (u"ࠬ࡮ࡵࡣࡔࡨ࡫࡮ࡵ࡮ࠨࡿ")]:
      from bstack_utils.constants import bstack1l11ll1lll_opy_
      bstack1l1lll1l11_opy_ = CONFIG[bstack111ll_opy_ (u"࠭ࡨࡶࡤࡕࡩ࡬࡯࡯࡯ࠩࢀ")]
      if bstack1l1lll1l11_opy_ in bstack1l11ll1lll_opy_:
        bstack11111l1111_opy_ = bstack1l11ll1lll_opy_[bstack1l1lll1l11_opy_]
        logger.debug(bstack1l11l1lll_opy_.format(bstack11111l1111_opy_))
        _1ll1l1ll1l_opy_([], bstack11111l1111_opy_, None)
        return
      else:
        logger.debug(bstack111ll_opy_ (u"ࠢࡉࡷࡥࠤࡰ࡫ࡹࠡࠩࡾࢁࠬࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࡎࡕࡃࡡࡘࡖࡑࡥࡍࡂࡒ࠯ࠤ࡫ࡧ࡬࡭࡫ࡱ࡫ࠥࡨࡡࡤ࡭ࠣࡸࡴࠦ࡯ࡱࡶ࡬ࡱࡦࡲࠠࡩࡷࡥࠤࡩ࡫ࡴࡦࡥࡷ࡭ࡴࡴࠢࢁ").format(bstack1l1lll1l11_opy_))
    bstack11ll111ll_opy_ = bstack1lll111l1_opy_()
    from concurrent.futures import ThreadPoolExecutor, as_completed
    if bstack11ll111ll_opy_:
        with ThreadPoolExecutor(max_workers=len(bstack11ll111ll_opy_)) as executor:
            bstack1lll1ll11l_opy_ = {executor.submit(bstack111ll11l_opy_, bstack111111l11_opy_): bstack111111l11_opy_ for bstack111111l11_opy_ in bstack11ll111ll_opy_}
            for future in as_completed(bstack1lll1ll11l_opy_):
                result = future.result()
                if result and result.get(bstack111ll_opy_ (u"ࠨ࡮ࡤࡸࡪࡴࡣࡺࠩࢂ")) is not None:
                    bstack11111l1111_opy_ = result[bstack111ll_opy_ (u"ࠩ࡫ࡹࡧࡥࡵࡳ࡮ࠪࢃ")]
                    logger.debug(bstack1l11l1lll_opy_.format(bstack11111l1111_opy_))
                    _1ll1l1ll1l_opy_(bstack11ll111ll_opy_, result[bstack111ll_opy_ (u"ࠪ࡬ࡺࡨ࡟ࡶࡴ࡯ࠫࢄ")], result[bstack111ll_opy_ (u"ࠫࡱࡧࡴࡦࡰࡦࡽࠬࢅ")])
                    return
        bstack11111l1111_opy_ = bstack11ll111ll_opy_[0]
        logger.debug(bstack1l11l1lll_opy_.format(bstack11111l1111_opy_))
        _1ll1l1ll1l_opy_(bstack11ll111ll_opy_, bstack11ll111ll_opy_[0], None)
        return
  except Exception as e:
    logger.debug(bstack1ll111lll1_opy_.format(e))
def _1ll1l1ll1l_opy_(bstack11ll111ll_opy_, bstack11lll1l1l1_opy_, latency):
  bstack111ll_opy_ (u"ࠧࠨࠢࡔࡶࡲࡶࡪࠦࡨࡶࡤࠣࡥࡱࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠠࡥࡣࡷࡥࠥ࡬࡯ࡳࠢ࡬ࡲࡸࡺࡲࡶ࡯ࡨࡲࡹࡧࡴࡪࡱࡱ࠲ࠥࡉࡡ࡭࡮ࡨࡨࠥ࡯࡮ࡵࡧࡵࡲࡦࡲ࡬ࡺࠢࡤࡪࡹ࡫ࡲࠡࡪࡸࡦࠥࡹࡥ࡭ࡧࡦࡸ࡮ࡵ࡮࠯ࠤࠥࠦࢆ")
  try:
    from bstack_utils.config import Config
    global_config = Config.bstack1l1l11ll1_opy_()
    data = {
      bstack111ll_opy_ (u"࠭࡮ࡦࡣࡵࡩࡸࡺࡈࡶࡤࡶࠫࢇ"): [bstack111ll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤ࢈") + bstack111111l11_opy_ for bstack111111l11_opy_ in bstack11ll111ll_opy_],
      bstack111ll_opy_ (u"ࠨࡵࡨࡰࡪࡩࡴࡦࡦࡋࡹࡧ࠭ࢉ"): bstack111ll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦࢊ") + bstack11lll1l1l1_opy_,
      bstack111ll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ࢋ"): int(time.time() * 1000)
    }
    if latency is not None:
      data[bstack111ll_opy_ (u"ࠫ࡭ࡻࡢࡍࡣࡷࡩࡳࡩࡩࡦࡵࠪࢌ")] = {bstack111ll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢࢍ") + bstack11lll1l1l1_opy_: latency}
      data[bstack111ll_opy_ (u"࠭ࡳࡦ࡮ࡨࡧࡹ࡫ࡤࡉࡷࡥࡐࡦࡺࡥ࡯ࡥࡼࠫࢎ")] = latency
    global_config.bstack1l1l1llll1_opy_(bstack111ll_opy_ (u"ࠧࡠࡪࡸࡦࡆࡲ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࡅࡣࡷࡥࠬ࢏"), data)
    logger.debug(bstack111ll_opy_ (u"ࠣࡊࡸࡦࠥࡧ࡬࡭ࡱࡦࡥࡹ࡯࡯࡯ࠢࡧࡥࡹࡧࠠࡴࡶࡲࡶࡪࡪ࠺ࠡࡽࢀࠦ࢐").format(data))
  except Exception as e:
    logger.debug(bstack111ll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡵࡷࡳࡷ࡯࡮ࡨࠢ࡫ࡹࡧࠦࡡ࡭࡮ࡲࡧࡦࡺࡩࡰࡰࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧ࢑").format(e))
from browserstack_sdk.bstack1lllllll1_opy_ import *
from browserstack_sdk.bstack1l1l1111ll_opy_ import bstack1ll1l111l1_opy_
from browserstack_sdk.bstack1l11ll1l11_opy_ import *
from browserstack_sdk.bstack11l111ll1l_opy_ import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.logger_utils import get_logger
from bstack_utils.measure import measure
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack1111l111l_opy_, stage=STAGE.bstack1l1l11l1l_opy_)
def bstack11ll1111_opy_():
    global bstack11111l1111_opy_
    try:
        bstack111l1111_opy_ = bstack1ll111lll_opy_()
        bstack1lll1l11l_opy_(bstack111l1111_opy_)
        hub_url = bstack111l1111_opy_.get(bstack111ll_opy_ (u"ࠥࡹࡷࡲࠢ࢒"), bstack111ll_opy_ (u"ࠦࠧ࢓"))
        if hub_url.endswith(bstack111ll_opy_ (u"ࠬ࠵ࡷࡥ࠱࡫ࡹࡧ࠭࢔")):
            hub_url = hub_url.rsplit(bstack111ll_opy_ (u"࠭࠯ࡸࡦ࠲࡬ࡺࡨࠧ࢕"), 1)[0]
        if hub_url.startswith(bstack111ll_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࠨ࢖")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack111ll_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࠪࢗ")):
            hub_url = hub_url[8:]
        bstack11111l1111_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack1ll111lll_opy_():
    global CONFIG
    bstack111l1l1lll_opy_ = CONFIG.get(bstack111ll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭࢘"), {}).get(bstack111ll_opy_ (u"ࠪ࡫ࡷ࡯ࡤࡏࡣࡰࡩ࢙ࠬ"), bstack111ll_opy_ (u"ࠫࡓࡕ࡟ࡈࡔࡌࡈࡤࡔࡁࡎࡇࡢࡔࡆ࡙ࡓࡆࡆ࢚ࠪ"))
    if not isinstance(bstack111l1l1lll_opy_, str):
        raise ValueError(bstack111ll_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡌࡸࡩࡥࠢࡱࡥࡲ࡫ࠠ࡮ࡷࡶࡸࠥࡨࡥࠡࡣࠣࡺࡦࡲࡩࡥࠢࡶࡸࡷ࡯࡮ࡨࠤ࢛"))
    try:
        bstack111l1111_opy_ = bstack111lll1111_opy_(bstack111l1l1lll_opy_)
        return bstack111l1111_opy_
    except Exception as e:
        logger.error(bstack111ll_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡩࡵ࡭ࡩࠦࡤࡦࡶࡤ࡭ࡱࡹࠠ࠻ࠢࡾࢁࠧ࢜").format(str(e)))
        return {}
def bstack111lll1111_opy_(bstack111l1l1lll_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack111ll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ࢝")] or not CONFIG[bstack111ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ࢞")]:
            raise ValueError(bstack111ll_opy_ (u"ࠤࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠤࡴࡸࠠࡢࡥࡦࡩࡸࡹࠠ࡬ࡧࡼࠦ࢟"))
        url = bstack1111l11l11_opy_ + bstack111l1l1lll_opy_
        auth = (CONFIG[bstack111ll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࢠ")], CONFIG[bstack111ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧࢡ")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack1ll1l1lll1_opy_ = json.loads(response.text)
            return bstack1ll1l1lll1_opy_
    except ValueError as ve:
        logger.error(bstack111ll_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡩࡵ࡭ࡩࠦࡤࡦࡶࡤ࡭ࡱࡹࠠ࠻ࠢࡾࢁࠧࢢ").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack111ll_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡪࡶ࡮ࡪࠠࡥࡧࡷࡥ࡮ࡲࡳࠡ࠼ࠣࡿࢂࠨࢣ").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack1lll1l11l_opy_(bstack11ll111ll1_opy_):
    global CONFIG
    if bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫࢤ") not in CONFIG or str(CONFIG[bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬࢥ")]).lower() == bstack111ll_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨࢦ"):
        CONFIG[bstack111ll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩࢧ")] = False
    elif bstack111ll_opy_ (u"ࠫ࡮ࡹࡔࡳ࡫ࡤࡰࡌࡸࡩࡥࠩࢨ") in bstack11ll111ll1_opy_:
        bstack1l1l1ll1_opy_ = CONFIG.get(bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢩ"), {})
        logger.debug(bstack111ll_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡸࡪࡵࡷ࡭ࡳ࡭ࠠ࡭ࡱࡦࡥࡱࠦ࡯ࡱࡶ࡬ࡳࡳࡹ࠺ࠡࠧࡶࠦࢪ"), bstack1l1l1ll1_opy_)
        bstack1ll1111l11_opy_ = bstack11ll111ll1_opy_.get(bstack111ll_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡒࡦࡲࡨࡥࡹ࡫ࡲࡴࠤࢫ"), [])
        bstack1l1ll11lll_opy_ = bstack111ll_opy_ (u"ࠣ࠮ࠥࢬ").join(bstack1ll1111l11_opy_)
        logger.debug(bstack111ll_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡅࡸࡷࡹࡵ࡭ࠡࡴࡨࡴࡪࡧࡴࡦࡴࠣࡷࡹࡸࡩ࡯ࡩ࠽ࠤࠪࡹࠢࢭ"), bstack1l1ll11lll_opy_)
        bstack1llll111ll_opy_ = {
            bstack111ll_opy_ (u"ࠥࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧࢮ"): bstack111ll_opy_ (u"ࠦࡦࡺࡳ࠮ࡴࡨࡴࡪࡧࡴࡦࡴࠥࢯ"),
            bstack111ll_opy_ (u"ࠧ࡬࡯ࡳࡥࡨࡐࡴࡩࡡ࡭ࠤࢰ"): bstack111ll_opy_ (u"ࠨࡴࡳࡷࡨࠦࢱ"),
            bstack111ll_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࠭ࡳࡧࡳࡩࡦࡺࡥࡳࠤࢲ"): bstack1l1ll11lll_opy_
        }
        bstack1l1l1ll1_opy_.update(bstack1llll111ll_opy_)
        logger.debug(bstack111ll_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡖࡲࡧࡥࡹ࡫ࡤࠡ࡮ࡲࡧࡦࡲࠠࡰࡲࡷ࡭ࡴࡴࡳ࠻ࠢࠨࡷࠧࢳ"), bstack1l1l1ll1_opy_)
        CONFIG[bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢴ")] = bstack1l1l1ll1_opy_
        logger.debug(bstack111ll_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡉ࡭ࡳࡧ࡬ࠡࡅࡒࡒࡋࡏࡇ࠻ࠢࠨࡷࠧࢵ"), CONFIG)
def get_turboscale_playwright_url():
    bstack111l1111_opy_ = bstack1ll111lll_opy_()
    if not bstack111l1111_opy_[bstack111ll_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡖࡴ࡯ࠫࢶ")]:
      raise ValueError(bstack111ll_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡗࡵࡰࠥ࡯ࡳࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡩࡶࡴࡳࠠࡨࡴ࡬ࡨࠥࡪࡥࡵࡣ࡬ࡰࡸ࠴ࠢࢷ"))
    return bstack111l1111_opy_[bstack111ll_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡘࡶࡱ࠭ࢸ")] + bstack111ll_opy_ (u"ࠧࡀࡥࡤࡴࡸࡃࠧࢹ")
@measure(event_name=EVENTS.bstack11l11lll11_opy_, stage=STAGE.bstack1l1l11l1l_opy_)
def bstack11l1lll1ll_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack111ll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪࢺ")], CONFIG[bstack111ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬࢻ")])
        url = bstack1lll1l11_opy_
        logger.debug(bstack111ll_opy_ (u"ࠥࡅࡹࡺࡥ࡮ࡲࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴࠢࡩࡶࡴࡳࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡔࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠣࡅࡕࡏࠢࢼ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack111ll_opy_ (u"ࠦࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠥࢽ"): bstack111ll_opy_ (u"ࠧࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠣࢾ")})
            if response.status_code == 200:
                bstack1l1l111l1_opy_ = json.loads(response.text)
                bstack1l1l111ll_opy_ = bstack1l1l111l1_opy_.get(bstack111ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡸ࠭ࢿ"), [])
                if bstack1l1l111ll_opy_:
                    bstack1111111l1l_opy_ = bstack1l1l111ll_opy_[0]
                    build_hashed_id = bstack1111111l1l_opy_.get(bstack111ll_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪࣀ"))
                    bstack1llll1ll1_opy_ = bstack1lll11111_opy_ + build_hashed_id
                    result.extend([build_hashed_id, bstack1llll1ll1_opy_])
                    logger.info(bstack1l1ll1l111_opy_.format(bstack1llll1ll1_opy_))
                    bstack11l1lll111_opy_ = CONFIG[bstack111ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫࣁ")]
                    if bstack111ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣂ") in CONFIG:
                      bstack11l1lll111_opy_ += bstack111ll_opy_ (u"ࠪࠤࠬࣃ") + CONFIG[bstack111ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࣄ")]
                    if bstack11l1lll111_opy_ != bstack1111111l1l_opy_.get(bstack111ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪࣅ")):
                      logger.debug(bstack1lll11ll1l_opy_.format(bstack1111111l1l_opy_.get(bstack111ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫࣆ")), bstack11l1lll111_opy_))
                    return result
                else:
                    logger.debug(bstack111ll_opy_ (u"ࠢࡂࡖࡖࠤ࠿ࠦࡎࡰࠢࡥࡹ࡮ࡲࡤࡴࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠱ࠦࣇ"))
            else:
                logger.debug(bstack111ll_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴ࠰ࠥࣈ"))
        except Exception as e:
            logger.error(bstack111ll_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࡶࠤ࠿ࠦࡻࡾࠤࣉ").format(str(e)))
    else:
        logger.debug(bstack111ll_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡆࡓࡓࡌࡉࡈࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡶࡩࡹ࠴ࠠࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴ࠰ࠥ࣊"))
    return [None, None]
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack11ll1l11_opy_ import bstack11ll1l11_opy_, Events, bstack1l1l1lllll_opy_, bstack1ll11l1l11_opy_
from bstack_utils.measure import bstack11ll1l1l_opy_
from bstack_utils.measure import measure
from bstack_utils.percy import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack11l111l1_opy_ import bstack1111l1lll_opy_
from bstack_utils.messages import *
from bstack_utils import logger_utils
from bstack_utils.constants import *
from bstack_utils.helper import bstack11111lll11_opy_, bstack1ll11l11l_opy_, bstack11l1llll1l_opy_, bstack1ll11l1ll1_opy_, \
  bstack11l1ll1l_opy_, \
  Notset, is_robot_playwright_installed, bstack11lll11lll_opy_, \
  bstack1l1l1l1l11_opy_, bstack1llll111l_opy_, bstack11l1ll1ll1_opy_, bstack1l11ll1111_opy_, bstack11l1ll1l1_opy_, bstack1ll11ll11l_opy_, \
  bstack111l1111ll_opy_, \
  bstack1111lll1l_opy_, bstack1llllll111_opy_, bstack11lllll111_opy_, bstack1111111ll_opy_, \
  bstack111ll1ll1_opy_, bstack111l11111_opy_, bstack1lllll11ll1_opy_, bstack11ll11l111_opy_, bstack11l1l111ll_opy_
from bstack_utils.bstack11l1lll1l1_opy_ import bstack1ll1l1ll11_opy_
from bstack_utils.bstack11ll11lll_opy_ import bstack11lll1111l_opy_, bstack1l1111l1l1_opy_
from bstack_utils.bstack1ll1ll1lll_opy_ import bstack1llll1l111_opy_
from bstack_utils.bstack11111l1ll1_opy_ import bstack11ll1l1l1_opy_, bstack1lllll111_opy_
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.bstack11l1l1l11l_opy_ import bstack1l1l111l1l_opy_
from bstack_utils.proxy import bstack111lllll1_opy_, bstack1l1111111l_opy_, bstack1lll1111ll_opy_, bstack111lll111_opy_
from bstack_utils.bstack11l1111l11_opy_ import bstack11l11ll1l_opy_, bstack1l1llll1l1_opy_
import bstack_utils.bstack1l1l1lll_opy_ as TestHubUtils
import bstack_utils.bstack11ll111l_opy_ as bstack1l1lll11l1_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.utils.bstack1l1llllll_opy_ import bstack1l11111ll_opy_
from bstack_utils.bstack111llll111_opy_ import bstack1ll11l1l_opy_
from bstack_utils.bstack1lll1llll1_opy_ import bstack111l1ll11l_opy_
from bstack_utils.bstack11ll1l1l_opy_ import bstack111l1l1l_opy_
if os.getenv(bstack111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡉࡑࡒࡏࡘ࠭࣋")):
  cli.bstack111lllll11_opy_()
else:
  os.environ[bstack111ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡊࡒࡓࡐ࡙ࠧ࣌")] = bstack111ll_opy_ (u"࠭ࡴࡳࡷࡨࠫ࣍")
bstack1lllll1l11_opy_ = bstack111ll_opy_ (u"ࠧࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠠࠡ࡫ࡩࠬࡵࡧࡧࡦࠢࡀࡁࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠠࡼ࡞ࡱࠤࠥࠦࡴࡳࡻࡾࡠࡳࠦࡣࡰࡰࡶࡸࠥ࡬ࡳࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࡡ࠭ࡦࡴ࡞ࠪ࠭ࡀࡢ࡮ࠡࠢࠣࠤࠥ࡬ࡳ࠯ࡣࡳࡴࡪࡴࡤࡇ࡫࡯ࡩࡘࡿ࡮ࡤࠪࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠬࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡳࡣ࡮ࡴࡤࡦࡺࠬࠤ࠰ࠦࠢ࠻ࠤࠣ࠯ࠥࡐࡓࡐࡐ࠱ࡷࡹࡸࡩ࡯ࡩ࡬ࡪࡾ࠮ࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࠬࡦࡽࡡࡪࡶࠣࡲࡪࡽࡐࡢࡩࡨ࠶࠳࡫ࡶࡢ࡮ࡸࡥࡹ࡫ࠨࠣࠪࠬࠤࡂࡄࠠࡼࡿࠥ࠰ࠥࡢࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡨࡧࡷࡗࡪࡹࡳࡪࡱࡱࡈࡪࡺࡡࡪ࡮ࡶࠦࢂࡢࠧࠪࠫࠬ࡟ࠧ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠣ࡟ࠬࠤ࠰ࠦࠢ࠭࡞࡟ࡲࠧ࠯࡜࡯ࠢࠣࠤࠥࢃࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡽ࡝ࡰࠣࠤ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠧ࣎")
LAUNCH_PATCH_ROBOT_PLAYWRIGHT = bstack111ll_opy_ (u"ࠨ࡞ࡱ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࡢ࡮ࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠻࡝ࠡ࠿ࡀࡁࠥࡢࠧࡵࡴࡸࡩࡡ࠭࡜࡯ࡥࡲࡲࡸࡺࠠࡣࡵࡷࡥࡨࡱ࡟ࡱࡣࡷ࡬ࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴࡟࡟ࡲࡨࡵ࡮ࡴࡶࠣࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࡝ࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠵ࡢࡢ࡮ࡤࡱࡱࡷࡹࠦࡰࡠ࡫ࡱࡨࡪࡾࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠵ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠵࡟ࠣࡁࡂࡃࠠ࡝ࠩࡷࡶࡺ࡫࡜ࠨ࡞ࡱࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡷࡱ࡯ࡣࡦࠪ࠳࠰ࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠵ࠪ࡞ࡱࡧࡴࡴࡳࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣࠫ࠾ࡠࡳࡩ࡯࡯ࡵࡷࠤࡴࡸࡩࡨ࡫ࡱࡥࡱࡥࡣࡩࡴࡲࡱ࡮ࡻ࡭ࡠ࡮ࡤࡹࡳࡩࡨࠡ࠿ࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡰࡦࡻ࡮ࡤࡪ࠱ࡦ࡮ࡴࡤࠩ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭ࠪ࠽࡟ࡲ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡱࡧࡵ࡯ࡥ࡫ࠤࡂࠦࡡࡴࡻࡱࡧࠥ࠮࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸ࠯ࠠ࠾ࡀࠣࡿࡡࡴࡩࡧࠢࠫࠥࡧࡹࡴࡢࡥ࡮ࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠪࠢࡾࡠࡳࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦ࡯ࡳ࡫ࡪ࡭ࡳࡧ࡬ࡠࡥ࡫ࡶࡴࡳࡩࡶ࡯ࡢࡰࡦࡻ࡮ࡤࡪࠫࡰࡦࡻ࡮ࡤࡪࡒࡴࡹ࡯࡯࡯ࡵࠬ࠿ࡡࡴࡽ࡝ࡰ࡯ࡩࡹࠦࡣࡢࡲࡶ࠿ࡡࡴࡴࡳࡻࠣࡿࡡࡴࡣࡢࡲࡶࠤࡂࠦࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠪ࡞ࡱࠤࠥࢃࠠࡤࡣࡷࡧ࡭࠮ࡥࡹࠫࠣࡿࡡࡴࠠࠡࠢࠣࢁࡡࡴࠠࠡ࡫ࡩࠤ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࠮ࠦࡻ࡝ࡰࠣࠤࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡩ࡯࡯ࡰࡨࡧࡹࡕࡶࡦࡴࡆࡈࡕ࠮ࡻ࡝ࡰࠣࠤࠥࠦࠠࠡࡧࡱࡨࡵࡵࡩ࡯ࡶࡘࡖࡑࡀࠠࡡࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠧࡿࡪࡴࡣࡰࡦࡨ࡙ࡗࡏࡃࡰ࡯ࡳࡳࡳ࡫࡮ࡵࠪࡍࡗࡔࡔ࠮ࡴࡶࡵ࡭ࡳ࡭ࡩࡧࡻࠫࡧࡦࡶࡳࠪࠫࢀࡤ࠱ࡢ࡮ࠡࠢࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴ࡞ࡱࠤࠥࠦࠠࡾࠫ࡟ࡲࠥࠦࡽ࡝ࡰࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࠻ࠢࡣࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠩࢁࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭ࢂࡦࠬ࡝ࡰࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴ࡞ࡱࠤࠥࢃࠩ࡝ࡰࢀࡠࡳࡩ࡯࡯ࡵࡷࠤࡴࡸࡩࡨ࡫ࡱࡥࡱࡥࡣࡰࡰࡱࡩࡨࡺࠠ࠾ࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱ࠮ࡤࡪࡵࡳࡲ࡯ࡵ࡮࠰ࡦࡳࡳࡴࡥࡤࡶ࠱ࡦ࡮ࡴࡤࠩ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭ࠪ࠽࡟ࡲ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡨࡵ࡮࡯ࡧࡦࡸࠥࡃࠠࡢࡵࡼࡲࡨࠦࠨࡤࡱࡱࡲࡪࡩࡴࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁ࡜࡯ࠢࠣ࡭࡫ࠦࠨࠢࡤࡶࡸࡦࡩ࡫ࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠮ࠦࡻ࡝ࡰࠣࠤࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥࡵࡲࡪࡩ࡬ࡲࡦࡲ࡟ࡤࡱࡱࡲࡪࡩࡴࠩࡥࡲࡲࡳ࡫ࡣࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠫ࠾ࡠࡳࠦࠠࡾ࡞ࡱࠤࠥࡲࡥࡵࠢࡦࡥࡵࡹ࠻࡝ࡰࠣࠤࡹࡸࡹࠡࡽ࡟ࡲࠥࠦࠠࠡࡥࡤࡴࡸࠦ࠽ࠡࡌࡖࡓࡓ࠴ࡰࡢࡴࡶࡩ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡩࡡࡱࡵࠬࡠࡳࠦࠠࡾࠢࡦࡥࡹࡩࡨࠩࡧࡻ࠭ࠥࢁ࡜࡯ࠢࠣࢁࡡࡴࠠࠡࡥࡲࡲࡸࡺࠠ࡮ࡱࡧ࡭࡫࡯ࡥࡥࡇࡱࡨࡵࡵࡩ࡯ࡶࠣࡁࠥࡦࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࡡࠢ࠮ࠤࡪࡴࡣࡰࡦࡨ࡙ࡗࡏࡃࡰ࡯ࡳࡳࡳ࡫࡮ࡵࠪࡍࡗࡔࡔ࠮ࡴࡶࡵ࡭ࡳ࡭ࡩࡧࡻࠫࡧࡦࡶࡳࠪࠫ࠾ࡠࡳࠦࠠࡪࡨࠣࠬࡧࡹࡴࡢࡥ࡮ࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ࠭ࠥࢁ࡜࡯ࠢࠣࠤࠥࡸࡥࡵࡷࡵࡲࠥࡧࡷࡢ࡫ࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡨࡵ࡮࡯ࡧࡦࡸࡔࡼࡥࡳࡅࡇࡔ࠭ࢁ࡜࡯ࠢࠣࠤࠥࠦࠠࡦࡰࡧࡴࡴ࡯࡮ࡵࡗࡕࡐ࠿ࠦ࡭ࡰࡦ࡬ࡪ࡮࡫ࡤࡆࡰࡧࡴࡴ࡯࡮ࡵ࠮࡟ࡲࠥࠦࠠࠡࠢࠣ࠲࠳࠴ࡣࡰࡰࡱࡩࡨࡺࡏࡱࡶ࡬ࡳࡳࡹ࡜࡯ࠢࠣࠤࠥࢃࠩ࡝ࡰࠣࠤࢂࡢ࡮ࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤ࠳࠴࠮ࡤࡱࡱࡲࡪࡩࡴࡐࡲࡷ࡭ࡴࡴࡳ࠭࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࡝ࡰࠣࠤࢂ࠯࡜࡯ࡿ࡟ࡲࡱ࡫ࡴࠡࡄࡵࡳࡼࡹࡥࡳࡅࡲࡲࡹ࡫ࡸࡵ࠽࡟ࡲࡹࡸࡹࠡࡽ࡟ࡲࠥࠦࡣࡰࡰࡶࡸࠥࡶࡡࡵࡪࡐࡳࡩࡻ࡬ࡦࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭ࠨࡰࡢࡶ࡫ࠦ࠮ࡁ࡜࡯ࠢࠣࡧࡴࡴࡳࡵࠢࡳࡻࡈࡵࡲࡦࡒࡤࡸ࡭ࠦ࠽ࠡࡲࡤࡸ࡭ࡓ࡯ࡥࡷ࡯ࡩ࠳ࡪࡩࡳࡰࡤࡱࡪ࠮ࡲࡦࡳࡸ࡭ࡷ࡫࠮ࡳࡧࡶࡳࡱࡼࡥࠩࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠳ࡣࡰࡴࡨ࠳ࡵࡧࡣ࡬ࡣࡪࡩ࠳ࡰࡳࡰࡰࠥ࠭࠮ࡁ࡜࡯ࠢࠣࡆࡷࡵࡷࡴࡧࡵࡇࡴࡴࡴࡦࡺࡷࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨࡱࡣࡷ࡬ࡒࡵࡤࡶ࡮ࡨ࠲࡯ࡵࡩ࡯ࠪࡳࡻࡈࡵࡲࡦࡒࡤࡸ࡭࠲ࠠࠣ࡮࡬ࡦ࠴ࡩ࡬ࡪࡧࡱࡸ࠴ࡨࡲࡰࡹࡶࡩࡷࡉ࡯࡯ࡶࡨࡼࡹࠨࠩࠪ࠰ࡅࡶࡴࡽࡳࡦࡴࡆࡳࡳࡺࡥࡹࡶ࠾ࡠࡳࢃࠠࡤࡣࡷࡧ࡭ࠦࠨࡦࠫࠣࡿࡡࡴࠠࠡࡥࡲࡲࡸࡵ࡬ࡦ࠰ࡺࡥࡷࡴࠨࠣࡅࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡱࡵࡡࡥࠢࡅࡶࡴࡽࡳࡦࡴࡆࡳࡳࡺࡥࡹࡶࠣࡪࡷࡵ࡭ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠲ࡩ࡯ࡳࡧ࠽ࠦ࠱ࠦࡥ࠯࡯ࡨࡷࡸࡧࡧࡦࠫ࠾ࡠࡳࢃ࡜࡯ࡥࡲࡲࡸࡺࠠࡰࡴ࡬࡫࡮ࡴࡡ࡭ࡡࡱࡩࡼࡖࡡࡨࡧࠣࡁࠥࡈࡲࡰࡹࡶࡩࡷࡉ࡯࡯ࡶࡨࡼࡹ࠴ࡰࡳࡱࡷࡳࡹࡿࡰࡦ࠰ࡱࡩࡼࡖࡡࡨࡧ࠾ࡠࡳࡈࡲࡰࡹࡶࡩࡷࡉ࡯࡯ࡶࡨࡼࡹ࠴ࡰࡳࡱࡷࡳࡹࡿࡰࡦ࠰ࡱࡩࡼࡖࡡࡨࡧࠣࡁࠥࡧࡳࡺࡰࡦࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠮ࠩࠡࡽ࡟ࡲࠥࠦࡩࡧࠢࠫࡦࡸࡺࡡࡤ࡭ࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠬࠤࢀࡢ࡮ࠡࠢࠣࠤࡹࡸࡹࠡࡽ࡟ࡲࠥࠦࠠࠡࠢࠣࡧࡴࡴࡳࡵࠢࡥࡶࡴࡽࡳࡦࡴࠣࡁࠥࡺࡨࡪࡵ࠱ࡦࡷࡵࡷࡴࡧࡵࠤࠫࠬࠠࡵࡪ࡬ࡷ࠳ࡨࡲࡰࡹࡶࡩࡷ࠮ࠩ࠼࡞ࡱࠤࠥࠦࠠࠡࠢ࡯ࡩࡹࠦࡰࡳ࡫ࡰࡥࡷࡿࡃࡰࡰࡷࡩࡽࡺࠠ࠾ࠢࡥࡶࡴࡽࡳࡦࡴࠣࠪࠫࠦࡴࡺࡲࡨࡳ࡫ࠦࡢࡳࡱࡺࡷࡪࡸ࠮ࡤࡱࡱࡸࡪࡾࡴࡴࠢࡀࡁࡂࠦ࡜ࠨࡨࡸࡲࡨࡺࡩࡰࡰ࡟ࠫࠥࡅࠠࡣࡴࡲࡻࡸ࡫ࡲ࠯ࡥࡲࡲࡹ࡫ࡸࡵࡵࠫ࠭ࡠ࠶࡝ࠡ࠼ࠣࡲࡺࡲ࡬࠼࡞ࡱࠤࠥࠦࠠࠡࠢ࡬ࡪࠥ࠮ࠡࡱࡴ࡬ࡱࡦࡸࡹࡄࡱࡱࡸࡪࡾࡴࠡࠨࠩࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࠬࠦࠡࡶࡼࡴࡪࡵࡦࠡࡤࡵࡳࡼࡹࡥࡳ࠰ࡱࡩࡼࡉ࡯࡯ࡶࡨࡼࡹࠦ࠽࠾࠿ࠣࡠࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡜ࠨࠫࠣࡿࡡࡴࠠࠡࠢࠣࠤࠥࠦࠠࡱࡴ࡬ࡱࡦࡸࡹࡄࡱࡱࡸࡪࡾࡴࠡ࠿ࠣࡥࡼࡧࡩࡵࠢࡥࡶࡴࡽࡳࡦࡴ࠱ࡲࡪࡽࡃࡰࡰࡷࡩࡽࡺࠨࠪ࠽࡟ࡲࠥࠦࠠࠡࠢࠣࢁࡡࡴࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡵࡷࠤࡹࡧࡲࡨࡧࡷࡇࡴࡴࡴࡦࡺࡷࠤࡂࠦࡰࡳ࡫ࡰࡥࡷࡿࡃࡰࡰࡷࡩࡽࡺࠠࡽࡾࠣࡸ࡭࡯ࡳ࠼࡞ࡱࠤࠥࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡲࡪࡽࡐࡢࡩࡨ࠲ࡨࡧ࡬࡭ࠪࡷࡥࡷ࡭ࡥࡵࡅࡲࡲࡹ࡫ࡸࡵࠫ࠾ࡠࡳࠦࠠࠡࠢࢀࠤࡨࡧࡴࡤࡪࠣࠬࡪ࠯ࠠࡼ࡞ࡱࠤࠥࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡲࡪࡽࡐࡢࡩࡨ࠲ࡨࡧ࡬࡭ࠪࡷ࡬࡮ࡹࠩ࠼࡞ࡱࠤࠥࠦࠠࡾ࡞ࡱࠤࠥࢃࠠ࡝ࡰࠣࠤࡪࡲࡳࡦࠢࡾࡠࡳࠦࠠࠡࠢࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣࡳࡷ࡯ࡧࡪࡰࡤࡰࡤࡴࡥࡸࡒࡤ࡫ࡪ࠴ࡣࡢ࡮࡯ࠬࡹ࡮ࡩࡴࠫ࠾ࡠࡳࠦࠠࡾ࡞ࡱࢁࡀࡢ࡮࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱࡟ࡲ࣏ࠬ")
from ._version import __version__
bstack1llllll1l1l_opy_ = None
CONFIG = {}
bstack1lllll1l11l_opy_ = {}
bstack1l1l1111l_opy_ = {}
bstack1l11l11l1l_opy_ = None
bstack1l11l11ll1_opy_ = None
SESSION_NAME = None
PLATFORM_INDEX = -1
bstack1ll11ll1ll_opy_ = 0
bstack111llllll_opy_ = bstack1l11l1lll1_opy_
bstack1ll11llll1_opy_ = 1
PARALLELISE_VANILLA_PYTHON = False
PARALLELISE_THREADING_PYTHON = False
FRAMEWORK_NAME = bstack111ll_opy_ (u"࣐ࠩࠪ")
bstack1lllllll1l_opy_ = bstack111ll_opy_ (u"࣑ࠪࠫ")
bstack1l11111ll1_opy_ = False
BROWSERSTACK_AUTOMATION = True
bstack111111lll_opy_ = False
bstack1l1l1llll_opy_ = bstack111ll_opy_ (u"࣒ࠫࠬ")
bstack11l1l1l1l1_opy_ = []
bstack1111ll1lll_opy_ = threading.Lock()
bstack11l11llll1_opy_ = threading.Lock()
bstack11l11l1ll1_opy_ = None
bstack11111l1111_opy_ = bstack111ll_opy_ (u"࣓ࠬ࠭")
SELENIUM_OR_PLAYWRIGHT_INSTALLED = False
bstack1ll1l111ll_opy_ = None
bstack11l1111lll_opy_ = None
bstack111llll1_opy_ = None
bstack11l11ll111_opy_ = -1
bstack1l1l1ll1l1_opy_ = os.path.join(os.path.expanduser(bstack111ll_opy_ (u"࠭ࡾࠨࣔ")), bstack111ll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧࣕ"), bstack111ll_opy_ (u"ࠨ࠰ࡵࡳࡧࡵࡴ࠮ࡴࡨࡴࡴࡸࡴ࠮ࡪࡨࡰࡵ࡫ࡲ࠯࡬ࡶࡳࡳ࠭ࣖ"))
bstack11llll1l1l_opy_ = 0
bstack111ll1l11_opy_ = 0
bstack1ll11l1l1l_opy_ = []
bstack1111l1111l_opy_ = []
ROBOT_PYTHON_ERRORS = []
bstack11l1llllll_opy_ = []
bstack11llll1111_opy_ = bstack111ll_opy_ (u"ࠩࠪࣗ")
bstack1l11lll11l_opy_ = bstack111ll_opy_ (u"ࠪࠫࣘ")
bstack1ll111l1l_opy_ = False
bstack1l11ll11_opy_ = False
bstack111llll11_opy_ = {}
bstack11l11l1lll_opy_ = {}
bstack1lllll1ll1_opy_ = None
bstack111l11l1l_opy_ = None
bstack111111lll1_opy_ = None
bstack1l1llll11_opy_ = None
bstack111l1l1111_opy_ = None
bstack1l111l1ll_opy_ = None
bstack1ll11111l1_opy_ = None
bstack1lll1l111l_opy_ = None
bstack1ll1lll11l_opy_ = None
bstack1l1ll11l_opy_ = None
bstack1ll1l11l_opy_ = None
bstack1l1lllllll_opy_ = None
bstack1ll1l1llll_opy_ = None
bstack1l1ll1lll_opy_ = None
bstack11l1ll1lll_opy_ = None
bstack1l1lll11ll_opy_ = None
bstack11ll111lll_opy_ = None
bstack1lll1ll1l1_opy_ = None
bstack1l1l1ll11l_opy_ = None
bstack1ll1l1ll1_opy_ = None
bstack11l11ll11l_opy_ = None
bstack1l1l1lll11_opy_ = None
bstack11lll1ll1_opy_ = None
thread_local = threading.local()
bstack1l11ll11l_opy_ = False
bstack11l1l1111l_opy_ = bstack111ll_opy_ (u"ࠦࠧࣙ")
_11ll1llll_opy_ = None
logger = logger_utils.get_logger(__name__, bstack111llllll_opy_)
automation_logger = logger_utils.get_automation_logger(__name__)
global_config = Config.bstack1l1l11ll1_opy_()
percy = bstack1l1lllll1_opy_()
bstack1llll1llll_opy_ = bstack1111l1lll_opy_()
bstack11lll1l1l_opy_ = bstack11l111ll1l_opy_()
def bstack1111111111_opy_():
  global CONFIG
  global bstack1ll111l1l_opy_
  global global_config
  testContextOptions = bstack1llllll1l_opy_(CONFIG)
  if bstack11l1ll1l_opy_(CONFIG):
    if (bstack111ll_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧࣚ") in testContextOptions and str(testContextOptions[bstack111ll_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࣛ")]).lower() == bstack111ll_opy_ (u"ࠧࡵࡴࡸࡩࠬࣜ")):
      bstack1ll111l1l_opy_ = True
      global_config.bstack1l1lll1l1_opy_(True)
    if (bstack111ll_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬࣝ") in testContextOptions and str(testContextOptions[bstack111ll_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ࣞ")]).lower() == bstack111ll_opy_ (u"ࠪࡸࡷࡻࡥࠨࣟ")):
      global_config.bstack1ll1l1l111_opy_(True)
  else:
    bstack1ll111l1l_opy_ = True
    global_config.bstack1l1lll1l1_opy_(True)
    global_config.bstack1ll1l1l111_opy_(True)
def bstack1l11lll1ll_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack111111111_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack11111l1l1_opy_():
  global bstack11l11l1lll_opy_
  args = sys.argv
  for i in range(len(args)):
    if bstack111ll_opy_ (u"ࠦ࠲࠳ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡨࡵ࡮ࡧ࡫ࡪࡪ࡮ࡲࡥࠣ࣠") == args[i].lower() or bstack111ll_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰࡰࡩ࡭࡬ࠨ࣡") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      bstack11l11l1lll_opy_[bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࡤࡌࡉࡍࡇࠪ࣢")] = path
      return path
  return None
bstack1lll1l1l_opy_ = re.compile(bstack111ll_opy_ (u"ࡲࠣ࠰࠭ࡃࡡࠪࡻࠩ࠰࠭ࡃ࠮ࢃ࠮ࠫࡁࣣࠥ"))
def bstack1lll1ll111_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1lll1l1l_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack111ll_opy_ (u"ࠣࠦࡾࠦࣤ") + group + bstack111ll_opy_ (u"ࠤࢀࠦࣥ"), os.environ.get(group))
  return value
def bstack11ll1ll1ll_opy_():
  global bstack11lll1ll1_opy_
  if bstack11lll1ll1_opy_ is None:
        bstack11lll1ll1_opy_ = bstack11111l1l1_opy_()
  bstack1l11llll_opy_ = bstack11lll1ll1_opy_
  if bstack1l11llll_opy_ and os.path.exists(os.path.abspath(bstack1l11llll_opy_)):
    fileName = bstack1l11llll_opy_
  if bstack111ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋࣦࠧ") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨࣧ")])) and not bstack111ll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡑࡥࡲ࡫ࠧࣨ") in locals():
    fileName = os.environ[bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࡤࡌࡉࡍࡇࣩࠪ")]
  if bstack111ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡓࡧ࡭ࡦࠩ࣪") in locals():
    bstack111l1_opy_ = os.path.abspath(fileName)
  else:
    bstack111l1_opy_ = bstack111ll_opy_ (u"ࠨࠩ࣫")
  bstack11ll1lll_opy_ = os.getcwd()
  bstack1lllllll11_opy_ = bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬ࣬")
  bstack11ll1lll1l_opy_ = bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡥࡲࡲ࣭ࠧ")
  while (not os.path.exists(bstack111l1_opy_)) and bstack11ll1lll_opy_ != bstack111ll_opy_ (u"࣮ࠦࠧ"):
    bstack111l1_opy_ = os.path.join(bstack11ll1lll_opy_, bstack1lllllll11_opy_)
    if not os.path.exists(bstack111l1_opy_):
      bstack111l1_opy_ = os.path.join(bstack11ll1lll_opy_, bstack11ll1lll1l_opy_)
    if bstack11ll1lll_opy_ != os.path.dirname(bstack11ll1lll_opy_):
      bstack11ll1lll_opy_ = os.path.dirname(bstack11ll1lll_opy_)
    else:
      bstack11ll1lll_opy_ = bstack111ll_opy_ (u"ࠧࠨ࣯")
  bstack11lll1ll1_opy_ = bstack111l1_opy_ if os.path.exists(bstack111l1_opy_) else None
  return bstack11lll1ll1_opy_
def bstack1111llll11_opy_(config):
    if bstack111ll_opy_ (u"࠭ࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬ࣰ࠭") in config:
      config[bstack111ll_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࣱࠫ")] = config[bstack111ll_opy_ (u"ࠨࡶࡨࡷࡹࡘࡥࡱࡱࡵࡸ࡮ࡴࡧࠨࣲ")]
    if bstack111ll_opy_ (u"ࠩࡷࡩࡸࡺࡒࡦࡲࡲࡶࡹ࡯࡮ࡨࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣳ") in config:
      config[bstack111ll_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧࣴ")] = config[bstack111ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࡓࡵࡺࡩࡰࡰࡶࠫࣵ")]
def bstack1111l111_opy_():
  bstack111l1_opy_ = bstack11ll1ll1ll_opy_()
  if not os.path.exists(bstack111l1_opy_):
    bstack1ll11l111_opy_(
      bstack1111llll1_opy_.format(os.getcwd()))
  try:
    with open(bstack111l1_opy_, bstack111ll_opy_ (u"ࠬࡸࣶࠧ")) as stream:
      yaml.add_implicit_resolver(bstack111ll_opy_ (u"ࠨࠡࡱࡣࡷ࡬ࡪࡾࠢࣷ"), bstack1lll1l1l_opy_)
      yaml.add_constructor(bstack111ll_opy_ (u"ࠢࠢࡲࡤࡸ࡭࡫ࡸࠣࣸ"), bstack1lll1ll111_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      bstack1111llll11_opy_(config)
      return config
  except:
    with open(bstack111l1_opy_, bstack111ll_opy_ (u"ࠨࡴࣹࠪ")) as stream:
      try:
        config = yaml.safe_load(stream)
        bstack1111llll11_opy_(config)
        return config
      except yaml.YAMLError as exc:
        bstack1ll11l111_opy_(bstack1l1l1l111_opy_.format(str(exc)))
def bstack111lll1l11_opy_(config):
  bstack11111ll1l1_opy_ = bstack1l111l11ll_opy_(config)
  for option in list(bstack11111ll1l1_opy_):
    if option.lower() in bstack1ll11l11_opy_ and option != bstack1ll11l11_opy_[option.lower()]:
      bstack11111ll1l1_opy_[bstack1ll11l11_opy_[option.lower()]] = bstack11111ll1l1_opy_[option]
      del bstack11111ll1l1_opy_[option]
  return config
def bstack11lll1ll_opy_():
  global bstack1l1l1111l_opy_
  for key, bstack1l1l11l1l1_opy_ in bstack1lll11l111_opy_.items():
    if isinstance(bstack1l1l11l1l1_opy_, list):
      for var in bstack1l1l11l1l1_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1l1l1111l_opy_[key] = os.environ[var]
          break
    elif bstack1l1l11l1l1_opy_ in os.environ and os.environ[bstack1l1l11l1l1_opy_] and str(os.environ[bstack1l1l11l1l1_opy_]).strip():
      bstack1l1l1111l_opy_[key] = os.environ[bstack1l1l11l1l1_opy_]
  if bstack111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࣺࠫ") in os.environ:
    bstack1l1l1111l_opy_[bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࣻ")] = {}
    bstack1l1l1111l_opy_[bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣼ")][bstack111ll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣽ")] = os.environ[bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨࣾ")]
def bstack1l1l11l1_opy_():
  global bstack1lllll1l11l_opy_
  global bstack1l1l1llll_opy_
  global bstack11l11l1lll_opy_
  bstack111111l1_opy_ = []
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) - 1 and bstack111ll_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣿ").lower() == val.lower():
      bstack1lllll1l11l_opy_[bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬऀ")] = {}
      bstack1lllll1l11l_opy_[bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ँ")][bstack111ll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬं")] = sys.argv[idx + 1]
      bstack111111l1_opy_.extend([idx, idx + 1])
      break
  for key, bstack1l1111l11l_opy_ in bstack1l1ll11ll1_opy_.items():
    if isinstance(bstack1l1111l11l_opy_, list):
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        for var in bstack1l1111l11l_opy_:
          if bstack111ll_opy_ (u"ࠫ࠲࠳ࠧः") + var.lower() == val.lower() and key not in bstack1lllll1l11l_opy_:
            bstack1lllll1l11l_opy_[key] = sys.argv[idx + 1]
            bstack1l1l1llll_opy_ += bstack111ll_opy_ (u"ࠬࠦ࠭࠮ࠩऄ") + var + bstack111ll_opy_ (u"࠭ࠠࠨअ") + shlex.quote(sys.argv[idx + 1])
            bstack11l1l111ll_opy_(bstack11l11l1lll_opy_, key, sys.argv[idx + 1])
            bstack111111l1_opy_.extend([idx, idx + 1])
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        if bstack111ll_opy_ (u"ࠧ࠮࠯ࠪआ") + bstack1l1111l11l_opy_.lower() == val.lower() and key not in bstack1lllll1l11l_opy_:
          bstack1lllll1l11l_opy_[key] = sys.argv[idx + 1]
          bstack1l1l1llll_opy_ += bstack111ll_opy_ (u"ࠨࠢ࠰࠱ࠬइ") + bstack1l1111l11l_opy_ + bstack111ll_opy_ (u"ࠩࠣࠫई") + shlex.quote(sys.argv[idx + 1])
          bstack11l1l111ll_opy_(bstack11l11l1lll_opy_, key, sys.argv[idx + 1])
          bstack111111l1_opy_.extend([idx, idx + 1])
  for idx in sorted(set(bstack111111l1_opy_), reverse=True):
    if idx < len(sys.argv):
      del sys.argv[idx]
def bstack1l1ll1ll1_opy_(config):
  bstack11l1ll11_opy_ = config.keys()
  for bstack1l1l1l11ll_opy_, bstack1lllll1ll_opy_ in bstack1l1ll1l1ll_opy_.items():
    if bstack1lllll1ll_opy_ in bstack11l1ll11_opy_:
      config[bstack1l1l1l11ll_opy_] = config[bstack1lllll1ll_opy_]
      del config[bstack1lllll1ll_opy_]
  for bstack1l1l1l11ll_opy_, bstack1lllll1ll_opy_ in bstack1111111l_opy_.items():
    if isinstance(bstack1lllll1ll_opy_, list):
      for bstack1l111l111_opy_ in bstack1lllll1ll_opy_:
        if bstack1l111l111_opy_ in bstack11l1ll11_opy_:
          config[bstack1l1l1l11ll_opy_] = config[bstack1l111l111_opy_]
          del config[bstack1l111l111_opy_]
          break
    elif bstack1lllll1ll_opy_ in bstack11l1ll11_opy_:
      config[bstack1l1l1l11ll_opy_] = config[bstack1lllll1ll_opy_]
      del config[bstack1lllll1ll_opy_]
  for bstack1l111l111_opy_ in list(config):
    for bstack11l111ll1_opy_ in bstack1l11ll111_opy_:
      if bstack1l111l111_opy_.lower() == bstack11l111ll1_opy_.lower() and bstack1l111l111_opy_ != bstack11l111ll1_opy_:
        config[bstack11l111ll1_opy_] = config[bstack1l111l111_opy_]
        del config[bstack1l111l111_opy_]
  bstack11l1lll1l_opy_ = [{}]
  if not config.get(bstack111ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭उ")):
    config[bstack111ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧऊ")] = [{}]
  bstack11l1lll1l_opy_ = config[bstack111ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨऋ")]
  for platform in bstack11l1lll1l_opy_:
    for bstack1l111l111_opy_ in list(platform):
      for bstack11l111ll1_opy_ in bstack1l11ll111_opy_:
        if bstack1l111l111_opy_.lower() == bstack11l111ll1_opy_.lower() and bstack1l111l111_opy_ != bstack11l111ll1_opy_:
          platform[bstack11l111ll1_opy_] = platform[bstack1l111l111_opy_]
          del platform[bstack1l111l111_opy_]
  for bstack1l1l1l11ll_opy_, bstack1lllll1ll_opy_ in bstack1111111l_opy_.items():
    for platform in bstack11l1lll1l_opy_:
      if isinstance(bstack1lllll1ll_opy_, list):
        for bstack1l111l111_opy_ in bstack1lllll1ll_opy_:
          if bstack1l111l111_opy_ in platform:
            platform[bstack1l1l1l11ll_opy_] = platform[bstack1l111l111_opy_]
            del platform[bstack1l111l111_opy_]
            break
      elif bstack1lllll1ll_opy_ in platform:
        platform[bstack1l1l1l11ll_opy_] = platform[bstack1lllll1ll_opy_]
        del platform[bstack1lllll1ll_opy_]
  for bstack11l111ll11_opy_ in bstack11l11l11l_opy_:
    if bstack11l111ll11_opy_ in config:
      if not bstack11l11l11l_opy_[bstack11l111ll11_opy_] in config:
        config[bstack11l11l11l_opy_[bstack11l111ll11_opy_]] = {}
      config[bstack11l11l11l_opy_[bstack11l111ll11_opy_]].update(config[bstack11l111ll11_opy_])
      del config[bstack11l111ll11_opy_]
  for platform in bstack11l1lll1l_opy_:
    for bstack11l111ll11_opy_ in bstack11l11l11l_opy_:
      if bstack11l111ll11_opy_ in list(platform):
        if not bstack11l11l11l_opy_[bstack11l111ll11_opy_] in platform:
          platform[bstack11l11l11l_opy_[bstack11l111ll11_opy_]] = {}
        platform[bstack11l11l11l_opy_[bstack11l111ll11_opy_]].update(platform[bstack11l111ll11_opy_])
        del platform[bstack11l111ll11_opy_]
  config = bstack111lll1l11_opy_(config)
  return config
def bstack1l1lllll1l_opy_(config):
  global bstack1lllllll1l_opy_
  bstack1ll11ll111_opy_ = False
  bstack1111lll11_opy_ = os.environ.get(bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡊࡅࡇࡃࡘࡐ࡙ࡥࡌࡐࡅࡄࡐࡤࡏࡄࠨऌ"))
  if bstack111ll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫऍ") in config and str(config[bstack111ll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬऎ")]).lower() != bstack111ll_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨए"):
    if bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧऐ") not in config or str(config[bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨऑ")]).lower() == bstack111ll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫऒ"):
      config[bstack111ll_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬओ")] = False
    else:
      bstack111l1111_opy_ = bstack1ll111lll_opy_()
      if bstack111ll_opy_ (u"ࠧࡪࡵࡗࡶ࡮ࡧ࡬ࡈࡴ࡬ࡨࠬऔ") in bstack111l1111_opy_:
        if not bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬक") in config:
          config[bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ख")] = {}
        config[bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧग")][bstack111ll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭घ")] = bstack111ll_opy_ (u"ࠬࡧࡴࡴ࠯ࡵࡩࡵ࡫ࡡࡵࡧࡵࠫङ")
        bstack1ll11ll111_opy_ = True
        bstack1lllllll1l_opy_ = config[bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪच")].get(bstack111ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩछ"))
  if bstack11l1ll1l_opy_(config) and bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬज") in config and str(config[bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭झ")]).lower() != bstack111ll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩञ") and not bstack1ll11ll111_opy_:
    if not bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨट") in config:
      config[bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩठ")] = {}
    bstack111l1lllll_opy_ = config[bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪड")].get(bstack111ll_opy_ (u"ࠧࡴ࡭࡬ࡴࡇ࡯࡮ࡢࡴࡼࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡸࡧࡴࡪࡱࡱࠫढ"))
    if bstack1111lll11_opy_:
      if bstack111l1lllll_opy_:
        config[bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬण")][bstack111ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫत")] = bstack1111lll11_opy_
      elif bstack111ll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬथ") not in config[bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨद")]:
        config[bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩध")][bstack111ll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨन")] = bstack1111lll11_opy_
    if not bstack111l1lllll_opy_ and bstack111ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऩ") not in config[bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬप")]:
      bstack1111l1l1l_opy_ = datetime.datetime.now()
      bstack11l1llll1_opy_ = bstack1111l1l1l_opy_.strftime(bstack111ll_opy_ (u"ࠩࠨࡨࡤࠫࡢࡠࠧࡋࠩࡒ࠭फ"))
      hostname = socket.gethostname()
      bstack1lll111lll_opy_ = bstack111ll_opy_ (u"ࠪࠫब").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack111ll_opy_ (u"ࠫࢀࢃ࡟ࡼࡿࡢࡿࢂ࠭भ").format(bstack11l1llll1_opy_, hostname, bstack1lll111lll_opy_)
      config[bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩम")][bstack111ll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨय")] = identifier
    bstack1lllllll1l_opy_ = config[bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫर")].get(bstack111ll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪऱ"))
  return config
def bstack1ll11ll1_opy_():
  bstack11ll111l1l_opy_ =  bstack1l11ll1111_opy_()[bstack111ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠨल")]
  return bstack11ll111l1l_opy_ if bstack11ll111l1l_opy_ else -1
def bstack1111lll1ll_opy_(bstack11ll111l1l_opy_):
  global CONFIG
  if not bstack111ll_opy_ (u"ࠪࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬळ") in CONFIG[bstack111ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ऴ")]:
    return
  CONFIG[bstack111ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧव")] = CONFIG[bstack111ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨश")].replace(
    bstack111ll_opy_ (u"ࠧࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩष"),
    str(bstack11ll111l1l_opy_)
  )
def bstack1l11l1l1l_opy_():
  global CONFIG
  if not bstack111ll_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧस") in CONFIG[bstack111ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫह")]:
    return
  bstack1111l1l1l_opy_ = datetime.datetime.now()
  bstack11l1llll1_opy_ = bstack1111l1l1l_opy_.strftime(bstack111ll_opy_ (u"ࠪࠩࡩ࠳ࠥࡣ࠯ࠨࡌ࠿ࠫࡍࠨऺ"))
  CONFIG[bstack111ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ऻ")] = CONFIG[bstack111ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ़ࠧ")].replace(
    bstack111ll_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬऽ"),
    bstack11l1llll1_opy_
  )
def bstack1llll1111_opy_():
  global CONFIG
  if bstack111ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩा") in CONFIG and not bool(CONFIG[bstack111ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪि")]):
    del CONFIG[bstack111ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫी")]
    return
  if not bstack111ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬु") in CONFIG:
    CONFIG[bstack111ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ू")] = bstack111ll_opy_ (u"ࠬࠩࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨृ")
  if bstack111ll_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬॄ") in CONFIG[bstack111ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩॅ")]:
    bstack1l11l1l1l_opy_()
    os.environ[bstack111ll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬॆ")] = CONFIG[bstack111ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫे")]
  if not bstack111ll_opy_ (u"ࠪࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬै") in CONFIG[bstack111ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ॉ")]:
    return
  bstack11ll111l1l_opy_ = bstack111ll_opy_ (u"ࠬ࠭ॊ")
  bstack11l111ll_opy_ = bstack1ll11ll1_opy_()
  if bstack11l111ll_opy_ != -1:
    bstack11ll111l1l_opy_ = bstack111ll_opy_ (u"࠭ࡃࡊࠢࠪो") + str(bstack11l111ll_opy_)
  if bstack11ll111l1l_opy_ == bstack111ll_opy_ (u"ࠧࠨौ"):
    bstack11ll11111l_opy_ = bstack1l1111l1l_opy_(CONFIG[bstack111ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨ्ࠫ")])
    if bstack11ll11111l_opy_ != -1:
      bstack11ll111l1l_opy_ = str(bstack11ll11111l_opy_)
  if bstack11ll111l1l_opy_:
    bstack1111lll1ll_opy_(bstack11ll111l1l_opy_)
    os.environ[bstack111ll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ॎ")] = CONFIG[bstack111ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬॏ")]
def bstack1l1l1ll111_opy_(bstack11lll1l1_opy_, bstack1llll1l1_opy_, path):
  json_data = {
    bstack111ll_opy_ (u"ࠫ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨॐ"): bstack1llll1l1_opy_
  }
  if os.path.exists(path):
    bstack1ll1111111_opy_ = json.load(open(path, bstack111ll_opy_ (u"ࠬࡸࡢࠨ॑")))
  else:
    bstack1ll1111111_opy_ = {}
  bstack1ll1111111_opy_[bstack11lll1l1_opy_] = json_data
  with open(path, bstack111ll_opy_ (u"ࠨࡷࠬࠤ॒")) as outfile:
    json.dump(bstack1ll1111111_opy_, outfile)
def bstack1l1111l1l_opy_(bstack11lll1l1_opy_):
  bstack11lll1l1_opy_ = str(bstack11lll1l1_opy_)
  bstack1ll11l11ll_opy_ = os.path.join(os.path.expanduser(bstack111ll_opy_ (u"ࠧࡿࠩ॓")), bstack111ll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ॔"))
  try:
    if not os.path.exists(bstack1ll11l11ll_opy_):
      os.makedirs(bstack1ll11l11ll_opy_)
    file_path = os.path.join(os.path.expanduser(bstack111ll_opy_ (u"ࠩࢁࠫॕ")), bstack111ll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪॖ"), bstack111ll_opy_ (u"ࠫ࠳ࡨࡵࡪ࡮ࡧ࠱ࡳࡧ࡭ࡦ࠯ࡦࡥࡨ࡮ࡥ࠯࡬ࡶࡳࡳ࠭ॗ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack111ll_opy_ (u"ࠬࡽࠧक़")):
        pass
      with open(file_path, bstack111ll_opy_ (u"ࠨࡷࠬࠤख़")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack111ll_opy_ (u"ࠧࡳࠩग़")) as bstack1llll11l1l_opy_:
      bstack1ll1l11ll_opy_ = json.load(bstack1llll11l1l_opy_)
    if bstack11lll1l1_opy_ in bstack1ll1l11ll_opy_:
      bstack11l1ll111_opy_ = bstack1ll1l11ll_opy_[bstack11lll1l1_opy_][bstack111ll_opy_ (u"ࠨ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬज़")]
      bstack11lllll1_opy_ = int(bstack11l1ll111_opy_) + 1
      bstack1l1l1ll111_opy_(bstack11lll1l1_opy_, bstack11lllll1_opy_, file_path)
      return bstack11lllll1_opy_
    else:
      bstack1l1l1ll111_opy_(bstack11lll1l1_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warning(bstack111111ll11_opy_.format(str(e)))
    return -1
def bstack11l11l11_opy_(config):
  if not config[bstack111ll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫड़")] or not config[bstack111ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ढ़")]:
    return True
  else:
    return False
def bstack1llllll1111_opy_(config, index=0):
  global bstack1l11111ll1_opy_
  bstack11l1l11l1l_opy_ = {}
  caps = bstack1lll11l1ll_opy_ + bstack1l11l1l1_opy_
  if config.get(bstack111ll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨफ़"), False):
    bstack11l1l11l1l_opy_[bstack111ll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩय़")] = True
    bstack11l1l11l1l_opy_[bstack111ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪॠ")] = config.get(bstack111ll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࡓࡵࡺࡩࡰࡰࡶࠫॡ"), {})
  if bstack1l11111ll1_opy_:
    caps += bstack111ll11l11_opy_
  for key in config:
    if key in caps + [bstack111ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫॢ")]:
      continue
    bstack11l1l11l1l_opy_[key] = config[key]
  if bstack111ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॣ") in config:
    for bstack11lll111ll_opy_ in config[bstack111ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭।")][index]:
      if bstack11lll111ll_opy_ in caps:
        continue
      bstack11l1l11l1l_opy_[bstack11lll111ll_opy_] = config[bstack111ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ॥")][index][bstack11lll111ll_opy_]
  bstack11l1l11l1l_opy_[bstack111ll_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧ०")] = socket.gethostname()
  if bstack111ll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧ१") in bstack11l1l11l1l_opy_:
    del (bstack11l1l11l1l_opy_[bstack111ll_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨ२")])
  return bstack11l1l11l1l_opy_
def bstack11l1ll11l1_opy_(config):
  global bstack1l11111ll1_opy_
  bstack1ll1l1111_opy_ = {}
  caps = bstack1l11l1l1_opy_
  if bstack1l11111ll1_opy_:
    caps += bstack111ll11l11_opy_
  for key in caps:
    if key in config:
      bstack1ll1l1111_opy_[key] = config[key]
  return bstack1ll1l1111_opy_
def bstack111111l111_opy_(bstack11l1l11l1l_opy_, bstack1ll1l1111_opy_):
  bstack1lllll11l11_opy_ = {}
  for key in bstack11l1l11l1l_opy_.keys():
    if key in bstack1l1ll1l1ll_opy_:
      bstack1lllll11l11_opy_[bstack1l1ll1l1ll_opy_[key]] = bstack11l1l11l1l_opy_[key]
    else:
      bstack1lllll11l11_opy_[key] = bstack11l1l11l1l_opy_[key]
  for key in bstack1ll1l1111_opy_:
    if key in bstack1l1ll1l1ll_opy_:
      bstack1lllll11l11_opy_[bstack1l1ll1l1ll_opy_[key]] = bstack1ll1l1111_opy_[key]
    else:
      bstack1lllll11l11_opy_[key] = bstack1ll1l1111_opy_[key]
  return bstack1lllll11l11_opy_
def get_caps(config, index=0):
  global bstack1l11111ll1_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack1111l1ll_opy_ = bstack11111lll11_opy_(bstack111ll11ll1_opy_, config, logger)
  bstack1ll1l1111_opy_ = bstack11l1ll11l1_opy_(config)
  bstack1111llll1l_opy_ = bstack1l11l1l1_opy_
  bstack1111llll1l_opy_ += bstack1lll1111l1_opy_
  bstack1ll1l1111_opy_ = update(bstack1ll1l1111_opy_, bstack1111l1ll_opy_)
  if bstack1l11111ll1_opy_:
    bstack1111llll1l_opy_ += bstack111ll11l11_opy_
  if bstack111ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ३") in config:
    if bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ४") in config[bstack111ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭५")][index]:
      caps[bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ६")] = config[bstack111ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ७")][index][bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ८")]
    if bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ९") in config[bstack111ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ॰")][index]:
      caps[bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪॱ")] = str(config[bstack111ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॲ")][index][bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬॳ")])
    bstack1ll1l1l1_opy_ = bstack11111lll11_opy_(bstack111ll11ll1_opy_, config[bstack111ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨॴ")][index], logger)
    bstack1111llll1l_opy_ += list(bstack1ll1l1l1_opy_.keys())
    for bstack11llllll11_opy_ in bstack1111llll1l_opy_:
      if bstack11llllll11_opy_ in config[bstack111ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩॵ")][index]:
        if bstack11llllll11_opy_ == bstack111ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩॶ"):
          try:
            bstack1ll1l1l1_opy_[bstack11llllll11_opy_] = str(config[bstack111ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫॷ")][index][bstack11llllll11_opy_] * 1.0)
          except:
            bstack1ll1l1l1_opy_[bstack11llllll11_opy_] = str(config[bstack111ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॸ")][index][bstack11llllll11_opy_])
        else:
          bstack1ll1l1l1_opy_[bstack11llllll11_opy_] = config[bstack111ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॹ")][index][bstack11llllll11_opy_]
        del (config[bstack111ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॺ")][index][bstack11llllll11_opy_])
    bstack1ll1l1111_opy_ = update(bstack1ll1l1111_opy_, bstack1ll1l1l1_opy_)
  bstack11l1l11l1l_opy_ = bstack1llllll1111_opy_(config, index)
  for bstack1l111l111_opy_ in bstack1l11l1l1_opy_ + list(bstack1111l1ll_opy_.keys()):
    if bstack1l111l111_opy_ in bstack11l1l11l1l_opy_:
      bstack1ll1l1111_opy_[bstack1l111l111_opy_] = bstack11l1l11l1l_opy_[bstack1l111l111_opy_]
      del (bstack11l1l11l1l_opy_[bstack1l111l111_opy_])
  if bstack11lll11lll_opy_(config):
    bstack11l1l11l1l_opy_[bstack111ll_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬॻ")] = True
    caps.update(bstack1ll1l1111_opy_)
    caps[bstack111ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧॼ")] = bstack11l1l11l1l_opy_
  else:
    bstack11l1l11l1l_opy_[bstack111ll_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧॽ")] = False
    caps.update(bstack111111l111_opy_(bstack11l1l11l1l_opy_, bstack1ll1l1111_opy_))
    if bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ॾ") in caps:
      caps[bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪॿ")] = caps[bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨঀ")]
      del (caps[bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩঁ")])
    if bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ং") in caps:
      caps[bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨঃ")] = caps[bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ঄")]
      del (caps[bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩঅ")])
  return caps
def bstack1lllll1l1ll_opy_():
  global bstack11111l1111_opy_
  global CONFIG
  if bstack11111l1111_opy_ != bstack111ll_opy_ (u"ࠩࠪআ") and (bstack11111l1111_opy_.startswith(bstack111ll_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫই")) or bstack11111l1111_opy_.startswith(bstack111ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࠭ঈ"))):
    return bstack11111l1111_opy_
  if bstack111111111_opy_() <= version.parse(bstack111ll_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬউ")):
    if bstack11111l1111_opy_ != bstack111ll_opy_ (u"࠭ࠧঊ"):
      return bstack111ll_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣঋ") + bstack11111l1111_opy_ + bstack111ll_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧঌ")
    return bstack111111l1l_opy_
  if bstack11111l1111_opy_ != bstack111ll_opy_ (u"ࠩࠪ঍"):
    return bstack111ll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ঎") + bstack11111l1111_opy_ + bstack111ll_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧএ")
  return bstack1ll111l1ll_opy_
def bstack111lllllll_opy_(options):
  return hasattr(options, bstack111ll_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭ঐ"))
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
def bstack11l1l11111_opy_(options, bstack11llll1ll1_opy_):
  for bstack1ll1l111_opy_ in bstack11llll1ll1_opy_:
    if bstack1ll1l111_opy_ in [bstack111ll_opy_ (u"࠭ࡡࡳࡩࡶࠫ঑"), bstack111ll_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫ঒")]:
      continue
    if bstack1ll1l111_opy_ in options._experimental_options:
      options._experimental_options[bstack1ll1l111_opy_] = update(options._experimental_options[bstack1ll1l111_opy_],
                                                         bstack11llll1ll1_opy_[bstack1ll1l111_opy_])
    else:
      options.add_experimental_option(bstack1ll1l111_opy_, bstack11llll1ll1_opy_[bstack1ll1l111_opy_])
  if bstack111ll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ও") in bstack11llll1ll1_opy_:
    for arg in bstack11llll1ll1_opy_[bstack111ll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧঔ")]:
      options.add_argument(arg)
    del (bstack11llll1ll1_opy_[bstack111ll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨক")])
  if bstack111ll_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨখ") in bstack11llll1ll1_opy_:
    for ext in bstack11llll1ll1_opy_[bstack111ll_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩগ")]:
      try:
        options.add_extension(ext)
      except OSError:
        options.add_encoded_extension(ext)
    del (bstack11llll1ll1_opy_[bstack111ll_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪঘ")])
def bstack1llllll11l1_opy_(options):
  global CONFIG
  global bstack111111lll_opy_
  try:
    if not bstack111111lll_opy_ or not options:
      return options
    from bstack_utils.bstack111111ll1_opy_ import bstack1l1l1l1ll_opy_
    bstack11l11l11ll_opy_ = bstack1l1l1l1ll_opy_(options, bstack11l1ll1111_opy_=bstack111ll_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢঙ"))
    if bstack11l11l11ll_opy_ > 0:
      logger.debug(bstack111ll_opy_ (u"ࠣࡎࡲࡥࡩࠦࡴࡦࡵࡷ࡭ࡳ࡭࠺ࠡࡃࡧࡨࡪࡪࠠࡼࡿࠣࡨࡪ࡬ࡡࡶ࡮ࡷࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠠࡧࡱࡵࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠦচ").format(bstack11l11l11ll_opy_))
  except Exception as e:
    logger.debug(bstack111ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡯࡮࡫ࡧࡦࡸࠥࡲ࡯ࡢࡦࠣࡸࡪࡹࡴࡪࡰࡪࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡴࡶࡴࡪࡱࡱࡷ࠿ࠦࡻࡾࠤছ").format(e))
  return options
def bstack111lll1l_opy_(options, bstack1lll11l1_opy_):
  if bstack111ll_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩজ") in bstack1lll11l1_opy_:
    for bstack1l1lll1l_opy_ in bstack1lll11l1_opy_[bstack111ll_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪঝ")]:
      if bstack1l1lll1l_opy_ in options._preferences:
        options._preferences[bstack1l1lll1l_opy_] = update(options._preferences[bstack1l1lll1l_opy_], bstack1lll11l1_opy_[bstack111ll_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫঞ")][bstack1l1lll1l_opy_])
      else:
        options.set_preference(bstack1l1lll1l_opy_, bstack1lll11l1_opy_[bstack111ll_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬট")][bstack1l1lll1l_opy_])
  if bstack111ll_opy_ (u"ࠧࡢࡴࡪࡷࠬঠ") in bstack1lll11l1_opy_:
    for arg in bstack1lll11l1_opy_[bstack111ll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ড")]:
      options.add_argument(arg)
def bstack11l1111l1_opy_(options, bstack11ll1llll1_opy_):
  if bstack111ll_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࠪঢ") in bstack11ll1llll1_opy_:
    options.use_webview(bool(bstack11ll1llll1_opy_[bstack111ll_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࠫণ")]))
  bstack11l1l11111_opy_(options, bstack11ll1llll1_opy_)
def bstack1l1111l111_opy_(options, bstack1111lllll_opy_):
  for bstack1ll1ll1ll_opy_ in bstack1111lllll_opy_:
    if bstack1ll1ll1ll_opy_ in [bstack111ll_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨত"), bstack111ll_opy_ (u"ࠬࡧࡲࡨࡵࠪথ")]:
      continue
    options.set_capability(bstack1ll1ll1ll_opy_, bstack1111lllll_opy_[bstack1ll1ll1ll_opy_])
  if bstack111ll_opy_ (u"࠭ࡡࡳࡩࡶࠫদ") in bstack1111lllll_opy_:
    for arg in bstack1111lllll_opy_[bstack111ll_opy_ (u"ࠧࡢࡴࡪࡷࠬধ")]:
      options.add_argument(arg)
  if bstack111ll_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬন") in bstack1111lllll_opy_:
    options.bstack1ll1l1l1ll_opy_(bool(bstack1111lllll_opy_[bstack111ll_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭঩")]))
def bstack1l1llll1_opy_(options, bstack1l1ll1l11l_opy_):
  for bstack1l1l1l1l_opy_ in bstack1l1ll1l11l_opy_:
    if bstack1l1l1l1l_opy_ in [bstack111ll_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧপ"), bstack111ll_opy_ (u"ࠫࡦࡸࡧࡴࠩফ")]:
      continue
    options._options[bstack1l1l1l1l_opy_] = bstack1l1ll1l11l_opy_[bstack1l1l1l1l_opy_]
  if bstack111ll_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩব") in bstack1l1ll1l11l_opy_:
    for bstack1111l1l11l_opy_ in bstack1l1ll1l11l_opy_[bstack111ll_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪভ")]:
      options.bstack11ll11lll1_opy_(
        bstack1111l1l11l_opy_, bstack1l1ll1l11l_opy_[bstack111ll_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫম")][bstack1111l1l11l_opy_])
  if bstack111ll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭য") in bstack1l1ll1l11l_opy_:
    for arg in bstack1l1ll1l11l_opy_[bstack111ll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧর")]:
      options.add_argument(arg)
def bstack1ll1l11111_opy_(options, caps):
  if not hasattr(options, bstack111ll_opy_ (u"ࠪࡏࡊ࡟ࠧ঱")):
    return
  if options.KEY == bstack111ll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩল"):
    options = a11y.bstack1l1lll1ll_opy_(bstack1ll1lll1ll_opy_=options, config=CONFIG)
  if options.KEY == bstack111ll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ঳") and options.KEY in caps:
    bstack11l1l11111_opy_(options, caps[bstack111ll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ঴")])
  elif options.KEY == bstack111ll_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬ঵") and options.KEY in caps:
    bstack111lll1l_opy_(options, caps[bstack111ll_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭শ")])
  elif options.KEY == bstack111ll_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪষ") and options.KEY in caps:
    bstack1l1111l111_opy_(options, caps[bstack111ll_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫস")])
  elif options.KEY == bstack111ll_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬহ") and options.KEY in caps:
    bstack11l1111l1_opy_(options, caps[bstack111ll_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭঺")])
  elif options.KEY == bstack111ll_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬ঻") and options.KEY in caps:
    bstack1l1llll1_opy_(options, caps[bstack111ll_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ়࠭")])
def bstack11ll1l1l11_opy_(caps):
  global bstack1l11111ll1_opy_
  if isinstance(os.environ.get(bstack111ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩঽ")), str):
    bstack1l11111ll1_opy_ = eval(os.getenv(bstack111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪা")))
  if bstack1l11111ll1_opy_:
    if bstack1l11lll1ll_opy_() < version.parse(bstack111ll_opy_ (u"ࠪ࠶࠳࠹࠮࠱ࠩি")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack111ll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫী")
    if bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪু") in caps:
      browser = caps[bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫূ")]
    elif bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨৃ") in caps:
      browser = caps[bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩৄ")]
    browser = str(browser).lower()
    if browser == bstack111ll_opy_ (u"ࠩ࡬ࡴ࡭ࡵ࡮ࡦࠩ৅") or browser == bstack111ll_opy_ (u"ࠪ࡭ࡵࡧࡤࠨ৆"):
      browser = bstack111ll_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫে")
    if browser == bstack111ll_opy_ (u"ࠬࡹࡡ࡮ࡵࡸࡲ࡬࠭ৈ"):
      browser = bstack111ll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭৉")
    if browser not in [bstack111ll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ৊"), bstack111ll_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭ো"), bstack111ll_opy_ (u"ࠩ࡬ࡩࠬৌ"), bstack111ll_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫্ࠪ"), bstack111ll_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬৎ")]:
      return None
    try:
      package = bstack111ll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡿࢂ࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧ৏").format(browser)
      name = bstack111ll_opy_ (u"࠭ࡏࡱࡶ࡬ࡳࡳࡹࠧ৐")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack111lllllll_opy_(options):
        return None
      for bstack1l111l111_opy_ in caps.keys():
        options.set_capability(bstack1l111l111_opy_, caps[bstack1l111l111_opy_])
      bstack1ll1l11111_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack111l111ll_opy_(options, bstack1111l1l1l1_opy_):
  if not bstack111lllllll_opy_(options):
    return
  for bstack1l111l111_opy_ in bstack1111l1l1l1_opy_.keys():
    if bstack1l111l111_opy_ in bstack1lll1111l1_opy_:
      continue
    if bstack1l111l111_opy_ in options._caps and type(options._caps[bstack1l111l111_opy_]) in [dict, list]:
      options._caps[bstack1l111l111_opy_] = update(options._caps[bstack1l111l111_opy_], bstack1111l1l1l1_opy_[bstack1l111l111_opy_])
    else:
      options.set_capability(bstack1l111l111_opy_, bstack1111l1l1l1_opy_[bstack1l111l111_opy_])
  bstack1ll1l11111_opy_(options, bstack1111l1l1l1_opy_)
  if bstack111ll_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ࠭৑") in options._caps:
    if options._caps[bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭৒")] and options._caps[bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ৓")].lower() != bstack111ll_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫ৔"):
      del options._caps[bstack111ll_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪ৕")]
def bstack1111llllll_opy_(proxy_config):
  if bstack111ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ৖") in proxy_config:
    proxy_config[bstack111ll_opy_ (u"࠭ࡳࡴ࡮ࡓࡶࡴࡾࡹࠨৗ")] = proxy_config[bstack111ll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ৘")]
    del (proxy_config[bstack111ll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ৙")])
  if bstack111ll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬ৚") in proxy_config and proxy_config[bstack111ll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭৛")].lower() != bstack111ll_opy_ (u"ࠫࡩ࡯ࡲࡦࡥࡷࠫড়"):
    proxy_config[bstack111ll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨঢ়")] = bstack111ll_opy_ (u"࠭࡭ࡢࡰࡸࡥࡱ࠭৞")
  if bstack111ll_opy_ (u"ࠧࡱࡴࡲࡼࡾࡇࡵࡵࡱࡦࡳࡳ࡬ࡩࡨࡗࡵࡰࠬয়") in proxy_config:
    proxy_config[bstack111ll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫৠ")] = bstack111ll_opy_ (u"ࠩࡳࡥࡨ࠭ৡ")
  return proxy_config
def bstack1ll1l11lll_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack111ll_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩৢ") in config:
    return proxy
  config[bstack111ll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪৣ")] = bstack1111llllll_opy_(config[bstack111ll_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ৤")])
  if proxy == None:
    proxy = Proxy(config[bstack111ll_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ৥")])
  return proxy
def bstack1l11l1111l_opy_(self):
  global CONFIG
  global bstack1l1lllllll_opy_
  try:
    proxy = bstack1lll1111ll_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack111ll_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ০")):
        proxies = bstack111lllll1_opy_(proxy, bstack1lllll1l1ll_opy_())
        if len(proxies) > 0:
          protocol, bstack11lll111l1_opy_ = proxies.popitem()
          if bstack111ll_opy_ (u"ࠣ࠼࠲࠳ࠧ১") in bstack11lll111l1_opy_:
            return bstack11lll111l1_opy_
          else:
            return bstack111ll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ২") + bstack11lll111l1_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack111ll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡰࡳࡱࡻࡽࠥࡻࡲ࡭ࠢ࠽ࠤࢀࢃࠢ৩").format(str(e)))
  return bstack1l1lllllll_opy_(self)
def bstack1l1ll1l11_opy_():
  global CONFIG
  return bstack111lll111_opy_(CONFIG) and bstack1ll11ll11l_opy_() and bstack111111111_opy_() >= version.parse(bstack1l1l1l1l1l_opy_)
def bstack1ll1ll1l1_opy_():
  global CONFIG
  return (bstack111ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ৪") in CONFIG or bstack111ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ৫") in CONFIG) and bstack111l1111ll_opy_()
def bstack1l111l11ll_opy_(config):
  bstack11111ll1l1_opy_ = {}
  if bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ৬") in config:
    bstack11111ll1l1_opy_ = config[bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ৭")]
  if bstack111ll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ৮") in config:
    bstack11111ll1l1_opy_ = config[bstack111ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ৯")]
  proxy = bstack1lll1111ll_opy_(config)
  if proxy:
    if proxy.endswith(bstack111ll_opy_ (u"ࠪ࠲ࡵࡧࡣࠨৰ")) and os.path.isfile(proxy):
      bstack11111ll1l1_opy_[bstack111ll_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧৱ")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack111ll_opy_ (u"ࠬ࠴ࡰࡢࡥࠪ৲")):
        proxies = bstack1l1111111l_opy_(config, bstack1lllll1l1ll_opy_())
        if len(proxies) > 0:
          protocol, bstack11lll111l1_opy_ = proxies.popitem()
          if bstack111ll_opy_ (u"ࠨ࠺࠰࠱ࠥ৳") in bstack11lll111l1_opy_:
            parsed_url = urlparse(bstack11lll111l1_opy_)
          else:
            parsed_url = urlparse(protocol + bstack111ll_opy_ (u"ࠢ࠻࠱࠲ࠦ৴") + bstack11lll111l1_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack11111ll1l1_opy_[bstack111ll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡈࡰࡵࡷࠫ৵")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack11111ll1l1_opy_[bstack111ll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬ৶")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack11111ll1l1_opy_[bstack111ll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭৷")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack11111ll1l1_opy_[bstack111ll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧ৸")] = str(parsed_url.password)
  return bstack11111ll1l1_opy_
def bstack1llllll1l_opy_(config):
  if bstack111ll_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪ৹") in config:
    return config[bstack111ll_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫ৺")]
  return {}
def update_caps_for_local(caps):
  global bstack1lllllll1l_opy_
  if bstack111ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ৻") in caps:
    caps[bstack111ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩৼ")][bstack111ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨ৽")] = True
    if bstack1lllllll1l_opy_:
      caps[bstack111ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ৾")][bstack111ll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭৿")] = bstack1lllllll1l_opy_
  else:
    caps[bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪ਀")] = True
    if bstack1lllllll1l_opy_:
      caps[bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧਁ")] = bstack1lllllll1l_opy_
@measure(event_name=EVENTS.bstack11l1lllll_opy_, stage=STAGE.bstack1l1l11l1l_opy_, bstack1111l11lll_opy_=SESSION_NAME)
def bstack1llll11111_opy_():
  global CONFIG, bstack1lllllll1l_opy_
  if not bstack11l1ll1l_opy_(CONFIG) or cli.is_enabled(CONFIG):
    return
  if bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫਂ") in CONFIG and bstack1lllll11ll1_opy_(CONFIG[bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬਃ")]):
    if (
      bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭਄") in CONFIG
      and bstack1lllll11ll1_opy_(CONFIG[bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧਅ")].get(bstack111ll_opy_ (u"ࠫࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠨਆ")))
    ):
      logger.debug(bstack111ll_opy_ (u"ࠧࡒ࡯ࡤࡣ࡯ࠤࡧ࡯࡮ࡢࡴࡼࠤࡳࡵࡴࠡࡵࡷࡥࡷࡺࡥࡥࠢࡤࡷࠥࡹ࡫ࡪࡲࡅ࡭ࡳࡧࡲࡺࡋࡱ࡭ࡹ࡯ࡡ࡭࡫ࡶࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠨਇ"))
      return
    bstack11111ll1l1_opy_ = bstack1l111l11ll_opy_(CONFIG)
    bstack1lllllll1l_opy_ = bstack11111ll1l1_opy_.get(bstack111ll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨਈ")) or bstack1lllllll1l_opy_
    bstack111l1lll_opy_(CONFIG[bstack111ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪਉ")], bstack11111ll1l1_opy_)
def bstack111l1lll_opy_(key, bstack11111ll1l1_opy_):
  global bstack1llllll1l1l_opy_
  logger.info(bstack1l1ll1ll_opy_)
  try:
    bstack1llllll1l1l_opy_ = Local()
    bstack1l1l11ll11_opy_ = {bstack111ll_opy_ (u"ࠨ࡭ࡨࡽࠬਊ"): key}
    bstack1l1l11ll11_opy_.update(bstack11111ll1l1_opy_)
    logger.debug(bstack1111111l11_opy_.format(str(bstack1l1l11ll11_opy_)).replace(key, bstack111ll_opy_ (u"ࠩ࡞ࡖࡊࡊࡁࡄࡖࡈࡈࡢ࠭਋")))
    bstack1llllll1l1l_opy_.start(**bstack1l1l11ll11_opy_)
    if bstack1llllll1l1l_opy_.isRunning():
      logger.info(bstack1lll11ll1_opy_)
  except Exception as e:
    bstack1ll11l111_opy_(bstack1ll111ll11_opy_.format(str(e)))
def bstack1l11l1l11_opy_():
  global bstack1llllll1l1l_opy_
  if bstack1llllll1l1l_opy_.isRunning():
    logger.info(bstack1lll1l1l11_opy_)
    bstack1llllll1l1l_opy_.stop()
  if bstack111ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡇࡉࡋࡇࡕࡍࡖࡢࡐࡔࡉࡁࡍࡡࡌࡈࠬ਌") in os.environ:
    del os.environ[bstack111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡈࡊࡌࡁࡖࡎࡗࡣࡑࡕࡃࡂࡎࡢࡍࡉ࠭਍")]
  bstack1llllll1l1l_opy_ = None
def bstack11ll1ll1l1_opy_(bstack11l1ll1ll_opy_=[]):
  global CONFIG
  bstack1l11l11lll_opy_ = []
  bstack111lllll1l_opy_ = [bstack111ll_opy_ (u"ࠬࡵࡳࠨ਎"), bstack111ll_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩਏ"), bstack111ll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫਐ"), bstack111ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪ਑"), bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ਒"), bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫਓ")]
  try:
    for err in bstack11l1ll1ll_opy_:
      bstack11l1ll11ll_opy_ = {}
      for k in bstack111lllll1l_opy_:
        val = CONFIG[bstack111ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਔ")][int(err[bstack111ll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫਕ")])].get(k)
        if val:
          bstack11l1ll11ll_opy_[k] = val
      if(err[bstack111ll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬਖ")] != bstack111ll_opy_ (u"ࠧࠨਗ")):
        bstack11l1ll11ll_opy_[bstack111ll_opy_ (u"ࠨࡶࡨࡷࡹࡹࠧਘ")] = {
          err[bstack111ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧਙ")]: err[bstack111ll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩਚ")]
        }
        bstack1l11l11lll_opy_.append(bstack11l1ll11ll_opy_)
  except Exception as e:
    logger.debug(bstack111ll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡰࡴࡰࡥࡹࡺࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷ࠾ࠥ࠭ਛ") + str(e))
  finally:
    return bstack1l11l11lll_opy_
def bstack1lll111ll_opy_(file_name):
  bstack1lllll1l111_opy_ = []
  try:
    bstack1lllll1111_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1lllll1111_opy_):
      with open(bstack1lllll1111_opy_) as f:
        bstack11l11lllll_opy_ = json.load(f)
        bstack1lllll1l111_opy_ = bstack11l11lllll_opy_
      os.remove(bstack1lllll1111_opy_)
    return bstack1lllll1l111_opy_
  except Exception as e:
    logger.debug(bstack111ll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧ࡫ࡱࡨ࡮ࡴࡧࠡࡧࡵࡶࡴࡸࠠ࡭࡫ࡶࡸ࠿ࠦࠧਜ") + str(e))
    return bstack1lllll1l111_opy_
def bstack11111lll1_opy_():
  try:
      import time
      from bstack_utils.constants import bstack11l11111_opy_, EVENTS
      from bstack_utils.helper import bstack1ll11l11l_opy_, get_host_info, global_config
      from datetime import datetime
      from filelock import FileLock
      from bstack_utils.bstack11ll1l1l_opy_ import bstack111l1l1l_opy_
      bstack111l1l1l_opy_.bstack1llll1l1ll_opy_()
      bstack1l11l111l_opy_ = os.path.join(os.getcwd(), bstack111ll_opy_ (u"࠭࡬ࡰࡩࠪਝ"), bstack111ll_opy_ (u"ࠧ࡬ࡧࡼ࠱ࡲ࡫ࡴࡳ࡫ࡦࡷ࠳ࡰࡳࡰࡰࠪਞ"))
      data = None
      lock = FileLock(bstack1l11l111l_opy_+bstack111ll_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢਟ"), timeout=2)
      try:
          with lock:
              with open(bstack1l11l111l_opy_, bstack111ll_opy_ (u"ࠤࡵࠦਠ"), encoding=bstack111ll_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤਡ")) as file:
                  data = json.load(file)
      except Exception as e:
          logger.debug(bstack111ll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡳࡧࡤࡨࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵࠣࡪ࡮ࡲࡥ࠻ࠢࡾࢁࠧਢ").format(e))
          return
      if not data:
          return
      def bstack11lll1l11l_opy_():
          try:
              config = {
                  bstack111ll_opy_ (u"ࠧ࡮ࡥࡢࡦࡨࡶࡸࠨਣ"): {
                      bstack111ll_opy_ (u"ࠨࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠧਤ"): bstack111ll_opy_ (u"ࠢࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠥਥ"),
                  }
              }
              bstack1l1l1l1ll1_opy_ = datetime.utcnow()
              bstack1111l1l1l_opy_ = bstack1l1l1l1ll1_opy_.strftime(bstack111ll_opy_ (u"ࠣࠧ࡜࠱ࠪࡳ࠭ࠦࡦࡗࠩࡍࡀࠥࡎ࠼ࠨࡗ࠳ࠫࡦࠡࡗࡗࡇࠧਦ"))
              test_id = os.environ.get(bstack111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧਧ")) if os.environ.get(bstack111ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨਨ")) else global_config.get_property(bstack111ll_opy_ (u"ࠦࡸࡪ࡫ࡓࡷࡱࡍࡩࠨ਩"))
              payload = {
                  bstack111ll_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠤਪ"): bstack111ll_opy_ (u"ࠨࡳࡥ࡭ࡢࡩࡻ࡫࡮ࡵࡵࠥਫ"),
                  bstack111ll_opy_ (u"ࠢࡥࡣࡷࡥࠧਬ"): {
                      bstack111ll_opy_ (u"ࠣࡶࡨࡷࡹ࡮ࡵࡣࡡࡸࡹ࡮ࡪࠢਭ"): test_id,
                      bstack111ll_opy_ (u"ࠤࡦࡶࡪࡧࡴࡦࡦࡢࡨࡦࡿࠢਮ"): bstack1111l1l1l_opy_,
                      bstack111ll_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡱࡥࡲ࡫ࠢਯ"): bstack111ll_opy_ (u"ࠦࡘࡊࡋࡇࡧࡤࡸࡺࡸࡥࡑࡧࡵࡪࡴࡸ࡭ࡢࡰࡦࡩࠧਰ"),
                      bstack111ll_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣ࡯ࡹ࡯࡯ࠤ਱"): {
                          bstack111ll_opy_ (u"ࠨ࡭ࡦࡣࡶࡹࡷ࡫ࡳࠣਲ"): data,
                          bstack111ll_opy_ (u"ࠢࡴࡦ࡮ࡖࡺࡴࡉࡥࠤਲ਼"): global_config.get_property(bstack111ll_opy_ (u"ࠣࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠥ਴"))
                      },
                      bstack111ll_opy_ (u"ࠤࡸࡷࡪࡸ࡟ࡥࡣࡷࡥࠧਵ"): global_config.get_property(bstack111ll_opy_ (u"ࠥࡹࡸ࡫ࡲࡏࡣࡰࡩࠧਸ਼")),
                      bstack111ll_opy_ (u"ࠦ࡭ࡵࡳࡵࡡ࡬ࡲ࡫ࡵࠢ਷"): get_host_info()
                  }
              }
              bstack11ll1lll11_opy_ = bstack11l1llll1l_opy_(cli.config, [bstack111ll_opy_ (u"ࠧࡧࡰࡪࡵࠥਸ"), bstack111ll_opy_ (u"ࠨࡥࡥࡵࡌࡲࡸࡺࡲࡶ࡯ࡨࡲࡹࡧࡴࡪࡱࡱࠦਹ"), bstack111ll_opy_ (u"ࠢࡢࡲ࡬ࠦ਺")], bstack11l11111_opy_)
              response = bstack1ll11l11l_opy_(bstack111ll_opy_ (u"ࠣࡒࡒࡗ࡙ࠨ਻"), bstack11ll1lll11_opy_, payload, config)
              if response.status_code >= 200 and response.status_code < 300:
                  logger.info(bstack111ll_opy_ (u"ࠤࡎࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹࠠࡴࡧࡱࡸࠥࡹࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡹࡵࠠࡼࡿ਼ࠥ").format(bstack11l11111_opy_))
              else:
                  logger.debug(bstack111ll_opy_ (u"ࠥࡏࡪࡿࠠ࡮ࡧࡷࡶ࡮ࡩࡳࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮ࠠࡴࡶࡤࡸࡺࡹࠠࡼࡿࠥ਽").format(response.status_code))
          except Exception as e:
              logger.debug(bstack111ll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡱࡨࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵ࠽ࠤࢀࢃࠢਾ").format(e))
      bstack11lll1l11l_opy_()
  except Exception as e:
      logger.debug(bstack111ll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡱࡨࡤࡱࡥࡺࡡࡰࡩࡹࡸࡩࡤࡵ࠽ࠤࢀࢃࠢਿ").format(e))
def bstack1l111111ll_opy_(bstack1llll11ll1_opy_=False):
  bstack11llllll1_opy_ = bstack111ll_opy_ (u"ࠨࠢੀ")
  global bstack11l1l1111l_opy_
  global bstack11l1l1l1l1_opy_
  global bstack1ll11l1l1l_opy_
  global bstack1111l1111l_opy_
  global ROBOT_PYTHON_ERRORS
  global bstack1l11lll11l_opy_
  global CONFIG
  bstack1l1ll11ll_opy_ = os.environ.get(bstack111ll_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨੁ"))
  if bstack1l1ll11ll_opy_ not in [bstack111ll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩੂ")]:
    bstack11llllll1_opy_ = bstack111l1l1l_opy_.bstack1ll1111l1_opy_(EVENTS.bstack111l1ll1l1_opy_)
  percy.shutdown()
  if bstack11l1l1111l_opy_:
    logger.warning(bstack1l11lll1l1_opy_.format(str(bstack11l1l1111l_opy_)))
  else:
    try:
      bstack1ll1111111_opy_ = bstack1l1l1l1l11_opy_(bstack111ll_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨ੃"), logger)
      if bstack1ll1111111_opy_.get(bstack111ll_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨ੄")) and bstack1ll1111111_opy_.get(bstack111ll_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩ੅")).get(bstack111ll_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧ੆")):
        logger.warning(bstack1l11lll1l1_opy_.format(str(bstack1ll1111111_opy_[bstack111ll_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫੇ")][bstack111ll_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩੈ")])))
    except Exception as e:
      logger.error(e)
  if cli.is_running() and bstack1l1ll11ll_opy_ not in [bstack111ll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ੉")]:
    if _11ll1llll_opy_ is not None:
      bstack1llll11ll1_opy_ = _11ll1llll_opy_
    else:
      bstack1llll11ll1_opy_ = cli.is_running()
    bstack11ll1l11_opy_.invoke(Events.bstack1l111lll11_opy_)
  elif _11ll1llll_opy_ is not None:
    bstack1llll11ll1_opy_ = _11ll1llll_opy_
  logger.info(bstack1ll111l11_opy_)
  global bstack1llllll1l1l_opy_
  if bstack1llllll1l1l_opy_:
    bstack1l11l1l11_opy_()
  try:
    with bstack1111ll1lll_opy_:
      bstack11l1ll111l_opy_ = bstack11l1l1l1l1_opy_.copy()
    for driver in bstack11l1ll111l_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack11111l11_opy_)
  ROBOT_PYTHON_ERRORS = []
  if bstack1l11lll11l_opy_ == bstack111ll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ੊"):
    ROBOT_PYTHON_ERRORS = bstack1lll111ll_opy_(bstack111ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫੋ"))
  if bstack1l11lll11l_opy_ == bstack111ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫੌ") and len(bstack1111l1111l_opy_) == 0:
    bstack1111l1111l_opy_ = bstack1lll111ll_opy_(bstack111ll_opy_ (u"ࠬࡶࡷࡠࡲࡼࡸࡪࡹࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰ੍ࠪ"))
    if len(bstack1111l1111l_opy_) == 0:
      bstack1111l1111l_opy_ = bstack1lll111ll_opy_(bstack111ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡰࡱࡲࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬ੎"))
  bstack1ll11ll11_opy_ = bstack111ll_opy_ (u"ࠧࠨ੏")
  if len(bstack1ll11l1l1l_opy_) > 0:
    bstack1ll11ll11_opy_ = bstack11ll1ll1l1_opy_(bstack1ll11l1l1l_opy_)
  elif len(bstack1111l1111l_opy_) > 0:
    bstack1ll11ll11_opy_ = bstack11ll1ll1l1_opy_(bstack1111l1111l_opy_)
  elif len(ROBOT_PYTHON_ERRORS) > 0:
    bstack1ll11ll11_opy_ = bstack11ll1ll1l1_opy_(ROBOT_PYTHON_ERRORS)
  elif len(bstack11l1llllll_opy_) > 0:
    bstack1ll11ll11_opy_ = bstack11ll1ll1l1_opy_(bstack11l1llllll_opy_)
  if bstack1l1ll11ll_opy_ not in [bstack111ll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ੐")]:
    def bstack111111llll_opy_():
      try:
        if bstack1l1ll11ll_opy_ in [bstack111ll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨੑ"), bstack111ll_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ੒")]:
          bstack1111l11l_opy_()
      except Exception as e:
        logger.debug(bstack111ll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡪࡰࡤࡰࡤ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧ੓").format(e))
    def bstack1l11l11l11_opy_():
      try:
        if bool(bstack1ll11ll11_opy_):
          bstack1l11l11l_opy_(bstack1ll11ll11_opy_, bstack1llll11ll1_opy_=bstack1llll11ll1_opy_)
        else:
          bstack1l11l11l_opy_(bstack1llll11ll1_opy_=bstack1llll11ll1_opy_)
      except Exception as e:
        logger.debug(bstack111ll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥ࡫ࡶࡦࡰࡷ࠾ࠥࢁࡽࠣ੔").format(e))
    def bstack111l11111l_opy_():
      try:
        logger_utils.bstack1lllll1l1_opy_(CONFIG)
      except Exception as e:
        logger.debug(bstack111ll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡹࡥ࡯ࡦ࡬ࡲ࡬ࠦ࡬ࡰࡩࡶ࠾ࠥࢁࡽࠣ੕").format(e))
    bstack11111111_opy_ = threading.Thread(target=bstack111111llll_opy_)
    bstack11l1l1ll_opy_ = threading.Thread(target=bstack1l11l11l11_opy_)
    bstack11l11lll1l_opy_ = threading.Thread(target=bstack111l11111l_opy_)
    threads = [bstack11111111_opy_, bstack11l1l1ll_opy_, bstack11l11lll1l_opy_]
    for thread in threads:
      try:
        thread.start()
      except Exception as e:
        logger.debug(bstack111ll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡳࡵࡣࡵࡸ࡮ࡴࡧࠡࡶ࡫ࡶࡪࡧࡤࠡࡽࢀ࠾ࠥࢁࡽࠣ੖").format(thread.name, e))
    for thread in threads:
      try:
        thread.join()
      except Exception as e:
        logger.debug(bstack111ll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠ࡫ࡱ࡬ࡲ࡮ࡴࡧࠡࡶ࡫ࡶࡪࡧࡤࠡࡽࢀ࠾ࠥࢁࡽࠣ੗").format(thread.name, e))
    bstack1llll111l_opy_(bstack1l1lll11_opy_, logger)
    bstack1llll111l_opy_(os.path.join(os.getcwd(), bstack111ll_opy_ (u"ࠩ࡯ࡳ࡬࠭੘"), bstack111ll_opy_ (u"ࠪ࡯ࡪࡿ࠭࡮ࡧࡷࡶ࡮ࡩࡳ࠯࡬ࡶࡳࡳ࠭ਖ਼")), logger)
  if bstack1l1ll11ll_opy_ not in [bstack111ll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬਗ਼")]:
    bstack111l1l1l_opy_.end(EVENTS.bstack111l1ll1l1_opy_.value, bstack11llllll1_opy_ + bstack111ll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧਜ਼"), bstack11llllll1_opy_ + bstack111ll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦੜ"), status=True, failure=None, test_name=None)
    bstack11111lll1_opy_()
    logger_utils.bstack11l1l1ll1_opy_()
    logging.shutdown()
  if len(ROBOT_PYTHON_ERRORS) > 0:
    sys.exit(len(ROBOT_PYTHON_ERRORS))
def bstack111l111l1l_opy_(bstack11l1111111_opy_, frame):
  global global_config
  logger.error(bstack11l1l1l1l_opy_)
  global_config.bstack1l1l1llll1_opy_(bstack111ll_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡏࡱࠪ੝"), bstack11l1111111_opy_)
  if hasattr(signal, bstack111ll_opy_ (u"ࠨࡕ࡬࡫ࡳࡧ࡬ࡴࠩਫ਼")):
    global_config.bstack1l1l1llll1_opy_(bstack111ll_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩ੟"), signal.Signals(bstack11l1111111_opy_).name)
  else:
    global_config.bstack1l1l1llll1_opy_(bstack111ll_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪ੠"), bstack111ll_opy_ (u"ࠫࡘࡏࡇࡖࡐࡎࡒࡔ࡝ࡎࠨ੡"))
  bstack1llll11ll1_opy_ = cli.is_running()
  if bstack1llll11ll1_opy_:
    bstack11ll1l11_opy_.invoke(Events.bstack1l111lll11_opy_)
  bstack1l1ll11ll_opy_ = os.environ.get(bstack111ll_opy_ (u"ࠬࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉ࠭੢"))
  if bstack1l1ll11ll_opy_ == bstack111ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭੣") and not cli.is_enabled(CONFIG):
    TestHubHandler.stop(global_config.get_property(bstack111ll_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡔ࡫ࡪࡲࡦࡲࠧ੤")))
  bstack1l111111ll_opy_(bstack1llll11ll1_opy_)
  sys.exit(1)
def bstack1ll11l111_opy_(err):
  logger.critical(bstack1l1ll1l1l_opy_.format(str(err)))
  bstack1l11l11l_opy_(bstack1l1ll1l1l_opy_.format(str(err)), True)
  atexit.unregister(bstack1l111111ll_opy_)
  bstack1111l11l_opy_()
  sys.exit(1)
def bstack11l11ll1l1_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1l11l11l_opy_(message, True)
  atexit.unregister(bstack1l111111ll_opy_)
  bstack1111l11l_opy_()
  sys.exit(1)
def bstack1l1111l1_opy_():
  global CONFIG
  global bstack1lllll1l11l_opy_
  global bstack1l1l1111l_opy_
  global BROWSERSTACK_AUTOMATION
  CONFIG = bstack1111l111_opy_()
  load_dotenv(CONFIG.get(bstack111ll_opy_ (u"ࠨࡧࡱࡺࡋ࡯࡬ࡦࠩ੥")))
  bstack11lll1ll_opy_()
  bstack1l1l11l1_opy_()
  CONFIG = bstack1l1ll1ll1_opy_(CONFIG)
  update(CONFIG, bstack1l1l1111l_opy_)
  update(CONFIG, bstack1lllll1l11l_opy_)
  if not cli.is_enabled(CONFIG):
    CONFIG = bstack1l1lllll1l_opy_(CONFIG)
  BROWSERSTACK_AUTOMATION = bstack11l1ll1l_opy_(CONFIG)
  os.environ[bstack111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬ੦")] = BROWSERSTACK_AUTOMATION.__str__().lower()
  global_config.bstack1l1l1llll1_opy_(bstack111ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫ੧"), BROWSERSTACK_AUTOMATION)
  if (bstack111ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ੨") in CONFIG and bstack111ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ੩") in bstack1lllll1l11l_opy_) or (
          bstack111ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ੪") in CONFIG and bstack111ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ੫") not in bstack1l1l1111l_opy_):
    if os.getenv(bstack111ll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬ੬")):
      CONFIG[bstack111ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ੭")] = os.getenv(bstack111ll_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧ੮"))
    else:
      if not CONFIG.get(bstack111ll_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠢ੯"), bstack111ll_opy_ (u"ࠧࠨੰ")) in bstack11l1l1l111_opy_:
        bstack1llll1111_opy_()
  elif (bstack111ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩੱ") not in CONFIG and bstack111ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩੲ") in CONFIG) or (
          bstack111ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫੳ") in bstack1l1l1111l_opy_ and bstack111ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬੴ") not in bstack1lllll1l11l_opy_):
    del (CONFIG[bstack111ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬੵ")])
  if bstack11l11l11_opy_(CONFIG):
    bstack1ll11l111_opy_(bstack11llll1l11_opy_)
  Config.bstack1l1l11ll1_opy_().bstack1l1l1llll1_opy_(bstack111ll_opy_ (u"ࠦࡺࡹࡥࡳࡐࡤࡱࡪࠨ੶"), CONFIG[bstack111ll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ੷")])
  bstack1lllll1ll1l_opy_()
  bstack1ll1ll1l_opy_()
  if bstack1l11111ll1_opy_ and not CONFIG.get(bstack111ll_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠤ੸"), bstack111ll_opy_ (u"ࠢࠣ੹")) in bstack11l1l1l111_opy_:
    CONFIG[bstack111ll_opy_ (u"ࠨࡣࡳࡴࠬ੺")] = bstack1111l111ll_opy_(CONFIG)
    logger.info(bstack1l1l11l111_opy_.format(CONFIG[bstack111ll_opy_ (u"ࠩࡤࡴࡵ࠭੻")]))
  if not BROWSERSTACK_AUTOMATION:
    CONFIG[bstack111ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭੼")] = [{}]
def bstack11ll1l11ll_opy_(config, bstack11ll1l1lll_opy_):
  global CONFIG
  global bstack1l11111ll1_opy_
  CONFIG = config
  bstack1l11111ll1_opy_ = bstack11ll1l1lll_opy_
def bstack1ll1ll1l_opy_():
  global CONFIG
  global bstack1l11111ll1_opy_
  if bstack111ll_opy_ (u"ࠫࡦࡶࡰࠨ੽") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack11l11ll1l1_opy_(e, bstack1ll1ll111l_opy_)
    bstack1l11111ll1_opy_ = True
    global_config.bstack1l1l1llll1_opy_(bstack111ll_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ੾"), True)
def bstack1111l111ll_opy_(config):
  bstack11ll11l1l1_opy_ = bstack111ll_opy_ (u"࠭ࠧ੿")
  app = config[bstack111ll_opy_ (u"ࠧࡢࡲࡳࠫ઀")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1lll111l_opy_:
      if os.path.exists(app):
        bstack11ll11l1l1_opy_ = bstack1lllll1lll1_opy_(config, app)
      elif bstack111l11llll_opy_(app):
        bstack11ll11l1l1_opy_ = app
      else:
        bstack1ll11l111_opy_(bstack1ll1lllll1_opy_.format(app))
    else:
      if bstack111l11llll_opy_(app):
        bstack11ll11l1l1_opy_ = app
      elif os.path.exists(app):
        bstack11ll11l1l1_opy_ = bstack1lllll1lll1_opy_(app)
      else:
        bstack1ll11l111_opy_(bstack1lllll11l_opy_)
  else:
    if len(app) > 2:
      bstack1ll11l111_opy_(bstack1lll11ll_opy_)
    elif len(app) == 2:
      if bstack111ll_opy_ (u"ࠨࡲࡤࡸ࡭࠭ઁ") in app and bstack111ll_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬં") in app:
        if os.path.exists(app[bstack111ll_opy_ (u"ࠪࡴࡦࡺࡨࠨઃ")]):
          bstack11ll11l1l1_opy_ = bstack1lllll1lll1_opy_(config, app[bstack111ll_opy_ (u"ࠫࡵࡧࡴࡩࠩ઄")], app[bstack111ll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨઅ")])
        else:
          bstack1ll11l111_opy_(bstack1ll1lllll1_opy_.format(app))
      else:
        bstack1ll11l111_opy_(bstack1lll11ll_opy_)
    else:
      for key in app:
        if key in bstack11lllll1l1_opy_:
          if key == bstack111ll_opy_ (u"࠭ࡰࡢࡶ࡫ࠫઆ"):
            if os.path.exists(app[key]):
              bstack11ll11l1l1_opy_ = bstack1lllll1lll1_opy_(config, app[key])
            else:
              bstack1ll11l111_opy_(bstack1ll1lllll1_opy_.format(app))
          else:
            bstack11ll11l1l1_opy_ = app[key]
        else:
          bstack1ll11l111_opy_(bstack1l11ll1l1l_opy_)
  return bstack11ll11l1l1_opy_
def bstack111l11llll_opy_(bstack11ll11l1l1_opy_):
  import re
  bstack1111ll1l1l_opy_ = re.compile(bstack111ll_opy_ (u"ࡲࠣࡠ࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯ࠪࠢઇ"))
  bstack1l1l11l1ll_opy_ = re.compile(bstack111ll_opy_ (u"ࡳࠤࡡ࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰࠯࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭ࠨࠧઈ"))
  if bstack111ll_opy_ (u"ࠩࡥࡷ࠿࠵࠯ࠨઉ") in bstack11ll11l1l1_opy_ or re.fullmatch(bstack1111ll1l1l_opy_, bstack11ll11l1l1_opy_) or re.fullmatch(bstack1l1l11l1ll_opy_, bstack11ll11l1l1_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack1llllll1l1_opy_, stage=STAGE.bstack1l1l11l1l_opy_, bstack1111l11lll_opy_=SESSION_NAME)
def bstack1lllll1lll1_opy_(config, path, bstack1llll1l11_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack111ll_opy_ (u"ࠪࡶࡧ࠭ઊ")).read()).hexdigest()
  bstack1llll1l1l_opy_ = bstack11111ll111_opy_(md5_hash)
  bstack11ll11l1l1_opy_ = None
  if bstack1llll1l1l_opy_:
    logger.info(bstack111lll1ll_opy_.format(bstack1llll1l1l_opy_, md5_hash))
    return bstack1llll1l1l_opy_
  bstack1l11111lll_opy_ = datetime.datetime.now()
  multipart_data = MultipartEncoder(
    fields={
      bstack111ll_opy_ (u"ࠫ࡫࡯࡬ࡦࠩઋ"): (os.path.basename(path), open(os.path.abspath(path), bstack111ll_opy_ (u"ࠬࡸࡢࠨઌ")), bstack111ll_opy_ (u"࠭ࡴࡦࡺࡷ࠳ࡵࡲࡡࡪࡰࠪઍ")),
      bstack111ll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪ઎"): bstack1llll1l11_opy_
    }
  )
  response = requests.post(bstack11l1l11lll_opy_, data=multipart_data,
                           headers={bstack111ll_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧએ"): multipart_data.content_type},
                           auth=(config[bstack111ll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫઐ")], config[bstack111ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ઑ")]))
  try:
    res = json.loads(response.text)
    bstack11ll11l1l1_opy_ = res[bstack111ll_opy_ (u"ࠫࡦࡶࡰࡠࡷࡵࡰࠬ઒")]
    logger.info(bstack1l111ll11l_opy_.format(bstack11ll11l1l1_opy_))
    bstack1l1l1ll1ll_opy_(md5_hash, bstack11ll11l1l1_opy_)
    cli.bstack1ll11111l_opy_(bstack111ll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽ࡹࡵࡲ࡯ࡢࡦࡢࡥࡵࡶࠢઓ"), datetime.datetime.now() - bstack1l11111lll_opy_)
  except ValueError as err:
    bstack1ll11l111_opy_(bstack1lll11lll_opy_.format(str(err)))
  return bstack11ll11l1l1_opy_
def bstack1lllll1ll1l_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack1ll11llll1_opy_
  bstack11llllllll_opy_ = 1
  bstack1111lll1l1_opy_ = 1
  if bstack111ll_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ઔ") in CONFIG:
    bstack1111lll1l1_opy_ = CONFIG[bstack111ll_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧક")]
  else:
    bstack1111lll1l1_opy_ = bstack1ll1ll1l11_opy_(framework_name, args) or 1
  if bstack111ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫખ") in CONFIG:
    bstack11llllllll_opy_ = len(CONFIG[bstack111ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬગ")])
  bstack1ll11llll1_opy_ = int(bstack1111lll1l1_opy_) * int(bstack11llllllll_opy_)
def bstack1ll1ll1l11_opy_(framework_name, args):
  if framework_name == bstack111l111l11_opy_ and args and bstack111ll_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨઘ") in args:
      bstack1ll1lll1_opy_ = args.index(bstack111ll_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩઙ"))
      return int(args[bstack1ll1lll1_opy_ + 1]) or 1
  return 1
def bstack11111ll111_opy_(md5_hash):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack111ll_opy_ (u"ࠬ࡬ࡩ࡭ࡧ࡯ࡳࡨࡱࠠ࡯ࡱࡷࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠬࠡࡷࡶ࡭ࡳ࡭ࠠࡣࡣࡶ࡭ࡨࠦࡦࡪ࡮ࡨࠤࡴࡶࡥࡳࡣࡷ࡭ࡴࡴࡳࠨચ"))
    bstack1ll1lll1l1_opy_ = os.path.join(os.path.expanduser(bstack111ll_opy_ (u"࠭ࡾࠨછ")), bstack111ll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧજ"), bstack111ll_opy_ (u"ࠨࡣࡳࡴ࡚ࡶ࡬ࡰࡣࡧࡑࡉ࠻ࡈࡢࡵ࡫࠲࡯ࡹ࡯࡯ࠩઝ"))
    if os.path.exists(bstack1ll1lll1l1_opy_):
      try:
        bstack1ll111111l_opy_ = json.load(open(bstack1ll1lll1l1_opy_, bstack111ll_opy_ (u"ࠩࡵࡦࠬઞ")))
        if md5_hash in bstack1ll111111l_opy_:
          bstack11ll11ll11_opy_ = bstack1ll111111l_opy_[md5_hash]
          bstack11111l1l11_opy_ = datetime.datetime.now()
          bstack1111l1ll1_opy_ = datetime.datetime.strptime(bstack11ll11ll11_opy_[bstack111ll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ટ")], bstack111ll_opy_ (u"ࠫࠪࡪ࠯ࠦ࡯࠲ࠩ࡞ࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨઠ"))
          if (bstack11111l1l11_opy_ - bstack1111l1ll1_opy_).days > 30:
            return None
          elif version.parse(str(__version__)) > version.parse(bstack11ll11ll11_opy_[bstack111ll_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪડ")]):
            return None
          return bstack11ll11ll11_opy_[bstack111ll_opy_ (u"࠭ࡩࡥࠩઢ")]
      except Exception as e:
        logger.debug(bstack111ll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡲࡦࡣࡧ࡭ࡳ࡭ࠠࡎࡆ࠸ࠤ࡭ࡧࡳࡩࠢࡩ࡭ࡱ࡫࠺ࠡࡽࢀࠫણ").format(str(e)))
    return None
  bstack1ll1lll1l1_opy_ = os.path.join(os.path.expanduser(bstack111ll_opy_ (u"ࠨࢀࠪત")), bstack111ll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩથ"), bstack111ll_opy_ (u"ࠪࡥࡵࡶࡕࡱ࡮ࡲࡥࡩࡓࡄ࠶ࡊࡤࡷ࡭࠴ࡪࡴࡱࡱࠫદ"))
  lock_file = bstack1ll1lll1l1_opy_ + bstack111ll_opy_ (u"ࠫ࠳ࡲ࡯ࡤ࡭ࠪધ")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack1ll1lll1l1_opy_):
        with open(bstack1ll1lll1l1_opy_, bstack111ll_opy_ (u"ࠬࡸࠧન")) as f:
          content = f.read().strip()
          if content:
            bstack1ll111111l_opy_ = json.loads(content)
            if md5_hash in bstack1ll111111l_opy_:
              bstack11ll11ll11_opy_ = bstack1ll111111l_opy_[md5_hash]
              bstack11111l1l11_opy_ = datetime.datetime.now()
              bstack1111l1ll1_opy_ = datetime.datetime.strptime(bstack11ll11ll11_opy_[bstack111ll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ઩")], bstack111ll_opy_ (u"ࠧࠦࡦ࠲ࠩࡲ࠵࡚ࠥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫપ"))
              if (bstack11111l1l11_opy_ - bstack1111l1ll1_opy_).days > 30:
                return None
              elif version.parse(str(__version__)) > version.parse(bstack11ll11ll11_opy_[bstack111ll_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ફ")]):
                return None
              return bstack11ll11ll11_opy_[bstack111ll_opy_ (u"ࠩ࡬ࡨࠬબ")]
      return None
  except Exception as e:
    logger.debug(bstack111ll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡺ࡭ࡹ࡮ࠠࡧ࡫࡯ࡩࠥࡲ࡯ࡤ࡭࡬ࡲ࡬ࠦࡦࡰࡴࠣࡑࡉ࠻ࠠࡩࡣࡶ࡬࠿ࠦࡻࡾࠩભ").format(str(e)))
    return None
def bstack1l1l1ll1ll_opy_(md5_hash, bstack11ll11l1l1_opy_):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack111ll_opy_ (u"ࠫ࡫࡯࡬ࡦ࡮ࡲࡧࡰࠦ࡮ࡰࡶࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪ࠲ࠠࡶࡵ࡬ࡲ࡬ࠦࡢࡢࡵ࡬ࡧࠥ࡬ࡩ࡭ࡧࠣࡳࡵ࡫ࡲࡢࡶ࡬ࡳࡳࡹࠧમ"))
    bstack1ll11l11ll_opy_ = os.path.join(os.path.expanduser(bstack111ll_opy_ (u"ࠬࢄࠧય")), bstack111ll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ર"))
    if not os.path.exists(bstack1ll11l11ll_opy_):
      os.makedirs(bstack1ll11l11ll_opy_)
    bstack1ll1lll1l1_opy_ = os.path.join(os.path.expanduser(bstack111ll_opy_ (u"ࠧࡿࠩ઱")), bstack111ll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨલ"), bstack111ll_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪળ"))
    bstack1ll11lllll_opy_ = {
      bstack111ll_opy_ (u"ࠪ࡭ࡩ࠭઴"): bstack11ll11l1l1_opy_,
      bstack111ll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧવ"): datetime.datetime.strftime(datetime.datetime.now(), bstack111ll_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩશ")),
      bstack111ll_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫષ"): str(__version__)
    }
    try:
      bstack1ll111111l_opy_ = {}
      if os.path.exists(bstack1ll1lll1l1_opy_):
        bstack1ll111111l_opy_ = json.load(open(bstack1ll1lll1l1_opy_, bstack111ll_opy_ (u"ࠧࡳࡤࠪસ")))
      bstack1ll111111l_opy_[md5_hash] = bstack1ll11lllll_opy_
      with open(bstack1ll1lll1l1_opy_, bstack111ll_opy_ (u"ࠣࡹ࠮ࠦહ")) as outfile:
        json.dump(bstack1ll111111l_opy_, outfile)
    except Exception as e:
      logger.debug(bstack111ll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡷࡳࡨࡦࡺࡩ࡯ࡩࠣࡑࡉ࠻ࠠࡩࡣࡶ࡬ࠥ࡬ࡩ࡭ࡧ࠽ࠤࢀࢃࠧ઺").format(str(e)))
    return
  bstack1ll11l11ll_opy_ = os.path.join(os.path.expanduser(bstack111ll_opy_ (u"ࠪࢂࠬ઻")), bstack111ll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮઼ࠫ"))
  if not os.path.exists(bstack1ll11l11ll_opy_):
    os.makedirs(bstack1ll11l11ll_opy_)
  bstack1ll1lll1l1_opy_ = os.path.join(os.path.expanduser(bstack111ll_opy_ (u"ࠬࢄࠧઽ")), bstack111ll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ા"), bstack111ll_opy_ (u"ࠧࡢࡲࡳ࡙ࡵࡲ࡯ࡢࡦࡐࡈ࠺ࡎࡡࡴࡪ࠱࡮ࡸࡵ࡮ࠨિ"))
  lock_file = bstack1ll1lll1l1_opy_ + bstack111ll_opy_ (u"ࠨ࠰࡯ࡳࡨࡱࠧી")
  bstack1ll11lllll_opy_ = {
    bstack111ll_opy_ (u"ࠩ࡬ࡨࠬુ"): bstack11ll11l1l1_opy_,
    bstack111ll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ૂ"): datetime.datetime.strftime(datetime.datetime.now(), bstack111ll_opy_ (u"ࠫࠪࡪ࠯ࠦ࡯࠲ࠩ࡞ࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨૃ")),
    bstack111ll_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪૄ"): str(__version__)
  }
  try:
    with FileLock(lock_file, timeout=10):
      bstack1ll111111l_opy_ = {}
      if os.path.exists(bstack1ll1lll1l1_opy_):
        with open(bstack1ll1lll1l1_opy_, bstack111ll_opy_ (u"࠭ࡲࠨૅ")) as f:
          content = f.read().strip()
          if content:
            bstack1ll111111l_opy_ = json.loads(content)
      bstack1ll111111l_opy_[md5_hash] = bstack1ll11lllll_opy_
      with open(bstack1ll1lll1l1_opy_, bstack111ll_opy_ (u"ࠢࡸࠤ૆")) as outfile:
        json.dump(bstack1ll111111l_opy_, outfile)
  except Exception as e:
    logger.debug(bstack111ll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡸ࡫ࡷ࡬ࠥ࡬ࡩ࡭ࡧࠣࡰࡴࡩ࡫ࡪࡰࡪࠤ࡫ࡵࡲࠡࡏࡇ࠹ࠥ࡮ࡡࡴࡪࠣࡹࡵࡪࡡࡵࡧ࠽ࠤࢀࢃࠧે").format(str(e)))
def bstack1ll11lll1_opy_(self):
  return
def bstack1l111ll1ll_opy_(self):
  return
def bstack1lll1lll1l_opy_():
  global bstack111llll1_opy_
  bstack111llll1_opy_ = True
def bstack1111l11l1l_opy_(self):
  global FRAMEWORK_NAME
  global bstack1l11l11l1l_opy_
  global bstack111l11l1l_opy_
  bstack11111l11l_opy_ = bstack111l1l1l_opy_.bstack1ll1111l1_opy_(EVENTS.bstack11lll1111_opy_)
  try:
    if bstack111ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩૈ") in FRAMEWORK_NAME and self.session_id != None and bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧૉ"), bstack111ll_opy_ (u"ࠫࠬ૊")) != bstack111ll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ો"):
      bstack1ll111l1l1_opy_ = bstack111ll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ૌ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack111ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪ્ࠧ")
      if bstack1ll111l1l1_opy_ == bstack111ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ૎"):
        bstack111ll1ll1_opy_(logger)
      if self != None:
        bstack11ll1l1l1_opy_(self, bstack1ll111l1l1_opy_, bstack111ll_opy_ (u"ࠩ࠯ࠤࠬ૏").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack111ll_opy_ (u"ࠪࠫૐ")
    if bstack111ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ૑") in FRAMEWORK_NAME and getattr(threading.current_thread(), bstack111ll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ૒"), None):
      bstack11l11111l_opy_.bstack111l11l1_opy_(self, bstack111llll11_opy_, logger, wait=True)
    if bstack111ll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭૓") in FRAMEWORK_NAME:
      bstack1l1lll11l1_opy_.bstack11111lll1l_opy_(self)
    bstack111l1l1l_opy_.end(EVENTS.bstack11lll1111_opy_.value, bstack11111l11l_opy_ + bstack111ll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ૔"), bstack11111l11l_opy_ + bstack111ll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ૕"), status=True, failure=None, test_name=None)
  except Exception as e:
    logger.debug(bstack111ll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࠥ૖") + str(e))
    bstack111l1l1l_opy_.end(EVENTS.bstack11lll1111_opy_.value, bstack11111l11l_opy_ + bstack111ll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ૗"), bstack11111l11l_opy_ + bstack111ll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ૘"), status=False, failure=str(e), test_name=None)
  bstack111l11l1l_opy_(self)
  self.session_id = None
def bstack1lllll11l1_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack111ll11111_opy_
    global FRAMEWORK_NAME
    command_executor = kwargs.get(bstack111ll_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠨ૙"), bstack111ll_opy_ (u"࠭ࠧ૚"))
    bstack11lllllll1_opy_ = False
    if type(command_executor) == str and bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ૛") in command_executor:
      bstack11lllllll1_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫ૜") in str(getattr(command_executor, bstack111ll_opy_ (u"ࠩࡢࡹࡷࡲࠧ૝"), bstack111ll_opy_ (u"ࠪࠫ૞"))):
      bstack11lllllll1_opy_ = True
    else:
      kwargs = a11y.bstack1l1lll1ll_opy_(bstack1ll1lll1ll_opy_=kwargs, config=CONFIG)
      return bstack1lllll1ll1_opy_(self, *args, **kwargs)
    if bstack11lllllll1_opy_:
      bstack11ll11l11_opy_ = TestHubUtils.bstack11ll11l1ll_opy_(CONFIG, FRAMEWORK_NAME)
      if kwargs.get(bstack111ll_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ૟")):
        kwargs[bstack111ll_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ૠ")] = bstack111ll11111_opy_(kwargs[bstack111ll_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧૡ")], FRAMEWORK_NAME, CONFIG, bstack11ll11l11_opy_)
      elif kwargs.get(bstack111ll_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧૢ")):
        kwargs[bstack111ll_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨૣ")] = bstack111ll11111_opy_(kwargs[bstack111ll_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ૤")], FRAMEWORK_NAME, CONFIG, bstack11ll11l11_opy_)
  except Exception as e:
    logger.error(bstack111ll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡘࡊࡋࠡࡥࡤࡴࡸࡀࠠࡼࡿࠥ૥").format(str(e)))
  return bstack1lllll1ll1_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack1l11ll1ll1_opy_, stage=STAGE.bstack1l1l11l1l_opy_, bstack1111l11lll_opy_=SESSION_NAME)
def bstack1ll111ll1l_opy_(self, command_executor=bstack111ll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳࠶࠸࠷࠯࠲࠱࠴࠳࠷࠺࠵࠶࠷࠸ࠧ૦"), *args, **kwargs):
  global bstack1l11l11l1l_opy_
  global bstack11l1l1l1l1_opy_
  bstack1111lllll1_opy_ = bstack1lllll11l1_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack111ll111_opy_.on():
    return bstack1111lllll1_opy_
  try:
    if isinstance(command_executor, (str, bytes)):
      bstack1l1ll1111l_opy_ = str(command_executor)
    else:
      bstack1l1ll1111l_opy_ = str(
        getattr(command_executor, bstack111ll_opy_ (u"ࠬࡥࡵࡳ࡮ࠪ૧"), None)
        or getattr(getattr(command_executor, bstack111ll_opy_ (u"࠭࡟ࡤ࡮࡬ࡩࡳࡺ࡟ࡤࡱࡱࡪ࡮࡭ࠧ૨"), None), bstack111ll_opy_ (u"ࠧࡳࡧࡰࡳࡹ࡫࡟ࡴࡧࡵࡺࡪࡸ࡟ࡢࡦࡧࡶࠬ૩"), None)
        or bstack111ll_opy_ (u"ࠨࠩ૪")
      )
    logger.debug(bstack111ll_opy_ (u"ࠩࡋࡹࡧࠦࡕࡓࡎࠣ࡭ࡸࠦ࠭ࠡࡽࢀࠫ૫").format(bstack1l1ll1111l_opy_.split(bstack111ll_opy_ (u"ࠪࡄࠬ૬"))[-1] if bstack111ll_opy_ (u"ࠫࡅ࠭૭") in bstack1l1ll1111l_opy_ else bstack1l1ll1111l_opy_))
    if bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨ૮") in bstack1l1ll1111l_opy_:
      global_config.bstack1l1l1llll1_opy_(bstack111ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ૯"), True)
  except Exception as e:
    logger.error(bstack111ll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡩࡨࡦࡥ࡮࡭ࡳ࡭ࠠࡤࡱࡰࡱࡦࡴࡤࠡࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧ૰").format(str(e)))
    pass
  if (isinstance(command_executor, str) and bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫ૱") in command_executor):
    global_config.bstack1l1l1llll1_opy_(bstack111ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪ૲"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1ll1ll11_opy_ = getattr(threading.current_thread(), bstack111ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡗࡩࡸࡺࡍࡦࡶࡤࠫ૳"), None)
  bstack11l1l11l_opy_ = {}
  if self.capabilities is not None:
    bstack11l1l11l_opy_[bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧࠪ૴")] = self.capabilities.get(bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ૵"))
    bstack11l1l11l_opy_[bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ૶")] = self.capabilities.get(bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ૷"))
    bstack11l1l11l_opy_[bstack111ll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡠࡱࡳࡸ࡮ࡵ࡮ࡴࠩ૸")] = self.capabilities.get(bstack111ll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧૹ"))
  if CONFIG.get(bstack111ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪૺ"), False) and a11y.bstack1lll1l1l1_opy_(bstack11l1l11l_opy_):
    threading.current_thread().a11yPlatform = True
  if bstack111ll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫૻ") in FRAMEWORK_NAME or bstack111ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫૼ") in FRAMEWORK_NAME:
    TestHubHandler.send_cbt_info(self)
  if bstack111ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭૽") in FRAMEWORK_NAME and bstack1ll1ll11_opy_ and bstack1ll1ll11_opy_.get(bstack111ll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ૾"), bstack111ll_opy_ (u"ࠨࠩ૿")) == bstack111ll_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ଀"):
    TestHubHandler.send_cbt_info(self)
  bstack1l11l11l1l_opy_ = self.session_id
  with bstack1111ll1lll_opy_:
    bstack11l1l1l1l1_opy_.append(self)
  return bstack1111lllll1_opy_
def bstack11lll1l11_opy_(args):
  return bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵࠫଁ") in str(args)
def bstack11l111l111_opy_(self, driver_command, *args, **kwargs):
  global bstack1ll1l1ll1_opy_
  global bstack1l11ll11l_opy_
  bstack111l1l111l_opy_ = bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨଂ"), None) and bstack1ll11l1ll1_opy_(
          threading.current_thread(), bstack111ll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫଃ"), None)
  bstack1llllll111l_opy_ = bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭଄"), None) and bstack1ll11l1ll1_opy_(
          threading.current_thread(), bstack111ll_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩଅ"), None)
  bstack1l1ll111_opy_ = getattr(self, bstack111ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨଆ"), None) != None and getattr(self, bstack111ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩଇ"), None) == True
  bstack1lll1lll1_opy_ = str(FRAMEWORK_NAME).lower()
  bstack11ll11l1l_opy_ = not bstack1l11ll11l_opy_ and bstack111ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪଈ") in CONFIG and CONFIG[bstack111ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫଉ")] == True and accessibility_scripts.bstack111l11ll1_opy_(driver_command) and (bstack1l1ll111_opy_ or bstack111l1l111l_opy_ or bstack1llllll111l_opy_) and not bstack11lll1l11_opy_(args)
  if bstack111ll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨ࠭ଊ") in bstack1lll1lll1_opy_:
    bstack1l11ll11l1_opy_ = a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX)
    bstack11ll11l1l_opy_ =  not bstack1l11ll11l_opy_ and bstack1l11ll11l1_opy_ and accessibility_scripts.bstack111l11ll1_opy_(driver_command) and (bstack1l1ll111_opy_ or bstack111l1l111l_opy_ or bstack1llllll111l_opy_) and not bstack11lll1l11_opy_(args)
  if bstack11ll11l1l_opy_:
    try:
      bstack1l11ll11l_opy_ = True
      logger.debug(bstack111ll_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡨࡲࡶࠥࢁࡽࠨଋ").format(driver_command))
      bstack1l11ll11ll_opy_ = perform_scan(self, driver_command=driver_command)
      logger.debug(bstack1l11ll11ll_opy_)
      try:
        log_data = {
          bstack111ll_opy_ (u"ࠢࡳࡧࡴࡹࡪࡹࡴࠣଌ"): {
            bstack111ll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤ଍"): bstack111ll_opy_ (u"ࠤࡄ࠵࠶࡟࡟ࡔࡅࡄࡒࠧ଎"),
            bstack111ll_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡧࡷࡩࡷࡹࠢଏ"): [
              {
                bstack111ll_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦଐ"): driver_command
              }
            ]
          },
          bstack111ll_opy_ (u"ࠧࡸࡥࡴࡲࡲࡲࡸ࡫ࠢ଑"): {
            bstack111ll_opy_ (u"ࠨࡢࡰࡦࡼࠦ଒"): {
              bstack111ll_opy_ (u"ࠢ࡮ࡵࡪࠦଓ"): bstack1l11ll11ll_opy_.get(bstack111ll_opy_ (u"ࠣ࡯ࡶ࡫ࠧଔ"), bstack111ll_opy_ (u"ࠤࠥକ")) if isinstance(bstack1l11ll11ll_opy_, dict) else bstack111ll_opy_ (u"ࠥࠦଖ"),
              bstack111ll_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧଗ"): bstack1l11ll11ll_opy_.get(bstack111ll_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨଘ"), True) if isinstance(bstack1l11ll11ll_opy_, dict) else True
            }
          }
        }
        logger.debug(bstack111ll_opy_ (u"࠭ࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡤࡣࡱࠤࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡ࡮ࡲ࡫ࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠧଙ").format(log_data))
        automation_logger.info(json.dumps(log_data, separators=(bstack111ll_opy_ (u"ࠧ࠭ࠩଚ"), bstack111ll_opy_ (u"ࠨ࠼ࠪଛ"))))
      except Exception as bstack1111l1llll_opy_:
        logger.debug(bstack111ll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡲ࡯ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡧࡦࡴࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠩଜ").format(str(bstack1111l1llll_opy_)))
    except Exception as err:
      logger.debug(bstack111ll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡦࡴࡩࡳࡷࡳࠠࡴࡥࡤࡲࠥࢁࡽࠨଝ").format(str(err)))
    bstack1l11ll11l_opy_ = False
  response = bstack1ll1l1ll1_opy_(self, driver_command, *args, **kwargs)
  bstack1l1ll1ll11_opy_ = (
    (bstack111ll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪଞ") in bstack1lll1lll1_opy_ or bstack111ll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬଟ") in bstack1lll1lll1_opy_) and bstack111ll111_opy_.on()
  ) or (bstack111ll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡧࡦࡰࡨࡶ࡮ࡩࠧଠ") in bstack1lll1lll1_opy_)
  if bstack1l1ll1ll11_opy_:
    try:
      if driver_command == bstack111ll_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫଡ"):
        bstack1lllllllll_opy_ = TestHubHandler.current_test_uuid()
        if not bstack1lllllllll_opy_:
          bstack1lllllllll_opy_ = bstack111ll111_opy_.current_hook_uuid()
        if not bstack1lllllllll_opy_ and bstack111ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩଢ") in bstack1lll1lll1_opy_:
          bstack1lllllllll_opy_ = getattr(threading.current_thread(), bstack111ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ଣ"), None)
        if bstack1lllllllll_opy_:
          bstack1lll11llll_opy_ = response.get(bstack111ll_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩତ"), None) if isinstance(response, dict) else None
          if bstack1lll11llll_opy_ and isinstance(bstack1lll11llll_opy_, str) and len(bstack1lll11llll_opy_) > 0:
            if bstack111ll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠬଥ") in bstack1lll1lll1_opy_:
              try:
                from browserstack_sdk.sdk_cli.cli import cli
                if cli and cli.is_running() and cli.bstack111111ll1l_opy_:
                  _1l1111lll1_opy_(cli, bstack1lll11llll_opy_, bstack1lllllllll_opy_)
                else:
                  logger.debug(bstack111ll_opy_ (u"࡙ࠬࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠢࡱࡳࡹࠦࡳࡦࡰࡷ࠾ࠥࡉࡌࡊࠢࡱࡳࡹࠦࡲࡦࡣࡧࡽࠬଦ"))
              except Exception as bstack11ll1l1l1l_opy_:
                logger.debug(bstack111ll_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡳࡪࠠࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠤࡻ࡯ࡡࠡࡩࡕࡔࡈࡀࠠࡼࡿࠪଧ").format(str(bstack11ll1l1l1l_opy_)))
            else:
              TestHubHandler.bstack1lllll11lll_opy_({
                  bstack111ll_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭ନ"): bstack1lll11llll_opy_,
                  bstack111ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ଩"): bstack1lllllllll_opy_
              })
        else:
          logger.debug(bstack111ll_opy_ (u"ࠩࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠦࡣࡢࡲࡷࡹࡷ࡫ࡤࠡࡤࡸࡸࠥࡴ࡯ࠡࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨࠤ࡫ࡵࡲࠡࡽࢀࠫପ").format(bstack1lll1lll1_opy_))
    except Exception as e:
      logger.debug(bstack111ll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡰࡧࠤࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴ࠻ࠢࡾࢁࠬଫ").format(str(e)))
  return response
def _1l1111lll1_opy_(cli, bstack1lll11llll_opy_, bstack1lllllllll_opy_):
  from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack11l1l1l1ll_opy_
  bstack1llllllll_opy_ = None
  try:
    if cli and cli.test_framework and hasattr(cli.test_framework, bstack111ll_opy_ (u"ࠫ࡬࡫ࡴࡠࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࠩବ")):
      bstack1llllllll_opy_ = cli.test_framework.get_current_test_instance()
  except Exception as e:
    logger.debug(bstack111ll_opy_ (u"࡙ࠬࡣࡳࡧࡨࡲࡸ࡮࡯ࡵ࠼ࠣࡇࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡧࡦࡶࠣࡸࡪࡹࡴࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠽ࠤࢀࢃࠧଭ").format(e))
  if bstack1llllllll_opy_ and cli.bstack1ll1lll1l_opy_:
    entry = bstack11l1l1l1ll_opy_(TestFramework.KIND_SCREENSHOT, bstack1lll11llll_opy_)
    cli.bstack1ll1lll1l_opy_.bstack1l1111ll1l_opy_(bstack1llllllll_opy_, [entry])
    logger.debug(bstack111ll_opy_ (u"࠭ࡓࡤࡴࡨࡩࡳࡹࡨࡰࡶࠣࡷࡪࡴࡴࠡࡸ࡬ࡥࠥ࡭ࡒࡑࡅࠣࡪࡴࡸࠠࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪ࠽ࡼࡿࠪମ").format(bstack1lllllllll_opy_))
  else:
    logger.debug(bstack111ll_opy_ (u"ࠧࡔࡥࡵࡩࡪࡴࡳࡩࡱࡷࠤࡳࡵࡴࠡࡵࡨࡲࡹࡀࠠࡵࡧࡶࡸࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣࡩࡻ࡫࡮ࡵࡡࡧ࡭ࡸࡶࡡࡵࡥ࡫ࡩࡷࡃࡻࡾࠩଯ").format(
      bstack1llllllll_opy_ is not None, cli.bstack1ll1lll1l_opy_ is not None))
def bstack1lll11l1l_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack1l11l11l1l_opy_
  global PLATFORM_INDEX
  global SESSION_NAME
  global PARALLELISE_VANILLA_PYTHON
  global PARALLELISE_THREADING_PYTHON
  global FRAMEWORK_NAME
  global bstack1lllll1ll1_opy_
  global bstack11l1l1l1l1_opy_
  global bstack11l11ll111_opy_
  global bstack111llll11_opy_
  bstack11111l11l_opy_ = bstack111l1l1l_opy_.bstack1ll1111l1_opy_(EVENTS.bstack111lllll_opy_.value)
  if os.getenv(bstack111ll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ର")) is not None and a11y.bstack111lll11ll_opy_(CONFIG) is None:
    CONFIG[bstack111ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ଱")] = True
  CONFIG[bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬଲ")] = str(FRAMEWORK_NAME) + str(__version__)
  bstack1ll11l1lll_opy_ = os.environ[bstack111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩଳ")]
  bstack11ll11l11_opy_ = TestHubUtils.bstack11ll11l1ll_opy_(CONFIG, FRAMEWORK_NAME)
  CONFIG[bstack111ll_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ଴")] = bstack1ll11l1lll_opy_
  CONFIG[bstack111ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨଵ")] = bstack11ll11l11_opy_
  if CONFIG.get(bstack111ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧଶ"),bstack111ll_opy_ (u"ࠨࠩଷ")) and bstack111ll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨସ") in FRAMEWORK_NAME:
    CONFIG[bstack111ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪହ")].pop(bstack111ll_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ଺"), None)
    CONFIG[bstack111ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ଻")].pop(bstack111ll_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨ଼ࠫ"), None)
  command_executor = bstack1lllll1l1ll_opy_()
  logger.debug(bstack1llllllll1_opy_.format(command_executor))
  proxy = bstack1ll1l11lll_opy_(CONFIG, proxy)
  bstack1l1l11111_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
  try:
    if PARALLELISE_VANILLA_PYTHON is True:
      bstack1l1l11111_opy_ = int(multiprocessing.current_process().name)
    elif PARALLELISE_THREADING_PYTHON is True:
      bstack1l1l11111_opy_ = int(threading.current_thread().name)
  except:
    bstack1l1l11111_opy_ = 0
  bstack1111l1l1l1_opy_ = get_caps(CONFIG, bstack1l1l11111_opy_)
  logger.debug(CONFIG_FILE_CONTENT.format(str(bstack1111l1l1l1_opy_)))
  if bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫଽ") in CONFIG and bstack1lllll11ll1_opy_(CONFIG[bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬା")]):
    update_caps_for_local(bstack1111l1l1l1_opy_)
  if a11y.is_enabled_platform(CONFIG, bstack1l1l11111_opy_) and a11y.is_platform_supported(bstack1111l1l1l1_opy_, options, desired_capabilities, CONFIG):
    threading.current_thread().a11yPlatform = True
    if (cli.accessibility is None or not cli.accessibility.is_enabled() or bstack111ll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠪି") in FRAMEWORK_NAME):
      a11y.set_capabilities(bstack1111l1l1l1_opy_, CONFIG)
  if desired_capabilities:
    bstack1lll11lll1_opy_ = bstack1l1ll1ll1_opy_(desired_capabilities)
    bstack1lll11lll1_opy_[bstack111ll_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪୀ")] = bstack11lll11lll_opy_(CONFIG)
    bstack1l1llll11l_opy_ = get_caps(bstack1lll11lll1_opy_)
    if bstack1l1llll11l_opy_:
      bstack1111l1l1l1_opy_ = update(bstack1l1llll11l_opy_, bstack1111l1l1l1_opy_)
    desired_capabilities = None
  if options:
    bstack111l111ll_opy_(options, bstack1111l1l1l1_opy_)
  if not options:
    options = bstack11ll1l1l11_opy_(bstack1111l1l1l1_opy_)
  try:
    if bstack111111lll_opy_:
      def _1ll1ll1111_opy_(bstack1ll1111l_opy_):
        if not isinstance(bstack1ll1111l_opy_, dict):
          return
        for _11l1l1111_opy_ in list(bstack1ll1111l_opy_.keys()):
          _1l11111l1_opy_ = bstack1ll1111l_opy_[_11l1l1111_opy_]
          if _1l11111l1_opy_ is None:
            bstack1ll1111l_opy_.pop(_11l1l1111_opy_, None)
          elif isinstance(_1l11111l1_opy_, dict):
            _1ll1ll1111_opy_(_1l11111l1_opy_)
      _1ll1ll1111_opy_(bstack1111l1l1l1_opy_)
      _1ll1ll1111_opy_(desired_capabilities)
      if options is not None and hasattr(options, bstack111ll_opy_ (u"ࠫࡤࡩࡡࡱࡵࠪୁ")):
        _1ll1ll1111_opy_(options._caps)
  except Exception as e:
    logger.debug(bstack111ll_opy_ (u"ࠧࡳ࡯ࡥࡡ࡬ࡲ࡮ࡺࠨࠪࠢࡳࡳࡸࡺ࠭ࡰࡲࡷ࡭ࡴࡴࡳࠡࡲࡵࡹࡳ࡫ࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡽࢀࠦୂ").format(e))
  if bstack111111lll_opy_:
    options = bstack1llllll11l1_opy_(options)
  bstack111llll11_opy_ = CONFIG.get(bstack111ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩୃ"))[bstack1l1l11111_opy_]
  if proxy and bstack111111111_opy_() >= version.parse(bstack111ll_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧୄ")):
    options.proxy(proxy)
  if options and bstack111111111_opy_() >= version.parse(bstack111ll_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ୅")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack111111111_opy_() < version.parse(bstack111ll_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ୆")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1111l1l1l1_opy_)
  logger.info(bstack111l111lll_opy_)
  bstack11ll1l1l_opy_.end(EVENTS.bstack11l1l1ll11_opy_.value, EVENTS.bstack11l1l1ll11_opy_.value + bstack111ll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥେ"), EVENTS.bstack11l1l1ll11_opy_.value + bstack111ll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤୈ"), status=True, failure=None, test_name=SESSION_NAME)
  if bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡰࡳࡱࡩ࡭ࡱ࡫ࠧ୉") in kwargs:
    del kwargs[bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡱࡴࡲࡪ࡮ࡲࡥࠨ୊")]
  bstack111l1l1l_opy_.end(EVENTS.bstack111lllll_opy_.value, bstack11111l11l_opy_ + bstack111ll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢୋ"), bstack11111l11l_opy_ + bstack111ll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨୌ"), status=True, failure=None, test_name=SESSION_NAME)
  try:
    if bstack111111111_opy_() >= version.parse(bstack111ll_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱୍ࠩ")):
      bstack1lllll1ll1_opy_(self, command_executor=command_executor,
                options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
    elif bstack111111111_opy_() >= version.parse(bstack111ll_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩ୎")):
      bstack1lllll1ll1_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities, options=options,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    elif bstack111111111_opy_() >= version.parse(bstack111ll_opy_ (u"ࠫ࠷࠴࠵࠴࠰࠳ࠫ୏")):
      bstack1lllll1ll1_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    else:
      bstack1lllll1ll1_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive)
  except Exception as bstack11l1l1lll1_opy_:
    logger.error(bstack111ll1l1ll_opy_.format(bstack111ll_opy_ (u"ࠬࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠫ୐"), str(bstack11l1l1lll1_opy_)))
    raise bstack11l1l1lll1_opy_
  bstack11111l11l_opy_ = bstack111l1l1l_opy_.bstack1ll1111l1_opy_(EVENTS.bstack1l11ll1ll1_opy_.value)
  if a11y.is_enabled_platform(CONFIG, bstack1l1l11111_opy_) and a11y.is_platform_supported(self.capabilities, options, desired_capabilities):
    if CONFIG[bstack111ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨ୑")][bstack111ll_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭୒")] == True:
      threading.current_thread().appA11yPlatform = True
      if cli.accessibility is None or not cli.accessibility.is_enabled() or bstack111ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩ୓") in FRAMEWORK_NAME:
        a11y.set_capabilities(bstack1111l1l1l1_opy_, CONFIG)
  try:
    bstack1ll11lll1l_opy_ = bstack111ll_opy_ (u"ࠩࠪ୔")
    if bstack111111111_opy_() >= version.parse(bstack111ll_opy_ (u"ࠪ࠸࠳࠶࠮࠱ࡤ࠴ࠫ୕")):
      if self.caps is not None:
        bstack1ll11lll1l_opy_ = self.caps.get(bstack111ll_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦୖ"))
    else:
      if self.capabilities is not None:
        bstack1ll11lll1l_opy_ = self.capabilities.get(bstack111ll_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧୗ"))
    if bstack1ll11lll1l_opy_:
      bstack11lllll111_opy_(bstack1ll11lll1l_opy_)
      if bstack111111111_opy_() <= version.parse(bstack111ll_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭୘")):
        if bstack11111l1111_opy_.startswith(bstack111ll_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࠨ୙")) or bstack11111l1111_opy_.startswith(bstack111ll_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࠪ୚")):
          self.command_executor._url = bstack11111l1111_opy_
        else:
          self.command_executor._url = bstack111ll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ୛") + bstack11111l1111_opy_ + bstack111ll_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢଡ଼")
      else:
        self.command_executor._url = bstack111ll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨଢ଼") + bstack1ll11lll1l_opy_ + bstack111ll_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨ୞")
      logger.debug(bstack1l111l111l_opy_.format(bstack1ll11lll1l_opy_))
    else:
      logger.debug(bstack1l1l1111_opy_.format(bstack111ll_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢୟ")))
  except Exception as e:
    logger.debug(bstack1l1l1111_opy_.format(e))
  if bstack111ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ୠ") in FRAMEWORK_NAME:
    bstack11lll1ll1l_opy_(PLATFORM_INDEX, bstack11l11ll111_opy_)
  bstack1l11l11l1l_opy_ = self.session_id
  if bstack111ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨୡ") in FRAMEWORK_NAME or bstack111ll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩୢ") in FRAMEWORK_NAME or bstack111ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩୣ") in FRAMEWORK_NAME or bstack111ll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠬ୤") in FRAMEWORK_NAME:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack1ll1ll11_opy_ = getattr(threading.current_thread(), bstack111ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࡙࡫ࡳࡵࡏࡨࡸࡦ࠭୥"), None)
  if bstack111ll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭୦") in FRAMEWORK_NAME or bstack111ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭୧") in FRAMEWORK_NAME:
    TestHubHandler.send_cbt_info(self)
  if bstack111ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ୨") in FRAMEWORK_NAME and bstack1ll1ll11_opy_ and bstack1ll1ll11_opy_.get(bstack111ll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ୩"), bstack111ll_opy_ (u"ࠪࠫ୪")) == bstack111ll_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ୫"):
    TestHubHandler.send_cbt_info(self)
  with bstack1111ll1lll_opy_:
    bstack11l1l1l1l1_opy_.append(self)
  if bstack111ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ୬") in CONFIG and bstack111ll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ୭") in CONFIG[bstack111ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ୮")][bstack1l1l11111_opy_]:
    SESSION_NAME = CONFIG[bstack111ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ୯")][bstack1l1l11111_opy_][bstack111ll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ୰")]
  logger.debug(bstack1111l1ll1l_opy_.format(bstack1l11l11l1l_opy_))
  bstack111l1l1l_opy_.end(EVENTS.bstack1l11ll1ll1_opy_.value, bstack11111l11l_opy_ + bstack111ll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥୱ"), bstack11111l11l_opy_ + bstack111ll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ୲"), status=True, failure=None, test_name=SESSION_NAME)
ROBOT_PLAYWRIGHT_CDP_URL = None
bstack1111l11ll_opy_ = False
bstack1l1l1lll11_opy_ = None
def set_playwright_globals(**kwargs):
    bstack111ll_opy_ (u"ࠧࠨࠢࡊࡰ࡭ࡩࡨࡺࠠࡨ࡮ࡲࡦࡦࡲࡳࠡࡨࡵࡳࡲࠦ࡟ࡠ࡫ࡱ࡭ࡹࡥ࡟࠯ࡲࡼࠤ࡮ࡴࡴࡰࠢࡷ࡬࡮ࡹࠠ࡮ࡱࡧࡹࡱ࡫ࠧࡴࠢࡱࡥࡲ࡫ࡳࡱࡣࡦࡩ࠳ࠐࠠࠡࠢࠣࡇࡦࡲ࡬ࡦࡦࠣࡦࡾࠦ࡟ࡠ࡫ࡱ࡭ࡹࡥ࡟࠯ࡲࡼࠤࡧ࡫ࡦࡰࡴࡨࠤࡵࡧࡴࡤࡪࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠨࠪࠢࡶࡳࠥࡺࡨࡢࡶࠣࡱࡴࡪ࡟࡭ࡣࡸࡲࡨ࡮ࠊࠡࠢࠣࠤࡦࡴࡤࠡࡲࡤࡸࡨ࡮࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡨࡧ࡮ࠡࡣࡦࡧࡪࡹࡳࠡࡅࡒࡒࡋࡏࡇ࠭ࠢࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤࡔࡁࡎࡇ࠯ࠤࡪࡺࡣ࠯ࠤࠥࠦ୳")
    g = globals()
    for key, value in kwargs.items():
        g[key] = value
try:
  try:
    import Browser
    import os
    from subprocess import Popen
    from browserstack_sdk.__init__ import get_turboscale_playwright_url
    from browserstack_sdk.sdk_cli.utils.bstack1l11l11l1_opy_ import bstack111l1l11_opy_
    def bstack11ll1l11l_opy_(self, args, **kwargs):
      global CONFIG
      global SELENIUM_OR_PLAYWRIGHT_INSTALLED
      global ROBOT_PLAYWRIGHT_CDP_URL
      global bstack1111l11ll_opy_
      from browserstack_sdk.__init__ import LAUNCH_PATCH_ROBOT_PLAYWRIGHT
      if(bstack111ll_opy_ (u"ࠨࡩ࡯ࡦࡨࡼ࠳ࡰࡳࠣ୴") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack111ll_opy_ (u"ࠧࡿࠩ୵")), bstack111ll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ୶"), bstack111ll_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫ୷")), bstack111ll_opy_ (u"ࠪࡻࠬ୸")) as fp:
          fp.write(bstack111ll_opy_ (u"ࠦࠧ୹"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack111ll_opy_ (u"ࠧ࡯࡮ࡥࡧࡻࡣࡧࡹࡴࡢࡥ࡮࠲࡯ࡹࠢ୺")))):
          with open(args[1], bstack111ll_opy_ (u"࠭ࡲࠨ୻")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack111ll_opy_ (u"ࠧࡢࡵࡼࡲࡨࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡡࡱࡩࡼࡖࡡࡨࡧࠫࡧࡴࡴࡴࡦࡺࡷ࠰ࠥࡶࡡࡨࡧࠣࡁࠥࡼ࡯ࡪࡦࠣ࠴࠮࠭୼") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1lllll1l11_opy_)
            if bstack111ll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ୽") in CONFIG and str(CONFIG[bstack111ll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭୾")]).lower() != bstack111ll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩ୿"):
                cdpUrl = get_turboscale_playwright_url()
                LAUNCH_PATCH_ROBOT_PLAYWRIGHT = bstack111ll_opy_ (u"ࠫࠬ࠭ࠊ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱ࠍࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠷ࡠࠤࡂࡃ࠽ࠡࠩࡷࡶࡺ࡫ࠧ࠼ࠌࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭ࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࡠ࠿ࠏࡩ࡯࡯ࡵࡷࠤࡧࡹࡴࡢࡥ࡮ࡣࡨࡧࡰࡴࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠶ࡣ࠻ࠋࡥࡲࡲࡸࡺࠠࡱࡡ࡬ࡲࡩ࡫ࡸࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࡝ࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠶ࡢࡁࠊࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠶ࡠࠤࡂࡃ࠽ࠡࠩࡷࡶࡺ࡫ࠧ࠼ࠌࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰ࡶࡰ࡮ࡩࡥࠩ࠲࠯ࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠻ࠩ࠼ࠌࡦࡳࡳࡹࡴࠡ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢࠪ࠽ࠍࡧࡴࡴࡳࡵࠢࡲࡶ࡮࡭ࡩ࡯ࡣ࡯ࡣࡨ࡮ࡲࡰ࡯࡬ࡹࡲࡥ࡬ࡢࡷࡱࡧ࡭ࠦ࠽ࠡ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭࠯࡮ࡤࡹࡳࡩࡨ࠯ࡤ࡬ࡲࡩ࠮ࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠯࠻ࠋ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭࠯࡮ࡤࡹࡳࡩࡨࠡ࠿ࠣࡥࡸࡿ࡮ࡤࠢࠫࡰࡦࡻ࡮ࡤࡪࡒࡴࡹ࡯࡯࡯ࡵࠬࠤࡂࡄࠠࡼࡽࠍࠤࠥ࡯ࡦࠡࠪࠤࡦࡸࡺࡡࡤ࡭ࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠩࠡࡽࡾࠎࠥࠦࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡣࡺࡥ࡮ࡺࠠࡰࡴ࡬࡫࡮ࡴࡡ࡭ࡡࡦ࡬ࡷࡵ࡭ࡪࡷࡰࡣࡱࡧࡵ࡯ࡥ࡫ࠬࡱࡧࡵ࡯ࡥ࡫ࡓࡵࡺࡩࡰࡰࡶ࠭ࡀࠐࠠࠡࡿࢀࠎࠥࠦ࡬ࡦࡶࠣࡧࡦࡶࡳ࠼ࠌࠣࠤࡹࡸࡹࠡࡽࡾࠎࠥࠦࠠࠡࡥࡤࡴࡸࠦ࠽ࠡࡌࡖࡓࡓ࠴ࡰࡢࡴࡶࡩ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡩࡡࡱࡵࠬ࠿ࠏࠦࠠࡾࡿࠣࡧࡦࡺࡣࡩࠢࠫࡩࡽ࠯ࠠࡼࡽࠍࠤࠥࠦࠠࡤࡱࡱࡷࡴࡲࡥ࠯ࡧࡵࡶࡴࡸࠨࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴ࠼ࠥ࠰ࠥ࡫ࡸࠪ࠽ࠍࠤࠥࢃࡽࠋࠢࠣ࡭࡫ࠦࠨࡣࡵࡷࡥࡨࡱ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠩࠡࡽࡾࠎࠥࠦࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡣࡺࡥ࡮ࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮ࡤࡱࡱࡲࡪࡩࡴࡐࡸࡨࡶࡈࡊࡐࠩࡽࡾࠎࠥࠦࠠࠡࠢࠣࡩࡳࡪࡰࡰ࡫ࡱࡸ࡚ࡘࡌ࠻ࠢࠪࡿࡨࡪࡰࡖࡴ࡯ࢁࠬࠦࠫࠡࡧࡱࡧࡴࡪࡥࡖࡔࡌࡇࡴࡳࡰࡰࡰࡨࡲࡹ࠮ࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡤࡣࡳࡷ࠮࠯ࠬࠋࠢࠣࠤࠥࠦࠠ࠯࠰࠱ࡰࡦࡻ࡮ࡤࡪࡒࡴࡹ࡯࡯࡯ࡵࠍࠤࠥࠦࠠࡾࡿࠬ࠿ࠏࠦࠠࡾࡿࠍࠤࠥࡸࡥࡵࡷࡵࡲࠥࡧࡷࡢ࡫ࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡨࡵ࡮࡯ࡧࡦࡸ࠭ࢁࡻࠋࠢࠣࠤࠥࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵ࠼ࠣࠫࢀࡩࡤࡱࡗࡵࡰࢂ࠭ࠠࠬࠢࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩ࠭ࠌࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴࠌࠣࠤࢂࢃࠩ࠼ࠌࢀࢁࡀࠐࡣࡰࡰࡶࡸࠥࡵࡲࡪࡩ࡬ࡲࡦࡲ࡟ࡤࡱࡱࡲࡪࡩࡴࠡ࠿ࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷ࠲ࡧ࡯࡮ࡥࠪ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱ࠮ࡤࡪࡵࡳࡲ࡯ࡵ࡮ࠫ࠾ࠎ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡨࡵ࡮࡯ࡧࡦࡸࠥࡃࠠࡢࡵࡼࡲࡨࠦࠨࡤࡱࡱࡲࡪࡩࡴࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁࡻࠋࠢࠣ࡭࡫ࠦࠨࠢࡤࡶࡸࡦࡩ࡫ࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠮ࠦࡻࡼࠌࠣࠤࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥࡵࡲࡪࡩ࡬ࡲࡦࡲ࡟ࡤࡱࡱࡲࡪࡩࡴࠩࡥࡲࡲࡳ࡫ࡣࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠫ࠾ࠎࠥࠦࡽࡾࠌࠣࠤࡱ࡫ࡴࠡࡥࡤࡴࡸࡁࠊࠡࠢࡷࡶࡾࠦࡻࡼࠌࠣࠤࠥࠦࡣࡢࡲࡶࠤࡂࠦࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠪ࠽ࠍࠤࠥࢃࡽࠡࡥࡤࡸࡨ࡮ࠠࠩࡧࡻ࠭ࠥࢁࡻࠋࠢࠣࢁࢂࠐࠠࠡࡥࡲࡲࡸࡺࠠ࡮ࡱࡧ࡭࡫࡯ࡥࡥࡇࡱࡨࡵࡵࡩ࡯ࡶࠣࡁࠥ࠭ࡻࡤࡦࡳ࡙ࡷࡲࡽࠨࠢ࠮ࠤࡪࡴࡣࡰࡦࡨ࡙ࡗࡏࡃࡰ࡯ࡳࡳࡳ࡫࡮ࡵࠪࡍࡗࡔࡔ࠮ࡴࡶࡵ࡭ࡳ࡭ࡩࡧࡻࠫࡧࡦࡶࡳࠪࠫ࠾ࠎࠥࠦࡩࡧࠢࠫࡦࡸࡺࡡࡤ࡭ࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠬࠤࢀࢁࠊࠡࠢࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷࡓࡻ࡫ࡲࡄࡆࡓࠬࢀࢁࠊࠡࠢࠣࠤࠥࠦࡥ࡯ࡦࡳࡳ࡮ࡴࡴࡖࡔࡏ࠾ࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࠭ࠌࠣࠤࠥࠦࠠࠡ࠰࠱࠲ࡨࡵ࡮࡯ࡧࡦࡸࡔࡶࡴࡪࡱࡱࡷࠏࠦࠠࠡࠢࢀࢁ࠮ࡁࠊࠡࠢࢀࢁࠏࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦ࡯ࡳ࡫ࡪ࡭ࡳࡧ࡬ࡠࡥࡲࡲࡳ࡫ࡣࡵࠪࡾࡿࠏࠦࠠࠡࠢ࠱࠲࠳ࡩ࡯࡯ࡰࡨࡧࡹࡕࡰࡵ࡫ࡲࡲࡸ࠲ࠊࠡࠢࠣࠤࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࠻ࠢࡰࡳࡩ࡯ࡦࡪࡧࡧࡉࡳࡪࡰࡰ࡫ࡱࡸࠏࠦࠠࡾࡿࠬ࠿ࠏࢃࡽ࠼ࠌ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࠏ࠭ࠧࠨ஀").format(cdpUrl=cdpUrl)
            lines.insert(1, LAUNCH_PATCH_ROBOT_PLAYWRIGHT)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack111ll_opy_ (u"ࠧ࡯࡮ࡥࡧࡻࡣࡧࡹࡴࡢࡥ࡮࠲࡯ࡹࠢ஁")), bstack111ll_opy_ (u"࠭ࡷࠨஂ")) as bstack1ll11lll_opy_:
              bstack1ll11lll_opy_.writelines(lines)
        CONFIG[bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩஃ")] = str(FRAMEWORK_NAME) + str(__version__)
        bstack1ll11l1lll_opy_ = os.environ[bstack111ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭஄")]
        bstack11ll11l11_opy_ = TestHubUtils.bstack11ll11l1ll_opy_(CONFIG, FRAMEWORK_NAME)
        CONFIG[bstack111ll_opy_ (u"ࠩࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬஅ")] = bstack1ll11l1lll_opy_
        CONFIG[bstack111ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬஆ")] = bstack11ll11l11_opy_
        bstack1l1l11111_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
        try:
          if PARALLELISE_VANILLA_PYTHON is True:
            bstack1l1l11111_opy_ = int(multiprocessing.current_process().name)
          elif PARALLELISE_THREADING_PYTHON is True:
            bstack1l1l11111_opy_ = int(threading.current_thread().name)
        except Exception:
          bstack1l1l11111_opy_ = 0
        CONFIG[bstack111ll_opy_ (u"ࠦࡺࡹࡥࡘ࠵ࡆࠦஇ")] = False
        CONFIG[bstack111ll_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦஈ")] = True
        bstack1l11ll1l1_opy_ = bstack111l1l11_opy_(bstack1l1l11111_opy_)
        if bstack1l11ll1l1_opy_ is not None:
          import bstack_utils.constants as _11l11l1l_opy_
          _1111l1l111_opy_ = bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧஉ") if bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨஊ") in bstack1l11ll1l1_opy_ else bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭஋")
          _1ll1l1l11_opy_ = bstack1l11ll1l1_opy_.get(_1111l1l111_opy_, bstack111ll_opy_ (u"ࠩࠪ஌")).strip().lower()
          _1l111ll11_opy_ = _1ll1l1l11_opy_ in _11l11l1l_opy_.bstack1l1l111111_opy_
          if bstack1l11ll1l1_opy_.get(bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ஍")) and not _1l111ll11_opy_:
            bstack1l11ll1l1_opy_[bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪஎ")] = False
            _111llll11l_opy_ = [k for k in bstack1l11ll1l1_opy_ if k.startswith(bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫஏ"))]
            for k in _111llll11l_opy_:
              del bstack1l11ll1l1_opy_[k]
          bstack1ll11111_opy_ = bstack1l11ll1l1_opy_
          import urllib.parse
          if bstack111ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪஐ") in CONFIG and str(CONFIG[bstack111ll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ஑")]).lower() != bstack111ll_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧஒ"):
            ROBOT_PLAYWRIGHT_CDP_URL = get_turboscale_playwright_url() + urllib.parse.quote(json.dumps(bstack1ll11111_opy_))
          else:
            ROBOT_PLAYWRIGHT_CDP_URL = bstack111ll_opy_ (u"ࠩࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠫஓ") + urllib.parse.quote(json.dumps(bstack1ll11111_opy_))
          os.environ[bstack111ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡓࡇࡕࡔࡠࡒ࡚ࡣࡈࡊࡐࡠࡗࡕࡐࠬஔ")] = ROBOT_PLAYWRIGHT_CDP_URL
          bstack1111l11ll_opy_ = True
          from browserstack_sdk.sdk_cli.bstack11l111l1l_opy_ import bstack11l1l1l1_opy_
          from browserstack_sdk.sdk_cli.bstack111l11ll_opy_ import bstack11ll1l1ll_opy_
          instance = next(iter(bstack11l1l1l1_opy_.bstack111l11l1l1_opy_.values()), None)
          if instance:
            bstack11ll1l1ll_opy_.bstack11ll11l1_opy_(instance, bstack11ll1l1ll_opy_.bstack1ll111ll_opy_, bstack1l11ll1l1_opy_)
            bstack11ll1l1ll_opy_.bstack11ll11l1_opy_(instance, bstack11ll1l1ll_opy_.bstack1ll1llll1_opy_, ROBOT_PLAYWRIGHT_CDP_URL)
          try:
            from browserstack_sdk.sdk_cli.cli import cli as _1lllllll1l1_opy_
            from browserstack_sdk.sdk_cli.bstack11l111l1l_opy_ import bstack1ll1l1111l_opy_, bstack1l1l111lll_opy_
            _1lllllll1l1_opy_.bstack11l111l1l_opy_.bstack1ll1ll111_opy_(
              None,
              (instance, bstack111ll_opy_ (u"ࠫࡲࡵࡤࡠࡲࡲࡴࡪࡴࠧக")),
              (bstack1ll1l1111l_opy_.bstack111l1ll111_opy_, bstack1l1l111lll_opy_.PRE),
              None,
            )
          except Exception as e:
            logger.debug(bstack111ll_opy_ (u"ࠧࡳ࡯ࡥࡡࡳࡳࡵ࡫࡮࠻ࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡬ࡩࡳࡧࠣࡇࡗࡋࡁࡕࡇ࠱ࡔࡗࡋ࠺ࠡࡽࢀࠦ஖").format(e))
          logger.debug(bstack111ll_opy_ (u"ࠨ࡭ࡰࡦࡢࡴࡴࡶࡥ࡯࠼ࠣࡹࡸ࡯࡮ࡨࠢࡩ࡭ࡳࡧ࡬ࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡧࡴࡲࡱࠥࡊࡲࡪࡸࡨࡶࡎࡴࡩࡵࠤ஗"))
        else:
          bstack1ll11111_opy_ = get_caps(CONFIG, bstack1l1l11111_opy_)
          if CONFIG.get(bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ஘")):
            update_caps_for_local(bstack1ll11111_opy_)
            bstack1ll11111_opy_[bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩங")] = os.environ[bstack111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫச")]
          logger.debug(bstack111ll_opy_ (u"ࠥࡱࡴࡪ࡟ࡱࡱࡳࡩࡳࡀࠠࡅࡴ࡬ࡺࡪࡸࡉ࡯࡫ࡷࠤࡺࡴࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦ࠮ࠣࡪࡦࡲ࡬ࡪࡰࡪࠤࡧࡧࡣ࡬ࠢࡷࡳࠥ࡭ࡥࡵࡡࡦࡥࡵࡹࠢ஛"))
        logger.debug(CONFIG_FILE_CONTENT.format(str(bstack1ll11111_opy_)))
        if bstack111ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧஜ") in CONFIG and bstack111ll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ஝") in CONFIG[bstack111ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩஞ")][bstack1l1l11111_opy_]:
          SESSION_NAME = CONFIG[bstack111ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪட")][bstack1l1l11111_opy_][bstack111ll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭஠")]
        from bstack_utils.helper import bstack11l1ll1l_opy_
        args.append(bstack111ll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ஡") if bstack11l1ll1l_opy_(CONFIG) else bstack111ll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩ஢"))
        args.append(str(bstack1ll11111_opy_.get(bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪண"), False)).lower())
        args.append(os.path.join(os.path.expanduser(bstack111ll_opy_ (u"ࠬࢄࠧத")), bstack111ll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭஥"), bstack111ll_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩ஦")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1ll11111_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack111ll_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥ஧"))
      SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
      return bstack11l1ll1lll_opy_(self, args, **kwargs)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1l111l11l1_opy_(self,
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
    CONFIG[bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫந")] = str(FRAMEWORK_NAME) + str(__version__)
    bstack1ll11l1lll_opy_ = os.environ[bstack111ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨன")]
    bstack11ll11l11_opy_ = TestHubUtils.bstack11ll11l1ll_opy_(CONFIG, FRAMEWORK_NAME)
    CONFIG[bstack111ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧப")] = bstack1ll11l1lll_opy_
    CONFIG[bstack111ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧ஫")] = bstack11ll11l11_opy_
    bstack1l1l11111_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
    try:
      if PARALLELISE_VANILLA_PYTHON is True:
        bstack1l1l11111_opy_ = int(multiprocessing.current_process().name)
      elif PARALLELISE_THREADING_PYTHON is True:
        bstack1l1l11111_opy_ = int(threading.current_thread().name)
    except Exception:
      bstack1l1l11111_opy_ = 0
    CONFIG[bstack111ll_opy_ (u"ࠨࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧ஬")] = True
    bstack1111l1l1l1_opy_ = get_caps(CONFIG, bstack1l1l11111_opy_)
    bstack11lll11l11_opy_ = bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ஭") if bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩம") in bstack1111l1l1l1_opy_ else bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧய")
    bstack111l1llll1_opy_ = False
    try:
        from bstack_utils import accessibility as a11y
        import bstack_utils.constants as bstack1l11l1ll1_opy_
        bstack1l111l1lll_opy_ = bstack1111l1l1l1_opy_.get(bstack11lll11l11_opy_, bstack111ll_opy_ (u"ࠪࠫர")).strip().lower()
        browser_version = str(bstack1111l1l1l1_opy_.get(bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ற"), bstack1111l1l1l1_opy_.get(bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ல"), bstack111ll_opy_ (u"࠭ࠧள")))).strip()
        bstack1ll111ll1_opy_ = bstack1l111l1lll_opy_ in bstack1l11l1ll1_opy_.bstack1l1l111111_opy_
        min_version = bstack1l11l1ll1_opy_.MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION
        if not browser_version or browser_version.lower().startswith(bstack111ll_opy_ (u"ࠧ࡭ࡣࡷࡩࡸࡺࠧழ")):
            bstack1l1llll111_opy_ = True
        else:
            major = browser_version.split(bstack111ll_opy_ (u"ࠨ࠰ࠪவ"))[0]
            bstack1l1llll111_opy_ = major.isdigit() and int(major) > min_version
        if not bstack1l1llll111_opy_:
            logger.warning(bstack111ll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࠣࡺࡪࡸࡳࡪࡱࡱࠤ࡬ࡸࡥࡢࡶࡨࡶࠥࡺࡨࡢࡰࠣࡿࢂ࠴ࠠࡄࡷࡵࡶࡪࡴࡴࠡࡸࡨࡶࡸ࡯࡯࡯࠼ࠣࡿࢂࠨஶ").format(min_version, browser_version))
        if a11y.is_enabled_platform(CONFIG, bstack1l1l11111_opy_) and bstack1ll111ll1_opy_ and bstack1l1llll111_opy_ and a11y.is_platform_supported(bstack1111l1l1l1_opy_, options=None, config=CONFIG):
            bstack111l1llll1_opy_ = True
            import browserstack_sdk
            browserstack_sdk.CONFIG[bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩஷ")] = True
            bstack1111l1l1l1_opy_[bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪஸ")] = True
            if CONFIG.get(bstack111ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧஹ")):
                bstack1111l1l1l1_opy_[bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧ஺")] = CONFIG[bstack111ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩ஻")]
            import json as _json
            bstack1l11lllll1_opy_ = os.getenv(bstack111ll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭஼"))
            bstack11111l11ll_opy_ = bstack1111l1l1l1_opy_.get(bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳ࠯ࡣࡸࡸ࡭࡚࡯࡬ࡧࡱࠫ஽"))
            if not bstack1l11lllll1_opy_ and bstack11111l11ll_opy_:
                os.environ[bstack111ll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨா")] = bstack11111l11ll_opy_
                bstack1l11lllll1_opy_ = bstack11111l11ll_opy_
            if bstack1l11lllll1_opy_:
                bstack1111l1l1l1_opy_[bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵ࠱ࡥࡺࡺࡨࡕࡱ࡮ࡩࡳ࠭ி")] = bstack1l11lllll1_opy_
            bstack1l11111l_opy_ = _json.loads(os.getenv(bstack111ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ீ"), bstack111ll_opy_ (u"࠭ࡻࡾࠩு"))).get(bstack111ll_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨூ"))
            if bstack1l11111l_opy_:
                bstack1111l1l1l1_opy_[bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹ࠮ࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ௃")] = bstack1l11111l_opy_
            bstack1111l1l1l1_opy_.pop(bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ௄"), None)
            bstack1111l1l1l1_opy_.pop(bstack111ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ௅"), None)
            bstack1111l1l1l1_opy_.pop(bstack111ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫெ"), None)
            logger.debug(bstack111ll_opy_ (u"ࠧࡇ࠱࠲ࡻࠣࡩࡳࡧࡢ࡭ࡧࡧࠤ࡫ࡵࡲࠡࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࠨࡼࡿࠣࡿࢂ࠯ࠢே").format(
                bstack1l111l1lll_opy_, browser_version))
    except Exception as e:
        bstack111l1llll1_opy_ = False
        logger.debug(bstack111ll_opy_ (u"ࠨࡁ࠲࠳ࡼࠤࡩ࡫ࡴࡦࡥࡷ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡽࢀࠦை").format(str(e)))
    logger.debug(CONFIG_FILE_CONTENT.format(str(bstack1111l1l1l1_opy_)))
    if CONFIG.get(bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ௉")):
      update_caps_for_local(bstack1111l1l1l1_opy_)
    if bstack111ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫொ") in CONFIG and bstack111ll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧோ") in CONFIG[bstack111ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ௌ")][bstack1l1l11111_opy_]:
      SESSION_NAME = CONFIG[bstack111ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹ்ࠧ")][bstack1l1l11111_opy_][bstack111ll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ௎")]
    import urllib
    import json
    if bstack111ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ௏") in CONFIG and str(CONFIG[bstack111ll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫௐ")]).lower() != bstack111ll_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧ௑"):
        bstack1l1ll11111_opy_ = get_turboscale_playwright_url()
        cdpUrl = bstack1l1ll11111_opy_ + urllib.parse.quote(json.dumps(bstack1111l1l1l1_opy_))
    else:
        cdpUrl = bstack111ll_opy_ (u"ࠩࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠫ௒") + urllib.parse.quote(json.dumps(bstack1111l1l1l1_opy_))
    try:
        from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
        PlaywrightDriverWrapperDirect.setup_dispatch_capture()
    except Exception as exc:
        logger.debug(bstack111ll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࡸࡴࠥࡪࡩࡴࡲࡤࡸࡨ࡮ࠠࡤࡣࡳࡸࡺࡸࡥࠡࡨࡲࡶࠥࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥ࠼ࠣࠩࡸࠨ௓"), exc)
    if bstack111l1llll1_opy_:
        browser = self.connect_over_cdp(cdpUrl)
    else:
        browser = bstack1l1l1lll11_opy_(self, cdpUrl)
    try:
        from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
        wrapper = PlaywrightDriverWrapperDirect(browser, page=None, capabilities=bstack1111l1l1l1_opy_, config=CONFIG)
        threading.current_thread().bstackSessionDriver = wrapper
        logger.debug(bstack111ll_opy_ (u"ࠦࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡅࡴ࡬ࡺࡪࡸࡗࡳࡣࡳࡴࡪࡸࡄࡪࡴࡨࡧࡹࠦࡳࡦࡶࡸࡴࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫ࠠࡧࡱࡵࠤࡹ࡮ࡲࡦࡣࡧࠤࠪࡹࠢ௔"), threading.get_ident())
        threading.current_thread().bstackTestErrorMessages = []
        if bstack111l1llll1_opy_:
            threading.current_thread().a11yPlatform = True
            wrapper.bstackA11yShouldScan = True
        if wrapper.session_id and not wrapper._cbt_info_sent:
            PlaywrightDriverWrapperDirect._send_cbt_info_on_session()
        try:
            from playwright.sync_api import Browser as bstack111l1ll1ll_opy_
            if not hasattr(bstack111l1ll1ll_opy_, bstack111ll_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥ࡮ࡦࡹࡢࡴࡦ࡭ࡥࡠࡲࡤࡸࡨ࡮ࡥࡥࠩ௕")):
                _111llll1l_opy_ = bstack111l1ll1ll_opy_.new_page
                def _11111lll_opy_(bstack111ll1l1l1_opy_, *bstack111lll11l_opy_, **bstack1l1lll1111_opy_):
                    if getattr(threading.current_thread(), bstack111ll_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ௖"), None):
                        try:
                            bstack1l1ll11l11_opy_ = bstack111ll1l1l1_opy_.contexts[0] if bstack111ll1l1l1_opy_.contexts else None
                            if bstack1l1ll11l11_opy_ and bstack1l1ll11l11_opy_.pages:
                                page = None
                                for _1ll1l1lll_opy_ in bstack1l1ll11l11_opy_.pages:
                                    if bstack111ll_opy_ (u"ࠢࡢࡤࡲࡹࡹࡀࡢ࡭ࡣࡱ࡯ࠧௗ") in _1ll1l1lll_opy_.url:
                                        page = _1ll1l1lll_opy_
                                        logger.debug(bstack111ll_opy_ (u"ࠣࡃ࠴࠵ࡾࡀࠠࡳࡧࡸࡷ࡮ࡴࡧࠡࡣࡥࡳࡺࡺ࠺ࡣ࡮ࡤࡲࡰࠦࡰࡢࡩࡨࠤ࡫ࡸ࡯࡮ࠢࡧࡩ࡫ࡧࡵ࡭ࡶࠣࡧࡴࡴࡴࡦࡺࡷࠦ௘"))
                                        break
                                if page is None:
                                    page = bstack1l1ll11l11_opy_.new_page(*bstack111lll11l_opy_, **bstack1l1lll1111_opy_)
                                    logger.debug(bstack111ll_opy_ (u"ࠤࡄ࠵࠶ࡿ࠺ࠡࡰࡲࠤࡧࡲࡡ࡯࡭ࠣࡴࡦ࡭ࡥࠡࡨࡲࡹࡳࡪࠬࠡࡥࡵࡩࡦࡺࡥࡥࠢࡱࡩࡼࠦࡰࡢࡩࡨࠤ࡮ࡴࠠࡥࡧࡩࡥࡺࡲࡴࠡࡥࡲࡲࡹ࡫ࡸࡵࠤ௙"))
                            elif bstack1l1ll11l11_opy_:
                                page = bstack1l1ll11l11_opy_.new_page(*bstack111lll11l_opy_, **bstack1l1lll1111_opy_)
                                logger.debug(bstack111ll_opy_ (u"ࠥࡅ࠶࠷ࡹ࠻ࠢࡦࡶࡪࡧࡴࡦࡦࠣࡲࡪࡽࠠࡱࡣࡪࡩࠥ࡯࡮ࠡࡦࡨࡪࡦࡻ࡬ࡵࠢࡦࡳࡳࡺࡥࡹࡶࠥ௚"))
                            else:
                                page = _111llll1l_opy_(bstack111ll1l1l1_opy_, *bstack111lll11l_opy_, **bstack1l1lll1111_opy_)
                                logger.debug(bstack111ll_opy_ (u"ࠦࡆ࠷࠱ࡺ࠼ࠣࡲࡴࠦࡤࡦࡨࡤࡹࡱࡺࠠࡤࡱࡱࡸࡪࡾࡴ࠭ࠢࡩࡥࡱࡲࡩ࡯ࡩࠣࡦࡦࡩ࡫ࠡࡶࡲࠤࡳ࡫ࡷࡠࡲࡤ࡫ࡪ࠮ࠩࠣ௛"))
                        except Exception as bstack1l11111l11_opy_:
                            logger.debug(bstack111ll_opy_ (u"ࠧࡇ࠱࠲ࡻ࠽ࠤࡩ࡫ࡦࡢࡷ࡯ࡸࠥࡩ࡯࡯ࡶࡨࡼࡹࠦࡰࡢࡩࡨࠤࡷ࡫ࡵࡴࡧࠣࡪࡦ࡯࡬ࡦࡦࠣࠬࠪࡹࠩ࠭ࠢࡩࡥࡱࡲࡩ࡯ࡩࠣࡦࡦࡩ࡫ࠣ௜"), bstack1l11111l11_opy_)
                            page = _111llll1l_opy_(bstack111ll1l1l1_opy_, *bstack111lll11l_opy_, **bstack1l1lll1111_opy_)
                    else:
                        page = _111llll1l_opy_(bstack111ll1l1l1_opy_, *bstack111lll11l_opy_, **bstack1l1lll1111_opy_)
                    try:
                        _w = getattr(threading.current_thread(), bstack111ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ௝"), None)
                        if _w and hasattr(_w, bstack111ll_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫࡟ࡱࡣࡪࡩࠬ௞")):
                            _w.update_page(page)
                        if _w and not _w.session_id:
                            try:
                                import json as _json
                                result = page.evaluate(
                                    bstack111ll_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ௟"), bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡪࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡥࡵࡣ࡬ࡰࡸࠨࡽࠨ௠"))
                                if isinstance(result, str):
                                    result = _json.loads(result)
                                if isinstance(result, dict):
                                    sid = result.get(bstack111ll_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭௡")) or result.get(bstack111ll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨ௢")) or result.get(bstack111ll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡏࡤࠨ௣"))
                                    if sid:
                                        import threading as _1lllll1lll_opy_
                                        from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
                                        with PlaywrightDriverWrapperDirect._session_ids_lock:
                                            PlaywrightDriverWrapperDirect._session_ids[_1lllll1lll_opy_.get_ident()] = sid
                                        logger.debug(bstack111ll_opy_ (u"ࠨࡃࡢࡲࡷࡹࡷ࡫ࡤࠡࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠥࡼࡩࡢࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠪࡹࠢ௤"), sid)
                                        PlaywrightDriverWrapperDirect._send_cbt_info_on_session()
                                    else:
                                        logger.debug(bstack111ll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲࠡࡩࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡉ࡫ࡴࡢ࡫࡯ࡷࠥࡸࡥࡵࡷࡵࡲࡪࡪࠠ࡯ࡱࠣࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪ࠺ࠡࠧࡶࠦ௥"), result)
                                else:
                                    logger.debug(bstack111ll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠢࡪࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡥࡵࡣ࡬ࡰࡸࠦࡲࡦࡵࡸࡰࡹࡀࠠࠦࡵࠥ௦"), result)
                            except Exception as _1llll1ll1l_opy_:
                                logger.debug(bstack111ll_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠦࡦࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡸ࡬ࡥࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࠦࡵࠥ௧"), _1llll1ll1l_opy_)
                        if (getattr(threading.current_thread(), bstack111ll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ௨"), None)
                                and not getattr(threading.current_thread(), bstack111ll_opy_ (u"ࠫࡦ࠷࠱ࡺࡡࡶࡸࡦࡸࡴࡦࡦࠪ௩"), False)):
                            threading.current_thread().a11y_started = True
                            try:
                                from bstack_utils import accessibility as _1llll1ll11_opy_
                                bstack111lll11_opy_ = getattr(threading.current_thread(), bstack111ll_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ௪"), True)
                                _1llll1ll11_opy_.start_test_capture(_w, bstack111lll11_opy_)
                            except Exception:
                                logger.debug(bstack111ll_opy_ (u"ࠨࡄࡦࡨࡨࡶࡷ࡫ࡤࠡࡃ࠴࠵ࡾࠦࡳࡵࡣࡵࡸࡤࡺࡥࡴࡶࡢࡧࡦࡶࡴࡶࡴࡨࠤ࡫ࡧࡩ࡭ࡧࡧࠦ௫"))
                    except Exception as exc:
                        logger.debug(bstack111ll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡹࡵࡪࡡࡵࡧࠣࡴࡦ࡭ࡥࠡ࡫ࡱࠤࡼࡸࡡࡱࡲࡨࡶ࠿ࠦࠥࡴࠤ௬"), exc)
                    return page
                bstack111l1ll1ll_opy_.new_page = _11111lll_opy_
                bstack111l1ll1ll_opy_._bstack_new_page_patched = True
        except Exception as exc:
            logger.debug(bstack111ll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡴࡤࡪࠣࡗࡾࡴࡣࡃࡴࡲࡻࡸ࡫ࡲ࠯ࡰࡨࡻࡤࡶࡡࡨࡧࠣࡪࡴࡸࠠࡱࡣࡪࡩࠥࡩࡡࡱࡶࡸࡶࡪࡀࠠࠦࡵࠥ௭"), exc)
        try:
            from playwright.sync_api import Page as bstack11lll111l_opy_, Browser as _1l11llll1l_opy_
            if not hasattr(bstack11lll111l_opy_, bstack111ll_opy_ (u"ࠩࡢࡦࡸࡺࡡࡤ࡭ࡢࡴࡦ࡭ࡥࡠࡥ࡯ࡳࡸ࡫࡟ࡱࡣࡷࡧ࡭࡫ࡤࠨ௮")):
                _1l11l1ll1l_opy_ = bstack11lll111l_opy_.close
                def _1llll11l1_opy_(bstack111l1llll_opy_, *bstack11111l11l1_opy_, _bstack_sdk_close=False, **bstack1111llll_opy_):
                    if not _bstack_sdk_close:
                        logger.debug(bstack111ll_opy_ (u"ࠥࡈࡪ࡬ࡥࡳࡴࡨࡨࠥࡶࡡࡨࡧ࠱ࡧࡱࡵࡳࡦࠪࠬࠤ⠙ࠦࡷࡪ࡮࡯ࠤࡨࡲ࡯ࡴࡧࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢ௯"))
                        threading.current_thread().bstack_deferred_page_close = True
                        threading.current_thread().bstack_deferred_page_ref = bstack111l1llll_opy_
                        return
                    return _1l11l1ll1l_opy_(bstack111l1llll_opy_, *bstack11111l11l1_opy_, **bstack1111llll_opy_)
                bstack11lll111l_opy_.close = _1llll11l1_opy_
                bstack11lll111l_opy_._bstack_page_close_patched = True
            if not hasattr(_1l11llll1l_opy_, bstack111ll_opy_ (u"ࠫࡤࡨࡳࡵࡣࡦ࡯ࡤࡨࡲࡰࡹࡶࡩࡷࡥࡣ࡭ࡱࡶࡩࡤࡶࡡࡵࡥ࡫ࡩࡩ࠭௰")):
                _1lll111ll1_opy_ = _1l11llll1l_opy_.close
                def _1l11llllll_opy_(bstack111ll1l1l1_opy_, *bstack1l1l1lll1l_opy_, _bstack_sdk_close=False, **bstack11ll11ll_opy_):
                    if not _bstack_sdk_close:
                        logger.debug(bstack111ll_opy_ (u"ࠧࡊࡥࡧࡧࡵࡶࡪࡪࠠࡣࡴࡲࡻࡸ࡫ࡲ࠯ࡥ࡯ࡳࡸ࡫ࠨࠪࠢ⠗ࠤࡼ࡯࡬࡭ࠢࡦࡰࡴࡹࡥࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧ௱"))
                        threading.current_thread().bstack_deferred_browser_close = True
                        threading.current_thread().bstack_deferred_browser_ref = bstack111ll1l1l1_opy_
                        return
                    return _1lll111ll1_opy_(bstack111ll1l1l1_opy_, *bstack1l1l1lll1l_opy_, **bstack11ll11ll_opy_)
                _1l11llll1l_opy_.close = _1l11llllll_opy_
                _1l11llll1l_opy_._bstack_browser_close_patched = True
            if not hasattr(bstack11lll111l_opy_, bstack111ll_opy_ (u"࠭࡟ࡣࡵࡷࡥࡨࡱ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡣࡵࡧࡴࡤࡪࡨࡨࠬ௲")):
                _1111111lll_opy_ = bstack11lll111l_opy_.screenshot
                def _11ll1l1111_opy_(bstack111l1llll_opy_, *bstack11ll1l11l1_opy_, **bstack1l111111_opy_):
                    result = _1111111lll_opy_(bstack111l1llll_opy_, *bstack11ll1l11l1_opy_, **bstack1l111111_opy_)
                    try:
                        from bstack_utils.testhub_handler import TestHubHandler
                        from bstack_utils.bstack111l1ll11_opy_ import bstack111ll111_opy_
                        if bstack111ll111_opy_.on():
                            import base64
                            if isinstance(result, bytes):
                                bstack1ll1llll1l_opy_ = base64.b64encode(result).decode(bstack111ll_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭௳"))
                            else:
                                bstack1ll1llll1l_opy_ = str(result)
                            test_uuid = TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack111ll111_opy_.current_hook_uuid()
                            if test_uuid and bstack1ll1llll1l_opy_:
                                TestHubHandler.bstack1lllll11lll_opy_({
                                    bstack111ll_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧ௴"): bstack1ll1llll1l_opy_,
                                    bstack111ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ௵"): test_uuid
                                })
                                logger.debug(bstack111ll_opy_ (u"ࠥࡗࡪࡴࡴࠡࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠢࡷࡳࠥࡕ࠱࠲ࡻࠣࡪࡴࡸࠠࡵࡧࡶࡸࠥࢁࡽࠣ௶").format(test_uuid))
                    except Exception as bstack1111l1ll11_opy_:
                        logger.debug(bstack111ll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡱࡨࠥࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠦࡴࡰࠢࡒ࠵࠶ࡿ࠺ࠡࡽࢀࠦ௷").format(str(bstack1111l1ll11_opy_)))
                    return result
                bstack11lll111l_opy_.screenshot = _11ll1l1111_opy_
                bstack11lll111l_opy_._bstack_screenshot_patched = True
        except Exception as exc:
            logger.debug(bstack111ll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡨࠤࡩ࡫ࡦࡦࡴࡵࡩࡩࠦࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡧࡱࡵࡳࡦࠢ࡫ࡳࡴࡱࡳ࠻ࠢࠨࡷࠧ௸"), exc)
        logger.debug(bstack111ll_opy_ (u"ࠨࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡇࡶ࡮ࡼࡥࡳ࡙ࡵࡥࡵࡶࡥࡳࡆ࡬ࡶࡪࡩࡴࠡࡵࡨࡸࡺࡶࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࠢࡩࡳࡷࠦࡴࡩࡴࡨࡥࡩࠦࡻࡾࠤ௹").format(threading.get_ident()))
    except Exception as e:
        logger.debug(bstack111ll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡷࡳࡣࡳࡴࡪࡸ࠺ࠡࡽࢀࠦ௺").format(str(e)))
    return browser
  async def bstack1llllll11l_opy_(self, *args, **kwargs):
    global bstack1l1l1lll11_opy_, CONFIG, FRAMEWORK_NAME, __version__, BROWSERSTACK_AUTOMATION
    global PLATFORM_INDEX, PARALLELISE_VANILLA_PYTHON, PARALLELISE_THREADING_PYTHON, SESSION_NAME
    import urllib.parse as _11l111111_opy_
    import json
    ws_endpoint = args[0] if args else kwargs.get(bstack111ll_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬ௻"), kwargs.get(bstack111ll_opy_ (u"ࠩࡺࡷࡤ࡫࡮ࡥࡲࡲ࡭ࡳࡺࠧ௼"), bstack111ll_opy_ (u"ࠪࠫ௽")))
    bstack1l1ll1l1l1_opy_ = (ws_endpoint
                 and bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧ௾") in str(ws_endpoint)
                 and bstack111ll_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫ௿") in str(ws_endpoint))
    bstack1lllll1l1l1_opy_ = {}
    if bstack1l1ll1l1l1_opy_:
        from bstack_utils.helper import bstack1l1l1l11_opy_
        bstack1llllll1ll1_opy_ = bstack1l1l1l11_opy_()
        try:
            if bstack1llllll1ll1_opy_:
                CONFIG[bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨఀ")] = str(FRAMEWORK_NAME) + str(__version__)
                bstack1ll11l1lll_opy_ = os.environ.get(bstack111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬఁ"), bstack111ll_opy_ (u"ࠨࠩం"))
                if bstack1ll11l1lll_opy_:
                    CONFIG[bstack111ll_opy_ (u"ࠩࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬః")] = bstack1ll11l1lll_opy_
                CONFIG[bstack111ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬఄ")] = TestHubUtils.bstack11ll11l1ll_opy_(CONFIG, FRAMEWORK_NAME)
                bstack1l1l11111_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
                try:
                    if PARALLELISE_VANILLA_PYTHON is True:
                        bstack1l1l11111_opy_ = int(multiprocessing.current_process().name)
                    elif PARALLELISE_THREADING_PYTHON is True:
                        bstack1l1l11111_opy_ = int(threading.current_thread().name)
                except Exception:
                    bstack1l1l11111_opy_ = 0
                CONFIG[bstack111ll_opy_ (u"ࠦ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥఅ")] = True
                bstack1lllll1l1l1_opy_ = get_caps(CONFIG, bstack1l1l11111_opy_)
                if CONFIG.get(bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩఆ")):
                    update_caps_for_local(bstack1lllll1l1l1_opy_)
                if bstack111ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩఇ") in CONFIG and bstack111ll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬఈ") in CONFIG[bstack111ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫఉ")][bstack1l1l11111_opy_]:
                    SESSION_NAME = CONFIG[bstack111ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬఊ")][bstack1l1l11111_opy_][bstack111ll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨఋ")]
                logger.debug(bstack111ll_opy_ (u"ࠦࡈࡧࡳࡦࠢࡄ࠾ࠥࡘࡥࡱ࡮ࡤࡧࡪࡪࠠࡶࡵࡨࡶࠥࡩࡡࡱࡵࠣࡻ࡮ࡺࡨࠡࡻࡰࡰࠥࡩࡡࡱࡵ࠽ࠤࢀࢃࠢఌ").format(str(bstack1lllll1l1l1_opy_)))
            else:
                bstack11111ll1_opy_ = str(ws_endpoint).split(bstack111ll_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫ఍"))[1]
                bstack1lllll1l1l1_opy_ = json.loads(_11l111111_opy_.unquote(bstack11111ll1_opy_))
                bstack1lllll1l1l1_opy_ = bstack1lllll1l1l1_opy_ or {}
                bstack1ll11l1lll_opy_ = os.environ.get(bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫఎ"), bstack111ll_opy_ (u"ࠧࠨఏ"))
                bstack11ll11l11_opy_ = TestHubUtils.bstack11ll11l1ll_opy_(CONFIG, FRAMEWORK_NAME)
                bstack1lllll1l1l1_opy_[bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩఐ")] = str(FRAMEWORK_NAME) + str(__version__)
                bstack1lllll1l1l1_opy_[bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ఑")] = BROWSERSTACK_AUTOMATION
                if bstack1ll11l1lll_opy_:
                    bstack1lllll1l1l1_opy_[bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬఒ")] = bstack1ll11l1lll_opy_
                bstack1lllll1l1l1_opy_[bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬఓ")] = bstack11ll11l11_opy_
                logger.debug(bstack111ll_opy_ (u"ࠧࡉࡡࡴࡧࠣࡈ࠿ࠦࡍࡦࡴࡪࡩࡩࠦࡓࡅࡍࠣࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࠦࡩ࡯ࡶࡲࠤࡺࡹࡥࡳࠢࡦࡥࡵࡹࠢఔ"))
            ws_url = str(ws_endpoint).split(bstack111ll_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬక"))[0]
            ws_endpoint = ws_url + bstack111ll_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭ఖ") + _11l111111_opy_.quote(json.dumps(bstack1lllll1l1l1_opy_))
            if args:
                args = (ws_endpoint,) + args[1:]
            else:
                if bstack111ll_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬగ") in kwargs:
                    kwargs[bstack111ll_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭ఘ")] = ws_endpoint
                else:
                    kwargs[bstack111ll_opy_ (u"ࠪࡻࡸࡥࡥ࡯ࡦࡳࡳ࡮ࡴࡴࠨఙ")] = ws_endpoint
            logger.debug(bstack111ll_opy_ (u"ࠦࡑ࡫ࡧࡢࡥࡼࠤࡨࡵ࡮࡯ࡧࡦࡸ࡛ࠥࡒࡍࠢࡸࡴࡩࡧࡴࡦࡦࠣࡻ࡮ࡺࡨࠡࡽࢀࠤࡨࡧࡰࡴࠤచ").format(bstack111ll_opy_ (u"ࠧࡿ࡭࡭ࠤఛ") if bstack1llllll1ll1_opy_ else bstack111ll_opy_ (u"ࠨࡴࡦ࡮ࡨࡱࡪࡺࡲࡺࠤజ")))
        except Exception as e:
            logger.debug(bstack111ll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡪࡸࡧࡦࠢࡦࡥࡵࡹࠠࡪࡰࡷࡳࠥࡩ࡯࡯ࡰࡨࡧࡹࠦࡕࡓࡎ࠽ࠤࢀࢃࠢఝ").format(str(e)))
        try:
            from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
            PlaywrightDriverWrapperDirect.setup_dispatch_capture()
        except Exception as exc:
            logger.debug(bstack111ll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࡶࡲࠣࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠥࡩࡡࡱࡶࡸࡶࡪࠦࡩ࡯ࠢࡰࡳࡩࡥࡣࡰࡰࡱࡩࡨࡺ࠺ࠡࠧࡶࠦఞ"), exc)
    browser = await bstack1l1l1lll11_opy_(self, *args, **kwargs)
    if bstack1l1ll1l1l1_opy_:
        try:
            from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
            wrapper = PlaywrightDriverWrapperDirect(browser, page=None, capabilities=bstack1lllll1l1l1_opy_, config=CONFIG)
            threading.current_thread().bstackSessionDriver = wrapper
            logger.debug(bstack111ll_opy_ (u"ࠤࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡊࡲࡪࡸࡨࡶ࡜ࡸࡡࡱࡲࡨࡶࡉ࡯ࡲࡦࡥࡷࠤࡸ࡫ࡴࡶࡲࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࠥ࡬࡯ࡳࠢࡷ࡬ࡷ࡫ࡡࡥࠢࠨࡷࠧట"), threading.get_ident())
            threading.current_thread().bstackTestErrorMessages = []
            if wrapper.session_id and not wrapper._cbt_info_sent:
                PlaywrightDriverWrapperDirect._send_cbt_info_on_session()
            try:
                from playwright.sync_api import Browser as bstack111l1ll1ll_opy_
                if not hasattr(bstack111l1ll1ll_opy_, bstack111ll_opy_ (u"ࠪࡣࡧࡹࡴࡢࡥ࡮ࡣࡳ࡫ࡷࡠࡲࡤ࡫ࡪࡥࡰࡢࡶࡦ࡬ࡪࡪࠧఠ")):
                    _111llll1l_opy_ = bstack111l1ll1ll_opy_.new_page
                    def _11111lll_opy_(bstack111ll1l1l1_opy_, *bstack111lll11l_opy_, **bstack1l1lll1111_opy_):
                        page = _111llll1l_opy_(bstack111ll1l1l1_opy_, *bstack111lll11l_opy_, **bstack1l1lll1111_opy_)
                        try:
                            _w = getattr(threading.current_thread(), bstack111ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪడ"), None)
                            if _w and hasattr(_w, bstack111ll_opy_ (u"ࠬࡻࡰࡥࡣࡷࡩࡤࡶࡡࡨࡧࠪఢ")):
                                _w.update_page(page)
                        except Exception as exc:
                            logger.debug(bstack111ll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡸࡴࡩࡧࡴࡦࠢࡳࡥ࡬࡫ࠠࡪࡰࠣࡻࡷࡧࡰࡱࡧࡵࠤ࠭ࡳ࡯ࡥࡡࡦࡳࡳࡴࡥࡤࡶࠬ࠾ࠥࠫࡳࠣణ"), exc)
                        return page
                    bstack111l1ll1ll_opy_.new_page = _11111lll_opy_
                    bstack111l1ll1ll_opy_._bstack_new_page_patched = True
            except Exception as exc:
                logger.debug(bstack111ll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡺࡣࡩࠢࡖࡽࡳࡩࡂࡳࡱࡺࡷࡪࡸ࠮࡯ࡧࡺࡣࡵࡧࡧࡦࠢ࡬ࡲࠥࡳ࡯ࡥࡡࡦࡳࡳࡴࡥࡤࡶ࠽ࠤࠪࡹࠢత"), exc)
            try:
                from playwright.sync_api import Page as bstack11lll111l_opy_, Browser as _1l11llll1l_opy_
                if not hasattr(bstack11lll111l_opy_, bstack111ll_opy_ (u"ࠨࡡࡥࡷࡹࡧࡣ࡬ࡡࡳࡥ࡬࡫࡟ࡤ࡮ࡲࡷࡪࡥࡰࡢࡶࡦ࡬ࡪࡪࠧథ")):
                    _1l11l1ll1l_opy_ = bstack11lll111l_opy_.close
                    def _1llll11l1_opy_(bstack111l1llll_opy_, *bstack11111l11l1_opy_, _bstack_sdk_close=False, **bstack1111llll_opy_):
                        if not _bstack_sdk_close:
                            logger.debug(bstack111ll_opy_ (u"ࠤࡇࡩ࡫࡫ࡲࡳࡧࡧࠤࡵࡧࡧࡦ࠰ࡦࡰࡴࡹࡥࠩࠫࠣ⠘ࠥࡽࡩ࡭࡮ࠣࡧࡱࡵࡳࡦࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨద"))
                            threading.current_thread().bstack_deferred_page_close = True
                            threading.current_thread().bstack_deferred_page_ref = bstack111l1llll_opy_
                            return
                        return _1l11l1ll1l_opy_(bstack111l1llll_opy_, *bstack11111l11l1_opy_, **bstack1111llll_opy_)
                    bstack11lll111l_opy_.close = _1llll11l1_opy_
                    bstack11lll111l_opy_._bstack_page_close_patched = True
                if not hasattr(_1l11llll1l_opy_, bstack111ll_opy_ (u"ࠪࡣࡧࡹࡴࡢࡥ࡮ࡣࡧࡸ࡯ࡸࡵࡨࡶࡤࡩ࡬ࡰࡵࡨࡣࡵࡧࡴࡤࡪࡨࡨࠬధ")):
                    _1lll111ll1_opy_ = _1l11llll1l_opy_.close
                    def _1l11llllll_opy_(bstack111ll1l1l1_opy_, *bstack1l1l1lll1l_opy_, _bstack_sdk_close=False, **bstack11ll11ll_opy_):
                        if not _bstack_sdk_close:
                            logger.debug(bstack111ll_opy_ (u"ࠦࡉ࡫ࡦࡦࡴࡵࡩࡩࠦࡢࡳࡱࡺࡷࡪࡸ࠮ࡤ࡮ࡲࡷࡪ࠮ࠩࠡ⠖ࠣࡻ࡮ࡲ࡬ࠡࡥ࡯ࡳࡸ࡫ࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦన"))
                            threading.current_thread().bstack_deferred_browser_close = True
                            threading.current_thread().bstack_deferred_browser_ref = bstack111ll1l1l1_opy_
                            return
                        return _1lll111ll1_opy_(bstack111ll1l1l1_opy_, *bstack1l1l1lll1l_opy_, **bstack11ll11ll_opy_)
                    _1l11llll1l_opy_.close = _1l11llllll_opy_
                    _1l11llll1l_opy_._bstack_browser_close_patched = True
                if not hasattr(bstack11lll111l_opy_, bstack111ll_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡢࡴࡦࡺࡣࡩࡧࡧࠫ఩")):
                    _1111111lll_opy_ = bstack11lll111l_opy_.screenshot
                    def _11ll1l1111_opy_(bstack111l1llll_opy_, *bstack11ll1l11l1_opy_, **bstack1l111111_opy_):
                        result = _1111111lll_opy_(bstack111l1llll_opy_, *bstack11ll1l11l1_opy_, **bstack1l111111_opy_)
                        try:
                            from bstack_utils.testhub_handler import TestHubHandler
                            from bstack_utils.bstack111l1ll11_opy_ import bstack111ll111_opy_
                            if bstack111ll111_opy_.on():
                                import base64
                                if isinstance(result, bytes):
                                    bstack1ll1llll1l_opy_ = base64.b64encode(result).decode(bstack111ll_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬప"))
                                else:
                                    bstack1ll1llll1l_opy_ = str(result)
                                test_uuid = TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack111ll111_opy_.current_hook_uuid()
                                if test_uuid and bstack1ll1llll1l_opy_:
                                    TestHubHandler.bstack1lllll11lll_opy_({
                                        bstack111ll_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭ఫ"): bstack1ll1llll1l_opy_,
                                        bstack111ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨబ"): test_uuid
                                    })
                        except Exception as bstack1111l1ll11_opy_:
                            logger.debug(bstack111ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥ࡯ࡦࠣࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠤࡹࡵࠠࡐ࠳࠴ࡽࠥ࠮࡭ࡰࡦࡢࡧࡴࡴ࡮ࡦࡥࡷ࠭࠿ࠦࠥࡴࠤభ"), bstack1111l1ll11_opy_)
                        return result
                    bstack11lll111l_opy_.screenshot = _11ll1l1111_opy_
                    bstack11lll111l_opy_._bstack_screenshot_patched = True
            except Exception as exc:
                logger.debug(bstack111ll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡦࠢࡧࡩ࡫࡫ࡲࡳࡧࡧࠤࡨࡲ࡯ࡴࡧࠣ࡬ࡴࡵ࡫ࡴࠢ࡬ࡲࠥࡳ࡯ࡥࡡࡦࡳࡳࡴࡥࡤࡶ࠽ࠤࠪࡹࠢమ"), exc)
            logger.debug(bstack111ll_opy_ (u"ࠦࡑ࡫ࡧࡢࡥࡼࠤࡨࡵ࡮࡯ࡧࡦࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡴࡳࡣࡦ࡯࡮ࡴࡧࠡࡵࡨࡸࡺࡶࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࠢࡩࡳࡷࠦࡴࡩࡴࡨࡥࡩࠦࡻࡾࠤయ").format(threading.get_ident()))
        except Exception as e:
            logger.debug(bstack111ll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠ࡭ࡧࡪࡥࡨࡿࠠࡤࡱࡱࡲࡪࡩࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡷࡶࡦࡩ࡫ࡪࡰࡪ࠾ࠥࢁࡽࠣర").format(str(e)))
    return browser
except Exception as e:
    pass
def patch_playwright():
    global SELENIUM_OR_PLAYWRIGHT_INSTALLED
    global FRAMEWORK_NAME
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l1l1l11_opy_
        global bstack1l1l1lll11_opy_
        if not bstack1l1l1lll11_opy_:
            bstack1l1l1lll11_opy_ = BrowserType.connect
        BrowserType.connect = bstack1llllll11l_opy_
        if bstack1l1l1l11_opy_():
            BrowserType.launch = bstack1l111l11l1_opy_
            SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
        try:
            from playwright.sync_api._context_manager import PlaywrightContextManager
            if not hasattr(PlaywrightContextManager, bstack111ll_opy_ (u"࠭࡟ࡣࡵࡷࡥࡨࡱ࡟ࡦࡰࡷࡩࡷࡥࡰࡢࡶࡦ࡬ࡪࡪࠧఱ")):
                _1lll1l1ll1_opy_ = PlaywrightContextManager.__enter__
                def _11111l111l_opy_(bstack1ll11lll11_opy_):
                    pw = _1lll1l1ll1_opy_(bstack1ll11lll11_opy_)
                    _11llllll_opy_ = pw.stop
                    _11ll11l11l_opy_ = threading.current_thread()
                    _11ll11l11l_opy_.bstack_deferred_pw_ref = pw
                    _11ll11l11l_opy_.bstack_deferred_pw_stop_fn = _11llllll_opy_
                    def _1l11111111_opy_(*args, _bstack_sdk_close=False, **kwargs):
                        if not _bstack_sdk_close:
                            logger.debug(bstack111ll_opy_ (u"ࠢࡅࡧࡩࡩࡷࡸࡥࡥࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠴ࡳࡵࡱࡳࠬ࠮ࠦ⠔ࠡࡹ࡬ࡰࡱࠦࡳࡵࡱࡳࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣల"))
                            threading.current_thread().bstack_deferred_pw_stop = True
                            return
                        return _11llllll_opy_()
                    pw.stop = _1l11111111_opy_
                    return pw
                PlaywrightContextManager.__enter__ = _11111l111l_opy_
                PlaywrightContextManager._bstack_enter_patched = True
        except Exception as e:
            logger.debug(bstack111ll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡴࡤࡪࠣࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࡃࡰࡰࡷࡩࡽࡺࡍࡢࡰࡤ࡫ࡪࡸ࠮ࡠࡡࡨࡲࡹ࡫ࡲࡠࡡ࠽ࠤࠪࡹࠢళ"), e)
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack11ll1l11l_opy_
      SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
    except Exception as e:
      pass
def playwright_set_session_name(context, bstack1111ll1111_opy_):
  try:
    if getattr(context, bstack111ll_opy_ (u"ࠩࡳࡥ࡬࡫ࠧఴ"), None):
      context.page.evaluate(bstack111ll_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦవ"), bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠨశ")+ json.dumps(bstack1111ll1111_opy_) + bstack111ll_opy_ (u"ࠧࢃࡽࠣష"))
  except Exception as e:
    logger.debug(bstack111ll_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡽࢀ࠾ࠥࢁࡽࠣస").format(str(e), traceback.format_exc()))
def playwright_annotate(context, message, level):
  try:
    if getattr(context, bstack111ll_opy_ (u"ࠧࡱࡣࡪࡩࠬహ"), None):
      context.page.evaluate(bstack111ll_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ఺"), bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ఻") + json.dumps(message) + bstack111ll_opy_ (u"ࠪ࠰ࠧࡲࡥࡷࡧ࡯ࠦ࠿఼࠭") + json.dumps(level) + bstack111ll_opy_ (u"ࠫࢂࢃࠧఽ"))
  except Exception as e:
    logger.debug(bstack111ll_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡣࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠥࢁࡽ࠻ࠢࡾࢁࠧా").format(str(e), traceback.format_exc()))
@measure(event_name=EVENTS.bstack111111111l_opy_, stage=STAGE.bstack1l1l11l1l_opy_, bstack1111l11lll_opy_=SESSION_NAME)
def bstack111ll1l1l_opy_(self, url):
  global bstack1l1ll1lll_opy_
  try:
    bstack1ll1l11l11_opy_(url)
  except Exception as err:
    logger.debug(bstack1l1llllll1_opy_.format(str(err)))
  try:
    bstack1l1ll1lll_opy_(self, url)
  except Exception as e:
    try:
      parsed_error = str(e)
      if any(err_msg in parsed_error for err_msg in bstack11l1llll_opy_):
        bstack1ll1l11l11_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1l1llllll1_opy_.format(str(err)))
    raise e
def bstack1l1lllll11_opy_(self):
  global bstack11l1111lll_opy_
  bstack11l1111lll_opy_ = self
  return
def bstack1ll1ll11l1_opy_(self):
  global bstack1ll1l111ll_opy_
  bstack1ll1l111ll_opy_ = self
  return
def bstack11ll111l1_opy_(test_name, bstack11111lllll_opy_):
  global CONFIG
  if percy.bstack11l1111ll_opy_() == bstack111ll_opy_ (u"ࠨࡴࡳࡷࡨࠦి"):
    bstack11l1l11ll_opy_ = os.path.relpath(bstack11111lllll_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack11l1l11ll_opy_)
    bstack1111l11lll_opy_ = suite_name + bstack111ll_opy_ (u"ࠢ࠮ࠤీ") + test_name
    threading.current_thread().percySessionName = bstack1111l11lll_opy_
def bstack11l1l111l_opy_(self, test, *args, **kwargs):
  global bstack111111lll1_opy_
  test_name = None
  bstack11111lllll_opy_ = None
  if test:
    test_name = str(test.name)
    bstack11111lllll_opy_ = str(test.source)
  bstack11ll111l1_opy_(test_name, bstack11111lllll_opy_)
  bstack111111lll1_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.bstack111llllll1_opy_, stage=STAGE.bstack1l1l11l1l_opy_, bstack1111l11lll_opy_=SESSION_NAME)
def bstack1l1lll111_opy_(driver, bstack1111l11lll_opy_):
  if not bstack1ll111l1l_opy_ and bstack1111l11lll_opy_:
      bstack1l1lll1ll1_opy_ = {
          bstack111ll_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨు"): bstack111ll_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪూ"),
          bstack111ll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ృ"): {
              bstack111ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩౄ"): bstack1111l11lll_opy_
          }
      }
      bstack111ll1llll_opy_ = bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪ౅").format(json.dumps(bstack1l1lll1ll1_opy_))
      driver.execute_script(bstack111ll1llll_opy_)
  if bstack1l11l11ll1_opy_:
      bstack1l1l11l11_opy_ = {
          bstack111ll_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭ె"): bstack111ll_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩే"),
          bstack111ll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫై"): {
              bstack111ll_opy_ (u"ࠩࡧࡥࡹࡧࠧ౉"): bstack1111l11lll_opy_ + bstack111ll_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬొ"),
              bstack111ll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪో"): bstack111ll_opy_ (u"ࠬ࡯࡮ࡧࡱࠪౌ")
          }
      }
      if bstack1l11l11ll1_opy_.status == bstack111ll_opy_ (u"࠭ࡐࡂࡕࡖ్ࠫ"):
          bstack111l11lll1_opy_ = bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬ౎").format(json.dumps(bstack1l1l11l11_opy_))
          driver.execute_script(bstack111l11lll1_opy_)
          bstack11ll1l1l1_opy_(driver, bstack111ll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ౏"))
      elif bstack1l11l11ll1_opy_.status == bstack111ll_opy_ (u"ࠩࡉࡅࡎࡒࠧ౐"):
          reason = bstack111ll_opy_ (u"ࠥࠦ౑")
          bstack1l1ll1ll1l_opy_ = bstack1111l11lll_opy_ + bstack111ll_opy_ (u"ࠫࠥ࡬ࡡࡪ࡮ࡨࡨࠬ౒")
          if bstack1l11l11ll1_opy_.message:
              reason = str(bstack1l11l11ll1_opy_.message)
              bstack1l1ll1ll1l_opy_ = bstack1l1ll1ll1l_opy_ + bstack111ll_opy_ (u"ࠬࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴ࠽ࠤࠬ౓") + reason
          bstack1l1l11l11_opy_[bstack111ll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ౔")] = {
              bstack111ll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱౕ࠭"): bstack111ll_opy_ (u"ࠨࡧࡵࡶࡴࡸౖࠧ"),
              bstack111ll_opy_ (u"ࠩࡧࡥࡹࡧࠧ౗"): bstack1l1ll1ll1l_opy_
          }
          bstack111l11lll1_opy_ = bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨౘ").format(json.dumps(bstack1l1l11l11_opy_))
          driver.execute_script(bstack111l11lll1_opy_)
          bstack11ll1l1l1_opy_(driver, bstack111ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫౙ"), reason)
          bstack111l11111_opy_(reason, str(bstack1l11l11ll1_opy_), str(PLATFORM_INDEX), logger)
@measure(event_name=EVENTS.bstack1lll1llll_opy_, stage=STAGE.bstack1l1l11l1l_opy_, bstack1111l11lll_opy_=SESSION_NAME)
def bstack11lllll1ll_opy_(driver, test):
  if percy.bstack11l1111ll_opy_() == bstack111ll_opy_ (u"ࠧࡺࡲࡶࡧࠥౚ") and percy.bstack111l1lll1_opy_() == bstack111ll_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣ౛"):
      bstack111l11ll1l_opy_ = bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ౜"), None)
      bstack11l111l1l1_opy_(driver, bstack111l11ll1l_opy_, test)
  if (bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬౝ"), None) and
      bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ౞"), None)) or (
      bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ౟"), None) and
      bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ౠ"), None)):
      logger.info(bstack111ll_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠣࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡷࡱࡨࡪࡸࡷࡢࡻ࠱ࠤࠧౡ"))
      a11y.bstack11l1ll11l_opy_(driver, name=test.name, path=test.source)
def bstack1l1l1l11l1_opy_(test, bstack1111l11lll_opy_):
    try:
      bstack1l11111lll_opy_ = datetime.datetime.now()
      data = {}
      if test:
        data[bstack111ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫౢ")] = bstack1111l11lll_opy_
      if bstack1l11l11ll1_opy_:
        if bstack1l11l11ll1_opy_.status == bstack111ll_opy_ (u"ࠧࡑࡃࡖࡗࠬౣ"):
          data[bstack111ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ౤")] = bstack111ll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ౥")
        elif bstack1l11l11ll1_opy_.status == bstack111ll_opy_ (u"ࠪࡊࡆࡏࡌࠨ౦"):
          data[bstack111ll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ౧")] = bstack111ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ౨")
          if bstack1l11l11ll1_opy_.message:
            data[bstack111ll_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭౩")] = str(bstack1l11l11ll1_opy_.message)
      user = CONFIG[bstack111ll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ౪")]
      key = CONFIG[bstack111ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ౫")]
      host = bstack11l1llll1l_opy_(cli.config, [bstack111ll_opy_ (u"ࠤࡤࡴ࡮ࡹࠢ౬"), bstack111ll_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷࡩࠧ౭"), bstack111ll_opy_ (u"ࠦࡦࡶࡩࠣ౮")], bstack111ll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡱ࡫࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࠨ౯"))
      url = bstack111ll_opy_ (u"࠭ࡻࡾ࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡸ࡫ࡳࡴ࡫ࡲࡲࡸ࠵ࡻࡾ࠰࡭ࡷࡴࡴࠧ౰").format(host, bstack1l11l11l1l_opy_)
      headers = {
        bstack111ll_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭౱"): bstack111ll_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ౲"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers, auth=(user, key))
        cli.bstack1ll11111l_opy_(bstack111ll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺ࡶࡲࡧࡥࡹ࡫࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡳࡵࡣࡷࡹࡸࠨ౳"), datetime.datetime.now() - bstack1l11111lll_opy_)
    except Exception as e:
      logger.error(bstack1lll1lllll_opy_.format(str(e)))
def bstack11ll11ll1l_opy_(test, bstack1111l11lll_opy_):
  global CONFIG
  global bstack1ll1l111ll_opy_
  global bstack11l1111lll_opy_
  global bstack1l11l11l1l_opy_
  global bstack1l11l11ll1_opy_
  global SESSION_NAME
  global bstack1l1llll11_opy_
  global bstack111l1l1111_opy_
  global bstack1l111l1ll_opy_
  global bstack11l11ll11l_opy_
  global bstack11l1l1l1l1_opy_
  global bstack111llll11_opy_
  global bstack11l11llll1_opy_
  try:
    if not bstack1l11l11l1l_opy_:
      with bstack11l11llll1_opy_:
        bstack11llll11l_opy_ = os.path.join(os.path.expanduser(bstack111ll_opy_ (u"ࠪࢂࠬ౴")), bstack111ll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ౵"), bstack111ll_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧ౶"))
        if os.path.exists(bstack11llll11l_opy_):
          with open(bstack11llll11l_opy_, bstack111ll_opy_ (u"࠭ࡲࠨ౷")) as f:
            content = f.read().strip()
            if content:
              bstack11l1111l_opy_ = json.loads(bstack111ll_opy_ (u"ࠢࡼࠤ౸") + content + bstack111ll_opy_ (u"ࠨࠤࡻࠦ࠿ࠦࠢࡺࠤࠪ౹") + bstack111ll_opy_ (u"ࠤࢀࠦ౺"))
              bstack1l11l11l1l_opy_ = bstack11l1111l_opy_.get(str(threading.get_ident()))
  except Exception as e:
    logger.debug(bstack111ll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡵࡩࡦࡪࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡎࡊࡳࠡࡨ࡬ࡰࡪࡀࠠࠨ౻") + str(e))
  if not is_robot_playwright_installed():
    if bstack11l1l1l1l1_opy_:
      with bstack1111ll1lll_opy_:
        bstack1111l1111_opy_ = bstack11l1l1l1l1_opy_.copy()
      for driver in bstack1111l1111_opy_:
        if bstack1l11l11l1l_opy_ == driver.session_id:
          if test:
            bstack11lllll1ll_opy_(driver, test)
          bstack1l1lll111_opy_(driver, bstack1111l11lll_opy_)
    elif bstack1l11l11l1l_opy_:
      bstack1l1l1l11l1_opy_(test, bstack1111l11lll_opy_)
    if bstack1ll1l111ll_opy_:
      bstack111l1l1111_opy_(bstack1ll1l111ll_opy_)
    if bstack11l1111lll_opy_:
      bstack1l111l1ll_opy_(bstack11l1111lll_opy_)
    if bstack111llll1_opy_:
      bstack11l11ll11l_opy_()
def bstack1ll1l1l11l_opy_(self, test, *args, **kwargs):
  bstack1111l11lll_opy_ = None
  if test:
    bstack1111l11lll_opy_ = str(test.name)
  bstack11ll11ll1l_opy_(test, bstack1111l11lll_opy_)
  bstack1l1llll11_opy_(self, test, *args, **kwargs)
def bstack1ll11l1l1_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1ll11111l1_opy_
  global CONFIG
  global bstack11l1l1l1l1_opy_
  global bstack1l11l11l1l_opy_
  global bstack11l11llll1_opy_
  bstack1111111ll1_opy_ = None
  try:
    if bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ౼"), None) or bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ౽"), None):
      try:
        if not bstack1l11l11l1l_opy_:
          bstack11llll11l_opy_ = os.path.join(os.path.expanduser(bstack111ll_opy_ (u"࠭ࡾࠨ౾")), bstack111ll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ౿"), bstack111ll_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪಀ"))
          with bstack11l11llll1_opy_:
            if os.path.exists(bstack11llll11l_opy_):
              with open(bstack11llll11l_opy_, bstack111ll_opy_ (u"ࠩࡵࠫಁ")) as f:
                content = f.read().strip()
                if content:
                  bstack11l1111l_opy_ = json.loads(bstack111ll_opy_ (u"ࠥࡿࠧಂ") + content + bstack111ll_opy_ (u"ࠫࠧࡾࠢ࠻ࠢࠥࡽࠧ࠭ಃ") + bstack111ll_opy_ (u"ࠧࢃࠢ಄"))
                  bstack1l11l11l1l_opy_ = bstack11l1111l_opy_.get(str(threading.get_ident()))
      except Exception as e:
        logger.debug(bstack111ll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡸࡥࡢࡦ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡊࡆࡶࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥࡺࡥࡴࡶࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࠬಅ") + str(e))
      if bstack11l1l1l1l1_opy_:
        with bstack1111ll1lll_opy_:
          bstack1111l1111_opy_ = bstack11l1l1l1l1_opy_.copy()
        for driver in bstack1111l1111_opy_:
          if bstack1l11l11l1l_opy_ == driver.session_id:
            bstack1111111ll1_opy_ = driver
    bstack111lll11_opy_ = a11y.is_enabled_testcase(test.tags)
    if bstack1111111ll1_opy_:
      threading.current_thread().isA11yTest = a11y.start_test_capture(bstack1111111ll1_opy_, bstack111lll11_opy_)
      threading.current_thread().isAppA11yTest = a11y.start_test_capture(bstack1111111ll1_opy_, bstack111lll11_opy_)
    else:
      threading.current_thread().isA11yTest = bstack111lll11_opy_
      threading.current_thread().isAppA11yTest = bstack111lll11_opy_
  except:
    pass
  bstack1ll11111l1_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1l11l11ll1_opy_
  try:
    bstack1l11l11ll1_opy_ = self._test
  except:
    bstack1l11l11ll1_opy_ = self.test
def bstack1l111llll_opy_():
  global bstack1l1l1ll1l1_opy_
  try:
    if os.path.exists(bstack1l1l1ll1l1_opy_):
      os.remove(bstack1l1l1ll1l1_opy_)
  except Exception as e:
    logger.debug(bstack111ll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪಆ") + str(e))
def bstack1llll11l11_opy_():
  global bstack1l1l1ll1l1_opy_
  bstack1ll1111111_opy_ = {}
  lock_file = bstack1l1l1ll1l1_opy_ + bstack111ll_opy_ (u"ࠨ࠰࡯ࡳࡨࡱࠧಇ")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack111ll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡬ࡰࡥ࡮ࠤࡳࡵࡴࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨ࠰ࠥࡻࡳࡪࡰࡪࠤࡧࡧࡳࡪࡥࠣࡪ࡮ࡲࡥࠡࡱࡳࡩࡷࡧࡴࡪࡱࡱࡷࠬಈ"))
    try:
      if not os.path.isfile(bstack1l1l1ll1l1_opy_):
        with open(bstack1l1l1ll1l1_opy_, bstack111ll_opy_ (u"ࠪࡻࠬಉ")) as f:
          json.dump({}, f)
      if os.path.exists(bstack1l1l1ll1l1_opy_):
        with open(bstack1l1l1ll1l1_opy_, bstack111ll_opy_ (u"ࠫࡷ࠭ಊ")) as f:
          content = f.read().strip()
          if content:
            bstack1ll1111111_opy_ = json.loads(content)
    except Exception as e:
      logger.debug(bstack111ll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡳࡧࡤࡨ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧಋ") + str(e))
    return bstack1ll1111111_opy_
  try:
    os.makedirs(os.path.dirname(bstack1l1l1ll1l1_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      if not os.path.isfile(bstack1l1l1ll1l1_opy_):
        with open(bstack1l1l1ll1l1_opy_, bstack111ll_opy_ (u"࠭ࡷࠨಌ")) as f:
          json.dump({}, f)
      if os.path.exists(bstack1l1l1ll1l1_opy_):
        with open(bstack1l1l1ll1l1_opy_, bstack111ll_opy_ (u"ࠧࡳࠩ಍")) as f:
          content = f.read().strip()
          if content:
            bstack1ll1111111_opy_ = json.loads(content)
  except Exception as e:
    logger.debug(bstack111ll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡶࡪࡧࡤࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪಎ") + str(e))
  finally:
    return bstack1ll1111111_opy_
def bstack11lll1ll1l_opy_(platform_index, item_index):
  global bstack1l1l1ll1l1_opy_
  lock_file = bstack1l1l1ll1l1_opy_ + bstack111ll_opy_ (u"ࠩ࠱ࡰࡴࡩ࡫ࠨಏ")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack111ll_opy_ (u"ࠪࡪ࡮ࡲࡥ࡭ࡱࡦ࡯ࠥࡴ࡯ࡵࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩ࠱ࠦࡵࡴ࡫ࡱ࡫ࠥࡨࡡࡴ࡫ࡦࠤ࡫࡯࡬ࡦࠢࡲࡴࡪࡸࡡࡵ࡫ࡲࡲࡸ࠭ಐ"))
    try:
      bstack1ll1111111_opy_ = {}
      if os.path.exists(bstack1l1l1ll1l1_opy_):
        with open(bstack1l1l1ll1l1_opy_, bstack111ll_opy_ (u"ࠫࡷ࠭಑")) as f:
          content = f.read().strip()
          if content:
            bstack1ll1111111_opy_ = json.loads(content)
      bstack1ll1111111_opy_[item_index] = platform_index
      with open(bstack1l1l1ll1l1_opy_, bstack111ll_opy_ (u"ࠧࡽࠢಒ")) as outfile:
        json.dump(bstack1ll1111111_opy_, outfile)
    except Exception as e:
      logger.debug(bstack111ll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡹࡵ࡭ࡹ࡯࡮ࡨࠢࡷࡳࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫಓ") + str(e))
    return
  try:
    os.makedirs(os.path.dirname(bstack1l1l1ll1l1_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      bstack1ll1111111_opy_ = {}
      if os.path.exists(bstack1l1l1ll1l1_opy_):
        with open(bstack1l1l1ll1l1_opy_, bstack111ll_opy_ (u"ࠧࡳࠩಔ")) as f:
          content = f.read().strip()
          if content:
            bstack1ll1111111_opy_ = json.loads(content)
      bstack1ll1111111_opy_[item_index] = platform_index
      with open(bstack1l1l1ll1l1_opy_, bstack111ll_opy_ (u"ࠣࡹࠥಕ")) as outfile:
        json.dump(bstack1ll1111111_opy_, outfile)
  except Exception as e:
    logger.debug(bstack111ll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡼࡸࡩࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧಖ") + str(e))
def bstack1ll1llll_opy_(bstack111ll1111l_opy_):
  global CONFIG
  bstack1llllllllll_opy_ = bstack111ll_opy_ (u"ࠪࠫಗ")
  if not bstack111ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧಘ") in CONFIG:
    logger.info(bstack111ll_opy_ (u"ࠬࡔ࡯ࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠤࡵࡧࡳࡴࡧࡧࠤࡺࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡨࡧࡱࡩࡷࡧࡴࡦࠢࡵࡩࡵࡵࡲࡵࠢࡩࡳࡷࠦࡒࡰࡤࡲࡸࠥࡸࡵ࡯ࠩಙ"))
  try:
    platform = CONFIG[bstack111ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩಚ")][bstack111ll1111l_opy_]
    if bstack111ll_opy_ (u"ࠧࡰࡵࠪಛ") in platform:
      bstack1llllllllll_opy_ += str(platform[bstack111ll_opy_ (u"ࠨࡱࡶࠫಜ")]) + bstack111ll_opy_ (u"ࠩ࠯ࠤࠬಝ")
    if bstack111ll_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ಞ") in platform:
      bstack1llllllllll_opy_ += str(platform[bstack111ll_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧಟ")]) + bstack111ll_opy_ (u"ࠬ࠲ࠠࠨಠ")
    if bstack111ll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪಡ") in platform:
      bstack1llllllllll_opy_ += str(platform[bstack111ll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫಢ")]) + bstack111ll_opy_ (u"ࠨ࠮ࠣࠫಣ")
    if bstack111ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫತ") in platform:
      bstack1llllllllll_opy_ += str(platform[bstack111ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬಥ")]) + bstack111ll_opy_ (u"ࠫ࠱ࠦࠧದ")
    if bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪಧ") in platform:
      bstack1llllllllll_opy_ += str(platform[bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫನ")]) + bstack111ll_opy_ (u"ࠧ࠭ࠢࠪ಩")
    if bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩಪ") in platform:
      bstack1llllllllll_opy_ += str(platform[bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪಫ")]) + bstack111ll_opy_ (u"ࠪ࠰ࠥ࠭ಬ")
  except Exception as e:
    logger.debug(bstack111ll_opy_ (u"ࠫࡘࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡴࡧࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡷࡹࡸࡩ࡯ࡩࠣࡪࡴࡸࠠࡳࡧࡳࡳࡷࡺࠠࡨࡧࡱࡩࡷࡧࡴࡪࡱࡱࠫಭ") + str(e))
  finally:
    if bstack1llllllllll_opy_[len(bstack1llllllllll_opy_) - 2:] == bstack111ll_opy_ (u"ࠬ࠲ࠠࠨಮ"):
      bstack1llllllllll_opy_ = bstack1llllllllll_opy_[:-2]
    return bstack1llllllllll_opy_
def bstack111lll1lll_opy_(path, bstack1llllllllll_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack11llll111l_opy_ = ET.parse(path)
    bstack11111llll_opy_ = bstack11llll111l_opy_.getroot()
    bstack11lll11ll_opy_ = None
    for suite in bstack11111llll_opy_.iter(bstack111ll_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬಯ")):
      if bstack111ll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧರ") in suite.attrib:
        suite.attrib[bstack111ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ಱ")] += bstack111ll_opy_ (u"ࠩࠣࠫಲ") + bstack1llllllllll_opy_
        bstack11lll11ll_opy_ = suite
    bstack111l111l_opy_ = None
    for robot in bstack11111llll_opy_.iter(bstack111ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩಳ")):
      bstack111l111l_opy_ = robot
    bstack1ll1ll11l_opy_ = len(bstack111l111l_opy_.findall(bstack111ll_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪ಴")))
    if bstack1ll1ll11l_opy_ == 1:
      bstack111l111l_opy_.remove(bstack111l111l_opy_.findall(bstack111ll_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫವ"))[0])
      bstack111l11l111_opy_ = ET.Element(bstack111ll_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬಶ"), attrib={bstack111ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬಷ"): bstack111ll_opy_ (u"ࠨࡕࡸ࡭ࡹ࡫ࡳࠨಸ"), bstack111ll_opy_ (u"ࠩ࡬ࡨࠬಹ"): bstack111ll_opy_ (u"ࠪࡷ࠵࠭಺")})
      bstack111l111l_opy_.insert(1, bstack111l11l111_opy_)
      bstack11lllll1l_opy_ = None
      for suite in bstack111l111l_opy_.iter(bstack111ll_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪ಻")):
        bstack11lllll1l_opy_ = suite
      bstack11lllll1l_opy_.append(bstack11lll11ll_opy_)
      bstack1l1l111ll1_opy_ = None
      for status in bstack11lll11ll_opy_.iter(bstack111ll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷ಼ࠬ")):
        bstack1l1l111ll1_opy_ = status
      bstack11lllll1l_opy_.append(bstack1l1l111ll1_opy_)
    bstack11llll111l_opy_.write(path)
  except Exception as e:
    logger.debug(bstack111ll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡶࡸ࡯࡮ࡨࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡱ࡫ࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠫಽ") + str(e))
def bstack1llll1lll1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1lll1ll1l1_opy_
  global CONFIG
  if bstack111ll_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡰࡢࡶ࡫ࠦಾ") in options:
    del options[bstack111ll_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡱࡣࡷ࡬ࠧಿ")]
  json_data = bstack1llll11l11_opy_()
  for item_id in json_data.keys():
    path = os.path.join(outs_dir, str(item_id), bstack111ll_opy_ (u"ࠩࡲࡹࡹࡶࡵࡵ࠰ࡻࡱࡱ࠭ೀ"))
    bstack111lll1lll_opy_(path, bstack1ll1llll_opy_(json_data[item_id]))
  bstack1l111llll_opy_()
  return bstack1lll1ll1l1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1l111111l_opy_(self, ff_profile_dir):
  global bstack1lll1l111l_opy_
  if not ff_profile_dir:
    return None
  return bstack1lll1l111l_opy_(self, ff_profile_dir)
def bstack1111l11111_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1lllllll1l_opy_
  bstack1l1ll1lll1_opy_ = []
  if bstack111ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ು") in CONFIG:
    bstack1l1ll1lll1_opy_ = CONFIG[bstack111ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧೂ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack111ll_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࠨೃ")],
      pabot_args[bstack111ll_opy_ (u"ࠨࡶࡦࡴࡥࡳࡸ࡫ࠢೄ")],
      argfile,
      pabot_args.get(bstack111ll_opy_ (u"ࠢࡩ࡫ࡹࡩࠧ೅")),
      pabot_args[bstack111ll_opy_ (u"ࠣࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠦೆ")],
      platform[0],
      bstack1lllllll1l_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack111ll_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡪ࡮ࡲࡥࡴࠤೇ")] or [(bstack111ll_opy_ (u"ࠥࠦೈ"), None)]
    for platform in enumerate(bstack1l1ll1lll1_opy_)
  ]
def bstack1lll1111l_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack11ll1l111l_opy_=bstack111ll_opy_ (u"ࠫࠬ೉")):
  global bstack1l1ll11l_opy_
  self.platform_index = platform_index
  self.bstack1l1l1111l1_opy_ = bstack11ll1l111l_opy_
  bstack1l1ll11l_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1l1l111l_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1ll1l11l_opy_
  global bstack1l1l1llll_opy_
  bstack1ll1l1ll_opy_ = copy.deepcopy(item)
  if not bstack111ll_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧೊ") in item.options:
    bstack1ll1l1ll_opy_.options[bstack111ll_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨೋ")] = []
  bstack1l111l1l11_opy_ = bstack1ll1l1ll_opy_.options[bstack111ll_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩೌ")].copy()
  for v in bstack1ll1l1ll_opy_.options[bstack111ll_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧ್ࠪ")]:
    if bstack111ll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘࠨ೎") in v:
      bstack1l111l1l11_opy_.remove(v)
    if bstack111ll_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡆࡐࡎࡇࡒࡈࡕࠪ೏") in v:
      bstack1l111l1l11_opy_.remove(v)
    if bstack111ll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨ೐") in v:
      bstack1l111l1l11_opy_.remove(v)
  bstack1l111l1l11_opy_.insert(0, bstack111ll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡕࡒࡁࡕࡈࡒࡖࡒࡏࡎࡅࡇ࡛࠾ࢀࢃࠧ೑").format(bstack1ll1l1ll_opy_.platform_index))
  bstack1l111l1l11_opy_.insert(0, bstack111ll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔ࠽ࡿࢂ࠭೒").format(bstack1ll1l1ll_opy_.bstack1l1l1111l1_opy_))
  bstack1ll1l1ll_opy_.options[bstack111ll_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ೓")] = bstack1l111l1l11_opy_
  if bstack1l1l1llll_opy_:
    bstack1ll1l1ll_opy_.options[bstack111ll_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ೔")].insert(0, bstack111ll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡅࡏࡍࡆࡘࡇࡔ࠼ࡾࢁࠬೕ").format(bstack1l1l1llll_opy_))
  return bstack1ll1l11l_opy_(caller_id, datasources, is_last, bstack1ll1l1ll_opy_, outs_dir)
def bstack11ll111111_opy_(command, item_index):
  try:
    if global_config.get_property(bstack111ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫೖ")):
      os.environ[bstack111ll_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬ೗")] = json.dumps(CONFIG[bstack111ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ೘")][item_index % bstack1ll11ll1ll_opy_])
    global bstack1l1l1llll_opy_
    os.environ[bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭೙")] = str(item_index % bstack1ll11ll1ll_opy_)
    listener_arg = bstack111ll_opy_ (u"ࠧࠨ೚")
    if is_robot_playwright_installed() and cli.is_enabled(CONFIG):
      listener_arg = bstack111ll_opy_ (u"ࠨࠢ࠰࠱ࡱ࡯ࡳࡵࡧࡱࡩࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡹࡤ࡬࠰ࡵࡳࡧࡵࡴࡠ࡮࡬ࡷࡹ࡫࡮ࡦࡴࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠮ࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡔࡦࡺࡣࡩࡧࡵࠫ೛")
      logger.debug(bstack111ll_opy_ (u"ࠤࡄࡨࡩ࡯࡮ࡨࠢࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡖࡡࡵࡥ࡫ࡩࡷࠦ࡬ࡪࡵࡷࡩࡳ࡫ࡲࠡࡨࡲࡶࠥ࡯ࡴࡦ࡯ࠣࡿࢂࠨ೜").format(item_index))
    bstack1ll1lllll_opy_ = bstack111ll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡶࡨࡰࠦࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠠ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࠣࠦೝ") + \
              str(item_index % bstack1ll11ll1ll_opy_) + \
              bstack111ll_opy_ (u"ࠦࠥ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠤࠧೞ") + \
              str(item_index) + \
              listener_arg
    if bstack1l1l1llll_opy_:
        bstack1ll1lllll_opy_ += bstack111ll_opy_ (u"ࠧࠦࠢ೟") + bstack1l1l1llll_opy_
    command[0:1] = bstack1ll1lllll_opy_.split()
  except Exception as e:
    logger.error(bstack111ll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡳ࡯ࡥ࡫ࡩࡽ࡮ࡴࡧࠡࡥࡲࡱࡲࡧ࡮ࡥࠢࡩࡳࡷࠦࡰࡢࡤࡲࡸࠥࡸࡵ࡯࠼ࠣࡿࢂ࠭ೠ").format(str(e)))
def bstack1ll1llll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1ll1lll11l_opy_
  try:
    bstack11ll111111_opy_(command, item_index)
    return bstack1ll1lll11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
  except Exception as e:
    logger.error(bstack111ll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡧࡵࡴࠡࡴࡸࡲ࠿ࠦࡻࡾࠩೡ").format(str(e)))
    raise e
def bstack11llll11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1ll1lll11l_opy_
  try:
    bstack11ll111111_opy_(command, item_index)
    return bstack1ll1lll11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
  except Exception as e:
    logger.error(bstack111ll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡦࡨ࡯ࡵࠢࡵࡹࡳࠦ࠲࠯࠳࠶࠾ࠥࢁࡽࠨೢ").format(str(e)))
    try:
      return bstack1ll1lll11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
    except Exception as e2:
      logger.error(bstack111ll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡢࡰࡶࠣ࠶࠳࠷࠳ࠡࡨࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࢀࢃࠧೣ").format(str(e2)))
      raise e
def bstack1lll1ll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1ll1lll11l_opy_
  try:
    bstack11ll111111_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    return bstack1ll1lll11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
  except Exception as e:
    logger.error(bstack111ll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡣࡱࡷࠤࡷࡻ࡮ࠡ࠴࠱࠵࠺ࡀࠠࡼࡿࠪ೤").format(str(e)))
    try:
      return bstack1ll1lll11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
    except Exception as e2:
      logger.error(bstack111ll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡢࡤࡲࡸࠥ࠸࠮࠲࠷ࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࡻࡾࠩ೥").format(str(e2)))
      raise e
def _11lll1llll_opy_(bstack1llll1ll_opy_, item_index, process_timeout, sleep_before_start, bstack1lll11ll11_opy_):
  bstack11ll111111_opy_(bstack1llll1ll_opy_, item_index)
  if process_timeout is None:
    process_timeout = 3600
  if sleep_before_start and sleep_before_start > 0:
    time.sleep(min(sleep_before_start, 5))
  return process_timeout
def bstack11lllll11l_opy_(command, bstack111ll1lll1_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack1ll1lll11l_opy_
  global bstack11l11l1lll_opy_
  global bstack1l1l1llll_opy_
  try:
    for env_name, bstack11ll11llll_opy_ in bstack11l11l1lll_opy_.items():
      os.environ[env_name] = bstack11ll11llll_opy_
    bstack1l1l1llll_opy_ = bstack111ll_opy_ (u"ࠧࠨ೦")
    bstack11ll111111_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    if sleep_before_start and sleep_before_start > 0:
      time.sleep(min(sleep_before_start, 5))
    return bstack1ll1lll11l_opy_(command, bstack111ll1lll1_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack111ll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠࡳࡷࡱࠤ࠺࠴࠰࠻ࠢࡾࢁࠬ೧").format(str(e)))
    try:
      return bstack1ll1lll11l_opy_(command, bstack111ll1lll1_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack111ll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡧࡵࡴࠡࡨࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࢀࢃࠧ೨").format(str(e2)))
      raise e
def bstack1llllll11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack1ll1lll11l_opy_
  try:
    process_timeout = _11lll1llll_opy_(command, item_index, process_timeout, sleep_before_start, bstack111ll_opy_ (u"ࠨ࠶࠱࠶ࠬ೩"))
    return bstack1ll1lll11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack111ll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡢࡰࡶࠣࡶࡺࡴࠠ࠵࠰࠵࠾ࠥࢁࡽࠨ೪").format(str(e)))
    try:
      return bstack1ll1lll11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack111ll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡣࡱࡷࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࡼࡿࠪ೫").format(str(e2)))
      raise e
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack1l11l111ll_opy_(self, runner, quiet=False, capture=True):
  global bstack1l111ll111_opy_
  bstack1ll1l11ll1_opy_ = bstack1l111ll111_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack111ll_opy_ (u"ࠫࡪࡾࡣࡦࡲࡷ࡭ࡴࡴ࡟ࡢࡴࡵࠫ೬")):
      runner.exception_arr = []
    if not hasattr(runner, bstack111ll_opy_ (u"ࠬ࡫ࡸࡤࡡࡷࡶࡦࡩࡥࡣࡣࡦ࡯ࡤࡧࡲࡳࠩ೭")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1ll1l11ll1_opy_
def bstack11111l1ll_opy_(runner, hook_name, context, element, bstack11111l111_opy_, *args):
  global bstack11l11l1ll1_opy_
  try:
    if runner.hooks.get(hook_name):
      bstack11lll1l1l_opy_.bstack11l11l1l11_opy_(hook_name, element)
    if bstack11l11l1ll1_opy_ is None or bstack11l11l1ll1_opy_:
      bstack11111l111_opy_(runner, hook_name, context, *args)
    else:
      bstack111ll1l111_opy_ = (context,) + args
      bstack11111l111_opy_(runner, hook_name, *bstack111ll1l111_opy_)
    if runner.hooks.get(hook_name):
      bstack11lll1l1l_opy_.bstack11ll1ll11l_opy_(element)
      if hook_name not in [bstack111ll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠪ೮"), bstack111ll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪ೯")] and args and hasattr(args[0], bstack111ll_opy_ (u"ࠨࡧࡵࡶࡴࡸ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠨ೰")):
        args[0].error_message = bstack111ll_opy_ (u"ࠩࠪೱ")
  except Exception as e:
    logger.debug(bstack111ll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡨࡢࡰࡧࡰࡪࠦࡨࡰࡱ࡮ࡷࠥ࡯࡮ࠡࡤࡨ࡬ࡦࡼࡥ࠻ࠢࡾࢁࠬೲ").format(str(e)))
@measure(event_name=EVENTS.bstack11l111111l_opy_, stage=STAGE.bstack1l1l11l1l_opy_, hook_type=bstack111ll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡅࡱࡲࠢೳ"), bstack1111l11lll_opy_=SESSION_NAME)
def bstack111ll11l1_opy_(runner, name, context, bstack11111l111_opy_, *args):
    if runner.hooks.get(bstack111ll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤ೴")).__name__ != bstack111ll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࡢࡨࡪ࡬ࡡࡶ࡮ࡷࡣ࡭ࡵ࡯࡬ࠤ೵"):
      bstack11111l1ll_opy_(runner, name, context, runner, bstack11111l111_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack1l111l1ll1_opy_(bstack111ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭೶")) else context.browser
      runner.driver_initialised = bstack111ll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧ೷")
    except Exception as e:
      logger.debug(bstack111ll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡧࡶ࡮ࡼࡥࡳࠢ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡷࡪࠦࡡࡵࡶࡵ࡭ࡧࡻࡴࡦ࠼ࠣࡿࢂ࠭೸").format(str(e)))
def bstack1l11lll1l_opy_(runner, name, context, bstack11111l111_opy_, *args):
    bstack11111l1ll_opy_(runner, name, context, context.feature, bstack11111l111_opy_, *args)
    try:
      if not bstack1ll111l1l_opy_:
        bstack1111111ll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1l111l1ll1_opy_(bstack111ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ೹")) else context.browser
        if is_driver_active(bstack1111111ll1_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack111ll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠧ೺")
          bstack1111ll1111_opy_ = str(runner.feature.name)
          playwright_set_session_name(context, bstack1111ll1111_opy_)
          bstack1111111ll1_opy_.execute_script(bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ೻") + json.dumps(bstack1111ll1111_opy_) + bstack111ll_opy_ (u"࠭ࡽࡾࠩ೼"))
    except Exception as e:
      logger.debug(bstack111ll_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧ೽").format(str(e)))
def bstack1l1ll1llll_opy_(runner, name, context, bstack11111l111_opy_, *args):
    target = context.scenario if hasattr(context, bstack111ll_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪ೾")) else context.feature
    bstack11111l1ll_opy_(runner, name, context, target, bstack11111l111_opy_, *args)
@measure(event_name=EVENTS.bstack11l1lll11l_opy_, stage=STAGE.bstack1l1l11l1l_opy_, bstack1111l11lll_opy_=SESSION_NAME)
def bstack1l111ll1l_opy_(runner, name, context, bstack11111l111_opy_, *args):
    bstack11lll1l1l_opy_.start_test(context)
    bstack11111l1ll_opy_(runner, name, context, context.scenario, bstack11111l111_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack1l1lll11l1_opy_.bstack11l11l1l1_opy_(context, *args)
    try:
      bstack1111111ll1_opy_ = bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ೿"), context.browser)
      if is_driver_active(bstack1111111ll1_opy_):
        TestHubHandler.send_cbt_info(bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩഀ"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack111ll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨഁ")
        if (not bstack1ll111l1l_opy_):
          scenario_name = args[0].name
          feature_name = bstack1111ll1111_opy_ = str(runner.feature.name)
          bstack1111ll1111_opy_ = feature_name + bstack111ll_opy_ (u"ࠬࠦ࠭ࠡࠩം") + scenario_name
          if runner.driver_initialised == bstack111ll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣഃ"):
            playwright_set_session_name(context, bstack1111ll1111_opy_)
            bstack1111111ll1_opy_.execute_script(bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬഄ") + json.dumps(bstack1111ll1111_opy_) + bstack111ll_opy_ (u"ࠨࡿࢀࠫഅ"))
    except Exception as e:
      logger.debug(bstack111ll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡ࡫ࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡀࠠࡼࡿࠪആ").format(str(e)))
@measure(event_name=EVENTS.bstack11l111111l_opy_, stage=STAGE.bstack1l1l11l1l_opy_, hook_type=bstack111ll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡖࡸࡪࡶࠢഇ"), bstack1111l11lll_opy_=SESSION_NAME)
def bstack1llllll1lll_opy_(runner, name, context, bstack11111l111_opy_, *args):
    bstack11111l1ll_opy_(runner, name, context, args[0], bstack11111l111_opy_, *args)
    try:
      bstack1111111ll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1l111l1ll1_opy_(bstack111ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪഈ")) else context.browser
      if is_driver_active(bstack1111111ll1_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack111ll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥഉ")
        bstack11lll1l1l_opy_.bstack1l1111ll_opy_(args[0])
        if runner.driver_initialised == bstack111ll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦഊ") and not bstack1ll111l1l_opy_:
          feature_name = bstack1111ll1111_opy_ = str(runner.feature.name)
          bstack1111ll1111_opy_ = feature_name + bstack111ll_opy_ (u"ࠧࠡ࠯ࠣࠫഋ") + context.scenario.name
          playwright_set_session_name(context, bstack1111ll1111_opy_)
          bstack1111111ll1_opy_.execute_script(bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭ഌ") + json.dumps(bstack1111ll1111_opy_) + bstack111ll_opy_ (u"ࠩࢀࢁࠬ഍"))
    except Exception as e:
      logger.debug(bstack111ll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡴࡦࡲ࠽ࠤࢀࢃࠧഎ").format(str(e)))
@measure(event_name=EVENTS.bstack11l111111l_opy_, stage=STAGE.bstack1l1l11l1l_opy_, hook_type=bstack111ll_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࡖࡸࡪࡶࠢഏ"), bstack1111l11lll_opy_=SESSION_NAME)
def bstack111ll1ll_opy_(runner, name, context, bstack11111l111_opy_, *args):
  bstack11lll1l1l_opy_.bstack1llll11ll_opy_(args[0])
  try:
    step_status = args[0].status.name
    bstack1111111ll1_opy_ = threading.current_thread().bstackSessionDriver if bstack111ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫഐ") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack1111111ll1_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack111ll_opy_ (u"࠭ࡩ࡯ࡵࡷࡩࡵ࠭഑")
        if not bstack1ll111l1l_opy_:
          feature_name = bstack1111ll1111_opy_ = str(runner.feature.name)
          bstack1111ll1111_opy_ = feature_name + bstack111ll_opy_ (u"ࠧࠡ࠯ࠣࠫഒ") + context.scenario.name
          playwright_set_session_name(context, bstack1111ll1111_opy_)
          bstack1111111ll1_opy_.execute_script(bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭ഓ") + json.dumps(bstack1111ll1111_opy_) + bstack111ll_opy_ (u"ࠩࢀࢁࠬഔ"))
    if str(step_status).lower() in [bstack111ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪക"), bstack111ll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪഖ")]:
      bstack1l1111lll_opy_ = bstack111ll_opy_ (u"ࠬ࠭ഗ")
      bstack1ll11111ll_opy_ = bstack111ll_opy_ (u"࠭ࠧഘ")
      bstack11l111lll_opy_ = bstack111ll_opy_ (u"ࠧࠨങ")
      try:
        import traceback
        bstack1l1111lll_opy_ = runner.exception.__class__.__name__
        bstack11l1lll11_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1ll11111ll_opy_ = bstack111ll_opy_ (u"ࠨࠢࠪച").join(bstack11l1lll11_opy_)
        bstack11l111lll_opy_ = bstack11l1lll11_opy_[-1]
      except Exception as e:
        logger.debug(bstack11l11lll_opy_.format(str(e)))
      bstack1l1111lll_opy_ += bstack11l111lll_opy_
      playwright_annotate(context, json.dumps(str(args[0].name) + bstack111ll_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣഛ") + str(bstack1ll11111ll_opy_)),
                          bstack111ll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤജ"))
      if runner.driver_initialised == bstack111ll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤഝ"):
        bstack1lllll111_opy_(getattr(context, bstack111ll_opy_ (u"ࠬࡶࡡࡨࡧࠪഞ"), None), bstack111ll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨട"), bstack1l1111lll_opy_)
        bstack1111111ll1_opy_.execute_script(bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬഠ") + json.dumps(str(args[0].name) + bstack111ll_opy_ (u"ࠣࠢ࠰ࠤࡋࡧࡩ࡭ࡧࡧࠥࡡࡴࠢഡ") + str(bstack1ll11111ll_opy_)) + bstack111ll_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࡽࡾࠩഢ"))
      if runner.driver_initialised == bstack111ll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣണ"):
        bstack11ll1l1l1_opy_(bstack1111111ll1_opy_, bstack111ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫത"), bstack111ll_opy_ (u"࡙ࠧࡣࡦࡰࡤࡶ࡮ࡵࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤഥ") + str(bstack1l1111lll_opy_))
    else:
      playwright_annotate(context, bstack111ll_opy_ (u"ࠨࡐࡢࡵࡶࡩࡩࠧࠢദ"), bstack111ll_opy_ (u"ࠢࡪࡰࡩࡳࠧധ"))
      if runner.driver_initialised == bstack111ll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨന"):
        bstack1lllll111_opy_(getattr(context, bstack111ll_opy_ (u"ࠩࡳࡥ࡬࡫ࠧഩ"), None), bstack111ll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥപ"))
      bstack1111111ll1_opy_.execute_script(bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩഫ") + json.dumps(str(args[0].name) + bstack111ll_opy_ (u"ࠧࠦ࠭ࠡࡒࡤࡷࡸ࡫ࡤࠢࠤബ")) + bstack111ll_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤࢀࢁࠬഭ"))
      if runner.driver_initialised == bstack111ll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧമ"):
        bstack11ll1l1l1_opy_(bstack1111111ll1_opy_, bstack111ll_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣയ"))
  except Exception as e:
    logger.debug(bstack111ll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡳࡵࡧࡳ࠾ࠥࢁࡽࠨര").format(str(e)))
  bstack11111l1ll_opy_(runner, name, context, args[0], bstack11111l111_opy_, *args)
@measure(event_name=EVENTS.bstack1lllll11ll_opy_, stage=STAGE.bstack1l1l11l1l_opy_, bstack1111l11lll_opy_=SESSION_NAME)
def bstack11llll11l1_opy_(runner, name, context, bstack11111l111_opy_, *args):
  bstack11lll1l1l_opy_.end_test(args[0])
  try:
    bstack1111l1l11_opy_ = args[0].status.name
    bstack1111111ll1_opy_ = bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩറ"), context.browser)
    bstack1l1lll11l1_opy_.bstack11111lll1l_opy_(bstack1111111ll1_opy_)
    if str(bstack1111l1l11_opy_).lower() in [bstack111ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫല"), bstack111ll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫള")]:
      bstack1l1111lll_opy_ = bstack111ll_opy_ (u"࠭ࠧഴ")
      bstack1ll11111ll_opy_ = bstack111ll_opy_ (u"ࠧࠨവ")
      bstack11l111lll_opy_ = bstack111ll_opy_ (u"ࠨࠩശ")
      try:
        import traceback
        bstack1l1111lll_opy_ = runner.exception.__class__.__name__
        bstack11l1lll11_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1ll11111ll_opy_ = bstack111ll_opy_ (u"ࠩࠣࠫഷ").join(bstack11l1lll11_opy_)
        bstack11l111lll_opy_ = bstack11l1lll11_opy_[-1]
      except Exception as e:
        logger.debug(bstack11l11lll_opy_.format(str(e)))
      bstack1l1111lll_opy_ += bstack11l111lll_opy_
      playwright_annotate(context, json.dumps(str(args[0].name) + bstack111ll_opy_ (u"ࠥࠤ࠲ࠦࡆࡢ࡫࡯ࡩࡩࠧ࡜࡯ࠤസ") + str(bstack1ll11111ll_opy_)),
                          bstack111ll_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥഹ"))
      if runner.driver_initialised == bstack111ll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢഺ") or runner.driver_initialised == bstack111ll_opy_ (u"࠭ࡩ࡯ࡵࡷࡩࡵ഻࠭"):
        bstack1lllll111_opy_(getattr(context, bstack111ll_opy_ (u"ࠧࡱࡣࡪࡩ഼ࠬ"), None), bstack111ll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣഽ"), bstack1l1111lll_opy_)
        bstack1111111ll1_opy_.execute_script(bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧാ") + json.dumps(str(args[0].name) + bstack111ll_opy_ (u"ࠥࠤ࠲ࠦࡆࡢ࡫࡯ࡩࡩࠧ࡜࡯ࠤി") + str(bstack1ll11111ll_opy_)) + bstack111ll_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣࡿࢀࠫീ"))
      if runner.driver_initialised == bstack111ll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢു") or runner.driver_initialised == bstack111ll_opy_ (u"࠭ࡩ࡯ࡵࡷࡩࡵ࠭ൂ"):
        bstack11ll1l1l1_opy_(bstack1111111ll1_opy_, bstack111ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧൃ"), bstack111ll_opy_ (u"ࠣࡕࡦࡩࡳࡧࡲࡪࡱࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧൄ") + str(bstack1l1111lll_opy_))
    else:
      playwright_annotate(context, bstack111ll_opy_ (u"ࠤࡓࡥࡸࡹࡥࡥࠣࠥ൅"), bstack111ll_opy_ (u"ࠥ࡭ࡳ࡬࡯ࠣെ"))
      if runner.driver_initialised == bstack111ll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨേ") or runner.driver_initialised == bstack111ll_opy_ (u"ࠬ࡯࡮ࡴࡶࡨࡴࠬൈ"):
        bstack1lllll111_opy_(getattr(context, bstack111ll_opy_ (u"࠭ࡰࡢࡩࡨࠫ൉"), None), bstack111ll_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢൊ"))
      bstack1111111ll1_opy_.execute_script(bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ോ") + json.dumps(str(args[0].name) + bstack111ll_opy_ (u"ࠤࠣ࠱ࠥࡖࡡࡴࡵࡨࡨࠦࠨൌ")) + bstack111ll_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾ്ࠩ"))
      if runner.driver_initialised == bstack111ll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨൎ") or runner.driver_initialised == bstack111ll_opy_ (u"ࠬ࡯࡮ࡴࡶࡨࡴࠬ൏"):
        bstack11ll1l1l1_opy_(bstack1111111ll1_opy_, bstack111ll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ൐"))
  except Exception as e:
    logger.debug(bstack111ll_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩ൑").format(str(e)))
  bstack11111l1ll_opy_(runner, name, context, context.scenario, bstack11111l111_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack1l111lll1l_opy_(runner, name, context, bstack11111l111_opy_, *args):
    target = context.scenario if hasattr(context, bstack111ll_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪ൒")) else context.feature
    bstack11111l1ll_opy_(runner, name, context, target, bstack11111l111_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack1111l1l1ll_opy_(runner, name, context, bstack11111l111_opy_, *args):
    try:
      bstack1111111ll1_opy_ = bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ൓"), context.browser)
      bstack1l11llll1_opy_ = bstack111ll_opy_ (u"ࠪࠫൔ")
      if context.failed is True:
        bstack1l111l1l1_opy_ = []
        bstack1l1l1l1111_opy_ = []
        bstack1111ll111l_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack1l111l1l1_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack11l1lll11_opy_ = traceback.format_tb(exc_tb)
            bstack1l11l1ll11_opy_ = bstack111ll_opy_ (u"ࠫࠥ࠭ൕ").join(bstack11l1lll11_opy_)
            bstack1l1l1l1111_opy_.append(bstack1l11l1ll11_opy_)
            bstack1111ll111l_opy_.append(bstack11l1lll11_opy_[-1])
        except Exception as e:
          logger.debug(bstack11l11lll_opy_.format(str(e)))
        bstack1l1111lll_opy_ = bstack111ll_opy_ (u"ࠬ࠭ൖ")
        for i in range(len(bstack1l111l1l1_opy_)):
          bstack1l1111lll_opy_ += bstack1l111l1l1_opy_[i] + bstack1111ll111l_opy_[i] + bstack111ll_opy_ (u"࠭࡜࡯ࠩൗ")
        bstack1l11llll1_opy_ = bstack111ll_opy_ (u"ࠧࠡࠩ൘").join(bstack1l1l1l1111_opy_)
        if runner.driver_initialised in [bstack111ll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠤ൙"), bstack111ll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨ൚")]:
          playwright_annotate(context, bstack1l11llll1_opy_, bstack111ll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤ൛"))
          bstack1lllll111_opy_(getattr(context, bstack111ll_opy_ (u"ࠫࡵࡧࡧࡦࠩ൜"), None), bstack111ll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ൝"), bstack1l1111lll_opy_)
          bstack1111111ll1_opy_.execute_script(bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ൞") + json.dumps(bstack1l11llll1_opy_) + bstack111ll_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦࢂࢃࠧൟ"))
          bstack11ll1l1l1_opy_(bstack1111111ll1_opy_, bstack111ll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣൠ"), bstack111ll_opy_ (u"ࠤࡖࡳࡲ࡫ࠠࡴࡥࡨࡲࡦࡸࡩࡰࡵࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࡡࡴࠢൡ") + str(bstack1l1111lll_opy_))
          bstack1111ll11_opy_ = bstack1111111ll_opy_(bstack1l11llll1_opy_, runner.feature.name, logger)
          if (bstack1111ll11_opy_ != None):
            bstack11l1llllll_opy_.append(bstack1111ll11_opy_)
      else:
        if runner.driver_initialised in [bstack111ll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦൢ"), bstack111ll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣൣ")]:
          playwright_annotate(context, bstack111ll_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࡀࠠࠣ൤") + str(runner.feature.name) + bstack111ll_opy_ (u"ࠨࠠࡱࡣࡶࡷࡪࡪࠡࠣ൥"), bstack111ll_opy_ (u"ࠢࡪࡰࡩࡳࠧ൦"))
          bstack1lllll111_opy_(getattr(context, bstack111ll_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭൧"), None), bstack111ll_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ൨"))
          bstack1111111ll1_opy_.execute_script(bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨ൩") + json.dumps(bstack111ll_opy_ (u"ࠦࡋ࡫ࡡࡵࡷࡵࡩ࠿ࠦࠢ൪") + str(runner.feature.name) + bstack111ll_opy_ (u"ࠧࠦࡰࡢࡵࡶࡩࡩࠧࠢ൫")) + bstack111ll_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤࢀࢁࠬ൬"))
          bstack11ll1l1l1_opy_(bstack1111111ll1_opy_, bstack111ll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ൭"))
          bstack1111ll11_opy_ = bstack1111111ll_opy_(bstack1l11llll1_opy_, runner.feature.name, logger)
          if (bstack1111ll11_opy_ != None):
            bstack11l1llllll_opy_.append(bstack1111ll11_opy_)
    except Exception as e:
      logger.debug(bstack111ll_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࠥ࡬ࡥࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪ൮").format(str(e)))
    bstack11111l1ll_opy_(runner, name, context, context.feature, bstack11111l111_opy_, *args)
@measure(event_name=EVENTS.bstack11l111111l_opy_, stage=STAGE.bstack1l1l11l1l_opy_, hook_type=bstack111ll_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࡂ࡮࡯ࠦ൯"), bstack1111l11lll_opy_=SESSION_NAME)
def bstack1l11l1111_opy_(runner, name, context, bstack11111l111_opy_, *args):
    bstack11111l1ll_opy_(runner, name, context, runner, bstack11111l111_opy_, *args)
def bstack1lll1l11l1_opy_(self, filename=None):
  global bstack1l11ll1l_opy_
  bstack1l11ll1l_opy_(self, filename)
  bstack11l111lll1_opy_ = []
  bstack1ll1111l1l_opy_ = [bstack111ll_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠫ൰"), bstack111ll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡹࡧࡧࠨ൱"), bstack111ll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧ൲"), bstack111ll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧ൳"), bstack111ll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡴࡢࡩࠪ൴"), bstack111ll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨ൵")]
  bstack1lllll11l1l_opy_ = lambda *_: None
  for hook_name in bstack1ll1111l1l_opy_:
    if hook_name not in self.hooks:
      self.hooks[hook_name] = bstack1lllll11l1l_opy_
      bstack11l111lll1_opy_.append(hook_name)
  if bstack11l111lll1_opy_:
    os.environ[bstack111ll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡖࡈࡐࡥࡄࡆࡈࡄ࡙ࡑ࡚࡟ࡉࡑࡒࡏࡘ࠭൶")] = bstack111ll_opy_ (u"ࠪ࠰ࠬ൷").join(bstack11l111lll1_opy_)
def _execute_deferred_playwright_close():
  try:
    _11ll11l11l_opy_ = threading.current_thread()
    _11ll1lll1_opy_ = getattr(_11ll11l11l_opy_, bstack111ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡩ࡫ࡦࡦࡴࡵࡩࡩࡥࡰࡢࡩࡨࡣࡷ࡫ࡦࠨ൸"), None)
    _1111lll111_opy_ = getattr(_11ll11l11l_opy_, bstack111ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡪࡥࡧࡧࡵࡶࡪࡪ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡠࡴࡨࡪࠬ൹"), None)
    _1ll11ll1l1_opy_ = getattr(_11ll11l11l_opy_, bstack111ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡤࡦࡨࡨࡶࡷ࡫ࡤࡠࡲࡺࡣࡸࡺ࡯ࡱࡡࡩࡲࠬൺ"), None)
    _wrapper = getattr(_11ll11l11l_opy_, bstack111ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ൻ"), None)
    if not _1111lll111_opy_ and _wrapper and hasattr(_wrapper, bstack111ll_opy_ (u"ࠨࡡࡥࡶࡴࡽࡳࡦࡴࠪർ")):
      _1111lll111_opy_ = _wrapper._browser
    if not _11ll1lll1_opy_ and _wrapper and hasattr(_wrapper, bstack111ll_opy_ (u"ࠩࡢࡴࡦ࡭ࡥࠨൽ")):
      _11ll1lll1_opy_ = _wrapper._page
    if not _1ll11ll1l1_opy_:
      _1lllllll11l_opy_ = getattr(_11ll11l11l_opy_, bstack111ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡨࡪ࡬ࡥࡳࡴࡨࡨࡤࡶࡷࡠࡴࡨࡪࠬൾ"), None)
      if _1lllllll11l_opy_ and hasattr(_1lllllll11l_opy_, bstack111ll_opy_ (u"ࠫࡸࡺ࡯ࡱࠩൿ")):
        _1ll11ll1l1_opy_ = _1lllllll11l_opy_.stop
    _1l1lll11l_opy_ = _11ll1lll1_opy_ or _1111lll111_opy_ or _1ll11ll1l1_opy_
    if not _1l1lll11l_opy_:
      return
    if _11ll1lll1_opy_ and hasattr(_11ll1lll1_opy_, bstack111ll_opy_ (u"ࠬࡩ࡬ࡰࡵࡨࠫ඀")):
      try:
        _11ll1lll1_opy_.close(_bstack_sdk_close=True)
      except TypeError:
        try:
          _11ll1lll1_opy_.close()
        except Exception:
          pass
      except Exception as e:
        logger.debug(bstack111ll_opy_ (u"࠭ࡄࡦࡨࡨࡶࡷ࡫ࡤࠡࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡶࡡࡨࡧ࠱ࡧࡱࡵࡳࡦࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡿࢂ࠭ඁ").format(str(e)))
    if _1111lll111_opy_ and hasattr(_1111lll111_opy_, bstack111ll_opy_ (u"ࠧࡤ࡮ࡲࡷࡪ࠭ං")):
      try:
        _1111lll111_opy_.close(_bstack_sdk_close=True)
      except TypeError:
        try:
          _1111lll111_opy_.close()
        except Exception:
          pass
      except Exception as e:
        logger.debug(bstack111ll_opy_ (u"ࠨࡆࡨࡪࡪࡸࡲࡦࡦࠣࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡣࡴࡲࡻࡸ࡫ࡲ࠯ࡥ࡯ࡳࡸ࡫ࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡽࢀࠫඃ").format(str(e)))
    if _1ll11ll1l1_opy_:
      try:
        _1ll11ll1l1_opy_(_bstack_sdk_close=True)
      except TypeError:
        try:
          _1ll11ll1l1_opy_()
        except Exception:
          pass
      except Exception as e:
        logger.debug(bstack111ll_opy_ (u"ࠩࡇࡩ࡫࡫ࡲࡳࡧࡧࠤࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡷࡳࡵࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࡼࡿࠪ඄").format(str(e)))
    for attr in (bstack111ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡨࡪ࡬ࡥࡳࡴࡨࡨࡤࡶࡡࡨࡧࡢࡧࡱࡵࡳࡦࠩඅ"), bstack111ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡩ࡫ࡦࡦࡴࡵࡩࡩࡥࡰࡢࡩࡨࡣࡷ࡫ࡦࠨආ"),
                 bstack111ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡪࡥࡧࡧࡵࡶࡪࡪ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡠࡥ࡯ࡳࡸ࡫ࠧඇ"), bstack111ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡤࡦࡨࡨࡶࡷ࡫ࡤࡠࡤࡵࡳࡼࡹࡥࡳࡡࡵࡩ࡫࠭ඈ"),
                 bstack111ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡥࡧࡩࡩࡷࡸࡥࡥࡡࡳࡻࡤࡹࡴࡰࡲࠪඉ"), bstack111ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡦࡨࡪࡪࡸࡲࡦࡦࡢࡴࡼࡥࡳࡵࡱࡳࡣ࡫ࡴࠧඊ"),
                 bstack111ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡧࡩ࡫࡫ࡲࡳࡧࡧࡣࡵࡽ࡟ࡳࡧࡩࠫඋ")):
      try:
        delattr(_11ll11l11l_opy_, attr)
      except AttributeError:
        pass
    if _wrapper:
      try:
        _wrapper._page = None
        _wrapper._browser = None
      except Exception:
        pass
    logger.debug(bstack111ll_opy_ (u"ࠪࡈࡪ࡬ࡥࡳࡴࡨࡨࠥࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡦࡰࡴࡹࡥࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠤ࡫ࡵࡲࠡࡶ࡫ࡶࡪࡧࡤࠡࡽࢀࠫඌ").format(_11ll11l11l_opy_.ident))
  except Exception as e:
    logger.debug(bstack111ll_opy_ (u"ࠫࡉ࡫ࡦࡦࡴࡵࡩࡩࠦࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡧࡱࡵࡳࡦࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡿࢂ࠭ඍ").format(str(e)))
def bstack1l1lll111l_opy_(self, name, *args):
  global bstack11111l111_opy_
  global bstack11l11l1ll1_opy_
  try:
    if BROWSERSTACK_AUTOMATION:
      platform_index = int(threading.current_thread()._name) % bstack1ll11ll1ll_opy_
      bstack1l1l1l11l_opy_ = CONFIG[bstack111ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨඎ")][platform_index]
      os.environ[bstack111ll_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧඏ")] = json.dumps(bstack1l1l1l11l_opy_)
    if not hasattr(self, bstack111ll_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡨࡨࠬඐ")):
      self.driver_initialised = None
    bstack1l1l111l11_opy_ = {
        bstack111ll_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠬඑ"): bstack111ll11l1_opy_,
        bstack111ll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠪඒ"): bstack1l11lll1l_opy_,
        bstack111ll_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡸࡦ࡭ࠧඓ"): bstack1l1ll1llll_opy_,
        bstack111ll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ඔ"): bstack1l111ll1l_opy_,
        bstack111ll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠪඕ"): bstack1llllll1lll_opy_,
        bstack111ll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡴࡦࡲࠪඖ"): bstack111ll1ll_opy_,
        bstack111ll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨ඗"): bstack11llll11l1_opy_,
        bstack111ll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡵࡣࡪࠫ඘"): bstack1l111lll1l_opy_,
        bstack111ll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠩ඙"): bstack1111l1l1ll_opy_,
        bstack111ll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ࠭ක"): bstack1l11l1111_opy_
    }
    handler = bstack1l1l111l11_opy_.get(name, bstack11111l111_opy_)
    try:
      if args:
        context = args[0]
        remaining_args = args[1:]
        if bstack11l11l1ll1_opy_ is None or not bstack11l11l1ll1_opy_:
          context = self.context
          remaining_args = args
      else:
        context = self.context
        remaining_args = ()
      handler(self, name, context, bstack11111l111_opy_, *remaining_args)
    except Exception as e:
      logger.debug(bstack111ll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡢࡦࡪࡤࡺࡪࠦࡨࡰࡱ࡮ࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶࠥࢁࡽ࠻ࠢࡾࢁࠬඛ").format(name, str(e)))
    if name == bstack111ll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ග"):
      _execute_deferred_playwright_close()
    if name in [bstack111ll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ඝ"), bstack111ll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨඞ"), bstack111ll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠫඟ")]:
      try:
        bstack1111111ll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1l111l1ll1_opy_(bstack111ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨච")) else context.browser
        bstack1l1lll1l1l_opy_ = (
          (name == bstack111ll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ࠭ඡ") and self.driver_initialised == bstack111ll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣජ")) or
          (name == bstack111ll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬඣ") and self.driver_initialised == bstack111ll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠢඤ")) or
          (name == bstack111ll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨඥ") and self.driver_initialised in [bstack111ll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥඦ"), bstack111ll_opy_ (u"ࠤ࡬ࡲࡸࡺࡥࡱࠤට")]) or
          (name == bstack111ll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡸࡪࡶࠧඨ") and self.driver_initialised == bstack111ll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤඩ"))
        )
        if bstack1l1lll1l1l_opy_:
          self.driver_initialised = None
          if bstack1111111ll1_opy_ and hasattr(bstack1111111ll1_opy_, bstack111ll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠩඪ")):
            try:
              bstack1111111ll1_opy_.quit()
            except Exception as e:
              logger.debug(bstack111ll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡷࡵࡪࡶࡷ࡭ࡳ࡭ࠠࡥࡴ࡬ࡺࡪࡸࠠࡪࡰࠣࡦࡪ࡮ࡡࡷࡧࠣ࡬ࡴࡵ࡫࠻ࠢࡾࢁࠬණ").format(str(e)))
      except Exception as e:
        logger.debug(bstack111ll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࠡࡪࡲࡳࡰࠦࡣ࡭ࡧࡤࡲࡺࡶࠠࡧࡱࡵࠤࢀࢃ࠺ࠡࡽࢀࠫඬ").format(name, str(e)))
  except Exception as e:
    logger.debug(bstack111ll_opy_ (u"ࠨࡅࡵ࡭ࡹ࡯ࡣࡢ࡮ࠣࡩࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡨࡥࡩࡣࡹࡩࠥࡸࡵ࡯ࠢ࡫ࡳࡴࡱࠠࡼࡿ࠽ࠤࢀࢃࠧත").format(name, str(e)))
    try:
      if bstack11l11l1ll1_opy_ is None or bstack11l11l1ll1_opy_:
        try:
          bstack11111l111_opy_(self, name, self.context, *args)
        except TypeError:
          bstack11111l111_opy_(self, name, *args)
      else:
        bstack11111l111_opy_(self, name, *args)
    except Exception as e2:
      logger.debug(bstack111ll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࠦ࡯ࡳ࡫ࡪ࡭ࡳࡧ࡬ࠡࡤࡨ࡬ࡦࡼࡥࠡࡪࡲࡳࡰࠦࡻࡾ࠼ࠣࡿࢂ࠭ථ").format(name, str(e2)))
  finally:
    if name == bstack111ll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫද"):
      _execute_deferred_playwright_close()
def bstack1ll1ll1ll1_opy_(config, startdir):
  return bstack111ll_opy_ (u"ࠦࡩࡸࡩࡷࡧࡵ࠾ࠥࢁ࠰ࡾࠤධ").format(bstack111ll_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦන"))
notset = Notset()
def bstack111l1l1l11_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1l1lll11ll_opy_
  if str(name).lower() == bstack111ll_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷ࠭඲"):
    return bstack111ll_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨඳ")
  else:
    return bstack1l1lll11ll_opy_(self, name, default, skip)
def bstack11l11l1111_opy_(item, when):
  global bstack11ll111lll_opy_
  try:
    bstack11ll111lll_opy_(item, when)
  except Exception as e:
    pass
def bstack111ll1l1_opy_():
  return
def bstack111ll111l_opy_(type, name, status, reason, bstack111l1l11ll_opy_, bstack1111111l1_opy_):
  bstack1l1lll1ll1_opy_ = {
    bstack111ll_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨප"): type,
    bstack111ll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬඵ"): {}
  }
  if type == bstack111ll_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬබ"):
    bstack1l1lll1ll1_opy_[bstack111ll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧභ")][bstack111ll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫම")] = bstack111l1l11ll_opy_
    bstack1l1lll1ll1_opy_[bstack111ll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩඹ")][bstack111ll_opy_ (u"ࠧࡥࡣࡷࡥࠬය")] = json.dumps(str(bstack1111111l1_opy_))
  if type == bstack111ll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩර"):
    bstack1l1lll1ll1_opy_[bstack111ll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ඼")][bstack111ll_opy_ (u"ࠪࡲࡦࡳࡥࠨල")] = name
  if type == bstack111ll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧ඾"):
    bstack1l1lll1ll1_opy_[bstack111ll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ඿")][bstack111ll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ව")] = status
    if status == bstack111ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧශ"):
      bstack1l1lll1ll1_opy_[bstack111ll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫෂ")][bstack111ll_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩස")] = json.dumps(str(reason))
  bstack111ll1llll_opy_ = bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨහ").format(json.dumps(bstack1l1lll1ll1_opy_))
  return bstack111ll1llll_opy_
def bstack11l1l11l1_opy_(driver_command, response):
    if driver_command == bstack111ll_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨළ"):
        TestHubHandler.bstack1lllll11lll_opy_({
            bstack111ll_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫෆ"): response[bstack111ll_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬ෇")],
            bstack111ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ෈"): TestHubHandler.current_test_uuid()
        })
def bstack11lll1l111_opy_(item, call, rep):
  global bstack1l1l1ll11l_opy_
  global bstack11l1l1l1l1_opy_
  global bstack1ll111l1l_opy_
  name = bstack111ll_opy_ (u"ࠨࠩ෉")
  try:
    if rep.when == bstack111ll_opy_ (u"ࠩࡦࡥࡱࡲ්ࠧ"):
      bstack1l11l11l1l_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1ll111l1l_opy_:
          name = str(rep.nodeid)
          bstack1l11l1l111_opy_ = bstack111ll111l_opy_(bstack111ll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ෋"), name, bstack111ll_opy_ (u"ࠫࠬ෌"), bstack111ll_opy_ (u"ࠬ࠭෍"), bstack111ll_opy_ (u"࠭ࠧ෎"), bstack111ll_opy_ (u"ࠧࠨා"))
          threading.current_thread().bstack111l11l11l_opy_ = name
          for driver in bstack11l1l1l1l1_opy_:
            if bstack1l11l11l1l_opy_ == driver.session_id:
              driver.execute_script(bstack1l11l1l111_opy_)
      except Exception as e:
        logger.debug(bstack111ll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨැ").format(str(e)))
      try:
        bstack11l11ll1l_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack111ll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪෑ"):
          status = bstack111ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪි") if rep.outcome.lower() == bstack111ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫී") else bstack111ll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬු")
          reason = bstack111ll_opy_ (u"࠭ࠧ෕")
          if status == bstack111ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧූ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack111ll_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭෗") if status == bstack111ll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩෘ") else bstack111ll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩෙ")
          data = name + bstack111ll_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭ේ") if status == bstack111ll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬෛ") else name + bstack111ll_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠡࠡࠩො") + reason
          bstack111ll1111_opy_ = bstack111ll111l_opy_(bstack111ll_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩෝ"), bstack111ll_opy_ (u"ࠨࠩෞ"), bstack111ll_opy_ (u"ࠩࠪෟ"), bstack111ll_opy_ (u"ࠪࠫ෠"), level, data)
          for driver in bstack11l1l1l1l1_opy_:
            if bstack1l11l11l1l_opy_ == driver.session_id:
              driver.execute_script(bstack111ll1111_opy_)
      except Exception as e:
        logger.debug(bstack111ll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡥࡲࡲࡹ࡫ࡸࡵࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨ෡").format(str(e)))
  except Exception as e:
    logger.debug(bstack111ll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡵࡷࡥࡹ࡫ࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻࡾࠩ෢").format(str(e)))
  bstack1l1l1ll11l_opy_(item, call, rep)
def bstack11l111l1l1_opy_(driver, bstack11l1llll11_opy_, test=None):
  global PLATFORM_INDEX
  if test != None:
    bstack11111llll1_opy_ = getattr(test, bstack111ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ෣"), None)
    bstack11l11111ll_opy_ = getattr(test, bstack111ll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ෤"), None)
    PercySDK.screenshot(driver, bstack11l1llll11_opy_, bstack11111llll1_opy_=bstack11111llll1_opy_, bstack11l11111ll_opy_=bstack11l11111ll_opy_, bstack1l111lll1_opy_=PLATFORM_INDEX)
  else:
    PercySDK.screenshot(driver, bstack11l1llll11_opy_)
@measure(event_name=EVENTS.bstack11lll11l1l_opy_, stage=STAGE.bstack1l1l11l1l_opy_, bstack1111l11lll_opy_=SESSION_NAME)
def bstack11l11llll_opy_(driver):
  if bstack1llll1llll_opy_.bstack11l1l11l11_opy_() is True or bstack1llll1llll_opy_.capturing() is True:
    return
  bstack1llll1llll_opy_.bstack1l1l11llll_opy_()
  while not bstack1llll1llll_opy_.bstack11l1l11l11_opy_():
    bstack1111ll1l1_opy_ = bstack1llll1llll_opy_.bstack11l111l11_opy_()
    bstack11l111l1l1_opy_(driver, bstack1111ll1l1_opy_)
  bstack1llll1llll_opy_.bstack1l1l11ll_opy_()
def bstack11ll1l111_opy_(sequence, driver_command, response = None, bstack11111ll11l_opy_ = None, args = None):
    try:
      if sequence != bstack111ll_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨ෥"):
        return
      if percy.bstack11l1111ll_opy_() == bstack111ll_opy_ (u"ࠤࡩࡥࡱࡹࡥࠣ෦"):
        return
      bstack1111ll1l1_opy_ = bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠪࡴࡪࡸࡣࡺࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭෧"), None)
      for command in bstack11lll1ll11_opy_:
        if command == driver_command:
          with bstack1111ll1lll_opy_:
            bstack1111l1111_opy_ = bstack11l1l1l1l1_opy_.copy()
          for driver in bstack1111l1111_opy_:
            bstack11l11llll_opy_(driver)
      bstack1lll111l1l_opy_ = percy.bstack111l1lll1_opy_()
      if driver_command in bstack1lll1lll_opy_[bstack1lll111l1l_opy_]:
        bstack1llll1llll_opy_.bstack1l111lllll_opy_(bstack1111ll1l1_opy_, driver_command)
    except Exception as e:
      pass
_11ll1l1ll1_opy_ = threading.Event()
def bstack1l11ll1ll_opy_(framework_name):
  if global_config.get_property(bstack111ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨ෨")):
      _11ll1l1ll1_opy_.wait(timeout=30)
      return
  global_config.bstack1l1l1llll1_opy_(bstack111ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩ෩"), True)
  global FRAMEWORK_NAME
  global SELENIUM_OR_PLAYWRIGHT_INSTALLED
  global bstack1l11ll11_opy_
  FRAMEWORK_NAME = framework_name
  logger.info(bstack1111ll1ll1_opy_.format(FRAMEWORK_NAME.split(bstack111ll_opy_ (u"࠭࠭ࠨ෪"))[0]))
  bstack1111111111_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    global bstack111111lll_opy_
    bstack1l11l111l1_opy_ = BROWSERSTACK_AUTOMATION or bstack111111lll_opy_
    if bstack1l11l111l1_opy_:
      Service.start = bstack1ll11lll1_opy_
      Service.stop = bstack1l111ll1ll_opy_
      webdriver.Remote.get = bstack111ll1l1l_opy_
      WebDriver.quit = bstack1111l11l1l_opy_
      webdriver.Remote.__init__ = bstack1lll11l1l_opy_
    if not BROWSERSTACK_AUTOMATION and not bstack111111lll_opy_:
        webdriver.Remote.__init__ = bstack1ll111ll1l_opy_
    WebDriver.getAccessibilityResults = getAccessibilityResults
    WebDriver.get_accessibility_results = getAccessibilityResults
    WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
    WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
    WebDriver.performScan = perform_scan
    WebDriver.perform_scan = perform_scan
    WebDriver.execute = bstack11l111l111_opy_
    SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
  except Exception as e:
    pass
  try:
    bstack1l11l111l1_opy_ = BROWSERSTACK_AUTOMATION or bstack111111lll_opy_
    if bstack1l11l111l1_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1lll1lll1l_opy_
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
    logger.debug(bstack111ll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤ࡬ࡲ࡯ࡣࡣ࡯ࡷ࠿ࠦࡻࡾࠤ෫").format(str(e)))
  patch_playwright()
  if not SELENIUM_OR_PLAYWRIGHT_INSTALLED:
    bstack11l11ll1l1_opy_(bstack111ll_opy_ (u"ࠣࡒࡤࡧࡰࡧࡧࡦࡵࠣࡲࡴࡺࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠥ෬"), bstack1l1111llll_opy_)
  if bstack1l1ll1l11_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      if hasattr(RemoteConnection, bstack111ll_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪ෭")) and callable(getattr(RemoteConnection, bstack111ll_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫ෮"))):
        RemoteConnection._get_proxy_url = bstack1l11l1111l_opy_
      else:
        from selenium.webdriver.remote.client_config import ClientConfig
        ClientConfig.get_proxy_url = bstack1l11l1111l_opy_
    except Exception as e:
      logger.error(bstack1l11lll1_opy_.format(str(e)))
  if bstack1ll1ll1l1_opy_():
    bstack1111lll1l_opy_(CONFIG, logger)
  if (bstack111ll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ෯") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      try:
        from pabot.pabot import QueueItem
        from pabot import pabot
      except Exception as e:
        logger.warning(bstack1l11l1llll_opy_ + str(e))
      if not is_robot_playwright_installed():
        try:
          if percy.bstack11l1111ll_opy_() == bstack111ll_opy_ (u"ࠧࡺࡲࡶࡧࠥ෰"):
            bstack1llll1l111_opy_(bstack11ll1l111_opy_)
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
          WebDriverCreator._get_ff_profile = bstack1l111111l_opy_
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
          WebDriverCache.close = bstack1ll1ll11l1_opy_
        except Exception as e:
          logger.warning(bstack1l1llll1l_opy_ + str(e))
        try:
          from AppiumLibrary.utils.applicationcache import ApplicationCache
          ApplicationCache.close = bstack1l1lllll11_opy_
        except Exception as e:
          logger.debug(bstack1llll1l11l_opy_ + str(e))
    except Exception as e:
      bstack11l11ll1l1_opy_(e, bstack1l1llll1l_opy_)
    Output.start_test = bstack11l1l111l_opy_
    Output.end_test = bstack1ll1l1l11l_opy_
    TestStatus.__init__ = bstack1ll11l1l1_opy_
    QueueItem.__init__ = bstack1lll1111l_opy_
    pabot._create_items = bstack1111l11111_opy_
    try:
      from pabot import __version__ as bstack11l11l1l1l_opy_
      if version.parse(bstack11l11l1l1l_opy_) >= version.parse(bstack111ll_opy_ (u"࠭࠵࠯࠲࠱࠴ࠬ෱")):
        pabot._run = bstack11lllll11l_opy_
      elif version.parse(bstack11l11l1l1l_opy_) >= version.parse(bstack111ll_opy_ (u"ࠧ࠵࠰࠵࠲࠵࠭ෲ")):
        pabot._run = bstack1llllll11ll_opy_
      elif version.parse(bstack11l11l1l1l_opy_) >= version.parse(bstack111ll_opy_ (u"ࠨ࠴࠱࠵࠺࠴࠰ࠨෳ")):
        pabot._run = bstack1lll1ll1l_opy_
      elif version.parse(bstack11l11l1l1l_opy_) >= version.parse(bstack111ll_opy_ (u"ࠩ࠵࠲࠶࠹࠮࠱ࠩ෴")):
        pabot._run = bstack11llll11ll_opy_
      else:
        pabot._run = bstack1ll1llll11_opy_
    except Exception as e:
      pabot._run = bstack1ll1llll11_opy_
    pabot._create_command_for_execution = bstack1l1l111l_opy_
    pabot._report_results = bstack1llll1lll1_opy_
  if bstack111ll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ෵") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11l11ll1l1_opy_(e, bstack11111l1l1l_opy_)
    Runner.run_hook = bstack1l1lll111l_opy_
    try:
      from behave import __version__ as bstack1l1l11lll1_opy_
      if version.parse(bstack1l1l11lll1_opy_) >= version.parse(bstack111ll_opy_ (u"ࠫ࠶࠴࠳࠯࠲ࠪ෶")):
        Runner.load_hooks = bstack1lll1l11l1_opy_
    except Exception as e:
      logger.debug(bstack111ll_opy_ (u"ࠬࡉ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤࡧ࡫ࡨࡢࡸࡨࠤࡻ࡫ࡲࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩ෷").format(str(e)))
    Step.run = bstack1l11l111ll_opy_
  if bstack111ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭෸") in str(framework_name).lower():
    if not BROWSERSTACK_AUTOMATION:
      _11ll1l1ll1_opy_.set()
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack1ll1ll1ll1_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack111ll1l1_opy_
      Config.getoption = bstack111l1l1l11_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack11lll1l111_opy_
    except Exception as e:
      pass
  _11ll1l1ll1_opy_.set()
def bstack1l11lllll_opy_():
  global CONFIG
  if bstack111ll_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ෹") in CONFIG and int(CONFIG[bstack111ll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ෺")]) > 1:
    logger.warning(bstack1llll111l1_opy_)
def bstack1l111ll1l1_opy_(arg, bstack11l1111ll1_opy_, bstack1lllll1l111_opy_=None):
  global CONFIG
  global bstack11111l1111_opy_
  global bstack1l11111ll1_opy_
  global BROWSERSTACK_AUTOMATION
  global bstack111111lll_opy_
  global global_config
  bstack1l1ll11ll_opy_ = bstack111ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ෻")
  if bstack11l1111ll1_opy_ and isinstance(bstack11l1111ll1_opy_, str):
    bstack11l1111ll1_opy_ = eval(bstack11l1111ll1_opy_)
  CONFIG = bstack11l1111ll1_opy_[bstack111ll_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪ෼")]
  bstack11111l1111_opy_ = bstack11l1111ll1_opy_[bstack111ll_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬ෽")]
  bstack1l11111ll1_opy_ = bstack11l1111ll1_opy_[bstack111ll_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ෾")]
  BROWSERSTACK_AUTOMATION = bstack11l1111ll1_opy_[bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ෿")]
  try:
    bstack111ll11l1l_opy_ = bstack11l1111ll1_opy_.get(bstack111ll_opy_ (u"ࠧࡐࡘࡈࡖࡗࡏࡄࡆࡡࡏࡓࡆࡊ࡟ࡕࡇࡖࡘࡎࡔࡇࠨ฀"), False)
    bstack111111lll_opy_ = bool(bstack111ll11l1l_opy_)
    os.environ[bstack111ll_opy_ (u"ࠨࡑ࡙ࡉࡗࡘࡉࡅࡇࡢࡐࡔࡇࡄࡠࡖࡈࡗ࡙ࡏࡎࡈࠩก")] = str(bstack111111lll_opy_).lower()
  except Exception as e:
    logger.error(bstack111ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡏࡗࡇࡕࡖࡎࡊࡅࡠࡎࡒࡅࡉࡥࡔࡆࡕࡗࡍࡓࡍ࠺ࠡࡽࢀࠦข").format(e))
    bstack111111lll_opy_ = False
    os.environ[bstack111ll_opy_ (u"ࠪࡓ࡛ࡋࡒࡓࡋࡇࡉࡤࡒࡏࡂࡆࡢࡘࡊ࡙ࡔࡊࡐࡊࠫฃ")] = bstack111ll_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪค")
  global_config.bstack1l1l1llll1_opy_(bstack111ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ฅ"), BROWSERSTACK_AUTOMATION)
  os.environ[bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨฆ")] = bstack1l1ll11ll_opy_
  os.environ[bstack111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌ࠭ง")] = json.dumps(CONFIG)
  os.environ[bstack111ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡉࡗࡅࡣ࡚ࡘࡌࠨจ")] = bstack11111l1111_opy_
  os.environ[bstack111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪฉ")] = str(bstack1l11111ll1_opy_)
  os.environ[bstack111ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡐ࡚ࡍࡉࡏࠩช")] = str(True)
  if bstack11l1ll1ll1_opy_(arg, [bstack111ll_opy_ (u"ࠫ࠲ࡴࠧซ"), bstack111ll_opy_ (u"ࠬ࠳࠭࡯ࡷࡰࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ฌ")]) != -1:
    os.environ[bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡁࡓࡃࡏࡐࡊࡒࠧญ")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack111l111ll1_opy_)
    return
  bstack1lll1l1l1l_opy_()
  global bstack1ll11llll1_opy_
  global PLATFORM_INDEX
  global bstack1lllllll1l_opy_
  global bstack1l1l1llll_opy_
  global bstack1111l1111l_opy_
  global bstack1l11ll11_opy_
  global PARALLELISE_VANILLA_PYTHON
  arg.append(bstack111ll_opy_ (u"ࠢ࠮࡙ࠥฎ"))
  arg.append(bstack111ll_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡥ࠻ࡏࡲࡨࡺࡲࡥࠡࡣ࡯ࡶࡪࡧࡤࡺࠢ࡬ࡱࡵࡵࡲࡵࡧࡧ࠾ࡵࡿࡴࡦࡵࡷ࠲ࡕࡿࡴࡦࡵࡷ࡛ࡦࡸ࡮ࡪࡰࡪࠦฏ"))
  arg.append(bstack111ll_opy_ (u"ࠤ࠰࡛ࠧฐ"))
  arg.append(bstack111ll_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧ࠽ࡘ࡭࡫ࠠࡩࡱࡲ࡯࡮ࡳࡰ࡭ࠤฑ"))
  global bstack1lllll1ll1_opy_
  global bstack111l11l1l_opy_
  global bstack1ll1l1ll1_opy_
  global bstack1ll11111l1_opy_
  global bstack1lll1l111l_opy_
  global bstack1l1ll11l_opy_
  global bstack1ll1l11l_opy_
  global bstack1ll1l1llll_opy_
  global bstack1l1ll1lll_opy_
  global bstack1l1lllllll_opy_
  global bstack1l1lll11ll_opy_
  global bstack11ll111lll_opy_
  global bstack1l1l1ll11l_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1lllll1ll1_opy_ = webdriver.Remote.__init__
    bstack111l11l1l_opy_ = WebDriver.quit
    bstack1ll1l1llll_opy_ = WebDriver.close
    bstack1l1ll1lll_opy_ = WebDriver.get
    bstack1ll1l1ll1_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack111lll111_opy_(CONFIG) and bstack1ll11ll11l_opy_():
    if bstack111111111_opy_() < version.parse(bstack1l1l1l1l1l_opy_):
      logger.error(bstack1l111l1l1l_opy_.format(bstack111111111_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack111ll_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬฒ")) and callable(getattr(RemoteConnection, bstack111ll_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭ณ"))):
          bstack1l1lllllll_opy_ = RemoteConnection._get_proxy_url
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          bstack1l1lllllll_opy_ = ClientConfig.get_proxy_url
      except Exception as e:
        logger.error(bstack1l11lll1_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1l1lll11ll_opy_ = Config.getoption
    from _pytest import runner
    bstack11ll111lll_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warning(bstack111ll_opy_ (u"ࠨࠥࡴ࠼ࠣࠩࡸࠨด"), bstack1111l111l1_opy_, str(e))
  try:
    from pytest_bdd import reporting
    bstack1l1l1ll11l_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack111ll_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨต"))
  if cli.is_enabled(CONFIG) and cli.config:
    bstack1lllllll1l_opy_ = cli.config.get(bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬถ"), {}).get(bstack111ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫท"))
  else:
    bstack1lllllll1l_opy_ = CONFIG.get(bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧธ"), {}).get(bstack111ll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭น"))
  PARALLELISE_VANILLA_PYTHON = True
  if cli.is_enabled(CONFIG):
    if cli.bstack11lll11ll1_opy_():
      bstack11ll1l11_opy_.invoke(Events.CONNECT, bstack1ll11l1l11_opy_())
    platform_index = int(os.environ.get(bstack111ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬบ"), bstack111ll_opy_ (u"࠭࠰ࠨป")))
  else:
    bstack1l11ll1ll_opy_(bstack1111ll11ll_opy_)
  os.environ[bstack111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨผ")] = CONFIG[bstack111ll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪฝ")]
  os.environ[bstack111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬพ")] = CONFIG[bstack111ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ฟ")]
  os.environ[bstack111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧภ")] = BROWSERSTACK_AUTOMATION.__str__()
  from _pytest.config import main as bstack1lll1l11ll_opy_
  bstack11l1l1l11_opy_ = []
  try:
    exit_code = bstack1lll1l11ll_opy_(arg)
    if cli.is_enabled(CONFIG):
      cli.bstack11lll11l_opy_()
    if bstack111ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩม") in multiprocessing.current_process().__dict__.keys():
      for bstack1lll1l1lll_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack11l1l1l11_opy_.append(bstack1lll1l1lll_opy_)
    try:
      bstack1l1ll111ll_opy_ = (bstack11l1l1l11_opy_, int(exit_code))
      bstack1lllll1l111_opy_.append(bstack1l1ll111ll_opy_)
    except:
      bstack1lllll1l111_opy_.append((bstack11l1l1l11_opy_, exit_code))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack11l1l1l11_opy_.append({bstack111ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫย"): bstack111ll_opy_ (u"ࠧࡑࡴࡲࡧࡪࡹࡳࠡࠩร") + os.environ.get(bstack111ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨฤ")), bstack111ll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨล"): traceback.format_exc(), bstack111ll_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩฦ"): int(os.environ.get(bstack111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫว")))})
    bstack1lllll1l111_opy_.append((bstack11l1l1l11_opy_, 1))
def mod_behave_main(args, retries):
  try:
    from behave.configuration import Configuration
    from behave.__main__ import run_behave
    from browserstack_sdk.bstack_behave_runner import BehaveRunner
    config = Configuration(args)
    config.update_userdata({bstack111ll_opy_ (u"ࠧࡸࡥࡵࡴ࡬ࡩࡸࠨศ"): str(retries)})
    return run_behave(config, runner_class=BehaveRunner)
  except Exception as e:
    bstack11lll1l1ll_opy_ = e.__class__.__name__
    print(bstack111ll_opy_ (u"ࠨࠥࡴ࠼ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡦࡪ࡮ࡡࡷࡧࠣࡸࡪࡹࡴࠡࠧࡶࠦษ") % (bstack11lll1l1ll_opy_, e))
    return 1
def bstack111l11l1ll_opy_(arg):
  global bstack111ll1l11_opy_
  bstack1l11ll1ll_opy_(bstack1l1l11l11l_opy_)
  os.environ[bstack111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨส")] = str(bstack1l11111ll1_opy_)
  retries = bstack1ll11l1l_opy_.bstack111l1l11l_opy_(CONFIG)
  status_code = 0
  if bstack1ll11l1l_opy_.bstack1111l11ll1_opy_(CONFIG):
    status_code = mod_behave_main(arg, retries)
  else:
    from behave.__main__ import main as bstack111l1ll1l_opy_
    status_code = bstack111l1ll1l_opy_(arg)
  if status_code != 0:
    bstack111ll1l11_opy_ = status_code
def bstack11l11ll1_opy_():
  logger.info(bstack1l1l1l1l1_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack111ll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧห"), help=bstack111ll_opy_ (u"ࠩࡊࡩࡳ࡫ࡲࡢࡶࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡧࡴࡴࡦࡪࡩࠪฬ"))
  parser.add_argument(bstack111ll_opy_ (u"ࠪ࠱ࡺ࠭อ"), bstack111ll_opy_ (u"ࠫ࠲࠳ࡵࡴࡧࡵࡲࡦࡳࡥࠨฮ"), help=bstack111ll_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫฯ"))
  parser.add_argument(bstack111ll_opy_ (u"࠭࠭࡬ࠩะ"), bstack111ll_opy_ (u"ࠧ࠮࠯࡮ࡩࡾ࠭ั"), help=bstack111ll_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡧࡣࡤࡧࡶࡷࠥࡱࡥࡺࠩา"))
  parser.add_argument(bstack111ll_opy_ (u"ࠩ࠰ࡪࠬำ"), bstack111ll_opy_ (u"ࠪ࠱࠲࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨิ"), help=bstack111ll_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪี"))
  bstack1lll1ll11_opy_ = parser.parse_args()
  try:
    bstack111l1ll1_opy_ = bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡬࡫࡮ࡦࡴ࡬ࡧ࠳ࡿ࡭࡭࠰ࡶࡥࡲࡶ࡬ࡦࠩึ")
    if bstack1lll1ll11_opy_.framework and bstack1lll1ll11_opy_.framework not in (bstack111ll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ื"), bstack111ll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨุ")):
      bstack111l1ll1_opy_ = bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࠱ࡽࡲࡲ࠮ࡴࡣࡰࡴࡱ࡫ูࠧ")
    bstack111ll111ll_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack111l1ll1_opy_)
    bstack111lll11l1_opy_ = open(bstack111ll111ll_opy_, bstack111ll_opy_ (u"ࠩࡵฺࠫ"))
    bstack111l1111l1_opy_ = bstack111lll11l1_opy_.read()
    bstack111lll11l1_opy_.close()
    if bstack1lll1ll11_opy_.username:
      bstack111l1111l1_opy_ = bstack111l1111l1_opy_.replace(bstack111ll_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪ฻"), bstack1lll1ll11_opy_.username)
    if bstack1lll1ll11_opy_.key:
      bstack111l1111l1_opy_ = bstack111l1111l1_opy_.replace(bstack111ll_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭฼"), bstack1lll1ll11_opy_.key)
    if bstack1lll1ll11_opy_.framework:
      bstack111l1111l1_opy_ = bstack111l1111l1_opy_.replace(bstack111ll_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭฽"), bstack1lll1ll11_opy_.framework)
    file_name = bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩ฾")
    file_path = os.path.abspath(file_name)
    bstack111l111111_opy_ = open(file_path, bstack111ll_opy_ (u"ࠧࡸࠩ฿"))
    bstack111l111111_opy_.write(bstack111l1111l1_opy_)
    bstack111l111111_opy_.close()
    logger.info(bstack1l1l1ll1l_opy_)
    try:
      os.environ[bstack111ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪเ")] = bstack1lll1ll11_opy_.framework if bstack1lll1ll11_opy_.framework != None else bstack111ll_opy_ (u"ࠤࠥแ")
      config = yaml.safe_load(bstack111l1111l1_opy_)
      config[bstack111ll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪโ")] = bstack111ll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱ࡸ࡫ࡴࡶࡲࠪใ")
      bstack11111111l1_opy_(bstack1llll11l_opy_, config)
    except Exception as e:
      logger.debug(bstack1ll111llll_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack11lllll11_opy_.format(str(e)))
def bstack11111111l1_opy_(bstack11l111l1ll_opy_, config, bstack1l11lll111_opy_=None, bstack1llll11ll1_opy_=False):
  global BROWSERSTACK_AUTOMATION
  global bstack1l11lll11l_opy_
  global global_config
  if not config:
    return
  if bstack1l11lll111_opy_ is None:
    bstack1l11lll111_opy_ = {}
  bstack1llll11lll_opy_ = bstack111ll111l1_opy_ if not BROWSERSTACK_AUTOMATION else (
    bstack11lllllll_opy_ if bstack111ll_opy_ (u"ࠬࡧࡰࡱࠩไ") in config else (
        bstack1ll1l111l_opy_ if config.get(bstack111ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪๅ")) else bstack11llll1ll_opy_
    )
)
  bstack1l1ll1111_opy_ = False
  bstack1l11l11111_opy_ = False
  if BROWSERSTACK_AUTOMATION is True:
      if bstack111ll_opy_ (u"ࠧࡢࡲࡳࠫๆ") in config:
          bstack1l1ll1111_opy_ = True
      else:
          bstack1l11l11111_opy_ = True
  bstack11ll11l11_opy_ = TestHubUtils.bstack11ll11l1ll_opy_(config, bstack1l11lll11l_opy_)
  bstack1llllllll1l_opy_ = bstack1l1111l1l1_opy_()
  data = {
    bstack111ll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ็"): config[bstack111ll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨ่ࠫ")],
    bstack111ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ้࠭"): config[bstack111ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿ๊ࠧ")],
    bstack111ll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦ๋ࠩ"): bstack11l111l1ll_opy_,
    bstack111ll_opy_ (u"࠭ࡤࡦࡶࡨࡧࡹ࡫ࡤࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ์"): os.environ.get(bstack111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩํ"), bstack1l11lll11l_opy_),
    bstack111ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ๎"): bstack11llll1111_opy_,
    bstack111ll_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯ࠫ๏"): bstack1llllll111_opy_(),
    bstack111ll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭๐"): {
      bstack111ll_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ๑"): str(config[bstack111ll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ๒")]) if bstack111ll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭๓") in config else bstack111ll_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣ๔"),
      bstack111ll_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧ࡙ࡩࡷࡹࡩࡰࡰࠪ๕"): sys.version,
      bstack111ll_opy_ (u"ࠩࡵࡩ࡫࡫ࡲࡳࡧࡵࠫ๖"): bstack1ll111l11l_opy_(os.environ.get(bstack111ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬ๗"), bstack1l11lll11l_opy_)),
      bstack111ll_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭๘"): bstack111ll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ๙"),
      bstack111ll_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧ๚"): bstack1llll11lll_opy_,
      bstack111ll_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬ๛"): bstack11ll11l11_opy_,
      bstack111ll_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡡࡸࡹ࡮ࡪࠧ๜"): os.environ[bstack111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ๝")],
      bstack111ll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭๞"): os.environ.get(bstack111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭๟"), bstack1l11lll11l_opy_),
      bstack111ll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ๠"): bstack11lll1111l_opy_(os.environ.get(bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ๡"), bstack1l11lll11l_opy_)),
      bstack111ll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭๢"): bstack1llllllll1l_opy_.get(bstack111ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭๣")),
      bstack111ll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ๤"): bstack1llllllll1l_opy_.get(bstack111ll_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫ๥")),
      bstack111ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ๦"): config[bstack111ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ๧")] if config[bstack111ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ๨")] else bstack111ll_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣ๩"),
      bstack111ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ๪"): str(config[bstack111ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ๫")]) if bstack111ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ๬") in config else bstack111ll_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧ๭"),
      bstack111ll_opy_ (u"ࠬࡵࡳࠨ๮"): sys.platform,
      bstack111ll_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨ๯"): socket.gethostname(),
      bstack111ll_opy_ (u"ࠧࡪࡵࡆࡐࡎࡋ࡮ࡢࡤ࡯ࡩࡩ࠭๰"): bstack1llll11ll1_opy_,
      bstack111ll_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪ๱"): global_config.get_property(bstack111ll_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫ๲"))
    }
  }
  if not global_config.get_property(bstack111ll_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪ๳")) is None:
    data[bstack111ll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧ๴")][bstack111ll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࡍࡦࡶࡤࡨࡦࡺࡡࠨ๵")] = {
      bstack111ll_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭๶"): bstack111ll_opy_ (u"ࠧࡶࡵࡨࡶࡤࡱࡩ࡭࡮ࡨࡨࠬ๷"),
      bstack111ll_opy_ (u"ࠨࡵ࡬࡫ࡳࡧ࡬ࠨ๸"): global_config.get_property(bstack111ll_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩ๹")),
      bstack111ll_opy_ (u"ࠪࡷ࡮࡭࡮ࡢ࡮ࡑࡹࡲࡨࡥࡳࠩ๺"): global_config.get_property(bstack111ll_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡓࡵࠧ๻"))
    }
  if bstack11l111l1ll_opy_ == bstack11l1ll1l1l_opy_:
    data[bstack111ll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨ๼")][bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡈࡵ࡮ࡧ࡫ࡪࠫ๽")] = bstack11ll11l111_opy_(config)
    data[bstack111ll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪ๾")][bstack111ll_opy_ (u"ࠨ࡫ࡶࡔࡪࡸࡣࡺࡃࡸࡸࡴࡋ࡮ࡢࡤ࡯ࡩࡩ࠭๿")] = percy.bstack11l11l111l_opy_
    data[bstack111ll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬ຀")][bstack111ll_opy_ (u"ࠪࡴࡪࡸࡣࡺࡄࡸ࡭ࡱࡪࡉࡥࠩກ")] = percy.percy_build_id
  if not bstack1ll11l1l_opy_.bstack1lllll111l_opy_(CONFIG):
    data[bstack111ll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧຂ")][bstack111ll_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠩ຃")] = bstack1ll11l1l_opy_.bstack1lllll111l_opy_(CONFIG)
  bstack1l11l11ll_opy_ = bstack111lll1l1l_opy_.bstack1l1l11ll1_opy_(CONFIG, logger)
  bstack111llll111_opy_ = bstack1ll11l1l_opy_.bstack1l1l11ll1_opy_(config=CONFIG)
  if bstack1l11l11ll_opy_ is not None and bstack111llll111_opy_ is not None and bstack111llll111_opy_.bstack11lll11l1_opy_():
    data[bstack111ll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩຄ")][bstack111llll111_opy_.bstack1lllll111ll_opy_()] = bstack1l11l11ll_opy_.bstack1lll1111_opy_()
  update(data[bstack111ll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪ຅")], bstack1l11lll111_opy_)
  try:
    response = bstack1ll11l11l_opy_(bstack111ll_opy_ (u"ࠨࡒࡒࡗ࡙࠭ຆ"), bstack1ll1l1ll11_opy_(bstack111l1l1l1_opy_), data, {
      bstack111ll_opy_ (u"ࠩࡤࡹࡹ࡮ࠧງ"): (config[bstack111ll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬຈ")], config[bstack111ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧຉ")])
    })
    if response:
      logger.debug(bstack1ll1l11l1l_opy_.format(bstack11l111l1ll_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1l111llll1_opy_.format(str(e)))
def bstack1ll111l11l_opy_(framework):
  return bstack111ll_opy_ (u"ࠧࢁࡽ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࡻࡾࠤຊ").format(str(framework), __version__) if framework else bstack111ll_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࢀࢃࠢ຋").format(
    __version__)
def bstack1lll1l1l1l_opy_():
  global CONFIG
  global bstack111llllll_opy_
  if bool(CONFIG):
    return
  try:
    bstack1l1111l1_opy_()
    logger.debug(bstack11111l1l_opy_.format(str(CONFIG)))
    bstack111llllll_opy_ = logger_utils.configure_logger(CONFIG, bstack111llllll_opy_)
    bstack1111111111_opy_()
  except Exception as e:
    logger.error(bstack111ll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱ࠮ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠦຌ") + str(e))
    sys.exit(1)
  atexit.register(bstack1l111111ll_opy_)
  if not os.environ.get(bstack111ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡆࡈࡣࡕࡒࡕࡈࡋࡑࡣࡒࡕࡄࡆࠩຍ")):
    sys.excepthook = bstack1l11l1l1l1_opy_
    signal.signal(signal.SIGINT, bstack111l111l1l_opy_)
    signal.signal(signal.SIGTERM, bstack111l111l1l_opy_)
def bstack1l11l1l1l1_opy_(exctype, value, traceback):
  global bstack11l1l1l1l1_opy_
  try:
    for driver in bstack11l1l1l1l1_opy_:
      bstack11ll1l1l1_opy_(driver, bstack111ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩຎ"), bstack111ll_opy_ (u"ࠥࡗࡪࡹࡳࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨຏ") + str(value))
  except Exception:
    pass
  logger.info(bstack11111111ll_opy_)
  bstack1l11l11l_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1l11l11l_opy_(message=bstack111ll_opy_ (u"ࠫࠬຐ"), bstack11l11l11l1_opy_ = False, bstack1llll11ll1_opy_ = False):
  global CONFIG
  global global_config
  bstack11l1l1llll_opy_ = bstack111ll_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠧຑ") if bstack11l11l11l1_opy_ else bstack111ll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬຒ")
  bstack1ll1111ll1_opy_ = bstack111l1l1l_opy_.bstack1ll1111l1_opy_(EVENTS.bstack1l11llll11_opy_)
  try:
    bstack1l11lll111_opy_ = {}
    bstack1l11111l1l_opy_ = global_config.get_property(bstack111ll_opy_ (u"ࠧࡠࡪࡸࡦࡆࡲ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࡅࡣࡷࡥࠬຓ"))
    if bstack1l11111l1l_opy_:
      bstack1l11lll111_opy_[bstack111ll_opy_ (u"ࠨࡪࡸࡦࡆࡲ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨດ")] = bstack1l11111l1l_opy_
    if message:
      bstack1l11lll111_opy_[bstack11l1l1llll_opy_] = str(message)
    try:
      bstack11111111l1_opy_(bstack11l1ll1l1l_opy_, CONFIG, bstack1l11lll111_opy_, bstack1llll11ll1_opy_)
    finally:
      bstack111l1l1l_opy_.end(EVENTS.bstack1l11llll11_opy_.value, bstack1ll1111ll1_opy_ + bstack111ll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤຕ"), bstack1ll1111ll1_opy_ + bstack111ll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣຖ"), status=True, failure=None, test_name=None)
  except Exception as e:
    logger.debug(bstack1lllll11_opy_.format(str(e)))
def bstack1l1l1ll11_opy_(bstack11llllll1l_opy_, size):
  bstack1l111ll1_opy_ = []
  while len(bstack11llllll1l_opy_) > size:
    bstack1llllllll11_opy_ = bstack11llllll1l_opy_[:size]
    bstack1l111ll1_opy_.append(bstack1llllllll11_opy_)
    bstack11llllll1l_opy_ = bstack11llllll1l_opy_[size:]
  bstack1l111ll1_opy_.append(bstack11llllll1l_opy_)
  return bstack1l111ll1_opy_
def bstack11llll111_opy_(args):
  if bstack111ll_opy_ (u"ࠫ࠲ࡳࠧທ") in args and bstack111ll_opy_ (u"ࠬࡶࡤࡣࠩຘ") in args:
    return True
  return False
@measure(event_name=EVENTS.bstack11l1l1ll11_opy_, stage=STAGE.bstack11llll1l1_opy_)
def run_on_browserstack(bstack1l1l1lll1_opy_=None, bstack1lllll1l111_opy_=None, bstack111l1l111_opy_=False):
  global CONFIG
  global bstack11111l1111_opy_
  global bstack1l11111ll1_opy_
  global bstack1l11lll11l_opy_
  global global_config
  bstack1l1ll11ll_opy_ = bstack111ll_opy_ (u"࠭ࠧນ")
  bstack11lll11111_opy_ = bstack111ll_opy_ (u"ࠢࠣບ")
  bstack1llll111l_opy_(bstack1l1lll11_opy_, logger)
  if bstack1l1l1lll1_opy_ and isinstance(bstack1l1l1lll1_opy_, str):
    bstack1l1l1lll1_opy_ = eval(bstack1l1l1lll1_opy_)
  if bstack1l1l1lll1_opy_:
    CONFIG = bstack1l1l1lll1_opy_[bstack111ll_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨປ")]
    bstack11111l1111_opy_ = bstack1l1l1lll1_opy_[bstack111ll_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪຜ")]
    bstack1l11111ll1_opy_ = bstack1l1l1lll1_opy_[bstack111ll_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬຝ")]
    global_config.bstack1l1l1llll1_opy_(bstack111ll_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ພ"), bstack1l11111ll1_opy_)
    bstack1l1ll11ll_opy_ = bstack111ll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨ࠭ຟ")
  global_config.bstack1l1l1llll1_opy_(bstack111ll_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨຠ"), uuid4().__str__())
  logger.info(bstack111ll_opy_ (u"ࠧࡔࡆࡎࠤࡷࡻ࡮ࠡࡵࡷࡥࡷࡺࡥࡥࠢࡺ࡭ࡹ࡮ࠠࡪࡦ࠽ࠤࠬມ") + global_config.get_property(bstack111ll_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪຢ")));
  logger.debug(bstack111ll_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࡁࠬຣ") + global_config.get_property(bstack111ll_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࠬ຤")))
  if not bstack111l1l111_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack111l111ll1_opy_)
      return
    if sys.argv[1] == bstack111ll_opy_ (u"ࠫ࠲࠳ࡶࡦࡴࡶ࡭ࡴࡴࠧລ") or sys.argv[1] == bstack111ll_opy_ (u"ࠬ࠳ࡶࠨ຦"):
      logger.info(bstack111ll_opy_ (u"࠭ࡂࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡖࡹࡵࡪࡲࡲ࡙ࠥࡄࡌࠢࡹࡿࢂ࠭ວ").format(__version__))
      return
    if sys.argv[1] == bstack111ll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ຨ"):
      bstack11l11ll1_opy_()
      return
    if sys.argv[1] == bstack111ll_opy_ (u"ࠨ࡮ࡲࡥࡩ࠭ຩ"):
      from browserstack_sdk.bstack1lll1l1111_opy_ import bstack111l1lll11_opy_
      bstack1lll1l1l1l_opy_()
      bstack111l1lll11_opy_(CONFIG)
      return
  args = sys.argv
  bstack1lll1l1l1l_opy_()
  global bstack111111lll_opy_
  try:
    from bstack_utils import constants as bstack1111lll1_opy_
    override_value = CONFIG.get(bstack111ll_opy_ (u"ࠩࡲࡺࡪࡸࡲࡪࡦࡨࡐࡴࡧࡤࡕࡧࡶࡸ࡮ࡴࡧࠨສ"), False)
    bstack111111lll_opy_ = bool(override_value)
  except Exception as e:
    logger.error(bstack111ll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡐࡘࡈࡖࡗࡏࡄࡆࡡࡏࡓࡆࡊ࡟ࡕࡇࡖࡘࡎࡔࡇ࠻ࠢࡾࢁࠧຫ").format(e))
    bstack111111lll_opy_ = False
  if bstack111111lll_opy_:
    bstack111ll1l11l_opy_ = CONFIG.get(bstack111ll_opy_ (u"ࠫࡱࡵࡡࡥࡖࡨࡷࡹ࡯࡮ࡨࡊࡸࡦ࡚ࡘࡌࠨຬ")) or bstack1111lll1_opy_.bstack11l1111l1l_opy_
    logger.info(bstack111ll_opy_ (u"ࠧࡍ࡬ࡰࡤࡤࡰࠥࡵࡶࡦࡴࡵ࡭ࡩ࡫࡬ࡰࡣࡧࡸࡪࡹࡴࡪࡰࡪࠤࡪࡴࡡࡣ࡮ࡨࡨ࠱ࠦࡵࡴ࡫ࡱ࡫ࠥ࡮ࡵࡣ࠼ࠣࡿࢂࠨອ").format(bstack111ll1l11l_opy_))
    bstack11111l1111_opy_ = bstack111ll1l11l_opy_
    try:
      bstack1111lll1_opy_.bstack1ll111l1ll_opy_ = bstack111ll1l11l_opy_
      bstack1111lll1_opy_.bstack111111l1l_opy_ = bstack111ll1l11l_opy_
    except Exception:
      pass
  global bstack1ll11llll1_opy_
  global bstack1ll11ll1ll_opy_
  global PARALLELISE_VANILLA_PYTHON
  global PARALLELISE_THREADING_PYTHON
  global PLATFORM_INDEX
  global bstack1lllllll1l_opy_
  global bstack1l1l1llll_opy_
  global bstack1ll11l1l1l_opy_
  global bstack1111l1111l_opy_
  global bstack1l11ll11_opy_
  global bstack11llll1l1l_opy_
  bstack1ll11ll1ll_opy_ = len(CONFIG.get(bstack111ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩຮ"), []))
  if not bstack1l1ll11ll_opy_:
    if args[1] == bstack111ll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧຯ") or args[1] == bstack111ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩະ") or args[1] == bstack111ll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠪັ"):
      bstack1l1ll11ll_opy_ = bstack111ll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠫາ")
      args = args[2:]
    elif args[1] == bstack111ll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪຳ"):
      bstack1l1ll11ll_opy_ = bstack111ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫິ")
      args = args[2:]
    elif args[1] == bstack111ll_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬີ"):
      bstack1l1ll11ll_opy_ = bstack111ll_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ຶ")
      args = args[2:]
    elif args[1] == bstack111ll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩື"):
      bstack1l1ll11ll_opy_ = bstack111ll_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ຸࠪ")
      args = args[2:]
    elif args[1] == bstack111ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶູࠪ"):
      bstack1l1ll11ll_opy_ = bstack111ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ຺ࠫ")
      args = args[2:]
    elif args[1] == bstack111ll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬົ"):
      bstack1l1ll11ll_opy_ = bstack111ll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ຼ")
      args = args[2:]
    else:
      if not bstack111ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪຽ") in CONFIG or str(CONFIG[bstack111ll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ຾")]).lower() in [bstack111ll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ຿"), bstack111ll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫເ"), bstack111ll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠬແ")]:
        bstack1l1ll11ll_opy_ = bstack111ll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨ࠭ໂ")
        args = args[1:]
      elif str(CONFIG[bstack111ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩໃ")]).lower() == bstack111ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ໄ"):
        bstack1l1ll11ll_opy_ = bstack111ll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ໅")
        args = args[1:]
      elif str(CONFIG[bstack111ll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬໆ")]).lower() == bstack111ll_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ໇"):
        bstack1l1ll11ll_opy_ = bstack111ll_opy_ (u"ࠫࡵࡧࡢࡰࡶ່ࠪ")
        args = args[1:]
      elif str(CONFIG[bstack111ll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ້")]).lower() == bstack111ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ໊࠭"):
        bstack1l1ll11ll_opy_ = bstack111ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ໋ࠧ")
        args = args[1:]
      elif str(CONFIG[bstack111ll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ໌")]).lower() == bstack111ll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩໍ"):
        bstack1l1ll11ll_opy_ = bstack111ll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ໎")
        args = args[1:]
      else:
        os.environ[bstack111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭໏")] = bstack1l1ll11ll_opy_
        bstack1ll11l111_opy_(bstack11l11lll1_opy_)
  os.environ[bstack111ll_opy_ (u"ࠬࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉ࠭໐")] = bstack1l1ll11ll_opy_
  bstack1l11lll11l_opy_ = bstack1l1ll11ll_opy_
  if cli.is_enabled(CONFIG):
    bstack1l1111ll11_opy_ = os.environ.get(bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡓࡆࡕࡖࡍࡔࡔ࡟ࡊࡆࠪ໑"), bstack111ll_opy_ (u"ࠧࠨ໒")) != bstack111ll_opy_ (u"ࠨࠩ໓")
    if bstack1l1111ll11_opy_:
        try:
          bstack11ll1l11_opy_.invoke(Events.CONNECT, bstack1ll11l1l11_opy_())
        except Exception as e:
          bstack11ll1l11_opy_.invoke(Events.bstack111ll1ll11_opy_, e.__traceback__, 1)
    else:
        try:
          if bstack1l1ll11ll_opy_ == bstack111ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ໔") and bstack11l1ll1l1_opy_():
            bstack1l1llll1ll_opy_ = bstack1ll11ll1l_opy_[bstack111ll_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖ࠰ࡆࡉࡊࠧ໕")]
          elif bstack1l1ll11ll_opy_ in [bstack111ll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ໖"), bstack111ll_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ໗")]:
            bstack1l1llll1ll_opy_ = bstack111ll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ໘")
          else:
            bstack1l1llll1ll_opy_ = bstack1l1ll11ll_opy_
          bstack11ll1l11_opy_.invoke(Events.bstack1ll111l1_opy_, bstack1l1l1lllll_opy_(
        sdk_version=__version__,
        path_config=bstack11ll1ll1ll_opy_(),
        path_project=os.getcwd(),
        test_framework=bstack1l1llll1ll_opy_,
        frameworks=[bstack1l1llll1ll_opy_],
        framework_versions={
          bstack1l1llll1ll_opy_: bstack11lll1111l_opy_(bstack111ll_opy_ (u"ࠧࡓࡱࡥࡳࡹ࠭໙") if bstack1l1ll11ll_opy_ in [bstack111ll_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ໚"), bstack111ll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ໛"), bstack111ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫໜ")] else bstack1l1ll11ll_opy_)
        },
        bs_config=CONFIG
      ))
          if cli.config and cli.config.get(bstack111ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࠨໝ"), None):
            CONFIG[bstack111ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠢໞ")] = cli.config.get(bstack111ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣໟ"), None)
        except Exception as e:
          bstack11ll1l11_opy_.invoke(Events.bstack111ll1ll11_opy_, e.__traceback__, 1)
    if bstack1l11111ll1_opy_:
      CONFIG[bstack111ll_opy_ (u"ࠢࡢࡲࡳࠦ໠")] = cli.config[bstack111ll_opy_ (u"ࠣࡣࡳࡴࠧ໡")]
      logger.info(bstack1l1l11l111_opy_.format(CONFIG[bstack111ll_opy_ (u"ࠩࡤࡴࡵ࠭໢")]))
  else:
    bstack11ll1l11_opy_.clear()
  global bstack11l1ll1lll_opy_
  global bstack1l1l1lll11_opy_
  if bstack1l1l1lll1_opy_:
    try:
      bstack1l11111lll_opy_ = datetime.datetime.now()
      os.environ[bstack111ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬ໣")] = bstack1l1ll11ll_opy_
      bstack1l111lll_opy_ = bstack111l1l1l_opy_.bstack1ll1111l1_opy_(EVENTS.bstack11l1l111_opy_)
      try:
        logger.info(bstack111ll_opy_ (u"ࠦࡘ࡫࡮ࡥ࡫ࡱ࡫࡙ࠥࡄࡌࠢࡗࡩࡸࡺࠠࡂࡶࡷࡩࡲࡶࡴࡦࡦࠣࡩࡻ࡫࡮ࡵࠤ໤"))
        bstack11111111l1_opy_(bstack1lll11l11_opy_, CONFIG)
      finally:
        bstack111l1l1l_opy_.end(EVENTS.bstack11l1l111_opy_.value, bstack1l111lll_opy_ + bstack111ll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ໥"), bstack1l111lll_opy_ + bstack111ll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ໦"), status=True, failure=None, test_name=None)
      cli.bstack1ll11111l_opy_(bstack111ll_opy_ (u"ࠢࡩࡶࡷࡴ࠿ࡹࡤ࡬ࡡࡷࡩࡸࡺ࡟ࡢࡶࡷࡩࡲࡶࡴࡦࡦࠥ໧"), datetime.datetime.now() - bstack1l11111lll_opy_)
    except Exception as e:
      logger.debug(bstack1ll11l111l_opy_.format(str(e)))
  global bstack1lllll1ll1_opy_
  global bstack111l11l1l_opy_
  global bstack111111lll1_opy_
  global bstack1l1llll11_opy_
  global bstack1l111l1ll_opy_
  global bstack111l1l1111_opy_
  global bstack1ll11111l1_opy_
  global bstack1lll1l111l_opy_
  global bstack1ll1lll11l_opy_
  global bstack1l1ll11l_opy_
  global bstack1ll1l11l_opy_
  global bstack1ll1l1llll_opy_
  global bstack11111l111_opy_
  global bstack1l11ll1l_opy_
  global bstack1l111ll111_opy_
  global bstack1l1ll1lll_opy_
  global bstack1l1lllllll_opy_
  global bstack1l1lll11ll_opy_
  global bstack11ll111lll_opy_
  global bstack1lll1ll1l1_opy_
  global bstack1l1l1ll11l_opy_
  global bstack1ll1l1ll1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1lllll1ll1_opy_ = webdriver.Remote.__init__
    bstack111l11l1l_opy_ = WebDriver.quit
    bstack1ll1l1llll_opy_ = WebDriver.close
    bstack1l1ll1lll_opy_ = WebDriver.get
    bstack1ll1l1ll1_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack11l1ll1lll_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack111l1l1ll1_opy_
    bstack1l1l1lll11_opy_ = bstack111l1l1ll1_opy_()
  except Exception as e:
    pass
  try:
    global bstack11l11ll11l_opy_
    from QWeb.keywords import browser
    bstack11l11ll11l_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack111lll111_opy_(CONFIG) and bstack1ll11ll11l_opy_():
    if bstack111111111_opy_() < version.parse(bstack1l1l1l1l1l_opy_):
      logger.error(bstack1l111l1l1l_opy_.format(bstack111111111_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack111ll_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩ໨")) and callable(getattr(RemoteConnection, bstack111ll_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪ໩"))):
          RemoteConnection._get_proxy_url = bstack1l11l1111l_opy_
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          ClientConfig.get_proxy_url = bstack1l11l1111l_opy_
      except Exception as e:
        logger.error(bstack1l11lll1_opy_.format(str(e)))
  if not CONFIG.get(bstack111ll_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬ໪"), False) and not bstack1l1l1lll1_opy_:
    logger.info(bstack1ll1111ll_opy_)
  bstack1lllll1ll11_opy_ = not cli.is_enabled(CONFIG) and bstack1l1ll11ll_opy_ not in [bstack111ll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ໫")]
  bstack1l11l1ll_opy_ = bstack1lllll1ll11_opy_ and bstack111ll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ໬") in CONFIG and str(CONFIG[bstack111ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ໭")]).lower() != bstack111ll_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭໮")
  bstack1ll11llll_opy_ = bstack1lllll1ll11_opy_ and not bstack1l11l1ll_opy_ and (bstack1l1ll11ll_opy_ != bstack111ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩ໯") or (bstack1l1ll11ll_opy_ == bstack111ll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠪ໰") and not bstack1l1l1lll1_opy_))
  if bstack1l1ll11ll_opy_ not in [bstack111ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ໱")]:
    bstack1llll111l_opy_(os.path.join(os.getcwd(), bstack111ll_opy_ (u"ࠫࡱࡵࡧࠨ໲"), bstack111ll_opy_ (u"ࠬࡱࡥࡺ࠯ࡰࡩࡹࡸࡩࡤࡵ࠱࡮ࡸࡵ࡮ࠨ໳")), logger)
  if (bstack1l1ll11ll_opy_ in [bstack111ll_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ໴"), bstack111ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭໵"), bstack111ll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ໶")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      try:
        from pabot.pabot import QueueItem
        from pabot import pabot
      except Exception as e:
        logger.warning(bstack1l11l1llll_opy_ + str(e))
      if not is_robot_playwright_installed():
        try:
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
          WebDriverCreator._get_ff_profile = bstack1l111111l_opy_
          bstack111l1l1111_opy_ = WebDriverCache.close
        except Exception as e:
          logger.warning(bstack1l1llll1l_opy_ + str(e))
        try:
          from AppiumLibrary.utils.applicationcache import ApplicationCache
          bstack1l111l1ll_opy_ = ApplicationCache.close
        except Exception as e:
          logger.debug(bstack1llll1l11l_opy_ + str(e))
    except Exception as e:
      bstack11l11ll1l1_opy_(e, bstack1l1llll1l_opy_)
    if bstack1l1ll11ll_opy_ != bstack111ll_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ໷"):
      bstack1l111llll_opy_()
    bstack111111lll1_opy_ = Output.start_test
    bstack1l1llll11_opy_ = Output.end_test
    bstack1ll11111l1_opy_ = TestStatus.__init__
    bstack1ll1lll11l_opy_ = pabot._run
    bstack1l1ll11l_opy_ = QueueItem.__init__
    bstack1ll1l11l_opy_ = pabot._create_command_for_execution
    bstack1lll1ll1l1_opy_ = pabot._report_results
  if bstack1l1ll11ll_opy_ == bstack111ll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ໸"):
    global bstack11l11l1ll1_opy_
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11l11ll1l1_opy_(e, bstack11111l1l1l_opy_)
    bstack11111l111_opy_ = Runner.run_hook
    bstack1l11ll1l_opy_ = Runner.load_hooks
    bstack1l111ll111_opy_ = Step.run
    try:
      sig = inspect.signature(bstack11111l111_opy_)
      params = list(sig.parameters.keys())
      bstack11l11l1ll1_opy_ = bstack111ll_opy_ (u"ࠫࡨࡵ࡮ࡵࡧࡻࡸࠬ໹") in params
      logger.info(bstack111ll_opy_ (u"ࠬࡊࡥࡵࡧࡦࡸࡪࡪࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡳࡷࡱࡣ࡭ࡵ࡯࡬ࠢࡶ࡭࡬ࡴࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩ໺").format(bstack111ll_opy_ (u"࠭࠱࠯࠴࠱࠺ࠥ࠮ࡷࡪࡶ࡫ࠤࡨࡵ࡮ࡵࡧࡻࡸ࠮࠭໻") if bstack11l11l1ll1_opy_ else bstack111ll_opy_ (u"ࠧ࠲࠰࠶࠯ࠥ࠮ࡷࡪࡶ࡫ࡳࡺࡺࠠࡤࡱࡱࡸࡪࡾࡴࠪࠩ໼")))
    except Exception as e:
      logger.debug(bstack111ll_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡥࡷࠤࡧ࡫ࡨࡢࡸࡨࠤࡷࡻ࡮ࡠࡪࡲࡳࡰࠦࡳࡪࡩࡱࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭໽").format(str(e)))
      bstack11l11l1ll1_opy_ = None
  if bstack1l1ll11ll_opy_ == bstack111ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ໾"):
    try:
      from _pytest.config import Config
      bstack1l1lll11ll_opy_ = Config.getoption
      from _pytest import runner
      bstack11ll111lll_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warning(bstack111ll_opy_ (u"ࠥࠩࡸࡀࠠࠦࡵࠥ໿"), bstack1111l111l1_opy_, str(e))
    try:
      from pytest_bdd import reporting
      bstack1l1l1ll11l_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack111ll_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡳࠥࡸࡵ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࡷࠬༀ"))
    if bstack1l1llll1l1_opy_():
      logger.warning(bstack11l1l11ll1_opy_[bstack111ll_opy_ (u"࡙ࠬࡄࡌ࠯ࡊࡉࡓ࠳࠰࠱࠷ࠪ༁")])
  try:
    framework_name = bstack111ll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ༂") if bstack1l1ll11ll_opy_ in [bstack111ll_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭༃"), bstack111ll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ༄"), bstack111ll_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ༅")] else bstack1111l1l1_opy_(bstack1l1ll11ll_opy_)
    bstack1lll111l11_opy_ = {
      bstack111ll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࠫ༆"): bstack111ll_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷ࠱ࡨࡻࡣࡶ࡯ࡥࡩࡷ࠭༇") if bstack1l1ll11ll_opy_ == bstack111ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ༈") and bstack11l1ll1l1_opy_() else framework_name,
      bstack111ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ༉"): bstack11lll1111l_opy_(framework_name),
      bstack111ll_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ༊"): __version__,
      bstack111ll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡺࡹࡥࡥࠩ་"): bstack1l1ll11ll_opy_
    }
    if bstack1l1ll11ll_opy_ in bstack1111ll111_opy_ + bstack111111l1ll_opy_:
      if a11y.is_enabled_root(CONFIG):
        if bstack111ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ༌") in CONFIG:
          os.environ[bstack111ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ།")] = os.getenv(bstack111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ༎"), json.dumps(CONFIG[bstack111ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ༏")]))
          CONFIG[bstack111ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭༐")].pop(bstack111ll_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬ༑"), None)
          CONFIG[bstack111ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ༒")].pop(bstack111ll_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ༓"), None)
        bstack111l1l1ll_opy_ = bstack111ll_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧ༔") if CONFIG.get(bstack111ll_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪ༕")) or bstack111l1111ll_opy_() else bstack111ll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧ༖")
        if bstack111l1l1ll_opy_ == bstack111ll_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪ༗"):
          try:
            import importlib.metadata as _1ll11l11l1_opy_
            bstack111l11l11_opy_ = _1ll11l11l1_opy_.version(bstack111ll_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ༘ࠦ"))
          except Exception:
            bstack111l11l11_opy_ = bstack111ll_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯༙ࠩ")
        else:
          bstack111l11l11_opy_ = str(bstack111111111_opy_())
        bstack1lll111l11_opy_[bstack111ll_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ༚")] = {
          bstack111ll_opy_ (u"ࠪࡲࡦࡳࡥࠨ༛"): bstack111l1l1ll_opy_,
          bstack111ll_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬ༜"): bstack111l11l11_opy_
        }
    bstack1l111l1111_opy_, bstack1ll1lll11_opy_ = None, {}
    bstack1l1l11ll1l_opy_ = None
    bstack111lll1l1_opy_ = None
    def bstack1ll1l11l1_opy_():
      if bstack1l11l1ll_opy_:
        bstack11ll1111_opy_()
      elif bstack1ll11llll_opy_:
        bstack11l111llll_opy_()
    def bstack1l1l11111l_opy_():
      nonlocal bstack1l111l1111_opy_, bstack1ll1lll11_opy_
      if bstack1l1ll11ll_opy_ not in [bstack111ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭༝")] and not cli.is_running():
        bstack1l111l1111_opy_, bstack1ll1lll11_opy_ = TestHubHandler.launch(CONFIG, bstack1lll111l11_opy_)
    if bstack1l11l1ll_opy_ or bstack1ll11llll_opy_:
      bstack1l1l11ll1l_opy_ = threading.Thread(target=bstack1ll1l11l1_opy_)
      bstack1l1l11ll1l_opy_.start()
    if bstack1l1ll11ll_opy_ not in [bstack111ll_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧ༞")] and not cli.is_running():
      bstack111lll1l1_opy_ = threading.Thread(target=bstack1l1l11111l_opy_)
      bstack111lll1l1_opy_.start()
    if bstack1l1l11ll1l_opy_:
      bstack1l1l11ll1l_opy_.join()
    if bstack111lll1l1_opy_:
      bstack111lll1l1_opy_.join()
    if bstack1ll1lll11_opy_.get(bstack111ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ༟")) is not None and a11y.bstack111lll11ll_opy_(CONFIG) is None:
      value = bstack1ll1lll11_opy_[bstack111ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ༠")].get(bstack111ll_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪ༡"))
      if value is not None:
          CONFIG[bstack111ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ༢")] = value
      else:
        logger.debug(bstack111ll_opy_ (u"ࠦࡓࡵࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡥࡣࡷࡥࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡳࡧࡶࡴࡴࡴࡳࡦࠤ༣"))
  except Exception as e:
    logger.debug(bstack111ll1l1ll_opy_.format(bstack111ll_opy_ (u"࡚ࠬࡥࡴࡶࡋࡹࡧ࠭༤"), str(e)))
  if bstack1l1ll11ll_opy_ == bstack111ll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡧࡦࡰࡨࡶ࡮ࡩࠧ༥"):
    PARALLELISE_VANILLA_PYTHON = True
    if bstack1l1l1lll1_opy_ and bstack111l1l111_opy_:
      if cli.is_enabled(CONFIG):
        bstack1lllllll1l_opy_ = cli.config.get(bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ༦"), {}).get(bstack111ll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ༧")) if cli.config else None
      else:
        bstack1lllllll1l_opy_ = CONFIG.get(bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭༨"), {}).get(bstack111ll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ༩"))
      bstack1l11ll1ll_opy_(bstack1l1111111_opy_)
    elif bstack1l1l1lll1_opy_:
      if cli.is_enabled(CONFIG):
        bstack1lllllll1l_opy_ = cli.config.get(bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ༪"), {}).get(bstack111ll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ༫")) if cli.config else None
      else:
        bstack1lllllll1l_opy_ = CONFIG.get(bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ༬"), {}).get(bstack111ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ༭"))
      global bstack11l1l1l1l1_opy_
      try:
        if bstack11llll111_opy_(bstack1l1l1lll1_opy_[bstack111ll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ༮")]) and multiprocessing.current_process().name == bstack111ll_opy_ (u"ࠩ࠳ࠫ༯"):
          bstack1l1l1lll1_opy_[bstack111ll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭༰")].remove(bstack111ll_opy_ (u"ࠫ࠲ࡳࠧ༱"))
          bstack1l1l1lll1_opy_[bstack111ll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ༲")].remove(bstack111ll_opy_ (u"࠭ࡰࡥࡤࠪ༳"))
          bstack1l1l1lll1_opy_[bstack111ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ༴")] = bstack1l1l1lll1_opy_[bstack111ll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨ༵ࠫ")][0]
          with open(bstack1l1l1lll1_opy_[bstack111ll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ༶")], bstack111ll_opy_ (u"ࠪࡶ༷ࠬ")) as f:
            file_content = f.read()
          bstack11ll1ll1_opy_ = bstack111ll_opy_ (u"ࠦࠧࠨࡦࡳࡱࡰࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡷࡩࡱࠠࡪ࡯ࡳࡳࡷࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡧ࠾ࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿ࡫ࠨࡼࡿࠬ࠿ࠥ࡬ࡲࡰ࡯ࠣࡴࡩࡨࠠࡪ࡯ࡳࡳࡷࡺࠠࡑࡦࡥ࠿ࠥࡵࡧࡠࡦࡥࠤࡂࠦࡐࡥࡤ࠱ࡨࡴࡥࡢࡳࡧࡤ࡯ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡧࡩ࡫ࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠪࡶࡩࡱ࡬ࠬࠡࡣࡵ࡫࠱ࠦࡴࡦ࡯ࡳࡳࡷࡧࡲࡺࠢࡀࠤ࠵࠯࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡴࡳࡻ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡦࡸࡧࠡ࠿ࠣࡷࡹࡸࠨࡪࡰࡷࠬࡦࡸࡧࠪ࠭࠴࠴࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡪࡾࡣࡦࡲࡷࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡢࡵࠣࡩ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡰࡢࡵࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡲ࡫ࡤࡪࡢࠩࡵࡨࡰ࡫࠲ࡡࡳࡩ࠯ࡸࡪࡳࡰࡰࡴࡤࡶࡾ࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡔࡩࡨ࠮ࡥࡱࡢࡦࠥࡃࠠ࡮ࡱࡧࡣࡧࡸࡥࡢ࡭ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡐࡥࡤ࠱ࡨࡴࡥࡢࡳࡧࡤ࡯ࠥࡃࠠ࡮ࡱࡧࡣࡧࡸࡥࡢ࡭ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡐࡥࡤࠫ࠭࠳ࡹࡥࡵࡡࡷࡶࡦࡩࡥࠩࠫ࡟ࡲࠧࠨࠢ༸").format(str(bstack1l1l1lll1_opy_))
          bstack11111111l_opy_ = bstack11ll1ll1_opy_ + file_content
          bstack1l11ll111l_opy_ = bstack1l1l1lll1_opy_[bstack111ll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ༹")] + bstack111ll_opy_ (u"࠭࡟ࡣࡵࡷࡥࡨࡱ࡟ࡵࡧࡰࡴ࠳ࡶࡹࠨ༺")
          with open(bstack1l11ll111l_opy_, bstack111ll_opy_ (u"ࠧࡸࠩ༻")):
            pass
          with open(bstack1l11ll111l_opy_, bstack111ll_opy_ (u"ࠣࡹ࠮ࠦ༼")) as f:
            f.write(bstack11111111l_opy_)
          import subprocess
          bstack1l111l11l_opy_ = subprocess.run([bstack111ll_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࠤ༽"), bstack1l11ll111l_opy_])
          if os.path.exists(bstack1l11ll111l_opy_):
            os.unlink(bstack1l11ll111l_opy_)
          os._exit(bstack1l111l11l_opy_.returncode)
        else:
          if bstack11llll111_opy_(bstack1l1l1lll1_opy_[bstack111ll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭༾")]):
            bstack1l1l1lll1_opy_[bstack111ll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ༿")].remove(bstack111ll_opy_ (u"ࠬ࠳࡭ࠨཀ"))
            bstack1l1l1lll1_opy_[bstack111ll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩཁ")].remove(bstack111ll_opy_ (u"ࠧࡱࡦࡥࠫག"))
            bstack1l1l1lll1_opy_[bstack111ll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫགྷ")] = bstack1l1l1lll1_opy_[bstack111ll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬང")][0]
          bstack1l11ll1ll_opy_(bstack1l1111111_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1l1l1lll1_opy_[bstack111ll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ཅ")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack111ll_opy_ (u"ࠫࡤࡥ࡮ࡢ࡯ࡨࡣࡤ࠭ཆ")] = bstack111ll_opy_ (u"ࠬࡥ࡟࡮ࡣ࡬ࡲࡤࡥࠧཇ")
          mod_globals[bstack111ll_opy_ (u"࠭࡟ࡠࡨ࡬ࡰࡪࡥ࡟ࠨ཈")] = os.path.abspath(bstack1l1l1lll1_opy_[bstack111ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪཉ")])
          exec(open(bstack1l1l1lll1_opy_[bstack111ll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫཊ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack111ll_opy_ (u"ࠩࡆࡥࡺ࡭ࡨࡵࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠩཋ").format(str(e)))
          for driver in bstack11l1l1l1l1_opy_:
            bstack1lllll1l111_opy_.append({
              bstack111ll_opy_ (u"ࠪࡲࡦࡳࡥࠨཌ"): bstack1l1l1lll1_opy_[bstack111ll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧཌྷ")],
              bstack111ll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫཎ"): str(e),
              bstack111ll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬཏ"): multiprocessing.current_process().name
            })
            bstack11ll1l1l1_opy_(driver, bstack111ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧཐ"), bstack111ll_opy_ (u"ࠣࡕࡨࡷࡸ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦད") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack11l1l1l1l1_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1l11111ll1_opy_, CONFIG, logger)
      bstack1llll11111_opy_()
      bstack1l11lllll_opy_()
      percy.bstack11111ll11_opy_()
      bstack11l1111ll1_opy_ = {
        bstack111ll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬདྷ"): args[0],
        bstack111ll_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪན"): CONFIG,
        bstack111ll_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬཔ"): bstack11111l1111_opy_,
        bstack111ll_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧཕ"): bstack1l11111ll1_opy_
      }
      if bstack111ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩབ") in CONFIG:
        bstack1lll111111_opy_ = bstack11lll1lll1_opy_(args, logger, CONFIG, BROWSERSTACK_AUTOMATION, bstack1ll11ll1ll_opy_)
        bstack1ll11l1l1l_opy_ = bstack1lll111111_opy_.bstack11ll1111l1_opy_(run_on_browserstack, bstack11l1111ll1_opy_, bstack11llll111_opy_(args))
      else:
        if bstack11llll111_opy_(args):
          bstack1ll1l1l1l1_opy_ = multiprocessing.get_context(bstack111ll_opy_ (u"ࠧࡴࡲࡤࡻࡳ࠭བྷ"))
          bstack11l1111ll1_opy_[bstack111ll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫམ")] = args
          test = bstack1ll1l1l1l1_opy_.Process(name=str(0),
                                target=run_on_browserstack, args=(bstack11l1111ll1_opy_,))
          test.start()
          test.join()
        else:
          bstack1l11ll1ll_opy_(bstack1l1111111_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack111ll_opy_ (u"ࠩࡢࡣࡳࡧ࡭ࡦࡡࡢࠫཙ")] = bstack111ll_opy_ (u"ࠪࡣࡤࡳࡡࡪࡰࡢࡣࠬཚ")
          mod_globals[bstack111ll_opy_ (u"ࠫࡤࡥࡦࡪ࡮ࡨࡣࡤ࠭ཛ")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1l1ll11ll_opy_ == bstack111ll_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫཛྷ") or bstack1l1ll11ll_opy_ == bstack111ll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬཝ"):
    percy.init(bstack1l11111ll1_opy_, CONFIG, logger)
    percy.bstack11111ll11_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack11l11ll1l1_opy_(e, bstack1l1llll1l_opy_)
    bstack1llll11111_opy_()
    if bstack1lllllll1l_opy_:
      os.environ[bstack111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡄࡆࡈࡄ࡙ࡑ࡚࡟ࡍࡑࡆࡅࡑࡥࡉࡅࠩཞ")] = bstack1lllllll1l_opy_
    bstack1l11ll1ll_opy_(bstack111l111l11_opy_)
    if BROWSERSTACK_AUTOMATION:
      bstack1lllll1ll1l_opy_(bstack111l111l11_opy_, args)
      if bstack111ll_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ཟ") in args:
        i = args.index(bstack111ll_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧའ"))
        args.pop(i)
        args.pop(i)
      if bstack111ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ཡ") not in CONFIG:
        CONFIG[bstack111ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧར")] = [{}]
        bstack1ll11ll1ll_opy_ = 1
      if bstack1ll11llll1_opy_ == 0:
        bstack1ll11llll1_opy_ = 1
      args.insert(0, str(bstack1ll11llll1_opy_))
      args.insert(0, str(bstack111ll_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪལ")))
    if TestHubHandler.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack11llll1l_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1lll1ll1_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack111ll_opy_ (u"ࠨࡒࡐࡄࡒࡘࡤࡕࡐࡕࡋࡒࡒࡘࠨཤ"),
        ).parse_args(bstack11llll1l_opy_)
        bstack11l1lll1_opy_ = args.index(bstack11llll1l_opy_[0]) if len(bstack11llll1l_opy_) > 0 else len(args)
        args.insert(bstack11l1lll1_opy_, str(bstack111ll_opy_ (u"ࠧ࠮࠯࡯࡭ࡸࡺࡥ࡯ࡧࡵࠫཥ")))
        args.insert(bstack11l1lll1_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack111ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡴࡲࡦࡴࡺ࡟࡭࡫ࡶࡸࡪࡴࡥࡳ࠰ࡳࡽࠬས"))))
        if bstack1ll11l1l_opy_.bstack1111l11ll1_opy_(CONFIG):
          args.insert(bstack11l1lll1_opy_, str(bstack111ll_opy_ (u"ࠩ࠰࠱ࡱ࡯ࡳࡵࡧࡱࡩࡷ࠭ཧ")))
          args.insert(bstack11l1lll1_opy_ + 1, str(bstack111ll_opy_ (u"ࠪࡖࡪࡺࡲࡺࡈࡤ࡭ࡱ࡫ࡤ࠻ࡽࢀࠫཨ").format(bstack1ll11l1l_opy_.bstack111l1l11l_opy_(CONFIG))))
        if bstack1lllll11ll1_opy_(os.environ.get(bstack111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠩཀྵ"))) and str(os.environ.get(bstack111ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠩཪ"), bstack111ll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫཫ"))) != bstack111ll_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬཬ"):
          for bstack1l1ll11l1l_opy_ in bstack1lll1ll1_opy_:
            args.remove(bstack1l1ll11l1l_opy_)
          test_files = os.environ.get(bstack111ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࡥࡔࡆࡕࡗࡗࠬ཭")).split(bstack111ll_opy_ (u"ࠩ࠯ࠫ཮"))
          for bstack1lllll1l1l_opy_ in test_files:
            args.append(bstack1lllll1l1l_opy_)
      except Exception as e:
        logger.error(bstack111ll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡣࡷࡸࡦࡩࡨࡪࡰࡪࠤࡱ࡯ࡳࡵࡧࡱࡩࡷࠦࡦࡰࡴࠣࡿࢂ࠴ࠠࡆࡴࡵࡳࡷࠦ࠭ࠡࡽࢀࠦ཯").format(bstack1ll1ll1l1l_opy_, e))
    pabot.main(args)
  elif bstack1l1ll11ll_opy_ == bstack111ll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ཰"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack11l11ll1l1_opy_(e, bstack1l1llll1l_opy_)
    for a in args:
      if bstack111ll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡕࡒࡁࡕࡈࡒࡖࡒࡏࡎࡅࡇཱ࡛ࠫ") in a:
        PLATFORM_INDEX = int(a.split(bstack111ll_opy_ (u"࠭࠺ࠨི"))[1])
      if bstack111ll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡄࡆࡈࡏࡓࡈࡇࡌࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕཱིࠫ") in a:
        bstack1lllllll1l_opy_ = str(a.split(bstack111ll_opy_ (u"ࠨ࠼ུࠪ"))[1])
      if bstack111ll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡅࡏࡍࡆࡘࡇࡔཱུࠩ") in a:
        bstack1l1l1llll_opy_ = str(a.split(bstack111ll_opy_ (u"ࠪ࠾ࠬྲྀ"))[1])
    if os.environ.get(bstack111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡈࡊࡌࡁࡖࡎࡗࡣࡑࡕࡃࡂࡎࡢࡍࡉ࠭ཷ")):
      bstack1lllllll1l_opy_ = os.environ.get(bstack111ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡉࡋࡆࡂࡗࡏࡘࡤࡒࡏࡄࡃࡏࡣࡎࡊࠧླྀ"))
    if bstack1lllllll1l_opy_:
      if bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪཹ") not in CONFIG:
        CONFIG[bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶེࠫ")] = {}
      CONFIG[bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷཻࠬ")][bstack111ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵོࠫ")] = bstack1lllllll1l_opy_
    bstack111111l1l1_opy_ = None
    bstack1l1ll111l1_opy_ = None
    if bstack111ll_opy_ (u"ࠪ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹཽࠩ") in args:
      i = args.index(bstack111ll_opy_ (u"ࠫ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠪཾ"))
      args.pop(i)
      bstack111111l1l1_opy_ = args.pop(i)
    if bstack111ll_opy_ (u"ࠬ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸࠨཿ") in args:
      i = args.index(bstack111ll_opy_ (u"࠭࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹྀࠩ"))
      args.pop(i)
      bstack1l1ll111l1_opy_ = args.pop(i)
    if bstack111111l1l1_opy_ is not None:
      global bstack11l11ll111_opy_
      bstack11l11ll111_opy_ = bstack111111l1l1_opy_
    if bstack1l1ll111l1_opy_ is not None and int(PLATFORM_INDEX) < 0:
      PLATFORM_INDEX = int(bstack1l1ll111l1_opy_)
    if cli.is_enabled(CONFIG):
      if cli.bstack11lll11ll1_opy_():
        bstack11ll1l11_opy_.invoke(Events.CONNECT, bstack1ll11l1l11_opy_())
        cli.bstack11ll11111_opy_(PLATFORM_INDEX)
      if cli.bstack11llll1lll_opy_(bstack1l111l11_opy_):
        cli.bstack11111l1lll_opy_()
    bstack1l11ll1ll_opy_(bstack111l111l11_opy_)
    run_cli(args)
    if bstack111ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷཱྀࠫ") in multiprocessing.current_process().__dict__.keys():
      for bstack1lll1l1lll_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1lllll1l111_opy_.append(bstack1lll1l1lll_opy_)
  elif bstack1l1ll11ll_opy_ == bstack111ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨྂ"):
    if os.environ.get(bstack111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡇࡉࡤࡖࡌࡖࡉࡌࡒࡤࡓࡏࡅࡇࠪྃ")):
      os.environ[bstack111ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏ྄ࠬ")] = bstack1l11lll11l_opy_
      os.environ[bstack111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠪ྅")] = json.dumps(CONFIG)
      os.environ[bstack111ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡍ࡛ࡂࡠࡗࡕࡐࠬ྆")] = bstack1lllll1l1ll_opy_()
      os.environ[bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ྇")] = str(bstack1l11111ll1_opy_)
      os.environ[bstack111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡍࡗࡊࡍࡓ࠭ྈ")] = str(True)
      os.environ[bstack111ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨྉ")] = str(max(PLATFORM_INDEX, 0))
      if CONFIG.get(bstack111ll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫྊ")):
        os.environ[bstack111ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫྋ")] = CONFIG[bstack111ll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ྌ")]
      if CONFIG.get(bstack111ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨྍ")):
        os.environ[bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩྎ")] = CONFIG[bstack111ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪྏ")]
      return
    else:
      bstack11ll1ll111_opy_ = bstack11l11111l_opy_(args, logger, CONFIG, BROWSERSTACK_AUTOMATION)
      bstack11ll1ll111_opy_.bstack1ll111l111_opy_()
      bstack1llll11111_opy_()
      PARALLELISE_THREADING_PYTHON = True
      bstack1l11ll11_opy_ = bstack11ll1ll111_opy_.bstack1l11l1l11l_opy_()
      bstack11ll1ll111_opy_.bstack11l1111ll1_opy_(bstack1ll111l1l_opy_)
      bstack11ll1ll111_opy_.bstack1l1l1l111l_opy_()
      bstack111l1ll11l_opy_(bstack1l1ll11ll_opy_, CONFIG, bstack11ll1ll111_opy_.bstack1lllllllll1_opy_())
      bstack11ll1l1l_opy_.end(EVENTS.bstack11l1l1ll11_opy_.value, EVENTS.bstack11l1l1ll11_opy_.value + bstack111ll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣྐ"), EVENTS.bstack11l1l1ll11_opy_.value + bstack111ll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢྑ"), status=True, failure=None, test_name=SESSION_NAME)
      bstack11lll111_opy_ = bstack11ll1ll111_opy_.bstack11ll1111l1_opy_(bstack1l111ll1l1_opy_, {
        bstack111ll_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪྒ"): CONFIG,
        bstack111ll_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬྒྷ"): bstack11111l1111_opy_,
        bstack111ll_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧྔ"): bstack1l11111ll1_opy_,
        bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩྕ"): BROWSERSTACK_AUTOMATION,
        bstack111ll_opy_ (u"ࠧࡐࡘࡈࡖࡗࡏࡄࡆࡡࡏࡓࡆࡊ࡟ࡕࡇࡖࡘࡎࡔࡇࠨྖ"): bstack111111lll_opy_
      })
      if not bstack1l1l1lll1_opy_:
        bstack11lll11111_opy_ = bstack111l1l1l_opy_.bstack1ll1111l1_opy_(EVENTS.bstack1ll1llllll_opy_.value)
      try:
        bstack11l1l1l11_opy_, bstack11l1l1lll_opy_ = map(list, zip(*bstack11lll111_opy_))
        bstack1111l1111l_opy_ = bstack11l1l1l11_opy_[0]
        for status_code in bstack11l1l1lll_opy_:
          if status_code != 0:
            bstack11llll1l1l_opy_ = status_code
            break
      except Exception as e:
        logger.debug(bstack111ll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡧࡶࡦࠢࡨࡶࡷࡵࡲࡴࠢࡤࡲࡩࠦࡳࡵࡣࡷࡹࡸࠦࡣࡰࡦࡨ࠲ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࠼ࠣࡿࢂࠨྗ").format(str(e)))
  elif bstack1l1ll11ll_opy_ == bstack111ll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ྘"):
    try:
      from behave.__main__ import main as bstack111l1ll1l_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack11l11ll1l1_opy_(e, bstack11111l1l1l_opy_)
    bstack1llll11111_opy_()
    PARALLELISE_THREADING_PYTHON = True
    bstack1lll11l11l_opy_ = 1
    if bstack111ll_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪྙ") in CONFIG:
      bstack1lll11l11l_opy_ = CONFIG[bstack111ll_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫྚ")]
    if bstack111ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨྛ") in CONFIG:
      bstack1l11l1l1ll_opy_ = int(bstack1lll11l11l_opy_) * int(len(CONFIG[bstack111ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩྜ")]))
    else:
      bstack1l11l1l1ll_opy_ = int(bstack1lll11l11l_opy_)
    config = Configuration(args)
    bstack1llll1l1l1_opy_ = config.paths
    if len(bstack1llll1l1l1_opy_) == 0:
      import glob
      pattern = bstack111ll_opy_ (u"ࠧࠫࠬ࠲࠮࠳࡬ࡥࡢࡶࡸࡶࡪ࠭ྜྷ")
      bstack11l1ll1l11_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack11l1ll1l11_opy_)
      config = Configuration(args)
      bstack1llll1l1l1_opy_ = config.paths
    bstack1lll1l111_opy_ = [os.path.normpath(item) for item in bstack1llll1l1l1_opy_]
    bstack1ll1l1l1l_opy_ = [os.path.normpath(item) for item in args]
    bstack1l1111l11_opy_ = [item for item in bstack1ll1l1l1l_opy_ if item not in bstack1lll1l111_opy_]
    import platform as pf
    if pf.system().lower() == bstack111ll_opy_ (u"ࠨࡹ࡬ࡲࡩࡵࡷࡴࠩྞ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1lll1l111_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1lllll1llll_opy_)))
                    for bstack1lllll1llll_opy_ in bstack1lll1l111_opy_]
    try:
      bstack1lll1lll11_opy_ = bstack1ll1l111l1_opy_(args, logger, CONFIG, BROWSERSTACK_AUTOMATION)
      bstack1lll1lll11_opy_.bstack111ll1lll_opy_(bstack1lll1l111_opy_)
      bstack1lll1lll11_opy_.bstack1l1l1l111l_opy_()
      bstack1lll1l111_opy_ = bstack1lll1lll11_opy_.bstack11ll1111ll_opy_()
    except Exception as e:
      logger.error(bstack111ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡧࡰࡱ࡮ࡼࠤࡹ࡫ࡳࡵࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡩࡳࡷࠦࡢࡦࡪࡤࡺࡪࡀࠠࠦࡵࠥྟ"), e, exc_info=True)
      logger.info(bstack111ll_opy_ (u"ࠥࡇࡴࡴࡴࡪࡰࡸ࡭ࡳ࡭ࠠࡸ࡫ࡷ࡬ࠥࡵࡲࡪࡩ࡬ࡲࡦࡲࠠࡴࡲࡨࡧࠥ࡬ࡩ࡭ࡧࡶࠤࡼ࡯ࡴࡩࡱࡸࡸࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠧྠ"))
    bstack1lllllll111_opy_ = []
    for spec in bstack1lll1l111_opy_:
      bstack1111ll1ll_opy_ = []
      bstack1111ll1ll_opy_ += bstack1l1111l11_opy_
      bstack1111ll1ll_opy_.append(spec)
      bstack1lllllll111_opy_.append(bstack1111ll1ll_opy_)
    execution_items = []
    for bstack1111ll1ll_opy_ in bstack1lllllll111_opy_:
      if bstack111ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧྡ") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack111ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨྡྷ")]):
          item = {}
          item[bstack111ll_opy_ (u"࠭ࡡࡳࡩࠪྣ")] = bstack111ll_opy_ (u"ࠧࠡࠩྤ").join(bstack1111ll1ll_opy_)
          item[bstack111ll_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧྥ")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack111ll_opy_ (u"ࠩࡤࡶ࡬࠭ྦ")] = bstack111ll_opy_ (u"ࠪࠤࠬྦྷ").join(bstack1111ll1ll_opy_)
        item[bstack111ll_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪྨ")] = 0
        execution_items.append(item)
    bstack1l111l1l_opy_ = bstack1l1l1ll11_opy_(execution_items, bstack1l11l1l1ll_opy_)
    for execution_item in bstack1l111l1l_opy_:
      bstack111111l11l_opy_ = []
      for item in execution_item:
        bstack111111l11l_opy_.append(bstack1ll1111lll_opy_(name=str(item[bstack111ll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫྩ")]),
                                             target=bstack111l11l1ll_opy_,
                                             args=(item[bstack111ll_opy_ (u"࠭ࡡࡳࡩࠪྪ")],)))
      for t in bstack111111l11l_opy_:
        t.start()
      for t in bstack111111l11l_opy_:
        t.join()
  else:
    bstack1ll11l111_opy_(bstack11l11lll1_opy_)
  if not bstack1l1l1lll1_opy_:
    bstack1111l11l_opy_()
    if bstack11lll11111_opy_:
      bstack111l1l1l_opy_.end(EVENTS.bstack1ll1llllll_opy_.value, bstack11lll11111_opy_ + bstack111ll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢྫ"), bstack11lll11111_opy_ + bstack111ll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨྫྷ"), status=True, failure=None, test_name=None)
  logger_utils.bstack11l1l1ll1_opy_()
def browserstack_initialize(bstack1l111111l1_opy_=None):
  logger.info(bstack111ll_opy_ (u"ࠩࡕࡹࡳࡴࡩ࡯ࡩࠣࡗࡉࡑࠠࡸ࡫ࡷ࡬ࠥࡧࡲࡨࡵ࠽ࠤࠬྭ") + str(bstack1l111111l1_opy_))
  run_on_browserstack(bstack1l111111l1_opy_, None, True)
@measure(event_name=EVENTS.bstack1ll11l1ll_opy_, stage=STAGE.bstack1l1l11l1l_opy_, bstack1111l11lll_opy_=SESSION_NAME)
def bstack1111l11l_opy_():
  global CONFIG
  global bstack1l11lll11l_opy_
  global bstack11llll1l1l_opy_
  global bstack111ll1l11_opy_
  global global_config
  global _11ll1llll_opy_
  bstack1l11111ll_opy_.bstack11111ll1ll_opy_()
  _11ll1llll_opy_ = cli.is_running()
  if _11ll1llll_opy_:
    bstack11ll1l11_opy_.invoke(Events.bstack1l111lll11_opy_)
  else:
    bstack111llll111_opy_ = bstack1ll11l1l_opy_.bstack1l1l11ll1_opy_(config=CONFIG)
    bstack111llll111_opy_.bstack1l1lllll_opy_(CONFIG)
  hashed_id = None
  bstack1llll1ll1_opy_ = None
  def bstack1llll1lll_opy_():
    try:
      if bstack1l11lll11l_opy_ == bstack111ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪྮ"):
        if not cli.is_enabled(CONFIG):
          TestHubHandler.stop()
      else:
        TestHubHandler.stop()
    except Exception as e:
      logger.debug(bstack111ll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡷࡹࡵࡰࡱ࡫ࡱ࡫࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࡼࡿࠥྯ").format(e))
  def bstack111l1l11l1_opy_():
    try:
      if not cli.is_enabled(CONFIG):
        bstack111ll111_opy_.bstack1111lll11l_opy_()
        bstack111ll111_opy_.bstack111lll1ll1_opy_(CONFIG)
    except Exception as e:
      logger.debug(bstack111ll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡵࡸࡩ࡯ࡶ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࠥࡲࡩ࡯࡭࠽ࠤࢀࢃࠢྰ").format(e))
  def bstack111111ll_opy_():
    nonlocal hashed_id, bstack1llll1ll1_opy_
    try:
      if bstack111ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪྱ") in CONFIG and str(CONFIG[bstack111ll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫྲ")]).lower() != bstack111ll_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧླ"):
        hashed_id, bstack1llll1ll1_opy_ = bstack11l1lll1ll_opy_()
      else:
        hashed_id, bstack1llll1ll1_opy_ = get_build_link()
    except Exception as e:
      logger.debug(bstack111ll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡥࡹ࡮ࡲࡤࠡ࡮࡬ࡲࡰࡀࠠࡼࡿࠥྴ").format(e))
  bstack11l11l111_opy_ = threading.Thread(target=bstack1llll1lll_opy_)
  bstack1lllllll1ll_opy_ = threading.Thread(target=bstack111l1l11l1_opy_)
  bstack111l11ll11_opy_ = threading.Thread(target=bstack111111ll_opy_)
  threads = [bstack11l11l111_opy_, bstack1lllllll1ll_opy_, bstack111l11ll11_opy_]
  for thread in threads:
    try:
      thread.start()
    except Exception as e:
      logger.debug(bstack111ll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡶࡸࡦࡸࡴࡪࡰࡪࠤࡹ࡮ࡲࡦࡣࡧࠤࢀࢃ࠺ࠡࡽࢀࠦྵ").format(thread.name, e))
  for thread in threads:
    try:
      thread.join()
    except Exception as e:
      logger.debug(bstack111ll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡮ࡴ࡯࡮ࡪࡰࡪࠤࡹ࡮ࡲࡦࡣࡧࠤࢀࢃ࠺ࠡࡽࢀࠦྶ").format(thread.name, e))
  bstack11l11111l1_opy_(hashed_id)
  logger.info(bstack111ll_opy_ (u"࡙ࠬࡄࡌࠢࡵࡹࡳࠦࡥ࡯ࡦࡨࡨࠥ࡬࡯ࡳࠢ࡬ࡨ࠿࠭ྷ") + global_config.get_property(bstack111ll_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨྸ"), bstack111ll_opy_ (u"ࠧࠨྐྵ")) + bstack111ll_opy_ (u"ࠨ࠮ࠣࡸࡪࡹࡴࡩࡷࡥࠤ࡮ࡪ࠺ࠡࠩྺ") + os.getenv(bstack111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧྻ"), bstack111ll_opy_ (u"ࠪࠫྼ")))
  if hashed_id is not None and bstack1ll11ll1_opy_() != -1:
    sessions = bstack111l11lll_opy_(hashed_id)
    bstack1111ll11l_opy_(sessions, bstack1llll1ll1_opy_)
  if bstack1l11lll11l_opy_ == bstack111ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ྽") and bstack11llll1l1l_opy_ != 0:
    sys.exit(bstack11llll1l1l_opy_)
  if bstack1l11lll11l_opy_ == bstack111ll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ྾") and bstack111ll1l11_opy_ != 0:
    sys.exit(bstack111ll1l11_opy_)
def bstack11l11111l1_opy_(new_id):
    global bstack11llll1111_opy_
    bstack11llll1111_opy_ = new_id
def bstack1111l1l1_opy_(bstack11l11l1ll_opy_):
  if bstack11l11l1ll_opy_:
    return bstack11l11l1ll_opy_.capitalize()
  else:
    return bstack111ll_opy_ (u"࠭ࠧ྿")
@measure(event_name=EVENTS.bstack1llllll11_opy_, stage=STAGE.bstack1l1l11l1l_opy_, bstack1111l11lll_opy_=SESSION_NAME)
def bstack1111ll11l1_opy_(bstack111lll111l_opy_):
  if bstack111ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ࿀") in bstack111lll111l_opy_ and bstack111lll111l_opy_[bstack111ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭࿁")] != bstack111ll_opy_ (u"ࠩࠪ࿂"):
    return bstack111lll111l_opy_[bstack111ll_opy_ (u"ࠪࡲࡦࡳࡥࠨ࿃")]
  else:
    bstack1111l11lll_opy_ = bstack111ll_opy_ (u"ࠦࠧ࿄")
    if bstack111ll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬ࿅") in bstack111lll111l_opy_ and bstack111lll111l_opy_[bstack111ll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࿆࠭")] != None:
      bstack1111l11lll_opy_ += bstack111lll111l_opy_[bstack111ll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ࿇")] + bstack111ll_opy_ (u"ࠣ࠮ࠣࠦ࿈")
      if bstack111lll111l_opy_[bstack111ll_opy_ (u"ࠩࡲࡷࠬ࿉")] == bstack111ll_opy_ (u"ࠥ࡭ࡴࡹࠢ࿊"):
        bstack1111l11lll_opy_ += bstack111ll_opy_ (u"ࠦ࡮ࡕࡓࠡࠤ࿋")
      bstack1111l11lll_opy_ += (bstack111lll111l_opy_[bstack111ll_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ࿌")] or bstack111ll_opy_ (u"࠭ࠧ࿍"))
      return bstack1111l11lll_opy_
    else:
      bstack1111l11lll_opy_ += bstack1111l1l1_opy_(bstack111lll111l_opy_[bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ࿎")]) + bstack111ll_opy_ (u"ࠣࠢࠥ࿏") + (
              bstack111lll111l_opy_[bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫ࿐")] or bstack111ll_opy_ (u"ࠪࠫ࿑")) + bstack111ll_opy_ (u"ࠦ࠱ࠦࠢ࿒")
      if bstack111lll111l_opy_[bstack111ll_opy_ (u"ࠬࡵࡳࠨ࿓")] == bstack111ll_opy_ (u"ࠨࡗࡪࡰࡧࡳࡼࡹࠢ࿔"):
        bstack1111l11lll_opy_ += bstack111ll_opy_ (u"ࠢࡘ࡫ࡱࠤࠧ࿕")
      bstack1111l11lll_opy_ += bstack111lll111l_opy_[bstack111ll_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ࿖")] or bstack111ll_opy_ (u"ࠩࠪ࿗")
      return bstack1111l11lll_opy_
@measure(event_name=EVENTS.bstack1l1lll1lll_opy_, stage=STAGE.bstack1l1l11l1l_opy_, bstack1111l11lll_opy_=SESSION_NAME)
def bstack111llll1ll_opy_(bstack1l1111ll1_opy_):
  if bstack1l1111ll1_opy_ == bstack111ll_opy_ (u"ࠥࡨࡴࡴࡥࠣ࿘"):
    return bstack111ll_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡧࡳࡧࡨࡲࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡧࡳࡧࡨࡲࠧࡄࡃࡰ࡯ࡳࡰࡪࡺࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ࿙")
  elif bstack1l1111ll1_opy_ == bstack111ll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ࿚"):
    return bstack111ll_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡴࡨࡨࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡲࡦࡦࠥࡂࡋࡧࡩ࡭ࡧࡧࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩ࿛")
  elif bstack1l1111ll1_opy_ == bstack111ll_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ࿜"):
    return bstack111ll_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽࡫ࡷ࡫ࡥ࡯࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥ࡫ࡷ࡫ࡥ࡯ࠤࡁࡔࡦࡹࡳࡦࡦ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨ࿝")
  elif bstack1l1111ll1_opy_ == bstack111ll_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣ࿞"):
    return bstack111ll_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡸࡥࡥ࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡶࡪࡪࠢ࠿ࡇࡵࡶࡴࡸ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ࿟")
  elif bstack1l1111ll1_opy_ == bstack111ll_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࠧ࿠"):
    return bstack111ll_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࠤࡧࡨࡥ࠸࠸࠶࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࠦࡩࡪࡧ࠳࠳࠸ࠥࡂ࡙࡯࡭ࡦࡱࡸࡸࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪ࿡")
  elif bstack1l1111ll1_opy_ == bstack111ll_opy_ (u"ࠨࡲࡶࡰࡱ࡭ࡳ࡭ࠢ࿢"):
    return bstack111ll_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡥࡰࡦࡩ࡫࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡥࡰࡦࡩ࡫ࠣࡀࡕࡹࡳࡴࡩ࡯ࡩ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨ࿣")
  else:
    return bstack111ll_opy_ (u"ࠨ࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡧࡲࡡࡤ࡭࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡧࡲࡡࡤ࡭ࠥࡂࠬ࿤") + bstack1111l1l1_opy_(
      bstack1l1111ll1_opy_) + bstack111ll_opy_ (u"ࠩ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨ࿥")
def bstack1ll111111_opy_(session):
  return bstack111ll_opy_ (u"ࠪࡀࡹࡸࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡳࡱࡺࠦࡃࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠠࡴࡧࡶࡷ࡮ࡵ࡮࠮ࡰࡤࡱࡪࠨ࠾࠽ࡣࠣ࡬ࡷ࡫ࡦ࠾ࠤࡾࢁࠧࠦࡴࡢࡴࡪࡩࡹࡃࠢࡠࡤ࡯ࡥࡳࡱࠢ࠿ࡽࢀࡀ࠴ࡧ࠾࠽࠱ࡷࡨࡃࢁࡽࡼࡿ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁ࠵ࡴࡳࡀࠪ࿦").format(
    session[bstack111ll_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦࡣࡺࡸ࡬ࠨ࿧")], bstack1111ll11l1_opy_(session), bstack111llll1ll_opy_(session[bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡸࡺࡡࡵࡷࡶࠫ࿨")]),
    bstack111llll1ll_opy_(session[bstack111ll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭࿩")]),
    bstack1111l1l1_opy_(session[bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ࿪")] or session[bstack111ll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨ࿫")] or bstack111ll_opy_ (u"ࠩࠪ࿬")) + bstack111ll_opy_ (u"ࠥࠤࠧ࿭") + (session[bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭࿮")] or bstack111ll_opy_ (u"ࠬ࠭࿯")),
    session[bstack111ll_opy_ (u"࠭࡯ࡴࠩ࿰")] + bstack111ll_opy_ (u"ࠢࠡࠤ࿱") + session[bstack111ll_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ࿲")], session[bstack111ll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫ࿳")] or bstack111ll_opy_ (u"ࠪࠫ࿴"),
    session[bstack111ll_opy_ (u"ࠫࡨࡸࡥࡢࡶࡨࡨࡤࡧࡴࠨ࿵")] if session[bstack111ll_opy_ (u"ࠬࡩࡲࡦࡣࡷࡩࡩࡥࡡࡵࠩ࿶")] else bstack111ll_opy_ (u"࠭ࠧ࿷"))
@measure(event_name=EVENTS.bstack111llll1l1_opy_, stage=STAGE.bstack1l1l11l1l_opy_, bstack1111l11lll_opy_=SESSION_NAME)
def bstack1111ll11l_opy_(sessions, bstack1llll1ll1_opy_):
  try:
    bstack1ll1lll111_opy_ = bstack111ll_opy_ (u"ࠢࠣ࿸")
    if not os.path.exists(bstack1l11lll11_opy_):
      os.mkdir(bstack1l11lll11_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack111ll_opy_ (u"ࠨࡣࡶࡷࡪࡺࡳ࠰ࡴࡨࡴࡴࡸࡴ࠯ࡪࡷࡱࡱ࠭࿹")), bstack111ll_opy_ (u"ࠩࡵࠫ࿺")) as f:
      bstack1ll1lll111_opy_ = f.read()
    bstack1ll1lll111_opy_ = bstack1ll1lll111_opy_.replace(bstack111ll_opy_ (u"ࠪࡿࠪࡘࡅࡔࡗࡏࡘࡘࡥࡃࡐࡗࡑࡘࠪࢃࠧ࿻"), str(len(sessions)))
    bstack1ll1lll111_opy_ = bstack1ll1lll111_opy_.replace(bstack111ll_opy_ (u"ࠫࢀࠫࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠧࢀࠫ࿼"), bstack1llll1ll1_opy_)
    bstack1ll1lll111_opy_ = bstack1ll1lll111_opy_.replace(bstack111ll_opy_ (u"ࠬࢁࠥࡃࡗࡌࡐࡉࡥࡎࡂࡏࡈࠩࢂ࠭࿽"),
                                              sessions[0].get(bstack111ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡴࡡ࡮ࡧࠪ࿾")) if sessions[0] else bstack111ll_opy_ (u"ࠧࠨ࿿"))
    with open(os.path.join(bstack1l11lll11_opy_, bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡳࡧࡳࡳࡷࡺ࠮ࡩࡶࡰࡰࠬက")), bstack111ll_opy_ (u"ࠩࡺࠫခ")) as stream:
      stream.write(bstack1ll1lll111_opy_.split(bstack111ll_opy_ (u"ࠪࡿ࡙ࠪࡅࡔࡕࡌࡓࡓ࡙࡟ࡅࡃࡗࡅࠪࢃࠧဂ"))[0])
      for session in sessions:
        stream.write(bstack1ll111111_opy_(session))
      stream.write(bstack1ll1lll111_opy_.split(bstack111ll_opy_ (u"ࠫࢀࠫࡓࡆࡕࡖࡍࡔࡔࡓࡠࡆࡄࡘࡆࠫࡽࠨဃ"))[1])
    logger.info(bstack111ll_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡫ࡤࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡣࡷ࡬ࡰࡩࠦࡡࡳࡶ࡬ࡪࡦࡩࡴࡴࠢࡤࡸࠥࢁࡽࠨင").format(bstack1l11lll11_opy_));
  except Exception as e:
    logger.debug(bstack111ll11lll_opy_.format(str(e)))
def bstack111l11lll_opy_(hashed_id):
  global CONFIG
  try:
    bstack1l11111lll_opy_ = datetime.datetime.now()
    host = bstack111ll_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡲ࡬࠱ࡨࡲ࡯ࡶࡦ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭စ") if bstack111ll_opy_ (u"ࠧࡢࡲࡳࠫဆ") in CONFIG else bstack111ll_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩဇ")
    user = CONFIG[bstack111ll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫဈ")]
    key = CONFIG[bstack111ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ဉ")]
    bstack111l1lll1l_opy_ = bstack111ll_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪည") if bstack111ll_opy_ (u"ࠬࡧࡰࡱࠩဋ") in CONFIG else (bstack111ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪဌ") if CONFIG.get(bstack111ll_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫဍ")) else bstack111ll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪဎ"))
    host = bstack11l1llll1l_opy_(cli.config, [bstack111ll_opy_ (u"ࠤࡤࡴ࡮ࡹࠢဏ"), bstack111ll_opy_ (u"ࠥࡥࡵࡶࡁࡶࡶࡲࡱࡦࡺࡥࠣတ"), bstack111ll_opy_ (u"ࠦࡦࡶࡩࠣထ")], host) if bstack111ll_opy_ (u"ࠬࡧࡰࡱࠩဒ") in CONFIG else bstack11l1llll1l_opy_(cli.config, [bstack111ll_opy_ (u"ࠨࡡࡱ࡫ࡶࠦဓ"), bstack111ll_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡦࠤန"), bstack111ll_opy_ (u"ࠣࡣࡳ࡭ࠧပ")], host)
    url = bstack111ll_opy_ (u"ࠩࡾࢁ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀ࠳ࡸ࡫ࡳࡴ࡫ࡲࡲࡸ࠴ࡪࡴࡱࡱࠫဖ").format(host, bstack111l1lll1l_opy_, hashed_id)
    headers = {
      bstack111ll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩဗ"): bstack111ll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧဘ"),
    }
    proxies = bstack1l1111111l_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies, auth=(user, key))
    if response.json():
      cli.bstack1ll11111l_opy_(bstack111ll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࡫ࡪࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࡡ࡯࡭ࡸࡺࠢမ"), datetime.datetime.now() - bstack1l11111lll_opy_)
      return list(map(lambda session: session[bstack111ll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࠫယ")], response.json()))
  except Exception as e:
    logger.debug(bstack111l1111l_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack1lll1l1ll_opy_, stage=STAGE.bstack1l1l11l1l_opy_, bstack1111l11lll_opy_=SESSION_NAME)
def get_build_link():
  global CONFIG
  global bstack11llll1111_opy_
  try:
    if bstack111ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪရ") in CONFIG:
      bstack1l11111lll_opy_ = datetime.datetime.now()
      host = bstack111ll_opy_ (u"ࠨࡣࡳ࡭࠲ࡩ࡬ࡰࡷࡧࠫလ") if bstack111ll_opy_ (u"ࠩࡤࡴࡵ࠭ဝ") in CONFIG else bstack111ll_opy_ (u"ࠪࡥࡵ࡯ࠧသ")
      user = CONFIG[bstack111ll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ဟ")]
      key = CONFIG[bstack111ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨဠ")]
      bstack111l1lll1l_opy_ = bstack111ll_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬအ") if bstack111ll_opy_ (u"ࠧࡢࡲࡳࠫဢ") in CONFIG else bstack111ll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪဣ")
      url = bstack111ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡾࢁ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀ࠳ࡧࡻࡩ࡭ࡦࡶ࠲࡯ࡹ࡯࡯ࠩဤ").format(user, key, host, bstack111l1lll1l_opy_)
      if cli.is_enabled(CONFIG):
        bstack1llll1ll1_opy_, hashed_id = cli.bstack11ll1111l_opy_()
        logger.info(bstack1l1ll1l111_opy_.format(bstack1llll1ll1_opy_))
        return [hashed_id, bstack1llll1ll1_opy_]
      else:
        headers = {
          bstack111ll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩဥ"): bstack111ll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧဦ"),
        }
        if bstack111ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧဧ") in CONFIG:
          params = {bstack111ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫဨ"): CONFIG[bstack111ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪဩ")], bstack111ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫဪ"): CONFIG[bstack111ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫါ")]}
        else:
          params = {bstack111ll_opy_ (u"ࠪࡲࡦࡳࡥࠨာ"): CONFIG[bstack111ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧိ")]}
        proxies = bstack1l1111111l_opy_(CONFIG, url)
        response = requests.get(url, params=params, headers=headers, proxies=proxies)
        if response.json():
          bstack1111l11l1_opy_ = response.json()[0][bstack111ll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡥࡹ࡮ࡲࡤࠨီ")]
          if bstack1111l11l1_opy_:
            bstack1llll1ll1_opy_ = bstack1111l11l1_opy_[bstack111ll_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨࡥࡵࡳ࡮ࠪု")].split(bstack111ll_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࠭ࡣࡷ࡬ࡰࡩ࠭ူ"))[0] + bstack111ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡳ࠰ࠩေ") + bstack1111l11l1_opy_[
              bstack111ll_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬဲ")]
            logger.info(bstack1l1ll1l111_opy_.format(bstack1llll1ll1_opy_))
            bstack11llll1111_opy_ = bstack1111l11l1_opy_[bstack111ll_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ဳ")]
            bstack11l1lll111_opy_ = CONFIG[bstack111ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧဴ")]
            if bstack111ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧဵ") in CONFIG:
              bstack11l1lll111_opy_ += bstack111ll_opy_ (u"࠭ࠠࠨံ") + CONFIG[bstack111ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳ့ࠩ")]
            if bstack11l1lll111_opy_ != bstack1111l11l1_opy_[bstack111ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭း")]:
              logger.debug(bstack1lll11ll1l_opy_.format(bstack1111l11l1_opy_[bstack111ll_opy_ (u"ࠩࡱࡥࡲ࡫္ࠧ")], bstack11l1lll111_opy_))
            cli.bstack1ll11111l_opy_(bstack111ll_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻ࡩࡨࡸࡤࡨࡵࡪ࡮ࡧࡣࡱ࡯࡮࡬ࠤ်"), datetime.datetime.now() - bstack1l11111lll_opy_)
            return [bstack1111l11l1_opy_[bstack111ll_opy_ (u"ࠫ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧျ")], bstack1llll1ll1_opy_]
    else:
      logger.warning(bstack11l1lllll1_opy_)
  except Exception as e:
    logger.debug(bstack11l1l111l1_opy_.format(str(e)))
  return [None, None]
def bstack1ll1l11l11_opy_(url, bstack11l1l1ll1l_opy_=False):
  global CONFIG
  global bstack11l1l1111l_opy_
  if not bstack11l1l1111l_opy_:
    hostname = bstack111ll11ll_opy_(url)
    is_private = bstack11llll11_opy_(hostname)
    if (bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩြ") in CONFIG and not bstack1lllll11ll1_opy_(CONFIG[bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪွ")])) and (is_private or bstack11l1l1ll1l_opy_):
      bstack11l1l1111l_opy_ = hostname
def bstack111ll11ll_opy_(url):
  return urlparse(url).hostname
def bstack11llll11_opy_(hostname):
  for bstack11l11ll11_opy_ in bstack11l111l11l_opy_:
    regex = re.compile(bstack11l11ll11_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1l111l1ll1_opy_(bstack1111l1lll1_opy_):
  return True if bstack1111l1lll1_opy_ in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack11l11ll1ll_opy_, stage=STAGE.bstack1l1l11l1l_opy_, bstack1111l11lll_opy_=SESSION_NAME)
def getAccessibilityResults(driver):
  global CONFIG
  global PLATFORM_INDEX
  bstack1lll11l1l1_opy_ = not (bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫှ"), None) and bstack1ll11l1ll1_opy_(
          threading.current_thread(), bstack111ll_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧဿ"), None))
  bstack1l1ll1l1_opy_ = getattr(driver, bstack111ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩ၀"), None) != True
  bstack1llllll111l_opy_ = bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ၁"), None) and bstack1ll11l1ll1_opy_(
          threading.current_thread(), bstack111ll_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭၂"), None)
  if bstack1llllll111l_opy_:
    if not bstack1l11l111_opy_():
      logger.warning(bstack111ll_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡰࡱࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡅࡵࡶࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳ࠯ࠤ၃"))
      return {}
    logger.debug(bstack111ll_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪ၄"))
    logger.debug(perform_scan(driver, driver_command=bstack111ll_opy_ (u"ࠧࡦࡺࡨࡧࡺࡺࡥࡔࡥࡵ࡭ࡵࡺࠧ၅")))
    results = bstack1l1ll11l1_opy_(bstack111ll_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࡴࠤ၆"))
    if results is not None and results.get(bstack111ll_opy_ (u"ࠤ࡬ࡷࡸࡻࡥࡴࠤ၇")) is not None:
        return results[bstack111ll_opy_ (u"ࠥ࡭ࡸࡹࡵࡦࡵࠥ၈")]
    logger.error(bstack111ll_opy_ (u"ࠦࡓࡵࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡓࡧࡶࡹࡱࡺࡳࠡࡹࡨࡶࡪࠦࡦࡰࡷࡱࡨ࠳ࠨ၉"))
    return []
  if not a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX) or (bstack1l1ll1l1_opy_ and bstack1lll11l1l1_opy_):
    logger.warning(bstack111ll_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹ࠮ࠣ၊"))
    return {}
  try:
    logger.debug(bstack111ll_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪ။"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(accessibility_scripts.get_results)
    return results
  except Exception:
    logger.error(bstack111ll_opy_ (u"ࠢࡏࡱࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡼ࡫ࡲࡦࠢࡩࡳࡺࡴࡤ࠯ࠤ၌"))
    return {}
@measure(event_name=EVENTS.bstack1llllll1ll_opy_, stage=STAGE.bstack1l1l11l1l_opy_, bstack1111l11lll_opy_=SESSION_NAME)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global PLATFORM_INDEX
  bstack1lll11l1l1_opy_ = not (bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬ၍"), None) and bstack1ll11l1ll1_opy_(
          threading.current_thread(), bstack111ll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ၎"), None))
  bstack1l1ll1l1_opy_ = getattr(driver, bstack111ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪ၏"), None) != True
  bstack1llllll111l_opy_ = bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫၐ"), None) and bstack1ll11l1ll1_opy_(
          threading.current_thread(), bstack111ll_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧၑ"), None)
  if bstack1llllll111l_opy_:
    if not bstack1l11l111_opy_():
      logger.warning(bstack111ll_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡆࡶࡰࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡶࡹࡲࡳࡡࡳࡻ࠱ࠦၒ"))
      return {}
    logger.debug(bstack111ll_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡸࡻ࡭࡮ࡣࡵࡽࠬၓ"))
    logger.debug(perform_scan(driver, driver_command=bstack111ll_opy_ (u"ࠨࡧࡻࡩࡨࡻࡴࡦࡕࡦࡶ࡮ࡶࡴࠨၔ")))
    results = bstack1l1ll11l1_opy_(bstack111ll_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡕࡸࡱࡲࡧࡲࡺࠤၕ"))
    if results is not None and results.get(bstack111ll_opy_ (u"ࠥࡷࡺࡳ࡭ࡢࡴࡼࠦၖ")) is not None:
        return results[bstack111ll_opy_ (u"ࠦࡸࡻ࡭࡮ࡣࡵࡽࠧၗ")]
    logger.error(bstack111ll_opy_ (u"ࠧࡔ࡯ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡔࡨࡷࡺࡲࡴࡴࠢࡖࡹࡲࡳࡡࡳࡻࠣࡻࡦࡹࠠࡧࡱࡸࡲࡩ࠴ࠢၘ"))
    return {}
  if not a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX) or (bstack1l1ll1l1_opy_ and bstack1lll11l1l1_opy_):
    logger.warning(bstack111ll_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡵࡸࡱࡲࡧࡲࡺ࠰ࠥၙ"))
    return {}
  try:
    logger.debug(bstack111ll_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡸࡻ࡭࡮ࡣࡵࡽࠬၚ"))
    logger.debug(perform_scan(driver))
    bstack1ll11l1111_opy_ = driver.execute_async_script(accessibility_scripts.get_results_summary)
    return bstack1ll11l1111_opy_
  except Exception:
    logger.error(bstack111ll_opy_ (u"ࠣࡐࡲࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸࡻ࡭࡮ࡣࡵࡽࠥࡽࡡࡴࠢࡩࡳࡺࡴࡤ࠯ࠤၛ"))
    return {}
def bstack1l11l111_opy_():
  global CONFIG
  global PLATFORM_INDEX
  bstack111ll1ll1l_opy_ = bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩၜ"), None) and bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬၝ"), None)
  if not a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX) or not bstack111ll1ll1l_opy_:
        logger.warning(bstack111ll_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡶࡰࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡵࡩࡸࡻ࡬ࡵࡵ࠱ࠦၞ"))
        return False
  return True
def bstack1l1ll11l1_opy_(result_type):
    bstack1lllllllll_opy_ = TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack111ll111_opy_.current_hook_uuid()
    with ThreadPoolExecutor() as executor:
        future = executor.submit(bstack1l1l111l1l_opy_(bstack1lllllllll_opy_, result_type))
        try:
            return future.result(timeout=bstack1l1l11lll_opy_)
        except TimeoutError:
            logger.error(bstack111ll_opy_ (u"࡚ࠧࡩ࡮ࡧࡲࡹࡹࠦࡡࡧࡶࡨࡶࠥࢁࡽࡴࠢࡺ࡬࡮ࡲࡥࠡࡨࡨࡸࡨ࡮ࡩ࡯ࡩࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡖࡪࡹࡵ࡭ࡶࡶࠦၟ").format(bstack1l1l11lll_opy_))
        except Exception as ex:
            logger.debug(bstack111ll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡸࡥࡵࡴ࡬ࡩࡻ࡯࡮ࡨࠢࡄࡴࡵࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡿࢂ࠴ࠠࡆࡴࡵࡳࡷࠦ࠭ࠡࡽࢀࠦၠ").format(result_type, str(ex)))
    return {}
@measure(event_name=EVENTS.bstack1lll1ll1ll_opy_, stage=STAGE.bstack1l1l11l1l_opy_, bstack1111l11lll_opy_=SESSION_NAME)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global PLATFORM_INDEX
  bstack1lll11l1l1_opy_ = not (bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫၡ"), None) and bstack1ll11l1ll1_opy_(
          threading.current_thread(), bstack111ll_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧၢ"), None))
  bstack1llll111_opy_ = not (bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩၣ"), None) and bstack1ll11l1ll1_opy_(
          threading.current_thread(), bstack111ll_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬၤ"), None))
  bstack1l1ll1l1_opy_ = getattr(driver, bstack111ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫၥ"), None) != True
  if not a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX) or (bstack1l1ll1l1_opy_ and bstack1lll11l1l1_opy_ and bstack1llll111_opy_):
    logger.warning(bstack111ll_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷࡻ࡮ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳ࠴ࠢၦ"))
    return {}
  try:
    bstack111l111l1_opy_ = bstack111ll_opy_ (u"࠭ࡡࡱࡲࠪၧ") in CONFIG and CONFIG.get(bstack111ll_opy_ (u"ࠧࡢࡲࡳࠫၨ"), bstack111ll_opy_ (u"ࠨࠩၩ"))
    session_id = getattr(driver, bstack111ll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩ࠭ၪ"), None)
    if not session_id:
      logger.warning(bstack111ll_opy_ (u"ࠥࡒࡴࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡊࡆࠣࡪࡴࡻ࡮ࡥࠢࡩࡳࡷࠦࡤࡳ࡫ࡹࡩࡷࠨၫ"))
      return {bstack111ll_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥၬ"): bstack111ll_opy_ (u"ࠧࡔ࡯ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡌࡈࠥ࡬࡯ࡶࡰࡧࠦၭ")}
    if bstack111l111l1_opy_:
      try:
        bstack11ll1lllll_opy_ = {
              bstack111ll_opy_ (u"࠭ࡴࡩࡌࡺࡸ࡙ࡵ࡫ࡦࡰࠪၮ"): os.environ.get(bstack111ll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬၯ"), os.environ.get(bstack111ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬၰ"), bstack111ll_opy_ (u"ࠩࠪၱ"))),
              bstack111ll_opy_ (u"ࠪࡸ࡭࡚ࡥࡴࡶࡕࡹࡳ࡛ࡵࡪࡦࠪၲ"): TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack111ll111_opy_.current_hook_uuid(),
              bstack111ll_opy_ (u"ࠫࡦࡻࡴࡩࡊࡨࡥࡩ࡫ࡲࠨၳ"): os.environ.get(bstack111ll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪၴ")),
              bstack111ll_opy_ (u"࠭ࡳࡤࡣࡱࡘ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ၵ"): str(int(datetime.datetime.now().timestamp() * 1000)),
              bstack111ll_opy_ (u"ࠧࡵࡪࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬၶ"): os.environ.get(bstack111ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ၷ"), bstack111ll_opy_ (u"ࠩࠪၸ")),
              bstack111ll_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࠪၹ"): kwargs.get(bstack111ll_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࡣࡨࡵ࡭࡮ࡣࡱࡨࠬၺ"), None) or bstack111ll_opy_ (u"ࠬ࠭ၻ")
          }
        if not hasattr(thread_local, bstack111ll_opy_ (u"࠭ࡢࡢࡵࡨࡣࡦࡶࡰࡠࡣ࠴࠵ࡾࡥࡳࡤࡴ࡬ࡴࡹ࠭ၼ")):
            scripts = {bstack111ll_opy_ (u"ࠧࡴࡥࡤࡲࠬၽ"): accessibility_scripts.perform_scan}
            thread_local.base_app_a11y_script = scripts
        bstack11ll1ll1l_opy_ = copy.deepcopy(thread_local.base_app_a11y_script)
        bstack11ll1ll1l_opy_[bstack111ll_opy_ (u"ࠨࡵࡦࡥࡳ࠭ၾ")] = bstack11ll1ll1l_opy_[bstack111ll_opy_ (u"ࠩࡶࡧࡦࡴࠧၿ")] % json.dumps(bstack11ll1lllll_opy_)
        accessibility_scripts.bstack11ll111l11_opy_(bstack11ll1ll1l_opy_)
        accessibility_scripts.store()
        bstack1llllll1l11_opy_ = driver.execute_script(accessibility_scripts.perform_scan)
      except Exception as bstack11ll1ll11_opy_:
        logger.info(bstack111ll_opy_ (u"ࠥࡅࡵࡶࡩࡶ࡯ࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࠥႀ") + str(bstack11ll1ll11_opy_))
        bstack1llllll1l11_opy_ = {bstack111ll_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥႁ"): str(bstack11ll1ll11_opy_)}
    else:
      bstack1llllll1l11_opy_ = driver.execute_async_script(accessibility_scripts.perform_scan, {bstack111ll_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬႂ"): kwargs.get(bstack111ll_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡣࡰ࡯ࡰࡥࡳࡪࠧႃ"), None) or bstack111ll_opy_ (u"ࠧࠨႄ")})
    return bstack1llllll1l11_opy_
  except Exception as err:
    logger.error(bstack111ll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡷࡻ࡮ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳ࠴ࠠࡼࡿࠥႅ").format(str(err)))
    return {}
def bstack1lll11111l_opy_(bstack1l1l1l1lll_opy_):
  bstack111ll_opy_ (u"ࠤࠥࠦࡎࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥࠡࡶ࡫ࡩ࡙ࠥࡄࡌࠢࡩࡳࡷࠦࡉࡅࡇ࠰ࡲࡦࡺࡩࡷࡧࠣࡴࡾࡺࡥࡴࡶࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࠨࡑࡻࡆ࡬ࡦࡸ࡭ࠪ࠰ࠍࠤࠥࡌࡡ࡬ࡧࡶࠤࡸࡿࡳ࠯ࡣࡵ࡫ࡻࠦࡴࡰࠢ࡯ࡳࡴࡱࠠ࡭࡫࡮ࡩࠥࡧࠠࡄࡎࡌࠤࡼࡸࡡࡱࡲࡨࡶࠥ࡯࡮ࡷࡱࡦࡥࡹ࡯࡯࡯࠮ࠣࡸ࡭࡫࡮ࠡࡥࡤࡰࡱࡹࠊࠡࠢࡵࡹࡳࡥ࡯࡯ࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠩࠫࠣࡷࡴࠦࡴࡩࡧࠣࡉ࡝ࡇࡃࡕࠢࡶࡥࡲ࡫ࠠࡤࡱࡧࡩࠥࡶࡡࡵࡪࠣࡶࡺࡴࡳ࠯ࠢࡗ࡬ࡪࠦ࡯࡯࡮ࡼࠎࠥࠦࡤࡪࡨࡩࡩࡷ࡫࡮ࡤࡧ࠽ࠤࡕࡿࡴࡦࡵࡷࡌࡦࡴࡤ࡭ࡧࡵ࠲ࡸࡺࡡࡳࡶࡢࡸࡪࡹࡴࡴࠪࠬࠤ࡮ࡹࠠ࡯ࡱࡷࠤࡨࡧ࡬࡭ࡧࡧࠤࡧ࡫ࡣࡢࡷࡶࡩࠏࠦࠠࡱࡻࡷࡩࡸࡺࠠࡪࡵࠣࡥࡱࡸࡥࡢࡦࡼࠤࡷࡻ࡮࡯࡫ࡱ࡫࠳ࠐࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࡣࡰࡰࡩ࡭࡬ࡥࡰࡢࡶ࡫࠾ࠥࡇࡢࡴࡱ࡯ࡹࡹ࡫ࠠࡱࡣࡷ࡬ࠥࡺ࡯ࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠤࡴࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹࡢ࡯࡯࠲ࠏࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࡖࡵࡹࡪࠦࡩࡧࠢ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠣࡷࡺࡩࡣࡦࡧࡧࡩࡩ࠲ࠠࡇࡣ࡯ࡷࡪࠦ࡯ࡵࡪࡨࡶࡼ࡯ࡳࡦ࠰ࠍࠤࠥࠨࠢࠣႆ")
  try:
    try:
      import selenium
      cli.session_framework = bstack111ll_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧႇ")
    except ImportError:
      try:
        import playwright
        cli.session_framework = bstack111ll_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣႈ")
      except ImportError:
        pass
    bstack1l1111l1ll_opy_ = sys.argv[:]
    sys.argv = [bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡸࡪ࡫ࠨႉ"), bstack111ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ႊ")]
    os.environ[bstack111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡅࡇࡢࡔࡑ࡛ࡇࡊࡐࡢࡑࡔࡊࡅࠨႋ")] = bstack111ll_opy_ (u"ࠨ࠳ࠪႌ")
    os.environ[bstack111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࡠࡈࡌࡐࡊႍ࠭")] = bstack1l1l1l1lll_opy_
    try:
      run_on_browserstack()
    finally:
      sys.argv = bstack1l1111l1ll_opy_
    return cli.is_running()
  except Exception as e:
    logger.error(bstack111ll_opy_ (u"ࠥࡍࡉࡋ࠭࡯ࡣࡷ࡭ࡻ࡫ࠠࡱ࡮ࡸ࡫࡮ࡴࠠࡪࡰ࡬ࡸࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡾࠤႎ").format(str(e)))
    logger.debug(traceback.format_exc())
    return False