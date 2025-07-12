# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack1111llll1ll_opy_, bstack11l1ll1l1l_opy_, bstack11ll1lll_opy_, bstack1lll1l1ll1_opy_, \
    bstack111l11lllll_opy_
from bstack_utils.measure import measure
def bstack111l1111_opy_(bstack11111111l1l_opy_):
    for driver in bstack11111111l1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11ll11l11l_opy_, stage=STAGE.bstack1111llll1_opy_)
def bstack1111l1l11_opy_(driver, status, reason=bstack11l1111_opy_ (u"࠭ࠧ὜")):
    bstack1l1l11l1ll_opy_ = Config.bstack11l1l11l11_opy_()
    if bstack1l1l11l1ll_opy_.bstack11111llll1_opy_():
        return
    bstack11lll1111_opy_ = bstack1l11111ll1_opy_(bstack11l1111_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪὝ"), bstack11l1111_opy_ (u"ࠨࠩ὞"), status, reason, bstack11l1111_opy_ (u"ࠩࠪὟ"), bstack11l1111_opy_ (u"ࠪࠫὠ"))
    driver.execute_script(bstack11lll1111_opy_)
@measure(event_name=EVENTS.bstack11ll11l11l_opy_, stage=STAGE.bstack1111llll1_opy_)
def bstack11lllll11l_opy_(page, status, reason=bstack11l1111_opy_ (u"ࠫࠬὡ")):
    try:
        if page is None:
            return
        bstack1l1l11l1ll_opy_ = Config.bstack11l1l11l11_opy_()
        if bstack1l1l11l1ll_opy_.bstack11111llll1_opy_():
            return
        bstack11lll1111_opy_ = bstack1l11111ll1_opy_(bstack11l1111_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨὢ"), bstack11l1111_opy_ (u"࠭ࠧὣ"), status, reason, bstack11l1111_opy_ (u"ࠧࠨὤ"), bstack11l1111_opy_ (u"ࠨࠩὥ"))
        page.evaluate(bstack11l1111_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥὦ"), bstack11lll1111_opy_)
    except Exception as e:
        print(bstack11l1111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡫ࡵࡲࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࢁࡽࠣὧ"), e)
def bstack1l11111ll1_opy_(type, name, status, reason, bstack11ll11lll_opy_, bstack11l1ll111_opy_):
    bstack1l1111l111_opy_ = {
        bstack11l1111_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫὨ"): type,
        bstack11l1111_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨὩ"): {}
    }
    if type == bstack11l1111_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨὪ"):
        bstack1l1111l111_opy_[bstack11l1111_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪὫ")][bstack11l1111_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧὬ")] = bstack11ll11lll_opy_
        bstack1l1111l111_opy_[bstack11l1111_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬὭ")][bstack11l1111_opy_ (u"ࠪࡨࡦࡺࡡࠨὮ")] = json.dumps(str(bstack11l1ll111_opy_))
    if type == bstack11l1111_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬὯ"):
        bstack1l1111l111_opy_[bstack11l1111_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨὰ")][bstack11l1111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫά")] = name
    if type == bstack11l1111_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪὲ"):
        bstack1l1111l111_opy_[bstack11l1111_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫέ")][bstack11l1111_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩὴ")] = status
        if status == bstack11l1111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪή") and str(reason) != bstack11l1111_opy_ (u"ࠦࠧὶ"):
            bstack1l1111l111_opy_[bstack11l1111_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨί")][bstack11l1111_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ὸ")] = json.dumps(str(reason))
    bstack1lll1ll111_opy_ = bstack11l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬό").format(json.dumps(bstack1l1111l111_opy_))
    return bstack1lll1ll111_opy_
def bstack1lll1l111_opy_(url, config, logger, bstack11l11111l_opy_=False):
    hostname = bstack11l1ll1l1l_opy_(url)
    is_private = bstack1lll1l1ll1_opy_(hostname)
    try:
        if is_private or bstack11l11111l_opy_:
            file_path = bstack1111llll1ll_opy_(bstack11l1111_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨὺ"), bstack11l1111_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨύ"), logger)
            if os.environ.get(bstack11l1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨὼ")) and eval(
                    os.environ.get(bstack11l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩώ"))):
                return
            if (bstack11l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ὾") in config and not config[bstack11l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ὿")]):
                os.environ[bstack11l1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬᾀ")] = str(True)
                bstack111111111l1_opy_ = {bstack11l1111_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪᾁ"): hostname}
                bstack111l11lllll_opy_(bstack11l1111_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨᾂ"), bstack11l1111_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨᾃ"), bstack111111111l1_opy_, logger)
    except Exception as e:
        pass
def bstack11l1111ll1_opy_(caps, bstack11111111l11_opy_):
    if bstack11l1111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᾄ") in caps:
        caps[bstack11l1111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᾅ")][bstack11l1111_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬᾆ")] = True
        if bstack11111111l11_opy_:
            caps[bstack11l1111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᾇ")][bstack11l1111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᾈ")] = bstack11111111l11_opy_
    else:
        caps[bstack11l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࠧᾉ")] = True
        if bstack11111111l11_opy_:
            caps[bstack11l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᾊ")] = bstack11111111l11_opy_
def bstack11111l111l1_opy_(bstack1111lll1l1_opy_):
    bstack111111111ll_opy_ = bstack11ll1lll_opy_(threading.current_thread(), bstack11l1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡕࡷࡥࡹࡻࡳࠨᾋ"), bstack11l1111_opy_ (u"ࠬ࠭ᾌ"))
    if bstack111111111ll_opy_ == bstack11l1111_opy_ (u"࠭ࠧᾍ") or bstack111111111ll_opy_ == bstack11l1111_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᾎ"):
        threading.current_thread().testStatus = bstack1111lll1l1_opy_
    else:
        if bstack1111lll1l1_opy_ == bstack11l1111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᾏ"):
            threading.current_thread().testStatus = bstack1111lll1l1_opy_