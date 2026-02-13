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
from bstack_utils.constants import bstack111lll1l1l1_opy_, EVENTS, bstack111ll1l1l11_opy_, bstack111ll1ll1l1_opy_, STAGE
import tempfile
import json
bstack111111ll1l1_opy_ = os.getenv(bstack11l11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡌࡥࡆࡊࡎࡈࠦ῞"), None) or os.path.join(tempfile.gettempdir(), bstack11l11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡨࡪࡨࡵࡨ࠰࡯ࡳ࡬ࠨ῟"))
bstack11111l11l11_opy_ = os.path.join(bstack11l11_opy_ (u"ࠧࡲ࡯ࡨࠤῠ"), bstack11l11_opy_ (u"࠭ࡳࡥ࡭࠰ࡧࡱ࡯࠭ࡥࡧࡥࡹ࡬࠴࡬ࡰࡩࠪῡ"))
_111111l1l11_opy_ = threading.Lock()
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack11l11_opy_ (u"ࠧࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࠫࠨ࡮ࡧࡶࡷࡦ࡭ࡥࠪࡵࠪῢ"),
      datefmt=bstack11l11_opy_ (u"ࠨࠧ࡜࠱ࠪࡳ࠭ࠦࡦࡗࠩࡍࡀࠥࡎ࠼ࠨࡗ࡟࠭ΰ"),
      stream=sys.stdout
    )
  return logger
def bstack11llll1l11_opy_(name=__name__, level=logging.DEBUG):
  bstack11l11_opy_ (u"ࠤࠥࠦࠏࠦࠠࡓࡧࡷࡹࡷࡴࡳࠡࡣࠣࡰࡴ࡭ࡧࡦࡴࠣࡸ࡭ࡧࡴࠡࡹࡵ࡭ࡹ࡫ࡳࠡࡱࡱࡰࡾࠦࡴࡰࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠴࡬ࡰࡩࠣࡪ࡮ࡲࡥࠋࠢࠣࡇࡷ࡫ࡡࡵࡧࡶࠤࡦࡴࡤࠡ࡯ࡤࡲࡦ࡭ࡥࡴࠢ࡬ࡸࡸࠦ࡯ࡸࡰࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡧ࡫࡯ࡩࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࠐࠠࠡࡑࡱࡰࡾࠦࡥ࡯ࡣࡥࡰࡪࡹࠠ࡭ࡱࡪ࡫࡮ࡴࡧࠡ࡫ࡩࠤࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔ࡟ࡍࡑࡊࡗࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶࠣࡺࡦࡸࡩࡢࡤ࡯ࡩࠥ࡯ࡳࠡࡵࡨࡸࠥࡺ࡯ࠡࡣࠣࡸࡷࡻࡴࡩࡻࠣࡺࡦࡲࡵࡦࠌࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠ࡯ࡣࡰࡩ࠿ࠦࡌࡰࡩࡪࡩࡷࠦ࡮ࡢ࡯ࡨࠤ࠭ࡪࡥࡧࡣࡸࡰࡹࡹࠠࡵࡱࠣࡣࡤࡴࡡ࡮ࡧࡢࡣ࠮ࠐࠠࠡࠢࠣࡰࡪࡼࡥ࡭࠼ࠣࡐࡴ࡭ࡧࡪࡰࡪࠤࡱ࡫ࡶࡦ࡮ࠣࠬࡩ࡫ࡦࡢࡷ࡯ࡸࡸࠦࡴࡰࠢࡇࡉࡇ࡛ࡇࠪࠌࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࡰࡴ࡭ࡧࡪࡰࡪ࠲ࡑࡵࡧࡨࡧࡵ࠾ࠥࡉ࡯࡯ࡨ࡬࡫ࡺࡸࡥࡥࠢ࡯ࡳ࡬࡭ࡥࡳࠢࡷ࡬ࡦࡺࠠࡸࡴ࡬ࡸࡪࡹࠠࡰࡰ࡯ࡽࠥࡺ࡯ࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠳ࡲ࡯ࡨࠢࠫ࡭࡫ࠦࡥ࡯ࡣࡥࡰࡪࡪࠩࠋࠢࠣࠦࠧࠨῤ")
  logger_name = bstack11l11_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠮ࡼ࠲ࢀࠦῥ").format(name)
  logger = logging.getLogger(logger_name)
  is_enabled = os.getenv(bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔ࡟ࡍࡑࡊࡗࠬῦ"), bstack11l11_opy_ (u"ࠬ࠭ῧ")).lower() == bstack11l11_opy_ (u"࠭ࡴࡳࡷࡨࠫῨ")
  if not is_enabled:
    logger.setLevel(logging.CRITICAL)
    logger.propagate = False
    return logger
  with _111111l1l11_opy_:
    if logger.handlers:
      return logger
    bstack1111111ll11_opy_ = os.path.join(os.getcwd(), bstack11l11_opy_ (u"ࠧ࡭ࡱࡪࠫῩ"), bstack11l11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠳ࡲ࡯ࡨࠩῪ"))
    log_dir = os.path.dirname(bstack1111111ll11_opy_)
    if not os.path.exists(log_dir):
      os.makedirs(log_dir)
    bstack1111111l1l1_opy_ = logging.FileHandler(bstack1111111ll11_opy_)
    bstack111111l1111_opy_ = logging.Formatter(
      fmt=bstack11l11_opy_ (u"ࠩࠨࠬࡦࡹࡣࡵ࡫ࡰࡩ࠮ࡹࠠ࡜ࠧࠫࡲࡦࡳࡥࠪࡵࡠ࡟ࠪ࠮࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠫࡶࡡࠥ࠳ࠠ࡜ࠢࡖࡈࡐ࠳ࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠣࡡࠥࠫࠨ࡮ࡧࡶࡷࡦ࡭ࡥࠪࡵࠪΎ"),
      datefmt=bstack11l11_opy_ (u"ࠪࠩ࡞࠳ࠥ࡮࠯ࠨࡨ࡙ࠫࡈ࠻ࠧࡐ࠾࡙࡚ࠪࠨῬ"),
    )
    bstack1111111l1l1_opy_.setFormatter(bstack111111l1111_opy_)
    bstack1111111l1l1_opy_.setLevel(level)
    bstack1111111l1l1_opy_.addFilter(lambda r: r.name != bstack11l11_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳ࠰ࡵࡩࡲࡵࡴࡦ࠰ࡵࡩࡲࡵࡴࡦࡡࡦࡳࡳࡴࡥࡤࡶ࡬ࡳࡳ࠭῭"))
    logger.addHandler(bstack1111111l1l1_opy_)
    logger.setLevel(level)
    logger.propagate = False
  return logger
def bstack1ll111l11l1_opy_():
  bstack11111l11ll1_opy_ = os.environ.get(bstack11l11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡏࡎࡂࡔ࡜ࡣࡉࡋࡂࡖࡉࠥ΅"), bstack11l11_opy_ (u"ࠨࡦࡢ࡮ࡶࡩࠧ`"))
  return logging.DEBUG if bstack11111l11ll1_opy_.lower() == bstack11l11_opy_ (u"ࠢࡵࡴࡸࡩࠧ῰") else logging.INFO
def bstack1l111llll11_opy_():
  global bstack111111ll1l1_opy_
  if os.path.exists(bstack111111ll1l1_opy_):
    os.remove(bstack111111ll1l1_opy_)
  if os.path.exists(bstack11111l11l11_opy_):
    os.remove(bstack11111l11l11_opy_)
def bstack111l1ll111_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def configure_logger(config, log_level):
  bstack111111l11l1_opy_ = log_level
  if bstack11l11_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪ῱") in config and config[bstack11l11_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫῲ")] in bstack111ll1l1l11_opy_:
    bstack111111l11l1_opy_ = bstack111ll1l1l11_opy_[config[bstack11l11_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬῳ")]]
  if config.get(bstack11l11_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭ῴ"), False):
    logging.getLogger().setLevel(bstack111111l11l1_opy_)
    return bstack111111l11l1_opy_
  global bstack111111ll1l1_opy_
  bstack111l1ll111_opy_()
  bstack1111111ll1l_opy_ = logging.Formatter(
    fmt=bstack11l11_opy_ (u"ࠬࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨ῵"),
    datefmt=bstack11l11_opy_ (u"࡚࠭ࠥ࠯ࠨࡱ࠲ࠫࡤࡕࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࡝ࠫῶ"),
  )
  bstack111111lll11_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack111111ll1l1_opy_)
  file_handler.setFormatter(bstack1111111ll1l_opy_)
  bstack111111lll11_opy_.setFormatter(bstack1111111ll1l_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack111111lll11_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack11l11_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࠰ࡺࡩࡧࡪࡲࡪࡸࡨࡶ࠳ࡸࡥ࡮ࡱࡷࡩ࠳ࡸࡥ࡮ࡱࡷࡩࡤࡩ࡯࡯ࡰࡨࡧࡹ࡯࡯࡯ࠩῷ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack111111lll11_opy_.setLevel(bstack111111l11l1_opy_)
  logging.getLogger().addHandler(bstack111111lll11_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack111111l11l1_opy_
def bstack11111l111ll_opy_(config):
  try:
    bstack11111l11111_opy_ = set(bstack111ll1ll1l1_opy_)
    bstack111111lll1l_opy_ = bstack11l11_opy_ (u"ࠨࠩῸ")
    with open(bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬΌ")) as bstack111111l11ll_opy_:
      bstack111111lllll_opy_ = bstack111111l11ll_opy_.read()
      bstack111111lll1l_opy_ = re.sub(bstack11l11_opy_ (u"ࡵࠫࡣ࠮࡜ࡴ࠭ࠬࡃࠨ࠴ࠪࠥ࡞ࡱࠫῺ"), bstack11l11_opy_ (u"ࠫࠬΏ"), bstack111111lllll_opy_, flags=re.M)
      bstack111111lll1l_opy_ = re.sub(
        bstack11l11_opy_ (u"ࡷ࠭࡞ࠩ࡞ࡶ࠯࠮ࡅࠨࠨῼ") + bstack11l11_opy_ (u"࠭ࡼࠨ´").join(bstack11111l11111_opy_) + bstack11l11_opy_ (u"ࠧࠪ࠰࠭ࠨࠬ῾"),
        bstack11l11_opy_ (u"ࡳࠩ࡟࠶࠿࡛ࠦࡓࡇࡇࡅࡈ࡚ࡅࡅ࡟ࠪ῿"),
        bstack111111lll1l_opy_, flags=re.M | re.I
      )
    def bstack1111111l1ll_opy_(dic):
      bstack11111l11l1l_opy_ = {}
      for key, value in dic.items():
        if key in bstack11111l11111_opy_:
          bstack11111l11l1l_opy_[key] = bstack11l11_opy_ (u"ࠩ࡞ࡖࡊࡊࡁࡄࡖࡈࡈࡢ࠭ ")
        else:
          if isinstance(value, dict):
            bstack11111l11l1l_opy_[key] = bstack1111111l1ll_opy_(value)
          else:
            bstack11111l11l1l_opy_[key] = value
      return bstack11111l11l1l_opy_
    bstack11111l11l1l_opy_ = bstack1111111l1ll_opy_(config)
    return {
      bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ "): bstack111111lll1l_opy_,
      bstack11l11_opy_ (u"ࠫ࡫࡯࡮ࡢ࡮ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧ "): json.dumps(bstack11111l11l1l_opy_)
    }
  except Exception as e:
    return {}
def bstack111111ll111_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack11l11_opy_ (u"ࠬࡲ࡯ࡨࠩ "))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack1lllll1l111_opy_ = os.path.join(log_dir, bstack11l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡣࡰࡰࡩ࡭࡬ࡹࠧ "))
  if not os.path.exists(bstack1lllll1l111_opy_):
    bstack111111l1l1l_opy_ = {
      bstack11l11_opy_ (u"ࠢࡪࡰ࡬ࡴࡦࡺࡨࠣ "): str(inipath),
      bstack11l11_opy_ (u"ࠣࡴࡲࡳࡹࡶࡡࡵࡪࠥ "): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack11l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡦࡳࡳ࡬ࡩࡨࡵ࠱࡮ࡸࡵ࡮ࠨ ")), bstack11l11_opy_ (u"ࠪࡻࠬ ")) as bstack1111111lll1_opy_:
      bstack1111111lll1_opy_.write(json.dumps(bstack111111l1l1l_opy_))
def bstack111111ll11l_opy_():
  try:
    bstack1lllll1l111_opy_ = os.path.join(os.getcwd(), bstack11l11_opy_ (u"ࠫࡱࡵࡧࠨ "), bstack11l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡩ࡯࡯ࡨ࡬࡫ࡸ࠴ࡪࡴࡱࡱࠫ "))
    if os.path.exists(bstack1lllll1l111_opy_):
      with open(bstack1lllll1l111_opy_, bstack11l11_opy_ (u"࠭ࡲࠨ​")) as bstack1111111lll1_opy_:
        bstack111111l1lll_opy_ = json.load(bstack1111111lll1_opy_)
      return bstack111111l1lll_opy_.get(bstack11l11_opy_ (u"ࠧࡪࡰ࡬ࡴࡦࡺࡨࠨ‌"), bstack11l11_opy_ (u"ࠨࠩ‍")), bstack111111l1lll_opy_.get(bstack11l11_opy_ (u"ࠩࡵࡳࡴࡺࡰࡢࡶ࡫ࠫ‎"), bstack11l11_opy_ (u"ࠪࠫ‏"))
  except:
    pass
  return None, None
def bstack111111ll1ll_opy_():
  try:
    bstack1lllll1l111_opy_ = os.path.join(os.getcwd(), bstack11l11_opy_ (u"ࠫࡱࡵࡧࠨ‐"), bstack11l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡩ࡯࡯ࡨ࡬࡫ࡸ࠴ࡪࡴࡱࡱࠫ‑"))
    if os.path.exists(bstack1lllll1l111_opy_):
      os.remove(bstack1lllll1l111_opy_)
  except:
    pass
def bstack1l1l1l11l_opy_(config):
  try:
    try:
      from bstack_utils.bstack11ll11ll1l_opy_ import bstack111l1lllll_opy_
    except Exception:
      bstack111l1lllll_opy_ = None
    start_time = time.time()
    from bstack_utils.helper import bstack11l1l1111_opy_, bstack1l11l1llll_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack111111ll1l1_opy_
    if config.get(bstack11l11_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨ‒"), False):
      return
    uuid = os.getenv(bstack11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ–")) if os.getenv(bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭—")) else bstack11l1l1111_opy_.get_property(bstack11l11_opy_ (u"ࠤࡶࡨࡰࡘࡵ࡯ࡋࡧࠦ―"))
    if not uuid or uuid == bstack11l11_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ‖"):
      return
    bstack1111111llll_opy_ = bstack111l1lllll_opy_.bstack1l11111111_opy_(EVENTS.bstack111ll11lll1_opy_.value) if bstack111l1lllll_opy_ else None
    bstack11111l111l1_opy_ = [bstack11l11_opy_ (u"ࠫࡷ࡫ࡱࡶ࡫ࡵࡩࡲ࡫࡮ࡵࡵ࠱ࡸࡽࡺࠧ‗"), bstack11l11_opy_ (u"ࠬࡖࡩࡱࡨ࡬ࡰࡪ࠭‘"), bstack11l11_opy_ (u"࠭ࡰࡺࡲࡵࡳ࡯࡫ࡣࡵ࠰ࡷࡳࡲࡲࠧ’"), bstack111111ll1l1_opy_, bstack11111l11l11_opy_]
    bstack111111llll1_opy_, root_path = bstack111111ll11l_opy_()
    if bstack111111llll1_opy_ != None:
      bstack11111l111l1_opy_.append(bstack111111llll1_opy_)
    if root_path != None:
      bstack11111l111l1_opy_.append(os.path.join(root_path, bstack11l11_opy_ (u"ࠧࡤࡱࡱࡪࡹ࡫ࡳࡵ࠰ࡳࡽࠬ‚")))
    bstack111111l111l_opy_ = os.path.join(os.getcwd(), bstack11l11_opy_ (u"ࠨ࡮ࡲ࡫ࠬ‛"), bstack11l11_opy_ (u"ࠩ࡮ࡩࡾ࠳࡭ࡦࡶࡵ࡭ࡨࡹ࠮࡫ࡵࡲࡲࠬ“"))
    if os.path.exists(bstack111111l111l_opy_):
      bstack11111l111l1_opy_.append(bstack111111l111l_opy_)
    output_file = os.path.join(tempfile.gettempdir(), bstack11l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠰ࡰࡴ࡭ࡳ࠮ࠩ”") + uuid + bstack11l11_opy_ (u"ࠫ࠳ࡺࡡࡳ࠰ࡪࡾࠬ„"))
    with tarfile.open(output_file, bstack11l11_opy_ (u"ࠧࡽ࠺ࡨࡼࠥ‟")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack11111l111l1_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack11111l111ll_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack111111l1ll1_opy_ = data.encode()
        tarinfo.size = len(bstack111111l1ll1_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack111111l1ll1_opy_))
    bstack11l1l1l1ll_opy_ = MultipartEncoder(
      fields= {
        bstack11l11_opy_ (u"࠭ࡤࡢࡶࡤࠫ†"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack11l11_opy_ (u"ࠧࡳࡤࠪ‡")), bstack11l11_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡸ࠮ࡩࡽ࡭ࡵ࠭•")),
        bstack11l11_opy_ (u"ࠩࡦࡰ࡮࡫࡮ࡵࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ‣"): uuid
      }
    )
    bstack11111l1111l_opy_ = bstack1l11l1llll_opy_(cli.config, [bstack11l11_opy_ (u"ࠥࡥࡵ࡯ࡳࠣ․"), bstack11l11_opy_ (u"ࠦࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠦ‥"), bstack11l11_opy_ (u"ࠧࡻࡰ࡭ࡱࡤࡨࠧ…")], bstack111lll1l1l1_opy_)
    response = requests.post(
      bstack11l11_opy_ (u"ࠨࡻࡾ࠱ࡦࡰ࡮࡫࡮ࡵ࠯࡯ࡳ࡬ࡹ࠯ࡶࡲ࡯ࡳࡦࡪࠢ‧").format(bstack11111l1111l_opy_),
      data=bstack11l1l1l1ll_opy_,
      headers={bstack11l11_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ "): bstack11l1l1l1ll_opy_.content_type},
      auth=(config[bstack11l11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ ")], config[bstack11l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ‪")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack11l11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡸࡴࡱࡵࡡࡥࠢ࡯ࡳ࡬ࡹ࠺ࠡࠩ‫") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack11l11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡴࡤࡪࡰࡪࠤࡱࡵࡧࡴ࠼ࠪ‬") + str(e))
  finally:
    try:
      bstack1l111llll11_opy_()
      bstack111111ll1ll_opy_()
    except:
      pass
    if bstack111l1lllll_opy_ and bstack1111111llll_opy_:
      bstack111l1lllll_opy_.end(EVENTS.bstack111ll11lll1_opy_.value, bstack1111111llll_opy_ + bstack11l11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ‭"), bstack1111111llll_opy_ + bstack11l11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ‮"), status=True, failure=None, test_name=None)
    try:
      elapsed = time.time() - start_time
      get_logger().debug(bstack11l11_opy_ (u"ࠢࡴࡧࡱࡨࡤࡲ࡯ࡨࡵࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࡩࠦࡩ࡯ࠢࡾ࠾࠳࠹ࡦࡾࠢࡶࡩࡨࡵ࡮ࡥࡵࠥ ").format(elapsed))
    except Exception:
      pass