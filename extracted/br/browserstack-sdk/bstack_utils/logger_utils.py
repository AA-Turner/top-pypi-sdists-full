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
import sys
import logging
import tarfile
import io
import os
import time
import requests
import re
import threading
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack111ll1l1l1l_opy_, EVENTS, bstack111ll1llll1_opy_, bstack111llll1l1l_opy_, STAGE
import tempfile
import json
bstack11111ll1111_opy_ = os.getenv(bstack11l1l11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡉࡢࡊࡎࡒࡅࠣῩ"), None) or os.path.join(tempfile.gettempdir(), bstack11l1l11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡥࡧࡥࡹ࡬࠴࡬ࡰࡩࠥῪ"))
bstack11111l11111_opy_ = os.path.join(bstack11l1l11_opy_ (u"ࠤ࡯ࡳ࡬ࠨΎ"), bstack11l1l11_opy_ (u"ࠪࡷࡩࡱ࠭ࡤ࡮࡬࠱ࡩ࡫ࡢࡶࡩ࠱ࡰࡴ࡭ࠧῬ"))
_11111l11ll1_opy_ = threading.Lock()
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack11l1l11_opy_ (u"ࠫࠪ࠮ࡡࡴࡥࡷ࡭ࡲ࡫ࠩࡴࠢ࡞ࠩ࠭ࡴࡡ࡮ࡧࠬࡷࡢࡡࠥࠩ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨ࠭ࡸࡣࠠ࠮ࠢࠨࠬࡲ࡫ࡳࡴࡣࡪࡩ࠮ࡹࠧ῭"),
      datefmt=bstack11l1l11_opy_ (u"࡙ࠬࠫ࠮ࠧࡰ࠱ࠪࡪࡔࠦࡊ࠽ࠩࡒࡀࠥࡔ࡜ࠪ΅"),
      stream=sys.stdout
    )
  return logger
def bstack1lll1lll_opy_(name=__name__, level=logging.DEBUG):
  bstack11l1l11_opy_ (u"ࠨࠢࠣࠌࠣࠤࡗ࡫ࡴࡶࡴࡱࡷࠥࡧࠠ࡭ࡱࡪ࡫ࡪࡸࠠࡵࡪࡤࡸࠥࡽࡲࡪࡶࡨࡷࠥࡵ࡮࡭ࡻࠣࡸࡴࠦࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠱ࡰࡴ࡭ࠠࡧ࡫࡯ࡩࠏࠦࠠࡄࡴࡨࡥࡹ࡫ࡳࠡࡣࡱࡨࠥࡳࡡ࡯ࡣࡪࡩࡸࠦࡩࡵࡵࠣࡳࡼࡴࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤ࡫࡯࡬ࡦࠢ࡫ࡥࡳࡪ࡬ࡦࡴࠍࠤࠥࡕ࡮࡭ࡻࠣࡩࡳࡧࡢ࡭ࡧࡶࠤࡱࡵࡧࡨ࡫ࡱ࡫ࠥ࡯ࡦࠡࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࡣࡑࡕࡇࡔࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠢ࡬ࡷࠥࡹࡥࡵࠢࡷࡳࠥࡧࠠࡵࡴࡸࡸ࡭ࡿࠠࡷࡣ࡯ࡹࡪࠐࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࡳࡧ࡭ࡦ࠼ࠣࡐࡴ࡭ࡧࡦࡴࠣࡲࡦࡳࡥࠡࠪࡧࡩ࡫ࡧࡵ࡭ࡶࡶࠤࡹࡵࠠࡠࡡࡱࡥࡲ࡫࡟ࡠࠫࠍࠤࠥࠦࠠ࡭ࡧࡹࡩࡱࡀࠠࡍࡱࡪ࡫࡮ࡴࡧࠡ࡮ࡨࡺࡪࡲࠠࠩࡦࡨࡪࡦࡻ࡬ࡵࡵࠣࡸࡴࠦࡄࡆࡄࡘࡋ࠮ࠐࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠ࡭ࡱࡪ࡫࡮ࡴࡧ࠯ࡎࡲ࡫࡬࡫ࡲ࠻ࠢࡆࡳࡳ࡬ࡩࡨࡷࡵࡩࡩࠦ࡬ࡰࡩࡪࡩࡷࠦࡴࡩࡣࡷࠤࡼࡸࡩࡵࡧࡶࠤࡴࡴ࡬ࡺࠢࡷࡳࠥࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠰࡯ࡳ࡬ࠦࠨࡪࡨࠣࡩࡳࡧࡢ࡭ࡧࡧ࠭ࠏࠦࠠࠣࠤࠥ`")
  logger_name = bstack11l1l11_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠲ࢀ࠶ࡽࠣ῰").format(name)
  logger = logging.getLogger(logger_name)
  is_enabled = os.getenv(bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࡣࡑࡕࡇࡔࠩ῱"), bstack11l1l11_opy_ (u"ࠩࠪῲ")).lower() == bstack11l1l11_opy_ (u"ࠪࡸࡷࡻࡥࠨῳ")
  if not is_enabled:
    logger.setLevel(logging.CRITICAL)
    logger.propagate = False
    return logger
  with _11111l11ll1_opy_:
    if logger.handlers:
      return logger
    bstack11111l1ll1l_opy_ = os.path.join(os.getcwd(), bstack11l1l11_opy_ (u"ࠫࡱࡵࡧࠨῴ"), bstack11l1l11_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠰࡯ࡳ࡬࠭῵"))
    log_dir = os.path.dirname(bstack11111l1ll1l_opy_)
    if not os.path.exists(log_dir):
      os.makedirs(log_dir)
    bstack11111ll111l_opy_ = logging.FileHandler(bstack11111l1ll1l_opy_)
    bstack11111l11l11_opy_ = logging.Formatter(
      fmt=bstack11l1l11_opy_ (u"࠭ࠥࠩࡣࡶࡧࡹ࡯࡭ࡦࠫࡶࠤࡠࠫࠨ࡯ࡣࡰࡩ࠮ࡹ࡝࡜ࠧࠫࡰࡪࡼࡥ࡭ࡰࡤࡱࡪ࠯ࡳ࡞ࠢ࠰ࠤࡠࠦࡓࡅࡍ࠰ࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠠ࡞ࠢࠨࠬࡲ࡫ࡳࡴࡣࡪࡩ࠮ࡹࠧῶ"),
      datefmt=bstack11l1l11_opy_ (u"࡛ࠧࠦ࠰ࠩࡲ࠳ࠥࡥࡖࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࡞ࠬῷ"),
    )
    bstack11111ll111l_opy_.setFormatter(bstack11111l11l11_opy_)
    bstack11111ll111l_opy_.setLevel(level)
    bstack11111ll111l_opy_.addFilter(lambda r: r.name != bstack11l1l11_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷ࠴ࡲࡦ࡯ࡲࡸࡪ࠴ࡲࡦ࡯ࡲࡸࡪࡥࡣࡰࡰࡱࡩࡨࡺࡩࡰࡰࠪῸ"))
    logger.addHandler(bstack11111ll111l_opy_)
    logger.setLevel(level)
    logger.propagate = False
  return logger
def bstack1ll1111l11l_opy_():
  bstack11111l111ll_opy_ = os.environ.get(bstack11l1l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡆࡈࡆ࡚ࡍࠢΌ"), bstack11l1l11_opy_ (u"ࠥࡪࡦࡲࡳࡦࠤῺ"))
  return logging.DEBUG if bstack11111l111ll_opy_.lower() == bstack11l1l11_opy_ (u"ࠦࡹࡸࡵࡦࠤΏ") else logging.INFO
def bstack1l11l1ll1l1_opy_():
  global bstack11111ll1111_opy_
  if os.path.exists(bstack11111ll1111_opy_):
    os.remove(bstack11111ll1111_opy_)
  if os.path.exists(bstack11111l11111_opy_):
    os.remove(bstack11111l11111_opy_)
def bstack1l1ll11l1_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def configure_logger(config, log_level):
  bstack111111lll11_opy_ = log_level
  if bstack11l1l11_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧῼ") in config and config[bstack11l1l11_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨ´")] in bstack111ll1llll1_opy_:
    bstack111111lll11_opy_ = bstack111ll1llll1_opy_[config[bstack11l1l11_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩ῾")]]
  if config.get(bstack11l1l11_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪ῿"), False):
    logging.getLogger().setLevel(bstack111111lll11_opy_)
    return bstack111111lll11_opy_
  global bstack11111ll1111_opy_
  bstack1l1ll11l1_opy_()
  bstack11111l111l1_opy_ = logging.Formatter(
    fmt=bstack11l1l11_opy_ (u"ࠩࠨࠬࡦࡹࡣࡵ࡫ࡰࡩ࠮ࡹࠠ࡜ࠧࠫࡲࡦࡳࡥࠪࡵࡠ࡟ࠪ࠮࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠫࡶࡡࠥ࠳ࠠࠦࠪࡰࡩࡸࡹࡡࡨࡧࠬࡷࠬ "),
    datefmt=bstack11l1l11_opy_ (u"ࠪࠩ࡞࠳ࠥ࡮࠯ࠨࡨ࡙ࠫࡈ࠻ࠧࡐ࠾࡙࡚ࠪࠨ "),
  )
  bstack11111ll1l11_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack11111ll1111_opy_)
  file_handler.setFormatter(bstack11111l111l1_opy_)
  bstack11111ll1l11_opy_.setFormatter(bstack11111l111l1_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack11111ll1l11_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack11l1l11_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳ࠰ࡵࡩࡲࡵࡴࡦ࠰ࡵࡩࡲࡵࡴࡦࡡࡦࡳࡳࡴࡥࡤࡶ࡬ࡳࡳ࠭ "))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack11111ll1l11_opy_.setLevel(bstack111111lll11_opy_)
  logging.getLogger().addHandler(bstack11111ll1l11_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack111111lll11_opy_
def bstack11111l1111l_opy_(config):
  try:
    bstack11111l1ll11_opy_ = set(bstack111llll1l1l_opy_)
    bstack111111lllll_opy_ = bstack11l1l11_opy_ (u"ࠬ࠭ ")
    with open(bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩ ")) as bstack111111lll1l_opy_:
      bstack11111l1lll1_opy_ = bstack111111lll1l_opy_.read()
      bstack111111lllll_opy_ = re.sub(bstack11l1l11_opy_ (u"ࡲࠨࡠࠫࡠࡸ࠱ࠩࡀࠥ࠱࠮ࠩࡢ࡮ࠨ "), bstack11l1l11_opy_ (u"ࠨࠩ "), bstack11111l1lll1_opy_, flags=re.M)
      bstack111111lllll_opy_ = re.sub(
        bstack11l1l11_opy_ (u"ࡴࠪࡢ࠭ࡢࡳࠬࠫࡂࠬࠬ ") + bstack11l1l11_opy_ (u"ࠪࢀࠬ ").join(bstack11111l1ll11_opy_) + bstack11l1l11_opy_ (u"ࠫ࠮࠴ࠪࠥࠩ "),
        bstack11l1l11_opy_ (u"ࡷ࠭࡜࠳࠼ࠣ࡟ࡗࡋࡄࡂࡅࡗࡉࡉࡣࠧ "),
        bstack111111lllll_opy_, flags=re.M | re.I
      )
    def bstack11111l1l1ll_opy_(dic):
      bstack11111l1llll_opy_ = {}
      for key, value in dic.items():
        if key in bstack11111l1ll11_opy_:
          bstack11111l1llll_opy_[key] = bstack11l1l11_opy_ (u"࡛࠭ࡓࡇࡇࡅࡈ࡚ࡅࡅ࡟ࠪ​")
        else:
          if isinstance(value, dict):
            bstack11111l1llll_opy_[key] = bstack11111l1l1ll_opy_(value)
          else:
            bstack11111l1llll_opy_[key] = value
      return bstack11111l1llll_opy_
    bstack11111l1llll_opy_ = bstack11111l1l1ll_opy_(config)
    return {
      bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪ‌"): bstack111111lllll_opy_,
      bstack11l1l11_opy_ (u"ࠨࡨ࡬ࡲࡦࡲࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫ‍"): json.dumps(bstack11111l1llll_opy_)
    }
  except Exception as e:
    return {}
def bstack11111l1l1l1_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack11l1l11_opy_ (u"ࠩ࡯ࡳ࡬࠭‎"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack1llllll111l_opy_ = os.path.join(log_dir, bstack11l1l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶࠫ‏"))
  if not os.path.exists(bstack1llllll111l_opy_):
    bstack11111ll11ll_opy_ = {
      bstack11l1l11_opy_ (u"ࠦ࡮ࡴࡩࡱࡣࡷ࡬ࠧ‐"): str(inipath),
      bstack11l1l11_opy_ (u"ࠧࡸ࡯ࡰࡶࡳࡥࡹ࡮ࠢ‑"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack11l1l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡣࡰࡰࡩ࡭࡬ࡹ࠮࡫ࡵࡲࡲࠬ‒")), bstack11l1l11_opy_ (u"ࠧࡸࠩ–")) as bstack11111l11l1l_opy_:
      bstack11111l11l1l_opy_.write(json.dumps(bstack11111ll11ll_opy_))
def bstack11111l1l111_opy_():
  try:
    bstack1llllll111l_opy_ = os.path.join(os.getcwd(), bstack11l1l11_opy_ (u"ࠨ࡮ࡲ࡫ࠬ—"), bstack11l1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡦࡳࡳ࡬ࡩࡨࡵ࠱࡮ࡸࡵ࡮ࠨ―"))
    if os.path.exists(bstack1llllll111l_opy_):
      with open(bstack1llllll111l_opy_, bstack11l1l11_opy_ (u"ࠪࡶࠬ‖")) as bstack11111l11l1l_opy_:
        bstack111111llll1_opy_ = json.load(bstack11111l11l1l_opy_)
      return bstack111111llll1_opy_.get(bstack11l1l11_opy_ (u"ࠫ࡮ࡴࡩࡱࡣࡷ࡬ࠬ‗"), bstack11l1l11_opy_ (u"ࠬ࠭‘")), bstack111111llll1_opy_.get(bstack11l1l11_opy_ (u"࠭ࡲࡰࡱࡷࡴࡦࡺࡨࠨ’"), bstack11l1l11_opy_ (u"ࠧࠨ‚"))
  except:
    pass
  return None, None
def bstack11111ll11l1_opy_():
  try:
    bstack1llllll111l_opy_ = os.path.join(os.getcwd(), bstack11l1l11_opy_ (u"ࠨ࡮ࡲ࡫ࠬ‛"), bstack11l1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡦࡳࡳ࡬ࡩࡨࡵ࠱࡮ࡸࡵ࡮ࠨ“"))
    if os.path.exists(bstack1llllll111l_opy_):
      os.remove(bstack1llllll111l_opy_)
  except:
    pass
def bstack1l111ll1_opy_(config):
  try:
    try:
      from bstack_utils.bstack111lll111l_opy_ import bstack11ll1l1l1_opy_
    except Exception:
      bstack11ll1l1l1_opy_ = None
    start_time = time.time()
    from bstack_utils.helper import global_config, bstack1ll11l1l11_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack11111ll1111_opy_
    if config.get(bstack11l1l11_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬ”"), False):
      return
    uuid = os.getenv(bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ„")) if os.getenv(bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ‟")) else global_config.get_property(bstack11l1l11_opy_ (u"ࠨࡳࡥ࡭ࡕࡹࡳࡏࡤࠣ†"))
    if not uuid or uuid == bstack11l1l11_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ‡"):
      return
    bstack11111ll1l1l_opy_ = bstack11ll1l1l1_opy_.bstack1l11l111ll_opy_(EVENTS.bstack111lllll1l1_opy_.value) if bstack11ll1l1l1_opy_ else None
    bstack11111l11lll_opy_ = [bstack11l1l11_opy_ (u"ࠨࡴࡨࡵࡺ࡯ࡲࡦ࡯ࡨࡲࡹࡹ࠮ࡵࡺࡷࠫ•"), bstack11l1l11_opy_ (u"ࠩࡓ࡭ࡵ࡬ࡩ࡭ࡧࠪ‣"), bstack11l1l11_opy_ (u"ࠪࡴࡾࡶࡲࡰ࡬ࡨࡧࡹ࠴ࡴࡰ࡯࡯ࠫ․"), bstack11111ll1111_opy_, bstack11111l11111_opy_]
    bstack11111ll1ll1_opy_, root_path = bstack11111l1l111_opy_()
    if bstack11111ll1ll1_opy_ != None:
      bstack11111l11lll_opy_.append(bstack11111ll1ll1_opy_)
    if root_path != None:
      bstack11111l11lll_opy_.append(os.path.join(root_path, bstack11l1l11_opy_ (u"ࠫࡨࡵ࡮ࡧࡶࡨࡷࡹ࠴ࡰࡺࠩ‥")))
    bstack111111ll1ll_opy_ = os.path.join(os.getcwd(), bstack11l1l11_opy_ (u"ࠬࡲ࡯ࡨࠩ…"), bstack11l1l11_opy_ (u"࠭࡫ࡦࡻ࠰ࡱࡪࡺࡲࡪࡥࡶ࠲࡯ࡹ࡯࡯ࠩ‧"))
    if os.path.exists(bstack111111ll1ll_opy_):
      bstack11111l11lll_opy_.append(bstack111111ll1ll_opy_)
    output_file = os.path.join(tempfile.gettempdir(), bstack11l1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠭࡭ࡱࡪࡷ࠲࠭ ") + uuid + bstack11l1l11_opy_ (u"ࠨ࠰ࡷࡥࡷ࠴ࡧࡻࠩ "))
    with tarfile.open(output_file, bstack11l1l11_opy_ (u"ࠤࡺ࠾࡬ࢀࠢ‪")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack11111l11lll_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack11111l1111l_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack11111l1l11l_opy_ = data.encode()
        tarinfo.size = len(bstack11111l1l11l_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack11111l1l11l_opy_))
    bstack11lllll1l1_opy_ = MultipartEncoder(
      fields= {
        bstack11l1l11_opy_ (u"ࠪࡨࡦࡺࡡࠨ‫"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack11l1l11_opy_ (u"ࠫࡷࡨࠧ‬")), bstack11l1l11_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲ࡼ࠲࡭ࡺࡪࡲࠪ‭")),
        bstack11l1l11_opy_ (u"࠭ࡣ࡭࡫ࡨࡲࡹࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ‮"): uuid
      }
    )
    bstack11111ll1lll_opy_ = bstack1ll11l1l11_opy_(cli.config, [bstack11l1l11_opy_ (u"ࠢࡢࡲ࡬ࡷࠧ "), bstack11l1l11_opy_ (u"ࠣࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠣ‰"), bstack11l1l11_opy_ (u"ࠤࡸࡴࡱࡵࡡࡥࠤ‱")], bstack111ll1l1l1l_opy_)
    response = requests.post(
      bstack11l1l11_opy_ (u"ࠥࡿࢂ࠵ࡣ࡭࡫ࡨࡲࡹ࠳࡬ࡰࡩࡶ࠳ࡺࡶ࡬ࡰࡣࡧࠦ′").format(bstack11111ll1lll_opy_),
      data=bstack11lllll1l1_opy_,
      headers={bstack11l1l11_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪ″"): bstack11lllll1l1_opy_.content_type},
      auth=(config[bstack11l1l11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ‴")], config[bstack11l1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ‵")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack11l1l11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡵࡱ࡮ࡲࡥࡩࠦ࡬ࡰࡩࡶ࠾ࠥ࠭‶") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack11l1l11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡧࡱࡨ࡮ࡴࡧࠡ࡮ࡲ࡫ࡸࡀࠧ‷") + str(e))
  finally:
    try:
      bstack1l11l1ll1l1_opy_()
      bstack11111ll11l1_opy_()
    except:
      pass
    if bstack11ll1l1l1_opy_ and bstack11111ll1l1l_opy_:
      bstack11ll1l1l1_opy_.end(EVENTS.bstack111lllll1l1_opy_.value, bstack11111ll1l1l_opy_ + bstack11l1l11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ‸"), bstack11111ll1l1l_opy_ + bstack11l1l11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ‹"), status=True, failure=None, test_name=None)
    try:
      elapsed = time.time() - start_time
      get_logger().debug(bstack11l1l11_opy_ (u"ࠦࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡹࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࡦࠣ࡭ࡳࠦࡻ࠻࠰࠶ࡪࢂࠦࡳࡦࡥࡲࡲࡩࡹࠢ›").format(elapsed))
    except Exception:
      pass