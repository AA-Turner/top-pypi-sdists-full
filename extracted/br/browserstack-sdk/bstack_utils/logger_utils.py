# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
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
from bstack_utils.constants import bstack111111l11l1_opy_, EVENTS, bstack1111111ll11_opy_, bstack111111l1l1l_opy_, STAGE
import tempfile
import json
bstack1lll1ll1l111_opy_ = os.getenv(bstack1l111l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡊࡣࡋࡏࡌࡆࠤ⑃"), None) or os.path.join(tempfile.gettempdir(), bstack1l111l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡦࡨࡦࡺ࡭࠮࡭ࡱࡪࠦ⑄"))
bstack1lll1ll111l1_opy_ = os.path.join(bstack1l111l_opy_ (u"ࠥࡰࡴ࡭ࠢ⑅"), bstack1l111l_opy_ (u"ࠫࡸࡪ࡫࠮ࡥ࡯࡭࠲ࡪࡥࡣࡷࡪ࠲ࡱࡵࡧࠨ⑆"))
_1lll1l1ll111_opy_ = threading.Lock()
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1l111l_opy_ (u"ࠬࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨ⑇"),
      datefmt=bstack1l111l_opy_ (u"࡚࠭ࠥ࠯ࠨࡱ࠲ࠫࡤࡕࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࡝ࠫ⑈"),
      stream=sys.stdout
    )
  return logger
def get_automation_logger(name=__name__, level=logging.DEBUG):
  bstack1l111l_opy_ (u"ࠢࠣࠤࠍࠤࠥࡘࡥࡵࡷࡵࡲࡸࠦࡡࠡ࡮ࡲ࡫࡬࡫ࡲࠡࡶ࡫ࡥࡹࠦࡷࡳ࡫ࡷࡩࡸࠦ࡯࡯࡮ࡼࠤࡹࡵࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠲ࡱࡵࡧࠡࡨ࡬ࡰࡪࠐࠠࠡࡅࡵࡩࡦࡺࡥࡴࠢࡤࡲࡩࠦ࡭ࡢࡰࡤ࡫ࡪࡹࠠࡪࡶࡶࠤࡴࡽ࡮ࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥ࡬ࡩ࡭ࡧࠣ࡬ࡦࡴࡤ࡭ࡧࡵࠎࠥࠦࡏ࡯࡮ࡼࠤࡪࡴࡡࡣ࡮ࡨࡷࠥࡲ࡯ࡨࡩ࡬ࡲ࡬ࠦࡩࡧࠢࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࡤࡒࡏࡈࡕࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴࠡࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠣ࡭ࡸࠦࡳࡦࡶࠣࡸࡴࠦࡡࠡࡶࡵࡹࡹ࡮ࡹࠡࡸࡤࡰࡺ࡫ࠊࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࡴࡡ࡮ࡧ࠽ࠤࡑࡵࡧࡨࡧࡵࠤࡳࡧ࡭ࡦࠢࠫࡨࡪ࡬ࡡࡶ࡮ࡷࡷࠥࡺ࡯ࠡࡡࡢࡲࡦࡳࡥࡠࡡࠬࠎࠥࠦࠠࠡ࡮ࡨࡺࡪࡲ࠺ࠡࡎࡲ࡫࡬࡯࡮ࡨࠢ࡯ࡩࡻ࡫࡬ࠡࠪࡧࡩ࡫ࡧࡵ࡭ࡶࡶࠤࡹࡵࠠࡅࡇࡅ࡙ࡌ࠯ࠊࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡ࡮ࡲ࡫࡬࡯࡮ࡨ࠰ࡏࡳ࡬࡭ࡥࡳ࠼ࠣࡇࡴࡴࡦࡪࡩࡸࡶࡪࡪࠠ࡭ࡱࡪ࡫ࡪࡸࠠࡵࡪࡤࡸࠥࡽࡲࡪࡶࡨࡷࠥࡵ࡮࡭ࡻࠣࡸࡴࠦࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠱ࡰࡴ࡭ࠠࠩ࡫ࡩࠤࡪࡴࡡࡣ࡮ࡨࡨ࠮ࠐࠠࠡࠤࠥࠦ⑉")
  logger_name = bstack1l111l_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠳ࢁ࠰ࡾࠤ⑊").format(name)
  logger = logging.getLogger(logger_name)
  is_enabled = os.getenv(bstack1l111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࡤࡒࡏࡈࡕࠪ⑋"), bstack1l111l_opy_ (u"ࠪࠫ⑌")).lower() == bstack1l111l_opy_ (u"ࠫࡹࡸࡵࡦࠩ⑍")
  if not is_enabled:
    logger.setLevel(logging.CRITICAL)
    logger.propagate = False
    return logger
  with _1lll1l1ll111_opy_:
    if logger.handlers:
      return logger
    bstack1lll1l1l11ll_opy_ = os.path.join(os.getcwd(), bstack1l111l_opy_ (u"ࠬࡲ࡯ࡨࠩ⑎"), bstack1l111l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠱ࡰࡴ࡭ࠧ⑏"))
    log_dir = os.path.dirname(bstack1lll1l1l11ll_opy_)
    if not os.path.exists(log_dir):
      os.makedirs(log_dir)
    bstack1lll1ll1111l_opy_ = logging.FileHandler(bstack1lll1l1l11ll_opy_)
    bstack1lll1l11llll_opy_ = logging.Formatter(
      fmt=bstack1l111l_opy_ (u"ࠧࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࡡࠠࡔࡆࡎ࠱ࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠡ࡟ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨ⑐"),
      datefmt=bstack1l111l_opy_ (u"ࠨࠧ࡜࠱ࠪࡳ࠭ࠦࡦࡗࠩࡍࡀࠥࡎ࠼ࠨࡗ࡟࠭⑑"),
    )
    bstack1lll1ll1111l_opy_.setFormatter(bstack1lll1l11llll_opy_)
    bstack1lll1ll1111l_opy_.setLevel(level)
    bstack1lll1ll1111l_opy_.addFilter(lambda r: r.name != bstack1l111l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࠮ࡳࡧࡰࡳࡹ࡫࠮ࡳࡧࡰࡳࡹ࡫࡟ࡤࡱࡱࡲࡪࡩࡴࡪࡱࡱࠫ⑒"))
    logger.addHandler(bstack1lll1ll1111l_opy_)
    logger.setLevel(level)
    logger.propagate = False
  return logger
def get_log_level():
  bstack1lll1l1l1111_opy_ = os.environ.get(bstack1l111l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡇࡉࡇ࡛ࡇࠣ⑓"), bstack1l111l_opy_ (u"ࠦ࡫ࡧ࡬ࡴࡧࠥ⑔"))
  return logging.DEBUG if bstack1lll1l1l1111_opy_.lower() == bstack1l111l_opy_ (u"ࠧࡺࡲࡶࡧࠥ⑕") else logging.INFO
def bstack11ll1l111ll_opy_():
  global bstack1lll1ll1l111_opy_
  if os.path.exists(bstack1lll1ll1l111_opy_):
    os.remove(bstack1lll1ll1l111_opy_)
  if os.path.exists(bstack1lll1ll111l1_opy_):
    os.remove(bstack1lll1ll111l1_opy_)
def bstack1l1111l1l1_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def configure_logger(config, log_level):
  bstack1lll1l1l11l1_opy_ = log_level
  if bstack1l111l_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨ⑖") in config and config[bstack1l111l_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩ⑗")] in bstack1111111ll11_opy_:
    bstack1lll1l1l11l1_opy_ = bstack1111111ll11_opy_[config[bstack1l111l_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪ⑘")]]
  if config.get(bstack1l111l_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫ⑙"), False):
    logging.getLogger().setLevel(bstack1lll1l1l11l1_opy_)
    return bstack1lll1l1l11l1_opy_
  global bstack1lll1ll1l111_opy_
  bstack1l1111l1l1_opy_()
  bstack1lll1l1l1l11_opy_ = logging.Formatter(
    fmt=bstack1l111l_opy_ (u"ࠪࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭⑚"),
    datefmt=bstack1l111l_opy_ (u"ࠫࠪ࡟࠭ࠦ࡯࠰ࠩࡩ࡚ࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࡛ࠩ⑛"),
  )
  bstack1lll1ll111ll_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1lll1ll1l111_opy_)
  file_handler.setFormatter(bstack1lll1l1l1l11_opy_)
  bstack1lll1ll111ll_opy_.setFormatter(bstack1lll1l1l1l11_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1lll1ll111ll_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1l111l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡶࡪࡳ࡯ࡵࡧ࠱ࡶࡪࡳ࡯ࡵࡧࡢࡧࡴࡴ࡮ࡦࡥࡷ࡭ࡴࡴࠧ⑜"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1lll1ll111ll_opy_.setLevel(bstack1lll1l1l11l1_opy_)
  logging.getLogger().addHandler(bstack1lll1ll111ll_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1lll1l1l11l1_opy_
def bstack1lll1ll11111_opy_(config):
  try:
    bstack1lll1l1l1ll1_opy_ = set(bstack111111l1l1l_opy_)
    bstack1lll1l1lllll_opy_ = bstack1l111l_opy_ (u"࠭ࠧ⑝")
    with open(bstack1l111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪ⑞")) as bstack1lll1l1l1l1l_opy_:
      bstack1lll1ll1l1ll_opy_ = bstack1lll1l1l1l1l_opy_.read()
      bstack1lll1l1lllll_opy_ = re.sub(bstack1l111l_opy_ (u"ࡳࠩࡡࠬࡡࡹࠫࠪࡁࠦ࠲࠯ࠪ࡜࡯ࠩ⑟"), bstack1l111l_opy_ (u"ࠩࠪ①"), bstack1lll1ll1l1ll_opy_, flags=re.M)
      bstack1lll1l1lllll_opy_ = re.sub(
        bstack1l111l_opy_ (u"ࡵࠫࡣ࠮࡜ࡴ࠭ࠬࡃ࠭࠭②") + bstack1l111l_opy_ (u"ࠫࢁ࠭③").join(bstack1lll1l1l1ll1_opy_) + bstack1l111l_opy_ (u"ࠬ࠯࠮ࠫࠦࠪ④"),
        bstack1l111l_opy_ (u"ࡸࠧ࡝࠴࠽ࠤࡠࡘࡅࡅࡃࡆࡘࡊࡊ࡝ࠨ⑤"),
        bstack1lll1l1lllll_opy_, flags=re.M | re.I
      )
    def bstack1lll1ll11l11_opy_(dic):
      bstack1lll1l1l1lll_opy_ = {}
      for key, value in dic.items():
        if key in bstack1lll1l1l1ll1_opy_:
          bstack1lll1l1l1lll_opy_[key] = bstack1l111l_opy_ (u"ࠧ࡜ࡔࡈࡈࡆࡉࡔࡆࡆࡠࠫ⑥")
        else:
          if isinstance(value, dict):
            bstack1lll1l1l1lll_opy_[key] = bstack1lll1ll11l11_opy_(value)
          else:
            bstack1lll1l1l1lll_opy_[key] = value
      return bstack1lll1l1l1lll_opy_
    bstack1lll1l1l1lll_opy_ = bstack1lll1ll11l11_opy_(config)
    return {
      bstack1l111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫ⑦"): bstack1lll1l1lllll_opy_,
      bstack1l111l_opy_ (u"ࠩࡩ࡭ࡳࡧ࡬ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬ⑧"): json.dumps(bstack1lll1l1l1lll_opy_)
    }
  except Exception as e:
    return {}
def bstack1lll1l1ll11l_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack1l111l_opy_ (u"ࠪࡰࡴ࡭ࠧ⑨"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack1lll1l11_opy_ = os.path.join(log_dir, bstack1l111l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷࠬ⑩"))
  if not os.path.exists(bstack1lll1l11_opy_):
    bstack1lll1l1lll1l_opy_ = {
      bstack1l111l_opy_ (u"ࠧ࡯࡮ࡪࡲࡤࡸ࡭ࠨ⑪"): str(inipath),
      bstack1l111l_opy_ (u"ࠨࡲࡰࡱࡷࡴࡦࡺࡨࠣ⑫"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack1l111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡤࡱࡱࡪ࡮࡭ࡳ࠯࡬ࡶࡳࡳ࠭⑬")), bstack1l111l_opy_ (u"ࠨࡹࠪ⑭")) as bstack1lll1l1l111l_opy_:
      bstack1lll1l1l111l_opy_.write(json.dumps(bstack1lll1l1lll1l_opy_))
def bstack1lll1ll1l1l1_opy_():
  try:
    bstack1lll1l11_opy_ = os.path.join(os.getcwd(), bstack1l111l_opy_ (u"ࠩ࡯ࡳ࡬࠭⑮"), bstack1l111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶ࠲࡯ࡹ࡯࡯ࠩ⑯"))
    if os.path.exists(bstack1lll1l11_opy_):
      with open(bstack1lll1l11_opy_, bstack1l111l_opy_ (u"ࠫࡷ࠭⑰")) as bstack1lll1l1l111l_opy_:
        bstack1lll1l1llll1_opy_ = json.load(bstack1lll1l1l111l_opy_)
      return bstack1lll1l1llll1_opy_.get(bstack1l111l_opy_ (u"ࠬ࡯࡮ࡪࡲࡤࡸ࡭࠭⑱"), bstack1l111l_opy_ (u"࠭ࠧ⑲")), bstack1lll1l1llll1_opy_.get(bstack1l111l_opy_ (u"ࠧࡳࡱࡲࡸࡵࡧࡴࡩࠩ⑳"), bstack1l111l_opy_ (u"ࠨࠩ⑴"))
  except:
    pass
  return None, None
def bstack1lll1l1ll1ll_opy_():
  try:
    bstack1lll1l11_opy_ = os.path.join(os.getcwd(), bstack1l111l_opy_ (u"ࠩ࡯ࡳ࡬࠭⑵"), bstack1l111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶ࠲࡯ࡹ࡯࡯ࠩ⑶"))
    if os.path.exists(bstack1lll1l11_opy_):
      os.remove(bstack1lll1l11_opy_)
  except:
    pass
def bstack1ll111l11_opy_(config):
  try:
    try:
      from bstack_utils.bstack1llll111_opy_ import bstack111ll11l1_opy_
    except Exception:
      bstack111ll11l1_opy_ = None
    start_time = time.time()
    from bstack_utils.helper import global_config, bstack111lll1ll_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack1lll1ll1l111_opy_
    if config.get(bstack1l111l_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭⑷"), False):
      return
    uuid = os.getenv(bstack1l111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ⑸")) if os.getenv(bstack1l111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ⑹")) else global_config.get_property(bstack1l111l_opy_ (u"ࠢࡴࡦ࡮ࡖࡺࡴࡉࡥࠤ⑺"))
    if not uuid or uuid == bstack1l111l_opy_ (u"ࠨࡰࡸࡰࡱ࠭⑻"):
      return
    bstack1lll1l1lll11_opy_ = bstack111ll11l1_opy_.bstack11l1111ll_opy_(EVENTS.bstack111111l1lll_opy_.value) if bstack111ll11l1_opy_ else None
    bstack1lll1l1ll1l1_opy_ = [bstack1l111l_opy_ (u"ࠩࡵࡩࡶࡻࡩࡳࡧࡰࡩࡳࡺࡳ࠯ࡶࡻࡸࠬ⑼"), bstack1l111l_opy_ (u"ࠪࡔ࡮ࡶࡦࡪ࡮ࡨࠫ⑽"), bstack1l111l_opy_ (u"ࠫࡵࡿࡰࡳࡱ࡭ࡩࡨࡺ࠮ࡵࡱࡰࡰࠬ⑾"), bstack1lll1ll1l111_opy_, bstack1lll1ll111l1_opy_]
    bstack1lll1ll11lll_opy_, root_path = bstack1lll1ll1l1l1_opy_()
    if bstack1lll1ll11lll_opy_ != None:
      bstack1lll1l1ll1l1_opy_.append(bstack1lll1ll11lll_opy_)
    if root_path != None:
      bstack1lll1l1ll1l1_opy_.append(os.path.join(root_path, bstack1l111l_opy_ (u"ࠬࡩ࡯࡯ࡨࡷࡩࡸࡺ࠮ࡱࡻࠪ⑿")))
    bstack1lll1ll11ll1_opy_ = os.path.join(os.getcwd(), bstack1l111l_opy_ (u"࠭࡬ࡰࡩࠪ⒀"), bstack1l111l_opy_ (u"ࠧ࡬ࡧࡼ࠱ࡲ࡫ࡴࡳ࡫ࡦࡷ࠳ࡰࡳࡰࡰࠪ⒁"))
    if os.path.exists(bstack1lll1ll11ll1_opy_):
      bstack1lll1l1ll1l1_opy_.append(bstack1lll1ll11ll1_opy_)
    output_file = os.path.join(tempfile.gettempdir(), bstack1l111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠮࡮ࡲ࡫ࡸ࠳ࠧ⒂") + uuid + bstack1l111l_opy_ (u"ࠩ࠱ࡸࡦࡸ࠮ࡨࡼࠪ⒃"))
    with tarfile.open(output_file, bstack1l111l_opy_ (u"ࠥࡻ࠿࡭ࡺࠣ⒄")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1lll1l1ll1l1_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1lll1ll11111_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1lll1ll11l1l_opy_ = data.encode()
        tarinfo.size = len(bstack1lll1ll11l1l_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1lll1ll11l1l_opy_))
    multipart_data = MultipartEncoder(
      fields= {
        bstack1l111l_opy_ (u"ࠫࡩࡧࡴࡢࠩ⒅"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1l111l_opy_ (u"ࠬࡸࡢࠨ⒆")), bstack1l111l_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳ࡽ࠳ࡧࡻ࡫ࡳࠫ⒇")),
        bstack1l111l_opy_ (u"ࠧࡤ࡮࡬ࡩࡳࡺࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ⒈"): uuid
      }
    )
    bstack1lll1ll1l11l_opy_ = bstack111lll1ll_opy_(cli.config, [bstack1l111l_opy_ (u"ࠣࡣࡳ࡭ࡸࠨ⒉"), bstack1l111l_opy_ (u"ࠤࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠤ⒊"), bstack1l111l_opy_ (u"ࠥࡹࡵࡲ࡯ࡢࡦࠥ⒋")], bstack111111l11l1_opy_)
    response = requests.post(
      bstack1l111l_opy_ (u"ࠦࢀࢃ࠯ࡤ࡮࡬ࡩࡳࡺ࠭࡭ࡱࡪࡷ࠴ࡻࡰ࡭ࡱࡤࡨࠧ⒌").format(bstack1lll1ll1l11l_opy_),
      data=multipart_data,
      headers={bstack1l111l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ⒍"): multipart_data.content_type},
      auth=(config[bstack1l111l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ⒎")], config[bstack1l111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ⒏")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1l111l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡶࡲ࡯ࡳࡦࡪࠠ࡭ࡱࡪࡷ࠿ࠦࠧ⒐") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1l111l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡲࡩ࡯࡮ࡨࠢ࡯ࡳ࡬ࡹ࠺ࠨ⒑") + str(e))
  finally:
    try:
      bstack11ll1l111ll_opy_()
      bstack1lll1l1ll1ll_opy_()
    except:
      pass
    if bstack111ll11l1_opy_ and bstack1lll1l1lll11_opy_:
      bstack111ll11l1_opy_.end(EVENTS.bstack111111l1lll_opy_.value, bstack1lll1l1lll11_opy_ + bstack1l111l_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ⒒"), bstack1lll1l1lll11_opy_ + bstack1l111l_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ⒓"), status=True, failure=None, test_name=None)
    try:
      elapsed = time.time() - start_time
      get_logger().debug(bstack1l111l_opy_ (u"ࠧࡹࡥ࡯ࡦࡢࡰࡴ࡭ࡳࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠤ࡮ࡴࠠࡼ࠼࠱࠷࡫ࢃࠠࡴࡧࡦࡳࡳࡪࡳࠣ⒔").format(elapsed))
    except Exception:
      pass