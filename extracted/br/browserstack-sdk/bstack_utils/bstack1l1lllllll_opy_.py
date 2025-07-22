# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l1l111111_opy_, bstack11lll1l1l_opy_, bstack1ll11lllll_opy_, bstack11l1l111l1_opy_, \
    bstack111lll11lll_opy_
from bstack_utils.measure import measure
def bstack111ll1l11_opy_(bstack111111111l1_opy_):
    for driver in bstack111111111l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11l11l11l1_opy_, stage=STAGE.bstack11l1llll1_opy_)
def bstack1l11ll11ll_opy_(driver, status, reason=bstack111l111_opy_ (u"ࠪࠫὠ")):
    bstack1ll1ll11_opy_ = Config.bstack1ll11ll1_opy_()
    if bstack1ll1ll11_opy_.bstack1111l1l1l1_opy_():
        return
    bstack1l11llll1_opy_ = bstack1llll1111l_opy_(bstack111l111_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧὡ"), bstack111l111_opy_ (u"ࠬ࠭ὢ"), status, reason, bstack111l111_opy_ (u"࠭ࠧὣ"), bstack111l111_opy_ (u"ࠧࠨὤ"))
    driver.execute_script(bstack1l11llll1_opy_)
@measure(event_name=EVENTS.bstack11l11l11l1_opy_, stage=STAGE.bstack11l1llll1_opy_)
def bstack1lllllll1_opy_(page, status, reason=bstack111l111_opy_ (u"ࠨࠩὥ")):
    try:
        if page is None:
            return
        bstack1ll1ll11_opy_ = Config.bstack1ll11ll1_opy_()
        if bstack1ll1ll11_opy_.bstack1111l1l1l1_opy_():
            return
        bstack1l11llll1_opy_ = bstack1llll1111l_opy_(bstack111l111_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬὦ"), bstack111l111_opy_ (u"ࠪࠫὧ"), status, reason, bstack111l111_opy_ (u"ࠫࠬὨ"), bstack111l111_opy_ (u"ࠬ࠭Ὡ"))
        page.evaluate(bstack111l111_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢὪ"), bstack1l11llll1_opy_)
    except Exception as e:
        print(bstack111l111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡࡨࡲࡶࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡾࢁࠧὫ"), e)
def bstack1llll1111l_opy_(type, name, status, reason, bstack1l1l11ll_opy_, bstack1ll1l1l111_opy_):
    bstack11ll111l11_opy_ = {
        bstack111l111_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨὬ"): type,
        bstack111l111_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬὭ"): {}
    }
    if type == bstack111l111_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬὮ"):
        bstack11ll111l11_opy_[bstack111l111_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧὯ")][bstack111l111_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫὰ")] = bstack1l1l11ll_opy_
        bstack11ll111l11_opy_[bstack111l111_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩά")][bstack111l111_opy_ (u"ࠧࡥࡣࡷࡥࠬὲ")] = json.dumps(str(bstack1ll1l1l111_opy_))
    if type == bstack111l111_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩέ"):
        bstack11ll111l11_opy_[bstack111l111_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬὴ")][bstack111l111_opy_ (u"ࠪࡲࡦࡳࡥࠨή")] = name
    if type == bstack111l111_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧὶ"):
        bstack11ll111l11_opy_[bstack111l111_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨί")][bstack111l111_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ὸ")] = status
        if status == bstack111l111_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧό") and str(reason) != bstack111l111_opy_ (u"ࠣࠤὺ"):
            bstack11ll111l11_opy_[bstack111l111_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬύ")][bstack111l111_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪὼ")] = json.dumps(str(reason))
    bstack111lllllll_opy_ = bstack111l111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩώ").format(json.dumps(bstack11ll111l11_opy_))
    return bstack111lllllll_opy_
def bstack111l1llll_opy_(url, config, logger, bstack1lll1l111l_opy_=False):
    hostname = bstack11lll1l1l_opy_(url)
    is_private = bstack11l1l111l1_opy_(hostname)
    try:
        if is_private or bstack1lll1l111l_opy_:
            file_path = bstack11l1l111111_opy_(bstack111l111_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ὾"), bstack111l111_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬ὿"), logger)
            if os.environ.get(bstack111l111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬᾀ")) and eval(
                    os.environ.get(bstack111l111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭ᾁ"))):
                return
            if (bstack111l111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᾂ") in config and not config[bstack111l111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᾃ")]):
                os.environ[bstack111l111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩᾄ")] = str(True)
                bstack1111111111l_opy_ = {bstack111l111_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧᾅ"): hostname}
                bstack111lll11lll_opy_(bstack111l111_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬᾆ"), bstack111l111_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬᾇ"), bstack1111111111l_opy_, logger)
    except Exception as e:
        pass
def bstack1l111l1l11_opy_(caps, bstack111111111ll_opy_):
    if bstack111l111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᾈ") in caps:
        caps[bstack111l111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᾉ")][bstack111l111_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩᾊ")] = True
        if bstack111111111ll_opy_:
            caps[bstack111l111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᾋ")][bstack111l111_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᾌ")] = bstack111111111ll_opy_
    else:
        caps[bstack111l111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࠫᾍ")] = True
        if bstack111111111ll_opy_:
            caps[bstack111l111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᾎ")] = bstack111111111ll_opy_
def bstack11111l11lll_opy_(bstack1111ll11ll_opy_):
    bstack11111111111_opy_ = bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬᾏ"), bstack111l111_opy_ (u"ࠩࠪᾐ"))
    if bstack11111111111_opy_ == bstack111l111_opy_ (u"ࠪࠫᾑ") or bstack11111111111_opy_ == bstack111l111_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᾒ"):
        threading.current_thread().testStatus = bstack1111ll11ll_opy_
    else:
        if bstack1111ll11ll_opy_ == bstack111l111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᾓ"):
            threading.current_thread().testStatus = bstack1111ll11ll_opy_