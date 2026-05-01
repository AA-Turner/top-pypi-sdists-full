# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
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
from bstack_utils.constants import bstack1111111l1ll_opy_, EVENTS, bstack11111111lll_opy_, bstack111111lll1l_opy_, STAGE
import tempfile
import json
bstack1lll1l11ll11_opy_ = os.getenv(bstack111ll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡈࡡࡉࡍࡑࡋࠢ⒜"), None) or os.path.join(tempfile.gettempdir(), bstack111ll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡤࡦࡤࡸ࡫࠳ࡲ࡯ࡨࠤ⒝"))
bstack1lll1l1lll11_opy_ = os.path.join(bstack111ll_opy_ (u"ࠣ࡮ࡲ࡫ࠧ⒞"), bstack111ll_opy_ (u"ࠩࡶࡨࡰ࠳ࡣ࡭࡫࠰ࡨࡪࡨࡵࡨ࠰࡯ࡳ࡬࠭⒟"))
_1lll1l1llll1_opy_ = threading.Lock()
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack111ll_opy_ (u"ࠪࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭⒠"),
      datefmt=bstack111ll_opy_ (u"ࠫࠪ࡟࠭ࠦ࡯࠰ࠩࡩ࡚ࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࡛ࠩ⒡"),
      stream=sys.stdout
    )
  return logger
def get_automation_logger(name=__name__, level=logging.DEBUG):
  bstack111ll_opy_ (u"ࠧࠨࠢࠋࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡦࠦ࡬ࡰࡩࡪࡩࡷࠦࡴࡩࡣࡷࠤࡼࡸࡩࡵࡧࡶࠤࡴࡴ࡬ࡺࠢࡷࡳࠥࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠰࡯ࡳ࡬ࠦࡦࡪ࡮ࡨࠎࠥࠦࡃࡳࡧࡤࡸࡪࡹࠠࡢࡰࡧࠤࡲࡧ࡮ࡢࡩࡨࡷࠥ࡯ࡴࡴࠢࡲࡻࡳࠦࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡪ࡮ࡲࡥࠡࡪࡤࡲࡩࡲࡥࡳࠌࠣࠤࡔࡴ࡬ࡺࠢࡨࡲࡦࡨ࡬ࡦࡵࠣࡰࡴ࡭ࡧࡪࡰࡪࠤ࡮࡬ࠠࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࡢࡐࡔࡍࡓࠡࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹࠦࡶࡢࡴ࡬ࡥࡧࡲࡥࠡ࡫ࡶࠤࡸ࡫ࡴࠡࡶࡲࠤࡦࠦࡴࡳࡷࡷ࡬ࡾࠦࡶࡢ࡮ࡸࡩࠏࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࡲࡦࡳࡥ࠻ࠢࡏࡳ࡬࡭ࡥࡳࠢࡱࡥࡲ࡫ࠠࠩࡦࡨࡪࡦࡻ࡬ࡵࡵࠣࡸࡴࠦ࡟ࡠࡰࡤࡱࡪࡥ࡟ࠪࠌࠣࠤࠥࠦ࡬ࡦࡸࡨࡰ࠿ࠦࡌࡰࡩࡪ࡭ࡳ࡭ࠠ࡭ࡧࡹࡩࡱࠦࠨࡥࡧࡩࡥࡺࡲࡴࡴࠢࡷࡳࠥࡊࡅࡃࡗࡊ࠭ࠏࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦ࡬ࡰࡩࡪ࡭ࡳ࡭࠮ࡍࡱࡪ࡫ࡪࡸ࠺ࠡࡅࡲࡲ࡫࡯ࡧࡶࡴࡨࡨࠥࡲ࡯ࡨࡩࡨࡶࠥࡺࡨࡢࡶࠣࡻࡷ࡯ࡴࡦࡵࠣࡳࡳࡲࡹࠡࡶࡲࠤࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠯࡮ࡲ࡫ࠥ࠮ࡩࡧࠢࡨࡲࡦࡨ࡬ࡦࡦࠬࠎࠥࠦࠢࠣࠤ⒢")
  logger_name = bstack111ll_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠱ࡿ࠵ࢃࠢ⒣").format(name)
  logger = logging.getLogger(logger_name)
  is_enabled = os.getenv(bstack111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࡢࡐࡔࡍࡓࠨ⒤"), bstack111ll_opy_ (u"ࠨࠩ⒥")).lower() == bstack111ll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ⒦")
  if not is_enabled:
    logger.setLevel(logging.CRITICAL)
    logger.propagate = False
    return logger
  with _1lll1l1llll1_opy_:
    if logger.handlers:
      return logger
    bstack1lll1l1ll1l1_opy_ = os.path.join(os.getcwd(), bstack111ll_opy_ (u"ࠪࡰࡴ࡭ࠧ⒧"), bstack111ll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠯࡮ࡲ࡫ࠬ⒨"))
    log_dir = os.path.dirname(bstack1lll1l1ll1l1_opy_)
    if not os.path.exists(log_dir):
      os.makedirs(log_dir)
    bstack1lll1l1l1ll1_opy_ = logging.FileHandler(bstack1lll1l1ll1l1_opy_)
    bstack1lll1l11lll1_opy_ = logging.Formatter(
      fmt=bstack111ll_opy_ (u"ࠬࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣ࡟࡙ࠥࡄࡌ࠯ࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓࠦ࡝ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭⒩"),
      datefmt=bstack111ll_opy_ (u"࡚࠭ࠥ࠯ࠨࡱ࠲ࠫࡤࡕࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࡝ࠫ⒪"),
    )
    bstack1lll1l1l1ll1_opy_.setFormatter(bstack1lll1l11lll1_opy_)
    bstack1lll1l1l1ll1_opy_.setLevel(level)
    bstack1lll1l1l1ll1_opy_.addFilter(lambda r: r.name != bstack111ll_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࠰ࡺࡩࡧࡪࡲࡪࡸࡨࡶ࠳ࡸࡥ࡮ࡱࡷࡩ࠳ࡸࡥ࡮ࡱࡷࡩࡤࡩ࡯࡯ࡰࡨࡧࡹ࡯࡯࡯ࠩ⒫"))
    logger.addHandler(bstack1lll1l1l1ll1_opy_)
    logger.setLevel(level)
    logger.propagate = False
  return logger
def get_log_level():
  bstack1lll1l11l111_opy_ = os.environ.get(bstack111ll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡅࡇࡅ࡙ࡌࠨ⒬"), bstack111ll_opy_ (u"ࠤࡩࡥࡱࡹࡥࠣ⒭"))
  return logging.DEBUG if bstack1lll1l11l111_opy_.lower() == bstack111ll_opy_ (u"ࠥࡸࡷࡻࡥࠣ⒮") else logging.INFO
def bstack11lll11l1ll_opy_():
  global bstack1lll1l11ll11_opy_
  if os.path.exists(bstack1lll1l11ll11_opy_):
    os.remove(bstack1lll1l11ll11_opy_)
  if os.path.exists(bstack1lll1l1lll11_opy_):
    os.remove(bstack1lll1l1lll11_opy_)
def bstack11l1l1ll1_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def configure_logger(config, log_level):
  bstack1lll1l1l1lll_opy_ = log_level
  if bstack111ll_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭⒯") in config and config[bstack111ll_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧ⒰")] in bstack11111111lll_opy_:
    bstack1lll1l1l1lll_opy_ = bstack11111111lll_opy_[config[bstack111ll_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨ⒱")]]
  if config.get(bstack111ll_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡷࡷࡳࡈࡧࡰࡵࡷࡵࡩࡑࡵࡧࡴࠩ⒲"), False):
    logging.getLogger().setLevel(bstack1lll1l1l1lll_opy_)
    return bstack1lll1l1l1lll_opy_
  global bstack1lll1l11ll11_opy_
  bstack11l1l1ll1_opy_()
  bstack1lll1l1ll1ll_opy_ = logging.Formatter(
    fmt=bstack111ll_opy_ (u"ࠨࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲ࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫ⒳"),
    datefmt=bstack111ll_opy_ (u"ࠩࠨ࡝࠲ࠫ࡭࠮ࠧࡧࡘࠪࡎ࠺ࠦࡏ࠽ࠩࡘࡠࠧ⒴"),
  )
  bstack1lll1l11l11l_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1lll1l11ll11_opy_)
  file_handler.setFormatter(bstack1lll1l1ll1ll_opy_)
  bstack1lll1l11l11l_opy_.setFormatter(bstack1lll1l1ll1ll_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1lll1l11l11l_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack111ll_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲ࠯ࡴࡨࡱࡴࡺࡥ࠯ࡴࡨࡱࡴࡺࡥࡠࡥࡲࡲࡳ࡫ࡣࡵ࡫ࡲࡲࠬ⒵"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1lll1l11l11l_opy_.setLevel(bstack1lll1l1l1lll_opy_)
  logging.getLogger().addHandler(bstack1lll1l11l11l_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1lll1l1l1lll_opy_
def bstack1lll1l11l1l1_opy_(config):
  try:
    bstack1lll1l1111ll_opy_ = set(bstack111111lll1l_opy_)
    bstack1lll1l11ll1l_opy_ = bstack111ll_opy_ (u"ࠫࠬⒶ")
    with open(bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨⒷ")) as bstack1lll1l1l111l_opy_:
      bstack1lll1l11llll_opy_ = bstack1lll1l1l111l_opy_.read()
      bstack1lll1l11ll1l_opy_ = re.sub(bstack111ll_opy_ (u"ࡸࠧ࡟ࠪ࡟ࡷ࠰࠯࠿ࠤ࠰࠭ࠨࡡࡴࠧⒸ"), bstack111ll_opy_ (u"ࠧࠨⒹ"), bstack1lll1l11llll_opy_, flags=re.M)
      bstack1lll1l11ll1l_opy_ = re.sub(
        bstack111ll_opy_ (u"ࡳࠩࡡࠬࡡࡹࠫࠪࡁࠫࠫⒺ") + bstack111ll_opy_ (u"ࠩࡿࠫⒻ").join(bstack1lll1l1111ll_opy_) + bstack111ll_opy_ (u"ࠪ࠭࠳࠰ࠤࠨⒼ"),
        bstack111ll_opy_ (u"ࡶࠬࡢ࠲࠻ࠢ࡞ࡖࡊࡊࡁࡄࡖࡈࡈࡢ࠭Ⓗ"),
        bstack1lll1l11ll1l_opy_, flags=re.M | re.I
      )
    def bstack1lll1l111l11_opy_(dic):
      bstack1lll1l1l11l1_opy_ = {}
      for key, value in dic.items():
        if key in bstack1lll1l1111ll_opy_:
          bstack1lll1l1l11l1_opy_[key] = bstack111ll_opy_ (u"ࠬࡡࡒࡆࡆࡄࡇ࡙ࡋࡄ࡞ࠩⒾ")
        else:
          if isinstance(value, dict):
            bstack1lll1l1l11l1_opy_[key] = bstack1lll1l111l11_opy_(value)
          else:
            bstack1lll1l1l11l1_opy_[key] = value
      return bstack1lll1l1l11l1_opy_
    bstack1lll1l1l11l1_opy_ = bstack1lll1l111l11_opy_(config)
    return {
      bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩⒿ"): bstack1lll1l11ll1l_opy_,
      bstack111ll_opy_ (u"ࠧࡧ࡫ࡱࡥࡱࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪⓀ"): json.dumps(bstack1lll1l1l11l1_opy_)
    }
  except Exception as e:
    return {}
def bstack1lll1l11l1ll_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack111ll_opy_ (u"ࠨ࡮ࡲ࡫ࠬⓁ"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack1l1l1l1lll_opy_ = os.path.join(log_dir, bstack111ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡦࡳࡳ࡬ࡩࡨࡵࠪⓂ"))
  if not os.path.exists(bstack1l1l1l1lll_opy_):
    bstack1lll1l1l11ll_opy_ = {
      bstack111ll_opy_ (u"ࠥ࡭ࡳ࡯ࡰࡢࡶ࡫ࠦⓃ"): str(inipath),
      bstack111ll_opy_ (u"ࠦࡷࡵ࡯ࡵࡲࡤࡸ࡭ࠨⓄ"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack111ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡩ࡯࡯ࡨ࡬࡫ࡸ࠴ࡪࡴࡱࡱࠫⓅ")), bstack111ll_opy_ (u"࠭ࡷࠨⓆ")) as bstack1lll1l111lll_opy_:
      bstack1lll1l111lll_opy_.write(json.dumps(bstack1lll1l1l11ll_opy_))
def bstack1lll1l1ll111_opy_():
  try:
    bstack1l1l1l1lll_opy_ = os.path.join(os.getcwd(), bstack111ll_opy_ (u"ࠧ࡭ࡱࡪࠫⓇ"), bstack111ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡥࡲࡲ࡫࡯ࡧࡴ࠰࡭ࡷࡴࡴࠧⓈ"))
    if os.path.exists(bstack1l1l1l1lll_opy_):
      with open(bstack1l1l1l1lll_opy_, bstack111ll_opy_ (u"ࠩࡵࠫⓉ")) as bstack1lll1l111lll_opy_:
        bstack1lll1l1lllll_opy_ = json.load(bstack1lll1l111lll_opy_)
      return bstack1lll1l1lllll_opy_.get(bstack111ll_opy_ (u"ࠪ࡭ࡳ࡯ࡰࡢࡶ࡫ࠫⓊ"), bstack111ll_opy_ (u"ࠫࠬⓋ")), bstack1lll1l1lllll_opy_.get(bstack111ll_opy_ (u"ࠬࡸ࡯ࡰࡶࡳࡥࡹ࡮ࠧⓌ"), bstack111ll_opy_ (u"࠭ࠧⓍ"))
  except:
    pass
  return None, None
def bstack1lll1l1l1l11_opy_():
  try:
    bstack1l1l1l1lll_opy_ = os.path.join(os.getcwd(), bstack111ll_opy_ (u"ࠧ࡭ࡱࡪࠫⓎ"), bstack111ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡥࡲࡲ࡫࡯ࡧࡴ࠰࡭ࡷࡴࡴࠧⓏ"))
    if os.path.exists(bstack1l1l1l1lll_opy_):
      os.remove(bstack1l1l1l1lll_opy_)
  except:
    pass
def bstack1lllll1l1_opy_(config):
  try:
    try:
      from bstack_utils.bstack11ll1l1l_opy_ import bstack111l1l1l_opy_
    except Exception:
      bstack111l1l1l_opy_ = None
    start_time = time.time()
    from bstack_utils.helper import global_config, bstack11l1llll1l_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack1lll1l11ll11_opy_
    if config.get(bstack111ll_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫⓐ"), False):
      return
    uuid = os.getenv(bstack111ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨⓑ")) if os.getenv(bstack111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩⓒ")) else global_config.get_property(bstack111ll_opy_ (u"ࠧࡹࡤ࡬ࡔࡸࡲࡎࡪࠢⓓ"))
    if not uuid or uuid == bstack111ll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫⓔ"):
      return
    bstack1lll1l1l1111_opy_ = bstack111l1l1l_opy_.bstack1ll1111l1_opy_(EVENTS.bstack111111l1lll_opy_.value) if bstack111l1l1l_opy_ else None
    bstack1lll1l1l1l1l_opy_ = [bstack111ll_opy_ (u"ࠧࡳࡧࡴࡹ࡮ࡸࡥ࡮ࡧࡱࡸࡸ࠴ࡴࡹࡶࠪⓕ"), bstack111ll_opy_ (u"ࠨࡒ࡬ࡴ࡫࡯࡬ࡦࠩⓖ"), bstack111ll_opy_ (u"ࠩࡳࡽࡵࡸ࡯࡫ࡧࡦࡸ࠳ࡺ࡯࡮࡮ࠪⓗ"), bstack1lll1l11ll11_opy_, bstack1lll1l1lll11_opy_]
    bstack1lll1l1lll1l_opy_, root_path = bstack1lll1l1ll111_opy_()
    if bstack1lll1l1lll1l_opy_ != None:
      bstack1lll1l1l1l1l_opy_.append(bstack1lll1l1lll1l_opy_)
    if root_path != None:
      bstack1lll1l1l1l1l_opy_.append(os.path.join(root_path, bstack111ll_opy_ (u"ࠪࡧࡴࡴࡦࡵࡧࡶࡸ࠳ࡶࡹࠨⓘ")))
    bstack1lll1l111l1l_opy_ = os.path.join(os.getcwd(), bstack111ll_opy_ (u"ࠫࡱࡵࡧࠨⓙ"), bstack111ll_opy_ (u"ࠬࡱࡥࡺ࠯ࡰࡩࡹࡸࡩࡤࡵ࠱࡮ࡸࡵ࡮ࠨⓚ"))
    if os.path.exists(bstack1lll1l111l1l_opy_):
      bstack1lll1l1l1l1l_opy_.append(bstack1lll1l111l1l_opy_)
    output_file = os.path.join(tempfile.gettempdir(), bstack111ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࠳࡬ࡰࡩࡶ࠱ࠬⓛ") + uuid + bstack111ll_opy_ (u"ࠧ࠯ࡶࡤࡶ࠳࡭ࡺࠨⓜ"))
    with tarfile.open(output_file, bstack111ll_opy_ (u"ࠣࡹ࠽࡫ࡿࠨⓝ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1lll1l1l1l1l_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1lll1l11l1l1_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1lll1l111ll1_opy_ = data.encode()
        tarinfo.size = len(bstack1lll1l111ll1_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1lll1l111ll1_opy_))
    multipart_data = MultipartEncoder(
      fields= {
        bstack111ll_opy_ (u"ࠩࡧࡥࡹࡧࠧⓞ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack111ll_opy_ (u"ࠪࡶࡧ࠭ⓟ")), bstack111ll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱ࡻ࠱࡬ࢀࡩࡱࠩⓠ")),
        bstack111ll_opy_ (u"ࠬࡩ࡬ࡪࡧࡱࡸࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧⓡ"): uuid
      }
    )
    bstack1lll1l1ll11l_opy_ = bstack11l1llll1l_opy_(cli.config, [bstack111ll_opy_ (u"ࠨࡡࡱ࡫ࡶࠦⓢ"), bstack111ll_opy_ (u"ࠢࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠢⓣ"), bstack111ll_opy_ (u"ࠣࡷࡳࡰࡴࡧࡤࠣⓤ")], bstack1111111l1ll_opy_)
    response = requests.post(
      bstack111ll_opy_ (u"ࠤࡾࢁ࠴ࡩ࡬ࡪࡧࡱࡸ࠲ࡲ࡯ࡨࡵ࠲ࡹࡵࡲ࡯ࡢࡦࠥⓥ").format(bstack1lll1l1ll11l_opy_),
      data=multipart_data,
      headers={bstack111ll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩⓦ"): multipart_data.content_type},
      auth=(config[bstack111ll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ⓧ")], config[bstack111ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨⓨ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack111ll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡻࡰ࡭ࡱࡤࡨࠥࡲ࡯ࡨࡵ࠽ࠤࠬⓩ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack111ll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡰࡧ࡭ࡳ࡭ࠠ࡭ࡱࡪࡷ࠿࠭⓪") + str(e))
  finally:
    try:
      bstack11lll11l1ll_opy_()
      bstack1lll1l1l1l11_opy_()
    except:
      pass
    if bstack111l1l1l_opy_ and bstack1lll1l1l1111_opy_:
      bstack111l1l1l_opy_.end(EVENTS.bstack111111l1lll_opy_.value, bstack1lll1l1l1111_opy_ + bstack111ll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ⓫"), bstack1lll1l1l1111_opy_ + bstack111ll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ⓬"), status=True, failure=None, test_name=None)
    try:
      elapsed = time.time() - start_time
      get_logger().debug(bstack111ll_opy_ (u"ࠥࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡸࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠢ࡬ࡲࠥࢁ࠺࠯࠵ࡩࢁࠥࡹࡥࡤࡱࡱࡨࡸࠨ⓭").format(elapsed))
    except Exception:
      pass