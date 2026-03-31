# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
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
from bstack_utils.constants import bstack1111lllll1l_opy_, EVENTS, bstack111l11lll11_opy_, bstack111l111l111_opy_, STAGE
import tempfile
import json
bstack1lllll1l1111_opy_ = os.getenv(bstack1ll11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡋࡤࡌࡉࡍࡇࠥ≓"), None) or os.path.join(tempfile.gettempdir(), bstack1ll11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡧࡩࡧࡻࡧ࠯࡮ࡲ࡫ࠧ≔"))
bstack1lllll11l1ll_opy_ = os.path.join(bstack1ll11_opy_ (u"ࠦࡱࡵࡧࠣ≕"), bstack1ll11_opy_ (u"ࠬࡹࡤ࡬࠯ࡦࡰ࡮࠳ࡤࡦࡤࡸ࡫࠳ࡲ࡯ࡨࠩ≖"))
_1lllll1l11ll_opy_ = threading.Lock()
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1ll11_opy_ (u"࠭ࠥࠩࡣࡶࡧࡹ࡯࡭ࡦࠫࡶࠤࡠࠫࠨ࡯ࡣࡰࡩ࠮ࡹ࡝࡜ࠧࠫࡰࡪࡼࡥ࡭ࡰࡤࡱࡪ࠯ࡳ࡞ࠢ࠰ࠤࠪ࠮࡭ࡦࡵࡶࡥ࡬࡫ࠩࡴࠩ≗"),
      datefmt=bstack1ll11_opy_ (u"࡛ࠧࠦ࠰ࠩࡲ࠳ࠥࡥࡖࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࡞ࠬ≘"),
      stream=sys.stdout
    )
  return logger
def get_automation_logger(name=__name__, level=logging.DEBUG):
  bstack1ll11_opy_ (u"ࠣࠤࠥࠎࠥࠦࡒࡦࡶࡸࡶࡳࡹࠠࡢࠢ࡯ࡳ࡬࡭ࡥࡳࠢࡷ࡬ࡦࡺࠠࡸࡴ࡬ࡸࡪࡹࠠࡰࡰ࡯ࡽࠥࡺ࡯ࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠳ࡲ࡯ࡨࠢࡩ࡭ࡱ࡫ࠊࠡࠢࡆࡶࡪࡧࡴࡦࡵࠣࡥࡳࡪࠠ࡮ࡣࡱࡥ࡬࡫ࡳࠡ࡫ࡷࡷࠥࡵࡷ࡯ࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡦࡪ࡮ࡨࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶࠏࠦࠠࡐࡰ࡯ࡽࠥ࡫࡮ࡢࡤ࡯ࡩࡸࠦ࡬ࡰࡩࡪ࡭ࡳ࡭ࠠࡪࡨࠣࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓࡥࡌࡐࡉࡖࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵࠢࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠤ࡮ࡹࠠࡴࡧࡷࠤࡹࡵࠠࡢࠢࡷࡶࡺࡺࡨࡺࠢࡹࡥࡱࡻࡥࠋࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦ࡮ࡢ࡯ࡨ࠾ࠥࡒ࡯ࡨࡩࡨࡶࠥࡴࡡ࡮ࡧࠣࠬࡩ࡫ࡦࡢࡷ࡯ࡸࡸࠦࡴࡰࠢࡢࡣࡳࡧ࡭ࡦࡡࡢ࠭ࠏࠦࠠࠡࠢ࡯ࡩࡻ࡫࡬࠻ࠢࡏࡳ࡬࡭ࡩ࡯ࡩࠣࡰࡪࡼࡥ࡭ࠢࠫࡨࡪ࡬ࡡࡶ࡮ࡷࡷࠥࡺ࡯ࠡࡆࡈࡆ࡚ࡍࠩࠋࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢ࡯ࡳ࡬࡭ࡩ࡯ࡩ࠱ࡐࡴ࡭ࡧࡦࡴ࠽ࠤࡈࡵ࡮ࡧ࡫ࡪࡹࡷ࡫ࡤࠡ࡮ࡲ࡫࡬࡫ࡲࠡࡶ࡫ࡥࡹࠦࡷࡳ࡫ࡷࡩࡸࠦ࡯࡯࡮ࡼࠤࡹࡵࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠲ࡱࡵࡧࠡࠪ࡬ࡪࠥ࡫࡮ࡢࡤ࡯ࡩࡩ࠯ࠊࠡࠢࠥࠦࠧ≙")
  logger_name = bstack1ll11_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠴ࡻ࠱ࡿࠥ≚").format(name)
  logger = logging.getLogger(logger_name)
  is_enabled = os.getenv(bstack1ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓࡥࡌࡐࡉࡖࠫ≛"), bstack1ll11_opy_ (u"ࠫࠬ≜")).lower() == bstack1ll11_opy_ (u"ࠬࡺࡲࡶࡧࠪ≝")
  if not is_enabled:
    logger.setLevel(logging.CRITICAL)
    logger.propagate = False
    return logger
  with _1lllll1l11ll_opy_:
    if logger.handlers:
      return logger
    bstack1lllll1111ll_opy_ = os.path.join(os.getcwd(), bstack1ll11_opy_ (u"࠭࡬ࡰࡩࠪ≞"), bstack1ll11_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠲ࡱࡵࡧࠨ≟"))
    log_dir = os.path.dirname(bstack1lllll1111ll_opy_)
    if not os.path.exists(log_dir):
      os.makedirs(log_dir)
    bstack1lllll1l1l1l_opy_ = logging.FileHandler(bstack1lllll1111ll_opy_)
    bstack1lllll1l1l11_opy_ = logging.Formatter(
      fmt=bstack1ll11_opy_ (u"ࠨࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲࡛ࠦࠡࡕࡇࡏ࠲ࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠢࡠࠤࠪ࠮࡭ࡦࡵࡶࡥ࡬࡫ࠩࡴࠩ≠"),
      datefmt=bstack1ll11_opy_ (u"ࠩࠨ࡝࠲ࠫ࡭࠮ࠧࡧࡘࠪࡎ࠺ࠦࡏ࠽ࠩࡘࡠࠧ≡"),
    )
    bstack1lllll1l1l1l_opy_.setFormatter(bstack1lllll1l1l11_opy_)
    bstack1lllll1l1l1l_opy_.setLevel(level)
    bstack1lllll1l1l1l_opy_.addFilter(lambda r: r.name != bstack1ll11_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲ࠯ࡴࡨࡱࡴࡺࡥ࠯ࡴࡨࡱࡴࡺࡥࡠࡥࡲࡲࡳ࡫ࡣࡵ࡫ࡲࡲࠬ≢"))
    logger.addHandler(bstack1lllll1l1l1l_opy_)
    logger.setLevel(level)
    logger.propagate = False
  return logger
def get_log_level():
  bstack1lllll111lll_opy_ = os.environ.get(bstack1ll11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢࡈࡊࡈࡕࡈࠤ≣"), bstack1ll11_opy_ (u"ࠧ࡬ࡡ࡭ࡵࡨࠦ≤"))
  return logging.DEBUG if bstack1lllll111lll_opy_.lower() == bstack1ll11_opy_ (u"ࠨࡴࡳࡷࡨࠦ≥") else logging.INFO
def bstack1l1111llll1_opy_():
  global bstack1lllll1l1111_opy_
  if os.path.exists(bstack1lllll1l1111_opy_):
    os.remove(bstack1lllll1l1111_opy_)
  if os.path.exists(bstack1lllll11l1ll_opy_):
    os.remove(bstack1lllll11l1ll_opy_)
def bstack1ll11ll1l1_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def configure_logger(config, log_level):
  bstack1lllll1l1ll1_opy_ = log_level
  if bstack1ll11_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩ≦") in config and config[bstack1ll11_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪ≧")] in bstack111l11lll11_opy_:
    bstack1lllll1l1ll1_opy_ = bstack111l11lll11_opy_[config[bstack1ll11_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫ≨")]]
  if config.get(bstack1ll11_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬ≩"), False):
    logging.getLogger().setLevel(bstack1lllll1l1ll1_opy_)
    return bstack1lllll1l1ll1_opy_
  global bstack1lllll1l1111_opy_
  bstack1ll11ll1l1_opy_()
  bstack1llll1llllll_opy_ = logging.Formatter(
    fmt=bstack1ll11_opy_ (u"ࠫࠪ࠮ࡡࡴࡥࡷ࡭ࡲ࡫ࠩࡴࠢ࡞ࠩ࠭ࡴࡡ࡮ࡧࠬࡷࡢࡡࠥࠩ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨ࠭ࡸࡣࠠ࠮ࠢࠨࠬࡲ࡫ࡳࡴࡣࡪࡩ࠮ࡹࠧ≪"),
    datefmt=bstack1ll11_opy_ (u"࡙ࠬࠫ࠮ࠧࡰ࠱ࠪࡪࡔࠦࡊ࠽ࠩࡒࡀࠥࡔ࡜ࠪ≫"),
  )
  bstack1lllll1l11l1_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1lllll1l1111_opy_)
  file_handler.setFormatter(bstack1llll1llllll_opy_)
  bstack1lllll1l11l1_opy_.setFormatter(bstack1llll1llllll_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1lllll1l11l1_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1ll11_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠯ࡹࡨࡦࡩࡸࡩࡷࡧࡵ࠲ࡷ࡫࡭ࡰࡶࡨ࠲ࡷ࡫࡭ࡰࡶࡨࡣࡨࡵ࡮࡯ࡧࡦࡸ࡮ࡵ࡮ࠨ≬"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1lllll1l11l1_opy_.setLevel(bstack1lllll1l1ll1_opy_)
  logging.getLogger().addHandler(bstack1lllll1l11l1_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1lllll1l1ll1_opy_
def bstack1lllll11111l_opy_(config):
  try:
    bstack1llll1lllll1_opy_ = set(bstack111l111l111_opy_)
    bstack1lllll11l11l_opy_ = bstack1ll11_opy_ (u"ࠧࠨ≭")
    with open(bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫ≮")) as bstack1lllll111ll1_opy_:
      bstack1llll1llll1l_opy_ = bstack1lllll111ll1_opy_.read()
      bstack1lllll11l11l_opy_ = re.sub(bstack1ll11_opy_ (u"ࡴࠪࡢ࠭ࡢࡳࠬࠫࡂࠧ࠳࠰ࠤ࡝ࡰࠪ≯"), bstack1ll11_opy_ (u"ࠪࠫ≰"), bstack1llll1llll1l_opy_, flags=re.M)
      bstack1lllll11l11l_opy_ = re.sub(
        bstack1ll11_opy_ (u"ࡶࠬࡤࠨ࡝ࡵ࠮࠭ࡄ࠮ࠧ≱") + bstack1ll11_opy_ (u"ࠬࢂࠧ≲").join(bstack1llll1lllll1_opy_) + bstack1ll11_opy_ (u"࠭ࠩ࠯ࠬࠧࠫ≳"),
        bstack1ll11_opy_ (u"ࡲࠨ࡞࠵࠾ࠥࡡࡒࡆࡆࡄࡇ࡙ࡋࡄ࡞ࠩ≴"),
        bstack1lllll11l11l_opy_, flags=re.M | re.I
      )
    def bstack1lllll11l1l1_opy_(dic):
      bstack1lllll111l1l_opy_ = {}
      for key, value in dic.items():
        if key in bstack1llll1lllll1_opy_:
          bstack1lllll111l1l_opy_[key] = bstack1ll11_opy_ (u"ࠨ࡝ࡕࡉࡉࡇࡃࡕࡇࡇࡡࠬ≵")
        else:
          if isinstance(value, dict):
            bstack1lllll111l1l_opy_[key] = bstack1lllll11l1l1_opy_(value)
          else:
            bstack1lllll111l1l_opy_[key] = value
      return bstack1lllll111l1l_opy_
    bstack1lllll111l1l_opy_ = bstack1lllll11l1l1_opy_(config)
    return {
      bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬ≶"): bstack1lllll11l11l_opy_,
      bstack1ll11_opy_ (u"ࠪࡪ࡮ࡴࡡ࡭ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭≷"): json.dumps(bstack1lllll111l1l_opy_)
    }
  except Exception as e:
    return {}
def bstack1lllll111l11_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack1ll11_opy_ (u"ࠫࡱࡵࡧࠨ≸"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack1lll1l11l11_opy_ = os.path.join(log_dir, bstack1ll11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡩ࡯࡯ࡨ࡬࡫ࡸ࠭≹"))
  if not os.path.exists(bstack1lll1l11l11_opy_):
    bstack1lllll11ll1l_opy_ = {
      bstack1ll11_opy_ (u"ࠨࡩ࡯࡫ࡳࡥࡹ࡮ࠢ≺"): str(inipath),
      bstack1ll11_opy_ (u"ࠢࡳࡱࡲࡸࡵࡧࡴࡩࠤ≻"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack1ll11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡥࡲࡲ࡫࡯ࡧࡴ࠰࡭ࡷࡴࡴࠧ≼")), bstack1ll11_opy_ (u"ࠩࡺࠫ≽")) as bstack1lllll11llll_opy_:
      bstack1lllll11llll_opy_.write(json.dumps(bstack1lllll11ll1l_opy_))
def bstack1lllll1ll11l_opy_():
  try:
    bstack1lll1l11l11_opy_ = os.path.join(os.getcwd(), bstack1ll11_opy_ (u"ࠪࡰࡴ࡭ࠧ≾"), bstack1ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷ࠳ࡰࡳࡰࡰࠪ≿"))
    if os.path.exists(bstack1lll1l11l11_opy_):
      with open(bstack1lll1l11l11_opy_, bstack1ll11_opy_ (u"ࠬࡸࠧ⊀")) as bstack1lllll11llll_opy_:
        bstack1lllll11ll11_opy_ = json.load(bstack1lllll11llll_opy_)
      return bstack1lllll11ll11_opy_.get(bstack1ll11_opy_ (u"࠭ࡩ࡯࡫ࡳࡥࡹ࡮ࠧ⊁"), bstack1ll11_opy_ (u"ࠧࠨ⊂")), bstack1lllll11ll11_opy_.get(bstack1ll11_opy_ (u"ࠨࡴࡲࡳࡹࡶࡡࡵࡪࠪ⊃"), bstack1ll11_opy_ (u"ࠩࠪ⊄"))
  except:
    pass
  return None, None
def bstack1lllll111111_opy_():
  try:
    bstack1lll1l11l11_opy_ = os.path.join(os.getcwd(), bstack1ll11_opy_ (u"ࠪࡰࡴ࡭ࠧ⊅"), bstack1ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷ࠳ࡰࡳࡰࡰࠪ⊆"))
    if os.path.exists(bstack1lll1l11l11_opy_):
      os.remove(bstack1lll1l11l11_opy_)
  except:
    pass
def bstack11111lll1l_opy_(config):
  try:
    try:
      from bstack_utils.bstack1ll1lll11l_opy_ import bstack11ll11l1ll_opy_
    except Exception:
      bstack11ll11l1ll_opy_ = None
    start_time = time.time()
    from bstack_utils.helper import global_config, bstack1l11llll11_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack1lllll1l1111_opy_
    if config.get(bstack1ll11_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧ⊇"), False):
      return
    uuid = os.getenv(bstack1ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ⊈")) if os.getenv(bstack1ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ⊉")) else global_config.get_property(bstack1ll11_opy_ (u"ࠣࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠥ⊊"))
    if not uuid or uuid == bstack1ll11_opy_ (u"ࠩࡱࡹࡱࡲࠧ⊋"):
      return
    bstack1lllll11lll1_opy_ = bstack11ll11l1ll_opy_.bstack11l11l111_opy_(EVENTS.bstack111l1111l1l_opy_.value) if bstack11ll11l1ll_opy_ else None
    bstack1lllll1ll111_opy_ = [bstack1ll11_opy_ (u"ࠪࡶࡪࡷࡵࡪࡴࡨࡱࡪࡴࡴࡴ࠰ࡷࡼࡹ࠭⊌"), bstack1ll11_opy_ (u"ࠫࡕ࡯ࡰࡧ࡫࡯ࡩࠬ⊍"), bstack1ll11_opy_ (u"ࠬࡶࡹࡱࡴࡲ࡮ࡪࡩࡴ࠯ࡶࡲࡱࡱ࠭⊎"), bstack1lllll1l1111_opy_, bstack1lllll11l1ll_opy_]
    bstack1lllll1l111l_opy_, root_path = bstack1lllll1ll11l_opy_()
    if bstack1lllll1l111l_opy_ != None:
      bstack1lllll1ll111_opy_.append(bstack1lllll1l111l_opy_)
    if root_path != None:
      bstack1lllll1ll111_opy_.append(os.path.join(root_path, bstack1ll11_opy_ (u"࠭ࡣࡰࡰࡩࡸࡪࡹࡴ࠯ࡲࡼࠫ⊏")))
    bstack1lllll11l111_opy_ = os.path.join(os.getcwd(), bstack1ll11_opy_ (u"ࠧ࡭ࡱࡪࠫ⊐"), bstack1ll11_opy_ (u"ࠨ࡭ࡨࡽ࠲ࡳࡥࡵࡴ࡬ࡧࡸ࠴ࡪࡴࡱࡱࠫ⊑"))
    if os.path.exists(bstack1lllll11l111_opy_):
      bstack1lllll1ll111_opy_.append(bstack1lllll11l111_opy_)
    output_file = os.path.join(tempfile.gettempdir(), bstack1ll11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠯࡯ࡳ࡬ࡹ࠭ࠨ⊒") + uuid + bstack1ll11_opy_ (u"ࠪ࠲ࡹࡧࡲ࠯ࡩࡽࠫ⊓"))
    with tarfile.open(output_file, bstack1ll11_opy_ (u"ࠦࡼࡀࡧࡻࠤ⊔")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1lllll1ll111_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1lllll11111l_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1lllll1l1lll_opy_ = data.encode()
        tarinfo.size = len(bstack1lllll1l1lll_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1lllll1l1lll_opy_))
    multipart_data = MultipartEncoder(
      fields= {
        bstack1ll11_opy_ (u"ࠬࡪࡡࡵࡣࠪ⊕"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1ll11_opy_ (u"࠭ࡲࡣࠩ⊖")), bstack1ll11_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡾ࠭ࡨࡼ࡬ࡴࠬ⊗")),
        bstack1ll11_opy_ (u"ࠨࡥ࡯࡭ࡪࡴࡴࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ⊘"): uuid
      }
    )
    bstack1lllll1111l1_opy_ = bstack1l11llll11_opy_(cli.config, [bstack1ll11_opy_ (u"ࠤࡤࡴ࡮ࡹࠢ⊙"), bstack1ll11_opy_ (u"ࠥࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠥ⊚"), bstack1ll11_opy_ (u"ࠦࡺࡶ࡬ࡰࡣࡧࠦ⊛")], bstack1111lllll1l_opy_)
    response = requests.post(
      bstack1ll11_opy_ (u"ࠧࢁࡽ࠰ࡥ࡯࡭ࡪࡴࡴ࠮࡮ࡲ࡫ࡸ࠵ࡵࡱ࡮ࡲࡥࡩࠨ⊜").format(bstack1lllll1111l1_opy_),
      data=multipart_data,
      headers={bstack1ll11_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬ⊝"): multipart_data.content_type},
      auth=(config[bstack1ll11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ⊞")], config[bstack1ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ⊟")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1ll11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡷࡳࡰࡴࡧࡤࠡ࡮ࡲ࡫ࡸࡀࠠࠨ⊠") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1ll11_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡩࡳࡪࡩ࡯ࡩࠣࡰࡴ࡭ࡳ࠻ࠩ⊡") + str(e))
  finally:
    try:
      bstack1l1111llll1_opy_()
      bstack1lllll111111_opy_()
    except:
      pass
    if bstack11ll11l1ll_opy_ and bstack1lllll11lll1_opy_:
      bstack11ll11l1ll_opy_.end(EVENTS.bstack111l1111l1l_opy_.value, bstack1lllll11lll1_opy_ + bstack1ll11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ⊢"), bstack1lllll11lll1_opy_ + bstack1ll11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ⊣"), status=True, failure=None, test_name=None)
    try:
      elapsed = time.time() - start_time
      get_logger().debug(bstack1ll11_opy_ (u"ࠨࡳࡦࡰࡧࡣࡱࡵࡧࡴࠢࡦࡳࡲࡶ࡬ࡦࡶࡨࡨࠥ࡯࡮ࠡࡽ࠽࠲࠸࡬ࡽࠡࡵࡨࡧࡴࡴࡤࡴࠤ⊤").format(elapsed))
    except Exception:
      pass