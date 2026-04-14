# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack1111lll11ll_opy_, bstack1l111ll1l1_opy_, get_host_info, bstack1lllll1lll1l_opy_, \
 bstack11llll1lll_opy_, bstack1l111l11l_opy_, error_handler, bstack1llllll11ll1_opy_, bstack111111l1l_opy_
import bstack_utils.accessibility as a11y
from bstack_utils.bstack1111l11l_opy_ import bstack1l1l111111_opy_
from bstack_utils.bstack1lll111111_opy_ import bstack1l1ll1l1ll_opy_
from bstack_utils.percy import bstack1llll1l11_opy_
from bstack_utils.config import Config
global_config = Config.bstack1ll11ll111_opy_()
logger = logging.getLogger(__name__)
percy = bstack1llll1l11_opy_()
@error_handler(class_method=False)
def bstack1ll111lllll1_opy_(bs_config, bstack1l1l1l111l_opy_):
  try:
    data = {
        bstack1l111l_opy_ (u"࠭ࡦࡰࡴࡰࡥࡹ࠭⢓"): bstack1l111l_opy_ (u"ࠧ࡫ࡵࡲࡲࠬ⢔"),
        bstack1l111l_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡡࡱࡥࡲ࡫ࠧ⢕"): bs_config.get(bstack1l111l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ⢖"), bstack1l111l_opy_ (u"ࠪࠫ⢗")),
        bstack1l111l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⢘"): bs_config.get(bstack1l111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ⢙"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1l111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ⢚"): bs_config.get(bstack1l111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ⢛")),
        bstack1l111l_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭⢜"): bs_config.get(bstack1l111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬ⢝"), bstack1l111l_opy_ (u"ࠪࠫ⢞")),
        bstack1l111l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⢟"): bstack111111l1l_opy_(),
        bstack1l111l_opy_ (u"ࠬࡺࡡࡨࡵࠪ⢠"): bstack1lllll1lll1l_opy_(bs_config),
        bstack1l111l_opy_ (u"࠭ࡨࡰࡵࡷࡣ࡮ࡴࡦࡰࠩ⢡"): get_host_info(),
        bstack1l111l_opy_ (u"ࠧࡤ࡫ࡢ࡭ࡳ࡬࡯ࠨ⢢"): bstack1l111ll1l1_opy_(),
        bstack1l111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡳࡷࡱࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ⢣"): os.environ.get(bstack1l111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨ⢤")),
        bstack1l111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࡡࡵࡩࡷࡻ࡮ࠨ⢥"): os.environ.get(bstack1l111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠩ⢦"), False),
        bstack1l111l_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࡥࡣࡰࡰࡷࡶࡴࡲࠧ⢧"): bstack1111lll11ll_opy_(),
        bstack1l111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⢨"): bstack1ll111ll1ll1_opy_(bs_config),
        bstack1l111l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡨࡪࡺࡡࡪ࡮ࡶࠫ⢩"): bstack1ll111ll1111_opy_(bstack1l1l1l111l_opy_),
        bstack1l111l_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭⢪"): bstack1ll111lll111_opy_(bs_config, bstack1l1l1l111l_opy_.get(bstack1l111l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦࠪ⢫"), bstack1l111l_opy_ (u"ࠪࠫ⢬"))),
        bstack1l111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭⢭"): bstack11llll1lll_opy_(bs_config),
        bstack1l111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠪ⢮"): bstack1ll111l1l1ll_opy_(bs_config)
    }
    return data
  except Exception as error:
    logger.error(bstack1l111l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡴࡦࡿ࡬ࡰࡣࡧࠤ࡫ࡵࡲࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࠤࢀࢃࠢ⢯").format(str(error)))
    return None
def bstack1ll111ll1111_opy_(framework):
  return {
    bstack1l111l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡑࡥࡲ࡫ࠧ⢰"): framework.get(bstack1l111l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࠩ⢱"), bstack1l111l_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩ⢲")),
    bstack1l111l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭⢳"): framework.get(bstack1l111l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ⢴")),
    bstack1l111l_opy_ (u"ࠬࡹࡤ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩ⢵"): framework.get(bstack1l111l_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ⢶")),
    bstack1l111l_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩ⢷"): bstack1l111l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ⢸"),
    bstack1l111l_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ⢹"): framework.get(bstack1l111l_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ⢺"))
  }
def bstack1ll111l1l1ll_opy_(bs_config):
  bstack1l111l_opy_ (u"ࠦࠧࠨࠊࠡࠢࡕࡩࡹࡻࡲ࡯ࡵࠣࡸ࡭࡫ࠠࡵࡧࡶࡸࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡣࡷ࡬ࡰࡩࠦࡳࡵࡣࡵࡸ࠳ࠐࠠࠡࠤࠥࠦ⢻")
  if not bs_config:
    return {}
  bstack1lll11111l11_opy_ = bstack1l1l111111_opy_(bs_config).bstack1lll111l11l1_opy_(bs_config)
  return bstack1lll11111l11_opy_
def bstack1111l1l11_opy_(bs_config, framework):
  bstack11l1l1l1l1_opy_ = False
  bstack1l111l1l11_opy_ = False
  bstack1ll111ll1lll_opy_ = False
  if bstack1l111l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ⢼") in bs_config:
    bstack1ll111ll1lll_opy_ = True
  elif bstack1l111l_opy_ (u"࠭ࡡࡱࡲࠪ⢽") in bs_config:
    bstack11l1l1l1l1_opy_ = True
  else:
    bstack1l111l1l11_opy_ = True
  bstack111llll11l_opy_ = {
    bstack1l111l_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ⢾"): bstack1l1ll1l1ll_opy_.bstack1ll111l1ll11_opy_(bs_config, framework),
    bstack1l111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⢿"): a11y.is_enabled_root(bs_config),
    bstack1l111l_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ⣀"): bs_config.get(bstack1l111l_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ⣁"), False),
    bstack1l111l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭⣂"): bstack1l111l1l11_opy_,
    bstack1l111l_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ⣃"): bstack11l1l1l1l1_opy_,
    bstack1l111l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪ⣄"): bstack1ll111ll1lll_opy_
  }
  return bstack111llll11l_opy_
@error_handler(class_method=False)
def bstack1ll111ll1ll1_opy_(bs_config):
  try:
    bstack1ll111ll11l1_opy_ = json.loads(os.getenv(bstack1l111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ⣅"), bstack1l111l_opy_ (u"ࠨࡽࢀࠫ⣆")))
    bstack1ll111ll11l1_opy_ = bstack1ll111l1llll_opy_(bs_config, bstack1ll111ll11l1_opy_)
    return {
        bstack1l111l_opy_ (u"ࠩࡶࡩࡹࡺࡩ࡯ࡩࡶࠫ⣇"): bstack1ll111ll11l1_opy_
    }
  except Exception as error:
    logger.error(bstack1l111l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸࠦࡦࡰࡴࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࠦࡻࡾࠤ⣈").format(str(error)))
    return {}
def bstack1ll111l1llll_opy_(bs_config, bstack1ll111ll11l1_opy_):
  if ((bstack1l111l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ⣉") in bs_config or not bstack11llll1lll_opy_(bs_config)) and a11y.is_enabled_root(bs_config)):
    bstack1ll111ll11l1_opy_[bstack1l111l_opy_ (u"ࠧ࡯࡮ࡤ࡮ࡸࡨࡪࡋ࡮ࡤࡱࡧࡩࡩࡋࡸࡵࡧࡱࡷ࡮ࡵ࡮ࠣ⣊")] = True
  return bstack1ll111ll11l1_opy_
def bstack1ll111lll11l_opy_(array, bstack1ll111ll11ll_opy_, bstack1ll111ll1l1l_opy_):
  result = {}
  for o in array:
    key = o[bstack1ll111ll11ll_opy_]
    result[key] = o[bstack1ll111ll1l1l_opy_]
  return result
def bstack1ll111llll1l_opy_(bstack1111ll11ll_opy_=bstack1l111l_opy_ (u"࠭ࠧ⣋")):
  bstack1ll111l1ll1l_opy_ = a11y.on()
  bstack1ll111ll1l11_opy_ = bstack1l1ll1l1ll_opy_.on()
  bstack1ll111l1lll1_opy_ = percy.bstack1111l11l11_opy_()
  if bstack1ll111l1lll1_opy_ and not bstack1ll111ll1l11_opy_ and not bstack1ll111l1ll1l_opy_:
    return bstack1111ll11ll_opy_ not in [bstack1l111l_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫ⣌"), bstack1l111l_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬ⣍")]
  elif bstack1ll111l1ll1l_opy_ and not bstack1ll111ll1l11_opy_:
    return bstack1111ll11ll_opy_ not in [bstack1l111l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ⣎"), bstack1l111l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⣏"), bstack1l111l_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨ⣐")]
  return bstack1ll111l1ll1l_opy_ or bstack1ll111ll1l11_opy_ or bstack1ll111l1lll1_opy_
@error_handler(class_method=False)
def bstack1ll11l111l11_opy_(bstack1111ll11ll_opy_, test=None):
  bstack1ll111ll111l_opy_ = a11y.on()
  if not bstack1ll111ll111l_opy_ or bstack1111ll11ll_opy_ not in [bstack1l111l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭⣑"), bstack1l111l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⣒"), bstack1l111l_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫ⣓")] or test == None:
    return None
  return {
    bstack1l111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⣔"): bstack1ll111ll111l_opy_ and bstack1l111l11l_opy_(threading.current_thread(), bstack1l111l_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ⣕"), None) == True and a11y.is_enabled_testcase(test.get(bstack1l111l_opy_ (u"ࠪࡸࡦ࡭ࡳࠨ⣖"), []))
  }
def bstack1ll111lll111_opy_(bs_config, framework):
  bstack11l1l1l1l1_opy_ = False
  bstack1l111l1l11_opy_ = False
  bstack1ll111ll1lll_opy_ = False
  if bstack1l111l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ⣗") in bs_config:
    bstack1ll111ll1lll_opy_ = True
  elif bstack1l111l_opy_ (u"ࠬࡧࡰࡱࠩ⣘") in bs_config:
    bstack11l1l1l1l1_opy_ = True
  else:
    bstack1l111l1l11_opy_ = True
  bstack111llll11l_opy_ = {
    bstack1l111l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⣙"): bstack1l1ll1l1ll_opy_.bstack1ll111l1ll11_opy_(bs_config, framework),
    bstack1l111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⣚"): a11y.bstack1l1111111l_opy_(bs_config),
    bstack1l111l_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ⣛"): bs_config.get(bstack1l111l_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ⣜"), False),
    bstack1l111l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ⣝"): bstack1l111l1l11_opy_,
    bstack1l111l_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪ⣞"): bstack11l1l1l1l1_opy_,
    bstack1l111l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩ⣟"): bstack1ll111ll1lll_opy_
  }
  return bstack111llll11l_opy_