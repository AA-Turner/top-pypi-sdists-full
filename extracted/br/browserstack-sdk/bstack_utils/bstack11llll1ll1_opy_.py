# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack1111ll11ll1_opy_, bstack1l11111l1l_opy_, get_host_info, bstack1llll1ll111l_opy_, \
 bstack11l1111l1l_opy_, bstack1llll11111_opy_, error_handler, bstack1lllllll1l11_opy_, bstack1lllllllll_opy_
import bstack_utils.accessibility as a11y
from bstack_utils.bstack1l111111l_opy_ import bstack111ll1ll_opy_
from bstack_utils.bstack1l1l1111_opy_ import bstack111l1l1l11_opy_
from bstack_utils.percy import bstack11llll1l1_opy_
from bstack_utils.config import Config
global_config = Config.bstack1lll111ll_opy_()
logger = logging.getLogger(__name__)
percy = bstack11llll1l1_opy_()
@error_handler(class_method=False)
def bstack1ll11l11llll_opy_(bs_config, bstack1l1111l11l_opy_):
  try:
    data = {
        bstack111l_opy_ (u"ࠬ࡬࡯ࡳ࡯ࡤࡸࠬ⡶"): bstack111l_opy_ (u"࠭ࡪࡴࡱࡱࠫ⡷"),
        bstack111l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡠࡰࡤࡱࡪ࠭⡸"): bs_config.get(bstack111l_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭⡹"), bstack111l_opy_ (u"ࠩࠪ⡺")),
        bstack111l_opy_ (u"ࠪࡲࡦࡳࡥࠨ⡻"): bs_config.get(bstack111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ⡼"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ⡽"): bs_config.get(bstack111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ⡾")),
        bstack111l_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬ⡿"): bs_config.get(bstack111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫ⢀"), bstack111l_opy_ (u"ࠩࠪ⢁")),
        bstack111l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⢂"): bstack1lllllllll_opy_(),
        bstack111l_opy_ (u"ࠫࡹࡧࡧࡴࠩ⢃"): bstack1llll1ll111l_opy_(bs_config),
        bstack111l_opy_ (u"ࠬ࡮࡯ࡴࡶࡢ࡭ࡳ࡬࡯ࠨ⢄"): get_host_info(),
        bstack111l_opy_ (u"࠭ࡣࡪࡡ࡬ࡲ࡫ࡵࠧ⢅"): bstack1l11111l1l_opy_(),
        bstack111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡲࡶࡰࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ⢆"): os.environ.get(bstack111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ⢇")),
        bstack111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡴࡨࡶࡺࡴࠧ⢈"): os.environ.get(bstack111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠨ⢉"), False),
        bstack111l_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࡤࡩ࡯࡯ࡶࡵࡳࡱ࠭⢊"): bstack1111ll11ll1_opy_(),
        bstack111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⢋"): bstack1ll11l111111_opy_(bs_config),
        bstack111l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡧࡩࡹࡧࡩ࡭ࡵࠪ⢌"): bstack1ll111lllll1_opy_(bstack1l1111l11l_opy_),
        bstack111l_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬ⢍"): bstack1ll111ll11ll_opy_(bs_config, bstack1l1111l11l_opy_.get(bstack111l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡺࡹࡥࡥࠩ⢎"), bstack111l_opy_ (u"ࠩࠪ⢏"))),
        bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ⢐"): bstack11l1111l1l_opy_(bs_config),
        bstack111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠩ⢑"): bstack1ll111llll11_opy_(bs_config)
    }
    return data
  except Exception as error:
    logger.error(bstack111l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡳࡥࡾࡲ࡯ࡢࡦࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࠣࡿࢂࠨ⢒").format(str(error)))
    return None
def bstack1ll111lllll1_opy_(framework):
  return {
    bstack111l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡐࡤࡱࡪ࠭⢓"): framework.get(bstack111l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠨ⢔"), bstack111l_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨ⢕")),
    bstack111l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬ⢖"): framework.get(bstack111l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ⢗")),
    bstack111l_opy_ (u"ࠫࡸࡪ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ⢘"): framework.get(bstack111l_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ⢙")),
    bstack111l_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨ⢚"): bstack111l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ⢛"),
    bstack111l_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ⢜"): framework.get(bstack111l_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ⢝"))
  }
def bstack1ll111llll11_opy_(bs_config):
  bstack111l_opy_ (u"ࠥࠦࠧࠐࠠࠡࡔࡨࡸࡺࡸ࡮ࡴࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡩࡧࡴࡢࠢࡩࡳࡷࠦࡢࡶ࡫࡯ࡨࠥࡹࡴࡢࡴࡷ࠲ࠏࠦࠠࠣࠤࠥ⢞")
  if not bs_config:
    return {}
  bstack1lll1111llll_opy_ = bstack111ll1ll_opy_(bs_config).bstack1lll11lll1l1_opy_(bs_config)
  return bstack1lll1111llll_opy_
def bstack1l1llll1l_opy_(bs_config, framework):
  bstack11l1ll1111_opy_ = False
  bstack1l11l1l1l_opy_ = False
  bstack1ll111ll1l1l_opy_ = False
  if bstack111l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ⢟") in bs_config:
    bstack1ll111ll1l1l_opy_ = True
  elif bstack111l_opy_ (u"ࠬࡧࡰࡱࠩ⢠") in bs_config:
    bstack11l1ll1111_opy_ = True
  else:
    bstack1l11l1l1l_opy_ = True
  bstack11lll1ll1l_opy_ = {
    bstack111l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⢡"): bstack111l1l1l11_opy_.bstack1ll111ll1l11_opy_(bs_config, framework),
    bstack111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⢢"): a11y.is_enabled_root(bs_config),
    bstack111l_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ⢣"): bs_config.get(bstack111l_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ⢤"), False),
    bstack111l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ⢥"): bstack1l11l1l1l_opy_,
    bstack111l_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪ⢦"): bstack11l1ll1111_opy_,
    bstack111l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩ⢧"): bstack1ll111ll1l1l_opy_
  }
  return bstack11lll1ll1l_opy_
@error_handler(class_method=False)
def bstack1ll11l111111_opy_(bs_config):
  try:
    bstack1ll111lll1l1_opy_ = json.loads(os.getenv(bstack111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ⢨"), bstack111l_opy_ (u"ࠧࡼࡿࠪ⢩")))
    bstack1ll111lll1l1_opy_ = bstack1ll111llll1l_opy_(bs_config, bstack1ll111lll1l1_opy_)
    return {
        bstack111l_opy_ (u"ࠨࡵࡨࡸࡹ࡯࡮ࡨࡵࠪ⢪"): bstack1ll111lll1l1_opy_
    }
  except Exception as error:
    logger.error(bstack111l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡷࡪࡺࡴࡪࡰࡪࡷࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࠥࢁࡽࠣ⢫").format(str(error)))
    return {}
def bstack1ll111llll1l_opy_(bs_config, bstack1ll111lll1l1_opy_):
  if ((bstack111l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ⢬") in bs_config or not bstack11l1111l1l_opy_(bs_config)) and a11y.is_enabled_root(bs_config)):
    bstack1ll111lll1l1_opy_[bstack111l_opy_ (u"ࠦ࡮ࡴࡣ࡭ࡷࡧࡩࡊࡴࡣࡰࡦࡨࡨࡊࡾࡴࡦࡰࡶ࡭ࡴࡴࠢ⢭")] = True
  return bstack1ll111lll1l1_opy_
def bstack1ll11l1l111l_opy_(array, bstack1ll111lll11l_opy_, bstack1ll111llllll_opy_):
  result = {}
  for o in array:
    key = o[bstack1ll111lll11l_opy_]
    result[key] = o[bstack1ll111llllll_opy_]
  return result
def bstack1ll11l1l11l1_opy_(bstack1l1111ll11_opy_=bstack111l_opy_ (u"ࠬ࠭⢮")):
  bstack1ll111ll1lll_opy_ = a11y.on()
  bstack1ll111ll1ll1_opy_ = bstack111l1l1l11_opy_.on()
  bstack1ll111lll111_opy_ = percy.bstack11l1111l1_opy_()
  if bstack1ll111lll111_opy_ and not bstack1ll111ll1ll1_opy_ and not bstack1ll111ll1lll_opy_:
    return bstack1l1111ll11_opy_ not in [bstack111l_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪ⢯"), bstack111l_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫ⢰")]
  elif bstack1ll111ll1lll_opy_ and not bstack1ll111ll1ll1_opy_:
    return bstack1l1111ll11_opy_ not in [bstack111l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ⢱"), bstack111l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⢲"), bstack111l_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧ⢳")]
  return bstack1ll111ll1lll_opy_ or bstack1ll111ll1ll1_opy_ or bstack1ll111lll111_opy_
@error_handler(class_method=False)
def bstack1ll11l1l11ll_opy_(bstack1l1111ll11_opy_, test=None):
  bstack1ll111lll1ll_opy_ = a11y.on()
  if not bstack1ll111lll1ll_opy_ or bstack1l1111ll11_opy_ not in [bstack111l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ⢴"), bstack111l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⢵"), bstack111l_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪ⢶")] or test == None:
    return None
  return {
    bstack111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⢷"): bstack1ll111lll1ll_opy_ and bstack1llll11111_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ⢸"), None) == True and a11y.is_enabled_testcase(test.get(bstack111l_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ⢹"), []))
  }
def bstack1ll111ll11ll_opy_(bs_config, framework):
  bstack11l1ll1111_opy_ = False
  bstack1l11l1l1l_opy_ = False
  bstack1ll111ll1l1l_opy_ = False
  if bstack111l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ⢺") in bs_config:
    bstack1ll111ll1l1l_opy_ = True
  elif bstack111l_opy_ (u"ࠫࡦࡶࡰࠨ⢻") in bs_config:
    bstack11l1ll1111_opy_ = True
  else:
    bstack1l11l1l1l_opy_ = True
  bstack11lll1ll1l_opy_ = {
    bstack111l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⢼"): bstack111l1l1l11_opy_.bstack1ll111ll1l11_opy_(bs_config, framework),
    bstack111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⢽"): a11y.bstack1lllll1l1ll_opy_(bs_config),
    bstack111l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭⢾"): bs_config.get(bstack111l_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ⢿"), False),
    bstack111l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ⣀"): bstack1l11l1l1l_opy_,
    bstack111l_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩ⣁"): bstack11l1ll1111_opy_,
    bstack111l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨ⣂"): bstack1ll111ll1l1l_opy_
  }
  return bstack11lll1ll1l_opy_