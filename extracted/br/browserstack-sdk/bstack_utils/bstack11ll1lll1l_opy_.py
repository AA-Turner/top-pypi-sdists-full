# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l1l11l1l1_opy_, bstack11lllllll_opy_, bstack1l111l11_opy_, bstack11l1l1ll1l_opy_, \
    bstack11l1lllll11_opy_
from bstack_utils.measure import measure
def bstack1l1l11l11l_opy_(bstack111l111l11l_opy_):
    for driver in bstack111l111l11l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11l1l1lll_opy_, stage=STAGE.bstack1111lll1_opy_)
def bstack1ll111lll1_opy_(driver, status, reason=bstack1l1lll_opy_ (u"ࠬ࠭ᶔ")):
    bstack11l1l1l1l_opy_ = Config.bstack1l111l11l_opy_()
    if bstack11l1l1l1l_opy_.bstack111l1111ll_opy_():
        return
    bstack1l1ll11lll_opy_ = bstack11ll11lll1_opy_(bstack1l1lll_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩᶕ"), bstack1l1lll_opy_ (u"ࠧࠨᶖ"), status, reason, bstack1l1lll_opy_ (u"ࠨࠩᶗ"), bstack1l1lll_opy_ (u"ࠩࠪᶘ"))
    driver.execute_script(bstack1l1ll11lll_opy_)
@measure(event_name=EVENTS.bstack11l1l1lll_opy_, stage=STAGE.bstack1111lll1_opy_)
def bstack1lll1ll11l_opy_(page, status, reason=bstack1l1lll_opy_ (u"ࠪࠫᶙ")):
    try:
        if page is None:
            return
        bstack11l1l1l1l_opy_ = Config.bstack1l111l11l_opy_()
        if bstack11l1l1l1l_opy_.bstack111l1111ll_opy_():
            return
        bstack1l1ll11lll_opy_ = bstack11ll11lll1_opy_(bstack1l1lll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧᶚ"), bstack1l1lll_opy_ (u"ࠬ࠭ᶛ"), status, reason, bstack1l1lll_opy_ (u"࠭ࠧᶜ"), bstack1l1lll_opy_ (u"ࠧࠨᶝ"))
        page.evaluate(bstack1l1lll_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤᶞ"), bstack1l1ll11lll_opy_)
    except Exception as e:
        print(bstack1l1lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࢀࢃࠢᶟ"), e)
def bstack11ll11lll1_opy_(type, name, status, reason, bstack111l1l1l_opy_, bstack1l11l1l1l1_opy_):
    bstack1lll111ll_opy_ = {
        bstack1l1lll_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪᶠ"): type,
        bstack1l1lll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᶡ"): {}
    }
    if type == bstack1l1lll_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧᶢ"):
        bstack1lll111ll_opy_[bstack1l1lll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᶣ")][bstack1l1lll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᶤ")] = bstack111l1l1l_opy_
        bstack1lll111ll_opy_[bstack1l1lll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᶥ")][bstack1l1lll_opy_ (u"ࠩࡧࡥࡹࡧࠧᶦ")] = json.dumps(str(bstack1l11l1l1l1_opy_))
    if type == bstack1l1lll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᶧ"):
        bstack1lll111ll_opy_[bstack1l1lll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᶨ")][bstack1l1lll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᶩ")] = name
    if type == bstack1l1lll_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩᶪ"):
        bstack1lll111ll_opy_[bstack1l1lll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᶫ")][bstack1l1lll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᶬ")] = status
        if status == bstack1l1lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᶭ") and str(reason) != bstack1l1lll_opy_ (u"ࠥࠦᶮ"):
            bstack1lll111ll_opy_[bstack1l1lll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᶯ")][bstack1l1lll_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬᶰ")] = json.dumps(str(reason))
    bstack1ll1l1l111_opy_ = bstack1l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫᶱ").format(json.dumps(bstack1lll111ll_opy_))
    return bstack1ll1l1l111_opy_
def bstack1l111ll1l_opy_(url, config, logger, bstack1l11l1l11_opy_=False):
    hostname = bstack11lllllll_opy_(url)
    is_private = bstack11l1l1ll1l_opy_(hostname)
    try:
        if is_private or bstack1l11l1l11_opy_:
            file_path = bstack11l1l11l1l1_opy_(bstack1l1lll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᶲ"), bstack1l1lll_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧᶳ"), logger)
            if os.environ.get(bstack1l1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧᶴ")) and eval(
                    os.environ.get(bstack1l1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨᶵ"))):
                return
            if (bstack1l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨᶶ") in config and not config[bstack1l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩᶷ")]):
                os.environ[bstack1l1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫᶸ")] = str(True)
                bstack111l111l1l1_opy_ = {bstack1l1lll_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩᶹ"): hostname}
                bstack11l1lllll11_opy_(bstack1l1lll_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧᶺ"), bstack1l1lll_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧᶻ"), bstack111l111l1l1_opy_, logger)
    except Exception as e:
        pass
def bstack1ll1llll1l_opy_(caps, bstack111l111l1ll_opy_):
    if bstack1l1lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᶼ") in caps:
        caps[bstack1l1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᶽ")][bstack1l1lll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫᶾ")] = True
        if bstack111l111l1ll_opy_:
            caps[bstack1l1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᶿ")][bstack1l1lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ᷀")] = bstack111l111l1ll_opy_
    else:
        caps[bstack1l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭᷁")] = True
        if bstack111l111l1ll_opy_:
            caps[bstack1l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴ᷂ࠪ")] = bstack111l111l1ll_opy_
def bstack111l1l1ll1l_opy_(bstack111lll11ll_opy_):
    bstack111l111l111_opy_ = bstack1l111l11_opy_(threading.current_thread(), bstack1l1lll_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧ᷃"), bstack1l1lll_opy_ (u"ࠫࠬ᷄"))
    if bstack111l111l111_opy_ == bstack1l1lll_opy_ (u"ࠬ࠭᷅") or bstack111l111l111_opy_ == bstack1l1lll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ᷆"):
        threading.current_thread().testStatus = bstack111lll11ll_opy_
    else:
        if bstack111lll11ll_opy_ == bstack1l1lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ᷇"):
            threading.current_thread().testStatus = bstack111lll11ll_opy_