# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
import os
if bstack1l1llll_opy_ (u"࠭ࡇࡓࡒࡆࡣ࡛ࡋࡒࡃࡑࡖࡍ࡙࡟ࠧൗ") not in os.environ:
    os.environ[bstack1l1llll_opy_ (u"ࠧࡈࡔࡓࡇࡤ࡜ࡅࡓࡄࡒࡗࡎ࡚࡙ࠨ൘")] = bstack1l1llll_opy_ (u"ࠨࡇࡕࡖࡔࡘࠧ൙")
import atexit
import hashlib
import shlex
import signal
try:
  from filelock import FileLock, Timeout as bstack1ll11l1l1ll_opy_
except ImportError:
  FileLock = None
  class bstack1ll11l1l1ll_opy_(Exception):
    pass
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
import tempfile
import inspect
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import json
from browserstack_sdk.sdk_cli.module_event_dispatcher import EventDispatcherModule
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from browserstack_sdk.bstack11l11ll1l_opy_ import bstack11l11ll11_opy_
from browserstack_sdk.bstack1ll11lll_opy_ import *
import time
import requests
from bstack_utils.constants import EVENTS, STAGE, bstack1ll1111ll11_opy_
from bstack_utils.messages import bstack11111l11l1_opy_, bstack1ll1l1111l1_opy_, bstack11lll1111l_opy_, bstack1111llll1l_opy_, bstack1l1ll1ll111_opy_, bstack1lll1l11l1_opy_
from bstack_utils.measure import measure
from bstack_utils.logger_utils import get_logger
from bstack_utils.helper import bstack1ll11l111l1_opy_
from bstack_utils.helper import get_ca_cert_path
from browserstack_sdk.bstack1l111lll1_opy_ import bstack1l111llll_opy_
logger = get_logger(__name__)
def bstack1l1ll11111l_opy_():
  global CONFIG
  headers = {
        bstack1l1llll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨ൚"): bstack1l1llll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭൛"),
      }
  proxies = bstack1ll11l111l1_opy_(CONFIG, bstack1ll1111ll11_opy_)
  from browserstack_sdk import CONFIG as _1111l1l11l_opy_
  bstack1l1l1111ll_opy_ = {bstack1l1llll_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬ൜"): headers, bstack1l1llll_opy_ (u"ࠬࡶࡲࡰࡺ࡬ࡩࡸ࠭൝"): proxies, bstack1l1llll_opy_ (u"࠭ࡴࡪ࡯ࡨࡳࡺࡺࠧ൞"): 2}
  cert_path = get_ca_cert_path(_1111l1l11l_opy_)
  if cert_path:
    bstack1l1l1111ll_opy_[bstack1l1llll_opy_ (u"ࠧࡷࡧࡵ࡭࡫ࡿࠧൟ")] = cert_path
  try:
    response = requests.get(bstack1ll1111ll11_opy_, **bstack1l1l1111ll_opy_)
    if response.json():
      bstack1llll11llll_opy_ = response.json()[bstack1l1llll_opy_ (u"ࠨࡪࡸࡦࡸ࠭ൠ")]
      logger.debug(bstack11111l11l1_opy_.format(response.json()))
      return bstack1llll11llll_opy_
    else:
      logger.debug(bstack1ll1l1111l1_opy_.format(bstack1l1llll_opy_ (u"ࠤࡕࡩࡸࡶ࡯࡯ࡵࡨࠤࡏ࡙ࡏࡏࠢࡳࡥࡷࡹࡥࠡࡧࡵࡶࡴࡸࠠࠣൡ")))
  except Exception as e:
    logger.debug(bstack1ll1l1111l1_opy_.format(e))
def bstack1l1l1ll1ll_opy_(hub_url):
  global CONFIG
  url = bstack1l1llll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧൢ")+  hub_url + bstack1l1llll_opy_ (u"ࠦ࠴ࡩࡨࡦࡥ࡮ࠦൣ")
  headers = {
        bstack1l1llll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫ൤"): bstack1l1llll_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ൥"),
      }
  proxies = bstack1ll11l111l1_opy_(CONFIG, url)
  from browserstack_sdk import CONFIG as _1111l1l11l_opy_
  bstack1l1l1l11lll_opy_ = {bstack1l1llll_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨ൦"): headers, bstack1l1llll_opy_ (u"ࠨࡲࡵࡳࡽ࡯ࡥࡴࠩ൧"): proxies, bstack1l1llll_opy_ (u"ࠩࡷ࡭ࡲ࡫࡯ࡶࡶࠪ൨"): (0.5, 1.0)}
  cert_path = get_ca_cert_path(_1111l1l11l_opy_)
  if cert_path:
    bstack1l1l1l11lll_opy_[bstack1l1llll_opy_ (u"ࠪࡺࡪࡸࡩࡧࡻࠪ൩")] = cert_path
  try:
    start_time = time.perf_counter()
    requests.get(url, **bstack1l1l1l11lll_opy_)
    latency = (time.perf_counter() - start_time) * 1000
    logger.debug(bstack11lll1111l_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1111llll1l_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack1ll1lll1l1_opy_, stage=STAGE.SINGLE)
def bstack11111111l_opy_():
  try:
    global bstack1lll1ll1l11_opy_
    global CONFIG
    if bstack1l1llll_opy_ (u"ࠫ࡭ࡻࡢࡓࡧࡪ࡭ࡴࡴࠧ൪") in CONFIG and CONFIG[bstack1l1llll_opy_ (u"ࠬ࡮ࡵࡣࡔࡨ࡫࡮ࡵ࡮ࠨ൫")]:
      from bstack_utils.constants import bstack1l1l111111_opy_
      bstack1ll11111ll1_opy_ = CONFIG[bstack1l1llll_opy_ (u"࠭ࡨࡶࡤࡕࡩ࡬࡯࡯࡯ࠩ൬")]
      if bstack1ll11111ll1_opy_ in bstack1l1l111111_opy_:
        bstack1lll1ll1l11_opy_ = bstack1l1l111111_opy_[bstack1ll11111ll1_opy_]
        logger.debug(bstack1l1ll1ll111_opy_.format(bstack1lll1ll1l11_opy_))
        _1ll1ll1lll_opy_([], bstack1lll1ll1l11_opy_, None)
        return
      else:
        logger.debug(bstack1l1llll_opy_ (u"ࠢࡉࡷࡥࠤࡰ࡫ࡹࠡࠩࡾࢁࠬࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࡎࡕࡃࡡࡘࡖࡑࡥࡍࡂࡒ࠯ࠤ࡫ࡧ࡬࡭࡫ࡱ࡫ࠥࡨࡡࡤ࡭ࠣࡸࡴࠦ࡯ࡱࡶ࡬ࡱࡦࡲࠠࡩࡷࡥࠤࡩ࡫ࡴࡦࡥࡷ࡭ࡴࡴࠢ൭").format(bstack1ll11111ll1_opy_))
    bstack1llll11llll_opy_ = bstack1l1ll11111l_opy_()
    if not bstack1llll11llll_opy_:
      return
    from concurrent.futures import ThreadPoolExecutor, as_completed
    executor = ThreadPoolExecutor(max_workers=len(bstack1llll11llll_opy_))
    futures = {executor.submit(bstack1l1l1ll1ll_opy_, bstack1lll11l11ll_opy_): bstack1lll11l11ll_opy_ for bstack1lll11l11ll_opy_ in bstack1llll11llll_opy_}
    winner = None
    for future in as_completed(futures):
      result = future.result()
      if result and result.get(bstack1l1llll_opy_ (u"ࠨ࡮ࡤࡸࡪࡴࡣࡺࠩ൮")) is not None:
        winner = result
        bstack1lll1ll1l11_opy_ = result[bstack1l1llll_opy_ (u"ࠩ࡫ࡹࡧࡥࡵࡳ࡮ࠪ൯")]
        logger.debug(bstack1l1ll1ll111_opy_.format(bstack1lll1ll1l11_opy_))
        _1ll1ll1lll_opy_(bstack1llll11llll_opy_, result[bstack1l1llll_opy_ (u"ࠪ࡬ࡺࡨ࡟ࡶࡴ࡯ࠫ൰")], result[bstack1l1llll_opy_ (u"ࠫࡱࡧࡴࡦࡰࡦࡽࠬ൱")])
        break
    if winner is None:
      bstack1lll1ll1l11_opy_ = bstack1llll11llll_opy_[0]
      logger.debug(bstack1l1ll1ll111_opy_.format(bstack1lll1ll1l11_opy_))
      _1ll1ll1lll_opy_(bstack1llll11llll_opy_, bstack1llll11llll_opy_[0], None, fallback=True)
      try:
        executor.shutdown(wait=False)
      except Exception:
        pass
      return
    t = bstack1l111llll_opy_(target=_1ll11lll1l1_opy_, args=(executor, futures, winner))
    t.daemon = True
    t.start()
  except Exception as e:
    logger.debug(bstack1lll1l11l1_opy_.format(e))
def _1ll11lll1l1_opy_(executor, futures, winner):
  bstack1l1llll_opy_ (u"ࠧࠨࠢࡃࡣࡦ࡯࡬ࡸ࡯ࡶࡰࡧࠤࡩࡸࡡࡪࡰࠣ⠘ࠥࡩ࡯࡭࡮ࡨࡧࡹࠦࡲࡦ࡯ࡤ࡭ࡳ࡯࡮ࡨࠢ࠲ࡧ࡭࡫ࡣ࡬ࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࡷࠥࡧ࡮ࡥࠢࡸࡴࡩࡧࡴࡦࠌࠣࠤࡤ࡮ࡵࡣࡃ࡯ࡰࡴࡩࡡࡵ࡫ࡲࡲࡉࡧࡴࡢ࡝ࠪ࡬ࡺࡨࡌࡢࡶࡨࡲࡨ࡯ࡥࡴࠩࡠࠤ࡮ࡴࠠࡱ࡮ࡤࡧࡪࠦࡳࡰࠢࡈࡈࡘࠦࡳࡦࡧࡶࠤࡦࡲ࡬ࠡࡲࡵࡳࡧ࡫ࡤࠡࡪࡸࡦࡸ࠴ࠢࠣࠤ൲")
  try:
    from concurrent.futures import as_completed
    from bstack_utils.config import Config
    global_config = Config.bstack1lll1l11_opy_()
    bstack11111l111_opy_ = {}
    if winner and winner.get(bstack1l1llll_opy_ (u"࠭࡬ࡢࡶࡨࡲࡨࡿࠧ൳")) is not None:
      bstack11111l111_opy_[bstack1l1llll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤ൴") + winner[bstack1l1llll_opy_ (u"ࠨࡪࡸࡦࡤࡻࡲ࡭ࠩ൵")]] = winner[bstack1l1llll_opy_ (u"ࠩ࡯ࡥࡹ࡫࡮ࡤࡻࠪ൶")]
    for future in as_completed(futures):
      try:
        result = future.result()
      except Exception:
        continue
      if result and result.get(bstack1l1llll_opy_ (u"ࠪࡰࡦࡺࡥ࡯ࡥࡼࠫ൷")) is not None:
        bstack11111l111_opy_[bstack1l1llll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨ൸") + result[bstack1l1llll_opy_ (u"ࠬ࡮ࡵࡣࡡࡸࡶࡱ࠭൹")]] = result[bstack1l1llll_opy_ (u"࠭࡬ࡢࡶࡨࡲࡨࡿࠧൺ")]
    bstack1l1ll1l1ll1_opy_ = global_config.get_property(bstack1l1llll_opy_ (u"ࠧࡠࡪࡸࡦࡆࡲ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࡅࡣࡷࡥࠬൻ"))
    if bstack1l1ll1l1ll1_opy_ and not bstack1l1ll1l1ll1_opy_.get(bstack1l1llll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩർ")):
      bstack1l1ll1l1ll1_opy_[bstack1l1llll_opy_ (u"ࠩ࡫ࡹࡧࡒࡡࡵࡧࡱࡧ࡮࡫ࡳࠨൽ")] = bstack11111l111_opy_
      global_config.bstack1ll11l111l_opy_(bstack1l1llll_opy_ (u"ࠪࡣ࡭ࡻࡢࡂ࡮࡯ࡳࡨࡧࡴࡪࡱࡱࡈࡦࡺࡡࠨൾ"), bstack1l1ll1l1ll1_opy_)
      logger.debug(bstack1l1llll_opy_ (u"ࠦࡍࡻࡢࠡࡣ࡯ࡰࡴࡩࡡࡵ࡫ࡲࡲࠥࡪࡡࡵࡣࠣࡩࡳࡸࡩࡤࡪࡨࡨ࠿ࠦࡻࡾࠤൿ").format(bstack1l1ll1l1ll1_opy_))
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡪࡴࡲࡪࡥ࡫࡭ࡳ࡭ࠠࡩࡷࡥࠤࡱࡧࡴࡦࡰࡦ࡭ࡪࡹ࠺ࠡࡽࢀࠦ඀").format(e))
  finally:
    try:
      executor.shutdown(wait=False)
    except Exception:
      pass
def _1ll1ll1lll_opy_(bstack1llll11llll_opy_, bstack1lll1l11l11_opy_, latency, fallback=False):
  bstack1l1llll_opy_ (u"ࠨࠢࠣࡕࡷࡳࡷ࡫ࠠࡩࡷࡥࠤࡦࡲ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡳࡷࡰࡩࡳࡺࡡࡵ࡫ࡲࡲ࠳ࠦࡃࡢ࡮࡯ࡩࡩࠦࡩ࡯ࡶࡨࡶࡳࡧ࡬࡭ࡻࠣࡥ࡫ࡺࡥࡳࠢ࡫ࡹࡧࠦࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯࠰ࠍࠤࠥࡇ࡬ࡸࡣࡼࡷࠥ࡫࡭ࡪࡶࡶࠤࡹ࡮ࡥࠡࡥࡤࡲࡴࡴࡩࡤࡣ࡯ࠤࡨࡸ࡯ࡴࡵ࠰ࡗࡉࡑࠠࡴࡪࡤࡴࡪࡀࠊࠡࠢࠣࠤࢀࠦ࡮ࡦࡣࡵࡩࡸࡺࡈࡶࡤࡶ࠰ࠥ࡮ࡵࡣࡎࡤࡸࡪࡴࡣࡪࡧࡶ࠰ࠥࡹࡥ࡭ࡧࡦࡸࡪࡪࡈࡶࡤ࠯ࠤࡸ࡫࡬ࡦࡥࡷࡩࡩࡎࡵࡣࡎࡤࡸࡪࡴࡣࡺ࠮ࠣࡸ࡮ࡳࡥࡴࡶࡤࡱࡵࠦࡽࠋࠢࠣࡻ࡮ࡺࡨࠡࡱࡳࡸ࡮ࡵ࡮ࡢ࡮ࠣࡤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࡕࡴࡸࡩࡥࠦ࡭ࡢࡴ࡮ࡩࡷࠦࡷࡩࡧࡱࠤࡹ࡮ࡥࠡࡣ࡯ࡰ࠲࡬ࡡࡪ࡮ࠣࡴࡦࡺࡨࠡ࡫ࡶࠤ࡭࡯ࡴࠡࡵࡲࠤࡊࡊࡓࠋࠢࠣࡧࡦࡴࠠࡥ࡫ࡶࡸ࡮ࡴࡧࡶ࡫ࡶ࡬ࠥࠨࡲࡢࡰࠣࡥࡳࡪࠠࡢ࡮࡯ࠤ࡫ࡧࡩ࡭ࡧࡧࠦࠥ࡬ࡲࡰ࡯ࠣࠦࡩ࡯ࡤ࡯ࠩࡷࠤࡷࡻ࡮ࠣ࠰ࠍࠤࠥࠨࠢࠣඁ")
  try:
    from bstack_utils.config import Config
    global_config = Config.bstack1lll1l11_opy_()
    data = {
      bstack1l1llll_opy_ (u"ࠧ࡯ࡧࡤࡶࡪࡹࡴࡉࡷࡥࡷࠬං"): [bstack1l1llll_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥඃ") + bstack1lll11l11ll_opy_ for bstack1lll11l11ll_opy_ in bstack1llll11llll_opy_],
      bstack1l1llll_opy_ (u"ࠩ࡫ࡹࡧࡒࡡࡵࡧࡱࡧ࡮࡫ࡳࠨ඄"): {} if latency is None else {bstack1l1llll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧඅ") + bstack1lll1l11l11_opy_: latency},
      bstack1l1llll_opy_ (u"ࠫࡸ࡫࡬ࡦࡥࡷࡩࡩࡎࡵࡣࠩආ"): bstack1l1llll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢඇ") + bstack1lll1l11l11_opy_,
      bstack1l1llll_opy_ (u"࠭ࡳࡦ࡮ࡨࡧࡹ࡫ࡤࡉࡷࡥࡐࡦࡺࡥ࡯ࡥࡼࠫඈ"): latency,
      bstack1l1llll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪඉ"): int(time.time() * 1000),
    }
    if fallback:
      data[bstack1l1llll_opy_ (u"ࠨࡨࡤࡰࡱࡨࡡࡤ࡭ࠪඊ")] = True
    global_config.bstack1ll11l111l_opy_(bstack1l1llll_opy_ (u"ࠩࡢ࡬ࡺࡨࡁ࡭࡮ࡲࡧࡦࡺࡩࡰࡰࡇࡥࡹࡧࠧඋ"), data)
    logger.debug(bstack1l1llll_opy_ (u"ࠥࡌࡺࡨࠠࡢ࡮࡯ࡳࡨࡧࡴࡪࡱࡱࠤࡩࡧࡴࡢࠢࡶࡸࡴࡸࡥࡥ࠼ࠣࡿࢂࠨඌ").format(data))
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡷࡹࡵࡲࡪࡰࡪࠤ࡭ࡻࡢࠡࡣ࡯ࡰࡴࡩࡡࡵ࡫ࡲࡲࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢඍ").format(e))
from browserstack_sdk.bstack11ll11l1l_opy_ import *
from browserstack_sdk.bstack1lll11ll_opy_ import bstack1lll11l1_opy_
from browserstack_sdk.bstack1l111lll1_opy_ import *
from browserstack_sdk.bstack_behave_listener import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.logger_utils import get_logger
from bstack_utils.measure import measure
from bstack_utils.helper import get_ca_cert_path
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack1l11ll1111_opy_, stage=STAGE.SINGLE)
def bstack1ll1l111ll1_opy_():
    global bstack1lll1ll1l11_opy_
    try:
        bstack11ll111ll1_opy_ = bstack111llllll1_opy_()
        bstack1ll11111l1_opy_(bstack11ll111ll1_opy_)
        hub_url = bstack11ll111ll1_opy_.get(bstack1l1llll_opy_ (u"ࠧࡻࡲ࡭ࠤඎ"), bstack1l1llll_opy_ (u"ࠨࠢඏ"))
        if hub_url.endswith(bstack1l1llll_opy_ (u"ࠧ࠰ࡹࡧ࠳࡭ࡻࡢࠨඐ")):
            hub_url = hub_url.rsplit(bstack1l1llll_opy_ (u"ࠨ࠱ࡺࡨ࠴࡮ࡵࡣࠩඑ"), 1)[0]
        if hub_url.startswith(bstack1l1llll_opy_ (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱ࠪඒ")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack1l1llll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠬඓ")):
            hub_url = hub_url[8:]
        bstack1lll1ll1l11_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack111llllll1_opy_():
    global CONFIG
    bstack1l1l11l11l_opy_ = CONFIG.get(bstack1l1llll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࡐࡲࡷ࡭ࡴࡴࡳࠨඔ"), {}).get(bstack1l1llll_opy_ (u"ࠬ࡭ࡲࡪࡦࡑࡥࡲ࡫ࠧඕ"), bstack1l1llll_opy_ (u"࠭ࡎࡐࡡࡊࡖࡎࡊ࡟ࡏࡃࡐࡉࡤࡖࡁࡔࡕࡈࡈࠬඖ"))
    if not isinstance(bstack1l1l11l11l_opy_, str):
        raise ValueError(bstack1l1llll_opy_ (u"ࠢࡂࡖࡖࠤ࠿ࠦࡇࡳ࡫ࡧࠤࡳࡧ࡭ࡦࠢࡰࡹࡸࡺࠠࡣࡧࠣࡥࠥࡼࡡ࡭࡫ࡧࠤࡸࡺࡲࡪࡰࡪࠦ඗"))
    try:
        bstack11ll111ll1_opy_ = bstack1ll1l1ll11l_opy_(bstack1l1l11l11l_opy_)
        return bstack11ll111ll1_opy_
    except Exception as e:
        logger.error(bstack1l1llll_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡪࡩࡹࡺࡩ࡯ࡩࠣ࡫ࡷ࡯ࡤࠡࡦࡨࡸࡦ࡯࡬ࡴࠢ࠽ࠤࢀࢃࠢ඘").format(str(e)))
        return {}
def bstack1ll1l1ll11l_opy_(bstack1l1l11l11l_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack1l1llll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ඙")] or not CONFIG[bstack1l1llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ක")]:
            raise ValueError(bstack1l1llll_opy_ (u"ࠦࡒ࡯ࡳࡴ࡫ࡱ࡫ࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡺࡹࡥࡳࡰࡤࡱࡪࠦ࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴࠢ࡮ࡩࡾࠨඛ"))
        url = bstack1ll1llll11l_opy_ + bstack1l1l11l11l_opy_
        auth = (CONFIG[bstack1l1llll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧග")], CONFIG[bstack1l1llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩඝ")])
        from browserstack_sdk import CONFIG as _1111l1l11l_opy_
        bstack1ll11l1llll_opy_ = {bstack1l1llll_opy_ (u"ࠧࡢࡷࡷ࡬ࠬඞ"): auth}
        cert_path = get_ca_cert_path(_1111l1l11l_opy_)
        if cert_path:
            bstack1ll11l1llll_opy_[bstack1l1llll_opy_ (u"ࠨࡸࡨࡶ࡮࡬ࡹࠨඟ")] = cert_path
        response = requests.get(url, **bstack1ll11l1llll_opy_)
        if response.status_code == 200 and response.text:
            bstack11ll1111l1_opy_ = json.loads(response.text)
            return bstack11ll1111l1_opy_
    except ValueError as ve:
        logger.error(bstack1l1llll_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥ࡭ࡲࡪࡦࠣࡨࡪࡺࡡࡪ࡮ࡶࠤ࠿ࠦࡻࡾࠤච").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack1l1llll_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡫࡫ࡴࡤࡪ࡬ࡲ࡬ࠦࡧࡳ࡫ࡧࠤࡩ࡫ࡴࡢ࡫࡯ࡷࠥࡀࠠࡼࡿࠥඡ").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack1ll11111l1_opy_(bstack1ll11ll111l_opy_):
    global CONFIG
    if bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨජ") not in CONFIG or str(CONFIG[bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩඣ")]).lower() == bstack1l1llll_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬඤ"):
        CONFIG[bstack1l1llll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭ඥ")] = False
    elif bstack1l1llll_opy_ (u"ࠨ࡫ࡶࡘࡷ࡯ࡡ࡭ࡉࡵ࡭ࡩ࠭ඦ") in bstack1ll11ll111l_opy_:
        bstack11111l1l11_opy_ = CONFIG.get(bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ට"), {})
        logger.debug(bstack1l1llll_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡈࡼ࡮ࡹࡴࡪࡰࡪࠤࡱࡵࡣࡢ࡮ࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࠫࡳࠣඨ"), bstack11111l1l11_opy_)
        bstack1l11l11l1l_opy_ = bstack1ll11ll111l_opy_.get(bstack1l1llll_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰࡖࡪࡶࡥࡢࡶࡨࡶࡸࠨඩ"), [])
        bstack1l1ll11lll1_opy_ = bstack1l1llll_opy_ (u"ࠧ࠲ࠢඪ").join(bstack1l11l11l1l_opy_)
        logger.debug(bstack1l1llll_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡉࡵࡴࡶࡲࡱࠥࡸࡥࡱࡧࡤࡸࡪࡸࠠࡴࡶࡵ࡭ࡳ࡭࠺ࠡࠧࡶࠦණ"), bstack1l1ll11lll1_opy_)
        bstack1l1l1lll1ll_opy_ = {
            bstack1l1llll_opy_ (u"ࠢ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤඬ"): bstack1l1llll_opy_ (u"ࠣࡣࡷࡷ࠲ࡸࡥࡱࡧࡤࡸࡪࡸࠢත"),
            bstack1l1llll_opy_ (u"ࠤࡩࡳࡷࡩࡥࡍࡱࡦࡥࡱࠨථ"): bstack1l1llll_opy_ (u"ࠥࡸࡷࡻࡥࠣද"),
            bstack1l1llll_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࠱ࡷ࡫ࡰࡦࡣࡷࡩࡷࠨධ"): bstack1l1ll11lll1_opy_
        }
        bstack11111l1l11_opy_.update(bstack1l1l1lll1ll_opy_)
        logger.debug(bstack1l1llll_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤ࡚ࡶࡤࡢࡶࡨࡨࠥࡲ࡯ࡤࡣ࡯ࠤࡴࡶࡴࡪࡱࡱࡷ࠿ࠦࠥࡴࠤන"), bstack11111l1l11_opy_)
        CONFIG[bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ඲")] = bstack11111l1l11_opy_
        logger.debug(bstack1l1llll_opy_ (u"ࠢࡂࡖࡖࠤ࠿ࠦࡆࡪࡰࡤࡰࠥࡉࡏࡏࡈࡌࡋ࠿ࠦࠥࡴࠤඳ"), CONFIG)
def get_turboscale_playwright_url():
    bstack11ll111ll1_opy_ = bstack111llllll1_opy_()
    if not bstack11ll111ll1_opy_[bstack1l1llll_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࡚ࡸ࡬ࠨප")]:
      raise ValueError(bstack1l1llll_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࡛ࡲ࡭ࠢ࡬ࡷࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡦࡳࡱࡰࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵ࠱ࠦඵ"))
    return bstack11ll111ll1_opy_[bstack1l1llll_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࡕࡳ࡮ࠪබ")] + bstack1l1llll_opy_ (u"ࠫࡄࡩࡡࡱࡵࡀࠫභ")
@measure(event_name=EVENTS.bstack11l111l1ll_opy_, stage=STAGE.SINGLE)
def bstack1ll1l1l11ll_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack1l1llll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧම")], CONFIG[bstack1l1llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩඹ")])
        url = bstack1l11lll11l_opy_
        logger.debug(bstack1l1llll_opy_ (u"ࠢࡂࡶࡷࡩࡲࡶࡴࡪࡰࡪࠤࡹࡵࠠࡧࡧࡷࡧ࡭ࠦࡢࡶ࡫࡯ࡨࡸࠦࡦࡳࡱࡰࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡘࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠠࡂࡒࡌࠦය"))
        from browserstack_sdk import CONFIG as _1111l1l11l_opy_
        bstack11lll111ll_opy_ = {bstack1l1llll_opy_ (u"ࠨࡣࡸࡸ࡭࠭ර"): auth, bstack1l1llll_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪ඼"): {bstack1l1llll_opy_ (u"ࠥࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠤල"): bstack1l1llll_opy_ (u"ࠦࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠢ඾")}}
        cert_path = get_ca_cert_path(_1111l1l11l_opy_)
        if cert_path:
            bstack11lll111ll_opy_[bstack1l1llll_opy_ (u"ࠬࡼࡥࡳ࡫ࡩࡽࠬ඿")] = cert_path
        try:
            response = requests.get(url, **bstack11lll111ll_opy_)
            if response.status_code == 200:
                bstack1ll1l1l1ll1_opy_ = json.loads(response.text)
                bstack1ll1lll1l1l_opy_ = bstack1ll1l1l1ll1_opy_.get(bstack1l1llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡸ࠭ව"), [])
                if bstack1ll1lll1l1l_opy_:
                    bstack1ll1ll111l_opy_ = bstack1ll1lll1l1l_opy_[0]
                    build_hashed_id = bstack1ll1ll111l_opy_.get(bstack1l1llll_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪශ"))
                    bstack11111ll1l_opy_ = bstack1l11l1l111_opy_ + build_hashed_id
                    result.extend([build_hashed_id, bstack11111ll1l_opy_])
                    logger.info(bstack1lll1l1lll1_opy_.format(bstack11111ll1l_opy_))
                    bstack1ll1llllll1_opy_ = CONFIG[bstack1l1llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫෂ")]
                    if bstack1l1llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫස") in CONFIG:
                      bstack1ll1llllll1_opy_ += bstack1l1llll_opy_ (u"ࠪࠤࠬහ") + CONFIG[bstack1l1llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ළ")]
                    if bstack1ll1llllll1_opy_ != bstack1ll1ll111l_opy_.get(bstack1l1llll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪෆ")):
                      logger.debug(bstack111lll1lll_opy_.format(bstack1ll1ll111l_opy_.get(bstack1l1llll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ෇")), bstack1ll1llllll1_opy_))
                    return result
                else:
                    logger.debug(bstack1l1llll_opy_ (u"ࠢࡂࡖࡖࠤ࠿ࠦࡎࡰࠢࡥࡹ࡮ࡲࡤࡴࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠱ࠦ෈"))
            else:
                logger.debug(bstack1l1llll_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴ࠰ࠥ෉"))
        except Exception as e:
            logger.error(bstack1l1llll_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࡶࠤ࠿ࠦࡻࡾࠤ්").format(str(e)))
    else:
        logger.debug(bstack1l1llll_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡆࡓࡓࡌࡉࡈࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡶࡩࡹ࠴ࠠࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴ࠰ࠥ෋"))
    return [None, None]
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack111ll1l11_opy_ import bstack111ll1l11_opy_, Events, bstack1lll1ll1l1_opy_, bstack111ll11ll_opy_
from bstack_utils.measure import performance_tester
from bstack_utils.measure import measure
from bstack_utils.percy import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1lllllllll_opy_ import bstack1lll11l1l1l_opy_
from bstack_utils.messages import *
from bstack_utils import logger_utils
from bstack_utils.constants import *
from bstack_utils.helper import bstack1ll111lllll_opy_, bstack1111ll1111_opy_, bstack11l11l111l_opy_, bstack11llll11_opy_, \
  bstack111l11l11l_opy_, \
  Notset, is_robot_playwright_installed, robot_pw_binary_flow, bstack11l1ll1111_opy_, \
  bstack1ll1ll1llll_opy_, bstack11llll11l1_opy_, bstack11l11111ll_opy_, bstack11111l1lll_opy_, bstack1llll1l11l1_opy_, bstack1l1111l1ll_opy_, \
  bstack1ll1lll11l_opy_, \
  bstack111l11111_opy_, bstack1ll11ll1ll1_opy_, bstack1lll11l111_opy_, bstack1ll11l11ll1_opy_, \
  bstack11l1ll11ll_opy_, bstack1ll1l1l11l_opy_, bstack11lll11l1l_opy_, bstack1lll11l11l1_opy_, bstack1llll1l1l11_opy_
from bstack_utils.bstack1lll11111l1_opy_ import bstack11l11111l1_opy_
from bstack_utils.bstack1ll111111l1_opy_ import bstack1l1l1l1l111_opy_, bstack1lllll1lll_opy_
from bstack_utils.bstack1ll1l1lll1l_opy_ import bstack1llllllllll_opy_
from bstack_utils.bstack1l1ll1ll1_opy_ import bstack1l1lll1ll1l_opy_, bstack1lll1111l1l_opy_
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.bstack1llll11l11l_opy_ import bstack11l1ll1l1l_opy_
from bstack_utils.proxy import bstack1ll1ll1111l_opy_, bstack1ll11l111l1_opy_, bstack1l111ll111_opy_, bstack11ll1l1ll1_opy_
from bstack_utils.bstack111111l11l_opy_ import bstack1lll11l11l_opy_, bstack111l1l1ll1_opy_
import bstack_utils.bstack11llll1ll1_opy_ as TestHubUtils
import bstack_utils.bstack11l11ll111_opy_ as bstack111ll1l111_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.utils.bstack111111ll1l_opy_ import FileUploader
from bstack_utils.bstack11ll1lll1_opy_ import bstack11ll1111l_opy_
from bstack_utils.bstack1l1l1l1l1ll_opy_ import bstack1ll111l1ll1_opy_
from bstack_utils.performance_tester import PerformanceTester
if os.getenv(bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡉࡑࡒࡏࡘ࠭෌")):
  cli.bstack1lllllll1l_opy_()
else:
  os.environ[bstack1l1llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡊࡒࡓࡐ࡙ࠧ෍")] = bstack1l1llll_opy_ (u"࠭ࡴࡳࡷࡨࠫ෎")
bstack1lll1l1l1ll_opy_ = bstack1l1llll_opy_ (u"ࠧࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠠࠡ࡫ࡩࠬࡵࡧࡧࡦࠢࡀࡁࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠠࡼ࡞ࡱࠤࠥࠦࡴࡳࡻࡾࡠࡳࠦࡣࡰࡰࡶࡸࠥ࡬ࡳࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࡡ࠭ࡦࡴ࡞ࠪ࠭ࡀࡢ࡮ࠡࠢࠣࠤࠥ࡬ࡳ࠯ࡣࡳࡴࡪࡴࡤࡇ࡫࡯ࡩࡘࡿ࡮ࡤࠪࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠬࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡳࡣ࡮ࡴࡤࡦࡺࠬࠤ࠰ࠦࠢ࠻ࠤࠣ࠯ࠥࡐࡓࡐࡐ࠱ࡷࡹࡸࡩ࡯ࡩ࡬ࡪࡾ࠮ࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࠬࡦࡽࡡࡪࡶࠣࡲࡪࡽࡐࡢࡩࡨ࠶࠳࡫ࡶࡢ࡮ࡸࡥࡹ࡫ࠨࠣࠪࠬࠤࡂࡄࠠࡼࡿࠥ࠰ࠥࡢࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡨࡧࡷࡗࡪࡹࡳࡪࡱࡱࡈࡪࡺࡡࡪ࡮ࡶࠦࢂࡢࠧࠪࠫࠬ࡟ࠧ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠣ࡟ࠬࠤ࠰ࠦࠢ࠭࡞࡟ࡲࠧ࠯࡜࡯ࠢࠣࠤࠥࢃࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡽ࡝ࡰࠣࠤ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠧා")
LAUNCH_PATCH_ROBOT_PLAYWRIGHT = bstack1l1llll_opy_ (u"ࠨ࡞ࡱ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࡢ࡮ࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠻࡝ࠡ࠿ࡀࡁࠥࡢࠧࡵࡴࡸࡩࡡ࠭࡜࡯ࡥࡲࡲࡸࡺࠠࡣࡵࡷࡥࡨࡱ࡟ࡱࡣࡷ࡬ࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴࡟࡟ࡲࡨࡵ࡮ࡴࡶࠣࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࡝ࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠵ࡢࡢ࡮ࡤࡱࡱࡷࡹࠦࡰࡠ࡫ࡱࡨࡪࡾࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠵ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠵࡟ࠣࡁࡂࡃࠠ࡝ࠩࡷࡶࡺ࡫࡜ࠨ࡞ࡱࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡷࡱ࡯ࡣࡦࠪ࠳࠰ࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠵ࠪ࡞ࡱࡧࡴࡴࡳࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣࠫ࠾ࡠࡳࡩ࡯࡯ࡵࡷࠤࡴࡸࡩࡨ࡫ࡱࡥࡱࡥࡣࡩࡴࡲࡱ࡮ࡻ࡭ࡠ࡮ࡤࡹࡳࡩࡨࠡ࠿ࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡰࡦࡻ࡮ࡤࡪ࠱ࡦ࡮ࡴࡤࠩ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭ࠪ࠽࡟ࡲ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡱࡧࡵ࡯ࡥ࡫ࠤࡂࠦࡡࡴࡻࡱࡧࠥ࠮࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸ࠯ࠠ࠾ࡀࠣࡿࡡࡴࡩࡧࠢࠫࠥࡧࡹࡴࡢࡥ࡮ࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠪࠢࡾࡠࡳࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦ࡯ࡳ࡫ࡪ࡭ࡳࡧ࡬ࡠࡥ࡫ࡶࡴࡳࡩࡶ࡯ࡢࡰࡦࡻ࡮ࡤࡪࠫࡰࡦࡻ࡮ࡤࡪࡒࡴࡹ࡯࡯࡯ࡵࠬ࠿ࡡࡴࡽ࡝ࡰ࡯ࡩࡹࠦࡣࡢࡲࡶ࠿ࡡࡴࡴࡳࡻࠣࡿࡡࡴࡣࡢࡲࡶࠤࡂࠦࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠪ࡞ࡱࠤࠥࢃࠠࡤࡣࡷࡧ࡭࠮ࡥࡹࠫࠣࡿࡡࡴࠠࠡࠢࠣࢁࡡࡴࠠࠡ࡫ࡩࠤ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࠮ࠦࡻ࡝ࡰࠣࠤࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡩ࡯࡯ࡰࡨࡧࡹࡕࡶࡦࡴࡆࡈࡕ࠮ࡻ࡝ࡰࠣࠤࠥࠦࠠࠡࡧࡱࡨࡵࡵࡩ࡯ࡶࡘࡖࡑࡀࠠࡡࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠧࡿࡪࡴࡣࡰࡦࡨ࡙ࡗࡏࡃࡰ࡯ࡳࡳࡳ࡫࡮ࡵࠪࡍࡗࡔࡔ࠮ࡴࡶࡵ࡭ࡳ࡭ࡩࡧࡻࠫࡧࡦࡶࡳࠪࠫࢀࡤ࠱ࡢ࡮ࠡࠢࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴ࡞ࡱࠤࠥࠦࠠࡾࠫ࡟ࡲࠥࠦࡽ࡝ࡰࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࠻ࠢࡣࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠩࢁࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭ࢂࡦࠬ࡝ࡰࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴ࡞ࡱࠤࠥࢃࠩ࡝ࡰࢀࡠࡳࡩ࡯࡯ࡵࡷࠤࡴࡸࡩࡨ࡫ࡱࡥࡱࡥࡣࡰࡰࡱࡩࡨࡺࠠ࠾ࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱ࠮ࡤࡪࡵࡳࡲ࡯ࡵ࡮࠰ࡦࡳࡳࡴࡥࡤࡶ࠱ࡦ࡮ࡴࡤࠩ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭ࠪ࠽࡟ࡲ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡨࡵ࡮࡯ࡧࡦࡸࠥࡃࠠࡢࡵࡼࡲࡨࠦࠨࡤࡱࡱࡲࡪࡩࡴࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁ࡜࡯ࠢࠣ࡭࡫ࠦࠨࠢࡤࡶࡸࡦࡩ࡫ࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠮ࠦࡻ࡝ࡰࠣࠤࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥࡵࡲࡪࡩ࡬ࡲࡦࡲ࡟ࡤࡱࡱࡲࡪࡩࡴࠩࡥࡲࡲࡳ࡫ࡣࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠫ࠾ࡠࡳࠦࠠࡾ࡞ࡱࠤࠥࡲࡥࡵࠢࡦࡥࡵࡹ࠻࡝ࡰࠣࠤࡹࡸࡹࠡࡽ࡟ࡲࠥࠦࠠࠡࡥࡤࡴࡸࠦ࠽ࠡࡌࡖࡓࡓ࠴ࡰࡢࡴࡶࡩ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡩࡡࡱࡵࠬࡠࡳࠦࠠࡾࠢࡦࡥࡹࡩࡨࠩࡧࡻ࠭ࠥࢁ࡜࡯ࠢࠣࢁࡡࡴࠠࠡࡥࡲࡲࡸࡺࠠ࡮ࡱࡧ࡭࡫࡯ࡥࡥࡇࡱࡨࡵࡵࡩ࡯ࡶࠣࡁࠥࡦࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࡡࠢ࠮ࠤࡪࡴࡣࡰࡦࡨ࡙ࡗࡏࡃࡰ࡯ࡳࡳࡳ࡫࡮ࡵࠪࡍࡗࡔࡔ࠮ࡴࡶࡵ࡭ࡳ࡭ࡩࡧࡻࠫࡧࡦࡶࡳࠪࠫ࠾ࡠࡳࠦࠠࡪࡨࠣࠬࡧࡹࡴࡢࡥ࡮ࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ࠭ࠥࢁ࡜࡯ࠢࠣࠤࠥࡸࡥࡵࡷࡵࡲࠥࡧࡷࡢ࡫ࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡨࡵ࡮࡯ࡧࡦࡸࡔࡼࡥࡳࡅࡇࡔ࠭ࢁ࡜࡯ࠢࠣࠤࠥࠦࠠࡦࡰࡧࡴࡴ࡯࡮ࡵࡗࡕࡐ࠿ࠦ࡭ࡰࡦ࡬ࡪ࡮࡫ࡤࡆࡰࡧࡴࡴ࡯࡮ࡵ࠮࡟ࡲࠥࠦࠠࠡࠢࠣ࠲࠳࠴ࡣࡰࡰࡱࡩࡨࡺࡏࡱࡶ࡬ࡳࡳࡹ࡜࡯ࠢࠣࠤࠥࢃࠩ࡝ࡰࠣࠤࢂࡢ࡮ࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤ࠳࠴࠮ࡤࡱࡱࡲࡪࡩࡴࡐࡲࡷ࡭ࡴࡴࡳ࠭࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࡝ࡰࠣࠤࢂ࠯࡜࡯ࡿ࡟ࡲࡱ࡫ࡴࠡࡄࡵࡳࡼࡹࡥࡳࡅࡲࡲࡹ࡫ࡸࡵ࠽࡟ࡲࡹࡸࡹࠡࡽ࡟ࡲࠥࠦࡣࡰࡰࡶࡸࠥࡶࡡࡵࡪࡐࡳࡩࡻ࡬ࡦࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭ࠨࡰࡢࡶ࡫ࠦ࠮ࡁ࡜࡯ࠢࠣࡧࡴࡴࡳࡵࠢࡳࡻࡈࡵࡲࡦࡒࡤࡸ࡭ࠦ࠽ࠡࡲࡤࡸ࡭ࡓ࡯ࡥࡷ࡯ࡩ࠳ࡪࡩࡳࡰࡤࡱࡪ࠮ࡲࡦࡳࡸ࡭ࡷ࡫࠮ࡳࡧࡶࡳࡱࡼࡥࠩࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠳ࡣࡰࡴࡨ࠳ࡵࡧࡣ࡬ࡣࡪࡩ࠳ࡰࡳࡰࡰࠥ࠭࠮ࡁ࡜࡯ࠢࠣࡆࡷࡵࡷࡴࡧࡵࡇࡴࡴࡴࡦࡺࡷࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨࡱࡣࡷ࡬ࡒࡵࡤࡶ࡮ࡨ࠲࡯ࡵࡩ࡯ࠪࡳࡻࡈࡵࡲࡦࡒࡤࡸ࡭࠲ࠠࠣ࡮࡬ࡦ࠴ࡩ࡬ࡪࡧࡱࡸ࠴ࡨࡲࡰࡹࡶࡩࡷࡉ࡯࡯ࡶࡨࡼࡹࠨࠩࠪ࠰ࡅࡶࡴࡽࡳࡦࡴࡆࡳࡳࡺࡥࡹࡶ࠾ࡠࡳࢃࠠࡤࡣࡷࡧ࡭ࠦࠨࡦࠫࠣࡿࡡࡴࠠࠡࡥࡲࡲࡸࡵ࡬ࡦ࠰ࡺࡥࡷࡴࠨࠣࡅࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡱࡵࡡࡥࠢࡅࡶࡴࡽࡳࡦࡴࡆࡳࡳࡺࡥࡹࡶࠣࡪࡷࡵ࡭ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠲ࡩ࡯ࡳࡧ࠽ࠦ࠱ࠦࡥ࠯࡯ࡨࡷࡸࡧࡧࡦࠫ࠾ࡠࡳࢃ࡜࡯ࡥࡲࡲࡸࡺࠠࡰࡴ࡬࡫࡮ࡴࡡ࡭ࡡࡱࡩࡼࡖࡡࡨࡧࠣࡁࠥࡈࡲࡰࡹࡶࡩࡷࡉ࡯࡯ࡶࡨࡼࡹ࠴ࡰࡳࡱࡷࡳࡹࡿࡰࡦ࠰ࡱࡩࡼࡖࡡࡨࡧ࠾ࡠࡳࡈࡲࡰࡹࡶࡩࡷࡉ࡯࡯ࡶࡨࡼࡹ࠴ࡰࡳࡱࡷࡳࡹࡿࡰࡦ࠰ࡱࡩࡼࡖࡡࡨࡧࠣࡁࠥࡧࡳࡺࡰࡦࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠮ࠩࠡࡽ࡟ࡲࠥࠦࡩࡧࠢࠫࡦࡸࡺࡡࡤ࡭ࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠬࠤࢀࡢ࡮ࠡࠢࠣࠤࡹࡸࡹࠡࡽ࡟ࡲࠥࠦࠠࠡࠢࠣࡧࡴࡴࡳࡵࠢࡥࡶࡴࡽࡳࡦࡴࠣࡁࠥࡺࡨࡪࡵ࠱ࡦࡷࡵࡷࡴࡧࡵࠤࠫࠬࠠࡵࡪ࡬ࡷ࠳ࡨࡲࡰࡹࡶࡩࡷ࠮ࠩ࠼࡞ࡱࠤࠥࠦࠠࠡࠢ࡯ࡩࡹࠦࡰࡳ࡫ࡰࡥࡷࡿࡃࡰࡰࡷࡩࡽࡺࠠ࠾ࠢࡥࡶࡴࡽࡳࡦࡴࠣࠪࠫࠦࡴࡺࡲࡨࡳ࡫ࠦࡢࡳࡱࡺࡷࡪࡸ࠮ࡤࡱࡱࡸࡪࡾࡴࡴࠢࡀࡁࡂࠦ࡜ࠨࡨࡸࡲࡨࡺࡩࡰࡰ࡟ࠫࠥࡅࠠࡣࡴࡲࡻࡸ࡫ࡲ࠯ࡥࡲࡲࡹ࡫ࡸࡵࡵࠫ࠭ࡠ࠶࡝ࠡ࠼ࠣࡲࡺࡲ࡬࠼࡞ࡱࠤࠥࠦࠠࠡࠢ࡬ࡪࠥ࠮ࠡࡱࡴ࡬ࡱࡦࡸࡹࡄࡱࡱࡸࡪࡾࡴࠡࠨࠩࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࠬࠦࠡࡶࡼࡴࡪࡵࡦࠡࡤࡵࡳࡼࡹࡥࡳ࠰ࡱࡩࡼࡉ࡯࡯ࡶࡨࡼࡹࠦ࠽࠾࠿ࠣࡠࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡜ࠨࠫࠣࡿࡡࡴࠠࠡࠢࠣࠤࠥࠦࠠࡱࡴ࡬ࡱࡦࡸࡹࡄࡱࡱࡸࡪࡾࡴࠡ࠿ࠣࡥࡼࡧࡩࡵࠢࡥࡶࡴࡽࡳࡦࡴ࠱ࡲࡪࡽࡃࡰࡰࡷࡩࡽࡺࠨࠪ࠽࡟ࡲࠥࠦࠠࠡࠢࠣࢁࡡࡴࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡵࡷࠤࡹࡧࡲࡨࡧࡷࡇࡴࡴࡴࡦࡺࡷࠤࡂࠦࡰࡳ࡫ࡰࡥࡷࡿࡃࡰࡰࡷࡩࡽࡺࠠࡽࡾࠣࡸ࡭࡯ࡳ࠼࡞ࡱࠤࠥࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡲࡪࡽࡐࡢࡩࡨ࠲ࡨࡧ࡬࡭ࠪࡷࡥࡷ࡭ࡥࡵࡅࡲࡲࡹ࡫ࡸࡵࠫ࠾ࡠࡳࠦࠠࠡࠢࢀࠤࡨࡧࡴࡤࡪࠣࠬࡪ࠯ࠠࡼ࡞ࡱࠤࠥࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡲࡪࡽࡐࡢࡩࡨ࠲ࡨࡧ࡬࡭ࠪࡷ࡬࡮ࡹࠩ࠼࡞ࡱࠤࠥࠦࠠࡾ࡞ࡱࠤࠥࢃࠠ࡝ࡰࠣࠤࡪࡲࡳࡦࠢࡾࡠࡳࠦࠠࠡࠢࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣࡳࡷ࡯ࡧࡪࡰࡤࡰࡤࡴࡥࡸࡒࡤ࡫ࡪ࠴ࡣࡢ࡮࡯ࠬࡹ࡮ࡩࡴࠫ࠾ࡠࡳࠦࠠࡾ࡞ࡱࢁࡀࡢ࡮࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱࡟ࡲࠬැ")
from ._version import __version__
bstack1l11llll11_opy_ = None
CONFIG = {}
bstack1111ll111_opy_ = {}
bstack1ll111lll1_opy_ = {}
bstack11llll1l11_opy_ = None
bstack1l1lllll1l_opy_ = None
SESSION_NAME = None
PLATFORM_INDEX = -1
bstack1111111l1_opy_ = 0
bstack1l1111l111_opy_ = bstack111l11l111_opy_
bstack1l1lll1lll_opy_ = 1
PARALLELISE_VANILLA_PYTHON = False
PARALLELISE_THREADING_PYTHON = False
FRAMEWORK_NAME = bstack1l1llll_opy_ (u"ࠩࠪෑ")
bstack1ll1ll111ll_opy_ = bstack1l1llll_opy_ (u"ࠪࠫි")
bstack11ll111lll_opy_ = False
BROWSERSTACK_AUTOMATION = True
bstack1l11l11l11_opy_ = False
bstack1l1ll1lll1l_opy_ = bstack1l1llll_opy_ (u"ࠫࠬී")
bstack11l1l11111_opy_ = []
bstack1111ll11l_opy_ = []
bstack1l1111ll1l_opy_ = threading.Lock()
bstack1111lll1ll_opy_ = threading.Lock()
_PLAYWRIGHT_ACTIVE_THREADS_LOCK = threading.Lock()
_PLAYWRIGHT_ACTIVE_THREADS = set()
bstack1l1ll1ll1l1_opy_ = None
bstack1lll1ll1l11_opy_ = bstack1l1llll_opy_ (u"ࠬ࠭ු")
SELENIUM_OR_PLAYWRIGHT_INSTALLED = False
bstack1ll1l11l111_opy_ = None
bstack1111lll111_opy_ = None
bstack1l1l1l11l1_opy_ = None
bstack1llll11111l_opy_ = -1
bstack111lll11ll_opy_ = os.path.join(os.path.expanduser(bstack1l1llll_opy_ (u"࠭ࡾࠨ෕")), bstack1l1llll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧූ"), bstack1l1llll_opy_ (u"ࠨ࠰ࡵࡳࡧࡵࡴ࠮ࡴࡨࡴࡴࡸࡴ࠮ࡪࡨࡰࡵ࡫ࡲ࠯࡬ࡶࡳࡳ࠭෗"))
bstack1111l1l111_opy_ = 0
bstack1l1l1l11l1l_opy_ = 0
bstack1llllll11ll_opy_ = []
bstack1lll1llll1_opy_ = []
ROBOT_PYTHON_ERRORS = []
bstack1ll111l11ll_opy_ = []
bstack1lll1l11l1l_opy_ = bstack1l1llll_opy_ (u"ࠩࠪෘ")
bstack1lll11l111l_opy_ = bstack1l1llll_opy_ (u"ࠪࠫෙ")
bstack11l11l1l1l_opy_ = False
bstack1ll11l1lll_opy_ = False
bstack1ll1ll11111_opy_ = {}
bstack1l11l1111l_opy_ = {}
_BSTACK_INIT_FAILURE_SENTINEL = bstack1l1llll_opy_ (u"ࠦࡤࡨࡳࡵࡣࡦ࡯ࡤ࡯࡮ࡪࡶࡢࡪࡦ࡯࡬ࡶࡴࡨࡣࡼࡸࡡࡱࡲࡨࡨࠧේ")
def _install_driver_init_failure_capture():
  try:
    from selenium import webdriver as _1l1lll1llll_opy_
    from bstack_utils.helper import instrument_driver_init_failure_event
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶ࠲࡯࡮ࡪࡶࠣࡧࡦࡶࡴࡶࡴࡨࠤࡼࡸࡡࡱࡲࡨࡶࠥࡴ࡯ࡵࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨ࠿ࠦࡻࡾࠤෛ").format(e))
    return
  try:
    _current = _1l1lll1llll_opy_.Remote.__init__
    if getattr(_current, _BSTACK_INIT_FAILURE_SENTINEL, False):
      return
    def _1l1lll1l1ll_opy_(self, *args, **kwargs):
      try:
        _current(self, *args, **kwargs)
      except Exception as e:
        try:
          instrument_driver_init_failure_event(e, bstack1l1llll_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣො"))
        except Exception as bstack1l11ll1lll_opy_:
          logger.debug(bstack1l1llll_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡧࡶ࡮ࡼࡥࡳ࠯࡬ࡲ࡮ࡺࠠࡤࡣࡳࡸࡺࡸࡥࠡࡵࡨࡲࡩࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࡼࡿࠥෝ").format(bstack1l11ll1lll_opy_))
        raise
    setattr(_1l1lll1l1ll_opy_, _BSTACK_INIT_FAILURE_SENTINEL, True)
    _1l1lll1llll_opy_.Remote.__init__ = _1l1lll1l1ll_opy_
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠮࡫ࡱ࡭ࡹࠦࡣࡢࡲࡷࡹࡷ࡫ࠠࡸࡴࡤࡴࡵ࡫ࡲࠡࡰࡲࡸࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤ࠻ࠢࡾࢁࠧෞ").format(e))
def _install_playwright_init_failure_capture():
  try:
    import asyncio as _1lll1111ll_opy_
    from playwright._impl._browser_type import BrowserType
    from bstack_utils.helper import instrument_driver_init_failure_event
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦ࡮ࡰࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡤࡦࡱ࡫ࠬࠡࡵ࡮࡭ࡵࡶࡩ࡯ࡩࠣ࡭ࡳ࡯ࡴࠡࡥࡤࡴࡹࡻࡲࡦ࠼ࠣࡿࢂࠨෟ").format(e))
    return
  try:
    for _1111111ll_opy_ in (bstack1l1llll_opy_ (u"ࠪࡧࡴࡴ࡮ࡦࡥࡷࠫ෠"), bstack1l1llll_opy_ (u"ࠫࡨࡵ࡮࡯ࡧࡦࡸࡤࡵࡶࡦࡴࡢࡧࡩࡶࠧ෡"), bstack1l1llll_opy_ (u"ࠬࡲࡡࡶࡰࡦ࡬ࠬ෢"), bstack1l1llll_opy_ (u"࠭࡬ࡢࡷࡱࡧ࡭ࡥࡰࡦࡴࡶ࡭ࡸࡺࡥ࡯ࡶࡢࡧࡴࡴࡴࡦࡺࡷࠫ෣")):
      _1l1111llll_opy_ = getattr(BrowserType, _1111111ll_opy_, None)
      if _1l1111llll_opy_ is None:
        continue
      if getattr(_1l1111llll_opy_, _BSTACK_INIT_FAILURE_SENTINEL, False):
        continue
      def _1lll1ll111_opy_(bstack1ll1111l111_opy_):
        if _1lll1111ll_opy_.iscoroutinefunction(bstack1ll1111l111_opy_):
          async def _1lll111l1ll_opy_(self, *args, **kwargs):
            try:
              return await bstack1ll1111l111_opy_(self, *args, **kwargs)
            except Exception as e:
              try:
                instrument_driver_init_failure_event(e, bstack1l1llll_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦ෤"))
              except Exception as bstack1l11ll1lll_opy_:
                logger.debug(bstack1l1llll_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡧࡳࡺࡰࡦࠤࡩࡸࡩࡷࡧࡵ࠱࡮ࡴࡩࡵࠢࡦࡥࡵࡺࡵࡳࡧࠣࡷࡪࡴࡤࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࡾࢁࠧ෥").format(bstack1l11ll1lll_opy_))
              raise
          setattr(_1lll111l1ll_opy_, _BSTACK_INIT_FAILURE_SENTINEL, True)
          return _1lll111l1ll_opy_
        def _1l1llllll1_opy_(self, *args, **kwargs):
          try:
            return bstack1ll1111l111_opy_(self, *args, **kwargs)
          except Exception as e:
            try:
              instrument_driver_init_failure_event(e, bstack1l1llll_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ෦"))
            except Exception as bstack1l11ll1lll_opy_:
              logger.debug(bstack1l1llll_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡻࡱࡧࠥࡪࡲࡪࡸࡨࡶ࠲࡯࡮ࡪࡶࠣࡧࡦࡶࡴࡶࡴࡨࠤࡸ࡫࡮ࡥࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡿࢂࠨ෧").format(bstack1l11ll1lll_opy_))
            raise
        setattr(_1l1llllll1_opy_, _BSTACK_INIT_FAILURE_SENTINEL, True)
        return _1l1llllll1_opy_
      setattr(BrowserType, _1111111ll_opy_, _1lll1ll111_opy_(_1l1111llll_opy_))
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠮࡫ࡱ࡭ࡹࠦࡣࡢࡲࡷࡹࡷ࡫ࠠࡸࡴࡤࡴࡵ࡫ࡲࠡࡰࡲࡸࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤ࠻ࠢࡾࢁࠧ෨").format(e))
bstack1l1l1l111l1_opy_ = None
bstack1lllll11111_opy_ = None
bstack111l1l111l_opy_ = None
bstack1l1ll1ll11l_opy_ = None
bstack1111lll1l1_opy_ = None
bstack1111llll11_opy_ = None
bstack1111l1l1l1_opy_ = None
bstack11l1l1l1l1_opy_ = None
bstack1ll1l11ll1_opy_ = None
bstack111lll1l11_opy_ = None
bstack1llllll111l_opy_ = None
bstack11l1l11l1l_opy_ = None
bstack11l11ll1ll_opy_ = None
bstack11l1111111_opy_ = None
bstack111l111l11_opy_ = None
bstack1l111l1ll1_opy_ = None
bstack111l1lll11_opy_ = None
bstack1ll111llll_opy_ = None
bstack1llllll1lll_opy_ = None
bstack1l1l111l11l_opy_ = None
bstack1lll1ll11ll_opy_ = None
bstack11l1111lll_opy_ = None
bstack111ll111ll_opy_ = None
thread_local = threading.local()
bstack11lll1llll_opy_ = False
bstack1lll111ll1_opy_ = bstack1l1llll_opy_ (u"ࠧࠨ෩")
_11lllllll1_opy_ = None
logger = logger_utils.get_logger(__name__, bstack1l1111l111_opy_)
automation_logger = logger_utils.get_automation_logger(__name__)
global_config = Config.bstack1lll1l11_opy_()
percy = bstack11ll1l1111_opy_()
bstack111lll1l1l_opy_ = bstack1lll11l1l1l_opy_()
bstack111111l1l_opy_ = bstack_behave_listener()
def bstack1l111l11l1_opy_():
  global CONFIG
  global bstack11l11l1l1l_opy_
  global global_config
  testContextOptions = bstack1l1l111ll1_opy_(CONFIG)
  if bstack111l11l11l_opy_(CONFIG):
    if (bstack1l1llll_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ෪") in testContextOptions and str(testContextOptions[bstack1l1llll_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ෫")]).lower() == bstack1l1llll_opy_ (u"ࠨࡶࡵࡹࡪ࠭෬")):
      bstack11l11l1l1l_opy_ = True
      global_config.bstack1ll111l1l1l_opy_(True)
    if (bstack1l1llll_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭෭") in testContextOptions and str(testContextOptions[bstack1l1llll_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧ෮")]).lower() == bstack1l1llll_opy_ (u"ࠫࡹࡸࡵࡦࠩ෯")):
      global_config.bstack1ll111llll1_opy_(True)
  else:
    bstack11l11l1l1l_opy_ = True
    global_config.bstack1ll111l1l1l_opy_(True)
    global_config.bstack1ll111llll1_opy_(True)
def bstack1ll1l1111l_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1l1ll11111_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1111ll1ll_opy_():
  global bstack1l11l1111l_opy_
  args = sys.argv
  for i in range(len(args)):
    if bstack1l1llll_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡩ࡯࡯ࡨ࡬࡫࡫࡯࡬ࡦࠤ෰") == args[i].lower() or bstack1l1llll_opy_ (u"ࠨ࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡪ࡮࡭ࠢ෱") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      bstack1l11l1111l_opy_[bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫෲ")] = path
      return path
  return None
bstack11111l1ll_opy_ = re.compile(bstack1l1llll_opy_ (u"ࡳࠤ࠱࠮ࡄࡢࠤࡼࠪ࠱࠮ࡄ࠯ࡽ࠯ࠬࡂࠦෳ"))
def bstack11111l1l1l_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack11111l1ll_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack1l1llll_opy_ (u"ࠤࠧࡿࠧ෴") + group + bstack1l1llll_opy_ (u"ࠥࢁࠧ෵"), os.environ.get(group))
  return value
def bstack1111111lll_opy_():
  global bstack111ll111ll_opy_
  if bstack111ll111ll_opy_ is None:
        bstack111ll111ll_opy_ = bstack1111ll1ll_opy_()
  bstack111ll11l1l_opy_ = bstack111ll111ll_opy_
  if bstack111ll11l1l_opy_ and os.path.exists(os.path.abspath(bstack111ll11l1l_opy_)):
    fileName = bstack111ll11l1l_opy_
  if bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ෶") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack1l1llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆࠩ෷")])) and not bstack1l1llll_opy_ (u"࠭ࡦࡪ࡮ࡨࡒࡦࡳࡥࠨ෸") in locals():
    fileName = os.environ[bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ෹")]
  if bstack1l1llll_opy_ (u"ࠨࡨ࡬ࡰࡪࡔࡡ࡮ࡧࠪ෺") in locals():
    filePath = os.path.abspath(fileName)
  else:
    filePath = bstack1l1llll_opy_ (u"ࠩࠪ෻")
  bstack11l11lll11_opy_ = os.getcwd()
  bstack1l1l1l1l11_opy_ = bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭෼")
  bstack1l11l1l11l_opy_ = bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡦࡳ࡬ࠨ෽")
  while (not os.path.exists(filePath)) and bstack11l11lll11_opy_ != bstack1l1llll_opy_ (u"ࠧࠨ෾"):
    filePath = os.path.join(bstack11l11lll11_opy_, bstack1l1l1l1l11_opy_)
    if not os.path.exists(filePath):
      filePath = os.path.join(bstack11l11lll11_opy_, bstack1l11l1l11l_opy_)
    if bstack11l11lll11_opy_ != os.path.dirname(bstack11l11lll11_opy_):
      bstack11l11lll11_opy_ = os.path.dirname(bstack11l11lll11_opy_)
    else:
      bstack11l11lll11_opy_ = bstack1l1llll_opy_ (u"ࠨࠢ෿")
  bstack111ll111ll_opy_ = filePath if os.path.exists(filePath) else None
  if bstack111ll111ll_opy_ and os.path.exists(bstack111ll111ll_opy_):
    os.environ[bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ฀")] = bstack111ll111ll_opy_
  return bstack111ll111ll_opy_
def bstack11111lllll_opy_(config):
    if bstack1l1llll_opy_ (u"ࠨࡶࡨࡷࡹࡘࡥࡱࡱࡵࡸ࡮ࡴࡧࠨก") in config:
      config[bstack1l1llll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ข")] = config[bstack1l1llll_opy_ (u"ࠪࡸࡪࡹࡴࡓࡧࡳࡳࡷࡺࡩ࡯ࡩࠪฃ")]
    if bstack1l1llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࡓࡵࡺࡩࡰࡰࡶࠫค") in config:
      config[bstack1l1llll_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩฅ")] = config[bstack1l1llll_opy_ (u"࠭ࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬ࡕࡰࡵ࡫ࡲࡲࡸ࠭ฆ")]
def bstack1l11111111_opy_():
  filePath = bstack1111111lll_opy_()
  if not os.path.exists(filePath):
    bstack1lll111lll_opy_(
      bstack1l1lll1111_opy_.format(os.getcwd()))
  try:
    with open(filePath, bstack1l1llll_opy_ (u"ࠧࡳࠩง")) as stream:
      yaml.add_implicit_resolver(bstack1l1llll_opy_ (u"ࠣࠣࡳࡥࡹ࡮ࡥࡹࠤจ"), bstack11111l1ll_opy_)
      yaml.add_constructor(bstack1l1llll_opy_ (u"ࠤࠤࡴࡦࡺࡨࡦࡺࠥฉ"), bstack11111l1l1l_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      bstack11111lllll_opy_(config)
      return config
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"ࠥࡽࡦࡳ࡬ࠡࡈࡸࡰࡱࡒ࡯ࡢࡦࡨࡶࠥ࡬ࡡࡪ࡮ࡨࡨ࠱ࠦࡦࡢ࡮࡯࡭ࡳ࡭ࠠࡣࡣࡦ࡯ࠥࡺ࡯ࠡࡵࡤࡪࡪࡥ࡬ࡰࡣࡧ࠾ࠥࢁࡽ࠻ࠢࡾࢁࠧช").format(type(e).__name__, e), exc_info=True)
    with open(filePath, bstack1l1llll_opy_ (u"ࠫࡷ࠭ซ")) as stream:
      try:
        config = yaml.safe_load(stream)
        bstack11111lllll_opy_(config)
        return config
      except yaml.YAMLError as exc:
        bstack1lll111lll_opy_(bstack1ll11l111ll_opy_.format(str(exc)))
def bstack1llll1l1ll1_opy_(config):
  bstack1lll1ll111l_opy_ = bstack1llll1ll11l_opy_(config)
  for option in list(bstack1lll1ll111l_opy_):
    if option.lower() in bstack1llll1l1ll_opy_ and option != bstack1llll1l1ll_opy_[option.lower()]:
      bstack1lll1ll111l_opy_[bstack1llll1l1ll_opy_[option.lower()]] = bstack1lll1ll111l_opy_[option]
      del bstack1lll1ll111l_opy_[option]
  return config
def bstack1lllll1ll11_opy_():
  global bstack1ll111lll1_opy_
  for key, bstack111l11l1l1_opy_ in bstack1l1ll1lllll_opy_.items():
    if isinstance(bstack111l11l1l1_opy_, list):
      for var in bstack111l11l1l1_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1ll111lll1_opy_[key] = os.environ[var]
          break
    elif bstack111l11l1l1_opy_ in os.environ and os.environ[bstack111l11l1l1_opy_] and str(os.environ[bstack111l11l1l1_opy_]).strip():
      bstack1ll111lll1_opy_[key] = os.environ[bstack111l11l1l1_opy_]
  if bstack1l1llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧฌ") in os.environ:
    bstack1ll111lll1_opy_[bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪญ")] = {}
    bstack1ll111lll1_opy_[bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫฎ")][bstack1l1llll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪฏ")] = os.environ[bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫฐ")]
def bstack11lll11111_opy_():
  global bstack1111ll111_opy_
  global bstack1l1ll1lll1l_opy_
  global bstack1l11l1111l_opy_
  global bstack11l1l11111_opy_
  bstack1lll1l1ll11_opy_ = []
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) - 1 and bstack1l1llll_opy_ (u"ࠪ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ฑ").lower() == val.lower():
      bstack1111ll111_opy_[bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨฒ")] = {}
      bstack1111ll111_opy_[bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩณ")][bstack1l1llll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨด")] = sys.argv[idx + 1]
      bstack11l1l11111_opy_.append(bstack1l1llll_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࡀࠫต") + sys.argv[idx + 1])
      bstack1lll1l1ll11_opy_.extend([idx, idx + 1])
      break
  for key, bstack1llll1ll11_opy_ in bstack1111lllll_opy_.items():
    if isinstance(bstack1llll1ll11_opy_, list):
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        for var in bstack1llll1ll11_opy_:
          if bstack1l1llll_opy_ (u"ࠨ࠯࠰ࠫถ") + var.lower() == val.lower() and key not in bstack1111ll111_opy_:
            bstack1111ll111_opy_[key] = sys.argv[idx + 1]
            bstack1l1ll1lll1l_opy_ += bstack1l1llll_opy_ (u"ࠩࠣ࠱࠲࠭ท") + var + bstack1l1llll_opy_ (u"ࠪࠤࠬธ") + shlex.quote(sys.argv[idx + 1])
            bstack1llll1l1l11_opy_(bstack1l11l1111l_opy_, key, sys.argv[idx + 1])
            bstack11l1l11111_opy_.append(bstack1l1llll_opy_ (u"ࠫ࠲࠳ࠧน") + var + bstack1l1llll_opy_ (u"ࠬࡃࠧบ") + sys.argv[idx + 1])
            bstack1lll1l1ll11_opy_.extend([idx, idx + 1])
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        if bstack1l1llll_opy_ (u"࠭࠭࠮ࠩป") + bstack1llll1ll11_opy_.lower() == val.lower() and key not in bstack1111ll111_opy_:
          bstack1111ll111_opy_[key] = sys.argv[idx + 1]
          bstack1l1ll1lll1l_opy_ += bstack1l1llll_opy_ (u"ࠧࠡ࠯࠰ࠫผ") + bstack1llll1ll11_opy_ + bstack1l1llll_opy_ (u"ࠨࠢࠪฝ") + shlex.quote(sys.argv[idx + 1])
          bstack1llll1l1l11_opy_(bstack1l11l1111l_opy_, key, sys.argv[idx + 1])
          bstack11l1l11111_opy_.append(bstack1l1llll_opy_ (u"ࠩ࠰࠱ࠬพ") + bstack1llll1ll11_opy_ + bstack1l1llll_opy_ (u"ࠪࡁࠬฟ") + sys.argv[idx + 1])
          bstack1lll1l1ll11_opy_.extend([idx, idx + 1])
  for idx in sorted(set(bstack1lll1l1ll11_opy_), reverse=True):
    if idx < len(sys.argv):
      del sys.argv[idx]
  import json as _1lllllll1l1_opy_
  os.environ[bstack1l1llll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡋࡕࡒࡘࡃࡕࡈࡤࡉࡌࡊࡡࡄࡖࡌ࡙ࠧภ")] = _1lllllll1l1_opy_.dumps(bstack11l1l11111_opy_)
def bstack1ll1l11ll1l_opy_(config):
  bstack11l1ll111l_opy_ = config.keys()
  for bstack1ll11llllll_opy_, bstack1l1llll1ll_opy_ in bstack1l111ll11l_opy_.items():
    if bstack1l1llll1ll_opy_ in bstack11l1ll111l_opy_:
      config[bstack1ll11llllll_opy_] = config[bstack1l1llll1ll_opy_]
      del config[bstack1l1llll1ll_opy_]
  for bstack1ll11llllll_opy_, bstack1l1llll1ll_opy_ in bstack1111lll11_opy_.items():
    if isinstance(bstack1l1llll1ll_opy_, list):
      for bstack11lll1lll1_opy_ in bstack1l1llll1ll_opy_:
        if bstack11lll1lll1_opy_ in bstack11l1ll111l_opy_:
          config[bstack1ll11llllll_opy_] = config[bstack11lll1lll1_opy_]
          del config[bstack11lll1lll1_opy_]
          break
    elif bstack1l1llll1ll_opy_ in bstack11l1ll111l_opy_:
      config[bstack1ll11llllll_opy_] = config[bstack1l1llll1ll_opy_]
      del config[bstack1l1llll1ll_opy_]
  for bstack11lll1lll1_opy_ in list(config):
    for bstack1l1ll1l11l_opy_ in bstack1l1l11lll1_opy_:
      if bstack11lll1lll1_opy_.lower() == bstack1l1ll1l11l_opy_.lower() and bstack11lll1lll1_opy_ != bstack1l1ll1l11l_opy_:
        config[bstack1l1ll1l11l_opy_] = config[bstack11lll1lll1_opy_]
        del config[bstack11lll1lll1_opy_]
  bstack1ll1ll11l1_opy_ = [{}]
  if not config.get(bstack1l1llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨม")):
    config[bstack1l1llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩย")] = [{}]
  bstack1ll1ll11l1_opy_ = config[bstack1l1llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪร")]
  for platform in bstack1ll1ll11l1_opy_:
    for bstack11lll1lll1_opy_ in list(platform):
      for bstack1l1ll1l11l_opy_ in bstack1l1l11lll1_opy_:
        if bstack11lll1lll1_opy_.lower() == bstack1l1ll1l11l_opy_.lower() and bstack11lll1lll1_opy_ != bstack1l1ll1l11l_opy_:
          platform[bstack1l1ll1l11l_opy_] = platform[bstack11lll1lll1_opy_]
          del platform[bstack11lll1lll1_opy_]
  for bstack1ll11llllll_opy_, bstack1l1llll1ll_opy_ in bstack1111lll11_opy_.items():
    for platform in bstack1ll1ll11l1_opy_:
      if isinstance(bstack1l1llll1ll_opy_, list):
        for bstack11lll1lll1_opy_ in bstack1l1llll1ll_opy_:
          if bstack11lll1lll1_opy_ in platform:
            platform[bstack1ll11llllll_opy_] = platform[bstack11lll1lll1_opy_]
            del platform[bstack11lll1lll1_opy_]
            break
      elif bstack1l1llll1ll_opy_ in platform:
        platform[bstack1ll11llllll_opy_] = platform[bstack1l1llll1ll_opy_]
        del platform[bstack1l1llll1ll_opy_]
  for bstack111111l11_opy_ in bstack1ll1l11l11_opy_:
    if bstack111111l11_opy_ in config:
      if not bstack1ll1l11l11_opy_[bstack111111l11_opy_] in config:
        config[bstack1ll1l11l11_opy_[bstack111111l11_opy_]] = {}
      config[bstack1ll1l11l11_opy_[bstack111111l11_opy_]].update(config[bstack111111l11_opy_])
      del config[bstack111111l11_opy_]
  for platform in bstack1ll1ll11l1_opy_:
    for bstack111111l11_opy_ in bstack1ll1l11l11_opy_:
      if bstack111111l11_opy_ in list(platform):
        if not bstack1ll1l11l11_opy_[bstack111111l11_opy_] in platform:
          platform[bstack1ll1l11l11_opy_[bstack111111l11_opy_]] = {}
        platform[bstack1ll1l11l11_opy_[bstack111111l11_opy_]].update(platform[bstack111111l11_opy_])
        del platform[bstack111111l11_opy_]
  config = bstack1llll1l1ll1_opy_(config)
  return config
def bstack1111l1lll_opy_(config):
  global bstack1ll1ll111ll_opy_
  bstack1l1l1lllll_opy_ = False
  bstack1l11lllll1_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡅࡇࡉࡅ࡚ࡒࡔࡠࡎࡒࡇࡆࡒ࡟ࡊࡆࠪฤ"))
  if bstack1l1llll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ล") in config and str(config[bstack1l1llll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧฦ")]).lower() != bstack1l1llll_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪว"):
    if bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩศ") not in config or str(config[bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪษ")]).lower() == bstack1l1llll_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ส"):
      config[bstack1l1llll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧห")] = False
    else:
      bstack11ll111ll1_opy_ = bstack111llllll1_opy_()
      if bstack1l1llll_opy_ (u"ࠩ࡬ࡷ࡙ࡸࡩࡢ࡮ࡊࡶ࡮ࡪࠧฬ") in bstack11ll111ll1_opy_:
        if not bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧอ") in config:
          config[bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨฮ")] = {}
        config[bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩฯ")][bstack1l1llll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨะ")] = bstack1l1llll_opy_ (u"ࠧࡢࡶࡶ࠱ࡷ࡫ࡰࡦࡣࡷࡩࡷ࠭ั")
        bstack1l1l1lllll_opy_ = True
        bstack1ll1ll111ll_opy_ = config[bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬา")].get(bstack1l1llll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫำ"))
  if bstack111l11l11l_opy_(config) and bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧิ") in config and str(config[bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨี")]).lower() != bstack1l1llll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫึ") and not bstack1l1l1lllll_opy_:
    if not bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪื") in config:
      config[bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶุࠫ")] = {}
    bstack1l1ll1l1l11_opy_ = config[bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷูࠬ")].get(bstack1l1llll_opy_ (u"ࠩࡶ࡯࡮ࡶࡂࡪࡰࡤࡶࡾࡏ࡮ࡪࡶ࡬ࡥࡱ࡯ࡳࡢࡶ࡬ࡳࡳฺ࠭"))
    if bstack1l11lllll1_opy_:
      if bstack1l1ll1l1l11_opy_:
        config[bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ฻")][bstack1l1llll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭฼")] = bstack1l11lllll1_opy_
      elif bstack1l1llll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ฽") not in config[bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ฾")]:
        config[bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ฿")][bstack1l1llll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪเ")] = bstack1l11lllll1_opy_
    if not bstack1l1ll1l1l11_opy_ and bstack1l1llll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫแ") not in config[bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧโ")]:
      bstack1l1111ll_opy_ = datetime.datetime.now()
      bstack11l1l11lll_opy_ = bstack1l1111ll_opy_.strftime(bstack1l1llll_opy_ (u"ࠫࠪࡪ࡟ࠦࡤࡢࠩࡍࠫࡍࠨใ"))
      hostname = socket.gethostname()
      bstack1llllll1111_opy_ = bstack1l1llll_opy_ (u"ࠬ࠭ไ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1l1llll_opy_ (u"࠭ࡻࡾࡡࡾࢁࡤࢁࡽࠨๅ").format(bstack11l1l11lll_opy_, hostname, bstack1llllll1111_opy_)
      config[bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫๆ")][bstack1l1llll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ็")] = identifier
    bstack1ll1ll111ll_opy_ = config[bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ่࠭")].get(bstack1l1llll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ้ࠬ"))
  return config
def bstack1llll1l111l_opy_():
  bstack1ll11111lll_opy_ =  bstack11111l1lll_opy_()[bstack1l1llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴ๊ࠪ")]
  return bstack1ll11111lll_opy_ if bstack1ll11111lll_opy_ else -1
def bstack1l111l111l_opy_(bstack1ll11111lll_opy_):
  global CONFIG
  if not bstack1l1llll_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃ๋ࠧ") in CONFIG[bstack1l1llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ์")]:
    return
  CONFIG[bstack1l1llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩํ")] = CONFIG[bstack1l1llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ๎")].replace(
    bstack1l1llll_opy_ (u"ࠩࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫ๏"),
    str(bstack1ll11111lll_opy_)
  )
def bstack11llll1111_opy_():
  global CONFIG
  if not bstack1l1llll_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾࠩ๐") in CONFIG[bstack1l1llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭๑")]:
    return
  bstack1l1111ll_opy_ = datetime.datetime.now()
  bstack11l1l11lll_opy_ = bstack1l1111ll_opy_.strftime(bstack1l1llll_opy_ (u"ࠬࠫࡤ࠮ࠧࡥ࠱ࠪࡎ࠺ࠦࡏࠪ๒"))
  CONFIG[bstack1l1llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ๓")] = CONFIG[bstack1l1llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ๔")].replace(
    bstack1l1llll_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧ๕"),
    bstack11l1l11lll_opy_
  )
def bstack1l1ll1llll1_opy_():
  global CONFIG
  if bstack1l1llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ๖") in CONFIG and not bool(CONFIG[bstack1l1llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ๗")]):
    del CONFIG[bstack1l1llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭๘")]
    return
  if not bstack1l1llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ๙") in CONFIG:
    CONFIG[bstack1l1llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ๚")] = bstack1l1llll_opy_ (u"ࠧࠤࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪ๛")
  if bstack1l1llll_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧ๜") in CONFIG[bstack1l1llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ๝")]:
    bstack11llll1111_opy_()
    os.environ[bstack1l1llll_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧ๞")] = CONFIG[bstack1l1llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭๟")]
  if not bstack1l1llll_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧ๠") in CONFIG[bstack1l1llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ๡")]:
    return
  bstack1ll11111lll_opy_ = bstack1l1llll_opy_ (u"ࠧࠨ๢")
  bstack1ll1l1l1lll_opy_ = bstack1llll1l111l_opy_()
  if bstack1ll1l1l1lll_opy_ != -1:
    bstack1ll11111lll_opy_ = bstack1l1llll_opy_ (u"ࠨࡅࡌࠤࠬ๣") + str(bstack1ll1l1l1lll_opy_)
  if bstack1ll11111lll_opy_ == bstack1l1llll_opy_ (u"ࠩࠪ๤"):
    bstack1lllllll111_opy_ = bstack1l1lll111l_opy_(CONFIG[bstack1l1llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭๥")])
    if bstack1lllllll111_opy_ != -1:
      bstack1ll11111lll_opy_ = str(bstack1lllllll111_opy_)
  if bstack1ll11111lll_opy_:
    bstack1l111l111l_opy_(bstack1ll11111lll_opy_)
    os.environ[bstack1l1llll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨ๦")] = CONFIG[bstack1l1llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ๧")]
def bstack1lll1l1111l_opy_(bstack11lll11l11_opy_, bstack1ll1111l11_opy_, path):
  json_data = {
    bstack1l1llll_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ๨"): bstack1ll1111l11_opy_
  }
  if os.path.exists(path):
    bstack1lll111111l_opy_ = json.load(open(path, bstack1l1llll_opy_ (u"ࠧࡳࡤࠪ๩")))
  else:
    bstack1lll111111l_opy_ = {}
  bstack1lll111111l_opy_[bstack11lll11l11_opy_] = json_data
  with open(path, bstack1l1llll_opy_ (u"ࠣࡹ࠮ࠦ๪")) as outfile:
    json.dump(bstack1lll111111l_opy_, outfile)
_1ll11llll1_opy_ = int(os.environ.get(bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡤࡉࡏࡐࡔࡇࡣ࡙࡚ࡌࡠࡕࠪ๫"), bstack1l1llll_opy_ (u"ࠪ࠶࠹࠶ࠧ๬")))
_1l1l111l111_opy_ = int(os.environ.get(bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔ࡟ࡍࡑࡆࡏࡤ࡚ࡉࡎࡇࡒ࡙࡙ࡥࡓࠨ๭"), bstack1l1llll_opy_ (u"ࠬ࠷࠸࠱ࠩ๮")))
_1l1l111l1l_opy_ = int(os.environ.get(bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡡࡇࡖࡆࡏࡎࡠࡖࡌࡑࡊࡕࡕࡕࡡࡖࠫ๯"), bstack1l1llll_opy_ (u"ࠧ࠷࠲ࠪ๰")))
_1l1lll1l11_opy_ = int(os.environ.get(bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡣࡕࡕࡓࡕࡡࡗࡍࡒࡋࡏࡖࡖࡢࡔࡔࡒࡌࡠࡕࠪ๱"), bstack1l1llll_opy_ (u"ࠩ࠹࠴ࠬ๲")))
_1l1l11ll1l1_opy_ = int(os.environ.get(bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡥࡔࡆࡃࡕࡈࡔ࡝ࡎࡠࡆࡕࡅࡎࡔ࡟ࡔࠩ๳"), bstack1l1llll_opy_ (u"ࠫ࠸࠶ࠧ๴")))
_11l11ll1l1_opy_ = {}
_1l1ll111lll_opy_ = threading.Lock()
def _1ll1l1l1l1l_opy_(bs_config):
  bstack1ll111l1lll_opy_ = bs_config.get(bstack1l1llll_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ๵"), bstack1l1llll_opy_ (u"࠭ࠧ๶")) or bstack1l1llll_opy_ (u"ࠧࠨ๷")
  build = bs_config.get(bstack1l1llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ๸"), bstack1l1llll_opy_ (u"ࠩࠪ๹")) or bstack1l1llll_opy_ (u"ࠪࠫ๺")
  try:
    _1llll11l1ll_opy_ = str(os.getuid())
  except AttributeError:
    try:
      import getpass
      _1llll11l1ll_opy_ = getpass.getuser()
    except Exception:
      _1llll11l1ll_opy_ = os.environ.get(bstack1l1llll_opy_ (u"࡚࡙ࠫࡅࡓࡐࡄࡑࡊ࠭๻")) or os.environ.get(bstack1l1llll_opy_ (u"࡛ࠬࡓࡆࡔࠪ๼")) or bstack1l1llll_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴࠧ๽")
  bstack1ll1l111ll_opy_ = bstack1l1llll_opy_ (u"ࠧࡼࡿ࠽࠾ࢀࢃ࠺࠻ࡽࢀࠫ๾").format(_1llll11l1ll_opy_, bstack1ll111l1lll_opy_, build)
  bstack1l111l1lll_opy_ = hashlib.sha1(bstack1ll1l111ll_opy_.encode(bstack1l1llll_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ๿"))).hexdigest()[:16]
  bstack111ll11111_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠯ࡶࡨࡰ࠳ࡣࡰࡱࡵࡨࠬ຀"))
  try:
    os.makedirs(bstack111ll11111_opy_, exist_ok=True)
  except Exception:
    bstack111ll11111_opy_ = tempfile.gettempdir()
  lock_path = os.path.join(bstack111ll11111_opy_, bstack1l1llll_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡧ࡯࡮࠮ࡵࡨࡷࡸ࡯࡯࡯࠯ࡾࢁ࠳ࡲ࡯ࡤ࡭ࠪກ").format(bstack1l111l1lll_opy_))
  bstack1lllll1ll1l_opy_ = os.path.join(bstack111ll11111_opy_, bstack1l1llll_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡨࡩ࡯࠯ࡶࡩࡸࡹࡩࡰࡰ࠰ࡿࢂ࠴ࡪࡴࡱࡱࠫຂ").format(bstack1l111l1lll_opy_))
  return lock_path, bstack1lllll1ll1l_opy_, bstack1ll1l111ll_opy_, bstack111ll11111_opy_, bstack1l111l1lll_opy_
def _1l1l1lll1l1_opy_(bstack111ll11111_opy_=None, bstack1l111l1lll_opy_=None, bstack1llllllll11_opy_=_1l1l111l1l_opy_):
  bstack111ll11111_opy_ = bstack111ll11111_opy_ or _11l11ll1l1_opy_.get(bstack1l1llll_opy_ (u"ࠬࡪࡩࡳࠩ຃"))
  bstack1l111l1lll_opy_ = bstack1l111l1lll_opy_ or _11l11ll1l1_opy_.get(bstack1l1llll_opy_ (u"࠭࡫ࡦࡻࡢ࡬ࡦࡹࡨࠨຄ"))
  if not bstack111ll11111_opy_ or not bstack1l111l1lll_opy_:
    return
  pattern = bstack1l1llll_opy_ (u"ࠧ࠯ࡤࡶࡸࡦࡩ࡫࠮ࡤ࡬ࡲ࠲ࡹࡥࡴࡵ࡬ࡳࡳ࠳ࡻࡾ࠰ࡩࡳࡱࡲ࡯ࡸࡧࡵ࠱ࠬ຅").format(bstack1l111l1lll_opy_)
  deadline = time.time() + bstack1llllllll11_opy_
  while time.time() < deadline:
    try:
      active = [f for f in os.listdir(bstack111ll11111_opy_)
                if f.startswith(pattern) and f.endswith(bstack1l1llll_opy_ (u"ࠨ࠰ࡤࡧࡹ࡯ࡶࡦࠩຆ"))]
    except Exception:
      return
    if not active:
      return
    time.sleep(1)
  logger.warning(bstack1l1llll_opy_ (u"ࠩࡥ࡭ࡳ࠳ࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡨࡲࡰࡱࡵࡷࡦࡴࡶࠤࡩ࡯ࡤࠡࡰࡲࡸࠥࡪࡲࡢ࡫ࡱࠤ࡮ࡴࠠࡼࡿࡶ࠿ࠥࡶࡲࡰࡥࡨࡩࡩ࡯࡮ࡨࠩງ").format(bstack1llllllll11_opy_))
def _1l1l11ll1l_opy_(bstack111ll11111_opy_, bstack1l111l1lll_opy_):
  try:
    marker = os.path.join(bstack111ll11111_opy_,
      bstack1l1llll_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡧ࡯࡮࠮ࡵࡨࡷࡸ࡯࡯࡯࠯ࡾࢁ࠳࡬࡯࡭࡮ࡲࡻࡪࡸ࠭ࡼࡿ࠱ࡥࡨࡺࡩࡷࡧࠪຈ").format(bstack1l111l1lll_opy_, os.getpid()))
    with open(marker, bstack1l1llll_opy_ (u"ࠫࡼ࠭ຉ")) as bstack1l1ll111l11_opy_:
      bstack1l1ll111l11_opy_.write(str(time.time()))
    atexit.register(lambda p=marker: os.remove(p) if os.path.exists(p) else None)
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"ࠬࡨࡩ࡯࠯ࡶࡩࡸࡹࡩࡰࡰ࠽ࠤ࡫ࡵ࡬࡭ࡱࡺࡩࡷࠦ࡭ࡢࡴ࡮ࡩࡷࠦࡷࡳ࡫ࡷࡩࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡾࠩຊ").format(e))
def _1lllll1111l_opy_(bs_config):
  if os.environ.get(bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡓࡆࡕࡖࡍࡔࡔ࡟ࡊࡆࠪ຋"), bstack1l1llll_opy_ (u"ࠧࠨຌ")) == bstack1l1llll_opy_ (u"ࠨࠩຍ"):
    return
  bstack1ll11lllll_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡤࡉࡏࡐࡔࡇࡣࡐࡋ࡙ࡠࡊࡄࡗࡍ࠭ຎ"), bstack1l1llll_opy_ (u"ࠪࠫຏ"))
  if bstack1ll11lllll_opy_:
    try:
      _, _, _, _, bstack1l1lll1lll1_opy_ = _1ll1l1l1l1l_opy_(bs_config)
      if bstack1ll11lllll_opy_ == bstack1l1lll1lll1_opy_:
        return
    except Exception as e:
      logger.debug(bstack1l1llll_opy_ (u"ࠫࡧ࡯࡮࠮ࡵࡨࡷࡸ࡯࡯࡯࠼ࠣ࡯ࡪࡿ࡟ࡩࡣࡶ࡬ࠥࡩ࡯࡮ࡲࡤࡶࡪࠦࡦࡢ࡫࡯ࡩࡩࠦࠨࡼࡿࠬ࠿ࠥࡺࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡢࡵࠣࡰࡪࡧ࡫ࠨຐ").format(e))
  if not bstack1ll11lllll_opy_ and os.environ.get(bstack1l1llll_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡞ࡄࡊࡕࡗࡣ࡜ࡕࡒࡌࡇࡕࠫຑ"), bstack1l1llll_opy_ (u"࠭ࠧຒ")):
    return
  bstack1llll111111_opy_ = []
  for _1ll11lllll1_opy_ in (bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡔࡇࡖࡗࡎࡕࡎࡠࡋࡇࠫຓ"), bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡎࡌࡗ࡙ࡋࡎࡠࡃࡇࡈࡗ࠭ດ"),
             bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡤࡉࡏࡐࡔࡇࡣࡉࡏࡒࠨຕ"), bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡥࡃࡐࡑࡕࡈࡤࡑࡅ࡚ࡡࡋࡅࡘࡎࠧຖ"),
             bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡗࡉࡑ࡟ࡄࡊࡌࡐࡉࡥࡗࡐࡔࡎࡉࡗ࠭ທ"), bstack1l1llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨຘ"),
             bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪນ"), bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬບ"),
             bstack1l1llll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧປ"), bstack1l1llll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧຜ")):
    if os.environ.pop(_1ll11lllll1_opy_, None) is not None:
      bstack1llll111111_opy_.append(_1ll11lllll1_opy_)
  try:
    from browserstack_sdk.sdk_cli.cli import cli as _1lllll1l1ll_opy_
    _1lllll1l1ll_opy_.cli_listen_addr = None
    _1lllll1l1ll_opy_.bstack111l111l1l_opy_ = True
  except Exception as _e:
    logger.debug(bstack1l1llll_opy_ (u"ࠪࡦ࡮ࡴ࠭ࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡸࡥࡴࡧࡷࠤࡨࡲࡩࠡࡵࡷࡥࡹ࡫ࠠࡢࡨࡷࡩࡷࠦࡳࡤࡴࡸࡦ࠿ࠦࡻࡾࠩຝ").format(_e))
  if bstack1llll111111_opy_:
    logger.info(bstack1l1llll_opy_ (u"ࠫࡧ࡯࡮࠮ࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡷࡨࡸࡵࡣࡤࡨࡨࠥࢁࡽࠡ࡮ࡨࡥࡰ࡫ࡤࠡࡧࡱࡺࠥࡼࡡࡳࡵࠣࡪࡷࡵ࡭ࠡࡷࡱࡶࡪࡲࡡࡵࡧࡧࠤࡵࡧࡲࡦࡰࡷࠤࡘࡊࡋࠡࡴࡸࡲࠬພ").format(len(bstack1llll111111_opy_)))
def _1ll11l11l1l_opy_(bs_config):
  if FileLock is None:
    logger.debug(bstack1l1llll_opy_ (u"ࠬࡨࡩ࡯࠯ࡶࡩࡸࡹࡩࡰࡰ࠽ࠤ࡫࡯࡬ࡦ࡮ࡲࡧࡰࠦࡵ࡯ࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨ࠰ࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡳࡵࡣࡱࡨࡦࡲ࡯࡯ࡧࠪຟ"))
    return (bstack1l1llll_opy_ (u"࠭ࡳࡵࡣࡱࡨࡦࡲ࡯࡯ࡧࠪຠ"), None, None)
  if os.environ.get(bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡔࡇࡖࡗࡎࡕࡎࡠࡋࡇࠫມ"), bstack1l1llll_opy_ (u"ࠨࠩຢ")) != bstack1l1llll_opy_ (u"ࠩࠪຣ"):
    try:
      bstack1ll1l1ll1ll_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡥࡃࡐࡑࡕࡈࡤࡊࡉࡓࠩ຤"), bstack1l1llll_opy_ (u"ࠫࠬລ"))
      bstack1ll1l111l1l_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡏࡎࡠࡅࡒࡓࡗࡊ࡟ࡌࡇ࡜ࡣࡍࡇࡓࡉࠩ຦"), bstack1l1llll_opy_ (u"࠭ࠧວ"))
      if not bstack1ll1l1ll1ll_opy_ or not bstack1ll1l111l1l_opy_:
        _, _, _, bstack1ll1l1ll1ll_opy_, bstack1ll1l111l1l_opy_ = _1ll1l1l1l1l_opy_(bs_config)
      _1l1l11ll1l_opy_(bstack1ll1l1ll1ll_opy_, bstack1ll1l111l1l_opy_)
    except Exception as _e:
      logger.debug(bstack1l1llll_opy_ (u"ࠧࡣ࡫ࡱ࠱ࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡥ࡯ࡸ࠰࡭ࡳ࡮ࡥࡳ࡫ࡷࡩࡩࠦࡦࡰ࡮࡯ࡳࡼ࡫ࡲࠡ࡯ࡤࡶࡰ࡫ࡲࠡࡵࡨࡸࡺࡶࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡽࢀࠫຨ").format(_e))
    return (bstack1l1llll_opy_ (u"ࠨࡨࡲࡰࡱࡵࡷࡦࡴࠪຩ"), None, None)
  lock_path, bstack1lllll1ll1l_opy_, bstack1ll1l111ll_opy_, bstack111ll11111_opy_, bstack1l111l1lll_opy_ = _1ll1l1l1l1l_opy_(bs_config)
  lock = FileLock(lock_path, timeout=_1l1l111l111_opy_)
  try:
    lock.acquire()
  except bstack1ll11l1l1ll_opy_:
    _11l11l1l11_opy_ = time.time() + _1l1lll1l11_opy_
    while time.time() < _11l11l1l11_opy_:
      try:
        if os.path.exists(bstack1lllll1ll1l_opy_):
          with open(bstack1lllll1ll1l_opy_, bstack1l1llll_opy_ (u"ࠩࡵࠫສ")) as f:
            cached = json.load(f)
          _alive = True
          if cached and cached.get(bstack1l1llll_opy_ (u"ࠪࡰࡪࡧࡤࡦࡴࡢࡴ࡮ࡪࠧຫ")):
            try:
              os.kill(int(cached[bstack1l1llll_opy_ (u"ࠫࡱ࡫ࡡࡥࡧࡵࡣࡵ࡯ࡤࠨຬ")]), 0)
            except (ProcessLookupError, PermissionError, OSError):
              _alive = False
          if (cached
              and cached.get(bstack1l1llll_opy_ (u"ࠬࡱࡥࡺࠩອ")) == bstack1ll1l111ll_opy_
              and cached.get(bstack1l1llll_opy_ (u"࠭ࡦࡪࡰࡤࡰ࡮ࢀࡥࡥࠩຮ")) is True
              and cached.get(bstack1l1llll_opy_ (u"ࠧࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨຯ"))
              and cached.get(bstack1l1llll_opy_ (u"ࠨࡥ࡯࡭ࡤࡲࡩࡴࡶࡨࡲࡤࡧࡤࡥࡴࠪະ"))
              and (time.time() - float(cached.get(bstack1l1llll_opy_ (u"ࠩࡺࡶ࡮ࡺࡴࡦࡰࡄࡸ࡙ࡹࠧັ"), 0))) < _1ll11llll1_opy_
              and _alive):
            os.environ[bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡗࡊ࡙ࡓࡊࡑࡑࡣࡎࡊࠧາ")] = cached[bstack1l1llll_opy_ (u"ࠫࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠬຳ")]
            os.environ[bstack1l1llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤࡒࡉࡔࡖࡈࡒࡤࡇࡄࡅࡔࠪິ")] = cached[bstack1l1llll_opy_ (u"࠭ࡣ࡭࡫ࡢࡰ࡮ࡹࡴࡦࡰࡢࡥࡩࡪࡲࠨີ")]
            if cached.get(bstack1l1llll_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡠࡤࡸ࡭ࡱࡪ࡟ࡶࡷ࡬ࡨࠬຶ")):
              os.environ[bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ື")] = cached[bstack1l1llll_opy_ (u"ࠩࡷࡩࡸࡺࡨࡶࡤࡢࡦࡺ࡯࡬ࡥࡡࡸࡹ࡮ࡪຸࠧ")]
            try:
              from browserstack_sdk.sdk_cli.cli import cli as _1lllll1l1ll_opy_
              _1lllll1l1ll_opy_.bstack111l111l1l_opy_ = False
            except Exception as _e:
              logger.debug(bstack1l1llll_opy_ (u"ࠪࡦ࡮ࡴ࠭ࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡳࡳࡸࡺ࠭ࡵ࡫ࡰࡩࡴࡻࡴࠡࡨ࡯࡭ࡵࠦࡣ࡭࡫࠱࡭ࡸࡥ࡭ࡢ࡫ࡱࡣࡵࡸ࡯ࡤࡧࡶࡷࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡾູࠩ").format(_e))
            logger.info(bstack1l1llll_opy_ (u"ࠫࡧ࡯࡮࠮ࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡴࡴࡹࡴ࠮ࡶ࡬ࡱࡪࡵࡵࡵࠢࡩࡳࡱࡲ࡯ࡸࡧࡵࠤ࡯ࡵࡩ࡯ࡧࡧࠤࡱ࡫ࡡࡥࡧࡵࠤࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࡂࢁࡽࠨ຺").format(cached[bstack1l1llll_opy_ (u"ࠬࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩ࠭ົ")]))
            _1l1l11ll1l_opy_(bstack111ll11111_opy_, bstack1l111l1lll_opy_)
            return (bstack1l1llll_opy_ (u"࠭ࡦࡰ࡮࡯ࡳࡼ࡫ࡲࠨຼ"), None, bstack1lllll1ll1l_opy_)
      except Exception as _e:
        logger.debug(bstack1l1llll_opy_ (u"ࠧࡣ࡫ࡱ࠱ࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡰࡰࡵࡷ࠱ࡹ࡯࡭ࡦࡱࡸࡸࠥࡩ࡯ࡰࡴࡧࠤࡷ࡫࠭ࡳࡧࡤࡨࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡾࠩຽ").format(_e))
      time.sleep(2)
    logger.warning(bstack1l1llll_opy_ (u"ࠨࡤ࡬ࡲ࠲ࡹࡥࡴࡵ࡬ࡳࡳࠦࡣࡰࡱࡵࡨࠥࡲ࡯ࡤ࡭ࠣࡸ࡮ࡳࡥࡰࡷࡷࠤࡆࡔࡄࠡࡰࡲࠤ࡫ࡸࡥࡴࡪࠣࡧࡴࡵࡲࡥࠢࡤࡪࡹ࡫ࡲࠡࡽࢀࡷࠥࡶ࡯࡭࡮ࠣ⠘ࠥࡶࡲࡰࡥࡨࡩࡩ࡯࡮ࡨࠢࡤࡷࠥࡹࡴࡢࡰࡧࡥࡱࡵ࡮ࡦࠢ࡯ࡩࡦࡪࡥࡳࠢࠫࡻ࡮ࡲ࡬ࠡࡴࡨ࡫࡮ࡹࡴࡦࡴࠣࡥࠥࡹࡥࡱࡣࡵࡥࡹ࡫ࠠࡕࡔࡄࠤࡧࡻࡩ࡭ࡦࠬࠫ຾").format(_1l1lll1l11_opy_))
    return (bstack1l1llll_opy_ (u"ࠩࡶࡸࡦࡴࡤࡢ࡮ࡲࡲࡪ࠭຿"), None, bstack1lllll1ll1l_opy_)
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"ࠪࡦ࡮ࡴ࠭ࡴࡧࡶࡷ࡮ࡵ࡮ࠡ࡮ࡲࡧࡰࠦࡡࡤࡳࡸ࡭ࡷ࡫ࠠࡦࡴࡵࡳࡷࠦࠨࡼࡿࠬࠤ⠙ࠦࡳࡵࡣࡱࡨࡦࡲ࡯࡯ࡧࠪເ").format(e))
    return (bstack1l1llll_opy_ (u"ࠫࡸࡺࡡ࡯ࡦࡤࡰࡴࡴࡥࠨແ"), None, bstack1lllll1ll1l_opy_)
  try:
    cached = None
    if os.path.exists(bstack1lllll1ll1l_opy_):
      try:
        with open(bstack1lllll1ll1l_opy_, bstack1l1llll_opy_ (u"ࠬࡸࠧໂ")) as f:
          cached = json.load(f)
      except Exception:
        cached = None
    bstack1l1ll1l111_opy_ = (
      cached is not None
      and cached.get(bstack1l1llll_opy_ (u"࠭࡫ࡦࡻࠪໃ")) == bstack1ll1l111ll_opy_
      and cached.get(bstack1l1llll_opy_ (u"ࠧࡧ࡫ࡱࡥࡱ࡯ࡺࡦࡦࠪໄ")) is True
      and (time.time() - float(cached.get(bstack1l1llll_opy_ (u"ࠨࡹࡵ࡭ࡹࡺࡥ࡯ࡃࡷࡘࡸ࠭໅"), 0))) < _1ll11llll1_opy_
      and cached.get(bstack1l1llll_opy_ (u"ࠩࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠪໆ"))
      and cached.get(bstack1l1llll_opy_ (u"ࠪࡧࡱ࡯࡟࡭࡫ࡶࡸࡪࡴ࡟ࡢࡦࡧࡶࠬ໇"))
    )
    if bstack1l1ll1l111_opy_ and cached.get(bstack1l1llll_opy_ (u"ࠫࡱ࡫ࡡࡥࡧࡵࡣࡵ࡯ࡤࠨ່")):
      try:
        os.kill(int(cached[bstack1l1llll_opy_ (u"ࠬࡲࡥࡢࡦࡨࡶࡤࡶࡩࡥ້ࠩ")]), 0)
      except (ProcessLookupError, PermissionError, OSError):
        bstack1l1ll1l111_opy_ = False
    if bstack1l1ll1l111_opy_:
      os.environ[bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡓࡆࡕࡖࡍࡔࡔ࡟ࡊࡆ໊ࠪ")] = cached[bstack1l1llll_opy_ (u"ࠧࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨ໋")]
      os.environ[bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡎࡌࡗ࡙ࡋࡎࡠࡃࡇࡈࡗ࠭໌")] = cached[bstack1l1llll_opy_ (u"ࠩࡦࡰ࡮ࡥ࡬ࡪࡵࡷࡩࡳࡥࡡࡥࡦࡵࠫໍ")]
      _11l1111ll1_opy_ = cached.get(bstack1l1llll_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡣࡧࡻࡩ࡭ࡦࡢࡹࡺ࡯ࡤࠨ໎"), bstack1l1llll_opy_ (u"ࠫࠬ໏"))
      if _11l1111ll1_opy_:
        os.environ[bstack1l1llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ໐")] = _11l1111ll1_opy_
      try:
        from browserstack_sdk.sdk_cli.cli import cli as _1lllll1l1ll_opy_
        _1lllll1l1ll_opy_.bstack111l111l1l_opy_ = False
      except Exception as _e:
        logger.debug(bstack1l1llll_opy_ (u"࠭ࡢࡪࡰ࠰ࡷࡪࡹࡳࡪࡱࡱ࠾ࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡨ࡯࡭ࡵࠦࡣ࡭࡫࠱࡭ࡸࡥ࡭ࡢ࡫ࡱࡣࡵࡸ࡯ࡤࡧࡶࡷ࠿ࠦࡻࡾࠩ໑").format(_e))
      logger.info(
        bstack1l1llll_opy_ (u"ࠧࡣ࡫ࡱ࠱ࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡦࡰ࡮࡯ࡳࡼ࡫ࡲࠡ࡬ࡲ࡭ࡳ࡫ࡤࠡ࡮ࡨࡥࡩ࡫ࡲࠡࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥ࠿ࡾࢁࠥࡧࡤࡥࡴࡀࡿࢂ࠭໒").format(
          cached[bstack1l1llll_opy_ (u"ࠨࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠩ໓")], cached[bstack1l1llll_opy_ (u"ࠩࡦࡰ࡮ࡥ࡬ࡪࡵࡷࡩࡳࡥࡡࡥࡦࡵࠫ໔")]))
      _1l1l11ll1l_opy_(bstack111ll11111_opy_, bstack1l111l1lll_opy_)
      try:
        lock.release()
      except Exception:
        pass
      return (bstack1l1llll_opy_ (u"ࠪࡪࡴࡲ࡬ࡰࡹࡨࡶࠬ໕"), None, bstack1lllll1ll1l_opy_)
    with _1l1ll111lll_opy_:
      _11l11ll1l1_opy_[bstack1l1llll_opy_ (u"ࠫࡩ࡯ࡲࠨ໖")] = bstack111ll11111_opy_
      _11l11ll1l1_opy_[bstack1l1llll_opy_ (u"ࠬࡱࡥࡺࡡ࡫ࡥࡸ࡮ࠧ໗")] = bstack1l111l1lll_opy_
    os.environ[bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡡࡆࡓࡔࡘࡄࡠࡆࡌࡖࠬ໘")] = bstack111ll11111_opy_
    os.environ[bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡢࡇࡔࡕࡒࡅࡡࡎࡉ࡞ࡥࡈࡂࡕࡋࠫ໙")] = bstack1l111l1lll_opy_
    logger.info(bstack1l1llll_opy_ (u"ࠨࡤ࡬ࡲ࠲ࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡤ࡮ࡤ࡭ࡲ࡫ࡤࠡ࡮ࡨࡥࡩ࡫ࡲࠡࡴࡲࡰࡪࠦࠨࡤࡹࡧࡁࢀࢃࠬࠡࡲࡵࡳ࡯࡫ࡣࡵ࠿ࡾࢁ࠱ࠦࡢࡶ࡫࡯ࡨࡂࢁࡽࠪࠩ໚").format(
      os.getcwd(), bs_config.get(bstack1l1llll_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ໛"), bstack1l1llll_opy_ (u"ࠪࠫໜ")), bs_config.get(bstack1l1llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧໝ"), bstack1l1llll_opy_ (u"ࠬ࠭ໞ"))))
    return (bstack1l1llll_opy_ (u"࠭࡬ࡦࡣࡧࡩࡷ࠭ໟ"), lock, bstack1lllll1ll1l_opy_)
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"ࠧࡣ࡫ࡱ࠱ࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡲࡰ࡮ࡨ࠱ࡦࡩࡱࡶ࡫ࡵࡩࠥࡻ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠬ໠").format(e))
    try:
      lock.release()
    except Exception:
      pass
    return (bstack1l1llll_opy_ (u"ࠨࡵࡷࡥࡳࡪࡡ࡭ࡱࡱࡩࠬ໡"), None, bstack1lllll1ll1l_opy_)
def _1lll1lll1l1_opy_(lock, bstack1lllll1ll1l_opy_, bs_config):
  if lock is None or bstack1lllll1ll1l_opy_ is None:
    return
  try:
    bin_session_id = os.environ.get(bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡖࡉࡘ࡙ࡉࡐࡐࡢࡍࡉ࠭໢"), bstack1l1llll_opy_ (u"ࠪࠫ໣"))
    cli_listen_addr = os.environ.get(bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡑࡏࡓࡕࡇࡑࡣࡆࡊࡄࡓࠩ໤"), bstack1l1llll_opy_ (u"ࠬ࠭໥"))
    bstack1111l1ll11_opy_ = os.environ.get(bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ໦"), bstack1l1llll_opy_ (u"ࠧࠨ໧"))
    bstack1ll111l1lll_opy_ = bs_config.get(bstack1l1llll_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭໨"), bstack1l1llll_opy_ (u"ࠩࠪ໩")) or bstack1l1llll_opy_ (u"ࠪࠫ໪")
    build = bs_config.get(bstack1l1llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ໫"), bstack1l1llll_opy_ (u"ࠬ࠭໬")) or bstack1l1llll_opy_ (u"࠭ࠧ໭")
    try:
      _1llll11l1ll_opy_ = str(os.getuid())
    except AttributeError:
      try:
        import getpass
        _1llll11l1ll_opy_ = getpass.getuser()
      except Exception:
        _1llll11l1ll_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠧࡖࡕࡈࡖࡓࡇࡍࡆࠩ໮")) or os.environ.get(bstack1l1llll_opy_ (u"ࠨࡗࡖࡉࡗ࠭໯")) or bstack1l1llll_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࠪ໰")
    bstack1ll1l111ll_opy_ = bstack1l1llll_opy_ (u"ࠪࡿࢂࡀ࠺ࡼࡿ࠽࠾ࢀࢃࠧ໱").format(_1llll11l1ll_opy_, bstack1ll111l1lll_opy_, build)
    bstack111ll11111_opy_ = os.path.dirname(bstack1lllll1ll1l_opy_)
    bstack1l111l1lll_opy_ = hashlib.sha1(bstack1ll1l111ll_opy_.encode(bstack1l1llll_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ໲"))).hexdigest()[:16]
    with _1l1ll111lll_opy_:
      _11l11ll1l1_opy_[bstack1l1llll_opy_ (u"ࠬࡪࡩࡳࠩ໳")] = bstack111ll11111_opy_
      _11l11ll1l1_opy_[bstack1l1llll_opy_ (u"࠭࡫ࡦࡻࡢ࡬ࡦࡹࡨࠨ໴")] = bstack1l111l1lll_opy_
    os.environ[bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡢࡇࡔࡕࡒࡅࡡࡇࡍࡗ࠭໵")] = bstack111ll11111_opy_
    os.environ[bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡣࡈࡕࡏࡓࡆࡢࡏࡊ࡟࡟ࡉࡃࡖࡌࠬ໶")] = bstack1l111l1lll_opy_
    payload = {
      bstack1l1llll_opy_ (u"ࠩ࡮ࡩࡾ࠭໷"): bstack1ll1l111ll_opy_,
      bstack1l1llll_opy_ (u"ࠪࡻࡷ࡯ࡴࡵࡧࡱࡅࡹ࡚ࡳࠨ໸"): time.time(),
      bstack1l1llll_opy_ (u"ࠫࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠬ໹"): bin_session_id,
      bstack1l1llll_opy_ (u"ࠬࡩ࡬ࡪࡡ࡯࡭ࡸࡺࡥ࡯ࡡࡤࡨࡩࡸࠧ໺"): cli_listen_addr,
      bstack1l1llll_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨ࡟ࡣࡷ࡬ࡰࡩࡥࡵࡶ࡫ࡧࠫ໻"): bstack1111l1ll11_opy_,
      bstack1l1llll_opy_ (u"ࠧ࡭ࡧࡤࡨࡪࡸ࡟ࡱ࡫ࡧࠫ໼"): os.getpid(),
      bstack1l1llll_opy_ (u"ࠨࡥࡲࡳࡷࡪ࡟ࡥ࡫ࡵࠫ໽"): bstack111ll11111_opy_,
      bstack1l1llll_opy_ (u"ࠩ࡮ࡩࡾࡥࡨࡢࡵ࡫ࠫ໾"): bstack1l111l1lll_opy_,
      bstack1l1llll_opy_ (u"ࠪࡪ࡮ࡴࡡ࡭࡫ࡽࡩࡩ࠭໿"): bool(bin_session_id and cli_listen_addr),
    }
    try:
      with open(bstack1lllll1ll1l_opy_, bstack1l1llll_opy_ (u"ࠫࡼ࠭ༀ")) as f:
        json.dump(payload, f)
      if bin_session_id and cli_listen_addr:
        logger.debug(bstack1l1llll_opy_ (u"ࠬࡨࡩ࡯࠯ࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࡱ࡫ࡡࡥࡧࡵࠤࡵࡻࡢ࡭࡫ࡶ࡬ࡪࡪࠠࡤࡱࡲࡶࡩࠦࡦࡪ࡮ࡨࠤࢀࢃࠧ༁").format(bstack1lllll1ll1l_opy_))
        _1l1llllllll_opy_ = os.path.join(bstack111ll11111_opy_, bstack1l1llll_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡣ࡫ࡱ࠱ࡸ࡫ࡳࡴ࡫ࡲࡲ࠲ࢁࡽ࠯࡮ࡲࡧࡰ࠭༂").format(bstack1l111l1lll_opy_))
        atexit.register(lambda p=bstack1lllll1ll1l_opy_, l=_1l1llllllll_opy_: [os.remove(x) for x in (p, l) if os.path.exists(x)])
      else:
        logger.warning(bstack1l1llll_opy_ (u"ࠧࡣ࡫ࡱ࠱ࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡂࡐࡑࡗࡗ࡙ࡘࡁࡑࠢࡧ࡭ࡩࠦ࡮ࡰࡶࠣࡴࡴࡶࡵ࡭ࡣࡷࡩࠥࡨࡩ࡯ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡩࡳࡼࠠࡷࡣࡵࡷࡀࠦࡳࡪࡤ࡯࡭ࡳ࡭ࡳࠡࡹ࡬ࡰࡱࠦࡦࡢ࡮࡯ࠤࡧࡧࡣ࡬ࠢࡷࡳࠥࡹࡴࡢࡰࡧࡥࡱࡵ࡮ࡦࠢ࡯ࡩࡦࡪࡥࡳࠢࡵࡳࡱ࡫ࠧ༃"))
    except Exception as e:
      logger.warning(bstack1l1llll_opy_ (u"ࠨࡤ࡬ࡲ࠲ࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡤࡱࡲࡶࡩࠦࡦࡪ࡮ࡨࠤࡼࡸࡩࡵࡧࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࢀࢃࠧ༄").format(e))
  finally:
    try:
      lock.release()
    except Exception:
      pass
def bstack1l1lll111l_opy_(bstack11lll11l11_opy_):
  bstack11lll11l11_opy_ = str(bstack11lll11l11_opy_)
  bstack111lll111l_opy_ = os.path.join(os.path.expanduser(bstack1l1llll_opy_ (u"ࠩࢁࠫ༅")), bstack1l1llll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ༆"))
  try:
    if not os.path.exists(bstack111lll111l_opy_):
      os.makedirs(bstack111lll111l_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1l1llll_opy_ (u"ࠫࢃ࠭༇")), bstack1l1llll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ༈"), bstack1l1llll_opy_ (u"࠭࠮ࡣࡷ࡬ࡰࡩ࠳࡮ࡢ࡯ࡨ࠱ࡨࡧࡣࡩࡧ࠱࡮ࡸࡵ࡮ࠨ༉"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1l1llll_opy_ (u"ࠧࡸࠩ༊")):
        pass
      with open(file_path, bstack1l1llll_opy_ (u"ࠣࡹ࠮ࠦ་")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1l1llll_opy_ (u"ࠩࡵࠫ༌")) as bstack1l111ll1ll_opy_:
      bstack11l1l1l1ll_opy_ = json.load(bstack1l111ll1ll_opy_)
    if bstack11lll11l11_opy_ in bstack11l1l1l1ll_opy_:
      bstack1llll1l1111_opy_ = bstack11l1l1l1ll_opy_[bstack11lll11l11_opy_][bstack1l1llll_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ།")]
      bstack1ll11111111_opy_ = int(bstack1llll1l1111_opy_) + 1
      bstack1lll1l1111l_opy_(bstack11lll11l11_opy_, bstack1ll11111111_opy_, file_path)
      return bstack1ll11111111_opy_
    else:
      bstack1lll1l1111l_opy_(bstack11lll11l11_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warning(bstack1lll11lll1l_opy_.format(str(e)))
    return -1
def bstack1111l1l1ll_opy_(config):
  if not config[bstack1l1llll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭༎")] or not config[bstack1l1llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ༏")]:
    return True
  else:
    return False
def bstack1lll11l1l1_opy_(config, index=0):
  global bstack11ll111lll_opy_
  bstack1l1l11l1l_opy_ = {}
  caps = bstack1ll1ll1l11l_opy_ + bstack11lll1ll11_opy_
  if config.get(bstack1l1llll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ༐"), False):
    bstack1l1l11l1l_opy_[bstack1l1llll_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫ༑")] = True
    bstack1l1l11l1l_opy_[bstack1l1llll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࡔࡶࡴࡪࡱࡱࡷࠬ༒")] = config.get(bstack1l1llll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭༓"), {})
  if bstack11ll111lll_opy_:
    caps += bstack1lll11lll11_opy_
  for key in config:
    if key in caps + [bstack1l1llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭༔")]:
      continue
    bstack1l1l11l1l_opy_[key] = config[key]
  if bstack1l1llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ༕") in config:
    for bstack1ll111ll111_opy_ in config[bstack1l1llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ༖")][index]:
      if bstack1ll111ll111_opy_ in caps:
        continue
      bstack1l1l11l1l_opy_[bstack1ll111ll111_opy_] = config[bstack1l1llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ༗")][index][bstack1ll111ll111_opy_]
  bstack1l1l11l1l_opy_[bstack1l1llll_opy_ (u"ࠧࡩࡱࡶࡸࡓࡧ࡭ࡦ༘ࠩ")] = socket.gethostname()
  if bstack1l1llll_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯༙ࠩ") in bstack1l1l11l1l_opy_:
    del (bstack1l1l11l1l_opy_[bstack1l1llll_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪ༚")])
  return bstack1l1l11l1l_opy_
def bstack1llll11l1l_opy_(config):
  global bstack11ll111lll_opy_
  bstack1lll1l111l1_opy_ = {}
  caps = bstack11lll1ll11_opy_
  if bstack11ll111lll_opy_:
    caps += bstack1lll11lll11_opy_
  for key in caps:
    if key in config:
      bstack1lll1l111l1_opy_[key] = config[key]
  return bstack1lll1l111l1_opy_
def bstack1111l11111_opy_(bstack1l1l11l1l_opy_, bstack1lll1l111l1_opy_):
  bstack1ll1ll1111_opy_ = {}
  for key in bstack1l1l11l1l_opy_.keys():
    if key in bstack1l111ll11l_opy_:
      bstack1ll1ll1111_opy_[bstack1l111ll11l_opy_[key]] = bstack1l1l11l1l_opy_[key]
    else:
      bstack1ll1ll1111_opy_[key] = bstack1l1l11l1l_opy_[key]
  for key in bstack1lll1l111l1_opy_:
    if key in bstack1l111ll11l_opy_:
      bstack1ll1ll1111_opy_[bstack1l111ll11l_opy_[key]] = bstack1lll1l111l1_opy_[key]
    else:
      bstack1ll1ll1111_opy_[key] = bstack1lll1l111l1_opy_[key]
  return bstack1ll1ll1111_opy_
def _1llll11ll1_opy_(caps):
  try:
    if bstack11ll111lll_opy_ or not bstack1ll1lll11l_opy_():
      return caps
    if not isinstance(caps, dict):
      return caps
    opts = caps.get(bstack1l1llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ༛"))
    opts = opts if isinstance(opts, dict) else None
    device = caps.get(bstack1l1llll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫ༜")) or caps.get(bstack1l1llll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩ༝"))
    if not device and opts:
      device = opts.get(bstack1l1llll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪ༞")) or opts.get(bstack1l1llll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ༟"))
    bstack1lll1l11ll1_opy_ = str(device).lower() if device else bstack1l1llll_opy_ (u"ࠨࠩ༠")
    if bstack1l1llll_opy_ (u"ࠩ࡬ࡴ࡭ࡵ࡮ࡦࠩ༡") in bstack1lll1l11ll1_opy_ or bstack1l1llll_opy_ (u"ࠪ࡭ࡵࡧࡤࠨ༢") in bstack1lll1l11ll1_opy_:
      removed = False
      for key in (bstack1l1llll_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡡࡰࡳࡧ࡯࡬ࡦࠩ༣"), bstack1l1llll_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩ༤")):
        if key in caps:
          del caps[key]
          removed = True
        if opts and key in opts:
          del opts[key]
          removed = True
      if removed:
        logger.debug(bstack1l1llll_opy_ (u"ࠨࡓࡵࡴ࡬ࡴࡵ࡫ࡤࠡࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠥ࡬࡯ࡳࠢ࡬ࡓࡘࠦࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࠨࡥࡧࡹ࡭ࡨ࡫࠽ࠦࡵࠬࠦ༥"), device)
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"ࠢࡪࡑࡖࠤࡕ࡝ࠠࡳࡧࡤࡰࡒࡵࡢࡪ࡮ࡨࠤࡸࡺࡲࡪࡲࠣࡷࡰ࡯ࡰࡱࡧࡧ࠾ࠥࢁࡽ࠻ࠢࡾࢁࠧ༦").format(type(e).__name__, e))
  return caps
def get_caps(config, index=0):
  global bstack11ll111lll_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack111lllll11_opy_ = bstack1ll111lllll_opy_(bstack1l11111l11_opy_, config, logger)
  bstack1lll1l111l1_opy_ = bstack1llll11l1l_opy_(config)
  bstack11l11l1111_opy_ = bstack11lll1ll11_opy_
  bstack11l11l1111_opy_ += bstack1ll1l11lll1_opy_
  bstack1lll1l111l1_opy_ = update(bstack1lll1l111l1_opy_, bstack111lllll11_opy_)
  if bstack11ll111lll_opy_:
    bstack11l11l1111_opy_ += bstack1lll11lll11_opy_
  if bstack1l1llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ༧") in config:
    if bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ༨") in config[bstack1l1llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭༩")][index]:
      caps[bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ༪")] = config[bstack1l1llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ༫")][index][bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ༬")]
    if bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ༭") in config[bstack1l1llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ༮")][index]:
      caps[bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ༯")] = str(config[bstack1l1llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭༰")][index][bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ༱")])
    bstack111l1111l_opy_ = bstack1ll111lllll_opy_(bstack1l11111l11_opy_, config[bstack1l1llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ༲")][index], logger)
    bstack11l11l1111_opy_ += list(bstack111l1111l_opy_.keys())
    for bstack11l111l11l_opy_ in bstack11l11l1111_opy_:
      if bstack11l111l11l_opy_ in config[bstack1l1llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ༳")][index]:
        if bstack11l111l11l_opy_ == bstack1l1llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ༴"):
          try:
            bstack111l1111l_opy_[bstack11l111l11l_opy_] = str(config[bstack1l1llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶ༵ࠫ")][index][bstack11l111l11l_opy_] * 1.0)
          except Exception as e:
            logger.debug(bstack1l1llll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠤࡳࡻ࡭ࡦࡴ࡬ࡧࠥࡩ࡯ࡦࡴࡦ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡽࢀ࠾ࠥࢁࡽࠣ༶").format(type(e).__name__, e), exc_info=True)
            bstack111l1111l_opy_[bstack11l111l11l_opy_] = str(config[bstack1l1llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ༷࠭")][index][bstack11l111l11l_opy_])
        else:
          bstack111l1111l_opy_[bstack11l111l11l_opy_] = config[bstack1l1llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ༸")][index][bstack11l111l11l_opy_]
        del (config[bstack1l1llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ༹")][index][bstack11l111l11l_opy_])
    bstack1lll1l111l1_opy_ = update(bstack1lll1l111l1_opy_, bstack111l1111l_opy_)
  bstack1l1l11l1l_opy_ = bstack1lll11l1l1_opy_(config, index)
  for bstack11lll1lll1_opy_ in bstack11lll1ll11_opy_ + list(bstack111lllll11_opy_.keys()):
    if bstack11lll1lll1_opy_ in bstack1l1l11l1l_opy_:
      bstack1lll1l111l1_opy_[bstack11lll1lll1_opy_] = bstack1l1l11l1l_opy_[bstack11lll1lll1_opy_]
      del (bstack1l1l11l1l_opy_[bstack11lll1lll1_opy_])
  if bstack11l1ll1111_opy_(config):
    bstack1l1l11l1l_opy_[bstack1l1llll_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭༺")] = True
    caps.update(bstack1lll1l111l1_opy_)
    caps[bstack1l1llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ༻")] = bstack1l1l11l1l_opy_
  else:
    bstack1l1l11l1l_opy_[bstack1l1llll_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨ༼")] = False
    caps.update(bstack1111l11111_opy_(bstack1l1l11l1l_opy_, bstack1lll1l111l1_opy_))
    if bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ༽") in caps:
      caps[bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫ༾")] = caps[bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ༿")]
      del (caps[bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪཀ")])
    if bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧཁ") in caps:
      caps[bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩག")] = caps[bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩགྷ")]
      del (caps[bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪང")])
  caps = _1llll11ll1_opy_(caps)
  return caps
def bstack1l1l111ll11_opy_():
  global bstack1lll1ll1l11_opy_
  global CONFIG
  if bstack1lll1ll1l11_opy_ != bstack1l1llll_opy_ (u"ࠪࠫཅ") and (bstack1lll1ll1l11_opy_.startswith(bstack1l1llll_opy_ (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࠬཆ")) or bstack1lll1ll1l11_opy_.startswith(bstack1l1llll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠧཇ"))):
    return bstack1lll1ll1l11_opy_
  if bstack1l1ll11111_opy_() <= version.parse(bstack1l1llll_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭཈")):
    if bstack1lll1ll1l11_opy_ != bstack1l1llll_opy_ (u"ࠧࠨཉ"):
      return bstack1l1llll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤཊ") + bstack1lll1ll1l11_opy_ + bstack1l1llll_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨཋ")
    return bstack1lll1111ll1_opy_
  if bstack1lll1ll1l11_opy_ != bstack1l1llll_opy_ (u"ࠪࠫཌ"):
    return bstack1l1llll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨཌྷ") + bstack1lll1ll1l11_opy_ + bstack1l1llll_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨཎ")
  return bstack1ll1111ll_opy_
def bstack1ll1l1l1111_opy_(options):
  return hasattr(options, bstack1l1llll_opy_ (u"࠭ࡳࡦࡶࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠧཏ"))
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
def bstack1l1l1l11l11_opy_(options, bstack1l1l11lllll_opy_):
  for bstack1l11ll1ll1_opy_ in bstack1l1l11lllll_opy_:
    if bstack1l11ll1ll1_opy_ in [bstack1l1llll_opy_ (u"ࠧࡢࡴࡪࡷࠬཐ"), bstack1l1llll_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬད")]:
      continue
    if bstack1l11ll1ll1_opy_ in options._experimental_options:
      options._experimental_options[bstack1l11ll1ll1_opy_] = update(options._experimental_options[bstack1l11ll1ll1_opy_],
                                                         bstack1l1l11lllll_opy_[bstack1l11ll1ll1_opy_])
    else:
      options.add_experimental_option(bstack1l11ll1ll1_opy_, bstack1l1l11lllll_opy_[bstack1l11ll1ll1_opy_])
  if bstack1l1llll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧདྷ") in bstack1l1l11lllll_opy_:
    for arg in bstack1l1l11lllll_opy_[bstack1l1llll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨན")]:
      options.add_argument(arg)
    del (bstack1l1l11lllll_opy_[bstack1l1llll_opy_ (u"ࠫࡦࡸࡧࡴࠩཔ")])
  if bstack1l1llll_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩཕ") in bstack1l1l11lllll_opy_:
    for ext in bstack1l1l11lllll_opy_[bstack1l1llll_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪབ")]:
      try:
        options.add_extension(ext)
      except OSError:
        options.add_encoded_extension(ext)
    del (bstack1l1l11lllll_opy_[bstack1l1llll_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫབྷ")])
def bstack1lllllll11_opy_(options):
  global CONFIG
  global bstack1l11l11l11_opy_
  try:
    if not bstack1l11l11l11_opy_ or not options:
      return options
    from bstack_utils.bstack1111ll1l1l_opy_ import bstack1l1l1lll11l_opy_
    bstack111111l1l1_opy_ = bstack1l1l1lll11l_opy_(options, bstack1ll1111l1l_opy_=bstack1l1llll_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࠣམ"))
    if bstack111111l1l1_opy_ > 0:
      logger.debug(bstack1l1llll_opy_ (u"ࠤࡏࡳࡦࡪࠠࡵࡧࡶࡸ࡮ࡴࡧ࠻ࠢࡄࡨࡩ࡫ࡤࠡࡽࢀࠤࡩ࡫ࡦࡢࡷ࡯ࡸࠥࡉࡨࡳࡱࡰࡩࠥࡧࡲࡨࡷࡰࡩࡳࡺࡳࠡࡨࡲࡶࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩࠧཙ").format(bstack111111l1l1_opy_))
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡩ࡯࡬ࡨࡧࡹࠦ࡬ࡰࡣࡧࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥࡉࡨࡳࡱࡰࡩࠥࡵࡰࡵ࡫ࡲࡲࡸࡀࠠࡼࡿࠥཚ").format(e))
  return options
def bstack111l1lll1l_opy_(options, bstack1l11l1llll_opy_):
  if bstack1l1llll_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪཛ") in bstack1l11l1llll_opy_:
    for bstack11ll11ll1l_opy_ in bstack1l11l1llll_opy_[bstack1l1llll_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫཛྷ")]:
      if bstack11ll11ll1l_opy_ in options._preferences:
        options._preferences[bstack11ll11ll1l_opy_] = update(options._preferences[bstack11ll11ll1l_opy_], bstack1l11l1llll_opy_[bstack1l1llll_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬཝ")][bstack11ll11ll1l_opy_])
      else:
        options.set_preference(bstack11ll11ll1l_opy_, bstack1l11l1llll_opy_[bstack1l1llll_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ཞ")][bstack11ll11ll1l_opy_])
  if bstack1l1llll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ཟ") in bstack1l11l1llll_opy_:
    for arg in bstack1l11l1llll_opy_[bstack1l1llll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧའ")]:
      options.add_argument(arg)
def bstack11ll1lll11_opy_(options, bstack1lll111l1l1_opy_):
  if bstack1l1llll_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࠫཡ") in bstack1lll111l1l1_opy_:
    options.use_webview(bool(bstack1lll111l1l1_opy_[bstack1l1llll_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࠬར")]))
  bstack1l1l1l11l11_opy_(options, bstack1lll111l1l1_opy_)
def bstack111l1llll1_opy_(options, bstack111ll1ll1l_opy_):
  for bstack11111ll11l_opy_ in bstack111ll1ll1l_opy_:
    if bstack11111ll11l_opy_ in [bstack1l1llll_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩལ"), bstack1l1llll_opy_ (u"࠭ࡡࡳࡩࡶࠫཤ")]:
      continue
    options.set_capability(bstack11111ll11l_opy_, bstack111ll1ll1l_opy_[bstack11111ll11l_opy_])
  if bstack1l1llll_opy_ (u"ࠧࡢࡴࡪࡷࠬཥ") in bstack111ll1ll1l_opy_:
    for arg in bstack111ll1ll1l_opy_[bstack1l1llll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ས")]:
      options.add_argument(arg)
  if bstack1l1llll_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭ཧ") in bstack111ll1ll1l_opy_:
    options.bstack1lll11l1ll1_opy_(bool(bstack111ll1ll1l_opy_[bstack1l1llll_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧཨ")]))
def bstack11ll11l1l1_opy_(options, bstack1l1lll1l11l_opy_):
  for bstack11111ll111_opy_ in bstack1l1lll1l11l_opy_:
    if bstack11111ll111_opy_ in [bstack1l1llll_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨཀྵ"), bstack1l1llll_opy_ (u"ࠬࡧࡲࡨࡵࠪཪ")]:
      continue
    options._options[bstack11111ll111_opy_] = bstack1l1lll1l11l_opy_[bstack11111ll111_opy_]
  if bstack1l1llll_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪཫ") in bstack1l1lll1l11l_opy_:
    for bstack1l1ll11l1l_opy_ in bstack1l1lll1l11l_opy_[bstack1l1llll_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫཬ")]:
      options.bstack1llllll1l1_opy_(
        bstack1l1ll11l1l_opy_, bstack1l1lll1l11l_opy_[bstack1l1llll_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ཭")][bstack1l1ll11l1l_opy_])
  if bstack1l1llll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ཮") in bstack1l1lll1l11l_opy_:
    for arg in bstack1l1lll1l11l_opy_[bstack1l1llll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ཯")]:
      options.add_argument(arg)
def bstack1lll111l111_opy_(options, caps):
  if not hasattr(options, bstack1l1llll_opy_ (u"ࠫࡐࡋ࡙ࠨ཰")):
    return
  if options.KEY == bstack1l1llll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵཱࠪ"):
    options = a11y.bstack1l1l1l11ll_opy_(bstack1ll1l11ll11_opy_=options, config=CONFIG)
  if options.KEY == bstack1l1llll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶིࠫ") and options.KEY in caps:
    bstack1l1l1l11l11_opy_(options, caps[bstack1l1llll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷཱིࠬ")])
  elif options.KEY == bstack1l1llll_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸུ࠭") and options.KEY in caps:
    bstack111l1lll1l_opy_(options, caps[bstack1l1llll_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹཱུࠧ")])
  elif options.KEY == bstack1l1llll_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫྲྀ") and options.KEY in caps:
    bstack111l1llll1_opy_(options, caps[bstack1l1llll_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬཷ")])
  elif options.KEY == bstack1l1llll_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ླྀ") and options.KEY in caps:
    bstack11ll1lll11_opy_(options, caps[bstack1l1llll_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧཹ")])
  elif options.KEY == bstack1l1llll_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸེ࠭") and options.KEY in caps:
    bstack11ll11l1l1_opy_(options, caps[bstack1l1llll_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹཻࠧ")])
def bstack1llll11ll11_opy_(caps):
  global bstack11ll111lll_opy_
  if isinstance(os.environ.get(bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇོࠪ")), str):
    bstack11ll111lll_opy_ = eval(os.getenv(bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈཽࠫ")))
  if bstack11ll111lll_opy_:
    if bstack1ll1l1111l_opy_() < version.parse(bstack1l1llll_opy_ (u"ࠫ࠷࠴࠳࠯࠲ࠪཾ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1l1llll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬཿ")
    if bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨྀࠫ") in caps:
      browser = caps[bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩཱྀࠬ")]
    elif bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩྂ") in caps:
      browser = caps[bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪྃ")]
    browser = str(browser).lower()
    if browser == bstack1l1llll_opy_ (u"ࠪ࡭ࡵ࡮࡯࡯ࡧ྄ࠪ") or browser == bstack1l1llll_opy_ (u"ࠫ࡮ࡶࡡࡥࠩ྅"):
      browser = bstack1l1llll_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬ྆")
    if browser == bstack1l1llll_opy_ (u"࠭ࡳࡢ࡯ࡶࡹࡳ࡭ࠧ྇"):
      browser = bstack1l1llll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧྈ")
    if browser not in [bstack1l1llll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨྉ"), bstack1l1llll_opy_ (u"ࠩࡨࡨ࡬࡫ࠧྊ"), bstack1l1llll_opy_ (u"ࠪ࡭ࡪ࠭ྋ"), bstack1l1llll_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫྌ"), bstack1l1llll_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭ྍ")]:
      return None
    try:
      package = bstack1l1llll_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠯ࡹࡨࡦࡩࡸࡩࡷࡧࡵ࠲ࢀࢃ࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨྎ").format(browser)
      name = bstack1l1llll_opy_ (u"ࠧࡐࡲࡷ࡭ࡴࡴࡳࠨྏ")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1ll1l1l1111_opy_(options):
        return None
      for bstack11lll1lll1_opy_ in caps.keys():
        options.set_capability(bstack11lll1lll1_opy_, caps[bstack11lll1lll1_opy_])
      bstack1lll111l111_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1lllll111l_opy_(options, bstack11111lll1l_opy_):
  if not bstack1ll1l1l1111_opy_(options):
    return
  for bstack11lll1lll1_opy_ in bstack11111lll1l_opy_.keys():
    if bstack11lll1lll1_opy_ in bstack1ll1l11lll1_opy_:
      continue
    if bstack11lll1lll1_opy_ in options._caps and type(options._caps[bstack11lll1lll1_opy_]) in [dict, list]:
      options._caps[bstack11lll1lll1_opy_] = update(options._caps[bstack11lll1lll1_opy_], bstack11111lll1l_opy_[bstack11lll1lll1_opy_])
    else:
      options.set_capability(bstack11lll1lll1_opy_, bstack11111lll1l_opy_[bstack11lll1lll1_opy_])
  bstack1lll111l111_opy_(options, bstack11111lll1l_opy_)
  if bstack1l1llll_opy_ (u"ࠨ࡯ࡲࡾ࠿ࡪࡥࡣࡷࡪ࡫ࡪࡸࡁࡥࡦࡵࡩࡸࡹࠧྐ") in options._caps:
    if options._caps[bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧྑ")] and options._caps[bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨྒ")].lower() != bstack1l1llll_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬྒྷ"):
      del options._caps[bstack1l1llll_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡧࡩࡧࡻࡧࡨࡧࡵࡅࡩࡪࡲࡦࡵࡶࠫྔ")]
def bstack11l1lll1l1_opy_(proxy_config):
  if bstack1l1llll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪྕ") in proxy_config:
    proxy_config[bstack1l1llll_opy_ (u"ࠧࡴࡵ࡯ࡔࡷࡵࡸࡺࠩྖ")] = proxy_config[bstack1l1llll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬྗ")]
    del (proxy_config[bstack1l1llll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭྘")])
  if bstack1l1llll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭ྙ") in proxy_config and proxy_config[bstack1l1llll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧྚ")].lower() != bstack1l1llll_opy_ (u"ࠬࡪࡩࡳࡧࡦࡸࠬྛ"):
    proxy_config[bstack1l1llll_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩྜ")] = bstack1l1llll_opy_ (u"ࠧ࡮ࡣࡱࡹࡦࡲࠧྜྷ")
  if bstack1l1llll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡁࡶࡶࡲࡧࡴࡴࡦࡪࡩࡘࡶࡱ࠭ྞ") in proxy_config:
    proxy_config[bstack1l1llll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬྟ")] = bstack1l1llll_opy_ (u"ࠪࡴࡦࡩࠧྠ")
  return proxy_config
def bstack1l1l11l1ll1_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1l1llll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪྡ") in config:
    return proxy
  config[bstack1l1llll_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫྡྷ")] = bstack11l1lll1l1_opy_(config[bstack1l1llll_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬྣ")])
  if proxy == None:
    proxy = Proxy(config[bstack1l1llll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭ྤ")])
  return proxy
def bstack1ll1ll1lll1_opy_(self):
  global CONFIG
  global bstack11l1l11l1l_opy_
  try:
    proxy = bstack1l111ll111_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1l1llll_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭ྥ")):
        proxies = bstack1ll1ll1111l_opy_(proxy, bstack1l1l111ll11_opy_())
        if len(proxies) > 0:
          protocol, bstack1ll1lllll1_opy_ = proxies.popitem()
          if bstack1l1llll_opy_ (u"ࠤ࠽࠳࠴ࠨྦ") in bstack1ll1lllll1_opy_:
            return bstack1ll1lllll1_opy_
          else:
            return bstack1l1llll_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦྦྷ") + bstack1ll1lllll1_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1l1llll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡱࡴࡲࡼࡾࠦࡵࡳ࡮ࠣ࠾ࠥࢁࡽࠣྨ").format(str(e)))
  return bstack11l1l11l1l_opy_(self)
def bstack1111lll11l_opy_():
  global CONFIG
  return bstack11ll1l1ll1_opy_(CONFIG) and bstack1l1111l1ll_opy_() and bstack1l1ll11111_opy_() >= version.parse(bstack1l1l1ll1l11_opy_)
def bstack1lll111ll11_opy_():
  global CONFIG
  return (bstack1l1llll_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨྩ") in CONFIG or bstack1l1llll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪྪ") in CONFIG) and bstack1ll1lll11l_opy_()
def bstack1llll1ll11l_opy_(config):
  bstack1lll1ll111l_opy_ = {}
  if bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫྫ") in config:
    bstack1lll1ll111l_opy_ = config[bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬྫྷ")]
  if bstack1l1llll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨྭ") in config:
    bstack1lll1ll111l_opy_ = config[bstack1l1llll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩྮ")]
  proxy = bstack1l111ll111_opy_(config)
  if proxy:
    if proxy.endswith(bstack1l1llll_opy_ (u"ࠫ࠳ࡶࡡࡤࠩྯ")) and os.path.isfile(proxy):
      bstack1lll1ll111l_opy_[bstack1l1llll_opy_ (u"ࠬ࠳ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨྰ")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1l1llll_opy_ (u"࠭࠮ࡱࡣࡦࠫྱ")):
        proxies = bstack1ll11l111l1_opy_(config, bstack1l1l111ll11_opy_())
        if len(proxies) > 0:
          protocol, bstack1ll1lllll1_opy_ = proxies.popitem()
          if bstack1l1llll_opy_ (u"ࠢ࠻࠱࠲ࠦྲ") in bstack1ll1lllll1_opy_:
            parsed_url = urlparse(bstack1ll1lllll1_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1l1llll_opy_ (u"ࠣ࠼࠲࠳ࠧླ") + bstack1ll1lllll1_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1lll1ll111l_opy_[bstack1l1llll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡉࡱࡶࡸࠬྴ")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1lll1ll111l_opy_[bstack1l1llll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡲࡶࡹ࠭ྵ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1lll1ll111l_opy_[bstack1l1llll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡘࡷࡪࡸࠧྶ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1lll1ll111l_opy_[bstack1l1llll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡦࡹࡳࠨྷ")] = str(parsed_url.password)
  return bstack1lll1ll111l_opy_
def bstack1l1l111ll1_opy_(config):
  if bstack1l1llll_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫྸ") in config:
    return config[bstack1l1llll_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬྐྵ")]
  return {}
def update_caps_for_local(caps):
  global bstack1ll1ll111ll_opy_
  if bstack1l1llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩྺ") in caps:
    caps[bstack1l1llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪྻ")][bstack1l1llll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩྼ")] = True
    if bstack1ll1ll111ll_opy_:
      caps[bstack1l1llll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ྽")][bstack1l1llll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ྾")] = bstack1ll1ll111ll_opy_
  else:
    caps[bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࠫ྿")] = True
    if bstack1ll1ll111ll_opy_:
      caps[bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ࿀")] = bstack1ll1ll111ll_opy_
@measure(event_name=EVENTS.bstack1llll1ll111_opy_, stage=STAGE.SINGLE, bstack11lllll111_opy_=SESSION_NAME)
def bstack1llll111l11_opy_():
  global CONFIG, bstack1ll1ll111ll_opy_
  if not bstack111l11l11l_opy_(CONFIG) or cli.is_enabled(CONFIG):
    return
  if bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ࿁") in CONFIG and bstack11lll11l1l_opy_(CONFIG[bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭࿂")]):
    if (
      bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ࿃") in CONFIG
      and bstack11lll11l1l_opy_(CONFIG[bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ࿄")].get(bstack1l1llll_opy_ (u"ࠬࡹ࡫ࡪࡲࡅ࡭ࡳࡧࡲࡺࡋࡱ࡭ࡹ࡯ࡡ࡭࡫ࡶࡥࡹ࡯࡯࡯ࠩ࿅")))
    ):
      logger.debug(bstack1l1llll_opy_ (u"ࠨࡌࡰࡥࡤࡰࠥࡨࡩ࡯ࡣࡵࡽࠥࡴ࡯ࡵࠢࡶࡸࡦࡸࡴࡦࡦࠣࡥࡸࠦࡳ࡬࡫ࡳࡆ࡮ࡴࡡࡳࡻࡌࡲ࡮ࡺࡩࡢ࡮࡬ࡷࡦࡺࡩࡰࡰࠣ࡭ࡸࠦࡥ࡯ࡣࡥࡰࡪࡪ࿆ࠢ"))
      return
    bstack1lll1ll111l_opy_ = bstack1llll1ll11l_opy_(CONFIG)
    bstack1ll1ll111ll_opy_ = bstack1lll1ll111l_opy_.get(bstack1l1llll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ࿇")) or bstack1ll1ll111ll_opy_
    bstack1111llllll_opy_(CONFIG[bstack1l1llll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ࿈")], bstack1lll1ll111l_opy_)
def bstack1111llllll_opy_(key, bstack1lll1ll111l_opy_):
  global bstack1l11llll11_opy_
  logger.info(bstack1ll11lll11l_opy_)
  try:
    bstack1l11llll11_opy_ = Local()
    bstack1llllll1l1l_opy_ = {bstack1l1llll_opy_ (u"ࠩ࡮ࡩࡾ࠭࿉"): key}
    bstack1llllll1l1l_opy_.update(bstack1lll1ll111l_opy_)
    logger.debug(bstack1lll1ll1ll1_opy_.format(str(bstack1llllll1l1l_opy_)).replace(key, bstack1l1llll_opy_ (u"ࠪ࡟ࡗࡋࡄࡂࡅࡗࡉࡉࡣࠧ࿊")))
    bstack1l11llll11_opy_.start(**bstack1llllll1l1l_opy_)
    if bstack1l11llll11_opy_.isRunning():
      logger.info(bstack11ll11l1ll_opy_)
  except Exception as e:
    bstack1lll111lll_opy_(bstack1l1l1ll11ll_opy_.format(str(e)))
def bstack11l1llllll_opy_():
  global bstack1l11llll11_opy_
  if bstack1l11llll11_opy_.isRunning():
    logger.info(bstack1ll1lll1ll1_opy_)
    bstack1l11llll11_opy_.stop()
  if bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡈࡊࡌࡁࡖࡎࡗࡣࡑࡕࡃࡂࡎࡢࡍࡉ࠭࿋") in os.environ:
    del os.environ[bstack1l1llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡉࡋࡆࡂࡗࡏࡘࡤࡒࡏࡄࡃࡏࡣࡎࡊࠧ࿌")]
  bstack1l11llll11_opy_ = None
def bstack1111l1lll1_opy_(bstack1ll111l1111_opy_=[]):
  global CONFIG
  bstack1lll1111lll_opy_ = []
  bstack1l1llll1ll1_opy_ = [bstack1l1llll_opy_ (u"࠭࡯ࡴࠩ࿍"), bstack1l1llll_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪ࿎"), bstack1l1llll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬ࿏"), bstack1l1llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ࿐"), bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ࿑"), bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ࿒")]
  try:
    for err in bstack1ll111l1111_opy_:
      bstack1ll1l11lll_opy_ = {}
      for k in bstack1l1llll1ll1_opy_:
        val = CONFIG[bstack1l1llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ࿓")][int(err[bstack1l1llll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ࿔")])].get(k)
        if val:
          bstack1ll1l11lll_opy_[k] = val
      if(err[bstack1l1llll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭࿕")] != bstack1l1llll_opy_ (u"ࠨࠩ࿖")):
        bstack1ll1l11lll_opy_[bstack1l1llll_opy_ (u"ࠩࡷࡩࡸࡺࡳࠨ࿗")] = {
          err[bstack1l1llll_opy_ (u"ࠪࡲࡦࡳࡥࠨ࿘")]: err[bstack1l1llll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ࿙")]
        }
        bstack1lll1111lll_opy_.append(bstack1ll1l11lll_opy_)
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧࡱࡵࡱࡦࡺࡴࡪࡰࡪࠤࡩࡧࡴࡢࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸ࠿ࠦࠧ࿚") + str(e))
  finally:
    return bstack1lll1111lll_opy_
def bstack1lll1lll1l_opy_(file_name):
  bstack111111111l_opy_ = []
  try:
    bstack1l1l11l111_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1l1l11l111_opy_):
      with open(bstack1l1l11l111_opy_) as f:
        bstack1l1l1ll111l_opy_ = json.load(f)
        bstack111111111l_opy_ = bstack1l1l1ll111l_opy_
      os.remove(bstack1l1l11l111_opy_)
    return bstack111111111l_opy_
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡨ࡬ࡲࡩ࡯࡮ࡨࠢࡨࡶࡷࡵࡲࠡ࡮࡬ࡷࡹࡀࠠࠨ࿛") + str(e))
    return bstack111111111l_opy_
def bstack11llll111l_opy_():
  try:
      import time
      from bstack_utils.constants import bstack1l1ll1l1ll_opy_, EVENTS
      from bstack_utils.helper import bstack1111ll1111_opy_, get_host_info, global_config
      from datetime import datetime
      from filelock import FileLock
      from bstack_utils.performance_tester import PerformanceTester
      PerformanceTester.bstack111l1ll1ll_opy_()
      bstack11l11llll1_opy_ = os.path.join(os.getcwd(), bstack1l1llll_opy_ (u"ࠧ࡭ࡱࡪࠫ࿜"), bstack1l1llll_opy_ (u"ࠨ࡭ࡨࡽ࠲ࡳࡥࡵࡴ࡬ࡧࡸ࠴ࡪࡴࡱࡱࠫ࿝"))
      data = None
      lock = FileLock(bstack11l11llll1_opy_+bstack1l1llll_opy_ (u"ࠤ࠱ࡰࡴࡩ࡫ࠣ࿞"), timeout=2)
      try:
          with lock:
              with open(bstack11l11llll1_opy_, bstack1l1llll_opy_ (u"ࠥࡶࠧ࿟"), encoding=bstack1l1llll_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥ࿠")) as file:
                  data = json.load(file)
      except Exception as e:
          logger.debug(bstack1l1llll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡴࡨࡥࡩࠦ࡫ࡦࡻࠣࡱࡪࡺࡲࡪࡥࡶࠤ࡫࡯࡬ࡦ࠼ࠣࡿࢂࠨ࿡").format(e))
          return
      if not data:
          return
      bstack1lllll111l1_opy_ = bstack11l11l111l_opy_(cli.config, [bstack1l1llll_opy_ (u"ࠨࡡࡱ࡫ࡶࠦ࿢"), bstack1l1llll_opy_ (u"ࠢࡦࡦࡶࡍࡳࡹࡴࡳࡷࡰࡩࡳࡺࡡࡵ࡫ࡲࡲࠧ࿣"), bstack1l1llll_opy_ (u"ࠣࡣࡳ࡭ࠧ࿤")], None)
      if bstack1lllll111l1_opy_:
          bstack1ll111l1ll_opy_ = bstack1l1llll_opy_ (u"ࠤࡾࢁ࠴ࡹࡥ࡯ࡦࡢࡷࡩࡱ࡟ࡦࡸࡨࡲࡹࡹࠢ࿥").format(bstack1lllll111l1_opy_.rstrip(bstack1l1llll_opy_ (u"ࠥ࠳ࠧ࿦")))
      else:
          bstack1ll111l1ll_opy_ = bstack1l1ll1l1ll_opy_
      def bstack1lll11ll1_opy_():
          try:
              config = {
                  bstack1l1llll_opy_ (u"ࠦ࡭࡫ࡡࡥࡧࡵࡷࠧ࿧"): {
                      bstack1l1llll_opy_ (u"ࠧࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠦ࿨"): bstack1l1llll_opy_ (u"ࠨࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠤ࿩"),
                  }
              }
              bstack1ll1l1l1ll_opy_ = datetime.utcnow()
              bstack1l1111ll_opy_ = bstack1ll1l1l1ll_opy_.strftime(bstack1l1llll_opy_ (u"࡛ࠢࠦ࠰ࠩࡲ࠳ࠥࡥࡖࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࠲ࠪ࡬ࠠࡖࡖࡆࠦ࿪"))
              test_id = os.environ.get(bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭࿫")) if os.environ.get(bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ࿬")) else global_config.get_property(bstack1l1llll_opy_ (u"ࠥࡷࡩࡱࡒࡶࡰࡌࡨࠧ࿭"))
              payload = {
                  bstack1l1llll_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠣ࿮"): bstack1l1llll_opy_ (u"ࠧࡹࡤ࡬ࡡࡨࡺࡪࡴࡴࡴࠤ࿯"),
                  bstack1l1llll_opy_ (u"ࠨࡤࡢࡶࡤࠦ࿰"): {
                      bstack1l1llll_opy_ (u"ࠢࡵࡧࡶࡸ࡭ࡻࡢࡠࡷࡸ࡭ࡩࠨ࿱"): test_id,
                      bstack1l1llll_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡥࡡࡧࡥࡾࠨ࿲"): bstack1l1111ll_opy_,
                      bstack1l1llll_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡰࡤࡱࡪࠨ࿳"): bstack1l1llll_opy_ (u"ࠥࡗࡉࡑࡆࡦࡣࡷࡹࡷ࡫ࡐࡦࡴࡩࡳࡷࡳࡡ࡯ࡥࡨࠦ࿴"),
                      bstack1l1llll_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢ࡮ࡸࡵ࡮ࠣ࿵"): {
                          bstack1l1llll_opy_ (u"ࠧࡳࡥࡢࡵࡸࡶࡪࡹࠢ࿶"): data,
                          bstack1l1llll_opy_ (u"ࠨࡳࡥ࡭ࡕࡹࡳࡏࡤࠣ࿷"): global_config.get_property(bstack1l1llll_opy_ (u"ࠢࡴࡦ࡮ࡖࡺࡴࡉࡥࠤ࿸"))
                      },
                      bstack1l1llll_opy_ (u"ࠣࡷࡶࡩࡷࡥࡤࡢࡶࡤࠦ࿹"): global_config.get_property(bstack1l1llll_opy_ (u"ࠤࡸࡷࡪࡸࡎࡢ࡯ࡨࠦ࿺")),
                      bstack1l1llll_opy_ (u"ࠥ࡬ࡴࡹࡴࡠ࡫ࡱࡪࡴࠨ࿻"): get_host_info()
                  }
              }
              response = bstack1111ll1111_opy_(bstack1l1llll_opy_ (u"ࠦࡕࡕࡓࡕࠤ࿼"), bstack1ll111l1ll_opy_, payload, config)
              if response.status_code >= 200 and response.status_code < 300:
                  logger.info(bstack1l1llll_opy_ (u"ࠧࡑࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵࠣࡷࡪࡴࡴࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡵࡱࠣࡿࢂࠨ࿽").format(bstack1ll111l1ll_opy_))
              else:
                  logger.debug(bstack1l1llll_opy_ (u"ࠨࡋࡦࡻࠣࡱࡪࡺࡲࡪࡥࡶࠤࡷ࡫ࡱࡶࡧࡶࡸࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪࠣࡷࡹࡧࡴࡶࡵࠣࡿࢂࠨ࿾").format(response.status_code))
          except Exception as e:
              logger.debug(bstack1l1llll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡴࡤࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࡀࠠࡼࡿࠥ࿿").format(e))
      bstack1lll11ll1_opy_()
  except Exception as e:
      logger.debug(bstack1l1llll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡴࡤࡠ࡭ࡨࡽࡤࡳࡥࡵࡴ࡬ࡧࡸࡀࠠࡼࡿࠥက").format(e))
def bstack1111l1111l_opy_(bstack1111ll1l11_opy_=False):
  bstack1ll111111l_opy_ = bstack1l1llll_opy_ (u"ࠤࠥခ")
  global bstack1lll111ll1_opy_
  global bstack1111ll11l_opy_
  global bstack1llllll11ll_opy_
  global bstack1lll1llll1_opy_
  global ROBOT_PYTHON_ERRORS
  global bstack1lll11l111l_opy_
  global CONFIG
  bstack11l11l1ll1_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠪࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡕࡔࡇࡇࠫဂ"))
  if bstack11l11l1ll1_opy_ not in [bstack1l1llll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬဃ")]:
    bstack1ll111111l_opy_ = PerformanceTester.mark_start(EVENTS.bstack1l1lll1l111_opy_)
  percy.shutdown()
  if bstack1lll111ll1_opy_:
    logger.warning(bstack1ll1lll11l1_opy_.format(str(bstack1lll111ll1_opy_)))
  else:
    try:
      bstack1lll111111l_opy_ = bstack1ll1ll1llll_opy_(bstack1l1llll_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫင"), logger)
      if bstack1lll111111l_opy_.get(bstack1l1llll_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫစ")) and bstack1lll111111l_opy_.get(bstack1l1llll_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬဆ")).get(bstack1l1llll_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪဇ")):
        logger.warning(bstack1ll1lll11l1_opy_.format(str(bstack1lll111111l_opy_[bstack1l1llll_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧဈ")][bstack1l1llll_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬဉ")])))
    except Exception as e:
      logger.error(e)
  if cli.is_running() and bstack11l11l1ll1_opy_ not in [bstack1l1llll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬည")]:
    if _11lllllll1_opy_ is not None:
      bstack1111ll1l11_opy_ = _11lllllll1_opy_
    else:
      bstack1111ll1l11_opy_ = cli.is_running()
    bstack111ll1l11_opy_.invoke(Events.bstack1l1l1111111_opy_)
  elif _11lllllll1_opy_ is not None:
    bstack1111ll1l11_opy_ = _11lllllll1_opy_
  logger.info(bstack1l1ll1lll11_opy_)
  global bstack1l11llll11_opy_
  if bstack1l11llll11_opy_:
    bstack11l1llllll_opy_()
  try:
    with bstack1l1111ll1l_opy_:
      bstack1ll11ll11l1_opy_ = bstack1111ll11l_opy_.copy()
    for driver in bstack1ll11ll11l1_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1l11lll1ll_opy_)
  ROBOT_PYTHON_ERRORS = []
  if bstack1lll11l111l_opy_ == bstack1l1llll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫဋ"):
    ROBOT_PYTHON_ERRORS = bstack1lll1lll1l_opy_(bstack1l1llll_opy_ (u"࠭ࡲࡰࡤࡲࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧဌ"))
  if bstack1lll11l111l_opy_ == bstack1l1llll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧဍ") and len(bstack1lll1llll1_opy_) == 0:
    bstack1lll1llll1_opy_ = bstack1lll1lll1l_opy_(bstack1l1llll_opy_ (u"ࠨࡲࡺࡣࡵࡿࡴࡦࡵࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ဎ"))
    if len(bstack1lll1llll1_opy_) == 0:
      bstack1lll1llll1_opy_ = bstack1lll1lll1l_opy_(bstack1l1llll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡳࡴࡵࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨဏ"))
  bstack1lll1ll11l1_opy_ = bstack1l1llll_opy_ (u"ࠪࠫတ")
  if len(bstack1llllll11ll_opy_) > 0:
    bstack1lll1ll11l1_opy_ = bstack1111l1lll1_opy_(bstack1llllll11ll_opy_)
  elif len(bstack1lll1llll1_opy_) > 0:
    bstack1lll1ll11l1_opy_ = bstack1111l1lll1_opy_(bstack1lll1llll1_opy_)
  elif len(ROBOT_PYTHON_ERRORS) > 0:
    bstack1lll1ll11l1_opy_ = bstack1111l1lll1_opy_(ROBOT_PYTHON_ERRORS)
  elif len(bstack1ll111l11ll_opy_) > 0:
    bstack1lll1ll11l1_opy_ = bstack1111l1lll1_opy_(bstack1ll111l11ll_opy_)
  if bstack11l11l1ll1_opy_ not in [bstack1l1llll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬထ")]:
    def bstack111l11ll1l_opy_():
      try:
        if bstack11l11l1ll1_opy_ in [bstack1l1llll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫဒ"), bstack1l1llll_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬဓ")]:
          bstack111l1l1l1l_opy_()
      except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩ࡭ࡳࡧ࡬ࡠࡧࡻࡩࡨࡻࡴࡪࡱࡱ࠾ࠥࢁࡽࠣန").format(e))
    def bstack1lll1l111l_opy_():
      try:
        if bool(bstack1lll1ll11l1_opy_):
          bstack11l1l1lll1_opy_(bstack1lll1ll11l1_opy_, bstack1111ll1l11_opy_=bstack1111ll1l11_opy_)
        else:
          bstack11l1l1lll1_opy_(bstack1111ll1l11_opy_=bstack1111ll1l11_opy_)
      except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡴࡧࡱࡨ࡮ࡴࡧࠡࡧࡹࡩࡳࡺ࠺ࠡࡽࢀࠦပ").format(e))
    def bstack1l1l11ll1ll_opy_():
      try:
        logger_utils.bstack1ll11111_opy_(CONFIG)
      except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡵࡨࡲࡩ࡯࡮ࡨࠢ࡯ࡳ࡬ࡹ࠺ࠡࡽࢀࠦဖ").format(e))
    bstack1l1l1l1llll_opy_ = threading.Thread(target=bstack111l11ll1l_opy_)
    bstack1lll1ll1lll_opy_ = threading.Thread(target=bstack1lll1l111l_opy_)
    bstack1l1ll11l11_opy_ = threading.Thread(target=bstack1l1l11ll1ll_opy_)
    threads = [bstack1l1l1l1llll_opy_, bstack1lll1ll1lll_opy_, bstack1l1ll11l11_opy_]
    for thread in threads:
      try:
        thread.start()
      except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡶࡸࡦࡸࡴࡪࡰࡪࠤࡹ࡮ࡲࡦࡣࡧࠤࢀࢃ࠺ࠡࡽࢀࠦဗ").format(thread.name, e))
    for thread in threads:
      try:
        thread.join()
      except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡮ࡴ࡯࡮ࡪࡰࡪࠤࡹ࡮ࡲࡦࡣࡧࠤࢀࢃ࠺ࠡࡽࢀࠦဘ").format(thread.name, e))
    bstack11llll11l1_opy_(bstack11l11lllll_opy_, logger)
    bstack11llll11l1_opy_(os.path.join(os.getcwd(), bstack1l1llll_opy_ (u"ࠬࡲ࡯ࡨࠩမ"), bstack1l1llll_opy_ (u"࠭࡫ࡦࡻ࠰ࡱࡪࡺࡲࡪࡥࡶ࠲࡯ࡹ࡯࡯ࠩယ")), logger)
  if bstack11l11l1ll1_opy_ not in [bstack1l1llll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨရ")]:
    try:
      from bstack_utils.helper import bstack11ll11lll1_opy_ as _111ll1l11l_opy_
      if _111ll1l11l_opy_():
        TestHubHandler.bstack1111111l_opy_()
    except Exception as _1l1l1l111ll_opy_:
      logger.debug(bstack1l1llll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡧ࡮ࡸࡷ࡭࡯࡮ࡨࠢࡗࡩࡸࡺࡈࡶࡤࠣࡵࡺ࡫ࡵࡦࠢࡲࡲࠥ࡫ࡸࡪࡶ࠽ࠤࢀࢃࠢလ").format(_1l1l1l111ll_opy_))
    PerformanceTester.end(EVENTS.bstack1l1lll1l111_opy_.value, bstack1ll111111l_opy_ + bstack1l1llll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤဝ"), bstack1ll111111l_opy_ + bstack1l1llll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣသ"), status=True, failure=None, test_name=None)
    bstack11llll111l_opy_()
    logger_utils.bstack1llll1l111_opy_()
    logging.shutdown()
  if len(ROBOT_PYTHON_ERRORS) > 0:
    sys.exit(len(ROBOT_PYTHON_ERRORS))
def bstack1111111ll1_opy_(bstack1l1l1lll111_opy_, frame):
  global global_config
  logger.error(bstack1ll111ll1l_opy_)
  global_config.bstack1ll11l111l_opy_(bstack1l1llll_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡓࡵࠧဟ"), bstack1l1l1lll111_opy_)
  if hasattr(signal, bstack1l1llll_opy_ (u"࡙ࠬࡩࡨࡰࡤࡰࡸ࠭ဠ")):
    global_config.bstack1ll11l111l_opy_(bstack1l1llll_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭အ"), signal.Signals(bstack1l1l1lll111_opy_).name)
  else:
    global_config.bstack1ll11l111l_opy_(bstack1l1llll_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡔ࡫ࡪࡲࡦࡲࠧဢ"), bstack1l1llll_opy_ (u"ࠨࡕࡌࡋ࡚ࡔࡋࡏࡑ࡚ࡒࠬဣ"))
  bstack1111ll1l11_opy_ = cli.is_running()
  if bstack1111ll1l11_opy_:
    bstack111ll1l11_opy_.invoke(Events.bstack1l1l1111111_opy_)
  bstack11l11l1ll1_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪဤ"))
  if bstack11l11l1ll1_opy_ == bstack1l1llll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪဥ") and not cli.is_enabled(CONFIG):
    TestHubHandler.stop(global_config.get_property(bstack1l1llll_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡘ࡯ࡧ࡯ࡣ࡯ࠫဦ")))
  bstack1111l1111l_opy_(bstack1111ll1l11_opy_)
  sys.exit(1)
def bstack1lll111lll_opy_(err):
  logger.critical(bstack111ll11l11_opy_.format(str(err)))
  bstack11l1l1lll1_opy_(bstack111ll11l11_opy_.format(str(err)), True)
  atexit.unregister(bstack1111l1111l_opy_)
  bstack111l1l1l1l_opy_()
  sys.exit(1)
def bstack1ll1l1lll1_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack11l1l1lll1_opy_(message, True)
  atexit.unregister(bstack1111l1111l_opy_)
  bstack111l1l1l1l_opy_()
  sys.exit(1)
def bstack111llll1ll_opy_():
  global CONFIG
  global bstack1111ll111_opy_
  global bstack1ll111lll1_opy_
  global BROWSERSTACK_AUTOMATION
  CONFIG = bstack1l11111111_opy_()
  load_dotenv(CONFIG.get(bstack1l1llll_opy_ (u"ࠬ࡫࡮ࡷࡈ࡬ࡰࡪ࠭ဧ")))
  bstack1lllll1ll11_opy_()
  bstack11lll11111_opy_()
  CONFIG = bstack1ll1l11ll1l_opy_(CONFIG)
  update(CONFIG, bstack1ll111lll1_opy_)
  update(CONFIG, bstack1111ll111_opy_)
  try:
    from bstack_utils.helper import configure_ca_environment
    configure_ca_environment(CONFIG)
  except Exception as _1ll1ll11l11_opy_:
    logger.debug(bstack1l1llll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡈࡧࡃࡦࡴࡷ࡭࡫࡯ࡣࡢࡶࡨ࠾ࠥ࡫࡮ࡷࠢࡶࡩࡹࡻࡰࠡࡵ࡮࡭ࡵࡶࡥࡥ࠼ࠣࡿࢂ࠭ဨ").format(_1ll1ll11l11_opy_))
  if bstack1l1llll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫဩ") in bstack1111ll111_opy_:
    CONFIG[bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪဪ")] = bstack1111ll111_opy_[bstack1l1llll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ါ")]
    os.environ[bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭ာ")] = str(bstack1111ll111_opy_[bstack1l1llll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨိ")])
  elif bstack1l1llll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩီ") in bstack1ll111lll1_opy_:
    CONFIG[bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨု")] = bstack1ll111lll1_opy_[bstack1l1llll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫူ")]
  if not cli.is_enabled(CONFIG):
    CONFIG = bstack1111l1lll_opy_(CONFIG)
  BROWSERSTACK_AUTOMATION = bstack111l11l11l_opy_(CONFIG)
  os.environ[bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫေ")] = BROWSERSTACK_AUTOMATION.__str__().lower()
  global_config.bstack1ll11l111l_opy_(bstack1l1llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪဲ"), BROWSERSTACK_AUTOMATION)
  if (bstack1l1llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ဳ") in CONFIG and bstack1l1llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧဴ") in bstack1111ll111_opy_) or (
          bstack1l1llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨဵ") in CONFIG and bstack1l1llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩံ") not in bstack1ll111lll1_opy_):
    if os.getenv(bstack1l1llll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇ့ࠫ")):
      CONFIG[bstack1l1llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪး")] = os.getenv(bstack1l1llll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ္࠭"))
    else:
      if not CONFIG.get(bstack1l1llll_opy_ (u"ࠥࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠨ်"), bstack1l1llll_opy_ (u"ࠦࠧျ")) in bstack1l111lll11_opy_:
        bstack1l1ll1llll1_opy_()
  elif (bstack1l1llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨြ") not in CONFIG and bstack1l1llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨွ") in CONFIG) or (
          bstack1l1llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪှ") in bstack1ll111lll1_opy_ and bstack1l1llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫဿ") not in bstack1111ll111_opy_):
    del (CONFIG[bstack1l1llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ၀")])
  if bstack1111l1l1ll_opy_(CONFIG):
    bstack1lll111lll_opy_(bstack1ll1ll1l11_opy_)
  Config.bstack1lll1l11_opy_().bstack1ll11l111l_opy_(bstack1l1llll_opy_ (u"ࠥࡹࡸ࡫ࡲࡏࡣࡰࡩࠧ၁"), CONFIG[bstack1l1llll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭၂")])
  bstack1ll1l1l111l_opy_()
  bstack1ll11ll1lll_opy_()
  if bstack11ll111lll_opy_ and not CONFIG.get(bstack1l1llll_opy_ (u"ࠧ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠣ၃"), bstack1l1llll_opy_ (u"ࠨࠢ၄")) in bstack1l111lll11_opy_:
    CONFIG[bstack1l1llll_opy_ (u"ࠧࡢࡲࡳࠫ၅")] = bstack1llllll111_opy_(CONFIG)
    logger.info(bstack1l1l1lll1l_opy_.format(CONFIG[bstack1l1llll_opy_ (u"ࠨࡣࡳࡴࠬ၆")]))
  if not BROWSERSTACK_AUTOMATION:
    CONFIG[bstack1l1llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ၇")] = [{}]
  try:
    from bstack_utils.helper import bstack11lll1l1l1_opy_
    if not os.environ.get(bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡑࡎࡄࡒࡤࡏࡄࠨ၈")):
      bstack1llll111ll_opy_ = bstack11lll1l1l1_opy_(CONFIG)
      if bstack1llll111ll_opy_:
        os.environ[bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡒࡏࡅࡓࡥࡉࡅࠩ၉")] = bstack1llll111ll_opy_
  except Exception as _1ll11ll111_opy_:
    logger.debug(bstack1l1llll_opy_ (u"ࠬࡺࡥࡴࡶࠣࡴࡱࡧ࡮ࠡ࡫ࡧࠤࡪࡴࡶࠡࡧࡻࡴࡴࡸࡴࠡࡵ࡮࡭ࡵࡶࡥࡥ࠼ࠣࡿࢂ࠭၊").format(_1ll11ll111_opy_))
def bstack1l1lll1111l_opy_(config, bstack1ll1111l1l1_opy_):
  global CONFIG
  global bstack11ll111lll_opy_
  CONFIG = config
  bstack11ll111lll_opy_ = bstack1ll1111l1l1_opy_
  try:
    from bstack_utils.helper import configure_ca_environment
    configure_ca_environment(CONFIG)
  except Exception as _1ll1ll11l11_opy_:
    logger.debug(bstack1l1llll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡈࡧࡃࡦࡴࡷ࡭࡫࡯ࡣࡢࡶࡨ࠾ࠥࡽ࡯ࡳ࡭ࡨࡶࠥ࡫࡮ࡷࠢࡶࡩࡹࡻࡰࠡࡵ࡮࡭ࡵࡶࡥࡥ࠼ࠣࡿࢂ࠭။").format(_1ll1ll11l11_opy_))
def bstack1ll11ll1lll_opy_():
  global CONFIG
  global bstack11ll111lll_opy_
  if bstack1l1llll_opy_ (u"ࠧࡢࡲࡳࠫ၌") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1ll1l1lll1_opy_(e, bstack1l1llll1111_opy_)
    bstack11ll111lll_opy_ = True
    global_config.bstack1ll11l111l_opy_(bstack1l1llll_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ၍"), True)
def bstack1llllll111_opy_(config):
  bstack1llll111ll1_opy_ = bstack1l1llll_opy_ (u"ࠩࠪ၎")
  app = config[bstack1l1llll_opy_ (u"ࠪࡥࡵࡶࠧ၏")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1ll11lll111_opy_:
      if os.path.exists(app):
        bstack1llll111ll1_opy_ = bstack1lll1111l11_opy_(config, app)
      elif bstack1lll11ll11_opy_(app):
        bstack1llll111ll1_opy_ = app
      else:
        bstack1lll111lll_opy_(bstack1llll11lll1_opy_.format(app))
    else:
      if bstack1lll11ll11_opy_(app):
        bstack1llll111ll1_opy_ = app
      elif os.path.exists(app):
        bstack1llll111ll1_opy_ = bstack1lll1111l11_opy_(app)
      else:
        bstack1lll111lll_opy_(bstack11lllll11l_opy_)
  else:
    if len(app) > 2:
      bstack1lll111lll_opy_(bstack1l1llll11l1_opy_)
    elif len(app) == 2:
      if bstack1l1llll_opy_ (u"ࠫࡵࡧࡴࡩࠩၐ") in app and bstack1l1llll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨၑ") in app:
        if os.path.exists(app[bstack1l1llll_opy_ (u"࠭ࡰࡢࡶ࡫ࠫၒ")]):
          bstack1llll111ll1_opy_ = bstack1lll1111l11_opy_(config, app[bstack1l1llll_opy_ (u"ࠧࡱࡣࡷ࡬ࠬၓ")], app[bstack1l1llll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫၔ")])
        else:
          bstack1lll111lll_opy_(bstack1llll11lll1_opy_.format(app))
      else:
        bstack1lll111lll_opy_(bstack1l1llll11l1_opy_)
    else:
      for key in app:
        if key in bstack1l1l1l1ll11_opy_:
          if key == bstack1l1llll_opy_ (u"ࠩࡳࡥࡹ࡮ࠧၕ"):
            if os.path.exists(app[key]):
              bstack1llll111ll1_opy_ = bstack1lll1111l11_opy_(config, app[key])
            else:
              bstack1lll111lll_opy_(bstack1llll11lll1_opy_.format(app))
          else:
            bstack1llll111ll1_opy_ = app[key]
        else:
          bstack1lll111lll_opy_(bstack1l1l11l1l1_opy_)
  return bstack1llll111ll1_opy_
def bstack1lll11ll11_opy_(bstack1llll111ll1_opy_):
  import re
  bstack1l1l111111l_opy_ = re.compile(bstack1l1llll_opy_ (u"ࡵࠦࡣࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫࠦࠥၖ"))
  bstack1l111l1l1l_opy_ = re.compile(bstack1l1llll_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬ࠲࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰ࠤࠣၗ"))
  if bstack1l1llll_opy_ (u"ࠬࡨࡳ࠻࠱࠲ࠫၘ") in bstack1llll111ll1_opy_ or re.fullmatch(bstack1l1l111111l_opy_, bstack1llll111ll1_opy_) or re.fullmatch(bstack1l111l1l1l_opy_, bstack1llll111ll1_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack1lll1lllll1_opy_, stage=STAGE.SINGLE, bstack11lllll111_opy_=SESSION_NAME)
def bstack1lll1111l11_opy_(config, path, bstack1l1llllll1l_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1l1llll_opy_ (u"࠭ࡲࡣࠩၙ")).read()).hexdigest()
  bstack1l1l1lllll1_opy_ = bstack1lll1l111ll_opy_(md5_hash)
  bstack1llll111ll1_opy_ = None
  if bstack1l1l1lllll1_opy_:
    logger.info(bstack1l1l1lll11_opy_.format(bstack1l1l1lllll1_opy_, md5_hash))
    return bstack1l1l1lllll1_opy_
  time_start = datetime.datetime.now()
  multipart_data = MultipartEncoder(
    fields={
      bstack1l1llll_opy_ (u"ࠧࡧ࡫࡯ࡩࠬၚ"): (os.path.basename(path), open(os.path.abspath(path), bstack1l1llll_opy_ (u"ࠨࡴࡥࠫၛ")), bstack1l1llll_opy_ (u"ࠩࡷࡩࡽࡺ࠯ࡱ࡮ࡤ࡭ࡳ࠭ၜ")),
      bstack1l1llll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ၝ"): bstack1l1llllll1l_opy_
    }
  )
  from bstack_utils.helper import get_ca_cert_path
  bstack1l11l1ll11_opy_ = {
    bstack1l1llll_opy_ (u"ࠫࡩࡧࡴࡢࠩၞ"): multipart_data,
    bstack1l1llll_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ၟ"): {bstack1l1llll_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬၠ"): multipart_data.content_type},
    bstack1l1llll_opy_ (u"ࠧࡢࡷࡷ࡬ࠬၡ"): (config[bstack1l1llll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪၢ")], config[bstack1l1llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬၣ")]),
  }
  cert_path = get_ca_cert_path(config)
  if cert_path:
    bstack1l11l1ll11_opy_[bstack1l1llll_opy_ (u"ࠪࡺࡪࡸࡩࡧࡻࠪၤ")] = cert_path
  response = requests.post(bstack1ll111l11l1_opy_, **bstack1l11l1ll11_opy_)
  try:
    res = json.loads(response.text)
    bstack1llll111ll1_opy_ = res[bstack1l1llll_opy_ (u"ࠫࡦࡶࡰࡠࡷࡵࡰࠬၥ")]
    logger.info(bstack1ll1l1l11l1_opy_.format(bstack1llll111ll1_opy_))
    bstack1l1l1ll1l1_opy_(md5_hash, bstack1llll111ll1_opy_)
    cli.add_benchmark(bstack1l1llll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽ࡹࡵࡲ࡯ࡢࡦࡢࡥࡵࡶࠢၦ"), datetime.datetime.now() - time_start)
  except ValueError as err:
    bstack1lll111lll_opy_(bstack1l1111l1l1_opy_.format(str(err)))
  return bstack1llll111ll1_opy_
def bstack1ll1l1l111l_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack1l1lll1lll_opy_
  bstack1ll11ll1_opy_ = 1
  bstack1111l111l_opy_ = 1
  if bstack1l1llll_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ၧ") in CONFIG:
    bstack1111l111l_opy_ = CONFIG[bstack1l1llll_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧၨ")]
  else:
    bstack1111l111l_opy_ = bstack111111lll_opy_(framework_name, args) or 1
  if bstack1l1llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫၩ") in CONFIG:
    bstack1ll11ll1_opy_ = len(CONFIG[bstack1l1llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬၪ")])
  bstack1l1lll1lll_opy_ = int(bstack1111l111l_opy_) * int(bstack1ll11ll1_opy_)
def bstack111111lll_opy_(framework_name, args):
  if framework_name == bstack1ll1ll1ll1l_opy_ and args and bstack1l1llll_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨၫ") in args:
      bstack1l1l11111ll_opy_ = args.index(bstack1l1llll_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩၬ"))
      return int(args[bstack1l1l11111ll_opy_ + 1]) or 1
  return 1
def bstack1lll1l111ll_opy_(md5_hash):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l1llll_opy_ (u"ࠬ࡬ࡩ࡭ࡧ࡯ࡳࡨࡱࠠ࡯ࡱࡷࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠬࠡࡷࡶ࡭ࡳ࡭ࠠࡣࡣࡶ࡭ࡨࠦࡦࡪ࡮ࡨࠤࡴࡶࡥࡳࡣࡷ࡭ࡴࡴࡳࠨၭ"))
    bstack1ll1ll1l1l1_opy_ = os.path.join(os.path.expanduser(bstack1l1llll_opy_ (u"࠭ࡾࠨၮ")), bstack1l1llll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧၯ"), bstack1l1llll_opy_ (u"ࠨࡣࡳࡴ࡚ࡶ࡬ࡰࡣࡧࡑࡉ࠻ࡈࡢࡵ࡫࠲࡯ࡹ࡯࡯ࠩၰ"))
    if os.path.exists(bstack1ll1ll1l1l1_opy_):
      try:
        bstack11ll1l11ll_opy_ = json.load(open(bstack1ll1ll1l1l1_opy_, bstack1l1llll_opy_ (u"ࠩࡵࡦࠬၱ")))
        if md5_hash in bstack11ll1l11ll_opy_:
          bstack1ll1l11l11l_opy_ = bstack11ll1l11ll_opy_[md5_hash]
          bstack1ll1l1111ll_opy_ = datetime.datetime.now()
          bstack1llll11lll_opy_ = datetime.datetime.strptime(bstack1ll1l11l11l_opy_[bstack1l1llll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ၲ")], bstack1l1llll_opy_ (u"ࠫࠪࡪ࠯ࠦ࡯࠲ࠩ࡞ࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨၳ"))
          if (bstack1ll1l1111ll_opy_ - bstack1llll11lll_opy_).days > 30:
            return None
          elif version.parse(str(__version__)) > version.parse(bstack1ll1l11l11l_opy_[bstack1l1llll_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪၴ")]):
            return None
          return bstack1ll1l11l11l_opy_[bstack1l1llll_opy_ (u"࠭ࡩࡥࠩၵ")]
      except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡲࡦࡣࡧ࡭ࡳ࡭ࠠࡎࡆ࠸ࠤ࡭ࡧࡳࡩࠢࡩ࡭ࡱ࡫࠺ࠡࡽࢀࠫၶ").format(str(e)))
    return None
  bstack1ll1ll1l1l1_opy_ = os.path.join(os.path.expanduser(bstack1l1llll_opy_ (u"ࠨࢀࠪၷ")), bstack1l1llll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩၸ"), bstack1l1llll_opy_ (u"ࠪࡥࡵࡶࡕࡱ࡮ࡲࡥࡩࡓࡄ࠶ࡊࡤࡷ࡭࠴ࡪࡴࡱࡱࠫၹ"))
  lock_file = bstack1ll1ll1l1l1_opy_ + bstack1l1llll_opy_ (u"ࠫ࠳ࡲ࡯ࡤ࡭ࠪၺ")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack1ll1ll1l1l1_opy_):
        with open(bstack1ll1ll1l1l1_opy_, bstack1l1llll_opy_ (u"ࠬࡸࠧၻ")) as f:
          content = f.read().strip()
          if content:
            bstack11ll1l11ll_opy_ = json.loads(content)
            if md5_hash in bstack11ll1l11ll_opy_:
              bstack1ll1l11l11l_opy_ = bstack11ll1l11ll_opy_[md5_hash]
              bstack1ll1l1111ll_opy_ = datetime.datetime.now()
              bstack1llll11lll_opy_ = datetime.datetime.strptime(bstack1ll1l11l11l_opy_[bstack1l1llll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩၼ")], bstack1l1llll_opy_ (u"ࠧࠦࡦ࠲ࠩࡲ࠵࡚ࠥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫၽ"))
              if (bstack1ll1l1111ll_opy_ - bstack1llll11lll_opy_).days > 30:
                return None
              elif version.parse(str(__version__)) > version.parse(bstack1ll1l11l11l_opy_[bstack1l1llll_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ၾ")]):
                return None
              return bstack1ll1l11l11l_opy_[bstack1l1llll_opy_ (u"ࠩ࡬ࡨࠬၿ")]
      return None
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡺ࡭ࡹ࡮ࠠࡧ࡫࡯ࡩࠥࡲ࡯ࡤ࡭࡬ࡲ࡬ࠦࡦࡰࡴࠣࡑࡉ࠻ࠠࡩࡣࡶ࡬࠿ࠦࡻࡾࠩႀ").format(str(e)))
    return None
def bstack1l1l1ll1l1_opy_(md5_hash, bstack1llll111ll1_opy_):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l1llll_opy_ (u"ࠫ࡫࡯࡬ࡦ࡮ࡲࡧࡰࠦ࡮ࡰࡶࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪ࠲ࠠࡶࡵ࡬ࡲ࡬ࠦࡢࡢࡵ࡬ࡧࠥ࡬ࡩ࡭ࡧࠣࡳࡵ࡫ࡲࡢࡶ࡬ࡳࡳࡹࠧႁ"))
    bstack111lll111l_opy_ = os.path.join(os.path.expanduser(bstack1l1llll_opy_ (u"ࠬࢄࠧႂ")), bstack1l1llll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ႃ"))
    if not os.path.exists(bstack111lll111l_opy_):
      os.makedirs(bstack111lll111l_opy_)
    bstack1ll1ll1l1l1_opy_ = os.path.join(os.path.expanduser(bstack1l1llll_opy_ (u"ࠧࡿࠩႄ")), bstack1l1llll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨႅ"), bstack1l1llll_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪႆ"))
    bstack1ll11ll1l11_opy_ = {
      bstack1l1llll_opy_ (u"ࠪ࡭ࡩ࠭ႇ"): bstack1llll111ll1_opy_,
      bstack1l1llll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧႈ"): datetime.datetime.strftime(datetime.datetime.now(), bstack1l1llll_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩႉ")),
      bstack1l1llll_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫႊ"): str(__version__)
    }
    try:
      bstack11ll1l11ll_opy_ = {}
      if os.path.exists(bstack1ll1ll1l1l1_opy_):
        bstack11ll1l11ll_opy_ = json.load(open(bstack1ll1ll1l1l1_opy_, bstack1l1llll_opy_ (u"ࠧࡳࡤࠪႋ")))
      bstack11ll1l11ll_opy_[md5_hash] = bstack1ll11ll1l11_opy_
      with open(bstack1ll1ll1l1l1_opy_, bstack1l1llll_opy_ (u"ࠣࡹ࠮ࠦႌ")) as outfile:
        json.dump(bstack11ll1l11ll_opy_, outfile)
    except Exception as e:
      logger.debug(bstack1l1llll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡷࡳࡨࡦࡺࡩ࡯ࡩࠣࡑࡉ࠻ࠠࡩࡣࡶ࡬ࠥ࡬ࡩ࡭ࡧ࠽ࠤࢀࢃႍࠧ").format(str(e)))
    return
  bstack111lll111l_opy_ = os.path.join(os.path.expanduser(bstack1l1llll_opy_ (u"ࠪࢂࠬႎ")), bstack1l1llll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫႏ"))
  if not os.path.exists(bstack111lll111l_opy_):
    os.makedirs(bstack111lll111l_opy_)
  bstack1ll1ll1l1l1_opy_ = os.path.join(os.path.expanduser(bstack1l1llll_opy_ (u"ࠬࢄࠧ႐")), bstack1l1llll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭႑"), bstack1l1llll_opy_ (u"ࠧࡢࡲࡳ࡙ࡵࡲ࡯ࡢࡦࡐࡈ࠺ࡎࡡࡴࡪ࠱࡮ࡸࡵ࡮ࠨ႒"))
  lock_file = bstack1ll1ll1l1l1_opy_ + bstack1l1llll_opy_ (u"ࠨ࠰࡯ࡳࡨࡱࠧ႓")
  bstack1ll11ll1l11_opy_ = {
    bstack1l1llll_opy_ (u"ࠩ࡬ࡨࠬ႔"): bstack1llll111ll1_opy_,
    bstack1l1llll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭႕"): datetime.datetime.strftime(datetime.datetime.now(), bstack1l1llll_opy_ (u"ࠫࠪࡪ࠯ࠦ࡯࠲ࠩ࡞ࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨ႖")),
    bstack1l1llll_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ႗"): str(__version__)
  }
  try:
    with FileLock(lock_file, timeout=10):
      bstack11ll1l11ll_opy_ = {}
      if os.path.exists(bstack1ll1ll1l1l1_opy_):
        with open(bstack1ll1ll1l1l1_opy_, bstack1l1llll_opy_ (u"࠭ࡲࠨ႘")) as f:
          content = f.read().strip()
          if content:
            bstack11ll1l11ll_opy_ = json.loads(content)
      bstack11ll1l11ll_opy_[md5_hash] = bstack1ll11ll1l11_opy_
      with open(bstack1ll1ll1l1l1_opy_, bstack1l1llll_opy_ (u"ࠢࡸࠤ႙")) as outfile:
        json.dump(bstack11ll1l11ll_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡸ࡫ࡷ࡬ࠥ࡬ࡩ࡭ࡧࠣࡰࡴࡩ࡫ࡪࡰࡪࠤ࡫ࡵࡲࠡࡏࡇ࠹ࠥ࡮ࡡࡴࡪࠣࡹࡵࡪࡡࡵࡧ࠽ࠤࢀࢃࠧႚ").format(str(e)))
def bstack1ll11llll11_opy_(self):
  return
def bstack1ll11l1l1l_opy_(self):
  return
def bstack1lll1lll111_opy_():
  global bstack1l1l1l11l1_opy_
  bstack1l1l1l11l1_opy_ = True
def bstack11lll1l111_opy_(self):
  global FRAMEWORK_NAME
  global bstack11llll1l11_opy_
  global bstack1lllll11111_opy_
  random_label = PerformanceTester.mark_start(EVENTS.bstack1llllll1ll1_opy_)
  try:
    if bstack1l1llll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩႛ") in FRAMEWORK_NAME and self.session_id != None and bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧႜ"), bstack1l1llll_opy_ (u"ࠫࠬႝ")) != bstack1l1llll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭႞"):
      bstack111llll1l1_opy_ = bstack1l1llll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭႟") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1l1llll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧႠ")
      if bstack111llll1l1_opy_ == bstack1l1llll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨႡ"):
        bstack11l1ll11ll_opy_(logger)
      if self != None:
        bstack1l1lll1ll1l_opy_(self, bstack111llll1l1_opy_, bstack1l1llll_opy_ (u"ࠩ࠯ࠤࠬႢ").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack1l1llll_opy_ (u"ࠪࠫႣ")
    if bstack1l1llll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫႤ") in FRAMEWORK_NAME and getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫႥ"), None):
      bstack11llll11l_opy_.bstack11l1ll111_opy_(self, bstack1ll1ll11111_opy_, logger, wait=True)
    if bstack1l1llll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭Ⴆ") in FRAMEWORK_NAME:
      bstack111ll1l111_opy_.bstack1l1ll1l11ll_opy_(self)
    PerformanceTester.end(EVENTS.bstack1llllll1ll1_opy_.value, random_label + bstack1l1llll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢႧ"), random_label + bstack1l1llll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨႨ"), status=True, failure=None, test_name=None)
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࠥႩ") + str(e))
    PerformanceTester.end(EVENTS.bstack1llllll1ll1_opy_.value, random_label + bstack1l1llll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥႪ"), random_label + bstack1l1llll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤႫ"), status=False, failure=str(e), test_name=None)
  bstack1lllll11111_opy_(self)
  self.session_id = None
def bstack1ll1lll11ll_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack1ll11ll1l1_opy_
    global FRAMEWORK_NAME
    command_executor = kwargs.get(bstack1l1llll_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠨႬ"), bstack1l1llll_opy_ (u"࠭ࠧႭ"))
    bstack1llllll1l11_opy_ = False
    if type(command_executor) == str and bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪႮ") in command_executor:
      bstack1llllll1l11_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫႯ") in str(getattr(command_executor, bstack1l1llll_opy_ (u"ࠩࡢࡹࡷࡲࠧႰ"), bstack1l1llll_opy_ (u"ࠪࠫႱ"))):
      bstack1llllll1l11_opy_ = True
    else:
      kwargs = a11y.bstack1l1l1l11ll_opy_(bstack1ll1l11ll11_opy_=kwargs, config=CONFIG)
      return bstack1l1l1l111l1_opy_(self, *args, **kwargs)
    if bstack1llllll1l11_opy_:
      bstack1l1l111lll_opy_ = TestHubUtils.bstack1l11111lll_opy_(CONFIG, FRAMEWORK_NAME)
      if kwargs.get(bstack1l1llll_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬႲ")):
        kwargs[bstack1l1llll_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭Ⴓ")] = bstack1ll11ll1l1_opy_(kwargs[bstack1l1llll_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧႴ")], FRAMEWORK_NAME, CONFIG, bstack1l1l111lll_opy_)
      elif kwargs.get(bstack1l1llll_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧႵ")):
        kwargs[bstack1l1llll_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨႶ")] = bstack1ll11ll1l1_opy_(kwargs[bstack1l1llll_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩႷ")], FRAMEWORK_NAME, CONFIG, bstack1l1l111lll_opy_)
  except Exception as e:
    logger.error(bstack1l1llll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡘࡊࡋࠡࡥࡤࡴࡸࡀࠠࡼࡿࠥႸ").format(str(e)))
  return bstack1l1l1l111l1_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack1ll1llll1ll_opy_, stage=STAGE.SINGLE, bstack11lllll111_opy_=SESSION_NAME, bstack1ll1111ll1_opy_=True)
def bstack1lll11llll_opy_(self, command_executor=bstack1l1llll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳࠶࠸࠷࠯࠲࠱࠴࠳࠷࠺࠵࠶࠷࠸ࠧႹ"), *args, **kwargs):
  global bstack11llll1l11_opy_
  global bstack1111ll11l_opy_
  bstack111111l1ll_opy_ = bstack1ll1lll11ll_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack1ll111ll_opy_.on():
    return bstack111111l1ll_opy_
  try:
    if isinstance(command_executor, (str, bytes)):
      bstack11l1lll11l_opy_ = str(command_executor)
    else:
      bstack11l1lll11l_opy_ = str(
        getattr(command_executor, bstack1l1llll_opy_ (u"ࠬࡥࡵࡳ࡮ࠪႺ"), None)
        or getattr(getattr(command_executor, bstack1l1llll_opy_ (u"࠭࡟ࡤ࡮࡬ࡩࡳࡺ࡟ࡤࡱࡱࡪ࡮࡭ࠧႻ"), None), bstack1l1llll_opy_ (u"ࠧࡳࡧࡰࡳࡹ࡫࡟ࡴࡧࡵࡺࡪࡸ࡟ࡢࡦࡧࡶࠬႼ"), None)
        or bstack1l1llll_opy_ (u"ࠨࠩႽ")
      )
    logger.debug(bstack1l1llll_opy_ (u"ࠩࡋࡹࡧࠦࡕࡓࡎࠣ࡭ࡸࠦ࠭ࠡࡽࢀࠫႾ").format(bstack11l1lll11l_opy_.split(bstack1l1llll_opy_ (u"ࠪࡄࠬႿ"))[-1] if bstack1l1llll_opy_ (u"ࠫࡅ࠭Ⴠ") in bstack11l1lll11l_opy_ else bstack11l1lll11l_opy_))
    if bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨჁ") in bstack11l1lll11l_opy_:
      global_config.bstack1ll11l111l_opy_(bstack1l1llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧჂ"), True)
  except Exception as e:
    logger.error(bstack1l1llll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡩࡨࡦࡥ࡮࡭ࡳ࡭ࠠࡤࡱࡰࡱࡦࡴࡤࠡࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧჃ").format(str(e)))
    pass
  if (isinstance(command_executor, str) and bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫჄ") in command_executor):
    global_config.bstack1ll11l111l_opy_(bstack1l1llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪჅ"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack111l1ll1l1_opy_ = getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡗࡩࡸࡺࡍࡦࡶࡤࠫ჆"), None)
  bstack1111l111ll_opy_ = {}
  if self.capabilities is not None:
    bstack1111l111ll_opy_[bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧࠪჇ")] = self.capabilities.get(bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ჈"))
    bstack1111l111ll_opy_[bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ჉")] = self.capabilities.get(bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ჊"))
    bstack1111l111ll_opy_[bstack1l1llll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡠࡱࡳࡸ࡮ࡵ࡮ࡴࠩ჋")] = self.capabilities.get(bstack1l1llll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ჌"))
  if CONFIG.get(bstack1l1llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪჍ"), False) and a11y.bstack1l1lll111l1_opy_(bstack1111l111ll_opy_):
    threading.current_thread().a11yPlatform = True
  if bstack1l1llll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ჎") in FRAMEWORK_NAME or bstack1l1llll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ჏") in FRAMEWORK_NAME:
    TestHubHandler.send_cbt_info(self)
  if bstack1l1llll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ა") in FRAMEWORK_NAME and bstack111l1ll1l1_opy_ and bstack111l1ll1l1_opy_.get(bstack1l1llll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧბ"), bstack1l1llll_opy_ (u"ࠨࠩგ")) == bstack1l1llll_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪდ"):
    TestHubHandler.send_cbt_info(self)
  bstack11llll1l11_opy_ = self.session_id
  with bstack1l1111ll1l_opy_:
    bstack1111ll11l_opy_.append(self)
  return bstack111111l1ll_opy_
def bstack1l11l1l1ll_opy_(args):
  return bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵࠫე") in str(args)
def bstack1ll1llll1l_opy_(self, driver_command, *args, **kwargs):
  global bstack1l1l111l11l_opy_
  global bstack11lll1llll_opy_
  bstack111ll1l1ll_opy_ = bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨვ"), None) and bstack11llll11_opy_(
          threading.current_thread(), bstack1l1llll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫზ"), None)
  bstack1ll1111111_opy_ = bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭თ"), None) and bstack11llll11_opy_(
          threading.current_thread(), bstack1l1llll_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩი"), None)
  bstack1111llll1_opy_ = getattr(self, bstack1l1llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨკ"), None) != None and getattr(self, bstack1l1llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩლ"), None) == True
  bstack1lllll11l1_opy_ = str(FRAMEWORK_NAME).lower()
  bstack1l111l1l11_opy_ = not bstack11lll1llll_opy_ and bstack1l1llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪმ") in CONFIG and CONFIG[bstack1l1llll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫნ")] == True and accessibility_scripts.bstack1ll111ll1l1_opy_(driver_command) and (bstack1111llll1_opy_ or bstack111ll1l1ll_opy_ or bstack1ll1111111_opy_) and not bstack1l11l1l1ll_opy_(args)
  if bstack1l1llll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨ࠭ო") in bstack1lllll11l1_opy_:
    bstack1111ll1ll1_opy_ = a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX)
    bstack1l111l1l11_opy_ =  not bstack11lll1llll_opy_ and bstack1111ll1ll1_opy_ and accessibility_scripts.bstack1ll111ll1l1_opy_(driver_command) and (bstack1111llll1_opy_ or bstack111ll1l1ll_opy_ or bstack1ll1111111_opy_) and not bstack1l11l1l1ll_opy_(args)
  if bstack1l111l1l11_opy_:
    try:
      bstack11lll1llll_opy_ = True
      logger.debug(bstack1l1llll_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡨࡲࡶࠥࢁࡽࠨპ").format(driver_command))
      bstack1l1l11l11l1_opy_ = perform_scan(self, driver_command=driver_command)
      logger.debug(bstack1l1l11l11l1_opy_)
      try:
        log_data = {
          bstack1l1llll_opy_ (u"ࠢࡳࡧࡴࡹࡪࡹࡴࠣჟ"): {
            bstack1l1llll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤრ"): bstack1l1llll_opy_ (u"ࠤࡄ࠵࠶࡟࡟ࡔࡅࡄࡒࠧს"),
            bstack1l1llll_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡧࡷࡩࡷࡹࠢტ"): [
              {
                bstack1l1llll_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦუ"): driver_command
              }
            ]
          },
          bstack1l1llll_opy_ (u"ࠧࡸࡥࡴࡲࡲࡲࡸ࡫ࠢფ"): {
            bstack1l1llll_opy_ (u"ࠨࡢࡰࡦࡼࠦქ"): {
              bstack1l1llll_opy_ (u"ࠢ࡮ࡵࡪࠦღ"): bstack1l1l11l11l1_opy_.get(bstack1l1llll_opy_ (u"ࠣ࡯ࡶ࡫ࠧყ"), bstack1l1llll_opy_ (u"ࠤࠥშ")) if isinstance(bstack1l1l11l11l1_opy_, dict) else bstack1l1llll_opy_ (u"ࠥࠦჩ"),
              bstack1l1llll_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧც"): bstack1l1l11l11l1_opy_.get(bstack1l1llll_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨძ"), True) if isinstance(bstack1l1l11l11l1_opy_, dict) else True
            }
          }
        }
        logger.debug(bstack1l1llll_opy_ (u"࠭ࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡤࡣࡱࠤࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡ࡮ࡲ࡫ࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠧწ").format(log_data))
        automation_logger.info(json.dumps(log_data, separators=(bstack1l1llll_opy_ (u"ࠧ࠭ࠩჭ"), bstack1l1llll_opy_ (u"ࠨ࠼ࠪხ"))))
      except Exception as bstack1ll1111ll1l_opy_:
        logger.debug(bstack1l1llll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡲ࡯ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡧࡦࡴࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠩჯ").format(str(bstack1ll1111ll1l_opy_)))
    except Exception as err:
      logger.debug(bstack1l1llll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡦࡴࡩࡳࡷࡳࠠࡴࡥࡤࡲࠥࢁࡽࠨჰ").format(str(err)))
    bstack11lll1llll_opy_ = False
  response = bstack1l1l111l11l_opy_(self, driver_command, *args, **kwargs)
  bstack1ll1111lll_opy_ = (
    (bstack1l1llll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪჱ") in bstack1lllll11l1_opy_ or bstack1l1llll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬჲ") in bstack1lllll11l1_opy_) and bstack1ll111ll_opy_.on()
  ) or (bstack1l1llll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡧࡦࡰࡨࡶ࡮ࡩࠧჳ") in bstack1lllll11l1_opy_)
  if bstack1ll1111lll_opy_:
    try:
      if driver_command == bstack1l1llll_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫჴ"):
        test_run_uuid = TestHubHandler.current_test_uuid()
        if not test_run_uuid:
          test_run_uuid = bstack1ll111ll_opy_.current_hook_uuid()
        if not test_run_uuid and bstack1l1llll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩჵ") in bstack1lllll11l1_opy_:
          test_run_uuid = getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ჶ"), None)
        if test_run_uuid:
          bstack11ll1ll1ll_opy_ = response.get(bstack1l1llll_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩჷ"), None) if isinstance(response, dict) else None
          if bstack11ll1ll1ll_opy_ and isinstance(bstack11ll1ll1ll_opy_, str) and len(bstack11ll1ll1ll_opy_) > 0:
            if bstack1l1llll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠬჸ") in bstack1lllll11l1_opy_:
              try:
                from browserstack_sdk.sdk_cli.cli import cli
                if cli and cli.is_running() and cli.cli_service:
                  _1l1l1ll11l_opy_(cli, bstack11ll1ll1ll_opy_, test_run_uuid)
                else:
                  logger.debug(bstack1l1llll_opy_ (u"࡙ࠬࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠢࡱࡳࡹࠦࡳࡦࡰࡷ࠾ࠥࡉࡌࡊࠢࡱࡳࡹࠦࡲࡦࡣࡧࡽࠬჹ"))
              except Exception as bstack1l1ll11llll_opy_:
                logger.debug(bstack1l1llll_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡳࡪࠠࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠤࡻ࡯ࡡࠡࡩࡕࡔࡈࡀࠠࡼࡿࠪჺ").format(str(bstack1l1ll11llll_opy_)))
            else:
              TestHubHandler.bstack1ll11ll1ll_opy_({
                  bstack1l1llll_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭჻"): bstack11ll1ll1ll_opy_,
                  bstack1l1llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨჼ"): test_run_uuid
              })
        else:
          logger.debug(bstack1l1llll_opy_ (u"ࠩࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠦࡣࡢࡲࡷࡹࡷ࡫ࡤࠡࡤࡸࡸࠥࡴ࡯ࠡࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨࠤ࡫ࡵࡲࠡࡽࢀࠫჽ").format(bstack1lllll11l1_opy_))
    except Exception as e:
      logger.debug(bstack1l1llll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡰࡧࠤࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴ࠻ࠢࡾࢁࠬჾ").format(str(e)))
  return response
def _1l1l1ll11l_opy_(cli, bstack11ll1ll1ll_opy_, test_run_uuid):
  from browserstack_sdk.sdk_cli.test_framework import TestFramework, LogEntry
  test_instance = None
  try:
    if cli and cli.test_framework and hasattr(cli.test_framework, bstack1l1llll_opy_ (u"ࠫ࡬࡫ࡴࡠࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࠩჿ")):
      test_instance = cli.test_framework.get_current_test_instance()
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"࡙ࠬࡣࡳࡧࡨࡲࡸ࡮࡯ࡵ࠼ࠣࡇࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡧࡦࡶࠣࡸࡪࡹࡴࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠽ࠤࢀࢃࠧᄀ").format(e))
  if test_instance and cli.event_dispatcher:
    entry = LogEntry(TestFramework.KIND_SCREENSHOT, bstack11ll1ll1ll_opy_)
    cli.event_dispatcher.send_log_created_event(test_instance, [entry])
    logger.debug(bstack1l1llll_opy_ (u"࠭ࡓࡤࡴࡨࡩࡳࡹࡨࡰࡶࠣࡷࡪࡴࡴࠡࡸ࡬ࡥࠥ࡭ࡒࡑࡅࠣࡪࡴࡸࠠࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪ࠽ࡼࡿࠪᄁ").format(test_run_uuid))
  else:
    logger.debug(bstack1l1llll_opy_ (u"ࠧࡔࡥࡵࡩࡪࡴࡳࡩࡱࡷࠤࡳࡵࡴࠡࡵࡨࡲࡹࡀࠠࡵࡧࡶࡸࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣࡩࡻ࡫࡮ࡵࡡࡧ࡭ࡸࡶࡡࡵࡥ࡫ࡩࡷࡃࡻࡾࠩᄂ").format(
      test_instance is not None, cli.event_dispatcher is not None))
def bstack1111ll11ll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack11llll1l11_opy_
  global PLATFORM_INDEX
  global SESSION_NAME
  global PARALLELISE_VANILLA_PYTHON
  global PARALLELISE_THREADING_PYTHON
  global FRAMEWORK_NAME
  global bstack1l1l1l111l1_opy_
  global bstack1111ll11l_opy_
  global bstack1llll11111l_opy_
  global bstack1ll1ll11111_opy_
  random_label = PerformanceTester.mark_start(EVENTS.bstack1ll1lllll1l_opy_.value)
  if os.getenv(bstack1l1llll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᄃ")) is not None and a11y.bstack1l11lll111_opy_(CONFIG) is None:
    CONFIG[bstack1l1llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᄄ")] = True
  CONFIG[bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬᄅ")] = str(FRAMEWORK_NAME) + str(__version__)
  bstack1111l1ll11_opy_ = os.environ[bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᄆ")]
  bstack1l1l111lll_opy_ = TestHubUtils.bstack1l11111lll_opy_(CONFIG, FRAMEWORK_NAME)
  CONFIG[bstack1l1llll_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨᄇ")] = bstack1111l1ll11_opy_
  CONFIG[bstack1l1llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨᄈ")] = bstack1l1l111lll_opy_
  if CONFIG.get(bstack1l1llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᄉ"),bstack1l1llll_opy_ (u"ࠨࠩᄊ")) and bstack1l1llll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨᄋ") in FRAMEWORK_NAME:
    CONFIG[bstack1l1llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᄌ")].pop(bstack1l1llll_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᄍ"), None)
    CONFIG[bstack1l1llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᄎ")].pop(bstack1l1llll_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᄏ"), None)
  command_executor = bstack1l1l111ll11_opy_()
  logger.debug(bstack11llll1lll_opy_.format(command_executor))
  proxy = bstack1l1l11l1ll1_opy_(CONFIG, proxy)
  bstack1ll1l111l1_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
  try:
    if PARALLELISE_VANILLA_PYTHON is True:
      bstack1ll1l111l1_opy_ = int(multiprocessing.current_process().name)
    elif PARALLELISE_THREADING_PYTHON is True:
      bstack1ll1l111l1_opy_ = int(threading.current_thread().name)
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"ࠢࡱࡣࡵࡥࡱࡲࡥ࡭ࠢࡳࡰࡦࡺࡦࡰࡴࡰ࠱࡮ࡴࡤࡦࡺࠣࡶࡪࡹ࡯࡭ࡷࡷ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡽࢀ࠾ࠥࢁࡽࠣᄐ").format(type(e).__name__, e), exc_info=True)
    bstack1ll1l111l1_opy_ = 0
  bstack11111lll1l_opy_ = get_caps(CONFIG, bstack1ll1l111l1_opy_)
  logger.debug(CONFIG_FILE_CONTENT.format(str(bstack11111lll1l_opy_)))
  if bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᄑ") in CONFIG and bstack11lll11l1l_opy_(CONFIG[bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᄒ")]):
    update_caps_for_local(bstack11111lll1l_opy_)
  if a11y.is_enabled_platform(CONFIG, bstack1ll1l111l1_opy_) and a11y.is_platform_supported(bstack11111lll1l_opy_, options, desired_capabilities, CONFIG):
    threading.current_thread().a11yPlatform = True
    if (cli.accessibility is None or not cli.accessibility.is_enabled() or bstack1l1llll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠫᄓ") in FRAMEWORK_NAME):
      a11y.set_capabilities(bstack11111lll1l_opy_, CONFIG)
  if desired_capabilities:
    bstack1lll111lll1_opy_ = bstack1ll1l11ll1l_opy_(desired_capabilities)
    bstack1lll111lll1_opy_[bstack1l1llll_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫᄔ")] = bstack11l1ll1111_opy_(CONFIG)
    bstack1l1lllll11_opy_ = get_caps(bstack1lll111lll1_opy_)
    if bstack1l1lllll11_opy_:
      bstack11111lll1l_opy_ = update(bstack1l1lllll11_opy_, bstack11111lll1l_opy_)
    desired_capabilities = None
  if options:
    bstack1lllll111l_opy_(options, bstack11111lll1l_opy_)
  if not options:
    options = bstack1llll11ll11_opy_(bstack11111lll1l_opy_)
  try:
    if bstack1l11l11l11_opy_:
      def _1l1111l11l_opy_(bstack11111ll11_opy_):
        if not isinstance(bstack11111ll11_opy_, dict):
          return
        for _1ll11lllll1_opy_ in list(bstack11111ll11_opy_.keys()):
          _1ll11l1111_opy_ = bstack11111ll11_opy_[_1ll11lllll1_opy_]
          if _1ll11l1111_opy_ is None:
            bstack11111ll11_opy_.pop(_1ll11lllll1_opy_, None)
          elif isinstance(_1ll11l1111_opy_, dict):
            _1l1111l11l_opy_(_1ll11l1111_opy_)
      _1l1111l11l_opy_(bstack11111lll1l_opy_)
      _1l1111l11l_opy_(desired_capabilities)
      if options is not None and hasattr(options, bstack1l1llll_opy_ (u"ࠬࡥࡣࡢࡲࡶࠫᄕ")):
        _1l1111l11l_opy_(options._caps)
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"ࠨ࡭ࡰࡦࡢ࡭ࡳ࡯ࡴࠩࠫࠣࡴࡴࡹࡴ࠮ࡱࡳࡸ࡮ࡵ࡮ࡴࠢࡳࡶࡺࡴࡥࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࡾࢁࠧᄖ").format(e))
  if bstack1l11l11l11_opy_:
    options = bstack1lllllll11_opy_(options)
  bstack1ll1ll11111_opy_ = CONFIG.get(bstack1l1llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᄗ"))[bstack1ll1l111l1_opy_]
  if proxy and bstack1l1ll11111_opy_() >= version.parse(bstack1l1llll_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨᄘ")):
    options.proxy(proxy)
  if options and bstack1l1ll11111_opy_() >= version.parse(bstack1l1llll_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨᄙ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1l1ll11111_opy_() < version.parse(bstack1l1llll_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩᄚ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack11111lll1l_opy_)
  logger.info(bstack1llll1llll1_opy_)
  performance_tester.end(EVENTS.bstack1111l1l1l_opy_.value, EVENTS.bstack1111l1l1l_opy_.value + bstack1l1llll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᄛ"), EVENTS.bstack1111l1l1l_opy_.value + bstack1l1llll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᄜ"), status=True, failure=None, test_name=SESSION_NAME)
  if bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡱࡴࡲࡪ࡮ࡲࡥࠨᄝ") in kwargs:
    del kwargs[bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡲࡵࡳ࡫࡯࡬ࡦࠩᄞ")]
  PerformanceTester.end(EVENTS.bstack1ll1lllll1l_opy_.value, random_label + bstack1l1llll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᄟ"), random_label + bstack1l1llll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᄠ"), status=True, failure=None, test_name=SESSION_NAME)
  try:
    if bstack1l1ll11111_opy_() >= version.parse(bstack1l1llll_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪᄡ")):
      bstack1l1l1l111l1_opy_(self, command_executor=command_executor,
                options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
    elif bstack1l1ll11111_opy_() >= version.parse(bstack1l1llll_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪᄢ")):
      bstack1l1l1l111l1_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities, options=options,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l1ll11111_opy_() >= version.parse(bstack1l1llll_opy_ (u"ࠬ࠸࠮࠶࠵࠱࠴ࠬᄣ")):
      bstack1l1l1l111l1_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    else:
      bstack1l1l1l111l1_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive)
  except Exception as bstack111lll11l1_opy_:
    logger.error(bstack111ll1111l_opy_.format(bstack1l1llll_opy_ (u"࠭ࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠬᄤ"), str(bstack111lll11l1_opy_)))
    raise bstack111lll11l1_opy_
  random_label = PerformanceTester.mark_start(EVENTS.bstack1ll1llll1ll_opy_.value)
  if a11y.is_enabled_platform(CONFIG, bstack1ll1l111l1_opy_) and a11y.is_platform_supported(self.capabilities, options, desired_capabilities):
    if CONFIG[bstack1l1llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩᄥ")][bstack1l1llll_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᄦ")] == True:
      threading.current_thread().appA11yPlatform = True
      if cli.accessibility is None or not cli.accessibility.is_enabled() or bstack1l1llll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠪᄧ") in FRAMEWORK_NAME:
        a11y.set_capabilities(bstack11111lll1l_opy_, CONFIG)
  try:
    bstack1l1l1llllll_opy_ = bstack1l1llll_opy_ (u"ࠪࠫᄨ")
    if bstack1l1ll11111_opy_() >= version.parse(bstack1l1llll_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࡥ࠵ࠬᄩ")):
      if self.caps is not None:
        bstack1l1l1llllll_opy_ = self.caps.get(bstack1l1llll_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧᄪ"))
    else:
      if self.capabilities is not None:
        bstack1l1l1llllll_opy_ = self.capabilities.get(bstack1l1llll_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨᄫ"))
    if bstack1l1l1llllll_opy_:
      bstack1lll11l111_opy_(bstack1l1l1llllll_opy_)
      if bstack1l1ll11111_opy_() <= version.parse(bstack1l1llll_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧᄬ")):
        if bstack1lll1ll1l11_opy_.startswith(bstack1l1llll_opy_ (u"ࠨࡪࡷࡸࡵࡀ࠯࠰ࠩᄭ")) or bstack1lll1ll1l11_opy_.startswith(bstack1l1llll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠫᄮ")):
          self.command_executor._url = bstack1lll1ll1l11_opy_
        else:
          self.command_executor._url = bstack1l1llll_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦᄯ") + bstack1lll1ll1l11_opy_ + bstack1l1llll_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣᄰ")
      else:
        self.command_executor._url = bstack1l1llll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢᄱ") + bstack1l1l1llllll_opy_ + bstack1l1llll_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢᄲ")
      logger.debug(bstack1lllll11l11_opy_.format(bstack1l1l1llllll_opy_))
    else:
      logger.debug(bstack1lllllll11l_opy_.format(bstack1l1llll_opy_ (u"ࠢࡐࡲࡷ࡭ࡲࡧ࡬ࠡࡊࡸࡦࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠣᄳ")))
  except Exception as e:
    logger.debug(bstack1lllllll11l_opy_.format(e))
  if bstack1l1llll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧᄴ") in FRAMEWORK_NAME:
    bstack1111l1111_opy_(PLATFORM_INDEX, bstack1llll11111l_opy_)
  bstack11llll1l11_opy_ = self.session_id
  if bstack1l1llll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᄵ") in FRAMEWORK_NAME or bstack1l1llll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪᄶ") in FRAMEWORK_NAME or bstack1l1llll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪᄷ") in FRAMEWORK_NAME or bstack1l1llll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨ࠭ᄸ") in FRAMEWORK_NAME:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack111l1ll1l1_opy_ = getattr(threading.current_thread(), bstack1l1llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡚ࡥࡴࡶࡐࡩࡹࡧࠧᄹ"), None)
  if bstack1l1llll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧᄺ") in FRAMEWORK_NAME or bstack1l1llll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧᄻ") in FRAMEWORK_NAME:
    TestHubHandler.send_cbt_info(self)
  if bstack1l1llll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᄼ") in FRAMEWORK_NAME and bstack111l1ll1l1_opy_ and bstack111l1ll1l1_opy_.get(bstack1l1llll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᄽ"), bstack1l1llll_opy_ (u"ࠫࠬᄾ")) == bstack1l1llll_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭ᄿ"):
    TestHubHandler.send_cbt_info(self)
  with bstack1l1111ll1l_opy_:
    bstack1111ll11l_opy_.append(self)
  if bstack1l1llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᅀ") in CONFIG and bstack1l1llll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᅁ") in CONFIG[bstack1l1llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᅂ")][bstack1ll1l111l1_opy_]:
    SESSION_NAME = CONFIG[bstack1l1llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᅃ")][bstack1ll1l111l1_opy_][bstack1l1llll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᅄ")]
  logger.debug(bstack1l1ll1ll1l_opy_.format(bstack11llll1l11_opy_))
  PerformanceTester.end(EVENTS.bstack1ll1llll1ll_opy_.value, random_label + bstack1l1llll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᅅ"), random_label + bstack1l1llll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᅆ"), status=True, failure=None, test_name=SESSION_NAME)
import browserstack_sdk
ROBOT_PLAYWRIGHT_CDP_URL = None
bstack1ll1l1ll11_opy_ = False
bstack11l1111lll_opy_ = None
def set_playwright_globals(**kwargs):
    bstack1l1llll_opy_ (u"ࠨࠢࠣࡋࡱ࡮ࡪࡩࡴࠡࡩ࡯ࡳࡧࡧ࡬ࡴࠢࡩࡶࡴࡳࠠࡠࡡ࡬ࡲ࡮ࡺ࡟ࡠ࠰ࡳࡽࠥ࡯࡮ࡵࡱࠣࡸ࡭࡯ࡳࠡ࡯ࡲࡨࡺࡲࡥࠨࡵࠣࡲࡦࡳࡥࡴࡲࡤࡧࡪ࠴ࠊࠡࠢࠣࠤࡈࡧ࡬࡭ࡧࡧࠤࡧࡿࠠࡠࡡ࡬ࡲ࡮ࡺ࡟ࡠ࠰ࡳࡽࠥࡨࡥࡧࡱࡵࡩࠥࡶࡡࡵࡥ࡫ࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠩࠫࠣࡷࡴࠦࡴࡩࡣࡷࠤࡲࡵࡤࡠ࡮ࡤࡹࡳࡩࡨࠋࠢࠣࠤࠥࡧ࡮ࡥࠢࡳࡥࡹࡩࡨࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡩࡡ࡯ࠢࡤࡧࡨ࡫ࡳࡴࠢࡆࡓࡓࡌࡉࡈ࠮ࠣࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡎࡂࡏࡈ࠰ࠥ࡫ࡴࡤ࠰ࠥࠦࠧᅇ")
    g = globals()
    for key, value in kwargs.items():
        g[key] = value
try:
  try:
    import Browser
    import os
    from subprocess import Popen
    from browserstack_sdk.__init__ import get_turboscale_playwright_url
    from browserstack_sdk.sdk_cli.utils.bstack1ll1l1llll1_opy_ import bstack1ll1lll1l11_opy_
    def bstack1ll1lll1lll_opy_(self, args, **kwargs):
      global CONFIG
      global SELENIUM_OR_PLAYWRIGHT_INSTALLED
      global ROBOT_PLAYWRIGHT_CDP_URL
      global bstack1ll1l1ll11_opy_
      from browserstack_sdk.__init__ import LAUNCH_PATCH_ROBOT_PLAYWRIGHT
      if(bstack1l1llll_opy_ (u"ࠢࡪࡰࡧࡩࡽ࠴ࡪࡴࠤᅈ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1l1llll_opy_ (u"ࠨࢀࠪᅉ")), bstack1l1llll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᅊ"), bstack1l1llll_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬᅋ")), bstack1l1llll_opy_ (u"ࠫࡼ࠭ᅌ")) as fp:
          fp.write(bstack1l1llll_opy_ (u"ࠧࠨᅍ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1l1llll_opy_ (u"ࠨࡩ࡯ࡦࡨࡼࡤࡨࡳࡵࡣࡦ࡯࠳ࡰࡳࠣᅎ")))):
          with open(args[1], bstack1l1llll_opy_ (u"ࠧࡳࠩᅏ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1l1llll_opy_ (u"ࠨࡣࡶࡽࡳࡩࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡢࡲࡪࡽࡐࡢࡩࡨࠬࡨࡵ࡮ࡵࡧࡻࡸ࠱ࠦࡰࡢࡩࡨࠤࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠧᅐ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1lll1l1l1ll_opy_)
            if bstack1l1llll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᅑ") in CONFIG and str(CONFIG[bstack1l1llll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧᅒ")]).lower() != bstack1l1llll_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪᅓ"):
                cdpUrl = get_turboscale_playwright_url()
                LAUNCH_PATCH_ROBOT_PLAYWRIGHT = bstack1l1llll_opy_ (u"ࠬ࠭ࠧࠋ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࠎࡨࡵ࡮ࡴࡶࠣࡦࡸࡺࡡࡤ࡭ࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠸ࡡࠥࡃ࠽࠾ࠢࠪࡸࡷࡻࡥࠨ࠽ࠍࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠶ࡡࡀࠐࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡩࡡࡱࡵࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠷࡝࠼ࠌࡦࡳࡳࡹࡴࠡࡲࡢ࡭ࡳࡪࡥࡹࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠷ࡣ࠻ࠋࡥࡲࡲࡸࡺࠠࡣࡵࡷࡥࡨࡱ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠷ࡡࠥࡃ࠽࠾ࠢࠪࡸࡷࡻࡥࠨ࠽ࠍࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡷࡱ࡯ࡣࡦࠪ࠳࠰ࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠵ࠪ࠽ࠍࡧࡴࡴࡳࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣࠫ࠾ࠎࡨࡵ࡮ࡴࡶࠣࡳࡷ࡯ࡧࡪࡰࡤࡰࡤࡩࡨࡳࡱࡰ࡭ࡺࡳ࡟࡭ࡣࡸࡲࡨ࡮ࠠ࠾ࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱ࠮ࡤࡪࡵࡳࡲ࡯ࡵ࡮࠰࡯ࡥࡺࡴࡣࡩ࠰ࡥ࡭ࡳࡪࠨࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳࠩ࠼ࠌ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱ࠮ࡤࡪࡵࡳࡲ࡯ࡵ࡮࠰࡯ࡥࡺࡴࡣࡩࠢࡀࠤࡦࡹࡹ࡯ࡥࠣࠬࡱࡧࡵ࡯ࡥ࡫ࡓࡵࡺࡩࡰࡰࡶ࠭ࠥࡃ࠾ࠡࡽࡾࠎࠥࠦࡩࡧࠢࠫࠥࡧࡹࡴࡢࡥ࡮ࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠪࠢࡾࡿࠏࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡢࡧ࡭ࡸ࡯࡮࡫ࡸࡱࡤࡲࡡࡶࡰࡦ࡬࠭ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷ࠮ࡁࠊࠡࠢࢀࢁࠏࠦࠠ࡭ࡧࡷࠤࡨࡧࡰࡴ࠽ࠍࠤࠥࡺࡲࡺࠢࡾࡿࠏࠦࠠࠡࠢࡦࡥࡵࡹࠠ࠾ࠢࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࡢࡴࡶࡤࡧࡰࡥࡣࡢࡲࡶ࠭ࡀࠐࠠࠡࡿࢀࠤࡨࡧࡴࡤࡪࠣࠬࡪࡾࠩࠡࡽࡾࠎࠥࠦࠠࠡࡥࡲࡲࡸࡵ࡬ࡦ࠰ࡨࡶࡷࡵࡲࠩࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵ࠽ࠦ࠱ࠦࡥࡹࠫ࠾ࠎࠥࠦࡽࡾࠌࠣࠤ࡮࡬ࠠࠩࡤࡶࡸࡦࡩ࡫ࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠪࠢࡾࡿࠏࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭࠯ࡥࡲࡲࡳ࡫ࡣࡵࡑࡹࡩࡷࡉࡄࡑࠪࡾࡿࠏࠦࠠࠡࠢࠣࠤࡪࡴࡤࡱࡱ࡬ࡲࡹ࡛ࡒࡍ࠼ࠣࠫࢀࡩࡤࡱࡗࡵࡰࢂ࠭ࠠࠬࠢࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩ࠭ࠌࠣࠤࠥࠦࠠࠡ࠰࠱࠲ࡱࡧࡵ࡯ࡥ࡫ࡓࡵࡺࡩࡰࡰࡶࠎࠥࠦࠠࠡࡿࢀ࠭ࡀࠐࠠࠡࡿࢀࠎࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡩ࡯࡯ࡰࡨࡧࡹ࠮ࡻࡼࠌࠣࠤࠥࠦࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶ࠽ࠤࠬࢁࡣࡥࡲࡘࡶࡱࢃࠧࠡ࠭ࠣࡩࡳࡩ࡯ࡥࡧࡘࡖࡎࡉ࡯࡮ࡲࡲࡲࡪࡴࡴࠩࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡦࡥࡵࡹࠩࠪ࠮ࠍࠤࠥࠦࠠ࠯࠰࠱ࡰࡦࡻ࡮ࡤࡪࡒࡴࡹ࡯࡯࡯ࡵࠍࠤࠥࢃࡽࠪ࠽ࠍࢁࢂࡁࠊࡤࡱࡱࡷࡹࠦ࡯ࡳ࡫ࡪ࡭ࡳࡧ࡬ࡠࡥࡲࡲࡳ࡫ࡣࡵࠢࡀࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡨࡵ࡮࡯ࡧࡦࡸ࠳ࡨࡩ࡯ࡦࠫ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯ࠬ࠿ࠏ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡩ࡯࡯ࡰࡨࡧࡹࠦ࠽ࠡࡣࡶࡽࡳࡩࠠࠩࡥࡲࡲࡳ࡫ࡣࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠫࠣࡁࡃࠦࡻࡼࠌࠣࠤ࡮࡬ࠠࠩࠣࡥࡷࡹࡧࡣ࡬ࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠯ࠠࡼࡽࠍࠤࠥࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦ࡯ࡳ࡫ࡪ࡭ࡳࡧ࡬ࡠࡥࡲࡲࡳ࡫ࡣࡵࠪࡦࡳࡳࡴࡥࡤࡶࡒࡴࡹ࡯࡯࡯ࡵࠬ࠿ࠏࠦࠠࡾࡿࠍࠤࠥࡲࡥࡵࠢࡦࡥࡵࡹ࠻ࠋࠢࠣࡸࡷࡿࠠࡼࡽࠍࠤࠥࠦࠠࡤࡣࡳࡷࠥࡃࠠࡋࡕࡒࡒ࠳ࡶࡡࡳࡵࡨࠬࡧࡹࡴࡢࡥ࡮ࡣࡨࡧࡰࡴࠫ࠾ࠎࠥࠦࡽࡾࠢࡦࡥࡹࡩࡨࠡࠪࡨࡼ࠮ࠦࡻࡼࠌࠣࠤࢂࢃࠊࠡࠢࡦࡳࡳࡹࡴࠡ࡯ࡲࡨ࡮࡬ࡩࡦࡦࡈࡲࡩࡶ࡯ࡪࡰࡷࠤࡂࠦࠧࡼࡥࡧࡴ࡚ࡸ࡬ࡾࠩࠣ࠯ࠥ࡫࡮ࡤࡱࡧࡩ࡚ࡘࡉࡄࡱࡰࡴࡴࡴࡥ࡯ࡶࠫࡎࡘࡕࡎ࠯ࡵࡷࡶ࡮ࡴࡧࡪࡨࡼࠬࡨࡧࡰࡴࠫࠬ࠿ࠏࠦࠠࡪࡨࠣࠬࡧࡹࡴࡢࡥ࡮ࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ࠭ࠥࢁࡻࠋࠢࠣࠤࠥࡸࡥࡵࡷࡵࡲࠥࡧࡷࡢ࡫ࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡨࡵ࡮࡯ࡧࡦࡸࡔࡼࡥࡳࡅࡇࡔ࠭ࢁࡻࠋࠢࠣࠤࠥࠦࠠࡦࡰࡧࡴࡴ࡯࡮ࡵࡗࡕࡐ࠿ࠦ࡭ࡰࡦ࡬ࡪ࡮࡫ࡤࡆࡰࡧࡴࡴ࡯࡮ࡵ࠮ࠍࠤࠥࠦࠠࠡࠢ࠱࠲࠳ࡩ࡯࡯ࡰࡨࡧࡹࡕࡰࡵ࡫ࡲࡲࡸࠐࠠࠡࠢࠣࢁࢂ࠯࠻ࠋࠢࠣࢁࢂࠐࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡣࡺࡥ࡮ࡺࠠࡰࡴ࡬࡫࡮ࡴࡡ࡭ࡡࡦࡳࡳࡴࡥࡤࡶࠫࡿࢀࠐࠠࠡࠢࠣ࠲࠳࠴ࡣࡰࡰࡱࡩࡨࡺࡏࡱࡶ࡬ࡳࡳࡹࠬࠋࠢࠣࠤࠥࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵ࠼ࠣࡱࡴࡪࡩࡧ࡫ࡨࡨࡊࡴࡤࡱࡱ࡬ࡲࡹࠐࠠࠡࡿࢀ࠭ࡀࠐࡽࡾ࠽ࠍ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࠐࠧࠨࠩᅔ").format(cdpUrl=cdpUrl)
            lines.insert(1, LAUNCH_PATCH_ROBOT_PLAYWRIGHT)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1l1llll_opy_ (u"ࠨࡩ࡯ࡦࡨࡼࡤࡨࡳࡵࡣࡦ࡯࠳ࡰࡳࠣᅕ")), bstack1l1llll_opy_ (u"ࠧࡸࠩᅖ")) as bstack11ll111l11_opy_:
              bstack11ll111l11_opy_.writelines(lines)
        CONFIG[bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪᅗ")] = str(FRAMEWORK_NAME) + str(__version__)
        import urllib.parse
        bstack1111l1ll11_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᅘ"), bstack1l1llll_opy_ (u"ࠪࠫᅙ"))
        bstack1l1l111lll_opy_ = TestHubUtils.bstack1l11111lll_opy_(CONFIG, FRAMEWORK_NAME)
        CONFIG[bstack1l1llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧᅚ")] = bstack1111l1ll11_opy_
        CONFIG[bstack1l1llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧᅛ")] = bstack1l1l111lll_opy_
        bstack1ll1l111l1_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
        try:
          if PARALLELISE_VANILLA_PYTHON is True:
            bstack1ll1l111l1_opy_ = int(multiprocessing.current_process().name)
          elif PARALLELISE_THREADING_PYTHON is True:
            bstack1ll1l111l1_opy_ = int(threading.current_thread().name)
        except Exception:
          bstack1ll1l111l1_opy_ = 0
        CONFIG[bstack1l1llll_opy_ (u"ࠨࡵࡴࡧ࡚࠷ࡈࠨᅜ")] = False
        CONFIG[bstack1l1llll_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨᅝ")] = True
        bstack11l1ll11_opy_ = bstack1ll1lll1l11_opy_(bstack1ll1l111l1_opy_)
        if bstack11l1ll11_opy_ is not None:
          import bstack_utils.constants as _1llll11l111_opy_
          _1lll11l1111_opy_ = bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩᅞ") if bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪᅟ") in bstack11l1ll11_opy_ else bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᅠ")
          _1ll1l11l1ll_opy_ = bstack11l1ll11_opy_.get(_1lll11l1111_opy_, bstack1l1llll_opy_ (u"ࠫࠬᅡ")).strip().lower()
          _1llll1ll1ll_opy_ = _1ll1l11l1ll_opy_ in _1llll11l111_opy_.bstack1llll1lll11_opy_
          if bstack11l1ll11_opy_.get(bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᅢ")) and not _1llll1ll1ll_opy_:
            bstack11l1ll11_opy_[bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᅣ")] = False
            _1ll1lll1111_opy_ = [k for k in bstack11l1ll11_opy_ if k.startswith(bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᅤ"))]
            for k in _1ll1lll1111_opy_:
              del bstack11l1ll11_opy_[k]
          bstack1ll111ll11l_opy_ = bstack11l1ll11_opy_
          import urllib.parse
          if bstack1l1llll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬᅥ") in CONFIG and str(CONFIG[bstack1l1llll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᅦ")]).lower() != bstack1l1llll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩᅧ"):
            ROBOT_PLAYWRIGHT_CDP_URL = get_turboscale_playwright_url() + urllib.parse.quote(json.dumps(bstack1ll111ll11l_opy_))
          else:
            ROBOT_PLAYWRIGHT_CDP_URL = bstack1l1llll_opy_ (u"ࠫࡼࡹࡳ࠻࠱࠲ࡧࡩࡶ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠿ࡤࡣࡳࡷࡂ࠭ᅨ") + urllib.parse.quote(json.dumps(bstack1ll111ll11l_opy_))
          os.environ[bstack1l1llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡕࡂࡐࡖࡢࡔ࡜ࡥࡃࡅࡒࡢ࡙ࡗࡒࠧᅩ")] = ROBOT_PLAYWRIGHT_CDP_URL
          bstack1ll1l1ll11_opy_ = True
          from browserstack_sdk.sdk_cli.automation_framework import bstack1l111l1l_opy_
          from browserstack_sdk.sdk_cli.bstack1l1ll1l1_opy_ import bstack111ll111_opy_
          instance = next(iter(bstack1l111l1l_opy_.instances.values()), None)
          if instance:
            bstack111ll111_opy_.set_state(instance, bstack111ll111_opy_.bstack1l111lll_opy_, bstack11l1ll11_opy_)
            bstack111ll111_opy_.set_state(instance, bstack111ll111_opy_.bstack11lll111_opy_, ROBOT_PLAYWRIGHT_CDP_URL)
          try:
            from browserstack_sdk.sdk_cli.cli import cli as _1lllll1l1ll_opy_
            from browserstack_sdk.sdk_cli.automation_framework import AutomationFrameworkState, HookState
            _1lllll1l1ll_opy_.automation_framework.bstack1l1lll11ll_opy_(
              None,
              (instance, bstack1l1llll_opy_ (u"࠭࡭ࡰࡦࡢࡴࡴࡶࡥ࡯ࠩᅪ")),
              (AutomationFrameworkState.CREATE, HookState.PRE),
              None,
            )
          except Exception as e:
            logger.debug(bstack1l1llll_opy_ (u"ࠢ࡮ࡱࡧࡣࡵࡵࡰࡦࡰ࠽ࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡧ࡫ࡵࡩࠥࡉࡒࡆࡃࡗࡉ࠳ࡖࡒࡆ࠼ࠣࡿࢂࠨᅫ").format(e))
          logger.debug(bstack1l1llll_opy_ (u"ࠣ࡯ࡲࡨࡤࡶ࡯ࡱࡧࡱ࠾ࠥࡻࡳࡪࡰࡪࠤ࡫࡯࡮ࡢ࡮ࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢࡩࡶࡴࡳࠠࡅࡴ࡬ࡺࡪࡸࡉ࡯࡫ࡷࠦᅬ"))
        else:
          bstack1ll111ll11l_opy_ = get_caps(CONFIG, bstack1ll1l111l1_opy_)
          if CONFIG.get(bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᅭ")):
            update_caps_for_local(bstack1ll111ll11l_opy_)
            bstack1ll111ll11l_opy_[bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᅮ")] = os.environ[bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ᅯ")]
          logger.debug(bstack1l1llll_opy_ (u"ࠧࡳ࡯ࡥࡡࡳࡳࡵ࡫࡮࠻ࠢࡇࡶ࡮ࡼࡥࡳࡋࡱ࡭ࡹࠦࡵ࡯ࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨ࠰ࠥ࡬ࡡ࡭࡮࡬ࡲ࡬ࠦࡢࡢࡥ࡮ࠤࡹࡵࠠࡨࡧࡷࡣࡨࡧࡰࡴࠤᅰ"))
        logger.debug(CONFIG_FILE_CONTENT.format(str(bstack1ll111ll11l_opy_)))
        if bstack1l1llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᅱ") in CONFIG and bstack1l1llll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᅲ") in CONFIG[bstack1l1llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᅳ")][bstack1ll1l111l1_opy_]:
          SESSION_NAME = CONFIG[bstack1l1llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᅴ")][bstack1ll1l111l1_opy_][bstack1l1llll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᅵ")]
        from bstack_utils.helper import bstack111l11l11l_opy_
        args.append(bstack1l1llll_opy_ (u"ࠫࡹࡸࡵࡦࠩᅶ") if bstack111l11l11l_opy_(CONFIG) else bstack1l1llll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫᅷ"))
        args.append(str(bstack1ll111ll11l_opy_.get(bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᅸ"), False)).lower())
        args.append(os.path.join(os.path.expanduser(bstack1l1llll_opy_ (u"ࠧࡿࠩᅹ")), bstack1l1llll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᅺ"), bstack1l1llll_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫᅻ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1ll111ll11l_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1l1llll_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧᅼ"))
      SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
      return bstack111l111l11_opy_(self, args, **kwargs)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack11111llll_opy_(self,
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
        firefoxUserPrefs = None,
        **kwargs
        ):
    global CONFIG
    global PLATFORM_INDEX
    global SESSION_NAME
    global PARALLELISE_VANILLA_PYTHON
    global PARALLELISE_THREADING_PYTHON
    global FRAMEWORK_NAME
    if FRAMEWORK_NAME and bstack1l1llll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫᅽ") in str(FRAMEWORK_NAME).lower() and os.environ.get(bstack1l1llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡊࡒࡓࡐ࡙ࠧᅾ")):
        logger.debug(bstack1l1llll_opy_ (u"ࠨ࡭ࡰࡦࡢࡰࡦࡻ࡮ࡤࡪ࠽ࠤࡇ࡫ࡨࡢࡸࡨࠤࡇ࡯࡮ࡢࡴࡼࠤࡋࡲ࡯ࡸࠢ⠗ࠤࡩ࡫ࡦࡦࡴࡵ࡭ࡳ࡭ࠠࡵࡱࠣࡗࡉࡑࠠࡄࡎࡌࠤ࡭ࡵ࡯࡬ࡵࠣ࠯ࠥࡲࡩࡴࡶࡨࡲࡪࡸࠢᅿ"))
        return
    CONFIG[bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᆀ")] = str(FRAMEWORK_NAME) + str(__version__)
    bstack1111l1ll11_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᆁ"), bstack1l1llll_opy_ (u"ࠩࠪᆂ"))
    bstack1l1l111lll_opy_ = TestHubUtils.bstack1l11111lll_opy_(CONFIG, FRAMEWORK_NAME)
    CONFIG[bstack1l1llll_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ᆃ")] = bstack1111l1ll11_opy_
    CONFIG[bstack1l1llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ᆄ")] = bstack1l1l111lll_opy_
    bstack1ll1l111l1_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
    try:
      if PARALLELISE_VANILLA_PYTHON is True:
        bstack1ll1l111l1_opy_ = int(multiprocessing.current_process().name)
      elif PARALLELISE_THREADING_PYTHON is True:
        bstack1ll1l111l1_opy_ = int(threading.current_thread().name)
    except Exception:
      bstack1ll1l111l1_opy_ = 0
    CONFIG[bstack1l1llll_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᆅ")] = True
    bstack11111lll1l_opy_ = get_caps(CONFIG, bstack1ll1l111l1_opy_)
    bstack1lll1ll11l_opy_ = bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧᆆ") if bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨᆇ") in bstack11111lll1l_opy_ else bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᆈ")
    bstack1ll1ll11l_opy_ = False
    try:
        from bstack_utils import accessibility as a11y
        import bstack_utils.constants as bstack1l1l1111lll_opy_
        bstack11l1111l1l_opy_ = bstack11111lll1l_opy_.get(bstack1lll1ll11l_opy_, bstack1l1llll_opy_ (u"ࠩࠪᆉ")).strip().lower()
        browser_version = str(bstack11111lll1l_opy_.get(bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᆊ"), bstack11111lll1l_opy_.get(bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᆋ"), bstack1l1llll_opy_ (u"ࠬ࠭ᆌ")))).strip()
        bstack1ll111lll11_opy_ = bstack11l1111l1l_opy_ in bstack1l1l1111lll_opy_.bstack1llll1lll11_opy_
        min_version = bstack1l1l1111lll_opy_.MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION
        if not browser_version or browser_version.lower().startswith(bstack1l1llll_opy_ (u"࠭࡬ࡢࡶࡨࡷࡹ࠭ᆍ")):
            bstack1l1llll111_opy_ = True
        else:
            major = browser_version.split(bstack1l1llll_opy_ (u"ࠧ࠯ࠩᆎ"))[0]
            bstack1l1llll111_opy_ = major.isdigit() and int(major) > min_version
        if not bstack1l1llll111_opy_:
            logger.warning(bstack1l1llll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠣ࡫ࡷ࡫ࡡࡵࡧࡵࠤࡹ࡮ࡡ࡯ࠢࡾࢁ࠳ࠦࡃࡶࡴࡵࡩࡳࡺࠠࡷࡧࡵࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠧᆏ").format(min_version, browser_version))
        if a11y.is_enabled_platform(CONFIG, bstack1ll1l111l1_opy_) and bstack1ll111lll11_opy_ and bstack1l1llll111_opy_ and a11y.is_platform_supported(bstack11111lll1l_opy_, options=None, config=CONFIG):
            bstack1ll1ll11l_opy_ = True
            import browserstack_sdk
            browserstack_sdk.CONFIG[bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᆐ")] = True
            bstack11111lll1l_opy_[bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᆑ")] = True
            if CONFIG.get(bstack1l1llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ᆒ")):
                bstack11111lll1l_opy_[bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ᆓ")] = CONFIG[bstack1l1llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨᆔ")]
            import json as _json
            bstack1llll11ll1l_opy_ = os.getenv(bstack1l1llll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᆕ"))
            bstack1llll1lll1l_opy_ = bstack11111lll1l_opy_.get(bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹ࠮ࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪᆖ"))
            if not bstack1llll11ll1l_opy_ and bstack1llll1lll1l_opy_:
                os.environ[bstack1l1llll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᆗ")] = bstack1llll1lll1l_opy_
                bstack1llll11ll1l_opy_ = bstack1llll1lll1l_opy_
            if bstack1llll11ll1l_opy_:
                bstack11111lll1l_opy_[bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴ࠰ࡤࡹࡹ࡮ࡔࡰ࡭ࡨࡲࠬᆘ")] = bstack1llll11ll1l_opy_
            bstack11111lll1_opy_ = _json.loads(os.getenv(bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᆙ"), bstack1l1llll_opy_ (u"ࠬࢁࡽࠨᆚ"))).get(bstack1l1llll_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᆛ"))
            if bstack11111lll1_opy_:
                bstack11111lll1l_opy_[bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠴ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᆜ")] = bstack11111lll1_opy_
            bstack11111lll1l_opy_.pop(bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᆝ"), None)
            bstack11111lll1l_opy_.pop(bstack1l1llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᆞ"), None)
            bstack11111lll1l_opy_.pop(bstack1l1llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᆟ"), None)
            logger.debug(bstack1l1llll_opy_ (u"ࠦࡆ࠷࠱ࡺࠢࡨࡲࡦࡨ࡬ࡦࡦࠣࡪࡴࡸࠠࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥ࠮ࡻࡾࠢࡾࢁ࠮ࠨᆠ").format(
                bstack11l1111l1l_opy_, browser_version))
    except Exception as e:
        bstack1ll1ll11l_opy_ = False
        logger.debug(bstack1l1llll_opy_ (u"ࠧࡇ࠱࠲ࡻࠣࡨࡪࡺࡥࡤࡶ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࡼࡿࠥᆡ").format(str(e)))
    logger.debug(CONFIG_FILE_CONTENT.format(str(bstack11111lll1l_opy_)))
    if CONFIG.get(bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᆢ")):
      update_caps_for_local(bstack11111lll1l_opy_)
    if bstack1l1llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᆣ") in CONFIG and bstack1l1llll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᆤ") in CONFIG[bstack1l1llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᆥ")][bstack1ll1l111l1_opy_]:
      SESSION_NAME = CONFIG[bstack1l1llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᆦ")][bstack1ll1l111l1_opy_][bstack1l1llll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᆧ")]
    import urllib
    import json
    if bstack1l1llll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩᆨ") in CONFIG and str(CONFIG[bstack1l1llll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪᆩ")]).lower() != bstack1l1llll_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ᆪ"):
        bstack1l1lllll1ll_opy_ = get_turboscale_playwright_url()
        cdpUrl = bstack1l1lllll1ll_opy_ + urllib.parse.quote(json.dumps(bstack11111lll1l_opy_))
    else:
        cdpUrl = bstack1l1llll_opy_ (u"ࠨࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠪᆫ") + urllib.parse.quote(json.dumps(bstack11111lll1l_opy_))
    try:
        from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
        PlaywrightDriverWrapperDirect.setup_dispatch_capture()
    except Exception as exc:
        logger.debug(bstack1l1llll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࡷࡳࠤࡩ࡯ࡳࡱࡣࡷࡧ࡭ࠦࡣࡢࡲࡷࡹࡷ࡫ࠠࡧࡱࡵࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤ࠻ࠢࠨࡷࠧᆬ"), exc)
    if bstack1ll1ll11l_opy_:
        browser = self.connect_over_cdp(cdpUrl)
    else:
        browser = bstack11l1111lll_opy_(self, cdpUrl)
    try:
        from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
        wrapper = PlaywrightDriverWrapperDirect(browser, page=None, capabilities=bstack11111lll1l_opy_, config=CONFIG)
        threading.current_thread().bstackSessionDriver = wrapper
        logger.debug(bstack1l1llll_opy_ (u"ࠥࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࡄࡳ࡫ࡹࡩࡷ࡝ࡲࡢࡲࡳࡩࡷࡊࡩࡳࡧࡦࡸࠥࡹࡥࡵࡷࡳࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࠦࡦࡰࡴࠣࡸ࡭ࡸࡥࡢࡦࠣࠩࡸࠨᆭ"), threading.get_ident())
        threading.current_thread().bstackTestErrorMessages = []
        if bstack1ll1ll11l_opy_:
            threading.current_thread().a11yPlatform = True
            wrapper.bstackA11yShouldScan = True
            try:
                _1ll1llll11_opy_ = threading.main_thread()
                if _1ll1llll11_opy_ is not threading.current_thread():
                    setattr(_1ll1llll11_opy_, bstack1l1llll_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᆮ"), True)
                    setattr(_1ll1llll11_opy_, bstack1l1llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫᆯ"), wrapper)
                    logger.debug(bstack1l1llll_opy_ (u"ࠨࡁ࠲࠳ࡼ࠾ࠥࡶࡲࡰࡲࡤ࡫ࡦࡺࡥࡥࠢࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠬࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠠࡵࡱࠣࡱࡦ࡯࡮ࠡࡶ࡫ࡶࡪࡧࡤࠡࡨࡲࡶࠥࡊࡩࡳࡧࡦࡸࠥࡌ࡬ࡰࡹࠣࡷࡹࡵࡰࠣᆰ"))
            except Exception as _1lll111ll1l_opy_:
                logger.debug(bstack1l1llll_opy_ (u"ࠢࡂ࠳࠴ࡽ࠿ࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡶࡴࡶࡡࡨࡣࡷࡩࠥࡺ࡯ࠡ࡯ࡤ࡭ࡳࠦࡴࡩࡴࡨࡥࡩࡀࠠࡼࡿࠥᆱ").format(_1lll111ll1l_opy_))
        if wrapper.session_id and not wrapper._cbt_info_sent:
            PlaywrightDriverWrapperDirect._send_cbt_info_on_session()
        try:
            from playwright.sync_api import Browser as bstack11lllll1l1_opy_
            if not hasattr(bstack11lllll1l1_opy_, bstack1l1llll_opy_ (u"ࠨࡡࡥࡷࡹࡧࡣ࡬ࡡࡱࡩࡼࡥࡰࡢࡩࡨࡣࡵࡧࡴࡤࡪࡨࡨࠬᆲ")):
                _1l1lll11lll_opy_ = bstack11lllll1l1_opy_.new_page
                def _1l1lllllll_opy_(bstack11l11l1lll_opy_, *bstack1l11l1ll1l_opy_, **bstack11ll111l1l_opy_):
                    if getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᆳ"), None):
                        try:
                            bstack1ll1111111l_opy_ = bstack11l11l1lll_opy_.contexts[0] if bstack11l11l1lll_opy_.contexts else None
                            if bstack1ll1111111l_opy_ and bstack1ll1111111l_opy_.pages:
                                page = None
                                for _1l1lll1ll11_opy_ in bstack1ll1111111l_opy_.pages:
                                    if bstack1l1llll_opy_ (u"ࠥࡥࡧࡵࡵࡵ࠼ࡥࡰࡦࡴ࡫ࠣᆴ") in _1l1lll1ll11_opy_.url:
                                        page = _1l1lll1ll11_opy_
                                        logger.debug(bstack1l1llll_opy_ (u"ࠦࡆ࠷࠱ࡺ࠼ࠣࡶࡪࡻࡳࡪࡰࡪࠤࡦࡨ࡯ࡶࡶ࠽ࡦࡱࡧ࡮࡬ࠢࡳࡥ࡬࡫ࠠࡧࡴࡲࡱࠥࡪࡥࡧࡣࡸࡰࡹࠦࡣࡰࡰࡷࡩࡽࡺࠢᆵ"))
                                        break
                                if page is None:
                                    page = bstack1ll1111111l_opy_.new_page(*bstack1l11l1ll1l_opy_, **bstack11ll111l1l_opy_)
                                    logger.debug(bstack1l1llll_opy_ (u"ࠧࡇ࠱࠲ࡻ࠽ࠤࡳࡵࠠࡣ࡮ࡤࡲࡰࠦࡰࡢࡩࡨࠤ࡫ࡵࡵ࡯ࡦ࠯ࠤࡨࡸࡥࡢࡶࡨࡨࠥࡴࡥࡸࠢࡳࡥ࡬࡫ࠠࡪࡰࠣࡨࡪ࡬ࡡࡶ࡮ࡷࠤࡨࡵ࡮ࡵࡧࡻࡸࠧᆶ"))
                            elif bstack1ll1111111l_opy_:
                                page = bstack1ll1111111l_opy_.new_page(*bstack1l11l1ll1l_opy_, **bstack11ll111l1l_opy_)
                                logger.debug(bstack1l1llll_opy_ (u"ࠨࡁ࠲࠳ࡼ࠾ࠥࡩࡲࡦࡣࡷࡩࡩࠦ࡮ࡦࡹࠣࡴࡦ࡭ࡥࠡ࡫ࡱࠤࡩ࡫ࡦࡢࡷ࡯ࡸࠥࡩ࡯࡯ࡶࡨࡼࡹࠨᆷ"))
                            else:
                                page = _1l1lll11lll_opy_(bstack11l11l1lll_opy_, *bstack1l11l1ll1l_opy_, **bstack11ll111l1l_opy_)
                                logger.debug(bstack1l1llll_opy_ (u"ࠢࡂ࠳࠴ࡽ࠿ࠦ࡮ࡰࠢࡧࡩ࡫ࡧࡵ࡭ࡶࠣࡧࡴࡴࡴࡦࡺࡷ࠰ࠥ࡬ࡡ࡭࡮࡬ࡲ࡬ࠦࡢࡢࡥ࡮ࠤࡹࡵࠠ࡯ࡧࡺࡣࡵࡧࡧࡦࠪࠬࠦᆸ"))
                        except Exception as bstack111lll1111_opy_:
                            logger.debug(bstack1l1llll_opy_ (u"ࠣࡃ࠴࠵ࡾࡀࠠࡥࡧࡩࡥࡺࡲࡴࠡࡥࡲࡲࡹ࡫ࡸࡵࠢࡳࡥ࡬࡫ࠠࡳࡧࡸࡷࡪࠦࡦࡢ࡫࡯ࡩࡩࠦࠨࠦࡵࠬ࠰ࠥ࡬ࡡ࡭࡮࡬ࡲ࡬ࠦࡢࡢࡥ࡮ࠦᆹ"), bstack111lll1111_opy_)
                            page = _1l1lll11lll_opy_(bstack11l11l1lll_opy_, *bstack1l11l1ll1l_opy_, **bstack11ll111l1l_opy_)
                    else:
                        page = _1l1lll11lll_opy_(bstack11l11l1lll_opy_, *bstack1l11l1ll1l_opy_, **bstack11ll111l1l_opy_)
                    try:
                        _w = getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨᆺ"), None)
                        if _w and hasattr(_w, bstack1l1llll_opy_ (u"ࠪࡹࡵࡪࡡࡵࡧࡢࡴࡦ࡭ࡥࠨᆻ")):
                            _w.update_page(page)
                        if _w and not _w.session_id:
                            try:
                                import json as _json
                                result = page.evaluate(
                                    bstack1l1llll_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧᆼ"), bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧ࡭ࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡆࡨࡸࡦ࡯࡬ࡴࠤࢀࠫᆽ"))
                                if isinstance(result, str):
                                    result = _json.loads(result)
                                if isinstance(result, dict):
                                    sid = result.get(bstack1l1llll_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᆾ")) or result.get(bstack1l1llll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠫᆿ")) or result.get(bstack1l1llll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡋࡧࠫᇀ"))
                                    if sid:
                                        import threading as _1111l1llll_opy_
                                        from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
                                        with PlaywrightDriverWrapperDirect._session_ids_lock:
                                            PlaywrightDriverWrapperDirect._session_ids[_1111l1llll_opy_.get_ident()] = sid
                                        logger.debug(bstack1l1llll_opy_ (u"ࠤࡆࡥࡵࡺࡵࡳࡧࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠡࡸ࡬ࡥࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠦࡵࠥᇁ"), sid)
                                        PlaywrightDriverWrapperDirect._send_cbt_info_on_session()
                                    else:
                                        logger.debug(bstack1l1llll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵࠤ࡬࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡧࡷࡥ࡮ࡲࡳࠡࡴࡨࡸࡺࡸ࡮ࡦࡦࠣࡲࡴࠦࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦ࠽ࠤࠪࡹࠢᇂ"), result)
                                else:
                                    logger.debug(bstack1l1llll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠥ࡭ࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡆࡨࡸࡦ࡯࡬ࡴࠢࡵࡩࡸࡻ࡬ࡵ࠼ࠣࠩࡸࠨᇃ"), result)
                            except Exception as _11l1l1ll11_opy_:
                                logger.debug(bstack1l1llll_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠢࡩࡥࡱࡲࡢࡢࡥ࡮ࠤࡻ࡯ࡡࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࠩࡸࠨᇄ"), _11l1l1ll11_opy_)
                        if (getattr(threading.current_thread(), bstack1l1llll_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬᇅ"), None)
                                and not getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠧࡢ࠳࠴ࡽࡤࡹࡴࡢࡴࡷࡩࡩ࠭ᇆ"), False)):
                            threading.current_thread().a11y_started = True
                            try:
                                from bstack_utils import accessibility as _1ll11l1l11_opy_
                                bstack1ll111l111_opy_ = getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬᇇ"), True)
                                _1ll11l1l11_opy_.start_test_capture(_w, bstack1ll111l111_opy_)
                            except Exception:
                                logger.debug(bstack1l1llll_opy_ (u"ࠤࡇࡩ࡫࡫ࡲࡳࡧࡧࠤࡆ࠷࠱ࡺࠢࡶࡸࡦࡸࡴࡠࡶࡨࡷࡹࡥࡣࡢࡲࡷࡹࡷ࡫ࠠࡧࡣ࡬ࡰࡪࡪࠢᇈ"))
                        if getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᇉ"), None):
                            try:
                                _1111l11l11_opy_ = page
                                _111l1ll11l_opy_ = page.__class__.close
                                def _1l1lll1l1l1_opy_(*_11111ll1ll_opy_, _bstack_sdk_close=False, **_11llllll11_opy_):
                                    if not _bstack_sdk_close:
                                        try:
                                            from browserstack_sdk.sdk_cli.cli import SDKCLI as _111l1ll111_opy_
                                            _1l1l1111ll1_opy_ = _111l1ll111_opy_._instance
                                            if _1l1l1111ll1_opy_ and _1l1l1111ll1_opy_.is_running():
                                                _1111l1ll1_opy_ = getattr(_1l1l1111ll1_opy_, bstack1l1llll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᇊ"), None)
                                                if _1111l1ll1_opy_:
                                                    _1111l1ll1_opy_.stop_capture_before_browser_close(_1111l11l11_opy_)
                                        except Exception as _11l111l1l1_opy_:
                                            logger.debug(bstack1l1llll_opy_ (u"ࠧࡇ࠱࠲ࡻࠣࡷࡹࡵࡰࡠࡥࡤࡴࡹࡻࡲࡦࠢࠫ࡭ࡳࡹࡴࡢࡰࡦࡩ࠮ࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࡼࡿࠥᇋ").format(_11l111l1l1_opy_))
                                        logger.debug(bstack1l1llll_opy_ (u"ࠨࡄࡦࡨࡨࡶࡷ࡫ࡤࠡࡲࡤ࡫ࡪ࠴ࡣ࡭ࡱࡶࡩ࠭࠯ࠠ⠕ࠢࡺ࡭ࡱࡲࠠࡤ࡮ࡲࡷࡪࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠣࠬࡦ࠷࠱ࡺࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡵࡧࡴࡤࡪࠬࠦᇌ"))
                                        threading.current_thread().bstack_deferred_page_close = True
                                        threading.current_thread().bstack_deferred_page_ref = _1111l11l11_opy_
                                        return
                                    return _111l1ll11l_opy_(_1111l11l11_opy_, **_11llllll11_opy_)
                                page.close = _1l1lll1l1l1_opy_
                                logger.debug(bstack1l1llll_opy_ (u"ࠢࡂ࠳࠴ࡽ࠿ࠦࡰࡢࡶࡦ࡬ࡪࡪࠠࡱࡣࡪࡩ࠳ࡩ࡬ࡰࡵࡨࠬ࠮ࠦࡡࡵࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡱ࡫ࡶࡦ࡮ࠣࡪࡴࡸࠠࡃࡧ࡫ࡥࡻ࡫ࠫࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᇍ"))
                            except Exception as _1l11ll11ll_opy_:
                                logger.debug(bstack1l1llll_opy_ (u"ࠣࡃ࠴࠵ࡾࡀࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡺࡣࡩࠢࡳࡥ࡬࡫࠮ࡤ࡮ࡲࡷࡪ࠮ࠩࠡࡣࡷࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦ࡬ࡦࡸࡨࡰ࠿ࠦࡻࡾࠤᇎ").format(_1l11ll11ll_opy_))
                    except Exception as exc:
                        logger.debug(bstack1l1llll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡻࡰࡥࡣࡷࡩࠥࡶࡡࡨࡧࠣ࡭ࡳࠦࡷࡳࡣࡳࡴࡪࡸ࠺ࠡࠧࡶࠦᇏ"), exc)
                    return page
                bstack11lllll1l1_opy_.new_page = _1l1lllllll_opy_
                bstack11lllll1l1_opy_._bstack_new_page_patched = True
        except Exception as exc:
            logger.debug(bstack1l1llll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡶࡦ࡬࡙ࠥࡹ࡯ࡥࡅࡶࡴࡽࡳࡦࡴ࠱ࡲࡪࡽ࡟ࡱࡣࡪࡩࠥ࡬࡯ࡳࠢࡳࡥ࡬࡫ࠠࡤࡣࡳࡸࡺࡸࡥ࠻ࠢࠨࡷࠧᇐ"), exc)
        try:
            from playwright.sync_api import Page as bstack11lll1l11l_opy_, Browser as _11llllllll_opy_
            if not hasattr(bstack11lll1l11l_opy_, bstack1l1llll_opy_ (u"ࠫࡤࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡨࡧࡢࡧࡱࡵࡳࡦࡡࡳࡥࡹࡩࡨࡦࡦࠪᇑ")):
                _1l1ll11ll1l_opy_ = bstack11lll1l11l_opy_.close
                def _1ll111l1l11_opy_(page_self, *bstack11l1l1l11l_opy_, _bstack_sdk_close=False, **bstack1111l1l11_opy_):
                    if not _bstack_sdk_close:
                        if getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫᇒ"), None):
                            try:
                                from browserstack_sdk.sdk_cli.cli import SDKCLI as _1111111l1l_opy_
                                _1l1lll1ll1_opy_ = _1111111l1l_opy_._instance
                                if _1l1lll1ll1_opy_ and _1l1lll1ll1_opy_.is_running():
                                    _1ll11l1l11_opy_ = getattr(_1l1lll1ll1_opy_, bstack1l1llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᇓ"), None)
                                    if _1ll11l1l11_opy_:
                                        _1ll11l1l11_opy_.stop_capture_before_browser_close(page_self)
                            except Exception as _11l1l1111l_opy_:
                                logger.debug(bstack1l1llll_opy_ (u"ࠢࡂ࠳࠴ࡽࠥࡹࡴࡰࡲࡢࡧࡦࡶࡴࡶࡴࡨࠤࡧ࡫ࡦࡰࡴࡨࠤࡵࡧࡧࡦ࠰ࡦࡰࡴࡹࡥࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࡾࢁࠧᇔ").format(_11l1l1111l_opy_))
                        logger.debug(bstack1l1llll_opy_ (u"ࠣࡆࡨࡪࡪࡸࡲࡦࡦࠣࡴࡦ࡭ࡥ࠯ࡥ࡯ࡳࡸ࡫ࠨࠪࠢ⠗ࠤࡼ࡯࡬࡭ࠢࡦࡰࡴࡹࡥࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧᇕ"))
                        threading.current_thread().bstack_deferred_page_close = True
                        threading.current_thread().bstack_deferred_page_ref = page_self
                        return
                    return _1l1ll11ll1l_opy_(page_self, *bstack11l1l1l11l_opy_, **bstack1111l1l11_opy_)
                bstack11lll1l11l_opy_.close = _1ll111l1l11_opy_
                bstack11lll1l11l_opy_._bstack_page_close_patched = True
            if not hasattr(_11llllllll_opy_, bstack1l1llll_opy_ (u"ࠩࡢࡦࡸࡺࡡࡤ࡭ࡢࡦࡷࡵࡷࡴࡧࡵࡣࡨࡲ࡯ࡴࡧࡢࡴࡦࡺࡣࡩࡧࡧࠫᇖ")):
                _1llll1l1lll_opy_ = _11llllllll_opy_.close
                def _1111l11l1l_opy_(bstack11l11l1lll_opy_, *bstack11l1lll111_opy_, _bstack_sdk_close=False, **bstack1ll11111ll_opy_):
                    if not _bstack_sdk_close:
                        logger.debug(bstack1l1llll_opy_ (u"ࠥࡈࡪ࡬ࡥࡳࡴࡨࡨࠥࡨࡲࡰࡹࡶࡩࡷ࠴ࡣ࡭ࡱࡶࡩ࠭࠯ࠠ⠕ࠢࡺ࡭ࡱࡲࠠࡤ࡮ࡲࡷࡪࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥᇗ"))
                        threading.current_thread().bstack_deferred_browser_close = True
                        threading.current_thread().bstack_deferred_browser_ref = bstack11l11l1lll_opy_
                        return
                    return _1llll1l1lll_opy_(bstack11l11l1lll_opy_, *bstack11l1lll111_opy_, **bstack1ll11111ll_opy_)
                _11llllllll_opy_.close = _1111l11l1l_opy_
                _11llllllll_opy_._bstack_browser_close_patched = True
        except Exception as exc:
            logger.debug(bstack1l1llll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡧࠣࡨࡪ࡬ࡥࡳࡴࡨࡨࠥࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡦࡰࡴࡹࡥࠡࡪࡲࡳࡰࡹ࠺ࠡࠧࡶࠦᇘ"), exc)
        logger.debug(bstack1l1llll_opy_ (u"ࠧࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡆࡵ࡭ࡻ࡫ࡲࡘࡴࡤࡴࡵ࡫ࡲࡅ࡫ࡵࡩࡨࡺࠠࡴࡧࡷࡹࡵࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࠡࡨࡲࡶࠥࡺࡨࡳࡧࡤࡨࠥࢁࡽࠣᇙ").format(threading.get_ident()))
    except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡽࡲࡢࡲࡳࡩࡷࡀࠠࡼࡿࠥᇚ").format(str(e)))
    return browser
  async def bstack1l11ll11l1_opy_(self, *args, **kwargs):
    global bstack11l1111lll_opy_, CONFIG, FRAMEWORK_NAME, __version__, BROWSERSTACK_AUTOMATION
    global PLATFORM_INDEX, PARALLELISE_VANILLA_PYTHON, PARALLELISE_THREADING_PYTHON, SESSION_NAME
    import urllib.parse as _1lll1l1l1l_opy_
    import json
    if FRAMEWORK_NAME and bstack1l1llll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧᇛ") in str(FRAMEWORK_NAME).lower() and os.environ.get(bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡍࡕࡏࡌࡕࠪᇜ")):
        logger.debug(bstack1l1llll_opy_ (u"ࠤࡰࡳࡩࡥࡣࡰࡰࡱࡩࡨࡺ࠺ࠡࡄࡨ࡬ࡦࡼࡥࠡࡄ࡬ࡲࡦࡸࡹࠡࡈ࡯ࡳࡼࠦ⠔ࠡࡦࡨࡪࡪࡸࡲࡪࡰࡪࠤࡹࡵࠠࡔࡆࡎࠤࡈࡒࡉࠡࡪࡲࡳࡰࡹࠢᇝ"))
        return await bstack11l1111lll_opy_(self, *args, **kwargs)
    ws_endpoint = (
      args[0] if args else
      kwargs.get(bstack1l1llll_opy_ (u"ࠪࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺࠧᇞ"),
        kwargs.get(bstack1l1llll_opy_ (u"ࠫࡼࡹ࡟ࡦࡰࡧࡴࡴ࡯࡮ࡵࠩᇟ"),
          kwargs.get(bstack1l1llll_opy_ (u"ࠬ࡫࡮ࡥࡲࡲ࡭ࡳࡺࠧᇠ"), bstack1l1llll_opy_ (u"࠭ࠧᇡ")))))
    bstack1l1lll1l1l_opy_ = (ws_endpoint
                 and bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪᇢ") in str(ws_endpoint)
                 and bstack1l1llll_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧᇣ") in str(ws_endpoint))
    bstack1l1l11l1ll_opy_ = {}
    if bstack1l1lll1l1l_opy_:
        from bstack_utils.helper import is_bstack_automation
        bstack1l1ll1l1l1_opy_ = is_bstack_automation()
        try:
            if bstack1l1ll1l1l1_opy_:
                CONFIG[bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫᇤ")] = str(FRAMEWORK_NAME) + str(__version__)
                bstack1111l1ll11_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᇥ"), bstack1l1llll_opy_ (u"ࠫࠬᇦ"))
                if bstack1111l1ll11_opy_:
                    CONFIG[bstack1l1llll_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨᇧ")] = bstack1111l1ll11_opy_
                CONFIG[bstack1l1llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨᇨ")] = TestHubUtils.bstack1l11111lll_opy_(CONFIG, FRAMEWORK_NAME)
                bstack1ll1l111l1_opy_ = 0 if PLATFORM_INDEX < 0 else PLATFORM_INDEX
                try:
                    if PARALLELISE_VANILLA_PYTHON is True:
                        bstack1ll1l111l1_opy_ = int(multiprocessing.current_process().name)
                    elif PARALLELISE_THREADING_PYTHON is True:
                        bstack1ll1l111l1_opy_ = int(threading.current_thread().name)
                except Exception:
                    bstack1ll1l111l1_opy_ = 0
                CONFIG[bstack1l1llll_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨᇩ")] = True
                bstack1l1l11l1ll_opy_ = get_caps(CONFIG, bstack1ll1l111l1_opy_)
                if CONFIG.get(bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᇪ")):
                    update_caps_for_local(bstack1l1l11l1ll_opy_)
                if bstack1l1llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᇫ") in CONFIG and bstack1l1llll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᇬ") in CONFIG[bstack1l1llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᇭ")][bstack1ll1l111l1_opy_]:
                    SESSION_NAME = CONFIG[bstack1l1llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᇮ")][bstack1ll1l111l1_opy_][bstack1l1llll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᇯ")]
                logger.debug(bstack1l1llll_opy_ (u"ࠢࡄࡣࡶࡩࠥࡇ࠺ࠡࡔࡨࡴࡱࡧࡣࡦࡦࠣࡹࡸ࡫ࡲࠡࡥࡤࡴࡸࠦࡷࡪࡶ࡫ࠤࡾࡳ࡬ࠡࡥࡤࡴࡸࡀࠠࡼࡿࠥᇰ").format(str(bstack1l1l11l1ll_opy_)))
            else:
                try:
                    bstack1l1ll11ll1_opy_ = str(ws_endpoint).split(bstack1l1llll_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧᇱ"))[1]
                    bstack1l1l11l1ll_opy_ = json.loads(_1lll1l1l1l_opy_.unquote(bstack1l1ll11ll1_opy_)) or {}
                except Exception:
                    bstack1l1l11l1ll_opy_ = {}
                bstack1111l1ll11_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᇲ"), bstack1l1llll_opy_ (u"ࠪࠫᇳ"))
                bstack1l1l111lll_opy_ = TestHubUtils.bstack1l11111lll_opy_(CONFIG, FRAMEWORK_NAME)
                bstack1l1l11l1ll_opy_[bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬᇴ")] = str(FRAMEWORK_NAME) + str(__version__)
                bstack1l1l11l1ll_opy_[bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᇵ")] = BROWSERSTACK_AUTOMATION
                if bstack1111l1ll11_opy_:
                    bstack1l1l11l1ll_opy_[bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨᇶ")] = bstack1111l1ll11_opy_
                bstack1l1l11l1ll_opy_[bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨᇷ")] = bstack1l1l111lll_opy_
            ws_url = str(ws_endpoint).split(bstack1l1llll_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧᇸ"))[0]
            ws_endpoint = ws_url + bstack1l1llll_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨᇹ") + _1lll1l1l1l_opy_.quote(json.dumps(bstack1l1l11l1ll_opy_))
            if args:
                args = (ws_endpoint,) + args[1:]
            elif bstack1l1llll_opy_ (u"ࠪࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺࠧᇺ") in kwargs:
                kwargs[bstack1l1llll_opy_ (u"ࠫࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴࠨᇻ")] = ws_endpoint
            elif bstack1l1llll_opy_ (u"ࠬࡽࡳࡠࡧࡱࡨࡵࡵࡩ࡯ࡶࠪᇼ") in kwargs:
                kwargs[bstack1l1llll_opy_ (u"࠭ࡷࡴࡡࡨࡲࡩࡶ࡯ࡪࡰࡷࠫᇽ")] = ws_endpoint
            elif bstack1l1llll_opy_ (u"ࠧࡦࡰࡧࡴࡴ࡯࡮ࡵࠩᇾ") in kwargs:
                kwargs[bstack1l1llll_opy_ (u"ࠨࡧࡱࡨࡵࡵࡩ࡯ࡶࠪᇿ")] = ws_endpoint
        except Exception as e:
            logger.debug(bstack1l1llll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡥࡳࡩࡨࠤࡨࡧࡰࡴࠢ࡬ࡲࡹࡵࠠࡤࡱࡱࡲࡪࡩࡴࠡࡗࡕࡐ࠿ࠦࡻࡾࠤሀ").format(str(e)))
        try:
            from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
            PlaywrightDriverWrapperDirect.setup_dispatch_capture()
        except Exception as exc:
            logger.debug(bstack1l1llll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࡸࡴࠥࡪࡩࡴࡲࡤࡸࡨ࡮ࠠࡤࡣࡳࡸࡺࡸࡥࠡ࡫ࡱࠤࡲࡵࡤࡠࡥࡲࡲࡳ࡫ࡣࡵ࠼ࠣࠩࡸࠨሁ"), exc)
    browser = await bstack11l1111lll_opy_(self, *args, **kwargs)
    if bstack1l1lll1l1l_opy_:
        try:
            from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
            wrapper = PlaywrightDriverWrapperDirect(browser, page=None, capabilities=bstack1l1l11l1ll_opy_, config=CONFIG)
            threading.current_thread().bstackSessionDriver = wrapper
            logger.debug(bstack1l1llll_opy_ (u"ࠦࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡅࡴ࡬ࡺࡪࡸࡗࡳࡣࡳࡴࡪࡸࡄࡪࡴࡨࡧࡹࠦࡳࡦࡶࡸࡴࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫ࠠࡧࡱࡵࠤࡹ࡮ࡲࡦࡣࡧࠤࠪࡹࠢሂ"), threading.get_ident())
            threading.current_thread().bstackTestErrorMessages = []
            if wrapper.session_id and not wrapper._cbt_info_sent:
                PlaywrightDriverWrapperDirect._send_cbt_info_on_session()
            try:
                from playwright.sync_api import Browser as bstack11lllll1l1_opy_
                if not hasattr(bstack11lllll1l1_opy_, bstack1l1llll_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥ࡮ࡦࡹࡢࡴࡦ࡭ࡥࡠࡲࡤࡸࡨ࡮ࡥࡥࠩሃ")):
                    _1l1lll11lll_opy_ = bstack11lllll1l1_opy_.new_page
                    def _1l1lllllll_opy_(bstack11l11l1lll_opy_, *bstack1l11l1ll1l_opy_, **bstack11ll111l1l_opy_):
                        page = _1l1lll11lll_opy_(bstack11l11l1lll_opy_, *bstack1l11l1ll1l_opy_, **bstack11ll111l1l_opy_)
                        try:
                            _w = getattr(threading.current_thread(), bstack1l1llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬሄ"), None)
                            if _w and hasattr(_w, bstack1l1llll_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫࡟ࡱࡣࡪࡩࠬህ")):
                                _w.update_page(page)
                        except Exception as exc:
                            logger.debug(bstack1l1llll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡺࡶࡤࡢࡶࡨࠤࡵࡧࡧࡦࠢ࡬ࡲࠥࡽࡲࡢࡲࡳࡩࡷࠦࠨ࡮ࡱࡧࡣࡨࡵ࡮࡯ࡧࡦࡸ࠮ࡀࠠࠦࡵࠥሆ"), exc)
                        return page
                    bstack11lllll1l1_opy_.new_page = _1l1lllllll_opy_
                    bstack11lllll1l1_opy_._bstack_new_page_patched = True
            except Exception as exc:
                logger.debug(bstack1l1llll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡵࡥ࡫ࠤࡘࡿ࡮ࡤࡄࡵࡳࡼࡹࡥࡳ࠰ࡱࡩࡼࡥࡰࡢࡩࡨࠤ࡮ࡴࠠ࡮ࡱࡧࡣࡨࡵ࡮࡯ࡧࡦࡸ࠿ࠦࠥࡴࠤሇ"), exc)
            try:
                from playwright.sync_api import Page as bstack11lll1l11l_opy_, Browser as _11llllllll_opy_
                if not hasattr(bstack11lll1l11l_opy_, bstack1l1llll_opy_ (u"ࠪࡣࡧࡹࡴࡢࡥ࡮ࡣࡵࡧࡧࡦࡡࡦࡰࡴࡹࡥࡠࡲࡤࡸࡨ࡮ࡥࡥࠩለ")):
                    _1l1ll11ll1l_opy_ = bstack11lll1l11l_opy_.close
                    def _1ll111l1l11_opy_(page_self, *bstack11l1l1l11l_opy_, _bstack_sdk_close=False, **bstack1111l1l11_opy_):
                        if not _bstack_sdk_close:
                            logger.debug(bstack1l1llll_opy_ (u"ࠦࡉ࡫ࡦࡦࡴࡵࡩࡩࠦࡰࡢࡩࡨ࠲ࡨࡲ࡯ࡴࡧࠫ࠭ࠥ⠚ࠠࡸ࡫࡯ࡰࠥࡩ࡬ࡰࡵࡨࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣሉ"))
                            threading.current_thread().bstack_deferred_page_close = True
                            threading.current_thread().bstack_deferred_page_ref = page_self
                            return
                        return _1l1ll11ll1l_opy_(page_self, *bstack11l1l1l11l_opy_, **bstack1111l1l11_opy_)
                    bstack11lll1l11l_opy_.close = _1ll111l1l11_opy_
                    bstack11lll1l11l_opy_._bstack_page_close_patched = True
                if not hasattr(_11llllllll_opy_, bstack1l1llll_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥࡢࡳࡱࡺࡷࡪࡸ࡟ࡤ࡮ࡲࡷࡪࡥࡰࡢࡶࡦ࡬ࡪࡪࠧሊ")):
                    _1llll1l1lll_opy_ = _11llllllll_opy_.close
                    def _1111l11l1l_opy_(bstack11l11l1lll_opy_, *bstack11l1lll111_opy_, _bstack_sdk_close=False, **bstack1ll11111ll_opy_):
                        if not _bstack_sdk_close:
                            logger.debug(bstack1l1llll_opy_ (u"ࠨࡄࡦࡨࡨࡶࡷ࡫ࡤࠡࡤࡵࡳࡼࡹࡥࡳ࠰ࡦࡰࡴࡹࡥࠩࠫࠣ⠘ࠥࡽࡩ࡭࡮ࠣࡧࡱࡵࡳࡦࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨላ"))
                            threading.current_thread().bstack_deferred_browser_close = True
                            threading.current_thread().bstack_deferred_browser_ref = bstack11l11l1lll_opy_
                            return
                        return _1llll1l1lll_opy_(bstack11l11l1lll_opy_, *bstack11l1lll111_opy_, **bstack1ll11111ll_opy_)
                    _11llllllll_opy_.close = _1111l11l1l_opy_
                    _11llllllll_opy_._bstack_browser_close_patched = True
            except Exception as exc:
                logger.debug(bstack1l1llll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡧࡴࡴࡦࡪࡩࡸࡶࡪࠦࡤࡦࡨࡨࡶࡷ࡫ࡤࠡࡥ࡯ࡳࡸ࡫ࠠࡩࡱࡲ࡯ࡸࠦࡩ࡯ࠢࡰࡳࡩࡥࡣࡰࡰࡱࡩࡨࡺ࠺ࠡࠧࡶࠦሌ"), exc)
            logger.debug(bstack1l1llll_opy_ (u"ࠣࡎࡨ࡫ࡦࡩࡹࠡࡥࡲࡲࡳ࡫ࡣࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡸࡷࡧࡣ࡬࡫ࡱ࡫ࠥࡹࡥࡵࡷࡳࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࠦࡦࡰࡴࠣࡸ࡭ࡸࡥࡢࡦࠣࡿࢂࠨል").format(threading.get_ident()))
        except Exception as e:
            logger.debug(bstack1l1llll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࡷࡳࠤࡱ࡫ࡧࡢࡥࡼࠤࡨࡵ࡮࡯ࡧࡦࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡴࡳࡣࡦ࡯࡮ࡴࡧ࠻ࠢࡾࢁࠧሎ").format(str(e)))
    return browser
except Exception as e:
    pass
def patch_playwright():
    global SELENIUM_OR_PLAYWRIGHT_INSTALLED
    global FRAMEWORK_NAME
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import is_bstack_automation
        global bstack11l1111lll_opy_
        if not bstack11l1111lll_opy_:
            bstack11l1111lll_opy_ = BrowserType.connect
        BrowserType.connect = bstack1l11ll11l1_opy_
        _1lll1ll1ll_opy_ = (FRAMEWORK_NAME and bstack1l1llll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪሏ") in str(FRAMEWORK_NAME).lower()
                             and os.environ.get(bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡉࡑࡒࡏࡘ࠭ሐ")))
        if not _1lll1ll1ll_opy_ and is_bstack_automation():
            BrowserType.launch = bstack11111llll_opy_
            SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
        try:
            from playwright.sync_api import Page as _11111lll11_opy_
            if not hasattr(_11111lll11_opy_, bstack1l1llll_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡢࡴࡦࡺࡣࡩࡧࡧࠫሑ")):
                _11l111ll11_opy_ = _11111lll11_opy_.screenshot
                def _1ll1111l1ll_opy_(page_self, *bstack1l1ll111l1l_opy_, **bstack1l1l1111l1_opy_):
                    result = _11l111ll11_opy_(page_self, *bstack1l1ll111l1l_opy_, **bstack1l1l1111l1_opy_)
                    try:
                        from bstack_utils.testhub_handler import TestHubHandler
                        from bstack_utils.bstack11l111ll_opy_ import bstack1ll111ll_opy_
                        if bstack1ll111ll_opy_.on():
                            import base64
                            bstack1ll11l11lll_opy_ = base64.b64encode(result).decode(bstack1l1llll_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬሒ")) if isinstance(result, bytes) else str(result)
                            test_uuid = TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack1ll111ll_opy_.current_hook_uuid()
                            if test_uuid and bstack1ll11l11lll_opy_:
                                TestHubHandler.bstack1ll11ll1ll_opy_({
                                    bstack1l1llll_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭ሓ"): bstack1ll11l11lll_opy_,
                                    bstack1l1llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨሔ"): test_uuid
                                })
                                logger.debug(bstack1l1llll_opy_ (u"ࠤࡖࡩࡳࡺࠠࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠡࡶࡲࠤࡔ࠷࠱ࡺࠢࡩࡳࡷࠦࡴࡦࡵࡷࠤࢀࢃࠢሕ").format(test_uuid))
                    except Exception as bstack1llllll11l1_opy_:
                        logger.debug(bstack1l1llll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡰࡧࠤࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠥࡺ࡯ࠡࡑ࠴࠵ࡾࡀࠠࡼࡿࠥሖ").format(str(bstack1llllll11l1_opy_)))
                    return result
                _11111lll11_opy_.screenshot = _1ll1111l1ll_opy_
                _11111lll11_opy_._bstack_screenshot_patched = True
        except Exception as e:
            logger.debug(bstack1l1llll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡷࡧ࡭ࠦࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺ࠺ࠡࠧࡶࠦሗ"), e)
        try:
            from playwright.sync_api import Page as _1lllll1l111_opy_
            if not hasattr(_1lllll1l111_opy_, bstack1l1llll_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥࡡ࠲࠳ࡼࡣࡸࡺࡵࡣࡡࡰࡩࡹ࡮࡯ࡥࡵࡢࡴࡦࡺࡣࡩࡧࡧࠫመ")):
                def _1l1ll11lll_opy_(_bstack_a11y_label):
                    def _1lll1l1l11l_opy_(page_self, *_a, **_1ll11lllll1_opy_):
                        _bstack_a11y_msg = bstack1l1llll_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࠣሙ") + _bstack_a11y_label + bstack1l1llll_opy_ (u"ࠢ࠯ࠤሚ")
                        logger.warning(_bstack_a11y_msg)
                        return {}
                    return _1lll1l1l11l_opy_
                _1lllll1l111_opy_.getAccessibilityResults = _1l1ll11lll_opy_(bstack1l1llll_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࡴࠤማ"))
                _1lllll1l111_opy_.get_accessibility_results = _1l1ll11lll_opy_(bstack1l1llll_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡵࠥሜ"))
                _1lllll1l111_opy_.getAccessibilityResultsSummary = _1l1ll11lll_opy_(bstack1l1llll_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡶࠤࡸࡻ࡭࡮ࡣࡵࡽࠧም"))
                _1lllll1l111_opy_.get_accessibility_results_summary = _1l1ll11lll_opy_(bstack1l1llll_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡹࡵ࡮࡯ࡤࡶࡾࠨሞ"))
                _1lllll1l111_opy_._bstack_a11y_stub_methods_patched = True
        except Exception as e:
            logger.debug(bstack1l1llll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡸࡨ࡮ࠠࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡆ࠷࠱ࡺࠢࡶࡸࡺࡨࠠ࡮ࡧࡷ࡬ࡴࡪࡳ࠻ࠢࠨࡷࠧሟ"), e)
        try:
            from playwright.sync_api._context_manager import PlaywrightContextManager
            if not hasattr(PlaywrightContextManager, bstack1l1llll_opy_ (u"࠭࡟ࡣࡵࡷࡥࡨࡱ࡟ࡦࡰࡷࡩࡷࡥࡰࡢࡶࡦ࡬ࡪࡪࠧሠ")):
                _1l1lll11ll1_opy_ = PlaywrightContextManager.__enter__
                def _1l1lll111ll_opy_(bstack1lll11ll111_opy_):
                    pw = _1l1lll11ll1_opy_(bstack1lll11ll111_opy_)
                    _1ll1ll11ll_opy_ = pw.stop
                    import browserstack_sdk
                    _thread_id = threading.get_ident()
                    try:
                        with browserstack_sdk._PLAYWRIGHT_ACTIVE_THREADS_LOCK:
                            browserstack_sdk._PLAYWRIGHT_ACTIVE_THREADS.add(_thread_id)
                    except Exception:
                        pass
                    _1l111l11_opy_ = threading.current_thread()
                    _1l111l11_opy_.bstack_deferred_pw_ref = pw
                    _1l111l11_opy_.bstack_deferred_pw_stop_fn = _1ll1ll11ll_opy_
                    def _1ll1ll111l1_opy_(*args, _bstack_sdk_close=False, **kwargs):
                        if not _bstack_sdk_close:
                            logger.debug(bstack1l1llll_opy_ (u"ࠢࡅࡧࡩࡩࡷࡸࡥࡥࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠴ࡳࡵࡱࡳࠬ࠮ࠦ⠔ࠡࡹ࡬ࡰࡱࠦࡳࡵࡱࡳࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣሡ"))
                            threading.current_thread().bstack_deferred_pw_stop = True
                            return
                        return _1ll1ll11ll_opy_()
                    pw.stop = _1ll1ll111l1_opy_
                    return pw
                PlaywrightContextManager.__enter__ = _1l1lll111ll_opy_
                PlaywrightContextManager._bstack_enter_patched = True
        except Exception as e:
            logger.debug(bstack1l1llll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡴࡤࡪࠣࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࡃࡰࡰࡷࡩࡽࡺࡍࡢࡰࡤ࡫ࡪࡸ࠮ࡠࡡࡨࡲࡹ࡫ࡲࡠࡡ࠽ࠤࠪࡹࠢሢ"), e)
        if is_bstack_automation():
            try:
                from playwright.sync_api import Page as _11111lll11_opy_, Browser as _11llllllll_opy_
                if not hasattr(_11111lll11_opy_, bstack1l1llll_opy_ (u"ࠩࡢࡦࡸࡺࡡࡤ࡭ࡢࡴࡦ࡭ࡥࡠࡥ࡯ࡳࡸ࡫࡟ࡱࡣࡷࡧ࡭࡫ࡤࠨሣ")):
                    _1lll111l11_opy_ = _11111lll11_opy_.close
                    def _1l1ll11l1l1_opy_(page_self, *_1l1l111llll_opy_, _bstack_sdk_close=False, **_1l1ll1ll11_opy_):
                        if not _bstack_sdk_close:
                            if getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩሤ"), None):
                                try:
                                    from browserstack_sdk.sdk_cli.cli import SDKCLI as _1111111l1l_opy_
                                    _1l1lll1ll1_opy_ = _1111111l1l_opy_._instance
                                    if _1l1lll1ll1_opy_ and _1l1lll1ll1_opy_.is_running():
                                        _1111l1ll1_opy_ = getattr(_1l1lll1ll1_opy_, bstack1l1llll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫሥ"), None)
                                        if _1111l1ll1_opy_:
                                            _1111l1ll1_opy_.stop_capture_before_browser_close(page_self)
                                except Exception as _1l1l111ll1l_opy_:
                                    logger.debug(bstack1l1llll_opy_ (u"ࠧࡇ࠱࠲ࡻࠣࡷࡹࡵࡰࡠࡥࡤࡴࡹࡻࡲࡦࠢࡥࡩ࡫ࡵࡲࡦࠢࡳࡥ࡬࡫࠮ࡤ࡮ࡲࡷࡪࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࡼࡿࠥሦ").format(_1l1l111ll1l_opy_))
                            logger.debug(bstack1l1llll_opy_ (u"ࠨࡄࡦࡨࡨࡶࡷ࡫ࡤࠡࡲࡤ࡫ࡪ࠴ࡣ࡭ࡱࡶࡩ࠭࠯ࠠ⠕ࠢࡺ࡭ࡱࡲࠠࡤ࡮ࡲࡷࡪࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥሧ"))
                            threading.current_thread().bstack_deferred_page_close = True
                            threading.current_thread().bstack_deferred_page_ref = page_self
                            return
                        return _1lll111l11_opy_(page_self, *_1l1l111llll_opy_, **_1l1ll1ll11_opy_)
                    _11111lll11_opy_.close = _1l1ll11l1l1_opy_
                    _11111lll11_opy_._bstack_page_close_patched = True
                if not hasattr(_11llllllll_opy_, bstack1l1llll_opy_ (u"ࠧࡠࡤࡶࡸࡦࡩ࡫ࡠࡤࡵࡳࡼࡹࡥࡳࡡࡦࡰࡴࡹࡥࡠࡲࡤࡸࡨ࡮ࡥࡥࠩረ")):
                    _1llll1ll1l1_opy_ = _11llllllll_opy_.close
                    def _1lllll1l1l1_opy_(bstack11l11l1lll_opy_, *_1ll1l11l1l_opy_, _bstack_sdk_close=False, **_1ll11l1lll1_opy_):
                        if not _bstack_sdk_close:
                            logger.debug(bstack1l1llll_opy_ (u"ࠣࡆࡨࡪࡪࡸࡲࡦࡦࠣࡦࡷࡵࡷࡴࡧࡵ࠲ࡨࡲ࡯ࡴࡧࠫ࠭ࠥ⠚ࠠࡸ࡫࡯ࡰࠥࡩ࡬ࡰࡵࡨࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣሩ"))
                            threading.current_thread().bstack_deferred_browser_close = True
                            threading.current_thread().bstack_deferred_browser_ref = bstack11l11l1lll_opy_
                            return
                        return _1llll1ll1l1_opy_(bstack11l11l1lll_opy_, *_1ll1l11l1l_opy_, **_1ll11l1lll1_opy_)
                    _11llllllll_opy_.close = _1lllll1l1l1_opy_
                    _11llllllll_opy_._bstack_browser_close_patched = True
            except Exception as _1l1l1111l11_opy_:
                logger.debug(bstack1l1llll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡥࠡࡩ࡯ࡳࡧࡧ࡬ࠡࡦࡨࡪࡪࡸࡲࡦࡦࠣࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡤ࡮ࡲࡷࡪࠦࡨࡰࡱ࡮ࡷ࠿ࠦࠥࡴࠤሪ"), _1l1l1111l11_opy_)
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1ll1lll1lll_opy_
      SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
    except Exception as e:
      pass
def playwright_set_session_name(context, bstack1l1ll11l1ll_opy_):
  try:
    if getattr(context, bstack1l1llll_opy_ (u"ࠪࡴࡦ࡭ࡥࠨራ"), None):
      context.page.evaluate(bstack1l1llll_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧሬ"), bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠩር")+ json.dumps(bstack1l1ll11l1ll_opy_) + bstack1l1llll_opy_ (u"ࠨࡽࡾࠤሮ"))
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢࡾࢁ࠿ࠦࡻࡾࠤሯ").format(str(e), traceback.format_exc()))
def playwright_annotate(context, message, level):
  try:
    if getattr(context, bstack1l1llll_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭ሰ"), None):
      context.page.evaluate(bstack1l1llll_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥሱ"), bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨሲ") + json.dumps(message) + bstack1l1llll_opy_ (u"ࠫ࠱ࠨ࡬ࡦࡸࡨࡰࠧࡀࠧሳ") + json.dumps(level) + bstack1l1llll_opy_ (u"ࠬࢃࡽࠨሴ"))
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠦࡻࡾ࠼ࠣࡿࢂࠨስ").format(str(e), traceback.format_exc()))
@measure(event_name=EVENTS.bstack1l1llll1l1_opy_, stage=STAGE.SINGLE, bstack11lllll111_opy_=SESSION_NAME)
def bstack1ll1ll11l1l_opy_(self, url):
  global bstack11l1111111_opy_
  try:
    bstack1l1l1llll1l_opy_(url)
  except Exception as err:
    logger.debug(bstack11l1l1ll1l_opy_.format(str(err)))
  try:
    bstack11l1111111_opy_(self, url)
  except Exception as e:
    try:
      parsed_error = str(e)
      if any(err_msg in parsed_error for err_msg in bstack1111ll111l_opy_):
        bstack1l1l1llll1l_opy_(url, True)
    except Exception as err:
      logger.debug(bstack11l1l1ll1l_opy_.format(str(err)))
    raise e
def bstack1ll111l11l_opy_(self):
  global bstack1111lll111_opy_
  bstack1111lll111_opy_ = self
  return
def bstack1ll11l11l11_opy_(self):
  global bstack1ll1l11l111_opy_
  bstack1ll1l11l111_opy_ = self
  return
def bstack11lll11ll1_opy_(test_name, bstack1l1l1111l1l_opy_):
  global CONFIG
  if percy.bstack1lll11llll1_opy_() == bstack1l1llll_opy_ (u"ࠢࡵࡴࡸࡩࠧሶ"):
    bstack1ll1lllllll_opy_ = os.path.relpath(bstack1l1l1111l1l_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack1ll1lllllll_opy_)
    bstack11lllll111_opy_ = suite_name + bstack1l1llll_opy_ (u"ࠣ࠯ࠥሷ") + test_name
    threading.current_thread().percySessionName = bstack11lllll111_opy_
def bstack1l1l11l1111_opy_(self, test, *args, **kwargs):
  global bstack111l1l111l_opy_
  test_name = None
  bstack1l1l1111l1l_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1l1l1111l1l_opy_ = str(test.source)
  bstack11lll11ll1_opy_(test_name, bstack1l1l1111l1l_opy_)
  bstack111l1l111l_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.SDK_AUTOMATE_SESSION_ANNOTATION, stage=STAGE.SINGLE, bstack11lllll111_opy_=SESSION_NAME)
def bstack11ll1ll11l_opy_(driver, bstack11lllll111_opy_):
  if not bstack11l11l1l1l_opy_ and bstack11lllll111_opy_:
      bstack11111ll1l1_opy_ = {
          bstack1l1llll_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩሸ"): bstack1l1llll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫሹ"),
          bstack1l1llll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧሺ"): {
              bstack1l1llll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪሻ"): bstack11lllll111_opy_
          }
      }
      bstack1lll111111_opy_ = bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫሼ").format(json.dumps(bstack11111ll1l1_opy_))
      driver.execute_script(bstack1lll111111_opy_)
  if bstack1l1lllll1l_opy_:
      bstack11ll1l1l1l_opy_ = {
          bstack1l1llll_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧሽ"): bstack1l1llll_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪሾ"),
          bstack1l1llll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬሿ"): {
              bstack1l1llll_opy_ (u"ࠪࡨࡦࡺࡡࠨቀ"): bstack11lllll111_opy_ + bstack1l1llll_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭ቁ"),
              bstack1l1llll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫቂ"): bstack1l1llll_opy_ (u"࠭ࡩ࡯ࡨࡲࠫቃ")
          }
      }
      if bstack1l1lllll1l_opy_.status == bstack1l1llll_opy_ (u"ࠧࡑࡃࡖࡗࠬቄ"):
          bstack1l1l11111l_opy_ = bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ቅ").format(json.dumps(bstack11ll1l1l1l_opy_))
          driver.execute_script(bstack1l1l11111l_opy_)
          bstack1l1lll1ll1l_opy_(driver, bstack1l1llll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩቆ"))
      elif bstack1l1lllll1l_opy_.status == bstack1l1llll_opy_ (u"ࠪࡊࡆࡏࡌࠨቇ"):
          reason = bstack1l1llll_opy_ (u"ࠦࠧቈ")
          bstack11llll11ll_opy_ = bstack11lllll111_opy_ + bstack1l1llll_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩ࠭቉")
          if bstack1l1lllll1l_opy_.message:
              reason = str(bstack1l1lllll1l_opy_.message)
              bstack11llll11ll_opy_ = bstack11llll11ll_opy_ + bstack1l1llll_opy_ (u"࠭ࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵ࠾ࠥ࠭ቊ") + reason
          bstack11ll1l1l1l_opy_[bstack1l1llll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪቋ")] = {
              bstack1l1llll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧቌ"): bstack1l1llll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨቍ"),
              bstack1l1llll_opy_ (u"ࠪࡨࡦࡺࡡࠨ቎"): bstack11llll11ll_opy_
          }
          bstack1l1l11111l_opy_ = bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩ቏").format(json.dumps(bstack11ll1l1l1l_opy_))
          driver.execute_script(bstack1l1l11111l_opy_)
          bstack1l1lll1ll1l_opy_(driver, bstack1l1llll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬቐ"), reason)
          bstack1ll1l1l11l_opy_(reason, str(bstack1l1lllll1l_opy_), str(PLATFORM_INDEX), logger)
@measure(event_name=EVENTS.bstack11l1l111ll_opy_, stage=STAGE.SINGLE, bstack11lllll111_opy_=SESSION_NAME)
def bstack1lllllllll1_opy_(driver, test):
  if percy.bstack1lll11llll1_opy_() == bstack1l1llll_opy_ (u"ࠨࡴࡳࡷࡨࠦቑ") and percy.bstack1l1ll1l1lll_opy_() == bstack1l1llll_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤቒ"):
      bstack11lll11lll_opy_ = bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠨࡲࡨࡶࡨࡿࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫቓ"), None)
      bstack11ll111111_opy_(driver, bstack11lll11lll_opy_, test)
  if (bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ቔ"), None) and
      bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩቕ"), None)) or (
      bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫቖ"), None) and
      bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ቗"), None)):
      logger.info(bstack1l1llll_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠤࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡩࡴࠢࡸࡲࡩ࡫ࡲࡸࡣࡼ࠲ࠥࠨቘ"))
      a11y.bstack11ll11lll_opy_(driver, name=test.name, path=test.source)
def bstack1l1l111l11_opy_(test, bstack11lllll111_opy_):
    try:
      time_start = datetime.datetime.now()
      data = {}
      if test:
        data[bstack1l1llll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ቙")] = bstack11lllll111_opy_
      if bstack1l1lllll1l_opy_:
        if bstack1l1lllll1l_opy_.status == bstack1l1llll_opy_ (u"ࠨࡒࡄࡗࡘ࠭ቚ"):
          data[bstack1l1llll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩቛ")] = bstack1l1llll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪቜ")
        elif bstack1l1lllll1l_opy_.status == bstack1l1llll_opy_ (u"ࠫࡋࡇࡉࡍࠩቝ"):
          data[bstack1l1llll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ቞")] = bstack1l1llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭቟")
          if bstack1l1lllll1l_opy_.message:
            data[bstack1l1llll_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧበ")] = str(bstack1l1lllll1l_opy_.message)
      user = CONFIG[bstack1l1llll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪቡ")]
      key = CONFIG[bstack1l1llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬቢ")]
      host = bstack11l11l111l_opy_(cli.config, [bstack1l1llll_opy_ (u"ࠥࡥࡵ࡯ࡳࠣባ"), bstack1l1llll_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸࡪࠨቤ"), bstack1l1llll_opy_ (u"ࠧࡧࡰࡪࠤብ")], bstack1l1llll_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡲ࡬࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠢቦ"))
      url = bstack1l1llll_opy_ (u"ࠧࡼࡿ࠲ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡹࡥࡴࡵ࡬ࡳࡳࡹ࠯ࡼࡿ࠱࡮ࡸࡵ࡮ࠨቧ").format(host, bstack11llll1l11_opy_)
      headers = {
        bstack1l1llll_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧቨ"): bstack1l1llll_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬቩ"),
      }
      if bool(data):
        from bstack_utils.helper import get_ca_cert_path
        bstack1l1l1ll111_opy_ = {bstack1l1llll_opy_ (u"ࠪ࡮ࡸࡵ࡮ࠨቪ"): data, bstack1l1llll_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬቫ"): headers, bstack1l1llll_opy_ (u"ࠬࡧࡵࡵࡪࠪቬ"): (user, key)}
        cert_path = get_ca_cert_path(CONFIG)
        if cert_path:
          bstack1l1l1ll111_opy_[bstack1l1llll_opy_ (u"࠭ࡶࡦࡴ࡬ࡪࡾ࠭ቭ")] = cert_path
        requests.put(url, **bstack1l1l1ll111_opy_)
        cli.add_benchmark(bstack1l1llll_opy_ (u"ࠢࡩࡶࡷࡴ࠿ࡻࡰࡥࡣࡷࡩࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡸࡺࡡࡵࡷࡶࠦቮ"), datetime.datetime.now() - time_start)
    except Exception as e:
      logger.error(bstack11ll1ll1l1_opy_.format(str(e)))
def bstack11l1ll1ll1_opy_(test, bstack11lllll111_opy_):
  global CONFIG
  global bstack1ll1l11l111_opy_
  global bstack1111lll111_opy_
  global bstack11llll1l11_opy_
  global bstack1l1lllll1l_opy_
  global SESSION_NAME
  global bstack1l1ll1ll11l_opy_
  global bstack1111lll1l1_opy_
  global bstack1111llll11_opy_
  global bstack1lll1ll11ll_opy_
  global bstack1111ll11l_opy_
  global bstack1ll1ll11111_opy_
  global bstack1111lll1ll_opy_
  try:
    if not bstack11llll1l11_opy_:
      with bstack1111lll1ll_opy_:
        bstack111l11l1ll_opy_ = os.path.join(os.path.expanduser(bstack1l1llll_opy_ (u"ࠨࢀࠪቯ")), bstack1l1llll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩተ"), bstack1l1llll_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬቱ"))
        if os.path.exists(bstack111l11l1ll_opy_):
          with open(bstack111l11l1ll_opy_, bstack1l1llll_opy_ (u"ࠫࡷ࠭ቲ")) as f:
            content = f.read().strip()
            if content:
              bstack11ll11111l_opy_ = json.loads(bstack1l1llll_opy_ (u"ࠧࢁࠢታ") + content + bstack1l1llll_opy_ (u"࠭ࠢࡹࠤ࠽ࠤࠧࡿࠢࠨቴ") + bstack1l1llll_opy_ (u"ࠢࡾࠤት"))
              bstack11llll1l11_opy_ = bstack11ll11111l_opy_.get(str(threading.get_ident()))
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡳࡧࡤࡨ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡌࡈࡸࠦࡦࡪ࡮ࡨ࠾ࠥ࠭ቶ") + str(e))
  if not is_robot_playwright_installed():
    if bstack1111ll11l_opy_:
      with bstack1l1111ll1l_opy_:
        bstack111111llll_opy_ = bstack1111ll11l_opy_.copy()
      for driver in bstack111111llll_opy_:
        if bstack11llll1l11_opy_ == driver.session_id:
          if test:
            bstack1lllllllll1_opy_(driver, test)
          bstack11ll1ll11l_opy_(driver, bstack11lllll111_opy_)
    elif bstack11llll1l11_opy_:
      bstack1l1l111l11_opy_(test, bstack11lllll111_opy_)
    if bstack1ll1l11l111_opy_:
      bstack1111lll1l1_opy_(bstack1ll1l11l111_opy_)
    if bstack1111lll111_opy_:
      bstack1111llll11_opy_(bstack1111lll111_opy_)
    if bstack1l1l1l11l1_opy_:
      bstack1lll1ll11ll_opy_()
def bstack1lllll1lll1_opy_(self, test, *args, **kwargs):
  bstack11lllll111_opy_ = None
  if test:
    bstack11lllll111_opy_ = str(test.name)
  bstack11l1ll1ll1_opy_(test, bstack11lllll111_opy_)
  bstack1l1ll1ll11l_opy_(self, test, *args, **kwargs)
def bstack1l1l1l1lll1_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1111l1l1l1_opy_
  global CONFIG
  global bstack1111ll11l_opy_
  global bstack11llll1l11_opy_
  global bstack1111lll1ll_opy_
  bstack111ll1ll11_opy_ = None
  try:
    if bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨቷ"), None) or bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬቸ"), None):
      try:
        if not bstack11llll1l11_opy_:
          bstack111l11l1ll_opy_ = os.path.join(os.path.expanduser(bstack1l1llll_opy_ (u"ࠫࢃ࠭ቹ")), bstack1l1llll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬቺ"), bstack1l1llll_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨቻ"))
          with bstack1111lll1ll_opy_:
            if os.path.exists(bstack111l11l1ll_opy_):
              with open(bstack111l11l1ll_opy_, bstack1l1llll_opy_ (u"ࠧࡳࠩቼ")) as f:
                content = f.read().strip()
                if content:
                  bstack11ll11111l_opy_ = json.loads(bstack1l1llll_opy_ (u"ࠣࡽࠥች") + content + bstack1l1llll_opy_ (u"ࠩࠥࡼࠧࡀࠠࠣࡻࠥࠫቾ") + bstack1l1llll_opy_ (u"ࠥࢁࠧቿ"))
                  bstack11llll1l11_opy_ = bstack11ll11111l_opy_.get(str(threading.get_ident()))
      except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡶࡪࡧࡤࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡏࡄࡴࠢࡩ࡭ࡱ࡫ࠠࡪࡰࠣࡸࡪࡹࡴࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࠪኀ") + str(e))
      if bstack1111ll11l_opy_:
        with bstack1l1111ll1l_opy_:
          bstack111111llll_opy_ = bstack1111ll11l_opy_.copy()
        for driver in bstack111111llll_opy_:
          if bstack11llll1l11_opy_ == driver.session_id:
            bstack111ll1ll11_opy_ = driver
    bstack1ll111l111_opy_ = a11y.is_enabled_testcase(test.tags)
    if bstack111ll1ll11_opy_:
      threading.current_thread().isA11yTest = a11y.start_test_capture(bstack111ll1ll11_opy_, bstack1ll111l111_opy_)
      threading.current_thread().isAppA11yTest = a11y.start_test_capture(bstack111ll1ll11_opy_, bstack1ll111l111_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1ll111l111_opy_
      threading.current_thread().isAppA11yTest = bstack1ll111l111_opy_
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"ࠧࡸ࡯ࡣࡱࡷࠤࡹ࡫ࡳࡵ࠯ࡶࡸࡦࡺࡵࡴࠢࡤ࠵࠶ࡿࠠࡴࡧࡷࡹࡵࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࡼࡿ࠽ࠤࢀࢃࠢኁ").format(type(e).__name__, e), exc_info=True)
  bstack1111l1l1l1_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1l1lllll1l_opy_
  try:
    bstack1l1lllll1l_opy_ = self._test
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"ࠨࡲࡰࡤࡲࡸ࡙ࠥࡅࡔࡕࡌࡓࡓࡥࡄࡆࡖࡄࡍࡑ࡙ࠠࡠࡶࡨࡷࡹࠦࡡࡵࡶࡵࠤࡲ࡯ࡳࡴ࡫ࡱ࡫࠿ࠦࡻࡾ࠼ࠣࡿࢂࠨኂ").format(type(e).__name__, e), exc_info=True)
    bstack1l1lllll1l_opy_ = self.test
def bstack111ll1llll_opy_():
  global bstack111lll11ll_opy_
  try:
    if os.path.exists(bstack111lll11ll_opy_):
      os.remove(bstack111lll11ll_opy_)
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪኃ") + str(e))
def bstack1llll1l1l1_opy_():
  global bstack111lll11ll_opy_
  bstack1lll111111l_opy_ = {}
  lock_file = bstack111lll11ll_opy_ + bstack1l1llll_opy_ (u"ࠨ࠰࡯ࡳࡨࡱࠧኄ")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l1llll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡬ࡰࡥ࡮ࠤࡳࡵࡴࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨ࠰ࠥࡻࡳࡪࡰࡪࠤࡧࡧࡳࡪࡥࠣࡪ࡮ࡲࡥࠡࡱࡳࡩࡷࡧࡴࡪࡱࡱࡷࠬኅ"))
    try:
      if not os.path.isfile(bstack111lll11ll_opy_):
        with open(bstack111lll11ll_opy_, bstack1l1llll_opy_ (u"ࠪࡻࠬኆ")) as f:
          json.dump({}, f)
      if os.path.exists(bstack111lll11ll_opy_):
        with open(bstack111lll11ll_opy_, bstack1l1llll_opy_ (u"ࠫࡷ࠭ኇ")) as f:
          content = f.read().strip()
          if content:
            bstack1lll111111l_opy_ = json.loads(content)
    except Exception as e:
      logger.debug(bstack1l1llll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡳࡧࡤࡨ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧኈ") + str(e))
    return bstack1lll111111l_opy_
  try:
    os.makedirs(os.path.dirname(bstack111lll11ll_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      if not os.path.isfile(bstack111lll11ll_opy_):
        with open(bstack111lll11ll_opy_, bstack1l1llll_opy_ (u"࠭ࡷࠨ኉")) as f:
          json.dump({}, f)
      if os.path.exists(bstack111lll11ll_opy_):
        with open(bstack111lll11ll_opy_, bstack1l1llll_opy_ (u"ࠧࡳࠩኊ")) as f:
          content = f.read().strip()
          if content:
            bstack1lll111111l_opy_ = json.loads(content)
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡶࡪࡧࡤࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪኋ") + str(e))
  finally:
    return bstack1lll111111l_opy_
def bstack1111l1111_opy_(platform_index, item_index):
  global bstack111lll11ll_opy_
  lock_file = bstack111lll11ll_opy_ + bstack1l1llll_opy_ (u"ࠩ࠱ࡰࡴࡩ࡫ࠨኌ")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l1llll_opy_ (u"ࠪࡪ࡮ࡲࡥ࡭ࡱࡦ࡯ࠥࡴ࡯ࡵࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩ࠱ࠦࡵࡴ࡫ࡱ࡫ࠥࡨࡡࡴ࡫ࡦࠤ࡫࡯࡬ࡦࠢࡲࡴࡪࡸࡡࡵ࡫ࡲࡲࡸ࠭ኍ"))
    try:
      bstack1lll111111l_opy_ = {}
      if os.path.exists(bstack111lll11ll_opy_):
        with open(bstack111lll11ll_opy_, bstack1l1llll_opy_ (u"ࠫࡷ࠭኎")) as f:
          content = f.read().strip()
          if content:
            bstack1lll111111l_opy_ = json.loads(content)
      bstack1lll111111l_opy_[item_index] = platform_index
      with open(bstack111lll11ll_opy_, bstack1l1llll_opy_ (u"ࠧࡽࠢ኏")) as outfile:
        json.dump(bstack1lll111111l_opy_, outfile)
    except Exception as e:
      logger.debug(bstack1l1llll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡹࡵ࡭ࡹ࡯࡮ࡨࠢࡷࡳࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫነ") + str(e))
    return
  try:
    os.makedirs(os.path.dirname(bstack111lll11ll_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      bstack1lll111111l_opy_ = {}
      if os.path.exists(bstack111lll11ll_opy_):
        with open(bstack111lll11ll_opy_, bstack1l1llll_opy_ (u"ࠧࡳࠩኑ")) as f:
          content = f.read().strip()
          if content:
            bstack1lll111111l_opy_ = json.loads(content)
      bstack1lll111111l_opy_[item_index] = platform_index
      with open(bstack111lll11ll_opy_, bstack1l1llll_opy_ (u"ࠣࡹࠥኒ")) as outfile:
        json.dump(bstack1lll111111l_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡼࡸࡩࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧና") + str(e))
def bstack1lll1l1lll_opy_(bstack1l1111111l_opy_):
  global CONFIG
  bstack11llll1l1l_opy_ = bstack1l1llll_opy_ (u"ࠪࠫኔ")
  if not bstack1l1llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧን") in CONFIG:
    logger.info(bstack1l1llll_opy_ (u"ࠬࡔ࡯ࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠤࡵࡧࡳࡴࡧࡧࠤࡺࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡨࡧࡱࡩࡷࡧࡴࡦࠢࡵࡩࡵࡵࡲࡵࠢࡩࡳࡷࠦࡒࡰࡤࡲࡸࠥࡸࡵ࡯ࠩኖ"))
  try:
    platform = CONFIG[bstack1l1llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩኗ")][bstack1l1111111l_opy_]
    if bstack1l1llll_opy_ (u"ࠧࡰࡵࠪኘ") in platform:
      bstack11llll1l1l_opy_ += str(platform[bstack1l1llll_opy_ (u"ࠨࡱࡶࠫኙ")]) + bstack1l1llll_opy_ (u"ࠩ࠯ࠤࠬኚ")
    if bstack1l1llll_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ኛ") in platform:
      bstack11llll1l1l_opy_ += str(platform[bstack1l1llll_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧኜ")]) + bstack1l1llll_opy_ (u"ࠬ࠲ࠠࠨኝ")
    if bstack1l1llll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪኞ") in platform:
      bstack11llll1l1l_opy_ += str(platform[bstack1l1llll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫኟ")]) + bstack1l1llll_opy_ (u"ࠨ࠮ࠣࠫአ")
    if bstack1l1llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫኡ") in platform:
      bstack11llll1l1l_opy_ += str(platform[bstack1l1llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬኢ")]) + bstack1l1llll_opy_ (u"ࠫ࠱ࠦࠧኣ")
    if bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪኤ") in platform:
      bstack11llll1l1l_opy_ += str(platform[bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫእ")]) + bstack1l1llll_opy_ (u"ࠧ࠭ࠢࠪኦ")
    if bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩኧ") in platform:
      bstack11llll1l1l_opy_ += str(platform[bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪከ")]) + bstack1l1llll_opy_ (u"ࠪ࠰ࠥ࠭ኩ")
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"ࠫࡘࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡴࡧࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡷࡹࡸࡩ࡯ࡩࠣࡪࡴࡸࠠࡳࡧࡳࡳࡷࡺࠠࡨࡧࡱࡩࡷࡧࡴࡪࡱࡱࠫኪ") + str(e))
  finally:
    if bstack11llll1l1l_opy_[len(bstack11llll1l1l_opy_) - 2:] == bstack1l1llll_opy_ (u"ࠬ࠲ࠠࠨካ"):
      bstack11llll1l1l_opy_ = bstack11llll1l1l_opy_[:-2]
    return bstack11llll1l1l_opy_
def bstack1lll1l1llll_opy_(path, bstack11llll1l1l_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack11lll1ll1l_opy_ = ET.parse(path)
    bstack1ll1ll11lll_opy_ = bstack11lll1ll1l_opy_.getroot()
    bstack1llll111lll_opy_ = None
    for suite in bstack1ll1ll11lll_opy_.iter(bstack1l1llll_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬኬ")):
      if bstack1l1llll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧክ") in suite.attrib:
        suite.attrib[bstack1l1llll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ኮ")] += bstack1l1llll_opy_ (u"ࠩࠣࠫኯ") + bstack11llll1l1l_opy_
        bstack1llll111lll_opy_ = suite
    bstack1l11l1lll1_opy_ = None
    for robot in bstack1ll1ll11lll_opy_.iter(bstack1l1llll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩኰ")):
      bstack1l11l1lll1_opy_ = robot
    bstack111l111lll_opy_ = len(bstack1l11l1lll1_opy_.findall(bstack1l1llll_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪ኱")))
    if bstack111l111lll_opy_ == 1:
      bstack1l11l1lll1_opy_.remove(bstack1l11l1lll1_opy_.findall(bstack1l1llll_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫኲ"))[0])
      bstack1l11111l1l_opy_ = ET.Element(bstack1l1llll_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬኳ"), attrib={bstack1l1llll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬኴ"): bstack1l1llll_opy_ (u"ࠨࡕࡸ࡭ࡹ࡫ࡳࠨኵ"), bstack1l1llll_opy_ (u"ࠩ࡬ࡨࠬ኶"): bstack1l1llll_opy_ (u"ࠪࡷ࠵࠭኷")})
      bstack1l11l1lll1_opy_.insert(1, bstack1l11111l1l_opy_)
      bstack1l1lllllll1_opy_ = None
      for suite in bstack1l11l1lll1_opy_.iter(bstack1l1llll_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪኸ")):
        bstack1l1lllllll1_opy_ = suite
      bstack1l1lllllll1_opy_.append(bstack1llll111lll_opy_)
      bstack1l1l11lll1l_opy_ = None
      for status in bstack1llll111lll_opy_.iter(bstack1l1llll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬኹ")):
        bstack1l1l11lll1l_opy_ = status
      bstack1l1lllllll1_opy_.append(bstack1l1l11lll1l_opy_)
    bstack11lll1ll1l_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡶࡸ࡯࡮ࡨࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡱ࡫ࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠫኺ") + str(e))
def bstack111l1l1lll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1ll111llll_opy_
  global CONFIG
  if bstack1l1llll_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡰࡢࡶ࡫ࠦኻ") in options:
    del options[bstack1l1llll_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡱࡣࡷ࡬ࠧኼ")]
  json_data = bstack1llll1l1l1_opy_()
  for item_id in json_data.keys():
    path = os.path.join(outs_dir, str(item_id), bstack1l1llll_opy_ (u"ࠩࡲࡹࡹࡶࡵࡵ࠰ࡻࡱࡱ࠭ኽ"))
    bstack1lll1l1llll_opy_(path, bstack1lll1l1lll_opy_(json_data[item_id]))
  bstack111ll1llll_opy_()
  return bstack1ll111llll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1l1ll1lll1_opy_(self, ff_profile_dir):
  global bstack11l1l1l1l1_opy_
  if not ff_profile_dir:
    return None
  return bstack11l1l1l1l1_opy_(self, ff_profile_dir)
def bstack1l1l11l1l11_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1ll1ll111ll_opy_
  bstack1lllll1ll1_opy_ = []
  if bstack1l1llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ኾ") in CONFIG:
    bstack1lllll1ll1_opy_ = CONFIG[bstack1l1llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ኿")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1l1llll_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࠨዀ")],
      pabot_args[bstack1l1llll_opy_ (u"ࠨࡶࡦࡴࡥࡳࡸ࡫ࠢ዁")],
      argfile,
      pabot_args.get(bstack1l1llll_opy_ (u"ࠢࡩ࡫ࡹࡩࠧዂ")),
      pabot_args[bstack1l1llll_opy_ (u"ࠣࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠦዃ")],
      platform[0],
      bstack1ll1ll111ll_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1l1llll_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡪ࡮ࡲࡥࡴࠤዄ")] or [(bstack1l1llll_opy_ (u"ࠥࠦዅ"), None)]
    for platform in enumerate(bstack1lllll1ll1_opy_)
  ]
def bstack1ll1l111111_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1l1llll11ll_opy_=bstack1l1llll_opy_ (u"ࠫࠬ዆")):
  global bstack111lll1l11_opy_
  self.platform_index = platform_index
  self.bstack11111llll1_opy_ = bstack1l1llll11ll_opy_
  bstack111lll1l11_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1l1l11ll11_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1llllll111l_opy_
  global bstack1l1ll1lll1l_opy_
  bstack1ll1l11llll_opy_ = copy.deepcopy(item)
  if not bstack1l1llll_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ዇") in item.options:
    bstack1ll1l11llll_opy_.options[bstack1l1llll_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨወ")] = []
  bstack1l1lllll1l1_opy_ = bstack1ll1l11llll_opy_.options[bstack1l1llll_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩዉ")].copy()
  for v in bstack1ll1l11llll_opy_.options[bstack1l1llll_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪዊ")]:
    if bstack1l1llll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘࠨዋ") in v:
      bstack1l1lllll1l1_opy_.remove(v)
    if bstack1l1llll_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡆࡐࡎࡇࡒࡈࡕࠪዌ") in v:
      bstack1l1lllll1l1_opy_.remove(v)
    if bstack1l1llll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨው") in v:
      bstack1l1lllll1l1_opy_.remove(v)
  bstack1l1lllll1l1_opy_.insert(0, bstack1l1llll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡕࡒࡁࡕࡈࡒࡖࡒࡏࡎࡅࡇ࡛࠾ࢀࢃࠧዎ").format(bstack1ll1l11llll_opy_.platform_index))
  bstack1l1lllll1l1_opy_.insert(0, bstack1l1llll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔ࠽ࡿࢂ࠭ዏ").format(bstack1ll1l11llll_opy_.bstack11111llll1_opy_))
  bstack1ll1l11llll_opy_.options[bstack1l1llll_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩዐ")] = bstack1l1lllll1l1_opy_
  if bstack1l1ll1lll1l_opy_:
    bstack1ll1l11llll_opy_.options[bstack1l1llll_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪዑ")].insert(0, bstack1l1llll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡅࡏࡍࡆࡘࡇࡔ࠼ࡾࢁࠬዒ").format(bstack1l1ll1lll1l_opy_))
  return bstack1llllll111l_opy_(caller_id, datasources, is_last, bstack1ll1l11llll_opy_, outs_dir)
def bstack111lllll1l_opy_(command, item_index):
  try:
    if global_config.get_property(bstack1l1llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫዓ")):
      os.environ[bstack1l1llll_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬዔ")] = json.dumps(CONFIG[bstack1l1llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨዕ")][item_index % bstack1111111l1_opy_])
    global bstack1l1ll1lll1l_opy_
    os.environ[bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ዖ")] = str(item_index % bstack1111111l1_opy_)
    listener_arg = bstack1l1llll_opy_ (u"ࠧࠨ዗")
    if robot_pw_binary_flow() and cli.is_enabled(CONFIG):
      listener_arg = bstack1l1llll_opy_ (u"ࠨࠢ࠰࠱ࡱ࡯ࡳࡵࡧࡱࡩࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡹࡤ࡬࠰ࡵࡳࡧࡵࡴࡠ࡮࡬ࡷࡹ࡫࡮ࡦࡴࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠮ࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡔࡦࡺࡣࡩࡧࡵࠫዘ")
      logger.debug(bstack1l1llll_opy_ (u"ࠤࡄࡨࡩ࡯࡮ࡨࠢࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡖࡡࡵࡥ࡫ࡩࡷࠦ࡬ࡪࡵࡷࡩࡳ࡫ࡲࠡࡨࡲࡶࠥ࡯ࡴࡦ࡯ࠣࡿࢂࠨዙ").format(item_index))
    bstack1ll11llll1l_opy_ = bstack1l1llll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡶࡨࡰࠦࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠠ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࠣࠦዚ") + \
              str(item_index % bstack1111111l1_opy_) + \
              bstack1l1llll_opy_ (u"ࠦࠥ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠤࠧዛ") + \
              str(item_index) + \
              listener_arg
    if bstack1l1ll1lll1l_opy_:
        bstack1ll11llll1l_opy_ += bstack1l1llll_opy_ (u"ࠧࠦࠢዜ") + bstack1l1ll1lll1l_opy_
    command[0:1] = bstack1ll11llll1l_opy_.split()
  except Exception as e:
    logger.error(bstack1l1llll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡳ࡯ࡥ࡫ࡩࡽ࡮ࡴࡧࠡࡥࡲࡱࡲࡧ࡮ࡥࠢࡩࡳࡷࠦࡰࡢࡤࡲࡸࠥࡸࡵ࡯࠼ࠣࡿࢂ࠭ዝ").format(str(e)))
def bstack11l111l111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1ll1l11ll1_opy_
  try:
    bstack111lllll1l_opy_(command, item_index)
    return bstack1ll1l11ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
  except Exception as e:
    logger.error(bstack1l1llll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡧࡵࡴࠡࡴࡸࡲ࠿ࠦࡻࡾࠩዞ").format(str(e)))
    raise e
def bstack1ll111111ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1ll1l11ll1_opy_
  try:
    bstack111lllll1l_opy_(command, item_index)
    return bstack1ll1l11ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
  except Exception as e:
    logger.error(bstack1l1llll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡦࡨ࡯ࡵࠢࡵࡹࡳࠦ࠲࠯࠳࠶࠾ࠥࢁࡽࠨዟ").format(str(e)))
    try:
      return bstack1ll1l11ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
    except Exception as e2:
      logger.error(bstack1l1llll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡢࡰࡶࠣ࠶࠳࠷࠳ࠡࡨࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࢀࢃࠧዠ").format(str(e2)))
      raise e
def bstack1ll11l11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1ll1l11ll1_opy_
  try:
    bstack111lllll1l_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    return bstack1ll1l11ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
  except Exception as e:
    logger.error(bstack1l1llll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡣࡱࡷࠤࡷࡻ࡮ࠡ࠴࠱࠵࠺ࡀࠠࡼࡿࠪዡ").format(str(e)))
    try:
      return bstack1ll1l11ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
    except Exception as e2:
      logger.error(bstack1l1llll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡢࡤࡲࡸࠥ࠸࠮࠲࠷ࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࡻࡾࠩዢ").format(str(e2)))
      raise e
def _1ll111l111l_opy_(bstack1l1llllll11_opy_, item_index, process_timeout, sleep_before_start, bstack1llll11111_opy_):
  bstack111lllll1l_opy_(bstack1l1llllll11_opy_, item_index)
  if process_timeout is None:
    process_timeout = 3600
  if sleep_before_start and sleep_before_start > 0:
    time.sleep(min(sleep_before_start, 5))
  return process_timeout
def bstack1ll11l1l11l_opy_(command, bstack1l111111ll_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack1ll1l11ll1_opy_
  global bstack1l11l1111l_opy_
  global bstack1l1ll1lll1l_opy_
  try:
    for env_name, bstack1lll111llll_opy_ in bstack1l11l1111l_opy_.items():
      os.environ[env_name] = bstack1lll111llll_opy_
    bstack1l1ll1lll1l_opy_ = bstack1l1llll_opy_ (u"ࠧࠨዣ")
    bstack111lllll1l_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    if sleep_before_start and sleep_before_start > 0:
      time.sleep(min(sleep_before_start, 5))
    return bstack1ll1l11ll1_opy_(command, bstack1l111111ll_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack1l1llll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠࡳࡷࡱࠤ࠺࠴࠰࠻ࠢࡾࢁࠬዤ").format(str(e)))
    try:
      return bstack1ll1l11ll1_opy_(command, bstack1l111111ll_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack1l1llll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡧࡵࡴࠡࡨࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࢀࢃࠧዥ").format(str(e2)))
      raise e
def bstack1l1l1ll1111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack1ll1l11ll1_opy_
  try:
    process_timeout = _1ll111l111l_opy_(command, item_index, process_timeout, sleep_before_start, bstack1l1llll_opy_ (u"ࠨ࠶࠱࠶ࠬዦ"))
    return bstack1ll1l11ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack1l1llll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡢࡰࡶࠣࡶࡺࡴࠠ࠵࠰࠵࠾ࠥࢁࡽࠨዧ").format(str(e)))
    try:
      return bstack1ll1l11ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack1l1llll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡣࡱࡷࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࡼࡿࠪየ").format(str(e2)))
      raise e
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def mod_behave_step_run(self, runner, quiet=False, capture=True):
  global bstack1l1l1ll1lll_opy_
  bstack11l1ll11l1_opy_ = bstack1l1l1ll1lll_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack1l1llll_opy_ (u"ࠫࡪࡾࡣࡦࡲࡷ࡭ࡴࡴ࡟ࡢࡴࡵࠫዩ")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1l1llll_opy_ (u"ࠬ࡫ࡸࡤࡡࡷࡶࡦࡩࡥࡣࡣࡦ࡯ࡤࡧࡲࡳࠩዪ")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack11l1ll11l1_opy_
def handle_hook_generic(runner, hook_name, context, element, bstack111ll1l1l1_opy_, *args):
  global bstack1l1ll1ll1l1_opy_
  try:
    if runner.hooks.get(hook_name):
      bstack111111l1l_opy_.start_hook(hook_name, element)
    if bstack1l1ll1ll1l1_opy_ is None or bstack1l1ll1ll1l1_opy_:
      bstack111ll1l1l1_opy_(runner, hook_name, context, *args)
    else:
      bstack1111111l11_opy_ = (context,) + args
      bstack111ll1l1l1_opy_(runner, hook_name, *bstack1111111l11_opy_)
    if runner.hooks.get(hook_name):
      bstack111111l1l_opy_.end_hook(hook_name, element)
      if hook_name not in [bstack1l1llll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠪያ"), bstack1l1llll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪዬ")] and args and hasattr(args[0], bstack1l1llll_opy_ (u"ࠨࡧࡵࡶࡴࡸ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠨይ")):
        args[0].error_message = bstack1l1llll_opy_ (u"ࠩࠪዮ")
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡨࡢࡰࡧࡰࡪࠦࡨࡰࡱ࡮ࡷࠥ࡯࡮ࠡࡤࡨ࡬ࡦࡼࡥ࠻ࠢࡾࢁࠬዯ").format(str(e)))
@measure(event_name=EVENTS.bstack1ll11lll1l_opy_, stage=STAGE.SINGLE, hook_type=bstack1l1llll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡅࡱࡲࠢደ"), bstack11lllll111_opy_=SESSION_NAME)
def handle_before_all(runner, name, context, bstack111ll1l1l1_opy_, *args):
    if runner.hooks.get(bstack1l1llll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤዱ")).__name__ != bstack1l1llll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࡢࡨࡪ࡬ࡡࡶ࡮ࡷࡣ࡭ࡵ࡯࡬ࠤዲ"):
      handle_hook_generic(runner, name, context, runner, bstack111ll1l1l1_opy_, *args)
    if not cli.is_running():
      try:
        threading.current_thread().bstackSessionDriver if bstack1l1ll1l1l1l_opy_(bstack1l1llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ዳ")) else context.browser
        runner.driver_initialised = bstack1l1llll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧዴ")
      except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡧࡶ࡮ࡼࡥࡳࠢ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡷࡪࠦࡡࡵࡶࡵ࡭ࡧࡻࡴࡦ࠼ࠣࡿࢂ࠭ድ").format(str(e)))
def handle_before_feature(runner, name, context, bstack111ll1l1l1_opy_, *args):
    handle_hook_generic(runner, name, context, context.feature, bstack111ll1l1l1_opy_, *args)
    if not cli.is_running():
      try:
        if not bstack11l11l1l1l_opy_:
          bstack111ll1ll11_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1ll1l1l1l_opy_(bstack1l1llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩዶ")) else context.browser
          if is_driver_active(bstack111ll1ll11_opy_):
            if runner.driver_initialised is None: runner.driver_initialised = bstack1l1llll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠧዷ")
            bstack1l1ll11l1ll_opy_ = str(runner.feature.name)
            playwright_set_session_name(context, bstack1l1ll11l1ll_opy_)
            bstack111ll1ll11_opy_.execute_script(bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪዸ") + json.dumps(bstack1l1ll11l1ll_opy_) + bstack1l1llll_opy_ (u"࠭ࡽࡾࠩዹ"))
      except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧዺ").format(str(e)))
def handle_before_tag(runner, name, context, bstack111ll1l1l1_opy_, *args):
    target = context.scenario if hasattr(context, bstack1l1llll_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪዻ")) else context.feature
    handle_hook_generic(runner, name, context, target, bstack111ll1l1l1_opy_, *args)
@measure(event_name=EVENTS.bstack11ll1lll1l_opy_, stage=STAGE.SINGLE, bstack11lllll111_opy_=SESSION_NAME)
def handle_before_scenario(runner, name, context, bstack111ll1l1l1_opy_, *args):
    bstack111111l1l_opy_.start_test(context)
    handle_hook_generic(runner, name, context, context.scenario, bstack111ll1l1l1_opy_, *args)
    if not cli.is_running():
      threading.current_thread().a11y_stop = False
      bstack111ll1l111_opy_.bstack1ll11l1l1l1_opy_(context, *args)
      try:
        bstack111ll1ll11_opy_ = bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨዼ"), context.browser)
        if is_driver_active(bstack111ll1ll11_opy_):
          TestHubHandler.send_cbt_info(bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩዽ"), {}))
          if runner.driver_initialised is None: runner.driver_initialised = bstack1l1llll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨዾ")
          if (not bstack11l11l1l1l_opy_):
            scenario_name = args[0].name
            feature_name = bstack1l1ll11l1ll_opy_ = str(runner.feature.name)
            bstack1l1ll11l1ll_opy_ = feature_name + bstack1l1llll_opy_ (u"ࠬࠦ࠭ࠡࠩዿ") + scenario_name
            if runner.driver_initialised == bstack1l1llll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣጀ"):
              playwright_set_session_name(context, bstack1l1ll11l1ll_opy_)
              bstack111ll1ll11_opy_.execute_script(bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬጁ") + json.dumps(bstack1l1ll11l1ll_opy_) + bstack1l1llll_opy_ (u"ࠨࡿࢀࠫጂ"))
      except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡ࡫ࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡀࠠࡼࡿࠪጃ").format(str(e)))
@measure(event_name=EVENTS.bstack1ll11lll1l_opy_, stage=STAGE.SINGLE, hook_type=bstack1l1llll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡖࡸࡪࡶࠢጄ"), bstack11lllll111_opy_=SESSION_NAME)
def handle_before_step(runner, name, context, bstack111ll1l1l1_opy_, *args):
    handle_hook_generic(runner, name, context, args[0], bstack111ll1l1l1_opy_, *args)
    if cli.is_running():
      bstack111111l1l_opy_.start_step(args[0])
    else:
      try:
        bstack111ll1ll11_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1ll1l1l1l_opy_(bstack1l1llll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪጅ")) else context.browser
        if is_driver_active(bstack111ll1ll11_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack1l1llll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥጆ")
          bstack111111l1l_opy_.start_step(args[0])
          if runner.driver_initialised == bstack1l1llll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦጇ") and not bstack11l11l1l1l_opy_:
            feature_name = bstack1l1ll11l1ll_opy_ = str(runner.feature.name)
            bstack1l1ll11l1ll_opy_ = feature_name + bstack1l1llll_opy_ (u"ࠧࠡ࠯ࠣࠫገ") + context.scenario.name
            playwright_set_session_name(context, bstack1l1ll11l1ll_opy_)
            bstack111ll1ll11_opy_.execute_script(bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭ጉ") + json.dumps(bstack1l1ll11l1ll_opy_) + bstack1l1llll_opy_ (u"ࠩࢀࢁࠬጊ"))
      except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡴࡦࡲ࠽ࠤࢀࢃࠧጋ").format(str(e)))
@measure(event_name=EVENTS.bstack1ll11lll1l_opy_, stage=STAGE.SINGLE, hook_type=bstack1l1llll_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࡖࡸࡪࡶࠢጌ"), bstack11lllll111_opy_=SESSION_NAME)
def handle_after_step(runner, name, context, bstack111ll1l1l1_opy_, *args):
  if cli.is_running():
    page = getattr(context, bstack1l1llll_opy_ (u"ࠬࡶࡡࡨࡧࠪግ"), None)
    if page and hasattr(page, bstack1l1llll_opy_ (u"࠭ࡥࡷࡣ࡯ࡹࡦࡺࡥࠨጎ")):
      threading.current_thread().bstackSessionPage = page
  bstack111111l1l_opy_.end_step(args[0])
  if not cli.is_running():
    try:
      step_status = args[0].status.name
      bstack111ll1ll11_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ጏ") in threading.current_thread().__dict__.keys() else context.browser
      try:
        _1ll11l1l111_opy_ = is_driver_active(bstack111ll1ll11_opy_)
      except Exception:
        _1ll11l1l111_opy_ = False
      if _1ll11l1l111_opy_:
        if runner.driver_initialised is None:
          runner.driver_initialised  = bstack1l1llll_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨጐ")
          if not bstack11l11l1l1l_opy_:
            feature_name = bstack1l1ll11l1ll_opy_ = str(runner.feature.name)
            bstack1l1ll11l1ll_opy_ = feature_name + bstack1l1llll_opy_ (u"ࠩࠣ࠱ࠥ࠭጑") + context.scenario.name
            playwright_set_session_name(context, bstack1l1ll11l1ll_opy_)
            bstack111ll1ll11_opy_.execute_script(bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨጒ") + json.dumps(bstack1l1ll11l1ll_opy_) + bstack1l1llll_opy_ (u"ࠫࢂࢃࠧጓ"))
      if str(step_status).lower() in [bstack1l1llll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬጔ"), bstack1l1llll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬጕ")]:
        bstack1ll1lll111l_opy_ = bstack1l1llll_opy_ (u"ࠧࠨ጖")
        bstack1ll1llllll_opy_ = bstack1l1llll_opy_ (u"ࠨࠩ጗")
        bstack1lll1llll11_opy_ = bstack1l1llll_opy_ (u"ࠩࠪጘ")
        try:
          import traceback
          bstack1ll1lll111l_opy_ = runner.exception.__class__.__name__
          bstack1l11ll1l_opy_ = traceback.format_tb(runner.exc_traceback)
          bstack1ll1llllll_opy_ = bstack1l1llll_opy_ (u"ࠪࠤࠬጙ").join(bstack1l11ll1l_opy_)
          bstack1lll1llll11_opy_ = bstack1l11ll1l_opy_[-1]
        except Exception as e:
          logger.debug(bstack1ll11l1ll11_opy_.format(str(e)))
        bstack1ll1lll111l_opy_ += bstack1lll1llll11_opy_
        playwright_annotate(context, json.dumps(str(args[0].name) + bstack1l1llll_opy_ (u"ࠦࠥ࠳ࠠࡇࡣ࡬ࡰࡪࡪࠡ࡝ࡰࠥጚ") + str(bstack1ll1llllll_opy_)),
                            bstack1l1llll_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦጛ"))
        if runner.driver_initialised == bstack1l1llll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦጜ"):
          bstack1lll1111l1l_opy_(getattr(context, bstack1l1llll_opy_ (u"ࠧࡱࡣࡪࡩࠬጝ"), None), bstack1l1llll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣጞ"), bstack1ll1lll111l_opy_)
          bstack111ll1ll11_opy_.execute_script(bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧጟ") + json.dumps(str(args[0].name) + bstack1l1llll_opy_ (u"ࠥࠤ࠲ࠦࡆࡢ࡫࡯ࡩࡩࠧ࡜࡯ࠤጠ") + str(bstack1ll1llllll_opy_)) + bstack1l1llll_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣࡿࢀࠫጡ"))
        if runner.driver_initialised == bstack1l1llll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥጢ"):
          bstack1l1lll1ll1l_opy_(bstack111ll1ll11_opy_, bstack1l1llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ጣ"), bstack1l1llll_opy_ (u"ࠢࡔࡥࡨࡲࡦࡸࡩࡰࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦጤ") + str(bstack1ll1lll111l_opy_))
      else:
        playwright_annotate(context, bstack1l1llll_opy_ (u"ࠣࡒࡤࡷࡸ࡫ࡤࠢࠤጥ"), bstack1l1llll_opy_ (u"ࠤ࡬ࡲ࡫ࡵࠢጦ"))
        if runner.driver_initialised == bstack1l1llll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣጧ"):
          bstack1lll1111l1l_opy_(getattr(context, bstack1l1llll_opy_ (u"ࠫࡵࡧࡧࡦࠩጨ"), None), bstack1l1llll_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧጩ"))
        bstack111ll1ll11_opy_.execute_script(bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫጪ") + json.dumps(str(args[0].name) + bstack1l1llll_opy_ (u"ࠢࠡ࠯ࠣࡔࡦࡹࡳࡦࡦࠤࠦጫ")) + bstack1l1llll_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦࢂࢃࠧጬ"))
        if runner.driver_initialised == bstack1l1llll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢጭ"):
          bstack1l1lll1ll1l_opy_(bstack111ll1ll11_opy_, bstack1l1llll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥጮ"))
    except Exception as e:
      logger.debug(bstack1l1llll_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࠡࡵࡷࡩࡵࡀࠠࡼࡿࠪጯ").format(str(e)))
  handle_hook_generic(runner, name, context, args[0], bstack111ll1l1l1_opy_, *args)
@measure(event_name=EVENTS.bstack1l1l1l1ll1_opy_, stage=STAGE.SINGLE, bstack11lllll111_opy_=SESSION_NAME)
def handle_after_scenario(runner, name, context, bstack111ll1l1l1_opy_, *args):
  if cli.is_running():
    handle_hook_generic(runner, name, context, context.scenario, bstack111ll1l1l1_opy_, *args)
    bstack111111l1l_opy_.end_test(args[0])
  else:
    bstack111111l1l_opy_.end_test(args[0], runner=runner)
    try:
      scenario_status = args[0].status.name
      bstack111ll1ll11_opy_ = bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫጰ"), context.browser)
      bstack111ll1l111_opy_.bstack1l1ll1l11ll_opy_(bstack111ll1ll11_opy_)
      if str(scenario_status).lower() in [bstack1l1llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ጱ"), bstack1l1llll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ጲ")]:
        bstack1ll1lll111l_opy_ = bstack1l1llll_opy_ (u"ࠨࠩጳ")
        bstack1ll1llllll_opy_ = bstack1l1llll_opy_ (u"ࠩࠪጴ")
        bstack1lll1llll11_opy_ = bstack1l1llll_opy_ (u"ࠪࠫጵ")
        try:
          import traceback
          bstack1ll1lll111l_opy_ = runner.exception.__class__.__name__
          bstack1l11ll1l_opy_ = traceback.format_tb(runner.exc_traceback)
          bstack1ll1llllll_opy_ = bstack1l1llll_opy_ (u"ࠫࠥ࠭ጶ").join(bstack1l11ll1l_opy_)
          bstack1lll1llll11_opy_ = bstack1l11ll1l_opy_[-1]
        except Exception as e:
          logger.debug(bstack1ll11l1ll11_opy_.format(str(e)))
        bstack1ll1lll111l_opy_ += bstack1lll1llll11_opy_
        playwright_annotate(context, json.dumps(str(args[0].name) + bstack1l1llll_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦጷ") + str(bstack1ll1llllll_opy_)),
                            bstack1l1llll_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧጸ"))
        if runner.driver_initialised == bstack1l1llll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤጹ") or runner.driver_initialised == bstack1l1llll_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨጺ"):
          bstack1lll1111l1l_opy_(getattr(context, bstack1l1llll_opy_ (u"ࠩࡳࡥ࡬࡫ࠧጻ"), None), bstack1l1llll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥጼ"), bstack1ll1lll111l_opy_)
          bstack111ll1ll11_opy_.execute_script(bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩጽ") + json.dumps(str(args[0].name) + bstack1l1llll_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦጾ") + str(bstack1ll1llllll_opy_)) + bstack1l1llll_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥࢁࢂ࠭ጿ"))
        if runner.driver_initialised == bstack1l1llll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤፀ") or runner.driver_initialised == bstack1l1llll_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨፁ"):
          bstack1l1lll1ll1l_opy_(bstack111ll1ll11_opy_, bstack1l1llll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩፂ"), bstack1l1llll_opy_ (u"ࠥࡗࡨ࡫࡮ࡢࡴ࡬ࡳࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢፃ") + str(bstack1ll1lll111l_opy_))
      else:
        playwright_annotate(context, bstack1l1llll_opy_ (u"ࠦࡕࡧࡳࡴࡧࡧࠥࠧፄ"), bstack1l1llll_opy_ (u"ࠧ࡯࡮ࡧࡱࠥፅ"))
        if runner.driver_initialised == bstack1l1llll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣፆ") or runner.driver_initialised == bstack1l1llll_opy_ (u"ࠧࡪࡰࡶࡸࡪࡶࠧፇ"):
          bstack1lll1111l1l_opy_(getattr(context, bstack1l1llll_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭ፈ"), None), bstack1l1llll_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤፉ"))
        bstack111ll1ll11_opy_.execute_script(bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨፊ") + json.dumps(str(args[0].name) + bstack1l1llll_opy_ (u"ࠦࠥ࠳ࠠࡑࡣࡶࡷࡪࡪࠡࠣፋ")) + bstack1l1llll_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫፌ"))
        if runner.driver_initialised == bstack1l1llll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣፍ") or runner.driver_initialised == bstack1l1llll_opy_ (u"ࠧࡪࡰࡶࡸࡪࡶࠧፎ"):
          bstack1l1lll1ll1l_opy_(bstack111ll1ll11_opy_, bstack1l1llll_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣፏ"))
    except Exception as e:
      logger.debug(bstack1l1llll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫፐ").format(str(e)))
    handle_hook_generic(runner, name, context, context.scenario, bstack111ll1l1l1_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def handle_after_tag(runner, name, context, bstack111ll1l1l1_opy_, *args):
    target = context.scenario if hasattr(context, bstack1l1llll_opy_ (u"ࠪࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬፑ")) else context.feature
    handle_hook_generic(runner, name, context, target, bstack111ll1l1l1_opy_, *args)
    threading.current_thread().current_test_uuid = None
def handle_after_feature(runner, name, context, bstack111ll1l1l1_opy_, *args):
    if cli.is_running():
      handle_hook_generic(runner, name, context, context.feature, bstack111ll1l1l1_opy_, *args)
      return
    try:
      bstack111ll1ll11_opy_ = bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪፒ"), context.browser)
      bstack1l11ll1l11_opy_ = bstack1l1llll_opy_ (u"ࠬ࠭ፓ")
      if context.failed is True:
        bstack111l1l11ll_opy_ = []
        bstack1l1l11llll_opy_ = []
        bstack1lllll1l1l_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack111l1l11ll_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1l11ll1l_opy_ = traceback.format_tb(exc_tb)
            bstack1lll1ll1111_opy_ = bstack1l1llll_opy_ (u"࠭ࠠࠨፔ").join(bstack1l11ll1l_opy_)
            bstack1l1l11llll_opy_.append(bstack1lll1ll1111_opy_)
            bstack1lllll1l1l_opy_.append(bstack1l11ll1l_opy_[-1])
        except Exception as e:
          logger.debug(bstack1ll11l1ll11_opy_.format(str(e)))
        bstack1ll1lll111l_opy_ = bstack1l1llll_opy_ (u"ࠧࠨፕ")
        for i in range(len(bstack111l1l11ll_opy_)):
          bstack1ll1lll111l_opy_ += bstack111l1l11ll_opy_[i] + bstack1lllll1l1l_opy_[i] + bstack1l1llll_opy_ (u"ࠨ࡞ࡱࠫፖ")
        bstack1l11ll1l11_opy_ = bstack1l1llll_opy_ (u"ࠩࠣࠫፗ").join(bstack1l1l11llll_opy_)
        if runner.driver_initialised in [bstack1l1llll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦፘ"), bstack1l1llll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣፙ")]:
          playwright_annotate(context, bstack1l11ll1l11_opy_, bstack1l1llll_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦፚ"))
          bstack1lll1111l1l_opy_(getattr(context, bstack1l1llll_opy_ (u"࠭ࡰࡢࡩࡨࠫ፛"), None), bstack1l1llll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ፜"), bstack1ll1lll111l_opy_)
          bstack111ll1ll11_opy_.execute_script(bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭፝") + json.dumps(bstack1l11ll1l11_opy_) + bstack1l1llll_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࡽࡾࠩ፞"))
          bstack1l1lll1ll1l_opy_(bstack111ll1ll11_opy_, bstack1l1llll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ፟"), bstack1l1llll_opy_ (u"ࠦࡘࡵ࡭ࡦࠢࡶࡧࡪࡴࡡࡳ࡫ࡲࡷࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦ࡜࡯ࠤ፠") + str(bstack1ll1lll111l_opy_))
          bstack1111lllll1_opy_ = bstack1ll11l11ll1_opy_(bstack1l11ll1l11_opy_, runner.feature.name, logger)
          if (bstack1111lllll1_opy_ != None):
            bstack1ll111l11ll_opy_.append(bstack1111lllll1_opy_)
      else:
        if runner.driver_initialised in [bstack1l1llll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨ፡"), bstack1l1llll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥ።")]:
          playwright_annotate(context, bstack1l1llll_opy_ (u"ࠢࡇࡧࡤࡸࡺࡸࡥ࠻ࠢࠥ፣") + str(runner.feature.name) + bstack1l1llll_opy_ (u"ࠣࠢࡳࡥࡸࡹࡥࡥࠣࠥ፤"), bstack1l1llll_opy_ (u"ࠤ࡬ࡲ࡫ࡵࠢ፥"))
          bstack1lll1111l1l_opy_(getattr(context, bstack1l1llll_opy_ (u"ࠪࡴࡦ࡭ࡥࠨ፦"), None), bstack1l1llll_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ፧"))
          bstack111ll1ll11_opy_.execute_script(bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ፨") + json.dumps(bstack1l1llll_opy_ (u"ࠨࡆࡦࡣࡷࡹࡷ࡫࠺ࠡࠤ፩") + str(runner.feature.name) + bstack1l1llll_opy_ (u"ࠢࠡࡲࡤࡷࡸ࡫ࡤࠢࠤ፪")) + bstack1l1llll_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦࢂࢃࠧ፫"))
          bstack1l1lll1ll1l_opy_(bstack111ll1ll11_opy_, bstack1l1llll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ፬"))
          bstack1111lllll1_opy_ = bstack1ll11l11ll1_opy_(bstack1l11ll1l11_opy_, runner.feature.name, logger)
          if (bstack1111lllll1_opy_ != None):
            bstack1ll111l11ll_opy_.append(bstack1111lllll1_opy_)
    except Exception as e:
      logger.debug(bstack1l1llll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡯࡮ࠡࡣࡩࡸࡪࡸࠠࡧࡧࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬ፭").format(str(e)))
    handle_hook_generic(runner, name, context, context.feature, bstack111ll1l1l1_opy_, *args)
@measure(event_name=EVENTS.bstack1ll11lll1l_opy_, stage=STAGE.SINGLE, hook_type=bstack1l1llll_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࡄࡰࡱࠨ፮"), bstack11lllll111_opy_=SESSION_NAME)
def handle_after_all(runner, name, context, bstack111ll1l1l1_opy_, *args):
    handle_hook_generic(runner, name, context, runner, bstack111ll1l1l1_opy_, *args)
def mod_behave_load_hooks(self, filename=None):
  global bstack1l1l111l1ll_opy_
  bstack1l1l111l1ll_opy_(self, filename)
  bstack1l1llll111l_opy_ = []
  bstack11l1111l11_opy_ = [bstack1l1llll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭፯"), bstack1l1llll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡴࡢࡩࠪ፰"), bstack1l1llll_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩ፱"), bstack1l1llll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩ፲"), bstack1l1llll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡶࡤ࡫ࠬ፳"), bstack1l1llll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪ፴")]
  bstack1llll111l1_opy_ = lambda *_: None
  for hook_name in bstack11l1111l11_opy_:
    if hook_name not in self.hooks:
      self.hooks[hook_name] = bstack1llll111l1_opy_
      bstack1l1llll111l_opy_.append(hook_name)
  if bstack1l1llll111l_opy_:
    os.environ[bstack1l1llll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡘࡊࡋࡠࡆࡈࡊࡆ࡛ࡌࡕࡡࡋࡓࡔࡑࡓࠨ፵")] = bstack1l1llll_opy_ (u"ࠬ࠲ࠧ፶").join(bstack1l1llll111l_opy_)
def _execute_deferred_playwright_close(bstack111l11llll_opy_=False):
  try:
    _1l111l11_opy_ = threading.current_thread()
    _1ll1l1llll_opy_ = getattr(_1l111l11_opy_, bstack1l1llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡤࡦࡨࡨࡶࡷ࡫ࡤࡠࡲࡤ࡫ࡪࡥࡲࡦࡨࠪ፷"), None)
    _1111111111_opy_ = getattr(_1l111l11_opy_, bstack1l1llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡥࡧࡩࡩࡷࡸࡥࡥࡡࡥࡶࡴࡽࡳࡦࡴࡢࡶࡪ࡬ࠧ፸"), None)
    _1l1ll111l1_opy_ = getattr(_1l111l11_opy_, bstack1l1llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡦࡨࡪࡪࡸࡲࡦࡦࡢࡴࡼࡥࡳࡵࡱࡳࡣ࡫ࡴࠧ፹"), None)
    _wrapper = getattr(_1l111l11_opy_, bstack1l1llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ፺"), None)
    if not _1111111111_opy_ and _wrapper and hasattr(_wrapper, bstack1l1llll_opy_ (u"ࠪࡣࡧࡸ࡯ࡸࡵࡨࡶࠬ፻")):
      _1111111111_opy_ = _wrapper._browser
    if not _1ll1l1llll_opy_ and _wrapper and hasattr(_wrapper, bstack1l1llll_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪ፼")):
      _1ll1l1llll_opy_ = _wrapper._page
    if not _1l1ll111l1_opy_:
      _1l1ll1llll_opy_ = getattr(_1l111l11_opy_, bstack1l1llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡪࡥࡧࡧࡵࡶࡪࡪ࡟ࡱࡹࡢࡶࡪ࡬ࠧ፽"), None)
      if _1l1ll1llll_opy_ and hasattr(_1l1ll1llll_opy_, bstack1l1llll_opy_ (u"࠭ࡳࡵࡱࡳࠫ፾")):
        _1l1ll111l1_opy_ = _1l1ll1llll_opy_.stop
    _1ll1l1l1l11_opy_ = _1ll1l1llll_opy_ or _1111111111_opy_ or _1l1ll111l1_opy_
    if not _1ll1l1l1l11_opy_:
      return
    if _1ll1l1llll_opy_ and hasattr(_1ll1l1llll_opy_, bstack1l1llll_opy_ (u"ࠧࡤ࡮ࡲࡷࡪ࠭፿")):
      try:
        _1ll1l1llll_opy_.close(_bstack_sdk_close=True)
      except TypeError:
        try:
          _r = _1ll1l1llll_opy_.close()
          if _r is not None and hasattr(_r, bstack1l1llll_opy_ (u"ࠨࡥ࡯ࡳࡸ࡫ࠧᎀ")):
            _r.close()
        except Exception:
          pass
      except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠩࡇࡩ࡫࡫ࡲࡳࡧࡧࠤࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡲࡤ࡫ࡪ࠴ࡣ࡭ࡱࡶࡩࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡾࠩᎁ").format(str(e)))
    if _1111111111_opy_ and hasattr(_1111111111_opy_, bstack1l1llll_opy_ (u"ࠪࡧࡱࡵࡳࡦࠩᎂ")):
      try:
        _1111111111_opy_.close(_bstack_sdk_close=True)
      except TypeError:
        try:
          _r = _1111111111_opy_.close()
          if _r is not None and hasattr(_r, bstack1l1llll_opy_ (u"ࠫࡨࡲ࡯ࡴࡧࠪᎃ")):
            _r.close()
        except Exception:
          pass
      except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠬࡊࡥࡧࡧࡵࡶࡪࡪࠠࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡧࡸ࡯ࡸࡵࡨࡶ࠳ࡩ࡬ࡰࡵࡨࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽࠨᎄ").format(str(e)))
    if _1l1ll111l1_opy_ and not bstack111l11llll_opy_:
      _thread_id = _1l111l11_opy_.ident
      bstack1l1l1l1111_opy_ = False
      try:
        with _PLAYWRIGHT_ACTIVE_THREADS_LOCK:
          _PLAYWRIGHT_ACTIVE_THREADS.discard(_thread_id)
          bstack1l1l1l1111_opy_ = len(_PLAYWRIGHT_ACTIVE_THREADS) == 0
      except Exception:
        bstack1l1l1l1111_opy_ = True
      if bstack1l1l1l1111_opy_:
        try:
          _1l1ll111l1_opy_(_bstack_sdk_close=True)
        except TypeError:
          try:
            _r = _1l1ll111l1_opy_()
            if _r is not None and hasattr(_r, bstack1l1llll_opy_ (u"࠭ࡣ࡭ࡱࡶࡩࠬᎅ")):
              _r.close()
          except Exception:
            pass
        except Exception:
          pass
    for attr in (bstack1l1llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡥࡧࡩࡩࡷࡸࡥࡥࡡࡳࡥ࡬࡫࡟ࡤ࡮ࡲࡷࡪ࠭ᎆ"), bstack1l1llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡦࡨࡪࡪࡸࡲࡦࡦࡢࡴࡦ࡭ࡥࡠࡴࡨࡪࠬᎇ"),
                 bstack1l1llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡧࡩ࡫࡫ࡲࡳࡧࡧࡣࡧࡸ࡯ࡸࡵࡨࡶࡤࡩ࡬ࡰࡵࡨࠫᎈ"), bstack1l1llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡨࡪ࡬ࡥࡳࡴࡨࡨࡤࡨࡲࡰࡹࡶࡩࡷࡥࡲࡦࡨࠪᎉ"),
                 bstack1l1llll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡩ࡫ࡦࡦࡴࡵࡩࡩࡥࡰࡸࡡࡶࡸࡴࡶࠧᎊ"), bstack1l1llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡪࡥࡧࡧࡵࡶࡪࡪ࡟ࡱࡹࡢࡷࡹࡵࡰࡠࡨࡱࠫᎋ"),
                 bstack1l1llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡤࡦࡨࡨࡶࡷ࡫ࡤࡠࡲࡺࡣࡷ࡫ࡦࠨᎌ")):
      try:
        delattr(_1l111l11_opy_, attr)
      except AttributeError:
        pass
    for attr in (bstack1l1llll_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᎍ"), bstack1l1llll_opy_ (u"ࠨࡣ࠴࠵ࡾࡥࡳࡵࡣࡵࡸࡪࡪࠧᎎ"), bstack1l1llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨᎏ"),
                 bstack1l1llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡓࡥ࡬࡫ࠧ᎐"), bstack1l1llll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡘࡪࡹࡴࡆࡴࡵࡳࡷࡓࡥࡴࡵࡤ࡫ࡪࡹࠧ᎑"),
                 bstack1l1llll_opy_ (u"ࠬࡧ࠱࠲ࡻࡢࡷࡦࡼࡥࡠࡴࡨࡷࡺࡲࡴࡠࡦࡲࡲࡪ࠭᎒"), bstack1l1llll_opy_ (u"࠭ࡡ࠲࠳ࡼࡣࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡲࡦࡳࡥࠨ᎓"),
                 bstack1l1llll_opy_ (u"ࠧࡢ࠳࠴ࡽࡤࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ᎔"), bstack1l1llll_opy_ (u"ࠨࡣ࠴࠵ࡾࡋ࡮ࡢࡤ࡯ࡩࡩ࠭᎕"),
                 bstack1l1llll_opy_ (u"ࠩࡢࡦࡸࡺࡡࡤ࡭ࡢࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴࡠࡦࡲࡲࡪ࠭᎖")):
      try:
        delattr(_1l111l11_opy_, attr)
      except AttributeError:
        pass
    try:
      _1ll1llll11_opy_ = threading.main_thread()
      if _1ll1llll11_opy_ != _1l111l11_opy_:
        for attr in (bstack1l1llll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ᎗"), bstack1l1llll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ᎘")):
          try:
            delattr(_1ll1llll11_opy_, attr)
          except AttributeError:
            pass
    except Exception:
      pass
    if _wrapper:
      try:
        _wrapper._page = None
        _wrapper._browser = None
      except Exception:
        pass
    logger.debug(bstack1l1llll_opy_ (u"ࠬࡊࡥࡧࡧࡵࡶࡪࡪࠠࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡨࡲ࡯ࡴࡧࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࡩࠦࡦࡰࡴࠣࡸ࡭ࡸࡥࡢࡦࠣࡿࢂ࠭᎙").format(_1l111l11_opy_.ident))
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"࠭ࡄࡦࡨࡨࡶࡷ࡫ࡤࠡࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡩ࡬ࡰࡵࡨࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽࠨ᎚").format(str(e)))
def mod_behave_run_hook(self, name, *args):
  global bstack111ll1l1l1_opy_
  global bstack1l1ll1ll1l1_opy_
  try:
    if BROWSERSTACK_AUTOMATION:
      platform_index = int(threading.current_thread()._name) % bstack1111111l1_opy_
      bstack1l1l1l1lll_opy_ = CONFIG[bstack1l1llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ᎛")][platform_index]
      os.environ[bstack1l1llll_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩ᎜")] = json.dumps(bstack1l1l1l1lll_opy_)
    if not hasattr(self, bstack1l1llll_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡷࡪࡪࠧ᎝")):
      self.driver_initialised = None
    bstack1lll111l11l_opy_ = {
        bstack1l1llll_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠧ᎞"): handle_before_all,
        bstack1l1llll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠬ᎟"): handle_before_feature,
        bstack1l1llll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡺࡡࡨࠩᎠ"): handle_before_tag,
        bstack1l1llll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨᎡ"): handle_before_scenario,
        bstack1l1llll_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠬᎢ"): handle_before_step,
        bstack1l1llll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡴࡶࡨࡴࠬᎣ"): handle_after_step,
        bstack1l1llll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪᎤ"): handle_after_scenario,
        bstack1l1llll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡷࡥ࡬࠭Ꭵ"): handle_after_tag,
        bstack1l1llll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫᎦ"): handle_after_feature,
        bstack1l1llll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠨᎧ"): handle_after_all
    }
    handler = bstack1lll111l11l_opy_.get(name, bstack111ll1l1l1_opy_)
    try:
      if args:
        context = args[0]
        remaining_args = args[1:]
        if bstack1l1ll1ll1l1_opy_ is None or not bstack1l1ll1ll1l1_opy_:
          context = self.context
          remaining_args = args
      else:
        context = self.context
        remaining_args = ()
      handler(self, name, context, bstack111ll1l1l1_opy_, *remaining_args)
    except Exception as e:
      logger.debug(bstack1l1llll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡤࡨ࡬ࡦࡼࡥࠡࡪࡲࡳࡰࠦࡨࡢࡰࡧࡰࡪࡸࠠࡼࡿ࠽ࠤࢀࢃࠧᎨ").format(name, str(e)))
    if name == bstack1l1llll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨᎩ"):
      _execute_deferred_playwright_close()
    if not cli.is_running() and name in [bstack1l1llll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨᎪ"), bstack1l1llll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪᎫ"), bstack1l1llll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ࠭Ꭼ")]:
      try:
        bstack111ll1ll11_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1ll1l1l1l_opy_(bstack1l1llll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪᎭ")) else context.browser
        bstack11l1l11l11_opy_ = (
          (name == bstack1l1llll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠨᎮ") and self.driver_initialised == bstack1l1llll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥᎯ")) or
          (name == bstack1l1llll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡦࡦࡣࡷࡹࡷ࡫ࠧᎰ") and self.driver_initialised == bstack1l1llll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠤᎱ")) or
          (name == bstack1l1llll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪᎲ") and self.driver_initialised in [bstack1l1llll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧᎳ"), bstack1l1llll_opy_ (u"ࠦ࡮ࡴࡳࡵࡧࡳࠦᎴ")]) or
          (name == bstack1l1llll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡺࡥࡱࠩᎵ") and self.driver_initialised == bstack1l1llll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦᎶ"))
        )
        if bstack11l1l11l11_opy_:
          self.driver_initialised = None
          if bstack111ll1ll11_opy_ and hasattr(bstack111ll1ll11_opy_, bstack1l1llll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠫᎷ")):
            try:
              bstack111ll1ll11_opy_.quit()
            except Exception as e:
              logger.debug(bstack1l1llll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡲࡷ࡬ࡸࡹ࡯࡮ࡨࠢࡧࡶ࡮ࡼࡥࡳࠢ࡬ࡲࠥࡨࡥࡩࡣࡹࡩࠥ࡮࡯ࡰ࡭࠽ࠤࢀࢃࠧᎸ").format(str(e)))
      except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࠣ࡬ࡴࡵ࡫ࠡࡥ࡯ࡩࡦࡴࡵࡱࠢࡩࡳࡷࠦࡻࡾ࠼ࠣࡿࢂ࠭Ꮉ").format(name, str(e)))
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"ࠪࡇࡷ࡯ࡴࡪࡥࡤࡰࠥ࡫ࡲࡳࡱࡵࠤ࡮ࡴࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡳࡷࡱࠤ࡭ࡵ࡯࡬ࠢࡾࢁ࠿ࠦࡻࡾࠩᎺ").format(name, str(e)))
    try:
      if bstack1l1ll1ll1l1_opy_ is None or bstack1l1ll1ll1l1_opy_:
        try:
          bstack111ll1l1l1_opy_(self, name, self.context, *args)
        except TypeError:
          bstack111ll1l1l1_opy_(self, name, *args)
      else:
        bstack111ll1l1l1_opy_(self, name, *args)
    except Exception as e2:
      logger.debug(bstack1l1llll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡱࡵ࡭࡬࡯࡮ࡢ࡮ࠣࡦࡪ࡮ࡡࡷࡧࠣ࡬ࡴࡵ࡫ࠡࡽࢀ࠾ࠥࢁࡽࠨᎻ").format(name, str(e2)))
  finally:
    if name == bstack1l1llll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭Ꮌ"):
      _execute_deferred_playwright_close()
def bstack1l1lll11l11_opy_(config, startdir):
  return bstack1l1llll_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡀࠠࡼ࠲ࢀࠦᎽ").format(bstack1l1llll_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨᎾ"))
notset = Notset()
def bstack11111l1ll1_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1l111l1ll1_opy_
  if str(name).lower() == bstack1l1llll_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࠨᎿ"):
    return bstack1l1llll_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣᏀ")
  else:
    return bstack1l111l1ll1_opy_(self, name, default, skip)
def bstack1l11llll1l_opy_(item, when):
  global bstack111l1lll11_opy_
  try:
    bstack111l1lll11_opy_(item, when)
  except Exception as e:
    pass
def bstack111l11lll1_opy_():
  return
def bstack1lll111ll_opy_(type, name, status, reason, bstack11l1l11l_opy_, bstack1l11ll11_opy_):
  bstack11111ll1l1_opy_ = {
    bstack1l1llll_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪᏁ"): type,
    bstack1l1llll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᏂ"): {}
  }
  if type == bstack1l1llll_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧᏃ"):
    bstack11111ll1l1_opy_[bstack1l1llll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᏄ")][bstack1l1llll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭Ꮕ")] = bstack11l1l11l_opy_
    bstack11111ll1l1_opy_[bstack1l1llll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᏆ")][bstack1l1llll_opy_ (u"ࠩࡧࡥࡹࡧࠧᏇ")] = json.dumps(str(bstack1l11ll11_opy_))
  if type == bstack1l1llll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᏈ"):
    bstack11111ll1l1_opy_[bstack1l1llll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᏉ")][bstack1l1llll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᏊ")] = name
  if type == bstack1l1llll_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩᏋ"):
    bstack11111ll1l1_opy_[bstack1l1llll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᏌ")][bstack1l1llll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᏍ")] = status
    if status == bstack1l1llll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᏎ"):
      bstack11111ll1l1_opy_[bstack1l1llll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭Ꮟ")][bstack1l1llll_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫᏐ")] = json.dumps(str(reason))
  bstack1lll111111_opy_ = bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪᏑ").format(json.dumps(bstack11111ll1l1_opy_))
  return bstack1lll111111_opy_
def bstack1111l11ll1_opy_(driver_command, response):
    if driver_command == bstack1l1llll_opy_ (u"࠭ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪᏒ"):
        TestHubHandler.bstack1ll11ll1ll_opy_({
            bstack1l1llll_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭Ꮣ"): response[bstack1l1llll_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧᏔ")],
            bstack1l1llll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᏕ"): TestHubHandler.current_test_uuid()
        })
def bstack1lll11ll11l_opy_(item, call, rep):
  global bstack1llllll1lll_opy_
  global bstack1111ll11l_opy_
  global bstack11l11l1l1l_opy_
  name = bstack1l1llll_opy_ (u"ࠪࠫᏖ")
  try:
    if rep.when == bstack1l1llll_opy_ (u"ࠫࡨࡧ࡬࡭ࠩᏗ"):
      bstack11llll1l11_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack11l11l1l1l_opy_:
          name = str(rep.nodeid)
          bstack1l1lll11l_opy_ = bstack1lll111ll_opy_(bstack1l1llll_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭Ꮨ"), name, bstack1l1llll_opy_ (u"࠭ࠧᏙ"), bstack1l1llll_opy_ (u"ࠧࠨᏚ"), bstack1l1llll_opy_ (u"ࠨࠩᏛ"), bstack1l1llll_opy_ (u"ࠩࠪᏜ"))
          threading.current_thread().bstack1l1l1ll1ll1_opy_ = name
          for driver in bstack1111ll11l_opy_:
            if bstack11llll1l11_opy_ == driver.session_id:
              driver.execute_script(bstack1l1lll11l_opy_)
      except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪᏝ").format(str(e)))
      try:
        bstack1lll11l11l_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack1l1llll_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᏞ"):
          status = bstack1l1llll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᏟ") if rep.outcome.lower() == bstack1l1llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭Ꮰ") else bstack1l1llll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᏡ")
          reason = bstack1l1llll_opy_ (u"ࠨࠩᏢ")
          if status == bstack1l1llll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᏣ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack1l1llll_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨᏤ") if status == bstack1l1llll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᏥ") else bstack1l1llll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᏦ")
          data = name + bstack1l1llll_opy_ (u"࠭ࠠࡱࡣࡶࡷࡪࡪࠡࠨᏧ") if status == bstack1l1llll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᏨ") else name + bstack1l1llll_opy_ (u"ࠨࠢࡩࡥ࡮ࡲࡥࡥࠣࠣࠫᏩ") + reason
          bstack1lll11l1lll_opy_ = bstack1lll111ll_opy_(bstack1l1llll_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫᏪ"), bstack1l1llll_opy_ (u"ࠪࠫᏫ"), bstack1l1llll_opy_ (u"ࠫࠬᏬ"), bstack1l1llll_opy_ (u"ࠬ࠭Ꮽ"), level, data)
          for driver in bstack1111ll11l_opy_:
            if bstack11llll1l11_opy_ == driver.session_id:
              driver.execute_script(bstack1lll11l1lll_opy_)
      except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡧࡴࡴࡴࡦࡺࡷࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪᏮ").format(str(e)))
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡷࡹࡧࡴࡦࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࡽࢀࠫᏯ").format(str(e)))
  bstack1llllll1lll_opy_(item, call, rep)
def bstack11ll111111_opy_(driver, bstack1l1l1l11ll1_opy_, test=None):
  global PLATFORM_INDEX
  if test != None:
    bstack1lll1llll1l_opy_ = getattr(test, bstack1l1llll_opy_ (u"ࠨࡰࡤࡱࡪ࠭Ᏸ"), None)
    bstack11l1l11ll1_opy_ = getattr(test, bstack1l1llll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᏱ"), None)
    PercySDK.screenshot(driver, bstack1l1l1l11ll1_opy_, bstack1lll1llll1l_opy_=bstack1lll1llll1l_opy_, bstack11l1l11ll1_opy_=bstack11l1l11ll1_opy_, bstack1llllll11l_opy_=PLATFORM_INDEX)
  else:
    PercySDK.screenshot(driver, bstack1l1l1l11ll1_opy_)
@measure(event_name=EVENTS.bstack111l1111ll_opy_, stage=STAGE.SINGLE, bstack11lllll111_opy_=SESSION_NAME)
def bstack1llll1111ll_opy_(driver):
  if bstack111lll1l1l_opy_.bstack11l111lll1_opy_() is True or bstack111lll1l1l_opy_.capturing() is True:
    return
  bstack111lll1l1l_opy_.bstack111ll111l1_opy_()
  while not bstack111lll1l1l_opy_.bstack11l111lll1_opy_():
    bstack1ll11l1ll1_opy_ = bstack111lll1l1l_opy_.bstack11ll1l1l11_opy_()
    bstack11ll111111_opy_(driver, bstack1ll11l1ll1_opy_)
  bstack111lll1l1l_opy_.bstack1llll1l11ll_opy_()
def bstack1l1ll111111_opy_(sequence, driver_command, response = None, bstack111111l111_opy_ = None, args = None):
    try:
      if sequence != bstack1l1llll_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪᏲ"):
        return
      if percy.bstack1lll11llll1_opy_() == bstack1l1llll_opy_ (u"ࠦ࡫ࡧ࡬ࡴࡧࠥᏳ"):
        return
      bstack1ll11l1ll1_opy_ = bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠬࡶࡥࡳࡥࡼࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᏴ"), None)
      for command in bstack1ll1l1l111_opy_:
        if command == driver_command:
          with bstack1l1111ll1l_opy_:
            bstack111111llll_opy_ = bstack1111ll11l_opy_.copy()
          for driver in bstack111111llll_opy_:
            bstack1llll1111ll_opy_(driver)
      bstack1l11l111ll_opy_ = percy.bstack1l1ll1l1lll_opy_()
      if driver_command in bstack1l1l1llll1_opy_[bstack1l11l111ll_opy_]:
        bstack111lll1l1l_opy_.bstack1l11l11111_opy_(bstack1ll11l1ll1_opy_, driver_command)
    except Exception as e:
      pass
_1lllll1111_opy_ = threading.Event()
def bstack1ll11111l11_opy_(framework_name):
  if global_config.get_property(bstack1l1llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪᏵ")):
      _1lllll1111_opy_.wait(timeout=30)
      return
  global_config.bstack1ll11l111l_opy_(bstack1l1llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟࡮ࡱࡧࡣࡨࡧ࡬࡭ࡧࡧࠫ᏶"), True)
  global FRAMEWORK_NAME
  global SELENIUM_OR_PLAYWRIGHT_INSTALLED
  global bstack1ll11l1lll_opy_
  FRAMEWORK_NAME = framework_name
  logger.info(bstack11l1llll11_opy_.format(FRAMEWORK_NAME.split(bstack1l1llll_opy_ (u"ࠨ࠯ࠪ᏷"))[0]))
  bstack1l111l11l1_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    global bstack1l11l11l11_opy_
    bstack1ll11l1111l_opy_ = BROWSERSTACK_AUTOMATION or bstack1l11l11l11_opy_
    if bstack1ll11l1111l_opy_:
      Service.start = bstack1ll11llll11_opy_
      Service.stop = bstack1ll11l1l1l_opy_
      webdriver.Remote.get = bstack1ll1ll11l1l_opy_
      WebDriver.quit = bstack11lll1l111_opy_
      webdriver.Remote.__init__ = bstack1111ll11ll_opy_
    if not BROWSERSTACK_AUTOMATION and not bstack1l11l11l11_opy_:
        webdriver.Remote.__init__ = bstack1lll11llll_opy_
    WebDriver.getAccessibilityResults = getAccessibilityResults
    WebDriver.get_accessibility_results = getAccessibilityResults
    WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
    WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
    WebDriver.performScan = perform_scan
    WebDriver.perform_scan = perform_scan
    WebDriver.execute = bstack1ll1llll1l_opy_
    SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
  except Exception as e:
    pass
  try:
    bstack1ll11l1111l_opy_ = BROWSERSTACK_AUTOMATION or bstack1l11l11l11_opy_
    if bstack1ll11l1111l_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1lll1lll111_opy_
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
    logger.debug(bstack1l1llll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡧ࡭ࡱࡥࡥࡱࡹ࠺ࠡࡽࢀࠦᏸ").format(str(e)))
  patch_playwright()
  if not SELENIUM_OR_PLAYWRIGHT_INSTALLED:
    bstack1ll1l1lll1_opy_(bstack1l1llll_opy_ (u"ࠥࡔࡦࡩ࡫ࡢࡩࡨࡷࠥࡴ࡯ࡵࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠧᏹ"), bstack1ll11111l1l_opy_)
  if bstack1111lll11l_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      if hasattr(RemoteConnection, bstack1l1llll_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬᏺ")) and callable(getattr(RemoteConnection, bstack1l1llll_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭ᏻ"))):
        RemoteConnection._get_proxy_url = bstack1ll1ll1lll1_opy_
      else:
        from selenium.webdriver.remote.client_config import ClientConfig
        ClientConfig.get_proxy_url = bstack1ll1ll1lll1_opy_
    except Exception as e:
      logger.error(bstack1ll1l1l1l1_opy_.format(str(e)))
  if bstack1lll111ll11_opy_():
    bstack111l11111_opy_(CONFIG, logger)
  if (bstack1l1llll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬᏼ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      try:
        from pabot.pabot import QueueItem
        from pabot import pabot
      except Exception as e:
        logger.warning(bstack1l1l11lll11_opy_ + str(e))
      if not is_robot_playwright_installed():
        try:
          if percy.bstack1lll11llll1_opy_() == bstack1l1llll_opy_ (u"ࠢࡵࡴࡸࡩࠧᏽ"):
            bstack1llllllllll_opy_(bstack1l1ll111111_opy_)
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
          WebDriverCreator._get_ff_profile = bstack1l1ll1lll1_opy_
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
          WebDriverCache.close = bstack1ll11l11l11_opy_
        except Exception as e:
          logger.warning(bstack1lll11l1ll_opy_ + str(e))
        try:
          from AppiumLibrary.utils.applicationcache import ApplicationCache
          ApplicationCache.close = bstack1ll111l11l_opy_
        except Exception as e:
          logger.debug(bstack11l11l11ll_opy_ + str(e))
    except Exception as e:
      bstack1ll1l1lll1_opy_(e, bstack1lll11l1ll_opy_)
    Output.start_test = bstack1l1l11l1111_opy_
    Output.end_test = bstack1lllll1lll1_opy_
    TestStatus.__init__ = bstack1l1l1l1lll1_opy_
    QueueItem.__init__ = bstack1ll1l111111_opy_
    pabot._create_items = bstack1l1l11l1l11_opy_
    try:
      from pabot import __version__ as bstack1ll1ll11ll1_opy_
      if version.parse(bstack1ll1ll11ll1_opy_) >= version.parse(bstack1l1llll_opy_ (u"ࠨ࠷࠱࠴࠳࠶ࠧ᏾")):
        pabot._run = bstack1ll11l1l11l_opy_
      elif version.parse(bstack1ll1ll11ll1_opy_) >= version.parse(bstack1l1llll_opy_ (u"ࠩ࠷࠲࠷࠴࠰ࠨ᏿")):
        pabot._run = bstack1l1l1ll1111_opy_
      elif version.parse(bstack1ll1ll11ll1_opy_) >= version.parse(bstack1l1llll_opy_ (u"ࠪ࠶࠳࠷࠵࠯࠲ࠪ᐀")):
        pabot._run = bstack1ll11l11ll_opy_
      elif version.parse(bstack1ll1ll11ll1_opy_) >= version.parse(bstack1l1llll_opy_ (u"ࠫ࠷࠴࠱࠴࠰࠳ࠫᐁ")):
        pabot._run = bstack1ll111111ll_opy_
      else:
        pabot._run = bstack11l111l111_opy_
    except Exception as e:
      pabot._run = bstack11l111l111_opy_
    pabot._create_command_for_execution = bstack1l1l11ll11_opy_
    pabot._report_results = bstack111l1l1lll_opy_
  if bstack1l1llll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬᐂ") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll1l1lll1_opy_(e, bstack1l111lllll_opy_)
    Runner.run_hook = mod_behave_run_hook
    try:
      from behave import __version__ as bstack1ll111lll1l_opy_
      if version.parse(bstack1ll111lll1l_opy_) >= version.parse(bstack1l1llll_opy_ (u"࠭࠱࠯࠵࠱࠴ࠬᐃ")):
        Runner.load_hooks = mod_behave_load_hooks
    except Exception as e:
      logger.debug(bstack1l1llll_opy_ (u"ࠧࡄࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡢࡦࡪࡤࡺࡪࠦࡶࡦࡴࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫᐄ").format(str(e)))
    Step.run = mod_behave_step_run
  if bstack1l1llll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᐅ") in str(framework_name).lower():
    if not BROWSERSTACK_AUTOMATION:
      _install_driver_init_failure_capture()
      _install_playwright_init_failure_capture()
      _1lllll1111_opy_.set()
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack1l1lll11l11_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack111l11lll1_opy_
      Config.getoption = bstack11111l1ll1_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1lll11ll11l_opy_
    except Exception as e:
      pass
  _install_driver_init_failure_capture()
  _install_playwright_init_failure_capture()
  _1lllll1111_opy_.set()
def bstack1llll11l1l1_opy_():
  global CONFIG
  if bstack1l1llll_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᐆ") in CONFIG and int(CONFIG[bstack1l1llll_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᐇ")]) > 1:
    logger.warning(bstack1lll1ll1l1l_opy_)
def bstack1ll11ll1111_opy_(arg, bstack11l1l11l1_opy_, bstack111111111l_opy_=None):
  global CONFIG
  global bstack1lll1ll1l11_opy_
  global bstack11ll111lll_opy_
  global BROWSERSTACK_AUTOMATION
  global bstack1l11l11l11_opy_
  global global_config
  bstack11l11l1ll1_opy_ = bstack1l1llll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᐈ")
  if bstack11l1l11l1_opy_ and isinstance(bstack11l1l11l1_opy_, str):
    bstack11l1l11l1_opy_ = eval(bstack11l1l11l1_opy_)
  CONFIG = bstack11l1l11l1_opy_[bstack1l1llll_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬᐉ")]
  bstack1lll1ll1l11_opy_ = bstack11l1l11l1_opy_[bstack1l1llll_opy_ (u"࠭ࡈࡖࡄࡢ࡙ࡗࡒࠧᐊ")]
  bstack11ll111lll_opy_ = bstack11l1l11l1_opy_[bstack1l1llll_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩᐋ")]
  BROWSERSTACK_AUTOMATION = bstack11l1l11l1_opy_[bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫᐌ")]
  try:
    bstack111l11111l_opy_ = bstack11l1l11l1_opy_.get(bstack1l1llll_opy_ (u"ࠩࡒ࡚ࡊࡘࡒࡊࡆࡈࡣࡑࡕࡁࡅࡡࡗࡉࡘ࡚ࡉࡏࡉࠪᐍ"), False)
    bstack1l11l11l11_opy_ = bool(bstack111l11111l_opy_)
    os.environ[bstack1l1llll_opy_ (u"ࠪࡓ࡛ࡋࡒࡓࡋࡇࡉࡤࡒࡏࡂࡆࡢࡘࡊ࡙ࡔࡊࡐࡊࠫᐎ")] = str(bstack1l11l11l11_opy_).lower()
  except Exception as e:
    logger.error(bstack1l1llll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡑ࡙ࡉࡗࡘࡉࡅࡇࡢࡐࡔࡇࡄࡠࡖࡈࡗ࡙ࡏࡎࡈ࠼ࠣࡿࢂࠨᐏ").format(e))
    bstack1l11l11l11_opy_ = False
    os.environ[bstack1l1llll_opy_ (u"ࠬࡕࡖࡆࡔࡕࡍࡉࡋ࡟ࡍࡑࡄࡈࡤ࡚ࡅࡔࡖࡌࡒࡌ࠭ᐐ")] = bstack1l1llll_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬᐑ")
  global_config.bstack1ll11l111l_opy_(bstack1l1llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨᐒ"), BROWSERSTACK_AUTOMATION)
  os.environ[bstack1lll1l11111_opy_] = bstack11l11l1ll1_opy_
  os.environ[bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍࠧᐓ")] = json.dumps(CONFIG)
  os.environ[bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡊࡘࡆࡤ࡛ࡒࡍࠩᐔ")] = bstack1lll1ll1l11_opy_
  os.environ[bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫᐕ")] = str(bstack11ll111lll_opy_)
  os.environ[bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡑ࡛ࡇࡊࡐࠪᐖ")] = str(True)
  if bstack11l11111ll_opy_(arg, [bstack1l1llll_opy_ (u"ࠬ࠳࡮ࠨᐗ"), bstack1l1llll_opy_ (u"࠭࠭࠮ࡰࡸࡱࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧᐘ")]) != -1:
    os.environ[bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡂࡔࡄࡐࡑࡋࡌࠨᐙ")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1l1l1ll11l1_opy_)
    return
  bstack1ll1l11l1l1_opy_()
  global bstack1l1lll1lll_opy_
  global PLATFORM_INDEX
  global bstack1ll1ll111ll_opy_
  global bstack1l1ll1lll1l_opy_
  global bstack1lll1llll1_opy_
  global bstack1ll11l1lll_opy_
  global PARALLELISE_VANILLA_PYTHON
  arg.append(bstack1l1llll_opy_ (u"ࠣ࠯࡚ࠦᐚ"))
  arg.append(bstack1l1llll_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡦ࠼ࡐࡳࡩࡻ࡬ࡦࠢࡤࡰࡷ࡫ࡡࡥࡻࠣ࡭ࡲࡶ࡯ࡳࡶࡨࡨ࠿ࡶࡹࡵࡧࡶࡸ࠳ࡖࡹࡵࡧࡶࡸ࡜ࡧࡲ࡯࡫ࡱ࡫ࠧᐛ"))
  arg.append(bstack1l1llll_opy_ (u"ࠥ࠱࡜ࠨᐜ"))
  arg.append(bstack1l1llll_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨ࠾࡙࡮ࡥࠡࡪࡲࡳࡰ࡯࡭ࡱ࡮ࠥᐝ"))
  global bstack1l1l1l111l1_opy_
  global bstack1lllll11111_opy_
  global bstack1l1l111l11l_opy_
  global bstack1111l1l1l1_opy_
  global bstack11l1l1l1l1_opy_
  global bstack111lll1l11_opy_
  global bstack1llllll111l_opy_
  global bstack11l11ll1ll_opy_
  global bstack11l1111111_opy_
  global bstack11l1l11l1l_opy_
  global bstack1l111l1ll1_opy_
  global bstack111l1lll11_opy_
  global bstack1llllll1lll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l1l1l111l1_opy_ = webdriver.Remote.__init__
    bstack1lllll11111_opy_ = WebDriver.quit
    bstack11l11ll1ll_opy_ = WebDriver.close
    bstack11l1111111_opy_ = WebDriver.get
    bstack1l1l111l11l_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack11ll1l1ll1_opy_(CONFIG) and bstack1l1111l1ll_opy_():
    if bstack1l1ll11111_opy_() < version.parse(bstack1l1l1ll1l11_opy_):
      logger.error(bstack1ll1ll1l1l_opy_.format(bstack1l1ll11111_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack1l1llll_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭ᐞ")) and callable(getattr(RemoteConnection, bstack1l1llll_opy_ (u"࠭࡟ࡨࡧࡷࡣࡵࡸ࡯ࡹࡻࡢࡹࡷࡲࠧᐟ"))):
          bstack11l1l11l1l_opy_ = RemoteConnection._get_proxy_url
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          bstack11l1l11l1l_opy_ = ClientConfig.get_proxy_url
      except Exception as e:
        logger.error(bstack1ll1l1l1l1_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1l111l1ll1_opy_ = Config.getoption
    from _pytest import runner
    bstack111l1lll11_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warning(bstack1l1llll_opy_ (u"ࠢࠦࡵ࠽ࠤࠪࡹࠢᐠ"), bstack11llllll1_opy_, str(e))
  try:
    from pytest_bdd import reporting
    bstack1llllll1lll_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡰࠢࡵࡹࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࡴࠩᐡ"))
  if cli.is_enabled(CONFIG) and cli.config:
    bstack1ll1ll111ll_opy_ = cli.config.get(bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ᐢ"), {}).get(bstack1l1llll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᐣ"))
  else:
    bstack1ll1ll111ll_opy_ = CONFIG.get(bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨᐤ"), {}).get(bstack1l1llll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᐥ"))
  PARALLELISE_VANILLA_PYTHON = True
  if cli.is_enabled(CONFIG):
    if cli.bstack111l1ll11_opy_():
      bstack111ll1l11_opy_.invoke(Events.CONNECT, bstack111ll11ll_opy_())
    if not bstack111l11l11l_opy_(CONFIG):
      try:
        bstack1ll11111l11_opy_(bstack1l111lll1l_opy_)
      except Exception as _e:
        logger.debug(bstack1l1llll_opy_ (u"ࠨࡢࡴࡶࡤࡧࡰࡀࡦࡢ࡮ࡶࡩࠥࡳ࡯ࡥࡡࡩࡳࡷࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡾࠤᐦ").format(_e))
    platform_index = int(os.environ.get(bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᐧ"), bstack1l1llll_opy_ (u"ࠨ࠲ࠪᐨ")))
  else:
    bstack1ll11111l11_opy_(bstack1l111lll1l_opy_)
  _install_driver_init_failure_capture()
  _install_playwright_init_failure_capture()
  os.environ[bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪᐩ")] = CONFIG[bstack1l1llll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᐪ")]
  os.environ[bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧᐫ")] = CONFIG[bstack1l1llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᐬ")]
  os.environ[bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩᐭ")] = BROWSERSTACK_AUTOMATION.__str__()
  from _pytest.config import main as bstack1l1ll11ll11_opy_
  bstack1l1lll11111_opy_ = []
  try:
    exit_code = bstack1l1ll11ll11_opy_(arg)
    if cli.is_enabled(CONFIG):
      cli.bstack1l1lll11l1l_opy_()
    if bstack1l1llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷࠫᐮ") in multiprocessing.current_process().__dict__.keys():
      for bstack1l1lllll11l_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1l1lll11111_opy_.append(bstack1l1lllll11l_opy_)
    try:
      bstack1ll1llll111_opy_ = (bstack1l1lll11111_opy_, int(exit_code))
      bstack111111111l_opy_.append(bstack1ll1llll111_opy_)
    except Exception as e:
      logger.debug(bstack1l1llll_opy_ (u"ࠣࡧࡻ࡭ࡹࡥࡣࡰࡦࡨࠤ࡮ࡴࡴࠡࡥࡲࡩࡷࡩࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࢀࢃ࠺ࠡࡽࢀࠦᐯ").format(type(e).__name__, e), exc_info=True)
      bstack111111111l_opy_.append((bstack1l1lll11111_opy_, exit_code))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack1l1lll11111_opy_.append({bstack1l1llll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᐰ"): bstack1l1llll_opy_ (u"ࠪࡔࡷࡵࡣࡦࡵࡶࠤࠬᐱ") + os.environ.get(bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᐲ")), bstack1l1llll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᐳ"): traceback.format_exc(), bstack1l1llll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬᐴ"): int(os.environ.get(bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᐵ")))})
    bstack111111111l_opy_.append((bstack1l1lll11111_opy_, 1))
def mod_behave_main(args, retries):
  try:
    from behave.configuration import Configuration
    from behave.__main__ import run_behave
    from browserstack_sdk.bstack_behave_runner import BehaveRunner
    config = Configuration(args)
    config.update_userdata({bstack1l1llll_opy_ (u"ࠣࡴࡨࡸࡷ࡯ࡥࡴࠤᐶ"): str(retries)})
    return run_behave(config, runner_class=BehaveRunner)
  except Exception as e:
    bstack11l11ll11l_opy_ = e.__class__.__name__
    print(bstack1l1llll_opy_ (u"ࠤࠨࡷ࠿ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡢࡦࡪࡤࡺࡪࠦࡴࡦࡵࡷࠤࠪࡹࠢᐷ") % (bstack11l11ll11l_opy_, e))
    return 1
def bstack1l1llll1l1l_opy_(arg):
  global bstack1l1l1l11l1l_opy_
  bstack1ll11111l11_opy_(bstack1ll111ll1ll_opy_)
  if cli.is_enabled(CONFIG):
    cli.bstack1ll1111l11l_opy_(platform_index=0)
    if cli.automation_framework and cli.bstack1l1ll1l1111_opy_(EventDispatcherModule):
      cli.bstack1ll11l111_opy_(bstack1l1llll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪᐸ"))
  os.environ[bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬᐹ")] = str(bstack11ll111lll_opy_)
  retries = bstack11ll1111l_opy_.bstack1l1111111_opy_(CONFIG)
  status_code = 0
  if bstack11ll1111l_opy_.bstack11lll1l1l_opy_(CONFIG):
    status_code = mod_behave_main(arg, retries)
  else:
    from behave.__main__ import main as bstack1l1111ll11_opy_
    status_code = bstack1l1111ll11_opy_(arg)
  if status_code != 0:
    bstack1l1l1l11l1l_opy_ = status_code
def bstack1l1l1l1l11l_opy_():
  logger.info(bstack1ll11lll11_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1l1llll_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᐺ"), help=bstack1l1llll_opy_ (u"࠭ࡇࡦࡰࡨࡶࡦࡺࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡤࡱࡱࡪ࡮࡭ࠧᐻ"))
  parser.add_argument(bstack1l1llll_opy_ (u"ࠧ࠮ࡷࠪᐼ"), bstack1l1llll_opy_ (u"ࠨ࠯࠰ࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬᐽ"), help=bstack1l1llll_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡵࡴࡧࡵࡲࡦࡳࡥࠨᐾ"))
  parser.add_argument(bstack1l1llll_opy_ (u"ࠪ࠱ࡰ࠭ᐿ"), bstack1l1llll_opy_ (u"ࠫ࠲࠳࡫ࡦࡻࠪᑀ"), help=bstack1l1llll_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡤࡧࡨ࡫ࡳࡴࠢ࡮ࡩࡾ࠭ᑁ"))
  parser.add_argument(bstack1l1llll_opy_ (u"࠭࠭ࡧࠩᑂ"), bstack1l1llll_opy_ (u"ࠧ࠮࠯ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᑃ"), help=bstack1l1llll_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᑄ"))
  bstack11ll1lllll_opy_ = parser.parse_args()
  try:
    bstack1l1ll1111l_opy_ = bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡩࡨࡲࡪࡸࡩࡤ࠰ࡼࡱࡱ࠴ࡳࡢ࡯ࡳࡰࡪ࠭ᑅ")
    if bstack11ll1lllll_opy_.framework and bstack11ll1lllll_opy_.framework not in (bstack1l1llll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪᑆ"), bstack1l1llll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬᑇ")):
      bstack1l1ll1111l_opy_ = bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠮ࡺ࡯࡯࠲ࡸࡧ࡭ࡱ࡮ࡨࠫᑈ")
    bstack11ll1l11l1_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l1ll1111l_opy_)
    bstack1l11llllll_opy_ = open(bstack11ll1l11l1_opy_, bstack1l1llll_opy_ (u"࠭ࡲࠨᑉ"))
    bstack11ll1l1lll_opy_ = bstack1l11llllll_opy_.read()
    bstack1l11llllll_opy_.close()
    if bstack11ll1lllll_opy_.username:
      bstack11ll1l1lll_opy_ = bstack11ll1l1lll_opy_.replace(bstack1l1llll_opy_ (u"࡚ࠧࡑࡘࡖࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧᑊ"), bstack11ll1lllll_opy_.username)
    if bstack11ll1lllll_opy_.key:
      bstack11ll1l1lll_opy_ = bstack11ll1l1lll_opy_.replace(bstack1l1llll_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪᑋ"), bstack11ll1lllll_opy_.key)
    if bstack11ll1lllll_opy_.framework:
      bstack11ll1l1lll_opy_ = bstack11ll1l1lll_opy_.replace(bstack1l1llll_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪᑌ"), bstack11ll1lllll_opy_.framework)
    file_name = bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ᑍ")
    file_path = os.path.abspath(file_name)
    bstack1ll1lll111_opy_ = open(file_path, bstack1l1llll_opy_ (u"ࠫࡼ࠭ᑎ"))
    bstack1ll1lll111_opy_.write(bstack11ll1l1lll_opy_)
    bstack1ll1lll111_opy_.close()
    logger.info(bstack1llll111l1l_opy_)
    try:
      os.environ[bstack1lll1l11111_opy_] = bstack11ll1lllll_opy_.framework if bstack11ll1lllll_opy_.framework != None else bstack1l1llll_opy_ (u"ࠧࠨᑏ")
      config = yaml.safe_load(bstack11ll1l1lll_opy_)
      config[bstack1l1llll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ᑐ")] = bstack1l1llll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡴࡧࡷࡹࡵ࠭ᑑ")
      bstack1l1l111l1l1_opy_(bstack11111l111l_opy_, config)
    except Exception as e:
      logger.debug(bstack111lllllll_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1ll1ll1ll11_opy_.format(str(e)))
def bstack1l1l111l1l1_opy_(bstack1l1lll111_opy_, config, bstack111l111111_opy_=None, bstack1111ll1l11_opy_=False):
  global BROWSERSTACK_AUTOMATION
  global bstack1lll11l111l_opy_
  global global_config
  if not config:
    return
  if bstack111l111111_opy_ is None:
    bstack111l111111_opy_ = {}
  bstack1l111l11ll_opy_ = bstack1l1l11l11ll_opy_ if not BROWSERSTACK_AUTOMATION else (
    bstack11ll11llll_opy_ if bstack1l1llll_opy_ (u"ࠨࡣࡳࡴࠬᑒ") in config else (
        bstack1llllllll1l_opy_ if config.get(bstack1l1llll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᑓ")) else bstack1l1l11111l1_opy_
    )
)
  bstack1lll1l11ll_opy_ = False
  bstack1lll111l1l_opy_ = False
  if BROWSERSTACK_AUTOMATION is True:
      if bstack1l1llll_opy_ (u"ࠪࡥࡵࡶࠧᑔ") in config:
          bstack1lll1l11ll_opy_ = True
      else:
          bstack1lll111l1l_opy_ = True
  bstack1l1l111lll_opy_ = TestHubUtils.bstack1l11111lll_opy_(config, bstack1lll11l111l_opy_)
  bstack11l1l1l111_opy_ = bstack1lllll1lll_opy_()
  data = {
    bstack1l1llll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᑕ"): config[bstack1l1llll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᑖ")],
    bstack1l1llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᑗ"): config[bstack1l1llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᑘ")],
    bstack1l1llll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᑙ"): bstack1l1lll111_opy_,
    bstack1l1llll_opy_ (u"ࠩࡧࡩࡹ࡫ࡣࡵࡧࡧࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᑚ"): os.environ.get(bstack1lll1l11111_opy_, bstack1lll11l111l_opy_),
    bstack1l1llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᑛ"): bstack1lll1l11l1l_opy_,
    bstack1l1llll_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠭ᑜ"): bstack1ll11ll1ll1_opy_(),
    bstack1l1llll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨᑝ"): {
      bstack1l1llll_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᑞ"): str(config[bstack1l1llll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧᑟ")]) if bstack1l1llll_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨᑠ") in config else bstack1l1llll_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࠥᑡ"),
      bstack1l1llll_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩ࡛࡫ࡲࡴ࡫ࡲࡲࠬᑢ"): sys.version,
      bstack1l1llll_opy_ (u"ࠫࡷ࡫ࡦࡦࡴࡵࡩࡷ࠭ᑣ"): bstack111l1l1l11_opy_(os.environ.get(bstack1lll1l11111_opy_, bstack1lll11l111l_opy_)),
      bstack1l1llll_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠧᑤ"): bstack1l1llll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ᑥ"),
      bstack1l1llll_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨᑦ"): bstack1l111l11ll_opy_,
      bstack1l1llll_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭ᑧ"): bstack1l1l111lll_opy_,
      bstack1l1llll_opy_ (u"ࠩࡷࡩࡸࡺࡨࡶࡤࡢࡹࡺ࡯ࡤࠨᑨ"): os.environ[bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᑩ")],
      bstack1l1llll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᑪ"): os.environ.get(bstack1lll1l11111_opy_, bstack1lll11l111l_opy_),
      bstack1l1llll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᑫ"): bstack1l1l1l1l111_opy_(os.environ.get(bstack1lll1l11111_opy_, bstack1lll11l111l_opy_)),
      bstack1l1llll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᑬ"): bstack11l1l1l111_opy_.get(bstack1l1llll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᑭ")),
      bstack1l1llll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧᑮ"): bstack11l1l1l111_opy_.get(bstack1l1llll_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪᑯ")),
      bstack1l1llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ᑰ"): config[bstack1l1llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᑱ")] if config[bstack1l1llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᑲ")] else bstack1l1llll_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢᑳ"),
      bstack1l1llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᑴ"): str(config[bstack1l1llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᑵ")]) if bstack1l1llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᑶ") in config else bstack1l1llll_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦᑷ"),
      bstack1l1llll_opy_ (u"ࠫࡴࡹࠧᑸ"): sys.platform,
      bstack1l1llll_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧᑹ"): socket.gethostname(),
      bstack1l1llll_opy_ (u"࠭ࡩࡴࡅࡏࡍࡊࡴࡡࡣ࡮ࡨࡨࠬᑺ"): bstack1111ll1l11_opy_,
      bstack1l1llll_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥࠩᑻ"): global_config.get_property(bstack1l1llll_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪᑼ"))
    }
  }
  if not global_config.get_property(bstack1l1llll_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩᑽ")) is None:
    data[bstack1l1llll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭ᑾ")][bstack1l1llll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡓࡥࡵࡣࡧࡥࡹࡧࠧᑿ")] = {
      bstack1l1llll_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬᒀ"): bstack1l1llll_opy_ (u"࠭ࡵࡴࡧࡵࡣࡰ࡯࡬࡭ࡧࡧࠫᒁ"),
      bstack1l1llll_opy_ (u"ࠧࡴ࡫ࡪࡲࡦࡲࠧᒂ"): global_config.get_property(bstack1l1llll_opy_ (u"ࠨࡵࡧ࡯ࡐ࡯࡬࡭ࡕ࡬࡫ࡳࡧ࡬ࠨᒃ")),
      bstack1l1llll_opy_ (u"ࠩࡶ࡭࡬ࡴࡡ࡭ࡐࡸࡱࡧ࡫ࡲࠨᒄ"): global_config.get_property(bstack1l1llll_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡒࡴ࠭ᒅ"))
    }
  if bstack1l1lll111_opy_ == bstack1lll11111ll_opy_:
    data[bstack1l1llll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧᒆ")][bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡇࡴࡴࡦࡪࡩࠪᒇ")] = bstack1lll11l11l1_opy_(config)
    data[bstack1l1llll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩᒈ")][bstack1l1llll_opy_ (u"ࠧࡪࡵࡓࡩࡷࡩࡹࡂࡷࡷࡳࡊࡴࡡࡣ࡮ࡨࡨࠬᒉ")] = percy.bstack111l1l1111_opy_
    data[bstack1l1llll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫᒊ")][bstack1l1llll_opy_ (u"ࠩࡳࡩࡷࡩࡹࡃࡷ࡬ࡰࡩࡏࡤࠨᒋ")] = percy.percy_build_id
  if not bstack11ll1111l_opy_.bstack11111111ll_opy_(CONFIG):
    data[bstack1l1llll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭ᒌ")][bstack1l1llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠨᒍ")] = bstack11ll1111l_opy_.bstack11111111ll_opy_(CONFIG)
  bstack1llll1ll_opy_ = bstack1ll1l1ll_opy_.bstack1lll1l11_opy_(CONFIG, logger)
  bstack11ll1lll1_opy_ = bstack11ll1111l_opy_.bstack1lll1l11_opy_(config=CONFIG)
  if bstack1llll1ll_opy_ is not None and bstack11ll1lll1_opy_ is not None and bstack11ll1lll1_opy_.bstack1ll1lll1_opy_():
    data[bstack1l1llll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨᒎ")][bstack11ll1lll1_opy_.bstack1lll1111111_opy_()] = bstack1llll1ll_opy_.bstack1l11ll111l_opy_()
  update(data[bstack1l1llll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩᒏ")], bstack111l111111_opy_)
  try:
    response = bstack1111ll1111_opy_(bstack1l1llll_opy_ (u"ࠧࡑࡑࡖࡘࠬᒐ"), bstack11l11111l1_opy_(bstack1111l11lll_opy_), data, {
      bstack1l1llll_opy_ (u"ࠨࡣࡸࡸ࡭࠭ᒑ"): (config[bstack1l1llll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᒒ")], config[bstack1l1llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᒓ")])
    })
    if response:
      logger.debug(bstack111111ll1_opy_.format(bstack1l1lll111_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1l1llll1l11_opy_.format(str(e)))
def bstack111l1l1l11_opy_(framework):
  return bstack1l1llll_opy_ (u"ࠦࢀࢃ࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴ࢁࡽࠣᒔ").format(str(framework), __version__) if framework else bstack1l1llll_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࡿࢂࠨᒕ").format(
    __version__)
def bstack1ll1l11l1l1_opy_():
  global CONFIG
  global bstack1l1111l111_opy_
  if bool(CONFIG):
    return
  try:
    bstack111llll1ll_opy_()
    logger.debug(bstack1111l111l1_opy_.format(str(CONFIG)))
    bstack1l1111l111_opy_ = logger_utils.configure_logger(CONFIG, bstack1l1111l111_opy_)
    bstack1l111l11l1_opy_()
  except Exception as e:
    logger.error(bstack1l1llll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࠥᒖ") + str(e))
    sys.exit(1)
  atexit.register(bstack1111l1111l_opy_)
  if not os.environ.get(bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡅࡇࡢࡔࡑ࡛ࡇࡊࡐࡢࡑࡔࡊࡅࠨᒗ")):
    sys.excepthook = bstack1ll1lllll11_opy_
    signal.signal(signal.SIGINT, bstack1111111ll1_opy_)
    signal.signal(signal.SIGTERM, bstack1111111ll1_opy_)
def bstack1ll1lllll11_opy_(exctype, value, traceback):
  global bstack1111ll11l_opy_
  try:
    for driver in bstack1111ll11l_opy_:
      bstack1l1lll1ll1l_opy_(driver, bstack1l1llll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᒘ"), bstack1l1llll_opy_ (u"ࠤࡖࡩࡸࡹࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧᒙ") + str(value))
  except Exception:
    pass
  logger.info(bstack11lllll1ll_opy_)
  bstack11l1l1lll1_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack11l1l1lll1_opy_(message=bstack1l1llll_opy_ (u"ࠪࠫᒚ"), bstack1llll1lllll_opy_ = False, bstack1111ll1l11_opy_ = False):
  global CONFIG
  global global_config
  bstack111111lll1_opy_ = bstack1l1llll_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡉࡽࡩࡥࡱࡶ࡬ࡳࡳ࠭ᒛ") if bstack1llll1lllll_opy_ else bstack1l1llll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᒜ")
  bstack1l1llll1lll_opy_ = PerformanceTester.mark_start(EVENTS.bstack1111ll1lll_opy_)
  try:
    bstack111l111111_opy_ = {}
    bstack1lll1lll1ll_opy_ = global_config.get_property(bstack1l1llll_opy_ (u"࠭࡟ࡩࡷࡥࡅࡱࡲ࡯ࡤࡣࡷ࡭ࡴࡴࡄࡢࡶࡤࠫᒝ"))
    if bstack1lll1lll1ll_opy_:
      bstack111l111111_opy_[bstack1l1llll_opy_ (u"ࠧࡩࡷࡥࡅࡱࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧᒞ")] = bstack1lll1lll1ll_opy_
    if message:
      bstack111l111111_opy_[bstack111111lll1_opy_] = str(message)
    try:
      bstack1l1l111l1l1_opy_(bstack1lll11111ll_opy_, CONFIG, bstack111l111111_opy_, bstack1111ll1l11_opy_)
    finally:
      PerformanceTester.end(EVENTS.bstack1111ll1lll_opy_.value, bstack1l1llll1lll_opy_ + bstack1l1llll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᒟ"), bstack1l1llll1lll_opy_ + bstack1l1llll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᒠ"), status=True, failure=None, test_name=None)
  except Exception as e:
    logger.debug(bstack1lllll1l11_opy_.format(str(e)))
def bstack1ll1l11111l_opy_(bstack111111111_opy_, size):
  bstack1l1l11ll11l_opy_ = []
  while len(bstack111111111_opy_) > size:
    bstack1l1ll11l111_opy_ = bstack111111111_opy_[:size]
    bstack1l1l11ll11l_opy_.append(bstack1l1ll11l111_opy_)
    bstack111111111_opy_ = bstack111111111_opy_[size:]
  bstack1l1l11ll11l_opy_.append(bstack111111111_opy_)
  return bstack1l1l11ll11l_opy_
def bstack111l1lllll_opy_(args):
  if bstack1l1llll_opy_ (u"ࠪ࠱ࡲ࠭ᒡ") in args and bstack1l1llll_opy_ (u"ࠫࡵࡪࡢࠨᒢ") in args:
    return True
  return False
def bstack11llllll1l_opy_(args):
  if not isinstance(args, (list, tuple)) or bstack1l1llll_opy_ (u"ࠬ࠳࡭ࠨᒣ") not in args or bstack111l1lllll_opy_(args):
    return False
  idx = args.index(bstack1l1llll_opy_ (u"࠭࠭࡮ࠩᒤ"))
  return all(str(tok).startswith(bstack1l1llll_opy_ (u"ࠧ࠮ࠩᒥ")) for tok in args[:idx])
def bstack1l1ll11l11l_opy_(args):
  import runpy
  idx = args.index(bstack1l1llll_opy_ (u"ࠨ࠯ࡰࠫᒦ"))
  if idx + 1 >= len(args):
    logger.error(bstack1l1llll_opy_ (u"ࠩࡑࡳࠥࡳ࡯ࡥࡷ࡯ࡩࠥࡴࡡ࡮ࡧࠣ࡫࡮ࡼࡥ࡯ࠢࡤࡪࡹ࡫ࡲࠡ࠯ࡰ࠲࡛ࠥࡳࡢࡩࡨ࠾ࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡸࡪ࡫ࠡࡲࡼࡸ࡭ࡵ࡮ࠡ࠯ࡰࠤࡁࡳ࡯ࡥࡷ࡯ࡩࡃ࡛ࠦࡢࡴࡪࡷࡢ࠭ᒧ"))
    return
  module_name = args[idx + 1]
  bstack11ll11l111_opy_ = list(args[idx + 2:])
  if sys.path[:1] != [bstack1l1llll_opy_ (u"ࠪࠫᒨ")]:
    sys.path.insert(0, bstack1l1llll_opy_ (u"ࠫࠬᒩ"))
  sys.argv = [module_name] + bstack11ll11l111_opy_
  runpy.run_module(module_name, None, bstack1l1llll_opy_ (u"ࠬࡥ࡟࡮ࡣ࡬ࡲࡤࡥࠧᒪ"), True)
@measure(event_name=EVENTS.bstack1111l1l1l_opy_, stage=STAGE.bstack1l11ll1l1l_opy_)
def run_on_browserstack(bstack1l1l1l1ll1l_opy_=None, bstack111111111l_opy_=None, bstack1ll1l1lll11_opy_=False):
  global CONFIG
  global bstack1lll1ll1l11_opy_
  global bstack11ll111lll_opy_
  global bstack1lll11l111l_opy_
  global global_config
  bstack11l11l1ll1_opy_ = bstack1l1llll_opy_ (u"࠭ࠧᒫ")
  bstack1l1ll1ll1ll_opy_ = bstack1l1llll_opy_ (u"ࠢࠣᒬ")
  bstack11llll11l1_opy_(bstack11l11lllll_opy_, logger)
  if bstack1l1l1l1ll1l_opy_ and isinstance(bstack1l1l1l1ll1l_opy_, str):
    bstack1l1l1l1ll1l_opy_ = eval(bstack1l1l1l1ll1l_opy_)
  if bstack1l1l1l1ll1l_opy_:
    CONFIG = bstack1l1l1l1ll1l_opy_[bstack1l1llll_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨᒭ")]
    bstack1lll1ll1l11_opy_ = bstack1l1l1l1ll1l_opy_[bstack1l1llll_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪᒮ")]
    bstack11ll111lll_opy_ = bstack1l1l1l1ll1l_opy_[bstack1l1llll_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬᒯ")]
    global_config.bstack1ll11l111l_opy_(bstack1l1llll_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ᒰ"), bstack11ll111lll_opy_)
    bstack11l11l1ll1_opy_ = bstack1l1llll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨ࠭ᒱ")
  global_config.bstack1ll11l111l_opy_(bstack1l1llll_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨᒲ"), uuid4().__str__())
  os.environ[BROWSERSTACK_SDK_RUN_ID_ENV] = global_config.get_property(bstack1l1llll_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥࠩᒳ"))
  logger.info(bstack1l1llll_opy_ (u"ࠨࡕࡇࡏࠥࡸࡵ࡯ࠢࡶࡸࡦࡸࡴࡦࡦࠣࡻ࡮ࡺࡨࠡ࡫ࡧ࠾ࠥ࠭ᒴ") + global_config.get_property(bstack1l1llll_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫᒵ")));
  logger.debug(bstack1l1llll_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࡂ࠭ᒶ") + global_config.get_property(bstack1l1llll_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭ᒷ")))
  if not bstack1ll1l1lll11_opy_:
    try:
      for _1lll1l1ll1_opy_ in bstack1111lll1l_opy_:
        logger.info(_1lll1l1ll1_opy_)
    except Exception:
      pass
    if len(sys.argv) <= 1:
      logger.critical(bstack1l1l1ll11l1_opy_)
      return
    if sys.argv[1] == bstack1l1llll_opy_ (u"ࠬ࠳࠭ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᒸ") or sys.argv[1] == bstack1l1llll_opy_ (u"࠭࠭ࡷࠩᒹ"):
      logger.info(bstack1l1llll_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡐࡺࡶ࡫ࡳࡳࠦࡓࡅࡍࠣࡺࢀࢃࠧᒺ").format(__version__))
      return
    if sys.argv[1] == bstack1l1llll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᒻ"):
      bstack1l1l1l1l11l_opy_()
      return
    if sys.argv[1] == bstack1l1llll_opy_ (u"ࠩ࡯ࡳࡦࡪࠧᒼ"):
      from browserstack_sdk.bstack1l11l1lll_opy_ import bstack1l11l1l11_opy_
      bstack1ll1l11l1l1_opy_()
      bstack1l11l1l11_opy_(CONFIG)
      return
  args = sys.argv
  bstack1ll1l11l1l1_opy_()
  global bstack1l11l11l11_opy_
  try:
    from bstack_utils import constants as bstack1ll1ll1l111_opy_
    override_value = CONFIG.get(bstack1l1llll_opy_ (u"ࠪࡳࡻ࡫ࡲࡳ࡫ࡧࡩࡑࡵࡡࡥࡖࡨࡷࡹ࡯࡮ࡨࠩᒽ"), False)
    bstack1l11l11l11_opy_ = bool(override_value)
    os.environ[bstack1l1llll_opy_ (u"ࠫࡔ࡜ࡅࡓࡔࡌࡈࡊࡥࡌࡐࡃࡇࡣ࡙ࡋࡓࡕࡋࡑࡋࠬᒾ")] = str(bstack1l11l11l11_opy_).lower()
    global_config.bstack1ll11l111l_opy_(bstack1l1llll_opy_ (u"ࠬࡵࡶࡦࡴࡵ࡭ࡩ࡫࡟࡭ࡱࡤࡨࡤࡺࡥࡴࡶ࡬ࡲ࡬࠭ᒿ"), bstack1l11l11l11_opy_)
  except Exception as e:
    logger.error(bstack1l1llll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩ࠲ࡴࡷࡵࡰࡢࡩࡤࡸ࡮ࡴࡧࠡࡑ࡙ࡉࡗࡘࡉࡅࡇࡢࡐࡔࡇࡄࡠࡖࡈࡗ࡙ࡏࡎࡈ࠼ࠣࡿࢂࠨᓀ").format(e))
    bstack1l11l11l11_opy_ = False
    try:
      os.environ[bstack1l1llll_opy_ (u"ࠧࡐࡘࡈࡖࡗࡏࡄࡆࡡࡏࡓࡆࡊ࡟ࡕࡇࡖࡘࡎࡔࡇࠨᓁ")] = bstack1l1llll_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧᓂ")
    except Exception:
      pass
  if bstack1l11l11l11_opy_:
    try:
      from bstack_utils.bstack1ll1l111lll_opy_ import apply as _1lll1l1111_opy_
      _1lll1l1111_opy_()
    except Exception as e:
      logger.error(bstack1l1llll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡧࡰࡱ࡮ࡼ࡭ࡳ࡭ࠠࡶࡰ࡬ࡸࡹ࡫ࡳࡵࠢࡏࡘࡘࠦࡰࡢࡶࡦ࡬࠿ࠦࡻࡾࠤᓃ").format(e))
    try:
      from bstack_utils.bstack11l11lll1l_opy_ import apply as _1lllll11lll_opy_
      _1lllll11lll_opy_()
    except Exception as e:
      logger.error(bstack1l1llll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡡࡱࡲ࡯ࡽ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯࠯࡯࡭࡫࡫ࡣࡺࡥ࡯ࡩࠥࡒࡔࡔࠢࡳࡥࡹࡩࡨ࠻ࠢࡾࢁࠧᓄ").format(e))
  if bstack1l11l11l11_opy_:
    bstack1ll1l1ll1l1_opy_ = CONFIG.get(bstack1l1llll_opy_ (u"ࠫࡱࡵࡡࡥࡖࡨࡷࡹ࡯࡮ࡨࡊࡸࡦ࡚ࡘࡌࠨᓅ")) or bstack1ll1ll1l111_opy_.bstack1111l11ll_opy_
    logger.info(bstack1l1llll_opy_ (u"ࠧࡍ࡬ࡰࡤࡤࡰࠥࡵࡶࡦࡴࡵ࡭ࡩ࡫࡬ࡰࡣࡧࡸࡪࡹࡴࡪࡰࡪࠤࡪࡴࡡࡣ࡮ࡨࡨ࠱ࠦࡵࡴ࡫ࡱ࡫ࠥ࡮ࡵࡣ࠼ࠣࡿࢂࠨᓆ").format(bstack1ll1l1ll1l1_opy_))
    bstack1lll1ll1l11_opy_ = bstack1ll1l1ll1l1_opy_
    try:
      bstack1ll1ll1l111_opy_.bstack1ll1111ll_opy_ = bstack1ll1l1ll1l1_opy_
      bstack1ll1ll1l111_opy_.bstack1lll1111ll1_opy_ = bstack1ll1l1ll1l1_opy_
    except Exception:
      pass
  global bstack1l1lll1lll_opy_
  global bstack1111111l1_opy_
  global PARALLELISE_VANILLA_PYTHON
  global PARALLELISE_THREADING_PYTHON
  global PLATFORM_INDEX
  global bstack1ll1ll111ll_opy_
  global bstack1l1ll1lll1l_opy_
  global bstack1llllll11ll_opy_
  global bstack1lll1llll1_opy_
  global bstack1ll11l1lll_opy_
  global bstack1111l1l111_opy_
  bstack1111111l1_opy_ = len(CONFIG.get(bstack1l1llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᓇ"), []))
  if not bstack11l11l1ll1_opy_:
    if args[1] == bstack1l1llll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧᓈ") or args[1] == bstack1l1llll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩᓉ") or args[1] == bstack1l1llll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠪᓊ"):
      bstack11l11l1ll1_opy_ = bstack1l1llll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠫᓋ")
      args = args[2:]
    elif args[1] == bstack1l1llll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪᓌ"):
      bstack11l11l1ll1_opy_ = bstack1l1llll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫᓍ")
      args = args[2:]
    elif args[1] == bstack1l1llll_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬᓎ"):
      bstack11l11l1ll1_opy_ = bstack1l1llll_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ᓏ")
      args = args[2:]
    elif args[1] == bstack1l1llll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩᓐ"):
      bstack11l11l1ll1_opy_ = bstack1l1llll_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪᓑ")
      args = args[2:]
    elif args[1] == bstack1l1llll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᓒ"):
      bstack11l11l1ll1_opy_ = bstack1l1llll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᓓ")
      args = args[2:]
    elif args[1] == bstack1l1llll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬᓔ"):
      bstack11l11l1ll1_opy_ = bstack1l1llll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ᓕ")
      args = args[2:]
    else:
      if not bstack1l1llll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᓖ") in CONFIG or str(CONFIG[bstack1l1llll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᓗ")]).lower() in [bstack1l1llll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩᓘ"), bstack1l1llll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫᓙ"), bstack1l1llll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠬᓚ")]:
        bstack11l11l1ll1_opy_ = bstack1l1llll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨ࠭ᓛ")
        args = args[1:]
      elif str(CONFIG[bstack1l1llll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᓜ")]).lower() == bstack1l1llll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ᓝ"):
        bstack11l11l1ll1_opy_ = bstack1l1llll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧᓞ")
        args = args[1:]
      elif str(CONFIG[bstack1l1llll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᓟ")]).lower() == bstack1l1llll_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩᓠ"):
        bstack11l11l1ll1_opy_ = bstack1l1llll_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪᓡ")
        args = args[1:]
      elif str(CONFIG[bstack1l1llll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᓢ")]).lower() == bstack1l1llll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᓣ"):
        bstack11l11l1ll1_opy_ = bstack1l1llll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᓤ")
        args = args[1:]
      elif str(CONFIG[bstack1l1llll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᓥ")]).lower() == bstack1l1llll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩᓦ"):
        bstack11l11l1ll1_opy_ = bstack1l1llll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪᓧ")
        args = args[1:]
      else:
        bstack1lll111lll_opy_(bstack1ll1l1lllll_opy_)
  os.environ[bstack1l1llll_opy_ (u"ࠫࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ࡟ࡖࡕࡈࡈࠬᓨ")] = bstack11l11l1ll1_opy_
  bstack1lll11l111l_opy_ = bstack11l11l1ll1_opy_
  if bstack11l11l1ll1_opy_:
    os.environ[bstack1lll1l11111_opy_] = bstack11l11l1ll1_opy_
  _1lllll1111l_opy_(CONFIG)
  if bstack11l11l1ll1_opy_ in [bstack1l1llll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫᓩ"), bstack1l1llll_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬᓪ")]:
    try:
      bstack111lll1ll1_opy_ = CONFIG.get(bstack1l1llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᓫ"), [])
      bstack1ll11ll1l1l_opy_ = CONFIG.get(bstack1l1llll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᓬ"), False)
      logger.debug(
        bstack1l1llll_opy_ (u"ࠤࡤ࠵࠶ࡿࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡳࡶࡪ࠳ࡶࡢ࡮࡬ࡨࡦࡺࡩࡰࡰ࠽ࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠽ࠣᓭ") + bstack11l11l1ll1_opy_
        + bstack1l1llll_opy_ (u"ࠥ࠰ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࡳ࠾ࠤᓮ") + str(len(bstack111lll1ll1_opy_))
      )
      for bstack1ll1l111l1_opy_, bstack1lll1l1l111_opy_ in enumerate(bstack111lll1ll1_opy_):
        if isinstance(bstack1lll1l1l111_opy_, dict) and bstack1l1llll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᓯ") in bstack1lll1l1l111_opy_:
          bstack1l1l1l11111_opy_ = bstack1lll1l1l111_opy_[bstack1l1llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᓰ")]
        else:
          bstack1l1l1l11111_opy_ = bstack1ll11ll1l1l_opy_
        if bstack1l1l1l11111_opy_:
          a11y.is_platform_supported(get_caps(CONFIG, bstack1ll1l111l1_opy_), options=None, config=CONFIG)
    except Exception as bstack1l1ll1111ll_opy_:
      logger.debug(bstack1l1llll_opy_ (u"ࠨࡡ࠲࠳ࡼࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡰࡳࡧ࠰ࡺࡦࡲࡩࡥࡣࡷ࡭ࡴࡴࠠࡴ࡭࡬ࡴࡵ࡫ࡤ࠻ࠢࠥᓱ") + str(bstack1l1ll1111ll_opy_))
  if cli.is_enabled(CONFIG):
    bstack1ll1111llll_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡔࡇࡖࡗࡎࡕࡎࡠࡋࡇࠫᓲ"), bstack1l1llll_opy_ (u"ࠨࠩᓳ")) != bstack1l1llll_opy_ (u"ࠩࠪᓴ")
    _1l11111ll1_opy_ = None
    _1ll11l11111_opy_ = None
    _1l1ll1l11l1_opy_, _1l11111ll1_opy_, _1ll11l11111_opy_ = _1ll11l11l1l_opy_(CONFIG)
    if _1l1ll1l11l1_opy_ == bstack1l1llll_opy_ (u"ࠪࡪࡴࡲ࡬ࡰࡹࡨࡶࠬᓵ"):
      bstack1ll1111llll_opy_ = True
    if bstack1ll1111llll_opy_:
        try:
          bstack111ll1l11_opy_.invoke(Events.CONNECT, bstack111ll11ll_opy_())
        except Exception as e:
          bstack111ll1l11_opy_.invoke(Events.bstack1lllll1l11l_opy_, e.__traceback__, 1)
    else:
        try:
          if bstack11l11l1ll1_opy_ == bstack1l1llll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᓶ") and bstack1llll1l11l1_opy_():
            bstack1l1ll111ll1_opy_ = bstack1ll11lll1ll_opy_[bstack1l1llll_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘ࠲ࡈࡄࡅࠩᓷ")]
          elif bstack11l11l1ll1_opy_ in [bstack1l1llll_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧᓸ"), bstack1l1llll_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ᓹ")]:
            bstack1l1ll111ll1_opy_ = bstack1l1llll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧᓺ")
          else:
            bstack1l1ll111ll1_opy_ = bstack11l11l1ll1_opy_
          bstack111ll1l11_opy_.invoke(Events.bstack1llll1lll1_opy_, bstack1lll1ll1l1_opy_(
        sdk_version=__version__,
        path_config=bstack1111111lll_opy_(),
        path_project=os.getcwd(),
        test_framework=bstack1l1ll111ll1_opy_,
        frameworks=[bstack1l1ll111ll1_opy_],
        framework_versions={
          bstack1l1ll111ll1_opy_: bstack1l1l1l1l111_opy_(bstack1l1llll_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨᓻ") if bstack11l11l1ll1_opy_ in [bstack1l1llll_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩᓼ"), bstack1l1llll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪᓽ"), bstack1l1llll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ᓾ")] else bstack11l11l1ll1_opy_)
        },
        bs_config=CONFIG
      ))
          if cli.config and cli.config.get(bstack1l1llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣᓿ"), None):
            CONFIG[bstack1l1llll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤᔀ")] = cli.config.get(bstack1l1llll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠥᔁ"), None)
        except Exception as e:
          bstack111ll1l11_opy_.invoke(Events.bstack1lllll1l11l_opy_, e.__traceback__, 1)
        finally:
          _1lll1lll1l1_opy_(_1l11111ll1_opy_, _1ll11l11111_opy_, CONFIG)
    if bstack11ll111lll_opy_:
      CONFIG[bstack1l1llll_opy_ (u"ࠤࡤࡴࡵࠨᔂ")] = cli.config[bstack1l1llll_opy_ (u"ࠥࡥࡵࡶࠢᔃ")]
      logger.info(bstack1l1l1lll1l_opy_.format(CONFIG[bstack1l1llll_opy_ (u"ࠫࡦࡶࡰࠨᔄ")]))
  else:
    bstack111ll1l11_opy_.clear()
  global bstack111l111l11_opy_
  global bstack11l1111lll_opy_
  if bstack1l1l1l1ll1l_opy_:
    try:
      time_start = datetime.datetime.now()
      os.environ[bstack1lll1l11111_opy_] = bstack11l11l1ll1_opy_
      bstack11l1l1llll_opy_ = PerformanceTester.mark_start(EVENTS.bstack1l111llll1_opy_)
      try:
        logger.info(bstack1l1llll_opy_ (u"࡙ࠧࡥ࡯ࡦ࡬ࡲ࡬ࠦࡓࡅࡍࠣࡘࡪࡹࡴࠡࡃࡷࡸࡪࡳࡰࡵࡧࡧࠤࡪࡼࡥ࡯ࡶࠥᔅ"))
        bstack1l1l111l1l1_opy_(bstack11ll1llll1_opy_, CONFIG)
      finally:
        PerformanceTester.end(EVENTS.bstack1l111llll1_opy_.value, bstack11l1l1llll_opy_ + bstack1l1llll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᔆ"), bstack11l1l1llll_opy_ + bstack1l1llll_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᔇ"), status=True, failure=None, test_name=None)
      cli.add_benchmark(bstack1l1llll_opy_ (u"ࠣࡪࡷࡸࡵࡀࡳࡥ࡭ࡢࡸࡪࡹࡴࡠࡣࡷࡸࡪࡳࡰࡵࡧࡧࠦᔈ"), datetime.datetime.now() - time_start)
    except Exception as e:
      logger.debug(bstack11l1llll1l_opy_.format(str(e)))
  global bstack1l1l1l111l1_opy_
  global bstack1lllll11111_opy_
  global bstack111l1l111l_opy_
  global bstack1l1ll1ll11l_opy_
  global bstack1111llll11_opy_
  global bstack1111lll1l1_opy_
  global bstack1111l1l1l1_opy_
  global bstack11l1l1l1l1_opy_
  global bstack1ll1l11ll1_opy_
  global bstack111lll1l11_opy_
  global bstack1llllll111l_opy_
  global bstack11l11ll1ll_opy_
  global bstack111ll1l1l1_opy_
  global bstack1l1l111l1ll_opy_
  global bstack1l1l1ll1lll_opy_
  global bstack11l1111111_opy_
  global bstack11l1l11l1l_opy_
  global bstack1l111l1ll1_opy_
  global bstack111l1lll11_opy_
  global bstack1ll111llll_opy_
  global bstack1llllll1lll_opy_
  global bstack1l1l111l11l_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l1l1l111l1_opy_ = webdriver.Remote.__init__
    bstack1lllll11111_opy_ = WebDriver.quit
    bstack11l11ll1ll_opy_ = WebDriver.close
    bstack11l1111111_opy_ = WebDriver.get
    bstack1l1l111l11l_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack111l111l11_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack1l1l11l1l1l_opy_
    bstack11l1111lll_opy_ = bstack1l1l11l1l1l_opy_()
  except Exception as e:
    pass
  try:
    global bstack1lll1ll11ll_opy_
    from QWeb.keywords import browser
    bstack1lll1ll11ll_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack11ll1l1ll1_opy_(CONFIG) and bstack1l1111l1ll_opy_():
    if bstack1l1ll11111_opy_() < version.parse(bstack1l1l1ll1l11_opy_):
      logger.error(bstack1ll1ll1l1l_opy_.format(bstack1l1ll11111_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack1l1llll_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪᔉ")) and callable(getattr(RemoteConnection, bstack1l1llll_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫᔊ"))):
          RemoteConnection._get_proxy_url = bstack1ll1ll1lll1_opy_
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          ClientConfig.get_proxy_url = bstack1ll1ll1lll1_opy_
      except Exception as e:
        logger.error(bstack1ll1l1l1l1_opy_.format(str(e)))
  if not CONFIG.get(bstack1l1llll_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭ᔋ"), False) and not bstack1l1l1l1ll1l_opy_:
    logger.info(bstack111111ll11_opy_)
  bstack1lll11111l_opy_ = not cli.is_enabled(CONFIG) and bstack11l11l1ll1_opy_ not in [bstack1l1llll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ᔌ")]
  bstack1ll1lll1ll_opy_ = bstack1lll11111l_opy_ and bstack1l1llll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪᔍ") in CONFIG and str(CONFIG[bstack1l1llll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫᔎ")]).lower() != bstack1l1llll_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧᔏ")
  bstack11l1ll1lll_opy_ = bstack1lll11111l_opy_ and not bstack1ll1lll1ll_opy_ and (bstack11l11l1ll1_opy_ != bstack1l1llll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠪᔐ") or (bstack11l11l1ll1_opy_ == bstack1l1llll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠫᔑ") and not bstack1l1l1l1ll1l_opy_))
  if bstack11l11l1ll1_opy_ not in [bstack1l1llll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬᔒ")]:
    bstack11llll11l1_opy_(os.path.join(os.getcwd(), bstack1l1llll_opy_ (u"ࠬࡲ࡯ࡨࠩᔓ"), bstack1l1llll_opy_ (u"࠭࡫ࡦࡻ࠰ࡱࡪࡺࡲࡪࡥࡶ࠲࡯ࡹ࡯࡯ࠩᔔ")), logger)
  if (bstack11l11l1ll1_opy_ in [bstack1l1llll_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ᔕ"), bstack1l1llll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧᔖ"), bstack1l1llll_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪᔗ")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      try:
        from pabot.pabot import QueueItem
        from pabot import pabot
      except Exception as e:
        logger.warning(bstack1l1l11lll11_opy_ + str(e))
      if not is_robot_playwright_installed():
        try:
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
          from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
          WebDriverCreator._get_ff_profile = bstack1l1ll1lll1_opy_
          bstack1111lll1l1_opy_ = WebDriverCache.close
        except Exception as e:
          logger.warning(bstack1lll11l1ll_opy_ + str(e))
        try:
          from AppiumLibrary.utils.applicationcache import ApplicationCache
          bstack1111llll11_opy_ = ApplicationCache.close
        except Exception as e:
          logger.debug(bstack11l11l11ll_opy_ + str(e))
    except Exception as e:
      bstack1ll1l1lll1_opy_(e, bstack1lll11l1ll_opy_)
    if bstack11l11l1ll1_opy_ != bstack1l1llll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫᔘ"):
      bstack111ll1llll_opy_()
    bstack111l1l111l_opy_ = Output.start_test
    bstack1l1ll1ll11l_opy_ = Output.end_test
    bstack1111l1l1l1_opy_ = TestStatus.__init__
    bstack1ll1l11ll1_opy_ = pabot._run
    bstack111lll1l11_opy_ = QueueItem.__init__
    bstack1llllll111l_opy_ = pabot._create_command_for_execution
    bstack1ll111llll_opy_ = pabot._report_results
  if bstack11l11l1ll1_opy_ == bstack1l1llll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫᔙ"):
    global bstack1l1ll1ll1l1_opy_
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll1l1lll1_opy_(e, bstack1l111lllll_opy_)
    bstack111ll1l1l1_opy_ = Runner.run_hook
    bstack1l1l111l1ll_opy_ = Runner.load_hooks
    bstack1l1l1ll1lll_opy_ = Step.run
    try:
      sig = inspect.signature(bstack111ll1l1l1_opy_)
      params = list(sig.parameters.keys())
      bstack1l1ll1ll1l1_opy_ = bstack1l1llll_opy_ (u"ࠬࡩ࡯࡯ࡶࡨࡼࡹ࠭ᔚ") in params
      logger.info(bstack1l1llll_opy_ (u"࠭ࡄࡦࡶࡨࡧࡹ࡫ࡤࠡࡤࡨ࡬ࡦࡼࡥࠡࡴࡸࡲࡤ࡮࡯ࡰ࡭ࠣࡷ࡮࡭࡮ࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪᔛ").format(bstack1l1llll_opy_ (u"ࠧ࠲࠰࠵࠲࠻ࠦࠨࡸ࡫ࡷ࡬ࠥࡩ࡯࡯ࡶࡨࡼࡹ࠯ࠧᔜ") if bstack1l1ll1ll1l1_opy_ else bstack1l1llll_opy_ (u"ࠨ࠳࠱࠷࠰ࠦࠨࡸ࡫ࡷ࡬ࡴࡻࡴࠡࡥࡲࡲࡹ࡫ࡸࡵࠫࠪᔝ")))
    except Exception as e:
      logger.debug(bstack1l1llll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡦࡸࠥࡨࡥࡩࡣࡹࡩࠥࡸࡵ࡯ࡡ࡫ࡳࡴࡱࠠࡴ࡫ࡪࡲࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧᔞ").format(str(e)))
      bstack1l1ll1ll1l1_opy_ = None
  if bstack11l11l1ll1_opy_ == bstack1l1llll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᔟ"):
    try:
      from _pytest.config import Config
      bstack1l111l1ll1_opy_ = Config.getoption
      from _pytest import runner
      bstack111l1lll11_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warning(bstack1l1llll_opy_ (u"ࠦࠪࡹ࠺ࠡࠧࡶࠦᔠ"), bstack11llllll1_opy_, str(e))
    try:
      from pytest_bdd import reporting
      bstack1llllll1lll_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1l1llll_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡴࠦࡲࡶࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࡸ࠭ᔡ"))
    if bstack111l1l1ll1_opy_():
      logger.warning(bstack1l1ll1111l1_opy_[bstack1l1llll_opy_ (u"࠭ࡓࡅࡍ࠰ࡋࡊࡔ࠭࠱࠲࠸ࠫᔢ")])
  try:
    framework_name = bstack1l1llll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ᔣ") if bstack11l11l1ll1_opy_ in [bstack1l1llll_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧᔤ"), bstack1l1llll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨᔥ"), bstack1l1llll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫᔦ")] else bstack11l1l111l1_opy_(bstack11l11l1ll1_opy_)
    bstack1111l11l1_opy_ = {
      bstack1l1llll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࠬᔧ"): bstack1l1llll_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧᔨ") if bstack11l11l1ll1_opy_ == bstack1l1llll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᔩ") and bstack1llll1l11l1_opy_() else framework_name,
      bstack1l1llll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫᔪ"): bstack1l1l1l1l111_opy_(framework_name),
      bstack1l1llll_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᔫ"): __version__,
      bstack1l1llll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦࠪᔬ"): bstack11l11l1ll1_opy_
    }
    if bstack11l11l1ll1_opy_ in bstack1llllll1ll_opy_ + bstack1lll11ll1l1_opy_:
      if a11y.is_enabled_root(CONFIG):
        if bstack1l1llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᔭ") in CONFIG:
          os.environ[bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᔮ")] = os.getenv(bstack1l1llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᔯ"), json.dumps(CONFIG[bstack1l1llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᔰ")]))
          CONFIG[bstack1l1llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᔱ")].pop(bstack1l1llll_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᔲ"), None)
          CONFIG[bstack1l1llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᔳ")].pop(bstack1l1llll_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᔴ"), None)
        bstack1l1l1llll11_opy_ = bstack1l1llll_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᔵ") if CONFIG.get(bstack1l1llll_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᔶ")) or bstack1ll1lll11l_opy_() else bstack1l1llll_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨᔷ")
        if bstack1l1l1llll11_opy_ == bstack1l1llll_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᔸ"):
          try:
            import importlib.metadata as _1ll111ll11_opy_
            bstack1lll1lll11l_opy_ = _1ll111ll11_opy_.version(bstack1l1llll_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᔹ"))
          except Exception:
            bstack1lll1lll11l_opy_ = bstack1l1llll_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࠪᔺ")
        else:
          bstack1lll1lll11l_opy_ = str(bstack1l1ll11111_opy_())
        bstack1111l11l1_opy_[bstack1l1llll_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᔻ")] = {
          bstack1l1llll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᔼ"): bstack1l1l1llll11_opy_,
          bstack1l1llll_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭ᔽ"): bstack1lll1lll11l_opy_
        }
    bstack11l1lllll1_opy_, bstack1ll11l11l1_opy_ = None, {}
    bstack1l1lllll111_opy_ = None
    bstack1lll1l1ll1l_opy_ = None
    def bstack1llll1l1l1l_opy_():
      if bstack1ll1lll1ll_opy_:
        bstack1ll1l111ll1_opy_()
      elif bstack11l1ll1lll_opy_:
        bstack11111111l_opy_()
    def bstack1l1l1l111l_opy_():
      nonlocal bstack11l1lllll1_opy_, bstack1ll11l11l1_opy_
      bstack11111l11l_opy_ = (
        bstack1l11l11l11_opy_ and bstack11l11l1ll1_opy_ not in [bstack1l1llll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᔾ"), bstack1l1llll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫᔿ")]
      )
      if bstack11l11l1ll1_opy_ not in [bstack1l1llll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩᕀ")] and (not cli.is_running() or bstack11111l11l_opy_):
        bstack11l1lllll1_opy_, bstack1ll11l11l1_opy_ = TestHubHandler.launch(CONFIG, bstack1111l11l1_opy_)
    if bstack1ll1lll1ll_opy_ or bstack11l1ll1lll_opy_:
      bstack1l1lllll111_opy_ = threading.Thread(target=bstack1llll1l1l1l_opy_)
      bstack1l1lllll111_opy_.start()
    bstack11111l11l_opy_ = (
      bstack1l11l11l11_opy_ and bstack11l11l1ll1_opy_ not in [bstack1l1llll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᕁ"), bstack1l1llll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧᕂ")]
    )
    if bstack11l11l1ll1_opy_ not in [bstack1l1llll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬᕃ")] and (not cli.is_running() or bstack11111l11l_opy_):
      bstack1lll1l1ll1l_opy_ = threading.Thread(target=bstack1l1l1l111l_opy_)
      bstack1lll1l1ll1l_opy_.start()
    if bstack1l1lllll111_opy_:
      bstack1l1lllll111_opy_.join()
    if bstack1lll1l1ll1l_opy_:
      bstack1lll1l1ll1l_opy_.join()
    if bstack1ll11l11l1_opy_.get(bstack1l1llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᕄ")) is not None and a11y.bstack1l11lll111_opy_(CONFIG) is None:
      value = bstack1ll11l11l1_opy_[bstack1l1llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᕅ")].get(bstack1l1llll_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨᕆ"))
      if value is not None:
          CONFIG[bstack1l1llll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᕇ")] = value
      else:
        logger.debug(bstack1l1llll_opy_ (u"ࠤࡑࡳࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡪࡡࡵࡣࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠢᕈ"))
  except Exception as e:
    logger.debug(bstack111ll1111l_opy_.format(bstack1l1llll_opy_ (u"ࠪࡘࡪࡹࡴࡉࡷࡥࠫᕉ"), str(e)))
  if bstack11l11l1ll1_opy_ == bstack1l1llll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠬᕊ"):
    PARALLELISE_VANILLA_PYTHON = True
    if bstack1l1l1l1ll1l_opy_ and bstack1ll1l1lll11_opy_:
      if cli.is_enabled(CONFIG):
        bstack1ll1ll111ll_opy_ = cli.config.get(bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩᕋ"), {}).get(bstack1l1llll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᕌ")) if cli.config else None
      else:
        bstack1ll1ll111ll_opy_ = CONFIG.get(bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫᕍ"), {}).get(bstack1l1llll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᕎ"))
      bstack1ll11111l11_opy_(bstack1l11l11lll_opy_)
    elif bstack1l1l1l1ll1l_opy_:
      if cli.is_enabled(CONFIG):
        bstack1ll1ll111ll_opy_ = cli.config.get(bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ᕏ"), {}).get(bstack1l1llll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᕐ")) if cli.config else None
      else:
        bstack1ll1ll111ll_opy_ = CONFIG.get(bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨᕑ"), {}).get(bstack1l1llll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᕒ"))
      global bstack1111ll11l_opy_
      try:
        if bstack111l1lllll_opy_(bstack1l1l1l1ll1l_opy_[bstack1l1llll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩᕓ")]) and multiprocessing.current_process().name == bstack1l1llll_opy_ (u"ࠧ࠱ࠩᕔ"):
          bstack1l1l1l1ll1l_opy_[bstack1l1llll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫᕕ")].remove(bstack1l1llll_opy_ (u"ࠩ࠰ࡱࠬᕖ"))
          bstack1l1l1l1ll1l_opy_[bstack1l1llll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ᕗ")].remove(bstack1l1llll_opy_ (u"ࠫࡵࡪࡢࠨᕘ"))
          bstack1l1l1l1ll1l_opy_[bstack1l1llll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨᕙ")] = bstack1l1l1l1ll1l_opy_[bstack1l1llll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩᕚ")][0]
          with open(bstack1l1l1l1ll1l_opy_[bstack1l1llll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪᕛ")], bstack1l1llll_opy_ (u"ࠨࡴࠪᕜ")) as f:
            file_content = f.read()
          bstack111l11ll11_opy_ = bstack1l1llll_opy_ (u"ࠤࠥࠦ࡫ࡸ࡯࡮ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡵࡧ࡯ࠥ࡯࡭ࡱࡱࡵࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥ࠼ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩ࠭ࢁࡽࠪ࠽ࠣࡪࡷࡵ࡭ࠡࡲࡧࡦࠥ࡯࡭ࡱࡱࡵࡸࠥࡖࡤࡣ࠽ࠣࡳ࡬ࡥࡤࡣࠢࡀࠤࡕࡪࡢ࠯ࡦࡲࡣࡧࡸࡥࡢ࡭࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡥࡧࡩࠤࡲࡵࡤࡠࡤࡵࡩࡦࡱࠨࡴࡧ࡯ࡪ࠱ࠦࡡࡳࡩ࠯ࠤࡹ࡫࡭ࡱࡱࡵࡥࡷࡿࠠ࠾ࠢ࠳࠭࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡹࡸࡹ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡤࡶ࡬ࠦ࠽ࠡࡵࡷࡶ࠭࡯࡮ࡵࠪࡤࡶ࡬࠯ࠫ࠲࠲ࠬࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡨࡼࡨ࡫ࡰࡵࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡧࡳࠡࡧ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡵࡧࡳࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡰࡩࡢࡨࡧ࠮ࡳࡦ࡮ࡩ࠰ࡦࡸࡧ࠭ࡶࡨࡱࡵࡵࡲࡢࡴࡼ࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡒࡧࡦ࠳ࡪ࡯ࡠࡤࠣࡁࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡕࡪࡢ࠯ࡦࡲࡣࡧࡸࡥࡢ࡭ࠣࡁࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡕࡪࡢࠩࠫ࠱ࡷࡪࡺ࡟ࡵࡴࡤࡧࡪ࠮ࠩ࡝ࡰࠥࠦࠧᕝ").format(str(bstack1l1l1l1ll1l_opy_))
          bstack1llllllll1_opy_ = bstack111l11ll11_opy_ + file_content
          bstack1l1ll1l111l_opy_ = bstack1l1l1l1ll1l_opy_[bstack1l1llll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ᕞ")] + bstack1l1llll_opy_ (u"ࠫࡤࡨࡳࡵࡣࡦ࡯ࡤࡺࡥ࡮ࡲ࠱ࡴࡾ࠭ᕟ")
          with open(bstack1l1ll1l111l_opy_, bstack1l1llll_opy_ (u"ࠬࡽࠧᕠ")):
            pass
          with open(bstack1l1ll1l111l_opy_, bstack1l1llll_opy_ (u"ࠨࡷࠬࠤᕡ")) as f:
            f.write(bstack1llllllll1_opy_)
          import subprocess
          bstack111ll11ll1_opy_ = subprocess.run([bstack1l1llll_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢᕢ"), bstack1l1ll1l111l_opy_])
          if os.path.exists(bstack1l1ll1l111l_opy_):
            os.unlink(bstack1l1ll1l111l_opy_)
          os._exit(bstack111ll11ll1_opy_.returncode)
        else:
          if bstack111l1lllll_opy_(bstack1l1l1l1ll1l_opy_[bstack1l1llll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫᕣ")]):
            bstack1l1l1l1ll1l_opy_[bstack1l1llll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬᕤ")].remove(bstack1l1llll_opy_ (u"ࠪ࠱ࡲ࠭ᕥ"))
            bstack1l1l1l1ll1l_opy_[bstack1l1llll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧᕦ")].remove(bstack1l1llll_opy_ (u"ࠬࡶࡤࡣࠩᕧ"))
            bstack1l1l1l1ll1l_opy_[bstack1l1llll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩᕨ")] = bstack1l1l1l1ll1l_opy_[bstack1l1llll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪᕩ")][0]
          if bstack11llllll1l_opy_(bstack1l1l1l1ll1l_opy_[bstack1l1llll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫᕪ")]):
            bstack1ll11111l11_opy_(bstack1l11l11lll_opy_)
            bstack1l1ll11l11l_opy_(bstack1l1l1l1ll1l_opy_[bstack1l1llll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬᕫ")])
          else:
            bstack1ll11111l11_opy_(bstack1l11l11lll_opy_)
            sys.path.append(os.path.dirname(os.path.abspath(bstack1l1l1l1ll1l_opy_[bstack1l1llll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ᕬ")])))
            sys.argv = sys.argv[2:]
            mod_globals = globals()
            mod_globals[bstack1l1llll_opy_ (u"ࠫࡤࡥ࡮ࡢ࡯ࡨࡣࡤ࠭ᕭ")] = bstack1l1llll_opy_ (u"ࠬࡥ࡟࡮ࡣ࡬ࡲࡤࡥࠧᕮ")
            mod_globals[bstack1l1llll_opy_ (u"࠭࡟ࡠࡨ࡬ࡰࡪࡥ࡟ࠨᕯ")] = os.path.abspath(bstack1l1l1l1ll1l_opy_[bstack1l1llll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪᕰ")])
            exec(open(bstack1l1l1l1ll1l_opy_[bstack1l1llll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫᕱ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1l1llll_opy_ (u"ࠩࡆࡥࡺ࡭ࡨࡵࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠩᕲ").format(str(e)))
          bstack1l11l1l1l1_opy_ = bstack1l1l1l1ll1l_opy_[bstack1l1llll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ᕳ")]
          if isinstance(bstack1l11l1l1l1_opy_, (list, tuple)):
            bstack1l11l1l1l1_opy_ = bstack1l1llll_opy_ (u"ࠫࠥ࠭ᕴ").join(str(a) for a in bstack1l11l1l1l1_opy_)
          for driver in bstack1111ll11l_opy_:
            bstack111111111l_opy_.append({
              bstack1l1llll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᕵ"): bstack1l11l1l1l1_opy_,
              bstack1l1llll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᕶ"): str(e),
              bstack1l1llll_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ᕷ"): multiprocessing.current_process().name
            })
            bstack1l1lll1ll1l_opy_(driver, bstack1l1llll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᕸ"), bstack1l1llll_opy_ (u"ࠤࡖࡩࡸࡹࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧᕹ") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1111ll11l_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack11ll111lll_opy_, CONFIG, logger)
      bstack1llll111l11_opy_()
      bstack1llll11l1l1_opy_()
      percy.bstack1lllll111ll_opy_()
      bstack11l1l11l1_opy_ = {
        bstack1l1llll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ᕺ"): args[0],
        bstack1l1llll_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫᕻ"): CONFIG,
        bstack1l1llll_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭ᕼ"): bstack1lll1ll1l11_opy_,
        bstack1l1llll_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨᕽ"): bstack11ll111lll_opy_
      }
      if bstack11llllll1l_opy_(args):
        bstack11l1l11l1_opy_[bstack1l1llll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪᕾ")] = args
      if bstack1l1llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᕿ") in CONFIG:
        bstack11111l11ll_opy_ = bstack11l11ll11_opy_(args, logger, CONFIG, BROWSERSTACK_AUTOMATION, bstack1111111l1_opy_)
        bstack1llllll11ll_opy_ = bstack11111l11ll_opy_.bstack11l1l1l11_opy_(run_on_browserstack, bstack11l1l11l1_opy_, bstack111l1lllll_opy_(args))
      else:
        if bstack111l1lllll_opy_(args):
          bstack11lllllll_opy_ = multiprocessing.get_context(bstack1l1llll_opy_ (u"ࠩࡶࡴࡦࡽ࡮ࠨᖀ"))
          bstack11l1l11l1_opy_[bstack1l1llll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ᖁ")] = args
          test = bstack11lllllll_opy_.Process(name=str(0),
                                target=run_on_browserstack, args=(bstack11l1l11l1_opy_,))
          test.start()
          test.join()
        elif bstack11llllll1l_opy_(args):
          bstack1ll11111l11_opy_(bstack1l11l11lll_opy_)
          bstack1l1ll11l11l_opy_(args)
        else:
          bstack1ll11111l11_opy_(bstack1l11l11lll_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1l1llll_opy_ (u"ࠫࡤࡥ࡮ࡢ࡯ࡨࡣࡤ࠭ᖂ")] = bstack1l1llll_opy_ (u"ࠬࡥ࡟࡮ࡣ࡬ࡲࡤࡥࠧᖃ")
          mod_globals[bstack1l1llll_opy_ (u"࠭࡟ࡠࡨ࡬ࡰࡪࡥ࡟ࠨᖄ")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack11l11l1ll1_opy_ == bstack1l1llll_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ᖅ") or bstack11l11l1ll1_opy_ == bstack1l1llll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧᖆ"):
    percy.init(bstack11ll111lll_opy_, CONFIG, logger)
    percy.bstack1lllll111ll_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1ll1l1lll1_opy_(e, bstack1lll11l1ll_opy_)
    bstack1llll111l11_opy_()
    if bstack1ll1ll111ll_opy_:
      os.environ[bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡆࡈࡊࡆ࡛ࡌࡕࡡࡏࡓࡈࡇࡌࡠࡋࡇࠫᖇ")] = bstack1ll1ll111ll_opy_
    bstack1ll11111l11_opy_(bstack1ll1ll1ll1l_opy_)
    if BROWSERSTACK_AUTOMATION:
      bstack1ll1l1l111l_opy_(bstack1ll1ll1ll1l_opy_, args)
      if bstack1l1llll_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨᖈ") in args:
        i = args.index(bstack1l1llll_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩᖉ"))
        args.pop(i)
        args.pop(i)
      if bstack1l1llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᖊ") not in CONFIG:
        CONFIG[bstack1l1llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᖋ")] = [{}]
        bstack1111111l1_opy_ = 1
      if bstack1l1lll1lll_opy_ == 0:
        bstack1l1lll1lll_opy_ = 1
      args.insert(0, str(bstack1l1lll1lll_opy_))
      args.insert(0, str(bstack1l1llll_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬᖌ")))
    if TestHubHandler.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1l111ll1l1_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack11111111l1_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack1l1llll_opy_ (u"ࠣࡔࡒࡆࡔ࡚࡟ࡐࡒࡗࡍࡔࡔࡓࠣᖍ"),
        ).parse_args(bstack1l111ll1l1_opy_)
        bstack111ll11lll_opy_ = args.index(bstack1l111ll1l1_opy_[0]) if len(bstack1l111ll1l1_opy_) > 0 else len(args)
        args.insert(bstack111ll11lll_opy_, str(bstack1l1llll_opy_ (u"ࠩ࠰࠱ࡱ࡯ࡳࡵࡧࡱࡩࡷ࠭ᖎ")))
        args.insert(bstack111ll11lll_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l1llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡶࡴࡨ࡯ࡵࡡ࡯࡭ࡸࡺࡥ࡯ࡧࡵ࠲ࡵࡿࠧᖏ"))))
        if bstack11ll1111l_opy_.bstack11lll1l1l_opy_(CONFIG):
          args.insert(bstack111ll11lll_opy_, str(bstack1l1llll_opy_ (u"ࠫ࠲࠳࡬ࡪࡵࡷࡩࡳ࡫ࡲࠨᖐ")))
          args.insert(bstack111ll11lll_opy_ + 1, str(bstack1l1llll_opy_ (u"ࠬࡘࡥࡵࡴࡼࡊࡦ࡯࡬ࡦࡦ࠽ࡿࢂ࠭ᖑ").format(bstack11ll1111l_opy_.bstack1l1111111_opy_(CONFIG))))
        if bstack11lll11l1l_opy_(os.environ.get(bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠫᖒ"))) and str(os.environ.get(bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠫᖓ"), bstack1l1llll_opy_ (u"ࠨࡰࡸࡰࡱ࠭ᖔ"))) != bstack1l1llll_opy_ (u"ࠩࡱࡹࡱࡲࠧᖕ"):
          for bstack11111l1111_opy_ in bstack11111111l1_opy_:
            args.remove(bstack11111l1111_opy_)
          test_files = os.environ.get(bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠧᖖ")).split(bstack1l1llll_opy_ (u"ࠫ࠱࠭ᖗ"))
          for bstack1l1l11ll111_opy_ in test_files:
            args.append(bstack1l1l11ll111_opy_)
      except Exception as e:
        logger.error(bstack1l1llll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡥࡹࡺࡡࡤࡪ࡬ࡲ࡬ࠦ࡬ࡪࡵࡷࡩࡳ࡫ࡲࠡࡨࡲࡶࠥࢁࡽ࠯ࠢࡈࡶࡷࡵࡲࠡ࠯ࠣࡿࢂࠨᖘ").format(bstack1lll11ll1l_opy_, e))
    pabot.main(args)
  elif bstack11l11l1ll1_opy_ == bstack1l1llll_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧᖙ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1ll1l1lll1_opy_(e, bstack1lll11l1ll_opy_)
    for a in args:
      if bstack1l1llll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝࠭ᖚ") in a:
        PLATFORM_INDEX = int(a.split(bstack1l1llll_opy_ (u"ࠨ࠼ࠪᖛ"))[1])
      if bstack1l1llll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡆࡈࡊࡑࡕࡃࡂࡎࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ᖜ") in a:
        bstack1ll1ll111ll_opy_ = str(a.split(bstack1l1llll_opy_ (u"ࠪ࠾ࠬᖝ"))[1])
      if bstack1l1llll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡇࡑࡏࡁࡓࡉࡖࠫᖞ") in a:
        bstack1l1ll1lll1l_opy_ = str(a.split(bstack1l1llll_opy_ (u"ࠬࡀࠧᖟ"))[1])
    if os.environ.get(bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡊࡅࡇࡃࡘࡐ࡙ࡥࡌࡐࡅࡄࡐࡤࡏࡄࠨᖠ")):
      bstack1ll1ll111ll_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡄࡆࡈࡄ࡙ࡑ࡚࡟ࡍࡑࡆࡅࡑࡥࡉࡅࠩᖡ"))
    if bstack1ll1ll111ll_opy_:
      if bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬᖢ") not in CONFIG:
        CONFIG[bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ᖣ")] = {}
      CONFIG[bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧᖤ")][bstack1l1llll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᖥ")] = bstack1ll1ll111ll_opy_
    bstack1l1l1l1111l_opy_ = None
    bstack1ll11ll11l_opy_ = None
    if bstack1l1llll_opy_ (u"ࠬ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠫᖦ") in args:
      i = args.index(bstack1l1llll_opy_ (u"࠭࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠬᖧ"))
      args.pop(i)
      bstack1l1l1l1111l_opy_ = args.pop(i)
    if bstack1l1llll_opy_ (u"ࠧ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࠪᖨ") in args:
      i = args.index(bstack1l1llll_opy_ (u"ࠨ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࠫᖩ"))
      args.pop(i)
      bstack1ll11ll11l_opy_ = args.pop(i)
    if bstack1l1l1l1111l_opy_ is not None:
      global bstack1llll11111l_opy_
      bstack1llll11111l_opy_ = bstack1l1l1l1111l_opy_
    if bstack1ll11ll11l_opy_ is not None and int(PLATFORM_INDEX) < 0:
      PLATFORM_INDEX = int(bstack1ll11ll11l_opy_)
    if cli.is_enabled(CONFIG):
      if cli.bstack111l1ll11_opy_():
        bstack111ll1l11_opy_.invoke(Events.CONNECT, bstack111ll11ll_opy_())
        cli.bstack1ll1111l11l_opy_(PLATFORM_INDEX)
      if cli.bstack1l1ll1l1111_opy_(EventDispatcherModule):
        cli.bstack1ll11l111_opy_()
    bstack1ll11111l11_opy_(bstack1ll1ll1ll1l_opy_)
    run_cli(args)
    if bstack1l1llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠭ᖪ") in multiprocessing.current_process().__dict__.keys():
      for bstack1l1lllll11l_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack111111111l_opy_.append(bstack1l1lllll11l_opy_)
  elif bstack11l11l1ll1_opy_ == bstack1l1llll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᖫ"):
    if os.environ.get(bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡉࡋ࡟ࡑࡎࡘࡋࡎࡔ࡟ࡎࡑࡇࡉࠬᖬ")):
      os.environ[bstack1lll1l11111_opy_] = bstack1lll11l111l_opy_
      os.environ[bstack1l1llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࠫᖭ")] = json.dumps(CONFIG)
      os.environ[bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡎࡕࡃࡡࡘࡖࡑ࠭ᖮ")] = bstack1l1l111ll11_opy_()
      os.environ[bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨᖯ")] = str(bstack11ll111lll_opy_)
      os.environ[bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡎࡘࡋࡎࡔࠧᖰ")] = str(True)
      os.environ[bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᖱ")] = str(max(PLATFORM_INDEX, 0))
      if CONFIG.get(bstack1l1llll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᖲ")):
        os.environ[bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬᖳ")] = CONFIG[bstack1l1llll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᖴ")]
      if CONFIG.get(bstack1l1llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᖵ")):
        os.environ[bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪᖶ")] = CONFIG[bstack1l1llll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᖷ")]
      return
    else:
      bstack1l11l11ll1_opy_ = bstack11llll11l_opy_(args, logger, CONFIG, BROWSERSTACK_AUTOMATION)
      bstack1l11l11ll1_opy_.bstack11l11llll_opy_()
      bstack1llll111l11_opy_()
      PARALLELISE_THREADING_PYTHON = True
      bstack1ll11l1lll_opy_ = bstack1l11l11ll1_opy_.bstack11ll1llll_opy_()
      bstack1l11l11ll1_opy_.bstack11l1l11l1_opy_(bstack11l11l1l1l_opy_)
      bstack1l11l11ll1_opy_.bstack1lll1111_opy_()
      bstack1ll111l1ll1_opy_(bstack11l11l1ll1_opy_, CONFIG, bstack1l11l11ll1_opy_.bstack1l111111l_opy_())
      performance_tester.end(EVENTS.bstack1111l1l1l_opy_.value, EVENTS.bstack1111l1l1l_opy_.value + bstack1l1llll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᖸ"), EVENTS.bstack1111l1l1l_opy_.value + bstack1l1llll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᖹ"), status=True, failure=None, test_name=SESSION_NAME)
      bstack1lll11l1l11_opy_ = bstack1l11l11ll1_opy_.bstack11l1l1l11_opy_(bstack1ll11ll1111_opy_, {
        bstack1l1llll_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫᖺ"): CONFIG,
        bstack1l1llll_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭ᖻ"): bstack1lll1ll1l11_opy_,
        bstack1l1llll_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨᖼ"): bstack11ll111lll_opy_,
        bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪᖽ"): BROWSERSTACK_AUTOMATION,
        bstack1l1llll_opy_ (u"ࠨࡑ࡙ࡉࡗࡘࡉࡅࡇࡢࡐࡔࡇࡄࡠࡖࡈࡗ࡙ࡏࡎࡈࠩᖾ"): bstack1l11l11l11_opy_
      })
      if not bstack1l1l1l1ll1l_opy_:
        bstack1l1ll1ll1ll_opy_ = PerformanceTester.mark_start(EVENTS.bstack1llll11l11_opy_.value)
      try:
        bstack1l1lll11111_opy_, bstack1ll11ll11ll_opy_ = map(list, zip(*bstack1lll11l1l11_opy_))
        bstack1lll1llll1_opy_ = bstack1l1lll11111_opy_[0]
        for status_code in bstack1ll11ll11ll_opy_:
          if status_code != 0:
            bstack1111l1l111_opy_ = status_code
            break
      except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡡࡷࡧࠣࡩࡷࡸ࡯ࡳࡵࠣࡥࡳࡪࠠࡴࡶࡤࡸࡺࡹࠠࡤࡱࡧࡩ࠳ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࠽ࠤࢀࢃࠢᖿ").format(str(e)))
  elif bstack11l11l1ll1_opy_ == bstack1l1llll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪᗀ"):
    try:
      from behave.__main__ import main as bstack1l1111ll11_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1ll1l1lll1_opy_(e, bstack1l111lllll_opy_)
    bstack1llll111l11_opy_()
    PARALLELISE_THREADING_PYTHON = True
    bstack11l1ll1l1_opy_ = 1
    if bstack1l1llll_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫᗁ") in CONFIG:
      bstack11l1ll1l1_opy_ = CONFIG[bstack1l1llll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬᗂ")]
    if bstack1l1llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᗃ") in CONFIG:
      bstack1lll1l1l1l1_opy_ = int(bstack11l1ll1l1_opy_) * int(len(CONFIG[bstack1l1llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᗄ")]))
    else:
      bstack1lll1l1l1l1_opy_ = int(bstack11l1ll1l1_opy_)
    config = Configuration(args)
    bstack11ll1l111l_opy_ = config.paths
    if len(bstack11ll1l111l_opy_) == 0:
      import glob
      pattern = bstack1l1llll_opy_ (u"ࠨࠬ࠭࠳࠯࠴ࡦࡦࡣࡷࡹࡷ࡫ࠧᗅ")
      feature_files = glob.glob(pattern, recursive=True)
      args.extend(feature_files)
      config = Configuration(args)
      bstack11ll1l111l_opy_ = config.paths
    bstack1lll1lll_opy_ = [os.path.normpath(item) for item in bstack11ll1l111l_opy_]
    bstack11111l1l1_opy_ = [os.path.normpath(item) for item in args]
    bstack1lll1111l1_opy_ = [item for item in bstack11111l1l1_opy_ if item not in bstack1lll1lll_opy_]
    import platform as pf
    if pf.system().lower() == bstack1l1llll_opy_ (u"ࠩࡺ࡭ࡳࡪ࡯ࡸࡵࠪᗆ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1lll1lll_opy_ = [str(PurePosixPath(PureWindowsPath(bstack11ll11l11l_opy_)))
                    for bstack11ll11l11l_opy_ in bstack1lll1lll_opy_]
    try:
      bstack1l1l11llll1_opy_ = bstack1lll11l1_opy_(args, logger, CONFIG, BROWSERSTACK_AUTOMATION)
      bstack1l1l11llll1_opy_.bstack1ll1ll11_opy_(bstack1lll1lll_opy_)
      bstack1l1l11llll1_opy_.bstack1lll1111_opy_()
      bstack1lll1lll_opy_ = bstack1l1l11llll1_opy_.bstack1llll11l_opy_()
    except Exception as e:
      logger.error(bstack1l1llll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡡࡱࡲ࡯ࡽࠥࡺࡥࡴࡶࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡪࡴࡸࠠࡣࡧ࡫ࡥࡻ࡫࠺ࠡࠧࡶࠦᗇ"), e, exc_info=True)
      logger.info(bstack1l1llll_opy_ (u"ࠦࡈࡵ࡮ࡵ࡫ࡱࡹ࡮ࡴࡧࠡࡹ࡬ࡸ࡭ࠦ࡯ࡳ࡫ࡪ࡭ࡳࡧ࡬ࠡࡵࡳࡩࡨࠦࡦࡪ࡮ࡨࡷࠥࡽࡩࡵࡪࡲࡹࡹࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠨᗈ"))
    bstack11l1ll11l_opy_ = []
    for spec in bstack1lll1lll_opy_:
      bstack11lll11ll_opy_ = []
      bstack11lll11ll_opy_ += bstack1lll1111l1_opy_
      bstack11lll11ll_opy_.append(spec)
      bstack11l1ll11l_opy_.append(bstack11lll11ll_opy_)
    execution_items = []
    for bstack11lll11ll_opy_ in bstack11l1ll11l_opy_:
      if bstack1l1llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᗉ") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack1l1llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᗊ")]):
          item = {}
          item[bstack1l1llll_opy_ (u"ࠧࡢࡴࡪࠫᗋ")] = bstack1l1llll_opy_ (u"ࠨࠢࠪᗌ").join(bstack11lll11ll_opy_)
          item[bstack1l1llll_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨᗍ")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack1l1llll_opy_ (u"ࠪࡥࡷ࡭ࠧᗎ")] = bstack1l1llll_opy_ (u"ࠫࠥ࠭ᗏ").join(bstack11lll11ll_opy_)
        item[bstack1l1llll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᗐ")] = 0
        execution_items.append(item)
    bstack1llll1l11l_opy_ = bstack1ll1l11111l_opy_(execution_items, bstack1lll1l1l1l1_opy_)
    for execution_item in bstack1llll1l11l_opy_:
      bstack11l1ll1ll_opy_ = []
      for item in execution_item:
        bstack11l1ll1ll_opy_.append(bstack1l111llll_opy_(name=str(item[bstack1l1llll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬᗑ")]),
                                             target=bstack1l1llll1l1l_opy_,
                                             args=(item[bstack1l1llll_opy_ (u"ࠧࡢࡴࡪࠫᗒ")],)))
      for t in bstack11l1ll1ll_opy_:
        t.start()
      for t in bstack11l1ll1ll_opy_:
        t.join()
  else:
    bstack1lll111lll_opy_(bstack1ll1l1lllll_opy_)
  if not bstack1l1l1l1ll1l_opy_:
    bstack111l1l1l1l_opy_()
    if bstack1l1ll1ll1ll_opy_:
      PerformanceTester.end(EVENTS.bstack1llll11l11_opy_.value, bstack1l1ll1ll1ll_opy_ + bstack1l1llll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᗓ"), bstack1l1ll1ll1ll_opy_ + bstack1l1llll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᗔ"), status=True, failure=None, test_name=None)
  logger_utils.bstack1llll1l111_opy_()
def browserstack_initialize(bstack111ll1lll1_opy_=None):
  logger.info(bstack1l1llll_opy_ (u"ࠪࡖࡺࡴ࡮ࡪࡰࡪࠤࡘࡊࡋࠡࡹ࡬ࡸ࡭ࠦࡡࡳࡩࡶ࠾ࠥ࠭ᗕ") + str(bstack111ll1lll1_opy_))
  run_on_browserstack(bstack111ll1lll1_opy_, None, True)
@measure(event_name=EVENTS.bstack11l11l11l1_opy_, stage=STAGE.SINGLE, bstack11lllll111_opy_=SESSION_NAME)
def bstack111l1l1l1l_opy_():
  global CONFIG
  global bstack1lll11l111l_opy_
  global bstack1111l1l111_opy_
  global bstack1l1l1l11l1l_opy_
  global global_config
  global _11lllllll1_opy_
  FileUploader.bstack11ll1111ll_opy_()
  _11lllllll1_opy_ = cli.is_running()
  if _11lllllll1_opy_:
    bstack111ll1l11_opy_.invoke(Events.bstack1l1l1111111_opy_)
  else:
    bstack11ll1lll1_opy_ = bstack11ll1111l_opy_.bstack1lll1l11_opy_(config=CONFIG)
    bstack11ll1lll1_opy_.bstack1ll1l111l11_opy_(CONFIG)
  hashed_id = None
  bstack11111ll1l_opy_ = None
  def bstack11ll1ll111_opy_():
    try:
      if bstack1lll11l111l_opy_ == bstack1l1llll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᗖ"):
        if not cli.is_enabled(CONFIG):
          TestHubHandler.stop()
      else:
        TestHubHandler.stop()
    except Exception as e:
      logger.debug(bstack1l1llll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡸࡺ࡯ࡱࡲ࡬ࡲ࡬ࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࡽࢀࠦᗗ").format(e))
  def bstack1l1111lll1_opy_():
    try:
      if not cli.is_enabled(CONFIG):
        bstack1ll111ll_opy_.bstack1lll1lll11_opy_()
        bstack1ll111ll_opy_.bstack1l1l1l1l1l_opy_(CONFIG)
    except Exception as e:
      logger.debug(bstack1l1llll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡶࡲࡪࡰࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࠦ࡬ࡪࡰ࡮࠾ࠥࢁࡽࠣᗘ").format(e))
  def bstack1llll1ll1l_opy_():
    nonlocal hashed_id, bstack11111ll1l_opy_
    try:
      if bstack1l1llll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫᗙ") in CONFIG and str(CONFIG[bstack1l1llll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬᗚ")]).lower() != bstack1l1llll_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨᗛ"):
        hashed_id, bstack11111ll1l_opy_ = bstack1ll1l1l11ll_opy_()
      else:
        hashed_id, bstack11111ll1l_opy_ = get_build_link()
    except Exception as e:
      logger.debug(bstack1l1llll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡦࡺ࡯࡬ࡥࠢ࡯࡭ࡳࡱ࠺ࠡࡽࢀࠦᗜ").format(e))
  bstack11lll1l1ll_opy_ = threading.Thread(target=bstack11ll1ll111_opy_)
  bstack1lll11ll1ll_opy_ = threading.Thread(target=bstack1l1111lll1_opy_)
  bstack1ll1ll1l1ll_opy_ = threading.Thread(target=bstack1llll1ll1l_opy_)
  threads = [bstack11lll1l1ll_opy_, bstack1lll11ll1ll_opy_, bstack1ll1ll1l1ll_opy_]
  for thread in threads:
    try:
      thread.start()
    except Exception as e:
      logger.debug(bstack1l1llll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡷࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡺࡨࡳࡧࡤࡨࠥࢁࡽ࠻ࠢࡾࢁࠧᗝ").format(thread.name, e))
  for thread in threads:
    try:
      thread.join()
    except Exception as e:
      logger.debug(bstack1l1llll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡯ࡵࡩ࡯࡫ࡱ࡫ࠥࡺࡨࡳࡧࡤࡨࠥࢁࡽ࠻ࠢࡾࢁࠧᗞ").format(thread.name, e))
  bstack111l1111l1_opy_(hashed_id)
  logger.info(bstack1l1llll_opy_ (u"࠭ࡓࡅࡍࠣࡶࡺࡴࠠࡦࡰࡧࡩࡩࠦࡦࡰࡴࠣ࡭ࡩࡀࠧᗟ") + global_config.get_property(bstack1l1llll_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥࠩᗠ"), bstack1l1llll_opy_ (u"ࠨࠩᗡ")) + bstack1l1llll_opy_ (u"ࠩ࠯ࠤࡹ࡫ࡳࡵࡪࡸࡦࠥ࡯ࡤ࠻ࠢࠪᗢ") + os.getenv(bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᗣ"), bstack1l1llll_opy_ (u"ࠫࠬᗤ")))
  if hashed_id is not None and bstack1llll1l111l_opy_() != -1:
    sessions = bstack11l111ll1l_opy_(hashed_id)
    bstack111l1l11l1_opy_(sessions, bstack11111ll1l_opy_)
  if bstack1lll11l111l_opy_ == bstack1l1llll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᗥ") and bstack1111l1l111_opy_ != 0:
    sys.exit(bstack1111l1l111_opy_)
  if bstack1lll11l111l_opy_ == bstack1l1llll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ᗦ") and bstack1l1l1l11l1l_opy_ != 0:
    sys.exit(bstack1l1l1l11l1l_opy_)
def bstack111l1111l1_opy_(new_id):
    global bstack1lll1l11l1l_opy_
    bstack1lll1l11l1l_opy_ = new_id
def bstack11l1l111l1_opy_(bstack1l1l1ll1l1l_opy_):
  if bstack1l1l1ll1l1l_opy_:
    return bstack1l1l1ll1l1l_opy_.capitalize()
  else:
    return bstack1l1llll_opy_ (u"ࠧࠨᗧ")
@measure(event_name=EVENTS.bstack1ll1111lll1_opy_, stage=STAGE.SINGLE, bstack11lllll111_opy_=SESSION_NAME)
def bstack1111ll1l1_opy_(bstack111l111ll1_opy_):
  if bstack1l1llll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᗨ") in bstack111l111ll1_opy_ and bstack111l111ll1_opy_[bstack1l1llll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᗩ")] != bstack1l1llll_opy_ (u"ࠪࠫᗪ"):
    return bstack111l111ll1_opy_[bstack1l1llll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᗫ")]
  else:
    bstack11lllll111_opy_ = bstack1l1llll_opy_ (u"ࠧࠨᗬ")
    if bstack1l1llll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ᗭ") in bstack111l111ll1_opy_ and bstack111l111ll1_opy_[bstack1l1llll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧᗮ")] != None:
      bstack11lllll111_opy_ += bstack111l111ll1_opy_[bstack1l1llll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨᗯ")] + bstack1l1llll_opy_ (u"ࠤ࠯ࠤࠧᗰ")
      if bstack111l111ll1_opy_[bstack1l1llll_opy_ (u"ࠪࡳࡸ࠭ᗱ")] == bstack1l1llll_opy_ (u"ࠦ࡮ࡵࡳࠣᗲ"):
        bstack11lllll111_opy_ += bstack1l1llll_opy_ (u"ࠧ࡯ࡏࡔࠢࠥᗳ")
      bstack11lllll111_opy_ += (bstack111l111ll1_opy_[bstack1l1llll_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪᗴ")] or bstack1l1llll_opy_ (u"ࠧࠨᗵ"))
      return bstack11lllll111_opy_
    else:
      bstack11lllll111_opy_ += bstack11l1l111l1_opy_(bstack111l111ll1_opy_[bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩᗶ")]) + bstack1l1llll_opy_ (u"ࠤࠣࠦᗷ") + (
              bstack111l111ll1_opy_[bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᗸ")] or bstack1l1llll_opy_ (u"ࠫࠬᗹ")) + bstack1l1llll_opy_ (u"ࠧ࠲ࠠࠣᗺ")
      if bstack111l111ll1_opy_[bstack1l1llll_opy_ (u"࠭࡯ࡴࠩᗻ")] == bstack1l1llll_opy_ (u"ࠢࡘ࡫ࡱࡨࡴࡽࡳࠣᗼ"):
        bstack11lllll111_opy_ += bstack1l1llll_opy_ (u"࡙ࠣ࡬ࡲࠥࠨᗽ")
      bstack11lllll111_opy_ += bstack111l111ll1_opy_[bstack1l1llll_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᗾ")] or bstack1l1llll_opy_ (u"ࠪࠫᗿ")
      return bstack11lllll111_opy_
@measure(event_name=EVENTS.bstack111llll111_opy_, stage=STAGE.SINGLE, bstack11lllll111_opy_=SESSION_NAME)
def bstack1111ll11l1_opy_(bstack1l1l11l111l_opy_):
  if bstack1l1l11l111l_opy_ == bstack1l1llll_opy_ (u"ࠦࡩࡵ࡮ࡦࠤᘀ"):
    return bstack1l1llll_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡨࡴࡨࡩࡳࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡨࡴࡨࡩࡳࠨ࠾ࡄࡱࡰࡴࡱ࡫ࡴࡦࡦ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨᘁ")
  elif bstack1l1l11l111l_opy_ == bstack1l1llll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᘂ"):
    return bstack1l1llll_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡵࡩࡩࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡳࡧࡧࠦࡃࡌࡡࡪ࡮ࡨࡨࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪᘃ")
  elif bstack1l1l11l111l_opy_ == bstack1l1llll_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣᘄ"):
    return bstack1l1llll_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾࡬ࡸࡥࡦࡰ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦ࡬ࡸࡥࡦࡰࠥࡂࡕࡧࡳࡴࡧࡧࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩᘅ")
  elif bstack1l1l11l111l_opy_ == bstack1l1llll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤᘆ"):
    return bstack1l1llll_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡲࡦࡦ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡷ࡫ࡤࠣࡀࡈࡶࡷࡵࡲ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ᘇ")
  elif bstack1l1l11l111l_opy_ == bstack1l1llll_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࠨᘈ"):
    return bstack1l1llll_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࠥࡨࡩࡦ࠹࠲࠷࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࠧࡪ࡫ࡡ࠴࠴࠹ࠦࡃ࡚ࡩ࡮ࡧࡲࡹࡹࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫᘉ")
  elif bstack1l1l11l111l_opy_ == bstack1l1llll_opy_ (u"ࠢࡳࡷࡱࡲ࡮ࡴࡧࠣᘊ"):
    return bstack1l1llll_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡦࡱࡧࡣ࡬࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡦࡱࡧࡣ࡬ࠤࡁࡖࡺࡴ࡮ࡪࡰࡪࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩᘋ")
  else:
    return bstack1l1llll_opy_ (u"ࠩ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡨ࡬ࡢࡥ࡮࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡨ࡬ࡢࡥ࡮ࠦࡃ࠭ᘌ") + bstack11l1l111l1_opy_(
      bstack1l1l11l111l_opy_) + bstack1l1llll_opy_ (u"ࠪࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩᘍ")
def bstack1lllll1llll_opy_(session):
  return bstack1l1llll_opy_ (u"ࠫࡁࡺࡲࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡴࡲࡻࠧࡄ࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠡࡵࡨࡷࡸ࡯࡯࡯࠯ࡱࡥࡲ࡫ࠢ࠿࠾ࡤࠤ࡭ࡸࡥࡧ࠿ࠥࡿࢂࠨࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣࡡࡥࡰࡦࡴ࡫ࠣࡀࡾࢁࡁ࠵ࡡ࠿࠾࠲ࡸࡩࡄࡻࡾࡽࢀࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂ࠯ࡵࡴࡁࠫᘎ").format(
    session[bstack1l1llll_opy_ (u"ࠬࡶࡵࡣ࡮࡬ࡧࡤࡻࡲ࡭ࠩᘏ")], bstack1111ll1l1_opy_(session), bstack1111ll11l1_opy_(session[bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡹࡴࡢࡶࡸࡷࠬᘐ")]),
    bstack1111ll11l1_opy_(session[bstack1l1llll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᘑ")]),
    bstack11l1l111l1_opy_(session[bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩᘒ")] or session[bstack1l1llll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩᘓ")] or bstack1l1llll_opy_ (u"ࠪࠫᘔ")) + bstack1l1llll_opy_ (u"ࠦࠥࠨᘕ") + (session[bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᘖ")] or bstack1l1llll_opy_ (u"࠭ࠧᘗ")),
    session[bstack1l1llll_opy_ (u"ࠧࡰࡵࠪᘘ")] + bstack1l1llll_opy_ (u"ࠣࠢࠥᘙ") + session[bstack1l1llll_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᘚ")], session[bstack1l1llll_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬᘛ")] or bstack1l1llll_opy_ (u"ࠫࠬᘜ"),
    session[bstack1l1llll_opy_ (u"ࠬࡩࡲࡦࡣࡷࡩࡩࡥࡡࡵࠩᘝ")] if session[bstack1l1llll_opy_ (u"࠭ࡣࡳࡧࡤࡸࡪࡪ࡟ࡢࡶࠪᘞ")] else bstack1l1llll_opy_ (u"ࠧࠨᘟ"))
@measure(event_name=EVENTS.bstack11l1lll1ll_opy_, stage=STAGE.SINGLE, bstack11lllll111_opy_=SESSION_NAME)
def bstack111l1l11l1_opy_(sessions, bstack11111ll1l_opy_):
  try:
    bstack1lll11lllll_opy_ = bstack1l1llll_opy_ (u"ࠣࠤᘠ")
    if not os.path.exists(bstack1l111111l1_opy_):
      os.mkdir(bstack1l111111l1_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l1llll_opy_ (u"ࠩࡤࡷࡸ࡫ࡴࡴ࠱ࡵࡩࡵࡵࡲࡵ࠰࡫ࡸࡲࡲࠧᘡ")), bstack1l1llll_opy_ (u"ࠪࡶࠬᘢ")) as f:
      bstack1lll11lllll_opy_ = f.read()
    bstack1lll11lllll_opy_ = bstack1lll11lllll_opy_.replace(bstack1l1llll_opy_ (u"ࠫࢀࠫࡒࡆࡕࡘࡐ࡙࡙࡟ࡄࡑࡘࡒ࡙ࠫࡽࠨᘣ"), str(len(sessions)))
    bstack1lll11lllll_opy_ = bstack1lll11lllll_opy_.replace(bstack1l1llll_opy_ (u"ࠬࢁࠥࡃࡗࡌࡐࡉࡥࡕࡓࡎࠨࢁࠬᘤ"), bstack11111ll1l_opy_)
    bstack1lll11lllll_opy_ = bstack1lll11lllll_opy_.replace(bstack1l1llll_opy_ (u"࠭ࡻࠦࡄࡘࡍࡑࡊ࡟ࡏࡃࡐࡉࠪࢃࠧᘥ"),
                                              sessions[0].get(bstack1l1llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥ࡮ࡢ࡯ࡨࠫᘦ")) if sessions[0] else bstack1l1llll_opy_ (u"ࠨࠩᘧ"))
    with open(os.path.join(bstack1l111111l1_opy_, bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠮ࡴࡨࡴࡴࡸࡴ࠯ࡪࡷࡱࡱ࠭ᘨ")), bstack1l1llll_opy_ (u"ࠪࡻࠬᘩ")) as stream:
      stream.write(bstack1lll11lllll_opy_.split(bstack1l1llll_opy_ (u"ࠫࢀࠫࡓࡆࡕࡖࡍࡔࡔࡓࡠࡆࡄࡘࡆࠫࡽࠨᘪ"))[0])
      for session in sessions:
        stream.write(bstack1lllll1llll_opy_(session))
      stream.write(bstack1lll11lllll_opy_.split(bstack1l1llll_opy_ (u"ࠬࢁࠥࡔࡇࡖࡗࡎࡕࡎࡔࡡࡇࡅ࡙ࡇࠥࡾࠩᘫ"))[1])
    logger.info(bstack1l1llll_opy_ (u"࠭ࡇࡦࡰࡨࡶࡦࡺࡥࡥࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡤࡸ࡭ࡱࡪࠠࡢࡴࡷ࡭࡫ࡧࡣࡵࡵࠣࡥࡹࠦࡻࡾࠩᘬ").format(bstack1l111111l1_opy_));
  except Exception as e:
    logger.debug(bstack1lllll11l1l_opy_.format(str(e)))
def bstack11l111ll1l_opy_(hashed_id):
  global CONFIG
  try:
    time_start = datetime.datetime.now()
    host = bstack1l1llll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠲ࡩ࡬ࡰࡷࡧ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧᘭ") if bstack1l1llll_opy_ (u"ࠨࡣࡳࡴࠬᘮ") in CONFIG else bstack1l1llll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡵ࡯࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪᘯ")
    user = CONFIG[bstack1l1llll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᘰ")]
    key = CONFIG[bstack1l1llll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᘱ")]
    bstack1lllllll1ll_opy_ = bstack1l1llll_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᘲ") if bstack1l1llll_opy_ (u"࠭ࡡࡱࡲࠪᘳ") in CONFIG else (bstack1l1llll_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫᘴ") if CONFIG.get(bstack1l1llll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬᘵ")) else bstack1l1llll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᘶ"))
    host = bstack11l11l111l_opy_(cli.config, [bstack1l1llll_opy_ (u"ࠥࡥࡵ࡯ࡳࠣᘷ"), bstack1l1llll_opy_ (u"ࠦࡦࡶࡰࡂࡷࡷࡳࡲࡧࡴࡦࠤᘸ"), bstack1l1llll_opy_ (u"ࠧࡧࡰࡪࠤᘹ")], host) if bstack1l1llll_opy_ (u"࠭ࡡࡱࡲࠪᘺ") in CONFIG else bstack11l11l111l_opy_(cli.config, [bstack1l1llll_opy_ (u"ࠢࡢࡲ࡬ࡷࠧᘻ"), bstack1l1llll_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧࠥᘼ"), bstack1l1llll_opy_ (u"ࠤࡤࡴ࡮ࠨᘽ")], host)
    url = bstack1l1llll_opy_ (u"ࠪࡿࢂ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡹࡥࡴࡵ࡬ࡳࡳࡹ࠮࡫ࡵࡲࡲࠬᘾ").format(host, bstack1lllllll1ll_opy_, hashed_id)
    headers = {
      bstack1l1llll_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪᘿ"): bstack1l1llll_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨᙀ"),
    }
    proxies = bstack1ll11l111l1_opy_(CONFIG, url)
    from bstack_utils.helper import get_ca_cert_path
    bstack1lll1lllll_opy_ = {bstack1l1llll_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᙁ"): headers, bstack1l1llll_opy_ (u"ࠧࡱࡴࡲࡼ࡮࡫ࡳࠨᙂ"): proxies, bstack1l1llll_opy_ (u"ࠨࡣࡸࡸ࡭࠭ᙃ"): (user, key)}
    cert_path = get_ca_cert_path(CONFIG)
    if cert_path:
      bstack1lll1lllll_opy_[bstack1l1llll_opy_ (u"ࠩࡹࡩࡷ࡯ࡦࡺࠩᙄ")] = cert_path
    response = requests.get(url, **bstack1lll1lllll_opy_)
    if response.json():
      cli.add_benchmark(bstack1l1llll_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻ࡩࡨࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡹ࡟࡭࡫ࡶࡸࠧᙅ"), datetime.datetime.now() - time_start)
      return list(map(lambda session: session[bstack1l1llll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩᙆ")], response.json()))
  except Exception as e:
    logger.debug(bstack1ll1l11111_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack1ll111l1l1_opy_, stage=STAGE.SINGLE, bstack11lllll111_opy_=SESSION_NAME)
def get_build_link():
  global CONFIG
  global bstack1lll1l11l1l_opy_
  try:
    if bstack1l1llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᙇ") in CONFIG:
      time_start = datetime.datetime.now()
      host = bstack1l1llll_opy_ (u"࠭ࡡࡱ࡫࠰ࡧࡱࡵࡵࡥࠩᙈ") if bstack1l1llll_opy_ (u"ࠧࡢࡲࡳࠫᙉ") in CONFIG else bstack1l1llll_opy_ (u"ࠨࡣࡳ࡭ࠬᙊ")
      user = CONFIG[bstack1l1llll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᙋ")]
      key = CONFIG[bstack1l1llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᙌ")]
      bstack1lllllll1ll_opy_ = bstack1l1llll_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪᙍ") if bstack1l1llll_opy_ (u"ࠬࡧࡰࡱࠩᙎ") in CONFIG else bstack1l1llll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨᙏ")
      url = bstack1l1llll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡽࢀ࠾ࢀࢃࡀࡼࡿ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠰࡭ࡷࡴࡴࠧᙐ").format(user, key, host, bstack1lllllll1ll_opy_)
      if cli.is_enabled(CONFIG):
        bstack11111ll1l_opy_, hashed_id = cli.bstack1ll1ll1ll1_opy_()
        logger.info(bstack1lll1l1lll1_opy_.format(bstack11111ll1l_opy_))
        return [hashed_id, bstack11111ll1l_opy_]
      else:
        headers = {
          bstack1l1llll_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧᙑ"): bstack1l1llll_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬᙒ"),
        }
        if bstack1l1llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᙓ") in CONFIG:
          params = {bstack1l1llll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᙔ"): CONFIG[bstack1l1llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᙕ")], bstack1l1llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᙖ"): CONFIG[bstack1l1llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᙗ")]}
        else:
          params = {bstack1l1llll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᙘ"): CONFIG[bstack1l1llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬᙙ")]}
        proxies = bstack1ll11l111l1_opy_(CONFIG, url)
        from bstack_utils.helper import get_ca_cert_path
        bstack1l11lll1l1_opy_ = {bstack1l1llll_opy_ (u"ࠪࡴࡦࡸࡡ࡮ࡵࠪᙚ"): params, bstack1l1llll_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᙛ"): headers, bstack1l1llll_opy_ (u"ࠬࡶࡲࡰࡺ࡬ࡩࡸ࠭ᙜ"): proxies}
        cert_path = get_ca_cert_path(CONFIG)
        if cert_path:
          bstack1l11lll1l1_opy_[bstack1l1llll_opy_ (u"࠭ࡶࡦࡴ࡬ࡪࡾ࠭ᙝ")] = cert_path
        response = requests.get(url, **bstack1l11lll1l1_opy_)
        if response.json():
          bstack1llll1111l_opy_ = response.json()[0][bstack1l1llll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡧࡻࡩ࡭ࡦࠪᙞ")]
          if bstack1llll1111l_opy_:
            bstack11111ll1l_opy_ = bstack1llll1111l_opy_[bstack1l1llll_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣࡠࡷࡵࡰࠬᙟ")].split(bstack1l1llll_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤ࠯ࡥࡹ࡮ࡲࡤࠨᙠ"))[0] + bstack1l1llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡵ࠲ࠫᙡ") + bstack1llll1111l_opy_[
              bstack1l1llll_opy_ (u"ࠫ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧᙢ")]
            logger.info(bstack1lll1l1lll1_opy_.format(bstack11111ll1l_opy_))
            bstack1lll1l11l1l_opy_ = bstack1llll1111l_opy_[bstack1l1llll_opy_ (u"ࠬ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᙣ")]
            bstack1ll1llllll1_opy_ = CONFIG[bstack1l1llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᙤ")]
            if bstack1l1llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᙥ") in CONFIG:
              bstack1ll1llllll1_opy_ += bstack1l1llll_opy_ (u"ࠨࠢࠪᙦ") + CONFIG[bstack1l1llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᙧ")]
            if bstack1ll1llllll1_opy_ != bstack1llll1111l_opy_[bstack1l1llll_opy_ (u"ࠪࡲࡦࡳࡥࠨᙨ")]:
              logger.debug(bstack111lll1lll_opy_.format(bstack1llll1111l_opy_[bstack1l1llll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᙩ")], bstack1ll1llllll1_opy_))
            cli.add_benchmark(bstack1l1llll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࡫ࡪࡺ࡟ࡣࡷ࡬ࡰࡩࡥ࡬ࡪࡰ࡮ࠦᙪ"), datetime.datetime.now() - time_start)
            return [bstack1llll1111l_opy_[bstack1l1llll_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᙫ")], bstack11111ll1l_opy_]
    else:
      logger.warning(bstack1l1l11l1lll_opy_)
  except Exception as e:
    logger.debug(bstack1lll11lll1_opy_.format(str(e)))
  return [None, None]
def bstack1l1l1llll1l_opy_(url, bstack1lll1l1l11_opy_=False):
  global CONFIG
  global bstack1lll111ll1_opy_
  if not bstack1lll111ll1_opy_:
    hostname = bstack11l1ll1l11_opy_(url)
    is_private = bstack1lllll11ll1_opy_(hostname)
    if (bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᙬ") in CONFIG and not bstack11lll11l1l_opy_(CONFIG[bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ᙭")])) and (is_private or bstack1lll1l1l11_opy_):
      bstack1lll111ll1_opy_ = hostname
def bstack11l1ll1l11_opy_(url):
  return urlparse(url).hostname
def bstack1lllll11ll1_opy_(hostname):
  for bstack1l1l1l1l1l1_opy_ in bstack1l1l111lll1_opy_:
    regex = re.compile(bstack1l1l1l1l1l1_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1l1ll1l1l1l_opy_(bstack1lll1llllll_opy_):
  return True if bstack1lll1llllll_opy_ in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack1l11l111l1_opy_, stage=STAGE.SINGLE, bstack11lllll111_opy_=SESSION_NAME)
def getAccessibilityResults(driver):
  global CONFIG
  global PLATFORM_INDEX
  bstack111llll11l_opy_ = not (bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭᙮"), None) and bstack11llll11_opy_(
          threading.current_thread(), bstack1l1llll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᙯ"), None))
  bstack1l1ll111ll_opy_ = getattr(driver, bstack1l1llll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫᙰ"), None) != True
  bstack1ll1111111_opy_ = bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠬ࡯ࡳࡂࡲࡳࡅ࠶࠷ࡹࡕࡧࡶࡸࠬᙱ"), None) and bstack11llll11_opy_(
          threading.current_thread(), bstack1l1llll_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᙲ"), None)
  if bstack1ll1111111_opy_:
    if not bstack1l111l1111_opy_():
      logger.warning(bstack1l1llll_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡲࡳࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡪࡺࡲࡪࡧࡹࡩࠥࡇࡰࡱࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵ࠱ࠦᙳ"))
      return {}
    logger.debug(bstack1l1llll_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠬᙴ"))
    logger.debug(perform_scan(driver, driver_command=bstack1l1llll_opy_ (u"ࠩࡨࡼࡪࡩࡵࡵࡧࡖࡧࡷ࡯ࡰࡵࠩᙵ")))
    results = bstack11lll111l1_opy_(bstack1l1llll_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡶࠦᙶ"))
    if results is not None and results.get(bstack1l1llll_opy_ (u"ࠦ࡮ࡹࡳࡶࡧࡶࠦᙷ")) is not None:
        return results[bstack1l1llll_opy_ (u"ࠧ࡯ࡳࡴࡷࡨࡷࠧᙸ")]
    logger.error(bstack1l1llll_opy_ (u"ࠨࡎࡰࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡕࡩࡸࡻ࡬ࡵࡵࠣࡻࡪࡸࡥࠡࡨࡲࡹࡳࡪ࠮ࠣᙹ"))
    return []
  if not a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX) or (bstack1l1ll111ll_opy_ and bstack111llll11l_opy_):
    logger.warning(bstack1l1llll_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴ࠰ࠥᙺ"))
    return {}
  try:
    logger.debug(bstack1l1llll_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠬᙻ"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(accessibility_scripts.get_results)
    return results
  except Exception:
    logger.error(bstack1l1llll_opy_ (u"ࠤࡑࡳࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡷࡦࡴࡨࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦᙼ"))
    return {}
@measure(event_name=EVENTS.bstack11l111111l_opy_, stage=STAGE.SINGLE, bstack11lllll111_opy_=SESSION_NAME)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global PLATFORM_INDEX
  bstack111llll11l_opy_ = not (bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧᙽ"), None) and bstack11llll11_opy_(
          threading.current_thread(), bstack1l1llll_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᙾ"), None))
  bstack1l1ll111ll_opy_ = getattr(driver, bstack1l1llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬᙿ"), None) != True
  bstack1ll1111111_opy_ = bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ "), None) and bstack11llll11_opy_(
          threading.current_thread(), bstack1l1llll_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᚁ"), None)
  if bstack1ll1111111_opy_:
    if not bstack1l111l1111_opy_():
      logger.warning(bstack1l1llll_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡳࡴࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡸࡻ࡭࡮ࡣࡵࡽ࠳ࠨᚂ"))
      return {}
    logger.debug(bstack1l1llll_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡳࡶ࡯ࡰࡥࡷࡿࠧᚃ"))
    logger.debug(perform_scan(driver, driver_command=bstack1l1llll_opy_ (u"ࠪࡩࡽ࡫ࡣࡶࡶࡨࡗࡨࡸࡩࡱࡶࠪᚄ")))
    results = bstack11lll111l1_opy_(bstack1l1llll_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷࡗࡺࡳ࡭ࡢࡴࡼࠦᚅ"))
    if results is not None and results.get(bstack1l1llll_opy_ (u"ࠧࡹࡵ࡮࡯ࡤࡶࡾࠨᚆ")) is not None:
        return results[bstack1l1llll_opy_ (u"ࠨࡳࡶ࡯ࡰࡥࡷࡿࠢᚇ")]
    logger.error(bstack1l1llll_opy_ (u"ࠢࡏࡱࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡖࡪࡹࡵ࡭ࡶࡶࠤࡘࡻ࡭࡮ࡣࡵࡽࠥࡽࡡࡴࠢࡩࡳࡺࡴࡤ࠯ࠤᚈ"))
    return {}
  if not a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX) or (bstack1l1ll111ll_opy_ and bstack111llll11l_opy_):
    logger.warning(bstack1l1llll_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡷࡺࡳ࡭ࡢࡴࡼ࠲ࠧᚉ"))
    return {}
  try:
    logger.debug(bstack1l1llll_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡳࡶ࡯ࡰࡥࡷࡿࠧᚊ"))
    logger.debug(perform_scan(driver))
    bstack1111l1ll1l_opy_ = driver.execute_async_script(accessibility_scripts.get_results_summary)
    return bstack1111l1ll1l_opy_
  except Exception:
    logger.error(bstack1l1llll_opy_ (u"ࠥࡒࡴࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡶ࡯ࡰࡥࡷࡿࠠࡸࡣࡶࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦᚋ"))
    return {}
def bstack1l111l1111_opy_():
  global CONFIG
  global PLATFORM_INDEX
  bstack1llll1111l1_opy_ = bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫᚌ"), None) and bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᚍ"), None)
  if not a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX) or not bstack1llll1111l1_opy_:
        logger.warning(bstack1l1llll_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡷ࡫ࡳࡶ࡮ࡷࡷ࠳ࠨᚎ"))
        return False
  return True
def bstack11lll111l1_opy_(result_type):
    test_run_uuid = TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack1ll111ll_opy_.current_hook_uuid()
    with ThreadPoolExecutor() as executor:
        future = executor.submit(bstack11l1ll1l1l_opy_(test_run_uuid, result_type))
        try:
            return future.result(timeout=bstack1ll1llll1l1_opy_)
        except TimeoutError:
            logger.error(bstack1l1llll_opy_ (u"ࠢࡕ࡫ࡰࡩࡴࡻࡴࠡࡣࡩࡸࡪࡸࠠࡼࡿࡶࠤࡼ࡮ࡩ࡭ࡧࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡘࡥࡴࡷ࡯ࡸࡸࠨᚏ").format(bstack1ll1llll1l1_opy_))
        except Exception as ex:
            logger.debug(bstack1l1llll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡳࡧࡷࡶ࡮࡫ࡶࡪࡰࡪࠤࡆࡶࡰࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࢁࡽ࠯ࠢࡈࡶࡷࡵࡲࠡ࠯ࠣࡿࢂࠨᚐ").format(result_type, str(ex)))
    return {}
@measure(event_name=EVENTS.bstack11l111llll_opy_, stage=STAGE.SINGLE, bstack11lllll111_opy_=SESSION_NAME)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global PLATFORM_INDEX
  bstack111llll11l_opy_ = not (bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ᚑ"), None) and bstack11llll11_opy_(
          threading.current_thread(), bstack1l1llll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᚒ"), None))
  bstack1l1llll11l_opy_ = not (bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫᚓ"), None) and bstack11llll11_opy_(
          threading.current_thread(), bstack1l1llll_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᚔ"), None))
  bstack1l1ll111ll_opy_ = getattr(driver, bstack1l1llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭ᚕ"), None) != True
  if not a11y.is_enabled_platform(CONFIG, PLATFORM_INDEX) or (bstack1l1ll111ll_opy_ and bstack111llll11l_opy_ and bstack1l1llll11l_opy_):
    logger.warning(bstack1l1llll_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡶࡰࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮࠯ࠤᚖ"))
    return {}
  try:
    bstack1l1lll11l1_opy_ = bstack1l1llll_opy_ (u"ࠨࡣࡳࡴࠬᚗ") in CONFIG and CONFIG.get(bstack1l1llll_opy_ (u"ࠩࡤࡴࡵ࠭ᚘ"), bstack1l1llll_opy_ (u"ࠪࠫᚙ"))
    session_id = getattr(driver, bstack1l1llll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨᚚ"), None)
    if not session_id:
      logger.warning(bstack1l1llll_opy_ (u"ࠧࡔ࡯ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡌࡈࠥ࡬࡯ࡶࡰࡧࠤ࡫ࡵࡲࠡࡦࡵ࡭ࡻ࡫ࡲࠣ᚛"))
      return {bstack1l1llll_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ᚜"): bstack1l1llll_opy_ (u"ࠢࡏࡱࠣࡷࡪࡹࡳࡪࡱࡱࠤࡎࡊࠠࡧࡱࡸࡲࡩࠨ᚝")}
    if bstack1l1lll11l1_opy_:
      try:
        bstack1ll1l1ll111_opy_ = {
              bstack1l1llll_opy_ (u"ࠨࡶ࡫ࡎࡼࡺࡔࡰ࡭ࡨࡲࠬ᚞"): os.environ.get(bstack1l1llll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ᚟"), os.environ.get(bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᚠ"), bstack1l1llll_opy_ (u"ࠫࠬᚡ"))),
              bstack1l1llll_opy_ (u"ࠬࡺࡨࡕࡧࡶࡸࡗࡻ࡮ࡖࡷ࡬ࡨࠬᚢ"): TestHubHandler.current_test_uuid() if TestHubHandler.current_test_uuid() else bstack1ll111ll_opy_.current_hook_uuid(),
              bstack1l1llll_opy_ (u"࠭ࡡࡶࡶ࡫ࡌࡪࡧࡤࡦࡴࠪᚣ"): os.environ.get(bstack1l1llll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᚤ")),
              bstack1l1llll_opy_ (u"ࠨࡵࡦࡥࡳ࡚ࡩ࡮ࡧࡶࡸࡦࡳࡰࠨᚥ"): str(int(datetime.datetime.now().timestamp() * 1000)),
              bstack1l1llll_opy_ (u"ࠩࡷ࡬ࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧᚦ"): os.environ.get(bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᚧ"), bstack1l1llll_opy_ (u"ࠫࠬᚨ")),
              bstack1l1llll_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬᚩ"): kwargs.get(bstack1l1llll_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡣࡰ࡯ࡰࡥࡳࡪࠧᚪ"), None) or bstack1l1llll_opy_ (u"ࠧࠨᚫ")
          }
        if not hasattr(thread_local, bstack1l1llll_opy_ (u"ࠨࡤࡤࡷࡪࡥࡡࡱࡲࡢࡥ࠶࠷ࡹࡠࡵࡦࡶ࡮ࡶࡴࠨᚬ")):
            scripts = {bstack1l1llll_opy_ (u"ࠩࡶࡧࡦࡴࠧᚭ"): accessibility_scripts.perform_scan}
            thread_local.base_app_a11y_script = scripts
        bstack1llll1llll_opy_ = copy.deepcopy(thread_local.base_app_a11y_script)
        bstack1llll1llll_opy_[bstack1l1llll_opy_ (u"ࠪࡷࡨࡧ࡮ࠨᚮ")] = bstack1llll1llll_opy_[bstack1l1llll_opy_ (u"ࠫࡸࡩࡡ࡯ࠩᚯ")] % json.dumps(bstack1ll1l1ll111_opy_)
        accessibility_scripts.bstack1ll1l1ll1l_opy_(bstack1llll1llll_opy_)
        accessibility_scripts.store()
        bstack1ll11l1ll1l_opy_ = driver.execute_script(accessibility_scripts.perform_scan)
      except Exception as bstack1lllll11ll_opy_:
        logger.info(bstack1l1llll_opy_ (u"ࠧࡇࡰࡱ࡫ࡸࡱࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡣࡢࡰࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࠧᚰ") + str(bstack1lllll11ll_opy_))
        bstack1ll11l1ll1l_opy_ = {bstack1l1llll_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧᚱ"): str(bstack1lllll11ll_opy_)}
    else:
      bstack1ll11l1ll1l_opy_ = driver.execute_async_script(accessibility_scripts.perform_scan, {bstack1l1llll_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪࠧᚲ"): kwargs.get(bstack1l1llll_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࡠࡥࡲࡱࡲࡧ࡮ࡥࠩᚳ"), None) or bstack1l1llll_opy_ (u"ࠩࠪᚴ")})
    return bstack1ll11l1ll1l_opy_
  except Exception as err:
    logger.error(bstack1l1llll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡲࡶࡰࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮࠯ࠢࡾࢁࠧᚵ").format(str(err)))
    return {}
def bstack1lll1l11lll_opy_(bstack1l11l1l1l_opy_):
  bstack1l1llll_opy_ (u"ࠦࠧࠨࡉ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡧࠣࡸ࡭࡫ࠠࡔࡆࡎࠤ࡫ࡵࡲࠡࡋࡇࡉ࠲ࡴࡡࡵ࡫ࡹࡩࠥࡶࡹࡵࡧࡶࡸࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠡࠪࡓࡽࡈ࡮ࡡࡳ࡯ࠬ࠲ࠏࠦࠠࡇࡣ࡮ࡩࡸࠦࡳࡺࡵ࠱ࡥࡷ࡭ࡶࠡࡶࡲࠤࡱࡵ࡯࡬ࠢ࡯࡭ࡰ࡫ࠠࡢࠢࡆࡐࡎࠦࡷࡳࡣࡳࡴࡪࡸࠠࡪࡰࡹࡳࡨࡧࡴࡪࡱࡱ࠰ࠥࡺࡨࡦࡰࠣࡧࡦࡲ࡬ࡴࠌࠣࠤࡷࡻ࡮ࡠࡱࡱࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠫ࠭ࠥࡹ࡯ࠡࡶ࡫ࡩࠥࡋࡘࡂࡅࡗࠤࡸࡧ࡭ࡦࠢࡦࡳࡩ࡫ࠠࡱࡣࡷ࡬ࠥࡸࡵ࡯ࡵ࠱ࠤ࡙࡮ࡥࠡࡱࡱࡰࡾࠐࠠࠡࡦ࡬ࡪ࡫࡫ࡲࡦࡰࡦࡩ࠿ࠦࡐࡺࡶࡨࡷࡹࡎࡡ࡯ࡦ࡯ࡩࡷ࠴ࡳࡵࡣࡵࡸࡤࡺࡥࡴࡶࡶࠬ࠮ࠦࡩࡴࠢࡱࡳࡹࠦࡣࡢ࡮࡯ࡩࡩࠦࡢࡦࡥࡤࡹࡸ࡫ࠊࠡࠢࡳࡽࡹ࡫ࡳࡵࠢ࡬ࡷࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡲࡶࡰࡱ࡭ࡳ࡭࠮ࠋࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࡥࡲࡲ࡫࡯ࡧࡠࡲࡤࡸ࡭ࡀࠠࡂࡤࡶࡳࡱࡻࡴࡦࠢࡳࡥࡹ࡮ࠠࡵࡱࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱࠦ࡯ࡳࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡤࡱࡱ࠴ࠊࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࡘࡷࡻࡥࠡ࡫ࡩࠤ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡡࡵ࡫ࡲࡲࠥࡹࡵࡤࡥࡨࡩࡩ࡫ࡤ࠭ࠢࡉࡥࡱࡹࡥࠡࡱࡷ࡬ࡪࡸࡷࡪࡵࡨ࠲ࠏࠦࠠࠣࠤࠥᚶ")
  try:
    try:
      import selenium
      cli.session_framework = bstack1l1llll_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢᚷ")
    except ImportError:
      try:
        import playwright
        cli.session_framework = bstack1l1llll_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᚸ")
      except ImportError:
        pass
    bstack11ll11ll11_opy_ = sys.argv[:]
    sys.argv = [bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡳࡥ࡭ࠪᚹ"), bstack1l1llll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᚺ")]
    os.environ[bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡇࡉࡤࡖࡌࡖࡉࡌࡒࡤࡓࡏࡅࡇࠪᚻ")] = bstack1l1llll_opy_ (u"ࠪ࠵ࠬᚼ")
    os.environ[bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨᚽ")] = bstack1l11l1l1l_opy_
    try:
      run_on_browserstack()
    finally:
      sys.argv = bstack11ll11ll11_opy_
    return cli.is_running()
  except Exception as e:
    logger.error(bstack1l1llll_opy_ (u"ࠧࡏࡄࡆ࠯ࡱࡥࡹ࡯ࡶࡦࠢࡳࡰࡺ࡭ࡩ࡯ࠢ࡬ࡲ࡮ࡺࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡽࢀࠦᚾ").format(str(e)))
    logger.debug(traceback.format_exc())
    return False