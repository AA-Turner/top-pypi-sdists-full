# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
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
from bstack_utils.constants import bstack11111l11l1l_opy_, EVENTS, bstack11111lll11l_opy_, bstack11111l11lll_opy_, STAGE
import tempfile
import json
bstack1lll1l1ll1l1_opy_ = os.getenv(bstack11ll11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡊࡣࡋࡏࡌࡆࠤ␧"), None) or os.path.join(tempfile.gettempdir(), bstack11ll11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡦࡨࡦࡺ࡭࠮࡭ࡱࡪࠦ␨"))
bstack1lll1l1lll11_opy_ = os.path.join(bstack11ll11_opy_ (u"ࠥࡰࡴ࡭ࠢ␩"), bstack11ll11_opy_ (u"ࠫࡸࡪ࡫࠮ࡥ࡯࡭࠲ࡪࡥࡣࡷࡪ࠲ࡱࡵࡧࠨ␪"))
_1lll1l1llll1_opy_ = threading.Lock()
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack11ll11_opy_ (u"ࠬࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨ␫"),
      datefmt=bstack11ll11_opy_ (u"࡚࠭ࠥ࠯ࠨࡱ࠲ࠫࡤࡕࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࡝ࠫ␬"),
      stream=sys.stdout
    )
  return logger
def get_automation_logger(name=__name__, level=logging.DEBUG):
  bstack11ll11_opy_ (u"ࠢࠣࠤࠍࠤࠥࡘࡥࡵࡷࡵࡲࡸࠦࡡࠡ࡮ࡲ࡫࡬࡫ࡲࠡࡶ࡫ࡥࡹࠦࡷࡳ࡫ࡷࡩࡸࠦ࡯࡯࡮ࡼࠤࡹࡵࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠲ࡱࡵࡧࠡࡨ࡬ࡰࡪࠐࠠࠡࡅࡵࡩࡦࡺࡥࡴࠢࡤࡲࡩࠦ࡭ࡢࡰࡤ࡫ࡪࡹࠠࡪࡶࡶࠤࡴࡽ࡮ࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥ࡬ࡩ࡭ࡧࠣ࡬ࡦࡴࡤ࡭ࡧࡵࠎࠥࠦࡏ࡯࡮ࡼࠤࡪࡴࡡࡣ࡮ࡨࡷࠥࡲ࡯ࡨࡩ࡬ࡲ࡬ࠦࡩࡧࠢࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࡤࡒࡏࡈࡕࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴࠡࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠣ࡭ࡸࠦࡳࡦࡶࠣࡸࡴࠦࡡࠡࡶࡵࡹࡹ࡮ࡹࠡࡸࡤࡰࡺ࡫ࠊࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࡴࡡ࡮ࡧ࠽ࠤࡑࡵࡧࡨࡧࡵࠤࡳࡧ࡭ࡦࠢࠫࡨࡪ࡬ࡡࡶ࡮ࡷࡷࠥࡺ࡯ࠡࡡࡢࡲࡦࡳࡥࡠࡡࠬࠎࠥࠦࠠࠡ࡮ࡨࡺࡪࡲ࠺ࠡࡎࡲ࡫࡬࡯࡮ࡨࠢ࡯ࡩࡻ࡫࡬ࠡࠪࡧࡩ࡫ࡧࡵ࡭ࡶࡶࠤࡹࡵࠠࡅࡇࡅ࡙ࡌ࠯ࠊࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡ࡮ࡲ࡫࡬࡯࡮ࡨ࠰ࡏࡳ࡬࡭ࡥࡳ࠼ࠣࡇࡴࡴࡦࡪࡩࡸࡶࡪࡪࠠ࡭ࡱࡪ࡫ࡪࡸࠠࡵࡪࡤࡸࠥࡽࡲࡪࡶࡨࡷࠥࡵ࡮࡭ࡻࠣࡸࡴࠦࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠱ࡰࡴ࡭ࠠࠩ࡫ࡩࠤࡪࡴࡡࡣ࡮ࡨࡨ࠮ࠐࠠࠡࠤࠥࠦ␭")
  logger_name = bstack11ll11_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠳ࢁ࠰ࡾࠤ␮").format(name)
  logger = logging.getLogger(logger_name)
  is_enabled = os.getenv(bstack11ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࡤࡒࡏࡈࡕࠪ␯"), bstack11ll11_opy_ (u"ࠪࠫ␰")).lower() == bstack11ll11_opy_ (u"ࠫࡹࡸࡵࡦࠩ␱")
  if not is_enabled:
    logger.setLevel(logging.CRITICAL)
    logger.propagate = False
    return logger
  with _1lll1l1llll1_opy_:
    if logger.handlers:
      return logger
    bstack1lll1ll1l11l_opy_ = os.path.join(os.getcwd(), bstack11ll11_opy_ (u"ࠬࡲ࡯ࡨࠩ␲"), bstack11ll11_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠱ࡰࡴ࡭ࠧ␳"))
    log_dir = os.path.dirname(bstack1lll1ll1l11l_opy_)
    if not os.path.exists(log_dir):
      os.makedirs(log_dir)
    bstack1lll1ll1l111_opy_ = logging.FileHandler(bstack1lll1ll1l11l_opy_)
    bstack1lll1lll11l1_opy_ = logging.Formatter(
      fmt=bstack11ll11_opy_ (u"ࠧࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࡡࠠࡔࡆࡎ࠱ࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠡ࡟ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨ␴"),
      datefmt=bstack11ll11_opy_ (u"ࠨࠧ࡜࠱ࠪࡳ࠭ࠦࡦࡗࠩࡍࡀࠥࡎ࠼ࠨࡗ࡟࠭␵"),
    )
    bstack1lll1ll1l111_opy_.setFormatter(bstack1lll1lll11l1_opy_)
    bstack1lll1ll1l111_opy_.setLevel(level)
    bstack1lll1ll1l111_opy_.addFilter(lambda r: r.name != bstack11ll11_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࠮ࡳࡧࡰࡳࡹ࡫࠮ࡳࡧࡰࡳࡹ࡫࡟ࡤࡱࡱࡲࡪࡩࡴࡪࡱࡱࠫ␶"))
    logger.addHandler(bstack1lll1ll1l111_opy_)
    logger.setLevel(level)
    logger.propagate = False
  return logger
def get_log_level():
  bstack1lll1lll111l_opy_ = os.environ.get(bstack11ll11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡇࡉࡇ࡛ࡇࠣ␷"), bstack11ll11_opy_ (u"ࠦ࡫ࡧ࡬ࡴࡧࠥ␸"))
  return logging.DEBUG if bstack1lll1lll111l_opy_.lower() == bstack11ll11_opy_ (u"ࠧࡺࡲࡶࡧࠥ␹") else logging.INFO
def bstack11ll11llll1_opy_():
  global bstack1lll1l1ll1l1_opy_
  if os.path.exists(bstack1lll1l1ll1l1_opy_):
    os.remove(bstack1lll1l1ll1l1_opy_)
  if os.path.exists(bstack1lll1l1lll11_opy_):
    os.remove(bstack1lll1l1lll11_opy_)
def bstack1l1lll111_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def configure_logger(config, log_level):
  bstack1lll1ll1ll11_opy_ = log_level
  if bstack11ll11_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨ␺") in config and config[bstack11ll11_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩ␻")] in bstack11111lll11l_opy_:
    bstack1lll1ll1ll11_opy_ = bstack11111lll11l_opy_[config[bstack11ll11_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪ␼")]]
  if config.get(bstack11ll11_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫ␽"), False):
    logging.getLogger().setLevel(bstack1lll1ll1ll11_opy_)
    return bstack1lll1ll1ll11_opy_
  global bstack1lll1l1ll1l1_opy_
  bstack1l1lll111_opy_()
  bstack1lll1ll11ll1_opy_ = logging.Formatter(
    fmt=bstack11ll11_opy_ (u"ࠪࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭␾"),
    datefmt=bstack11ll11_opy_ (u"ࠫࠪ࡟࠭ࠦ࡯࠰ࠩࡩ࡚ࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࡛ࠩ␿"),
  )
  bstack1lll1ll1l1ll_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1lll1l1ll1l1_opy_)
  file_handler.setFormatter(bstack1lll1ll11ll1_opy_)
  bstack1lll1ll1l1ll_opy_.setFormatter(bstack1lll1ll11ll1_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1lll1ll1l1ll_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack11ll11_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡶࡪࡳ࡯ࡵࡧ࠱ࡶࡪࡳ࡯ࡵࡧࡢࡧࡴࡴ࡮ࡦࡥࡷ࡭ࡴࡴࠧ⑀"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1lll1ll1l1ll_opy_.setLevel(bstack1lll1ll1ll11_opy_)
  logging.getLogger().addHandler(bstack1lll1ll1l1ll_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1lll1ll1ll11_opy_
def bstack1lll1ll1111l_opy_(config):
  try:
    bstack1lll1l1l1lll_opy_ = set(bstack11111l11lll_opy_)
    bstack1lll1ll111ll_opy_ = bstack11ll11_opy_ (u"࠭ࠧ⑁")
    with open(bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪ⑂")) as bstack1lll1ll1ll1l_opy_:
      bstack1lll1l1ll11l_opy_ = bstack1lll1ll1ll1l_opy_.read()
      bstack1lll1ll111ll_opy_ = re.sub(bstack11ll11_opy_ (u"ࡳࠩࡡࠬࡡࡹࠫࠪࡁࠦ࠲࠯ࠪ࡜࡯ࠩ⑃"), bstack11ll11_opy_ (u"ࠩࠪ⑄"), bstack1lll1l1ll11l_opy_, flags=re.M)
      bstack1lll1ll111ll_opy_ = re.sub(
        bstack11ll11_opy_ (u"ࡵࠫࡣ࠮࡜ࡴ࠭ࠬࡃ࠭࠭⑅") + bstack11ll11_opy_ (u"ࠫࢁ࠭⑆").join(bstack1lll1l1l1lll_opy_) + bstack11ll11_opy_ (u"ࠬ࠯࠮ࠫࠦࠪ⑇"),
        bstack11ll11_opy_ (u"ࡸࠧ࡝࠴࠽ࠤࡠࡘࡅࡅࡃࡆࡘࡊࡊ࡝ࠨ⑈"),
        bstack1lll1ll111ll_opy_, flags=re.M | re.I
      )
    def bstack1lll1l1lll1l_opy_(dic):
      bstack1lll1ll1lll1_opy_ = {}
      for key, value in dic.items():
        if key in bstack1lll1l1l1lll_opy_:
          bstack1lll1ll1lll1_opy_[key] = bstack11ll11_opy_ (u"ࠧ࡜ࡔࡈࡈࡆࡉࡔࡆࡆࡠࠫ⑉")
        else:
          if isinstance(value, dict):
            bstack1lll1ll1lll1_opy_[key] = bstack1lll1l1lll1l_opy_(value)
          else:
            bstack1lll1ll1lll1_opy_[key] = value
      return bstack1lll1ll1lll1_opy_
    bstack1lll1ll1lll1_opy_ = bstack1lll1l1lll1l_opy_(config)
    return {
      bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫ⑊"): bstack1lll1ll111ll_opy_,
      bstack11ll11_opy_ (u"ࠩࡩ࡭ࡳࡧ࡬ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬ⑋"): json.dumps(bstack1lll1ll1lll1_opy_)
    }
  except Exception as e:
    return {}
def bstack1lll1ll1llll_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack11ll11_opy_ (u"ࠪࡰࡴ࡭ࠧ⑌"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack1ll1l11l11l_opy_ = os.path.join(log_dir, bstack11ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷࠬ⑍"))
  if not os.path.exists(bstack1ll1l11l11l_opy_):
    bstack1lll1ll11111_opy_ = {
      bstack11ll11_opy_ (u"ࠧ࡯࡮ࡪࡲࡤࡸ࡭ࠨ⑎"): str(inipath),
      bstack11ll11_opy_ (u"ࠨࡲࡰࡱࡷࡴࡦࡺࡨࠣ⑏"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack11ll11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡤࡱࡱࡪ࡮࡭ࡳ࠯࡬ࡶࡳࡳ࠭⑐")), bstack11ll11_opy_ (u"ࠨࡹࠪ⑑")) as bstack1lll1l1ll111_opy_:
      bstack1lll1l1ll111_opy_.write(json.dumps(bstack1lll1ll11111_opy_))
def bstack1lll1l1lllll_opy_():
  try:
    bstack1ll1l11l11l_opy_ = os.path.join(os.getcwd(), bstack11ll11_opy_ (u"ࠩ࡯ࡳ࡬࠭⑒"), bstack11ll11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶ࠲࡯ࡹ࡯࡯ࠩ⑓"))
    if os.path.exists(bstack1ll1l11l11l_opy_):
      with open(bstack1ll1l11l11l_opy_, bstack11ll11_opy_ (u"ࠫࡷ࠭⑔")) as bstack1lll1l1ll111_opy_:
        bstack1lll1lll1111_opy_ = json.load(bstack1lll1l1ll111_opy_)
      return bstack1lll1lll1111_opy_.get(bstack11ll11_opy_ (u"ࠬ࡯࡮ࡪࡲࡤࡸ࡭࠭⑕"), bstack11ll11_opy_ (u"࠭ࠧ⑖")), bstack1lll1lll1111_opy_.get(bstack11ll11_opy_ (u"ࠧࡳࡱࡲࡸࡵࡧࡴࡩࠩ⑗"), bstack11ll11_opy_ (u"ࠨࠩ⑘"))
  except:
    pass
  return None, None
def bstack1lll1ll11l1l_opy_():
  try:
    bstack1ll1l11l11l_opy_ = os.path.join(os.getcwd(), bstack11ll11_opy_ (u"ࠩ࡯ࡳ࡬࠭⑙"), bstack11ll11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶ࠲࡯ࡹ࡯࡯ࠩ⑚"))
    if os.path.exists(bstack1ll1l11l11l_opy_):
      os.remove(bstack1ll1l11l11l_opy_)
  except:
    pass
def bstack111ll1lll1_opy_(config):
  try:
    try:
      from bstack_utils.bstack1l11l1l11_opy_ import bstack1ll111lll_opy_
    except Exception:
      bstack1ll111lll_opy_ = None
    start_time = time.time()
    from bstack_utils.helper import global_config, bstack11lll1lll_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack1lll1l1ll1l1_opy_
    if config.get(bstack11ll11_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭⑛"), False):
      return
    uuid = os.getenv(bstack11ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ⑜")) if os.getenv(bstack11ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ⑝")) else global_config.get_property(bstack11ll11_opy_ (u"ࠢࡴࡦ࡮ࡖࡺࡴࡉࡥࠤ⑞"))
    if not uuid or uuid == bstack11ll11_opy_ (u"ࠨࡰࡸࡰࡱ࠭⑟"):
      return
    bstack1lll1ll11lll_opy_ = bstack1ll111lll_opy_.bstack1ll11l11_opy_(EVENTS.bstack111111ll111_opy_.value) if bstack1ll111lll_opy_ else None
    bstack1lll1ll1l1l1_opy_ = [bstack11ll11_opy_ (u"ࠩࡵࡩࡶࡻࡩࡳࡧࡰࡩࡳࡺࡳ࠯ࡶࡻࡸࠬ①"), bstack11ll11_opy_ (u"ࠪࡔ࡮ࡶࡦࡪ࡮ࡨࠫ②"), bstack11ll11_opy_ (u"ࠫࡵࡿࡰࡳࡱ࡭ࡩࡨࡺ࠮ࡵࡱࡰࡰࠬ③"), bstack1lll1l1ll1l1_opy_, bstack1lll1l1lll11_opy_]
    bstack1lll1ll11l11_opy_, root_path = bstack1lll1l1lllll_opy_()
    if bstack1lll1ll11l11_opy_ != None:
      bstack1lll1ll1l1l1_opy_.append(bstack1lll1ll11l11_opy_)
    if root_path != None:
      bstack1lll1ll1l1l1_opy_.append(os.path.join(root_path, bstack11ll11_opy_ (u"ࠬࡩ࡯࡯ࡨࡷࡩࡸࡺ࠮ࡱࡻࠪ④")))
    bstack1lll1ll111l1_opy_ = os.path.join(os.getcwd(), bstack11ll11_opy_ (u"࠭࡬ࡰࡩࠪ⑤"), bstack11ll11_opy_ (u"ࠧ࡬ࡧࡼ࠱ࡲ࡫ࡴࡳ࡫ࡦࡷ࠳ࡰࡳࡰࡰࠪ⑥"))
    if os.path.exists(bstack1lll1ll111l1_opy_):
      bstack1lll1ll1l1l1_opy_.append(bstack1lll1ll111l1_opy_)
    output_file = os.path.join(tempfile.gettempdir(), bstack11ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠮࡮ࡲ࡫ࡸ࠳ࠧ⑦") + uuid + bstack11ll11_opy_ (u"ࠩ࠱ࡸࡦࡸ࠮ࡨࡼࠪ⑧"))
    with tarfile.open(output_file, bstack11ll11_opy_ (u"ࠥࡻ࠿࡭ࡺࠣ⑨")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1lll1ll1l1l1_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1lll1ll1111l_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1lll1l1ll1ll_opy_ = data.encode()
        tarinfo.size = len(bstack1lll1l1ll1ll_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1lll1l1ll1ll_opy_))
    multipart_data = MultipartEncoder(
      fields= {
        bstack11ll11_opy_ (u"ࠫࡩࡧࡴࡢࠩ⑩"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack11ll11_opy_ (u"ࠬࡸࡢࠨ⑪")), bstack11ll11_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳ࡽ࠳ࡧࡻ࡫ࡳࠫ⑫")),
        bstack11ll11_opy_ (u"ࠧࡤ࡮࡬ࡩࡳࡺࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ⑬"): uuid
      }
    )
    bstack1lll1l1l1ll1_opy_ = bstack11lll1lll_opy_(cli.config, [bstack11ll11_opy_ (u"ࠣࡣࡳ࡭ࡸࠨ⑭"), bstack11ll11_opy_ (u"ࠤࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠤ⑮"), bstack11ll11_opy_ (u"ࠥࡹࡵࡲ࡯ࡢࡦࠥ⑯")], bstack11111l11l1l_opy_)
    response = requests.post(
      bstack11ll11_opy_ (u"ࠦࢀࢃ࠯ࡤ࡮࡬ࡩࡳࡺ࠭࡭ࡱࡪࡷ࠴ࡻࡰ࡭ࡱࡤࡨࠧ⑰").format(bstack1lll1l1l1ll1_opy_),
      data=multipart_data,
      headers={bstack11ll11_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ⑱"): multipart_data.content_type},
      auth=(config[bstack11ll11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ⑲")], config[bstack11ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ⑳")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack11ll11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡶࡲ࡯ࡳࡦࡪࠠ࡭ࡱࡪࡷ࠿ࠦࠧ⑴") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack11ll11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡲࡩ࡯࡮ࡨࠢ࡯ࡳ࡬ࡹ࠺ࠨ⑵") + str(e))
  finally:
    try:
      bstack11ll11llll1_opy_()
      bstack1lll1ll11l1l_opy_()
    except:
      pass
    if bstack1ll111lll_opy_ and bstack1lll1ll11lll_opy_:
      bstack1ll111lll_opy_.end(EVENTS.bstack111111ll111_opy_.value, bstack1lll1ll11lll_opy_ + bstack11ll11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ⑶"), bstack1lll1ll11lll_opy_ + bstack11ll11_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ⑷"), status=True, failure=None, test_name=None)
    try:
      elapsed = time.time() - start_time
      get_logger().debug(bstack11ll11_opy_ (u"ࠧࡹࡥ࡯ࡦࡢࡰࡴ࡭ࡳࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠤ࡮ࡴࠠࡼ࠼࠱࠷࡫ࢃࠠࡴࡧࡦࡳࡳࡪࡳࠣ⑸").format(elapsed))
    except Exception:
      pass