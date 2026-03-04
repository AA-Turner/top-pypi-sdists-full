# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
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
from bstack_utils.constants import bstack111ll1l1lll_opy_, EVENTS, bstack111ll111111_opy_, bstack111l1lll1ll_opy_, STAGE
import tempfile
import json
bstack11111111111_opy_ = os.getenv(bstack1lll1l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡊࡣࡋࡏࡌࡆࠤℐ"), None) or os.path.join(tempfile.gettempdir(), bstack1lll1l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡦࡨࡦࡺ࡭࠮࡭ࡱࡪࠦℑ"))
bstack1111111llll_opy_ = os.path.join(bstack1lll1l_opy_ (u"ࠥࡰࡴ࡭ࠢℒ"), bstack1lll1l_opy_ (u"ࠫࡸࡪ࡫࠮ࡥ࡯࡭࠲ࡪࡥࡣࡷࡪ࠲ࡱࡵࡧࠨℓ"))
_111111111l1_opy_ = threading.Lock()
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1lll1l_opy_ (u"ࠬࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨ℔"),
      datefmt=bstack1lll1l_opy_ (u"࡚࠭ࠥ࠯ࠨࡱ࠲ࠫࡤࡕࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࡝ࠫℕ"),
      stream=sys.stdout
    )
  return logger
def bstack1l1l1l111_opy_(name=__name__, level=logging.DEBUG):
  bstack1lll1l_opy_ (u"ࠢࠣࠤࠍࠤࠥࡘࡥࡵࡷࡵࡲࡸࠦࡡࠡ࡮ࡲ࡫࡬࡫ࡲࠡࡶ࡫ࡥࡹࠦࡷࡳ࡫ࡷࡩࡸࠦ࡯࡯࡮ࡼࠤࡹࡵࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠲ࡱࡵࡧࠡࡨ࡬ࡰࡪࠐࠠࠡࡅࡵࡩࡦࡺࡥࡴࠢࡤࡲࡩࠦ࡭ࡢࡰࡤ࡫ࡪࡹࠠࡪࡶࡶࠤࡴࡽ࡮ࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥ࡬ࡩ࡭ࡧࠣ࡬ࡦࡴࡤ࡭ࡧࡵࠎࠥࠦࡏ࡯࡮ࡼࠤࡪࡴࡡࡣ࡮ࡨࡷࠥࡲ࡯ࡨࡩ࡬ࡲ࡬ࠦࡩࡧࠢࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࡤࡒࡏࡈࡕࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴࠡࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠣ࡭ࡸࠦࡳࡦࡶࠣࡸࡴࠦࡡࠡࡶࡵࡹࡹ࡮ࡹࠡࡸࡤࡰࡺ࡫ࠊࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࡴࡡ࡮ࡧ࠽ࠤࡑࡵࡧࡨࡧࡵࠤࡳࡧ࡭ࡦࠢࠫࡨࡪ࡬ࡡࡶ࡮ࡷࡷࠥࡺ࡯ࠡࡡࡢࡲࡦࡳࡥࡠࡡࠬࠎࠥࠦࠠࠡ࡮ࡨࡺࡪࡲ࠺ࠡࡎࡲ࡫࡬࡯࡮ࡨࠢ࡯ࡩࡻ࡫࡬ࠡࠪࡧࡩ࡫ࡧࡵ࡭ࡶࡶࠤࡹࡵࠠࡅࡇࡅ࡙ࡌ࠯ࠊࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡ࡮ࡲ࡫࡬࡯࡮ࡨ࠰ࡏࡳ࡬࡭ࡥࡳ࠼ࠣࡇࡴࡴࡦࡪࡩࡸࡶࡪࡪࠠ࡭ࡱࡪ࡫ࡪࡸࠠࡵࡪࡤࡸࠥࡽࡲࡪࡶࡨࡷࠥࡵ࡮࡭ࡻࠣࡸࡴࠦࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠱ࡰࡴ࡭ࠠࠩ࡫ࡩࠤࡪࡴࡡࡣ࡮ࡨࡨ࠮ࠐࠠࠡࠤࠥࠦ№")
  logger_name = bstack1lll1l_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠳ࢁ࠰ࡾࠤ℗").format(name)
  logger = logging.getLogger(logger_name)
  is_enabled = os.getenv(bstack1lll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࡤࡒࡏࡈࡕࠪ℘"), bstack1lll1l_opy_ (u"ࠪࠫℙ")).lower() == bstack1lll1l_opy_ (u"ࠫࡹࡸࡵࡦࠩℚ")
  if not is_enabled:
    logger.setLevel(logging.CRITICAL)
    logger.propagate = False
    return logger
  with _111111111l1_opy_:
    if logger.handlers:
      return logger
    bstack11111111l1l_opy_ = os.path.join(os.getcwd(), bstack1lll1l_opy_ (u"ࠬࡲ࡯ࡨࠩℛ"), bstack1lll1l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠱ࡰࡴ࡭ࠧℜ"))
    log_dir = os.path.dirname(bstack11111111l1l_opy_)
    if not os.path.exists(log_dir):
      os.makedirs(log_dir)
    bstack11111111ll1_opy_ = logging.FileHandler(bstack11111111l1l_opy_)
    bstack111111l11l1_opy_ = logging.Formatter(
      fmt=bstack1lll1l_opy_ (u"ࠧࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࡡࠠࡔࡆࡎ࠱ࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠡ࡟ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨℝ"),
      datefmt=bstack1lll1l_opy_ (u"ࠨࠧ࡜࠱ࠪࡳ࠭ࠦࡦࡗࠩࡍࡀࠥࡎ࠼ࠨࡗ࡟࠭℞"),
    )
    bstack11111111ll1_opy_.setFormatter(bstack111111l11l1_opy_)
    bstack11111111ll1_opy_.setLevel(level)
    bstack11111111ll1_opy_.addFilter(lambda r: r.name != bstack1lll1l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࠮ࡳࡧࡰࡳࡹ࡫࠮ࡳࡧࡰࡳࡹ࡫࡟ࡤࡱࡱࡲࡪࡩࡴࡪࡱࡱࠫ℟"))
    logger.addHandler(bstack11111111ll1_opy_)
    logger.setLevel(level)
    logger.propagate = False
  return logger
def bstack1l1llllll11_opy_():
  bstack1111111ll11_opy_ = os.environ.get(bstack1lll1l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡇࡉࡇ࡛ࡇࠣ℠"), bstack1lll1l_opy_ (u"ࠦ࡫ࡧ࡬ࡴࡧࠥ℡"))
  return logging.DEBUG if bstack1111111ll11_opy_.lower() == bstack1lll1l_opy_ (u"ࠧࡺࡲࡶࡧࠥ™") else logging.INFO
def bstack1l11l1lll11_opy_():
  global bstack11111111111_opy_
  if os.path.exists(bstack11111111111_opy_):
    os.remove(bstack11111111111_opy_)
  if os.path.exists(bstack1111111llll_opy_):
    os.remove(bstack1111111llll_opy_)
def bstack111ll11l1_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def configure_logger(config, log_level):
  bstack1111111l1l1_opy_ = log_level
  if bstack1lll1l_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨ℣") in config and config[bstack1lll1l_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩℤ")] in bstack111ll111111_opy_:
    bstack1111111l1l1_opy_ = bstack111ll111111_opy_[config[bstack1lll1l_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪ℥")]]
  if config.get(bstack1lll1l_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫΩ"), False):
    logging.getLogger().setLevel(bstack1111111l1l1_opy_)
    return bstack1111111l1l1_opy_
  global bstack11111111111_opy_
  bstack111ll11l1_opy_()
  bstack111111l1ll1_opy_ = logging.Formatter(
    fmt=bstack1lll1l_opy_ (u"ࠪࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭℧"),
    datefmt=bstack1lll1l_opy_ (u"ࠫࠪ࡟࠭ࠦ࡯࠰ࠩࡩ࡚ࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࡛ࠩℨ"),
  )
  bstack1lllllllllll_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack11111111111_opy_)
  file_handler.setFormatter(bstack111111l1ll1_opy_)
  bstack1lllllllllll_opy_.setFormatter(bstack111111l1ll1_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1lllllllllll_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1lll1l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡶࡪࡳ࡯ࡵࡧ࠱ࡶࡪࡳ࡯ࡵࡧࡢࡧࡴࡴ࡮ࡦࡥࡷ࡭ࡴࡴࠧ℩"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1lllllllllll_opy_.setLevel(bstack1111111l1l1_opy_)
  logging.getLogger().addHandler(bstack1lllllllllll_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1111111l1l1_opy_
def bstack11111111l11_opy_(config):
  try:
    bstack111111l111l_opy_ = set(bstack111l1lll1ll_opy_)
    bstack1111111l1ll_opy_ = bstack1lll1l_opy_ (u"࠭ࠧK")
    with open(bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪÅ")) as bstack1111111111l_opy_:
      bstack11111111lll_opy_ = bstack1111111111l_opy_.read()
      bstack1111111l1ll_opy_ = re.sub(bstack1lll1l_opy_ (u"ࡳࠩࡡࠬࡡࡹࠫࠪࡁࠦ࠲࠯ࠪ࡜࡯ࠩℬ"), bstack1lll1l_opy_ (u"ࠩࠪℭ"), bstack11111111lll_opy_, flags=re.M)
      bstack1111111l1ll_opy_ = re.sub(
        bstack1lll1l_opy_ (u"ࡵࠫࡣ࠮࡜ࡴ࠭ࠬࡃ࠭࠭℮") + bstack1lll1l_opy_ (u"ࠫࢁ࠭ℯ").join(bstack111111l111l_opy_) + bstack1lll1l_opy_ (u"ࠬ࠯࠮ࠫࠦࠪℰ"),
        bstack1lll1l_opy_ (u"ࡸࠧ࡝࠴࠽ࠤࡠࡘࡅࡅࡃࡆࡘࡊࡊ࡝ࠨℱ"),
        bstack1111111l1ll_opy_, flags=re.M | re.I
      )
    def bstack1llllllll1ll_opy_(dic):
      bstack111111111ll_opy_ = {}
      for key, value in dic.items():
        if key in bstack111111l111l_opy_:
          bstack111111111ll_opy_[key] = bstack1lll1l_opy_ (u"ࠧ࡜ࡔࡈࡈࡆࡉࡔࡆࡆࡠࠫℲ")
        else:
          if isinstance(value, dict):
            bstack111111111ll_opy_[key] = bstack1llllllll1ll_opy_(value)
          else:
            bstack111111111ll_opy_[key] = value
      return bstack111111111ll_opy_
    bstack111111111ll_opy_ = bstack1llllllll1ll_opy_(config)
    return {
      bstack1lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫℳ"): bstack1111111l1ll_opy_,
      bstack1lll1l_opy_ (u"ࠩࡩ࡭ࡳࡧ࡬ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬℴ"): json.dumps(bstack111111111ll_opy_)
    }
  except Exception as e:
    return {}
def bstack1111111lll1_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack1lll1l_opy_ (u"ࠪࡰࡴ࡭ࠧℵ"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack1lllll1lll1_opy_ = os.path.join(log_dir, bstack1lll1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷࠬℶ"))
  if not os.path.exists(bstack1lllll1lll1_opy_):
    bstack111111l11ll_opy_ = {
      bstack1lll1l_opy_ (u"ࠧ࡯࡮ࡪࡲࡤࡸ࡭ࠨℷ"): str(inipath),
      bstack1lll1l_opy_ (u"ࠨࡲࡰࡱࡷࡴࡦࡺࡨࠣℸ"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack1lll1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡤࡱࡱࡪ࡮࡭ࡳ࠯࡬ࡶࡳࡳ࠭ℹ")), bstack1lll1l_opy_ (u"ࠨࡹࠪ℺")) as bstack111111l1111_opy_:
      bstack111111l1111_opy_.write(json.dumps(bstack111111l11ll_opy_))
def bstack1111111l111_opy_():
  try:
    bstack1lllll1lll1_opy_ = os.path.join(os.getcwd(), bstack1lll1l_opy_ (u"ࠩ࡯ࡳ࡬࠭℻"), bstack1lll1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶ࠲࡯ࡹ࡯࡯ࠩℼ"))
    if os.path.exists(bstack1lllll1lll1_opy_):
      with open(bstack1lllll1lll1_opy_, bstack1lll1l_opy_ (u"ࠫࡷ࠭ℽ")) as bstack111111l1111_opy_:
        bstack1llllllllll1_opy_ = json.load(bstack111111l1111_opy_)
      return bstack1llllllllll1_opy_.get(bstack1lll1l_opy_ (u"ࠬ࡯࡮ࡪࡲࡤࡸ࡭࠭ℾ"), bstack1lll1l_opy_ (u"࠭ࠧℿ")), bstack1llllllllll1_opy_.get(bstack1lll1l_opy_ (u"ࠧࡳࡱࡲࡸࡵࡧࡴࡩࠩ⅀"), bstack1lll1l_opy_ (u"ࠨࠩ⅁"))
  except:
    pass
  return None, None
def bstack1111111l11l_opy_():
  try:
    bstack1lllll1lll1_opy_ = os.path.join(os.getcwd(), bstack1lll1l_opy_ (u"ࠩ࡯ࡳ࡬࠭⅂"), bstack1lll1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶ࠲࡯ࡹ࡯࡯ࠩ⅃"))
    if os.path.exists(bstack1lllll1lll1_opy_):
      os.remove(bstack1lllll1lll1_opy_)
  except:
    pass
def bstack11ll1l1l11_opy_(config):
  try:
    try:
      from bstack_utils.bstack1l1ll1l111_opy_ import bstack1l11l11ll1_opy_
    except Exception:
      bstack1l11l11ll1_opy_ = None
    start_time = time.time()
    from bstack_utils.helper import global_config, bstack1l1ll1l11l_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack11111111111_opy_
    if config.get(bstack1lll1l_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭⅄"), False):
      return
    uuid = os.getenv(bstack1lll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪⅅ")) if os.getenv(bstack1lll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫⅆ")) else global_config.get_property(bstack1lll1l_opy_ (u"ࠢࡴࡦ࡮ࡖࡺࡴࡉࡥࠤⅇ"))
    if not uuid or uuid == bstack1lll1l_opy_ (u"ࠨࡰࡸࡰࡱ࠭ⅈ"):
      return
    bstack1lllllllll1l_opy_ = bstack1l11l11ll1_opy_.bstack1111l1lll_opy_(EVENTS.bstack111ll1l1ll1_opy_.value) if bstack1l11l11ll1_opy_ else None
    bstack1lllllllll11_opy_ = [bstack1lll1l_opy_ (u"ࠩࡵࡩࡶࡻࡩࡳࡧࡰࡩࡳࡺࡳ࠯ࡶࡻࡸࠬⅉ"), bstack1lll1l_opy_ (u"ࠪࡔ࡮ࡶࡦࡪ࡮ࡨࠫ⅊"), bstack1lll1l_opy_ (u"ࠫࡵࡿࡰࡳࡱ࡭ࡩࡨࡺ࠮ࡵࡱࡰࡰࠬ⅋"), bstack11111111111_opy_, bstack1111111llll_opy_]
    bstack1111111ll1l_opy_, root_path = bstack1111111l111_opy_()
    if bstack1111111ll1l_opy_ != None:
      bstack1lllllllll11_opy_.append(bstack1111111ll1l_opy_)
    if root_path != None:
      bstack1lllllllll11_opy_.append(os.path.join(root_path, bstack1lll1l_opy_ (u"ࠬࡩ࡯࡯ࡨࡷࡩࡸࡺ࠮ࡱࡻࠪ⅌")))
    bstack111111l1lll_opy_ = os.path.join(os.getcwd(), bstack1lll1l_opy_ (u"࠭࡬ࡰࡩࠪ⅍"), bstack1lll1l_opy_ (u"ࠧ࡬ࡧࡼ࠱ࡲ࡫ࡴࡳ࡫ࡦࡷ࠳ࡰࡳࡰࡰࠪⅎ"))
    if os.path.exists(bstack111111l1lll_opy_):
      bstack1lllllllll11_opy_.append(bstack111111l1lll_opy_)
    output_file = os.path.join(tempfile.gettempdir(), bstack1lll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠮࡮ࡲ࡫ࡸ࠳ࠧ⅏") + uuid + bstack1lll1l_opy_ (u"ࠩ࠱ࡸࡦࡸ࠮ࡨࡼࠪ⅐"))
    with tarfile.open(output_file, bstack1lll1l_opy_ (u"ࠥࡻ࠿࡭ࡺࠣ⅑")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1lllllllll11_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack11111111l11_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack111111l1l1l_opy_ = data.encode()
        tarinfo.size = len(bstack111111l1l1l_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack111111l1l1l_opy_))
    bstack1lllllll1_opy_ = MultipartEncoder(
      fields= {
        bstack1lll1l_opy_ (u"ࠫࡩࡧࡴࡢࠩ⅒"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1lll1l_opy_ (u"ࠬࡸࡢࠨ⅓")), bstack1lll1l_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳ࡽ࠳ࡧࡻ࡫ࡳࠫ⅔")),
        bstack1lll1l_opy_ (u"ࠧࡤ࡮࡬ࡩࡳࡺࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ⅕"): uuid
      }
    )
    bstack111111l1l11_opy_ = bstack1l1ll1l11l_opy_(cli.config, [bstack1lll1l_opy_ (u"ࠣࡣࡳ࡭ࡸࠨ⅖"), bstack1lll1l_opy_ (u"ࠤࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠤ⅗"), bstack1lll1l_opy_ (u"ࠥࡹࡵࡲ࡯ࡢࡦࠥ⅘")], bstack111ll1l1lll_opy_)
    response = requests.post(
      bstack1lll1l_opy_ (u"ࠦࢀࢃ࠯ࡤ࡮࡬ࡩࡳࡺ࠭࡭ࡱࡪࡷ࠴ࡻࡰ࡭ࡱࡤࡨࠧ⅙").format(bstack111111l1l11_opy_),
      data=bstack1lllllll1_opy_,
      headers={bstack1lll1l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ⅚"): bstack1lllllll1_opy_.content_type},
      auth=(config[bstack1lll1l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ⅛")], config[bstack1lll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ⅜")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1lll1l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡶࡲ࡯ࡳࡦࡪࠠ࡭ࡱࡪࡷ࠿ࠦࠧ⅝") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1lll1l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡲࡩ࡯࡮ࡨࠢ࡯ࡳ࡬ࡹ࠺ࠨ⅞") + str(e))
  finally:
    try:
      bstack1l11l1lll11_opy_()
      bstack1111111l11l_opy_()
    except:
      pass
    if bstack1l11l11ll1_opy_ and bstack1lllllllll1l_opy_:
      bstack1l11l11ll1_opy_.end(EVENTS.bstack111ll1l1ll1_opy_.value, bstack1lllllllll1l_opy_ + bstack1lll1l_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ⅟"), bstack1lllllllll1l_opy_ + bstack1lll1l_opy_ (u"ࠦ࠿࡫࡮ࡥࠤⅠ"), status=True, failure=None, test_name=None)
    try:
      elapsed = time.time() - start_time
      get_logger().debug(bstack1lll1l_opy_ (u"ࠧࡹࡥ࡯ࡦࡢࡰࡴ࡭ࡳࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠤ࡮ࡴࠠࡼ࠼࠱࠷࡫ࢃࠠࡴࡧࡦࡳࡳࡪࡳࠣⅡ").format(elapsed))
    except Exception:
      pass