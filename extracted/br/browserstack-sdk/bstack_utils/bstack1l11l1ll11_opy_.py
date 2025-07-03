# coding: UTF-8
import sys
bstack1111l11_opy_ = sys.version_info [0] == 2
bstack1lll1l_opy_ = 2048
bstack1l11111_opy_ = 7
def bstack1l1_opy_ (bstack1lll_opy_):
    global bstack111l1l_opy_
    bstack1l11lll_opy_ = ord (bstack1lll_opy_ [-1])
    bstack1l11ll1_opy_ = bstack1lll_opy_ [:-1]
    bstack11llll1_opy_ = bstack1l11lll_opy_ % len (bstack1l11ll1_opy_)
    bstack1l1ll11_opy_ = bstack1l11ll1_opy_ [:bstack11llll1_opy_] + bstack1l11ll1_opy_ [bstack11llll1_opy_:]
    if bstack1111l11_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    return eval (bstack11l1ll_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack11lll1111ll_opy_, bstack11111lll1_opy_, get_host_info, bstack11l11ll1l1l_opy_, \
 bstack11l1lll111_opy_, bstack1ll11lll1l_opy_, bstack1111ll1lll_opy_, bstack11l1111l1l1_opy_, bstack111ll11ll_opy_
import bstack_utils.accessibility as bstack11l111l11_opy_
from bstack_utils.bstack111lll11ll_opy_ import bstack11l1l111l1_opy_
from bstack_utils.percy import bstack11lll1ll1l_opy_
from bstack_utils.config import Config
bstack11ll1l1l1_opy_ = Config.bstack1l1l111l1l_opy_()
logger = logging.getLogger(__name__)
percy = bstack11lll1ll1l_opy_()
@bstack1111ll1lll_opy_(class_method=False)
def bstack1llllll111l1_opy_(bs_config, bstack111111l1l_opy_):
  try:
    data = {
        bstack1l1_opy_ (u"࠭ࡦࡰࡴࡰࡥࡹ࠭ℇ"): bstack1l1_opy_ (u"ࠧ࡫ࡵࡲࡲࠬ℈"),
        bstack1l1_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡡࡱࡥࡲ࡫ࠧ℉"): bs_config.get(bstack1l1_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧℊ"), bstack1l1_opy_ (u"ࠪࠫℋ")),
        bstack1l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩℌ"): bs_config.get(bstack1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨℍ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩℎ"): bs_config.get(bstack1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩℏ")),
        bstack1l1_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ℐ"): bs_config.get(bstack1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬℑ"), bstack1l1_opy_ (u"ࠪࠫℒ")),
        bstack1l1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨℓ"): bstack111ll11ll_opy_(),
        bstack1l1_opy_ (u"ࠬࡺࡡࡨࡵࠪ℔"): bstack11l11ll1l1l_opy_(bs_config),
        bstack1l1_opy_ (u"࠭ࡨࡰࡵࡷࡣ࡮ࡴࡦࡰࠩℕ"): get_host_info(),
        bstack1l1_opy_ (u"ࠧࡤ࡫ࡢ࡭ࡳ࡬࡯ࠨ№"): bstack11111lll1_opy_(),
        bstack1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡳࡷࡱࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ℗"): os.environ.get(bstack1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨ℘")),
        bstack1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࡡࡵࡩࡷࡻ࡮ࠨℙ"): os.environ.get(bstack1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠩℚ"), False),
        bstack1l1_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࡥࡣࡰࡰࡷࡶࡴࡲࠧℛ"): bstack11lll1111ll_opy_(),
        bstack1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ℜ"): bstack1llll1lllll1_opy_(bs_config),
        bstack1l1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡨࡪࡺࡡࡪ࡮ࡶࠫℝ"): bstack1llll1llllll_opy_(bstack111111l1l_opy_),
        bstack1l1_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭℞"): bstack1lllll1111l1_opy_(bs_config, bstack111111l1l_opy_.get(bstack1l1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦࠪ℟"), bstack1l1_opy_ (u"ࠪࠫ℠"))),
        bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭℡"): bstack11l1lll111_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack1l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡳࡥࡾࡲ࡯ࡢࡦࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࠣࡿࢂࠨ™").format(str(error)))
    return None
def bstack1llll1llllll_opy_(framework):
  return {
    bstack1l1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡐࡤࡱࡪ࠭℣"): framework.get(bstack1l1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠨℤ"), bstack1l1_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨ℥")),
    bstack1l1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬΩ"): framework.get(bstack1l1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ℧")),
    bstack1l1_opy_ (u"ࠫࡸࡪ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨℨ"): framework.get(bstack1l1_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ℩")),
    bstack1l1_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨK"): bstack1l1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧÅ"),
    bstack1l1_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨℬ"): framework.get(bstack1l1_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩℭ"))
  }
def bstack11l1lllll_opy_(bs_config, framework):
  bstack1llll11l_opy_ = False
  bstack1lll1l1l11_opy_ = False
  bstack1llll1llll1l_opy_ = False
  if bstack1l1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ℮") in bs_config:
    bstack1llll1llll1l_opy_ = True
  elif bstack1l1_opy_ (u"ࠫࡦࡶࡰࠨℯ") in bs_config:
    bstack1llll11l_opy_ = True
  else:
    bstack1lll1l1l11_opy_ = True
  bstack11ll11ll1l_opy_ = {
    bstack1l1_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬℰ"): bstack11l1l111l1_opy_.bstack1llll1llll11_opy_(bs_config, framework),
    bstack1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ℱ"): bstack11l111l11_opy_.bstack11l1l1l1l_opy_(bs_config),
    bstack1l1_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭Ⅎ"): bs_config.get(bstack1l1_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧℳ"), False),
    bstack1l1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫℴ"): bstack1lll1l1l11_opy_,
    bstack1l1_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩℵ"): bstack1llll11l_opy_,
    bstack1l1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨℶ"): bstack1llll1llll1l_opy_
  }
  return bstack11ll11ll1l_opy_
@bstack1111ll1lll_opy_(class_method=False)
def bstack1llll1lllll1_opy_(bs_config):
  try:
    bstack1lllll111lll_opy_ = json.loads(os.getenv(bstack1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ℷ"), bstack1l1_opy_ (u"࠭ࡻࡾࠩℸ")))
    bstack1lllll111lll_opy_ = bstack1lllll11l111_opy_(bs_config, bstack1lllll111lll_opy_)
    return {
        bstack1l1_opy_ (u"ࠧࡴࡧࡷࡸ࡮ࡴࡧࡴࠩℹ"): bstack1lllll111lll_opy_
    }
  except Exception as error:
    logger.error(bstack1l1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥ࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡶࡩࡹࡺࡩ࡯ࡩࡶࠤ࡫ࡵࡲࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࠤࢀࢃࠢ℺").format(str(error)))
    return {}
def bstack1lllll11l111_opy_(bs_config, bstack1lllll111lll_opy_):
  if ((bstack1l1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭℻") in bs_config or not bstack11l1lll111_opy_(bs_config)) and bstack11l111l11_opy_.bstack11l1l1l1l_opy_(bs_config)):
    bstack1lllll111lll_opy_[bstack1l1_opy_ (u"ࠥ࡭ࡳࡩ࡬ࡶࡦࡨࡉࡳࡩ࡯ࡥࡧࡧࡉࡽࡺࡥ࡯ࡵ࡬ࡳࡳࠨℼ")] = True
  return bstack1lllll111lll_opy_
def bstack1lllll1ll11l_opy_(array, bstack1lllll111ll1_opy_, bstack1lllll111l1l_opy_):
  result = {}
  for o in array:
    key = o[bstack1lllll111ll1_opy_]
    result[key] = o[bstack1lllll111l1l_opy_]
  return result
def bstack1llllll111ll_opy_(bstack1l111111l_opy_=bstack1l1_opy_ (u"ࠫࠬℽ")):
  bstack1lllll111l11_opy_ = bstack11l111l11_opy_.on()
  bstack1lllll1111ll_opy_ = bstack11l1l111l1_opy_.on()
  bstack1lllll111111_opy_ = percy.bstack1l111l1111_opy_()
  if bstack1lllll111111_opy_ and not bstack1lllll1111ll_opy_ and not bstack1lllll111l11_opy_:
    return bstack1l111111l_opy_ not in [bstack1l1_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩℾ"), bstack1l1_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪℿ")]
  elif bstack1lllll111l11_opy_ and not bstack1lllll1111ll_opy_:
    return bstack1l111111l_opy_ not in [bstack1l1_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ⅀"), bstack1l1_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⅁"), bstack1l1_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭⅂")]
  return bstack1lllll111l11_opy_ or bstack1lllll1111ll_opy_ or bstack1lllll111111_opy_
@bstack1111ll1lll_opy_(class_method=False)
def bstack1llllll1111l_opy_(bstack1l111111l_opy_, test=None):
  bstack1lllll11111l_opy_ = bstack11l111l11_opy_.on()
  if not bstack1lllll11111l_opy_ or bstack1l111111l_opy_ not in [bstack1l1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⅃")] or test == None:
    return None
  return {
    bstack1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⅄"): bstack1lllll11111l_opy_ and bstack1ll11lll1l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫⅅ"), None) == True and bstack11l111l11_opy_.bstack11l1111ll_opy_(test[bstack1l1_opy_ (u"࠭ࡴࡢࡩࡶࠫⅆ")])
  }
def bstack1lllll1111l1_opy_(bs_config, framework):
  bstack1llll11l_opy_ = False
  bstack1lll1l1l11_opy_ = False
  bstack1llll1llll1l_opy_ = False
  if bstack1l1_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫⅇ") in bs_config:
    bstack1llll1llll1l_opy_ = True
  elif bstack1l1_opy_ (u"ࠨࡣࡳࡴࠬⅈ") in bs_config:
    bstack1llll11l_opy_ = True
  else:
    bstack1lll1l1l11_opy_ = True
  bstack11ll11ll1l_opy_ = {
    bstack1l1_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩⅉ"): bstack11l1l111l1_opy_.bstack1llll1llll11_opy_(bs_config, framework),
    bstack1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⅊"): bstack11l111l11_opy_.bstack1ll1l111ll_opy_(bs_config),
    bstack1l1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ⅋"): bs_config.get(bstack1l1_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ⅌"), False),
    bstack1l1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ⅍"): bstack1lll1l1l11_opy_,
    bstack1l1_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ⅎ"): bstack1llll11l_opy_,
    bstack1l1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬ⅏"): bstack1llll1llll1l_opy_
  }
  return bstack11ll11ll1l_opy_