# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
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
from bstack_utils.constants import bstack111111l1l1l_opy_, EVENTS, bstack11111l11lll_opy_, bstack111111ll11l_opy_, STAGE
import tempfile
import json
bstack1lll1l1l1l11_opy_ = os.getenv(bstack1ll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡍ࡟ࡇࡋࡏࡉࠧ␪"), None) or os.path.join(tempfile.gettempdir(), bstack1ll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡩ࡫ࡢࡶࡩ࠱ࡰࡴ࡭ࠢ␫"))
bstack1lll1ll1l11l_opy_ = os.path.join(bstack1ll_opy_ (u"ࠨ࡬ࡰࡩࠥ␬"), bstack1ll_opy_ (u"ࠧࡴࡦ࡮࠱ࡨࡲࡩ࠮ࡦࡨࡦࡺ࡭࠮࡭ࡱࡪࠫ␭"))
_1lll1ll11l1l_opy_ = threading.Lock()
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1ll_opy_ (u"ࠨࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲ࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫ␮"),
      datefmt=bstack1ll_opy_ (u"ࠩࠨ࡝࠲ࠫ࡭࠮ࠧࡧࡘࠪࡎ࠺ࠦࡏ࠽ࠩࡘࡠࠧ␯"),
      stream=sys.stdout
    )
  return logger
def get_automation_logger(name=__name__, level=logging.DEBUG):
  bstack1ll_opy_ (u"ࠥࠦࠧࠐࠠࠡࡔࡨࡸࡺࡸ࡮ࡴࠢࡤࠤࡱࡵࡧࡨࡧࡵࠤࡹ࡮ࡡࡵࠢࡺࡶ࡮ࡺࡥࡴࠢࡲࡲࡱࡿࠠࡵࡱࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠮࡭ࡱࡪࠤ࡫࡯࡬ࡦࠌࠣࠤࡈࡸࡥࡢࡶࡨࡷࠥࡧ࡮ࡥࠢࡰࡥࡳࡧࡧࡦࡵࠣ࡭ࡹࡹࠠࡰࡹࡱࠤࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡨ࡬ࡰࡪࠦࡨࡢࡰࡧࡰࡪࡸࠊࠡࠢࡒࡲࡱࡿࠠࡦࡰࡤࡦࡱ࡫ࡳࠡ࡮ࡲ࡫࡬࡯࡮ࡨࠢ࡬ࡪࠥࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࡠࡎࡒࡋࡘࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷࠤࡻࡧࡲࡪࡣࡥࡰࡪࠦࡩࡴࠢࡶࡩࡹࠦࡴࡰࠢࡤࠤࡹࡸࡵࡵࡪࡼࠤࡻࡧ࡬ࡶࡧࠍࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࡰࡤࡱࡪࡀࠠࡍࡱࡪ࡫ࡪࡸࠠ࡯ࡣࡰࡩࠥ࠮ࡤࡦࡨࡤࡹࡱࡺࡳࠡࡶࡲࠤࡤࡥ࡮ࡢ࡯ࡨࡣࡤ࠯ࠊࠡࠢࠣࠤࡱ࡫ࡶࡦ࡮࠽ࠤࡑࡵࡧࡨ࡫ࡱ࡫ࠥࡲࡥࡷࡧ࡯ࠤ࠭ࡪࡥࡧࡣࡸࡰࡹࡹࠠࡵࡱࠣࡈࡊࡈࡕࡈࠫࠍࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࡱࡵࡧࡨ࡫ࡱ࡫࠳ࡒ࡯ࡨࡩࡨࡶ࠿ࠦࡃࡰࡰࡩ࡭࡬ࡻࡲࡦࡦࠣࡰࡴ࡭ࡧࡦࡴࠣࡸ࡭ࡧࡴࠡࡹࡵ࡭ࡹ࡫ࡳࠡࡱࡱࡰࡾࠦࡴࡰࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠴࡬ࡰࡩࠣࠬ࡮࡬ࠠࡦࡰࡤࡦࡱ࡫ࡤࠪࠌࠣࠤࠧࠨࠢ␰")
  logger_name = bstack1ll_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠯ࡽ࠳ࢁࠧ␱").format(name)
  logger = logging.getLogger(logger_name)
  is_enabled = os.getenv(bstack1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࡠࡎࡒࡋࡘ࠭␲"), bstack1ll_opy_ (u"࠭ࠧ␳")).lower() == bstack1ll_opy_ (u"ࠧࡵࡴࡸࡩࠬ␴")
  if not is_enabled:
    logger.setLevel(logging.CRITICAL)
    logger.propagate = False
    return logger
  with _1lll1ll11l1l_opy_:
    if logger.handlers:
      return logger
    bstack1lll1l1ll1ll_opy_ = os.path.join(os.getcwd(), bstack1ll_opy_ (u"ࠨ࡮ࡲ࡫ࠬ␵"), bstack1ll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠴࡬ࡰࡩࠪ␶"))
    log_dir = os.path.dirname(bstack1lll1l1ll1ll_opy_)
    if not os.path.exists(log_dir):
      os.makedirs(log_dir)
    bstack1lll1l1l1ll1_opy_ = logging.FileHandler(bstack1lll1l1ll1ll_opy_)
    bstack1lll1ll1l111_opy_ = logging.Formatter(
      fmt=bstack1ll_opy_ (u"ࠪࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡ࡝ࠣࡗࡉࡑ࠭ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠤࡢࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫ␷"),
      datefmt=bstack1ll_opy_ (u"ࠫࠪ࡟࠭ࠦ࡯࠰ࠩࡩ࡚ࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࡛ࠩ␸"),
    )
    bstack1lll1l1l1ll1_opy_.setFormatter(bstack1lll1ll1l111_opy_)
    bstack1lll1l1l1ll1_opy_.setLevel(level)
    bstack1lll1l1l1ll1_opy_.addFilter(lambda r: r.name != bstack1ll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡶࡪࡳ࡯ࡵࡧ࠱ࡶࡪࡳ࡯ࡵࡧࡢࡧࡴࡴ࡮ࡦࡥࡷ࡭ࡴࡴࠧ␹"))
    logger.addHandler(bstack1lll1l1l1ll1_opy_)
    logger.setLevel(level)
    logger.propagate = False
  return logger
def get_log_level():
  bstack1lll1l1ll111_opy_ = os.environ.get(bstack1ll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡃࡕ࡝ࡤࡊࡅࡃࡗࡊࠦ␺"), bstack1ll_opy_ (u"ࠢࡧࡣ࡯ࡷࡪࠨ␻"))
  return logging.DEBUG if bstack1lll1l1ll111_opy_.lower() == bstack1ll_opy_ (u"ࠣࡶࡵࡹࡪࠨ␼") else logging.INFO
def bstack11ll1l1lll1_opy_():
  global bstack1lll1l1l1l11_opy_
  if os.path.exists(bstack1lll1l1l1l11_opy_):
    os.remove(bstack1lll1l1l1l11_opy_)
  if os.path.exists(bstack1lll1ll1l11l_opy_):
    os.remove(bstack1lll1ll1l11l_opy_)
def bstack11ll1lll1_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def configure_logger(config, log_level):
  bstack1lll1ll1l1ll_opy_ = log_level
  if bstack1ll_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫ␽") in config and config[bstack1ll_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬ␾")] in bstack11111l11lll_opy_:
    bstack1lll1ll1l1ll_opy_ = bstack11111l11lll_opy_[config[bstack1ll_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭␿")]]
  if config.get(bstack1ll_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧ⑀"), False):
    logging.getLogger().setLevel(bstack1lll1ll1l1ll_opy_)
    return bstack1lll1ll1l1ll_opy_
  global bstack1lll1l1l1l11_opy_
  bstack11ll1lll1_opy_()
  bstack1lll1ll11111_opy_ = logging.Formatter(
    fmt=bstack1ll_opy_ (u"࠭ࠥࠩࡣࡶࡧࡹ࡯࡭ࡦࠫࡶࠤࡠࠫࠨ࡯ࡣࡰࡩ࠮ࡹ࡝࡜ࠧࠫࡰࡪࡼࡥ࡭ࡰࡤࡱࡪ࠯ࡳ࡞ࠢ࠰ࠤࠪ࠮࡭ࡦࡵࡶࡥ࡬࡫ࠩࡴࠩ⑁"),
    datefmt=bstack1ll_opy_ (u"࡛ࠧࠦ࠰ࠩࡲ࠳ࠥࡥࡖࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࡞ࠬ⑂"),
  )
  bstack1lll1l1lll1l_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1lll1l1l1l11_opy_)
  file_handler.setFormatter(bstack1lll1ll11111_opy_)
  bstack1lll1l1lll1l_opy_.setFormatter(bstack1lll1ll11111_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1lll1l1lll1l_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1ll_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷ࠴ࡲࡦ࡯ࡲࡸࡪ࠴ࡲࡦ࡯ࡲࡸࡪࡥࡣࡰࡰࡱࡩࡨࡺࡩࡰࡰࠪ⑃"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1lll1l1lll1l_opy_.setLevel(bstack1lll1ll1l1ll_opy_)
  logging.getLogger().addHandler(bstack1lll1l1lll1l_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1lll1ll1l1ll_opy_
def bstack1lll1ll1111l_opy_(config):
  try:
    bstack1lll1ll1ll1l_opy_ = set(bstack111111ll11l_opy_)
    bstack1lll1l1lll11_opy_ = bstack1ll_opy_ (u"ࠩࠪ⑄")
    with open(bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭⑅")) as bstack1lll1l1l11l1_opy_:
      bstack1lll1ll11lll_opy_ = bstack1lll1l1l11l1_opy_.read()
      bstack1lll1l1lll11_opy_ = re.sub(bstack1ll_opy_ (u"ࡶࠬࡤࠨ࡝ࡵ࠮࠭ࡄࠩ࠮ࠫࠦ࡟ࡲࠬ⑆"), bstack1ll_opy_ (u"ࠬ࠭⑇"), bstack1lll1ll11lll_opy_, flags=re.M)
      bstack1lll1l1lll11_opy_ = re.sub(
        bstack1ll_opy_ (u"ࡸࠧ࡟ࠪ࡟ࡷ࠰࠯࠿ࠩࠩ⑈") + bstack1ll_opy_ (u"ࠧࡽࠩ⑉").join(bstack1lll1ll1ll1l_opy_) + bstack1ll_opy_ (u"ࠨࠫ࠱࠮ࠩ࠭⑊"),
        bstack1ll_opy_ (u"ࡴࠪࡠ࠷ࡀࠠ࡜ࡔࡈࡈࡆࡉࡔࡆࡆࡠࠫ⑋"),
        bstack1lll1l1lll11_opy_, flags=re.M | re.I
      )
    def bstack1lll1l1l1lll_opy_(dic):
      bstack1lll1l1l111l_opy_ = {}
      for key, value in dic.items():
        if key in bstack1lll1ll1ll1l_opy_:
          bstack1lll1l1l111l_opy_[key] = bstack1ll_opy_ (u"ࠪ࡟ࡗࡋࡄࡂࡅࡗࡉࡉࡣࠧ⑌")
        else:
          if isinstance(value, dict):
            bstack1lll1l1l111l_opy_[key] = bstack1lll1l1l1lll_opy_(value)
          else:
            bstack1lll1l1l111l_opy_[key] = value
      return bstack1lll1l1l111l_opy_
    bstack1lll1l1l111l_opy_ = bstack1lll1l1l1lll_opy_(config)
    return {
      bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧ⑍"): bstack1lll1l1lll11_opy_,
      bstack1ll_opy_ (u"ࠬ࡬ࡩ࡯ࡣ࡯ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨ⑎"): json.dumps(bstack1lll1l1l111l_opy_)
    }
  except Exception as e:
    return {}
def bstack1lll1ll1ll11_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack1ll_opy_ (u"࠭࡬ࡰࡩࠪ⑏"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack1ll1l11lll1_opy_ = os.path.join(log_dir, bstack1ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡤࡱࡱࡪ࡮࡭ࡳࠨ⑐"))
  if not os.path.exists(bstack1ll1l11lll1_opy_):
    bstack1lll1l1l1l1l_opy_ = {
      bstack1ll_opy_ (u"ࠣ࡫ࡱ࡭ࡵࡧࡴࡩࠤ⑑"): str(inipath),
      bstack1ll_opy_ (u"ࠤࡵࡳࡴࡺࡰࡢࡶ࡫ࠦ⑒"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack1ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶ࠲࡯ࡹ࡯࡯ࠩ⑓")), bstack1ll_opy_ (u"ࠫࡼ࠭⑔")) as bstack1lll1l1lllll_opy_:
      bstack1lll1l1lllll_opy_.write(json.dumps(bstack1lll1l1l1l1l_opy_))
def bstack1lll1l1llll1_opy_():
  try:
    bstack1ll1l11lll1_opy_ = os.path.join(os.getcwd(), bstack1ll_opy_ (u"ࠬࡲ࡯ࡨࠩ⑕"), bstack1ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡣࡰࡰࡩ࡭࡬ࡹ࠮࡫ࡵࡲࡲࠬ⑖"))
    if os.path.exists(bstack1ll1l11lll1_opy_):
      with open(bstack1ll1l11lll1_opy_, bstack1ll_opy_ (u"ࠧࡳࠩ⑗")) as bstack1lll1l1lllll_opy_:
        bstack1lll1ll11ll1_opy_ = json.load(bstack1lll1l1lllll_opy_)
      return bstack1lll1ll11ll1_opy_.get(bstack1ll_opy_ (u"ࠨ࡫ࡱ࡭ࡵࡧࡴࡩࠩ⑘"), bstack1ll_opy_ (u"ࠩࠪ⑙")), bstack1lll1ll11ll1_opy_.get(bstack1ll_opy_ (u"ࠪࡶࡴࡵࡴࡱࡣࡷ࡬ࠬ⑚"), bstack1ll_opy_ (u"ࠫࠬ⑛"))
  except:
    pass
  return None, None
def bstack1lll1ll1l1l1_opy_():
  try:
    bstack1ll1l11lll1_opy_ = os.path.join(os.getcwd(), bstack1ll_opy_ (u"ࠬࡲ࡯ࡨࠩ⑜"), bstack1ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡣࡰࡰࡩ࡭࡬ࡹ࠮࡫ࡵࡲࡲࠬ⑝"))
    if os.path.exists(bstack1ll1l11lll1_opy_):
      os.remove(bstack1ll1l11lll1_opy_)
  except:
    pass
def bstack111l11l1_opy_(config):
  try:
    try:
      from bstack_utils.bstack1l11ll1lll_opy_ import bstack1l11l1ll11_opy_
    except Exception:
      bstack1l11l1ll11_opy_ = None
    start_time = time.time()
    from bstack_utils.helper import global_config, bstack11lll111ll_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack1lll1l1l1l11_opy_
    if config.get(bstack1ll_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡷࡷࡳࡈࡧࡰࡵࡷࡵࡩࡑࡵࡧࡴࠩ⑞"), False):
      return
    uuid = os.getenv(bstack1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭⑟")) if os.getenv(bstack1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ①")) else global_config.get_property(bstack1ll_opy_ (u"ࠥࡷࡩࡱࡒࡶࡰࡌࡨࠧ②"))
    if not uuid or uuid == bstack1ll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ③"):
      return
    bstack1lll1l1l11ll_opy_ = bstack1l11l1ll11_opy_.bstack1111ll1111_opy_(EVENTS.bstack1111111lll1_opy_.value) if bstack1l11l1ll11_opy_ else None
    bstack1lll1l1ll11l_opy_ = [bstack1ll_opy_ (u"ࠬࡸࡥࡲࡷ࡬ࡶࡪࡳࡥ࡯ࡶࡶ࠲ࡹࡾࡴࠨ④"), bstack1ll_opy_ (u"࠭ࡐࡪࡲࡩ࡭ࡱ࡫ࠧ⑤"), bstack1ll_opy_ (u"ࠧࡱࡻࡳࡶࡴࡰࡥࡤࡶ࠱ࡸࡴࡳ࡬ࠨ⑥"), bstack1lll1l1l1l11_opy_, bstack1lll1ll1l11l_opy_]
    bstack1lll1ll11l11_opy_, root_path = bstack1lll1l1llll1_opy_()
    if bstack1lll1ll11l11_opy_ != None:
      bstack1lll1l1ll11l_opy_.append(bstack1lll1ll11l11_opy_)
    if root_path != None:
      bstack1lll1l1ll11l_opy_.append(os.path.join(root_path, bstack1ll_opy_ (u"ࠨࡥࡲࡲ࡫ࡺࡥࡴࡶ࠱ࡴࡾ࠭⑦")))
    bstack1lll1l1ll1l1_opy_ = os.path.join(os.getcwd(), bstack1ll_opy_ (u"ࠩ࡯ࡳ࡬࠭⑧"), bstack1ll_opy_ (u"ࠪ࡯ࡪࡿ࠭࡮ࡧࡷࡶ࡮ࡩࡳ࠯࡬ࡶࡳࡳ࠭⑨"))
    if os.path.exists(bstack1lll1l1ll1l1_opy_):
      bstack1lll1l1ll11l_opy_.append(bstack1lll1l1ll1l1_opy_)
    output_file = os.path.join(tempfile.gettempdir(), bstack1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠱ࡱࡵࡧࡴ࠯ࠪ⑩") + uuid + bstack1ll_opy_ (u"ࠬ࠴ࡴࡢࡴ࠱࡫ࡿ࠭⑪"))
    with tarfile.open(output_file, bstack1ll_opy_ (u"ࠨࡷ࠻ࡩࡽࠦ⑫")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1lll1l1ll11l_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1lll1ll1111l_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1lll1ll111ll_opy_ = data.encode()
        tarinfo.size = len(bstack1lll1ll111ll_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1lll1ll111ll_opy_))
    multipart_data = MultipartEncoder(
      fields= {
        bstack1ll_opy_ (u"ࠧࡥࡣࡷࡥࠬ⑬"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1ll_opy_ (u"ࠨࡴࡥࠫ⑭")), bstack1ll_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯ࡹ࠯ࡪࡾ࡮ࡶࠧ⑮")),
        bstack1ll_opy_ (u"ࠪࡧࡱ࡯ࡥ࡯ࡶࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬ⑯"): uuid
      }
    )
    bstack1lll1ll111l1_opy_ = bstack11lll111ll_opy_(cli.config, [bstack1ll_opy_ (u"ࠦࡦࡶࡩࡴࠤ⑰"), bstack1ll_opy_ (u"ࠧࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠧ⑱"), bstack1ll_opy_ (u"ࠨࡵࡱ࡮ࡲࡥࡩࠨ⑲")], bstack111111l1l1l_opy_)
    response = requests.post(
      bstack1ll_opy_ (u"ࠢࡼࡿ࠲ࡧࡱ࡯ࡥ࡯ࡶ࠰ࡰࡴ࡭ࡳ࠰ࡷࡳࡰࡴࡧࡤࠣ⑳").format(bstack1lll1ll111l1_opy_),
      data=multipart_data,
      headers={bstack1ll_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ⑴"): multipart_data.content_type},
      auth=(config[bstack1ll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ⑵")], config[bstack1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭⑶")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1ll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡹࡵࡲ࡯ࡢࡦࠣࡰࡴ࡭ࡳ࠻ࠢࠪ⑷") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1ll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥࡲ࡯ࡨࡵ࠽ࠫ⑸") + str(e))
  finally:
    try:
      bstack11ll1l1lll1_opy_()
      bstack1lll1ll1l1l1_opy_()
    except:
      pass
    if bstack1l11l1ll11_opy_ and bstack1lll1l1l11ll_opy_:
      bstack1l11l1ll11_opy_.end(EVENTS.bstack1111111lll1_opy_.value, bstack1lll1l1l11ll_opy_ + bstack1ll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ⑹"), bstack1lll1l1l11ll_opy_ + bstack1ll_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ⑺"), status=True, failure=None, test_name=None)
    try:
      elapsed = time.time() - start_time
      get_logger().debug(bstack1ll_opy_ (u"ࠣࡵࡨࡲࡩࡥ࡬ࡰࡩࡶࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࡪࠠࡪࡰࠣࡿ࠿࠴࠳ࡧࡿࠣࡷࡪࡩ࡯࡯ࡦࡶࠦ⑻").format(elapsed))
    except Exception:
      pass