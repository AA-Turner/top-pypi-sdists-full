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
from bstack_utils.constants import bstack111ll1l1l11_opy_, EVENTS, bstack111ll1ll1l1_opy_, bstack111l1llll11_opy_, STAGE
import tempfile
import json
bstack111111l11l1_opy_ = os.getenv(bstack1111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡋࡤࡌࡉࡍࡇࠥℑ"), None) or os.path.join(tempfile.gettempdir(), bstack1111_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡧࡩࡧࡻࡧ࠯࡮ࡲ࡫ࠧℒ"))
bstack1llllllll1l1_opy_ = os.path.join(bstack1111_opy_ (u"ࠦࡱࡵࡧࠣℓ"), bstack1111_opy_ (u"ࠬࡹࡤ࡬࠯ࡦࡰ࡮࠳ࡤࡦࡤࡸ࡫࠳ࡲ࡯ࡨࠩ℔"))
_11111111l1l_opy_ = threading.Lock()
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1111_opy_ (u"࠭ࠥࠩࡣࡶࡧࡹ࡯࡭ࡦࠫࡶࠤࡠࠫࠨ࡯ࡣࡰࡩ࠮ࡹ࡝࡜ࠧࠫࡰࡪࡼࡥ࡭ࡰࡤࡱࡪ࠯ࡳ࡞ࠢ࠰ࠤࠪ࠮࡭ࡦࡵࡶࡥ࡬࡫ࠩࡴࠩℕ"),
      datefmt=bstack1111_opy_ (u"࡛ࠧࠦ࠰ࠩࡲ࠳ࠥࡥࡖࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࡞ࠬ№"),
      stream=sys.stdout
    )
  return logger
def bstack1ll11llll1_opy_(name=__name__, level=logging.DEBUG):
  bstack1111_opy_ (u"ࠣࠤࠥࠎࠥࠦࡒࡦࡶࡸࡶࡳࡹࠠࡢࠢ࡯ࡳ࡬࡭ࡥࡳࠢࡷ࡬ࡦࡺࠠࡸࡴ࡬ࡸࡪࡹࠠࡰࡰ࡯ࡽࠥࡺ࡯ࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠳ࡲ࡯ࡨࠢࡩ࡭ࡱ࡫ࠊࠡࠢࡆࡶࡪࡧࡴࡦࡵࠣࡥࡳࡪࠠ࡮ࡣࡱࡥ࡬࡫ࡳࠡ࡫ࡷࡷࠥࡵࡷ࡯ࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡦࡪ࡮ࡨࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶࠏࠦࠠࡐࡰ࡯ࡽࠥ࡫࡮ࡢࡤ࡯ࡩࡸࠦ࡬ࡰࡩࡪ࡭ࡳ࡭ࠠࡪࡨࠣࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓࡥࡌࡐࡉࡖࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵࠢࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠤ࡮ࡹࠠࡴࡧࡷࠤࡹࡵࠠࡢࠢࡷࡶࡺࡺࡨࡺࠢࡹࡥࡱࡻࡥࠋࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦ࡮ࡢ࡯ࡨ࠾ࠥࡒ࡯ࡨࡩࡨࡶࠥࡴࡡ࡮ࡧࠣࠬࡩ࡫ࡦࡢࡷ࡯ࡸࡸࠦࡴࡰࠢࡢࡣࡳࡧ࡭ࡦࡡࡢ࠭ࠏࠦࠠࠡࠢ࡯ࡩࡻ࡫࡬࠻ࠢࡏࡳ࡬࡭ࡩ࡯ࡩࠣࡰࡪࡼࡥ࡭ࠢࠫࡨࡪ࡬ࡡࡶ࡮ࡷࡷࠥࡺ࡯ࠡࡆࡈࡆ࡚ࡍࠩࠋࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢ࡯ࡳ࡬࡭ࡩ࡯ࡩ࠱ࡐࡴ࡭ࡧࡦࡴ࠽ࠤࡈࡵ࡮ࡧ࡫ࡪࡹࡷ࡫ࡤࠡ࡮ࡲ࡫࡬࡫ࡲࠡࡶ࡫ࡥࡹࠦࡷࡳ࡫ࡷࡩࡸࠦ࡯࡯࡮ࡼࠤࡹࡵࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠲ࡱࡵࡧࠡࠪ࡬ࡪࠥ࡫࡮ࡢࡤ࡯ࡩࡩ࠯ࠊࠡࠢࠥࠦࠧ℗")
  logger_name = bstack1111_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠴ࡻ࠱ࡿࠥ℘").format(name)
  logger = logging.getLogger(logger_name)
  is_enabled = os.getenv(bstack1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓࡥࡌࡐࡉࡖࠫℙ"), bstack1111_opy_ (u"ࠫࠬℚ")).lower() == bstack1111_opy_ (u"ࠬࡺࡲࡶࡧࠪℛ")
  if not is_enabled:
    logger.setLevel(logging.CRITICAL)
    logger.propagate = False
    return logger
  with _11111111l1l_opy_:
    if logger.handlers:
      return logger
    bstack1111111l111_opy_ = os.path.join(os.getcwd(), bstack1111_opy_ (u"࠭࡬ࡰࡩࠪℜ"), bstack1111_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠲ࡱࡵࡧࠨℝ"))
    log_dir = os.path.dirname(bstack1111111l111_opy_)
    if not os.path.exists(log_dir):
      os.makedirs(log_dir)
    bstack1111111ll1l_opy_ = logging.FileHandler(bstack1111111l111_opy_)
    bstack111111l1l11_opy_ = logging.Formatter(
      fmt=bstack1111_opy_ (u"ࠨࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲࡛ࠦࠡࡕࡇࡏ࠲ࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠢࡠࠤࠪ࠮࡭ࡦࡵࡶࡥ࡬࡫ࠩࡴࠩ℞"),
      datefmt=bstack1111_opy_ (u"ࠩࠨ࡝࠲ࠫ࡭࠮ࠧࡧࡘࠪࡎ࠺ࠦࡏ࠽ࠩࡘࡠࠧ℟"),
    )
    bstack1111111ll1l_opy_.setFormatter(bstack111111l1l11_opy_)
    bstack1111111ll1l_opy_.setLevel(level)
    bstack1111111ll1l_opy_.addFilter(lambda r: r.name != bstack1111_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲ࠯ࡴࡨࡱࡴࡺࡥ࠯ࡴࡨࡱࡴࡺࡥࡠࡥࡲࡲࡳ࡫ࡣࡵ࡫ࡲࡲࠬ℠"))
    logger.addHandler(bstack1111111ll1l_opy_)
    logger.setLevel(level)
    logger.propagate = False
  return logger
def bstack1ll111111l1_opy_():
  bstack11111111ll1_opy_ = os.environ.get(bstack1111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢࡈࡊࡈࡕࡈࠤ℡"), bstack1111_opy_ (u"ࠧ࡬ࡡ࡭ࡵࡨࠦ™"))
  return logging.DEBUG if bstack11111111ll1_opy_.lower() == bstack1111_opy_ (u"ࠨࡴࡳࡷࡨࠦ℣") else logging.INFO
def bstack1l11l11ll11_opy_():
  global bstack111111l11l1_opy_
  if os.path.exists(bstack111111l11l1_opy_):
    os.remove(bstack111111l11l1_opy_)
  if os.path.exists(bstack1llllllll1l1_opy_):
    os.remove(bstack1llllllll1l1_opy_)
def bstack1llll1111_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def configure_logger(config, log_level):
  bstack11111111l11_opy_ = log_level
  if bstack1111_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩℤ") in config and config[bstack1111_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪ℥")] in bstack111ll1ll1l1_opy_:
    bstack11111111l11_opy_ = bstack111ll1ll1l1_opy_[config[bstack1111_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫΩ")]]
  if config.get(bstack1111_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬ℧"), False):
    logging.getLogger().setLevel(bstack11111111l11_opy_)
    return bstack11111111l11_opy_
  global bstack111111l11l1_opy_
  bstack1llll1111_opy_()
  bstack1lllllllll1l_opy_ = logging.Formatter(
    fmt=bstack1111_opy_ (u"ࠫࠪ࠮ࡡࡴࡥࡷ࡭ࡲ࡫ࠩࡴࠢ࡞ࠩ࠭ࡴࡡ࡮ࡧࠬࡷࡢࡡࠥࠩ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨ࠭ࡸࡣࠠ࠮ࠢࠨࠬࡲ࡫ࡳࡴࡣࡪࡩ࠮ࡹࠧℨ"),
    datefmt=bstack1111_opy_ (u"࡙ࠬࠫ࠮ࠧࡰ࠱ࠪࡪࡔࠦࡊ࠽ࠩࡒࡀࠥࡔ࡜ࠪ℩"),
  )
  bstack111111l11ll_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack111111l11l1_opy_)
  file_handler.setFormatter(bstack1lllllllll1l_opy_)
  bstack111111l11ll_opy_.setFormatter(bstack1lllllllll1l_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack111111l11ll_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1111_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠯ࡹࡨࡦࡩࡸࡩࡷࡧࡵ࠲ࡷ࡫࡭ࡰࡶࡨ࠲ࡷ࡫࡭ࡰࡶࡨࡣࡨࡵ࡮࡯ࡧࡦࡸ࡮ࡵ࡮ࠨK"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack111111l11ll_opy_.setLevel(bstack11111111l11_opy_)
  logging.getLogger().addHandler(bstack111111l11ll_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack11111111l11_opy_
def bstack1llllllllll1_opy_(config):
  try:
    bstack1lllllllll11_opy_ = set(bstack111l1llll11_opy_)
    bstack111111111ll_opy_ = bstack1111_opy_ (u"ࠧࠨÅ")
    with open(bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫℬ")) as bstack11111111lll_opy_:
      bstack111111l1111_opy_ = bstack11111111lll_opy_.read()
      bstack111111111ll_opy_ = re.sub(bstack1111_opy_ (u"ࡴࠪࡢ࠭ࡢࡳࠬࠫࡂࠧ࠳࠰ࠤ࡝ࡰࠪℭ"), bstack1111_opy_ (u"ࠪࠫ℮"), bstack111111l1111_opy_, flags=re.M)
      bstack111111111ll_opy_ = re.sub(
        bstack1111_opy_ (u"ࡶࠬࡤࠨ࡝ࡵ࠮࠭ࡄ࠮ࠧℯ") + bstack1111_opy_ (u"ࠬࢂࠧℰ").join(bstack1lllllllll11_opy_) + bstack1111_opy_ (u"࠭ࠩ࠯ࠬࠧࠫℱ"),
        bstack1111_opy_ (u"ࡲࠨ࡞࠵࠾ࠥࡡࡒࡆࡆࡄࡇ࡙ࡋࡄ࡞ࠩℲ"),
        bstack111111111ll_opy_, flags=re.M | re.I
      )
    def bstack1111111l11l_opy_(dic):
      bstack1llllllll11l_opy_ = {}
      for key, value in dic.items():
        if key in bstack1lllllllll11_opy_:
          bstack1llllllll11l_opy_[key] = bstack1111_opy_ (u"ࠨ࡝ࡕࡉࡉࡇࡃࡕࡇࡇࡡࠬℳ")
        else:
          if isinstance(value, dict):
            bstack1llllllll11l_opy_[key] = bstack1111111l11l_opy_(value)
          else:
            bstack1llllllll11l_opy_[key] = value
      return bstack1llllllll11l_opy_
    bstack1llllllll11l_opy_ = bstack1111111l11l_opy_(config)
    return {
      bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬℴ"): bstack111111111ll_opy_,
      bstack1111_opy_ (u"ࠪࡪ࡮ࡴࡡ࡭ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭ℵ"): json.dumps(bstack1llllllll11l_opy_)
    }
  except Exception as e:
    return {}
def bstack1111111l1ll_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack1111_opy_ (u"ࠫࡱࡵࡧࠨℶ"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack1lllll1l1ll_opy_ = os.path.join(log_dir, bstack1111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡩ࡯࡯ࡨ࡬࡫ࡸ࠭ℷ"))
  if not os.path.exists(bstack1lllll1l1ll_opy_):
    bstack1llllllll1ll_opy_ = {
      bstack1111_opy_ (u"ࠨࡩ࡯࡫ࡳࡥࡹ࡮ࠢℸ"): str(inipath),
      bstack1111_opy_ (u"ࠢࡳࡱࡲࡸࡵࡧࡴࡩࠤℹ"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack1111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡥࡲࡲ࡫࡯ࡧࡴ࠰࡭ࡷࡴࡴࠧ℺")), bstack1111_opy_ (u"ࠩࡺࠫ℻")) as bstack11111111111_opy_:
      bstack11111111111_opy_.write(json.dumps(bstack1llllllll1ll_opy_))
def bstack1111111111l_opy_():
  try:
    bstack1lllll1l1ll_opy_ = os.path.join(os.getcwd(), bstack1111_opy_ (u"ࠪࡰࡴ࡭ࠧℼ"), bstack1111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷ࠳ࡰࡳࡰࡰࠪℽ"))
    if os.path.exists(bstack1lllll1l1ll_opy_):
      with open(bstack1lllll1l1ll_opy_, bstack1111_opy_ (u"ࠬࡸࠧℾ")) as bstack11111111111_opy_:
        bstack1111111ll11_opy_ = json.load(bstack11111111111_opy_)
      return bstack1111111ll11_opy_.get(bstack1111_opy_ (u"࠭ࡩ࡯࡫ࡳࡥࡹ࡮ࠧℿ"), bstack1111_opy_ (u"ࠧࠨ⅀")), bstack1111111ll11_opy_.get(bstack1111_opy_ (u"ࠨࡴࡲࡳࡹࡶࡡࡵࡪࠪ⅁"), bstack1111_opy_ (u"ࠩࠪ⅂"))
  except:
    pass
  return None, None
def bstack111111l111l_opy_():
  try:
    bstack1lllll1l1ll_opy_ = os.path.join(os.getcwd(), bstack1111_opy_ (u"ࠪࡰࡴ࡭ࠧ⅃"), bstack1111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷ࠳ࡰࡳࡰࡰࠪ⅄"))
    if os.path.exists(bstack1lllll1l1ll_opy_):
      os.remove(bstack1lllll1l1ll_opy_)
  except:
    pass
def bstack1l1111l11_opy_(config):
  try:
    try:
      from bstack_utils.bstack1ll1l11ll1_opy_ import bstack1l11l1ll_opy_
    except Exception:
      bstack1l11l1ll_opy_ = None
    start_time = time.time()
    from bstack_utils.helper import global_config, bstack11111l1ll_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack111111l11l1_opy_
    if config.get(bstack1111_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧⅅ"), False):
      return
    uuid = os.getenv(bstack1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫⅆ")) if os.getenv(bstack1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬⅇ")) else global_config.get_property(bstack1111_opy_ (u"ࠣࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠥⅈ"))
    if not uuid or uuid == bstack1111_opy_ (u"ࠩࡱࡹࡱࡲࠧⅉ"):
      return
    bstack1lllllllllll_opy_ = bstack1l11l1ll_opy_.bstack11l111111_opy_(EVENTS.bstack111ll11l11l_opy_.value) if bstack1l11l1ll_opy_ else None
    bstack111111l1l1l_opy_ = [bstack1111_opy_ (u"ࠪࡶࡪࡷࡵࡪࡴࡨࡱࡪࡴࡴࡴ࠰ࡷࡼࡹ࠭⅊"), bstack1111_opy_ (u"ࠫࡕ࡯ࡰࡧ࡫࡯ࡩࠬ⅋"), bstack1111_opy_ (u"ࠬࡶࡹࡱࡴࡲ࡮ࡪࡩࡴ࠯ࡶࡲࡱࡱ࠭⅌"), bstack111111l11l1_opy_, bstack1llllllll1l1_opy_]
    bstack1111111lll1_opy_, root_path = bstack1111111111l_opy_()
    if bstack1111111lll1_opy_ != None:
      bstack111111l1l1l_opy_.append(bstack1111111lll1_opy_)
    if root_path != None:
      bstack111111l1l1l_opy_.append(os.path.join(root_path, bstack1111_opy_ (u"࠭ࡣࡰࡰࡩࡸࡪࡹࡴ࠯ࡲࡼࠫ⅍")))
    bstack111111111l1_opy_ = os.path.join(os.getcwd(), bstack1111_opy_ (u"ࠧ࡭ࡱࡪࠫⅎ"), bstack1111_opy_ (u"ࠨ࡭ࡨࡽ࠲ࡳࡥࡵࡴ࡬ࡧࡸ࠴ࡪࡴࡱࡱࠫ⅏"))
    if os.path.exists(bstack111111111l1_opy_):
      bstack111111l1l1l_opy_.append(bstack111111111l1_opy_)
    output_file = os.path.join(tempfile.gettempdir(), bstack1111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠯࡯ࡳ࡬ࡹ࠭ࠨ⅐") + uuid + bstack1111_opy_ (u"ࠪ࠲ࡹࡧࡲ࠯ࡩࡽࠫ⅑"))
    with tarfile.open(output_file, bstack1111_opy_ (u"ࠦࡼࡀࡧࡻࠤ⅒")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack111111l1l1l_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1llllllllll1_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1111111l1l1_opy_ = data.encode()
        tarinfo.size = len(bstack1111111l1l1_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1111111l1l1_opy_))
    bstack11111ll1l_opy_ = MultipartEncoder(
      fields= {
        bstack1111_opy_ (u"ࠬࡪࡡࡵࡣࠪ⅓"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1111_opy_ (u"࠭ࡲࡣࠩ⅔")), bstack1111_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡾ࠭ࡨࡼ࡬ࡴࠬ⅕")),
        bstack1111_opy_ (u"ࠨࡥ࡯࡭ࡪࡴࡴࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ⅖"): uuid
      }
    )
    bstack1111111llll_opy_ = bstack11111l1ll_opy_(cli.config, [bstack1111_opy_ (u"ࠤࡤࡴ࡮ࡹࠢ⅗"), bstack1111_opy_ (u"ࠥࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠥ⅘"), bstack1111_opy_ (u"ࠦࡺࡶ࡬ࡰࡣࡧࠦ⅙")], bstack111ll1l1l11_opy_)
    response = requests.post(
      bstack1111_opy_ (u"ࠧࢁࡽ࠰ࡥ࡯࡭ࡪࡴࡴ࠮࡮ࡲ࡫ࡸ࠵ࡵࡱ࡮ࡲࡥࡩࠨ⅚").format(bstack1111111llll_opy_),
      data=bstack11111ll1l_opy_,
      headers={bstack1111_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬ⅛"): bstack11111ll1l_opy_.content_type},
      auth=(config[bstack1111_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ⅜")], config[bstack1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ⅝")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡷࡳࡰࡴࡧࡤࠡ࡮ࡲ࡫ࡸࡀࠠࠨ⅞") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1111_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡩࡳࡪࡩ࡯ࡩࠣࡰࡴ࡭ࡳ࠻ࠩ⅟") + str(e))
  finally:
    try:
      bstack1l11l11ll11_opy_()
      bstack111111l111l_opy_()
    except:
      pass
    if bstack1l11l1ll_opy_ and bstack1lllllllllll_opy_:
      bstack1l11l1ll_opy_.end(EVENTS.bstack111ll11l11l_opy_.value, bstack1lllllllllll_opy_ + bstack1111_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦⅠ"), bstack1lllllllllll_opy_ + bstack1111_opy_ (u"ࠧࡀࡥ࡯ࡦࠥⅡ"), status=True, failure=None, test_name=None)
    try:
      elapsed = time.time() - start_time
      get_logger().debug(bstack1111_opy_ (u"ࠨࡳࡦࡰࡧࡣࡱࡵࡧࡴࠢࡦࡳࡲࡶ࡬ࡦࡶࡨࡨࠥ࡯࡮ࠡࡽ࠽࠲࠸࡬ࡽࠡࡵࡨࡧࡴࡴࡤࡴࠤⅢ").format(elapsed))
    except Exception:
      pass