# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
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
from bstack_utils.constants import bstack11111l1l111_opy_, EVENTS, bstack111111l11ll_opy_, bstack11111ll111l_opy_, STAGE
import tempfile
import json
bstack1lll1ll11111_opy_ = os.getenv(bstack1ll1l11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡉࡢࡊࡎࡒࡅࠣ␦"), None) or os.path.join(tempfile.gettempdir(), bstack1ll1l11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡥࡧࡥࡹ࡬࠴࡬ࡰࡩࠥ␧"))
bstack1lll1ll1ll11_opy_ = os.path.join(bstack1ll1l11_opy_ (u"ࠤ࡯ࡳ࡬ࠨ␨"), bstack1ll1l11_opy_ (u"ࠪࡷࡩࡱ࠭ࡤ࡮࡬࠱ࡩ࡫ࡢࡶࡩ࠱ࡰࡴ࡭ࠧ␩"))
_1lll1ll1l11l_opy_ = threading.Lock()
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1ll1l11_opy_ (u"ࠫࠪ࠮ࡡࡴࡥࡷ࡭ࡲ࡫ࠩࡴࠢ࡞ࠩ࠭ࡴࡡ࡮ࡧࠬࡷࡢࡡࠥࠩ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨ࠭ࡸࡣࠠ࠮ࠢࠨࠬࡲ࡫ࡳࡴࡣࡪࡩ࠮ࡹࠧ␪"),
      datefmt=bstack1ll1l11_opy_ (u"࡙ࠬࠫ࠮ࠧࡰ࠱ࠪࡪࡔࠦࡊ࠽ࠩࡒࡀࠥࡔ࡜ࠪ␫"),
      stream=sys.stdout
    )
  return logger
def get_automation_logger(name=__name__, level=logging.DEBUG):
  bstack1ll1l11_opy_ (u"ࠨࠢࠣࠌࠣࠤࡗ࡫ࡴࡶࡴࡱࡷࠥࡧࠠ࡭ࡱࡪ࡫ࡪࡸࠠࡵࡪࡤࡸࠥࡽࡲࡪࡶࡨࡷࠥࡵ࡮࡭ࡻࠣࡸࡴࠦࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠱ࡰࡴ࡭ࠠࡧ࡫࡯ࡩࠏࠦࠠࡄࡴࡨࡥࡹ࡫ࡳࠡࡣࡱࡨࠥࡳࡡ࡯ࡣࡪࡩࡸࠦࡩࡵࡵࠣࡳࡼࡴࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤ࡫࡯࡬ࡦࠢ࡫ࡥࡳࡪ࡬ࡦࡴࠍࠤࠥࡕ࡮࡭ࡻࠣࡩࡳࡧࡢ࡭ࡧࡶࠤࡱࡵࡧࡨ࡫ࡱ࡫ࠥ࡯ࡦࠡࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࡣࡑࡕࡇࡔࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠢ࡬ࡷࠥࡹࡥࡵࠢࡷࡳࠥࡧࠠࡵࡴࡸࡸ࡭ࡿࠠࡷࡣ࡯ࡹࡪࠐࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࡳࡧ࡭ࡦ࠼ࠣࡐࡴ࡭ࡧࡦࡴࠣࡲࡦࡳࡥࠡࠪࡧࡩ࡫ࡧࡵ࡭ࡶࡶࠤࡹࡵࠠࡠࡡࡱࡥࡲ࡫࡟ࡠࠫࠍࠤࠥࠦࠠ࡭ࡧࡹࡩࡱࡀࠠࡍࡱࡪ࡫࡮ࡴࡧࠡ࡮ࡨࡺࡪࡲࠠࠩࡦࡨࡪࡦࡻ࡬ࡵࡵࠣࡸࡴࠦࡄࡆࡄࡘࡋ࠮ࠐࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠ࡭ࡱࡪ࡫࡮ࡴࡧ࠯ࡎࡲ࡫࡬࡫ࡲ࠻ࠢࡆࡳࡳ࡬ࡩࡨࡷࡵࡩࡩࠦ࡬ࡰࡩࡪࡩࡷࠦࡴࡩࡣࡷࠤࡼࡸࡩࡵࡧࡶࠤࡴࡴ࡬ࡺࠢࡷࡳࠥࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠰࡯ࡳ࡬ࠦࠨࡪࡨࠣࡩࡳࡧࡢ࡭ࡧࡧ࠭ࠏࠦࠠࠣࠤࠥ␬")
  logger_name = bstack1ll1l11_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠲ࢀ࠶ࡽࠣ␭").format(name)
  logger = logging.getLogger(logger_name)
  is_enabled = os.getenv(bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࡣࡑࡕࡇࡔࠩ␮"), bstack1ll1l11_opy_ (u"ࠩࠪ␯")).lower() == bstack1ll1l11_opy_ (u"ࠪࡸࡷࡻࡥࠨ␰")
  if not is_enabled:
    logger.setLevel(logging.CRITICAL)
    logger.propagate = False
    return logger
  with _1lll1ll1l11l_opy_:
    if logger.handlers:
      return logger
    bstack1lll1ll1llll_opy_ = os.path.join(os.getcwd(), bstack1ll1l11_opy_ (u"ࠫࡱࡵࡧࠨ␱"), bstack1ll1l11_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠰࡯ࡳ࡬࠭␲"))
    log_dir = os.path.dirname(bstack1lll1ll1llll_opy_)
    if not os.path.exists(log_dir):
      os.makedirs(log_dir)
    bstack1lll1ll11ll1_opy_ = logging.FileHandler(bstack1lll1ll1llll_opy_)
    bstack1lll1ll111l1_opy_ = logging.Formatter(
      fmt=bstack1ll1l11_opy_ (u"࠭ࠥࠩࡣࡶࡧࡹ࡯࡭ࡦࠫࡶࠤࡠࠫࠨ࡯ࡣࡰࡩ࠮ࡹ࡝࡜ࠧࠫࡰࡪࡼࡥ࡭ࡰࡤࡱࡪ࠯ࡳ࡞ࠢ࠰ࠤࡠࠦࡓࡅࡍ࠰ࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠠ࡞ࠢࠨࠬࡲ࡫ࡳࡴࡣࡪࡩ࠮ࡹࠧ␳"),
      datefmt=bstack1ll1l11_opy_ (u"࡛ࠧࠦ࠰ࠩࡲ࠳ࠥࡥࡖࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࡞ࠬ␴"),
    )
    bstack1lll1ll11ll1_opy_.setFormatter(bstack1lll1ll111l1_opy_)
    bstack1lll1ll11ll1_opy_.setLevel(level)
    bstack1lll1ll11ll1_opy_.addFilter(lambda r: r.name != bstack1ll1l11_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷ࠴ࡲࡦ࡯ࡲࡸࡪ࠴ࡲࡦ࡯ࡲࡸࡪࡥࡣࡰࡰࡱࡩࡨࡺࡩࡰࡰࠪ␵"))
    logger.addHandler(bstack1lll1ll11ll1_opy_)
    logger.setLevel(level)
    logger.propagate = False
  return logger
def get_log_level():
  bstack1lll1l1ll11l_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡆࡈࡆ࡚ࡍࠢ␶"), bstack1ll1l11_opy_ (u"ࠥࡪࡦࡲࡳࡦࠤ␷"))
  return logging.DEBUG if bstack1lll1l1ll11l_opy_.lower() == bstack1ll1l11_opy_ (u"ࠦࡹࡸࡵࡦࠤ␸") else logging.INFO
def bstack11lll11ll1l_opy_():
  global bstack1lll1ll11111_opy_
  if os.path.exists(bstack1lll1ll11111_opy_):
    os.remove(bstack1lll1ll11111_opy_)
  if os.path.exists(bstack1lll1ll1ll11_opy_):
    os.remove(bstack1lll1ll1ll11_opy_)
def bstack1111111ll1_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def configure_logger(config, log_level):
  bstack1lll1l1ll1l1_opy_ = log_level
  if bstack1ll1l11_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧ␹") in config and config[bstack1ll1l11_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨ␺")] in bstack111111l11ll_opy_:
    bstack1lll1l1ll1l1_opy_ = bstack111111l11ll_opy_[config[bstack1ll1l11_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩ␻")]]
  if config.get(bstack1ll1l11_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪ␼"), False):
    logging.getLogger().setLevel(bstack1lll1l1ll1l1_opy_)
    return bstack1lll1l1ll1l1_opy_
  global bstack1lll1ll11111_opy_
  bstack1111111ll1_opy_()
  bstack1lll1ll11l1l_opy_ = logging.Formatter(
    fmt=bstack1ll1l11_opy_ (u"ࠩࠨࠬࡦࡹࡣࡵ࡫ࡰࡩ࠮ࡹࠠ࡜ࠧࠫࡲࡦࡳࡥࠪࡵࡠ࡟ࠪ࠮࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠫࡶࡡࠥ࠳ࠠࠦࠪࡰࡩࡸࡹࡡࡨࡧࠬࡷࠬ␽"),
    datefmt=bstack1ll1l11_opy_ (u"ࠪࠩ࡞࠳ࠥ࡮࠯ࠨࡨ࡙ࠫࡈ࠻ࠧࡐ࠾࡙࡚ࠪࠨ␾"),
  )
  bstack1lll1ll1l111_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1lll1ll11111_opy_)
  file_handler.setFormatter(bstack1lll1ll11l1l_opy_)
  bstack1lll1ll1l111_opy_.setFormatter(bstack1lll1ll11l1l_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1lll1ll1l111_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1ll1l11_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳ࠰ࡵࡩࡲࡵࡴࡦ࠰ࡵࡩࡲࡵࡴࡦࡡࡦࡳࡳࡴࡥࡤࡶ࡬ࡳࡳ࠭␿"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1lll1ll1l111_opy_.setLevel(bstack1lll1l1ll1l1_opy_)
  logging.getLogger().addHandler(bstack1lll1ll1l111_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1lll1l1ll1l1_opy_
def bstack1lll1ll1lll1_opy_(config):
  try:
    bstack1lll1ll1ll1l_opy_ = set(bstack11111ll111l_opy_)
    bstack1lll1l1l1lll_opy_ = bstack1ll1l11_opy_ (u"ࠬ࠭⑀")
    with open(bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩ⑁")) as bstack1lll1l1ll111_opy_:
      bstack1lll1ll111ll_opy_ = bstack1lll1l1ll111_opy_.read()
      bstack1lll1l1l1lll_opy_ = re.sub(bstack1ll1l11_opy_ (u"ࡲࠨࡠࠫࡠࡸ࠱ࠩࡀࠥ࠱࠮ࠩࡢ࡮ࠨ⑂"), bstack1ll1l11_opy_ (u"ࠨࠩ⑃"), bstack1lll1ll111ll_opy_, flags=re.M)
      bstack1lll1l1l1lll_opy_ = re.sub(
        bstack1ll1l11_opy_ (u"ࡴࠪࡢ࠭ࡢࡳࠬࠫࡂࠬࠬ⑄") + bstack1ll1l11_opy_ (u"ࠪࢀࠬ⑅").join(bstack1lll1ll1ll1l_opy_) + bstack1ll1l11_opy_ (u"ࠫ࠮࠴ࠪࠥࠩ⑆"),
        bstack1ll1l11_opy_ (u"ࡷ࠭࡜࠳࠼ࠣ࡟ࡗࡋࡄࡂࡅࡗࡉࡉࡣࠧ⑇"),
        bstack1lll1l1l1lll_opy_, flags=re.M | re.I
      )
    def bstack1lll1lll1111_opy_(dic):
      bstack1lll1lll11ll_opy_ = {}
      for key, value in dic.items():
        if key in bstack1lll1ll1ll1l_opy_:
          bstack1lll1lll11ll_opy_[key] = bstack1ll1l11_opy_ (u"࡛࠭ࡓࡇࡇࡅࡈ࡚ࡅࡅ࡟ࠪ⑈")
        else:
          if isinstance(value, dict):
            bstack1lll1lll11ll_opy_[key] = bstack1lll1lll1111_opy_(value)
          else:
            bstack1lll1lll11ll_opy_[key] = value
      return bstack1lll1lll11ll_opy_
    bstack1lll1lll11ll_opy_ = bstack1lll1lll1111_opy_(config)
    return {
      bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪ⑉"): bstack1lll1l1l1lll_opy_,
      bstack1ll1l11_opy_ (u"ࠨࡨ࡬ࡲࡦࡲࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫ⑊"): json.dumps(bstack1lll1lll11ll_opy_)
    }
  except Exception as e:
    return {}
def bstack1lll1l1ll1ll_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack1ll1l11_opy_ (u"ࠩ࡯ࡳ࡬࠭⑋"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack1ll1l11ll11_opy_ = os.path.join(log_dir, bstack1ll1l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶࠫ⑌"))
  if not os.path.exists(bstack1ll1l11ll11_opy_):
    bstack1lll1l1lll1l_opy_ = {
      bstack1ll1l11_opy_ (u"ࠦ࡮ࡴࡩࡱࡣࡷ࡬ࠧ⑍"): str(inipath),
      bstack1ll1l11_opy_ (u"ࠧࡸ࡯ࡰࡶࡳࡥࡹ࡮ࠢ⑎"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack1ll1l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡣࡰࡰࡩ࡭࡬ࡹ࠮࡫ࡵࡲࡲࠬ⑏")), bstack1ll1l11_opy_ (u"ࠧࡸࠩ⑐")) as bstack1lll1ll11lll_opy_:
      bstack1lll1ll11lll_opy_.write(json.dumps(bstack1lll1l1lll1l_opy_))
def bstack1lll1lll11l1_opy_():
  try:
    bstack1ll1l11ll11_opy_ = os.path.join(os.getcwd(), bstack1ll1l11_opy_ (u"ࠨ࡮ࡲ࡫ࠬ⑑"), bstack1ll1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡦࡳࡳ࡬ࡩࡨࡵ࠱࡮ࡸࡵ࡮ࠨ⑒"))
    if os.path.exists(bstack1ll1l11ll11_opy_):
      with open(bstack1ll1l11ll11_opy_, bstack1ll1l11_opy_ (u"ࠪࡶࠬ⑓")) as bstack1lll1ll11lll_opy_:
        bstack1lll1l1lll11_opy_ = json.load(bstack1lll1ll11lll_opy_)
      return bstack1lll1l1lll11_opy_.get(bstack1ll1l11_opy_ (u"ࠫ࡮ࡴࡩࡱࡣࡷ࡬ࠬ⑔"), bstack1ll1l11_opy_ (u"ࠬ࠭⑕")), bstack1lll1l1lll11_opy_.get(bstack1ll1l11_opy_ (u"࠭ࡲࡰࡱࡷࡴࡦࡺࡨࠨ⑖"), bstack1ll1l11_opy_ (u"ࠧࠨ⑗"))
  except:
    pass
  return None, None
def bstack1lll1l1lllll_opy_():
  try:
    bstack1ll1l11ll11_opy_ = os.path.join(os.getcwd(), bstack1ll1l11_opy_ (u"ࠨ࡮ࡲ࡫ࠬ⑘"), bstack1ll1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡦࡳࡳ࡬ࡩࡨࡵ࠱࡮ࡸࡵ࡮ࠨ⑙"))
    if os.path.exists(bstack1ll1l11ll11_opy_):
      os.remove(bstack1ll1l11ll11_opy_)
  except:
    pass
def bstack1l11ll11l_opy_(config):
  try:
    try:
      from bstack_utils.bstack1111llll1l_opy_ import bstack11l1111l1l_opy_
    except Exception:
      bstack11l1111l1l_opy_ = None
    start_time = time.time()
    from bstack_utils.helper import global_config, bstack1l111l1ll1_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack1lll1ll11111_opy_
    if config.get(bstack1ll1l11_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬ⑚"), False):
      return
    uuid = os.getenv(bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ⑛")) if os.getenv(bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ⑜")) else global_config.get_property(bstack1ll1l11_opy_ (u"ࠨࡳࡥ࡭ࡕࡹࡳࡏࡤࠣ⑝"))
    if not uuid or uuid == bstack1ll1l11_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ⑞"):
      return
    bstack1lll1lll111l_opy_ = bstack11l1111l1l_opy_.bstack1l11llll1_opy_(EVENTS.bstack11111ll1lll_opy_.value) if bstack11l1111l1l_opy_ else None
    bstack1lll1ll1l1ll_opy_ = [bstack1ll1l11_opy_ (u"ࠨࡴࡨࡵࡺ࡯ࡲࡦ࡯ࡨࡲࡹࡹ࠮ࡵࡺࡷࠫ⑟"), bstack1ll1l11_opy_ (u"ࠩࡓ࡭ࡵ࡬ࡩ࡭ࡧࠪ①"), bstack1ll1l11_opy_ (u"ࠪࡴࡾࡶࡲࡰ࡬ࡨࡧࡹ࠴ࡴࡰ࡯࡯ࠫ②"), bstack1lll1ll11111_opy_, bstack1lll1ll1ll11_opy_]
    bstack1lll1ll11l11_opy_, root_path = bstack1lll1lll11l1_opy_()
    if bstack1lll1ll11l11_opy_ != None:
      bstack1lll1ll1l1ll_opy_.append(bstack1lll1ll11l11_opy_)
    if root_path != None:
      bstack1lll1ll1l1ll_opy_.append(os.path.join(root_path, bstack1ll1l11_opy_ (u"ࠫࡨࡵ࡮ࡧࡶࡨࡷࡹ࠴ࡰࡺࠩ③")))
    bstack1lll1ll1l1l1_opy_ = os.path.join(os.getcwd(), bstack1ll1l11_opy_ (u"ࠬࡲ࡯ࡨࠩ④"), bstack1ll1l11_opy_ (u"࠭࡫ࡦࡻ࠰ࡱࡪࡺࡲࡪࡥࡶ࠲࡯ࡹ࡯࡯ࠩ⑤"))
    if os.path.exists(bstack1lll1ll1l1l1_opy_):
      bstack1lll1ll1l1ll_opy_.append(bstack1lll1ll1l1l1_opy_)
    output_file = os.path.join(tempfile.gettempdir(), bstack1ll1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠭࡭ࡱࡪࡷ࠲࠭⑥") + uuid + bstack1ll1l11_opy_ (u"ࠨ࠰ࡷࡥࡷ࠴ࡧࡻࠩ⑦"))
    with tarfile.open(output_file, bstack1ll1l11_opy_ (u"ࠤࡺ࠾࡬ࢀࠢ⑧")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1lll1ll1l1ll_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1lll1ll1lll1_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1lll1l1llll1_opy_ = data.encode()
        tarinfo.size = len(bstack1lll1l1llll1_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1lll1l1llll1_opy_))
    multipart_data = MultipartEncoder(
      fields= {
        bstack1ll1l11_opy_ (u"ࠪࡨࡦࡺࡡࠨ⑨"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1ll1l11_opy_ (u"ࠫࡷࡨࠧ⑩")), bstack1ll1l11_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲ࡼ࠲࡭ࡺࡪࡲࠪ⑪")),
        bstack1ll1l11_opy_ (u"࠭ࡣ࡭࡫ࡨࡲࡹࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ⑫"): uuid
      }
    )
    bstack1lll1ll1111l_opy_ = bstack1l111l1ll1_opy_(cli.config, [bstack1ll1l11_opy_ (u"ࠢࡢࡲ࡬ࡷࠧ⑬"), bstack1ll1l11_opy_ (u"ࠣࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠣ⑭"), bstack1ll1l11_opy_ (u"ࠤࡸࡴࡱࡵࡡࡥࠤ⑮")], bstack11111l1l111_opy_)
    response = requests.post(
      bstack1ll1l11_opy_ (u"ࠥࡿࢂ࠵ࡣ࡭࡫ࡨࡲࡹ࠳࡬ࡰࡩࡶ࠳ࡺࡶ࡬ࡰࡣࡧࠦ⑯").format(bstack1lll1ll1111l_opy_),
      data=multipart_data,
      headers={bstack1ll1l11_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪ⑰"): multipart_data.content_type},
      auth=(config[bstack1ll1l11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ⑱")], config[bstack1ll1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ⑲")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1ll1l11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡵࡱ࡮ࡲࡥࡩࠦ࡬ࡰࡩࡶ࠾ࠥ࠭⑳") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1ll1l11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡧࡱࡨ࡮ࡴࡧࠡ࡮ࡲ࡫ࡸࡀࠧ⑴") + str(e))
  finally:
    try:
      bstack11lll11ll1l_opy_()
      bstack1lll1l1lllll_opy_()
    except:
      pass
    if bstack11l1111l1l_opy_ and bstack1lll1lll111l_opy_:
      bstack11l1111l1l_opy_.end(EVENTS.bstack11111ll1lll_opy_.value, bstack1lll1lll111l_opy_ + bstack1ll1l11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ⑵"), bstack1lll1lll111l_opy_ + bstack1ll1l11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ⑶"), status=True, failure=None, test_name=None)
    try:
      elapsed = time.time() - start_time
      get_logger().debug(bstack1ll1l11_opy_ (u"ࠦࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡹࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࡦࠣ࡭ࡳࠦࡻ࠻࠰࠶ࡪࢂࠦࡳࡦࡥࡲࡲࡩࡹࠢ⑷").format(elapsed))
    except Exception:
      pass