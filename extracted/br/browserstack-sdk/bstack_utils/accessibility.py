# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack11ll111lll1_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack11ll111ll1l_opy_ as bstack11ll1l1l111_opy_, EVENTS
from bstack_utils.bstack1llll111_opy_ import bstack1llll111_opy_
from bstack_utils.helper import bstack11l1l1l1l1_opy_, bstack111l1l11ll_opy_, bstack11l1lll1ll_opy_, bstack11ll1ll11l1_opy_, \
  bstack11ll1ll1l11_opy_, bstack1l1llll111_opy_, get_host_info, bstack11ll1ll1l1l_opy_, bstack1lllll1111_opy_, error_handler, bstack11ll1ll1111_opy_, bstack11ll11l1111_opy_, bstack1111l1l11_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack1lll1llll_opy_ import get_logger
from bstack_utils.bstack1l1ll11l1l_opy_ import bstack1ll1ll11ll1_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
logger = get_logger(__name__)
bstack1l1ll11l1l_opy_ = bstack1ll1ll11ll1_opy_()
@error_handler(class_method=False)
def _11ll111llll_opy_(driver, bstack11111lll1l_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1ll11ll_opy_ (u"࠭࡯ࡴࡡࡱࡥࡲ࡫ࠧᘞ"): caps.get(bstack1ll11ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ᘟ"), None),
        bstack1ll11ll_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᘠ"): bstack11111lll1l_opy_.get(bstack1ll11ll_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬᘡ"), None),
        bstack1ll11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩᘢ"): caps.get(bstack1ll11ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᘣ"), None),
        bstack1ll11ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᘤ"): caps.get(bstack1ll11ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᘥ"), None)
    }
  except Exception as error:
    logger.debug(bstack1ll11ll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡪࡺࡡࡪ࡮ࡶࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲࠡ࠼ࠣࠫᘦ") + str(error))
  return response
def on():
    if os.environ.get(bstack1ll11ll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᘧ"), None) is None or os.environ[bstack1ll11ll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᘨ")] == bstack1ll11ll_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᘩ"):
        return False
    return True
def bstack1ll1l11lll_opy_(config):
  return config.get(bstack1ll11ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᘪ"), False) or any([p.get(bstack1ll11ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᘫ"), False) == True for p in config.get(bstack1ll11ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᘬ"), [])])
def bstack1l1l1lll1l_opy_(config, bstack11llll111l_opy_):
  try:
    bstack11ll1l1l1l1_opy_ = config.get(bstack1ll11ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᘭ"), False)
    if int(bstack11llll111l_opy_) < len(config.get(bstack1ll11ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᘮ"), [])) and config[bstack1ll11ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᘯ")][bstack11llll111l_opy_]:
      bstack11ll1l111l1_opy_ = config[bstack1ll11ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᘰ")][bstack11llll111l_opy_].get(bstack1ll11ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᘱ"), None)
    else:
      bstack11ll1l111l1_opy_ = config.get(bstack1ll11ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᘲ"), None)
    if bstack11ll1l111l1_opy_ != None:
      bstack11ll1l1l1l1_opy_ = bstack11ll1l111l1_opy_
    bstack11ll1l11ll1_opy_ = os.getenv(bstack1ll11ll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᘳ")) is not None and len(os.getenv(bstack1ll11ll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᘴ"))) > 0 and os.getenv(bstack1ll11ll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᘵ")) != bstack1ll11ll_opy_ (u"ࠩࡱࡹࡱࡲࠧᘶ")
    return bstack11ll1l1l1l1_opy_ and bstack11ll1l11ll1_opy_
  except Exception as error:
    logger.debug(bstack1ll11ll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡹࡩࡷ࡯ࡦࡺ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡩࡸࡹࡩࡰࡰࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸࠠ࠻ࠢࠪᘷ") + str(error))
  return False
def bstack1l1l1l11ll_opy_(test_tags):
  bstack1ll111llll1_opy_ = os.getenv(bstack1ll11ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᘸ"))
  if bstack1ll111llll1_opy_ is None:
    return True
  bstack1ll111llll1_opy_ = json.loads(bstack1ll111llll1_opy_)
  try:
    include_tags = bstack1ll111llll1_opy_[bstack1ll11ll_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᘹ")] if bstack1ll11ll_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᘺ") in bstack1ll111llll1_opy_ and isinstance(bstack1ll111llll1_opy_[bstack1ll11ll_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᘻ")], list) else []
    exclude_tags = bstack1ll111llll1_opy_[bstack1ll11ll_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᘼ")] if bstack1ll11ll_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᘽ") in bstack1ll111llll1_opy_ and isinstance(bstack1ll111llll1_opy_[bstack1ll11ll_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᘾ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1ll11ll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡹࡥࡱ࡯ࡤࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡢࡦࡨࡲࡶࡪࠦࡳࡤࡣࡱࡲ࡮ࡴࡧ࠯ࠢࡈࡶࡷࡵࡲࠡ࠼ࠣࠦᘿ") + str(error))
  return False
def bstack11ll1l1l1ll_opy_(config, bstack11ll11l1l1l_opy_, bstack11ll11llll1_opy_, bstack11ll1ll1lll_opy_):
  bstack11ll1l11lll_opy_ = bstack11ll1ll11l1_opy_(config)
  bstack11ll11ll111_opy_ = bstack11ll1ll1l11_opy_(config)
  if bstack11ll1l11lll_opy_ is None or bstack11ll11ll111_opy_ is None:
    logger.error(bstack1ll11ll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡳࡷࡱࠤ࡫ࡵࡲࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡡࡶࡶ࡫ࡩࡳࡺࡩࡤࡣࡷ࡭ࡴࡴࠠࡵࡱ࡮ࡩࡳ࠭ᙀ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1ll11ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧᙁ"), bstack1ll11ll_opy_ (u"ࠧࡼࡿࠪᙂ")))
    data = {
        bstack1ll11ll_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᙃ"): config[bstack1ll11ll_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᙄ")],
        bstack1ll11ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ᙅ"): config.get(bstack1ll11ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᙆ"), os.path.basename(os.getcwd())),
        bstack1ll11ll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡘ࡮ࡳࡥࠨᙇ"): bstack11l1l1l1l1_opy_(),
        bstack1ll11ll_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᙈ"): config.get(bstack1ll11ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪᙉ"), bstack1ll11ll_opy_ (u"ࠨࠩᙊ")),
        bstack1ll11ll_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩᙋ"): {
            bstack1ll11ll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡔࡡ࡮ࡧࠪᙌ"): bstack11ll11l1l1l_opy_,
            bstack1ll11ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧᙍ"): bstack11ll11llll1_opy_,
            bstack1ll11ll_opy_ (u"ࠬࡹࡤ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩᙎ"): __version__,
            bstack1ll11ll_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨᙏ"): bstack1ll11ll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧᙐ"),
            bstack1ll11ll_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᙑ"): bstack1ll11ll_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫᙒ"),
            bstack1ll11ll_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪᙓ"): bstack11ll1ll1lll_opy_
        },
        bstack1ll11ll_opy_ (u"ࠫࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭ᙔ"): settings,
        bstack1ll11ll_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࡉ࡯࡯ࡶࡵࡳࡱ࠭ᙕ"): bstack11ll1ll1l1l_opy_(),
        bstack1ll11ll_opy_ (u"࠭ࡣࡪࡋࡱࡪࡴ࠭ᙖ"): bstack1l1llll111_opy_(),
        bstack1ll11ll_opy_ (u"ࠧࡩࡱࡶࡸࡎࡴࡦࡰࠩᙗ"): get_host_info(),
        bstack1ll11ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᙘ"): bstack11l1lll1ll_opy_(config)
    }
    headers = {
        bstack1ll11ll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨᙙ"): bstack1ll11ll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ᙚ"),
    }
    config = {
        bstack1ll11ll_opy_ (u"ࠫࡦࡻࡴࡩࠩᙛ"): (bstack11ll1l11lll_opy_, bstack11ll11ll111_opy_),
        bstack1ll11ll_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᙜ"): headers
    }
    response = bstack1lllll1111_opy_(bstack1ll11ll_opy_ (u"࠭ࡐࡐࡕࡗࠫᙝ"), bstack11ll1l1l111_opy_ + bstack1ll11ll_opy_ (u"ࠧ࠰ࡸ࠵࠳ࡹ࡫ࡳࡵࡡࡵࡹࡳࡹࠧᙞ"), data, config)
    bstack11ll11ll1ll_opy_ = response.json()
    if bstack11ll11ll1ll_opy_[bstack1ll11ll_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩᙟ")]:
      parsed = json.loads(os.getenv(bstack1ll11ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᙠ"), bstack1ll11ll_opy_ (u"ࠪࡿࢂ࠭ᙡ")))
      parsed[bstack1ll11ll_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᙢ")] = bstack11ll11ll1ll_opy_[bstack1ll11ll_opy_ (u"ࠬࡪࡡࡵࡣࠪᙣ")][bstack1ll11ll_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᙤ")]
      os.environ[bstack1ll11ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᙥ")] = json.dumps(parsed)
      bstack1llll111_opy_.bstack1l111l11_opy_(bstack11ll11ll1ll_opy_[bstack1ll11ll_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᙦ")][bstack1ll11ll_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪᙧ")])
      bstack1llll111_opy_.bstack11ll11l1l11_opy_(bstack11ll11ll1ll_opy_[bstack1ll11ll_opy_ (u"ࠪࡨࡦࡺࡡࠨᙨ")][bstack1ll11ll_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ᙩ")])
      bstack1llll111_opy_.store()
      return bstack11ll11ll1ll_opy_[bstack1ll11ll_opy_ (u"ࠬࡪࡡࡵࡣࠪᙪ")][bstack1ll11ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࡚࡯࡬ࡧࡱࠫᙫ")], bstack11ll11ll1ll_opy_[bstack1ll11ll_opy_ (u"ࠧࡥࡣࡷࡥࠬᙬ")][bstack1ll11ll_opy_ (u"ࠨ࡫ࡧࠫ᙭")]
    else:
      logger.error(bstack1ll11ll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠻ࠢࠪ᙮") + bstack11ll11ll1ll_opy_[bstack1ll11ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᙯ")])
      if bstack11ll11ll1ll_opy_[bstack1ll11ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᙰ")] == bstack1ll11ll_opy_ (u"ࠬࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡰࡢࡵࡶࡩࡩ࠴ࠧᙱ"):
        for bstack11ll1l1l11l_opy_ in bstack11ll11ll1ll_opy_[bstack1ll11ll_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭ᙲ")]:
          logger.error(bstack11ll1l1l11l_opy_[bstack1ll11ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᙳ")])
      return None, None
  except Exception as error:
    logger.error(bstack1ll11ll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡶࡺࡴࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࠤᙴ") +  str(error))
    return None, None
def bstack11ll1l11111_opy_():
  if os.getenv(bstack1ll11ll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᙵ")) is None:
    return {
        bstack1ll11ll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᙶ"): bstack1ll11ll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᙷ"),
        bstack1ll11ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᙸ"): bstack1ll11ll_opy_ (u"࠭ࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡩࡣࡧࠤ࡫ࡧࡩ࡭ࡧࡧ࠲ࠬᙹ")
    }
  data = {bstack1ll11ll_opy_ (u"ࠧࡦࡰࡧࡘ࡮ࡳࡥࠨᙺ"): bstack11l1l1l1l1_opy_()}
  headers = {
      bstack1ll11ll_opy_ (u"ࠨࡃࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨᙻ"): bstack1ll11ll_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࠪᙼ") + os.getenv(bstack1ll11ll_opy_ (u"ࠥࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠣᙽ")),
      bstack1ll11ll_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪᙾ"): bstack1ll11ll_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨᙿ")
  }
  response = bstack1lllll1111_opy_(bstack1ll11ll_opy_ (u"࠭ࡐࡖࡖࠪ "), bstack11ll1l1l111_opy_ + bstack1ll11ll_opy_ (u"ࠧ࠰ࡶࡨࡷࡹࡥࡲࡶࡰࡶ࠳ࡸࡺ࡯ࡱࠩᚁ"), data, { bstack1ll11ll_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᚂ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1ll11ll_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡚ࠥࡥࡴࡶࠣࡖࡺࡴࠠ࡮ࡣࡵ࡯ࡪࡪࠠࡢࡵࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࡩࠦࡡࡵࠢࠥᚃ") + bstack111l1l11ll_opy_().isoformat() + bstack1ll11ll_opy_ (u"ࠪ࡞ࠬᚄ"))
      return {bstack1ll11ll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᚅ"): bstack1ll11ll_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ᚆ"), bstack1ll11ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᚇ"): bstack1ll11ll_opy_ (u"ࠧࠨᚈ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1ll11ll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡨࡵ࡭ࡱ࡮ࡨࡸ࡮ࡵ࡮ࠡࡱࡩࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡕࡧࡶࡸࠥࡘࡵ࡯࠼ࠣࠦᚉ") + str(error))
    return {
        bstack1ll11ll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᚊ"): bstack1ll11ll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᚋ"),
        bstack1ll11ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᚌ"): str(error)
    }
def bstack11ll1l11l1l_opy_(bstack11ll1l1111l_opy_):
    return re.match(bstack1ll11ll_opy_ (u"ࡷ࠭࡞࡝ࡦ࠮ࠬࡡ࠴࡜ࡥ࠭ࠬࡃࠩ࠭ᚍ"), bstack11ll1l1111l_opy_.strip()) is not None
def bstack11ll1l1l1_opy_(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack11ll1ll1ll1_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11ll1ll1ll1_opy_ = desired_capabilities
        else:
          bstack11ll1ll1ll1_opy_ = {}
        bstack1ll11llllll_opy_ = (bstack11ll1ll1ll1_opy_.get(bstack1ll11ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬᚎ"), bstack1ll11ll_opy_ (u"ࠧࠨᚏ")).lower() or caps.get(bstack1ll11ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧᚐ"), bstack1ll11ll_opy_ (u"ࠩࠪᚑ")).lower())
        if bstack1ll11llllll_opy_ == bstack1ll11ll_opy_ (u"ࠪ࡭ࡴࡹࠧᚒ"):
            return True
        if bstack1ll11llllll_opy_ == bstack1ll11ll_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࠬᚓ"):
            bstack1ll11ll11l1_opy_ = str(float(caps.get(bstack1ll11ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧᚔ")) or bstack11ll1ll1ll1_opy_.get(bstack1ll11ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᚕ"), {}).get(bstack1ll11ll_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪᚖ"),bstack1ll11ll_opy_ (u"ࠨࠩᚗ"))))
            if bstack1ll11llllll_opy_ == bstack1ll11ll_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࠪᚘ") and int(bstack1ll11ll11l1_opy_.split(bstack1ll11ll_opy_ (u"ࠪ࠲ࠬᚙ"))[0]) < float(bstack11ll11lll1l_opy_):
                logger.warning(str(bstack11ll11l111l_opy_))
                return False
            return True
        bstack1ll1l1111l1_opy_ = caps.get(bstack1ll11ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᚚ"), {}).get(bstack1ll11ll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩ᚛"), caps.get(bstack1ll11ll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭᚜"), bstack1ll11ll_opy_ (u"ࠧࠨ᚝")))
        if bstack1ll1l1111l1_opy_:
            logger.warning(bstack1ll11ll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡆࡨࡷࡰࡺ࡯ࡱࠢࡥࡶࡴࡽࡳࡦࡴࡶ࠲ࠧ᚞"))
            return False
        browser = caps.get(bstack1ll11ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ᚟"), bstack1ll11ll_opy_ (u"ࠪࠫᚠ")).lower() or bstack11ll1ll1ll1_opy_.get(bstack1ll11ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᚡ"), bstack1ll11ll_opy_ (u"ࠬ࠭ᚢ")).lower()
        if browser != bstack1ll11ll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ᚣ"):
            logger.warning(bstack1ll11ll_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥᚤ"))
            return False
        browser_version = caps.get(bstack1ll11ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᚥ")) or caps.get(bstack1ll11ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫᚦ")) or bstack11ll1ll1ll1_opy_.get(bstack1ll11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᚧ")) or bstack11ll1ll1ll1_opy_.get(bstack1ll11ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᚨ"), {}).get(bstack1ll11ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᚩ")) or bstack11ll1ll1ll1_opy_.get(bstack1ll11ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᚪ"), {}).get(bstack1ll11ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᚫ"))
        bstack1ll11lll11l_opy_ = bstack11ll111lll1_opy_.bstack1ll11l11111_opy_
        bstack11ll11ll1l1_opy_ = False
        if config is not None:
          bstack11ll11ll1l1_opy_ = bstack1ll11ll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬᚬ") in config and str(config[bstack1ll11ll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᚭ")]).lower() != bstack1ll11ll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩᚮ")
        if os.environ.get(bstack1ll11ll_opy_ (u"ࠫࡎ࡙࡟ࡏࡑࡑࡣࡇ࡙ࡔࡂࡅࡎࡣࡎࡔࡆࡓࡃࡢࡅ࠶࠷࡙ࡠࡕࡈࡗࡘࡏࡏࡏࠩᚯ"), bstack1ll11ll_opy_ (u"ࠬ࠭ᚰ")).lower() == bstack1ll11ll_opy_ (u"࠭ࡴࡳࡷࡨࠫᚱ") or bstack11ll11ll1l1_opy_:
          bstack1ll11lll11l_opy_ = bstack11ll111lll1_opy_.bstack1ll11l1llll_opy_
        if browser_version and browser_version != bstack1ll11ll_opy_ (u"ࠧ࡭ࡣࡷࡩࡸࡺࠧᚲ") and int(browser_version.split(bstack1ll11ll_opy_ (u"ࠨ࠰ࠪᚳ"))[0]) <= bstack1ll11lll11l_opy_:
          logger.warning(bstack1lll111ll1l_opy_ (u"ࠩࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࠣࡺࡪࡸࡳࡪࡱࡱࠤ࡬ࡸࡥࡢࡶࡨࡶࠥࡺࡨࡢࡰࠣࡿࡲ࡯࡮ࡠࡣ࠴࠵ࡾࡥࡳࡶࡲࡳࡳࡷࡺࡥࡥࡡࡦ࡬ࡷࡵ࡭ࡦࡡࡹࡩࡷࡹࡩࡰࡰࢀ࠲ࠬᚴ"))
          return False
        if not options:
          bstack1ll11lll111_opy_ = caps.get(bstack1ll11ll_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᚵ")) or bstack11ll1ll1ll1_opy_.get(bstack1ll11ll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᚶ"), {})
          if bstack1ll11ll_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴࠩᚷ") in bstack1ll11lll111_opy_.get(bstack1ll11ll_opy_ (u"࠭ࡡࡳࡩࡶࠫᚸ"), []):
              logger.warning(bstack1ll11ll_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡱࡳࡹࠦࡲࡶࡰࠣࡳࡳࠦ࡬ࡦࡩࡤࡧࡾࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠠࡔࡹ࡬ࡸࡨ࡮ࠠࡵࡱࠣࡲࡪࡽࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫ࠠࡰࡴࠣࡥࡻࡵࡩࡥࠢࡸࡷ࡮ࡴࡧࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠤᚹ"))
              return False
        return True
    except Exception as error:
        logger.debug(bstack1ll11ll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡣ࡯࡭ࡩࡧࡴࡦࠢࡤ࠵࠶ࡿࠠࡴࡷࡳࡴࡴࡸࡴࠡ࠼ࠥᚺ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1lll11l1111_opy_ = config.get(bstack1ll11ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᚻ"), {})
    bstack1lll11l1111_opy_[bstack1ll11ll_opy_ (u"ࠪࡥࡺࡺࡨࡕࡱ࡮ࡩࡳ࠭ᚼ")] = os.getenv(bstack1ll11ll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᚽ"))
    bstack11ll11ll11l_opy_ = json.loads(os.getenv(bstack1ll11ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᚾ"), bstack1ll11ll_opy_ (u"࠭ࡻࡾࠩᚿ"))).get(bstack1ll11ll_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᛀ"))
    if not config[bstack1ll11ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪᛁ")].get(bstack1ll11ll_opy_ (u"ࠤࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠣᛂ")):
      if bstack1ll11ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᛃ") in caps:
        caps[bstack1ll11ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᛄ")][bstack1ll11ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᛅ")] = bstack1lll11l1111_opy_
        caps[bstack1ll11ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᛆ")][bstack1ll11ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᛇ")][bstack1ll11ll_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᛈ")] = bstack11ll11ll11l_opy_
      else:
        caps[bstack1ll11ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᛉ")] = bstack1lll11l1111_opy_
        caps[bstack1ll11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᛊ")][bstack1ll11ll_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᛋ")] = bstack11ll11ll11l_opy_
  except Exception as error:
    logger.debug(bstack1ll11ll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ࠲ࠥࡋࡲࡳࡱࡵ࠾ࠥࠨᛌ") +  str(error))
def bstack111ll1111_opy_(driver, bstack11ll1l1llll_opy_):
  try:
    setattr(driver, bstack1ll11ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭ᛍ"), True)
    session = driver.session_id
    if session:
      bstack11ll11l11l1_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11ll11l11l1_opy_ = False
      bstack11ll11l11l1_opy_ = url.scheme in [bstack1ll11ll_opy_ (u"ࠢࡩࡶࡷࡴࠧᛎ"), bstack1ll11ll_opy_ (u"ࠣࡪࡷࡸࡵࡹࠢᛏ")]
      if bstack11ll11l11l1_opy_:
        if bstack11ll1l1llll_opy_:
          logger.info(bstack1ll11ll_opy_ (u"ࠤࡖࡩࡹࡻࡰࠡࡨࡲࡶࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡨࡢࡵࠣࡷࡹࡧࡲࡵࡧࡧ࠲ࠥࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡧ࡫ࡧࡪࡰࠣࡱࡴࡳࡥ࡯ࡶࡤࡶ࡮ࡲࡹ࠯ࠤᛐ"))
      return bstack11ll1l1llll_opy_
  except Exception as e:
    logger.error(bstack1ll11ll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡦࡸࡴࡪࡰࡪࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨ࠾ࠥࠨᛑ") + str(e))
    return False
def bstack1l11ll1l11_opy_(driver, name, path):
  try:
    bstack1ll1111llll_opy_ = {
        bstack1ll11ll_opy_ (u"ࠫࡹ࡮ࡔࡦࡵࡷࡖࡺࡴࡕࡶ࡫ࡧࠫᛒ"): threading.current_thread().current_test_uuid,
        bstack1ll11ll_opy_ (u"ࠬࡺࡨࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪᛓ"): os.environ.get(bstack1ll11ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᛔ"), bstack1ll11ll_opy_ (u"ࠧࠨᛕ")),
        bstack1ll11ll_opy_ (u"ࠨࡶ࡫ࡎࡼࡺࡔࡰ࡭ࡨࡲࠬᛖ"): os.environ.get(bstack1ll11ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ᛗ"), bstack1ll11ll_opy_ (u"ࠪࠫᛘ"))
    }
    bstack1ll111ll1ll_opy_ = bstack1l1ll11l1l_opy_.bstack1ll111l1111_opy_(EVENTS.bstack11ll111l11_opy_.value)
    logger.debug(bstack1ll11ll_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡢࡦࡨࡲࡶࡪࠦࡳࡢࡸ࡬ࡲ࡬ࠦࡲࡦࡵࡸࡰࡹࡹࠧᛙ"))
    try:
      if (bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠬ࡯ࡳࡂࡲࡳࡅ࠶࠷ࡹࡕࡧࡶࡸࠬᛚ"), None) and bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᛛ"), None)):
        scripts = {bstack1ll11ll_opy_ (u"ࠧࡴࡥࡤࡲࠬᛜ"): bstack1llll111_opy_.perform_scan}
        bstack11ll11l1lll_opy_ = json.loads(scripts[bstack1ll11ll_opy_ (u"ࠣࡵࡦࡥࡳࠨᛝ")].replace(bstack1ll11ll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠧᛞ"), bstack1ll11ll_opy_ (u"ࠥࠦᛟ")))
        bstack11ll11l1lll_opy_[bstack1ll11ll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᛠ")][bstack1ll11ll_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬᛡ")] = None
        scripts[bstack1ll11ll_opy_ (u"ࠨࡳࡤࡣࡱࠦᛢ")] = bstack1ll11ll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࠥᛣ") + json.dumps(bstack11ll11l1lll_opy_)
        bstack1llll111_opy_.bstack1l111l11_opy_(scripts)
        bstack1llll111_opy_.store()
        logger.debug(driver.execute_script(bstack1llll111_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1llll111_opy_.perform_scan, {bstack1ll11ll_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠣᛤ"): name}))
      bstack1l1ll11l1l_opy_.end(EVENTS.bstack11ll111l11_opy_.value, bstack1ll111ll1ll_opy_ + bstack1ll11ll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᛥ"), bstack1ll111ll1ll_opy_ + bstack1ll11ll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᛦ"), True, None)
    except Exception as error:
      bstack1l1ll11l1l_opy_.end(EVENTS.bstack11ll111l11_opy_.value, bstack1ll111ll1ll_opy_ + bstack1ll11ll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᛧ"), bstack1ll111ll1ll_opy_ + bstack1ll11ll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᛨ"), False, str(error))
    bstack1ll111ll1ll_opy_ = bstack1l1ll11l1l_opy_.bstack11ll1l111ll_opy_(EVENTS.bstack1ll111lllll_opy_.value)
    bstack1l1ll11l1l_opy_.mark(bstack1ll111ll1ll_opy_ + bstack1ll11ll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᛩ"))
    try:
      if (bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧᛪ"), None) and bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ᛫"), None)):
        scripts = {bstack1ll11ll_opy_ (u"ࠩࡶࡧࡦࡴࠧ᛬"): bstack1llll111_opy_.perform_scan}
        bstack11ll11l1lll_opy_ = json.loads(scripts[bstack1ll11ll_opy_ (u"ࠥࡷࡨࡧ࡮ࠣ᛭")].replace(bstack1ll11ll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࠢᛮ"), bstack1ll11ll_opy_ (u"ࠧࠨᛯ")))
        bstack11ll11l1lll_opy_[bstack1ll11ll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᛰ")][bstack1ll11ll_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪࠧᛱ")] = None
        scripts[bstack1ll11ll_opy_ (u"ࠣࡵࡦࡥࡳࠨᛲ")] = bstack1ll11ll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠧᛳ") + json.dumps(bstack11ll11l1lll_opy_)
        bstack1llll111_opy_.bstack1l111l11_opy_(scripts)
        bstack1llll111_opy_.store()
        logger.debug(driver.execute_script(bstack1llll111_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1llll111_opy_.bstack11ll1l1lll1_opy_, bstack1ll1111llll_opy_))
      bstack1l1ll11l1l_opy_.end(bstack1ll111ll1ll_opy_, bstack1ll111ll1ll_opy_ + bstack1ll11ll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᛴ"), bstack1ll111ll1ll_opy_ + bstack1ll11ll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᛵ"),True, None)
    except Exception as error:
      bstack1l1ll11l1l_opy_.end(bstack1ll111ll1ll_opy_, bstack1ll111ll1ll_opy_ + bstack1ll11ll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᛶ"), bstack1ll111ll1ll_opy_ + bstack1ll11ll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᛷ"),False, str(error))
    logger.info(bstack1ll11ll_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠥᛸ"))
  except Exception as bstack1ll11ll1lll_opy_:
    logger.error(bstack1ll11ll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡦࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥ࠻ࠢࠥ᛹") + str(path) + bstack1ll11ll_opy_ (u"ࠤࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠦ᛺") + str(bstack1ll11ll1lll_opy_))
def bstack11ll11lllll_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack1ll11ll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤ᛻")) and str(caps.get(bstack1ll11ll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥ᛼"))).lower() == bstack1ll11ll_opy_ (u"ࠧࡧ࡮ࡥࡴࡲ࡭ࡩࠨ᛽"):
        bstack1ll11ll11l1_opy_ = caps.get(bstack1ll11ll_opy_ (u"ࠨࡡࡱࡲ࡬ࡹࡲࡀࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣ᛾")) or caps.get(bstack1ll11ll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤ᛿"))
        if bstack1ll11ll11l1_opy_ and int(str(bstack1ll11ll11l1_opy_)) < bstack11ll11lll1l_opy_:
            return False
    return True
def bstack1llllll1ll_opy_(config):
  if bstack1ll11ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᜀ") in config:
        return config[bstack1ll11ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᜁ")]
  for platform in config.get(bstack1ll11ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᜂ"), []):
      if bstack1ll11ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᜃ") in platform:
          return platform[bstack1ll11ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᜄ")]
  return None
def bstack1l111l1l1_opy_(bstack11llllllll_opy_):
  try:
    browser_name = bstack11llllllll_opy_[bstack1ll11ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟࡯ࡣࡰࡩࠬᜅ")]
    browser_version = bstack11llllllll_opy_[bstack1ll11ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᜆ")]
    chrome_options = bstack11llllllll_opy_[bstack1ll11ll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡠࡱࡳࡸ࡮ࡵ࡮ࡴࠩᜇ")]
    try:
        bstack11ll11l11ll_opy_ = int(browser_version.split(bstack1ll11ll_opy_ (u"ࠩ࠱ࠫᜈ"))[0])
    except ValueError as e:
        logger.error(bstack1ll11ll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡥࡲࡲࡻ࡫ࡲࡵ࡫ࡱ࡫ࠥࡨࡲࡰࡹࡶࡩࡷࠦࡶࡦࡴࡶ࡭ࡴࡴࠢᜉ") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack1ll11ll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫᜊ")):
        logger.warning(bstack1ll11ll_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣᜋ"))
        return False
    if bstack11ll11l11ll_opy_ < bstack11ll111lll1_opy_.bstack1ll11l1llll_opy_:
        logger.warning(bstack1lll111ll1l_opy_ (u"࠭ࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡶࡪࡷࡵࡪࡴࡨࡷࠥࡉࡨࡳࡱࡰࡩࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡻࡄࡑࡑࡗ࡙ࡇࡎࡕࡕ࠱ࡑࡎࡔࡉࡎࡗࡐࡣࡓࡕࡎࡠࡄࡖࡘࡆࡉࡋࡠࡋࡑࡊࡗࡇ࡟ࡂ࠳࠴࡝ࡤ࡙ࡕࡑࡒࡒࡖ࡙ࡋࡄࡠࡅࡋࡖࡔࡓࡅࡠࡘࡈࡖࡘࡏࡏࡏࡿࠣࡳࡷࠦࡨࡪࡩ࡫ࡩࡷ࠴ࠧᜌ"))
        return False
    if chrome_options and any(bstack1ll11ll_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࠫᜍ") in value for value in chrome_options.values() if isinstance(value, str)):
        logger.warning(bstack1ll11ll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡲࡴࡺࠠࡳࡷࡱࠤࡴࡴࠠ࡭ࡧࡪࡥࡨࡿࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠡࡕࡺ࡭ࡹࡩࡨࠡࡶࡲࠤࡳ࡫ࡷࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥࠡࡱࡵࠤࡦࡼ࡯ࡪࡦࠣࡹࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠥᜎ"))
        return False
    return True
  except Exception as e:
    logger.error(bstack1ll11ll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡨ࡮ࡥࡤ࡭࡬ࡲ࡬ࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡵࡸࡴࡵࡵࡲࡵࠢࡩࡳࡷࠦ࡬ࡰࡥࡤࡰࠥࡉࡨࡳࡱࡰࡩ࠿ࠦࠢᜏ") + str(e))
    return False
def bstack11ll111ll_opy_(bstack1l111lll1_opy_, config):
    try:
      bstack1ll11l1lll1_opy_ = bstack1ll11ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᜐ") in config and config[bstack1ll11ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᜑ")] == True
      bstack11ll11ll1l1_opy_ = bstack1ll11ll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩᜒ") in config and str(config[bstack1ll11ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪᜓ")]).lower() != bstack1ll11ll_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ᜔࠭")
      if not (bstack1ll11l1lll1_opy_ and (not bstack11l1lll1ll_opy_(config) or bstack11ll11ll1l1_opy_)):
        return bstack1l111lll1_opy_
      bstack11ll11l1ll1_opy_ = bstack1llll111_opy_.bstack11ll1l11l11_opy_
      if bstack11ll11l1ll1_opy_ is None:
        logger.debug(bstack1ll11ll_opy_ (u"ࠣࡉࡲࡳ࡬ࡲࡥࠡࡥ࡫ࡶࡴࡳࡥࠡࡱࡳࡸ࡮ࡵ࡮ࡴࠢࡤࡶࡪࠦࡎࡰࡰࡨ᜕ࠦ"))
        return bstack1l111lll1_opy_
      bstack11ll1ll11ll_opy_ = int(str(bstack11ll11l1111_opy_()).split(bstack1ll11ll_opy_ (u"ࠩ࠱ࠫ᜖"))[0])
      logger.debug(bstack1ll11ll_opy_ (u"ࠥࡗࡪࡲࡥ࡯࡫ࡸࡱࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡤࡦࡶࡨࡧࡹ࡫ࡤ࠻ࠢࠥ᜗") + str(bstack11ll1ll11ll_opy_) + bstack1ll11ll_opy_ (u"ࠦࠧ᜘"))
      if bstack11ll1ll11ll_opy_ == 3 and isinstance(bstack1l111lll1_opy_, dict) and bstack1ll11ll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬ᜙") in bstack1l111lll1_opy_ and bstack11ll11l1ll1_opy_ is not None:
        if bstack1ll11ll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ᜚") not in bstack1l111lll1_opy_[bstack1ll11ll_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ᜛")]:
          bstack1l111lll1_opy_[bstack1ll11ll_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ᜜")][bstack1ll11ll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᜝")] = {}
        if bstack1ll11ll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ᜞") in bstack11ll11l1ll1_opy_:
          if bstack1ll11ll_opy_ (u"ࠫࡦࡸࡧࡴࠩᜟ") not in bstack1l111lll1_opy_[bstack1ll11ll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᜠ")][bstack1ll11ll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᜡ")]:
            bstack1l111lll1_opy_[bstack1ll11ll_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᜢ")][bstack1ll11ll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᜣ")][bstack1ll11ll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᜤ")] = []
          for arg in bstack11ll11l1ll1_opy_[bstack1ll11ll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᜥ")]:
            if arg not in bstack1l111lll1_opy_[bstack1ll11ll_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᜦ")][bstack1ll11ll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᜧ")][bstack1ll11ll_opy_ (u"࠭ࡡࡳࡩࡶࠫᜨ")]:
              bstack1l111lll1_opy_[bstack1ll11ll_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᜩ")][bstack1ll11ll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᜪ")][bstack1ll11ll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᜫ")].append(arg)
        if bstack1ll11ll_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᜬ") in bstack11ll11l1ll1_opy_:
          if bstack1ll11ll_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨᜭ") not in bstack1l111lll1_opy_[bstack1ll11ll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᜮ")][bstack1ll11ll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᜯ")]:
            bstack1l111lll1_opy_[bstack1ll11ll_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᜰ")][bstack1ll11ll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᜱ")][bstack1ll11ll_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᜲ")] = []
          for ext in bstack11ll11l1ll1_opy_[bstack1ll11ll_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᜳ")]:
            if ext not in bstack1l111lll1_opy_[bstack1ll11ll_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ᜴ࠫ")][bstack1ll11ll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ᜵")][bstack1ll11ll_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪ᜶")]:
              bstack1l111lll1_opy_[bstack1ll11ll_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ᜷")][bstack1ll11ll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᜸")][bstack1ll11ll_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭᜹")].append(ext)
        if bstack1ll11ll_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩ᜺") in bstack11ll11l1ll1_opy_:
          if bstack1ll11ll_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪ᜻") not in bstack1l111lll1_opy_[bstack1ll11ll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬ᜼")][bstack1ll11ll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ᜽")]:
            bstack1l111lll1_opy_[bstack1ll11ll_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ᜾")][bstack1ll11ll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᜿")][bstack1ll11ll_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᝀ")] = {}
          bstack11ll1ll1111_opy_(bstack1l111lll1_opy_[bstack1ll11ll_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᝁ")][bstack1ll11ll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᝂ")][bstack1ll11ll_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫᝃ")],
                    bstack11ll11l1ll1_opy_[bstack1ll11ll_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬᝄ")])
        os.environ[bstack1ll11ll_opy_ (u"ࠧࡊࡕࡢࡒࡔࡔ࡟ࡃࡕࡗࡅࡈࡑ࡟ࡊࡐࡉࡖࡆࡥࡁ࠲࠳࡜ࡣࡘࡋࡓࡔࡋࡒࡒࠬᝅ")] = bstack1ll11ll_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᝆ")
        return bstack1l111lll1_opy_
      else:
        chrome_options = None
        if isinstance(bstack1l111lll1_opy_, ChromeOptions):
          chrome_options = bstack1l111lll1_opy_
        elif isinstance(bstack1l111lll1_opy_, dict):
          for value in bstack1l111lll1_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack1l111lll1_opy_, dict):
            bstack1l111lll1_opy_[bstack1ll11ll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪᝇ")] = chrome_options
          else:
            bstack1l111lll1_opy_ = chrome_options
        if bstack11ll11l1ll1_opy_ is not None:
          if bstack1ll11ll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᝈ") in bstack11ll11l1ll1_opy_:
                bstack11ll1l1ll11_opy_ = chrome_options.arguments or []
                new_args = bstack11ll11l1ll1_opy_[bstack1ll11ll_opy_ (u"ࠫࡦࡸࡧࡴࠩᝉ")]
                for arg in new_args:
                    if arg not in bstack11ll1l1ll11_opy_:
                        chrome_options.add_argument(arg)
          if bstack1ll11ll_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᝊ") in bstack11ll11l1ll1_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack1ll11ll_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᝋ"), [])
                bstack11ll1l1ll1l_opy_ = bstack11ll11l1ll1_opy_[bstack1ll11ll_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᝌ")]
                for extension in bstack11ll1l1ll1l_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack1ll11ll_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᝍ") in bstack11ll11l1ll1_opy_:
                bstack11ll1ll111l_opy_ = chrome_options.experimental_options.get(bstack1ll11ll_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᝎ"), {})
                bstack11ll11lll11_opy_ = bstack11ll11l1ll1_opy_[bstack1ll11ll_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᝏ")]
                bstack11ll1ll1111_opy_(bstack11ll1ll111l_opy_, bstack11ll11lll11_opy_)
                chrome_options.add_experimental_option(bstack1ll11ll_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪᝐ"), bstack11ll1ll111l_opy_)
        os.environ[bstack1ll11ll_opy_ (u"ࠬࡏࡓࡠࡐࡒࡒࡤࡈࡓࡕࡃࡆࡏࡤࡏࡎࡇࡔࡄࡣࡆ࠷࠱࡚ࡡࡖࡉࡘ࡙ࡉࡐࡐࠪᝑ")] = bstack1ll11ll_opy_ (u"࠭ࡴࡳࡷࡨࠫᝒ")
        return bstack1l111lll1_opy_
    except Exception as e:
      logger.error(bstack1ll11ll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡧࡤࡥ࡫ࡱ࡫ࠥࡴ࡯࡯࠯ࡅࡗࠥ࡯࡮ࡧࡴࡤࠤࡦ࠷࠱ࡺࠢࡦ࡬ࡷࡵ࡭ࡦࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࠧᝓ") + str(e))
      return bstack1l111lll1_opy_