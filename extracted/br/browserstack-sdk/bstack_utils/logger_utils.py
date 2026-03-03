# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
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
from bstack_utils.constants import bstack111ll1llll1_opy_, EVENTS, bstack111lll111l1_opy_, bstack111ll1l1l11_opy_, STAGE
import tempfile
import json
bstack11111l11l1l_opy_ = os.getenv(bstack11ll111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡍ࡟ࡇࡋࡏࡉࠧῦ"), None) or os.path.join(tempfile.gettempdir(), bstack11ll111_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡩ࡫ࡢࡶࡩ࠱ࡰࡴ࡭ࠢῧ"))
bstack11111l111l1_opy_ = os.path.join(bstack11ll111_opy_ (u"ࠨ࡬ࡰࡩࠥῨ"), bstack11ll111_opy_ (u"ࠧࡴࡦ࡮࠱ࡨࡲࡩ࠮ࡦࡨࡦࡺ࡭࠮࡭ࡱࡪࠫῩ"))
_11111ll1ll1_opy_ = threading.Lock()
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack11ll111_opy_ (u"ࠨࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲ࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫῪ"),
      datefmt=bstack11ll111_opy_ (u"ࠩࠨ࡝࠲ࠫ࡭࠮ࠧࡧࡘࠪࡎ࠺ࠦࡏ࠽ࠩࡘࡠࠧΎ"),
      stream=sys.stdout
    )
  return logger
def bstack11l1l11ll_opy_(name=__name__, level=logging.DEBUG):
  bstack11ll111_opy_ (u"ࠥࠦࠧࠐࠠࠡࡔࡨࡸࡺࡸ࡮ࡴࠢࡤࠤࡱࡵࡧࡨࡧࡵࠤࡹ࡮ࡡࡵࠢࡺࡶ࡮ࡺࡥࡴࠢࡲࡲࡱࡿࠠࡵࡱࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠮࡭ࡱࡪࠤ࡫࡯࡬ࡦࠌࠣࠤࡈࡸࡥࡢࡶࡨࡷࠥࡧ࡮ࡥࠢࡰࡥࡳࡧࡧࡦࡵࠣ࡭ࡹࡹࠠࡰࡹࡱࠤࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡨ࡬ࡰࡪࠦࡨࡢࡰࡧࡰࡪࡸࠊࠡࠢࡒࡲࡱࡿࠠࡦࡰࡤࡦࡱ࡫ࡳࠡ࡮ࡲ࡫࡬࡯࡮ࡨࠢ࡬ࡪࠥࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࡠࡎࡒࡋࡘࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷࠤࡻࡧࡲࡪࡣࡥࡰࡪࠦࡩࡴࠢࡶࡩࡹࠦࡴࡰࠢࡤࠤࡹࡸࡵࡵࡪࡼࠤࡻࡧ࡬ࡶࡧࠍࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࡰࡤࡱࡪࡀࠠࡍࡱࡪ࡫ࡪࡸࠠ࡯ࡣࡰࡩࠥ࠮ࡤࡦࡨࡤࡹࡱࡺࡳࠡࡶࡲࠤࡤࡥ࡮ࡢ࡯ࡨࡣࡤ࠯ࠊࠡࠢࠣࠤࡱ࡫ࡶࡦ࡮࠽ࠤࡑࡵࡧࡨ࡫ࡱ࡫ࠥࡲࡥࡷࡧ࡯ࠤ࠭ࡪࡥࡧࡣࡸࡰࡹࡹࠠࡵࡱࠣࡈࡊࡈࡕࡈࠫࠍࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࡱࡵࡧࡨ࡫ࡱ࡫࠳ࡒ࡯ࡨࡩࡨࡶ࠿ࠦࡃࡰࡰࡩ࡭࡬ࡻࡲࡦࡦࠣࡰࡴ࡭ࡧࡦࡴࠣࡸ࡭ࡧࡴࠡࡹࡵ࡭ࡹ࡫ࡳࠡࡱࡱࡰࡾࠦࡴࡰࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠴࡬ࡰࡩࠣࠬ࡮࡬ࠠࡦࡰࡤࡦࡱ࡫ࡤࠪࠌࠣࠤࠧࠨࠢῬ")
  logger_name = bstack11ll111_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠯ࡽ࠳ࢁࠧ῭").format(name)
  logger = logging.getLogger(logger_name)
  is_enabled = os.getenv(bstack11ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࡠࡎࡒࡋࡘ࠭΅"), bstack11ll111_opy_ (u"࠭ࠧ`")).lower() == bstack11ll111_opy_ (u"ࠧࡵࡴࡸࡩࠬ῰")
  if not is_enabled:
    logger.setLevel(logging.CRITICAL)
    logger.propagate = False
    return logger
  with _11111ll1ll1_opy_:
    if logger.handlers:
      return logger
    bstack111111ll1l1_opy_ = os.path.join(os.getcwd(), bstack11ll111_opy_ (u"ࠨ࡮ࡲ࡫ࠬ῱"), bstack11ll111_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠴࡬ࡰࡩࠪῲ"))
    log_dir = os.path.dirname(bstack111111ll1l1_opy_)
    if not os.path.exists(log_dir):
      os.makedirs(log_dir)
    bstack111111llll1_opy_ = logging.FileHandler(bstack111111ll1l1_opy_)
    bstack11111l1ll11_opy_ = logging.Formatter(
      fmt=bstack11ll111_opy_ (u"ࠪࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡ࡝ࠣࡗࡉࡑ࠭ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠤࡢࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫῳ"),
      datefmt=bstack11ll111_opy_ (u"ࠫࠪ࡟࠭ࠦ࡯࠰ࠩࡩ࡚ࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࡛ࠩῴ"),
    )
    bstack111111llll1_opy_.setFormatter(bstack11111l1ll11_opy_)
    bstack111111llll1_opy_.setLevel(level)
    bstack111111llll1_opy_.addFilter(lambda r: r.name != bstack11ll111_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡶࡪࡳ࡯ࡵࡧ࠱ࡶࡪࡳ࡯ࡵࡧࡢࡧࡴࡴ࡮ࡦࡥࡷ࡭ࡴࡴࠧ῵"))
    logger.addHandler(bstack111111llll1_opy_)
    logger.setLevel(level)
    logger.propagate = False
  return logger
def bstack1ll1l11ll1l_opy_():
  bstack11111l11111_opy_ = os.environ.get(bstack11ll111_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡃࡕ࡝ࡤࡊࡅࡃࡗࡊࠦῶ"), bstack11ll111_opy_ (u"ࠢࡧࡣ࡯ࡷࡪࠨῷ"))
  return logging.DEBUG if bstack11111l11111_opy_.lower() == bstack11ll111_opy_ (u"ࠣࡶࡵࡹࡪࠨῸ") else logging.INFO
def bstack1l111llllll_opy_():
  global bstack11111l11l1l_opy_
  if os.path.exists(bstack11111l11l1l_opy_):
    os.remove(bstack11111l11l1l_opy_)
  if os.path.exists(bstack11111l111l1_opy_):
    os.remove(bstack11111l111l1_opy_)
def bstack11l1l111l_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def configure_logger(config, log_level):
  bstack11111l1l11l_opy_ = log_level
  if bstack11ll111_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫΌ") in config and config[bstack11ll111_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬῺ")] in bstack111lll111l1_opy_:
    bstack11111l1l11l_opy_ = bstack111lll111l1_opy_[config[bstack11ll111_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭Ώ")]]
  if config.get(bstack11ll111_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧῼ"), False):
    logging.getLogger().setLevel(bstack11111l1l11l_opy_)
    return bstack11111l1l11l_opy_
  global bstack11111l11l1l_opy_
  bstack11l1l111l_opy_()
  bstack11111l11l11_opy_ = logging.Formatter(
    fmt=bstack11ll111_opy_ (u"࠭ࠥࠩࡣࡶࡧࡹ࡯࡭ࡦࠫࡶࠤࡠࠫࠨ࡯ࡣࡰࡩ࠮ࡹ࡝࡜ࠧࠫࡰࡪࡼࡥ࡭ࡰࡤࡱࡪ࠯ࡳ࡞ࠢ࠰ࠤࠪ࠮࡭ࡦࡵࡶࡥ࡬࡫ࠩࡴࠩ´"),
    datefmt=bstack11ll111_opy_ (u"࡛ࠧࠦ࠰ࠩࡲ࠳ࠥࡥࡖࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࡞ࠬ῾"),
  )
  bstack11111l1llll_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack11111l11l1l_opy_)
  file_handler.setFormatter(bstack11111l11l11_opy_)
  bstack11111l1llll_opy_.setFormatter(bstack11111l11l11_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack11111l1llll_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack11ll111_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷ࠴ࡲࡦ࡯ࡲࡸࡪ࠴ࡲࡦ࡯ࡲࡸࡪࡥࡣࡰࡰࡱࡩࡨࡺࡩࡰࡰࠪ῿"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack11111l1llll_opy_.setLevel(bstack11111l1l11l_opy_)
  logging.getLogger().addHandler(bstack11111l1llll_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack11111l1l11l_opy_
def bstack11111ll11l1_opy_(config):
  try:
    bstack11111l11lll_opy_ = set(bstack111ll1l1l11_opy_)
    bstack11111ll1l11_opy_ = bstack11ll111_opy_ (u"ࠩࠪ ")
    with open(bstack11ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ ")) as bstack11111l1lll1_opy_:
      bstack11111ll11ll_opy_ = bstack11111l1lll1_opy_.read()
      bstack11111ll1l11_opy_ = re.sub(bstack11ll111_opy_ (u"ࡶࠬࡤࠨ࡝ࡵ࠮࠭ࡄࠩ࠮ࠫࠦ࡟ࡲࠬ "), bstack11ll111_opy_ (u"ࠬ࠭ "), bstack11111ll11ll_opy_, flags=re.M)
      bstack11111ll1l11_opy_ = re.sub(
        bstack11ll111_opy_ (u"ࡸࠧ࡟ࠪ࡟ࡷ࠰࠯࠿ࠩࠩ ") + bstack11ll111_opy_ (u"ࠧࡽࠩ ").join(bstack11111l11lll_opy_) + bstack11ll111_opy_ (u"ࠨࠫ࠱࠮ࠩ࠭ "),
        bstack11ll111_opy_ (u"ࡴࠪࡠ࠷ࡀࠠ࡜ࡔࡈࡈࡆࡉࡔࡆࡆࡠࠫ "),
        bstack11111ll1l11_opy_, flags=re.M | re.I
      )
    def bstack11111ll111l_opy_(dic):
      bstack111111lllll_opy_ = {}
      for key, value in dic.items():
        if key in bstack11111l11lll_opy_:
          bstack111111lllll_opy_[key] = bstack11ll111_opy_ (u"ࠪ࡟ࡗࡋࡄࡂࡅࡗࡉࡉࡣࠧ ")
        else:
          if isinstance(value, dict):
            bstack111111lllll_opy_[key] = bstack11111ll111l_opy_(value)
          else:
            bstack111111lllll_opy_[key] = value
      return bstack111111lllll_opy_
    bstack111111lllll_opy_ = bstack11111ll111l_opy_(config)
    return {
      bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧ "): bstack11111ll1l11_opy_,
      bstack11ll111_opy_ (u"ࠬ࡬ࡩ࡯ࡣ࡯ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨ "): json.dumps(bstack111111lllll_opy_)
    }
  except Exception as e:
    return {}
def bstack11111l1l1l1_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack11ll111_opy_ (u"࠭࡬ࡰࡩࠪ​"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack1lllll1lll1_opy_ = os.path.join(log_dir, bstack11ll111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡤࡱࡱࡪ࡮࡭ࡳࠨ‌"))
  if not os.path.exists(bstack1lllll1lll1_opy_):
    bstack111111lll1l_opy_ = {
      bstack11ll111_opy_ (u"ࠣ࡫ࡱ࡭ࡵࡧࡴࡩࠤ‍"): str(inipath),
      bstack11ll111_opy_ (u"ࠤࡵࡳࡴࡺࡰࡢࡶ࡫ࠦ‎"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack11ll111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶ࠲࡯ࡹ࡯࡯ࠩ‏")), bstack11ll111_opy_ (u"ࠫࡼ࠭‐")) as bstack11111l1111l_opy_:
      bstack11111l1111l_opy_.write(json.dumps(bstack111111lll1l_opy_))
def bstack11111l111ll_opy_():
  try:
    bstack1lllll1lll1_opy_ = os.path.join(os.getcwd(), bstack11ll111_opy_ (u"ࠬࡲ࡯ࡨࠩ‑"), bstack11ll111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡣࡰࡰࡩ࡭࡬ࡹ࠮࡫ࡵࡲࡲࠬ‒"))
    if os.path.exists(bstack1lllll1lll1_opy_):
      with open(bstack1lllll1lll1_opy_, bstack11ll111_opy_ (u"ࠧࡳࠩ–")) as bstack11111l1111l_opy_:
        bstack11111l1l111_opy_ = json.load(bstack11111l1111l_opy_)
      return bstack11111l1l111_opy_.get(bstack11ll111_opy_ (u"ࠨ࡫ࡱ࡭ࡵࡧࡴࡩࠩ—"), bstack11ll111_opy_ (u"ࠩࠪ―")), bstack11111l1l111_opy_.get(bstack11ll111_opy_ (u"ࠪࡶࡴࡵࡴࡱࡣࡷ࡬ࠬ‖"), bstack11ll111_opy_ (u"ࠫࠬ‗"))
  except:
    pass
  return None, None
def bstack11111l11ll1_opy_():
  try:
    bstack1lllll1lll1_opy_ = os.path.join(os.getcwd(), bstack11ll111_opy_ (u"ࠬࡲ࡯ࡨࠩ‘"), bstack11ll111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡣࡰࡰࡩ࡭࡬ࡹ࠮࡫ࡵࡲࡲࠬ’"))
    if os.path.exists(bstack1lllll1lll1_opy_):
      os.remove(bstack1lllll1lll1_opy_)
  except:
    pass
def bstack1ll11l1ll_opy_(config):
  try:
    try:
      from bstack_utils.bstack11111111l_opy_ import bstack1111l1l1l_opy_
    except Exception:
      bstack1111l1l1l_opy_ = None
    start_time = time.time()
    from bstack_utils.helper import global_config, bstack1llll1ll_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack11111l11l1l_opy_
    if config.get(bstack11ll111_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡷࡷࡳࡈࡧࡰࡵࡷࡵࡩࡑࡵࡧࡴࠩ‚"), False):
      return
    uuid = os.getenv(bstack11ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭‛")) if os.getenv(bstack11ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ“")) else global_config.get_property(bstack11ll111_opy_ (u"ࠥࡷࡩࡱࡒࡶࡰࡌࡨࠧ”"))
    if not uuid or uuid == bstack11ll111_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ„"):
      return
    bstack111111lll11_opy_ = bstack1111l1l1l_opy_.bstack1ll111l11_opy_(EVENTS.bstack111lll1ll1l_opy_.value) if bstack1111l1l1l_opy_ else None
    bstack11111l1ll1l_opy_ = [bstack11ll111_opy_ (u"ࠬࡸࡥࡲࡷ࡬ࡶࡪࡳࡥ࡯ࡶࡶ࠲ࡹࡾࡴࠨ‟"), bstack11ll111_opy_ (u"࠭ࡐࡪࡲࡩ࡭ࡱ࡫ࠧ†"), bstack11ll111_opy_ (u"ࠧࡱࡻࡳࡶࡴࡰࡥࡤࡶ࠱ࡸࡴࡳ࡬ࠨ‡"), bstack11111l11l1l_opy_, bstack11111l111l1_opy_]
    bstack11111ll1l1l_opy_, root_path = bstack11111l111ll_opy_()
    if bstack11111ll1l1l_opy_ != None:
      bstack11111l1ll1l_opy_.append(bstack11111ll1l1l_opy_)
    if root_path != None:
      bstack11111l1ll1l_opy_.append(os.path.join(root_path, bstack11ll111_opy_ (u"ࠨࡥࡲࡲ࡫ࡺࡥࡴࡶ࠱ࡴࡾ࠭•")))
    bstack11111ll1111_opy_ = os.path.join(os.getcwd(), bstack11ll111_opy_ (u"ࠩ࡯ࡳ࡬࠭‣"), bstack11ll111_opy_ (u"ࠪ࡯ࡪࡿ࠭࡮ࡧࡷࡶ࡮ࡩࡳ࠯࡬ࡶࡳࡳ࠭․"))
    if os.path.exists(bstack11111ll1111_opy_):
      bstack11111l1ll1l_opy_.append(bstack11111ll1111_opy_)
    output_file = os.path.join(tempfile.gettempdir(), bstack11ll111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠱ࡱࡵࡧࡴ࠯ࠪ‥") + uuid + bstack11ll111_opy_ (u"ࠬ࠴ࡴࡢࡴ࠱࡫ࡿ࠭…"))
    with tarfile.open(output_file, bstack11ll111_opy_ (u"ࠨࡷ࠻ࡩࡽࠦ‧")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack11111l1ll1l_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack11111ll11l1_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack111111ll1ll_opy_ = data.encode()
        tarinfo.size = len(bstack111111ll1ll_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack111111ll1ll_opy_))
    bstack11l1111l11_opy_ = MultipartEncoder(
      fields= {
        bstack11ll111_opy_ (u"ࠧࡥࡣࡷࡥࠬ "): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack11ll111_opy_ (u"ࠨࡴࡥࠫ ")), bstack11ll111_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯ࡹ࠯ࡪࡾ࡮ࡶࠧ‪")),
        bstack11ll111_opy_ (u"ࠪࡧࡱ࡯ࡥ࡯ࡶࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬ‫"): uuid
      }
    )
    bstack11111l1l1ll_opy_ = bstack1llll1ll_opy_(cli.config, [bstack11ll111_opy_ (u"ࠦࡦࡶࡩࡴࠤ‬"), bstack11ll111_opy_ (u"ࠧࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠧ‭"), bstack11ll111_opy_ (u"ࠨࡵࡱ࡮ࡲࡥࡩࠨ‮")], bstack111ll1llll1_opy_)
    response = requests.post(
      bstack11ll111_opy_ (u"ࠢࡼࡿ࠲ࡧࡱ࡯ࡥ࡯ࡶ࠰ࡰࡴ࡭ࡳ࠰ࡷࡳࡰࡴࡧࡤࠣ ").format(bstack11111l1l1ll_opy_),
      data=bstack11l1111l11_opy_,
      headers={bstack11ll111_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ‰"): bstack11l1111l11_opy_.content_type},
      auth=(config[bstack11ll111_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ‱")], config[bstack11ll111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭′")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack11ll111_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡹࡵࡲ࡯ࡢࡦࠣࡰࡴ࡭ࡳ࠻ࠢࠪ″") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack11ll111_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥࡲ࡯ࡨࡵ࠽ࠫ‴") + str(e))
  finally:
    try:
      bstack1l111llllll_opy_()
      bstack11111l11ll1_opy_()
    except:
      pass
    if bstack1111l1l1l_opy_ and bstack111111lll11_opy_:
      bstack1111l1l1l_opy_.end(EVENTS.bstack111lll1ll1l_opy_.value, bstack111111lll11_opy_ + bstack11ll111_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ‵"), bstack111111lll11_opy_ + bstack11ll111_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ‶"), status=True, failure=None, test_name=None)
    try:
      elapsed = time.time() - start_time
      get_logger().debug(bstack11ll111_opy_ (u"ࠣࡵࡨࡲࡩࡥ࡬ࡰࡩࡶࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࡪࠠࡪࡰࠣࡿ࠿࠴࠳ࡧࡿࠣࡷࡪࡩ࡯࡯ࡦࡶࠦ‷").format(elapsed))
    except Exception:
      pass