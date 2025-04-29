# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack111l1l1_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1llllll_opy_ (bstack1ll111l_opy_):
    global bstack1l111l_opy_
    bstack1l11l_opy_ = ord (bstack1ll111l_opy_ [-1])
    bstack1111l1l_opy_ = bstack1ll111l_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack1l11l_opy_ % len (bstack1111l1l_opy_)
    bstack1ll1_opy_ = bstack1111l1l_opy_ [:bstack11ll1ll_opy_] + bstack1111l1l_opy_ [bstack11ll1ll_opy_:]
    if bstack11l1l1_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1lllll1l_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l11llll11_opy_, bstack11ll1l11l1_opy_, bstack1lll11l1_opy_, bstack11llll1111_opy_, \
    bstack11l1lll11l1_opy_
from bstack_utils.measure import measure
def bstack1l111ll1_opy_(bstack111l111l1ll_opy_):
    for driver in bstack111l111l1ll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l1lll11l1_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
def bstack1ll1l1l1l1_opy_(driver, status, reason=bstack1llllll_opy_ (u"ࠧࠨᶏ")):
    bstack1l1ll1l1l1_opy_ = Config.bstack11ll1ll1l1_opy_()
    if bstack1l1ll1l1l1_opy_.bstack1111lllll1_opy_():
        return
    bstack1l11ll1l1_opy_ = bstack1111l111_opy_(bstack1llllll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᶐ"), bstack1llllll_opy_ (u"ࠩࠪᶑ"), status, reason, bstack1llllll_opy_ (u"ࠪࠫᶒ"), bstack1llllll_opy_ (u"ࠫࠬᶓ"))
    driver.execute_script(bstack1l11ll1l1_opy_)
@measure(event_name=EVENTS.bstack1l1lll11l1_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
def bstack1ll1l1lll_opy_(page, status, reason=bstack1llllll_opy_ (u"ࠬ࠭ᶔ")):
    try:
        if page is None:
            return
        bstack1l1ll1l1l1_opy_ = Config.bstack11ll1ll1l1_opy_()
        if bstack1l1ll1l1l1_opy_.bstack1111lllll1_opy_():
            return
        bstack1l11ll1l1_opy_ = bstack1111l111_opy_(bstack1llllll_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩᶕ"), bstack1llllll_opy_ (u"ࠧࠨᶖ"), status, reason, bstack1llllll_opy_ (u"ࠨࠩᶗ"), bstack1llllll_opy_ (u"ࠩࠪᶘ"))
        page.evaluate(bstack1llllll_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦᶙ"), bstack1l11ll1l1_opy_)
    except Exception as e:
        print(bstack1llllll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡻࡾࠤᶚ"), e)
def bstack1111l111_opy_(type, name, status, reason, bstack11lll1llll_opy_, bstack1l1lllll_opy_):
    bstack1ll11111l1_opy_ = {
        bstack1llllll_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬᶛ"): type,
        bstack1llllll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᶜ"): {}
    }
    if type == bstack1llllll_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩᶝ"):
        bstack1ll11111l1_opy_[bstack1llllll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᶞ")][bstack1llllll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᶟ")] = bstack11lll1llll_opy_
        bstack1ll11111l1_opy_[bstack1llllll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᶠ")][bstack1llllll_opy_ (u"ࠫࡩࡧࡴࡢࠩᶡ")] = json.dumps(str(bstack1l1lllll_opy_))
    if type == bstack1llllll_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᶢ"):
        bstack1ll11111l1_opy_[bstack1llllll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᶣ")][bstack1llllll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᶤ")] = name
    if type == bstack1llllll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᶥ"):
        bstack1ll11111l1_opy_[bstack1llllll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᶦ")][bstack1llllll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᶧ")] = status
        if status == bstack1llllll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᶨ") and str(reason) != bstack1llllll_opy_ (u"ࠧࠨᶩ"):
            bstack1ll11111l1_opy_[bstack1llllll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᶪ")][bstack1llllll_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧᶫ")] = json.dumps(str(reason))
    bstack11ll1l111_opy_ = bstack1llllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ᶬ").format(json.dumps(bstack1ll11111l1_opy_))
    return bstack11ll1l111_opy_
def bstack111lll1ll_opy_(url, config, logger, bstack11l11l111_opy_=False):
    hostname = bstack11ll1l11l1_opy_(url)
    is_private = bstack11llll1111_opy_(hostname)
    try:
        if is_private or bstack11l11l111_opy_:
            file_path = bstack11l11llll11_opy_(bstack1llllll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᶭ"), bstack1llllll_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᶮ"), logger)
            if os.environ.get(bstack1llllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩᶯ")) and eval(
                    os.environ.get(bstack1llllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪᶰ"))):
                return
            if (bstack1llllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᶱ") in config and not config[bstack1llllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᶲ")]):
                os.environ[bstack1llllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭ᶳ")] = str(True)
                bstack111l111l11l_opy_ = {bstack1llllll_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫᶴ"): hostname}
                bstack11l1lll11l1_opy_(bstack1llllll_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᶵ"), bstack1llllll_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩᶶ"), bstack111l111l11l_opy_, logger)
    except Exception as e:
        pass
def bstack11ll1111l1_opy_(caps, bstack111l111l111_opy_):
    if bstack1llllll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᶷ") in caps:
        caps[bstack1llllll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᶸ")][bstack1llllll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭ᶹ")] = True
        if bstack111l111l111_opy_:
            caps[bstack1llllll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᶺ")][bstack1llllll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᶻ")] = bstack111l111l111_opy_
    else:
        caps[bstack1llllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨᶼ")] = True
        if bstack111l111l111_opy_:
            caps[bstack1llllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᶽ")] = bstack111l111l111_opy_
def bstack111l1l1ll11_opy_(bstack111ll1l11l_opy_):
    bstack111l111l1l1_opy_ = bstack1lll11l1_opy_(threading.current_thread(), bstack1llllll_opy_ (u"ࠬࡺࡥࡴࡶࡖࡸࡦࡺࡵࡴࠩᶾ"), bstack1llllll_opy_ (u"࠭ࠧᶿ"))
    if bstack111l111l1l1_opy_ == bstack1llllll_opy_ (u"ࠧࠨ᷀") or bstack111l111l1l1_opy_ == bstack1llllll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ᷁"):
        threading.current_thread().testStatus = bstack111ll1l11l_opy_
    else:
        if bstack111ll1l11l_opy_ == bstack1llllll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥ᷂ࠩ"):
            threading.current_thread().testStatus = bstack111ll1l11l_opy_