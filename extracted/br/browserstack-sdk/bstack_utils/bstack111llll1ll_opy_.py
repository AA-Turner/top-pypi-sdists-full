# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
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
from bstack_utils.constants import bstack11l111lll11_opy_, EVENTS, bstack11l11l11l1l_opy_, bstack11l11111l1l_opy_, STAGE
import tempfile
import json
bstack1111l1l111l_opy_ = os.getenv(bstack1l1111_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡉࡢࡊࡎࡒࡅࠣử"), None) or os.path.join(tempfile.gettempdir(), bstack1l1111_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡥࡧࡥࡹ࡬࠴࡬ࡰࡩࠥỮ"))
bstack1111l11ll11_opy_ = os.path.join(bstack1l1111_opy_ (u"ࠤ࡯ࡳ࡬ࠨữ"), bstack1l1111_opy_ (u"ࠪࡷࡩࡱ࠭ࡤ࡮࡬࠱ࡩ࡫ࡢࡶࡩ࠱ࡰࡴ࡭ࠧỰ"))
_1111l1lll1l_opy_ = threading.Lock()
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1l1111_opy_ (u"ࠫࠪ࠮ࡡࡴࡥࡷ࡭ࡲ࡫ࠩࡴࠢ࡞ࠩ࠭ࡴࡡ࡮ࡧࠬࡷࡢࡡࠥࠩ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨ࠭ࡸࡣࠠ࠮ࠢࠨࠬࡲ࡫ࡳࡴࡣࡪࡩ࠮ࡹࠧự"),
      datefmt=bstack1l1111_opy_ (u"࡙ࠬࠫ࠮ࠧࡰ࠱ࠪࡪࡔࠦࡊ࠽ࠩࡒࡀࠥࡔ࡜ࠪỲ"),
      stream=sys.stdout
    )
  return logger
def bstack1l11ll11l_opy_(name=__name__, level=logging.DEBUG):
  bstack1l1111_opy_ (u"ࠨࠢࠣࠌࠣࠤࡗ࡫ࡴࡶࡴࡱࡷࠥࡧࠠ࡭ࡱࡪ࡫ࡪࡸࠠࡵࡪࡤࡸࠥࡽࡲࡪࡶࡨࡷࠥࡵ࡮࡭ࡻࠣࡸࡴࠦࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠱ࡰࡴ࡭ࠠࡧ࡫࡯ࡩࠏࠦࠠࡄࡴࡨࡥࡹ࡫ࡳࠡࡣࡱࡨࠥࡳࡡ࡯ࡣࡪࡩࡸࠦࡩࡵࡵࠣࡳࡼࡴࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤ࡫࡯࡬ࡦࠢ࡫ࡥࡳࡪ࡬ࡦࡴࠍࠤࠥࡕ࡮࡭ࡻࠣࡩࡳࡧࡢ࡭ࡧࡶࠤࡱࡵࡧࡨ࡫ࡱ࡫ࠥ࡯ࡦࠡࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࡣࡑࡕࡇࡔࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠢ࡬ࡷࠥࡹࡥࡵࠢࡷࡳࠥࡧࠠࡵࡴࡸࡸ࡭ࡿࠠࡷࡣ࡯ࡹࡪࠐࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࡳࡧ࡭ࡦ࠼ࠣࡐࡴ࡭ࡧࡦࡴࠣࡲࡦࡳࡥࠡࠪࡧࡩ࡫ࡧࡵ࡭ࡶࡶࠤࡹࡵࠠࡠࡡࡱࡥࡲ࡫࡟ࡠࠫࠍࠤࠥࠦࠠ࡭ࡧࡹࡩࡱࡀࠠࡍࡱࡪ࡫࡮ࡴࡧࠡ࡮ࡨࡺࡪࡲࠠࠩࡦࡨࡪࡦࡻ࡬ࡵࡵࠣࡸࡴࠦࡄࡆࡄࡘࡋ࠮ࠐࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠ࡭ࡱࡪ࡫࡮ࡴࡧ࠯ࡎࡲ࡫࡬࡫ࡲ࠻ࠢࡆࡳࡳ࡬ࡩࡨࡷࡵࡩࡩࠦ࡬ࡰࡩࡪࡩࡷࠦࡴࡩࡣࡷࠤࡼࡸࡩࡵࡧࡶࠤࡴࡴ࡬ࡺࠢࡷࡳࠥࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠰࡯ࡳ࡬ࠦࠨࡪࡨࠣࡩࡳࡧࡢ࡭ࡧࡧ࠭ࠏࠦࠠࠣࠤࠥỳ")
  logger_name = bstack1l1111_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠲ࢀ࠶ࡽࠣỴ").format(name)
  logger = logging.getLogger(logger_name)
  is_enabled = os.getenv(bstack1l1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࡣࡑࡕࡇࡔࠩỵ"), bstack1l1111_opy_ (u"ࠩࠪỶ")).lower() == bstack1l1111_opy_ (u"ࠪࡸࡷࡻࡥࠨỷ")
  if not is_enabled:
    logger.setLevel(logging.CRITICAL)
    logger.propagate = False
    return logger
  with _1111l1lll1l_opy_:
    if logger.handlers:
      return logger
    bstack1111l11l11l_opy_ = os.path.join(os.getcwd(), bstack1l1111_opy_ (u"ࠫࡱࡵࡧࠨỸ"), bstack1l1111_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠰࡯ࡳ࡬࠭ỹ"))
    log_dir = os.path.dirname(bstack1111l11l11l_opy_)
    if not os.path.exists(log_dir):
      os.makedirs(log_dir)
    bstack1111l11lll1_opy_ = logging.FileHandler(bstack1111l11l11l_opy_)
    bstack1111l1lll11_opy_ = logging.Formatter(
      fmt=bstack1l1111_opy_ (u"࠭ࠥࠩࡣࡶࡧࡹ࡯࡭ࡦࠫࡶࠤࡠࠫࠨ࡯ࡣࡰࡩ࠮ࡹ࡝࡜ࠧࠫࡰࡪࡼࡥ࡭ࡰࡤࡱࡪ࠯ࡳ࡞ࠢ࠰ࠤࡠࠦࡓࡅࡍ࠰ࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠠ࡞ࠢࠨࠬࡲ࡫ࡳࡴࡣࡪࡩ࠮ࡹࠧỺ"),
      datefmt=bstack1l1111_opy_ (u"࡛ࠧࠦ࠰ࠩࡲ࠳ࠥࡥࡖࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࡞ࠬỻ"),
    )
    bstack1111l11lll1_opy_.setFormatter(bstack1111l1lll11_opy_)
    bstack1111l11lll1_opy_.setLevel(level)
    bstack1111l11lll1_opy_.addFilter(lambda r: r.name != bstack1l1111_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷ࠴ࡲࡦ࡯ࡲࡸࡪ࠴ࡲࡦ࡯ࡲࡸࡪࡥࡣࡰࡰࡱࡩࡨࡺࡩࡰࡰࠪỼ"))
    logger.addHandler(bstack1111l11lll1_opy_)
    logger.setLevel(level)
    logger.propagate = False
  return logger
def bstack1ll11l1l111_opy_():
  bstack1111l11ll1l_opy_ = os.environ.get(bstack1l1111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡆࡈࡆ࡚ࡍࠢỽ"), bstack1l1111_opy_ (u"ࠥࡪࡦࡲࡳࡦࠤỾ"))
  return logging.DEBUG if bstack1111l11ll1l_opy_.lower() == bstack1l1111_opy_ (u"ࠦࡹࡸࡵࡦࠤỿ") else logging.INFO
def bstack1l11lllll11_opy_():
  global bstack1111l1l111l_opy_
  if os.path.exists(bstack1111l1l111l_opy_):
    os.remove(bstack1111l1l111l_opy_)
  if os.path.exists(bstack1111l11ll11_opy_):
    os.remove(bstack1111l11ll11_opy_)
def bstack1111ll1ll_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def configure_logger(config, log_level):
  bstack1111l1l11l1_opy_ = log_level
  if bstack1l1111_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧἀ") in config and config[bstack1l1111_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨἁ")] in bstack11l11l11l1l_opy_:
    bstack1111l1l11l1_opy_ = bstack11l11l11l1l_opy_[config[bstack1l1111_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩἂ")]]
  if config.get(bstack1l1111_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪἃ"), False):
    logging.getLogger().setLevel(bstack1111l1l11l1_opy_)
    return bstack1111l1l11l1_opy_
  global bstack1111l1l111l_opy_
  bstack1111ll1ll_opy_()
  bstack1111l11llll_opy_ = logging.Formatter(
    fmt=bstack1l1111_opy_ (u"ࠩࠨࠬࡦࡹࡣࡵ࡫ࡰࡩ࠮ࡹࠠ࡜ࠧࠫࡲࡦࡳࡥࠪࡵࡠ࡟ࠪ࠮࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠫࡶࡡࠥ࠳ࠠࠦࠪࡰࡩࡸࡹࡡࡨࡧࠬࡷࠬἄ"),
    datefmt=bstack1l1111_opy_ (u"ࠪࠩ࡞࠳ࠥ࡮࠯ࠨࡨ࡙ࠫࡈ࠻ࠧࡐ࠾࡙࡚ࠪࠨἅ"),
  )
  bstack1111ll111l1_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1111l1l111l_opy_)
  file_handler.setFormatter(bstack1111l11llll_opy_)
  bstack1111ll111l1_opy_.setFormatter(bstack1111l11llll_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1111ll111l1_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1l1111_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳ࠰ࡵࡩࡲࡵࡴࡦ࠰ࡵࡩࡲࡵࡴࡦࡡࡦࡳࡳࡴࡥࡤࡶ࡬ࡳࡳ࠭ἆ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1111ll111l1_opy_.setLevel(bstack1111l1l11l1_opy_)
  logging.getLogger().addHandler(bstack1111ll111l1_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1111l1l11l1_opy_
def bstack1111l11l1l1_opy_(config):
  try:
    bstack1111ll11l11_opy_ = set(bstack11l11111l1l_opy_)
    bstack1111l1l1lll_opy_ = bstack1l1111_opy_ (u"ࠬ࠭ἇ")
    with open(bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩἈ")) as bstack1111ll11111_opy_:
      bstack1111l1ll111_opy_ = bstack1111ll11111_opy_.read()
      bstack1111l1l1lll_opy_ = re.sub(bstack1l1111_opy_ (u"ࡲࠨࡠࠫࡠࡸ࠱ࠩࡀࠥ࠱࠮ࠩࡢ࡮ࠨἉ"), bstack1l1111_opy_ (u"ࠨࠩἊ"), bstack1111l1ll111_opy_, flags=re.M)
      bstack1111l1l1lll_opy_ = re.sub(
        bstack1l1111_opy_ (u"ࡴࠪࡢ࠭ࡢࡳࠬࠫࡂࠬࠬἋ") + bstack1l1111_opy_ (u"ࠪࢀࠬἌ").join(bstack1111ll11l11_opy_) + bstack1l1111_opy_ (u"ࠫ࠮࠴ࠪࠥࠩἍ"),
        bstack1l1111_opy_ (u"ࡷ࠭࡜࠳࠼ࠣ࡟ࡗࡋࡄࡂࡅࡗࡉࡉࡣࠧἎ"),
        bstack1111l1l1lll_opy_, flags=re.M | re.I
      )
    def bstack1111l11l1ll_opy_(dic):
      bstack1111l1l11ll_opy_ = {}
      for key, value in dic.items():
        if key in bstack1111ll11l11_opy_:
          bstack1111l1l11ll_opy_[key] = bstack1l1111_opy_ (u"࡛࠭ࡓࡇࡇࡅࡈ࡚ࡅࡅ࡟ࠪἏ")
        else:
          if isinstance(value, dict):
            bstack1111l1l11ll_opy_[key] = bstack1111l11l1ll_opy_(value)
          else:
            bstack1111l1l11ll_opy_[key] = value
      return bstack1111l1l11ll_opy_
    bstack1111l1l11ll_opy_ = bstack1111l11l1ll_opy_(config)
    return {
      bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪἐ"): bstack1111l1l1lll_opy_,
      bstack1l1111_opy_ (u"ࠨࡨ࡬ࡲࡦࡲࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫἑ"): json.dumps(bstack1111l1l11ll_opy_)
    }
  except Exception as e:
    return {}
def bstack1111l1l1l11_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack1l1111_opy_ (u"ࠩ࡯ࡳ࡬࠭ἒ"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack1111l1l1111_opy_ = os.path.join(log_dir, bstack1l1111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶࠫἓ"))
  if not os.path.exists(bstack1111l1l1111_opy_):
    bstack1111l1llll1_opy_ = {
      bstack1l1111_opy_ (u"ࠦ࡮ࡴࡩࡱࡣࡷ࡬ࠧἔ"): str(inipath),
      bstack1l1111_opy_ (u"ࠧࡸ࡯ࡰࡶࡳࡥࡹ࡮ࠢἕ"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack1l1111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡣࡰࡰࡩ࡭࡬ࡹ࠮࡫ࡵࡲࡲࠬ἖")), bstack1l1111_opy_ (u"ࠧࡸࠩ἗")) as bstack1111l1l1ll1_opy_:
      bstack1111l1l1ll1_opy_.write(json.dumps(bstack1111l1llll1_opy_))
def bstack1111l1ll1l1_opy_():
  try:
    bstack1111l1l1111_opy_ = os.path.join(os.getcwd(), bstack1l1111_opy_ (u"ࠨ࡮ࡲ࡫ࠬἘ"), bstack1l1111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡦࡳࡳ࡬ࡩࡨࡵ࠱࡮ࡸࡵ࡮ࠨἙ"))
    if os.path.exists(bstack1111l1l1111_opy_):
      with open(bstack1111l1l1111_opy_, bstack1l1111_opy_ (u"ࠪࡶࠬἚ")) as bstack1111l1l1ll1_opy_:
        bstack1111l1lllll_opy_ = json.load(bstack1111l1l1ll1_opy_)
      return bstack1111l1lllll_opy_.get(bstack1l1111_opy_ (u"ࠫ࡮ࡴࡩࡱࡣࡷ࡬ࠬἛ"), bstack1l1111_opy_ (u"ࠬ࠭Ἔ")), bstack1111l1lllll_opy_.get(bstack1l1111_opy_ (u"࠭ࡲࡰࡱࡷࡴࡦࡺࡨࠨἝ"), bstack1l1111_opy_ (u"ࠧࠨ἞"))
  except:
    pass
  return None, None
def bstack1111l1l1l1l_opy_():
  try:
    bstack1111l1l1111_opy_ = os.path.join(os.getcwd(), bstack1l1111_opy_ (u"ࠨ࡮ࡲ࡫ࠬ἟"), bstack1l1111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡦࡳࡳ࡬ࡩࡨࡵ࠱࡮ࡸࡵ࡮ࠨἠ"))
    if os.path.exists(bstack1111l1l1111_opy_):
      os.remove(bstack1111l1l1111_opy_)
  except:
    pass
def bstack1l1111ll_opy_(config):
  try:
    try:
      from bstack_utils.bstack11l111111l_opy_ import bstack11ll111lll_opy_
    except Exception:
      bstack11ll111lll_opy_ = None
    start_time = time.time()
    from bstack_utils.helper import bstack1llllll11l_opy_, bstack11ll1l11_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack1111l1l111l_opy_
    if config.get(bstack1l1111_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬἡ"), False):
      return
    uuid = os.getenv(bstack1l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩἢ")) if os.getenv(bstack1l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪἣ")) else bstack1llllll11l_opy_.get_property(bstack1l1111_opy_ (u"ࠨࡳࡥ࡭ࡕࡹࡳࡏࡤࠣἤ"))
    if not uuid or uuid == bstack1l1111_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬἥ"):
      return
    bstack1111l1ll1ll_opy_ = bstack11ll111lll_opy_.bstack111llllll_opy_(EVENTS.bstack11l11l11111_opy_.value) if bstack11ll111lll_opy_ else None
    bstack1111ll1111l_opy_ = [bstack1l1111_opy_ (u"ࠨࡴࡨࡵࡺ࡯ࡲࡦ࡯ࡨࡲࡹࡹ࠮ࡵࡺࡷࠫἦ"), bstack1l1111_opy_ (u"ࠩࡓ࡭ࡵ࡬ࡩ࡭ࡧࠪἧ"), bstack1l1111_opy_ (u"ࠪࡴࡾࡶࡲࡰ࡬ࡨࡧࡹ࠴ࡴࡰ࡯࡯ࠫἨ"), bstack1111l1l111l_opy_, bstack1111l11ll11_opy_]
    bstack1111ll111ll_opy_, root_path = bstack1111l1ll1l1_opy_()
    if bstack1111ll111ll_opy_ != None:
      bstack1111ll1111l_opy_.append(bstack1111ll111ll_opy_)
    if root_path != None:
      bstack1111ll1111l_opy_.append(os.path.join(root_path, bstack1l1111_opy_ (u"ࠫࡨࡵ࡮ࡧࡶࡨࡷࡹ࠴ࡰࡺࠩἩ")))
    output_file = os.path.join(tempfile.gettempdir(), bstack1l1111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠲ࡲ࡯ࡨࡵ࠰ࠫἪ") + uuid + bstack1l1111_opy_ (u"࠭࠮ࡵࡣࡵ࠲࡬ࢀࠧἫ"))
    with tarfile.open(output_file, bstack1l1111_opy_ (u"ࠢࡸ࠼ࡪࡾࠧἬ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1111ll1111l_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1111l11l1l1_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1111ll11l1l_opy_ = data.encode()
        tarinfo.size = len(bstack1111ll11l1l_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1111ll11l1l_opy_))
    bstack1ll11l1111_opy_ = MultipartEncoder(
      fields= {
        bstack1l1111_opy_ (u"ࠨࡦࡤࡸࡦ࠭Ἥ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1l1111_opy_ (u"ࠩࡵࡦࠬἮ")), bstack1l1111_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰ࡺ࠰࡫ࡿ࡯ࡰࠨἯ")),
        bstack1l1111_opy_ (u"ࠫࡨࡲࡩࡦࡰࡷࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ἰ"): uuid
      }
    )
    bstack1111l1ll11l_opy_ = bstack11ll1l11_opy_(cli.config, [bstack1l1111_opy_ (u"ࠧࡧࡰࡪࡵࠥἱ"), bstack1l1111_opy_ (u"ࠨ࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࠨἲ"), bstack1l1111_opy_ (u"ࠢࡶࡲ࡯ࡳࡦࡪࠢἳ")], bstack11l111lll11_opy_)
    response = requests.post(
      bstack1l1111_opy_ (u"ࠣࡽࢀ࠳ࡨࡲࡩࡦࡰࡷ࠱ࡱࡵࡧࡴ࠱ࡸࡴࡱࡵࡡࡥࠤἴ").format(bstack1111l1ll11l_opy_),
      data=bstack1ll11l1111_opy_,
      headers={bstack1l1111_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨἵ"): bstack1ll11l1111_opy_.content_type},
      auth=(config[bstack1l1111_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬἶ")], config[bstack1l1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧἷ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1l1111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡺࡶ࡬ࡰࡣࡧࠤࡱࡵࡧࡴ࠼ࠣࠫἸ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1l1111_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥ࡯ࡦ࡬ࡲ࡬ࠦ࡬ࡰࡩࡶ࠾ࠬἹ") + str(e))
  finally:
    try:
      bstack1l11lllll11_opy_()
      bstack1111l1l1l1l_opy_()
    except:
      pass
    if bstack11ll111lll_opy_ and bstack1111l1ll1ll_opy_:
      bstack11ll111lll_opy_.end(EVENTS.bstack11l11l11111_opy_.value, bstack1111l1ll1ll_opy_ + bstack1l1111_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢἺ"), bstack1111l1ll1ll_opy_ + bstack1l1111_opy_ (u"ࠣ࠼ࡨࡲࡩࠨἻ"), status=True, failure=None, test_name=None)
    try:
      elapsed = time.time() - start_time
      get_logger().debug(bstack1l1111_opy_ (u"ࠤࡶࡩࡳࡪ࡟࡭ࡱࡪࡷࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠡ࡫ࡱࠤࢀࡀ࠮࠴ࡨࢀࠤࡸ࡫ࡣࡰࡰࡧࡷࠧἼ").format(elapsed))
    except Exception:
      pass