# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack11l1ll11lll_opy_, bstack11l1lll11l_opy_, get_host_info, bstack111l1ll1l1l_opy_, \
 bstack1l1l1111l1_opy_, bstack111ll1l1_opy_, error_handler, bstack111l1l11l11_opy_, bstack1ll1llll11_opy_
import bstack_utils.accessibility as bstack1l11l1l1l_opy_
from bstack_utils.bstack1l1ll1l111_opy_ import bstack11111l1l_opy_
from bstack_utils.bstack1111llll11_opy_ import bstack1ll11l1l1l_opy_
from bstack_utils.percy import bstack111llll11_opy_
from bstack_utils.config import Config
bstack11lll111l_opy_ = Config.bstack1l11l11l1_opy_()
logger = logging.getLogger(__name__)
percy = bstack111llll11_opy_()
@error_handler(class_method=False)
def bstack1lll11ll1l1l_opy_(bs_config, bstack1l11llll_opy_):
  try:
    data = {
        bstack11l1ll1_opy_ (u"ࠫ࡫ࡵࡲ࡮ࡣࡷࠫ⌵"): bstack11l1ll1_opy_ (u"ࠬࡰࡳࡰࡰࠪ⌶"),
        bstack11l1ll1_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺ࡟࡯ࡣࡰࡩࠬ⌷"): bs_config.get(bstack11l1ll1_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ⌸"), bstack11l1ll1_opy_ (u"ࠨࠩ⌹")),
        bstack11l1ll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ⌺"): bs_config.get(bstack11l1ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭⌻"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack11l1ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ⌼"): bs_config.get(bstack11l1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ⌽")),
        bstack11l1ll1_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫ⌾"): bs_config.get(bstack11l1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ⌿"), bstack11l1ll1_opy_ (u"ࠨࠩ⍀")),
        bstack11l1ll1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⍁"): bstack1ll1llll11_opy_(),
        bstack11l1ll1_opy_ (u"ࠪࡸࡦ࡭ࡳࠨ⍂"): bstack111l1ll1l1l_opy_(bs_config),
        bstack11l1ll1_opy_ (u"ࠫ࡭ࡵࡳࡵࡡ࡬ࡲ࡫ࡵࠧ⍃"): get_host_info(),
        bstack11l1ll1_opy_ (u"ࠬࡩࡩࡠ࡫ࡱࡪࡴ࠭⍄"): bstack11l1lll11l_opy_(),
        bstack11l1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡸࡵ࡯ࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭⍅"): os.environ.get(bstack11l1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭⍆")),
        bstack11l1ll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࡠࡶࡨࡷࡹࡹ࡟ࡳࡧࡵࡹࡳ࠭⍇"): os.environ.get(bstack11l1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠧ⍈"), False),
        bstack11l1ll1_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࡣࡨࡵ࡮ࡵࡴࡲࡰࠬ⍉"): bstack11l1ll11lll_opy_(),
        bstack11l1ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⍊"): bstack1lll11l11111_opy_(bs_config),
        bstack11l1ll1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡦࡨࡸࡦ࡯࡬ࡴࠩ⍋"): bstack1lll11l1l111_opy_(bstack1l11llll_opy_),
        bstack11l1ll1_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ࡟࡮ࡣࡳࠫ⍌"): bstack1lll11l1111l_opy_(bs_config, bstack1l11llll_opy_.get(bstack11l1ll1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨ⍍"), bstack11l1ll1_opy_ (u"ࠨࠩ⍎"))),
        bstack11l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ⍏"): bstack1l1l1111l1_opy_(bs_config),
        bstack11l1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠨ⍐"): bstack1lll11l11lll_opy_(bs_config)
    }
    return data
  except Exception as error:
    logger.error(bstack11l1ll1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡲࡤࡽࡱࡵࡡࡥࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࠢࡾࢁࠧ⍑").format(str(error)))
    return None
def bstack1lll11l1l111_opy_(framework):
  return {
    bstack11l1ll1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡏࡣࡰࡩࠬ⍒"): framework.get(bstack11l1ll1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࠧ⍓"), bstack11l1ll1_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧ⍔")),
    bstack11l1ll1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫ⍕"): framework.get(bstack11l1ll1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭⍖")),
    bstack11l1ll1_opy_ (u"ࠪࡷࡩࡱࡖࡦࡴࡶ࡭ࡴࡴࠧ⍗"): framework.get(bstack11l1ll1_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ⍘")),
    bstack11l1ll1_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠧ⍙"): bstack11l1ll1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭⍚"),
    bstack11l1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ⍛"): framework.get(bstack11l1ll1_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ⍜"))
  }
def bstack1lll11l11lll_opy_(bs_config):
  bstack11l1ll1_opy_ (u"ࠤࠥࠦࠏࠦࠠࡓࡧࡷࡹࡷࡴࡳࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥࡨࡵࡪ࡮ࡧࠤࡸࡺࡡࡳࡶ࠱ࠎࠥࠦࠢࠣࠤ⍝")
  if not bs_config:
    return {}
  bstack111111llll1_opy_ = bstack11111l1l_opy_(bs_config).bstack1111111l1l1_opy_(bs_config)
  return bstack111111llll1_opy_
def bstack1l111lll1l_opy_(bs_config, framework):
  bstack11111111l_opy_ = False
  bstack1l1111l1l1_opy_ = False
  bstack1lll11l11ll1_opy_ = False
  if bstack11l1ll1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ⍞") in bs_config:
    bstack1lll11l11ll1_opy_ = True
  elif bstack11l1ll1_opy_ (u"ࠫࡦࡶࡰࠨ⍟") in bs_config:
    bstack11111111l_opy_ = True
  else:
    bstack1l1111l1l1_opy_ = True
  bstack1l1l11l11_opy_ = {
    bstack11l1ll1_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⍠"): bstack1ll11l1l1l_opy_.bstack1lll111llll1_opy_(bs_config, framework),
    bstack11l1ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⍡"): bstack1l11l1l1l_opy_.bstack111l111l1_opy_(bs_config),
    bstack11l1ll1_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭⍢"): bs_config.get(bstack11l1ll1_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ⍣"), False),
    bstack11l1ll1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ⍤"): bstack1l1111l1l1_opy_,
    bstack11l1ll1_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩ⍥"): bstack11111111l_opy_,
    bstack11l1ll1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨ⍦"): bstack1lll11l11ll1_opy_
  }
  return bstack1l1l11l11_opy_
@error_handler(class_method=False)
def bstack1lll11l11111_opy_(bs_config):
  try:
    bstack1lll111lll1l_opy_ = json.loads(os.getenv(bstack11l1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭⍧"), bstack11l1ll1_opy_ (u"࠭ࡻࡾࠩ⍨")))
    bstack1lll111lll1l_opy_ = bstack1lll11l111ll_opy_(bs_config, bstack1lll111lll1l_opy_)
    return {
        bstack11l1ll1_opy_ (u"ࠧࡴࡧࡷࡸ࡮ࡴࡧࡴࠩ⍩"): bstack1lll111lll1l_opy_
    }
  except Exception as error:
    logger.error(bstack11l1ll1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥ࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡶࡩࡹࡺࡩ࡯ࡩࡶࠤ࡫ࡵࡲࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࠤࢀࢃࠢ⍪").format(str(error)))
    return {}
def bstack1lll11l111ll_opy_(bs_config, bstack1lll111lll1l_opy_):
  if ((bstack11l1ll1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭⍫") in bs_config or not bstack1l1l1111l1_opy_(bs_config)) and bstack1l11l1l1l_opy_.bstack111l111l1_opy_(bs_config)):
    bstack1lll111lll1l_opy_[bstack11l1ll1_opy_ (u"ࠥ࡭ࡳࡩ࡬ࡶࡦࡨࡉࡳࡩ࡯ࡥࡧࡧࡉࡽࡺࡥ࡯ࡵ࡬ࡳࡳࠨ⍬")] = True
  return bstack1lll111lll1l_opy_
def bstack1lll11lll11l_opy_(array, bstack1lll111lll11_opy_, bstack1lll111ll1ll_opy_):
  result = {}
  for o in array:
    key = o[bstack1lll111lll11_opy_]
    result[key] = o[bstack1lll111ll1ll_opy_]
  return result
def bstack1lll11ll1ll1_opy_(bstack1lllll1111_opy_=bstack11l1ll1_opy_ (u"ࠫࠬ⍭")):
  bstack1lll111lllll_opy_ = bstack1l11l1l1l_opy_.on()
  bstack1lll11l11l11_opy_ = bstack1ll11l1l1l_opy_.on()
  bstack1lll11l11l1l_opy_ = percy.bstack1l11l111l_opy_()
  if bstack1lll11l11l1l_opy_ and not bstack1lll11l11l11_opy_ and not bstack1lll111lllll_opy_:
    return bstack1lllll1111_opy_ not in [bstack11l1ll1_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩ⍮"), bstack11l1ll1_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪ⍯")]
  elif bstack1lll111lllll_opy_ and not bstack1lll11l11l11_opy_:
    return bstack1lllll1111_opy_ not in [bstack11l1ll1_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ⍰"), bstack11l1ll1_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⍱"), bstack11l1ll1_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭⍲")]
  return bstack1lll111lllll_opy_ or bstack1lll11l11l11_opy_ or bstack1lll11l11l1l_opy_
@error_handler(class_method=False)
def bstack1lll11l1llll_opy_(bstack1lllll1111_opy_, test=None):
  bstack1lll11l111l1_opy_ = bstack1l11l1l1l_opy_.on()
  if not bstack1lll11l111l1_opy_ or bstack1lllll1111_opy_ not in [bstack11l1ll1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⍳")] or test == None:
    return None
  return {
    bstack11l1ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⍴"): bstack1lll11l111l1_opy_ and bstack111ll1l1_opy_(threading.current_thread(), bstack11l1ll1_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ⍵"), None) == True and bstack1l11l1l1l_opy_.bstack1lll1l1lll_opy_(test[bstack11l1ll1_opy_ (u"࠭ࡴࡢࡩࡶࠫ⍶")])
  }
def bstack1lll11l1111l_opy_(bs_config, framework):
  bstack11111111l_opy_ = False
  bstack1l1111l1l1_opy_ = False
  bstack1lll11l11ll1_opy_ = False
  if bstack11l1ll1_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ⍷") in bs_config:
    bstack1lll11l11ll1_opy_ = True
  elif bstack11l1ll1_opy_ (u"ࠨࡣࡳࡴࠬ⍸") in bs_config:
    bstack11111111l_opy_ = True
  else:
    bstack1l1111l1l1_opy_ = True
  bstack1l1l11l11_opy_ = {
    bstack11l1ll1_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⍹"): bstack1ll11l1l1l_opy_.bstack1lll111llll1_opy_(bs_config, framework),
    bstack11l1ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⍺"): bstack1l11l1l1l_opy_.bstack1lllll111_opy_(bs_config),
    bstack11l1ll1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ⍻"): bs_config.get(bstack11l1ll1_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ⍼"), False),
    bstack11l1ll1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ⍽"): bstack1l1111l1l1_opy_,
    bstack11l1ll1_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭⍾"): bstack11111111l_opy_,
    bstack11l1ll1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬ⍿"): bstack1lll11l11ll1_opy_
  }
  return bstack1l1l11l11_opy_