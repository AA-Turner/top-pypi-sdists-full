# coding: UTF-8
import sys
bstack111l1l1_opy_ = sys.version_info [0] == 2
bstack1ll1l1l_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack11lll_opy_ (bstack111ll1l_opy_):
    global bstack1l111l_opy_
    bstack1lllll1l_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack11111ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11ll1l1_opy_ = bstack1lllll1l_opy_ % len (bstack11111ll_opy_)
    bstack1lll1l1_opy_ = bstack11111ll_opy_ [:bstack11ll1l1_opy_] + bstack11111ll_opy_ [bstack11ll1l1_opy_:]
    if bstack111l1l1_opy_:
        bstack1ll1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    else:
        bstack1ll1ll1_opy_ = str () .join ([chr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    return eval (bstack1ll1ll1_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l1lllll1l_opy_, bstack1l1l1l1111_opy_, bstack1llll11ll1_opy_, bstack11l11ll1l1_opy_, \
    bstack11l1l1l11ll_opy_
from bstack_utils.measure import measure
def bstack11ll1l1lll_opy_(bstack111l111l111_opy_):
    for driver in bstack111l111l111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l11l1ll11_opy_, stage=STAGE.bstack11l111ll_opy_)
def bstack1l1111lll1_opy_(driver, status, reason=bstack11lll_opy_ (u"ࠩࠪᶘ")):
    bstack1llllll11_opy_ = Config.bstack1l1l1l1ll1_opy_()
    if bstack1llllll11_opy_.bstack1111ll11ll_opy_():
        return
    bstack11llll111_opy_ = bstack1l11l1lll1_opy_(bstack11lll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᶙ"), bstack11lll_opy_ (u"ࠫࠬᶚ"), status, reason, bstack11lll_opy_ (u"ࠬ࠭ᶛ"), bstack11lll_opy_ (u"࠭ࠧᶜ"))
    driver.execute_script(bstack11llll111_opy_)
@measure(event_name=EVENTS.bstack1l11l1ll11_opy_, stage=STAGE.bstack11l111ll_opy_)
def bstack11l1l11l_opy_(page, status, reason=bstack11lll_opy_ (u"ࠧࠨᶝ")):
    try:
        if page is None:
            return
        bstack1llllll11_opy_ = Config.bstack1l1l1l1ll1_opy_()
        if bstack1llllll11_opy_.bstack1111ll11ll_opy_():
            return
        bstack11llll111_opy_ = bstack1l11l1lll1_opy_(bstack11lll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᶞ"), bstack11lll_opy_ (u"ࠩࠪᶟ"), status, reason, bstack11lll_opy_ (u"ࠪࠫᶠ"), bstack11lll_opy_ (u"ࠫࠬᶡ"))
        page.evaluate(bstack11lll_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨᶢ"), bstack11llll111_opy_)
    except Exception as e:
        print(bstack11lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡽࢀࠦᶣ"), e)
def bstack1l11l1lll1_opy_(type, name, status, reason, bstack11lll1111l_opy_, bstack1ll1l1l1_opy_):
    bstack11ll11l11l_opy_ = {
        bstack11lll_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧᶤ"): type,
        bstack11lll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᶥ"): {}
    }
    if type == bstack11lll_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫᶦ"):
        bstack11ll11l11l_opy_[bstack11lll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᶧ")][bstack11lll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᶨ")] = bstack11lll1111l_opy_
        bstack11ll11l11l_opy_[bstack11lll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᶩ")][bstack11lll_opy_ (u"࠭ࡤࡢࡶࡤࠫᶪ")] = json.dumps(str(bstack1ll1l1l1_opy_))
    if type == bstack11lll_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᶫ"):
        bstack11ll11l11l_opy_[bstack11lll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᶬ")][bstack11lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᶭ")] = name
    if type == bstack11lll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᶮ"):
        bstack11ll11l11l_opy_[bstack11lll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᶯ")][bstack11lll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᶰ")] = status
        if status == bstack11lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᶱ") and str(reason) != bstack11lll_opy_ (u"ࠢࠣᶲ"):
            bstack11ll11l11l_opy_[bstack11lll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᶳ")][bstack11lll_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩᶴ")] = json.dumps(str(reason))
    bstack11l1ll1ll1_opy_ = bstack11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨᶵ").format(json.dumps(bstack11ll11l11l_opy_))
    return bstack11l1ll1ll1_opy_
def bstack1l1l111l_opy_(url, config, logger, bstack11ll1llll_opy_=False):
    hostname = bstack1l1l1l1111_opy_(url)
    is_private = bstack11l11ll1l1_opy_(hostname)
    try:
        if is_private or bstack11ll1llll_opy_:
            file_path = bstack11l1lllll1l_opy_(bstack11lll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᶶ"), bstack11lll_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᶷ"), logger)
            if os.environ.get(bstack11lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫᶸ")) and eval(
                    os.environ.get(bstack11lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬᶹ"))):
                return
            if (bstack11lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᶺ") in config and not config[bstack11lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᶻ")]):
                os.environ[bstack11lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨᶼ")] = str(True)
                bstack111l1111lll_opy_ = {bstack11lll_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ᶽ"): hostname}
                bstack11l1l1l11ll_opy_(bstack11lll_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᶾ"), bstack11lll_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫᶿ"), bstack111l1111lll_opy_, logger)
    except Exception as e:
        pass
def bstack1l1l11111_opy_(caps, bstack111l111l11l_opy_):
    if bstack11lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ᷀") in caps:
        caps[bstack11lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᷁")][bstack11lll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨ᷂")] = True
        if bstack111l111l11l_opy_:
            caps[bstack11lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ᷃")][bstack11lll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭᷄")] = bstack111l111l11l_opy_
    else:
        caps[bstack11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪ᷅")] = True
        if bstack111l111l11l_opy_:
            caps[bstack11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ᷆")] = bstack111l111l11l_opy_
def bstack111l1l11lll_opy_(bstack111l1l1l1l_opy_):
    bstack111l1111ll1_opy_ = bstack1llll11ll1_opy_(threading.current_thread(), bstack11lll_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫ᷇"), bstack11lll_opy_ (u"ࠨࠩ᷈"))
    if bstack111l1111ll1_opy_ == bstack11lll_opy_ (u"ࠩࠪ᷉") or bstack111l1111ll1_opy_ == bstack11lll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧ᷊ࠫ"):
        threading.current_thread().testStatus = bstack111l1l1l1l_opy_
    else:
        if bstack111l1l1l1l_opy_ == bstack11lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ᷋"):
            threading.current_thread().testStatus = bstack111l1l1l1l_opy_