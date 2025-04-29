# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack111l1l1_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1llllll_opy_ (bstack1ll111l_opy_):
    global bstack1l111l_opy_
    bstack1l11l_opy_ = ord (bstack1ll111l_opy_ [-1])
    bstack1111l1l_opy_ = bstack1ll111l_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack1l11l_opy_ % len (bstack1111l1l_opy_)
    bstack1ll1_opy_ = bstack1111l1l_opy_ [:bstack11ll1ll_opy_] + bstack1111l1l_opy_ [bstack11ll1ll_opy_:]
    if bstack11l1l1_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1lllll1l_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack11llll11l1l_opy_, bstack1l1ll111_opy_, get_host_info, bstack11l1ll11111_opy_, \
 bstack1l1ll1lll_opy_, bstack1lll11l1_opy_, bstack111l1l1111_opy_, bstack11l1ll1llll_opy_, bstack1l11l1l11l_opy_
import bstack_utils.accessibility as bstack11111l11l_opy_
from bstack_utils.bstack11l1111ll1_opy_ import bstack1ll1l111l1_opy_
from bstack_utils.percy import bstack11lll1ll1_opy_
from bstack_utils.config import Config
bstack1l1ll1l1l1_opy_ = Config.bstack11ll1ll1l1_opy_()
logger = logging.getLogger(__name__)
percy = bstack11lll1ll1_opy_()
@bstack111l1l1111_opy_(class_method=False)
def bstack1111ll1l1l1_opy_(bs_config, bstack1l1lllllll_opy_):
  try:
    data = {
        bstack1llllll_opy_ (u"ࠪࡪࡴࡸ࡭ࡢࡶࠪỾ"): bstack1llllll_opy_ (u"ࠫ࡯ࡹ࡯࡯ࠩỿ"),
        bstack1llllll_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡥ࡮ࡢ࡯ࡨࠫἀ"): bs_config.get(bstack1llllll_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫἁ"), bstack1llllll_opy_ (u"ࠧࠨἂ")),
        bstack1llllll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ἃ"): bs_config.get(bstack1llllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬἄ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1llllll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ἅ"): bs_config.get(bstack1llllll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ἆ")),
        bstack1llllll_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪἇ"): bs_config.get(bstack1llllll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡉ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩἈ"), bstack1llllll_opy_ (u"ࠧࠨἉ")),
        bstack1llllll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬἊ"): bstack1l11l1l11l_opy_(),
        bstack1llllll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧἋ"): bstack11l1ll11111_opy_(bs_config),
        bstack1llllll_opy_ (u"ࠪ࡬ࡴࡹࡴࡠ࡫ࡱࡪࡴ࠭Ἄ"): get_host_info(),
        bstack1llllll_opy_ (u"ࠫࡨ࡯࡟ࡪࡰࡩࡳࠬἍ"): bstack1l1ll111_opy_(),
        bstack1llllll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣࡷࡻ࡮ࡠ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬἎ"): os.environ.get(bstack1llllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬἏ")),
        bstack1llllll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪ࡟ࡵࡧࡶࡸࡸࡥࡲࡦࡴࡸࡲࠬἐ"): os.environ.get(bstack1llllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓ࠭ἑ"), False),
        bstack1llllll_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࡢࡧࡴࡴࡴࡳࡱ࡯ࠫἒ"): bstack11llll11l1l_opy_(),
        bstack1llllll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪἓ"): bstack1111l1l11l1_opy_(),
        bstack1llllll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡥࡧࡷࡥ࡮ࡲࡳࠨἔ"): bstack1111l1ll111_opy_(bstack1l1lllllll_opy_),
        bstack1llllll_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹࡥ࡭ࡢࡲࠪἕ"): bstack1111l1l1111_opy_(bs_config, bstack1l1lllllll_opy_.get(bstack1llllll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡸࡷࡪࡪࠧ἖"), bstack1llllll_opy_ (u"ࠧࠨ἗"))),
        bstack1llllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪἘ"): bstack1l1ll1lll_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack1llllll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡰࡢࡻ࡯ࡳࡦࡪࠠࡧࡱࡵࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࠠࡼࡿࠥἙ").format(str(error)))
    return None
def bstack1111l1ll111_opy_(framework):
  return {
    bstack1llllll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡔࡡ࡮ࡧࠪἚ"): framework.get(bstack1llllll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࠬἛ"), bstack1llllll_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬἜ")),
    bstack1llllll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩἝ"): framework.get(bstack1llllll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ἞")),
    bstack1llllll_opy_ (u"ࠨࡵࡧ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬ἟"): framework.get(bstack1llllll_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧἠ")),
    bstack1llllll_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬἡ"): bstack1llllll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫἢ"),
    bstack1llllll_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬἣ"): framework.get(bstack1llllll_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ἤ"))
  }
def bstack1l1l1l1lll_opy_(bs_config, framework):
  bstack1l11l1ll_opy_ = False
  bstack11ll11l1ll_opy_ = False
  bstack1111l1l1l1l_opy_ = False
  if bstack1llllll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫἥ") in bs_config:
    bstack1111l1l1l1l_opy_ = True
  elif bstack1llllll_opy_ (u"ࠨࡣࡳࡴࠬἦ") in bs_config:
    bstack1l11l1ll_opy_ = True
  else:
    bstack11ll11l1ll_opy_ = True
  bstack1lll1l1l1_opy_ = {
    bstack1llllll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩἧ"): bstack1ll1l111l1_opy_.bstack1111l1l1ll1_opy_(bs_config, framework),
    bstack1llllll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪἨ"): bstack11111l11l_opy_.bstack11l11ll111_opy_(bs_config),
    bstack1llllll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪἩ"): bs_config.get(bstack1llllll_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫἪ"), False),
    bstack1llllll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨἫ"): bstack11ll11l1ll_opy_,
    bstack1llllll_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭Ἤ"): bstack1l11l1ll_opy_,
    bstack1llllll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬἭ"): bstack1111l1l1l1l_opy_
  }
  return bstack1lll1l1l1_opy_
@bstack111l1l1111_opy_(class_method=False)
def bstack1111l1l11l1_opy_():
  try:
    bstack1111l11llll_opy_ = json.loads(os.getenv(bstack1llllll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪἮ"), bstack1llllll_opy_ (u"ࠪࡿࢂ࠭Ἧ")))
    return {
        bstack1llllll_opy_ (u"ࠫࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭ἰ"): bstack1111l11llll_opy_
    }
  except Exception as error:
    logger.error(bstack1llllll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠡࡨࡲࡶ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࠡࡽࢀࠦἱ").format(str(error)))
    return {}
def bstack1111ll111l1_opy_(array, bstack1111l1l1l11_opy_, bstack1111l1l111l_opy_):
  result = {}
  for o in array:
    key = o[bstack1111l1l1l11_opy_]
    result[key] = o[bstack1111l1l111l_opy_]
  return result
def bstack1111lll1l11_opy_(bstack11ll1llll_opy_=bstack1llllll_opy_ (u"࠭ࠧἲ")):
  bstack1111l1l1lll_opy_ = bstack11111l11l_opy_.on()
  bstack1111l1ll11l_opy_ = bstack1ll1l111l1_opy_.on()
  bstack1111l1ll1l1_opy_ = percy.bstack1lll11111l_opy_()
  if bstack1111l1ll1l1_opy_ and not bstack1111l1ll11l_opy_ and not bstack1111l1l1lll_opy_:
    return bstack11ll1llll_opy_ not in [bstack1llllll_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫἳ"), bstack1llllll_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬἴ")]
  elif bstack1111l1l1lll_opy_ and not bstack1111l1ll11l_opy_:
    return bstack11ll1llll_opy_ not in [bstack1llllll_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪἵ"), bstack1llllll_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬἶ"), bstack1llllll_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨἷ")]
  return bstack1111l1l1lll_opy_ or bstack1111l1ll11l_opy_ or bstack1111l1ll1l1_opy_
@bstack111l1l1111_opy_(class_method=False)
def bstack1111ll11ll1_opy_(bstack11ll1llll_opy_, test=None):
  bstack1111l1l11ll_opy_ = bstack11111l11l_opy_.on()
  if not bstack1111l1l11ll_opy_ or bstack11ll1llll_opy_ not in [bstack1llllll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧἸ")] or test == None:
    return None
  return {
    bstack1llllll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭Ἱ"): bstack1111l1l11ll_opy_ and bstack1lll11l1_opy_(threading.current_thread(), bstack1llllll_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭Ἲ"), None) == True and bstack11111l11l_opy_.bstack11l1ll11l_opy_(test[bstack1llllll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭Ἳ")])
  }
def bstack1111l1l1111_opy_(bs_config, framework):
  bstack1l11l1ll_opy_ = False
  bstack11ll11l1ll_opy_ = False
  bstack1111l1l1l1l_opy_ = False
  if bstack1llllll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭Ἴ") in bs_config:
    bstack1111l1l1l1l_opy_ = True
  elif bstack1llllll_opy_ (u"ࠪࡥࡵࡶࠧἽ") in bs_config:
    bstack1l11l1ll_opy_ = True
  else:
    bstack11ll11l1ll_opy_ = True
  bstack1lll1l1l1_opy_ = {
    bstack1llllll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫἾ"): bstack1ll1l111l1_opy_.bstack1111l1l1ll1_opy_(bs_config, framework),
    bstack1llllll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬἿ"): bstack11111l11l_opy_.bstack1l1l1lll11_opy_(bs_config),
    bstack1llllll_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬὀ"): bs_config.get(bstack1llllll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ὁ"), False),
    bstack1llllll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪὂ"): bstack11ll11l1ll_opy_,
    bstack1llllll_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨὃ"): bstack1l11l1ll_opy_,
    bstack1llllll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧὄ"): bstack1111l1l1l1l_opy_
  }
  return bstack1lll1l1l1_opy_