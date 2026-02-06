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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack111ll1l11ll_opy_, bstack11ll11l11l_opy_, bstack1l1ll1ll1_opy_, bstack1l11111lll_opy_, \
    bstack111l111l11l_opy_
from bstack_utils.measure import measure
def bstack1l1llll1_opy_(bstack1lll1ll11111_opy_):
    for driver in bstack1lll1ll11111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l11ll1lll_opy_, stage=STAGE.bstack1llll11111_opy_)
def bstack11l1l111l_opy_(driver, status, reason=bstack11lllll_opy_ (u"ࠪࠫ↞")):
    bstack1l111111_opy_ = Config.bstack1llll1l111_opy_()
    if bstack1l111111_opy_.bstack1llll1l11ll_opy_():
        return
    bstack1lll1l11_opy_ = bstack111l1ll111_opy_(bstack11lllll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧ↟"), bstack11lllll_opy_ (u"ࠬ࠭↠"), status, reason, bstack11lllll_opy_ (u"࠭ࠧ↡"), bstack11lllll_opy_ (u"ࠧࠨ↢"))
    driver.execute_script(bstack1lll1l11_opy_)
@measure(event_name=EVENTS.bstack1l11ll1lll_opy_, stage=STAGE.bstack1llll11111_opy_)
def bstack1ll11lll1_opy_(page, status, reason=bstack11lllll_opy_ (u"ࠨࠩ↣")):
    try:
        if page is None:
            return
        bstack1l111111_opy_ = Config.bstack1llll1l111_opy_()
        if bstack1l111111_opy_.bstack1llll1l11ll_opy_():
            return
        bstack1lll1l11_opy_ = bstack111l1ll111_opy_(bstack11lllll_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ↤"), bstack11lllll_opy_ (u"ࠪࠫ↥"), status, reason, bstack11lllll_opy_ (u"ࠫࠬ↦"), bstack11lllll_opy_ (u"ࠬ࠭↧"))
        page.evaluate(bstack11lllll_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢ↨"), bstack1lll1l11_opy_)
    except Exception as e:
        print(bstack11lllll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡࡨࡲࡶࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡾࢁࠧ↩"), e)
def bstack111l1ll111_opy_(type, name, status, reason, bstack1l1l111ll_opy_, bstack11l111ll_opy_):
    bstack11l1l11l_opy_ = {
        bstack11lllll_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨ↪"): type,
        bstack11lllll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ↫"): {}
    }
    if type == bstack11lllll_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬ↬"):
        bstack11l1l11l_opy_[bstack11lllll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ↭")][bstack11lllll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ↮")] = bstack1l1l111ll_opy_
        bstack11l1l11l_opy_[bstack11lllll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ↯")][bstack11lllll_opy_ (u"ࠧࡥࡣࡷࡥࠬ↰")] = json.dumps(str(bstack11l111ll_opy_))
    if type == bstack11lllll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ↱"):
        bstack11l1l11l_opy_[bstack11lllll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ↲")][bstack11lllll_opy_ (u"ࠪࡲࡦࡳࡥࠨ↳")] = name
    if type == bstack11lllll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧ↴"):
        bstack11l1l11l_opy_[bstack11lllll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ↵")][bstack11lllll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭↶")] = status
        if status == bstack11lllll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ↷") and str(reason) != bstack11lllll_opy_ (u"ࠣࠤ↸"):
            bstack11l1l11l_opy_[bstack11lllll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ↹")][bstack11lllll_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪ↺")] = json.dumps(str(reason))
    bstack11lll11l1l_opy_ = bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩ↻").format(json.dumps(bstack11l1l11l_opy_))
    return bstack11lll11l1l_opy_
def bstack1ll11l1l_opy_(url, config, logger, bstack1ll11111_opy_=False):
    hostname = bstack11ll11l11l_opy_(url)
    is_private = bstack1l11111lll_opy_(hostname)
    try:
        if is_private or bstack1ll11111_opy_:
            file_path = bstack111ll1l11ll_opy_(bstack11lllll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ↼"), bstack11lllll_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬ↽"), logger)
            if os.environ.get(bstack11lllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬ↾")) and eval(
                    os.environ.get(bstack11lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭↿"))):
                return
            if (bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭⇀") in config and not config[bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ⇁")]):
                os.environ[bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩ⇂")] = str(True)
                bstack1lll1ll1111l_opy_ = {bstack11lllll_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧ⇃"): hostname}
                bstack111l111l11l_opy_(bstack11lllll_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬ⇄"), bstack11lllll_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬ⇅"), bstack1lll1ll1111l_opy_, logger)
    except Exception as e:
        pass
def bstack1lll11lll_opy_(caps, bstack1lll1l1lllll_opy_):
    if bstack11lllll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ⇆") in caps:
        caps[bstack11lllll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ⇇")][bstack11lllll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩ⇈")] = True
        if bstack1lll1l1lllll_opy_:
            caps[bstack11lllll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ⇉")][bstack11lllll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ⇊")] = bstack1lll1l1lllll_opy_
    else:
        caps[bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࠫ⇋")] = True
        if bstack1lll1l1lllll_opy_:
            caps[bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ⇌")] = bstack1lll1l1lllll_opy_
def bstack1llll11111ll_opy_(bstack1111l1l111_opy_):
    bstack1lll1ll111l1_opy_ = bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬ⇍"), bstack11lllll_opy_ (u"ࠩࠪ⇎"))
    if bstack1lll1ll111l1_opy_ == bstack11lllll_opy_ (u"ࠪࠫ⇏") or bstack1lll1ll111l1_opy_ == bstack11lllll_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ⇐"):
        threading.current_thread().testStatus = bstack1111l1l111_opy_
    else:
        if bstack1111l1l111_opy_ == bstack11lllll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⇑"):
            threading.current_thread().testStatus = bstack1111l1l111_opy_