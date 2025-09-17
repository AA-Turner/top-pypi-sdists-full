# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack11ll1l11l1l_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack11ll1llll11_opy_ as bstack11lll1111l1_opy_, EVENTS
from bstack_utils.bstack1l11l11l_opy_ import bstack1l11l11l_opy_
from bstack_utils.helper import bstack1ll11l1ll1_opy_, bstack1111ll11l1_opy_, bstack1llll1llll_opy_, bstack11ll11ll1l1_opy_, \
  bstack11ll1ll11l1_opy_, bstack1lll11ll1l_opy_, get_host_info, bstack11ll11ll111_opy_, bstack1l1ll1ll1l_opy_, error_handler, bstack11ll1l1111l_opy_, bstack11ll1lllll1_opy_, bstack1l11111ll_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack1lll1l1l1l_opy_ import get_logger
from bstack_utils.bstack1lll11l1_opy_ import bstack1lll11111l1_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
logger = get_logger(__name__)
bstack1lll11l1_opy_ = bstack1lll11111l1_opy_()
@error_handler(class_method=False)
def _11ll1l1ll11_opy_(driver, bstack1111l111l1_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1l11ll1_opy_ (u"ࠧࡰࡵࡢࡲࡦࡳࡥࠨᘘ"): caps.get(bstack1l11ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧᘙ"), None),
        bstack1l11ll1_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᘚ"): bstack1111l111l1_opy_.get(bstack1l11ll1_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᘛ"), None),
        bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧࠪᘜ"): caps.get(bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᘝ"), None),
        bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᘞ"): caps.get(bstack1l11ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᘟ"), None)
    }
  except Exception as error:
    logger.debug(bstack1l11ll1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩ࡫ࡴࡢ࡫࡯ࡷࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳࠢ࠽ࠤࠬᘠ") + str(error))
  return response
def on():
    if os.environ.get(bstack1l11ll1_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᘡ"), None) is None or os.environ[bstack1l11ll1_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᘢ")] == bstack1l11ll1_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᘣ"):
        return False
    return True
def bstack11l11l1l1l_opy_(config):
  return config.get(bstack1l11ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᘤ"), False) or any([p.get(bstack1l11ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᘥ"), False) == True for p in config.get(bstack1l11ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᘦ"), [])])
def bstack1l1l11l111_opy_(config, bstack1lll1ll111_opy_):
  try:
    bstack11ll1ll1111_opy_ = config.get(bstack1l11ll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᘧ"), False)
    if int(bstack1lll1ll111_opy_) < len(config.get(bstack1l11ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᘨ"), [])) and config[bstack1l11ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᘩ")][bstack1lll1ll111_opy_]:
      bstack11ll1ll1lll_opy_ = config[bstack1l11ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᘪ")][bstack1lll1ll111_opy_].get(bstack1l11ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᘫ"), None)
    else:
      bstack11ll1ll1lll_opy_ = config.get(bstack1l11ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᘬ"), None)
    if bstack11ll1ll1lll_opy_ != None:
      bstack11ll1ll1111_opy_ = bstack11ll1ll1lll_opy_
    bstack11ll1l11lll_opy_ = os.getenv(bstack1l11ll1_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᘭ")) is not None and len(os.getenv(bstack1l11ll1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᘮ"))) > 0 and os.getenv(bstack1l11ll1_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᘯ")) != bstack1l11ll1_opy_ (u"ࠪࡲࡺࡲ࡬ࠨᘰ")
    return bstack11ll1ll1111_opy_ and bstack11ll1l11lll_opy_
  except Exception as error:
    logger.debug(bstack1l11ll1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡺࡪࡸࡩࡧࡻ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡪࡹࡳࡪࡱࡱࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲࠡ࠼ࠣࠫᘱ") + str(error))
  return False
def bstack11l1lllll_opy_(test_tags):
  bstack1ll11lll1ll_opy_ = os.getenv(bstack1l11ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᘲ"))
  if bstack1ll11lll1ll_opy_ is None:
    return True
  bstack1ll11lll1ll_opy_ = json.loads(bstack1ll11lll1ll_opy_)
  try:
    include_tags = bstack1ll11lll1ll_opy_[bstack1l11ll1_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᘳ")] if bstack1l11ll1_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᘴ") in bstack1ll11lll1ll_opy_ and isinstance(bstack1ll11lll1ll_opy_[bstack1l11ll1_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᘵ")], list) else []
    exclude_tags = bstack1ll11lll1ll_opy_[bstack1l11ll1_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᘶ")] if bstack1l11ll1_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᘷ") in bstack1ll11lll1ll_opy_ and isinstance(bstack1ll11lll1ll_opy_[bstack1l11ll1_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᘸ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1l11ll1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡺࡦࡲࡩࡥࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡥࡤࡲࡳ࡯࡮ࡨ࠰ࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠤࠧᘹ") + str(error))
  return False
def bstack11ll1l1l1ll_opy_(config, bstack11ll11ll11l_opy_, bstack11ll1l11111_opy_, bstack11ll1l1l1l1_opy_):
  bstack11ll1lll111_opy_ = bstack11ll11ll1l1_opy_(config)
  bstack11ll1l111ll_opy_ = bstack11ll1ll11l1_opy_(config)
  if bstack11ll1lll111_opy_ is None or bstack11ll1l111ll_opy_ is None:
    logger.error(bstack1l11ll1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࡍࡪࡵࡶ࡭ࡳ࡭ࠠࡢࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡࡶࡲ࡯ࡪࡴࠧᘺ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1l11ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᘻ"), bstack1l11ll1_opy_ (u"ࠨࡽࢀࠫᘼ")))
    data = {
        bstack1l11ll1_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᘽ"): config[bstack1l11ll1_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᘾ")],
        bstack1l11ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᘿ"): config.get(bstack1l11ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᙀ"), os.path.basename(os.getcwd())),
        bstack1l11ll1_opy_ (u"࠭ࡳࡵࡣࡵࡸ࡙࡯࡭ࡦࠩᙁ"): bstack1ll11l1ll1_opy_(),
        bstack1l11ll1_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᙂ"): config.get(bstack1l11ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᙃ"), bstack1l11ll1_opy_ (u"ࠩࠪᙄ")),
        bstack1l11ll1_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪᙅ"): {
            bstack1l11ll1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨࠫᙆ"): bstack11ll11ll11l_opy_,
            bstack1l11ll1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᙇ"): bstack11ll1l11111_opy_,
            bstack1l11ll1_opy_ (u"࠭ࡳࡥ࡭࡙ࡩࡷࡹࡩࡰࡰࠪᙈ"): __version__,
            bstack1l11ll1_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩᙉ"): bstack1l11ll1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨᙊ"),
            bstack1l11ll1_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᙋ"): bstack1l11ll1_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬᙌ"),
            bstack1l11ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫᙍ"): bstack11ll1l1l1l1_opy_
        },
        bstack1l11ll1_opy_ (u"ࠬࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧᙎ"): settings,
        bstack1l11ll1_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࡃࡰࡰࡷࡶࡴࡲࠧᙏ"): bstack11ll11ll111_opy_(),
        bstack1l11ll1_opy_ (u"ࠧࡤ࡫ࡌࡲ࡫ࡵࠧᙐ"): bstack1lll11ll1l_opy_(),
        bstack1l11ll1_opy_ (u"ࠨࡪࡲࡷࡹࡏ࡮ࡧࡱࠪᙑ"): get_host_info(),
        bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᙒ"): bstack1llll1llll_opy_(config)
    }
    headers = {
        bstack1l11ll1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩᙓ"): bstack1l11ll1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧᙔ"),
    }
    config = {
        bstack1l11ll1_opy_ (u"ࠬࡧࡵࡵࡪࠪᙕ"): (bstack11ll1lll111_opy_, bstack11ll1l111ll_opy_),
        bstack1l11ll1_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᙖ"): headers
    }
    response = bstack1l1ll1ll1l_opy_(bstack1l11ll1_opy_ (u"ࠧࡑࡑࡖࡘࠬᙗ"), bstack11lll1111l1_opy_ + bstack1l11ll1_opy_ (u"ࠨ࠱ࡹ࠶࠴ࡺࡥࡴࡶࡢࡶࡺࡴࡳࠨᙘ"), data, config)
    bstack11ll11lll1l_opy_ = response.json()
    if bstack11ll11lll1l_opy_[bstack1l11ll1_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪᙙ")]:
      parsed = json.loads(os.getenv(bstack1l11ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᙚ"), bstack1l11ll1_opy_ (u"ࠫࢀࢃࠧᙛ")))
      parsed[bstack1l11ll1_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᙜ")] = bstack11ll11lll1l_opy_[bstack1l11ll1_opy_ (u"࠭ࡤࡢࡶࡤࠫᙝ")][bstack1l11ll1_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᙞ")]
      os.environ[bstack1l11ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᙟ")] = json.dumps(parsed)
      bstack1l11l11l_opy_.bstack1lll1l1l11_opy_(bstack11ll11lll1l_opy_[bstack1l11ll1_opy_ (u"ࠩࡧࡥࡹࡧࠧᙠ")][bstack1l11ll1_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫᙡ")])
      bstack1l11l11l_opy_.bstack11ll1l1llll_opy_(bstack11ll11lll1l_opy_[bstack1l11ll1_opy_ (u"ࠫࡩࡧࡴࡢࠩᙢ")][bstack1l11ll1_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧᙣ")])
      bstack1l11l11l_opy_.store()
      return bstack11ll11lll1l_opy_[bstack1l11ll1_opy_ (u"࠭ࡤࡢࡶࡤࠫᙤ")][bstack1l11ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡔࡰ࡭ࡨࡲࠬᙥ")], bstack11ll11lll1l_opy_[bstack1l11ll1_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᙦ")][bstack1l11ll1_opy_ (u"ࠩ࡬ࡨࠬᙧ")]
    else:
      logger.error(bstack1l11ll1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࠫᙨ") + bstack11ll11lll1l_opy_[bstack1l11ll1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᙩ")])
      if bstack11ll11lll1l_opy_[bstack1l11ll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᙪ")] == bstack1l11ll1_opy_ (u"࠭ࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡱࡣࡶࡷࡪࡪ࠮ࠨᙫ"):
        for bstack11ll1l1lll1_opy_ in bstack11ll11lll1l_opy_[bstack1l11ll1_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧᙬ")]:
          logger.error(bstack11ll1l1lll1_opy_[bstack1l11ll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ᙭")])
      return None, None
  except Exception as error:
    logger.error(bstack1l11ll1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡷࡻ࡮ࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠻ࠢࠥ᙮") +  str(error))
    return None, None
def bstack11ll11lll11_opy_():
  if os.getenv(bstack1l11ll1_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᙯ")) is None:
    return {
        bstack1l11ll1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᙰ"): bstack1l11ll1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᙱ"),
        bstack1l11ll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᙲ"): bstack1l11ll1_opy_ (u"ࠧࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡪࡤࡨࠥ࡬ࡡࡪ࡮ࡨࡨ࠳࠭ᙳ")
    }
  data = {bstack1l11ll1_opy_ (u"ࠨࡧࡱࡨ࡙࡯࡭ࡦࠩᙴ"): bstack1ll11l1ll1_opy_()}
  headers = {
      bstack1l11ll1_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩᙵ"): bstack1l11ll1_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࠫᙶ") + os.getenv(bstack1l11ll1_opy_ (u"ࠦࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠤᙷ")),
      bstack1l11ll1_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫᙸ"): bstack1l11ll1_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩᙹ")
  }
  response = bstack1l1ll1ll1l_opy_(bstack1l11ll1_opy_ (u"ࠧࡑࡗࡗࠫᙺ"), bstack11lll1111l1_opy_ + bstack1l11ll1_opy_ (u"ࠨ࠱ࡷࡩࡸࡺ࡟ࡳࡷࡱࡷ࠴ࡹࡴࡰࡲࠪᙻ"), data, { bstack1l11ll1_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪᙼ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1l11ll1_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡔࡦࡵࡷࠤࡗࡻ࡮ࠡ࡯ࡤࡶࡰ࡫ࡤࠡࡣࡶࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࡪࠠࡢࡶࠣࠦᙽ") + bstack1111ll11l1_opy_().isoformat() + bstack1l11ll1_opy_ (u"ࠫ࡟࠭ᙾ"))
      return {bstack1l11ll1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᙿ"): bstack1l11ll1_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧ "), bstack1l11ll1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᚁ"): bstack1l11ll1_opy_ (u"ࠨࠩᚂ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1l11ll1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡯࡯࡯ࠢࡲࡪࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡖࡨࡷࡹࠦࡒࡶࡰ࠽ࠤࠧᚃ") + str(error))
    return {
        bstack1l11ll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᚄ"): bstack1l11ll1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᚅ"),
        bstack1l11ll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᚆ"): str(error)
    }
def bstack11ll11llll1_opy_(bstack11ll1llllll_opy_):
    return re.match(bstack1l11ll1_opy_ (u"ࡸࠧ࡟࡞ࡧ࠯࠭ࡢ࠮࡝ࡦ࠮࠭ࡄࠪࠧᚇ"), bstack11ll1llllll_opy_.strip()) is not None
def bstack11l1l11111_opy_(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack11ll1l11l11_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11ll1l11l11_opy_ = desired_capabilities
        else:
          bstack11ll1l11l11_opy_ = {}
        bstack1ll11l1111l_opy_ = (bstack11ll1l11l11_opy_.get(bstack1l11ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ᚈ"), bstack1l11ll1_opy_ (u"ࠨࠩᚉ")).lower() or caps.get(bstack1l11ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨᚊ"), bstack1l11ll1_opy_ (u"ࠪࠫᚋ")).lower())
        if bstack1ll11l1111l_opy_ == bstack1l11ll1_opy_ (u"ࠫ࡮ࡵࡳࠨᚌ"):
            return True
        if bstack1ll11l1111l_opy_ == bstack1l11ll1_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩ࠭ᚍ"):
            bstack1ll11l1l1ll_opy_ = str(float(caps.get(bstack1l11ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᚎ")) or bstack11ll1l11l11_opy_.get(bstack1l11ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᚏ"), {}).get(bstack1l11ll1_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫᚐ"),bstack1l11ll1_opy_ (u"ࠩࠪᚑ"))))
            if bstack1ll11l1111l_opy_ == bstack1l11ll1_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࠫᚒ") and int(bstack1ll11l1l1ll_opy_.split(bstack1l11ll1_opy_ (u"ࠫ࠳࠭ᚓ"))[0]) < float(bstack11lll11111l_opy_):
                logger.warning(str(bstack11ll1ll1l1l_opy_))
                return False
            return True
        bstack1ll111l1111_opy_ = caps.get(bstack1l11ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᚔ"), {}).get(bstack1l11ll1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪᚕ"), caps.get(bstack1l11ll1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧᚖ"), bstack1l11ll1_opy_ (u"ࠨࠩᚗ")))
        if bstack1ll111l1111_opy_:
            logger.warning(bstack1l11ll1_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡇࡩࡸࡱࡴࡰࡲࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᚘ"))
            return False
        browser = caps.get(bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᚙ"), bstack1l11ll1_opy_ (u"ࠫࠬᚚ")).lower() or bstack11ll1l11l11_opy_.get(bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ᚛"), bstack1l11ll1_opy_ (u"࠭ࠧ᚜")).lower()
        if browser != bstack1l11ll1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ᚝"):
            logger.warning(bstack1l11ll1_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦ᚞"))
            return False
        browser_version = caps.get(bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ᚟")) or caps.get(bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᚠ")) or bstack11ll1l11l11_opy_.get(bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᚡ")) or bstack11ll1l11l11_opy_.get(bstack1l11ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᚢ"), {}).get(bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᚣ")) or bstack11ll1l11l11_opy_.get(bstack1l11ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᚤ"), {}).get(bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪᚥ"))
        bstack1ll1111ll1l_opy_ = bstack11ll1l11l1l_opy_.bstack1ll11ll11ll_opy_
        bstack11ll1l1ll1l_opy_ = False
        if config is not None:
          bstack11ll1l1ll1l_opy_ = bstack1l11ll1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᚦ") in config and str(config[bstack1l11ll1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧᚧ")]).lower() != bstack1l11ll1_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪᚨ")
        if os.environ.get(bstack1l11ll1_opy_ (u"ࠬࡏࡓࡠࡐࡒࡒࡤࡈࡓࡕࡃࡆࡏࡤࡏࡎࡇࡔࡄࡣࡆ࠷࠱࡚ࡡࡖࡉࡘ࡙ࡉࡐࡐࠪᚩ"), bstack1l11ll1_opy_ (u"࠭ࠧᚪ")).lower() == bstack1l11ll1_opy_ (u"ࠧࡵࡴࡸࡩࠬᚫ") or bstack11ll1l1ll1l_opy_:
          bstack1ll1111ll1l_opy_ = bstack11ll1l11l1l_opy_.bstack1ll111l1ll1_opy_
        if browser_version and browser_version != bstack1l11ll1_opy_ (u"ࠨ࡮ࡤࡸࡪࡹࡴࠨᚬ") and int(browser_version.split(bstack1l11ll1_opy_ (u"ࠩ࠱ࠫᚭ"))[0]) <= bstack1ll1111ll1l_opy_:
          logger.warning(bstack1llll111ll1_opy_ (u"ࠪࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥ࡭ࡲࡦࡣࡷࡩࡷࠦࡴࡩࡣࡱࠤࢀࡳࡩ࡯ࡡࡤ࠵࠶ࡿ࡟ࡴࡷࡳࡴࡴࡸࡴࡦࡦࡢࡧ࡭ࡸ࡯࡮ࡧࡢࡺࡪࡸࡳࡪࡱࡱࢁ࠳࠭ᚮ"))
          return False
        if not options:
          bstack1ll11l1ll11_opy_ = caps.get(bstack1l11ll1_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᚯ")) or bstack11ll1l11l11_opy_.get(bstack1l11ll1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᚰ"), {})
          if bstack1l11ll1_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࠪᚱ") in bstack1ll11l1ll11_opy_.get(bstack1l11ll1_opy_ (u"ࠧࡢࡴࡪࡷࠬᚲ"), []):
              logger.warning(bstack1l11ll1_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡲࡴࡺࠠࡳࡷࡱࠤࡴࡴࠠ࡭ࡧࡪࡥࡨࡿࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠡࡕࡺ࡭ࡹࡩࡨࠡࡶࡲࠤࡳ࡫ࡷࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥࠡࡱࡵࠤࡦࡼ࡯ࡪࡦࠣࡹࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠥᚳ"))
              return False
        return True
    except Exception as error:
        logger.debug(bstack1l11ll1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡸࡤࡰ࡮ࡪࡡࡵࡧࠣࡥ࠶࠷ࡹࠡࡵࡸࡴࡵࡵࡲࡵࠢ࠽ࠦᚴ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1lll11l1l1l_opy_ = config.get(bstack1l11ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᚵ"), {})
    bstack1lll11l1l1l_opy_[bstack1l11ll1_opy_ (u"ࠫࡦࡻࡴࡩࡖࡲ࡯ࡪࡴࠧᚶ")] = os.getenv(bstack1l11ll1_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᚷ"))
    bstack11ll1ll111l_opy_ = json.loads(os.getenv(bstack1l11ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧᚸ"), bstack1l11ll1_opy_ (u"ࠧࡼࡿࠪᚹ"))).get(bstack1l11ll1_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᚺ"))
    if not config[bstack1l11ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫᚻ")].get(bstack1l11ll1_opy_ (u"ࠥࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠤᚼ")):
      if bstack1l11ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᚽ") in caps:
        caps[bstack1l11ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᚾ")][bstack1l11ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᚿ")] = bstack1lll11l1l1l_opy_
        caps[bstack1l11ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᛀ")][bstack1l11ll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᛁ")][bstack1l11ll1_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᛂ")] = bstack11ll1ll111l_opy_
      else:
        caps[bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᛃ")] = bstack1lll11l1l1l_opy_
        caps[bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᛄ")][bstack1l11ll1_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᛅ")] = bstack11ll1ll111l_opy_
  except Exception as error:
    logger.debug(bstack1l11ll1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷ࠳ࠦࡅࡳࡴࡲࡶ࠿ࠦࠢᛆ") +  str(error))
def bstack1lllll11_opy_(driver, bstack11ll1l1l11l_opy_):
  try:
    setattr(driver, bstack1l11ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧᛇ"), True)
    session = driver.session_id
    if session:
      bstack11ll1llll1l_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11ll1llll1l_opy_ = False
      bstack11ll1llll1l_opy_ = url.scheme in [bstack1l11ll1_opy_ (u"ࠣࡪࡷࡸࡵࠨᛈ"), bstack1l11ll1_opy_ (u"ࠤ࡫ࡸࡹࡶࡳࠣᛉ")]
      if bstack11ll1llll1l_opy_:
        if bstack11ll1l1l11l_opy_:
          logger.info(bstack1l11ll1_opy_ (u"ࠥࡗࡪࡺࡵࡱࠢࡩࡳࡷࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡩࡣࡶࠤࡸࡺࡡࡳࡶࡨࡨ࠳ࠦࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡨࡥࡨ࡫ࡱࠤࡲࡵ࡭ࡦࡰࡷࡥࡷ࡯࡬ࡺ࠰ࠥᛊ"))
      return bstack11ll1l1l11l_opy_
  except Exception as e:
    logger.error(bstack1l11ll1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩ࠿ࠦࠢᛋ") + str(e))
    return False
def bstack1l1ll1111_opy_(driver, name, path):
  try:
    bstack1ll1l1111ll_opy_ = {
        bstack1l11ll1_opy_ (u"ࠬࡺࡨࡕࡧࡶࡸࡗࡻ࡮ࡖࡷ࡬ࡨࠬᛌ"): threading.current_thread().current_test_uuid,
        bstack1l11ll1_opy_ (u"࠭ࡴࡩࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫᛍ"): os.environ.get(bstack1l11ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᛎ"), bstack1l11ll1_opy_ (u"ࠨࠩᛏ")),
        bstack1l11ll1_opy_ (u"ࠩࡷ࡬ࡏࡽࡴࡕࡱ࡮ࡩࡳ࠭ᛐ"): os.environ.get(bstack1l11ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᛑ"), bstack1l11ll1_opy_ (u"ࠫࠬᛒ"))
    }
    bstack1ll111l1lll_opy_ = bstack1lll11l1_opy_.bstack1ll111l11ll_opy_(EVENTS.bstack1l1l1l1ll_opy_.value)
    logger.debug(bstack1l11ll1_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡣࡹ࡭ࡳ࡭ࠠࡳࡧࡶࡹࡱࡺࡳࠨᛓ"))
    try:
      if (bstack1l11111ll_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ᛔ"), None) and bstack1l11111ll_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᛕ"), None)):
        scripts = {bstack1l11ll1_opy_ (u"ࠨࡵࡦࡥࡳ࠭ᛖ"): bstack1l11l11l_opy_.perform_scan}
        bstack11ll11lllll_opy_ = json.loads(scripts[bstack1l11ll1_opy_ (u"ࠤࡶࡧࡦࡴࠢᛗ")].replace(bstack1l11ll1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨᛘ"), bstack1l11ll1_opy_ (u"ࠦࠧᛙ")))
        bstack11ll11lllll_opy_[bstack1l11ll1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᛚ")][bstack1l11ll1_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩ࠭ᛛ")] = None
        scripts[bstack1l11ll1_opy_ (u"ࠢࡴࡥࡤࡲࠧᛜ")] = bstack1l11ll1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࠦᛝ") + json.dumps(bstack11ll11lllll_opy_)
        bstack1l11l11l_opy_.bstack1lll1l1l11_opy_(scripts)
        bstack1l11l11l_opy_.store()
        logger.debug(driver.execute_script(bstack1l11l11l_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1l11l11l_opy_.perform_scan, {bstack1l11ll1_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࠤᛞ"): name}))
      bstack1lll11l1_opy_.end(EVENTS.bstack1l1l1l1ll_opy_.value, bstack1ll111l1lll_opy_ + bstack1l11ll1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᛟ"), bstack1ll111l1lll_opy_ + bstack1l11ll1_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᛠ"), True, None)
    except Exception as error:
      bstack1lll11l1_opy_.end(EVENTS.bstack1l1l1l1ll_opy_.value, bstack1ll111l1lll_opy_ + bstack1l11ll1_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᛡ"), bstack1ll111l1lll_opy_ + bstack1l11ll1_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᛢ"), False, str(error))
    bstack1ll111l1lll_opy_ = bstack1lll11l1_opy_.bstack11lll111111_opy_(EVENTS.bstack1ll111l1l1l_opy_.value)
    bstack1lll11l1_opy_.mark(bstack1ll111l1lll_opy_ + bstack1l11ll1_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᛣ"))
    try:
      if (bstack1l11111ll_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨᛤ"), None) and bstack1l11111ll_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫᛥ"), None)):
        scripts = {bstack1l11ll1_opy_ (u"ࠪࡷࡨࡧ࡮ࠨᛦ"): bstack1l11l11l_opy_.perform_scan}
        bstack11ll11lllll_opy_ = json.loads(scripts[bstack1l11ll1_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᛧ")].replace(bstack1l11ll1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠣᛨ"), bstack1l11ll1_opy_ (u"ࠨࠢᛩ")))
        bstack11ll11lllll_opy_[bstack1l11ll1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᛪ")][bstack1l11ll1_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࠨ᛫")] = None
        scripts[bstack1l11ll1_opy_ (u"ࠤࡶࡧࡦࡴࠢ᛬")] = bstack1l11ll1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨ᛭") + json.dumps(bstack11ll11lllll_opy_)
        bstack1l11l11l_opy_.bstack1lll1l1l11_opy_(scripts)
        bstack1l11l11l_opy_.store()
        logger.debug(driver.execute_script(bstack1l11l11l_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1l11l11l_opy_.bstack11ll1ll1l11_opy_, bstack1ll1l1111ll_opy_))
      bstack1lll11l1_opy_.end(bstack1ll111l1lll_opy_, bstack1ll111l1lll_opy_ + bstack1l11ll1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᛮ"), bstack1ll111l1lll_opy_ + bstack1l11ll1_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᛯ"),True, None)
    except Exception as error:
      bstack1lll11l1_opy_.end(bstack1ll111l1lll_opy_, bstack1ll111l1lll_opy_ + bstack1l11ll1_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᛰ"), bstack1ll111l1lll_opy_ + bstack1l11ll1_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᛱ"),False, str(error))
    logger.info(bstack1l11ll1_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠦᛲ"))
  except Exception as bstack1ll11l1l111_opy_:
    logger.error(bstack1l11ll1_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡧࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡢࡦࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦ࠼ࠣࠦᛳ") + str(path) + bstack1l11ll1_opy_ (u"ࠥࠤࡊࡸࡲࡰࡴࠣ࠾ࠧᛴ") + str(bstack1ll11l1l111_opy_))
def bstack11ll1ll1ll1_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack1l11ll1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥᛵ")) and str(caps.get(bstack1l11ll1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦᛶ"))).lower() == bstack1l11ll1_opy_ (u"ࠨࡡ࡯ࡦࡵࡳ࡮ࡪࠢᛷ"):
        bstack1ll11l1l1ll_opy_ = caps.get(bstack1l11ll1_opy_ (u"ࠢࡢࡲࡳ࡭ࡺࡳ࠺ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤᛸ")) or caps.get(bstack1l11ll1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥ᛹"))
        if bstack1ll11l1l1ll_opy_ and int(str(bstack1ll11l1l1ll_opy_)) < bstack11lll11111l_opy_:
            return False
    return True
def bstack1l111l11l1_opy_(config):
  if bstack1l11ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ᛺") in config:
        return config[bstack1l11ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ᛻")]
  for platform in config.get(bstack1l11ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ᛼"), []):
      if bstack1l11ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ᛽") in platform:
          return platform[bstack1l11ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭᛾")]
  return None
def bstack11l1lll11l_opy_(bstack11lll1111_opy_):
  try:
    browser_name = bstack11lll1111_opy_[bstack1l11ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡰࡤࡱࡪ࠭᛿")]
    browser_version = bstack11lll1111_opy_[bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪᜀ")]
    chrome_options = bstack11lll1111_opy_[bstack1l11ll1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡡࡲࡴࡹ࡯࡯࡯ࡵࠪᜁ")]
    try:
        bstack11ll1l111l1_opy_ = int(browser_version.split(bstack1l11ll1_opy_ (u"ࠪ࠲ࠬᜂ"))[0])
    except ValueError as e:
        logger.error(bstack1l11ll1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡦࡳࡳࡼࡥࡳࡶ࡬ࡲ࡬ࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠣᜃ") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack1l11ll1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬᜄ")):
        logger.warning(bstack1l11ll1_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤᜅ"))
        return False
    if bstack11ll1l111l1_opy_ < bstack11ll1l11l1l_opy_.bstack1ll111l1ll1_opy_:
        logger.warning(bstack1llll111ll1_opy_ (u"ࠧࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡷ࡫ࡱࡶ࡫ࡵࡩࡸࠦࡃࡩࡴࡲࡱࡪࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡼࡅࡒࡒࡘ࡚ࡁࡏࡖࡖ࠲ࡒࡏࡎࡊࡏࡘࡑࡤࡔࡏࡏࡡࡅࡗ࡙ࡇࡃࡌࡡࡌࡒࡋࡘࡁࡠࡃ࠴࠵࡞ࡥࡓࡖࡒࡓࡓࡗ࡚ࡅࡅࡡࡆࡌࡗࡕࡍࡆࡡ࡙ࡉࡗ࡙ࡉࡐࡐࢀࠤࡴࡸࠠࡩ࡫ࡪ࡬ࡪࡸ࠮ࠨᜆ"))
        return False
    if chrome_options and any(bstack1l11ll1_opy_ (u"ࠨ࠯࠰࡬ࡪࡧࡤ࡭ࡧࡶࡷࠬᜇ") in value for value in chrome_options.values() if isinstance(value, str)):
        logger.warning(bstack1l11ll1_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡳࡵࡴࠡࡴࡸࡲࠥࡵ࡮ࠡ࡮ࡨ࡫ࡦࡩࡹࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠢࡖࡻ࡮ࡺࡣࡩࠢࡷࡳࠥࡴࡥࡸࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦࠢࡲࡶࠥࡧࡶࡰ࡫ࡧࠤࡺࡹࡩ࡯ࡩࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠦᜈ"))
        return False
    return True
  except Exception as e:
    logger.error(bstack1l11ll1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡩࡨࡦࡥ࡮࡭ࡳ࡭ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡶࡹࡵࡶ࡯ࡳࡶࠣࡪࡴࡸࠠ࡭ࡱࡦࡥࡱࠦࡃࡩࡴࡲࡱࡪࡀࠠࠣᜉ") + str(e))
    return False
def bstack1111111ll_opy_(bstack1l1l111l_opy_, config):
    try:
      bstack1ll11l11lll_opy_ = bstack1l11ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᜊ") in config and config[bstack1l11ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᜋ")] == True
      bstack11ll1l1ll1l_opy_ = bstack1l11ll1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪᜌ") in config and str(config[bstack1l11ll1_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫᜍ")]).lower() != bstack1l11ll1_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧᜎ")
      if not (bstack1ll11l11lll_opy_ and (not bstack1llll1llll_opy_(config) or bstack11ll1l1ll1l_opy_)):
        return bstack1l1l111l_opy_
      bstack11ll1lll1ll_opy_ = bstack1l11l11l_opy_.bstack11ll1ll11ll_opy_
      if bstack11ll1lll1ll_opy_ is None:
        logger.debug(bstack1l11ll1_opy_ (u"ࠤࡊࡳࡴ࡭࡬ࡦࠢࡦ࡬ࡷࡵ࡭ࡦࠢࡲࡴࡹ࡯࡯࡯ࡵࠣࡥࡷ࡫ࠠࡏࡱࡱࡩࠧᜏ"))
        return bstack1l1l111l_opy_
      bstack11ll1lll1l1_opy_ = int(str(bstack11ll1lllll1_opy_()).split(bstack1l11ll1_opy_ (u"ࠪ࠲ࠬᜐ"))[0])
      logger.debug(bstack1l11ll1_opy_ (u"ࠦࡘ࡫࡬ࡦࡰ࡬ࡹࡲࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡥࡧࡷࡩࡨࡺࡥࡥ࠼ࠣࠦᜑ") + str(bstack11ll1lll1l1_opy_) + bstack1l11ll1_opy_ (u"ࠧࠨᜒ"))
      if bstack11ll1lll1l1_opy_ == 3 and isinstance(bstack1l1l111l_opy_, dict) and bstack1l11ll1_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᜓ") in bstack1l1l111l_opy_ and bstack11ll1lll1ll_opy_ is not None:
        if bstack1l11ll1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷ᜔ࠬ") not in bstack1l1l111l_opy_[bstack1l11ll1_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ᜕")]:
          bstack1l1l111l_opy_[bstack1l11ll1_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ᜖")][bstack1l11ll1_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ᜗")] = {}
        if bstack1l11ll1_opy_ (u"ࠫࡦࡸࡧࡴࠩ᜘") in bstack11ll1lll1ll_opy_:
          if bstack1l11ll1_opy_ (u"ࠬࡧࡲࡨࡵࠪ᜙") not in bstack1l1l111l_opy_[bstack1l11ll1_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭᜚")][bstack1l11ll1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ᜛")]:
            bstack1l1l111l_opy_[bstack1l11ll1_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ᜜")][bstack1l11ll1_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᜝")][bstack1l11ll1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ᜞")] = []
          for arg in bstack11ll1lll1ll_opy_[bstack1l11ll1_opy_ (u"ࠫࡦࡸࡧࡴࠩᜟ")]:
            if arg not in bstack1l1l111l_opy_[bstack1l11ll1_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᜠ")][bstack1l11ll1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᜡ")][bstack1l11ll1_opy_ (u"ࠧࡢࡴࡪࡷࠬᜢ")]:
              bstack1l1l111l_opy_[bstack1l11ll1_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᜣ")][bstack1l11ll1_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᜤ")][bstack1l11ll1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᜥ")].append(arg)
        if bstack1l11ll1_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨᜦ") in bstack11ll1lll1ll_opy_:
          if bstack1l11ll1_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᜧ") not in bstack1l1l111l_opy_[bstack1l11ll1_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᜨ")][bstack1l11ll1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᜩ")]:
            bstack1l1l111l_opy_[bstack1l11ll1_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᜪ")][bstack1l11ll1_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᜫ")][bstack1l11ll1_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᜬ")] = []
          for ext in bstack11ll1lll1ll_opy_[bstack1l11ll1_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨᜭ")]:
            if ext not in bstack1l1l111l_opy_[bstack1l11ll1_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᜮ")][bstack1l11ll1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᜯ")][bstack1l11ll1_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᜰ")]:
              bstack1l1l111l_opy_[bstack1l11ll1_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᜱ")][bstack1l11ll1_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᜲ")][bstack1l11ll1_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᜳ")].append(ext)
        if bstack1l11ll1_opy_ (u"ࠫࡵࡸࡥࡧࡵ᜴ࠪ") in bstack11ll1lll1ll_opy_:
          if bstack1l11ll1_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ᜵") not in bstack1l1l111l_opy_[bstack1l11ll1_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭᜶")][bstack1l11ll1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ᜷")]:
            bstack1l1l111l_opy_[bstack1l11ll1_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ᜸")][bstack1l11ll1_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᜹")][bstack1l11ll1_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩ᜺")] = {}
          bstack11ll1l1111l_opy_(bstack1l1l111l_opy_[bstack1l11ll1_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ᜻")][bstack1l11ll1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ᜼")][bstack1l11ll1_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬ᜽")],
                    bstack11ll1lll1ll_opy_[bstack1l11ll1_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭᜾")])
        os.environ[bstack1l11ll1_opy_ (u"ࠨࡋࡖࡣࡓࡕࡎࡠࡄࡖࡘࡆࡉࡋࡠࡋࡑࡊࡗࡇ࡟ࡂ࠳࠴࡝ࡤ࡙ࡅࡔࡕࡌࡓࡓ࠭᜿")] = bstack1l11ll1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᝀ")
        return bstack1l1l111l_opy_
      else:
        chrome_options = None
        if isinstance(bstack1l1l111l_opy_, ChromeOptions):
          chrome_options = bstack1l1l111l_opy_
        elif isinstance(bstack1l1l111l_opy_, dict):
          for value in bstack1l1l111l_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack1l1l111l_opy_, dict):
            bstack1l1l111l_opy_[bstack1l11ll1_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫᝁ")] = chrome_options
          else:
            bstack1l1l111l_opy_ = chrome_options
        if bstack11ll1lll1ll_opy_ is not None:
          if bstack1l11ll1_opy_ (u"ࠫࡦࡸࡧࡴࠩᝂ") in bstack11ll1lll1ll_opy_:
                bstack11ll1l11ll1_opy_ = chrome_options.arguments or []
                new_args = bstack11ll1lll1ll_opy_[bstack1l11ll1_opy_ (u"ࠬࡧࡲࡨࡵࠪᝃ")]
                for arg in new_args:
                    if arg not in bstack11ll1l11ll1_opy_:
                        chrome_options.add_argument(arg)
          if bstack1l11ll1_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᝄ") in bstack11ll1lll1ll_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack1l11ll1_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᝅ"), [])
                bstack11ll11ll1ll_opy_ = bstack11ll1lll1ll_opy_[bstack1l11ll1_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᝆ")]
                for extension in bstack11ll11ll1ll_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack1l11ll1_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᝇ") in bstack11ll1lll1ll_opy_:
                bstack11ll1lll11l_opy_ = chrome_options.experimental_options.get(bstack1l11ll1_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᝈ"), {})
                bstack11ll1l1l111_opy_ = bstack11ll1lll1ll_opy_[bstack1l11ll1_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪᝉ")]
                bstack11ll1l1111l_opy_(bstack11ll1lll11l_opy_, bstack11ll1l1l111_opy_)
                chrome_options.add_experimental_option(bstack1l11ll1_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫᝊ"), bstack11ll1lll11l_opy_)
        os.environ[bstack1l11ll1_opy_ (u"࠭ࡉࡔࡡࡑࡓࡓࡥࡂࡔࡖࡄࡇࡐࡥࡉࡏࡈࡕࡅࡤࡇ࠱࠲࡛ࡢࡗࡊ࡙ࡓࡊࡑࡑࠫᝋ")] = bstack1l11ll1_opy_ (u"ࠧࡵࡴࡸࡩࠬᝌ")
        return bstack1l1l111l_opy_
    except Exception as e:
      logger.error(bstack1l11ll1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡡࡥࡦ࡬ࡲ࡬ࠦ࡮ࡰࡰ࠰ࡆࡘࠦࡩ࡯ࡨࡵࡥࠥࡧ࠱࠲ࡻࠣࡧ࡭ࡸ࡯࡮ࡧࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࠨᝍ") + str(e))
      return bstack1l1l111l_opy_