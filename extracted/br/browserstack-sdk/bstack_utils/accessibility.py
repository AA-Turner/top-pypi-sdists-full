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
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack11l11l111l1_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack11l111lll11_opy_ as bstack11l11l1111l_opy_, EVENTS
from bstack_utils.bstack11ll11llll_opy_ import bstack11ll11llll_opy_
from bstack_utils.helper import current_time, bstack1111111l11_opy_, bstack11l1llllll_opy_, bstack11l111ll1l1_opy_, \
  bstack11l11lll111_opy_, bstack1llll111_opy_, get_host_info, bstack11l11ll1111_opy_, bstack1l1l11ll_opy_, error_handler, bstack11l1l111111_opy_, bstack11l11lll1ll_opy_, bstack1lll11l111_opy_
from browserstack_sdk._version import __version__
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack11111111l_opy_ import bstack1111l1l1l_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
from bstack_utils import logger_utils
logger = get_logger(__name__)
bstack1l1ll1ll11_opy_ = logger_utils.bstack11l1l11ll_opy_(__name__)
bstack11111111l_opy_ = bstack1111l1l1l_opy_()
@error_handler(class_method=False)
def _11l11llll1l_opy_(driver, bstack1lll1lllll1_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack11ll111_opy_ (u"ࠧࡰࡵࡢࡲࡦࡳࡥࠨ៻"): caps.get(bstack11ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧ៼"), None),
        bstack11ll111_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭៽"): bstack1lll1lllll1_opy_.get(bstack11ll111_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭៾"), None),
        bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧࠪ៿"): caps.get(bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ᠀"), None),
        bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ᠁"): caps.get(bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᠂"), None)
    }
  except Exception as error:
    logger.debug(bstack11ll111_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩ࡫ࡴࡢ࡫࡯ࡷࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳࠢ࠽ࠤࠬ᠃") + str(error))
  return response
def on():
    if os.environ.get(bstack11ll111_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ᠄"), None) is None or os.environ[bstack11ll111_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ᠅")] == bstack11ll111_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ᠆"):
        return False
    return True
def bstack1ll1ll1111_opy_(config):
  return config.get(bstack11ll111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ᠇"), False) or any([p.get(bstack11ll111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭᠈"), False) == True for p in config.get(bstack11ll111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ᠉"), [])])
def bstack11l1111ll_opy_(config, bstack1l111l111_opy_):
  try:
    bstack11l111llll1_opy_ = config.get(bstack11ll111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ᠊"), False)
    if int(bstack1l111l111_opy_) < len(config.get(bstack11ll111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ᠋"), [])) and config[bstack11ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭᠌")][bstack1l111l111_opy_]:
      bstack11l111lllll_opy_ = config[bstack11ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ᠍")][bstack1l111l111_opy_].get(bstack11ll111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ᠎"), None)
    else:
      bstack11l111lllll_opy_ = config.get(bstack11ll111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭᠏"), None)
    if bstack11l111lllll_opy_ != None:
      bstack11l111llll1_opy_ = bstack11l111lllll_opy_
    bstack11l11ll1ll1_opy_ = os.getenv(bstack11ll111_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ᠐")) is not None and len(os.getenv(bstack11ll111_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭᠑"))) > 0 and os.getenv(bstack11ll111_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ᠒")) != bstack11ll111_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ᠓")
    return bstack11l111llll1_opy_ and bstack11l11ll1ll1_opy_
  except Exception as error:
    logger.debug(bstack11ll111_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡺࡪࡸࡩࡧࡻ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡪࡹࡳࡪࡱࡱࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲࠡ࠼ࠣࠫ᠔") + str(error))
  return False
def bstack1l11ll1111_opy_(test_tags):
  bstack1l1l1llllll_opy_ = os.getenv(bstack11ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭᠕"))
  if bstack1l1l1llllll_opy_ is None:
    return True
  bstack1l1l1llllll_opy_ = json.loads(bstack1l1l1llllll_opy_)
  try:
    include_tags = bstack1l1l1llllll_opy_[bstack11ll111_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫ᠖")] if bstack11ll111_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬ᠗") in bstack1l1l1llllll_opy_ and isinstance(bstack1l1l1llllll_opy_[bstack11ll111_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭᠘")], list) else []
    exclude_tags = bstack1l1l1llllll_opy_[bstack11ll111_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ᠙")] if bstack11ll111_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨ᠚") in bstack1l1l1llllll_opy_ and isinstance(bstack1l1l1llllll_opy_[bstack11ll111_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ᠛")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack11ll111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡺࡦࡲࡩࡥࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡥࡤࡲࡳ࡯࡮ࡨ࠰ࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠤࠧ᠜") + str(error))
  return False
def bstack11l11ll11ll_opy_(config, bstack11l11l111ll_opy_, bstack11l11l1llll_opy_, bstack11l11l11111_opy_):
  bstack11l11l1ll1l_opy_ = bstack11l111ll1l1_opy_(config)
  bstack11l11l1lll1_opy_ = bstack11l11lll111_opy_(config)
  if bstack11l11l1ll1l_opy_ is None or bstack11l11l1lll1_opy_ is None:
    logger.error(bstack11ll111_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࡍࡪࡵࡶ࡭ࡳ࡭ࠠࡢࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡࡶࡲ࡯ࡪࡴࠧ᠝"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack11ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ᠞"), bstack11ll111_opy_ (u"ࠨࡽࢀࠫ᠟")))
    data = {
        bstack11ll111_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᠠ"): config[bstack11ll111_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᠡ")],
        bstack11ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᠢ"): config.get(bstack11ll111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᠣ"), os.path.basename(os.getcwd())),
        bstack11ll111_opy_ (u"࠭ࡳࡵࡣࡵࡸ࡙࡯࡭ࡦࠩᠤ"): current_time(),
        bstack11ll111_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᠥ"): config.get(bstack11ll111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᠦ"), bstack11ll111_opy_ (u"ࠩࠪᠧ")),
        bstack11ll111_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪᠨ"): {
            bstack11ll111_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨࠫᠩ"): bstack11l11l111ll_opy_,
            bstack11ll111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᠪ"): bstack11l11l1llll_opy_,
            bstack11ll111_opy_ (u"࠭ࡳࡥ࡭࡙ࡩࡷࡹࡩࡰࡰࠪᠫ"): __version__,
            bstack11ll111_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩᠬ"): bstack11ll111_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨᠭ"),
            bstack11ll111_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᠮ"): bstack11ll111_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬᠯ"),
            bstack11ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫᠰ"): bstack11l11l11111_opy_
        },
        bstack11ll111_opy_ (u"ࠬࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧᠱ"): settings,
        bstack11ll111_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࡃࡰࡰࡷࡶࡴࡲࠧᠲ"): bstack11l11ll1111_opy_(),
        bstack11ll111_opy_ (u"ࠧࡤ࡫ࡌࡲ࡫ࡵࠧᠳ"): bstack1llll111_opy_(),
        bstack11ll111_opy_ (u"ࠨࡪࡲࡷࡹࡏ࡮ࡧࡱࠪᠴ"): get_host_info(),
        bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᠵ"): bstack11l1llllll_opy_(config)
    }
    headers = {
        bstack11ll111_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩᠶ"): bstack11ll111_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧᠷ"),
    }
    config = {
        bstack11ll111_opy_ (u"ࠬࡧࡵࡵࡪࠪᠸ"): (bstack11l11l1ll1l_opy_, bstack11l11l1lll1_opy_),
        bstack11ll111_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᠹ"): headers
    }
    response = bstack1l1l11ll_opy_(bstack11ll111_opy_ (u"ࠧࡑࡑࡖࡘࠬᠺ"), bstack11l11l1111l_opy_ + bstack11ll111_opy_ (u"ࠨ࠱ࡹ࠶࠴ࡺࡥࡴࡶࡢࡶࡺࡴࡳࠨᠻ"), data, config)
    bstack11l11l1l11l_opy_ = response.json()
    if bstack11l11l1l11l_opy_[bstack11ll111_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪᠼ")]:
      parsed = json.loads(os.getenv(bstack11ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᠽ"), bstack11ll111_opy_ (u"ࠫࢀࢃࠧᠾ")))
      parsed[bstack11ll111_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᠿ")] = bstack11l11l1l11l_opy_[bstack11ll111_opy_ (u"࠭ࡤࡢࡶࡤࠫᡀ")][bstack11ll111_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᡁ")]
      os.environ[bstack11ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᡂ")] = json.dumps(parsed)
      bstack11ll11llll_opy_.bstack11llll1l1_opy_(bstack11l11l1l11l_opy_[bstack11ll111_opy_ (u"ࠩࡧࡥࡹࡧࠧᡃ")][bstack11ll111_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫᡄ")])
      bstack11ll11llll_opy_.bstack11l11llllll_opy_(bstack11l11l1l11l_opy_[bstack11ll111_opy_ (u"ࠫࡩࡧࡴࡢࠩᡅ")][bstack11ll111_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧᡆ")])
      bstack11ll11llll_opy_.store()
      return bstack11l11l1l11l_opy_[bstack11ll111_opy_ (u"࠭ࡤࡢࡶࡤࠫᡇ")][bstack11ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡔࡰ࡭ࡨࡲࠬᡈ")], bstack11l11l1l11l_opy_[bstack11ll111_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᡉ")][bstack11ll111_opy_ (u"ࠩ࡬ࡨࠬᡊ")]
    else:
      logger.error(bstack11ll111_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࠫᡋ") + bstack11l11l1l11l_opy_[bstack11ll111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᡌ")])
      if bstack11l11l1l11l_opy_[bstack11ll111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᡍ")] == bstack11ll111_opy_ (u"࠭ࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡱࡣࡶࡷࡪࡪ࠮ࠨᡎ"):
        for bstack11l1l1111ll_opy_ in bstack11l11l1l11l_opy_[bstack11ll111_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧᡏ")]:
          logger.error(bstack11l1l1111ll_opy_[bstack11ll111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᡐ")])
      return None, None
  except Exception as error:
    logger.error(bstack11ll111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡷࡻ࡮ࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠻ࠢࠥᡑ") +  str(error))
    return None, None
def bstack11l11l11l1l_opy_():
  if os.getenv(bstack11ll111_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᡒ")) is None:
    return {
        bstack11ll111_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᡓ"): bstack11ll111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᡔ"),
        bstack11ll111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᡕ"): bstack11ll111_opy_ (u"ࠧࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡪࡤࡨࠥ࡬ࡡࡪ࡮ࡨࡨ࠳࠭ᡖ")
    }
  data = {bstack11ll111_opy_ (u"ࠨࡧࡱࡨ࡙࡯࡭ࡦࠩᡗ"): current_time()}
  headers = {
      bstack11ll111_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩᡘ"): bstack11ll111_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࠫᡙ") + os.getenv(bstack11ll111_opy_ (u"ࠦࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠤᡚ")),
      bstack11ll111_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫᡛ"): bstack11ll111_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩᡜ")
  }
  response = bstack1l1l11ll_opy_(bstack11ll111_opy_ (u"ࠧࡑࡗࡗࠫᡝ"), bstack11l11l1111l_opy_ + bstack11ll111_opy_ (u"ࠨ࠱ࡷࡩࡸࡺ࡟ࡳࡷࡱࡷ࠴ࡹࡴࡰࡲࠪᡞ"), data, { bstack11ll111_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪᡟ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack11ll111_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡔࡦࡵࡷࠤࡗࡻ࡮ࠡ࡯ࡤࡶࡰ࡫ࡤࠡࡣࡶࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࡪࠠࡢࡶࠣࠦᡠ") + bstack1111111l11_opy_().isoformat() + bstack11ll111_opy_ (u"ࠫ࡟࠭ᡡ"))
      return {bstack11ll111_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᡢ"): bstack11ll111_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧᡣ"), bstack11ll111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᡤ"): bstack11ll111_opy_ (u"ࠨࠩᡥ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack11ll111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡯࡯࡯ࠢࡲࡪࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡖࡨࡷࡹࠦࡒࡶࡰ࠽ࠤࠧᡦ") + str(error))
    return {
        bstack11ll111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᡧ"): bstack11ll111_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᡨ"),
        bstack11ll111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᡩ"): str(error)
    }
def bstack11l1l1111l1_opy_(bstack11l11l1ll11_opy_):
    return re.match(bstack11ll111_opy_ (u"ࡸࠧ࡟࡞ࡧ࠯࠭ࡢ࠮࡝ࡦ࠮࠭ࡄࠪࠧᡪ"), bstack11l11l1ll11_opy_.strip()) is not None
def bstack1l1lllll1l_opy_(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack11l11lll1l1_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11l11lll1l1_opy_ = desired_capabilities
        else:
          bstack11l11lll1l1_opy_ = {}
        bstack1l1l11l1lll_opy_ = (bstack11l11lll1l1_opy_.get(bstack11ll111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ᡫ"), bstack11ll111_opy_ (u"ࠨࠩᡬ")).lower() or caps.get(bstack11ll111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨᡭ"), bstack11ll111_opy_ (u"ࠪࠫᡮ")).lower())
        if bstack1l1l11l1lll_opy_ == bstack11ll111_opy_ (u"ࠫ࡮ࡵࡳࠨᡯ"):
            return True
        if bstack1l1l11l1lll_opy_ == bstack11ll111_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩ࠭ᡰ"):
            bstack1l1l1l1ll11_opy_ = str(float(caps.get(bstack11ll111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᡱ")) or bstack11l11lll1l1_opy_.get(bstack11ll111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᡲ"), {}).get(bstack11ll111_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫᡳ"),bstack11ll111_opy_ (u"ࠩࠪᡴ"))))
            if bstack1l1l11l1lll_opy_ == bstack11ll111_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࠫᡵ") and int(bstack1l1l1l1ll11_opy_.split(bstack11ll111_opy_ (u"ࠫ࠳࠭ᡶ"))[0]) < float(bstack11l11l1l1l1_opy_):
                logger.warning(str(bstack11l11l1l1ll_opy_))
                return False
            return True
        bstack1l1l1l1lll1_opy_ = caps.get(bstack11ll111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᡷ"), {}).get(bstack11ll111_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪᡸ"), caps.get(bstack11ll111_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ᡹"), bstack11ll111_opy_ (u"ࠨࠩ᡺")))
        if bstack1l1l1l1lll1_opy_:
            logger.warning(bstack11ll111_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡇࡩࡸࡱࡴࡰࡲࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨ᡻"))
            return False
        browser = caps.get(bstack11ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ᡼"), bstack11ll111_opy_ (u"ࠫࠬ᡽")).lower() or bstack11l11lll1l1_opy_.get(bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ᡾"), bstack11ll111_opy_ (u"࠭ࠧ᡿")).lower()
        if browser != bstack11ll111_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧᢀ"):
            logger.warning(bstack11ll111_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦᢁ"))
            return False
        browser_version = caps.get(bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᢂ")) or caps.get(bstack11ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᢃ")) or bstack11l11lll1l1_opy_.get(bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᢄ")) or bstack11l11lll1l1_opy_.get(bstack11ll111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᢅ"), {}).get(bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᢆ")) or bstack11l11lll1l1_opy_.get(bstack11ll111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᢇ"), {}).get(bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪᢈ"))
        bstack1l1ll1l1l1l_opy_ = bstack11l11l111l1_opy_.bstack1l1ll111111_opy_
        bstack11l11llll11_opy_ = False
        if config is not None:
          bstack11l11llll11_opy_ = bstack11ll111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᢉ") in config and str(config[bstack11ll111_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧᢊ")]).lower() != bstack11ll111_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪᢋ")
        if os.environ.get(bstack11ll111_opy_ (u"ࠬࡏࡓࡠࡐࡒࡒࡤࡈࡓࡕࡃࡆࡏࡤࡏࡎࡇࡔࡄࡣࡆ࠷࠱࡚ࡡࡖࡉࡘ࡙ࡉࡐࡐࠪᢌ"), bstack11ll111_opy_ (u"࠭ࠧᢍ")).lower() == bstack11ll111_opy_ (u"ࠧࡵࡴࡸࡩࠬᢎ") or bstack11l11llll11_opy_:
          bstack1l1ll1l1l1l_opy_ = bstack11l11l111l1_opy_.bstack1l1ll11l11l_opy_
        if browser_version and browser_version != bstack11ll111_opy_ (u"ࠨ࡮ࡤࡸࡪࡹࡴࠨᢏ") and int(browser_version.split(bstack11ll111_opy_ (u"ࠩ࠱ࠫᢐ"))[0]) <= bstack1l1ll1l1l1l_opy_:
          logger.warning(bstack1lll11111l1_opy_ (u"ࠪࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥ࡭ࡲࡦࡣࡷࡩࡷࠦࡴࡩࡣࡱࠤࢀࡳࡩ࡯ࡡࡤ࠵࠶ࡿ࡟ࡴࡷࡳࡴࡴࡸࡴࡦࡦࡢࡧ࡭ࡸ࡯࡮ࡧࡢࡺࡪࡸࡳࡪࡱࡱࢁ࠳࠭ᢑ"))
          return False
        if not options:
          bstack1l1ll1ll11l_opy_ = caps.get(bstack11ll111_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᢒ")) or bstack11l11lll1l1_opy_.get(bstack11ll111_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᢓ"), {})
          if bstack11ll111_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࠪᢔ") in bstack1l1ll1ll11l_opy_.get(bstack11ll111_opy_ (u"ࠧࡢࡴࡪࡷࠬᢕ"), []):
              logger.warning(bstack11ll111_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡲࡴࡺࠠࡳࡷࡱࠤࡴࡴࠠ࡭ࡧࡪࡥࡨࡿࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠡࡕࡺ࡭ࡹࡩࡨࠡࡶࡲࠤࡳ࡫ࡷࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥࠡࡱࡵࠤࡦࡼ࡯ࡪࡦࠣࡹࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠥᢖ"))
              return False
        return True
    except Exception as error:
        logger.debug(bstack11ll111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡸࡤࡰ࡮ࡪࡡࡵࡧࠣࡥ࠶࠷ࡹࠡࡵࡸࡴࡵࡵࡲࡵࠢ࠽ࠦᢗ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1ll11llll1l_opy_ = config.get(bstack11ll111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᢘ"), {})
    bstack1ll11llll1l_opy_[bstack11ll111_opy_ (u"ࠫࡦࡻࡴࡩࡖࡲ࡯ࡪࡴࠧᢙ")] = os.getenv(bstack11ll111_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᢚ"))
    bstack11l11ll1l1l_opy_ = json.loads(os.getenv(bstack11ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧᢛ"), bstack11ll111_opy_ (u"ࠧࡼࡿࠪᢜ"))).get(bstack11ll111_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᢝ"))
    if not config[bstack11ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫᢞ")].get(bstack11ll111_opy_ (u"ࠥࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠤᢟ")):
      if bstack11ll111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᢠ") in caps:
        caps[bstack11ll111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᢡ")][bstack11ll111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᢢ")] = bstack1ll11llll1l_opy_
        caps[bstack11ll111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᢣ")][bstack11ll111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᢤ")][bstack11ll111_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᢥ")] = bstack11l11ll1l1l_opy_
      else:
        caps[bstack11ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᢦ")] = bstack1ll11llll1l_opy_
        caps[bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᢧ")][bstack11ll111_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᢨ")] = bstack11l11ll1l1l_opy_
  except Exception as error:
    logger.debug(bstack11ll111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷ࠳ࠦࡅࡳࡴࡲࡶ࠿ᢩࠦࠢ") +  str(error))
def bstack11lll111l1_opy_(driver, bstack11l1l11111l_opy_):
  try:
    setattr(driver, bstack11ll111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧᢪ"), True)
    session = driver.session_id
    if session:
      bstack11l11lll11l_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11l11lll11l_opy_ = False
      bstack11l11lll11l_opy_ = url.scheme in [bstack11ll111_opy_ (u"ࠣࡪࡷࡸࡵࠨ᢫"), bstack11ll111_opy_ (u"ࠤ࡫ࡸࡹࡶࡳࠣ᢬")]
      if bstack11l11lll11l_opy_:
        if bstack11l1l11111l_opy_:
          logger.info(bstack11ll111_opy_ (u"ࠥࡗࡪࡺࡵࡱࠢࡩࡳࡷࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡩࡣࡶࠤࡸࡺࡡࡳࡶࡨࡨ࠳ࠦࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡨࡥࡨ࡫ࡱࠤࡲࡵ࡭ࡦࡰࡷࡥࡷ࡯࡬ࡺ࠰ࠥ᢭"))
      return bstack11l1l11111l_opy_
  except Exception as e:
    logger.error(bstack11ll111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩ࠿ࠦࠢ᢮") + str(e))
    return False
def bstack111l1l11l1_opy_(driver, name, path):
  try:
    bstack1l1ll11ll1l_opy_ = {
        bstack11ll111_opy_ (u"ࠬࡺࡨࡕࡧࡶࡸࡗࡻ࡮ࡖࡷ࡬ࡨࠬ᢯"): threading.current_thread().current_test_uuid,
        bstack11ll111_opy_ (u"࠭ࡴࡩࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫᢰ"): os.environ.get(bstack11ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᢱ"), bstack11ll111_opy_ (u"ࠨࠩᢲ")),
        bstack11ll111_opy_ (u"ࠩࡷ࡬ࡏࡽࡴࡕࡱ࡮ࡩࡳ࠭ᢳ"): os.environ.get(bstack11ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᢴ"), bstack11ll111_opy_ (u"ࠫࠬᢵ"))
    }
    bstack11llllllll_opy_ = bstack11111111l_opy_.bstack1ll111l11_opy_(EVENTS.bstack111ll111ll_opy_.value)
    logger.debug(bstack11ll111_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡣࡹ࡭ࡳ࡭ࠠࡳࡧࡶࡹࡱࡺࡳࠨᢶ"))
    try:
      if (bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ᢷ"), None) and bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᢸ"), None)):
        scripts = {bstack11ll111_opy_ (u"ࠨࡵࡦࡥࡳ࠭ᢹ"): bstack11ll11llll_opy_.perform_scan}
        bstack11l11ll1l11_opy_ = json.loads(scripts[bstack11ll111_opy_ (u"ࠤࡶࡧࡦࡴࠢᢺ")].replace(bstack11ll111_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨᢻ"), bstack11ll111_opy_ (u"ࠦࠧᢼ")))
        bstack11l11ll1l11_opy_[bstack11ll111_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᢽ")][bstack11ll111_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩ࠭ᢾ")] = None
        scripts[bstack11ll111_opy_ (u"ࠢࡴࡥࡤࡲࠧᢿ")] = bstack11ll111_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࠦᣀ") + json.dumps(bstack11l11ll1l11_opy_)
        bstack11ll11llll_opy_.bstack11llll1l1_opy_(scripts)
        bstack11ll11llll_opy_.store()
        logger.debug(driver.execute_script(bstack11ll11llll_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack11ll11llll_opy_.perform_scan, {bstack11ll111_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࠤᣁ"): name}))
      bstack11111111l_opy_.end(EVENTS.bstack111ll111ll_opy_.value, bstack11llllllll_opy_ + bstack11ll111_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᣂ"), bstack11llllllll_opy_ + bstack11ll111_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᣃ"), True, None)
    except Exception as error:
      bstack11111111l_opy_.end(EVENTS.bstack111ll111ll_opy_.value, bstack11llllllll_opy_ + bstack11ll111_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᣄ"), bstack11llllllll_opy_ + bstack11ll111_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᣅ"), False, str(error))
    bstack11llllllll_opy_ = bstack11111111l_opy_.bstack11l11ll11l1_opy_(EVENTS.bstack1l1ll1l11l1_opy_.value)
    bstack11111111l_opy_.mark(bstack11llllllll_opy_ + bstack11ll111_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᣆ"))
    try:
      if (bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨᣇ"), None) and bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫᣈ"), None)):
        scripts = {bstack11ll111_opy_ (u"ࠪࡷࡨࡧ࡮ࠨᣉ"): bstack11ll11llll_opy_.perform_scan}
        bstack11l11ll1l11_opy_ = json.loads(scripts[bstack11ll111_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᣊ")].replace(bstack11ll111_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠣᣋ"), bstack11ll111_opy_ (u"ࠨࠢᣌ")))
        bstack11l11ll1l11_opy_[bstack11ll111_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᣍ")][bstack11ll111_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࠨᣎ")] = None
        scripts[bstack11ll111_opy_ (u"ࠤࡶࡧࡦࡴࠢᣏ")] = bstack11ll111_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨᣐ") + json.dumps(bstack11l11ll1l11_opy_)
        bstack11ll11llll_opy_.bstack11llll1l1_opy_(scripts)
        bstack11ll11llll_opy_.store()
        logger.debug(driver.execute_script(bstack11ll11llll_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack11ll11llll_opy_.bstack11l111ll11l_opy_, bstack1l1ll11ll1l_opy_))
      bstack11111111l_opy_.end(bstack11llllllll_opy_, bstack11llllllll_opy_ + bstack11ll111_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᣑ"), bstack11llllllll_opy_ + bstack11ll111_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᣒ"),True, None)
    except Exception as error:
      bstack11111111l_opy_.end(bstack11llllllll_opy_, bstack11llllllll_opy_ + bstack11ll111_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᣓ"), bstack11llllllll_opy_ + bstack11ll111_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᣔ"),False, str(error))
    logger.info(bstack11ll111_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠦᣕ"))
    try:
      bstack1l1l1lll111_opy_ = {
        bstack11ll111_opy_ (u"ࠤࡵࡩࡶࡻࡥࡴࡶࠥᣖ"): {
          bstack11ll111_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࠦᣗ"): bstack11ll111_opy_ (u"ࠦࡆ࠷࠱࡚ࡡࡖࡅ࡛ࡋ࡟ࡓࡇࡖ࡙ࡑ࡚ࡓࠣᣘ"),
        },
        bstack11ll111_opy_ (u"ࠧࡸࡥࡴࡲࡲࡲࡸ࡫ࠢᣙ"): {
          bstack11ll111_opy_ (u"ࠨࡢࡰࡦࡼࠦᣚ"): {
            bstack11ll111_opy_ (u"ࠢ࡮ࡵࡪࠦᣛ"): bstack11ll111_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠦᣜ"),
            bstack11ll111_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥᣝ"): True
          }
        }
      }
      bstack1l1ll1ll11_opy_.info(json.dumps(bstack1l1l1lll111_opy_, separators=(bstack11ll111_opy_ (u"ࠪ࠰ࠬᣞ"), bstack11ll111_opy_ (u"ࠫ࠿࠭ᣟ"))))
    except Exception as bstack111lll11l1_opy_:
      logger.debug(bstack11ll111_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡮ࡲ࡫ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡡࡷࡧࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡩࡧࡴࡢ࠼ࠣࠦᣠ") + str(bstack111lll11l1_opy_) + bstack11ll111_opy_ (u"ࠨࠢᣡ"))
  except Exception as bstack1l1l1l11lll_opy_:
    logger.error(bstack11ll111_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡥࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡧ࡫ࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡪࡴࡸࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤᣢ") + str(path) + bstack11ll111_opy_ (u"ࠣࠢࡈࡶࡷࡵࡲࠡ࠼ࠥᣣ") + str(bstack1l1l1l11lll_opy_))
def bstack11l11ll1lll_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack11ll111_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣᣤ")) and str(caps.get(bstack11ll111_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤᣥ"))).lower() == bstack11ll111_opy_ (u"ࠦࡦࡴࡤࡳࡱ࡬ࡨࠧᣦ"):
        bstack1l1l1l1ll11_opy_ = caps.get(bstack11ll111_opy_ (u"ࠧࡧࡰࡱ࡫ࡸࡱ࠿ࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢᣧ")) or caps.get(bstack11ll111_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣᣨ"))
        if bstack1l1l1l1ll11_opy_ and int(str(bstack1l1l1l1ll11_opy_)) < bstack11l11l1l1l1_opy_:
            return False
    return True
def bstack1l1lll11_opy_(config):
  if bstack11ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᣩ") in config:
        return config[bstack11ll111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᣪ")]
  for platform in config.get(bstack11ll111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᣫ"), []):
      if bstack11ll111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᣬ") in platform:
          return platform[bstack11ll111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᣭ")]
  return None
def bstack11ll1llll_opy_(bstack1l11l11ll_opy_):
  try:
    browser_name = bstack1l11l11ll_opy_[bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫᣮ")]
    browser_version = bstack1l11l11ll_opy_[bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᣯ")]
    chrome_options = bstack1l11l11ll_opy_[bstack11ll111_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫࡟ࡰࡲࡷ࡭ࡴࡴࡳࠨᣰ")]
    try:
        bstack11l111ll1ll_opy_ = int(browser_version.split(bstack11ll111_opy_ (u"ࠨ࠰ࠪᣱ"))[0])
    except ValueError as e:
        logger.error(bstack11ll111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡱࡱࡺࡪࡸࡴࡪࡰࡪࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࡼࡥࡳࡵ࡬ࡳࡳࠨᣲ") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack11ll111_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪᣳ")):
        logger.warning(bstack11ll111_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢᣴ"))
        return False
    if bstack11l111ll1ll_opy_ < bstack11l11l111l1_opy_.bstack1l1ll11l11l_opy_:
        logger.warning(bstack1lll11111l1_opy_ (u"ࠬࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡵࡩࡶࡻࡩࡳࡧࡶࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࢁࡃࡐࡐࡖࡘࡆࡔࡔࡔ࠰ࡐࡍࡓࡏࡍࡖࡏࡢࡒࡔࡔ࡟ࡃࡕࡗࡅࡈࡑ࡟ࡊࡐࡉࡖࡆࡥࡁ࠲࠳࡜ࡣࡘ࡛ࡐࡑࡑࡕࡘࡊࡊ࡟ࡄࡊࡕࡓࡒࡋ࡟ࡗࡇࡕࡗࡎࡕࡎࡾࠢࡲࡶࠥ࡮ࡩࡨࡪࡨࡶ࠳࠭ᣵ"))
        return False
    if chrome_options and any(bstack11ll111_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࠪ᣶") in value for value in chrome_options.values() if isinstance(value, str)):
        logger.warning(bstack11ll111_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡱࡳࡹࠦࡲࡶࡰࠣࡳࡳࠦ࡬ࡦࡩࡤࡧࡾࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠠࡔࡹ࡬ࡸࡨ࡮ࠠࡵࡱࠣࡲࡪࡽࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫ࠠࡰࡴࠣࡥࡻࡵࡩࡥࠢࡸࡷ࡮ࡴࡧࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠤ᣷"))
        return False
    return True
  except Exception as e:
    logger.error(bstack11ll111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡧ࡭࡫ࡣ࡬࡫ࡱ࡫ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡴࡷࡳࡴࡴࡸࡴࠡࡨࡲࡶࠥࡲ࡯ࡤࡣ࡯ࠤࡈ࡮ࡲࡰ࡯ࡨ࠾ࠥࠨ᣸") + str(e))
    return False
def bstack1l111ll11_opy_(bstack11111lll1_opy_, config):
    try:
      bstack1l1l1ll111l_opy_ = bstack11ll111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ᣹") in config and config[bstack11ll111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ᣺")] == True
      bstack11l11llll11_opy_ = bstack11ll111_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ᣻") in config and str(config[bstack11ll111_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ᣼")]).lower() != bstack11ll111_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ᣽")
      if not (bstack1l1l1ll111l_opy_ and (not bstack11l1llllll_opy_(config) or bstack11l11llll11_opy_)):
        return bstack11111lll1_opy_
      bstack11l11l11lll_opy_ = bstack11ll11llll_opy_.bstack11l11l1l111_opy_
      if bstack11l11l11lll_opy_ is None:
        logger.debug(bstack11ll111_opy_ (u"ࠢࡈࡱࡲ࡫ࡱ࡫ࠠࡤࡪࡵࡳࡲ࡫ࠠࡰࡲࡷ࡭ࡴࡴࡳࠡࡣࡵࡩࠥࡔ࡯࡯ࡧࠥ᣾"))
        return bstack11111lll1_opy_
      bstack11l11lllll1_opy_ = int(str(bstack11l11lll1ll_opy_()).split(bstack11ll111_opy_ (u"ࠨ࠰ࠪ᣿"))[0])
      logger.debug(bstack11ll111_opy_ (u"ࠤࡖࡩࡱ࡫࡮ࡪࡷࡰࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡪࡥࡵࡧࡦࡸࡪࡪ࠺ࠡࠤᤀ") + str(bstack11l11lllll1_opy_) + bstack11ll111_opy_ (u"ࠥࠦᤁ"))
      if bstack11l11lllll1_opy_ == 3 and isinstance(bstack11111lll1_opy_, dict) and bstack11ll111_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᤂ") in bstack11111lll1_opy_ and bstack11l11l11lll_opy_ is not None:
        if bstack11ll111_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᤃ") not in bstack11111lll1_opy_[bstack11ll111_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᤄ")]:
          bstack11111lll1_opy_[bstack11ll111_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᤅ")][bstack11ll111_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᤆ")] = {}
        if bstack11ll111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᤇ") in bstack11l11l11lll_opy_:
          if bstack11ll111_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᤈ") not in bstack11111lll1_opy_[bstack11ll111_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᤉ")][bstack11ll111_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᤊ")]:
            bstack11111lll1_opy_[bstack11ll111_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᤋ")][bstack11ll111_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᤌ")][bstack11ll111_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᤍ")] = []
          for arg in bstack11l11l11lll_opy_[bstack11ll111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᤎ")]:
            if arg not in bstack11111lll1_opy_[bstack11ll111_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᤏ")][bstack11ll111_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᤐ")][bstack11ll111_opy_ (u"ࠬࡧࡲࡨࡵࠪᤑ")]:
              bstack11111lll1_opy_[bstack11ll111_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᤒ")][bstack11ll111_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᤓ")][bstack11ll111_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᤔ")].append(arg)
        if bstack11ll111_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᤕ") in bstack11l11l11lll_opy_:
          if bstack11ll111_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᤖ") not in bstack11111lll1_opy_[bstack11ll111_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᤗ")][bstack11ll111_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᤘ")]:
            bstack11111lll1_opy_[bstack11ll111_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᤙ")][bstack11ll111_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᤚ")][bstack11ll111_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᤛ")] = []
          for ext in bstack11l11l11lll_opy_[bstack11ll111_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᤜ")]:
            if ext not in bstack11111lll1_opy_[bstack11ll111_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᤝ")][bstack11ll111_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᤞ")][bstack11ll111_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩ᤟")]:
              bstack11111lll1_opy_[bstack11ll111_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᤠ")][bstack11ll111_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᤡ")][bstack11ll111_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᤢ")].append(ext)
        if bstack11ll111_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᤣ") in bstack11l11l11lll_opy_:
          if bstack11ll111_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᤤ") not in bstack11111lll1_opy_[bstack11ll111_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᤥ")][bstack11ll111_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᤦ")]:
            bstack11111lll1_opy_[bstack11ll111_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᤧ")][bstack11ll111_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᤨ")][bstack11ll111_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᤩ")] = {}
          bstack11l1l111111_opy_(bstack11111lll1_opy_[bstack11ll111_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᤪ")][bstack11ll111_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᤫ")][bstack11ll111_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪ᤬")],
                    bstack11l11l11lll_opy_[bstack11ll111_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ᤭")])
        os.environ[bstack11ll111_opy_ (u"࠭ࡉࡔࡡࡑࡓࡓࡥࡂࡔࡖࡄࡇࡐࡥࡉࡏࡈࡕࡅࡤࡇ࠱࠲࡛ࡢࡗࡊ࡙ࡓࡊࡑࡑࠫ᤮")] = bstack11ll111_opy_ (u"ࠧࡵࡴࡸࡩࠬ᤯")
        return bstack11111lll1_opy_
      else:
        chrome_options = None
        if isinstance(bstack11111lll1_opy_, ChromeOptions):
          chrome_options = bstack11111lll1_opy_
        elif isinstance(bstack11111lll1_opy_, dict):
          for value in bstack11111lll1_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack11111lll1_opy_, dict):
            bstack11111lll1_opy_[bstack11ll111_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩᤰ")] = chrome_options
          else:
            bstack11111lll1_opy_ = chrome_options
        if bstack11l11l11lll_opy_ is not None:
          if bstack11ll111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᤱ") in bstack11l11l11lll_opy_:
                bstack11l111lll1l_opy_ = chrome_options.arguments or []
                new_args = bstack11l11l11lll_opy_[bstack11ll111_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᤲ")]
                for arg in new_args:
                    if arg not in bstack11l111lll1l_opy_:
                        chrome_options.add_argument(arg)
          if bstack11ll111_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨᤳ") in bstack11l11l11lll_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack11ll111_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᤴ"), [])
                bstack11l11l11ll1_opy_ = bstack11l11l11lll_opy_[bstack11ll111_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᤵ")]
                for extension in bstack11l11l11ll1_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack11ll111_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ᤶ") in bstack11l11l11lll_opy_:
                bstack11l11ll111l_opy_ = chrome_options.experimental_options.get(bstack11ll111_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᤷ"), {})
                bstack11l11l11l11_opy_ = bstack11l11l11lll_opy_[bstack11ll111_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᤸ")]
                bstack11l1l111111_opy_(bstack11l11ll111l_opy_, bstack11l11l11l11_opy_)
                chrome_options.add_experimental_option(bstack11ll111_opy_ (u"ࠪࡴࡷ࡫ࡦࡴ᤹ࠩ"), bstack11l11ll111l_opy_)
        os.environ[bstack11ll111_opy_ (u"ࠫࡎ࡙࡟ࡏࡑࡑࡣࡇ࡙ࡔࡂࡅࡎࡣࡎࡔࡆࡓࡃࡢࡅ࠶࠷࡙ࡠࡕࡈࡗࡘࡏࡏࡏࠩ᤺")] = bstack11ll111_opy_ (u"ࠬࡺࡲࡶࡧ᤻ࠪ")
        return bstack11111lll1_opy_
    except Exception as e:
      logger.error(bstack11ll111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡦࡪࡤࡪࡰࡪࠤࡳࡵ࡮࠮ࡄࡖࠤ࡮ࡴࡦࡳࡣࠣࡥ࠶࠷ࡹࠡࡥ࡫ࡶࡴࡳࡥࠡࡱࡳࡸ࡮ࡵ࡮ࡴ࠼ࠣࠦ᤼") + str(e))
      return bstack11111lll1_opy_