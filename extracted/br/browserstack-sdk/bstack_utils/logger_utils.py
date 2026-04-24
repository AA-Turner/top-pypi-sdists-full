# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
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
from bstack_utils.constants import bstack111111lllll_opy_, EVENTS, bstack1111111ll1l_opy_, bstack111111l11l1_opy_, STAGE
import tempfile
import json
bstack1lll1l1ll111_opy_ = os.getenv(bstack111ll11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡉࡢࡊࡎࡒࡅࠣ⑐"), None) or os.path.join(tempfile.gettempdir(), bstack111ll11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡥࡧࡥࡹ࡬࠴࡬ࡰࡩࠥ⑑"))
bstack1lll1ll11111_opy_ = os.path.join(bstack111ll11_opy_ (u"ࠤ࡯ࡳ࡬ࠨ⑒"), bstack111ll11_opy_ (u"ࠪࡷࡩࡱ࠭ࡤ࡮࡬࠱ࡩ࡫ࡢࡶࡩ࠱ࡰࡴ࡭ࠧ⑓"))
_1lll1l1l1l11_opy_ = threading.Lock()
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack111ll11_opy_ (u"ࠫࠪ࠮ࡡࡴࡥࡷ࡭ࡲ࡫ࠩࡴࠢ࡞ࠩ࠭ࡴࡡ࡮ࡧࠬࡷࡢࡡࠥࠩ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨ࠭ࡸࡣࠠ࠮ࠢࠨࠬࡲ࡫ࡳࡴࡣࡪࡩ࠮ࡹࠧ⑔"),
      datefmt=bstack111ll11_opy_ (u"࡙ࠬࠫ࠮ࠧࡰ࠱ࠪࡪࡔࠦࡊ࠽ࠩࡒࡀࠥࡔ࡜ࠪ⑕"),
      stream=sys.stdout
    )
  return logger
def get_automation_logger(name=__name__, level=logging.DEBUG):
  bstack111ll11_opy_ (u"ࠨࠢࠣࠌࠣࠤࡗ࡫ࡴࡶࡴࡱࡷࠥࡧࠠ࡭ࡱࡪ࡫ࡪࡸࠠࡵࡪࡤࡸࠥࡽࡲࡪࡶࡨࡷࠥࡵ࡮࡭ࡻࠣࡸࡴࠦࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠱ࡰࡴ࡭ࠠࡧ࡫࡯ࡩࠏࠦࠠࡄࡴࡨࡥࡹ࡫ࡳࠡࡣࡱࡨࠥࡳࡡ࡯ࡣࡪࡩࡸࠦࡩࡵࡵࠣࡳࡼࡴࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤ࡫࡯࡬ࡦࠢ࡫ࡥࡳࡪ࡬ࡦࡴࠍࠤࠥࡕ࡮࡭ࡻࠣࡩࡳࡧࡢ࡭ࡧࡶࠤࡱࡵࡧࡨ࡫ࡱ࡫ࠥ࡯ࡦࠡࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࡣࡑࡕࡇࡔࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠢ࡬ࡷࠥࡹࡥࡵࠢࡷࡳࠥࡧࠠࡵࡴࡸࡸ࡭ࡿࠠࡷࡣ࡯ࡹࡪࠐࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࡳࡧ࡭ࡦ࠼ࠣࡐࡴ࡭ࡧࡦࡴࠣࡲࡦࡳࡥࠡࠪࡧࡩ࡫ࡧࡵ࡭ࡶࡶࠤࡹࡵࠠࡠࡡࡱࡥࡲ࡫࡟ࡠࠫࠍࠤࠥࠦࠠ࡭ࡧࡹࡩࡱࡀࠠࡍࡱࡪ࡫࡮ࡴࡧࠡ࡮ࡨࡺࡪࡲࠠࠩࡦࡨࡪࡦࡻ࡬ࡵࡵࠣࡸࡴࠦࡄࡆࡄࡘࡋ࠮ࠐࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠ࡭ࡱࡪ࡫࡮ࡴࡧ࠯ࡎࡲ࡫࡬࡫ࡲ࠻ࠢࡆࡳࡳ࡬ࡩࡨࡷࡵࡩࡩࠦ࡬ࡰࡩࡪࡩࡷࠦࡴࡩࡣࡷࠤࡼࡸࡩࡵࡧࡶࠤࡴࡴ࡬ࡺࠢࡷࡳࠥࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠰࡯ࡳ࡬ࠦࠨࡪࡨࠣࡩࡳࡧࡢ࡭ࡧࡧ࠭ࠏࠦࠠࠣࠤࠥ⑖")
  logger_name = bstack111ll11_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠲ࢀ࠶ࡽࠣ⑗").format(name)
  logger = logging.getLogger(logger_name)
  is_enabled = os.getenv(bstack111ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࡣࡑࡕࡇࡔࠩ⑘"), bstack111ll11_opy_ (u"ࠩࠪ⑙")).lower() == bstack111ll11_opy_ (u"ࠪࡸࡷࡻࡥࠨ⑚")
  if not is_enabled:
    logger.setLevel(logging.CRITICAL)
    logger.propagate = False
    return logger
  with _1lll1l1l1l11_opy_:
    if logger.handlers:
      return logger
    bstack1lll1l11lll1_opy_ = os.path.join(os.getcwd(), bstack111ll11_opy_ (u"ࠫࡱࡵࡧࠨ⑛"), bstack111ll11_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠰࡯ࡳ࡬࠭⑜"))
    log_dir = os.path.dirname(bstack1lll1l11lll1_opy_)
    if not os.path.exists(log_dir):
      os.makedirs(log_dir)
    bstack1lll1l1lllll_opy_ = logging.FileHandler(bstack1lll1l11lll1_opy_)
    bstack1lll1l1l11ll_opy_ = logging.Formatter(
      fmt=bstack111ll11_opy_ (u"࠭ࠥࠩࡣࡶࡧࡹ࡯࡭ࡦࠫࡶࠤࡠࠫࠨ࡯ࡣࡰࡩ࠮ࡹ࡝࡜ࠧࠫࡰࡪࡼࡥ࡭ࡰࡤࡱࡪ࠯ࡳ࡞ࠢ࠰ࠤࡠࠦࡓࡅࡍ࠰ࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠠ࡞ࠢࠨࠬࡲ࡫ࡳࡴࡣࡪࡩ࠮ࡹࠧ⑝"),
      datefmt=bstack111ll11_opy_ (u"࡛ࠧࠦ࠰ࠩࡲ࠳ࠥࡥࡖࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࡞ࠬ⑞"),
    )
    bstack1lll1l1lllll_opy_.setFormatter(bstack1lll1l1l11ll_opy_)
    bstack1lll1l1lllll_opy_.setLevel(level)
    bstack1lll1l1lllll_opy_.addFilter(lambda r: r.name != bstack111ll11_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷ࠴ࡲࡦ࡯ࡲࡸࡪ࠴ࡲࡦ࡯ࡲࡸࡪࡥࡣࡰࡰࡱࡩࡨࡺࡩࡰࡰࠪ⑟"))
    logger.addHandler(bstack1lll1l1lllll_opy_)
    logger.setLevel(level)
    logger.propagate = False
  return logger
def get_log_level():
  bstack1lll1ll1111l_opy_ = os.environ.get(bstack111ll11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡆࡈࡆ࡚ࡍࠢ①"), bstack111ll11_opy_ (u"ࠥࡪࡦࡲࡳࡦࠤ②"))
  return logging.DEBUG if bstack1lll1ll1111l_opy_.lower() == bstack111ll11_opy_ (u"ࠦࡹࡸࡵࡦࠤ③") else logging.INFO
def bstack11lll1l111l_opy_():
  global bstack1lll1l1ll111_opy_
  if os.path.exists(bstack1lll1l1ll111_opy_):
    os.remove(bstack1lll1l1ll111_opy_)
  if os.path.exists(bstack1lll1ll11111_opy_):
    os.remove(bstack1lll1ll11111_opy_)
def bstack11ll1ll1l_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def configure_logger(config, log_level):
  bstack1lll1l11l111_opy_ = log_level
  if bstack111ll11_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧ④") in config and config[bstack111ll11_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨ⑤")] in bstack1111111ll1l_opy_:
    bstack1lll1l11l111_opy_ = bstack1111111ll1l_opy_[config[bstack111ll11_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩ⑥")]]
  if config.get(bstack111ll11_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪ⑦"), False):
    logging.getLogger().setLevel(bstack1lll1l11l111_opy_)
    return bstack1lll1l11l111_opy_
  global bstack1lll1l1ll111_opy_
  bstack11ll1ll1l_opy_()
  bstack1lll1l1ll1l1_opy_ = logging.Formatter(
    fmt=bstack111ll11_opy_ (u"ࠩࠨࠬࡦࡹࡣࡵ࡫ࡰࡩ࠮ࡹࠠ࡜ࠧࠫࡲࡦࡳࡥࠪࡵࡠ࡟ࠪ࠮࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠫࡶࡡࠥ࠳ࠠࠦࠪࡰࡩࡸࡹࡡࡨࡧࠬࡷࠬ⑧"),
    datefmt=bstack111ll11_opy_ (u"ࠪࠩ࡞࠳ࠥ࡮࠯ࠨࡨ࡙ࠫࡈ࠻ࠧࡐ࠾࡙࡚ࠪࠨ⑨"),
  )
  bstack1lll1l1llll1_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1lll1l1ll111_opy_)
  file_handler.setFormatter(bstack1lll1l1ll1l1_opy_)
  bstack1lll1l1llll1_opy_.setFormatter(bstack1lll1l1ll1l1_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1lll1l1llll1_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack111ll11_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳ࠰ࡵࡩࡲࡵࡴࡦ࠰ࡵࡩࡲࡵࡴࡦࡡࡦࡳࡳࡴࡥࡤࡶ࡬ࡳࡳ࠭⑩"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1lll1l1llll1_opy_.setLevel(bstack1lll1l11l111_opy_)
  logging.getLogger().addHandler(bstack1lll1l1llll1_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1lll1l11l111_opy_
def bstack1lll1l11l1ll_opy_(config):
  try:
    bstack1lll1l1l1lll_opy_ = set(bstack111111l11l1_opy_)
    bstack1lll1l11ll11_opy_ = bstack111ll11_opy_ (u"ࠬ࠭⑪")
    with open(bstack111ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩ⑫")) as bstack1lll1ll111ll_opy_:
      bstack1lll1l1l1l1l_opy_ = bstack1lll1ll111ll_opy_.read()
      bstack1lll1l11ll11_opy_ = re.sub(bstack111ll11_opy_ (u"ࡲࠨࡠࠫࡠࡸ࠱ࠩࡀࠥ࠱࠮ࠩࡢ࡮ࠨ⑬"), bstack111ll11_opy_ (u"ࠨࠩ⑭"), bstack1lll1l1l1l1l_opy_, flags=re.M)
      bstack1lll1l11ll11_opy_ = re.sub(
        bstack111ll11_opy_ (u"ࡴࠪࡢ࠭ࡢࡳࠬࠫࡂࠬࠬ⑮") + bstack111ll11_opy_ (u"ࠪࢀࠬ⑯").join(bstack1lll1l1l1lll_opy_) + bstack111ll11_opy_ (u"ࠫ࠮࠴ࠪࠥࠩ⑰"),
        bstack111ll11_opy_ (u"ࡷ࠭࡜࠳࠼ࠣ࡟ࡗࡋࡄࡂࡅࡗࡉࡉࡣࠧ⑱"),
        bstack1lll1l11ll11_opy_, flags=re.M | re.I
      )
    def bstack1lll1l1l1ll1_opy_(dic):
      bstack1lll1l11l1l1_opy_ = {}
      for key, value in dic.items():
        if key in bstack1lll1l1l1lll_opy_:
          bstack1lll1l11l1l1_opy_[key] = bstack111ll11_opy_ (u"࡛࠭ࡓࡇࡇࡅࡈ࡚ࡅࡅ࡟ࠪ⑲")
        else:
          if isinstance(value, dict):
            bstack1lll1l11l1l1_opy_[key] = bstack1lll1l1l1ll1_opy_(value)
          else:
            bstack1lll1l11l1l1_opy_[key] = value
      return bstack1lll1l11l1l1_opy_
    bstack1lll1l11l1l1_opy_ = bstack1lll1l1l1ll1_opy_(config)
    return {
      bstack111ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪ⑳"): bstack1lll1l11ll11_opy_,
      bstack111ll11_opy_ (u"ࠨࡨ࡬ࡲࡦࡲࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫ⑴"): json.dumps(bstack1lll1l11l1l1_opy_)
    }
  except Exception as e:
    return {}
def bstack1lll1l11l11l_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack111ll11_opy_ (u"ࠩ࡯ࡳ࡬࠭⑵"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack11l11l1ll1_opy_ = os.path.join(log_dir, bstack111ll11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶࠫ⑶"))
  if not os.path.exists(bstack11l11l1ll1_opy_):
    bstack1lll1ll111l1_opy_ = {
      bstack111ll11_opy_ (u"ࠦ࡮ࡴࡩࡱࡣࡷ࡬ࠧ⑷"): str(inipath),
      bstack111ll11_opy_ (u"ࠧࡸ࡯ࡰࡶࡳࡥࡹ࡮ࠢ⑸"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack111ll11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡣࡰࡰࡩ࡭࡬ࡹ࠮࡫ࡵࡲࡲࠬ⑹")), bstack111ll11_opy_ (u"ࠧࡸࠩ⑺")) as bstack1lll1l1ll1ll_opy_:
      bstack1lll1l1ll1ll_opy_.write(json.dumps(bstack1lll1ll111l1_opy_))
def bstack1lll1l1lll1l_opy_():
  try:
    bstack11l11l1ll1_opy_ = os.path.join(os.getcwd(), bstack111ll11_opy_ (u"ࠨ࡮ࡲ࡫ࠬ⑻"), bstack111ll11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡦࡳࡳ࡬ࡩࡨࡵ࠱࡮ࡸࡵ࡮ࠨ⑼"))
    if os.path.exists(bstack11l11l1ll1_opy_):
      with open(bstack11l11l1ll1_opy_, bstack111ll11_opy_ (u"ࠪࡶࠬ⑽")) as bstack1lll1l1ll1ll_opy_:
        bstack1lll1l1lll11_opy_ = json.load(bstack1lll1l1ll1ll_opy_)
      return bstack1lll1l1lll11_opy_.get(bstack111ll11_opy_ (u"ࠫ࡮ࡴࡩࡱࡣࡷ࡬ࠬ⑾"), bstack111ll11_opy_ (u"ࠬ࠭⑿")), bstack1lll1l1lll11_opy_.get(bstack111ll11_opy_ (u"࠭ࡲࡰࡱࡷࡴࡦࡺࡨࠨ⒀"), bstack111ll11_opy_ (u"ࠧࠨ⒁"))
  except:
    pass
  return None, None
def bstack1lll1l1l111l_opy_():
  try:
    bstack11l11l1ll1_opy_ = os.path.join(os.getcwd(), bstack111ll11_opy_ (u"ࠨ࡮ࡲ࡫ࠬ⒂"), bstack111ll11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡦࡳࡳ࡬ࡩࡨࡵ࠱࡮ࡸࡵ࡮ࠨ⒃"))
    if os.path.exists(bstack11l11l1ll1_opy_):
      os.remove(bstack11l11l1ll1_opy_)
  except:
    pass
def bstack111ll11lll_opy_(config):
  try:
    try:
      from bstack_utils.bstack1lll1l1ll1_opy_ import bstack1ll1l11l1_opy_
    except Exception:
      bstack1ll1l11l1_opy_ = None
    start_time = time.time()
    from bstack_utils.helper import global_config, bstack11ll1lll11_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack1lll1l1ll111_opy_
    if config.get(bstack111ll11_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬ⒄"), False):
      return
    uuid = os.getenv(bstack111ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ⒅")) if os.getenv(bstack111ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ⒆")) else global_config.get_property(bstack111ll11_opy_ (u"ࠨࡳࡥ࡭ࡕࡹࡳࡏࡤࠣ⒇"))
    if not uuid or uuid == bstack111ll11_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ⒈"):
      return
    bstack1lll1l1l1111_opy_ = bstack1ll1l11l1_opy_.bstack11lllll1_opy_(EVENTS.bstack11111l1lll1_opy_.value) if bstack1ll1l11l1_opy_ else None
    bstack1lll1ll11l11_opy_ = [bstack111ll11_opy_ (u"ࠨࡴࡨࡵࡺ࡯ࡲࡦ࡯ࡨࡲࡹࡹ࠮ࡵࡺࡷࠫ⒉"), bstack111ll11_opy_ (u"ࠩࡓ࡭ࡵ࡬ࡩ࡭ࡧࠪ⒊"), bstack111ll11_opy_ (u"ࠪࡴࡾࡶࡲࡰ࡬ࡨࡧࡹ࠴ࡴࡰ࡯࡯ࠫ⒋"), bstack1lll1l1ll111_opy_, bstack1lll1ll11111_opy_]
    bstack1lll1l11llll_opy_, root_path = bstack1lll1l1lll1l_opy_()
    if bstack1lll1l11llll_opy_ != None:
      bstack1lll1ll11l11_opy_.append(bstack1lll1l11llll_opy_)
    if root_path != None:
      bstack1lll1ll11l11_opy_.append(os.path.join(root_path, bstack111ll11_opy_ (u"ࠫࡨࡵ࡮ࡧࡶࡨࡷࡹ࠴ࡰࡺࠩ⒌")))
    bstack1lll1l11ll1l_opy_ = os.path.join(os.getcwd(), bstack111ll11_opy_ (u"ࠬࡲ࡯ࡨࠩ⒍"), bstack111ll11_opy_ (u"࠭࡫ࡦࡻ࠰ࡱࡪࡺࡲࡪࡥࡶ࠲࡯ࡹ࡯࡯ࠩ⒎"))
    if os.path.exists(bstack1lll1l11ll1l_opy_):
      bstack1lll1ll11l11_opy_.append(bstack1lll1l11ll1l_opy_)
    output_file = os.path.join(tempfile.gettempdir(), bstack111ll11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠭࡭ࡱࡪࡷ࠲࠭⒏") + uuid + bstack111ll11_opy_ (u"ࠨ࠰ࡷࡥࡷ࠴ࡧࡻࠩ⒐"))
    with tarfile.open(output_file, bstack111ll11_opy_ (u"ࠤࡺ࠾࡬ࢀࠢ⒑")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1lll1ll11l11_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1lll1l11l1ll_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1lll1l1ll11l_opy_ = data.encode()
        tarinfo.size = len(bstack1lll1l1ll11l_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1lll1l1ll11l_opy_))
    multipart_data = MultipartEncoder(
      fields= {
        bstack111ll11_opy_ (u"ࠪࡨࡦࡺࡡࠨ⒒"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack111ll11_opy_ (u"ࠫࡷࡨࠧ⒓")), bstack111ll11_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲ࡼ࠲࡭ࡺࡪࡲࠪ⒔")),
        bstack111ll11_opy_ (u"࠭ࡣ࡭࡫ࡨࡲࡹࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ⒕"): uuid
      }
    )
    bstack1lll1l1l11l1_opy_ = bstack11ll1lll11_opy_(cli.config, [bstack111ll11_opy_ (u"ࠢࡢࡲ࡬ࡷࠧ⒖"), bstack111ll11_opy_ (u"ࠣࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠣ⒗"), bstack111ll11_opy_ (u"ࠤࡸࡴࡱࡵࡡࡥࠤ⒘")], bstack111111lllll_opy_)
    response = requests.post(
      bstack111ll11_opy_ (u"ࠥࡿࢂ࠵ࡣ࡭࡫ࡨࡲࡹ࠳࡬ࡰࡩࡶ࠳ࡺࡶ࡬ࡰࡣࡧࠦ⒙").format(bstack1lll1l1l11l1_opy_),
      data=multipart_data,
      headers={bstack111ll11_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪ⒚"): multipart_data.content_type},
      auth=(config[bstack111ll11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ⒛")], config[bstack111ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ⒜")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack111ll11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡵࡱ࡮ࡲࡥࡩࠦ࡬ࡰࡩࡶ࠾ࠥ࠭⒝") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack111ll11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡧࡱࡨ࡮ࡴࡧࠡ࡮ࡲ࡫ࡸࡀࠧ⒞") + str(e))
  finally:
    try:
      bstack11lll1l111l_opy_()
      bstack1lll1l1l111l_opy_()
    except:
      pass
    if bstack1ll1l11l1_opy_ and bstack1lll1l1l1111_opy_:
      bstack1ll1l11l1_opy_.end(EVENTS.bstack11111l1lll1_opy_.value, bstack1lll1l1l1111_opy_ + bstack111ll11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ⒟"), bstack1lll1l1l1111_opy_ + bstack111ll11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ⒠"), status=True, failure=None, test_name=None)
    try:
      elapsed = time.time() - start_time
      get_logger().debug(bstack111ll11_opy_ (u"ࠦࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡹࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࡦࠣ࡭ࡳࠦࡻ࠻࠰࠶ࡪࢂࠦࡳࡦࡥࡲࡲࡩࡹࠢ⒡").format(elapsed))
    except Exception:
      pass