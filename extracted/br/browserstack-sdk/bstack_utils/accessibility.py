# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack11ll1l111ll_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack11ll11ll1l1_opy_ as bstack11ll1ll1lll_opy_, EVENTS
from bstack_utils.bstack1ll1ll1ll1_opy_ import bstack1ll1ll1ll1_opy_
from bstack_utils.helper import bstack1ll111ll1l_opy_, bstack1111l1lll1_opy_, bstack111l1l11_opy_, bstack11ll1ll11l1_opy_, \
  bstack11lll11111l_opy_, bstack1ll111ll_opy_, get_host_info, bstack11ll1l1lll1_opy_, bstack1ll111l111_opy_, error_handler, bstack11ll11ll11l_opy_, bstack11ll11lllll_opy_, bstack1l11l1lll_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack11l1111l1_opy_ import get_logger
from bstack_utils.bstack1lllll1ll_opy_ import bstack1lll11111ll_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
logger = get_logger(__name__)
bstack1lllll1ll_opy_ = bstack1lll11111ll_opy_()
@error_handler(class_method=False)
def _11ll1l1111l_opy_(driver, bstack1111l1111l_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1111l1l_opy_ (u"ࠩࡲࡷࡤࡴࡡ࡮ࡧࠪᘚ"): caps.get(bstack1111l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩᘛ"), None),
        bstack1111l1l_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᘜ"): bstack1111l1111l_opy_.get(bstack1111l1l_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨᘝ"), None),
        bstack1111l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟࡯ࡣࡰࡩࠬᘞ"): caps.get(bstack1111l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᘟ"), None),
        bstack1111l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪᘠ"): caps.get(bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᘡ"), None)
    }
  except Exception as error:
    logger.debug(bstack1111l1l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡦࡶࡤ࡭ࡱࡹࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵࠤ࠿ࠦࠧᘢ") + str(error))
  return response
def on():
    if os.environ.get(bstack1111l1l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᘣ"), None) is None or os.environ[bstack1111l1l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᘤ")] == bstack1111l1l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᘥ"):
        return False
    return True
def bstack11l1l11ll_opy_(config):
  return config.get(bstack1111l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᘦ"), False) or any([p.get(bstack1111l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᘧ"), False) == True for p in config.get(bstack1111l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᘨ"), [])])
def bstack1llll1l1l_opy_(config, bstack11lll11l_opy_):
  try:
    bstack11ll1ll1l11_opy_ = config.get(bstack1111l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᘩ"), False)
    if int(bstack11lll11l_opy_) < len(config.get(bstack1111l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᘪ"), [])) and config[bstack1111l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᘫ")][bstack11lll11l_opy_]:
      bstack11ll1llll11_opy_ = config[bstack1111l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᘬ")][bstack11lll11l_opy_].get(bstack1111l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᘭ"), None)
    else:
      bstack11ll1llll11_opy_ = config.get(bstack1111l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᘮ"), None)
    if bstack11ll1llll11_opy_ != None:
      bstack11ll1ll1l11_opy_ = bstack11ll1llll11_opy_
    bstack11ll1lll11l_opy_ = os.getenv(bstack1111l1l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᘯ")) is not None and len(os.getenv(bstack1111l1l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᘰ"))) > 0 and os.getenv(bstack1111l1l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᘱ")) != bstack1111l1l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪᘲ")
    return bstack11ll1ll1l11_opy_ and bstack11ll1lll11l_opy_
  except Exception as error:
    logger.debug(bstack1111l1l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡥࡳ࡫ࡩࡽ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴࠣ࠾ࠥ࠭ᘳ") + str(error))
  return False
def bstack11l111ll_opy_(test_tags):
  bstack1ll11ll1l1l_opy_ = os.getenv(bstack1111l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᘴ"))
  if bstack1ll11ll1l1l_opy_ is None:
    return True
  bstack1ll11ll1l1l_opy_ = json.loads(bstack1ll11ll1l1l_opy_)
  try:
    include_tags = bstack1ll11ll1l1l_opy_[bstack1111l1l_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᘵ")] if bstack1111l1l_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᘶ") in bstack1ll11ll1l1l_opy_ and isinstance(bstack1ll11ll1l1l_opy_[bstack1111l1l_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᘷ")], list) else []
    exclude_tags = bstack1ll11ll1l1l_opy_[bstack1111l1l_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᘸ")] if bstack1111l1l_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᘹ") in bstack1ll11ll1l1l_opy_ and isinstance(bstack1ll11ll1l1l_opy_[bstack1111l1l_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᘺ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1111l1l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡼࡡ࡭࡫ࡧࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡧࡦࡴ࡮ࡪࡰࡪ࠲ࠥࡋࡲࡳࡱࡵࠤ࠿ࠦࠢᘻ") + str(error))
  return False
def bstack11ll1l11lll_opy_(config, bstack11ll11llll1_opy_, bstack11ll1lllll1_opy_, bstack11ll11lll1l_opy_):
  bstack11ll1lll111_opy_ = bstack11ll1ll11l1_opy_(config)
  bstack11ll1ll11ll_opy_ = bstack11lll11111l_opy_(config)
  if bstack11ll1lll111_opy_ is None or bstack11ll1ll11ll_opy_ is None:
    logger.error(bstack1111l1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡶࡺࡴࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࡏ࡬ࡷࡸ࡯࡮ࡨࠢࡤࡹࡹ࡮ࡥ࡯ࡶ࡬ࡧࡦࡺࡩࡰࡰࠣࡸࡴࡱࡥ࡯ࠩᘼ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1111l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᘽ"), bstack1111l1l_opy_ (u"ࠪࡿࢂ࠭ᘾ")))
    data = {
        bstack1111l1l_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᘿ"): config[bstack1111l1l_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᙀ")],
        bstack1111l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᙁ"): config.get(bstack1111l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᙂ"), os.path.basename(os.getcwd())),
        bstack1111l1l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡔࡪ࡯ࡨࠫᙃ"): bstack1ll111ll1l_opy_(),
        bstack1111l1l_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧᙄ"): config.get(bstack1111l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ᙅ"), bstack1111l1l_opy_ (u"ࠫࠬᙆ")),
        bstack1111l1l_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬᙇ"): {
            bstack1111l1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡐࡤࡱࡪ࠭ᙈ"): bstack11ll11llll1_opy_,
            bstack1111l1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪᙉ"): bstack11ll1lllll1_opy_,
            bstack1111l1l_opy_ (u"ࠨࡵࡧ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬᙊ"): __version__,
            bstack1111l1l_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫᙋ"): bstack1111l1l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪᙌ"),
            bstack1111l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᙍ"): bstack1111l1l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧᙎ"),
            bstack1111l1l_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᙏ"): bstack11ll11lll1l_opy_
        },
        bstack1111l1l_opy_ (u"ࠧࡴࡧࡷࡸ࡮ࡴࡧࡴࠩᙐ"): settings,
        bstack1111l1l_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࡅࡲࡲࡹࡸ࡯࡭ࠩᙑ"): bstack11ll1l1lll1_opy_(),
        bstack1111l1l_opy_ (u"ࠩࡦ࡭ࡎࡴࡦࡰࠩᙒ"): bstack1ll111ll_opy_(),
        bstack1111l1l_opy_ (u"ࠪ࡬ࡴࡹࡴࡊࡰࡩࡳࠬᙓ"): get_host_info(),
        bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᙔ"): bstack111l1l11_opy_(config)
    }
    headers = {
        bstack1111l1l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫᙕ"): bstack1111l1l_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩᙖ"),
    }
    config = {
        bstack1111l1l_opy_ (u"ࠧࡢࡷࡷ࡬ࠬᙗ"): (bstack11ll1lll111_opy_, bstack11ll1ll11ll_opy_),
        bstack1111l1l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᙘ"): headers
    }
    response = bstack1ll111l111_opy_(bstack1111l1l_opy_ (u"ࠩࡓࡓࡘ࡚ࠧᙙ"), bstack11ll1ll1lll_opy_ + bstack1111l1l_opy_ (u"ࠪ࠳ࡻ࠸࠯ࡵࡧࡶࡸࡤࡸࡵ࡯ࡵࠪᙚ"), data, config)
    bstack11lll1111ll_opy_ = response.json()
    if bstack11lll1111ll_opy_[bstack1111l1l_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬᙛ")]:
      parsed = json.loads(os.getenv(bstack1111l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᙜ"), bstack1111l1l_opy_ (u"࠭ࡻࡾࠩᙝ")))
      parsed[bstack1111l1l_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᙞ")] = bstack11lll1111ll_opy_[bstack1111l1l_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᙟ")][bstack1111l1l_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᙠ")]
      os.environ[bstack1111l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᙡ")] = json.dumps(parsed)
      bstack1ll1ll1ll1_opy_.bstack1l11l1ll_opy_(bstack11lll1111ll_opy_[bstack1111l1l_opy_ (u"ࠫࡩࡧࡴࡢࠩᙢ")][bstack1111l1l_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭ᙣ")])
      bstack1ll1ll1ll1_opy_.bstack11ll1l1l11l_opy_(bstack11lll1111ll_opy_[bstack1111l1l_opy_ (u"࠭ࡤࡢࡶࡤࠫᙤ")][bstack1111l1l_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩᙥ")])
      bstack1ll1ll1ll1_opy_.store()
      return bstack11lll1111ll_opy_[bstack1111l1l_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᙦ")][bstack1111l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡖࡲ࡯ࡪࡴࠧᙧ")], bstack11lll1111ll_opy_[bstack1111l1l_opy_ (u"ࠪࡨࡦࡺࡡࠨᙨ")][bstack1111l1l_opy_ (u"ࠫ࡮ࡪࠧᙩ")]
    else:
      logger.error(bstack1111l1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥ࠭ᙪ") + bstack11lll1111ll_opy_[bstack1111l1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᙫ")])
      if bstack11lll1111ll_opy_[bstack1111l1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᙬ")] == bstack1111l1l_opy_ (u"ࠨࡋࡱࡺࡦࡲࡩࡥࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡳࡥࡸࡹࡥࡥ࠰ࠪ᙭"):
        for bstack11ll1llll1l_opy_ in bstack11lll1111ll_opy_[bstack1111l1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩ᙮")]:
          logger.error(bstack11ll1llll1l_opy_[bstack1111l1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᙯ")])
      return None, None
  except Exception as error:
    logger.error(bstack1111l1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡲࡶࡰࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࠧᙰ") +  str(error))
    return None, None
def bstack11ll1l1l1l1_opy_():
  if os.getenv(bstack1111l1l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᙱ")) is None:
    return {
        bstack1111l1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᙲ"): bstack1111l1l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᙳ"),
        bstack1111l1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᙴ"): bstack1111l1l_opy_ (u"ࠩࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣ࡬ࡦࡪࠠࡧࡣ࡬ࡰࡪࡪ࠮ࠨᙵ")
    }
  data = {bstack1111l1l_opy_ (u"ࠪࡩࡳࡪࡔࡪ࡯ࡨࠫᙶ"): bstack1ll111ll1l_opy_()}
  headers = {
      bstack1111l1l_opy_ (u"ࠫࡆࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫᙷ"): bstack1111l1l_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥ࠭ᙸ") + os.getenv(bstack1111l1l_opy_ (u"ࠨࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠦᙹ")),
      bstack1111l1l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ᙺ"): bstack1111l1l_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫᙻ")
  }
  response = bstack1ll111l111_opy_(bstack1111l1l_opy_ (u"ࠩࡓ࡙࡙࠭ᙼ"), bstack11ll1ll1lll_opy_ + bstack1111l1l_opy_ (u"ࠪ࠳ࡹ࡫ࡳࡵࡡࡵࡹࡳࡹ࠯ࡴࡶࡲࡴࠬᙽ"), data, { bstack1111l1l_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᙾ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1111l1l_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡖࡨࡷࡹࠦࡒࡶࡰࠣࡱࡦࡸ࡫ࡦࡦࠣࡥࡸࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠢࡤࡸࠥࠨᙿ") + bstack1111l1lll1_opy_().isoformat() + bstack1111l1l_opy_ (u"࡚࠭ࠨ "))
      return {bstack1111l1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᚁ"): bstack1111l1l_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩᚂ"), bstack1111l1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᚃ"): bstack1111l1l_opy_ (u"ࠪࠫᚄ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1111l1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡤࡱࡰࡴࡱ࡫ࡴࡪࡱࡱࠤࡴ࡬ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡘࡪࡹࡴࠡࡔࡸࡲ࠿ࠦࠢᚅ") + str(error))
    return {
        bstack1111l1l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᚆ"): bstack1111l1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᚇ"),
        bstack1111l1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᚈ"): str(error)
    }
def bstack11lll1111l1_opy_(bstack11ll1ll1ll1_opy_):
    return re.match(bstack1111l1l_opy_ (u"ࡳࠩࡡࡠࡩ࠱ࠨ࡝࠰࡟ࡨ࠰࠯࠿ࠥࠩᚉ"), bstack11ll1ll1ll1_opy_.strip()) is not None
def bstack1l1lll1lll_opy_(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack11lll111111_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11lll111111_opy_ = desired_capabilities
        else:
          bstack11lll111111_opy_ = {}
        bstack1ll11l1l1ll_opy_ = (bstack11lll111111_opy_.get(bstack1111l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨᚊ"), bstack1111l1l_opy_ (u"ࠪࠫᚋ")).lower() or caps.get(bstack1111l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪᚌ"), bstack1111l1l_opy_ (u"ࠬ࠭ᚍ")).lower())
        if bstack1ll11l1l1ll_opy_ == bstack1111l1l_opy_ (u"࠭ࡩࡰࡵࠪᚎ"):
            return True
        if bstack1ll11l1l1ll_opy_ == bstack1111l1l_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࠨᚏ"):
            bstack1ll11l1l111_opy_ = str(float(caps.get(bstack1111l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪᚐ")) or bstack11lll111111_opy_.get(bstack1111l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᚑ"), {}).get(bstack1111l1l_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᚒ"),bstack1111l1l_opy_ (u"ࠫࠬᚓ"))))
            if bstack1ll11l1l1ll_opy_ == bstack1111l1l_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩ࠭ᚔ") and int(bstack1ll11l1l111_opy_.split(bstack1111l1l_opy_ (u"࠭࠮ࠨᚕ"))[0]) < float(bstack11ll1l1ll1l_opy_):
                logger.warning(str(bstack11ll11ll1ll_opy_))
                return False
            return True
        bstack1ll11l1l1l1_opy_ = caps.get(bstack1111l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᚖ"), {}).get(bstack1111l1l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬᚗ"), caps.get(bstack1111l1l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩᚘ"), bstack1111l1l_opy_ (u"ࠪࠫᚙ")))
        if bstack1ll11l1l1l1_opy_:
            logger.warning(bstack1111l1l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡉ࡫ࡳ࡬ࡶࡲࡴࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣᚚ"))
            return False
        browser = caps.get(bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ᚛"), bstack1111l1l_opy_ (u"࠭ࠧ᚜")).lower() or bstack11lll111111_opy_.get(bstack1111l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ᚝"), bstack1111l1l_opy_ (u"ࠨࠩ᚞")).lower()
        if browser != bstack1111l1l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩ᚟"):
            logger.warning(bstack1111l1l_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᚠ"))
            return False
        browser_version = caps.get(bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᚡ")) or caps.get(bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᚢ")) or bstack11lll111111_opy_.get(bstack1111l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᚣ")) or bstack11lll111111_opy_.get(bstack1111l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᚤ"), {}).get(bstack1111l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᚥ")) or bstack11lll111111_opy_.get(bstack1111l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᚦ"), {}).get(bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᚧ"))
        bstack1ll1111ll11_opy_ = bstack11ll1l111ll_opy_.bstack1ll1l111l11_opy_
        bstack11ll1lll1l1_opy_ = False
        if config is not None:
          bstack11ll1lll1l1_opy_ = bstack1111l1l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨᚨ") in config and str(config[bstack1111l1l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩᚩ")]).lower() != bstack1111l1l_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬᚪ")
        if os.environ.get(bstack1111l1l_opy_ (u"ࠧࡊࡕࡢࡒࡔࡔ࡟ࡃࡕࡗࡅࡈࡑ࡟ࡊࡐࡉࡖࡆࡥࡁ࠲࠳࡜ࡣࡘࡋࡓࡔࡋࡒࡒࠬᚫ"), bstack1111l1l_opy_ (u"ࠨࠩᚬ")).lower() == bstack1111l1l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᚭ") or bstack11ll1lll1l1_opy_:
          bstack1ll1111ll11_opy_ = bstack11ll1l111ll_opy_.bstack1ll11l11lll_opy_
        if browser_version and browser_version != bstack1111l1l_opy_ (u"ࠪࡰࡦࡺࡥࡴࡶࠪᚮ") and int(browser_version.split(bstack1111l1l_opy_ (u"ࠫ࠳࠭ᚯ"))[0]) <= bstack1ll1111ll11_opy_:
          logger.warning(bstack1lll11lll1l_opy_ (u"ࠬࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡨࡴࡨࡥࡹ࡫ࡲࠡࡶ࡫ࡥࡳࠦࡻ࡮࡫ࡱࡣࡦ࠷࠱ࡺࡡࡶࡹࡵࡶ࡯ࡳࡶࡨࡨࡤࡩࡨࡳࡱࡰࡩࡤࡼࡥࡳࡵ࡬ࡳࡳࢃ࠮ࠨᚰ"))
          return False
        if not options:
          bstack1ll111ll11l_opy_ = caps.get(bstack1111l1l_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᚱ")) or bstack11lll111111_opy_.get(bstack1111l1l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᚲ"), {})
          if bstack1111l1l_opy_ (u"ࠨ࠯࠰࡬ࡪࡧࡤ࡭ࡧࡶࡷࠬᚳ") in bstack1ll111ll11l_opy_.get(bstack1111l1l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᚴ"), []):
              logger.warning(bstack1111l1l_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡴ࡯ࡵࠢࡵࡹࡳࠦ࡯࡯ࠢ࡯ࡩ࡬ࡧࡣࡺࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠣࡗࡼ࡯ࡴࡤࡪࠣࡸࡴࠦ࡮ࡦࡹࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧࠣࡳࡷࠦࡡࡷࡱ࡬ࡨࠥࡻࡳࡪࡰࡪࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲ࠧᚵ"))
              return False
        return True
    except Exception as error:
        logger.debug(bstack1111l1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡺࡦࡲࡩࡥࡣࡷࡩࠥࡧ࠱࠲ࡻࠣࡷࡺࡶࡰࡰࡴࡷࠤ࠿ࠨᚶ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1lll11ll11l_opy_ = config.get(bstack1111l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᚷ"), {})
    bstack1lll11ll11l_opy_[bstack1111l1l_opy_ (u"࠭ࡡࡶࡶ࡫ࡘࡴࡱࡥ࡯ࠩᚸ")] = os.getenv(bstack1111l1l_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᚹ"))
    bstack11ll1l1llll_opy_ = json.loads(os.getenv(bstack1111l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᚺ"), bstack1111l1l_opy_ (u"ࠩࡾࢁࠬᚻ"))).get(bstack1111l1l_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᚼ"))
    if not config[bstack1111l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ᚽ")].get(bstack1111l1l_opy_ (u"ࠧࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠦᚾ")):
      if bstack1111l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᚿ") in caps:
        caps[bstack1111l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᛀ")][bstack1111l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᛁ")] = bstack1lll11ll11l_opy_
        caps[bstack1111l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᛂ")][bstack1111l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᛃ")][bstack1111l1l_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᛄ")] = bstack11ll1l1llll_opy_
      else:
        caps[bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᛅ")] = bstack1lll11ll11l_opy_
        caps[bstack1111l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᛆ")][bstack1111l1l_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᛇ")] = bstack11ll1l1llll_opy_
  except Exception as error:
    logger.debug(bstack1111l1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡪࡺࡴࡪࡰࡪࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠮ࠡࡇࡵࡶࡴࡸ࠺ࠡࠤᛈ") +  str(error))
def bstack11l1ll1l1l_opy_(driver, bstack11ll1ll1111_opy_):
  try:
    setattr(driver, bstack1111l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩᛉ"), True)
    session = driver.session_id
    if session:
      bstack11ll1l11111_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11ll1l11111_opy_ = False
      bstack11ll1l11111_opy_ = url.scheme in [bstack1111l1l_opy_ (u"ࠥ࡬ࡹࡺࡰࠣᛊ"), bstack1111l1l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥᛋ")]
      if bstack11ll1l11111_opy_:
        if bstack11ll1ll1111_opy_:
          logger.info(bstack1111l1l_opy_ (u"࡙ࠧࡥࡵࡷࡳࠤ࡫ࡵࡲࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡫ࡥࡸࠦࡳࡵࡣࡵࡸࡪࡪ࠮ࠡࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡣࡧࡪ࡭ࡳࠦ࡭ࡰ࡯ࡨࡲࡹࡧࡲࡪ࡮ࡼ࠲ࠧᛌ"))
      return bstack11ll1ll1111_opy_
  except Exception as e:
    logger.error(bstack1111l1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡢࡴࡷ࡭ࡳ࡭ࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸࡩࡡ࡯ࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤᛍ") + str(e))
    return False
def bstack11ll1l11_opy_(driver, name, path):
  try:
    bstack1ll1l11111l_opy_ = {
        bstack1111l1l_opy_ (u"ࠧࡵࡪࡗࡩࡸࡺࡒࡶࡰࡘࡹ࡮ࡪࠧᛎ"): threading.current_thread().current_test_uuid,
        bstack1111l1l_opy_ (u"ࠨࡶ࡫ࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ᛏ"): os.environ.get(bstack1111l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᛐ"), bstack1111l1l_opy_ (u"ࠪࠫᛑ")),
        bstack1111l1l_opy_ (u"ࠫࡹ࡮ࡊࡸࡶࡗࡳࡰ࡫࡮ࠨᛒ"): os.environ.get(bstack1111l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩᛓ"), bstack1111l1l_opy_ (u"࠭ࠧᛔ"))
    }
    bstack1ll111l1ll1_opy_ = bstack1lllll1ll_opy_.bstack1ll1l111111_opy_(EVENTS.bstack1ll11ll1l1_opy_.value)
    logger.debug(bstack1111l1l_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡥࡻ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪᛕ"))
    try:
      if (bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨᛖ"), None) and bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫᛗ"), None)):
        scripts = {bstack1111l1l_opy_ (u"ࠪࡷࡨࡧ࡮ࠨᛘ"): bstack1ll1ll1ll1_opy_.perform_scan}
        bstack11ll1l11l11_opy_ = json.loads(scripts[bstack1111l1l_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᛙ")].replace(bstack1111l1l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠣᛚ"), bstack1111l1l_opy_ (u"ࠨࠢᛛ")))
        bstack11ll1l11l11_opy_[bstack1111l1l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᛜ")][bstack1111l1l_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࠨᛝ")] = None
        scripts[bstack1111l1l_opy_ (u"ࠤࡶࡧࡦࡴࠢᛞ")] = bstack1111l1l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨᛟ") + json.dumps(bstack11ll1l11l11_opy_)
        bstack1ll1ll1ll1_opy_.bstack1l11l1ll_opy_(scripts)
        bstack1ll1ll1ll1_opy_.store()
        logger.debug(driver.execute_script(bstack1ll1ll1ll1_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1ll1ll1ll1_opy_.perform_scan, {bstack1111l1l_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦᛠ"): name}))
      bstack1lllll1ll_opy_.end(EVENTS.bstack1ll11ll1l1_opy_.value, bstack1ll111l1ll1_opy_ + bstack1111l1l_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᛡ"), bstack1ll111l1ll1_opy_ + bstack1111l1l_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᛢ"), True, None)
    except Exception as error:
      bstack1lllll1ll_opy_.end(EVENTS.bstack1ll11ll1l1_opy_.value, bstack1ll111l1ll1_opy_ + bstack1111l1l_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᛣ"), bstack1ll111l1ll1_opy_ + bstack1111l1l_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᛤ"), False, str(error))
    bstack1ll111l1ll1_opy_ = bstack1lllll1ll_opy_.bstack11ll1l1ll11_opy_(EVENTS.bstack1ll1l1111l1_opy_.value)
    bstack1lllll1ll_opy_.mark(bstack1ll111l1ll1_opy_ + bstack1111l1l_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᛥ"))
    try:
      if (bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪᛦ"), None) and bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᛧ"), None)):
        scripts = {bstack1111l1l_opy_ (u"ࠬࡹࡣࡢࡰࠪᛨ"): bstack1ll1ll1ll1_opy_.perform_scan}
        bstack11ll1l11l11_opy_ = json.loads(scripts[bstack1111l1l_opy_ (u"ࠨࡳࡤࡣࡱࠦᛩ")].replace(bstack1111l1l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࠥᛪ"), bstack1111l1l_opy_ (u"ࠣࠤ᛫")))
        bstack11ll1l11l11_opy_[bstack1111l1l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ᛬")][bstack1111l1l_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࠪ᛭")] = None
        scripts[bstack1111l1l_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᛮ")] = bstack1111l1l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠣᛯ") + json.dumps(bstack11ll1l11l11_opy_)
        bstack1ll1ll1ll1_opy_.bstack1l11l1ll_opy_(scripts)
        bstack1ll1ll1ll1_opy_.store()
        logger.debug(driver.execute_script(bstack1ll1ll1ll1_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1ll1ll1ll1_opy_.bstack11ll1l11l1l_opy_, bstack1ll1l11111l_opy_))
      bstack1lllll1ll_opy_.end(bstack1ll111l1ll1_opy_, bstack1ll111l1ll1_opy_ + bstack1111l1l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᛰ"), bstack1ll111l1ll1_opy_ + bstack1111l1l_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᛱ"),True, None)
    except Exception as error:
      bstack1lllll1ll_opy_.end(bstack1ll111l1ll1_opy_, bstack1ll111l1ll1_opy_ + bstack1111l1l_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᛲ"), bstack1ll111l1ll1_opy_ + bstack1111l1l_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᛳ"),False, str(error))
    logger.info(bstack1111l1l_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠨᛴ"))
  except Exception as bstack1ll11l1ll11_opy_:
    logger.error(bstack1111l1l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡩ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡤࡨࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨ࠾ࠥࠨᛵ") + str(path) + bstack1111l1l_opy_ (u"ࠧࠦࡅࡳࡴࡲࡶࠥࡀࠢᛶ") + str(bstack1ll11l1ll11_opy_))
def bstack11ll1l111l1_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack1111l1l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧᛷ")) and str(caps.get(bstack1111l1l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨᛸ"))).lower() == bstack1111l1l_opy_ (u"ࠣࡣࡱࡨࡷࡵࡩࡥࠤ᛹"):
        bstack1ll11l1l111_opy_ = caps.get(bstack1111l1l_opy_ (u"ࠤࡤࡴࡵ࡯ࡵ࡮࠼ࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦ᛺")) or caps.get(bstack1111l1l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧ᛻"))
        if bstack1ll11l1l111_opy_ and int(str(bstack1ll11l1l111_opy_)) < bstack11ll1l1ll1l_opy_:
            return False
    return True
def bstack1llllllll1_opy_(config):
  if bstack1111l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ᛼") in config:
        return config[bstack1111l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ᛽")]
  for platform in config.get(bstack1111l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ᛾"), []):
      if bstack1111l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ᛿") in platform:
          return platform[bstack1111l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᜀ")]
  return None
def bstack11l1l11l11_opy_(bstack11l1l1ll11_opy_):
  try:
    browser_name = bstack11l1l1ll11_opy_[bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡲࡦࡳࡥࠨᜁ")]
    browser_version = bstack11l1l1ll11_opy_[bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᜂ")]
    chrome_options = bstack11l1l1ll11_opy_[bstack1111l1l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡣࡴࡶࡴࡪࡱࡱࡷࠬᜃ")]
    try:
        bstack11ll1lll1ll_opy_ = int(browser_version.split(bstack1111l1l_opy_ (u"ࠬ࠴ࠧᜄ"))[0])
    except ValueError as e:
        logger.error(bstack1111l1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡨࡵ࡮ࡷࡧࡵࡸ࡮ࡴࡧࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠥᜅ") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack1111l1l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧᜆ")):
        logger.warning(bstack1111l1l_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦᜇ"))
        return False
    if bstack11ll1lll1ll_opy_ < bstack11ll1l111ll_opy_.bstack1ll11l11lll_opy_:
        logger.warning(bstack1lll11lll1l_opy_ (u"ࠩࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡲࡦࡳࡸ࡭ࡷ࡫ࡳࠡࡅ࡫ࡶࡴࡳࡥࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡾࡇࡔࡔࡓࡕࡃࡑࡘࡘ࠴ࡍࡊࡐࡌࡑ࡚ࡓ࡟ࡏࡑࡑࡣࡇ࡙ࡔࡂࡅࡎࡣࡎࡔࡆࡓࡃࡢࡅ࠶࠷࡙ࡠࡕࡘࡔࡕࡕࡒࡕࡇࡇࡣࡈࡎࡒࡐࡏࡈࡣ࡛ࡋࡒࡔࡋࡒࡒࢂࠦ࡯ࡳࠢ࡫࡭࡬࡮ࡥࡳ࠰ࠪᜈ"))
        return False
    if chrome_options and any(bstack1111l1l_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹࠧᜉ") in value for value in chrome_options.values() if isinstance(value, str)):
        logger.warning(bstack1111l1l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦ࡮ࡰࡶࠣࡶࡺࡴࠠࡰࡰࠣࡰࡪ࡭ࡡࡤࡻࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠤࡘࡽࡩࡵࡥ࡫ࠤࡹࡵࠠ࡯ࡧࡺࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠤࡴࡸࠠࡢࡸࡲ࡭ࡩࠦࡵࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠨᜊ"))
        return False
    return True
  except Exception as e:
    logger.error(bstack1111l1l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡤࡪࡨࡧࡰ࡯࡮ࡨࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡸࡻࡰࡱࡱࡵࡸࠥ࡬࡯ࡳࠢ࡯ࡳࡨࡧ࡬ࠡࡅ࡫ࡶࡴࡳࡥ࠻ࠢࠥᜋ") + str(e))
    return False
def bstack1llll1ll_opy_(bstack1ll1llll1l_opy_, config):
    try:
      bstack1ll111l1l1l_opy_ = bstack1111l1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᜌ") in config and config[bstack1111l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᜍ")] == True
      bstack11ll1lll1l1_opy_ = bstack1111l1l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬᜎ") in config and str(config[bstack1111l1l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᜏ")]).lower() != bstack1111l1l_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩᜐ")
      if not (bstack1ll111l1l1l_opy_ and (not bstack111l1l11_opy_(config) or bstack11ll1lll1l1_opy_)):
        return bstack1ll1llll1l_opy_
      bstack11ll1l11ll1_opy_ = bstack1ll1ll1ll1_opy_.bstack11ll1ll1l1l_opy_
      if bstack11ll1l11ll1_opy_ is None:
        logger.debug(bstack1111l1l_opy_ (u"ࠦࡌࡵ࡯ࡨ࡮ࡨࠤࡨ࡮ࡲࡰ࡯ࡨࠤࡴࡶࡴࡪࡱࡱࡷࠥࡧࡲࡦࠢࡑࡳࡳ࡫ࠢᜑ"))
        return bstack1ll1llll1l_opy_
      bstack11ll1ll111l_opy_ = int(str(bstack11ll11lllll_opy_()).split(bstack1111l1l_opy_ (u"ࠬ࠴ࠧᜒ"))[0])
      logger.debug(bstack1111l1l_opy_ (u"ࠨࡓࡦ࡮ࡨࡲ࡮ࡻ࡭ࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡧࡩࡹ࡫ࡣࡵࡧࡧ࠾ࠥࠨᜓ") + str(bstack11ll1ll111l_opy_) + bstack1111l1l_opy_ (u"᜔ࠢࠣ"))
      if bstack11ll1ll111l_opy_ == 3 and isinstance(bstack1ll1llll1l_opy_, dict) and bstack1111l1l_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ᜕") in bstack1ll1llll1l_opy_ and bstack11ll1l11ll1_opy_ is not None:
        if bstack1111l1l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᜖") not in bstack1ll1llll1l_opy_[bstack1111l1l_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ᜗")]:
          bstack1ll1llll1l_opy_[bstack1111l1l_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ᜘")][bstack1111l1l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ᜙")] = {}
        if bstack1111l1l_opy_ (u"࠭ࡡࡳࡩࡶࠫ᜚") in bstack11ll1l11ll1_opy_:
          if bstack1111l1l_opy_ (u"ࠧࡢࡴࡪࡷࠬ᜛") not in bstack1ll1llll1l_opy_[bstack1111l1l_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ᜜")][bstack1111l1l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᜝")]:
            bstack1ll1llll1l_opy_[bstack1111l1l_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ᜞")][bstack1111l1l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᜟ")][bstack1111l1l_opy_ (u"ࠬࡧࡲࡨࡵࠪᜠ")] = []
          for arg in bstack11ll1l11ll1_opy_[bstack1111l1l_opy_ (u"࠭ࡡࡳࡩࡶࠫᜡ")]:
            if arg not in bstack1ll1llll1l_opy_[bstack1111l1l_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᜢ")][bstack1111l1l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᜣ")][bstack1111l1l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᜤ")]:
              bstack1ll1llll1l_opy_[bstack1111l1l_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᜥ")][bstack1111l1l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᜦ")][bstack1111l1l_opy_ (u"ࠬࡧࡲࡨࡵࠪᜧ")].append(arg)
        if bstack1111l1l_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᜨ") in bstack11ll1l11ll1_opy_:
          if bstack1111l1l_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᜩ") not in bstack1ll1llll1l_opy_[bstack1111l1l_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᜪ")][bstack1111l1l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᜫ")]:
            bstack1ll1llll1l_opy_[bstack1111l1l_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᜬ")][bstack1111l1l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᜭ")][bstack1111l1l_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᜮ")] = []
          for ext in bstack11ll1l11ll1_opy_[bstack1111l1l_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᜯ")]:
            if ext not in bstack1ll1llll1l_opy_[bstack1111l1l_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᜰ")][bstack1111l1l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᜱ")][bstack1111l1l_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᜲ")]:
              bstack1ll1llll1l_opy_[bstack1111l1l_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᜳ")][bstack1111l1l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴ᜴ࠩ")][bstack1111l1l_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩ᜵")].append(ext)
        if bstack1111l1l_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬ᜶") in bstack11ll1l11ll1_opy_:
          if bstack1111l1l_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭᜷") not in bstack1ll1llll1l_opy_[bstack1111l1l_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ᜸")][bstack1111l1l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᜹")]:
            bstack1ll1llll1l_opy_[bstack1111l1l_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ᜺")][bstack1111l1l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᜻")][bstack1111l1l_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ᜼")] = {}
          bstack11ll11ll11l_opy_(bstack1ll1llll1l_opy_[bstack1111l1l_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭᜽")][bstack1111l1l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ᜾")][bstack1111l1l_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧ᜿")],
                    bstack11ll1l11ll1_opy_[bstack1111l1l_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᝀ")])
        os.environ[bstack1111l1l_opy_ (u"ࠪࡍࡘࡥࡎࡐࡐࡢࡆࡘ࡚ࡁࡄࡍࡢࡍࡓࡌࡒࡂࡡࡄ࠵࠶࡟࡟ࡔࡇࡖࡗࡎࡕࡎࠨᝁ")] = bstack1111l1l_opy_ (u"ࠫࡹࡸࡵࡦࠩᝂ")
        return bstack1ll1llll1l_opy_
      else:
        chrome_options = None
        if isinstance(bstack1ll1llll1l_opy_, ChromeOptions):
          chrome_options = bstack1ll1llll1l_opy_
        elif isinstance(bstack1ll1llll1l_opy_, dict):
          for value in bstack1ll1llll1l_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack1ll1llll1l_opy_, dict):
            bstack1ll1llll1l_opy_[bstack1111l1l_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ᝃ")] = chrome_options
          else:
            bstack1ll1llll1l_opy_ = chrome_options
        if bstack11ll1l11ll1_opy_ is not None:
          if bstack1111l1l_opy_ (u"࠭ࡡࡳࡩࡶࠫᝄ") in bstack11ll1l11ll1_opy_:
                bstack11ll1l1l111_opy_ = chrome_options.arguments or []
                new_args = bstack11ll1l11ll1_opy_[bstack1111l1l_opy_ (u"ࠧࡢࡴࡪࡷࠬᝅ")]
                for arg in new_args:
                    if arg not in bstack11ll1l1l111_opy_:
                        chrome_options.add_argument(arg)
          if bstack1111l1l_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᝆ") in bstack11ll1l11ll1_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack1111l1l_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᝇ"), [])
                bstack11ll1l1l1ll_opy_ = bstack11ll1l11ll1_opy_[bstack1111l1l_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᝈ")]
                for extension in bstack11ll1l1l1ll_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack1111l1l_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪᝉ") in bstack11ll1l11ll1_opy_:
                bstack11ll11lll11_opy_ = chrome_options.experimental_options.get(bstack1111l1l_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫᝊ"), {})
                bstack11ll1llllll_opy_ = bstack11ll1l11ll1_opy_[bstack1111l1l_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬᝋ")]
                bstack11ll11ll11l_opy_(bstack11ll11lll11_opy_, bstack11ll1llllll_opy_)
                chrome_options.add_experimental_option(bstack1111l1l_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ᝌ"), bstack11ll11lll11_opy_)
        os.environ[bstack1111l1l_opy_ (u"ࠨࡋࡖࡣࡓࡕࡎࡠࡄࡖࡘࡆࡉࡋࡠࡋࡑࡊࡗࡇ࡟ࡂ࠳࠴࡝ࡤ࡙ࡅࡔࡕࡌࡓࡓ࠭ᝍ")] = bstack1111l1l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᝎ")
        return bstack1ll1llll1l_opy_
    except Exception as e:
      logger.error(bstack1111l1l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡣࡧࡨ࡮ࡴࡧࠡࡰࡲࡲ࠲ࡈࡓࠡ࡫ࡱࡪࡷࡧࠠࡢ࠳࠴ࡽࠥࡩࡨࡳࡱࡰࡩࠥࡵࡰࡵ࡫ࡲࡲࡸࡀࠠࠣᝏ") + str(e))
      return bstack1ll1llll1l_opy_