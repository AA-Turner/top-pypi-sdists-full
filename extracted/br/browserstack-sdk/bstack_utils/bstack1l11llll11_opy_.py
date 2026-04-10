# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack1111lll1l11_opy_, bstack1lll11l1ll_opy_, get_host_info, bstack1llll11lll1l_opy_, \
 bstack1lll1111ll_opy_, bstack1llll1lll_opy_, error_handler, bstack1lllll1lll1l_opy_, bstack11l1ll1ll_opy_
import bstack_utils.accessibility as a11y
from bstack_utils.bstack1ll1ll1ll_opy_ import bstack1l111111ll_opy_
from bstack_utils.bstack1l1l11l1_opy_ import bstack111l111ll1_opy_
from bstack_utils.percy import bstack1ll1l11l11_opy_
from bstack_utils.config import Config
global_config = Config.bstack1l111l1111_opy_()
logger = logging.getLogger(__name__)
percy = bstack1ll1l11l11_opy_()
@error_handler(class_method=False)
def bstack1ll11l1l1111_opy_(bs_config, bstack11ll1ll11_opy_):
  try:
    data = {
        bstack1ll_opy_ (u"ࠩࡩࡳࡷࡳࡡࡵࠩ⡺"): bstack1ll_opy_ (u"ࠪ࡮ࡸࡵ࡮ࠨ⡻"),
        bstack1ll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡤࡴࡡ࡮ࡧࠪ⡼"): bs_config.get(bstack1ll_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ⡽"), bstack1ll_opy_ (u"࠭ࠧ⡾")),
        bstack1ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ⡿"): bs_config.get(bstack1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ⢀"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ⢁"): bs_config.get(bstack1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ⢂")),
        bstack1ll_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩ⢃"): bs_config.get(bstack1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ⢄"), bstack1ll_opy_ (u"࠭ࠧ⢅")),
        bstack1ll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⢆"): bstack11l1ll1ll_opy_(),
        bstack1ll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭⢇"): bstack1llll11lll1l_opy_(bs_config),
        bstack1ll_opy_ (u"ࠩ࡫ࡳࡸࡺ࡟ࡪࡰࡩࡳࠬ⢈"): get_host_info(),
        bstack1ll_opy_ (u"ࠪࡧ࡮ࡥࡩ࡯ࡨࡲࠫ⢉"): bstack1lll11l1ll_opy_(),
        bstack1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡶࡺࡴ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ⢊"): os.environ.get(bstack1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ⢋")),
        bstack1ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࡤࡸࡥࡳࡷࡱࠫ⢌"): os.environ.get(bstack1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠬ⢍"), False),
        bstack1ll_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࡡࡦࡳࡳࡺࡲࡰ࡮ࠪ⢎"): bstack1111lll1l11_opy_(),
        bstack1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⢏"): bstack1ll111l1llll_opy_(bs_config),
        bstack1ll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡤࡦࡶࡤ࡭ࡱࡹࠧ⢐"): bstack1ll111ll11ll_opy_(bstack11ll1ll11_opy_),
        bstack1ll_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩ⢑"): bstack1ll111lll11l_opy_(bs_config, bstack11ll1ll11_opy_.get(bstack1ll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡷࡶࡩࡩ࠭⢒"), bstack1ll_opy_ (u"࠭ࠧ⢓"))),
        bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ⢔"): bstack1lll1111ll_opy_(bs_config),
        bstack1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠭⢕"): bstack1ll111ll11l1_opy_(bs_config)
    }
    return data
  except Exception as error:
    logger.error(bstack1ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡰࡢࡻ࡯ࡳࡦࡪࠠࡧࡱࡵࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࠠࡼࡿࠥ⢖").format(str(error)))
    return None
def bstack1ll111ll11ll_opy_(framework):
  return {
    bstack1ll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡔࡡ࡮ࡧࠪ⢗"): framework.get(bstack1ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࠬ⢘"), bstack1ll_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬ⢙")),
    bstack1ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩ⢚"): framework.get(bstack1ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ⢛")),
    bstack1ll_opy_ (u"ࠨࡵࡧ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬ⢜"): framework.get(bstack1ll_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ⢝")),
    bstack1ll_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬ⢞"): bstack1ll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ⢟"),
    bstack1ll_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ⢠"): framework.get(bstack1ll_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭⢡"))
  }
def bstack1ll111ll11l1_opy_(bs_config):
  bstack1ll_opy_ (u"ࠢࠣࠤࠍࠤࠥࡘࡥࡵࡷࡵࡲࡸࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣࡦࡺ࡯࡬ࡥࠢࡶࡸࡦࡸࡴ࠯ࠌࠣࠤࠧࠨࠢ⢢")
  if not bs_config:
    return {}
  bstack1lll1111l11l_opy_ = bstack1l111111ll_opy_(bs_config).bstack1lll11l111l1_opy_(bs_config)
  return bstack1lll1111l11l_opy_
def bstack11l11l11l_opy_(bs_config, framework):
  bstack11ll11ll11_opy_ = False
  bstack11lll11111_opy_ = False
  bstack1ll111ll1ll1_opy_ = False
  if bstack1ll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ⢣") in bs_config:
    bstack1ll111ll1ll1_opy_ = True
  elif bstack1ll_opy_ (u"ࠩࡤࡴࡵ࠭⢤") in bs_config:
    bstack11ll11ll11_opy_ = True
  else:
    bstack11lll11111_opy_ = True
  bstack111ll1l1ll_opy_ = {
    bstack1ll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ⢥"): bstack111l111ll1_opy_.bstack1ll111l1ll1l_opy_(bs_config, framework),
    bstack1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⢦"): a11y.is_enabled_root(bs_config),
    bstack1ll_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ⢧"): bs_config.get(bstack1ll_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ⢨"), False),
    bstack1ll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩ⢩"): bstack11lll11111_opy_,
    bstack1ll_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ⢪"): bstack11ll11ll11_opy_,
    bstack1ll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭⢫"): bstack1ll111ll1ll1_opy_
  }
  return bstack111ll1l1ll_opy_
@error_handler(class_method=False)
def bstack1ll111l1llll_opy_(bs_config):
  try:
    bstack1ll111ll111l_opy_ = json.loads(os.getenv(bstack1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ⢬"), bstack1ll_opy_ (u"ࠫࢀࢃࠧ⢭")))
    bstack1ll111ll111l_opy_ = bstack1ll111ll1l1l_opy_(bs_config, bstack1ll111ll111l_opy_)
    return {
        bstack1ll_opy_ (u"ࠬࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧ⢮"): bstack1ll111ll111l_opy_
    }
  except Exception as error:
    logger.error(bstack1ll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡴࡧࡷࡸ࡮ࡴࡧࡴࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࠢࡾࢁࠧ⢯").format(str(error)))
    return {}
def bstack1ll111ll1l1l_opy_(bs_config, bstack1ll111ll111l_opy_):
  if ((bstack1ll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ⢰") in bs_config or not bstack1lll1111ll_opy_(bs_config)) and a11y.is_enabled_root(bs_config)):
    bstack1ll111ll111l_opy_[bstack1ll_opy_ (u"ࠣ࡫ࡱࡧࡱࡻࡤࡦࡇࡱࡧࡴࡪࡥࡥࡇࡻࡸࡪࡴࡳࡪࡱࡱࠦ⢱")] = True
  return bstack1ll111ll111l_opy_
def bstack1ll11l111l1l_opy_(array, bstack1ll111lll1l1_opy_, bstack1ll111ll1111_opy_):
  result = {}
  for o in array:
    key = o[bstack1ll111lll1l1_opy_]
    result[key] = o[bstack1ll111ll1111_opy_]
  return result
def bstack1ll11l1111ll_opy_(bstack1l1l111l1_opy_=bstack1ll_opy_ (u"ࠩࠪ⢲")):
  bstack1ll111l1lll1_opy_ = a11y.on()
  bstack1ll111ll1lll_opy_ = bstack111l111ll1_opy_.on()
  bstack1ll111lll111_opy_ = percy.bstack11l11ll11l_opy_()
  if bstack1ll111lll111_opy_ and not bstack1ll111ll1lll_opy_ and not bstack1ll111l1lll1_opy_:
    return bstack1l1l111l1_opy_ not in [bstack1ll_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧ⢳"), bstack1ll_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨ⢴")]
  elif bstack1ll111l1lll1_opy_ and not bstack1ll111ll1lll_opy_:
    return bstack1l1l111l1_opy_ not in [bstack1ll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭⢵"), bstack1ll_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⢶"), bstack1ll_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫ⢷")]
  return bstack1ll111l1lll1_opy_ or bstack1ll111ll1lll_opy_ or bstack1ll111lll111_opy_
@error_handler(class_method=False)
def bstack1ll11l11l111_opy_(bstack1l1l111l1_opy_, test=None):
  bstack1ll111ll1l11_opy_ = a11y.on()
  if not bstack1ll111ll1l11_opy_ or bstack1l1l111l1_opy_ not in [bstack1ll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ⢸"), bstack1ll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⢹"), bstack1ll_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧ⢺")] or test == None:
    return None
  return {
    bstack1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⢻"): bstack1ll111ll1l11_opy_ and bstack1llll1lll_opy_(threading.current_thread(), bstack1ll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ⢼"), None) == True and a11y.is_enabled_testcase(test.get(bstack1ll_opy_ (u"࠭ࡴࡢࡩࡶࠫ⢽"), []))
  }
def bstack1ll111lll11l_opy_(bs_config, framework):
  bstack11ll11ll11_opy_ = False
  bstack11lll11111_opy_ = False
  bstack1ll111ll1ll1_opy_ = False
  if bstack1ll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ⢾") in bs_config:
    bstack1ll111ll1ll1_opy_ = True
  elif bstack1ll_opy_ (u"ࠨࡣࡳࡴࠬ⢿") in bs_config:
    bstack11ll11ll11_opy_ = True
  else:
    bstack11lll11111_opy_ = True
  bstack111ll1l1ll_opy_ = {
    bstack1ll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⣀"): bstack111l111ll1_opy_.bstack1ll111l1ll1l_opy_(bs_config, framework),
    bstack1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⣁"): a11y.bstack1l111l111l_opy_(bs_config),
    bstack1ll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ⣂"): bs_config.get(bstack1ll_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ⣃"), False),
    bstack1ll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ⣄"): bstack11lll11111_opy_,
    bstack1ll_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭⣅"): bstack11ll11ll11_opy_,
    bstack1ll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬ⣆"): bstack1ll111ll1ll1_opy_
  }
  return bstack111ll1l1ll_opy_