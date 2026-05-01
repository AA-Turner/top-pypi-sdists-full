# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack1111ll11l11_opy_, bstack1l11ll1111_opy_, get_host_info, bstack1llllll1ll11_opy_, \
 bstack11l1ll1l_opy_, bstack1ll11l1ll1_opy_, error_handler, bstack1lllll11llll_opy_, bstack1111l1l1l_opy_
import bstack_utils.accessibility as a11y
from bstack_utils.bstack111llll111_opy_ import bstack1ll11l1l_opy_
from bstack_utils.bstack111l1ll11_opy_ import bstack111ll111_opy_
from bstack_utils.percy import bstack1l1lllll1_opy_
from bstack_utils.config import Config
global_config = Config.bstack1l1l11ll1_opy_()
logger = logging.getLogger(__name__)
percy = bstack1l1lllll1_opy_()
@error_handler(class_method=False)
def bstack1ll111l1ll11_opy_(bs_config, bstack1lll111l11_opy_):
  try:
    data = {
        bstack111ll_opy_ (u"ࠪࡪࡴࡸ࡭ࡢࡶࠪ⣹"): bstack111ll_opy_ (u"ࠫ࡯ࡹ࡯࡯ࠩ⣺"),
        bstack111ll_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡥ࡮ࡢ࡯ࡨࠫ⣻"): bs_config.get(bstack111ll_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫ⣼"), bstack111ll_opy_ (u"ࠧࠨ⣽")),
        bstack111ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭⣾"): bs_config.get(bstack111ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ⣿"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack111ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭⤀"): bs_config.get(bstack111ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭⤁")),
        bstack111ll_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ⤂"): bs_config.get(bstack111ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡉ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩ⤃"), bstack111ll_opy_ (u"ࠧࠨ⤄")),
        bstack111ll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⤅"): bstack1111l1l1l_opy_(),
        bstack111ll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ⤆"): bstack1llllll1ll11_opy_(bs_config),
        bstack111ll_opy_ (u"ࠪ࡬ࡴࡹࡴࡠ࡫ࡱࡪࡴ࠭⤇"): get_host_info(),
        bstack111ll_opy_ (u"ࠫࡨ࡯࡟ࡪࡰࡩࡳࠬ⤈"): bstack1l11ll1111_opy_(),
        bstack111ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣࡷࡻ࡮ࡠ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ⤉"): os.environ.get(bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬ⤊")),
        bstack111ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪ࡟ࡵࡧࡶࡸࡸࡥࡲࡦࡴࡸࡲࠬ⤋"): os.environ.get(bstack111ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓ࠭⤌"), False),
        bstack111ll_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࡢࡧࡴࡴࡴࡳࡱ࡯ࠫ⤍"): bstack1111ll11l11_opy_(),
        bstack111ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⤎"): bstack1ll111l111l1_opy_(bs_config),
        bstack111ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡥࡧࡷࡥ࡮ࡲࡳࠨ⤏"): bstack1ll1111lllll_opy_(bstack1lll111l11_opy_),
        bstack111ll_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹࡥ࡭ࡢࡲࠪ⤐"): bstack1ll111l11l11_opy_(bs_config, bstack1lll111l11_opy_.get(bstack111ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡸࡷࡪࡪࠧ⤑"), bstack111ll_opy_ (u"ࠧࠨ⤒"))),
        bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ⤓"): bstack11l1ll1l_opy_(bs_config),
        bstack111ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠧ⤔"): bstack1ll1111ll1ll_opy_(bs_config)
    }
    return data
  except Exception as error:
    logger.error(bstack111ll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡱࡣࡼࡰࡴࡧࡤࠡࡨࡲࡶ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࠡࡽࢀࠦ⤕").format(str(error)))
    return None
def bstack1ll1111lllll_opy_(framework):
  return {
    bstack111ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨࠫ⤖"): framework.get(bstack111ll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪ࠭⤗"), bstack111ll_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭⤘")),
    bstack111ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪ⤙"): framework.get(bstack111ll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ⤚")),
    bstack111ll_opy_ (u"ࠩࡶࡨࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭⤛"): framework.get(bstack111ll_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ⤜")),
    bstack111ll_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭⤝"): bstack111ll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ⤞"),
    bstack111ll_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭⤟"): framework.get(bstack111ll_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ⤠"))
  }
def bstack1ll1111ll1ll_opy_(bs_config):
  bstack111ll_opy_ (u"ࠣࠤࠥࠎࠥࠦࡒࡦࡶࡸࡶࡳࡹࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡧࡥࡹࡧࠠࡧࡱࡵࠤࡧࡻࡩ࡭ࡦࠣࡷࡹࡧࡲࡵ࠰ࠍࠤࠥࠨࠢࠣ⤡")
  if not bs_config:
    return {}
  bstack1lll11l111ll_opy_ = bstack1ll11l1l_opy_(bs_config).bstack1lll11l1l11l_opy_(bs_config)
  return bstack1lll11l111ll_opy_
def bstack11ll11l1ll_opy_(bs_config, framework):
  bstack1l1ll1111_opy_ = False
  bstack1l11l11111_opy_ = False
  bstack1ll111l11ll1_opy_ = False
  if bstack111ll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭⤢") in bs_config:
    bstack1ll111l11ll1_opy_ = True
  elif bstack111ll_opy_ (u"ࠪࡥࡵࡶࠧ⤣") in bs_config:
    bstack1l1ll1111_opy_ = True
  else:
    bstack1l11l11111_opy_ = True
  bstack11ll11l11_opy_ = {
    bstack111ll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⤤"): bstack111ll111_opy_.bstack1ll111l11l1l_opy_(bs_config, framework),
    bstack111ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⤥"): a11y.is_enabled_root(bs_config),
    bstack111ll_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ⤦"): bs_config.get(bstack111ll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭⤧"), False),
    bstack111ll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ⤨"): bstack1l11l11111_opy_,
    bstack111ll_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨ⤩"): bstack1l1ll1111_opy_,
    bstack111ll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧ⤪"): bstack1ll111l11ll1_opy_
  }
  return bstack11ll11l11_opy_
@error_handler(class_method=False)
def bstack1ll111l111l1_opy_(bs_config):
  try:
    bstack1ll1111lll1l_opy_ = json.loads(os.getenv(bstack111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ⤫"), bstack111ll_opy_ (u"ࠬࢁࡽࠨ⤬")))
    bstack1ll1111lll1l_opy_ = bstack1ll111l1l111_opy_(bs_config, bstack1ll1111lll1l_opy_)
    return {
        bstack111ll_opy_ (u"࠭ࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨ⤭"): bstack1ll1111lll1l_opy_
    }
  except Exception as error:
    logger.error(bstack111ll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤ࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡵࡨࡸࡹ࡯࡮ࡨࡵࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࠣࡿࢂࠨ⤮").format(str(error)))
    return {}
def bstack1ll111l1l111_opy_(bs_config, bstack1ll1111lll1l_opy_):
  if ((bstack111ll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ⤯") in bs_config or not bstack11l1ll1l_opy_(bs_config)) and a11y.is_enabled_root(bs_config)):
    bstack1ll1111lll1l_opy_[bstack111ll_opy_ (u"ࠤ࡬ࡲࡨࡲࡵࡥࡧࡈࡲࡨࡵࡤࡦࡦࡈࡼࡹ࡫࡮ࡴ࡫ࡲࡲࠧ⤰")] = True
  return bstack1ll1111lll1l_opy_
def bstack1ll111lll1ll_opy_(array, bstack1ll111l11lll_opy_, bstack1ll111l11111_opy_):
  result = {}
  for o in array:
    key = o[bstack1ll111l11lll_opy_]
    result[key] = o[bstack1ll111l11111_opy_]
  return result
def bstack1ll111lll1l1_opy_(bstack11l111l1ll_opy_=bstack111ll_opy_ (u"ࠪࠫ⤱")):
  bstack1ll111l111ll_opy_ = a11y.on()
  bstack1ll1111lll11_opy_ = bstack111ll111_opy_.on()
  bstack1ll111l1111l_opy_ = percy.bstack11l1111ll_opy_()
  if bstack1ll111l1111l_opy_ and not bstack1ll1111lll11_opy_ and not bstack1ll111l111ll_opy_:
    return bstack11l111l1ll_opy_ not in [bstack111ll_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨ⤲"), bstack111ll_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩ⤳")]
  elif bstack1ll111l111ll_opy_ and not bstack1ll1111lll11_opy_:
    return bstack11l111l1ll_opy_ not in [bstack111ll_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ⤴"), bstack111ll_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ⤵"), bstack111ll_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬ⤶")]
  return bstack1ll111l111ll_opy_ or bstack1ll1111lll11_opy_ or bstack1ll111l1111l_opy_
@error_handler(class_method=False)
def bstack1ll11l11111l_opy_(bstack11l111l1ll_opy_, test=None):
  bstack1ll1111llll1_opy_ = a11y.on()
  if not bstack1ll1111llll1_opy_ or bstack11l111l1ll_opy_ not in [bstack111ll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ⤷"), bstack111ll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⤸"), bstack111ll_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨ⤹")] or test == None:
    return None
  return {
    bstack111ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⤺"): bstack1ll1111llll1_opy_ and bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ⤻"), None) == True and a11y.is_enabled_testcase(test.get(bstack111ll_opy_ (u"ࠧࡵࡣࡪࡷࠬ⤼"), []))
  }
def bstack1ll111l11l11_opy_(bs_config, framework):
  bstack1l1ll1111_opy_ = False
  bstack1l11l11111_opy_ = False
  bstack1ll111l11ll1_opy_ = False
  if bstack111ll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ⤽") in bs_config:
    bstack1ll111l11ll1_opy_ = True
  elif bstack111ll_opy_ (u"ࠩࡤࡴࡵ࠭⤾") in bs_config:
    bstack1l1ll1111_opy_ = True
  else:
    bstack1l11l11111_opy_ = True
  bstack11ll11l11_opy_ = {
    bstack111ll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ⤿"): bstack111ll111_opy_.bstack1ll111l11l1l_opy_(bs_config, framework),
    bstack111ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⥀"): a11y.bstack111lll11ll_opy_(bs_config),
    bstack111ll_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ⥁"): bs_config.get(bstack111ll_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ⥂"), False),
    bstack111ll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩ⥃"): bstack1l11l11111_opy_,
    bstack111ll_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ⥄"): bstack1l1ll1111_opy_,
    bstack111ll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭⥅"): bstack1ll111l11ll1_opy_
  }
  return bstack11ll11l11_opy_