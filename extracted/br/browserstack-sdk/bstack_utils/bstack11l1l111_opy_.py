# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l1l111lll_opy_, bstack1l1l11l111_opy_, bstack11111ll1l_opy_, bstack1ll111lll_opy_, \
    bstack11l11l1l11l_opy_
from bstack_utils.measure import measure
def bstack11lll11l1l_opy_(bstack11111111ll1_opy_):
    for driver in bstack11111111ll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l111l11_opy_, stage=STAGE.bstack11l1lll1l1_opy_)
def bstack1l1ll11lll_opy_(driver, status, reason=bstack11ll1l1_opy_ (u"ࠪࠫἚ")):
    bstack1111ll111_opy_ = Config.bstack1lllll111l_opy_()
    if bstack1111ll111_opy_.bstack1111l1111l_opy_():
        return
    bstack11lll11l11_opy_ = bstack1l11llll_opy_(bstack11ll1l1_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧἛ"), bstack11ll1l1_opy_ (u"ࠬ࠭Ἔ"), status, reason, bstack11ll1l1_opy_ (u"࠭ࠧἝ"), bstack11ll1l1_opy_ (u"ࠧࠨ἞"))
    driver.execute_script(bstack11lll11l11_opy_)
@measure(event_name=EVENTS.bstack1l111l11_opy_, stage=STAGE.bstack11l1lll1l1_opy_)
def bstack1lllll11_opy_(page, status, reason=bstack11ll1l1_opy_ (u"ࠨࠩ἟")):
    try:
        if page is None:
            return
        bstack1111ll111_opy_ = Config.bstack1lllll111l_opy_()
        if bstack1111ll111_opy_.bstack1111l1111l_opy_():
            return
        bstack11lll11l11_opy_ = bstack1l11llll_opy_(bstack11ll1l1_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬἠ"), bstack11ll1l1_opy_ (u"ࠪࠫἡ"), status, reason, bstack11ll1l1_opy_ (u"ࠫࠬἢ"), bstack11ll1l1_opy_ (u"ࠬ࠭ἣ"))
        page.evaluate(bstack11ll1l1_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢἤ"), bstack11lll11l11_opy_)
    except Exception as e:
        print(bstack11ll1l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡࡨࡲࡶࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡾࢁࠧἥ"), e)
def bstack1l11llll_opy_(type, name, status, reason, bstack111l1lll_opy_, bstack1l1ll11ll_opy_):
    bstack11lll1l1_opy_ = {
        bstack11ll1l1_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨἦ"): type,
        bstack11ll1l1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬἧ"): {}
    }
    if type == bstack11ll1l1_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬἨ"):
        bstack11lll1l1_opy_[bstack11ll1l1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧἩ")][bstack11ll1l1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫἪ")] = bstack111l1lll_opy_
        bstack11lll1l1_opy_[bstack11ll1l1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩἫ")][bstack11ll1l1_opy_ (u"ࠧࡥࡣࡷࡥࠬἬ")] = json.dumps(str(bstack1l1ll11ll_opy_))
    if type == bstack11ll1l1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩἭ"):
        bstack11lll1l1_opy_[bstack11ll1l1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬἮ")][bstack11ll1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨἯ")] = name
    if type == bstack11ll1l1_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧἰ"):
        bstack11lll1l1_opy_[bstack11ll1l1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨἱ")][bstack11ll1l1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ἲ")] = status
        if status == bstack11ll1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧἳ") and str(reason) != bstack11ll1l1_opy_ (u"ࠣࠤἴ"):
            bstack11lll1l1_opy_[bstack11ll1l1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬἵ")][bstack11ll1l1_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪἶ")] = json.dumps(str(reason))
    bstack1ll1111l_opy_ = bstack11ll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩἷ").format(json.dumps(bstack11lll1l1_opy_))
    return bstack1ll1111l_opy_
def bstack1ll1111ll_opy_(url, config, logger, bstack1111l111_opy_=False):
    hostname = bstack1l1l11l111_opy_(url)
    is_private = bstack1ll111lll_opy_(hostname)
    try:
        if is_private or bstack1111l111_opy_:
            file_path = bstack11l1l111lll_opy_(bstack11ll1l1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬἸ"), bstack11ll1l1_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬἹ"), logger)
            if os.environ.get(bstack11ll1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬἺ")) and eval(
                    os.environ.get(bstack11ll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭Ἳ"))):
                return
            if (bstack11ll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭Ἴ") in config and not config[bstack11ll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧἽ")]):
                os.environ[bstack11ll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩἾ")] = str(True)
                bstack1111111l11l_opy_ = {bstack11ll1l1_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧἿ"): hostname}
                bstack11l11l1l11l_opy_(bstack11ll1l1_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬὀ"), bstack11ll1l1_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬὁ"), bstack1111111l11l_opy_, logger)
    except Exception as e:
        pass
def bstack1l111111l1_opy_(caps, bstack1111111l111_opy_):
    if bstack11ll1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩὂ") in caps:
        caps[bstack11ll1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪὃ")][bstack11ll1l1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩὄ")] = True
        if bstack1111111l111_opy_:
            caps[bstack11ll1l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬὅ")][bstack11ll1l1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ὆")] = bstack1111111l111_opy_
    else:
        caps[bstack11ll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࠫ὇")] = True
        if bstack1111111l111_opy_:
            caps[bstack11ll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨὈ")] = bstack1111111l111_opy_
def bstack11111l1ll1l_opy_(bstack111l11lll1_opy_):
    bstack11111111lll_opy_ = bstack11111ll1l_opy_(threading.current_thread(), bstack11ll1l1_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬὉ"), bstack11ll1l1_opy_ (u"ࠩࠪὊ"))
    if bstack11111111lll_opy_ == bstack11ll1l1_opy_ (u"ࠪࠫὋ") or bstack11111111lll_opy_ == bstack11ll1l1_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬὌ"):
        threading.current_thread().testStatus = bstack111l11lll1_opy_
    else:
        if bstack111l11lll1_opy_ == bstack11ll1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬὍ"):
            threading.current_thread().testStatus = bstack111l11lll1_opy_