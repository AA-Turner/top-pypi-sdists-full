# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
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
from bstack_utils.constants import bstack1111lll11l1_opy_, EVENTS, bstack1111ll1ll1l_opy_, bstack111llll1111_opy_, STAGE
import tempfile
import json
bstack1111l1lll11_opy_ = os.getenv(bstack1ll111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡊࡣࡋࡏࡌࡆࠤ᱀"), None) or os.path.join(tempfile.gettempdir(), bstack1ll111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡦࡨࡦࡺ࡭࠮࡭ࡱࡪࠦ᱁"))
bstack1111ll11lll_opy_ = os.path.join(bstack1ll111_opy_ (u"ࠥࡰࡴ࡭ࠢ᱂"), bstack1ll111_opy_ (u"ࠫࡸࡪ࡫࠮ࡥ࡯࡭࠲ࡪࡥࡣࡷࡪ࠲ࡱࡵࡧࠨ᱃"))
_1111lll1l11_opy_ = threading.Lock()
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1ll111_opy_ (u"ࠬࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨ᱄"),
      datefmt=bstack1ll111_opy_ (u"࡚࠭ࠥ࠯ࠨࡱ࠲ࠫࡤࡕࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࡝ࠫ᱅"),
      stream=sys.stdout
    )
  return logger
def bstack1111l1ll1_opy_(name=__name__, level=logging.DEBUG):
  bstack1ll111_opy_ (u"ࠢࠣࠤࠍࠤࠥࡘࡥࡵࡷࡵࡲࡸࠦࡡࠡ࡮ࡲ࡫࡬࡫ࡲࠡࡶ࡫ࡥࡹࠦࡷࡳ࡫ࡷࡩࡸࠦ࡯࡯࡮ࡼࠤࡹࡵࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠲ࡱࡵࡧࠡࡨ࡬ࡰࡪࠐࠠࠡࡅࡵࡩࡦࡺࡥࡴࠢࡤࡲࡩࠦ࡭ࡢࡰࡤ࡫ࡪࡹࠠࡪࡶࡶࠤࡴࡽ࡮ࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥ࡬ࡩ࡭ࡧࠣ࡬ࡦࡴࡤ࡭ࡧࡵࠎࠥࠦࡏ࡯࡮ࡼࠤࡪࡴࡡࡣ࡮ࡨࡷࠥࡲ࡯ࡨࡩ࡬ࡲ࡬ࠦࡩࡧࠢࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࡤࡒࡏࡈࡕࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴࠡࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠣ࡭ࡸࠦࡳࡦࡶࠣࡸࡴࠦࡡࠡࡶࡵࡹࡹ࡮ࡹࠡࡸࡤࡰࡺ࡫ࠊࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࡴࡡ࡮ࡧ࠽ࠤࡑࡵࡧࡨࡧࡵࠤࡳࡧ࡭ࡦࠢࠫࡨࡪ࡬ࡡࡶ࡮ࡷࡷࠥࡺ࡯ࠡࡡࡢࡲࡦࡳࡥࡠࡡࠬࠎࠥࠦࠠࠡ࡮ࡨࡺࡪࡲ࠺ࠡࡎࡲ࡫࡬࡯࡮ࡨࠢ࡯ࡩࡻ࡫࡬ࠡࠪࡧࡩ࡫ࡧࡵ࡭ࡶࡶࠤࡹࡵࠠࡅࡇࡅ࡙ࡌ࠯ࠊࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡ࡮ࡲ࡫࡬࡯࡮ࡨ࠰ࡏࡳ࡬࡭ࡥࡳ࠼ࠣࡇࡴࡴࡦࡪࡩࡸࡶࡪࡪࠠ࡭ࡱࡪ࡫ࡪࡸࠠࡵࡪࡤࡸࠥࡽࡲࡪࡶࡨࡷࠥࡵ࡮࡭ࡻࠣࡸࡴࠦࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠱ࡰࡴ࡭ࠠࠩ࡫ࡩࠤࡪࡴࡡࡣ࡮ࡨࡨ࠮ࠐࠠࠡࠤࠥࠦ᱆")
  logger_name = bstack1ll111_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠳ࢁ࠰ࡾࠤ᱇").format(name)
  logger = logging.getLogger(logger_name)
  is_enabled = os.getenv(bstack1ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࡤࡒࡏࡈࡕࠪ᱈"), bstack1ll111_opy_ (u"ࠪࠫ᱉")).lower() == bstack1ll111_opy_ (u"ࠫࡹࡸࡵࡦࠩ᱊")
  if not is_enabled:
    logger.setLevel(logging.CRITICAL)
    logger.propagate = False
    return logger
  with _1111lll1l11_opy_:
    if logger.handlers:
      return logger
    bstack1111ll1ll11_opy_ = os.path.join(os.getcwd(), bstack1ll111_opy_ (u"ࠬࡲ࡯ࡨࠩ᱋"), bstack1ll111_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠱ࡰࡴ࡭ࠧ᱌"))
    log_dir = os.path.dirname(bstack1111ll1ll11_opy_)
    if not os.path.exists(log_dir):
      os.makedirs(log_dir)
    bstack1111llll11l_opy_ = logging.FileHandler(bstack1111ll1ll11_opy_)
    bstack1111lll1lll_opy_ = logging.Formatter(
      fmt=bstack1ll111_opy_ (u"ࠧࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࡡࠠࡔࡆࡎ࠱ࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠡ࡟ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨᱍ"),
      datefmt=bstack1ll111_opy_ (u"ࠨࠧ࡜࠱ࠪࡳ࠭ࠦࡦࡗࠩࡍࡀࠥࡎ࠼ࠨࡗ࡟࠭ᱎ"),
    )
    bstack1111llll11l_opy_.setFormatter(bstack1111lll1lll_opy_)
    bstack1111llll11l_opy_.setLevel(level)
    bstack1111llll11l_opy_.addFilter(lambda r: r.name != bstack1ll111_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࠮ࡳࡧࡰࡳࡹ࡫࠮ࡳࡧࡰࡳࡹ࡫࡟ࡤࡱࡱࡲࡪࡩࡴࡪࡱࡱࠫᱏ"))
    logger.addHandler(bstack1111llll11l_opy_)
    logger.setLevel(level)
    logger.propagate = False
  return logger
def bstack1ll111l111l_opy_():
  bstack1111ll1l1ll_opy_ = os.environ.get(bstack1ll111_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡇࡉࡇ࡛ࡇࠣ᱐"), bstack1ll111_opy_ (u"ࠦ࡫ࡧ࡬ࡴࡧࠥ᱑"))
  return logging.DEBUG if bstack1111ll1l1ll_opy_.lower() == bstack1ll111_opy_ (u"ࠧࡺࡲࡶࡧࠥ᱒") else logging.INFO
def bstack1l11l11111l_opy_():
  global bstack1111l1lll11_opy_
  if os.path.exists(bstack1111l1lll11_opy_):
    os.remove(bstack1111l1lll11_opy_)
  if os.path.exists(bstack1111ll11lll_opy_):
    os.remove(bstack1111ll11lll_opy_)
def bstack111l11111_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def configure_logger(config, log_level):
  bstack1111ll1l111_opy_ = log_level
  if bstack1ll111_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨ᱓") in config and config[bstack1ll111_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩ᱔")] in bstack1111ll1ll1l_opy_:
    bstack1111ll1l111_opy_ = bstack1111ll1ll1l_opy_[config[bstack1ll111_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪ᱕")]]
  if config.get(bstack1ll111_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫ᱖"), False):
    logging.getLogger().setLevel(bstack1111ll1l111_opy_)
    return bstack1111ll1l111_opy_
  global bstack1111l1lll11_opy_
  bstack111l11111_opy_()
  bstack1111llll111_opy_ = logging.Formatter(
    fmt=bstack1ll111_opy_ (u"ࠪࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭᱗"),
    datefmt=bstack1ll111_opy_ (u"ࠫࠪ࡟࠭ࠦ࡯࠰ࠩࡩ࡚ࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࡛ࠩ᱘"),
  )
  bstack1111lll1111_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1111l1lll11_opy_)
  file_handler.setFormatter(bstack1111llll111_opy_)
  bstack1111lll1111_opy_.setFormatter(bstack1111llll111_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1111lll1111_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1ll111_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡶࡪࡳ࡯ࡵࡧ࠱ࡶࡪࡳ࡯ࡵࡧࡢࡧࡴࡴ࡮ࡦࡥࡷ࡭ࡴࡴࠧ᱙"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1111lll1111_opy_.setLevel(bstack1111ll1l111_opy_)
  logging.getLogger().addHandler(bstack1111lll1111_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1111ll1l111_opy_
def bstack1111lll111l_opy_(config):
  try:
    bstack1111ll11l1l_opy_ = set(bstack111llll1111_opy_)
    bstack1111ll11111_opy_ = bstack1ll111_opy_ (u"࠭ࠧᱚ")
    with open(bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪᱛ")) as bstack1111l1llll1_opy_:
      bstack1111ll11l11_opy_ = bstack1111l1llll1_opy_.read()
      bstack1111ll11111_opy_ = re.sub(bstack1ll111_opy_ (u"ࡳࠩࡡࠬࡡࡹࠫࠪࡁࠦ࠲࠯ࠪ࡜࡯ࠩᱜ"), bstack1ll111_opy_ (u"ࠩࠪᱝ"), bstack1111ll11l11_opy_, flags=re.M)
      bstack1111ll11111_opy_ = re.sub(
        bstack1ll111_opy_ (u"ࡵࠫࡣ࠮࡜ࡴ࠭ࠬࡃ࠭࠭ᱞ") + bstack1ll111_opy_ (u"ࠫࢁ࠭ᱟ").join(bstack1111ll11l1l_opy_) + bstack1ll111_opy_ (u"ࠬ࠯࠮ࠫࠦࠪᱠ"),
        bstack1ll111_opy_ (u"ࡸࠧ࡝࠴࠽ࠤࡠࡘࡅࡅࡃࡆࡘࡊࡊ࡝ࠨᱡ"),
        bstack1111ll11111_opy_, flags=re.M | re.I
      )
    def bstack1111lll1ll1_opy_(dic):
      bstack1111lll1l1l_opy_ = {}
      for key, value in dic.items():
        if key in bstack1111ll11l1l_opy_:
          bstack1111lll1l1l_opy_[key] = bstack1ll111_opy_ (u"ࠧ࡜ࡔࡈࡈࡆࡉࡔࡆࡆࡠࠫᱢ")
        else:
          if isinstance(value, dict):
            bstack1111lll1l1l_opy_[key] = bstack1111lll1ll1_opy_(value)
          else:
            bstack1111lll1l1l_opy_[key] = value
      return bstack1111lll1l1l_opy_
    bstack1111lll1l1l_opy_ = bstack1111lll1ll1_opy_(config)
    return {
      bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫᱣ"): bstack1111ll11111_opy_,
      bstack1ll111_opy_ (u"ࠩࡩ࡭ࡳࡧ࡬ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬᱤ"): json.dumps(bstack1111lll1l1l_opy_)
    }
  except Exception as e:
    return {}
def bstack1111ll1llll_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack1ll111_opy_ (u"ࠪࡰࡴ࡭ࠧᱥ"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack1llll1ll11l_opy_ = os.path.join(log_dir, bstack1ll111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷࠬᱦ"))
  if not os.path.exists(bstack1llll1ll11l_opy_):
    bstack1111l1lllll_opy_ = {
      bstack1ll111_opy_ (u"ࠧ࡯࡮ࡪࡲࡤࡸ࡭ࠨᱧ"): str(inipath),
      bstack1ll111_opy_ (u"ࠨࡲࡰࡱࡷࡴࡦࡺࡨࠣᱨ"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack1ll111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡤࡱࡱࡪ࡮࡭ࡳ࠯࡬ࡶࡳࡳ࠭ᱩ")), bstack1ll111_opy_ (u"ࠨࡹࠪᱪ")) as bstack1111llll1l1_opy_:
      bstack1111llll1l1_opy_.write(json.dumps(bstack1111l1lllll_opy_))
def bstack1111ll111l1_opy_():
  try:
    bstack1llll1ll11l_opy_ = os.path.join(os.getcwd(), bstack1ll111_opy_ (u"ࠩ࡯ࡳ࡬࠭ᱫ"), bstack1ll111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶ࠲࡯ࡹ࡯࡯ࠩᱬ"))
    if os.path.exists(bstack1llll1ll11l_opy_):
      with open(bstack1llll1ll11l_opy_, bstack1ll111_opy_ (u"ࠫࡷ࠭ᱭ")) as bstack1111llll1l1_opy_:
        bstack1111ll1l11l_opy_ = json.load(bstack1111llll1l1_opy_)
      return bstack1111ll1l11l_opy_.get(bstack1ll111_opy_ (u"ࠬ࡯࡮ࡪࡲࡤࡸ࡭࠭ᱮ"), bstack1ll111_opy_ (u"࠭ࠧᱯ")), bstack1111ll1l11l_opy_.get(bstack1ll111_opy_ (u"ࠧࡳࡱࡲࡸࡵࡧࡴࡩࠩᱰ"), bstack1ll111_opy_ (u"ࠨࠩᱱ"))
  except:
    pass
  return None, None
def bstack1111ll1111l_opy_():
  try:
    bstack1llll1ll11l_opy_ = os.path.join(os.getcwd(), bstack1ll111_opy_ (u"ࠩ࡯ࡳ࡬࠭ᱲ"), bstack1ll111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶ࠲࡯ࡹ࡯࡯ࠩᱳ"))
    if os.path.exists(bstack1llll1ll11l_opy_):
      os.remove(bstack1llll1ll11l_opy_)
  except:
    pass
def bstack11lll1l1_opy_(config):
  try:
    try:
      from bstack_utils.bstack11lll11l1l_opy_ import bstack111ll11111_opy_
    except Exception:
      bstack111ll11111_opy_ = None
    start_time = time.time()
    from bstack_utils.helper import global_config, bstack1l1ll11lll_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack1111l1lll11_opy_
    if config.get(bstack1ll111_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭ᱴ"), False):
      return
    uuid = os.getenv(bstack1ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᱵ")) if os.getenv(bstack1ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᱶ")) else global_config.get_property(bstack1ll111_opy_ (u"ࠢࡴࡦ࡮ࡖࡺࡴࡉࡥࠤᱷ"))
    if not uuid or uuid == bstack1ll111_opy_ (u"ࠨࡰࡸࡰࡱ࠭ᱸ"):
      return
    bstack1111ll111ll_opy_ = bstack111ll11111_opy_.bstack111l11l11_opy_(EVENTS.bstack1111ll11ll1_opy_.value) if bstack111ll11111_opy_ else None
    bstack1111ll1l1l1_opy_ = [bstack1ll111_opy_ (u"ࠩࡵࡩࡶࡻࡩࡳࡧࡰࡩࡳࡺࡳ࠯ࡶࡻࡸࠬᱹ"), bstack1ll111_opy_ (u"ࠪࡔ࡮ࡶࡦࡪ࡮ࡨࠫᱺ"), bstack1ll111_opy_ (u"ࠫࡵࡿࡰࡳࡱ࡭ࡩࡨࡺ࠮ࡵࡱࡰࡰࠬᱻ"), bstack1111l1lll11_opy_, bstack1111ll11lll_opy_]
    bstack1111ll1lll1_opy_, root_path = bstack1111ll111l1_opy_()
    if bstack1111ll1lll1_opy_ != None:
      bstack1111ll1l1l1_opy_.append(bstack1111ll1lll1_opy_)
    if root_path != None:
      bstack1111ll1l1l1_opy_.append(os.path.join(root_path, bstack1ll111_opy_ (u"ࠬࡩ࡯࡯ࡨࡷࡩࡸࡺ࠮ࡱࡻࠪᱼ")))
    bstack1111llll1ll_opy_ = os.path.join(os.getcwd(), bstack1ll111_opy_ (u"࠭࡬ࡰࡩࠪᱽ"), bstack1ll111_opy_ (u"ࠧ࡬ࡧࡼ࠱ࡲ࡫ࡴࡳ࡫ࡦࡷ࠳ࡰࡳࡰࡰࠪ᱾"))
    if os.path.exists(bstack1111llll1ll_opy_):
      bstack1111ll1l1l1_opy_.append(bstack1111llll1ll_opy_)
    output_file = os.path.join(tempfile.gettempdir(), bstack1ll111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠮࡮ࡲ࡫ࡸ࠳ࠧ᱿") + uuid + bstack1ll111_opy_ (u"ࠩ࠱ࡸࡦࡸ࠮ࡨࡼࠪᲀ"))
    with tarfile.open(output_file, bstack1ll111_opy_ (u"ࠥࡻ࠿࡭ࡺࠣᲁ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1111ll1l1l1_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1111lll111l_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1111lll11ll_opy_ = data.encode()
        tarinfo.size = len(bstack1111lll11ll_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1111lll11ll_opy_))
    multipart_data = MultipartEncoder(
      fields= {
        bstack1ll111_opy_ (u"ࠫࡩࡧࡴࡢࠩᲂ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1ll111_opy_ (u"ࠬࡸࡢࠨᲃ")), bstack1ll111_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳ࡽ࠳ࡧࡻ࡫ࡳࠫᲄ")),
        bstack1ll111_opy_ (u"ࠧࡤ࡮࡬ࡩࡳࡺࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩᲅ"): uuid
      }
    )
    bstack1111l1lll1l_opy_ = bstack1l1ll11lll_opy_(cli.config, [bstack1ll111_opy_ (u"ࠣࡣࡳ࡭ࡸࠨᲆ"), bstack1ll111_opy_ (u"ࠤࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠤᲇ"), bstack1ll111_opy_ (u"ࠥࡹࡵࡲ࡯ࡢࡦࠥᲈ")], bstack1111lll11l1_opy_)
    response = requests.post(
      bstack1ll111_opy_ (u"ࠦࢀࢃ࠯ࡤ࡮࡬ࡩࡳࡺ࠭࡭ࡱࡪࡷ࠴ࡻࡰ࡭ࡱࡤࡨࠧᲉ").format(bstack1111l1lll1l_opy_),
      data=multipart_data,
      headers={bstack1ll111_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫᲊ"): multipart_data.content_type},
      auth=(config[bstack1ll111_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ᲋")], config[bstack1ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ᲌")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1ll111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡶࡲ࡯ࡳࡦࡪࠠ࡭ࡱࡪࡷ࠿ࠦࠧ᲍") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1ll111_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡲࡩ࡯࡮ࡨࠢ࡯ࡳ࡬ࡹ࠺ࠨ᲎") + str(e))
  finally:
    try:
      bstack1l11l11111l_opy_()
      bstack1111ll1111l_opy_()
    except:
      pass
    if bstack111ll11111_opy_ and bstack1111ll111ll_opy_:
      bstack111ll11111_opy_.end(EVENTS.bstack1111ll11ll1_opy_.value, bstack1111ll111ll_opy_ + bstack1ll111_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ᲏"), bstack1111ll111ll_opy_ + bstack1ll111_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᲐ"), status=True, failure=None, test_name=None)
    try:
      elapsed = time.time() - start_time
      get_logger().debug(bstack1ll111_opy_ (u"ࠧࡹࡥ࡯ࡦࡢࡰࡴ࡭ࡳࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠤ࡮ࡴࠠࡼ࠼࠱࠷࡫ࢃࠠࡴࡧࡦࡳࡳࡪࡳࠣᲑ").format(elapsed))
    except Exception:
      pass