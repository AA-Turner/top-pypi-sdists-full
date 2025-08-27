# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack11lll111lll_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack11ll1ll11l1_opy_ as bstack11ll1l111ll_opy_, EVENTS
from bstack_utils.bstack1l1ll1lll_opy_ import bstack1l1ll1lll_opy_
from bstack_utils.helper import bstack11l11ll1l1_opy_, bstack111l1111ll_opy_, bstack11l1111l1l_opy_, bstack11ll11llll1_opy_, \
  bstack11ll1l1l11l_opy_, bstack1l111ll11l_opy_, get_host_info, bstack11ll1ll1lll_opy_, bstack1l11l1l1_opy_, error_handler, bstack11ll1llllll_opy_, bstack11ll1lll1ll_opy_, bstack1l11l1l1ll_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack1l1l11111_opy_ import get_logger
from bstack_utils.bstack11l11111_opy_ import bstack1ll1llll11l_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
logger = get_logger(__name__)
bstack11l11111_opy_ = bstack1ll1llll11l_opy_()
@error_handler(class_method=False)
def _11ll1l1ll1l_opy_(driver, bstack1111l1lll1_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1111lll_opy_ (u"ࠫࡴࡹ࡟࡯ࡣࡰࡩࠬᘕ"): caps.get(bstack1111lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫᘖ"), None),
        bstack1111lll_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪᘗ"): bstack1111l1lll1_opy_.get(bstack1111lll_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪᘘ"), None),
        bstack1111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧᘙ"): caps.get(bstack1111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᘚ"), None),
        bstack1111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᘛ"): caps.get(bstack1111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᘜ"), None)
    }
  except Exception as error:
    logger.debug(bstack1111lll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫࡫ࡴࡤࡪ࡬ࡲ࡬ࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡦࡨࡸࡦ࡯࡬ࡴࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࠦ࠺ࠡࠩᘝ") + str(error))
  return response
def on():
    if os.environ.get(bstack1111lll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᘞ"), None) is None or os.environ[bstack1111lll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᘟ")] == bstack1111lll_opy_ (u"ࠣࡰࡸࡰࡱࠨᘠ"):
        return False
    return True
def bstack1l111l111_opy_(config):
  return config.get(bstack1111lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᘡ"), False) or any([p.get(bstack1111lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᘢ"), False) == True for p in config.get(bstack1111lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᘣ"), [])])
def bstack1l1l1lll1l_opy_(config, bstack1111ll11_opy_):
  try:
    bstack11ll1l11l1l_opy_ = config.get(bstack1111lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᘤ"), False)
    if int(bstack1111ll11_opy_) < len(config.get(bstack1111lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᘥ"), [])) and config[bstack1111lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᘦ")][bstack1111ll11_opy_]:
      bstack11lll111l11_opy_ = config[bstack1111lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᘧ")][bstack1111ll11_opy_].get(bstack1111lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᘨ"), None)
    else:
      bstack11lll111l11_opy_ = config.get(bstack1111lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᘩ"), None)
    if bstack11lll111l11_opy_ != None:
      bstack11ll1l11l1l_opy_ = bstack11lll111l11_opy_
    bstack11ll1l1l1ll_opy_ = os.getenv(bstack1111lll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᘪ")) is not None and len(os.getenv(bstack1111lll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᘫ"))) > 0 and os.getenv(bstack1111lll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᘬ")) != bstack1111lll_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᘭ")
    return bstack11ll1l11l1l_opy_ and bstack11ll1l1l1ll_opy_
  except Exception as error:
    logger.debug(bstack1111lll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡧࡵ࡭࡫ࡿࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶࠥࡀࠠࠨᘮ") + str(error))
  return False
def bstack11llll111l_opy_(test_tags):
  bstack1ll11ll11l1_opy_ = os.getenv(bstack1111lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᘯ"))
  if bstack1ll11ll11l1_opy_ is None:
    return True
  bstack1ll11ll11l1_opy_ = json.loads(bstack1ll11ll11l1_opy_)
  try:
    include_tags = bstack1ll11ll11l1_opy_[bstack1111lll_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᘰ")] if bstack1111lll_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᘱ") in bstack1ll11ll11l1_opy_ and isinstance(bstack1ll11ll11l1_opy_[bstack1111lll_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᘲ")], list) else []
    exclude_tags = bstack1ll11ll11l1_opy_[bstack1111lll_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᘳ")] if bstack1111lll_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᘴ") in bstack1ll11ll11l1_opy_ and isinstance(bstack1ll11ll11l1_opy_[bstack1111lll_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᘵ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1111lll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡷࡣ࡯࡭ࡩࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡡ࡯ࡰ࡬ࡲ࡬࠴ࠠࡆࡴࡵࡳࡷࠦ࠺ࠡࠤᘶ") + str(error))
  return False
def bstack11ll1ll1l11_opy_(config, bstack11lll1111l1_opy_, bstack11lll111111_opy_, bstack11lll111l1l_opy_):
  bstack11ll1l1lll1_opy_ = bstack11ll11llll1_opy_(config)
  bstack11ll1lll111_opy_ = bstack11ll1l1l11l_opy_(config)
  if bstack11ll1l1lll1_opy_ is None or bstack11ll1lll111_opy_ is None:
    logger.error(bstack1111lll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡸࡵ࡯ࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࡑ࡮ࡹࡳࡪࡰࡪࠤࡦࡻࡴࡩࡧࡱࡸ࡮ࡩࡡࡵ࡫ࡲࡲࠥࡺ࡯࡬ࡧࡱࠫᘷ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1111lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᘸ"), bstack1111lll_opy_ (u"ࠬࢁࡽࠨᘹ")))
    data = {
        bstack1111lll_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᘺ"): config[bstack1111lll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᘻ")],
        bstack1111lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᘼ"): config.get(bstack1111lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬᘽ"), os.path.basename(os.getcwd())),
        bstack1111lll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡖ࡬ࡱࡪ࠭ᘾ"): bstack11l11ll1l1_opy_(),
        bstack1111lll_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩᘿ"): config.get(bstack1111lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᙀ"), bstack1111lll_opy_ (u"࠭ࠧᙁ")),
        bstack1111lll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧᙂ"): {
            bstack1111lll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡒࡦࡳࡥࠨᙃ"): bstack11lll1111l1_opy_,
            bstack1111lll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬᙄ"): bstack11lll111111_opy_,
            bstack1111lll_opy_ (u"ࠪࡷࡩࡱࡖࡦࡴࡶ࡭ࡴࡴࠧᙅ"): __version__,
            bstack1111lll_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭ᙆ"): bstack1111lll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᙇ"),
            bstack1111lll_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᙈ"): bstack1111lll_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩᙉ"),
            bstack1111lll_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᙊ"): bstack11lll111l1l_opy_
        },
        bstack1111lll_opy_ (u"ࠩࡶࡩࡹࡺࡩ࡯ࡩࡶࠫᙋ"): settings,
        bstack1111lll_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࡇࡴࡴࡴࡳࡱ࡯ࠫᙌ"): bstack11ll1ll1lll_opy_(),
        bstack1111lll_opy_ (u"ࠫࡨ࡯ࡉ࡯ࡨࡲࠫᙍ"): bstack1l111ll11l_opy_(),
        bstack1111lll_opy_ (u"ࠬ࡮࡯ࡴࡶࡌࡲ࡫ࡵࠧᙎ"): get_host_info(),
        bstack1111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᙏ"): bstack11l1111l1l_opy_(config)
    }
    headers = {
        bstack1111lll_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ᙐ"): bstack1111lll_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫᙑ"),
    }
    config = {
        bstack1111lll_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᙒ"): (bstack11ll1l1lll1_opy_, bstack11ll1lll111_opy_),
        bstack1111lll_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᙓ"): headers
    }
    response = bstack1l11l1l1_opy_(bstack1111lll_opy_ (u"ࠫࡕࡕࡓࡕࠩᙔ"), bstack11ll1l111ll_opy_ + bstack1111lll_opy_ (u"ࠬ࠵ࡶ࠳࠱ࡷࡩࡸࡺ࡟ࡳࡷࡱࡷࠬᙕ"), data, config)
    bstack11ll1llll1l_opy_ = response.json()
    if bstack11ll1llll1l_opy_[bstack1111lll_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧᙖ")]:
      parsed = json.loads(os.getenv(bstack1111lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᙗ"), bstack1111lll_opy_ (u"ࠨࡽࢀࠫᙘ")))
      parsed[bstack1111lll_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᙙ")] = bstack11ll1llll1l_opy_[bstack1111lll_opy_ (u"ࠪࡨࡦࡺࡡࠨᙚ")][bstack1111lll_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᙛ")]
      os.environ[bstack1111lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᙜ")] = json.dumps(parsed)
      bstack1l1ll1lll_opy_.bstack1lll111ll_opy_(bstack11ll1llll1l_opy_[bstack1111lll_opy_ (u"࠭ࡤࡢࡶࡤࠫᙝ")][bstack1111lll_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨᙞ")])
      bstack1l1ll1lll_opy_.bstack11ll1ll1l1l_opy_(bstack11ll1llll1l_opy_[bstack1111lll_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᙟ")][bstack1111lll_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫᙠ")])
      bstack1l1ll1lll_opy_.store()
      return bstack11ll1llll1l_opy_[bstack1111lll_opy_ (u"ࠪࡨࡦࡺࡡࠨᙡ")][bstack1111lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡘࡴࡱࡥ࡯ࠩᙢ")], bstack11ll1llll1l_opy_[bstack1111lll_opy_ (u"ࠬࡪࡡࡵࡣࠪᙣ")][bstack1111lll_opy_ (u"࠭ࡩࡥࠩᙤ")]
    else:
      logger.error(bstack1111lll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࠨᙥ") + bstack11ll1llll1l_opy_[bstack1111lll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᙦ")])
      if bstack11ll1llll1l_opy_[bstack1111lll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᙧ")] == bstack1111lll_opy_ (u"ࠪࡍࡳࡼࡡ࡭࡫ࡧࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡵࡧࡳࡴࡧࡧ࠲ࠬᙨ"):
        for bstack11ll1l1l111_opy_ in bstack11ll1llll1l_opy_[bstack1111lll_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶࠫᙩ")]:
          logger.error(bstack11ll1l1l111_opy_[bstack1111lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᙪ")])
      return None, None
  except Exception as error:
    logger.error(bstack1111lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࠢᙫ") +  str(error))
    return None, None
def bstack11lll111ll1_opy_():
  if os.getenv(bstack1111lll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᙬ")) is None:
    return {
        bstack1111lll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ᙭"): bstack1111lll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ᙮"),
        bstack1111lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᙯ"): bstack1111lll_opy_ (u"ࠫࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥ࡮ࡡࡥࠢࡩࡥ࡮ࡲࡥࡥ࠰ࠪᙰ")
    }
  data = {bstack1111lll_opy_ (u"ࠬ࡫࡮ࡥࡖ࡬ࡱࡪ࠭ᙱ"): bstack11l11ll1l1_opy_()}
  headers = {
      bstack1111lll_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭ᙲ"): bstack1111lll_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࠨᙳ") + os.getenv(bstack1111lll_opy_ (u"ࠣࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙ࠨᙴ")),
      bstack1111lll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨᙵ"): bstack1111lll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ᙶ")
  }
  response = bstack1l11l1l1_opy_(bstack1111lll_opy_ (u"ࠫࡕ࡛ࡔࠨᙷ"), bstack11ll1l111ll_opy_ + bstack1111lll_opy_ (u"ࠬ࠵ࡴࡦࡵࡷࡣࡷࡻ࡮ࡴ࠱ࡶࡸࡴࡶࠧᙸ"), data, { bstack1111lll_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᙹ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1111lll_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡘࡪࡹࡴࠡࡔࡸࡲࠥࡳࡡࡳ࡭ࡨࡨࠥࡧࡳࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠤࡦࡺࠠࠣᙺ") + bstack111l1111ll_opy_().isoformat() + bstack1111lll_opy_ (u"ࠨ࡜ࠪᙻ"))
      return {bstack1111lll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᙼ"): bstack1111lll_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫᙽ"), bstack1111lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᙾ"): bstack1111lll_opy_ (u"ࠬ࠭ᙿ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1111lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡦࡳࡲࡶ࡬ࡦࡶ࡬ࡳࡳࠦ࡯ࡧࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡚ࠥࡥࡴࡶࠣࡖࡺࡴ࠺ࠡࠤ ") + str(error))
    return {
        bstack1111lll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᚁ"): bstack1111lll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᚂ"),
        bstack1111lll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᚃ"): str(error)
    }
def bstack11ll1ll111l_opy_(bstack11ll11lllll_opy_):
    return re.match(bstack1111lll_opy_ (u"ࡵࠫࡣࡢࡤࠬࠪ࡟࠲ࡡࡪࠫࠪࡁࠧࠫᚄ"), bstack11ll11lllll_opy_.strip()) is not None
def bstack1111111l_opy_(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack11ll1l11111_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11ll1l11111_opy_ = desired_capabilities
        else:
          bstack11ll1l11111_opy_ = {}
        bstack1ll111l1111_opy_ = (bstack11ll1l11111_opy_.get(bstack1111lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪᚅ"), bstack1111lll_opy_ (u"ࠬ࠭ᚆ")).lower() or caps.get(bstack1111lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬᚇ"), bstack1111lll_opy_ (u"ࠧࠨᚈ")).lower())
        if bstack1ll111l1111_opy_ == bstack1111lll_opy_ (u"ࠨ࡫ࡲࡷࠬᚉ"):
            return True
        if bstack1ll111l1111_opy_ == bstack1111lll_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࠪᚊ"):
            bstack1ll11lll1ll_opy_ = str(float(caps.get(bstack1111lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᚋ")) or bstack11ll1l11111_opy_.get(bstack1111lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᚌ"), {}).get(bstack1111lll_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨᚍ"),bstack1111lll_opy_ (u"࠭ࠧᚎ"))))
            if bstack1ll111l1111_opy_ == bstack1111lll_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࠨᚏ") and int(bstack1ll11lll1ll_opy_.split(bstack1111lll_opy_ (u"ࠨ࠰ࠪᚐ"))[0]) < float(bstack11lll1111ll_opy_):
                logger.warning(str(bstack11lll11111l_opy_))
                return False
            return True
        bstack1ll11l1llll_opy_ = caps.get(bstack1111lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᚑ"), {}).get(bstack1111lll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧᚒ"), caps.get(bstack1111lll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫᚓ"), bstack1111lll_opy_ (u"ࠬ࠭ᚔ")))
        if bstack1ll11l1llll_opy_:
            logger.warning(bstack1111lll_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡄࡦࡵ࡮ࡸࡴࡶࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥᚕ"))
            return False
        browser = caps.get(bstack1111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᚖ"), bstack1111lll_opy_ (u"ࠨࠩᚗ")).lower() or bstack11ll1l11111_opy_.get(bstack1111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᚘ"), bstack1111lll_opy_ (u"ࠪࠫᚙ")).lower()
        if browser != bstack1111lll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫᚚ"):
            logger.warning(bstack1111lll_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣ᚛"))
            return False
        browser_version = caps.get(bstack1111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ᚜")) or caps.get(bstack1111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ᚝")) or bstack11ll1l11111_opy_.get(bstack1111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ᚞")) or bstack11ll1l11111_opy_.get(bstack1111lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ᚟"), {}).get(bstack1111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᚠ")) or bstack11ll1l11111_opy_.get(bstack1111lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᚡ"), {}).get(bstack1111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᚢ"))
        bstack1ll1l111111_opy_ = bstack11lll111lll_opy_.bstack1ll111ll11l_opy_
        bstack11ll1llll11_opy_ = False
        if config is not None:
          bstack11ll1llll11_opy_ = bstack1111lll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪᚣ") in config and str(config[bstack1111lll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫᚤ")]).lower() != bstack1111lll_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧᚥ")
        if os.environ.get(bstack1111lll_opy_ (u"ࠩࡌࡗࡤࡔࡏࡏࡡࡅࡗ࡙ࡇࡃࡌࡡࡌࡒࡋࡘࡁࡠࡃ࠴࠵࡞ࡥࡓࡆࡕࡖࡍࡔࡔࠧᚦ"), bstack1111lll_opy_ (u"ࠪࠫᚧ")).lower() == bstack1111lll_opy_ (u"ࠫࡹࡸࡵࡦࠩᚨ") or bstack11ll1llll11_opy_:
          bstack1ll1l111111_opy_ = bstack11lll111lll_opy_.bstack1ll111l1ll1_opy_
        if browser_version and browser_version != bstack1111lll_opy_ (u"ࠬࡲࡡࡵࡧࡶࡸࠬᚩ") and int(browser_version.split(bstack1111lll_opy_ (u"࠭࠮ࠨᚪ"))[0]) <= bstack1ll1l111111_opy_:
          logger.warning(bstack1llll1l1ll1_opy_ (u"ࠧࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡪࡶࡪࡧࡴࡦࡴࠣࡸ࡭ࡧ࡮ࠡࡽࡰ࡭ࡳࡥࡡ࠲࠳ࡼࡣࡸࡻࡰࡱࡱࡵࡸࡪࡪ࡟ࡤࡪࡵࡳࡲ࡫࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࡾ࠰ࠪᚫ"))
          return False
        if not options:
          bstack1ll11lll1l1_opy_ = caps.get(bstack1111lll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᚬ")) or bstack11ll1l11111_opy_.get(bstack1111lll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᚭ"), {})
          if bstack1111lll_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹࠧᚮ") in bstack1ll11lll1l1_opy_.get(bstack1111lll_opy_ (u"ࠫࡦࡸࡧࡴࠩᚯ"), []):
              logger.warning(bstack1111lll_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠ࡯ࡱࡷࠤࡷࡻ࡮ࠡࡱࡱࠤࡱ࡫ࡧࡢࡥࡼࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲࡙ࠥࡷࡪࡶࡦ࡬ࠥࡺ࡯ࠡࡰࡨࡻࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩࠥࡵࡲࠡࡣࡹࡳ࡮ࡪࠠࡶࡵ࡬ࡲ࡬ࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠢᚰ"))
              return False
        return True
    except Exception as error:
        logger.debug(bstack1111lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡡ࡭࡫ࡧࡥࡹ࡫ࠠࡢ࠳࠴ࡽࠥࡹࡵࡱࡲࡲࡶࡹࠦ࠺ࠣᚱ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1ll1llll1l1_opy_ = config.get(bstack1111lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᚲ"), {})
    bstack1ll1llll1l1_opy_[bstack1111lll_opy_ (u"ࠨࡣࡸࡸ࡭࡚࡯࡬ࡧࡱࠫᚳ")] = os.getenv(bstack1111lll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᚴ"))
    bstack11ll1l1l1l1_opy_ = json.loads(os.getenv(bstack1111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᚵ"), bstack1111lll_opy_ (u"ࠫࢀࢃࠧᚶ"))).get(bstack1111lll_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᚷ"))
    if not config[bstack1111lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨᚸ")].get(bstack1111lll_opy_ (u"ࠢࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪࠨᚹ")):
      if bstack1111lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᚺ") in caps:
        caps[bstack1111lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᚻ")][bstack1111lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᚼ")] = bstack1ll1llll1l1_opy_
        caps[bstack1111lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᚽ")][bstack1111lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᚾ")][bstack1111lll_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᚿ")] = bstack11ll1l1l1l1_opy_
      else:
        caps[bstack1111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᛀ")] = bstack1ll1llll1l1_opy_
        caps[bstack1111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᛁ")][bstack1111lll_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᛂ")] = bstack11ll1l1l1l1_opy_
  except Exception as error:
    logger.debug(bstack1111lll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴ࠰ࠣࡉࡷࡸ࡯ࡳ࠼ࠣࠦᛃ") +  str(error))
def bstack11111llll_opy_(driver, bstack11ll1l11l11_opy_):
  try:
    setattr(driver, bstack1111lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫᛄ"), True)
    session = driver.session_id
    if session:
      bstack11ll1ll1ll1_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11ll1ll1ll1_opy_ = False
      bstack11ll1ll1ll1_opy_ = url.scheme in [bstack1111lll_opy_ (u"ࠧ࡮ࡴࡵࡲࠥᛅ"), bstack1111lll_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧᛆ")]
      if bstack11ll1ll1ll1_opy_:
        if bstack11ll1l11l11_opy_:
          logger.info(bstack1111lll_opy_ (u"ࠢࡔࡧࡷࡹࡵࠦࡦࡰࡴࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡭ࡧࡳࠡࡵࡷࡥࡷࡺࡥࡥ࠰ࠣࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡥࡩ࡬࡯࡮ࠡ࡯ࡲࡱࡪࡴࡴࡢࡴ࡬ࡰࡾ࠴ࠢᛇ"))
      return bstack11ll1l11l11_opy_
  except Exception as e:
    logger.error(bstack1111lll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡤࡶࡹ࡯࡮ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦ࠼ࠣࠦᛈ") + str(e))
    return False
def bstack1ll1ll1l1l_opy_(driver, name, path):
  try:
    bstack1ll111ll1ll_opy_ = {
        bstack1111lll_opy_ (u"ࠩࡷ࡬࡙࡫ࡳࡵࡔࡸࡲ࡚ࡻࡩࡥࠩᛉ"): threading.current_thread().current_test_uuid,
        bstack1111lll_opy_ (u"ࠪࡸ࡭ࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨᛊ"): os.environ.get(bstack1111lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᛋ"), bstack1111lll_opy_ (u"ࠬ࠭ᛌ")),
        bstack1111lll_opy_ (u"࠭ࡴࡩࡌࡺࡸ࡙ࡵ࡫ࡦࡰࠪᛍ"): os.environ.get(bstack1111lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫᛎ"), bstack1111lll_opy_ (u"ࠨࠩᛏ"))
    }
    bstack1ll11l1l11l_opy_ = bstack11l11111_opy_.bstack1ll111llll1_opy_(EVENTS.bstack1l1ll1lll1_opy_.value)
    logger.debug(bstack1111lll_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡧࡶࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠬᛐ"))
    try:
      if (bstack1l11l1l1ll_opy_(threading.current_thread(), bstack1111lll_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪᛑ"), None) and bstack1l11l1l1ll_opy_(threading.current_thread(), bstack1111lll_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᛒ"), None)):
        scripts = {bstack1111lll_opy_ (u"ࠬࡹࡣࡢࡰࠪᛓ"): bstack1l1ll1lll_opy_.perform_scan}
        bstack11ll1lll11l_opy_ = json.loads(scripts[bstack1111lll_opy_ (u"ࠨࡳࡤࡣࡱࠦᛔ")].replace(bstack1111lll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࠥᛕ"), bstack1111lll_opy_ (u"ࠣࠤᛖ")))
        bstack11ll1lll11l_opy_[bstack1111lll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᛗ")][bstack1111lll_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࠪᛘ")] = None
        scripts[bstack1111lll_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᛙ")] = bstack1111lll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠣᛚ") + json.dumps(bstack11ll1lll11l_opy_)
        bstack1l1ll1lll_opy_.bstack1lll111ll_opy_(scripts)
        bstack1l1ll1lll_opy_.store()
        logger.debug(driver.execute_script(bstack1l1ll1lll_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1l1ll1lll_opy_.perform_scan, {bstack1111lll_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࠨᛛ"): name}))
      bstack11l11111_opy_.end(EVENTS.bstack1l1ll1lll1_opy_.value, bstack1ll11l1l11l_opy_ + bstack1111lll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᛜ"), bstack1ll11l1l11l_opy_ + bstack1111lll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᛝ"), True, None)
    except Exception as error:
      bstack11l11111_opy_.end(EVENTS.bstack1l1ll1lll1_opy_.value, bstack1ll11l1l11l_opy_ + bstack1111lll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᛞ"), bstack1ll11l1l11l_opy_ + bstack1111lll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᛟ"), False, str(error))
    bstack1ll11l1l11l_opy_ = bstack11l11111_opy_.bstack11ll1lllll1_opy_(EVENTS.bstack1ll11llll11_opy_.value)
    bstack11l11111_opy_.mark(bstack1ll11l1l11l_opy_ + bstack1111lll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᛠ"))
    try:
      if (bstack1l11l1l1ll_opy_(threading.current_thread(), bstack1111lll_opy_ (u"ࠬ࡯ࡳࡂࡲࡳࡅ࠶࠷ࡹࡕࡧࡶࡸࠬᛡ"), None) and bstack1l11l1l1ll_opy_(threading.current_thread(), bstack1111lll_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᛢ"), None)):
        scripts = {bstack1111lll_opy_ (u"ࠧࡴࡥࡤࡲࠬᛣ"): bstack1l1ll1lll_opy_.perform_scan}
        bstack11ll1lll11l_opy_ = json.loads(scripts[bstack1111lll_opy_ (u"ࠣࡵࡦࡥࡳࠨᛤ")].replace(bstack1111lll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠧᛥ"), bstack1111lll_opy_ (u"ࠥࠦᛦ")))
        bstack11ll1lll11l_opy_[bstack1111lll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᛧ")][bstack1111lll_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬᛨ")] = None
        scripts[bstack1111lll_opy_ (u"ࠨࡳࡤࡣࡱࠦᛩ")] = bstack1111lll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࠥᛪ") + json.dumps(bstack11ll1lll11l_opy_)
        bstack1l1ll1lll_opy_.bstack1lll111ll_opy_(scripts)
        bstack1l1ll1lll_opy_.store()
        logger.debug(driver.execute_script(bstack1l1ll1lll_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1l1ll1lll_opy_.bstack11ll1l1111l_opy_, bstack1ll111ll1ll_opy_))
      bstack11l11111_opy_.end(bstack1ll11l1l11l_opy_, bstack1ll11l1l11l_opy_ + bstack1111lll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ᛫"), bstack1ll11l1l11l_opy_ + bstack1111lll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ᛬"),True, None)
    except Exception as error:
      bstack11l11111_opy_.end(bstack1ll11l1l11l_opy_, bstack1ll11l1l11l_opy_ + bstack1111lll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ᛭"), bstack1ll11l1l11l_opy_ + bstack1111lll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᛮ"),False, str(error))
    logger.info(bstack1111lll_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠣᛯ"))
  except Exception as bstack1ll11l11lll_opy_:
    logger.error(bstack1111lll_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡤࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡦࡪࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡩࡳࡷࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࡀࠠࠣᛰ") + str(path) + bstack1111lll_opy_ (u"ࠢࠡࡇࡵࡶࡴࡸࠠ࠻ࠤᛱ") + str(bstack1ll11l11lll_opy_))
def bstack11ll1lll1l1_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack1111lll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢᛲ")) and str(caps.get(bstack1111lll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣᛳ"))).lower() == bstack1111lll_opy_ (u"ࠥࡥࡳࡪࡲࡰ࡫ࡧࠦᛴ"):
        bstack1ll11lll1ll_opy_ = caps.get(bstack1111lll_opy_ (u"ࠦࡦࡶࡰࡪࡷࡰ࠾ࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨᛵ")) or caps.get(bstack1111lll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢᛶ"))
        if bstack1ll11lll1ll_opy_ and int(str(bstack1ll11lll1ll_opy_)) < bstack11lll1111ll_opy_:
            return False
    return True
def bstack11l1111l1_opy_(config):
  if bstack1111lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᛷ") in config:
        return config[bstack1111lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᛸ")]
  for platform in config.get(bstack1111lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ᛹"), []):
      if bstack1111lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ᛺") in platform:
          return platform[bstack1111lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ᛻")]
  return None
def bstack1ll1l11l11_opy_(bstack11l11l1l_opy_):
  try:
    browser_name = bstack11l11l1l_opy_[bstack1111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧࠪ᛼")]
    browser_version = bstack11l11l1l_opy_[bstack1111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ᛽")]
    chrome_options = bstack11l11l1l_opy_[bstack1111lll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡥ࡯ࡱࡶ࡬ࡳࡳࡹࠧ᛾")]
    try:
        bstack11ll1ll11ll_opy_ = int(browser_version.split(bstack1111lll_opy_ (u"ࠧ࠯ࠩ᛿"))[0])
    except ValueError as e:
        logger.error(bstack1111lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡣࡰࡰࡹࡩࡷࡺࡩ࡯ࡩࠣࡦࡷࡵࡷࡴࡧࡵࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠧᜀ") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack1111lll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩᜁ")):
        logger.warning(bstack1111lll_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᜂ"))
        return False
    if bstack11ll1ll11ll_opy_ < bstack11lll111lll_opy_.bstack1ll111l1ll1_opy_:
        logger.warning(bstack1llll1l1ll1_opy_ (u"ࠫࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡴࡨࡵࡺ࡯ࡲࡦࡵࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡺࡪࡸࡳࡪࡱࡱࠤࢀࡉࡏࡏࡕࡗࡅࡓ࡚ࡓ࠯ࡏࡌࡒࡎࡓࡕࡎࡡࡑࡓࡓࡥࡂࡔࡖࡄࡇࡐࡥࡉࡏࡈࡕࡅࡤࡇ࠱࠲࡛ࡢࡗ࡚ࡖࡐࡐࡔࡗࡉࡉࡥࡃࡉࡔࡒࡑࡊࡥࡖࡆࡔࡖࡍࡔࡔࡽࠡࡱࡵࠤ࡭࡯ࡧࡩࡧࡵ࠲ࠬᜃ"))
        return False
    if chrome_options and any(bstack1111lll_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴࠩᜄ") in value for value in chrome_options.values() if isinstance(value, str)):
        logger.warning(bstack1111lll_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡰࡲࡸࠥࡸࡵ࡯ࠢࡲࡲࠥࡲࡥࡨࡣࡦࡽࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠦࡓࡸ࡫ࡷࡧ࡭ࠦࡴࡰࠢࡱࡩࡼࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪࠦ࡯ࡳࠢࡤࡺࡴ࡯ࡤࠡࡷࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠣᜅ"))
        return False
    return True
  except Exception as e:
    logger.error(bstack1111lll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡦ࡬ࡪࡩ࡫ࡪࡰࡪࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡳࡶࡲࡳࡳࡷࡺࠠࡧࡱࡵࠤࡱࡵࡣࡢ࡮ࠣࡇ࡭ࡸ࡯࡮ࡧ࠽ࠤࠧᜆ") + str(e))
    return False
def bstack1lll1l1l1_opy_(bstack1ll1llll1_opy_, config):
    try:
      bstack1ll11ll1lll_opy_ = bstack1111lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᜇ") in config and config[bstack1111lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᜈ")] == True
      bstack11ll1llll11_opy_ = bstack1111lll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧᜉ") in config and str(config[bstack1111lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨᜊ")]).lower() != bstack1111lll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫᜋ")
      if not (bstack1ll11ll1lll_opy_ and (not bstack11l1111l1l_opy_(config) or bstack11ll1llll11_opy_)):
        return bstack1ll1llll1_opy_
      bstack11ll1l11lll_opy_ = bstack1l1ll1lll_opy_.bstack11ll1l111l1_opy_
      if bstack11ll1l11lll_opy_ is None:
        logger.debug(bstack1111lll_opy_ (u"ࠨࡇࡰࡱࡪࡰࡪࠦࡣࡩࡴࡲࡱࡪࠦ࡯ࡱࡶ࡬ࡳࡳࡹࠠࡢࡴࡨࠤࡓࡵ࡮ࡦࠤᜌ"))
        return bstack1ll1llll1_opy_
      bstack11ll1ll1111_opy_ = int(str(bstack11ll1lll1ll_opy_()).split(bstack1111lll_opy_ (u"ࠧ࠯ࠩᜍ"))[0])
      logger.debug(bstack1111lll_opy_ (u"ࠣࡕࡨࡰࡪࡴࡩࡶ࡯ࠣࡺࡪࡸࡳࡪࡱࡱࠤࡩ࡫ࡴࡦࡥࡷࡩࡩࡀࠠࠣᜎ") + str(bstack11ll1ll1111_opy_) + bstack1111lll_opy_ (u"ࠤࠥᜏ"))
      if bstack11ll1ll1111_opy_ == 3 and isinstance(bstack1ll1llll1_opy_, dict) and bstack1111lll_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᜐ") in bstack1ll1llll1_opy_ and bstack11ll1l11lll_opy_ is not None:
        if bstack1111lll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᜑ") not in bstack1ll1llll1_opy_[bstack1111lll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᜒ")]:
          bstack1ll1llll1_opy_[bstack1111lll_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᜓ")][bstack1111lll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷ᜔ࠬ")] = {}
        if bstack1111lll_opy_ (u"ࠨࡣࡵ࡫ࡸ᜕࠭") in bstack11ll1l11lll_opy_:
          if bstack1111lll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ᜖") not in bstack1ll1llll1_opy_[bstack1111lll_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ᜗")][bstack1111lll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᜘")]:
            bstack1ll1llll1_opy_[bstack1111lll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬ᜙")][bstack1111lll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ᜚")][bstack1111lll_opy_ (u"ࠧࡢࡴࡪࡷࠬ᜛")] = []
          for arg in bstack11ll1l11lll_opy_[bstack1111lll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭᜜")]:
            if arg not in bstack1ll1llll1_opy_[bstack1111lll_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ᜝")][bstack1111lll_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ᜞")][bstack1111lll_opy_ (u"ࠫࡦࡸࡧࡴࠩᜟ")]:
              bstack1ll1llll1_opy_[bstack1111lll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᜠ")][bstack1111lll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᜡ")][bstack1111lll_opy_ (u"ࠧࡢࡴࡪࡷࠬᜢ")].append(arg)
        if bstack1111lll_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᜣ") in bstack11ll1l11lll_opy_:
          if bstack1111lll_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᜤ") not in bstack1ll1llll1_opy_[bstack1111lll_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᜥ")][bstack1111lll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᜦ")]:
            bstack1ll1llll1_opy_[bstack1111lll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᜧ")][bstack1111lll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᜨ")][bstack1111lll_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᜩ")] = []
          for ext in bstack11ll1l11lll_opy_[bstack1111lll_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᜪ")]:
            if ext not in bstack1ll1llll1_opy_[bstack1111lll_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᜫ")][bstack1111lll_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᜬ")][bstack1111lll_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨᜭ")]:
              bstack1ll1llll1_opy_[bstack1111lll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᜮ")][bstack1111lll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᜯ")][bstack1111lll_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᜰ")].append(ext)
        if bstack1111lll_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᜱ") in bstack11ll1l11lll_opy_:
          if bstack1111lll_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᜲ") not in bstack1ll1llll1_opy_[bstack1111lll_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᜳ")][bstack1111lll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴ᜴ࠩ")]:
            bstack1ll1llll1_opy_[bstack1111lll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬ᜵")][bstack1111lll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ᜶")][bstack1111lll_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭᜷")] = {}
          bstack11ll1llllll_opy_(bstack1ll1llll1_opy_[bstack1111lll_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ᜸")][bstack1111lll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᜹")][bstack1111lll_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩ᜺")],
                    bstack11ll1l11lll_opy_[bstack1111lll_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪ᜻")])
        os.environ[bstack1111lll_opy_ (u"ࠬࡏࡓࡠࡐࡒࡒࡤࡈࡓࡕࡃࡆࡏࡤࡏࡎࡇࡔࡄࡣࡆ࠷࠱࡚ࡡࡖࡉࡘ࡙ࡉࡐࡐࠪ᜼")] = bstack1111lll_opy_ (u"࠭ࡴࡳࡷࡨࠫ᜽")
        return bstack1ll1llll1_opy_
      else:
        chrome_options = None
        if isinstance(bstack1ll1llll1_opy_, ChromeOptions):
          chrome_options = bstack1ll1llll1_opy_
        elif isinstance(bstack1ll1llll1_opy_, dict):
          for value in bstack1ll1llll1_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack1ll1llll1_opy_, dict):
            bstack1ll1llll1_opy_[bstack1111lll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ᜾")] = chrome_options
          else:
            bstack1ll1llll1_opy_ = chrome_options
        if bstack11ll1l11lll_opy_ is not None:
          if bstack1111lll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭᜿") in bstack11ll1l11lll_opy_:
                bstack11lll11l111_opy_ = chrome_options.arguments or []
                new_args = bstack11ll1l11lll_opy_[bstack1111lll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᝀ")]
                for arg in new_args:
                    if arg not in bstack11lll11l111_opy_:
                        chrome_options.add_argument(arg)
          if bstack1111lll_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᝁ") in bstack11ll1l11lll_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack1111lll_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨᝂ"), [])
                bstack11ll1l1llll_opy_ = bstack11ll1l11lll_opy_[bstack1111lll_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᝃ")]
                for extension in bstack11ll1l1llll_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack1111lll_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬᝄ") in bstack11ll1l11lll_opy_:
                bstack11ll1l11ll1_opy_ = chrome_options.experimental_options.get(bstack1111lll_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ᝅ"), {})
                bstack11ll1l1ll11_opy_ = bstack11ll1l11lll_opy_[bstack1111lll_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᝆ")]
                bstack11ll1llllll_opy_(bstack11ll1l11ll1_opy_, bstack11ll1l1ll11_opy_)
                chrome_options.add_experimental_option(bstack1111lll_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᝇ"), bstack11ll1l11ll1_opy_)
        os.environ[bstack1111lll_opy_ (u"ࠪࡍࡘࡥࡎࡐࡐࡢࡆࡘ࡚ࡁࡄࡍࡢࡍࡓࡌࡒࡂࡡࡄ࠵࠶࡟࡟ࡔࡇࡖࡗࡎࡕࡎࠨᝈ")] = bstack1111lll_opy_ (u"ࠫࡹࡸࡵࡦࠩᝉ")
        return bstack1ll1llll1_opy_
    except Exception as e:
      logger.error(bstack1111lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡥࡩࡪࡩ࡯ࡩࠣࡲࡴࡴ࠭ࡃࡕࠣ࡭ࡳ࡬ࡲࡢࠢࡤ࠵࠶ࡿࠠࡤࡪࡵࡳࡲ࡫ࠠࡰࡲࡷ࡭ࡴࡴࡳ࠻ࠢࠥᝊ") + str(e))
      return bstack1ll1llll1_opy_