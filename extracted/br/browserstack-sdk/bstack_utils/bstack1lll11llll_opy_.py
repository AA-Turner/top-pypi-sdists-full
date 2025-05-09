# coding: UTF-8
import sys
bstack111l1l1_opy_ = sys.version_info [0] == 2
bstack1ll1l1l_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack11lll_opy_ (bstack111ll1l_opy_):
    global bstack1l111l_opy_
    bstack1lllll1l_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack11111ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11ll1l1_opy_ = bstack1lllll1l_opy_ % len (bstack11111ll_opy_)
    bstack1lll1l1_opy_ = bstack11111ll_opy_ [:bstack11ll1l1_opy_] + bstack11111ll_opy_ [bstack11ll1l1_opy_:]
    if bstack111l1l1_opy_:
        bstack1ll1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    else:
        bstack1ll1ll1_opy_ = str () .join ([chr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    return eval (bstack1ll1ll1_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack11lll1l1lll_opy_, bstack11lllll11_opy_, get_host_info, bstack11l11lll11l_opy_, \
 bstack1l111l1ll1_opy_, bstack1llll11ll1_opy_, bstack111l11l1ll_opy_, bstack11l11ll1ll1_opy_, bstack11ll11l1ll_opy_
import bstack_utils.accessibility as bstack11l1lll11_opy_
from bstack_utils.bstack111llllll1_opy_ import bstack1llll1ll1l_opy_
from bstack_utils.percy import bstack1lll1l11ll_opy_
from bstack_utils.config import Config
bstack1llllll11_opy_ = Config.bstack1l1l1l1ll1_opy_()
logger = logging.getLogger(__name__)
percy = bstack1lll1l11ll_opy_()
@bstack111l11l1ll_opy_(class_method=False)
def bstack1111ll1l11l_opy_(bs_config, bstack11l11llll_opy_):
  try:
    data = {
        bstack11lll_opy_ (u"ࠬ࡬࡯ࡳ࡯ࡤࡸࠬἇ"): bstack11lll_opy_ (u"࠭ࡪࡴࡱࡱࠫἈ"),
        bstack11lll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡠࡰࡤࡱࡪ࠭Ἁ"): bs_config.get(bstack11lll_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭Ἂ"), bstack11lll_opy_ (u"ࠩࠪἋ")),
        bstack11lll_opy_ (u"ࠪࡲࡦࡳࡥࠨἌ"): bs_config.get(bstack11lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧἍ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack11lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨἎ"): bs_config.get(bstack11lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨἏ")),
        bstack11lll_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬἐ"): bs_config.get(bstack11lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫἑ"), bstack11lll_opy_ (u"ࠩࠪἒ")),
        bstack11lll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧἓ"): bstack11ll11l1ll_opy_(),
        bstack11lll_opy_ (u"ࠫࡹࡧࡧࡴࠩἔ"): bstack11l11lll11l_opy_(bs_config),
        bstack11lll_opy_ (u"ࠬ࡮࡯ࡴࡶࡢ࡭ࡳ࡬࡯ࠨἕ"): get_host_info(),
        bstack11lll_opy_ (u"࠭ࡣࡪࡡ࡬ࡲ࡫ࡵࠧ἖"): bstack11lllll11_opy_(),
        bstack11lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡲࡶࡰࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ἗"): os.environ.get(bstack11lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧἘ")),
        bstack11lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡴࡨࡶࡺࡴࠧἙ"): os.environ.get(bstack11lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠨἚ"), False),
        bstack11lll_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࡤࡩ࡯࡯ࡶࡵࡳࡱ࠭Ἓ"): bstack11lll1l1lll_opy_(),
        bstack11lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬἜ"): bstack1111l11lll1_opy_(),
        bstack11lll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡧࡩࡹࡧࡩ࡭ࡵࠪἝ"): bstack1111l1ll111_opy_(bstack11l11llll_opy_),
        bstack11lll_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬ἞"): bstack1111l1l111l_opy_(bs_config, bstack11l11llll_opy_.get(bstack11lll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡺࡹࡥࡥࠩ἟"), bstack11lll_opy_ (u"ࠩࠪἠ"))),
        bstack11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬἡ"): bstack1l111l1ll1_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack11lll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡲࡤࡽࡱࡵࡡࡥࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࠢࡾࢁࠧἢ").format(str(error)))
    return None
def bstack1111l1ll111_opy_(framework):
  return {
    bstack11lll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡏࡣࡰࡩࠬἣ"): framework.get(bstack11lll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࠧἤ"), bstack11lll_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧἥ")),
    bstack11lll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫἦ"): framework.get(bstack11lll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ἧ")),
    bstack11lll_opy_ (u"ࠪࡷࡩࡱࡖࡦࡴࡶ࡭ࡴࡴࠧἨ"): framework.get(bstack11lll_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩἩ")),
    bstack11lll_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠧἪ"): bstack11lll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭Ἣ"),
    bstack11lll_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧἬ"): framework.get(bstack11lll_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨἭ"))
  }
def bstack11lll11ll_opy_(bs_config, framework):
  bstack1l1ll1ll11_opy_ = False
  bstack1l11ll1l1l_opy_ = False
  bstack1111l1l1lll_opy_ = False
  if bstack11lll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭Ἦ") in bs_config:
    bstack1111l1l1lll_opy_ = True
  elif bstack11lll_opy_ (u"ࠪࡥࡵࡶࠧἯ") in bs_config:
    bstack1l1ll1ll11_opy_ = True
  else:
    bstack1l11ll1l1l_opy_ = True
  bstack1l11lll1l_opy_ = {
    bstack11lll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫἰ"): bstack1llll1ll1l_opy_.bstack1111l1l1l1l_opy_(bs_config, framework),
    bstack11lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬἱ"): bstack11l1lll11_opy_.bstack11ll111l1l_opy_(bs_config),
    bstack11lll_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬἲ"): bs_config.get(bstack11lll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ἳ"), False),
    bstack11lll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪἴ"): bstack1l11ll1l1l_opy_,
    bstack11lll_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨἵ"): bstack1l1ll1ll11_opy_,
    bstack11lll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧἶ"): bstack1111l1l1lll_opy_
  }
  return bstack1l11lll1l_opy_
@bstack111l11l1ll_opy_(class_method=False)
def bstack1111l11lll1_opy_():
  try:
    bstack1111l1l11l1_opy_ = json.loads(os.getenv(bstack11lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬἷ"), bstack11lll_opy_ (u"ࠬࢁࡽࠨἸ")))
    return {
        bstack11lll_opy_ (u"࠭ࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨἹ"): bstack1111l1l11l1_opy_
    }
  except Exception as error:
    logger.error(bstack11lll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤ࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡵࡨࡸࡹ࡯࡮ࡨࡵࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࠣࡿࢂࠨἺ").format(str(error)))
    return {}
def bstack1111l1ll1ll_opy_(array, bstack1111l1l11ll_opy_, bstack1111l11ll1l_opy_):
  result = {}
  for o in array:
    key = o[bstack1111l1l11ll_opy_]
    result[key] = o[bstack1111l11ll1l_opy_]
  return result
def bstack1111ll1ll11_opy_(bstack1llllllll1_opy_=bstack11lll_opy_ (u"ࠨࠩἻ")):
  bstack1111l1l1ll1_opy_ = bstack11l1lll11_opy_.on()
  bstack1111l11llll_opy_ = bstack1llll1ll1l_opy_.on()
  bstack1111l1l1111_opy_ = percy.bstack1l111lll11_opy_()
  if bstack1111l1l1111_opy_ and not bstack1111l11llll_opy_ and not bstack1111l1l1ll1_opy_:
    return bstack1llllllll1_opy_ not in [bstack11lll_opy_ (u"ࠩࡆࡆ࡙࡙ࡥࡴࡵ࡬ࡳࡳࡉࡲࡦࡣࡷࡩࡩ࠭Ἴ"), bstack11lll_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧἽ")]
  elif bstack1111l1l1ll1_opy_ and not bstack1111l11llll_opy_:
    return bstack1llllllll1_opy_ not in [bstack11lll_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬἾ"), bstack11lll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧἿ"), bstack11lll_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪὀ")]
  return bstack1111l1l1ll1_opy_ or bstack1111l11llll_opy_ or bstack1111l1l1111_opy_
@bstack111l11l1ll_opy_(class_method=False)
def bstack1111ll1llll_opy_(bstack1llllllll1_opy_, test=None):
  bstack1111l1l1l11_opy_ = bstack11l1lll11_opy_.on()
  if not bstack1111l1l1l11_opy_ or bstack1llllllll1_opy_ not in [bstack11lll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩὁ")] or test == None:
    return None
  return {
    bstack11lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨὂ"): bstack1111l1l1l11_opy_ and bstack1llll11ll1_opy_(threading.current_thread(), bstack11lll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨὃ"), None) == True and bstack11l1lll11_opy_.bstack1l11l111l_opy_(test[bstack11lll_opy_ (u"ࠪࡸࡦ࡭ࡳࠨὄ")])
  }
def bstack1111l1l111l_opy_(bs_config, framework):
  bstack1l1ll1ll11_opy_ = False
  bstack1l11ll1l1l_opy_ = False
  bstack1111l1l1lll_opy_ = False
  if bstack11lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨὅ") in bs_config:
    bstack1111l1l1lll_opy_ = True
  elif bstack11lll_opy_ (u"ࠬࡧࡰࡱࠩ὆") in bs_config:
    bstack1l1ll1ll11_opy_ = True
  else:
    bstack1l11ll1l1l_opy_ = True
  bstack1l11lll1l_opy_ = {
    bstack11lll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭὇"): bstack1llll1ll1l_opy_.bstack1111l1l1l1l_opy_(bs_config, framework),
    bstack11lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧὈ"): bstack11l1lll11_opy_.bstack11ll1l1111_opy_(bs_config),
    bstack11lll_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧὉ"): bs_config.get(bstack11lll_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨὊ"), False),
    bstack11lll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬὋ"): bstack1l11ll1l1l_opy_,
    bstack11lll_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪὌ"): bstack1l1ll1ll11_opy_,
    bstack11lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩὍ"): bstack1111l1l1lll_opy_
  }
  return bstack1l11lll1l_opy_