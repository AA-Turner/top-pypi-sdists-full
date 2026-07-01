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
from bstack_utils.constants import bstack1llllll1ll1l_opy_, EVENTS, bstack1llllllllll1_opy_, bstack11111111111_opy_, STAGE
import tempfile
import json
bstack1lll111l1l11_opy_ = os.getenv(bstack1l1llll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡊࡣࡋࡏࡌࡆࠤ⠉"), None) or os.path.join(tempfile.gettempdir(), bstack1l1llll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡦࡨࡦࡺ࡭࠮࡭ࡱࡪࠦ⠊"))
bstack1ll1lllll111_opy_ = os.path.join(bstack1l1llll_opy_ (u"ࠥࡰࡴ࡭ࠢ⠋"), bstack1l1llll_opy_ (u"ࠫࡸࡪ࡫࠮ࡥ࡯࡭࠲ࡪࡥࡣࡷࡪ࠲ࡱࡵࡧࠨ⠌"))
_1lll1111l11l_opy_ = threading.Lock()
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1l1llll_opy_ (u"ࠬࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨ⠍"),
      datefmt=bstack1l1llll_opy_ (u"࡚࠭ࠥ࠯ࠨࡱ࠲ࠫࡤࡕࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࡝ࠫ⠎"),
      stream=sys.stdout
    )
  return logger
def get_automation_logger(name=__name__, level=logging.DEBUG):
  bstack1l1llll_opy_ (u"ࠢࠣࠤࠍࠤࠥࡘࡥࡵࡷࡵࡲࡸࠦࡡࠡ࡮ࡲ࡫࡬࡫ࡲࠡࡶ࡫ࡥࡹࠦࡷࡳ࡫ࡷࡩࡸࠦ࡯࡯࡮ࡼࠤࡹࡵࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠲ࡱࡵࡧࠡࡨ࡬ࡰࡪࠐࠠࠡࡅࡵࡩࡦࡺࡥࡴࠢࡤࡲࡩࠦ࡭ࡢࡰࡤ࡫ࡪࡹࠠࡪࡶࡶࠤࡴࡽ࡮ࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥ࡬ࡩ࡭ࡧࠣ࡬ࡦࡴࡤ࡭ࡧࡵࠎࠥࠦࡏ࡯࡮ࡼࠤࡪࡴࡡࡣ࡮ࡨࡷࠥࡲ࡯ࡨࡩ࡬ࡲ࡬ࠦࡩࡧࠢࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࡤࡒࡏࡈࡕࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴࠡࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠣ࡭ࡸࠦࡳࡦࡶࠣࡸࡴࠦࡡࠡࡶࡵࡹࡹ࡮ࡹࠡࡸࡤࡰࡺ࡫ࠊࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࡴࡡ࡮ࡧ࠽ࠤࡑࡵࡧࡨࡧࡵࠤࡳࡧ࡭ࡦࠢࠫࡨࡪ࡬ࡡࡶ࡮ࡷࡷࠥࡺ࡯ࠡࡡࡢࡲࡦࡳࡥࡠࡡࠬࠎࠥࠦࠠࠡ࡮ࡨࡺࡪࡲ࠺ࠡࡎࡲ࡫࡬࡯࡮ࡨࠢ࡯ࡩࡻ࡫࡬ࠡࠪࡧࡩ࡫ࡧࡵ࡭ࡶࡶࠤࡹࡵࠠࡅࡇࡅ࡙ࡌ࠯ࠊࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡ࡮ࡲ࡫࡬࡯࡮ࡨ࠰ࡏࡳ࡬࡭ࡥࡳ࠼ࠣࡇࡴࡴࡦࡪࡩࡸࡶࡪࡪࠠ࡭ࡱࡪ࡫ࡪࡸࠠࡵࡪࡤࡸࠥࡽࡲࡪࡶࡨࡷࠥࡵ࡮࡭ࡻࠣࡸࡴࠦࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠱ࡰࡴ࡭ࠠࠩ࡫ࡩࠤࡪࡴࡡࡣ࡮ࡨࡨ࠮ࠐࠠࠡࠤࠥࠦ⠏")
  logger_name = bstack1l1llll_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠳ࢁ࠰ࡾࠤ⠐").format(name)
  logger = logging.getLogger(logger_name)
  is_enabled = os.getenv(bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࡤࡒࡏࡈࡕࠪ⠑"), bstack1l1llll_opy_ (u"ࠪࠫ⠒")).lower() == bstack1l1llll_opy_ (u"ࠫࡹࡸࡵࡦࠩ⠓")
  if not is_enabled:
    logger.setLevel(logging.CRITICAL)
    logger.propagate = False
    return logger
  with _1lll1111l11l_opy_:
    if logger.handlers:
      return logger
    bstack1lll11111l1l_opy_ = os.path.join(os.getcwd(), bstack1l1llll_opy_ (u"ࠬࡲ࡯ࡨࠩ⠔"), bstack1l1llll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠱ࡰࡴ࡭ࠧ⠕"))
    log_dir = os.path.dirname(bstack1lll11111l1l_opy_)
    if not os.path.exists(log_dir):
      os.makedirs(log_dir)
    bstack1lll111l11ll_opy_ = logging.FileHandler(bstack1lll11111l1l_opy_)
    bstack1lll1111l1l1_opy_ = logging.Formatter(
      fmt=bstack1l1llll_opy_ (u"ࠧࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࡡࠠࡔࡆࡎ࠱ࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠡ࡟ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨ⠖"),
      datefmt=bstack1l1llll_opy_ (u"ࠨࠧ࡜࠱ࠪࡳ࠭ࠦࡦࡗࠩࡍࡀࠥࡎ࠼ࠨࡗ࡟࠭⠗"),
    )
    bstack1lll111l11ll_opy_.setFormatter(bstack1lll1111l1l1_opy_)
    bstack1lll111l11ll_opy_.setLevel(level)
    bstack1lll111l11ll_opy_.addFilter(lambda r: r.name != bstack1l1llll_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࠮ࡳࡧࡰࡳࡹ࡫࠮ࡳࡧࡰࡳࡹ࡫࡟ࡤࡱࡱࡲࡪࡩࡴࡪࡱࡱࠫ⠘"))
    logger.addHandler(bstack1lll111l11ll_opy_)
    logger.setLevel(level)
    logger.propagate = False
  return logger
def get_log_level():
  bstack1lll1111ll11_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡇࡉࡇ࡛ࡇࠣ⠙"), bstack1l1llll_opy_ (u"ࠦ࡫ࡧ࡬ࡴࡧࠥ⠚"))
  return logging.DEBUG if bstack1lll1111ll11_opy_.lower() == bstack1l1llll_opy_ (u"ࠧࡺࡲࡶࡧࠥ⠛") else logging.INFO
def clear_logs():
  global bstack1lll111l1l11_opy_
  if os.path.exists(bstack1lll111l1l11_opy_):
    os.remove(bstack1lll111l1l11_opy_)
  if os.path.exists(bstack1ll1lllll111_opy_):
    os.remove(bstack1ll1lllll111_opy_)
def bstack1llll1l111_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def configure_logger(config, log_level):
  bstack1ll1lllll1l1_opy_ = log_level
  if bstack1l1llll_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨ⠜") in config and config[bstack1l1llll_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩ⠝")] in bstack1llllllllll1_opy_:
    bstack1ll1lllll1l1_opy_ = bstack1llllllllll1_opy_[config[bstack1l1llll_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪ⠞")]]
  if config.get(bstack1l1llll_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫ⠟"), False):
    logging.getLogger().setLevel(bstack1ll1lllll1l1_opy_)
    return bstack1ll1lllll1l1_opy_
  global bstack1lll111l1l11_opy_
  bstack1llll1l111_opy_()
  bstack1lll1111111l_opy_ = logging.Formatter(
    fmt=bstack1l1llll_opy_ (u"ࠪࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭⠠"),
    datefmt=bstack1l1llll_opy_ (u"ࠫࠪ࡟࠭ࠦ࡯࠰ࠩࡩ࡚ࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࡛ࠩ⠡"),
  )
  bstack1lll111111ll_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1lll111l1l11_opy_)
  file_handler.setFormatter(bstack1lll1111111l_opy_)
  bstack1lll111111ll_opy_.setFormatter(bstack1lll1111111l_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1lll111111ll_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1l1llll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡶࡪࡳ࡯ࡵࡧ࠱ࡶࡪࡳ࡯ࡵࡧࡢࡧࡴࡴ࡮ࡦࡥࡷ࡭ࡴࡴࠧ⠢"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1lll111111ll_opy_.setLevel(bstack1ll1lllll1l1_opy_)
  logging.getLogger().addHandler(bstack1lll111111ll_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1ll1lllll1l1_opy_
def bstack1ll1lllllll1_opy_(config):
  try:
    bstack1lll111l11l1_opy_ = set(bstack11111111111_opy_)
    bstack1lll1111lll1_opy_ = bstack1l1llll_opy_ (u"࠭ࠧ⠣")
    bstack1lll111111l1_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ⠤"))
    if not bstack1lll111111l1_opy_:
      logging.getLogger(__name__).debug(
        bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠥࡻ࡮ࡴࡧࡷ࠿ࠥ࡬ࡡ࡭࡮࡬ࡲ࡬ࠦࡢࡢࡥ࡮ࠤࡹࡵࠠࡤࡹࡧ࠱ࡷ࡫࡬ࡢࡶ࡬ࡺࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩ⠥")
      )
      bstack1lll111111l1_opy_ = bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬ⠦")
    with open(bstack1lll111111l1_opy_) as bstack1ll1llllllll_opy_:
      bstack1ll1llllll1l_opy_ = bstack1ll1llllllll_opy_.read()
      bstack1lll1111lll1_opy_ = re.sub(bstack1l1llll_opy_ (u"ࡵࠫࡣ࠮࡜ࡴ࠭ࠬࡃࠨ࠴ࠪࠥ࡞ࡱࠫ⠧"), bstack1l1llll_opy_ (u"ࠫࠬ⠨"), bstack1ll1llllll1l_opy_, flags=re.M)
      bstack1lll1111lll1_opy_ = re.sub(
        bstack1l1llll_opy_ (u"ࡷ࠭࡞ࠩ࡞ࡶ࠯࠮ࡅࠨࠨ⠩") + bstack1l1llll_opy_ (u"࠭ࡼࠨ⠪").join(bstack1lll111l11l1_opy_) + bstack1l1llll_opy_ (u"ࠧࠪ࠰࠭ࠨࠬ⠫"),
        bstack1l1llll_opy_ (u"ࡳࠩ࡟࠶࠿࡛ࠦࡓࡇࡇࡅࡈ࡚ࡅࡅ࡟ࠪ⠬"),
        bstack1lll1111lll1_opy_, flags=re.M | re.I
      )
    def bstack1ll1lllll11l_opy_(dic):
      bstack1lll11111l11_opy_ = {}
      for key, value in dic.items():
        if key in bstack1lll111l11l1_opy_:
          bstack1lll11111l11_opy_[key] = bstack1l1llll_opy_ (u"ࠩ࡞ࡖࡊࡊࡁࡄࡖࡈࡈࡢ࠭⠭")
        else:
          if isinstance(value, dict):
            bstack1lll11111l11_opy_[key] = bstack1ll1lllll11l_opy_(value)
          else:
            bstack1lll11111l11_opy_[key] = value
      return bstack1lll11111l11_opy_
    bstack1lll11111l11_opy_ = bstack1ll1lllll11l_opy_(config)
    return {
      bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭⠮"): bstack1lll1111lll1_opy_,
      bstack1l1llll_opy_ (u"ࠫ࡫࡯࡮ࡢ࡮ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧ⠯"): json.dumps(bstack1lll11111l11_opy_)
    }
  except Exception as e:
    return {}
def bstack1ll1llll1l11_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack1l1llll_opy_ (u"ࠬࡲ࡯ࡨࠩ⠰"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack1l11l1l1l_opy_ = os.path.join(log_dir, bstack1l1llll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡣࡰࡰࡩ࡭࡬ࡹࠧ⠱"))
  if not os.path.exists(bstack1l11l1l1l_opy_):
    bstack1ll1llll1ll1_opy_ = {
      bstack1l1llll_opy_ (u"ࠢࡪࡰ࡬ࡴࡦࡺࡨࠣ⠲"): str(inipath),
      bstack1l1llll_opy_ (u"ࠣࡴࡲࡳࡹࡶࡡࡵࡪࠥ⠳"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack1l1llll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡦࡳࡳ࡬ࡩࡨࡵ࠱࡮ࡸࡵ࡮ࠨ⠴")), bstack1l1llll_opy_ (u"ࠪࡻࠬ⠵")) as bstack1ll1llllll11_opy_:
      bstack1ll1llllll11_opy_.write(json.dumps(bstack1ll1llll1ll1_opy_))
def bstack1ll1llll1l1l_opy_():
  try:
    bstack1l11l1l1l_opy_ = os.path.join(os.getcwd(), bstack1l1llll_opy_ (u"ࠫࡱࡵࡧࠨ⠶"), bstack1l1llll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡩ࡯࡯ࡨ࡬࡫ࡸ࠴ࡪࡴࡱࡱࠫ⠷"))
    if os.path.exists(bstack1l11l1l1l_opy_):
      with open(bstack1l11l1l1l_opy_, bstack1l1llll_opy_ (u"࠭ࡲࠨ⠸")) as bstack1ll1llllll11_opy_:
        bstack1lll11111ll1_opy_ = json.load(bstack1ll1llllll11_opy_)
      return bstack1lll11111ll1_opy_.get(bstack1l1llll_opy_ (u"ࠧࡪࡰ࡬ࡴࡦࡺࡨࠨ⠹"), bstack1l1llll_opy_ (u"ࠨࠩ⠺")), bstack1lll11111ll1_opy_.get(bstack1l1llll_opy_ (u"ࠩࡵࡳࡴࡺࡰࡢࡶ࡫ࠫ⠻"), bstack1l1llll_opy_ (u"ࠪࠫ⠼"))
  except Exception as e:
    get_logger(__name__).debug(bstack1l1llll_opy_ (u"ࠦ࡬࡫ࡴࡠࡲࡼࡸࡪࡹࡴࡠࡥࡲࡲ࡫࡯ࡧࡠࡲࡤࡸ࡭ࡹࠠࡳࡧࡤࡨࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡾ࠼ࠣࡿࢂࠨ⠽").format(type(e).__name__, e), exc_info=True)
  return None, None
def bstack1lll11111111_opy_():
  try:
    bstack1l11l1l1l_opy_ = os.path.join(os.getcwd(), bstack1l1llll_opy_ (u"ࠬࡲ࡯ࡨࠩ⠾"), bstack1l1llll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡣࡰࡰࡩ࡭࡬ࡹ࠮࡫ࡵࡲࡲࠬ⠿"))
    if os.path.exists(bstack1l11l1l1l_opy_):
      os.remove(bstack1l11l1l1l_opy_)
  except Exception as e:
    get_logger(__name__).debug(bstack1l1llll_opy_ (u"ࠢࡳࡧࡰࡳࡻ࡫࡟ࡤࡱࡱࡪ࡮࡭࡟ࡱࡣࡷ࡬ࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡾ࠼ࠣࡿࢂࠨ⡀").format(type(e).__name__, e), exc_info=True)
def bstack1ll11111_opy_(config):
  status = True
  failure = None
  bstack1ll1lllll1ll_opy_ = None
  try:
    try:
      from bstack_utils.performance_tester import PerformanceTester
    except Exception:
      PerformanceTester = None
    start_time = time.time()
    from bstack_utils.helper import global_config, bstack11l11l111l_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack1lll111l1l11_opy_
    bstack1ll1lllll1ll_opy_ = PerformanceTester.mark_start(EVENTS.bstack1lllllll1111_opy_.value) if PerformanceTester else None
    if config.get(bstack1l1llll_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪ⡁"), False):
      status = False
      failure = bstack1l1llll_opy_ (u"ࠤࡶ࡯࡮ࡶࡰࡦࡦ࠽ࠤࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸࡃࡴࡳࡷࡨࠦ⡂")
      return
    uuid = os.getenv(bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ⡃")) if os.getenv(bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ⡄")) else global_config.get_property(bstack1l1llll_opy_ (u"ࠧࡹࡤ࡬ࡔࡸࡲࡎࡪࠢ⡅"))
    if not uuid or uuid == bstack1l1llll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ⡆"):
      status = False
      failure = bstack1l1llll_opy_ (u"ࠢࡴ࡭࡬ࡴࡵ࡫ࡤ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࡢࡸࡪࡹࡴࡩࡷࡥࡣࡺࡻࡩࡥࡡࡤࡲࡩࡥࡳࡥ࡭ࡕࡹࡳࡏࡤࠣ⡇")
      return
    bstack1lll111l1111_opy_ = [bstack1l1llll_opy_ (u"ࠨࡴࡨࡵࡺ࡯ࡲࡦ࡯ࡨࡲࡹࡹ࠮ࡵࡺࡷࠫ⡈"), bstack1l1llll_opy_ (u"ࠩࡓ࡭ࡵ࡬ࡩ࡭ࡧࠪ⡉"), bstack1l1llll_opy_ (u"ࠪࡴࡾࡶࡲࡰ࡬ࡨࡧࡹ࠴ࡴࡰ࡯࡯ࠫ⡊"), bstack1lll111l1l11_opy_, bstack1ll1lllll111_opy_]
    bstack1ll1llll1lll_opy_, root_path = bstack1ll1llll1l1l_opy_()
    if bstack1ll1llll1lll_opy_ != None:
      bstack1lll111l1111_opy_.append(bstack1ll1llll1lll_opy_)
    if root_path != None:
      bstack1lll111l1111_opy_.append(os.path.join(root_path, bstack1l1llll_opy_ (u"ࠫࡨࡵ࡮ࡧࡶࡨࡷࡹ࠴ࡰࡺࠩ⡋")))
    bstack1lll1111l111_opy_ = os.path.join(os.getcwd(), bstack1l1llll_opy_ (u"ࠬࡲ࡯ࡨࠩ⡌"), bstack1l1llll_opy_ (u"࠭࡫ࡦࡻ࠰ࡱࡪࡺࡲࡪࡥࡶ࠲࡯ࡹ࡯࡯ࠩ⡍"))
    if os.path.exists(bstack1lll1111l111_opy_):
      bstack1lll111l1111_opy_.append(bstack1lll1111l111_opy_)
    output_file = os.path.join(tempfile.gettempdir(), bstack1l1llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠭࡭ࡱࡪࡷ࠲࠭⡎") + uuid + bstack1l1llll_opy_ (u"ࠨ࠰ࡷࡥࡷ࠴ࡧࡻࠩ⡏"))
    bstack1lll1111llll_opy_ = []
    with tarfile.open(output_file, bstack1l1llll_opy_ (u"ࠤࡺ࠾࡬ࢀࠢ⡐")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1lll111l1111_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except Exception as bstack1lll11111lll_opy_:
          bstack1lll1111llll_opy_.append(bstack1l1llll_opy_ (u"ࠥࡿࢂࡀࠠࡼࡿࠥ⡑").format(os.path.basename(file), bstack1lll11111lll_opy_))
      bstack1lll1111l1ll_opy_ = bstack1ll1lllllll1_opy_(config)
      if not bstack1lll1111l1ll_opy_ and failure is None:
        failure = bstack1l1llll_opy_ (u"ࠦࡷ࡫ࡤࡢࡥࡷ࡭ࡴࡴ࡟ࡧࡣ࡬ࡰࡪࡪࠢ⡒")
      for name, data in bstack1lll1111l1ll_opy_.items():
        tarinfo = tarfile.TarInfo(name)
        bstack1lll111l111l_opy_ = data.encode()
        tarinfo.size = len(bstack1lll111l111l_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1lll111l111l_opy_))
    if bstack1lll1111llll_opy_ and failure is None:
      failure = bstack1l1llll_opy_ (u"ࠧࡧࡲࡤࡪ࡬ࡺࡪࡥࡡࡥࡦࡢࡪࡦ࡯࡬ࡦࡦࠣ࡟ࢀࢃ࡝࠻ࠢࡾࢁࠧ⡓").format(len(bstack1lll1111llll_opy_), bstack1l1llll_opy_ (u"࠭࠻ࠡࠩ⡔").join(bstack1lll1111llll_opy_))[:300]
    multipart_data = MultipartEncoder(
      fields= {
        bstack1l1llll_opy_ (u"ࠧࡥࡣࡷࡥࠬ⡕"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1l1llll_opy_ (u"ࠨࡴࡥࠫ⡖")), bstack1l1llll_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯ࡹ࠯ࡪࡾ࡮ࡶࠧ⡗")),
        bstack1l1llll_opy_ (u"ࠪࡧࡱ࡯ࡥ࡯ࡶࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬ⡘"): uuid
      }
    )
    bstack1ll1llll11ll_opy_ = bstack11l11l111l_opy_(cli.config, [bstack1l1llll_opy_ (u"ࠦࡦࡶࡩࡴࠤ⡙"), bstack1l1llll_opy_ (u"ࠧࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠧ⡚"), bstack1l1llll_opy_ (u"ࠨࡵࡱ࡮ࡲࡥࡩࠨ⡛")], bstack1llllll1ll1l_opy_)
    from bstack_utils.helper import get_ca_cert_path
    bstack1l11l1ll11_opy_ = {
      bstack1l1llll_opy_ (u"ࠧࡥࡣࡷࡥࠬ⡜"): multipart_data,
      bstack1l1llll_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩ⡝"): {bstack1l1llll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨ⡞"): multipart_data.content_type},
      bstack1l1llll_opy_ (u"ࠪࡥࡺࡺࡨࠨ⡟"): (config[bstack1l1llll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭⡠")], config[bstack1l1llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ⡡")]),
    }
    cert_path = get_ca_cert_path(config)
    if cert_path:
      bstack1l11l1ll11_opy_[bstack1l1llll_opy_ (u"࠭ࡶࡦࡴ࡬ࡪࡾ࠭⡢")] = cert_path
    response = requests.post(
      bstack1l1llll_opy_ (u"ࠢࡼࡿ࠲ࡧࡱ࡯ࡥ࡯ࡶ࠰ࡰࡴ࡭ࡳ࠰ࡷࡳࡰࡴࡧࡤࠣ⡣").format(bstack1ll1llll11ll_opy_),
      **bstack1l11l1ll11_opy_
    )
    os.remove(output_file)
    if response.status_code != 200:
      status = False
      failure = bstack1l1llll_opy_ (u"ࠣࡊࡗࡘࡕࠦࡻࡾࠢ࠰ࠤࢀࢃࠢ⡤").format(response.status_code, (response.text or bstack1l1llll_opy_ (u"ࠩࠪ⡥"))[:200])
      get_logger().debug(bstack1l1llll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡸࡴࡱࡵࡡࡥࠢ࡯ࡳ࡬ࡹ࠺ࠡࡽࢀࠫ⡦").format(response.status_code))
  except Exception as e:
    status = False
    failure = bstack1l1llll_opy_ (u"ࠦࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡹࠠࡦࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃࠢ⡧").format(e)
    get_logger().debug(bstack1l1llll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥࡲ࡯ࡨࡵ࠽ࠫ⡨") + str(e))
  finally:
    try:
      clear_logs()
      bstack1lll11111111_opy_()
    except Exception as bstack1lll1111ll1l_opy_:
      if failure is None:
        status = False
        failure = bstack1l1llll_opy_ (u"ࠨࡣ࡭ࡧࡤࡲࡺࡶ࡟ࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡽࢀࠦ⡩").format(bstack1lll1111ll1l_opy_)
    if PerformanceTester and bstack1ll1lllll1ll_opy_:
      PerformanceTester.end(EVENTS.bstack1lllllll1111_opy_.value, bstack1ll1lllll1ll_opy_ + bstack1l1llll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ⡪"), bstack1ll1lllll1ll_opy_ + bstack1l1llll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ⡫"), status=status, failure=failure, test_name=None)
    try:
      elapsed = time.time() - start_time
      get_logger().debug(bstack1l1llll_opy_ (u"ࠤࡶࡩࡳࡪ࡟࡭ࡱࡪࡷࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠡ࡫ࡱࠤࢀࡀ࠮࠴ࡨࢀࠤࡸ࡫ࡣࡰࡰࡧࡷࠧ⡬").format(elapsed))
    except Exception:
      pass