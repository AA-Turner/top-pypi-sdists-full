# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack1llll1lll111_opy_, bstack1111lll11_opy_, bstack111lll1ll1_opy_, bstack11lll1l1l1_opy_, \
    bstack1llll1lll11l_opy_
from bstack_utils.measure import measure
def bstack1ll111l1_opy_(bstack1ll11ll11ll1_opy_):
    for driver in bstack1ll11ll11ll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l111l11l1_opy_, stage=STAGE.bstack1l1l1ll111_opy_)
def bstack11111lll11_opy_(driver, status, reason=bstack111ll11_opy_ (u"ࠪࠫ⛬")):
    global_config = Config.bstack1lllll1lll1_opy_()
    if global_config.bstack1ll1l1ll1l1_opy_():
        return
    bstack1llllllllll_opy_ = bstack1lll1l1l11_opy_(bstack111ll11_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧ⛭"), bstack111ll11_opy_ (u"ࠬ࠭⛮"), status, reason, bstack111ll11_opy_ (u"࠭ࠧ⛯"), bstack111ll11_opy_ (u"ࠧࠨ⛰"))
    driver.execute_script(bstack1llllllllll_opy_)
@measure(event_name=EVENTS.bstack1l111l11l1_opy_, stage=STAGE.bstack1l1l1ll111_opy_)
def bstack1lll1l1l1l_opy_(page, status, reason=bstack111ll11_opy_ (u"ࠨࠩ⛱")):
    try:
        if page is None:
            return
        global_config = Config.bstack1lllll1lll1_opy_()
        if global_config.bstack1ll1l1ll1l1_opy_():
            return
        bstack1llllllllll_opy_ = bstack1lll1l1l11_opy_(bstack111ll11_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ⛲"), bstack111ll11_opy_ (u"ࠪࠫ⛳"), status, reason, bstack111ll11_opy_ (u"ࠫࠬ⛴"), bstack111ll11_opy_ (u"ࠬ࠭⛵"))
        page.evaluate(bstack111ll11_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢ⛶"), bstack1llllllllll_opy_)
    except Exception as e:
        print(bstack111ll11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡࡨࡲࡶࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡾࢁࠧ⛷"), e)
def bstack1lll1l1l11_opy_(type, name, status, reason, bstack11l11111l1_opy_, bstack1111ll111l_opy_):
    bstack1l1llll1_opy_ = {
        bstack111ll11_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨ⛸"): type,
        bstack111ll11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ⛹"): {}
    }
    if type == bstack111ll11_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬ⛺"):
        bstack1l1llll1_opy_[bstack111ll11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ⛻")][bstack111ll11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ⛼")] = bstack11l11111l1_opy_
        bstack1l1llll1_opy_[bstack111ll11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ⛽")][bstack111ll11_opy_ (u"ࠧࡥࡣࡷࡥࠬ⛾")] = json.dumps(str(bstack1111ll111l_opy_))
    if type == bstack111ll11_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ⛿"):
        bstack1l1llll1_opy_[bstack111ll11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ✀")][bstack111ll11_opy_ (u"ࠪࡲࡦࡳࡥࠨ✁")] = name
    if type == bstack111ll11_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧ✂"):
        bstack1l1llll1_opy_[bstack111ll11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ✃")][bstack111ll11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭✄")] = status
        if status == bstack111ll11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ✅") and str(reason) != bstack111ll11_opy_ (u"ࠣࠤ✆"):
            bstack1l1llll1_opy_[bstack111ll11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ✇")][bstack111ll11_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪ✈")] = json.dumps(str(reason))
    bstack1ll1lllll_opy_ = bstack111ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩ✉").format(json.dumps(bstack1l1llll1_opy_))
    return bstack1ll1lllll_opy_
def bstack111l1ll111_opy_(url, config, logger, bstack111l1lll1_opy_=False):
    hostname = bstack1111lll11_opy_(url)
    is_private = bstack11lll1l1l1_opy_(hostname)
    try:
        if is_private or bstack111l1lll1_opy_:
            file_path = bstack1llll1lll111_opy_(bstack111ll11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ✊"), bstack111ll11_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬ✋"), logger)
            if os.environ.get(bstack111ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬ✌")) and eval(
                    os.environ.get(bstack111ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭✍"))):
                return
            if (bstack111ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭✎") in config and not config[bstack111ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ✏")]):
                os.environ[bstack111ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩ✐")] = str(True)
                bstack1ll11ll1l11l_opy_ = {bstack111ll11_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧ✑"): hostname}
                bstack1llll1lll11l_opy_(bstack111ll11_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬ✒"), bstack111ll11_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬ✓"), bstack1ll11ll1l11l_opy_, logger)
    except Exception as e:
        pass
def update_caps_for_local(caps, bstack1ll11ll11lll_opy_):
    if bstack111ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ✔") in caps:
        caps[bstack111ll11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ✕")][bstack111ll11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩ✖")] = True
        if bstack1ll11ll11lll_opy_:
            caps[bstack111ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ✗")][bstack111ll11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ✘")] = bstack1ll11ll11lll_opy_
    else:
        caps[bstack111ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࠫ✙")] = True
        if bstack1ll11ll11lll_opy_:
            caps[bstack111ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ✚")] = bstack1ll11ll11lll_opy_
def bstack1ll1l11111ll_opy_(bstack1lll11l1ll1_opy_):
    bstack1ll11ll1l111_opy_ = bstack111lll1ll1_opy_(threading.current_thread(), bstack111ll11_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬ✛"), bstack111ll11_opy_ (u"ࠩࠪ✜"))
    if bstack1ll11ll1l111_opy_ == bstack111ll11_opy_ (u"ࠪࠫ✝") or bstack1ll11ll1l111_opy_ == bstack111ll11_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ✞"):
        threading.current_thread().testStatus = bstack1lll11l1ll1_opy_
    else:
        if bstack1lll11l1ll1_opy_ == bstack111ll11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ✟"):
            threading.current_thread().testStatus = bstack1lll11l1ll1_opy_