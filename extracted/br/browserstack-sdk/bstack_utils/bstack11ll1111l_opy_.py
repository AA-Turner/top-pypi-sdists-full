# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l1l1l1l1l_opy_, bstack11l1l1l11l_opy_, bstack11l11l1ll1_opy_, bstack11l1lll1l1_opy_, \
    bstack11l1l11l111_opy_
from bstack_utils.measure import measure
def bstack1l111l11l_opy_(bstack111l111l11l_opy_):
    for driver in bstack111l111l11l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11l1lll11_opy_, stage=STAGE.bstack1l1ll11ll1_opy_)
def bstack11l1111l1_opy_(driver, status, reason=bstack1l11lll_opy_ (u"ࠬ࠭ᶍ")):
    bstack11lll1l1ll_opy_ = Config.bstack1lll1l1lll_opy_()
    if bstack11lll1l1ll_opy_.bstack1111llll11_opy_():
        return
    bstack1ll1lll1l_opy_ = bstack11ll11l111_opy_(bstack1l11lll_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩᶎ"), bstack1l11lll_opy_ (u"ࠧࠨᶏ"), status, reason, bstack1l11lll_opy_ (u"ࠨࠩᶐ"), bstack1l11lll_opy_ (u"ࠩࠪᶑ"))
    driver.execute_script(bstack1ll1lll1l_opy_)
@measure(event_name=EVENTS.bstack11l1lll11_opy_, stage=STAGE.bstack1l1ll11ll1_opy_)
def bstack1lll111l11_opy_(page, status, reason=bstack1l11lll_opy_ (u"ࠪࠫᶒ")):
    try:
        if page is None:
            return
        bstack11lll1l1ll_opy_ = Config.bstack1lll1l1lll_opy_()
        if bstack11lll1l1ll_opy_.bstack1111llll11_opy_():
            return
        bstack1ll1lll1l_opy_ = bstack11ll11l111_opy_(bstack1l11lll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧᶓ"), bstack1l11lll_opy_ (u"ࠬ࠭ᶔ"), status, reason, bstack1l11lll_opy_ (u"࠭ࠧᶕ"), bstack1l11lll_opy_ (u"ࠧࠨᶖ"))
        page.evaluate(bstack1l11lll_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤᶗ"), bstack1ll1lll1l_opy_)
    except Exception as e:
        print(bstack1l11lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࢀࢃࠢᶘ"), e)
def bstack11ll11l111_opy_(type, name, status, reason, bstack11llllll_opy_, bstack1ll1ll1ll_opy_):
    bstack1ll1l1111_opy_ = {
        bstack1l11lll_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪᶙ"): type,
        bstack1l11lll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᶚ"): {}
    }
    if type == bstack1l11lll_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧᶛ"):
        bstack1ll1l1111_opy_[bstack1l11lll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᶜ")][bstack1l11lll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᶝ")] = bstack11llllll_opy_
        bstack1ll1l1111_opy_[bstack1l11lll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᶞ")][bstack1l11lll_opy_ (u"ࠩࡧࡥࡹࡧࠧᶟ")] = json.dumps(str(bstack1ll1ll1ll_opy_))
    if type == bstack1l11lll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᶠ"):
        bstack1ll1l1111_opy_[bstack1l11lll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᶡ")][bstack1l11lll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᶢ")] = name
    if type == bstack1l11lll_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩᶣ"):
        bstack1ll1l1111_opy_[bstack1l11lll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᶤ")][bstack1l11lll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᶥ")] = status
        if status == bstack1l11lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᶦ") and str(reason) != bstack1l11lll_opy_ (u"ࠥࠦᶧ"):
            bstack1ll1l1111_opy_[bstack1l11lll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᶨ")][bstack1l11lll_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬᶩ")] = json.dumps(str(reason))
    bstack11lll11111_opy_ = bstack1l11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫᶪ").format(json.dumps(bstack1ll1l1111_opy_))
    return bstack11lll11111_opy_
def bstack11ll111l11_opy_(url, config, logger, bstack11lll11ll_opy_=False):
    hostname = bstack11l1l1l11l_opy_(url)
    is_private = bstack11l1lll1l1_opy_(hostname)
    try:
        if is_private or bstack11lll11ll_opy_:
            file_path = bstack11l1l1l1l1l_opy_(bstack1l11lll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᶫ"), bstack1l11lll_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧᶬ"), logger)
            if os.environ.get(bstack1l11lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧᶭ")) and eval(
                    os.environ.get(bstack1l11lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨᶮ"))):
                return
            if (bstack1l11lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨᶯ") in config and not config[bstack1l11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩᶰ")]):
                os.environ[bstack1l11lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫᶱ")] = str(True)
                bstack111l111l1l1_opy_ = {bstack1l11lll_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩᶲ"): hostname}
                bstack11l1l11l111_opy_(bstack1l11lll_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧᶳ"), bstack1l11lll_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧᶴ"), bstack111l111l1l1_opy_, logger)
    except Exception as e:
        pass
def bstack11l1l1l1ll_opy_(caps, bstack111l111l111_opy_):
    if bstack1l11lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᶵ") in caps:
        caps[bstack1l11lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᶶ")][bstack1l11lll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫᶷ")] = True
        if bstack111l111l111_opy_:
            caps[bstack1l11lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᶸ")][bstack1l11lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᶹ")] = bstack111l111l111_opy_
    else:
        caps[bstack1l11lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭ᶺ")] = True
        if bstack111l111l111_opy_:
            caps[bstack1l11lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᶻ")] = bstack111l111l111_opy_
def bstack111l1l11ll1_opy_(bstack111ll1l11l_opy_):
    bstack111l111l1ll_opy_ = bstack11l11l1ll1_opy_(threading.current_thread(), bstack1l11lll_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧᶼ"), bstack1l11lll_opy_ (u"ࠫࠬᶽ"))
    if bstack111l111l1ll_opy_ == bstack1l11lll_opy_ (u"ࠬ࠭ᶾ") or bstack111l111l1ll_opy_ == bstack1l11lll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᶿ"):
        threading.current_thread().testStatus = bstack111ll1l11l_opy_
    else:
        if bstack111ll1l11l_opy_ == bstack1l11lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ᷀"):
            threading.current_thread().testStatus = bstack111ll1l11l_opy_