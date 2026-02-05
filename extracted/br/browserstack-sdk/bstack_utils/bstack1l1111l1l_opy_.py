# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
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
from bstack_utils.constants import bstack11l1111lll1_opy_, EVENTS, bstack11l11l11111_opy_, bstack11l111l11ll_opy_, STAGE
import tempfile
import json
bstack1111l1ll11l_opy_ = os.getenv(bstack11l1ll1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡈࡡࡉࡍࡑࡋࠢỳ"), None) or os.path.join(tempfile.gettempdir(), bstack11l1ll1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡤࡦࡤࡸ࡫࠳ࡲ࡯ࡨࠤỴ"))
bstack1111l11ll1l_opy_ = os.path.join(bstack11l1ll1_opy_ (u"ࠣ࡮ࡲ࡫ࠧỵ"), bstack11l1ll1_opy_ (u"ࠩࡶࡨࡰ࠳ࡣ࡭࡫࠰ࡨࡪࡨࡵࡨ࠰࡯ࡳ࡬࠭Ỷ"))
_1111l1lll11_opy_ = threading.Lock()
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack11l1ll1_opy_ (u"ࠪࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭ỷ"),
      datefmt=bstack11l1ll1_opy_ (u"ࠫࠪ࡟࠭ࠦ࡯࠰ࠩࡩ࡚ࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࡛ࠩỸ"),
      stream=sys.stdout
    )
  return logger
def bstack11l1111l11_opy_(name=__name__, level=logging.DEBUG):
  bstack11l1ll1_opy_ (u"ࠧࠨࠢࠋࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡦࠦ࡬ࡰࡩࡪࡩࡷࠦࡴࡩࡣࡷࠤࡼࡸࡩࡵࡧࡶࠤࡴࡴ࡬ࡺࠢࡷࡳࠥࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠰࡯ࡳ࡬ࠦࡦࡪ࡮ࡨࠎࠥࠦࡃࡳࡧࡤࡸࡪࡹࠠࡢࡰࡧࠤࡲࡧ࡮ࡢࡩࡨࡷࠥ࡯ࡴࡴࠢࡲࡻࡳࠦࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡪ࡮ࡲࡥࠡࡪࡤࡲࡩࡲࡥࡳࠌࠣࠤࡔࡴ࡬ࡺࠢࡨࡲࡦࡨ࡬ࡦࡵࠣࡰࡴ࡭ࡧࡪࡰࡪࠤ࡮࡬ࠠࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࡢࡐࡔࡍࡓࠡࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹࠦࡶࡢࡴ࡬ࡥࡧࡲࡥࠡ࡫ࡶࠤࡸ࡫ࡴࠡࡶࡲࠤࡦࠦࡴࡳࡷࡷ࡬ࡾࠦࡶࡢ࡮ࡸࡩࠏࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࡲࡦࡳࡥ࠻ࠢࡏࡳ࡬࡭ࡥࡳࠢࡱࡥࡲ࡫ࠠࠩࡦࡨࡪࡦࡻ࡬ࡵࡵࠣࡸࡴࠦ࡟ࡠࡰࡤࡱࡪࡥ࡟ࠪࠌࠣࠤࠥࠦ࡬ࡦࡸࡨࡰ࠿ࠦࡌࡰࡩࡪ࡭ࡳ࡭ࠠ࡭ࡧࡹࡩࡱࠦࠨࡥࡧࡩࡥࡺࡲࡴࡴࠢࡷࡳࠥࡊࡅࡃࡗࡊ࠭ࠏࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦ࡬ࡰࡩࡪ࡭ࡳ࡭࠮ࡍࡱࡪ࡫ࡪࡸ࠺ࠡࡅࡲࡲ࡫࡯ࡧࡶࡴࡨࡨࠥࡲ࡯ࡨࡩࡨࡶࠥࡺࡨࡢࡶࠣࡻࡷ࡯ࡴࡦࡵࠣࡳࡳࡲࡹࠡࡶࡲࠤࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠯࡮ࡲ࡫ࠥ࠮ࡩࡧࠢࡨࡲࡦࡨ࡬ࡦࡦࠬࠎࠥࠦࠢࠣࠤỹ")
  logger_name = bstack11l1ll1_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠱ࡿ࠵ࢃࠢỺ").format(name)
  logger = logging.getLogger(logger_name)
  is_enabled = os.getenv(bstack11l1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࡢࡐࡔࡍࡓࠨỻ"), bstack11l1ll1_opy_ (u"ࠨࠩỼ")).lower() == bstack11l1ll1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧỽ")
  if not is_enabled:
    logger.setLevel(logging.CRITICAL)
    logger.propagate = False
    return logger
  with _1111l1lll11_opy_:
    if logger.handlers:
      return logger
    bstack1111l11l11l_opy_ = os.path.join(os.getcwd(), bstack11l1ll1_opy_ (u"ࠪࡰࡴ࡭ࠧỾ"), bstack11l1ll1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠯࡮ࡲ࡫ࠬỿ"))
    log_dir = os.path.dirname(bstack1111l11l11l_opy_)
    if not os.path.exists(log_dir):
      os.makedirs(log_dir)
    bstack1111l11lll1_opy_ = logging.FileHandler(bstack1111l11l11l_opy_)
    bstack1111l11llll_opy_ = logging.Formatter(
      fmt=bstack11l1ll1_opy_ (u"ࠬࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣ࡟࡙ࠥࡄࡌ࠯ࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓࠦ࡝ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭ἀ"),
      datefmt=bstack11l1ll1_opy_ (u"࡚࠭ࠥ࠯ࠨࡱ࠲ࠫࡤࡕࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࡝ࠫἁ"),
    )
    bstack1111l11lll1_opy_.setFormatter(bstack1111l11llll_opy_)
    bstack1111l11lll1_opy_.setLevel(level)
    bstack1111l11lll1_opy_.addFilter(lambda r: r.name != bstack11l1ll1_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࠰ࡺࡩࡧࡪࡲࡪࡸࡨࡶ࠳ࡸࡥ࡮ࡱࡷࡩ࠳ࡸࡥ࡮ࡱࡷࡩࡤࡩ࡯࡯ࡰࡨࡧࡹ࡯࡯࡯ࠩἂ"))
    logger.addHandler(bstack1111l11lll1_opy_)
    logger.setLevel(level)
    logger.propagate = False
  return logger
def bstack1lll111l11l_opy_():
  bstack1111l111l1l_opy_ = os.environ.get(bstack11l1ll1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡅࡇࡅ࡙ࡌࠨἃ"), bstack11l1ll1_opy_ (u"ࠤࡩࡥࡱࡹࡥࠣἄ"))
  return logging.DEBUG if bstack1111l111l1l_opy_.lower() == bstack11l1ll1_opy_ (u"ࠥࡸࡷࡻࡥࠣἅ") else logging.INFO
def bstack1l11lll11ll_opy_():
  global bstack1111l1ll11l_opy_
  if os.path.exists(bstack1111l1ll11l_opy_):
    os.remove(bstack1111l1ll11l_opy_)
  if os.path.exists(bstack1111l11ll1l_opy_):
    os.remove(bstack1111l11ll1l_opy_)
def bstack11llllll1_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def configure_logger(config, log_level):
  bstack1111l1l1l1l_opy_ = log_level
  if bstack11l1ll1_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ἆ") in config and config[bstack11l1ll1_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧἇ")] in bstack11l11l11111_opy_:
    bstack1111l1l1l1l_opy_ = bstack11l11l11111_opy_[config[bstack11l1ll1_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨἈ")]]
  if config.get(bstack11l1ll1_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡷࡷࡳࡈࡧࡰࡵࡷࡵࡩࡑࡵࡧࡴࠩἉ"), False):
    logging.getLogger().setLevel(bstack1111l1l1l1l_opy_)
    return bstack1111l1l1l1l_opy_
  global bstack1111l1ll11l_opy_
  bstack11llllll1_opy_()
  bstack1111l1llll1_opy_ = logging.Formatter(
    fmt=bstack11l1ll1_opy_ (u"ࠨࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲ࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫἊ"),
    datefmt=bstack11l1ll1_opy_ (u"ࠩࠨ࡝࠲ࠫ࡭࠮ࠧࡧࡘࠪࡎ࠺ࠦࡏ࠽ࠩࡘࡠࠧἋ"),
  )
  bstack1111l1l1l11_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1111l1ll11l_opy_)
  file_handler.setFormatter(bstack1111l1llll1_opy_)
  bstack1111l1l1l11_opy_.setFormatter(bstack1111l1llll1_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1111l1l1l11_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack11l1ll1_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲ࠯ࡴࡨࡱࡴࡺࡥ࠯ࡴࡨࡱࡴࡺࡥࡠࡥࡲࡲࡳ࡫ࡣࡵ࡫ࡲࡲࠬἌ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1111l1l1l11_opy_.setLevel(bstack1111l1l1l1l_opy_)
  logging.getLogger().addHandler(bstack1111l1l1l11_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1111l1l1l1l_opy_
def bstack1111l111ll1_opy_(config):
  try:
    bstack1111l1l11l1_opy_ = set(bstack11l111l11ll_opy_)
    bstack1111l1l111l_opy_ = bstack11l1ll1_opy_ (u"ࠫࠬἍ")
    with open(bstack11l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨἎ")) as bstack1111l1ll111_opy_:
      bstack1111ll1111l_opy_ = bstack1111l1ll111_opy_.read()
      bstack1111l1l111l_opy_ = re.sub(bstack11l1ll1_opy_ (u"ࡸࠧ࡟ࠪ࡟ࡷ࠰࠯࠿ࠤ࠰࠭ࠨࡡࡴࠧἏ"), bstack11l1ll1_opy_ (u"ࠧࠨἐ"), bstack1111ll1111l_opy_, flags=re.M)
      bstack1111l1l111l_opy_ = re.sub(
        bstack11l1ll1_opy_ (u"ࡳࠩࡡࠬࡡࡹࠫࠪࡁࠫࠫἑ") + bstack11l1ll1_opy_ (u"ࠩࡿࠫἒ").join(bstack1111l1l11l1_opy_) + bstack11l1ll1_opy_ (u"ࠪ࠭࠳࠰ࠤࠨἓ"),
        bstack11l1ll1_opy_ (u"ࡶࠬࡢ࠲࠻ࠢ࡞ࡖࡊࡊࡁࡄࡖࡈࡈࡢ࠭ἔ"),
        bstack1111l1l111l_opy_, flags=re.M | re.I
      )
    def bstack1111l1l1lll_opy_(dic):
      bstack1111l1l1ll1_opy_ = {}
      for key, value in dic.items():
        if key in bstack1111l1l11l1_opy_:
          bstack1111l1l1ll1_opy_[key] = bstack11l1ll1_opy_ (u"ࠬࡡࡒࡆࡆࡄࡇ࡙ࡋࡄ࡞ࠩἕ")
        else:
          if isinstance(value, dict):
            bstack1111l1l1ll1_opy_[key] = bstack1111l1l1lll_opy_(value)
          else:
            bstack1111l1l1ll1_opy_[key] = value
      return bstack1111l1l1ll1_opy_
    bstack1111l1l1ll1_opy_ = bstack1111l1l1lll_opy_(config)
    return {
      bstack11l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩ἖"): bstack1111l1l111l_opy_,
      bstack11l1ll1_opy_ (u"ࠧࡧ࡫ࡱࡥࡱࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪ἗"): json.dumps(bstack1111l1l1ll1_opy_)
    }
  except Exception as e:
    return {}
def bstack1111l1ll1ll_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack11l1ll1_opy_ (u"ࠨ࡮ࡲ࡫ࠬἘ"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack1111l111lll_opy_ = os.path.join(log_dir, bstack11l1ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡦࡳࡳ࡬ࡩࡨࡵࠪἙ"))
  if not os.path.exists(bstack1111l111lll_opy_):
    bstack1111l11ll11_opy_ = {
      bstack11l1ll1_opy_ (u"ࠥ࡭ࡳ࡯ࡰࡢࡶ࡫ࠦἚ"): str(inipath),
      bstack11l1ll1_opy_ (u"ࠦࡷࡵ࡯ࡵࡲࡤࡸ࡭ࠨἛ"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack11l1ll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡩ࡯࡯ࡨ࡬࡫ࡸ࠴ࡪࡴࡱࡱࠫἜ")), bstack11l1ll1_opy_ (u"࠭ࡷࠨἝ")) as bstack1111l1ll1l1_opy_:
      bstack1111l1ll1l1_opy_.write(json.dumps(bstack1111l11ll11_opy_))
def bstack1111ll111l1_opy_():
  try:
    bstack1111l111lll_opy_ = os.path.join(os.getcwd(), bstack11l1ll1_opy_ (u"ࠧ࡭ࡱࡪࠫ἞"), bstack11l1ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡥࡲࡲ࡫࡯ࡧࡴ࠰࡭ࡷࡴࡴࠧ἟"))
    if os.path.exists(bstack1111l111lll_opy_):
      with open(bstack1111l111lll_opy_, bstack11l1ll1_opy_ (u"ࠩࡵࠫἠ")) as bstack1111l1ll1l1_opy_:
        bstack1111l1lll1l_opy_ = json.load(bstack1111l1ll1l1_opy_)
      return bstack1111l1lll1l_opy_.get(bstack11l1ll1_opy_ (u"ࠪ࡭ࡳ࡯ࡰࡢࡶ࡫ࠫἡ"), bstack11l1ll1_opy_ (u"ࠫࠬἢ")), bstack1111l1lll1l_opy_.get(bstack11l1ll1_opy_ (u"ࠬࡸ࡯ࡰࡶࡳࡥࡹ࡮ࠧἣ"), bstack11l1ll1_opy_ (u"࠭ࠧἤ"))
  except:
    pass
  return None, None
def bstack1111l11l111_opy_():
  try:
    bstack1111l111lll_opy_ = os.path.join(os.getcwd(), bstack11l1ll1_opy_ (u"ࠧ࡭ࡱࡪࠫἥ"), bstack11l1ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡥࡲࡲ࡫࡯ࡧࡴ࠰࡭ࡷࡴࡴࠧἦ"))
    if os.path.exists(bstack1111l111lll_opy_):
      os.remove(bstack1111l111lll_opy_)
  except:
    pass
def bstack1111llll1_opy_(config):
  try:
    try:
      from bstack_utils.bstack11ll1ll111_opy_ import bstack1ll1111ll_opy_
    except Exception:
      bstack1ll1111ll_opy_ = None
    start_time = time.time()
    from bstack_utils.helper import bstack11lll111l_opy_, bstack1lll1l111l_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack1111l1ll11l_opy_
    if config.get(bstack11l1ll1_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫἧ"), False):
      return
    uuid = os.getenv(bstack11l1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨἨ")) if os.getenv(bstack11l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩἩ")) else bstack11lll111l_opy_.get_property(bstack11l1ll1_opy_ (u"ࠧࡹࡤ࡬ࡔࡸࡲࡎࡪࠢἪ"))
    if not uuid or uuid == bstack11l1ll1_opy_ (u"࠭࡮ࡶ࡮࡯ࠫἫ"):
      return
    bstack1111l1l1111_opy_ = bstack1ll1111ll_opy_.bstack11l11l1l_opy_(EVENTS.bstack11l111l1l11_opy_.value) if bstack1ll1111ll_opy_ else None
    bstack1111l1l11ll_opy_ = [bstack11l1ll1_opy_ (u"ࠧࡳࡧࡴࡹ࡮ࡸࡥ࡮ࡧࡱࡸࡸ࠴ࡴࡹࡶࠪἬ"), bstack11l1ll1_opy_ (u"ࠨࡒ࡬ࡴ࡫࡯࡬ࡦࠩἭ"), bstack11l1ll1_opy_ (u"ࠩࡳࡽࡵࡸ࡯࡫ࡧࡦࡸ࠳ࡺ࡯࡮࡮ࠪἮ"), bstack1111l1ll11l_opy_, bstack1111l11ll1l_opy_]
    bstack1111l11l1l1_opy_, root_path = bstack1111ll111l1_opy_()
    if bstack1111l11l1l1_opy_ != None:
      bstack1111l1l11ll_opy_.append(bstack1111l11l1l1_opy_)
    if root_path != None:
      bstack1111l1l11ll_opy_.append(os.path.join(root_path, bstack11l1ll1_opy_ (u"ࠪࡧࡴࡴࡦࡵࡧࡶࡸ࠳ࡶࡹࠨἯ")))
    bstack1111l1lllll_opy_ = os.path.join(os.getcwd(), bstack11l1ll1_opy_ (u"ࠫࡱࡵࡧࠨἰ"), bstack11l1ll1_opy_ (u"ࠬࡱࡥࡺ࠯ࡰࡩࡹࡸࡩࡤࡵ࠱࡮ࡸࡵ࡮ࠨἱ"))
    if os.path.exists(bstack1111l1lllll_opy_):
      bstack1111l1l11ll_opy_.append(bstack1111l1lllll_opy_)
    output_file = os.path.join(tempfile.gettempdir(), bstack11l1ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࠳࡬ࡰࡩࡶ࠱ࠬἲ") + uuid + bstack11l1ll1_opy_ (u"ࠧ࠯ࡶࡤࡶ࠳࡭ࡺࠨἳ"))
    with tarfile.open(output_file, bstack11l1ll1_opy_ (u"ࠣࡹ࠽࡫ࡿࠨἴ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1111l1l11ll_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1111l111ll1_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1111ll11111_opy_ = data.encode()
        tarinfo.size = len(bstack1111ll11111_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1111ll11111_opy_))
    bstack1llll11l_opy_ = MultipartEncoder(
      fields= {
        bstack11l1ll1_opy_ (u"ࠩࡧࡥࡹࡧࠧἵ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack11l1ll1_opy_ (u"ࠪࡶࡧ࠭ἶ")), bstack11l1ll1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱ࡻ࠱࡬ࢀࡩࡱࠩἷ")),
        bstack11l1ll1_opy_ (u"ࠬࡩ࡬ࡪࡧࡱࡸࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧἸ"): uuid
      }
    )
    bstack1111l11l1ll_opy_ = bstack1lll1l111l_opy_(cli.config, [bstack11l1ll1_opy_ (u"ࠨࡡࡱ࡫ࡶࠦἹ"), bstack11l1ll1_opy_ (u"ࠢࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠢἺ"), bstack11l1ll1_opy_ (u"ࠣࡷࡳࡰࡴࡧࡤࠣἻ")], bstack11l1111lll1_opy_)
    response = requests.post(
      bstack11l1ll1_opy_ (u"ࠤࡾࢁ࠴ࡩ࡬ࡪࡧࡱࡸ࠲ࡲ࡯ࡨࡵ࠲ࡹࡵࡲ࡯ࡢࡦࠥἼ").format(bstack1111l11l1ll_opy_),
      data=bstack1llll11l_opy_,
      headers={bstack11l1ll1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩἽ"): bstack1llll11l_opy_.content_type},
      auth=(config[bstack11l1ll1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭Ἶ")], config[bstack11l1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨἿ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack11l1ll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡻࡰ࡭ࡱࡤࡨࠥࡲ࡯ࡨࡵ࠽ࠤࠬὀ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack11l1ll1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡰࡧ࡭ࡳ࡭ࠠ࡭ࡱࡪࡷ࠿࠭ὁ") + str(e))
  finally:
    try:
      bstack1l11lll11ll_opy_()
      bstack1111l11l111_opy_()
    except:
      pass
    if bstack1ll1111ll_opy_ and bstack1111l1l1111_opy_:
      bstack1ll1111ll_opy_.end(EVENTS.bstack11l111l1l11_opy_.value, bstack1111l1l1111_opy_ + bstack11l1ll1_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣὂ"), bstack1111l1l1111_opy_ + bstack11l1ll1_opy_ (u"ࠤ࠽ࡩࡳࡪࠢὃ"), status=True, failure=None, test_name=None)
    try:
      elapsed = time.time() - start_time
      get_logger().debug(bstack11l1ll1_opy_ (u"ࠥࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡸࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠢ࡬ࡲࠥࢁ࠺࠯࠵ࡩࢁࠥࡹࡥࡤࡱࡱࡨࡸࠨὄ").format(elapsed))
    except Exception:
      pass