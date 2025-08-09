# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l111l1l11_opy_, bstack1ll11111ll_opy_, bstack1ll11l11ll_opy_, bstack11ll11l11l_opy_, \
    bstack11l11l1l11l_opy_
from bstack_utils.measure import measure
def bstack11l1ll11l1_opy_(bstack1llllll1l1ll_opy_):
    for driver in bstack1llllll1l1ll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1ll1l11l11_opy_, stage=STAGE.bstack11lll1l1_opy_)
def bstack11ll1l111_opy_(driver, status, reason=bstack11l1_opy_ (u"࠭ࠧῨ")):
    bstack1l1llll1l_opy_ = Config.bstack1l1lll11l_opy_()
    if bstack1l1llll1l_opy_.bstack1111l1ll11_opy_():
        return
    bstack1ll11llll_opy_ = bstack11l1lll11l_opy_(bstack11l1_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪῩ"), bstack11l1_opy_ (u"ࠨࠩῪ"), status, reason, bstack11l1_opy_ (u"ࠩࠪΎ"), bstack11l1_opy_ (u"ࠪࠫῬ"))
    driver.execute_script(bstack1ll11llll_opy_)
@measure(event_name=EVENTS.bstack1ll1l11l11_opy_, stage=STAGE.bstack11lll1l1_opy_)
def bstack11ll11ll11_opy_(page, status, reason=bstack11l1_opy_ (u"ࠫࠬ῭")):
    try:
        if page is None:
            return
        bstack1l1llll1l_opy_ = Config.bstack1l1lll11l_opy_()
        if bstack1l1llll1l_opy_.bstack1111l1ll11_opy_():
            return
        bstack1ll11llll_opy_ = bstack11l1lll11l_opy_(bstack11l1_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ΅"), bstack11l1_opy_ (u"࠭ࠧ`"), status, reason, bstack11l1_opy_ (u"ࠧࠨ῰"), bstack11l1_opy_ (u"ࠨࠩ῱"))
        page.evaluate(bstack11l1_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥῲ"), bstack1ll11llll_opy_)
    except Exception as e:
        print(bstack11l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡫ࡵࡲࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࢁࡽࠣῳ"), e)
def bstack11l1lll11l_opy_(type, name, status, reason, bstack11l1ll1l_opy_, bstack11l1111lll_opy_):
    bstack11111l1l1_opy_ = {
        bstack11l1_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫῴ"): type,
        bstack11l1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ῵"): {}
    }
    if type == bstack11l1_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨῶ"):
        bstack11111l1l1_opy_[bstack11l1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪῷ")][bstack11l1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧῸ")] = bstack11l1ll1l_opy_
        bstack11111l1l1_opy_[bstack11l1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬΌ")][bstack11l1_opy_ (u"ࠪࡨࡦࡺࡡࠨῺ")] = json.dumps(str(bstack11l1111lll_opy_))
    if type == bstack11l1_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬΏ"):
        bstack11111l1l1_opy_[bstack11l1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨῼ")][bstack11l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ´")] = name
    if type == bstack11l1_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪ῾"):
        bstack11111l1l1_opy_[bstack11l1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ῿")][bstack11l1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ ")] = status
        if status == bstack11l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ ") and str(reason) != bstack11l1_opy_ (u"ࠦࠧ "):
            bstack11111l1l1_opy_[bstack11l1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ ")][bstack11l1_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ ")] = json.dumps(str(reason))
    bstack1ll11lllll_opy_ = bstack11l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬ ").format(json.dumps(bstack11111l1l1_opy_))
    return bstack1ll11lllll_opy_
def bstack11l1l111l1_opy_(url, config, logger, bstack1l1111l1l_opy_=False):
    hostname = bstack1ll11111ll_opy_(url)
    is_private = bstack11ll11l11l_opy_(hostname)
    try:
        if is_private or bstack1l1111l1l_opy_:
            file_path = bstack11l111l1l11_opy_(bstack11l1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ "), bstack11l1_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨ "), logger)
            if os.environ.get(bstack11l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨ ")) and eval(
                    os.environ.get(bstack11l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩ "))):
                return
            if (bstack11l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ ") in config and not config[bstack11l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ​")]):
                os.environ[bstack11l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬ‌")] = str(True)
                bstack1llllll1l111_opy_ = {bstack11l1_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪ‍"): hostname}
                bstack11l11l1l11l_opy_(bstack11l1_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨ‎"), bstack11l1_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨ‏"), bstack1llllll1l111_opy_, logger)
    except Exception as e:
        pass
def bstack1111l1l1l_opy_(caps, bstack1llllll1l11l_opy_):
    if bstack11l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ‐") in caps:
        caps[bstack11l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭‑")][bstack11l1_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬ‒")] = True
        if bstack1llllll1l11l_opy_:
            caps[bstack11l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ–")][bstack11l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ—")] = bstack1llllll1l11l_opy_
    else:
        caps[bstack11l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࠧ―")] = True
        if bstack1llllll1l11l_opy_:
            caps[bstack11l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ‖")] = bstack1llllll1l11l_opy_
def bstack11111111l11_opy_(bstack111l1l1111_opy_):
    bstack1llllll1l1l1_opy_ = bstack1ll11l11ll_opy_(threading.current_thread(), bstack11l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡕࡷࡥࡹࡻࡳࠨ‗"), bstack11l1_opy_ (u"ࠬ࠭‘"))
    if bstack1llllll1l1l1_opy_ == bstack11l1_opy_ (u"࠭ࠧ’") or bstack1llllll1l1l1_opy_ == bstack11l1_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ‚"):
        threading.current_thread().testStatus = bstack111l1l1111_opy_
    else:
        if bstack111l1l1111_opy_ == bstack11l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ‛"):
            threading.current_thread().testStatus = bstack111l1l1111_opy_