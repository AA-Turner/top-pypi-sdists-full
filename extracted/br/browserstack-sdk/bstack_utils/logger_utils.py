# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
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
from bstack_utils.constants import bstack11111l1llll_opy_, EVENTS, bstack111111lll1l_opy_, bstack111111lllll_opy_, STAGE
import tempfile
import json
bstack1lll1l11l1ll_opy_ = os.getenv(bstack1l1111l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡋࡤࡌࡉࡍࡇࠥ⑒"), None) or os.path.join(tempfile.gettempdir(), bstack1l1111l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡧࡩࡧࡻࡧ࠯࡮ࡲ࡫ࠧ⑓"))
bstack1lll1ll111l1_opy_ = os.path.join(bstack1l1111l_opy_ (u"ࠦࡱࡵࡧࠣ⑔"), bstack1l1111l_opy_ (u"ࠬࡹࡤ࡬࠯ࡦࡰ࡮࠳ࡤࡦࡤࡸ࡫࠳ࡲ࡯ࡨࠩ⑕"))
_1lll1l1l1l1l_opy_ = threading.Lock()
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1l1111l_opy_ (u"࠭ࠥࠩࡣࡶࡧࡹ࡯࡭ࡦࠫࡶࠤࡠࠫࠨ࡯ࡣࡰࡩ࠮ࡹ࡝࡜ࠧࠫࡰࡪࡼࡥ࡭ࡰࡤࡱࡪ࠯ࡳ࡞ࠢ࠰ࠤࠪ࠮࡭ࡦࡵࡶࡥ࡬࡫ࠩࡴࠩ⑖"),
      datefmt=bstack1l1111l_opy_ (u"࡛ࠧࠦ࠰ࠩࡲ࠳ࠥࡥࡖࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࡞ࠬ⑗"),
      stream=sys.stdout
    )
  return logger
def get_automation_logger(name=__name__, level=logging.DEBUG):
  bstack1l1111l_opy_ (u"ࠣࠤࠥࠎࠥࠦࡒࡦࡶࡸࡶࡳࡹࠠࡢࠢ࡯ࡳ࡬࡭ࡥࡳࠢࡷ࡬ࡦࡺࠠࡸࡴ࡬ࡸࡪࡹࠠࡰࡰ࡯ࡽࠥࡺ࡯ࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠳ࡲ࡯ࡨࠢࡩ࡭ࡱ࡫ࠊࠡࠢࡆࡶࡪࡧࡴࡦࡵࠣࡥࡳࡪࠠ࡮ࡣࡱࡥ࡬࡫ࡳࠡ࡫ࡷࡷࠥࡵࡷ࡯ࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡦࡪ࡮ࡨࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶࠏࠦࠠࡐࡰ࡯ࡽࠥ࡫࡮ࡢࡤ࡯ࡩࡸࠦ࡬ࡰࡩࡪ࡭ࡳ࡭ࠠࡪࡨࠣࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓࡥࡌࡐࡉࡖࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵࠢࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠤ࡮ࡹࠠࡴࡧࡷࠤࡹࡵࠠࡢࠢࡷࡶࡺࡺࡨࡺࠢࡹࡥࡱࡻࡥࠋࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦ࡮ࡢ࡯ࡨ࠾ࠥࡒ࡯ࡨࡩࡨࡶࠥࡴࡡ࡮ࡧࠣࠬࡩ࡫ࡦࡢࡷ࡯ࡸࡸࠦࡴࡰࠢࡢࡣࡳࡧ࡭ࡦࡡࡢ࠭ࠏࠦࠠࠡࠢ࡯ࡩࡻ࡫࡬࠻ࠢࡏࡳ࡬࡭ࡩ࡯ࡩࠣࡰࡪࡼࡥ࡭ࠢࠫࡨࡪ࡬ࡡࡶ࡮ࡷࡷࠥࡺ࡯ࠡࡆࡈࡆ࡚ࡍࠩࠋࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢ࡯ࡳ࡬࡭ࡩ࡯ࡩ࠱ࡐࡴ࡭ࡧࡦࡴ࠽ࠤࡈࡵ࡮ࡧ࡫ࡪࡹࡷ࡫ࡤࠡ࡮ࡲ࡫࡬࡫ࡲࠡࡶ࡫ࡥࡹࠦࡷࡳ࡫ࡷࡩࡸࠦ࡯࡯࡮ࡼࠤࡹࡵࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠲ࡱࡵࡧࠡࠪ࡬ࡪࠥ࡫࡮ࡢࡤ࡯ࡩࡩ࠯ࠊࠡࠢࠥࠦࠧ⑘")
  logger_name = bstack1l1111l_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠴ࡻ࠱ࡿࠥ⑙").format(name)
  logger = logging.getLogger(logger_name)
  is_enabled = os.getenv(bstack1l1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓࡥࡌࡐࡉࡖࠫ⑚"), bstack1l1111l_opy_ (u"ࠫࠬ⑛")).lower() == bstack1l1111l_opy_ (u"ࠬࡺࡲࡶࡧࠪ⑜")
  if not is_enabled:
    logger.setLevel(logging.CRITICAL)
    logger.propagate = False
    return logger
  with _1lll1l1l1l1l_opy_:
    if logger.handlers:
      return logger
    bstack1lll1l1ll1ll_opy_ = os.path.join(os.getcwd(), bstack1l1111l_opy_ (u"࠭࡬ࡰࡩࠪ⑝"), bstack1l1111l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠲ࡱࡵࡧࠨ⑞"))
    log_dir = os.path.dirname(bstack1lll1l1ll1ll_opy_)
    if not os.path.exists(log_dir):
      os.makedirs(log_dir)
    bstack1lll1l1ll1l1_opy_ = logging.FileHandler(bstack1lll1l1ll1ll_opy_)
    bstack1lll1l1l11ll_opy_ = logging.Formatter(
      fmt=bstack1l1111l_opy_ (u"ࠨࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲࡛ࠦࠡࡕࡇࡏ࠲ࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠢࡠࠤࠪ࠮࡭ࡦࡵࡶࡥ࡬࡫ࠩࡴࠩ⑟"),
      datefmt=bstack1l1111l_opy_ (u"ࠩࠨ࡝࠲ࠫ࡭࠮ࠧࡧࡘࠪࡎ࠺ࠦࡏ࠽ࠩࡘࡠࠧ①"),
    )
    bstack1lll1l1ll1l1_opy_.setFormatter(bstack1lll1l1l11ll_opy_)
    bstack1lll1l1ll1l1_opy_.setLevel(level)
    bstack1lll1l1ll1l1_opy_.addFilter(lambda r: r.name != bstack1l1111l_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲ࠯ࡴࡨࡱࡴࡺࡥ࠯ࡴࡨࡱࡴࡺࡥࡠࡥࡲࡲࡳ࡫ࡣࡵ࡫ࡲࡲࠬ②"))
    logger.addHandler(bstack1lll1l1ll1l1_opy_)
    logger.setLevel(level)
    logger.propagate = False
  return logger
def get_log_level():
  bstack1lll1l1lllll_opy_ = os.environ.get(bstack1l1111l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢࡈࡊࡈࡕࡈࠤ③"), bstack1l1111l_opy_ (u"ࠧ࡬ࡡ࡭ࡵࡨࠦ④"))
  return logging.DEBUG if bstack1lll1l1lllll_opy_.lower() == bstack1l1111l_opy_ (u"ࠨࡴࡳࡷࡨࠦ⑤") else logging.INFO
def bstack11ll1llll1l_opy_():
  global bstack1lll1l11l1ll_opy_
  if os.path.exists(bstack1lll1l11l1ll_opy_):
    os.remove(bstack1lll1l11l1ll_opy_)
  if os.path.exists(bstack1lll1ll111l1_opy_):
    os.remove(bstack1lll1ll111l1_opy_)
def bstack11l1lll1_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def configure_logger(config, log_level):
  bstack1lll1l11ll1l_opy_ = log_level
  if bstack1l1111l_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩ⑥") in config and config[bstack1l1111l_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪ⑦")] in bstack111111lll1l_opy_:
    bstack1lll1l11ll1l_opy_ = bstack111111lll1l_opy_[config[bstack1l1111l_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫ⑧")]]
  if config.get(bstack1l1111l_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬ⑨"), False):
    logging.getLogger().setLevel(bstack1lll1l11ll1l_opy_)
    return bstack1lll1l11ll1l_opy_
  global bstack1lll1l11l1ll_opy_
  bstack11l1lll1_opy_()
  bstack1lll1l11l11l_opy_ = logging.Formatter(
    fmt=bstack1l1111l_opy_ (u"ࠫࠪ࠮ࡡࡴࡥࡷ࡭ࡲ࡫ࠩࡴࠢ࡞ࠩ࠭ࡴࡡ࡮ࡧࠬࡷࡢࡡࠥࠩ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨ࠭ࡸࡣࠠ࠮ࠢࠨࠬࡲ࡫ࡳࡴࡣࡪࡩ࠮ࡹࠧ⑩"),
    datefmt=bstack1l1111l_opy_ (u"࡙ࠬࠫ࠮ࠧࡰ࠱ࠪࡪࡔࠦࡊ࠽ࠩࡒࡀࠥࡔ࡜ࠪ⑪"),
  )
  bstack1lll1ll11111_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1lll1l11l1ll_opy_)
  file_handler.setFormatter(bstack1lll1l11l11l_opy_)
  bstack1lll1ll11111_opy_.setFormatter(bstack1lll1l11l11l_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1lll1ll11111_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1l1111l_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠯ࡹࡨࡦࡩࡸࡩࡷࡧࡵ࠲ࡷ࡫࡭ࡰࡶࡨ࠲ࡷ࡫࡭ࡰࡶࡨࡣࡨࡵ࡮࡯ࡧࡦࡸ࡮ࡵ࡮ࠨ⑫"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1lll1ll11111_opy_.setLevel(bstack1lll1l11ll1l_opy_)
  logging.getLogger().addHandler(bstack1lll1ll11111_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1lll1l11ll1l_opy_
def bstack1lll1l1l1l11_opy_(config):
  try:
    bstack1lll1l1llll1_opy_ = set(bstack111111lllll_opy_)
    bstack1lll1l1lll1l_opy_ = bstack1l1111l_opy_ (u"ࠧࠨ⑬")
    with open(bstack1l1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫ⑭")) as bstack1lll1l1l111l_opy_:
      bstack1lll1l11l1l1_opy_ = bstack1lll1l1l111l_opy_.read()
      bstack1lll1l1lll1l_opy_ = re.sub(bstack1l1111l_opy_ (u"ࡴࠪࡢ࠭ࡢࡳࠬࠫࡂࠧ࠳࠰ࠤ࡝ࡰࠪ⑮"), bstack1l1111l_opy_ (u"ࠪࠫ⑯"), bstack1lll1l11l1l1_opy_, flags=re.M)
      bstack1lll1l1lll1l_opy_ = re.sub(
        bstack1l1111l_opy_ (u"ࡶࠬࡤࠨ࡝ࡵ࠮࠭ࡄ࠮ࠧ⑰") + bstack1l1111l_opy_ (u"ࠬࢂࠧ⑱").join(bstack1lll1l1llll1_opy_) + bstack1l1111l_opy_ (u"࠭ࠩ࠯ࠬࠧࠫ⑲"),
        bstack1l1111l_opy_ (u"ࡲࠨ࡞࠵࠾ࠥࡡࡒࡆࡆࡄࡇ࡙ࡋࡄ࡞ࠩ⑳"),
        bstack1lll1l1lll1l_opy_, flags=re.M | re.I
      )
    def bstack1lll1l111lll_opy_(dic):
      bstack1lll1l1l11l1_opy_ = {}
      for key, value in dic.items():
        if key in bstack1lll1l1llll1_opy_:
          bstack1lll1l1l11l1_opy_[key] = bstack1l1111l_opy_ (u"ࠨ࡝ࡕࡉࡉࡇࡃࡕࡇࡇࡡࠬ⑴")
        else:
          if isinstance(value, dict):
            bstack1lll1l1l11l1_opy_[key] = bstack1lll1l111lll_opy_(value)
          else:
            bstack1lll1l1l11l1_opy_[key] = value
      return bstack1lll1l1l11l1_opy_
    bstack1lll1l1l11l1_opy_ = bstack1lll1l111lll_opy_(config)
    return {
      bstack1l1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬ⑵"): bstack1lll1l1lll1l_opy_,
      bstack1l1111l_opy_ (u"ࠪࡪ࡮ࡴࡡ࡭ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭⑶"): json.dumps(bstack1lll1l1l11l1_opy_)
    }
  except Exception as e:
    return {}
def bstack1lll1l1ll11l_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack1l1111l_opy_ (u"ࠫࡱࡵࡧࠨ⑷"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack11l11ll11l_opy_ = os.path.join(log_dir, bstack1l1111l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡩ࡯࡯ࡨ࡬࡫ࡸ࠭⑸"))
  if not os.path.exists(bstack11l11ll11l_opy_):
    bstack1lll1l11l111_opy_ = {
      bstack1l1111l_opy_ (u"ࠨࡩ࡯࡫ࡳࡥࡹ࡮ࠢ⑹"): str(inipath),
      bstack1l1111l_opy_ (u"ࠢࡳࡱࡲࡸࡵࡧࡴࡩࠤ⑺"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack1l1111l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡥࡲࡲ࡫࡯ࡧࡴ࠰࡭ࡷࡴࡴࠧ⑻")), bstack1l1111l_opy_ (u"ࠩࡺࠫ⑼")) as bstack1lll1l111ll1_opy_:
      bstack1lll1l111ll1_opy_.write(json.dumps(bstack1lll1l11l111_opy_))
def bstack1lll1l1l1111_opy_():
  try:
    bstack11l11ll11l_opy_ = os.path.join(os.getcwd(), bstack1l1111l_opy_ (u"ࠪࡰࡴ࡭ࠧ⑽"), bstack1l1111l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷ࠳ࡰࡳࡰࡰࠪ⑾"))
    if os.path.exists(bstack11l11ll11l_opy_):
      with open(bstack11l11ll11l_opy_, bstack1l1111l_opy_ (u"ࠬࡸࠧ⑿")) as bstack1lll1l111ll1_opy_:
        bstack1lll1l1lll11_opy_ = json.load(bstack1lll1l111ll1_opy_)
      return bstack1lll1l1lll11_opy_.get(bstack1l1111l_opy_ (u"࠭ࡩ࡯࡫ࡳࡥࡹ࡮ࠧ⒀"), bstack1l1111l_opy_ (u"ࠧࠨ⒁")), bstack1lll1l1lll11_opy_.get(bstack1l1111l_opy_ (u"ࠨࡴࡲࡳࡹࡶࡡࡵࡪࠪ⒂"), bstack1l1111l_opy_ (u"ࠩࠪ⒃"))
  except:
    pass
  return None, None
def bstack1lll1l1l1ll1_opy_():
  try:
    bstack11l11ll11l_opy_ = os.path.join(os.getcwd(), bstack1l1111l_opy_ (u"ࠪࡰࡴ࡭ࠧ⒄"), bstack1l1111l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷ࠳ࡰࡳࡰࡰࠪ⒅"))
    if os.path.exists(bstack11l11ll11l_opy_):
      os.remove(bstack11l11ll11l_opy_)
  except:
    pass
def bstack11l1lllll_opy_(config):
  try:
    try:
      from bstack_utils.bstack11l11lll_opy_ import bstack11lll1111_opy_
    except Exception:
      bstack11lll1111_opy_ = None
    start_time = time.time()
    from bstack_utils.helper import global_config, bstack1ll11l111l_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack1lll1l11l1ll_opy_
    if config.get(bstack1l1111l_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧ⒆"), False):
      return
    uuid = os.getenv(bstack1l1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ⒇")) if os.getenv(bstack1l1111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ⒈")) else global_config.get_property(bstack1l1111l_opy_ (u"ࠣࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠥ⒉"))
    if not uuid or uuid == bstack1l1111l_opy_ (u"ࠩࡱࡹࡱࡲࠧ⒊"):
      return
    bstack1lll1l11ll11_opy_ = bstack11lll1111_opy_.bstack1l11l1ll_opy_(EVENTS.bstack111111ll111_opy_.value) if bstack11lll1111_opy_ else None
    bstack1lll1l11llll_opy_ = [bstack1l1111l_opy_ (u"ࠪࡶࡪࡷࡵࡪࡴࡨࡱࡪࡴࡴࡴ࠰ࡷࡼࡹ࠭⒋"), bstack1l1111l_opy_ (u"ࠫࡕ࡯ࡰࡧ࡫࡯ࡩࠬ⒌"), bstack1l1111l_opy_ (u"ࠬࡶࡹࡱࡴࡲ࡮ࡪࡩࡴ࠯ࡶࡲࡱࡱ࠭⒍"), bstack1lll1l11l1ll_opy_, bstack1lll1ll111l1_opy_]
    bstack1lll1l11lll1_opy_, root_path = bstack1lll1l1l1111_opy_()
    if bstack1lll1l11lll1_opy_ != None:
      bstack1lll1l11llll_opy_.append(bstack1lll1l11lll1_opy_)
    if root_path != None:
      bstack1lll1l11llll_opy_.append(os.path.join(root_path, bstack1l1111l_opy_ (u"࠭ࡣࡰࡰࡩࡸࡪࡹࡴ࠯ࡲࡼࠫ⒎")))
    bstack1lll1l1l1lll_opy_ = os.path.join(os.getcwd(), bstack1l1111l_opy_ (u"ࠧ࡭ࡱࡪࠫ⒏"), bstack1l1111l_opy_ (u"ࠨ࡭ࡨࡽ࠲ࡳࡥࡵࡴ࡬ࡧࡸ࠴ࡪࡴࡱࡱࠫ⒐"))
    if os.path.exists(bstack1lll1l1l1lll_opy_):
      bstack1lll1l11llll_opy_.append(bstack1lll1l1l1lll_opy_)
    output_file = os.path.join(tempfile.gettempdir(), bstack1l1111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠯࡯ࡳ࡬ࡹ࠭ࠨ⒑") + uuid + bstack1l1111l_opy_ (u"ࠪ࠲ࡹࡧࡲ࠯ࡩࡽࠫ⒒"))
    with tarfile.open(output_file, bstack1l1111l_opy_ (u"ࠦࡼࡀࡧࡻࠤ⒓")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1lll1l11llll_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1lll1l1l1l11_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1lll1l1ll111_opy_ = data.encode()
        tarinfo.size = len(bstack1lll1l1ll111_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1lll1l1ll111_opy_))
    multipart_data = MultipartEncoder(
      fields= {
        bstack1l1111l_opy_ (u"ࠬࡪࡡࡵࡣࠪ⒔"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1l1111l_opy_ (u"࠭ࡲࡣࠩ⒕")), bstack1l1111l_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡾ࠭ࡨࡼ࡬ࡴࠬ⒖")),
        bstack1l1111l_opy_ (u"ࠨࡥ࡯࡭ࡪࡴࡴࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ⒗"): uuid
      }
    )
    bstack1lll1ll1111l_opy_ = bstack1ll11l111l_opy_(cli.config, [bstack1l1111l_opy_ (u"ࠤࡤࡴ࡮ࡹࠢ⒘"), bstack1l1111l_opy_ (u"ࠥࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠥ⒙"), bstack1l1111l_opy_ (u"ࠦࡺࡶ࡬ࡰࡣࡧࠦ⒚")], bstack11111l1llll_opy_)
    response = requests.post(
      bstack1l1111l_opy_ (u"ࠧࢁࡽ࠰ࡥ࡯࡭ࡪࡴࡴ࠮࡮ࡲ࡫ࡸ࠵ࡵࡱ࡮ࡲࡥࡩࠨ⒛").format(bstack1lll1ll1111l_opy_),
      data=multipart_data,
      headers={bstack1l1111l_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬ⒜"): multipart_data.content_type},
      auth=(config[bstack1l1111l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ⒝")], config[bstack1l1111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ⒞")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1l1111l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡷࡳࡰࡴࡧࡤࠡ࡮ࡲ࡫ࡸࡀࠠࠨ⒟") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1l1111l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡩࡳࡪࡩ࡯ࡩࠣࡰࡴ࡭ࡳ࠻ࠩ⒠") + str(e))
  finally:
    try:
      bstack11ll1llll1l_opy_()
      bstack1lll1l1l1ll1_opy_()
    except:
      pass
    if bstack11lll1111_opy_ and bstack1lll1l11ll11_opy_:
      bstack11lll1111_opy_.end(EVENTS.bstack111111ll111_opy_.value, bstack1lll1l11ll11_opy_ + bstack1l1111l_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ⒡"), bstack1lll1l11ll11_opy_ + bstack1l1111l_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ⒢"), status=True, failure=None, test_name=None)
    try:
      elapsed = time.time() - start_time
      get_logger().debug(bstack1l1111l_opy_ (u"ࠨࡳࡦࡰࡧࡣࡱࡵࡧࡴࠢࡦࡳࡲࡶ࡬ࡦࡶࡨࡨࠥ࡯࡮ࠡࡽ࠽࠲࠸࡬ࡽࠡࡵࡨࡧࡴࡴࡤࡴࠤ⒣").format(elapsed))
    except Exception:
      pass