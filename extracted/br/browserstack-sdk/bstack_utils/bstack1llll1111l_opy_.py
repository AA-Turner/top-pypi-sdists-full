# coding: UTF-8
import sys
bstack1l1l11l_opy_ = sys.version_info [0] == 2
bstack1ll11l_opy_ = 2048
bstack1l11ll1_opy_ = 7
def bstack1l1ll1_opy_ (bstack111ll1l_opy_):
    global bstack111ll1_opy_
    bstack11ll1ll_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack1l11ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11l1l11_opy_ = bstack11ll1ll_opy_ % len (bstack1l11ll_opy_)
    bstack11ll1_opy_ = bstack1l11ll_opy_ [:bstack11l1l11_opy_] + bstack1l11ll_opy_ [bstack11l1l11_opy_:]
    if bstack1l1l11l_opy_:
        bstack111ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack111ll11_opy_ = str () .join ([chr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack111ll11_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l1111111l_opy_, bstack11lllll1l1_opy_, bstack11l1ll11ll_opy_, bstack1lll1111l1_opy_, \
    bstack11l1l111111_opy_
from bstack_utils.measure import measure
def bstack11ll1l1ll_opy_(bstack1111111l111_opy_):
    for driver in bstack1111111l111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1ll1llllll_opy_, stage=STAGE.bstack1l1ll11ll1_opy_)
def bstack1l1ll1lll1_opy_(driver, status, reason=bstack1l1ll1_opy_ (u"ࠪࠫἚ")):
    bstack11lll111ll_opy_ = Config.bstack11ll1l11l_opy_()
    if bstack11lll111ll_opy_.bstack1111ll11ll_opy_():
        return
    bstack1lllllll11_opy_ = bstack111111ll1_opy_(bstack1l1ll1_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧἛ"), bstack1l1ll1_opy_ (u"ࠬ࠭Ἔ"), status, reason, bstack1l1ll1_opy_ (u"࠭ࠧἝ"), bstack1l1ll1_opy_ (u"ࠧࠨ἞"))
    driver.execute_script(bstack1lllllll11_opy_)
@measure(event_name=EVENTS.bstack1ll1llllll_opy_, stage=STAGE.bstack1l1ll11ll1_opy_)
def bstack1ll1111l11_opy_(page, status, reason=bstack1l1ll1_opy_ (u"ࠨࠩ἟")):
    try:
        if page is None:
            return
        bstack11lll111ll_opy_ = Config.bstack11ll1l11l_opy_()
        if bstack11lll111ll_opy_.bstack1111ll11ll_opy_():
            return
        bstack1lllllll11_opy_ = bstack111111ll1_opy_(bstack1l1ll1_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬἠ"), bstack1l1ll1_opy_ (u"ࠪࠫἡ"), status, reason, bstack1l1ll1_opy_ (u"ࠫࠬἢ"), bstack1l1ll1_opy_ (u"ࠬ࠭ἣ"))
        page.evaluate(bstack1l1ll1_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢἤ"), bstack1lllllll11_opy_)
    except Exception as e:
        print(bstack1l1ll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡࡨࡲࡶࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡾࢁࠧἥ"), e)
def bstack111111ll1_opy_(type, name, status, reason, bstack1lll1111_opy_, bstack11ll1111ll_opy_):
    bstack1llllllll1_opy_ = {
        bstack1l1ll1_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨἦ"): type,
        bstack1l1ll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬἧ"): {}
    }
    if type == bstack1l1ll1_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬἨ"):
        bstack1llllllll1_opy_[bstack1l1ll1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧἩ")][bstack1l1ll1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫἪ")] = bstack1lll1111_opy_
        bstack1llllllll1_opy_[bstack1l1ll1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩἫ")][bstack1l1ll1_opy_ (u"ࠧࡥࡣࡷࡥࠬἬ")] = json.dumps(str(bstack11ll1111ll_opy_))
    if type == bstack1l1ll1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩἭ"):
        bstack1llllllll1_opy_[bstack1l1ll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬἮ")][bstack1l1ll1_opy_ (u"ࠪࡲࡦࡳࡥࠨἯ")] = name
    if type == bstack1l1ll1_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧἰ"):
        bstack1llllllll1_opy_[bstack1l1ll1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨἱ")][bstack1l1ll1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ἲ")] = status
        if status == bstack1l1ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧἳ") and str(reason) != bstack1l1ll1_opy_ (u"ࠣࠤἴ"):
            bstack1llllllll1_opy_[bstack1l1ll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬἵ")][bstack1l1ll1_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪἶ")] = json.dumps(str(reason))
    bstack11lllllll_opy_ = bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩἷ").format(json.dumps(bstack1llllllll1_opy_))
    return bstack11lllllll_opy_
def bstack11ll1lllll_opy_(url, config, logger, bstack1ll1l11l_opy_=False):
    hostname = bstack11lllll1l1_opy_(url)
    is_private = bstack1lll1111l1_opy_(hostname)
    try:
        if is_private or bstack1ll1l11l_opy_:
            file_path = bstack11l1111111l_opy_(bstack1l1ll1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬἸ"), bstack1l1ll1_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬἹ"), logger)
            if os.environ.get(bstack1l1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬἺ")) and eval(
                    os.environ.get(bstack1l1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭Ἳ"))):
                return
            if (bstack1l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭Ἴ") in config and not config[bstack1l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧἽ")]):
                os.environ[bstack1l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩἾ")] = str(True)
                bstack11111111lll_opy_ = {bstack1l1ll1_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧἿ"): hostname}
                bstack11l1l111111_opy_(bstack1l1ll1_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬὀ"), bstack1l1ll1_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬὁ"), bstack11111111lll_opy_, logger)
    except Exception as e:
        pass
def bstack11lll11l1l_opy_(caps, bstack1111111l11l_opy_):
    if bstack1l1ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩὂ") in caps:
        caps[bstack1l1ll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪὃ")][bstack1l1ll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩὄ")] = True
        if bstack1111111l11l_opy_:
            caps[bstack1l1ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬὅ")][bstack1l1ll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ὆")] = bstack1111111l11l_opy_
    else:
        caps[bstack1l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࠫ὇")] = True
        if bstack1111111l11l_opy_:
            caps[bstack1l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨὈ")] = bstack1111111l11l_opy_
def bstack11111l11lll_opy_(bstack1111llllll_opy_):
    bstack1111111l1l1_opy_ = bstack11l1ll11ll_opy_(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬὉ"), bstack1l1ll1_opy_ (u"ࠩࠪὊ"))
    if bstack1111111l1l1_opy_ == bstack1l1ll1_opy_ (u"ࠪࠫὋ") or bstack1111111l1l1_opy_ == bstack1l1ll1_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬὌ"):
        threading.current_thread().testStatus = bstack1111llllll_opy_
    else:
        if bstack1111llllll_opy_ == bstack1l1ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬὍ"):
            threading.current_thread().testStatus = bstack1111llllll_opy_