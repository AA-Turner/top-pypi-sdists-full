# coding: UTF-8
import sys
bstack11ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack1l1_opy_ (bstack1111l11_opy_):
    global bstack111l1ll_opy_
    bstack1l111l1_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1llll11_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l1l111_opy_ = bstack1l111l1_opy_ % len (bstack1llll11_opy_)
    bstack11l1l_opy_ = bstack1llll11_opy_ [:bstack1l1l111_opy_] + bstack1llll11_opy_ [bstack1l1l111_opy_:]
    if bstack11ll11_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11lll11_opy_)
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
from bstack_utils.constants import bstack111l11111ll_opy_, EVENTS, bstack111l11lll11_opy_, bstack111l11l111l_opy_, STAGE
import tempfile
import json
bstack1lllll1l1l1l_opy_ = os.getenv(bstack1l1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡈࡡࡉࡍࡑࡋࠢ∦"), None) or os.path.join(tempfile.gettempdir(), bstack1l1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡤࡦࡤࡸ࡫࠳ࡲ࡯ࡨࠤ∧"))
bstack1lllll1l11ll_opy_ = os.path.join(bstack1l1_opy_ (u"ࠣ࡮ࡲ࡫ࠧ∨"), bstack1l1_opy_ (u"ࠩࡶࡨࡰ࠳ࡣ࡭࡫࠰ࡨࡪࡨࡵࡨ࠰࡯ࡳ࡬࠭∩"))
_1lllll1ll1ll_opy_ = threading.Lock()
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1l1_opy_ (u"ࠪࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭∪"),
      datefmt=bstack1l1_opy_ (u"ࠫࠪ࡟࠭ࠦ࡯࠰ࠩࡩ࡚ࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࡛ࠩ∫"),
      stream=sys.stdout
    )
  return logger
def get_automation_logger(name=__name__, level=logging.DEBUG):
  bstack1l1_opy_ (u"ࠧࠨࠢࠋࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡦࠦ࡬ࡰࡩࡪࡩࡷࠦࡴࡩࡣࡷࠤࡼࡸࡩࡵࡧࡶࠤࡴࡴ࡬ࡺࠢࡷࡳࠥࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠰࡯ࡳ࡬ࠦࡦࡪ࡮ࡨࠎࠥࠦࡃࡳࡧࡤࡸࡪࡹࠠࡢࡰࡧࠤࡲࡧ࡮ࡢࡩࡨࡷࠥ࡯ࡴࡴࠢࡲࡻࡳࠦࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡪ࡮ࡲࡥࠡࡪࡤࡲࡩࡲࡥࡳࠌࠣࠤࡔࡴ࡬ࡺࠢࡨࡲࡦࡨ࡬ࡦࡵࠣࡰࡴ࡭ࡧࡪࡰࡪࠤ࡮࡬ࠠࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࡢࡐࡔࡍࡓࠡࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹࠦࡶࡢࡴ࡬ࡥࡧࡲࡥࠡ࡫ࡶࠤࡸ࡫ࡴࠡࡶࡲࠤࡦࠦࡴࡳࡷࡷ࡬ࡾࠦࡶࡢ࡮ࡸࡩࠏࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࡲࡦࡳࡥ࠻ࠢࡏࡳ࡬࡭ࡥࡳࠢࡱࡥࡲ࡫ࠠࠩࡦࡨࡪࡦࡻ࡬ࡵࡵࠣࡸࡴࠦ࡟ࡠࡰࡤࡱࡪࡥ࡟ࠪࠌࠣࠤࠥࠦ࡬ࡦࡸࡨࡰ࠿ࠦࡌࡰࡩࡪ࡭ࡳ࡭ࠠ࡭ࡧࡹࡩࡱࠦࠨࡥࡧࡩࡥࡺࡲࡴࡴࠢࡷࡳࠥࡊࡅࡃࡗࡊ࠭ࠏࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦ࡬ࡰࡩࡪ࡭ࡳ࡭࠮ࡍࡱࡪ࡫ࡪࡸ࠺ࠡࡅࡲࡲ࡫࡯ࡧࡶࡴࡨࡨࠥࡲ࡯ࡨࡩࡨࡶࠥࡺࡨࡢࡶࠣࡻࡷ࡯ࡴࡦࡵࠣࡳࡳࡲࡹࠡࡶࡲࠤࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠯࡮ࡲ࡫ࠥ࠮ࡩࡧࠢࡨࡲࡦࡨ࡬ࡦࡦࠬࠎࠥࠦࠢࠣࠤ∬")
  logger_name = bstack1l1_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠱ࡿ࠵ࢃࠢ∭").format(name)
  logger = logging.getLogger(logger_name)
  is_enabled = os.getenv(bstack1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࡢࡐࡔࡍࡓࠨ∮"), bstack1l1_opy_ (u"ࠨࠩ∯")).lower() == bstack1l1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ∰")
  if not is_enabled:
    logger.setLevel(logging.CRITICAL)
    logger.propagate = False
    return logger
  with _1lllll1ll1ll_opy_:
    if logger.handlers:
      return logger
    bstack1lllll11llll_opy_ = os.path.join(os.getcwd(), bstack1l1_opy_ (u"ࠪࡰࡴ࡭ࠧ∱"), bstack1l1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠯࡮ࡲ࡫ࠬ∲"))
    log_dir = os.path.dirname(bstack1lllll11llll_opy_)
    if not os.path.exists(log_dir):
      os.makedirs(log_dir)
    bstack1lllll11ll11_opy_ = logging.FileHandler(bstack1lllll11llll_opy_)
    bstack1lllll1l1l11_opy_ = logging.Formatter(
      fmt=bstack1l1_opy_ (u"ࠬࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣ࡟࡙ࠥࡄࡌ࠯ࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓࠦ࡝ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭∳"),
      datefmt=bstack1l1_opy_ (u"࡚࠭ࠥ࠯ࠨࡱ࠲ࠫࡤࡕࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࡝ࠫ∴"),
    )
    bstack1lllll11ll11_opy_.setFormatter(bstack1lllll1l1l11_opy_)
    bstack1lllll11ll11_opy_.setLevel(level)
    bstack1lllll11ll11_opy_.addFilter(lambda r: r.name != bstack1l1_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࠰ࡺࡩࡧࡪࡲࡪࡸࡨࡶ࠳ࡸࡥ࡮ࡱࡷࡩ࠳ࡸࡥ࡮ࡱࡷࡩࡤࡩ࡯࡯ࡰࡨࡧࡹ࡯࡯࡯ࠩ∵"))
    logger.addHandler(bstack1lllll11ll11_opy_)
    logger.setLevel(level)
    logger.propagate = False
  return logger
def get_log_level():
  bstack1lllll1l1ll1_opy_ = os.environ.get(bstack1l1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡅࡇࡅ࡙ࡌࠨ∶"), bstack1l1_opy_ (u"ࠤࡩࡥࡱࡹࡥࠣ∷"))
  return logging.DEBUG if bstack1lllll1l1ll1_opy_.lower() == bstack1l1_opy_ (u"ࠥࡸࡷࡻࡥࠣ∸") else logging.INFO
def bstack1l111ll1l11_opy_():
  global bstack1lllll1l1l1l_opy_
  if os.path.exists(bstack1lllll1l1l1l_opy_):
    os.remove(bstack1lllll1l1l1l_opy_)
  if os.path.exists(bstack1lllll1l11ll_opy_):
    os.remove(bstack1lllll1l11ll_opy_)
def bstack1ll111l11l_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def configure_logger(config, log_level):
  bstack1lllll11lll1_opy_ = log_level
  if bstack1l1_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭∹") in config and config[bstack1l1_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧ∺")] in bstack111l11lll11_opy_:
    bstack1lllll11lll1_opy_ = bstack111l11lll11_opy_[config[bstack1l1_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨ∻")]]
  if config.get(bstack1l1_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡷࡷࡳࡈࡧࡰࡵࡷࡵࡩࡑࡵࡧࡴࠩ∼"), False):
    logging.getLogger().setLevel(bstack1lllll11lll1_opy_)
    return bstack1lllll11lll1_opy_
  global bstack1lllll1l1l1l_opy_
  bstack1ll111l11l_opy_()
  bstack1lllll1ll111_opy_ = logging.Formatter(
    fmt=bstack1l1_opy_ (u"ࠨࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲ࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫ∽"),
    datefmt=bstack1l1_opy_ (u"ࠩࠨ࡝࠲ࠫ࡭࠮ࠧࡧࡘࠪࡎ࠺ࠦࡏ࠽ࠩࡘࡠࠧ∾"),
  )
  bstack1lllll1l1111_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1lllll1l1l1l_opy_)
  file_handler.setFormatter(bstack1lllll1ll111_opy_)
  bstack1lllll1l1111_opy_.setFormatter(bstack1lllll1ll111_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1lllll1l1111_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1l1_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲ࠯ࡴࡨࡱࡴࡺࡥ࠯ࡴࡨࡱࡴࡺࡥࡠࡥࡲࡲࡳ࡫ࡣࡵ࡫ࡲࡲࠬ∿"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1lllll1l1111_opy_.setLevel(bstack1lllll11lll1_opy_)
  logging.getLogger().addHandler(bstack1lllll1l1111_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1lllll11lll1_opy_
def bstack1lllll111lll_opy_(config):
  try:
    bstack1lllll1l11l1_opy_ = set(bstack111l11l111l_opy_)
    bstack1lllll1lll11_opy_ = bstack1l1_opy_ (u"ࠫࠬ≀")
    with open(bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨ≁")) as bstack1llllll111l1_opy_:
      bstack1llllll1111l_opy_ = bstack1llllll111l1_opy_.read()
      bstack1lllll1lll11_opy_ = re.sub(bstack1l1_opy_ (u"ࡸࠧ࡟ࠪ࡟ࡷ࠰࠯࠿ࠤ࠰࠭ࠨࡡࡴࠧ≂"), bstack1l1_opy_ (u"ࠧࠨ≃"), bstack1llllll1111l_opy_, flags=re.M)
      bstack1lllll1lll11_opy_ = re.sub(
        bstack1l1_opy_ (u"ࡳࠩࡡࠬࡡࡹࠫࠪࡁࠫࠫ≄") + bstack1l1_opy_ (u"ࠩࡿࠫ≅").join(bstack1lllll1l11l1_opy_) + bstack1l1_opy_ (u"ࠪ࠭࠳࠰ࠤࠨ≆"),
        bstack1l1_opy_ (u"ࡶࠬࡢ࠲࠻ࠢ࡞ࡖࡊࡊࡁࡄࡖࡈࡈࡢ࠭≇"),
        bstack1lllll1lll11_opy_, flags=re.M | re.I
      )
    def bstack1lllll1llll1_opy_(dic):
      bstack1lllll11l1l1_opy_ = {}
      for key, value in dic.items():
        if key in bstack1lllll1l11l1_opy_:
          bstack1lllll11l1l1_opy_[key] = bstack1l1_opy_ (u"ࠬࡡࡒࡆࡆࡄࡇ࡙ࡋࡄ࡞ࠩ≈")
        else:
          if isinstance(value, dict):
            bstack1lllll11l1l1_opy_[key] = bstack1lllll1llll1_opy_(value)
          else:
            bstack1lllll11l1l1_opy_[key] = value
      return bstack1lllll11l1l1_opy_
    bstack1lllll11l1l1_opy_ = bstack1lllll1llll1_opy_(config)
    return {
      bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩ≉"): bstack1lllll1lll11_opy_,
      bstack1l1_opy_ (u"ࠧࡧ࡫ࡱࡥࡱࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪ≊"): json.dumps(bstack1lllll11l1l1_opy_)
    }
  except Exception as e:
    return {}
def bstack1lllll1lllll_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack1l1_opy_ (u"ࠨ࡮ࡲ࡫ࠬ≋"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack1lll1ll1ll1_opy_ = os.path.join(log_dir, bstack1l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡦࡳࡳ࡬ࡩࡨࡵࠪ≌"))
  if not os.path.exists(bstack1lll1ll1ll1_opy_):
    bstack1lllll1lll1l_opy_ = {
      bstack1l1_opy_ (u"ࠥ࡭ࡳ࡯ࡰࡢࡶ࡫ࠦ≍"): str(inipath),
      bstack1l1_opy_ (u"ࠦࡷࡵ࡯ࡵࡲࡤࡸ࡭ࠨ≎"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack1l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡩ࡯࡯ࡨ࡬࡫ࡸ࠴ࡪࡴࡱࡱࠫ≏")), bstack1l1_opy_ (u"࠭ࡷࠨ≐")) as bstack1llllll11111_opy_:
      bstack1llllll11111_opy_.write(json.dumps(bstack1lllll1lll1l_opy_))
def bstack1lllll1l1lll_opy_():
  try:
    bstack1lll1ll1ll1_opy_ = os.path.join(os.getcwd(), bstack1l1_opy_ (u"ࠧ࡭ࡱࡪࠫ≑"), bstack1l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡥࡲࡲ࡫࡯ࡧࡴ࠰࡭ࡷࡴࡴࠧ≒"))
    if os.path.exists(bstack1lll1ll1ll1_opy_):
      with open(bstack1lll1ll1ll1_opy_, bstack1l1_opy_ (u"ࠩࡵࠫ≓")) as bstack1llllll11111_opy_:
        bstack1lllll1l111l_opy_ = json.load(bstack1llllll11111_opy_)
      return bstack1lllll1l111l_opy_.get(bstack1l1_opy_ (u"ࠪ࡭ࡳ࡯ࡰࡢࡶ࡫ࠫ≔"), bstack1l1_opy_ (u"ࠫࠬ≕")), bstack1lllll1l111l_opy_.get(bstack1l1_opy_ (u"ࠬࡸ࡯ࡰࡶࡳࡥࡹ࡮ࠧ≖"), bstack1l1_opy_ (u"࠭ࠧ≗"))
  except:
    pass
  return None, None
def bstack1lllll11l11l_opy_():
  try:
    bstack1lll1ll1ll1_opy_ = os.path.join(os.getcwd(), bstack1l1_opy_ (u"ࠧ࡭ࡱࡪࠫ≘"), bstack1l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡥࡲࡲ࡫࡯ࡧࡴ࠰࡭ࡷࡴࡴࠧ≙"))
    if os.path.exists(bstack1lll1ll1ll1_opy_):
      os.remove(bstack1lll1ll1ll1_opy_)
  except:
    pass
def bstack1llllll1l1_opy_(config):
  try:
    try:
      from bstack_utils.bstack11l1l1ll_opy_ import bstack111l1111l_opy_
    except Exception:
      bstack111l1111l_opy_ = None
    start_time = time.time()
    from bstack_utils.helper import global_config, bstack11l1lll11_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack1lllll1l1l1l_opy_
    if config.get(bstack1l1_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫ≚"), False):
      return
    uuid = os.getenv(bstack1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ≛")) if os.getenv(bstack1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ≜")) else global_config.get_property(bstack1l1_opy_ (u"ࠧࡹࡤ࡬ࡔࡸࡲࡎࡪࠢ≝"))
    if not uuid or uuid == bstack1l1_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ≞"):
      return
    bstack1lllll1ll11l_opy_ = bstack111l1111l_opy_.bstack1ll1l1l1l_opy_(EVENTS.bstack111l11ll11l_opy_.value) if bstack111l1111l_opy_ else None
    bstack1lllll11l1ll_opy_ = [bstack1l1_opy_ (u"ࠧࡳࡧࡴࡹ࡮ࡸࡥ࡮ࡧࡱࡸࡸ࠴ࡴࡹࡶࠪ≟"), bstack1l1_opy_ (u"ࠨࡒ࡬ࡴ࡫࡯࡬ࡦࠩ≠"), bstack1l1_opy_ (u"ࠩࡳࡽࡵࡸ࡯࡫ࡧࡦࡸ࠳ࡺ࡯࡮࡮ࠪ≡"), bstack1lllll1l1l1l_opy_, bstack1lllll1l11ll_opy_]
    bstack1lllll1ll1l1_opy_, root_path = bstack1lllll1l1lll_opy_()
    if bstack1lllll1ll1l1_opy_ != None:
      bstack1lllll11l1ll_opy_.append(bstack1lllll1ll1l1_opy_)
    if root_path != None:
      bstack1lllll11l1ll_opy_.append(os.path.join(root_path, bstack1l1_opy_ (u"ࠪࡧࡴࡴࡦࡵࡧࡶࡸ࠳ࡶࡹࠨ≢")))
    bstack1lllll11ll1l_opy_ = os.path.join(os.getcwd(), bstack1l1_opy_ (u"ࠫࡱࡵࡧࠨ≣"), bstack1l1_opy_ (u"ࠬࡱࡥࡺ࠯ࡰࡩࡹࡸࡩࡤࡵ࠱࡮ࡸࡵ࡮ࠨ≤"))
    if os.path.exists(bstack1lllll11ll1l_opy_):
      bstack1lllll11l1ll_opy_.append(bstack1lllll11ll1l_opy_)
    output_file = os.path.join(tempfile.gettempdir(), bstack1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࠳࡬ࡰࡩࡶ࠱ࠬ≥") + uuid + bstack1l1_opy_ (u"ࠧ࠯ࡶࡤࡶ࠳࡭ࡺࠨ≦"))
    with tarfile.open(output_file, bstack1l1_opy_ (u"ࠣࡹ࠽࡫ࡿࠨ≧")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1lllll11l1ll_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1lllll111lll_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1lllll11l111_opy_ = data.encode()
        tarinfo.size = len(bstack1lllll11l111_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1lllll11l111_opy_))
    multipart_data = MultipartEncoder(
      fields= {
        bstack1l1_opy_ (u"ࠩࡧࡥࡹࡧࠧ≨"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1l1_opy_ (u"ࠪࡶࡧ࠭≩")), bstack1l1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱ࡻ࠱࡬ࢀࡩࡱࠩ≪")),
        bstack1l1_opy_ (u"ࠬࡩ࡬ࡪࡧࡱࡸࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧ≫"): uuid
      }
    )
    bstack1llllll111ll_opy_ = bstack11l1lll11_opy_(cli.config, [bstack1l1_opy_ (u"ࠨࡡࡱ࡫ࡶࠦ≬"), bstack1l1_opy_ (u"ࠢࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠢ≭"), bstack1l1_opy_ (u"ࠣࡷࡳࡰࡴࡧࡤࠣ≮")], bstack111l11111ll_opy_)
    response = requests.post(
      bstack1l1_opy_ (u"ࠤࡾࢁ࠴ࡩ࡬ࡪࡧࡱࡸ࠲ࡲ࡯ࡨࡵ࠲ࡹࡵࡲ࡯ࡢࡦࠥ≯").format(bstack1llllll111ll_opy_),
      data=multipart_data,
      headers={bstack1l1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩ≰"): multipart_data.content_type},
      auth=(config[bstack1l1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭≱")], config[bstack1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ≲")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1l1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡻࡰ࡭ࡱࡤࡨࠥࡲ࡯ࡨࡵ࠽ࠤࠬ≳") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1l1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡰࡧ࡭ࡳ࡭ࠠ࡭ࡱࡪࡷ࠿࠭≴") + str(e))
  finally:
    try:
      bstack1l111ll1l11_opy_()
      bstack1lllll11l11l_opy_()
    except:
      pass
    if bstack111l1111l_opy_ and bstack1lllll1ll11l_opy_:
      bstack111l1111l_opy_.end(EVENTS.bstack111l11ll11l_opy_.value, bstack1lllll1ll11l_opy_ + bstack1l1_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ≵"), bstack1lllll1ll11l_opy_ + bstack1l1_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ≶"), status=True, failure=None, test_name=None)
    try:
      elapsed = time.time() - start_time
      get_logger().debug(bstack1l1_opy_ (u"ࠥࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡸࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠢ࡬ࡲࠥࢁ࠺࠯࠵ࡩࢁࠥࡹࡥࡤࡱࡱࡨࡸࠨ≷").format(elapsed))
    except Exception:
      pass