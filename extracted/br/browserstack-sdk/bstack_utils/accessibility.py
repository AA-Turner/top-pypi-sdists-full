# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack11l11l1l1l1_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack11l11l1l11l_opy_ as bstack11l1l111111_opy_, EVENTS
from bstack_utils.bstack111llllll1_opy_ import bstack111llllll1_opy_
from bstack_utils.helper import current_time, bstack1llllll1lll_opy_, bstack1lll1l1l_opy_, bstack11l11l1111l_opy_, \
  bstack11l11l11l11_opy_, bstack1l111l1lll_opy_, get_host_info, bstack11l11ll11ll_opy_, bstack11l11llll_opy_, error_handler, bstack11l1l1111ll_opy_, bstack11l111ll1ll_opy_, bstack11llll11l1_opy_
from browserstack_sdk._version import __version__
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack111lll111l_opy_ import bstack11ll1l1l1_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
from bstack_utils import logger_utils
logger = get_logger(__name__)
bstack11ll111ll_opy_ = logger_utils.bstack1lll1lll_opy_(__name__)
bstack111lll111l_opy_ = bstack11ll1l1l1_opy_()
@error_handler(class_method=False)
def _11l11llll1l_opy_(driver, bstack1llll1lllll_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack11l1l11_opy_ (u"ࠪࡳࡸࡥ࡮ࡢ࡯ࡨࠫ៾"): caps.get(bstack11l1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪ៿"), None),
        bstack11l1l11_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ᠀"): bstack1llll1lllll_opy_.get(bstack11l1l11_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ᠁"), None),
        bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡰࡤࡱࡪ࠭᠂"): caps.get(bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭᠃"), None),
        bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫ᠄"): caps.get(bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ᠅"), None)
    }
  except Exception as error:
    logger.debug(bstack11l1l11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡥࡧࡷࡥ࡮ࡲࡳࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶࠥࡀࠠࠨ᠆") + str(error))
  return response
def on():
    if os.environ.get(bstack11l1l11_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ᠇"), None) is None or os.environ[bstack11l1l11_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ᠈")] == bstack11l1l11_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ᠉"):
        return False
    return True
def bstack111l1ll1l_opy_(config):
  return config.get(bstack11l1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ᠊"), False) or any([p.get(bstack11l1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ᠋"), False) == True for p in config.get(bstack11l1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭᠌"), [])])
def bstack111ll1111l_opy_(config, bstack1ll11ll1l1_opy_):
  try:
    bstack11l11l1ll11_opy_ = config.get(bstack11l1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ᠍"), False)
    if int(bstack1ll11ll1l1_opy_) < len(config.get(bstack11l1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ᠎"), [])) and config[bstack11l1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ᠏")][bstack1ll11ll1l1_opy_]:
      bstack11l11ll1111_opy_ = config[bstack11l1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ᠐")][bstack1ll11ll1l1_opy_].get(bstack11l1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ᠑"), None)
    else:
      bstack11l11ll1111_opy_ = config.get(bstack11l1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ᠒"), None)
    if bstack11l11ll1111_opy_ != None:
      bstack11l11l1ll11_opy_ = bstack11l11ll1111_opy_
    bstack11l11ll111l_opy_ = os.getenv(bstack11l1l11_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ᠓")) is not None and len(os.getenv(bstack11l1l11_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ᠔"))) > 0 and os.getenv(bstack11l1l11_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ᠕")) != bstack11l1l11_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ᠖")
    return bstack11l11l1ll11_opy_ and bstack11l11ll111l_opy_
  except Exception as error:
    logger.debug(bstack11l1l11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡶࡦࡴ࡬ࡪࡾ࡯࡮ࡨࠢࡷ࡬ࡪࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵࠤ࠿ࠦࠧ᠗") + str(error))
  return False
def bstack11ll1lll1l_opy_(test_tags):
  bstack1l1l1lllll1_opy_ = os.getenv(bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩ᠘"))
  if bstack1l1l1lllll1_opy_ is None:
    return True
  bstack1l1l1lllll1_opy_ = json.loads(bstack1l1l1lllll1_opy_)
  try:
    include_tags = bstack1l1l1lllll1_opy_[bstack11l1l11_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ᠙")] if bstack11l1l11_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨ᠚") in bstack1l1l1lllll1_opy_ and isinstance(bstack1l1l1lllll1_opy_[bstack11l1l11_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ᠛")], list) else []
    exclude_tags = bstack1l1l1lllll1_opy_[bstack11l1l11_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ᠜")] if bstack11l1l11_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫ᠝") in bstack1l1l1lllll1_opy_ and isinstance(bstack1l1l1lllll1_opy_[bstack11l1l11_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬ᠞")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack11l1l11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡶࡢ࡮࡬ࡨࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡦࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡨࡧ࡮࡯࡫ࡱ࡫࠳ࠦࡅࡳࡴࡲࡶࠥࡀࠠࠣ᠟") + str(error))
  return False
def bstack11l11l111ll_opy_(config, bstack11l11ll1lll_opy_, bstack11l11l11ll1_opy_, bstack11l11lllll1_opy_):
  bstack11l11lll1ll_opy_ = bstack11l11l1111l_opy_(config)
  bstack11l11l11111_opy_ = bstack11l11l11l11_opy_(config)
  if bstack11l11lll1ll_opy_ is None or bstack11l11l11111_opy_ is None:
    logger.error(bstack11l1l11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡷࡻ࡮ࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠻ࠢࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡥࡺࡺࡨࡦࡰࡷ࡭ࡨࡧࡴࡪࡱࡱࠤࡹࡵ࡫ࡦࡰࠪᠠ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᠡ"), bstack11l1l11_opy_ (u"ࠫࢀࢃࠧᠢ")))
    data = {
        bstack11l1l11_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᠣ"): config[bstack11l1l11_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᠤ")],
        bstack11l1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᠥ"): config.get(bstack11l1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᠦ"), os.path.basename(os.getcwd())),
        bstack11l1l11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡕ࡫ࡰࡩࠬᠧ"): current_time(),
        bstack11l1l11_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᠨ"): config.get(bstack11l1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧᠩ"), bstack11l1l11_opy_ (u"ࠬ࠭ᠪ")),
        bstack11l1l11_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ᠫ"): {
            bstack11l1l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡑࡥࡲ࡫ࠧᠬ"): bstack11l11ll1lll_opy_,
            bstack11l1l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫᠭ"): bstack11l11l11ll1_opy_,
            bstack11l1l11_opy_ (u"ࠩࡶࡨࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᠮ"): __version__,
            bstack11l1l11_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬᠯ"): bstack11l1l11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫᠰ"),
            bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᠱ"): bstack11l1l11_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨᠲ"),
            bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧᠳ"): bstack11l11lllll1_opy_
        },
        bstack11l1l11_opy_ (u"ࠨࡵࡨࡸࡹ࡯࡮ࡨࡵࠪᠴ"): settings,
        bstack11l1l11_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࡆࡳࡳࡺࡲࡰ࡮ࠪᠵ"): bstack11l11ll11ll_opy_(),
        bstack11l1l11_opy_ (u"ࠪࡧ࡮ࡏ࡮ࡧࡱࠪᠶ"): bstack1l111l1lll_opy_(),
        bstack11l1l11_opy_ (u"ࠫ࡭ࡵࡳࡵࡋࡱࡪࡴ࠭ᠷ"): get_host_info(),
        bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᠸ"): bstack1lll1l1l_opy_(config)
    }
    headers = {
        bstack11l1l11_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬᠹ"): bstack11l1l11_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪᠺ"),
    }
    config = {
        bstack11l1l11_opy_ (u"ࠨࡣࡸࡸ࡭࠭ᠻ"): (bstack11l11lll1ll_opy_, bstack11l11l11111_opy_),
        bstack11l1l11_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪᠼ"): headers
    }
    response = bstack11l11llll_opy_(bstack11l1l11_opy_ (u"ࠪࡔࡔ࡙ࡔࠨᠽ"), bstack11l1l111111_opy_ + bstack11l1l11_opy_ (u"ࠫ࠴ࡼ࠲࠰ࡶࡨࡷࡹࡥࡲࡶࡰࡶࠫᠾ"), data, config)
    bstack11l11l11lll_opy_ = response.json()
    if bstack11l11l11lll_opy_[bstack11l1l11_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ᠿ")]:
      parsed = json.loads(os.getenv(bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧᡀ"), bstack11l1l11_opy_ (u"ࠧࡼࡿࠪᡁ")))
      parsed[bstack11l1l11_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᡂ")] = bstack11l11l11lll_opy_[bstack11l1l11_opy_ (u"ࠩࡧࡥࡹࡧࠧᡃ")][bstack11l1l11_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᡄ")]
      os.environ[bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᡅ")] = json.dumps(parsed)
      bstack111llllll1_opy_.bstack11l11l1ll_opy_(bstack11l11l11lll_opy_[bstack11l1l11_opy_ (u"ࠬࡪࡡࡵࡣࠪᡆ")][bstack11l1l11_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧᡇ")])
      bstack111llllll1_opy_.bstack11l111lllll_opy_(bstack11l11l11lll_opy_[bstack11l1l11_opy_ (u"ࠧࡥࡣࡷࡥࠬᡈ")][bstack11l1l11_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪᡉ")])
      bstack111llllll1_opy_.store()
      return bstack11l11l11lll_opy_[bstack11l1l11_opy_ (u"ࠩࡧࡥࡹࡧࠧᡊ")][bstack11l1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡗࡳࡰ࡫࡮ࠨᡋ")], bstack11l11l11lll_opy_[bstack11l1l11_opy_ (u"ࠫࡩࡧࡴࡢࠩᡌ")][bstack11l1l11_opy_ (u"ࠬ࡯ࡤࠨᡍ")]
    else:
      logger.error(bstack11l1l11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡴࡸࡲࡳ࡯࡮ࡨࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࠧᡎ") + bstack11l11l11lll_opy_[bstack11l1l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᡏ")])
      if bstack11l11l11lll_opy_[bstack11l1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᡐ")] == bstack11l1l11_opy_ (u"ࠩࡌࡲࡻࡧ࡬ࡪࡦࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡴࡦࡹࡳࡦࡦ࠱ࠫᡑ"):
        for bstack11l11l11l1l_opy_ in bstack11l11l11lll_opy_[bstack11l1l11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡵࠪᡒ")]:
          logger.error(bstack11l11l11l1l_opy_[bstack11l1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᡓ")])
      return None, None
  except Exception as error:
    logger.error(bstack11l1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡳࡷࡱࠤ࡫ࡵࡲࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥࠨᡔ") +  str(error))
    return None, None
def bstack11l1l1111l1_opy_():
  if os.getenv(bstack11l1l11_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᡕ")) is None:
    return {
        bstack11l1l11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᡖ"): bstack11l1l11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᡗ"),
        bstack11l1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᡘ"): bstack11l1l11_opy_ (u"ࠪࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤ࡭ࡧࡤࠡࡨࡤ࡭ࡱ࡫ࡤ࠯ࠩᡙ")
    }
  data = {bstack11l1l11_opy_ (u"ࠫࡪࡴࡤࡕ࡫ࡰࡩࠬᡚ"): current_time()}
  headers = {
      bstack11l1l11_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬᡛ"): bstack11l1l11_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࠧᡜ") + os.getenv(bstack11l1l11_opy_ (u"ࠢࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠧᡝ")),
      bstack11l1l11_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧᡞ"): bstack11l1l11_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬᡟ")
  }
  response = bstack11l11llll_opy_(bstack11l1l11_opy_ (u"ࠪࡔ࡚࡚ࠧᡠ"), bstack11l1l111111_opy_ + bstack11l1l11_opy_ (u"ࠫ࠴ࡺࡥࡴࡶࡢࡶࡺࡴࡳ࠰ࡵࡷࡳࡵ࠭ᡡ"), data, { bstack11l1l11_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᡢ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack11l1l11_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡗࡩࡸࡺࠠࡓࡷࡱࠤࡲࡧࡲ࡬ࡧࡧࠤࡦࡹࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࡦࠣࡥࡹࠦࠢᡣ") + bstack1llllll1lll_opy_().isoformat() + bstack11l1l11_opy_ (u"࡛ࠧࠩᡤ"))
      return {bstack11l1l11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᡥ"): bstack11l1l11_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪᡦ"), bstack11l1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᡧ"): bstack11l1l11_opy_ (u"ࠫࠬᡨ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack11l1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡥࡲࡱࡵࡲࡥࡵ࡫ࡲࡲࠥࡵࡦࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤ࡙࡫ࡳࡵࠢࡕࡹࡳࡀࠠࠣᡩ") + str(error))
    return {
        bstack11l1l11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᡪ"): bstack11l1l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᡫ"),
        bstack11l1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᡬ"): str(error)
    }
def bstack11l11l111l1_opy_(bstack11l111llll1_opy_):
    return re.match(bstack11l1l11_opy_ (u"ࡴࠪࡢࡡࡪࠫࠩ࡞࠱ࡠࡩ࠱ࠩࡀࠦࠪᡭ"), bstack11l111llll1_opy_.strip()) is not None
def bstack11l1llllll_opy_(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack11l11ll1l11_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11l11ll1l11_opy_ = desired_capabilities
        else:
          bstack11l11ll1l11_opy_ = {}
        bstack1l1ll11ll1l_opy_ = (bstack11l11ll1l11_opy_.get(bstack11l1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩᡮ"), bstack11l1l11_opy_ (u"ࠫࠬᡯ")).lower() or caps.get(bstack11l1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫᡰ"), bstack11l1l11_opy_ (u"࠭ࠧᡱ")).lower())
        if bstack1l1ll11ll1l_opy_ == bstack11l1l11_opy_ (u"ࠧࡪࡱࡶࠫᡲ"):
            return True
        if bstack1l1ll11ll1l_opy_ == bstack11l1l11_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࠩᡳ"):
            bstack1l1ll1ll1l1_opy_ = str(float(caps.get(bstack11l1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫᡴ")) or bstack11l11ll1l11_opy_.get(bstack11l1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᡵ"), {}).get(bstack11l1l11_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧᡶ"),bstack11l1l11_opy_ (u"ࠬ࠭ᡷ"))))
            if bstack1l1ll11ll1l_opy_ == bstack11l1l11_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࠧᡸ") and int(bstack1l1ll1ll1l1_opy_.split(bstack11l1l11_opy_ (u"ࠧ࠯ࠩ᡹"))[0]) < float(bstack11l11ll1ll1_opy_):
                logger.warning(str(bstack11l11l1l111_opy_))
                return False
            return True
        bstack1l1ll1111ll_opy_ = caps.get(bstack11l1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᡺"), {}).get(bstack11l1l11_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭᡻"), caps.get(bstack11l1l11_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪ᡼"), bstack11l1l11_opy_ (u"ࠫࠬ᡽")))
        if bstack1l1ll1111ll_opy_:
            logger.warning(bstack11l1l11_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡊࡥࡴ࡭ࡷࡳࡵࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤ᡾"))
            return False
        browser = caps.get(bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ᡿"), bstack11l1l11_opy_ (u"ࠧࠨᢀ")).lower() or bstack11l11ll1l11_opy_.get(bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᢁ"), bstack11l1l11_opy_ (u"ࠩࠪᢂ")).lower()
        if browser != bstack11l1l11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪᢃ"):
            logger.warning(bstack11l1l11_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢᢄ"))
            return False
        browser_version = caps.get(bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᢅ")) or caps.get(bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᢆ")) or bstack11l11ll1l11_opy_.get(bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᢇ")) or bstack11l11ll1l11_opy_.get(bstack11l1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᢈ"), {}).get(bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᢉ")) or bstack11l11ll1l11_opy_.get(bstack11l1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᢊ"), {}).get(bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᢋ"))
        bstack1l1ll111lll_opy_ = bstack11l11l1l1l1_opy_.bstack1l1ll11l111_opy_
        bstack11l11l1l1ll_opy_ = False
        if config is not None:
          bstack11l11l1l1ll_opy_ = bstack11l1l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩᢌ") in config and str(config[bstack11l1l11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪᢍ")]).lower() != bstack11l1l11_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ᢎ")
        if os.environ.get(bstack11l1l11_opy_ (u"ࠨࡋࡖࡣࡓࡕࡎࡠࡄࡖࡘࡆࡉࡋࡠࡋࡑࡊࡗࡇ࡟ࡂ࠳࠴࡝ࡤ࡙ࡅࡔࡕࡌࡓࡓ࠭ᢏ"), bstack11l1l11_opy_ (u"ࠩࠪᢐ")).lower() == bstack11l1l11_opy_ (u"ࠪࡸࡷࡻࡥࠨᢑ") or bstack11l11l1l1ll_opy_:
          bstack1l1ll111lll_opy_ = bstack11l11l1l1l1_opy_.bstack1l1ll1l1l1l_opy_
        if browser_version and browser_version != bstack11l1l11_opy_ (u"ࠫࡱࡧࡴࡦࡵࡷࠫᢒ") and int(browser_version.split(bstack11l1l11_opy_ (u"ࠬ࠴ࠧᢓ"))[0]) <= bstack1l1ll111lll_opy_:
          logger.warning(bstack1lll11l11ll_opy_ (u"࠭ࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡩࡵࡩࡦࡺࡥࡳࠢࡷ࡬ࡦࡴࠠࡼ࡯࡬ࡲࡤࡧ࠱࠲ࡻࡢࡷࡺࡶࡰࡰࡴࡷࡩࡩࡥࡣࡩࡴࡲࡱࡪࡥࡶࡦࡴࡶ࡭ࡴࡴࡽ࠯ࠩᢔ"))
          return False
        if not options:
          bstack1l1l1lll111_opy_ = caps.get(bstack11l1l11_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᢕ")) or bstack11l11ll1l11_opy_.get(bstack11l1l11_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᢖ"), {})
          if bstack11l1l11_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸ࠭ᢗ") in bstack1l1l1lll111_opy_.get(bstack11l1l11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᢘ"), []):
              logger.warning(bstack11l1l11_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦ࡮ࡰࡶࠣࡶࡺࡴࠠࡰࡰࠣࡰࡪ࡭ࡡࡤࡻࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠤࡘࡽࡩࡵࡥ࡫ࠤࡹࡵࠠ࡯ࡧࡺࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠤࡴࡸࠠࡢࡸࡲ࡭ࡩࠦࡵࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠨᢙ"))
              return False
        return True
    except Exception as error:
        logger.debug(bstack11l1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻࡧ࡬ࡪࡦࡤࡸࡪࠦࡡ࠲࠳ࡼࠤࡸࡻࡰࡱࡱࡵࡸࠥࡀࠢᢚ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1l1llllll11_opy_ = config.get(bstack11l1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᢛ"), {})
    bstack1l1llllll11_opy_[bstack11l1l11_opy_ (u"ࠧࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪᢜ")] = os.getenv(bstack11l1l11_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᢝ"))
    bstack11l1l111l11_opy_ = json.loads(os.getenv(bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᢞ"), bstack11l1l11_opy_ (u"ࠪࡿࢂ࠭ᢟ"))).get(bstack11l1l11_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᢠ"))
    if not config[bstack11l1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧᢡ")].get(bstack11l1l11_opy_ (u"ࠨࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠧᢢ")):
      if bstack11l1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᢣ") in caps:
        caps[bstack11l1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᢤ")][bstack11l1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᢥ")] = bstack1l1llllll11_opy_
        caps[bstack11l1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᢦ")][bstack11l1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᢧ")][bstack11l1l11_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᢨ")] = bstack11l1l111l11_opy_
      else:
        caps[bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷᢩࠬ")] = bstack1l1llllll11_opy_
        caps[bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᢪ")][bstack11l1l11_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ᢫")] = bstack11l1l111l11_opy_
  except Exception as error:
    logger.debug(bstack11l1l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠯ࠢࡈࡶࡷࡵࡲ࠻ࠢࠥ᢬") +  str(error))
def bstack111ll1ll11_opy_(driver, bstack11l11lll111_opy_):
  try:
    setattr(driver, bstack11l1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪ᢭"), True)
    session = driver.session_id
    if session:
      bstack11l111lll11_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11l111lll11_opy_ = False
      bstack11l111lll11_opy_ = url.scheme in [bstack11l1l11_opy_ (u"ࠦ࡭ࡺࡴࡱࠤ᢮"), bstack11l1l11_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦ᢯")]
      if bstack11l111lll11_opy_:
        if bstack11l11lll111_opy_:
          logger.info(bstack11l1l11_opy_ (u"ࠨࡓࡦࡶࡸࡴࠥ࡬࡯ࡳࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡬ࡦࡹࠠࡴࡶࡤࡶࡹ࡫ࡤ࠯ࠢࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡤࡨ࡫࡮ࡴࠠ࡮ࡱࡰࡩࡳࡺࡡࡳ࡫࡯ࡽ࠳ࠨᢰ"))
      return bstack11l11lll111_opy_
  except Exception as e:
    logger.error(bstack11l1l11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡣࡵࡸ࡮ࡴࡧࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡣࡢࡰࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥ࠻ࠢࠥᢱ") + str(e))
    return False
def bstack1l111ll1l1_opy_(driver, name, path):
  try:
    bstack1l1l1l1l1l1_opy_ = {
        bstack11l1l11_opy_ (u"ࠨࡶ࡫ࡘࡪࡹࡴࡓࡷࡱ࡙ࡺ࡯ࡤࠨᢲ"): threading.current_thread().current_test_uuid,
        bstack11l1l11_opy_ (u"ࠩࡷ࡬ࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧᢳ"): os.environ.get(bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᢴ"), bstack11l1l11_opy_ (u"ࠫࠬᢵ")),
        bstack11l1l11_opy_ (u"ࠬࡺࡨࡋࡹࡷࡘࡴࡱࡥ࡯ࠩᢶ"): os.environ.get(bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪᢷ"), bstack11l1l11_opy_ (u"ࠧࠨᢸ"))
    }
    bstack1l1l1l1111_opy_ = bstack111lll111l_opy_.bstack1l11l111ll_opy_(EVENTS.bstack1l11llll_opy_.value)
    logger.debug(bstack11l1l11_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡦࡼࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠫᢹ"))
    try:
      if (bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩᢺ"), None) and bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬᢻ"), None)):
        scripts = {bstack11l1l11_opy_ (u"ࠫࡸࡩࡡ࡯ࠩᢼ"): bstack111llllll1_opy_.perform_scan}
        bstack11l111ll1l1_opy_ = json.loads(scripts[bstack11l1l11_opy_ (u"ࠧࡹࡣࡢࡰࠥᢽ")].replace(bstack11l1l11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࠤᢾ"), bstack11l1l11_opy_ (u"ࠢࠣᢿ")))
        bstack11l111ll1l1_opy_[bstack11l1l11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᣀ")][bstack11l1l11_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࠩᣁ")] = None
        scripts[bstack11l1l11_opy_ (u"ࠥࡷࡨࡧ࡮ࠣᣂ")] = bstack11l1l11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࠢᣃ") + json.dumps(bstack11l111ll1l1_opy_)
        bstack111llllll1_opy_.bstack11l11l1ll_opy_(scripts)
        bstack111llllll1_opy_.store()
        logger.debug(driver.execute_script(bstack111llllll1_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack111llllll1_opy_.perform_scan, {bstack11l1l11_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࠧᣄ"): name}))
      bstack111lll111l_opy_.end(EVENTS.bstack1l11llll_opy_.value, bstack1l1l1l1111_opy_ + bstack11l1l11_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᣅ"), bstack1l1l1l1111_opy_ + bstack11l1l11_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᣆ"), True, None)
    except Exception as error:
      bstack111lll111l_opy_.end(EVENTS.bstack1l11llll_opy_.value, bstack1l1l1l1111_opy_ + bstack11l1l11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᣇ"), bstack1l1l1l1111_opy_ + bstack11l1l11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᣈ"), False, str(error))
    bstack1l1l1l1111_opy_ = bstack111lll111l_opy_.bstack11l11lll1l1_opy_(EVENTS.bstack1l1l1llllll_opy_.value)
    bstack111lll111l_opy_.mark(bstack1l1l1l1111_opy_ + bstack11l1l11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᣉ"))
    try:
      if (bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫᣊ"), None) and bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᣋ"), None)):
        scripts = {bstack11l1l11_opy_ (u"࠭ࡳࡤࡣࡱࠫᣌ"): bstack111llllll1_opy_.perform_scan}
        bstack11l111ll1l1_opy_ = json.loads(scripts[bstack11l1l11_opy_ (u"ࠢࡴࡥࡤࡲࠧᣍ")].replace(bstack11l1l11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࠦᣎ"), bstack11l1l11_opy_ (u"ࠤࠥᣏ")))
        bstack11l111ll1l1_opy_[bstack11l1l11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᣐ")][bstack11l1l11_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࠫᣑ")] = None
        scripts[bstack11l1l11_opy_ (u"ࠧࡹࡣࡢࡰࠥᣒ")] = bstack11l1l11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࠤᣓ") + json.dumps(bstack11l111ll1l1_opy_)
        bstack111llllll1_opy_.bstack11l11l1ll_opy_(scripts)
        bstack111llllll1_opy_.store()
        logger.debug(driver.execute_script(bstack111llllll1_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack111llllll1_opy_.bstack11l11ll11l1_opy_, bstack1l1l1l1l1l1_opy_))
      bstack111lll111l_opy_.end(bstack1l1l1l1111_opy_, bstack1l1l1l1111_opy_ + bstack11l1l11_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᣔ"), bstack1l1l1l1111_opy_ + bstack11l1l11_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᣕ"),True, None)
    except Exception as error:
      bstack111lll111l_opy_.end(bstack1l1l1l1111_opy_, bstack1l1l1l1111_opy_ + bstack11l1l11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᣖ"), bstack1l1l1l1111_opy_ + bstack11l1l11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᣗ"),False, str(error))
    logger.info(bstack11l1l11_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠢᣘ"))
    try:
      bstack1l1ll1l111l_opy_ = {
        bstack11l1l11_opy_ (u"ࠧࡸࡥࡲࡷࡨࡷࡹࠨᣙ"): {
          bstack11l1l11_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࠢᣚ"): bstack11l1l11_opy_ (u"ࠢࡂ࠳࠴࡝ࡤ࡙ࡁࡗࡇࡢࡖࡊ࡙ࡕࡍࡖࡖࠦᣛ"),
        },
        bstack11l1l11_opy_ (u"ࠣࡴࡨࡷࡵࡵ࡮ࡴࡧࠥᣜ"): {
          bstack11l1l11_opy_ (u"ࠤࡥࡳࡩࡿࠢᣝ"): {
            bstack11l1l11_opy_ (u"ࠥࡱࡸ࡭ࠢᣞ"): bstack11l1l11_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠢᣟ"),
            bstack11l1l11_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨᣠ"): True
          }
        }
      }
      bstack11ll111ll_opy_.info(json.dumps(bstack1l1ll1l111l_opy_, separators=(bstack11l1l11_opy_ (u"࠭ࠬࠨᣡ"), bstack11l1l11_opy_ (u"ࠧ࠻ࠩᣢ"))))
    except Exception as bstack111l1l11ll_opy_:
      logger.debug(bstack11l1l11_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡱࡵࡧࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡤࡺࡪࠦࡲࡦࡵࡸࡰࡹࡹࠠࡥࡣࡷࡥ࠿ࠦࠢᣣ") + str(bstack111l1l11ll_opy_) + bstack11l1l11_opy_ (u"ࠤࠥᣤ"))
  except Exception as bstack1l1ll111l1l_opy_:
    logger.error(bstack11l1l11_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡨࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡣࡧࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧ࠽ࠤࠧᣥ") + str(path) + bstack11l1l11_opy_ (u"ࠦࠥࡋࡲࡳࡱࡵࠤ࠿ࠨᣦ") + str(bstack1l1ll111l1l_opy_))
def bstack11l11llll11_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack11l1l11_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦᣧ")) and str(caps.get(bstack11l1l11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧᣨ"))).lower() == bstack11l1l11_opy_ (u"ࠢࡢࡰࡧࡶࡴ࡯ࡤࠣᣩ"):
        bstack1l1ll1ll1l1_opy_ = caps.get(bstack11l1l11_opy_ (u"ࠣࡣࡳࡴ࡮ࡻ࡭࠻ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥᣪ")) or caps.get(bstack11l1l11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦᣫ"))
        if bstack1l1ll1ll1l1_opy_ and int(str(bstack1l1ll1ll1l1_opy_)) < bstack11l11ll1ll1_opy_:
            return False
    return True
def bstack11l1ll1ll1_opy_(config):
  if bstack11l1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᣬ") in config:
        return config[bstack11l1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᣭ")]
  for platform in config.get(bstack11l1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᣮ"), []):
      if bstack11l1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᣯ") in platform:
          return platform[bstack11l1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᣰ")]
  return None
def bstack1l1l11lll1_opy_(bstack111l11l111_opy_):
  try:
    browser_name = bstack111l11l111_opy_[bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧᣱ")]
    browser_version = bstack111l11l111_opy_[bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫᣲ")]
    chrome_options = bstack111l11l111_opy_[bstack11l1l11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡢࡳࡵࡺࡩࡰࡰࡶࠫᣳ")]
    try:
        bstack11l11l1ll1l_opy_ = int(browser_version.split(bstack11l1l11_opy_ (u"ࠫ࠳࠭ᣴ"))[0])
    except ValueError as e:
        logger.error(bstack11l1l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡴࡴࡶࡦࡴࡷ࡭ࡳ࡭ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠤᣵ") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack11l1l11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭᣶")):
        logger.warning(bstack11l1l11_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥ᣷"))
        return False
    if bstack11l11l1ll1l_opy_ < bstack11l11l1l1l1_opy_.bstack1l1ll1l1l1l_opy_:
        logger.warning(bstack1lll11l11ll_opy_ (u"ࠨࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡸࡥࡲࡷ࡬ࡶࡪࡹࠠࡄࡪࡵࡳࡲ࡫ࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡽࡆࡓࡓ࡙ࡔࡂࡐࡗࡗ࠳ࡓࡉࡏࡋࡐ࡙ࡒࡥࡎࡐࡐࡢࡆࡘ࡚ࡁࡄࡍࡢࡍࡓࡌࡒࡂࡡࡄ࠵࠶࡟࡟ࡔࡗࡓࡔࡔࡘࡔࡆࡆࡢࡇࡍࡘࡏࡎࡇࡢ࡚ࡊࡘࡓࡊࡑࡑࢁࠥࡵࡲࠡࡪ࡬࡫࡭࡫ࡲ࠯ࠩ᣸"))
        return False
    if chrome_options and any(bstack11l1l11_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸ࠭᣹") in value for value in chrome_options.values() if isinstance(value, str)):
        logger.warning(bstack11l1l11_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡴ࡯ࡵࠢࡵࡹࡳࠦ࡯࡯ࠢ࡯ࡩ࡬ࡧࡣࡺࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠣࡗࡼ࡯ࡴࡤࡪࠣࡸࡴࠦ࡮ࡦࡹࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧࠣࡳࡷࠦࡡࡷࡱ࡬ࡨࠥࡻࡳࡪࡰࡪࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲ࠧ᣺"))
        return False
    return True
  except Exception as e:
    logger.error(bstack11l1l11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡣࡩࡧࡦ࡯࡮ࡴࡧࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡷࡺࡶࡰࡰࡴࡷࠤ࡫ࡵࡲࠡ࡮ࡲࡧࡦࡲࠠࡄࡪࡵࡳࡲ࡫࠺ࠡࠤ᣻") + str(e))
    return False
def bstack1ll1ll1l11_opy_(bstack11llllll_opy_, config):
    try:
      bstack1l1ll1l1ll1_opy_ = bstack11l1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ᣼") in config and config[bstack11l1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭᣽")] == True
      bstack11l11l1l1ll_opy_ = bstack11l1l11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ᣾") in config and str(config[bstack11l1l11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ᣿")]).lower() != bstack11l1l11_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨᤀ")
      if not (bstack1l1ll1l1ll1_opy_ and (not bstack1lll1l1l_opy_(config) or bstack11l11l1l1ll_opy_)):
        return bstack11llllll_opy_
      bstack11l11ll1l1l_opy_ = bstack111llllll1_opy_.bstack11l111lll1l_opy_
      if bstack11l11ll1l1l_opy_ is None:
        logger.debug(bstack11l1l11_opy_ (u"ࠥࡋࡴࡵࡧ࡭ࡧࠣࡧ࡭ࡸ࡯࡮ࡧࠣࡳࡵࡺࡩࡰࡰࡶࠤࡦࡸࡥࠡࡐࡲࡲࡪࠨᤁ"))
        return bstack11llllll_opy_
      bstack11l11llllll_opy_ = int(str(bstack11l111ll1ll_opy_()).split(bstack11l1l11_opy_ (u"ࠫ࠳࠭ᤂ"))[0])
      logger.debug(bstack11l1l11_opy_ (u"࡙ࠧࡥ࡭ࡧࡱ࡭ࡺࡳࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡦࡨࡸࡪࡩࡴࡦࡦ࠽ࠤࠧᤃ") + str(bstack11l11llllll_opy_) + bstack11l1l11_opy_ (u"ࠨࠢᤄ"))
      if bstack11l11llllll_opy_ == 3 and isinstance(bstack11llllll_opy_, dict) and bstack11l1l11_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᤅ") in bstack11llllll_opy_ and bstack11l11ll1l1l_opy_ is not None:
        if bstack11l1l11_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᤆ") not in bstack11llllll_opy_[bstack11l1l11_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᤇ")]:
          bstack11llllll_opy_[bstack11l1l11_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᤈ")][bstack11l1l11_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᤉ")] = {}
        if bstack11l1l11_opy_ (u"ࠬࡧࡲࡨࡵࠪᤊ") in bstack11l11ll1l1l_opy_:
          if bstack11l1l11_opy_ (u"࠭ࡡࡳࡩࡶࠫᤋ") not in bstack11llllll_opy_[bstack11l1l11_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᤌ")][bstack11l1l11_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᤍ")]:
            bstack11llllll_opy_[bstack11l1l11_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᤎ")][bstack11l1l11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᤏ")][bstack11l1l11_opy_ (u"ࠫࡦࡸࡧࡴࠩᤐ")] = []
          for arg in bstack11l11ll1l1l_opy_[bstack11l1l11_opy_ (u"ࠬࡧࡲࡨࡵࠪᤑ")]:
            if arg not in bstack11llllll_opy_[bstack11l1l11_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᤒ")][bstack11l1l11_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᤓ")][bstack11l1l11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᤔ")]:
              bstack11llllll_opy_[bstack11l1l11_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᤕ")][bstack11l1l11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᤖ")][bstack11l1l11_opy_ (u"ࠫࡦࡸࡧࡴࠩᤗ")].append(arg)
        if bstack11l1l11_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᤘ") in bstack11l11ll1l1l_opy_:
          if bstack11l1l11_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᤙ") not in bstack11llllll_opy_[bstack11l1l11_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᤚ")][bstack11l1l11_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᤛ")]:
            bstack11llllll_opy_[bstack11l1l11_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᤜ")][bstack11l1l11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᤝ")][bstack11l1l11_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨᤞ")] = []
          for ext in bstack11l11ll1l1l_opy_[bstack11l1l11_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩ᤟")]:
            if ext not in bstack11llllll_opy_[bstack11l1l11_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᤠ")][bstack11l1l11_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᤡ")][bstack11l1l11_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᤢ")]:
              bstack11llllll_opy_[bstack11l1l11_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᤣ")][bstack11l1l11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᤤ")][bstack11l1l11_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨᤥ")].append(ext)
        if bstack11l1l11_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫᤦ") in bstack11l11ll1l1l_opy_:
          if bstack11l1l11_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬᤧ") not in bstack11llllll_opy_[bstack11l1l11_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᤨ")][bstack11l1l11_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᤩ")]:
            bstack11llllll_opy_[bstack11l1l11_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᤪ")][bstack11l1l11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᤫ")][bstack11l1l11_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪ᤬")] = {}
          bstack11l1l1111ll_opy_(bstack11llllll_opy_[bstack11l1l11_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬ᤭")][bstack11l1l11_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ᤮")][bstack11l1l11_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭᤯")],
                    bstack11l11ll1l1l_opy_[bstack11l1l11_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᤰ")])
        os.environ[bstack11l1l11_opy_ (u"ࠩࡌࡗࡤࡔࡏࡏࡡࡅࡗ࡙ࡇࡃࡌࡡࡌࡒࡋࡘࡁࡠࡃ࠴࠵࡞ࡥࡓࡆࡕࡖࡍࡔࡔࠧᤱ")] = bstack11l1l11_opy_ (u"ࠪࡸࡷࡻࡥࠨᤲ")
        return bstack11llllll_opy_
      else:
        chrome_options = None
        if isinstance(bstack11llllll_opy_, ChromeOptions):
          chrome_options = bstack11llllll_opy_
        elif isinstance(bstack11llllll_opy_, dict):
          for value in bstack11llllll_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack11llllll_opy_, dict):
            bstack11llllll_opy_[bstack11l1l11_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬᤳ")] = chrome_options
          else:
            bstack11llllll_opy_ = chrome_options
        if bstack11l11ll1l1l_opy_ is not None:
          if bstack11l1l11_opy_ (u"ࠬࡧࡲࡨࡵࠪᤴ") in bstack11l11ll1l1l_opy_:
                bstack11l11l1lll1_opy_ = chrome_options.arguments or []
                new_args = bstack11l11ll1l1l_opy_[bstack11l1l11_opy_ (u"࠭ࡡࡳࡩࡶࠫᤵ")]
                for arg in new_args:
                    if arg not in bstack11l11l1lll1_opy_:
                        chrome_options.add_argument(arg)
          if bstack11l1l11_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᤶ") in bstack11l11ll1l1l_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack11l1l11_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᤷ"), [])
                bstack11l11lll11l_opy_ = bstack11l11ll1l1l_opy_[bstack11l1l11_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᤸ")]
                for extension in bstack11l11lll11l_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack11l1l11_opy_ (u"ࠪࡴࡷ࡫ࡦࡴ᤹ࠩ") in bstack11l11ll1l1l_opy_:
                bstack11l11l1llll_opy_ = chrome_options.experimental_options.get(bstack11l1l11_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪ᤺"), {})
                bstack11l1l11111l_opy_ = bstack11l11ll1l1l_opy_[bstack11l1l11_opy_ (u"ࠬࡶࡲࡦࡨࡶ᤻ࠫ")]
                bstack11l1l1111ll_opy_(bstack11l11l1llll_opy_, bstack11l1l11111l_opy_)
                chrome_options.add_experimental_option(bstack11l1l11_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬ᤼"), bstack11l11l1llll_opy_)
        os.environ[bstack11l1l11_opy_ (u"ࠧࡊࡕࡢࡒࡔࡔ࡟ࡃࡕࡗࡅࡈࡑ࡟ࡊࡐࡉࡖࡆࡥࡁ࠲࠳࡜ࡣࡘࡋࡓࡔࡋࡒࡒࠬ᤽")] = bstack11l1l11_opy_ (u"ࠨࡶࡵࡹࡪ࠭᤾")
        return bstack11llllll_opy_
    except Exception as e:
      logger.error(bstack11l1l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡢࡦࡧ࡭ࡳ࡭ࠠ࡯ࡱࡱ࠱ࡇ࡙ࠠࡪࡰࡩࡶࡦࠦࡡ࠲࠳ࡼࠤࡨ࡮ࡲࡰ࡯ࡨࠤࡴࡶࡴࡪࡱࡱࡷ࠿ࠦࠢ᤿") + str(e))
      return bstack11llllll_opy_