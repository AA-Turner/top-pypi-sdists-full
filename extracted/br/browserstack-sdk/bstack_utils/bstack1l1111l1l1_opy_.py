# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l1l111l11_opy_, bstack1l1ll1ll1l_opy_, bstack11ll1111ll_opy_, bstack1l11ll1l1l_opy_, \
    bstack11l1111l1ll_opy_
from bstack_utils.measure import measure
def bstack11l1ll1111_opy_(bstack11111111111_opy_):
    for driver in bstack11111111111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1lll1ll1l_opy_, stage=STAGE.bstack1l1111ll1_opy_)
def bstack1l1lll11ll_opy_(driver, status, reason=bstackl_opy_ (u"ࠫࠬὡ")):
    bstack1l1llll1l1_opy_ = Config.bstack1l1l11ll_opy_()
    if bstack1l1llll1l1_opy_.bstack11111lllll_opy_():
        return
    bstack11l11111_opy_ = bstack11l1l1l1l_opy_(bstackl_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨὢ"), bstackl_opy_ (u"࠭ࠧὣ"), status, reason, bstackl_opy_ (u"ࠧࠨὤ"), bstackl_opy_ (u"ࠨࠩὥ"))
    driver.execute_script(bstack11l11111_opy_)
@measure(event_name=EVENTS.bstack1lll1ll1l_opy_, stage=STAGE.bstack1l1111ll1_opy_)
def bstack1l1l111l11_opy_(page, status, reason=bstackl_opy_ (u"ࠩࠪὦ")):
    try:
        if page is None:
            return
        bstack1l1llll1l1_opy_ = Config.bstack1l1l11ll_opy_()
        if bstack1l1llll1l1_opy_.bstack11111lllll_opy_():
            return
        bstack11l11111_opy_ = bstack11l1l1l1l_opy_(bstackl_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ὧ"), bstackl_opy_ (u"ࠫࠬὨ"), status, reason, bstackl_opy_ (u"ࠬ࠭Ὡ"), bstackl_opy_ (u"࠭ࠧὪ"))
        page.evaluate(bstackl_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣὫ"), bstack11l11111_opy_)
    except Exception as e:
        print(bstackl_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢࡩࡳࡷࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡿࢂࠨὬ"), e)
def bstack11l1l1l1l_opy_(type, name, status, reason, bstack111llll1_opy_, bstack111l1l111_opy_):
    bstack11lllll11l_opy_ = {
        bstackl_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩὭ"): type,
        bstackl_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭Ὦ"): {}
    }
    if type == bstackl_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭Ὧ"):
        bstack11lllll11l_opy_[bstackl_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨὰ")][bstackl_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬά")] = bstack111llll1_opy_
        bstack11lllll11l_opy_[bstackl_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪὲ")][bstackl_opy_ (u"ࠨࡦࡤࡸࡦ࠭έ")] = json.dumps(str(bstack111l1l111_opy_))
    if type == bstackl_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪὴ"):
        bstack11lllll11l_opy_[bstackl_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ή")][bstackl_opy_ (u"ࠫࡳࡧ࡭ࡦࠩὶ")] = name
    if type == bstackl_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨί"):
        bstack11lllll11l_opy_[bstackl_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩὸ")][bstackl_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧό")] = status
        if status == bstackl_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨὺ") and str(reason) != bstackl_opy_ (u"ࠤࠥύ"):
            bstack11lllll11l_opy_[bstackl_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ὼ")][bstackl_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫώ")] = json.dumps(str(reason))
    bstack1ll11lll1_opy_ = bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪ὾").format(json.dumps(bstack11lllll11l_opy_))
    return bstack1ll11lll1_opy_
def bstack1l11111l_opy_(url, config, logger, bstack11l1lll11l_opy_=False):
    hostname = bstack1l1ll1ll1l_opy_(url)
    is_private = bstack1l11ll1l1l_opy_(hostname)
    try:
        if is_private or bstack11l1lll11l_opy_:
            file_path = bstack11l1l111l11_opy_(bstackl_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭὿"), bstackl_opy_ (u"ࠧ࠯ࡤࡶࡸࡦࡩ࡫࠮ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭ᾀ"), logger)
            if os.environ.get(bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭ᾁ")) and eval(
                    os.environ.get(bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧᾂ"))):
                return
            if (bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᾃ") in config and not config[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨᾄ")]):
                os.environ[bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪᾅ")] = str(True)
                bstack1111111111l_opy_ = {bstackl_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨᾆ"): hostname}
                bstack11l1111l1ll_opy_(bstackl_opy_ (u"ࠧ࠯ࡤࡶࡸࡦࡩ࡫࠮ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭ᾇ"), bstackl_opy_ (u"ࠨࡰࡸࡨ࡬࡫࡟࡭ࡱࡦࡥࡱ࠭ᾈ"), bstack1111111111l_opy_, logger)
    except Exception as e:
        pass
def bstack11l1l1lll_opy_(caps, bstack111111111l1_opy_):
    if bstackl_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᾉ") in caps:
        caps[bstackl_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᾊ")][bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࠪᾋ")] = True
        if bstack111111111l1_opy_:
            caps[bstackl_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᾌ")][bstackl_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᾍ")] = bstack111111111l1_opy_
    else:
        caps[bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࠬᾎ")] = True
        if bstack111111111l1_opy_:
            caps[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᾏ")] = bstack111111111l1_opy_
def bstack11111l1l111_opy_(bstack111l11ll11_opy_):
    bstack1lllllllllll_opy_ = bstack11ll1111ll_opy_(threading.current_thread(), bstackl_opy_ (u"ࠩࡷࡩࡸࡺࡓࡵࡣࡷࡹࡸ࠭ᾐ"), bstackl_opy_ (u"ࠪࠫᾑ"))
    if bstack1lllllllllll_opy_ == bstackl_opy_ (u"ࠫࠬᾒ") or bstack1lllllllllll_opy_ == bstackl_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᾓ"):
        threading.current_thread().testStatus = bstack111l11ll11_opy_
    else:
        if bstack111l11ll11_opy_ == bstackl_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᾔ"):
            threading.current_thread().testStatus = bstack111l11ll11_opy_