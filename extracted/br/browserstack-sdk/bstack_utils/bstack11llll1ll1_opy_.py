# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack1111l111111_opy_, bstack11111l1lll_opy_, get_host_info, get_custom_tags, \
 bstack111l11l11l_opy_, bstack11llll11_opy_, error_handler, bstack1llll1l111ll_opy_, bstack1l1111ll_opy_, \
 bstack11ll11lll1_opy_, bstack11lll1l1l1_opy_
import bstack_utils.accessibility as a11y
from bstack_utils.bstack11ll1lll1_opy_ import bstack11ll1111l_opy_
from bstack_utils.bstack11l111ll_opy_ import bstack1ll111ll_opy_
from bstack_utils.percy import bstack11ll1l1111_opy_
from bstack_utils.config import Config
global_config = Config.bstack1lll1l11_opy_()
logger = logging.getLogger(__name__)
percy = bstack11ll1l1111_opy_()
@error_handler(class_method=False)
def bstack1l1lll1lllll_opy_(bs_config, bstack1111l11l1_opy_):
  try:
    data = {
        bstack1l1llll_opy_ (u"ࠪࡪࡴࡸ࡭ࡢࡶࠪⱹ"): bstack1l1llll_opy_ (u"ࠫ࡯ࡹ࡯࡯ࠩⱺ"),
        bstack1l1llll_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡥ࡮ࡢ࡯ࡨࠫⱻ"): bs_config.get(bstack1l1llll_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫⱼ"), bstack1l1llll_opy_ (u"ࠧࠨⱽ")),
        bstack1l1llll_opy_ (u"ࠨࡰࡤࡱࡪ࠭Ȿ"): bs_config.get(bstack1l1llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬⱿ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1l1llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭Ⲁ"): bs_config.get(bstack1l1llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ⲁ")),
        bstack1l1llll_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪⲂ"): bs_config.get(bstack1l1llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡉ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩⲃ"), bstack1l1llll_opy_ (u"ࠧࠨⲄ")),
        bstack1l1llll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬⲅ"): bstack1l1111ll_opy_(),
        bstack1l1llll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧⲆ"): get_custom_tags(bs_config),
        bstack1l1llll_opy_ (u"ࠪ࡬ࡴࡹࡴࡠ࡫ࡱࡪࡴ࠭ⲇ"): get_host_info(),
        bstack1l1llll_opy_ (u"ࠫࡨ࡯࡟ࡪࡰࡩࡳࠬⲈ"): bstack11111l1lll_opy_(),
        bstack1l1llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣࡷࡻ࡮ࡠ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬⲉ"): os.environ.get(bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬⲊ")),
        bstack1l1llll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪ࡟ࡵࡧࡶࡸࡸࡥࡲࡦࡴࡸࡲࠬⲋ"): os.environ.get(bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓ࠭Ⲍ"), False),
        bstack1l1llll_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࡢࡧࡴࡴࡴࡳࡱ࡯ࠫⲍ"): bstack1111l111111_opy_(),
        bstack1l1llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪⲎ"): bstack1l1lll111lll_opy_(bs_config),
        bstack1l1llll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡥࡧࡷࡥ࡮ࡲࡳࠨⲏ"): bstack1l1lll111l1l_opy_(bstack1111l11l1_opy_),
        bstack1l1llll_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹࡥ࡭ࡢࡲࠪⲐ"): bstack1l1ll1lllll1_opy_(bs_config, bstack1111l11l1_opy_.get(bstack1l1llll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡸࡷࡪࡪࠧⲑ"), bstack1l1llll_opy_ (u"ࠧࠨⲒ"))),
        bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪⲓ"): bstack111l11l11l_opy_(bs_config),
        bstack1l1llll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠧⲔ"): bstack1l1lll1111ll_opy_(bs_config)
    }
    bstack1l1ll1lll1l1_opy_ = (os.environ.get(bstack1l1llll_opy_ (u"ࠪࡐࡎࡔࡋࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡘ࡙ࡎࡊࠧⲕ")) or bstack1l1llll_opy_ (u"ࠫࠬⲖ")).strip()
    if bstack1l1ll1lll1l1_opy_ and bstack11ll11lll1_opy_():
      data[bstack1l1llll_opy_ (u"ࠬࡲࡩ࡯࡭ࡨࡨࡤࡨࡵࡪ࡮ࡧࡣࡺࡻࡩࡥࠩⲗ")] = bstack1l1ll1lll1l1_opy_
    try:
      bstack1llll1ll1l11_opy_ = bstack11lll1l1l1_opy_(bs_config)
      if bstack1llll1ll1l11_opy_:
        data[bstack1l1llll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡲࡧ࡮ࡢࡩࡨࡱࡪࡴࡴࠨⲘ")] = {
          bstack1l1llll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡶ࡬ࡢࡰࡢ࡭ࡩ࠭ⲙ"): bstack1llll1ll1l11_opy_
        }
    except Exception as error:
      logger.debug(bstack1l1llll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡥࡹࡺࡡࡤࡪ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡵࡲࡡ࡯ࠢ࡬ࡨࠥࡺ࡯ࠡࡤࡸ࡭ࡱࡪࠠࡴࡶࡤࡶࡹࠦࡰࡢࡻ࡯ࡳࡦࡪ࠺ࠡࡽࢀࠦⲚ").format(str(error)))
    return data
  except Exception as error:
    logger.error(bstack1l1llll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡰࡢࡻ࡯ࡳࡦࡪࠠࡧࡱࡵࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࠠࡼࡿࠥⲛ").format(str(error)))
    return None
def bstack1l1lll111l1l_opy_(framework):
  return {
    bstack1l1llll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡔࡡ࡮ࡧࠪⲜ"): framework.get(bstack1l1llll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࠬⲝ"), bstack1l1llll_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬⲞ")),
    bstack1l1llll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩⲟ"): framework.get(bstack1l1llll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫⲠ")),
    bstack1l1llll_opy_ (u"ࠨࡵࡧ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬⲡ"): framework.get(bstack1l1llll_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧⲢ")),
    bstack1l1llll_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬⲣ"): bstack1l1llll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫⲤ"),
    bstack1l1llll_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬⲥ"): framework.get(bstack1l1llll_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭Ⲧ"))
  }
def bstack1l1lll1111ll_opy_(bs_config):
  bstack1l1llll_opy_ (u"ࠢࠣࠤࠍࠤࠥࡘࡥࡵࡷࡵࡲࡸࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣࡦࡺ࡯࡬ࡥࠢࡶࡸࡦࡸࡴ࠯ࠌࠣࠤࠧࠨࠢⲧ")
  if not bs_config:
    return {}
  bstack1ll1ll1l1lll_opy_ = bstack11ll1111l_opy_(bs_config).bstack1ll1l1l1ll1l_opy_(bs_config)
  return bstack1ll1ll1l1lll_opy_
def bstack1l11111lll_opy_(bs_config, framework):
  bstack1lll1l11ll_opy_ = False
  bstack1lll111l1l_opy_ = False
  bstack1l1lll11111l_opy_ = False
  bstack1l1ll1lll111_opy_ = bstack11ll11lll1_opy_()
  if bstack1l1llll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬⲨ") in bs_config:
    bstack1l1lll11111l_opy_ = True
  elif bstack1l1llll_opy_ (u"ࠩࡤࡴࡵ࠭ⲩ") in bs_config:
    bstack1lll1l11ll_opy_ = True
  elif bstack1l1ll1lll111_opy_:
    bstack1lll111l1l_opy_ = False
  else:
    bstack1lll111l1l_opy_ = True
  bstack1l1l111lll_opy_ = {
    bstack1l1llll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪⲪ"): bstack1ll111ll_opy_.bstack1l1ll1llllll_opy_(bs_config, framework),
    bstack1l1llll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫⲫ"): a11y.is_enabled_root(bs_config),
    bstack1l1llll_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫⲬ"): bs_config.get(bstack1l1llll_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬⲭ"), False),
    bstack1l1llll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩⲮ"): bstack1lll111l1l_opy_,
    bstack1l1llll_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧⲯ"): bstack1lll1l11ll_opy_,
    bstack1l1llll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭Ⲱ"): bstack1l1lll11111l_opy_,
    bstack1l1llll_opy_ (u"ࠪࡰࡹࡹࠧⲱ"): bstack1l1ll1lll111_opy_
  }
  return bstack1l1l111lll_opy_
@error_handler(class_method=False)
def bstack1l1lll111lll_opy_(bs_config):
  try:
    bstack1l1lll111l11_opy_ = json.loads(os.getenv(bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬⲲ"), bstack1l1llll_opy_ (u"ࠬࢁࡽࠨⲳ")))
    bstack1l1lll111l11_opy_ = bstack1l1ll1lll1ll_opy_(bs_config, bstack1l1lll111l11_opy_)
    return {
        bstack1l1llll_opy_ (u"࠭ࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨⲴ"): bstack1l1lll111l11_opy_
    }
  except Exception as error:
    logger.error(bstack1l1llll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤ࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡵࡨࡸࡹ࡯࡮ࡨࡵࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࠣࡿࢂࠨⲵ").format(str(error)))
    return {}
def bstack1l1ll1lll1ll_opy_(bs_config, bstack1l1lll111l11_opy_):
  if ((bstack1l1llll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬⲶ") in bs_config or not bstack111l11l11l_opy_(bs_config)) and a11y.is_enabled_root(bs_config)):
    bstack1l1lll111l11_opy_[bstack1l1llll_opy_ (u"ࠤ࡬ࡲࡨࡲࡵࡥࡧࡈࡲࡨࡵࡤࡦࡦࡈࡼࡹ࡫࡮ࡴ࡫ࡲࡲࠧⲷ")] = True
  return bstack1l1lll111l11_opy_
def bstack1l1lll1l11l1_opy_(array, bstack1l1lll1111l1_opy_, bstack1l1ll1llll1l_opy_):
  result = {}
  for o in array:
    key = o[bstack1l1lll1111l1_opy_]
    result[key] = o[bstack1l1ll1llll1l_opy_]
  return result
def bstack1l1lll1l111l_opy_(bstack1l1lll111_opy_=bstack1l1llll_opy_ (u"ࠪࠫⲸ")):
  bstack11l1l1111l1_opy_ = a11y.on()
  bstack1l1lll111ll1_opy_ = bstack1ll111ll_opy_.on()
  bstack1l1ll1llll11_opy_ = percy.bstack1lll11llll1_opy_()
  bstack1l1lll111111_opy_ = bstack11ll11lll1_opy_()
  if not (bstack11l1l1111l1_opy_ or bstack1l1lll111ll1_opy_ or bstack1l1ll1llll11_opy_ or bstack1l1lll111111_opy_):
    return False
  if bstack1l1ll1llll11_opy_ and not bstack1l1lll111ll1_opy_ and not bstack11l1l1111l1_opy_:
    return bstack1l1lll111_opy_ not in [bstack1l1llll_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨⲹ"), bstack1l1llll_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩⲺ")]
  if bstack11l1l1111l1_opy_ and not bstack1l1lll111ll1_opy_ and not bstack1l1ll1llll11_opy_:
    return bstack1l1lll111_opy_ not in [bstack1l1llll_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧⲻ"), bstack1l1llll_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩⲼ"), bstack1l1llll_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬⲽ")]
  return True
@error_handler(class_method=False)
def bstack1l1lll1ll1l1_opy_(bstack1l1lll111_opy_, test=None):
  bstack1l1ll1lll11l_opy_ = a11y.on()
  if not bstack1l1ll1lll11l_opy_ or bstack1l1lll111_opy_ not in [bstack1l1llll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪⲾ"), bstack1l1llll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬⲿ"), bstack1l1llll_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨⳀ")] or test == None:
    return None
  return {
    bstack1l1llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬⳁ"): bstack1l1ll1lll11l_opy_ and bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬⳂ"), None) == True and a11y.is_enabled_testcase(test.get(bstack1l1llll_opy_ (u"ࠧࡵࡣࡪࡷࠬⳃ"), []))
  }
def bstack1l1ll1lllll1_opy_(bs_config, framework):
  bstack1lll1l11ll_opy_ = False
  bstack1lll111l1l_opy_ = False
  bstack1l1lll11111l_opy_ = False
  bstack1l1ll1lll111_opy_ = bstack11ll11lll1_opy_()
  if bstack1l1llll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬⳄ") in bs_config:
    bstack1l1lll11111l_opy_ = True
  elif bstack1l1llll_opy_ (u"ࠩࡤࡴࡵ࠭ⳅ") in bs_config:
    bstack1lll1l11ll_opy_ = True
  elif bstack1l1ll1lll111_opy_:
    bstack1lll111l1l_opy_ = False
  else:
    bstack1lll111l1l_opy_ = True
  bstack1l1l111lll_opy_ = {
    bstack1l1llll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪⳆ"): bstack1ll111ll_opy_.bstack1l1ll1llllll_opy_(bs_config, framework),
    bstack1l1llll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫⳇ"): a11y.bstack1l11lll111_opy_(bs_config),
    bstack1l1llll_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫⳈ"): bs_config.get(bstack1l1llll_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬⳉ"), False),
    bstack1l1llll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩⳊ"): bstack1lll111l1l_opy_,
    bstack1l1llll_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧⳋ"): bstack1lll1l11ll_opy_,
    bstack1l1llll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭Ⳍ"): bstack1l1lll11111l_opy_,
    bstack1l1llll_opy_ (u"ࠪࡰࡹࡹࠧⳍ"): bstack1l1ll1lll111_opy_
  }
  return bstack1l1l111lll_opy_