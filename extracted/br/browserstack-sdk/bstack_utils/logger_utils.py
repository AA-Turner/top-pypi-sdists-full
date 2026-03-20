# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
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
from bstack_utils.constants import bstack111l1l11ll1_opy_, EVENTS, bstack111l1l1l1ll_opy_, bstack111l1l11lll_opy_, STAGE
import tempfile
import json
bstack1lllll1lll1l_opy_ = os.getenv(bstack11lll1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡋࡤࡌࡉࡍࡇࠥ∛"), None) or os.path.join(tempfile.gettempdir(), bstack11lll1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡧࡩࡧࡻࡧ࠯࡮ࡲ࡫ࠧ∜"))
bstack1llllll111l1_opy_ = os.path.join(bstack11lll1_opy_ (u"ࠦࡱࡵࡧࠣ∝"), bstack11lll1_opy_ (u"ࠬࡹࡤ࡬࠯ࡦࡰ࡮࠳ࡤࡦࡤࡸ࡫࠳ࡲ࡯ࡨࠩ∞"))
_1lllll11l1ll_opy_ = threading.Lock()
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack11lll1_opy_ (u"࠭ࠥࠩࡣࡶࡧࡹ࡯࡭ࡦࠫࡶࠤࡠࠫࠨ࡯ࡣࡰࡩ࠮ࡹ࡝࡜ࠧࠫࡰࡪࡼࡥ࡭ࡰࡤࡱࡪ࠯ࡳ࡞ࠢ࠰ࠤࠪ࠮࡭ࡦࡵࡶࡥ࡬࡫ࠩࡴࠩ∟"),
      datefmt=bstack11lll1_opy_ (u"࡛ࠧࠦ࠰ࠩࡲ࠳ࠥࡥࡖࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࡞ࠬ∠"),
      stream=sys.stdout
    )
  return logger
def get_automation_logger(name=__name__, level=logging.DEBUG):
  bstack11lll1_opy_ (u"ࠣࠤࠥࠎࠥࠦࡒࡦࡶࡸࡶࡳࡹࠠࡢࠢ࡯ࡳ࡬࡭ࡥࡳࠢࡷ࡬ࡦࡺࠠࡸࡴ࡬ࡸࡪࡹࠠࡰࡰ࡯ࡽࠥࡺ࡯ࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠳ࡲ࡯ࡨࠢࡩ࡭ࡱ࡫ࠊࠡࠢࡆࡶࡪࡧࡴࡦࡵࠣࡥࡳࡪࠠ࡮ࡣࡱࡥ࡬࡫ࡳࠡ࡫ࡷࡷࠥࡵࡷ࡯ࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡦࡪ࡮ࡨࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶࠏࠦࠠࡐࡰ࡯ࡽࠥ࡫࡮ࡢࡤ࡯ࡩࡸࠦ࡬ࡰࡩࡪ࡭ࡳ࡭ࠠࡪࡨࠣࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓࡥࡌࡐࡉࡖࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵࠢࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠤ࡮ࡹࠠࡴࡧࡷࠤࡹࡵࠠࡢࠢࡷࡶࡺࡺࡨࡺࠢࡹࡥࡱࡻࡥࠋࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦ࡮ࡢ࡯ࡨ࠾ࠥࡒ࡯ࡨࡩࡨࡶࠥࡴࡡ࡮ࡧࠣࠬࡩ࡫ࡦࡢࡷ࡯ࡸࡸࠦࡴࡰࠢࡢࡣࡳࡧ࡭ࡦࡡࡢ࠭ࠏࠦࠠࠡࠢ࡯ࡩࡻ࡫࡬࠻ࠢࡏࡳ࡬࡭ࡩ࡯ࡩࠣࡰࡪࡼࡥ࡭ࠢࠫࡨࡪ࡬ࡡࡶ࡮ࡷࡷࠥࡺ࡯ࠡࡆࡈࡆ࡚ࡍࠩࠋࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢ࡯ࡳ࡬࡭ࡩ࡯ࡩ࠱ࡐࡴ࡭ࡧࡦࡴ࠽ࠤࡈࡵ࡮ࡧ࡫ࡪࡹࡷ࡫ࡤࠡ࡮ࡲ࡫࡬࡫ࡲࠡࡶ࡫ࡥࡹࠦࡷࡳ࡫ࡷࡩࡸࠦ࡯࡯࡮ࡼࠤࡹࡵࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠲ࡱࡵࡧࠡࠪ࡬ࡪࠥ࡫࡮ࡢࡤ࡯ࡩࡩ࠯ࠊࠡࠢࠥࠦࠧ∡")
  logger_name = bstack11lll1_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠴ࡻ࠱ࡿࠥ∢").format(name)
  logger = logging.getLogger(logger_name)
  is_enabled = os.getenv(bstack11lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓࡥࡌࡐࡉࡖࠫ∣"), bstack11lll1_opy_ (u"ࠫࠬ∤")).lower() == bstack11lll1_opy_ (u"ࠬࡺࡲࡶࡧࠪ∥")
  if not is_enabled:
    logger.setLevel(logging.CRITICAL)
    logger.propagate = False
    return logger
  with _1lllll11l1ll_opy_:
    if logger.handlers:
      return logger
    bstack1llllll11l1l_opy_ = os.path.join(os.getcwd(), bstack11lll1_opy_ (u"࠭࡬ࡰࡩࠪ∦"), bstack11lll1_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠲ࡱࡵࡧࠨ∧"))
    log_dir = os.path.dirname(bstack1llllll11l1l_opy_)
    if not os.path.exists(log_dir):
      os.makedirs(log_dir)
    bstack1lllll1ll1ll_opy_ = logging.FileHandler(bstack1llllll11l1l_opy_)
    bstack1llllll1111l_opy_ = logging.Formatter(
      fmt=bstack11lll1_opy_ (u"ࠨࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲࡛ࠦࠡࡕࡇࡏ࠲ࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠢࡠࠤࠪ࠮࡭ࡦࡵࡶࡥ࡬࡫ࠩࡴࠩ∨"),
      datefmt=bstack11lll1_opy_ (u"ࠩࠨ࡝࠲ࠫ࡭࠮ࠧࡧࡘࠪࡎ࠺ࠦࡏ࠽ࠩࡘࡠࠧ∩"),
    )
    bstack1lllll1ll1ll_opy_.setFormatter(bstack1llllll1111l_opy_)
    bstack1lllll1ll1ll_opy_.setLevel(level)
    bstack1lllll1ll1ll_opy_.addFilter(lambda r: r.name != bstack11lll1_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲ࠯ࡴࡨࡱࡴࡺࡥ࠯ࡴࡨࡱࡴࡺࡥࡠࡥࡲࡲࡳ࡫ࡣࡵ࡫ࡲࡲࠬ∪"))
    logger.addHandler(bstack1lllll1ll1ll_opy_)
    logger.setLevel(level)
    logger.propagate = False
  return logger
def get_log_level():
  bstack1lllll11llll_opy_ = os.environ.get(bstack11lll1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢࡈࡊࡈࡕࡈࠤ∫"), bstack11lll1_opy_ (u"ࠧ࡬ࡡ࡭ࡵࡨࠦ∬"))
  return logging.DEBUG if bstack1lllll11llll_opy_.lower() == bstack11lll1_opy_ (u"ࠨࡴࡳࡷࡨࠦ∭") else logging.INFO
def bstack1l1111llll1_opy_():
  global bstack1lllll1lll1l_opy_
  if os.path.exists(bstack1lllll1lll1l_opy_):
    os.remove(bstack1lllll1lll1l_opy_)
  if os.path.exists(bstack1llllll111l1_opy_):
    os.remove(bstack1llllll111l1_opy_)
def bstack111l1ll1l_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def configure_logger(config, log_level):
  bstack1lllll1l11ll_opy_ = log_level
  if bstack11lll1_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩ∮") in config and config[bstack11lll1_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪ∯")] in bstack111l1l1l1ll_opy_:
    bstack1lllll1l11ll_opy_ = bstack111l1l1l1ll_opy_[config[bstack11lll1_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫ∰")]]
  if config.get(bstack11lll1_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬ∱"), False):
    logging.getLogger().setLevel(bstack1lllll1l11ll_opy_)
    return bstack1lllll1l11ll_opy_
  global bstack1lllll1lll1l_opy_
  bstack111l1ll1l_opy_()
  bstack1lllll1l111l_opy_ = logging.Formatter(
    fmt=bstack11lll1_opy_ (u"ࠫࠪ࠮ࡡࡴࡥࡷ࡭ࡲ࡫ࠩࡴࠢ࡞ࠩ࠭ࡴࡡ࡮ࡧࠬࡷࡢࡡࠥࠩ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨ࠭ࡸࡣࠠ࠮ࠢࠨࠬࡲ࡫ࡳࡴࡣࡪࡩ࠮ࡹࠧ∲"),
    datefmt=bstack11lll1_opy_ (u"࡙ࠬࠫ࠮ࠧࡰ࠱ࠪࡪࡔࠦࡊ࠽ࠩࡒࡀࠥࡔ࡜ࠪ∳"),
  )
  bstack1lllll1l1ll1_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1lllll1lll1l_opy_)
  file_handler.setFormatter(bstack1lllll1l111l_opy_)
  bstack1lllll1l1ll1_opy_.setFormatter(bstack1lllll1l111l_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1lllll1l1ll1_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack11lll1_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠯ࡹࡨࡦࡩࡸࡩࡷࡧࡵ࠲ࡷ࡫࡭ࡰࡶࡨ࠲ࡷ࡫࡭ࡰࡶࡨࡣࡨࡵ࡮࡯ࡧࡦࡸ࡮ࡵ࡮ࠨ∴"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1lllll1l1ll1_opy_.setLevel(bstack1lllll1l11ll_opy_)
  logging.getLogger().addHandler(bstack1lllll1l1ll1_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1lllll1l11ll_opy_
def bstack1llllll111ll_opy_(config):
  try:
    bstack1llllll11l11_opy_ = set(bstack111l1l11lll_opy_)
    bstack1lllll1ll11l_opy_ = bstack11lll1_opy_ (u"ࠧࠨ∵")
    with open(bstack11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫ∶")) as bstack1llllll11lll_opy_:
      bstack1lllll1l1lll_opy_ = bstack1llllll11lll_opy_.read()
      bstack1lllll1ll11l_opy_ = re.sub(bstack11lll1_opy_ (u"ࡴࠪࡢ࠭ࡢࡳࠬࠫࡂࠧ࠳࠰ࠤ࡝ࡰࠪ∷"), bstack11lll1_opy_ (u"ࠪࠫ∸"), bstack1lllll1l1lll_opy_, flags=re.M)
      bstack1lllll1ll11l_opy_ = re.sub(
        bstack11lll1_opy_ (u"ࡶࠬࡤࠨ࡝ࡵ࠮࠭ࡄ࠮ࠧ∹") + bstack11lll1_opy_ (u"ࠬࢂࠧ∺").join(bstack1llllll11l11_opy_) + bstack11lll1_opy_ (u"࠭ࠩ࠯ࠬࠧࠫ∻"),
        bstack11lll1_opy_ (u"ࡲࠨ࡞࠵࠾ࠥࡡࡒࡆࡆࡄࡇ࡙ࡋࡄ࡞ࠩ∼"),
        bstack1lllll1ll11l_opy_, flags=re.M | re.I
      )
    def bstack1lllll1l1l1l_opy_(dic):
      bstack1lllll1l1l11_opy_ = {}
      for key, value in dic.items():
        if key in bstack1llllll11l11_opy_:
          bstack1lllll1l1l11_opy_[key] = bstack11lll1_opy_ (u"ࠨ࡝ࡕࡉࡉࡇࡃࡕࡇࡇࡡࠬ∽")
        else:
          if isinstance(value, dict):
            bstack1lllll1l1l11_opy_[key] = bstack1lllll1l1l1l_opy_(value)
          else:
            bstack1lllll1l1l11_opy_[key] = value
      return bstack1lllll1l1l11_opy_
    bstack1lllll1l1l11_opy_ = bstack1lllll1l1l1l_opy_(config)
    return {
      bstack11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬ∾"): bstack1lllll1ll11l_opy_,
      bstack11lll1_opy_ (u"ࠪࡪ࡮ࡴࡡ࡭ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭∿"): json.dumps(bstack1lllll1l1l11_opy_)
    }
  except Exception as e:
    return {}
def bstack1lllll11ll11_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack11lll1_opy_ (u"ࠫࡱࡵࡧࠨ≀"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack1lll1lll11l_opy_ = os.path.join(log_dir, bstack11lll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡩ࡯࡯ࡨ࡬࡫ࡸ࠭≁"))
  if not os.path.exists(bstack1lll1lll11l_opy_):
    bstack1lllll11ll1l_opy_ = {
      bstack11lll1_opy_ (u"ࠨࡩ࡯࡫ࡳࡥࡹ࡮ࠢ≂"): str(inipath),
      bstack11lll1_opy_ (u"ࠢࡳࡱࡲࡸࡵࡧࡴࡩࠤ≃"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack11lll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡥࡲࡲ࡫࡯ࡧࡴ࠰࡭ࡷࡴࡴࠧ≄")), bstack11lll1_opy_ (u"ࠩࡺࠫ≅")) as bstack1lllll1lll11_opy_:
      bstack1lllll1lll11_opy_.write(json.dumps(bstack1lllll11ll1l_opy_))
def bstack1lllll1lllll_opy_():
  try:
    bstack1lll1lll11l_opy_ = os.path.join(os.getcwd(), bstack11lll1_opy_ (u"ࠪࡰࡴ࡭ࠧ≆"), bstack11lll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷ࠳ࡰࡳࡰࡰࠪ≇"))
    if os.path.exists(bstack1lll1lll11l_opy_):
      with open(bstack1lll1lll11l_opy_, bstack11lll1_opy_ (u"ࠬࡸࠧ≈")) as bstack1lllll1lll11_opy_:
        bstack1lllll1l1111_opy_ = json.load(bstack1lllll1lll11_opy_)
      return bstack1lllll1l1111_opy_.get(bstack11lll1_opy_ (u"࠭ࡩ࡯࡫ࡳࡥࡹ࡮ࠧ≉"), bstack11lll1_opy_ (u"ࠧࠨ≊")), bstack1lllll1l1111_opy_.get(bstack11lll1_opy_ (u"ࠨࡴࡲࡳࡹࡶࡡࡵࡪࠪ≋"), bstack11lll1_opy_ (u"ࠩࠪ≌"))
  except:
    pass
  return None, None
def bstack1lllll1llll1_opy_():
  try:
    bstack1lll1lll11l_opy_ = os.path.join(os.getcwd(), bstack11lll1_opy_ (u"ࠪࡰࡴ࡭ࠧ≍"), bstack11lll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷ࠳ࡰࡳࡰࡰࠪ≎"))
    if os.path.exists(bstack1lll1lll11l_opy_):
      os.remove(bstack1lll1lll11l_opy_)
  except:
    pass
def bstack1l1111l1ll_opy_(config):
  try:
    try:
      from bstack_utils.bstack1lll11lll_opy_ import bstack1llll11l_opy_
    except Exception:
      bstack1llll11l_opy_ = None
    start_time = time.time()
    from bstack_utils.helper import global_config, bstack11111l11ll_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack1lllll1lll1l_opy_
    if config.get(bstack11lll1_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧ≏"), False):
      return
    uuid = os.getenv(bstack11lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ≐")) if os.getenv(bstack11lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ≑")) else global_config.get_property(bstack11lll1_opy_ (u"ࠣࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠥ≒"))
    if not uuid or uuid == bstack11lll1_opy_ (u"ࠩࡱࡹࡱࡲࠧ≓"):
      return
    bstack1llllll11111_opy_ = bstack1llll11l_opy_.bstack11ll11l1l_opy_(EVENTS.bstack111l1l1111l_opy_.value) if bstack1llll11l_opy_ else None
    bstack1lllll1ll111_opy_ = [bstack11lll1_opy_ (u"ࠪࡶࡪࡷࡵࡪࡴࡨࡱࡪࡴࡴࡴ࠰ࡷࡼࡹ࠭≔"), bstack11lll1_opy_ (u"ࠫࡕ࡯ࡰࡧ࡫࡯ࡩࠬ≕"), bstack11lll1_opy_ (u"ࠬࡶࡹࡱࡴࡲ࡮ࡪࡩࡴ࠯ࡶࡲࡱࡱ࠭≖"), bstack1lllll1lll1l_opy_, bstack1llllll111l1_opy_]
    bstack1lllll1ll1l1_opy_, root_path = bstack1lllll1lllll_opy_()
    if bstack1lllll1ll1l1_opy_ != None:
      bstack1lllll1ll111_opy_.append(bstack1lllll1ll1l1_opy_)
    if root_path != None:
      bstack1lllll1ll111_opy_.append(os.path.join(root_path, bstack11lll1_opy_ (u"࠭ࡣࡰࡰࡩࡸࡪࡹࡴ࠯ࡲࡼࠫ≗")))
    bstack1lllll1l11l1_opy_ = os.path.join(os.getcwd(), bstack11lll1_opy_ (u"ࠧ࡭ࡱࡪࠫ≘"), bstack11lll1_opy_ (u"ࠨ࡭ࡨࡽ࠲ࡳࡥࡵࡴ࡬ࡧࡸ࠴ࡪࡴࡱࡱࠫ≙"))
    if os.path.exists(bstack1lllll1l11l1_opy_):
      bstack1lllll1ll111_opy_.append(bstack1lllll1l11l1_opy_)
    output_file = os.path.join(tempfile.gettempdir(), bstack11lll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠯࡯ࡳ࡬ࡹ࠭ࠨ≚") + uuid + bstack11lll1_opy_ (u"ࠪ࠲ࡹࡧࡲ࠯ࡩࡽࠫ≛"))
    with tarfile.open(output_file, bstack11lll1_opy_ (u"ࠦࡼࡀࡧࡻࠤ≜")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1lllll1ll111_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1llllll111ll_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1llllll11ll1_opy_ = data.encode()
        tarinfo.size = len(bstack1llllll11ll1_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1llllll11ll1_opy_))
    multipart_data = MultipartEncoder(
      fields= {
        bstack11lll1_opy_ (u"ࠬࡪࡡࡵࡣࠪ≝"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack11lll1_opy_ (u"࠭ࡲࡣࠩ≞")), bstack11lll1_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡾ࠭ࡨࡼ࡬ࡴࠬ≟")),
        bstack11lll1_opy_ (u"ࠨࡥ࡯࡭ࡪࡴࡴࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ≠"): uuid
      }
    )
    bstack1lllll11lll1_opy_ = bstack11111l11ll_opy_(cli.config, [bstack11lll1_opy_ (u"ࠤࡤࡴ࡮ࡹࠢ≡"), bstack11lll1_opy_ (u"ࠥࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠥ≢"), bstack11lll1_opy_ (u"ࠦࡺࡶ࡬ࡰࡣࡧࠦ≣")], bstack111l1l11ll1_opy_)
    response = requests.post(
      bstack11lll1_opy_ (u"ࠧࢁࡽ࠰ࡥ࡯࡭ࡪࡴࡴ࠮࡮ࡲ࡫ࡸ࠵ࡵࡱ࡮ࡲࡥࡩࠨ≤").format(bstack1lllll11lll1_opy_),
      data=multipart_data,
      headers={bstack11lll1_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬ≥"): multipart_data.content_type},
      auth=(config[bstack11lll1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ≦")], config[bstack11lll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ≧")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack11lll1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡷࡳࡰࡴࡧࡤࠡ࡮ࡲ࡫ࡸࡀࠠࠨ≨") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack11lll1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡩࡳࡪࡩ࡯ࡩࠣࡰࡴ࡭ࡳ࠻ࠩ≩") + str(e))
  finally:
    try:
      bstack1l1111llll1_opy_()
      bstack1lllll1llll1_opy_()
    except:
      pass
    if bstack1llll11l_opy_ and bstack1llllll11111_opy_:
      bstack1llll11l_opy_.end(EVENTS.bstack111l1l1111l_opy_.value, bstack1llllll11111_opy_ + bstack11lll1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ≪"), bstack1llllll11111_opy_ + bstack11lll1_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ≫"), status=True, failure=None, test_name=None)
    try:
      elapsed = time.time() - start_time
      get_logger().debug(bstack11lll1_opy_ (u"ࠨࡳࡦࡰࡧࡣࡱࡵࡧࡴࠢࡦࡳࡲࡶ࡬ࡦࡶࡨࡨࠥ࡯࡮ࠡࡽ࠽࠲࠸࡬ࡽࠡࡵࡨࡧࡴࡴࡤࡴࠤ≬").format(elapsed))
    except Exception:
      pass