# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
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
from bstack_utils.constants import bstack111l1l11l11_opy_, EVENTS, bstack111l1ll1111_opy_, bstack111l1l1l11l_opy_, STAGE
import tempfile
import json
bstack1lllllll1lll_opy_ = os.getenv(bstack1111l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡍ࡟ࡇࡋࡏࡉࠧ⇐"), None) or os.path.join(tempfile.gettempdir(), bstack1111l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡩ࡫ࡢࡶࡩ࠱ࡰࡴ࡭ࠢ⇑"))
bstack1llllll1l111_opy_ = os.path.join(bstack1111l_opy_ (u"ࠨ࡬ࡰࡩࠥ⇒"), bstack1111l_opy_ (u"ࠧࡴࡦ࡮࠱ࡨࡲࡩ࠮ࡦࡨࡦࡺ࡭࠮࡭ࡱࡪࠫ⇓"))
_1lllllll1l11_opy_ = threading.Lock()
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1111l_opy_ (u"ࠨࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲ࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫ⇔"),
      datefmt=bstack1111l_opy_ (u"ࠩࠨ࡝࠲ࠫ࡭࠮ࠧࡧࡘࠪࡎ࠺ࠦࡏ࠽ࠩࡘࡠࠧ⇕"),
      stream=sys.stdout
    )
  return logger
def get_automation_logger(name=__name__, level=logging.DEBUG):
  bstack1111l_opy_ (u"ࠥࠦࠧࠐࠠࠡࡔࡨࡸࡺࡸ࡮ࡴࠢࡤࠤࡱࡵࡧࡨࡧࡵࠤࡹ࡮ࡡࡵࠢࡺࡶ࡮ࡺࡥࡴࠢࡲࡲࡱࡿࠠࡵࡱࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠮࡭ࡱࡪࠤ࡫࡯࡬ࡦࠌࠣࠤࡈࡸࡥࡢࡶࡨࡷࠥࡧ࡮ࡥࠢࡰࡥࡳࡧࡧࡦࡵࠣ࡭ࡹࡹࠠࡰࡹࡱࠤࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡨ࡬ࡰࡪࠦࡨࡢࡰࡧࡰࡪࡸࠊࠡࠢࡒࡲࡱࡿࠠࡦࡰࡤࡦࡱ࡫ࡳࠡ࡮ࡲ࡫࡬࡯࡮ࡨࠢ࡬ࡪࠥࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࡠࡎࡒࡋࡘࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷࠤࡻࡧࡲࡪࡣࡥࡰࡪࠦࡩࡴࠢࡶࡩࡹࠦࡴࡰࠢࡤࠤࡹࡸࡵࡵࡪࡼࠤࡻࡧ࡬ࡶࡧࠍࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࡰࡤࡱࡪࡀࠠࡍࡱࡪ࡫ࡪࡸࠠ࡯ࡣࡰࡩࠥ࠮ࡤࡦࡨࡤࡹࡱࡺࡳࠡࡶࡲࠤࡤࡥ࡮ࡢ࡯ࡨࡣࡤ࠯ࠊࠡࠢࠣࠤࡱ࡫ࡶࡦ࡮࠽ࠤࡑࡵࡧࡨ࡫ࡱ࡫ࠥࡲࡥࡷࡧ࡯ࠤ࠭ࡪࡥࡧࡣࡸࡰࡹࡹࠠࡵࡱࠣࡈࡊࡈࡕࡈࠫࠍࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࡱࡵࡧࡨ࡫ࡱ࡫࠳ࡒ࡯ࡨࡩࡨࡶ࠿ࠦࡃࡰࡰࡩ࡭࡬ࡻࡲࡦࡦࠣࡰࡴ࡭ࡧࡦࡴࠣࡸ࡭ࡧࡴࠡࡹࡵ࡭ࡹ࡫ࡳࠡࡱࡱࡰࡾࠦࡴࡰࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠴࡬ࡰࡩࠣࠬ࡮࡬ࠠࡦࡰࡤࡦࡱ࡫ࡤࠪࠌࠣࠤࠧࠨࠢ⇖")
  logger_name = bstack1111l_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠯ࡽ࠳ࢁࠧ⇗").format(name)
  logger = logging.getLogger(logger_name)
  is_enabled = os.getenv(bstack1111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࡠࡎࡒࡋࡘ࠭⇘"), bstack1111l_opy_ (u"࠭ࠧ⇙")).lower() == bstack1111l_opy_ (u"ࠧࡵࡴࡸࡩࠬ⇚")
  if not is_enabled:
    logger.setLevel(logging.CRITICAL)
    logger.propagate = False
    return logger
  with _1lllllll1l11_opy_:
    if logger.handlers:
      return logger
    bstack11111111111_opy_ = os.path.join(os.getcwd(), bstack1111l_opy_ (u"ࠨ࡮ࡲ࡫ࠬ⇛"), bstack1111l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠴࡬ࡰࡩࠪ⇜"))
    log_dir = os.path.dirname(bstack11111111111_opy_)
    if not os.path.exists(log_dir):
      os.makedirs(log_dir)
    bstack1llllll1ll11_opy_ = logging.FileHandler(bstack11111111111_opy_)
    bstack1llllllll1ll_opy_ = logging.Formatter(
      fmt=bstack1111l_opy_ (u"ࠪࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡ࡝ࠣࡗࡉࡑ࠭ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠤࡢࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫ⇝"),
      datefmt=bstack1111l_opy_ (u"ࠫࠪ࡟࠭ࠦ࡯࠰ࠩࡩ࡚ࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࡛ࠩ⇞"),
    )
    bstack1llllll1ll11_opy_.setFormatter(bstack1llllllll1ll_opy_)
    bstack1llllll1ll11_opy_.setLevel(level)
    bstack1llllll1ll11_opy_.addFilter(lambda r: r.name != bstack1111l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡶࡪࡳ࡯ࡵࡧ࠱ࡶࡪࡳ࡯ࡵࡧࡢࡧࡴࡴ࡮ࡦࡥࡷ࡭ࡴࡴࠧ⇟"))
    logger.addHandler(bstack1llllll1ll11_opy_)
    logger.setLevel(level)
    logger.propagate = False
  return logger
def get_log_level():
  bstack1llllll1l1ll_opy_ = os.environ.get(bstack1111l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡃࡕ࡝ࡤࡊࡅࡃࡗࡊࠦ⇠"), bstack1111l_opy_ (u"ࠢࡧࡣ࡯ࡷࡪࠨ⇡"))
  return logging.DEBUG if bstack1llllll1l1ll_opy_.lower() == bstack1111l_opy_ (u"ࠣࡶࡵࡹࡪࠨ⇢") else logging.INFO
def bstack1l111lll111_opy_():
  global bstack1lllllll1lll_opy_
  if os.path.exists(bstack1lllllll1lll_opy_):
    os.remove(bstack1lllllll1lll_opy_)
  if os.path.exists(bstack1llllll1l111_opy_):
    os.remove(bstack1llllll1l111_opy_)
def bstack11l1l1l1_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def configure_logger(config, log_level):
  bstack1llllll1lll1_opy_ = log_level
  if bstack1111l_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫ⇣") in config and config[bstack1111l_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬ⇤")] in bstack111l1ll1111_opy_:
    bstack1llllll1lll1_opy_ = bstack111l1ll1111_opy_[config[bstack1111l_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭⇥")]]
  if config.get(bstack1111l_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧ⇦"), False):
    logging.getLogger().setLevel(bstack1llllll1lll1_opy_)
    return bstack1llllll1lll1_opy_
  global bstack1lllllll1lll_opy_
  bstack11l1l1l1_opy_()
  bstack1lllllll1l1l_opy_ = logging.Formatter(
    fmt=bstack1111l_opy_ (u"࠭ࠥࠩࡣࡶࡧࡹ࡯࡭ࡦࠫࡶࠤࡠࠫࠨ࡯ࡣࡰࡩ࠮ࡹ࡝࡜ࠧࠫࡰࡪࡼࡥ࡭ࡰࡤࡱࡪ࠯ࡳ࡞ࠢ࠰ࠤࠪ࠮࡭ࡦࡵࡶࡥ࡬࡫ࠩࡴࠩ⇧"),
    datefmt=bstack1111l_opy_ (u"࡛ࠧࠦ࠰ࠩࡲ࠳ࠥࡥࡖࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࡞ࠬ⇨"),
  )
  bstack1llllll11ll1_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1lllllll1lll_opy_)
  file_handler.setFormatter(bstack1lllllll1l1l_opy_)
  bstack1llllll11ll1_opy_.setFormatter(bstack1lllllll1l1l_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1llllll11ll1_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1111l_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷ࠴ࡲࡦ࡯ࡲࡸࡪ࠴ࡲࡦ࡯ࡲࡸࡪࡥࡣࡰࡰࡱࡩࡨࡺࡩࡰࡰࠪ⇩"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1llllll11ll1_opy_.setLevel(bstack1llllll1lll1_opy_)
  logging.getLogger().addHandler(bstack1llllll11ll1_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1llllll1lll1_opy_
def bstack1llllll11lll_opy_(config):
  try:
    bstack1llllllllll1_opy_ = set(bstack111l1l1l11l_opy_)
    bstack1lllllllllll_opy_ = bstack1111l_opy_ (u"ࠩࠪ⇪")
    with open(bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭⇫")) as bstack1llllll1l11l_opy_:
      bstack1lllllllll11_opy_ = bstack1llllll1l11l_opy_.read()
      bstack1lllllllllll_opy_ = re.sub(bstack1111l_opy_ (u"ࡶࠬࡤࠨ࡝ࡵ࠮࠭ࡄࠩ࠮ࠫࠦ࡟ࡲࠬ⇬"), bstack1111l_opy_ (u"ࠬ࠭⇭"), bstack1lllllllll11_opy_, flags=re.M)
      bstack1lllllllllll_opy_ = re.sub(
        bstack1111l_opy_ (u"ࡸࠧ࡟ࠪ࡟ࡷ࠰࠯࠿ࠩࠩ⇮") + bstack1111l_opy_ (u"ࠧࡽࠩ⇯").join(bstack1llllllllll1_opy_) + bstack1111l_opy_ (u"ࠨࠫ࠱࠮ࠩ࠭⇰"),
        bstack1111l_opy_ (u"ࡴࠪࡠ࠷ࡀࠠ࡜ࡔࡈࡈࡆࡉࡔࡆࡆࡠࠫ⇱"),
        bstack1lllllllllll_opy_, flags=re.M | re.I
      )
    def bstack1lllllll11ll_opy_(dic):
      bstack1llllll1llll_opy_ = {}
      for key, value in dic.items():
        if key in bstack1llllllllll1_opy_:
          bstack1llllll1llll_opy_[key] = bstack1111l_opy_ (u"ࠪ࡟ࡗࡋࡄࡂࡅࡗࡉࡉࡣࠧ⇲")
        else:
          if isinstance(value, dict):
            bstack1llllll1llll_opy_[key] = bstack1lllllll11ll_opy_(value)
          else:
            bstack1llllll1llll_opy_[key] = value
      return bstack1llllll1llll_opy_
    bstack1llllll1llll_opy_ = bstack1lllllll11ll_opy_(config)
    return {
      bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧ⇳"): bstack1lllllllllll_opy_,
      bstack1111l_opy_ (u"ࠬ࡬ࡩ࡯ࡣ࡯ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨ⇴"): json.dumps(bstack1llllll1llll_opy_)
    }
  except Exception as e:
    return {}
def bstack1llllll11l11_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack1111l_opy_ (u"࠭࡬ࡰࡩࠪ⇵"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack1llll1l1ll1_opy_ = os.path.join(log_dir, bstack1111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡤࡱࡱࡪ࡮࡭ࡳࠨ⇶"))
  if not os.path.exists(bstack1llll1l1ll1_opy_):
    bstack1lllllllll1l_opy_ = {
      bstack1111l_opy_ (u"ࠣ࡫ࡱ࡭ࡵࡧࡴࡩࠤ⇷"): str(inipath),
      bstack1111l_opy_ (u"ࠤࡵࡳࡴࡺࡰࡢࡶ࡫ࠦ⇸"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack1111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶ࠲࡯ࡹ࡯࡯ࠩ⇹")), bstack1111l_opy_ (u"ࠫࡼ࠭⇺")) as bstack1llllll11l1l_opy_:
      bstack1llllll11l1l_opy_.write(json.dumps(bstack1lllllllll1l_opy_))
def bstack1llllllll11l_opy_():
  try:
    bstack1llll1l1ll1_opy_ = os.path.join(os.getcwd(), bstack1111l_opy_ (u"ࠬࡲ࡯ࡨࠩ⇻"), bstack1111l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡣࡰࡰࡩ࡭࡬ࡹ࠮࡫ࡵࡲࡲࠬ⇼"))
    if os.path.exists(bstack1llll1l1ll1_opy_):
      with open(bstack1llll1l1ll1_opy_, bstack1111l_opy_ (u"ࠧࡳࠩ⇽")) as bstack1llllll11l1l_opy_:
        bstack1lllllll111l_opy_ = json.load(bstack1llllll11l1l_opy_)
      return bstack1lllllll111l_opy_.get(bstack1111l_opy_ (u"ࠨ࡫ࡱ࡭ࡵࡧࡴࡩࠩ⇾"), bstack1111l_opy_ (u"ࠩࠪ⇿")), bstack1lllllll111l_opy_.get(bstack1111l_opy_ (u"ࠪࡶࡴࡵࡴࡱࡣࡷ࡬ࠬ∀"), bstack1111l_opy_ (u"ࠫࠬ∁"))
  except:
    pass
  return None, None
def bstack1llllll1ll1l_opy_():
  try:
    bstack1llll1l1ll1_opy_ = os.path.join(os.getcwd(), bstack1111l_opy_ (u"ࠬࡲ࡯ࡨࠩ∂"), bstack1111l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡣࡰࡰࡩ࡭࡬ࡹ࠮࡫ࡵࡲࡲࠬ∃"))
    if os.path.exists(bstack1llll1l1ll1_opy_):
      os.remove(bstack1llll1l1ll1_opy_)
  except:
    pass
def bstack1l1l1111l_opy_(config):
  try:
    try:
      from bstack_utils.bstack111l1l1ll1_opy_ import bstack1l11ll1l1_opy_
    except Exception:
      bstack1l11ll1l1_opy_ = None
    start_time = time.time()
    from bstack_utils.helper import global_config, bstack111l1lll1_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack1lllllll1lll_opy_
    if config.get(bstack1111l_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡷࡷࡳࡈࡧࡰࡵࡷࡵࡩࡑࡵࡧࡴࠩ∄"), False):
      return
    uuid = os.getenv(bstack1111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭∅")) if os.getenv(bstack1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ∆")) else global_config.get_property(bstack1111l_opy_ (u"ࠥࡷࡩࡱࡒࡶࡰࡌࡨࠧ∇"))
    if not uuid or uuid == bstack1111l_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ∈"):
      return
    bstack1lllllll11l1_opy_ = bstack1l11ll1l1_opy_.bstack11ll11l1ll_opy_(EVENTS.bstack111l1lll1l1_opy_.value) if bstack1l11ll1l1_opy_ else None
    bstack1llllllll1l1_opy_ = [bstack1111l_opy_ (u"ࠬࡸࡥࡲࡷ࡬ࡶࡪࡳࡥ࡯ࡶࡶ࠲ࡹࡾࡴࠨ∉"), bstack1111l_opy_ (u"࠭ࡐࡪࡲࡩ࡭ࡱ࡫ࠧ∊"), bstack1111l_opy_ (u"ࠧࡱࡻࡳࡶࡴࡰࡥࡤࡶ࠱ࡸࡴࡳ࡬ࠨ∋"), bstack1lllllll1lll_opy_, bstack1llllll1l111_opy_]
    bstack1llllll1l1l1_opy_, root_path = bstack1llllllll11l_opy_()
    if bstack1llllll1l1l1_opy_ != None:
      bstack1llllllll1l1_opy_.append(bstack1llllll1l1l1_opy_)
    if root_path != None:
      bstack1llllllll1l1_opy_.append(os.path.join(root_path, bstack1111l_opy_ (u"ࠨࡥࡲࡲ࡫ࡺࡥࡴࡶ࠱ࡴࡾ࠭∌")))
    bstack1lllllll1111_opy_ = os.path.join(os.getcwd(), bstack1111l_opy_ (u"ࠩ࡯ࡳ࡬࠭∍"), bstack1111l_opy_ (u"ࠪ࡯ࡪࡿ࠭࡮ࡧࡷࡶ࡮ࡩࡳ࠯࡬ࡶࡳࡳ࠭∎"))
    if os.path.exists(bstack1lllllll1111_opy_):
      bstack1llllllll1l1_opy_.append(bstack1lllllll1111_opy_)
    output_file = os.path.join(tempfile.gettempdir(), bstack1111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠱ࡱࡵࡧࡴ࠯ࠪ∏") + uuid + bstack1111l_opy_ (u"ࠬ࠴ࡴࡢࡴ࠱࡫ࡿ࠭∐"))
    with tarfile.open(output_file, bstack1111l_opy_ (u"ࠨࡷ࠻ࡩࡽࠦ∑")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1llllllll1l1_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1llllll11lll_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1llllllll111_opy_ = data.encode()
        tarinfo.size = len(bstack1llllllll111_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1llllllll111_opy_))
    multipart_data = MultipartEncoder(
      fields= {
        bstack1111l_opy_ (u"ࠧࡥࡣࡷࡥࠬ−"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1111l_opy_ (u"ࠨࡴࡥࠫ∓")), bstack1111l_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯ࡹ࠯ࡪࡾ࡮ࡶࠧ∔")),
        bstack1111l_opy_ (u"ࠪࡧࡱ࡯ࡥ࡯ࡶࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬ∕"): uuid
      }
    )
    bstack1lllllll1ll1_opy_ = bstack111l1lll1_opy_(cli.config, [bstack1111l_opy_ (u"ࠦࡦࡶࡩࡴࠤ∖"), bstack1111l_opy_ (u"ࠧࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠧ∗"), bstack1111l_opy_ (u"ࠨࡵࡱ࡮ࡲࡥࡩࠨ∘")], bstack111l1l11l11_opy_)
    response = requests.post(
      bstack1111l_opy_ (u"ࠢࡼࡿ࠲ࡧࡱ࡯ࡥ࡯ࡶ࠰ࡰࡴ࡭ࡳ࠰ࡷࡳࡰࡴࡧࡤࠣ∙").format(bstack1lllllll1ll1_opy_),
      data=multipart_data,
      headers={bstack1111l_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ√"): multipart_data.content_type},
      auth=(config[bstack1111l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ∛")], config[bstack1111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭∜")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1111l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡹࡵࡲ࡯ࡢࡦࠣࡰࡴ࡭ࡳ࠻ࠢࠪ∝") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1111l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥࡲ࡯ࡨࡵ࠽ࠫ∞") + str(e))
  finally:
    try:
      bstack1l111lll111_opy_()
      bstack1llllll1ll1l_opy_()
    except:
      pass
    if bstack1l11ll1l1_opy_ and bstack1lllllll11l1_opy_:
      bstack1l11ll1l1_opy_.end(EVENTS.bstack111l1lll1l1_opy_.value, bstack1lllllll11l1_opy_ + bstack1111l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ∟"), bstack1lllllll11l1_opy_ + bstack1111l_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ∠"), status=True, failure=None, test_name=None)
    try:
      elapsed = time.time() - start_time
      get_logger().debug(bstack1111l_opy_ (u"ࠣࡵࡨࡲࡩࡥ࡬ࡰࡩࡶࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࡪࠠࡪࡰࠣࡿ࠿࠴࠳ࡧࡿࠣࡷࡪࡩ࡯࡯ࡦࡶࠦ∡").format(elapsed))
    except Exception:
      pass