# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
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
from bstack_utils.constants import bstack11l111111ll_opy_, EVENTS, bstack11l111l11l1_opy_, bstack111llllll11_opy_, STAGE
import tempfile
import json
bstack1111l11l1ll_opy_ = os.getenv(bstack11lllll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡌࡥࡆࡊࡎࡈࠦἓ"), None) or os.path.join(tempfile.gettempdir(), bstack11lllll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡨࡪࡨࡵࡨ࠰࡯ࡳ࡬ࠨἔ"))
bstack1111l111111_opy_ = os.path.join(bstack11lllll_opy_ (u"ࠧࡲ࡯ࡨࠤἕ"), bstack11lllll_opy_ (u"࠭ࡳࡥ࡭࠰ࡧࡱ࡯࠭ࡥࡧࡥࡹ࡬࠴࡬ࡰࡩࠪ἖"))
_11111lllll1_opy_ = threading.Lock()
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack11lllll_opy_ (u"ࠧࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࠫࠨ࡮ࡧࡶࡷࡦ࡭ࡥࠪࡵࠪ἗"),
      datefmt=bstack11lllll_opy_ (u"ࠨࠧ࡜࠱ࠪࡳ࠭ࠦࡦࡗࠩࡍࡀࠥࡎ࠼ࠨࡗ࡟࠭Ἐ"),
      stream=sys.stdout
    )
  return logger
def bstack1l1l11111l_opy_(name=__name__, level=logging.DEBUG):
  bstack11lllll_opy_ (u"ࠤࠥࠦࠏࠦࠠࡓࡧࡷࡹࡷࡴࡳࠡࡣࠣࡰࡴ࡭ࡧࡦࡴࠣࡸ࡭ࡧࡴࠡࡹࡵ࡭ࡹ࡫ࡳࠡࡱࡱࡰࡾࠦࡴࡰࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠴࡬ࡰࡩࠣࡪ࡮ࡲࡥࠋࠢࠣࡇࡷ࡫ࡡࡵࡧࡶࠤࡦࡴࡤࠡ࡯ࡤࡲࡦ࡭ࡥࡴࠢ࡬ࡸࡸࠦ࡯ࡸࡰࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡧ࡫࡯ࡩࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࠐࠠࠡࡑࡱࡰࡾࠦࡥ࡯ࡣࡥࡰࡪࡹࠠ࡭ࡱࡪ࡫࡮ࡴࡧࠡ࡫ࡩࠤࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔ࡟ࡍࡑࡊࡗࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶࠣࡺࡦࡸࡩࡢࡤ࡯ࡩࠥ࡯ࡳࠡࡵࡨࡸࠥࡺ࡯ࠡࡣࠣࡸࡷࡻࡴࡩࡻࠣࡺࡦࡲࡵࡦࠌࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠ࡯ࡣࡰࡩ࠿ࠦࡌࡰࡩࡪࡩࡷࠦ࡮ࡢ࡯ࡨࠤ࠭ࡪࡥࡧࡣࡸࡰࡹࡹࠠࡵࡱࠣࡣࡤࡴࡡ࡮ࡧࡢࡣ࠮ࠐࠠࠡࠢࠣࡰࡪࡼࡥ࡭࠼ࠣࡐࡴ࡭ࡧࡪࡰࡪࠤࡱ࡫ࡶࡦ࡮ࠣࠬࡩ࡫ࡦࡢࡷ࡯ࡸࡸࠦࡴࡰࠢࡇࡉࡇ࡛ࡇࠪࠌࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࡰࡴ࡭ࡧࡪࡰࡪ࠲ࡑࡵࡧࡨࡧࡵ࠾ࠥࡉ࡯࡯ࡨ࡬࡫ࡺࡸࡥࡥࠢ࡯ࡳ࡬࡭ࡥࡳࠢࡷ࡬ࡦࡺࠠࡸࡴ࡬ࡸࡪࡹࠠࡰࡰ࡯ࡽࠥࡺ࡯ࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠳ࡲ࡯ࡨࠢࠫ࡭࡫ࠦࡥ࡯ࡣࡥࡰࡪࡪࠩࠋࠢࠣࠦࠧࠨἙ")
  logger_name = bstack11lllll_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠮ࡼ࠲ࢀࠦἚ").format(name)
  logger = logging.getLogger(logger_name)
  is_enabled = os.getenv(bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔ࡟ࡍࡑࡊࡗࠬἛ"), bstack11lllll_opy_ (u"ࠬ࠭Ἔ")).lower() == bstack11lllll_opy_ (u"࠭ࡴࡳࡷࡨࠫἝ")
  if not is_enabled:
    logger.setLevel(logging.CRITICAL)
    logger.propagate = False
    return logger
  with _11111lllll1_opy_:
    if logger.handlers:
      return logger
    bstack1111l11llll_opy_ = os.path.join(os.getcwd(), bstack11lllll_opy_ (u"ࠧ࡭ࡱࡪࠫ἞"), bstack11lllll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠳ࡲ࡯ࡨࠩ἟"))
    log_dir = os.path.dirname(bstack1111l11llll_opy_)
    if not os.path.exists(log_dir):
      os.makedirs(log_dir)
    bstack1111l1111l1_opy_ = logging.FileHandler(bstack1111l11llll_opy_)
    bstack1111l1ll111_opy_ = logging.Formatter(
      fmt=bstack11lllll_opy_ (u"ࠩࠨࠬࡦࡹࡣࡵ࡫ࡰࡩ࠮ࡹࠠ࡜ࠧࠫࡲࡦࡳࡥࠪࡵࡠ࡟ࠪ࠮࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠫࡶࡡࠥ࠳ࠠ࡜ࠢࡖࡈࡐ࠳ࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠣࡡࠥࠫࠨ࡮ࡧࡶࡷࡦ࡭ࡥࠪࡵࠪἠ"),
      datefmt=bstack11lllll_opy_ (u"ࠪࠩ࡞࠳ࠥ࡮࠯ࠨࡨ࡙ࠫࡈ࠻ࠧࡐ࠾࡙࡚ࠪࠨἡ"),
    )
    bstack1111l1111l1_opy_.setFormatter(bstack1111l1ll111_opy_)
    bstack1111l1111l1_opy_.setLevel(level)
    bstack1111l1111l1_opy_.addFilter(lambda r: r.name != bstack11lllll_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳ࠰ࡵࡩࡲࡵࡴࡦ࠰ࡵࡩࡲࡵࡴࡦࡡࡦࡳࡳࡴࡥࡤࡶ࡬ࡳࡳ࠭ἢ"))
    logger.addHandler(bstack1111l1111l1_opy_)
    logger.setLevel(level)
    logger.propagate = False
  return logger
def bstack1ll1ll1l1l1_opy_():
  bstack1111l11l111_opy_ = os.environ.get(bstack11lllll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡏࡎࡂࡔ࡜ࡣࡉࡋࡂࡖࡉࠥἣ"), bstack11lllll_opy_ (u"ࠨࡦࡢ࡮ࡶࡩࠧἤ"))
  return logging.DEBUG if bstack1111l11l111_opy_.lower() == bstack11lllll_opy_ (u"ࠢࡵࡴࡸࡩࠧἥ") else logging.INFO
def bstack1l1l11111l1_opy_():
  global bstack1111l11l1ll_opy_
  if os.path.exists(bstack1111l11l1ll_opy_):
    os.remove(bstack1111l11l1ll_opy_)
  if os.path.exists(bstack1111l111111_opy_):
    os.remove(bstack1111l111111_opy_)
def bstack1l1llllll_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def configure_logger(config, log_level):
  bstack1111l1ll11l_opy_ = log_level
  if bstack11lllll_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪἦ") in config and config[bstack11lllll_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫἧ")] in bstack11l111l11l1_opy_:
    bstack1111l1ll11l_opy_ = bstack11l111l11l1_opy_[config[bstack11lllll_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬἨ")]]
  if config.get(bstack11lllll_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭Ἡ"), False):
    logging.getLogger().setLevel(bstack1111l1ll11l_opy_)
    return bstack1111l1ll11l_opy_
  global bstack1111l11l1ll_opy_
  bstack1l1llllll_opy_()
  bstack1111l111l11_opy_ = logging.Formatter(
    fmt=bstack11lllll_opy_ (u"ࠬࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨἪ"),
    datefmt=bstack11lllll_opy_ (u"࡚࠭ࠥ࠯ࠨࡱ࠲ࠫࡤࡕࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࡝ࠫἫ"),
  )
  bstack11111llllll_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1111l11l1ll_opy_)
  file_handler.setFormatter(bstack1111l111l11_opy_)
  bstack11111llllll_opy_.setFormatter(bstack1111l111l11_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack11111llllll_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack11lllll_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࠰ࡺࡩࡧࡪࡲࡪࡸࡨࡶ࠳ࡸࡥ࡮ࡱࡷࡩ࠳ࡸࡥ࡮ࡱࡷࡩࡤࡩ࡯࡯ࡰࡨࡧࡹ࡯࡯࡯ࠩἬ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack11111llllll_opy_.setLevel(bstack1111l1ll11l_opy_)
  logging.getLogger().addHandler(bstack11111llllll_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1111l1ll11l_opy_
def bstack1111l1ll1ll_opy_(config):
  try:
    bstack1111l1l11ll_opy_ = set(bstack111llllll11_opy_)
    bstack1111l11l1l1_opy_ = bstack11lllll_opy_ (u"ࠨࠩἭ")
    with open(bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬἮ")) as bstack1111l1l1lll_opy_:
      bstack1111l111l1l_opy_ = bstack1111l1l1lll_opy_.read()
      bstack1111l11l1l1_opy_ = re.sub(bstack11lllll_opy_ (u"ࡵࠫࡣ࠮࡜ࡴ࠭ࠬࡃࠨ࠴ࠪࠥ࡞ࡱࠫἯ"), bstack11lllll_opy_ (u"ࠫࠬἰ"), bstack1111l111l1l_opy_, flags=re.M)
      bstack1111l11l1l1_opy_ = re.sub(
        bstack11lllll_opy_ (u"ࡷ࠭࡞ࠩ࡞ࡶ࠯࠮ࡅࠨࠨἱ") + bstack11lllll_opy_ (u"࠭ࡼࠨἲ").join(bstack1111l1l11ll_opy_) + bstack11lllll_opy_ (u"ࠧࠪ࠰࠭ࠨࠬἳ"),
        bstack11lllll_opy_ (u"ࡳࠩ࡟࠶࠿࡛ࠦࡓࡇࡇࡅࡈ࡚ࡅࡅ࡟ࠪἴ"),
        bstack1111l11l1l1_opy_, flags=re.M | re.I
      )
    def bstack1111l1l1ll1_opy_(dic):
      bstack1111l1l1l11_opy_ = {}
      for key, value in dic.items():
        if key in bstack1111l1l11ll_opy_:
          bstack1111l1l1l11_opy_[key] = bstack11lllll_opy_ (u"ࠩ࡞ࡖࡊࡊࡁࡄࡖࡈࡈࡢ࠭ἵ")
        else:
          if isinstance(value, dict):
            bstack1111l1l1l11_opy_[key] = bstack1111l1l1ll1_opy_(value)
          else:
            bstack1111l1l1l11_opy_[key] = value
      return bstack1111l1l1l11_opy_
    bstack1111l1l1l11_opy_ = bstack1111l1l1ll1_opy_(config)
    return {
      bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ἶ"): bstack1111l11l1l1_opy_,
      bstack11lllll_opy_ (u"ࠫ࡫࡯࡮ࡢ࡮ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧἷ"): json.dumps(bstack1111l1l1l11_opy_)
    }
  except Exception as e:
    return {}
def bstack1111l1111ll_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack11lllll_opy_ (u"ࠬࡲ࡯ࡨࠩἸ"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack1111l11lll1_opy_ = os.path.join(log_dir, bstack11lllll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡣࡰࡰࡩ࡭࡬ࡹࠧἹ"))
  if not os.path.exists(bstack1111l11lll1_opy_):
    bstack1111l11l11l_opy_ = {
      bstack11lllll_opy_ (u"ࠢࡪࡰ࡬ࡴࡦࡺࡨࠣἺ"): str(inipath),
      bstack11lllll_opy_ (u"ࠣࡴࡲࡳࡹࡶࡡࡵࡪࠥἻ"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack11lllll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡦࡳࡳ࡬ࡩࡨࡵ࠱࡮ࡸࡵ࡮ࠨἼ")), bstack11lllll_opy_ (u"ࠪࡻࠬἽ")) as bstack1111l111ll1_opy_:
      bstack1111l111ll1_opy_.write(json.dumps(bstack1111l11l11l_opy_))
def bstack1111l1l11l1_opy_():
  try:
    bstack1111l11lll1_opy_ = os.path.join(os.getcwd(), bstack11lllll_opy_ (u"ࠫࡱࡵࡧࠨἾ"), bstack11lllll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡩ࡯࡯ࡨ࡬࡫ࡸ࠴ࡪࡴࡱࡱࠫἿ"))
    if os.path.exists(bstack1111l11lll1_opy_):
      with open(bstack1111l11lll1_opy_, bstack11lllll_opy_ (u"࠭ࡲࠨὀ")) as bstack1111l111ll1_opy_:
        bstack1111l1l1l1l_opy_ = json.load(bstack1111l111ll1_opy_)
      return bstack1111l1l1l1l_opy_.get(bstack11lllll_opy_ (u"ࠧࡪࡰ࡬ࡴࡦࡺࡨࠨὁ"), bstack11lllll_opy_ (u"ࠨࠩὂ")), bstack1111l1l1l1l_opy_.get(bstack11lllll_opy_ (u"ࠩࡵࡳࡴࡺࡰࡢࡶ࡫ࠫὃ"), bstack11lllll_opy_ (u"ࠪࠫὄ"))
  except:
    pass
  return None, None
def bstack1111l11ll11_opy_():
  try:
    bstack1111l11lll1_opy_ = os.path.join(os.getcwd(), bstack11lllll_opy_ (u"ࠫࡱࡵࡧࠨὅ"), bstack11lllll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡩ࡯࡯ࡨ࡬࡫ࡸ࠴ࡪࡴࡱࡱࠫ὆"))
    if os.path.exists(bstack1111l11lll1_opy_):
      os.remove(bstack1111l11lll1_opy_)
  except:
    pass
def bstack1ll111l1ll_opy_(config):
  try:
    try:
      from bstack_utils.bstack11lll1l11l_opy_ import bstack1lll11l1ll_opy_
    except Exception:
      bstack1lll11l1ll_opy_ = None
    start_time = time.time()
    from bstack_utils.helper import bstack1l111111_opy_, bstack1lll1l111_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack1111l11l1ll_opy_
    if config.get(bstack11lllll_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨ὇"), False):
      return
    uuid = os.getenv(bstack11lllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬὈ")) if os.getenv(bstack11lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭Ὁ")) else bstack1l111111_opy_.get_property(bstack11lllll_opy_ (u"ࠤࡶࡨࡰࡘࡵ࡯ࡋࡧࠦὊ"))
    if not uuid or uuid == bstack11lllll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨὋ"):
      return
    bstack1111l1l1111_opy_ = bstack1lll11l1ll_opy_.bstack1llll1l1ll_opy_(EVENTS.bstack111llllllll_opy_.value) if bstack1lll11l1ll_opy_ else None
    bstack1111l1ll1l1_opy_ = [bstack11lllll_opy_ (u"ࠫࡷ࡫ࡱࡶ࡫ࡵࡩࡲ࡫࡮ࡵࡵ࠱ࡸࡽࡺࠧὌ"), bstack11lllll_opy_ (u"ࠬࡖࡩࡱࡨ࡬ࡰࡪ࠭Ὅ"), bstack11lllll_opy_ (u"࠭ࡰࡺࡲࡵࡳ࡯࡫ࡣࡵ࠰ࡷࡳࡲࡲࠧ὎"), bstack1111l11l1ll_opy_, bstack1111l111111_opy_]
    bstack1111l11ll1l_opy_, root_path = bstack1111l1l11l1_opy_()
    if bstack1111l11ll1l_opy_ != None:
      bstack1111l1ll1l1_opy_.append(bstack1111l11ll1l_opy_)
    if root_path != None:
      bstack1111l1ll1l1_opy_.append(os.path.join(root_path, bstack11lllll_opy_ (u"ࠧࡤࡱࡱࡪࡹ࡫ࡳࡵ࠰ࡳࡽࠬ὏")))
    bstack1111l1l111l_opy_ = os.path.join(os.getcwd(), bstack11lllll_opy_ (u"ࠨ࡮ࡲ࡫ࠬὐ"), bstack11lllll_opy_ (u"ࠩ࡮ࡩࡾ࠳࡭ࡦࡶࡵ࡭ࡨࡹ࠮࡫ࡵࡲࡲࠬὑ"))
    if os.path.exists(bstack1111l1l111l_opy_):
      bstack1111l1ll1l1_opy_.append(bstack1111l1l111l_opy_)
    output_file = os.path.join(tempfile.gettempdir(), bstack11lllll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠰ࡰࡴ࡭ࡳ࠮ࠩὒ") + uuid + bstack11lllll_opy_ (u"ࠫ࠳ࡺࡡࡳ࠰ࡪࡾࠬὓ"))
    with tarfile.open(output_file, bstack11lllll_opy_ (u"ࠧࡽ࠺ࡨࡼࠥὔ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1111l1ll1l1_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1111l1ll1ll_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1111l11111l_opy_ = data.encode()
        tarinfo.size = len(bstack1111l11111l_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1111l11111l_opy_))
    bstack1lll1111ll_opy_ = MultipartEncoder(
      fields= {
        bstack11lllll_opy_ (u"࠭ࡤࡢࡶࡤࠫὕ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack11lllll_opy_ (u"ࠧࡳࡤࠪὖ")), bstack11lllll_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡸ࠮ࡩࡽ࡭ࡵ࠭ὗ")),
        bstack11lllll_opy_ (u"ࠩࡦࡰ࡮࡫࡮ࡵࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ὘"): uuid
      }
    )
    bstack1111l111lll_opy_ = bstack1lll1l111_opy_(cli.config, [bstack11lllll_opy_ (u"ࠥࡥࡵ࡯ࡳࠣὙ"), bstack11lllll_opy_ (u"ࠦࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠦ὚"), bstack11lllll_opy_ (u"ࠧࡻࡰ࡭ࡱࡤࡨࠧὛ")], bstack11l111111ll_opy_)
    response = requests.post(
      bstack11lllll_opy_ (u"ࠨࡻࡾ࠱ࡦࡰ࡮࡫࡮ࡵ࠯࡯ࡳ࡬ࡹ࠯ࡶࡲ࡯ࡳࡦࡪࠢ὜").format(bstack1111l111lll_opy_),
      data=bstack1lll1111ll_opy_,
      headers={bstack11lllll_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭Ὕ"): bstack1lll1111ll_opy_.content_type},
      auth=(config[bstack11lllll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ὞")], config[bstack11lllll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬὟ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack11lllll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡸࡴࡱࡵࡡࡥࠢ࡯ࡳ࡬ࡹ࠺ࠡࠩὠ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack11lllll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡴࡤࡪࡰࡪࠤࡱࡵࡧࡴ࠼ࠪὡ") + str(e))
  finally:
    try:
      bstack1l1l11111l1_opy_()
      bstack1111l11ll11_opy_()
    except:
      pass
    if bstack1lll11l1ll_opy_ and bstack1111l1l1111_opy_:
      bstack1lll11l1ll_opy_.end(EVENTS.bstack111llllllll_opy_.value, bstack1111l1l1111_opy_ + bstack11lllll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧὢ"), bstack1111l1l1111_opy_ + bstack11lllll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦὣ"), status=True, failure=None, test_name=None)
    try:
      elapsed = time.time() - start_time
      get_logger().debug(bstack11lllll_opy_ (u"ࠢࡴࡧࡱࡨࡤࡲ࡯ࡨࡵࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࡩࠦࡩ࡯ࠢࡾ࠾࠳࠹ࡦࡾࠢࡶࡩࡨࡵ࡮ࡥࡵࠥὤ").format(elapsed))
    except Exception:
      pass