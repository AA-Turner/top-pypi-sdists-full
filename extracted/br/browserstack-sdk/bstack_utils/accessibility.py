# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack11l1l1l1l11_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack11l1l1ll1l1_opy_ as bstack11l11llll1l_opy_, EVENTS
from bstack_utils.bstack1ll1111l1l_opy_ import bstack1ll1111l1l_opy_
from bstack_utils.helper import bstack1lll11lll1_opy_, bstack11111ll1ll_opy_, bstack1l111lll1l_opy_, bstack11l1l1ll111_opy_, \
  bstack11l1l1ll1ll_opy_, bstack11ll1lll1l_opy_, get_host_info, bstack11l1l1l1ll1_opy_, bstack111ll111_opy_, error_handler, bstack11l1l1l1lll_opy_, bstack11l1l111l11_opy_, bstack1l1ll1ll1_opy_
from browserstack_sdk._version import __version__
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack11lll1l11l_opy_ import bstack1lll11l1ll_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
from bstack_utils import logger_utils
logger = get_logger(__name__)
bstack1l111l111l_opy_ = logger_utils.bstack1l1l11111l_opy_(__name__)
bstack11lll1l11l_opy_ = bstack1lll11l1ll_opy_()
@error_handler(class_method=False)
def _11l1ll11l11_opy_(driver, bstack1lllll11111_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack11lllll_opy_ (u"ࠬࡵࡳࡠࡰࡤࡱࡪ࠭ᝊ"): caps.get(bstack11lllll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬᝋ"), None),
        bstack11lllll_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫᝌ"): bstack1lllll11111_opy_.get(bstack11lllll_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫᝍ"), None),
        bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡲࡦࡳࡥࠨᝎ"): caps.get(bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᝏ"), None),
        bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᝐ"): caps.get(bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᝑ"), None)
    }
  except Exception as error:
    logger.debug(bstack11lllll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡥࡵࡥ࡫࡭ࡳ࡭ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡧࡩࡹࡧࡩ࡭ࡵࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸࠠ࠻ࠢࠪᝒ") + str(error))
  return response
def on():
    if os.environ.get(bstack11lllll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᝓ"), None) is None or os.environ[bstack11lllll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭᝔")] == bstack11lllll_opy_ (u"ࠤࡱࡹࡱࡲࠢ᝕"):
        return False
    return True
def bstack1lll1lll1l_opy_(config):
  return config.get(bstack11lllll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ᝖"), False) or any([p.get(bstack11lllll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ᝗"), False) == True for p in config.get(bstack11lllll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ᝘"), [])])
def bstack1ll1ll11l1_opy_(config, bstack11111l111_opy_):
  try:
    bstack11l1l11l11l_opy_ = config.get(bstack11lllll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭᝙"), False)
    if int(bstack11111l111_opy_) < len(config.get(bstack11lllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ᝚"), [])) and config[bstack11lllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ᝛")][bstack11111l111_opy_]:
      bstack11l1l11l111_opy_ = config[bstack11lllll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ᝜")][bstack11111l111_opy_].get(bstack11lllll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ᝝"), None)
    else:
      bstack11l1l11l111_opy_ = config.get(bstack11lllll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ᝞"), None)
    if bstack11l1l11l111_opy_ != None:
      bstack11l1l11l11l_opy_ = bstack11l1l11l111_opy_
    bstack11l1l1ll11l_opy_ = os.getenv(bstack11lllll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ᝟")) is not None and len(os.getenv(bstack11lllll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᝠ"))) > 0 and os.getenv(bstack11lllll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᝡ")) != bstack11lllll_opy_ (u"ࠨࡰࡸࡰࡱ࠭ᝢ")
    return bstack11l1l11l11l_opy_ and bstack11l1l1ll11l_opy_
  except Exception as error:
    logger.debug(bstack11lllll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡸࡨࡶ࡮࡬ࡹࡪࡰࡪࠤࡹ࡮ࡥࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࠦ࠺ࠡࠩᝣ") + str(error))
  return False
def bstack1l11lll111_opy_(test_tags):
  bstack1l1ll111l11_opy_ = os.getenv(bstack11lllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᝤ"))
  if bstack1l1ll111l11_opy_ is None:
    return True
  bstack1l1ll111l11_opy_ = json.loads(bstack1l1ll111l11_opy_)
  try:
    include_tags = bstack1l1ll111l11_opy_[bstack11lllll_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᝥ")] if bstack11lllll_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᝦ") in bstack1l1ll111l11_opy_ and isinstance(bstack1l1ll111l11_opy_[bstack11lllll_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᝧ")], list) else []
    exclude_tags = bstack1l1ll111l11_opy_[bstack11lllll_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᝨ")] if bstack11lllll_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᝩ") in bstack1l1ll111l11_opy_ and isinstance(bstack1l1ll111l11_opy_[bstack11lllll_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᝪ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack11lllll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡸࡤࡰ࡮ࡪࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡢࡰࡱ࡭ࡳ࡭࠮ࠡࡇࡵࡶࡴࡸࠠ࠻ࠢࠥᝫ") + str(error))
  return False
def bstack11l1ll1111l_opy_(config, bstack11l1l111ll1_opy_, bstack11l1l1111ll_opy_, bstack11l1l1l11ll_opy_):
  bstack11l11llllll_opy_ = bstack11l1l1ll111_opy_(config)
  bstack11l1l1111l1_opy_ = bstack11l1l1ll1ll_opy_(config)
  if bstack11l11llllll_opy_ is None or bstack11l1l1111l1_opy_ is None:
    logger.error(bstack11lllll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡲࡶࡰࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࡒ࡯ࡳࡴ࡫ࡱ࡫ࠥࡧࡵࡵࡪࡨࡲࡹ࡯ࡣࡢࡶ࡬ࡳࡳࠦࡴࡰ࡭ࡨࡲࠬᝬ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack11lllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭᝭"), bstack11lllll_opy_ (u"࠭ࡻࡾࠩᝮ")))
    data = {
        bstack11lllll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᝯ"): config[bstack11lllll_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᝰ")],
        bstack11lllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ᝱"): config.get(bstack11lllll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ᝲ"), os.path.basename(os.getcwd())),
        bstack11lllll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡗ࡭ࡲ࡫ࠧᝳ"): bstack1lll11lll1_opy_(),
        bstack11lllll_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ᝴"): config.get(bstack11lllll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡉ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩ᝵"), bstack11lllll_opy_ (u"ࠧࠨ᝶")),
        bstack11lllll_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ᝷"): {
            bstack11lllll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡓࡧ࡭ࡦࠩ᝸"): bstack11l1l111ll1_opy_,
            bstack11lllll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭᝹"): bstack11l1l1111ll_opy_,
            bstack11lllll_opy_ (u"ࠫࡸࡪ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᝺"): __version__,
            bstack11lllll_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠧ᝻"): bstack11lllll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭᝼"),
            bstack11lllll_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ᝽"): bstack11lllll_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࠪ᝾"),
            bstack11lllll_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩ᝿"): bstack11l1l1l11ll_opy_
        },
        bstack11lllll_opy_ (u"ࠪࡷࡪࡺࡴࡪࡰࡪࡷࠬក"): settings,
        bstack11lllll_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࡈࡵ࡮ࡵࡴࡲࡰࠬខ"): bstack11l1l1l1ll1_opy_(),
        bstack11lllll_opy_ (u"ࠬࡩࡩࡊࡰࡩࡳࠬគ"): bstack11ll1lll1l_opy_(),
        bstack11lllll_opy_ (u"࠭ࡨࡰࡵࡷࡍࡳ࡬࡯ࠨឃ"): get_host_info(),
        bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩង"): bstack1l111lll1l_opy_(config)
    }
    headers = {
        bstack11lllll_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧច"): bstack11lllll_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬឆ"),
    }
    config = {
        bstack11lllll_opy_ (u"ࠪࡥࡺࡺࡨࠨជ"): (bstack11l11llllll_opy_, bstack11l1l1111l1_opy_),
        bstack11lllll_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬឈ"): headers
    }
    response = bstack111ll111_opy_(bstack11lllll_opy_ (u"ࠬࡖࡏࡔࡖࠪញ"), bstack11l11llll1l_opy_ + bstack11lllll_opy_ (u"࠭࠯ࡷ࠴࠲ࡸࡪࡹࡴࡠࡴࡸࡲࡸ࠭ដ"), data, config)
    bstack11l1l1lllll_opy_ = response.json()
    if bstack11l1l1lllll_opy_[bstack11lllll_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨឋ")]:
      parsed = json.loads(os.getenv(bstack11lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩឌ"), bstack11lllll_opy_ (u"ࠩࡾࢁࠬឍ")))
      parsed[bstack11lllll_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫណ")] = bstack11l1l1lllll_opy_[bstack11lllll_opy_ (u"ࠫࡩࡧࡴࡢࠩត")][bstack11lllll_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ថ")]
      os.environ[bstack11lllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧទ")] = json.dumps(parsed)
      bstack1ll1111l1l_opy_.bstack1l11l11ll1_opy_(bstack11l1l1lllll_opy_[bstack11lllll_opy_ (u"ࠧࡥࡣࡷࡥࠬធ")][bstack11lllll_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩន")])
      bstack1ll1111l1l_opy_.bstack11l1ll111l1_opy_(bstack11l1l1lllll_opy_[bstack11lllll_opy_ (u"ࠩࡧࡥࡹࡧࠧប")][bstack11lllll_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬផ")])
      bstack1ll1111l1l_opy_.store()
      return bstack11l1l1lllll_opy_[bstack11lllll_opy_ (u"ࠫࡩࡧࡴࡢࠩព")][bstack11lllll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࡙ࡵ࡫ࡦࡰࠪភ")], bstack11l1l1lllll_opy_[bstack11lllll_opy_ (u"࠭ࡤࡢࡶࡤࠫម")][bstack11lllll_opy_ (u"ࠧࡪࡦࠪយ")]
    else:
      logger.error(bstack11lllll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡶࡺࡴ࡮ࡪࡰࡪࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࠩរ") + bstack11l1l1lllll_opy_[bstack11lllll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪល")])
      if bstack11l1l1lllll_opy_[bstack11lllll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫវ")] == bstack11lllll_opy_ (u"ࠫࡎࡴࡶࡢ࡮࡬ࡨࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥࡶࡡࡴࡵࡨࡨ࠳࠭ឝ"):
        for bstack11l1l11l1l1_opy_ in bstack11l1l1lllll_opy_[bstack11lllll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡷࠬឞ")]:
          logger.error(bstack11l1l11l1l1_opy_[bstack11lllll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧស")])
      return None, None
  except Exception as error:
    logger.error(bstack11lllll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡵࡹࡳࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࠣហ") +  str(error))
    return None, None
def bstack11l1l1llll1_opy_():
  if os.getenv(bstack11lllll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ឡ")) is None:
    return {
        bstack11lllll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩអ"): bstack11lllll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩឣ"),
        bstack11lllll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬឤ"): bstack11lllll_opy_ (u"ࠬࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡨࡢࡦࠣࡪࡦ࡯࡬ࡦࡦ࠱ࠫឥ")
    }
  data = {bstack11lllll_opy_ (u"࠭ࡥ࡯ࡦࡗ࡭ࡲ࡫ࠧឦ"): bstack1lll11lll1_opy_()}
  headers = {
      bstack11lllll_opy_ (u"ࠧࡂࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧឧ"): bstack11lllll_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࠩឨ") + os.getenv(bstack11lllll_opy_ (u"ࠤࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠢឩ")),
      bstack11lllll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩឪ"): bstack11lllll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧឫ")
  }
  response = bstack111ll111_opy_(bstack11lllll_opy_ (u"ࠬࡖࡕࡕࠩឬ"), bstack11l11llll1l_opy_ + bstack11lllll_opy_ (u"࠭࠯ࡵࡧࡶࡸࡤࡸࡵ࡯ࡵ࠲ࡷࡹࡵࡰࠨឭ"), data, { bstack11lllll_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨឮ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack11lllll_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤ࡙࡫ࡳࡵࠢࡕࡹࡳࠦ࡭ࡢࡴ࡮ࡩࡩࠦࡡࡴࠢࡦࡳࡲࡶ࡬ࡦࡶࡨࡨࠥࡧࡴࠡࠤឯ") + bstack11111ll1ll_opy_().isoformat() + bstack11lllll_opy_ (u"ࠩ࡝ࠫឰ"))
      return {bstack11lllll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪឱ"): bstack11lllll_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬឲ"), bstack11lllll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ឳ"): bstack11lllll_opy_ (u"࠭ࠧ឴")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack11lllll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡧࡴࡳࡰ࡭ࡧࡷ࡭ࡴࡴࠠࡰࡨࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡔࡦࡵࡷࠤࡗࡻ࡮࠻ࠢࠥ឵") + str(error))
    return {
        bstack11lllll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨា"): bstack11lllll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨិ"),
        bstack11lllll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫី"): str(error)
    }
def bstack11l1l111lll_opy_(bstack11l1l11lll1_opy_):
    return re.match(bstack11lllll_opy_ (u"ࡶࠬࡤ࡜ࡥ࠭ࠫࡠ࠳ࡢࡤࠬࠫࡂࠨࠬឹ"), bstack11l1l11lll1_opy_.strip()) is not None
def bstack1l1l1l1l1l_opy_(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack11l1ll11l1l_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11l1ll11l1l_opy_ = desired_capabilities
        else:
          bstack11l1ll11l1l_opy_ = {}
        bstack1l1l1lll111_opy_ = (bstack11l1ll11l1l_opy_.get(bstack11lllll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫឺ"), bstack11lllll_opy_ (u"࠭ࠧុ")).lower() or caps.get(bstack11lllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ូ"), bstack11lllll_opy_ (u"ࠨࠩួ")).lower())
        if bstack1l1l1lll111_opy_ == bstack11lllll_opy_ (u"ࠩ࡬ࡳࡸ࠭ើ"):
            return True
        if bstack1l1l1lll111_opy_ == bstack11lllll_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࠫឿ"):
            bstack1l1ll1111l1_opy_ = str(float(caps.get(bstack11lllll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ៀ")) or bstack11l1ll11l1l_opy_.get(bstack11lllll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭េ"), {}).get(bstack11lllll_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩែ"),bstack11lllll_opy_ (u"ࠧࠨៃ"))))
            if bstack1l1l1lll111_opy_ == bstack11lllll_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࠩោ") and int(bstack1l1ll1111l1_opy_.split(bstack11lllll_opy_ (u"ࠩ࠱ࠫៅ"))[0]) < float(bstack11l1l11111l_opy_):
                logger.warning(str(bstack11l1l1lll1l_opy_))
                return False
            return True
        bstack1l1l1l1l1l1_opy_ = caps.get(bstack11lllll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫំ"), {}).get(bstack11lllll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨះ"), caps.get(bstack11lllll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬៈ"), bstack11lllll_opy_ (u"࠭ࠧ៉")))
        if bstack1l1l1l1l1l1_opy_:
            logger.warning(bstack11lllll_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡅࡧࡶ࡯ࡹࡵࡰࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦ៊"))
            return False
        browser = caps.get(bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭់"), bstack11lllll_opy_ (u"ࠩࠪ៌")).lower() or bstack11l1ll11l1l_opy_.get(bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ៍"), bstack11lllll_opy_ (u"ࠫࠬ៎")).lower()
        if browser != bstack11lllll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬ៏"):
            logger.warning(bstack11lllll_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤ័"))
            return False
        browser_version = caps.get(bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ៑")) or caps.get(bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰ្ࠪ")) or bstack11l1ll11l1l_opy_.get(bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ៓")) or bstack11l1ll11l1l_opy_.get(bstack11lllll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ។"), {}).get(bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ៕")) or bstack11l1ll11l1l_opy_.get(bstack11lllll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭៖"), {}).get(bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨៗ"))
        bstack1l1ll1llll1_opy_ = bstack11l1l1l1l11_opy_.bstack1l1l1ll1111_opy_
        bstack11l1l1lll11_opy_ = False
        if config is not None:
          bstack11l1l1lll11_opy_ = bstack11lllll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ៘") in config and str(config[bstack11lllll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ៙")]).lower() != bstack11lllll_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ៚")
        if os.environ.get(bstack11lllll_opy_ (u"ࠪࡍࡘࡥࡎࡐࡐࡢࡆࡘ࡚ࡁࡄࡍࡢࡍࡓࡌࡒࡂࡡࡄ࠵࠶࡟࡟ࡔࡇࡖࡗࡎࡕࡎࠨ៛"), bstack11lllll_opy_ (u"ࠫࠬៜ")).lower() == bstack11lllll_opy_ (u"ࠬࡺࡲࡶࡧࠪ៝") or bstack11l1l1lll11_opy_:
          bstack1l1ll1llll1_opy_ = bstack11l1l1l1l11_opy_.bstack1l1ll11l11l_opy_
        if browser_version and browser_version != bstack11lllll_opy_ (u"࠭࡬ࡢࡶࡨࡷࡹ࠭៞") and int(browser_version.split(bstack11lllll_opy_ (u"ࠧ࠯ࠩ៟"))[0]) <= bstack1l1ll1llll1_opy_:
          logger.warning(bstack1llll11111l_opy_ (u"ࠨࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠣ࡫ࡷ࡫ࡡࡵࡧࡵࠤࡹ࡮ࡡ࡯ࠢࡾࡱ࡮ࡴ࡟ࡢ࠳࠴ࡽࡤࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࡠࡥ࡫ࡶࡴࡳࡥࡠࡸࡨࡶࡸ࡯࡯࡯ࡿ࠱ࠫ០"))
          return False
        if not options:
          bstack1l1l1ll1lll_opy_ = caps.get(bstack11lllll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ១")) or bstack11l1ll11l1l_opy_.get(bstack11lllll_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ២"), {})
          if bstack11lllll_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳࠨ៣") in bstack1l1l1ll1lll_opy_.get(bstack11lllll_opy_ (u"ࠬࡧࡲࡨࡵࠪ៤"), []):
              logger.warning(bstack11lllll_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡰࡲࡸࠥࡸࡵ࡯ࠢࡲࡲࠥࡲࡥࡨࡣࡦࡽࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠦࡓࡸ࡫ࡷࡧ࡭ࠦࡴࡰࠢࡱࡩࡼࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪࠦ࡯ࡳࠢࡤࡺࡴ࡯ࡤࠡࡷࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠣ៥"))
              return False
        return True
    except Exception as error:
        logger.debug(bstack11lllll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡶࡢ࡮࡬ࡨࡦࡺࡥࠡࡣ࠴࠵ࡾࠦࡳࡶࡲࡳࡳࡷࡺࠠ࠻ࠤ៦") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1ll1111111l_opy_ = config.get(bstack11lllll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ៧"), {})
    bstack1ll1111111l_opy_[bstack11lllll_opy_ (u"ࠩࡤࡹࡹ࡮ࡔࡰ࡭ࡨࡲࠬ៨")] = os.getenv(bstack11lllll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ៩"))
    bstack11l1l11ll1l_opy_ = json.loads(os.getenv(bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ៪"), bstack11lllll_opy_ (u"ࠬࢁࡽࠨ៫"))).get(bstack11lllll_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ៬"))
    if not config[bstack11lllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩ៭")].get(bstack11lllll_opy_ (u"ࠣࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠢ៮")):
      if bstack11lllll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ៯") in caps:
        caps[bstack11lllll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ៰")][bstack11lllll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ៱")] = bstack1ll1111111l_opy_
        caps[bstack11lllll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭៲")][bstack11lllll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭៳")][bstack11lllll_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ៴")] = bstack11l1l11ll1l_opy_
      else:
        caps[bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ៵")] = bstack1ll1111111l_opy_
        caps[bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ៶")][bstack11lllll_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ៷")] = bstack11l1l11ll1l_opy_
  except Exception as error:
    logger.debug(bstack11lllll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵ࠱ࠤࡊࡸࡲࡰࡴ࠽ࠤࠧ៸") +  str(error))
def bstack1ll11l1l11_opy_(driver, bstack11l1ll11ll1_opy_):
  try:
    setattr(driver, bstack11lllll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬ៹"), True)
    session = driver.session_id
    if session:
      bstack11l1l11ll11_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11l1l11ll11_opy_ = False
      bstack11l1l11ll11_opy_ = url.scheme in [bstack11lllll_opy_ (u"ࠨࡨࡵࡶࡳࠦ៺"), bstack11lllll_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨ៻")]
      if bstack11l1l11ll11_opy_:
        if bstack11l1ll11ll1_opy_:
          logger.info(bstack11lllll_opy_ (u"ࠣࡕࡨࡸࡺࡶࠠࡧࡱࡵࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡮ࡡࡴࠢࡶࡸࡦࡸࡴࡦࡦ࠱ࠤࡆࡻࡴࡰ࡯ࡤࡸࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡦࡪ࡭ࡩ࡯ࠢࡰࡳࡲ࡫࡮ࡵࡣࡵ࡭ࡱࡿ࠮ࠣ៼"))
      return bstack11l1ll11ll1_opy_
  except Exception as e:
    logger.error(bstack11lllll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡥࡷࡺࡩ࡯ࡩࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧ࠽ࠤࠧ៽") + str(e))
    return False
def bstack1111ll1ll_opy_(driver, name, path):
  try:
    bstack1l1ll1l11l1_opy_ = {
        bstack11lllll_opy_ (u"ࠪࡸ࡭࡚ࡥࡴࡶࡕࡹࡳ࡛ࡵࡪࡦࠪ៾"): threading.current_thread().current_test_uuid,
        bstack11lllll_opy_ (u"ࠫࡹ࡮ࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ៿"): os.environ.get(bstack11lllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ᠀"), bstack11lllll_opy_ (u"࠭ࠧ᠁")),
        bstack11lllll_opy_ (u"ࠧࡵࡪࡍࡻࡹ࡚࡯࡬ࡧࡱࠫ᠂"): os.environ.get(bstack11lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ᠃"), bstack11lllll_opy_ (u"ࠩࠪ᠄"))
    }
    bstack1ll11111l_opy_ = bstack11lll1l11l_opy_.bstack1llll1l1ll_opy_(EVENTS.bstack1ll1l111l1_opy_.value)
    logger.debug(bstack11lllll_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡡࡷ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸ࠭᠅"))
    try:
      if (bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ᠆"), None) and bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ᠇"), None)):
        scripts = {bstack11lllll_opy_ (u"࠭ࡳࡤࡣࡱࠫ᠈"): bstack1ll1111l1l_opy_.perform_scan}
        bstack11l1l11llll_opy_ = json.loads(scripts[bstack11lllll_opy_ (u"ࠢࡴࡥࡤࡲࠧ᠉")].replace(bstack11lllll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࠦ᠊"), bstack11lllll_opy_ (u"ࠤࠥ᠋")))
        bstack11l1l11llll_opy_[bstack11lllll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭᠌")][bstack11lllll_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࠫ᠍")] = None
        scripts[bstack11lllll_opy_ (u"ࠧࡹࡣࡢࡰࠥ᠎")] = bstack11lllll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࠤ᠏") + json.dumps(bstack11l1l11llll_opy_)
        bstack1ll1111l1l_opy_.bstack1l11l11ll1_opy_(scripts)
        bstack1ll1111l1l_opy_.store()
        logger.debug(driver.execute_script(bstack1ll1111l1l_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1ll1111l1l_opy_.perform_scan, {bstack11lllll_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢ᠐"): name}))
      bstack11lll1l11l_opy_.end(EVENTS.bstack1ll1l111l1_opy_.value, bstack1ll11111l_opy_ + bstack11lllll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ᠑"), bstack1ll11111l_opy_ + bstack11lllll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ᠒"), True, None)
    except Exception as error:
      bstack11lll1l11l_opy_.end(EVENTS.bstack1ll1l111l1_opy_.value, bstack1ll11111l_opy_ + bstack11lllll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ᠓"), bstack1ll11111l_opy_ + bstack11lllll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ᠔"), False, str(error))
    bstack1ll11111l_opy_ = bstack11lll1l11l_opy_.bstack11l1l111l1l_opy_(EVENTS.bstack1l1l1l1l11l_opy_.value)
    bstack11lll1l11l_opy_.mark(bstack1ll11111l_opy_ + bstack11lllll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ᠕"))
    try:
      if (bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭᠖"), None) and bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ᠗"), None)):
        scripts = {bstack11lllll_opy_ (u"ࠨࡵࡦࡥࡳ࠭᠘"): bstack1ll1111l1l_opy_.perform_scan}
        bstack11l1l11llll_opy_ = json.loads(scripts[bstack11lllll_opy_ (u"ࠤࡶࡧࡦࡴࠢ᠙")].replace(bstack11lllll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨ᠚"), bstack11lllll_opy_ (u"ࠦࠧ᠛")))
        bstack11l1l11llll_opy_[bstack11lllll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ᠜")][bstack11lllll_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩ࠭᠝")] = None
        scripts[bstack11lllll_opy_ (u"ࠢࡴࡥࡤࡲࠧ᠞")] = bstack11lllll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࠦ᠟") + json.dumps(bstack11l1l11llll_opy_)
        bstack1ll1111l1l_opy_.bstack1l11l11ll1_opy_(scripts)
        bstack1ll1111l1l_opy_.store()
        logger.debug(driver.execute_script(bstack1ll1111l1l_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1ll1111l1l_opy_.bstack11l1l1l11l1_opy_, bstack1l1ll1l11l1_opy_))
      bstack11lll1l11l_opy_.end(bstack1ll11111l_opy_, bstack1ll11111l_opy_ + bstack11lllll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᠠ"), bstack1ll11111l_opy_ + bstack11lllll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᠡ"),True, None)
    except Exception as error:
      bstack11lll1l11l_opy_.end(bstack1ll11111l_opy_, bstack1ll11111l_opy_ + bstack11lllll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᠢ"), bstack1ll11111l_opy_ + bstack11lllll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᠣ"),False, str(error))
    logger.info(bstack11lllll_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠤᠤ"))
    try:
      bstack1l1ll1ll11l_opy_ = {
        bstack11lllll_opy_ (u"ࠢࡳࡧࡴࡹࡪࡹࡴࠣᠥ"): {
          bstack11lllll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤᠦ"): bstack11lllll_opy_ (u"ࠤࡄ࠵࠶࡟࡟ࡔࡃ࡙ࡉࡤࡘࡅࡔࡗࡏࡘࡘࠨᠧ"),
        },
        bstack11lllll_opy_ (u"ࠥࡶࡪࡹࡰࡰࡰࡶࡩࠧᠨ"): {
          bstack11lllll_opy_ (u"ࠦࡧࡵࡤࡺࠤᠩ"): {
            bstack11lllll_opy_ (u"ࠧࡳࡳࡨࠤᠪ"): bstack11lllll_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠤᠫ"),
            bstack11lllll_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳࠣᠬ"): True
          }
        }
      }
      bstack1l111l111l_opy_.info(json.dumps(bstack1l1ll1ll11l_opy_, separators=(bstack11lllll_opy_ (u"ࠨ࠮ࠪᠭ"), bstack11lllll_opy_ (u"ࠩ࠽ࠫᠮ"))))
    except Exception as bstack111l1l1l_opy_:
      logger.debug(bstack11lllll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡬ࡰࡩࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡦࡼࡥࠡࡴࡨࡷࡺࡲࡴࡴࠢࡧࡥࡹࡧ࠺ࠡࠤᠯ") + str(bstack111l1l1l_opy_) + bstack11lllll_opy_ (u"ࠦࠧᠰ"))
  except Exception as bstack1l1ll1l1ll1_opy_:
    logger.error(bstack11lllll_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡣࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡥࡩࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡨࡲࡶࠥࡺࡨࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩ࠿ࠦࠢᠱ") + str(path) + bstack11lllll_opy_ (u"ࠨࠠࡆࡴࡵࡳࡷࠦ࠺ࠣᠲ") + str(bstack1l1ll1l1ll1_opy_))
def bstack11l1ll111ll_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack11lllll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨᠳ")) and str(caps.get(bstack11lllll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢᠴ"))).lower() == bstack11lllll_opy_ (u"ࠤࡤࡲࡩࡸ࡯ࡪࡦࠥᠵ"):
        bstack1l1ll1111l1_opy_ = caps.get(bstack11lllll_opy_ (u"ࠥࡥࡵࡶࡩࡶ࡯࠽ࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧᠶ")) or caps.get(bstack11lllll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨᠷ"))
        if bstack1l1ll1111l1_opy_ and int(str(bstack1l1ll1111l1_opy_)) < bstack11l1l11111l_opy_:
            return False
    return True
def bstack1lll1l11ll_opy_(config):
  if bstack11lllll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᠸ") in config:
        return config[bstack11lllll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᠹ")]
  for platform in config.get(bstack11lllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᠺ"), []):
      if bstack11lllll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᠻ") in platform:
          return platform[bstack11lllll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᠼ")]
  return None
def bstack1l111l11ll_opy_(bstack1ll11ll1ll_opy_):
  try:
    browser_name = bstack1ll11ll1ll_opy_[bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩᠽ")]
    browser_version = bstack1ll11ll1ll_opy_[bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᠾ")]
    chrome_options = bstack1ll11ll1ll_opy_[bstack11lllll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡤࡵࡰࡵ࡫ࡲࡲࡸ࠭ᠿ")]
    try:
        bstack11l11lllll1_opy_ = int(browser_version.split(bstack11lllll_opy_ (u"࠭࠮ࠨᡀ"))[0])
    except ValueError as e:
        logger.error(bstack11lllll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡩ࡯࡯ࡸࡨࡶࡹ࡯࡮ࡨࠢࡥࡶࡴࡽࡳࡦࡴࠣࡺࡪࡸࡳࡪࡱࡱࠦᡁ") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack11lllll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨᡂ")):
        logger.warning(bstack11lllll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶ࠲ࠧᡃ"))
        return False
    if bstack11l11lllll1_opy_ < bstack11l1l1l1l11_opy_.bstack1l1ll11l11l_opy_:
        logger.warning(bstack1llll11111l_opy_ (u"ࠪࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡳࡧࡴࡹ࡮ࡸࡥࡴࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡹࡩࡷࡹࡩࡰࡰࠣࡿࡈࡕࡎࡔࡖࡄࡒ࡙࡙࠮ࡎࡋࡑࡍࡒ࡛ࡍࡠࡐࡒࡒࡤࡈࡓࡕࡃࡆࡏࡤࡏࡎࡇࡔࡄࡣࡆ࠷࠱࡚ࡡࡖ࡙ࡕࡖࡏࡓࡖࡈࡈࡤࡉࡈࡓࡑࡐࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࢃࠠࡰࡴࠣ࡬࡮࡭ࡨࡦࡴ࠱ࠫᡄ"))
        return False
    if chrome_options and any(bstack11lllll_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳࠨᡅ") in value for value in chrome_options.values() if isinstance(value, str)):
        logger.warning(bstack11lllll_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠ࡯ࡱࡷࠤࡷࡻ࡮ࠡࡱࡱࠤࡱ࡫ࡧࡢࡥࡼࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲࡙ࠥࡷࡪࡶࡦ࡬ࠥࡺ࡯ࠡࡰࡨࡻࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩࠥࡵࡲࠡࡣࡹࡳ࡮ࡪࠠࡶࡵ࡬ࡲ࡬ࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠢᡆ"))
        return False
    return True
  except Exception as e:
    logger.error(bstack11lllll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡥ࡫ࡩࡨࡱࡩ࡯ࡩࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡹࡵࡱࡲࡲࡶࡹࠦࡦࡰࡴࠣࡰࡴࡩࡡ࡭ࠢࡆ࡬ࡷࡵ࡭ࡦ࠼ࠣࠦᡇ") + str(e))
    return False
def bstack11111l1l_opy_(bstack111ll1ll1_opy_, config):
    try:
      bstack1l1ll11l1l1_opy_ = bstack11lllll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᡈ") in config and config[bstack11lllll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᡉ")] == True
      bstack11l1l1lll11_opy_ = bstack11lllll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᡊ") in config and str(config[bstack11lllll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧᡋ")]).lower() != bstack11lllll_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪᡌ")
      if not (bstack1l1ll11l1l1_opy_ and (not bstack1l111lll1l_opy_(config) or bstack11l1l1lll11_opy_)):
        return bstack111ll1ll1_opy_
      bstack11l1ll11lll_opy_ = bstack1ll1111l1l_opy_.bstack11l1l1l111l_opy_
      if bstack11l1ll11lll_opy_ is None:
        logger.debug(bstack11lllll_opy_ (u"ࠧࡍ࡯ࡰࡩ࡯ࡩࠥࡩࡨࡳࡱࡰࡩࠥࡵࡰࡵ࡫ࡲࡲࡸࠦࡡࡳࡧࠣࡒࡴࡴࡥࠣᡍ"))
        return bstack111ll1ll1_opy_
      bstack11l1l1l1111_opy_ = int(str(bstack11l1l111l11_opy_()).split(bstack11lllll_opy_ (u"࠭࠮ࠨᡎ"))[0])
      logger.debug(bstack11lllll_opy_ (u"ࠢࡔࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡹࡩࡷࡹࡩࡰࡰࠣࡨࡪࡺࡥࡤࡶࡨࡨ࠿ࠦࠢᡏ") + str(bstack11l1l1l1111_opy_) + bstack11lllll_opy_ (u"ࠣࠤᡐ"))
      if bstack11l1l1l1111_opy_ == 3 and isinstance(bstack111ll1ll1_opy_, dict) and bstack11lllll_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᡑ") in bstack111ll1ll1_opy_ and bstack11l1ll11lll_opy_ is not None:
        if bstack11lllll_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᡒ") not in bstack111ll1ll1_opy_[bstack11lllll_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᡓ")]:
          bstack111ll1ll1_opy_[bstack11lllll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᡔ")][bstack11lllll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᡕ")] = {}
        if bstack11lllll_opy_ (u"ࠧࡢࡴࡪࡷࠬᡖ") in bstack11l1ll11lll_opy_:
          if bstack11lllll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᡗ") not in bstack111ll1ll1_opy_[bstack11lllll_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᡘ")][bstack11lllll_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᡙ")]:
            bstack111ll1ll1_opy_[bstack11lllll_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᡚ")][bstack11lllll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᡛ")][bstack11lllll_opy_ (u"࠭ࡡࡳࡩࡶࠫᡜ")] = []
          for arg in bstack11l1ll11lll_opy_[bstack11lllll_opy_ (u"ࠧࡢࡴࡪࡷࠬᡝ")]:
            if arg not in bstack111ll1ll1_opy_[bstack11lllll_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᡞ")][bstack11lllll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᡟ")][bstack11lllll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᡠ")]:
              bstack111ll1ll1_opy_[bstack11lllll_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᡡ")][bstack11lllll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᡢ")][bstack11lllll_opy_ (u"࠭ࡡࡳࡩࡶࠫᡣ")].append(arg)
        if bstack11lllll_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᡤ") in bstack11l1ll11lll_opy_:
          if bstack11lllll_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᡥ") not in bstack111ll1ll1_opy_[bstack11lllll_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᡦ")][bstack11lllll_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᡧ")]:
            bstack111ll1ll1_opy_[bstack11lllll_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᡨ")][bstack11lllll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᡩ")][bstack11lllll_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᡪ")] = []
          for ext in bstack11l1ll11lll_opy_[bstack11lllll_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᡫ")]:
            if ext not in bstack111ll1ll1_opy_[bstack11lllll_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᡬ")][bstack11lllll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᡭ")][bstack11lllll_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᡮ")]:
              bstack111ll1ll1_opy_[bstack11lllll_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᡯ")][bstack11lllll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᡰ")][bstack11lllll_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᡱ")].append(ext)
        if bstack11lllll_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ᡲ") in bstack11l1ll11lll_opy_:
          if bstack11lllll_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᡳ") not in bstack111ll1ll1_opy_[bstack11lllll_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᡴ")][bstack11lllll_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᡵ")]:
            bstack111ll1ll1_opy_[bstack11lllll_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᡶ")][bstack11lllll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᡷ")][bstack11lllll_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬᡸ")] = {}
          bstack11l1l1l1lll_opy_(bstack111ll1ll1_opy_[bstack11lllll_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ᡹")][bstack11lllll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᡺")][bstack11lllll_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨ᡻")],
                    bstack11l1ll11lll_opy_[bstack11lllll_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩ᡼")])
        os.environ[bstack11lllll_opy_ (u"ࠫࡎ࡙࡟ࡏࡑࡑࡣࡇ࡙ࡔࡂࡅࡎࡣࡎࡔࡆࡓࡃࡢࡅ࠶࠷࡙ࡠࡕࡈࡗࡘࡏࡏࡏࠩ᡽")] = bstack11lllll_opy_ (u"ࠬࡺࡲࡶࡧࠪ᡾")
        return bstack111ll1ll1_opy_
      else:
        chrome_options = None
        if isinstance(bstack111ll1ll1_opy_, ChromeOptions):
          chrome_options = bstack111ll1ll1_opy_
        elif isinstance(bstack111ll1ll1_opy_, dict):
          for value in bstack111ll1ll1_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack111ll1ll1_opy_, dict):
            bstack111ll1ll1_opy_[bstack11lllll_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧ᡿")] = chrome_options
          else:
            bstack111ll1ll1_opy_ = chrome_options
        if bstack11l1ll11lll_opy_ is not None:
          if bstack11lllll_opy_ (u"ࠧࡢࡴࡪࡷࠬᢀ") in bstack11l1ll11lll_opy_:
                bstack11l1l11l1ll_opy_ = chrome_options.arguments or []
                new_args = bstack11l1ll11lll_opy_[bstack11lllll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᢁ")]
                for arg in new_args:
                    if arg not in bstack11l1l11l1ll_opy_:
                        chrome_options.add_argument(arg)
          if bstack11lllll_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᢂ") in bstack11l1ll11lll_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack11lllll_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᢃ"), [])
                bstack11l1l1l1l1l_opy_ = bstack11l1ll11lll_opy_[bstack11lllll_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨᢄ")]
                for extension in bstack11l1l1l1l1l_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack11lllll_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫᢅ") in bstack11l1ll11lll_opy_:
                bstack11l1l111111_opy_ = chrome_options.experimental_options.get(bstack11lllll_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬᢆ"), {})
                bstack11l1ll11111_opy_ = bstack11l1ll11lll_opy_[bstack11lllll_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ᢇ")]
                bstack11l1l1l1lll_opy_(bstack11l1l111111_opy_, bstack11l1ll11111_opy_)
                chrome_options.add_experimental_option(bstack11lllll_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᢈ"), bstack11l1l111111_opy_)
        os.environ[bstack11lllll_opy_ (u"ࠩࡌࡗࡤࡔࡏࡏࡡࡅࡗ࡙ࡇࡃࡌࡡࡌࡒࡋࡘࡁࡠࡃ࠴࠵࡞ࡥࡓࡆࡕࡖࡍࡔࡔࠧᢉ")] = bstack11lllll_opy_ (u"ࠪࡸࡷࡻࡥࠨᢊ")
        return bstack111ll1ll1_opy_
    except Exception as e:
      logger.error(bstack11lllll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡤࡨࡩ࡯࡮ࡨࠢࡱࡳࡳ࠳ࡂࡔࠢ࡬ࡲ࡫ࡸࡡࠡࡣ࠴࠵ࡾࠦࡣࡩࡴࡲࡱࡪࠦ࡯ࡱࡶ࡬ࡳࡳࡹ࠺ࠡࠤᢋ") + str(e))
      return bstack111ll1ll1_opy_