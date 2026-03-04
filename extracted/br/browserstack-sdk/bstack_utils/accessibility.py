# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack11l111l1l11_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack11l111111ll_opy_ as bstack11l111l1l1l_opy_, EVENTS
from bstack_utils.bstack1l11l11l1l_opy_ import bstack1l11l11l1l_opy_
from bstack_utils.helper import current_time, bstack11111l1ll1_opy_, bstack11lll11l1l_opy_, bstack11l111l11ll_opy_, \
  bstack11l111l1ll1_opy_, bstack1ll1111l1l_opy_, get_host_info, bstack11l111l1111_opy_, bstack1llll1l111_opy_, error_handler, bstack11l11111lll_opy_, bstack11l111lll1l_opy_, bstack1lll111ll_opy_
from browserstack_sdk._version import __version__
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack1l1ll1l111_opy_ import bstack1l11l11ll1_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
from bstack_utils import logger_utils
logger = get_logger(__name__)
bstack1llll11111_opy_ = logger_utils.bstack1l1l1l111_opy_(__name__)
bstack1l1ll1l111_opy_ = bstack1l11l11ll1_opy_()
@error_handler(class_method=False)
def _11l1111111l_opy_(driver, bstack1lll1lll1l1_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1lll1l_opy_ (u"ࠫࡴࡹ࡟࡯ࡣࡰࡩࠬᤥ"): caps.get(bstack1lll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫᤦ"), None),
        bstack1lll1l_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪᤧ"): bstack1lll1lll1l1_opy_.get(bstack1lll1l_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪᤨ"), None),
        bstack1lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧᤩ"): caps.get(bstack1lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᤪ"), None),
        bstack1lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᤫ"): caps.get(bstack1lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᤬"), None)
    }
  except Exception as error:
    logger.debug(bstack1lll1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫࡫ࡴࡤࡪ࡬ࡲ࡬ࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡦࡨࡸࡦ࡯࡬ࡴࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࠦ࠺ࠡࠩ᤭") + str(error))
  return response
def on():
    if os.environ.get(bstack1lll1l_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ᤮"), None) is None or os.environ[bstack1lll1l_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ᤯")] == bstack1lll1l_opy_ (u"ࠣࡰࡸࡰࡱࠨᤰ"):
        return False
    return True
def bstack1l11ll11l1_opy_(config):
  return config.get(bstack1lll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᤱ"), False) or any([p.get(bstack1lll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᤲ"), False) == True for p in config.get(bstack1lll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᤳ"), [])])
def bstack1llll11l11_opy_(config, bstack1ll1llll1l_opy_):
  try:
    bstack11l11111ll1_opy_ = config.get(bstack1lll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᤴ"), False)
    if int(bstack1ll1llll1l_opy_) < len(config.get(bstack1lll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᤵ"), [])) and config[bstack1lll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᤶ")][bstack1ll1llll1l_opy_]:
      bstack11l11l11111_opy_ = config[bstack1lll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᤷ")][bstack1ll1llll1l_opy_].get(bstack1lll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᤸ"), None)
    else:
      bstack11l11l11111_opy_ = config.get(bstack1lll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻ᤹ࠪ"), None)
    if bstack11l11l11111_opy_ != None:
      bstack11l11111ll1_opy_ = bstack11l11l11111_opy_
    bstack11l1111l1ll_opy_ = os.getenv(bstack1lll1l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ᤺")) is not None and len(os.getenv(bstack1lll1l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖ᤻ࠪ"))) > 0 and os.getenv(bstack1lll1l_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ᤼")) != bstack1lll1l_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ᤽")
    return bstack11l11111ll1_opy_ and bstack11l1111l1ll_opy_
  except Exception as error:
    logger.debug(bstack1lll1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡧࡵ࡭࡫ࡿࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶࠥࡀࠠࠨ᤾") + str(error))
  return False
def bstack1lll11ll_opy_(test_tags):
  bstack1l1l1lll1l1_opy_ = os.getenv(bstack1lll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ᤿"))
  if bstack1l1l1lll1l1_opy_ is None:
    return True
  bstack1l1l1lll1l1_opy_ = json.loads(bstack1l1l1lll1l1_opy_)
  try:
    include_tags = bstack1l1l1lll1l1_opy_[bstack1lll1l_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨ᥀")] if bstack1lll1l_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ᥁") in bstack1l1l1lll1l1_opy_ and isinstance(bstack1l1l1lll1l1_opy_[bstack1lll1l_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ᥂")], list) else []
    exclude_tags = bstack1l1l1lll1l1_opy_[bstack1lll1l_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫ᥃")] if bstack1lll1l_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬ᥄") in bstack1l1l1lll1l1_opy_ and isinstance(bstack1l1l1lll1l1_opy_[bstack1lll1l_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭᥅")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1lll1l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡷࡣ࡯࡭ࡩࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡡ࡯ࡰ࡬ࡲ࡬࠴ࠠࡆࡴࡵࡳࡷࠦ࠺ࠡࠤ᥆") + str(error))
  return False
def bstack11l11l1111l_opy_(config, bstack111lllllll1_opy_, bstack11l111111l1_opy_, bstack11l111ll1ll_opy_):
  bstack11l11111111_opy_ = bstack11l111l11ll_opy_(config)
  bstack11l11l111l1_opy_ = bstack11l111l1ll1_opy_(config)
  if bstack11l11111111_opy_ is None or bstack11l11l111l1_opy_ is None:
    logger.error(bstack1lll1l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡸࡵ࡯ࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࡑ࡮ࡹࡳࡪࡰࡪࠤࡦࡻࡴࡩࡧࡱࡸ࡮ࡩࡡࡵ࡫ࡲࡲࠥࡺ࡯࡬ࡧࡱࠫ᥇"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1lll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ᥈"), bstack1lll1l_opy_ (u"ࠬࢁࡽࠨ᥉")))
    data = {
        bstack1lll1l_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫ᥊"): config[bstack1lll1l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ᥋")],
        bstack1lll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ᥌"): config.get(bstack1lll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ᥍"), os.path.basename(os.getcwd())),
        bstack1lll1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡖ࡬ࡱࡪ࠭᥎"): current_time(),
        bstack1lll1l_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩ᥏"): config.get(bstack1lll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᥐ"), bstack1lll1l_opy_ (u"࠭ࠧᥑ")),
        bstack1lll1l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧᥒ"): {
            bstack1lll1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡒࡦࡳࡥࠨᥓ"): bstack111lllllll1_opy_,
            bstack1lll1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬᥔ"): bstack11l111111l1_opy_,
            bstack1lll1l_opy_ (u"ࠪࡷࡩࡱࡖࡦࡴࡶ࡭ࡴࡴࠧᥕ"): __version__,
            bstack1lll1l_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭ᥖ"): bstack1lll1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᥗ"),
            bstack1lll1l_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᥘ"): bstack1lll1l_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩᥙ"),
            bstack1lll1l_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᥚ"): bstack11l111ll1ll_opy_
        },
        bstack1lll1l_opy_ (u"ࠩࡶࡩࡹࡺࡩ࡯ࡩࡶࠫᥛ"): settings,
        bstack1lll1l_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࡇࡴࡴࡴࡳࡱ࡯ࠫᥜ"): bstack11l111l1111_opy_(),
        bstack1lll1l_opy_ (u"ࠫࡨ࡯ࡉ࡯ࡨࡲࠫᥝ"): bstack1ll1111l1l_opy_(),
        bstack1lll1l_opy_ (u"ࠬ࡮࡯ࡴࡶࡌࡲ࡫ࡵࠧᥞ"): get_host_info(),
        bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᥟ"): bstack11lll11l1l_opy_(config)
    }
    headers = {
        bstack1lll1l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ᥠ"): bstack1lll1l_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫᥡ"),
    }
    config = {
        bstack1lll1l_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᥢ"): (bstack11l11111111_opy_, bstack11l11l111l1_opy_),
        bstack1lll1l_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᥣ"): headers
    }
    response = bstack1llll1l111_opy_(bstack1lll1l_opy_ (u"ࠫࡕࡕࡓࡕࠩᥤ"), bstack11l111l1l1l_opy_ + bstack1lll1l_opy_ (u"ࠬ࠵ࡶ࠳࠱ࡷࡩࡸࡺ࡟ࡳࡷࡱࡷࠬᥥ"), data, config)
    bstack111lllll1ll_opy_ = response.json()
    if bstack111lllll1ll_opy_[bstack1lll1l_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧᥦ")]:
      parsed = json.loads(os.getenv(bstack1lll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᥧ"), bstack1lll1l_opy_ (u"ࠨࡽࢀࠫᥨ")))
      parsed[bstack1lll1l_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᥩ")] = bstack111lllll1ll_opy_[bstack1lll1l_opy_ (u"ࠪࡨࡦࡺࡡࠨᥪ")][bstack1lll1l_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᥫ")]
      os.environ[bstack1lll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᥬ")] = json.dumps(parsed)
      bstack1l11l11l1l_opy_.bstack11l1l1lll_opy_(bstack111lllll1ll_opy_[bstack1lll1l_opy_ (u"࠭ࡤࡢࡶࡤࠫᥭ")][bstack1lll1l_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨ᥮")])
      bstack1l11l11l1l_opy_.bstack11l1111ll11_opy_(bstack111lllll1ll_opy_[bstack1lll1l_opy_ (u"ࠨࡦࡤࡸࡦ࠭᥯")][bstack1lll1l_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫᥰ")])
      bstack1l11l11l1l_opy_.store()
      return bstack111lllll1ll_opy_[bstack1lll1l_opy_ (u"ࠪࡨࡦࡺࡡࠨᥱ")][bstack1lll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡘࡴࡱࡥ࡯ࠩᥲ")], bstack111lllll1ll_opy_[bstack1lll1l_opy_ (u"ࠬࡪࡡࡵࡣࠪᥳ")][bstack1lll1l_opy_ (u"࠭ࡩࡥࠩᥴ")]
    else:
      logger.error(bstack1lll1l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࠨ᥵") + bstack111lllll1ll_opy_[bstack1lll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ᥶")])
      if bstack111lllll1ll_opy_[bstack1lll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ᥷")] == bstack1lll1l_opy_ (u"ࠪࡍࡳࡼࡡ࡭࡫ࡧࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡵࡧࡳࡴࡧࡧ࠲ࠬ᥸"):
        for bstack11l111l11l1_opy_ in bstack111lllll1ll_opy_[bstack1lll1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶࠫ᥹")]:
          logger.error(bstack11l111l11l1_opy_[bstack1lll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭᥺")])
      return None, None
  except Exception as error:
    logger.error(bstack1lll1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࠢ᥻") +  str(error))
    return None, None
def bstack11l1111l11l_opy_():
  if os.getenv(bstack1lll1l_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ᥼")) is None:
    return {
        bstack1lll1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ᥽"): bstack1lll1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ᥾"),
        bstack1lll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ᥿"): bstack1lll1l_opy_ (u"ࠫࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥ࡮ࡡࡥࠢࡩࡥ࡮ࡲࡥࡥ࠰ࠪᦀ")
    }
  data = {bstack1lll1l_opy_ (u"ࠬ࡫࡮ࡥࡖ࡬ࡱࡪ࠭ᦁ"): current_time()}
  headers = {
      bstack1lll1l_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭ᦂ"): bstack1lll1l_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࠨᦃ") + os.getenv(bstack1lll1l_opy_ (u"ࠣࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙ࠨᦄ")),
      bstack1lll1l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨᦅ"): bstack1lll1l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ᦆ")
  }
  response = bstack1llll1l111_opy_(bstack1lll1l_opy_ (u"ࠫࡕ࡛ࡔࠨᦇ"), bstack11l111l1l1l_opy_ + bstack1lll1l_opy_ (u"ࠬ࠵ࡴࡦࡵࡷࡣࡷࡻ࡮ࡴ࠱ࡶࡸࡴࡶࠧᦈ"), data, { bstack1lll1l_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᦉ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1lll1l_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡘࡪࡹࡴࠡࡔࡸࡲࠥࡳࡡࡳ࡭ࡨࡨࠥࡧࡳࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠤࡦࡺࠠࠣᦊ") + bstack11111l1ll1_opy_().isoformat() + bstack1lll1l_opy_ (u"ࠨ࡜ࠪᦋ"))
      return {bstack1lll1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᦌ"): bstack1lll1l_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫᦍ"), bstack1lll1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᦎ"): bstack1lll1l_opy_ (u"ࠬ࠭ᦏ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1lll1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡦࡳࡲࡶ࡬ࡦࡶ࡬ࡳࡳࠦ࡯ࡧࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡚ࠥࡥࡴࡶࠣࡖࡺࡴ࠺ࠡࠤᦐ") + str(error))
    return {
        bstack1lll1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᦑ"): bstack1lll1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᦒ"),
        bstack1lll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᦓ"): str(error)
    }
def bstack11l11111l1l_opy_(bstack11l1111llll_opy_):
    return re.match(bstack1lll1l_opy_ (u"ࡵࠫࡣࡢࡤࠬࠪ࡟࠲ࡡࡪࠫࠪࡁࠧࠫᦔ"), bstack11l1111llll_opy_.strip()) is not None
def bstack1l1ll1111_opy_(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack11l11l111ll_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11l11l111ll_opy_ = desired_capabilities
        else:
          bstack11l11l111ll_opy_ = {}
        bstack1l1ll11l111_opy_ = (bstack11l11l111ll_opy_.get(bstack1lll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪᦕ"), bstack1lll1l_opy_ (u"ࠬ࠭ᦖ")).lower() or caps.get(bstack1lll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬᦗ"), bstack1lll1l_opy_ (u"ࠧࠨᦘ")).lower())
        if bstack1l1ll11l111_opy_ == bstack1lll1l_opy_ (u"ࠨ࡫ࡲࡷࠬᦙ"):
            return True
        if bstack1l1ll11l111_opy_ == bstack1lll1l_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࠪᦚ"):
            bstack1l1l1llllll_opy_ = str(float(caps.get(bstack1lll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᦛ")) or bstack11l11l111ll_opy_.get(bstack1lll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᦜ"), {}).get(bstack1lll1l_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨᦝ"),bstack1lll1l_opy_ (u"࠭ࠧᦞ"))))
            if bstack1l1ll11l111_opy_ == bstack1lll1l_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࠨᦟ") and int(bstack1l1l1llllll_opy_.split(bstack1lll1l_opy_ (u"ࠨ࠰ࠪᦠ"))[0]) < float(bstack111lllll1l1_opy_):
                logger.warning(str(bstack11l111lllll_opy_))
                return False
            return True
        bstack1l1ll1111l1_opy_ = caps.get(bstack1lll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᦡ"), {}).get(bstack1lll1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧᦢ"), caps.get(bstack1lll1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫᦣ"), bstack1lll1l_opy_ (u"ࠬ࠭ᦤ")))
        if bstack1l1ll1111l1_opy_:
            logger.warning(bstack1lll1l_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡄࡦࡵ࡮ࡸࡴࡶࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥᦥ"))
            return False
        browser = caps.get(bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᦦ"), bstack1lll1l_opy_ (u"ࠨࠩᦧ")).lower() or bstack11l11l111ll_opy_.get(bstack1lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᦨ"), bstack1lll1l_opy_ (u"ࠪࠫᦩ")).lower()
        if browser != bstack1lll1l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫᦪ"):
            logger.warning(bstack1lll1l_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣᦫ"))
            return False
        browser_version = caps.get(bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ᦬")) or caps.get(bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ᦭")) or bstack11l11l111ll_opy_.get(bstack1lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ᦮")) or bstack11l11l111ll_opy_.get(bstack1lll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ᦯"), {}).get(bstack1lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᦰ")) or bstack11l11l111ll_opy_.get(bstack1lll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᦱ"), {}).get(bstack1lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᦲ"))
        bstack1l1ll111ll1_opy_ = bstack11l111l1l11_opy_.bstack1l1l111l1ll_opy_
        bstack11l111l111l_opy_ = False
        if config is not None:
          bstack11l111l111l_opy_ = bstack1lll1l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪᦳ") in config and str(config[bstack1lll1l_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫᦴ")]).lower() != bstack1lll1l_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧᦵ")
        if os.environ.get(bstack1lll1l_opy_ (u"ࠩࡌࡗࡤࡔࡏࡏࡡࡅࡗ࡙ࡇࡃࡌࡡࡌࡒࡋࡘࡁࡠࡃ࠴࠵࡞ࡥࡓࡆࡕࡖࡍࡔࡔࠧᦶ"), bstack1lll1l_opy_ (u"ࠪࠫᦷ")).lower() == bstack1lll1l_opy_ (u"ࠫࡹࡸࡵࡦࠩᦸ") or bstack11l111l111l_opy_:
          bstack1l1ll111ll1_opy_ = bstack11l111l1l11_opy_.bstack1l1l1l1l11l_opy_
        if browser_version and browser_version != bstack1lll1l_opy_ (u"ࠬࡲࡡࡵࡧࡶࡸࠬᦹ") and int(browser_version.split(bstack1lll1l_opy_ (u"࠭࠮ࠨᦺ"))[0]) <= bstack1l1ll111ll1_opy_:
          logger.warning(bstack1ll1l1ll11l_opy_ (u"ࠧࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡪࡶࡪࡧࡴࡦࡴࠣࡸ࡭ࡧ࡮ࠡࡽࡰ࡭ࡳࡥࡡ࠲࠳ࡼࡣࡸࡻࡰࡱࡱࡵࡸࡪࡪ࡟ࡤࡪࡵࡳࡲ࡫࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࡾ࠰ࠪᦻ"))
          return False
        if not options:
          bstack1l1l111ll11_opy_ = caps.get(bstack1lll1l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᦼ")) or bstack11l11l111ll_opy_.get(bstack1lll1l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᦽ"), {})
          if bstack1lll1l_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹࠧᦾ") in bstack1l1l111ll11_opy_.get(bstack1lll1l_opy_ (u"ࠫࡦࡸࡧࡴࠩᦿ"), []):
              logger.warning(bstack1lll1l_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠ࡯ࡱࡷࠤࡷࡻ࡮ࠡࡱࡱࠤࡱ࡫ࡧࡢࡥࡼࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲࡙ࠥࡷࡪࡶࡦ࡬ࠥࡺ࡯ࠡࡰࡨࡻࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩࠥࡵࡲࠡࡣࡹࡳ࡮ࡪࠠࡶࡵ࡬ࡲ࡬ࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠢᧀ"))
              return False
        return True
    except Exception as error:
        logger.debug(bstack1lll1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡡ࡭࡫ࡧࡥࡹ࡫ࠠࡢ࠳࠴ࡽࠥࡹࡵࡱࡲࡲࡶࡹࠦ࠺ࠣᧁ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1l1llllll1l_opy_ = config.get(bstack1lll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᧂ"), {})
    bstack1l1llllll1l_opy_[bstack1lll1l_opy_ (u"ࠨࡣࡸࡸ࡭࡚࡯࡬ࡧࡱࠫᧃ")] = os.getenv(bstack1lll1l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᧄ"))
    bstack11l111lll11_opy_ = json.loads(os.getenv(bstack1lll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᧅ"), bstack1lll1l_opy_ (u"ࠫࢀࢃࠧᧆ"))).get(bstack1lll1l_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᧇ"))
    if not config[bstack1lll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨᧈ")].get(bstack1lll1l_opy_ (u"ࠢࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪࠨᧉ")):
      if bstack1lll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᧊") in caps:
        caps[bstack1lll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ᧋")][bstack1lll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ᧌")] = bstack1l1llllll1l_opy_
        caps[bstack1lll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ᧍")][bstack1lll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ᧎")][bstack1lll1l_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ᧏")] = bstack11l111lll11_opy_
      else:
        caps[bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭᧐")] = bstack1l1llllll1l_opy_
        caps[bstack1lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ᧑")][bstack1lll1l_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ᧒")] = bstack11l111lll11_opy_
  except Exception as error:
    logger.debug(bstack1lll1l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴ࠰ࠣࡉࡷࡸ࡯ࡳ࠼ࠣࠦ᧓") +  str(error))
def bstack11ll1lll11_opy_(driver, bstack11l111ll1l1_opy_):
  try:
    setattr(driver, bstack1lll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫ᧔"), True)
    session = driver.session_id
    if session:
      bstack11l1111l1l1_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11l1111l1l1_opy_ = False
      bstack11l1111l1l1_opy_ = url.scheme in [bstack1lll1l_opy_ (u"ࠧ࡮ࡴࡵࡲࠥ᧕"), bstack1lll1l_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧ᧖")]
      if bstack11l1111l1l1_opy_:
        if bstack11l111ll1l1_opy_:
          logger.info(bstack1lll1l_opy_ (u"ࠢࡔࡧࡷࡹࡵࠦࡦࡰࡴࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡭ࡧࡳࠡࡵࡷࡥࡷࡺࡥࡥ࠰ࠣࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡥࡩ࡬࡯࡮ࠡ࡯ࡲࡱࡪࡴࡴࡢࡴ࡬ࡰࡾ࠴ࠢ᧗"))
      return bstack11l111ll1l1_opy_
  except Exception as e:
    logger.error(bstack1lll1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡤࡶࡹ࡯࡮ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦ࠼ࠣࠦ᧘") + str(e))
    return False
def bstack11111ll11_opy_(driver, name, path):
  try:
    bstack1l1l1ll11ll_opy_ = {
        bstack1lll1l_opy_ (u"ࠩࡷ࡬࡙࡫ࡳࡵࡔࡸࡲ࡚ࡻࡩࡥࠩ᧙"): threading.current_thread().current_test_uuid,
        bstack1lll1l_opy_ (u"ࠪࡸ࡭ࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ᧚"): os.environ.get(bstack1lll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ᧛"), bstack1lll1l_opy_ (u"ࠬ࠭᧜")),
        bstack1lll1l_opy_ (u"࠭ࡴࡩࡌࡺࡸ࡙ࡵ࡫ࡦࡰࠪ᧝"): os.environ.get(bstack1lll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ᧞"), bstack1lll1l_opy_ (u"ࠨࠩ᧟"))
    }
    bstack1ll111111l_opy_ = bstack1l1ll1l111_opy_.bstack1111l1lll_opy_(EVENTS.bstack111l1ll1l1_opy_.value)
    logger.debug(bstack1lll1l_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡧࡶࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠬ᧠"))
    try:
      if (bstack1lll111ll_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ᧡"), None) and bstack1lll111ll_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭᧢"), None)):
        scripts = {bstack1lll1l_opy_ (u"ࠬࡹࡣࡢࡰࠪ᧣"): bstack1l11l11l1l_opy_.perform_scan}
        bstack111llllllll_opy_ = json.loads(scripts[bstack1lll1l_opy_ (u"ࠨࡳࡤࡣࡱࠦ᧤")].replace(bstack1lll1l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࠥ᧥"), bstack1lll1l_opy_ (u"ࠣࠤ᧦")))
        bstack111llllllll_opy_[bstack1lll1l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ᧧")][bstack1lll1l_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࠪ᧨")] = None
        scripts[bstack1lll1l_opy_ (u"ࠦࡸࡩࡡ࡯ࠤ᧩")] = bstack1lll1l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠣ᧪") + json.dumps(bstack111llllllll_opy_)
        bstack1l11l11l1l_opy_.bstack11l1l1lll_opy_(scripts)
        bstack1l11l11l1l_opy_.store()
        logger.debug(driver.execute_script(bstack1l11l11l1l_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1l11l11l1l_opy_.perform_scan, {bstack1lll1l_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࠨ᧫"): name}))
      bstack1l1ll1l111_opy_.end(EVENTS.bstack111l1ll1l1_opy_.value, bstack1ll111111l_opy_ + bstack1lll1l_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ᧬"), bstack1ll111111l_opy_ + bstack1lll1l_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ᧭"), True, None)
    except Exception as error:
      bstack1l1ll1l111_opy_.end(EVENTS.bstack111l1ll1l1_opy_.value, bstack1ll111111l_opy_ + bstack1lll1l_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ᧮"), bstack1ll111111l_opy_ + bstack1lll1l_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ᧯"), False, str(error))
    bstack1ll111111l_opy_ = bstack1l1ll1l111_opy_.bstack11l111llll1_opy_(EVENTS.bstack1l1l1ll11l1_opy_.value)
    bstack1l1ll1l111_opy_.mark(bstack1ll111111l_opy_ + bstack1lll1l_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ᧰"))
    try:
      if (bstack1lll111ll_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠬ࡯ࡳࡂࡲࡳࡅ࠶࠷ࡹࡕࡧࡶࡸࠬ᧱"), None) and bstack1lll111ll_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ᧲"), None)):
        scripts = {bstack1lll1l_opy_ (u"ࠧࡴࡥࡤࡲࠬ᧳"): bstack1l11l11l1l_opy_.perform_scan}
        bstack111llllllll_opy_ = json.loads(scripts[bstack1lll1l_opy_ (u"ࠣࡵࡦࡥࡳࠨ᧴")].replace(bstack1lll1l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠧ᧵"), bstack1lll1l_opy_ (u"ࠥࠦ᧶")))
        bstack111llllllll_opy_[bstack1lll1l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ᧷")][bstack1lll1l_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬ᧸")] = None
        scripts[bstack1lll1l_opy_ (u"ࠨࡳࡤࡣࡱࠦ᧹")] = bstack1lll1l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࠥ᧺") + json.dumps(bstack111llllllll_opy_)
        bstack1l11l11l1l_opy_.bstack11l1l1lll_opy_(scripts)
        bstack1l11l11l1l_opy_.store()
        logger.debug(driver.execute_script(bstack1l11l11l1l_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1l11l11l1l_opy_.bstack11l1111l111_opy_, bstack1l1l1ll11ll_opy_))
      bstack1l1ll1l111_opy_.end(bstack1ll111111l_opy_, bstack1ll111111l_opy_ + bstack1lll1l_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ᧻"), bstack1ll111111l_opy_ + bstack1lll1l_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ᧼"),True, None)
    except Exception as error:
      bstack1l1ll1l111_opy_.end(bstack1ll111111l_opy_, bstack1ll111111l_opy_ + bstack1lll1l_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ᧽"), bstack1ll111111l_opy_ + bstack1lll1l_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ᧾"),False, str(error))
    logger.info(bstack1lll1l_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠣ᧿"))
    try:
      bstack1l1l111l11l_opy_ = {
        bstack1lll1l_opy_ (u"ࠨࡲࡦࡳࡸࡩࡸࡺࠢᨀ"): {
          bstack1lll1l_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࠣᨁ"): bstack1lll1l_opy_ (u"ࠣࡃ࠴࠵࡞ࡥࡓࡂࡘࡈࡣࡗࡋࡓࡖࡎࡗࡗࠧᨂ"),
        },
        bstack1lll1l_opy_ (u"ࠤࡵࡩࡸࡶ࡯࡯ࡵࡨࠦᨃ"): {
          bstack1lll1l_opy_ (u"ࠥࡦࡴࡪࡹࠣᨄ"): {
            bstack1lll1l_opy_ (u"ࠦࡲࡹࡧࠣᨅ"): bstack1lll1l_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠣᨆ"),
            bstack1lll1l_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢᨇ"): True
          }
        }
      }
      bstack1llll11111_opy_.info(json.dumps(bstack1l1l111l11l_opy_, separators=(bstack1lll1l_opy_ (u"ࠧ࠭ࠩᨈ"), bstack1lll1l_opy_ (u"ࠨ࠼ࠪᨉ"))))
    except Exception as bstack11llll11l1_opy_:
      logger.debug(bstack1lll1l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡲ࡯ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡥࡻ࡫ࠠࡳࡧࡶࡹࡱࡺࡳࠡࡦࡤࡸࡦࡀࠠࠣᨊ") + str(bstack11llll11l1_opy_) + bstack1lll1l_opy_ (u"ࠥࠦᨋ"))
  except Exception as bstack1l1l1ll1ll1_opy_:
    logger.error(bstack1lll1l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡩ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡤࡨࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨ࠾ࠥࠨᨌ") + str(path) + bstack1lll1l_opy_ (u"ࠧࠦࡅࡳࡴࡲࡶࠥࡀࠢᨍ") + str(bstack1l1l1ll1ll1_opy_))
def bstack11l111l1lll_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack1lll1l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧᨎ")) and str(caps.get(bstack1lll1l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨᨏ"))).lower() == bstack1lll1l_opy_ (u"ࠣࡣࡱࡨࡷࡵࡩࡥࠤᨐ"):
        bstack1l1l1llllll_opy_ = caps.get(bstack1lll1l_opy_ (u"ࠤࡤࡴࡵ࡯ࡵ࡮࠼ࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦᨑ")) or caps.get(bstack1lll1l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧᨒ"))
        if bstack1l1l1llllll_opy_ and int(str(bstack1l1l1llllll_opy_)) < bstack111lllll1l1_opy_:
            return False
    return True
def bstack11111111_opy_(config):
  if bstack1lll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᨓ") in config:
        return config[bstack1lll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᨔ")]
  for platform in config.get(bstack1lll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᨕ"), []):
      if bstack1lll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᨖ") in platform:
          return platform[bstack1lll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᨗ")]
  return None
def bstack1l111l111l_opy_(bstack11l1lll1ll_opy_):
  try:
    browser_name = bstack11l1lll1ll_opy_[bstack1lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡲࡦࡳࡥࠨᨘ")]
    browser_version = bstack11l1lll1ll_opy_[bstack1lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᨙ")]
    chrome_options = bstack11l1lll1ll_opy_[bstack1lll1l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡣࡴࡶࡴࡪࡱࡱࡷࠬᨚ")]
    try:
        bstack11l1111ll1l_opy_ = int(browser_version.split(bstack1lll1l_opy_ (u"ࠬ࠴ࠧᨛ"))[0])
    except ValueError as e:
        logger.error(bstack1lll1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡨࡵ࡮ࡷࡧࡵࡸ࡮ࡴࡧࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠥ᨜") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack1lll1l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ᨝")):
        logger.warning(bstack1lll1l_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦ᨞"))
        return False
    if bstack11l1111ll1l_opy_ < bstack11l111l1l11_opy_.bstack1l1l1l1l11l_opy_:
        logger.warning(bstack1ll1l1ll11l_opy_ (u"ࠩࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡲࡦࡳࡸ࡭ࡷ࡫ࡳࠡࡅ࡫ࡶࡴࡳࡥࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡾࡇࡔࡔࡓࡕࡃࡑࡘࡘ࠴ࡍࡊࡐࡌࡑ࡚ࡓ࡟ࡏࡑࡑࡣࡇ࡙ࡔࡂࡅࡎࡣࡎࡔࡆࡓࡃࡢࡅ࠶࠷࡙ࡠࡕࡘࡔࡕࡕࡒࡕࡇࡇࡣࡈࡎࡒࡐࡏࡈࡣ࡛ࡋࡒࡔࡋࡒࡒࢂࠦ࡯ࡳࠢ࡫࡭࡬࡮ࡥࡳ࠰ࠪ᨟"))
        return False
    if chrome_options and any(bstack1lll1l_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹࠧᨠ") in value for value in chrome_options.values() if isinstance(value, str)):
        logger.warning(bstack1lll1l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦ࡮ࡰࡶࠣࡶࡺࡴࠠࡰࡰࠣࡰࡪ࡭ࡡࡤࡻࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠤࡘࡽࡩࡵࡥ࡫ࠤࡹࡵࠠ࡯ࡧࡺࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠤࡴࡸࠠࡢࡸࡲ࡭ࡩࠦࡵࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠨᨡ"))
        return False
    return True
  except Exception as e:
    logger.error(bstack1lll1l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡤࡪࡨࡧࡰ࡯࡮ࡨࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡸࡻࡰࡱࡱࡵࡸࠥ࡬࡯ࡳࠢ࡯ࡳࡨࡧ࡬ࠡࡅ࡫ࡶࡴࡳࡥ࠻ࠢࠥᨢ") + str(e))
    return False
def bstack111l1ll1l_opy_(bstack11111lll_opy_, config):
    try:
      bstack1l1l1l1l111_opy_ = bstack1lll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᨣ") in config and config[bstack1lll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᨤ")] == True
      bstack11l111l111l_opy_ = bstack1lll1l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬᨥ") in config and str(config[bstack1lll1l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᨦ")]).lower() != bstack1lll1l_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩᨧ")
      if not (bstack1l1l1l1l111_opy_ and (not bstack11lll11l1l_opy_(config) or bstack11l111l111l_opy_)):
        return bstack11111lll_opy_
      bstack111llllll11_opy_ = bstack1l11l11l1l_opy_.bstack11l111ll111_opy_
      if bstack111llllll11_opy_ is None:
        logger.debug(bstack1lll1l_opy_ (u"ࠦࡌࡵ࡯ࡨ࡮ࡨࠤࡨ࡮ࡲࡰ࡯ࡨࠤࡴࡶࡴࡪࡱࡱࡷࠥࡧࡲࡦࠢࡑࡳࡳ࡫ࠢᨨ"))
        return bstack11111lll_opy_
      bstack11l111ll11l_opy_ = int(str(bstack11l111lll1l_opy_()).split(bstack1lll1l_opy_ (u"ࠬ࠴ࠧᨩ"))[0])
      logger.debug(bstack1lll1l_opy_ (u"ࠨࡓࡦ࡮ࡨࡲ࡮ࡻ࡭ࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡧࡩࡹ࡫ࡣࡵࡧࡧ࠾ࠥࠨᨪ") + str(bstack11l111ll11l_opy_) + bstack1lll1l_opy_ (u"ࠢࠣᨫ"))
      if bstack11l111ll11l_opy_ == 3 and isinstance(bstack11111lll_opy_, dict) and bstack1lll1l_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᨬ") in bstack11111lll_opy_ and bstack111llllll11_opy_ is not None:
        if bstack1lll1l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᨭ") not in bstack11111lll_opy_[bstack1lll1l_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᨮ")]:
          bstack11111lll_opy_[bstack1lll1l_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᨯ")][bstack1lll1l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᨰ")] = {}
        if bstack1lll1l_opy_ (u"࠭ࡡࡳࡩࡶࠫᨱ") in bstack111llllll11_opy_:
          if bstack1lll1l_opy_ (u"ࠧࡢࡴࡪࡷࠬᨲ") not in bstack11111lll_opy_[bstack1lll1l_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᨳ")][bstack1lll1l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᨴ")]:
            bstack11111lll_opy_[bstack1lll1l_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᨵ")][bstack1lll1l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᨶ")][bstack1lll1l_opy_ (u"ࠬࡧࡲࡨࡵࠪᨷ")] = []
          for arg in bstack111llllll11_opy_[bstack1lll1l_opy_ (u"࠭ࡡࡳࡩࡶࠫᨸ")]:
            if arg not in bstack11111lll_opy_[bstack1lll1l_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᨹ")][bstack1lll1l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᨺ")][bstack1lll1l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᨻ")]:
              bstack11111lll_opy_[bstack1lll1l_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᨼ")][bstack1lll1l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᨽ")][bstack1lll1l_opy_ (u"ࠬࡧࡲࡨࡵࠪᨾ")].append(arg)
        if bstack1lll1l_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᨿ") in bstack111llllll11_opy_:
          if bstack1lll1l_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᩀ") not in bstack11111lll_opy_[bstack1lll1l_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᩁ")][bstack1lll1l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᩂ")]:
            bstack11111lll_opy_[bstack1lll1l_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᩃ")][bstack1lll1l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᩄ")][bstack1lll1l_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᩅ")] = []
          for ext in bstack111llllll11_opy_[bstack1lll1l_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᩆ")]:
            if ext not in bstack11111lll_opy_[bstack1lll1l_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᩇ")][bstack1lll1l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᩈ")][bstack1lll1l_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᩉ")]:
              bstack11111lll_opy_[bstack1lll1l_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᩊ")][bstack1lll1l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᩋ")][bstack1lll1l_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᩌ")].append(ext)
        if bstack1lll1l_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬᩍ") in bstack111llllll11_opy_:
          if bstack1lll1l_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ᩎ") not in bstack11111lll_opy_[bstack1lll1l_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᩏ")][bstack1lll1l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᩐ")]:
            bstack11111lll_opy_[bstack1lll1l_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᩑ")][bstack1lll1l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᩒ")][bstack1lll1l_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫᩓ")] = {}
          bstack11l11111lll_opy_(bstack11111lll_opy_[bstack1lll1l_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᩔ")][bstack1lll1l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᩕ")][bstack1lll1l_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᩖ")],
                    bstack111llllll11_opy_[bstack1lll1l_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᩗ")])
        os.environ[bstack1lll1l_opy_ (u"ࠪࡍࡘࡥࡎࡐࡐࡢࡆࡘ࡚ࡁࡄࡍࡢࡍࡓࡌࡒࡂࡡࡄ࠵࠶࡟࡟ࡔࡇࡖࡗࡎࡕࡎࠨᩘ")] = bstack1lll1l_opy_ (u"ࠫࡹࡸࡵࡦࠩᩙ")
        return bstack11111lll_opy_
      else:
        chrome_options = None
        if isinstance(bstack11111lll_opy_, ChromeOptions):
          chrome_options = bstack11111lll_opy_
        elif isinstance(bstack11111lll_opy_, dict):
          for value in bstack11111lll_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack11111lll_opy_, dict):
            bstack11111lll_opy_[bstack1lll1l_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ᩚ")] = chrome_options
          else:
            bstack11111lll_opy_ = chrome_options
        if bstack111llllll11_opy_ is not None:
          if bstack1lll1l_opy_ (u"࠭ࡡࡳࡩࡶࠫᩛ") in bstack111llllll11_opy_:
                bstack11l1111lll1_opy_ = chrome_options.arguments or []
                new_args = bstack111llllll11_opy_[bstack1lll1l_opy_ (u"ࠧࡢࡴࡪࡷࠬᩜ")]
                for arg in new_args:
                    if arg not in bstack11l1111lll1_opy_:
                        chrome_options.add_argument(arg)
          if bstack1lll1l_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᩝ") in bstack111llllll11_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack1lll1l_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᩞ"), [])
                bstack11l11l11l11_opy_ = bstack111llllll11_opy_[bstack1lll1l_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧ᩟")]
                for extension in bstack11l11l11l11_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack1lll1l_opy_ (u"ࠫࡵࡸࡥࡧࡵ᩠ࠪ") in bstack111llllll11_opy_:
                bstack11l11111l11_opy_ = chrome_options.experimental_options.get(bstack1lll1l_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫᩡ"), {})
                bstack111llllll1l_opy_ = bstack111llllll11_opy_[bstack1lll1l_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬᩢ")]
                bstack11l11111lll_opy_(bstack11l11111l11_opy_, bstack111llllll1l_opy_)
                chrome_options.add_experimental_option(bstack1lll1l_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ᩣ"), bstack11l11111l11_opy_)
        os.environ[bstack1lll1l_opy_ (u"ࠨࡋࡖࡣࡓࡕࡎࡠࡄࡖࡘࡆࡉࡋࡠࡋࡑࡊࡗࡇ࡟ࡂ࠳࠴࡝ࡤ࡙ࡅࡔࡕࡌࡓࡓ࠭ᩤ")] = bstack1lll1l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᩥ")
        return bstack11111lll_opy_
    except Exception as e:
      logger.error(bstack1lll1l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡣࡧࡨ࡮ࡴࡧࠡࡰࡲࡲ࠲ࡈࡓࠡ࡫ࡱࡪࡷࡧࠠࡢ࠳࠴ࡽࠥࡩࡨࡳࡱࡰࡩࠥࡵࡰࡵ࡫ࡲࡲࡸࡀࠠࠣᩦ") + str(e))
      return bstack11111lll_opy_