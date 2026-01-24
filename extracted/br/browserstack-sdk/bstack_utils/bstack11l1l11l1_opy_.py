# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack111ll1l1l11_opy_, bstack1l11l1l1l1_opy_, bstack111111lll_opy_, bstack11ll1ll1_opy_, \
    bstack111l1ll1l1l_opy_
from bstack_utils.measure import measure
def bstack1l111l11_opy_(bstack1lll1ll1llll_opy_):
    for driver in bstack1lll1ll1llll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1llll11ll_opy_, stage=STAGE.bstack1111lll11_opy_)
def bstack1l111l1ll_opy_(driver, status, reason=bstack1l1111_opy_ (u"ࠩࠪⅺ")):
    bstack1llllll11l_opy_ = Config.bstack111ll1lll1_opy_()
    if bstack1llllll11l_opy_.bstack1llll11l111_opy_():
        return
    bstack1l1l1l1l_opy_ = bstack1lll1l1l_opy_(bstack1l1111_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ⅻ"), bstack1l1111_opy_ (u"ࠫࠬⅼ"), status, reason, bstack1l1111_opy_ (u"ࠬ࠭ⅽ"), bstack1l1111_opy_ (u"࠭ࠧⅾ"))
    driver.execute_script(bstack1l1l1l1l_opy_)
@measure(event_name=EVENTS.bstack1llll11ll_opy_, stage=STAGE.bstack1111lll11_opy_)
def bstack1llll1lll1_opy_(page, status, reason=bstack1l1111_opy_ (u"ࠧࠨⅿ")):
    try:
        if page is None:
            return
        bstack1llllll11l_opy_ = Config.bstack111ll1lll1_opy_()
        if bstack1llllll11l_opy_.bstack1llll11l111_opy_():
            return
        bstack1l1l1l1l_opy_ = bstack1lll1l1l_opy_(bstack1l1111_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫↀ"), bstack1l1111_opy_ (u"ࠩࠪↁ"), status, reason, bstack1l1111_opy_ (u"ࠪࠫↂ"), bstack1l1111_opy_ (u"ࠫࠬↃ"))
        page.evaluate(bstack1l1111_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨↄ"), bstack1l1l1l1l_opy_)
    except Exception as e:
        print(bstack1l1111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡽࢀࠦↅ"), e)
def bstack1lll1l1l_opy_(type, name, status, reason, bstack11ll11llll_opy_, bstack1ll1l11ll1_opy_):
    bstack11ll1l11l1_opy_ = {
        bstack1l1111_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧↆ"): type,
        bstack1l1111_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫↇ"): {}
    }
    if type == bstack1l1111_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫↈ"):
        bstack11ll1l11l1_opy_[bstack1l1111_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭↉")][bstack1l1111_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ↊")] = bstack11ll11llll_opy_
        bstack11ll1l11l1_opy_[bstack1l1111_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ↋")][bstack1l1111_opy_ (u"࠭ࡤࡢࡶࡤࠫ↌")] = json.dumps(str(bstack1ll1l11ll1_opy_))
    if type == bstack1l1111_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ↍"):
        bstack11ll1l11l1_opy_[bstack1l1111_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ↎")][bstack1l1111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ↏")] = name
    if type == bstack1l1111_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭←"):
        bstack11ll1l11l1_opy_[bstack1l1111_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ↑")][bstack1l1111_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ→")] = status
        if status == bstack1l1111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭↓") and str(reason) != bstack1l1111_opy_ (u"ࠢࠣ↔"):
            bstack11ll1l11l1_opy_[bstack1l1111_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ↕")][bstack1l1111_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩ↖")] = json.dumps(str(reason))
    bstack11l1l11l1l_opy_ = bstack1l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨ↗").format(json.dumps(bstack11ll1l11l1_opy_))
    return bstack11l1l11l1l_opy_
def bstack1lll1l11_opy_(url, config, logger, bstack1l1111l11_opy_=False):
    hostname = bstack1l11l1l1l1_opy_(url)
    is_private = bstack11ll1ll1_opy_(hostname)
    try:
        if is_private or bstack1l1111l11_opy_:
            file_path = bstack111ll1l1l11_opy_(bstack1l1111_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ↘"), bstack1l1111_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫ↙"), logger)
            if os.environ.get(bstack1l1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫ↚")) and eval(
                    os.environ.get(bstack1l1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬ↛"))):
                return
            if (bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ↜") in config and not config[bstack1l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭↝")]):
                os.environ[bstack1l1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨ↞")] = str(True)
                bstack1lll1ll1ll11_opy_ = {bstack1l1111_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭↟"): hostname}
                bstack111l1ll1l1l_opy_(bstack1l1111_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫ↠"), bstack1l1111_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫ↡"), bstack1lll1ll1ll11_opy_, logger)
    except Exception as e:
        pass
def bstack1111l11l_opy_(caps, bstack1lll1ll1ll1l_opy_):
    if bstack1l1111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ↢") in caps:
        caps[bstack1l1111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ↣")][bstack1l1111_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨ↤")] = True
        if bstack1lll1ll1ll1l_opy_:
            caps[bstack1l1111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ↥")][bstack1l1111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭↦")] = bstack1lll1ll1ll1l_opy_
    else:
        caps[bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪ↧")] = True
        if bstack1lll1ll1ll1l_opy_:
            caps[bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ↨")] = bstack1lll1ll1ll1l_opy_
def bstack1llll111llll_opy_(bstack111111l11l_opy_):
    bstack1lll1ll1lll1_opy_ = bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫ↩"), bstack1l1111_opy_ (u"ࠨࠩ↪"))
    if bstack1lll1ll1lll1_opy_ == bstack1l1111_opy_ (u"ࠩࠪ↫") or bstack1lll1ll1lll1_opy_ == bstack1l1111_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ↬"):
        threading.current_thread().testStatus = bstack111111l11l_opy_
    else:
        if bstack111111l11l_opy_ == bstack1l1111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ↭"):
            threading.current_thread().testStatus = bstack111111l11l_opy_