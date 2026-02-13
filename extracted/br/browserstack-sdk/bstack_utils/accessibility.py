# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack11l11l1l11l_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack11l11ll1l11_opy_ as bstack11l11l1l1ll_opy_, EVENTS
from bstack_utils.bstack1l1lll111l_opy_ import bstack1l1lll111l_opy_
from bstack_utils.helper import bstack11l1lll11_opy_, bstack111111l11l_opy_, bstack1ll111l11_opy_, bstack11l11l11lll_opy_, \
  bstack11l111l1ll1_opy_, bstack11l1lllll1_opy_, get_host_info, bstack11l111ll1ll_opy_, bstack1l11l11ll1_opy_, error_handler, bstack11l111l1l11_opy_, bstack11l11ll11ll_opy_, bstack11ll11l11_opy_
from browserstack_sdk._version import __version__
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack11ll11ll1l_opy_ import bstack111l1lllll_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
from bstack_utils import logger_utils
logger = get_logger(__name__)
bstack111111l11_opy_ = logger_utils.bstack11llll1l11_opy_(__name__)
bstack11ll11ll1l_opy_ = bstack111l1lllll_opy_()
@error_handler(class_method=False)
def _11l111llll1_opy_(driver, bstack1llll11ll11_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack11l11_opy_ (u"ࠧࡰࡵࡢࡲࡦࡳࡥࠨ៴"): caps.get(bstack11l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧ៵"), None),
        bstack11l11_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭៶"): bstack1llll11ll11_opy_.get(bstack11l11_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭៷"), None),
        bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧࠪ៸"): caps.get(bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ៹"), None),
        bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ៺"): caps.get(bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ៻"), None)
    }
  except Exception as error:
    logger.debug(bstack11l11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩ࡫ࡴࡢ࡫࡯ࡷࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳࠢ࠽ࠤࠬ៼") + str(error))
  return response
def on():
    if os.environ.get(bstack11l11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ៽"), None) is None or os.environ[bstack11l11_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ៾")] == bstack11l11_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ៿"):
        return False
    return True
def bstack1lll1l1l1_opy_(config):
  return config.get(bstack11l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ᠀"), False) or any([p.get(bstack11l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭᠁"), False) == True for p in config.get(bstack11l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ᠂"), [])])
def bstack1llll1lll1_opy_(config, bstack11lllll1l1_opy_):
  try:
    bstack11l11l1l111_opy_ = config.get(bstack11l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ᠃"), False)
    if int(bstack11lllll1l1_opy_) < len(config.get(bstack11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ᠄"), [])) and config[bstack11l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭᠅")][bstack11lllll1l1_opy_]:
      bstack11l11l11l11_opy_ = config[bstack11l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ᠆")][bstack11lllll1l1_opy_].get(bstack11l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ᠇"), None)
    else:
      bstack11l11l11l11_opy_ = config.get(bstack11l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭᠈"), None)
    if bstack11l11l11l11_opy_ != None:
      bstack11l11l1l111_opy_ = bstack11l11l11l11_opy_
    bstack11l111ll111_opy_ = os.getenv(bstack11l11_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ᠉")) is not None and len(os.getenv(bstack11l11_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭᠊"))) > 0 and os.getenv(bstack11l11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ᠋")) != bstack11l11_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ᠌")
    return bstack11l11l1l111_opy_ and bstack11l111ll111_opy_
  except Exception as error:
    logger.debug(bstack11l11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡺࡪࡸࡩࡧࡻ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡪࡹࡳࡪࡱࡱࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲࠡ࠼ࠣࠫ᠍") + str(error))
  return False
def bstack11l11l1lll_opy_(test_tags):
  bstack1l1l1l11ll1_opy_ = os.getenv(bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭᠎"))
  if bstack1l1l1l11ll1_opy_ is None:
    return True
  bstack1l1l1l11ll1_opy_ = json.loads(bstack1l1l1l11ll1_opy_)
  try:
    include_tags = bstack1l1l1l11ll1_opy_[bstack11l11_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫ᠏")] if bstack11l11_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬ᠐") in bstack1l1l1l11ll1_opy_ and isinstance(bstack1l1l1l11ll1_opy_[bstack11l11_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭᠑")], list) else []
    exclude_tags = bstack1l1l1l11ll1_opy_[bstack11l11_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ᠒")] if bstack11l11_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨ᠓") in bstack1l1l1l11ll1_opy_ and isinstance(bstack1l1l1l11ll1_opy_[bstack11l11_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ᠔")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack11l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡺࡦࡲࡩࡥࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡥࡤࡲࡳ࡯࡮ࡨ࠰ࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠤࠧ᠕") + str(error))
  return False
def bstack11l111l11ll_opy_(config, bstack11l1111lll1_opy_, bstack11l11ll111l_opy_, bstack11l1111l1ll_opy_):
  bstack11l111l111l_opy_ = bstack11l11l11lll_opy_(config)
  bstack11l111lll11_opy_ = bstack11l111l1ll1_opy_(config)
  if bstack11l111l111l_opy_ is None or bstack11l111lll11_opy_ is None:
    logger.error(bstack11l11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࡍࡪࡵࡶ࡭ࡳ࡭ࠠࡢࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡࡶࡲ࡯ࡪࡴࠧ᠖"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ᠗"), bstack11l11_opy_ (u"ࠨࡽࢀࠫ᠘")))
    data = {
        bstack11l11_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ᠙"): config[bstack11l11_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ᠚")],
        bstack11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ᠛"): config.get(bstack11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ᠜"), os.path.basename(os.getcwd())),
        bstack11l11_opy_ (u"࠭ࡳࡵࡣࡵࡸ࡙࡯࡭ࡦࠩ᠝"): bstack11l1lll11_opy_(),
        bstack11l11_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬ᠞"): config.get(bstack11l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫ᠟"), bstack11l11_opy_ (u"ࠩࠪᠠ")),
        bstack11l11_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪᠡ"): {
            bstack11l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨࠫᠢ"): bstack11l1111lll1_opy_,
            bstack11l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᠣ"): bstack11l11ll111l_opy_,
            bstack11l11_opy_ (u"࠭ࡳࡥ࡭࡙ࡩࡷࡹࡩࡰࡰࠪᠤ"): __version__,
            bstack11l11_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩᠥ"): bstack11l11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨᠦ"),
            bstack11l11_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᠧ"): bstack11l11_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬᠨ"),
            bstack11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫᠩ"): bstack11l1111l1ll_opy_
        },
        bstack11l11_opy_ (u"ࠬࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧᠪ"): settings,
        bstack11l11_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࡃࡰࡰࡷࡶࡴࡲࠧᠫ"): bstack11l111ll1ll_opy_(),
        bstack11l11_opy_ (u"ࠧࡤ࡫ࡌࡲ࡫ࡵࠧᠬ"): bstack11l1lllll1_opy_(),
        bstack11l11_opy_ (u"ࠨࡪࡲࡷࡹࡏ࡮ࡧࡱࠪᠭ"): get_host_info(),
        bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᠮ"): bstack1ll111l11_opy_(config)
    }
    headers = {
        bstack11l11_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩᠯ"): bstack11l11_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧᠰ"),
    }
    config = {
        bstack11l11_opy_ (u"ࠬࡧࡵࡵࡪࠪᠱ"): (bstack11l111l111l_opy_, bstack11l111lll11_opy_),
        bstack11l11_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᠲ"): headers
    }
    response = bstack1l11l11ll1_opy_(bstack11l11_opy_ (u"ࠧࡑࡑࡖࡘࠬᠳ"), bstack11l11l1l1ll_opy_ + bstack11l11_opy_ (u"ࠨ࠱ࡹ࠶࠴ࡺࡥࡴࡶࡢࡶࡺࡴࡳࠨᠴ"), data, config)
    bstack11l11l11l1l_opy_ = response.json()
    if bstack11l11l11l1l_opy_[bstack11l11_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪᠵ")]:
      parsed = json.loads(os.getenv(bstack11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᠶ"), bstack11l11_opy_ (u"ࠫࢀࢃࠧᠷ")))
      parsed[bstack11l11_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᠸ")] = bstack11l11l11l1l_opy_[bstack11l11_opy_ (u"࠭ࡤࡢࡶࡤࠫᠹ")][bstack11l11_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᠺ")]
      os.environ[bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᠻ")] = json.dumps(parsed)
      bstack1l1lll111l_opy_.bstack1l111l111_opy_(bstack11l11l11l1l_opy_[bstack11l11_opy_ (u"ࠩࡧࡥࡹࡧࠧᠼ")][bstack11l11_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫᠽ")])
      bstack1l1lll111l_opy_.bstack11l1111ll1l_opy_(bstack11l11l11l1l_opy_[bstack11l11_opy_ (u"ࠫࡩࡧࡴࡢࠩᠾ")][bstack11l11_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧᠿ")])
      bstack1l1lll111l_opy_.store()
      return bstack11l11l11l1l_opy_[bstack11l11_opy_ (u"࠭ࡤࡢࡶࡤࠫᡀ")][bstack11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡔࡰ࡭ࡨࡲࠬᡁ")], bstack11l11l11l1l_opy_[bstack11l11_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᡂ")][bstack11l11_opy_ (u"ࠩ࡬ࡨࠬᡃ")]
    else:
      logger.error(bstack11l11_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࠫᡄ") + bstack11l11l11l1l_opy_[bstack11l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᡅ")])
      if bstack11l11l11l1l_opy_[bstack11l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᡆ")] == bstack11l11_opy_ (u"࠭ࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡱࡣࡶࡷࡪࡪ࠮ࠨᡇ"):
        for bstack11l111l1l1l_opy_ in bstack11l11l11l1l_opy_[bstack11l11_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧᡈ")]:
          logger.error(bstack11l111l1l1l_opy_[bstack11l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᡉ")])
      return None, None
  except Exception as error:
    logger.error(bstack11l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡷࡻ࡮ࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠻ࠢࠥᡊ") +  str(error))
    return None, None
def bstack11l11l11111_opy_():
  if os.getenv(bstack11l11_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᡋ")) is None:
    return {
        bstack11l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᡌ"): bstack11l11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᡍ"),
        bstack11l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᡎ"): bstack11l11_opy_ (u"ࠧࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡪࡤࡨࠥ࡬ࡡࡪ࡮ࡨࡨ࠳࠭ᡏ")
    }
  data = {bstack11l11_opy_ (u"ࠨࡧࡱࡨ࡙࡯࡭ࡦࠩᡐ"): bstack11l1lll11_opy_()}
  headers = {
      bstack11l11_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩᡑ"): bstack11l11_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࠫᡒ") + os.getenv(bstack11l11_opy_ (u"ࠦࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠤᡓ")),
      bstack11l11_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫᡔ"): bstack11l11_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩᡕ")
  }
  response = bstack1l11l11ll1_opy_(bstack11l11_opy_ (u"ࠧࡑࡗࡗࠫᡖ"), bstack11l11l1l1ll_opy_ + bstack11l11_opy_ (u"ࠨ࠱ࡷࡩࡸࡺ࡟ࡳࡷࡱࡷ࠴ࡹࡴࡰࡲࠪᡗ"), data, { bstack11l11_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪᡘ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack11l11_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡔࡦࡵࡷࠤࡗࡻ࡮ࠡ࡯ࡤࡶࡰ࡫ࡤࠡࡣࡶࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࡪࠠࡢࡶࠣࠦᡙ") + bstack111111l11l_opy_().isoformat() + bstack11l11_opy_ (u"ࠫ࡟࠭ᡚ"))
      return {bstack11l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᡛ"): bstack11l11_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧᡜ"), bstack11l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᡝ"): bstack11l11_opy_ (u"ࠨࠩᡞ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack11l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡯࡯࡯ࠢࡲࡪࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡖࡨࡷࡹࠦࡒࡶࡰ࠽ࠤࠧᡟ") + str(error))
    return {
        bstack11l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᡠ"): bstack11l11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᡡ"),
        bstack11l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᡢ"): str(error)
    }
def bstack11l111ll1l1_opy_(bstack11l11l111ll_opy_):
    return re.match(bstack11l11_opy_ (u"ࡸࠧ࡟࡞ࡧ࠯࠭ࡢ࠮࡝ࡦ࠮࠭ࡄࠪࠧᡣ"), bstack11l11l111ll_opy_.strip()) is not None
def bstack11l111l1l_opy_(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack11l11l11ll1_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11l11l11ll1_opy_ = desired_capabilities
        else:
          bstack11l11l11ll1_opy_ = {}
        bstack1l1l1lll1l1_opy_ = (bstack11l11l11ll1_opy_.get(bstack11l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ᡤ"), bstack11l11_opy_ (u"ࠨࠩᡥ")).lower() or caps.get(bstack11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨᡦ"), bstack11l11_opy_ (u"ࠪࠫᡧ")).lower())
        if bstack1l1l1lll1l1_opy_ == bstack11l11_opy_ (u"ࠫ࡮ࡵࡳࠨᡨ"):
            return True
        if bstack1l1l1lll1l1_opy_ == bstack11l11_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩ࠭ᡩ"):
            bstack1l1ll11ll1l_opy_ = str(float(caps.get(bstack11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᡪ")) or bstack11l11l11ll1_opy_.get(bstack11l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᡫ"), {}).get(bstack11l11_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫᡬ"),bstack11l11_opy_ (u"ࠩࠪᡭ"))))
            if bstack1l1l1lll1l1_opy_ == bstack11l11_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࠫᡮ") and int(bstack1l1ll11ll1l_opy_.split(bstack11l11_opy_ (u"ࠫ࠳࠭ᡯ"))[0]) < float(bstack11l111lll1l_opy_):
                logger.warning(str(bstack11l11l1ll1l_opy_))
                return False
            return True
        bstack1l1ll111l1l_opy_ = caps.get(bstack11l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᡰ"), {}).get(bstack11l11_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪᡱ"), caps.get(bstack11l11_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧᡲ"), bstack11l11_opy_ (u"ࠨࠩᡳ")))
        if bstack1l1ll111l1l_opy_:
            logger.warning(bstack11l11_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡇࡩࡸࡱࡴࡰࡲࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᡴ"))
            return False
        browser = caps.get(bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᡵ"), bstack11l11_opy_ (u"ࠫࠬᡶ")).lower() or bstack11l11l11ll1_opy_.get(bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᡷ"), bstack11l11_opy_ (u"࠭ࠧᡸ")).lower()
        if browser != bstack11l11_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ᡹"):
            logger.warning(bstack11l11_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦ᡺"))
            return False
        browser_version = caps.get(bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ᡻")) or caps.get(bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ᡼")) or bstack11l11l11ll1_opy_.get(bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᡽")) or bstack11l11l11ll1_opy_.get(bstack11l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭᡾"), {}).get(bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ᡿")) or bstack11l11l11ll1_opy_.get(bstack11l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᢀ"), {}).get(bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪᢁ"))
        bstack1l1ll111111_opy_ = bstack11l11l1l11l_opy_.bstack1l1l1ll111l_opy_
        bstack11l111l1111_opy_ = False
        if config is not None:
          bstack11l111l1111_opy_ = bstack11l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᢂ") in config and str(config[bstack11l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧᢃ")]).lower() != bstack11l11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪᢄ")
        if os.environ.get(bstack11l11_opy_ (u"ࠬࡏࡓࡠࡐࡒࡒࡤࡈࡓࡕࡃࡆࡏࡤࡏࡎࡇࡔࡄࡣࡆ࠷࠱࡚ࡡࡖࡉࡘ࡙ࡉࡐࡐࠪᢅ"), bstack11l11_opy_ (u"࠭ࠧᢆ")).lower() == bstack11l11_opy_ (u"ࠧࡵࡴࡸࡩࠬᢇ") or bstack11l111l1111_opy_:
          bstack1l1ll111111_opy_ = bstack11l11l1l11l_opy_.bstack1l1ll111lll_opy_
        if browser_version and browser_version != bstack11l11_opy_ (u"ࠨ࡮ࡤࡸࡪࡹࡴࠨᢈ") and int(browser_version.split(bstack11l11_opy_ (u"ࠩ࠱ࠫᢉ"))[0]) <= bstack1l1ll111111_opy_:
          logger.warning(bstack1ll1lllll11_opy_ (u"ࠪࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥ࡭ࡲࡦࡣࡷࡩࡷࠦࡴࡩࡣࡱࠤࢀࡳࡩ࡯ࡡࡤ࠵࠶ࡿ࡟ࡴࡷࡳࡴࡴࡸࡴࡦࡦࡢࡧ࡭ࡸ࡯࡮ࡧࡢࡺࡪࡸࡳࡪࡱࡱࢁ࠳࠭ᢊ"))
          return False
        if not options:
          bstack1l1ll11ll11_opy_ = caps.get(bstack11l11_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᢋ")) or bstack11l11l11ll1_opy_.get(bstack11l11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᢌ"), {})
          if bstack11l11_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࠪᢍ") in bstack1l1ll11ll11_opy_.get(bstack11l11_opy_ (u"ࠧࡢࡴࡪࡷࠬᢎ"), []):
              logger.warning(bstack11l11_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡲࡴࡺࠠࡳࡷࡱࠤࡴࡴࠠ࡭ࡧࡪࡥࡨࡿࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠡࡕࡺ࡭ࡹࡩࡨࠡࡶࡲࠤࡳ࡫ࡷࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥࠡࡱࡵࠤࡦࡼ࡯ࡪࡦࠣࡹࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠥᢏ"))
              return False
        return True
    except Exception as error:
        logger.debug(bstack11l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡸࡤࡰ࡮ࡪࡡࡵࡧࠣࡥ࠶࠷ࡹࠡࡵࡸࡴࡵࡵࡲࡵࠢ࠽ࠦᢐ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1ll1l11ll11_opy_ = config.get(bstack11l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᢑ"), {})
    bstack1ll1l11ll11_opy_[bstack11l11_opy_ (u"ࠫࡦࡻࡴࡩࡖࡲ࡯ࡪࡴࠧᢒ")] = os.getenv(bstack11l11_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᢓ"))
    bstack11l11l1l1l1_opy_ = json.loads(os.getenv(bstack11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧᢔ"), bstack11l11_opy_ (u"ࠧࡼࡿࠪᢕ"))).get(bstack11l11_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᢖ"))
    if not config[bstack11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫᢗ")].get(bstack11l11_opy_ (u"ࠥࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠤᢘ")):
      if bstack11l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᢙ") in caps:
        caps[bstack11l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᢚ")][bstack11l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᢛ")] = bstack1ll1l11ll11_opy_
        caps[bstack11l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᢜ")][bstack11l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᢝ")][bstack11l11_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᢞ")] = bstack11l11l1l1l1_opy_
      else:
        caps[bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᢟ")] = bstack1ll1l11ll11_opy_
        caps[bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᢠ")][bstack11l11_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᢡ")] = bstack11l11l1l1l1_opy_
  except Exception as error:
    logger.debug(bstack11l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷ࠳ࠦࡅࡳࡴࡲࡶ࠿ࠦࠢᢢ") +  str(error))
def bstack11l1l11ll1_opy_(driver, bstack11l111l11l1_opy_):
  try:
    setattr(driver, bstack11l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧᢣ"), True)
    session = driver.session_id
    if session:
      bstack11l11l1lll1_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11l11l1lll1_opy_ = False
      bstack11l11l1lll1_opy_ = url.scheme in [bstack11l11_opy_ (u"ࠣࡪࡷࡸࡵࠨᢤ"), bstack11l11_opy_ (u"ࠤ࡫ࡸࡹࡶࡳࠣᢥ")]
      if bstack11l11l1lll1_opy_:
        if bstack11l111l11l1_opy_:
          logger.info(bstack11l11_opy_ (u"ࠥࡗࡪࡺࡵࡱࠢࡩࡳࡷࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡩࡣࡶࠤࡸࡺࡡࡳࡶࡨࡨ࠳ࠦࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡨࡥࡨ࡫ࡱࠤࡲࡵ࡭ࡦࡰࡷࡥࡷ࡯࡬ࡺ࠰ࠥᢦ"))
      return bstack11l111l11l1_opy_
  except Exception as e:
    logger.error(bstack11l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩ࠿ࠦࠢᢧ") + str(e))
    return False
def bstack1ll1l111l1_opy_(driver, name, path):
  try:
    bstack1l1ll11lll1_opy_ = {
        bstack11l11_opy_ (u"ࠬࡺࡨࡕࡧࡶࡸࡗࡻ࡮ࡖࡷ࡬ࡨࠬᢨ"): threading.current_thread().current_test_uuid,
        bstack11l11_opy_ (u"࠭ࡴࡩࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧᢩࠫ"): os.environ.get(bstack11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᢪ"), bstack11l11_opy_ (u"ࠨࠩ᢫")),
        bstack11l11_opy_ (u"ࠩࡷ࡬ࡏࡽࡴࡕࡱ࡮ࡩࡳ࠭᢬"): os.environ.get(bstack11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ᢭"), bstack11l11_opy_ (u"ࠫࠬ᢮"))
    }
    bstack1l111l111l_opy_ = bstack11ll11ll1l_opy_.bstack1l11111111_opy_(EVENTS.bstack11ll1l1lll_opy_.value)
    logger.debug(bstack11l11_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡣࡹ࡭ࡳ࡭ࠠࡳࡧࡶࡹࡱࡺࡳࠨ᢯"))
    try:
      if (bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ᢰ"), None) and bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᢱ"), None)):
        scripts = {bstack11l11_opy_ (u"ࠨࡵࡦࡥࡳ࠭ᢲ"): bstack1l1lll111l_opy_.perform_scan}
        bstack11l11ll1111_opy_ = json.loads(scripts[bstack11l11_opy_ (u"ࠤࡶࡧࡦࡴࠢᢳ")].replace(bstack11l11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨᢴ"), bstack11l11_opy_ (u"ࠦࠧᢵ")))
        bstack11l11ll1111_opy_[bstack11l11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᢶ")][bstack11l11_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩ࠭ᢷ")] = None
        scripts[bstack11l11_opy_ (u"ࠢࡴࡥࡤࡲࠧᢸ")] = bstack11l11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࠦᢹ") + json.dumps(bstack11l11ll1111_opy_)
        bstack1l1lll111l_opy_.bstack1l111l111_opy_(scripts)
        bstack1l1lll111l_opy_.store()
        logger.debug(driver.execute_script(bstack1l1lll111l_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1l1lll111l_opy_.perform_scan, {bstack11l11_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࠤᢺ"): name}))
      bstack11ll11ll1l_opy_.end(EVENTS.bstack11ll1l1lll_opy_.value, bstack1l111l111l_opy_ + bstack11l11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᢻ"), bstack1l111l111l_opy_ + bstack11l11_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᢼ"), True, None)
    except Exception as error:
      bstack11ll11ll1l_opy_.end(EVENTS.bstack11ll1l1lll_opy_.value, bstack1l111l111l_opy_ + bstack11l11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᢽ"), bstack1l111l111l_opy_ + bstack11l11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᢾ"), False, str(error))
    bstack1l111l111l_opy_ = bstack11ll11ll1l_opy_.bstack11l11l111l1_opy_(EVENTS.bstack1l1l1l11lll_opy_.value)
    bstack11ll11ll1l_opy_.mark(bstack1l111l111l_opy_ + bstack11l11_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᢿ"))
    try:
      if (bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨᣀ"), None) and bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫᣁ"), None)):
        scripts = {bstack11l11_opy_ (u"ࠪࡷࡨࡧ࡮ࠨᣂ"): bstack1l1lll111l_opy_.perform_scan}
        bstack11l11ll1111_opy_ = json.loads(scripts[bstack11l11_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᣃ")].replace(bstack11l11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠣᣄ"), bstack11l11_opy_ (u"ࠨࠢᣅ")))
        bstack11l11ll1111_opy_[bstack11l11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᣆ")][bstack11l11_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࠨᣇ")] = None
        scripts[bstack11l11_opy_ (u"ࠤࡶࡧࡦࡴࠢᣈ")] = bstack11l11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨᣉ") + json.dumps(bstack11l11ll1111_opy_)
        bstack1l1lll111l_opy_.bstack1l111l111_opy_(scripts)
        bstack1l1lll111l_opy_.store()
        logger.debug(driver.execute_script(bstack1l1lll111l_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1l1lll111l_opy_.bstack11l1111ll11_opy_, bstack1l1ll11lll1_opy_))
      bstack11ll11ll1l_opy_.end(bstack1l111l111l_opy_, bstack1l111l111l_opy_ + bstack11l11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᣊ"), bstack1l111l111l_opy_ + bstack11l11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᣋ"),True, None)
    except Exception as error:
      bstack11ll11ll1l_opy_.end(bstack1l111l111l_opy_, bstack1l111l111l_opy_ + bstack11l11_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᣌ"), bstack1l111l111l_opy_ + bstack11l11_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᣍ"),False, str(error))
    logger.info(bstack11l11_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠦᣎ"))
    try:
      bstack1l1l1ll1ll1_opy_ = {
        bstack11l11_opy_ (u"ࠤࡵࡩࡶࡻࡥࡴࡶࠥᣏ"): {
          bstack11l11_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࠦᣐ"): bstack11l11_opy_ (u"ࠦࡆ࠷࠱࡚ࡡࡖࡅ࡛ࡋ࡟ࡓࡇࡖ࡙ࡑ࡚ࡓࠣᣑ"),
        },
        bstack11l11_opy_ (u"ࠧࡸࡥࡴࡲࡲࡲࡸ࡫ࠢᣒ"): {
          bstack11l11_opy_ (u"ࠨࡢࡰࡦࡼࠦᣓ"): {
            bstack11l11_opy_ (u"ࠢ࡮ࡵࡪࠦᣔ"): bstack11l11_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠦᣕ"),
            bstack11l11_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥᣖ"): True
          }
        }
      }
      bstack111111l11_opy_.info(json.dumps(bstack1l1l1ll1ll1_opy_, separators=(bstack11l11_opy_ (u"ࠪ࠰ࠬᣗ"), bstack11l11_opy_ (u"ࠫ࠿࠭ᣘ"))))
    except Exception as bstack11llll1l_opy_:
      logger.debug(bstack11l11_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡮ࡲ࡫ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡡࡷࡧࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡩࡧࡴࡢ࠼ࠣࠦᣙ") + str(bstack11llll1l_opy_) + bstack11l11_opy_ (u"ࠨࠢᣚ"))
  except Exception as bstack1l1l1l1llll_opy_:
    logger.error(bstack11l11_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡥࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡧ࡫ࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡪࡴࡸࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤᣛ") + str(path) + bstack11l11_opy_ (u"ࠣࠢࡈࡶࡷࡵࡲࠡ࠼ࠥᣜ") + str(bstack1l1l1l1llll_opy_))
def bstack11l111lllll_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack11l11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣᣝ")) and str(caps.get(bstack11l11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤᣞ"))).lower() == bstack11l11_opy_ (u"ࠦࡦࡴࡤࡳࡱ࡬ࡨࠧᣟ"):
        bstack1l1ll11ll1l_opy_ = caps.get(bstack11l11_opy_ (u"ࠧࡧࡰࡱ࡫ࡸࡱ࠿ࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢᣠ")) or caps.get(bstack11l11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣᣡ"))
        if bstack1l1ll11ll1l_opy_ and int(str(bstack1l1ll11ll1l_opy_)) < bstack11l111lll1l_opy_:
            return False
    return True
def bstack1ll11l1l1l_opy_(config):
  if bstack11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᣢ") in config:
        return config[bstack11l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᣣ")]
  for platform in config.get(bstack11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᣤ"), []):
      if bstack11l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᣥ") in platform:
          return platform[bstack11l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᣦ")]
  return None
def bstack11l1l1l111_opy_(bstack1ll1ll1l_opy_):
  try:
    browser_name = bstack1ll1ll1l_opy_[bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫᣧ")]
    browser_version = bstack1ll1ll1l_opy_[bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᣨ")]
    chrome_options = bstack1ll1ll1l_opy_[bstack11l11_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫࡟ࡰࡲࡷ࡭ࡴࡴࡳࠨᣩ")]
    try:
        bstack11l11ll11l1_opy_ = int(browser_version.split(bstack11l11_opy_ (u"ࠨ࠰ࠪᣪ"))[0])
    except ValueError as e:
        logger.error(bstack11l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡱࡱࡺࡪࡸࡴࡪࡰࡪࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࡼࡥࡳࡵ࡬ࡳࡳࠨᣫ") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack11l11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪᣬ")):
        logger.warning(bstack11l11_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢᣭ"))
        return False
    if bstack11l11ll11l1_opy_ < bstack11l11l1l11l_opy_.bstack1l1ll111lll_opy_:
        logger.warning(bstack1ll1lllll11_opy_ (u"ࠬࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡵࡩࡶࡻࡩࡳࡧࡶࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࢁࡃࡐࡐࡖࡘࡆࡔࡔࡔ࠰ࡐࡍࡓࡏࡍࡖࡏࡢࡒࡔࡔ࡟ࡃࡕࡗࡅࡈࡑ࡟ࡊࡐࡉࡖࡆࡥࡁ࠲࠳࡜ࡣࡘ࡛ࡐࡑࡑࡕࡘࡊࡊ࡟ࡄࡊࡕࡓࡒࡋ࡟ࡗࡇࡕࡗࡎࡕࡎࡾࠢࡲࡶࠥ࡮ࡩࡨࡪࡨࡶ࠳࠭ᣮ"))
        return False
    if chrome_options and any(bstack11l11_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࠪᣯ") in value for value in chrome_options.values() if isinstance(value, str)):
        logger.warning(bstack11l11_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡱࡳࡹࠦࡲࡶࡰࠣࡳࡳࠦ࡬ࡦࡩࡤࡧࡾࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠠࡔࡹ࡬ࡸࡨ࡮ࠠࡵࡱࠣࡲࡪࡽࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫ࠠࡰࡴࠣࡥࡻࡵࡩࡥࠢࡸࡷ࡮ࡴࡧࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠤᣰ"))
        return False
    return True
  except Exception as e:
    logger.error(bstack11l11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡧ࡭࡫ࡣ࡬࡫ࡱ࡫ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡴࡷࡳࡴࡴࡸࡴࠡࡨࡲࡶࠥࡲ࡯ࡤࡣ࡯ࠤࡈ࡮ࡲࡰ࡯ࡨ࠾ࠥࠨᣱ") + str(e))
    return False
def bstack1l111l1l_opy_(bstack111l1ll1ll_opy_, config):
    try:
      bstack1l1l111l1l1_opy_ = bstack11l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᣲ") in config and config[bstack11l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᣳ")] == True
      bstack11l111l1111_opy_ = bstack11l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨᣴ") in config and str(config[bstack11l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩᣵ")]).lower() != bstack11l11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ᣶")
      if not (bstack1l1l111l1l1_opy_ and (not bstack1ll111l11_opy_(config) or bstack11l111l1111_opy_)):
        return bstack111l1ll1ll_opy_
      bstack11l11l1111l_opy_ = bstack1l1lll111l_opy_.bstack11l111ll11l_opy_
      if bstack11l11l1111l_opy_ is None:
        logger.debug(bstack11l11_opy_ (u"ࠢࡈࡱࡲ࡫ࡱ࡫ࠠࡤࡪࡵࡳࡲ࡫ࠠࡰࡲࡷ࡭ࡴࡴࡳࠡࡣࡵࡩࠥࡔ࡯࡯ࡧࠥ᣷"))
        return bstack111l1ll1ll_opy_
      bstack11l11l1ll11_opy_ = int(str(bstack11l11ll11ll_opy_()).split(bstack11l11_opy_ (u"ࠨ࠰ࠪ᣸"))[0])
      logger.debug(bstack11l11_opy_ (u"ࠤࡖࡩࡱ࡫࡮ࡪࡷࡰࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡪࡥࡵࡧࡦࡸࡪࡪ࠺ࠡࠤ᣹") + str(bstack11l11l1ll11_opy_) + bstack11l11_opy_ (u"ࠥࠦ᣺"))
      if bstack11l11l1ll11_opy_ == 3 and isinstance(bstack111l1ll1ll_opy_, dict) and bstack11l11_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ᣻") in bstack111l1ll1ll_opy_ and bstack11l11l1111l_opy_ is not None:
        if bstack11l11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ᣼") not in bstack111l1ll1ll_opy_[bstack11l11_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭᣽")]:
          bstack111l1ll1ll_opy_[bstack11l11_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ᣾")][bstack11l11_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᣿")] = {}
        if bstack11l11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᤀ") in bstack11l11l1111l_opy_:
          if bstack11l11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᤁ") not in bstack111l1ll1ll_opy_[bstack11l11_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᤂ")][bstack11l11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᤃ")]:
            bstack111l1ll1ll_opy_[bstack11l11_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᤄ")][bstack11l11_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᤅ")][bstack11l11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᤆ")] = []
          for arg in bstack11l11l1111l_opy_[bstack11l11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᤇ")]:
            if arg not in bstack111l1ll1ll_opy_[bstack11l11_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᤈ")][bstack11l11_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᤉ")][bstack11l11_opy_ (u"ࠬࡧࡲࡨࡵࠪᤊ")]:
              bstack111l1ll1ll_opy_[bstack11l11_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᤋ")][bstack11l11_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᤌ")][bstack11l11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᤍ")].append(arg)
        if bstack11l11_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᤎ") in bstack11l11l1111l_opy_:
          if bstack11l11_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᤏ") not in bstack111l1ll1ll_opy_[bstack11l11_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᤐ")][bstack11l11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᤑ")]:
            bstack111l1ll1ll_opy_[bstack11l11_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᤒ")][bstack11l11_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᤓ")][bstack11l11_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᤔ")] = []
          for ext in bstack11l11l1111l_opy_[bstack11l11_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᤕ")]:
            if ext not in bstack111l1ll1ll_opy_[bstack11l11_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᤖ")][bstack11l11_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᤗ")][bstack11l11_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᤘ")]:
              bstack111l1ll1ll_opy_[bstack11l11_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᤙ")][bstack11l11_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᤚ")][bstack11l11_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᤛ")].append(ext)
        if bstack11l11_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᤜ") in bstack11l11l1111l_opy_:
          if bstack11l11_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᤝ") not in bstack111l1ll1ll_opy_[bstack11l11_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᤞ")][bstack11l11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ᤟")]:
            bstack111l1ll1ll_opy_[bstack11l11_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᤠ")][bstack11l11_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᤡ")][bstack11l11_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᤢ")] = {}
          bstack11l111l1l11_opy_(bstack111l1ll1ll_opy_[bstack11l11_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᤣ")][bstack11l11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᤤ")][bstack11l11_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪᤥ")],
                    bstack11l11l1111l_opy_[bstack11l11_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫᤦ")])
        os.environ[bstack11l11_opy_ (u"࠭ࡉࡔࡡࡑࡓࡓࡥࡂࡔࡖࡄࡇࡐࡥࡉࡏࡈࡕࡅࡤࡇ࠱࠲࡛ࡢࡗࡊ࡙ࡓࡊࡑࡑࠫᤧ")] = bstack11l11_opy_ (u"ࠧࡵࡴࡸࡩࠬᤨ")
        return bstack111l1ll1ll_opy_
      else:
        chrome_options = None
        if isinstance(bstack111l1ll1ll_opy_, ChromeOptions):
          chrome_options = bstack111l1ll1ll_opy_
        elif isinstance(bstack111l1ll1ll_opy_, dict):
          for value in bstack111l1ll1ll_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack111l1ll1ll_opy_, dict):
            bstack111l1ll1ll_opy_[bstack11l11_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩᤩ")] = chrome_options
          else:
            bstack111l1ll1ll_opy_ = chrome_options
        if bstack11l11l1111l_opy_ is not None:
          if bstack11l11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᤪ") in bstack11l11l1111l_opy_:
                bstack11l1111l1l1_opy_ = chrome_options.arguments or []
                new_args = bstack11l11l1111l_opy_[bstack11l11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᤫ")]
                for arg in new_args:
                    if arg not in bstack11l1111l1l1_opy_:
                        chrome_options.add_argument(arg)
          if bstack11l11_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨ᤬") in bstack11l11l1111l_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack11l11_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩ᤭"), [])
                bstack11l1111llll_opy_ = bstack11l11l1111l_opy_[bstack11l11_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪ᤮")]
                for extension in bstack11l1111llll_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack11l11_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭᤯") in bstack11l11l1111l_opy_:
                bstack11l111l1lll_opy_ = chrome_options.experimental_options.get(bstack11l11_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᤰ"), {})
                bstack11l11l1llll_opy_ = bstack11l11l1111l_opy_[bstack11l11_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᤱ")]
                bstack11l111l1l11_opy_(bstack11l111l1lll_opy_, bstack11l11l1llll_opy_)
                chrome_options.add_experimental_option(bstack11l11_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᤲ"), bstack11l111l1lll_opy_)
        os.environ[bstack11l11_opy_ (u"ࠫࡎ࡙࡟ࡏࡑࡑࡣࡇ࡙ࡔࡂࡅࡎࡣࡎࡔࡆࡓࡃࡢࡅ࠶࠷࡙ࡠࡕࡈࡗࡘࡏࡏࡏࠩᤳ")] = bstack11l11_opy_ (u"ࠬࡺࡲࡶࡧࠪᤴ")
        return bstack111l1ll1ll_opy_
    except Exception as e:
      logger.error(bstack11l11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡦࡪࡤࡪࡰࡪࠤࡳࡵ࡮࠮ࡄࡖࠤ࡮ࡴࡦࡳࡣࠣࡥ࠶࠷ࡹࠡࡥ࡫ࡶࡴࡳࡥࠡࡱࡳࡸ࡮ࡵ࡮ࡴ࠼ࠣࠦᤵ") + str(e))
      return bstack111l1ll1ll_opy_