# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack111llllllll_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack111lllll111_opy_ as bstack11l111ll1l1_opy_, EVENTS
from bstack_utils.bstack1l111l111_opy_ import bstack1l111l111_opy_
from bstack_utils.helper import current_time, bstack11111111l1_opy_, bstack1ll11ll11l_opy_, bstack11l111l1l1l_opy_, \
  bstack11l1111l1l1_opy_, bstack1ll11111_opy_, get_host_info, bstack111llllll11_opy_, bstack1llll1l1ll_opy_, error_handler, bstack11l111l111l_opy_, bstack11l1111llll_opy_, bstack1lll11lll1_opy_
from browserstack_sdk._version import __version__
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack1ll1l11ll1_opy_ import bstack1l11l1ll_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
from bstack_utils import logger_utils
logger = get_logger(__name__)
bstack11llllll1l_opy_ = logger_utils.bstack1ll11llll1_opy_(__name__)
bstack1ll1l11ll1_opy_ = bstack1l11l1ll_opy_()
@error_handler(class_method=False)
def _111lllll1ll_opy_(driver, bstack1llll1l1111_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1111_opy_ (u"ࠬࡵࡳࡠࡰࡤࡱࡪ࠭ᤦ"): caps.get(bstack1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬᤧ"), None),
        bstack1111_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫᤨ"): bstack1llll1l1111_opy_.get(bstack1111_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫᤩ"), None),
        bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡲࡦࡳࡥࠨᤪ"): caps.get(bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᤫ"), None),
        bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭᤬"): caps.get(bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭᤭"), None)
    }
  except Exception as error:
    logger.debug(bstack1111_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡥࡵࡥ࡫࡭ࡳ࡭ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡧࡩࡹࡧࡩ࡭ࡵࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸࠠ࠻ࠢࠪ᤮") + str(error))
  return response
def on():
    if os.environ.get(bstack1111_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ᤯"), None) is None or os.environ[bstack1111_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᤰ")] == bstack1111_opy_ (u"ࠤࡱࡹࡱࡲࠢᤱ"):
        return False
    return True
def bstack1llllll11_opy_(config):
  return config.get(bstack1111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᤲ"), False) or any([p.get(bstack1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᤳ"), False) == True for p in config.get(bstack1111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᤴ"), [])])
def bstack111ll1lll1_opy_(config, bstack111ll11111_opy_):
  try:
    bstack11l111lllll_opy_ = config.get(bstack1111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᤵ"), False)
    if int(bstack111ll11111_opy_) < len(config.get(bstack1111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᤶ"), [])) and config[bstack1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᤷ")][bstack111ll11111_opy_]:
      bstack11l111lll1l_opy_ = config[bstack1111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᤸ")][bstack111ll11111_opy_].get(bstack1111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻ᤹ࠪ"), None)
    else:
      bstack11l111lll1l_opy_ = config.get(bstack1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ᤺"), None)
    if bstack11l111lll1l_opy_ != None:
      bstack11l111lllll_opy_ = bstack11l111lll1l_opy_
    bstack11l111111l1_opy_ = os.getenv(bstack1111_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖ᤻ࠪ")) is not None and len(os.getenv(bstack1111_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ᤼"))) > 0 and os.getenv(bstack1111_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ᤽")) != bstack1111_opy_ (u"ࠨࡰࡸࡰࡱ࠭᤾")
    return bstack11l111lllll_opy_ and bstack11l111111l1_opy_
  except Exception as error:
    logger.debug(bstack1111_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡸࡨࡶ࡮࡬ࡹࡪࡰࡪࠤࡹ࡮ࡥࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࠦ࠺ࠡࠩ᤿") + str(error))
  return False
def bstack111l1lll1_opy_(test_tags):
  bstack1l1l1111lll_opy_ = os.getenv(bstack1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ᥀"))
  if bstack1l1l1111lll_opy_ is None:
    return True
  bstack1l1l1111lll_opy_ = json.loads(bstack1l1l1111lll_opy_)
  try:
    include_tags = bstack1l1l1111lll_opy_[bstack1111_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ᥁")] if bstack1111_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ᥂") in bstack1l1l1111lll_opy_ and isinstance(bstack1l1l1111lll_opy_[bstack1111_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫ᥃")], list) else []
    exclude_tags = bstack1l1l1111lll_opy_[bstack1111_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬ᥄")] if bstack1111_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭᥅") in bstack1l1l1111lll_opy_ and isinstance(bstack1l1l1111lll_opy_[bstack1111_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ᥆")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡸࡤࡰ࡮ࡪࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡢࡰࡱ࡭ࡳ࡭࠮ࠡࡇࡵࡶࡴࡸࠠ࠻ࠢࠥ᥇") + str(error))
  return False
def bstack11l111lll11_opy_(config, bstack11l111ll11l_opy_, bstack11l111ll1ll_opy_, bstack111lllll1l1_opy_):
  bstack11l111l11ll_opy_ = bstack11l111l1l1l_opy_(config)
  bstack11l111l1l11_opy_ = bstack11l1111l1l1_opy_(config)
  if bstack11l111l11ll_opy_ is None or bstack11l111l1l11_opy_ is None:
    logger.error(bstack1111_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡲࡶࡰࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࡒ࡯ࡳࡴ࡫ࡱ࡫ࠥࡧࡵࡵࡪࡨࡲࡹ࡯ࡣࡢࡶ࡬ࡳࡳࠦࡴࡰ࡭ࡨࡲࠬ᥈"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭᥉"), bstack1111_opy_ (u"࠭ࡻࡾࠩ᥊")))
    data = {
        bstack1111_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ᥋"): config[bstack1111_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭᥌")],
        bstack1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ᥍"): config.get(bstack1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭᥎"), os.path.basename(os.getcwd())),
        bstack1111_opy_ (u"ࠫࡸࡺࡡࡳࡶࡗ࡭ࡲ࡫ࠧ᥏"): current_time(),
        bstack1111_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪᥐ"): config.get(bstack1111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡉ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩᥑ"), bstack1111_opy_ (u"ࠧࠨᥒ")),
        bstack1111_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨᥓ"): {
            bstack1111_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡓࡧ࡭ࡦࠩᥔ"): bstack11l111ll11l_opy_,
            bstack1111_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᥕ"): bstack11l111ll1ll_opy_,
            bstack1111_opy_ (u"ࠫࡸࡪ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᥖ"): __version__,
            bstack1111_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠧᥗ"): bstack1111_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ᥘ"),
            bstack1111_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᥙ"): bstack1111_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࠪᥚ"),
            bstack1111_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩᥛ"): bstack111lllll1l1_opy_
        },
        bstack1111_opy_ (u"ࠪࡷࡪࡺࡴࡪࡰࡪࡷࠬᥜ"): settings,
        bstack1111_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࡈࡵ࡮ࡵࡴࡲࡰࠬᥝ"): bstack111llllll11_opy_(),
        bstack1111_opy_ (u"ࠬࡩࡩࡊࡰࡩࡳࠬᥞ"): bstack1ll11111_opy_(),
        bstack1111_opy_ (u"࠭ࡨࡰࡵࡷࡍࡳ࡬࡯ࠨᥟ"): get_host_info(),
        bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᥠ"): bstack1ll11ll11l_opy_(config)
    }
    headers = {
        bstack1111_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧᥡ"): bstack1111_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬᥢ"),
    }
    config = {
        bstack1111_opy_ (u"ࠪࡥࡺࡺࡨࠨᥣ"): (bstack11l111l11ll_opy_, bstack11l111l1l11_opy_),
        bstack1111_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᥤ"): headers
    }
    response = bstack1llll1l1ll_opy_(bstack1111_opy_ (u"ࠬࡖࡏࡔࡖࠪᥥ"), bstack11l111ll1l1_opy_ + bstack1111_opy_ (u"࠭࠯ࡷ࠴࠲ࡸࡪࡹࡴࡠࡴࡸࡲࡸ࠭ᥦ"), data, config)
    bstack11l11l1111l_opy_ = response.json()
    if bstack11l11l1111l_opy_[bstack1111_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨᥧ")]:
      parsed = json.loads(os.getenv(bstack1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᥨ"), bstack1111_opy_ (u"ࠩࡾࢁࠬᥩ")))
      parsed[bstack1111_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᥪ")] = bstack11l11l1111l_opy_[bstack1111_opy_ (u"ࠫࡩࡧࡴࡢࠩᥫ")][bstack1111_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᥬ")]
      os.environ[bstack1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧᥭ")] = json.dumps(parsed)
      bstack1l111l111_opy_.bstack11ll1111l_opy_(bstack11l11l1111l_opy_[bstack1111_opy_ (u"ࠧࡥࡣࡷࡥࠬ᥮")][bstack1111_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩ᥯")])
      bstack1l111l111_opy_.bstack11l1111l11l_opy_(bstack11l11l1111l_opy_[bstack1111_opy_ (u"ࠩࡧࡥࡹࡧࠧᥰ")][bstack1111_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬᥱ")])
      bstack1l111l111_opy_.store()
      return bstack11l11l1111l_opy_[bstack1111_opy_ (u"ࠫࡩࡧࡴࡢࠩᥲ")][bstack1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࡙ࡵ࡫ࡦࡰࠪᥳ")], bstack11l11l1111l_opy_[bstack1111_opy_ (u"࠭ࡤࡢࡶࡤࠫᥴ")][bstack1111_opy_ (u"ࠧࡪࡦࠪ᥵")]
    else:
      logger.error(bstack1111_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡶࡺࡴ࡮ࡪࡰࡪࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࠩ᥶") + bstack11l11l1111l_opy_[bstack1111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ᥷")])
      if bstack11l11l1111l_opy_[bstack1111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ᥸")] == bstack1111_opy_ (u"ࠫࡎࡴࡶࡢ࡮࡬ࡨࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥࡶࡡࡴࡵࡨࡨ࠳࠭᥹"):
        for bstack11l111ll111_opy_ in bstack11l11l1111l_opy_[bstack1111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡷࠬ᥺")]:
          logger.error(bstack11l111ll111_opy_[bstack1111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ᥻")])
      return None, None
  except Exception as error:
    logger.error(bstack1111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡵࡹࡳࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࠣ᥼") +  str(error))
    return None, None
def bstack11l1111ll11_opy_():
  if os.getenv(bstack1111_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭᥽")) is None:
    return {
        bstack1111_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ᥾"): bstack1111_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ᥿"),
        bstack1111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᦀ"): bstack1111_opy_ (u"ࠬࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡨࡢࡦࠣࡪࡦ࡯࡬ࡦࡦ࠱ࠫᦁ")
    }
  data = {bstack1111_opy_ (u"࠭ࡥ࡯ࡦࡗ࡭ࡲ࡫ࠧᦂ"): current_time()}
  headers = {
      bstack1111_opy_ (u"ࠧࡂࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧᦃ"): bstack1111_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࠩᦄ") + os.getenv(bstack1111_opy_ (u"ࠤࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠢᦅ")),
      bstack1111_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩᦆ"): bstack1111_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧᦇ")
  }
  response = bstack1llll1l1ll_opy_(bstack1111_opy_ (u"ࠬࡖࡕࡕࠩᦈ"), bstack11l111ll1l1_opy_ + bstack1111_opy_ (u"࠭࠯ࡵࡧࡶࡸࡤࡸࡵ࡯ࡵ࠲ࡷࡹࡵࡰࠨᦉ"), data, { bstack1111_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᦊ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1111_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤ࡙࡫ࡳࡵࠢࡕࡹࡳࠦ࡭ࡢࡴ࡮ࡩࡩࠦࡡࡴࠢࡦࡳࡲࡶ࡬ࡦࡶࡨࡨࠥࡧࡴࠡࠤᦋ") + bstack11111111l1_opy_().isoformat() + bstack1111_opy_ (u"ࠩ࡝ࠫᦌ"))
      return {bstack1111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᦍ"): bstack1111_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬᦎ"), bstack1111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᦏ"): bstack1111_opy_ (u"࠭ࠧᦐ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡧࡴࡳࡰ࡭ࡧࡷ࡭ࡴࡴࠠࡰࡨࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡔࡦࡵࡷࠤࡗࡻ࡮࠻ࠢࠥᦑ") + str(error))
    return {
        bstack1111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᦒ"): bstack1111_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᦓ"),
        bstack1111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᦔ"): str(error)
    }
def bstack11l1111l1ll_opy_(bstack111lllllll1_opy_):
    return re.match(bstack1111_opy_ (u"ࡶࠬࡤ࡜ࡥ࠭ࠫࡠ࠳ࡢࡤࠬࠫࡂࠨࠬᦕ"), bstack111lllllll1_opy_.strip()) is not None
def bstack1ll1111l1l_opy_(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack11l11111l1l_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11l11111l1l_opy_ = desired_capabilities
        else:
          bstack11l11111l1l_opy_ = {}
        bstack1l1l1l1llll_opy_ = (bstack11l11111l1l_opy_.get(bstack1111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫᦖ"), bstack1111_opy_ (u"࠭ࠧᦗ")).lower() or caps.get(bstack1111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ᦘ"), bstack1111_opy_ (u"ࠨࠩᦙ")).lower())
        if bstack1l1l1l1llll_opy_ == bstack1111_opy_ (u"ࠩ࡬ࡳࡸ࠭ᦚ"):
            return True
        if bstack1l1l1l1llll_opy_ == bstack1111_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࠫᦛ"):
            bstack1l1l1l1ll1l_opy_ = str(float(caps.get(bstack1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᦜ")) or bstack11l11111l1l_opy_.get(bstack1111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᦝ"), {}).get(bstack1111_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩᦞ"),bstack1111_opy_ (u"ࠧࠨᦟ"))))
            if bstack1l1l1l1llll_opy_ == bstack1111_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࠩᦠ") and int(bstack1l1l1l1ll1l_opy_.split(bstack1111_opy_ (u"ࠩ࠱ࠫᦡ"))[0]) < float(bstack11l111llll1_opy_):
                logger.warning(str(bstack111lllll11l_opy_))
                return False
            return True
        bstack1l1ll1111l1_opy_ = caps.get(bstack1111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᦢ"), {}).get(bstack1111_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨᦣ"), caps.get(bstack1111_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬᦤ"), bstack1111_opy_ (u"࠭ࠧᦥ")))
        if bstack1l1ll1111l1_opy_:
            logger.warning(bstack1111_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡅࡧࡶ࡯ࡹࡵࡰࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦᦦ"))
            return False
        browser = caps.get(bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᦧ"), bstack1111_opy_ (u"ࠩࠪᦨ")).lower() or bstack11l11111l1l_opy_.get(bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᦩ"), bstack1111_opy_ (u"ࠫࠬᦪ")).lower()
        if browser != bstack1111_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬᦫ"):
            logger.warning(bstack1111_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤ᦬"))
            return False
        browser_version = caps.get(bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᦭")) or caps.get(bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪ᦮")) or bstack11l11111l1l_opy_.get(bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ᦯")) or bstack11l11111l1l_opy_.get(bstack1111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᦰ"), {}).get(bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᦱ")) or bstack11l11111l1l_opy_.get(bstack1111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᦲ"), {}).get(bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᦳ"))
        bstack1l1l11ll11l_opy_ = bstack111llllllll_opy_.bstack1l1l1ll1111_opy_
        bstack11l111l1111_opy_ = False
        if config is not None:
          bstack11l111l1111_opy_ = bstack1111_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫᦴ") in config and str(config[bstack1111_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬᦵ")]).lower() != bstack1111_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨᦶ")
        if os.environ.get(bstack1111_opy_ (u"ࠪࡍࡘࡥࡎࡐࡐࡢࡆࡘ࡚ࡁࡄࡍࡢࡍࡓࡌࡒࡂࡡࡄ࠵࠶࡟࡟ࡔࡇࡖࡗࡎࡕࡎࠨᦷ"), bstack1111_opy_ (u"ࠫࠬᦸ")).lower() == bstack1111_opy_ (u"ࠬࡺࡲࡶࡧࠪᦹ") or bstack11l111l1111_opy_:
          bstack1l1l11ll11l_opy_ = bstack111llllllll_opy_.bstack1l1l1111ll1_opy_
        if browser_version and browser_version != bstack1111_opy_ (u"࠭࡬ࡢࡶࡨࡷࡹ࠭ᦺ") and int(browser_version.split(bstack1111_opy_ (u"ࠧ࠯ࠩᦻ"))[0]) <= bstack1l1l11ll11l_opy_:
          logger.warning(bstack1ll1l1l11l1_opy_ (u"ࠨࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠣ࡫ࡷ࡫ࡡࡵࡧࡵࠤࡹ࡮ࡡ࡯ࠢࡾࡱ࡮ࡴ࡟ࡢ࠳࠴ࡽࡤࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࡠࡥ࡫ࡶࡴࡳࡥࡠࡸࡨࡶࡸ࡯࡯࡯ࡿ࠱ࠫᦼ"))
          return False
        if not options:
          bstack1l1l1l1ll11_opy_ = caps.get(bstack1111_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᦽ")) or bstack11l11111l1l_opy_.get(bstack1111_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᦾ"), {})
          if bstack1111_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳࠨᦿ") in bstack1l1l1l1ll11_opy_.get(bstack1111_opy_ (u"ࠬࡧࡲࡨࡵࠪᧀ"), []):
              logger.warning(bstack1111_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡰࡲࡸࠥࡸࡵ࡯ࠢࡲࡲࠥࡲࡥࡨࡣࡦࡽࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠦࡓࡸ࡫ࡷࡧ࡭ࠦࡴࡰࠢࡱࡩࡼࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪࠦ࡯ࡳࠢࡤࡺࡴ࡯ࡤࠡࡷࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠣᧁ"))
              return False
        return True
    except Exception as error:
        logger.debug(bstack1111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡶࡢ࡮࡬ࡨࡦࡺࡥࠡࡣ࠴࠵ࡾࠦࡳࡶࡲࡳࡳࡷࡺࠠ࠻ࠤᧂ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1ll11111111_opy_ = config.get(bstack1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᧃ"), {})
    bstack1ll11111111_opy_[bstack1111_opy_ (u"ࠩࡤࡹࡹ࡮ࡔࡰ࡭ࡨࡲࠬᧄ")] = os.getenv(bstack1111_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᧅ"))
    bstack11l11111ll1_opy_ = json.loads(os.getenv(bstack1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᧆ"), bstack1111_opy_ (u"ࠬࢁࡽࠨᧇ"))).get(bstack1111_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᧈ"))
    if not config[bstack1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩᧉ")].get(bstack1111_opy_ (u"ࠣࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠢ᧊")):
      if bstack1111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ᧋") in caps:
        caps[bstack1111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ᧌")][bstack1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ᧍")] = bstack1ll11111111_opy_
        caps[bstack1111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭᧎")][bstack1111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭᧏")][bstack1111_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᧐")] = bstack11l11111ll1_opy_
      else:
        caps[bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ᧑")] = bstack1ll11111111_opy_
        caps[bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ᧒")][bstack1111_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ᧓")] = bstack11l11111ll1_opy_
  except Exception as error:
    logger.debug(bstack1111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵ࠱ࠤࡊࡸࡲࡰࡴ࠽ࠤࠧ᧔") +  str(error))
def bstack11ll1llll1_opy_(driver, bstack11l111l1ll1_opy_):
  try:
    setattr(driver, bstack1111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬ᧕"), True)
    session = driver.session_id
    if session:
      bstack11l1111111l_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11l1111111l_opy_ = False
      bstack11l1111111l_opy_ = url.scheme in [bstack1111_opy_ (u"ࠨࡨࡵࡶࡳࠦ᧖"), bstack1111_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨ᧗")]
      if bstack11l1111111l_opy_:
        if bstack11l111l1ll1_opy_:
          logger.info(bstack1111_opy_ (u"ࠣࡕࡨࡸࡺࡶࠠࡧࡱࡵࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡮ࡡࡴࠢࡶࡸࡦࡸࡴࡦࡦ࠱ࠤࡆࡻࡴࡰ࡯ࡤࡸࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡦࡪ࡭ࡩ࡯ࠢࡰࡳࡲ࡫࡮ࡵࡣࡵ࡭ࡱࡿ࠮ࠣ᧘"))
      return bstack11l111l1ll1_opy_
  except Exception as e:
    logger.error(bstack1111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡥࡷࡺࡩ࡯ࡩࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧ࠽ࠤࠧ᧙") + str(e))
    return False
def bstack1ll1ll1l11_opy_(driver, name, path):
  try:
    bstack1l1l11l11l1_opy_ = {
        bstack1111_opy_ (u"ࠪࡸ࡭࡚ࡥࡴࡶࡕࡹࡳ࡛ࡵࡪࡦࠪ᧚"): threading.current_thread().current_test_uuid,
        bstack1111_opy_ (u"ࠫࡹ࡮ࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ᧛"): os.environ.get(bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ᧜"), bstack1111_opy_ (u"࠭ࠧ᧝")),
        bstack1111_opy_ (u"ࠧࡵࡪࡍࡻࡹ࡚࡯࡬ࡧࡱࠫ᧞"): os.environ.get(bstack1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ᧟"), bstack1111_opy_ (u"ࠩࠪ᧠"))
    }
    bstack1l1l1llll1_opy_ = bstack1ll1l11ll1_opy_.bstack11l111111_opy_(EVENTS.bstack11l11lll_opy_.value)
    logger.debug(bstack1111_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡡࡷ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸ࠭᧡"))
    try:
      if (bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ᧢"), None) and bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ᧣"), None)):
        scripts = {bstack1111_opy_ (u"࠭ࡳࡤࡣࡱࠫ᧤"): bstack1l111l111_opy_.perform_scan}
        bstack11l111l1lll_opy_ = json.loads(scripts[bstack1111_opy_ (u"ࠢࡴࡥࡤࡲࠧ᧥")].replace(bstack1111_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࠦ᧦"), bstack1111_opy_ (u"ࠤࠥ᧧")))
        bstack11l111l1lll_opy_[bstack1111_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭᧨")][bstack1111_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࠫ᧩")] = None
        scripts[bstack1111_opy_ (u"ࠧࡹࡣࡢࡰࠥ᧪")] = bstack1111_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࠤ᧫") + json.dumps(bstack11l111l1lll_opy_)
        bstack1l111l111_opy_.bstack11ll1111l_opy_(scripts)
        bstack1l111l111_opy_.store()
        logger.debug(driver.execute_script(bstack1l111l111_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1l111l111_opy_.perform_scan, {bstack1111_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢ᧬"): name}))
      bstack1ll1l11ll1_opy_.end(EVENTS.bstack11l11lll_opy_.value, bstack1l1l1llll1_opy_ + bstack1111_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ᧭"), bstack1l1l1llll1_opy_ + bstack1111_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ᧮"), True, None)
    except Exception as error:
      bstack1ll1l11ll1_opy_.end(EVENTS.bstack11l11lll_opy_.value, bstack1l1l1llll1_opy_ + bstack1111_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ᧯"), bstack1l1l1llll1_opy_ + bstack1111_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ᧰"), False, str(error))
    bstack1l1l1llll1_opy_ = bstack1ll1l11ll1_opy_.bstack11l111111ll_opy_(EVENTS.bstack1l1l11llll1_opy_.value)
    bstack1ll1l11ll1_opy_.mark(bstack1l1l1llll1_opy_ + bstack1111_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ᧱"))
    try:
      if (bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭᧲"), None) and bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ᧳"), None)):
        scripts = {bstack1111_opy_ (u"ࠨࡵࡦࡥࡳ࠭᧴"): bstack1l111l111_opy_.perform_scan}
        bstack11l111l1lll_opy_ = json.loads(scripts[bstack1111_opy_ (u"ࠤࡶࡧࡦࡴࠢ᧵")].replace(bstack1111_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨ᧶"), bstack1111_opy_ (u"ࠦࠧ᧷")))
        bstack11l111l1lll_opy_[bstack1111_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ᧸")][bstack1111_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩ࠭᧹")] = None
        scripts[bstack1111_opy_ (u"ࠢࡴࡥࡤࡲࠧ᧺")] = bstack1111_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࠦ᧻") + json.dumps(bstack11l111l1lll_opy_)
        bstack1l111l111_opy_.bstack11ll1111l_opy_(scripts)
        bstack1l111l111_opy_.store()
        logger.debug(driver.execute_script(bstack1l111l111_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1l111l111_opy_.bstack11l111l11l1_opy_, bstack1l1l11l11l1_opy_))
      bstack1ll1l11ll1_opy_.end(bstack1l1l1llll1_opy_, bstack1l1l1llll1_opy_ + bstack1111_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ᧼"), bstack1l1l1llll1_opy_ + bstack1111_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ᧽"),True, None)
    except Exception as error:
      bstack1ll1l11ll1_opy_.end(bstack1l1l1llll1_opy_, bstack1l1l1llll1_opy_ + bstack1111_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ᧾"), bstack1l1l1llll1_opy_ + bstack1111_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ᧿"),False, str(error))
    logger.info(bstack1111_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠤᨀ"))
    try:
      bstack1l1l1ll11l1_opy_ = {
        bstack1111_opy_ (u"ࠢࡳࡧࡴࡹࡪࡹࡴࠣᨁ"): {
          bstack1111_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤᨂ"): bstack1111_opy_ (u"ࠤࡄ࠵࠶࡟࡟ࡔࡃ࡙ࡉࡤࡘࡅࡔࡗࡏࡘࡘࠨᨃ"),
        },
        bstack1111_opy_ (u"ࠥࡶࡪࡹࡰࡰࡰࡶࡩࠧᨄ"): {
          bstack1111_opy_ (u"ࠦࡧࡵࡤࡺࠤᨅ"): {
            bstack1111_opy_ (u"ࠧࡳࡳࡨࠤᨆ"): bstack1111_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠤᨇ"),
            bstack1111_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳࠣᨈ"): True
          }
        }
      }
      bstack11llllll1l_opy_.info(json.dumps(bstack1l1l1ll11l1_opy_, separators=(bstack1111_opy_ (u"ࠨ࠮ࠪᨉ"), bstack1111_opy_ (u"ࠩ࠽ࠫᨊ"))))
    except Exception as bstack1l111l1l11_opy_:
      logger.debug(bstack1111_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡬ࡰࡩࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡦࡼࡥࠡࡴࡨࡷࡺࡲࡴࡴࠢࡧࡥࡹࡧ࠺ࠡࠤᨋ") + str(bstack1l111l1l11_opy_) + bstack1111_opy_ (u"ࠦࠧᨌ"))
  except Exception as bstack1l1l1ll1l1l_opy_:
    logger.error(bstack1111_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡣࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡥࡩࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡨࡲࡶࠥࡺࡨࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩ࠿ࠦࠢᨍ") + str(path) + bstack1111_opy_ (u"ࠨࠠࡆࡴࡵࡳࡷࠦ࠺ࠣᨎ") + str(bstack1l1l1ll1l1l_opy_))
def bstack11l11l111l1_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack1111_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨᨏ")) and str(caps.get(bstack1111_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢᨐ"))).lower() == bstack1111_opy_ (u"ࠤࡤࡲࡩࡸ࡯ࡪࡦࠥᨑ"):
        bstack1l1l1l1ll1l_opy_ = caps.get(bstack1111_opy_ (u"ࠥࡥࡵࡶࡩࡶ࡯࠽ࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧᨒ")) or caps.get(bstack1111_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨᨓ"))
        if bstack1l1l1l1ll1l_opy_ and int(str(bstack1l1l1l1ll1l_opy_)) < bstack11l111llll1_opy_:
            return False
    return True
def bstack1l1l1ll1l_opy_(config):
  if bstack1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᨔ") in config:
        return config[bstack1111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᨕ")]
  for platform in config.get(bstack1111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᨖ"), []):
      if bstack1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᨗ") in platform:
          return platform[bstack1111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺᨘࠩ")]
  return None
def bstack1l111l11l1_opy_(bstack1ll1l11l11_opy_):
  try:
    browser_name = bstack1ll1l11l11_opy_[bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩᨙ")]
    browser_version = bstack1ll1l11l11_opy_[bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᨚ")]
    chrome_options = bstack1ll1l11l11_opy_[bstack1111_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡤࡵࡰࡵ࡫ࡲࡲࡸ࠭ᨛ")]
    try:
        bstack11l11l11111_opy_ = int(browser_version.split(bstack1111_opy_ (u"࠭࠮ࠨ᨜"))[0])
    except ValueError as e:
        logger.error(bstack1111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡩ࡯࡯ࡸࡨࡶࡹ࡯࡮ࡨࠢࡥࡶࡴࡽࡳࡦࡴࠣࡺࡪࡸࡳࡪࡱࡱࠦ᨝") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack1111_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨ᨞")):
        logger.warning(bstack1111_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶ࠲ࠧ᨟"))
        return False
    if bstack11l11l11111_opy_ < bstack111llllllll_opy_.bstack1l1l1111ll1_opy_:
        logger.warning(bstack1ll1l1l11l1_opy_ (u"ࠪࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡳࡧࡴࡹ࡮ࡸࡥࡴࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡹࡩࡷࡹࡩࡰࡰࠣࡿࡈࡕࡎࡔࡖࡄࡒ࡙࡙࠮ࡎࡋࡑࡍࡒ࡛ࡍࡠࡐࡒࡒࡤࡈࡓࡕࡃࡆࡏࡤࡏࡎࡇࡔࡄࡣࡆ࠷࠱࡚ࡡࡖ࡙ࡕࡖࡏࡓࡖࡈࡈࡤࡉࡈࡓࡑࡐࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࢃࠠࡰࡴࠣ࡬࡮࡭ࡨࡦࡴ࠱ࠫᨠ"))
        return False
    if chrome_options and any(bstack1111_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳࠨᨡ") in value for value in chrome_options.values() if isinstance(value, str)):
        logger.warning(bstack1111_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠ࡯ࡱࡷࠤࡷࡻ࡮ࠡࡱࡱࠤࡱ࡫ࡧࡢࡥࡼࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲࡙ࠥࡷࡪࡶࡦ࡬ࠥࡺ࡯ࠡࡰࡨࡻࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩࠥࡵࡲࠡࡣࡹࡳ࡮ࡪࠠࡶࡵ࡬ࡲ࡬ࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠢᨢ"))
        return False
    return True
  except Exception as e:
    logger.error(bstack1111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡥ࡫ࡩࡨࡱࡩ࡯ࡩࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡹࡵࡱࡲࡲࡶࡹࠦࡦࡰࡴࠣࡰࡴࡩࡡ࡭ࠢࡆ࡬ࡷࡵ࡭ࡦ࠼ࠣࠦᨣ") + str(e))
    return False
def bstack11l1l11l1_opy_(bstack1llll1l1l1_opy_, config):
    try:
      bstack1l1l1l111l1_opy_ = bstack1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᨤ") in config and config[bstack1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᨥ")] == True
      bstack11l111l1111_opy_ = bstack1111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᨦ") in config and str(config[bstack1111_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧᨧ")]).lower() != bstack1111_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪᨨ")
      if not (bstack1l1l1l111l1_opy_ and (not bstack1ll11ll11l_opy_(config) or bstack11l111l1111_opy_)):
        return bstack1llll1l1l1_opy_
      bstack11l11111l11_opy_ = bstack1l111l111_opy_.bstack11l1111l111_opy_
      if bstack11l11111l11_opy_ is None:
        logger.debug(bstack1111_opy_ (u"ࠧࡍ࡯ࡰࡩ࡯ࡩࠥࡩࡨࡳࡱࡰࡩࠥࡵࡰࡵ࡫ࡲࡲࡸࠦࡡࡳࡧࠣࡒࡴࡴࡥࠣᨩ"))
        return bstack1llll1l1l1_opy_
      bstack11l1111lll1_opy_ = int(str(bstack11l1111llll_opy_()).split(bstack1111_opy_ (u"࠭࠮ࠨᨪ"))[0])
      logger.debug(bstack1111_opy_ (u"ࠢࡔࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡹࡩࡷࡹࡩࡰࡰࠣࡨࡪࡺࡥࡤࡶࡨࡨ࠿ࠦࠢᨫ") + str(bstack11l1111lll1_opy_) + bstack1111_opy_ (u"ࠣࠤᨬ"))
      if bstack11l1111lll1_opy_ == 3 and isinstance(bstack1llll1l1l1_opy_, dict) and bstack1111_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᨭ") in bstack1llll1l1l1_opy_ and bstack11l11111l11_opy_ is not None:
        if bstack1111_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᨮ") not in bstack1llll1l1l1_opy_[bstack1111_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᨯ")]:
          bstack1llll1l1l1_opy_[bstack1111_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᨰ")][bstack1111_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᨱ")] = {}
        if bstack1111_opy_ (u"ࠧࡢࡴࡪࡷࠬᨲ") in bstack11l11111l11_opy_:
          if bstack1111_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᨳ") not in bstack1llll1l1l1_opy_[bstack1111_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᨴ")][bstack1111_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᨵ")]:
            bstack1llll1l1l1_opy_[bstack1111_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᨶ")][bstack1111_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᨷ")][bstack1111_opy_ (u"࠭ࡡࡳࡩࡶࠫᨸ")] = []
          for arg in bstack11l11111l11_opy_[bstack1111_opy_ (u"ࠧࡢࡴࡪࡷࠬᨹ")]:
            if arg not in bstack1llll1l1l1_opy_[bstack1111_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᨺ")][bstack1111_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᨻ")][bstack1111_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᨼ")]:
              bstack1llll1l1l1_opy_[bstack1111_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᨽ")][bstack1111_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᨾ")][bstack1111_opy_ (u"࠭ࡡࡳࡩࡶࠫᨿ")].append(arg)
        if bstack1111_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᩀ") in bstack11l11111l11_opy_:
          if bstack1111_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᩁ") not in bstack1llll1l1l1_opy_[bstack1111_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᩂ")][bstack1111_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᩃ")]:
            bstack1llll1l1l1_opy_[bstack1111_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᩄ")][bstack1111_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᩅ")][bstack1111_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᩆ")] = []
          for ext in bstack11l11111l11_opy_[bstack1111_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᩇ")]:
            if ext not in bstack1llll1l1l1_opy_[bstack1111_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᩈ")][bstack1111_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᩉ")][bstack1111_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᩊ")]:
              bstack1llll1l1l1_opy_[bstack1111_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᩋ")][bstack1111_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᩌ")][bstack1111_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᩍ")].append(ext)
        if bstack1111_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ᩎ") in bstack11l11111l11_opy_:
          if bstack1111_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᩏ") not in bstack1llll1l1l1_opy_[bstack1111_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᩐ")][bstack1111_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᩑ")]:
            bstack1llll1l1l1_opy_[bstack1111_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᩒ")][bstack1111_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᩓ")][bstack1111_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬᩔ")] = {}
          bstack11l111l111l_opy_(bstack1llll1l1l1_opy_[bstack1111_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᩕ")][bstack1111_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᩖ")][bstack1111_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᩗ")],
                    bstack11l11111l11_opy_[bstack1111_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᩘ")])
        os.environ[bstack1111_opy_ (u"ࠫࡎ࡙࡟ࡏࡑࡑࡣࡇ࡙ࡔࡂࡅࡎࡣࡎࡔࡆࡓࡃࡢࡅ࠶࠷࡙ࡠࡕࡈࡗࡘࡏࡏࡏࠩᩙ")] = bstack1111_opy_ (u"ࠬࡺࡲࡶࡧࠪᩚ")
        return bstack1llll1l1l1_opy_
      else:
        chrome_options = None
        if isinstance(bstack1llll1l1l1_opy_, ChromeOptions):
          chrome_options = bstack1llll1l1l1_opy_
        elif isinstance(bstack1llll1l1l1_opy_, dict):
          for value in bstack1llll1l1l1_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack1llll1l1l1_opy_, dict):
            bstack1llll1l1l1_opy_[bstack1111_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧᩛ")] = chrome_options
          else:
            bstack1llll1l1l1_opy_ = chrome_options
        if bstack11l11111l11_opy_ is not None:
          if bstack1111_opy_ (u"ࠧࡢࡴࡪࡷࠬᩜ") in bstack11l11111l11_opy_:
                bstack11l11111lll_opy_ = chrome_options.arguments or []
                new_args = bstack11l11111l11_opy_[bstack1111_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᩝ")]
                for arg in new_args:
                    if arg not in bstack11l11111lll_opy_:
                        chrome_options.add_argument(arg)
          if bstack1111_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᩞ") in bstack11l11111l11_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack1111_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧ᩟"), [])
                bstack111llllll1l_opy_ = bstack11l11111l11_opy_[bstack1111_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨ᩠")]
                for extension in bstack111llllll1l_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack1111_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫᩡ") in bstack11l11111l11_opy_:
                bstack11l1111ll1l_opy_ = chrome_options.experimental_options.get(bstack1111_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬᩢ"), {})
                bstack11l11111111_opy_ = bstack11l11111l11_opy_[bstack1111_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ᩣ")]
                bstack11l111l111l_opy_(bstack11l1111ll1l_opy_, bstack11l11111111_opy_)
                chrome_options.add_experimental_option(bstack1111_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᩤ"), bstack11l1111ll1l_opy_)
        os.environ[bstack1111_opy_ (u"ࠩࡌࡗࡤࡔࡏࡏࡡࡅࡗ࡙ࡇࡃࡌࡡࡌࡒࡋࡘࡁࡠࡃ࠴࠵࡞ࡥࡓࡆࡕࡖࡍࡔࡔࠧᩥ")] = bstack1111_opy_ (u"ࠪࡸࡷࡻࡥࠨᩦ")
        return bstack1llll1l1l1_opy_
    except Exception as e:
      logger.error(bstack1111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡤࡨࡩ࡯࡮ࡨࠢࡱࡳࡳ࠳ࡂࡔࠢ࡬ࡲ࡫ࡸࡡࠡࡣ࠴࠵ࡾࠦࡣࡩࡴࡲࡱࡪࠦ࡯ࡱࡶ࡬ࡳࡳࡹ࠺ࠡࠤᩧ") + str(e))
      return bstack1llll1l1l1_opy_