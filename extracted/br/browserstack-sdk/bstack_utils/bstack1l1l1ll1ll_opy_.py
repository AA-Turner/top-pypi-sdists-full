# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack11llll1l1ll_opy_, bstack1lll1ll1ll_opy_, get_host_info, bstack11ll111111l_opy_, \
 bstack1l11l1l1l_opy_, bstack11l11l1ll1_opy_, bstack111l1ll1ll_opy_, bstack11l1l1l111l_opy_, bstack11lll111l1_opy_
import bstack_utils.accessibility as bstack11ll1l1ll1_opy_
from bstack_utils.bstack111lllll11_opy_ import bstack111l1llll_opy_
from bstack_utils.percy import bstack1l1l111lll_opy_
from bstack_utils.config import Config
bstack11lll1l1ll_opy_ = Config.bstack1lll1l1lll_opy_()
logger = logging.getLogger(__name__)
percy = bstack1l1l111lll_opy_()
@bstack111l1ll1ll_opy_(class_method=False)
def bstack1111ll1l111_opy_(bs_config, bstack1l111111ll_opy_):
  try:
    data = {
        bstack1l11lll_opy_ (u"ࠨࡨࡲࡶࡲࡧࡴࠨỼ"): bstack1l11lll_opy_ (u"ࠩ࡭ࡷࡴࡴࠧỽ"),
        bstack1l11lll_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡣࡳࡧ࡭ࡦࠩỾ"): bs_config.get(bstack1l11lll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩỿ"), bstack1l11lll_opy_ (u"ࠬ࠭ἀ")),
        bstack1l11lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫἁ"): bs_config.get(bstack1l11lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪἂ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1l11lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫἃ"): bs_config.get(bstack1l11lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫἄ")),
        bstack1l11lll_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨἅ"): bs_config.get(bstack1l11lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧἆ"), bstack1l11lll_opy_ (u"ࠬ࠭ἇ")),
        bstack1l11lll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪἈ"): bstack11lll111l1_opy_(),
        bstack1l11lll_opy_ (u"ࠧࡵࡣࡪࡷࠬἉ"): bstack11ll111111l_opy_(bs_config),
        bstack1l11lll_opy_ (u"ࠨࡪࡲࡷࡹࡥࡩ࡯ࡨࡲࠫἊ"): get_host_info(),
        bstack1l11lll_opy_ (u"ࠩࡦ࡭ࡤ࡯࡮ࡧࡱࠪἋ"): bstack1lll1ll1ll_opy_(),
        bstack1l11lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡵࡹࡳࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪἌ"): os.environ.get(bstack1l11lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪἍ")),
        bstack1l11lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࡤࡺࡥࡴࡶࡶࡣࡷ࡫ࡲࡶࡰࠪἎ"): os.environ.get(bstack1l11lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠫἏ"), False),
        bstack1l11lll_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࡠࡥࡲࡲࡹࡸ࡯࡭ࠩἐ"): bstack11llll1l1ll_opy_(),
        bstack1l11lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨἑ"): bstack1111l1ll111_opy_(),
        bstack1l11lll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡪࡥࡵࡣ࡬ࡰࡸ࠭ἒ"): bstack1111l1l11ll_opy_(bstack1l111111ll_opy_),
        bstack1l11lll_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨἓ"): bstack1111l1ll11l_opy_(bs_config, bstack1l111111ll_opy_.get(bstack1l11lll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬἔ"), bstack1l11lll_opy_ (u"ࠬ࠭ἕ"))),
        bstack1l11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ἖"): bstack1l11l1l1l_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack1l11lll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡵࡧࡹ࡭ࡱࡤࡨࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࠥࢁࡽࠣ἗").format(str(error)))
    return None
def bstack1111l1l11ll_opy_(framework):
  return {
    bstack1l11lll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡒࡦࡳࡥࠨἘ"): framework.get(bstack1l11lll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࠪἙ"), bstack1l11lll_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪἚ")),
    bstack1l11lll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧἛ"): framework.get(bstack1l11lll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩἜ")),
    bstack1l11lll_opy_ (u"࠭ࡳࡥ࡭࡙ࡩࡷࡹࡩࡰࡰࠪἝ"): framework.get(bstack1l11lll_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ἞")),
    bstack1l11lll_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪ἟"): bstack1l11lll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩἠ"),
    bstack1l11lll_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪἡ"): framework.get(bstack1l11lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫἢ"))
  }
def bstack1lll11ll_opy_(bs_config, framework):
  bstack111ll111_opy_ = False
  bstack1l1lllll_opy_ = False
  bstack1111l1l11l1_opy_ = False
  if bstack1l11lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩἣ") in bs_config:
    bstack1111l1l11l1_opy_ = True
  elif bstack1l11lll_opy_ (u"࠭ࡡࡱࡲࠪἤ") in bs_config:
    bstack111ll111_opy_ = True
  else:
    bstack1l1lllll_opy_ = True
  bstack1ll1111l_opy_ = {
    bstack1l11lll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧἥ"): bstack111l1llll_opy_.bstack1111l11llll_opy_(bs_config, framework),
    bstack1l11lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨἦ"): bstack11ll1l1ll1_opy_.bstack1lll1ll1l_opy_(bs_config),
    bstack1l11lll_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨἧ"): bs_config.get(bstack1l11lll_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩἨ"), False),
    bstack1l11lll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭Ἡ"): bstack1l1lllll_opy_,
    bstack1l11lll_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫἪ"): bstack111ll111_opy_,
    bstack1l11lll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪἫ"): bstack1111l1l11l1_opy_
  }
  return bstack1ll1111l_opy_
@bstack111l1ll1ll_opy_(class_method=False)
def bstack1111l1ll111_opy_():
  try:
    bstack1111l1l1l11_opy_ = json.loads(os.getenv(bstack1l11lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨἬ"), bstack1l11lll_opy_ (u"ࠨࡽࢀࠫἭ")))
    return {
        bstack1l11lll_opy_ (u"ࠩࡶࡩࡹࡺࡩ࡯ࡩࡶࠫἮ"): bstack1111l1l1l11_opy_
    }
  except Exception as error:
    logger.error(bstack1l11lll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸࠦࡦࡰࡴࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࠦࡻࡾࠤἯ").format(str(error)))
    return {}
def bstack1111l1llll1_opy_(array, bstack1111l1l1111_opy_, bstack1111l1l1ll1_opy_):
  result = {}
  for o in array:
    key = o[bstack1111l1l1111_opy_]
    result[key] = o[bstack1111l1l1ll1_opy_]
  return result
def bstack1111lll111l_opy_(bstack11l11llll1_opy_=bstack1l11lll_opy_ (u"ࠫࠬἰ")):
  bstack1111l1ll1l1_opy_ = bstack11ll1l1ll1_opy_.on()
  bstack1111l1l111l_opy_ = bstack111l1llll_opy_.on()
  bstack1111l1l1lll_opy_ = percy.bstack1l111l111_opy_()
  if bstack1111l1l1lll_opy_ and not bstack1111l1l111l_opy_ and not bstack1111l1ll1l1_opy_:
    return bstack11l11llll1_opy_ not in [bstack1l11lll_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩἱ"), bstack1l11lll_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪἲ")]
  elif bstack1111l1ll1l1_opy_ and not bstack1111l1l111l_opy_:
    return bstack11l11llll1_opy_ not in [bstack1l11lll_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨἳ"), bstack1l11lll_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪἴ"), bstack1l11lll_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ἵ")]
  return bstack1111l1ll1l1_opy_ or bstack1111l1l111l_opy_ or bstack1111l1l1lll_opy_
@bstack111l1ll1ll_opy_(class_method=False)
def bstack1111l1ll1ll_opy_(bstack11l11llll1_opy_, test=None):
  bstack1111l1l1l1l_opy_ = bstack11ll1l1ll1_opy_.on()
  if not bstack1111l1l1l1l_opy_ or bstack11l11llll1_opy_ not in [bstack1l11lll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬἶ")] or test == None:
    return None
  return {
    bstack1l11lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫἷ"): bstack1111l1l1l1l_opy_ and bstack11l11l1ll1_opy_(threading.current_thread(), bstack1l11lll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫἸ"), None) == True and bstack11ll1l1ll1_opy_.bstack111ll1l1l_opy_(test[bstack1l11lll_opy_ (u"࠭ࡴࡢࡩࡶࠫἹ")])
  }
def bstack1111l1ll11l_opy_(bs_config, framework):
  bstack111ll111_opy_ = False
  bstack1l1lllll_opy_ = False
  bstack1111l1l11l1_opy_ = False
  if bstack1l11lll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫἺ") in bs_config:
    bstack1111l1l11l1_opy_ = True
  elif bstack1l11lll_opy_ (u"ࠨࡣࡳࡴࠬἻ") in bs_config:
    bstack111ll111_opy_ = True
  else:
    bstack1l1lllll_opy_ = True
  bstack1ll1111l_opy_ = {
    bstack1l11lll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩἼ"): bstack111l1llll_opy_.bstack1111l11llll_opy_(bs_config, framework),
    bstack1l11lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪἽ"): bstack11ll1l1ll1_opy_.bstack11lll11l1l_opy_(bs_config),
    bstack1l11lll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪἾ"): bs_config.get(bstack1l11lll_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫἿ"), False),
    bstack1l11lll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨὀ"): bstack1l1lllll_opy_,
    bstack1l11lll_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ὁ"): bstack111ll111_opy_,
    bstack1l11lll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬὂ"): bstack1111l1l11l1_opy_
  }
  return bstack1ll1111l_opy_