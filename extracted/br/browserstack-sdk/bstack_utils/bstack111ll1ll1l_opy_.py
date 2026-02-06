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
import logging
import datetime
import threading
from bstack_utils.helper import bstack11l1l1l1ll1_opy_, bstack11ll1lll1l_opy_, get_host_info, bstack111l1l111l1_opy_, \
 bstack1l111lll1l_opy_, bstack1l1ll1ll1_opy_, error_handler, bstack1111lllll1l_opy_, bstack1lll11lll1_opy_
import bstack_utils.accessibility as bstack11l1llll11_opy_
from bstack_utils.bstack1lll1111l1_opy_ import bstack11l1lll11_opy_
from bstack_utils.bstack1111l1lll1_opy_ import bstack1l1l11llll_opy_
from bstack_utils.percy import bstack111llll1l1_opy_
from bstack_utils.config import Config
bstack1l111111_opy_ = Config.bstack1llll1l111_opy_()
logger = logging.getLogger(__name__)
percy = bstack111llll1l1_opy_()
@error_handler(class_method=False)
def bstack1lll11l1l111_opy_(bs_config, bstack1l1l111111_opy_):
  try:
    data = {
        bstack11lllll_opy_ (u"ࠨࡨࡲࡶࡲࡧࡴࠨ⍕"): bstack11lllll_opy_ (u"ࠩ࡭ࡷࡴࡴࠧ⍖"),
        bstack11lllll_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡣࡳࡧ࡭ࡦࠩ⍗"): bs_config.get(bstack11lllll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ⍘"), bstack11lllll_opy_ (u"ࠬ࠭⍙")),
        bstack11lllll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⍚"): bs_config.get(bstack11lllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ⍛"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack11lllll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ⍜"): bs_config.get(bstack11lllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ⍝")),
        bstack11lllll_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ⍞"): bs_config.get(bstack11lllll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ⍟"), bstack11lllll_opy_ (u"ࠬ࠭⍠")),
        bstack11lllll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⍡"): bstack1lll11lll1_opy_(),
        bstack11lllll_opy_ (u"ࠧࡵࡣࡪࡷࠬ⍢"): bstack111l1l111l1_opy_(bs_config),
        bstack11lllll_opy_ (u"ࠨࡪࡲࡷࡹࡥࡩ࡯ࡨࡲࠫ⍣"): get_host_info(),
        bstack11lllll_opy_ (u"ࠩࡦ࡭ࡤ࡯࡮ࡧࡱࠪ⍤"): bstack11ll1lll1l_opy_(),
        bstack11lllll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡵࡹࡳࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ⍥"): os.environ.get(bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪ⍦")),
        bstack11lllll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࡤࡺࡥࡴࡶࡶࡣࡷ࡫ࡲࡶࡰࠪ⍧"): os.environ.get(bstack11lllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠫ⍨"), False),
        bstack11lllll_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࡠࡥࡲࡲࡹࡸ࡯࡭ࠩ⍩"): bstack11l1l1l1ll1_opy_(),
        bstack11lllll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⍪"): bstack1lll111llll1_opy_(bs_config),
        bstack11lllll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡪࡥࡵࡣ࡬ࡰࡸ࠭⍫"): bstack1lll111lllll_opy_(bstack1l1l111111_opy_),
        bstack11lllll_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨ⍬"): bstack1lll11l1111l_opy_(bs_config, bstack1l1l111111_opy_.get(bstack11lllll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬ⍭"), bstack11lllll_opy_ (u"ࠬ࠭⍮"))),
        bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ⍯"): bstack1l111lll1l_opy_(bs_config),
        bstack11lllll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠬ⍰"): bstack1lll111lll11_opy_(bs_config)
    }
    return data
  except Exception as error:
    logger.error(bstack11lllll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡶࡡࡺ࡮ࡲࡥࡩࠦࡦࡰࡴࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࠦࡻࡾࠤ⍱").format(str(error)))
    return None
def bstack1lll111lllll_opy_(framework):
  return {
    bstack11lllll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡓࡧ࡭ࡦࠩ⍲"): framework.get(bstack11lllll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࠫ⍳"), bstack11lllll_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫ⍴")),
    bstack11lllll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ⍵"): framework.get(bstack11lllll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ⍶")),
    bstack11lllll_opy_ (u"ࠧࡴࡦ࡮࡚ࡪࡸࡳࡪࡱࡱࠫ⍷"): framework.get(bstack11lllll_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭⍸")),
    bstack11lllll_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫ⍹"): bstack11lllll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ⍺"),
    bstack11lllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ⍻"): framework.get(bstack11lllll_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ⍼"))
  }
def bstack1lll111lll11_opy_(bs_config):
  bstack11lllll_opy_ (u"ࠨࠢࠣࠌࠣࠤࡗ࡫ࡴࡶࡴࡱࡷࠥࡺࡨࡦࠢࡷࡩࡸࡺࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡥࡹ࡮ࡲࡤࠡࡵࡷࡥࡷࡺ࠮ࠋࠢࠣࠦࠧࠨ⍽")
  if not bs_config:
    return {}
  bstack111111lll11_opy_ = bstack11l1lll11_opy_(bs_config).bstack111111ll1l1_opy_(bs_config)
  return bstack111111lll11_opy_
def bstack1111l111_opy_(bs_config, framework):
  bstack1llll1l1l1_opy_ = False
  bstack1l1l1l1ll_opy_ = False
  bstack1lll111l1lll_opy_ = False
  if bstack11lllll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ⍾") in bs_config:
    bstack1lll111l1lll_opy_ = True
  elif bstack11lllll_opy_ (u"ࠨࡣࡳࡴࠬ⍿") in bs_config:
    bstack1llll1l1l1_opy_ = True
  else:
    bstack1l1l1l1ll_opy_ = True
  bstack1l1l111ll1_opy_ = {
    bstack11lllll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⎀"): bstack1l1l11llll_opy_.bstack1lll111lll1l_opy_(bs_config, framework),
    bstack11lllll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⎁"): bstack11l1llll11_opy_.bstack1lll1lll1l_opy_(bs_config),
    bstack11lllll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ⎂"): bs_config.get(bstack11lllll_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ⎃"), False),
    bstack11lllll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ⎄"): bstack1l1l1l1ll_opy_,
    bstack11lllll_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭⎅"): bstack1llll1l1l1_opy_,
    bstack11lllll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬ⎆"): bstack1lll111l1lll_opy_
  }
  return bstack1l1l111ll1_opy_
@error_handler(class_method=False)
def bstack1lll111llll1_opy_(bs_config):
  try:
    bstack1lll111ll1ll_opy_ = json.loads(os.getenv(bstack11lllll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ⎇"), bstack11lllll_opy_ (u"ࠪࡿࢂ࠭⎈")))
    bstack1lll111ll1ll_opy_ = bstack1lll11l111l1_opy_(bs_config, bstack1lll111ll1ll_opy_)
    return {
        bstack11lllll_opy_ (u"ࠫࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭⎉"): bstack1lll111ll1ll_opy_
    }
  except Exception as error:
    logger.error(bstack11lllll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠡࡨࡲࡶ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࠡࡽࢀࠦ⎊").format(str(error)))
    return {}
def bstack1lll11l111l1_opy_(bs_config, bstack1lll111ll1ll_opy_):
  if ((bstack11lllll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ⎋") in bs_config or not bstack1l111lll1l_opy_(bs_config)) and bstack11l1llll11_opy_.bstack1lll1lll1l_opy_(bs_config)):
    bstack1lll111ll1ll_opy_[bstack11lllll_opy_ (u"ࠢࡪࡰࡦࡰࡺࡪࡥࡆࡰࡦࡳࡩ࡫ࡤࡆࡺࡷࡩࡳࡹࡩࡰࡰࠥ⎌")] = True
  return bstack1lll111ll1ll_opy_
def bstack1lll11ll1l11_opy_(array, bstack1lll111ll11l_opy_, bstack1lll111l1ll1_opy_):
  result = {}
  for o in array:
    key = o[bstack1lll111ll11l_opy_]
    result[key] = o[bstack1lll111l1ll1_opy_]
  return result
def bstack1lll11ll1111_opy_(bstack11l11l111l_opy_=bstack11lllll_opy_ (u"ࠨࠩ⎍")):
  bstack1lll11l11111_opy_ = bstack11l1llll11_opy_.on()
  bstack1lll111l1l1l_opy_ = bstack1l1l11llll_opy_.on()
  bstack1lll111ll111_opy_ = percy.bstack11l1l1ll_opy_()
  if bstack1lll111ll111_opy_ and not bstack1lll111l1l1l_opy_ and not bstack1lll11l11111_opy_:
    return bstack11l11l111l_opy_ not in [bstack11lllll_opy_ (u"ࠩࡆࡆ࡙࡙ࡥࡴࡵ࡬ࡳࡳࡉࡲࡦࡣࡷࡩࡩ࠭⎎"), bstack11lllll_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧ⎏")]
  elif bstack1lll11l11111_opy_ and not bstack1lll111l1l1l_opy_:
    return bstack11l11l111l_opy_ not in [bstack11lllll_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ⎐"), bstack11lllll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⎑"), bstack11lllll_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪ⎒")]
  return bstack1lll11l11111_opy_ or bstack1lll111l1l1l_opy_ or bstack1lll111ll111_opy_
@error_handler(class_method=False)
def bstack1lll11l11l1l_opy_(bstack11l11l111l_opy_, test=None):
  bstack1lll111ll1l1_opy_ = bstack11l1llll11_opy_.on()
  if not bstack1lll111ll1l1_opy_ or bstack11l11l111l_opy_ not in [bstack11lllll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ⎓")] or test == None:
    return None
  return {
    bstack11lllll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⎔"): bstack1lll111ll1l1_opy_ and bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ⎕"), None) == True and bstack11l1llll11_opy_.bstack1l11lll111_opy_(test[bstack11lllll_opy_ (u"ࠪࡸࡦ࡭ࡳࠨ⎖")])
  }
def bstack1lll11l1111l_opy_(bs_config, framework):
  bstack1llll1l1l1_opy_ = False
  bstack1l1l1l1ll_opy_ = False
  bstack1lll111l1lll_opy_ = False
  if bstack11lllll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ⎗") in bs_config:
    bstack1lll111l1lll_opy_ = True
  elif bstack11lllll_opy_ (u"ࠬࡧࡰࡱࠩ⎘") in bs_config:
    bstack1llll1l1l1_opy_ = True
  else:
    bstack1l1l1l1ll_opy_ = True
  bstack1l1l111ll1_opy_ = {
    bstack11lllll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⎙"): bstack1l1l11llll_opy_.bstack1lll111lll1l_opy_(bs_config, framework),
    bstack11lllll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⎚"): bstack11l1llll11_opy_.bstack1lll1l11ll_opy_(bs_config),
    bstack11lllll_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ⎛"): bs_config.get(bstack11lllll_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ⎜"), False),
    bstack11lllll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ⎝"): bstack1l1l1l1ll_opy_,
    bstack11lllll_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪ⎞"): bstack1llll1l1l1_opy_,
    bstack11lllll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩ⎟"): bstack1lll111l1lll_opy_
  }
  return bstack1l1l111ll1_opy_