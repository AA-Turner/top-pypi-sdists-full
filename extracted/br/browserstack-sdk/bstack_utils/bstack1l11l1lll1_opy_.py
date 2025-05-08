# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack11lll1lllll_opy_, bstack1l1l1ll1l_opy_, get_host_info, bstack11l1l11111l_opy_, \
 bstack1lll111l1l_opy_, bstack1l111l11_opy_, bstack111ll1ll1l_opy_, bstack11l1l1l111l_opy_, bstack1l1ll1ll_opy_
import bstack_utils.accessibility as bstack1l1l1l11l_opy_
from bstack_utils.bstack11l111l111_opy_ import bstack1l11ll11ll_opy_
from bstack_utils.percy import bstack11ll1lllll_opy_
from bstack_utils.config import Config
bstack11l1l1l1l_opy_ = Config.bstack1l111l11l_opy_()
logger = logging.getLogger(__name__)
percy = bstack11ll1lllll_opy_()
@bstack111ll1ll1l_opy_(class_method=False)
def bstack1111lll11ll_opy_(bs_config, bstack1l11111l_opy_):
  try:
    data = {
        bstack1l1lll_opy_ (u"ࠨࡨࡲࡶࡲࡧࡴࠨἃ"): bstack1l1lll_opy_ (u"ࠩ࡭ࡷࡴࡴࠧἄ"),
        bstack1l1lll_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡣࡳࡧ࡭ࡦࠩἅ"): bs_config.get(bstack1l1lll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩἆ"), bstack1l1lll_opy_ (u"ࠬ࠭ἇ")),
        bstack1l1lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫἈ"): bs_config.get(bstack1l1lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪἉ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1l1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫἊ"): bs_config.get(bstack1l1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫἋ")),
        bstack1l1lll_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨἌ"): bs_config.get(bstack1l1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧἍ"), bstack1l1lll_opy_ (u"ࠬ࠭Ἆ")),
        bstack1l1lll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪἏ"): bstack1l1ll1ll_opy_(),
        bstack1l1lll_opy_ (u"ࠧࡵࡣࡪࡷࠬἐ"): bstack11l1l11111l_opy_(bs_config),
        bstack1l1lll_opy_ (u"ࠨࡪࡲࡷࡹࡥࡩ࡯ࡨࡲࠫἑ"): get_host_info(),
        bstack1l1lll_opy_ (u"ࠩࡦ࡭ࡤ࡯࡮ࡧࡱࠪἒ"): bstack1l1l1ll1l_opy_(),
        bstack1l1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡵࡹࡳࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪἓ"): os.environ.get(bstack1l1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪἔ")),
        bstack1l1lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࡤࡺࡥࡴࡶࡶࡣࡷ࡫ࡲࡶࡰࠪἕ"): os.environ.get(bstack1l1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠫ἖"), False),
        bstack1l1lll_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࡠࡥࡲࡲࡹࡸ࡯࡭ࠩ἗"): bstack11lll1lllll_opy_(),
        bstack1l1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨἘ"): bstack1111l1ll11l_opy_(),
        bstack1l1lll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡪࡥࡵࡣ࡬ࡰࡸ࠭Ἑ"): bstack1111l1ll111_opy_(bstack1l11111l_opy_),
        bstack1l1lll_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨἚ"): bstack1111l1l111l_opy_(bs_config, bstack1l11111l_opy_.get(bstack1l1lll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬἛ"), bstack1l1lll_opy_ (u"ࠬ࠭Ἔ"))),
        bstack1l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨἝ"): bstack1lll111l1l_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack1l1lll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡵࡧࡹ࡭ࡱࡤࡨࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࠥࢁࡽࠣ἞").format(str(error)))
    return None
def bstack1111l1ll111_opy_(framework):
  return {
    bstack1l1lll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡒࡦࡳࡥࠨ἟"): framework.get(bstack1l1lll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࠪἠ"), bstack1l1lll_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪἡ")),
    bstack1l1lll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧἢ"): framework.get(bstack1l1lll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩἣ")),
    bstack1l1lll_opy_ (u"࠭ࡳࡥ࡭࡙ࡩࡷࡹࡩࡰࡰࠪἤ"): framework.get(bstack1l1lll_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬἥ")),
    bstack1l1lll_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪἦ"): bstack1l1lll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩἧ"),
    bstack1l1lll_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪἨ"): framework.get(bstack1l1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫἩ"))
  }
def bstack1llll1l1ll_opy_(bs_config, framework):
  bstack11ll11lll_opy_ = False
  bstack1l1l11l11_opy_ = False
  bstack1111l1l1l11_opy_ = False
  if bstack1l1lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩἪ") in bs_config:
    bstack1111l1l1l11_opy_ = True
  elif bstack1l1lll_opy_ (u"࠭ࡡࡱࡲࠪἫ") in bs_config:
    bstack11ll11lll_opy_ = True
  else:
    bstack1l1l11l11_opy_ = True
  bstack1ll1l11ll_opy_ = {
    bstack1l1lll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧἬ"): bstack1l11ll11ll_opy_.bstack1111l11llll_opy_(bs_config, framework),
    bstack1l1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨἭ"): bstack1l1l1l11l_opy_.bstack111ll1ll1_opy_(bs_config),
    bstack1l1lll_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨἮ"): bs_config.get(bstack1l1lll_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩἯ"), False),
    bstack1l1lll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ἰ"): bstack1l1l11l11_opy_,
    bstack1l1lll_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫἱ"): bstack11ll11lll_opy_,
    bstack1l1lll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪἲ"): bstack1111l1l1l11_opy_
  }
  return bstack1ll1l11ll_opy_
@bstack111ll1ll1l_opy_(class_method=False)
def bstack1111l1ll11l_opy_():
  try:
    bstack1111l1l1lll_opy_ = json.loads(os.getenv(bstack1l1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨἳ"), bstack1l1lll_opy_ (u"ࠨࡽࢀࠫἴ")))
    return {
        bstack1l1lll_opy_ (u"ࠩࡶࡩࡹࡺࡩ࡯ࡩࡶࠫἵ"): bstack1111l1l1lll_opy_
    }
  except Exception as error:
    logger.error(bstack1l1lll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸࠦࡦࡰࡴࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࠦࡻࡾࠤἶ").format(str(error)))
    return {}
def bstack1111ll1ll11_opy_(array, bstack1111l1l1l1l_opy_, bstack1111l1l11ll_opy_):
  result = {}
  for o in array:
    key = o[bstack1111l1l1l1l_opy_]
    result[key] = o[bstack1111l1l11ll_opy_]
  return result
def bstack1111l1ll1ll_opy_(bstack11l1l1l1l1_opy_=bstack1l1lll_opy_ (u"ࠫࠬἷ")):
  bstack1111l1l1ll1_opy_ = bstack1l1l1l11l_opy_.on()
  bstack1111l1l1111_opy_ = bstack1l11ll11ll_opy_.on()
  bstack1111l1ll1l1_opy_ = percy.bstack1llllllll_opy_()
  if bstack1111l1ll1l1_opy_ and not bstack1111l1l1111_opy_ and not bstack1111l1l1ll1_opy_:
    return bstack11l1l1l1l1_opy_ not in [bstack1l1lll_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩἸ"), bstack1l1lll_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪἹ")]
  elif bstack1111l1l1ll1_opy_ and not bstack1111l1l1111_opy_:
    return bstack11l1l1l1l1_opy_ not in [bstack1l1lll_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨἺ"), bstack1l1lll_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪἻ"), bstack1l1lll_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭Ἴ")]
  return bstack1111l1l1ll1_opy_ or bstack1111l1l1111_opy_ or bstack1111l1ll1l1_opy_
@bstack111ll1ll1l_opy_(class_method=False)
def bstack1111l1lllll_opy_(bstack11l1l1l1l1_opy_, test=None):
  bstack1111l1l11l1_opy_ = bstack1l1l1l11l_opy_.on()
  if not bstack1111l1l11l1_opy_ or bstack11l1l1l1l1_opy_ not in [bstack1l1lll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬἽ")] or test == None:
    return None
  return {
    bstack1l1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫἾ"): bstack1111l1l11l1_opy_ and bstack1l111l11_opy_(threading.current_thread(), bstack1l1lll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫἿ"), None) == True and bstack1l1l1l11l_opy_.bstack1ll1llll11_opy_(test[bstack1l1lll_opy_ (u"࠭ࡴࡢࡩࡶࠫὀ")])
  }
def bstack1111l1l111l_opy_(bs_config, framework):
  bstack11ll11lll_opy_ = False
  bstack1l1l11l11_opy_ = False
  bstack1111l1l1l11_opy_ = False
  if bstack1l1lll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫὁ") in bs_config:
    bstack1111l1l1l11_opy_ = True
  elif bstack1l1lll_opy_ (u"ࠨࡣࡳࡴࠬὂ") in bs_config:
    bstack11ll11lll_opy_ = True
  else:
    bstack1l1l11l11_opy_ = True
  bstack1ll1l11ll_opy_ = {
    bstack1l1lll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩὃ"): bstack1l11ll11ll_opy_.bstack1111l11llll_opy_(bs_config, framework),
    bstack1l1lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪὄ"): bstack1l1l1l11l_opy_.bstack1ll11ll111_opy_(bs_config),
    bstack1l1lll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪὅ"): bs_config.get(bstack1l1lll_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ὆"), False),
    bstack1l1lll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ὇"): bstack1l1l11l11_opy_,
    bstack1l1lll_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭Ὀ"): bstack11ll11lll_opy_,
    bstack1l1lll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬὉ"): bstack1111l1l1l11_opy_
  }
  return bstack1ll1l11ll_opy_