# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
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
from bstack_utils.constants import bstack111l111l1ll_opy_, EVENTS, bstack111l111lll1_opy_, bstack111l111l1l1_opy_, STAGE
import tempfile
import json
bstack1lllll1lll1l_opy_ = os.getenv(bstack1ll1lll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡊࡣࡋࡏࡌࡆࠤ∡"), None) or os.path.join(tempfile.gettempdir(), bstack1ll1lll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡦࡨࡦࡺ࡭࠮࡭ࡱࡪࠦ∢"))
bstack1lllll11ll11_opy_ = os.path.join(bstack1ll1lll_opy_ (u"ࠥࡰࡴ࡭ࠢ∣"), bstack1ll1lll_opy_ (u"ࠫࡸࡪ࡫࠮ࡥ࡯࡭࠲ࡪࡥࡣࡷࡪ࠲ࡱࡵࡧࠨ∤"))
_1llllll11111_opy_ = threading.Lock()
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1ll1lll_opy_ (u"ࠬࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨ∥"),
      datefmt=bstack1ll1lll_opy_ (u"࡚࠭ࠥ࠯ࠨࡱ࠲ࠫࡤࡕࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࡝ࠫ∦"),
      stream=sys.stdout
    )
  return logger
def get_automation_logger(name=__name__, level=logging.DEBUG):
  bstack1ll1lll_opy_ (u"ࠢࠣࠤࠍࠤࠥࡘࡥࡵࡷࡵࡲࡸࠦࡡࠡ࡮ࡲ࡫࡬࡫ࡲࠡࡶ࡫ࡥࡹࠦࡷࡳ࡫ࡷࡩࡸࠦ࡯࡯࡮ࡼࠤࡹࡵࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠲ࡱࡵࡧࠡࡨ࡬ࡰࡪࠐࠠࠡࡅࡵࡩࡦࡺࡥࡴࠢࡤࡲࡩࠦ࡭ࡢࡰࡤ࡫ࡪࡹࠠࡪࡶࡶࠤࡴࡽ࡮ࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥ࡬ࡩ࡭ࡧࠣ࡬ࡦࡴࡤ࡭ࡧࡵࠎࠥࠦࡏ࡯࡮ࡼࠤࡪࡴࡡࡣ࡮ࡨࡷࠥࡲ࡯ࡨࡩ࡬ࡲ࡬ࠦࡩࡧࠢࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࡤࡒࡏࡈࡕࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴࠡࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠣ࡭ࡸࠦࡳࡦࡶࠣࡸࡴࠦࡡࠡࡶࡵࡹࡹ࡮ࡹࠡࡸࡤࡰࡺ࡫ࠊࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࡴࡡ࡮ࡧ࠽ࠤࡑࡵࡧࡨࡧࡵࠤࡳࡧ࡭ࡦࠢࠫࡨࡪ࡬ࡡࡶ࡮ࡷࡷࠥࡺ࡯ࠡࡡࡢࡲࡦࡳࡥࡠࡡࠬࠎࠥࠦࠠࠡ࡮ࡨࡺࡪࡲ࠺ࠡࡎࡲ࡫࡬࡯࡮ࡨࠢ࡯ࡩࡻ࡫࡬ࠡࠪࡧࡩ࡫ࡧࡵ࡭ࡶࡶࠤࡹࡵࠠࡅࡇࡅ࡙ࡌ࠯ࠊࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡ࡮ࡲ࡫࡬࡯࡮ࡨ࠰ࡏࡳ࡬࡭ࡥࡳ࠼ࠣࡇࡴࡴࡦࡪࡩࡸࡶࡪࡪࠠ࡭ࡱࡪ࡫ࡪࡸࠠࡵࡪࡤࡸࠥࡽࡲࡪࡶࡨࡷࠥࡵ࡮࡭ࡻࠣࡸࡴࠦࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠱ࡰࡴ࡭ࠠࠩ࡫ࡩࠤࡪࡴࡡࡣ࡮ࡨࡨ࠮ࠐࠠࠡࠤࠥࠦ∧")
  logger_name = bstack1ll1lll_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠳ࢁ࠰ࡾࠤ∨").format(name)
  logger = logging.getLogger(logger_name)
  is_enabled = os.getenv(bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࡤࡒࡏࡈࡕࠪ∩"), bstack1ll1lll_opy_ (u"ࠪࠫ∪")).lower() == bstack1ll1lll_opy_ (u"ࠫࡹࡸࡵࡦࠩ∫")
  if not is_enabled:
    logger.setLevel(logging.CRITICAL)
    logger.propagate = False
    return logger
  with _1llllll11111_opy_:
    if logger.handlers:
      return logger
    bstack1lllll1l1111_opy_ = os.path.join(os.getcwd(), bstack1ll1lll_opy_ (u"ࠬࡲ࡯ࡨࠩ∬"), bstack1ll1lll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠱ࡰࡴ࡭ࠧ∭"))
    log_dir = os.path.dirname(bstack1lllll1l1111_opy_)
    if not os.path.exists(log_dir):
      os.makedirs(log_dir)
    bstack1lllll1l111l_opy_ = logging.FileHandler(bstack1lllll1l1111_opy_)
    bstack1lllll11ll1l_opy_ = logging.Formatter(
      fmt=bstack1ll1lll_opy_ (u"ࠧࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࡡࠠࡔࡆࡎ࠱ࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠡ࡟ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨ∮"),
      datefmt=bstack1ll1lll_opy_ (u"ࠨࠧ࡜࠱ࠪࡳ࠭ࠦࡦࡗࠩࡍࡀࠥࡎ࠼ࠨࡗ࡟࠭∯"),
    )
    bstack1lllll1l111l_opy_.setFormatter(bstack1lllll11ll1l_opy_)
    bstack1lllll1l111l_opy_.setLevel(level)
    bstack1lllll1l111l_opy_.addFilter(lambda r: r.name != bstack1ll1lll_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࠮ࡳࡧࡰࡳࡹ࡫࠮ࡳࡧࡰࡳࡹ࡫࡟ࡤࡱࡱࡲࡪࡩࡴࡪࡱࡱࠫ∰"))
    logger.addHandler(bstack1lllll1l111l_opy_)
    logger.setLevel(level)
    logger.propagate = False
  return logger
def get_log_level():
  bstack1lllll1l1l11_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡇࡉࡇ࡛ࡇࠣ∱"), bstack1ll1lll_opy_ (u"ࠦ࡫ࡧ࡬ࡴࡧࠥ∲"))
  return logging.DEBUG if bstack1lllll1l1l11_opy_.lower() == bstack1ll1lll_opy_ (u"ࠧࡺࡲࡶࡧࠥ∳") else logging.INFO
def bstack1l111l1111l_opy_():
  global bstack1lllll1lll1l_opy_
  if os.path.exists(bstack1lllll1lll1l_opy_):
    os.remove(bstack1lllll1lll1l_opy_)
  if os.path.exists(bstack1lllll11ll11_opy_):
    os.remove(bstack1lllll11ll11_opy_)
def bstack1llll111_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def configure_logger(config, log_level):
  bstack1lllll1l1ll1_opy_ = log_level
  if bstack1ll1lll_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨ∴") in config and config[bstack1ll1lll_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩ∵")] in bstack111l111lll1_opy_:
    bstack1lllll1l1ll1_opy_ = bstack111l111lll1_opy_[config[bstack1ll1lll_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪ∶")]]
  if config.get(bstack1ll1lll_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫ∷"), False):
    logging.getLogger().setLevel(bstack1lllll1l1ll1_opy_)
    return bstack1lllll1l1ll1_opy_
  global bstack1lllll1lll1l_opy_
  bstack1llll111_opy_()
  bstack1lllll11l1l1_opy_ = logging.Formatter(
    fmt=bstack1ll1lll_opy_ (u"ࠪࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭∸"),
    datefmt=bstack1ll1lll_opy_ (u"ࠫࠪ࡟࠭ࠦ࡯࠰ࠩࡩ࡚ࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࡛ࠩ∹"),
  )
  bstack1llllll1111l_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1lllll1lll1l_opy_)
  file_handler.setFormatter(bstack1lllll11l1l1_opy_)
  bstack1llllll1111l_opy_.setFormatter(bstack1lllll11l1l1_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1llllll1111l_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1ll1lll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡶࡪࡳ࡯ࡵࡧ࠱ࡶࡪࡳ࡯ࡵࡧࡢࡧࡴࡴ࡮ࡦࡥࡷ࡭ࡴࡴࠧ∺"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1llllll1111l_opy_.setLevel(bstack1lllll1l1ll1_opy_)
  logging.getLogger().addHandler(bstack1llllll1111l_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1lllll1l1ll1_opy_
def bstack1lllll11l1ll_opy_(config):
  try:
    bstack1llllll111ll_opy_ = set(bstack111l111l1l1_opy_)
    bstack1lllll11lll1_opy_ = bstack1ll1lll_opy_ (u"࠭ࠧ∻")
    with open(bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪ∼")) as bstack1lllll11l11l_opy_:
      bstack1llllll111l1_opy_ = bstack1lllll11l11l_opy_.read()
      bstack1lllll11lll1_opy_ = re.sub(bstack1ll1lll_opy_ (u"ࡳࠩࡡࠬࡡࡹࠫࠪࡁࠦ࠲࠯ࠪ࡜࡯ࠩ∽"), bstack1ll1lll_opy_ (u"ࠩࠪ∾"), bstack1llllll111l1_opy_, flags=re.M)
      bstack1lllll11lll1_opy_ = re.sub(
        bstack1ll1lll_opy_ (u"ࡵࠫࡣ࠮࡜ࡴ࠭ࠬࡃ࠭࠭∿") + bstack1ll1lll_opy_ (u"ࠫࢁ࠭≀").join(bstack1llllll111ll_opy_) + bstack1ll1lll_opy_ (u"ࠬ࠯࠮ࠫࠦࠪ≁"),
        bstack1ll1lll_opy_ (u"ࡸࠧ࡝࠴࠽ࠤࡠࡘࡅࡅࡃࡆࡘࡊࡊ࡝ࠨ≂"),
        bstack1lllll11lll1_opy_, flags=re.M | re.I
      )
    def bstack1lllll1l1lll_opy_(dic):
      bstack1lllll1lll11_opy_ = {}
      for key, value in dic.items():
        if key in bstack1llllll111ll_opy_:
          bstack1lllll1lll11_opy_[key] = bstack1ll1lll_opy_ (u"ࠧ࡜ࡔࡈࡈࡆࡉࡔࡆࡆࡠࠫ≃")
        else:
          if isinstance(value, dict):
            bstack1lllll1lll11_opy_[key] = bstack1lllll1l1lll_opy_(value)
          else:
            bstack1lllll1lll11_opy_[key] = value
      return bstack1lllll1lll11_opy_
    bstack1lllll1lll11_opy_ = bstack1lllll1l1lll_opy_(config)
    return {
      bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫ≄"): bstack1lllll11lll1_opy_,
      bstack1ll1lll_opy_ (u"ࠩࡩ࡭ࡳࡧ࡬ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬ≅"): json.dumps(bstack1lllll1lll11_opy_)
    }
  except Exception as e:
    return {}
def bstack1lllll1ll11l_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack1ll1lll_opy_ (u"ࠪࡰࡴ࡭ࠧ≆"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack1lll1ll11l1_opy_ = os.path.join(log_dir, bstack1ll1lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷࠬ≇"))
  if not os.path.exists(bstack1lll1ll11l1_opy_):
    bstack1lllll11llll_opy_ = {
      bstack1ll1lll_opy_ (u"ࠧ࡯࡮ࡪࡲࡤࡸ࡭ࠨ≈"): str(inipath),
      bstack1ll1lll_opy_ (u"ࠨࡲࡰࡱࡷࡴࡦࡺࡨࠣ≉"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack1ll1lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡤࡱࡱࡪ࡮࡭ࡳ࠯࡬ࡶࡳࡳ࠭≊")), bstack1ll1lll_opy_ (u"ࠨࡹࠪ≋")) as bstack1lllll11l111_opy_:
      bstack1lllll11l111_opy_.write(json.dumps(bstack1lllll11llll_opy_))
def bstack1lllll1l1l1l_opy_():
  try:
    bstack1lll1ll11l1_opy_ = os.path.join(os.getcwd(), bstack1ll1lll_opy_ (u"ࠩ࡯ࡳ࡬࠭≌"), bstack1ll1lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶ࠲࡯ࡹ࡯࡯ࠩ≍"))
    if os.path.exists(bstack1lll1ll11l1_opy_):
      with open(bstack1lll1ll11l1_opy_, bstack1ll1lll_opy_ (u"ࠫࡷ࠭≎")) as bstack1lllll11l111_opy_:
        bstack1lllll1ll1l1_opy_ = json.load(bstack1lllll11l111_opy_)
      return bstack1lllll1ll1l1_opy_.get(bstack1ll1lll_opy_ (u"ࠬ࡯࡮ࡪࡲࡤࡸ࡭࠭≏"), bstack1ll1lll_opy_ (u"࠭ࠧ≐")), bstack1lllll1ll1l1_opy_.get(bstack1ll1lll_opy_ (u"ࠧࡳࡱࡲࡸࡵࡧࡴࡩࠩ≑"), bstack1ll1lll_opy_ (u"ࠨࠩ≒"))
  except:
    pass
  return None, None
def bstack1lllll1l11ll_opy_():
  try:
    bstack1lll1ll11l1_opy_ = os.path.join(os.getcwd(), bstack1ll1lll_opy_ (u"ࠩ࡯ࡳ࡬࠭≓"), bstack1ll1lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶ࠲࡯ࡹ࡯࡯ࠩ≔"))
    if os.path.exists(bstack1lll1ll11l1_opy_):
      os.remove(bstack1lll1ll11l1_opy_)
  except:
    pass
def bstack11lllll111_opy_(config):
  try:
    try:
      from bstack_utils.bstack1ll11111_opy_ import bstack1lll1lll11_opy_
    except Exception:
      bstack1lll1lll11_opy_ = None
    start_time = time.time()
    from bstack_utils.helper import global_config, bstack1l11llll1l_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack1lllll1lll1l_opy_
    if config.get(bstack1ll1lll_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭≕"), False):
      return
    uuid = os.getenv(bstack1ll1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ≖")) if os.getenv(bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ≗")) else global_config.get_property(bstack1ll1lll_opy_ (u"ࠢࡴࡦ࡮ࡖࡺࡴࡉࡥࠤ≘"))
    if not uuid or uuid == bstack1ll1lll_opy_ (u"ࠨࡰࡸࡰࡱ࠭≙"):
      return
    bstack1lllll1llll1_opy_ = bstack1lll1lll11_opy_.bstack11l1llllll_opy_(EVENTS.bstack111l1l1l11l_opy_.value) if bstack1lll1lll11_opy_ else None
    bstack1lllll1ll111_opy_ = [bstack1ll1lll_opy_ (u"ࠩࡵࡩࡶࡻࡩࡳࡧࡰࡩࡳࡺࡳ࠯ࡶࡻࡸࠬ≚"), bstack1ll1lll_opy_ (u"ࠪࡔ࡮ࡶࡦࡪ࡮ࡨࠫ≛"), bstack1ll1lll_opy_ (u"ࠫࡵࡿࡰࡳࡱ࡭ࡩࡨࡺ࠮ࡵࡱࡰࡰࠬ≜"), bstack1lllll1lll1l_opy_, bstack1lllll11ll11_opy_]
    bstack1lllll1ll1ll_opy_, root_path = bstack1lllll1l1l1l_opy_()
    if bstack1lllll1ll1ll_opy_ != None:
      bstack1lllll1ll111_opy_.append(bstack1lllll1ll1ll_opy_)
    if root_path != None:
      bstack1lllll1ll111_opy_.append(os.path.join(root_path, bstack1ll1lll_opy_ (u"ࠬࡩ࡯࡯ࡨࡷࡩࡸࡺ࠮ࡱࡻࠪ≝")))
    bstack1llllll11l11_opy_ = os.path.join(os.getcwd(), bstack1ll1lll_opy_ (u"࠭࡬ࡰࡩࠪ≞"), bstack1ll1lll_opy_ (u"ࠧ࡬ࡧࡼ࠱ࡲ࡫ࡴࡳ࡫ࡦࡷ࠳ࡰࡳࡰࡰࠪ≟"))
    if os.path.exists(bstack1llllll11l11_opy_):
      bstack1lllll1ll111_opy_.append(bstack1llllll11l11_opy_)
    output_file = os.path.join(tempfile.gettempdir(), bstack1ll1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠮࡮ࡲ࡫ࡸ࠳ࠧ≠") + uuid + bstack1ll1lll_opy_ (u"ࠩ࠱ࡸࡦࡸ࠮ࡨࡼࠪ≡"))
    with tarfile.open(output_file, bstack1ll1lll_opy_ (u"ࠥࡻ࠿࡭ࡺࠣ≢")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1lllll1ll111_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1lllll11l1ll_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1lllll1l11l1_opy_ = data.encode()
        tarinfo.size = len(bstack1lllll1l11l1_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1lllll1l11l1_opy_))
    multipart_data = MultipartEncoder(
      fields= {
        bstack1ll1lll_opy_ (u"ࠫࡩࡧࡴࡢࠩ≣"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1ll1lll_opy_ (u"ࠬࡸࡢࠨ≤")), bstack1ll1lll_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳ࡽ࠳ࡧࡻ࡫ࡳࠫ≥")),
        bstack1ll1lll_opy_ (u"ࠧࡤ࡮࡬ࡩࡳࡺࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ≦"): uuid
      }
    )
    bstack1lllll1lllll_opy_ = bstack1l11llll1l_opy_(cli.config, [bstack1ll1lll_opy_ (u"ࠣࡣࡳ࡭ࡸࠨ≧"), bstack1ll1lll_opy_ (u"ࠤࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠤ≨"), bstack1ll1lll_opy_ (u"ࠥࡹࡵࡲ࡯ࡢࡦࠥ≩")], bstack111l111l1ll_opy_)
    response = requests.post(
      bstack1ll1lll_opy_ (u"ࠦࢀࢃ࠯ࡤ࡮࡬ࡩࡳࡺ࠭࡭ࡱࡪࡷ࠴ࡻࡰ࡭ࡱࡤࡨࠧ≪").format(bstack1lllll1lllll_opy_),
      data=multipart_data,
      headers={bstack1ll1lll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ≫"): multipart_data.content_type},
      auth=(config[bstack1ll1lll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ≬")], config[bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ≭")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1ll1lll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡶࡲ࡯ࡳࡦࡪࠠ࡭ࡱࡪࡷ࠿ࠦࠧ≮") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1ll1lll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡲࡩ࡯࡮ࡨࠢ࡯ࡳ࡬ࡹ࠺ࠨ≯") + str(e))
  finally:
    try:
      bstack1l111l1111l_opy_()
      bstack1lllll1l11ll_opy_()
    except:
      pass
    if bstack1lll1lll11_opy_ and bstack1lllll1llll1_opy_:
      bstack1lll1lll11_opy_.end(EVENTS.bstack111l1l1l11l_opy_.value, bstack1lllll1llll1_opy_ + bstack1ll1lll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ≰"), bstack1lllll1llll1_opy_ + bstack1ll1lll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ≱"), status=True, failure=None, test_name=None)
    try:
      elapsed = time.time() - start_time
      get_logger().debug(bstack1ll1lll_opy_ (u"ࠧࡹࡥ࡯ࡦࡢࡰࡴ࡭ࡳࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠤ࡮ࡴࠠࡼ࠼࠱࠷࡫ࢃࠠࡴࡧࡦࡳࡳࡪࡳࠣ≲").format(elapsed))
    except Exception:
      pass